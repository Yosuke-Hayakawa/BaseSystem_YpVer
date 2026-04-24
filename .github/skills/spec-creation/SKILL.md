---
name: spec-creation
description: docs/spec/ ディレクトリに仕様書を作成するためのガイド。Intent/Constraints/AC パターンに従った新規仕様や機能要件の作成時に使用します。
license: MIT
---

# 仕様作成スキル

`docs/spec/` に新しい仕様書を作成する際は、以下の構造化されたアプローチに従ってください：

## 1. テンプレートの使用

`docs/spec/_template.md` の標準構造を基に仕様を作成します：

```markdown
# 仕様（Spec）テンプレート

## 目的（Intent）
- [目標は何か？どんな問題を解決するか？]

## 制約（Constraints）
- [制限事項、依存関係、譲れない要件は何か？]

## 受け入れ条件（Acceptance Criteria / Outcomes）
- [ ] [完了を定義するテスト可能な基準]

## Plan（Barnesが分解する観点）
- Coleが並列に実行できる粒度に分ける
- 競合（同じファイル編集）が起きないように分担する

## タスクリスト（Coleへ配布する単位）
| task | assignee | input | output |
|---|---|---|---|
| | | | |
```

## 2. 重要な原則

- **Intent（目的）**: 1〜3文で目的を明確に記述。どんな価値を提供するか？
- **Constraints（制約）**: 技術的、セキュリティ、運用上の制限を最初に列挙
- **Acceptance Criteria（受け入れ条件/AC）**: チェックボックス `- [ ]` を使用してテスト可能な条件を記述
  - 各ACは検証可能（合格/不合格）であること
  - 形式: "X のとき、Y となる" または "X が与えられ、Y のとき、Z となる"
  - エッジケースとエラー条件を含める
- **Plan（計画）**: 並列タスクへの分解方法をメモ（Barnesが実装）
- **Task List（タスクリスト）**: 初期タスク分解（Barnesが洗練させる）

## 3. ファイル命名

説明的なケバブケース名を使用：
- 良い例: `multi-agent-orchestration-v1.md`, `タスク管理-automation-v2.md`
- 避ける: `spec1.md`, `new-feature.md`

## 4. バージョン管理

- 重大な変更にはバージョン接尾辞を追加（例: `-v1`, `-v2`）
- 設計判断は `docs/decisions.md` に記録

## 5. ワークフローとの統合

仕様作成後：
1. `status/task.md` に新規仕様と初期ステータスを更新
2. Barnes（レビュー/QA エージェント）にタスク分解を依頼
3. Phillips（Phillips）が Cole（実行エージェント）にタスクを割り当て

## 例

```markdown
# 仕様: タスク管理 Auto-update

## 目的（Intent）

- Barnes が進捗を status/task.md に手動で転記する作業を自動化し、Coleの報告YAML から自動更新する。

## 制約（Constraints）

- タスク管理.md のフォーマット（Markdown table）を維持する
- Git操作は report_progress ツールに依存し、直接 git commit しない
- 既存の報告YAML（role/topic/status/outputs/summary）に変更を加えない

## 受け入れ条件（Acceptance Criteria / Outcomes）

- [ ] Coleが報告YAMLを提出したとき、status/task.md が自動更新される
- [ ] 更新後の タスク管理.md が人間に読みやすい形式を維持している
- [ ] エラー時はBarnesに通知され、手動フォールバックが可能である

## Plan（Barnesが分解する観点）

- YAML parser の実装（Cole）
- タスク管理 updater の実装（Cole）
- Error handling の実装（Cole）
- テストケース作成（Cole）

## タスクリスト（Coleへ配布する単位）

| task | assignee | input | output |
|---|---|---|---|
| YAML parser | Cole | 報告YAML例 | parser.js |
| タスク管理 updater | Cole | parser.js | updater.js |
| Error handling | Cole | updater.js | error-handler.js |
| Test cases | Cole | 全実装 | test/ |
```

## 避けるべき一般的なミス

- ❌ Intent に実装詳細を書く（高レベルに保つ）
- ❌ 「うまく動く」のような曖昧なAC（テスト可能にする）
- ❌ 1つの仕様に複数の機能を混在させる（分割する）
- ❌ 並列タスク分解を考慮し忘れる
