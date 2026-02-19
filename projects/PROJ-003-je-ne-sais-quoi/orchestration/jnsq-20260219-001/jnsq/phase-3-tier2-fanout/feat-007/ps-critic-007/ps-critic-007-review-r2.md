# ps-critic-007 Review R2: S-002 (Devil's Advocate)

<!--
AGENT: ps-critic-007
ROUND: 2
STRATEGIES: S-002 (Devil's Advocate)
DELIVERABLE: ps-creator-007-draft.md (v0.2.0 -> v0.3.0)
DATE: 2026-02-19
-->

## Document Sections

| Section | Purpose |
|---------|---------|
| [R1 Open Items Resolution](#r1-open-items-resolution) | Status of items carried from R1 |
| [Devil's Advocate Challenges](#devils-advocate-challenges) | Deep challenges to design decisions |
| [Fixes Applied](#fixes-applied) | Changes made to draft in this round |
| [Assessment](#assessment) | Overall quality assessment after R2 |
| [Open Items for R3](#open-items-for-r3) | Issues for constitutional compliance review |

---

## R1 Open Items Resolution

| ID | Issue | Resolution | Status |
|----|-------|------------|--------|
| R2-001 | Achievement persistence ambiguity | Updated Achievement Tracking to SHOULD persist in WORKTRACKER.md metadata with `delight_achievements` section. Session-only fallback acknowledged with risk. | FIXED |
| R2-002 | Soundtrack anchor user-facing leak risk | Added "Soundtrack Energy Anchor Convention" paragraph at top of Tone Calibration section. Explicit rule: anchors MUST NOT appear in user-facing output in any form. | FIXED |
| R2-003 | Time-of-day / session greeting interaction model | Added "Time-of-Day Interaction Model" section with numbered rules: greetings priority, farewell modification, mid-session exclusion. | FIXED |
| R2-004 | Delight budget enforcement mechanism | Added "Budget Enforcement" paragraph specifying `delight_budget_remaining` counter, pre-allocated greeting/farewell slots, V-FALLBACK selection, and tier boundary adjustment. | FIXED |
| R2-005 | Context detection confidence | Added "Context Misdetection Handling" paragraph with asymmetric error analysis, bias-toward-lower-energy mitigation, and silent recovery rule. | FIXED |

---

## Devil's Advocate Challenges

### Challenge R2-C1: Could Delight Mechanics Create Fatigue Despite the Budget?

**The challenge:** The delight budget limits personality moments to 2-8 per session, but even within budget, repetition of the same structural pattern (information + one-line personality observation) may become predictable. The developer may learn to "tune out" the appended observation because they know it is coming. Pattern predictability, not just quantity, is a fatigue vector.

**Analysis:** The 30% fallback weighting partially addresses this -- not every delight moment produces personality. The variant pool with staleness tracking (avoid repeats within session and across recent sessions) further addresses it. However, the document does not address structural variety -- all delight moments follow the pattern "information first, personality observation appended." A system where personality occasionally appears as a prefix, or as an aside in parentheses, or as a different structural position would be less predictable.

**Disposition:** This is a valid concern but a MEDIUM-priority implementation detail. The spec correctly defines the principle (personality should not feel templated) and provides mechanisms (variant pools, fallback weighting, staleness tracking). Structural variety is an implementation refinement that can be explored without changing the spec. The "template detector" test in Implementation Guidance (line 686-687) already calls this out: "If you can hear the curly braces, the template is showing." No spec change needed; noted as implementation guidance.

### Challenge R2-C2: Is Streak Recognition Pressure-Creating?

**The challenge:** Streak messages ("Three consecutive passes. The process is working.") implicitly create an expectation of continuation. When the streak breaks, the developer knows the framework noticed -- because it celebrated the streak. The silence on a broken streak (rule 4) may itself create a felt absence that the developer interprets as judgment.

**Analysis:** The document handles this thoughtfully. Streak rule 4 says "Silence on a broken streak is kinder than commentary" -- which is correct. But the challenge is whether the streak system creates a felt pressure to maintain the streak, turning what should be a pleasant observation into an implicit target.

**Mitigating factors in the spec:**
1. Streak messages replace (not supplement) the standard delight observation -- they do not stack.
2. Streak thresholds are spaced (3, 5, 10) with no messages between thresholds, so the streak is not constantly reinforced.
3. The document's design philosophy explicitly prevents "Premature" celebration (anti-pattern: celebrating proximity rather than outcomes).

**Disposition:** The concern is valid but the existing mitigation is adequate. The key safeguard is the spacing of thresholds (3, 5, 10) -- a developer who passes 4 quality gates does not receive escalating pressure between the 3-streak and 5-streak messages. The silence between thresholds prevents accumulating pressure. No spec change needed.

### Challenge R2-C3: Do Companion Behaviors Cross Into Patronizing Territory?

**The challenge:** Knowledge sharing ("First time with /adversary? The SKILL.md has a quick start section.") and gentle redirects ("No tests for this implementation yet. H-20: test before implement.") could feel condescending to experienced developers who know the rules.

**Analysis:** The document addresses this through two mechanisms:
1. Knowledge sharing fires once per trigger per session -- so the developer is not reminded of the same thing repeatedly.
2. Gentle redirects include the "why" (the rule reference), treating the developer as a peer who may have made a deliberate choice.

However, the document does not specify a learning curve for knowledge sharing. A developer who has used /adversary 50 times should not receive "First time with /adversary?" on a new project just because it is the first session on that project. The detection signal for "first time" should be framework-wide, not project-scoped.

**Disposition:** MEDIUM concern. The "first time" detection for knowledge sharing should be scoped to the developer's overall framework usage, not per-project. However, this is an implementation detail -- the spec says "first time using a skill" without scoping it to a project. The implementation should interpret "first time" as "first time for this developer," using a framework-level flag rather than project-level. No spec change needed -- the current language is ambiguous in the right direction.

### Challenge R2-C4: Are Tone Calibrations for Debugging Truly Zero-Personality?

**The challenge:** The debugging context says "Personality budget: Zero" and "No jokes. No references. No soundtrack allusions. No ski metaphors." But the recurring error pattern message ("This is the third time {error_class} has appeared. Consider {structural_fix}.") has a subtly warm, companion-like tone. Is counting occurrences and suggesting structural fixes a form of personality?

**Analysis:** Counting occurrences and suggesting structural fixes is diagnostic behavior, not personality. The warmth in the debugging context is appropriate: "Direct, Warm (supportive, not cheerful)" is the error recovery trait, and "Technically Precise, Direct" is the debugging trait. Warmth in this context means treating the developer as a capable adult who benefits from precise, structured observation -- not injecting humor or personality elements.

The message "This is the third time {error_class} has appeared. Consider {structural_fix}." passes Authenticity Test 1 (information completeness -- it provides the count and the structural suggestion). It also passes Test 3 (new developer legibility -- any developer understands this). The personality is zero; the directness is warm.

**Disposition:** No issue. The debugging context correctly distinguishes between personality (zero) and warmth (appropriate level). No change needed.

### Challenge R2-C5: Delight Budget vs. Powder Day Conflict

**The challenge:** The Powder Day farewell (F-003) is a multi-line box-art celebration -- the highest-energy delight moment. But what if the delight budget is already exhausted when the session ends? Should F-003 still fire, or should it fall back to F-001?

**Analysis:** Session greetings and farewells are pre-allocated (per the new Budget Enforcement paragraph). F-003 is a farewell variant, so it is within the pre-allocated farewell budget slot. This means F-003 fires regardless of whether contextual delight budget is exhausted. This is correct -- a Powder Day moment (all items complete) is too rare and significant to suppress because the contextual budget was used up during the session.

**Disposition:** No issue. The pre-allocation design correctly handles this. Powder Day celebrations are within the farewell budget slot and are not affected by contextual budget exhaustion.

---

## Fixes Applied

| Finding | Fix | Lines Affected |
|---------|-----|----------------|
| R2-001 | Achievement tracking persistence RECOMMENDED via WORKTRACKER.md | Achievement Tracking paragraph |
| R2-002 | Soundtrack Energy Anchor Convention (internal-only rule) | Top of Tone Calibration section |
| R2-003 | Time-of-Day Interaction Model (greeting priority, farewell modification, mid-session exclusion) | Time-of-Day Awareness section |
| R2-004 | Budget Enforcement mechanism with `delight_budget_remaining` counter | Delight Budget Per Session section |
| R2-005 | Context Misdetection Handling with asymmetric error analysis | Contextual Awareness section |

**Draft version:** 0.2.0 -> 0.3.0

---

## Assessment

After R2, the deliverable addresses all six requirements:

1. **Session personality:** Greetings (5), farewells (5), progress, continuity -- all specified with selection rules and tone positions.
2. **Companion behaviors:** Contextual awareness (5 contexts), encouragement (6 triggers), gentle redirects (5 boundaries), knowledge sharing (4 triggers) -- all with constraints.
3. **Celebrations:** By criticality (C1-C4), milestones (4 types), achievements (5 first-time events), anti-patterns (6 named) -- proportionality principle governs.
4. **Tone calibration:** 5 contexts with detailed attribute tables, behavioral rules, and energy anchors. Zero-personality debugging/error recovery correctly specified.
5. **Delight mechanics:** Randomization (variant pools, 30% fallback), time-of-day (5 windows with interaction model), streaks (5 types with threshold spacing), personality consistency (persisted state), delight budget (graduated, enforced).
6. **/saucer-boy integration:** sb-reviewer validation routing, sb-calibrator scoring targets with below-threshold handling, tone spectrum position mapping.

**Remaining concerns for R3:**
- Constitutional compliance verification (P-003, P-022, H-23/H-24)
- Boundary condition adherence verification
- Integration consistency with FEAT-004/006

---

## Open Items for R3

| ID | Issue | Source | Priority |
|----|-------|--------|----------|
| R3-001 | P-003 compliance verification (no subagent patterns in spec) | Constitutional | REQUIRED |
| R3-002 | P-022 compliance verification (no deception about capabilities) | Constitutional | REQUIRED |
| R3-003 | H-23/H-24 navigation compliance verification | Constitutional | REQUIRED |
| R3-004 | Boundary condition adherence (persona NOT conditions) | Constitutional | REQUIRED |
| R3-005 | FEAT-004/006 integration consistency check | Integration | HIGH |
| R3-006 | Self-review (S-010) checklist update for R1/R2 additions | Quality | MEDIUM |
