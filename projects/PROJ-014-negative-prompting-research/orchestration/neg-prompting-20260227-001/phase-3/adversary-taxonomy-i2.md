# Quality Score Report: Negative Prompting Taxonomy and Pattern Catalog (v2.0.0, I2)

## L0 Executive Summary

**Score:** 0.938/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Actionability (0.88)
**One-line assessment:** The I2 revision resolves all 4 Critical and all 11 Major I1 findings with structural depth; the document approaches threshold but three residual gaps — one in traceability mechanics, one in actionability completeness, and one newly introduced internal consistency issue — prevent PASS at the C4 >= 0.95 bar.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md`
- **Deliverable Type:** Research Synthesis (Phase 3 Taxonomy)
- **Criticality Level:** C4
- **Quality Threshold:** >= 0.95 (C4, per orchestration directive)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **I1 Score:** 0.845 (REJECTED)
- **This Iteration:** I2
- **Scored:** 2026-02-28
- **Special Verification:** Barrier 2 ST-5 Phase 3 Gate Checks GC-1, GC-2, GC-3

---

## Special Verification Results (Barrier 2 ST-5)

| Gate Check | Requirement | Verdict | Evidence Location |
|------------|-------------|---------|------------------|
| **GC-1** | Taxonomy MUST NOT imply directional verdict at ranks 9–11 | **PASS** | L0 Executive Summary: "NEVER use this taxonomy to imply a directional verdict." NPT-009 Known Limitations: "NEVER claim NPT-009 is experimentally validated as superior to a structurally equivalent positive alternative." NPT-010 When NOT to use: "NEVER treat NPT-010 as validated over NPT-009-only." NPT-011 Known Limitations: "No T1 controlled comparison." All entries consistently apply the UNTESTED label. |
| **GC-2** | C1–C7 pilot condition mapping MUST be preserved or impact assessment provided | **PASS** | C1–C7 Condition Alignment Matrix is fully populated with alignment verdict "PRESERVED" explicitly stated. All 7 conditions mapped. No hierarchy modifications made in any entry-level field. DA-001 resolution adds a Prospective Validity Note to Origin and Scope Disclosure that explicitly addresses what would change if ranks 5–11 were reordered — this exceeds the "impact assessment provided" requirement. |
| **GC-3** | Rank 12 MUST be distinguished from ranks 9–11 with confidence labels | **PASS** | NPT-007 Causal Confidence: HIGH. NPT-014 Causal Confidence: HIGH (for the specific finding that standalone blunt prohibition underperforms). NPT-009 Causal Confidence: LOW (UNTESTED vs. positive equivalent). NPT-010, NPT-011 Causal Confidence: UNTESTED. Separate catalog entries with distinct IG-002 type designations (Type 1 vs. Type 2 extended). |

**Overall gate check result:** All three Phase 3-specific requirements are satisfied in the v2.0.0 revision.

---

## Critical and Major Finding Resolution Verification

### Critical Findings (4 of 4)

**DA-001 — Prospective validity of hierarchy as experimental scaffolding:**
RESOLVED. A new "Prospective Validity Note" subsection is added to Origin and Scope Disclosure (lines 77–85 of the document). The subsection explicitly addresses what would change in the C1–C7 mapping if ranks 9–11 reorder, if rank 6 drops below rank 9, and if external validation introduces a rank 7 occupant. The statement "NEVER treat the C1–C7 condition assignments as immutable prior to external validation of the hierarchy" and the MUST reassessment trigger are present. The resolution exceeds the I1 recommendation.

**FM-001 — Cross-reference matrix strips T1 evidence scope:**
RESOLVED. A "T1 Scope" row has been added to the Full Pattern Cross-Reference Matrix. Each cell specifies the exact construct covered at T1 (e.g., NPT-005: "Negation accuracy only (NOT compliance, NOT hallucination rate)"; NPT-006: "Compliance rate only (NOT hallucination, NOT long-context)"; NPT-007/014: "Underperformance established (NOT: expert users, all domains, all model generations)"). The row directly addresses the FMEA failure mode where downstream analysts using the matrix alone would overestimate evidence quality. An "FM-001 addition" annotation is also present in each affected pattern entry under "T1 Scope."

**IN-001 — Evidence scope constraints not surfaced in lookup tools:**
RESOLVED. A bold critical usage warning block is present at the Full Pattern Cross-Reference Matrix header and the Downstream Reference Index header. The matrix warning states: "NEVER use this matrix as a standalone decision guide. Evidence scope constraints present in the full pattern entries are NOT reproduced here... NEVER extract rows from this matrix without reading the corresponding full pattern entry." This directly implements the IN-001 recommendation.

**RT-001 — Cross-reference matrix exploitable for premature causal claims:**
RESOLVED. The critical usage warning at the Cross-Reference Matrix header explicitly states: "'Use for enforcement tier?' reflects observational evidence only — it does NOT imply experimental validation of negative framing over positive equivalents. All rows marked T4 have UNTESTED causal comparison status." This directly closes the primary exploitation vector identified in RT-001. The "Use for enforcement tier?" column entries have also been updated to include "(T4 obs, UNTESTED causal)" qualifiers inline.

### Major Findings (11 of 11)

**SM-001 (Rank 7 unoccupied):** RESOLVED. "Rank 7 gap note" added to L0 Executive Summary with explicit reasoning for why rank 7 is not occupied (no technique warrants rank 7 without either reordering existing ranks or introducing a rank lacking distinguishing evidence). The note frames the gap as "honest evidence coverage, not a cataloging error."

**SR-004 (Braun & Clarke methodological misrepresentation):** RESOLVED. The frontmatter now states "Deductive framework extension" as the methodology. A dedicated "Methodology Subsection" has been added with explicit sections for Method Applied, What Braun & Clarke Was NOT Applied To, and Source Inputs and Their Role. This is one of the most significant structural improvements in v2.0.0.

**CC-001 (14 patterns overcounts distinct techniques):** RESOLVED. L0 now states "14 named patterns (13 distinct techniques — NPT-007 and NPT-014 are dual entries for the same Type 1 blunt prohibition technique)." A "Dual-entry design rationale" section is present in the Pattern Catalog preamble explaining the NPT-007/NPT-014 distinction.

**DA-002 (Confidence label conflation):** RESOLVED. Every pattern entry now uses two separate fields: "Observational Confidence" and "Causal Confidence." The Cross-Reference Matrix contains both rows. The distinction is structurally visible rather than only lexically distinguishable. All T4 patterns (NPT-009 through NPT-013) consistently present Observational Confidence as HIGH or MEDIUM and Causal Confidence as LOW, UNTESTED, or construct-scoped.

**DA-003 ("Orthogonal" claim inaccurate):** RESOLVED. "Three orthogonal classification dimensions" replaced with "three classification dimensions providing independent analytical perspectives." A note on structurally impossible combinations is present in the Taxonomy Classification Dimensions introduction. The Dimension A table includes a note on multi-type assignments (NPT-010, NPT-012) explaining these reflect simultaneous structural operation at multiple levels rather than exclusive membership.

**PM-001 (Prospective constraint design missing):** RESOLVED. A "Design new behavioral constraints (prospective)" row has been added to the Downstream Reference Index with UNTESTED caveats and a structural checklist: (1) Is the failure mode specific and documentable? → NPT-009. (2) Is a positive alternative unambiguous? → add NPT-010 element. (3) Does the rationale help define edge cases? → add NPT-011 element. The CAVEAT explicitly states: "whether equivalent positive framing would achieve equal results is UNTESTED."

**PM-002 (Citation requirements unspecified):** RESOLVED. A "Citation requirement (PM-002 resolution)" note is present after the Practitioner Guidance Summary table. A dedicated "Constraint Propagation Requirement" section is present in PS Integration with a downstream checklist specifying NEVER directives for each NPT pattern when cited.

**FM-002 (Context compaction risk rationale missing):** RESOLVED. An explanatory note has been added to NPT-006 Known Limitations: "Context compaction risk note: The 'Low' context compaction risk rating assigned to NPT-006 in the Cross-Reference Matrix requires explanation... this is a design hypothesis, not empirically verified." The matrix cell for NPT-006 now reads "Low (design inference, not empirically established)."

**IN-002 (UNTESTED label absent from matrix):** RESOLVED. A "Causal comparison tested?" row has been added to the Full Pattern Cross-Reference Matrix. NPT-009 through NPT-013 all show "No." NPT-005, NPT-006, NPT-007/014 show "No" or scoped "No" with the specific construct noted. This directly surfaces UNTESTED status in the primary lookup tool.

**RT-002 (Practitioner guidance extractable without confidence labels):** RESOLVED. A critical extraction warning block has been added to the Practitioner Guidance Summary header: "NEVER extract these guidance items without co-citing the Confidence column. MEDIUM confidence items are working practice only and are NOT validated recommendations."

**RT-003 (ST-5 constraint propagation unaddressed):** RESOLVED. A "Constraint Propagation Requirement" section is present in PS Integration with a downstream checklist requiring downstream documents to co-cite T4 observational, UNTESTED causal comparison, scope constraints, and schema-mandatory labels for each NPT pattern.

### Minor Findings (12 of 12)

All 12 minor findings have been addressed as documented in the Revision Log. SM-002, SM-003, SR-001, SR-002, SR-003, SR-005, CC-002, CC-003, PM-003, CV-001, CV-002, and FM-003 are each verified through specific changes visible in the document. NEVER use the self-review checklist's self-reported PASS status alone as verification — the above assessment is based on direct content examination.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.938 |
| **Threshold** | 0.95 (H-13, C4) |
| **Verdict** | REVISE |
| **Prior Score (I1)** | 0.845 |
| **Score Delta** | +0.093 |
| **Strategy Findings Incorporated** | Yes — I1 findings report (adversary-taxonomy-i1.md) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.190 | All 14 patterns cataloged; all required sections present; DA-001 prospective validity note present; prospective constraint design row in index |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Orthogonality claim corrected; extended rank designation clarified; methodology label corrected; residual SM-003 multi-type assignment creates one new tension |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | Braun & Clarke replaced with accurate deductive framework extension; full methodology subsection added; context compaction risk rationale added; confidence label structure split into two fields |
| Evidence Quality | 0.15 | 0.96 | 0.144 | T1 Scope row in matrix; T1 scope annotations in each pattern entry; causal vs. observational confidence split throughout; evidence scope constraints surfaced in all lookup tools |
| Actionability | 0.15 | 0.88 | 0.132 | Downstream index warnings present; prospective design row added; multi-pattern interaction caveat added; residual gap: constraint propagation checklist is present but provides no mechanism for Phase 5 to detect propagation failures |
| Traceability | 0.10 | 0.94 | 0.094 | SR-001 version reference added; ST-5 inheritance chain documented; constraint propagation requirement in PS Integration; residual gap: propagation mechanism is advisory checklist, not a structural enforcement mechanism |
| **TOTAL** | **1.00** | | **0.938** | |

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**
The v2.0.0 revision achieves near-complete coverage across all required dimensions. All 14 pattern entries are fully specified with the new FM-001 T1 Scope annotations, dual Observational/Causal Confidence fields, and updated Known Limitations sections. All required sections from the orchestration directive are present and populated: L0 Executive Summary, Origin and Scope Disclosure, Methodology Subsection (new in v2.0.0), L1 Full Taxonomy, Taxonomy Classification Dimensions, IG-002 Taxonomy Integration, Pattern Catalog Entries, L2 Evidence Tables, C1–C7 Condition Alignment Matrix, Evidence Gap Map, Full Pattern Cross-Reference Matrix, Downstream Reference Index, Practitioner Guidance Summary, PS Integration, Self-Review Checklist, and Revision Log. The DA-001 resolution adds a Prospective Validity Note that explicitly addresses what-if scenarios for rank reordering. PM-001 resolution adds the prospective constraint design row. PM-003 resolution adds the NPT-007/NPT-014 merged Phase 5 priority note.

**Gaps:**
The NPT-014 Evidence Gap Map Phase 5 Priority cell reads "HIGH — C2 baseline condition (merged priority with NPT-007: same technique, same Phase 5 role)" with a note below the table. The merge is documented but the row itself still appears for NPT-014 — a reader scanning the gap map column still sees two HIGH entries before reaching the note. This is a minor presentation issue, not a structural gap. No major completeness gaps are identified.

**Improvement Path:**
To reach 1.00, the NPT-014 Evidence Gap Map row could be merged into the NPT-007 row visually (e.g., "NPT-007 / NPT-014" as a single row), eliminating any residual double-counting appearance. This is cosmetic. The 0.95 score reflects that all substantive completeness requirements are met.

---

### Internal Consistency (0.92/1.00)

**Evidence:**
The v2.0.0 revision corrects the primary consistency issues from I1: the "orthogonal" claim is replaced throughout with "independent analytical perspectives"; the Braun & Clarke methodology claim is removed and corrected; NPT-012 "extended" rank designation is clarified as a mechanism extension in the IG-002 Integration section; T2 tier status is explained; NPT-007/NPT-014 dual-entry is made explicit in the L0 and Pattern Catalog preamble. The Dimension A table now includes a note on multi-type assignments for NPT-010 and NPT-012.

**Gaps:**
One residual consistency issue is present that was partially addressed (SM-003) but not fully resolved. The Dimension A table still includes NPT-010 in BOTH A3 and A4 rows: "A3: Augmented prohibition ... NPT-008, NPT-011, NPT-012" and "A4: Enforcement-tier prohibition ... NPT-010, NPT-012, NPT-013." The resolution note states "some patterns span multiple Dimension A types" and the table reflects "primary and secondary classifications rather than exclusive membership." However, the NPT-010 individual entry states "Technique Type: A3 (Augmented prohibition) and A4 (Enforcement-tier — when deployed in a tier architecture)" — this is now consistent with the table, which is an improvement. The remaining inconsistency is that the note on multi-type patterns is present in the Dimension A table introduction but is not repeated in the NPT-010 entry itself where the dual assignment is stated. A reader arriving at NPT-010 without having read the Dimension A introduction could still be confused.

Additionally, a newly introduced minor tension exists in the Dimension B Evidence Tier table. The table header in v2.0.0 includes a T2 row noting "None (absorbed into T4 in this taxonomy)" with a T2 note explaining the merger. This is consistent with the SR-003 fix recommendation. However, the T2 note references "vendor documentation examined (Claude Code rule files, OpenAI system prompt design docs, LlamaIndex documentation) functions as direct observation evidence rather than as prescriptive methodology published for external consumption." This explanation is sound but not cross-referenced from the individual pattern entries for NPT-009 through NPT-013 that cite VS-001–VS-004 — a reader checking why T4 (not T2) is used for VS-001–VS-004 evidence must navigate back to the Dimension B table note. This is a navigation gap, not an inconsistency per se.

**Improvement Path:**
Add the multi-type note from the Dimension A table directly to NPT-010's Technique Type field: "A3 and A4 — see multi-type assignment note in Dimension A table." This cross-reference eliminates the navigation gap that remains after SM-003 resolution. The Internal Consistency score of 0.92 reflects a well-addressed revision with one remaining navigational inconsistency.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**
The SR-004 resolution is the most significant methodological improvement in v2.0.0. The dedicated Methodology Subsection accurately describes the deductive framework extension approach in four numbered steps: starting framework, deductive pattern assignment, gap identification, and the explicit statement that no inductive thematic coding was performed. The subsection explicitly explains why "Braun & Clarke (2006) was NOT Applied To" this taxonomy, distinguishing Phase 3's deductive role from earlier phases' potentially inductive work. This correction substantially raises methodological integrity. The Source Inputs and Their Role table in the Methodology Subsection provides a clean role-by-role accounting of how each upstream document contributed to the taxonomy construction — this is methodologically rigorous and exceeds the I1 recommendation.

The DA-002 resolution (split Observational/Causal Confidence fields) is also a significant methodological improvement: the two-dimensional confidence scheme is now structurally enforced in every pattern header and cross-reference matrix row rather than relying on lexical parsing of a single "Confidence Level" field.

The FM-002 resolution adds explicit methodology to the context compaction risk ratings in NPT-006: "design hypothesis, not empirically verified." The cross-reference matrix cell reads "Low (design inference, not empirically established)." This is honest about the rating's epistemic basis.

**Gaps:**
No Critical or Major methodological gaps remain. One minor gap: the context compaction risk rationale fix applies only to NPT-006 (where "Low" is the non-obvious rating). NPT-009 and NPT-010 receive "HIGH" ratings without the same explicit methodology note — but HIGH compaction risk for single NEVER rules is more intuitively grounded and less likely to mislead. The absence of a symmetric rationale note for HIGH ratings is a SOFT issue, not a MEDIUM.

**Improvement Path:**
Add a brief footnote to the "Context compaction risk?" row in the Cross-Reference Matrix noting that HIGH ratings reflect the T-004 failure mode analysis, and LOW ratings reflect design inference (not empirical study). This symmetric treatment would raise this dimension to 0.97+.

---

### Evidence Quality (0.96/1.00)

**Evidence:**
The FM-001 T1 Scope row is the highest-impact evidence quality improvement in v2.0.0. Each cell in the cross-reference matrix now specifies exactly what construct the T1 evidence covers: NPT-005 "Negation accuracy only (NOT compliance, NOT hallucination rate)"; NPT-006 "Compliance rate only (NOT hallucination, NOT long-context)"; NPT-007/014 "Underperformance established (NOT: expert users, all domains, all model generations)." Patterns with no T1 evidence correctly show "No T1."

The FM-001 T1 Scope annotations are also present in each individual pattern entry as "T1 Scope (FM-001 addition)" fields, creating consistency between the matrix summary and the detailed entry. This is methodologically sound evidence documentation.

The Causal Confidence row in the Cross-Reference Matrix correctly shows "LOW (UNTESTED vs. positive equivalent)" for NPT-009, "UNTESTED" for NPT-010/011/013, and "LOW (UNTESTED vocabulary contribution)" for NPT-012. These distinctions are precise and consistent with the individual entries.

The SR-005 resolution for A-23 venue confirmation adds the provenance note: "Venue confirmed via ACL Anthology 2025.findings-emnlp.761; verification provenance: internal pipeline confirmation — external venue verification not re-performed within this synthesis." This is an honest disclosure of verification depth.

**Gaps:**
The CV-001 "33 instances" count remains unverified within this synthesis as documented — the resolution is a documentation note ("count sourced from supplemental-vendor-evidence.md VS-001; not independently re-verified within this synthesis"), not a re-verification. This is appropriate for a T4 observational claim and was classified as "Document" only in I1. It is not a gap in the scoring sense.

One minor residual: the NPT-007 Evidence Base still describes A-20 as establishing "prohibition-style instructions fail at baseline rates; blunt prohibitions are among the least reliable constraint forms." The phrase "among the least reliable" is comparative but the comparison group is not named. This is a very minor phrasing issue, not a scope misrepresentation.

**Improvement Path:**
To reach 1.00, the A-20 evidence description in NPT-007 could be made more precise: "blunt prohibitions underperform structured alternatives in instruction-following tasks" (comparison group named). The 0.96 score reflects the strongest evidence quality dimension in the document.

---

### Actionability (0.88/1.00)

**Evidence:**
The v2.0.0 revision substantially improves actionability over v1.0.0. The PM-001 resolution adds the prospective constraint design row to the Downstream Reference Index — the most operationally important addition for Phase 4 practitioners. The row includes a structural checklist: (1) failure mode specific and documentable → NPT-009; (2) positive alternative unambiguous → add NPT-010; (3) rationale helps define edge cases → add NPT-011. The UNTESTED caveat is present throughout.

The critical usage warnings on both the Cross-Reference Matrix and Downstream Reference Index are operationally protective: they direct Phase 4 agents to full pattern entries before making design decisions. The Constraint Propagation Requirement checklist in PS Integration gives downstream Phase 4 and Phase 5 agents explicit NEVER directives for each pattern.

The FM-003 resolution adds "NEVER assume combined patterns are simply additive" to the Downstream Reference Index warning, addressing the multi-pattern interaction effects gap.

**Gaps:**
The Actionability score does not reach 0.92+ for two reasons.

First, the Constraint Propagation Requirement in PS Integration is a checklist that downstream agents must voluntarily apply. There is no structural mechanism that enforces propagation — no schema field, no required frontmatter, no worktracker enforcement. The checklist reads "Downstream documents MUST NOT cite NPT-009 through NPT-013 without the accompanying..." but the enforcement is entirely at the honor system level. For a C4 deliverable with 0.95 threshold requirements, the absence of a verifiable enforcement hook is a meaningful gap. This is not a newly introduced gap — it is an inherent limitation of the PM-002/RT-003 fix approach — but it limits actionability for the specific task of ensuring downstream documents honor the constraint propagation requirement.

Second, the prospective constraint design row (PM-001 fix) provides a structural checklist but does not address the scenario where Phase 4 analysis encounters a constraint that was previously stated positively and a stakeholder asks whether to convert it to negative framing. The row correctly says this comparison is UNTESTED and cannot be guided by the taxonomy, but this answer closes the Phase 4 use case rather than guiding it. A Phase 4 agent encountering this scenario has no actionable path forward from the taxonomy. This is epistemically honest and structurally correct — the taxonomy CANNOT provide this guidance without Phase 5 results — but it means the actionability for this specific Phase 4 task is zero from the taxonomy's perspective. The score reflects that actionability for the defined scope (retrospective audit + prospective structural checklist) is strong, but actionability for the framing choice itself (the most operationally relevant question) remains explicitly deferred.

**Improvement Path:**
To raise Actionability above 0.92:
1. Add a schema hook to the worktracker entry requiring downstream Phase 4 artifacts to declare "constraint_propagation_checked: true" with a link to the checklist. This would create a verifiable enforcement point for the propagation requirement.
2. Add a brief section to the Downstream Reference Index explaining that Phase 5 results will close the framing-choice gap and providing a placeholder for Phase 5 result integration (e.g., "When Phase 5 completes, this row will be updated with the experimental verdict on negative vs. positive framing").

---

### Traceability (0.94/1.00)

**Evidence:**
The SR-001 resolution adds "(R4, 0.953 PASS, 2026-02-27)" to the AGREE-5 reference in the Origin and Scope Disclosure, creating full version traceability for the foundational hierarchy. The frontmatter input sources are all version-tagged: "barrier-1/synthesis.md (R4, 0.953 PASS)", "barrier-2/synthesis.md (v3.0.0, 0.953 max-iter PASS)", "phase-2/claim-validation.md (R4, 0.959 PASS)", "phase-2/comparative-effectiveness.md (R5, 0.933 max-iter)".

The ST-5 constraint inheritance chain is traceable: Origin and Scope Disclosure explicitly states "CONSTRAINT INHERITANCE FROM BARRIER-2/SYNTHESIS.MD ST-5" with four numbered constraints. Each constraint is carried into the relevant pattern entries and lookup tool warnings.

The Methodology Subsection traces each source document's role in the taxonomy construction in a Source Inputs and Their Role table — this is strong traceability for the method itself.

The Revision Log provides a version-by-version accounting of changes with finding IDs explicitly mapped to changes.

**Gaps:**
One traceability gap remains that slightly reduces this dimension. The Constraint Propagation Requirement in PS Integration specifies that downstream documents MUST co-cite the epistemological status of NPT patterns. However, there is no traceability back to where this requirement was established — no reference to the specific I1 finding (PM-002/RT-003) that motivated it, no version tag on the requirement itself. A downstream Phase 4 agent reading the propagation requirement has no way to trace why it exists or when it was added without reading the Revision Log. This is a minor cross-referencing gap.

Additionally, the Downstream Reference Index warnings cite the general constraint but do not carry source document version references for the specific constraints they enforce. A Phase 4 agent reading the Downstream Reference Index warning ("NEVER use this index to justify implementation decisions that should await Phase 5 experimental validation") cannot trace this specific directive to its source without navigating to the Origin section. This is a navigation gap that slightly reduces traceability.

**Improvement Path:**
Add "(RT-001/IN-001 resolution, v2.0.0)" as a footnote to the Cross-Reference Matrix critical usage warning. Add "(RT-003/PM-002 resolution, v2.0.0)" to the Constraint Propagation Requirement heading. These trivial additions would create a complete traceability chain from warning to the I1 finding that motivated it, raising this dimension to 0.97+.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Actionability | 0.88 | 0.92+ | Add a worktracker schema hook requiring downstream Phase 4 artifacts to declare "constraint_propagation_checked: true" linking to the PS Integration checklist. Add a Phase 5 integration placeholder row to the Downstream Reference Index for the framing-choice guidance that will be enabled by Phase 5 results. |
| 2 | Internal Consistency | 0.92 | 0.95+ | Add a cross-reference note to NPT-010's Technique Type field: "A3 and A4 — see multi-type assignment note in Dimension A Classification table." This eliminates the last navigation gap from the SM-003 partial resolution. |
| 3 | Traceability | 0.94 | 0.97+ | Add I1 finding IDs and version tags to the critical usage warning in the Cross-Reference Matrix, the Downstream Reference Index warning, and the Constraint Propagation Requirement heading. These are trivial additions that complete the traceability chain from protection mechanism to motivating finding. |
| 4 | Evidence Quality | 0.96 | 0.98+ | Add symmetric rationale notes for HIGH context compaction risk ratings in the Cross-Reference Matrix (citing T-004 failure mode analysis). This matches the treatment given to NPT-006's LOW rating. |
| 5 | Methodological Rigor | 0.95 | 0.97+ | Add a brief footnote to the Context compaction risk row header in the Cross-Reference Matrix explaining HIGH = T-004 failure mode derived, LOW = design inference. Symmetric treatment for all cells. |
| 6 | Completeness | 0.95 | 0.97+ | Merge NPT-007 and NPT-014 into a single "NPT-007 / NPT-014" row in the Evidence Gap Map to eliminate the visual double-counting even though a footnote already explains it. |

---

## New Findings Introduced by the I2 Revision

The following issues were introduced or became visible through the I2 revision and are not present in the I1 findings report.

**NEW-001 (Minor): Dimension A Multi-Type Note Placement**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NPT-010 entry; Dimension A Classification table |
| **Introduced By** | SM-003 resolution: added multi-type note to Dimension A table but did not add cross-reference in NPT-010 entry |

The SM-003 resolution adds a note on multi-type assignments to the Dimension A table introduction. The NPT-010 entry now lists "Technique Type: A3 (Augmented prohibition) and A4 (Enforcement-tier — when deployed in a tier architecture)" which is consistent with the table. However, the note explaining that some patterns span multiple types is in the Dimension A table section, not in NPT-010's individual entry. A reader navigating directly to NPT-010 via the Pattern Catalog will not encounter the multi-type explanation without reading the Dimension A section. This is a navigation cross-referencing gap.

**NEW-002 (Minor): Causal Confidence Row Label Inconsistency**

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Full Pattern Cross-Reference Matrix |
| **Introduced By** | DA-002 resolution: split "Confidence Level" into two rows |

The Cross-Reference Matrix Causal Confidence row for NPT-005 reads "MEDIUM (negation accuracy construct only)" — which is the observational/causal confidence for the specific construct, not a standalone causal confidence. NPT-005's individual entry lists "Observational Confidence: MEDIUM — ONE T1 study, no replication" and "Causal Confidence: MEDIUM for negation accuracy construct only." In the matrix, the Causal Confidence cell reads "MEDIUM (negation accuracy construct only)" while the Observational Confidence cell reads "MEDIUM." This creates a near-identical appearance for both confidence types for NPT-005, which partially undermines the split's intent for this pattern. A downstream reader scanning the two rows for NPT-005 may not see a meaningful distinction. This is Minor because the full pattern entry correctly explains the two dimensions.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score — no score above 0.88 without specific supporting evidence
- [x] Uncertain scores resolved downward (Actionability resolved to 0.88, not 0.90, given the constraint propagation enforcement gap; Internal Consistency resolved to 0.92, not 0.95, given the SM-003 navigation residual)
- [x] First-draft calibration not applicable — this is I2 of a substantive revision; calibrated against I2 quality expectations
- [x] No dimension scored above 0.96 without exceptional evidence (Evidence Quality at 0.96 is justified by the T1 Scope matrix row, FM-001 annotations in every pattern entry, and dual confidence field split)
- [x] Anti-leniency: The composite score of 0.938 reflects genuine improvement from 0.845 but MUST NOT be treated as threshold-adjacent to 0.95 when specific Actionability and Internal Consistency gaps remain verifiable. The 0.012 gap to threshold is not cosmetic.

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.938
threshold: 0.95
weakest_dimension: Actionability
weakest_score: 0.88
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Add worktracker schema hook for constraint propagation enforcement (Actionability gap)"
  - "Add cross-reference note to NPT-010 entry pointing to Dimension A multi-type explanation (Internal Consistency gap)"
  - "Add I1 finding ID version tags to critical usage warnings (Traceability gap)"
  - "Add symmetric context compaction risk rationale notes for HIGH-rated patterns (Methodological Rigor)"
new_findings_introduced:
  - "NEW-001 Minor: Dimension A multi-type note not cross-referenced in NPT-010 entry"
  - "NEW-002 Minor: Causal/Observational Confidence near-identical for NPT-005 in matrix"
phase3_gate_checks:
  GC1: PASS
  GC2: PASS
  GC3: PASS
```

---

*adv-scorer | TASK-009 | Barrier 3 | PROJ-014 | 2026-02-28*
*Deliverable: taxonomy-pattern-catalog.md v2.0.0 (I2)*
*S-014 Composite: 0.938 (REVISE — below 0.95 C4 threshold)*
*I1 Delta: +0.093 (0.845 → 0.938)*
*Critical findings resolved: 4/4 | Major findings resolved: 11/11 | Minor findings resolved: 12/12*
*New findings introduced: 2 (both Minor)*
*Phase 3 Gate Checks: GC-1 PASS | GC-2 PASS | GC-3 PASS*
*Constitutional Compliance: P-003, P-020, P-022*
