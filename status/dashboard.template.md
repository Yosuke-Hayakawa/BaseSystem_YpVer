# Dashboard template

このファイルは `status/dashboard.md` の記入ガイド（ひな形）です。

- 実運用：`status/dashboard.md`
- 見方（役割・更新ルール・よくある見方）：`docs/ARCHITECTURE.md`（「ダッシュボードの見方」セクション）

---

## ログ書式

- 推奨：`[YYYY-MM-DD-HH:MM] <role>: <event>: <topic> (<note>)`
	- role: `orchestrator` / `coordinator` / `worker-1` / `worker-2` ...
	- event: `start` / `plan start` / `plan done` / `done` / `error` / `blocked`
	- **必ず現在時刻（HH:MM）を記録する**こと。時刻をどうしても取得できない場合のみ `00:00` を使用

## 記入例（チームオーナー→Orchestratorの依頼が来た直後）

> 実案件ではこのセクションを消してOK。

- request: <チームオーナーの依頼の短い要約>
	- status: triage
	- orchestrator: pending
	- coordinator: pending
	- worker: pending

### ログ（時系列）

- [2026-xx-xx-HH:MM] orchestrator: start: <topic>
- [2026-xx-xx-HH:MM] coordinator: plan start: <topic>
- [2026-xx-xx-HH:MM] coordinator: plan done: <topic>
- [2026-xx-xx-HH:MM] worker-1: start: <task>
- [2026-xx-xx-HH:MM] worker-1: done: <task> (<note>)
