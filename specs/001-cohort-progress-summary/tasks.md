# Tasks: Cohort Progress Summary and Escalation Alerts

**Input**: Design documents from `/specs/001-cohort-progress-summary/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md), [contracts/](contracts/)

**Organization**: Tasks are grouped by user story. Existing baseline behavior must remain working while the corrected progress fields, generated risk evidence, and real provider path are maintained.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the package and test environment for the corrected brief.

- [x] T001 Verify Python 3.12+ package entry points and test directories in `src/edukate_progress_summariser/__init__.py`, `src/edukate_progress_summariser/__main__.py`, and `tests/`
- [x] T002 [P] Update packaging metadata and provider dependencies for local editable installation in `pyproject.toml`
- [x] T003 [P] Verify `.env`, `.env.example`, Python caches, build output, and virtual environments are excluded appropriately in `.gitignore`
- [x] T004 [P] Keep `data/valid-input.json` as the authoritative source-of-truth fixture and retain the related invalid packet fixtures in `data/`

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T006 [P] Define aggregate generated-risk evidence by category and severity for the AI boundary in `src/edukate_progress_summariser/prompting.py`
- [x] T007 [P] Load OpenAI configuration and provider settings from trusted environment configuration in `src/edukate_progress_summariser/config.py`
- [x] T008 [P] Enforce aggregate, cohort-only evidence construction that excludes learner-level details, names, credentials, and free text while including generated risk counts in `src/edukate_progress_summariser/privacy.py` and `src/edukate_progress_summariser/prompting.py`
- [x] T009 [P] Wire real OpenAI provider selection while retaining fake-provider injection for offline tests in `src/edukate_progress_summariser/ai_service.py` and `src/edukate_progress_summariser/cli.py`

**Purpose**: Establish shared models, configuration, privacy boundaries, and provider selection before story work.

- [x] T005 Extend learner models with optional `sessions_attended` and optional `assessments_submitted`; keep risk evidence derived rather than input-provided in `src/edukate_progress_summariser/models.py`
- [x] T010 Add shared fixture helpers and test constants for sessions, assessments, and at-risk flags in `tests/helpers.py`
- [x] T011 Add foundation tests for new fields, flag validation, environment precedence, provider selection, and privacy-safe evidence in `tests/unit/test_foundation.py` and `tests/unit/test_ai_service.py`

## Phase 3: User Story 1 - Generate an evidence-based cohort summary (Priority: P1) MVP

**Goal**: Produce an employer-facing summary containing factual sessions, assessments, hours, and generated aggregate risk evidence alongside labelled AI interpretation.

**Independent Test**: Run `data/valid-input.json` with a fake provider and verify available session evidence, unavailable assessment evidence, generated risk counts, evidence limitations, and AI labeling.

- [x] T012 [P] [US1] Extend metric tests for sessions, assessments, hours, and missing-versus-zero values in `tests/unit/test_metrics.py`
- [x] T013 [P] [US1] Add summary workflow tests proving generated risk evidence is aggregate, AI interpretation is labelled, and learner details are excluded from model evidence in `tests/integration/test_summary_workflow.py`
- [x] T014 [P] [US1] Extend CLI contract tests for canonical and human-readable output containing sessions, assessments, hours, and generated risk evidence in `tests/contract/test_cli_summary.py`
- [x] T015 [US1] Add deterministic aggregation of sessions, assessments, and generated alert counts by category and severity, preserving unavailable values in `src/edukate_progress_summariser/metrics.py` and `src/edukate_progress_summariser/prompting.py`
- [x] T016 [US1] Extend the canonical AI evidence allowlist with session, assessment, hour, activity, recency, and aggregate generated-risk fields in `src/edukate_progress_summariser/prompting.py`
- [x] T017 [US1] Extend the employer summary with factual sections, generated risk evidence, evidence limitations, and labelled AI interpretation in `src/edukate_progress_summariser/summariser.py`
- [x] T018 [US1] Make the CLI default and documented primary execution path use the configured real provider while retaining explicit fake-provider mode in `src/edukate_progress_summariser/cli.py` and `README.md`
- [x] T019 [US1] Extend canonical result serialization with the new factual metrics and source flag details in `src/edukate_progress_summariser/cli.py`

## Phase 4: User Story 2 - Identify and communicate intervention needs (Priority: P1)

**Goal**: Escalate stale contact and configured session/assessment conditions through the channel-neutral payload, with aggregate generated risk evidence for AI interpretation.

**Independent Test**: Run known flags and metric conditions and verify deterministic alerts preserve source evidence and remain formatter-compatible.

- [x] T020 [P] [US2] Add rule tests for generated risk conditions and session/assessment thresholds with product defaults and employer/cohort overrides in `tests/unit/test_alert_rules.py`
- [x] T021 [P] [US2] Extend payload contract tests for source flag evidence, categories, severity, learner reference, and disclaimer in `tests/contract/test_alert_payload.py`
- [x] T022 [P] [US2] Add integration tests for multiple alert categories and channel-neutral payload reuse in `tests/integration/test_alert_workflow.py`
- [x] T023 [US2] Add versioned default rules for stale contact, matching at-risk flags, low sessions, and missing or low assessment submissions in `src/edukate_progress_summariser/rules.py`
- [x] T024 [US2] Implement deterministic evaluation for sessions and assessments with insufficient-evidence outcomes in `src/edukate_progress_summariser/alerts.py`
- [x] T025 [US2] Preserve source flag code and severity in alert evidence and distinguish source evidence from AI explanation in `src/edukate_progress_summariser/alerts.py`
- [x] T026 [US2] Integrate expanded alerts into summary generation and the canonical channel-neutral payload without delivery transmission in `src/edukate_progress_summariser/summariser.py`
- [x] T027 [US2] Extend text and canonical CLI output to expose all structured alerts without channel-specific credentials or transmission in `src/edukate_progress_summariser/cli.py`

## Phase 5: User Story 3 - Validate and protect the progress packet (Priority: P1)

**Goal**: Validate the corrected fields and protect source flag details, credentials, and real-provider execution.

**Independent Test**: Run all invalid fixtures and provider paths and verify safe rejection, no sensitive model input, and no secret leakage.

- [x] T028 [P] [US3] Add invalid fixtures for negative/non-integer sessions or assessments, invalid flag shapes, empty code/severity, duplicate flag codes, and malformed new fields in `data/invalid-*.json`
- [x] T029 [P] [US3] Extend validation contract tests for every new invalid fixture and field-specific safe errors in `tests/contract/test_invalid_packets.py`
- [x] T030 [P] [US3] Extend privacy tests for flag descriptions, direct identifiers, credentials, and real-provider evidence requests in `tests/unit/test_privacy_boundary.py`
- [x] T031 [P] [US3] Extend prompt-injection tests for flag descriptions and learner free text in `tests/unit/test_prompt_injection.py`
- [x] T032 [P] [US3] Extend CLI error tests for missing OpenAI key, invalid new fields, no partial output, safe stderr, and fake-provider fallback in `tests/contract/test_cli_errors.py`
- [x] T033 [US3] Validate optional sessions, optional assessments, flag objects, code/severity values, duplicate flag codes, and missing-versus-zero semantics in `src/edukate_progress_summariser/validation.py`
- [x] T034 [US3] Ensure validation errors identify field paths/categories without echoing invalid values, names, descriptions, credentials, or secrets in `src/edukate_progress_summariser/errors.py`
- [x] T035 [US3] Enforce packet validation and size limits before provider requests or result construction in `src/edukate_progress_summariser/summariser.py`
- [x] T036 [US3] Enforce the fixed AI evidence allowlist and immutable labels/disclaimers for flags and free text in `src/edukate_progress_summariser/prompting.py` and `src/edukate_progress_summariser/summariser.py`
- [x] T037 [US3] Ensure OpenAI credentials are read only from trusted configuration and absent from logs, metadata, summaries, and payloads in `src/edukate_progress_summariser/ai_service.py` and `src/edukate_progress_summariser/logging_utils.py`
- [x] T038 [US3] Return safe non-zero CLI exit codes for provider and validation failures without partial output in `src/edukate_progress_summariser/cli.py`

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T039 [P] Add end-to-end tests for corrected fields, generated risk evidence, provider selection, payloads, fallback, and traceability in `tests/integration/test_end_to_end.py`
- [x] T040 [P] Extend formatter compatibility tests for sessions, assessments, and at-risk evidence in `tests/contract/test_formatter_compatibility.py`
- [x] T041 [P] Update package usage, `.env` setup, real OpenAI execution, fake-provider testing, input shape, and output examples in `README.md`
- [x] T042 Update the quickstart with corrected fields, invalid fixture expectations, and real-provider validation in `specs/001-cohort-progress-summary/quickstart.md`
- [x] T043 Run the complete quickstart under Python 3.12+ and record successful validation results in `README.md`
- [x] T044 Run the complete test suite and clean editable installation using `python3.12 -m unittest discover -s tests -v` and `python3.12 -m pip install -e .`

## Dependencies & Execution Order

- Setup T001-T004 precedes Foundation T005-T011.
- Foundation precedes US1 T012-T019, US2 T020-T027, and US3 T028-T038.
- US1, US2, and US3 are independently testable after Foundation; US2 and US3 integrate with the US1 result/CLI surface.
- Polish T039-T044 depends on all three story checkpoints.

## Parallel Opportunities

- T002-T004 after T001.
- T006-T009 after T005.
- T012-T014, T020-T022, and T028-T032 are independent test-writing tracks.
- T015-T016, T023-T025, and T033-T037 can be split by file boundaries where integration dependencies allow.
- T039-T042 can run in parallel after the story checkpoints.

## Parallel Example: User Story 1

```text
Task: T012 [US1] Metric tests in tests/unit/test_metrics.py
Task: T013 [US1] Summary workflow tests in tests/integration/test_summary_workflow.py
Task: T014 [US1] CLI contract tests in tests/contract/test_cli_summary.py
```

## Parallel Example: User Story 2

```text
Task: T020 [US2] Rule tests in tests/unit/test_alert_rules.py
Task: T021 [US2] Payload contract tests in tests/contract/test_alert_payload.py
Task: T022 [US2] Alert workflow tests in tests/integration/test_alert_workflow.py
```

## Parallel Example: User Story 3

```text
Task: T028 [US3] New invalid fixtures in data/invalid-*.json
Task: T029 [US3] Validation contract tests in tests/contract/test_invalid_packets.py
Task: T030 [US3] Privacy tests in tests/unit/test_privacy_boundary.py
Task: T031 [US3] Prompt-injection tests in tests/unit/test_prompt_injection.py
```

## Implementation Strategy

### MVP First

Complete Setup and Foundation, then implement US1 with the corrected valid packet and fake provider. Verify the real OpenAI path afterward.

### Incremental Delivery

Add US2 deterministic alerts and the reusable payload, then US3 validation/privacy hardening, then final documentation and clean-checkout verification.

## Notes

- Tasks are fresh and unchecked because the clarified data model changes the previous implementation baseline.
- The implementation must preserve the existing channel-neutral payload and fake-provider test path.
- `.env` contains local secrets and remains ignored; `.env.example` contains placeholders only.
