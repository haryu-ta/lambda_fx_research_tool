# Contract: Notification and Error Messaging

## Scope
本契約は、Lambda から LINE Messaging API Push Message を呼び出す際の
送信ペイロードとメッセージ文言ルールを定義する。

## Outbound API Contract (LINE Messaging API)
- Endpoint: `POST https://api.line.me/v2/bot/message/push`
- Headers:
  - `Authorization: Bearer ${LINE_CHANNEL_ACCESS_TOKEN}`
  - `Content-Type: application/json`
- Body schema:

```json
{
  "to": "<LINE_TO_USER_ID>",
  "messages": [
    {
      "type": "text",
      "text": "<message_text>"
    }
  ]
}
```

## Message Text Contract

### Success
- Pattern: `HH:MM時点  1ドル = XXX.XX 円`
- Example: `09:00時点  1ドル = 150.25 円`

### Error: FX API failure or throttling
- Exact text: `HH:MM時点  為替API　実行NG`

### Error: Invalid/missing USDJPY value in API response
- Exact text: `HH:MM時点  為替情報取得できず`

### Error: Missing/empty credentials
- Exact text: `HH:MM時点  為替情報取得NG`

## Failure Handling Contract
- LINE Push 呼び出し失敗時は ERROR ログを記録し、実行を失敗終了する。
- スケジュール起動経路では自動再実行を行わない（FR-015）。
- 失敗通知送信処理自体が失敗した場合も再試行しない。

## Validation Contract
- `HH:MM` は JST の 24 時間表記。
- 成功時レートは小数第2位まで。
- 仕様外文言は送信不可。
