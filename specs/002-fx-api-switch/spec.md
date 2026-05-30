# Feature Specification: 為替API切替

**Feature Branch**: `002-fx-line-notify`

**Created**: 2026-05-30

**Status**: Draft

**Input**: User description: "--file ./docs/requirements-002.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 高頻度更新レートを通知する (Priority: P1)

運用担当者として、更新頻度の高い為替APIからUSD/JPYを取得して通知したい。そうすることで、実運用で古い為替情報が届くリスクを下げられる。

**Why this priority**: 既存機能の価値は通知の鮮度に依存しており、API差し替えは最優先の改善であるため。

**Independent Test**: 定期実行を1回トリガーし、通知のレート値が新APIの同時点の値と一致することを確認すれば、このストーリー単体で価値を検証できる。

**Acceptance Scenarios**:

1. **Given** 新しい為替APIの認証情報が有効である, **When** スケジュール実行が開始される, **Then** USD/JPYを取得し「HH:MM時点\n１ドル = XXX.XX円」で通知する。
2. **Given** 取得した為替値が小数を含む, **When** 通知メッセージを生成する, **Then** 小数第2位で丸めた値が通知文に表示される。


### Edge Cases

- 新APIがHTTP 200を返しても、USD/JPYキーが欠落している場合は失敗通知として扱う。
- 新APIのレート値が数値以外で返却された場合は、通知送信前に検証エラーとして失敗させる。
- 新APIのレスポンス遅延でタイムアウトした場合は再試行せず、既存の障害通知契約に従って1回のみエラー通知を行う。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: システムは、USD/JPY取得元として Open Exchange Rates を利用しなければならない。
- **FR-002**: システムは、新APIから取得したレートを既存成功通知フォーマット「HH:MM時点\n１ドル = XXX.XX円」で配信しなければならない。
- **FR-003**: システムは、新API利用時も既存の失敗通知文言（為替API 実行NG、為替情報取得できず、為替情報取得NG）を維持しなければならない。
- **FR-004**: システムは、新APIレスポンスをJSONとして処理し、USD/JPYレートが数値であることを検証しなければならない。
- **FR-005**: システムは、新API障害時に構造化ERRORログを出力し、実行を失敗終了しなければならない。
- **FR-006**: システムは、EventBridge起動・LINE通知の既存インターフェースを変更してはならない。
- **FR-007**: システムは、切替後もスケジュール起動経路で自動再試行を有効化してはならない。

### Key Entities *(include if feature involves data)*

- **為替APIレスポンス**: Open Exchange Rates から取得するJSONデータ。取得時刻、通貨コード、USD/JPYのレート値を含む。
- **為替レートスナップショット**: 通知作成に利用する正規化済みレート情報。時刻、レート値、取得元状態を保持する。
- **通知メッセージ**: 成功または失敗の配信用テキスト。表示時刻と文言契約を含む。

## Success Criteria *(mandatory)*
- 成功通知の100%が文言フォーマット「HH:MM時点\n１ドル = XXX.XX円」に一致する
- 失敗実行の100%において、失敗理由を含む構造化ERRORログが記録される。

## Review Notes

- 既存通知契約（成功/失敗文言）との互換性を確認済み
- EventBridge および LINE 連携インターフェースが非変更であることを確認済み

## Assumptions

- Open Exchange Rates の無料プランで、現行の実行頻度に対して十分な利用枠がある。
- EventBridgeスケジュールとLINE通知経路は既存設定をそのまま利用できる。
- 追加機能はAPI差し替えが範囲であり、通知先の複数化やUI追加は対象外。
- 既存の監視クエリと運用フロー（CloudWatch確認手順）は継続利用する。
