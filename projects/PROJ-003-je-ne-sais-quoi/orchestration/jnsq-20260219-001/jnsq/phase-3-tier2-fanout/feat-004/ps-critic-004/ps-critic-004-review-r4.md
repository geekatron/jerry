# ps-critic-004 Review R4: Targeted Revision Pass

<!--
AGENT: ps-critic-004
REVIEW: R4
PASS TYPE: Targeted revision (surgical fixes only)
DELIVERABLE: ps-creator-004-draft.md (FEAT-004 Framework Voice & Personality)
TRIGGER: adv-scorer-004 score report (composite 0.901, below 0.92 threshold)
TARGET DIMENSIONS: Evidence Quality (0.86), Completeness (0.88)
CRITICALITY: C2 (Standard)
DATE: 2026-02-19
DRAFT VERSION BEFORE: 0.4.0
DRAFT VERSION AFTER: 0.5.0
-->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Revision Mandate](#revision-mandate) | Score report findings that triggered this pass |
| [Fix 1: Skiing Vocabulary Legibility Claim](#fix-1-skiing-vocabulary-legibility-claim) | Evidence Quality — anchored "transparent" assertion to Authenticity Test 3 |
| [Fix 2: File Not Found Conclusory Note](#fix-2-file-not-found-conclusory-note) | Evidence Quality — inline citation for "directness IS the personality" |
| [Fix 3: Audience Adaptation Matrix Embedded](#fix-3-audience-adaptation-matrix-embedded) | Evidence Quality + Completeness — inline matrix in Step 2 |
| [Fix 4: Template 3 Variable Dimension Count](#fix-4-template-3-variable-dimension-count) | Completeness + Actionability — removed rigid 3-slot structure |
| [Fix 5: Template 3 Priority Dimension Selection Algorithm](#fix-5-template-3-priority-dimension-selection-algorithm) | Actionability + Evidence Quality — explicit selection rule added |
| [Fix 6: Template 11 Rule Explanation](#fix-6-template-11-rule-explanation) | Completeness — parameterized Category 6 Help Text template added |
| [Fix 7: Template 12 Generic Error](#fix-7-template-12-generic-error) | Completeness — generic error template covering 4 un-templated error sub-types |
| [Version and Metadata Updates](#version-and-metadata-updates) | Version 0.4.0 → 0.5.0, Document History added |
| [Projected Score Impact](#projected-score-impact) | Estimated per-dimension score improvement |
| [Change Summary](#change-summary) | Count and scope of all changes |

---

## Revision Mandate

The adv-scorer-004 quality score report (`adv-scorer-004-quality-score.md`) returned a composite of **0.901**, below the H-13 threshold of 0.92. Band: REVISE. The two weakest dimensions drove the gap:

| Dimension | Score | Gap to 0.92 threshold |
|-----------|-------|-----------------------|
| Evidence Quality | 0.86 | -0.06 |
| Completeness | 0.88 | -0.04 |

The scorer identified four material issues across these dimensions:

1. **Evidence Quality — Skiing vocabulary "transparent" claim asserted without definition or test linkage** (adv-scorer-004 Dimension 4, third bullet)
2. **Evidence Quality — Audience Adaptation Matrix cited but not present** (adv-scorer-004 Dimension 4, second bullet; Dimension 1 fourth bullet)
3. **Evidence Quality — Conclusory voice application notes** (adv-scorer-004 Dimension 4, fourth bullet)
4. **Completeness — Category 6 has no standalone template** (adv-scorer-004 Dimension 1, first bullet; Dimension 5, first bullet)
5. **Completeness — Only 1 of 5 error sub-types has a named template** (adv-scorer-004 Dimension 1, second bullet)
6. **Completeness/Actionability — Template 3 rigid 3-slot structure with no selection algorithm** (adv-scorer-004 Dimension 5, second and third bullets)

This pass addresses all six issues with surgical fixes. No structural changes were made.

---

## Fix 1: Skiing Vocabulary Legibility Claim

**Target dimension:** Evidence Quality (scored 0.86)

**Location:** Anti-Pattern 7: Forced Skiing References — `**Why it fails:**` paragraph

**Scorer finding:** "The document claims that 'clean run,' 'drop in,' and 'powder day' are 'transparent to non-skiers.' This is a behavioral claim about audience legibility, but no evidence is provided — no user testing, no citation of a legibility study, and no definition of 'transparent.' The claim may be accurate, but it is asserted rather than demonstrated."

**Before:**
> The approved skiing vocabulary (voice-guide.md) is limited to terms that are transparent to non-skiers: "clean run," "drop in," "powder day."

**After:**
> The approved skiing vocabulary (voice-guide.md) is limited to terms that are transparent to non-skiers — meaning decodable from context without skiing knowledge, per Authenticity Test 3 (New Developer Legibility): "Could a developer unfamiliar with skiing or McConkey still extract all technical information without confusion?" A reader who does not ski knows that "clean run" means clean execution, "drop in" means start, and "powder day" means an exceptionally good day. "Schuss," "halfpipe," and "pizza-and-french-fry" do not decode without skiing knowledge.

**Change type:** Inline extension of existing sentence. No structural change.

**Rationale:** Replaces assertion with the operative definition from Authenticity Test 3, provides concrete decodability reasoning for each approved term, and contrasts with the failing terms from the anti-pattern. The claim is now demonstrative rather than asserted.

---

## Fix 2: File Not Found Conclusory Note

**Target dimension:** Evidence Quality (scored 0.86)

**Location:** Category 2: Error Messages > Error Sub-Category: File Not Found — `**Voice application notes:**`

**Scorer finding:** "Some 'voice application notes' are conclusory. For example, in the File Not Found error sub-type: 'No personality is needed here. The directness IS the personality.' This is a claim about the persona's behavior, not a demonstration of it."

**Before:**
> - No personality is needed here. The directness IS the personality.

**After:**
> - No personality is needed here. The directness IS the personality — per persona doc Voice Trait 1 (Direct): "Says the thing. No preamble. No throat-clearing." The before example's "Error: File not found:" prefix is throat-clearing; removing it and leading with the fact is the voice transformation.

**Change type:** Inline extension of existing bullet. No structural change.

**Rationale:** Anchors the claim to the specific persona doc voice trait that justifies it, and shows concretely what the voice transformation consists of (removing the "Error:" prefix). The note is now demonstrative.

---

## Fix 3: Audience Adaptation Matrix Embedded

**Target dimensions:** Evidence Quality (0.86) and Completeness (0.88)

**Location:** Integration Workflow > Step 2: Identify the Message Context

**Scorer finding (Dimension 4):** "The Audience Adaptation Matrix is cited but not reproduced. Multiple sections reference the Audience Adaptation Matrix for context-dependent decisions. For FEAT-004 to function as a standalone specification, the matrix — or at minimum a summary row for the key audience contexts — should be present. As-is, a developer implementing FEAT-004 without access to FEAT-002 cannot execute the audience adaptation guidance."

**Scorer finding (Dimension 1):** "The document instructs that new message types 'should be classified using the Audience Adaptation Matrix and added to this document,' but the Audience Adaptation Matrix is not defined within this document — it is referenced as coming from SKILL.md (FEAT-002). An implementer who is working on FEAT-004 without FEAT-002 context cannot execute this instruction."

**Before:**
> Look up the message's context in the Voice Application Guide (this document) or the Audience Adaptation Matrix (from SKILL.md). Determine: [4 bullet points]

**After:** The step now leads with "Look up the message's context in the Voice Application Guide (this document). If the audience context is not covered by an existing category, use the Audience Adaptation Matrix below." A 6-row inline summary table follows immediately with columns: Audience Context, Energy Level, Humor Deployment, Technical Depth, Tone Anchor. A selection rule is also added explaining that message-moment state takes precedence over session state. The full-matrix cross-reference to FEAT-002 SKILL.md is preserved.

**Audience contexts covered by the inline table:**
- Active session (routine work)
- Debugging / error state
- Celebration (milestone / all-done)
- Onboarding / new developer
- Post-incident / hard stop
- Documentation / reference

**Change type:** Step 2 paragraph replaced with expanded version including inline table. The 4 determination bullets are preserved.

**Rationale:** FEAT-004 is now self-contained for the key audience adaptation decision. The scorer's "cannot execute this instruction" finding is resolved. The FEAT-002 cross-reference is maintained for completeness.

---

## Fix 4: Template 3 Variable Dimension Count

**Target dimensions:** Completeness (0.88), Actionability (0.91)

**Location:** Message Templates > Template 3: Quality Gate REJECTED

**Scorer finding (Dimension 5):** "Template 3 is rigid at the three-dimension example. Template 3 (Quality Gate REJECTED) shows exactly 3 dimension entries. The template uses `{dimension_1}`, `{dimension_2}`, `{dimension_3}` as fixed slots. But a REJECTED score could have anywhere from 1 to 6 underperforming dimensions. There is no guidance on how to handle a REJECTED message with only 1 underperforming dimension or all 6 underperforming. The template implies exactly 3."

**Before:** Template body showed exactly three `{dimension_N}: {score_N} -- {diagnosis_N}` slots with no annotation about variable count.

**After:** Template is restructured into two variants:
1. **Multi-dimension case (2 or more):** Dimension block uses plain `{dimension}: {score} -- {diagnosis}` with a `[...repeat for each underperforming dimension...]` annotation.
2. **Single-dimension case (exactly 1):** Separate template variant with simplified closing line ("Address {dimension} directly. The gap to 0.92 runs through here.").

A preamble note is added: "The dimension block repeats once per underperforming dimension. Minimum 1, maximum 6."

**Change type:** Template body and variables block replaced. Content of the multi-dimension case is functionally identical to v0.4.0; no voice or information change.

**Rationale:** Eliminates the implied 3-slot constraint. The scorer's "implies exactly 3" finding is resolved. Implementers now have explicit guidance for both the common case (multiple dimensions) and the edge case (one dimension).

---

## Fix 5: Template 3 Priority Dimension Selection Algorithm

**Target dimensions:** Actionability (0.91), Evidence Quality (0.86)

**Location:** Message Templates > Template 3: Quality Gate REJECTED — Variables section

**Scorer finding (Dimension 5):** "'Start with {priority_dimension} -- it's pulling everything else down' (Template 3). The guidance for selecting `{priority_dimension}` is 'The dimension to fix first' — but no selection algorithm is provided. Is it always the lowest-scoring dimension? The one with the highest weight? This is ambiguous."

**Before:**
> `{priority_dimension}`: The dimension to fix first

**After:** Variable definition updated to "The dimension to fix first (see selection algorithm below)." A 3-step **Priority dimension selection algorithm** block is added:
1. Select the dimension with the lowest raw score.
2. If two or more dimensions are within 0.02 of each other (tie zone), prefer the dimension with the higher weight per quality-enforcement.md. Weight order provided explicitly.
3. In the single-dimension case, the priority dimension is that sole dimension; the "Start with" line simplifies to the single-dimension template.

**Change type:** New content block added after the Variables section. No existing content removed.

**Rationale:** Replaces ambiguous "the dimension to fix first" with a specific, deterministic rule. The tie-breaking criterion (weight from quality-enforcement.md) makes the rule executable without judgment. The scorer's "selection rule absent" finding is resolved.

---

## Fix 6: Template 11 Rule Explanation

**Target dimension:** Completeness (0.88)

**Location:** Message Templates section — new Template 11 added after Template 10

**Scorer finding (Dimension 1):** "Category 6 (Help Text & Documentation) has a before/after example but no standalone template in the Message Templates section — the category is present in the Voice Application Guide but absent from the template inventory. An implementer who looks only at the templates section will find no template for rule explanations or onboarding text."

**Scorer finding (Dimension 5):** "There is no Template 11 (Rule Explanation) or Template 12 (Onboarding Text) in the Message Templates section. An implementer working on rule explanations must extract the pattern from the before/after pair rather than a parameterized template. This is a genuine implementation ambiguity — how much of the rule explanation pattern is boilerplate vs. variable?"

**Added:** Template 11: Rule Explanation (Help Text)

Template structure:
```
{rule_id}: {rule_description}.

{threshold_or_constraint}

{reasoning}
```

Variables defined:
- `{rule_id}`: Rule identifier (e.g., H-13)
- `{rule_description}`: One-sentence statement of what the rule requires
- `{threshold_or_constraint}`: Quantitative/structural constraint stated plainly
- `{reasoning}`: WHY behind the rule (2–5 sentences). Closes with a direct sentence ("That's the logic." / "That's the tradeoff.")

Notes specify: no "H-13 says" preamble; reasoning explains WHY not WHAT; "That's the logic" is the voice contribution; use scope (help views, inline callouts, onboarding docs — NOT error messages).

Visual integration: Rule ID in Cyan (`COLOR_RULE`), body default, no decoration.

**Change type:** New template block added. No existing content modified.

**Rationale:** Category 6 now has a parameterized template. The before/after pair in the Voice Application Guide serves as the worked example; this template is the implementation artifact. The "boilerplate vs. variable" ambiguity the scorer identified is resolved by the variable definitions.

---

## Fix 7: Template 12 Generic Error

**Target dimension:** Completeness (0.88)

**Location:** Message Templates section — new Template 12 added after Template 11

**Scorer finding (Dimension 1):** "Error templates are thin. 5 error sub-types receive before/after examples in the Voice Application Guide, but only 1 (Missing Environment Variable) has a full named template (Template 5) in the Message Templates section. A developer implementing the error message layer must reverse-engineer templates from the before/after pairs in the Voice Application Guide — which is workable but not complete."

**Added:** Template 12: Generic Error

Template structure:
```
{error_identity}.

{optional_explanation}

{optional_diagnostic_action}
```

Variables defined:
- `{error_identity}`: What failed, stated directly. No "Error:" prefix. No bureaucratic framing.
- `{optional_explanation}`: One sentence of context when cause is not self-evident. For system-level failures: explicitly say this is a framework issue, not the developer's.
- `{optional_diagnostic_action}`: Copy-pasteable commands. Omit if no useful diagnostic action exists.

Population rules specify:
- Never omit `{error_identity}`.
- Developer-caused errors: include diagnostic action. System-caused errors: include explanation.
- Personality is not added; non-bureaucratic framing is the voice.

Scope note: covers File Not Found, Validation Error, Command Dispatcher, Session Handlers, and future error sub-types not addressed by Templates 4–5.

Visual integration: Default color; diagnostic commands in Cyan (`COLOR_PATH`); no decoration.

**Change type:** New template block added. No existing content modified.

**Rationale:** The 4 error sub-types with only before/after pairs (File Not Found, Validation Error, Command Dispatcher, Session Handlers) now have a parameterized template to implement against. The `{optional_*}` variable approach captures the pattern common to all 4 sub-types without forcing artificial uniformity. The scorer's "reverse-engineer from examples" finding is resolved.

---

## Version and Metadata Updates

**HTML comment header:** VERSION 0.4.0 → 0.5.0; STATUS updated to "REVISED (R4 targeted revision pass)".

**Document Metadata table:**
- Version: 0.4.0 → 0.5.0
- Status: Updated to reflect R4 targeted revision and adv-scorer-004 trigger
- Critic review row: updated to note R4 pass
- Next step: updated to "adv-scorer-004 re-score (S-014)"

**Document History table added** (new — not present in v0.4.0):

| Version | Change |
|---------|--------|
| 0.1.0 | Initial draft |
| 0.2.0 | R1: S-010 + S-003 (5 edits) |
| 0.3.0 | R2: S-002 (4 edits) |
| 0.4.0 | R3: S-007 (2 edits) |
| 0.5.0 | R4: targeted revision — Evidence Quality + Completeness fixes (6 surgical edits) |

**Self-Review Verification table:** Template count updated from "10 templates" to "12 templates (Templates 1–10 as before; Template 11: Rule Explanation; Template 12: Generic Error)".

---

## Projected Score Impact

These projections are estimates based on the scorer's stated penalty rationales. The definitive score will be produced by adv-scorer-004 re-run.

| Dimension | v0.4.0 Score | Fix(es) Applied | Projected v0.5.0 Score |
|-----------|-------------|-----------------|------------------------|
| Completeness (0.20) | 0.88 | Fix 4 (Template 3 slots), Fix 6 (Template 11), Fix 7 (Template 12), Fix 3 (Matrix embedded) | 0.93–0.95 |
| Evidence Quality (0.15) | 0.86 | Fix 1 (skiing claim), Fix 2 (conclusory note), Fix 3 (matrix embedded), Fix 5 (selection algorithm) | 0.91–0.93 |
| Actionability (0.15) | 0.91 | Fix 4 (Template 3 slots), Fix 5 (selection algorithm) | 0.93–0.95 |
| Internal Consistency (0.20) | 0.90 | No targeted fixes | 0.90 (unchanged) |
| Methodological Rigor (0.20) | 0.93 | No targeted fixes | 0.93 (unchanged) |
| Traceability (0.10) | 0.93 | No targeted fixes | 0.93 (unchanged) |

**Projected composite (conservative estimate):**

Using projected scores at the lower bounds of the ranges:
- Completeness: 0.93 × 0.20 = 0.186
- Internal Consistency: 0.90 × 0.20 = 0.180
- Methodological Rigor: 0.93 × 0.20 = 0.186
- Evidence Quality: 0.91 × 0.15 = 0.137
- Actionability: 0.93 × 0.15 = 0.140
- Traceability: 0.93 × 0.10 = 0.093

**Conservative projected composite: 0.922** — above the 0.92 threshold.

**Risk note:** The Actionability improvement is incidental to the Completeness fixes. If the scorer does not credit the Template 3 restructure as an Actionability improvement (because it was primarily a Completeness fix), the composite may sit closer to 0.918. A re-score is required for the definitive verdict.

---

## Change Summary

| Fix | Location | Dimension(s) Targeted | Change Type |
|-----|----------|-----------------------|-------------|
| Fix 1: Skiing vocabulary legibility | Anti-Pattern 7 — Why it fails | Evidence Quality | Inline sentence extension |
| Fix 2: File Not Found conclusory note | Category 2, File Not Found — voice application notes | Evidence Quality | Inline bullet extension |
| Fix 3: Audience Adaptation Matrix embedded | Integration Workflow, Step 2 | Evidence Quality, Completeness | Step 2 paragraph + new table added |
| Fix 4: Template 3 variable slot count | Message Templates, Template 3 body | Completeness, Actionability | Template body restructured (2 variants) |
| Fix 5: Template 3 priority dimension algorithm | Message Templates, Template 3 variables | Actionability, Evidence Quality | New algorithm block added after variables |
| Fix 6: Template 11 Rule Explanation | Message Templates — new template | Completeness | New template block added |
| Fix 7: Template 12 Generic Error | Message Templates — new template | Completeness | New template block added |
| Version + metadata | HTML comment, Document Metadata, Self-Review | — | Version bump 0.4.0 → 0.5.0; Document History added |

**Total distinct change locations: 8** (7 content fixes + 1 metadata update)

**Scope verification:** No sections were rewritten. No content was removed. All fixes are additive (extensions or new blocks) except Template 3's body restructure, which preserves all v0.4.0 information while adding the single-dimension variant and the `[...repeat...]` annotation.

---

## Review Metadata

| Attribute | Value |
|-----------|-------|
| Round | R4 (targeted revision pass) |
| Trigger | adv-scorer-004 score report — composite 0.901 < 0.92 threshold |
| Strategies applied | Surgical fix (no strategy invocation — this is a targeted revision pass, not an adversarial review) |
| Findings addressed | 6 scorer findings across Evidence Quality and Completeness |
| Draft version before | 0.4.0 |
| Draft version after | 0.5.0 |
| Reviewer | ps-critic-004 |
| Date | 2026-02-19 |
