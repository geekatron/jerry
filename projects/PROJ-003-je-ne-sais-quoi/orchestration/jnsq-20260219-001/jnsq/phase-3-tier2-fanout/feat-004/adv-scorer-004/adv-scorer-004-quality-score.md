# adv-scorer-004: S-014 Quality Score — FEAT-004 Framework Voice & Personality

<!--
AGENT: adv-scorer-004
ROLE: S-014 LLM-as-Judge Quality Scorer
DELIVERABLE: ps-creator-004-draft.md (FEAT-004 Framework Voice & Personality, v0.4.0)
STRATEGY: S-014 (LLM-as-Judge)
CRITICALITY: C2 (Standard)
THRESHOLD: >= 0.92 (H-13)
DATE: 2026-02-19
INDEPENDENCE: Scored fresh. Critic round estimates NOT anchored to.
-->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scoring Methodology](#scoring-methodology) | How this score was produced |
| [Dimension Scores](#dimension-scores) | Per-dimension scores with justification |
| [Strengths](#strengths) | What the deliverable does well |
| [Weaknesses](#weaknesses) | Where the deliverable falls short |
| [Composite Score and Verdict](#composite-score-and-verdict) | Weighted total and PASS/REVISE/REJECTED |
| [Revision Guidance](#revision-guidance) | Targeted recommendations (if REVISE/REJECTED) |
| [Score Metadata](#score-metadata) | Machine-readable YAML |

---

## Scoring Methodology

This scoring applies S-014 (LLM-as-Judge) as defined in `quality-enforcement.md`. The scorer is independent — it has not been seeded with any critic estimates and does not anchor to the three-round ps-critic-004 review conclusions. Evidence is drawn exclusively from the artifact at v0.4.0.

**Anti-leniency protocol in effect:** Each dimension is scored on what is demonstrably present in the artifact, not on what was intended, what was fixed, or what the reviewer believes would have been produced. Hedged language, assumed context, and referenced-but-not-present content are scored as absent.

**FEAT-004 requirements source:** EPIC-001-je-ne-sais-quoi.md Feature Inventory (FEAT-004: "Quality gate messages, hook outputs, error messages with character. The McConkey energy: technically precise, never dry.") and the implementation scope as bounded by the deliverable's own stated scope.

---

## Dimension Scores

### Dimension 1: Completeness (weight 0.20)

**Score: 0.88**

**Rubric question:** Does the deliverable fully address all FEAT-004 requirements?

**What FEAT-004 requires:** Per EPIC-001, FEAT-004 covers "quality gate messages, hook outputs, error messages with character." The deliverable self-scopes to 6 message categories: Quality Gate, Errors, CLI Session, Hook Output, Progress/Status, Help/Documentation.

**Evidence for high score:**

- All 6 self-declared categories are fully covered with tone guidance, before/after examples, voice application notes, and boundary conditions.
- 10 concrete message templates with complete variable documentation.
- 8 anti-patterns with specific failure mode identification.
- Integration workflow covers both lightweight and full paths.
- Visual integration section maps FEAT-003 to every category.
- Traceability covers 7 source documents.
- The scope exclusion (JSON output mode) is explicitly documented in the Core Principle section.

**Evidence for score penalty:**

- **Template coverage is uneven.** The deliverable provides 10 named templates but these cluster heavily around quality gate and session messages. Category 6 (Help Text & Documentation) has a before/after example but no standalone template in the Message Templates section — the category is present in the Voice Application Guide but absent from the template inventory. An implementer who looks only at the templates section will find no template for rule explanations or onboarding text.

- **Error templates are thin.** 5 error sub-types receive before/after examples in the Voice Application Guide, but only 1 (Missing Environment Variable) has a full named template (Template 5) in the Message Templates section. A developer implementing the error message layer must reverse-engineer templates from the before/after pairs in the Voice Application Guide — which is workable but not complete.

- **No explicit template for Hook Output errors.** The SessionStart Hook: Invalid Project sub-type has a before/after pair but no standalone template. If a developer working on hook rendering wants the canonical one-liner, they must find it in the Voice Application Guide section rather than the template inventory.

- **Future-proofing gap.** The document instructs that new message types "should be classified using the Audience Adaptation Matrix and added to this document," but the Audience Adaptation Matrix is not defined within this document — it is referenced as coming from SKILL.md (FEAT-002). An implementer who is working on FEAT-004 without FEAT-002 context cannot execute this instruction.

**Deductions from a high baseline:** The core categorical inventory is complete and well-specified. The gaps are at the template layer (3-4 missing templates) and one unresolved forward reference. These are real but not structural. Score: 0.88.

---

### Dimension 2: Internal Consistency (weight 0.20)

**Score: 0.90**

**Rubric question:** Are all parts internally consistent (no contradictions, aligned terminology)?

**Evidence for high score:**

- Tone graduation is internally consistent across all 4 quality gate sub-categories. The Humor Deployment column (None / Gentle / Yes / None for REJECTED, REVISE, PASS, Constitutional) is applied consistently in every example and template.
- REVISE semantic accuracy is correct after R3 edit: Sub-Category 1b explicitly states "still rejected per H-13" and the template does not suggest otherwise. Score band language (PASS/REVISE/REJECTED) matches quality-enforcement.md SSOT exactly.
- The Core Principle ("Clarity ALWAYS trumps personality") is operationally consistent in the templates — every template includes all technical information before any voice element.
- Visual Budget Per Category table is consistent with the per-category visual notes in each Voice Application Guide sub-section.
- Integration workflow (6 steps) and the Lightweight Path (3 steps) are consistent: the Lightweight Path correctly identifies that full workflow is required for quality gate, novel error types, celebration session messages, and substantial transformations.
- Anti-pattern citations consistently map to named Boundary Conditions (e.g., Anti-Pattern 3 cites #7, #4, and Authenticity Test 3).

**Evidence for score penalty:**

- **Template 7 / Self-Review discrepancy.** Template 7 (Session End All Items Complete) specifies `skier` emoji prefix on "All items landed" in full terminals. The Visual Budget Per Category table for "Session End (all done)" shows "Skier (1 max)" in the Emoji column. The voice application note in the Session End (All Items Complete) sub-section does not mention this emoji; it only discusses the box-art and "Saucer Boy approves" identifier. An implementer reading the voice application note section alone would not know about the emoji. Minor but inconsistent.

- **Priority Order vs. Lightweight Path alignment.** The Priority Order table in Message Categories ranks Help and Documentation as priority 5 and Progress indicators as priority 6. The Lightweight Path designates Categories 4-6 as eligible for lightweight treatment. However, Priority Order uses 1-5 scale (priority 1 = quality gate messages, priority 5 = help/documentation, priority 6 = progress indicators), while Message Categories uses 1-6 numbering. The Lightweight Path says "Categories 4-6" using the Category numbering (Hook output, Progress, Help/Documentation). This is correct, but a reader skimming the Priority Order table (which goes to priority 6) might conflate the two numbering systems. Low severity, but could create confusion.

- **"Categories Not Covered" exclusion rationale is slightly inconsistent.** The section states transcript output is "covered by Category 5 (Progress & Status Indicators) patterns" — which is correct. But the Priority Order table ranks progress indicators as priority 6 ("Lowest priority — efficiency is the job"), signaling minimal voice. This is actually consistent, but a reader might expect the transcript command to get its own explicit callout given the framework has a dedicated `/transcript` skill. Not a true inconsistency, but a potential confusion point.

These are minor friction points, not structural contradictions. Score: 0.90.

---

### Dimension 3: Methodological Rigor (weight 0.20)

**Score: 0.93**

**Rubric question:** Is the approach systematic, well-structured, following best practices?

**Evidence for high score:**

- The document is structured from principle to application: Core Principle (load-bearing constraint) → Message Categories (inventory and classification) → Voice Application Guide (per-category specification) → Message Templates (concrete implementation artifacts) → Integration Workflow (operational process) → Anti-Patterns (negative calibration) → Visual Integration (cross-feature bridge) → Traceability → Self-Review Verification.

- This is a sound specification document structure. Each section has a distinct purpose and there is no redundancy between sections.

- The Audience Adaptation Matrix is explicitly referenced for context-dependent decisions, and the before/after pairs include voice application notes that explain the reasoning rather than just showing the result.

- The integration workflow distinguishes between lightweight and full paths with explicit criteria for each. The criteria are precise: full workflow is REQUIRED for quality gate messages, new error types not in templates, session celebration messages, and any message where transformation substantially changes text. This prevents the lightweight path from becoming a general-purpose shortcut.

- The graduated tone system (Full Energy / Medium / Low / Hard Stop) is systematic and consistent with the source persona document's Tone Spectrum.

- Calibration pairs from voice-guide.md are cited per sub-category, providing a traceable source for the tone decisions.

- The anti-pattern section uses 8 examples that cover distinct failure modes (sarcasm, performative quirkiness, diagnosis-obscuring humor, corporate formalism, high-stakes humor, empty personality, forced skiing references, grandiosity) — this is comprehensive and avoids repetition between entries.

- The R1-R3 review cycle applied S-010, S-003, S-002, and S-007 in the correct H-16-compliant order (steelman before devil's advocate).

**Evidence for score penalty:**

- **The Workflow Summary Diagram is asymmetric.** The diagram shows a feedback loop for below-target scoring (Step 6 → Steps 3-5) but does not show what happens when the full 6-step workflow identifies an information gap at Step 1 validation. The diagram shows the information gap fix as a bottom-level path labeled "Fix information gap if Test 1 fails" — but the arrow's return point is ambiguous. Does the developer restart at Step 1? Go back to content writing? The diagram notation (`+-----+` box at bottom with arrow back to the left) is hard to trace without the text context. This is a minor usability gap in the workflow section.

- **No explicit guidance on when to update this document.** The document specifies that new message types should be added to it, but there is no versioning protocol, no maintenance owner, and no process for triggering updates when FEAT-003 finalizes its color constants. The dependency note in Visual Integration acknowledges this but does not resolve it. For a specification document that will be used as a living reference, this is a meaningful gap.

These are procedural gaps rather than methodological failures. The structure, rigor, and systematic approach are strong. Score: 0.93.

---

### Dimension 4: Evidence Quality (weight 0.15)

**Score: 0.86**

**Rubric question:** Are claims supported by evidence, citations, concrete examples?

**Evidence for high score:**

- Before/after pairs provide concrete evidence for every voice application claim. The before examples are verified as honest representations of current CLI output (traceability section maps to `src/interface/cli/adapter.py` and `scripts/session_start_hook.py`).

- Traceability table maps 7 source documents to specific sections referenced. This is not a vague "based on persona doc" assertion — it names specific artifacts (ps-creator-001-draft.md, ps-creator-002-draft.md, ps-creator-003-draft.md, adapter.py, main.py, session_start_hook.py, quality-enforcement.md) and specifies which sections of each document were used.

- Anti-patterns cite specific boundary conditions and authenticity tests by number, providing a direct link between the failure example and the governance constraint being violated.

- Calibration pairs (voice-guide.md Pair 1, Pair 2, Pair 3, Pair 6, Pair 7) are cited by number per sub-category, providing traceable sources for tone decisions.

- "Biographical anchors" (banana-suit energy, iteration energy, meticulous preparation energy) are named per sub-category with reference to the persona doc's constructs. These anchors are not arbitrary — they are derived from the persona distillation.

**Evidence for score penalty:**

- **The 124 print statement count claim is not independently verifiable from the document.** The Self-Review Verification states "src/interface/cli/adapter.py (124 print statements)" — this is a specific, verifiable claim. However, the document presents it as a self-verified count with no citation (e.g., no line range, no method). An auditor reading this document cannot verify the count without independently running a search. The claim is specific enough to be falsifiable (which is good), but the evidence is unverifiable from the document alone.

- **The Audience Adaptation Matrix is cited but not reproduced.** Multiple sections reference the Audience Adaptation Matrix for context-dependent decisions (e.g., Step 2 of the integration workflow, the Onboarding Text guidance in Category 6). The matrix is defined in FEAT-002's SKILL.md. For FEAT-004 to function as a standalone specification, the matrix — or at minimum a summary row for the key audience contexts — should be present. As-is, a developer implementing FEAT-004 without access to FEAT-002 cannot execute the audience adaptation guidance.

- **"Transparent to non-skiers" claim for skiing vocabulary.** The document claims that "clean run," "drop in," and "powder day" are "transparent to non-skiers" (Authenticity Test 3 compliance). This is a behavioral claim about audience legibility, but no evidence is provided — no user testing, no citation of a legibility study, and no definition of "transparent." The claim may be accurate, but it is asserted rather than demonstrated. In a HARD evidence dimension, assertion-without-support is a penalty.

- **Some "voice application notes" are conclusory.** For example, in the File Not Found error sub-type: "No personality is needed here. The directness IS the personality." This is a claim about the persona's behavior, not a demonstration of it. The anti-patterns section provides detailed reasoning for why things fail; the boundary cases in the voice application guide are thinner.

Score: 0.86. The traceability and concrete examples are good. The unsupported behavioral claims and the absent Audience Adaptation Matrix are material gaps.

---

### Dimension 5: Actionability (weight 0.15)

**Score: 0.91**

**Rubric question:** Can someone implement this directly without ambiguity?

**Evidence for high score:**

- The 10 templates with `{placeholder}` variables are directly implementable. Variable documentation is specific (e.g., `{gap_description}` specifies when "Close" is appropriate; `{forward_guidance}` is illustrated with an example).

- The Lightweight Path gives implementers a clear decision rule: for Categories 4-6 and minimal transformations, use direct application. For Categories 1-3 and substantial transformations, use full workflow.

- Integration workflow Steps 3-5 provide concrete invocation prompts for sb-rewriter, sb-reviewer, and sb-calibrator, including the SB CONTEXT block format. An implementer can copy-paste these invocations.

- Visual Budget Per Category table gives unambiguous rendering decisions per message type (color, emoji, box-art, bold, dim). This is directly implementable by a terminal rendering engineer.

- NO_COLOR compliance, graceful degradation (3 tiers), and the 80-character constraint on hook systemMessage are all specific and actionable.

- The "Authenticity Test 1 validation" instruction at Step 1 of the workflow gives a concrete gate: "If removing all voice elements would leave the developer without what they need, the content is not ready for voice. Fix the information gap first." This is actionable.

**Evidence for score penalty:**

- **No template for Category 6 (Help Text & Documentation).** The Voice Application Guide for Category 6 provides before/after examples for rule explanations, CLI help text, and onboarding text. But there is no Template 11 (Rule Explanation) or Template 12 (Onboarding Text) in the Message Templates section. An implementer working on rule explanations must extract the pattern from the before/after pair rather than a parameterized template. This is a genuine implementation ambiguity — how much of the rule explanation pattern is boilerplate vs. variable?

- **Template 3 is rigid at the three-dimension example.** Template 3 (Quality Gate REJECTED) shows exactly 3 dimension entries. The template uses `{dimension_1}`, `{dimension_2}`, `{dimension_3}` as fixed slots. But a REJECTED score could have anywhere from 1 to 6 underperforming dimensions. There is no guidance on how to handle a REJECTED message with only 1 underperforming dimension or all 6 underperforming. The template implies exactly 3.

- **"Start with {priority_dimension} -- it's pulling everything else down" (Template 3).** The guidance for selecting `{priority_dimension}` is "The dimension to fix first" — but no selection algorithm is provided. The preceding text says "Start with completeness -- it's pulling everything else down" in the example, but the general rule for selecting the priority dimension when all 3 are at roughly equal depths is not specified. Is it always the lowest-scoring dimension? The one with the highest weight? This is ambiguous.

Score: 0.91. Strong actionability overall. The missing Category 6 templates and the Template 3 rigid slot count are real implementation gaps.

---

### Dimension 6: Traceability (weight 0.10)

**Score: 0.93**

**Rubric question:** Can we trace requirements to implementation and back?

**Evidence for high score:**

- The Traceability section explicitly maps 7 source documents to sections referenced. Each entry specifies the source artifact, its role in the derivation, and which sections were used.

- EPIC-001 requirements (quality gate messages, hook outputs, error messages with character) are directly addressed by the document's Category 1, 4, and 2 respectively.

- Score band labels (PASS/REVISE/REJECTED thresholds, SSOT alignment) were verified in R3 and confirmed aligned with quality-enforcement.md.

- Calibration pairs (Pair 1-7) are cited by number per sub-category, creating a traceable link from each message to its persona doc source.

- The Self-Review Verification (S-010) checklist includes 17 checks with evidence, providing a self-audit trail for completeness.

- The Document Metadata section records the 3-round critic review chain with version increments (0.1.0 → 0.2.0 → 0.3.0 → 0.4.0) and strategy labels per round.

**Evidence for score penalty:**

- **FEAT-001 (Persona Distillation) is the canonical voice source but the version referenced is "v0.9.0."** The traceability entry names the file as `ps-creator-001-draft.md (Persona Distillation v0.9.0)`. If the Persona Distillation advances to 1.0.0 before FEAT-004 is implemented, the voice guidance could be based on a superseded version. There is no protocol for version tracking between dependent features.

- **The EPIC-001 requirements are loosely paraphrased, not directly quoted.** The document's scope is derived from the EPIC, but the EPIC's formal feature definition ("Quality gate messages, hook outputs, error messages with character. The McConkey energy: technically precise, never dry.") is not quoted or cited in the deliverable itself. A formal traceability audit would want to see the requirements quoted at the top of the specification.

Score: 0.93. The traceability is strong. The version pinning gap and absent explicit requirements citation are minor but real.

---

## Strengths

1. **Core Principle placement and clarity.** Making "Clarity ALWAYS trumps personality" the load-bearing constraint, placed first, traced to Authenticity Test 1, with an explicit corollary — this is architecturally sound and well-executed.

2. **Graduated tone across quality gate sub-categories.** The four sub-categories (PASS / REVISE / REJECTED / Constitutional Failure) demonstrate precise, consistent tone graduation. The humor deployment rules follow correctly: earned celebration, gentle encouragement, diagnostic precision, and zero-humor hard stop. This is the document's strongest section.

3. **Before/after pairs with reasoning.** Every pair includes voice application notes that explain WHY rather than just showing the result. This makes the document teachable, not just referenceable.

4. **Anti-pattern section.** 8 anti-patterns covering distinct failure modes. Anti-Pattern 3 (humor obscuring diagnosis) and Anti-Pattern 7 (forced skiing references) are particularly well-chosen — they address failure modes that are plausible and genuinely difficult to detect without explicit guidance. Each anti-pattern includes boundary condition citations.

5. **Lightweight path addition (R2 improvement).** The distinction between minimal-transformation and substantial-transformation messages addresses the real adoption risk of requiring 3 agent invocations to remove an "Error:" prefix. The criteria for when each path applies are clear.

6. **Visual integration bridge.** The Visual Budget Per Category table is a clean decision matrix that an implementer can use without reading the full Visual Application Guide. The graceful degradation specification (3 tiers) and NO_COLOR compliance are well-specified for a terminal rendering implementer.

---

## Weaknesses

1. **Template inventory is incomplete.** Category 6 (Help Text & Documentation) and non-env-var error types have before/after examples in the Voice Application Guide but no parameterized templates in the Message Templates section. An implementer working from templates alone will find gaps in Category 2 and Category 6.

2. **Audience Adaptation Matrix is absent.** The matrix is referenced as the authoritative tool for audience-dependent voice decisions but is defined in FEAT-002 (SKILL.md), not here. FEAT-004 should be actionable without requiring the reader to navigate to a dependency document.

3. **Template 3 rigid slot count.** The REJECTED template uses exactly 3 dimension slots. No guidance covers the 1-dimension or 6-dimension REJECTED case. The priority dimension selection algorithm is absent ("the dimension to fix first" is not a selection rule).

4. **Behavioral claims asserted without evidence.** "Transparent to non-skiers" (skiing vocabulary legibility), "the directness IS the personality" (file-not-found case), and the 124 print statement count are asserted without independently verifiable evidence. The skiing vocabulary claim is the most material, as it is a behavioral prediction about audience reception.

5. **Workflow diagram ambiguity.** The information gap feedback loop in the Workflow Summary Diagram does not clearly indicate whether the developer returns to Step 1, restarts content writing, or takes some other action. The ASCII diagram notation is ambiguous at the feedback junction.

6. **No document maintenance protocol.** The deliverable will require updates when FEAT-003 finalizes color constants and when FEAT-001 advances to v1.0.0. No update trigger or owner is defined.

---

## Composite Score and Verdict

| Dimension | Raw Score | Weight | Weighted Score |
|-----------|-----------|--------|----------------|
| Completeness | 0.88 | 0.20 | 0.176 |
| Internal Consistency | 0.90 | 0.20 | 0.180 |
| Methodological Rigor | 0.93 | 0.20 | 0.186 |
| Evidence Quality | 0.86 | 0.15 | 0.129 |
| Actionability | 0.91 | 0.15 | 0.137 |
| Traceability | 0.93 | 0.10 | 0.093 |
| **COMPOSITE** | | **1.00** | **0.901** |

**Weighted composite score: 0.901**

**Band: REVISE (0.85 - 0.91)**

**Verdict: REVISE — deliverable is rejected per H-13. Targeted revision is likely sufficient to reach >= 0.92.**

The deliverable does not meet the 0.92 threshold by 0.019 points. This is not a structural failure — the core architecture (Core Principle, tone graduation, before/after pairs, integration workflow) is strong. The gap is driven by two dimensions that scored below 0.91: Evidence Quality (0.86) and Completeness (0.88). These are the revision targets.

---

## Revision Guidance

The following is targeted to the two weakest dimensions. Addressing both is likely sufficient to cross the 0.92 threshold.

### Priority 1: Completeness (scored 0.88, target >= 0.92)

Add the following to the Message Templates section:

1. **Template 11: Rule Explanation.** Parameterize the pattern from the Category 6 before/after pair. Variables: `{rule_id}`, `{rule_description}`, `{threshold_or_constraint}`, `{reasoning}`. This fills the only category with no standalone template.

2. **Template 12 (or lightweight guidance): Generic Error.** The 4 error sub-types without templates (File Not Found, Validation Error, Command Dispatcher, Session Handlers) share a common pattern: state the fact, add one explanatory line or diagnostic action. A generic error template with `{error_identity}`, `{optional_explanation}`, `{optional_diagnostic_action}` would cover these cases.

3. **Audience Adaptation Matrix summary table.** Extract the relevant rows from FEAT-002 SKILL.md and embed a summary (at minimum: the audience contexts used in this document — active-session, debugging, onboarding, documentation, post-incident) directly in the Integration Workflow Step 2. This makes FEAT-004 self-contained for the key decision point.

### Priority 2: Evidence Quality (scored 0.86, target >= 0.92)

1. **Skiing vocabulary legibility claim.** Add a note to the vocabulary restriction in the Core Principle or Voice Application Guide acknowledging that "transparent" means "decodable from context without skiing knowledge" and cite the Authenticity Test 3 definition from the persona doc. Replace the bare assertion with the test criterion.

2. **Template 3 priority dimension selection algorithm.** Specify the selection rule: "Select the dimension with the lowest score. If two dimensions are within 0.02 of each other, prefer the dimension with the higher weight (per quality-enforcement.md weight table)." Add this to the `{priority_dimension}` variable documentation.

3. **Template 3 variable count.** Replace `{dimension_1}`, `{dimension_2}`, `{dimension_3}` fixed slots with a note that the template repeats the dimension block for each underperforming dimension. Explicitly note: "If only one dimension is underperforming, omit the count prefix ('N dimensions are underperforming') and state the single dimension directly."

These revisions address the material gaps without requiring structural changes to the document. The core architecture is sound and should not be revised.

---

## Score Metadata

```yaml
scorer: adv-scorer-004
strategy: S-014 (LLM-as-Judge)
deliverable: ps-creator-004-draft.md
deliverable_version: "0.4.0"
feature: FEAT-004
criticality: C2
date: "2026-02-19"
threshold: 0.92
dimensions:
  completeness:
    score: 0.88
    weight: 0.20
    weighted: 0.176
  internal_consistency:
    score: 0.90
    weight: 0.20
    weighted: 0.180
  methodological_rigor:
    score: 0.93
    weight: 0.20
    weighted: 0.186
  evidence_quality:
    score: 0.86
    weight: 0.15
    weighted: 0.129
  actionability:
    score: 0.91
    weight: 0.15
    weighted: 0.137
  traceability:
    score: 0.93
    weight: 0.10
    weighted: 0.093
composite_score: 0.901
band: REVISE
verdict: REJECTED_PER_H13
revision_required: true
revision_priority:
  - completeness
  - evidence_quality
weakest_dimensions:
  - name: evidence_quality
    score: 0.86
  - name: completeness
    score: 0.88
independence: true
anchoring_suppressed: true
```
