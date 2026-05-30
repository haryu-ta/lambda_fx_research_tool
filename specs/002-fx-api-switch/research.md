# Research: FX API Switch to Open Exchange Rates

## Decision 1: 為替取得プロバイダーは Open Exchange Rates を採用
- Decision: 既存 ExchangeRate-API から Open Exchange Rates に切り替える。
- Rationale: 追加要件で更新頻度改善が求められており、要件で採用先が明示されているため。
- Alternatives considered:
  - ExchangeRate-API 継続: 現行の更新頻度要件に課題が残る。
  - 他無料API: 要件で Open Exchange Rates 指定のため採用しない。

## Decision 2: レスポンス変換は `rates.JPY` を正規化して既存モデルに合わせる
- Decision: Open Exchange Rates の `rates.JPY` を既存の `ExchangeRateSnapshot.rate` へマッピングする。
- Rationale: 通知ロジックと契約を維持しつつ、プロバイダー差分を取得層で吸収できる。
- Alternatives considered:
  - モデル全面変更: 影響範囲が広く、既存テスト・ログ契約を崩すリスクが高い。

## Decision 3: 失敗通知文言は既存契約を完全維持
- Decision: API切替後も失敗通知文言（為替API 実行NG、為替情報取得できず、為替情報取得NG）を変更しない。
- Rationale: 運用フローと監視手順の継続性を優先するため。
- Alternatives considered:
  - 文言の詳細化: 可読性は上がるが運用手順と監視条件の修正が必要になる。

## Decision 4: タイムアウト/スロットリング時は再試行せず失敗終了
- Decision: 既存方針どおり、スケジュール起動経路の自動再試行を無効のまま維持する。
- Rationale: 重複通知防止（FR-007）を優先し、失敗は通知とログで検知する。
- Alternatives considered:
  - 自動再試行有効化: 可用性改善の余地はあるが重複通知リスクが増す。

## Decision 5: 検証と観測は既存スタックを継続
- Decision: `pydantic` v2 と `aws-lambda-powertools` を継続利用する。
- Rationale: 憲章（Schema Validation / Observability）に準拠し、実装差分を最小化できる。
- Alternatives considered:
  - 独自検証・標準 logging: 一貫性が下がり、障害解析コストが上がる。
