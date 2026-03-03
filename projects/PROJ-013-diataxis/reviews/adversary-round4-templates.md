# Quality Score Report: Diataxis Templates (Round 4)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Stakeholder-facing verdict and top action item |
| [Scoring Context](#scoring-context) | Deliverable, type, criticality, strategy reference |
| [Score Summary](#score-summary) | Weighted composite and threshold verdict |
| [R3 Fix Verification](#r3-fix-verification) | Applied vs. not-applied R3 recommendations |
| [Dimension Scores](#dimension-scores) | Per-dimension table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement paths |
| [S-007 Constitutional Review](#s-007-constitutional-review-round-4) | New constitutional gaps in current state |
| [S-013 Inversion Analysis](#s-013-inversion-analysis-round-4) | Stress-test remaining assumptions |
| [S-010 Self-Refine](#s-010-self-refine-round-4) | Priority-ordered improvement recommendations |
| [Improvement Recommendations](#improvement-recommendations-priority-ordered) | Actionable fix table |
| [Score Trajectory](#score-trajectory) | Multi-round progression |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency verification |

---

## L0 Executive Summary

**Score:** 0.886/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.86)

**One-line assessment:** The two major R3 findings are partially resolved — the domain-agnostic observable skill examples are fully fixed, but the R-01 "MUST mirror" fix is incomplete because the explanatory comment still uses "should mirror," creating a heading/comment contradiction that will guide writer-agents to the MEDIUM interpretation. Three minor findings from R3 were also left unfixed, holding Internal Consistency at 0.86 and Methodological Rigor at 0.87.

---

## Scoring Context

- **Deliverables:**
  - `skills/diataxis/templates/tutorial-template.md`
  - `skills/diataxis/templates/howto-template.md`
  - `skills/diataxis/templates/reference-template.md`
  - `skills/diataxis/templates/explanation-template.md`
- **Deliverable Type:** Other (documentation templates / scaffolds)
- **Criticality Level:** C2 (Standard — part of skill deliverable set)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **Adversarial Strategies Applied:** S-007 (Constitutional AI Critique), S-013 (Inversion), S-010 (Self-Refine)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Round Score:** 0.873 (Round 3)
- **Iteration:** 4
- **Scored:** 2026-02-27

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.886 |
| **Threshold** | 0.95 (user-specified) |
| **Verdict** | REVISE |
| **Prior Round Score** | 0.873 |
| **Delta from Prior Round** | +0.013 |
| **Strategy Findings Incorporated** | Yes — Round 3 report (`adversary-round3-templates.md`) |

---

## R3 Fix Verification

The following table records which Round 3 SR-R3 recommendations were applied (per user-stated context), verified against current template state.

| R3 SR # | Recommendation | Applied | Verification |
|---------|----------------|---------|-------------|
| SR-R3-001 | Tutorial — Propagate TAP-03 guard to Steps 2 and 3 (CC-R3-001) | **YES** | Tutorial line 40: `{Brief instruction. One path only — no "alternatively" or "you could also."}` and line 53: same. Guard now consistent across Steps 1, 2, 3. |
| SR-R3-002 | Reference — Fix third Category 2 entry example placeholder (CC-R3-002) | **YES** | All three example placeholders now read: `{illustrative usage showing the entry in context — NOT a procedural recipe}`. Consistent. |
| SR-R3-003 | Tutorial — Domain-agnostic observable skill examples (IN-R3-001) | **YES** | Tutorial lines 67-68: `{Observable skill 1 -- e.g., "create a {resource} using the \`{tool command}\` command"}` and `{Observable skill 2 -- e.g., "verify {resource} status by running \`{verification command}\`"}`. Jerry-specific CLI references removed. |
| SR-R3-004 | Reference — Upgrade R-01 language to HARD-equivalent (IN-R3-003) | **PARTIAL** | Heading (line 13): `MUST mirror` applied. Heading (line 49): `MUST mirror` applied. Comment (line 17): still reads `should mirror the described system's own structure`. Heading and comment now contradict each other. |
| SR-R3-005 | Reference — Propagate Since: field to all entry templates (DA-R3-002) | **YES** | Since: field present in all three entry templates (lines 24, 39, 57). R-05 consistency restored. |
| SR-R3-006 | Tutorial — Extend T-08 comment for multi-environment scope (DA-R3-003) | **NO** | Line 26 still reads: `<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED]. -->`. No placement example, no multi-environment note. |
| SR-R3-007 | Explanation — Add EAP-01 guard to Alternative Perspectives section (CC-R3-004) | **NO** | Explanation line 34: `{Acknowledge that other valid approaches or viewpoints exist. Explain the trade-offs.}`. No EAP-01 guard added. |
| SR-R3-008 | How-To — Add in-situ HAP-04 guard to Step 2 (CC-R3-005) | **NO** | Step 2 has no inline HAP-04 comment. Guard remains only at post-Step-3 position (lines 50-51). |

### Fix Summary

| Status | Count | Items |
|--------|-------|-------|
| APPLIED (full) | 4 | SR-R3-001, SR-R3-002, SR-R3-003, SR-R3-005 |
| APPLIED (partial) | 1 | SR-R3-004 (heading MUST, comment still "should") |
| NOT APPLIED | 3 | SR-R3-006, SR-R3-007, SR-R3-008 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | All quadrant criteria sections structurally present; DA-R3-001 scope restriction tension persists (no first-class variation qualifier) |
| Internal Consistency | 0.20 | 0.86 | 0.172 | Heading "MUST mirror" contradicts comment "should mirror" in reference (partial SR-R3-004 fix); EAP-01 guard inconsistent across explanation sections (CC-R3-004 open) |
| Methodological Rigor | 0.20 | 0.87 | 0.174 | IN-R3-001 fully fixed (domain-agnostic examples); IN-R3-003 partially fixed (comment still MEDIUM tier); CC-R3-004, CC-R3-005 unfixed |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Criteria IDs cited in all templates; T-08 [UNTESTED] guidance still lacks placement context and multi-environment scope (CC-R3-003, DA-R3-003 unfixed) |
| Actionability | 0.15 | 0.90 | 0.135 | TAP-03 guard now on all steps; reference entries fully consistent; HAP-04 educational moment still missed at Step 2; EAP-01 absent from Alternative Perspectives |
| Traceability | 0.10 | 0.93 | 0.093 | All four templates cite diataxis-standards.md sections; anti-pattern IDs cited inline; R-01 and R-07 referenced; no traceability degradation |
| **TOTAL** | **1.00** | | **0.886** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**

All four templates provide complete structural scaffolding for their respective quadrant types:

- Tutorial: 7 sections (title, tagline, What You Will Achieve, Prerequisites, Steps, What You Learned, Related). All T-01 through T-08 criteria are addressed — T-07 (endpoint shown upfront) via the "What You Will Achieve" section, T-06 (prerequisites stated) via Prerequisites block, T-02 (visible result) via `**Expected result:**` in every step, T-08 (reliable reproduction) via the [UNTESTED] comment.
- How-To: 6 sections (title, Before You Begin, Steps, Verification, Troubleshooting, Related). H-01 through H-07 covered. Verification section addresses H-03 (real-world variations) and verification confirmation.
- Reference: Overview, categories, Related. R-01 through R-07 addressed. R-07 completeness checklist present at line 68.
- Explanation: Context, Core Concept sections, Connections, Alternative Perspectives, Related. E-01 through E-07 structurally covered. Scope boundary guidance present.

**Gaps:**

DA-R3-001 persists: The explanation template's scope constraint ("must be a bounded concept, name at least one concrete exclusion") and the how-to's HAP-04 guard ("at most one conditional per step") do not distinguish between truly unbounded scope (EAP-05) and legitimately complex topics requiring broader coverage. A distributed-systems explanation covering Raft, Paxos, and PBFT as co-equal perspectives cannot satisfy the template's "name at least one concrete exclusion" instruction honestly without misleading readers about scope. Similarly, a how-to guide for a multi-platform tool (Kubernetes vs. Docker vs. bare metal) may have three first-class paths, not two edge cases plus one main path. The templates apply guards uniformly without the first-class variation qualifier.

IN-R3-005 (carried from R3, unresolved): The explanation scope placeholder `{specific aspect of topic — must be a bounded concept}` does not provide an example of what "bounded" means. A writer can fill this with "the entire authentication system" — which sounds specific but is unbounded.

**Improvement Path:**

To raise this to 0.93: Add a qualifier to the HAP-04 guard distinguishing edge cases from first-class variations. Add a "bounded concept" example to the explanation scope placeholder (e.g., "bounded: 'the token expiry model in JWT-based auth'. Unbounded: 'authentication'").

---

### Internal Consistency (0.86/1.00)

**Evidence of resolved inconsistencies:**

- CC-R3-001 FIXED: Steps 2 and 3 now have the TAP-03 guard text (`One path only — no "alternatively" or "you could also."`), matching Step 1. T-04 constraint consistently communicated.
- CC-R3-002 FIXED: All three reference example placeholders now use identical wording: `{illustrative usage showing the entry in context — NOT a procedural recipe}`.
- DA-R3-002 FIXED: Since: field now appears in all three entry templates (lines 24, 39, 57). R-05 (standard formatting) compliance restored.

**Gaps (inconsistencies remaining):**

**Gap 1 — Heading/comment MUST/should contradiction (NEW in R4, introduced by partial SR-R3-004 fix):**

Reference template line 13: `## {Category 1 — name MUST mirror the described system's own terminology (R-01)}`
Reference template line 17: `<!-- R-01: Category names should mirror the described system's own structure -- for code: module/class names; for CLI: command groups; for config: section names. -->`

These two lines are read together. The heading says MUST; the explanatory comment says should. In the Jerry framework's tier vocabulary, "should" is explicitly MEDIUM-tier — overridable with documented justification. A writer-agent trained on this framework will encounter a direct contradiction and must choose between the heading and the comment. In practice, agents rely on the elaborating comment for interpretation, not the section heading placeholder. The "should" interpretation is more likely to win because: (a) it is the elaboration, (b) it is more permissive, and (c) framework training assigns should = MEDIUM = overridable.

Reference line 49 has the same heading fix (`MUST mirror`) and the same unresolved comment at line 17 applies to Category 2 as well.

**Gap 2 — Inconsistent EAP-01 guard coverage in explanation (CC-R3-004 unfixed):**

Explanation template section-level EAP-01 coverage:
- Line 13 (Context section): No EAP-01 guard
- Lines 15-18 (Core Concept 1): `Do NOT use imperative verbs (run, configure, set, install).` — EAP-01 guard present
- Lines 20-22 (Core Concept 2): Inherits the same guidance comment
- Lines 33-35 (Alternative Perspectives): No EAP-01 guard
- Lines 28-31 (Connections): No EAP-01 guard

Only Core Concept sections have the guard. The Alternative Perspectives section — which specifically prompts writers to discuss and compare approaches — is the highest-risk section for instructional creep, yet has no guard.

**Improvement Path:**

To raise this to 0.92: (1) Resolve the MUST/should contradiction in the R-01 comment — change "should mirror" to "MUST mirror" at line 17. (2) Add EAP-01 inline guard to the Alternative Perspectives placeholder text.

---

### Methodological Rigor (0.87/1.00)

**Evidence of resolved issues:**

- IN-R3-001 FULLY FIXED: Observable skill placeholders in tutorial lines 67-68 now use domain-agnostic format: `"create a {resource} using the \`{tool command}\` command"` and `"verify {resource} status by running \`{verification command}\`"`. The action verb is embedded in the example ("create", "verify"), the format is explicit, and no jerry-specific tools are cited. Writers producing non-jerry tutorials will not see CLI commands from the Jerry framework. This is a clean, complete fix. Estimated recovery: +0.04 on Methodological Rigor (IN-R3-001 was -0.03 impact in R3; the fix over-delivers slightly because the new format is more actionable than the pre-SR-R2-003 state).

**Gaps:**

**Gap 1 — IN-R3-003 partial fix: R-01 comment still MEDIUM-tier:**

R-01 in diataxis-standards.md is a quality criterion with a pass/fail test (Section 1, Reference Quality Criteria). The template comment at line 17 continues to use "should mirror" — MEDIUM-tier language per quality-enforcement.md tier vocabulary. The heading was changed to "MUST mirror" but the comment provides the interpretive context for the heading. A writer seeing "MUST mirror" in the heading and "should mirror" in the comment will resolve this ambiguity toward the MEDIUM interpretation. The fix was therefore only partially effective.

This is equivalent to the original IN-R3-003 finding: agents trained on the Jerry framework's tier vocabulary will correctly identify "should" as overridable, overriding the MUST in the heading through comment disambiguation.

**Gap 2 — CC-R3-004: Alternative Perspectives EAP-01 guard missing:**

The explanation template's `## Alternative Perspectives` section (lines 33-35) prompts: `{Acknowledge that other valid approaches or viewpoints exist. Explain the trade-offs.}`. The "Explain the trade-offs" prompt does not prohibit imperative voice. A writer discussing trade-offs may write: "To use approach B, configure X then restart Y" — a direct EAP-01 violation. The section-level EAP-01 guard that protects Core Concept 1 and Core Concept 2 is absent here.

**Gap 3 — CC-R3-005: HAP-04 in-situ guard still missing from Step 2:**

The how-to template introduces the conditional branch pattern in Step 2 (lines 29-38) with two `If you need {variation}:` branches. The educational warning about over-branching appears AFTER Step 3 (lines 50-51), not alongside the pattern where it is introduced. A writer modeling Steps 4, 5, 6 on Step 2's pattern can produce 3-4 conditionals per step before encountering the guard. The guard at post-Step-3 position is pedagogically late.

**Improvement Path:**

To raise this to 0.93: (1) Fix R-01 comment to "MUST mirror" (one word change). (2) Add EAP-01 guard to Alternative Perspectives placeholder. (3) Add in-situ HAP-04 one-liner to Step 2.

---

### Evidence Quality (0.88/1.00)

**Evidence:**

All four templates provide strong evidence anchoring via criterion citations:
- Tutorial header: `<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (T-01 through T-08) -->`
- Anti-pattern IDs cited inline: `<!-- Anti-patterns to avoid: TAP-01 (abstraction), TAP-02 (extended explanation), TAP-03 (offering choices) -->`
- Reference: R-01 through R-07 criteria referenced; R-07 completeness checklist explicitly cited at line 68
- Example placeholders now provide format models (action verb + resource + method pattern) — writers can verify their output against the model
- `NOT a procedural recipe` guard in reference examples explains what RAP-02 looks like in practice

**Gaps:**

**Gap 1 — CC-R3-003 unfixed: T-08 [UNTESTED] flag placement unspecified:**

Tutorial line 26: `<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED]. -->`

The comment does not specify WHERE to place the `[UNTESTED]` flag. The Step 1 heading is `### 1. {First action}`. A writer who has not tested Step 3 does not know whether to write: `### 3. [UNTESTED] {Third action}` (on the heading), `**Expected result:** [UNTESTED] {Observable outcome.}` (on the result line), or inline within the step body. SR-R3-003 (Round 3 CC-R3-003 recommendation) was not applied. This is an evidence quality gap: the template asserts a quality mechanism ([UNTESTED]) but does not provide sufficient evidence for the writer to apply it correctly.

**Gap 2 — DA-R3-003 unfixed: T-08 partial-verification failure mode not addressed:**

The T-08 comment treats verification as binary: either verified (no flag) or unverified ([UNTESTED]). It does not address the more common failure mode: steps verified on one OS or environment but not others. A writer who runs all steps on macOS marks no steps [UNTESTED], but Windows or Linux readers may encounter failures. This gap in T-08 guidance allows tutorials that appear fully verified to silently contain cross-platform gaps.

**Improvement Path:**

To raise this to 0.92: Apply SR-R3-006 (extend T-08 comment with placement example and multi-environment note). Estimated impact: +0.02-0.03 on Evidence Quality.

---

### Actionability (0.90/1.00)

**Evidence:**

- Tutorial: TAP-03 guard now present on Steps 1, 2, and 3 — writers know the one-path constraint applies to every step, not just the first. Step title uses `### N. {First action}` imperative format. Expected result in each step.
- How-To: Step titles now model `### N. {Imperative verb + object}` with example ("Configure the database connection"). HAP-04 guard present at end of steps section.
- Reference: R-01 heading now says MUST (actionable constraint, even if comment contradicts). All three entry templates have identical structure (Type, Default, Required, Since:). R-07 completeness checklist is an actionable pre-finalization check.
- Explanation: Scope boundary with "must be bounded" and "name at least one concrete exclusion" is actionable. EAP-01 guard on Core Concept sections.

**Gaps:**

**Gap 1 — CC-R3-005 unfixed: HAP-04 in-situ guidance missing at Step 2:**

A writer applying the how-to template reads Step 2, sees two conditional branches, and proceeds to write Steps 3-6. The HAP-04 guard they eventually encounter (after Step 3, lines 50-51) says "at most one conditional per step," but they have already modeled multiple conditionals on Step 2. The actionable constraint arrives too late in the reading sequence to be preventive.

**Gap 2 — CC-R3-004 unfixed: EAP-01 missing from Alternative Perspectives:**

A writer filling in the Alternative Perspectives section has no in-context guidance that imperative constructions are prohibited. The only EAP-01 guard in the explanation template is in the Core Concept body — writers who follow the template sequentially through Context, Core Concepts 1-2, Connections, Alternative Perspectives reach the last section without having seen an EAP-01 reminder for approximately 10-15 template lines.

**Improvement Path:**

To raise this to 0.93: Apply SR-R3-008 (add one-line HAP-04 comment after Step 2 conditional block) and SR-R3-007 (add EAP-01 guard to Alternative Perspectives placeholder text). Both are minimal, targeted changes.

---

### Traceability (0.93/1.00)

**Evidence:**

All four templates maintain full traceability chains:
- Each template header names the applicable quality criteria section in diataxis-standards.md with criterion ID ranges (T-01 through T-08, etc.)
- Anti-pattern IDs cited inline with human-readable descriptions
- Voice guidelines section reference: "See Section 5 of diataxis-standards.md"
- R-01 cited in section heading and explanatory comment
- R-07 explicitly referenced in the completeness checklist comment
- The partial MUST/should fix does not break traceability — R-01 is still cited correctly, and both the heading and comment trace to R-01. The inconsistency is a consistency issue, not a traceability break.

**Gaps:**

Minor: The MUST/should contradiction at R-01 comment vs. heading creates interpretation ambiguity in what the traced criterion requires. A writer tracing R-01 in diataxis-standards.md will find: "Test: Section hierarchy matches the structure of the described system" with no MUST qualifier. The template's heading says MUST, but neither the comment nor the standard itself uses MUST language. This is a gap in how the enforcement tier is communicated through the traceability chain.

**Improvement Path:**

To raise to 0.95: Document in the R-01 comment that this criterion is treated as HARD-equivalent (pass/fail test) in the quality framework, even though the standard itself uses neutral language.

---

## S-007 Constitutional Review (Round 4)

*New constitutional gaps identified in current template state.*

### CC-R4-001: Reference Template Has Internal Contradiction on R-01 Enforcement Tier [Minor]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor (was Major before partial fix; heading now partially corrects) |
| **Template** | `reference-template.md` — lines 13 and 17 |
| **Strategy Step** | S-007 check (b): anti-pattern exposure from remediations |

**Evidence:**
- Line 13: `## {Category 1 — name MUST mirror the described system's own terminology (R-01)}`
- Line 17: `<!-- R-01: Category names should mirror the described system's own structure -- for code: module/class names; for CLI: command groups; for config: section names. -->`

The heading and comment directly contradict each other on the enforcement tier for R-01. "MUST mirror" (heading) is HARD-tier; "should mirror" (comment) is MEDIUM-tier and explicitly overridable per quality-enforcement.md. The comment is the explanatory elaboration writers use to understand the heading; it will win in interpretation. The fix was applied to the headings but the comment — which carries the explanatory authority — was not updated.

**Mitigation (same as SR-R3-004 remainder):**

Change line 17 from:
```markdown
<!-- R-01: Category names should mirror the described system's own structure -- for code: module/class names; for CLI: command groups; for config: section names. -->
```
To:
```markdown
<!-- R-01 (HARD — pass/fail): Category names MUST mirror the described system's own structure -- for code: module/class names; for CLI: command groups; for config: section names. Organizational names like "Common Options" or "Advanced Use Cases" violate R-01. -->
```

---

### CC-R4-002: Explanation Template — EAP-01 Guard Inconsistently Applied Across Sections [Minor]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Template** | `explanation-template.md` — lines 33-35 |
| **Strategy Step** | S-007 check (a): structural match to E-07 (no imperative instructions) |

**Evidence:**

EAP-01 guard coverage across explanation sections:
- Core Concept sections (lines 15-22): `Do NOT use imperative verbs (run, configure, set, install). If you find yourself writing instructions, move that content to a How-To Guide.`
- Context section (lines 11-13): No EAP-01 guard
- Connections section (lines 28-31): No EAP-01 guard
- Alternative Perspectives (lines 33-35): No EAP-01 guard

E-07 (no imperative instructions) applies to the entire explanation document, not only to Core Concept sections. The sections without guards are precisely those where imperative verb use is plausible: Context section might contain "Run the migration before deployment"; Connections section might say "Use X when Y"; Alternative Perspectives might say "To use approach B, configure...".

**Mitigation:** Apply inline EAP-01 note to Alternative Perspectives placeholder (SR-R3-007, not yet applied). Consider also adding a brief note to the Connections section.

---

## S-013 Inversion Analysis (Round 4)

*Stress-test assumptions in current (post-R3-fix) template state.*

### Step 1: Current State Goals

The R4 templates share the same goals as R3 (G-01 through G-05) with one addition from the partial fixes:

- **G-06 (new):** The R-01 enforcement language in the reference template must be unambiguous enough that writer-agents trained on the Jerry tier vocabulary cannot interpret it as MEDIUM-tier.

### Step 2-4: New Assumption Stress-Tests

| ID | Assumption | Inversion | Plausibility | Severity | Affected Templates |
|----|-----------|-----------|--------------|----------|--------------------|
| A-R4-01 | Domain-agnostic examples (`{resource}`, `{tool command}`) guide writers to domain-appropriate skill statements | Writer fills `{resource}` as a named tool and `{tool command}` as a tool command, but loses the action verb entirely — producing "skill: `openssl req`" instead of "create a TLS certificate using `openssl req`" | Low | Minor | Tutorial |
| A-R4-02 | Heading "MUST mirror" overrides comment "should mirror" in writer interpretation | Writer resolves MUST/should by reading the comment (elaboration) as authoritative, uses MEDIUM interpretation, produces "Common Operations" category names | High | Minor (from Major, after partial fix) | Reference |
| A-R4-03 | HAP-04 guard at post-Step-3 position prevents multi-branch step explosion | Writer models Steps 4-7 on Step 2's two-branch pattern before reaching the guard — Steps 4-7 each have 2-3 conditionals; the guide has 12+ conditional blocks | Medium | Minor | How-To |
| A-R4-04 | `{Explain the trade-offs}` in Alternative Perspectives prompts discursive prose | Writer produces: "If the design uses eventual consistency, configure your retry logic for idempotency by setting `MAX_RETRIES=3`" — imperative instruction embedded in trade-off analysis | Medium | Minor | Explanation |

### Step 5: Mitigations

**A-R4-01 (Low plausibility, Minor):** Low risk. The example format `"create a {resource} using the \`{tool command}\` command"` has the action verb embedded in the surrounding text, making it structural. The writer must place a resource and tool command into a pre-built sentence frame. The risk is minor because the verb is not a placeholder.

**A-R4-02 (High plausibility, Minor):** Directly addressed by CC-R4-001. The heading-level MUST fix created a new assumption that heading authority supersedes comment authority; this assumption fails in practice. The mitigation is to fix the comment (one word: "should" → "MUST").

**A-R4-03 (Medium plausibility, Minor):** Directly addressed by SR-R3-008 (not yet applied). The in-situ HAP-04 guard at Step 2 breaks the pattern at the point of introduction rather than three steps later.

**A-R4-04 (Medium plausibility, Minor):** Directly addressed by SR-R3-007 (not yet applied). The guard text prevents writers from treating "explain the trade-offs" as license to produce imperative instructions.

---

## S-010 Self-Refine (Round 4)

*Systematic review of all four templates for remaining refinement opportunities, ordered by impact.*

### SR-R4-001: Reference — Fix R-01 Comment to MUST-tier Language [HIGH IMPACT]

**Dimension:** Internal Consistency, Methodological Rigor

**Evidence:** Line 17 comment `should mirror` directly contradicts line 13 heading `MUST mirror`. This is the dominant remaining gap — the partial fix created a new inconsistency more visible than the original.

**Change:**
```markdown
<!-- R-01: Category names should mirror the described system's own structure -- for code: module/class names; for CLI: command groups; for config: section names. -->
```
To:
```markdown
<!-- R-01 (HARD — pass/fail): Category names MUST mirror the described system's own structure -- for code: module/class names; for CLI: command groups; for config: section names. Organizational names like "Common Options" or "Advanced Use Cases" violate R-01. -->
```

**Estimated impact:** +0.03 on Internal Consistency, +0.02 on Methodological Rigor.

---

### SR-R4-002: Explanation — Add EAP-01 Guard to Alternative Perspectives [MEDIUM IMPACT]

**Dimension:** Methodological Rigor, Actionability

**Evidence:** Alternative Perspectives placeholder has no EAP-01 guard. CC-R3-004 carried forward to R4.

**Change:**

From:
```markdown
{Acknowledge that other valid approaches or viewpoints exist. Explain the trade-offs.}
```
To:
```markdown
{Acknowledge that other valid approaches or viewpoints exist. Explain the trade-offs in discursive prose — no imperative verbs (EAP-01). Compare approaches; do not direct the reader to "switch to approach B" or "use X instead."}
```

**Estimated impact:** +0.01 on Methodological Rigor, +0.01 on Actionability, +0.01 on Internal Consistency (EAP-01 guard now consistent across more sections).

---

### SR-R4-003: How-To — Add In-Situ HAP-04 Guard to Step 2 [MEDIUM IMPACT]

**Dimension:** Methodological Rigor, Actionability

**Evidence:** HAP-04 guard at post-Step-3 position misses the educational moment in Step 2. CC-R3-005 carried forward to R4. A-R4-03 confirms medium plausibility of multi-branch explosion.

**Add after the Step 2 conditional block (after line 38, before the Step 3 heading):**
```markdown
<!-- HAP-04: One conditional per step is the maximum. More conditionals suggest the step should be split or documented in separate guides. First-class paths (e.g., Kubernetes vs. Docker) may warrant separate guides rather than a single branched guide. -->
```

**Estimated impact:** +0.01 on Methodological Rigor, +0.01 on Actionability.

---

### SR-R4-004: Tutorial — Extend T-08 Comment for Placement and Multi-Environment Scope [MINOR IMPACT]

**Dimension:** Evidence Quality

**Evidence:** CC-R3-003 and DA-R3-003 both carried forward to R4. The T-08 [UNTESTED] flag is operationally underspecified.

**Change line 26 from:**
```markdown
<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED]. -->
```
**To:**
```markdown
<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED].
     Placement: flag on the step heading. Example: "### 2. [UNTESTED] Configure the database"
     Multi-environment: if verified on one OS only, add context: "Verified on macOS 14. Windows users: see Troubleshooting." -->
```

**Estimated impact:** +0.02 on Evidence Quality, +0.01 on Actionability.

---

### SR-R4-005: Completeness — Add First-Class Variation Qualifier to HAP-04 Guard and Explanation Scope [MINOR IMPACT]

**Dimension:** Completeness

**Evidence:** DA-R3-001 carried forward to R4. Scope restriction guards do not distinguish between anti-pattern suppression and artificially narrow scope.

**How-To HAP-04 guard (current lines 50-51), change second sentence from:**
```markdown
Additional conditionals suggest the step should be split or the variations documented in separate guides.
```
**To:**
```markdown
Additional conditionals suggest the step should be split or the variations documented in separate guides. Exception: if all variations are first-class platform paths (e.g., Kubernetes, Docker, bare metal) for the same task, a unified guide with clearly labeled platform branches is acceptable.
```

**Explanation scope placeholder (line 5), extend to include:**
```
...must be a bounded concept, not the entire domain. Example of bounded: "the token expiry model in JWT authentication". Example of unbounded (not allowed): "authentication"}
```

**Estimated impact:** +0.01 on Completeness.

---

## Improvement Recommendations (Priority Ordered)

| Priority | ID | Dimension | Current | Target | Template | Recommendation |
|----------|-----|-----------|---------|--------|----------|----------------|
| 1 | SR-R4-001 | Internal Consistency, Methodological Rigor | 0.86, 0.87 | 0.89, 0.89 | reference-template.md | Change R-01 comment line 17 "should mirror" to "MUST mirror" and add R-01 (HARD — pass/fail) qualifier |
| 2 | SR-R4-002 | Methodological Rigor, Actionability | 0.87, 0.90 | 0.88, 0.91 | explanation-template.md | Add EAP-01 guard to Alternative Perspectives placeholder text |
| 3 | SR-R4-003 | Methodological Rigor, Actionability | 0.87, 0.90 | 0.88, 0.91 | howto-template.md | Add in-situ HAP-04 one-liner after Step 2 conditional block |
| 4 | SR-R4-004 | Evidence Quality | 0.88 | 0.90 | tutorial-template.md | Extend T-08 comment with [UNTESTED] placement example and multi-environment note |
| 5 | SR-R4-005 | Completeness | 0.90 | 0.91 | howto-template.md, explanation-template.md | Add first-class variation qualifier to HAP-04 guard; add bounded concept example to explanation scope placeholder |

### Projected Round 5 Score (with all SR-R4 applied)

| Dimension | Current | SR-R4 Impact | Projected |
|-----------|---------|-------------|-----------|
| Completeness | 0.90 | +0.01 (SR-R4-005) | 0.91 |
| Internal Consistency | 0.86 | +0.03 (SR-R4-001) +0.01 (SR-R4-002) | 0.90 |
| Methodological Rigor | 0.87 | +0.02 (SR-R4-001) +0.02 (SR-R4-002, SR-R4-003) | 0.91 |
| Evidence Quality | 0.88 | +0.02 (SR-R4-004) | 0.90 |
| Actionability | 0.90 | +0.02 (SR-R4-002, SR-R4-003, SR-R4-004) | 0.92 |
| Traceability | 0.93 | 0.00 | 0.93 |

**Projected R5 composite:**
- Completeness: 0.91 × 0.20 = 0.182
- Internal Consistency: 0.90 × 0.20 = 0.180
- Methodological Rigor: 0.91 × 0.20 = 0.182
- Evidence Quality: 0.90 × 0.15 = 0.135
- Actionability: 0.92 × 0.15 = 0.138
- Traceability: 0.93 × 0.10 = 0.093

**Projected R5 score: 0.910 — still REVISE at 0.95 threshold**

### Gap Analysis Against 0.95 Threshold

The 0.95 threshold requires 0.064 more than the current 0.886. All SR-R4 recommendations deliver approximately +0.024, leaving a remaining gap of ~0.040 after Round 5.

As noted in Round 3, the 0.95 threshold is aspirationally high for template-format deliverables. Templates by design contain placeholder text and comment-based guidance that adversarial strategies can always challenge on interpretation adequacy. The mathematical constraint is:

To reach 0.95, every dimension must average approximately 0.95 or higher (given the equal-weight structure). The current ceiling on Completeness and Internal Consistency is approximately 0.92-0.93 for template-format artifacts — structurally correct but with inherent ambiguity in placeholder interpretation that adversarial scoring will always surface.

**Recommendation to orchestrator:** Consider whether 0.92 (standard H-13 threshold) is the operative gate for template-format deliverables. At the 0.92 threshold, projected R5 score (0.910) is within one focused revision cycle of PASS. All remaining findings are Minor severity; no Critical or Major findings remain in R4.

---

## Score Trajectory

| Round | Score | Delta | Major Findings | Verdict |
|-------|-------|-------|----------------|---------|
| Round 1 | 0.714 | — | Multiple | REJECTED |
| Round 2 | 0.871 | +0.157 | 2 | REVISE |
| Round 3 | 0.873 | +0.002 | 2 | REVISE |
| Round 4 | 0.886 | +0.013 | 0 | REVISE |

**Round 4 finding summary:**

| Severity | Count | IDs |
|----------|-------|-----|
| Critical | 0 | — |
| Major | 0 | — |
| Minor | 4 | CC-R4-001, CC-R4-002, A-R4-02 (confirmed gap), SR-R4 not-yet-applied items |

**Structural observation:** Round 4 marks the first round with zero Major findings. All remaining gaps are Minor. The templates have cleared the major quality barriers. The remaining work is precision refinement: one comment word change, two placeholder text additions, one comment extension.

---

## Leniency Bias Check

- [x] Each dimension scored independently with specific evidence (lines cited for every gap)
- [x] Evidence documented for each score (template line numbers and quoted text)
- [x] Uncertain scores resolved downward (Completeness: 0.90 not 0.91; IC: 0.86 not 0.87 or 0.88)
- [x] First-draft calibration considered (Round 4 is iteration 4; calibration anchor is 0.85 for "Strong work with minor refinements needed" — current 0.886 is in that band)
- [x] No dimension scored above 0.95 without exceptional evidence (highest is Traceability at 0.93)
- [x] Weighted composite verified: 0.180 + 0.172 + 0.174 + 0.132 + 0.135 + 0.093 = 0.886
- [x] Verdict confirmed: 0.886 is in the 0.85-0.91 REVISE band
- [x] Partial fix identified and penalized: SR-R3-004 partial fix (heading MUST, comment should) scored as a new inconsistency, not as a resolved finding
- [x] Leniency check: R3 projected R4 at 0.913 with "all SR-R3 applied." Only 4 of 8 SR-R3 items were fully applied (1 partial). Current score of 0.886 is below that projection, consistent with partial application. Score is not inflated to match the projection.

---

## Session Context Schema

```yaml
verdict: REVISE
composite_score: 0.886
threshold: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.86
critical_findings_count: 0
major_findings_count: 0
minor_findings_count: 4
iteration: 4
score_trajectory:
  - round: 1
    score: 0.714
  - round: 2
    score: 0.871
  - round: 3
    score: 0.873
  - round: 4
    score: 0.886
improvement_recommendations:
  - "SR-R4-001: Fix R-01 comment in reference-template.md line 17 — change 'should mirror' to 'MUST mirror' (one word, highest impact)"
  - "SR-R4-002: Add EAP-01 guard to Alternative Perspectives placeholder in explanation-template.md"
  - "SR-R4-003: Add in-situ HAP-04 guard comment after Step 2 conditional block in howto-template.md"
  - "SR-R4-004: Extend T-08 comment in tutorial-template.md with [UNTESTED] placement example and multi-environment note"
  - "SR-R4-005: Add first-class variation qualifier to HAP-04 guard; add bounded concept example to explanation scope placeholder"
r5_projected_score: 0.910
threshold_calibration_note: "0.95 threshold is aspirationally high for template-format artifacts. At 0.92 (standard H-13), projected R5 score of 0.910 is within one focused revision cycle of PASS."
```

---

*Quality Score Report Round 4 executed by: adv-scorer*
*Constitutional compliance: P-001 (evidence-based), P-002 (persisted), P-004 (provenance cited per dimension)*
*Prior round SSOT: `projects/PROJ-013-diataxis/reviews/adversary-round3-templates.md`*
*Strategies applied: S-007 (Constitutional AI Critique), S-013 (Inversion), S-010 (Self-Refine)*
*SSOT references: `.context/rules/quality-enforcement.md`, `skills/diataxis/rules/diataxis-standards.md`*
