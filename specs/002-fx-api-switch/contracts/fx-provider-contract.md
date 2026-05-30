# Contract: FX Provider Switch (Open Exchange Rates)

## Scope
本契約は、為替取得プロバイダーを Open Exchange Rates に切り替える際の
外部 API 入出力と、既存通知契約との整合条件を定義する。

## Inbound API Contract (Open Exchange Rates)
- Endpoint: `GET https://openexchangerates.org/api/latest.json`
- Query parameters:
  - `app_id`: `${OPEN_EXCHANGE_RATES_APP_KEY}`
  - `base`: `USD`（プラン都合で固定される場合はレスポンス値優先で検証）
  - `symbols`: `JPY`
- Success response (example):

```json
{
  "timestamp": 1717065600,
  "base": "USD",
  "rates": {
    "JPY": 150.25
  }
}
```

## Mapping Contract
- `base` -> `ExchangeRateSnapshot.base_currency`
- `rates.JPY` -> `ExchangeRateSnapshot.rate`
- `timestamp` -> `ExchangeRateSnapshot.provider_timestamp`
- HTTP status -> `ExchangeRateSnapshot.provider_status_code`

## Validation Contract
- `rates.JPY` が欠損または非数値の場合、`為替情報取得できず` を通知して失敗終了する。
- API エラー、タイムアウト、スロットリング時は `為替API　実行NG` を通知して失敗終了する。
- 認証情報未設定時は `為替情報取得NG` を通知して失敗終了する。

## Compatibility Contract
- EventBridge トリガー仕様は変更しない。
- LINE Push Message ペイロードと成功文言フォーマットは変更しない。
- スケジュール起動経路の自動再試行は無効のまま維持する。

## Success Message Contract
- Format (exact): `HH:MM時点\n１ドル = XXX.XX円`
