# 仕様: AgentHQ 移行（Custom Agents / Subagents / Prompt Files / Handoffs）

## 目的（Intent）

Phillips/Cole/Barnes/Volkovaエージェント体制を、VS Code の最新 Custom Agents 機能（frontmatter: tools/agents/handoffs）+
Prompt Files + Subagents 機能を用いた正式なオーケストレーション基盤へ移行する。

これにより以下を実現する：

- Phillipsがオーケストレーターとして、Barnes・Coleをサブエージェントとして並列委任できる
- エージェント間の遷移を handoffs で明示化し、ワークフロー（Spec→Plan→Tasks→Run→Review→タスク管理）を再現可能にする
- よく使うワークフロー（仕様作成、タスク分解、レビュー依頼等）を Prompt Files（スラッシュコマンド）で標準化する
- 各エージェントが使えるツールを明示的に制限し、最小権限を強化する

## 制約（Constraints）

- 仕様駆動（Spec→Plan→Tasks→Run→タスク管理）のフローを維持する
- SOLID（SRP/DIP）を維持する
- 既存の運用ルール（ロギング契約、output/ 制約、ユーザ確認ゲート）を破壊しない
- 追加の実行エンジンは持たない（VS Code + Markdown 運用を維持）
- `.agent.md` / `.prompt.md` ファイルは `.github/agents/` および `.github/prompts/` に配置する（VS Code 標準）

## 受け入れ条件（Acceptance Criteria / Outcomes）

### Custom Agents（agent.md）

- [ ] `phillips.agent.md` が以下を満たす
  - `skills` にオーケストレーション関連のスキル（orchestration, specification-definition等）が定義される
  - `tools` に read/search/fetch/agent（サブエージェント起動）/edit が含まれる
  - `agents` に Barnes, Cole が指定される
  - `handoffs` に「Barnesへタスク分解を依頼」が定義される
  - 従来のプロンプト本文（仕様確定→タスク分割→並列委任→統合→検証→記録）が維持される
- [ ] `barnes.agent.md` が以下を満たす
  - `skills` にレビュー/QA関連のスキル（code-review, quality-assurance等）が定義される
  - `tools` にレビュー/QA に必要な read/search/edit/agent が含まれる
  - `agents` に Cole が指定される（Coleへ修正依頼を出せる）
  - `handoffs` に「Phillipsへ統合報告」「Coleへ修正指示」が定義される
  - 従来のプロンプト本文（レビュー観点、ロギング契約）が維持される
- [ ] `cole.agent.md` が以下を満たす
  - `skills` に実装関連のスキル（code-implementation, testing等）が定義される
  - `tools` に実装に必要な read/search/edit/run（ターミナル実行）が含まれる
  - `agents` は空配列 `[]`（Coleは他エージェントを起動しない: 最小権限）
  - `handoffs` に「Barnesへ結果報告」が定義される
  - 従来のプロンプト本文（最小権限、報告テンプレ）が維持される

### Prompt Files（prompt.md）

- [ ] `.github/prompts/` に以下の Prompt Files が存在する
  - `create-spec.prompt.md`: 新規仕様を作成するテンプレ
  - `decompose-tasks.prompt.md`: 仕様からタスク分解を行うテンプレ
  - `review-request.prompt.md`: Barnesにレビュー依頼するテンプレ
  - `report-done.prompt.md`: Coleの完了報告テンプレ
  - `escalate.prompt.md`: ユーザお伺いテンプレ

### ドキュメント

- [ ] `docs/ARCHITECTURE.md` に Custom Agents / Prompt Files / Handoffs の概要が追記される
- [ ] `docs/USAGE.md` に新しいエージェント切替・Prompt Files の使い方が追記される
- [ ] `docs/decisions.md` に本移行の判断が記録される
- [ ] `status/task.md` に移行の進捗が記録される

## Plan（Barnesが分解する観点）

- agent.md の変更は3ファイルとも独立（競合しない）
- prompt files は新規作成で既存に影響なし
- ドキュメント更新は docs/status 各ファイルが担当分離されている

## タスクリスト（Coleへ配布する単位）

| task | assignee | input | output |
|---|---|---|---|
| phillips.agent.md 更新 | Cole | 現行ファイル + 本スペック | `.github/agents/phillips.agent.md` |
| barnes.agent.md 更新 | Cole | 現行ファイル + 本スペック | `.github/agents/barnes.agent.md` |
| cole.agent.md 更新 | Cole | 現行ファイル + 本スペック | `.github/agents/cole.agent.md` |
| Prompt Files 作成 | Cole | 本スペック + USAGE.md テンプレ | `.github/prompts/*.prompt.md` |
| ARCHITECTURE.md 更新 | Cole | 現行ファイル + 本スペック | `docs/ARCHITECTURE.md` |
| USAGE.md 更新 | Cole | 現行ファイル + 本スペック | `docs/USAGE.md` |
| decisions.md 記録 | Cole | 本スペック | `docs/decisions.md` |
| タスク管理.md 更新 | Barnes | 全成果 | `status/task.md` |
| instructions 整合性確認 | Cole | `.github/instructions/*.instructions.md` | 更新パッチ（必要な場合のみ） |
