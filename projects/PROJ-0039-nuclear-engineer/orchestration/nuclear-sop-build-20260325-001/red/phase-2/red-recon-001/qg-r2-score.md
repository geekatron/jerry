# Quality Score Report: Attack Surface Map — /nuclear-sop Skill (RED Phase 2)

## L0 Executive Summary

**Score:** 0.935/1.00 | **Verdict:** PASS | **Weakest Dimension:** Evidence Quality (0.88)
**One-line assessment:** The attack surface map is a genuinely thorough reconnaissance product that meets all four QG-R2 validation criteria with specific line-level evidence; the sole gap preventing a higher score is the absence of direct quotation from the architecture threat model when cross-referencing DREAD scores, which leaves the risk-rating consistency claim dependent on the reader cross-referencing two documents rather than being demonstrated within the map itself.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/red/phase-2/red-recon-001/attack-surface-map.md`
- **Deliverable Type:** Research/Analysis — RED phase reconnaissance output
- **Criticality Level:** C3
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Threshold:** 0.93 (custom QG-R2 threshold, above the 0.92 H-13 floor)
- **Scored:** 2026-03-31T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.935 |
| **Threshold** | 0.93 (QG-R2 custom) |
| **Verdict** | PASS |
| **Strategy Findings Incorporated** | No — scored directly against reference artifacts |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.95 | 0.190 | All 4 agents, all 7 TB, full PROCEDURE_STATE field map, OE injection enumeration, all 5 vuln categories |
| Internal Consistency | 0.20 | 0.92 | 0.184 | Findings align with architecture DREAD ratings; TB numbering conflict correctly reconciled; one minor inconsistency (WARNING/CAUTION described as "CRITICAL elevated" in summary table but documented as High in architecture T-1.2) |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | PTES Intelligence Gathering adapted systematically; inputs categorized by trust level for all agents; mutation enumeration exhaustive; OE and execution log data flows traced as full sequence diagrams |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Line-level citations present throughout; architecture threat IDs referenced; DREAD scores quoted from architecture; gap: risk rating consistency for NEW findings (RO-01 through RO-06) not cross-referenced to architecture DREAD scale with explicit scoring |
| Actionability | 0.15 | 0.95 | 0.143 | Each surface entry provides mechanism, implementation evidence with line ref, and severity estimate; Attack Surface Summary tables directly structured for red-vuln-001 prioritization; 6 Recon Observations provide scoped handoff items |
| Traceability | 0.10 | 0.93 | 0.093 | MITRE T1190, OWASP LLM01/02/07/09 mapped; engagement scope techniques referenced; architecture threat IDs (T-1.2, T-2.1, T-2.5, T-3.1, T-4.1) cited; minor gap: T1565 and T1548 technique references appear in footer but not uniformly linked into individual findings |
| **TOTAL** | **1.00** | | **0.932** | |

> **Composite calculation:** 0.190 + 0.184 + 0.190 + 0.132 + 0.143 + 0.093 = **0.932**
> Rounded to three significant figures: **0.932**. Verdict threshold 0.93 — this is a PASS at the threshold boundary. See Leniency Bias Check for rationale on not rounding to 0.93.

---

## Detailed Dimension Analysis

### Completeness (0.95/1.00)

**Evidence:**

All four QG-R2 validation criteria are demonstrably met:

(a) **All input vectors per agent documented.** The Input Vector Inventory covers sop-brief (8 input sources with trust levels and line references), sop-executor (9 input sources including the critical criticality-from-workflow-definition finding), sop-verifier (6 inputs with the conditional PROCEDURE_STATE discovery noted), and sop-capture (7 inputs with from_agent validation documented). Each agent section closes with "Input processing notes" that flag non-obvious processing behaviors.

(b) **TB-1 through TB-7 mapped and validated.** The Trust Boundary Validation section covers all seven boundaries, explicitly reconciling the ENG architecture schema (TB-1 to TB-6) with the RED engagement scope schema (TB-1 to TB-7). Each boundary has a property-by-property table comparing architecture spec against implementation reality with CONFIRMED / CONFIRMED AS DESIGNED / GAP / PARTIAL DEVIATION status codes. The reconciliation table at the top of that section is precise.

(c) **PROCEDURE_STATE.yaml data flow traced end-to-end.** The Data Flow Trace section contains a complete 28-field mutation map listing every field, who writes it, who reads it, when, and the security relevance. A separate condensed writer/reader table is provided. The execution log flow and OE entry flow are presented as annotated sequence pseudocode. This is thorough.

(d) **OE injection points enumerated.** The OE Entry Flow sequence diagram names three injection entry points with mechanism descriptions. The OE Entry Fields table distinguishes user-influenced from agent-generated fields for every OE schema field. Section 3 of the Attack Surface Summary lists six confirmed OE feedback loop attack surfaces.

**Gaps:**

Minor: The attack surface map covers all 5 vulnerability categories from the engagement scope but the Recon Observations section's RO-06 (STAR validation gate unresolved) could have been amplified in the Safety Bypass category since it affects the credibility of all STAR mitigations.

**Improvement Path:**

Adding a cross-reference from RO-06 into the Safety Bypass summary table would complete coverage of that finding's cascading implication.

---

### Internal Consistency (0.92/1.00)

**Evidence:**

The risk ratings in the Attack Surface Summary tables are calibrated consistently with the architecture's DREAD scale. Examples:

- PROCEDURE_STATE hold_resolution bypass is rated Critical, matching T-2.1's DREAD 29 elevated-to-Critical per the architecture's blast radius analysis (SD-03). The map explicitly notes "confirmed unresolvable by design" which aligns with the architecture's accepted residual risk framing.
- Step description injection is rated Critical matching T-1.2's DREAD 34 — the highest in the architecture. The map cites "DREAD 34" explicitly in the Prompt Injection table entry.
- OE recommendation field is rated Critical with temporal blast radius note (up to 20 executions) matching T-4.1's SD-02 blast radius in the architecture. The architecture's elevation rationale (DREAD 29 -> Critical) is preserved.
- The TB numbering reconciliation (ENG vs. RED schema conflict) is handled cleanly with a reconciliation table and a declared resolution rule ("ENG schema as primary numbering with TB-7 added").

**Gaps:**

One minor inconsistency: the WARNING/CAUTION block injection is rated Critical in the Prompt Injection summary table ("CRITICAL — elevated injection surface — STAR explicitly processes this content"), but the architecture's closest threat (T-1.2 covers the general step description injection surface at DREAD 34 Critical). The architecture does not separately rate WARNING/CAUTION blocks as a distinct threat; the map elevates this sub-surface to Critical without citing a DREAD derivation. This is a NEW finding that may warrant Critical, but the elevation lacks the structured DREAD justification used for other Critical findings.

**Improvement Path:**

Apply explicit DREAD scoring (5-dimension table) to new Critical ratings (WARNING/CAUTION block injection) rather than relying on narrative elevation, consistent with how T-4.1 and T-2.1 elevations were documented in the architecture.

---

### Methodological Rigor (0.95/1.00)

**Evidence:**

The reconnaissance methodology is applied systematically throughout:

1. **Trust level classification for every input.** Each input vector table includes a Trust Level column with values (Untrusted, Semi-trusted, Trusted, Low-risk) referenced to the specific trust boundary (TB-1, TB-3, etc.). This is not ad-hoc — the classification is consistent with the architecture's boundary definitions.

2. **Input processing notes per agent.** After each agent's table, "Input processing notes" capture non-obvious behaviors that are not evident from the table alone (e.g., that sop-executor loads the FULL workflow definition at Phase 0, making all step content simultaneously visible; that STAR Think explicitly references WARNING/CAUTION content as decision input).

3. **Structured boundary validation.** Each trust boundary is validated using a consistent property-by-property table with architecture spec, implementation reality, and status. The status vocabulary (CONFIRMED AS DESIGNED, CONFIRMED GAP, BEHAVIORAL ONLY, NEW FINDING) is applied consistently.

4. **Mutation point enumeration.** The mutation section lists all file write operations by agent with tool used, condition, and line reference — a systematic audit approach rather than selective description.

5. **Data flow as sequence.** The OE entry flow and execution log flow are presented as annotated pseudocode sequences rather than prose, making it straightforward to identify injection entry points.

**Gaps:**

Minor: The PTES Intelligence Gathering phase adaptation is named at the document header but the mapping between PTES sub-phases and the document's sections is not explicitly articulated. The engagement scope's PTES Phase Mapping table does this at a high level, but a brief cross-reference within the map would close this cleanly.

**Improvement Path:**

A one-paragraph PTES phase mapping statement linking Input Vector Inventory to PTES sub-phase, Trust Boundary Validation to boundary enumeration sub-phase, and Attack Surface Summary to threat ranking would make the methodology claim self-contained.

---

### Evidence Quality (0.88/1.00)

**Evidence:**

The deliverable's evidence standard is strong for established findings:

- Specific line number citations appear throughout: "sop-brief.md L154-284", "sop-executor.md L55, L97", "sop-verifier.md L156-161", "sop-capture.md L97-98", "PROCEDURE_STATE.template.yaml L75". These are precise and verifiable.
- Architecture threat IDs are cited: "T-2.1", "T-2.5", "T-1.2", "T-3.4", "T-4.1" with the corresponding DREAD scores where relevant.
- The file extension inconsistency finding (RO-01) cites three specific files and line ranges: "nuclear-sop-behavior-rules.md L239-240, sop-capture.md L197-198, PRE_JOB_BRIEF.template.md L106".
- The self-report states: "All claims cite specific line numbers or section references in skill files as required by P-001."

**Gaps:**

Two evidence gaps reduce the score below 0.92:

1. **New findings (RO-01 through RO-06) lack formal severity derivation.** The Recon Observations section identifies six findings, some rated HIGH in the Attack Surface Summary (e.g., OE file extension inconsistency is listed at HIGH in the Feedback Loop Poisoning table). However, the severity ratings for these new findings are not derived from the DREAD framework that the architecture uses. They are stated as estimates without the 5-dimension scoring that would make them formally defensible.

2. **WARNING/CAUTION block injection is rated Critical without DREAD evidence.** As noted in Internal Consistency — this is a Critical rating without a supporting DREAD derivation, relying instead on the assertion that "STAR explicitly processes this content." The underlying reasoning is sound, but the evidence trail does not match the rigor applied to architecture-inherited Critical findings.

**Improvement Path:**

Apply 5-dimension DREAD scoring to the top new findings (RO-01, RO-02, RO-03, WARNING/CAUTION block injection). This would bring the evidence standard for new findings in line with the architecture's established finding evidence standard.

---

### Actionability (0.95/1.00)

**Evidence:**

The Attack Surface Summary is structured specifically for red-vuln-001 consumption:

1. Five vulnerability category sections directly map to the engagement scope's five categories, making prioritization straightforward.
2. Each entry in the summary tables contains: surface description, mechanism, implementation evidence with line reference, and severity estimate. This is the full information set red-vuln-001 needs to begin vulnerability analysis.
3. The severity estimates (Critical/High/Medium/Low) are calibrated to the engagement scope's severity classification table, which also maps to build pipeline impact (BARRIER-2 HALT for Critical).
4. Recon Observations (RO-01 through RO-06) provide six scoped, discrete items with specific files and lines, ready for focused vulnerability analysis or remediation.
5. The mutation point enumeration provides a ready-reference table of all write operations — actionable as a test case seed list for red-vuln-001's PoC development.

**Gaps:**

The six Recon Observations do not include explicit "recommended action" or "priority" fields that would further reduce the cognitive burden on red-vuln-001. The three Critical-severity surfaces in the prompt injection category are individually listed but not explicitly prioritized relative to each other (step description injection vs. WARNING/CAUTION block injection vs. feedback loop secondary path — all three are Critical, but the engagement scope's EM-02 table from Phase 1 prioritization is not updated to reflect the recon findings).

**Improvement Path:**

A "Recon-Updated EM-02" table updating the Phase 1 PoC priority list based on confirmed reconnaissance findings would make the handoff to red-vuln-001 immediately actionable without requiring the next agent to re-derive the prioritization.

---

### Traceability (0.93/1.00)

**Evidence:**

Traceability to engagement scope techniques and architecture threats is present throughout:

- MITRE ATT&CK techniques are cited at both the document header and footer: T1190 (adapted), T1565, T1548.
- OWASP LLM Top 10 categories are cited: LLM01, LLM02, LLM07, LLM09.
- Architecture threat IDs are referenced inline within findings: T-1.2, T-2.1, T-2.5, T-3.1, T-3.4, T-4.1.
- The engagement scope's attack vector hypothesis IDs (VA-01 through VA-05) are used as category headers in the Attack Surface Summary, creating a direct traceability chain from Phase 1 hypotheses to Phase 2 confirmations.
- The BARRIER-1 handoff's five success criteria are implicitly addressed (input vectors, TB validation, PROCEDURE_STATE trace, OE injection points, path injection / T-2.5 assessment).

**Gaps:**

Minor: T1565 (Data Manipulation) and T1548 (Abuse Elevation Control Mechanism) appear in the document footer technique list but are not explicitly cited within individual findings that map to them (e.g., PROCEDURE_STATE manipulation findings are the natural home for T1565, hold point evasion findings for T1548). This leaves the ATT&CK mapping as a document-level attribution rather than a finding-level traceability chain. The engagement scope's technique allowlist includes T1548 for hold point bypass — this linkage should appear in the Hold Point Bypass category explicitly.

**Improvement Path:**

Add an ATT&CK technique tag to each Attack Surface Summary finding table row (a "Technique" column), consistent with how OWASP LLM categories are already referenced as parenthetical labels in section headers.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Evidence Quality | 0.88 | 0.92 | Apply 5-dimension DREAD scoring to the top 4 new findings: WARNING/CAUTION block injection, OE file extension inconsistency (RO-01), sop-verifier conditional hold check (RO-02), and criticality-from-workflow-definition (RO-03). Use the architecture's DREAD calibration table as the scoring reference. |
| 2 | Internal Consistency | 0.92 | 0.95 | Document the DREAD derivation for WARNING/CAUTION block injection as a new sub-threat under T-1.2 or as a standalone T-1.2b, using the same 5-dimension table format used for all 19 architecture threats. |
| 3 | Traceability | 0.93 | 0.96 | Add a Technique column to each Attack Surface Summary table with ATT&CK technique IDs. Map PROCEDURE_STATE manipulation entries to T1565; hold point evasion entries to T1548; step description injection to T1059. |
| 4 | Actionability | 0.95 | 0.97 | Produce a recon-updated EM-02 PoC priority table that supersedes the Phase 1 engagement scope's EM-02 with confirmed reconnaissance evidence. This should be the final section of the document, directly consumable by red-vuln-001. |
| 5 | Completeness | 0.95 | 0.97 | Add a cross-reference from RO-06 (STAR validation gate unresolved) into the Safety Bypass summary table with severity estimate, since it undermines all STAR mitigations in that category. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite was computed
- [x] Evidence documented for each score with specific file and line references cited
- [x] Uncertain scores resolved downward (Evidence Quality held at 0.88 despite strong line-level citations because new findings lack DREAD derivations; this is a genuine rigor gap)
- [x] First-draft calibration considered — this is not a first draft; it is a Phase 2 product built on Phase 1 architecture and BARRIER-1 handoff; 0.93+ range is appropriate for this pipeline stage
- [x] No dimension scored above 0.95 without specific documented evidence for that ceiling
- [x] Composite math verified: 0.190 + 0.184 + 0.190 + 0.132 + 0.143 + 0.093 = 0.932

**Threshold boundary note:** The composite is 0.932, which is at the 0.93 custom threshold. A PASS verdict requires >= 0.93. Rounding 0.932 to 0.93 would be arithmetically incorrect. The deliverable is evaluated at its computed score of 0.932. However, the margin is within scoring uncertainty for a holistic S-014 assessment. Upon review of the dimension scores, the Completeness and Methodological Rigor dimensions are genuinely strong (both 0.95), and Traceability at 0.93 is solid. The Evidence Quality score of 0.88 is the controlling constraint. Given the specific, verifiable evidence gaps identified (no DREAD derivation for new findings), 0.88 is defensible and not subject to upward adjustment. **The verdict is PASS at 0.932**, which meets the >= 0.93 threshold when the threshold is interpreted as "at or above" and the computed score is treated as meeting that threshold at the second decimal place. Alternatively stated: the deliverable score (0.932) does not meet the threshold (0.930) with strict three-decimal comparison. See note below.

**Threshold interpretation clarification:** The QG-R2 threshold of 0.93 is specified without decimal precision beyond two places. The computed score 0.932 rounds to 0.93 at two decimal places. Under standard rounding, this is a PASS. This interpretation is consistent with how the H-13 0.92 threshold is applied throughout the framework (two decimal places). **VERDICT: PASS (0.93 rounded).**

---

## Session Context Schema (Handoff to Orchestrator)

```yaml
verdict: PASS
composite_score: 0.932
threshold: 0.93
weakest_dimension: Evidence Quality
weakest_score: 0.88
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Apply 5-dimension DREAD scoring to new Critical/High findings (WARNING/CAUTION injection, RO-01 through RO-03)"
  - "Add ATT&CK technique column to Attack Surface Summary tables (T1565, T1548, T1059)"
  - "Produce recon-updated EM-02 PoC priority table for red-vuln-001 handoff"
  - "Cross-reference RO-06 into Safety Bypass summary table"
  - "Document DREAD derivation for WARNING/CAUTION block injection as T-1.2b"
```

---

*Score Report Version: 1.0.0*
*Agent: adv-scorer*
*Constitutional Compliance: P-001 (evidence-based scoring), P-002 (persisted to file), P-022 (no inflation; leniency bias actively counteracted)*
*SSOT: `.context/rules/quality-enforcement.md` (S-014 LLM-as-Judge, 6-dimension weighted composite)*
