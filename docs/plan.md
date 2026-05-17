# 技術計画書 (plan.md)

## 1. 実行環境 & ランタイム
- **ランタイム**: Python 3.13 (AWS Lambda 準拠)
- **デプロイ形式**: 依存ライブラリを含めた ZIP アーカイブ（または AWS Lambda レイヤーの活用）
- **アーキテクチャ**: `arm64` (コスト効率とパフォーマンス重視)

## 2. 外部ライブラリ・依存関係 (dependencies)
Python 3.13 の標準ライブラリ（`urllib.request` など）だけで組むことも可能ですが、開発効率と堅牢性を高めるために以下の構成を提案・採用します。

- **`requests`**: 為替APIおよびLINE APIとの通信用（標準の `urllib` より可読性が高いため）。
- **`aws-lambda-powertools`**: 憲法（CONSTITUTION）に従い、構造化ログ（JSON）とシームレスなロギングを実現するため。
- **`pydantic` (v2)**: 為替APIから返ってきたレスポンスデータの型安全なバリデーション用。
※ `boto3` はローカル開発環境（`requirements-dev.txt`）にのみ含め、Lambdaパッケージからは除外する。

## 3. 外部APIの選定と通信仕様
- **為替レートAPI**: `ExchangeRate-API` (無料プラン: 月1,500リクエストまで。今回の1日1回実行という要件に対して十分余裕があるため採用)。
  - エンドポイント: `https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD`
- **LINE通知**: `LINE Messaging API`（Push Message を用いて通知配信を行う。要件で定義した失敗時通知にも対応しやすいため採用）。
  - エンドポイント: `https://api.line.me/v2/bot/message/push`

## 4. 認証情報（シークレット）の管理方針
AIがコードへ直接トークンを書き込むのを防ぐため、以下の環境変数設計とします。
Lambdaの「環境変数」から直接読み込む設定とします。（※より強固にする場合は AWS Secrets Manager も検討できますが、今回はミニマムスタートのため環境変数を採用）。

- `EXCHANGE_RATE_API_KEY`: 為替APIのアクセスキー
- `LINE_CHANNEL_ACCESS_TOKEN`: LINE Messaging API のチャネルアクセストークン
- `LINE_TO_USER_ID`: 通知先ユーザーID（Push Message の送信先）

## 5. モジュール・ディレクトリ構成
コードの肥大化を防ぎ、テストしやすくするために、以下のように役割を明確に分割します。

```text
src/
├── lambda_function.py     # Lambdaエントリーポイント（イベント受付、全体のハンドリング）
├── exchange_service.py    # 為替レートAPIとの通信、Pydanticによるデータパース
├── line_service.py        # LINE APIへのメッセージ送信処理
└── config.py              # 環境変数の読み込みとバリデーション