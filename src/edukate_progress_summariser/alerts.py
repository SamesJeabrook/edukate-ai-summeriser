from __future__ import annotations

from typing import Iterable, Tuple

from .models import AlertPayload, EscalationAlert, InterventionRule, ProgressPacket


def _matches(value: float, rule: InterventionRule) -> bool:
    if rule.operator == ">=":
        return value >= rule.threshold
    if rule.operator == ">":
        return value > rule.threshold
    if rule.operator == "<=":
        return value <= rule.threshold
    if rule.operator == "<":
        return value < rule.threshold
    if rule.operator == "==":
        return value == rule.threshold
    raise ValueError(f"unsupported intervention operator: {rule.operator}")


def evaluate_alerts(packet: ProgressPacket, rules: Iterable[InterventionRule]) -> Tuple[EscalationAlert, ...]:
    alerts = []
    for learner in packet.learners:
        for rule in rules:
            value = getattr(learner, rule.metric, None)
            if value is None:
                continue
            if _matches(value, rule):
                evidence = (f"{rule.metric}={value:g}", f"threshold={rule.operator}{rule.threshold:g}")
                alerts.append(EscalationAlert(
                    learner_reference=learner.name,
                    learner_name=learner.name,
                    severity=rule.severity,
                    category=rule.category,
                    triggering_evidence=evidence,
                    explanation=f"{rule.metric} meets intervention threshold.",
                    recommended_follow_up=rule.recommended_follow_up,
                    evidence_complete=True,
                ))
    return tuple(alerts)


def build_alert_payload(
    employer_id,
    facts,
    alerts: Iterable[EscalationAlert],
    disclaimer: str,
) -> AlertPayload:
    return AlertPayload(
        cohort_context={"employer_id": employer_id},
        alerts=tuple(alerts),
        human_review_disclaimer=disclaimer,
        facts=facts,
    )