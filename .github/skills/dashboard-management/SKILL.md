---
name: dashboard-management
description: Guide for managing the status/dashboard.md progress tracking file. Use this when updating project status, task completion, and progress reporting as Karo (home secretary).
license: MIT
---

# Dashboard Management Skill

The `status/dashboard.md` file is the **single source of truth** for project progress. This skill provides guidance on maintaining it effectively.

## Ownership

**Karo (Reviewer/QA)** is the primary owner of `status/dashboard.md`.
- Shogun and Ashigaru should **not directly edit** this file (prevents conflicts)
- Ashigaru reports to Karo via YAML
- Karo consolidates and updates dashboard

## Dashboard Structure

### Standard Format

```markdown
# プロジェクト進捗ダッシュボード

最終更新: YYYY-MM-DD HH:MM

## 🎯 現在の目標

<High-level goal from the spec>

## 📋 タスク一覧

| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| Task 1 | ashigaru-1 | done ✅ | src/file1.js | Completed on 2024-02-13 |
| Task 2 | ashigaru-2 | in progress 🔄 | src/file2.js | Waiting for review |
| Task 3 | ashigaru-3 | blocked ⛔ | test/file.test.js | Needs Task 1 output |
| Task 4 | ashigaru-4 | not started ⏸️ | docs/api.md | Scheduled next |

**完了率**: 25% (1/4)

## 🚨 要対応（上様判断待ち）

| 論点 | 選択肢 | 推奨 | 理由 |
|------|--------|------|------|
| <Decision needed> | A/B/C | A | <Rationale> |

## 📊 最近の活動

### YYYY-MM-DD HH:MM - ashigaru-1
- ✅ Implemented authentication service
- Output: src/auth-service.js
- Skills demonstrated: Node.js, JWT, error-handling

### YYYY-MM-DD HH:MM - karo
- 📝 Reviewed authentication implementation
- Issues: None
- Risks: Rate limiting not implemented (low priority)

## 📚 関連ドキュメント

- Spec: docs/spec/auth-feature-v1.md
- Decisions: docs/decisions.md#auth-library-selection
- Previous dashboard: status/archive/dashboard-2024-02-12.md
```

## Status Icons

Use consistent icons:
- ✅ `done` - Task completed
- 🔄 `in progress` - Currently working
- ⛔ `blocked` - Cannot proceed (dependency or issue)
- ⏸️ `not started` - Queued but not begun
- ❌ `error` - Failed, needs retry or fix

## Update Triggers

Karo should update dashboard when:
1. **New spec created** (Shogun) → Add goal and initial task list
2. **Task decomposition complete** (Karo) → Add detailed task breakdown
3. **Ashigaru reports** (Ashigaru) → Update task status and add activity log
4. **Review complete** (Karo) → Add review notes
5. **Decision needed** (Shogun/Karo) → Add to "要対応" section
6. **Decision made** (User) → Remove from "要対応", update tasks if needed

## Receiving Ashigaru Reports (YAML)

When Ashigaru reports in YAML format:

```yaml
role: ashigaru-2
topic: implement-logger
status: done
outputs:
  - src/logger.js
  - output/ashigaru-2/logger-design.md
summary: |
  - Implemented Winston-based logger with rotation
  - Added error, warn, info, debug levels
  - Configuration via environment variables
skill_candidate:
  - winston
  - logging-systems
  - configuration-management
```

**Karo's Actions**:
1. **Parse the YAML** to extract key info
2. **Update task status** in the task table
3. **Add activity log** entry with timestamp
4. **Note skills** for future task assignments
5. **Validate outputs** exist (check files/paths)

Example Update:
```markdown
## 📋 タスク一覧

| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| Implement logger | ashigaru-2 | done ✅ | src/logger.js | Winston-based, env config |

## 📊 最近の活動

### 2024-02-13 14:30 - ashigaru-2
- ✅ Implemented Winston-based logger with rotation
- Output: src/logger.js, output/ashigaru-2/logger-design.md
- Skills: winston, logging-systems, configuration-management
```

## Handling Important Decisions (上様お伺い)

When Shogun or Karo identifies an important decision:

### 1. Add to "🚨 要対応" Section

```markdown
## 🚨 要対応（上様判断待ち）

| 論点 | 選択肢 | 推奨 | 理由 |
|------|--------|------|------|
| ログライブラリの選定 | A. Winston / B. Bunyan / C. Pino | A (Winston) | 実績多数、プラグイン豊富、チーム経験あり |
| 認証方式 | A. JWT / B. Session / C. OAuth2 | A (JWT) | ステートレス、スケーラブル、API向き |
```

### 2. Block Related Tasks

Mark dependent tasks as "blocked ⛔" until decision is made:

```markdown
| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| Implement auth | ashigaru-3 | blocked ⛔ | src/auth.js | 待ち: 認証方式の決定 |
```

### 3. After User Decides

- **Remove** from "🚨 要対応"
- **Unblock** related tasks
- **Record decision** in `docs/decisions.md`
- **Update** task notes with chosen approach

## Progress Calculation

Calculate completion rate:
```
完了率 = (done tasks / total tasks) × 100%
```

Example:
- Total: 8 tasks
- Done: 3 tasks
- In progress: 2 tasks
- Not started: 3 tasks

```markdown
**完了率**: 37.5% (3/8)
**進行中**: 2
**残タスク**: 3
```

## Activity Log Best Practices

### Good Activity Entry
```markdown
### 2024-02-13 14:30 - ashigaru-2
- ✅ Implemented Winston-based logger with rotation
- Output: src/logger.js, output/ashigaru-2/logger-design.md
- Skills: winston, logging-systems, configuration-management
- Notes: Config via env vars, ready for production
```

### Bad Activity Entry (Too Vague)
```markdown
### 2024-02-13 - ashigaru-2
- Did some work on logging
```

### What to Include
- ✅ **Timestamp**: Date and time (HH:MM)
- ✅ **Agent**: Who did the work
- ✅ **Action**: What was accomplished (verb + object)
- ✅ **Outputs**: Concrete file paths or artifacts
- ✅ **Skills**: Demonstrated competencies
- ❌ **Avoid**: Vague statements, opinions, unnecessary details

## Dashboard Archiving

When starting a new major phase or sprint:

1. **Copy current dashboard** to `status/archive/dashboard-YYYY-MM-DD.md`
2. **Reset task list** for new work
3. **Keep** the "関連ドキュメント" section with archive link
4. **Retain** unresolved "要対応" items

Example:
```bash
cp status/dashboard.md status/archive/dashboard-2024-02-13.md
# Edit dashboard.md for new sprint
```

## Integration with Other Files

### Spec Files (`docs/spec/`)
- Dashboard **references** active specs
- Task lists **derive from** spec AC and Plan sections
- Link spec path in "関連ドキュメント"

### Decision Log (`docs/decisions.md`)
- Dashboard **links to** specific decisions
- Important decisions **start in** dashboard's "要対応"
- After approval, decisions **recorded in** decisions.md

### Instructions (`.github/instructions/`)
- Dashboard **follows format** defined in instructions
- Karo **references** instructions for update rules

## Common Mistakes

### ❌ Don't Do This
- Letting Shogun or Ashigaru directly edit dashboard (causes conflicts)
- Forgetting to update after receiving reports
- Using inconsistent status labels
- Omitting timestamps in activity log
- Deleting old activity (keep history)
- Making up task status (always base on actual reports)

### ✅ Do This
- Karo is the single editor (no conflicts)
- Update immediately after events
- Use standard icons consistently
- Include precise timestamps
- Archive when full, don't delete
- Trust only verified reports from agents

## Example: Full Update Cycle

### 1. Initial State (Shogun creates spec)
```markdown
# プロジェクト進捗ダッシュボード

## 🎯 現在の目標
Authentication機能の実装

## 📋 タスク一覧
(Empty - awaiting task decomposition)

## 📚 関連ドキュメント
- Spec: docs/spec/auth-feature-v1.md
```

### 2. After Karo Decomposes
```markdown
## 📋 タスク一覧

| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| Implement auth service | ashigaru-1 | not started ⏸️ | src/auth-service.js | |
| Write auth tests | ashigaru-2 | not started ⏸️ | test/auth.test.js | Depends on ashigaru-1 |
| Update API docs | ashigaru-3 | not started ⏸️ | docs/api/auth.md | |

**完了率**: 0% (0/3)
```

### 3. After Ashigaru-1 Reports Done
```markdown
| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| Implement auth service | ashigaru-1 | done ✅ | src/auth-service.js | JWT-based |
| Write auth tests | ashigaru-2 | in progress 🔄 | test/auth.test.js | Started |
| Update API docs | ashigaru-3 | not started ⏸️ | docs/api/auth.md | |

**完了率**: 33% (1/3)

## 📊 最近の活動

### 2024-02-13 15:00 - ashigaru-1
- ✅ Implemented JWT-based auth service
- Output: src/auth-service.js
- Skills: jwt, bcrypt, express-middleware
```

### 4. After All Tasks Complete
```markdown
| Task | Assignee | Status | Output | Notes |
|------|----------|--------|--------|-------|
| Implement auth service | ashigaru-1 | done ✅ | src/auth-service.js | JWT-based |
| Write auth tests | ashigaru-2 | done ✅ | test/auth.test.js | Coverage: 95% |
| Update API docs | ashigaru-3 | done ✅ | docs/api/auth.md | Swagger integrated |

**完了率**: 100% (3/3) 🎉
```

## Summary

- **Karo owns** status/dashboard.md (single editor)
- **Update triggers**: spec creation, task decomposition, agent reports, reviews, decisions
- **Standard format**: Goal, Task table, Important decisions, Activity log, Related docs
- **Consistent icons**: ✅ done, 🔄 in progress, ⛔ blocked, ⏸️ not started, ❌ error
- **Archive** when starting new phases
- **Link** to specs and decisions
