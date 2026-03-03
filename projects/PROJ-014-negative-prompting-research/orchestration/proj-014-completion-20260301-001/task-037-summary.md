# TASK-037 Summary: Framing Vocabulary Standardization in 12 SKILL.md Files

> **Task:** Convert "Do NOT use when:" bullet lists to NPT-013 NEVER-framed format with consequences
> **Date:** 2026-03-01
> **Rationale:** PG-003 (CONDITIONAL GO, p=0.016) + G-001 (NPT-013 structured negation achieves 100% compliance vs 92.2% for positive-only framing)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Results Summary](#results-summary) | Aggregate counts |
| [Per-File Status](#per-file-status) | Detailed status for each of 12 files |
| [Change Details](#change-details) | Before/after patterns for edited files |
| [Verification](#verification) | Post-edit validation results |

---

## Results Summary

| Metric | Count |
|--------|-------|
| Total files checked | 12 |
| Files edited (had "Do NOT use when:" bullets) | 6 |
| Files with no changes needed | 6 |
| Unexpected findings | 0 |

---

## Per-File Status

| # | File | Status | Notes |
|---|------|--------|-------|
| 1 | `skills/problem-solving/SKILL.md` | No change needed | No "Do NOT use when:" section present; only has Routing Disambiguation table |
| 2 | `skills/nasa-se/SKILL.md` | No change needed | No "Do NOT use when:" section present; only has Routing Disambiguation table |
| 3 | `skills/orchestration/SKILL.md` | **Edited** | Converted 3 bullets from "Do NOT use when:" to NEVER format with consequences |
| 4 | `skills/adversary/SKILL.md` | **Edited** | Converted 6 bullets from "Do NOT use when:" to NEVER format with consequences |
| 5 | `skills/worktracker/SKILL.md` | No change needed | No "Do NOT use when:" section present; only has Routing Disambiguation table |
| 6 | `skills/saucer-boy/SKILL.md` | **Edited** | Converted 5 bullets from "Do NOT use when:" to NEVER format with consequences |
| 7 | `skills/saucer-boy-framework-voice/SKILL.md` | **Edited** | Converted 4 bullets from "Do NOT use when:" to NEVER format with consequences |
| 8 | `skills/transcript/SKILL.md` | No change needed | No "Do NOT use when:" section present |
| 9 | `skills/ast/SKILL.md` | **Edited** | Converted 2 bullets from "Do NOT use `/ast` for:" to NEVER format with consequences |
| 10 | `skills/eng-team/SKILL.md` | No change needed | No "Do NOT use when:" section present |
| 11 | `skills/red-team/SKILL.md` | **Edited** | Converted 5 bullets from "Do NOT use when:" to NEVER format with consequences |
| 12 | `skills/architecture/SKILL.md` | No change needed | No "Do NOT use when:" section present |

---

## Change Details

### Pattern Applied

All edits followed the same conversion pattern:

**FROM:**
```markdown
**Do NOT use when:**
- {condition} ({redirect})
```

**TO:**
```markdown
NEVER invoke this skill when:
- {condition} -- Consequence: {impact explanation}; {redirect if applicable}
```

### orchestration/SKILL.md (3 bullets)

| Original Bullet | Converted Form |
|-----------------|----------------|
| Single agent task (use problem-solving skill instead) | Task requires a single agent only -- Consequence: Orchestration overhead...wastes significant context budget; use `/problem-solving` instead |
| Simple sequential flow (use direct agent invocation) | Flow is simple and sequential without parallel pipelines -- Consequence: Three artifacts created...artifact overhead exceeds task complexity; use direct agent invocation |
| No cross-session state needed | No cross-session state persistence is needed -- Consequence: YAML state management and checkpointing infrastructure adds complexity without value |

### adversary/SKILL.md (6 bullets)

| Original Bullet | Converted Form |
|-----------------|----------------|
| You need a creator-critic-revision loop | Task requires iterative creator-critic-revision loop -- Consequence: one-shot assessment produces premature rejection without revision pathway |
| You need routine code review for quick defect checks | Task is routine code review for quick defect checks -- Consequence: full strategy template execution wastes context budget |
| You need constraint validation | Task is binary constraint validation -- Consequence: strategies assess quality dimensions, not binary compliance |
| Working on routine code changes at C1 criticality | Work is routine code changes at C1 criticality -- Consequence: disproportionate context budget for low-risk work |
| Fixing defects or bugs with obvious solutions | Defects or bugs have obvious solutions -- Consequence: evaluates existing deliverables, not diagnose root causes |
| User explicitly requests a quick review without adversarial rigor | User explicitly requests a quick review -- Consequence: overriding preference violates P-020 |

### saucer-boy/SKILL.md (5 bullets)

| Original Bullet | Converted Form |
|-----------------|----------------|
| Producing framework output (quality gates, error messages, hooks) | Producing framework output -- Consequence: conversational voice violates voice consistency standards; requires rewrite |
| In a constitutional failure or governance escalation | Constitutional failure or governance escalation is active -- Consequence: personality obscures critical information |
| Security-relevant operations | Security-relevant operations are in progress -- Consequence: personality flair reduces clarity |
| User explicitly requests formal/neutral tone | User explicitly requests formal/neutral tone -- Consequence: overriding preference violates P-020 |
| Writing internal design docs, ADRs, or research artifacts | Writing internal design docs, ADRs, or research artifacts -- Consequence: personality undermines precision and auditability |

### saucer-boy-framework-voice/SKILL.md (4 bullets)

| Original Bullet | Converted Form |
|-----------------|----------------|
| Modifying how Claude agents reason or converse | Task involves modifying how Claude agents reason or converse -- Consequence: persona voice calibration produces behavioral interference |
| Adding personality to messages that should be neutral | Messages should be neutral -- Consequence: voice fidelity scoring during hard stops delays critical information |
| Working on non-framework-output text | Working on non-framework-output text -- Consequence: framework voice calibration introduces personality where precision is required |
| The text is a governance escalation or security-relevant failure | Text is a governance escalation or security-relevant failure -- Consequence: humor deployment violates boundary condition #3 |

### red-team/SKILL.md (5 bullets)

| Original Bullet | Converted Form |
|-----------------|----------------|
| Building secure software | Task is building secure software (defensive security) -- Consequence: offensive methodology produces attack narratives instead of hardened code |
| Performing adversarial quality reviews of deliverables | Task is adversarial quality review -- Consequence: produces engagement reports instead of quality scores |
| Conducting general security research without engagement context | General security research without engagement context -- Consequence: agents require authorized scope documents |
| No active scope document exists and no engagement is being planned | No active scope document exists -- Consequence: operations without scope authorization violate engagement methodology |
| The target is outside any authorized engagement boundary | Target is outside authorized engagement boundary -- Consequence: out-of-scope testing violates rules of engagement |

### ast/SKILL.md (2 bullets)

| Original Bullet | Converted Form |
|-----------------|----------------|
| Reading raw file content (use Read tool directly) | Reading raw file content without structural parsing -- Consequence: AST parsing overhead wastes CLI invocation cost |
| Writing arbitrary content to files (use Write/Edit tools directly) | Writing arbitrary content to files -- Consequence: AST modify is scoped to frontmatter field updates only; arbitrary writes fail |

---

## Verification

Post-edit validation confirms:

| Check | Result |
|-------|--------|
| `grep "NEVER invoke this skill when:" skills/*/SKILL.md` | 6 files match (all 6 edited files) |
| `grep "Do NOT use" skills/*/SKILL.md` | 0 files match (all instances converted) |
| All "See [Routing Disambiguation]..." links preserved | Confirmed in all 6 edited files |
| Routing Disambiguation tables (from TASK-036) untouched | Confirmed -- no table rows modified |

---

*Generated: 2026-03-01*
*Agent: Claude Opus 4.6 (direct execution, no subagent)*
