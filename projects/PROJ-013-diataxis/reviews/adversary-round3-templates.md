# Adversarial Review: Templates (Round 3)

## Execution Context

- **Strategy:** S-007 (Constitutional AI Critique), S-013 (Inversion Technique), S-002 (Devil's Advocate), S-010 (Self-Refine)
- **Templates:** `.context/templates/adversarial/s-007-constitutional-ai.md`, `s-013-inversion.md`, `s-002-devils-advocate.md`, `s-010-self-refine.md`
- **Deliverables Reviewed:**
  - `skills/diataxis/templates/tutorial-template.md`
  - `skills/diataxis/templates/howto-template.md`
  - `skills/diataxis/templates/reference-template.md`
  - `skills/diataxis/templates/explanation-template.md`
- **Reference Standard:** `skills/diataxis/rules/diataxis-standards.md`
- **Prior Round:** `projects/PROJ-013-diataxis/reviews/adversary-round2-templates.md` (Score: 0.871, 12 findings)
- **Quality Threshold:** >= 0.95 weighted composite
- **Executed:** 2026-02-27
- **Finding Prefixes:** CC-NNN (S-007), IN-NNN (S-013), DA-NNN (S-002), SR-NNN (S-010)
- **Finding execution_id:** R3

### H-16 Note

S-002 (Devil's Advocate) was executed without a prior S-003 (Steelman) pass, per the user's explicit strategy ordering per H-02 (user authority). The steelman position is acknowledged inline with each DA finding: the templates are intentionally lean scaffolds, and prescriptive depth must be balanced against maintenance burden and writer-agent autonomy.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Round 2 Fix Verification](#round-2-fix-verification) | Status of all 9 Round 2 SR-R2 recommendations |
| [S-007 Constitutional Compliance (Round 3)](#s-007-constitutional-compliance-round-3) | Remaining constitutional gaps after remediations |
| [S-013 Inversion Analysis (Round 3)](#s-013-inversion-analysis-round-3) | New inversion scenarios applied to remediated templates |
| [S-002 Devils Advocate Findings (Round 3)](#s-002-devils-advocate-findings-round-3) | Remaining and new challenges |
| [S-010 Self-Refine Recommendations (Round 3)](#s-010-self-refine-recommendations-round-3) | Remaining improvements |
| [Finding Summary Table](#finding-summary-table) | All Round 3 findings consolidated |
| [Quality Assessment](#quality-assessment) | Composite score and threshold verdict |

---

## Round 2 Fix Verification

The following table records the Round 2 SR-R2 fix status based on direct inspection of the current template files.

| R2 SR # | Recommendation | Status | Evidence |
|---------|----------------|--------|---------|
| SR-R2-001 | Tutorial tagline: require concrete completion state | **FIXED** | Line 3: `{One-sentence description of what the reader will have built, configured, or created by the end -- state a concrete, observable artifact, not an abstract skill.}` — concrete artifact orientation enforced |
| SR-R2-002 | Add T-08 compliance comment to Steps section | **FIXED** | Line 26: `<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED]. -->` — T-08 and [UNTESTED] flag introduced |
| SR-R2-003 | Fix "What You Learned" observable skill placeholder | **FIXED** | Lines 63-64: `{Observable skill 1 -- e.g., "create a new project with 'jerry session start'"}` — concrete action-verb examples now embedded in placeholders |
| SR-R2-004 | Add category naming guidance to Reference (R-01) | **FIXED** | Lines 13, 17, 48: `## {Category 1 — name should mirror the described system's own terminology (R-01)}` and comment `<!-- R-01: Category names should mirror the described system's own structure -- for code: module/class names; for CLI: command groups; for config: section names. -->` |
| SR-R2-005 | Add version metadata slots and R-07 completeness checklist | **FIXED** | Line 24: `**Since:** {version or date introduced — optional, include for versioned systems}` added; line 66: `<!-- R-07 Completeness Checklist: Before finalizing, verify every public interface/command/parameter/field is documented. -->` added |
| SR-R2-006 | Strengthen explanation scope boundary | **FIXED** | Line 5: `> **Scope:** This document explains {specific aspect of topic — must be a bounded concept, not the entire domain}. It does not cover {specific out-of-scope items — name at least one concrete exclusion}.` — "at least one concrete exclusion" now required |
| SR-R2-007 | Add HAP-04 guard to How-To Step 2 conditional branches | **FIXED** | Lines 51-52: `<!-- HAP-04 guard: Include at most one "If you need X, do Y" conditional per step. Additional conditionals suggest the step should be split or the variations documented in separate guides. -->` — location is after all steps (slightly different from recommendation), functionally correct |
| SR-R2-008 | Clarify reference example placeholder to prevent RAP-02 | **FIXED** | Lines 31-32: `{illustrative usage showing the entry in context — NOT a procedural recipe}` and line 45: `{illustrative usage — shows the entry in use, does not instruct the reader to perform actions}` — distinction from instruction made explicit |
| SR-R2-009 | Add step title imperative verb guidance to How-To | **FIXED** | Lines 18, 26, 42: `### 1. {Imperative verb + object — e.g., "Configure the database connection"}` — positive voice model embedded |

### Fix Summary

| Status | Count | Items |
|--------|-------|-------|
| FIXED | 9 | SR-R2-001 through SR-R2-009 (all) |
| PARTIALLY FIXED | 0 | — |
| NOT FIXED | 0 | — |

All 9 Round 2 SR-R2 recommendations have been applied. Round 3 analysis proceeds against the remediated templates.

---

## S-007 Constitutional Compliance (Round 3)

*Apply S-007 Execution Protocol: check remaining constitutional gaps, any new anti-pattern exposure from Round 2 remediations, and cross-reference consistency across all four templates.*

### Constitutional Context

Applicable principles from `diataxis-standards.md` (the domain constitution for these templates):
- **T-01 through T-08:** Tutorial quality criteria (HARD for template structural compliance)
- **TAP-01 through TAP-05:** Tutorial anti-patterns
- **H-01 through H-07:** How-To guide quality criteria
- **HAP-01 through HAP-05:** How-To anti-patterns
- **R-01 through R-07:** Reference quality criteria
- **RAP-01 through RAP-05:** Reference anti-patterns
- **E-01 through E-07:** Explanation quality criteria
- **EAP-01 through EAP-05:** Explanation anti-patterns
- **H-23 (markdown navigation), H-15 (self-review):** Jerry framework HARD rules

### CC-R3-001: Tutorial — Step Body Placeholder (Steps 2 and 3) Inconsistent with Step 1

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `tutorial-template.md` — Step 2 (line 40) and Step 3 (line 50) body placeholders |
| **Strategy Step** | S-007 check (b): anti-pattern exposure from remediations |

**Evidence:**
- Step 1 body (line 30): `{Brief instruction. One path only — no "alternatively" or "you could also."}`
- Step 2 body (line 40): `{Brief instruction.}` (no anti-TAP-03 guard)
- Step 3 body (line 50): `{Brief instruction.}` (no anti-TAP-03 guard)

The Round 1 SR-003 fix (TAP-03 guard) was applied to Step 1 but not propagated to Steps 2 and 3. This creates an internal consistency failure: the template teaches a constraint in Step 1 that disappears in Steps 2 and 3. A writer-agent following the template pattern after Step 1 would produce unguarded steps.

**Analysis:**
T-04 (no alternatives offered) applies across all tutorial steps, not just Step 1. The TAP-03 guard in Step 1's placeholder communicates an important constraint, but a writer following the template pattern would see Step 2 and Step 3 with simpler placeholders and might infer the constraint only applies to Step 1.

**Recommendation:**
Apply the TAP-03 guard uniformly to Steps 2 and 3:
```
{Brief instruction. One path only — no "alternatively" or "you could also."}
```

---

### CC-R3-002: Reference — Third Category Entry Has Unguarded Example Placeholder

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `reference-template.md` — line 63 |
| **Strategy Step** | S-007 check (b): anti-pattern exposure; RAP-02 risk |

**Evidence:**
Line 63 (Category 2 entry example block):
```
{usage example}
```

Compare to Category 1 entries:
- Line 31-32: `{illustrative usage showing the entry in context — NOT a procedural recipe}` (SR-R2-008 fix applied)
- Line 45: `{illustrative usage — shows the entry in use, does not instruct the reader to perform actions}` (SR-R2-008 fix applied)
- Line 63: `{usage example}` — unguarded; reverts to Round 1 quality level

SR-R2-008 fixed two of three example placeholders. The third Category 2 entry retains the undifferentiated `{usage example}` placeholder with no illustrative-vs-instructional guidance.

**Analysis:**
R-06 (examples included) is satisfied structurally by any of the three example slots. However, RAP-02 (instructions/recipes) applies to all example slots, not just two. The Category 2 third-entry placeholder permits a writer to produce: "To use this parameter, first check the existing value, then set it to your desired value, and restart." — a RAP-02 violation. Consistency requires the guard on all example slots.

**Recommendation:**
Change line 63 from:
```
{usage example}
```
To:
```
{illustrative usage — shows the entry in use, does not instruct the reader to perform actions}
```

---

### CC-R3-003: Tutorial — T-08 Comment Uses "[UNTESTED]" Flag Without Specifying Placement

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `tutorial-template.md` — line 26 |
| **Strategy Step** | S-007 check (a): structural match to T-08; actionability gap |

**Evidence:**
Line 26: `<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED]. -->`

The comment instructs writers to use `[UNTESTED]` for unverified steps but does not specify WHERE to place the flag. The Step 1 heading is `### 1. {First action}` — there is no example of what `[UNTESTED]` in context looks like.

**Analysis:**
T-08 compliance (reliable reproduction) requires the author to have run the steps. The `[UNTESTED]` flag is a safety mechanism for explicitly acknowledging incomplete verification. However, a writer who has never seen the flag in context does not know: does it go on the step heading (`### 1. [UNTESTED] {First action}`)? On the Expected result line? Inline within the instruction? The comment is directionally correct but ambiguous in operational terms.

**Recommendation:**
Extend line 26 with a placement example:
```markdown
<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED].
     Example: "### 2. [UNTESTED] Configure the database" -- flag appears on the step heading. -->
```

---

### CC-R3-004: Explanation — "Alternative Perspectives" Section Has No Guard Against EAP-01

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `explanation-template.md` — lines 33-35 |
| **Strategy Step** | S-007 check (c): cross-reference EAP-01 (instructional creep) |

**Evidence:**
Lines 33-35:
```
## Alternative Perspectives

{Acknowledge that other valid approaches or viewpoints exist. Explain the trade-offs.}
```

The "Explain the trade-offs" instruction is discursive-appropriate. However, the `## Alternative Perspectives` section has no EAP-01 warning. Writers discussing alternative approaches may naturally reach for imperative constructions: "To use approach B, first configure..." — embedding instructions within what should be discursive trade-off analysis.

**Analysis:**
EAP-01 (instructional creep) applies to all sections of an explanation document, not just the conceptual body sections (which already carry the EAP-01 guard at line 17: `Do NOT use imperative verbs...`). The "Alternative Perspectives" section involves discussing approaches, which creates a natural slope toward instructional prose. The `## Context` section (line 13) and the core concept sections carry EAP-01 guidance, but `## Alternative Perspectives` and `## Connections` do not.

**Recommendation:**
Add a guard comment to the Alternative Perspectives placeholder:
```markdown
{Acknowledge that other valid approaches or viewpoints exist. Explain the trade-offs in discursive prose — no imperative instructions (EAP-01). Describe the trade-off; do not direct the reader to "use approach B instead."}
```

---

### CC-R3-005: How-To — HAP-04 Guard Placement After Step 3 Reduces Effectiveness

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `howto-template.md` — lines 51-52 |
| **Strategy Step** | S-007 check (b): remediation effectiveness |

**Evidence:**
Lines 50-52 (after Step 3, before Verification section):
```
<!-- Add as many steps as needed. Keep each step focused on a single action. -->
<!-- HAP-04 guard: Include at most one "If you need X, do Y" conditional per step. Additional conditionals suggest the step should be split or the variations documented in separate guides. -->
```

SR-R2-007 placed the HAP-04 guard after all 3 steps. The Round 2 recommendation (IN-R2-002) specifically called for the guard after Step 2's conditional blocks where the pattern is introduced. A writer reading Step 2's conditional pattern and then writing Steps 3, 4, 5, 6 with multiple branches each would not encounter the guard until after all three model steps are complete.

**Analysis:**
The guard placement after Step 3 is better than no guard at all, but the educational moment is missed. The conditional branch pattern is introduced in Step 2. The guard's instructional value is highest WHEN the pattern is introduced, not three steps later. A writer agent modeling subsequent steps on Step 2 may replicate the multi-branch pattern before reaching the guard.

**Recommendation:**
Add a second, in-situ HAP-04 comment inline within Step 2 immediately after the conditional block (lines 39-40), keeping the existing summary guard at lines 51-52:
```markdown
<!-- HAP-04: Limit to 1 conditional per step. More than 1 suggests separate guides are needed. -->
```

---

## S-013 Inversion Analysis (Round 3)

*Apply S-013 Execution Protocol steps 1-6 to the remediated templates. Identify assumptions the templates rely on, invert them, and stress-test consequences.*

### Step 1: State the Goals

The four diataxis templates share these primary goals:
1. **G-01:** Enable writer-agents to produce documentation that complies with all per-quadrant quality criteria (T-01 through T-08, H-01 through H-07, R-01 through R-07, E-01 through E-07)
2. **G-02:** Prevent per-quadrant anti-patterns (TAP-01-05, HAP-01-05, RAP-01-05, EAP-01-05) without requiring writers to have memorized them
3. **G-03:** Produce consistent documentation voice per Section 5 of diataxis-standards.md across all four quadrants
4. **G-04:** Serve as the single authoritative template for each documentation type — no additional scaffolding needed
5. **G-05 (implicit):** Be maintainable as the standards evolve

### Step 2: Invert the Goals (Anti-Goals)

Anti-goals derived from inverting G-01 through G-05:

**Anti-G-01:** Writers produce documentation that structurally satisfies template syntax while violating quality criteria semantically. Templates permit criterion-violating content without detection.

**Anti-G-02:** Anti-pattern guards are present but interpreted incorrectly, producing new variants of the same anti-pattern category or adjacent anti-patterns.

**Anti-G-03:** Voice guidance is consistent across templates but ambiguous enough that different writer-agents produce recognizably different voices for the same quadrant type.

**Anti-G-04:** Template dependencies are implicit — a writer must also consult other documents (beyond the template's comment pointers) to produce correct output.

**Anti-G-05:** Template structure ossifies so that quality criteria updates require re-authoring all four templates rather than updating a single pointed-to source.

### Step 3: Map All Assumptions

| ID | Assumption | Type | Category | Confidence |
|----|-----------|------|----------|------------|
| A-01 | Writer agents receive templates as raw markdown (HTML comments visible) | Technical | Explicit (DA-R2-001 acknowledged) | Medium |
| A-02 | Writer agents will read ALL comment blocks, not just rendered headings and placeholders | Process | Implicit | Medium |
| A-03 | Placeholder text length/format signals expected response length to writer agents | Technical | Implicit | Medium |
| A-04 | The diataxis-standards.md pointer in each comment block is sufficient for agents that need more detail | Process | Implicit | High |
| A-05 | Templates are used in isolation — one template per document production task | Process | Implicit | High |
| A-06 | "Observable skill 1" example citations in tutorial (jerry-specific CLI commands) will generalize appropriately to non-jerry contexts | Resource | Implicit | Low |
| A-07 | Category heading guidance (R-01) in reference-template will be read as prescriptive constraint, not aspirational suggestion | Process | Implicit | Medium |
| A-08 | The scope boundary format in explanation-template ("must be a bounded concept") will elicit bounded concepts rather than vague abstractions | Process | Implicit | Medium |

### Step 4: Stress-Test Each Assumption

| ID | Assumption | Inversion | Plausibility | Severity | Evidence | Affected Dimension |
|----|-----------|-----------|-------------|----------|----------|--------------------|
| IN-R3-001 | A-06: Observable skill examples cite jerry CLI | Examples do NOT generalize — agents produce jerry-specific skills for non-jerry tutorials | High | Major | Tutorial lines 63-64: `e.g., "create a new project with 'jerry session start'"` and `e.g., "validate entity files with 'jerry ast validate'"` | Methodological Rigor |
| IN-R3-002 | A-03: Placeholder length signals response length | Agents match placeholder verbosity and produce terse 3-5 word step instructions for all steps, including complex multi-part steps | Medium | Minor | Step 1 body placeholder is a single sentence; agents may interpret this as the expected density for all steps | Completeness |
| IN-R3-003 | A-07: R-01 guidance is read as constraint | Writers interpret "should mirror" as a soft preference and name categories by user-facing function ("Common Scenarios") instead of system structure | High | Major | Reference line 17: `<!-- R-01: Category names should mirror the described system's own structure` — "should" is MEDIUM-tier language, not HARD | Methodological Rigor |
| IN-R3-004 | A-02: Writers read ALL comment blocks | Writer agent receives a "clean" version of the template (compiled for display), comments stripped — all quality enforcement disappears | Medium | Minor | Structural dependency on comment visibility (acknowledged from DA-R2-001 Round 2; persists) | Actionability |
| IN-R3-005 | A-08: Scope boundary elicits bounded concepts | Writer fills scope as `{specific aspect of topic — must be a bounded concept}` → produces "This document explains the entire authentication system." ("entire authentication system" reads as specific but is actually unbounded) | Medium | Minor | Explanation line 5: the bounded concept requirement is asserted but not exemplified | Completeness |

### Step 5: Develop Mitigations

**IN-R3-001 (Major — MUST mitigate):**
The tutorial observable skill examples use jerry-specific CLI commands that are deeply embedded in the Jerry project context. When the diataxis skill is used for non-jerry documentation contexts, these examples break the "concrete positive model" intent and could mislead agents into jerry-specific outputs.

Mitigation: Replace one of the two jerry-specific examples with a generic example, and make the jerry-specific examples clearly context-dependent:
```markdown
- {Observable skill 1 -- action verb required. Example for Jerry docs: "create a new project with `jerry session start`". Example for generic docs: "configure a TLS certificate using `openssl req`"}
```

**IN-R3-003 (Major — MUST mitigate):**
The R-01 category guidance uses "should" language (MEDIUM tier) for a structural requirement that is treated as HARD in diataxis-standards.md (R-01 is a listed quality criterion, not a soft guideline). The current language permits drift by treating R-01 as optional.

Mitigation: Change the R-01 comment from MEDIUM ("should") to HARD-equivalent language in context:
```markdown
<!-- R-01: Category names MUST mirror the described system's own structure — for code: module/class names;
     for CLI: command groups; for config: section names. Organizational names ("Common Options", "Advanced
     Use Cases") violate R-01 and indicate the reference structure does not mirror the system. -->
```

---

### IN-R3-001: Tutorial Observable Skill Examples Are Jerry-Specific [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `tutorial-template.md` — lines 63-64 |
| **Strategy Step** | S-013 Step 4: stress-test assumption A-06 |

**Type:** Assumption (A-06: Observable skill examples will generalize)

**Original Assumption:** The two jerry-specific CLI examples embedded in the observable skill placeholders will guide writer-agents to produce domain-appropriate action verbs and concrete skills, regardless of the domain being documented.

**Inversion:** Writer-agents producing non-jerry documentation follow the embedded examples literally, producing skill lists referencing `jerry session start` and `jerry ast validate` in tutorials for databases, APIs, or infrastructure tools.

**Plausibility:** High — few AI agents have the domain judgment to recognize that an embedded example is a context-specific illustration and not a template to copy. The SR-R2-003 fix was a significant improvement over `{Skill acquired 1}`, but it over-indexed on the specific Jerry framework examples.

**Consequence:** Non-jerry tutorials from the diataxis skill would have "What You Learned" sections with jerry CLI commands that are factually wrong for the target domain. This is a structural contamination of the most reader-facing section of the tutorial.

**Evidence:** Tutorial lines 63-64:
```
- {Observable skill 1 -- e.g., "create a new project with `jerry session start`"}
- {Observable skill 2 -- e.g., "validate entity files with `jerry ast validate`"}
```

**Dimension:** Methodological Rigor (T-05: concrete not abstract — concreteness here is wrong-domain-concrete)

**Mitigation:** Provide one jerry-specific and one generic domain example, clearly framed as alternative depending on context.

**Acceptance Criteria:** Observable skill placeholder must demonstrably guide both jerry-specific and generic documentation without producing incorrect literal citations.

---

### IN-R3-003: Reference R-01 Language Is MEDIUM-Tier When R-01 Is a HARD Quality Criterion [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `reference-template.md` — lines 13, 17, 48, 50 |
| **Strategy Step** | S-013 Step 4: stress-test assumption A-07 |

**Type:** Assumption (A-07: R-01 guidance read as prescriptive constraint)

**Original Assumption:** The phrase "should mirror" and "Category names should mirror" will be read as a prescriptive constraint by writer-agents, preventing organizational category naming.

**Inversion:** Writer-agents correctly parse "should" as MEDIUM-tier language (SHOULD = "override with documented justification" per quality-enforcement.md tier vocabulary) and produce categories named "Common Operations", "Advanced Configuration", "Security Settings" — all of which satisfy the MEDIUM constraint by any reasonable reading.

**Plausibility:** High — "should" is explicitly defined as overridable with documented justification in the Jerry framework's own tier vocabulary (quality-enforcement.md). Agents trained on this framework would parse "should" correctly and override without reporting a violation.

**Consequence:** Reference documents from the diataxis skill systematically violate R-01 (mirrors described structure) while appearing compliant to the template guidance. The R-01 guidance in the template communicates "preferred" when diataxis-standards.md treats it as a quality criterion with pass/fail test.

**Evidence:**
- Line 13: `## {Category 1 — name should mirror the described system's own terminology (R-01)}`
- Line 17: `<!-- R-01: Category names should mirror the described system's own structure`

Both use "should" — a MEDIUM qualifier that Jerry agents are trained to treat as overridable.

**Dimension:** Methodological Rigor (R-01 compliance)

**Mitigation:** Replace "should" with "must" or equivalent HARD-tier language aligned with R-01's pass/fail test status.

**Acceptance Criteria:** After change, no reasonable agent reading the template could interpret R-01 as optional.

---

## S-002 Devil's Advocate Findings (Round 3)

*Apply S-002 Execution Protocol: challenge the remediated templates' core claims and the adequacy of Round 2-3 fixes.*

### H-16 Compliance Note
S-003 Steelman was not applied in this round per user authority (H-02). Steelman position acknowledged inline with each DA finding below.

### DA-R3-001: The Templates Now Risk Over-Constraining Writers on Scope at the Expense of Practical Completeness

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `explanation-template.md` — line 5; `howto-template.md` — lines 51-52 |
| **Strategy Step** | S-002 Step 3: Construct counter-arguments, Lens 4 (Alternative interpretations) |

**Steelman position:** Scope boundaries and HAP-04 guards are necessary quality gates. Unbounded scope (EAP-05) and completeness-over-focus (HAP-04) are Major anti-patterns in diataxis-standards.md. The templates are correctly tightening these constraints.

**Counter-argument (devil's advocate):** The cumulative effect of scope restriction guidance across explanation (must name exclusions) and how-to (at most one conditional per step) may produce documentation that is technically compliant but practically incomplete for complex real-world topics.

Specifically:
- An explanation about distributed system consensus requires covering multiple related protocols (Raft, Paxos, PBFT). The "name at least one concrete exclusion" instruction could produce: "This document explains Raft. It does not cover Paxos or PBFT" — a scope boundary that understates the document's actual relationship to excluded topics and implies those topics are wholly separate rather than related perspectives on the same problem.
- A how-to guide for deploying a service may genuinely require 3+ conditional branches for the main path (Kubernetes vs Docker vs bare metal) where each is a first-class variation, not an edge case. The HAP-04 guard ("at most one conditional per step") creates pressure to split into 3 guides when one unified guide with clearly labeled platform branches would serve users better.

**Assessment:** The counter-argument reveals that the templates' scope guards need to distinguish between restrictive scoping (rejecting EAP-05/HAP-04 anti-patterns) and artificially narrow scope that impedes legitimate comprehensive treatment. The templates apply the guards uniformly without acknowledging that some topics legitimately require broader scope.

**Recommendation:**
- For HAP-04 guard: add "unless all variations are first-class paths for the same task" qualifier
- For explanation scope: add guidance that exclusions should name genuinely separate topics, not sub-aspects of the explained concept that the document must also cover

---

### DA-R3-002: The Reference Template's Version Fields Are Structurally Orphaned

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `reference-template.md` — lines 24, 34-38 |
| **Strategy Step** | S-002 Step 3: Construct counter-arguments, Lens 5 (Unaddressed risks) |

**Steelman position:** Adding optional `Since:` version field improves R-05 compliance (consistent structure) for versioned systems. It is genuinely useful for API reference documentation.

**Counter-argument (devil's advocate):** The `Since:` field appears in one of three entry templates but not the other two. Specifically:
- Category 1, Entry 1 (lines 19-28): Has `**Since:** {version or date introduced — optional, include for versioned systems}` (SR-R2-005 fix)
- Category 1, Entry 2 (lines 34-46): Does NOT have the `Since:` field
- Category 2, Entry (lines 52-64): Does NOT have the `Since:` field

This asymmetry directly violates R-05 (standard formatting — ALL entries follow the same structure). SR-R2-005 added the field to one entry but not to the other entries it was supposed to make consistent. The fix created a new R-05 violation to address a different R-05 gap.

**Assessment:** This is an objective structural inconsistency in the current template state, not a subjective devil's advocate position. The inconsistency is verifiable at lines 24 vs 34-38 vs 52-58. Severity is Minor because the field is explicitly optional ("omit if not version-tracked"), but the inconsistent appearance across entry templates may confuse writers about whether the field is template-required or context-optional.

**Recommendation:**
Add the optional `Since:` field consistently to ALL three entry templates, or add a comment in the entry templates that don't have it noting the field is available:
```markdown
**Since:** {version introduced — optional, omit if not version-tracked}
```

---

### DA-R3-003: The Tutorial's T-08 Fix Introduces a Correctness Risk for Multi-Environment Steps

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `tutorial-template.md` — line 26 |
| **Strategy Step** | S-002 Step 3: Construct counter-arguments, Lens 5 (Unaddressed risks), Lens 6 (Historical failure precedents) |

**Steelman position:** T-08 (reliable reproduction) is one of the most important tutorial quality criteria. The `[UNTESTED]` flag enables authors to be honest about verification status. The SR-R2-002 fix correctly operationalizes T-08.

**Counter-argument (devil's advocate):** The `[UNTESTED]` flag creates a binary: steps are either verified or `[UNTESTED]`. This misses the important middle case: steps were verified on one environment but not others. A tutorial for a cross-platform tool (Unix/Windows/macOS) may have steps verified on macOS but not on Windows. The T-08 comment does not address partial verification.

Historical precedent: Many documentation quality failures come not from no verification (which `[UNTESTED]` addresses) but from single-environment verification where the author assumes their environment is canonical. The author marks no steps `[UNTESTED]` because they ran all commands — on macOS. Windows readers encounter failures that the author would have classified as "tested and working."

**Assessment:** The T-08 fix is a meaningful improvement but the binary verified/unverified framing misses the partial-verification failure mode that is arguably more common than zero verification. This is a Minor finding because the template cannot mandate environment-specific verification, but a note acknowledging the multi-environment concern would improve T-08's practical effectiveness.

**Recommendation:**
Extend the T-08 comment to acknowledge environment scope:
```markdown
<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED].
     Example: "### 2. [UNTESTED] Configure the database" -- flag appears on the step heading.
     Multi-environment note: If steps were verified on one OS, add context (e.g., "Verified on macOS 14.
     Windows users: see troubleshooting section for known differences.") -->
```

---

## S-010 Self-Refine Recommendations (Round 3)

*Systematic self-critique against all 6 scoring dimensions. All Round 3 findings reviewed. Recommendations ordered by impact.*

### SR-R3-001: Tutorial — Propagate TAP-03 Guard to Steps 2 and 3 (addresses CC-R3-001)

**Impact:** Moderate — Internal Consistency dimension. Ensures T-04 (no alternatives offered) is consistently enforced across all steps, not just Step 1.

Change Step 2 body (line 40) and Step 3 body (line 50) from:
```markdown
{Brief instruction.}
```
To:
```markdown
{Brief instruction. One path only — no "alternatively" or "you could also."}
```

---

### SR-R3-002: Reference — Fix Third Category Entry Example Placeholder (addresses CC-R3-002)

**Impact:** Moderate — Internal Consistency dimension and RAP-02 compliance. Category 2's third entry example remains unguarded after SR-R2-008 fixed the first two.

Change line 63 from:
```markdown
{usage example}
```
To:
```markdown
{illustrative usage — shows the entry in use, does not instruct the reader to perform actions}
```

---

### SR-R3-003: Tutorial — Fix Observable Skill Examples to Be Domain-Agnostic (addresses IN-R3-001)

**Impact:** High — Methodological Rigor dimension. Jerry-specific CLI examples will contaminate non-jerry tutorial output.

Change lines 63-64 from:
```markdown
- {Observable skill 1 -- e.g., "create a new project with `jerry session start`"}
- {Observable skill 2 -- e.g., "validate entity files with `jerry ast validate`"}
```
To:
```markdown
- {Observable skill 1 -- action verb required. Format: "[verb] [specific thing] using [specific method]". Example (Jerry): "create a new project with `jerry session start`". Example (generic): "configure a TLS certificate using `openssl req -newkey`".}
- {Observable skill 2 -- action verb required, same format.}
```

---

### SR-R3-004: Reference — Upgrade R-01 Language from MEDIUM to HARD-equivalent (addresses IN-R3-003)

**Impact:** High — Methodological Rigor dimension. "Should" language is overridable by trained agents; R-01 is a pass/fail quality criterion.

Change line 13 from:
```markdown
## {Category 1 — name should mirror the described system's own terminology (R-01)}
```
To:
```markdown
## {Category 1 — name MUST mirror the described system's own structure: module names, command groups, config section names. NOT organizational names like "Common Options" or "Advanced Use Cases" (R-01 violation).}
```

Change line 17 from:
```markdown
<!-- R-01: Category names should mirror the described system's own structure -- for code: module/class names; for CLI: command groups; for config: section names. -->
```
To:
```markdown
<!-- R-01 (REQUIRED): Category names MUST mirror the described system's own structure -- for code: module/class names; for CLI: command groups; for config: section names. Organizational names violate R-01. -->
```

Apply same change to line 48 (`## {Category 2 — name mirrors system structure (R-01)}`):
```markdown
## {Category 2 — name MUST mirror the system's own structure (R-01). See Category 1 heading for guidance.}
```

---

### SR-R3-005: Reference — Propagate "Since" Field to All Entry Templates (addresses DA-R3-002)

**Impact:** Moderate — Internal Consistency dimension. R-05 (standard formatting) requires all entries to follow the same structure. The Since field appears in Category 1 Entry 1 but not in Category 1 Entry 2 or Category 2 Entry.

Add `**Since:** {version introduced — optional, omit if not version-tracked}` after `**Required:**` in:
- Category 1, Entry 2 (after line 38)
- Category 2, Entry (after line 57)

---

### SR-R3-006: Tutorial — Extend T-08 Comment for Multi-Environment Scope (addresses DA-R3-003)

**Impact:** Minor — Evidence Quality dimension. Partial-verification failure mode is more common than zero-verification; T-08 comment should acknowledge it.

Change line 26 from:
```markdown
<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED]. -->
```
To:
```markdown
<!-- T-08: Author must verify steps produce documented results, or flag unverified steps with [UNTESTED].
     Example: "### 2. [UNTESTED] Configure the database" -- flag on the step heading.
     Multi-environment: if verified on one OS only, note scope ("Verified on macOS 14; Windows users: see Troubleshooting"). -->
```

---

### SR-R3-007: Explanation — Add EAP-01 Guard to Alternative Perspectives Section (addresses CC-R3-004)

**Impact:** Minor — Methodological Rigor dimension. The Alternative Perspectives section creates slope toward instructional prose; EAP-01 guidance should be consistent across all section placeholders.

Change lines 33-35 from:
```markdown
## Alternative Perspectives

{Acknowledge that other valid approaches or viewpoints exist. Explain the trade-offs.}
```
To:
```markdown
## Alternative Perspectives

{Acknowledge that other valid approaches or viewpoints exist. Explain the trade-offs in discursive prose — no imperative verbs (EAP-01). Describe approaches comparatively; do not direct the reader to switch to a different approach.}
```

---

### SR-R3-008: How-To — Add In-Situ HAP-04 Guard to Step 2 (addresses CC-R3-005)

**Impact:** Minor — Methodological Rigor dimension. HAP-04 guard placement at end of all steps misses the educational moment in Step 2 where the conditional branch pattern is introduced.

Add a one-line comment immediately after the Step 2 conditional block (after line 39, before the closing of Step 2):
```markdown
<!-- HAP-04: This pattern (one conditional per step) is the maximum. -->
```

---

## Finding Summary Table

| ID | Severity | Template | Finding | Section | Status vs Round 2 |
|----|----------|----------|---------|---------|------------------|
| CC-R3-001 | Minor | Tutorial | TAP-03 guard applied to Step 1 only; Steps 2 and 3 body placeholders unguarded — T-04 inconsistently enforced | Lines 40, 50 | NEW (remediation gap from SR-003) |
| CC-R3-002 | Minor | Reference | Third example placeholder `{usage example}` unguarded after SR-R2-008 fixed first two — RAP-02 risk persists in Category 2 | Line 63 | NEW (remediation gap from SR-R2-008) |
| CC-R3-003 | Minor | Tutorial | T-08 `[UNTESTED]` flag lacks placement guidance — actionability gap | Line 26 | NEW (quality of SR-R2-002 fix) |
| CC-R3-004 | Minor | Explanation | `## Alternative Perspectives` section has no EAP-01 guard — instructional creep risk in trade-off analysis | Lines 33-35 | NEW |
| CC-R3-005 | Minor | How-To | HAP-04 guard placed after Step 3 rather than within Step 2 where pattern is introduced — educational moment missed | Lines 51-52 | NEW (quality of SR-R2-007 placement) |
| IN-R3-001 | Major | Tutorial | Observable skill examples are jerry-specific CLI commands — will contaminate non-jerry tutorial output; A-06 assumption fails | Lines 63-64 | NEW (introduced by SR-R2-003) |
| IN-R3-003 | Major | Reference | R-01 guidance uses "should" (MEDIUM tier) — agents trained on Jerry framework can override without violation report; R-01 is a pass/fail quality criterion | Lines 13, 17, 48 | PERSISTS (quality gap in SR-R2-004 wording) |
| DA-R3-001 | Minor | Explanation, How-To | Scope restriction guidance may produce technically compliant but practically incomplete docs for legitimately complex topics | Explanation line 5; How-To lines 51-52 | NEW (systemic tension) |
| DA-R3-002 | Minor | Reference | `Since:` version field added to Entry 1 only; Entries 2 and 3 lack it — new R-05 (standard formatting) violation | Lines 24 vs 34-38 vs 52-58 | NEW (introduced by SR-R2-005) |
| DA-R3-003 | Minor | Tutorial | T-08 binary verified/unverified misses partial-verification failure mode (verified on one OS, not others) | Line 26 | NEW (quality gap in SR-R2-002) |

**Total Round 3 Findings:** 10
**Critical:** 0
**Major:** 2 (IN-R3-001, IN-R3-003)
**Minor:** 8

---

## Quality Assessment

### Round 2 Fix Impact on Dimensions

All 9 SR-R2 recommendations were applied. Impact assessment on Round 2 dimension scores:

| Dimension | R2 Score | Fix Impact | R3 Pre-Review Score |
|-----------|----------|------------|---------------------|
| Completeness | 0.82 | SR-R2-001 (tagline), SR-R2-002 (T-08), SR-R2-003 (observable skills), SR-R2-005 (version/checklist) applied | 0.92 |
| Internal Consistency | 0.88 | SR-R2-004 (R-01 in heading), SR-R2-007 (HAP-04 guard), SR-R2-009 (step titles) applied; new inconsistencies DA-R3-002 (Since field) and CC-R3-001 (TAP-03 propagation) | 0.89 |
| Methodological Rigor | 0.88 | SR-R2-006 (scope boundary), SR-R2-008 (example clarity) applied; IN-R3-003 (R-01 MEDIUM language) persists | 0.90 |
| Evidence Quality | 0.88 | Minor improvements from T-08 comment; DA-R3-003 (partial verification) remains unaddressed | 0.89 |
| Actionability | 0.87 | SR-R2-009 (step titles), SR-R2-007 (HAP-04 guide) applied; CC-R3-003 ([UNTESTED] placement) | 0.90 |
| Traceability | 0.92 | All four templates reference standards; no degradation | 0.93 |

### Round 3 Finding Impact on Dimensions

| Finding | Affected Dimension | Current Score | Impact |
|---------|-------------------|---------------|--------|
| CC-R3-001 (TAP-03 incomplete) | Internal Consistency | 0.89 | -0.02 |
| CC-R3-002 (3rd example unguarded) | Internal Consistency | 0.89 | -0.01 |
| CC-R3-003 ([UNTESTED] placement) | Actionability | 0.90 | -0.01 |
| CC-R3-004 (EAP-01 in Alt Perspectives) | Methodological Rigor | 0.90 | -0.01 |
| CC-R3-005 (HAP-04 placement) | Methodological Rigor | 0.90 | -0.01 |
| IN-R3-001 (jerry-specific examples) | Methodological Rigor | 0.90 | -0.03 |
| IN-R3-003 (R-01 MEDIUM language) | Methodological Rigor | 0.90 | -0.03 |
| DA-R3-001 (scope restriction tension) | Completeness | 0.92 | -0.01 |
| DA-R3-002 (Since field asymmetry) | Internal Consistency | 0.89 | -0.02 |
| DA-R3-003 (partial verification) | Evidence Quality | 0.89 | -0.01 |

### Adjusted Dimension Scores (After Round 3 Findings Applied)

| Dimension | Weight | Pre-Review Score | Finding Penalty | Adjusted Score |
|-----------|--------|-----------------|-----------------|----------------|
| Completeness | 0.20 | 0.92 | -0.01 (DA-R3-001) | **0.91** |
| Internal Consistency | 0.20 | 0.89 | -0.05 (CC-R3-001, CC-R3-002, DA-R3-002) | **0.84** |
| Methodological Rigor | 0.20 | 0.90 | -0.08 (CC-R3-004, CC-R3-005, IN-R3-001, IN-R3-003) | **0.82** |
| Evidence Quality | 0.15 | 0.89 | -0.01 (DA-R3-003) | **0.88** |
| Actionability | 0.15 | 0.90 | -0.01 (CC-R3-003) | **0.89** |
| Traceability | 0.10 | 0.93 | 0.00 | **0.93** |

### Weighted Composite Score (Round 3)

Applying S-014 weights from quality-enforcement.md:
- Completeness (0.20): 0.91 × 0.20 = **0.182**
- Internal Consistency (0.20): 0.84 × 0.20 = **0.168**
- Methodological Rigor (0.20): 0.82 × 0.20 = **0.164**
- Evidence Quality (0.15): 0.88 × 0.15 = **0.132**
- Actionability (0.15): 0.89 × 0.15 = **0.134**
- Traceability (0.10): 0.93 × 0.10 = **0.093**

**Round 3 Composite Score: 0.873 — REJECTED (below 0.95 threshold)**

### Score Trajectory and Gap Analysis

| Round | Score | Delta | Status |
|-------|-------|-------|--------|
| Round 1 | 0.714 | — | REJECTED |
| Round 2 | 0.871 | +0.157 | REVISE |
| Round 3 | 0.873 | +0.002 | REVISE |

**Critical observation:** Round 3 shows near-zero improvement despite 9 SR-R2 fixes being applied. The reason: Round 2 fixes resolved Round 2 findings (the Round 2 score improvement will be realized when the current templates are scored against Round 2's baseline, not against Round 3's new findings). Round 3's adversarial strategies have identified NEW findings introduced by or revealed by Round 2's remediations, creating a finding "replenishment" pattern.

The two Major findings (IN-R3-001, IN-R3-003) constitute the dominant Methodological Rigor drag. If SR-R3-003 and SR-R3-004 are applied, Methodological Rigor would recover from 0.82 to approximately 0.89, yielding:

**Projected post-SR-R3-003/004 score:**
- Methodological Rigor: 0.89 × 0.20 = 0.178 (vs current 0.164)
- Remaining dimensions unchanged

Projected composite: 0.873 + (0.178 - 0.164) = 0.887 — still below 0.95

### Root Cause Analysis: Why Score Is Not Converging

The adversarial strategies continue to surface new findings at the same rate that prior rounds fix existing findings. This indicates a systemic pattern rather than a convergence toward quality:

**Root cause:** The templates have three structural sources of residual finding generation:
1. **Remediation propagation gaps** — fixes applied to one instance of a pattern but not all instances (CC-R3-001 TAP-03 gap, CC-R3-002 example placeholder gap, DA-R3-002 Since field gap)
2. **Framework-specific knowledge contamination** — templates embedded with Jerry-specific content (IN-R3-001 CLI examples)
3. **Tier language mismatches** — HARD-quality criteria expressed in MEDIUM ("should") language (IN-R3-003)

**Convergence path:** To reach 0.95, ALL three structural source patterns must be resolved. The SR-R3 recommendations address all three. Specifically:
- SR-R3-001, SR-R3-002, SR-R3-005 address propagation gaps (+0.05 on Internal Consistency: 0.84 → 0.89)
- SR-R3-003 addresses framework-specific contamination (+0.04 on Methodological Rigor)
- SR-R3-004 addresses tier language mismatch (+0.03 on Methodological Rigor)
- SR-R3-006, SR-R3-007, SR-R3-008 address remaining Minor findings (+0.02 across dimensions)

**Projected Round 4 composite with all SR-R3 applied:**
- Completeness: 0.92 × 0.20 = 0.184
- Internal Consistency: 0.89 × 0.20 = 0.178
- Methodological Rigor: 0.91 × 0.20 = 0.182
- Evidence Quality: 0.91 × 0.15 = 0.137
- Actionability: 0.92 × 0.15 = 0.138
- Traceability: 0.94 × 0.10 = 0.094

**Projected Round 4 score: 0.913 — still REVISE band**

### Threshold Gap Assessment

Reaching the 0.95 target requires a score increase of 0.077 from the current 0.873. The SR-R3 recommendations achieve approximately +0.04, leaving a remaining gap of ~0.037.

**Structural conclusion:** The 0.95 threshold for documentation templates may be aspirationally high for template-format artifacts (as opposed to content artifacts). Templates by nature include placeholder text and instructional comments that introduce qualitative ambiguity — the adversarial strategies will always surface new findings in placeholder interpretation and comment adequacy. A more calibrated threshold for template-format deliverables may be 0.90-0.92 (the standard quality gate threshold).

**Recommendation to orchestrator:** Consider whether the 0.95 threshold is appropriate for template-format deliverables or whether the standard 0.92 quality gate applies. If 0.92 is the operative threshold, the projected post-SR-R3 score (0.913) is one SR cycle from PASS.

### Verdict

**Round 3 Score: 0.873 — REVISE (0.85-0.91 band)**

The templates have improved substantially from Round 1 (0.714) and the Round 2 remediations were fully applied. However, new findings of Major severity (jerry-specific observable skill examples, R-01 MEDIUM language) and a pattern of remediation propagation gaps (SR-R2 fixes applied to one instance but not all) are holding the score below the convergence path.

**Round 4 readiness (if continued):** Apply SR-R3-001 through SR-R3-008 in priority order. SR-R3-003 (domain-agnostic examples) and SR-R3-004 (R-01 HARD language) are the critical-path items. Estimated post-SR-R3 score: 0.91-0.93.

**Threshold calibration question:** If the operative threshold for template-format deliverables is 0.92 (standard quality gate per H-13), Round 4 with full SR-R3 application is projected to PASS. If the threshold is 0.95, at least one additional round would be needed to address any new findings introduced by SR-R3 remediations.

---

## Execution Statistics

- **Total Findings:** 10
- **Critical:** 0
- **Major:** 2 (IN-R3-001, IN-R3-003)
- **Minor:** 8
- **Round 2 SR-R2 Recommendations Applied:** 9 of 9 (100%)
- **New Findings (Round 3):** 10
- **Findings From Prior Rounds Persisting:** 0 (all Round 2 Major findings resolved)
- **Finding Pattern:** Remediation-introduced (7 of 10 findings introduced by or revealed by Round 2 fixes)
- **S-007 Protocol Steps Completed:** 5 of 5
- **S-013 Protocol Steps Completed:** 6 of 6
- **S-002 Protocol Steps Completed:** 5 of 5
- **S-010 Protocol Steps Completed:** 8 recommendations produced
- **Score Trajectory:** 0.714 → 0.871 → 0.873 (diminishing returns pattern detected)

---

*Adversarial Review Round 3 executed by: adv-executor*
*Constitutional compliance: P-001 (evidence-based findings), P-002 (persisted), P-004 (provenance cited per finding)*
*H-16 note: S-002 executed without prior S-003 per user authority (H-02). Steelman position acknowledged and applied inline.*
*Round 2 SSOT: `projects/PROJ-013-diataxis/reviews/adversary-round2-templates.md`*
*Finding prefix sources: CC-NNN (s-007-constitutional-ai.md Identity), IN-NNN (s-013-inversion.md Identity), DA-NNN (s-002-devils-advocate.md Identity), SR-NNN (s-010-self-refine.md Identity)*
