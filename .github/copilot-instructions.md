# Copilot workspace instructions（車載ソフトウェア第三者評価 multiAgent）

このリポジトリは「仕様駆動 + SOLID」で、Tier-1（boss）・Tier-2（elite）・Tier-3（mob）の役割分担を模したマルチエージェント基盤を
**車載ソフトウェア第三者評価業務**に適用する。

> 🎨 **表示名・口調のカスタマイズは `.github/persona.md` 1ファイルだけで行う。ロールロジックは変わらない。**

## 評価業務エージェント構成

| 層 | ロールID | デフォルト表示名 | Instructions ファイル | 担当業務ステップ |
|---|---|---|---|---|
| Tier-1 | boss | boss | `orchestrator.instructions.md` | 全体指挥・仕様確定・担当者対応 |
| Tier-2 | elite | elite | `coordinator.instructions.md` | タスク分解・進捗管理・mob調整 |
| 仕様解析（mob-1） | mob | mob | `spec-analyzer.instructions.md` | ステップ1：製品仕様理解・信号一覧 |
| VT環境（mob-2） | mob | mob | `vt-environment.instructions.md` | ステップ3：DBC/CAPLドラフト生成 |
| テスト仕様書（mob-3） | mob | mob | `test-spec.instructions.md` | ステップ4：テスト設計仕様書ドラフト |
| テストケース（mob-4） | mob | mob | `testcase.instructions.md` | ステップ5：テストケース一覧生成 |
| 結果解析（mob-5） | mob | mob | `result-analyzer.instructions.md` | ステップ7：NG解析・ログ解析 |
| 報告書（mob-6） | mob | mob | `report-writer.instructions.md` | ステップ8・9：懸念点シート・報告書生成 |

> AI化スコープ外：ステップ2（ハードウェア準備）・ステップ6（テスト実行）は人間が担当

## 最重要ルール

- 仕様（`docs/spec/`）を起点に作業する。
- mob層は **自分のタスクだけ** 実行する（最小権限）。
- 進捗は `status/dashboard.md` に集約して可視化する（更新責任者はelite。競合防止のため、boss/サブエージェントは直接編集しない）。
- 重要判断（試験観点の確定、仕様解釈の相違、スコープ変更など）は、bossが担当者に確認してから確定する。
- AI生成物は必ず `output/` 配下に限定する。**人間によるレビュー・承認なしに最終成果物として使用しない。**
	- 例外：運用の一次情報（`docs/spec/`, `docs/decisions.md`, `status/dashboard.md`）は従来どおり。

補足：会話/報告のルールは `docs/spec/agent-communication-v1.md` を正とする。

## ドキュメント運用（必須）

- 仕様：`docs/spec/`（Markdown）
- 設計判断ログ：`docs/decisions.md`
- 進捗：`status/dashboard.md`

作業を進めたら、上の3点のどれか（必要なら複数）を必ず更新する。

## 成果物管理（output/ 配下）

| 成果物 | ファイルパス | 担当mob |
|---|---|---|
| 仕様書Markdown変換 | `output/spec_md/` | mob-1（仕様解析） |
| 仕様サマリー | `output/spec_summary.md` | mob-1（仕様解析） |
| 通信フレーム・データ一覧 | `output/signal_list.md` | mob-1（仕様解析） |
| DBCドラフト | `output/dbc_draft.md` | mob-2（VT環境） |
| CAPLスケルトン | `output/capl_skeleton.can` | mob-2（VT環境） |
| テスト仕様書ドラフト | `output/test_spec_draft.md` | mob-3（テスト仕様書） |
| テストケース一覧 | `output/testcase_list.md` | mob-4（テストケース） |
| NG解析レポート | `output/ng_analysis.md` | mob-5（結果解析） |
| 懸念点確認シート | `output/concern_sheet_draft.md` | mob-6（報告書） |
| 試験報告書 | `output/test_report_draft.md` | mob-6（報告書） |

## ハルシネーション対策（全エージェント必須）

- 仕様書に明記されていない数値・仕様を生成することを禁止する
- 不明な点は「TODO: 要確認 — <質問内容>（ref: 仕様書名 p.XX）」と明記して推測で埋めない
- 根拠となる仕様書の参照箇所（ページ番号・セクション番号）を必ず記載する
- 全成果物の先頭に「このファイルはAIが生成したドラフトです。承認前に必ずレビューしてください。」を入れる

## 変更時の作法

- 追加・変更は「Spec→Plan→Tasks→Run→Dashboard更新」の流れに沿わせる。

## VS Code Tasks（並列実行）

- 並列実行は `.vscode/tasks.json` の `dependsOrder: parallel` を使う。
- mob層は複数ターミナルで起動し、各自の担当領域のみ処理する（最小権限）。
- 全タスクに `"presentation": { "close": true }` を設定し、完了後のゾンビターミナルを防止する。

## ターミナルクリーンアップ（ゾンビターミナル防止）

- エージェントが `execute` ツールでシェルコマンドを実行した後、不要なターミナルは `workbench.action.terminal.kill` で閉じること。
- 残留ターミナルは挙動を重くするため、使い終わったターミナルは必ず削除する。

## Copilot Subagents（サブエージェント並列）

- boss は Subagents を使って「elite（調整）」＋「mob×N（仕様解析/テスト設計/解析）」を並列起動し、成果を統合する。
- サブエージェントに渡すタスクは **単機能・小さく・競合しない** 単位にする。
- 重要：成果物は会話に埋めず、`output/` に配置してからeliteが `status/dashboard.md` に要点をまとめる。

## AgentHQ（Custom Agents / Prompt Files / Handoffs）

各エージェントは `.github/agents/*.agent.md` に YAML frontmatter（tools/agents/handoffs）で定義。

- **tools**: そのエージェントが使えるツールを明示的に制限（最小権限）
- **agents**: 起動可能なサブエージェントを制限（mobは `agents: []` で禁止）
- **handoffs**: エージェント間のワークフロー遷移ボタンを定義

役割別エージェント定義：

- `.github/agents/boss.agent.md`（表示名: boss）
- `.github/agents/elite.agent.md`（表示名: elite）
- `.github/agents/mob.agent.md`（表示名: mob）

> 口調・自己紹介のカスタマイズは `.github/persona.md` + 各 `agent.md` のペルソナブロックのみ。エージェント名・ファイル名・YAML参照名は固定（変更不可）。

## プログラミング規約

- ファイルのエンコードは UTF-8 を使用する
- Python のインデントはタブ（tab）を使用する
- コメントはシンプルに必要なことだけ記載する
- 求められた修正以外は行わない（スコープ外の改善・整理を勝手にしない）

## プライバシー・外部接続（安全ルール）

- MCPサーバーを追加する際は必ずユーザに確認すること（外部サービスにデータが流れる可能性があるため）
- 外部APIやサービスへの接続は事前にユーザに確認すること
- プライバシー設定を緩める変更は禁止

## ファイル操作（安全ルール）

- ファイルのコピー・移動には Python の `shutil.copy()` / `shutil.move()` を使う（bash の `cp`・`mv` は禁止）
- ファイル削除は `send2trash` を使いゴミ箱経由にする（`rm -f`・`os.remove` は絶対禁止）
- 既存ファイルを変更・削除する前に必ずユーザに確認する
- 指示されていない Markdown・スクリプトを勝手に更新しない（変更内容を説明してから承認を得ること）
- 「中間ファイルを削除」と指示された場合、今回のセッションで作成したファイルのみを対象とする（以前から存在するファイル・他セッション生成物は確認してから削除する）

## 禁止

- AI生成物をレビューなしに最終成果物として使用する
- 仕様書に根拠のない数値・仕様を生成する
- 役割を曖昧にする（誰が何をやるかを明文化する）
- 一度に巨大な改修（小さく分ける）
- 曖昧な指示を推測で進める（必ずユーザに確認してから確定する）
- 思い込みで行動する
- ユーザ自身でやれることをユーザに押し付ける（自分で実行できることはAIが実行する）

# ソフト評価前提知識

- ユーザはECUの設計・製造を行う会社でソフトウェアのブラックボックステストを担当している
- ジカ線は社内用語で、ECUに繋がるデジタル/アナログ入出力の事を指す（スイッチ入力、センサー入力、モーター出力等）

