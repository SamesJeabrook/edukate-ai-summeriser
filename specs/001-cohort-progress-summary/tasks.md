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

- [ ] T028 [P] [US3] Add validation contract tests covering all `data/invalid-*.json` fixtures and expected field-specific errors in `tests/contract/test_invalid_packets.py`
- [ ] T029 [P] [US3] Add privacy tests proving learner names, direct identifiers, credential-like values, and sensitive free text are absent from model requests and logs in `tests/unit/test_privacy_boundary.py`
- [ ] T030 [P] [US3] Add prompt-injection tests proving untrusted packet text cannot alter instructions, output labels, or required disclaimers in `tests/unit/test_prompt_injection.py`
- [ ] T031 [P] [US3] Add CLI failure tests proving non-zero exit, no partial output, and non-sensitive stderr for malformed, missing-field, invalid-type, date, duplicate, empty, and insufficient-evidence fixtures in `tests/contract/test_cli_errors.py`

### Implementation for User Story 3

- [ ] T032 [US3] Complete progress-packet and nested activity validation, including required fields, uniqueness, supported types, non-negative values, and valid non-future dates in `src/edukate_progress_summariser/validation.py`
- [ ] T033 [US3] Implement safe error formatting that reports field paths and validation categories without echoing learner-sensitive values or credentials in `src/edukate_progress_summariser/errors.py`
- [ ] T034 [US3] Enforce pre-provider rejection and no-partial-result behavior for invalid packets in `src/edukate_progress_summariser/summariser.py`
- [ ] T035 [US3] Enforce prompt-injection-safe evidence boundaries and output-label invariants in `src/edukate_progress_summariser/prompting.py` and `src/edukate_progress_summariser/summariser.py`
- [ ] T036 [US3] Add credential-safe logging and generation metadata redaction in `src/edukate_progress_summariser/logging_utils.py` and `src/edukate_progress_summariser/privacy.py`
- [ ] T037 [US3] Wire validation and processing errors to CLI exit codes and stderr without writing partial output in `src/edukate_progress_summariser/cli.py`

**Checkpoint**: All invalid fixtures are rejected safely, and valid packets cannot leak learner identifiers or credentials across the AI/logging boundary.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify the complete contract, documentation, security posture, and clean-checkout workflow.

- [ ] T038 [P] Add end-to-end tests for valid output, interpretation failure, invalid input rejection, alert payload shape, and traceability metadata in `tests/integration/test_end_to_end.py`
- [ ] T039 [P] Add formatter compatibility tests proving one canonical payload can produce baseline plain text and future formatter adapters without changing evidence semantics in `tests/contract/test_formatter_compatibility.py`
- [ ] T040 [P] Add package usage and configuration documentation with credential handling and offline test instructions in `README.md`
- [ ] T041 Run the complete quickstart validation scenarios from `specs/001-cohort-progress-summary/quickstart.md` and record any implementation discrepancies in `README.md`
- [ ] T042 Run the complete test suite under Python 3.12+ and verify the package installs from a clean checkout using `python -m unittest discover -s tests -v`

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
- US2: T020, T021, and T022 can run in parallel; T023-T025 can proceed in parallel before T026.
- US3: T028-T031 can run in parallel; T033 and T036 can proceed in parallel with validation implementation.
- Cross-cutting: T038-T040 can run in parallel after story completion.

## Parallel Example: User Story 1

```text
Task: T012 [US1] Metric fixture tests in tests/unit/test_metrics.py
Task: T013 [US1] Fake-provider summary tests in tests/integration/test_summary_workflow.py
Task: T014 [US1] CLI contract tests in tests/contract/test_cli_summary.py
```

## Parallel Example: User Story 2

```text
Task: T020 [US2] Intervention-rule tests in tests/unit/test_alert_rules.py
Task: T021 [US2] Alert payload contract tests in tests/contract/test_alert_payload.py
Task: T022 [US2] Alert identity integration tests in tests/integration/test_alert_workflow.py
```

## Parallel Example: User Story 3

```text
Task: T028 [US3] Invalid fixture contract tests in tests/contract/test_invalid_packets.py
Task: T029 [US3] Privacy boundary tests in tests/unit/test_privacy_boundary.py
Task: T030 [US3] Prompt-injection tests in tests/unit/test_prompt_injection.py
Task: T031 [US3] CLI error tests in tests/contract/test_cli_errors.py
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Complete User Story 1.
3. Run the independent US1 test path with `data/valid-input.json` and a fake provider.
4. Add User Story 2 for actionable escalation output.
5. Add User Story 3 before treating the feature as release-ready because privacy and validation are constitution-mandated.

### Incremental Delivery

1. Setup + Foundation establishes models, validation primitives, configuration, and the provider seam.
2. US1 delivers factual cohort metrics and labelled interpretation.
3. US2 adds deterministic risk alerts and the extensible canonical payload.
4. US3 hardens invalid-input, privacy, credential, and prompt-injection behavior.
5. Polish verifies the complete CLI contract, documentation, and clean-checkout quickstart.

## Notes

- Every task follows the required checklist format: checkbox, sequential ID, optional `[P]`, required story label for story tasks, and a concrete file path.
- Tests are included because the constitution explicitly requires focused tests for data handling, AI output, privacy, prompt injection, failure behavior, and traceability.
- The existing `data/valid-input.json` and `data/invalid-*.json` fixtures are the primary validation inputs.
