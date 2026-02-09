# Dashboard

進捗とやり取りの要点は、このファイルに集約します（単一更新者：家老）。

- 見方：`docs/DASHBOARD.md`
- ひな形：`status/dashboard.template.md`
- テンプレートリポ自身の履歴：`status/dashboard.history.md`

## ログ（時系列）

- 書式：`[YYYY-MM-DD-HH:MM] <role>: <event>: <topic> (<note>)`
	- role: `shogun` / `karo` / `ashigaru-1` / `ashigaru-2` ...
	- event: `start` / `plan start` / `plan done` / `done` / `error` / `blocked`
	- 時刻不明の場合は `00:00` を使用

<!-- ここにログ行を追記していく -->

## 🚨 要対応（上様判断待ち）

重要判断（技術選定、外部依存追加、破壊的変更、運用ルール変更、セキュリティ/権限、生成物の配置など）が出たら、
将軍が家老へ共有し、**家老がここに集約**します（単一更新者ルールのため）。

- [ ] [YYYY-MM-DD-HH:MM] <topic>
	- 選択肢：A / B / C
	- 推奨：B
	- 理由：<one-line>
	- リスク：<one-line>
	- 期限：<任意>

## Kaizen（改善/ナレッジ）バックログ

ここは「運用していて気付いた改善点」を一旦集める場所です。

- [ ] [YYYY-MM-DD-HH:MM] <role>: kaizen found: <topic> (<one-line>)
- [ ] [YYYY-MM-DD-HH:MM] shogun: kaizen decision: adopt/hold/reject (<reason>)

（記入例は `status/dashboard.template.md` を参照）

