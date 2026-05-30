# EventBridge Scheduler Setup (JST)

## 目的
Lambda を JST 基準で定期実行し、重複通知を防ぐため再試行を無効化します。

## 推奨 cron 設定
- Timezone: `Asia/Tokyo`
- 毎日 07:00 - 22:00 (1時間おき) JST
  - `cron(0 7-22 * * ? *)`

## 事前準備: Scheduler 用 IAM ロールの作成
Scheduler が Lambda を起動するために必要なロールを作成します。

```bash
# ロールの作成
aws iam create-role --role-name fx-rate-scheduler-role --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "scheduler.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}'

# 権限の付与 (Lambda呼び出し権限)
aws iam put-role-policy --role-name fx-rate-scheduler-role --policy-name LambdaInvokePolicy --policy-document '{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Action": "lambda:InvokeFunction", "Resource": "*"}]
}'

# ARNの取得
SCHEDULER_ROLE_ARN=$(aws iam get-role --role-name fx-rate-scheduler-role --query "Role.Arn" --output text)
LAMBDA_ARN=$(aws lambda get-function --function-name fx-rate-line-notify --query "Configuration.FunctionArn" --output text)
```

## AWS CLI 例
```bash
aws scheduler create-schedule \
  --name fx-rate-line-notify-hourly-daytime \
  --schedule-expression "cron(0 7-22 * * ? *)" \
  --schedule-expression-timezone "Asia/Tokyo" \
  --flexible-time-window '{"Mode":"OFF"}' \
  --target '{
    "Arn":"'$LAMBDA_ARN'",
    "RoleArn":"'$SCHEDULER_ROLE_ARN'",
    "RetryPolicy":{"MaximumRetryAttempts":0}
  }'
```

## 重要設定
- `RetryPolicy.MaximumRetryAttempts=0`
- 失敗時の重複通知回避のため、再試行は有効化しない

## 設定確認コマンド
```bash
aws scheduler get-schedule --name fx-rate-line-notify-hourly-daytime \
  --query '{Timezone:ScheduleExpressionTimezone,Retry:Target.RetryPolicy.MaximumRetryAttempts}'
```

期待値:
- `Timezone` が `Asia/Tokyo`
- `Retry` が `0`
