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

## 3. デプロイパッケージ作成
```bash
rm -rf build package.zip
mkdir -p build
python -m pip install -r requirements.txt -t build
cp -R src/*.py build/
cd build && zip -r ../package.zip .
```

## 4. Lambda 更新
```bash
aws lambda update-function-code \
  --function-name <FUNCTION_NAME> \
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
