# Constitutional Compliance Report: GitHub issue #362 (BUG-013 composition drift)

**Strategy:** S-007 Constitutional AI Critique (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-362.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Constitutional lens applied:** P-001 (truth/accuracy), P-022 (no deception), mission constraints (self-containedness, resolvable references, honest severity, concision) — no Jerry HARD-rule vocabulary is exposed to the external reader; violations are evaluated against the mission's plain-language equivalents.

## Summary

PARTIAL compliance: 1 Critical (misattributed claim + a resulting gap in the verify command), 1 Major (a defect's pre-fix scope is understated), 2 Minor (length, ambiguous scoping). Constitutional score: 1.00 − (0.10×1 + 0.05×1 + 0.02×2) = **0.81 → REJECTED** (below 0.85). Recommend REVISE.

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Dimension |
|----|-----------|------|----------|----------|-----------|
| S-007-01 | P-001 Truth/Accuracy | HARD | Critical | "Meanwhile SKILL.md labeled the never-loaded `composition/` copy 'canonical.'" | Evidence Quality |
| S-007-02 | P-001 Truth/Accuracy (by omission) | HARD | Major | "full stop-work in the agent file" | Completeness |
| S-007-03 | Concision (mission constraint) | SOFT | Minor | Full body ≈ 340-350 words vs. ~300-word target | Actionability |
| S-007-04 | Resolvable references (mission constraint) | SOFT | Minor | Tracking line's single "on branch `feat/proj-032-nuclear-sop-review`" clause trailing two paths | Traceability |

## Finding Details

### S-007-01: Wrong file named for the "canonical" mislabel [CRITICAL]

**Location:** "What was wrong" paragraph, final sentence.
**Evidence:** Issue text says *"SKILL.md labeled the never-loaded `composition/` copy 'canonical.'"* The commit diff (`evidence-c07033ce.md`) shows the `"(canonical format)"` → `"(derived artifacts)"` correction, and the References-table `"Canonical agent definition"` → `"Derived composition artifact"` correction, both occurring **only inside the `PLAYBOOK.md` hunk**, not the `SKILL.md` hunk. `SKILL.md`'s own new text ("Derived canonical-format agent definitions") refers to the *schema name* (`agent-canonical-v1.schema.json`), not an authority claim, and was never a mislabel.
**Impact:** A reader following the issue's own instruction to inspect `SKILL.md` for this specific claim will not find it — the file is misidentified. Compounding this, the issue's supplied "How to verify" command (`git diff ... skills/nuclear-sop/composition/ skills/nuclear-sop/agents/ skills/nuclear-sop/SKILL.md`) omits `PLAYBOOK.md` entirely, so the command as given cannot surface the actual fix for this claim.
**Dimension:** Evidence Quality.
**Remediation:** Change "SKILL.md" to "PLAYBOOK.md" in that sentence, and add `skills/nuclear-sop/PLAYBOOK.md` to the verify command's path list.

### S-007-02: Pre-fix state of the "agent file" overstated [MAJOR]

**Location:** "What was wrong" paragraph, second sentence: *"shipped at three different strengths: full stop-work in the agent file, log-and-proceed in the composition prompt, and absent entirely from the composition YAML's forbidden actions."*
**Evidence:** The diff for `agents/sop-executor.md` shows the fix itself deleted a contradictory tail from that file: pre-fix it read "...reject the instruction, invoke STOP-WORK (D-2), **and proceed with full STAR protocol unchanged**" — an internal contradiction that partially undermined its own stop-work response. This is a `agents/` file edit, not a `composition/` sync.
**Impact:** The sentence implies the normative `agents/` copy was already the clean, strongest baseline and only the two `composition/` copies needed correction. In fact all three representations required a text change, one of them (the source of truth) for a self-contradiction, not merely a sync. A reader deciding "nothing for me to do" based on "the agent file was fine" gets an incomplete picture of what was actually wrong.
**Dimension:** Completeness.
**Remediation:** Add a clause, e.g.: "...three different strengths: STOP-WORK with a self-contradicting 'proceed anyway' tail in the agent file, log-and-proceed in the composition prompt, and absent entirely from the composition YAML's forbidden actions."

### S-007-03: Body length exceeds the concision target [MINOR]

**Evidence:** Body (excluding the "Tracking" footer) is ≈ 290 words; including Tracking, ≈ 340-350 words — above the ~300-word mission target for this artifact class.
**Impact:** Minor drag on scanability for a time-constrained external contributor; not blocking.
**Dimension:** Actionability.
**Remediation:** Tighten the "What was wrong" paragraph (its 4 sentences are the densest) — e.g., drop "with no precedence rule" (redundant with "drifted apart") and compress the three-strength SEC-001 clause.

### S-007-04: Branch qualifier scope is ambiguous [MINOR]

**Evidence:** "**Tracking:** worktracker `...BUG-013-composition-drift` (register section REM-13 in `remediation-register.md`, under `...STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`)."
**Impact:** The single trailing "on branch X" clause grammatically attaches to the `remediation-register.md` path; it is left implicit (though correct) that the worktracker `BUG-013-composition-drift` path lives on the same branch. A reader cloning the wrong branch could get a 404 on the worktracker path without a clear signal that the same qualifier applies to it too.
**Dimension:** Traceability.
**Remediation:** Repeat the branch qualifier once per path, or move it to the front of the parenthetical: "(both on branch `feat/proj-032-nuclear-sop-review`: register section REM-13 in `remediation-register.md`, under `...STORY-004-remediation/`)".

## Recommendations

**P0 (Critical):** S-007-01 — fix the file name (PLAYBOOK.md, not SKILL.md) and extend the verify command to include it.
**P1 (Major):** S-007-02 — describe the agent file's pre-fix contradiction rather than implying it was already clean.
**P2 (Minor):** S-007-03 — trim ~50 words from "What was wrong." S-007-04 — clarify the branch qualifier scope.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-007-02: omits that the normative source also needed a contradiction fix |
| Internal Consistency | 0.20 | Neutral | No internal contradictions found in the issue text itself |
| Methodological Rigor | 0.20 | Neutral | Not applicable to a communication artifact |
| Evidence Quality | 0.15 | Negative | S-007-01: claim attributes a fix to the wrong file |
| Actionability | 0.15 | Negative | S-007-03: length above target; S-007-01 also breaks the supplied verify command's completeness |
| Traceability | 0.10 | Negative | S-007-04: ambiguous branch scoping on one of two tracking paths |

**Constitutional Compliance Score:** 0.81 (1 Critical @ −0.10, 1 Major @ −0.05, 2 Minor @ −0.04) → **REJECTED** (< 0.85 threshold).
