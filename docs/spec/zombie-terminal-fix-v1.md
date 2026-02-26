# ゾンビターミナル解消（VS Code Tasks 自動クローズ＋エージェントターミナル手動クローズ）

## 目的（Intent）

VS Code Tasks およびエージェントが `execute` ツールで直接シェルコマンドを実行した際、
完了後もターミナルが残留する「ゾンビターミナル」問題を解消する。

## 制約（Constraints）

- `.vscode/tasks.json` の既存タスク定義の構造・動作を変えない（最小変更）。
- タスクの `presentation` オプションのみ追加する。
- エージェント定義/指示書への追記は最小限（既存ルールを上書きしない）。

## 受け入れ条件（Acceptance Criteria）

- [ ] `.vscode/tasks.json` の全シェルタスクに `"presentation": { "close": true }` が設定されている。
- [ ] タスク完了後、対応するターミナルパネルが自動的に閉じる（目視確認）。
- [ ] 既存タスクの実行動作（コマンド・引数）は変更されない。
- [ ] エージェント（足軽）が `execute` ツールでコマンドを実行した後、不要なターミナルを `workbench.action.terminal.kill` で閉じる旨が指示書に明記されている。
- [ ] `.github/copilot-instructions.md` にターミナルクリーンアップの全体ルールが明記されている。
- [ ] `docs/decisions.md` に採用判断が記録されている。
