from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
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
        values = environ or _load_environment()
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


def _load_environment() -> Mapping[str, str]:
    values = dict(os.environ)
    env_path = Path.cwd() / ".env"
    if not env_path.is_file():
        return values
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and key not in values:
            values[key] = value
    return values


def openai_api_key() -> Optional[str]:
    return _load_environment().get("OPENAI_API_KEY")
