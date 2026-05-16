# プロジェクト憲法: Lambda FX Research Tool

この文書は、.specify/memory/constitution.md の運用向け要約です。
正式な規範は .specify/memory/constitution.md を参照します。

## 1. コア原則

### I. Stateless Lambda Design
- Lambda ハンドラーは invocation 間で状態を保持してはならない。
- 共有状態は DynamoDB/S3 などの明示的な外部ストアに置く。

### II. Single Responsibility per Handler
- 1 ハンドラーは 1 つのユースケースのみを担当する。
- エントリーポイントは `lambda_handler(event, context)` とする。
- ビジネスロジックは handlers ではなく services/domain/repositories に配置する。

### III. Cold-Start and Dependency Discipline
- Runtime は Python 3.13 を使用する。
- デプロイアーティファクトへ runtime 同梱の boto3 を重複同梱しない。
- 重い初期化は可能な限りハンドラー外で再利用する。

### IV. Schema Validation and Error Contract
- 入出力境界は pydantic v2 で検証する。
- エラー形式は予測可能な契約を維持し、内部情報を漏らさない。

### V. Observability and Operability
- 構造化ログと相関 ID を標準とする。
- 機密情報をログへ出力しない。

## 2. 技術標準
- Runtime: Python 3.13
- AWS SDK: boto3 は Lambda ランタイム提供を優先
- Validation: pydantic v2
- 推奨構成:
  - src/handlers/
  - src/services/
  - src/repositories/
  - src/utils/

## 3. 開発ワークフローと品質ゲート
- 実装前に仕様化を行う。
- タスクはユーザーストーリーまたは横断要件へトレース可能にする。
- PR では憲章準拠を明記し、例外は理由と是正期限を記録する。

## 4. ガバナンス
- 本憲章はこのリポジトリにおける最上位規範とする。
- 改訂は影響範囲の明示と関連文書の同時更新を要件とする。

**Version**: 1.0.0  
**Ratified**: 2026-05-16  
**Last Amended**: 2026-05-16
