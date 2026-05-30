# Data Model: FX API Switch

## Entity: OpenExchangeRateResponse
- Purpose: Open Exchange Rates API の生レスポンス表現。
- Fields:
  - `disclaimer` (string, optional)
  - `license` (string, optional)
  - `timestamp` (integer, required)
  - `base` (string, required)
  - `rates` (object, required)
- Validation rules:
  - `base` は `USD` を期待する。
  - `rates.JPY` が存在し、数値であること。

## Entity: ExchangeRateSnapshot
- Purpose: 通知処理に利用する正規化済みの為替情報。
- Fields:
  - `base_currency` (string, required): `USD`
  - `target_currency` (string, required): `JPY`
  - `rate` (number, required): USD/JPY
  - `provider_timestamp` (datetime/string, optional): 取得元時刻
  - `provider_status_code` (integer, required): HTTP status
- Validation rules:
  - `rate` は正の数値。
  - `rate` 欠損や非数値はエラー通知フローへ遷移。

## Entity: NotificationMessage
- Purpose: LINE Push Message の論理モデル。
- Fields:
  - `message_type` (enum, required): `success` | `fx_api_ng` | `fx_data_unavailable` | `fx_info_ng`
  - `text` (string, required)
  - `display_time_hhmm` (string, required)
  - `to_user_id` (string, required)
- Validation rules:
  - 成功時文言は `HH:MM時点\n１ドル = XXX.XX円` に一致。
  - 失敗時文言は既存契約3種のいずれか。

## Entity: ExecutionLogRecord
- Purpose: 実行トレース用の構造化ログ。
- Fields:
  - `execution_id` (string, required)
  - `level` (enum, required): `INFO` | `ERROR`
  - `event_type` (string, required): `rate_fetch`, `line_push`, `validation_error`, `config_error`
  - `timestamp` (datetime, required)
  - `details` (object, optional)
- Validation rules:
  - `ERROR` ログは `details.reason` を含める。

## State Transitions
1. `scheduled` -> `fetching_rate`
2. `fetching_rate` -> `rate_ready` | `failed_fx_api` | `failed_rate_data`
3. `rate_ready` -> `sending_success_message`
4. `sending_success_message` -> `completed` | `failed_line_push`
5. `failed_fx_api` -> `sending_error_message(fx_api_ng)` -> `failed`
6. `failed_rate_data` -> `sending_error_message(fx_data_unavailable)` -> `failed`
7. `failed_config` -> `sending_error_message(fx_info_ng)` -> `failed`

Note: 自動再試行には遷移しない（重複通知防止）。
