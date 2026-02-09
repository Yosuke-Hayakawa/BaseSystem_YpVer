# 使い方（VS Code + Copilot Agent運用）

このワークスペースは、添付のまとめにある通り、
**VS Code と Copilot Chat（Agentモード）**で「仕様駆動」「SOLID」「役割分担（将軍/家老/足軽）」「進捗可視化」を回すための “ファイル運用基盤” です。

並列実行は「VS Code Tasksで複数ターミナルを同時起動」する発想を踏襲しますが、
実際の実行コマンドはあなたのプロジェクト（例：組込みCのbuild/test/lint）に合わせて設定してください。

## 準備（VS Code 側で行うこと）

このリポジトリ側で設定を自動でONにはできません（VS Code のユーザー設定領域のため）。
ただし、以下が揃えば運用（将軍/家老/足軽 + Subagents）が成立します。

### ✅ クローン直後のチェックリスト（まずここだけ）

- [ ] VS Code に GitHub Copilot と Copilot Chat が入っている（組織ポリシーに従う）
- [ ] Copilot Chat を開いて **Agent** モードに切り替えられる
- [ ] instruction files が有効（`github.copilot.chat.codeGeneration.useInstructionFiles: true`）
- [ ] ツールピッカーで `runSubagent`（または同等機能）を有効化できる
- [ ]（任意）`chat.customAgentInSubagent.enabled: true` があればON（サブエージェントにカスタムエージェント割当）

> もし詰まったら：まず「instruction files が有効か」「Agent モードになっているか」だけ確認すると復帰しやすいです。

### うまくいかない時（最小）

- まず VS Code / Copilot 拡張を最新版に更新
- 組織管理PCの場合、ポリシーで無効化されていることがあります（その場合は管理者側の許可が必要）

### instruction files の設定（最小）

VS Code のユーザー設定（JSON）に、以下が入っていればOKです。

```jsonc
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true
}
```

メモ：このワークスペースで参照される instruction files は以下です。

- 全体：`.github/copilot-instructions.md`
- 役割別：`.github/instructions/*.instructions.md`

### Subagents（サブエージェント）を使う（最小）

- Copilot Chat のツールピッカーで `runSubagent`（または同等のサブエージェント起動ツール）を有効化します。
- 可能なら設定（実験的）：
	- `chat.customAgentInSubagent.enabled: true`（サブエージェントにカスタムエージェントを割り当てる）

手順（`runSubagent` を有効化）：

1. Copilot Chat を開く
2. モードを **Agent** に切り替える
3. チャット入力欄の近くにある「ツール（Tools）/ ツールピッカー」を開く
4. `runSubagent`（または Subagent 相当）を探して有効化する

手順（任意：サブエージェントにカスタムエージェントを割り当てられるようにする）：

1. VS Code の設定を開く（Windows: `Ctrl + ,`）
2. 「設定（JSON）」を開く
3. 以下を追加/確認する

    ```jsonc
    {
      "chat.customAgentInSubagent.enabled": true
    }
    ```

補足（スラッシュコマンド、エージェント一覧、運用フロー、生成物/Tasksの考え方など）は `docs/ARCHITECTURE.md` にまとめます。

## 上様（ユーザ）の役割：将軍への指示の出し方

あなた（上様）は **手を動かす人ではなく、判断と方向付けを担当** します。
将軍がオーケストレーションを全て行うため、あなたがやることは「指示を出す → 判断を返す → 完了を承認する」の3つだけです。

### 🚀 最短ルート（3ステップ）

```
Step 1: Copilot Chat で Shogun を選択し、依頼を投げる
Step 2: 将軍が「お伺い」してきたら A/B/C を選ぶ
Step 3: 将軍が完了報告してきたら dashboard を見て承認する
```

### Step 1: 将軍に依頼を投げる

**操作手順:**
1. VS Code で Copilot Chat を開く（`Ctrl+Shift+I` or サイドバー）
2. チャットモードを **Agent** に切り替える（チャット入力欄の左上ドロップダウン）
3. エージェントを **Shogun (Orchestrator)** に切り替える（エージェントドロップダウン）
4. 以下のテンプレートに沿って依頼を入力し、送信する

**指示テンプレート（将軍宛・コピペ用）:**

```
以下の〈やりたいこと〉を作成/実装してほしい。

■ 概要
- 〈何を・どういう技術で〉
- ビルド環境: 〈例: GCC, CMake, etc.〉
- テスト: 〈例: GoogleTest, Unity, pytest, etc.〉

■ 制約
- 〈守るべきアーキテクチャ: 例 Port/Adapter, SOLID〉
- 〈使わないもの: 例 外部ライブラリ禁止〉
- 〈成果物の場所: 例 output/ 配下〉

■ 期待する成果物
- 〈ファイル or ディレクトリの一覧〉

■ 進め方
1. まず仕様(Spec)とACを作成して見せてください
2. 重要判断は私に確認してください
3. タスク分解→並列実装→レビュー→統合の流れで進めてください
```

> **ポイント:** 「■ 進め方」の3行は毎回そのままコピーで OK。将軍が自動的に Spec→Plan→Tasks→Run→Review のフローに乗せます。

### Step 2: 将軍の「お伺い」に答える

将軍は重要判断のたびに「🚨 上様お伺い」として以下の形式で確認を求めてきます:

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

**あなたの返答例:**
- シンプル: `Bで` / `推奨案で`
- 補足付き: `Bで。ただし〇〇は△△にしてほしい`
- 複数一括: `判断1→A、判断2→推奨、判断3→Cで`

> 将軍は回答が来るまで該当作業をブロックするので、早めに返すとスムーズです。

### Step 3: 完了を確認する

将軍が完了報告したら、`status/dashboard.md` を見て「何が終わったか」「判断待ちが残っていないか」を確認します。

補足：運用全体像や参考情報（生成物の置き場所、VS Code Tasks 等）は `docs/ARCHITECTURE.md` を参照してください。

