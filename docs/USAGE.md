# 使い方（車載ソフトウェア第三者評価 — VS Code + Copilot Agent 運用）

このワークスペースは、**車載ソフトウェア第三者評価業務**を AI 化するための「ファイル運用基盤」です。
VS Code と Copilot Chat（Agent モード）で「Race Director/Pit Chief/Mechanic」の役割分担を使って評価業務を進めます。

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
- Race Director：`.github/instructions/race-director.instructions.md`
- Pit Chief：`.github/instructions/pit-chief.instructions.md`
- 仕様解析（Mechanic-1）：`.github/instructions/spec-analyzer.instructions.md`
- VT環境（Mechanic-2）：`.github/instructions/vt-environment.instructions.md`
- テスト仕様書（Mechanic-3）：`.github/instructions/test-spec.instructions.md`
- テストケース（Mechanic-4）：`.github/instructions/testcase.instructions.md`
- 結果解析（Mechanic-5）：`.github/instructions/result-analyzer.instructions.md`
- 報告書（Mechanic-6）：`.github/instructions/report-writer.instructions.md`

---

## 担当者（チームオーナー）の役割：Race Directorへの指示の出し方

あなた（チームオーナー）は **手を動かす人ではなく、判断と方向付けを担当** します。
Race Directorがオーケストレーションを全て行うため、やることは「指示を出す → 判断を返す → 成果物を承認する」の3つだけです。

### 🚀 最短ルート（3ステップ）

```
Step 1: Copilot Chat で Race Director を選択し、評価業務の依頼を投げる
Step 2: Race Directorが「お伺い」してきたら A/B/C を選ぶ
Step 3: status/dashboard.md を見て output/ 配下の成果物を承認する
```

### Step 1: Race Directorに依頼を投げる

**操作手順:**
1. VS Code で Copilot Chat を開く（`Ctrl+Shift+I` またはサイドバー）
2. チャットモードを **Agent** に切り替える
3. エージェントを **Race Director (Orchestrator)** に選択する
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

## Step 2: Race Directorの「お伺い」に答える

Race Directorは重要判断のたびに「🚨 チームオーナーお伺い」として確認を求めてきます：

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

> Race Directorは回答が来るまで該当作業をブロックするので、早めに返すとスムーズです。

---

## Step 3: 成果物を確認・承認する

Race Directorが完了報告したら、`status/dashboard.md` でステータスを確認し、`output/` 配下の成果物をレビューします。

| 成果物 | パス | 担当Mechanic |
|---|---|---|
| 仕様サマリー | `output/spec_summary.md` | Mechanic-1 |
| 信号一覧 | `output/signal_list.md` | Mechanic-1 |
| DBCドラフト | `output/dbc_draft.md` | Mechanic-2 |
| CAPLスケルトン | `output/capl_skeleton.can` | Mechanic-2 |
| テスト仕様書ドラフト | `output/test_spec_draft.md` | Mechanic-3 |
| テストケース一覧 | `output/testcase_list.md` | Mechanic-4 |
| NG解析レポート | `output/ng_analysis.md` | Mechanic-5 |
| 懸念点確認シート | `output/concern_sheet_draft.md` | Mechanic-6 |
| 試験報告書 | `output/test_report_draft.md` | Mechanic-6 |

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

## Python 仮想環境のセットアップ（xlsx / xlsm / pdf / docx / pptx 読み取り）

仕様書が `.xlsx`・`.xlsm`・`.pdf`・`.docx`・`.pptx` 形式の場合、`tools/spec_to_md.py` で Markdown へ変換してから
エージェントに渡します。初回のみ以下の手順で環境を構築してください。

### 前提

- Python 3.10 以上がインストールされていること（`python --version` で確認）

### セットアップ手順（1 回だけ）

```powershell
# リポジトリのルートで実行
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

または VS Code のタスクから実行できます：

> **ターミナル → タスクの実行 → `Python: セットアップ（仮想環境作成）`**

### 仕様書を Markdown へ変換する

```powershell
# 仮想環境が有効な状態で実行
.venv\Scripts\python tools/spec_to_md.py docs/spec/03_仕様書/product_spec.xlsx    # Excel
.venv\Scripts\python tools/spec_to_md.py docs/spec/03_仕様書/product_spec.xlsm    # マクロ付き Excel（マクロは実行せず読み取りのみ）
.venv\Scripts\python tools/spec_to_md.py docs/spec/03_仕様書/product_spec.pdf     # PDF
.venv\Scripts\python tools/spec_to_md.py docs/spec/03_仕様書/product_spec.docx    # Word
.venv\Scripts\python tools/spec_to_md.py docs/spec/03_仕様書/product_spec.pptx    # PowerPoint
```

または VS Code のタスクから：

> **ターミナル → タスクの実行 → `Spec: 仕様書→Markdown変換`**
> （ファイルパスと出力先を対話入力します）

**各形式の動作**

| 拡張子 | 抽出内容 | 備考 |
|---|---|---|
| `.xlsx` | 全シートをテーブル形式で抽出 | シートごとに `##` 見出しを付与 |
| `.xlsm` | マクロ付き Excel。マクロは実行せずデータのみ読み取り | `.xlsx` と同一の出力 |
| `.pdf` | ページごとにテキスト・テーブルを抽出 | 画像埋め込み PDF はテキスト無し |
| `.docx` | 見出し・段落・テーブルを Markdown に変換 | 見出しスタイルは日英両対応 |
| `.pptx` | スライドごとにタイトル・本文・テーブルを抽出 | 画像・図形は非対応 |

変換後のファイルは `docs/spec/<元ファイル名>.md`（デフォルト）または `--out` で指定したディレクトリに出力されます。
その後、Race Director へ「`docs/spec/product_spec.md` を参照して…」と依頼するだけです。

### インストールされるライブラリ

| ライブラリ | 用途 |
|---|---|
| `openpyxl` | `.xlsx` / `.xlsm` シート読み取り |
| `pdfplumber` | `.pdf` テキスト・テーブル抽出 |
| `python-docx` | `.docx` 見出し・段落・テーブル抽出 |
| `python-pptx` | `.pptx` スライド・テキスト・テーブル抽出 |
| `pandas` | xlsx/xlsm の後続データ解析・集計用 |

> `.venv/` は `.gitignore` で除外済みです。各メンバーがローカルで `pip install` を実行してください。

---

## うまくいかない時（トラブルシュート）

- まず VS Code / Copilot 拡張を最新版に更新
- 組織管理PCの場合、ポリシーで無効化されていることがあります（管理者への許可申請が必要）
- instruction files が読まれているか確認：`github.copilot.chat.codeGeneration.useInstructionFiles: true`

### pip インストール時にプロキシが必要な場合

ネットワークがプロキシ経由の環境の場合、次のいずれかの方法でインストールしてください。

**方法1：VS Code タスクを使う（推奨）**

> **ターミナル → タスクの実行 → `Python: セットアップ（プロキシ経由）`**

**方法2：ターミナルで手動実行**

```powershell
python -m venv .venv
.venv\Scripts\pip install --proxy http://192.168.14.55:8080 -r requirements.txt
```

**方法3：環境変数で永続設定（セッション内有効）**

```powershell
$env:https_proxy = "http://192.168.14.55:8080"
$env:http_proxy  = "http://192.168.14.55:8080"
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

> プロキシアドレスが変わった場合は `tasks.json` の `Python: セットアップ（プロキシ経由）` のコマンド内の IP アドレスを更新してください。

