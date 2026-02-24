# ダッシュボード

進捗は `status/dashboard.md` に集約されます。

- ひな形（記入例）：`status/dashboard.template.md`
- テンプレートリポ自身の履歴：`status/dashboard.history.md`

## コミュニケーションはユーザが確認できる？

できます。
この運用では、会話ログ（チャット）ではなく **`status/dashboard.md` が“やり取りの要約ログ”**になります。

- 将軍：方針・受け入れ条件（AC）・優先度と、上様お伺い（重要判断）を担当（dashboardは直接編集しない）
- 家老：このファイルの **単一更新者**。start/done/blocked と進捗要点を集約して記録
- 足軽：実行結果（done/error、再現手順の要点）を家老へ報告（必要なら `output/` に生成物を残す）

ユーザ（上様）は、`status/dashboard.md` を見れば「誰が・いつ・何を決め/分解し/実行したか」を時系列で追えます。

## 何が書かれる？

- 足軽の起動（家老が要点を転記）
- タスクの start / done / error（作業者の役割名をログ行に含める）
- plan生成（家老の分解結果の要点）

## ログの書式

- 推奨：`[YYYY-MM-DD-HH:MM] <role>: <event>: <topic> (<note>)`
	- **必ず現在時刻（HH:MM）を記録する**こと
	- 時刻をどうしても取得できない場合のみ `00:00` を使用（例外。通常は使わない）

## どう見る？

VS Codeで `status/dashboard.md` を開き、Markdownプレビューで眺めます。

## よくある見方

- `start` が出たのに `done` が出ない：足軽が止まっている/タスクが失敗している
- 記録が増えない：家老が `status/dashboard.md` を更新できているか確認（詳細ログは `output/` にあるかも）

補足：報告テンプレ（YAML、skill_candidate 等）は `docs/spec/agent-communication-v1.md` を参照。

