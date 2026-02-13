---
name: spec-creation
description: Guide for creating specification documents in the docs/spec/ directory. Use this when asked to create new specifications or feature requirements following the Intent/Constraints/AC pattern.
license: MIT
---

# Specification Creation Skill

When creating a new specification document in `docs/spec/`, follow this structured approach:

## 1. Use the Template

Base your specification on `docs/spec/_template.md` which provides the standard structure:

```markdown
# 仕様（Spec）テンプレート

## 目的（Intent）
- [What is the goal? What problem does this solve?]

## 制約（Constraints）
- [What are the limitations, dependencies, or non-negotiable requirements?]

## 受け入れ条件（Acceptance Criteria / Outcomes）
- [ ] [Testable criteria that define when this is complete]

## Plan（家老が分解する観点）
- 足軽が並列に実行できる粒度に分ける
- 競合（同じファイル編集）が起きないように分担する

## タスクリスト（足軽へ配布する単位）
| task | assignee | input | output |
|---|---|---|---|
| | | | |
```

## 2. Key Principles

- **Intent**: State the purpose clearly in 1-3 sentences. What value does this deliver?
- **Constraints**: List technical, security, or operational limitations upfront
- **Acceptance Criteria (AC)**: Write testable conditions using checkboxes `- [ ]`
  - Each AC should be verifiable (pass/fail)
  - Format: "When X, then Y" or "Given X, when Y, then Z"
  - Include edge cases and error conditions
- **Plan**: Note how to decompose into parallel tasks (for Karo to implement)
- **Task List**: Initial task breakdown (Karo will refine this)

## 3. File Naming

Use descriptive kebab-case names:
- Good: `multi-agent-orchestration-v1.md`, `dashboard-automation-v2.md`
- Avoid: `spec1.md`, `new-feature.md`

## 4. Version Control

- Add version suffix for significant changes (e.g., `-v1`, `-v2`)
- Record design decisions in `docs/decisions.md`

## 5. Integration with Workflow

After creating the spec:
1. Update `status/dashboard.md` with the new spec and initial status
2. Have Karo (Reviewer/QA agent) decompose it into tasks
3. Have Shogun (Orchestrator) assign tasks to Ashigaru (Executor) agents

## Example

```markdown
# 仕様: Dashboard Auto-update

## 目的（Intent）

- 家老（Karo）が進捗を status/dashboard.md に手動で転記する作業を自動化し、足軽の報告YAML から自動更新する。

## 制約（Constraints）

- dashboard.md のフォーマット（Markdown table）を維持する
- Git操作は report_progress ツールに依存し、直接 git commit しない
- 既存の報告YAML（role/topic/status/outputs/summary）に変更を加えない

## 受け入れ条件（Acceptance Criteria / Outcomes）

- [ ] 足軽が報告YAMLを提出したとき、status/dashboard.md が自動更新される
- [ ] 更新後の dashboard.md が人間に読みやすい形式を維持している
- [ ] エラー時は家老に通知され、手動フォールバックが可能である

## Plan（家老が分解する観点）

- YAML parser の実装（足軽A）
- Dashboard updater の実装（足軽B）
- Error handling の実装（足軽C）
- テストケース作成（足軽D）

## タスクリスト（足軽へ配布する単位）

| task | assignee | input | output |
|---|---|---|---|
| YAML parser | ashigaru-1 | 報告YAML例 | parser.js |
| Dashboard updater | ashigaru-2 | parser.js | updater.js |
| Error handling | ashigaru-3 | updater.js | error-handler.js |
| Test cases | ashigaru-4 | 全実装 | test/ |
```

## Common Mistakes to Avoid

- ❌ Writing implementation details in Intent (keep it high-level)
- ❌ Vague AC like "works well" (make it testable)
- ❌ Mixing multiple features in one spec (split them)
- ❌ Forgetting to consider parallel task decomposition
