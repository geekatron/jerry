# Strategy Execution Report: C4 Full Tournament — Industry Survey (Iteration 3)

## Execution Context

- **Strategy:** C4 Tournament (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014)
- **Templates:** `.context/templates/adversarial/s-00{1,2,3,4,7,10,11,12,13,14}.md`
- **Deliverable:** `projects/PROJ-014-negative-prompting-research/research/industry-survey.md`
- **Executed:** 2026-02-27T00:00:00Z
- **Iteration:** 3 of N (prior scores: Iter 1 = 0.770, Iter 2 = 0.907)
- **H-16 Compliance:** S-003 (Steelman) executed before all critique strategies
- **Leniency Bias Counteraction:** Active — scoring absolute quality, not improvement trajectory

---

## Part I: Strategy Executions (S-001 through S-013)

---

### S-003: Steelman Technique

**H-16 Compliance:** S-003 executes first per mandatory ordering.

**Step 1: Deep Understanding**

The deliverable is a 31-source industry and practitioner survey on negative prompting in LLMs. Core thesis: negative instructions in LLMs are less effective than positive framing for behavioral control, due to multiple failure mechanisms, though they retain legitimate roles in safety boundaries and programmatic enforcement. The document is organized in three tiers (L0 executive summary, L1 source catalog, L2 detailed analysis) with cross-references and methodology sections.

**Step 2: Identify Presentation Weaknesses**

The survey is substantially mature. After two revision cycles, the document has:
- Well-defined evidence tier definitions with 5 sub-categories and epistemic weighting
- Consistent analyst-inference labels on Theme 6 patterns
- Corrected source count (31 core + 1 adjacent)
- U-shaped recovery caveats in both relevant locations
- Corrected PromptHub/Bsharat et al. attribution

**Step 3: Steelman Assessment**

| Weakness | Type | Magnitude |
|----------|------|-----------|
| Source Types table notes 0 conference talks as a factual gap observation | Structural | Minor |
| Cross-vendor synthesis table lacks "Evidence Tier" column for readers comparing vendor strength | Structural | Minor |
| Theme 5 Mechanism 5 (Context Compaction) could cite Source 32's specific GitHub issue numbers more prominently | Evidence | Minor |
| Sub-tier note in Evidence Tier Distribution references sub-categories by letter but the full (a)-(e) vocabulary only defined in Tier Definitions table | Structural | Minor |

**Step 4: Best Case Scenario**

The document is most compelling as a comprehensive landscape survey that honestly acknowledges its own evidentiary limitations. Its self-referential honesty (acknowledging what is vendor recommendation vs. practitioner anecdote vs. empirical evidence) is a genuine strength that distinguishes it from credulous survey aggregations. Under ideal conditions, this survey serves as a definitive Phase 1 artifact on which Phase 2 (academic survey) and Phase 3 (synthesis) build.

**Step 5: Improvement Findings**

| ID | Improvement | Severity | Dimension |
|----|-------------|----------|-----------|
| SM-001-iter3 | Cross-vendor synthesis table could include evidence tier column to help readers evaluate vendor claim weight | Minor | Evidence Quality |
| SM-002-iter3 | Theme 5 Mechanism 5 would benefit from explicit GitHub issue numbers in body text (currently only in Source Table row 32) | Minor | Traceability |
| SM-003-iter3 | Sub-tier distribution note uses letter references that require readers to scroll to Tier Definitions; inline letter definitions would improve readability | Minor | Completeness |

**Steelman Assessment:** Document is already in strong condition after two revision cycles. Remaining weaknesses are presentational and minor. The core analytical and evidentiary framework is sound. Ready for adversarial critique.

---

### S-007: Constitutional AI Critique

**Applicable Principles for Document Deliverable:**
- H-23: Navigation table required for documents over 30 lines (HARD)
- H-24: Navigation table anchor links required (HARD)
- P-001: Truth/Accuracy — no misrepresentation
- P-004: Evidence-based claims
- P-011: Evidence citations required for factual assertions
- H-15: Self-review before presenting

**Step 3: Principle-by-Principle Evaluation**

| ID | Principle | Tier | Result | Evidence |
|----|-----------|------|--------|---------|
| CC-001-iter3 | H-23: Navigation table | HARD | COMPLIANT | Document Sections table present with 5 sections |
| CC-002-iter3 | H-24: Anchor links | HARD | COMPLIANT | All navigation entries use anchor links |
| CC-003-iter3 | P-001: Truth/Accuracy | MEDIUM | COMPLIANT | Evidence tiers accurately labeled; claims qualified |
| CC-004-iter3 | P-004: Provenance | MEDIUM | COMPLIANT | All claims attributed to specific sources with IDs |
| CC-005-iter3 | P-011: Evidence citations | MEDIUM | COMPLIANT | Source references throughout; limitations noted per source |

**Assessment:** No constitutional violations found. All HARD rules satisfied. All MEDIUM principles met.

**Constitutional Compliance Score:** 1.00 - 0 = 1.00 → **PASS**

---

### S-002: Devil's Advocate

**H-16 Compliance:** S-003 executed prior. Proceeding.

**Step 1: Role Assumption**

Deliverable: Industry survey on negative prompting. Criticality: C4. H-16 confirmed. Adopting adversarial stance: finding the strongest reasons the deliverable's claims are wrong, incomplete, or analytically flawed.

**Step 2: Challenge Assumptions**

| Assumption | Challenge |
|------------|-----------|
| 31 sources constitute a representative sample | 31 sources from a 2-day search may systematically over-represent SEO-optimized blog posts and under-represent grey literature, internal practitioner documentation, and non-English sources |
| Vendor recommendations reflect cross-model findings | Each vendor's guidance reflects their own model; Anthropic's recommendation against negatives may not apply to OpenAI models and vice versa |
| Evidence tier classification is objective | The tier system involves editorial judgment; the boundary between "empirical" and "practitioner anecdote" has edge cases |
| The "positive framing is better" conclusion is generalizable | All cited quantitative evidence involves single models at specific capability levels; the trend lines from Sources 4/5 (OpenAI) suggest this may be improving |

**Step 3: Counter-Arguments**

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter3 | Recency confound: the survey's most actionable finding (newer models follow negatives more literally) undermines its own primary recommendation | Major | Sources 4, 5 document that GPT-4.1/GPT-5 follow negative instructions "more closely and more literally." This directly conflicts with the L0 headline finding that negatives fail. The survey notes this pattern (Theme 6, Pattern 4) but does not elevate it to L0 prominence, leaving L0 with a message that may be obsolete for current-generation models | Completeness |
| DA-002-iter3 | The 31-source count claims representativeness but is methodologically undefined — no stopping criterion, coverage threshold, or saturation measure is stated | Major | Methodology section states "40 search queries were executed... Of the results returned, 31 unique sources met the selection criteria." The count (31) appears to be the output of a convenience search, not a systematic sample with defined saturation criteria. No justification for why 31 sources constitutes an adequate sample | Methodological Rigor |
| DA-003-iter3 | Vendor recommendations presented as convergent evidence but may represent collective groupthink on a self-serving hypothesis | Minor | Four vendors all recommend positive framing. But these vendors share researchers, practitioners, and publication venues. The cross-vendor "convergence" may reflect shared industry norms rather than independent empirical validation. If one influential publication shaped the norm (e.g., early Anthropic guidance), the apparent multi-vendor agreement is not independent evidence | Evidence Quality |
| DA-004-iter3 | The survey's own data contradicts its conclusion for narrow use cases — but this nuance is buried | Minor | Source 5 (GPT-5) provides clear evidence that specific negative instructions WORK: "Do NOT guess or make up an answer" is explicitly endorsed. Source 19 (Palantir) uses negatives as standard tools. Source 21 (DSPy) shows 164% improvement via programmatic negatives. The survey documents these but the L0 headline finding still leads with the negative-framing-fails narrative | Internal Consistency |

**Step 4: Response Requirements**

| Priority | Finding | Required Response |
|----------|---------|-------------------|
| P1 | DA-001-iter3 | L0 should surface the model-generation caveat prominently — either as a standalone bullet or as a qualifier on the primary recommendation. Acceptance criteria: L0 explicitly addresses that newer model generation compliance behavior may differ from the survey's primary finding |
| P1 | DA-002-iter3 | Methodology should state a saturation criterion or acknowledge the absence of one. Acceptance criteria: explicit statement that 31 sources represents the output of the defined search strategy, not a saturation-guaranteed sample |
| P2 | DA-003-iter3 | Acknowledge potential for vendor groupthink in evidence assessment. Acceptance criteria: note added to cross-vendor synthesis acknowledging shared publishing ecosystem |
| P2 | DA-004-iter3 | L0 framing could be more balanced. Acceptance criteria: acknowledgment or minor reframing of primary finding |

---

### S-004: Pre-Mortem Analysis

**H-16 Compliance:** S-003 executed prior. Proceeding.

**Step 1: Set the Stage**

Failure scenario: "It is August 2026. The Phase 1 industry survey has been cited in the Phase 3 synthesis and final deliverable. A peer reviewer demonstrates that 3 of the survey's 7 quantitative claims cannot be traced to their stated sources, and that the primary conclusion ('positive framing is better') was based on 2023 model data that no longer applies to GPT-5 and Claude 4. The survey is retracted from the synthesis."

**Step 2: Declare Failure**

Temporal frame established: Looking back from August 2026 at a survey that failed in production.

**Step 3: Generate Failure Causes**

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-iter3 | Model generation confound: primary finding is based on sources from 2023-2025; by mid-2026, GPT-5/Claude 5/Gemini 4 behavior has evolved and the survey's recommendations may no longer apply | Assumption | Medium | Major | P1 | Evidence Quality |
| PM-002-iter3 | Source URL decay: 31 web sources with links but no access dates or archived copies; URLs may be dead in 6 months | Technical | High | Major | P1 | Traceability |
| PM-003-iter3 | 55%/66.7% figures are from Bsharat et al. (2023, GPT-4) — the most-cited quantitative findings in the survey — but these are for an outdated model and may not hold for current models | Assumption | Medium | Major | P1 | Evidence Quality |
| PM-004-iter3 | Single-researcher bias: all 40 queries were executed by one agent in one session; saturation effects and query framing bias may have systematically excluded contrary evidence | Process | Medium | Major | P1 | Methodological Rigor |
| PM-005-iter3 | Instruction decay figures (95% → 20-60%) are the most action-guiding specific statistics in the survey but have no disclosed methodology and may be entirely anecdotal | Assumption | Medium | Minor | P2 | Evidence Quality |
| PM-006-iter3 | The survey includes DreamHost (Source 12) as "Empirical Evidence" despite disclosing no methodology; this categorization elevates its credibility beyond what the evidence supports | Process | Low | Minor | P2 | Methodological Rigor |

**Step 4: Prioritize**

P1 findings: PM-001 through PM-004 (Major severity, Medium-High likelihood)
P2 findings: PM-005, PM-006 (Minor severity)

**Step 5: Mitigations**

| ID | Mitigation |
|----|-----------|
| PM-001-iter3 | Already partially addressed: model-generation confound section exists in Cross-References. Acceptance: adequate. |
| PM-002-iter3 | URLs present but no access dates documented. The Methodology section could note "All sources accessed 2026-02-27" as a standard archival reference. This is a gap. |
| PM-003-iter3 | Bsharat et al. limitation already noted per-source (Source 13) and in Theme 2 analysis. Acceptance: adequate. |
| PM-004-iter3 | Methodology section does not acknowledge single-researcher limitation or potential query framing bias. This is an unaddressed gap for a survey claiming to represent an industry landscape. |

---

### S-012: FMEA

**Step 1: Decompose**

| Element | ID |
|---------|-----|
| L0 Executive Summary (5 bullets + 2 sub-sections) | E1 |
| L1 Source Catalog (tier defs + source table + adjacent + tier distribution) | E2 |
| L2 Detailed Analysis (6 themes) | E3 |
| Cross-References section | E4 |
| Methodology section | E5 |

**Step 2-3: Failure Modes and RPN**

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Dimension |
|----|---------|-------------|---|---|---|-----|----------|-----------|
| FM-001-iter3 | E1 (L0) | Model-gen caveat present in Cross-References but not in L0 executive bullet where the primary recommendation lives | 6 | 4 | 6 | 144 | Major | Completeness |
| FM-002-iter3 | E5 (Methodology) | No URL access dates documented for 31 sources; links may be dead in 6-12 months | 7 | 8 | 3 | 168 | Major | Traceability |
| FM-003-iter3 | E5 (Methodology) | No saturation criterion stated for source count; "31 sources" lacks justification for why this number is sufficient | 5 | 6 | 5 | 150 | Major | Methodological Rigor |
| FM-004-iter3 | E5 (Methodology) | Single-researcher/single-session limitation not disclosed | 5 | 7 | 6 | 210 | Critical | Methodological Rigor |
| FM-005-iter3 | E2 (L1 Source Table) | Source 32 listed as single entry (multiple GitHub issues); Issues #5055, #6120, #15443, #18660 cited in body but URL links to only #5055 | 3 | 5 | 4 | 60 | Minor | Traceability |
| FM-006-iter3 | E3 (L2 Theme 6) | Patterns 4-5 lack analyst-inference labels — yet these patterns involve editorial synthesis (e.g., "model-generation shift" as a pattern is not labeled as analyst inference despite being synthesized from Sources 4, 5) | 4 | 5 | 5 | 100 | Major | Internal Consistency |
| FM-007-iter3 | E3 (L2 Theme 2) | 55%/66.7% figures from Bsharat et al. cited as "strongest quantitative claim" but their 2023-era GPT-4 basis limits current applicability; could be more prominently flagged in evidence assessment | 4 | 3 | 6 | 72 | Minor | Evidence Quality |

**Step 4: Prioritize**

Critical: FM-004-iter3 (RPN=210): Single-researcher limitation not disclosed
Major: FM-002-iter3 (168), FM-003-iter3 (150), FM-001-iter3 (144), FM-006-iter3 (100)
Minor: FM-007-iter3 (72), FM-005-iter3 (60)

---

### S-013: Inversion

**Step 1: Goals**

1. Provide decision-grade Phase 1 landscape intelligence on negative prompting in LLMs
2. Accurately represent the evidence landscape including its limitations
3. Enable Phase 2 (academic survey) and Phase 3 (synthesis) to build on reliable foundations
4. Achieve >= 0.95 quality gate for C4 tournament

**Step 2: Anti-Goals (Inversion)**

To guarantee this survey FAILS its purpose:
- Present vendor recommendations as empirical evidence (already avoided — tier system prevents this)
- Omit uncertainty qualifications (already avoided — extensive per-source caveats)
- Omit major limitation categories (RISK: single-researcher limitation not disclosed — this is a live anti-goal condition)
- Allow key quantitative figures to be mis-cited (already avoided — Bsharat et al. attribution corrected)
- Present outdated evidence as current (RISK: model-generation confound acknowledged in Cross-References but not in L0 primary finding)

**Step 3: Assumption Map**

| # | Assumption | Type | Confidence | Validation |
|---|-----------|------|------------|-----------|
| A1 | 40 search queries provide adequate coverage of the topic landscape | Process | Medium | Unvalidated — no saturation criterion |
| A2 | English-language sources adequately represent the global practitioner consensus | External | Low | Not addressed in methodology |
| A3 | Blog/article publication format captures representative practitioner views | External | Medium | Partially addressed (SEO-optimized sources noted implicitly) |
| A4 | URL links will remain accessible for readers of the downstream synthesis | Technical | Low | Not addressed — no archived copies or access dates |
| A5 | Evidence tier classification is stable and unambiguous | Process | High | Well-defined with examples |
| A6 | Source publication dates reflect the currency of the findings | Temporal | Medium | Addressed in model-gen confound section |

**Step 4: Stress-Test**

| ID | Assumption | Inversion | Severity | Dimension |
|----|-----------|-----------|----------|-----------|
| IN-001-iter3 | A1: 40 queries provide adequate coverage | Adversarial queries targeting "negative prompting works well" or non-English content would return systematically different sources, potentially inverting the consensus | Major | Methodological Rigor |
| IN-002-iter3 | A2: English-language sources adequate | Non-English LLM research communities (Chinese, Japanese, European) may have different empirical findings; the survey is silently English-centric | Minor | Completeness |
| IN-003-iter3 | A4: URLs remain accessible | 31 URLs with no access dates or archived copies; typical blog URL decay rate is 20-30% over 2 years | Major | Traceability |
| IN-004-iter3 | A6: Publication dates reflect finding currency | Sources 9 (2024), 13 (2024), 18 (2023) may be superseded by current model behavior documented in Sources 4, 5 (2025) | Minor | Evidence Quality |

---

### S-011: Chain-of-Verification

**Step 1: Extract Claims**

| ID | Claim | Type | Source |
|----|-------|------|--------|
| CL-001 | "31 core sources cataloged (1 adjacent source documented separately)" | Quoted value | Document header |
| CL-002 | "Empirical evidence constitutes 23% (7 of 31 core sources)" | Quoted value | L0 Evidence Landscape |
| CL-003 | "Vendor Recommendation: 29%" | Quoted value | Evidence Tier Distribution table |
| CL-004 | "Practitioner Anecdote: 48%" | Quoted value | Evidence Tier Distribution table |
| CL-005 | Vendor Recommendation sources listed as: "1, 3, 4, 5, 6, 7, 15, 19, 27" | Rule citation | Evidence Tier Distribution table |
| CL-006 | Empirical Evidence sources listed as: "14, 20, 21, 18, 12, 13, 30" | Rule citation | Evidence Tier Distribution table |
| CL-007 | Practitioner Anecdote sources listed as: "2, 8, 9, 10, 11, 16, 17, 22, 23, 24, 25, 28, 29, 31, 32" | Rule citation | Evidence Tier Distribution table |
| CL-008 | "Total core sources: 31 (excluding Source 26)" | Quoted value | Source Types table |
| CL-009 | Source Types: "Vendor documentation 8, Blog post/article 17, Framework documentation 3, Community discussion/forum 2, Community guide 1" | Quoted value | Source Types table |
| CL-010 | Source 13 "reports Bsharat et al. (2023) academic study showing 55% improvement and 66.7% correctness increase" | Behavioral claim | Source 13 row + L0 |

**Step 3: Independent Verification**

CL-001: Count unique sources in source table rows 1-32 excluding row 26. Rows present: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,27,28,29,30,31,32 = 31 sources. Adjacent: row 26. VERIFIED.

CL-002: 7 of 31 = 22.58% ≈ 23%. Check: 7/31 = 0.2258. VERIFIED (rounded correctly).

CL-003: 9 of 31 = 29.03% ≈ 29%. Check: 9/31 = 0.2903. VERIFIED.

CL-004: 15 of 31 = 48.39% ≈ 48%. Check: 15/31 = 0.4839. VERIFIED.

CL-005: Vendor Recommendation sources: Sources 1, 3, 4, 5, 6, 7, 15, 19, 27.
- Source 1 (Anthropic): Vendor Recommendation ✓
- Source 3 (OpenAI): Vendor Recommendation ✓
- Source 4 (OpenAI GPT-4.1): Vendor Recommendation ✓
- Source 5 (OpenAI GPT-5): Vendor Recommendation ✓
- Source 6 (Google Gemini): Vendor Recommendation ✓
- Source 7 (Google Gemini 3): Vendor Recommendation ✓
- Source 15 (Anthropic Engineering): Vendor Recommendation ✓
- Source 19 (Palantir): Vendor Recommendation ✓
- Source 27 (NVIDIA NeMo): Vendor Recommendation ✓
Count: 9. VERIFIED.

CL-006: Empirical Evidence sources: 14, 20, 21, 18, 12, 13, 30.
- Source 14 (MLOps Community): Empirical Evidence ✓
- Source 20 (QED42): Empirical Evidence ✓
- Source 21 (DSPy): Empirical Evidence ✓
- Source 18 (Inverse Scaling Prize): Empirical Evidence (Competition) ✓
- Source 12 (DreamHost): Empirical Evidence (Practitioner) ✓
- Source 13 (PromptHub): Empirical Evidence (Cited) ✓
- Source 30 (Big Data Guy): Empirical Evidence (Sentiment) ✓
Count: 7. VERIFIED.

CL-007: Practitioner Anecdote count: Listed as 15 sources. Count sources: 2,8,9,10,11,16,17,22,23,24,25,28,29,31,32 = 15. VERIFIED.

CL-008: Total core = 9+7+15 = 31. VERIFIED.

CL-009: Source types — verify counts by scanning source table:
- Vendor documentation: Sources 1(vendor doc), 3(vendor doc), 4(vendor doc), 5(vendor doc), 6(vendor doc), 7(vendor doc), 15(vendor doc), 19(vendor doc) = 8. Source 27 is "Framework documentation" not "Vendor documentation." 8 vendor docs VERIFIED.
- Blog post/article: Sources 2,8,9,10,11,12,13,14,16,17,22,23,24,25,28,29,30 = 17. VERIFIED.
- Framework documentation: Sources 21(DSPy), 27(NeMo), 31(Nir Diamant notebook) = 3. VERIFIED.
- Community discussion/forum: Sources 18(LessWrong), 32(GitHub) = 2. VERIFIED.
- Community guide: Source 2 is listed as "Community guide" but also counted in Blog post/article. DISCREPANCY DETECTED.

**Discrepancy on CL-009:** Source 2 (DAIR-AI / PromptingGuide.ai) is listed in the Source Table as "Type: Community guide" but the Source Types table shows "Community guide: 1" AND "Blog post / article: 17." Counting sources by type from the Source Table: if Source 2 is Community guide, then blog posts should be 16 (sources 8,9,10,11,12,13,14,16,17,22,23,24,25,28,29,30 = 16 sources). But the table claims 17 blog posts AND 1 community guide = 18 non-vendor-doc non-framework non-forum sources. With 8 vendor docs + 3 framework docs + 2 forum = 13, remaining = 31-13 = 18. 17+1=18. So the math works IF Source 2 is counted as Community Guide (1) and the 17 blog posts exclude Source 2. Let me recount blogs excluding Source 2: 8,9,10,11,12,13,14,16,17,22,23,24,25,28,29,30 = 16 — only 16, not 17.

The count of 17 blog posts appears to include Source 2. But Source 2 is also claimed as a "Community guide." This is a MINOR DISCREPANCY — either Source 2 is a Community guide (count = 17 blogs + 1 community guide) OR it's a blog (count = 17 blogs, 0 community guides) but the table says BOTH 17 blogs AND 1 community guide.

**Step 4: Consistency Check**

| ID | Claim | Result | Severity |
|----|-------|--------|----------|
| CV-001-iter3 | Source Types: 17 blog posts AND 1 community guide | MINOR DISCREPANCY: If Source 2 is Community guide, blog posts should be 16, not 17 | Minor |
| CV-002-iter3 | All percentage calculations | VERIFIED | N/A |
| CV-003-iter3 | Source tier classifications | VERIFIED | N/A |
| CV-004-iter3 | Source count 31 core + 1 adjacent | VERIFIED | N/A |

**Chain-of-Verification Summary:** 9 of 10 claims VERIFIED. 1 minor discrepancy (CV-001-iter3: Source 2 type classification creates an overcounting issue in the Source Types table — community guide + blog post counts sum to 18 when only 17 non-framework, non-vendor, non-forum sources exist after accounting for Source 2 as community guide).

---

### S-001: Red Team Analysis

**H-16 Compliance:** S-003 executed prior. Proceeding.

**Step 1: Define Threat Actor**

Profile: "A motivated academic reviewer conducting a literature-based peer review of PROJ-014 in September 2026. Goal: demonstrate that the survey's primary findings are methodologically unsound or temporally obsolete. Capability: ability to cross-reference claims against primary sources, re-run the search strategy, and compare against post-2026 model documentation. Motivation: establishing that the survey over-claims consensus based on a convenience sample."

**Step 2: Enumerate Attack Vectors**

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-001-iter3 | Convenience sample attack: 40 queries executed by one researcher; no saturation criterion; reviewer conducts alternative search and finds 15 sources not in the catalog with contrary findings | Ambiguity | Medium | Major | P1 | Missing | Methodological Rigor |
| RT-002-iter3 | Temporal obsolescence: GPT-5/Claude 4 guidance (Sources 4, 5) documents improved negative instruction compliance; reviewer argues survey's L0 headline ("negatives fail") is already superseded by the survey's own newer sources | Ambiguity | High | Major | P1 | Partial (model-gen caveat in Cross-References) | Completeness |
| RT-003-iter3 | Source type overcounting (CV-001-iter3): Source 2 counted in both "Blog post/article" (17) and "Community guide" (1), summing to 18 when only 17 such sources exist — reviewer finds this arithmetic inconsistency and questions overall table accuracy | Boundary | Low | Minor | P2 | Missing | Traceability |
| RT-004-iter3 | Single-researcher limitation not disclosed: reviewer asks "what would a second researcher with different query terms find?" and the answer is not addressed in the methodology | Ambiguity | Medium | Major | P1 | Missing | Methodological Rigor |
| RT-005-iter3 | Degradation path: the survey makes strong claims about URL sources (31 links) with no access dates; reviewer attempts to access 5 links in August 2026 and finds 2 are dead | Degradation | High | Minor | P2 | Missing | Traceability |

**Step 3: Defense Gap Assessment**

- RT-001: Missing defense. Methodology states 40 queries but gives no saturation criterion or acknowledgment of single-researcher limitation.
- RT-002: Partial defense. Model-generation confound section exists in Cross-References but is not reflected in L0 executive bullet.
- RT-003: Missing defense. Minor arithmetic issue in Source Types table.
- RT-004: Missing defense. Methodology section does not acknowledge single-researcher or single-session limitations.
- RT-005: Missing defense. No URL access dates, no archived versions noted.

**Step 4: Countermeasures**

| ID | Countermeasure |
|----|---------------|
| RT-001/RT-004 | Add explicit methodology limitation: "This survey was conducted by a single researcher in a single session. A different researcher with alternative query terms may surface different sources. No saturation criterion was applied." |
| RT-002 | Add model-generation caveat sentence to L0 primary recommendation bullet |
| RT-003 | Correct Source Types table: either reclassify Source 2 as blog post (making community guide count = 0) or keep Source 2 as community guide and correct blog count to 16 |
| RT-005 | Note URL access date in Methodology: "All URLs accessed 2026-02-27." |

---

### S-010: Self-Refine

**Step 1: Objectivity Check**

This is the third adversarial iteration. Medium attachment to process. Proceeding with leniency-bias counteraction active.

**Step 2: Systematic Self-Critique**

Reviewing the document against each dimension:

**Completeness (0.20):** L0 contains 5 comprehensive bullets, Evidence Landscape Assessment, and Gaps section. L1 contains full source catalog with tier definitions (now expanded to 5 sub-categories), adjacent sources, tier distribution, and source types. L2 contains 6 themes with cross-cutting synthesis. All major sections present. Key remaining gap: L0 does not include the model-generation caveat in the primary recommendation bullet (the caveat lives in Cross-References). This is a moderate completeness issue for L0 readers who may not read the full document.

**Internal Consistency (0.20):** Source Types table has a minor overcounting issue (Source 2). Evidence tier percentages are internally consistent and verified. All theme 6 patterns 1-3 are labeled as analyst inference. Patterns 4-5 are not labeled as analyst inference — yet "Model-Specific Compliance Evolution" (Pattern 4) is explicitly an editorial synthesis characterizing a trend from Sources 4 and 5, not a term used by those sources.

**Methodological Rigor (0.20):** 40 queries executed, 31 sources selected. Missing: (a) saturation criterion, (b) single-researcher limitation acknowledgment, (c) URL access dates. These are standard survey methodology components.

**Evidence Quality (0.15):** Per-source limitations are well-documented. Analyst-inference labels are applied (Patterns 1-3). The Bsharat et al. attribution is now corrected throughout. Source 30 scope note is clear. Evidence tier sub-categories are well-defined.

**Actionability (0.15):** Gaps section is comprehensive (8 gaps). Cross-references section provides revision triggers. The survey is primarily informational and does not claim to be prescriptive, so actionability expectations are appropriately different from ADR-type deliverables.

**Traceability (0.10):** Source IDs used throughout. All theme analyses cite source numbers. Navigation table present. Footer revision notes are comprehensive.

**Step 3: Findings**

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-iter3 | Model-generation caveat present in Cross-References but absent from L0 primary recommendation bullet | Major | L0 first bullet: "Three of four major platform vendors recommend positive framing" — no qualifier about newer model behavior. Cross-References contains the caveat but not L0 | Completeness |
| SR-002-iter3 | Methodology section missing URL access dates and single-researcher limitation disclosure | Major | Methodology states "Searches conducted: 2026-02-27" for date but no "all URLs accessed [date]" or disclosure of single-researcher limitation | Methodological Rigor |
| SR-003-iter3 | Source Types table minor overcounting (Source 2 in community guide AND blog count) | Minor | Source 2 typed as "Community guide" in Source Table; Source Types table shows 17 blog posts + 1 community guide = 18 non-vendor/framework/forum sources, but 31-8-3-2=18 and 2+Source2=would make 18 sources fill 19 slots | Traceability |
| SR-004-iter3 | Theme 6 Pattern 4 not labeled as analyst inference | Minor | Pattern 4 ("Model-Specific Compliance Evolution") synthesizes Sources 4 and 5 into a trend characterization not explicitly labeled with an analyst-inference marker, unlike Patterns 1-3 | Internal Consistency |

---

### S-014: LLM-as-Judge

**Step 1: Load Deliverable and Context**

Deliverable: Industry survey on negative prompting, 31 core sources, 3 tiers. Revision 2. C4 criticality. Prior S-014 scores: Iter 1 = 0.770, Iter 2 = 0.907. Target: >= 0.95.

**Step 2: Score Each Dimension Independently**

**Completeness (weight 0.20)**

Rubric criteria: All major sections present; all required subsections populated; no gaps in coverage that would leave readers without critical information; L0 summary accurately represents L1/L2 content.

Evidence for:
- All 5 document sections present with full content
- L1 Source Catalog includes tier definitions (5 sub-categories), 31 source table entries, adjacent sources section, tier distribution table, source types table
- L2 covers 6 themes with detailed sub-analysis
- Gaps section explicitly identifies 8 unaddressed areas
- Cross-references section addresses model-generation confound and revision triggers

Evidence against:
- L0 primary recommendation bullet does not include the model-generation caveat (present only in Cross-References). A reader consuming only L0 receives the primary finding without the important temporal qualification that Sources 4/5 (GPT-4.1/GPT-5) suggest improved negative instruction compliance in newer models.
- Theme 6 Pattern 4 lacks analyst-inference label consistent with Patterns 1-3

Assessment: Document is highly complete. The model-generation caveat gap in L0 is a real but moderate issue — the caveat is present in the document, just not in the primary recommendation bullet where it most affects reader interpretation. Applying strict rubric comparison:

Score: **0.90** (Strong but not exceptional — the L0 model-generation caveat gap and Pattern 4 label gap prevent full score; these are meaningful coverage gaps for L0 readers)

**Internal Consistency (weight 0.20)**

Rubric criteria: No contradictions between sections; claims are internally self-consistent; evidence characterizations do not conflict across different document locations.

Evidence for:
- Percentages (29%/23%/48%) verified arithmetically correct
- Source tier classifications consistent throughout
- Pink Elephant caveat consistently labeled as hypothesis (Theme 2, Theme 5, L0)
- Bsharat et al. attribution consistent (corrected in Revision 2)
- U-shaped recovery caveat present in both Theme 2 and Theme 5
- Analyst-inference labels consistent for Patterns 1-3

Evidence against:
- Source Types table: "Blog post/article: 17" AND "Community guide: 1" creates a minor overcounting issue. Source 2 is classified as "Community guide" in the Source Table type column but the count of 17 blog posts would need to include Source 2 to reach 17 (without it, blogs = 16). This is a minor but verifiable internal inconsistency.
- Theme 6 Pattern 4 ("Model-Specific Compliance Evolution") synthesizes Sources 4 and 5 into a trend claim without an analyst-inference label, unlike Patterns 1-3 which carry explicit "(Sources X, Y -- analyst inference)" labels. This is a labeling inconsistency.

Assessment: High internal consistency overall. Two identified inconsistencies are both minor but real. Applying strict rubric:

Score: **0.90** (Strong — zero contradictions on material claims, minor inconsistencies on Source 2 typing and Pattern 4 label)

**Methodological Rigor (weight 0.20)**

Rubric criteria: Research methodology is appropriate to the task; selection criteria are defined and applied; limitations are acknowledged; procedures are transparent and reproducible.

Evidence for:
- 40 search queries explicitly listed
- Selection criteria defined (5 criteria)
- Exclusion decisions documented with rationale table
- Evidence tier system is well-defined with 5 sub-categories and epistemic weighting
- Per-source limitations documented throughout L2
- Model-generation confound explicitly noted in Cross-References
- Revision triggers defined

Evidence against:
- No saturation criterion for source count (31 sources). Standard systematic review practice requires either a saturation criterion ("no new themes emerged after N sources") or a predetermined scope statement. The methodology says 40 queries returned 31 qualifying sources — this is a convenience count, not a saturation-validated sample.
- Single-researcher limitation not disclosed. A single researcher executing queries in one session introduces query framing bias and missed perspectives. This is a standard disclosure requirement in landscape surveys.
- No URL access dates (e.g., "URLs accessed 2026-02-27"). This is a standard citation completeness requirement.

Assessment: Methodology section is more complete than most practitioner surveys but falls below academic survey standards on three specific points. For a C4 deliverable targeting the highest quality tier, these are meaningful gaps. Applying strict rubric comparison to the 0.95+ criteria (which requires systematic methodology fully documented):

Score: **0.87** (Acceptable to Strong range — excellent on coverage/criteria/exclusions; below threshold on saturation criterion, single-researcher disclosure, and URL access dates)

**Evidence Quality (weight 0.15)**

Rubric criteria: Claims are backed by specific evidence; evidence characterizations are accurate; source limitations are disclosed; quantitative claims are properly attributed.

Evidence for:
- Per-source limitations documented for every empirical source
- Analyst-inference labels applied to synthesized patterns (1-3)
- Bsharat et al. attribution corrected throughout
- Source 30 scope note present and accurate
- Source 18 competition-vs-peer-review caveat present
- Source 12 methodology-not-disclosed caveat present
- Pink Elephant analogy explicitly labeled as hypothesis (not mechanistic evidence)
- Sub-tier note in Evidence Tier Distribution accurately characterizes epistemic weight differences

Evidence against:
- Theme 6 Pattern 4 lacks analyst-inference label (minor gap)
- The 55%/66.7% figures are attributed to Bsharat et al. but the survey does not note these are 2023 GPT-4 figures whose currency is uncertain for 2025+ models
- DreamHost (Source 12) classified as "Empirical Evidence" despite undisclosed methodology; the sub-tier caveat addresses this, but the tier classification itself may over-elevate this source's standing

Assessment: Evidence quality is strong. The Bsharat et al. currency issue is partially addressed but could be more prominent. The three remaining gaps are minor.

Score: **0.93** (Strong — comprehensive source-level limitation documentation; minor gaps on Bsharat et al. currency and Pattern 4 inference label)

**Actionability (weight 0.15)**

Rubric criteria: For a research survey, actionability means practitioners can act on the findings; gaps section identifies clear next steps; recommendations are specific.

Evidence for:
- 8 specific gaps identified in the gaps section
- Cross-references section identifies 6 specific follow-up research areas
- Revision triggers defined (model generation, A/B study, 6-month elapsed)
- L0 provides clear, actionable recommendations (use positive framing; reserve negatives for safety; use programmatic enforcement)
- Theme analyses consistently link findings to actionable guidance

Evidence against:
- The primary finding ("positive framing preferred") lacks a qualifier for when this guideline applies to newer models — practitioners using GPT-5 or Claude 4 in 2026 may apply outdated guidance

Assessment: Actionability is strong for a research survey. The model-generation caveat issue reduces actionability slightly for cutting-edge practitioners.

Score: **0.91** (Strong — comprehensive gaps section and actionable guidance; slight reduction for model-generation caveat not reflected in primary recommendation)

**Traceability (weight 0.10)**

Rubric criteria: Sources are cited; claims trace to sources; source IDs are consistent; navigation table present.

Evidence for:
- Navigation table with anchor links present (H-23/H-24 compliant)
- Source numbers cited throughout L2 analysis (Source X pattern)
- All 31 sources in L1 table accessible by number
- Adjacent Sources section explicitly documents Source 26 exclusion with rationale
- Footer revision notes trace changes back to specific findings from prior iterations

Evidence against:
- Source Types table has minor overcounting issue (Source 2 / blog count)
- No URL access dates (standard traceability requirement for web sources)
- Theme 6 Pattern 4 cites Sources 4, 5 but not labeled as analyst inference (reduces traceability of the editorial synthesis decision)

Score: **0.89** (Acceptable-to-Strong — good source citation throughout; reduced by URL access date gap and Source Types table discrepancy)

**Step 3: Compute Weighted Composite**

```
composite = (0.90 × 0.20) + (0.90 × 0.20) + (0.87 × 0.20) + (0.93 × 0.15) + (0.91 × 0.15) + (0.89 × 0.10)
          = 0.180 + 0.180 + 0.174 + 0.1395 + 0.1365 + 0.089
          = 0.899
```

Rounded to two decimal places: **0.90**

**Step 4: Determine Verdict**

Composite 0.90 is in the 0.85-0.91 REVISE band. H-13 threshold not met (< 0.92).

**Verdict: REVISE**

**Step 5: Improvement Recommendations**

| Priority | Dimension | Current Score | Gap | Recommendation |
|----------|-----------|---------------|-----|----------------|
| 1 | Methodological Rigor | 0.87 | 0.05+ | Add to Methodology section: (a) URL access date "All URLs accessed 2026-02-27", (b) single-researcher limitation disclosure, (c) saturation criterion acknowledgment |
| 2 | Traceability | 0.89 | 0.03+ | Correct Source Types table (Source 2 overcounting); add URL access dates |
| 3 | Completeness | 0.90 | 0.02+ | Add model-generation caveat to L0 primary recommendation bullet; add analyst-inference label to Theme 6 Pattern 4 |
| 4 | Internal Consistency | 0.90 | 0.02+ | Correct Source 2 type ambiguity; add Pattern 4 analyst-inference label |
| 5 | Actionability | 0.91 | 0.01 | Add model-gen qualifier to L0 recommendation bullet |

**Step 6: Leniency Bias Check**

- Methodological Rigor 0.87: Verified against rubric. The three missing methodology components (saturation criterion, single-researcher disclosure, URL access dates) are genuine and standard. 0.87 is not lenient.
- Completeness 0.90: The L0 model-generation caveat gap is real but moderate (caveat exists in Cross-References). 0.90 is appropriate.
- Internal Consistency 0.90: Two minor but verifiable inconsistencies. 0.90 is appropriate.
- Evidence Quality 0.93: High score justified by comprehensive per-source documentation. Not lenient.
- Actionability 0.91: High score; small reduction for model-gen caveat. Appropriate.
- Traceability 0.89: URL access date gap and Source Types table discrepancy justify < 0.90. Appropriate.

No leniency bias detected. Scores reflect literal rubric application.

**Step 7: Score Report**

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.90 | 0.180 |
| Internal Consistency | 0.20 | 0.90 | 0.180 |
| Methodological Rigor | 0.20 | 0.87 | 0.174 |
| Evidence Quality | 0.15 | 0.93 | 0.1395 |
| Actionability | 0.15 | 0.91 | 0.1365 |
| Traceability | 0.10 | 0.89 | 0.089 |
| **Composite** | | | **0.899 → 0.90** |

---

## Part II: Findings Summary

| ID | Strategy | Severity | Finding | Section |
|----|---------|---------|---------|---------|
| SM-001-iter3 | S-003 | Minor | Cross-vendor synthesis table could include evidence tier column | L2 Theme 1 |
| SM-002-iter3 | S-003 | Minor | Theme 5 GitHub issue numbers not prominent in body text | L2 Theme 5 |
| SM-003-iter3 | S-003 | Minor | Sub-tier distribution note letter references require scrolling | L1 Distribution |
| DA-001-iter3 | S-002 | Major | Recency confound: newer models follow negatives more literally — this is not prominent in L0 | L0, Theme 6 |
| DA-002-iter3 | S-002 | Major | No saturation criterion for 31-source count | Methodology |
| DA-003-iter3 | S-002 | Minor | Cross-vendor convergence may reflect shared industry norms rather than independent validation | L2 Theme 6 |
| DA-004-iter3 | S-002 | Minor | L0 headlines the negative-framing-fails narrative despite nuanced counterevidence in body | L0 |
| PM-001-iter3 | S-004 | Major | Model-generation confound acknowledged in Cross-References but not mitigated in L0 | Cross-References |
| PM-002-iter3 | S-004 | Major | URL access dates not documented | Methodology |
| PM-003-iter3 | S-004 | Major | Bsharat et al. figures are 2023/GPT-4; currency for 2026 models uncertain | L0, L2 |
| PM-004-iter3 | S-004 | Major (Critical by FMEA) | Single-researcher/single-session limitation not disclosed | Methodology |
| PM-005-iter3 | S-004 | Minor | Instruction decay figures (95%→20-60%) have undisclosed methodology | L2 Theme 2 |
| PM-006-iter3 | S-004 | Minor | DreamHost as "Empirical Evidence" classification may over-elevate | L1 Source Table |
| FM-001-iter3 | S-012 | Major (RPN=144) | Model-gen caveat not in L0 | L0 |
| FM-002-iter3 | S-012 | Major (RPN=168) | URL access dates not documented | Methodology |
| FM-003-iter3 | S-012 | Major (RPN=150) | No saturation criterion | Methodology |
| FM-004-iter3 | S-012 | Critical (RPN=210) | Single-researcher limitation not disclosed | Methodology |
| FM-005-iter3 | S-012 | Minor (RPN=60) | Source 32 URL links to #5055 only | L1 Source Table |
| FM-006-iter3 | S-012 | Major (RPN=100) | Patterns 4-5 lack analyst-inference labels | L2 Theme 6 |
| FM-007-iter3 | S-012 | Minor (RPN=72) | Bsharat et al. currency limitation prominent per-source but not in summary | L2 Theme 2 |
| IN-001-iter3 | S-013 | Major | Coverage adequacy assumption unvalidated | Methodology |
| IN-002-iter3 | S-013 | Minor | English-language-only scope not disclosed | Methodology |
| IN-003-iter3 | S-013 | Major | URL decay risk unaddressed | Methodology |
| IN-004-iter3 | S-013 | Minor | Publication date currency risk partially mitigated | Cross-References |
| RT-001-iter3 | S-001 | Major | Convenience sample — no saturation criterion | Methodology |
| RT-002-iter3 | S-001 | Major | Temporal obsolescence risk — L0 conclusion not model-gen qualified | L0 |
| RT-003-iter3 | S-001 | Minor | Source Types table overcounting (Source 2) | L1 Source Types |
| RT-004-iter3 | S-001 | Major | Single-researcher limitation not disclosed | Methodology |
| RT-005-iter3 | S-001 | Minor | URL access dates missing | Methodology |
| CV-001-iter3 | S-011 | Minor | Source 2 overcounting in Source Types table | L1 Source Types |
| SR-001-iter3 | S-010 | Major | L0 lacks model-generation caveat in primary recommendation | L0 |
| SR-002-iter3 | S-010 | Major | Methodology missing URL access dates and single-researcher limitation | Methodology |
| SR-003-iter3 | S-010 | Minor | Source Types table minor overcounting | L1 Source Types |
| SR-004-iter3 | S-010 | Minor | Theme 6 Pattern 4 lacks analyst-inference label | L2 Theme 6 |
| LJ-001-iter3 | S-014 | Minor | Completeness 0.90 — L0 model-gen caveat gap and Pattern 4 label | L0, L2 |
| LJ-002-iter3 | S-014 | Minor | Internal Consistency 0.90 — Source 2 type ambiguity, Pattern 4 label | L1, L2 |
| LJ-003-iter3 | S-014 | Major | Methodological Rigor 0.87 — saturation criterion, single-researcher, URL access dates | Methodology |
| LJ-004-iter3 | S-014 | Minor | Evidence Quality 0.93 — Pattern 4 label, Bsharat currency | L2 |
| LJ-005-iter3 | S-014 | Minor | Actionability 0.91 — model-gen caveat absent from primary recommendation | L0 |
| LJ-006-iter3 | S-014 | Minor | Traceability 0.89 — URL access dates, Source Types table | Methodology, L1 |

---

## Part III: Consolidated Finding Groups

Cross-strategy findings converge on **4 distinct actionable gaps**:

### Gap A: Methodology Disclosure (P0 — blocks 0.95 threshold)
Converged findings: DA-002, PM-004, FM-003, FM-004, IN-001, RT-001, RT-004, SR-002, LJ-003

The Methodology section is missing three standard survey disclosure components:
1. **Single-researcher/single-session limitation**: All 40 queries conducted by one researcher in one session; this is not disclosed and represents a standard survey limitation acknowledgment
2. **URL access dates**: No "all URLs accessed 2026-02-27" statement; standard citation requirement for web sources
3. **Saturation criterion**: 31 sources is the output of the search strategy, not a saturation-validated sample; this should be explicitly acknowledged

**Corrective action:** Add 3-sentence paragraph to Methodology section (or sub-section) acknowledging: (a) single-researcher limitation with query framing bias risk; (b) absence of saturation criterion; (c) URL access date.

### Gap B: L0 Model-Generation Caveat (P1 — affects Completeness and Actionability)
Converged findings: DA-001, PM-001, FM-001, RT-002, SR-001, LJ-001, LJ-005

The primary L0 recommendation ("positive framing preferred") is accurate for the surveyed sources but the model-generation caveat (documented in Cross-References) is not surfaced in L0. Sources 4 and 5 (GPT-4.1 and GPT-5) document improved negative instruction compliance in newer models. A practitioner reading only L0 misses this qualification.

**Corrective action:** Add a qualifier sentence to the first L0 bullet (or a standalone L0 bullet) noting that newer model generations (GPT-4.1, GPT-5, Claude 4) follow instructions more literally including negatives, and that the survey's primary finding reflects the balance of evidence across 2023-2026 source dates rather than a claim about current frontier model behavior.

### Gap C: Theme 6 Pattern 4 Analyst-Inference Label (P2 — affects Internal Consistency)
Converged findings: FM-006, SR-004, LJ-002, LJ-004

Theme 6 Patterns 1-3 carry explicit "(Sources X, Y -- analyst inference)" labels per Revision 2 fixes. Pattern 4 ("Model-Specific Compliance Evolution") synthesizes a trend narrative from Sources 4 and 5 without the same labeling. This creates an inconsistency in the systematic application of the analyst-inference labeling convention.

**Corrective action:** Add analyst-inference label to Pattern 4 heading: "Pattern 4: Model-Specific Compliance Evolution (Sources 4, 5 -- analyst synthesis)"

### Gap D: Source Types Table Source 2 Overcounting (P2 — affects Traceability)
Converged findings: CV-001, RT-003, SR-003, LJ-006

Source 2 (DAIR-AI / PromptingGuide.ai) is typed as "Community guide" in the Source Table but the Source Types table reports 17 blog posts AND 1 community guide. If blog posts = 17, that count must include Source 2. If Source 2 is Community guide, blog posts should be 16. The table reports both, which overcounts by 1.

**Corrective action:** Either (a) reclassify Source 2 as "Blog post / article" (change its type in the Source Table from "Community guide" to "Blog post / article" — and set community guide count to 0), or (b) keep Source 2 as "Community guide" and correct the blog count from 17 to 16. Recommendation: option (b), keeping "Community guide" as a distinct type that accurately describes PromptingGuide.ai, and correcting the blog count to 16.

---

## Part IV: S-014 Score Report

### Dimension Scores

| Dimension | Weight | Score | Weighted Score | Evidence Summary |
|-----------|--------|-------|---------------|-----------------|
| Completeness | 0.20 | 0.90 | 0.180 | High completeness; L0 model-gen caveat gap and Pattern 4 label gap prevent full score |
| Internal Consistency | 0.20 | 0.90 | 0.180 | Zero material contradictions; Source 2 type ambiguity and Pattern 4 label inconsistency are minor but real |
| Methodological Rigor | 0.20 | 0.87 | 0.174 | Strong on criteria/exclusions/coverage; missing saturation criterion, single-researcher disclosure, URL access dates |
| Evidence Quality | 0.15 | 0.93 | 0.1395 | Comprehensive per-source documentation; analyst-inference labels for Patterns 1-3; correct Bsharat et al. attribution |
| Actionability | 0.15 | 0.91 | 0.1365 | Comprehensive gaps section and revision triggers; slight reduction for model-gen caveat absent from primary recommendation |
| Traceability | 0.10 | 0.89 | 0.089 | Good source citation throughout; URL access date gap and Source Types discrepancy reduce score |

### Weighted Composite

```
composite = 0.180 + 0.180 + 0.174 + 0.1395 + 0.1365 + 0.089
          = 0.899
```

**Composite Score: 0.90**

### Verdict

**REVISE** — Composite 0.90 is in the 0.85-0.91 band. Below H-13 threshold (0.92). Below target threshold (0.95).

### Gap to Thresholds

- Gap to 0.92 (H-13): 0.02 points
- Gap to 0.95 (target): 0.05 points

### Projected Score After Addressing All 4 Gaps

If all 4 gaps are addressed:
- Methodological Rigor: 0.87 → 0.94 (single-researcher + saturation + URL access dates = full methodology disclosure)
- Traceability: 0.89 → 0.94 (URL access dates + Source Types correction)
- Completeness: 0.90 → 0.94 (L0 model-gen caveat + Pattern 4 label)
- Internal Consistency: 0.90 → 0.94 (Source 2 type fix + Pattern 4 label)
- Evidence Quality: 0.93 → 0.94 (Pattern 4 label fix)
- Actionability: 0.91 → 0.94 (L0 model-gen caveat)

```
projected = (0.94 × 0.20) + (0.94 × 0.20) + (0.94 × 0.20) + (0.94 × 0.15) + (0.94 × 0.15) + (0.94 × 0.10)
           = 0.188 + 0.188 + 0.188 + 0.141 + 0.141 + 0.094
           = 0.94
```

**Projected Composite After Full Remediation: 0.94** — This meets H-13 (>= 0.92) but falls short of the 0.95 target. Reaching 0.95 requires addressing the gaps to an exceptional standard, not merely adequate.

---

## Execution Statistics

- **Total Findings:** 37 (across all strategies)
- **Critical:** 1 (FM-004-iter3: single-researcher limitation not disclosed, RPN=210)
- **Major:** 15
- **Minor:** 21
- **Protocol Steps Completed:** All 10 strategies fully executed (S-003, S-007, S-002, S-004, S-012, S-013, S-011, S-001, S-010, S-014)
- **Composite Score:** 0.90
- **Verdict:** REVISE (below H-13 threshold 0.92; below target 0.95)
- **Convergent Gap Analysis:** 4 distinct actionable gaps identified across strategies (Gaps A-D)

---

## Iteration 3 Comparison

| Dimension | Iter 1 | Iter 2 | Iter 3 | Delta Iter2→3 |
|-----------|--------|--------|--------|---------------|
| Completeness | ~0.72 | ~0.88 | 0.90 | +0.02 |
| Internal Consistency | ~0.76 | ~0.92 | 0.90 | -0.02 |
| Methodological Rigor | ~0.72 | ~0.88 | 0.87 | -0.01 |
| Evidence Quality | ~0.82 | ~0.92 | 0.93 | +0.01 |
| Actionability | ~0.78 | ~0.93 | 0.91 | -0.02 |
| Traceability | ~0.72 | ~0.90 | 0.89 | -0.01 |
| **Composite** | **0.770** | **0.907** | **0.90** | **-0.007** |

**Analysis:** The composite score declined slightly from 0.907 to 0.90. This is not a sign of regression in the document — it reflects two factors: (1) Iter 3 applies stricter scrutiny to methodology section gaps (single-researcher limitation, saturation criterion, URL access dates) that were present but unexamined in Iter 2; (2) The Internal Consistency and Traceability scores exposed a Source 2 counting issue that Iter 2 missed. The document is genuinely good quality; the remaining gaps are concentrated in methodology disclosure standards that are fixable with a targeted revision.

---

## Priority-Ordered Remediation Plan

**P0 (Critical — addresses FM-004-iter3 and Gap A, largest score impact):**

Add to Methodology section (after "Date Range" or as new sub-section "Limitations"):

> "**Survey Limitations:** This survey was conducted by a single researcher executing all 40 search queries in a single session (2026-02-27). A different researcher with alternative query formulations or different search platforms may surface additional sources not included here. No saturation criterion was applied to the source count; 31 sources reflects the output of the defined search strategy against the stated selection criteria, not a saturation-validated representative sample. All source URLs were accessed 2026-02-27; link availability may degrade over time. Non-English language sources were not systematically searched."

**P1 (Major — addresses Gap B, affects L0 reader experience):**

Add to L0 first bullet (after the sentence ending "...programmatic enforcement via frameworks like DSPy Assertions and NeMo Guardrails."):

> "Note: This recommendation reflects the balance of evidence across 2023-2026 sources. Sources 4 and 5 (OpenAI GPT-4.1/GPT-5 guides) document that newer model generations follow instructions more literally including negative instructions; the effectiveness of positive framing may continue to evolve with model capability. See Cross-References for the model-generation confound discussion."

**P2 (Minor — addresses Gaps C and D, affects internal consistency):**

1. Theme 6 Pattern 4 heading: Change "Pattern 4: Model-Specific Compliance Evolution (Sources 4, 5)" to "Pattern 4: Model-Specific Compliance Evolution (Sources 4, 5 -- analyst synthesis)"

2. Source Types table: Change "Blog post / article: 17" to "Blog post / article: 16" (Source 2 remains classified as Community guide per its Source Table type entry)

---

*Execution report produced by adv-executor for PROJ-014-negative-prompting-research, Iteration 3.*
*All 10 C4 strategies executed: S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014*
*H-16 compliance: S-003 (Steelman) executed first*
*P-002 compliance: Report persisted to file*
*H-15 compliance: Self-review applied before persistence*
*Date: 2026-02-27*
*Agent: adv-executor*
