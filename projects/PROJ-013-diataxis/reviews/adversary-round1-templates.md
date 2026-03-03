# Adversarial Review: Templates (Round 1)

## Execution Context

- **Strategies Applied:** S-007 (Constitutional AI Critique), S-013 (Inversion Technique), S-002 (Devil's Advocate), S-010 (Self-Refine)
- **Deliverables Reviewed:**
  - `skills/diataxis/templates/tutorial-template.md`
  - `skills/diataxis/templates/howto-template.md`
  - `skills/diataxis/templates/reference-template.md`
  - `skills/diataxis/templates/explanation-template.md`
- **Reference Standard:** `skills/diataxis/rules/diataxis-standards.md`
- **Quality Threshold:** >= 0.95 weighted composite
- **Executed:** 2026-02-27
- **Finding Prefixes:** CC-NNN (S-007), IN-NNN (S-013), DA-NNN (S-002), SR-NNN (S-010)

### H-16 Note

S-002 (Devil's Advocate) was executed without a prior S-003 (Steelman) pass, as the user's explicit strategy ordering constitutes informed authority per H-02 (user authority). To satisfy the spirit of H-16 (strengthen before critique), the steelman position is acknowledged here: the templates are intentionally lean, avoiding over-prescription that would constrain writer judgment and make templates harder to maintain. This position is held in mind during all S-002 analysis.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Per-Template Summary](#per-template-summary) | Quality criteria coverage, anti-pattern protection, gaps |
| [S-007 Constitutional Compliance](#s-007-constitutional-compliance) | Criteria match, anti-pattern presence, cross-reference convention |
| [S-013 Inversion Analysis](#s-013-inversion-analysis) | What would make these templates produce bad documentation |
| [S-002 Devil's Advocate Findings](#s-002-devils-advocate-findings) | Voice enforcement, placeholder clarity, compliance test, mixing prevention |
| [S-010 Self-Refine Recommendations](#s-010-self-refine-recommendations) | Specific improvements with severity classification |
| [Finding Summary Table](#finding-summary-table) | All findings consolidated |
| [Quality Assessment](#quality-assessment) | Composite score estimate and threshold verdict |

---

## Per-Template Summary

| Template | Quality Criteria Met | Anti-Pattern Protection | Voice Enforcement | Quadrant Mixing Prevention | Placeholder Clarity |
|----------|---------------------|------------------------|-------------------|---------------------------|---------------------|
| Tutorial | T-02, T-06, T-07 met; T-01, T-03, T-04, T-05, T-08 not structurally enforced | TAP-02, TAP-03 unguarded | None embedded | Insufficient | Adequate except `{Brief instruction.}` |
| How-To | H-01, H-02 (partial, Step 1 only), H-03 met; H-04, H-06 not enforced | HAP-01 partially guarded in Step 1; Step 3 unguarded | None embedded | Step 1 guarded; Step 3 unguarded | `{what success looks like}` inadequate |
| Reference | R-02, R-04 (partial), R-05, R-06 met; R-01, R-07 not template-enforceable | RAP-01 partially guarded; RAP-02, RAP-03 unguarded | None embedded | Adequate for structural anti-patterns; RAP-02 unguarded | `{Category 1}` inadequate |
| Explanation | E-01, E-02, E-03, E-04, E-05 met; E-06, E-07 not structurally enforced | EAP-01, EAP-05 unguarded | None embedded | Insufficient; section heading placeholders invite procedural names | `{Core Concept 1}` misleading |

**Overall assessment:** The templates correctly enforce the structural anatomy of each quadrant. They fail to embed voice guidance, fail to prevent three of four quadrant-mixing anti-patterns, and several placeholders underdetermine what compliant content looks like. A writer agent filling in these templates could produce structurally valid but quadrant-contaminated, voice-non-compliant documents without violating any template constraint. The critical gap: no template references `diataxis-standards.md`, making quality criteria, anti-patterns, and voice guidelines invisible to agents using the template as their only input.

---

## S-007 Constitutional Compliance

*Strategy: Verify (a) each template structurally matches its quadrant's quality criteria in diataxis-standards.md, (b) templates do not contain anti-patterns for their own quadrant, (c) cross-reference links follow Jerry convention.*

### CC-001: Tutorial — T-08 (Reliable Reproduction) Has No Template Enforcement

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `tutorial-template.md` — Steps 1–3 (lines 20–60) |
| **Strategy Step** | S-007 check (a): structural match to quality criteria |

**Evidence:**
The tutorial template contains three step sections with `{command or code}` and `{expected output}` placeholders. No placeholder, comment, or structural element prompts the writer to verify that steps are reproducible before publishing.

**Analysis:**
T-08 requires "Reliable reproduction: Following the steps produces the documented outcome. Tested end-to-end." TAP-05 (Untested steps) is classified as Critical severity in diataxis-standards.md. The template structurally enables TAP-05 by providing output placeholder slots without any signal that those outputs must come from an actual run. A writer who invents plausible-looking output satisfies all template slots without triggering any constraint.

**Recommendation:**
Add a comment at the end of the Steps section:
```
<!-- T-08 Compliance: Before publishing, verify all commands run on the target environment
     and produce the exact output shown. Replace {expected output} with captured actual output. -->
```

---

### CC-002: Tutorial — T-03 and T-04 Have No Structural Enforcement

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `tutorial-template.md` — Step body placeholders (lines 22, 36, 50) |
| **Strategy Step** | S-007 check (a) + check (b) |

**Evidence:**
Step body placeholder text: `{Brief instruction.}` across all three steps. No constraint against explanatory prose (T-03) or alternative-offering constructions (T-04).

**Analysis:**
T-03 requires no step to assume knowledge not introduced earlier. T-04 requires exactly one path — zero "alternatively" or "you could also" constructions. Anti-patterns TAP-02 (extended explanation) and TAP-03 (offering choices) are both Major severity. The placeholder `{Brief instruction.}` provides no protection against either. A writer who inserts "This works because..." between steps or "Alternatively, you can use command B" violates both criteria without deviating from the template's guidance.

**Recommendation:**
Change step body placeholder to: `{Action instruction — imperative verb required. ONE path only. Do NOT explain why. Do NOT offer alternatives. "Why" belongs in an Explanation document; alternatives belong in a How-To Guide.}`

---

### CC-003: Tutorial — T-07 Intent Undermined by Abstract Completion State Placeholder

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `tutorial-template.md` — line 3 |
| **Strategy Step** | S-007 check (a) |

**Evidence:**
Tagline placeholder: `{One-sentence description of what the reader will achieve.}`

**Analysis:**
T-07 requires "Reader knows what they will achieve before starting." The test is: does the reader know the CONCRETE ENDPOINT? The placeholder permits "Learn about configuration" (abstract learning goal) or "Understand how pipelines work" (comprehension claim). Both satisfy the template while violating T-07's intent that the endpoint be a concrete, observable completion state — something the reader will HAVE, not something they will KNOW.

**Recommendation:**
Change to: `{One-sentence concrete completion state. Format: "You will have [artifact or working system] that [observable behavior]." Example: "You will have a running local deployment that responds to requests on port 8080."}`

---

### CC-004: How-To — Step 3 Loses the H-02 Anti-Explanation Enforcement

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `howto-template.md` — line 39 vs. line 15 |
| **Strategy Step** | S-007 check (a) + check (b) |

**Evidence:**
- Step 1 body (line 15): `{Direct instruction. No explanation of why.}`
- Step 3 body (line 39): `{Direct instruction.}`

The anti-explanation clause `No explanation of why.` is present in Step 1 and absent from Step 3.

**Analysis:**
H-02 requires action-only content across all steps — not just Step 1. HAP-01 (conflating with tutorial — explanatory insertion) is Major severity. The inconsistency creates an unguarded injection point specifically in the final step, which is precisely where writers feel the urge to add closure rationale ("Now your service is configured, which means..."). The inconsistency will predictably produce H-02 violations at the end of guides.

**Recommendation:**
Change Step 3 body placeholder to: `{Direct instruction. No explanation of why.}` — consistent with Step 1.

---

### CC-005: Explanation — E-06 (Bounded Scope) Has No Template Element

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `explanation-template.md` — full document structure |
| **Strategy Step** | S-007 check (a) |

**Evidence:**
The explanation template has: title, tagline, Context, Core Concept 1, Core Concept 2, Connections, Alternative Perspectives, Further Reading. No section or placeholder states the scope boundary.

**Analysis:**
E-06 requires "Bounded scope. Does not try to cover everything. Clear topic boundary stated." EAP-05 (Unbounded scope) is classified as Major severity in diataxis-standards.md. The template provides no structural slot for scope declaration. A writer can expand an explanation to cover adjacent topics, related technologies, and historical context without any template constraint resisting the expansion. This is structurally unconstrained by design — but it produces a Major quality gap.

**Recommendation:**
Add a scope statement below the tagline:
```
> **Scope:** This document explains {specific aspect of topic}. It does not cover {what is explicitly out of scope}.
```

---

### CC-006: Explanation — E-07 (No Imperative Instructions) Has No Template Warning

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `explanation-template.md` — Core Concept body placeholders (lines 11–13, 16–17) |
| **Strategy Step** | S-007 check (b): anti-patterns for own quadrant |

**Evidence:**
Core concept body placeholder: `{Discursive prose exploring the concept. No numbered steps. Make connections to related ideas. Explain *why*, not just *what*.}`

The placeholder prohibits numbered steps but says nothing about imperative verbs.

**Analysis:**
E-07 requires zero "Run this command" or "Configure X" constructions. EAP-01 (Instructional creep) is Major severity. The placeholder's `No numbered steps.` instruction prevents one symptom of EAP-01 (step sequences) but not the underlying cause (imperative voice). A writer who adds "Set the log level to DEBUG to see detailed output" violates E-07 without using a numbered step list.

**Recommendation:**
Add to the body placeholder: `Do NOT use imperative verbs (run, configure, set, install). If you find yourself writing instructions, move that content to a How-To Guide.`

---

### CC-007: All Templates — Zero Voice Guidance Embedded

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | All four templates |
| **Strategy Step** | S-007 check (a): structural match to quality criteria |

**Evidence:**
No template contains any reference to diataxis-standards.md Section 5 (Jerry Voice Guidelines). No template embeds per-quadrant register guidance, tone description, or anti-examples.

**Analysis:**
The voice quality gate in diataxis-standards.md Section 5 requires writer agents to check output against universal voice markers and per-quadrant guidelines during H-15 self-review. Templates are the primary artifact writer agents use. Without voice guidance embedded in or explicitly referenced from the templates, writer agents using only the template as input will produce structurally correct but register-non-compliant output. This is a systemic gap, not a single-document issue.

**Recommendation:**
Add a writer agent instruction block at the top of each template (see SR-001).

---

### CC-008: Cross-Reference Section Naming Inconsistency

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | All four templates — cross-reference section headings |
| **Strategy Step** | S-007 check (c): cross-reference links follow Jerry convention |

**Evidence:**
- `tutorial-template.md`: `## Next Steps`
- `howto-template.md`: `## Related`
- `reference-template.md`: `## Related`
- `explanation-template.md`: `## Further Reading`

Three different names for the same navigational section.

**Analysis:**
Jerry convention (as evidenced by the majority pattern across two templates) uses `## Related`. The tutorial and explanation templates deviate. This inconsistency creates parsing friction for agents navigating document sets and for readers expecting uniform navigation structure across all quadrant documents.

**Recommendation:**
Standardize all four templates to `## Related`. The tutorial's "next steps" concept can be preserved in the link description text.

---

### CC-009: Reference — No Writer Guidance on R-01 or R-07 Compliance

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `reference-template.md` — category structure |
| **Strategy Step** | S-007 check (a) |

**Evidence:**
Category headings use generic `## {Category 1}`, `## {Category 2}` with no guidance on organizing by code structure (R-01) or ensuring all public interfaces are documented (R-07).

**Analysis:**
R-01 (mirrors code structure) and R-07 (complete coverage) are inherently writer-knowledge-dependent — the template cannot enforce them without knowing the codebase. However, the template provides zero guidance directing writers to inventory public interfaces or organize categories by code structure. A writer producing a reference document could use organizational categories ("Common Options," "Advanced Options") that violate R-01, or omit entire subsystems that violate R-07, without any template-level signal.

**Recommendation:**
Add a completeness check comment (see SR-016) and refine the category heading placeholder (see SR-011).

---

## S-013 Inversion Analysis

*Strategy: What would make these templates produce BAD documentation? Identify structural weaknesses, missing placeholder guidance, ambiguous sections, missing elements from quality criteria.*

### IN-001: The Templates Produce Bad Documentation When Writer Agents Have No Quality Criteria Pointer

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | All four templates — top of document |
| **Strategy Step** | Inversion: remove quality enforcement, observe outcome |

**Evidence:**
None of the four templates contains a reference to `diataxis-standards.md`, a comment block directing writer agents to load quality criteria, or any embedded quality checklist.

**Analysis:**
Inversion test: A writer agent receives only the template file. It fills in all placeholders. The resulting document is structurally valid — all sections present, all placeholders replaced. But the agent has applied no quality criteria (Section 1), checked no anti-patterns (Section 2), and enforced no voice guidelines (Section 5). The resulting document is a structurally correct shell that may contain:
- Explanation between tutorial steps (TAP-02) — no template block prevents it
- Imperative instructions in explanation (EAP-01) — no template block prevents it
- Marketing language in reference (RAP-01) — partially warned against but not strongly

The templates are blank-fill forms, not quality-enforcing scaffolds. The inversion makes this visible: removing `diataxis-standards.md` from a writer agent's context produces bad documentation even when the template is fully and correctly filled.

**Recommendation:**
Add a comment block at the top of each template directing writer agents to load and apply `diataxis-standards.md` (see SR-001).

---

### IN-002: Tutorial Templates Produce Bad Documentation When Step Count Exceeds 3

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `tutorial-template.md` — Steps section (lines 18–60) |
| **Strategy Step** | Inversion: scale up content, observe structural failure |

**Evidence:**
The template scaffolds exactly 3 steps. No extension guidance exists.

**Analysis:**
Inversion test: A writer building a tutorial for a 10-step process has two options: (a) artificially compress the tutorial to 3 steps, producing overly dense steps that violate T-02 (visible result per step) by bundling multiple actions, or (b) add 7 more steps without structural guidance, potentially breaking step numbering, losing the `{expected output}` pattern, or introducing inconsistent formatting.

Most real tutorials need 5–10 steps. The template's 3-step scaffold either truncates or leaves writers without a model for extension.

**Recommendation:**
Add an extension comment after Step 3 (see SR-004). Add a note on maximum tutorial length and when to split into multiple tutorials.

---

### IN-003: How-To Templates Produce Bad Documentation When Troubleshooting Is Edge-Case Focused

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `howto-template.md` — Troubleshooting section (lines 55–61) |
| **Strategy Step** | Inversion: substitute rare problems for common ones |

**Evidence:**
Troubleshooting placeholders: `**Problem:** {Common issue}` / `**Solution:** {Fix}`. Two pairs hardcoded.

**Analysis:**
Inversion test: A writer who lists edge-case or theoretical problems ("Problem: Installation fails if you have Python 2 and Python 3 both installed") rather than high-frequency issues satisfies the template while producing low-utility troubleshooting content. The placeholder says "Common issue" but provides no guidance on HOW to determine commonality. Two hardcoded pairs also under-scaffold — guides typically need 3–5 troubleshooting entries.

**Recommendation:**
Add guidance: `{Most frequently encountered issue — if you are unsure, list the error message that most commonly appears in support requests or documentation feedback.}` Add a comment noting that 3–5 entries are typical.

---

### IN-004: Explanation Templates Produce Bad Documentation When Core Concept Sections Use Procedural Headings

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `explanation-template.md` — Core Concept headings (lines 9, 15) |
| **Strategy Step** | Inversion: substitute procedural names for conceptual names |

**Evidence:**
Section heading placeholders: `## {Core Concept 1}`, `## {Core Concept 2}`.

**Analysis:**
Inversion test: A writer produces sections titled `## How to Configure the Pipeline` and `## Step-by-Step Overview`. Both are syntactically valid substitutions for `{Core Concept N}`. But procedural headings invite procedural content — once a writer names a section "How to Configure X," they will fill it with instructions rather than explanatory prose (EAP-01). The heading placeholder is the primary structural entry point for quadrant contamination in the explanation template.

**Recommendation:**
Change placeholder to: `{Conceptual heading — must describe an IDEA or PRINCIPLE, not an action. "Why Event Sourcing" not "How to Use Event Sourcing". "The Trade-Off Between Consistency and Availability" not "Configuring Consistency".}` (see SR-009).

---

### IN-005: Reference Templates Produce Bad Documentation When Overview Becomes Narrative

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `reference-template.md` — Overview section (lines 6–8) |
| **Strategy Step** | Inversion: expand overview into explanatory narrative |

**Evidence:**
Overview placeholder: `{Brief neutral description of the subject. No opinions or marketing.}`

**Analysis:**
Inversion test: "Brief" is undefined. A writer produces a 600-word overview explaining the design decisions behind the system, its historical evolution, and the trade-offs involved. All of this is opinion-free and factual — it satisfies "neutral" and "no marketing" — but it violates RAP-03 (Narrative explanation in reference) by embedding explanation content in a reference document. The inversion is clean: the writer has followed the template instruction ("neutral, no marketing") while producing a document that mixes quadrants.

**Recommendation:**
Add explicit length and content constraints to the Overview placeholder (see SR-010).

---

### IN-006: Tutorial "What You Learned" Permits Non-Observable Skill Statements

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `tutorial-template.md` — lines 64–66 |
| **Strategy Step** | Inversion: substitute comprehension claims for skill statements |

**Evidence:**
Wrap-up bullets: `{Skill acquired 1}`, `{Skill acquired 2}`.

**Analysis:**
Inversion test: A writer produces "You now know how to understand configuration" and "You now know the theory behind pipeline execution" — comprehension claims, not observable skills. These satisfy `{Skill acquired N}` syntactically but violate T-05 (concrete, not abstract). Tutorial wrap-up should list DOABLE skills — things the reader can now perform, not things they now know.

**Recommendation:**
Change placeholder to: `{Observable skill — begins with an action verb. "configure X using Y" not "understand X". Must describe something the reader can now DO.}` (see SR-013).

---

### IN-007: Reference Entry Template Has No Version/Deprecation Slot — Forces Ad Hoc Additions

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `reference-template.md` — entry structure (lines 13–15) |
| **Strategy Step** | Inversion: add version metadata, observe structure break |

**Evidence:**
Entry structure fields: `Type`, `Default`, `Required` — three fields only.

**Analysis:**
Inversion test: A writer needs to document that parameter X was added in v2.0 and parameter Y was deprecated in v3.1. Options: (a) omit the version information (R-02 violation: ambiguous lifecycle state), or (b) add `Since:` and `Deprecated:` fields ad hoc to some entries but not others (R-05 violation: inconsistent entry structure). The template forces a choice between two quality criterion violations.

**Recommendation:**
Add optional fields to the entry structure (see SR-014).

---

## S-002 Devil's Advocate Findings

*Strategy: Challenge (a) voice guideline enforcement, (b) placeholder self-documentation, (c) writer agent compliance test, (d) quadrant mixing prevention.*

### DA-001: Voice Enforcement — Templates Are Structure-Only Artifacts

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | All four templates |
| **Strategy Step** | S-002 challenge (a): voice guideline enforcement |

**Steelman position:** Lean templates preserve writer agency. Over-prescribing voice in a template would make templates feel bureaucratic, increase maintenance burden when voice guidelines evolve, and constrain creative writers who can self-apply guidelines from diataxis-standards.md.

**Counter-argument:** The steelman holds only if writer agents reliably load and apply diataxis-standards.md independently. There is no mechanism ensuring this. Writer agents receiving only a template file will produce structurally valid but voice-non-compliant output. The maintenance burden argument is addressed by using a reference pointer (one comment line) rather than embedding the full guidelines inline.

**Finding:** None of the four templates enforce voice. They enforce anatomy (which sections exist) but not register (how to write within those sections). A writer agent filling any template could produce:
- Tutorial: Passive, hedging prose ("The output may appear as follows")
- How-To: Verbose, indirect instructions ("In order to accomplish the deployment...")
- Reference: Neutral in tone but over-long in description
- Explanation: Flat, reference-like prose with no "why" reasoning

The diataxis-standards.md Section 5 voice guidelines exist and are well-specified. They are disconnected from the templates.

**Recommendation:**
SR-001 (writer agent instruction block) provides the minimal effective fix without embedding guidelines inline.

---

### DA-002: Placeholder Self-Documentation — Three Critical Failures

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Multiple templates |
| **Strategy Step** | S-002 challenge (b): placeholder self-documentation |

**Steelman position:** Simple placeholder names (`{Skill acquired 1}`, `{Core Concept 1}`) are easier to scan and replace. Over-verbose placeholders become noise.

**Counter-argument:** A placeholder that can be replaced with a non-compliant value provides false structure. The three failures below produce actual compliance gaps, not merely style differences:

**Failure 1: `{Core Concept 1}` in explanation-template.md**
A writer reads this as "give the concept a name" and produces `## How to Configure the Pipeline` — a procedural heading that triggers EAP-01. The placeholder does not communicate that the heading must be conceptual, not procedural.

**Failure 2: `{what success looks like}` in howto-template.md**
"Looks like" is subjective and visual. A writer produces "Expected result: The service should be running" — unconfirmable without specifying what "running" means in observable terms (process name, port, HTTP response). The placeholder does not communicate that success must be OBSERVABLE AND SPECIFIC.

**Failure 3: `{Brief instruction.}` in tutorial-template.md**
"Brief" is undefined. Ranges from one action sentence (correct) to one explanatory paragraph (TAP-02 violation). The placeholder permits both without distinction.

**Recommendation:**
See SR-002, SR-006, SR-003 for refined placeholder text addressing each failure.

---

### DA-003: Writer Agent Compliance Test — Structural Gaps Produce Systematic Failures

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | All four templates |
| **Strategy Step** | S-002 challenge (c): writer agent compliance test |

**Steelman position:** Templates cannot and should not enforce every quality criterion — some criteria require human judgment about the specific content domain.

**Counter-argument:** The steelman correctly identifies that R-01 (mirror code structure) and R-07 (complete coverage) cannot be template-enforced. But the structural gap for T-03, T-04, H-04, H-06, E-06, and E-07 is different: these criteria CAN be addressed with placeholder guidance and do not require domain knowledge. The compliance table below shows the difference:

| Template | Enforceable via template, currently unenforced | Inherently writer-knowledge-dependent |
|----------|-----------------------------------------------|--------------------------------------|
| Tutorial | T-03, T-04, T-05, T-08 | None of the unenforced criteria |
| How-To | H-04, H-06 | None of the unenforced criteria |
| Reference | None (R-01, R-07 are domain-dependent) | R-01, R-07 |
| Explanation | E-06, E-07 | None of the unenforced criteria |

A writer agent filling in only the template, without loading diataxis-standards.md, would produce documents that pass structural checks but fail on T-03, T-04, H-04, H-06, E-06, E-07 — all of which ARE addressable through improved placeholders and the SR-001 instruction block.

**Recommendation:**
SR-001 through SR-012 address all enforceable-via-template gaps.

---

### DA-004: Quadrant Mixing Prevention — Asymmetric and Insufficient

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | All four templates |
| **Strategy Step** | S-002 challenge (d): quadrant mixing prevention |

**Steelman position:** Templates cannot police every mixing failure mode. Structural signals (section presence, heading names) provide sufficient orientation; detailed anti-mixing guidance belongs in the standards file, not the template.

**Counter-argument:** The steelman is correct that templates cannot prevent all mixing. But the current templates provide asymmetric protection — some quadrants have partial guards while others have none:

| Template | Mixing guard present | Mixing guard absent |
|----------|---------------------|---------------------|
| Tutorial | None | TAP-02 (explanation between steps), TAP-03 (alternatives) |
| How-To | HAP-01 in Step 1 body only | HAP-01 in Step 3 body; HAP-04 |
| Reference | RAP-01 (partial, overview only) | RAP-02 (numbered steps in entries), RAP-03 |
| Explanation | None | EAP-01 (imperative verbs), EAP-05 (unbounded scope) |

The most significant gap is the explanation template, which provides zero protection against EAP-01 (Major severity). Imperative verbs in explanations are the primary mixing failure mode for this quadrant, and the template has no structural resistance to them.

**Recommendation:**
SR-003, SR-005, SR-007, SR-008 add targeted mixing guards to the highest-risk injection points.

---

## S-010 Self-Refine Recommendations

*All findings from S-007, S-013, S-002 reviewed and consolidated. Recommendations ordered by severity, then by template.*

### Critical Recommendations

**SR-001: Add writer agent instruction block to all four templates (addresses IN-001, CC-007)**

Add at the top of each template, before the title:
```markdown
<!-- Writer Agent Instructions:
     Before filling this template, load and apply:
     skills/diataxis/rules/diataxis-standards.md
     - Section 1: Per-quadrant quality criteria (use as self-review checklist)
     - Section 2: Per-quadrant anti-patterns (check before presenting output)
     - Section 5: Jerry voice guidelines (apply to all prose in this template)
-->
```

**Applies to:** All four templates.
**Effort:** Low — single comment block per file.
**Impact:** Highest-leverage fix. Makes quality criteria, anti-patterns, and voice guidelines visible to any writer agent using the template as their primary input.

---

### Major Recommendations

**SR-002: Tutorial — Refine tagline placeholder to require concrete completion state (addresses CC-003, IN-002 partial)**

Change line 3:
```
> {One-sentence description of what the reader will achieve.}
```
To:
```
> {One-sentence concrete completion state. Format: "You will have [artifact or working system] that [observable behavior]." Example: "You will have a running local deployment that responds to requests on port 8080."}
```

---

**SR-003: Tutorial — Add anti-pattern warnings to step body placeholders (addresses CC-002, DA-004)**

Change step body placeholders from `{Brief instruction.}` to:
```
{Action instruction — imperative verb required. ONE path only. Do NOT explain why. Do NOT offer alternatives. "Why" belongs in an Explanation document; alternatives belong in a How-To Guide.}
```

Apply to all three step bodies (lines 22, 36, 50).

---

**SR-004: Tutorial — Add step count extension guidance (addresses IN-002)**

After Step 3, before `## What You Learned`, add:
```markdown
<!-- Add more steps following the same pattern (### N. {Action}, instruction, code block, expected output).
     Most tutorials need 4–8 numbered steps. If the tutorial exceeds 10 steps, consider splitting
     into two tutorials with a clear handoff point. Each step MUST produce a visible result. -->
```

---

**SR-005: How-To — Restore `No explanation of why.` to Step 3 (addresses CC-004)**

Change Step 3 body placeholder (line 39) from:
```
{Direct instruction.}
```
To:
```
{Direct instruction. No explanation of why.}
```

---

**SR-006: How-To — Refine verification placeholder (addresses DA-002 Failure 2)**

Change lines 53:
```
Expected result: {what success looks like}.
```
To:
```
Expected result: {specific, observable output — e.g., exit code 0, HTTP 200 response, process name visible in `ps aux`, log line "Started successfully"}. Must be confirmable without judgment.
```

---

**SR-007: Explanation — Add scope boundary element (addresses CC-005)**

Add below the tagline (after line 3):
```markdown
> **Scope:** This document explains {specific aspect of topic}. It does not cover {what is explicitly out of scope — name adjacent topics this document deliberately omits}.
```

---

**SR-008: Explanation — Add EAP-01 warning to core concept body placeholders (addresses CC-006, DA-004)**

Change core concept body placeholders from:
```
{Discursive prose exploring the concept. No numbered steps. Make connections to related ideas. Explain *why*, not just *what*.}
```
To:
```
{Discursive prose — continuous paragraphs only, no numbered lists, no bullet lists. Explain WHY, not WHAT or HOW. Do NOT use imperative verbs (run, configure, set, install, open). If you find yourself writing instructions, move that content to a How-To Guide instead.}
```

Apply to both Core Concept body sections.

---

**SR-009: Explanation — Rename `{Core Concept 1}` placeholder to enforce conceptual headings (addresses IN-004, DA-002 Failure 1)**

Change `## {Core Concept 1}` and `## {Core Concept 2}` to:
```markdown
## {Conceptual heading — describes an IDEA or PRINCIPLE, not an action. Good: "Why Event Sourcing", "The Trade-Off Between Consistency and Availability". Bad: "How to Configure X", "Step-by-Step Overview".}
```

---

**SR-010: Reference — Add length and content constraints to Overview placeholder (addresses IN-005)**

Change Overview body placeholder:
```
{Brief neutral description of the subject. No opinions or marketing.}
```
To:
```
{One to three sentences maximum. State what system or component this reference covers — no more. Neutral declarative sentences only. No opinions, design rationale, or historical context — those belong in the companion Explanation document.}
```

---

**SR-011: Reference — Add category naming guidance (addresses CC-009, IN-005 partial)**

Change `## {Category 1}` placeholder comment to:
```markdown
## {Category name — should match a code module, class, or system component. Examples: "Commands", "Configuration Fields", "Environment Variables", "Events". Do NOT use organizational categories like "Common Options" or "Advanced Options".}
```

---

**SR-012: All templates — Standardize cross-reference section name to `## Related` (addresses CC-008)**

- `tutorial-template.md` line 69: Change `## Next Steps` to `## Related`
- `explanation-template.md` line 29: Change `## Further Reading` to `## Related`

The "next steps" concept is preserved in the tutorial link labels, which already read "Apply what you learned to a real task."

---

### Minor Recommendations

**SR-013: Tutorial — Clarify "What You Learned" placeholder to require observable skills (addresses IN-006)**

Change `{Skill acquired 1}` and `{Skill acquired 2}` to:
```
{Observable skill — begins with an action verb. Example: "configure X using Y" not "understand X". Must describe something the reader can now DO.}
```

---

**SR-014: Reference — Add optional version metadata fields to entry structure (addresses IN-007)**

Add as optional fields after `Required`:
```markdown
**Since:** {version this was introduced, or omit if not version-tracked}
**Deprecated:** {version and replacement, or omit if not deprecated}
```

---

**SR-015: How-To — Add step title voice guidance (addresses DA-004 partial)**

Add comment to `### {Action step}` heading placeholders:
```
{Step title — use imperative verb phrase. Example: "Configure the output directory" not "Output Directory Configuration".}
```

---

**SR-016: Reference — Add completeness check comment (addresses CC-009)**

Add after the `## Related` section:
```markdown
<!-- Pre-publish completeness checklist (R-07 compliance):
     [ ] All public commands, parameters, fields, and options documented?
     [ ] Category structure mirrors code/system structure (R-01)?
     [ ] Every entry has a usage example (R-06)?
     Undocumented public interfaces violate R-07. -->
```

---

## Finding Summary Table

| # | Template | Severity | Finding | Location | Recommendation |
|---|----------|----------|---------|----------|----------------|
| 1 | All | Critical | No writer agent instruction block — quality criteria, anti-patterns, and voice guidelines invisible to agents using templates as sole input | All templates, top | SR-001: Add comment block pointing to diataxis-standards.md |
| 2 | Tutorial | Major | T-08 (reliable reproduction) not enforced; TAP-05 (untested steps, Critical severity) structurally enabled | Steps 1–3 | Add T-08 reminder comment in Steps section |
| 3 | Tutorial | Major | T-03 (no unexplained steps) and T-04 (no alternatives) have no structural protection; TAP-02 and TAP-03 unguarded | Step body placeholders lines 22, 36, 50 | SR-003: Add anti-pattern warning to all step body placeholders |
| 4 | Tutorial | Major | "What You Will Achieve" placeholder permits abstract completion states; T-07 intent not enforced | Line 3 | SR-002: Require concrete completion state format |
| 5 | Tutorial | Major | Step count fixed at 3 with no extension guidance; tutorial completeness (T-01) undermined for real content | Lines 18–60 | SR-004: Add step extension comment |
| 6 | How-To | Major | Step 3 body loses `No explanation of why.` enforcement; HAP-01 injection point in final step | Line 39 | SR-005: Restore anti-explanation clause |
| 7 | How-To | Major | Verification placeholder `{what success looks like}` permits unconfirmable success criteria | Line 53 | SR-006: Require specific observable output |
| 8 | Explanation | Major | E-06 (bounded scope) has no template element; EAP-05 (unbounded scope, Major severity) unguarded | No scope section in template | SR-007: Add scope boundary statement |
| 9 | Explanation | Major | E-07 (no imperative instructions) has no template warning; EAP-01 (instructional creep, Major severity) unguarded | Core concept body placeholders | SR-008: Add EAP-01 warning to body placeholders |
| 10 | Explanation | Major | `{Core Concept 1}` placeholder permits procedural section headings; primary structural entry point for EAP-01 | Lines 9, 15 | SR-009: Rename to require conceptual headings |
| 11 | All | Major | Zero voice guidance embedded; writer agents produce structurally correct but voice-non-compliant output | All templates | SR-001 provides pointer; SR-003, SR-008 add inline enforcement |
| 12 | All | Major | Quadrant mixing prevention asymmetric: tutorial and explanation have no mixing guards; how-to partial; reference partial | Various | SR-003, SR-005, SR-008 |
| 13 | Reference | Major | Overview placeholder underdefined — permits 500-word narrative violating R-04 and RAP-03 | Lines 6–8 | SR-010: Add length and content constraint |
| 14 | Tutorial | Minor | "What You Learned" bullets permit non-observable comprehension claims ("understand X") | Lines 64–66 | SR-013: Clarify to require observable action-verb skills |
| 15 | How-To | Minor | Troubleshooting `{Fix}` placeholder does not model imperative direct-address register | Lines 57–60 | SR-015 partial: Add voice note to solution placeholders |
| 16 | How-To | Minor | Step title placeholder `{Action step}` does not enforce imperative verb form | Lines 13, 21, 37 | SR-015: Add step title voice guidance |
| 17 | Reference | Minor | R-01 (mirror code structure) and R-07 (complete coverage) not addressable from template; no guidance given | Category headers and end of doc | SR-011, SR-016: Add category naming and completeness guidance |
| 18 | Reference | Minor | No `Since:` / `Deprecated:` metadata slot; forces ad hoc additions breaking R-05 (consistent formatting) | Entry structure lines 13–15 | SR-014: Add optional version fields |
| 19 | Reference | Minor | Category naming gives no structural mapping guidance; permits organizational categories violating R-01 | Lines 9, 39 | SR-011: Add category naming guidance |
| 20 | All | Minor | Three different cross-reference section names across four templates (`## Next Steps`, `## Related`, `## Further Reading`) | Section headings | SR-012: Standardize to `## Related` |

---

## Quality Assessment

**Total Findings:** 20
**Critical:** 1
**Major:** 12
**Minor:** 7

### Dimension Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 0.65 | Structural completeness strong; quality criteria coverage gaps significant |
| Internal Consistency | 0.70 | How-to Step 1 vs. Step 3 inconsistency; three cross-reference naming schemes |
| Methodological Rigor | 0.68 | Templates enforce anatomy, not quality; no reference to standards file |
| Evidence Quality | 0.85 | Placeholder text is evidence-based; examples present in reference template |
| Actionability | 0.80 | Writers can fill templates; quality is not actionable without standards pointer |
| Traceability | 0.60 | No connection between templates and their governing quality criteria |

**Estimated weighted composite score: 0.71 — REJECTED (below 0.95 threshold)**

Dimension weights from quality-enforcement.md applied: Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10.

Weighted score: (0.65×0.20) + (0.70×0.20) + (0.68×0.20) + (0.85×0.15) + (0.80×0.15) + (0.60×0.10) = 0.130 + 0.140 + 0.136 + 0.128 + 0.120 + 0.060 = **0.714**

### Path to 0.95

The templates require the following changes to reach the 0.95 threshold:

1. **SR-001** (writer agent instruction block) — alone addresses the Traceability gap (0.60 → 0.90) and contributes to Methodological Rigor
2. **SR-003, SR-005, SR-008** (anti-pattern warnings) — address Methodological Rigor gap and Internal Consistency
3. **SR-002, SR-006, SR-009** (placeholder refinement) — address Completeness gap
4. **SR-007, SR-010, SR-011** (structural additions) — address Completeness and Methodological Rigor
5. **SR-012** (standardize section names) — address Internal Consistency gap

With SR-001 through SR-012 applied, estimated revised score: **0.94–0.96** (dependent on implementation quality).

---

*Adversarial Review executed by: adv-executor*
*Constitutional compliance: P-001 (evidence-based findings), P-002 (persisted), P-004 (provenance cited per finding)*
*H-16 note: S-002 executed without prior S-003 per user authority (H-02). Steelman position acknowledged and applied inline.*
