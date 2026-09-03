from __future__ import annotations

from typing import Any, Dict

from .models import ProgressPacket
from .privacy import derive_learner_reference


def build_evidence(packet: ProgressPacket) -> Dict[str, Any]:
    learners = []
    for position, learner in enumerate(packet.learners):
        learners.append({
            "learner_reference": derive_learner_reference(packet.employer_id, learner.name, position),
            "product": learner.product,
            "otj_hours": learner.otj_hours,
            "meeting_count": len(learner.meetings),
            "workshop_count": len(learner.workshops),
            "days_since_last_meeting": learner.days_since_last_meeting,
            "sessions_attended": learner.sessions_attended,
            "assessments_submitted": learner.assessments_submitted,
            "at_risk_flags": [{"code": flag.code, "severity": flag.severity} for flag in learner.at_risk_flags],
        })
    return {"employer_id": packet.employer_id, "learners": learners}


def validate_evidence_boundary(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Allow only the fixed, de-identified fields sent to the provider."""
    allowed = {"employer_id", "learners"}
    if set(evidence) - allowed:
        raise ValueError("unsupported AI evidence field")
    for learner in evidence.get("learners", []):
        required = {"learner_reference", "product", "otj_hours", "meeting_count", "workshop_count", "days_since_last_meeting", "sessions_attended", "assessments_submitted", "at_risk_flags"}
        if set(learner) != required:
            raise ValueError("unsupported AI learner evidence field")
    return evidence


def build_interpretation_prompt(packet: ProgressPacket) -> Dict[str, Any]:
    return validate_evidence_boundary(build_evidence(packet))