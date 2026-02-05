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

## 拡張ポイント

- Instruction の強化：`.github/instructions/` にルールやテンプレを追加
- Spec テンプレの更新：`docs/spec/_template.md` を育てる
- 実行コマンドの整備：`.vscode/tasks.json` に、あなたのプロジェクト固有のコマンドを登録

