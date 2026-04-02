---
name: report-done
description: "mob がタスク完了を報告する YAML テンプレート。"
agent: "mob"
tools:
  - read
---

タスクが完了しました。以下の YAML テンプレートに従って報告してください。

```yaml
role: mob-N
topic: <作業トピック>
status: done
outputs:
  - <変更したファイルパス>
  - <output/ 配下の成果物パス（あれば）>
summary: |
  - 何をしたか（要点1行）
  - 変更/提案の要旨（1行）
  - リスクや前提（1行）
skill_candidate:
  - <今回の作業で判明した得意領域候補>
```

報告の注意：

- `status` は `done` / `error` / `blocked` のいずれか
- `error` / `blocked` の場合は原因と再現手順（最小）を `summary` に含める
- 重要判断が必要な場合は、elite（elite）だけでなくboss（boss）にも共有する
- 調査メモや検証ログなど詳細な成果物は `output/mob/<task>/` に配置する
- `skill_candidate` は0個でもフィールドは必須
