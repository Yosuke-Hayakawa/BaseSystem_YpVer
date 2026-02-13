# アーキテクチャ

## このリポジトリの狙い

Zennの記事で出てくる「将軍→家老→足軽（並列）」の形を、**tmuxなし**かつ **仕様駆動 + SOLID** を意識して小さく再構成します。

このリポジトリは「実行エンジン」を内蔵しません。
代わりに **VS Code + Copilot Chat（Agentモード）** と Markdown ファイルを“運用基盤”として使います。

## どこから読むか（入口）

- 概要（最短）：`README.md`
- 初回準備と、将軍への指示の出し方：`docs/USAGE.md`
- 進捗の見方：`docs/DASHBOARD.md`（実ファイルは `status/dashboard.md`）
- 仕組みの全体像（この文書）：`docs/ARCHITECTURE.md`

## 構成要素（一次情報と生成物）

- Spec：`docs/spec/`（仕様：Intent/Constraints/AC。将軍が確定させる）
- Decisions：`docs/decisions.md`（設計判断ログ：各プロジェクトで使うテンプレ）
- Dashboard：`status/dashboard.md`（進捗とやり取り要点：**家老が単一更新者**）
- Output：`output/`（生成物：調査メモ、比較表、検証ログ、ビルド生成物、tmp 等）
- Instructions：`.github/instructions/*.instructions.md`（役割ごとの振る舞いを固定）
- Tasks（任意）：`.vscode/tasks.json`（あなたのプロジェクトの build/test/lint を並列実行する“器”）

## 運用モデル（役割・フロー・競合回避）

### 役割と責務

- 上様（ユーザ）：方向付けと承認（重要判断への回答、完了の承認）
- 将軍（shogun）：Spec と受け入れ条件（AC）を確定し、重要判断は上様に確認してから進める
- 家老（karo）：Spec をタスクへ分解し、足軽へ配布し、`status/dashboard.md` に進捗を集約（単一更新者）
- 足軽（ashigaru）：自分の担当タスクだけ実行し、要点を家老へ返す（必要なら `output/` に生成物）

### 基本フロー

1. 将軍：`docs/spec/` に Spec（目的/制約/AC）を作る
2. 家老：Spec を読み、並列可能なタスクに分解（競合しない切り方）
3. 足軽：担当タスクを実行（コード編集/レビュー/テスト/調査など）
4. 家老：結果を取りまとめ、`status/dashboard.md` に start/done/error/blocked を集約
5. 上様：判断待ち（`🚨 要対応`）に答え、完了を承認する

会話/報告テンプレ（YAML 等）の詳細は `docs/spec/agent-communication-v1.md` を参照してください。

### 並列化と競合回避

- 足軽は複数起動して並列対応する（担当を分ける）
- 競合回避：同じファイルを複数の足軽が同時に編集しないよう、家老が **ファイル単位**でタスクを切る
- 進捗の同期：会話ログではなく、家老が `status/dashboard.md` に要点を転記して合流する

### ログ/成果物の置き場所

- 一次情報：`docs/spec/`, `docs/decisions.md`, `status/dashboard.md`
- 生成物：`output/` 配下のみ（調査メモ、比較表、検証ログ、ビルド生成物、tmp 等）

## AgentHQ（Custom Agents / Subagents / Prompt Files / Handoffs）

VS Code の Custom Agents 機能を使い、将軍/家老/足軽のオーケストレーションを正式に定義しています。

### Custom Agents（`.github/agents/*.agent.md`）

各エージェントは YAML frontmatter で `skills`（得意領域）、`tools`（使えるツール）、`agents`（起動できるサブエージェント）、`handoffs`（ワークフロー遷移ボタン）を明示的に定義しています。

| Agent | Role | skills | tools | agents | handoffs |
|---|---|---|---|---|---|
| **Shogun** | Orchestrator | orchestration, specification-definition, task-planning等 | read, search, fetch, agent, editFiles, problems | Karo, Ashigaru, Plan | 家老へタスク分解/レビュー依頼、足軽へ実装委任 |
| **Karo** | Reviewer/QA | code-review, quality-assurance, task-decomposition等 | read, search, fetch, editFiles, problems, agent | Ashigaru | 将軍へ統合報告、足軽へ修正指示 |
| **Ashigaru** | Executor | code-implementation, testing, minimal-changes等 | read, search, editFiles, runInTerminal, problems | *（なし）* | 家老へ結果報告、将軍へ重要判断共有 |

最小権限の原則：

- 足軽は `agents: []` でサブエージェント起動を禁止
- 足軽に `fetch` は不要（外部情報取得は将軍/家老が担当）
- 家老の `agent` は足軽への修正指示に限定

### Prompt Files（`.github/prompts/*.prompt.md`）

よく使うワークフローをスラッシュコマンドとして定義し、再現可能にしています。

| Prompt File | 用途 | 対応Agent |
|---|---|---|
| `/create-spec` | 新規仕様作成 | Shogun |
| `/decompose-tasks` | タスク分解 | Karo |
| `/review-request` | レビュー依頼 | Karo |
| `/report-done` | 完了報告 | Ashigaru |
| `/escalate` | 上様お伺い | Shogun |

### Handoffs（ワークフロー遷移）

エージェント間の遷移を handoffs で明示化し、ワンクリックで次の工程に移れるようにしています。

```
Shogun ──[家老へタスク分解を依頼]──→ Karo
Shogun ──[家老へレビューを依頼]──→ Karo
Shogun ──[足軽へ実装を委任]──→ Ashigaru
Karo   ──[将軍へ統合報告]──→ Shogun
Karo   ──[足軽へ修正指示]──→ Ashigaru
Ashigaru ──[家老へ結果報告]──→ Karo
Ashigaru ──[将軍へ重要判断を共有]──→ Shogun
```

### Subagents（並列実行）

将軍はサブエージェントとして家老・足軽を並列起動できます。
各サブエージェントは独立したコンテキストで動作し、最終結果のみをメインに返します。

## 拡張ポイント（プロジェクトに合わせて育てる場所）

- Custom Agents の強化：`.github/agents/` にエージェントを追加（例：テスト専用エージェント）
- Prompt Files の追加：`.github/prompts/` にワークフローを追加
- Instruction の強化：`.github/instructions/` にルールやテンプレを追加
- Spec テンプレの更新：`docs/spec/_template.md` を育てる
- 実行コマンドの整備：`.vscode/tasks.json` に、あなたのプロジェクト固有のコマンドを登録

## 上様（ユーザ）がやること（最小）

上様がやることは3つだけ。それ以外は将軍/家老/足軽が進めます（詳細は `docs/USAGE.md`）。

1. 依頼を投げる（Copilot Chat で Shogun を選ぶ）
2. 重要判断に答える（将軍の「🚨 上様お伺い」へ A/B/C などで回答する）
3. 完了を確認する（`status/dashboard.md` を見て承認する）
