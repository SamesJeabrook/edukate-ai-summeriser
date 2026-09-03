# Implementation Plan: Cohort Progress Summary and Escalation Alerts

**Branch**: `main` | **Date**: 2026-09-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-cohort-progress-summary/spec.md`

**Input**: Feature specification from `/specs/001-cohort-progress-summary/spec.md`

## Summary

Build a self-contained Python module and CLI that accepts one employer cohort JSON packet, validates and normalises it, computes deterministic progress and intervention metrics, sends only minimum de-identified evidence to an isolated language-model service, and returns two outputs: a human-readable employer progress summary and a structured, extensible escalation payload. Channel presentation and delivery are separate concerns.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: Python standard library for parsing, validation, deterministic metrics, and baseline formatting; official OpenAI SDK isolated behind a provider boundary. No web framework or delivery SDK.

**Storage**: N/A; packet input and result output are local process data.

**Testing**: Python `unittest` with fixture-driven unit, contract, privacy, and integration tests; model calls replaced with a fake provider.

**Target Platform**: Local Python 3.12+ runtime on macOS/Linux-compatible environments.

**Project Type**: Self-contained Python library with a command-line interface.

**Performance Goals**: Produce a result for a supported packet in under 2 minutes; deterministic validation and metrics complete before the model request.

**Constraints**: No learner names or direct identifiers in model input or logs; no credentials in output; invalid packets produce no summary or escalation payload; model failure must not discard validated facts; output is channel-neutral and extensible.

**Scale/Scope**: One employer/cohort packet per CLI invocation, within an explicitly configured learner/activity limit; no persistence, multi-user access control, scheduling, or delivery transmission.

## Constitution Check

_GATE: Must pass before Phase 0 research and after Phase 1 design._

| Gate                                  | Status                 | Evidence / plan action                                                                                                                                         |
| ------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python simplicity and clarity         | PASS                   | Use a small standard-library module/CLI and avoid infrastructure.                                                                                              |
| Evidence-led human decision support   | PASS                   | Compute factual metrics deterministically; label model interpretation and evidence sufficiency; record model configuration metadata.                           |
| Privacy and data minimisation         | PASS                   | Keep names local to authorised output; derive non-identifying learner references; redact sensitive values from model input and logs.                           |
| Secure and trustworthy AI integration | PASS                   | Isolate the official OpenAI SDK behind an injectable service boundary; keep credentials in trusted runtime configuration; treat free text as untrusted.        |
| Traceability and quality gates        | PASS                   | Record non-sensitive model, timestamp, packet-reference, and output-status metadata; add focused tests for privacy, labelling, failures, and prompt injection. |
| Local clean-checkout operation        | PASS with prerequisite | Document Python 3.12+ setup and offline fake-provider test path; current shell reports Python 3.9.21 and must be upgraded for execution.                       |

## Project Structure

### Documentation (this feature)

```text
specs/001-cohort-progress-summary/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── cli.md
│   └── output-schema.json
└── tasks.md                 # Created by /speckit-tasks
```

### Source Code (repository root)

```text
src/
└── edukate_progress_summariser/
  ├── __init__.py
  ├── __main__.py
  ├── cli.py
  ├── models.py
  ├── validation.py
  ├── metrics.py
  ├── alerts.py
  ├── summariser.py
  ├── prompting.py
  └── ai_service.py

tests/
├── unit/
├── contract/
├── integration/
└── fixtures/                # References or copies of data/ fixtures
```

**Structure Decision**: Use one small package under `src/` with explicit modules for the data model, validation, deterministic analysis, alert payload construction, AI boundary, and CLI orchestration. Keep tests split by behavior and preserve the existing `data/` fixtures as input examples. Do not add persistence, a web layer, or channel delivery adapters in this feature.

## Complexity Tracking

No constitution violations. The AI provider boundary is required by the constitution and supports model/provider replacement; it does not introduce a second application or infrastructure layer.
src/
├── edukate_progress_summariser/
├── **init**.py
├── **main**.py
├── cli.py
├── models.py
├── validation.py
├── metrics.py
├── alerts.py
├── summariser.py
├── prompting.py
└── ai_service.py

tests/
├── unit/
├── contract/
├── integration/
└── fixtures/ -> repository data fixtures
**Structure Decision**: Use one small package under `src/` with explicit modules for the data model, validation, deterministic analysis, alert payload construction, AI boundary, and CLI orchestration. Keep tests split by behavior and preserve the existing `data/` fixtures as input examples. Do not add persistence, a web layer, or channel delivery adapters in this feature.
