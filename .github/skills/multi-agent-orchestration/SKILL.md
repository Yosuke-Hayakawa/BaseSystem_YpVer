---
name: multi-agent-orchestration
description: Guide for orchestrating the Shogun/Karo/Ashigaru multi-agent workflow. Use this when coordinating multiple agents following the specification-driven, SOLID-based development process.
license: MIT
---

# Multi-Agent Orchestration Skill

This skill provides guidance for orchestrating the three-tier agent system: Shogun (Orchestrator), Karo (Reviewer/QA), and Ashigaru (Executor).

## Agent Roles and Responsibilities

### Shogun (Orchestrator) - 将軍
**Primary Role**: Strategic planning and decision-making

**Responsibilities**:
- Create and validate specifications in `docs/spec/`
- Make important decisions (escalate to user when needed)
- Coordinate Karo and Ashigaru via subagents
- Update `docs/decisions.md` with key decisions
- Monitor overall progress

**Key Skills**: orchestration, specification-definition, requirements-analysis, task-planning, multi-agent-coordination, progress-tracking, decision-making, stakeholder-communication

**Agents Available**: Karo, Ashigaru, Plan

### Karo (Reviewer/QA) - 家老
**Primary Role**: Quality assurance and task management

**Responsibilities**:
- Decompose specs into parallel tasks (using task-decomposition skill)
- Review code for SOLID principles, security, and spec compliance
- Update `status/dashboard.md` (single source of truth for progress)
- Manage Ashigaru assignments and resolve blockers
- Report results to Shogun

**Key Skills**: code-review, quality-assurance, task-decomposition, solid-principles, security-analysis, risk-assessment, test-planning, specification-validation

**Agents Available**: Ashigaru

### Ashigaru (Executor) - 足軽
**Primary Role**: Focused task execution

**Responsibilities**:
- Execute assigned tasks ONLY (no scope creep)
- Make minimal changes to achieve task goals
- Report results in YAML format (with skill_candidate)
- Place artifacts in `output/` directory
- Never call other agents (agents: [])

**Key Skills**: code-implementation, focused-execution, minimal-changes, testing, debugging, file-operations, command-execution

**Agents Available**: None (enforces least privilege)

## Standard Workflow

### Phase 1: Specification (Shogun)
```
1. User provides high-level requirement
2. Shogun creates spec in docs/spec/<name>.md
   - Intent: What and why
   - Constraints: Technical/security limitations
   - AC: Testable acceptance criteria
3. Shogun checks for important decisions
   → If yes: Escalate to user for approval
   → If no: Proceed to Phase 2
4. Record decision in docs/decisions.md
```

### Phase 2: Task Decomposition (Karo)
```
1. Shogun handoffs to Karo: "Decompose this spec"
2. Karo analyzes spec using task-decomposition skill
   - Identify components
   - Check file boundaries (avoid conflicts)
   - Create parallel-safe task list
3. Karo updates status/dashboard.md with tasks
4. Karo reports back to Shogun:
   - Task count and parallelization plan
   - Risk assessment
   - File ownership map
```

### Phase 3: Parallel Execution (Ashigaru × N)
```
1. Shogun launches multiple Ashigaru via subagents
   - Each gets ONE task from the task list
   - Each works on DIFFERENT files
2. Ashigaru execute independently:
   - Read spec and assigned task
   - Make minimal changes
   - Create artifacts in output/ if needed
   - Report in YAML format
3. Karo monitors progress (updates dashboard)
```

### Phase 4: Review and Integration (Karo)
```
1. Karo reviews Ashigaru outputs
   - Check AC compliance
   - Verify SOLID principles
   - Security analysis (NULL checks, boundaries)
   - Test coverage
2. If issues found:
   → Karo handoffs to specific Ashigaru for fixes
3. If OK:
   → Karo reports to Shogun: "Ready for final validation"
```

### Phase 5: Final Validation (Shogun)
```
1. Shogun performs final checks
   - All ACs met?
   - Dashboard shows all tasks complete?
   - Decisions recorded?
2. If OK:
   → Mark complete, commit via report_progress
3. If not OK:
   → Loop back to appropriate phase
```

## Communication Protocol

### Shogun → Karo Handoff
```markdown
以下の仕様をタスクに分解してください。
- 足軽同士が同じファイルを触らない切り方（ファイル単位で競合回避）
- 担当/成果物/完了条件を明記
- リスクTop3を添えて

Spec: docs/spec/feature-x-v1.md
```

### Karo → Ashigaru Handoff
```markdown
以下のタスクを実行してください。担当範囲のみ処理し、完了後に結果を返してください。

Task: <specific task from task list>
Input: <files or specs to read>
Output: <files to create/modify>
AC: <relevant acceptance criteria from spec>
```

### Ashigaru → Karo Report (YAML)
```yaml
role: ashigaru-N
topic: <task name>
status: done | error | blocked
outputs:
  - <file paths or output/ artifacts>
summary: |
  - What was done
  - Key changes
  - Risks or assumptions
skill_candidate:
  - <discovered specialties>
```

### Karo → Shogun Report
```markdown
タスク分解が完了しました。

Task count: 5 (3並列、2直列)
Files: src/a.js (ashigaru-1), src/b.js (ashigaru-2), test/ab.test.js (ashigaru-3)
Risks:
  1. Feature B depends on Feature A (must sequence)
  2. API変更により既存機能への影響あり
  3. テストカバレッジが現時点で60%（目標80%）

Dashboard: 更新済み (status/dashboard.md)
```

## Important Decision Gate (上様お伺い)

When Shogun or Karo encounters an important decision:

**Format**:
```markdown
🚨 上様、お伺い申す

論点: <decision needed>
選択肢:
  A. <option A>
  B. <option B>
  C. <option C>
推奨: <A/B/C>
理由: <why recommended>
リスク: <risk of each option>
期限: <optional deadline>
```

**Important Decisions Include**:
- Technology selection (libraries, frameworks)
- External dependency addition/update
- Breaking changes (API changes, file moves)
- Security/auth/secrets handling
- Artifact placement outside of output/
- Operational flow changes

**Wait for user response before proceeding with that decision.**

## File and Directory Conventions

### Source of Truth (一次情報)
- `docs/spec/`: Specifications (Intent/Constraints/AC)
- `docs/decisions.md`: Design decision log
- `status/dashboard.md`: Progress tracking (Karo owns this)

### Artifacts (生成物)
- `output/`: All generated artifacts (research notes, logs, comparison tables, build outputs)
  - Example: `output/ashigaru-1/`, `output/karo/review-2024-02-13.md`

### Instructions
- `.github/copilot-instructions.md`: Global rules
- `.github/instructions/*.instructions.md`: Role-specific rules

### Agent Definitions
- `.github/agents/*.agent.md`: Custom agent definitions with skills

### Skills
- `.github/skills/*/SKILL.md`: Specialized task instructions

## Parallelization Guidelines

### ✅ Safe to Parallelize
- Different files entirely
- Different modules/packages
- Read-only operations on the same file
- Independent test files

### ❌ Cannot Parallelize
- Same file edits (merge conflict risk)
- Sequential dependencies (B needs A's output)
- Shared mutable state
- Global configuration changes

### Example: Safe Parallelization
```
Task 1 (ashigaru-1): Implement src/auth.js
Task 2 (ashigaru-2): Implement src/logger.js
Task 3 (ashigaru-3): Write test/auth.test.js
Task 4 (ashigaru-4): Write test/logger.test.js
→ All 4 can run in parallel (no file conflicts)
```

## Error Handling

### If Ashigaru Reports Error
```
1. Karo analyzes the error
2. If fixable: Karo creates fix task, assigns to Ashigaru
3. If blocker: Karo reports to Shogun
4. Shogun decides: continue, pivot, or escalate to user
```

### If File Conflict Occurs
```
1. STOP all parallel work on that file
2. Karo sequences the tasks
3. Restart with sequential execution
4. Update dashboard with new plan
```

## Progress Tracking

Karo updates `status/dashboard.md` with:
- [ ] Task list with status (start/done/error/blocked)
- [ ] Ashigaru assignments
- [ ] Completion percentage
- [ ] Blockers (🚨 要対応)

Format:
```markdown
## 進捗状況

| Task | Assignee | Status | Output |
|------|----------|--------|--------|
| Implement auth | ashigaru-1 | done ✅ | src/auth.js |
| Write auth tests | ashigaru-2 | done ✅ | test/auth.test.js |
| Update API docs | ashigaru-3 | in progress 🔄 | docs/api.md |

完了率: 66% (2/3)
```

## Best Practices

1. **Always start with a spec** - No code before specification
2. **Decompose carefully** - Avoid file conflicts
3. **Use subagents** - Leverage parallelism
4. **Update dashboard** - Single source of truth
5. **Escalate important decisions** - Don't assume
6. **Make minimal changes** - YAGNI principle
7. **Test as you go** - Don't defer testing
8. **Document decisions** - Future you will thank you

## Common Pitfalls

- ❌ Skipping spec creation (leads to scope creep)
- ❌ Having Ashigaru call other agents (violates least privilege)
- ❌ Multiple agents editing the same file (merge conflicts)
- ❌ Making important decisions without user approval
- ❌ Forgetting to update dashboard (loses progress visibility)
- ❌ Creating artifacts outside of output/ (clutters repo)
- ❌ Writing code before tests (reduces quality)
