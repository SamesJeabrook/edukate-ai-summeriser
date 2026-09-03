from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Optional

from .ai_service import AIProvider
from .metrics import calculate_facts
from .models import AlertPayload, GenerationMetadata, ProgressPacket, ResultStatus, SummaryResult
from .prompting import build_interpretation_prompt


DISCLAIMER = "Escalations support human review and do not represent an automatic employment or learner outcome decision."


class SummaryService:
    def __init__(self, provider: AIProvider):
        self.provider = provider

    def generate(self, packet: ProgressPacket) -> SummaryResult:
        facts = calculate_facts(packet)
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
            status = ResultStatus.VALIDATED
            evidence_status = "Evidence reviewed; deterministic facts are separated from AI-generated interpretation."
            output_status = "validated"
        except Exception:
            interpretation = None
            status = ResultStatus.INTERPRETATION_UNAVAILABLE
            evidence_status = "AI interpretation unavailable; validated factual measures are retained."
            output_status = "interpretation_unavailable"

        metadata = GenerationMetadata(**metadata_base, output_status=output_status)
        payload = AlertPayload(
            cohort_context={"employer_id": packet.employer_id},
            alerts=(),
            human_review_disclaimer=DISCLAIMER,
            facts=facts,
            interpretation=interpretation,
        )
        return SummaryResult(status, facts, interpretation, evidence_status, (), payload, metadata)


def render_text(result: SummaryResult) -> str:
    lines = [
        "Cohort Progress Summary",
        "",
        "Factual metrics",
        f"Learners: {result.facts.learner_count}",
        f"Recorded hours: {result.facts.total_otj_hours:g}",
        f"Meetings: {result.facts.meeting_count}",
        f"Workshops: {result.facts.workshop_count}",
        f"Evidence status: {result.evidence_status}",
        "",
        "AI-generated interpretation",
        result.interpretation or "Unavailable",
    ]
    if result.facts.evidence_limitations:
        lines.extend(["", "Evidence limitations", *result.facts.evidence_limitations])
    return "\n".join(lines)