# Copilot workspace instructions（multiAgent）

このリポジトリは「仕様駆動 + SOLID」で、将軍・家老・足軽の役割分担を模したマルチエージェント基盤を作る。

## 最重要ルール

- 仕様（`docs/spec/`）を起点に実装する。コード変更時は、まず仕様/受け入れ条件を更新する。
- SOLID を意識し、Port/Adapter（依存性逆転）を守る。
- 足軽（worker）は **自分のタスクだけ** 実行する（最小権限）。
- 進捗は必ず `status/dashboard.md` に追記して可視化する。

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

役割別エージェント定義：

- `.github/agents/shogun.agent.md`
- `.github/agents/karo.agent.md`
- `.github/agents/ashigaru.agent.md`

## 禁止

- 一度に巨大な改修（小さく分ける）
- 役割を曖昧にする（誰が何をやるかを明文化する）
