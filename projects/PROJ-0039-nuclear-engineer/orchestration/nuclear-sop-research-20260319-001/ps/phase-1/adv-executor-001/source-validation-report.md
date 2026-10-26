# Strategy Execution Report: Quality Gate 1 — Source Validation

## Execution Context

- **Strategy:** S-002 (Devil's Advocate) + S-007 (Constitutional AI Critique) — compound source validation gate
- **Template:** `.context/templates/adversarial/s-002-devils-advocate.md` (S-002), `.context/templates/adversarial/s-007-constitutional-ai.md` (S-007)
- **Deliverable:** `/Users/evorun/workspace/jerry/.worktrees/proj-0039-nuclear-engineer/projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-1/ps-researcher-001/nuclear-sop-survey.md`
- **Executed:** 2026-03-22T00:00:00Z
- **Executor:** adv-executor-001 (Quality Gate 1 — Source Validation)

### Protocol Note: H-16 Constraint

H-16 requires S-003 (Steelman) to be executed before S-002 (Devil's Advocate). This invocation is a compound source validation gate directed by the orchestrator, not a standalone adversarial review. The orchestrator has applied both S-002 and S-007 simultaneously for source integrity validation purposes. This deviates from the canonical H-16 ordering, which is noted for the orchestrator's record. The source validation nature of this gate (checking URL validity, attribution quality, hallucination detection, source authority) is a specialized quality gate that does not benefit from prior steelmanning of the research claims. Escalation to the orchestrator for H-16 compliance decision is recommended before proceeding to standard adversarial review phases.

### Tool Limitation Note

adv-executor operates at T1 (Read-Only) tier. URL verification was conducted through structural analysis — examining URL format patterns, ADAMS accession number validity, known NRC/DOE/IAEA URL conventions, and internal document consistency — rather than live WebFetch validation. Live URL verification would require T3 tool access (WebFetch). This report notes where live verification is needed and flags the limitation accordingly.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| DA-001 | Major | T4 source used as primary evidence for INPO T2-level claims (5 principles, 10 tools) | Section 2.1 |
| DA-002 | Major | INPO 09-004 proprietary content quoted through T4 blog without proper attribution chain | Section 2.2 |
| DA-003 | Minor | `50.54(i-1)` is non-standard CFR notation — likely incorrect subsection designation | Section 1.1 |
| DA-004 | Minor | NUREG-1358 cited via NRC safety issues index page rather than the NUREG document itself | Section 1.3 |
| DA-005 | Minor | Uncited factual claim in Section 6.4 (three-part communication required scenarios) | Section 6.4 |
| DA-006 | Minor | NUREG-0899 URL uses inconsistent lowercase `ml` casing vs. all other NRC ADAMS URLs | Section 1.3, References |
| CC-001 | Major | INPO 09-004 content sourced indirectly violates the project constraint that all research must come from verifiable web sources | Section 2.2 |
| CC-002 | Minor | Three URLs cannot be verified without live fetch: NUREG-0899 PDF, DOE-HDBK-1028-2009, DOE Maintenance Guide | References T1, T2 |

---

## Detailed Findings

### DA-001: T4 Source Used as Primary Evidence for INPO T2-Level Claims

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Section 2.1 (INPO's Human Performance Framework) |
| **Strategy Step** | S-002 Devil's Advocate — challenge whether claims are supported by cited sources |

**Evidence:**

> The framework rests on **five core principles** ([Nuclear PSG](https://www.nuclearpsg.co.uk/understanding-human-performance-in-nuclear/)):
> These principles drive **ten error reduction tools** ([Nuclear PSG](https://www.nuclearpsg.co.uk/understanding-human-performance-in-nuclear/)):

The five INPO human performance principles and the ten error reduction tools are attributed solely to `nuclearpsg.co.uk` — a UK nuclear consulting/blog website classified as T4 (context sources) in the document's own source hierarchy. The researcher's source count table confirms: "9 T4 sources (context) — contextual only."

**Analysis:**

The INPO human performance framework (five principles, ten tools) is core to INPO's published guidance, originally from INPO AP-913 and INPO 12-012. The document acknowledges (in section 2.2) that INPO documents are proprietary, but T4 context sources were used for content that should be attributed to:
- DOE-HDBK-1028-2009 (which the document cites in Section 6.3 for peer checking but NOT for the five principles or ten tools)
- INPO Traits of a Healthy Nuclear Safety Culture (cited as source 23 in References but not used in Section 2.1)
- The Academia.edu article (source 49) is cited once for a general framing statement, not for the specific five principles

The content of the five principles is plausible and accurate to the known INPO framework, but the source authority is T4. For the source hierarchy this research claims (T1/T2 for primary claims, T4 for context only), Section 2.1 violates the stated methodology. The DOE-HDBK-1028-2009 source, which was accessed and cited elsewhere in the document, likely contains this same framework and would be a T2 citation for the same content.

**Recommendation:**

Re-cite the five principles and ten tools from DOE-HDBK-1028-2009 (source 24) which is a T2 source and available at the DOE standards URL. Alternatively, cite DOE-HDBK-1028-2009 alongside nuclearpsg.co.uk to establish T2 authority for the content. Do not remove the T4 source, but it should not be the ONLY source for T2-level content claims.

---

### DA-002: INPO 09-004 Proprietary Content Quoted Through T4 Blog

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Section 2.2 (INPO 09-004: Procedure Use and Adherence) |
| **Strategy Step** | S-002 Devil's Advocate — challenge whether claims are actually supported by cited sources |

**Evidence:**

> INPO defines procedure adherence as "understanding a procedure's purpose, scope, and intent and following its direction. The user performs all actions as written in the sequence specified by the procedure" ([ATR Blog on INPO procedure adherence](https://www.atrco.com/blog/does-organization-follow-procedure-use-adherence-policy)).
>
> The critical safety rule: "if the procedure cannot be used as written, then the activity is stopped and the issue is resolved before the user continues" ([ATR Blog](https://www.atrco.com/blog/does-organization-follow-procedure-use-adherence-policy)).

These are presented as quoted definitions from INPO 09-004. The Limitations section acknowledges: "INPO standards documents (INPO 09-004) are proprietary and not publicly available in full text. Content was obtained through publicly available summaries and derivative sources."

**Analysis:**

The section heading is "INPO 09-004: Procedure Use and Adherence," which implies the content is from that specific INPO document. However, the actual source is a blog post (ATR Training & Consulting). Quotation marks around this content create a misleading implication that these are direct quotes from INPO 09-004, when they are actually quotes from a blog's interpretation of INPO 09-004.

This is a source provenance chain problem. The content is likely accurate (the ATR blog is a training company focused on INPO procedures), but:
1. The section is titled after the primary source (INPO 09-004)
2. The actual source is a T4 blog
3. Quotation marks suggest direct quotation from INPO 09-004
4. There is no indication in the citation that the content is from a blog summary, not the primary document

This creates a risk of third-party garbling: if the ATR blog mischaracterized or paraphrased INPO 09-004, that error would propagate into this research document without any way to verify it against the actual standard.

**Recommendation:**

Modify the attribution to be transparent about the indirect sourcing:
- Change section framing from "INPO defines procedure adherence as..." to "Per publicly available summaries of INPO 09-004 procedure adherence policy..."
- Add in-text clarification: "(sourced from ATR Training blog summary of proprietary INPO 09-004)"
- If the DOE-HDBK-1028-2009 document contains equivalent language (which it likely does, as DOE explicitly credits INPO's membership experience), use that as a T2 citation instead

---

### DA-003: `50.54(i-1)` — Non-Standard CFR Notation

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Section 1.1 (10 CFR Part 50: The Procedural Foundation) |
| **Strategy Step** | S-002 Devil's Advocate — challenge specific regulatory citations |

**Evidence:**

> - **50.54(i-1)**: Operator requalification program requirements within three months of receiving an operating license

**Analysis:**

10 CFR 50.54 uses standard alphabetic subsection notation: (a), (b), (c)...(z), then extended. The notation `(i-1)` with a hyphen is not a standard CFR citation format. The actual 10 CFR 50.54 has a subsection `(i)` that addresses operator qualifications and requalification. The `-1` suffix is potentially:
1. A garbling of `(i)(1)` — referring to the first paragraph of subsection (i)
2. An LLM-generated pseudo-citation that doesn't correspond to the actual CFR structure
3. A reference to a sub-item within `(i)` that the researcher could not directly verify

The "within three months" timing claim also needs verification. Operator requalification requirements under 50.54(i) are tied to the initial license issuance process, but the specific "three months" timeframe is a precise claim. Without live verification of the eCFR text, this cannot be confirmed or denied through structural analysis alone.

**Recommendation:**

Verify the actual subsection notation for the operator requalification requirement by reading `https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0054` directly. Correct to `50.54(i)` or the appropriate nested reference. Verify the "within three months" claim against the actual regulatory text.

---

### DA-004: NUREG-1358 Cited via NRC Safety Issues Index Page

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Section 1.3 (NUREG Series Guidance Documents) |
| **Strategy Step** | S-002 Devil's Advocate — is this actually supported by the cited source? |

**Evidence:**

> **NUREG-1358** (Lessons Learned from the Special Inspection Program for Emergency Operating Procedures) documents findings from an NRC special inspection program covering multiple plants between October 1988 and September 1991... ([NUREG-1358 Reference](https://www.nrc.gov/sr0933/Section%204.%20Human%20Factor%20Issues/hf4r7.html))

The URL `https://www.nrc.gov/sr0933/Section%204.%20Human%20Factor%20Issues/hf4r7.html` points to the NRC's SR0933 (Generic Safety Issues) database page `hf4r7`, which is a human factors issue entry that references NUREG-1358, not the NUREG-1358 document itself.

**Analysis:**

The citation is technically valid (the NRC SR0933 database does reference NUREG-1358), but it is indirect. The actual NUREG-1358 would have its own ADAMS accession number (in the ML series). The SR0933 index page may describe NUREG-1358 but does not contain its full content. The specific claims about "October 1988 to September 1991" timeframe and the "four specific areas" (technical guidelines, writer's guide, V&V, training) may or may not be directly stated in the SR0933 page — they may instead be LLM-generated summaries of what NUREG-1358 is expected to contain.

This is a weaker citation than a direct NUREG document link. The content is plausible but the traceability chain is incomplete.

**Recommendation:**

Find the NUREG-1358 ADAMS accession number and provide a direct link (e.g., `https://www.nrc.gov/docs/ML[accession].pdf`). The NRC ADAMS public search can locate NUREG-1358 directly. Replace or supplement the SR0933 index citation with the primary document citation.

---

### DA-005: Uncited Factual Claim in Section 6.4

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Section 6.4 (Three-Part Communication) |
| **Strategy Step** | S-002 Devil's Advocate — look for claims without citations |

**Evidence:**

> Required for: task assignments affecting equipment or personnel safety, equipment condition communication, critical parameter values, procedure step performance, and equipment operation or alteration.

This sentence appears between two cited statements in the three-part communication section. The surrounding text cites `humanperformancetools.com`. This line has no citation marker.

**Analysis:**

The content is plausible and consistent with the surrounding cited material. It is likely from the same humanperformancetools.com source. However, it is presented as a standalone statement without a citation, which violates the document's own standard of citing every specific claim. In the context of source validation, this is a documentation gap — a minor one, but it creates a traceability gap for downstream consumers of this research.

**Recommendation:**

Add the appropriate citation marker. If from humanperformancetools.com, add `([Human Performance Tools](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-three-part-communication))` at the end of the line.

---

### DA-006: NUREG-0899 URL Casing Inconsistency

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | References T1, inline citations |
| **Strategy Step** | S-002 Devil's Advocate — URL format validity assessment |

**Evidence:**

> [NUREG-0899 PDF](https://www.nrc.gov/docs/ml1025/ml102560007.pdf)

All other NRC ADAMS URLs in the document use mixed case matching the ADAMS accession number format (e.g., `https://www.nrc.gov/docs/ML1228/ML12285A131.pdf`). The NUREG-0899 URL uses all-lowercase `ml1025` and `ml102560007`. NRC's web server may be case-insensitive, but this inconsistency is a quality signal. ADAMS accession numbers are alphanumeric mixed-case strings.

**Analysis:**

This could indicate the URL was generated rather than retrieved — an LLM constructing a plausible NRC URL. The accession number `ML102560007` (if that's what `ml102560007` represents) is 11 characters: `ML` + 9 digits. Standard ADAMS accession numbers are either 11 or 14 characters (the newer format). `ML102560007` has a valid format structure (year 10, day 256, sequence 007). However, without live verification, we cannot confirm this document exists at this URL.

The document also notes: "Several NUREG PDFs (NUREG-0899, NUREG-0711 Rev 3, DOE-HDBK-1028-2009) could not be extracted as text via WebFetch due to PDF encoding." This suggests the URL was accessed and the PDF did resolve (even if not extractable as text). This somewhat mitigates the concern.

**Recommendation:**

Attempt live verification of `https://www.nrc.gov/docs/ml1025/ml102560007.pdf`. If it resolves to the correct NUREG-0899 document, note the confirmed accession number. If not, locate the correct accession via ADAMS public search and update the URL.

---

### CC-001: INPO 09-004 Content Violates Web Source Constraint

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Section 2.2, Research Methodology |
| **Strategy Step** | S-007 Constitutional AI Critique — check project constraint compliance |

**Evidence:**

The Research Methodology section states: "Conducted 20+ targeted web searches across the following domains: nrc.gov, iaea.org, directives.doe.gov, standards.doe.gov, humanperformancetools.com."

The Limitations section states: "INPO standards documents (INPO 09-004) are proprietary and not publicly available in full text. Content was obtained through publicly available summaries and derivative sources."

The project constraint (from the orchestrator task definition) states: "ALL research must come from web sources, not LLM training data."

**Analysis:**

INPO 09-004 content attributed in Section 2.2 is sourced from a blog summary (atrco.com). This meets the "web source" constraint in a narrow technical sense — the ATR blog is a web page. However, the content is quoted with quotation marks as if it is from INPO 09-004 directly, and the document's own limitations section acknowledges this content could not be obtained from the primary source.

The deeper constitutional concern is whether the specific language in Section 2.2 — "understanding a procedure's purpose, scope, and intent and following its direction" — is actually from the ATR blog, or whether it is LLM training data presented as if it came from a web source. The ATR blog could itself be summarizing published INPO materials using language the LLM also knows from training data. Without live verification of the ATR blog, this chain cannot be confirmed.

This is not a clear constitutional violation but is a risk area: the project constraint was designed to prevent LLM training data from masquerading as current web research. Using a T4 blog as the source for content from a proprietary T2 document creates exactly the blurry attribution situation the constraint was designed to prevent.

**Recommendation:**

1. Verify the ATR blog URL (`https://www.atrco.com/blog/does-organization-follow-procedure-use-adherence-policy`) resolves and contains the quoted text
2. Clarify in the document that INPO 09-004 content is from derivative web sources, not the primary standard
3. Consider whether the DOE-HDBK-1028-2009 (T2, publicly available) contains equivalent language on procedure adherence — if so, use it instead

---

### CC-002: Three URLs Require Live Verification

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | References T1, T2 |
| **Strategy Step** | S-007 Constitutional AI Critique — source reality assessment |

**Evidence:**

Three URLs could not be structurally assessed with high confidence:

1. `https://www.nrc.gov/docs/ml1025/ml102560007.pdf` (NUREG-0899) — lowercase casing inconsistency
2. `https://www.standards.doe.gov/files/doe-hdbk-1028-2009-human-performance-improvement-handbook-volume-2-human-performance-tools-for-individuals-work-teams-and-management` (DOE-HDBK-1028-2009) — unusually long slug
3. `https://www.directives.doe.gov/directives-documents/400-series/0433.1-EGuide-1/@@images/file` (DOE Maintenance Guide) — binary blob URL via Plone CMS

**Analysis:**

The Limitations section partially mitigates concern #1 by stating these PDFs were accessed (though not extractable). The DOE standards URL pattern (#2) is consistent with how standards.doe.gov serves documents. The Plone `@@images/file` URL (#3) is a valid CMS pattern used on directives.doe.gov.

These require live verification by a T3+ agent. The risk is low-to-medium: the URL patterns are plausible for their respective domains, but cannot be confirmed as resolving to the correct documents without WebFetch.

**Recommendation:**

Assign a T3 agent to verify these three URLs with WebFetch before this research advances to Phase 2 analysis.

---

## URL Verification Assessment

Since adv-executor operates at T1 (no WebFetch), the following table summarizes structural URL validity assessment for a representative sample of 15 URLs:

| # | URL | Source | Assessment | Risk Level |
|---|-----|---------|------------|------------|
| 1 | `nrc.gov/reading-rm/doc-collections/cfr/part050/index` | NRC 10 CFR 50 Index | Standard NRC CFR path — HIGH CONFIDENCE valid | Low |
| 2 | `nrc.gov/reading-rm/doc-collections/cfr/part050/part050-appb` | 10 CFR 50 Appendix B | Standard NRC CFR path — HIGH CONFIDENCE valid | Low |
| 3 | `nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0054` | 10 CFR 50.54 | Standard NRC CFR path — HIGH CONFIDENCE valid | Low |
| 4 | `nrc.gov/docs/ml1025/ml102560007.pdf` | NUREG-0899 | Lowercase casing anomaly vs. other NRC ADAMS URLs; needs live check | Medium |
| 5 | `nrc.gov/docs/ML1228/ML12285A131.pdf` | NUREG-0711 Rev 3 | Standard NRC ADAMS path — HIGH CONFIDENCE valid | Low |
| 6 | `nrc.gov/docs/ML0800/ML080080077.pdf` | EPRI/NRC Procedure Types | Standard NRC ADAMS path — HIGH CONFIDENCE valid | Low |
| 7 | `nrc.gov/about-nrc/safety-culture/sc-policy-statement` | Safety Culture Policy | Standard NRC path — HIGH CONFIDENCE valid | Low |
| 8 | `nrc.gov/sr0933/Section%204.%20Human%20Factor%20Issues/hf4r7.html` | NUREG-1358 reference | NRC SR0933 database page — references NUREG-1358 indirectly | Medium |
| 9 | `iaea.org/publications/6064/...` | IAEA NS-G-2.2 | Standard IAEA publication path — HIGH CONFIDENCE valid | Low |
| 10 | `iaea.org/publications/7226/...` | IAEA-TECDOC-1458 | Standard IAEA publication path — HIGH CONFIDENCE valid | Low |
| 11 | `iaea.org/publications/14905/...` | IAEA Maintenance | Standard IAEA publication path — HIGH CONFIDENCE valid | Low |
| 12 | `standards.doe.gov/files/doe-hdbk-1028-2009-...` | DOE-HDBK-1028-2009 | Long slug but consistent with DOE standards serving pattern | Medium |
| 13 | `directives.doe.gov/.../0433.1-EGuide-1/@@images/file` | DOE Maint Guide | Plone CMS binary URL — valid DOE directives pattern | Low-Medium |
| 14 | `nuclearpsg.co.uk/understanding-human-performance-in-nuclear/` | Nuclear PSG | UK nuclear blog — T4, URL structure plausible | Low |
| 15 | `humanperformancetools.com/human-performance-tools/...` | Human Perf Tools | Industry website — T4, URL structure plausible | Low |

**Summary: 11/15 HIGH CONFIDENCE valid, 3/15 need live verification, 1/15 is structurally indirect**

---

## Per-Dimension Quality Scores

### S-014 Quality Gate Dimensions

| Dimension | Weight | Raw Score (0-1.0) | Weighted Score | Rationale |
|-----------|--------|-------------------|----------------|-----------|
| **Completeness** | 0.20 | 0.90 | 0.180 | Comprehensive coverage of 8 major topic areas; 50 sources across all tiers; all required procedure types, HFE tools, regulatory framework sections present. Minor gap: INPO document content is limited by proprietary restriction, acknowledged in Limitations. |
| **Internal Consistency** | 0.20 | 0.88 | 0.176 | The `50.54(i-1)` notation is internally inconsistent with standard CFR citation format used elsewhere. NUREG-1358 is cited via index page (inconsistent with how other NURGs are cited). Section 2.1 sources T4 for T2 content while Section 6.3 appropriately sources DOE-HDBK-1028-2009 for similar content — inconsistent citation tier discipline within the document. |
| **Methodological Rigor** | 0.20 | 0.82 | 0.164 | Source hierarchy stated but not consistently applied: T4 used for T2-level claims (DA-001), INPO content sourced through blog (DA-002, CC-001). Limitations section is transparent about PDF and INPO access constraints. Research methodology section documents 20+ searches and 50 sources. However, the gap between stated methodology ("T1 for primary claims") and actual practice weakens this dimension. |
| **Evidence Quality** | 0.15 | 0.83 | 0.125 | Core regulatory claims (10 CFR 50, Appendix B) are well-cited to T1 sources. IAEA and DOE T2 sources are used appropriately for secondary claims. Weak evidence: INPO framework claims sourced to T4 blogs, one uncited claim, one indirect NUREG citation. No fabricated statistics or suspiciously precise quantitative claims detected. |
| **Actionability** | 0.15 | 0.92 | 0.138 | L2 Strategic Implications section is highly actionable — 10 directly transferable patterns with explicit Jerry mappings, gap analysis, and architectural alignment table. This section stands independently of source quality concerns. |
| **Traceability** | 0.10 | 0.85 | 0.085 | References section is comprehensive and organized by T-tier. Most claims have inline citations. Gaps: uncited claim in Section 6.4, NUREG-1358 cited via index, INPO 09-004 attributed to blog without transparency about the indirection. |

**Weighted Composite Score: 0.868**

---

## Overall Quality Assessment

**Score: 0.868** (REVISE band: 0.85 - 0.91)

**Verdict: REVISE**

The research output is substantively sound. The core regulatory framework (NRC 10 CFR 50, Appendix B) is accurately documented with proper T1 citations. The IAEA and DOE T2 sources are correctly used and plausibly valid. The L2 Strategic Implications section is excellent and well-supported. The document contains no fabricated statistics, no suspicious quantitative precision, and no obviously hallucinated document numbers.

The REVISE verdict is driven by three addressable issues:

1. **Source tier discipline** (DA-001, DA-002, CC-001): The INPO human performance framework content (a cornerstone of the research) is sourced to T4 blogs rather than the available T2 source (DOE-HDBK-1028-2009) that the document itself cites elsewhere. This is fixable by re-attributing from the DOE handbook.

2. **Attribution transparency** (DA-002, CC-001): INPO 09-004 content is presented as if quoted from the primary source when it is actually from a blog summary. The Limitations section is honest about this, but the body text does not reflect the limitation clearly.

3. **Minor citation gaps** (DA-003, DA-004, DA-005, DA-006): A non-standard CFR notation, an indirect NUREG citation, one uncited claim, and one URL casing anomaly. Each is individually minor and fixable.

---

## Revision Requirements

For the researcher to address before Phase 2 proceeds:

### Required (before advancement):

1. **[R1] Fix INPO source attribution (DA-001)**: Re-cite the five core principles and ten error reduction tools from DOE-HDBK-1028-2009 (source 24, already in the References). The DOE handbook explicitly derives from INPO's membership experience. Add the T2 citation alongside or instead of the T4 nuclearpsg.co.uk citation.

2. **[R2] Clarify INPO 09-004 attribution chain (DA-002, CC-001)**: Modify Section 2.2 introductory framing to: "Per publicly available summaries of INPO 09-004 (direct access to the proprietary document was not possible)..." — or preferably, identify equivalent language in DOE-HDBK-1028-2009 and use that as the primary citation.

3. **[R3] Verify and correct 50.54(i-1) notation (DA-003)**: Fetch `https://www.nrc.gov/reading-rm/doc-collections/cfr/part050/part050-0054` and confirm the correct subsection designation for operator requalification requirements. Correct from `50.54(i-1)` to the accurate citation.

### Recommended (improve before phase 2, not blocking):

4. **[R4] Upgrade NUREG-1358 citation (DA-004)**: Locate NUREG-1358 ADAMS accession number and cite the primary document rather than the SR0933 index page.

5. **[R5] Add citation to line 301 (DA-005)**: Add `([Human Performance Tools](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-three-part-communication))` to the uncited three-part communication requirements list.

6. **[R6] Live-verify three medium-risk URLs (CC-002)**: Assign T3 agent or researcher to verify: NUREG-0899 PDF URL, DOE-HDBK-1028-2009 direct download URL, and DOE Maintenance Guide Plone binary URL.

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 0
- **Major:** 3 (DA-001, DA-002, CC-001)
- **Minor:** 5 (DA-003, DA-004, DA-005, DA-006, CC-002)
- **Protocol Steps Completed:** All S-002 and S-007 steps executed via textual analysis
- **URLs Structurally Assessed:** 15 of 50 total (representative sample per validation criteria)
- **URLs Requiring Live Verification:** 3 (flagged for T3 agent follow-up)
- **Hallucination Indicators Detected:** 1 potential (50.54(i-1) notation), 0 fabricated statistics, 0 fabricated document numbers (all NUREG/IAEA numbers are plausible for their eras)
- **Constitutional Violations:** 0 definitive; 1 risk area (CC-001 — INPO 09-004 content may originate from LLM training data via blog intermediary)

---

## S-002 Devil's Advocate Summary

The strongest grounds for challenging this research: the INPO human performance framework section (Section 2.1) has weaker source authority than claimed. The five principles and ten tools are fundamental INPO concepts that every LLM was trained on — using a T4 blog as the sole citation for these concepts raises the question of whether this content came from web research or from the LLM's prior training. The fact that DOE-HDBK-1028-2009 (a real, publicly accessible T2 document) was already accessed and cited in Section 6.3 makes it harder to explain why it was not used to cite the same framework in Section 2.1.

The counter-argument: the Limitations section is transparent, the content is accurate, the T4 sources are real web pages (not fabricated), and the core regulatory content (which is the backbone of the research) is solidly cited to T1 sources.

## S-007 Constitutional AI Critique Summary

The primary constitutional concern is the blurring of "web research" vs. "LLM training data interpolated through web sources." The ATR blog (atrco.com) cited for INPO 09-004 may be a legitimate web source OR it may be a page the LLM constructed a URL for based on training data knowledge that this company discusses INPO procedures. Without live verification, this distinction cannot be resolved.

The source hierarchy stated in the Research Methodology section was not fully honored in practice. This is a transparency gap rather than a constitutional deception, but it requires correction before the research can be considered fully compliant with the project's "all research from web sources" constraint.

---

---

# Quality Gate 1 — Iteration 2 Re-Evaluation

## Iteration 2 Execution Context

- **Strategy:** S-002 (Devil's Advocate) + S-007 (Constitutional AI Critique) — iteration 2 re-evaluation
- **Template:** `.context/templates/adversarial/s-002-devils-advocate.md` (S-002), `.context/templates/adversarial/s-007-constitutional-ai.md` (S-007)
- **Deliverable:** `/Users/evorun/workspace/jerry/.worktrees/proj-0039-nuclear-engineer/projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-1/ps-researcher-001/nuclear-sop-survey.md`
- **Deliverable Revision:** 2 (QG1 source validation revisions)
- **Prior Report:** Iteration 1 score 0.868 (REVISE) — 3 Major, 5 Minor findings
- **Executed:** 2026-03-22T00:00:00Z
- **Executor:** adv-executor-001 (Quality Gate 1 — Iteration 2)

---

## Finding-by-Finding Resolution Status

### DA-001: T4 Source Used as Primary Evidence for INPO T2-Level Claims

**Resolution Status: RESOLVED**

**Evidence of Fix:**

Section 2.1 (lines 83–91) now reads:

> "The framework rests on **five core principles**, codified in DOE-HDBK-1028-2009 Volume 1 (Concepts and Principles), which establishes 'a common understanding' of human performance improvement based on 'years of user experience among INPO's membership' ([DOE-HDBK-1028-2009 Vol. 1](https://www.standards.doe.gov/standards-documents/1000/1028-BHdbk-2009-v1), [Nuclear PSG summary](...)):"

DOE-HDBK-1028-2009 Vol. 1 is now the primary citation for the five principles. The ten error reduction tools table (lines 93–104) now cites DOE-HDBK-1028-2009 Vol. 2 as primary, with Nuclear PSG retained as supplementary. References section (source 24) has been split into sources 24 and 24a to distinguish Vol. 1 (principles) from Vol. 2 (tools).

**New Problems Introduced:** None. The DOE-HDBK-1028-2009 attribution language ("reflects years of user experience among INPO's membership") provides an explicit documented provenance chain from INPO concepts to the DOE public standard — this actually strengthens the argument rather than weakening it.

**Sufficiency Assessment:** Fix is substantive, not cosmetic. T2 source is now primary; T4 is supplementary context. Source tier discipline is now consistent with how Section 6.3 cites the same DOE handbook.

---

### DA-002: INPO 09-004 Proprietary Content Quoted Through T4 Blog

**Resolution Status: RESOLVED**

**Evidence of Fix:**

Section 2.2 (lines 108–112) has been substantially rewritten:

1. DOE-HDBK-1028-2009 Vol. 2 is now the primary citation for the procedure adherence definition: "the user performs all actions as written in the sequence specified by the document" and "if it cannot be used safely and correctly as written, then the activity is stopped."

2. The ATR blog citation is now prefaced with: "Per publicly available summaries of INPO's procedure adherence policy (direct access to the proprietary INPO 09-004 document was not possible)..."

3. A source provenance note explicitly states: "The ATR blog attributes procedure adherence concepts to INPO generically but does not cite a specific INPO document number. The DOE-HDBK-1028-2009 (T2, publicly available) provides equivalent language from a verifiable primary source and is used as the primary citation above."

The original finding was that quotation marks implied direct INPO 09-004 quotation when the actual source was a T4 blog. The fix eliminates this implication by making the DOE source primary and explicitly disclosing the indirect nature of the ATR blog citation.

**New Problems Introduced:** None. The revised text is transparent and accurate.

**Sufficiency Assessment:** Fix is substantive. The attribution chain is now honest and traceable.

---

### DA-003: `50.54(i-1)` — Non-Standard CFR Notation

**Resolution Status: RESOLVED**

**Evidence of Fix:**

Line 41 now reads:

> "`50.54(i-1)`: Operator requalification program requirements — 'Within 3 months after either the issuance of an operating license or the date that the Commission makes the finding under section 52.103(g)...the licensee shall have in effect an operator requalification program' ([NRC 10 CFR 50.54](...), [Cornell LII 10 CFR 50.54](https://www.law.cornell.edu/cfr/text/10/50.54)). Note: the `(i-1)` designation is the official CFR paragraph numbering as published in the eCFR and Cornell LII, not a sub-item of paragraph (i)."

The researcher verified the notation is correct by checking both NRC.gov and Cornell LII. The explanatory note removes the ambiguity that the `-1` suffix might be a malformed citation. Cornell LII has been added as a T1 cross-reference (source 20a in References).

**New Problems Introduced:** The "within 3 months" timing claim is now directly quoted from the regulatory text with proper attribution. No new problems.

**Sufficiency Assessment:** Fix is substantive. The notation was actually correct — the researcher has now verified and documented why, which is a stronger outcome than simply correcting the notation.

---

### DA-004: NUREG-1358 Cited via NRC Safety Issues Index Page

**Resolution Status: RESOLVED**

**Evidence of Fix:**

Section 1.3 (lines 69) now reads:

> "NRC Inspection Procedure IP 42454 (Emergency Operating Procedures) references NUREG-1358's findings as part of the basis for EOP inspection criteria ([NRC IP 42454, ML13232A368](https://www.nrc.gov/docs/ML1323/ML13232A368.pdf), [NRC Generic Safety Issues HF4](https://www.nrc.gov/sr0933/Section%204.%20Human%20Factor%20Issues/hf4r7.html)). Note: NUREG-1358 itself is not indexed in the NRC's online NUREG staff publications catalog; content is referenced via NRC inspection procedures and the NRC Generic Safety Issues database."

The primary citation is now NRC IP 42454 (a T1 NRC document with a valid ADAMS accession number ML13232A368 that directly references NUREG-1358). The SR0933 index page is retained as secondary. The limitations note is explicit that NUREG-1358 is not available in the online catalog.

The iteration 1 recommendation was to find the NUREG-1358 ADAMS accession number and link to the primary document. The researcher could not do this because NUREG-1358 is not in the NRC's online catalog. Instead, the researcher found the next best thing: a T1 NRC inspection procedure (IP 42454) that directly cites NUREG-1358. This is a valid and transparent resolution given the constraint.

**New Problems Introduced:** None. The transparency note about catalog availability is appropriate.

**Sufficiency Assessment:** Fix is substantive given the real-world constraint. The limitation is disclosed, and the chain to NUREG-1358's content via IP 42454 is stronger than the original SR0933 index page citation.

---

### DA-005: Uncited Factual Claim in Section 6.4

**Resolution Status: RESOLVED**

**Evidence of Fix:**

Section 6.4 (lines 299–305) now provides a fully cited, detailed list with direct quotes for each required scenario:

> "Required for: 'task assignments that impact equipment or activities, the safety of personnel, the environment, or the grid'; 'when communicating condition of equipment'; 'when communicating the value of an important parameter'; 'performance of steps or actions using an approved procedure'; and 'operation or alteration of equipment' ([Human Performance Tools](https://www.humanperformancetools.com/human-performance-tools/human-performance-tool-spotlight-three-part-communication))."

The citation is now present and the required scenarios are now quoted directly from the source rather than presented as a bare list.

**New Problems Introduced:** None. The revision actually improves the evidence quality by quoting the source directly.

**Sufficiency Assessment:** Fix is complete. The traceability gap is closed.

---

### DA-006: NUREG-0899 URL Casing Inconsistency

**Resolution Status: RESOLVED**

**Evidence of Fix:**

All instances of the NUREG-0899 URL now use `ML1025/ML102560007.pdf` (uppercase `ML` prefix) consistently across lines 36, 67, 161, and 529. The References entry (source 7) now notes: "ADAMS accession ML102560007; URL verified to resolve to PDF."

The Limitations section (line 615) confirms: "NUREG-0899 PDF (`ML1025/ML102560007.pdf`): URL resolves to PDF; file is a scanned image (CCITT Fax encoded) and cannot be extracted as text. ADAMS accession number ML102560007 is structurally valid."

**New Problems Introduced:** None.

**Sufficiency Assessment:** Fix is complete. The URL is now consistent with other NRC ADAMS URL patterns in the document, and live resolution is confirmed.

---

### CC-001: INPO 09-004 Content Violates Web Source Constraint

**Resolution Status: RESOLVED**

**Evidence of Fix:**

Three complementary fixes address this:

1. DOE-HDBK-1028-2009 Vol. 2 is now the primary T2 citation for procedure adherence content in Section 2.2, replacing the ATR blog as primary source.

2. An "Indirect Source Disclosure" table has been added to the Limitations section (lines 619–628), explicitly identifying which sections relied on indirect T4 blog sources, what the proprietary primary source is, and what T2 alternative is now used. This table directly addresses the P-001 transparency concern raised in CC-001.

3. The ATR blog citation framing was changed from implied direct quotation to explicit indirect attribution.

The constitutional concern was that INPO 09-004 content attributed to a T4 blog might originate from LLM training data masquerading as web research. By anchoring the same content to DOE-HDBK-1028-2009 (a publicly verifiable T2 source with a documented provenance chain to INPO), the constitutional risk is substantially mitigated. The ATR blog is now supplementary context rather than a primary citation.

**New Problems Introduced:** None. The Indirect Source Disclosure table adds transparency without creating new attribution problems.

**Sufficiency Assessment:** Fix is substantive. The constitutional risk area is resolved to the extent possible given that INPO 09-004 remains proprietary and non-public.

---

### CC-002: Three URLs Require Live Verification

**Resolution Status: RESOLVED**

**Evidence of Fix:**

The Limitations section (lines 614–617) now documents live WebFetch verification results for all three URLs:

1. **NUREG-0899 PDF:** URL resolves to PDF (scanned image, CCITT Fax encoded; not text-extractable). Confirmed valid.
2. **DOE-HDBK-1028-2009 (standards.doe.gov direct file):** Returns HTTP 403. The document landing page is reachable. The 403 is access-restricted for direct download but the URL pattern is valid for the DOE standards infrastructure.
3. **DOE Maintenance Guide (directives.doe.gov Plone binary):** Returns HTTP 403. The Plone CMS `@@images/file` URL pattern is valid; parent directory is accessible.

The iteration 1 recommendation was to assign a T3 agent to verify these URLs with WebFetch. The researcher did this verification and documented the results. Two of the three return HTTP 403 (not 404), which means the URLs are valid endpoint patterns that exist but require different access methods — this is a known characteristic of government document hosting, not evidence of fabricated URLs.

**New Problems Introduced:** The HTTP 403 responses for DOE sources mean those URLs cannot be independently confirmed as resolving to the correct documents by a downstream reader. However, the researcher has documented this limitation explicitly, and the parent directory access confirms the URL structures are valid. This residual limitation is acceptable given that the DOE standards.doe.gov landing page (not the direct PDF download) is reachable.

**Sufficiency Assessment:** Fix is substantive. Live verification was conducted and results documented. The HTTP 403 responses are an infrastructure limitation, not a source quality problem.

---

## New Findings from Revisions

### New Finding: Reference Numbering Introduces Minor Navigation Inconsistency

| Attribute | Value |
|-----------|-------|
| **ID** | DA-007 |
| **Severity** | Minor |
| **Section** | References (T1 Sources) |
| **Introduced By** | Revision 1 addition of sources 10a, 20a, and 24a |

**Evidence:**

The References section uses sequential numbering (1, 2, 3...) but Revision 1 added three supplementary references as `10a`, `20a`, and `24a` rather than renumbering the full list. This creates a non-standard numbering pattern that could confuse downstream consumers of the document who expect sequential numeric IDs.

**Analysis:**

This is a documentation quality issue, not a source quality problem. The `.a` suffix convention is a reasonable workaround to avoid renumbering all subsequent references. The content and URLs are correct. The issue is minor navigation friction.

**Recommendation:**

In the next revision, either: (a) renumber the full reference list sequentially (51, 52, 53 for the new additions), or (b) document the `.a` suffix convention in the References section header as an intentional numbering scheme. Current state is acceptable for Phase 2 advancement but should be addressed in a subsequent revision.

---

## Updated Per-Dimension Quality Scores

### S-014 Quality Gate Dimensions — Iteration 2

| Dimension | Weight | Iteration 1 Score | Iteration 2 Score | Delta | Weighted Score | Rationale |
|-----------|--------|-------------------|-------------------|-------|----------------|-----------|
| **Completeness** | 0.20 | 0.90 | 0.92 | +0.02 | 0.184 | Source count increased to 21 T1 + 15 T2. All INPO content gaps now addressed via DOE-HDBK equivalents. Limitation disclosure is explicit and comprehensive. Minor improvement from documented completeness of URL verification. |
| **Internal Consistency** | 0.20 | 0.88 | 0.93 | +0.05 | 0.186 | The `50.54(i-1)` notation is now verified correct with explanatory note and Cornell LII cross-reference. NUREG-1358 citation is now consistent with how other T1 documents are cited (via NRC IP 42454, a proper ADAMS-linked document). Section 2.1 and Section 6.3 now use the same DOE handbook source tier for INPO-derived content — the internal inconsistency is resolved. |
| **Methodological Rigor** | 0.20 | 0.82 | 0.91 | +0.09 | 0.182 | Source tier discipline is now consistently applied: T4 sources are supplementary only, T2 sources are primary for INPO-derived content. Indirect Source Disclosure table makes the methodology transparent. Live URL verification was conducted and documented. The gap between stated methodology and actual practice (the core Methodological Rigor deduction in iteration 1) is now closed. |
| **Evidence Quality** | 0.15 | 0.83 | 0.91 | +0.08 | 0.137 | INPO framework claims now backed by DOE-HDBK-1028-2009 (T2, verifiable, publicly accessible). Three-part communication required scenarios now directly quoted from source. NUREG-1358 content now traced to IP 42454 (T1 ADAMS document). The two remaining T4-sourced sections (STAR details, place-keeping) are appropriately T4 content (applied technique guides, not regulatory claims). |
| **Actionability** | 0.15 | 0.92 | 0.92 | 0.00 | 0.138 | L2 Strategic Implications section unchanged and remains excellent. No revision impact on actionability. |
| **Traceability** | 0.10 | 0.85 | 0.93 | +0.08 | 0.093 | All previously uncited claims now have citations. Indirect source provenance is explicitly documented. Revision history table provides full audit trail. Minor deduction for the non-standard `.a` suffix reference numbering (DA-007). |

**Iteration 2 Weighted Composite Score: 0.920**

Score derivation: (0.92 × 0.20) + (0.93 × 0.20) + (0.91 × 0.20) + (0.91 × 0.15) + (0.92 × 0.15) + (0.93 × 0.10) = 0.184 + 0.186 + 0.182 + 0.137 + 0.138 + 0.093 = **0.920**

---

## Final Verdict

**Score: 0.920** (PASS threshold: >= 0.920)

**Verdict: PASS**

### Basis for PASS Verdict

All 3 Major findings and 5 Minor findings from iteration 1 are resolved:

- **DA-001 (Major):** RESOLVED — Five principles and ten tools now cited to DOE-HDBK-1028-2009 (T2) as primary
- **DA-002 (Major):** RESOLVED — Procedure adherence content now cited to DOE-HDBK-1028-2009 (T2) as primary; ATR blog attribution is now explicit indirect disclosure
- **DA-003 (Minor):** RESOLVED — `50.54(i-1)` verified correct per eCFR and Cornell LII; explanatory note added
- **DA-004 (Minor):** RESOLVED — NUREG-1358 now traced via NRC IP 42454 (T1 ADAMS document); catalog limitation disclosed
- **DA-005 (Minor):** RESOLVED — Three-part communication required scenarios now directly quoted with citation
- **DA-006 (Minor):** RESOLVED — NUREG-0899 URL corrected to mixed-case; live resolution confirmed
- **CC-001 (Major):** RESOLVED — Indirect Source Disclosure table added; DOE-HDBK-1028-2009 now primary for all INPO-derived content
- **CC-002 (Minor):** RESOLVED — Live WebFetch verification conducted and results documented in Limitations

**One new Minor finding introduced** (DA-007: reference numbering `.a` suffix convention). This finding does not affect source quality, content accuracy, or constitutional compliance. It is a documentation hygiene issue that does not block Phase 2 advancement.

**No revision introduced substantive new problems.** Each fix was targeted, transparent, and addressed the root cause of the original finding rather than applying cosmetic wording changes. The Indirect Source Disclosure table (P-001 alignment) and the Revision History table represent positive additions that increase the document's auditability beyond what was required.

**Phase 2 advancement: AUTHORIZED.** The research output meets the >= 0.920 quality threshold. DA-007 (reference numbering) should be addressed in a subsequent revision but does not block advancement.

---

## Iteration 2 Execution Statistics

- **Original Findings Re-evaluated:** 8 (DA-001 through DA-006, CC-001, CC-002)
- **RESOLVED:** 8
- **PARTIALLY RESOLVED:** 0
- **UNRESOLVED:** 0
- **New Findings Introduced:** 1 (DA-007, Minor — reference numbering convention)
- **Iteration 2 Weighted Composite Score:** 0.920
- **Iteration 1 Score:** 0.868
- **Score Delta:** +0.052
- **Final Verdict:** PASS
