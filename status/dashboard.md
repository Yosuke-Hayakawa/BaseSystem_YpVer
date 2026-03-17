# Dashboard — 車載ソフトウェア第三者評価

進捗とやり取りの要点は、このファイルに集約します（単一更新者：Pit Chief）。

- ひな形：`status/dashboard.template.md`
- 履歴：`status/dashboard.history.md`

---

## 現在のプロジェクト

| 項目 | 内容 |
|---|---|
| 製品名/型番 | — |
| 試験種別 | — |
| フェーズ | — |
| 担当者 | — |

---

## 成果物ステータス

| 成果物 | ファイル | ステータス | 担当Mechanic | 備考 |
|---|---|---|---|---|
| 仕様サマリー | `output/spec_summary.md` | 未着手 | Mechanic-1 | |
| 信号一覧 | `output/signal_list.md` | 未着手 | Mechanic-1 | |
| DBCドラフト | `output/dbc_draft.md` | 未着手 | Mechanic-2 | |
| CAPLスケルトン | `output/capl_skeleton.can` | 未着手 | Mechanic-2 | |
| テスト仕様書ドラフト | `output/test_spec_draft.md` | 未着手 | Mechanic-3 | |
| テストケース一覧 | `output/testcase_list.md` | 未着手 | Mechanic-4 | |
| NG解析レポート | `output/ng_analysis.md` | 未着手 | Mechanic-5 | |
| 懸念点確認シート | `output/concern_sheet_draft.md` | 未着手 | Mechanic-6 | |
| 試験報告書 | `output/test_report_draft.md` | 未着手 | Mechanic-6 | |

> ステータス凡例：未着手 / 作業中 / レビュー待ち / 承認済み / ブロック中

---

## ログ（時系列）

- 書式：`[YYYY-MM-DD-HH:MM] <role>: <event>: <topic> (<note>)`
	- role: `race-director` / `pit-chief` / `mechanic-1` 〜 `mechanic-6`
	- event: `start` / `plan start` / `plan done` / `done` / `error` / `blocked`
	- **必ず現在時刻（HH:MM）を記録する**こと

<!-- ここにログ行を追記していく -->
- [2026-03-17-00:00] race-director: start: リポジトリ初期化（設計部署用から第三者評価用に変更）

---

## 🚨 要対応（チームオーナー判断待ち）

重要判断（試験スコープ確定、合否基準解釈、非機能試験条件確定、仕様の矛盾裁定など）が出たら、
Race DirectorがPit Chiefへ共有し、**Pit Chiefがここに集約**します。

- [ ] [YYYY-MM-DD-HH:MM] <topic>
	- 選択肢：A / B / C
	- 推奨：B
	- 理由：<one-line>
	- リスク：<one-line>
	- 期限：<任意>

---

## Kaizen（改善/ナレッジ）バックログ

- [ ] [YYYY-MM-DD-HH:MM] <role>: kaizen found: <topic> (<one-line>)
- [ ] [YYYY-MM-DD-HH:MM] race-director: kaizen decision: adopt/hold/reject (<reason>)

（記入例は `status/dashboard.template.md` を参照）

