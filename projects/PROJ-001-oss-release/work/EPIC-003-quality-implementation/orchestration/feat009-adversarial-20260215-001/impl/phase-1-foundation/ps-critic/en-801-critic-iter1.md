# EN-801 Critic Report -- Iteration 1

<!--
CRITIC: ps-critic (adversarial reviewer)
ENABLER: EN-801 (Template Format Standard)
FILE: .context/templates/adversarial/TEMPLATE-FORMAT.md
STRATEGIES: S-014 (LLM-as-Judge) + S-003 (Steelman)
DATE: 2026-02-15
ITERATION: 1
-->

> **Deliverable:** `.context/templates/adversarial/TEMPLATE-FORMAT.md`
> **Enabler:** EN-801 (Template Format Standard)
> **Strategies Applied:** S-014 (LLM-as-Judge), S-003 (Steelman)
> **Reviewer:** ps-critic (adversarial)
> **Criticality:** C3 (touches `.context/templates/`, defines format for quality framework templates)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Analysis (S-003)](#steelman-analysis-s-003) | Strongest version of the deliverable's argument |
| [LLM-as-Judge Scoring (S-014)](#llm-as-judge-scoring-s-014) | Per-dimension scoring with evidence |
| [Findings Table](#findings-table) | All findings with severity and dimension |
| [Finding Details](#finding-details) | Expanded description of Critical and Major findings |
| [Weighted Composite](#weighted-composite) | Final score calculation |
| [Verdict](#verdict) | PASS or REVISE determination |
| [Improvement Recommendations](#improvement-recommendations) | Prioritized actions if REVISE |

---

## Steelman Analysis (S-003)

Per H-16, steelman analysis precedes critique.

### Core Value Proposition

TEMPLATE-FORMAT.md establishes a single, authoritative format standard for all 10 adversarial strategy execution templates. This is a genuinely valuable contribution because:

1. **Structural consistency across 10 strategies.** Without a canonical format, each strategy template could drift into its own structure, making it difficult for consumers (both human and LLM) to navigate, compare, and apply strategies. The 8-section structure provides a predictable contract that every template must honor.

2. **SSOT alignment is thorough and correct.** The document consistently defers to `quality-enforcement.md` for all constants -- thresholds, weights, criticality levels, and strategy catalog data. Every constant I cross-referenced matches exactly. This is not trivial; it requires discipline to maintain traceability without accidental redefinition.

3. **Finding documentation is well-specified.** The finding format (ID, Finding, Severity, Evidence, Affected Dimension) with severity definitions (Critical/Major/Minor) and the requirement to map findings to scoring dimensions creates a closed loop between strategy execution and quality scoring. This is the kind of operational specificity that makes templates actually usable rather than aspirational.

4. **Criticality-based selection is properly encoded.** The Integration section (Section 8) includes the criticality-based selection table that matches the SSOT, ensuring templates know where they sit in the C1-C4 hierarchy.

5. **Self-consistency mechanisms.** The Validation Checklist provides a concrete mechanism for verifying template compliance. The "Constants Reference" section consolidates all referenced constants in one place while explicitly stating they are sourced from, not redefined by, this document.

6. **H-16 (Steelman before critique) is properly threaded.** The document references H-16 in Section 2 (Purpose, pairing recommendations), Section 3 (Prerequisites, ordering constraints), and Section 8 (Integration, H-16 compliance). This multi-point referencing ensures template authors cannot miss this constraint.

### What This Document Does Well

- Metadata is complete and well-structured (frontmatter, version, enabler reference)
- Navigation table is present (H-23) with anchor links (H-24)
- File naming convention is documented (`.context/templates/adversarial/{S-NNN}-{strategy-slug}.md`)
- Finding prefix assignments are unique (10 strategies, 10 distinct 2-letter prefixes)
- The step format template in Section 4 provides a concrete, copy-paste-ready skeleton
- The template notes in the HTML comment block (lines 332-355) provide useful instantiation guidance
- Evidence requirements in Section 5 (line 193-194) are specific: location, quotation/paraphrase, explanation

### Strongest Argument for the Deliverable

This document solves the "template drift" problem for adversarial strategy execution. By encoding both structural requirements (8 sections, specific fields) and content requirements (minimum counts, format templates, validation checklist), it creates a specification that is simultaneously prescriptive enough to ensure consistency and flexible enough to accommodate strategy-specific content (the Execution Protocol and Examples sections are strategy-specific by design). The explicit "MUST NOT redefine constants" principle prevents the most dangerous form of drift -- silent divergence from the SSOT.

---

## LLM-as-Judge Scoring (S-014)

### 1. Completeness (Weight: 0.20)

**Score: 0.90**

**Evidence supporting the score:**
- All 8 canonical sections are present and in the correct order (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration).
- The Strategy Catalog Reference table includes all 10 selected strategies with correct IDs, names, scores, and families.
- The Validation Checklist covers both structural and per-section content requirements.
- The Constants Reference consolidates quality gate, scoring dimensions, criticality levels, and relevant HARD rules.

**Gaps and weaknesses:**
- **Missing: Excluded strategies context.** The SSOT includes 5 excluded strategies (S-005, S-006, S-008, S-009, S-015) with reconsideration conditions. The template format document references "10 selected strategies from ADR-EPIC002-001" but does not mention the exclusions. While templates are only needed for selected strategies, a brief acknowledgment of excluded strategies would improve completeness and help template authors understand the full landscape.
- **Missing: Auto-Escalation Rules relevance.** The Constants Reference includes H-rules but does not reference Auto-Escalation rules (AE-001 through AE-006), despite the fact that AE-002 (touches `.context/rules/` = auto-C3) directly applies to the templates themselves (they live in `.context/templates/` but reference `.context/rules/`). The template notes mention "C3+ review (AE-002 applies)" but this is in an HTML comment, not in the document body.
- **Missing: Enforcement Architecture context.** The SSOT defines a 5-layer enforcement architecture (L1-L5). The template format does not explain where strategy execution templates fit within this architecture (they primarily serve L1 and L4). This is a minor gap but relevant for understanding the operational context.
- **Section 7 (Examples) is underspecified.** The format requires "at least one concrete example" but does not specify minimum complexity, expected length, or whether the example should demonstrate a passing or failing strategy execution. This leaves significant ambiguity for template authors.

### 2. Internal Consistency (Weight: 0.20)

**Score: 0.93**

**Evidence supporting the score:**
- All constants cross-referenced against `quality-enforcement.md` match exactly (strategy catalog, scoring dimensions, weights, criticality levels, quality gate threshold).
- The Validation Checklist in lines 266-283 is consistent with the section definitions in the body of the document.
- Finding prefix assignments are all unique and use a consistent 2-letter + NNN pattern.
- The "MUST NOT redefine" principle is stated at least 3 times (lines 49, 202, 210, 289) and consistently applied.

**Gaps and weaknesses:**
- **Minor inconsistency in threshold bands.** Section 6 (Scoring Rubric, line 208) defines three bands: PASS (>= 0.92), REVISE (0.85-0.91), ESCALATE (< 0.85). The SSOT does not define an "ESCALATE" band -- it says "Below threshold: Deliverable REJECTED; revision required per H-13." The introduction of "ESCALATE" as a category is a minor extension beyond the SSOT that could be seen as redefining behavior. While reasonable, it should be explicitly acknowledged as a template-specific extension rather than presented as sourced from quality-enforcement.md.
- **Section 6 says "from quality-enforcement.md, MUST NOT be redefined"** for the threshold bands, but the ESCALATE band IS a redefinition/extension. This creates a self-contradiction: the section claims to not redefine while simultaneously introducing a new band name.

### 3. Methodological Rigor (Weight: 0.20)

**Score: 0.88**

**Evidence supporting the score:**
- The 8-section structure is well-motivated and follows a logical progression: identify -> explain purpose -> check prerequisites -> execute -> format output -> score -> demonstrate -> integrate.
- The step format template (lines 136-149) provides a concrete, reproducible skeleton.
- The finding documentation format (lines 155-164) is well-structured with severity definitions.
- The validation checklist provides a systematic verification mechanism.

**Gaps and weaknesses:**
- **No versioning protocol for templates.** The format specifies a version field (Section 1) but does not define versioning rules: when to bump major/minor/patch, how to handle breaking changes to the format, how template versions relate to format versions. Since this document will govern 10+ templates over time, versioning methodology matters.
- **No conflict resolution procedure.** If a template author encounters a contradiction between this format and the SSOT, the document says to follow the SSOT (implied by "MUST NOT redefine"), but there is no explicit procedure for reporting and resolving such conflicts.
- **Validation checklist is manual.** The checklist uses markdown checkboxes but there is no mention of automated validation (L3/L5 enforcement layers). For a quality framework that emphasizes deterministic gating, relying solely on manual checklist review is a methodological weakness.
- **No guidance on template review process.** The document defines what templates must contain but not how they should be reviewed. Is template review subject to the same creator-critic-revision cycle (H-14)? The HTML comment mentions this (line 341-342) but the document body does not.

### 4. Evidence Quality (Weight: 0.15)

**Score: 0.91**

**Evidence supporting the score:**
- Every constant is explicitly sourced to `quality-enforcement.md`, `ADR-EPIC002-001`, or `ADR-EPIC002-002`.
- The traceability block in the HTML comment (lines 347-352) lists EN-801 through EN-809 and the source documents.
- The Constants Reference section (lines 287-328) provides a consolidated evidence base.

**Gaps and weaknesses:**
- **Source references are to document names, not specific sections or line numbers.** For example, "from quality-enforcement.md" appears multiple times but never says "from quality-enforcement.md, Strategy Catalog section, lines 142-155." This makes verification possible but slower than necessary.
- **HTML comments contain evidence that should be in the document body.** The traceability block (lines 332-355) contains important information about instantiation rules, validation process, maintenance, and traceability that is only visible in source view. If these templates are consumed by LLMs, the HTML comments may or may not be visible depending on the rendering context.

### 5. Actionability (Weight: 0.15)

**Score: 0.92**

**Evidence supporting the score:**
- The step format template (Section 4) is directly copy-paste-ready.
- The finding documentation format is a concrete table template.
- The scoring impact table (Section 5) provides a fill-in-the-blank structure.
- The validation checklist provides a concrete verification procedure.
- File naming convention is explicit and unambiguous.
- "Target length per template: 200-400 lines" provides a concrete sizing guideline.

**Gaps and weaknesses:**
- **No starter template or skeleton file.** While the format is well-described, there is no companion skeleton file (e.g., `TEMPLATE-SKELETON.md`) that a template author could copy and fill in. The current document describes the format but does not provide a single unified skeleton. This is a minor gap given the clarity of the descriptions, but a skeleton would significantly improve actionability.
- **Finding prefix assignments are documented but not the allocation process.** If a new strategy is added to the catalog in the future, there is no documented process for assigning a new finding prefix. This is low priority but relevant for long-term actionability.

### 6. Traceability (Weight: 0.10)

**Score: 0.92**

**Evidence supporting the score:**
- The enabler ID (EN-801) is documented in metadata and HTML comment.
- Source documents are referenced (quality-enforcement.md, ADR-EPIC002-001, ADR-EPIC002-002).
- The Constants Reference section provides bidirectional traceability between template constants and SSOT.
- The Relevant HARD Rules table (lines 319-328) maps HARD rules to their template relevance.

**Gaps and weaknesses:**
- **No link to the EPIC or FEAT that produced this deliverable.** The metadata says "SOURCE: EPIC-003 Quality Framework" but does not reference FEAT-009 or the specific orchestration that created it. Within the project's work tracking system, this makes it harder to trace back to the decision to create this deliverable.
- **Traceability of the 8-section structure itself is not documented.** Why these 8 sections? What requirement or analysis led to this specific structure? There is no reference to a design decision or analysis that motivated the section selection.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| LJ-001 | ESCALATE band (< 0.85) in Section 6 is not in SSOT; introduced as if sourced from SSOT | Major | Lines 202-208: "from quality-enforcement.md, MUST NOT be redefined" but ESCALATE is a new category | Internal Consistency |
| LJ-002 | Traceability block and instantiation guidance hidden in HTML comments, not in document body | Major | Lines 332-355: critical operational guidance only in HTML comment | Evidence Quality, Actionability |
| LJ-003 | No versioning protocol for format or template updates | Major | Section 1 requires version field but no rules for when/how to version | Methodological Rigor |
| LJ-004 | No automated validation pathway referenced; checklist is manual only | Minor | Lines 260-283: manual checkboxes; no L3/L5 enforcement mentioned | Methodological Rigor |
| LJ-005 | Excluded strategies not mentioned in document body | Minor | SSOT lists 5 excluded strategies; template format omits them entirely | Completeness |
| LJ-006 | Auto-Escalation Rules not referenced in document body | Minor | AE-002 applies to these templates; mentioned only in HTML comment | Completeness |
| LJ-007 | No conflict resolution procedure for SSOT contradictions | Minor | Implied by "MUST NOT redefine" but no explicit procedure | Methodological Rigor |
| LJ-008 | Section 7 (Examples) underspecified on complexity and scope | Minor | "at least one concrete example" with no minimum quality bar | Completeness |
| LJ-009 | No starter skeleton template provided | Minor | Format described but no companion skeleton file | Actionability |
| LJ-010 | Source references lack section/line specificity | Minor | "from quality-enforcement.md" without section references | Traceability |

---

## Finding Details

### LJ-001 (Major): ESCALATE Band Self-Contradiction

**Location:** Section 6: Scoring Rubric, lines 202-208.

**Content:** The section header states "Threshold Bands (from quality-enforcement.md, MUST NOT be redefined)" and then presents three bands: PASS (>= 0.92), REVISE (0.85-0.91), ESCALATE (< 0.85).

**Problem:** The SSOT (`quality-enforcement.md`) does not define three named bands. It states: "Threshold: >= 0.92 weighted composite score (C2+ deliverables)" and "Below threshold: Deliverable REJECTED; revision required per H-13." The SSOT uses "REJECTED" for below-threshold, not "ESCALATE." The introduction of "REVISE" and "ESCALATE" as named bands, while operationally reasonable, constitutes a redefinition -- which directly contradicts the "MUST NOT be redefined" claim in the same section.

**Recommendation:** Either (a) align the bands exactly with SSOT language (PASS >= 0.92, REJECTED < 0.92), or (b) explicitly acknowledge the named bands as a template-format extension beyond the SSOT with a note like: "Note: REVISE and ESCALATE are template-specific operational categories not defined in the SSOT. The SSOT defines only the 0.92 threshold with REJECTED as the below-threshold outcome."

### LJ-002 (Major): Critical Guidance in HTML Comments

**Location:** Lines 332-355 (HTML comment block at end of file).

**Content:** The HTML comment contains four subsections -- INSTANTIATION, VALIDATION, MAINTENANCE, and TRACEABILITY -- that provide operationally critical information:
- Instantiation rules (placeholders, which sections are strategy-specific, which constants are never modified)
- Validation integration with H-14 (creator-critic-revision cycle)
- Maintenance requirements (C3+ review, AE-002)
- Traceability map (EN-801 through EN-809, source documents)

**Problem:** HTML comments are not reliably visible in all rendering contexts. More importantly, the MAINTENANCE note that "changes require C3+ review (AE-002 applies)" is operationally important and should be in the document body. The TRACEABILITY map linking EN-801 through EN-809 is essential for understanding the deliverable landscape and should not be hidden.

**Recommendation:** Move the INSTANTIATION, MAINTENANCE, and TRACEABILITY content into a new "Template Instantiation Guide" section or an expanded "Overview" section in the document body. The HTML comment can retain brief notes, but operationally critical content belongs in the visible document.

### LJ-003 (Major): No Versioning Protocol

**Location:** Section 1 (Identity), line 87-88.

**Content:** The Identity section requires a "Version" field (semantic version) and a "Date" field, but there is no guidance on versioning rules.

**Problem:** This format document will govern 10 strategy templates. When the format changes (e.g., a new required section is added), all 10 templates must be updated. Without a versioning protocol, there is no mechanism to: (a) signal breaking format changes vs. additive ones, (b) track which templates conform to which format version, (c) determine when templates need re-validation.

**Recommendation:** Add a "Versioning Protocol" subsection to the Overview that defines: major version = breaking structural changes (new required sections, removed sections); minor version = additive changes (new optional fields, clarifications); patch version = typo fixes. Include a rule: "When the format major version increments, all templates MUST be re-validated against the new format within one development cycle."

---

## Weighted Composite

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.90 | 0.180 |
| Internal Consistency | 0.20 | 0.93 | 0.186 |
| Methodological Rigor | 0.20 | 0.88 | 0.176 |
| Evidence Quality | 0.15 | 0.91 | 0.1365 |
| Actionability | 0.15 | 0.92 | 0.138 |
| Traceability | 0.10 | 0.92 | 0.092 |
| **TOTAL** | **1.00** | -- | **0.9085** |

**Weighted Composite Score: 0.909**

---

## Verdict

**REVISE** (close to threshold)

The deliverable scores 0.909, which falls in the 0.85-0.91 range -- close to the 0.92 threshold but not yet passing. The document demonstrates strong SSOT alignment and thorough structural design, but three Major findings must be addressed:

1. The ESCALATE band self-contradiction (LJ-001) undermines internal consistency
2. Critical operational guidance hidden in HTML comments (LJ-002) weakens evidence quality and actionability
3. Missing versioning protocol (LJ-003) is a methodological gap for a format standard that will govern 10+ documents

Addressing these three Major findings would likely raise the score above 0.92. The Minor findings are improvement opportunities but would not individually block acceptance.

---

## Improvement Recommendations

Prioritized by impact on weighted composite score:

### Priority 1: Fix ESCALATE Band (LJ-001) -- Impact: Internal Consistency +0.02-0.03

Either align threshold bands with SSOT language or explicitly acknowledge the extension. The current self-contradiction ("MUST NOT be redefined" + introduces new band) is the most direct consistency violation.

**Suggested fix:** Change the Scoring Rubric bands to:
- PASS: >= 0.92 (accepted)
- REVISE: 0.85-0.91 (revision required, close to threshold)
- REJECTED: < 0.85 (revision required per H-13, significant gaps)

And add a note: "The SSOT defines the 0.92 threshold and REJECTED outcome. The REVISE band is a template-specific operational subdivision to distinguish near-threshold from far-below-threshold deliverables."

### Priority 2: Move Critical Content from HTML Comments (LJ-002) -- Impact: Evidence Quality +0.02, Actionability +0.01

Create a visible section (e.g., "Template Instantiation Guide" or expand "Overview") containing:
- Instantiation rules (placeholder replacement, strategy-specific sections, immutable constants)
- Maintenance requirements (AE-002, C3+ review)
- Traceability map (EN-801 through EN-809)

### Priority 3: Add Versioning Protocol (LJ-003) -- Impact: Methodological Rigor +0.02-0.03

Add a subsection to Overview defining:
- Semantic versioning rules for the format (major/minor/patch criteria)
- Template re-validation requirement on major version changes
- Format-to-template version compatibility tracking

### Priority 4 (Optional): Acknowledge Excluded Strategies (LJ-005) -- Impact: Completeness +0.01

Add a brief note in Strategy Catalog Reference: "5 strategies were excluded from the catalog (S-005, S-006, S-008, S-009, S-015). See quality-enforcement.md Strategy Catalog for exclusion rationale. No templates are required for excluded strategies."

### Priority 5 (Optional): Reference Auto-Escalation Rules (LJ-006) -- Impact: Completeness +0.01

Add AE-002 to the Constants Reference section: "AE-002: Changes to `.context/rules/` or `.context/templates/` require C3+ review."

---

## Scoring Impact Summary

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | Missing excluded strategies context, AE rules, enforcement architecture context, underspecified Examples section |
| Internal Consistency | 0.20 | Negative | ESCALATE band self-contradiction (LJ-001) is the primary drag on this dimension |
| Methodological Rigor | 0.20 | Negative | No versioning protocol, no conflict resolution, manual-only validation, no review process guidance |
| Evidence Quality | 0.15 | Negative | Critical guidance in HTML comments, source references lack specificity |
| Actionability | 0.15 | Positive | Strong step format template, finding format, validation checklist; minor gap on skeleton file |
| Traceability | 0.10 | Positive | Good SSOT alignment, Constants Reference, HARD rule mapping; minor gaps on FEAT/EPIC linkage |

---

<!--
CRITIC METADATA:
- Enabler: EN-801
- File reviewed: .context/templates/adversarial/TEMPLATE-FORMAT.md (356 lines)
- SSOT verified: .context/rules/quality-enforcement.md (176 lines)
- Strategies applied: S-003 (Steelman), S-014 (LLM-as-Judge)
- Findings: 3 Major, 7 Minor
- Weighted composite: 0.909
- Verdict: REVISE (close to threshold, 0.011 below)
- Estimated revision effort: Small (address 3 Major findings)
- Expected post-revision score: 0.93-0.95
-->
