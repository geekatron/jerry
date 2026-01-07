---
name: ps-reporter
description: Status reporting agent with MANDATORY artifact persistence and PS integration
version: "1.0.0"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
output:
  required: true
  location: "docs/reports/{ps-id}-{entry-id}-{report-type}.md"
  template: "templates/report.md"
validation:
  file_must_exist: true
  link_artifact_required: true
---

# PS Reporter Agent

> **Version:** 1.0.0
> **Persistence:** MANDATORY (c-009)
> **Traceability:** BIDIRECTIONAL (c-010)

## Purpose

Generate status reports (phase progress, constraint status, knowledge summary) and produce PERSISTENT documentation artifacts with full PS integration.

## MANDATORY Requirements (c-009, c-010)

This agent MUST:

1. **Create a file** using the Write tool (NOT just return transient output)
2. **Call link-artifact** after file creation to establish bidirectional traceability
3. **Follow the report template** at `templates/report.md`
4. **Include proper frontmatter** with PS and exploration references

## Output Location

```
docs/reports/{ps-id}-{entry-id}-{report-type}.md
```

Example: `docs/reports/phase-38.17-e-041-phase-status.md`

## Report Types

| Type | Purpose | Output Sections |
|------|---------|-----------------|
| `phase-status` | Phase progress overview | Status, Deliverables, Blockers, Next Steps |
| `constraint-status` | Constraint satisfaction report | Per-constraint status, Evidence, Gaps |
| `knowledge-summary` | KB items generated in phase | ASM, LES, PAT, ADR counts with highlights |
| `experience-wisdom` | Experience/Wisdom synthesis | Experiences, Wisdoms, Relationships |

## Required Frontmatter

```yaml
---
ps: {PS_ID}
exploration: {ENTRY_ID}
created: {DATE}
status: REPORT
agent: ps-reporter
type: {REPORT_TYPE}
---
```

## Invocation Protocol

When invoking this agent via Task tool, the prompt MUST include:

```markdown
## PS CONTEXT (REQUIRED)
- **PS ID:** {ps_id}
- **Entry ID:** {entry_id} (create with add-entry if not exists)
- **Report Type:** {report_type}

## MANDATORY PERSISTENCE (c-009)
After generating the report, you MUST:

1. Use the Write tool to create your report at:
   `sidequests/evolving-claude-workflow/docs/reports/{ps_id}-{entry_id}-{report_type}.md`

2. Use the report template structure from:
   `.claude/skills/problem-statement/templates/report.md`

3. Run this command to link the artifact:
   ```bash
   python3 .claude/skills/problem-statement/scripts/cli.py link-artifact \
       {ps_id} {entry_id} FILE \
       "docs/reports/{ps_id}-{entry_id}-{report_type}.md" \
       "{Report description}"
   ```

DO NOT return transient output only. File creation AND link-artifact are MANDATORY.
```

## Report Sections by Type

### Phase Status Report

1. Executive Summary
2. Phase Overview (ID, Title, Status, Dates)
3. Deliverables Checklist
4. Constraint Satisfaction Status
5. Open Questions
6. Blockers and Risks
7. Next Steps
8. PS Integration

### Constraint Status Report

1. Executive Summary
2. Constraint Inventory (with IDs)
3. Per-Constraint Analysis
   - Status: VALIDATED | PARTIAL | UNVALIDATED | BLOCKED
   - Evidence: Test files, code references, documentation
   - Gaps: What's missing
4. Aggregate Metrics (validated/total)
5. Recommendations
6. PS Integration

### Knowledge Summary Report

1. Executive Summary
2. Knowledge Metrics
   - Assumptions: count, pending, validated
   - Lessons: count, by category
   - Patterns: count, by category
   - Decisions: count, by status
3. Key Items Highlights
4. Knowledge Graph Summary
5. Recommendations for Promotion
6. PS Integration

### Experience/Wisdom Report

1. Executive Summary
2. Experiences Recorded
   - Per experience: context, insight, applicability
3. Wisdoms Synthesized
   - Per wisdom: contributing experiences, confidence
4. Relationship Graph
5. Recommendations
6. PS Integration

## Post-Completion Commands

After report generation, the agent should run:

```bash
# Link the report artifact
python3 .claude/skills/problem-statement/scripts/cli.py link-artifact \
    {ps_id} {entry_id} FILE \
    "docs/reports/{ps_id}-{entry_id}-{report_type}.md" \
    "Phase {ps_id} {report_type} report"
```

## Integration with Enforcement Tiers (c-009)

| Tier | Enforcement Point |
|------|-------------------|
| Advisory | SessionStart reminder to use ps-reporter correctly |
| Soft | Stop hook warns if Task invoked without file creation |
| Medium | PreToolUse injects persistence reminder into prompt |
| Hard | PostToolUse blocks if file not created after Task completes |

---

## Example Complete Invocation

```python
# 1. Create exploration entry first
python3 .claude/skills/problem-statement/scripts/cli.py add-entry phase-38.17 \
    "Report: Phase Status" \
    --type REPORT --severity LOW
# Returns: e-041

# 2. Invoke ps-reporter with full context
Task(
    description="ps-reporter: Phase status",
    subagent_type="general-purpose",
    prompt="""
You are the ps-reporter agent.

## PS CONTEXT (REQUIRED)
- **PS ID:** phase-38.17
- **Entry ID:** e-041
- **Report Type:** phase-status

## MANDATORY PERSISTENCE (c-009)
After generating the report, you MUST:

1. Use the Write tool to create your report at:
   `sidequests/evolving-claude-workflow/docs/reports/phase-38.17-e-041-phase-status.md`

2. Use the report template structure from:
   `.claude/skills/problem-statement/templates/report.md`

3. Run this command to link the artifact:
   ```bash
   python3 .claude/skills/problem-statement/scripts/cli.py link-artifact \
       phase-38.17 e-041 FILE \
       "docs/reports/phase-38.17-e-041-phase-status.md" \
       "Phase 38.17 status report"
   ```

DO NOT return transient output only. File creation AND link-artifact are MANDATORY.

## YOUR REPORT TASK
Generate a phase status report for phase-38.17.
"""
)

# 3. Verify after completion
ls docs/reports/phase-38.17-e-041-*.md
python3 .claude/skills/problem-statement/scripts/cli.py view phase-38.17 | grep e-041
```