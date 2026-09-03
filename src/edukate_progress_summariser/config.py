from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Optional


@dataclass(frozen=True)
class AppConfig:
    model: str = "gpt-4o-mini"
    max_learners: int = 500
    max_activity_records: int = 5000
    employer_rule_config: Optional[str] = None
    cohort_rule_config: Optional[str] = None

    @classmethod
    def from_env(cls, environ: Optional[Mapping[str, str]] = None) -> "AppConfig":
        values = environ or os.environ
        return cls(
            model=values.get("EDUKATE_MODEL", cls.model),
            max_learners=_positive_int(values.get("EDUKATE_MAX_LEARNERS"), cls.max_learners),
            max_activity_records=_positive_int(values.get("EDUKATE_MAX_ACTIVITY_RECORDS"), cls.max_activity_records),
            employer_rule_config=values.get("EDUKATE_EMPLOYER_RULES"),
            cohort_rule_config=values.get("EDUKATE_COHORT_RULES"),
        )


def _positive_int(value: Optional[str], default: int) -> int:
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return parsed if parsed > 0 else default
