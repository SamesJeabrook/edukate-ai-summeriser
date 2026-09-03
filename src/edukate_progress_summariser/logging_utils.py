from __future__ import annotations

import logging
from typing import Any

from .privacy import redact_sensitive


def get_logger(name: str = "edukate_progress_summariser") -> logging.Logger:
    return logging.getLogger(name)


def safe_log(logger: logging.Logger, level: int, message: str, details: Any = None) -> None:
    safe_details = redact_sensitive(details) if details is not None else None
    if safe_details is None:
        logger.log(level, message)
    else:
        logger.log(level, "%s: %s", message, safe_details)