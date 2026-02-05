# 設計判断ログ（decisions）

このファイルは「なぜその設計にしたか」を短く残すログです。

- いつ：YYYY-MM-DD
- 何を：判断内容
- なぜ：理由
- 代替案：検討した選択肢
- 影響：影響範囲

---

## 2026-02-05: 実行基盤を「VS Code + ファイル運用」に統一（Python/シェルなし）

- 何を：タスク実行エンジン（Python実装やシェルスクリプト）を内蔵せず、VS Code + Copilot Chat（Agentモード）と Markdown ファイルで運用する
- なぜ：要求「VS Codeの設定と各種ファイル設定のみで実現」「Python/シェル排除」を優先
- 代替案：Node/Pythonで実行エンジンを実装 / bashでキュー処理
- 影響：ドキュメントと instruction を運用の中心にする（`docs/spec/`, `docs/decisions.md`, `status/dashboard.md`）。`.vscode/tasks.json` はプロジェクト固有コマンドの“器”として任意。
