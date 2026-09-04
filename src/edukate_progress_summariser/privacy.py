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
    learners = packet.get("learners", [])
    return {
        "cohort": {
            "learner_count": len(learners),
            "sessions_attended": sum(
                learner.get("sessions_attended") if learner.get("sessions_attended") is not None else len(learner.get("meetings", [])) + len(learner.get("workshops", []))
                for learner in learners if isinstance(learner, Mapping)
            ),
            "assessments_submitted": None if any(learner.get("assessments_submitted") is None for learner in learners if isinstance(learner, Mapping)) else sum(learner.get("assessments_submitted", 0) for learner in learners if isinstance(learner, Mapping)),
            "total_otj_hours": sum(learner.get("otj_hours") or 0 for learner in learners if isinstance(learner, Mapping)),
            "meeting_count": sum(len(learner.get("meetings", [])) for learner in learners if isinstance(learner, Mapping)),
            "workshop_count": sum(len(learner.get("workshops", [])) for learner in learners if isinstance(learner, Mapping)),
            "learners_without_activity": sum(not learner.get("meetings") and not learner.get("workshops") for learner in learners if isinstance(learner, Mapping)),
            "risk_alert_count": 0,
            "risk_alerts_by_category": {},
            "risk_alerts_by_severity": {},
            "evidence_limitations": [],
        }
    }
