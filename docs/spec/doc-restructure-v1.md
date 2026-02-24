# 仕様: ドキュメント構成の見直し（重複削除 + 整理）

## 目的（Intent）

- `docs/` フォルダの重複した記述を削除し、読み手が迷わない構成にする。
- 薄い単独ファイル（`docs/DASHBOARD.md`）を既存のドキュメントへ統合する。
- テンプレートリポジトリ自身の記録（`docs/decisions.md`）と、利用プロジェクト用テンプレートの分離を徹底する。

## 制約（Constraints）

- 情報を削除せず、適切な場所へ移動する（リンク切れを防ぐ）。
- 既存のワークフロー（Spec→Plan→Tasks→Run→Dashboard）を変更しない。
- 参照リンクを全件更新する。

## 受け入れ条件（Acceptance Criteria / Outcomes）

- [ ] `docs/DASHBOARD.md` が削除され、内容が `docs/ARCHITECTURE.md` の新セクションへ統合されている。
- [ ] `README.md`、`status/dashboard.md`、`status/dashboard.template.md` 内の `docs/DASHBOARD.md` への参照が `docs/ARCHITECTURE.md` へ更新されている。
- [ ] `docs/ARCHITECTURE.md` 内の `docs/DASHBOARD.md` への参照（「どこから読むか」セクション）が削除されている。
- [ ] `docs/decisions.md` からテンプレートリポ固有の "Decision: skills フィールドの追加" エントリが削除され、`docs/history.md` へ移動されている。
- [ ] `status/dashboard.template.md` の重複セクション（コミュニケーションの見え方）が削除/簡略化されている。
- [ ] `docs/history.md` に本変更の記録が追加されている。

## タスクリスト（足軽へ配布する単位）

| task | assignee | input | output |
|---|---|---|---|
| ARCHITECTURE.md に DASHBOARD.md 内容を統合 | ashigaru | `docs/DASHBOARD.md`, `docs/ARCHITECTURE.md` | `docs/ARCHITECTURE.md` 更新 |
| DASHBOARD.md 削除・参照更新 | ashigaru | 全ファイル | 参照先を `docs/ARCHITECTURE.md` へ変更 |
| decisions.md → history.md へ移動 | ashigaru | `docs/decisions.md`, `docs/history.md` | 両ファイル更新 |
| dashboard.template.md 重複削除 | ashigaru | `status/dashboard.template.md` | 更新パッチ |
| history.md に変更記録追加 | ashigaru | `docs/history.md` | 更新パッチ |
