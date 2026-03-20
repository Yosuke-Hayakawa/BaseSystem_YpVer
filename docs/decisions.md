# 設計判断ログ（decisions）

このファイルは、**各プロジェクト**で「なぜその設計にしたか」を短く残すためのログ（テンプレート）です。

- このテンプレートリポジトリ自身の履歴は `docs/history.md` で管理します。

## 記載ルール（推奨）

- いつ：YYYY-MM-DD
- 何を：判断内容
- なぜ：理由
- 代替案：検討した選択肢
- 反映先：変更したファイル/ディレクトリ
- 影響：利用者/運用/互換性への影響

---

## テンプレ: Decision

- いつ：YYYY-MM-DD
- 何を：
- なぜ：
- 代替案：
- 反映先：
- 影響：

## テンプレ: Kaizen Decision（運用改善の採用判断）

- いつ：YYYY-MM-DD
- 何を：改善点（ナレッジ/手順/テンプレ/ルール変更）
- なぜ：背景・痛み・期待効果
- 代替案：採用しない場合/別案
- 反映先：`docs/spec/` / `docs/USAGE.md` / `.github/instructions/` / `.vscode/tasks.json` など
- 影響：利用者/運用への影響、移行の注意

---

## 2026-03-20: Persona / Role 分離アーキテクチャの採用

- いつ：2026-03-20
- 何を：エージェントの「名前・口調（Persona）」と「ロールロジック（Role）」を分離。`persona.md` 1ファイルでテーマを切り替え可能にした。
- なぜ：チームによってネーミングや口調を変えたいが、アウトプットの品質（ロジック）は変えたくないというニーズに対応するため。従来は名前変更に約15ファイルの編集が必要だった。
- 代替案：各 instructions ファイルに直接テーマ分岐を書く（→ ロジックとペルソナが混在するため却下）
- 反映先：
  - 新規: `.github/persona.md`（唯一の変更点）
  - 新規: `.github/instructions/persona.instructions.md`（全エージェント共通・applyTo: "**"）
  - 変更: `.github/instructions/orchestrator.instructions.md`（Tier-1ロールIDに変更・ペルソナ記述を削除）
  - 変更: `.github/instructions/coordinator.instructions.md`（Tier-2ロールIDに変更・ペルソナ記述を削除）
  - 変更: `.github/instructions/worker.instructions.md`（Tier-3ロールIDに変更・ペルソナ記述を削除）
  - 変更: `.github/agents/orchestrator.agent.md`（name: "Orchestrator (Tier-1)"、handoffs更新）
  - 変更: `.github/agents/coordinator.agent.md`（name: "Coordinator (Tier-2)"、handoffs更新）
  - 変更: `.github/agents/worker.agent.md`（name: "Worker (Tier-3)"、handoffs更新）
  - 更新: `.github/copilot-instructions.md`（テーブルをロールIDベースに更新）
- 影響：
  - テーマ切り替え時の作業が「persona.md + agent.md×3の name: フィールド」だけに集約される
  - ロジック（判断・報告・権限）は一切変わらないためアウトプット品質は保たれる
  - 既存のファイルパスはorchestrator/coordinator/workerにリネーム済み
  - プリセット（Standard/Racing/戦国/軍事/航空）をコメントアウトで保持しており、貼り替えるだけで切り替え可能
