from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional, Sequence, Tuple

from .models import ActivityRecord, LearnerProgress, ProgressPacket


class ValidationError(ValueError):
    def __init__(self, errors: Sequence[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


def load_json_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(("input: malformed JSON",)) from exc
    except OSError as exc:
        raise ValidationError(("input: unable to read packet",)) from exc


def parse_date(value: Any, field_path: str, now: Optional[datetime] = None) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError((f"{field_path}: date must be a non-empty string",))
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError((f"{field_path}: invalid date",)) from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    reference = now or datetime.now(timezone.utc)
    if parsed > reference:
        raise ValidationError((f"{field_path}: future date is not allowed",))
    return parsed


def _required(mapping: dict, key: str, path: str, errors: List[str]) -> Any:
    if key not in mapping:
        errors.append(f"{path}.{key}: required field is missing")
        return None
    return mapping[key]


def _activity(value: Any, path: str, kind: str, errors: List[str]) -> Tuple[ActivityRecord, ...]:
    if not isinstance(value, list):
        errors.append(f"{path}: must be a list")
        return ()
    records = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_path}: must be an object")
            continue
        date_value = item.get("date_timestamp")
        try:
            date = parse_date(date_value, f"{item_path}.date_timestamp")
        except ValidationError as exc:
            errors.extend(exc.errors)
            continue
        name_key = "meeting_name" if kind == "meeting" else "calendar_event_name"
        name = item.get(name_key)
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{item_path}.{name_key}: must be a non-empty string")
            continue
        records.append(ActivityRecord(date=date, name=name.strip(), kind=kind))
    return tuple(records)


def validate_packet(data: Any, max_learners: Optional[int] = None, max_activity_records: Optional[int] = None) -> ProgressPacket:
    errors: List[str] = []
    if not isinstance(data, dict):
        raise ValidationError(("packet: must be a JSON object",))
    employer_id = _required(data, "employer_id", "packet", errors)
    if employer_id is not None and (not isinstance(employer_id, (str, int)) or isinstance(employer_id, bool) or (isinstance(employer_id, str) and not employer_id.strip())):
        errors.append("packet.employer_id: must be a non-empty string or integer")
    learners_value = _required(data, "learners", "packet", errors)
    learners = []
    if not isinstance(learners_value, list):
        errors.append("packet.learners: must be a list")
        learners_value = []
    if not learners_value:
        errors.append("packet.learners: must contain at least one learner")
    if max_learners is not None and isinstance(learners_value, list) and len(learners_value) > max_learners:
        errors.append(f"packet.learners: exceeds configured limit of {max_learners}")
    references = set()
    for index, raw in enumerate(learners_value):
        path = f"packet.learners[{index}]"
        if not isinstance(raw, dict):
            errors.append(f"{path}: must be an object")
            continue
        name = _required(raw, "name", path, errors)
        product = _required(raw, "product", path, errors)
        otj_hours = _required(raw, "otj_hours", path, errors)
        meetings_value = _required(raw, "meetings", path, errors)
        workshops_value = _required(raw, "workshops", path, errors)
        recency = _required(raw, "days_since_last_meeting", path, errors)
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{path}.name: must be a non-empty string")
        if not isinstance(product, str) or not product.strip():
            errors.append(f"{path}.product: must be a non-empty string")
        if otj_hours is not None and (not isinstance(otj_hours, (int, float)) or isinstance(otj_hours, bool) or not math.isfinite(otj_hours) or otj_hours < 0):
            errors.append(f"{path}.otj_hours: must be a non-negative number or null")
        if recency is not None and (not isinstance(recency, int) or isinstance(recency, bool) or recency < 0):
            errors.append(f"{path}.days_since_last_meeting: must be a non-negative integer or null")
        meetings = _activity(meetings_value, f"{path}.meetings", "meeting", errors)
        workshops = _activity(workshops_value, f"{path}.workshops", "workshop", errors)
        if max_activity_records is not None and len(meetings) + len(workshops) > max_activity_records:
            errors.append(f"{path}: exceeds configured activity limit of {max_activity_records}")
        learner_id = raw.get("learner_id")
        if learner_id is not None and (not isinstance(learner_id, str) or not learner_id.strip()):
            errors.append(f"{path}.learner_id: must be a non-empty string when provided")
        reference = learner_id.strip() if isinstance(learner_id, str) and learner_id.strip() else name.strip() if isinstance(name, str) else None
        if reference in references:
            errors.append(f"{path}: duplicate learner reference")
        if reference:
            references.add(reference)
        if isinstance(name, str) and isinstance(product, str) and (otj_hours is None or isinstance(otj_hours, (int, float))) and (recency is None or isinstance(recency, int)):
            learners.append(LearnerProgress(name.strip(), product.strip(), float(otj_hours) if otj_hours is not None else None, meetings, workshops, recency, learner_id=learner_id.strip() if isinstance(learner_id, str) and learner_id.strip() else None))
    if errors:
        raise ValidationError(errors)
    return ProgressPacket(employer_id=employer_id, learners=tuple(learners))
