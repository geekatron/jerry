# EN-926 Adversarial Critic Report

**Criticality:** C3 (AE-002 auto-escalation - touches `.context/rules/`)
**Deliverables:**
- `.context/rules/mandatory-skill-usage.md`
- `.context/rules/quality-enforcement.md`
- `skills/adversary/SKILL.md`

**Reviewer:** Claude Sonnet 4.5
**Review Date:** 2026-02-16
**Strategies Applied:** S-014, S-007, S-002, S-004, S-012, S-013 (C3 required set)

---

## Executive Summary

**VERDICT: REVISE (Score: 0.88)**

The rule synchronization successfully adds `/adversary` to the H-22 trigger map and creates implementation guidance, but falls short of the 0.92 threshold due to **critical keyword overlap issues**, **ambiguous guidance**, and **incomplete FMEA coverage**. The deliverables meet basic requirements but introduce confusion that could cause Claude to invoke the wrong skill.

**Critical Issues (MUST FIX):**
1. Keyword overlap between `/adversary` and `/problem-solving` creates ambiguous triggers
2. Implementation section doesn't clearly distinguish when to use `/adversary` vs ps-critic for quality scoring
3. SKILL.md "When NOT to use" section contradicts its own purpose

**Impact:** Medium risk of skill invocation confusion, leading to workflow inefficiency or incorrect review application.

---

## S-014 LLM-as-Judge Scoring

| Dimension | Weight | Score | Justification |
|-----------|--------|-------|---------------|
| **Completeness** | 0.20 | 0.85 | All 3 ACs addressed, but Implementation section is thin. Missing: explicit escalation path when both skills could apply. Missing: guidance for "quality review" keyword which overlaps with ps-critic. |
| **Internal Consistency** | 0.20 | 0.80 | CONTRADICTION: SKILL.md says "Do NOT use when: You need code review or defect detection (use ps-reviewer)" but `/adversary` includes "quality review" trigger which IS code/defect review context. Trigger map has "evaluate quality" but ps-critic also evaluates quality. |
| **Methodological Rigor** | 0.20 | 0.90 | Trigger keywords correctly reference adversarial strategies. Implementation section correctly links to agents. H-22 rule language preserved. SKILL.md triple-lens format applied. |
| **Evidence Quality** | 0.15 | 0.85 | Keywords match actual adversary capabilities (tournament, red team, steelman). SKILL.md correctly cites SSOT. BUT: no evidence that "quality review" won't collide with ps-critic invocation. |
| **Actionability** | 0.15 | 0.90 | Clear trigger map. Implementation section provides paths to agents. SKILL.md has concrete usage examples. Keywords are recognizable. |
| **Traceability** | 0.10 | 1.00 | H-22 reference maintained. Strategy IDs cited (S-014, S-007, etc.). SSOT version updated. SKILL.md references quality-enforcement.md. |

**Weighted Composite:** (0.85×0.20) + (0.80×0.20) + (0.90×0.20) + (0.85×0.15) + (0.90×0.15) + (1.00×0.10) = **0.88**

**Threshold:** 0.92 (C2+ deliverables per H-13)

**Outcome:** REVISE (below threshold per H-13)

---

## S-007 Constitutional AI Critique

### Constitutional Violations: NONE FOUND

All HARD rules preserved:
- H-22 rule text intact, only extended with `/adversary` clause
- No P-003 violations (no recursive subagents introduced)
- No P-020 violations (user authority preserved)
- No P-022 violations (no deception about capabilities)

### Constitutional Concerns: 2 WARNINGS

**W-1: Potential P-022 Deception Risk (Misleading Triggers)**

The keyword "quality review" in the `/adversary` trigger map could mislead Claude into thinking `/adversary` is the ONLY quality review skill, when ps-critic also performs quality reviews. This is not active deception, but could create misleading impressions about skill boundaries.

**Recommendation:** Add "adversarial quality review" instead of bare "quality review" to clarify the distinction.

**W-2: H-22 Enforcement Ambiguity**

H-22 says "MUST invoke /adversary for adversarial quality reviews and tournament scoring" but doesn't define when a quality review is "adversarial" vs "iterative critique." This creates an enforcement gap where Claude might invoke either skill for the same scenario.

**Recommendation:** Add clarifying language: "MUST invoke /adversary for standalone adversarial reviews outside creator-critic loops."

---

## S-002 Devil's Advocate

### Challenge 1: "Why not just use ps-critic for everything?"

The deliverables claim `/adversary` and `ps-critic` are complementary, but the trigger keywords suggest they're competing for the same invocation contexts:

- Both handle "quality review"
- Both apply adversarial strategies
- Both produce quality scores using S-014

**Counter-argument from deliverables:** `/adversary` is for standalone/tournament reviews, ps-critic is for embedded loops.

**Devil's Advocate rebuttal:** If they're truly complementary, why does the trigger map include "quality review" which is generic? A user asking "can you do a quality review of this ADR" could trigger either skill. The deliverables don't resolve this ambiguity.

**Verdict:** The distinction exists but is poorly communicated in the trigger map. The SKILL.md "When to Use /adversary vs ps-critic" section is excellent, but the trigger keywords don't reflect that nuance.

### Challenge 2: "The Implementation section is just a list of links"

The quality-enforcement.md Implementation section (lines 194-218) says "see this file" and "see that agent" but doesn't actually IMPLEMENT anything. It's a reference list, not implementation guidance.

**Counter-argument:** It provides clear pointers to operational components.

**Devil's Advocate rebuttal:** A section titled "Implementation" should describe HOW the framework is applied operationally, not WHERE to find the pieces. For example: "When Claude detects adversarial review keywords per H-22, it invokes /adversary skill. The adv-selector agent maps criticality to strategies. The adv-executor agent loads templates from .context/templates/adversarial/. The adv-scorer agent produces S-014 scores."

**Verdict:** The section is a navigation aid masquerading as implementation guidance. Rename to "Operational Components" or expand with actual workflow description.

### Challenge 3: "Why would I ever NOT use adversary skill for quality?"

The SKILL.md says:

> **Do NOT use when:**
> - You need a creator-critic-revision loop (use `/problem-solving` with ps-critic instead)
> - You need code review or defect detection (use ps-reviewer)

But the H-22 trigger map includes "quality review" which INCLUDES code review and defect detection contexts. This creates a contradiction: the trigger map says "yes" but the guidance says "no."

**Counter-argument:** "Quality review" in the trigger map means "adversarial quality review."

**Devil's Advocate rebuttal:** That's not what it says. The word "adversarial" is a separate trigger, not a modifier of "quality review."

**Verdict:** Ambiguous guidance that could cause Claude to invoke `/adversary` for routine code review when ps-reviewer is more appropriate.

---

## S-004 Pre-Mortem Analysis

**Scenario:** It's 2026-03-01. EN-926 has been merged and deployed. Claude Code sessions are experiencing skill invocation confusion and workflow delays.

### Failure Mode 1: "Claude invoked `/adversary` when I just wanted a quick code review"

**What went wrong:** User said "can you review this code for quality issues?" Claude saw "quality review" in the H-22 trigger map and invoked `/adversary` skill, which launched adv-selector, attempted to load strategy templates, and produced a multi-page tournament report when the user just wanted a 5-minute sanity check.

**Root cause:** Keyword "quality review" is too generic. It captures routine quality checks that should go to ps-reviewer.

**Prevention:** Replace "quality review" with "adversarial quality review" or "tournament quality review."

### Failure Mode 2: "Claude invoked `/problem-solving` with ps-critic when I explicitly asked for adversary skill"

**What went wrong:** User said "I need a rigorous critique of this architecture decision" and Claude invoked `/problem-solving` with ps-critic instead of `/adversary` because "critique" is a problem-solving keyword too.

**Root cause:** The trigger keywords don't include "critique" for `/adversary`, only for `/problem-solving`.

**Prevention:** Add "rigorous critique" or "formal critique" to `/adversary` trigger map.

### Failure Mode 3: "I asked for tournament scoring but got a regular critic report"

**What went wrong:** User said "score this deliverable" and Claude invoked ps-critic which produced a score, but not the full C4 tournament with all 10 strategies.

**Root cause:** "Score" is in both trigger maps (implicitly for ps-critic via "evaluate quality"). The distinction between "scoring" (generic) and "tournament scoring" (specific) is not clear in triggers.

**Prevention:** Make "tournament" a stronger trigger. Add "C4 review" as explicit trigger (already present, good).

### Failure Mode 4: "The Implementation section didn't help me understand when to use which skill"

**What went wrong:** Developer read quality-enforcement.md Implementation section to understand when to invoke `/adversary` vs ps-critic, but only found file paths and agent names. Had to read both SKILL.md files to understand the distinction.

**Root cause:** Implementation section is a reference list, not decision guidance.

**Prevention:** Add a decision tree or usage scenarios to Implementation section, OR rename to "Operational Components" to set correct expectations.

---

## S-012 FMEA (Failure Mode and Effects Analysis)

| Failure Mode | Severity (1-5) | Likelihood (1-5) | Detection (1-5) | RPN | Mitigation |
|--------------|----------------|------------------|-----------------|-----|------------|
| FM-1: Keyword overlap causes wrong skill invocation | 3 (Medium - workflow delay, wrong output format) | 4 (High - "quality review" is common phrase) | 2 (Easy - user will notice wrong skill activated) | 24 | Replace "quality review" with "adversarial quality review" |
| FM-2: Missing "critique" keyword causes adversary skill under-invocation | 2 (Low - user can explicitly invoke) | 3 (Medium - "critique" is common request) | 3 (Moderate - user may not realize they got wrong review type) | 18 | Add "rigorous critique" to trigger map |
| FM-3: Implementation section misleads readers | 2 (Low - navigation inconvenience) | 2 (Low - most users read SKILL.md first) | 4 (Hard - title suggests it's implementation guidance) | 16 | Rename to "Operational Components" OR expand with workflow |
| FM-4: "Do NOT use" contradicts trigger map | 3 (Medium - creates confusion) | 2 (Low - only affects users who read both sections) | 3 (Moderate - contradiction is subtle) | 18 | Align SKILL.md "Do NOT use" with trigger keywords |
| FM-5: "score" keyword ambiguity between adversary and ps-critic | 3 (Medium - wrong scoring method applied) | 3 (Medium - "score this" is common) | 2 (Easy - user will see different output) | 18 | Make "tournament score" explicit trigger |

**Critical RPN Threshold:** 27 (Severity 3 × Likelihood 3 × Detection 3)

**No critical failures**, but FM-1 (RPN 24) is close. All failures are mitigable with keyword refinement.

---

## S-013 Inversion Technique

**Inversion Question:** "What if adding `/adversary` to H-22 makes things WORSE instead of better?"

### Inversion 1: "Could the trigger keywords cause MORE confusion than clarity?"

**Current state:** No explicit `/adversary` triggers, users must manually invoke.

**Proposed state:** H-22 triggers on "quality review", "adversarial", "tournament", etc.

**Inversion:** If "quality review" is too broad, Claude might invoke `/adversary` for routine code reviews, adding unnecessary overhead. Users who just want a quick sanity check now get multi-page tournament reports.

**Evidence:** Trigger map includes "quality review" without "adversarial" modifier. SKILL.md says "Do NOT use for code review" but trigger says the opposite.

**Conclusion:** The trigger keywords could INCREASE confusion if not refined. The intent is good but the execution introduces ambiguity.

### Inversion 2: "Could the Implementation section make quality-enforcement.md HARDER to understand?"

**Current state (v1.2.0):** No Implementation section, users infer operational usage from Strategy Catalog.

**Proposed state (v1.3.0):** Implementation section with links to agents and templates.

**Inversion:** If the Implementation section is just a list of file paths, it adds bulk without adding clarity. Users expecting "how to apply this" get "where to find pieces" instead.

**Evidence:** Lines 194-218 are mostly navigation ("See `skills/adversary/SKILL.md` for..."). No workflow description or decision guidance.

**Conclusion:** The Implementation section is NET NEUTRAL at best, possibly NET NEGATIVE if it misleads readers expecting operational guidance.

### Inversion 3: "Could the SKILL.md 'When NOT to use' guidance backfire?"

**Current approach:** Tell users when NOT to use `/adversary` (creator-critic loops, code review, constraint validation).

**Inversion:** If the trigger map invokes `/adversary` for "quality review" but SKILL.md says "don't use for code review", Claude is caught in a contradiction. It might invoke the skill (per H-22) but then second-guess itself (per SKILL.md guidance).

**Evidence:** Trigger map line 34 has "quality review" but SKILL.md line 73 says "Do NOT use when: You need code review."

**Conclusion:** The "When NOT to use" guidance is correct but conflicts with the trigger map. Either fix the triggers or fix the guidance.

---

## Synthesis of Findings

### What's Working

1. **AC-1 PASS:** H-22 trigger map includes `/adversary` with appropriate keywords (adversarial, tournament, red team, steelman, score, devil's advocate, quality gate).
2. **AC-2 PASS:** quality-enforcement.md has Implementation section linking to `/adversary` skill and agents.
3. **AC-3 PASS:** adversary SKILL.md distinguishes `/adversary` from ps-critic with detailed comparison table (lines 279-314).
4. **Traceability EXCELLENT:** All strategy IDs cited, SSOT references correct, version updated to 1.3.0.
5. **SKILL.md structure EXCELLENT:** Triple-lens format, clear agent descriptions, comprehensive usage guidance.

### What's Broken

1. **Keyword overlap (FM-1):** "quality review" is too generic and conflicts with ps-reviewer use cases.
2. **Missing "critique" trigger (FM-2):** Users requesting "rigorous critique" may not trigger `/adversary`.
3. **Implementation section (FM-3):** Title promises workflow guidance, delivers navigation links.
4. **SKILL.md contradiction (FM-4):** "Do NOT use for code review" contradicts "quality review" trigger.
5. **Constitutional concern W-2:** H-22 doesn't define when a review is "adversarial" vs "iterative."

### Recommended Revisions

**High Priority (MUST FIX for 0.92+):**

1. **Refine trigger keywords in mandatory-skill-usage.md:**
   - Replace "quality review" with "adversarial quality review"
   - Add "rigorous critique" or "formal critique"
   - Keep "tournament", "red team", "devil's advocate", "steelman", "quality gate" (these are specific)

2. **Clarify H-22 rule text:**
   - Change: "MUST invoke `/adversary` for adversarial quality reviews and tournament scoring."
   - To: "MUST invoke `/adversary` for standalone adversarial reviews outside creator-critic loops, tournament scoring, and formal strategy application (red team, devil's advocate, steelman, pre-mortem)."

3. **Align SKILL.md "Do NOT use" section:**
   - Remove "code review or defect detection" from exclusions (or qualify it: "routine code review — use ps-reviewer for quick checks")
   - Add: "Use `/adversary` for adversarial code review (e.g., red team security review, tournament quality assessment). Use ps-reviewer for routine defect detection."

**Medium Priority (SHOULD FIX for clarity):**

4. **Expand or rename quality-enforcement.md Implementation section:**
   - Option A: Rename to "Operational Components" to set correct expectations.
   - Option B: Add workflow description: "When Claude detects adversarial review keywords per H-22, it invokes the /adversary skill. The skill orchestrates three agents: adv-selector (strategy selection), adv-executor (template execution), and adv-scorer (S-014 scoring). See agents/ directory for detailed agent prompts."

5. **Add decision guidance to Implementation section:**
   - Include a table:
     | User Request | Skill | Rationale |
     |--------------|-------|-----------|
     | "Review this code for bugs" | ps-reviewer | Routine defect detection |
     | "Give me adversarial critique of this architecture" | /adversary | Standalone adversarial review |
     | "Improve this deliverable iteratively" | /problem-solving (ps-critic) | Creator-critic loop |
     | "Run tournament review for C4" | /adversary | Tournament mode |

**Low Priority (NICE TO HAVE):**

6. **Add L2-REINJECT comment to mandatory-skill-usage.md:**
   - Suggested: `<!-- L2-REINJECT: rank=6, tokens=35, content="/adversary for standalone adversarial reviews, tournament scoring, red team. ps-critic for embedded loops." -->`

---

## Final Verdict

**Score:** 0.88 / 1.00
**Threshold:** 0.92 (C3 minimum per H-13)
**Outcome:** **REVISE**

**Rationale:** The deliverables successfully add `/adversary` to H-22 and create implementation guidance, but keyword overlap and ambiguous guidance create medium risk of skill invocation confusion. The score falls short of 0.92 primarily due to Internal Consistency (0.80) and Completeness (0.85) deficiencies.

**Criticality Assessment:** C3 is appropriate (AE-002 auto-escalation). No escalation to C4 needed — these are fixable issues that don't threaten constitutional integrity.

**Revision Strategy:** Focus on keyword refinement (High Priority items 1-3). The structural changes are sound; the execution needs precision tuning.

**Estimated Revision Effort:** 30-45 minutes to refine keywords, clarify H-22 rule text, and align SKILL.md guidance.

---

## Strategy Application Summary

| Strategy | Applied | Key Findings |
|----------|---------|--------------|
| S-014 (LLM-as-Judge) | ✓ | Score: 0.88. Internal Consistency (0.80) and Completeness (0.85) drag down composite. |
| S-007 (Constitutional) | ✓ | No violations. 2 warnings: P-022 deception risk (misleading triggers), H-22 enforcement ambiguity. |
| S-002 (Devil's Advocate) | ✓ | 3 challenges: ps-critic overlap, Implementation section is just links, "Do NOT use" contradicts triggers. |
| S-004 (Pre-Mortem) | ✓ | 4 failure modes identified: wrong skill invocation, missing critique trigger, misleading Implementation, contradictory guidance. |
| S-012 (FMEA) | ✓ | 5 failure modes, RPN 16-24. FM-1 (keyword overlap, RPN 24) is highest risk. All mitigable. |
| S-013 (Inversion) | ✓ | 3 inversions: trigger keywords could increase confusion, Implementation section might mislead, "Do NOT use" guidance backfires. |

**C3 Strategy Coverage:** All 6 required strategies applied (S-014, S-007, S-002 from C2 + S-004, S-012, S-013 from C3).

---

## Appendix: Evidence References

| Finding | Evidence Location |
|---------|-------------------|
| Keyword overlap | mandatory-skill-usage.md:34 ("quality review") vs SKILL.md:73 ("Do NOT use when: code review") |
| Implementation section is thin | quality-enforcement.md:194-218 (mostly links, no workflow) |
| SKILL.md contradiction | SKILL.md:73 vs mandatory-skill-usage.md:34 |
| H-22 rule preserved | mandatory-skill-usage.md:23 (rule text intact, only extended) |
| Traceability complete | quality-enforcement.md:3 (version 1.3.0), SKILL.md:30 (SSOT reference) |

---

*Report Generated: 2026-02-16*
*Reviewer: Claude Sonnet 4.5*
*Enabler: EN-926 (Rule Synchronization)*
*Criticality: C3*
*Strategies: S-014, S-007, S-002, S-004, S-012, S-013*
