# Edukate Progress Summariser

A local Python module and CLI for producing evidence-based employer cohort summaries and structured escalation payloads from JSON progress packets.

## Requirements

- Python 3.12 or newer
- An OpenAI API key only when using the real provider

The repository does not commit `.venv/`, credentials, generated output, or build artifacts.

## Setup

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Run

Use the fake provider for local development and tests. It requires no credentials or network access.

```sh
python -m edukate_progress_summariser data/valid-input.json --provider fake --format canonical
python -m edukate_progress_summariser data/valid-input.json --provider fake --format text

# Use the actual OpenAI provider. The CLI loads OPENAI_API_KEY from .env.
python -m edukate_progress_summariser data/valid-input.json --provider openai --format text
```

A successful result contains deterministic factual metrics, a clearly labelled AI-generated interpretation, structured escalation alerts, a canonical channel-neutral `alert_payload`, and non-sensitive generation metadata.

The CLI processes one packet per invocation. It does not send messages or configure recipients. Future Slack, email, or other channel formatters can consume the canonical payload without changing its evidence.

## Validation and safety

Run the full test suite with:

```sh
python -m unittest discover -s tests -v
```

The fixtures in `data/invalid-*.json` cover malformed JSON, missing fields, empty cohorts, invalid types, invalid dates, duplicate references, insufficient evidence, prompt-injection text, and credential-like values. Hard-invalid packets return a non-zero exit and no partial result. Parseable packets with insufficient or untrusted evidence are processed with explicit evidence limitations and privacy-safe model input.

Learner names and direct identifiers remain in authorised account-manager-facing output only. Model evidence uses derived non-identifying references and a fixed minimum field set. Packet free text is treated as untrusted and is not included in model evidence. Logs and generation metadata must not contain learner names, credentials, raw free text, or the original packet.

## Configuration

The model name and packet limits can be set through trusted environment configuration:

```sh
export EDUKATE_MODEL=gpt-4o-mini
export EDUKATE_MAX_LEARNERS=500
export EDUKATE_MAX_ACTIVITY_RECORDS=5000
```

The official OpenAI SDK adapter is isolated behind the `AIProvider` boundary. Tests inject `FakeAIProvider`, so normal validation does not require `OPENAI_API_KEY`. For a real request, put the key in the local `.env` file or export it in the shell, then pass `--provider openai`. Credentials must be supplied through the trusted runtime environment and must never be committed or printed.

## Design references

- [Feature specification](specs/001-cohort-progress-summary/spec.md)
- [Implementation plan](specs/001-cohort-progress-summary/plan.md)
- [Data model](specs/001-cohort-progress-summary/data-model.md)
- [CLI contract](specs/001-cohort-progress-summary/contracts/cli.md)
- [Output schema](specs/001-cohort-progress-summary/contracts/output-schema.json)
- [Quickstart validation guide](specs/001-cohort-progress-summary/quickstart.md)
