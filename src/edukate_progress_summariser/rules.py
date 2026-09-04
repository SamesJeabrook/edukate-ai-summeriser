from __future__ import annotations

from typing import Iterable, Tuple

from .models import InterventionRule


def default_rules() -> Tuple[InterventionRule, ...]:
    return (
        InterventionRule(
            rule_id="stale-contact",
            version="product-v1",
            category="contact_recency",
            severity="high",
            metric="days_since_last_meeting",
            threshold=30,
            operator=">=",
            recommended_follow_up="Review learner contact history and arrange a progress check-in.",
        ),
        InterventionRule("low-sessions", "product-v1", "session_attendance", "medium", "sessions_attended", 1, "<", "Review attendance and arrange learner support."),
        InterventionRule("low-assessments", "product-v1", "assessment_submissions", "medium", "assessments_submitted", 1, "<", "Review assessment progress and arrange learner support."),
    )


def select_rules(
    defaults: Iterable[InterventionRule],
    employer_overrides: Iterable[InterventionRule] = (),
    cohort_overrides: Iterable[InterventionRule] = (),
) -> Tuple[InterventionRule, ...]:
    selected = {rule.rule_id: rule for rule in defaults}
    selected.update({rule.rule_id: rule for rule in employer_overrides})
    selected.update({rule.rule_id: rule for rule in cohort_overrides})
    return tuple(selected.values())