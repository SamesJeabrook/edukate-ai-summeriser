# CLI Contract

## Invocation

```text
python -m edukate_progress_summariser INPUT.json [--output OUTPUT.json] [--rules RULES.json] [--format canonical|text]
```

The CLI reads one JSON packet. It writes the canonical structured result to standard output by default, or to `--output` when supplied. A human-readable employer summary is included in the result and may be selected with `--format text`. No command sends messages to an external channel.

## Exit behavior

- `0`: valid packet processed; interpretation may be unavailable but the result is explicit about that status.
- non-zero: malformed or invalid packet, configuration error, or unrecoverable processing failure. Standard error contains a field-specific, non-sensitive message; no partial result is written.

## Input

The input must satisfy the original Progress Packet model in [data-model.md](../data-model.md). Learner names, direct identifiers, and other free text remain local and are excluded from the AI evidence request. Risk information is generated deterministically from the progress evidence rather than supplied as an input flag.

## Output behavior

A successful result contains:

- `status`
- `summary` with factual metrics, labelled interpretation, and evidence limitations
- `alerts` with structured escalation data
- `alert_payload` with canonical channel-neutral content
- `metadata` without learner-identifying content or credentials

The canonical payload is intended for future formatter adapters. Slack/email formatting and delivery are not performed by this CLI contract. Use `--provider fake` for offline tests or `--provider openai` for an actual AI request using `OPENAI_API_KEY`.
