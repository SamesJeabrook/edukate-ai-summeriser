from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


SENSITIVE_KEYS = frozenset({"name", "learner_name", "learner_id", "api_key", "password", "token", "secret", "credentials", "notes", "free_text"})


def derive_learner_reference(employer_id: Any, learner_name: str, position: int) -> str:
    payload = json.dumps([str(employer_id), learner_name, position], ensure_ascii=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"learner-{digest}"


def redact_sensitive(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: "[REDACTED]" if key.lower() in SENSITIVE_KEYS else redact_sensitive(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_sensitive(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_sensitive(item) for item in value)
    return value


def build_ai_evidence(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    learners = []
    employer_id = packet.get("employer_id")
    for position, learner in enumerate(packet.get("learners", [])):
        if not isinstance(learner, Mapping):
            continue
        reference = derive_learner_reference(employer_id, str(learner.get("name", "")), position)
        learners.append({
            "learner_reference": reference,
            "product": learner.get("product"),
            "otj_hours": learner.get("otj_hours"),
            "meeting_count": len(learner.get("meetings", [])) if isinstance(learner.get("meetings"), list) else None,
            "workshop_count": len(learner.get("workshops", [])) if isinstance(learner.get("workshops"), list) else None,
            "days_since_last_meeting": learner.get("days_since_last_meeting"),
        })
    return {"employer_id": employer_id, "learners": learners}
