# Data Model: FX Rate LINE Notification

## Entity: ScheduleConfiguration
- Purpose: 定期実行条件を保持する実行設定モデル。
- Fields:
  - `cron_expression` (string, required): EventBridge cron 式。
  - `timezone` (string, required): `Asia/Tokyo` 固定。
  - `retry_enabled` (boolean, required): `false` 固定（重複配信防止）。
- Validation rules:
  - `timezone` は `Asia/Tokyo` のみ許可。
  - `retry_enabled` は `false` 以外を許可しない。

## Entity: ExchangeRateSnapshot
- Purpose: 為替 API 応答を正規化した取得結果モデル（生レスポンスをそのまま保持するモデルではない）。
- Fields:
  - `base_currency` (string, required): `USD`。
  - `target_currency` (string, required): `JPY`。
  - `rate` (number, required): USD/JPY レート。
  - `provider_timestamp` (datetime/string, optional): 提供元時刻。
  - `provider_status_code` (integer, required): HTTP ステータス。
- Validation rules:
  - `rate` は数値かつ正値。
  - `rate` が欠損/非数値の場合はエラー通知へ遷移。

### Raw Response Mapping (ExchangeRate-API Standard)
- Raw `base_code` -> `base_currency`
- Raw `conversion_rates.JPY` -> `rate`
- Raw `time_last_update_utc` (または `time_last_update_unix`) -> `provider_timestamp`
- HTTP status code -> `provider_status_code`

Note:
- `target_currency` は固定値 `JPY` としてアプリ側で補完する。
- Raw には `target_currency` / `provider_status_code` というキーは存在しない。

## Entity: NotificationMessage
- Purpose: LINE 送信用メッセージの論理モデル。
- Fields:
  - `message_type` (enum, required): `success` | `fx_api_ng` | `fx_data_unavailable` | `fx_info_ng`。
  - `text` (string, required): 表示文言。
  - `display_time_hhmm` (string, required): JST の `HH:MM`。
  - `to_user_id` (string, required): LINE 送信先ユーザーID。
- Validation rules:
  - `text` は仕様定義済み文言と一致。
  - `display_time_hhmm` は 24h フォーマット。

## Entity: ExecutionLogRecord
- Purpose: 実行結果を追跡する構造化ログイベント。
- Fields:
  - `execution_id` (string, required)
  - `level` (enum, required): `INFO` | `ERROR`
  - `event_type` (string, required): `rate_fetch`, `line_push`, `validation_error`, `config_error`
  - `timestamp` (datetime, required)
  - `details` (object, optional)
- Validation rules:
  - `ERROR` 時は `details.reason` を必須。

## State Transitions
1. `scheduled` -> `fetching_rate`
2. `fetching_rate` -> `rate_ready` | `failed_fx_api` | `failed_rate_data`
3. `rate_ready` -> `sending_success_message`
4. `sending_success_message` -> `completed` | `failed_line_push`
5. `failed_fx_api` -> `sending_error_message(fx_api_ng)` -> `failed`
6. `failed_rate_data` -> `sending_error_message(fx_data_unavailable)` -> `failed`
7. `failed_config` -> `sending_error_message(fx_info_ng)` -> `failed`

Note: 失敗時は再試行に遷移しない（FR-015）。
