# CloudWatch Log Insights Queries

## 1. 直近の失敗イベント
```sql
fields @timestamp, event_type, execution_id, reason, details
| filter level = "ERROR"
| sort @timestamp desc
| limit 50
```

## 2. 実行ID単位のトレース
```sql
fields @timestamp, level, event_type, execution_id, details
| filter execution_id = "<execution-id>"
| sort @timestamp asc
```

## 3. 為替取得失敗の集計
```sql
fields @timestamp, event_type, reason
| filter event_type = "rate_fetch" and level = "ERROR"
| stats count() as error_count by reason
| sort error_count desc
```

## 4. LINE送信失敗の集計
```sql
fields @timestamp, event_type, reason
| filter event_type = "line_push" and level = "ERROR"
| stats count() as error_count by reason
| sort error_count desc
```
