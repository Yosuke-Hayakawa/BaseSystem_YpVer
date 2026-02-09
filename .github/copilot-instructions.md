# Copilot workspace instructions（multiAgent）

このリポジトリは「仕様駆動 + SOLID」で、将軍・家老・足軽の役割分担を模したマルチエージェント基盤を作る。

## 最重要ルール

- 仕様（`docs/spec/`）を起点に実装する。コード変更時は、まず仕様/受け入れ条件を更新する。
- SOLID を意識し、Port/Adapter（依存性逆転）を守る。
- 足軽（worker）は **自分のタスクだけ** 実行する（最小権限）。
- 進捗は `status/dashboard.md` に集約して可視化する（更新責任者は家老。競合防止のため、将軍/サブエージェントは直接編集しない）。
- 重要判断（技術選定、外部依存追加、破壊的変更、運用ルール変更など）は、将軍が上様（ユーザー）に確認してから確定する。
- 生成物（調査メモ、比較表、検証ログ、ビルド生成物、tmp等）は `output/` 配下に限定する。
	- 例外：運用の一次情報（`docs/spec/`, `docs/decisions.md`, `status/dashboard.md`）は従来どおり。

補足：会話/報告のルールは `docs/spec/agent-communication-v1.md` を正とする。

## ドキュメント運用（必須）

- 仕様：`docs/spec/`（Markdown）
- 設計判断ログ：`docs/decisions.md`
- 進捗：`status/dashboard.md`

変更を入れたら、上の3点のどれか（必要なら複数）を必ず更新する。

## 変更時の作法

- 追加機能は「Spec→Plan→Tasks→Run→Dashboard更新」の流れに沿わせる。
- コマンドや自動化の追加は、プロジェクトの言語/ビルド方式に合わせて小さく導入し、既存運用を壊さない。
- 可能ならプロジェクト標準のテスト（例：ユニットテスト）を最低1本（成功 + 失敗/境界）追加する。

## VS Code Tasks（並列実行）

- 並列実行は `.vscode/tasks.json` の `dependsOrder: parallel` を使う。
- 足軽は複数ターミナルで起動し、各自の担当領域のみ処理する（最小権限）。

## Copilot Subagents（サブエージェント並列）

- 将軍は Subagents を使って「家老（レビュー）」＋「足軽×N（実装/調査/テスト）」を並列起動し、成果を統合する。
- サブエージェントに渡すタスクは **単機能・小さく・競合しない**単位にする。
- 重要：成果物は会話に埋めず、必要に応じて `docs/spec/` / `docs/decisions.md` / `status/dashboard.md` に反映してから統合する。
	- 補足：調査結果や詳細ログなど「生成物」は `output/` に置き、家老が要点だけを `status/dashboard.md` に転記する。

## AgentHQ（Custom Agents / Prompt Files / Handoffs）

各エージェントは `.github/agents/*.agent.md` に YAML frontmatter（tools/agents/handoffs）で定義。

- **tools**: そのエージェントが使えるツールを明示的に制限（最小権限）
- **agents**: 起動可能なサブエージェントを制限（足軽は `agents: []` で禁止）
- **handoffs**: エージェント間のワークフロー遷移ボタンを定義

Prompt Files（`.github/prompts/*.prompt.md`）でワークフローをスラッシュコマンド化：
- `/create-spec`, `/decompose-tasks`, `/review-request`, `/report-done`, `/escalate`

役割別エージェント定義：

- `.github/agents/shogun.agent.md`
- `.github/agents/karo.agent.md`
- `.github/agents/ashigaru.agent.md`

## 禁止

- 一度に巨大な改修（小さく分ける）
- 役割を曖昧にする（誰が何をやるかを明文化する）
