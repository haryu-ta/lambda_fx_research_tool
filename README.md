# セットアップ
```
uvx --from git+https://github.com/github/spec-kit.git specify init lambda_fx_reseatch_tool
```

# SpecKitの手順
## 憲法の定義
```
# Copilot　Chatにて実行すること
/speckit.constitution --file ./docs/CONSTITUTION.md
```

## 要件の定義

```
# Copilot　Chatにて実行すること
/speckit.specify --file ./docs/requirements.md
```

## 要件の精緻化

```
# Copilot　Chatにて実行すること
/speckit.clarify パフォーマンス面を精緻化する
```


## 技術計画の作成

```
# Copilot　Chatにて実行すること
/speckit.plan --file ./docs/plan.md
```

## 要件の検証

```
# Copilot　Chatにて実行すること
/speckit.checklist
```

### 作成物

- data-model.md
  - データモデル定義
  - システム内で飛び交うデータの「形（スキーマ）」を厳密に定義したファイルです。
- plan.md
  - 技術計画書
  - 全体のアーキテクチャや、ソースコードをどう分割するか（ディレクトリ構造）をまとめたファイルです。
- quickstart.md
  - 開発・起動ガイド
  - このプロジェクトをローカル環境でどうやってセットアップし、どうやってテストやデプロイを実行すればいいかの「手順書」です。
- research.md
  - 技術調査・検証ログ
  - AIが設計を決めるにあたって、「本当にこの方法で実現可能か？」を裏付け調査した内容の記録です。

## タスク生成

```
# Copilot　Chatにて実行すること
/speckit.tasks
```

## 実装

```
# Copilot　Chatにて実行すること
/speckit.implement
```