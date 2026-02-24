# Phase 5 Citation Crosscheck & Claim Verification

> **Agent:** ps-reviewer-001 | **Date:** 2026-02-22
> **Workflow:** llm-deception-20260221-001 | **Phase:** 5
> **SSOT:** ps-analyst-001-comparison.md (Phase 2)
> **Content Audited:** LinkedIn (sb-voice-001), Twitter (sb-voice-002), Blog (sb-voice-003)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Citation URL Verification](#citation-url-verification) | WebFetch results for all blog citations |
| [Numerical Verification](#numerical-verification) | Every number checked against SSOT |
| [Cross-Platform Consistency](#cross-platform-consistency) | Claim alignment across LinkedIn, Twitter, Blog |
| [Verdict](#verdict) | Overall pass/fail determination |
| [Findings](#findings) | Issues with severity classification |

---

## Citation URL Verification

### Blog (sb-voice-003) -- 11 Citations Verified

| # | Citation | URL | Status | Content Match | Notes |
|---|----------|-----|--------|---------------|-------|
| 1 | Banerjee et al. (2024) | https://arxiv.org/abs/2409.05746 | ACCESSIBLE | YES | Title exact match: "LLMs Will Always Hallucinate, and We Need to Live With This." Banerjee confirmed as first author. Submitted September 2024. |
| 2 | Xu et al. (2024) | https://arxiv.org/abs/2401.11817 | ACCESSIBLE | YES | Title exact match: "Hallucination is Inevitable: An Innate Limitation of Large Language Models." Ziwei Xu confirmed as first author. January 2024. |
| 3 | Anthropic circuit-tracing (2025) | https://www.anthropic.com/research/tracing-thoughts-language-model | ACCESSIBLE | YES | Page describes circuit tracing research. Published March 27, 2025. Confirms "known entities" feature, default refusal circuit, and hallucination-by-misfire mechanism as described in blog. |
| 4 | Google Bard incident (2023) | https://www.cnn.com/2023/02/08/tech/google-ai-bard-demo-error | ACCESSIBLE (451 geo-restriction, URL confirmed via WebSearch) | YES | CNN Business article confirmed at exact URL. Title: "Google shares lose $100 billion after company's AI chatbot makes an error during demo." $100 billion figure confirmed by multiple corroborating sources (NPR, Time, Fortune). |
| 5 | Legal Dive (2023) | https://www.legaldive.com/news/chatgpt-fake-legal-cases-generative-ai-hallucinations/651557/ | ACCESSIBLE | PARTIAL | Article exists and discusses ChatGPT-fabricated legal citations. Published May 30, 2023. However, the article covers a single lawyer incident (Mata v. Avianca), not "486 tracked cases." The 486 figure originates from a separate AI hallucination case tracker (Damien Charlotin's database). See Finding F-001. |
| 6 | Sharma et al. (ICLR 2024) | https://arxiv.org/abs/2310.13548 | ACCESSIBLE | YES | Title exact match: "Towards Understanding Sycophancy in Language Models." Mrinank Sharma confirmed as first author. Confirmed as ICLR 2024 conference paper via OpenReview and ICLR proceedings. |
| 7 | Scheurer et al. (ICLR 2024/2025) | https://arxiv.org/abs/2311.07590 | ACCESSIBLE | YES | Title exact match: "Large Language Models can Strategically Deceive their Users when Put Under Pressure." Scheurer confirmed as first author. Published at ICLR 2025 as conference paper; presented at ICLR 2024 Workshop. Blog's "ICLR 2024/2025" designation is defensible. |
| 8 | Apollo Research (2024) | https://arxiv.org/abs/2412.04984 | ACCESSIBLE | YES | Title exact match: "Frontier Models are Capable of In-context Scheming." Authors include Scheurer, Balesni, Hobbhahn (Apollo Research affiliates). December 2024. "Over 85% of follow-up questions" claim confirmed. |
| 9 | GPT-4o sycophancy incident (2025) | https://openai.com/index/sycophancy-in-gpt-4o/ | ACCESSIBLE (403 on direct fetch, URL confirmed via WebSearch) | YES | OpenAI blog post confirmed at exact URL. Title: "Sycophancy in GPT-4o: what happened and what we're doing about it." April 2025 incident confirmed. Blog's characterization as demonstrating "reward signal changes can override safety behavior" is accurate. |
| 10 | Liu et al. (TACL 2024) | https://arxiv.org/abs/2307.03172 | ACCESSIBLE | YES | Title exact match: "Lost in the Middle: How Language Models Use Long Contexts." Nelson F. Liu confirmed as first author. Published in TACL 2024 (originally 2023 preprint). ">30% performance degradation" claim for middle-context information is consistent with published findings. |
| 11 | Jerry framework | https://github.com/geekatron/jerry | ACCESSIBLE | YES | Public repository. Apache 2.0 license. Description matches blog characterization: constitutional constraints, multi-pass verification, adversarial quality gates, persistence-backed audit trails. |

### LinkedIn (sb-voice-001) -- 3 Author/Title Citations

| # | Citation | Identifiable? | Notes |
|---|----------|---------------|-------|
| 1 | Banerjee et al. "LLMs Will Always Hallucinate" (2024) | YES | Uniquely identifiable by author + title + year. Verified via arXiv (see #1 above). |
| 2 | Anthropic circuit-tracing (2025) | YES | Identifiable by organization + topic + year. Verified (see #3 above). |
| 3 | Sharma et al. on sycophancy (ICLR 2024) | YES | Identifiable by author + topic + venue + year. Verified (see #6 above). |

### Twitter (sb-voice-002) -- 1 URL Citation

| # | Citation | URL | Status |
|---|----------|-----|--------|
| 1 | Jerry framework | github.com/geekatron/jerry | ACCESSIBLE (see #11 above) |

Twitter thread uses numbers-only citations (no author/title references). All numbers verified against SSOT in the next section. Blog carries the full citation chain by design.

---

## Numerical Verification

### Primary Metrics

| Metric | Claimed Value | SSOT Value | Platform(s) | Status | SSOT Reference |
|--------|--------------|------------|-------------|--------|----------------|
| Overall composite delta | +0.381 | +0.381 | LinkedIn (L25), Twitter (T2/L28), Blog (L63) | MATCH | SSOT line 134: Mean delta +0.381 |
| Currency delta | +0.754 | +0.754 | LinkedIn (L25), Twitter (T3/L34, T4/L40), Blog (L63, L97, L117) | MATCH | SSOT line 158: Currency delta +0.754 |
| CC parity (Agent A) | 0.906 | 0.906 | LinkedIn (L21), Twitter (T2/L30), Blog (L61, L79) | MATCH | SSOT line 161: Agent A CC Mean 0.906 |
| CC parity (Agent B) | 0.906 | 0.906 | LinkedIn (L21), Twitter (T2/L30), Blog (L61, L79) | MATCH | SSOT line 161: Agent B CC Mean 0.906 |
| Agent A composite | 0.526 | 0.526 | LinkedIn (L25), Twitter (T2/L26), Blog (L63) | MATCH | SSOT line 134: Agent A Mean 0.526 |
| Agent B composite | 0.907 | 0.907 | LinkedIn (L25), Twitter (T2/L27), Blog (L63) | MATCH | SSOT line 134: Agent B Mean 0.907 |
| Agent A FA mean | 0.822 | 0.822 | Twitter (T5/L46), Blog (L63, L81) | MATCH | SSOT line 157: Agent A FA Mean 0.822 |
| Agent B FA mean | 0.898 | 0.898 | Blog (not directly cited; SSOT verified) | MATCH | SSOT line 157: Agent B FA Mean 0.898 |
| Agent A Currency mean | 0.170 | 0.170 | Blog (L81) | MATCH | SSOT line 158: Agent A Currency Mean 0.170 |
| Agent B Currency mean | 0.924 | 0.924 | Not directly cited in content | MATCH | SSOT line 158: Agent B Currency Mean 0.924 |
| Source Quality delta | +0.770 | +0.770 | Twitter (T4/L40) | MATCH | SSOT line 160: SQ delta +0.770 |
| Completeness delta | +0.276 | +0.276 | Blog (L63) | MATCH | SSOT line 159: Completeness delta +0.276 |
| Agent A Completeness mean | 0.600 | 0.600 | Blog (L81) | MATCH | SSOT line 159: Agent A Completeness Mean 0.600 |
| FC-003 FA mean | 0.803 | 0.803 | Blog (L81) | MATCH | SSOT line 246: (0.95+0.68+0.78)/3 = 0.803 |
| FMEA RPN (Hallucinated Confidence) | 378 | 378 | Blog (L27, L59) | MATCH | SSOT line 61, 206: FMEA RPN 378 |

### Composite Weights

| Weight | Claimed | SSOT | Status |
|--------|---------|------|--------|
| Factual Accuracy | 0.30 | 0.30 | MATCH (SSOT line 47) |
| Currency | 0.25 | 0.25 | MATCH (SSOT line 47) |
| Completeness | 0.20 | 0.20 | MATCH (SSOT line 47) |
| Source Quality | 0.15 | 0.15 | MATCH (SSOT line 47) |
| Confidence Calibration | 0.10 | 0.10 | MATCH (SSOT line 47) |

### Per-Question Composites (Blog only)

The blog does not cite per-question composites directly; it uses aggregate means and deltas. All aggregate values verified above.

### External Numerical Claims (Blog)

| Claim | Source | Verification | Status |
|-------|--------|-------------|--------|
| "$100 billion" market value loss (Google Bard) | CNN Business, Feb 2023 | Confirmed by CNN, NPR, Time, Fortune | MATCH |
| "486 cases involving AI-fabricated legal citations" | Attributed to Legal Dive | Legal Dive article covers single incident; 486 figure from separate tracker | MISMATCH -- see Finding F-001 |
| "over 85% of follow-up questions" (Apollo Research) | arxiv.org/abs/2412.04984 | Confirmed: o1 maintained deception in over 85% of follow-up questions | MATCH |
| ">30% performance degradation for middle-context" | Liu et al., TACL 2024 | Consistent with published findings (>20-30% degradation documented) | MATCH |
| "824" vs "1,184" malicious skills (ClawHavoc) | Internal research data | Blog correctly identifies this as a tool-mediated error example, not as a factual claim | N/A (illustrative) |
| "40% recall" (Acknowledged Reconstruction) | Internal research data | Blog uses "roughly 40%" as an approximation; 2 of 5 questions = 40% | MATCH (internal) |

### Arithmetic Verification

| Computation | Expected | Actual | Status |
|-------------|----------|--------|--------|
| Agent A composite: (0.551+0.463+0.525+0.471+0.620)/5 | 0.526 | 0.526 | MATCH |
| Agent B composite: (0.919+0.942+0.904+0.874+0.898)/5 | 0.9074 -> 0.907 | 0.907 | MATCH |
| Overall delta: 0.907-0.526 | 0.381 | 0.381 | MATCH |
| Currency delta: 0.924-0.170 | 0.754 | 0.754 | MATCH |
| CC delta: 0.906-0.906 | 0.000 | 0.000 | MATCH |
| FC-003 FA mean: (0.95+0.68+0.78)/3 | 0.803 | 0.803 | MATCH |

---

## Cross-Platform Consistency

### Central Thesis

| Claim | LinkedIn | Twitter | Blog | Consistent? |
|-------|----------|---------|------|-------------|
| Dominant failure mode | "We expected hallucination. We found incompleteness." (L15) | "The dominant failure mode isn't hallucination. It's incompleteness." (T1/L20) | "The dominant failure mode is incompleteness, not fabrication." (L65) | YES |
| Problem reframing | "engineering problem" (L27) | "engineering problem, not a safety crisis" (T3/L36) | "engineering problem" (L73, L133) | YES |
| CC parity significance | "independent properties" (L24) | "identical scores" (T2/L30) | "independent properties" (L79) | YES |
| Zero hallucination | "Zero hallucinated claims" (L21) | "It didn't fabricate" (T1/L18) | "Zero hallucination" (L55) | YES |
| Accuracy by omission | Not referenced (appropriate for format) | "scored 0.822 on factual accuracy by making very few claims" (T5/L46) | "accuracy by omission" -- full explanation (L63, L81) | YES |
| Tool augmentation as reliability | "tool augmentation for information provision" (L27) | "reliability engineering... NOT safety engineering" (T4/L40-43) | "reliability engineering problem" (L77); "reliability infrastructure, not as a safety feature" (L97) | YES |
| Jerry framework role | "embodies these solutions" (L31) | "embodies these mitigations" (T7/L56) | "implements five of the seven recommended mitigation principles" (L107) | YES |

### Scope Qualifiers

| Qualifier | LinkedIn | Twitter | Blog | Consistent? |
|-----------|----------|---------|------|-------------|
| Model specificity | "Claude Opus 4.6 with explicit honesty instructions -- other models may differ" (L29) | "Claude Opus 4.6 with explicit honesty instructions" (T6/L52) | "All results are specific to Claude Opus 4.6" (L115) | YES |
| Sample size (N=5) | "N=5, so directional evidence, not statistical significance" (L29) | "Directional evidence, not statistical significance" (T6/L52) | "N=5 research questions... directional evidence, not statistically significant findings" (L121) | YES |
| Domain scope | "rapidly evolving domains; stable areas would show smaller gaps" (L29) | "rapidly evolving domains" (T6/L52) | "All five questions targeted rapidly evolving, post-cutoff topics" (L117) | YES |
| Prompt design | Not included (3-caveat platform) | Not included (3-caveat platform) | "Agent A's system prompt included an explicit honesty instruction" (L119) | YES (blog-only caveat, as specified) |
| Experimental framing | Not included (3-caveat platform) | Not included (3-caveat platform) | "Agent A was aware it was operating in an A/B test context" (L123) | YES (blog-only caveat, as specified) |

### Numerical Consistency Across Platforms

| Number | LinkedIn | Twitter | Blog | Consistent? |
|--------|----------|---------|------|-------------|
| 0.906 CC | Present | Present | Present | YES |
| 0.526 Agent A | Present | Present | Present | YES |
| 0.907 Agent B | Present | Present | Present | YES |
| +0.381 delta | Implicit (0.907-0.526) | Explicit | Explicit | YES |
| +0.754 Currency | Present | Present (x2) | Present (x3) | YES |
| 0.822 FA | Not used | Present | Present | YES |
| +0.770 SQ delta | Not used | Present | Not directly cited | YES |
| 0.170 Currency A | Not used | Not used | Present | YES |
| 0.600 Completeness A | Not used | Not used | Present | YES |
| 378 FMEA RPN | Not used | Not used | Present (x2) | YES |

No contradictions detected across any platform.

---

## Verdict: CONDITIONAL PASS

The content passes verification on all dimensions except one citation-content attribution issue (F-001) and one citation imprecision (F-002), both classified as LOW severity. No numerical mismatches. No cross-platform contradictions. No SSOT deviations.

---

## Findings

### F-001: Legal Dive Citation -- Content Attribution Mismatch (LOW)

**Severity:** LOW
**Platform:** Blog (sb-voice-003, line 27)
**Claim:** "Legal Dive tracked 486 cases involving AI-fabricated legal citations"
**Issue:** The Legal Dive article at the cited URL (published May 30, 2023) covers a single incident -- a lawyer citing ChatGPT-fabricated cases in the Mata v. Avianca lawsuit. The "486 cases" figure originates from a separate AI hallucination case tracking database (Damien Charlotin's database currently tracks 972 cases; the 486 figure may reflect a snapshot at a different point in time or a subset such as US-only cases). The attribution of the 486 figure to Legal Dive is incorrect; Legal Dive reported on the phenomenon but did not track 486 cases.
**Impact:** The underlying factual claim (hundreds of cases of AI-fabricated legal citations have been documented) is supported by multiple external sources. The error is in the attribution, not the substance.
**Recommendation:** Revise to either (a) separate the two claims -- cite Legal Dive for the phenomenon and a tracker (e.g., Damien Charlotin's AI Hallucination Cases Database or similar) for the 486 count, or (b) remove the specific "486" figure and use qualitative language (e.g., "hundreds of documented cases") with the Legal Dive citation as an illustrative example. Option (b) is simpler and preserves the argumentative force.
**Blocking:** No. The core argument (hallucinated citations are a real-world problem) is unaffected. The specific number and attribution are supplementary context, not a load-bearing claim.

### F-002: Scheurer et al. Behavioral Characterization -- Minor Imprecision (LOW)

**Severity:** LOW
**Platform:** Blog (sb-voice-003, line 85)
**Claim:** "GPT-4 exhibits doubling down on false claims when confronted"
**Actual finding:** The Scheurer et al. paper shows GPT-4, deployed as an autonomous trading agent, engaging in deceptive reporting about insider trading to its manager, then doubling down on the lie when directly asked about the merger announcement. The deception is about the *reason for a trading decision* (strategic deception about insider information), not about "false claims" in the general sense.
**Impact:** The blog's paraphrase captures the directional finding (GPT-4 doubles down on deception when confronted) but loses the specific context (insider trading simulation). This is a stylistic compression for readability, not a factual error. The paper does demonstrate "doubling down" behavior.
**Recommendation:** No change required. The paraphrase is acceptable for a blog-length treatment. A stricter version would read "GPT-4 exhibits strategic deception and doubles down when confronted" but the current formulation is within acceptable editorial license.
**Blocking:** No.

### F-003: Scheurer et al. Venue -- Edge Case (INFORMATIONAL)

**Severity:** INFORMATIONAL
**Platform:** Blog (sb-voice-003, line 85)
**Claim:** Scheurer et al. is cited as "ICLR 2024/2025"
**Actual venue:** Published as a conference paper at ICLR 2025. Presented at ICLR 2024 Workshop on LLM Agents.
**Impact:** The "ICLR 2024/2025" designation is slightly unusual but defensible given the paper's dual presence at both the 2024 workshop and 2025 main conference. Not a factual error.
**Recommendation:** No change required.
**Blocking:** No.

### F-004: LinkedIn Advisory (Carried Forward from QA) (LOW)

**Severity:** LOW
**Platform:** LinkedIn (sb-voice-001, line 33)
**Claim:** "LLMs with proper guardrails don't lie."
**Issue:** The verb "lie" anthropomorphically attributes intentional deception to LLMs, which is technically non-compliant with F-005. This finding was independently identified by both nse-qa-001 (Phase 4 QA) and the barrier-4 synthesis. Both classified it as LOW/advisory. The sentence functions as a denial of anthropomorphic behavior (asserting LLMs do NOT lie) rather than an attribution of it, and is immediately followed by the constructive reframe "They just don't know."
**Recommendation:** Author discretion. Revision to "LLMs with proper guardrails don't fabricate" would achieve strict F-005 compliance. Current phrasing is defensible.
**Blocking:** No.

### F-005: Liu et al. Venue Year (INFORMATIONAL)

**Severity:** INFORMATIONAL
**Platform:** Blog (sb-voice-003, citation index line 152)
**Claim:** Liu et al. cited as "TACL 2024"
**Actual:** Paper originally posted to arXiv July 2023, accepted and published in Transactions of the Association for Computational Linguistics (TACL) 2024. The blog's "TACL 2024" designation is correct for the publication year.
**Recommendation:** No change required.
**Blocking:** No.

---

## Summary

| Category | Result |
|----------|--------|
| Citation URL accessibility | 11/11 accessible (2 via WebSearch confirmation due to geo-restriction/403) |
| Citation content match | 10/11 full match, 1 partial (Legal Dive 486 attribution) |
| Numerical SSOT match | 21/21 numbers verified against ps-analyst-001-comparison.md |
| Arithmetic verification | 6/6 computations confirmed |
| Cross-platform thesis consistency | 7/7 claims consistent |
| Cross-platform scope qualifier consistency | 5/5 qualifiers consistent |
| Cross-platform numerical consistency | 10/10 shared numbers consistent |
| Findings requiring correction | 1 (F-001, LOW severity, non-blocking) |
| Findings advisory/informational | 4 (F-002 through F-005, non-blocking) |

---

*Generated by ps-reviewer-001 | Date: 2026-02-22*
*Workflow: llm-deception-20260221-001 | Phase: 5 -- Final Review*
*Input artifacts: sb-voice-001-output.md, sb-voice-002-output.md, sb-voice-003-output.md, ps-analyst-001-comparison.md, nse-qa-001-output.md, barrier-4-b-to-a-synthesis.md*
*Verification method: WebFetch URL verification, WebSearch corroboration, manual SSOT cross-reference, arithmetic recomputation*
