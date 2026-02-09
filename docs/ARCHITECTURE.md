# アーキテクチャ

## 目的

Zennの記事で出てくる「将軍→家老→足軽（並列）」の形を、
**tmuxなし**かつ **仕様駆動 + SOLID** を意識して、小さく再構成します。

## 主要コンポーネント

このリポジトリは「実行エンジン」を内蔵しません。
代わりに、VS Code + Copilot Chat（Agentモード）と Markdown ファイルを“基盤”として使います。

- Spec：`docs/spec/`（将軍が intent/constraints/AC を確定させる）
- Decisions：`docs/decisions.md`（設計判断を残す）
- Dashboard：`status/dashboard.md`（進捗と結果を残す）
- Output：`output/`（調査メモ、比較表、検証ログ、ビルド生成物などの生成物を集約）
- Instructions：`.github/instructions/*.instructions.md`（役割ごとの振る舞いを固定）
- Tasks（任意）：`.vscode/tasks.json`（あなたのプロジェクトの build/test/lint 等を並列実行する“器”）

## 並列化

- 足軽を複数起動して並列対応（Copilot Chat の Agent を複数走らせる/担当を分ける）
- 競合回避：同じファイルを複数の足軽が同時に編集しないよう、家老がタスクを分割
- 進捗の“同期”：家老が `status/dashboard.md` に start/done/error を集約して合流（単一更新者）

## AgentHQ（Custom Agents / Subagents / Prompt Files / Handoffs）

VS Code の Custom Agents 機能を使い、将軍/家老/足軽のオーケストレーションを正式に定義しています。

### Custom Agents（`.github/agents/*.agent.md`）

各エージェントは YAML frontmatter で `tools`（使えるツール）、`agents`（起動できるサブエージェント）、`handoffs`（ワークフロー遷移ボタン）を明示的に定義しています。

| Agent | Role | tools | agents | handoffs |
|---|---|---|---|---|
| **Shogun** | Orchestrator | read, search, fetch, agent, editFiles, problems | Karo, Ashigaru, Plan | 家老へタスク分解/レビュー依頼、足軽へ実装委任 |
| **Karo** | Reviewer/QA | read, search, fetch, editFiles, problems, agent | Ashigaru | 将軍へ統合報告、足軽へ修正指示 |
| **Ashigaru** | Executor | read, search, editFiles, runInTerminal, problems | *（なし）* | 家老へ結果報告、将軍へ重要判断共有 |

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

将軍は `agent` ツールを使って家老・足軽をサブエージェントとして並列起動できます。
各サブエージェントは独立したコンテキストウィンドウで動作し、最終結果のみをメインエージェントに返します。

## 拡張ポイント

- Custom Agents の強化：`.github/agents/` にエージェントを追加（例：テスト専用エージェント）
- Prompt Files の追加：`.github/prompts/` にワークフローを追加
- Instruction の強化：`.github/instructions/` にルールやテンプレを追加
- Spec テンプレの更新：`docs/spec/_template.md` を育てる
- 実行コマンドの整備：`.vscode/tasks.json` に、あなたのプロジェクト固有のコマンドを登録

## 上様（ユーザ）の介入ポイント

上様がやることは3つだけ。それ以外は将軍/家老/足軽が自動で処理します。

```
上様（ユーザ）

  ① 依頼を投げる ──→ Shogun（将軍）
                         │
  ② お伺いに答える ←── 将軍「技術選定/ディレクトリ構成は A or B?」
                         │
                         ├─→ Karo（家老）──→ タスク分解 / レビュー
                         │                     │
                         ├─→ Ashigaru×N ──→ 並列実装 / テスト
                         │
  ③ 完了を確認する ←── 将軍「差分要約 / 残課題 / ビルド手順」
                         │
                     dashboard.md で進捗を可視化
```

- **①と②はチャット上で行う**（Copilot Chat の Shogun エージェント宛）
- **③は `status/dashboard.md` で確認**
- 詳細手順は `docs/USAGE.md` の「上様（ユーザ）の役割」を参照

