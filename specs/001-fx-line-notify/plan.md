# Implementation Plan: FX Rate LINE Notification

**Branch**: `001-create-feature-branch` | **Date**: 2026-05-17 | **Spec**: `/specs/001-fx-line-notify/spec.md`

**Input**: Feature specification from `/specs/001-fx-line-notify/spec.md`

## Summary

EventBridge の定期実行で Lambda を起動し、ExchangeRate-API から USD/JPY を取得して
LINE Messaging API の Push Message で通知する。通常通知に加えて障害通知を明確化し、
重複配信防止のためスケジュール起動経路では自動再実行を無効化する。

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**:
- `requests` (外部 API 通信)
- `pydantic` v2 (レスポンス検証)
- `aws-lambda-powertools` (構造化ログ)

**Storage**: N/A（永続ストレージなし。状態は保持しない）

**Testing**: `pytest`（unit/integration）、`unittest.mock` で外部 API をスタブ化

**Target Platform**: AWS Lambda (`arm64`) + Amazon EventBridge Scheduler/Rule

**Project Type**: serverless backend (single Lambda service)

**Performance Goals**:
- 通常実行の 95% を 60 秒以内で完了
- 通知文面フォーマット一致率 100%

**Constraints**:
- シークレットは環境変数のみ（ハードコード禁止）
- 失敗時は構造化 ERROR ログを必須
- スケジュール起動経路で自動再実行を無効化（重複配信防止）

**Scale/Scope**:
- 初期リリースは通知先 1 宛先
- 実行頻度は日次想定（将来 cron 調整可）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gate Review

- ✅ Stateless Lambda Design: 永続状態を持たない方針。外部 API 取得と通知のみ。
- ✅ Single Responsibility per Handler: エントリポイントは `lambda_handler` に集約、
  ロジックは service 層へ分離する設計。
- ✅ Cold-Start and Dependency Discipline: Python 3.13、依存は最小セット、`boto3` を
  デプロイ同梱しない方針を維持。
- ✅ Schema Validation and Error Contract: `pydantic` v2 による入力/レスポンス検証、
  失敗系メッセージを仕様で固定。
- ✅ Observability and Operability: `aws-lambda-powertools` による構造化ログ前提。

Gate Status: **PASS**

## Project Structure

### Documentation (this feature)

```text
specs/001-fx-line-notify/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── notification-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── lambda_function.py
├── exchange_service.py
├── line_service.py
└── config.py

tests/
├── unit/
└── integration/
```

**Structure Decision**: 単一の Lambda サービス構成を採用。ハンドラーを薄く保ち、
外部通信とバリデーションを service/config へ分離する。

## Post-Design Constitution Re-Check

- ✅ 原則 1-5 に対する違反なし
- ✅ 失敗通知の契約を `contracts/notification-contract.md` に定義
- ✅ quickstart に運用確認手順を明記

Gate Status: **PASS**

## Complexity Tracking

現時点で憲章違反を伴う複雑化はなし。例外記録不要。
