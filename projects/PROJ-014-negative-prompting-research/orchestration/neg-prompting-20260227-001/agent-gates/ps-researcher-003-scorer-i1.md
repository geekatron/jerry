# Quality Score Report: Context7 Library Documentation Survey — Negative Prompting Patterns

## L0 Executive Summary

**Score:** 0.80/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.76)
**One-line assessment:** The survey provides strong primary-source coverage and internal narrative coherence for 5 of 6 libraries, but fails to reach the C4 threshold (0.95) due to a missing hypothesis verdict in L0, unintegrated academic evidence, non-reproducible methodology (missing access dates), an overstated OpenAI Coverage Matrix entry, and unjustified source scope — all of which must be resolved before the artifact can serve as a reliable Phase 2 input.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-014-negative-prompting-research/research/context7-survey.md`
- **Deliverable Type:** Research Survey (Context7 Library Documentation Survey on Negative Prompting Patterns)
- **Criticality Level:** C4
- **Quality Threshold:** 0.95 (C4 — all tiers + tournament, per quality-enforcement.md)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** Yes — 47 findings from ps-researcher-003-executor-findings.md (6 Critical, 25 Major, 16 Minor)
- **Scored:** 2026-02-27T00:00:00Z
- **Iteration:** 1

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.80 |
| **Threshold** | 0.95 (H-13, C4) |
| **Verdict** | REVISE |
| **Gap to Threshold** | 0.15 |
| **Strategy Findings Incorporated** | Yes — 47 findings (6 Critical, 25 Major, 16 Minor) |

**Note:** 6 unresolved Critical findings from adv-executor automatically trigger REVISE regardless of score. Score also falls below the 0.95 threshold, independently confirming REVISE.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.79 | 0.158 | L0/L1/L2 structure present; 6 targets covered; but no hypothesis verdict in L0, LangChain thin, excluded providers unjustified, PS Integration missing from nav table |
| Internal Consistency | 0.20 | 0.81 | 0.162 | L0/L1/L2 narrative coherent; material inconsistency: OpenAI Coverage Matrix claims "explicit coverage" while body acknowledges 403; vendor contradiction framed as established fact |
| Methodological Rigor | 0.20 | 0.76 | 0.152 | 28 queries logged; Context7 fallback disclosed; but no access dates, no query-to-library mapping, WebSearch/Context7 equivalence unvalidated, "emerging consensus" unsourced |
| Evidence Quality | 0.15 | 0.78 | 0.117 | Direct quotes used throughout L1; but both academic papers (arXiv:2601.03269, arXiv:2510.18892) are in references only — not integrated into findings; low-authority sources (Lakera, 16x.engineer) cited without tier differentiation |
| Actionability | 0.15 | 0.82 | 0.123 | L2 Implications section provides a refined hypothesis and identifies 4 implications; but implications are not mapped to specific Phase 2 tasks or artifacts; hypothesis verdict absent from L0 prevents readers from acting on the primary conclusion |
| Traceability | 0.10 | 0.82 | 0.082 | Query Log is an excellent traceability mechanism (28 entries, each query logged); but URL access dates are absent, "Young et al. 2025" author attribution for arXiv:2601.03269 is unverifiable, "2025 Community Consensus" is unattributed |
| **TOTAL** | **1.00** | | **0.794** | |

**Rounded composite: 0.80**

---

## Detailed Dimension Analysis

### Completeness (0.79/1.00)

**Evidence:**
The survey covers all 6 stated library/framework targets (Anthropic, OpenAI, LangChain, LlamaIndex, DSPy, Prompt Engineering Guides). The L0/L1/L2/Methodology/References structure is present and populated. The Coverage Matrix provides a systematic per-library summary. All 28 queries are documented. Key findings 1-5 in L0 address the primary research question with appropriate specificity.

**Gaps:**

1. **No explicit hypothesis verdict in L0 (Critical — FM-001):** The stated research purpose is to "directly inform the PROJ-014 hypothesis that negative unambiguous prompting reduces hallucination by 60%." L2 has an "Implications for PROJ-014 Hypothesis" section that includes the phrase "The 60% claim is unsupported by any vendor documentation," but L0 contains no verdict statement. A reader consuming only the executive summary cannot determine whether the hypothesis was falsified, unsupported, or conditionally supported. This is a material completeness gap given the survey's stated purpose.

2. **LangChain coverage is thin (Critical — FM-002):** Only 3 queries were executed against LangChain, and no direct documentation was extracted. The "silent" conclusion may be premature — LangChain has extensive LCEL (LangChain Expression Language) prompt composition documentation that was not surfaced. A conclusion of "no guidance found" with 3 queries is weaker than one supported by systematic exhaustion of available documentation paths.

3. **Excluded providers unjustified (Major — DA-004, IN-002):** Google (Gemini), Meta (LLaMA), and Cohere are not included in the 6 sources. No rationale is given for their exclusion. At C4 criticality, the scope decision must be explicitly documented.

4. **PS Integration section not in navigation table (Major — CC-001):** The document includes a "PS Integration" section below References, but the Document Sections navigation table does not list it. This is a H-23 partial compliance gap.

**Improvement Path:**
Add an explicit "Hypothesis Verdict" subsection to L0 with a clear verdict statement on the 60% claim. Expand LangChain coverage with at least 2 additional targeted queries (LCEL, chat model prompts). Add a "Source Selection Rationale" subsection to Methodology. Add PS Integration to the nav table.

---

### Internal Consistency (0.81/1.00)

**Evidence:**
The L0 Coverage Matrix correctly reflects the per-library findings in L1 for LangChain ("No — silent on the topic"), LlamaIndex ("No — silent on the topic"), and DSPy ("No — silent on the topic"). The narrative in L2 Cross-Library Analysis is coherent with the L1 library sections. The four convergent patterns identified in L2 are traceable to the specific library findings that support them. No direct contradiction was found between L0 Key Findings 1-4 and L1 per-library text.

**Gaps:**

1. **OpenAI Coverage Matrix inconsistency (Major — DA-002, CC-004, CV-004):** The Coverage Matrix marks OpenAI as "Yes — direct guidance with examples" with "Recommends Positive Over Negative: Yes." However, L1 Library 2 Queries Executed section states: "OpenAI platform docs returned 403 on direct fetch; content retrieved via WebSearch snippets and cookbook guides." Cookbook guides are developer examples, not the official prompt engineering guide. The Coverage Matrix row for OpenAI presents a stronger evidence basis than was actually achieved. This is a genuine internal inconsistency between the matrix and the methodology section.

2. **Vendor contradiction framed as established fact (Critical — DA-001):** L2 Pattern Divergence states: "This suggests the recommendation is oversimplified. In practice, even the vendors who recommend positive framing recognize that negative constraints are sometimes the clearest way to express a boundary." This conclusion is stated as established fact, but the evidence supports it only as one plausible interpretation. An alternative explanation — that vendor-authored examples were written before the positive-framing recommendation was adopted, or that example prompts serve pedagogical rather than production purposes — is not acknowledged. The survey's most significant finding is presented with higher certainty than the evidence warrants.

3. **"Prompt Engineering Guides" category conflates source types (Major — FM-006):** The Coverage Matrix lumps promptingguide.ai (community guide, MEDIUM authority), Lakera (2026 blog post, LOW authority), and 16x.engineer (analysis post, LOW authority) under a single "Prompt Engineering Guides" row. The row is assigned "Explicit coverage: Yes — from OpenAI's original guidance" — but promptingguide.ai is not OpenAI; it is a community resource that cites OpenAI. This conflation makes the coverage appear higher-authority than it is.

**Improvement Path:**
Correct the OpenAI row in the Coverage Matrix to "Partial — cookbook guides only; platform docs inaccessible (403)." Add a qualifier to the vendor contradiction conclusion acknowledging alternative explanations. Split the "Prompt Engineering Guides" Coverage Matrix row into distinct authority tiers.

---

### Methodological Rigor (0.76/1.00)

**Evidence:**
The survey executes 28 queries against 6 target libraries (plus 3 academic queries). The query log is complete and includes query text, method (WebSearch vs. WebFetch), target URL or search string, and result status. Context7 MCP unavailability is disclosed transparently. A source hierarchy (HIGH/MEDIUM/LOW) is defined in the Methodology section. WebFetch was used for direct documentation access wherever accessible, which is methodologically sounder than relying solely on search snippets.

**Gaps:**

1. **Non-reproducible methodology — missing access dates (Critical — PM-001, RT-001):** Zero of the 28 URLs in the query log include access dates. Vendor documentation is living content — the Anthropic and OpenAI guides referenced are subject to update at any time. A researcher attempting to reproduce this survey in three months cannot verify that the retrieved content matches what the survey describes. The absence of access dates is a fundamental reproducibility gap.

2. **WebSearch/Context7 equivalence unvalidated (Critical — IN-001, SR-001):** The Methodology states the WebSearch fallback was used "per the MCP error handling protocol" and treats it as equivalent to Context7. However, Context7 provides structured library documentation lookup (official library docs indexed as structured content), while WebSearch provides general web search results ranked by SEO. No validation step confirms that the WebSearch results covered the same content that Context7 would have indexed. The equivalence is asserted, not demonstrated.

3. **Query-to-library mapping absent (Major — FM-003):** The query log has 28 entries, but queries 26-28 (academic papers) are not reflected in the L0 Coverage Matrix (which lists only 6 library categories). A reader cannot determine without manual counting which queries serve which library. This absence weakens the traceability of coverage claims.

4. **"Emerging consensus" unsourced (Major — DA-003):** L0 Key Finding 5 states: "The emerging consensus is a hybrid approach: use negative constraints for hard safety boundaries and prohibitions, but pair them with positive alternatives." No source is cited for this characterization. The synthesis is the researcher's own — which may be accurate — but presenting it as an "emerging consensus" without attribution elevates its authority beyond what the evidence supports.

5. **Source tier differentiation not applied in presentation (Major — PM-002):** The Methodology defines a source hierarchy (HIGH, MEDIUM, LOW) but the References list contains no tier annotations. L0 and L1 cite Lakera (LOW) and 16x.engineer (LOW) alongside Anthropic and OpenAI (HIGH) without differentiation. The stated methodology was defined but not applied.

**Improvement Path:**
Add "(Accessed: 2026-02-27)" to every URL in the Query Log and References. Add a "Reproducibility Statement" to the Methodology section. Revise the Tool Availability Note to explicitly acknowledge what Context7 provides vs. WebSearch, and what verification steps were taken. Add a query-to-library mapping table. Replace the unsourced "emerging consensus" with specific attributed claims from the prompt engineering guides reviewed. Add authority tier annotations to all References.

---

### Evidence Quality (0.78/1.00)

**Evidence:**
Direct quotes are used extensively in L1 for Anthropic (4 XML code blocks quoted verbatim), OpenAI (6 direct quotes across GPT-4.1 through GPT-5.2 guides), LlamaIndex (5 direct quotes from default_prompts.py source), and DSPy (direct quotes from assertions documentation). For the libraries that provided accessible content, the evidence quality is strong — the researcher retrieved primary source material and quoted it directly rather than paraphrasing.

**Gaps:**

1. **Academic papers not integrated into findings (Major — DA-005, IN-004, RT-002):** Two academic papers are referenced:
   - arXiv:2601.03269 ("The Instruction Gap") — These are the only empirical sources that provide compliance rate data comparing negative vs. positive instruction following across model architectures.
   - arXiv:2510.18892 — Tests "256 LLMs across 20 instruction types."

   Both papers appear in the Query Log (entries 27-28) and References (#18, #19), but neither is quoted or analyzed in L1 or L2 findings. The L2 Coverage Gaps section mentions "The 'Instruction Gap' paper identifies that models follow negative instructions less reliably than positive ones" without quoting the finding or providing the compliance rate gap. These are the only sources with empirical data rather than prescriptive guidance — their absence from the findings is the single largest evidence quality gap.

2. **Low-authority sources cited without tier differentiation in findings presentation (Major — PM-002):** L1 Library 6 Pattern 3 cites the Lakera prompt engineering guide (2026) and L0 Key Finding 5 draws on it — but Lakera is a commercial security company publishing a guide, categorized as LOW authority per the survey's own source hierarchy. The Pink Elephant Problem analysis from 16x.engineer is also LOW. In L0 Key Finding 5, these sources are cited alongside vendor documentation without differentiation.

3. **OpenAI evidence basis overstated (Major — DA-002):** Reference #3 (OpenAI Prompt Engineering Guide) is marked "(403 on direct fetch; content confirmed via secondary sources)." The Coverage Matrix and L0 Key Finding 2 treat this as direct OpenAI guidance, but the source accessed was promptingguide.ai (a third-party resource that quotes OpenAI), not OpenAI's own platform documentation. The evidentiary weight of this source is lower than presented.

4. **"Claude 4.6" version label unverifiable (Major — CV-001, RT-003):** The survey references "Anthropic Claude 4.6 best practices" based on a URL path (`claude-4-best-practices`). Anthropic's public naming conventions do not use decimal versioning for Claude (models are named Claude 3 Opus, Claude 3.5 Sonnet, etc.). The version label "4.6" appears to be either internal, future-dated, or a URL slug that does not correspond to publicly documented versioning. This creates an ambiguity about which model generation the guidance applies to.

**Improvement Path:**
Add an "Academic Research Findings" subsection to L2 with direct quotes or accurately paraphrased key findings from both arXiv papers. Add authority tier annotations to all References (#HIGH, #MEDIUM, #LOW). Downgrade the OpenAI Prompt Engineering Guide reference to reflect secondary source access. Add a note on the Claude version URL ambiguity acknowledging that the URL slug "claude-4-best-practices" does not correspond to a publicly documented Anthropic model version.

---

### Actionability (0.82/1.00)

**Evidence:**
The L2 Implications for PROJ-014 Hypothesis section provides concrete takeaways: (1) the 60% claim is unsupported, (2) vendor recommendations conflict with vendor practice, (3) the hypothesis may be asking the wrong question, and (4) a more defensible hypothesis reframe is provided. The "Next Agent Hint" directs the orchestrator to ps-analyst. The refined hypothesis ("Specific, contextually justified constraints... combined with structural enforcement mechanisms reduce hallucination more effectively than unstructured instructions") is directly useful for Phase 2.

**Gaps:**

1. **Hypothesis verdict absent from L0 (Major — FM-001, SR-002):** The actionable conclusion — that the 60% claim is unsupported — is buried in L2. A reader who consumes only L0 (the appropriate entry point for stakeholders and subsequent agents) cannot determine the survey's verdict. In the orchestration pipeline, if ps-analyst receives this artifact and reads L0 first, the primary actionable conclusion is not visible.

2. **L2 implications not mapped to Phase 2 tasks (Major — FM-005, PM-003):** The 4 implications are stated at the research level but not operationalized: "Implication 1: The 60% claim is unsupported" does not tell ps-analyst which specific task, artifact, or analytical approach is required in Phase 2. The "more defensible hypothesis" is provided but not connected to a specific Phase 2 deliverable.

3. **No operationalization of "what would support the hypothesis" (Minor — DA-006):** The implications section does not specify what evidence would constitute support for a revised version of the 60% claim. Without this, Phase 2 has no clear success criteria for the hypothesis-testing task.

**Improvement Path:**
Add a "Hypothesis Verdict" subsection to L0 with the explicit verdict and the refined hypothesis. Revise L2 Implications to add explicit Phase 2 mapping: "Implication X should inform [specific task/artifact] in Phase 2." Add a "What Would Support the Hypothesis" subsection specifying the evidence type (controlled experiment, compliance rate data, etc.) that Phase 2 would need to produce.

---

### Traceability (0.82/1.00)

**Evidence:**
The Query Log (28 entries) is the strongest traceability feature of this survey. Each library section references specific queries by method and target, enabling a reader to trace each pattern back to its source query. References are numbered (1-20) and linked to specific key insights. Each L1 library section begins with a "Queries Executed" subsection explicitly listing the queries used for that library.

**Gaps:**

1. **URL access dates absent (Critical — PM-001, RT-001):** Zero URLs include access dates. For a temporal point-in-time artifact (vendor documentation changes frequently), this breaks the traceability chain. A reader cannot determine whether the content described matches current or historical documentation.

2. **"Young et al., 2025" attribution unverifiable (Major — CV-002):** L2 Coverage Gaps references "The 'Instruction Gap' paper (Young et al., 2025)" — but the survey body never confirms this author attribution against the actual paper. The arXiv ID (2601.03269) is present but the author attribution may be incorrect; it cannot be verified from the available content.

3. **"2025 Community Consensus" unattributed (Major — DA-003, CC-003):** L1 Library 6 Pattern 5 cites "2025 Community Consensus" as the source for three quoted best-practice statements. No specific publications, forum threads, or community resources are identified as constituting this consensus. The traceability chain for these three quoted items is broken.

4. **Academic papers listed but findings disconnected (Minor — CC-002):** References #18 and #19 establish that the academic papers were accessed (per the Query Log), but their findings are not in the body. This means the references are traceable to sources but the specific claims derived from those sources are absent — partial traceability.

**Improvement Path:**
Add "(Accessed: 2026-02-27)" to every URL reference. Replace "Young et al., 2025" with the actual author list from the paper, or remove the author attribution and cite by arXiv ID only. Replace "2025 Community Consensus" with specific source attributions. Integrate academic paper findings into L2 body to close the reference-without-finding gap.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.79 | 0.93+ | Add explicit "Hypothesis Verdict" subsection to L0: state that the 60% claim is NOT SUPPORTED by any surveyed source; this is the survey's primary deliverable and must be findable in L0 without reading L2 |
| 2 | Methodological Rigor | 0.76 | 0.90+ | Add "(Accessed: 2026-02-27)" to all 28 URLs in the Query Log and all 20 References; add a Reproducibility Statement to the Methodology section |
| 3 | Evidence Quality | 0.78 | 0.90+ | Add an "Academic Research Findings" subsection to L2 integrating direct quotes or key findings from arXiv:2601.03269 and arXiv:2510.18892 — these are the only empirical sources in the survey |
| 4 | Internal Consistency | 0.81 | 0.93+ | Correct the OpenAI row in the Coverage Matrix from "Yes — direct guidance" to "Partial — cookbook guides only; platform docs returned 403"; qualify the vendor contradiction conclusion with alternative explanations |
| 5 | Methodological Rigor | 0.76 | 0.90+ | Add a "Source Selection Rationale" subsection to Methodology documenting why these 6 sources were selected and explicitly acknowledging Google, Meta, and Cohere as excluded scope |
| 6 | Methodological Rigor | 0.76 | 0.90+ | Add a query-to-library mapping table; add source tier annotations (HIGH/MEDIUM/LOW) to all 20 References |
| 7 | Actionability | 0.82 | 0.92+ | Map L2 implications to specific Phase 2 tasks/artifacts; add "What Would Support the Hypothesis" specification |
| 8 | Traceability | 0.82 | 0.92+ | Replace "Young et al., 2025" with verified author attribution or arXiv-ID-only citation; replace "2025 Community Consensus" with attributed quotes from specific sources |
| 9 | Completeness | 0.79 | 0.93+ | Expand LangChain coverage with at least 2 additional targeted queries (LCEL prompt composition, ChatModel prompt templates); either strengthen or qualify the "silent" conclusion |
| 10 | Completeness | 0.79 | 0.93+ | Add PS Integration to Document Sections navigation table (resolves H-23 partial violation) |

---

## Critical Findings Requiring Mandatory Resolution

The following 6 Critical findings from adv-executor are unresolved and independently trigger REVISE regardless of composite score:

| # | Finding ID | Strategy | Finding | Blocks |
|---|-----------|---------|---------|--------|
| 1 | FM-001 | S-012 | No explicit hypothesis verdict in L0 (RPN 256) | Completeness |
| 2 | FM-002 | S-012 | LangChain coverage insufficient for "silent" conclusion (RPN 252) | Completeness |
| 3 | IN-001 | S-013 | WebSearch equivalence to Context7 unvalidated | Methodological Rigor |
| 4 | PM-001 | S-004 | Non-reproducible methodology (no access dates) | Methodological Rigor |
| 5 | RT-001 | S-001 | Temporal attack vector: live URLs without archival | Methodological Rigor |
| 6 | DA-001 | S-002 | Vendor contradiction conclusion overstated | Internal Consistency |

All 6 Critical findings must be resolved before the next scoring iteration. Resolution of P0 items from the executor recommendations (items 1-6) directly addresses 5 of 6 Critical findings.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score — specific findings cited by ID
- [x] Uncertain scores resolved downward: Evidence Quality was considered at 0.80 (strong direct quotes) but reduced to 0.78 due to the academic paper integration gap being material; Methodological Rigor was considered at 0.78 but reduced to 0.76 given that the reproducibility gap (missing access dates on all 28 URLs) is a fundamental issue, not a minor one
- [x] First-draft calibration considered: this is iteration 1 of a C4 artifact against a 0.95 threshold; scoring 0.80 on first pass is consistent with expected first-draft range (0.65-0.80)
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] S-014 executor self-score (0.81 composite) used as calibration anchor; independent scorer arrived at 0.80 — within 0.01 difference, confirming calibration is consistent

**Calibration anchor comparison (executor S-014 vs. this scorer):**

| Dimension | Executor S-014 | This Scorer | Delta | Direction |
|-----------|---------------|-------------|-------|-----------|
| Completeness | 0.80 | 0.79 | -0.01 | Stricter |
| Internal Consistency | 0.82 | 0.81 | -0.01 | Stricter |
| Methodological Rigor | 0.78 | 0.76 | -0.02 | Stricter |
| Evidence Quality | 0.79 | 0.78 | -0.01 | Stricter |
| Actionability | 0.83 | 0.82 | -0.01 | Stricter |
| Traceability | 0.83 | 0.82 | -0.01 | Stricter |
| **Composite** | **0.81** | **0.80** | **-0.01** | **Stricter** |

This scorer applied stricter values across all 6 dimensions, consistent with anti-leniency bias protocol. Methodological Rigor received the largest additional reduction (-0.02) because the absence of access dates on 28 URLs represents a total failure of URL archiving — not a minor gap — and this dimension had the most Critical findings (3 of 6 total).

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.80
threshold: 0.95
weakest_dimension: Methodological Rigor
weakest_score: 0.76
critical_findings_count: 6
iteration: 1
improvement_recommendations:
  - "Add explicit Hypothesis Verdict subsection to L0 stating 60% claim is NOT SUPPORTED"
  - "Add access dates (Accessed: 2026-02-27) to all 28 URLs in Query Log and all 20 References"
  - "Add Academic Research Findings subsection to L2 integrating arXiv:2601.03269 and arXiv:2510.18892"
  - "Correct OpenAI Coverage Matrix row to Partial - cookbook guides only"
  - "Add Source Selection Rationale subsection documenting excluded providers (Google, Meta, Cohere)"
  - "Add query-to-library mapping table and source tier annotations to References"
  - "Map L2 implications to specific Phase 2 tasks and artifacts"
  - "Replace unattributed citations (Young et al. 2025, 2025 Community Consensus) with verifiable attributions"
  - "Expand LangChain coverage with 2+ additional targeted queries"
  - "Add PS Integration to Document Sections navigation table (H-23 compliance)"
```
