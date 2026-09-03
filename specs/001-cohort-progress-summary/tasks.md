# Tasks: Cohort Progress Summary and Escalation Alerts

**Input**: Design documents from `/specs/001-cohort-progress-summary/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md), [contracts/](contracts/)

**Organization**: Tasks are grouped by user story so each increment can be implemented and tested independently after the shared foundation is complete.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare the package and test environment for the corrected brief.

- [ ] T001 Verify the Python 3.12+ package entry points and test directories in `src/edukate_progress_summariser/__init__.py`, `src/edukate_progress_summariser/__main__.py`, and `tests/`
- [ ] T002 [P] Update packaging metadata and provider dependencies for local editable installation in `pyproject.toml`
- [ ] T003 [P] Verify `.env`, `.env.example`, Python caches, build output, and virtual environments are excluded appropriately in `.gitignore`
- [ ] T004 [P] Add corrected valid and invalid packet fixtures for the new progress fields in `data/valid-input.json` and `data/invalid-*.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared models, configuration, privacy boundaries, and provider selection before story work.

**Checkpoint**: Foundation supports sessions, assessments, source flags, real OpenAI execution, and offline fake-provider tests.

- [ ] T005 Extend learner and cohort domain models with optional `sessions_attended`, optional `assessments_submitted`, and structured at-risk flags in `src/edukate_progress_summariser/models.py`
- [ ] T006 [P] Define the typed At-Risk Flag model with required `code` and `severity` and optional untrusted descriptive text in `src/edukate_progress_summariser/models.py`
- [ ] T007 [P] Add configuration loading for `OPENAI_API_KEY`, `EDUKATE_MODEL`, packet limits, and provider selection without exposing secrets in `src/edukate_progress_summariser/config.py`
- [ ] T008 [P] Extend privacy-safe evidence construction to exclude names, direct identifiers, flag descriptions, credentials, and arbitrary free text while retaining allowed progress fields in `src/edukate_progress_summariser/privacy.py` and `src/edukate_progress_summariser/prompting.py`
- [ ] T009 [P] Add real OpenAI provider selection and fail-safe missing-key handling while preserving fake-provider injection in `src/edukate_progress_summariser/ai_service.py` and `src/edukate_progress_summariser/cli.py`
- [ ] T010 Add shared fixture helpers and test constants for sessions, assessments, and at-risk flags in `tests/helpers.py`
- [ ] T011 Add foundation tests for new domain fields, flag validation, environment precedence, provider selection, and privacy-safe evidence in `tests/unit/test_foundation.py` and `tests/unit/test_ai_service.py`

---

## Phase 3: User Story 1 - Generate an evidence-based cohort summary (Priority: P1) MVP

**Goal**: Produce an employer-facing summary that includes sessions attended, assessments submitted, off-the-job hours, and source at-risk flags as factual evidence alongside labelled AI interpretation.

**Independent Test**: Run the corrected valid packet with a fake provider and verify that all new factual fields appear in the summary, flags retain their source code and severity, and AI interpretation is clearly labelled.

### Tests for User Story 1

- [ ] T012 [P] [US1] Extend metric tests for total and per-learner sessions attended, assessments submitted, off-the-job hours, and missing-versus-zero values in `tests/unit/test_metrics.py`
- [ ] T013 [P] [US1] Add summary workflow tests proving source at-risk flags are factual data, AI interpretation is labelled, and model evidence excludes flag descriptions and names in `tests/integration/test_summary_workflow.py`
- [ ] T014 [P] [US1] Extend CLI contract tests for canonical and human-readable output containing sessions, assessments, hours, and source flags in `tests/contract/test_cli_summary.py`

### Implementation for User Story 1

- [ ] T015 [US1] Add deterministic aggregation of sessions, assessments, and source at-risk flag counts by code and severity, preserving unavailable values in `src/edukate_progress_summariser/metrics.py`
- [ ] T016 [US1] Extend the canonical AI evidence allowlist with session, assessment, hour, activity-count, recency, and de-identified flag-code/severity fields in `src/edukate_progress_summariser/prompting.py`
- [ ] T017 [US1] Extend the human-readable employer summary with factual sections for sessions, assessments, off-the-job hours, source flags, evidence limitations, and labelled AI interpretation in `src/edukate_progress_summariser/summariser.py`
- [ ] T018 [US1] Make the CLI default and documented primary execution path use the configured real provider while retaining explicit fake-provider mode for offline tests in `src/edukate_progress_summariser/cli.py` and `README.md`
- [ ] T019 [US1] Extend canonical result serialization with the new factual metrics and source flag details in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: US1 produces a complete employer summary from `data/valid-input.json` with either the real provider or an injected fake provider.

---

## Phase 4: User Story 2 - Identify and communicate intervention needs (Priority: P1)

**Goal**: Escalate stale contact, explicit source at-risk flags, and configured session/assessment conditions through the channel-neutral payload.

**Independent Test**: Run a packet containing known flags and metric conditions, then verify deterministic alerts preserve source code/severity, include evidence, and are reusable by future formatters.

### Tests for User Story 2

- [ ] T020 [P] [US2] Add rule tests for source at-risk flag conditions and session/assessment thresholds with product defaults and employer/cohort overrides in `tests/unit/test_alert_rules.py`
- [ ] T021 [P] [US2] Extend alert payload contract tests for source flag evidence, alert categories, severity, learner reference, and human-review disclaimer in `tests/contract/test_alert_payload.py`
- [ ] T022 [P] [US2] Add integration tests for multiple alert categories and channel-neutral payload reuse without changing source evidence in `tests/integration/test_alert_workflow.py`

### Implementation for User Story 2

- [ ] T023 [US2] Add versioned default rules for stale contact, explicit at-risk flags, low session attendance, and missing or low assessment submissions in `src/edukate_progress_summariser/rules.py`
- [ ] T024 [US2] Implement deterministic rule evaluation for sessions, assessments, and source at-risk flags with explicit insufficient-evidence outcomes in `src/edukate_progress_summariser/alerts.py`
- [ ] T025 [US2] Preserve source flag code and severity in alert triggering evidence and distinguish source evidence from AI explanation in `src/edukate_progress_summariser/alerts.py`
- [ ] T026 [US2] Integrate the expanded alert set into summary generation and the canonical channel-neutral payload without delivery transmission in `src/edukate_progress_summariser/summariser.py`
- [ ] T027 [US2] Extend text and canonical CLI output to expose all structured alerts without channel-specific formatting or credentials in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: US2 returns actionable structured alerts for all supported risk evidence and exposes a reusable payload for future channels.

---

## Phase 5: User Story 3 - Validate and protect the progress packet (Priority: P1)

**Goal**: Validate the new fields, protect source flag details and credentials, and ensure real-provider execution cannot bypass privacy or safety controls.

**Independent Test**: Run all invalid fixtures and real/fake provider paths; verify invalid new-field types are rejected safely, source flag descriptions never reach the model, and no key or sensitive learner data appears in output/logs.

### Tests for User Story 3

- [ ] T028 [P] [US3] Add invalid fixtures for negative or non-integer sessions/assessments, invalid flag shapes, empty codes/severities, duplicate flag codes, and malformed new fields in `data/invalid-*.json`
- [ ] T029 [P] [US3] Extend validation contract tests to cover every new invalid fixture and field-specific non-sensitive errors in `tests/contract/test_invalid_packets.py`
- [ ] T030 [P] [US3] Extend privacy tests for source flag descriptions, direct identifiers, credential-like values, and real-provider evidence requests in `tests/unit/test_privacy_boundary.py`
- [ ] T031 [P] [US3] Extend prompt-injection tests to prove flag descriptions and learner free text cannot change instructions, labels, or disclaimers in `tests/unit/test_prompt_injection.py`
- [ ] T032 [P] [US3] Extend CLI error tests for missing OpenAI key, invalid new fields, no partial output, safe stderr, and fake-provider fallback in `tests/contract/test_cli_errors.py`

### Implementation for User Story 3

- [ ] T033 [US3] Validate optional sessions, optional assessments, at-risk flag objects, code/severity values, duplicate flag codes, and missing-versus-zero semantics in `src/edukate_progress_summariser/validation.py`
- [ ] T034 [US3] Ensure validation errors identify field paths and categories without echoing invalid values, names, descriptions, credentials, or secrets in `src/edukate_progress_summariser/errors.py`
- [ ] T035 [US3] Enforce packet validation and size limits before any provider request or result construction in `src/edukate_progress_summariser/summariser.py`
- [ ] T036 [US3] Enforce the fixed AI evidence allowlist and immutable output labels/disclaimers for all source flag and free-text inputs in `src/edukate_progress_summariser/prompting.py` and `src/edukate_progress_summariser/summariser.py`
- [ ] T037 [US3] Ensure OpenAI credentials are read only from trusted environment configuration and are absent from logs, metadata, summaries, and payloads in `src/edukate_progress_summariser/ai_service.py` and `src/edukate_progress_summariser/logging_utils.py`
- [ ] T038 [US3] Return safe non-zero CLI exit codes for provider configuration and packet validation failures without writing partial output in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: All corrected packets and provider paths satisfy the privacy, validation, and prompt-injection boundaries.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify the corrected brief end to end and document how to run it.

- [ ] T039 [P] Add end-to-end tests covering corrected fields, source flags, real/fake provider selection, alert payloads, fallback, and traceability metadata in `tests/integration/test_end_to_end.py`
- [ ] T040 [P] Extend formatter compatibility tests to prove sessions, assessments, and at-risk evidence survive future channel formatting unchanged in `tests/contract/test_formatter_compatibility.py`
- [ ] T041 [P] Update package usage, `.env` setup, real OpenAI execution, fake-provider testing, input shape, and output examples in `README.md`
- [ ] T042 Update the quickstart with corrected valid-packet fields, invalid fixture expectations, and real-provider validation in `specs/001-cohort-progress-summary/quickstart.md`
- [ ] T043 Run the complete quickstart under Python 3.12+ and record successful validation results in `README.md`
- [ ] T044 Run the complete test suite and clean editable installation from a checkout using `python3.12 -m unittest discover -s tests -v` and `python3.12 -m pip install -e .`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001-T004; T002-T004 can run in parallel after package verification.
- **Foundational (Phase 2)**: T005-T011 depend on setup; T006-T009 can run in parallel after the model shape is agreed.
- **User Story 1 (Phase 3)**: T012-T019 depend on the foundation; tests can run in parallel before implementation.
- **User Story 2 (Phase 4)**: T020-T027 depend on the corrected models and US1 result shape; rule and payload work can proceed in parallel before integration.
- **User Story 3 (Phase 5)**: T028-T038 depend on the corrected validation/privacy interfaces; tests can run in parallel before hardening implementation.
- **Polish (Phase 6)**: T039-T044 depend on all three user-story checkpoints.

### User Story Dependencies

- **US1 (P1)**: Depends on the foundational phase and is the MVP for the corrected data shape.
- **US2 (P1)**: Depends on the foundational phase and the US1 result model; it adds deterministic alerts without channel delivery.
- **US3 (P1)**: Depends on the foundational validation/privacy interfaces and must pass before release.

### Parallel Opportunities

- T002-T004 after setup verification.
- T006-T009 after the model contract is fixed.
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

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Add the corrected valid packet shape and deterministic summary fields.
3. Complete User Story 1 and validate with the fake provider.
4. Verify the real OpenAI path with a configured local key.

### Incremental Delivery

1. US1 adds sessions, assessments, source flags, and the real-provider primary path.
2. US2 adds deterministic escalation rules and the reusable structured payload.
3. US3 validates and hardens all new data and provider boundaries.
4. Polish runs the complete quickstart and clean-install test suite.

## Notes

- Tasks are intentionally fresh and unchecked because they represent the corrected brief after the earlier baseline implementation.
- The implementation must preserve the existing channel-neutral payload and fake-provider test path.
- `.env` contains local secrets and must remain ignored; `.env.example` contains placeholders only.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the Python package, local installation, and test entry point.

- [ ] T001 Verify the Python 3.12+ package entry points and test directories in `src/edukate_progress_summariser/__init__.py`, `src/edukate_progress_summariser/__main__.py`, and `tests/`
- [ ] T002 [P] Update packaging metadata and provider dependencies for local editable installation in `pyproject.toml`
- [ ] T003 [P] Verify `.env`, `.env.example`, Python caches, build output, and virtual environments are excluded appropriately in `.gitignore`
- [ ] T004 [P] Add corrected valid and invalid packet fixtures for the new progress fields in `data/valid-input.json` and `data/invalid-*.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared models, configuration, privacy boundaries, and provider selection before story work.

**Checkpoint**: Foundation supports sessions, assessments, source flags, real OpenAI execution, and offline fake-provider tests.

- [ ] T005 Extend learner and cohort domain models with `sessions_attended`, `assessments_submitted`, and structured at-risk flags in `src/edukate_progress_summariser/models.py`
- [ ] T006 [P] Define the typed At-Risk Flag model with required `code` and `severity` and optional untrusted descriptive text in `src/edukate_progress_summariser/models.py`
- [ ] T007 [P] Add configuration loading for `OPENAI_API_KEY`, `EDUKATE_MODEL`, packet limits, and provider selection without exposing secrets in `src/edukate_progress_summariser/config.py`
- [ ] T008 [P] Extend privacy-safe evidence construction to exclude names, direct identifiers, flag descriptions, credentials, and arbitrary free text while retaining allowed progress fields in `src/edukate_progress_summariser/privacy.py` and `src/edukate_progress_summariser/prompting.py`
- [ ] T009 [P] Add real OpenAI provider selection and fail-safe missing-key handling while preserving fake-provider injection in `src/edukate_progress_summariser/ai_service.py` and `src/edukate_progress_summariser/cli.py`
- [ ] T010 Add shared fixture helpers and test constants for sessions, assessments, and at-risk flags in `tests/helpers.py`
- [ ] T011 Add foundation tests for new domain fields, flag validation, environment precedence, provider selection, and privacy-safe evidence in `tests/unit/test_foundation.py` and `tests/unit/test_ai_service.py`

---

## Phase 3: User Story 1 - Generate an evidence-based cohort summary (Priority: P1) MVP

**Goal**: Produce an employer-facing summary that includes sessions attended, assessments submitted, off-the-job hours, and source at-risk flags as factual evidence alongside labelled AI interpretation.

**Independent Test**: Run the corrected valid packet with a fake provider and verify that all new factual fields appear in the summary, flags retain their source code and severity, and AI interpretation is clearly labelled.

### Tests for User Story 1

- [ ] T012 [P] [US1] Extend metric tests for total and per-learner sessions attended, assessments submitted, off-the-job hours, and missing-versus-zero values in `tests/unit/test_metrics.py`
- [ ] T013 [P] [US1] Add summary workflow tests proving source at-risk flags are factual data, AI interpretation is labelled, and model evidence excludes flag descriptions and names in `tests/integration/test_summary_workflow.py`
- [ ] T014 [P] [US1] Extend CLI contract tests for canonical and human-readable output containing sessions, assessments, hours, and source flags in `tests/contract/test_cli_summary.py`

### Implementation for User Story 1

- [ ] T015 [US1] Add deterministic aggregation of sessions, assessments, and source at-risk flag counts by code and severity in `src/edukate_progress_summariser/metrics.py`
- [ ] T016 [US1] Extend the canonical AI evidence allowlist with session, assessment, hour, activity-count, recency, and de-identified flag-code/severity fields in `src/edukate_progress_summariser/prompting.py`
- [ ] T017 [US1] Extend the human-readable employer summary with factual sections for sessions, assessments, off-the-job hours, source flags, evidence limitations, and labelled AI interpretation in `src/edukate_progress_summariser/summariser.py`
- [ ] T018 [US1] Make the CLI default and documented primary execution path use the configured real provider while retaining explicit fake-provider mode for offline tests in `src/edukate_progress_summariser/cli.py` and `README.md`
- [ ] T019 [US1] Extend canonical result serialization with the new factual metrics and source flag details in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: US1 produces a complete employer summary from `data/valid-input.json` with either the real provider or an injected fake provider.

---

## Phase 4: User Story 2 - Identify and communicate intervention needs (Priority: P1)

**Goal**: Escalate stale contact, explicit source at-risk flags, and configured session/assessment conditions through the channel-neutral payload.

**Independent Test**: Run a packet containing known flags and metric conditions, then verify deterministic alerts preserve source code/severity, include evidence, and are reusable by future formatters.

### Tests for User Story 2

- [ ] T020 [P] [US2] Add rule tests for source at-risk flag conditions and session/assessment thresholds with product defaults and employer/cohort overrides in `tests/unit/test_alert_rules.py`
- [ ] T021 [P] [US2] Extend alert payload contract tests for source flag evidence, alert categories, severity, learner reference, and human-review disclaimer in `tests/contract/test_alert_payload.py`
- [ ] T022 [P] [US2] Add integration tests for multiple alert categories and channel-neutral payload reuse without changing source evidence in `tests/integration/test_alert_workflow.py`

### Implementation for User Story 2

- [ ] T023 [US2] Add versioned default rules for stale contact, explicit at-risk flags, low session attendance, and missing or low assessment submissions in `src/edukate_progress_summariser/rules.py`
- [ ] T024 [US2] Implement deterministic rule evaluation for sessions, assessments, and source at-risk flags with explicit insufficient-evidence outcomes in `src/edukate_progress_summariser/alerts.py`
- [ ] T025 [US2] Preserve source flag code and severity in alert triggering evidence and distinguish source evidence from AI explanation in `src/edukate_progress_summariser/alerts.py`
- [ ] T026 [US2] Integrate the expanded alert set into summary generation and the canonical channel-neutral payload without delivery transmission in `src/edukate_progress_summariser/summariser.py`
- [ ] T027 [US2] Extend text and canonical CLI output to expose all structured alerts without channel-specific formatting or credentials in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: US2 returns actionable structured alerts for all supported risk evidence and exposes a reusable payload for future channels.

---

## Phase 5: User Story 3 - Validate and protect the progress packet (Priority: P1)

**Goal**: Validate the new fields, protect source flag details and credentials, and ensure real-provider execution cannot bypass privacy or safety controls.

**Independent Test**: Run all invalid fixtures and real/fake provider paths; verify invalid new-field types are rejected safely, source flag descriptions never reach the model, and no key or sensitive learner data appears in output/logs.

### Tests for User Story 3

- [ ] T028 [P] [US3] Add invalid fixtures for negative or non-integer sessions/assessments, invalid flag shapes, empty codes/severities, duplicate flag codes, and malformed new fields in `data/invalid-*.json`
- [ ] T029 [P] [US3] Extend validation contract tests to cover every new invalid fixture and field-specific non-sensitive errors in `tests/contract/test_invalid_packets.py`
- [ ] T030 [P] [US3] Extend privacy tests for source flag descriptions, direct identifiers, credential-like values, and real-provider evidence requests in `tests/unit/test_privacy_boundary.py`
- [ ] T031 [P] [US3] Extend prompt-injection tests to prove flag descriptions and learner free text cannot change instructions, labels, or disclaimers in `tests/unit/test_prompt_injection.py`
- [ ] T032 [P] [US3] Extend CLI error tests for missing OpenAI key, invalid new fields, no partial output, safe stderr, and fake-provider fallback in `tests/contract/test_cli_errors.py`

### Implementation for User Story 3

- [ ] T033 [US3] Validate sessions, assessments, at-risk flag objects, code/severity values, duplicate flag codes, and missing-versus-zero semantics in `src/edukate_progress_summariser/validation.py`
- [ ] T034 [US3] Ensure validation errors identify field paths and categories without echoing invalid values, names, descriptions, credentials, or secrets in `src/edukate_progress_summariser/errors.py`
- [ ] T035 [US3] Enforce packet validation and size limits before any provider request or result construction in `src/edukate_progress_summariser/summariser.py`
- [ ] T036 [US3] Enforce the fixed AI evidence allowlist and immutable output labels/disclaimers for all source flag and free-text inputs in `src/edukate_progress_summariser/prompting.py` and `src/edukate_progress_summariser/summariser.py`
- [ ] T037 [US3] Ensure OpenAI credentials are read only from trusted environment configuration and are absent from logs, metadata, summaries, and payloads in `src/edukate_progress_summariser/ai_service.py` and `src/edukate_progress_summariser/logging_utils.py`
- [ ] T038 [US3] Return safe non-zero CLI exit codes for provider configuration and packet validation failures without writing partial output in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: All corrected packets and provider paths satisfy the privacy, validation, and prompt-injection boundaries.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify the corrected brief end to end and document how to run it.

- [ ] T039 [P] Add end-to-end tests covering corrected fields, source flags, real/fake provider selection, alert payloads, fallback, and traceability metadata in `tests/integration/test_end_to_end.py`
- [ ] T040 [P] Extend formatter compatibility tests to prove sessions, assessments, and at-risk evidence survive future channel formatting unchanged in `tests/contract/test_formatter_compatibility.py`
- [ ] T041 [P] Update package usage, `.env` setup, real OpenAI execution, fake-provider testing, input shape, and output examples in `README.md`
- [ ] T042 Update the quickstart with corrected valid-packet fields, invalid fixture expectations, and real-provider validation in `specs/001-cohort-progress-summary/quickstart.md`
- [ ] T043 Run the complete quickstart under Python 3.12+ and record successful validation results in `README.md`
- [ ] T044 Run the complete test suite and clean editable installation from a checkout using `python3.12 -m unittest discover -s tests -v` and `python3.12 -m pip install -e .`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001-T004; T002-T004 can run in parallel after package verification.
- **Foundational (Phase 2)**: T005-T011 depend on setup; T006-T009 can run in parallel after the model shape is agreed.
- **User Story 1 (Phase 3)**: T012-T019 depend on the foundation; tests can run in parallel before implementation.
- **User Story 2 (Phase 4)**: T020-T027 depend on the corrected models and US1 result shape; rule and payload work can proceed in parallel before integration.
- **User Story 3 (Phase 5)**: T028-T038 depend on the corrected validation/privacy interfaces; tests can run in parallel before hardening implementation.
- **Polish (Phase 6)**: T039-T044 depend on all three user-story checkpoints.

### User Story Dependencies

- **US1 (P1)**: Depends on the foundational phase and is the MVP for the corrected data shape.
- **US2 (P1)**: Depends on the foundational phase and the US1 result model; it adds deterministic alerts without channel delivery.
- **US3 (P1)**: Depends on the foundational validation/privacy interfaces and must pass before release.

### Parallel Opportunities

- T002-T004 after setup verification.
- T006-T009 after the model contract is fixed.
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

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Add the corrected valid packet shape and deterministic summary fields.
3. Complete User Story 1 and validate with the fake provider.
4. Verify the real OpenAI path with a configured local key.

### Incremental Delivery

1. US1 adds sessions, assessments, source flags, and the real-provider primary path.
2. US2 adds deterministic escalation rules and the reusable structured payload.
3. US3 validates and hardens all new data and provider boundaries.
4. Polish runs the complete quickstart and clean-install test suite.

## Notes

- Tasks are intentionally fresh and unchecked because they represent the corrected brief after the earlier baseline implementation.
- The implementation must preserve the existing channel-neutral payload and fake-provider test path.
- `.env` contains local secrets and must remain ignored; `.env.example` contains placeholders only.

# Tasks: Cohort Progress Summary and Escalation Alerts

**Input**: Design documents from `/specs/001-cohort-progress-summary/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md), [contracts/](contracts/)

**Organization**: Tasks are grouped by user story so each increment can be implemented and tested independently after the shared foundation is complete.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the Python package, local installation, and test entry point.

- [x] T001 Create the `src/edukate_progress_summariser/` package, `tests/` subdirectories, and package entry points in `src/edukate_progress_summariser/__init__.py` and `src/edukate_progress_summariser/__main__.py`
- [x] T002 [P] Create `pyproject.toml` with Python 3.12+ metadata, editable-install configuration, and the official OpenAI SDK dependency in `pyproject.toml`
- [x] T003 [P] Configure repository exclusions for `.venv/`, bytecode, build output, and test caches in `.gitignore`
- [x] T004 [P] Add the standard-library test discovery configuration and shared test helpers in `tests/__init__.py` and `tests/helpers.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared domain types, safe configuration, validation primitives, and provider boundaries required by all stories.

**Checkpoint**: Foundation ready; user story work can proceed independently in parallel.

- [x] T005 Define typed domain models for progress packets, learners, activity records, intervention rules, facts, alerts, payloads, metadata, and result states in `src/edukate_progress_summariser/models.py`
- [x] T006 [P] Implement JSON loading, field-path error collection, date parsing, and distinction between missing, null, zero, and invalid values in `src/edukate_progress_summariser/validation.py`
- [x] T007 [P] Implement environment/configuration loading for model selection, packet limits, and product/employer/cohort intervention-rule defaults without exposing credentials in `src/edukate_progress_summariser/config.py`
- [x] T008 [P] Define the replaceable AI provider protocol and official OpenAI SDK adapter boundary in `src/edukate_progress_summariser/ai_service.py`
- [x] T009 [P] Implement derived non-identifying learner-reference generation and sensitive-field redaction helpers in `src/edukate_progress_summariser/privacy.py`
- [x] T010 Add foundational unit tests for domain construction, configuration precedence, date parsing, reference derivation, and redaction in `tests/unit/test_foundation.py`
- [x] T011 Add provider-boundary tests proving fake-provider injection works without network access or credentials in `tests/unit/test_ai_service.py`

---

## Phase 3: User Story 1 - Generate an evidence-based cohort summary (Priority: P1) MVP

**Goal**: Turn a valid JSON cohort packet into deterministic factual metrics plus clearly labelled AI interpretation and evidence limitations.

**Independent Test**: Run the sample valid packet through the library with a fake provider and verify cohort facts, labelled interpretation, evidence status, and non-sensitive metadata are returned.

### Tests for User Story 1

- [x] T012 [P] [US1] Add fixture-driven metric tests for learner count, hours, meetings, workshops, recency, missing evidence, and zero values in `tests/unit/test_metrics.py`
- [x] T013 [P] [US1] Add fake-provider summary tests for factual-versus-interpretive labelling, prompt input ordering, model metadata, and interpretation-unavailable fallback in `tests/integration/test_summary_workflow.py`
- [x] T014 [P] [US1] Add CLI contract tests for successful canonical and text output using `data/valid-input.json` in `tests/contract/test_cli_summary.py`

### Implementation for User Story 1

- [x] T015 [US1] Implement deterministic cohort and learner progress calculations in `src/edukate_progress_summariser/metrics.py`
- [x] T016 [US1] Implement minimum-evidence prompt construction that excludes learner names, direct identifiers, credentials, and untrusted free-text instructions in `src/edukate_progress_summariser/prompting.py`
- [x] T017 [US1] Implement human-readable employer summary assembly with factual sections, AI interpretation labels, evidence-sufficiency status, and generation metadata in `src/edukate_progress_summariser/summariser.py`
- [x] T018 [US1] Implement summary orchestration that computes deterministic facts before invoking the provider and preserves facts when interpretation fails in `src/edukate_progress_summariser/summariser.py`
- [x] T019 [US1] Implement CLI argument parsing, input loading, result serialization, and successful exit behavior in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: User Story 1 works independently with `data/valid-input.json`, a fake provider, and no external network call.

---

## Phase 4: User Story 2 - Identify and communicate intervention needs (Priority: P1)

**Goal**: Apply configured intervention rules and return structured alerts plus a channel-neutral payload that future formatters can consume.

**Independent Test**: Run records with stale contact, absent activity, and insufficient evidence through the alert workflow and verify alert fields, severity, evidence, human-review language, and canonical payload structure.

### Tests for User Story 2

- [x] T020 [P] [US2] Add intervention-rule evaluation tests for default thresholds, employer/cohort overrides, matching conditions, severity, and insufficient evidence in `tests/unit/test_alert_rules.py`
- [x] T021 [P] [US2] Add alert payload contract tests against `specs/001-cohort-progress-summary/contracts/output-schema.json` in `tests/contract/test_alert_payload.py`
- [x] T022 [P] [US2] Add multi-alert integration tests proving learner identity is account-manager-facing while AI evidence uses derived references in `tests/integration/test_alert_workflow.py`

### Implementation for User Story 2

- [x] T023 [US2] Implement product-default and employer/cohort override selection for versioned intervention rules in `src/edukate_progress_summariser/rules.py`
- [x] T024 [US2] Implement deterministic alert evaluation with explicit insufficient-evidence results in `src/edukate_progress_summariser/alerts.py`
- [x] T025 [US2] Implement canonical channel-neutral alert payload construction with cohort context, required evidence, labels, disclaimers, and metadata in `src/edukate_progress_summariser/alerts.py`
- [x] T026 [US2] Add result integration so summary generation includes structured alerts and the canonical `alert_payload` without channel delivery behavior in `src/edukate_progress_summariser/summariser.py`
- [x] T027 [US2] Extend CLI serialization and text rendering to expose structured alerts and the canonical payload without channel-specific credentials or transmission in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: User Stories 1 and 2 work independently after foundation; the canonical payload can be handed to future Slack, email, or other formatters.

---

## Phase 5: User Story 3 - Validate and protect the progress packet (Priority: P1)

**Goal**: Reject malformed or unsafe packets with specific non-sensitive errors and enforce privacy, credential, and prompt-injection boundaries.

**Independent Test**: Run every `data/invalid-*.json` fixture and verify invalid packets produce non-zero exits, field-specific safe errors, no model request, and no partial summary or payload; run security tests with a recording fake provider.

### Tests for User Story 3

- [x] T028 [P] [US3] Add validation contract tests covering all `data/invalid-*.json` fixtures and expected field-specific errors in `tests/contract/test_invalid_packets.py`
- [x] T029 [P] [US3] Add privacy tests proving learner names, direct identifiers, credential-like values, and sensitive free text are absent from model requests and logs in `tests/unit/test_privacy_boundary.py`
- [x] T030 [P] [US3] Add prompt-injection tests proving untrusted packet text cannot alter instructions, output labels, or required disclaimers in `tests/unit/test_prompt_injection.py`
- [x] T031 [P] [US3] Add CLI failure tests proving non-zero exit, no partial output, and non-sensitive stderr for malformed, missing-field, invalid-type, date, duplicate, empty, and insufficient-evidence fixtures in `tests/contract/test_cli_errors.py`

### Implementation for User Story 3

- [x] T032 [US3] Complete progress-packet and nested activity validation, including required fields, uniqueness, supported types, non-negative values, and valid non-future dates in `src/edukate_progress_summariser/validation.py`
- [x] T033 [US3] Implement safe error formatting that reports field paths and validation categories without echoing learner-sensitive values or credentials in `src/edukate_progress_summariser/errors.py`
- [x] T034 [US3] Enforce pre-provider rejection and no-partial-result behavior for invalid packets in `src/edukate_progress_summariser/summariser.py`
- [x] T035 [US3] Enforce prompt-injection-safe evidence boundaries and output-label invariants in `src/edukate_progress_summariser/prompting.py` and `src/edukate_progress_summariser/summariser.py`
- [x] T036 [US3] Add credential-safe logging and generation metadata redaction in `src/edukate_progress_summariser/logging_utils.py` and `src/edukate_progress_summariser/privacy.py`
- [x] T037 [US3] Wire validation and processing errors to CLI exit codes and stderr without writing partial output in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: All invalid fixtures are rejected safely, and valid packets cannot leak learner identifiers or credentials across the AI/logging boundary.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify the complete contract, documentation, security posture, and clean-checkout workflow.

- [x] T038 [P] Add end-to-end tests for valid output, interpretation failure, invalid input rejection, alert payload shape, and traceability metadata in `tests/integration/test_end_to_end.py`
- [x] T039 [P] Add formatter compatibility tests proving one canonical payload can produce baseline plain text and future formatter adapters without changing evidence semantics in `tests/contract/test_formatter_compatibility.py`
- [x] T040 [P] Add package usage and configuration documentation with credential handling and offline test instructions in `README.md`
- [x] T041 Run the complete quickstart validation scenarios from `specs/001-cohort-progress-summary/quickstart.md` and record any implementation discrepancies in `README.md`
- [x] T042 Run the complete test suite under Python 3.12+ and verify the package installs from a clean checkout using `python -m unittest discover -s tests -v`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001-T004; no dependencies and T002-T004 can run in parallel after T001 where needed.
- **Foundational (Phase 2)**: T005-T011 depend on setup; T006-T009 can proceed in parallel after T005, while T010-T011 follow their respective foundation modules.
- **User Story 1 (Phase 3)**: T012-T019 depend on the foundational phase; its tests can be written in parallel, then implementation proceeds from metrics and prompting into orchestration and CLI.
- **User Story 2 (Phase 4)**: T020-T027 depend on T005-T009 and can reuse the US1 result model; rule/payload work can proceed in parallel before integration.
- **User Story 3 (Phase 5)**: T028-T037 depend on foundational validation/privacy boundaries; fixture tests can start in parallel with error and logging implementation.
- **Polish (Phase 6)**: T038-T042 depend on the desired user-story checkpoints being complete.

### User Story Dependencies

- **US1 (P1)**: Depends only on the foundational phase. This is the MVP increment.
- **US2 (P1)**: Depends on foundational models and can be developed in parallel with US1; T026-T027 integrate with the shared result/CLI surface.
- **US3 (P1)**: Depends on foundational validation/privacy boundaries and can be developed in parallel with US1/US2; its hard-rejection behavior must be complete before release.

### Parallel Opportunities

- Setup: T002, T003, and T004 can run in parallel after T001.
- Foundation: T006, T007, T008, and T009 can run in parallel after T005; T010 and T011 can then run alongside story test authoring.
- US1: T012, T013, and T014 can run in parallel; T015 and T016 can then proceed in parallel.
