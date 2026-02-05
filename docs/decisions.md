# 設計判断ログ（decisions）

このファイルは「なぜその設計にしたか」を短く残すログです。

- いつ：YYYY-MM-DD
- 何を：判断内容
- なぜ：理由
- 代替案：検討した選択肢
- 影響：影響範囲

---

## テンプレ: Kaizen Decision（運用改善の採用判断）

- いつ：YYYY-MM-DD
- 何を：改善点（ナレッジ/手順/テンプレ/ルール変更）
- なぜ：背景・痛み・期待効果
- 代替案：採用しない場合/別案
- 反映先：`docs/spec/` / `docs/USAGE.md` / `.github/instructions/` / `.vscode/tasks.json` など
- 影響：利用者/運用への影響、移行の注意

## 2026-02-05: 実行基盤を「VS Code + ファイル運用」に統一（Python/シェルなし）

- 何を：タスク実行エンジン（Python実装やシェルスクリプト）を内蔵せず、VS Code + Copilot Chat（Agentモード）と Markdown ファイルで運用する
- なぜ：要求「VS Codeの設定と各種ファイル設定のみで実現」「Python/シェル排除」を優先
- 代替案：Node/Pythonで実行エンジンを実装 / bashでキュー処理
- 影響：ドキュメントと instruction を運用の中心にする（`docs/spec/`, `docs/decisions.md`, `status/dashboard.md`）。`.vscode/tasks.json` はプロジェクト固有コマンドの“器”として任意。

## 2026-02-05: 重要判断の上様確認ゲート + ロギング契約 + output/ 生成物制約を採用

- 何を：
	- 重要判断（技術選定、外部依存追加、破壊的変更、運用ルール変更など）は将軍が上様に確認してから確定する
	- ロギング契約を明確化する（Spec/Decisions/Dashboard/Output）
	- 生成物（調査メモ、比較表、検証ログ、ビルド生成物、tmp等）は `output/` 配下に限定する
	- `status/dashboard.md` は（当時）将軍が集約して更新する（単一更新者）
		- 注：後続判断で dashboard の単一更新者は「将軍→家老」へ変更済み（本ファイル内の 2026-02-05: 会話/報告プロトコル（v1）を参照）
- なぜ：
	- 複数エージェントが同一ファイルを編集して競合する事故を避けたい
	- 判断待ちを見失わず、上様が“どこを見ればよいか”を固定したい
	- 生成物がリポジトリ直下に散らばる運用コストを下げたい
- 代替案：
	- 家老/足軽も直接 `status/dashboard.md` を更新する（競合リスクが高い）
	- 生成物を各自の任意フォルダに置く（探索コストが高い）
- 反映先：`docs/spec/agent-governance-v2.md`, `docs/USAGE.md`, `.github/agents/*.agent.md`, `.github/instructions/*.instructions.md`, `status/dashboard.md`, `.gitignore`
- 影響：
	- （当時）家老/足軽は dashboard を直接編集しない（将軍へ要点を返す）
		- 注：後続判断で dashboard の単一更新者は「将軍→家老」へ変更済み。現行は「足軽→家老へ報告、家老が dashboard へ転記」（本ファイル内の 2026-02-05: 会話/報告プロトコル（v1）を参照）
	- `output/` は基本的にGit管理しない（`output/.gitkeep` のみ例外）

## 2026-02-05: 会話/報告プロトコル（v1）を導入し、dashboard単一更新者を家老に変更

- 何を：
	- `docs/spec/agent-communication-v1.md` を追加し、話法（チャットのみ戦国風）・上様お伺いテンプレ・報告YAML（skill_candidate含む）を標準化
	- `status/dashboard.md` の単一更新者を「将軍」から「家老」へ変更
- なぜ：
	- 参考リポ（multi-agent-shogun等）のノウハウ（判断待ち集約、報告フォーマット統一）を取り込み、運用の再現性を上げる
	- dashboard更新を家老に集約することで、タスク分解/進捗把握の責務（SRP）を明確にし、将軍は上様対応と意思決定に集中できる
- 代替案：
	- dashboard更新者は将軍のまま（従来v2の継続）
	- 戦国風口調をdocs/status/outputにも適用（読みやすさ低下の懸念）
- 反映先：`docs/spec/agent-communication-v1.md`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/agents/*.agent.md`, `docs/USAGE.md`, `status/dashboard.md`
- 影響：
	- 将軍/足軽は dashboard を直接編集しない（家老へ報告→家老が転記）
	- 足軽の報告に `skill_candidate` フィールドが追加される（ボトムアップのスキル発見）
