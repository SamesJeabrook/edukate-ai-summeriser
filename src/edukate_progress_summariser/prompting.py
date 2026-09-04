from __future__ import annotations

from typing import Any, Dict

from .metrics import calculate_facts
from .models import EscalationAlert, ProgressPacket
from .privacy import derive_learner_reference


def build_evidence(packet: ProgressPacket, alerts: tuple[EscalationAlert, ...] = ()) -> Dict[str, Any]:
    facts = calculate_facts(packet)
    return {
        "cohort": {
            "learner_count": facts.learner_count,
            "sessions_attended": facts.sessions_attended,
            "assessments_submitted": facts.assessments_submitted,
            "total_otj_hours": facts.total_otj_hours,
            "meeting_count": facts.meeting_count,
            "workshop_count": facts.workshop_count,
            "learners_without_activity": facts.learners_without_activity,
            "risk_alert_count": len(alerts),
            "risk_alerts_by_category": _count_alerts(alerts, "category"),
            "risk_alerts_by_severity": _count_alerts(alerts, "severity"),
            "evidence_limitations": list(facts.evidence_limitations),
        }
    }


def validate_evidence_boundary(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Allow only the fixed, de-identified fields sent to the provider."""
    allowed = {"cohort"}
    if set(evidence) - allowed:
        raise ValueError("unsupported AI evidence field")
    required = {"learner_count", "sessions_attended", "assessments_submitted", "total_otj_hours", "meeting_count", "workshop_count", "learners_without_activity", "risk_alert_count", "risk_alerts_by_category", "risk_alerts_by_severity", "evidence_limitations"}
    if set(evidence["cohort"]) != required:
        raise ValueError("unsupported AI cohort evidence field")
    return evidence


def _count_alerts(alerts: tuple[EscalationAlert, ...], attribute: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for alert in alerts:
        key = getattr(alert, attribute)
        counts[key] = counts.get(key, 0) + 1
    return counts


def build_interpretation_prompt(packet: ProgressPacket, alerts: tuple[EscalationAlert, ...] = ()) -> Dict[str, Any]:
    return validate_evidence_boundary(build_evidence(packet, alerts))