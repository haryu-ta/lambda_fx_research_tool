---
description: "Implementation task list for FX Rate LINE Notification"
---

# Tasks: FX Rate LINE Notification

**Input**: Design documents from `/specs/001-fx-line-notify/`

**Spec**: [spec.md](spec.md) (3 user stories, P1-P3)

**Plan**: [plan.md](plan.md) (Python 3.13, Lambda, EventBridge, LINE Messaging API, ExchangeRate-API)

**Tests**: Included per specification requirements (unit + integration)

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Parallelizable tasks (different files, no blocking dependencies)
- **[Story]**: User story label (US1, US2, US3)
- **File path**: Exact target location in repository

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan (src/, tests/unit, tests/integration directories)
- [ ] T002 Initialize Python 3.13 project with dependencies: requests, pydantic>=2.0, aws-lambda-powertools, pytest, pytest-mock
- [ ] T003 [P] Configure linting (ruff) and formatting (black) tools with pyproject.toml
- [ ] T004 [P] Create .env.example template with EXCHANGE_RATE_API_KEY, LINE_CHANNEL_ACCESS_TOKEN, LINE_TO_USER_ID placeholders

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

⚠️ **CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Implement src/config.py with environment variable validation (raise error on missing/empty keys)
- [ ] T006 [P] Define pydantic models in src/models.py: ScheduleConfiguration, ExchangeRateSnapshot, NotificationMessage, ExecutionLogRecord
- [ ] T007 [P] Configure aws-lambda-powertools Logger in src/logger.py with JSON structured logging and execution_id tracking
- [ ] T008 Setup test infrastructure: tests/__init__.py, conftest.py with pytest fixtures and mock utilities
- [ ] T009 Create src/lambda_function.py entry point skeleton with lambda_handler(event, context) signature

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 定期実行 USD/JPY 通知を受け取る (Priority: P1) 🎯 MVP

**Goal**: Users receive periodic USD/JPY rate notification in correct format via LINE

**Independent Test Criteria**: 
- Trigger scheduled execution → verify LINE receives `HH:MM時点  1ドル = XXX.XX 円` format
- Verify rate matches API response with 2 decimal places
- Verify INFO log records execution success

**Tests** (if requested): Implement test cases for success path

### Implementation Tasks

- [ ] T010 [US1] Implement src/exchange_service.py: ExchangeRateSnapshot model validation and error handling
- [ ] T011 [US1] Implement ExchangeRate-API client in src/exchange_service.py: fetch_rate() function with HTTP error handling
- [ ] T012 [US1] Implement src/line_service.py: NotificationMessage model and format_success_message(rate, timestamp) function
- [ ] T013 [US1] Implement LINE Messaging API client in src/line_service.py: send_push_message(message_text, user_id) function
- [ ] T014 [US1] Implement success path in src/lambda_function.py: fetch rate → format message → send to LINE → log SUCCESS
- [ ] T015 [US1] [P] Create tests/unit/test_exchange_service.py: Unit tests for rate fetching and ExchangeRateSnapshot validation
- [ ] T016 [US1] [P] Create tests/unit/test_line_service.py: Unit tests for message formatting and LINE API calls (mocked)
- [ ] T017 [US1] [P] Create tests/unit/test_config.py: Unit tests for environment variable validation
- [ ] T018 [US1] Create tests/integration/test_lambda_success_path.py: Integration test with mocked external APIs

---

## Phase 4: User Story 2 - 外部 API 障害時に安全運用できる (Priority: P2)

**Goal**: Operations team can clearly detect and respond to external service failures

**Independent Test Criteria**:
- FX API failure → verify LINE receives `HH:MM時点  為替API　実行NG` and ERROR log exists
- Invalid rate data → verify LINE receives `HH:MM時点  為替情報取得できず` and ERROR log exists  
- Missing credentials → verify LINE receives `HH:MM時点  為替情報取得NG` and ERROR log exists
- LINE Push failure → verify ERROR log exists and execution fails (no retry)

**Tests**: Implement test cases for all 4 failure paths

### Implementation Tasks

- [ ] T019 [US2] [P] Implement error handling in src/exchange_service.py: catch API errors, throttling, invalid response data
- [ ] T019B [US2] [P] Implement format_fx_api_error_message(timestamp) in src/line_service.py: `HH:MM時点  為替API　実行NG`
- [ ] T020 [US2] [P] Implement format_fx_data_unavailable_message(timestamp) in src/line_service.py: `HH:MM時点  為替情報取得できず`
- [ ] T021 [US2] [P] Implement format_fx_info_error_message(timestamp) in src/line_service.py: `HH:MM時点  為替情報取得NG`
- [ ] T022 [US2] [P] Add error handling in src/config.py: validate credentials exist and are non-empty; raise with clear error messages
- [ ] T023 [US2] Implement error paths in src/lambda_function.py: catch exceptions → send appropriate error message → log ERROR → fail execution
- [ ] T024 [US2] [P] Create tests/unit/test_error_messages.py: Unit tests for all error message formats
- [ ] T025 [US2] [P] Create tests/integration/test_lambda_fx_api_failure.py: Integration test for FX API error path (mocked failure)
- [ ] T026 [US2] [P] Create tests/integration/test_lambda_fx_data_invalid.py: Integration test for invalid rate data path
- [ ] T027 [US2] [P] Create tests/integration/test_lambda_line_failure.py: Integration test for LINE Push failure path
- [ ] T028 [US2] Create tests/integration/test_lambda_credentials_missing.py: Integration test for missing credentials path

---

## Phase 5: User Story 3 - JST 基準で実行時刻を制御できる (Priority: P3)

**Goal**: Operations can set cron schedule in JST timezone

**Independent Test Criteria**:
- Set EventBridge cron rule with JST timezone → verify execution triggers at intended JST time

**Tests**: Implement timezone control test

### Implementation Tasks

- [ ] T029 [US3] Create AWS EventBridge scheduler configuration template (cron + JST timezone) in docs/eventbridge-setup.md
- [ ] T030 [US3] Add validation of JST timezone in src/config.py: enforce `Asia/Tokyo` for schedule context
- [ ] T031 [US3] [P] Create tests/integration/test_lambda_timezone_jst.py: Integration test verifying JST timestamp in log records

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Observability, deployment readiness, operational documentation

### Observability & Logging

- [ ] T032 [P] Verify all INFO/ERROR logs include execution_id, timestamp, event_type, details per ExecutionLogRecord schema
- [ ] T033 [P] Add CloudWatch Log Insights query examples in docs/cloudwatch-queries.md for troubleshooting

### Deployment & Operations

- [ ] T034 Create src/requirements.txt with pinned dependency versions
- [ ] T035 Create deployment instructions in docs/deploy.md: packaging, Lambda layer setup, environment variables
- [ ] T036 [P] Create operational runbook in docs/runbook.md: manual trigger, failure response, monitoring checklist
- [ ] T037 [P] Verify retry policy: set EventBridge target Lambda retry = 0 (prevent duplicate notifications)

### Final Validation

- [ ] T038 Run full integration test suite: all 4 failure paths + success path pass
- [ ] T039 Validate message formats against contract: all message texts match exactly per contracts/notification-contract.md
- [ ] T040 Code review: check all secrets are environment variable sourced, no hardcoded keys
- [ ] T041 Commit all source code and documentation, create release tag

---

## Implementation Strategy

### MVP Scope (Phase 1 + 2 + 3)
**Minimum viable product**: Regular USD/JPY notifications delivered on schedule in correct format.
- Estimated completion: Phase 3 closes MVP
- Target: Users can receive daily rate updates; observability limited to success case

### Incremental Delivery
1. **Phase 1-2**: Foundation ready (estimated 2-3 tasks)
2. **Phase 3**: MVP complete - first working increment (estimated 8 tasks + tests)
3. **Phase 4**: Production-ready with failure handling (estimated 9 tasks + tests)
4. **Phase 5**: Operational flexibility via timezone control (estimated 3 tasks + tests)
5. **Phase 6**: Observability and deployment (estimated 10 tasks)

### Parallel Opportunities
- **Phase 1**: Tasks T002, T003, T004 can run in parallel (independent setup items)
- **Phase 2**: Tasks T006, T007, T008 can run in parallel (model definition, logger setup, test framework)
- **Phase 3**: Tasks T015, T016, T017, T018 can run in parallel (unit tests for independent modules)
- **Phase 4**: Tasks T019B, T020, T021, T022, T024, T025, T026, T027 can run in parallel (error handlers and tests for independent failure paths)
- **Phase 5**: Tasks T030, T031 can run in parallel (config validation and timezone test)
- **Phase 6**: Tasks T032, T033, T035, T036, T037 can run in parallel (docs and validation tasks)

### Dependencies
- No user story can begin until Phase 2 (Foundation) is complete
- US3 (timezone) depends on US1 (basic execution working first)
- All phases depend on Phase 1 (project structure)

---

## Validation Checklist

**Format Compliance**:
- [x] All tasks follow `- [ ] [ID] [P?] [Story?] Description` format
- [x] All tasks have unique IDs (T001–T041)
- [x] Parallelizable tasks marked with [P]
- [x] User story tasks marked with [US1], [US2], or [US3]
- [x] All file paths are exact and include `src/`, `tests/`, or `docs/` prefixes

**Coverage**:
- [x] Phase 1: Setup infrastructure
- [x] Phase 2: Blocking foundations (config, models, logger, tests, entry point)
- [x] Phase 3: US1 success path (fetch → format → send → log)
- [x] Phase 4: US2 error paths (4 failure scenarios)
- [x] Phase 5: US3 timezone control
- [x] Phase 6: Observability, deployment, documentation

**Completeness**:
- [x] Each user story can be implemented and tested independently
- [x] MVP scope identified (Phases 1-3)
- [x] Parallel execution opportunities identified
- [x] Dependencies clearly stated
- [x] Each task includes exact file path for implementation

---

## Notes

- **Retry Policy**: EventBridge must be configured with `retry_attempts = 0` to prevent duplicate notifications per FR-015 (research.md Decision 3)
- **Message Format**: All message texts must match contracts/notification-contract.md exactly (100% compliance per SC-004)
- **Error Notification Requirement**: Every error path must trigger a notification message to the user (FR-011 through FR-014)
- **Stateless Design**: No persistent state; each execution is independent per constitution
