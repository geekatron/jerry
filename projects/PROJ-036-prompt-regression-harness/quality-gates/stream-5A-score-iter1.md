# Quality Score Report: Security Assessment — Stream 5A (PROJ-036)

## L0 Executive Summary

**Score:** 0.835/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.78)

**One-line assessment:** The security assessment demonstrates strong technical depth and evidence quality with specific file:line findings, but falls below the C4 threshold of 0.94 due to a substantive threat-mapping inconsistency in F-001, incomplete OWASP Top 10 coverage (6 of 10 categories assessed), methodological gaps in CWE Top 25 application, and traceability errors that map findings to the wrong threat IDs.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-036-prompt-regression-harness/security/security-assessment.md`
- **Deliverable Type:** Analysis (Security Assessment)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **Custom Threshold:** 0.94 (C4 elevated from H-13 baseline of 0.92)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Context Files Validated:**
  - `projects/PROJ-036-prompt-regression-harness/requirements/harness-requirements.md` (FR-023 through FR-025)
  - `projects/PROJ-036-prompt-regression-harness/design/system-design.md` (Part 3: threat model, MC-01 through MC-14)
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 1

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.835 |
| **C4 Custom Threshold** | 0.94 |
| **H-13 Standard Threshold** | 0.92 |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor report provided) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.164 | All 14 MC controls assessed; only 6 of 10 OWASP categories covered; ASVS V1/V2 absent |
| Internal Consistency | 0.20 | 0.82 | 0.164 | F-001 maps to T-02 (YAML injection) but the actual gap is in the DeepEval adapter, a distinct injection surface; summary count annotation "1 PARTIAL-CRITICAL" is non-standard |
| Methodological Rigor | 0.20 | 0.84 | 0.168 | ASVS 5.0 V5/V6/V7/V8 applied; STRIDE used via design document; CWE Top 25 checklist claimed but no systematic checklist evidence shown |
| Evidence Quality | 0.15 | 0.89 | 0.134 | All 9 findings include specific file:line citations with verbatim code excerpts; supply chain SHA hashes verified |
| Actionability | 0.15 | 0.85 | 0.128 | Priority-ordered P-1 through P-10 table with effort estimates; code remediation examples in F-001 through F-008; P-6 lacks line-level schema structure; UV version pinning omits target version |
| Traceability | 0.10 | 0.78 | 0.078 | F-001 maps to T-02 (YAML injection), but the gap is in deepeval_adapter.py which processes DeepEval inputs, not YAML test case vars; F-005 mapped to T-02 where T-06 or T-07 would be more precise; MC-28 used in OWASP table without being in the MC-01 through MC-14 scope |
| **TOTAL** | **1.00** | | **0.835** | |

**Arithmetic verification:**
- Completeness: 0.82 × 0.20 = 0.1640
- Internal Consistency: 0.82 × 0.20 = 0.1640
- Methodological Rigor: 0.84 × 0.20 = 0.1680
- Evidence Quality: 0.89 × 0.15 = 0.1335
- Actionability: 0.85 × 0.15 = 0.1275
- Traceability: 0.78 × 0.10 = 0.0780
- **Sum: 0.164 + 0.164 + 0.168 + 0.1335 + 0.1275 + 0.078 = 0.835**

---

## Detailed Dimension Analysis

### Completeness (0.82/1.00)

**Evidence:**

The Threat Model Coverage Matrix covers all 14 MC controls (MC-01 through MC-14) as required, with specific IMPLEMENTED / PARTIAL / MISSING verdicts supported by code evidence. This is the strongest completeness element.

The OWASP Alignment Table covers six categories: A01 (Broken Access Control), A03 (Injection), A04 (Insecure Design), A05 (Security Misconfiguration), A07 (Identification and Authentication Failures), A08 (Software and Data Integrity Failures). This leaves four OWASP Top 10 categories unaddressed:
- **A02:2021 Cryptographic Failures** — not assessed, despite F-009 touching hash truncation and the system handling API keys
- **A06:2021 Vulnerable and Outdated Components** — promptfoo npm dependency supply chain is partially covered in the Supply Chain section but not mapped to the OWASP table
- **A09:2021 Security Logging and Monitoring Failures** — F-004 touches logging inadequacy but no OWASP mapping
- **A10:2021 Server-Side Request Forgery** — not assessed; the promptfoo `file://` protocol handler (T-07) is relevant to SSRF-adjacent risks

The self-review S-010 claims "ASVS Coverage — ASVS V5, V6, V7 addressed" and omits V1 (Architecture) and V2 (Authentication), which are relevant to key management and workflow trust decisions. Ten implementation files are confirmed as reviewed (listed in the S-010 completeness check).

**Gaps:**
1. Four OWASP categories unaddressed without documented justification for exclusion
2. ASVS V1 (Architecture) and V2 (Authentication) not covered despite key management decisions being in scope
3. No coverage of the T-40 threat (adversarial near-zero-variance bypass) in the findings section, despite T-40 being listed as a top-9 risk in the design threat model

**Improvement Path:** Add OWASP A02, A06, A09, A10 assessments, or document explicitly why each is out of scope. Add at least an informational finding on T-40 (statistical input validation bypass) since the design identifies it as one of the highest-priority threats.

---

### Internal Consistency (0.82/1.00)

**Evidence:**

The CVSS base scores are internally consistent with severity labels: F-002 (High, CVSS 7.4), F-001 (High, CVSS 6.5), F-003 (Medium, CVSS 5.3), F-004 (Medium, CVSS 4.3), F-005 (Medium, CVSS 4.6), F-006 (Low, CVSS 3.1), F-007 (Low, CVSS 2.5), F-008 (Low, CVSS 3.7), F-009 (Info, CVSS 0.0). This progression is plausible and internally coherent.

**Specific inconsistencies identified:**

1. **F-001 threat mapping inconsistency:** F-001 is titled "MISSING Input Sanitization for Prompt Injection (MC-02)" and the attribute table maps it to "T-02 (YAML injection, Likelihood=H, Impact=H, Risk=High)." However, the finding describes the `deepeval_adapter.py` `evaluate_batch()` method passing prompt and output strings directly to DeepEval. T-02 in the design threat model is "Attacker injects prompt injection payload into YAML `vars.user_query` field, causing the LLM to produce manipulated outputs that bias scores." These are different surfaces — T-02 is the YAML input injection point; the finding is about the DeepEval evaluation adapter. The MC-02 control is assigned in the design to "Input sanitization layer strips known injection patterns," which is correctly identified as the missing control. The threat ID mapping is imprecise.

2. **Summary count annotation:** The control matrix summary states "7 IMPLEMENTED, 4 PARTIAL, 2 MISSING, 1 PARTIAL-CRITICAL (MC-02 missing sanitization with HIGH impact)." Counting the matrix: MC-01=PARTIAL, MC-02=MISSING, MC-03=PARTIAL, MC-04=IMPLEMENTED, MC-05=PARTIAL, MC-06=PARTIAL, MC-07=IMPLEMENTED, MC-08=MISSING, MC-09=IMPLEMENTED, MC-10=IMPLEMENTED, MC-11=IMPLEMENTED, MC-12=IMPLEMENTED, MC-13=IMPLEMENTED, MC-14=IMPLEMENTED. Tally: 7 IMPLEMENTED, 4 PARTIAL, 2 MISSING. The "1 PARTIAL-CRITICAL" description is not a separate entry — MC-02 is already counted as MISSING, making the summary misleadingly suggest 14 + 1 = 15 statuses for 14 controls.

3. **OWASP table references MC-28** (Fork PR secret isolation, A01 assessment) which is outside the MC-01 through MC-14 scope of the threat model coverage matrix. This is not wrong — MC-28 is a real control in the design — but it is inconsistent with the stated scope of the threat model coverage matrix section.

**Improvement Path:** Correct F-001's threat mapping to identify the specific threat that matches the DeepEval adapter injection surface (a T-02 variant or a new threat ID if one exists in the full 40-threat model). Revise the summary count to remove the "1 PARTIAL-CRITICAL" annotation or explain its distinct meaning.

---

### Methodological Rigor (0.84/1.00)

**Evidence:**

The methodology statement is substantive: "Manual code review with data flow tracing, CWE Top 25 2025 checklist, OWASP ASVS 5.0 V5/V6/V7/V8, threat model correlation (MC-01 through MC-14)." CVSS 3.1 base scores are computed for all 9 findings. The assessment correctly applies STRIDE-based threat correlation by referencing design-document threat IDs. Supply chain assessment follows a structured format covering GHA actions, Docker, Python (UV), and npm supply chains.

The OWASP ASVS coverage is applied correctly for the categories addressed: V5 (F-001, F-003 input validation), V6 (F-009 hash truncation), V7 (F-004 exception swallowing). The Docker security assessment follows established hardening checklists (non-root user, capability dropping, read-only filesystem, no-new-privileges).

**Methodological gaps:**

1. **CWE Top 25 2025 checklist** is claimed as a methodology input, but only 7 CWE identifiers appear across all findings (CWE-20, CWE-1395, CWE-390, CWE-693, CWE-840, CWE-327, CWE-1059). No evidence is provided that a full CWE Top 25 checklist was systematically walked — a common rigor shortfall where the checklist is named but not shown as applied. For a C4 assessment, the CWE Top 25 application should be evidenced with explicit "not applicable" annotations for each non-covered CWE.

2. **OWASP alignment table** covers 6 of 10 categories without documenting which 4 were excluded and why. For a rigorous assessment, excluded categories should appear in the table with "NOT IN SCOPE" or "NOT APPLICABLE" annotations and rationale.

3. **T-40 (near-zero-variance statistical bypass)** is identified as a top-9 threat in the design document's STRIDE matrix (ranked #7 by DREAD score 6.2, tied with T-07) but receives no finding in the assessment. The assessment references `stats.py`'s `_validate_score_array()` in F-004 as providing "some protection" but does not formally assess whether the adversarial score sequence protection is complete.

**Improvement Path:** Evidence the CWE Top 25 checklist application with a table showing each CWE and its assessment result (APPLICABLE/NOT APPLICABLE/FINDING). Add excluded OWASP categories to the alignment table with scope justification. Add a finding or explicit "NOT FINDING" note for T-40.

---

### Evidence Quality (0.89/1.00)

**Evidence:**

This is the strongest dimension. All nine findings (F-001 through F-009) include:
- Specific file paths (`jerry/testing/evaluation/deepeval_adapter.py`, `jerry/testing/baselines/store.py`, etc.)
- Line number citations (F-001: lines 251-384, 329-331; F-002: lines 34-39, 212-218; F-003: lines 410-432, 263-290)
- Verbatim code excerpts demonstrating the exact vulnerability
- Side-by-side comparison in F-003 showing the weaker `store.py` validation against the stronger `version_keys.py` validation

The supply chain section provides specific GitHub Actions SHA digests (e.g., `11bd71901bbe5b1630ceea73d27597364c9af683` for `actions/checkout`), which demonstrates actual code review rather than documentation-only assessment.

The container security assessment lists specific Dockerfile line numbers for both positive and negative findings.

**Minor gaps:**
- F-001 cites "lines 251-384" and separately "lines 199-249" — two large ranges without pinning the exact starting point of the missing sanitization logic. The excerpt at 329-331 is precise, but the range descriptions suggest the reviewer read broad sections rather than pinpointing the specific entry path.
- The UV version setup in the `setup-uv` action uses `version: "latest"` (Supply Chain section). This is flagged correctly but the specific line number in the smoke workflow is not cited (only described).

**Improvement Path:** These are minor gaps. Pinning the exact line where sanitization should be inserted (rather than the range of the method) would increase precision. Adding the smoke workflow line number for the `version: "latest"` UV setup would round out the supply chain evidence.

---

### Actionability (0.85/1.00)

**Evidence:**

The priority-ordered recommendations table (P-1 through P-10) clearly labels P-1 and P-2 as "pre-production blockers." Effort estimates are provided for each item (Low/Medium with time ranges). Eight of nine findings include concrete code remediation examples with syntactically plausible Python or Dockerfile snippets.

F-001 remediation provides a specific `_sanitize_input()` function with byte-length enforcement and regex injection pattern detection. F-002 remediation gives the exact Docker command sequence needed to obtain a digest. F-003 remediation gives the exact import and replacement call. F-007 remediation gives both pip-removal and multi-stage build alternatives.

**Actionability gaps:**

1. **P-6 (PARTIAL controls: MC-01/MC-03/MC-05/MC-06):** The recommendation is "Implement the `tests/prompt-regression/schemas/test-case.schema.json` file and conftest.py validation." This does not specify the schema structure, the threshold minimum values to enforce (which were defined in the design document's threat model as `minimum` constraints on threshold values), or the conftest.py implementation pattern. An engineer receiving this recommendation cannot begin implementation without consulting additional context.

2. **P-7 (Supply chain — UV version pinning):** "Replace `version: \"latest\"` with a specific version string" — the remediation does not identify which UV version to pin to (e.g., the current stable release at time of assessment). For automated DevSecOps remediation, the target version should be specified.

3. **Network allowlist recommendation** (Container Security section): The narrative suggests adding a network policy restricting the Standard/Full containers to `api.anthropic.com` only, but this does not appear in the P-1 through P-10 priority table and has no tracking number. Actionable recommendations buried in narrative without a priority number risk being overlooked.

**Improvement Path:** Add the schema field structure (or reference the design document section containing it) to P-6. Identify the target UV version for P-7. Promote the network policy recommendation to a numbered entry in the priority table.

---

### Traceability (0.78/1.00)

**Evidence:**

Most findings correctly trace to threat IDs and MC controls from the design document. FR-023 (UV-only execution), FR-024 (Langfuse observability), and FR-025 (Docker isolation) are referenced in the appropriate findings. The MC control cross-references are accurate for F-002 (MC-08), F-004 (contracts.md Section D), F-005 (MC-01), F-006 (MC-09), F-008 (MC-22).

**Traceability errors identified:**

1. **F-001 maps to T-02 incorrectly:** T-02 in the design is "Attacker injects prompt injection payload into YAML `vars.user_query` field." The finding describes `deepeval_adapter.py`'s failure to sanitize inputs to the DeepEval LLM judge. The DeepEval adapter is a separate attack surface from the YAML test input layer. The correct threat context would be a DeepEval-specific injection threat (the design's 40-threat model includes threats numbered into the T-30s and T-40s; a T-2x or T-3x may be the correct reference, or the assessment should acknowledge this is an unmodeled threat). Citing T-02 for a different attack surface is a material traceability error.

2. **F-005 maps to T-02 (YAML injection variant) and T-03:** F-005 describes `AGENT_ID` not being validated against the `COVERED_AGENTS` allowlist before Docker execution. T-02 is YAML `vars.user_query` injection; T-03 is modification of `assert.threshold` values. Neither maps precisely to CI workflow environment variable injection. T-06 (DoS via unlimited test cases) or T-07 (promptfoo `file://` exploit via path traversal) would be more accurate if path separator characters are the concern, or this finding could acknowledge it maps to an unspecified T-0x threat not individually enumerated in the threat model.

3. **FR references inconsistent:** F-004 references "contracts.md Section D" — this document is not identified in the assessment's context files, the requirements specification, or the design document's Evidence Traceability section. This is an unverifiable reference.

4. **MC-28 scope creep:** The OWASP table's A01 assessment cites "MC-28 (Fork secret isolation)" correctly, but MC-28 is outside the MC-01 through MC-14 scope that the assessment header defines as its threat model coverage scope. The scope definition should either be expanded to MC-01 through MC-40, or the reference should be removed from the OWASP table.

**Improvement Path:** Correct F-001's threat ID to the appropriate T-xx that matches DeepEval adapter injection (or explicitly state it is an unmodeled threat). Correct F-005's threat mapping. Identify `contracts.md` in the context files or replace with a verifiable reference. Clarify whether the assessment scope is MC-01 through MC-14 or MC-01 through MC-40.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.78 | 0.88 | Correct F-001 threat ID: T-02 maps to YAML vars injection, not DeepEval adapter injection. Identify the correct threat (T-xx from the full 40-threat model) or explicitly flag as an unmodeled injection surface. Correct F-005 mapping similarly. Resolve the `contracts.md` reference to a verifiable document. |
| 2 | Completeness | 0.82 | 0.90 | Add OWASP A02 (Cryptographic Failures — key management), A06 (Vulnerable/Outdated Components — promptfoo npm supply chain), A09 (Security Logging/Monitoring — F-004 logging gap), A10 (SSRF — T-07 file:// protocol risk). Add a finding or explicit NOT-FINDING for T-40 (statistical bypass), which the design identifies as a top-9 threat. |
| 3 | Internal Consistency | 0.82 | 0.90 | Fix the summary count annotation: "1 PARTIAL-CRITICAL" is not a distinct status category — MC-02 is already counted as MISSING. Remove or clarify this annotation. Explain MC-28 reference in OWASP table relative to the MC-01 through MC-14 stated scope. |
| 4 | Methodological Rigor | 0.84 | 0.91 | Evidence the CWE Top 25 2025 checklist application: add a table or appendix mapping each of the Top 25 CWEs to APPLICABLE/NOT APPLICABLE/FINDING status. Without this evidence, the methodology claim is unverifiable. Add T-40 assessment even if only to document why the existing `stats.py` validation is sufficient. |
| 5 | Actionability | 0.85 | 0.91 | P-6: Add the JSON Schema field structure for `test-case.schema.json` (minimum threshold constraints from design document threat model). P-7: Specify the target UV version. Promote network policy recommendation to a numbered priority entry. |
| 6 | Evidence Quality | 0.89 | 0.93 | Pin the exact insertion point for F-001 sanitization (specific line before `LLMTestCase` construction). Add smoke workflow line number for UV `version: "latest"` finding. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific quotes and findings
- [x] Uncertain scores resolved downward (Completeness: 0.82 not 0.85 due to OWASP coverage gap; Traceability: 0.78 not 0.82 due to two material threat ID mapping errors)
- [x] First-draft calibration considered: this is iteration 1; score of 0.835 is within the expected 0.80-0.90 range for a technically strong but not yet polished C4 assessment
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] F-001 threat mapping error counted against both Internal Consistency AND Traceability (it is a genuine error visible in both dimensions, not double-counted in the composite — each dimension reflects a separate quality concern)

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.835
threshold: 0.94
weakest_dimension: Traceability
weakest_score: 0.78
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Correct F-001 threat ID from T-02 (YAML injection) to the appropriate DeepEval adapter threat or document as unmodeled surface"
  - "Add OWASP A02, A06, A09, A10 coverage or explicit scope exclusion justification"
  - "Fix summary count annotation (1 PARTIAL-CRITICAL is not a distinct status)"
  - "Evidence CWE Top 25 2025 checklist with per-CWE APPLICABLE/NOT APPLICABLE table"
  - "Add T-40 statistical bypass assessment (top-9 design threat, not addressed in findings)"
  - "Resolve contracts.md reference to a verifiable document"
  - "Specify target UV version in P-7 remediation"
```

---

*Score report produced by: adv-scorer*
*Scoring date: 2026-03-07*
*Deliverable iteration: 1*
*Report version: 1.0*
