# エージェント運用ルール更新（ユーザー判断ゲート + ロギング + output制約）

## 目的（Intent）

- 将軍/家老/足軽の指示書・定義を更新し、運用のブレと競合（同一ファイル編集）を減らす。
- 将軍が「重要判断」を上様（ユーザー）に確認してから進める仕組みを明文化する。
- ログ/成果物の置き場所を明確化し、生成物がリポジトリ直下に散らばらないようにする。

## 制約（Constraints）

- 仕様駆動（Spec → Plan → Tasks → Run → Dashboard更新）を維持する。
- SOLID（特に SRP/DIP）と最小変更を優先する。
- 生成物（調査メモ、比較表、スクリーンショット解析結果、ビルド成果物、tmp等）は `output/` 配下に限定する。
  - 例外：運用の一次情報（Spec/Decisions/Dashboard/Instructions）は既存どおり `docs/` と `status/` に置く。
- 参考: https://github.com/yohey-w/multi-agent-shogun の「上様お伺い（要対応集約）」「単一更新者」「イベント駆動」などの思想を、当リポジトリ（VS Code + Markdown運用）に合わせて移植する。

## 受け入れ条件（Acceptance Criteria / Outcomes）

- [ ] `.github/agents/shogun.agent.md` に「重要判断は上様に確認する」ルールが明文化され、質問フォーマット（選択肢と推奨）を含む。
- [ ] `.github/agents/karo.agent.md` / `.github/agents/ashigaru.agent.md` にも、判断が必要な場合のエスカレーション先（将軍）とログ場所が明記される。
- [ ] `.github/instructions/*.instructions.md` に、以下が明記される。
  - [ ] どの役割がどのファイルへ何を書くか（ロギング契約）
  - [ ] 生成物は `output/` 配下に限定（例外も明記）
- [ ] `status/dashboard.md` に「🚨 要対応（上様判断待ち）」のセクションが追加され、家老が判断待ち事項を集約する運用が書かれている（将軍は上様確認ゲートを担当）。
- [ ] `.gitignore` に `output/` 配下の生成物を基本的に追跡しない設定（例: `output/**` + `output/.gitkeep` 例外）が追加される。
- [ ] `docs/USAGE.md` に、`output/` の使い方（例: `output/build` を使う、調査結果は `output/reports/` 等）と例外（docs/statusは運用一次情報）が追記される。
- [ ] `docs/decisions.md` に本変更の採用判断が記録される。

## Plan（家老が分解する観点）

- 役割ごとの責務（誰が何を決め、どこに記録するか）を先に固定する
- 「上様お伺い」を必要とする判断点（技術選択/破壊的変更/生成物管理/外部依存/セキュリティ等）を列挙する
- 既存テンプレ（dashboard/usage）に無理なく差し込む（全面刷新はしない）

## タスクリスト（足軽へ配布する単位）

| task | assignee | input | output |
|---|---|---|---|
| エージェント定義（chatagent）更新 | ashigaru | `.github/agents/*.agent.md` | 更新パッチ |
| 指示書（instructions）更新 | ashigaru | `.github/instructions/*.instructions.md` | 更新パッチ |
| 運用Doc/ignore更新 | ashigaru | `docs/USAGE.md`, `.gitignore`, `status/dashboard.md`, `docs/decisions.md` | 更新パッチ |
