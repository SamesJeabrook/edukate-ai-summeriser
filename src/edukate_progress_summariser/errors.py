from __future__ import annotations

from typing import Iterable

from .validation import ValidationError


def format_validation_error(error: ValidationError) -> str:
    """Return field-aware categories without echoing packet values."""
    return "Input validation failed: " + "; ".join(error.errors)


def format_processing_error(category: str) -> str:
    return f"Processing failed: {category}."