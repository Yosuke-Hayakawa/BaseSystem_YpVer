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

## Decision: ゾンビターミナル解消（2026-02-26）

- いつ：2026-02-26
- 何を：(1) `.vscode/tasks.json` の全シェルタスクに `"presentation": { "close": true }` を追加。(2) エージェント指示書（`ashigaru.agent.md`, `ashigaru.instructions.md`）および `copilot-instructions.md` に `execute` ツール使用後のターミナルクリーンアップルール（`workbench.action.terminal.kill`）を追記。
- なぜ：エージェントがターミナルを使った際、終了時にクローズしないことでゾンビターミナルが発生し挙動が重くなるため。VS Code Tasks と直接 `execute` ツール利用の両経路を対策する。
- 代替案：`"reveal": "silent"` のみ設定（ターミナルを非表示にするが削除はしない）→ 根本解消にならないため不採用
- 反映先：`.vscode/tasks.json`、`.github/agents/ashigaru.agent.md`、`.github/instructions/ashigaru.instructions.md`、`.github/copilot-instructions.md`、`docs/spec/zombie-terminal-fix-v1.md`
- 影響：タスク完了後にターミナルパネルが自動クローズされる。エージェントが `execute` ツールを使った後も不要ターミナルが削除される。既存の実行動作（コマンド・引数）は変更なし。
