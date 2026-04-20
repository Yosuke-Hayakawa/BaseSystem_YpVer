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

<!-- プロジェクト固有の設計判断をここに追記してください -->

## Decision: mob を固定役割から汎用プール方式に変更

- いつ：2026-04-20
- 何を：mob-1〜6 の固定役割構成を廃止し、汎用 mob プール方式に移行。elite がタスクごとに必要な数の mob を起動し、タスクテンプレート（旧・専用 instructions）を渡して指示する構成に変更。
- なぜ：固定 mob では同一ステップ内の並列処理ができず、仕様書が大量にある場合や NG が多発した場合にボトルネックになっていた。SKILL.md（task-decomposition, multi-agent-orchestration）の設計思想と整合させるため。
- 代替案：
  - A. 現行維持（固定 mob-1〜6）→ 並列効率の問題が残る
  - B. ハイブリッド（専任 + 汎用補助）→ mob の種類が増えて管理が複雑化
  - C. 完全汎用化（採用）→ SKILL.md と整合し、シンプル
- 反映先：`.github/copilot-instructions.md`, `.github/instructions/coordinator.instructions.md`, `.github/instructions/worker.instructions.md`, `.github/instructions/spec-analyzer.instructions.md`, `.github/instructions/vt-environment.instructions.md`, `.github/instructions/test-spec.instructions.md`, `.github/instructions/testcase.instructions.md`, `.github/instructions/result-analyzer.instructions.md`, `.github/instructions/report-writer.instructions.md`, `docs/ARCHITECTURE.md`
- 影響：elite の指示構成が「固定 mob を指名」から「テンプレートを選んで mob に渡す」に変わる。既存のタスクテンプレート（instructions ファイル）はそのまま再利用。
