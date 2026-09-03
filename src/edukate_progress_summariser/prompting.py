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
        })
    return {"employer_id": packet.employer_id, "learners": learners}


def build_interpretation_prompt(packet: ProgressPacket) -> Dict[str, Any]:
    return build_evidence(packet)