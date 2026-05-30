# 開発要求書: 為替レートLINE通知システム

## 1. 概要
EventBridgeの時間起動（スケジュール）をトリガーとしてLambda関数を起動し、外部APIから最新の為替レート（USD/JPY）を取得して、LINEでユーザーに通知する。
基本的な機能はあるので基本はそれは改修しない。ただし、データ取得先の為替レートAPIを違うAPIに差し替える改修をしたい（現状使用しているものが情報の更新頻度が低いため）

## 2. システム連携要件
- **トリガー**: AWS EventBridge 
- **データ取得先**: 外部の為替レートAPI (無料プランがあるもの)
- **通知先**: LINE Messaging API

EventBridgeとLineは既存の機能があるので反抗ない

## 3. 機能要件
- 1ドルが何円か（例: 150.25円）を正確に取得すること。
- LINEに通知するメッセージは以下のフォーマットとする。
  「HH:MM時点\n１ドル = XXX.XX円」
  
## ４. 為替API仕様
- USD/JPY の為替レートを取得する
- 無料利用可能なAPIを使用する
- JSON形式でレスポンスを返すAPIを採用する
- Open Exchange Ratesを使用するように変更

## 5. 環境変数要件
- `OPEN_EXCHANGE_RATES_APP_KEY` を Open Exchange Rates の `app_id` として利用する
- `EXCHANGE_RATE_PROVIDER` は `open_exchange_rates` を使用する（既定値あり）
- `LINE_CHANNEL_ACCESS_TOKEN` / `LINE_TO_USER_ID` は既存どおり必須

