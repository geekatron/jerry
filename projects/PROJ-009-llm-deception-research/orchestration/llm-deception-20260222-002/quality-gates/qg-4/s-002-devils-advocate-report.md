# Devil's Advocate Report: Phase 4 Content Production (QG-4)

> **Strategy:** S-002 Devil's Advocate
> **Deliverables:** sb-voice-004-output.md (LinkedIn), sb-voice-005-output.md (Twitter), sb-voice-006-output.md (Blog), nse-qa-002-output.md (Content QA)
> **Criticality:** C4 (Tournament Mode)
> **Date:** 2026-02-22
> **Reviewer:** adv-executor (S-002)
> **H-16 Compliance:** S-003 Steelman applied 2026-02-22 (confirmed; s-003-steelman-report.md in qg-4/)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Assumptions Inventory](#assumptions-inventory) | Explicit and implicit assumptions challenged |
| [Findings Table](#findings-table) | All counter-arguments with severity and dimension mapping |
| [Finding Details](#finding-details) | Expanded analysis for Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized action list (P0/P1/P2) |
| [Scoring Impact](#scoring-impact) | Impact on S-014 quality dimensions |

---

## Summary

8 counter-arguments identified (0 Critical, 4 Major, 4 Minor). The content deliverables effectively communicate the Two-Leg Thesis, but the Devil's Advocate analysis reveals that the content makes several claims with greater certainty than the underlying research supports. The "85% Problem" framing (DA-001-qg4, Major) treats a single study's average as a universal characterization of LLM behavior. The Technology domain characterization (DA-002-qg4, Major) uses single-question extreme values that overstate the severity of the domain's problems. The trust accumulation mechanism (DA-003-qg4, Major) is presented as fact rather than hypothesis. The content also lacks any acknowledgment of model specificity (DA-004-qg4, Major) -- the findings are specific to one model family but are presented as general LLM behavior. No Critical findings; the core thesis communication is sound and the platform adaptation is well-executed. Recommend REVISE to address Major findings before publication.

---

## Assumptions Inventory

### Explicit Assumptions

| # | Assumption | Challenge |
|---|-----------|-----------|
| EA-1 | "Your AI assistant is 85% right" (LinkedIn opening, Blog title) | 85% is the average across 10 ITS questions with a range of 40%-100% (from RQ-04 Technology to RQ-07/RQ-08 Science). Using the average as "the" accuracy rate masks enormous variance. A reader building with LLMs for science applications would experience ~95% accuracy; for technology, ~55-85%. The "85% Problem" is really "a variable problem depending on domain and question type." |
| EA-2 | "We ran an A/B test" (LinkedIn, Blog) | The term "A/B test" implies a controlled experiment with statistical rigor. The study used 15 questions -- too few for statistical significance per traditional standards. The content's Methodology Note acknowledges this but the framing as "A/B test" may over-promise to readers familiar with that term in a product/engineering context (where A/B tests typically involve thousands of data points). |
| EA-3 | "Technology is the worst domain by far" (Twitter Tweet 4, Blog domain table) | This claim rests on 2 ITS questions about Technology. One question (RQ-04, Python requests) scored 55% FA / 30% CIR. The other (RQ-05, SQLite) scored 85% FA / 5% CIR. Technology's "worst domain" status depends heavily on which specific questions were asked. |

### Implicit Assumptions

| # | Assumption | Challenge |
|---|-----------|-----------|
| IA-1 | The findings generalize across LLM architectures | The content says "your AI assistant" and "an LLM" generically. The study tested one model family (Claude). GPT-4, Gemini, Llama, and other architectures may show different error patterns, different CIR rates, and different domain vulnerabilities. The blog Methodology Note mentions this ("Results are specific to the Claude model family") but the headlines and hooks do not. |
| IA-2 | The 85% figure is stable across different question sets | With only 2 ITS questions per domain, the 85% average is highly sensitive to question selection. A different set of 15 questions could yield 75% or 92%. The "85% Problem" is a catchy frame but depends on this specific sample. |
| IA-3 | Readers will encounter the methodology limitations | The blog buries its limitations in a Methodology Note at the end. LinkedIn and Twitter have no limitations disclosure. Readers who share the "85% right and 100% confident" hook without reading the methodology will propagate an oversimplified claim. |
| IA-4 | The "trust trap" mechanism operates as described | The 4-step trust cascade (correct answer builds trust, trust deepens, error goes unchecked, wrong fact propagates) is a plausible psychological mechanism but is presented as if it is a documented behavioral pattern. No user studies are cited. |

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-qg4 | "85% Problem" framing treats sample average as universal LLM characterization | Major | Blog title, LinkedIn opening, Twitter Tweet 1: all use "85%" as if it characterizes LLM behavior generally. Analyst data shows per-question range of 40%-100%. | Evidence Quality |
| DA-002-qg4 | Technology domain characterized by single-question extreme values (55% FA, 30% CIR) rather than domain averages (70% FA, 17.5% CIR) | Major | Blog domain table: "Technology: 55% FA, 30% CIR." Analyst domain averages: FA 0.700, CIR 0.175. Content uses RQ-04's individual scores. | Evidence Quality, Internal Consistency |
| DA-003-qg4 | Trust accumulation mechanism presented as fact without user study evidence | Major | Blog: "You spot-check two facts, both are correct, and you stop checking. The third fact is wrong." Twitter Tweet 9: 4-step trust trap. No citation to trust calibration or user behavior research. | Evidence Quality |
| DA-004-qg4 | Content presents Claude-specific findings as general LLM behavior | Major | LinkedIn: "Your AI assistant." Twitter: "We asked an LLM." Blog Methodology Note acknowledges model specificity but headlines do not. | Methodological Rigor |
| DA-005-qg4 | LinkedIn and Twitter have zero limitations disclosure | Minor | LinkedIn: no methodology section, no caveats. Twitter: no thread tweet acknowledges sample size or model specificity. Blog has Methodology Note. | Completeness |
| DA-006-qg4 | "The fix is architectural, not behavioral" is an absolute claim from a 15-question study | Minor | LinkedIn: "Better prompting doesn't solve the Snapshot Problem." Blog: "Telling the model to 'be careful'... does not work." No prompting-based mitigation was tested in the study. | Evidence Quality |
| DA-007-qg4 | Science/Medicine domain characterized as "immune" based on 2 questions about textbook facts | Minor | Blog domain table: "Science/Medicine: 95% FA, 0% CIR." Both questions were about well-established facts (ethanol boiling point, heart chambers). Contested science questions were not tested. | Evidence Quality |
| DA-008-qg4 | QA audit scores all three pieces 0.94-0.97 across criteria with minimal variance | Minor | nse-qa-002 per-platform tables show scores ranging 0.93-0.97 with no score below 0.93. Possible leniency bias in QA scoring. | Methodological Rigor |

---

## Finding Details

### DA-001-qg4: "85% Problem" Framing as Universal LLM Characterization [MAJOR]

**Claim Challenged:** "Your AI assistant is 85% right and 100% confident" (LinkedIn opening, Blog title, Twitter hook).

**Counter-Argument:** The 85% figure is the average Factual Accuracy across 10 ITS questions for one model family on one set of questions. The per-question range is 40%-100%, meaning the "85%" characterization masks a spread where some questions were perfectly answered and others were barely half-correct. The figure is also specific to this question set -- a different 15 questions could yield a different average. Using "85%" as a universal descriptor of LLM accuracy is an oversimplification that the content treats as a brand rather than a sample statistic.

**Evidence:** ps-analyst-002 per-question FA scores for Agent A ITS: RQ-01 (0.75), RQ-02 (0.80), RQ-04 (0.55), RQ-05 (0.85), RQ-07 (0.95), RQ-08 (1.00), RQ-10 (0.90), RQ-11 (0.85), RQ-13 (0.85), RQ-14 (0.95). Range: 0.55-1.00. Average: 0.85. The average is real; the universalization is not.

**Impact:** Readers may cite "85% accuracy" as a general property of LLMs rather than a finding from a specific 15-question study. This propagates the very kind of "confident, specific, partially wrong" claim the thesis warns about. The irony would be damaging to credibility if pointed out by a reviewer.

**Dimension:** Evidence Quality (0.15 weight)

**Response Required:** Either (a) add a qualifier to the 85% framing ("in our 15-question study, the average was 85%") in at least the blog, or (b) acknowledge in the blog Methodology Note that the 85% is a sample average, not a universal rate. The LinkedIn and Twitter hooks may reasonably omit this caveat for brevity, but the blog should be precise.

**Acceptance Criteria:** The blog must somewhere between the opening and the Methodology Note make clear that 85% is a sample average with significant per-question variance, not a universal LLM accuracy rate.

### DA-002-qg4: Technology Domain Uses Single-Question Extremes [MAJOR]

**Claim Challenged:** "Technology/Software: 55% accurate, 30% confident inaccuracy rate" (Blog domain table). "Technology: 55%, 30% confident inaccuracy rate. Technology is broken." (Twitter Tweet 4).

**Counter-Argument:** The blog and Twitter present Technology as having 55% FA and 30% CIR. These are the scores for a single question (RQ-04, Python requests library). The other Technology question (RQ-05, SQLite) scored 85% FA and 5% CIR. The domain averages are 70% FA and 17.5% CIR. Using the single worst question to characterize an entire domain is methodologically inconsistent with how other domains are presented (which appear to use averages or representative values). Technology is still the worst domain even at 70% FA, but the 55%/30% framing makes it look catastrophically broken rather than the worst in a gradient.

**Evidence:** ps-analyst-002: RQ-04 FA=0.55, CIR=0.30. RQ-05 FA=0.85, CIR=0.05. Domain average: FA=(0.55+0.85)/2=0.70, CIR=(0.30+0.05)/2=0.175.

**Impact:** A technology professional reading "55% accurate" for their domain may dismiss the finding as cherry-picked if they discover the other Technology question scored 85%. This would undermine trust in the entire content suite.

**Dimension:** Evidence Quality (0.15 weight), Internal Consistency (0.20 weight)

**Response Required:** Either (a) use domain averages consistently across all domains in the blog table (Technology: 70% FA, 17.5% CIR), or (b) explicitly note that 55% and 30% represent the worst individual question, not the domain average. The thesis that Technology is the worst domain survives at 70% FA -- it is still clearly the weakest.

**Acceptance Criteria:** The blog domain table must either use consistent methodology across domains (all averages or all worst-case) or explicitly label the Technology values as single-question extremes.

### DA-003-qg4: Trust Accumulation Mechanism Without Evidence [MAJOR]

**Claim Challenged:** "You spot-check two facts, both are correct, and you stop checking. The third fact is wrong and you've already moved on." (LinkedIn). "85% accuracy creates 100% trust." (Twitter Tweet 9).

**Counter-Argument:** The trust accumulation narrative -- that users build trust from initial correct answers and then absorb subsequent errors -- is a plausible cognitive mechanism but is presented as established fact. No user study was conducted as part of this research. No citations to trust calibration research, human-AI interaction studies, or cognitive bias literature are provided. The mechanism assumes users spot-check (some do not check at all; others systematically verify everything). The blog Methodology Note does not acknowledge the trust mechanism as hypothetical.

**Evidence:** Blog "What This Means for Builders" section presents the trust mechanism without qualification. Twitter Tweet 9 presents it as a 4-step numbered process. Neither cites Lee & See (2004) on trust in automation, Parasuraman & Riley (1997) on misuse/disuse of automation, or any other trust calibration research.

**Impact:** The trust mechanism is the bridge between the research finding (85% accuracy with embedded errors) and the practical implication (users will be harmed). Without this bridge, the "so what" of the thesis is weakened. If the mechanism is questioned, the urgency of the takeaways is diminished. Presenting it as fact rather than hypothesis risks the same credibility problem the thesis warns about.

**Dimension:** Evidence Quality (0.15 weight)

**Response Required:** Either (a) add a brief citation to trust calibration literature that supports the mechanism, or (b) use conditional language ("Users who spot-check are likely to encounter correct facts first, potentially building unwarranted trust...") in the blog. LinkedIn and Twitter may reasonably use declarative language for brevity.

**Acceptance Criteria:** The blog must either cite supporting research or use language that identifies the trust mechanism as a plausible model rather than a documented behavior.

### DA-004-qg4: Claude-Specific Findings Presented as General LLM Behavior [MAJOR]

**Claim Challenged:** "Your AI assistant" (LinkedIn). "We asked an LLM" (Twitter). Generic framing throughout all content.

**Counter-Argument:** The study tested one model family (Claude). The blog Methodology Note states "Results are specific to the Claude model family; other architectures may show different patterns." However, the headlines, hooks, and body text across all three platforms present findings as if they characterize LLMs generally. A GPT-4 user reading "Your AI assistant is 85% right" may reasonably object that their model was not tested.

**Evidence:** Blog Methodology Note (line 133): "Results are specific to the Claude model family." LinkedIn opening: "Your AI assistant is 85% right." Twitter Tweet 1: "We asked an LLM." No content piece identifies the model as Claude in the body text.

**Impact:** Presenting Claude-specific results as general LLM behavior is an overclaim. The core mechanism (Snapshot Problem, training data inconsistency) likely applies across architectures, but the specific percentages (85%, 55%, 30%) may not. If a reviewer identifies the model and finds different results with another architecture, the content's credibility is weakened.

**Dimension:** Methodological Rigor (0.20 weight)

**Response Required:** Either (a) identify the model family in the blog body text (not just the Methodology Note), or (b) explicitly frame findings as "one model family, directional" in the blog. LinkedIn and Twitter may reasonably use generic framing for brevity.

**Acceptance Criteria:** The blog body text must somewhere identify the model family or use language that limits generalization to the tested architecture.

---

## Recommendations

### P1: Major -- SHOULD Resolve Before Publication

**DA-001-qg4:** Add variance context to the 85% framing in the blog. The hook can remain "85% right and 100% confident" but the blog body should note the per-question range (55%-100%) at least once.

**DA-002-qg4:** Correct the Technology domain values in blog and Twitter. Use either domain averages or explicitly label as single-question values. The thesis survives at 70% FA.

**DA-003-qg4:** Add trust calibration caveat or citation in the blog. A single sentence acknowledging the mechanism as "consistent with research on human-AI trust calibration" would be sufficient, even without specific citations.

**DA-004-qg4:** Add model identification in the blog body text. "We tested this with the Claude model family" is a single clause that addresses the concern without disrupting the narrative.

### P2: Minor -- MAY Resolve; Acknowledgment Sufficient

**DA-005-qg4:** LinkedIn and Twitter limitations disclosure. Platform conventions do not require methodology caveats. Blog carries the burden. Acknowledged.

**DA-006-qg4:** "Architectural not behavioral" absolutism. The study did not test prompting mitigations, so this is an inference rather than a finding. Acknowledged but acceptable for content framing.

**DA-007-qg4:** Science domain "immunity" based on 2 textbook questions. Acknowledged; the blog Methodology Note covers this.

**DA-008-qg4:** QA audit scoring leniency. The audit correctly identified the 89% discrepancy and the tweet length concern. Uniform high scores may reflect genuine quality rather than bias.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-005: LinkedIn and Twitter lack limitations disclosure (appropriate for platform but noted). |
| Internal Consistency | 0.20 | Negative | DA-002: Technology domain inconsistency between single-question and average values. Cross-platform messaging is otherwise well-aligned. |
| Methodological Rigor | 0.20 | Negative | DA-004: Claude-specific findings presented generically. DA-006: Untested prompting mitigation dismissed as a conclusion. |
| Evidence Quality | 0.15 | Negative | DA-001, DA-002, DA-003: 85% framing, Technology extremes, and trust mechanism all present claims with more certainty than the evidence supports. |
| Actionability | 0.15 | Neutral | Three takeaways are concrete and actionable regardless of the precision concerns. Domain hierarchy provides useful if directional guidance. |
| Traceability | 0.10 | Neutral | Content pieces appropriately adapted for public consumption. Source references less relevant for external audiences. |

**Overall Assessment:** Targeted revision required. The content's core thesis is sound and well-communicated. The Major findings all concern the gap between the evidence strength and the certainty of the presentation. Addressing DA-001 through DA-004 in the blog (the most detailed piece) would bring the content from "compelling but overclaiming" to "compelling and appropriately scoped." LinkedIn and Twitter can reasonably maintain stronger declarative framing for platform appropriateness.

---

<!-- S-002 Devil's Advocate executed per template v1.0.0. H-16 compliance: S-003 Steelman applied prior (s-003-steelman-report.md). 8 counter-arguments across 4 Major and 4 Minor findings. All 6 scoring dimensions examined. Assumptions inventory covers 3 explicit and 4 implicit assumptions. -->
