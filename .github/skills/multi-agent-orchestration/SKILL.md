---
name: multi-agent-orchestration
description: Phillips/Cole/Barnes/Volkova マルチエージェントワークフローを調整するためのガイド。仕様駆動・SOLID ベースの開発プロセスに従って複数のエージェントを調整する際に使用します。
license: MIT
---

# マルチエージェント オーケストレーション スキル

このスキルは、3層エージェントシステムを調整するためのガイダンスを提供します：Phillips、Barnes、Cole。

## エージェントの役割と責任

### Phillips- Phillips
**主要な役割**: 戦略的計画と意思決定

**責任**:
- `docs/spec/` に仕様を作成・検証
- 重要な決定を行う（必要に応じてユーザにエスカレーション）
- サブエージェント経由で Barnes と Cole を調整
- 重要な決定を `docs/decisions.md` に更新
- 全体の進捗を監視

**主要スキル**: orchestration, specification-definition, requirements-analysis, task-planning, multi-agent-coordination, progress-tracking, decision-making, stakeholder-communication

**利用可能なエージェント**: Barnes, Cole, Plan

### Barnes- Barnes
**主要な役割**: 品質保証とタスク管理

**責任**:
- 仕様を並列タスクに分解（task-decomposition スキルを使用）
- SOLID 原則、セキュリティ、仕様準拠のコードレビュー
- `status/task.md` を更新（進捗の単一の真実のソース）
- Cole の割り当てを管理し、ブロッカーを解決
- 結果を Phillips に報告

**主要スキル**: code-review, quality-assurance, task-decomposition, solid-principles, security-analysis, risk-assessment, test-planning, specification-validation

**利用可能なエージェント**: Cole

### Cole - フィールドエージェント
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

### フェーズ1: 仕様作成（Phillips）
```
1. ユーザが高レベルの要件を提供
2. Phillips が docs/spec/<name>.md に仕様を作成
   - Intent: 何を、なぜ
   - Constraints: 技術的/セキュリティ上の制限
   - AC: テスト可能な受け入れ条件
3. Phillips が重要な決定を確認
   → はい: ユーザの承認にエスカレーション
   → いいえ: フェーズ2に進む
4. docs/decisions.md に決定を記録
```

### フェーズ2: タスク分解（Barnes）
```
1. Phillips が Barnes にハンドオフ: "この仕様を分解してください"
2. Barnes が task-decomposition スキルを使用して仕様を分析
   - コンポーネントを特定
   - ファイル境界を確認（競合を回避）
   - 並列安全なタスクリストを作成
3. Barnes が status/task.md をタスクで更新
4. Barnes が Phillips に報告:
   - タスク数と並列化計画
   - リスク評価
   - ファイル所有権マップ
```

### フェーズ3: 並列実行（Cole × N）
```
1. Phillips がサブエージェント経由で複数の Cole を起動
   - 各自がタスクリストから1つのタスクを取得
   - 各自が異なるファイルで作業
2. Cole が独立して実行:
   - 仕様と割り当てられたタスクを読む
   - 最小限の変更を行う
   - 必要に応じて output/ に成果物を作成
   - YAML 形式で報告
3. Barnes が進捗を監視（タスク管理を更新）
```

### フェーズ4: レビューと統合（Barnes）
```
1. Barnes が Cole の出力をレビュー
   - AC 準拠を確認
   - SOLID 原則を検証
   - セキュリティ分析（NULL チェック、境界）
   - テストカバレッジ
2. 問題が見つかった場合:
   → Barnes が特定の Cole に修正をハンドオフ
3. OK の場合:
   → Barnes が Phillips に報告: "最終検証の準備完了"
```

### フェーズ5: 最終検証（Phillips）
```
1. Phillips が最終チェックを実行
   - すべての AC が満たされているか？
   - タスク管理がすべてのタスクが完了していることを示しているか？
   - 決定が記録されているか？
2. OK の場合:
   → 完了としてマークし、report_progress 経由でコミット
3. OK でない場合:
   → 適切なフェーズにループバック
```

## コミュニケーションプロトコル

### Phillips → Barnes ハンドオフ
```markdown
以下の仕様をタスクに分解してください。
- Cole同士が同じファイルを触らない切り方（ファイル単位で競合回避）
- 担当/成果物/完了条件を明記
- リスクTop3を添えて

Spec: docs/spec/feature-x-v1.md
```

### Barnes → Cole ハンドオフ
```markdown
以下のタスクを実行してください。担当範囲のみ処理し、完了後に結果を返してください。

Task: <タスクリストから特定のタスク>
Input: <読むべきファイルや仕様>
Output: <作成/変更するファイル>
AC: <仕様から関連する受け入れ条件>
```

### Cole → Barnes 報告（YAML）
```yaml
role: Cole
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

### Barnes → Phillips 報告
```markdown
タスク分解が完了しました。

Task count: 5 (3並列、2直列)
Files: src/a.js (Cole), src/b.js (Cole), test/ab.test.js (Cole)
Risks:
  1. 機能B は機能A に依存（順次実行が必要）
  2. API 変更により既存機能への影響あり
  3. テストカバレッジが現時点で60%（目標80%）

タスク管理: 更新済み (status/task.md)
```

## 重要な決定ゲート（ユーザお伺い）

Phillips または Barnes が重要な決定に遭遇した場合：

**形式**:
```markdown
🚨 お伺いいたします

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

**その決定を進める前にユーザの応答を待ってください。**

## ファイルとディレクトリの規則

### 真実のソース（一次情報）
- `docs/spec/`: 仕様（Intent/Constraints/AC）
- `docs/decisions.md`: 設計決定ログ
- `status/task.md`: 進捗追跡（Barnes が所有）

### 成果物（生成物）
- `output/`: すべての生成された成果物（調査メモ、ログ、比較表、ビルド出力）
  - 例: `output/Cole/`, `output/barnes/review-2024-02-13.md`

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
タスク1 (Cole): src/auth.js を実装
タスク2 (Cole): src/logger.js を実装
タスク3 (Cole): test/auth.test.js を書く
タスク4 (Cole): test/logger.test.js を書く
→ 4つすべてが並列実行可能（ファイル競合なし）
```

## エラーハンドリング

### Cole がエラーを報告した場合
```
1. Barnes がエラーを分析
2. 修正可能な場合: Barnes が修正タスクを作成し、Cole に割り当て
3. ブロッカーの場合: Barnes が Phillips に報告
4. Phillips が決定: 続行、方向転換、またはユーザにエスカレーション
```

### ファイル競合が発生した場合
```
1. そのファイルでのすべての並列作業を停止
2. Barnes がタスクを順次化
3. 順次実行で再開
4. タスク管理を新しい計画で更新
```

## 進捗追跡

Barnes が `status/task.md` を以下で更新：
- [ ] ステータス付きタスクリスト（start/done/error/blocked）
- [ ] Cole の割り当て
- [ ] 完了率
- [ ] ブロッカー（🚨 要対応）

形式:
```markdown
## 進捗状況

| Task | Assignee | Status | Output |
|------|----------|--------|--------|
| 認証を実装 | Cole | done ✅ | src/auth.js |
| 認証テストを書く | Cole | done ✅ | test/auth.test.js |
| API ドキュメントを更新 | Cole | in progress 🔄 | docs/api.md |

完了率: 66% (2/3)
```

## ベストプラクティス

1. **常に仕様から始める** - コードの前に仕様
2. **慎重に分解する** - ファイル競合を避ける
3. **サブエージェントを使う** - 並列性を活用
4. **タスク管理を更新** - 単一の真実のソース
5. **重要な決定をエスカレーション** - 推測しない
6. **最小限の変更を行う** - YAGNI 原則
7. **進めながらテスト** - テストを後回しにしない
8. **決定を文書化** - 未来の自分が感謝する

## よくある落とし穴

- ❌ 仕様作成をスキップ（スコープクリープにつながる）
- ❌ Cole に他のエージェントを呼ばせる（最小権限違反）
- ❌ 複数のエージェントが同じファイルを編集（マージ競合）
- ❌ ユーザの承認なしに重要な決定を行う
- ❌ タスク管理の更新を忘れる（進捗の可視性を失う）
- ❌ output/ 外に成果物を作成（リポジトリが散らかる）
- ❌ テスト前にコードを書く（品質が低下）
