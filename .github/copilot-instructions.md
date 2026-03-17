# Copilot workspace instructions（車載ソフトウェア第三者評価 multiAgent）

このリポジトリは「仕様駆動 + SOLID」で、Race Director・Pit Chief・Mechanicの役割分担を模したマルチエージェント基盤を
**車載ソフトウェア第三者評価業務**に適用する。

## 評価業務エージェント構成

| 役割 | Instructions ファイル | 担当業務ステップ |
|---|---|---|
| Race Director（レースディレクター） | `race-director.instructions.md` | 全体指揮・仕様確定・上様対応 |
| Pit Chief（ピットチーフ） | `pit-chief.instructions.md` | タスク分解・進捗管理・Mechanic調整 |
| 仕様解析（Mechanic-1） | `spec-analyzer.instructions.md` | ステップ1：製品仕様理解・信号一覧 |
| VT環境（Mechanic-2） | `vt-environment.instructions.md` | ステップ3：DBC/CAPLドラフト生成 |
| テスト仕様書（Mechanic-3） | `test-spec.instructions.md` | ステップ4：テスト設計仕様書ドラフト |
| テストケース（Mechanic-4） | `testcase.instructions.md` | ステップ5：テストケース一覧生成 |
| 結果解析（Mechanic-5） | `result-analyzer.instructions.md` | ステップ7：NG解析・ログ解析 |
| 報告書（Mechanic-6） | `report-writer.instructions.md` | ステップ8・9：懸念点シート・報告書生成 |

> AI化スコープ外：ステップ2（ハードウェア準備）・ステップ6（テスト実行）は人間が担当

## 最重要ルール

- 仕様（`docs/spec/`）を起点に作業する。
- Mechanic（worker）は **自分のタスクだけ** 実行する（最小権限）。
- 進捗は `status/dashboard.md` に集約して可視化する（更新責任者はPit Chief。競合防止のため、Race Director/サブエージェントは直接編集しない）。
- 重要判断（試験観点の確定、仕様解釈の相違、スコープ変更など）は、Race Directorが上様（担当者）に確認してから確定する。
- AI生成物は必ず `output/` 配下に限定する。**人間によるレビュー・承認なしに最終成果物として使用しない。**
	- 例外：運用の一次情報（`docs/spec/`, `docs/decisions.md`, `status/dashboard.md`）は従来どおり。

補足：会話/報告のルールは `docs/spec/agent-communication-v1.md` を正とする。

## ドキュメント運用（必須）

- 仕様：`docs/spec/`（Markdown）
- 設計判断ログ：`docs/decisions.md`
- 進捗：`status/dashboard.md`

作業を進めたら、上の3点のどれか（必要なら複数）を必ず更新する。

## 成果物管理（output/ 配下）

| 成果物 | ファイルパス | 担当Mechanic |
|---|---|---|
| 仕様サマリー | `output/spec_summary.md` | Mechanic-1（仕様解析） |
| 信号一覧 | `output/signal_list.md` | Mechanic-1（仕様解析） |
| DBCドラフト | `output/dbc_draft.md` | Mechanic-2（VT環境） |
| CAPLスケルトン | `output/capl_skeleton.can` | Mechanic-2（VT環境） |
| テスト仕様書ドラフト | `output/test_spec_draft.md` | Mechanic-3（テスト仕様書） |
| テストケース一覧 | `output/testcase_list.md` | Mechanic-4（テストケース） |
| NG解析レポート | `output/ng_analysis.md` | Mechanic-5（結果解析） |
| 懸念点確認シート | `output/concern_sheet_draft.md` | Mechanic-6（報告書） |
| 試験報告書 | `output/test_report_draft.md` | Mechanic-6（報告書） |

## ハルシネーション対策（全エージェント必須）

- 仕様書に明記されていない数値・仕様を生成することを禁止する
- 不明な点は「TODO: 要確認 — <質問内容>（ref: 仕様書名 p.XX）」と明記して推測で埋めない
- 根拠となる仕様書の参照箇所（ページ番号・セクション番号）を必ず記載する
- 全成果物の先頭に「このファイルはAIが生成したドラフトです。承認前に必ずレビューしてください。」を入れる

## 変更時の作法

- 追加・変更は「Spec→Plan→Tasks→Run→Dashboard更新」の流れに沿わせる。

## VS Code Tasks（並列実行）

- 並列実行は `.vscode/tasks.json` の `dependsOrder: parallel` を使う。
- Mechanicは複数ターミナルで起動し、各自の担当領域のみ処理する（最小権限）。
- 全タスクに `"presentation": { "close": true }` を設定し、完了後のゾンビターミナルを防止する。

## ターミナルクリーンアップ（ゾンビターミナル防止）

- エージェントが `execute` ツールでシェルコマンドを実行した後、不要なターミナルは `workbench.action.terminal.kill` で閉じること。
- 残留ターミナルは挙動を重くするため、使い終わったターミナルは必ず削除する。

## Copilot Subagents（サブエージェント並列）

- Race Directorは Subagents を使って「Pit Chief（調整）」＋「Mechanic×N（仕様解析/テスト設計/解析）」を並列起動し、成果を統合する。
- サブエージェントに渡すタスクは **単機能・小さく・競合しない** 単位にする。
- 重要：成果物は会話に埋めず、`output/` に配置してからPit Chiefが `status/dashboard.md` に要点をまとめる。

## AgentHQ（Custom Agents / Prompt Files / Handoffs）

各エージェントは `.github/agents/*.agent.md` に YAML frontmatter（tools/agents/handoffs）で定義。

- **tools**: そのエージェントが使えるツールを明示的に制限（最小権限）
- **agents**: 起動可能なサブエージェントを制限（Mechanicは `agents: []` で禁止）
- **handoffs**: エージェント間のワークフロー遷移ボタンを定義

役割別エージェント定義：

- `.github/agents/race-director.agent.md`
- `.github/agents/pit-chief.agent.md`
- `.github/agents/mechanic.agent.md`

## 禁止

- AI生成物をレビューなしに最終成果物として使用する
- 仕様書に根拠のない数値・仕様を生成する
- 役割を曖昧にする（誰が何をやるかを明文化する）
- 一度に巨大な改修（小さく分ける）
