# multiAgent（Python・シェルなし / 仕様駆動 + SOLID）

添付のまとめ（VS Code + Copilot Agent運用 / 仕様駆動 / SOLID / dashboard）を踏襲し、
**Pythonやシェルスクリプトに依存しない**形で「将軍→家老→足軽×N（並列）」を運用するためのベース環境です。

## 概念図（この環境が提供するもの）

```mermaid
flowchart TB
	U[上様（ユーザ）\n意思決定・方向付け] -->|指示/AC/優先度| S[将軍（shogun）\n仕様確定・判断]
	S -->|タスク分解を依頼| K[家老（karo）\n分解・調整・取りまとめ]
	K -->|担当割当| A1[足軽（ashigaru-1）\n担当のみ実行]
	K -->|担当割当| A2[足軽（ashigaru-2）\n担当のみ実行]

	subgraph Files[ファイル（真実のソース）]
		SPEC[docs/spec/\n仕様（Intent/Constraints/AC）]
		DEC[docs/decisions.md\n設計判断ログ]
		DASH[status/dashboard.md\n進捗・結果]
		INS[.github/instructions/\n役割ごとのルール]
	end

	S <--> SPEC
	K <--> SPEC
	S <--> DEC
	K <--> DEC
	S <--> DASH
	K <--> DASH
	A1 -->|done/error を記録| DASH
	A2 -->|done/error を記録| DASH
	S --> INS
	K --> INS
	A1 --> INS
	A2 --> INS

	subgraph Optional[任意（プロジェクトに合わせて設定）]
		T[.vscode/tasks.json\nビルド/解析/テスト等の器]
	end
	A1 -. 実行 .-> T
	A2 -. 実行 .-> T
```

## ここでやること

- `.github/copilot-instructions.md` と `.github/instructions/*.instructions.md` にルールを集約
- `docs/spec/` に仕様を Markdown で残す
- `docs/decisions.md` に設計判断を残す
- `status/dashboard.md` で進捗可視化
- VS Code の `tasks.json` で、タスク（例：ビルド/解析/テスト）を **並列実行**

## 主要ファイル

- `.github/copilot-instructions.md`：全体ルール（仕様駆動/ SOLID / 小さく変更 / docs更新）
- `.github/instructions/`：用途別ルール（将軍/家老/足軽/ドキュメント）
- `docs/spec/`：仕様（Markdown）
- `docs/decisions.md`：設計判断ログ
- `status/dashboard.md`：進捗ダッシュボード
- `.vscode/tasks.json`：並列実行の要

## 使い方

`docs/USAGE.md` を参照。

## VS Code側の前提（これだけ設定）

このリポジトリは、VS Code の Copilot Chat を前提にした“運用基盤”です（リポジトリ側から設定を強制はできません）。

- Copilot Chat を **Agent** モードで使う
- instruction files を有効化
	- `github.copilot.chat.codeGeneration.useInstructionFiles: true`
- Subagents を使う（ツールピッカーで `runSubagent` を有効化）
	- 可能なら `chat.customAgentInSubagent.enabled: true`

