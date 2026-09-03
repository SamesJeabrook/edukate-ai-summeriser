# Research: Cohort Progress Summary and Escalation Alerts

## Decision: Use deterministic pre-processing before AI interpretation

- **Decision**: Parse, validate, normalise, aggregate progress measures, and apply intervention rules before constructing any model request.
- **Rationale**: Factual values and alert triggers must be reproducible, testable, and available even when the model is unavailable. It also limits the evidence sent to the model.
- **Alternatives considered**: Asking the model to calculate risk directly was rejected because it weakens traceability and makes numeric validation unreliable.

## Decision: Use an injectable AI service boundary

- **Decision**: Define a small provider protocol owned by the application and keep the official OpenAI SDK implementation behind it. The summariser accepts a provider instance, allowing a fake provider in tests and a future provider replacement.
- **Rationale**: This satisfies the constitution's official SDK requirement while preventing provider-specific calls from spreading through domain logic. Tests can run without credentials or network access.
- **Alternatives considered**: Calling the SDK from the CLI was rejected because it couples orchestration to one provider and makes privacy/failure tests harder. A generic hosted AI gateway was rejected because it adds infrastructure outside the prototype scope.

## Decision: Keep one canonical structured result and separate formatters

- **Decision**: Produce a canonical result containing facts, interpretation, evidence status, alerts, and metadata. Add formatter boundaries that consume this result; implement a readable baseline formatter and leave channel-specific presentation details for implementation planning.
- **Rationale**: Slack, email, and future channels can evolve independently without changing alert evidence or risk semantics. The canonical payload remains suitable for testing and integration handoff.
- **Alternatives considered**: Generating one final channel string was rejected because it prevents later formats from reusing structured evidence.

## Decision: Treat invalid packets as a hard validation failure

- **Decision**: Reject malformed, incomplete, type-invalid, duplicate-reference, and invalid-date packets before AI processing. Return field-specific, non-sensitive errors and no summary or escalation payload.
- **Rationale**: Prevents misleading employer communication and ensures invalid data never crosses the AI boundary.
- **Alternatives considered**: Silently coercing invalid values was rejected because it conflates missing, zero, and invalid evidence.

## Decision: Use derived non-identifying learner references for AI

- **Decision**: Keep the learner name available only in authorised account-manager-facing output. Derive a stable non-identifying reference from packet context and learner position/content for model input and traceability, without logging the source name.
- **Rationale**: Supports actionability for the account manager while meeting the privacy boundary.
- **Alternatives considered**: Sending names to the model was rejected by the constitution. Using packet position alone was rejected because reordering would break traceability.

## Decision: Configuration precedence is product default then employer/cohort override

- **Decision**: Represent intervention rules as named, versioned configuration with product defaults and optional employer/cohort overrides. No per-review rule authoring is included.
- **Rationale**: Provides predictable defaults and supports different programme expectations without changing the input packet.
- **Alternatives considered**: Fixed thresholds only were rejected because cohorts may have different expectations. Account-manager editing during review was rejected because it makes results harder to reproduce.

## Decision: Optional session and assessment counts preserve missing evidence

- **Decision**: Accept missing `sessions_attended` and `assessments_submitted` values, distinguish them from zero, and report their absence as an evidence limitation.
- **Rationale**: Source systems may not provide every progress measure. Treating missing values as zero would create false negative progress and misleading escalation decisions.
- **Alternatives considered**: Requiring both fields was rejected because it would exclude incomplete but otherwise useful packets. Defaulting missing values to zero was rejected because it changes the meaning of the source evidence.

## Decision: Source at-risk flags are rule inputs, not automatic alerts

- **Decision**: Preserve each source flag code and severity as factual evidence; create an escalation alert only when the flag matches a configured intervention rule.
- **Rationale**: This keeps the employer summary faithful to the source while allowing configurable alert sensitivity and avoiding unnecessary alert noise.
- **Alternatives considered**: Automatically alerting on every flag was rejected because source flags may be informational or already resolved. Alerting only high-severity flags was rejected because severity policy belongs in configurable intervention rules.

## Decision: Use standard-library-first local execution

- **Decision**: Use Python 3.12+, standard-library JSON/date handling, and `unittest`; add only the official OpenAI SDK for the real provider integration.
- **Rationale**: Matches the constitution's simplicity and clean-checkout requirements and keeps offline tests straightforward.
- **Alternatives considered**: A web framework, database, queue, or delivery SDK was rejected because none is required for this single-invocation CLI.
