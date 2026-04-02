# 仕様: ナレッジ/改善のフィードバック（Kaizen Loop）

## 目的（Intent）

この環境でプロジェクトを進める中で判明したナレッジ（学び・落とし穴・ベストプラクティス）や改善点（テンプレ修正・運用手順の更新・ルール追加）を、
**運用基盤（このリポジトリ）に継続的に還流**できるようにする。

## 制約（Constraints）

- “真実のソース”はファイルとする（会話ログだけに依存しない）
- 追加の実行エンジンは持たない（VS Code + Markdown 運用を維持）
- 変更は小さく行い、適用理由を残す
- mob（mob）は最小権限（自分のタスク範囲のみ）

## 受け入れ条件（Acceptance Criteria / Outcomes）

- [ ] 改善/ナレッジが発生したときの記録先が明文化されている
- [ ] その記録が、仕様/ルール/テンプレへ反映されるまでの流れが明文化されている
- [ ] 反映の結果が `status/dashboard.md` に残る

## 運用（Workflow）

### 1) まず記録（発見を逃さない）

- 気づき（短期のメモ/根拠）: 必要なら `output/` に残す
  - 例: `output/reports/kaizen-<topic>.md`
- 要点はelite（elite）へ返す（eliteが `status/dashboard.md` に集約して残す）
  - 重要判断が必要な場合は、boss（boss）にも共有する（ユーザ確認の材料）

### 2) 採用判断（boss / boss）

- boss（boss）が以下を判断する
  - 採用する / しない / 保留
  - 優先度（速度/品質/安全/学習）

### 3) 反映（eliteが分解 → mobが実装）

- 採用する場合、elite（elite）が変更をタスクへ分解し、mob（mob）へ配布する
- 反映先の例
  - 仕様テンプレ: `docs/spec/_template.md`
  - 使い方: `docs/USAGE.md`
  - 設計判断: `docs/decisions.md`
  - 役割ルール: `.github/instructions/*.instructions.md`
  - タスク実行の器: `.vscode/tasks.json`

### 4) ログ（なぜそうしたかを残す）

- 判断理由（設計/運用の決定）: `docs/decisions.md`
- 完了報告（いつ何が反映されたか）: `status/dashboard.md`

## タスクリスト（elite→mobへ配布する単位の例）

| task | assignee | input | output |
|---|---|---|---|
| Kaizenエントリ書式案を作る | mob-1 | Spec（本書） | `output/` 配下のメモ（例：`output/mob/kaizen-entry-format.md`） |
| ダッシュボードへ反映（集約） | elite | 上記メモ | `status/dashboard.md` 更新 |
| USAGEに改善フローを追記 | mob-2 | Spec（本書） | `docs/USAGE.md` 更新 |
| decisionsに判断テンプレを追記 | mob-3 | Spec（本書） | `docs/decisions.md` 更新 |
