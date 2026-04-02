# multiAgent（Python・シェルなし / 仕様駆動 + SOLID）

添付のまとめ（VS Code + Copilot Agent運用 / 仕様駆動 / SOLID / dashboard）を踏襲し、
**Pythonやシェルスクリプトに依存しない**形で「boss→elite→mob×N（並列）」を運用するためのベース環境です。

## ユーザ向け：最初に押さえる4点

- **ユーザの読むべき部分**：この `README.md` と `docs/USAGE.md`
- **ユーザの準備すべき部分**：`docs/USAGE.md` の「VS Code 側で行うこと（設定）」
- **ユーザが入力する部分**：Copilot Chat（Agentモード）で **boss** に依頼（テンプレは `docs/USAGE.md`）
- **ユーザが監視する部分**：`status/dashboard.md`（見方の説明は `docs/ARCHITECTURE.md`）

## 概念図（この環境が提供するもの）

```mermaid
flowchart TB
	U[ユーザ\n意思決定・方向付け] -->|指示/AC/優先度| S[boss\n仕様確定・判断]
	S -->|タスク分解を依頼| K[elite\n分解・調整・取りまとめ]
	K -->|担当割当| A1[mob（No.1）\n担当のみ実行]
	K -->|担当割当| A2[mob（No.2）\n担当のみ実行]
	A1 -->|結果/要点を報告| K
	A2 -->|結果/要点を報告| K
	K -->|分解案/レビューを報告| S

	subgraph Files[ファイル（真実のソース）]
		SPEC[docs/spec/\n仕様（Intent/Constraints/AC）]
		DEC[docs/decisions.md\n設計判断ログ]
		DASH[status/dashboard.md\n進捗・結果]
		OUT[output/\n生成物（調査メモ/検証ログ等）]
		INS[.github/instructions/\n役割ごとのルール]
	end

	S <--> SPEC
	K <--> SPEC
	S <--> DEC
	K <--> DEC
	K <--> DASH
	K --> OUT
	A1 --> OUT
	A2 --> OUT
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
- `output/` に生成物（調査メモ、検証ログ、ビルド生成物など）を集約
- VS Code の `tasks.json` で、タスク（例：ビルド/解析/テスト）を **並列実行**

## 主要ファイル

- `.github/copilot-instructions.md`：全体ルール（仕様駆動/ SOLID / 小さく変更 / docs更新）
- `.github/instructions/`：用途別ルール（boss/elite/mob/ドキュメント）
- `docs/spec/`：仕様（Markdown）
- `docs/decisions.md`：設計判断ログ
- `status/dashboard.md`：進捗ダッシュボード
- `output/`：生成物置き場（Git管理しないのが基本）
- `.vscode/tasks.json`：並列実行の要

## クイックスタート（ユーザ向け）

**初回セットアップ（1回だけ）:**

- VS Code の前提設定は `docs/USAGE.md` を参照（Agent / instruction files / runSubagent）

**タスクの依頼方法（毎回）:**

1. Copilot Chat でエージェントを **boss** に切り替え
2. やりたいことを自然言語で指示（テンプレートは `docs/USAGE.md` 参照）
3. bossが「お伺い」してきたら選択肢を選ぶ
4. `status/dashboard.md` で進捗を確認

> 詳しくは `docs/USAGE.md` の「ユーザの役割：bossへの指示の出し方」を参照。

## 使い方（詳細）

`docs/USAGE.md` を参照。

## VS Code側の前提（入口）

このリポジトリは、VS Code の Copilot Chat（Agentモード）を前提にした“運用基盤”です。
具体的な設定手順は `docs/USAGE.md` に集約しています（README では重複を避けます）。

