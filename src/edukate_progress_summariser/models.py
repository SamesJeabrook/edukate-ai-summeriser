from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

Scalar = Union[str, int, float, bool, None]


@dataclass(frozen=True)
class ActivityRecord:
    date: datetime
    name: str
    kind: str


@dataclass(frozen=True)
class LearnerProgress:
    name: str
    product: str
    otj_hours: Optional[float]
    meetings: Tuple[ActivityRecord, ...]
    workshops: Tuple[ActivityRecord, ...]
    days_since_last_meeting: Optional[int]
    learner_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProgressPacket:
    employer_id: Union[str, int]
    learners: Tuple[LearnerProgress, ...]


@dataclass(frozen=True)
class InterventionRule:
    rule_id: str
    version: str
    category: str
    severity: str
    metric: str
    threshold: float
    operator: str
    recommended_follow_up: str


@dataclass(frozen=True)
class CohortFacts:
    learner_count: int
    total_otj_hours: float
    meeting_count: int
    workshop_count: int
    learners_without_activity: int
    recency_values: Tuple[Optional[int], ...]
    evidence_limitations: Tuple[str, ...] = ()


@dataclass(frozen=True)
class EscalationAlert:
    learner_reference: str
    severity: str
    category: str
    triggering_evidence: Tuple[str, ...]
    explanation: str
    recommended_follow_up: str
    evidence_complete: bool
    learner_name: Optional[str] = None


@dataclass(frozen=True)
class AlertPayload:
    cohort_context: Dict[str, Scalar]
    alerts: Tuple[EscalationAlert, ...]
    human_review_disclaimer: str
    facts: Optional[CohortFacts] = None
    interpretation: Optional[str] = None


@dataclass(frozen=True)
class GenerationMetadata:
    generated_at: str
    model: str
    input_packet_reference: str
    output_status: str
    rule_configuration_version: Optional[str] = None


class ResultStatus(str, Enum):
    VALIDATED = "validated"
    INTERPRETATION_UNAVAILABLE = "interpretation_unavailable"
    REJECTED = "rejected"


@dataclass(frozen=True)
class SummaryResult:
    status: ResultStatus
    facts: CohortFacts
    interpretation: Optional[str]
    evidence_status: str
    alerts: Tuple[EscalationAlert, ...]
    alert_payload: AlertPayload
    metadata: GenerationMetadata

    @property
    def interpretation_label(self) -> str:
        return "AI-generated interpretation"
