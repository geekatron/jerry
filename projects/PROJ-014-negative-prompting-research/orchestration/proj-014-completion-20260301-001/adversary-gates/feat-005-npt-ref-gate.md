# Quality Score Report: NPT Pattern Reference

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, top action item |
| [Scoring Context](#scoring-context) | Deliverable metadata and scoring parameters |
| [Score Summary](#score-summary) | Weighted composite and threshold comparison |
| [Dimension Scores](#dimension-scores) | Per-dimension scores with evidence summaries |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement paths per dimension |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered fixes to reach threshold |
| [Leniency Bias Check](#leniency-bias-check) | Self-verification of scoring discipline |

---

## L0 Executive Summary

**Score:** 0.734/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.62)
**One-line assessment:** The Taxonomy Classification Reference section contains 5/7 incorrect technique type labels and the document redefines NPT-013 from "constitutional triplet" to a formatting pattern without noting the divergence -- fix these accuracy issues and the document can reach threshold.

---

## Scoring Context

- **Deliverable:** `skills/prompt-engineering/rules/npt-pattern-reference.md`
- **Deliverable Type:** Reference document / actionable lookup table for pe-constraint-gen agent
- **Criticality Level:** C4 (user-specified)
- **Quality Threshold:** 0.95 (user-specified C4 gate)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Source Taxonomy:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md`
- **Agent Governance YAML:** `skills/prompt-engineering/agents/pe-constraint-gen.governance.yaml`
- **A/B Testing Results:** `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md`
- **Scored:** 2026-03-01T21:00:00Z
- **Iteration:** 1 (first scoring)

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.734 |
| **Threshold** | 0.95 (user-specified C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (standalone scoring) |
| **Gap to Threshold** | 0.216 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.78 | 0.156 | Core NPT-009/NPT-013 sections complete; missing NPT-010/011/012 upgrade path guidance; no NPT-014 anti-pattern diagnostic |
| Internal Consistency | 0.20 | 0.62 | 0.124 | NPT-013 redefined from "constitutional triplet" to formatting pattern without noting divergence; A1-A7 labels wrong |
| Methodological Rigor | 0.20 | 0.72 | 0.144 | Pattern Selection Guide and Quality Criteria well-structured; Taxonomy Reference section not verified against source |
| Evidence Quality | 0.15 | 0.73 | 0.110 | NPT-009/NPT-013 evidence citations accurate; A/B test stats match source; Taxonomy Reference section inaccurate |
| Actionability | 0.15 | 0.87 | 0.131 | Decision table, format templates, XML wrapping, quality checklist all immediately usable by pe-constraint-gen |
| Traceability | 0.10 | 0.70 | 0.070 | Source paths, evidence references, PG-003 citation all present; NPT-013 redefinition untraced |
| **TOTAL** | **1.00** | | **0.734** | |

---

## Detailed Dimension Analysis

### Completeness (0.78/1.00)

**Evidence:**

The deliverable includes six well-organized sections: Pattern Selection Guide (5 context types with rationale), NPT-009 (format, template, 4 examples), NPT-013 (format, template, 3 examples), XML Wrapping Reference (3 contexts), Constraint Quality Criteria (5 checks with pass/fail examples), and Taxonomy Classification Reference (technique types and evidence tiers). Navigation table is H-23/H-24 compliant with anchor links.

**Gaps:**

1. **Missing NPT-010/011/012 upgrade path guidance.** The taxonomy establishes NPT-010 as an "EXTENSION of NPT-009" and NPT-011 as a "justified variant." The pe-constraint-gen agent needs to know when generating a plain NPT-009 constraint should be upgraded to NPT-010 (add positive alternative) or NPT-011 (add justification). The current reference provides no guidance on this progression.

2. **Missing NPT-014 anti-pattern coverage.** The taxonomy explicitly states NPT-014 should be used as a "diagnostic reference for identifying under-engineered constraints" in Phase 4 downstream. The pe-constraint-gen agent would benefit from a section on recognizing and upgrading NPT-014 patterns.

3. **Taxonomy Classification Reference is abbreviated.** Lists only A1-A7 type names and T1-T5 tier names without the pattern assignments that make the taxonomy navigable. For example, the source taxonomy maps NPT-006 to both A2 and A7, but the deliverable omits pattern-to-type assignments entirely.

**Improvement Path:**
- Add a "Pattern Upgrade Path" section showing NPT-014 -> NPT-009 -> NPT-010 -> NPT-011 progression with decision criteria
- Add a brief NPT-014 diagnostic section (what it looks like, how to upgrade it)
- Expand the Taxonomy Classification Reference with pattern assignments per type

### Internal Consistency (0.62/1.00)

**Evidence:**

Two significant consistency problems were identified:

**Problem 1: NPT-013 Semantic Redefinition**

The source taxonomy defines NPT-013 as "Constitutional Triplet: A mandatory set of minimum three prohibitions expressing the most safety-critical behavioral constraints" (taxonomy line 744). Its example shows `forbidden_actions` entries and `constitution.principles_applied` entries -- a structural pattern about the minimum set, not a formatting pattern.

The deliverable redefines NPT-013 as a formatting pattern: "NEVER {action} -- Consequence: {impact}. Instead: {alternative}" (line 73). This is actually the NPT-010 format ("Paired Prohibition with Positive Alternative" per taxonomy line 602). The deliverable explicitly says "What distinguishes NPT-013 from NPT-009: The `Instead:` alternative clause" (line 68), but in the taxonomy, NPT-010 is what adds the `Instead:` clause, not NPT-013.

This redefinition is not documented anywhere in the deliverable. There is no note explaining why the reference diverges from the taxonomy. The pe-constraint-gen agent would generate constraints labeled "NPT-013" that do not match what "NPT-013" means in the source taxonomy.

**Problem 2: Technique Type Label Mismatches (5/7 wrong)**

| Type | Deliverable Label | Source Taxonomy Label |
|------|------------------|----------------------|
| A1 | "Explicit Prohibition" | "Prohibition-only" |
| A2 | "Structured Prohibition (NPT-009)" | "Structured prohibition" (NPT-006, NPT-007, NPT-009, NPT-010) |
| A3 | "Conditional Restriction" | "Augmented prohibition" |
| A4 | "Enforcement-tier / Constitutional (NPT-013)" | "Enforcement-tier prohibition" (NPT-010, NPT-012, NPT-013) |
| A5 | "Scope Limitation" | "Programmatic enforcement" |
| A6 | "Error Prevention" | "Training-time constraint" |
| A7 | "Structured Negation" | "Meta-prompting" |

Five of seven labels are factually incorrect against the source taxonomy. A2 has the right name but lists only NPT-009 when the source includes NPT-006, NPT-007, and NPT-010.

**Problem 3: Evidence Tier Label Mismatches (3/5 wrong)**

| Tier | Deliverable Label | Source Taxonomy Label |
|------|------------------|----------------------|
| T2 | "Industry validated" | (empty in taxonomy; described as "established practitioner") |
| T3 | "Framework validated (>= 0.95 adversary gate)" | "Preprint / unreviewed" |
| T5 | "Theoretical" | "Session observation" |

T3 is the most consequential mismatch: the source taxonomy assigns T3 to arXiv preprints, while the deliverable redefines it as "Framework validated" -- an entirely different concept.

**Gaps:**

The NPT-013 redefinition and the taxonomy label mismatches create a situation where the pe-constraint-gen agent operates with a reference that contradicts its authoritative source. Any constraint generated and labeled "NPT-013" will not match what downstream consumers expect from the taxonomy.

**Improvement Path:**
- Fix all 7 technique type labels to match source taxonomy exactly
- Fix all 5 evidence tier labels to match source taxonomy exactly
- Either: (a) rename the deliverable's "NPT-013" formatting pattern to something else (e.g., "NPT-009+alt" or define it as a pe-constraint-gen operational variant), or (b) explicitly document the intentional redefinition with a divergence note and rationale

### Methodological Rigor (0.72/1.00)

**Evidence:**

The Pattern Selection Guide follows a rigorous decision table format with context, pattern, and rationale columns, plus a disambiguation decision rule (line 29). The Constraint Quality Criteria section provides a structured self-review checklist with binary pass/fail examples -- methodologically sound for a reference document. The NPT-009 and NPT-013 format specifications include precise component requirements (binary-testable action, single action per constraint, specific consequence). The XML Wrapping Reference correctly distinguishes 3 wrapping contexts.

**Gaps:**

1. **Taxonomy Reference section was not verified against source.** The 5/7 technique type mismatches and 3/5 evidence tier mismatches indicate the Taxonomy Classification Reference was composed without cross-referencing the source taxonomy. A rigorous methodology would have included a verification step for factual claims against the SSOT.

2. **No version linkage to taxonomy version.** The taxonomy catalog is at v3.0.0 (I3). The deliverable does not record which taxonomy version it was derived from, making future reconciliation difficult.

**Improvement Path:**
- Cross-reference all taxonomy labels against the source (lines 138-197 of the taxonomy catalog)
- Add a taxonomy version reference in the deliverable header or footer
- Add a self-review check for "all taxonomy labels verified against source SSOT"

### Evidence Quality (0.73/1.00)

**Evidence:**

The NPT-009 evidence citation ("T4 observational, 33 production instances, VS-001 through VS-004") is verified accurate against the source taxonomy (line 544). The NPT-013 evidence citation ("T4 observational, schema-mandatory, VS-004") matches the source (line 737). The A/B testing result "100% compliance vs 92.2% for positive-only framing (p=0.016)" is accurately traced to the go-no-go determination (go-no-go line 23: "100% compliance" for structured negation, "7.8% violation rate" for positive-only = 92.2% compliance). The PG-003 "CONDITIONAL GO" status and "convention-alignment rationale" qualifier accurately represent the go-no-go decision.

The deliverable appropriately preserves epistemic calibration: "Causal superiority over positive-only framing is UNTESTED" (line 137) aligns with the taxonomy's repeated disclaimers.

**Gaps:**

1. **Taxonomy Reference section evidence claims are inaccurate.** The redefined A1-A7 and T1-T5 labels create misleading evidence claims. A downstream consumer reading "T3 Framework validated (>= 0.95 adversary gate)" would understand something fundamentally different from the taxonomy's "T3 Preprint / unreviewed."

2. **No citation of the go-no-go determination path.** The A/B testing statistics are cited but the source document path is not provided for traceability.

**Improvement Path:**
- Fix all taxonomy labels to match source
- Add explicit path citation for go-no-go determination when citing A/B testing results
- Consider adding the key statistical parameters (McNemar exact, pooled n=90, Bonferroni-corrected alpha)

### Actionability (0.87/1.00)

**Evidence:**

This is the strongest dimension. The deliverable is purpose-built as an operational reference for pe-constraint-gen, and it succeeds in that regard:

1. **Pattern Selection Guide** (lines 21-29): Five context-to-pattern mappings with rationale, plus a decision rule. An agent can look up its context and immediately know which format to use.

2. **Format templates** (lines 40-42, 72-74): Precise placeholder-based templates that can be filled in mechanically.

3. **Examples** (lines 48-58, 81-89): Real examples from Jerry Framework agent definitions, not synthetic/hypothetical examples. The H-35 constitutional triplet examples are drawn from actual governance YAML.

4. **Quality Criteria** (lines 119-125): Five checks with pass/fail columns, immediately usable as a self-review checklist.

5. **XML Wrapping Reference** (lines 95-111): Three contexts with exact XML structures. Eliminates ambiguity about wrapping.

**Gaps:**

1. **No error recovery guidance.** When a generated constraint fails quality criteria, the reference does not suggest specific recovery actions beyond the general quality checks.

2. **Pattern upgrade guidance missing** (as noted in Completeness). When pe-constraint-gen recognizes an NPT-014 pattern in a target file, there is no upgrade procedure.

**Improvement Path:**
- Add a brief "Common Generation Failures" section with correction examples
- Add pattern upgrade procedure for NPT-014 -> NPT-009 -> NPT-010

### Traceability (0.70/1.00)

**Evidence:**

The deliverable provides several traceability links: source taxonomy path in frontmatter (line 4) and Taxonomy Classification Reference section (line 131); PROJ-014 status with TASK-025 reference in footer (line 141); PG-003 reference traceable to ADR-002 Sub-Decision 6; VS-001 through VS-004 evidence references; H-35 and H-15 rule references; pe-constraint-gen agent SSOT reference in footer (line 142).

**Gaps:**

1. **NPT-013 redefinition is untraced.** The most significant traceability gap: the deliverable redefines NPT-013 without any note explaining the divergence from the taxonomy. There is no "Divergence Note" or "Adaptation Note" section.

2. **No taxonomy version pinning.** The taxonomy catalog is v3.0.0. The deliverable does not record which version it was built against.

3. **Go-no-go determination path not cited.** The A/B testing statistics on line 66-67 lack a source path citation.

4. **agent-development-standards.md cross-reference incomplete.** The deliverable references H-35 but does not link to the specific section in agent-development-standards.md where NPT-009 format is defined for `forbidden_actions`.

**Improvement Path:**
- Add taxonomy version pin: "Built against taxonomy-pattern-catalog.md v3.0.0"
- Add divergence note if NPT-013 redefinition is intentional
- Add go-no-go determination source path
- Add agent-development-standards.md section reference for H-35/forbidden_actions format

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.62 | 0.90 | Fix all 7 technique type labels (A1-A7) to match source taxonomy exactly: A1=Prohibition-only, A2=Structured prohibition, A3=Augmented prohibition, A4=Enforcement-tier prohibition, A5=Programmatic enforcement, A6=Training-time constraint, A7=Meta-prompting |
| 2 | Internal Consistency | 0.62 | 0.90 | Fix all evidence tier labels: T2=empty (established practitioner), T3=Preprint/unreviewed, T5=Session observation |
| 3 | Internal Consistency | 0.62 | 0.90 | Resolve NPT-013 semantic divergence: either (a) rename the "constraint with Instead: clause" format to an operational variant name, or (b) add an explicit divergence note explaining why the reference redefines NPT-013 for pe-constraint-gen use |
| 4 | Completeness | 0.78 | 0.90 | Add pattern upgrade path section: NPT-014 -> NPT-009 -> NPT-010 -> NPT-011 with decision criteria for when to upgrade |
| 5 | Traceability | 0.70 | 0.85 | Add taxonomy version pin, go-no-go source path citation, and agent-development-standards.md section cross-reference |
| 6 | Evidence Quality | 0.73 | 0.88 | After fixing taxonomy labels (P1-P2), add pattern-to-type assignments in the Taxonomy Classification Reference so downstream consumers can navigate the taxonomy |
| 7 | Methodological Rigor | 0.72 | 0.88 | Add a self-review check: "All taxonomy labels verified against source SSOT" in the Constraint Quality Criteria section |
| 8 | Actionability | 0.87 | 0.92 | Add brief NPT-014 diagnostic section with recognition criteria and upgrade examples |

**Estimated post-revision score:** If priorities 1-5 are addressed, the composite should rise to approximately 0.88-0.92. Addressing all 8 priorities could reach 0.95+.

---

## Leniency Bias Check

- [x] Each dimension scored independently (Internal Consistency at 0.62 is not pulled up by Actionability at 0.87)
- [x] Evidence documented for each score (specific line references, cross-referenced against source taxonomy)
- [x] Uncertain scores resolved downward (Internal Consistency: considered 0.65 but chose 0.62 given severity of 5/7 type mismatches AND the NPT-013 redefinition; Traceability: considered 0.75 but chose 0.70 given untraced NPT-013 divergence)
- [x] First-draft calibration considered (this is a first draft; 0.734 composite is within the 0.65-0.80 first-draft range)
- [x] No dimension scored above 0.95 without exceptional evidence (highest is Actionability at 0.87)
- [x] Weighted composite verified: (0.78*0.20) + (0.62*0.20) + (0.72*0.20) + (0.73*0.15) + (0.87*0.15) + (0.70*0.10) = 0.156 + 0.124 + 0.144 + 0.1095 + 0.1305 + 0.070 = 0.734

---

*Scored by: adv-scorer | Strategy: S-014 (LLM-as-Judge) | SSOT: `.context/rules/quality-enforcement.md`*
*Source taxonomy verified: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md` (v3.0.0)*
*Agent governance YAML verified: `skills/prompt-engineering/agents/pe-constraint-gen.governance.yaml` (v1.0.0)*
*A/B testing results verified: `projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md`*
