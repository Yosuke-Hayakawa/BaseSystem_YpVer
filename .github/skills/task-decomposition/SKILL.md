---
name: task-decomposition
description: Guide for decomposing specifications into parallel, non-conflicting tasks for Ashigaru (executor) agents. Use this when breaking down a spec into actionable tasks following SOLID principles and avoiding file conflicts.
license: MIT
---

# Task Decomposition Skill

When decomposing a specification into tasks (typically done by Karo, the Reviewer/QA agent), follow these principles to enable parallel execution without conflicts.

## Core Principles

### 1. Single Responsibility (SRP)
- Each task should have ONE clear responsibility
- Bad: "Implement and test feature X"
- Good: "Implement feature X" + separate "Write tests for feature X"

### 2. File-Level Separation
- **Critical**: Assign different files to different Ashigaru to avoid merge conflicts
- If multiple tasks need the same file, sequence them (not parallel)
- Example:
  ```
  ✅ Good (parallel-safe):
  - Task A: Edit file1.js (ashigaru-1)
  - Task B: Edit file2.js (ashigaru-2)
  
  ❌ Bad (conflict risk):
  - Task A: Edit config.js lines 1-10 (ashigaru-1)
  - Task B: Edit config.js lines 20-30 (ashigaru-2)
  ```

### 3. Clear Inputs and Outputs
Each task must specify:
- **Input**: What the task depends on (files, data, specs)
- **Output**: What the task produces (files, paths, documentation)

### 4. Testable Completion Criteria
- Each task should have clear done/not-done criteria
- Link back to the spec's Acceptance Criteria

## Decomposition Process

### Step 1: Identify Components
Break the feature into logical components based on:
- File boundaries (different modules, classes, configs)
- Layers (UI, logic, data, tests)
- Concerns (feature implementation vs. documentation vs. testing)

### Step 2: Check Dependencies
- Map which tasks depend on others
- Group dependent tasks for sequential execution
- Identify truly independent tasks for parallel execution

### Step 3: Assign Responsibility
- Name each Ashigaru: `ashigaru-1`, `ashigaru-2`, etc.
- Ensure no two Ashigaru modify the same file
- Balance workload (roughly equal complexity)

### Step 4: Document in Table Format

Use the standard task list format:

```markdown
| task | assignee | input | output |
|---|---|---|---|
| Implement parser | ashigaru-1 | spec section 3.1 | src/parser.js |
| Create tests | ashigaru-2 | spec AC 1-3 | test/parser.test.js |
| Update docs | ashigaru-3 | src/parser.js | docs/api.md |
```

## Example: Multi-File Feature

**Spec**: Add user authentication to the system

**Bad Decomposition** (conflict risk):
```markdown
| task | assignee | input | output |
|---|---|---|---|
| Add login route | ashigaru-1 | spec | server.js, auth.js |
| Add logout route | ashigaru-2 | spec | server.js, auth.js |
```
☠️ Both touch `server.js` and `auth.js` → merge conflicts!

**Good Decomposition** (parallel-safe):
```markdown
| task | assignee | input | output |
|---|---|---|---|
| Implement auth service | ashigaru-1 | spec AC 1-2 | src/auth-service.js |
| Implement login route | ashigaru-2 | spec AC 3 | routes/login.js |
| Implement logout route | ashigaru-3 | spec AC 4 | routes/logout.js |
| Write auth tests | ashigaru-4 | spec AC 1-4 | test/auth.test.js |
| Update API docs | ashigaru-5 | routes/*.js | docs/api/auth.md |
```
✅ Each Ashigaru has their own file(s)!

## Handling Shared Files

When a file MUST be edited by multiple tasks:

### Option 1: Sequence Tasks
```markdown
| task | assignee | input | output | depends_on |
|---|---|---|---|---|
| Add base config | ashigaru-1 | spec | config.js | - |
| Add feature A config | ashigaru-2 | config.js | config.js | ashigaru-1 |
| Add feature B config | ashigaru-3 | config.js | config.js | ashigaru-2 |
```

### Option 2: Create Separate Files
```markdown
| task | assignee | input | output |
|---|---|---|---|
| Create base config | ashigaru-1 | spec | config/base.js |
| Create feature A config | ashigaru-2 | spec | config/feature-a.js |
| Create feature B config | ashigaru-3 | spec | config/feature-b.js |
| Integrate configs | ashigaru-4 | config/*.js | config/index.js |
```

## Task Size Guidelines

- **Too small**: "Add a single line to file.js" (not worth separate task)
- **Too large**: "Implement the entire feature" (defeats parallel execution)
- **Just right**: "Implement the user service class" (clear scope, file boundary)

Aim for: **1-3 hours of work per task** (estimating for experienced developer)

## Reporting Back to Shogun

After decomposing, provide:
1. **Task count**: "分解結果: 5タスク（3並列実行可）"
2. **Parallelization plan**: Which tasks can run in parallel
3. **Risk assessment**: Potential bottlenecks or dependencies
4. **File map**: Which Ashigaru owns which files

## Common Mistakes

- ❌ Creating tasks that modify the same file in parallel
- ❌ Forgetting to specify inputs/outputs
- ❌ Making tasks too dependent (reducing parallelism)
- ❌ Ignoring test task separation (tests should be separate tasks)
- ❌ Not considering `output/` directory for intermediate artifacts

## Integration with Workflow

1. **Receive** spec from Shogun (Orchestrator)
2. **Decompose** using this skill's guidelines
3. **Validate** no file conflicts exist
4. **Report** to Shogun with task list
5. **Update** `status/dashboard.md` with task assignments
6. **Monitor** Ashigaru progress and resolve blockers
