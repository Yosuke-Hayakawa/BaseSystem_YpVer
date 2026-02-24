# 履歴（このテンプレートリポジトリ自身）

このファイルは、このテンプレートリポジトリ（shogun）の変更履歴・判断履歴を残すためのものです。

- 利用者がテンプレートとして使用する際、`docs/decisions.md` は各プロジェクトの設計判断ログとして使えるよう **テンプレ化**します。
- テンプレート側の履歴（いつ何を決めたか）は、この `docs/history.md` に退避します。

---

## 設計判断ログ（archive）

### 2026-02-05: 実行基盤を「VS Code + ファイル運用」に統一（Python/シェルなし）

- 何を：タスク実行エンジン（Python実装やシェルスクリプト）を内蔵せず、VS Code + Copilot Chat（Agentモード）と Markdown ファイルで運用する
- なぜ：要求「VS Codeの設定と各種ファイル設定のみで実現」「Python/シェル排除」を優先
- 代替案：Node/Pythonで実行エンジンを実装 / bashでキュー処理
- 影響：ドキュメントと instruction を運用の中心にする（`docs/spec/`, `docs/decisions.md`, `status/dashboard.md`）。`.vscode/tasks.json` はプロジェクト固有コマンドの“器”として任意。

### 2026-02-05: 重要判断の上様確認ゲート + ロギング契約 + output/ 生成物制約を採用

- 何を：
	- 重要判断（技術選定、外部依存追加、破壊的変更、運用ルール変更など）は将軍が上様に確認してから確定する
	- ロギング契約を明確化する（Spec/Decisions/Dashboard/Output）
	- 生成物（調査メモ、比較表、検証ログ、ビルド生成物、tmp等）は `output/` 配下に限定する
	- `status/dashboard.md` は（当時）将軍が集約して更新する（単一更新者）
		- 注：後続判断で dashboard の単一更新者は「将軍→家老」へ変更済み
- なぜ：
	- 複数エージェントが同一ファイルを編集して競合する事故を避けたい
	- 判断待ちを見失わず、上様が“どこを見ればよいか”を固定したい
	- 生成物がリポジトリ直下に散らばる運用コストを下げたい
- 代替案：
	- 家老/足軽も直接 `status/dashboard.md` を更新する（競合リスクが高い）
	- 生成物を各自の任意フォルダに置く（探索コストが高い）
- 反映先：`docs/spec/agent-governance-v2.md`, `docs/USAGE.md`, `.github/agents/*.agent.md`, `.github/instructions/*.instructions.md`, `status/dashboard.md`, `.gitignore`
- 影響：
	- `output/` は基本的にGit管理しない（`output/.gitkeep` のみ例外）

### 2026-02-05: 会話/報告プロトコル（v1）を導入し、dashboard単一更新者を家老に変更

- 何を：
	- `docs/spec/agent-communication-v1.md` を追加し、話法（チャットのみ戦国風）・上様お伺いテンプレ・報告YAML（skill_candidate含む）を標準化
	- `status/dashboard.md` の単一更新者を「将軍」から「家老」へ変更
- なぜ：
	- 判断待ち集約、報告フォーマット統一により運用の再現性を上げる
	- dashboard更新を家老に集約し、将軍は上様対応と意思決定に集中できる
- 代替案：
	- dashboard更新者は将軍のまま
- 反映先：`docs/spec/agent-communication-v1.md`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/agents/*.agent.md`, `docs/USAGE.md`, `status/dashboard.md`
- 影響：
	- 将軍/足軽は dashboard を直接編集しない（家老へ報告→家老が転記）
	- 足軽の報告に `skill_candidate` フィールドが追加

### 2026-02-09: AgentHQ移行（Custom Agents / Subagents / Prompt Files / Handoffs）

- 何を：
	- `.github/agents/*.agent.md` の YAML frontmatter に `tools` / `agents` / `handoffs` を追加
	- `.github/prompts/*.prompt.md` を作成（create-spec, decompose-tasks, review-request, report-done, escalate）
	- Handoffs でエージェント間のワークフロー遷移を明示化
	- 足軽は `agents: []` でサブエージェント起動を禁止
- なぜ：
	- VS Code の Custom Agents 機能に正式対応し、ワークフローの再現性を上げる
- 代替案：
	- 現状維持
- 反映先：`.github/agents/*.agent.md`, `.github/prompts/*.prompt.md`, `docs/ARCHITECTURE.md`, `docs/USAGE.md`, `docs/spec/agenthq-migration-v1.md`, `status/dashboard.md`
- 影響：
	- スラッシュコマンドや handoffs により操作性が改善

### 2026-02-09: dashboard の運用/ひな形/履歴を分離し、ログ時刻を `YYYY-MM-DD-HH:MM` に統一

- 何を：
	- `status/dashboard.md` を実運用の最小構成に整理
	- 記入ガイドを `status/dashboard.template.md` に分離
	- テンプレートリポ自身の過去ログを `status/dashboard.history.md` に退避
	- ログ書式を `YYYY-MM-DD-HH:MM`（分単位）に統一（時刻不明は `00:00`）
- なぜ：
	- テンプレとしてのノイズ（例/履歴/説明の混在）を減らし、運用開始時に迷わない導線にする
- 代替案：
	- `status/dashboard.md` に説明/履歴/例を同居させる（将来の追記が読みにくくなる）
- 反映先：`status/dashboard.md`, `status/dashboard.template.md`, `status/dashboard.history.md`, `docs/DASHBOARD.md`
- 影響：
	- 上様（ユーザ）は `status/dashboard.md` を主に監視し、必要に応じて template/history を参照する

### 2026-02-09: `docs/USAGE.md` を「準備 → 将軍への指示」中心に最小化（認知負荷低減）

- 何を：
	- `docs/USAGE.md` の補足（運用フロー、生成物、VS Code Tasks 等）を削減し、最短導線に寄せた
	- 補足情報は `docs/ARCHITECTURE.md` に集約した
- なぜ：
	- 初見ユーザが読む量を減らし、次に何をすればよいか（準備→依頼）を迷わないようにする
- 代替案：
	- `docs/USAGE.md` に詳細説明を同居させる（理解には良いが、初見時の負荷が高い）
- 反映先：`docs/USAGE.md`, `docs/ARCHITECTURE.md`
- 影響：
	- 初見ユーザは `docs/USAGE.md` を上から読めば開始でき、詳細は必要時に `docs/ARCHITECTURE.md` へ移動する

### 2026-02-13: Custom Agent 定義（`.agent.md`）に `skills` フィールドを追加

- 何を：Custom Agent 定義（`.agent.md`）に `skills` フィールドを追加
- なぜ：GitHub Copilot の Custom Agents 機能において、各エージェントの得意領域（skills）を明示することで、タスクルーティングの精度向上と、エージェント選択時の可視性向上が期待される。Qiita 記事などのベストプラクティスに基づき、標準的な agent.md 形式に準拠する。
- 代替案：
	- skills フィールドなし：エージェント選択が description のみに依存し、機械的なルーティングが困難
	- skills を description に統合：人間の可読性は向上するが、構造化された情報が失われる
- 反映先：
	- `.github/agents/shogun.agent.md`
	- `.github/agents/karo.agent.md`
	- `.github/agents/ashigaru.agent.md`
	- `docs/spec/agenthq-migration-v1.md`（受け入れ条件に skills を追記）
	- `docs/ARCHITECTURE.md`（Custom Agents の表に skills を追記）
- 影響：
	- 既存のエージェント動作には影響なし（skills は追加情報）
	- 将来的なタスク自動割り当て機能で活用可能
	- エージェント選択時の UI で skills が表示される可能性あり

### 2026-02-24: ドキュメント構成の見直し（重複削除 + 整理）

- 何を：
	- `docs/DASHBOARD.md`（薄いラッパーファイル）を削除し、内容を `docs/ARCHITECTURE.md` の「ダッシュボードの見方」セクションへ統合
	- `status/dashboard.template.md` の重複セクション（コミュニケーションの見え方）を削除し、`docs/ARCHITECTURE.md` へ参照を統一
	- `docs/decisions.md` のテンプレートリポ固有エントリ（skills フィールド）を `docs/history.md` へ移動し、`docs/decisions.md` を利用プロジェクト向けの純粋なテンプレートに整理
- なぜ：
	- 同じ内容が複数ファイルに散在し、どれが正しい情報か判断しにくかった
	- `docs/decisions.md` にテンプレートリポ自身の履歴が混在していた（利用者が誤読するリスク）
	- ファイル数を減らして「どこを見ればよいか」を明確にする
- 代替案：
	- `docs/DASHBOARD.md` を残し、内容を補充する：ファイル数が増え、参照先が分散する
- 反映先：`docs/ARCHITECTURE.md`, `docs/decisions.md`, `docs/history.md`, `status/dashboard.md`, `status/dashboard.template.md`, `README.md`
- 影響：
	- `docs/DASHBOARD.md` は存在しなくなる（旧リンクは `docs/ARCHITECTURE.md` へ読み替える）

---

## メモ

- ドキュメントの改善やIssue対応など、プロジェクト運用上の履歴が増える場合も、このファイルに追記します。
