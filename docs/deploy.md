# Deployment Guide

## 1. 前提
- Python 3.13
- AWS CLI 設定済み
- Lambda 実行ロール作成済み

## 2. 依存パッケージの準備
```bash
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## attenion

### インフラ初期セットアップ (初回のみ)

```
# 1. 信頼ポリシー（Lambdaがこのロールを使えるようにする設定）を作成
cat <<EOF > trust-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# 2. ロールを作成
aws iam create-role \
  --role-name fx-rate-lambda-role \
  --assume-role-policy-document file://trust-policy.json

# 3. ログ出力用の管理ポリシーをアタッチ
aws iam attach-role-policy \
  --role-name fx-rate-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# ロールの ARN を取得（変数に格納）
ROLE_ARN=$(aws iam get-role --role-name fx-rate-lambda-role --query 'Role.Arn' --output text)

# Lambda 関数を作成
aws lambda create-function \
  --function-name fx-rate-line-notify \
  --runtime python3.13 \
  --architectures arm64 \
  --handler src.lambda_function.lambda_handler \
  --role $ROLE_ARN \
  --zip-file fileb://package.zip

```


## 3. デプロイパッケージ作成
```bash
rm -rf build package.zip
mkdir -p build
python -m pip install \
    --platform manylinux2014_aarch64 \
    --target build \
    --implementation cp \
    --python-version 3.13 \
    --only-binary=:all: \
    -r requirements.txt
cp -R src build/
cd build && zip -r ../package.zip .
```

## 4. Lambda 更新
```bash
cd ..
aws lambda update-function-code \
  --function-name fx-rate-line-notify \
  --zip-file fileb://package.zip
```

## 5. 環境変数設定
- `EXCHANGE_RATE_API_KEY`
- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_TO_USER_ID`
- `LOG_LEVEL` (任意)

```bash
aws lambda update-function-configuration \
  --function-name <FUNCTION_NAME> \
  --environment 'Variables={EXCHANGE_RATE_API_KEY=xxx,LINE_CHANNEL_ACCESS_TOKEN=yyy,LINE_TO_USER_ID=zzz,LOG_LEVEL=INFO}'
```

## 6. EventBridge 設定
- [eventbridge-setup.md](eventbridge-setup.md) を参照
- `MaximumRetryAttempts=0` を確認
