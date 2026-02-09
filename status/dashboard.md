# Dashboard

- [2026-02-05] init
- [2026-02-05 10:26:01] karo: plan start: sample
- [2026-02-05 10:26:05] karo: plan done: sample (tasks written)
- [2026-02-05] shogun: chore: expand .vscode/tasks.json (parallel placeholders)
- [2026-02-05] shogun: docs: add kaizen-loop spec and feedback workflow
- [2026-02-05] shogun: decision: dashboard single editor -> karo
- [2026-02-05] karo: chore: dashboard becomes single editor (rules updated)
- [2026-02-09] shogun: start: AgentHQ移行（Custom Agents / Subagents / Prompt Files / Handoffs）
- [2026-02-09] shogun: spec done: `docs/spec/agenthq-migration-v1.md` 作成
- [2026-02-09] ashigaru: done: agent.md 3ファイル更新（tools/agents/handoffs frontmatter追加）
- [2026-02-09] ashigaru: done: Prompt Files 5ファイル作成（`.github/prompts/`）
- [2026-02-09] ashigaru: done: ARCHITECTURE.md / USAGE.md / decisions.md 更新
- [2026-02-09] karo: done: dashboard更新（AgentHQ移行完了記録）

## コミュニケーションの見え方（上様向け）

このファイルが、将軍・家老・足軽の「やり取りの要約ログ」です。

重要：競合防止のため、このファイルは **家老（karo）が集約して更新**します（単一更新者）。
ログ行の `role` は「実際に作業した役割」を表し、家老が要点を転記します。

補足：報告テンプレ（YAML）など会話/報告の規約は `docs/spec/agent-communication-v1.md` を参照。

- 書き方の推奨：`<date time> <role>: <event>: <topic> (<note>)`
	- role: `shogun` / `karo` / `ashigaru-1` / `ashigaru-2` ...
	- event: `start` / `plan start` / `plan done` / `done` / `error` / `blocked`

上様はここを見て、次を確認します：

- 将軍：方針・受け入れ条件（AC）・優先度が固まったか
- 家老：タスク分解と担当割当が済んだか（競合しない切り方か）
- 足軽：担当タスクの start/done/error と、結果の要点が残っているか

## 🚨 要対応（上様判断待ち）

重要判断（技術選定、外部依存追加、破壊的変更、運用ルール変更、セキュリティ/権限、生成物の配置など）が出たら、将軍がここに集約します。

- [ ] (date) <topic>
	- 選択肢：A / B / C
	- 推奨：B
	- 理由：<one-line>
	- リスク：<one-line>
	- 期限：<任意>

## Kaizen（改善/ナレッジ）バックログ

ここは「運用していて気付いた改善点」を一旦集める場所です。

- [ ] (date) <role>: kaizen found: <topic> (<one-line>)
- [ ] (date) shogun: kaizen decision: adopt/hold/reject (<reason>)

## 記入例（上様→将軍の依頼が来た直後）

> これは例です。実案件ではこのセクションを消してOK。

- request: <上様の依頼の短い要約>
	- status: triage
	- shogun: pending
	- karo: pending
	- ashigaru: pending

### ログ（時系列）

- 2026-xx-xx shogun: start / done / blocked（どれか）
- 2026-xx-xx karo: plan start / plan done
- 2026-xx-xx ashigaru-1: start / done / error
