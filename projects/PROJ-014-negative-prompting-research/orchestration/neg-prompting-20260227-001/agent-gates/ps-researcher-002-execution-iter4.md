# Strategy Execution Report: C4 Full Tournament — Industry Survey (Iteration 4)

## Execution Context

- **Strategy:** C4 Tournament (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014)
- **Templates:** `.context/templates/adversarial/s-00{1,2,3,4,7,10,11,12,13,14}.md`
- **Deliverable:** `projects/PROJ-014-negative-prompting-research/research/industry-survey.md`
- **Executed:** 2026-02-27T00:00:00Z
- **Iteration:** 4 of N (prior scores: Iter 1 = 0.770, Iter 2 = 0.907, Iter 3 = 0.900)
- **H-16 Compliance:** S-003 (Steelman) executed before all critique strategies
- **Leniency Bias Counteraction:** Active — scoring absolute quality, NOT improvement trajectory
- **Prior Convergent Gaps Addressed (Revision 3):**
  - Gap A (P0): Added Survey Limitations sub-section (single-researcher, single-session, no saturation criterion, URL access dates, English-only scope)
  - Gap B (P1): Added model-generation caveat to L0 primary recommendation bullet
  - Gap C (P2): Added analyst-synthesis label to Theme 6 Pattern 4 heading and body text
  - Gap D (P2): Verified Source Types table counts — blog count of 17 confirmed correct (Source 20/QED42 is a blog; Source 2 is community guide; 17+1+8+3+2=31)

---

## Part I: Strategy Executions (S-001 through S-013)

---

### S-003: Steelman Technique

**H-16 Compliance:** S-003 executes first per mandatory ordering.

**Step 1: Deep Understanding**

The deliverable is a 31-source industry and practitioner survey on negative prompting in LLMs, now in its fourth iteration. Core thesis: negative instructions in LLMs are less effective than positive framing for behavioral control, with documented failure mechanisms (attention-based concept activation, inverse scaling, instruction count degradation, positional decay, context compaction loss, semantic confusion), though negative constraints retain legitimate roles in safety boundaries and programmatic enforcement. The document is structured in three tiers (L0 executive summary, L1 source catalog, L2 detailed analysis) with cross-references and methodology sections.

After three revision cycles, the document has addressed every convergent gap identified in prior tournament rounds:
- Evidence tier definitions with 5 sub-categories and epistemic weighting (added Revision 1)
- Source count corrected to 31 core + 1 adjacent with all percentages recalculated (Revision 2)
- Analyst-inference labels on all Theme 6 Patterns 1-4 (Revision 2-3)
- U-shaped recovery caveats in both relevant locations (Revision 2)
- Bsharat et al. attribution corrected throughout (Revision 2)
- Survey Limitations sub-section with full methodological disclosure (Revision 3)
- Model-generation caveat in L0 primary recommendation bullet (Revision 3)

**Step 2: Identify Presentation Weaknesses**

| Weakness | Type | Magnitude |
|----------|------|-----------|
| Source Types table shows "Blog post / article: 17" alongside "Community guide: 1" with total = 31 — this is mathematically sound if Source 20 (QED42) is a blog, which it is, but the inclusion of Source 20 in the blog count is not obvious to a reader cross-checking the table | Presentational | Minor |
| The Survey Limitations paragraph is dense — five distinct limitations compressed into a single paragraph rather than a structured list | Structural | Minor |
| Cross-Vendor Synthesis table (Theme 1) lacks an "Evidence Tier" column, limiting readers' ability to evaluate the relative weight of each vendor's recommendation | Structural | Minor |
| The primary recommendation in L0 now carries a model-generation caveat, but the caveat describes the *narrowing* of the effectiveness gap — it does not fully acknowledge that for current frontier models, the primary finding may not hold at all | Analytical | Minor |
| Theme 3 "System Prompt Architecture" section cites "Source 1, 4, 5, 28" but the inline text only discusses Sources 1, 4, and 5 in the preceding paragraph; Source 28's relevance to system prompt architecture is implied rather than stated | Traceability | Minor |

**Step 3: Steelman Assessment**

| Weakness | Type | Magnitude |
|----------|------|-----------|
| Survey Limitations paragraph density | Structural | Minor |
| Cross-vendor synthesis evidence tier column missing | Structural | Minor |
| L0 caveat language characterizes narrowing effectiveness gap rather than possible reversal | Analytical | Minor |
| Theme 3 Source 28 citation without explicit link to system prompt architecture | Traceability | Minor |

**Step 4: Best Case Scenario**

Under ideal conditions, this is a comprehensive, self-critical Phase 1 landscape survey that:
1. Accurately represents the prevailing industry consensus across all major platform vendors
2. Honestly categorizes evidence quality with exceptional per-source limitation documentation
3. Acknowledges its own methodological constraints explicitly
4. Enables Phase 2 (academic survey) and Phase 3 (synthesis) to build on reliable foundations

The document's epistemic honesty — distinguishing vendor recommendations from empirical evidence, labeling analyst inferences explicitly, qualifying all quantitative figures — is its greatest strength.

**Step 5: Improvement Findings**

| ID | Improvement | Severity | Dimension |
|----|-------------|----------|-----------|
| SM-001-iter4 | Cross-vendor synthesis table could include evidence tier column | Minor | Evidence Quality |
| SM-002-iter4 | Survey Limitations paragraph could be restructured as a bulleted list for navigability | Minor | Completeness |
| SM-003-iter4 | L0 model-generation caveat could more explicitly note that the survey's primary finding may not apply to current frontier models (not just that the gap "may narrow") | Minor | Completeness |
| SM-004-iter4 | Theme 3 Source 28 reference in "System Prompt Architecture" section should be explicitly linked to context compaction (not just implied) | Minor | Traceability |

**Steelman Assessment:** Document has achieved strong quality after three revision cycles. All major structural, methodological, and analytical gaps from prior iterations have been addressed. Remaining weaknesses are presentational (density of limitations paragraph) and minor analytical (caveat language precision in L0). The core evidence framework, tier definitions, and analytical structure are sound. Ready for adversarial critique.

---

### S-007: Constitutional AI Critique

**Applicable Principles for Document Deliverable:**
- H-23: Navigation table required for documents over 30 lines (HARD)
- H-24: Navigation table anchor links required (HARD)
- P-001: Truth/Accuracy — no misrepresentation
- P-004: Provenance — claims traced to sources
- P-011: Evidence-based claims with citations
- H-15: Self-review before presenting

**Step 1: Identify Applicable Principles**

For a research survey deliverable, the constitutional principles are:
1. Structural compliance (H-23, H-24): navigation table presence and format
2. Accuracy principles (P-001, P-004, P-011): all claims attributed, evidence-based
3. Process principles (H-15): self-review applied

**Step 2: Principle-by-Principle Evaluation**

| ID | Principle | Tier | Result | Evidence |
|----|-----------|------|--------|---------|
| CC-001-iter4 | H-23: Navigation table | HARD | COMPLIANT | Document Sections table present with 5 sections, each with anchor link |
| CC-002-iter4 | H-24: Anchor links | HARD | COMPLIANT | All navigation entries use markdown anchor link syntax |
| CC-003-iter4 | P-001: Truth/Accuracy | MEDIUM | COMPLIANT | Evidence tiers accurately labeled; claims qualified with per-source caveats; analyst-inference labels applied to synthesized patterns |
| CC-004-iter4 | P-004: Provenance | MEDIUM | COMPLIANT | All claims attributed to specific source IDs; quantitative figures attributed to primary sources (Bsharat et al., not PromptHub); footer revision notes trace changes |
| CC-005-iter4 | P-011: Evidence citations | MEDIUM | COMPLIANT | Source references throughout L2; every theme analysis cites source numbers; per-source limitations noted |
| CC-006-iter4 | H-15: Self-review | MEDIUM | COMPLIANT | Revision 3 footer explicitly documents S-010 self-review application and verification results |

**Step 3: Constitutional Violations**

None detected. All HARD rules satisfied. All MEDIUM principles met.

**Assessment:** No constitutional violations found. The document demonstrates exceptional adherence to provenance and accuracy principles, with explicit analyst-inference labels, per-source limitation documentation, and clear distinction between evidence tiers.

**Constitutional Compliance Score:** 1.00 - 0 = 1.00 → **PASS**

---

### S-002: Devil's Advocate

**H-16 Compliance:** S-003 executed prior. Proceeding.

**Step 1: Role Assumption**

Deliverable: Industry survey on negative prompting, Revision 3. Criticality: C4. H-16 confirmed. Adopting adversarial stance: finding the strongest reasons the deliverable's claims are wrong, incomplete, or analytically insufficient despite three revision cycles.

**Step 2: Challenge Assumptions**

| Assumption | Challenge |
|------------|-----------|
| Survey Limitations paragraph adequately discloses methodological constraints | The paragraph discloses the right facts but buries them: "No formal saturation criterion was applied" and "A different researcher...may surface additional sources" are mixed into a dense paragraph. Reviewers doing a quality audit might miss these disclosures |
| The model-generation caveat in L0 adequately qualifies the primary finding | The caveat says the "effectiveness gap...may narrow with future model capability improvements" — but Sources 4 and 5 are from 2025 (not "future models"); the narrowing may already have occurred. The framing as "future" may be inaccurate |
| Source 30 (Big Data Guy/sentiment study) belongs in the Empirical Evidence tier | Source 30 measures emotional sentiment effects, not instructional negation. Classifying it as Empirical Evidence (even with a scope note) may overstate its relevance to the core research question |
| 31 sources adequately represent industry consensus | The survey specifically excludes non-English sources (now disclosed). If significant practitioner communities in China or Japan have different findings on LLM negation handling, the claimed "consensus" is geographically and linguistically narrow |

**Step 3: Counter-Arguments**

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter4 | The L0 model-generation caveat uses temporal framing ("future model capability improvements") that may be factually incorrect — Sources 4 and 5 are *current* 2025 documentation, not future projections. The gap may have already narrowed. | Major | L0 bullet 1: "The effectiveness gap between positive and negative framing may narrow with future model capability improvements." Sources 4 (GPT-4.1, 2025) and 5 (GPT-5, 2025) document *current* models following negatives more literally. The word "future" is inaccurate — this narrowing is documented in *present* 2025 sources. | Accuracy / Internal Consistency |
| DA-002-iter4 | Source 30 (Big Data Guy sentiment study) is classified as "Empirical Evidence" and counts toward the 23% empirical percentage, but it measures *emotional sentiment*, not *instructional negation*. Including it in the Empirical tier inflates the empirical percentage by 1/7 (~14% inflation within the tier) | Minor | Source 30 scope note in Source Table and L2 Theme 2 clearly states it measures emotional tone, not instruction syntax. The per-source caveat is present. However, the source still counts in the "Empirical Evidence" tier and "23% empirical" claim, even though its evidence is about a related but distinct phenomenon. | Evidence Quality / Methodological Rigor |
| DA-003-iter4 | The English-language limitation is disclosed ("Non-English language sources were not systematically searched") but not assessed for impact. Practitioner communities in non-English contexts may have published different empirical findings; the survey cannot characterize whether this omission is material | Minor | Survey Limitations paragraph: "Non-English language sources were not systematically searched." This is present but passive — the survey does not assess whether non-English literature might contain contrary evidence | Completeness |
| DA-004-iter4 | Cross-Vendor Convergence section (Theme 6) claims "all major vendors converge on the same recommendation" — but Palantir's explicit balanced approach (treating negatives as standard tools) contradicts this convergence narrative. The body of Theme 1 correctly documents Palantir as the exception, but Theme 6's convergence claim is overstated | Minor | Theme 6 Cross-Vendor Convergence: "all major vendors converge on the same recommendation: positive framing preferred, negatives for narrow safety boundaries only." Theme 1 Palantir subsection: "treats negatives as one tool among many rather than as categorically inferior." These statements are in tension. | Internal Consistency |

**Step 4: Response Requirements**

| Priority | Finding | Required Response |
|----------|---------|-------------------|
| P1 | DA-001-iter4 | Correct L0 caveat temporal framing: replace "may narrow with future model capability improvements" with accurate language acknowledging that GPT-4.1 and GPT-5 (2025 current models) already show improved negative instruction compliance. |
| P2 | DA-002-iter4 | Acknowledge in the Evidence Landscape Assessment that the 23% empirical figure includes Source 30 which measures emotional sentiment (not instruction syntax), and that the "strict" empirical count (addressing instructional negation directly) is lower |
| P2 | DA-003-iter4 | Assess impact of English-language limitation — at minimum note whether the researcher believes non-English literature would likely contain contrary evidence |
| P2 | DA-004-iter4 | Reconcile Theme 6 Cross-Vendor Convergence claim with Palantir's documented balanced approach — either qualify "all major vendors" or explicitly exclude Palantir from the convergence claim |

---

### S-004: Pre-Mortem Analysis

**H-16 Compliance:** S-003 executed prior. Proceeding.

**Step 1: Set the Stage**

Failure scenario: "It is November 2026. The Phase 1 industry survey has been cited in the Phase 3 synthesis. A practitioner using the survey applies the primary L0 recommendation to a GPT-5 system prompt in production and experiences unexpected behavior because GPT-5's improved literal compliance (documented in Source 5, GPT-5 Prompting Guide, 2025) inverts the survey's guidance in their specific use case. They read the survey's L0 caveat and find it describes this narrowing as something that 'may' happen with 'future' models — but the GPT-5 guide was published in 2025, and they are using GPT-5 now. The survey's temporal framing creates false confidence."

**Step 2: Declare Failure**

Temporal frame established: Looking back from November 2026 at a survey misapplied due to temporal caveat inaccuracy.

**Step 3: Generate Failure Causes**

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-iter4 | L0 model-generation caveat uses "future" framing when Sources 4-5 are current 2025 documents; practitioners reading L0 may believe the narrowing is speculative/future when it has already been documented | Accuracy | High | Major | P1 | Accuracy / Completeness |
| PM-002-iter4 | Source 30 (sentiment study) counted in the 23% empirical figure; if cited by Phase 3 synthesis as "23% of sources provided empirical evidence on instructional negation," this would be a factual overstatement since Source 30 does not address instructional negation | Precision | Medium | Minor | P2 | Methodological Rigor |
| PM-003-iter4 | URL decay: 31 URLs accessed 2026-02-27 with access date now disclosed; but no archived copies; by November 2026 (9 months) some links will likely be dead (typical blog decay rate 10-20%/year) | Technical | Medium | Minor | P2 | Traceability |
| PM-004-iter4 | Theme 6 convergence claim overstates vendor agreement; a Phase 3 synthesis author may cite "all major vendors converge" without noting Palantir's documented divergence | Precision | Low | Minor | P2 | Internal Consistency |
| PM-005-iter4 | Survey Limitations paragraph is a single dense block; a future reader auditing methodology may miss the saturation criterion disclosure or single-researcher disclosure if scanning quickly | Structural | Low | Minor | P3 | Methodological Rigor |

**Step 4: Prioritize**

P1 findings: PM-001 (Major severity, High likelihood — the "future" language is factually incorrect)
P2 findings: PM-002 through PM-004 (Minor severity)
P3 findings: PM-005 (low severity/likelihood)

**Step 5: Mitigations**

| ID | Mitigation | Status |
|----|-----------|--------|
| PM-001-iter4 | Correct "future" framing in L0 caveat to reflect that Sources 4-5 document current behavior | OPEN — specific wording needs correction |
| PM-002-iter4 | Add clarifying note to Evidence Landscape Assessment about Source 30's scope | PARTIAL — scope note exists per-source but not in the aggregate statistics context |
| PM-003-iter4 | URL access date now documented ("All source URLs were accessed 2026-02-27") — adequate | CLOSED (adequate as-is; no archived copies is an acknowledged limitation) |
| PM-004-iter4 | Theme 6 convergence claim should qualify Palantir | OPEN — minor precision fix needed |

---

### S-012: FMEA

**Step 1: Decompose**

| Element | ID |
|---------|-----|
| L0 Executive Summary (5 bullets + 2 sub-sections) | E1 |
| L1 Source Catalog (tier defs + source table + adjacent + tier distribution) | E2 |
| L2 Detailed Analysis (6 themes) | E3 |
| Cross-References section | E4 |
| Methodology section (with Survey Limitations sub-section) | E5 |

**Step 2-3: Failure Modes and RPN**

Scale: Severity (1-10), Occurrence (1-10), Detectability (1-10; 1=easy to detect, 10=hard to detect). RPN = S × O × D.

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Dimension |
|----|---------|-------------|---|---|---|-----|----------|-----------|
| FM-001-iter4 | E1 (L0) | Model-gen caveat uses "future" framing for Sources 4-5 which are 2025 current documents; may mislead practitioners about current applicability | 6 | 7 | 5 | 210 | Major | Accuracy |
| FM-002-iter4 | E2 (L1 Source Table) | Source 30 (sentiment study) classified as Empirical Evidence and counted in the 23% figure; scope note present per-source but the aggregate 23% figure implicitly conflates emotional sentiment evidence with instructional negation evidence | 4 | 5 | 6 | 120 | Minor | Evidence Quality |
| FM-003-iter4 | E3 (L2 Theme 6) | Cross-Vendor Convergence claim ("all major vendors converge") conflicts with Theme 1's accurate depiction of Palantir as an exception | 4 | 5 | 5 | 100 | Minor | Internal Consistency |
| FM-004-iter4 | E5 (Methodology) | Survey Limitations paragraph (Revision 3 addition) condenses five distinct limitations into one dense paragraph; readers scanning quickly may not register all five limitations | 3 | 4 | 6 | 72 | Minor | Methodological Rigor |
| FM-005-iter4 | E3 (L2 Theme 3) | "System Prompt Architecture" section cites Source 28 but the preceding paragraph's architecture pattern discussion does not explicitly link Source 28 to context compaction; Source 28 is primarily about context compaction (not system prompt architecture patterns) | 3 | 4 | 5 | 60 | Minor | Traceability |
| FM-006-iter4 | E2 (L1 Distribution) | "Sub-tier note" references sub-categories (a)-(e) but readers must scroll to Tier Definitions to decode the letters; no inline legend | 2 | 4 | 7 | 56 | Minor | Completeness |

**Step 4: Prioritize**

Critical: None
Major: FM-001-iter4 (RPN=210): "Future" temporal framing in L0 model-gen caveat
Minor: FM-002-iter4 (120), FM-003-iter4 (100), FM-004-iter4 (72), FM-005-iter4 (60), FM-006-iter4 (56)

**Assessment:** The prior Critical/Major findings from Iterations 1-3 (single-researcher disclosure, URL access dates, saturation criterion, L0 model-gen caveat absence, Source count error) have all been resolved. One new Major finding emerges: FM-001 — the Revision 3 fix for the L0 model-generation caveat introduced a temporal accuracy error by describing current documented behavior as "future."

---

### S-013: Inversion Technique

**Step 1: Goals**

1. Provide decision-grade Phase 1 landscape intelligence on negative prompting in LLMs
2. Accurately represent the evidence landscape including its limitations and temporal boundaries
3. Enable Phase 2 (academic survey) and Phase 3 (synthesis) to build on reliable foundations
4. Achieve >= 0.95 quality gate for C4 tournament

**Step 2: Anti-Goals (Inversion)**

To guarantee this survey FAILS its purpose:
- Present vendor recommendations as empirical evidence (avoided — tier system prevents this)
- Omit uncertainty qualifications (avoided — extensive per-source caveats present)
- Omit major limitation categories (PARTIALLY ADDRESSED: single-researcher limitation now disclosed in Survey Limitations paragraph)
- Allow key quantitative figures to be mis-cited (avoided — Bsharat et al. attribution corrected)
- Present outdated evidence as current (RISK REMAINS: L0 caveat describes current 2025 sources as "future" improvements — this misframes existing documentation as speculation)
- Overclaim vendor consensus (RISK: Theme 6 convergence language overstates agreement given Palantir's documented divergence)

**Step 3: Assumption Map**

| # | Assumption | Type | Confidence | Validation |
|---|-----------|------|------------|-----------|
| A1 | 40 search queries provide adequate coverage of the topic landscape | Process | Medium | Partially validated — saturation disclosure added; no saturation test performed |
| A2 | English-language sources adequately represent the global practitioner consensus | External | Low | Disclosed as limitation; impact not assessed |
| A3 | Blog/article publication format captures representative practitioner views | External | Medium | Addressed implicitly through evidence tier system |
| A4 | URL links will remain accessible for readers of the downstream synthesis | Technical | Medium | Access date now disclosed (2026-02-27); no archived copies |
| A5 | Evidence tier classification is stable and unambiguous | Process | High | Well-defined with examples; sub-tier distinctions documented |
| A6 | The "effectiveness gap may narrow with future model capability improvements" framing is temporally accurate | Temporal | Low | **INVALID**: Sources 4 and 5 document this in 2025 current models, not future models |

**Step 4: Stress-Test**

| ID | Assumption | Inversion | Severity | Dimension |
|----|-----------|-----------|----------|-----------|
| IN-001-iter4 | A6: "Future" framing temporally inaccurate | A practitioner citing L0 tells their team "the survey says this narrowing MIGHT happen in future models" — but it's already documented in 2025 GPT-4.1/GPT-5 guides. Misguidance about current state. | Major | Accuracy |
| IN-002-iter4 | A3: Blog/article representativeness | If practitioner communities that favor negative prompting are less likely to publish blog posts about it (publication bias toward "here's what broke and how I fixed it"), the survey systematically over-captures failure cases | Minor | Methodological Rigor |
| IN-003-iter4 | Theme 6 convergence accuracy | If someone cites "all major vendors converge" without noting Palantir, the document actively misleads about the degree of cross-vendor agreement | Minor | Internal Consistency |
| IN-004-iter4 | A1: Coverage adequacy | An adversarial researcher with queries specifically targeting "negative prompting success stories" or "when negative prompting works" may find a different balance of evidence | Minor | Methodological Rigor |

---

### S-011: Chain-of-Verification

**Step 1: Extract Claims**

| ID | Claim | Type | Source |
|----|-------|------|--------|
| CL-001 | "31 core sources cataloged (1 adjacent source documented separately)" | Quoted value | Document header |
| CL-002 | "Empirical evidence constitutes 23% (7 of 31 core sources)" | Quoted value | L0 Evidence Landscape |
| CL-003 | "Vendor Recommendation: 29%" (9 of 31) | Quoted value | Evidence Tier Distribution |
| CL-004 | "Practitioner Anecdote: 48%" (15 of 31) | Quoted value | Evidence Tier Distribution |
| CL-005 | Source Types: "Blog post / article: 17, Vendor documentation: 8, Framework documentation: 3, Community discussion/forum: 2, Community guide: 1" | Quoted value | Source Types table |
| CL-006 | "Sources 4 and 5 (OpenAI GPT-4.1 and GPT-5 guides) document that newer model generations follow instructions more literally, including negative instructions" | Behavioral claim | L0 model-gen caveat |
| CL-007 | "The effectiveness gap between positive and negative framing may narrow with future model capability improvements" | Temporal claim | L0 model-gen caveat |
| CL-008 | Theme 6 Cross-Vendor Convergence: "all major vendors converge on the same recommendation" | Convergence claim | L2 Theme 6 |
| CL-009 | Pattern 4 heading: "Model-Specific Compliance Evolution (Sources 4, 5 -- analyst synthesis)" | Label claim | L2 Theme 6 |
| CL-010 | Survey Limitations: "single researcher executing all 40 search queries in a single session (2026-02-27)" | Process claim | Methodology |

**Step 3: Independent Verification**

**CL-001:** Count source table rows excluding row 26: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,27,28,29,30,31,32 = 31. Row 26 in Adjacent Sources section. VERIFIED.

**CL-002:** 7/31 = 0.2258 ≈ 23%. Sources: 14, 20, 21, 18, 12, 13, 30 = 7. VERIFIED.

**CL-003:** 9/31 = 0.2903 ≈ 29%. Sources: 1,3,4,5,6,7,15,19,27 = 9. VERIFIED.

**CL-004:** 15/31 = 0.4839 ≈ 48%. Sources: 2,8,9,10,11,16,17,22,23,24,25,28,29,31,32 = 15. VERIFIED.

**CL-005:** Source Types table verification:
- Vendor documentation: Sources 1,3,4,5,6,7,15,19 = 8 (Source 27 is Framework documentation). VERIFIED = 8.
- Blog post / article: Sources 8,9,10,11,12,13,14,16,17,20,22,23,24,25,28,29,30 = 17 (includes Source 20/QED42 which is typed "Blog post / article" in Source Table). VERIFIED = 17.
- Framework documentation: Sources 21,27,31 = 3. VERIFIED = 3.
- Community discussion / forum: Sources 18,32 = 2. VERIFIED = 2.
- Community guide: Source 2 = 1. VERIFIED = 1.
- Total: 8+17+3+2+1 = 31. VERIFIED. ✓

*Note: The previous iteration's finding about Source 2 overcounting (CV-001-iter3) was incorrect. Source 20 (QED42) is a blog, making the blog count = 17 valid while Source 2 remains a distinct Community guide. No discrepancy exists.*

**CL-006:** Source 4 (GPT-4.1 Prompting Guide, OpenAI 2025) Key Finding: "GPT-4.1 follows instructions 'more closely and more literally' than predecessors." Source 5 (GPT-5 Prompting Guide, OpenAI 2025) Key Finding: "Contradictory instructions waste reasoning tokens. Positive framing of constraints preferred over accumulated prohibitions." Verification of the claim that Sources 4-5 document "newer model generations follow instructions more literally, including negative instructions": VERIFIED. Source 4 explicitly states literal instruction-following. Source 5 shows both improved compliance and improved consequence sensitivity.

**CL-007:** Claim: "The effectiveness gap between positive and negative framing may narrow with **future** model capability improvements."
Verification: Sources 4 and 5 — both published in 2025 — document GPT-4.1 and GPT-5 as *current* models where this narrowing is already observed. The word "future" in CL-007 is NOT supported by the referenced sources. This is a **temporal accuracy error** — the L0 caveat frames an already-documented current phenomenon as a future possibility.

**DISCREPANCY DETECTED — CL-007:** The word "future" in the L0 model-generation caveat is factually incorrect. Sources 4 and 5, cited inline as the basis for this caveat, are 2025 documents about current model generations (GPT-4.1, GPT-5). The gap has already narrowed (or reversed) for these models, not merely "may narrow" in the future.

**CL-008:** Theme 6 Cross-Vendor Convergence: "all major vendors converge on the same recommendation: positive framing preferred, negatives for narrow safety boundaries only, examples trump instructions, and programmatic enforcement for critical constraints."
Verification: Theme 1 Palantir subsection states Palantir "treats negatives as one tool among many rather than as categorically inferior" and "takes a more balanced approach, explicitly supporting both positive constraints...and negative examples."
**DISCREPANCY DETECTED — CL-008:** The convergence claim "all major vendors" is contradicted by the documented Palantir exception. Palantir does NOT share the "positive framing preferred" recommendation per the survey's own Theme 1 analysis.

**CL-009:** Pattern 4 heading: "Model-Specific Compliance Evolution (Sources 4, 5 -- analyst synthesis)". VERIFIED — the label is present. Consistent with Patterns 1-3 analyst-inference labeling. ✓

**CL-010:** Survey Limitations: "single researcher executing all 40 search queries in a single session (2026-02-27)". VERIFIED — this statement is present in the Survey Limitations paragraph. ✓

**Step 4: Consistency Check**

| ID | Claim | Result | Severity |
|----|-------|--------|----------|
| CV-001-iter4 | Source Types table total: 8+17+3+2+1=31 | VERIFIED — correct. Prior iter3 discrepancy was a counting error by the adversary (Source 20 omitted from blog count). | N/A |
| CV-002-iter4 | L0 caveat: "may narrow with future model capability improvements" | TEMPORAL ACCURACY ERROR: Sources 4-5 are 2025 current models, not future models. The narrowing is already documented. | Major |
| CV-003-iter4 | Theme 6: "all major vendors converge" | INTERNAL INCONSISTENCY: Palantir's documented balanced approach contradicts this convergence claim | Minor |
| CV-004-iter4 | Source count 31 core + 1 adjacent | VERIFIED | N/A |
| CV-005-iter4 | Pattern 4 analyst-synthesis label | VERIFIED | N/A |
| CV-006-iter4 | Survey Limitations single-researcher disclosure | VERIFIED | N/A |

**Chain-of-Verification Summary:** 8 of 10 claims VERIFIED. 2 discrepancies:
- CV-002-iter4 (Major): Temporal accuracy error in L0 model-gen caveat — "future" should be "current/recent"
- CV-003-iter4 (Minor): Theme 6 convergence claim overstates vendor agreement given documented Palantir exception

---

### S-001: Red Team Analysis

**H-16 Compliance:** S-003 executed prior. Proceeding.

**Step 1: Define Threat Actor**

Profile: "A motivated practitioner who applied the survey's primary L0 recommendation to a GPT-5 production system in Q3 2026. They experienced unexpected behavior — the negative instruction 'DO NOT hallucinate' was followed more literally than expected, causing the model to refuse to generate content when it was uncertain rather than expressing uncertainty inline. Reading the survey's L0 caveat more carefully, they discover it says this might happen with 'future' models — but the GPT-5 guide was published in 2025. They conclude the survey provided inaccurate temporal guidance about currently-deployed models."

**Step 2: Enumerate Attack Vectors**

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-----------|
| RT-001-iter4 | Temporal accuracy attack: L0 caveat says "future model capability improvements" but Sources 4-5 are 2025 current models — reviewer demonstrates the survey misinformed practitioners about currently-deployed GPT-4.1/GPT-5 behavior | Accuracy | High | Major | P1 | Missing | Accuracy |
| RT-002-iter4 | Convergence overclaim attack: reviewer demonstrates Theme 6 "all major vendors converge" claim is contradicted by the survey's own Theme 1 Palantir analysis | Ambiguity | Medium | Minor | P2 | Missing | Internal Consistency |
| RT-003-iter4 | Source 30 inflation attack: reviewer argues the 23% empirical figure misleads because Source 30 measures emotional sentiment, not instructional negation; the "strict" empirical percentage is 6/31 = 19.4% (excluding Source 30) | Boundary | Medium | Minor | P2 | Partial (scope note present per-source but not in aggregate statistics) | Evidence Quality |
| RT-004-iter4 | Publication bias attack: the survey's 40 queries were all framed around failure cases and best practices for avoiding negatives; an adversarial researcher with queries framed around "when negative prompting works" or "negative prompting success" would likely find different sources | Process | Medium | Minor | P2 | Partial (survey limitations disclosed) | Methodological Rigor |
| RT-005-iter4 | URL decay: 9 months after publication (November 2026), a fraction of the 31 URLs may be dead; the survey has access dates but no archived copies | Degradation | Medium | Minor | P3 | Partial (access date disclosed) | Traceability |

**Step 3: Defense Gap Assessment**

- RT-001: Missing defense. The "future" language in L0 creates a false impression about the temporal status of the narrowing-effectiveness-gap finding. Sources 4 and 5 are dated 2025.
- RT-002: Missing defense. Theme 6 Cross-Vendor Convergence does not qualify Palantir, despite Theme 1 correctly documenting Palantir's balanced approach.
- RT-003: Partial defense. Source 30 scope note is present per-source and in L2 Theme 2, but the aggregate "23%" figure does not reflect the scope limitation.
- RT-004: Partial defense. Survey Limitations now acknowledges single-researcher and English-only limitations, but query framing bias is not explicitly called out.
- RT-005: Partial defense. Access date disclosed. No archived copies — acknowledged as limitation.

**Step 4: Countermeasures**

| ID | Countermeasure |
|----|---------------|
| RT-001 | Correct L0 caveat: replace "may narrow with future model capability improvements" with language that acknowledges this narrowing has ALREADY been documented in current 2025 models (GPT-4.1, GPT-5). Suggested: "GPT-4.1 and GPT-5 (2025) already demonstrate improved negative instruction compliance; this survey's primary finding reflects earlier model generations and may not fully apply to current frontier models." |
| RT-002 | Qualify Theme 6 convergence claim: "Three of four major vendors converge..." or "Major LLM vendors (with the exception of Palantir's balanced approach) converge..." |
| RT-003 | Add note to Evidence Landscape Assessment: "If Source 30 (sentiment study measuring emotional tone, not instruction syntax) is excluded from the empirical count, the percentage addressing instructional negation directly is 6/31 = 19%." |
| RT-004 | Add query framing bias disclosure to Survey Limitations: "Search queries were primarily framed around failure cases and best practices; queries specifically targeting successful negative prompting applications may yield additional contrary evidence." |

---

### S-010: Self-Refine

**Step 1: Objectivity Check**

This is the fourth adversarial iteration. The prior three iterations identified and addressed the following convergent gaps:
- Iteration 1: Evidence tier definitions, source count correction, Pink Elephant caveats, gaps list expansion, model-gen confound warning
- Iteration 2: Sub-tier labels, Source 26 exclusion from core count, analyst-inference labels (Patterns 1-3), U-shaped recovery caveats, Bsharat et al. attribution
- Iteration 3: Survey Limitations paragraph (single-researcher, saturation, URL access dates), L0 model-gen caveat, Pattern 4 analyst-synthesis label

Proceeding with leniency-bias counteraction active. Focus on current document quality, not improvement trajectory.

**Step 2: Systematic Self-Critique**

**Completeness (0.20):** All five document sections present and populated. L0 has 5 bullets, Evidence Landscape Assessment, Gaps section (8 items). L1 has full tier definitions with 5 sub-categories, 31-source catalog, adjacent sources, distribution table, source types table. L2 has 6 themes with cross-cutting synthesis. Cross-references has 4 items including revision triggers. Methodology has search queries, date range, selection criteria, survey limitations, exclusion decisions.

Key issue: The L0 model-generation caveat (added Revision 3) uses "future" framing for a phenomenon already documented in current 2025 sources. This is a minor accuracy issue in L0 completeness — the caveat is present and directionally correct, but the temporal framing may mislead.

**Internal Consistency (0.20):** Percentages (29%/23%/48%) verified arithmetically correct. All Theme 6 Patterns 1-4 carry analyst-inference/synthesis labels. U-shaped recovery caveats present in both locations. Bsharat et al. attribution consistent. Source Types counts verified (8+17+3+2+1=31).

Key issue: Theme 6 Cross-Vendor Convergence states "all major vendors converge" — but Theme 1 documents Palantir as explicitly taking a balanced, non-convergent approach. This is a minor internal inconsistency between sections.

**Methodological Rigor (0.20):** 40 search queries listed. Selection criteria defined. Exclusion decisions documented. Survey Limitations paragraph now present with: single-researcher disclosure, no saturation criterion acknowledgment, URL access date, English-only scope. These are the four standard methodological disclosures.

Remaining gap: Query framing bias is not disclosed (all 40 queries were framed around negative prompting problems/best practices; no "when negative prompting works" queries). This is a less critical but real omission.

**Evidence Quality (0.15):** Per-source limitations documented throughout. Analyst-inference labels on Patterns 1-4. Bsharat et al. currency limitation noted per-source. Source 30 scope note clear. Source 18 competition-vs-peer-review caveat present. Pink Elephant analogy labeled as hypothesis.

Remaining gap: Source 30 (sentiment study) counted in the 23% empirical figure without a parallel note in the aggregate statistics that this source measures a distinct phenomenon. The per-source note is there; the aggregate-level disambiguation is not.

**Actionability (0.15):** 8 specific gaps identified. 6 follow-up research areas in cross-references. Revision triggers defined. L0 provides clear actionable recommendations. Good for a research survey.

Minor issue: The model-generation caveat in L0 describes the narrowing as potentially future, when it has already been documented for 2025 models. Practitioners using GPT-5 or Claude 4 now may receive guidance that underestimates how much model behavior has already shifted.

**Traceability (0.10):** Source IDs cited throughout. Navigation table with anchor links present. Footer revision notes comprehensive. URL access date now documented. No archived copies (acknowledged as limitation). Pattern 4 analyst-synthesis label added.

Remaining: Source 28 cited in Theme 3 System Prompt Architecture section but its contribution to that specific pattern is not explicitly explained (Source 28 is primarily about context compaction, not system prompt architecture patterns).

**Step 3: Findings**

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-iter4 | L0 model-gen caveat uses "future" temporal framing for behavior already documented in 2025 Sources 4-5 | Major | L0: "may narrow with future model capability improvements" — but Sources 4 (GPT-4.1, 2025) and 5 (GPT-5, 2025) are current, not future | Accuracy / Completeness |
| SR-002-iter4 | Theme 6 "all major vendors converge" contradicts Theme 1's accurate Palantir exception documentation | Minor | Theme 6 convergence claim vs. Theme 1 Palantir: "treats negatives as one tool among many" | Internal Consistency |
| SR-003-iter4 | Source 30 (sentiment study) included in 23% empirical count but measures emotional tone, not instruction syntax | Minor | Evidence Landscape Assessment claims 23% empirical; Source 30 scope note present per-source but not reflected in aggregate statistic | Evidence Quality |
| SR-004-iter4 | Query framing bias not disclosed in Survey Limitations | Minor | Survey Limitations discloses single-researcher, saturation, URL dates, English-only — but not query-framing bias toward failure cases | Methodological Rigor |

---

## Part II: S-014 LLM-as-Judge Scoring

### Step 1: Load Deliverable and Context

Deliverable: Industry survey on negative prompting, 31 core sources, Revision 3. C4 criticality. Prior S-014 scores: Iter 1 = 0.770, Iter 2 = 0.907, Iter 3 = 0.900. Target: >= 0.95. Strict scoring active — scoring absolute quality, not improvement trajectory.

### Step 2: Score Each Dimension Independently

---

#### Completeness (weight 0.20)

Rubric criteria: All major sections present; all required subsections populated; no gaps in coverage that would leave readers without critical information; L0 summary accurately represents L1/L2 content.

**Evidence for:**
- All 5 document sections present with full content (L0, L1, L2, Cross-References, Methodology)
- L1 Source Catalog includes tier definitions (5 sub-categories with epistemic weighting), 31-source table, adjacent sources, tier distribution, source types table
- L2 covers 6 themes with detailed sub-analysis and cross-cutting synthesis sections
- Gaps section explicitly identifies 8 unaddressed areas
- Cross-references addresses model-generation confound, revision triggers, and 6 follow-up research areas
- Survey Limitations sub-section (added Revision 3) discloses 5 distinct methodological constraints

**Evidence against:**
- L0 model-generation caveat describes the narrowing effectiveness gap as something that "may narrow with future model capability improvements" — but Sources 4 and 5 are 2025 documents about *current* models. A reader consuming L0 may believe this is speculative/future when it is documented in currently-deployed GPT-4.1 and GPT-5. The caveat is present but temporally inaccurate, leaving L0 readers with a misleading picture of current state.
- Survey Limitations paragraph is dense (5 limitations in one paragraph) — reduces scannability of the disclosures
- Query framing bias not disclosed (all queries focused on failure cases; no queries specifically targeting successful negative prompting)

**Assessment:** The document is highly complete. The L0 model-generation caveat is now present (addressing the primary prior gap), but its temporal framing introduces a new accuracy issue. The Survey Limitations paragraph addresses all major methodological concerns. Strict rubric assessment: the "future" framing error in L0 is a meaningful accuracy gap — a practitioner reading L0 receives a directionally misleading temporal signal about currently-deployed models.

Score: **0.91** (Strong — near-complete; reduced by the L0 temporal accuracy error in the model-gen caveat and query framing disclosure gap)

---

#### Internal Consistency (weight 0.20)

Rubric criteria: No contradictions between sections; claims are internally self-consistent; evidence characterizations do not conflict across different document locations.

**Evidence for:**
- Percentages (29%/23%/48%) verified arithmetically correct (Chain-of-Verification CL-001 through CL-005 all VERIFIED)
- Source tier classifications consistent throughout (all 31 sources match their tier in both Source Table and Distribution table)
- Pink Elephant caveat consistently labeled as hypothesis/analogy (Theme 2, Theme 5, L0)
- Bsharat et al. attribution consistent at all occurrences
- U-shaped recovery caveat present in both Theme 2 and Theme 5 Mechanism 2
- All Theme 6 Patterns 1-4 carry analyst-inference/synthesis labels
- Source Types table verified correct (8+17+3+2+1=31, with Source 20 as blog and Source 2 as community guide)

**Evidence against:**
- Theme 6 Cross-Vendor Convergence: "all major vendors converge on the same recommendation: positive framing preferred, negatives for narrow safety boundaries only" — but Theme 1 explicitly documents Palantir as the exception ("treats negatives as one tool among many rather than as categorically inferior"). The cross-section inconsistency is clear and verifiable.
- L0 caveat's "future" framing conflicts with the cross-references section's "Model-Generation Confound" which presents Sources 4 and 5 as documenting current behavior, not future behavior.

**Assessment:** High internal consistency overall. Two verifiable inconsistencies exist: (1) Theme 6 convergence claim vs. Theme 1 Palantir exception, and (2) L0 "future" framing vs. cross-references current behavior documentation. Both are minor-to-moderate in isolation but represent genuine cross-section contradictions. Strict rubric assessment: these are real inconsistencies, not cosmetic.

Score: **0.88** (Strong-to-Acceptable — high consistency on quantitative claims and evidence characterizations; two verifiable cross-section inconsistencies that a careful reader will notice)

---

#### Methodological Rigor (weight 0.20)

Rubric criteria: Research methodology is appropriate to the task; selection criteria are defined and applied; limitations are acknowledged; procedures are transparent and reproducible.

**Evidence for:**
- 40 search queries explicitly listed with specific query strings
- Selection criteria defined (5 criteria with clear rationale)
- Exclusion decisions documented with rationale table (11 exclusions with reasons)
- Evidence tier system with 5 sub-categories and epistemic weighting
- Per-source limitations documented throughout L2
- Survey Limitations paragraph (Revision 3) discloses: single-researcher, single-session, no saturation criterion, URL access dates, English-only scope

**Evidence against:**
- Query framing bias not disclosed: all 40 queries were framed around negative prompting failures, limitations, and best practices for avoiding negatives. No queries specifically targeted "negative prompting success stories," "when negative prompting works," or "negative prompting advantages." This is a systematic search bias that could skew the evidence balance.
- Survey Limitations paragraph is structurally a single dense paragraph rather than a bulleted list, reducing auditability of the individual disclosures.

**Assessment:** The methodology section has improved substantially through three revision cycles. The addition of the Survey Limitations paragraph addresses the primary prior gaps (single-researcher, saturation, URL access dates). The remaining gap — query framing bias — is a genuine methodological limitation that is standard to disclose in systematic landscape searches. It is less severe than the prior gaps because the survey's evidence tier system and per-source limitations already provide some protection against overconfidence in the findings.

Score: **0.91** (Strong — comprehensive survey methodology documentation; reduced by undisclosed query framing bias and paragraph density of limitations disclosure)

*Note: This is a substantial improvement from the Iter 3 score of 0.87 due to the addition of the Survey Limitations paragraph addressing the three primary prior gaps.*

---

#### Evidence Quality (weight 0.15)

Rubric criteria: Claims are backed by specific evidence; evidence characterizations are accurate; source limitations are disclosed; quantitative claims are properly attributed.

**Evidence for:**
- Per-source limitations documented for every empirical source
- Analyst-inference labels applied to all synthesized patterns (Patterns 1-4)
- Bsharat et al. attribution corrected throughout (the 55%/66.7% figures attributed to Bsharat et al., not PromptHub)
- Source 30 scope note present and accurate at source level and in Theme 2 analysis
- Source 18 competition-vs-peer-review caveat present in both L1 and L2
- Source 12 methodology-not-disclosed caveat present
- Pink Elephant analogy explicitly labeled as hypothesis (not mechanistic evidence)
- Sub-tier note in Evidence Tier Distribution accurately characterizes epistemic weight differences
- Source 13 limitation on Bsharat et al. currency noted per-source (2023 figures)

**Evidence against:**
- Source 30 (sentiment study) is counted in the "23% empirical" figure in the Evidence Landscape Assessment, but this source measures emotional tone/sentiment, not instructional negation syntax. The per-source scope note is present, but the aggregate 23% figure implicitly includes this methodologically distinct source without a corresponding note at the aggregate level.
- The Bsharat et al. currency limitation (2023 GPT-4 data) is noted per-source (Source 13) but the L0 summary ("strongest quantitative finding...reporting 55% improvement and 66.7% correctness increase") does not note that these figures are 2023/GPT-4 specific.

**Assessment:** Evidence quality is strong — the per-source documentation is comprehensive and the analyst-inference labeling is thorough. Two minor gaps: Source 30 aggregate-level disambiguation and Bsharat et al. currency note in L0 summary.

Score: **0.93** (Strong — comprehensive source-level limitation documentation; minor gaps on Source 30 aggregate treatment and Bsharat et al. L0 currency note)

---

#### Actionability (weight 0.15)

Rubric criteria: For a research survey, actionability means practitioners can act on the findings; gaps section identifies clear next steps; recommendations are specific and applicable.

**Evidence for:**
- 8 specific gaps identified in the gaps section with clear framing
- Cross-references section identifies 6 specific follow-up research areas
- Revision triggers defined (model generation, A/B study, 6-month elapsed)
- L0 provides clear, actionable recommendations: use positive framing; reserve negatives for safety; use programmatic enforcement
- Theme analyses consistently link findings to actionable guidance
- Survey Limitations discloses scope, helping practitioners understand when findings do/don't apply

**Evidence against:**
- The primary actionability concern: L0's model-generation caveat says the effectiveness gap "may narrow with future model capability improvements" — a practitioner using GPT-5 (2025) or Claude 4 (2025) NOW receives guidance that under-quantifies how much model behavior has already shifted toward more literal instruction compliance. This reduces the survey's actionability for current frontier model users.

**Assessment:** Actionability is strong for a research survey. The gaps section, follow-up research list, and revision triggers are well-constructed. The model-generation caveat accuracy issue reduces actionability for practitioners on current frontier models.

Score: **0.91** (Strong — comprehensive gaps section and actionable guidance; slight reduction for model-generation caveat temporal inaccuracy affecting current-model practitioners)

---

#### Traceability (weight 0.10)

Rubric criteria: Sources are cited; claims trace to sources; source IDs are consistent; navigation table present; URL access dates documented.

**Evidence for:**
- Navigation table with anchor links present (H-23/H-24 compliant)
- Source numbers cited throughout L2 analysis
- All 31 sources in L1 table with URLs
- Adjacent Sources section explicitly documents Source 26 exclusion with rationale
- Footer revision notes trace every change to specific prior findings
- URL access date now documented: "All source URLs were accessed 2026-02-27"
- Analyst-inference labels on Patterns 1-4 improve traceability of synthesis decisions
- Exclusion decisions table documents 11 excluded sources with rationale

**Evidence against:**
- No archived copies of the 31 web sources (acknowledged as limitation but represents a real traceability risk)
- Source 28 cited in Theme 3 "System Prompt Architecture" section but the relevance of Source 28 (about context compaction during conversations) to the system prompt architecture discussion is not explicitly bridged in the text

**Assessment:** Traceability is strong. The URL access date addition (Revision 3) addresses the primary prior gap. No major traceability deficits remain. The lack of archived copies is a known, disclosed limitation.

Score: **0.94** (Strong — all primary traceability components present including URL access dates; minor reduction for no archived copies and Source 28 implicit citation)

---

### Step 3: Compute Weighted Composite

```
Dimension         | Weight | Score | Weighted
------------------|--------|-------|----------
Completeness      | 0.20   | 0.91  | 0.182
Internal Consist. | 0.20   | 0.88  | 0.176
Method. Rigor     | 0.20   | 0.91  | 0.182
Evidence Quality  | 0.15   | 0.93  | 0.1395
Actionability     | 0.15   | 0.91  | 0.1365
Traceability      | 0.10   | 0.94  | 0.094
                  |        |       |
Composite         |        |       | 0.910
```

Composite = (0.91 × 0.20) + (0.88 × 0.20) + (0.91 × 0.20) + (0.93 × 0.15) + (0.91 × 0.15) + (0.94 × 0.10)
          = 0.182 + 0.176 + 0.182 + 0.1395 + 0.1365 + 0.094
          = **0.910**

### Step 4: Determine Verdict

Composite 0.910 is in the 0.85-0.91 REVISE band. The C4 target threshold (>= 0.95) is not met. H-13 threshold (>= 0.92) is also not met.

**Verdict: REVISE**

### Step 5: Improvement Recommendations

| Priority | Dimension | Current Score | Gap to 0.95 | Recommendation |
|----------|-----------|---------------|-------------|----------------|
| P1 | Internal Consistency | 0.88 | 0.07+ | Fix Theme 6 convergence claim ("all major vendors") to acknowledge Palantir exception; correct L0 "future" framing to reflect that Sources 4-5 document *current* 2025 model behavior, not future |
| P1 | Completeness | 0.91 | 0.04+ | Correct L0 temporal framing: "may narrow with future model capability improvements" → language acknowledging GPT-4.1 and GPT-5 (2025) already demonstrate improved compliance |
| P2 | Methodological Rigor | 0.91 | 0.04+ | Add query framing bias disclosure to Survey Limitations: queries were framed toward failure cases; queries specifically targeting successful negative prompting applications were not executed |
| P2 | Evidence Quality | 0.93 | 0.02+ | Add aggregate-level note in Evidence Landscape Assessment acknowledging Source 30 measures emotional sentiment; "strict instructional negation" empirical count is 6/31 = 19% |
| P3 | Actionability | 0.91 | 0.04+ | Follows from P1 fix: correcting L0 temporal framing resolves actionability gap for current frontier model users |

### Step 6: Leniency Bias Check

- Internal Consistency 0.88: Two verifiable cross-section inconsistencies (Theme 6 convergence vs. Theme 1 Palantir; L0 "future" vs. cross-references "current"). Strict rubric application. 0.88 is not lenient — these are real contradictions.
- Completeness 0.91: The L0 model-generation caveat is present (addressing prior gap), but its temporal framing is inaccurate. 0.91 is appropriate — the presence of the caveat prevents a lower score, but its inaccuracy prevents a higher one.
- Methodological Rigor 0.91: Major prior gaps addressed (saturation, single-researcher, URL access dates). Query framing bias undisclosed is a real but secondary gap. 0.91 reflects genuine improvement with a remaining gap.
- Evidence Quality 0.93: Strong per-source documentation. Minor aggregate-level Source 30 issue. 0.93 is appropriate.
- Actionability 0.91: Strong gaps section. Reduced by model-gen temporal framing issue. 0.91 is appropriate.
- Traceability 0.94: URL access dates added; full source citation present. 0.94 reflects near-complete traceability. Appropriate.

**Anti-leniency check:** Temptation to inflate scores because the document has been revised three times. COUNTERACTED. Scores reflect literal rubric application against the current document's absolute quality, not its improvement trajectory. The composite of 0.910 accurately reflects a document that has resolved its major prior gaps but introduced a new accuracy error (L0 temporal framing) and retains two minor gaps (query framing bias, Theme 6 convergence overstatement).

**Comparison with Iter 3 score (0.900):**
- Methodological Rigor: 0.87 → 0.91 (+0.04) — Survey Limitations paragraph added
- Traceability: 0.89 → 0.94 (+0.05) — URL access dates added
- Internal Consistency: 0.90 → 0.88 (-0.02) — L0 "future" framing creates new cross-section inconsistency
- Completeness: 0.90 → 0.91 (+0.01) — Model-gen caveat added (but temporal framing slightly inaccurate)
- Overall: 0.900 → 0.910 (+0.010) — Net improvement, but below 0.95 threshold

### Step 7: Score Report

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.91 | 0.182 |
| Internal Consistency | 0.20 | 0.88 | 0.176 |
| Methodological Rigor | 0.20 | 0.91 | 0.182 |
| Evidence Quality | 0.15 | 0.93 | 0.1395 |
| Actionability | 0.15 | 0.91 | 0.1365 |
| Traceability | 0.10 | 0.94 | 0.094 |
| **Composite** | | | **0.910** |

**Verdict: REVISE (0.85-0.91 band) — C4 target 0.95 not met**

---

## Part III: Consolidated Findings

### Findings Summary Table

| ID | Strategy | Severity | Finding | Section | Priority |
|----|---------|---------|---------|---------|---------|
| DA-001-iter4 | S-002 | Major | L0 model-gen caveat uses "future" framing for behavior documented in current 2025 Sources 4-5 | L0 | P1 |
| CV-002-iter4 | S-011 | Major | "may narrow with future model capability improvements" — Sources 4-5 are 2025 current models | L0 | P1 |
| FM-001-iter4 | S-012 | Major (RPN=210) | L0 temporal framing inaccuracy — "future" vs. current 2025 documented behavior | L0 | P1 |
| SR-001-iter4 | S-010 | Major | L0 "future" framing for phenomenon already documented in 2025 Sources | L0 | P1 |
| RT-001-iter4 | S-001 | Major | Temporal accuracy attack — L0 caveat misinforms about currently-deployed model behavior | L0 | P1 |
| IN-001-iter4 | S-013 | Major | Assumption A6 invalid — "future" framing for current 2025 model behavior | L0 | P1 |
| PM-001-iter4 | S-004 | Major | L0 caveat temporal framing creates false confidence for current frontier model users | L0 | P1 |
| DA-004-iter4 | S-002 | Minor | Theme 6 "all major vendors converge" contradicts Theme 1 Palantir exception | L2 Theme 6 | P2 |
| CV-003-iter4 | S-011 | Minor | "all major vendors converge" — Palantir documented as non-convergent in same document | L2 Theme 6 | P2 |
| FM-003-iter4 | S-012 | Minor (RPN=100) | Theme 6 convergence claim conflicts with Theme 1 Palantir analysis | L2 Theme 6 | P2 |
| SR-002-iter4 | S-010 | Minor | Theme 6 "all major vendors converge" contradicts documented Palantir exception | L2 Theme 6 | P2 |
| RT-002-iter4 | S-001 | Minor | Convergence overclaim — Palantir exception not reflected in Theme 6 | L2 Theme 6 | P2 |
| DA-002-iter4 | S-002 | Minor | Source 30 (sentiment study) counted in 23% empirical figure measuring a distinct phenomenon | L0, L1 | P2 |
| RT-003-iter4 | S-001 | Minor | Source 30 in 23% aggregate figure conflates emotional sentiment with instructional negation | Evidence Landscape | P2 |
| SR-003-iter4 | S-010 | Minor | Source 30 in 23% empirical aggregate without aggregate-level disambiguation | Evidence Landscape | P2 |
| SR-004-iter4 | S-010 | Minor | Query framing bias not disclosed in Survey Limitations | Methodology | P2 |
| RT-004-iter4 | S-001 | Minor | Query framing bias not disclosed | Methodology | P2 |
| IN-002-iter4 | S-013 | Minor | Publication bias toward failure cases not disclosed | Methodology | P2 |
| DA-003-iter4 | S-002 | Minor | English-language limitation disclosed but impact not assessed | Methodology | P2 |
| FM-002-iter4 | S-012 | Minor (RPN=120) | Source 30 aggregate-level disambiguation missing | L1 Distribution | P2 |
| FM-004-iter4 | S-012 | Minor (RPN=72) | Survey Limitations paragraph density reduces scannability | Methodology | P3 |
| FM-005-iter4 | S-012 | Minor (RPN=60) | Theme 3 Source 28 citation without explicit bridge to system prompt architecture | L2 Theme 3 | P3 |
| SM-001-iter4 | S-003 | Minor | Cross-vendor synthesis table lacks evidence tier column | L2 Theme 1 | P3 |
| SM-003-iter4 | S-003 | Minor | L0 caveat language characterizes "narrowing" as future when already documented | L0 | P1 |
| IN-003-iter4 | S-013 | Minor | Theme 6 convergence accuracy — Palantir non-convergent | L2 Theme 6 | P2 |

---

## Part IV: Convergent Gap Analysis

Cross-strategy findings converge on **3 distinct actionable gaps**:

---

### Gap A: L0 Model-Generation Caveat Temporal Accuracy (P1 — affects Internal Consistency, Completeness, Actionability)

**Converged findings:** DA-001-iter4, CV-002-iter4, FM-001-iter4, SR-001-iter4, RT-001-iter4, IN-001-iter4, PM-001-iter4, SM-003-iter4

**Root cause:** Revision 3 correctly added the model-generation caveat to L0 but used "future" framing that is factually inaccurate. The L0 bullet currently reads: "The effectiveness gap between positive and negative framing **may narrow with future model capability improvements**." However, Sources 4 (GPT-4.1, 2025) and 5 (GPT-5, 2025) are current documents that already demonstrate improved negative instruction compliance in currently-deployed models. "Future" misdescribes the temporal status of this evidence.

**Impact:** A practitioner reading L0 in 2026 receives the message that this narrowing is speculative/future. In reality, it is documented in 2025 current models that are in widespread production use. This temporal inaccuracy could lead to misapplication of the survey's primary recommendation for current frontier model users.

**Corrective action:** Replace the temporal framing in the L0 model-generation caveat:
- Current: "The effectiveness gap between positive and negative framing may narrow with future model capability improvements."
- Proposed: "This recommendation reflects the balance of evidence across 2023-2026 sources. GPT-4.1 and GPT-5 (Sources 4-5, OpenAI 2025) already document that newer model generations follow instructions more literally, including negative instructions, and their unintended consequences are also more pronounced — suggesting this survey's primary finding may not fully apply to current frontier models."

*(Note: The preceding sentences in the L0 bullet — "Sources 4 and 5 (OpenAI GPT-4.1 and GPT-5 guides) document that newer model generations follow instructions more literally, including negative instructions, and their unintended consequences are also more pronounced" — are actually already present in the current L0 bullet. The specific fix is the last sentence: remove "may narrow with future model capability improvements" and replace with something that accurately characterizes these as current, not future, observations.)*

**Acceptance criterion:** L0 model-generation caveat does not use "future" framing for behavior documented in 2025 current sources. The caveat explicitly acknowledges that GPT-4.1 and GPT-5 (currently deployed) already show this behavior, not merely that it might occur in future models.

---

### Gap B: Theme 6 Cross-Vendor Convergence Overstatement (P2 — affects Internal Consistency)

**Converged findings:** DA-004-iter4, CV-003-iter4, FM-003-iter4, SR-002-iter4, RT-002-iter4, IN-003-iter4

**Root cause:** Theme 6 Cross-Vendor Convergence states "all major vendors converge on the same recommendation: positive framing preferred, negatives for narrow safety boundaries only." However, Theme 1 correctly and explicitly documents Palantir as the exception: "treats negatives as one tool among many rather than as categorically inferior." This creates a verifiable cross-section inconsistency within the same document.

**Impact:** A reader of the synthesis may cite "all major vendors converge" without the Palantir qualification, overstating cross-vendor consensus. This is a factual inaccuracy about the degree of agreement, even if the underlying trend is real.

**Corrective action:** Qualify the convergence claim in Theme 6 to reflect the documented exception:
- Current: "Despite different model architectures, all major vendors converge on the same recommendation..."
- Proposed: "Despite different model architectures, three of four major vendors (Anthropic, OpenAI, Google) converge on the same recommendation..., while Palantir takes a more balanced approach (see Theme 1: Palantir). This three-of-four convergence suggests the recommendation is broadly applicable but not universal across the surveyed vendor ecosystem."

**Acceptance criterion:** Theme 6 convergence claim does not use "all major vendors" without acknowledging Palantir's documented divergence.

---

### Gap C: Query Framing Bias Disclosure (P2 — affects Methodological Rigor)

**Converged findings:** SR-004-iter4, RT-004-iter4, IN-002-iter4, IN-004-iter4

**Root cause:** The 40 search queries listed in the Methodology section are framed primarily around failure cases and best practices for avoiding negative prompting (e.g., "negative prompting best practices LLM 2024 2025," "LLM negation understanding failure 'do not' compliance rate," "prompt engineering 'positive vs negative framing' effectiveness"). No queries specifically targeted "negative prompting success stories," "when negative prompting works well," or "negative prompting advantages." This creates a search framing bias toward finding evidence that negative prompting fails, which is consistent with (but not independent of) the survey's primary conclusion.

**Impact:** The Survey Limitations paragraph (Revision 3) discloses single-researcher bias, saturation, URL access dates, and English-only scope — but not query framing bias. This is the most significant remaining methodological disclosure gap given that the survey's primary conclusion aligns with the framing direction of most queries.

**Corrective action:** Add a sentence to the Survey Limitations paragraph:
- Proposed addition: "Search queries were primarily framed around negative prompting limitations and best practices for avoiding negative framing; no queries specifically targeted documentation of successful negative prompting applications or scenarios where negative instructions perform better than positive framing. Researchers seeking contrary evidence may benefit from targeted queries in this direction."

**Acceptance criterion:** Survey Limitations explicitly acknowledges that search query framing may have systematically over-represented evidence for negative prompting failures relative to successes.

---

## Part V: Scoring Trajectory

| Iteration | Composite Score | Verdict | Key Gap |
|-----------|----------------|---------|---------|
| 1 | 0.770 | REJECTED | Missing evidence tier definitions, source count errors, no caveats |
| 2 | 0.907 | REVISE | Sub-tier labels incomplete, Source 26 overcounting, analyst-inference labels missing |
| 3 | 0.900 | REVISE | Single-researcher disclosure missing, URL access dates, L0 model-gen caveat absent |
| 4 | 0.910 | REVISE | L0 temporal framing inaccuracy ("future" for current models), Theme 6 convergence overstatement, query framing bias |

**Current composite: 0.910 — REVISE band (0.85-0.91)**

**Assessment:** The document has improved from 0.770 to 0.910 across four iterations, resolving all structural, source-counting, evidence-tier, and methodological disclosure gaps from prior iterations. The Iteration 4 REVISE result is not due to persisting prior gaps — it is due to a new accuracy error introduced in Revision 3 (the "future" temporal framing in the model-generation caveat) and two remaining minor gaps (Theme 6 convergence overstatement, query framing bias).

**Path to 0.95:** The three convergent gaps identified above are specific, narrow, and correctable in a single revision pass:
- Gap A (P1): One sentence correction in L0 — remove "future" framing, replace with current-model accurate language
- Gap B (P2): One sentence edit in Theme 6 — qualify "all major vendors" to acknowledge Palantir exception
- Gap C (P2): One sentence addition to Survey Limitations paragraph — disclose query framing bias

These three changes collectively address the primary scoring gaps across Internal Consistency (-0.07 from target 0.95), Completeness (-0.04), and Methodological Rigor (-0.04). Projected composite after Gap A + Gap B + Gap C addressed: approximately 0.94-0.96.

---

## Execution Statistics

- **Total Findings:** 25 (across all strategies)
- **Critical:** 0
- **Major:** 7 (converging on Gap A — L0 temporal framing)
- **Minor:** 18 (converging on Gaps B and C)
- **Protocol Steps Completed:** 10 of 10 strategies executed
- **H-16 Compliance:** S-003 (Steelman) executed before all critique strategies ✓
- **Constitutional Violations:** 0
- **Chain-of-Verification Discrepancies:** 2 (CV-002-iter4 Major, CV-003-iter4 Minor)
- **New findings vs. Iter 3 gaps:** All 4 iter3 gaps (A-D) have been addressed. 3 new convergent gaps identified (A-C above)

---

*Report generated by adv-executor for PROJ-014 C4 Tournament, Iteration 4.*
*Date: 2026-02-27*
*H-15 Self-Review Applied: (1) All 7 major findings trace to the same root cause (L0 "future" framing) — convergence confirmed. (2) Severity classifications verified: no Major finding without specific quoted evidence. (3) Finding IDs follow {PREFIX}-{NNN}-iter4 format throughout. (4) Summary table matches detailed findings. (5) Score computation verified: 0.182+0.176+0.182+0.1395+0.1365+0.094 = 0.910. (6) Prior gaps A-D from iter3 confirmed addressed in current document. (7) No findings minimized: the L0 "future" framing error is genuinely new and introduced by Revision 3; it is correctly classified as Major.*
