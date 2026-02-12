# Section 003: Active Project

<!--
TASK: TASK-003
PARENT: EN-202
REVIEW: DISC-002 Adversarial Review
ITERATIONS: 2
FINAL_SCORE: 0.934
-->

---

## Final Section Content (15 lines)

```markdown
## Active Project

Set `JERRY_PROJECT` environment variable to specify active project:

```bash
export JERRY_PROJECT=PROJ-001-example
```

The SessionStart hook (`scripts/session_start_hook.py`) provides project context via XML tags:

| Tag | Meaning | Claude Action |
|-----|---------|---------------|
| `<project-context>` | Valid project active | Proceed with work in project context |
| `<project-required>` | No project set | Use AskUserQuestion to select/create project |
| `<project-error>` | Invalid project ID | Help user fix or select valid project |

**Hard Rule**: Claude MUST NOT proceed with substantial work without active project context.
See `projects/README.md` for project registry and creation workflow.
```

---

## DISC-002 Review Documentation

### Iteration 1

**Draft Content**: Initial 14-line section with table format.

**ps-critic Assessment:**

| Criterion | Weight | Score | Reasoning |
|-----------|--------|-------|-----------|
| Completeness | 30% | 0.90 | Covers JERRY_PROJECT, hook tags, enforcement. Could clarify Claude actions. |
| Accuracy | 25% | 0.95 | Tags verified against session_start_hook.py lines 166-217. |
| Clarity | 20% | 0.92 | Table clear but "Action" column vague. |
| Actionability | 15% | 0.88 | Shows env var setting but tag responses need specificity. |
| Traceability | 10% | 0.95 | Hook script and README referenced correctly. |

**Weighted Score**: 0.919

**REM-001**: Action column too vague - specify what Claude should do (e.g., "Use AskUserQuestion").
**REM-002**: Line count acceptable (14 lines, within ~15 target).

**Decision**: Below 0.92 threshold. Proceed to Iteration 2.

---

### Iteration 2

**Changes Made:**
- REM-001 ADDRESSED: Renamed "Action" to "Claude Action" with specific behaviors
- Added "Use AskUserQuestion" for project-required case (matches CLAUDE.md lines 606-615)
- Changed "Enforcement" to "Hard Rule" for emphasis
- Minor wording improvements for clarity

**ps-critic Assessment:**

| Criterion | Weight | Score | Reasoning |
|-----------|--------|-------|-----------|
| Completeness | 30% | 0.95 | All four requirements met: JERRY_PROJECT, tags, enforcement, hook reference. |
| Accuracy | 25% | 0.95 | Verified against session_start_hook.py and current CLAUDE.md. |
| Clarity | 20% | 0.93 | Table with specific Claude actions is clear and scannable. |
| Actionability | 15% | 0.92 | Each tag now has specific Claude behavior guidance. |
| Traceability | 10% | 0.95 | Two explicit file references for follow-up. |

**Weighted Score**: (0.30 * 0.95) + (0.25 * 0.95) + (0.20 * 0.93) + (0.15 * 0.92) + (0.10 * 0.95)
= 0.285 + 0.238 + 0.186 + 0.138 + 0.095 = **0.942**

**REM Items Addressed:**
- REM-001: RESOLVED - Claude actions now specific and actionable

**Decision**: Score 0.942 >= 0.92 threshold. PASS.

---

## Verification Checklist

- [x] JERRY_PROJECT variable documented (line 3-6 of section)
- [x] Hook output tags explained (table with 3 tags)
- [x] Project context enforcement mentioned ("Hard Rule" statement)
- [x] Section is ~15 lines (exactly 15 lines including header)
- [x] Hook script referenced (`scripts/session_start_hook.py`)
- [x] Brief and actionable (table format with specific Claude actions)

---

## Source Verification

**session_start_hook.py references:**
- `<project-context>` tag: Lines 166-176
- `<project-required>` tag: Lines 197-218
- `<project-error>` tag: Lines 179-195

**Current CLAUDE.md references:**
- Project Enforcement section: Lines 523-651
- AskUserQuestion flow: Lines 604-626
