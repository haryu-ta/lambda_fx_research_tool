# Operational Runbook

## 1. 手動実行
```bash
aws lambda invoke --function-name <FUNCTION_NAME> out.json && cat out.json
```

## 2. 正常系チェック
- LINE に `HH:MM時点  1ドル = XXX.XX 円` が届く
- CloudWatch に `rate_fetch` と `line_push` の INFO が出る

## 3. 障害対応
### FX API 障害
- 通知文: `HH:MM時点  為替API　実行NG`
- `rate_fetch` の ERROR を確認

### 為替データ不正
- 通知文: `HH:MM時点  為替情報取得できず`
- `validation_error` の ERROR を確認

### 認証情報不足
- 通知文: `HH:MM時点  為替情報取得NG`
- `config_error` の ERROR を確認

### LINE 送信失敗
- 実行は失敗終了
- `line_push` の ERROR を確認

## 4. 監視チェックリスト
- EventBridge スケジュール有効
- Timezone が `Asia/Tokyo`
- Retry が 0
- 直近24時間の ERROR 件数
