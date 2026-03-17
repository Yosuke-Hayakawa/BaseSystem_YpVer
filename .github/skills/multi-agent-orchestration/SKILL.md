---
name: multi-agent-orchestration
description: Race Director/Pit Chief/Mechanic マルチエージェントワークフローを調整するためのガイド。仕様駆動・SOLID ベースの開発プロセスに従って複数のエージェントを調整する際に使用します。
license: MIT
---

# マルチエージェント オーケストレーション スキル

このスキルは、3層エージェントシステムを調整するためのガイダンスを提供します：Race Director（オーケストレーター）、Pit Chief（レビュー/QA）、Mechanic（実行者）。

## エージェントの役割と責任

### Race Director（オーケストレーター）- Race Director
**主要な役割**: 戦略的計画と意思決定

**責任**:
- `docs/spec/` に仕様を作成・検証
- 重要な決定を行う（必要に応じてユーザーにエスカレーション）
- サブエージェント経由で Pit Chief と Mechanic を調整
- 重要な決定を `docs/decisions.md` に更新
- 全体の進捗を監視

**主要スキル**: orchestration, specification-definition, requirements-analysis, task-planning, multi-agent-coordination, progress-tracking, decision-making, stakeholder-communication

**利用可能なエージェント**: Pit Chief, Mechanic, Plan

### Pit Chief（レビュー/QA）- Pit Chief
**主要な役割**: 品質保証とタスク管理

**責任**:
- 仕様を並列タスクに分解（task-decomposition スキルを使用）
- SOLID 原則、セキュリティ、仕様準拠のコードレビュー
- `status/dashboard.md` を更新（進捗の単一の真実のソース）
- Mechanic の割り当てを管理し、ブロッカーを解決
- 結果を Race Director に報告

**主要スキル**: code-review, quality-assurance, task-decomposition, solid-principles, security-analysis, risk-assessment, test-planning, specification-validation

**利用可能なエージェント**: Mechanic

### Mechanic（実行者）- Mechanic
**主要な役割**: 集中的なタスク実行

**責任**:
- 割り当てられたタスクのみを実行（スコープクリープなし）
- タスクゴールを達成するための最小限の変更
- YAML 形式で結果を報告（skill_candidate を含む）
- 成果物を `output/` ディレクトリに配置
- 他のエージェントを呼び出さない（agents: []）

**主要スキル**: code-implementation, focused-execution, minimal-changes, testing, debugging, file-operations, command-execution

**利用可能なエージェント**: なし（最小権限を強制）

## 標準ワークフロー

### フェーズ1: 仕様作成（Race Director）
```
1. ユーザーが高レベルの要件を提供
2. Race Director が docs/spec/<name>.md に仕様を作成
   - Intent: 何を、なぜ
   - Constraints: 技術的/セキュリティ上の制限
   - AC: テスト可能な受け入れ条件
3. Race Director が重要な決定を確認
   → はい: ユーザーの承認にエスカレーション
   → いいえ: フェーズ2に進む
4. docs/decisions.md に決定を記録
```

### フェーズ2: タスク分解（Pit Chief）
```
1. Race Director が Pit Chief にハンドオフ: "この仕様を分解してください"
2. Pit Chief が task-decomposition スキルを使用して仕様を分析
   - コンポーネントを特定
   - ファイル境界を確認（競合を回避）
   - 並列安全なタスクリストを作成
3. Pit Chief が status/dashboard.md をタスクで更新
4. Pit Chief が Race Director に報告:
   - タスク数と並列化計画
   - リスク評価
   - ファイル所有権マップ
```

### フェーズ3: 並列実行（Mechanic × N）
```
1. Race Director がサブエージェント経由で複数の Mechanic を起動
   - 各自がタスクリストから1つのタスクを取得
   - 各自が異なるファイルで作業
2. Mechanic が独立して実行:
   - 仕様と割り当てられたタスクを読む
   - 最小限の変更を行う
   - 必要に応じて output/ に成果物を作成
   - YAML 形式で報告
3. Pit Chief が進捗を監視（ダッシュボードを更新）
```

### フェーズ4: レビューと統合（Pit Chief）
```
1. Pit Chief が Mechanic の出力をレビュー
   - AC 準拠を確認
   - SOLID 原則を検証
   - セキュリティ分析（NULL チェック、境界）
   - テストカバレッジ
2. 問題が見つかった場合:
   → Pit Chief が特定の Mechanic に修正をハンドオフ
3. OK の場合:
   → Pit Chief が Race Director に報告: "最終検証の準備完了"
```

### フェーズ5: 最終検証（Race Director）
```
1. Race Director が最終チェックを実行
   - すべての AC が満たされているか？
   - ダッシュボードがすべてのタスクが完了していることを示しているか？
   - 決定が記録されているか？
2. OK の場合:
   → 完了としてマークし、report_progress 経由でコミット
3. OK でない場合:
   → 適切なフェーズにループバック
```

## コミュニケーションプロトコル

### Race Director → Pit Chief ハンドオフ
```markdown
以下の仕様をタスクに分解してください。
- Mechanic同士が同じファイルを触らない切り方（ファイル単位で競合回避）
- 担当/成果物/完了条件を明記
- リスクTop3を添えて

Spec: docs/spec/feature-x-v1.md
```

### Pit Chief → Mechanic ハンドオフ
```markdown
以下のタスクを実行してください。担当範囲のみ処理し、完了後に結果を返してください。

Task: <タスクリストから特定のタスク>
Input: <読むべきファイルや仕様>
Output: <作成/変更するファイル>
AC: <仕様から関連する受け入れ条件>
```

### Mechanic → Pit Chief 報告（YAML）
```yaml
role: mechanic-N
topic: <タスク名>
status: done | error | blocked
outputs:
  - <ファイルパスまたは output/ の成果物>
summary: |
  - 何を行ったか
  - 主要な変更
  - リスクや前提条件
skill_candidate:
  - <発見された専門領域>
```

### Pit Chief → Race Director 報告
```markdown
タスク分解が完了しました。

Task count: 5 (3並列、2直列)
Files: src/a.js (mechanic-1), src/b.js (mechanic-2), test/ab.test.js (mechanic-3)
Risks:
  1. 機能B は機能A に依存（順次実行が必要）
  2. API 変更により既存機能への影響あり
  3. テストカバレッジが現時点で60%（目標80%）

Dashboard: 更新済み (status/dashboard.md)
```

## 重要な決定ゲート（上様お伺い）

Race Director または Pit Chief が重要な決定に遭遇した場合：

**形式**:
```markdown
🚨 上様、お伺い申す

論点: <必要な決定>
選択肢:
  A. <選択肢A>
  B. <選択肢B>
  C. <選択肢C>
推奨: <A/B/C>
理由: <推奨する理由>
リスク: <各選択肢のリスク>
期限: <任意の期限>
```

**重要な決定に含まれるもの**:
- 技術選定（ライブラリ、フレームワーク）
- 外部依存関係の追加/更新
- 破壊的変更（API 変更、ファイル移動）
- セキュリティ/認証/シークレットの扱い
- output/ 外への成果物の配置
- 運用フロー変更

**その決定を進める前にユーザーの応答を待ってください。**

## ファイルとディレクトリの規則

### 真実のソース（一次情報）
- `docs/spec/`: 仕様（Intent/Constraints/AC）
- `docs/decisions.md`: 設計決定ログ
- `status/dashboard.md`: 進捗追跡（Pit Chief が所有）

### 成果物（生成物）
- `output/`: すべての生成された成果物（調査メモ、ログ、比較表、ビルド出力）
  - 例: `output/mechanic-1/`, `output/pit-chief/review-2024-02-13.md`

### 指示書
- `.github/copilot-instructions.md`: グローバルルール
- `.github/instructions/*.instructions.md`: 役割固有のルール

### エージェント定義
- `.github/agents/*.agent.md`: スキルを持つカスタムエージェント定義

### スキル
- `.github/skills/*/SKILL.md`: 専門タスク指示

## 並列化ガイドライン

### ✅ 並列化しても安全
- 完全に異なるファイル
- 異なるモジュール/パッケージ
- 同じファイルへの読み取り専用操作
- 独立したテストファイル

### ❌ 並列化できない
- 同じファイルの編集（マージ競合リスク）
- 順次依存関係（B が A の出力を必要とする）
- 共有可変状態
- グローバル設定の変更

### 例: 安全な並列化
```
タスク1 (mechanic-1): src/auth.js を実装
タスク2 (mechanic-2): src/logger.js を実装
タスク3 (mechanic-3): test/auth.test.js を書く
タスク4 (mechanic-4): test/logger.test.js を書く
→ 4つすべてが並列実行可能（ファイル競合なし）
```

## エラーハンドリング

### Mechanic がエラーを報告した場合
```
1. Pit Chief がエラーを分析
2. 修正可能な場合: Pit Chief が修正タスクを作成し、Mechanic に割り当て
3. ブロッカーの場合: Pit Chief が Race Director に報告
4. Race Director が決定: 続行、方向転換、またはユーザーにエスカレーション
```

### ファイル競合が発生した場合
```
1. そのファイルでのすべての並列作業を停止
2. Pit Chief がタスクを順次化
3. 順次実行で再開
4. ダッシュボードを新しい計画で更新
```

## 進捗追跡

Pit Chief が `status/dashboard.md` を以下で更新：
- [ ] ステータス付きタスクリスト（start/done/error/blocked）
- [ ] Mechanic の割り当て
- [ ] 完了率
- [ ] ブロッカー（🚨 要対応）

形式:
```markdown
## 進捗状況

| Task | Assignee | Status | Output |
|------|----------|--------|--------|
| 認証を実装 | mechanic-1 | done ✅ | src/auth.js |
| 認証テストを書く | mechanic-2 | done ✅ | test/auth.test.js |
| API ドキュメントを更新 | mechanic-3 | in progress 🔄 | docs/api.md |

完了率: 66% (2/3)
```

## ベストプラクティス

1. **常に仕様から始める** - コードの前に仕様
2. **慎重に分解する** - ファイル競合を避ける
3. **サブエージェントを使う** - 並列性を活用
4. **ダッシュボードを更新** - 単一の真実のソース
5. **重要な決定をエスカレーション** - 推測しない
6. **最小限の変更を行う** - YAGNI 原則
7. **進めながらテスト** - テストを後回しにしない
8. **決定を文書化** - 未来の自分が感謝する

## よくある落とし穴

- ❌ 仕様作成をスキップ（スコープクリープにつながる）
- ❌ Mechanic に他のエージェントを呼ばせる（最小権限違反）
- ❌ 複数のエージェントが同じファイルを編集（マージ競合）
- ❌ ユーザーの承認なしに重要な決定を行う
- ❌ ダッシュボードの更新を忘れる（進捗の可視性を失う）
- ❌ output/ 外に成果物を作成（リポジトリが散らかる）
- ❌ テスト前にコードを書く（品質が低下）
