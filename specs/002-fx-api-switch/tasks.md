---
description: "Implementation task list for FX API switch to Open Exchange Rates"
---

# Tasks: FX API Switch

**Input**: Design documents from `/specs/002-fx-api-switch/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included (spec.md の User Scenarios & Testing 要件に基づき unit/integration を定義)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Parallelizable tasks (different files, no blocking dependency)
- **[Story]**: User story label (`[US1]`, `[US2]`, `[US3]`)
- **File path**: Exact target path in this repository

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: API切替の作業前提を整える

- [ ] T001 Open Exchange Rates 用の環境変数説明を更新 in docs/requirements-002.md
- [ ] T002 API切替方針と手順をREADMEに追記 in README.md
- [ ] T003 [P] 既存デプロイ手順に新API前提を反映 in docs/deploy.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 全ストーリーの前提となる共通基盤を整備

⚠️ **CRITICAL**: User story 実装前に完了必須

- [ ] T004 Open Exchange Rates 用設定検証を追加 in src/config.py
- [ ] T005 [P] OpenExchangeRateResponse モデルを追加 in src/models.py
- [ ] T006 [P] プロバイダ種別と変換ログ項目を追加 in src/logger.py
- [ ] T007 共通モック/fixtureを新API仕様に更新 in tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - 高頻度更新レートを通知する (Priority: P1) 🎯 MVP

**Goal**: Open Exchange Rates から USD/JPY を取得し既存成功文言で通知する

**Independent Test**: 1回の擬似スケジュール実行で、正常通知と代表的な失敗通知（API失敗/データ不正）を確認

### Tests for User Story 1

- [ ] T008 [P] [US1] Open Exchange Rates 正常レスポンスの単体テストを追加 in tests/unit/test_exchange_service.py
- [ ] T009 [P] [US1] レート丸めと成功文言の単体テストを更新 in tests/unit/test_line_service.py
- [ ] T010 [P] [US1] APIエラー/タイムアウト時の単体テストを追加 in tests/unit/test_exchange_service.py
- [ ] T011 [P] [US1] データ欠損・非数値時の単体テストを追加 in tests/unit/test_exchange_service.py
- [ ] T012 [US1] 成功経路の統合テストを新API仕様へ更新 in tests/integration/test_lambda_success_path.py
- [ ] T013 [P] [US1] API失敗経路の統合テストを新API仕様へ更新 in tests/integration/test_lambda_fx_api_failure.py
- [ ] T014 [P] [US1] データ不正経路の統合テストを新API仕様へ更新 in tests/integration/test_lambda_fx_data_invalid.py

### Implementation for User Story 1

- [ ] T015 [US1] Open Exchange Rates クライアント呼び出しを実装 in src/exchange_service.py
- [ ] T016 [US1] `rates.JPY` から ExchangeRateSnapshot への正規化処理を実装 in src/exchange_service.py
- [ ] T017 [US1] APIエラー/スロットリングの例外マッピングを実装 in src/exchange_service.py
- [ ] T018 [US1] 欠損・型不正の検証エラー処理を実装 in src/exchange_service.py
- [ ] T019 [US1] Lambdaの成功/失敗分岐連携を更新 in src/lambda_function.py
- [ ] T020 [US1] Quickstart の検証手順を更新 in specs/002-fx-api-switch/quickstart.md

**Checkpoint**: User Story 1 is independently functional and testable

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: 横断品質の最終仕上げ

- [ ] T021 [P] API切替の仕様整合レビューを反映 in specs/002-fx-api-switch/spec.md
- [ ] T022 [P] 計画・調査・クイックスタートの用語統一 in specs/002-fx-api-switch/plan.md
- [ ] T023 [P] 運用監視クエリを API切替観点で更新 in docs/cloudwatch-queries.md
- [ ] T024 [P] 障害時切り分けフローと設定確認項目を更新 in docs/runbook.md
- [ ] T025 フルテスト実行と結果記録 in specs/002-fx-api-switch/quickstart.md
- [ ] T026 変更セットをコミットしタグ候補を記録 in specs/002-fx-api-switch/tasks.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: 依存なしで着手可能
- **Phase 2 (Foundational)**: Phase 1 完了後。全 User Story のブロッカー
- **Phase 3 (User Story 1)**: Phase 2 完了後に実施
- **Phase 4 (Polish)**: User Story 1 完了後

### User Story Dependencies

- **US1 (P1)**: Foundational 完了後に着手可能（MVP）

### Within Each User Story

- テストタスクを先に作成し、失敗を確認してから実装
- 取得/モデル更新 -> ハンドラ連携 -> ドキュメント更新の順に実施

### Dependency Graph

- Setup -> Foundational -> US1 -> Polish

---

## Parallel Example: User Story 1

```bash
Task T008: tests/unit/test_exchange_service.py
Task T009: tests/unit/test_line_service.py
Task T010: tests/unit/test_exchange_service.py
Task T011: tests/unit/test_exchange_service.py
Task T013: tests/integration/test_lambda_fx_api_failure.py
Task T014: tests/integration/test_lambda_fx_data_invalid.py

Task T015/T016/T017/T018 が完了後に T019 を実施
```

---

## Implementation Strategy

### MVP First (US1)

1. Phase 1-2 を完了
2. US1 を完了
3. tests/unit/test_exchange_service.py と tests/integration/test_lambda_success_path.py で独立検証
4. MVP デモ/確認

### Incremental Delivery

1. US1: 正常通知と失敗通知契約を成立
2. Phase 4: 運用文書と監視観点を強化

### Parallel Team Strategy

- Developer A: src/exchange_service.py と関連 unit test
- Developer B: src/lambda_function.py と integration test
- Developer C: docs/runbook/deploy/eventbridge など運用文書

---

## Notes

- 各タスクは exact file path を含めている
- [P] はファイル競合が起きにくいものに限定
- User story tasks は全て [US1] を付与
- 実装時は既存通知文言契約を変更しないこと
