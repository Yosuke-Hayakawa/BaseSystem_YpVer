# ダッシュボード

進捗は `status/dashboard.md` に集約されます。

## コミュニケーションはユーザが確認できる？

できます。
この運用では、会話ログ（チャット）ではなく **`status/dashboard.md` が“やり取りの要約ログ”**になります。

- 将軍：start/done/blocked と意思決定（方針・優先度）を記録
- 家老：plan start/plan done、タスク分解結果（担当/成果物/完了条件）を記録
- 足軽：start/done/error と、変更要旨・再現手順（最小）を記録

ユーザ（上様）は、`status/dashboard.md` を見れば「誰が・いつ・何を決め/分解し/実行したか」を時系列で追えます。

## 何が書かれる？

- 足軽の起動
- タスクの start / done / error
- plan生成（家老）

## どう見る？

VS Codeで `status/dashboard.md` を開き、Markdownプレビューで眺めます。

## よくある見方

- `start` が出たのに `done` が出ない：足軽が止まっている/タスクが失敗している
- 記録が増えない：作業ログの追記先が `status/dashboard.md` になっているか確認（会話ログではなくファイルに残す）

