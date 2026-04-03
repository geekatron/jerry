# STORY-018: Execute Governance YAML Migration (51 Files)

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Mechanical migration of tool_tier values across 51 governance YAML files
-->

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-03-28T18:00:00Z
> **Due:**
> **Completed:** 2026-03-28T22:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | What needs to happen |
| [Migration Specification](#migration-specification) | Exact file changes |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist by skill |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry framework maintainer

**I want** all 51 governance YAML `tool_tier` fields updated to reflect the new Persistent-First Linear model

**So that** every agent's tier classification matches the authoritative tier definitions in agent-development-standards.md

---

## Summary

The migration reclassifies 51 of 89 governance YAML files:

| Change | Count | Agents |
|--------|-------|--------|
| T3 → T4 | 49 | All current-T3 agents (eng-*, red-*, ps-analyst, ps-researcher, etc.) |
| T4 → T3 | 2 | ts-parser, ts-extractor |
| Unchanged | 38 | T1 (4), T2 (28), T4-with-web (5), T5 (1) |

The migration uses the ADR's 3-step protection pattern (T3_HOLD intermediate value) and handles three YAML value formats:
- Unquoted: `tool_tier: T3`
- Quoted: `tool_tier: "T3"`
- **Inline comment** (VALIDATED BUG): `tool_tier: T3  # comment` — the sed `$` anchor fails because the line doesn't end with `T3`. Affects `diataxis-explanation.governance.yaml` (confirmed 1 file).

**Verification grep caveat:** `grep -rl 'tool_tier:.*T2'` returns a false positive on `diataxis-explanation.governance.yaml` because its inline comment contains "Upgraded from T2". Verification patterns must use precise matching (see below).

**Skills informing this story:**
- `/eng-team` (eng-lead): Script safety, pre/post validation, rollback testing
- `/eng-team` (eng-security): Verify no agents gain unintended tool access
- `/problem-solving` (ps-validator): Post-migration schema validation of all 89 governance YAMLs
- `/adversary` (adv-executor): Verify migration completeness via independent audit

---

## Migration Specification

### Pre-Migration Audit (Step 0)

```bash
# Baseline counts (precise patterns to avoid false positives from inline comments)
grep -Prl 'tool_tier:\s*"?T1"?\s*(#|$)' skills/*/agents/*.governance.yaml | wc -l  # Expected: 4
grep -Prl 'tool_tier:\s*"?T2"?\s*(#|$)' skills/*/agents/*.governance.yaml | wc -l  # Expected: 28
grep -Prl 'tool_tier:\s*"?T3"?\s*(#|$)' skills/*/agents/*.governance.yaml | wc -l  # Expected: 49
grep -Prl 'tool_tier:\s*"?T4"?\s*(#|$)' skills/*/agents/*.governance.yaml | wc -l  # Expected: 7
grep -Prl 'tool_tier:\s*"?T5"?\s*(#|$)' skills/*/agents/*.governance.yaml | wc -l  # Expected: 1
# NOTE: -P enables Perl regex. The pattern matches the tier value at the start of the value
# position, then optional quote, then optional space+comment or end-of-line.
# This avoids false positives from inline comments mentioning other tier numbers
# (e.g., diataxis-explanation.governance.yaml mentions "T2" in a T3 line comment).
#
# EXECUTOR NOTE: If using simple grep (without -P), T2 count will show 29 instead of 28.
# This is a false positive: diataxis-explanation.governance.yaml has tool_tier: T3 with
# an inline comment containing "Upgraded from T2". The precise pattern above returns 28.
# If you see 29 with simple grep, this is expected and NOT a migration error.

# MK anomaly check: no T3 agent should already have memory-keeper
grep -rl 'memory-keeper' skills/*/agents/*.md | while read f; do
  if grep -q 'tool_tier:.*T3' "${f%.md}.governance.yaml" 2>/dev/null; then echo "ANOMALY: $f"; fi
done
# Expected: no output
```

### Migration Script (Steps 1-3)

```bash
# Step 1: Protect ts-parser and ts-extractor
sed -i '' 's/tool_tier: T4/tool_tier: T3_HOLD/' skills/transcript/agents/ts-parser.governance.yaml
sed -i '' 's/tool_tier: T4/tool_tier: T3_HOLD/' skills/transcript/agents/ts-extractor.governance.yaml

# Step 2: T3 → T4 (three formats: unquoted, quoted, inline comment)
for file in $(grep -rl 'tool_tier:.*T3' skills/*/agents/*.governance.yaml); do
  sed -i '' 's/tool_tier: T3$/tool_tier: T4/' "$file"           # unquoted, no comment
  sed -i '' 's/tool_tier: "T3"$/tool_tier: "T4"/' "$file"       # quoted, no comment
  sed -i '' 's/tool_tier: T3  #/tool_tier: T4  #/' "$file"      # inline comment (diataxis-explanation)
done

# Step 3: Finalize ts-parser and ts-extractor
sed -i '' 's/tool_tier: T3_HOLD/tool_tier: T3/' skills/transcript/agents/ts-parser.governance.yaml
sed -i '' 's/tool_tier: T3_HOLD/tool_tier: T3/' skills/transcript/agents/ts-extractor.governance.yaml
```

### Post-Migration Verification (Step 4)

| Check | Command | Expected |
|-------|---------|----------|
| T1 count | `grep -Prl 'tool_tier:\s*"?T1"?\s*(#\|$)' skills/*/agents/*.governance.yaml \| wc -l` | 4 |
| T2 count | `grep -Prl 'tool_tier:\s*"?T2"?\s*(#\|$)' skills/*/agents/*.governance.yaml \| wc -l` | 28 |
| T3 count | `grep -Prl 'tool_tier:\s*"?T3"?\s*(#\|$)' skills/*/agents/*.governance.yaml \| wc -l` | 2 |
| T4 count | `grep -Prl 'tool_tier:\s*"?T4"?\s*(#\|$)' skills/*/agents/*.governance.yaml \| wc -l` | 54 |
| T5 count | `grep -Prl 'tool_tier:\s*"?T5"?\s*(#\|$)' skills/*/agents/*.governance.yaml \| wc -l` | 1 |
| T3 agents | `grep -rl 'tool_tier:.*T3' skills/*/agents/*.governance.yaml` | ts-parser, ts-extractor only |
| No T3_HOLD | `grep -rl 'T3_HOLD' skills/*/agents/*.governance.yaml` | (empty) |
| Total | Sum | 89 |

---

## Acceptance Criteria

### /eng-team (eng-lead): Script Safety

- [ ] Pre-migration audit passes (counts match expected, no MK anomalies)
- [ ] Migration script handles all three YAML forms: unquoted (`T3`), quoted (`"T3"`), and inline comment (`T3  # ...`)
- [ ] T3_HOLD intermediate value fully resolved (no residual T3_HOLD in any file)
- [ ] Post-migration verification passes all 8 checks
- [ ] Migration and rule file changes are in the same commit (atomic)

### /eng-team (eng-security): Access Control Integrity

- [ ] No agent's `.md` frontmatter `tools` or `mcpServers` fields changed (migration is governance-only)
- [ ] No agent gains actual tool access it didn't have before
- [ ] ts-parser and ts-extractor retain Memory-Keeper access (not lost during T4→T3 reclassification)

### /problem-solving (ps-validator): Schema Validation

- [ ] All 89 governance YAMLs pass `agent-governance-v1.schema.json` validation after migration
- [ ] `tool_tier` enum values are all valid (T1, T2, T3, T4, or T5)
- [ ] No YAML formatting corruption from sed operations

### /adversary (completeness audit)

- [ ] Independent recount of all 89 agents confirms correct tier assignment
- [ ] Every agent in the ADR's per-agent migration table has the correct new tier

### Rollback

- [ ] Rollback script tested (forward + rollback produces original state)
- [ ] Rollback handles all three forms: quoted, unquoted, and inline comment
- [ ] Post-rollback counts match pre-migration baseline

---

## Children (Tasks)

| ID | Title | Status | Owner | Skill |
|----|-------|--------|-------|-------|
| TASK-001 | Run pre-migration audit (Step 0 + Step 0b) | pending | -- | /eng-team |
| TASK-002 | Execute 3-step migration script | pending | -- | /eng-team |
| TASK-003 | Run post-migration verification checklist | pending | -- | /eng-team |
| TASK-004 | Validate all governance YAMLs against JSON schema | pending | -- | /problem-solving |
| TASK-005 | Test rollback script (forward + rollback = original state) | pending | -- | /eng-team |
| TASK-006 | Independent agent-by-agent tier verification | pending | -- | /adversary |

---

## Related Items

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Depends On | STORY-017 | Rule files must define new tiers before YAMLs reference them |
| Blocks | STORY-019 | Documentation references new tier assignments |
| Blocks | STORY-020 | Security assessment reviews implemented state |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-28 | adam.nowak | pending | Created -- 51-file migration with 3-step protection pattern |
| 2026-03-28 | claude | completed | 51 YAMLs migrated (49 T3→T4, 2 T4→T3). Post-migration: T1=4, T2=28, T3=2, T4=54, T5=1. All 89 tool_tier values valid. |
