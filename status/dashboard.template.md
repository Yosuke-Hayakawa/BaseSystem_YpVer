# Dashboard template

このファイルは `status/dashboard.md` の記入ガイド（ひな形）です。

- 実運用：`status/dashboard.md`
- 見方：`docs/DASHBOARD.md`

---

## コミュニケーションの見え方（上様向け）

`status/dashboard.md` が、将軍・家老・足軽の「やり取りの要約ログ」になります。

重要：競合防止のため、dashboard は **家老（karo）が集約して更新**します（単一更新者）。
ログ行の `role` は「実際に作業した役割」を表し、家老が要点を転記します。

補足：報告テンプレ（YAML）など会話/報告の規約は `docs/spec/agent-communication-v1.md` を参照。

## ログ書式

- 推奨：`[YYYY-MM-DD-HH:MM] <role>: <event>: <topic> (<note>)`
	- role: `shogun` / `karo` / `ashigaru-1` / `ashigaru-2` ...
	- event: `start` / `plan start` / `plan done` / `done` / `error` / `blocked`
	- **必ず現在時刻（HH:MM）を記録する**こと。時刻をどうしても取得できない場合のみ `00:00` を使用

## 記入例（上様→将軍の依頼が来た直後）

> 実案件ではこのセクションを消してOK。

- request: <上様の依頼の短い要約>
	- status: triage
	- shogun: pending
	- karo: pending
	- ashigaru: pending

### ログ（時系列）

- [2026-xx-xx-HH:MM] shogun: start: <topic>
- [2026-xx-xx-HH:MM] karo: plan start: <topic>
- [2026-xx-xx-HH:MM] karo: plan done: <topic>
- [2026-xx-xx-HH:MM] ashigaru-1: start: <task>
- [2026-xx-xx-HH:MM] ashigaru-1: done: <task> (<note>)
