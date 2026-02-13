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

## Decision: skills フィールドの追加

- いつ：2026-02-13
- 何を：Custom Agent 定義（`.agent.md`）に `skills` フィールドを追加
- なぜ：GitHub Copilot の Custom Agents 機能において、各エージェントの得意領域（skills）を明示することで、タスクルーティングの精度向上と、エージェント選択時の可視性向上が期待される。Qiita 記事などのベストプラクティスに基づき、標準的な agent.md 形式に準拠する。
- 代替案：
  - skills フィールドなし：エージェント選択が description のみに依存し、機械的なルーティングが困難
  - skills を description に統合：人間の可読性は向上するが、構造化された情報が失われる
- 反映先：
  - `.github/agents/shogun.agent.md`
  - `.github/agents/karo.agent.md`
  - `.github/agents/ashigaru.agent.md`
  - `docs/spec/agenthq-migration-v1.md`（受け入れ条件に skills を追記）
  - `docs/ARCHITECTURE.md`（Custom Agents の表に skills を追記）
- 影響：
  - 既存のエージェント動作には影響なし（skills は追加情報）
  - 将来的なタスク自動割り当て機能で活用可能
  - エージェント選択時の UI で skills が表示される可能性あり
