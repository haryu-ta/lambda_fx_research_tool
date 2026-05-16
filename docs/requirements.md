# 開発要求書: 為替レートLINE通知システム

## 1. 概要
EventBridgeの時間起動（スケジュール）をトリガーとしてLambda関数を起動し、外部APIから最新の為替レート（USD/JPY）を取得して、LINEでユーザーに通知する。

## 2. システム連携要件
- **トリガー**: AWS EventBridge 
- **データ取得先**: 外部の為替レートAPI (無料プランがあるもの)
- **通知先**: LINE Messaging API

## 3. 機能要件
- 1ドルが何円か（例: 150.25円）を正確に取得すること。
- LINEに通知するメッセージは以下のフォーマットとする。
  「HH:MM時点  1ドル = XXX.XX 円」

## 4. 非機能・エラー要件
- 為替APIやLINE APIの呼び出しでエラーが発生した場合、CloudWatchに構造化ログ（Errorレベル）を出力し、Lambdaを異常終了（Exceptionをスロー）させること。
- APIキーやトークンなどの機密情報はコードにハードコードせず、環境変数から読み込む設計にすること。
  
## 5. 実行タイミング要件
- EventBridge により定期実行する
- スケジュールは cron 式で設定可能とする
- タイムゾーンは JST とする
  
## 6. 為替API仕様
- USD/JPY の為替レートを取得する
- 無料利用可能なAPIを使用する
- JSON形式でレスポンスを返すAPIを採用する
- API候補:
  - ExchangeRate-API
  - Open Exchange Rates

## 7. LINE通知仕様
- LINE Messaging API の Push Message を利用する
- 通知対象ユーザーIDは環境変数で管理する
- 通知メッセージはテキスト形式とする
 
## 8. ログ要件
- CloudWatch Logs にJSON形式で出力する
- INFO / ERROR レベルを使い分ける
- 以下の情報を含める
  - 実行時刻
  - APIレスポンスステータス
  - エラー内容