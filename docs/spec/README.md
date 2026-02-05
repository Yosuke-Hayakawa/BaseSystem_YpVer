# specs（仕様置き場）

このフォルダは「仕様駆動（Spec → Plan → 実装）」の **Spec** を Markdown で管理します。

## 使い方

- `docs/spec/_template.md` をコピーして Spec を作成
- 将軍が以下を明確化
  - 目的（Intent）
  - 制約（Constraints）
  - 受け入れ条件（Acceptance Criteria）
- 家老が Spec を読んで、並列タスクに分解し `status/dashboard.md` にタスクと担当を記載
- 足軽が担当タスクを進め、結果（done/error、再現手順や差分）を `status/dashboard.md` に記録

## ファイル例

- `YYYYMMDD-your-feature.md`

## 改善（Kaizen）の扱い

プロジェクトを進める中で出た「学び/落とし穴/手順の改善」は、仕様として扱うと運用に還流しやすくなります。

- 改善フロー仕様：`docs/spec/kaizen-loop.md`
