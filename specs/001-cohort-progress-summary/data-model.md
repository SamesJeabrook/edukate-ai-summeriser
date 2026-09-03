# Data Model: Cohort Progress Summary and Escalation Alerts

## Progress Packet

The validated input snapshot for one employer or cohort.

| Field         | Type                             | Required | Validation                                                     |
| ------------- | -------------------------------- | -------: | -------------------------------------------------------------- |
| `employer_id` | integer or string identifier     |      Yes | Present, non-empty, and identifies one employer/cohort context |
| `learners`    | array of Learner Progress Record |      Yes | Non-empty; learner references are unique within the packet     |

Unknown top-level fields are ignored unless explicitly supported. The original packet is not persisted.

## Learner Progress Record

| Field                     | Type                          |                      Required | Validation / meaning                                                                 |
| ------------------------- | ----------------------------- | ----------------------------: | ------------------------------------------------------------------------------------ |
| `name`                    | string                        | Yes for current packet format | Account-manager-facing reference; never sent to AI                                   |
| `learner_id`              | string                        |                      Optional | Source reference when supplied; not required by the clarified name-based input model |
| `product`                 | string                        |                           Yes | Non-empty programme name                                                             |
| `sessions_attended`       | non-negative integer or null  |                            No | Missing means unavailable; zero is a valid measured value                            |
| `assessments_submitted`   | non-negative integer or null  |                            No | Missing means unavailable; zero is a valid measured value                            |
| `otj_hours`               | non-negative number or null   |                           Yes | Null means missing; zero is a valid measured value                                   |
| `meetings`                | array of activity records     |                           Yes | Empty array means no recorded meetings; wrong type is invalid                        |
| `workshops`               | array of activity records     |                           Yes | Empty array means no recorded workshops; wrong type is invalid                       |
| `days_since_last_meeting` | non-negative integer or null  |                           Yes | Null means unavailable; zero is valid                                                |
| `at_risk_flags`           | array of At-Risk Flag or null |                      Optional | Null means unavailable; an empty array means no supplied flags                       |
| supported activity fields | defined types                 |                      Optional | Unsupported fields do not become evidence automatically                              |

### At-Risk Flag

Each supplied flag is an object with a required non-empty `code` and `severity` string. The code identifies the source condition and the severity indicates the source assessment. Optional descriptive text is untrusted input, is not sent to the AI, and must not override processing instructions or output labels. Duplicate flag codes for one learner are invalid.

An activity record contains a valid, non-future `date_timestamp` and a non-empty activity name (`meeting_name` or `calendar_event_name`). Conflicting derived recency is marked unreliable.

## Deterministic Cohort Metrics

Computed from validated records before AI processing: learner count, sessions attended, assessments submitted, total and per-learner recorded hours, meeting count, workshop count, supplied at-risk-flag counts by code and severity, learners with no recorded activity, available last-contact recency, and evidence completeness/limitations.

## Intervention Rule and Evaluation

A named rule has a stable identifier, version, severity, condition, threshold, and recommended follow-up. Product defaults are selected first; employer/cohort overrides replace matching thresholds without changing packet shape. Rules evaluate only assessable evidence. A non-assessable rule produces an insufficient-evidence status, not a risk alert. Source-provided at-risk flags are treated as evidence and create alerts only when they match a configured rule.

## Escalation Alert

Contains `learner_reference`, optional authorised-facing `learner_name`, `severity`, `category`, `triggering_evidence`, `explanation`, `recommended_follow_up`, and `evidence_complete`. It includes human-review language and never represents an employment decision.

## Alert Payload

A canonical channel-neutral object containing cohort context, alert collection, factual evidence, labelled interpretation where available, evidence status, and generation metadata. Formatters can transform it for Slack, email, or future channels without reinterpreting evidence. Delivery settings and transmission are outside the model.

## Generation Metadata

Non-sensitive `generated_at`, configured `model`, model/provider status, input packet reference (such as a digest), rule configuration version, and output status. It must not contain learner names, raw free text, credentials, or the original packet.

## Result States

1. **Validated**: facts and applicable alerts are available; interpretation may be available or unavailable.
2. **Interpretation unavailable**: validated facts remain available and no fabricated interpretation is emitted.
3. **Rejected**: validation errors are returned; no summary, alert, or AI request is produced.
