# Quickstart Validation Guide

This guide validates the planned local CLI without sending real learner data or requiring a network call. The implementation must be run with Python 3.12+.

## Prerequisites

```text
python3.12 --version
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

The real OpenAI provider requires credentials supplied through trusted runtime configuration. The default validation path uses a fake provider and does not require credentials.

## Run the test suite

```text
python -m unittest discover -s tests -v
```

Expected result: all tests pass without network access.

## Validate a successful packet

```text
python -m edukate_progress_summariser data/valid-input.json --provider fake --format canonical
```

Verify that the result contains validated factual cohort metrics for `sessions_attended`, `assessments_submitted`, and off-the-job hours, supplied `at_risk_flags`, a clearly labelled interpretation, evidence status, structured alerts, a channel-neutral `alert_payload`, and non-sensitive generation metadata.

## Validate invalid packets

Run the CLI against each `data/invalid-*.json` fixture. Verify that every invalid packet returns a non-zero exit status, a field-specific non-sensitive error, no model request, and no partial summary or alert payload. `invalid-malformed-json.json` must fail JSON parsing; the other fixtures must reach schema, data-quality, or safety validation.

## Validate privacy and prompt-injection boundaries

Use a fake provider that records its request. Run `invalid-prompt-injection-content.json` and `invalid-credential-like-data.json` through the relevant validation/security tests. Verify that learner names, direct identifiers, credential-like values, and instruction-like free text are absent from the model request and application logs, and that untrusted text cannot alter required output labels or processing rules.

## Validate model failure behavior

Configure the fake provider to fail or return unusable content for a valid packet. Verify that deterministic factual metrics remain available, the result status says interpretation is unavailable, no fabricated interpretation or escalation alert is created, and the failure message contains no credentials or learner-sensitive content.

## Validate output extensibility

Validate the canonical result against [contracts/output-schema.json](contracts/output-schema.json). Exercise formatter tests with the same `alert_payload` to produce a baseline plain-text rendering and future formatter stubs. Confirm that formatters consume canonical evidence without changing alert severity, evidence, or human-review disclaimers. Delivery transmission is not part of this validation.

## Validate the real AI provider

After placing `OPENAI_API_KEY` in the local `.env` file, run:

```text
python -m edukate_progress_summariser data/valid-input.json --provider openai --format text
```

Verify that the output includes an AI-generated interpretation and that no API key, learner name, direct identifier, flag description, or other sensitive input appears in the output or logs. Use the fake provider for repeatable tests and avoid sending real learner data during development.

See [data-model.md](data-model.md) for entity and state rules and [contracts/cli.md](contracts/cli.md) for invocation and exit behavior.
