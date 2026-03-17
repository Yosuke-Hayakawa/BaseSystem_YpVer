---
name: create-spec
description: "新規仕様（Spec）を docs/spec/ に作成する。目的/制約/受け入れ条件を構造化する。"
agent: "Race Director (Orchestrator)"
tools:
  - read
  - search
  - editFiles
---

以下の手順で新規仕様を作成してください。

1. `docs/spec/_template.md` を読み込む
2. ユーザーの指示（目的/背景）を元に、テンプレートに従って仕様を構造化する
3. `docs/spec/<topic>.md` として保存する

必須セクション：

- **目的（Intent）**: 何を達成するか（1-2行）
- **制約（Constraints）**: 守るべきルール（仕様駆動、SOLID、既存運用維持 等）
- **受け入れ条件（AC）**: テスト可能な条件を箇条書き（入力/条件→期待結果）
- **Plan**: Pit Chiefがタスク分解する際の観点
- **タスクリスト**: Mechanicへ配布する単位（task / assignee / input / output）

注意：
- ACは具体的・検証可能に
- 仕様が曖昧な場合はユーザー（上様）に質問して確定させる
- 作成後は `status/dashboard.md` への記録をPit Chiefに依頼する
