from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any

from .ai_service import FakeAIProvider
from .summariser import SummaryService, render_text
from .validation import ValidationError, load_json_file, validate_packet


def _serialise(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _serialise(item) for key, item in dataclasses.asdict(value).items()}
    if isinstance(value, tuple):
        return [_serialise(item) for item in value]
    if hasattr(value, "value"):
        return value.value
    return value


def _serialise_result(result: Any) -> dict[str, Any]:
    return {
        "status": result.status.value,
        "summary": {
            "facts": _serialise(result.facts),
            "interpretation": result.interpretation,
            "interpretation_label": result.interpretation_label,
            "evidence_status": result.evidence_status,
        },
        "alerts": _serialise(result.alerts),
        "alert_payload": _serialise(result.alert_payload),
        "metadata": _serialise(result.metadata),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an evidence-based cohort progress summary.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--provider", choices=("fake",), default="fake")
    parser.add_argument("--format", choices=("canonical", "text"), default="canonical")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        packet = validate_packet(load_json_file(args.input))
        result = SummaryService(FakeAIProvider()).generate(packet)
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"processing error: {exc}", file=sys.stderr)
        return 1

    if args.format == "text":
        output = render_text(result)
    else:
        output = json.dumps(_serialise_result(result), indent=2)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0