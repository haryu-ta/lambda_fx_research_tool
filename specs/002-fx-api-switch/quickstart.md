# Quickstart: FX API Switch to Open Exchange Rates

## 1. Prerequisites
- Python 3.13
- AWS CLI configured
- Existing Lambda function and EventBridge schedule
- LINE Messaging API channel
- Open Exchange Rates API key

## 2. Environment Variables
Lambda に以下を設定する。

- `EXCHANGE_RATE_API_KEY` (Open Exchange Rates の app_id)
- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_TO_USER_ID`
- `LOG_LEVEL` (optional)

## 3. Implementation Steps
1. `src/exchange_service.py` の API エンドポイントを Open Exchange Rates に変更する。
2. レスポンスの `rates.JPY` を既存 `ExchangeRateSnapshot` へマッピングする。
3. 既存の通知文言フォーマットを維持する（`src/line_service.py` は文言変更しない）。
4. 既存エラー分岐（API失敗、データ不正、認証不足）を維持する。

## 4. Test Steps
1. Unit tests: `tests/unit/test_exchange_service.py` を更新し、新レスポンス形式を検証する。
2. Integration tests: success/failure パスが既存文言契約を満たすことを確認する。
3. Execute:

```bash
.venv/bin/pytest -q
```

4. 最低確認ケース:
- 正常系: 成功通知が `HH:MM時点  1ドル = XXX.XX 円` である
- API障害: `為替API　実行NG` が送信される
- データ不正: `為替情報取得できず` が送信される

## 5. Deployment Verification
1. Lambda を更新して手動実行する。
2. 成功時: LINE に `HH:MM時点  1ドル = XXX.XX 円` が届くこと。
3. 失敗時: 既存3種のエラー通知文言が維持されること。
4. CloudWatch で `rate_fetch` / `line_push` の INFO/ERROR を確認する。

## 6. Operational Checks
- EventBridge timezone が `Asia/Tokyo`
- Retry policy が `MaximumRetryAttempts=0`
- 直近実行ログに `execution_id` が出力される
- `rate_fetch` ログの `provider` が `open_exchange_rates` である

## 7. Latest Validation Result
- Date: 2026-05-30
- Command: `.venv/bin/pytest -q`
- Result: `36 passed`
