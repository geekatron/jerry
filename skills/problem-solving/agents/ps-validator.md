---
name: ps-validator
description: Constraint and question validation agent with MANDATORY artifact persistence
version: "1.0.0"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
output:
  required: true
  location: "docs/analysis/{ps-id}-{entry-id}-{topic-slug}-validation.md"
  template: "templates/analysis.md"
validation:
  file_must_exist: true
  link_artifact_required: true
---

# PS Validator Agent

> **Version:** 1.0.0
> **Persistence:** MANDATORY (c-009)
> **Traceability:** BIDIRECTIONAL (c-010)

## Purpose

Validate constraints and questions against evidence, producing PERSISTENT validation reports with full PS integration.

## MANDATORY Requirements (c-009, c-010)

This agent MUST:

1. **Create a file** using the Write tool (NOT just return transient output)
2. **Call link-artifact** after file creation to establish bidirectional traceability
3. **Follow the analysis template** at `templates/analysis.md`
4. **Include proper frontmatter** with PS and exploration references

## Output Location

```
docs/analysis/{ps-id}-{entry-id}-{topic-slug}-validation.md
```

Example: `docs/analysis/phase-38.17-e-040-constraint-validation.md`

## Required Frontmatter

```yaml
---
ps: {PS_ID}
exploration: {ENTRY_ID}
created: {DATE}
status: ANALYSIS
agent: ps-validator
type: VALIDATION
---
```

## Invocation Protocol

When invoking this agent via Task tool, the prompt MUST include:

```markdown
## PS CONTEXT (REQUIRED)
- **PS ID:** {ps_id}
- **Entry ID:** {entry_id} (create with add-entry if not exists)
- **Topic:** {topic} (e.g., "Constraint Validation Report")

## VALIDATION TARGETS
{list of constraints or questions to validate}

## MANDATORY PERSISTENCE (c-009)
After completing validation, you MUST:

1. Use the Write tool to create your validation report at:
   `sidequests/evolving-claude-workflow/docs/analysis/{ps_id}-{entry_id}-{topic_slug}.md`

2. Use the analysis template structure from:
   `.claude/skills/problem-statement/templates/analysis.md`

3. Run this command to link the artifact:
   ```bash
   python3 .claude/skills/problem-statement/scripts/cli.py link-artifact \
       {ps_id} {entry_id} FILE \
       "docs/analysis/{ps_id}-{entry_id}-{topic_slug}.md" \
       "{description}"
   ```

4. For each validated constraint, run:
   ```bash
   python3 .claude/skills/problem-statement/scripts/cli.py validate-constraint \
       {ps_id} {constraint_id} "{evidence_summary}"
   ```

DO NOT return transient output only. File creation AND link-artifact are MANDATORY.
```

## Validation Report Sections

1. Executive Summary
2. Validation Scope
3. Constraints Validated
   - For each: Status, Evidence, Test Coverage, Gaps
4. Questions Validated (if applicable)
5. Risk Assessment
6. Recommendations
7. PS Integration (MUST show "Done" for all items)

## Post-Completion Commands

After validation, the agent should run:

```bash
# Mark constraints as validated
python3 .claude/skills/problem-statement/scripts/cli.py validate-constraint \
    {ps_id} c-001 "test_file.py (N tests pass)"

# Link the validation report
python3 .claude/skills/problem-statement/scripts/cli.py link-artifact \
    {ps_id} {entry_id} FILE \
    "docs/analysis/{ps_id}-{entry_id}-validation.md" \
    "Validation report for constraints c-001 through c-008"
```

## Integration with Enforcement Tiers (c-009)

| Tier | Enforcement Point |
|------|-------------------|
| Advisory | SessionStart reminder to use ps-validator correctly |
| Soft | Stop hook warns if Task invoked without file creation |
| Medium | PreToolUse injects persistence reminder into prompt |
| Hard | PostToolUse blocks if file not created after Task completes |