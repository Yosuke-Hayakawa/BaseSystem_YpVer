# Dashboard

- [2026-02-05] init
- [2026-02-05 10:26:01] karo: plan start: sample
- [2026-02-05 10:26:05] karo: plan done: sample (tasks written)
- [2026-02-05] shogun: chore: expand .vscode/tasks.json (parallel placeholders)
- [2026-02-05] shogun: docs: add kaizen-loop spec and feedback workflow

## コミュニケーションの見え方（上様向け）

このファイルが、将軍・家老・足軽の「やり取りの要約ログ」です。

- 書き方の推奨：`<date time> <role>: <event>: <topic> (<note>)`
	- role: `shogun` / `karo` / `ashigaru-1` / `ashigaru-2` ...
	- event: `start` / `plan start` / `plan done` / `done` / `error` / `blocked`

上様はここを見て、次を確認します：

- 将軍：方針・受け入れ条件（AC）・優先度が固まったか
- 家老：タスク分解と担当割当が済んだか（競合しない切り方か）
- 足軽：担当タスクの start/done/error と、結果の要点が残っているか

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
