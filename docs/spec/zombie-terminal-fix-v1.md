# ゾンビターミナル解消（VS Code Tasks 自動クローズ）

## 目的（Intent）

VS Code Tasks でエージェントがシェルコマンドを実行した際、タスク完了後もターミナルが残留する「ゾンビターミナル」問題を解消する。

## 制約（Constraints）

- `.vscode/tasks.json` の既存タスク定義の構造・動作を変えない（最小変更）。
- タスクの `presentation` オプションのみ追加する。
- 他のファイルへの影響を最小化する。

## 受け入れ条件（Acceptance Criteria）

- [ ] `.vscode/tasks.json` の全シェルタスクに `"presentation": { "close": true }` が設定されている。
- [ ] タスク完了後、対応するターミナルパネルが自動的に閉じる（目視確認）。
- [ ] 既存タスクの実行動作（コマンド・引数）は変更されない。
- [ ] `docs/decisions.md` に採用判断が記録されている。
