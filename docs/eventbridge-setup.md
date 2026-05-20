# EventBridge Scheduler Setup (JST)

## 目的
Lambda を JST 基準で定期実行し、重複通知を防ぐため再試行を無効化します。

## 推奨 cron 設定
- Timezone: `Asia/Tokyo`
- 例: 毎日 09:00 JST
  - `cron(0 9 * * ? *)`

## AWS CLI 例
```bash
aws scheduler create-schedule \
  --name fx-rate-line-notify-daily \
  --schedule-expression "cron(0 9 * * ? *)" \
  --schedule-expression-timezone "Asia/Tokyo" \
  --flexible-time-window '{"Mode":"OFF"}' \
  --target '{
    "Arn":"<LAMBDA_ARN>",
    "RoleArn":"<SCHEDULER_ROLE_ARN>",
    "RetryPolicy":{"MaximumRetryAttempts":0}
  }'
```

## 重要設定
- `RetryPolicy.MaximumRetryAttempts=0`
- 失敗時の重複通知回避のため、再試行は有効化しない
