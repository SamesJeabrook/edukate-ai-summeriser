from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Iterable, Optional

from .ai_service import AIProvider
from .alerts import build_alert_payload, evaluate_alerts
from .config import AppConfig
from .errors import format_processing_error
from .metrics import calculate_facts
from .models import GenerationMetadata, InterventionRule, ProgressPacket, ResultStatus, SummaryResult
from .prompting import build_interpretation_prompt
from .rules import default_rules


DISCLAIMER = "Escalations support human review and do not represent an automatic employment or learner outcome decision."


class SummaryService:
    def __init__(self, provider: AIProvider, rules: Optional[Iterable[InterventionRule]] = None, config: Optional[AppConfig] = None):
        self.provider = provider
        self.rules = tuple(rules) if rules is not None else default_rules()
        self.config = config or AppConfig()

    def generate(self, packet: ProgressPacket) -> SummaryResult:
        facts = calculate_facts(packet)
        alerts = evaluate_alerts(packet, self.rules)
        evidence = build_interpretation_prompt(packet)
        packet_reference = hashlib.sha256(json.dumps(evidence, sort_keys=True).encode("utf-8")).hexdigest()[:16]
        generated_at = datetime.now(timezone.utc).isoformat()
        metadata_base = {
            "generated_at": generated_at,
            "model": self.provider.model,
            "input_packet_reference": packet_reference,
        }

        try:
            interpretation = self.provider.interpret(evidence).strip()
            if not interpretation:
                raise RuntimeError("empty interpretation")
            status = ResultStatus.VALIDATED
            evidence_status = "Evidence reviewed; deterministic facts are separated from AI-generated interpretation."
            output_status = "validated"
        except Exception:
            interpretation = None
            status = ResultStatus.INTERPRETATION_UNAVAILABLE
            evidence_status = format_processing_error("AI interpretation unavailable; validated factual measures are retained")
            output_status = "interpretation_unavailable"

        metadata = GenerationMetadata(**metadata_base, output_status=output_status)
        payload = build_alert_payload(
            packet.employer_id,
            facts,
            alerts,
            DISCLAIMER,
        )
        payload = payload.__class__(
            cohort_context=payload.cohort_context,
            alerts=payload.alerts,
            human_review_disclaimer=payload.human_review_disclaimer,
            facts=payload.facts,
            interpretation=interpretation,
        )
        return SummaryResult(status, facts, interpretation, evidence_status, alerts, payload, metadata)


def render_text(result: SummaryResult) -> str:
    lines = [
        "Cohort Progress Summary",
        "",
        "Factual metrics",
        f"Learners: {result.facts.learner_count}",
        f"Recorded hours: {result.facts.total_otj_hours:g}",
        f"Meetings: {result.facts.meeting_count}",
        f"Workshops: {result.facts.workshop_count}",
        f"Escalation alerts: {len(result.alerts)}",
        f"Evidence status: {result.evidence_status}",
        "",
        "AI-generated interpretation",
        result.interpretation or "Unavailable",
    ]
    if result.facts.evidence_limitations:
        lines.extend(["", "Evidence limitations", *result.facts.evidence_limitations])
    if result.alerts:
        lines.extend(["", "Escalation alerts"])
        for alert in result.alerts:
            lines.append(f"- {alert.severity.upper()}: {alert.learner_reference} - {alert.explanation}")
    return "\n".join(lines)