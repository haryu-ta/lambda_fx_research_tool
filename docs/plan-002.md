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
- **為替レートAPI**: `Open Exchange Rates` (無料プランでも月1000回まで実行可能で、１時間に１回と情報更新頻度が高いため)。
  - エンドポイント: `https://openexchangerates.org/api/latest.json?app_id={APP_KEY}`


## 4. 認証情報（シークレット）の管理方針
AIがコードへ直接トークンを書き込むのを防ぐため、以下の環境変数設計とします。
Lambdaの「環境変数」から直接読み込む設定とします。（※より強固にする場合は AWS Secrets Manager も検討できますが、今回はミニマムスタートのため環境変数を採用）。

- `OPEN_EXCHANGE_RATES_APP_KEY`: 為替APIのAPPキー

## 5. モジュール・ディレクトリ構成
コードの肥大化を防ぎ、テストしやすくするために、以下のように役割を明確に分割します。
本改修は使用するAPIの差し替えのため、exchange_service.py の改修が中心になる。

```text
src/
├── lambda_function.py     # Lambdaエントリーポイント（イベント受付、全体のハンドリング）
├── exchange_service.py    # 為替レートAPIとの通信、Pydanticによるデータパース
├── line_service.py        # LINE APIへのメッセージ送信処理
└── config.py              # 環境変数の読み込みとバリデーション