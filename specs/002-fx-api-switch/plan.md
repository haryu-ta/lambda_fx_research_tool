# Implementation Plan: 為替API切替

**Branch**: `002-fx-line-notify` | **Date**: 2026-05-30 | **Spec**: `/specs/002-fx-api-switch/spec.md`

**Input**: Feature specification from `/specs/002-fx-api-switch/spec.md`

## Summary

既存の EventBridge -> Lambda -> LINE の通知フローは維持し、為替取得プロバイダーのみを
Open Exchange Rates に差し替える。成功通知文言と失敗通知契約は既存仕様を維持し、
レスポンスのスキーマ差異を吸収する変換ロジックと検証を追加する。

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**:
- `requests` (外部 API 通信)
- `pydantic` v2 (レスポンス検証)
- `aws-lambda-powertools` (構造化ログ)

**Storage**: N/A（永続ストレージなし）

**Testing**: `pytest`（unit/integration）、`unittest.mock` による API モック

**Target Platform**: AWS Lambda (`arm64`) + Amazon EventBridge Scheduler + LINE Messaging API

**Project Type**: serverless backend（単一Lambdaサービス）

**Performance Goals**:
- 通常実行の 95% を 60 秒以内で完了
- 通知フォーマット契約一致率 100%

**Constraints**:
- 既存の通知文言契約を変更しない
- シークレットは環境変数のみ利用
- スケジュール起動経路の自動再試行を無効のまま維持

**Scale/Scope**:
- 初期リリースは通知先 1 宛先
- 本対応スコープは為替API差し替えと関連テスト/運用ドキュメント更新のみ

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gate Review

- ✅ I. Stateless Lambda Design: 処理は実行ごとに完結し、状態は保持しない。
- ✅ II. Single Responsibility per Handler: `lambda_handler` はオーケストレーションのみ、
  API 通信と整形は service 層へ分離する。
- ✅ III. Cold-Start and Dependency Discipline: 既存依存セットを維持し、追加依存を増やさない。
- ✅ IV. Schema Validation and Error Contract: Open Exchange Rates レスポンスを
  `pydantic` で検証し、既存エラー契約を維持する。
- ✅ V. Observability and Operability: 既存の構造化ログイベントを維持し、
  runbook/queries を更新して運用継続性を担保する。

Gate Status: **PASS**

## Project Structure

### Documentation (this feature)

```text
specs/002-fx-api-switch/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── fx-provider-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── config.py
├── exchange_service.py
├── lambda_function.py
├── line_service.py
├── logger.py
└── models.py

tests/
├── integration/
└── unit/

docs/
├── deploy.md
├── runbook.md
└── cloudwatch-queries.md
```

**Structure Decision**: 既存の単一 Lambda サービス構成を維持し、`src/exchange_service.py` を中心に
プロバイダー差し替えを実施する。テストは既存 unit/integration 構成に追加する。

## Post-Design Constitution Re-Check

- ✅ 原則 I-V に対する新規違反なし
- ✅ エラー文言契約は既存維持で後方互換性を確保
- ✅ quickstart/runbook 更新により運用手順の継続性を担保

Gate Status: **PASS**

## Complexity Tracking

現時点で憲章違反を伴う複雑化はなし。例外記録不要。
