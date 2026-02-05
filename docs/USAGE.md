# 使い方（VS Code + Copilot Agent運用）

このワークスペースは、添付のまとめにある通り、
**VS Code と Copilot Chat（Agentモード）**で「仕様駆動」「SOLID」「役割分担（将軍/家老/足軽）」「進捗可視化」を回すための “ファイル運用基盤” です。

並列実行は「VS Code Tasksで複数ターミナルを同時起動」する発想を踏襲しますが、
実際の実行コマンドはあなたのプロジェクト（例：組込みCのbuild/test/lint）に合わせて設定してください。

## ゴール

- Spec（仕様）→ Plan（分解）→ Tasks（並列）→ Dashboard（進捗）の流れを、ファイルで運用する
- docs/spec・docs/decisions・status/dashboard が常に更新される

## VS Code 側で行うこと（設定）

このリポジトリ側で「設定を自動でON」にすることはできません（VS Code のユーザー設定領域のため）。
ただし、ここに挙げる3点が揃えば、このワークスペースの運用（将軍/家老/足軽 + Subagents）が成立します。

### ✅ クローン直後のチェックリスト（まずここだけ）

- [ ] VS Code に GitHub Copilot と Copilot Chat が入っている（組織ポリシーに従う）
- [ ] Copilot Chat を開いて **Agent** モードに切り替えられる
- [ ] instruction files が有効（`github.copilot.chat.codeGeneration.useInstructionFiles: true`）
- [ ] ツールピッカーで `runSubagent`（または同等機能）を有効化できる
- [ ]（任意）`chat.customAgentInSubagent.enabled: true` があればON（サブエージェントにカスタムエージェント割当）

> もし詰まったら：まず「instruction files が有効か」「Agent モードになっているか」だけ確認すると復帰しやすいです。

### うまくいかない時（特に Subagents が見つからない時）

- VS Code のバージョン差で、設定名やUIが変わることがあります。
- `runSubagent` がツールピッカーに出ない場合は、まず **VS Code を最新版へアップデート**してから再確認してください（段階配布/実験機能の可能性があります）。
- 組織管理PCの場合、ポリシーで無効化されていることがあります。その場合は管理者側の許可が必要です。

### 1) Copilot Chat の Agent を有効化

- Copilot Chat を開き、モードを **Agent** に切り替えて利用します。

### 2) Instruction files（カスタム指示ファイル）を使う

- VS Code 設定で instruction files の利用を有効化します。
	- `github.copilot.chat.codeGeneration.useInstructionFiles: true`

手順（おすすめ）：

1. VS Code の設定を開く（Windows: `Ctrl + ,`）
2. 右上の「設定（JSON）を開く」（`{}` アイコン）を押す
3. 以下を追加/確認する

		```jsonc
		{
			"github.copilot.chat.codeGeneration.useInstructionFiles": true
		}
		```

#### ✅ 確認（設定できているか）

「設定したつもりだけど効いてるか不安」問題は、まず **設定値** を見に行くのが確実です。

1. コマンドパレットを開く（Windows: `Ctrl + Shift + P`）
2. `Preferences: Open Settings (JSON)` もしくは `Preferences: Open User Settings (JSON)` を開く
3. 以下が `true` になっていることを確認する

	```jsonc
	{
		"github.copilot.chat.codeGeneration.useInstructionFiles": true
	}
	```

> 注意：Settings には「User / Workspace」などのスコープがあります。
> Workspace 側の `.vscode/settings.json` に書いてもよいですが、本リポジトリは“自動ON”を前提にしないため、まずは User 側での有効化を推奨します。

#### ✅ 確認（実際に効いているか・動作チェック）

設定値が `true` でも、拡張/機能の状態次第で体感が薄いことがあります。
Copilot Chat（Agent）に次を聞いて、**具体ファイル名が出る**なら概ねOKです。

- 質問例：
	- 「このワークスペースで参照すべき instruction files のパスを列挙して」
	- 「このリポジトリの最重要ルールを、どのファイルに書いてあるか添えて3つ挙げて」

期待される方向性：

- `.github/copilot-instructions.md` や `.github/instructions/*.instructions.md` に言及する
- `docs/spec/` / `docs/decisions.md` / `status/dashboard.md` の更新を促す

#### トラブルシュート（見つからない/設定が効かない）

- 設定名が候補に出ない場合：VS Code / GitHub Copilot / Copilot Chat を **最新版へ更新**してから再確認
- 組織管理PCの場合：ポリシーで設定が上書き/無効化されることがあります（管理者へ確認）
- Remote/WSL/コンテナ利用時：開いている“場所”によって設定スコープが分かれることがあります（User/Remote のどちらに入れるか再確認）

このワークスペースでは、以下が instruction files として効きます：

- 全体：`.github/copilot-instructions.md`
- 役割別：`.github/instructions/*.instructions.md`

### 3) Subagents（サブエージェント）を使う

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

> 設定名は VS Code のバージョン/提供状況で変わる場合があります。
> 見つからない場合は「ツールピッカーで runSubagent を有効化」だけで開始できます。

## 進め方（基本フロー）

1. 将軍：`docs/spec/` に仕様を書く（目的/制約/受け入れ条件）
2. 家老：仕様を読み、実行可能なタスクに分解し `status/dashboard.md` に並列タスクとして記載
3. 足軽：担当タスクを実行（実行内容はプロジェクトに依存。コード編集/レビュー/テスト等）
4. 家老：結果の取りまとめ、未完了タスクの再分配
5. 将軍：承認/却下/方向転換の判断

> 補足：ユーザ（上様）が「将軍・家老・足軽のコミュニケーション」を確認したい場合は、
> 会話ログではなく `status/dashboard.md` を見ます（ここが“やり取りの要約ログ”）。

## 上様（ユーザ）の役割：将軍への指示の出し方

## ナレッジ/改善を環境にフィードバックできる？（Kaizen Loop）

できます。この環境は「会話ログ」ではなく、**ファイル（Spec/Decisions/Dashboard/Instructions）**に運用知を還流させる設計です。

最短の流れ：

1. 発見（足軽/家老/将軍）：`status/dashboard.md` に *kaizen found* を1行で残す
2. 判断（将軍）：採用/保留/却下と優先度を決める
3. 分解（家老）：反映先（`docs/USAGE.md` や `.github/instructions/` 等）ごとにタスクへ切り、足軽へ配布
4. 反映（足軽）：担当ファイルのみ更新し、`status/dashboard.md` に done/error を残す
5. 記録（将軍/家老）：判断理由は `docs/decisions.md` に残す

詳細仕様は `docs/spec/kaizen-loop.md` を参照。

上様（あなた）は「手を動かす人」ではなく、**判断と方向付け**を担当します。

### 将軍に最初に渡すべき情報（テンプレ）

下をコピペして、Copilot Chat（Agentモード）で将軍に渡すと、ブレずに進みます。

#### 指示テンプレ（将軍宛）

- 目的（1行）：
- 背景：
- 制約（必須）：
	- 仕様駆動（Spec→Plan→実装）で進める
	- SOLID（SRP/DIP最優先）
	- 変更後は `docs/spec/` / `docs/decisions.md` / `status/dashboard.md` を更新
- 受け入れ条件（AC）：
	- [ ] 
- 優先度：速度 / 品質 / 安全 / 学習（どれを優先？）
- 禁止事項：
	- 例：外部依存追加禁止、既存API破壊禁止、など

### 上様がやる「最低限の介入」

- 将軍の提案が複数あるときに **A/B/C を選ぶ**
- 方向が違うと感じたら **「それ違う」**と言う
- 受け入れ条件を満たしたら **承認**する

## 将軍→家老→足軽の連携（ファイル運用）

このリポジトリでは、会話だけでなく **ファイル**を“真実のソース”にします。

### 将軍（shogun）

- `docs/spec/` に仕様（Intent/Constraints/AC）を確定させる
- 家老に「分解方針」を与える（競合が起きない切り方、優先度）

参考：`.github/instructions/shogun.instructions.md`

### 家老（karo）

- Specを読み、並列タスクへ分解
- `status/dashboard.md` に「足軽タスク一覧」と進捗を記載
- 設計判断が出たら `docs/decisions.md` に残す

参考：`.github/instructions/karo.instructions.md`

### 足軽（ashigaru）

- 自分の担当タスクだけを実行（最小権限）
- 実行結果（done/error、再現手順）を `status/dashboard.md` に残す

参考：`.github/instructions/ashigaru.instructions.md`

## 「やり取りが見える」テンプレ（Subagents並列の例）

ここは *会話ログそのもの* ではなく、「こういう粒度で投げると役割分担が見えて面白い」例です。
このテンプレを Copilot Chat（Agent）に貼って運用してください（成果物は `status/dashboard.md` に寄せます）。

### 将軍 → 家老（分解/レビュー依頼）

- 仕様：`docs/spec/<対象>.md` を前提に、ACを満たすためのタスク分割案をください
- 制約：足軽同士が同じファイルを触らない切り方（ファイル単位で競合回避）
- 出力：`status/dashboard.md` に貼れる形（担当/成果物/完了条件）
- リスク：Top3 を添えて

### 将軍 → 足軽（実装/調査タスクの委任）

- あなたの担当：<タスク名>
- 成果物：<ファイルパス or 変更内容の要約>
- 完了条件：<ACのどれを満たすか>
- 禁止：範囲外の変更、不要なリファクタ
- 報告先：`status/dashboard.md` に start/done/error と要点

### 家老 → 将軍（レビュー返却）

- 結論：OK/NG
- 仕様（AC）適合：どれが満たせていて、どれが未達か
- 重大リスク Top3：
- 最小修正案：
- 追加テスト案：

### 足軽 → 将軍（結果返却）

- 何をしたか（要点）：
- 変更の要旨：
- リスク/前提：
- 次に将軍が決めること：

## 必須のファイル更新

- 仕様：`docs/spec/`
- 判断ログ：`docs/decisions.md`
- 進捗：`status/dashboard.md`

## VS Code Tasks の使い方（テンプレ）

`.vscode/tasks.json` は、あなたのプロジェクトのコマンド（例：ビルド、静的解析、ユニットテスト）に合わせて編集してください。
複数タスクを `dependsOrder: parallel` で束ねるのが基本です。

このリポジトリには雛形として、プレースホルダ（`echo`）で動く並列タスク `Sample: All (parallel)` を同梱しています。
あなたのプロジェクトに合わせて `Sample: * (placeholder)` の `command/args` を実コマンドに置き換えてください。

