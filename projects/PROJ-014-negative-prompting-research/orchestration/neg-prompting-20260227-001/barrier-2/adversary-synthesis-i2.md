# Quality Score Report: Barrier 2 Synthesis v2.0.0 (I2)

> adv-scorer | Iteration 2 | S-014 LLM-as-Judge | PROJ-014 | 2026-02-28
> Target: barrier-2/synthesis.md (v2.0.0, TASK-007, ps-synthesizer)
> Criticality: C4 (Critical) | Threshold: >= 0.95 | Prior score: I1 = 0.868 REVISE

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, key finding |
| [Scoring Context](#scoring-context) | Deliverable metadata |
| [Score Summary](#score-summary) | Composite, threshold, verdict table |
| [Dimension Scores](#dimension-scores) | Weighted scoring table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, improvement path |
| [I1 Finding Resolution Audit](#i1-finding-resolution-audit) | Critical and Major finding verification |
| [Remaining Findings](#remaining-findings) | Residual issues in v2.0.0 |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered improvement table |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency verification |
| [Session Context Handoff](#session-context-handoff) | Orchestrator handoff YAML |

---

## L0 Executive Summary

**Score:** 0.927/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Actionability (0.88)
**One-line assessment:** The v2.0.0 revision resolves all 5 Critical and 16 of 19 Major I1 findings with genuine structural improvements, but three persistent gaps — no enforcement owner/timeline assignments in ST-7 blocking gates, PG-003 confidence tag misalignment between ST-4 narrative and table, and the ST-4 "unconditional" framing for PG-004/PG-005 that still flattens confidence differentiation — keep the composite 0.023 below the C4 threshold of 0.95.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-2/synthesis.md`
- **Deliverable Version:** 2.0.0 (Iteration 2)
- **Deliverable Type:** Research Synthesis
- **Criticality Level:** C4 (Critical — irreversible, governance-level)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** I1 = 0.868 REVISE (5 Critical, 19 Major, 15 Minor)
- **I1 Report:** `barrier-2/adversary-synthesis-i1.md`
- **Scored:** 2026-02-28

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.927 |
| **Threshold** | 0.95 (C4, orchestration directive) |
| **Verdict** | REVISE |
| **Distance to Threshold** | -0.023 |
| **Strategy Findings Incorporated** | Yes — I1 adversary tournament (39 findings: 5 Critical, 19 Major, 15 Minor) |
| **Critical Findings Resolved** | 5 of 5 |
| **Major Findings Resolved** | 16 of 19 (3 persistent) |
| **Minor Findings Resolved** | 12 of 15 (3 deferred with rationale) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.94 | 0.188 | All 7 synthesis tasks present and substantive; EO-001–EO-003 now integrated in ST-1; L0 mentions retrospective; one residual gap (ST-7 no owner/timeline) |
| Internal Consistency | 0.20 | 0.93 | 0.186 | "UNANIMOUS" correctly replaced with "INTERNALLY AGREED"; A-23 label rationale added; "identical evidence tiers" corrected; one residual: PG-003 framing tension |
| Methodological Rigor | 0.20 | 0.92 | 0.184 | BLOCKING gate language fully added to ST-7; checklist now has I1→I2 revision column; circularity note in Source Summary; three unresolved gaps (RT-004, PM-005, external validation) |
| Evidence Quality | 0.15 | 0.94 | 0.141 | U-004 Anthropic concentration quantified; circularity caveat on L2 matrix header; ST-6 SCANNING CAUTION callout added with confound column; labels corrected |
| Actionability | 0.15 | 0.88 | 0.132 | Adversary gate verification requirements added to all 3 phases in ST-5; PG confidence tags added in ST-4; Key Imperatives Index in L0; ST-7 BLOCKING structure solid; ST-7 still lacks owner/timeline |
| Traceability | 0.10 | 0.96 | 0.096 | Revision log fully documents I1→I2 changes; self-review checklist has I1→I2 column; U-003 cross-linked to Phase 5; EO observations traced into body |
| **TOTAL** | **1.00** | | **0.927** | |

---

## Detailed Dimension Analysis

### Completeness (0.94/1.00)

**Evidence:**

The v2.0.0 document addresses all seven synthesis tasks (ST-1 through ST-7) with substantive content at every level. The major completeness improvements from I1 are genuine:

- EO-001–EO-003 session observations are now explicitly integrated in ST-1 (lines 100–103) with T5 evidence tier label and scope note: "These session observations are T5 evidence (single-session observation, no controls)."
- L0 narrative now includes the retrospective comparison reference with confound caveat: the narrative paragraph explicitly mentions "A retrospective comparison of PROJ-014 (negative-constraint governance) vs. PROJ-007 (positive-framing governance) produced an observational baseline only — NEVER cite as a controlled test."
- ST-7 prerequisites are now a full BLOCKING gate specification with Completion criterion and Fallback columns — a genuine structural upgrade over the "What is needed" I1 framing.
- ST-4 is restructured into three sub-sections with per-finding confidence tags, addressing the PG confidence differentiation gap.

**Gaps:**

One residual completeness gap: the ST-7 BLOCKING prerequisites table (P-001 through P-004) provides Completion criterion and Fallback columns but still has no Owner or Timeline columns. The I1 finding IN-003-i1 specified "prerequisites have no owner or timeline — guaranteed to be treated as parallel work." The revision log entry for IN-003-i1 states: "BLOCKING gate table adds Completion criterion and Fallback if unachievable columns; BLOCKING definition statement added to ST-7 header." This resolves the BLOCKING ambiguity (PM-002, FM-002, FM-008) but does not address the ownership and timeline dimensions of IN-003. A downstream Phase 5 consumer reading ST-7 knows the prerequisites are blocking but still has no assigned owner or timeline, which remains an execution risk.

**Improvement Path:**

Add Owner and Timeline estimate columns to the ST-7 BLOCKING prerequisites table. Even if the owner is "Phase 5 lead" for all four gates, the explicit assignment converts the constraint from aspirational to operational. Score would increase to 0.96–0.97 if this gap is resolved alongside the actionability gap.

---

### Internal Consistency (0.93/1.00)

**Evidence:**

The major I1 internal consistency findings are resolved:

- "UNANIMOUS" labels replaced throughout L2 cross-reference matrix with "INTERNALLY AGREED (4 pipeline-internal documents)" and a circularity caveat note appears as the matrix header. This directly addresses RT-001-i1, IN-002-i1, FM-003-i1, and CC-001-i1.
- A-23 combined label selection rationale is now explicit in ST-2: "combined label adopts TASK-006 I5 calibration; operationalized scale defines MEDIUM as exactly 1 T1 study with no replication." This directly addresses SR-001-i1.
- L0 "identical evidence tiers" corrected to "reconcilable confidence scales derived from the same evidence base using terminologically distinct but epistemically compatible scales" — addressing CV-001-i1.
- The confidence reconciliation matrix (ST-2) is internally consistent: THREE distinct confidence tiers are presented clearly and mapped correctly.
- The synthesis's own internal consistency is strong — null finding protection language is consistent throughout ("untested, not disproven"), A-23 scope caveat (negation reasoning accuracy, not hallucination rate) is applied consistently across ST-1, ST-2, L2 matrix, and downstream specifications.

**Gaps:**

One residual internal consistency tension: PG-003's confidence tag in ST-4 reads "[T4 observational, MEDIUM — working practice, not validated finding]" but the ST-4 narrative for Finding M-1 (Structured negative techniques at rank 5 improve negation accuracy) presents A-23 (T1 evidence) as the basis, while PG-003 is about pairing enforcement-tier constraints with consequences — a different operational recommendation sourced from T4 vendor practice, not from A-23 directly. A careful reader can distinguish these, but the close proximity of the T1 Finding M-1 and PG-003 (T4) creates potential for a reader to conflate A-23's T1 evidence as the basis for PG-003. This is a minor but genuine tension not fully resolved in v2.0.0.

Additionally, the narrative summary in L0 contains the phrase "The two deliverables agree on all core verdicts and apply reconcilable confidence scales derived from the same evidence base" — which is now accurate and consistent with the corrected ST-2 language.

**Improvement Path:**

Add one sentence in ST-4 explicitly separating Finding M-1 (evidence for rank 5 improvement, based on A-23 T1) from PG-003 (pairing recommendation, based on T4 vendor practice). Something like: "Note: PG-003 is NOT derived from A-23. A-23 supports Finding M-1 (negation accuracy). PG-003 is a working practice from T4 vendor observation."

---

### Methodological Rigor (0.92/1.00)

**Evidence:**

The major methodological rigor improvements are real and significant:

- ST-7 prerequisite table is now fully restructured with BLOCKING gate language. The header states: "Verdict: SUFFICIENT — subject to four BLOCKING prerequisite gates." The BLOCKING definition is explicit: "A BLOCKING prerequisite is a condition that MUST be COMPLETE before the pilot can launch. Treating any of P-001 through P-004 as parallel work (proceeding with pilot preparation while prerequisites are incomplete) is a protocol violation. The pilot MUST NOT launch until all four BLOCKING prerequisites are documented as COMPLETE by the Phase 5 lead." This directly and substantively resolves PM-002-i1, FM-002-i1, and FM-008-i1.
- Self-review checklist now has an "I1→I2 revision" column documenting which finding each checklist item addresses. This directly resolves CC-003-i1 and FM-004-i1, converting the checklist from a pro-forma assertion into an auditable revision record.
- Braun & Clarke methodology citation is present and the seven-task structure is maintained throughout.
- Pipeline circularity note is added to Source Summary: "Treating these scores as independent quality validation would be circular. The scores represent internal pipeline consistency checks, not independent peer review."

**Gaps:**

Three methodological rigor gaps persist — all three were explicitly deferred in the revision log with rationale, which is transparent:

1. **RT-004-i1 / CC-002-i1 (deferred):** ST-7 "SUFFICIENT" verdict lacks external methods validation citation (P-011). The revision log acknowledges: "Resolving this would require external experimental design consultation that is outside the synthesis agent's scope." This is an honest deferral — the synthesis agent cannot retroactively consult external methods experts. However, the gap remains real: the "SUFFICIENT" verdict is an internal pipeline judgment, not an externally validated one.

2. **PM-005-i1 (deferred):** Researcher circularity disclosed but not operationally blocked. The revision log acknowledges this requires "a separate research protocol decision." True, but the gap reduces methodological rigor because the disclosure is now pro-forma — well-articulated but not operationally constrained.

3. **SR-004-i1 (deferred):** ST-7 lacks formal sufficiency gap analysis. The revision log notes "formal gap analysis would require a methods expert." Addressed partially by the BLOCKING gate restructuring (which is more operationally specific), but the formal gap analysis remains absent.

**Improvement Path:**

For the deferred items: (1) add a sentence to ST-7 explicitly flagging that the "SUFFICIENT" verdict has not been externally validated and recommending Phase 5 obtain an independent methods review before pilot launch; (2) add one operational constraint to ST-5 Phase 5 inputs: "Independent replication by a researcher outside the PROJ-014 team is REQUIRED before VS-002 interpretations are used beyond PROJ-014 scope." These additions do not require external consultation but operationalize the disclosures.

---

### Evidence Quality (0.94/1.00)

**Evidence:**

The I1 evidence quality findings are substantively resolved:

- U-004 (Assumption: vendor evidence not Anthropic-dominated) now quantifies the concentration: "Of the 33 cataloged instances, the supplemental report documents: Anthropic/Claude Code = the primary source for VS-001 taxonomy (rules documented as exemplars); OpenAI behavioral guidance contributes C-6 and C-7 (2 of 33 explicitly non-Anthropic vendor sources); LlamaIndex governance documentation contributes C-11." This directly resolves SR-002-i1.
- L2 cross-reference matrix header includes circularity caveat: "All 'Internally agreed' labels below reflect consistency across four documents produced by the same research pipeline using the same evidence base. These are internal consistency findings, not independent corroboration."
- L2 confidence reconciliation matrix row for vendor self-practice now explicitly reads: "T4 observational (HIGH observational, LOW causal; Anthropic-heavy concentration — see U-004)"
- ST-6 SCANNING CAUTION callout is present before the retrospective table: "The numerical table below presents quality metrics that are CONFOUNDED. Read the confound analysis before extracting any numbers. NEVER cite these figures as a directional comparison."
- ST-6 now includes a "Confound verdict" column in the retrospective data table — the confound analysis is co-located with each numerical row rather than in separate prose below.
- T1/T4/T5 evidence tier distinctions are consistently maintained throughout. The scope caveat for A-23 (negation reasoning accuracy, not hallucination rate) is present in ST-1, ST-2, ST-4, and L2 matrix. No evidence tier conflation was detected.

**Gaps:**

One minor gap: the confidence reconciliation matrix row for "Vendor self-practice pattern (observational)" lists "3+ vendors (Anthropic-heavy concentration — see U-004)" which now correctly flags the concentration. However, the label "3+ vendors" slightly overstates the diversification — only 2 of 33 instances are explicitly from OpenAI, and 1 is from LlamaIndex. "3 vendors" is accurate (Anthropic, OpenAI, LlamaIndex), but "3+ vendors" implies more breadth than the actual distribution supports. This is a very minor precision gap.

**Improvement Path:**

Change "3+ vendors" to "3 vendors (Anthropic-heavy: 30+ instances Anthropic/Claude Code; 2 OpenAI; 1 LlamaIndex)" in the confidence reconciliation matrix row. This makes the distribution visible without requiring a read of U-004.

---

### Actionability (0.88/1.00)

**Evidence:**

The actionability improvements are genuine and address the highest-severity I1 gaps:

- All three downstream phases now have "Adversary gate verification requirement" subsections in ST-5 specifying exactly which NEVER constraints must be checked. For Phase 3: "The Phase 3 adversary gate MUST verify: (1) the taxonomy does not imply a directional verdict at ranks 9–11; (2) the C1–C7 pilot condition mapping is preserved or an impact assessment is provided; (3) rank 12 is distinguished from ranks 9–11 with confidence labels." Phase 4 and Phase 5 have equivalent specificity. This directly resolves FM-007-i1 and DA-004-i1.
- PG-001 through PG-005 now have explicit confidence tags co-located in ST-4: PG-001 [T1+T3, HIGH, unconditional], PG-002 [T1+T4, HIGH, unconditional], PG-003 [T4 observational, MEDIUM — working practice, not validated finding], PG-004 [T4, unconditional by failure mode logic], PG-005 [T3, unconditional investment allocation]. The "CRITICAL READING NOTE" at the top of ST-4 explicitly states: "PG-001 through PG-005 are NOT uniformly authoritative — each carries a distinct confidence tag. NEVER extract PG statements without their co-located confidence tier and key caveat."
- Key Imperatives Index in L0 consolidates 10 NEVER constraints in a scannable table format with source citations.
- ST-7 BLOCKING gate structure is now operationally actionable: four gates with Completion criterion and Fallback columns.

**Gaps (persistent):**

This is the weakest dimension and the primary barrier to reaching 0.95 composite.

1. **Owner and timeline absent from ST-7 BLOCKING gates.** The BLOCKING gate structure resolves the ambiguity about sequential vs. parallel execution, but P-002 (pre-validated example pair pool, "highest-risk prerequisite") still has no assigned owner and no timeline estimate. The revision log addresses IN-003-i1 by adding "Completion criterion" and "Fallback if unachievable" columns — but the original IN-003 finding was explicitly about "no owner, no timeline — guaranteed to be treated as parallel work." The fallback column partially addresses this ("if kappa < 0.80 after 2 revision cycles, escalate to research lead") but the escalation path assumes there is a "research lead" — never named or assigned. Downstream Phase 5 still has no actionable ownership assignment.

2. **PG-003's confidence tag in the ST-4 narrative is misaligned.** ST-4 restructured Finding M-1 (rank 5 negation accuracy, A-23 T1) as the evidence base, and PG-003 follows immediately as a practitioner implication — but PG-003's confidence basis is T4 observational vendor practice, not A-23. The confidence tag "[T4 observational, MEDIUM — working practice, not validated finding]" is correct, but the structural proximity to the T1 A-23 evidence in Finding M-1 creates actionability risk: a downstream consumer reading the "Provisional findings" sub-section will see A-23 T1 evidence and PG-003 as a continuous block, potentially treating PG-003 as T1-backed when it is T4-backed. This is a lower-severity persistence of IN-001-i1's core concern.

3. **Adversary gate verification requirements in ST-5 are recommendations without a cross-link mechanism.** The ST-5 adversary gate verification requirements are well-specified, but the synthesis still does not propose how Phase 3/4/5 orchestration plans will be informed about these requirements — i.e., there is no pointer suggesting the orchestrator should copy these gate requirements into Phase 3/4/5 orchestration plans or quality gate templates. The NEVER constraints now have downstream adversary gate specifications, but the pathway from this synthesis to those future adversary gates remains indirect.

**Improvement Path:**

Priority 1: Add Owner (even if "Phase 5 lead") and rough Timeline estimate (e.g., "2–3 weeks before pilot launch") to ST-7 BLOCKING prerequisites table. This directly converts aspirational BLOCKING gates into assigned operational items. Priority 2: Add one sentence separating Finding M-1's A-23 T1 evidence from PG-003's T4 basis.

---

### Traceability (0.96/1.00)

**Evidence:**

Traceability is the strongest dimension in v2.0.0 and the most improved from I1:

- Revision log (I1→I2) is comprehensive and finding-by-finding: 5 Critical findings, 19 Major findings, and selected Minor findings each have documented resolution with explicit "Section(s) changed" column. This is genuine H-15 evidence — the checklist now maps to actual documented revisions.
- Self-review checklist has "I1→I2 revision" column linking each PASS item to the specific finding ID it addresses. This converts the H-15 assertion from nominal to evidenced.
- U-003 (context compaction assumption) is now cross-linked to Phase 5 deployment constraint in ST-3 and to the L2 Phase 5 specification table.
- EO-001–EO-003 session observations are traced from Source Summary into ST-1 body, closing the CV-002-i1 traceability gap.
- All primary claims cite specific identifiers (AGREE-X, E-FOR-X, D1–D5, VS-00X, PG-00X, EO-00X, C1–C7) consistently throughout.
- The "4 pipeline-internal documents" circularity label in the L2 matrix is now consistently applied, making the provenance boundaries explicit.

**Gaps:**

Minor: The deferred findings (RT-004-i1, CC-002-i1, SR-004-i1, PM-005-i1) are listed in the "Findings Not Resolved" section with rationale — this is a good traceability practice. However, the traceability from the deferred findings to the downstream remediation plan is weak: "flagged for Phase 5" appears for RT-004-i1 but no specific Phase 5 worktracker item or gate criterion is created to ensure follow-through.

**Improvement Path:**

Add one row to the ST-5 Phase 5 adversary gate verification requirement: "Obtain independent methods review of the n=30 pilot design from a researcher outside the PROJ-014 pipeline before pilot launch (RT-004-i1 deferred item)."

---

## I1 Finding Resolution Audit

### Critical Findings (5 of 5 verified resolved)

| Finding ID | Severity | Original Description | Resolution Status | Evidence in v2.0.0 |
|-----------|----------|---------------------|-------------------|---------------------|
| IN-001-i1 | Critical | Extractable confident fragments without co-located caveats | RESOLVED | ST-4 "CRITICAL READING NOTE" + per-PG confidence tags co-located with each finding; three explicit sub-sections (HIGH/MEDIUM/Unconditional operational) |
| PM-001-i1 / FM-001-i1 | Critical | PG-001–PG-005 uniformly "unconditional" — confidence differentiation lost | RESOLVED | Each PG has explicit tag: PG-001 [T1+T3, HIGH], PG-002 [T1+T4, HIGH], PG-003 [T4 observational, MEDIUM], PG-004 [T4, unconditional by failure mode logic], PG-005 [T3, unconditional investment allocation] |
| PM-002-i1 / FM-002-i1 / FM-008-i1 | Critical | Prerequisite BLOCKING status not explicit | RESOLVED | ST-7 header: "Verdict: SUFFICIENT — subject to four BLOCKING prerequisite gates"; BLOCKING definition statement explicit; Completion criterion and Fallback columns added |
| FM-007-i1 / DA-004-i1 | Critical | NEVER constraints in ST-5 have no enforcement mechanism | RESOLVED | Adversary gate verification requirement subsections added to Phase 3, Phase 4, and Phase 5 in ST-5 with specific MUST verify items |

**Assessment:** All 5 Critical findings are genuinely resolved. The resolutions are structural (not superficial label changes) and substantively address the root causes identified in I1.

### Major Findings (16 of 19 resolved, 3 persistent)

| Finding ID | Severity | Original Description | Resolution Status | Notes |
|-----------|----------|---------------------|-------------------|-------|
| DA-001-i1 | Major | Synthesis manufactures consensus — co-dependent alignment | RESOLVED | "UNANIMOUSLY" → "INTERNALLY AGREED (4 pipeline-internal documents)" throughout L2; circularity caveat as matrix header; pipeline circularity note in Source Summary |
| DA-002-i1 | Major | Execution risk for prerequisites under-weighted | RESOLVED | BLOCKING gate structure with P-002 explicitly called "highest-risk prerequisite" |
| DA-004-i1 | Major | NEVER constraints lack enforcement mechanism | RESOLVED | See FM-007-i1 resolution |
| PM-003-i1 | Major | ST-6 retrospective table scannable as directional evidence | RESOLVED | "SCANNING CAUTION" callout + "Confound verdict" column in table |
| PM-004-i1 | Major | Assumption U-001 does not protect pilot condition alignment | RESOLVED | Explicit C1–C7 alignment constraint added to U-001: "Any modification MUST preserve the C1–C7 pilot condition alignment" |
| FM-001-i1 | Major | PG confidence differentiation lost (RPN 144) | RESOLVED | See PM-001-i1 resolution |
| FM-006-i1 | Major | ST-6 table-vs-narrative presentation risk (RPN 120) | RESOLVED | See PM-003-i1 resolution |
| CC-003-i1 | Major | Self-review checklist lacks iteration history | RESOLVED | "I1→I2 revision" column added to checklist with specific finding IDs |
| RT-001-i1 | Major | "UNANIMOUS" labels epistemically unjustified | RESOLVED | See DA-001-i1 resolution |
| RT-002-i1 | Major | Circular quality assurance | RESOLVED | Pipeline circularity note added to Source Summary with explicit acknowledgment |
| SR-001-i1 | Major | A-23 combined label selection rationale missing | RESOLVED | Explicit rationale in ST-2 and L2 matrix: "combined label adopts TASK-006 I5 calibration" |
| SR-002-i1 | Major | Assumption U-004 vendor concentration not quantified | RESOLVED | Specific counts added: Anthropic primary, OpenAI C-6/C-7 (2 instances), LlamaIndex C-11 |
| SM-001-i1 | Major | L0 buries highest-confidence finding | RESOLVED | L0 restructured: Three-Line Summary opens with HIGH/MEDIUM/UNTESTED tiers first |
| SM-002-i1 | Major | ST-4 lacks explicit "Established findings" sub-section | RESOLVED | Three sub-sections added: Established (HIGH), Provisional (MEDIUM), Unconditional operational |
| FM-003-i1 | Major | "UNANIMOUS" without circularity caveat (RPN 140) | RESOLVED | See RT-001-i1 resolution + matrix header caveat |
| FM-004-i1 | Major | Self-review checklist lacks iteration history (RPN 105) | RESOLVED | See CC-003-i1 resolution |
| **IN-003-i1** | **Major** | **Prerequisites have no owner or timeline** | **PARTIALLY RESOLVED** | BLOCKING gates added; Completion criterion and Fallback columns added; but no Owner or Timeline estimate columns; ownership still unassigned |
| **IN-002-i1** | **Major** | **"UNANIMOUS" labels enable misrepresentation** | **RESOLVED (technical) / RESIDUAL RISK** | Label change is correct; however, "INTERNALLY AGREED" without further context explanation in L2 matrix still allows misinterpretation by a reader who does not follow the circularity caveat note at the matrix header |
| **DA-003-i1** | **Minor in I1 but relevant** | **Null finding emphasis may prime for inconclusive results** | **ACKNOWLEDGED, NOT FULLY RESOLVED** | Noted in revision log; revision log states "inconclusiveness is 'a legitimate expected outcome, not a failure' while preserving scientific equipoise" — the structural imbalance between inconclusive and positive outcome planning is partially addressed by the three-tier confidence sub-sections |

**Note on IN-002-i1 categorization:** The label change itself is resolved. The residual risk is that a downstream reader who scans the L2 matrix without reading the header note will still see "INTERNALLY AGREED" repeated across 9 rows and may interpret it as independent corroboration. This is partially mitigated by the header caveat. Given that the finding was formally addressed, this is scored as resolved for purposes of finding counts but flagged as a residual structural risk.

### Minor Findings

Per the revision log: 12 of 15 Minor findings resolved; 3 deferred (RT-004-i1, CC-002-i1, SR-004-i1, PM-005-i1 — note: the revision log lists 4 items in the "not resolved" table, which conflicts slightly with the "12 Minor resolved" claim in the header). The deferred items are documented with rationale and are all legitimately outside the synthesis agent's authority (requiring external methods consultation or project management decisions).

---

## Remaining Findings

### Findings Confirmed Persisting in v2.0.0

| ID | Severity | Description | Section | Dimension Impact |
|----|----------|-------------|---------|-----------------|
| R-001 | Major | ST-7 BLOCKING gates have no Owner or Timeline columns — IN-003-i1 partially resolved; ownership gap persists | ST-7 | Actionability (primary), Completeness (secondary) |
| R-002 | Minor | PG-003 confidence tag correctly marked [T4 observational, MEDIUM] in ST-4, but structural proximity to A-23 T1 evidence in Finding M-1 still creates conflation risk for scanning readers | ST-4 | Actionability, Internal Consistency |
| R-003 | Minor | Adversary gate verification requirements in ST-5 are not linked to orchestration plan or Phase 3/4/5 template specifications — the downstream adversary gate check cannot be triggered by the synthesis document alone | ST-5 | Actionability |
| R-004 | Minor (deferred) | ST-7 "SUFFICIENT" verdict has no external methods citation — acknowledged in revision log as outside synthesis scope | ST-7 | Methodological Rigor |
| R-005 | Minor (deferred) | Researcher circularity operationally disclosed but not operationally blocked — acknowledged as project management decision | ST-3 | Methodological Rigor |
| R-006 | Minor | Confidence reconciliation matrix row for vendor self-practice reads "3+ vendors" which overstates breadth (actual: 3 vendors with Anthropic-heavy distribution, 2 OpenAI, 1 LlamaIndex) | L2 | Evidence Quality |

**No new Critical findings identified in v2.0.0.**
**R-001 is the only Major-severity remaining finding.**
**R-002 through R-006 are Minor severity.**

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Actionability | 0.88 | 0.93 | Add Owner (at minimum "Phase 5 lead") and Timeline estimate (e.g., "Required: 2–3 weeks before pilot launch") columns to ST-7 BLOCKING prerequisites table for all four gates; this converts aspirational blocking into assigned operational items and resolves R-001 |
| 2 | Actionability | 0.88 | 0.91 | Add one separating sentence in ST-4 between Finding M-1 (A-23 T1 basis) and PG-003 (T4 basis) to prevent conflation: "Note: PG-003 is derived from T4 vendor practice (VS-001–VS-004), not from A-23. A-23 supports Finding M-1 only." Resolves R-002 |
| 3 | Methodological Rigor | 0.92 | 0.94 | Add a sentence to ST-7 explicitly recommending that Phase 5 obtain independent methods review of the pilot design from outside the PROJ-014 pipeline before launch; add this as a Phase 5 adversary gate verification item in ST-5; partially resolves R-004 |
| 4 | Traceability | 0.96 | 0.97 | Add one row to ST-5 Phase 5 adversary gate requirements: "Obtain and document independent methods review (RT-004-i1 deferred item)" to create a verifiable traceability chain from the deferred finding to a gate checkpoint |
| 5 | Evidence Quality | 0.94 | 0.95 | Change "3+ vendors" in L2 confidence reconciliation matrix to explicit distribution: "3 vendors (Anthropic primary: ~30 instances; OpenAI: C-6, C-7; LlamaIndex: C-11)" — resolves R-006 |

**Projected composite if all 5 recommendations addressed:** 0.950–0.955 (borderline PASS at C4 threshold; contingent on verification of implementation quality).

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific section citations
- [x] Uncertain scores resolved downward (Actionability held at 0.88 despite substantial improvement; considered 0.90 but downgraded due to persistent R-001 ownership gap)
- [x] First-draft calibration not applicable (this is I2 revision, not a first draft)
- [x] No dimension scored above 0.95 without exceptional documented evidence (Traceability at 0.96 is justified by the explicit revision log, finding-by-finding checklist, and comprehensive cross-linking)
- [x] C4 threshold of 0.95 applied literally — composite of 0.927 is below threshold despite strong improvement arc from 0.868

**Anti-leniency note:** The I1 → I2 improvement of +0.059 composite is substantial and reflects genuine structural work. The temptation is to score this as a PASS given the evident care in the revision. The critical counteraction: the three persistent actionability gaps (R-001 ownership, R-002 PG-003 proximity, R-003 no orchestration link) are genuine risks at C4 criticality where downstream consumers may misapply these findings in irreversible research design decisions. The synthesis has not yet earned the "near-perfect" standard that 0.95 requires. Scoring held at 0.927.

**Calibration verification:**
- 0.927 composite maps to: strong work with targeted refinements needed (calibration anchor: 0.85 = strong work with minor refinements)
- This is above 0.85 but below 0.92 calibration anchor, consistent with "strong work" that has not yet reached the "genuinely excellent" threshold
- The score is plausible for a C4 I2 revision that resolves all Critical and 16 of 19 Major findings but retains one Major and five Minor residual gaps

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.927
threshold: 0.95
weakest_dimension: actionability
weakest_score: 0.88
critical_findings_count: 0
major_findings_remaining: 1
minor_findings_remaining: 5
iteration: 2
prior_score: 0.868
score_delta: +0.059
distance_to_threshold: -0.023
improvement_recommendations:
  - "Add Owner and Timeline columns to ST-7 BLOCKING prerequisites table (resolves R-001: highest priority)"
  - "Add separating sentence in ST-4 between Finding M-1 (A-23 T1) and PG-003 (T4) to prevent conflation (resolves R-002)"
  - "Add independent methods review recommendation to ST-7 and Phase 5 adversary gate in ST-5 (partially resolves R-004)"
  - "Add Phase 5 adversary gate item for external methods review traceability (resolves deferred RT-004-i1)"
  - "Change '3+ vendors' to explicit distribution in L2 confidence reconciliation matrix (resolves R-006)"
projected_pass_score_if_resolved: 0.950_to_0.955
i1_critical_findings_resolved: 5
i1_major_findings_resolved: 16
i1_minor_findings_resolved: 12
```

---

*Score Report Version: I2*
*Scoring Agent: adv-scorer*
*Constitutional Compliance: P-003, P-020, P-022*
*SSOT: `.context/rules/quality-enforcement.md`*
*Created: 2026-02-28*
*Deliverable: barrier-2/synthesis.md (v2.0.0)*
*I1 Report: barrier-2/adversary-synthesis-i1.md*
