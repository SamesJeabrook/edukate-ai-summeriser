# Tasks: Cohort Progress Summary and Escalation Alerts

**Input**: Design documents from `/specs/001-cohort-progress-summary/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md), [contracts/](contracts/)

**Organization**: Tasks are grouped by user story. Existing baseline behavior must remain working while the corrected progress fields, source at-risk flags, and real provider path are added.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the package and test environment for the corrected brief.

- [ ] T001 Verify Python 3.12+ package entry points and test directories in `src/edukate_progress_summariser/__init__.py`, `src/edukate_progress_summariser/__main__.py`, and `tests/`
- [ ] T002 [P] Update packaging metadata and provider dependencies for local editable installation in `pyproject.toml`
- [ ] T003 [P] Verify `.env`, `.env.example`, Python caches, build output, and virtual environments are excluded appropriately in `.gitignore`
- [ ] T004 [P] Add corrected valid and invalid packet fixtures for the new progress fields in `data/valid-input.json` and `data/invalid-*.json`

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared models, configuration, privacy boundaries, and provider selection before story work.

- [ ] T005 Extend learner and cohort models with optional `sessions_attended`, optional `assessments_submitted`, and structured at-risk flags in `src/edukate_progress_summariser/models.py`
- [ ] T006 [P] Define the typed At-Risk Flag model with required `code` and `severity` and optional untrusted descriptive text in `src/edukate_progress_summariser/models.py`
- [ ] T007 [P] Add configuration loading for `OPENAI_API_KEY`, `EDUKATE_MODEL`, packet limits, and provider selection without exposing secrets in `src/edukate_progress_summariser/config.py`
- [ ] T008 [P] Extend privacy-safe evidence construction to exclude names, direct identifiers, flag descriptions, credentials, and arbitrary free text in `src/edukate_progress_summariser/privacy.py` and `src/edukate_progress_summariser/prompting.py`
- [ ] T009 [P] Add real OpenAI provider selection and fail-safe missing-key handling while preserving fake-provider injection in `src/edukate_progress_summariser/ai_service.py` and `src/edukate_progress_summariser/cli.py`
- [ ] T010 Add shared fixture helpers and test constants for sessions, assessments, and at-risk flags in `tests/helpers.py`
- [ ] T011 Add foundation tests for new fields, flag validation, environment precedence, provider selection, and privacy-safe evidence in `tests/unit/test_foundation.py` and `tests/unit/test_ai_service.py`

## Phase 3: User Story 1 - Generate an evidence-based cohort summary (Priority: P1) MVP

**Goal**: Produce an employer-facing summary containing factual sessions, assessments, hours, and source flags alongside labelled AI interpretation.

**Independent Test**: Run the corrected valid packet with a fake provider and verify all new factual fields, source flag code/severity, evidence limitations, and AI labeling.

- [ ] T012 [P] [US1] Extend metric tests for sessions, assessments, hours, and missing-versus-zero values in `tests/unit/test_metrics.py`
- [ ] T013 [P] [US1] Add summary workflow tests proving source flags are factual, AI interpretation is labelled, and flag descriptions/names are excluded from model evidence in `tests/integration/test_summary_workflow.py`
- [ ] T014 [P] [US1] Extend CLI contract tests for canonical and human-readable output containing sessions, assessments, hours, and source flags in `tests/contract/test_cli_summary.py`
- [ ] T015 [US1] Add deterministic aggregation of sessions, assessments, and source flag counts by code and severity, preserving unavailable values in `src/edukate_progress_summariser/metrics.py`
- [ ] T016 [US1] Extend the canonical AI evidence allowlist with session, assessment, hour, activity, recency, and de-identified flag fields in `src/edukate_progress_summariser/prompting.py`
- [ ] T017 [US1] Extend the employer summary with factual sections, source flags, evidence limitations, and labelled AI interpretation in `src/edukate_progress_summariser/summariser.py`
- [ ] T018 [US1] Make the CLI default and documented primary execution path use the configured real provider while retaining explicit fake-provider mode in `src/edukate_progress_summariser/cli.py` and `README.md`
- [ ] T019 [US1] Extend canonical result serialization with the new factual metrics and source flag details in `src/edukate_progress_summariser/cli.py`

## Phase 4: User Story 2 - Identify and communicate intervention needs (Priority: P1)

**Goal**: Escalate stale contact, matching source flags, and configured session/assessment conditions through the channel-neutral payload.

**Independent Test**: Run known flags and metric conditions and verify deterministic alerts preserve source evidence and remain formatter-compatible.

- [ ] T020 [P] [US2] Add rule tests for source flags and session/assessment thresholds with product defaults and employer/cohort overrides in `tests/unit/test_alert_rules.py`
- [ ] T021 [P] [US2] Extend payload contract tests for source flag evidence, categories, severity, learner reference, and disclaimer in `tests/contract/test_alert_payload.py`
- [ ] T022 [P] [US2] Add integration tests for multiple alert categories and channel-neutral payload reuse in `tests/integration/test_alert_workflow.py`
- [ ] T023 [US2] Add versioned default rules for stale contact, matching at-risk flags, low sessions, and missing or low assessments in `src/edukate_progress_summariser/rules.py`
- [ ] T024 [US2] Implement deterministic evaluation for sessions, assessments, and source flags with insufficient-evidence outcomes in `src/edukate_progress_summariser/alerts.py`
- [ ] T025 [US2] Preserve source flag code and severity in alert evidence and distinguish source evidence from AI explanation in `src/edukate_progress_summariser/alerts.py`
- [ ] T026 [US2] Integrate expanded alerts into summary generation and the canonical channel-neutral payload without delivery transmission in `src/edukate_progress_summariser/summariser.py`
- [ ] T027 [US2] Extend text and canonical CLI output to expose all structured alerts without channel-specific credentials or transmission in `src/edukate_progress_summariser/cli.py`

## Phase 5: User Story 3 - Validate and protect the progress packet (Priority: P1)

**Goal**: Validate the corrected fields and protect source flag details, credentials, and real-provider execution.

**Independent Test**: Run all invalid fixtures and provider paths and verify safe rejection, no sensitive model input, and no secret leakage.

- [ ] T028 [P] [US3] Add invalid fixtures for negative/non-integer sessions or assessments, invalid flag shapes, empty code/severity, duplicate flag codes, and malformed new fields in `data/invalid-*.json`
- [ ] T029 [P] [US3] Extend validation contract tests for every new invalid fixture and field-specific safe errors in `tests/contract/test_invalid_packets.py`
- [ ] T030 [P] [US3] Extend privacy tests for flag descriptions, direct identifiers, credentials, and real-provider evidence requests in `tests/unit/test_privacy_boundary.py`
- [ ] T031 [P] [US3] Extend prompt-injection tests for flag descriptions and learner free text in `tests/unit/test_prompt_injection.py`
- [ ] T032 [P] [US3] Extend CLI error tests for missing OpenAI key, invalid new fields, no partial output, safe stderr, and fake-provider fallback in `tests/contract/test_cli_errors.py`
- [ ] T033 [US3] Validate optional sessions, optional assessments, flag objects, code/severity values, duplicate flag codes, and missing-versus-zero semantics in `src/edukate_progress_summariser/validation.py`
- [ ] T034 [US3] Ensure validation errors identify field paths/categories without echoing invalid values, names, descriptions, credentials, or secrets in `src/edukate_progress_summariser/errors.py`
- [ ] T035 [US3] Enforce packet validation and size limits before provider requests or result construction in `src/edukate_progress_summariser/summariser.py`
- [ ] T036 [US3] Enforce the fixed AI evidence allowlist and immutable labels/disclaimers for flags and free text in `src/edukate_progress_summariser/prompting.py` and `src/edukate_progress_summariser/summariser.py`
- [ ] T037 [US3] Ensure OpenAI credentials are read only from trusted configuration and absent from logs, metadata, summaries, and payloads in `src/edukate_progress_summariser/ai_service.py` and `src/edukate_progress_summariser/logging_utils.py`
- [ ] T038 [US3] Return safe non-zero CLI exit codes for provider and validation failures without partial output in `src/edukate_progress_summariser/cli.py`

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T039 [P] Add end-to-end tests for corrected fields, source flags, provider selection, payloads, fallback, and traceability in `tests/integration/test_end_to_end.py`
- [ ] T040 [P] Extend formatter compatibility tests for sessions, assessments, and at-risk evidence in `tests/contract/test_formatter_compatibility.py`
- [ ] T041 [P] Update package usage, `.env` setup, real OpenAI execution, fake-provider testing, input shape, and output examples in `README.md`
- [ ] T042 Update the quickstart with corrected fields, invalid fixture expectations, and real-provider validation in `specs/001-cohort-progress-summary/quickstart.md`
- [ ] T043 Run the complete quickstart under Python 3.12+ and record successful validation results in `README.md`
- [ ] T044 Run the complete test suite and clean editable installation using `python3.12 -m unittest discover -s tests -v` and `python3.12 -m pip install -e .`

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
