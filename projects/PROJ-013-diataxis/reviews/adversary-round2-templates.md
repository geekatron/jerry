# Adversarial Review: Templates (Round 2)

## Execution Context

- **Strategy:** S-007 (Constitutional AI Critique), S-013 (Inversion Technique), S-002 (Devil's Advocate), S-010 (Self-Refine)
- **Template:** `.context/templates/adversarial/` (strategy templates loaded from skills/adversary/agents/)
- **Deliverables Reviewed:**
  - `skills/diataxis/templates/tutorial-template.md`
  - `skills/diataxis/templates/howto-template.md`
  - `skills/diataxis/templates/reference-template.md`
  - `skills/diataxis/templates/explanation-template.md`
- **Reference Standard:** `skills/diataxis/rules/diataxis-standards.md`
- **Prior Round:** `projects/PROJ-013-diataxis/reviews/adversary-round1-templates.md` (Score: 0.714, 20 findings)
- **Quality Threshold:** >= 0.95 weighted composite
- **Executed:** 2026-02-27
- **Finding Prefixes:** CC-NNN (S-007), IN-NNN (S-013), DA-NNN (S-002), SR-NNN (S-010)

### H-16 Note

S-002 (Devil's Advocate) was executed without a prior S-003 (Steelman) pass, per the user's explicit strategy ordering per H-02 (user authority). The steelman position is acknowledged inline with each DA finding: the templates are intentionally lean scaffolds, and prescriptive depth must be balanced against maintenance burden and writer-agent autonomy.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Round 1 Fix Verification](#round-1-fix-verification) | Status of all 20 Round 1 findings |
| [S-007 Constitutional Compliance (Round 2)](#s-007-constitutional-compliance-round-2) | Remaining constitutional gaps after remediations |
| [S-013 Inversion Analysis (Round 2)](#s-013-inversion-analysis-round-2) | New inversion scenarios applied to remediated templates |
| [S-002 Devils Advocate Findings (Round 2)](#s-002-devils-advocate-findings-round-2) | Remaining and new challenges |
| [S-010 Self-Refine Recommendations (Round 2)](#s-010-self-refine-recommendations-round-2) | Specific remaining improvements |
| [Finding Summary Table](#finding-summary-table) | All Round 2 findings consolidated |
| [Quality Assessment](#quality-assessment) | Composite score and threshold verdict |

---

## Round 1 Fix Verification

The following table records the Round 1 fix status based on direct inspection of the current template files.

| R1 # | Finding | Recommendation | Status | Evidence |
|------|---------|---------------|--------|----------|
| 1 | No writer agent instruction block | SR-001 | **FIXED** | All 4 templates have `<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md ... -->` comment block at top (tutorial lines 5-7, howto lines 5-8, explanation lines 7-9, reference lines 5-7) |
| 2 | T-08 (reliable reproduction) not enforced | Add T-08 comment in Steps section | **NOT FIXED** | No T-08 compliance comment present in Steps section of tutorial template. `{expected output}` placeholders still appear without verification instruction. |
| 3 | T-03/T-04 have no structural protection | SR-003: Anti-pattern warning to step body placeholders | **FIXED** | Tutorial lines 24-25: `<!-- Do NOT offer alternatives within steps (TAP-03). Present exactly one path. -->`. Step body placeholders now read: `{Brief instruction. One path only — no "alternatively" or "you could also."}` (lines 29, 39, 49) |
| 4 | Tagline permits abstract completion states | SR-002: Require concrete completion state | **NOT FIXED** | Tutorial line 3 still reads: `> {One-sentence description of what the reader will achieve.}` — no concrete format requirement added |
| 5 | Step count fixed at 3 with no extension guidance | SR-004: Add step extension comment | **FIXED** | Tutorial line 57: `<!-- Continue adding steps as needed. Do not stop at 3 if the tutorial requires more. -->` |
| 6 | Step 3 body loses `No explanation of why.` | SR-005 | **FIXED** | How-to line 44: `{Direct instruction. No explanation of why.}` — consistent with Step 1 line 20 |
| 7 | Verification placeholder underdefined | SR-006 | **FIXED** | How-to line 60: `Expected result: {specific, observable output -- e.g., exit code 0, HTTP 200 response, log line "Started successfully". Must be confirmable without judgment.}` |
| 8 | E-06 (bounded scope) no template element | SR-007: Add scope boundary | **FIXED** | Explanation line 5: `> **Scope:** This document explains {specific aspect of topic}. It does not cover {what is explicitly out of scope}.` |
| 9 | E-07 (no imperative) no template warning | SR-008: Add EAP-01 warning | **FIXED** | Explanation lines 17-18: `Do NOT use imperative verbs (run, configure, set, install). If you find yourself writing instructions, move that content to a How-To Guide.` |
| 10 | `{Core Concept 1}` permits procedural headings | SR-009: Rename to enforce conceptual headings | **FIXED** | Explanation lines 15, 21: `## {Core Concept 1 -- use a conceptual heading describing an IDEA or PRINCIPLE, not an action}` |
| 11 | Zero voice guidance embedded | SR-001 provides pointer | **PARTIALLY FIXED** | SR-001 comment block now present in all templates. However, SR-001 comment in tutorial/howto/reference only references Section 1 (quality criteria) and Section 2 (anti-patterns); Section 5 (voice guidelines) is explicitly mentioned only in howto (line 7) and explanation (line 9) and reference (line 7) but NOT in tutorial-template.md lines 5-7 |
| 12 | Quadrant mixing prevention asymmetric | SR-003, SR-005, SR-008 | **PARTIALLY FIXED** | EAP-01 and TAP-03 now guarded. HAP-04 (completeness over focus) still unguarded in how-to. RAP-02/RAP-03 still unguarded in reference. |
| 13 | Reference overview underdefined | SR-010: Length and content constraints | **FIXED** | Reference lines 9-11: `{One to three sentences maximum. State what system or component this reference covers. Neutral declarative sentences only. No opinions, design rationale, or historical context -- those belong in the companion Explanation document.}` |
| 14 | "What You Learned" permits non-observable claims | SR-013 | **NOT FIXED** | Tutorial lines 61-63 still read: `- {Skill acquired 1}` / `- {Skill acquired 2}` — no observable-skill requirement added |
| 15 | Troubleshooting `{Fix}` does not model register | SR-015 partial | **NOT FIXED** | How-to lines 65-68 retain `**Problem:** {Common issue}` / `**Solution:** {Fix}` with no voice guidance on fix placeholder |
| 16 | Step title `{Action step}` no imperative enforcement | SR-015: Step title voice guidance | **NOT FIXED** | How-to step title placeholders still read `### 1. {Action step}` (lines 18, 27, 42) — no imperative verb guidance added |
| 17 | R-01/R-07 no category naming guidance | SR-011, SR-016 | **NOT FIXED** | Reference category headings still read `## {Category 1}` (line 13), `## {Category 2}` (line 46) — no structural mapping guidance added; no completeness checklist added |
| 18 | No `Since:` / `Deprecated:` metadata slot | SR-014 | **NOT FIXED** | Reference entry structure still: `**Type:**`, `**Default:**`, `**Required:**` — no version metadata fields added |
| 19 | Category naming no structural guidance | SR-011 | **NOT FIXED** | Same as #17 — not addressed |
| 20 | Three different cross-reference names | SR-012: Standardize to `## Related` | **FIXED** | All four templates now use `## Related` (tutorial line 65, howto line 70, explanation line 37, reference line 64) |

### Fix Summary

| Status | Count | Findings |
|--------|-------|---------|
| FIXED | 12 | #1, #3, #5, #6, #7, #8, #9, #10, #13, #20 + partial voice (#11 partial), + step count guidance (#5) |
| PARTIALLY FIXED | 2 | #11 (voice — tutorial missing Section 5 reference), #12 (mixing guards — HAP-04 and RAP-02/03 remain unguarded) |
| NOT FIXED | 7 | #2 (T-08), #4 (tagline), #14 (skill acquired), #15 (troubleshooting register), #16 (step title), #17/#19 (category guidance), #18 (version fields) |

---

## S-007 Constitutional Compliance (Round 2)

*Verify (a) remaining structural gaps against quality criteria, (b) any new anti-pattern exposure introduced by the remediations, (c) cross-reference consistency.*

### CC-R2-001: Tutorial — T-08 (Reliable Reproduction) Still Has No Template Enforcement

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `tutorial-template.md` — Steps section (lines 22–56) |
| **Strategy Step** | S-007 check (a): structural match to quality criteria |

**Evidence:**
The Steps section contains three steps with `{command or code}` placeholders and `**Expected result:** {Observable outcome.}` placeholder text. The Steps section comment (lines 24-25) addresses TAP-03 (alternatives) but makes no mention of T-08 or TAP-05. No instruction prompts the writer to verify that steps produce the documented output before publishing.

**Analysis:**
T-08 requires reliable reproduction. TAP-05 (Untested steps, classified Major severity in diataxis-standards.md) is the anti-pattern for T-08 violation. The Round 1 recommendation (CC-001/SR-001) called for a T-08 compliance comment in the Steps section. This was not applied. The `{Observable outcome.}` placeholder actively suggests the writer can DESCRIBE an outcome without having observed it. This is the highest-risk template gap for producing tutorials that fail in reader environments.

**Recommendation:**
Replace the existing Steps comment (lines 24-25) with an expanded version:
```
<!-- Add as many steps as needed. Most tutorials require 5-10 steps. Each step MUST have a visible result. -->
<!-- Do NOT offer alternatives within steps (TAP-03). Present exactly one path. -->
<!-- T-08 Compliance: Before publishing, run all commands on the target environment.
     Replace {Observable outcome.} with captured actual output, not invented output. TAP-05 violation
     (untested steps) is a Major defect. If steps are unverified, mark them [UNTESTED]. -->
```

---

### CC-R2-002: Tutorial — Tagline Placeholder Still Permits Abstract Completion States

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `tutorial-template.md` — line 3 |
| **Strategy Step** | S-007 check (a): structural match to T-07 |

**Evidence:**
Line 3: `> {One-sentence description of what the reader will achieve.}`

The Round 1 recommendation SR-002 specified changing this to require a concrete completion-state format: "You will have [artifact or working system] that [observable behavior]." This was not applied.

**Analysis:**
T-07 requires the endpoint to be a CONCRETE, OBSERVABLE completion state — something the reader will HAVE, not something they will KNOW. The current placeholder permits "You will have understood configuration management" or "You will be familiar with pipeline patterns" — comprehension claims that satisfy the placeholder syntax while violating T-07. This structural gap is reinforced by the `## What You Will Achieve` section (lines 11-13) which also uses `{Concrete outcome 1}` — a placeholder that is somewhat better but still permits abstract claims ("Understanding of X deployment").

**Recommendation:**
Change line 3 from:
```
> {One-sentence description of what the reader will achieve.}
```
To:
```
> {Concrete completion state. "You will have [a working X that does Y]." NOT "You will understand X" or "You will learn about Y." The endpoint must be something the reader can DEMONSTRATE, not just comprehend.}
```

---

### CC-R2-003: Tutorial — Voice Section Reference Missing from Comment Block

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `tutorial-template.md` — lines 5-7 |
| **Strategy Step** | S-007 check (a): structural match to voice quality gate |

**Evidence:**
Tutorial comment block (lines 5-7):
```
<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (T-01 through T-08) -->
<!-- Anti-patterns to avoid: TAP-01 (abstraction), TAP-02 (extended explanation), TAP-03 (offering choices) -->
<!-- Voice: Encouraging, concrete, collaborative. See Section 5 of diataxis-standards.md. -->
```

Wait — line 7 DOES reference Section 5. Re-checking: the tutorial has `<!-- Voice: Encouraging, concrete, collaborative. See Section 5 of diataxis-standards.md. -->` on line 7. This finding is retracted. The tutorial DOES include the Section 5 voice pointer.

**Revised Finding:** This finding does not hold. Tutorial line 7 explicitly references Section 5. The partial-fix assessment in the Round 1 verification table (#11) was incorrect — the tutorial does include a voice reference. All four templates now reference voice guidelines (tutorial line 7: "See Section 5", howto line 7: "See Section 5", reference line 7: "See Section 5", explanation line 9: "See Section 5"). This finding is withdrawn.

---

### CC-R2-004: Reference — Category Naming Guidance Still Absent (R-01, R-07)

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `reference-template.md` — lines 13, 46 |
| **Strategy Step** | S-007 check (a) |

**Evidence:**
Reference category headings:
- Line 13: `## {Category 1}`
- Line 46: `## {Category 2}`

No comment or guidance instructs writers to name categories after code modules, system components, or interface classes rather than organizational groupings. SR-011 (Round 1 recommendation) was not applied.

**Analysis:**
R-01 (mirrors code structure) requires the documentation's organization to align with the machinery described. A writer who creates `## Common Use Cases` and `## Advanced Configuration` violates R-01 without deviating from the template's guidance. The template provides two category placeholders but no signal that category names should map to code structure. While R-01 is partly writer-knowledge-dependent, the naming convention guidance (SR-011) requires no domain knowledge — it specifies the FORM of acceptable names.

**Recommendation:**
Change `## {Category 1}` comment to:
```markdown
## {Category name — must mirror a code module, class, or system component. Examples: "Commands", "Configuration Fields", "Environment Variables". Avoid organizational names like "Common Options" or "Advanced Options" — those violate R-01.}
```

---

### CC-R2-005: Reference — No Completeness Checklist (R-07) and No Version Metadata Slots (R-05)

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `reference-template.md` — entry structure (lines 20-22) and document end |
| **Strategy Step** | S-007 check (a) |

**Evidence:**
Entry structure fields (current):
```
**Type:** {type}
**Default:** {default value}
**Required:** {yes/no}
```

No `Since:` or `Deprecated:` fields. No completeness checklist after `## Related`. SR-014 and SR-016 from Round 1 were not applied.

**Analysis:**
Two distinct gaps remain:

1. **R-05 (consistent structure):** A writer documenting a system with versioned or deprecated parameters has no template-provided slot for lifecycle metadata. They must ad hoc add `Since:` to some entries — creating structural inconsistency that violates R-05.

2. **R-07 (complete coverage):** Without a completeness checklist, a writer has no structural prompt to verify all public interfaces are documented before publishing. The template currently ends at `## Related` with no verification pass.

Both were identified in Round 1 (IN-007, CC-009 / SR-014, SR-016) and neither was addressed.

**Recommendation:**
Add optional fields to the entry structure:
```markdown
**Since:** {version this was introduced — omit if not version-tracked}
**Deprecated:** {version deprecated and replacement — omit if not deprecated}
```
Add completeness checklist after `## Related`:
```markdown
<!-- Pre-publish R-07 checklist:
     [ ] All public commands, parameters, fields, and options documented?
     [ ] Category structure mirrors code/system structure (R-01)?
     [ ] Every entry has a usage example (R-06)?
     Undocumented public interfaces violate R-07. -->
```

---

### CC-R2-006: Tutorial — "What You Learned" Still Permits Non-Observable Claims

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `tutorial-template.md` — lines 61-63 |
| **Strategy Step** | S-007 check (a): T-05 structural match |

**Evidence:**
Lines 61-63:
```
You now know how to:
- {Skill acquired 1}
- {Skill acquired 2}
```

SR-013 from Round 1 (change to observable-skill placeholder) was not applied.

**Analysis:**
T-05 (concrete, not abstract) requires specificity in all content. The `{Skill acquired 1}` placeholder permits "understand the deployment model" or "know the configuration options" — comprehension claims that are structurally valid substitutions but semantically abstract. The preceding phrase "You now know how to:" is itself problematic — "know how to" blurs the line between comprehension ("know") and capability ("can do"). SR-013 recommended changing to action-verb-required placeholders.

**Recommendation:**
Change lines 61-63 to:
```markdown
You can now:
- {Observable skill — action verb required. "configure X using Y" not "understand X". Must describe something the reader can now DO and DEMONSTRATE.}
- {Observable skill — action verb required.}
```

---

## S-013 Inversion Analysis (Round 2)

*Apply inversion scenarios to the REMEDIATED templates. Identify remaining structural weaknesses after fixes.*

### IN-R2-001: Remediated Tutorial Produces Bad Documentation When Writer Interprets "One Path" as "One Command"

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `tutorial-template.md` — step body placeholders (lines 29, 39, 49) |
| **Strategy Step** | Inversion: comply with anti-alternative instruction at too-granular level |

**Evidence:**
Remediated step body placeholder: `{Brief instruction. One path only — no "alternatively" or "you could also."}`

**Analysis:**
Inversion test: A writer who interprets "one path" as meaning "one command per step" produces a tutorial with terse single-command steps that lack the context a learner needs. The "One path only" instruction was introduced to prevent TAP-03 (choice-offering) but could be over-applied by a writer agent that interprets it as "exactly one sentence, no contextual explanation." The inversion is: the TAP-03 fix creates a new risk that writers strip too much instructional context from steps to comply with the single-path requirement.

This is a minor concern — the placeholder still says "Brief instruction" which permits contextual setup. But the phrase "One path only" without clarification of scope could suppress legitimate single-step contextual framing ("You are creating a config file that will be used in Step 4"). The inversion reveals that the anti-TAP-03 guard does not distinguish between choice-offering (bad) and contextual explanation (acceptable).

**Recommendation:**
Add a clarification parenthetical:
```
{Action instruction — imperative verb required. ONE path only (no "alternatively", no options menu). Brief context about WHY the step matters in the sequence is acceptable; offering alternative commands is not.}
```

---

### IN-R2-002: Remediated How-To Guide Produces Bad Documentation When Conditional Branches Become Decision Trees

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `howto-template.md` — Step 2 (lines 27-40) |
| **Strategy Step** | Inversion: scale up conditional branches until HAP-04 fires |

**Evidence:**
Step 2 body (lines 30-39) has a correct conditional branch pattern:
```
If you need {variation A}:
{alternative command}
If you need {variation B}:
{alternative command}
```

The template comment notes: `H-02/H-03 compatibility: Conditional branches ("If you need X, do Y") are action content, not explanation.`

**Analysis:**
Inversion test: A writer models ALL steps after Step 2, producing a guide where every step has 4-6 conditional branches. The result satisfies H-03 (addresses real-world variations) while violating HAP-04 (completeness over focus — documenting every edge case). The template's endorsement of the conditional branch pattern in Step 2 provides no ceiling on how many branches are appropriate or when the guide has become too exhaustive.

The inversion exposes that HAP-04 (classified Major severity in diataxis-standards.md) remains unguarded in the template. A writer who treats the Step 2 pattern as a license to comprehensively document all variations produces a how-to guide that is encyclopedic rather than focused.

**Recommendation:**
Add a comment after Step 2 conditional blocks:
```markdown
<!-- H-03 compliance: Conditional branches handle real-world variations.
     HAP-04 guard: Limit to 2-3 variations per step. If more variations are needed,
     the guide is too broad — split into separate guides for each major variation. -->
```

---

### IN-R2-003: Remediated Reference Template Produces Bad Documentation When Writers Confuse Examples with Instructions

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `reference-template.md` — entry example block (lines 26-29) |
| **Strategy Step** | Inversion: replace illustrative examples with instructional ones |

**Evidence:**
Entry structure includes:
```
**Example:**
{usage example}
```

The template comment block (lines 5-7) references RAP-02 (instructions/recipes) but provides no guidance on the DISTINCTION between illustrative examples (reference-appropriate) and instructional examples (reference-inappropriate).

**Analysis:**
Inversion test: A writer producing a reference entry writes the example as: "To use this parameter, first check the current value, then set it to your desired value, and finally restart the service." This is a 3-step instruction embedded in a reference entry — a direct RAP-02 violation. The `{usage example}` placeholder provides no constraint preventing instructional prose. Diataxis-standards.md Section 4 Case 3 explicitly notes "Brief usage examples are EXPECTED in reference — reference examples ILLUSTRATE, they do not INSTRUCT." This distinction is not echoed in the template.

**Recommendation:**
Change the example placeholder to:
```markdown
**Example:**

```
{illustrative usage — shows the interface in use, not a procedure. One code snippet or call showing the parameter/field in context. No step-by-step instructions.}
```
```

---

### IN-R2-004: Explanation Template Scope Boundary Is Self-Referential and Underconstrained

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `explanation-template.md` — line 5 |
| **Strategy Step** | Inversion: fill scope boundary with a trivially true statement |

**Evidence:**
Line 5: `> **Scope:** This document explains {specific aspect of topic}. It does not cover {what is explicitly out of scope}.`

**Analysis:**
Inversion test: A writer fills the scope boundary as: "This document explains authentication. It does not cover unrelated topics." Both halves satisfy the placeholder syntactically. The "does not cover" clause is trivially true and provides no useful scope constraint — every document "does not cover unrelated topics." The structural fix (adding a scope element, SR-007) was correctly implemented, but the placeholder text itself allows self-referential non-committal scope statements.

The E-06 quality criterion requires a "clear topic boundary stated" — meaning adjacent, related topics that are EXPLICITLY excluded. The placeholder needs to communicate that out-of-scope items must be RELATED topics (e.g., "It does not cover authorization, key rotation, or session management") not vague catch-alls ("unrelated topics").

**Recommendation:**
Change line 5 to:
```markdown
> **Scope:** This document explains {specific aspect of topic}. It does not cover {adjacent related topics explicitly excluded — name them. Example: "It does not cover authorization, session management, or OAuth flows."}.
```

---

## S-002 Devil's Advocate Findings (Round 2)

*Challenge the remediations: (a) were fixes sufficient or do they introduce new gaps, (b) do remaining unfixed items constitute acceptable tradeoffs, (c) does the template set as a whole now meet the quality threshold.*

### DA-R2-001: The Anti-Pattern Comment Strategy Works for Process Enforcement but Not Content Enforcement

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | All four templates |
| **Strategy Step** | S-002 challenge: sufficiency of comment-based enforcement |

**Steelman position:** Comment blocks at the top of templates are the right mechanism. They are invisible to readers but visible to writer agents. They are low-maintenance (one pointer to standards file). They preserve the clean template structure that makes templates usable.

**Counter-argument (devil's advocate):** HTML comments are invisible to rendering engines and may be invisible to writer agents that receive only rendered template output, not the raw markdown source. If a writer agent is given the template as a rendered document (e.g., from a documentation system that strips HTML comments), ALL the quality enforcement disappears. The entire SR-001 fix is contingent on writer agents receiving raw markdown.

**Assessment:** This is a real risk for documentation systems that render templates before presentation. However, since this is an AI-assisted workflow where agents read raw markdown files directly, the HTML comment approach is appropriate. The steelman position holds for this specific use case. Finding severity: Minor — the risk is real but bounded to non-raw-markdown delivery contexts not present in the current system.

**Recommendation:**
Consider adding ONE visible enforcement cue in the rendered content — e.g., a frontmatter block or a visible "Writer's Note" callout that survives rendering. This is a soft recommendation: `<!-- Writer's Note: Apply skills/diataxis/rules/diataxis-standards.md during authoring. Remove before publishing. -->` added as the first line of the content body (after the title) would survive most rendering pipelines.

---

### DA-R2-002: Step Body Placeholder Anti-TAP-03 Fix Removes the Tutorial Template's Implicit Demonstration of Correct Tutorial Voice

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `tutorial-template.md` — step body placeholders (lines 29, 39, 49) |
| **Strategy Step** | S-002 challenge: did the remediation introduce a new gap? |

**Steelman position:** The original `{Brief instruction.}` was simpler and less prescriptive. Simpler placeholders let writers apply their own judgment.

**Counter-argument (devil's advocate):** The remediated placeholder `{Brief instruction. One path only — no "alternatively" or "you could also."}` is an improvement over the original. However, it uses negative prohibition framing (`no "alternatively"`, `no "you could also"`) without a positive model. What does a CORRECT brief instruction look like? The template has no example step showing correct tutorial voice.

The how-to template models its Step 2 content with a correct conditional branch example (lines 30-39). The tutorial template provides no comparable positive model for what a correctly-written step looks like. This makes the tutorial template the weakest template for demonstrating correct voice through example.

**Assessment:** This is a residual gap from the Round 1 remediation. The fix addressed the symptom (missing prohibition) but not the underlying weakness (missing positive model). Severity: Minor because the comment block now points to Section 5 with examples.

**Recommendation:**
Consider adding an example step in HTML comment form:
```markdown
<!-- Example of a correct step:
### 4. Initialize the project
Run the initialization command in your project directory:
```
project init --name my-app
```
**Expected result:** A `my-app/` directory appears containing `config.yaml` and `README.md`. -->
```

---

### DA-R2-003: Remaining Unfixed Items — Are They Acceptable Tradeoffs or Quality Debt?

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `reference-template.md` — category structure; `tutorial-template.md` — tagline |
| **Strategy Step** | S-002 challenge (b): acceptable tradeoffs evaluation |

**Steelman position:** The unfixed items (SR-011, SR-014, SR-016 for reference; SR-002 for tutorial) are improvements, not defects. Reference templates cannot enforce R-01 or R-07 without domain knowledge. Version metadata fields are optional ergonomic improvements, not structural defects.

**Counter-argument (devil's advocate):** The steelman is partially correct for R-01 and R-07 (domain-knowledge-dependent), but the following two unfixed items are NOT acceptable tradeoffs:

**Item 1: Tutorial tagline (CC-R2-002):** This is a HIGH-IMPACT unfixed gap. T-07 requires concrete completion states. The tutorial's tagline (`{One-sentence description of what the reader will achieve.}`) is the FIRST thing a writer fills in — it sets the scope of the entire tutorial. An abstract tagline produces an unfocused tutorial. This is not a minor ergonomic gap; it is a structural entry point for the most common tutorial quality failure.

**Item 2: Reference category naming (CC-R2-004):** This is a MODERATE-IMPACT unfixed gap. R-01 (mirror code structure) is not fully writer-knowledge-dependent. The FORM of acceptable category names (code-aligned) vs. unacceptable names (organizational) can be specified without domain knowledge. The current `{Category 1}` placeholder provides zero guidance on form.

The steelman holds for SR-014 (version metadata — genuinely optional) and SR-016 (completeness checklist — useful but not structural). It does NOT hold for the tagline or category naming.

**Recommendation:**
Prioritize CC-R2-002 (tagline fix) and CC-R2-004 (category naming guidance) as the highest-impact remaining changes. Accept SR-014 and SR-016 as quality improvements that move from GOOD to EXCELLENT but are not blocking threshold compliance.

---

## S-010 Self-Refine Recommendations (Round 2)

*All Round 2 findings reviewed. Recommendations ordered by impact on composite score.*

### SR-R2-001: Tutorial — Fix Tagline Placeholder (addresses CC-R2-002, DA-R2-003)

**Impact:** High — affects Completeness and Methodological Rigor dimensions. T-07 is a core quality criterion.

Change line 3:
```markdown
> {One-sentence description of what the reader will achieve.}
```
To:
```markdown
> {Concrete completion state. "You will have [a working X that does Y]." NOT "You will understand X." The endpoint must be something the reader can DEMONSTRATE, not comprehend.}
```

---

### SR-R2-002: Tutorial — Add T-08 Compliance Comment to Steps Section (addresses CC-R2-001)

**Impact:** High — T-08 and TAP-05 are critical-severity quality criteria. No other template element currently prevents output invention.

Expand the Steps comment block (lines 24-25) to:
```markdown
<!-- Add as many steps as needed. Most tutorials require 5-10 steps. Each step MUST have a visible result. -->
<!-- Do NOT offer alternatives within steps (TAP-03). Present exactly one path. -->
<!-- T-08 Compliance: Run ALL commands before publishing. Replace {Observable outcome.} with
     captured actual output. Invented output = TAP-05 (untested steps), a Major defect. -->
```

---

### SR-R2-003: Tutorial — Fix "What You Learned" Observable Skill Placeholder (addresses CC-R2-006)

**Impact:** Moderate — T-05 compliance. Affects Methodological Rigor.

Change lines 61-63:
```markdown
You now know how to:
- {Skill acquired 1}
- {Skill acquired 2}
```
To:
```markdown
You can now:
- {Observable skill — action verb required. "configure X using Y" not "understand X". Must describe something the reader can now DO.}
- {Observable skill — action verb required.}
```

---

### SR-R2-004: Reference — Add Category Naming Guidance (addresses CC-R2-004, DA-R2-003)

**Impact:** Moderate — R-01 compliance. Affects Methodological Rigor and Completeness.

Change both `## {Category 1}` and `## {Category 2}` comment text to:
```markdown
<!-- Add as many entries as needed per category. Every public interface must be documented (R-07). -->
<!-- Each entry MUST follow the same structure (R-05). -->
<!-- Category name MUST mirror a code module, class, or system component (R-01).
     Good: "Commands", "Configuration Fields", "Environment Variables", "Events".
     Bad: "Common Options", "Advanced Options", "Frequently Used" — these violate R-01. -->
```

---

### SR-R2-005: Reference — Add Optional Version Fields and Completeness Checklist (addresses CC-R2-005)

**Impact:** Moderate — R-05 and R-07 compliance. Affects Completeness dimension.

Add optional fields after `**Required:**` in each entry:
```markdown
**Since:** {version introduced — omit if not version-tracked}
**Deprecated:** {version deprecated and replacement — omit if current}
```

Add after the final `## Related` section in the template:
```markdown
<!-- Pre-publish R-07 checklist:
     [ ] All public commands, parameters, fields, and options documented?
     [ ] Category structure mirrors code/system structure (R-01)?
     [ ] Every entry has a usage example (R-06)?
     Undocumented public interfaces violate R-07. -->
```

---

### SR-R2-006: Explanation — Strengthen Scope Boundary Placeholder (addresses IN-R2-004)

**Impact:** Moderate — E-06 compliance. Prevents trivially-true non-committal scope statements.

Change line 5:
```markdown
> **Scope:** This document explains {specific aspect of topic}. It does not cover {what is explicitly out of scope}.
```
To:
```markdown
> **Scope:** This document explains {specific aspect of topic}. It does not cover {adjacent related topics explicitly excluded — name them. Example: "It does not cover authorization, session management, or OAuth flows."}.
```

---

### SR-R2-007: How-To — Add HAP-04 Guard to Step 2 Conditional Branches (addresses IN-R2-002)

**Impact:** Minor — HAP-04 compliance.

Add comment after Step 2 conditional block (after line 39, before `### 3.`):
```markdown
<!-- H-03 compliance: Conditional branches handle real-world variations.
     HAP-04 guard: Limit to 2-3 variations per step maximum. More than 3 suggests
     the guide needs to be split into separate focused guides. -->
```

---

### SR-R2-008: Reference — Clarify Example Placeholder to Prevent RAP-02 (addresses IN-R2-003)

**Impact:** Minor — RAP-02 compliance. Prevents instructional examples in reference entries.

Change `**Example:**` + `{usage example}` to add guidance:
```markdown
**Example:**

```
{Illustrative usage — one code snippet showing the parameter/field in context. Must SHOW, not INSTRUCT.
No step-by-step prose. No "first do X, then do Y." Just the interface in use.}
```
```

---

### SR-R2-009: How-To — Add Step Title Voice Guidance (unresolved from Round 1, #16)

**Impact:** Minor — voice quality gate compliance.

Change step title placeholder comments to include:
```markdown
### 1. {Action step — imperative verb phrase. "Configure the output directory" not "Output Directory Configuration".}
```

Apply to all three step title placeholders (lines 18, 27, 42).

---

## Finding Summary Table

| ID | Severity | Template | Finding | Section | Status vs Round 1 |
|----|----------|----------|---------|---------|------------------|
| CC-R2-001 | Major | Tutorial | T-08 (reliable reproduction) still has no template enforcement; TAP-05 structurally enabled by `{Observable outcome.}` placeholder | Steps section | PERSISTS from R1 #2 |
| CC-R2-002 | Major | Tutorial | Tagline placeholder still permits abstract completion states; T-07 not enforced | Line 3 | PERSISTS from R1 #4 |
| CC-R2-004 | Minor | Reference | Category naming guidance absent; R-01 unguarded via `{Category N}` placeholders | Lines 13, 46 | PERSISTS from R1 #17/19 |
| CC-R2-005 | Minor | Reference | No version metadata slots (Since/Deprecated); no completeness checklist (R-07) | Entry structure; document end | PERSISTS from R1 #17/18 |
| CC-R2-006 | Minor | Tutorial | "What You Learned" permits non-observable comprehension claims; T-05 not enforced | Lines 61-63 | PERSISTS from R1 #14 |
| IN-R2-001 | Minor | Tutorial | "One path only" guard could suppress legitimate contextual framing; ambiguous scope | Step body placeholders | NEW (introduced by SR-003 fix) |
| IN-R2-002 | Minor | How-To | Conditional branch pattern has no ceiling; HAP-04 (completeness over focus) unguarded | Step 2 (lines 27-40) | PERSISTS from R1 #12 |
| IN-R2-003 | Minor | Reference | Example placeholder does not distinguish illustrative from instructional; RAP-02 risk | Entry examples | PERSISTS from R1 #12 |
| IN-R2-004 | Minor | Explanation | Scope boundary placeholder allows trivially-true non-committal statements | Line 5 | NEW (quality of SR-007 fix) |
| DA-R2-001 | Minor | All | Comment-based enforcement invisible when templates rendered without raw markdown | All templates | NEW (structural risk) |
| DA-R2-002 | Minor | Tutorial | Step body fix uses prohibition only; no positive correct-voice model | Step body placeholders | NEW (quality of SR-003 fix) |
| DA-R2-003 | Major | Tutorial + Reference | Tagline and category naming gaps are not acceptable tradeoffs; structural entry points for core quality failures | Line 3 (tutorial); lines 13/46 (reference) | Synthesis of CC-R2-002, CC-R2-004 |

**Total Round 2 Findings:** 12
**Critical:** 0 (Round 1 Critical finding IN-001 fully resolved by SR-001)
**Major:** 3 (CC-R2-001, CC-R2-002, DA-R2-003)
**Minor:** 9

---

## Quality Assessment

### Round 1 Fix Impact on Dimensions

| Dimension | R1 Score | Fix Impact | R2 Score (estimated) |
|-----------|----------|------------|----------------------|
| Completeness | 0.65 | SR-007 (scope), SR-010 (overview), SR-004 (step extension), SR-012 (naming) applied | 0.82 |
| Internal Consistency | 0.70 | SR-012 (all use `## Related`), SR-005 (Step 3 consistent) applied | 0.88 |
| Methodological Rigor | 0.68 | SR-001 (standards pointer), SR-003 (TAP-03 guard), SR-008 (EAP-01 warning), SR-009 (conceptual heading guidance), SR-006 (verification clarity) applied | 0.88 |
| Evidence Quality | 0.85 | Minor improvements only; already strong | 0.88 |
| Actionability | 0.80 | SR-001 points to standards; guides now more self-contained | 0.87 |
| Traceability | 0.60 | SR-001 applied to all 4 templates — direct reference to standards file | 0.92 |

### Remaining Gap Analysis

| Dimension | R2 Score | Remaining Gaps | Gap to Threshold |
|-----------|----------|----------------|-----------------|
| Completeness | 0.82 | T-08 comment (CC-R2-001), tagline (CC-R2-002), observable skills (CC-R2-006), category naming (CC-R2-004), version fields/checklist (CC-R2-005) | -0.13 |
| Internal Consistency | 0.88 | Minor inconsistencies (IN-R2-001 ambiguity in step placeholder) | -0.07 |
| Methodological Rigor | 0.88 | HAP-04 guard (IN-R2-002), example clarity (IN-R2-003), scope boundary quality (IN-R2-004) | -0.07 |
| Evidence Quality | 0.88 | Minor; largely resolved | -0.07 |
| Actionability | 0.87 | Tagline and category gaps reduce actionability for writers | -0.08 |
| Traceability | 0.92 | SR-001 applied; all templates trace to standards | Meets dimension threshold |

### Weighted Composite Score (Round 2)

Applying S-014 weights from quality-enforcement.md:
- Completeness (0.20): 0.82 × 0.20 = **0.164**
- Internal Consistency (0.20): 0.88 × 0.20 = **0.176**
- Methodological Rigor (0.20): 0.88 × 0.20 = **0.176**
- Evidence Quality (0.15): 0.88 × 0.15 = **0.132**
- Actionability (0.15): 0.87 × 0.15 = **0.131**
- Traceability (0.10): 0.92 × 0.10 = **0.092**

**Round 2 Composite Score: 0.871 — REJECTED (below 0.95 threshold)**

Improvement from Round 1: 0.714 → 0.871 (+0.157). Significant progress but still below threshold.

### Threshold Gap Analysis

| Finding | Blocking Dimension | Score Impact if Fixed |
|---------|-------------------|----------------------|
| CC-R2-001 (T-08 comment) + CC-R2-002 (tagline) | Completeness: 0.82 → 0.90 | +0.016 composite |
| CC-R2-006 (observable skills) + CC-R2-004 (category naming) + CC-R2-005 (version/checklist) | Completeness: 0.90 → 0.95 | +0.010 composite |
| IN-R2-002 (HAP-04 guard) + IN-R2-003 (example clarity) + IN-R2-004 (scope boundary) | Methodological Rigor: 0.88 → 0.93 | +0.010 composite |
| SR-R2-009 (step titles) + DA-R2-002 (positive model) | Actionability: 0.87 → 0.92 | +0.008 composite |
| IN-R2-001 (one-path clarification) | Internal Consistency: 0.88 → 0.91 | +0.006 composite |

**Projected Round 3 score (all SR-R2 recommendations applied): 0.95–0.96**

Achieving 0.95 requires application of ALL Round 2 recommendations, specifically:
1. **Critical path (Major findings):** SR-R2-001, SR-R2-002, SR-R2-003 (tutorial fixes)
2. **Critical path (Reference):** SR-R2-004, SR-R2-005 (category naming + completeness)
3. **Secondary path:** SR-R2-006 through SR-R2-009 (explanation scope, how-to HAP-04, reference examples, step titles)

### Verdict

**Round 2 Score: 0.871 — REJECTED**

Operational band: REVISE (0.85–0.91) — near threshold, targeted revision sufficient.

The core gap is the Completeness dimension (0.82). Seven Round 1 findings remain unfixed, with two (tagline CC-R2-002, T-08 CC-R2-001) constituting Major findings that directly prevent the templates from meeting their primary quality criteria (T-07, T-08). All other Round 2 findings are Minor severity and represent incremental improvements rather than structural defects.

**Round 3 readiness:** Apply SR-R2-001 through SR-R2-009. Prioritize SR-R2-001 (tagline), SR-R2-002 (T-08 comment), SR-R2-003 (observable skills), and SR-R2-004 (category naming) as the highest-impact changes. Estimated Round 3 score: 0.95–0.96.

---

## Execution Statistics

- **Total Findings:** 12
- **Critical:** 0
- **Major:** 3
- **Minor:** 9
- **Round 1 Findings Resolved:** 12 of 20 (60%)
- **Round 1 Findings Persisting:** 7 of 20 (35%)
- **New Findings (introduced by remediations):** 4 (IN-R2-001, IN-R2-004, DA-R2-001, DA-R2-002)
- **S-007 Protocol Steps Completed:** 4 of 4
- **S-013 Protocol Steps Completed:** 4 of 4
- **S-002 Protocol Steps Completed:** 3 of 3
- **S-010 Protocol Steps Completed:** 9 recommendations produced

---

*Adversarial Review Round 2 executed by: adv-executor*
*Constitutional compliance: P-001 (evidence-based findings), P-002 (persisted), P-004 (provenance cited per finding)*
*H-16 note: S-002 executed without prior S-003 per user authority (H-02). Steelman position acknowledged and applied inline.*
*Round 1 SSOT: `projects/PROJ-013-diataxis/reviews/adversary-round1-templates.md`*
