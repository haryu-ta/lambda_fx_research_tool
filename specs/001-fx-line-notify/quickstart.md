# Quickstart: FX Rate LINE Notification

## 1. Prerequisites
- Python 3.13
- AWS アカウント（Lambda + EventBridge）
- LINE Messaging API チャネル
- ExchangeRate-API キー

## 2. Environment Variables
Lambda に以下を設定する。

- `EXCHANGE_RATE_API_KEY`
- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_TO_USER_ID`

## 3. Deploy Skeleton
1. `src/lambda_function.py` をエントリポイントとして実装。
2. `src/exchange_service.py` で為替取得と `pydantic` 検証を実装。
3. `src/line_service.py` で Push Message 送信処理を実装。
4. `src/config.py` で環境変数検証（未設定/空文字をエラー化）を実装。

## 4. Schedule Setup
- EventBridge で cron ルールを作成。
- タイムゾーンを JST (`Asia/Tokyo`) に設定。
- ターゲット Lambda の再試行ポリシーは無効化（retry 0）に設定。

## 5. Manual Verification
### Success path
1. テスト実行をトリガー。
2. LINE に `HH:MM時点  1ドル = XXX.XX 円` が届くことを確認。
3. CloudWatch に INFO ログが出ることを確認。

### Failure path: FX API unavailable
1. API キーを無効値へ変更して実行。
2. LINE に `HH:MM時点  為替API　実行NG` が届くことを確認。
3. CloudWatch に ERROR ログが出ることを確認。

### Failure path: invalid rate payload
1. API 応答をモックして rate 欠損を再現。
2. LINE に `HH:MM時点  為替情報取得できず` が届くことを確認。

### Failure path: missing credentials
1. `LINE_CHANNEL_ACCESS_TOKEN` または `LINE_TO_USER_ID` を空にして実行。
2. LINE に `HH:MM時点  為替情報取得NG` が届くことを確認。

## 6. Observability Checks
- 全実行で `execution_id` をログ出力。
- ERROR ログに失敗理由と失敗連携先を含める。
- 重複配信が発生していないことを運用ログで確認する。
