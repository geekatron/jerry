# Adversarial Review: FEAT-040-056 OSS Documentation Best-Practices Research — Iteration 3

## Execution Context

| Field | Value |
|-------|-------|
| **Feature** | FEAT-040-056 |
| **Strategies Executed** | S-007, S-014, S-002, S-004, S-012, S-013 |
| **Criticality** | C3 |
| **Threshold** | 0.92 |
| **Iteration** | 3 of 7 |
| **Deliverable** | `projects/PROJ-040-documentation/work/EPIC-040-001/research/FEAT-040-056/ps-researcher-output.md` |
| **Executed** | 2026-04-20 |
| **Self-Reported Score** | 0.926 |
| **Verified Score** | 0.918 |
| **Verdict** | REVISE — BELOW C3 THRESHOLD (0.918 < 0.92; gap 0.002; REVISE band 0.85–0.91 does not technically apply — gap-zone between REVISE and PASS) |

**H-16 Note:** S-003 (Steelman) is waivable per the C3 review brief for this iteration (prior iterations applied). Internal steelmanning applied before S-002 Devil's Advocate execution. No H-16 violation generated.

**Iteration 3 Summary:** All P0 items from iter-2 are genuinely resolved — the GitLab L0 restructuring is structurally correct and the DORA inline caveat is substantive. Three P1 items are partially resolved. The gap to 0.92 is 0.002. The deliverable has improved meaningfully from iter-2 (0.906 → 0.918, +0.012). The self-score of 0.926 is slightly optimistic (delta −0.008; self-report over-estimated Methodological Rigor at 0.91→0.91 fine, but over-estimated Completeness at 0.92 and slightly over-estimated Evidence Quality). The single remaining blocker is that the P1 DA-007 scope limitation paragraph lists general search-surface exclusions (non-English, enterprise-internal, academic HCI, etc.) rather than the three specific recommendation-level disconfirmation gaps DA-007 explicitly required. This is a targeted one-paragraph addition that should close in iter-4.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Iter-2 Closure Verification](#iter-2-closure-verification) | Pass/fail for each iter-2 P0 and P1 requirement |
| [Findings Summary](#findings-summary) | All findings by severity for iter-3 |
| [S-007 Constitutional AI Critique](#s-007-constitutional-ai-critique) | Principle-by-principle compliance — iter-2 resolutions verified |
| [S-014 LLM-as-Judge](#s-014-llm-as-judge) | Dimensional scoring with composite (PRIMARY) |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Counter-arguments against iter-3 additions |
| [S-004 Pre-Mortem](#s-004-pre-mortem) | Prospective failure analysis for iter-3 changes |
| [S-012 FMEA](#s-012-fmea) | Failure mode update post-iter-3 corrections |
| [S-013 Inversion](#s-013-inversion) | Assumption stress-tests on iter-3 additions |
| [Score Challenge](#score-challenge) | Verification of self-reported 0.926 vs actual 0.918 |
| [Revision Requirements](#revision-requirements) | Priority-ordered action list for iteration 4 |

---

## Iter-2 Closure Verification

Explicit pass/fail for each iter-2 requirement:

| Item | Priority | Required Action | Iter-3 Status | Evidence |
|------|----------|----------------|---------------|---------|
| CONVERGENT-4 / DA-006 / FM-009: Restructure L0 finding #1 — separate documented adopters from practice-inferred GitLab | P0 | Primary sentence: 4 documented adopters only. GitLab in subordinate sub-bullet visually and semantically separated. Acceptance: L0 cannot be read as listing 5 equivalent production deployments. | **PASS** | L0 finding #1 primary sentence lists "Cloudflare, Canonical/Ubuntu, Django, and Gatsby" only. GitLab in subordinate sub-bullet with italic lead "*Practice-aligned, framework not explicitly adopted:*" and explicit D-05 inference cross-reference. NumPy in separate sub-bullet labeled "Proposal only." Structural subordination is genuine. |
| CONVERGENT-5 / FM-010 / CC-003: Add inline DORA calibration caveat to L0 finding #3 | P0 | Inline text: "...correlates with higher team performance (specific correlation figure not independently verified against primary DORA 2023 report — see Limitations)." Acceptance: L0-only reader can calibrate without navigating to Limitations. | **PASS** | L0 finding #3 now reads: "documentation quality correlates with team performance per DORA reports; specific effect magnitudes are not independently confirmed — see [Limitations](#l1-limitations) L1.1 for chain-citation status on the '25% higher team performance' figure." Inline caveat is present and self-contained. Slight wording divergence from the recommended text is acceptable — substance is equivalent. |
| DA-007: Add scope limitation note to Challenging Evidence listing specific unsearched disconfirmation surfaces | P1 | Three specific recommendation-level gaps: (a) Diataxis tutorial/how-to vs. alternative IA in sub-100-star OSS, (b) Vale false-positive rates for specialized vocabularies, (c) Google style guide compatibility with pre-existing voice systems. | **PARTIAL PASS** | Scope limitation paragraph added (lines 488-497) listing 6 unsearched surfaces: non-English sources, enterprise-internal frameworks, paid doc-as-a-service beyond Mintlify/Fern, academic HCI beyond CHASE 2025, IR/tech-comm academic journals, internal Jerry-project prior artifacts. These are valid search-surface exclusions but are NOT the three recommendation-level disconfirmation gaps DA-007 specifically requested. The paragraph improves methodological honesty for breadth-of-search but does not acknowledge that the three highest-risk recommendations (Diataxis for sub-100-star OSS, Vale false-positives, Google style vs. existing voice) were not specifically targeted for disconfirmation. See finding DA-009. |
| FM-011 / PM-007: Add Recommendation rank 11 (command-manifest.yaml) | P1 | Concrete recommendation with FM-011 rationale and evidence-tier labeling. | **PASS** | Rank 11 added with explicit FM-011 citation, "Synthesis (no OSS project surfaced with a published command-to-docs manifest; framework pattern is inference from OpenAPI analogy)" evidence-tier label, advisory scope designation, and Wave-specific placement (Wave 4a planning / implementation Wave 5 or post-release). |
| Revision Log gap: Add entry documenting GitLab addition | P1 | "GitLab added to L0 finding #1 and Section 2.1 D-05 as practice-aligned adoption..." | **PASS** | Iter-3 Changes table fully documents CONVERGENT-4 resolution including the GitLab subordination fix with D-05 inference cross-reference. Revision Log now accurately reflects all substantive L0 changes. |

**P0 Resolution Rate: 2/2 (100%)**
**P1 Resolution Rate: 2/3 (67%; DA-007 scope limitation is partial)**

---

## Findings Summary

### New Findings (Iter-3 Review)

| ID | Strategy | Severity | Finding | Section |
|----|----------|----------|---------|---------|
| DA-009 | S-002 | Minor | Scope limitation paragraph addresses general search-surface gaps (non-English, enterprise-internal, etc.) rather than the three recommendation-level disconfirmation gaps DA-007 specified; partial resolution of P1 item; keeps Methodological Rigor at 0.91 | L2 Challenging Evidence, scope limitation subsection |
| FM-012 | S-012 | Minor | Finding D-05 in L2 Section 2.1 is labeled "(direct)" while L0 sub-bullet cross-references it as "D-05 inference" — label mismatch creates minor confusion for a reader reconciling L0 classification against L2 body text; L1.4 cross-reference in L0 also doesn't mention GitLab | L2 Section 2.1 D-05 vs. L0 finding #1 sub-bullet |

### Iter-2 P0 Findings — Resolution Status

| Finding | Iter-2 Severity | Iter-3 Status |
|---------|----------------|---------------|
| CONVERGENT-4 / DA-006 / FM-009: GitLab L0 placement | Major (RPN 90) | RESOLVED — genuine structural subordination |
| CONVERGENT-5 / FM-010 / CC-003: DORA asymmetric disclosure | Major (RPN 120) | RESOLVED — inline calibration caveat present |
| FM-011: HITL post-publication advisory only | Major (RPN 196) | SUBSTANTIALLY RESOLVED — rank 11 (command-manifest.yaml) provides concrete mechanism |
| DA-007: Challenging Evidence scope too narrow | Minor | PARTIALLY RESOLVED — see DA-009 |
| DA-008: LLM-as-judge validator source absent | Minor | No change — vendor-advocated qualifier accepted as sufficient |
| IN-006: GitLab retroactive framework attribution | Minor | RESOLVED via L0 restructure |
| IN-007: 40% direct-citation tier masking | Minor | RESOLVED via D-05 subordination and DORA inline caveat |
| DA-003: Vale ongoing calibration cost | Minor (P2) | Unchanged; P2 status maintained |
| PM-007: No tutorial-to-command mapping | Minor | RESOLVED via rank 11 |
| PM-008: Feature-owner self-verification constraint | Minor | Unchanged; systemic constraint |

---

## S-007 Constitutional AI Critique

**Strategy:** S-007 Constitutional AI Critique
**Finding Prefix:** CC

### Iter-2 Finding Resolution

- **CC-003 (Minor — DORA Asymmetric Disclosure):** RESOLVED. L0 finding #3 now carries an inline parenthetical caveat visible to L0-only readers without navigating to Limitations. The disclosure is self-contained: "specific effect magnitudes are not independently confirmed — see [Limitations](#l1-limitations) L1.1 for chain-citation status on the '25% higher team performance' figure."

### Constitutional Compliance Iter-3

No new constitutional violations found in iter-3 additions.

**Verification of iter-3 changes:**
- Rank 11 (command-manifest.yaml): Accurately labeled as "Synthesis (no OSS project surfaced with a published command-to-docs manifest; framework pattern is inference from OpenAPI analogy)." The evidence-tier label is honest and self-aware. No P-001 (Accuracy) violation.
- Scope limitation paragraph: Genuinely documents unsearched surfaces. The paragraph is accurate — it does list real search-surface limitations. The issue (DA-009) is one of completeness (what it doesn't say) rather than accuracy (what it does say). No P-001 violation.
- D-05 "(direct)" label: The direct label refers to directly-observed GitLab folder structure, which is accurate. The inference arises in the attribution step (GitLab's structure → Diataxis alignment). The L0 sub-bullet uses "D-05 inference" informally to mean inference-tier attribution. This is a precision gap, not a deception. Minor P-001 concern.

**Constitutional Compliance Score (iter-3):** 1.00 − 0.01 (D-05 label precision gap, Minor) = **0.99 — PASS**. Constitutional gate cleared.

---

## S-014 LLM-as-Judge

**Strategy:** S-014 LLM-as-Judge
**Finding Prefix:** LJ
**Criticality:** C3 (PRIMARY strategy — required)

### Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.918 |
| **Threshold (H-13)** | 0.92 |
| **Verdict** | REVISE — gap 0.002 |
| **Self-Reported Score** | 0.926 |
| **Score Challenge** | −0.008 (self-report slightly above adversarial; self slightly optimistic on Completeness and Evidence Quality) |
| **Gap to Threshold** | 0.002 |
| **Weakest Dimension** | Evidence Quality (0.89) |
| **Strongest Dimension** | Actionability (0.94) |

### Dimension Scores

| Dimension | Weight | Score | Weighted | vs Iter-2 | Evidence Summary |
|-----------|--------|-------|----------|-----------|-----------------|
| Completeness | 0.20 | 0.92 | 0.184 | +0.02 | Rank 11 closes FM-011 gap; scope limitation closes DA-007 breadth; all 9 research areas intact; DORA primary pagination remains chain-cited ceiling |
| Internal Consistency | 0.20 | 0.92 | 0.184 | 0.00 | GitLab L0 restructure genuinely executed; D-05 labeled "(direct)" in body while L0 calls it "D-05 inference" — residual minor mismatch; L1.4 cross-reference doesn't mention GitLab |
| Methodological Rigor | 0.20 | 0.91 | 0.182 | +0.01 | Scope limitation paragraph adds genuine methodological honesty; but documents search-surface gaps rather than the three recommendation-level disconfirmation gaps DA-007 specified; partial resolution only |
| Evidence Quality | 0.15 | 0.89 | 0.134 | +0.03 | GitLab L0 fix is primary driver (+0.03 improvement); DORA inline caveat adds calibration; D-05 body still "(direct)" is minor residual; HITL vendor-only and DORA primary pagination unchanged; ceiling at ~0.90 |
| Actionability | 0.15 | 0.94 | 0.141 | 0.00 | Rank 11 is a concrete advisory recommendation; HITL process unchanged and production-ready; no regression |
| Traceability | 0.10 | 0.93 | 0.093 | +0.01 | Iter-3 Changes table fully documents P0×2 + P1×3 items; Revision Log complete; minor D-05 label traceability gap |
| **TOTAL** | **1.00** | | **0.918** | **+0.012** | |

**Computation verification:**
```
(0.92 × 0.20) + (0.92 × 0.20) + (0.91 × 0.20) + (0.89 × 0.15) + (0.94 × 0.15) + (0.93 × 0.10)
= 0.184 + 0.184 + 0.182 + 0.134 + 0.141 + 0.093
= 0.918
```

### Detailed Dimension Analysis

#### Completeness (0.92/1.00)

**Iter-3 improvements:**
- Rank 11 (command-manifest.yaml) addresses the FM-011 gap: a concrete mechanism for post-publication tutorial drift detection is now recommended. The recommendation is correctly scoped as advisory with Wave 4a planning / implementation Wave 5 or post-release.
- Scope limitation paragraph in Challenging Evidence converts an implicit limitation to an explicit one, improving epistemic completeness. Six unsearched surfaces are enumerated.
- Iter-3 Changes table completes the Revision Log.

**Remaining ceiling:**
- DORA 2023 primary report pagination unverified — this is a correctly disclosed ceiling rather than a gap.
- CHASE 2025 abstract-only — correctly disclosed.

**Score rationale:** The targeted additions close the gaps that were within scope. Both the FM-011 gap and the Challenging Evidence completeness gap are now addressed. Moving from 0.90 to 0.92 is supported. No unresolved completeness gaps within secondary-research scope.

---

#### Internal Consistency (0.92/1.00)

**Iter-3 improvements:**
- L0 finding #1 restructuring: the four documented adopters appear only in the primary sentence; GitLab is in a clearly sub-bullet tier with explicit inference labeling; NumPy is in its own sub-bullet. This is structurally consistent with L2 Section 2.1's treatment of D-05 as "practice-aligned adoption, not explicit Diataxis adoption."
- Revision Log now records all substantive L0 changes.

**Residual gap — Finding D-05 Label Mismatch (FM-012):**
L2 Section 2.1 line 186 still reads: `**Finding D-05 (direct):**` The L0 sub-bullet in finding #1 cross-references this as "D-05 inference." The self-score table (line 631) claims "L0 finding #1 now consistent with L2 Section 2.1 Finding D-05 inference classification" — but D-05 body is labeled (direct), not (inference). Additionally, the L0 sub-bullet directs readers to "section L1.4 on observational/inference attribution" but L1.4 names only "Cloudflare, Canonical, Django, Gatsby, NumPy proposal" — not GitLab. A reader following the L0 cross-reference to L1.4 will not find GitLab discussed there.

These are Minor residual inconsistencies. They do not threaten the primary structural integrity (GitLab IS correctly subordinated in L0) but they create precision gaps for a careful reader. Holding at 0.92, same as iter-2, because the improvement (GitLab restructure) is offset by the newly surfaced D-05 label mismatch.

---

#### Methodological Rigor (0.91/1.00)

**Iter-3 improvements:**
- Scope limitation paragraph added to Challenging Evidence section. The paragraph explicitly names six types of evidence surfaces that were not searched: non-English communities, enterprise-internal frameworks, paid doc-as-a-service providers beyond Mintlify/Fern, academic HCI literature beyond CHASE 2025, IR/tech-comm academic journals, and internal Jerry-project prior artifacts.
- The concluding sentence — "Readers relying on this research for high-stakes decisions should treat the 'no contradicting evidence surfaced' outcome as bounded by the searched surfaces above, not as a global negative" — is methodologically sound and correct.

**Residual gap (DA-009 — partial DA-007 resolution):**
The iter-2 DA-007 P1 requirement specifically requested that the scope limitation acknowledge three recommendation-level disconfirmation gaps:
1. Diataxis tutorial/how-to separation efficacy vs. alternative IA interventions in sub-100-star OSS projects
2. Vale false-positive rates for specialized technical vocabularies
3. Google style guide compatibility with pre-existing project-specific voice systems

The iter-3 scope limitation paragraph lists general search-surface exclusions (language, institution type, publication format) rather than these three specific "we didn't look for evidence against our highest-stakes recommendations" acknowledgments. This is a different type of scope disclosure: the paragraph explains _where_ the research didn't look, while DA-007 asked it to acknowledge _what questions_ it didn't specifically ask. Both are legitimate methodological disclosures; they are not equivalent.

The practical impact: a reader of the scope limitation paragraph will understand that the research was bounded to Anglophone public OSS literature. They will not learn that Diataxis adoption for tiny-team OSS was never specifically subject to disconfirmation search. The three DA-007 concerns map to the highest-risk structural recommendations for PROJ-040 — where the absence of disconfirmation matters most.

Scoring: Up from 0.90 to 0.91. The search-surface limitation addition is a genuine improvement. Full resolution to 0.92 requires the three recommendation-level acknowledgments.

---

#### Evidence Quality (0.89/1.00)

**Iter-3 improvements:**
- **GitLab L0 restructure (primary fix):** The L0 finding #1 primary sentence now exclusively lists Cloudflare, Canonical, Django, and Gatsby. GitLab appears in a subordinate sub-bullet with the explicit "(Practice-aligned, framework not explicitly adopted)" label. This is a genuine structural fix that addresses CONVERGENT-4/DA-006/FM-009. A reader scanning L0 finding #1 now clearly sees four validated adopters plus two subordinate qualifications (GitLab practice-aligned; NumPy proposal-only). The FM-009 failure mode (parenthetical qualifier stripped in downstream citations) is substantially mitigated by the visual and structural separation.
- **DORA inline caveat:** The calibration information is now visible to L0-only readers.

**Remaining ceiling:**
1. D-05 body text still labeled "(direct)" while L0 calls it "D-05 inference" — minor label precision gap. The evidence-tier ambiguity is real: GitLab's folder structure is directly observed; the Diataxis attribution is inferred. The "(direct)" label in the body refers to the observational fact; the "inference" label in L0 refers to the attribution step. This is accurate but imprecise — the two-step nature (direct observation → inference conclusion) should be explicit in D-05's body label for clarity.
2. DORA 2023 primary pagination unverified (correctly disclosed ceiling).
3. HITL 60-70% figure vendor-only (correctly disclosed, no independent source added).
4. Evidence-tier concentration: 40% direct-citation tier is weighted toward tool-adoption facts (Vale adoption list, Docusaurus versioning, WCAG publication dates) while the highest-stakes strategic claims (Diataxis tutorial/how-to win, HITL defect rate) are synthesis/inference tier. This is accurately disclosed in L1.1 but not surfaced at L0. IN-007 residual.

Score: Up from 0.86 to 0.89. The GitLab L0 fix removes the primary evidence-quality defect identified in iter-2. The ceiling remains at ~0.90 pending primary DORA verification and independent HITL figure validation — both correctly identified as out of scope.

---

#### Actionability (0.94/1.00)

**Iter-3 improvements:**
- Rank 11 (command-manifest.yaml) is concrete and actionable: named artifact (`command-manifest.yaml`), stated purpose (CLI command → documentation location mapping), explicit use case (automated drift detection), Wave-specific placement (advisory in Wave 4a planning; implementation in Wave 5 or post-release), and honest evidence-tier label (Synthesis, inference from OpenAPI analogy).
- The advisory designation is appropriate — this is a forward-looking mechanism rather than a blocking deliverable requirement.

**Score:** Unchanged at 0.94. Rank 11 adds value without displacing any existing actionable content.

---

#### Traceability (0.93/1.00)

**Iter-3 improvements:**
- Iter-3 Changes table in Revision Log: explicitly maps 2 P0 items + 3 P1 items to their iter-2 blocker IDs with iter-3 resolution summaries. This is the most complete revision log the deliverable has had.
- Rank 11 FM-011 citation: directly traceable to the iter-2 S-012 FMEA finding.
- Scope limitation paragraph: traceably linked to DA-007 via the P1 description in the Iter-3 Changes table.

**Residual gap:**
- D-05 label mismatch (body "(direct)" vs. L0 "inference") creates a minor traceability confusion for a reader cross-referencing the two levels. The L0 cross-reference to L1.4 is slightly misleading because L1.4 does not discuss GitLab.

**Score:** Up from 0.92 to 0.93. The Revision Log completeness improvement is the driver.

---

### Verdict Rationale

**Verdict: REVISE**

Composite 0.918 is below the H-13 C3 threshold of 0.92. Gap: 0.002. This is an extremely narrow gap — the deliverable is functionally very close to the threshold. The gap is driven by:

1. **Methodological Rigor at 0.91** (would need 0.92): DA-007 scope limitation is partially resolved. The paragraph added describes search-surface exclusions rather than the three specific recommendation-level disconfirmation gaps requested. This is the single dimension blocking the threshold.
2. **Evidence Quality at 0.89** (would need ~0.90 for threshold improvement, but this dimension has a known ceiling): The GitLab fix substantially improves this dimension; the ceiling is the unresolved DORA primary and HITL independent-validation gaps.

**Path to 0.92:** A single targeted paragraph addition — adding the three recommendation-level disconfirmation gaps (a, b, c from DA-007) to the existing scope limitation subsection — would move Methodological Rigor from 0.91 to 0.92, yielding:
```
Composite with Methodological Rigor at 0.92:
(0.92 × 0.20) + (0.92 × 0.20) + (0.92 × 0.20) + (0.89 × 0.15) + (0.94 × 0.15) + (0.93 × 0.10)
= 0.184 + 0.184 + 0.184 + 0.134 + 0.141 + 0.093
= 0.920
```

0.920 = threshold. Adding the D-05 label clarification (FM-012) would push Internal Consistency marginally above 0.92, yielding composite ~0.921-0.922 — robustly at threshold.

**Trajectory:** 0.859 (iter-1) → 0.906 (iter-2) → 0.918 (iter-3). The deliverable has improved +0.059 from the iter-1 baseline. All critical blockers (iter-1) and all iter-2 P0 items are fully resolved. The remaining gap is a single targeted paragraph addition.

---

## S-002 Devil's Advocate

**Strategy:** S-002 Devil's Advocate
**Finding Prefix:** DA
**H-16:** Internal steelmanning applied (S-003 waivable per brief).

### Steelman Summary

The iter-3 deliverable is the strongest version of this research document. The L0 finding #1 restructuring is a genuine improvement: the four documented adopters are clearly primary, GitLab is clearly secondary, and NumPy is clearly non-production. The document now models how to handle evidence tiers at different levels of presentation — a lesson that generalizes to future Jerry research outputs. The Iter-3 Changes table in the Revision Log is a model of surgical iteration traceability: each change is linked to its blocker ID, priority tier, iter-2 problem statement, and iter-3 resolution. The command-manifest.yaml recommendation (rank 11) is appropriately scoped as advisory, explicitly labeled Synthesis/inference, and provides a concrete engineering hook for future automation. The scope limitation paragraph converts the Challenging Evidence section's implicit limitation to an explicit one — a methodological honesty standard rarely met in industry research.

### Counter-Arguments

#### DA-009 [Minor]: Scope Limitation Paragraph Targets Wrong Surfaces for DA-007 Resolution

**Claim challenged:** Iter-3 Changes table (line 59): "New 'Scope limitation' subsection in Challenging Evidence lists 6 explicitly out-of-scope disconfirmation surfaces... Bounds the 'no contradicting evidence' outcome."

**Counter-argument:** The six surfaces documented (non-English, enterprise-internal, paid doc-as-a-service, academic HCI, IR/tech-comm journals, internal Jerry artifacts) are valid search-surface limitations. However, DA-007's P1 requirement was specifically:

> "The following higher-risk structural recommendations were NOT subject to specific disconfirmation search: (a) Diataxis tutorial/how-to separation efficacy vs. alternative IA interventions in sub-100-star OSS projects; (b) Vale false-positive rates for specialized technical vocabularies; (c) Google style guide compatibility with pre-existing project-specific voice systems."

The iter-3 paragraph answers "what publications didn't we search?" but not "what specific questions didn't we ask?" These are two orthogonal disclosure types. A practitioner acting on L0 recommendations for PROJ-040 would want to know: "Was the evidence specifically tested for the case of a sub-100-star OSS project adopting Diataxis quadrant separation?" The scope limitation paragraph says nothing about this. The three highest-risk structural recommendations for PROJ-040 are not acknowledged as subject to bounded disconfirmation search.

**Evidence:** Iter-2 DA-007 (lines 280-287): "The three highest-risk recommendations for PROJ-040 are: (1) Diataxis quadrant restructure... The disconfirmation search asked 'is Diataxis harmful for small projects?' but did NOT ask 'does Diataxis specifically (vs. any structured IA) produce measurable adoption lift in sub-100-star OSS projects?'"

**Impact:** Minor — the scope limitation paragraph is a genuine improvement; it just doesn't complete the DA-007 resolution. The "no contradicting evidence" outcome is still bounded in a weaker-than-required way for the three highest-stakes recommendations.

**Response required:** Add three bullet points to the scope limitation subsection: "(a) Disconfirmation was not specifically sought for whether Diataxis tutorial/how-to separation (vs. any structured IA intervention) measurably improves adoption in sub-100-star OSS projects — this is a genuine field gap, not a confirmed field absence. (b) Disconfirmation was not specifically sought for Vale false-positive rates in specialized technical vocabularies with non-prose syntax. (c) Disconfirmation was not specifically sought for compatibility of the Google developer documentation style guide with existing project-specific voice systems." This is a five-sentence addition to an existing paragraph.

---

#### FM-012 [Minor]: D-05 Finding Label Mismatch — "(direct)" vs. "inference"

**Claim challenged:** Self-score table (line 631): "L0 finding #1 now consistent with L2 Section 2.1 Finding D-05 inference classification."

**Counter-argument:** L2 Section 2.1 line 186 reads `**Finding D-05 (direct):**`. The L0 sub-bullet in finding #1 says "Classified as D-05 inference, not direct adoption." The self-score assertion that L0 is now consistent with L2 is technically incorrect: L2 still labels D-05 as "(direct)," not "(inference)." The "(direct)" label in the body refers to the directly-observed GitLab folder structure pattern. The "inference" in L0 refers to the attribution step (folder structure → Diataxis alignment). These refer to different aspects of the same finding, but a reader tracing L0's "D-05 inference" back to the L2 body finding "(direct)" will notice the discrepancy.

A secondary cross-reference issue: the L0 sub-bullet directs readers to "L1.4 on observational/inference attribution" but L1.4 (lines 164-166) names "Cloudflare, Canonical, Django, Gatsby, NumPy proposal" without mentioning GitLab. The intended cross-reference target is not fulfilled.

**Corrective action:** (a) Change D-05 body label from "(direct)" to "(direct observation, inference attribution)" or "(practice-aligned inference)." (b) Either add a GitLab sentence to L1.4, or update the L0 cross-reference to point to "Finding D-05 in Section 2.1" rather than "L1.4." Severity: Minor — structural subordination in L0 is correct; this is a label precision issue.

---

### Scoring Impact (S-002)

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Neutral | DA-007 partial resolution adds some completeness; does not fully achieve it |
| Internal Consistency | Minor negative | D-05 label mismatch (FM-012) creates new minor inconsistency |
| Methodological Rigor | Marginal positive | Scope limitation is genuine; does not complete DA-007 requirement |
| Evidence Quality | Neutral | No new evidence quality issues introduced |
| Actionability | Neutral | Rank 11 addition is positive; no new actionability gaps |
| Traceability | Neutral | Minor D-05 cross-reference issue |

---

## S-004 Pre-Mortem

**Strategy:** S-004 Pre-Mortem Analysis
**Finding Prefix:** PM

### Failure Scenario Assessment (Iter-3)

**Prior failure scenario (iter-2):** Tutorial drift due to no command-to-tutorial mapping. Status: **substantially mitigated** by rank 11 (command-manifest.yaml). The research now includes a concrete recommendation for detecting drift. The mitigation is advisory (Wave 4a planning; implementation Wave 5 or post-release), which is appropriate for a research document — it defers implementation to the planning phase rather than attempting to prescribe a full solution.

### Updated Failure Inventory

| ID | Category | Finding | Likelihood | Severity | Resolution Status |
|----|----------|---------|------------|----------|------------------|
| PM-007 | Process | No tutorial-to-command mapping — drift detection mechanism absent | Low | Now Mitigated | Rank 11 provides concrete mechanism; implementation Wave 5 or post-release |
| PM-008 | Process | Feature-owner self-verification for C3+ tutorials; second-reviewer explicitly optional | Medium | Minor | Unchanged — systemic solo-maintainer constraint |
| PM-009 | Research | Scope limitation paragraph added but recommendation-level disconfirmation gaps not disclosed — iter-4 failure mode: practitioner acts on recommendations without knowing that the three highest-risk ones were never subject to targeted disconfirmation search | Medium | Minor (research scope) | DA-009 — targeted fix required |

**P0 (MUST mitigate — iter-4):** None. No new P0 items identified.

**P1 (SHOULD mitigate — iter-4):**

**PM-009 / DA-009:** Add three recommendation-level acknowledgments to the scope limitation subsection. One paragraph addition. This completes the DA-007 P1 requirement from iter-2 and closes the methodological rigor gap preventing the 0.92 threshold.

**P2 (Advisory):**

**PM-008:** Solo-maintainer second-reviewer constraint. Unchanged. No research-level resolution available.

---

## S-012 FMEA

**Strategy:** S-012 FMEA
**Finding Prefix:** FM

### Iter-2 Major Failure Mode Resolution

| ID | Iter-2 RPN | Iter-3 Post-Correction RPN | Verdict |
|----|-----------|--------------------------|---------|
| FM-009 (GitLab L0 qualifier buried) | 90 | ~12 (S=3, O=2, D=2) | RESOLVED — structural subordination eliminates parent failure mode |
| FM-010 (DORA asymmetric disclosure) | 120 | ~12 (S=3, O=2, D=2) | RESOLVED — inline caveat present at L0 |
| FM-011 (HITL post-publication advisory) | 196 | ~48 (S=4, O=4, D=3) | SUBSTANTIALLY RESOLVED — rank 11 provides mechanism; residual RPN reflects deferred implementation |

**Total P0 RPN reduction: 315 → ~72 (77% reduction on P0 items).**

### New Failure Mode (Iter-3)

#### FM-012 [Minor] — D-05 Finding Label Mismatch

| Attribute | Value |
|-----------|-------|
| **Element** | E-01 (L0 finding #1 sub-bullet) vs. E-04 (L2 Section 2.1 Finding D-05) |
| **Failure Mode** | D-05 body labeled "(direct)"; L0 sub-bullet labels it "D-05 inference"; L1.4 cross-reference in L0 does not discuss GitLab |
| **Effect** | Reader tracing L0 → D-05 body finds label mismatch; L0 → L1.4 finds GitLab absent; minor inconsistency undermines the precision of the iter-3 fix |
| **Severity (S)** | 2 (low — structural subordination is correct; label precision only) |
| **Occurrence (O)** | 4 (moderate — careful readers will check cross-references) |
| **Detectability (D)** | 5 (medium — requires cross-referencing two sections) |
| **RPN** | **40** |

**Corrective action:** Update D-05 body label from "(direct)" to "(practice-aligned inference)" or add a clarifying parenthetical: "(direct observation; Diataxis attribution is inference)." Update L0 cross-reference from "L1.4" to "Finding D-05 in Section 2.1" or add a GitLab sentence to L1.4. Estimated post-correction RPN: **8** (S=2, O=2, D=2).

---

### Updated RPN Summary

| Category | Count | Total RPN |
|----------|-------|-----------|
| Iter-1 Critical items (post-correction) | 5 | ~185 (iter-2 measured) |
| Iter-2 P0 Major items (post-iter-3 correction) | 3 | ~72 |
| Iter-2 P1 Minor items (DA-007 partial) | 1 | ~24 (estimated) |
| Iter-3 New Minor items | 1 (FM-012) | ~40 |
| **Total iter-3 RPN** | **10** | **~321** |
| Post-iter-4 correction estimate | 10 | ~260 |

**Note:** Total RPN increased slightly from iter-2's ~591 to ~321 because iter-2's Major P0 items (RPN 90+120+196=406) are substantially resolved, but the residual items and new FM-012 add approximately the above. The net trajectory from iter-1 baseline (1,458) to iter-3 post-correction estimate (~260) is an 82% reduction — matching the iter-2 estimate.

---

## S-013 Inversion

**Strategy:** S-013 Inversion Technique
**Finding Prefix:** IN

### Anti-Goal Re-Examination (Iter-3)

#### Anti-Goal for G-2: "Cite proposals as production deployments"

**Iter-2 status:** RESOLVED (NumPy NEP 44) + PARTIALLY RESOLVED (GitLab retroactive attribution concern).

**Iter-3 check:** The GitLab subordination is genuine. The L0 primary sentence does not list GitLab. A reader extracting the "production Diataxis adopters" list from L0 will correctly identify four: Cloudflare, Canonical, Django, Gatsby. GitLab is visually and textually subordinated. The anti-goal condition is now adequately mitigated.

**Residual:** D-05 body still labeled "(direct)" — this is a different anti-goal (anti-goal for evidence classification, not deployment citation). Minor.

**Status: ADEQUATE — anti-goal condition eliminated at L0 level where it matters most.**

#### Anti-Goal for G-7: "Assume the highest-risk recommendations are adequately tested"

**New for iter-3:** The scope limitation paragraph (iter-3 P1 addition) partially addresses this anti-goal by disclosing what wasn't searched. However, the three highest-risk structural recommendations for PROJ-040 are not named as "not specifically targeted for disconfirmation search." A practitioner who wants to know "did this research specifically look for evidence against the Diataxis-for-tiny-teams recommendation?" cannot find that information in the scope limitation paragraph.

**IN-008 [Minor]:** The "no contradicting evidence" conclusion in Challenging Evidence implicitly applies across all recommendations equally. The scope limitation paragraph limits this conclusion by publication type and language — but not by recommendation scope. A reader of the scope limitation section does not learn that the three highest-risk recommendations (Diataxis adoption lift for sub-100-star OSS, Vale false-positive rates, Google style guide vs. existing voice) were never specifically subject to disconfirmation search. This is equivalent to DA-009 from a different analytical lens.

**Action:** Same as DA-009 — add three recommendation-level bullets to the scope limitation subsection.

---

### Mitigation Plan (Iter-3)

**DA-009 / IN-008 (Minor, P1):** Add three recommendation-level disconfirmation scope acknowledgments to the Challenging Evidence scope limitation subsection. Five-sentence addition to existing paragraph.

**FM-012 (Minor, P1):** Update D-05 body label; update L0 cross-reference. Two-line fix.

---

## Score Challenge

**Self-reported score: 0.926 | Verified score: 0.918 | Delta: −0.008 (self slightly above adversarial)**

| Dimension | Self-Score | Adversarial | Delta | Assessment |
|-----------|-----------|-------------|-------|------------|
| Completeness | 0.92 | 0.92 | 0.00 | Exact match |
| Internal Consistency | 0.94 | 0.92 | +0.02 | Self slightly optimistic; D-05 label mismatch not self-flagged |
| Methodological Rigor | 0.91 | 0.91 | 0.00 | Exact match |
| Evidence Quality | 0.90 | 0.89 | +0.01 | Marginal optimism; D-05 label gap not fully weighted |
| Actionability | 0.96 | 0.94 | +0.02 | Self unchanged from iter-2; adversarial also unchanged |
| Traceability | 0.93 | 0.93 | 0.00 | Exact match |

**Self-calibration assessment:** The iter-2 delta was +0.004 (adversarial marginally above self-report). Iter-3 delta is −0.008 (self-report marginally above adversarial). This is a slight calibration reversal — the self-report is now slightly optimistic rather than slightly conservative. The calibration remains within acceptable bounds. The over-optimism is concentrated in Internal Consistency (which the self-score table explicitly claims D-05 consistency as fully achieved, which it is not) and Actionability (where the self-score inherited the iter-2 level without accounting for the static dimension). The self-score is not challenged as a P-022 concern; it remains well-calibrated for practical purposes. The −0.008 delta is within the ±0.01 calibration tolerance established by the iter-2 calibration history.

---

## Revision Requirements

### P0 — MUST resolve before iter-4 can pass threshold

1. **[DA-009 / IN-008 / PM-009]** Add three recommendation-level disconfirmation scope acknowledgments to the existing scope limitation subsection in Challenging Evidence. Append after the six current bullet points (before the closing sentence):
   - "(a) Disconfirmation was not specifically sought for whether Diataxis tutorial/how-to separation (vs. any other structured IA intervention) measurably improves adoption in sub-100-star OSS projects. This is a genuine field gap — not a confirmed field absence — and the Wave 3-4 Diataxis investment should be understood as evidence-supported but not disconfirmation-tested for the PROJ-040 specific scale."
   - "(b) Disconfirmation was not specifically sought for Vale false-positive rates in technical vocabularies with heavy non-prose syntax (e.g., slash-command syntax, agent-name patterns, H-rule notation). The pre-integration audit (Recommendation rank 2) is the mitigating mechanism."
   - "(c) Disconfirmation was not specifically sought for compatibility of the Google developer documentation style guide with pre-existing project-specific voice systems (see DA-003, IN-004). Jerry's saucer-boy-framework-voice system is an example of project-specific voice that may conflict with Google style guide defaults."

   Acceptance criteria: The scope limitation subsection explicitly acknowledges what specific disconfirmation was NOT conducted for the three highest-risk structural recommendations. This moves Methodological Rigor from 0.91 to 0.92, yielding estimated composite 0.920+.

### P1 — SHOULD resolve in iter-4; justification required if deferred

2. **[FM-012]** Update D-05 body label from "(direct)" to "(practice-aligned inference)" OR add parenthetical "(direct observation; Diataxis alignment is inferred, not documented)" to the existing D-05 body text. Additionally, update the L0 sub-bullet cross-reference from "L1.4 on observational/inference attribution" to "Finding D-05 in [Section 2.1](#21-diataxis-in-production)" — since L1.4 does not discuss GitLab. Acceptance criteria: A reader tracing L0 cross-references finds consistent labels at the target sections.

### P2 — MAY resolve; acknowledgment sufficient

3. **[DA-003 inherited]** Vale ongoing calibration cost (maintenance cost beyond pre-integration audit) still not addressed. No change from iter-2. Remains P2.
4. **[PM-008 inherited]** Solo-maintainer second-reviewer constraint. No research-level resolution available. Remains P2.

---

## Path to 0.92

Single P0 item resolution (DA-009 three-bullet addition) yields:

```
Completeness:          0.92 × 0.20 = 0.184  (unchanged)
Internal Consistency:  0.92 × 0.20 = 0.184  (unchanged)
Methodological Rigor:  0.92 × 0.20 = 0.184  (P0 DA-009 resolution)
Evidence Quality:      0.89 × 0.15 = 0.134  (unchanged)
Actionability:         0.94 × 0.15 = 0.141  (unchanged)
Traceability:          0.93 × 0.10 = 0.093  (unchanged)
TOTAL:                              = 0.920
```

P0 alone crosses the threshold at exactly 0.920.

P0 + P1 item 2 (FM-012 D-05 label fix) yields Internal Consistency up to ~0.93:

```
Methodological Rigor:  0.92 × 0.20 = 0.184
Internal Consistency:  0.93 × 0.20 = 0.186
TOTAL (all others unchanged): ~0.922
```

**Recommendation for orchestrator:** Dispatch iter-4 with P0 item 1 (DA-009 three-bullet addition, ~five sentences) as the sole required change. P1 item 2 (FM-012 D-05 label clarification) is a two-line fix that should be co-executed. Combined, these yield estimated iter-4 composite 0.921-0.922 — robustly at threshold.

---

## Execution Statistics

| Metric | Value |
|--------|-------|
| **Total Findings (iter-3)** | 2 new (DA-009, FM-012) + 2 inherited partial (DA-007, D-05 label) |
| **Critical** | 0 |
| **Major** | 0 |
| **Minor** | 2 new (DA-009, FM-012) |
| **Convergent Defects** | 1 new (DA-009 + IN-008 confirm same gap from two strategies) |
| **Iter-2 P0 Items Resolved** | 2 of 2 (100%) |
| **Iter-2 P1 Items Resolved** | 2 of 3 (67%; DA-007 partial) |
| **Iter-2 P2 Items** | Unchanged (DA-003, PM-008) |
| **S-014 Composite** | 0.918 |
| **Verdict** | REVISE — gap 0.002 |
| **Self-Report Challenged** | No (delta −0.008; within calibration tolerance) |
| **P0 Actions Required (iter-4)** | 1 (DA-009 three-bullet paragraph addition, ~five sentences) |
| **P1 Actions** | 1 (FM-012 D-05 label + cross-reference fix, two lines) |
| **P2 Actions** | 2 (inherited, no new P2) |
| **Strategies Completed** | 6 of 6 (S-007, S-014, S-002, S-004, S-012, S-013) |
| **Protocol Steps Completed** | All steps for all 6 strategies |
| **Estimated Score After P0** | 0.920–0.922 (crosses 0.92 threshold) |
| **RPN Reduction from Iter-1 Baseline** | ~(1,458 − 321) / 1,458 = 78% reduction; post-iter-4 estimated ~82% |
| **Trajectory** | 0.859 → 0.906 → 0.918 (+0.059 total; +0.012 this iteration) |
| **XP-07 Handoff Status** | BLOCKED — iter-4 required before Phase 2 remediation planning |

---

*Adversarial Review Iteration 3 — FEAT-040-056*
*Executed: 2026-04-20 by adv-executor*
*Prior review: `orchestration/reviews/FEAT-040-056-adv-review-iter-2.md` (score 0.906)*
*Next action: Dispatch to ps-researcher for iter-4. Single P0 item (DA-009 three-bullet addition to Challenging Evidence scope limitation subsection). P1 item FM-012 (D-05 label + cross-reference fix) strongly recommended co-execution. Estimated iter-4 composite: 0.921–0.922. XP-07 research handoff to Phase 2 remediation planning remains BLOCKED pending PASS verdict.*
