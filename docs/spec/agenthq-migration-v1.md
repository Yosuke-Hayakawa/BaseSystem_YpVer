# 仕様: AgentHQ 移行（Custom Agents / Subagents / Prompt Files / Handoffs）

## 目的（Intent）

現行のRace Director/Pit Chief/Mechanicエージェント体制を、VS Code の最新 Custom Agents 機能（frontmatter: tools/agents/handoffs）+
Prompt Files + Subagents 機能を用いた正式なオーケストレーション基盤へ移行する。

これにより以下を実現する：

- Race Directorがオーケストレーターとして、Pit Chief・Mechanicをサブエージェントとして並列委任できる
- エージェント間の遷移を handoffs で明示化し、ワークフロー（Spec→Plan→Tasks→Run→Review→Dashboard）を再現可能にする
- よく使うワークフロー（仕様作成、タスク分解、レビュー依頼等）を Prompt Files（スラッシュコマンド）で標準化する
- 各エージェントが使えるツールを明示的に制限し、最小権限を強化する

## 制約（Constraints）

- 仕様駆動（Spec→Plan→Tasks→Run→Dashboard）のフローを維持する
- SOLID（SRP/DIP）を維持する
- 既存の運用ルール（ロギング契約、output/ 制約、上様確認ゲート）を破壊しない
- 追加の実行エンジンは持たない（VS Code + Markdown 運用を維持）
- `.agent.md` / `.prompt.md` ファイルは `.github/agents/` および `.github/prompts/` に配置する（VS Code 標準）

## 受け入れ条件（Acceptance Criteria / Outcomes）

### Custom Agents（agent.md）

- [ ] `race-director.agent.md` が以下を満たす
  - `skills` にオーケストレーション関連のスキル（orchestration, specification-definition等）が定義される
  - `tools` に read/search/fetch/agent（サブエージェント起動）/edit が含まれる
  - `agents` に Pit Chief, Mechanic が指定される
  - `handoffs` に「Pit Chiefへタスク分解を依頼」が定義される
  - 従来のプロンプト本文（仕様確定→タスク分割→並列委任→統合→検証→記録）が維持される
- [ ] `pit-chief.agent.md` が以下を満たす
  - `skills` にレビュー/QA関連のスキル（code-review, quality-assurance等）が定義される
  - `tools` にレビュー/QA に必要な read/search/edit/agent が含まれる
  - `agents` に Mechanic が指定される（Mechanicへ修正依頼を出せる）
  - `handoffs` に「Race Directorへ統合報告」「Mechanicへ修正指示」が定義される
  - 従来のプロンプト本文（レビュー観点、ロギング契約）が維持される
- [ ] `mechanic.agent.md` が以下を満たす
  - `skills` に実装関連のスキル（code-implementation, testing等）が定義される
  - `tools` に実装に必要な read/search/edit/run（ターミナル実行）が含まれる
  - `agents` は空配列 `[]`（Mechanicは他エージェントを起動しない: 最小権限）
  - `handoffs` に「Pit Chiefへ結果報告」が定義される
  - 従来のプロンプト本文（最小権限、報告テンプレ）が維持される

### Prompt Files（prompt.md）

- [ ] `.github/prompts/` に以下の Prompt Files が存在する
  - `create-spec.prompt.md`: 新規仕様を作成するテンプレ
  - `decompose-tasks.prompt.md`: 仕様からタスク分解を行うテンプレ
  - `review-request.prompt.md`: Pit Chiefにレビュー依頼するテンプレ
  - `report-done.prompt.md`: Mechanicの完了報告テンプレ
  - `escalate.prompt.md`: 上様お伺いテンプレ

### ドキュメント

- [ ] `docs/ARCHITECTURE.md` に Custom Agents / Prompt Files / Handoffs の概要が追記される
- [ ] `docs/USAGE.md` に新しいエージェント切替・Prompt Files の使い方が追記される
- [ ] `docs/decisions.md` に本移行の判断が記録される
- [ ] `status/dashboard.md` に移行の進捗が記録される

## Plan（Pit Chiefが分解する観点）

- agent.md の変更は3ファイルとも独立（競合しない）
- prompt files は新規作成で既存に影響なし
- ドキュメント更新は docs/status 各ファイルが担当分離されている

## タスクリスト（Mechanicへ配布する単位）

| task | assignee | input | output |
|---|---|---|---|
| race-director.agent.md 更新 | mechanic-1 | 現行ファイル + 本Spec | `.github/agents/race-director.agent.md` |
| pit-chief.agent.md 更新 | mechanic-2 | 現行ファイル + 本Spec | `.github/agents/pit-chief.agent.md` |
| mechanic.agent.md 更新 | mechanic-3 | 現行ファイル + 本Spec | `.github/agents/mechanic.agent.md` |
| Prompt Files 作成 | mechanic-4 | 本Spec + USAGE.md テンプレ | `.github/prompts/*.prompt.md` |
| ARCHITECTURE.md 更新 | mechanic-5 | 現行ファイル + 本Spec | `docs/ARCHITECTURE.md` |
| USAGE.md 更新 | mechanic-6 | 現行ファイル + 本Spec | `docs/USAGE.md` |
| decisions.md 記録 | mechanic-7 | 本Spec | `docs/decisions.md` |
| dashboard.md 更新 | pit-chief | 全成果 | `status/dashboard.md` |
| instructions 整合性確認 | mechanic-8 | `.github/instructions/*.instructions.md` | 更新パッチ（必要な場合のみ） |
