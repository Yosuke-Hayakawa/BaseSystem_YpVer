# アーキテクチャ

## このリポジトリの狙い

Zennの記事で出てくる「Race Director→Pit Chief→Mechanic（並列）」の形を、**tmuxなし**かつ **仕様駆動 + SOLID** を意識して小さく再構成します。

このリポジトリは「実行エンジン」を内蔵しません。
代わりに **VS Code + Copilot Chat（Agentモード）** と Markdown ファイルを“運用基盤”として使います。

## どこから読むか（入口）

- 概要（最短）：`README.md`
- 初回準備と、Race Directorへの指示の出し方：`docs/USAGE.md`
- 仕組みの全体像（この文書）：`docs/ARCHITECTURE.md`

## 構成要素（一次情報と生成物）

- Spec：`docs/spec/`（仕様：Intent/Constraints/AC。Race Directorが確定させる）
- Decisions：`docs/decisions.md`（設計判断ログ：各プロジェクトで使うテンプレ）
- Dashboard：`status/dashboard.md`（進捗とやり取り要点：**Pit Chiefが単一更新者**）
- Output：`output/`（生成物：調査メモ、比較表、検証ログ、ビルド生成物、tmp 等）
- Instructions：`.github/instructions/*.instructions.md`（役割ごとの振る舞いを固定）
- Tasks（任意）：`.vscode/tasks.json`（あなたのプロジェクトの build/test/lint を並列実行する“器”）

## 運用モデル（役割・フロー・競合回避）

### 役割と責務

- 上様（ユーザ）：方向付けと承認（重要判断への回答、完了の承認）
- Race Director（race-director）：Spec と受け入れ条件（AC）を確定し、重要判断は上様に確認してから進める
- Pit Chief（pit-chief）：Spec をタスクへ分解し、Mechanicへ配布し、`status/dashboard.md` に進捗を集約（単一更新者）
- Mechanic（mechanic）：自分の担当タスクだけ実行し、要点をPit Chiefへ返す（必要なら `output/` に生成物）

### 基本フロー

1. Race Director：`docs/spec/` に Spec（目的/制約/AC）を作る
2. Pit Chief：Spec を読み、並列可能なタスクに分解（競合しない切り方）
3. Mechanic：担当タスクを実行（コード編集/レビュー/テスト/調査など）
4. Pit Chief：結果を取りまとめ、`status/dashboard.md` に start/done/error/blocked を集約
5. 上様：判断待ち（`🚨 要対応`）に答え、完了を承認する

会話/報告テンプレ（YAML 等）の詳細は `docs/spec/agent-communication-v1.md` を参照してください。

### 並列化と競合回避

- Mechanicは複数起動して並列対応する（担当を分ける）
- 競合回避：同じファイルを複数のMechanicが同時に編集しないよう、Pit Chiefが **ファイル単位**でタスクを切る
- 進捗の同期：会話ログではなく、Pit Chiefが `status/dashboard.md` に要点を転記して合流する

### ログ/成果物の置き場所

- 一次情報：`docs/spec/`, `docs/decisions.md`, `status/dashboard.md`
- 生成物：`output/` 配下のみ（調査メモ、比較表、検証ログ、ビルド生成物、tmp 等）

## AgentHQ（Custom Agents / Subagents / Prompt Files / Handoffs）

VS Code の Custom Agents 機能を使い、Race Director/Pit Chief/Mechanicのオーケストレーションを正式に定義しています。

### Custom Agents（`.github/agents/*.agent.md`）

各エージェントは YAML frontmatter で `skills`（得意領域）、`tools`（使えるツール）、`agents`（起動できるサブエージェント）、`handoffs`（ワークフロー遷移ボタン）を明示的に定義しています。

| Agent | Role | skills | tools | agents | handoffs |
|---|---|---|---|---|---|
| **Race Director** | Orchestrator | orchestration, specification-definition, task-planning等 | read, search, fetch, agent, editFiles, problems | Pit Chief, Mechanic, Plan | Pit Chiefへタスク分解/レビュー依頼、Mechanicへ実装委任 |
| **Pit Chief** | Reviewer/QA | code-review, quality-assurance, task-decomposition等 | read, search, fetch, editFiles, problems, agent | Mechanic | Race Directorへ統合報告、Mechanicへ修正指示 |
| **Mechanic** | Executor | code-implementation, testing, minimal-changes等 | read, search, editFiles, runInTerminal, problems | *（なし）* | Pit Chiefへ結果報告、Race Directorへ重要判断共有 |

最小権限の原則：

- Mechanicは `agents: []` でサブエージェント起動を禁止
- Mechanicに `fetch` は不要（外部情報取得はRace Director/Pit Chiefが担当）
- Pit Chiefの `agent` はMechanicへの修正指示に限定

### Prompt Files（`.github/prompts/*.prompt.md`）

よく使うワークフローをスラッシュコマンドとして定義し、再現可能にしています。

| Prompt File | 用途 | 対応Agent |
|---|---|---|
| `/create-spec` | 新規仕様作成 | Race Director |
| `/decompose-tasks` | タスク分解 | Pit Chief |
| `/review-request` | レビュー依頼 | Pit Chief |
| `/report-done` | 完了報告 | Mechanic |
| `/escalate` | 上様お伺い | Race Director |

### Handoffs（ワークフロー遷移）

エージェント間の遷移を handoffs で明示化し、ワンクリックで次の工程に移れるようにしています。

```
Race Director ──[Pit Chiefへタスク分解を依頼]──→ Pit Chief
Race Director ──[Pit Chiefへレビューを依頼]──→ Pit Chief
Race Director ──[Mechanicへ実装を委任]──→ Mechanic
Pit Chief   ──[Race Directorへ統合報告]──→ Race Director
Pit Chief   ──[Mechanicへ修正指示]──→ Mechanic
Mechanic ──[Pit Chiefへ結果報告]──→ Pit Chief
Mechanic ──[Race Directorへ重要判断を共有]──→ Race Director
```

### Subagents（並列実行）

Race DirectorはサブエージェントとしてPit Chief・Mechanicを並列起動できます。
各サブエージェントは独立したコンテキストで動作し、最終結果のみをメインに返します。

## 拡張ポイント（プロジェクトに合わせて育てる場所）

- Custom Agents の強化：`.github/agents/` にエージェントを追加（例：テスト専用エージェント）
- Prompt Files の追加：`.github/prompts/` にワークフローを追加
- Instruction の強化：`.github/instructions/` にルールやテンプレを追加
- Spec テンプレの更新：`docs/spec/_template.md` を育てる
- 実行コマンドの整備：`.vscode/tasks.json` に、あなたのプロジェクト固有のコマンドを登録

## 上様（ユーザ）がやること（最小）

上様がやることは3つだけ。それ以外はRace Director/Pit Chief/Mechanicが進めます（詳細は `docs/USAGE.md`）。

1. 依頼を投げる（Copilot Chat で Race Director を選ぶ）
2. 重要判断に答える（Race Directorの「🚨 上様お伺い」へ A/B/C などで回答する）
3. 完了を確認する（`status/dashboard.md` を見て承認する）

## ダッシュボードの見方（`status/dashboard.md`）

### コミュニケーションはユーザが確認できる？

できます。
この運用では、会話ログ（チャット）ではなく **`status/dashboard.md` が"やり取りの要約ログ"** になります。

- Race Director：方針・受け入れ条件（AC）・優先度と、上様お伺い（重要判断）を担当（dashboard は直接編集しない）
- Pit Chief：このファイルの **単一更新者**。start/done/blocked と進捗要点を集約して記録
- Mechanic：実行結果（done/error、再現手順の要点）をPit Chiefへ報告（必要なら `output/` に生成物を残す）

ユーザ（上様）は、`status/dashboard.md` を見れば「誰が・いつ・何を決め/分解し/実行したか」を時系列で追えます。

### 何が書かれる？

- Mechanicの起動（Pit Chiefが要点を転記）
- タスクの start / done / error（作業者の役割名をログ行に含める）
- plan 生成（Pit Chiefの分解結果の要点）

### ログの書式

- 推奨：`[YYYY-MM-DD-HH:MM] <role>: <event>: <topic> (<note>)`
	- **必ず現在時刻（HH:MM）を記録する**こと
	- 時刻をどうしても取得できない場合のみ `00:00` を使用（例外。通常は使わない）

### よくある見方

- `start` が出たのに `done` が出ない：Mechanicが止まっている/タスクが失敗している
- 記録が増えない：Pit Chiefが `status/dashboard.md` を更新できているか確認（詳細ログは `output/` にあるかも）

補足：報告テンプレ（YAML、skill_candidate 等）は `docs/spec/agent-communication-v1.md` を参照。
