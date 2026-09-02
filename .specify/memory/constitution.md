<!--
Sync Impact Report
- Version change: not established -> 1.0.0
- Modified principles: scaffold placeholders -> Python Simplicity and Clarity;
	scaffold placeholders -> Evidence-Led Human Decision Support; scaffold
	placeholders -> Privacy and Data Minimisation; scaffold placeholders -> Secure
	and Trustworthy AI Integration; scaffold placeholders -> Traceability and
	Quality Gates
- Added sections: Technical and Compliance Constraints; Development Workflow and
	Quality Gates
- Removed sections: none
- Follow-up TODOs: TODO(RATIFICATION_DATE): confirm the project's original
	constitution adoption date.
-->

# Edukate Progress Summariser Constitution

## Core Principles

### I. Python Simplicity and Clarity

The project MUST support Python 3.12 or later and follow the principles of PEP 20:
explicit, readable, simple, and unsurprising code is preferred. New dependencies,
frameworks, services, and infrastructure MUST be avoided unless the prototype
requires them; each external dependency MUST have a documented, clear justification.
The rationale is to keep local execution reliable, understandable, and maintainable.

### II. Evidence-Led Human Decision Support

Generated summaries MUST support human decision-making and MUST NOT replace professional
or organisational judgement. Every summary MUST distinguish factual learner data from
AI-generated interpretation, identify AI-generated content clearly, and state when the
available evidence is insufficient. The OpenAI model or version MUST be configurable
through application configuration, and the selected configuration MUST be recorded in
generation metadata. The rationale is to make interpretation reviewable and prevent
unsupported automation from being treated as fact.

### III. Privacy and Data Minimisation

Learner data MUST be treated as sensitive educational data. The system MUST follow UK
GDPR principles, send only the minimum data required to the AI, and MUST NOT send
personally identifiable learner data to the AI. Learner data MUST NOT be exposed between
users or organisations, and sensitive learner information MUST NOT be written to logs.
Access, retention, and sharing MUST default to the most restrictive practical setting.
The rationale is to reduce privacy risk while preserving the minimum evidence needed for
a useful summary.

### IV. Secure and Trustworthy AI Integration

The implementation MUST use the official OpenAI SDK and MUST keep API keys and all
credentials on the server or in the local trusted runtime; credentials MUST never be
exposed to a client. Security MUST be enabled by default. All learner-generated content
MUST be treated as untrusted input, and prompts and processing MUST include appropriate
safeguards against prompt injection and malicious content. The rationale is to keep the
AI boundary controlled even when input is adversarial.

### V. Traceability and Quality Gates

The system MUST record sufficient non-sensitive metadata to explain how each summary was
generated, including the configured model version and a traceable reference to the
learner-data evidence used. Traceability references MUST avoid reproducing sensitive
learner content. Changes affecting data handling, AI prompts, model configuration,
summary labelling, or evidence interpretation MUST include focused tests or an explicit
documented reason why testing is not practical. The rationale is to make outputs
auditable without creating a second store of learner information.

## Technical and Compliance Constraints

The prototype MUST run locally from a clean checkout using documented Python 3.12+
setup steps. It MUST use the smallest practical technology stack and MUST NOT introduce
a web framework, hosted service, database, queue, or other infrastructure unless a
specific requirement demonstrates that it is necessary. OpenAI integration MUST be
isolated behind a clear application boundary so the application can be run and tested
without sending real learner data. Configuration MUST support selecting the AI model or
version without code changes, and production credentials MUST be supplied through a
trusted configuration mechanism rather than committed files.

## Development Workflow and Quality Gates

Every change MUST be checked against this constitution before review. Tests MUST cover
the minimum-data boundary, factual-versus-interpretive labelling, insufficient-evidence
behaviour, credential isolation, prompt-injection handling, and traceability metadata
whenever those behaviours are changed. Reviews MUST verify that logs and generated
outputs do not disclose sensitive learner data and that AI output remains clearly
identified. A clean-checkout local run MUST be verified for changes to setup,
configuration, or runtime dependencies.

## Governance

<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution is the highest-level project governance document. An amendment MUST
identify the affected principles, explain its rationale, update the Sync Impact Report,
and include any required migration or follow-up work. Amendments require review by the
project owner and MUST pass the applicable quality gates before adoption.

The constitution uses semantic versioning. A MAJOR version is required for incompatible
governance changes or removal/redefinition of a principle. A MINOR version is required
for a new principle, section, or material expansion of guidance. A PATCH version is
required for clarifications, wording, or other non-semantic refinements. Each review
MUST verify compliance with the current version, UK GDPR obligations, data minimisation,
credential handling, and AI-output safeguards.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm original adoption date | **Last Amended**: 2026-09-02
