<!--
Sync Impact Report
- Version change: template (unversioned) -> 1.0.0
- Modified principles:
	- [PRINCIPLE_1_NAME] -> I. Stateless Lambda Design
	- [PRINCIPLE_2_NAME] -> II. Single Responsibility per Handler
	- [PRINCIPLE_3_NAME] -> III. Cold-Start and Dependency Discipline
	- [PRINCIPLE_4_NAME] -> IV. Schema Validation and Error Contract
	- [PRINCIPLE_5_NAME] -> V. Observability and Operability
- Added sections:
	- Technical Standards
	- Development Workflow and Quality Gates
- Removed sections:
	- None
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md (generic Constitution Check remains compatible)
	- ✅ .specify/templates/spec-template.md (mandatory requirements/testing structure remains compatible)
	- ✅ .specify/templates/tasks-template.md (phase/task model remains compatible)
	- ⚠ pending .specify/templates/commands/*.md (directory not present in repository)
	- ✅ docs/CONSTITUTION.md (synchronized to this constitution)
- Follow-up TODOs:
	- None
-->

# Lambda FX Research Tool Constitution

## Core Principles

### I. Stateless Lambda Design
All Lambda handlers MUST remain stateless across invocations. Code MUST NOT persist
request-specific mutable state in module-level variables or process memory for reuse
across different requests. Durable or shared state MUST be stored in explicit external
systems (for example, DynamoDB, S3, or managed caches with clear boundaries).
Rationale: Stateless execution keeps behavior deterministic under horizontal scaling
and retry-driven invocation semantics.

### II. Single Responsibility per Handler
Each handler module MUST implement one bounded use case (one endpoint or one trigger
contract) and expose `lambda_handler(event, context)` as the entrypoint. Handlers MUST
coordinate input parsing, service invocation, and response mapping only; business rules
MUST live in dedicated modules such as `services/`, `domain/`, and `repositories/`.
Rationale: Tight boundaries improve testability, change safety, and operational clarity.

### III. Cold-Start and Dependency Discipline
Runtime MUST target Python 3.13. Dependency usage MUST be minimal and explicit.
`boto3` MUST NOT be packaged into deployment artifacts when provided by the Lambda
runtime, while local development dependencies MAY include it when needed. Initialization
costly objects SHOULD be created once per execution environment outside the handler,
and imports MUST avoid unused heavy libraries.
Rationale: Cold-start latency is a first-order availability and cost concern.

### IV. Schema Validation and Error Contract
Input and output contracts MUST be validated with `pydantic` v2 models at boundaries.
Handlers and services MUST return predictable error structures and MUST NOT leak raw
tracebacks or provider internals to callers. Contract changes MUST include explicit
versioning notes in specs and tasks.
Rationale: Strict schema and stable errors prevent integration breakage and reduce
incident recovery time.

### V. Observability and Operability
All production code paths MUST emit structured logs with correlation identifiers and
key domain events (start, success, failure, external dependency calls). Sensitive
information (secrets, personal data, tokens) MUST NOT be logged. Operational runbooks
or quickstart guidance MUST document how to reproduce, test, and troubleshoot flows.
Rationale: Strong observability is required for fast diagnosis in serverless systems.

## Technical Standards

- Runtime: Python 3.13.
- AWS SDK: Prefer runtime-provided `boto3` for deployment packages.
- Validation: `pydantic` v2 for request/response schema validation.
- Recommended source layout:
	- `src/handlers/` for Lambda entrypoints
	- `src/services/` for business orchestration
	- `src/repositories/` for external I/O
	- `src/utils/` for shared utilities

## Development Workflow and Quality Gates

- Specification-first: any new behavior MUST be captured in spec artifacts before
	implementation starts.
- Task traceability: implementation tasks MUST map to user stories or explicit
	cross-cutting requirements.
- Testing: unit or integration tests SHOULD be added for new logic; when omitted,
	the plan MUST document why omission is acceptable.
- Review gate: pull requests MUST include constitution compliance checks for the five
	core principles.

## Governance

This constitution is the highest-priority engineering policy for this repository.
If any lower-level document conflicts with it, this constitution takes precedence.

Amendment procedure:
1. Propose changes through a documented update to constitution text and impact.
2. Review the proposal against existing specs, plans, and task templates.
3. Approve and merge with synchronized updates to affected guidance documents.

Versioning policy:
- MAJOR: incompatible principle removals or redefinitions.
- MINOR: new principle/section or materially expanded mandatory guidance.
- PATCH: wording clarifications and non-semantic refinements.

Compliance review expectations:
- Every implementation plan MUST pass a Constitution Check before design/research.
- Every pull request MUST state compliance or justified exceptions.
- Exceptions MUST include rationale, risk, and a remediation timeline.

**Version**: 1.0.0 | **Ratified**: 2026-05-16 | **Last Amended**: 2026-05-16
