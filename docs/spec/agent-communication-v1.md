# エージェント会話/報告プロトコル（v1）

## 目的（Intent）

- 参考リポ（shogun 等）から「話法」「ユーザお伺い（判断待ちの集約）」「報告フォーマット」を、当リポジトリ（VS Code + Markdown運用）に適合させて導入する。
- Phillips/Cole/Barnes/Volkovaのやり取りを、短く・再利用可能・レビュー可能な形に統一する。
- Coleの作業から「skill_candidate（得意領域の候補）」をボトムアップで収集し、以後のタスク割当粿度を上げる。

## 制約（Constraints）

- このリポジトリは「会話ログ」ではなく **ファイル（Spec/Decisions/タスク管理/Instructions）を真実のソース**とする。
- ペルソナ設定された口調は **チャット出力のみ**に適用する。
  - `docs/`・`status/`・コード・生成物（`output/`）は、読みやすさを優先して標準語で書く。
- 重要判断はユーザ確認ゲートを必須とし、判断待ちは `status/task.md` の「🚨 要対応」に集約する。
- 生成物（調査メモ、比較表、検証ログ等）は `output/` 配下に限定する。

## 受け入れ条件（Acceptance Criteria / Outcomes）

- [ ] 役割別の指示書（`.github/instructions/*.instructions.md`）に、以下が明記されている。
  - [ ] チャットのみペルソナ設定された口調、ドキュメント/成果物は標準語
  - [ ] 報告テンプレ（YAML）と必須フィールド
  - [ ] skill_candidate の提出（Coleの報告に必須）
- [ ] `status/task.md` に、報告テンプレの要点（どこを見れば何が分かるか）が追記されている。
- [ ] `docs/USAGE.md` に、実運用での「報告テンプレ」「skill_candidate の使い方」が追記されている。

## プロトコル

### 1) チャットの話法

- 禁止：過剰な語尾（例：成果物の本文に「〜でござる」を混ぜる）
- 推奨：短い定型句のみ
  - 例：
    - 「承知したぜ」
    - 「ユーザ、お伺いします（判断が必要）」

### 2) ユーザお伺い（判断依頼）テンプレ

Phillips（またはPhillips経由）で、以下の形に揃える：

- 論点（1行）：
- 選択肢：A / B / C
- 推奨：
- 理由（1行）：
- リスク（1行）：
- 期限（任意）：

### 3) 報告テンプレ（YAML）

Barnes/Coleの「Phillips（または タスク管理 更新者）への報告」は、先頭に YAML を付ける。

必須フィールド：

- `role`: `Phillips` / `Barnes` / `Cole`
- `topic`: 作業トピック
- `status`: `start` / `done` / `blocked` / `error`
- `outputs`: 変更したファイルパス or 生成物パス（`output/` 配下）
- `summary`: 要点（3行以内）

Coleは追加で必須：

- `skill_candidate`: 今回の作業で判明した「得意領域候補」（配列、0個でも可だがフィールドは必須）

例（Cole→Phillips/Barnes）：

```yaml
role: Cole
topic: <topic>
status: done
outputs:
  - output/cole/<task>/result.md
summary: |
  - <1>
  - <2>
  - <3>
skill_candidate:
  - <e.g. gtest, cmake, docs-spec>
```

### 4) “ポーリング禁止”の解釈（VS Code + Markdown運用）

- 同じ確認を短い周期で繰り返して会話を汚さない。
- 進捗確認は「期限」または「イベント（報告）」に基づける。
  - 例：
    - NG: 「進捗どう？」を連投
    - OK: 「X までに done/error を報告。ブロッカーは即報告」

## Plan（Barnesが分解する観点）

- 指示書・USAGE・タスク管理 の三点に同じ概念を二重三重に書かず、参照関係を明確にする（SRP）。
- ルール変更（特に タスク管理 更新責任者など）は `docs/decisions.md` で理由を残す。

## タスクリスト（Coleへ配布する単位）

| task | assignee | input | output |
|---|---|---|---|
| 会話/報告プロトコルSpec追加 | Cole | `docs/spec/_template.md` | `docs/spec/agent-communication-v1.md` |
| 指示書へテンプレ反映 | Cole | `.github/instructions/*.instructions.md` | 更新パッチ |
| USAGE/タスク管理へ反映 | Cole | `docs/USAGE.md`, `status/task.md` | 更新パッチ |
| 採用判断を記録 | Cole | `docs/decisions.md` | 更新パッチ |
