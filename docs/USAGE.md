# 使い方（車載ソフトウェア第三者評価 — VS Code + Copilot Agent 運用）

このワークスペースは、**車載ソフトウェア第三者評価業務**を AI 化するための「ファイル運用基盤」です。
VS Code と Copilot Chat（Agent モード）で「将軍/家老/足軽」の役割分担を使って評価業務を進めます。

---

## 準備（VS Code 側で行うこと）

### ✅ インストール直後のチェックリスト

- [ ] VS Code に GitHub Copilot と Copilot Chat が入っている（組織ポリシーに従う）
- [ ] Copilot Chat を開いて **Agent** モードに切り替えられる
- [ ] instruction files が有効（`github.copilot.chat.codeGeneration.useInstructionFiles: true`）
- [ ] ツールピッカーで `runSubagent`（または同等機能）を有効化できる
- [ ]（任意）`chat.customAgentInSubagent.enabled: true` があればON

### instruction files の設定（最小）

VS Code のユーザー設定（JSON）に以下を追加してください。

```jsonc
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true
}
```

参照される instruction files：

- 全体ルール：`.github/copilot-instructions.md`
- 将軍：`.github/instructions/shogun.instructions.md`
- 家老：`.github/instructions/karo.instructions.md`
- 仕様解析（足軽-1）：`.github/instructions/spec-analyzer.instructions.md`
- VT環境（足軽-2）：`.github/instructions/vt-environment.instructions.md`
- テスト仕様書（足軽-3）：`.github/instructions/test-spec.instructions.md`
- テストケース（足軽-4）：`.github/instructions/testcase.instructions.md`
- 結果解析（足軽-5）：`.github/instructions/result-analyzer.instructions.md`
- 報告書（足軽-6）：`.github/instructions/report-writer.instructions.md`

---

## 担当者（上様）の役割：将軍への指示の出し方

あなた（上様）は **手を動かす人ではなく、判断と方向付けを担当** します。
将軍がオーケストレーションを全て行うため、やることは「指示を出す → 判断を返す → 成果物を承認する」の3つだけです。

### 🚀 最短ルート（3ステップ）

```
Step 1: Copilot Chat で Shogun を選択し、評価業務の依頼を投げる
Step 2: 将軍が「お伺い」してきたら A/B/C を選ぶ
Step 3: status/dashboard.md を見て output/ 配下の成果物を承認する
```

### Step 1: 将軍に依頼を投げる

**操作手順:**
1. VS Code で Copilot Chat を開く（`Ctrl+Shift+I` またはサイドバー）
2. チャットモードを **Agent** に切り替える
3. エージェントを **Shogun (Orchestrator)** に選択する
4. 業務別のテンプレート（下記）を参考に依頼を送信する

---

## 業務別の指示テンプレート例

### テスト仕様書作成を依頼する場合

```
以下の製品のテスト仕様書（ドラフト）を作成してほしい。

■ 概要
- 製品: 〈製品名・型番〉
- 対象試験: 非機能試験（ノイズ印加、電源電圧変動）、ユースケース試験
- 参照仕様書: 〈添付ファイル名を列挙〉

■ 制約
- テスト設計仕様書テンプレートの構成に沿うこと
- 第三者評価の視点（ノイズ・電圧変動等の非機能試験重視）で作成すること
- 成果物は output/ 配下に Markdown 形式で出力すること

■ 期待する成果物
- output/spec_summary.md（仕様サマリー）
- output/test_spec_draft.md（テスト仕様書ドラフト）

■ 進め方
1. まず仕様のポイントと試験観点を整理して見せてください
2. 重要判断は私に確認してください
3. タスク分解→並列作成→レビュー→統合の流れで進めてください
```

### テストケース作成を依頼する場合

```
output/test_spec_draft.md のテスト仕様書をもとに、テストケース一覧を作成してほしい。

■ 概要
- テスト設計技法: 境界値分析、同値分割、ユースケース記述を適用すること
- 入力値・期待値・試験手順を明記すること

■ 制約
- vTESTstudio での実装を想定した記述にすること
- 成果物は output/testcase_list.md に出力すること

■ 進め方
1. まずテスト観点の分類方針を見せてください
2. 重要判断は私に確認してください
3. タスク分解→並列作成→レビュー→統合の流れで進めてください
```

### NG解析・報告書作成を依頼する場合

```
テスト実行後のログと CANoe レポートを解析し、試験報告書のドラフトを作成してほしい。

■ 概要
- 添付: CANoe テストレポート（HTML/XML）、ログファイル（BLF/ASC）
- 参照: output/testcase_list.md（実施したテストケース）

■ 成果物
- output/ng_analysis.md（NG解析レポート）
- output/concern_sheet_draft.md（懸念点確認シート）
- output/test_report_draft.md（試験報告書ドラフト）

■ 進め方
1. まず NG の一覧と根本原因候補を整理して見せてください
2. 重要判断は私に確認してください
3. 確認後に報告書ドラフトを生成してください
```

---

## Step 2: 将軍の「お伺い」に答える

将軍は重要判断のたびに「🚨 上様お伺い」として確認を求めてきます：

```
論点: 〈何を決めるか〉
選択肢:
  A: 〈選択肢Aの説明〉
  B: 〈選択肢Bの説明〉
  C: 〈選択肢Cの説明〉
推奨: B
理由: 〈1行〉
リスク: 〈1行〉
```

**返答例:**
- シンプル: `Bで` / `推奨案で`
- 補足付き: `Bで。ただし〇〇は△△にしてほしい`
- 複数一括: `判断1→A、判断2→推奨、判断3→Cで`

> 将軍は回答が来るまで該当作業をブロックするので、早めに返すとスムーズです。

---

## Step 3: 成果物を確認・承認する

将軍が完了報告したら、`status/dashboard.md` でステータスを確認し、`output/` 配下の成果物をレビューします。

| 成果物 | パス | 担当足軽 |
|---|---|---|
| 仕様サマリー | `output/spec_summary.md` | 足軽-1 |
| 信号一覧 | `output/signal_list.md` | 足軽-1 |
| DBCドラフト | `output/dbc_draft.md` | 足軽-2 |
| CAPLスケルトン | `output/capl_skeleton.can` | 足軽-2 |
| テスト仕様書ドラフト | `output/test_spec_draft.md` | 足軽-3 |
| テストケース一覧 | `output/testcase_list.md` | 足軽-4 |
| NG解析レポート | `output/ng_analysis.md` | 足軽-5 |
| 懸念点確認シート | `output/concern_sheet_draft.md` | 足軽-6 |
| 試験報告書 | `output/test_report_draft.md` | 足軽-6 |

> **⚠️ 重要:** `output/` 配下の成果物はすべてAIが生成したドラフトです。
> **人間によるレビュー・承認なしに最終成果物として使用しないでください。**

---

## 仕様書のセットアップ（プロジェクト開始時）

評価業務を開始する前に、以下のテンプレートファイルを更新してください：

| ファイル | 内容 |
|---|---|
| `docs/spec/product_spec.md` | 製品仕様の要点 |
| `docs/spec/communication_spec.md` | 通信仕様（信号定義） |
| `docs/spec/safety_requirements.md` | 機能安全要求（ASIL等） |

> 仕様書ファイル（PDF/Word/Excel）を Copilot Chat に直接添付して使うことも可能です。

---

## うまくいかない時（トラブルシュート）

- まず VS Code / Copilot 拡張を最新版に更新
- 組織管理PCの場合、ポリシーで無効化されていることがあります（管理者への許可申請が必要）
- instruction files が読まれているか確認：`github.copilot.chat.codeGeneration.useInstructionFiles: true`

