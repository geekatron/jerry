# Adversarial Review: FEAT-040-056 OSS Documentation Best-Practices Research

## Execution Context

| Field | Value |
|-------|-------|
| **Feature** | FEAT-040-056 |
| **Strategies Executed** | S-007, S-002, S-014, S-004, S-012, S-013 |
| **Criticality** | C3 |
| **Threshold** | 0.92 |
| **Iteration** | 1 of 7 |
| **Deliverable** | `projects/PROJ-040-documentation/work/EPIC-040-001/research/FEAT-040-056/ps-researcher-output.md` |
| **Executed** | 2026-04-17 |
| **Self-Reported Score** | 0.90 |
| **Verified Score** | 0.859 |
| **Verdict** | REVISE — BELOW C3 THRESHOLD |

**H-16 Note:** S-003 (Steelman) was not formally executed prior to S-002. Per protocol, S-002 was executed using internal steelmanning. No H-16 violation is generated for the executor; however, the orchestrator should schedule a formal S-003 pass before iteration 2 if S-002 is re-run.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Findings Summary](#findings-summary) | All findings by severity across all strategies |
| [S-007 Constitutional AI Critique](#s-007-constitutional-ai-critique) | Principle-by-principle compliance review |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Counter-arguments against key claims |
| [S-014 LLM-as-Judge](#s-014-llm-as-judge) | Dimensional scoring with composite |
| [S-004 Pre-Mortem](#s-004-pre-mortem) | Prospective failure analysis |
| [S-012 FMEA](#s-012-fmea) | Component-level failure modes and RPN |
| [S-013 Inversion](#s-013-inversion) | Goal inversion and assumption stress-tests |
| [Convergent Findings](#convergent-findings) | Defects confirmed across multiple strategies |
| [Score Challenge](#score-challenge) | Verification of self-reported 0.90 vs actual 0.859 |
| [Revision Requirements](#revision-requirements) | Priority-ordered action list for iteration 2 |

---

## Findings Summary

| ID | Strategy | Severity | Finding | Section |
|----|----------|----------|---------|---------|
| FM-001 | S-012 FMEA | Critical | NumPy NEP 44 cited as production deployment in L0; it is a proposal (RPN 504) | L0 Executive Summary |
| FM-004 | S-012 FMEA | Critical | Human command-execution verification recommendation has no process, owner, or acceptance criteria (RPN 240) | L2 Recommendations rank 7 |
| FM-002 | S-012 FMEA | Critical | Evidence classification "~60% direct" is self-assessed; DORA chain citation, Mintlify vendor-reported data undermine the claim (RPN 294) | L1 Methodology |
| FM-003 | S-012 FMEA | Critical | Wave 2-4 retroactive Google style guide application creates scope ambiguity — no resolution when Vale CI gates land in Wave 5 (RPN 210) | L2 Recommendations rank 1 |
| FM-005 | S-012 FMEA | Critical | HEART metrics for docs acknowledged as "genuinely rare in OSS" but risk to ux-heart-analyst wave (no OSS baselines) is deferred, not mitigated (RPN 210) | Section 2.8 Measurement |
| DA-001 | S-002 | Major | "Validated at scale" list overstated — Gatsby is a minor case; NumPy NEP 44 is a proposal; evidence base for Diataxis scalability is 2-3 projects, not 6 | L0 finding #1, Section 2.1 |
| DA-002 | S-002 | Major | "Jerry already matches field consensus" is self-referential validation — confirming evidence selected; no sources challenge LLM-as-judge for structured documentation domains | Section 2.9, L0 finding #5 |
| DA-004 | S-002 | Major | "~60% direct citation" self-report is generous — several key recommendations rest on secondary advocacy articles, vendor-reported metrics, and a 2020 baseline | L1 Methodology, end note |
| CC-001 | S-007 | Major | L0 summary and L2 D-01 are inconsistent: L0 claims NumPy NEP 44 as validated; L2 correctly identifies it as a proposal | L0 vs Section 2.1 Finding D-01 |
| IN-001 | S-013 | Major | Confirmation bias anti-pattern: all recommendations frame Jerry's existing practices favorably; no finding challenges any core Jerry approach | L0 findings, Section 2.9 |
| IN-002 | S-013 | Major | Anti-goal for evidence quality confirmed: NumPy NEP 44 cited as production deployment (convergent with CC-001, DA-001, FM-001) | L0 Executive Summary |
| IN-003 | S-013 | Major | Anti-goal for actionability confirmed: human HITL recommendation lacks mechanism (convergent with PM-004, FM-004) | L2 Recommendations rank 7 |
| PM-001 | S-004 | Major | Diataxis quadrant ratios unknown for skill-based framework (OQ-1) but Waves 4a/4b proceed as highest-priority without resolving this | Open Questions, L0 finding #1 |
| PM-002 | S-004 | Major | Vale + Google style integration risk: Jerry-specific syntax patterns (`/skill`, agent names, H-rule notation) may trigger false-positive style violations; no calibration plan | L2 Recommendations rank 2 |
| PM-003 | S-004 | Major | Wave 2 README optimization premised on assumption that README is primary discovery path; OQ-2 flags this as unknown | L0 finding #4, Open Questions |
| PM-004 | S-004 | Critical | Human command-execution verification (Wave 4a) has no defined process owner or criteria — most important HITL recommendation is operationally hollow | L2 Recommendations rank 7, Section 2.9 |
| FM-007 | S-012 FMEA | Major | OQ-7 (solo maintainer sustainability) is treated as academic gap but directly applies to PROJ-040; no post-Wave-5 maintenance plan assessed | Open Questions OQ-7 |
| FM-008 | S-012 FMEA | Major | SD-01 (navigation vs. search) rests on 2020 Optimal Workshop baseline with no 2024 update — absence of contradicting data is not confirmation | Section 2.5, References |
| DA-003 | S-002 | Minor | Vale recommendation does not address cost of rule tuning for Jerry-specific patterns | L2 Recommendations rank 2 |
| DA-005 | S-002 | Minor | OQ-4 is flagged open but answered within the same section — structural inconsistency | Open Questions OQ-4, Section 2.9 |
| IN-004 | S-013 | Minor | Assumption: Vale + Google is cheaper than house style — not costed; Jerry already has a defined voice system (saucer-boy-framework-voice) that partial Vale integration may conflict with | L2 Recommendations rank 1-2 |
| IN-005 | S-013 | Minor | Tutorial/how-to separation attributed specifically to Diataxis with no control group; any structured IA intervention may achieve similar results | L0 finding #1, Section 2.1 |
| CC-002 | S-007 | Minor | WCAG 3.0 "substantially-complete draft expected early 2026" may be stale or inaccurate as of April 2026 | Section 2.4 Finding A-01 |

---

## S-007 Constitutional AI Critique

**Strategy:** S-007 Constitutional AI Critique
**Finding Prefix:** CC
**Deliverable type:** Research document
**Applicable principles:** P-001 (Accuracy), P-022 (No Deception/Confidence), H-23 (Navigation table), H-24 (Anchor links)

### Findings

#### CC-001 [Major] — L0/L2 Inconsistency on NumPy NEP 44

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L0 Executive Summary vs Section 2.1 Finding D-01 |
| **Principle** | P-001 (Truth/Accuracy) — MEDIUM tier violation |

**Evidence:**
- L0 finding #1 (line 35): "Cloudflare, Canonical, Django, NumPy (via NEP 44)" listed as validated production Diataxis deployments
- Section 2.1 D-01 (line 94): "NumPy has a formal restructure proposal (NEP 44) that adopts Diataxis as its target architecture"

**Analysis:** The executive summary (the highest-visibility output section) asserts NumPy as a validated production deployment. The L2 body correctly identifies NEP 44 as a proposal. Readers who consume only the L0 will make planning decisions based on an overstated evidence base for Diataxis scalability. This is an internal consistency failure that also implicates P-001 accuracy.

**Recommendation:** Revise L0 finding #1 to distinguish completed deployments (Cloudflare, Canonical, Django) from in-progress restructures (NumPy NEP 44 — proposal). Add qualifier: "NumPy has a formal restructure proposal (NEP 44) adopting Diataxis but has not yet completed migration."

---

#### CC-002 [Minor] — Potentially Stale WCAG 3.0 Timeline

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Section 2.4 Finding A-01 |
| **Principle** | P-001 (Accuracy) — SOFT tier |

**Evidence:** Finding A-01 (line 151): "WCAG 3.0 is in Working Draft as of September 2025 with a substantially-complete draft expected in early 2026."

**Analysis:** The research is dated April 2026. WCAG 3.0 remains in Working Draft. The prediction "expected in early 2026" has passed without fulfillment. The claim is technically qualified ("expected") but may mislead readers about WCAG 3.0's current status.

**Recommendation:** Update to "As of April 2026, WCAG 3.0 remains in Working Draft; the substantially-complete milestone has not yet been reached."

---

**Constitutional Compliance Score:** 1.00 - 0.05 (1 Major) - 0.02 (1 Minor) = **0.93 — PASS** (constitutional gate cleared, but CC-001 impacts Internal Consistency in S-014).

**Compliant items:** H-23 (navigation table present), H-24 (anchor links used), P-002 (persisted), P-004 (provenance cited), structured evidence classification.

---

## S-002 Devil's Advocate

**Strategy:** S-002 Devil's Advocate
**Finding Prefix:** DA
**H-16 Note:** S-003 not formally executed prior. Internal steelmanning applied. No H-16 violation generated by executor; orchestrator should schedule formal S-003 in the revision sequence.

### Summary

5 counter-arguments identified (0 Critical, 3 Major, 2 Minor). The deliverable is well-structured and the Diataxis/Vale core recommendations are broadly sound, but three significant weaknesses undermine its credibility: an overstated evidence list for Diataxis adoption, systematic self-referential validation bias, and an inflated evidence classification claim. The HITL recommendation is directionally correct but operationally hollow.

### Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001 | "Validated at scale" Diataxis list overstates evidence | Major | L0 finding #1 lists 6 projects; NumPy is a proposal, Gatsby is minor; core evidence is 2-3 strong cases | Evidence Quality |
| DA-002 | Self-referential validation bias in AI-docs alignment | Major | Section 2.9: "Jerry already matches 2026 AI-docs consensus" — all evidence selected confirms Jerry's existing approach | Methodological Rigor |
| DA-004 | "~60% direct citation" self-report is generous | Major | L1 Methodology: DORA chain-cited, Mintlify vendor-reported, SD-01 is 2020 baseline | Evidence Quality |
| DA-003 | Vale rule tuning cost not addressed | Minor | Recommendations rank 2: "cheaper than hand-authored style guide" without cost estimate for rule calibration | Actionability |
| DA-005 | OQ-4 flagged open but answered in same document | Minor | Open Questions OQ-4 vs Section 2.9 last paragraph | Internal Consistency |

### Detailed Findings

#### DA-001: Diataxis "Validated at Scale" List Overstated [Major]

**Claim Challenged:** L0 finding #1: "Cloudflare, Canonical/Ubuntu, Django, Python, Gatsby, and NumPy (via NEP 44) have all restructured around Diataxis."

**Counter-Argument:** The list conflates projects of very different scales and completion levels. NumPy NEP 44 is explicitly a proposal in L2. Gatsby is a JavaScript build framework that uses Diataxis in its own docs site — this is not the same scale as Canonical's full Ubuntu documentation restructure or Cloudflare's developer docs. The Python community docs reference is vague. The actual strong production evidence is: Cloudflare, Canonical, Django — 3 projects. Presenting 6 signals a broader validation than the evidence supports.

**Evidence:** L2 D-01 (line 94): "NumPy has a formal restructure proposal (NEP 44)." L2 D-01 does not list Python community docs as a validated restructure — this appears only in L0.

**Impact:** PROJ-040 Wave 4a/4b prioritization is based on Diataxis being "validated at scale" across many projects. If validation is weaker than claimed, the risk of restructuring Jerry's docs around Diataxis is higher than assessed.

**Response Required:** Revise L0 to accurately enumerate: completed restructures (Cloudflare, Canonical, Django), in-progress/proposed (NumPy NEP 44), minor adoptions (Gatsby). Acceptance criteria: L0 claims match L2 evidence exactly.

---

#### DA-002: Self-Referential Validation Bias [Major]

**Claim Challenged:** L0 finding #5: "Jerry's /adversary skill with C4 >= 0.95 plus independent reviewer (Wave 2 #100 AC-6) is already aligned with the field."

**Counter-Argument:** The research is commissioned to inform PROJ-040 — a project that already has an approach. The finding that "Jerry already does this correctly" for the most important AI-docs recommendation (HITL review) should trigger additional scrutiny, not acceptance. No source in the research challenges whether Jerry's specific LLM-as-judge configuration (S-014 six-dimension rubric, tournament scoring) is calibrated for documentation quality vs. code quality. The 60-70% SME agreement figure (AI-03) comes from Comet and Maxim AI — commercial HITL vendors with inherent incentive to emphasize human oversight. No source in the research questions whether S-014 might perform better than average LLM judges for structured documentation review.

**Evidence:** Section 2.9 PROJ-040 relevance (line 258): "Jerry's creator-critic-revision pattern (H-14) with C4 >= 0.95 adversarial tournament plus independent reviewer for Wave 2 is already the field-consensus pattern applied at an above-median rigor level."

**Impact:** If S-014 is actually effective at detecting documentation defects, the elaborate independent reviewer process may be over-engineered. If it is not, the recommendation to "keep the independent reviewer" needs stronger evidence than self-affirmation.

**Response Required:** Add at least one source that either (a) validates LLM-as-judge specifically for structured documentation review quality, or (b) questions the 60-70% SME agreement figure's applicability to rule-governed documentation domains. Acceptance criteria: evidence is bidirectional, not purely confirmatory.

---

#### DA-004: Evidence Classification Self-Report Overstated [Major]

**Claim Challenged:** End note (line 411): "Evidence classification: ~60% direct citation, ~30% synthesis, ~10% labeled inference."

**Counter-Argument:** Systematic review of the findings reveals the 60% figure is optimistic. DORA 2023 25% figure is cited "via Write the Docs 2024 takeaways" — chain citation. Mintlify "8-figure ARR, 10K+ customers, 1M+ monthly AI queries" (line 241) is vendor-reported only. Nielsen Norman navigation research (SD-01, lines 166-167) acknowledges "2020 baseline, with no contradicting 2024 data surfaced" — absence of contradiction is not direct citation evidence. Several key style guide recommendations (S-02: "industry-accepted guidance" from "multiple 2024-2026 style-guide comparison articles") cite secondary advocacy content. The actual direct citation percentage for key decision-influencing claims (DORA, Mintlify, Nielsen Norman, style guide recommendations) is closer to 40-45%, not 60%.

**Evidence:** L1 Methodology evidence classification definition (lines 77-79) defines "Direct" as named project explicitly documenting the practice. Many findings meeting this definition are for tool-adoption facts (Vale vendor list, Docusaurus versioning guidance) which are lower-stakes than the evidence claimed for primary recommendations (DORA, HITL).

**Response Required:** Revise the evidence classification ratio to reflect actual distribution, or add a qualifier distinguishing evidence quality by recommendation tier (structural tool recommendations vs. strategic process recommendations). Acceptance criteria: classification notes which high-stakes recommendations rest on chain citations or vendor-reported data.

---

### Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Neutral | All 9 areas covered; no missing research area |
| Internal Consistency | Negative | DA-005 (OQ-4 open but answered); DA-001 (L0 vs L2 NEP 44) |
| Methodological Rigor | Negative | DA-002 (systematic confirmation bias in evidence selection) |
| Evidence Quality | Negative | DA-001 (overstated adoption list), DA-004 (inflated classification) |
| Actionability | Negative (Minor) | DA-003 (Vale calibration cost unaddressed) |
| Traceability | Neutral | Citations present; chain citation issue captured in Evidence Quality |

---

## S-014 LLM-as-Judge

**Strategy:** S-014 LLM-as-Judge
**Finding Prefix:** LJ
**Criticality:** C3 (REQUIRED)

### Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.859 |
| **Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE |
| **Self-Reported Score** | 0.90 |
| **Score Challenge** | -0.041 (actual below self-report) |
| **Weakest Dimension** | Evidence Quality (0.81) |

### Dimension Scores

| Dimension | Weight | Score | Weighted | Severity | Evidence Summary |
|-----------|--------|-------|----------|----------|------------------|
| Completeness | 0.20 | 0.88 | 0.176 | Minor | All 9 areas covered; DORA 2023 is chain-cited (no primary source access); CHASE 2025 link is a conference detail page |
| Internal Consistency | 0.20 | 0.83 | 0.166 | Major | L0 says NumPy NEP 44 is validated; L2 D-01 correctly says it is a proposal; OQ-4 flagged open but answered in same section |
| Methodological Rigor | 0.20 | 0.85 | 0.170 | Minor | Inclusion criteria and evidence classification documented; Context7 MCP non-use justified; SD-01 2020 baseline not explicitly flagged in findings |
| Evidence Quality | 0.15 | 0.81 | 0.122 | Major | DORA chain-cited; Mintlify vendor-reported; Nielsen Norman 2020 baseline; "~60% direct" overstated |
| Actionability | 0.15 | 0.91 | 0.137 | Minor | 10 ranked recommendations with wave assignments; Vale specifies Google rules as starting point; HITL recommendation is directionally correct but mechanistically hollow |
| Traceability | 0.10 | 0.88 | 0.088 | Minor | Evidence labels on each finding; L0 traces to L2; CHASE 2025 citation is a conference page not paper access |
| **TOTAL** | **1.00** | | **0.859** | | |

**Computation verification:**
```
(0.88 × 0.20) + (0.83 × 0.20) + (0.85 × 0.20) + (0.81 × 0.15) + (0.91 × 0.15) + (0.88 × 0.10)
= 0.176 + 0.166 + 0.170 + 0.122 + 0.137 + 0.088
= 0.859
```

### Detailed Dimension Analysis

#### Completeness (0.88/1.00) — Minor

**Evidence:** All 9 research areas scoped in the state file are present as L2 sections. L0/L1/L2 structure is complete. Recommended patterns (10 items) and anti-patterns (8 items) are present. Open questions documented (7 items). References grouped by area with 40+ citations.

**Gaps:** DORA 2023 25% performance correlation figure is not sourced from the original report — only from Write the Docs 2024 secondary writeups. This is the single most-cited empirical claim ("docs quality correlates with 25% higher team performance") and lacks primary source verification. CHASE 2025 reference links to a conference detail page, not the paper content.

**Improvement Path:** Add primary source access for DORA 2023 claim: either direct citation to the DORA 2023 PDF with page number, or flag explicitly as "sourced via secondary summary, primary source not independently verified." Target: 0.92.

---

#### Internal Consistency (0.83/1.00) — Major

**Evidence:**
- Inconsistency 1: L0 finding #1 (line 35) lists "NumPy (via NEP 44)" in a sentence about projects that "have all restructured around Diataxis." Section 2.1 D-01 (line 94) states "NumPy has a formal restructure proposal (NEP 44) that adopts Diataxis as its target architecture." These directly contradict.
- Inconsistency 2: Open Question OQ-4 (line 313) asks "Can /adversary tournaments substitute for independent human review at C4? Current practice says no." Section 2.9 PROJ-040 relevance (line 258) provides a complete answer to this question. The question should not appear in Open Questions.

**Gaps:** Two factual inconsistencies between document sections. The L0/L2 inconsistency is the more serious — it affects decision-making for the highest-visibility consumers.

**Improvement Path:** (1) Revise L0 to separate completed restructures from proposals. (2) Close OQ-4 by noting it is answered in Section 2.9. Target: 0.92.

---

#### Methodological Rigor (0.85/1.00) — Minor

**Evidence:** Inclusion criteria are explicit and tiered (primary > secondary > tertiary). Evidence classification (direct/synthesis/inference) is applied per finding. Known gaps are acknowledged (lines 83-87). Context7 MCP exception justified. Research window is clearly bounded (2023-2026, primary weight 2024-2026).

**Gaps:** SD-01 (navigation vs. search, Section 2.5) cites "2020 baseline, with no contradicting 2024 data surfaced" — this acknowledgment appears only in the source description (line 166), not in the finding itself or in the Recommendations section where the 3-tier discovery model is built on it. The research correctly flags it in methodology but does not propagate the staleness caveat into the downstream recommendation.

**Improvement Path:** Add staleness caveat to Finding SD-01 and recommendation rank 4 (cross-linking). Note that the three-tier discovery model is partially built on 2020 navigation research and the AI-search layer (2025-2026) is the better-evidenced component. Target: 0.92.

---

#### Evidence Quality (0.81/1.00) — Major

**Evidence of gaps:**
1. DORA 2023 25% figure: cited as "DORA 2023 State of DevOps Report (cited via Write the Docs 2024 takeaways)" — chain citation. The figure appears in L0 finding #3, Findings W-02, and is the canonical justification for "why docs quality matters." Primary source not verified.
2. Mintlify metrics (Section 2.9 Finding AI-01): "8-figure ARR, 10,000+ customers, 1M+ monthly AI queries" — vendor's own year-in-review blog post. No independent confirmation.
3. Nielsen Norman/Optimal Workshop (Finding SD-01): "2020 baseline, with no contradicting 2024 data surfaced" — acknowledged staleness.
4. "Multiple 2024-2026 style-guide comparison articles" (Finding S-02): The recommendation to adopt Google's guide rather than write one rests on "industry-accepted guidance" from secondary comparison articles, which are themselves advocacy pieces. No primary empirical study comparing outcomes of adopted vs. house style guides is cited.

**Improvement Path:** (1) Obtain primary source access for DORA 2023 or explicitly flag as unverified chain citation. (2) Flag Mintlify metrics as vendor-reported in Finding AI-01. (3) Add qualifier to S-02 recommendation noting the evidence base is secondary/advocacy. (4) Revise "~60% direct" evidence classification to acknowledge key decision-relevant claims rest on chain citations. Target: 0.88 (full resolution to 0.92 requires primary source verification outside scope of this revision).

---

#### Actionability (0.91/1.00) — Minor

**Evidence of strength:** 10 recommendations ranked with rationale, evidence tier, and wave assignment. Vale recommendation specifies "Google developer documentation style guide as a starting rule set, not a hand-authored house style." Human command-execution verification for Wave 4a is specific about insertion point. CONTRIBUTING.md recommendation has CHASE 2025 evidence. Broken-link CI check is immediately actionable.

**Gap:** Recommendation rank 7 (human command-execution verification, line 274): "For Wave 4 skill tutorials, add a human sanity-check step specifically for executable commands and file paths." Who performs this check? At what point in the workflow? What is the pass/fail criterion? The recommendation identifies the HITL insertion point but provides no operational process. Given this is flagged as preventing "the 30% defect rate" (the highest-severity AI-docs risk), the lack of a defined process is a meaningful gap.

**Improvement Path:** Add a defined process for human command-execution verification: reviewer role, checklist (commands executed on fresh Jerry install, paths verified, expected output documented), acceptance criteria. Target: 0.95.

---

#### Traceability (0.88/1.00) — Minor

**Evidence:** Evidence labels (direct/synthesis/inference) on each finding. L0 recommendations trace to specific L2 section citations. References grouped by area. Wave assignments connect to PROJ-040 structure. PROJ-040 relevance sections close each research area.

**Gap:** CHASE 2025 citation (line 373) links to a conference proceedings detail page. The paper "The Introduction of README and CONTRIBUTING Files in Open Source Software Development" may not be publicly accessible from that URL. The finding C-01 (projects add CONTRIBUTING reactively) rests entirely on this paper. If the citation is not verifiable, C-01 loses its empirical basis and reverts to inference.

**Improvement Path:** Verify CHASE 2025 paper accessibility and add direct quotation from the paper abstract or findings to Finding C-01. If not accessible, reclassify C-01 as synthesis/inference. Target: 0.92.

---

### Verdict Rationale

**Verdict: REVISE**

Composite 0.859 is below the H-13 C3 threshold of 0.92. The gap is 0.061. Two dimensions score in Major territory (Internal Consistency 0.83, Evidence Quality 0.81). No dimensions score Critical (<0.50). The deliverable is not fundamentally flawed — the research direction is correct and most recommendations are actionable. The gaps are concentrated in evidence quality (chain citations, vendor-reported data, stale baseline) and internal consistency (L0/L2 NumPy discrepancy). These are addressable in a targeted revision without restructuring the research.

---

## S-004 Pre-Mortem

**Strategy:** S-004 Pre-Mortem Analysis
**Finding Prefix:** PM
**Failure Scenario:** "It is October 2026. PROJ-040 has launched. External contributors and new users report the Jerry docs are confusing, tutorials have broken commands, and the documentation system is inconsistent. The OSS release has not improved adoption metrics."

### Failure Cause Inventory

| ID | Category | Finding | Likelihood | Severity | Dimension |
|----|----------|---------|------------|----------|-----------|
| PM-004 | Process | Human command-execution verification for Wave 4a has no process, owner, or criteria | High | Critical | Actionability |
| PM-002 | Technical | Vale + Google style generates false-positive violations on Jerry-specific syntax patterns | High | Major | Methodological Rigor |
| PM-001 | Assumption | Diataxis quadrant ratios unknown for skill-based framework; Waves 4a/4b proceed without resolving OQ-1 | Medium | Major | Completeness |
| PM-003 | Assumption | Wave 2 README optimization assumes README is primary discovery path; OQ-2 says this is unknown | Medium | Major | Evidence Quality |
| PM-006 | Assumption | Diataxis frontmatter tags assumed to support AI-era retrieval but no evidence LLM/RAG systems honor frontmatter for routing | Medium | Minor | Evidence Quality |
| PM-005 | External | HITL 60-70% SME agreement figure may be overstated by commercial vendors | Low | Minor | Evidence Quality |

### Priority Matrix

**P0 (Immediate — MUST mitigate):**

**PM-004:** The most operationally hollow recommendation in the research is the one with the highest cited stakes ("prevents 30% defect rate"). Define the process before Wave 4a begins: who performs command execution verification, what constitutes the checklist, what is the pass/fail criterion, and where in the workflow this step occurs.

**P1 (Important — SHOULD mitigate):**

**PM-002:** Before committing to Vale + Google style guide in Wave 5, run Vale on a sample of existing Jerry docs to identify false-positive rate for Jerry-specific patterns. Patterns at risk: `/skill` syntax, agent names (adv-selector, ps-researcher), H-rule notation (H-01 through H-36), finding prefixes (DA-001, FM-001), saucer-boy voice phrases. Acceptance criteria: Vale rule customization plan documented before CI integration.

**PM-001:** Address OQ-1 (Diataxis quadrant ratios) with at least a stated hypothesis before Wave 4a begins. Proposed answer from internal evidence: tutorials and how-tos are the dominant quadrant for skills (per D-03); reference is auto-generated from docstrings; explanation is lowest priority. Document this as a hypothesis to be validated after Wave 4 launch, not an open question.

**PM-003:** Address OQ-2 (discovery path) with a hypothesis or weak evidence. Options: (a) instrument `/help` usage in Jerry CLI to measure current discovery, (b) state explicitly that README optimization is a safe bet regardless of discovery path since README is always-visible. If (b), close OQ-2 as "addressed by safe-bet rationale."

**P2 (Monitor):**

**PM-006:** Flag Diataxis frontmatter tags as "low-cost, future-proofing" rather than presenting it as AI-era functionality. Add caveat that current LLM systems do not have confirmed frontmatter-routing behavior.

**PM-005:** Flag Mintlify and Maxim AI vendor-origin explicitly in citations.

---

## S-012 FMEA

**Strategy:** S-012 FMEA
**Finding Prefix:** FM

### Element Decomposition

| Element | Description |
|---------|-------------|
| E-01 | L0 Executive Summary (5 findings, primary consumer-facing output) |
| E-02 | L1 Methodology (sources, inclusion criteria, evidence classification claim) |
| E-03 | L2.1 Diataxis findings (D-01 through D-05 + migration patterns) |
| E-04 | L2.2-L2.4 Write the Docs, Style Guides, Accessibility |
| E-05 | L2.5-L2.6 Search/Discovery, Versioning |
| E-06 | L2.7-L2.9 Contribution Patterns, Measurement, AI-Assisted Docs |
| E-07 | L2 Recommendations table (10 ranked items) |
| E-08 | L2 Patterns to Avoid (8 anti-patterns) |
| E-09 | L2 Open Questions (7 items) |
| E-10 | References section (40+ citations) |

### Critical Failure Modes (RPN >= 200)

| ID | Element | Failure Mode | Effect | S | O | D | RPN | Severity |
|----|---------|-------------|--------|---|---|---|-----|----------|
| FM-001 | E-01 | Incorrect: NumPy NEP 44 listed as production deployment in L0 | Downstream work planned on inflated Diataxis validation evidence | 7 | 9 | 8 | 504 | Critical |
| FM-002 | E-02 | Insufficient: "~60% direct citation" self-assessed; DORA chain-cited; Mintlify vendor-reported | Decision-makers calibrate on overstated evidence quality assurance | 6 | 7 | 7 | 294 | Critical |
| FM-004 | E-07 | Missing: Human command-execution verification has no process, owner, or acceptance criteria | The only HITL recommendation with cited 30% defect-rate stakes is operationally hollow | 8 | 6 | 5 | 240 | Critical |
| FM-003 | E-07 | Ambiguous: Retroactive Wave 2-4 Google style application scope — when Vale CI gates land in Wave 5, unclear if prior work needs rework | Scope creep / rework risk at Wave 5 launch | 5 | 7 | 6 | 210 | Critical |
| FM-005 | E-06 | Insufficient: HEART metrics documented as "genuinely rare" but risk to ux-heart-analyst (no OSS baselines) is deferred | ux-heart-analyst wave plans against unverifiable baselines | 6 | 5 | 7 | 210 | Critical |

### Major Failure Modes (RPN 80-199)

| ID | Element | Failure Mode | Effect | S | O | D | RPN | Severity |
|----|---------|-------------|--------|---|---|---|-----|----------|
| FM-007 | E-09 | Insufficient: OQ-7 (solo maintainer sustainability) treated as academic gap | Post-Wave-5 maintenance not planned; applies directly to PROJ-040 | 7 | 5 | 5 | 175 | Major |
| FM-008 | E-05 | Stale: SD-01 rests on 2020 Optimal Workshop research | Three-tier discovery model partially built on 6-year-old navigation data | 5 | 6 | 6 | 180 | Major |

### Corrective Actions

| ID | Current RPN | Corrective Action | Estimated Post-Correction RPN |
|----|------------|-------------------|-------------------------------|
| FM-001 | 504 | Revise L0 finding #1 to separate completed deployments from proposals/in-progress | S=7, O=1, D=2 → 14 |
| FM-002 | 294 | Add qualifier to evidence classification; flag DORA chain citation; flag Mintlify vendor-reported | S=5, O=4, D=4 → 80 |
| FM-004 | 240 | Define human command-execution verification process: reviewer role, checklist, acceptance criteria | S=8, O=3, D=2 → 48 |
| FM-003 | 210 | Add explicit scope guidance: "Waves 2-4 apply Google guide as authoring reference; Vale CI enforces in Wave 5 — no retroactive rework required if prose follows the style" | S=3, O=3, D=3 → 27 |
| FM-005 | 210 | Add risk statement to HEART measurement section: "No OSS baseline exists for HEART docs metrics; ux-heart-analyst should plan to establish baselines, not measure against existing benchmarks" | S=4, O=3, D=4 → 48 |
| FM-007 | 175 | Close OQ-7 with PROJ-040-specific guidance: "As a solo-maintainer framework, sustainability plan for post-Wave-5 maintenance should be scoped in EPIC-040 retrospective" | S=5, O=3, D=3 → 45 |
| FM-008 | 180 | Add caveat to SD-01: "2020 baseline; three-tier discovery model recommendation built primarily on AI-search (2025-2026 evidence) for the conversational tier and on inference for its current developer-docs applicability" | S=4, O=4, D=3 → 48 |

**Total current RPN (Critical items):** 504 + 294 + 240 + 210 + 210 = **1,458**
**Total post-correction RPN (estimated):** 14 + 80 + 48 + 27 + 48 = **217**
**RPN reduction:** 85%

---

## S-013 Inversion

**Strategy:** S-013 Inversion Technique
**Finding Prefix:** IN

### Goal Inventory

| ID | Goal | Type | Specificity |
|----|------|------|-------------|
| G-1 | Provide actionable recommendations for PROJ-040 Waves 2-5 | Explicit | Clear |
| G-2 | Establish evidence-based confidence in Diataxis adoption | Explicit | Clear |
| G-3 | Give Jerry a defensible style/quality framework | Explicit | Clear |
| G-4 | Align Jerry's existing practices with field consensus | Implicit | Present — all major L0 findings contain "Jerry already does X" or "Jerry should add Y minor step" |
| G-5 | Provide research findings stakeholders can trust as objective | Implicit | Assumed by L0 consumer |

### Anti-Goal Analysis

**Anti-goal for G-4:** "To guarantee Jerry's practices appear misaligned with field consensus, cite evidence that contradicts Jerry's approach."

**Inversion result (IN-001):** The research does NOT cite any source that contradicts Jerry's core approach. No finding states "field practice X is inconsistent with Jerry's approach Y." All five L0 findings are framed as confirming Jerry's existing direction:
- Finding 1: Diataxis — "Wave 4a/4b priorities are correct"
- Finding 2: Vale — "add Vale in Wave 5" (minor addition)
- Finding 3: Docs-as-code — "treat every snippet as testable" (extension of existing approach)
- Finding 4: Search/discovery — "Wave 2 README should surface Diataxis quadrants" (minor refinement)
- Finding 5: AI-HITL — "Jerry already aligned"

This is not necessarily wrong — Jerry's approach may genuinely align with field consensus. But a research deliverable for C3 quality should demonstrate that disconfirming evidence was sought and found absent, not simply that confirming evidence was found. Severity: **Major** (affects Methodological Rigor).

**Anti-goal for G-2 (IN-002):** "To undermine Diataxis evidence quality, cite proposals as completed restructures."

**Inversion result:** Finding confirmed — NumPy NEP 44 appears in L0 as a production deployment. This anti-goal condition is present in the deliverable. Severity: **Major** (convergent with CC-001, DA-001, FM-001).

**Anti-goal for G-1 (IN-003):** "To guarantee recommendations are not actionable, make the most important one vague."

**Inversion result:** Finding confirmed — recommendation rank 7 (human command-execution verification) lacks a process definition. The "most important" qualifier is supported by the document's own framing: this recommendation prevents the "30% defect rate" cited as the primary AI-docs risk. Severity: **Major** (convergent with PM-004, FM-004).

### Assumption Stress-Tests

| ID | Assumption | Confidence | Inversion | Plausibility | Severity | Dimension |
|----|-----------|------------|-----------|--------------|----------|-----------|
| IN-004 | Vale + Google is cheaper than a house style guide | Medium | "Vale + Google is MORE expensive" — 800+ Google rules, ongoing calibration, potential conflict with Jerry's existing voice system (saucer-boy-framework-voice) | Plausible: Jerry already has defined voice; Vale rules may flag Jerry's intentional voice as violations | Minor | Actionability |
| IN-005 | Tutorial/how-to separation is specifically the Diataxis 80% win | Medium | "Any structured IA intervention achieves similar results" — no control group in cited studies | Plausible: all Diataxis studies are observational; attribution to the specific tutorial/how-to separation is an inference | Minor | Evidence Quality |

### Mitigation Plan

**IN-001 (Major):** Add a dedicated "Challenging Evidence" subsection to L1 Methodology or L0 stating: "Field practices where Jerry's current approach diverges from documented consensus, or where the evidence is ambiguous." If no divergences exist, state this explicitly with supporting analysis. This transforms the absence of disconfirming evidence from an omission artifact into a documented research finding.

**IN-002 (Major):** Resolved by CC-001/DA-001/FM-001 corrective action (revise NumPy NEP 44 characterization in L0).

**IN-003 (Major):** Resolved by PM-004/FM-004 corrective action (define HITL verification process).

**IN-004 (Minor):** Add caveat to Vale recommendation: "Before Vale CI integration, audit existing Jerry docs for Jerry-specific patterns that may require custom rule exceptions (e.g., `/skill` syntax, H-rule notation, agent name conventions)."

---

## Convergent Findings

Findings appearing across 3+ strategies indicate genuine defects rather than perspective artifacts:

### CONVERGENT-1: NumPy NEP 44 L0/L2 Inconsistency
Confirmed by: **CC-001** (Constitutional), **DA-001** (Devil's Advocate), **FM-001** (FMEA, RPN 504), **IN-002** (Inversion).

This is the highest-confidence defect in the deliverable. Four independent strategies using different evaluation lenses all surface the same factual inconsistency. The fix is simple and must occur in the next revision.

### CONVERGENT-2: Human HITL Verification Process is Operationally Hollow
Confirmed by: **PM-004** (Pre-Mortem, Critical), **FM-004** (FMEA, RPN 240), **IN-003** (Inversion, Major).

The recommendation with the highest cited stakes (preventing 30% defect rate) lacks a defined process. Three strategies independently identify this as a critical gap. The fix requires adding a process specification, not just a recommendation.

### CONVERGENT-3: Evidence Quality Overstated
Confirmed by: **DA-004** (Devil's Advocate), **FM-002** (FMEA, RPN 294), **LJ Evidence Quality = 0.81** (LLM-as-Judge).

Three strategies independently assess the evidence classification as overstated. The key evidence chain (DORA 2023 via secondary citation, Mintlify vendor-reported, Nielsen Norman 2020 baseline) does not support "~60% direct citation."

---

## Score Challenge

**Self-reported score: 0.90 | Verified score: 0.859 | Delta: -0.041**

The self-reported score is CHALLENGED. The gap is driven by:

1. **Internal Consistency (0.83 vs implied ~0.90):** L0/L2 NumPy NEP 44 inconsistency and OQ-4 structural issue both reduce this dimension below the self-report's implied assumption.

2. **Evidence Quality (0.81 vs implied ~0.90):** Chain citations for DORA, vendor-reported Mintlify data, and 2020 baseline for navigation research collectively reduce this dimension. The "~60% direct" self-classification applies to lower-stakes findings (tool adoption facts) while higher-stakes strategic claims (DORA 25% performance correlation, HITL 60-70% agreement) rest on weaker evidence.

3. **Actionability (0.91, not blocking):** The HITL recommendation operational gap is a meaningful weakness that holds this dimension just below 0.92.

The self-reported confidence of 0.75 was appropriately calibrated to the secondary-research ceiling. The self-reported quality score of 0.90 was not.

---

## Revision Requirements

### P0 — MUST resolve before next iteration passes threshold

1. **[CONVERGENT-1]** Revise L0 finding #1 to accurately distinguish: (a) completed Diataxis restructures: Cloudflare, Canonical, Django; (b) in-progress proposals: NumPy NEP 44; (c) minor adoptions: Gatsby. Remove "have all restructured" framing for projects that have not completed restructuring.

2. **[CONVERGENT-2]** Define the human command-execution verification process for Wave 4a tutorials: reviewer role, step-by-step checklist (at minimum: run each command on a fresh Jerry install, verify expected output, verify file paths exist), and pass/fail acceptance criteria.

3. **[CONVERGENT-3]** Revise evidence classification end note to add qualifier: "Key strategic recommendations (DORA 25% figure, HITL 60-70% agreement, navigation research) rest on chain citations, vendor-reported data, or 2020 baseline. High-confidence direct citations apply primarily to tool adoption facts (Vale adoption list, Docusaurus versioning, WCAG 2.2 publication dates)."

4. **[CC-002]** Update WCAG 3.0 timeline statement to reflect April 2026 status (still in Working Draft).

### P1 — SHOULD resolve; justification required if deferred

5. **[DA-002 / IN-001]** Add "Challenging Evidence" content to L1 Methodology or L0: explicitly document whether evidence was found that challenges Jerry's existing approach. If absent, state this as a finding ("no disconfirming evidence found for Jerry's core creator-critic-revision approach in the 2023-2026 literature reviewed").

6. **[FM-003]** Clarify retroactive Wave 2-4 Google style guide scope: specify whether this means "apply as authoring reference guidance" (no CI enforcement needed) or "enforce via Vale in Wave 5 requiring Wave 2-4 rework." Add a single sentence resolving this scope question.

7. **[PM-002]** Add Vale pre-integration audit step: before Wave 5 CI integration, run Vale on a sample of 5-10 existing Jerry docs to identify false-positive rate on Jerry-specific syntax. Document the planned custom rule exceptions.

8. **[FM-005]** Add risk statement to HEART measurement section: "No OSS baseline exists for HEART docs metrics. The ux-heart-analyst wave should scope baseline establishment as its primary output rather than measurement against existing benchmarks."

9. **[PM-003 / OQ-2]** Address OQ-2 (discovery path) with either a stated safe-bet rationale or a hypothesis. Suggested resolution: "README optimization is valid regardless of discovery path because README is always visible. This does not require OQ-2 resolution."

10. **[FM-007 / OQ-7]** Close OQ-7 with PROJ-040-specific guidance on post-Wave-5 maintenance sustainability. As a solo/small-team framework, this is not a theoretical gap.

### P2 — MAY resolve; acknowledgment sufficient

11. **[DA-003 / IN-004]** Add Vale calibration cost caveat to recommendation rank 2.
12. **[DA-005]** Close OQ-4 by noting it is answered in Section 2.9.
13. **[FM-008 / SD-01]** Add staleness caveat propagation from SD-01 into recommendation rank 4 (cross-linking).
14. **[IN-005]** Add caveat that tutorial/how-to separation attribution is observational (no control group).
15. **[PM-006]** Qualify Diataxis frontmatter tags recommendation: "low-cost future-proofing; current LLM systems have not been confirmed to honor frontmatter for routing."

---

## Execution Statistics

| Metric | Value |
|--------|-------|
| **Total Findings** | 23 |
| **Critical** | 5 (FM-001, FM-002, FM-003, FM-004, FM-005 + PM-004 classified Critical in Pre-Mortem) |
| **Major** | 12 |
| **Minor** | 6 |
| **Convergent Defects** | 3 (confirmed across 3+ strategies) |
| **S-014 Composite** | 0.859 |
| **Verdict** | REVISE |
| **Self-Report Challenged** | Yes (-0.041) |
| **P0 Actions Required** | 4 |
| **P1 Actions** | 6 |
| **P2 Actions** | 5 |
| **Strategies Completed** | 6 of 6 (S-007, S-002, S-014, S-004, S-012, S-013) |
| **Protocol Steps Completed** | All steps for all 6 strategies |

---

*Adversarial Review Iteration 1 — FEAT-040-056*
*Executed: 2026-04-17 by adv-executor*
*Next action: Deliver findings to ps-researcher for targeted revision targeting P0 items first.*
*Estimated score after P0 resolution: 0.90-0.91 (P1 items required to reach 0.92)*
