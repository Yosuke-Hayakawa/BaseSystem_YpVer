---
name: task-management
description: status/task.md 進捗追跡ファイルを管理するためのガイド。Barnesとしてプロジェクトステータス、タスク完了、進捗報告を更新する際に使用します。
license: MIT
---

# タスク管理スキル

`status/task.md` ファイルは、プロジェクト進捗の**単一の真実のソース**です。このスキルは、それを効果的に維持するためのガイダンスを提供します。

## 所有権

**Barnes** が `status/task.md` の主要な所有者です。
- Phillips と Cole はこのファイルを**直接編集すべきではない**（競合を防止）
- Cole は YAML 経由で Barnes に報告
- Barnes が統合してタスク管理を更新

## タスク管理構造

### 標準形式

```markdown
# プロジェクト進捗タスク管理

最終更新: YYYY-MM-DD HH:MM

## 🎯 現在の目標

<仕様からの高レベルな目標>

## 📋 タスク一覧

| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| タスク1 | Cole | done ✅ | src/file1.js | 2024-02-13 に完了 |
| タスク2 | Cole | in progress 🔄 | src/file2.js | レビュー待ち |
| タスク3 | Cole | blocked ⛔ | test/file.test.js | タスク1の出力が必要 |
| タスク4 | Cole | not started ⏸️ | docs/api.md | 次に予定 |

**完了率**: 25% (1/4)

## 🚨 要対応（ユーザ判断待ち）

| 論点 | 選択肢 | 推奨 | 理由 |
|------|--------|------|------|
| <必要な決定> | A/B/C | A | <根拠> |

## 📊 最近の活動

### YYYY-MM-DD HH:MM - Cole
- ✅ 認証サービスを実装
- Output: src/auth-service.js
- Skills demonstrated: Node.js, JWT, error-handling

### YYYY-MM-DD HH:MM - Barnes
- 📝 認証実装をレビュー
- Issues: なし
- Risks: レート制限が未実装（優先度低）

## 📚 関連ドキュメント

- Spec: docs/spec/auth-feature-v1.md
- Decisions: docs/decisions.md#auth-library-selection
- Previous タスク管理: status/archive/task-2024-02-12.md
```

## ステータスアイコン

一貫したアイコンを使用：
- ✅ `done` - タスク完了
- 🔄 `in progress` - 現在作業中
- ⛔ `blocked` - 進行不可（依存関係または問題）
- ⏸️ `not started` - キュー済みだが未開始
- ❌ `error` - 失敗、再試行または修正が必要

## 更新トリガー

Barnes は以下の場合にタスク管理を更新すべき：
1. **新規仕様作成**（Phillips）→ 目標と初期タスクリストを追加
2. **タスク分解完了**（Barnes）→ 詳細なタスク分解を追加
3. **Cole 報告**（Cole）→ タスクステータスを更新し、活動ログを追加
4. **レビュー完了**（Barnes）→ レビューノートを追加
5. **決定が必要**（Phillips/Barnes）→ "要対応" セクションに追加
6. **決定済み**（ユーザ）→ "要対応" から削除し、必要に応じてタスクを更新

## Cole 報告の受信（YAML）

Cole が YAML 形式で報告する場合：

```yaml
role: Cole
topic: implement-logger
status: done
outputs:
  - src/logger.js
  - output/Cole/logger-design.md
summary: |
  - Winston ベースのログローテーション付きロガーを実装
  - error, warn, info, debug レベルを追加
  - 環境変数による設定
skill_candidate:
  - winston
  - logging-systems
  - configuration-management
```

**Barnes のアクション**:
1. **YAML を解析**して主要情報を抽出
2. タスクテーブルで**タスクステータスを更新**
3. タイムスタンプ付きで**活動ログ**エントリを追加
4. 今後のタスク割り当てのため**スキルをメモ**
5. 出力が存在することを**検証**（ファイル/パスを確認）

更新例:
```markdown
## 📋 タスク一覧

| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| ロガーを実装 | Cole | done ✅ | src/logger.js | Winston ベース、環境変数設定 |

## 📊 最近の活動

### 2024-02-13 14:30 - Cole
- ✅ Winston ベースのログローテーション付きロガーを実装
- Output: src/logger.js, output/Cole/logger-design.md
- Skills: winston, logging-systems, configuration-management
```

## 重要な決定の扱い（ユーザお伺い）

Phillips または Barnes が重要な決定を特定した場合：

### 1. "🚨 要対応" セクションに追加

```markdown
## 🚨 要対応（ユーザ判断待ち）

| 論点 | 選択肢 | 推奨 | 理由 |
|------|--------|------|------|
| ログライブラリの選定 | A. Winston / B. Bunyan / C. Pino | A (Winston) | 実績多数、プラグイン豊富、チーム経験あり |
| 認証方式 | A. JWT / B. Session / C. OAuth2 | A (JWT) | ステートレス、スケーラブル、API向き |
```

### 2. 関連タスクをブロック

決定が行われるまで、依存タスクを "blocked ⛔" としてマーク：

```markdown
| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| 認証を実装 | Cole | blocked ⛔ | src/auth.js | 待ち: 認証方式の決定 |
```

### 3. ユーザーが決定した後

- "🚨 要対応" から**削除**
- 関連タスクを**ブロック解除**
- `docs/decisions.md` に**決定を記録**
- 選択されたアプローチでタスクノートを**更新**

## 進捗計算

完了率を計算：
```
完了率 = (完了タスク数 / 総タスク数) × 100%
```

例：
- 合計: 8 タスク
- 完了: 3 タスク
- 進行中: 2 タスク
- 未開始: 3 タスク

```markdown
**完了率**: 37.5% (3/8)
**進行中**: 2
**残タスク**: 3
```

## 活動ログのベストプラクティス

### タイムスタンプの取得方法

ログ行を書く際は、**必ず現在の日時（YYYY-MM-DD HH:MM）を使用**すること。
`00:00` はデフォルトではなく「時刻がどうしても取得できない場合のみ使う例外」です。

現在時刻の確認方法（例）：
- bash: `date '+%Y-%m-%d %H:%M'`
- Python: `from datetime import datetime; datetime.now().strftime('%Y-%m-%d %H:%M')`

### 良い活動エントリ
```markdown
### 2024-02-13 14:30 - Cole
- ✅ Winston ベースのログローテーション付きロガーを実装
- Output: src/logger.js, output/Cole/logger-design.md
- Skills: winston, logging-systems, configuration-management
- Notes: 環境変数による設定、本番環境対応
```

### 悪い活動エントリ（曖昧すぎる）
```markdown
### 2024-02-13 - Cole
- ログ処理に関する作業を実施
```

### 含めるべき内容
- ✅ **タイムスタンプ**: 日付と時刻（HH:MM）
- ✅ **エージェント**: 作業を実施した人
- ✅ **アクション**: 達成されたこと（動詞 + 目的語）
- ✅ **出力**: 具体的なファイルパスまたは成果物
- ✅ **スキル**: 実証された能力
- ❌ **避ける**: 曖昧な発言、意見、不要な詳細

## タスク管理のアーカイブ

新しい主要フェーズまたはスプリントを開始する場合：

1. **現在のタスク管理をコピー**して `status/archive/task-YYYY-MM-DD.md` へ
2. 新しい作業のため**タスクリストをリセット**
3. アーカイブリンク付きで "関連ドキュメント" セクションを**保持**
4. 未解決の "要対応" 項目を**保持**

例：
```bash
cp status/task.md status/archive/task-2024-02-13.md
# 新しいスプリント用に タスク管理.md を編集
```

## 他のファイルとの統合

### 仕様ファイル（`docs/spec/`）
- タスク管理はアクティブな仕様を**参照**
- タスクリストは仕様の AC と Plan セクションから**派生**
- "関連ドキュメント" に仕様パスを**リンク**

### 決定ログ（`docs/decisions.md`）
- タスク管理は特定の決定に**リンク**
- 重要な決定はタスク管理の "要対応" から**開始**
- 承認後、決定は decisions.md に**記録**

### 指示書（`.github/instructions/`）
- タスク管理は指示書で定義された形式に**従う**
- Barnes は更新ルールとして指示書を**参照**

## よくあるミス

### ❌ してはいけないこと
- Phillips や Cole にタスク管理を直接編集させる（競合を引き起こす）
- 報告受信後の更新を忘れる
- 一貫性のないステータスラベルを使用
- 活動ログでタイムスタンプを省略
- 古い活動を削除（履歴を保持）
- タスクステータスを作る（常に実際の報告に基づく）

### ✅ すべきこと
- Barnes が単一の編集者（競合なし）
- イベント後すぐに更新
- アイコンを一貫して使用
- 正確なタイムスタンプを含める
- 満杯になったらアーカイブ、削除しない
- エージェントからの検証済み報告のみを信頼

## 例: 完全な更新サイクル

### 1. 初期状態（Phillips が仕様を作成）
```markdown
# プロジェクト進捗タスク管理

## 🎯 現在の目標
認証機能の実装

## 📋 タスク一覧
(空 - タスク分解を待機中)

## 📚 関連ドキュメント
- Spec: docs/spec/auth-feature-v1.md
```

### 2. Barnes が分解した後
```markdown
## 📋 タスク一覧

| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| 認証サービスを実装 | Cole | not started ⏸️ | src/auth-service.js | |
| 認証テストを書く | Cole | not started ⏸️ | test/auth.test.js | Cole に依存 |
| API ドキュメントを更新 | Cole | not started ⏸️ | docs/api/auth.md | |

**完了率**: 0% (0/3)
```

### 3. Cole が完了を報告した後
```markdown
| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| 認証サービスを実装 | Cole | done ✅ | src/auth-service.js | JWT ベース |
| 認証テストを書く | Cole | in progress 🔄 | test/auth.test.js | 開始済み |
| API ドキュメントを更新 | Cole | not started ⏸️ | docs/api/auth.md | |

**完了率**: 33% (1/3)

## 📊 最近の活動

### 2024-02-13 15:00 - Cole
- ✅ JWT ベースの認証サービスを実装
- Output: src/auth-service.js
- Skills: jwt, bcrypt, express-middleware
```

### 4. すべてのタスク完了後
```markdown
| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| 認証サービスを実装 | Cole | done ✅ | src/auth-service.js | JWT ベース |
| 認証テストを書く | Cole | done ✅ | test/auth.test.js | カバレッジ: 95% |
| API ドキュメントを更新 | Cole | done ✅ | docs/api/auth.md | Swagger 統合 |

**完了率**: 100% (3/3) 🎉
```

## まとめ

- **Barnes が所有** status/task.md（単一の編集者）
- **更新トリガー**: 仕様作成、タスク分解、エージェント報告、レビュー、決定
- **標準形式**: 目標、タスクテーブル、重要な決定、活動ログ、関連ドキュメント
- **一貫したアイコン**: ✅ done, 🔄 in progress, ⛔ blocked, ⏸️ not started, ❌ error
- **アーカイブ**: 新フェーズ開始時
- **リンク**: 仕様と決定へ
