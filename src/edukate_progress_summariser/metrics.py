from __future__ import annotations

from .models import CohortFacts, ProgressPacket


def calculate_facts(packet: ProgressPacket) -> CohortFacts:
    limitations = []
    missing_hours = sum(learner.otj_hours is None for learner in packet.learners)
    missing_recency = sum(learner.days_since_last_meeting is None for learner in packet.learners)
    if missing_hours:
        limitations.append(f"Recorded hours are missing for {missing_hours} learner(s).")
    if missing_recency:
        limitations.append(f"Last-meeting recency is unavailable for {missing_recency} learner(s).")

    return CohortFacts(
        learner_count=len(packet.learners),
        total_otj_hours=sum(learner.otj_hours or 0 for learner in packet.learners),
        meeting_count=sum(len(learner.meetings) for learner in packet.learners),
        workshop_count=sum(len(learner.workshops) for learner in packet.learners),
        learners_without_activity=sum(not learner.meetings and not learner.workshops for learner in packet.learners),
        recency_values=tuple(learner.days_since_last_meeting for learner in packet.learners),
        evidence_limitations=tuple(limitations),
    )