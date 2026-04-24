# タスク管理 template

このファイルは `status/task.md` の記入ガイド（ひな形）です。

- 実運用：`status/task.md`
- 見方（役割・更新ルール・よくある見方）：`docs/ARCHITECTURE.md`（「タスク管理の見方」セクション）

---

## ログ書式

- 推奨：`[YYYY-MM-DD-HH:MM] <role>: <event>: <topic> (<note>)`
	- role: `Phillips` / `Barnes` / `Cole` / `Cole` ...
	- event: `start` / `plan start` / `plan done` / `done` / `error` / `blocked`
	- **必ず現在時刻（HH:MM）を記録する**こと。時刻をどうしても取得できない場合のみ `00:00` を使用

## 記入例（ユーザ→Phillipsの依頼が来た直後）

> 実案件ではこのセクションを消してOK。

- request: <ユーザの依頼の短い要約>
	- status: triage
	- Phillips: pending
	- Barnes: pending
	- Cole: pending

### ログ（時系列）

- [2026-xx-xx-HH:MM] Phillips: start: <topic>
- [2026-xx-xx-HH:MM] Barnes: plan start: <topic>
- [2026-xx-xx-HH:MM] Barnes: plan done: <topic>
- [2026-xx-xx-HH:MM] Cole: start: <task>
- [2026-xx-xx-HH:MM] Cole: done: <task> (<note>)
