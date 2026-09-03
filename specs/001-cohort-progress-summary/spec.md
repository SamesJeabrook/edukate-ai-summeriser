# Feature Specification: Cohort Progress Summary and Escalation Alerts

**Feature Branch**: `001-cohort-progress-summary`

**Created**: 2026-09-03

**Status**: Draft

**Input**: User description: "As an account manager, I want to provide learner progress data for an employee's cohort and receive an evidence based cohort summary and structured escalation alerts, so that I can quickly communicate progress to the employer and identify learners requiring intervention. The data will be provided from a JSON packet."

## Clarifications

### Session 2026-09-03

- Q: Should the final cohort summary and escalation payload identify learners by name, by a non-identifying learner reference, or by both? → A: Both a learner reference and learner name may appear in account-manager-facing output; only the non-identifying reference and minimum evidence are used for AI processing.
- Q: Should intervention thresholds be fixed product-defined defaults, configurable per employer or cohort, or configurable by the account manager during each review? → A: Product-defined defaults with thresholds configurable per employer or cohort.
- Q: Should each learner record be required to provide a stable non-identifying learner reference, or should the system generate one when the JSON packet contains only a learner name? → A: Use the learner name as the account-manager-facing reference; derive a non-identifying reference for AI processing.
- Q: Should `sessions_attended` and `assessments_submitted` be required for every learner record, or should they be optional when the source system does not provide them? → A: Allow missing values; distinguish missing from zero and report the evidence limitation.
- Q: Should every source-provided at-risk flag automatically create an escalation alert, or should only flags matching configured rules create alerts? → A: Treat source flags as evidence and create alerts only when they match configured intervention rules.

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Generate an evidence-based cohort summary (Priority: P1)

As an account manager, I want to provide a valid JSON progress packet and receive a concise cohort summary so that I can communicate overall learner progress to the employer using the available evidence.

**Why this priority**: The cohort summary is the primary employer communication outcome and is useful even when no individual escalation is required.

**Independent Test**: Provide the sample engineering-manager JSON packet and verify that the result describes sessions attended, assessments submitted, off-the-job hours, and supplied at-risk flags, distinguishes reported facts from interpretation, identifies evidence limitations, and can be reviewed without inspecting the source packet.

**Acceptance Scenarios**:

1. **Given** a valid JSON packet containing an employer or cohort identifier and learner progress records, **When** the account manager requests a summary, **Then** the system presents cohort-level factual metrics for sessions attended, assessments submitted, off-the-job hours, and supplied at-risk flags, together with an evidence-based interpretation of overall progress.
2. **Given** a packet with incomplete learner activity fields, **When** the account manager requests a summary, **Then** the system identifies missing or incomplete evidence and avoids presenting unsupported conclusions as facts.
3. **Given** a generated summary, **When** the account manager reviews it, **Then** AI-generated interpretation is clearly labelled separately from factual data supplied in the packet.

### User Story 2 - Identify and communicate intervention needs (Priority: P1)

As an account manager, I want structured escalation alerts for learners who may require intervention so that I can prioritise follow-up and communicate specific evidence to the employer through a channel-ready payload.

**Why this priority**: Timely identification of learners needing support is the second critical outcome and turns the summary into an actionable employer conversation.

**Independent Test**: Provide records containing stale contact, absent activity, and incomplete data, then verify that each applicable alert contains a learner reference, severity, trigger evidence, explanation, recommended human follow-up, and a channel-neutral payload that can be formatted for Slack, email, or a future communication channel.

**Acceptance Scenarios**:

1. **Given** a learner record meets one or more configured intervention rules, **When** the summary is generated, **Then** the result includes one structured alert per applicable learner with the triggering evidence and a severity level.
2. **Given** a learner record does not contain enough evidence to assess an intervention rule, **When** the summary is generated, **Then** the result marks the assessment as insufficient evidence rather than inventing a risk conclusion.
3. **Given** a structured alert, **When** the account manager reviews it, **Then** the alert states that it supports human follow-up and does not represent an automatic employment or learner outcome decision.
4. **Given** one or more structured alerts, **When** the result is prepared for communication, **Then** the system produces a channel-neutral payload containing the cohort context, alert severity, affected learner reference, evidence, explanation, recommended follow-up, and human-review disclaimer, which can be passed to a Slack or email formatter without sending the alert or requiring channel-specific delivery configuration.

### User Story 3 - Validate and protect the progress packet (Priority: P1)

As an account manager, I want clear feedback when a JSON packet is invalid or sensitive data is handled incorrectly so that I can correct the input without exposing learner information.

**Why this priority**: Reliable input handling and privacy protection are prerequisites for trustworthy employer communication.

**Independent Test**: Submit valid, malformed, incomplete, and adversarial packets and verify that valid packets are processed, invalid packets receive actionable non-sensitive errors, and learner-identifying data is not sent to the language model or written to logs.

**Acceptance Scenarios**:

1. **Given** a malformed JSON packet, **When** the account manager submits it, **Then** processing stops with an actionable validation message and no summary or alert is produced.
2. **Given** a packet containing learner names or other identifying details, **When** interpretation is requested, **Then** the account-manager-facing result may use the learner name as the learner reference, while the language model receives only a derived non-identifying reference and the minimum de-identified evidence required for the requested analysis.
3. **Given** learner-provided text contains instructions attempting to change the system's behaviour, **When** the packet is processed, **Then** the content is treated as untrusted evidence and cannot override the summary, privacy, or output-labelling rules.
4. **Given** a syntactically valid packet contains an invalid field type or date, such as text in `otj_hours`, a text value instead of a meetings list, or a malformed or future activity date, **When** the account manager submits it, **Then** processing stops with a field-specific, non-sensitive validation message and no summary or escalation payload is produced.

### Edge Cases

- A packet is valid JSON but lacks the employer or cohort identifier, contains no learners, or has duplicate learner references; the system reports the specific validation issue and does not generate a misleading empty summary.
- A learner has no meetings or workshops, a null last-contact value, zero recorded hours, or activity fields with unexpected types; the system preserves the distinction between zero, missing, and invalid data.
- Dates are missing, malformed, in the future, or inconsistent with the stated recency value; the system flags the affected evidence as unreliable instead of silently calculating a conclusion.
- A packet contains unexpected additional fields or learner-generated free text; the system ignores unsupported fields unless they are explicitly accepted as evidence and treats free text as untrusted.
- The language model is unavailable, returns unusable content, or produces unsupported claims; the system reports that interpretation is unavailable and retains any validated factual metrics without fabricating alerts.
- The packet includes more learners or activity records than the supported processing limit; the system reports the limit and does not partially present an unlabelled result.

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: The system MUST accept a JSON packet representing one employer or cohort and its learner progress records.
- **FR-002**: The system MUST validate the packet structure, required identifiers, learner references, supported data types, and date values before generating output.
- **FR-003**: The system MUST distinguish missing, null, zero, and invalid values when calculating or presenting progress evidence.
- **FR-004**: The system MUST calculate and present cohort-level factual measures from the packet, including learner count, recorded progress hours, contact activity, workshop activity, and available recency information.
- **FR-004a**: The system MUST calculate and present cohort-level factual measures for sessions attended, assessments submitted, and off-the-job hours, preserving per-learner values where relevant.
- **FR-004b**: The system MUST present supplied at-risk flags as factual source data separately from any AI-generated interpretation and MUST preserve each flag's code and severity.
- **FR-005**: The system MUST present factual packet data separately from any generated interpretation and label all generated interpretation as AI-generated.
- **FR-006**: The system MUST state when evidence is incomplete, conflicting, stale, or insufficient to support a conclusion.
- **FR-007**: The system MUST apply the defined intervention rules to each assessable learner and create structured alerts only for matching conditions; source-provided at-risk flags that do not match a configured rule remain factual summary evidence without creating an alert.
- **FR-008**: Each escalation alert MUST include a learner reference, severity, alert category, triggering evidence, explanation, recommended human follow-up, and an indication of whether the evidence is complete.
- **FR-009**: The system MUST avoid presenting an alert as a diagnosis, employment decision, guaranteed outcome, or substitute for account-manager or employer judgement.
- **FR-010**: The system MUST produce a channel-neutral alert payload that can be formatted for Slack, email, and additional communication channels added later.
- **FR-011**: Each alert payload MUST include the cohort context, alert severity, affected learner reference, learner name as the reference when available to the authorised account manager, alert category, triggering evidence, explanation, recommended human follow-up, evidence-completeness status, AI-generated-content label where applicable, and human-review disclaimer.
- **FR-012**: The channel-neutral payload MUST remain independent of channel-specific delivery settings, credentials, templates, and transmission behavior; the exact formatted elements and channel presentation rules will be defined during planning.
- **FR-013**: The system MUST provide product-defined default intervention rules and thresholds, allow those thresholds to be configured per employer or cohort, and apply the applicable configuration without changing the source progress packet format.
- **FR-014**: The system MUST keep learner names and other direct identifiers available only to the authorised account-manager-facing result, MUST use the learner name as the account-manager-facing reference when no separate reference is provided, and MUST send the language model only a derived non-identifying reference and the minimum evidence necessary for interpretation.
- **FR-015**: The system MUST treat all learner-generated or packet-provided free text as untrusted input and prevent it from changing processing instructions, privacy controls, or output labels.
- **FR-016**: The system MUST keep credentials outside user-visible output and MUST NOT write learner-identifying data or credentials to logs.
- **FR-017**: The system MUST record non-sensitive generation metadata sufficient to identify the configured model version, generation time, input packet reference, and output status without reproducing learner content.
- **FR-018**: The system MUST handle validation failures and language-model failures with clear, non-sensitive messages and MUST preserve validated factual measures when interpretation cannot be generated.
- **FR-019**: The system MUST produce a reviewable result that an account manager can use to communicate cohort progress and prioritise learner follow-up.

### Key Entities _(include if feature involves data)_

- **Progress Packet**: A JSON-provided snapshot for one employer or cohort, including its identifier and learner progress records.
- **Learner Progress Record**: A learner name when available, an optional source reference, and the available evidence about their programme, sessions, assessments, hours, meetings, workshops, recency, at-risk flags, and supported activity fields.
- **At-Risk Flag**: A source-provided indication requiring review, containing a machine-readable code and severity; it is evidence to assess, not an automatic outcome or diagnosis.
- **Cohort Summary**: A reviewable result containing validated cohort facts, clearly labelled AI-generated interpretation, evidence limitations, and generation metadata.
- **Escalation Alert**: A structured, human-reviewable indication that a learner record matches an intervention rule, including severity, evidence, rationale, and recommended follow-up.
- **Alert Payload**: A channel-neutral representation of one or more escalation alerts, including the authorised account-manager-facing learner reference when available, that contains the information needed to produce Slack, email, or future channel formats without making those channels part of this feature's delivery behavior.
- **Intervention Rule**: A named condition and threshold used to identify evidence that warrants account-manager review.
- **Generation Metadata**: Non-sensitive information about when and how a result was generated and which input evidence reference and model configuration were used.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: For a valid packet within the supported size limit, an account manager can obtain a reviewable cohort summary and alert list in under 2 minutes from submission.
- **SC-002**: In validation tests covering valid, malformed, incomplete, null, zero, and inconsistent values, 100% of invalid packets are rejected with a specific non-sensitive reason and 0% produce an unlabelled summary.
- **SC-003**: In an evaluation set with known intervention conditions, at least 95% of expected matching learner records receive an alert containing the required evidence fields, and no alert is generated where the required evidence is explicitly insufficient.
- **SC-003a**: In an evaluation set containing known session, assessment, and at-risk-flag values, 100% of valid records expose those values in the factual summary without converting them into unsupported AI claims.
- **SC-004**: In payload review tests, 100% of generated alert payloads contain the required communication fields and can be transformed into a Slack format, an email format, or an additional supported channel format without reinterpreting the underlying alert evidence.
- **SC-005**: In review tests, 100% of generated interpretations are visibly identified as AI-generated and 100% of summaries include an explicit evidence-sufficiency statement.
- **SC-006**: In privacy tests, 0 learner names, direct identifiers, credentials, or sensitive learner free-text values are present in language-model input or application logs.
- **SC-007**: At least 90% of account managers testing the primary workflow can identify the cohort's overall status and the highest-priority follow-up learner on their first review.
- **SC-008**: When interpretation is unavailable, 100% of valid packets still return validated factual measures or a clear processing-status explanation, with no fabricated interpretation or escalation alert.

## Assumptions

- The account manager is authorised to access the employer or cohort represented by the packet; authentication and organisation-level access control are outside this feature's initial scope.
- The JSON packet is a snapshot rather than a long-term system of record, and the feature does not import data directly from external learning, calendar, or employer systems.
- The packet may include fields such as learner name, product, recorded hours, meetings, workshops, and days since last meeting; unsupported fields are ignored and do not become evidence automatically.
- Each learner record may include non-negative `sessions_attended` and `assessments_submitted` counts, plus an optional `at_risk_flags` list of objects with required `code` and `severity` strings; missing values are distinct from zero and are reported as evidence limitations.
- At-risk flags are source-provided evidence and may trigger deterministic escalation rules; the AI may interpret them only after de-identification and must not invent new flags.
- When no source reference is provided, the learner name is used as the account-manager-facing reference and a derived non-identifying reference connects AI output to the source packet; the learner name remains excluded from language-model input.
- Intervention rules have product-defined defaults and may be adjusted per employer or cohort; account managers do not author or change rules during an individual review.
- Alert payload generation and the ability to support Slack, email, and future channel formats are in scope, but the exact formatted elements, channel presentation rules, and configuring or operating channel delivery, including recipients, authentication, scheduling, retries, and transmission, are outside this specification and will be defined during planning or a later delivery feature.
- The initial workflow is local; no hosted service, database, or background processing is required.
- Results are intended for prompt employer communication and human follow-up, not for automated learner ranking, disciplinary action, or employment decisions.
