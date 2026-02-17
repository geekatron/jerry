# TASK-003: Fix SubagentStop Hook — Correct Event and Output

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-02-17 (Claude)
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Content](#content) | Description and acceptance criteria |
| [History](#history) | Status changes |

---

## Frontmatter

```yaml
id: "TASK-003"
work_type: TASK
title: "Fix SubagentStop Hook — Correct Event and Output"
status: pending
priority: HIGH
parent_id: "BUG-002"
assignee: "Claude"
created_at: "2026-02-17"
activity: DEVELOPMENT
effort: 2
```

---

## Content

### Description

Fix `scripts/subagent_stop.py` to use the correct Claude Code event and output format.

**Changes required:**

1. **hooks.json:** Change event from `Stop` to `SubagentStop`. SubagentStop supports matchers on agent type (e.g., `"Bash"`, `"Explore"`, `"Plan"`, or custom agent names). Remove the invalid `"subagent:*"` matcher — use `"*"` or omit entirely to match all subagent types.

2. **Input schema update:** SubagentStop hooks receive `agent_id`, `agent_type`, `agent_transcript_path`, and `stop_hook_active` fields (not `agent_name` and `output` as currently expected).

3. **Output format:** SubagentStop uses the same decision control as Stop hooks:
```json
{
    "decision": "block",
    "reason": "reason why subagent should continue"
}
```
Non-standard fields like `action`, `to_agent`, `work_items` are ignored.

4. **Exit codes:** Exit 1 is a non-blocking error. For "no handoff needed", exit 0 with empty JSON instead.

**Files to modify:**
- `hooks/hooks.json` (lines 40-51)
- `scripts/subagent_stop.py` (input parsing, output format, exit codes)

### Acceptance Criteria

- [ ] hooks.json registers under `SubagentStop` event (not `Stop`)
- [ ] Matcher is valid for SubagentStop (agent type names or omitted)
- [ ] Input parsing uses correct field names (`agent_type`, not `agent_name`)
- [ ] Output conforms to SubagentStop decision control schema
- [ ] Exit codes follow hook protocol (0 = success, 2 = blocking)

### Related Items

- Parent: [BUG-002](../BUG-002-hook-schema-validation-failures.md)
- Files: `scripts/subagent_stop.py`, `hooks/hooks.json`

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation |
