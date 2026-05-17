# Research: FX Rate LINE Notification

## Decision 1: LINE通知方式は Messaging API Push Message を採用
- Decision: LINE Notify ではなく LINE Messaging API の Push Message を使用する。
- Rationale: 仕様（FR-011〜FR-014）で定義された障害通知の制御と将来拡張性に適合し、
  ユーザーID指定による明確な送信先管理が可能。
- Alternatives considered:
  - LINE Notify: 実装は簡易だが、機能拡張性と長期運用の観点で不利。

## Decision 2: 為替取得は ExchangeRate-API を採用
- Decision: ExchangeRate-API (`latest/USD`) を採用する。
- Rationale: 無料枠（1日1回運用に十分）と JSON レスポンスのシンプルさが要件に合致。
- Alternatives considered:
  - Open Exchange Rates: 利用可能だが、初期要件に対して追加設定が相対的に増える。

## Decision 3: 失敗時の再試行方針は「しない」を採用
- Decision: スケジュール起動経路で自動再実行を無効化し、重複配信リスクを回避する。
- Rationale: 送信タイムアウト境界での再実行は二重通知を引き起こすため、
  本機能では「欠損許容・重複禁止」を優先。
- Alternatives considered:
  - 自動再試行あり: 可用性は上がるが重複配信の制御が複雑化。

## Decision 4: バリデーションとログの実装方針
- Decision: `pydantic` v2 でレスポンス検証、`aws-lambda-powertools` で構造化ログを実施。
- Rationale: 憲章の Schema Validation / Observability 原則に準拠し、障害原因の追跡を容易化。
- Alternatives considered:
  - 手書きバリデーション + 標準logging: 実装量増加と品質ばらつきリスク。

## Decision 5: シークレット管理
- Decision: 環境変数 (`EXCHANGE_RATE_API_KEY`, `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_TO_USER_ID`) を採用。
- Rationale: 初期段階の運用負荷を抑えつつ、ハードコードを防止できる。
- Alternatives considered:
  - AWS Secrets Manager: セキュリティ強度は高いが初期構築コストが増える。
