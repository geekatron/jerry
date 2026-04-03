# Quality Score Report: Claude Code Schema Validation Deliverable Set (C4 Re-Score)

## L0 Executive Summary

**Score:** 0.823/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.72)
**One-line assessment:** Strong post-remediation deliverable set with four documented, specific defects — a stale gap analysis row, a security review that did not reconcile against the v1.1.0 schema changes it was supposed to verify, a missing negative test for the reserved-word fix, and an unreconciled severity count discrepancy between two security documents — that collectively prevent acceptance.

---

## Scoring Context

- **Deliverable Set:** 6 artifacts (2 schemas, 1 test suite, 1 gap analysis, 1 security review, 1 vulnerability assessment)
- **Deliverable Paths:**
  - `docs/schemas/claude-code-frontmatter-v1.schema.json` (v1.1.0)
  - `docs/schemas/claude-code-skill-frontmatter-v1.schema.json` (v1.1.0)
  - `tests/schemas/test_frontmatter_schemas.py` (34 tests)
  - `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-003-gap-analysis-refinement/gap-analysis.md`
  - `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-004-schema-remediation/security-review-findings.md`
  - `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-004-schema-remediation/vulnerability-assessment.md`
- **Deliverable Type:** Analysis + Design (schema artifacts with supporting analysis)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.79 (first C4 review)
- **Scored:** 2026-03-26T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.823 |
| **Prior Score** | 0.79 |
| **Delta** | +0.033 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (no adv-executor reports available; scored from direct artifact inspection) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.88 | 0.176 | All 16 agent + 17 skill fields addressed; all 4 v1.0.0 CRITICAL/HIGH gaps resolved; 34 tests (positive, negative, roundtrip, integrity); but gap analysis still marks "No validation test suite" as OPEN when test suite is delivered in this set |
| Internal Consistency | 0.20 | 0.72 | 0.144 | Security review (0 Critical, 3 High) and vulnerability assessment (2 Critical, 3 High) are not reconciled; gap analysis stale row contradicts delivered test suite; agent schema `additionalProperties: true` description promises flagging that the schema does not perform (FIND-005 in security review, unresolved in v1.1.0) |
| Methodological Rigor | 0.20 | 0.86 | 0.172 | Multi-layered methodology: ASVS + CWE + CVSS + PTES + BDD; live roundtrip tests catch drift; scope/limitations and maintenance sections present; gap: no negative test case verifying the reserved-word `not` constraint actually rejects "claude" or "anthropic" |
| Evidence Quality | 0.15 | 0.88 | 0.132 | Line-level citations in security review; proof-of-concept YAML payloads in vulnerability assessment; ASVS chapter + CWE IDs per finding; March 2026 source URLs in schema description; minor gap in direct citation of upstream research artifacts |
| Actionability | 0.15 | 0.78 | 0.117 | Remediation tables with effort estimates and copy-paste JSON Schema snippets are excellent; but reader confusion persists: FIND-001/FIND-002 in the security review flag the reserved-word bypass as unresolved, while the v1.1.0 schema already contains the `allOf/not` fix — it is unclear whether these findings require action or are already closed |
| Traceability | 0.10 | 0.82 | 0.082 | Schema `$id` URIs pinned to March 2026 source; test file cites EN-003, H-20, H-34; gap analysis table links every field to source; security review cites CWE + ASVS + affected line for each finding; gap: no test exercises the reserved-word fix that is the stated primary v1.1.0 security change |
| **TOTAL** | **1.00** | | **0.823** | |

---

## Detailed Dimension Analysis

### Completeness (0.88/1.00)

**Evidence:**
The agent schema covers all 16 fields documented in the CLAUDE.md `agent-development-standards.md` table plus two additional observed-in-practice fields (`effort`, `initialPrompt`). The skill schema covers all 17 fields including Agent Skills Standard fields (`license`, `compatibility`, `metadata`). The gap analysis provides a complete resolution table with v1.1.0 status for every identified gap. The test suite delivers 5 agent positive tests, 10 agent negative tests, 7 skill negative tests, 5 live roundtrip tests, and 7 schema integrity tests totaling 34 tests, all confirmed passing. The security review covers the schema with ASVS V1 and V5 chapters and evaluates 14 CWE checklist items.

**Gaps:**
The gap analysis "Shared Issues" table (line 104) still contains the row: "No validation test suite | Both | Schema regression undetectable | OPEN -- follow-up enabler needed". The test suite is delivered as part of this same deliverable set. This OPEN row was not updated to RESOLVED. This is not a missing deliverable but it does mean the gap analysis does not accurately describe the current state of the work. A reader who only reads the gap analysis will conclude a validation test suite does not exist.

**Improvement Path:**
Update the gap analysis "No validation test suite" row status from OPEN to RESOLVED, pointing to `tests/schemas/test_frontmatter_schemas.py`. Update the "Future: Validation Test Suite" subsection accordingly. This is a single-paragraph update.

---

### Internal Consistency (0.72/1.00)

**Evidence:**
This is the weakest dimension and the primary blocker. Four specific inconsistencies:

1. **Stale gap analysis row:** The gap analysis still states "No validation test suite | OPEN" while the test suite is a delivered artifact in this review set. The gap analysis' own "Summary (v1.1.0)" says "All 4 gaps RESOLVED" but then the Shared Issues table shows an unresolved OPEN item — an internal contradiction within the same document.

2. **Security review / vulnerability assessment severity mismatch:** The security review reports "0 Critical, 3 High" findings. The vulnerability assessment reports "2 Critical, 3 High" findings. The two documents review the same schemas on the same date. Neither document acknowledges the other or explains the difference in severity count. The Critical-vs-not-Critical difference for the `mcpServers` injection and unbounded `description` findings is the most significant discrepancy. A reader must choose which severity rating to act on without guidance.

3. **FIND-001/FIND-002 reconciliation gap:** The security review findings FIND-001 and FIND-002 flag the reserved-word bypass as an unresolved High severity finding. Looking at the v1.1.0 schemas directly, both schemas contain the `allOf/not` fix:
   - Agent schema line 11-14: `"allOf": [{ "pattern": "..." }, { "not": { "pattern": "claude|anthropic" } }]`
   - Skill schema line 11-13: same construction
   The security review either reviewed v1.0.0 or did not check whether its remediation was already applied. The document reports a High severity finding for a control that exists in the schema. This creates a false impression that the reserved-word fix still needs work.

4. **Schema description vs. schema behavior (agent `additionalProperties`):** The agent schema description (line 5) states "Unrecognized fields are silently ignored by Claude Code at runtime but flagged here to prevent governance metadata from leaking into frontmatter." The schema body sets `additionalProperties: true`, which does NOT flag unknown fields. FIND-005 in the security review correctly identifies this. It is unresolved in v1.1.0 and the description still contains the false claim.

**Improvement Path:**
(a) Update the gap analysis stale row. (b) Add a reconciliation note to either the security review or vulnerability assessment explaining the Critical vs. High severity difference for V-03-001 and V-04-001. (c) Update security review FIND-001/FIND-002 to note that the `allOf/not` fix was applied in v1.1.0 and confirm whether the finding is resolved or if the implemented pattern is insufficient. (d) Correct the agent schema description field on `additionalProperties` to say "silently accepted" not "flagged here."

---

### Methodological Rigor (0.86/1.00)

**Evidence:**
The methodology stack is genuinely strong:
- Gap analysis: explicit field-by-field comparison against March 2026 Anthropic documentation with severity classification and resolution tracking.
- Test suite: BDD H-20 compliance acknowledgment, three test classes (positive/negative/integrity), live roundtrip tests that directly read from disk rather than relying only on hard-coded fixtures. The `TestLiveFileFrontmatterRoundTrip` class is architecturally superior to positive-only fixtures because it catches drift between the schema and actual production files.
- Security review: ASVS V1 + V5 application, 14-item CWE checklist, explicit ReDoS analysis (confirmed no catastrophic backtracking), hardcoded credential scan, external dependency audit.
- Vulnerability assessment: PTES Vulnerability Analysis phase, OWASP A04, CVSS 3.1-informed scoring, attack path analysis with three chained exploitation scenarios.
- Scope and limitations section distinguishes schema capabilities from complementary CI controls.
- Maintenance process section addresses version staleness.

**Gaps:**
The most specific methodological gap: the reserved-word `not` constraint is the primary stated v1.1.0 security fix (mentioned in the input context: "'name' field in both schemas now enforces reserved word prohibition via allOf/not"). Yet there is no negative test case in the test suite that verifies a name containing "claude" or "anthropic" is actually rejected by the schema. The 10 agent negative fixtures and 7 skill negative fixtures do not include a case like `{"name": "claude", "description": "..."}` that should fail. The test suite validates that the constraint exists (test_agent_schema_requires_name_and_description) but does not exercise the reserved-word branch of the `allOf/not` structure. If a future schema edit mistakenly removed the `not` block, no test would catch it.

**Improvement Path:**
Add two negative test cases to `_AGENT_NEGATIVE_FIXTURES`:
- `{"name": "claude", "description": "Reserved word agent name should be rejected."}`
- `{"name": "my-anthropic-tool", "description": "Reserved word in hyphenated name should be rejected."}`
Add corresponding cases to `_SKILL_NEGATIVE_FIXTURES`. This directly tests the primary v1.1.0 security change.

---

### Evidence Quality (0.88/1.00)

**Evidence:**
Line-level citations are present throughout the security review ("line 11", "line 139", "lines 59-62"). Proof-of-concept YAML payloads are included for every vulnerability assertion in the vulnerability assessment; they show exact schema-valid content with confirmed "Schema PASS" outcome. The security review provides copy-paste JSON Schema remediation snippets that can be directly applied. CWE IDs and ASVS chapter references are present in every finding. The agent schema description cites three specific URLs and a research artifact path. Schema `$id` URIs include the version date context. The analysis demonstrates depth: V-01-003 in the vulnerability assessment correctly traces through the regex mechanics to show consecutive hyphen rejection is actually structural (not a documentation gap), and V-02-002 similarly proves the double-`[1m]` case is correctly handled. These are non-trivial analytical conclusions supported by step-by-step evidence.

**Gaps:**
The gap analysis header states "Sources: STORY-001 + STORY-002 research artifacts" but does not provide the artifact paths or quote specific conclusions from those artifacts. A reader wanting to verify the gap analysis claims against the upstream research cannot do so without knowing the research file paths. The vulnerability assessment and security review do not cross-reference each other, which means the shared findings (reserved word bypass, unbounded description, mcpServers injection) appear in both with different conclusions but no shared evidence chain.

**Improvement Path:**
Add the specific file paths of STORY-001 and STORY-002 research artifacts to the gap analysis header. Add a one-line cross-reference in the security review L2 section noting that findings FIND-001/FIND-003/FIND-004 overlap with V-01-001/V-04-001/V-03-001 in the vulnerability assessment.

---

### Actionability (0.78/1.00)

**Evidence:**
The priority-ordered remediation table in the vulnerability assessment is the strongest actionability artifact: it provides effort estimates (Minutes/Hours/Days), sprint-cycle classification (Immediate/Sprint/Quarter/Backlog), and rationale for ordering. Copy-paste JSON Schema snippets remove the authoring burden for each fix. The test suite is immediately runnable with `uv run pytest tests/schemas/test_frontmatter_schemas.py`.

**Gaps:**
The dominant actionability problem is the FIND-001/FIND-002 confusion. A developer assigned to address security review findings would:
1. Read FIND-001: "Reserved word bypass -- High -- unresolved"
2. Look at the current agent schema: see the `allOf/not` block at line 11-14
3. Have no guidance from the document on whether this is already fixed or needs further work

The security review's L0 summary section "Recommended Immediate Actions" item 1 says "Add a `not` + `pattern` constraint to both `name` fields" -- but this constraint already exists in the schema. A developer acting on this recommendation would implement a change that is already present, potentially introducing a duplicate constraint or confusion. This is a concrete actionability failure for the highest-priority recommended action.

Secondary gap: the security review and vulnerability assessment each contain slightly different remediation patterns for the same issues (e.g., FIND-001 uses `(^|[-])claude([-]|$)` for word-boundary matching, while V-01-001 uses `(claude|anthropic)` for substring matching). Neither explains why the patterns differ or which is preferred. The schema's actual implementation uses `claude|anthropic` (substring). The developer must choose between three versions without guidance.

**Improvement Path:**
Update the security review FIND-001/FIND-002 status to note the `allOf/not` fix is already applied in v1.1.0. Mark the findings as "Partially Mitigated -- v1.1.0" or "Closed" with a note on what remains open (e.g., whether `claudia` should also be rejected). Reconcile the three pattern variants (schema body, FIND-001, V-01-001) with a single recommended pattern and rationale.

---

### Traceability (0.82/1.00)

**Evidence:**
The schema `$id` URIs are versioned and include the date context. The test file module docstring references EN-003, H-20, and H-34. The gap analysis field tables link each field to "Our Schema (v1.0.0)", "Official (March 2026)", and "v1.1.0 Status". Security review findings cite affected file, affected field, affected line number, CWE, and ASVS reference for every finding. The vulnerability assessment cites PTES, OWASP, and CVSS. The schema `description` fields link to specific Anthropic documentation URLs and to the research artifact path.

**Gaps:**
The primary traceability gap is that no test exercises the reserved-word constraint that is the primary stated v1.1.0 security change. If the `not` block were silently removed from either schema, no existing test would fail. The reserved-word prohibition appears in:
- The gap analysis (gap #5 for agent, described as "OK" in v1.0.0 but the v1.1.0 status says "allOf/not" fix)
- FIND-001/FIND-002 in the security review
- V-01-001 in the vulnerability assessment
- The schema itself (lines 11-14 in both schemas)

But there is no test ID in the test suite that closes this traceability chain. The test suite has `test_agent_schema_requires_name_and_description` (integrity check) but no `test_agent_name_rejects_reserved_words`. This is a direct traceability failure from requirement to test.

**Improvement Path:**
Add reserved-word negative test cases as described under Methodological Rigor. Each test should have a descriptive ID that references the specific constraint being tested.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.72 | 0.85 | Update security review FIND-001/FIND-002 to reflect that the `allOf/not` fix is already applied in v1.1.0 schemas; mark findings as Partially Mitigated or Closed with notes on what remains |
| 2 | Internal Consistency | 0.72 | 0.85 | Add a reconciliation paragraph to the security review L2 section explaining why the security review reports 0 Critical while the vulnerability assessment reports 2 Critical for the same schema artifacts |
| 3 | Methodological Rigor + Traceability | 0.86/0.82 | 0.92/0.90 | Add 4 negative test cases to the test suite: `name: claude` (agent), `name: my-anthropic-tool` (agent), `name: claude` (skill), `name: anthropic-service` (skill) — these test the primary v1.1.0 security change |
| 4 | Completeness + Internal Consistency | 0.88/0.72 | 0.92/0.85 | Update gap analysis "No validation test suite" OPEN row to RESOLVED, pointing to `tests/schemas/test_frontmatter_schemas.py`; update the "Future: Validation Test Suite" section to past tense |
| 5 | Actionability | 0.78 | 0.88 | Reconcile the three pattern variants for the reserved-word check (schema body: `claude|anthropic`; FIND-001: `(^|[-])claude([-]|$)`; V-01-001: `(claude|anthropic)`) with a single canonical pattern and rationale for the choice |
| 6 | Internal Consistency | 0.72 | 0.82 | Correct the agent schema `description` field (line 5) from "flagged here to prevent governance metadata from leaking" to accurately state that `additionalProperties: true` accepts unknown fields silently and flagging is deferred to CI lint |

---

## Delta Analysis from First Review (0.79 → 0.823)

| Dimension | First Score (est.) | Re-Score | Change | Driver |
|-----------|-------------------|----------|--------|--------|
| Completeness | ~0.70 | 0.88 | +0.18 | Test suite delivered (34 tests); all 11 missing skill fields added; gap analysis scope/limitations/maintenance sections added |
| Internal Consistency | ~0.75 | 0.72 | -0.03 | New inconsistencies introduced: security review not reconciled with v1.1.0 schema state; FIND-001/002 conflict with applied fix; severity count mismatch between security and vulnerability docs |
| Methodological Rigor | ~0.80 | 0.86 | +0.06 | BDD test suite with live roundtrip; ASVS + CVSS + PTES methodology; scope and limitations; maintenance process |
| Evidence Quality | ~0.82 | 0.88 | +0.06 | PoC payloads in vulnerability assessment; line-level evidence in security review; CWE/ASVS citations |
| Actionability | ~0.80 | 0.78 | -0.02 | New actionability problem: FIND-001/002 recommend action already taken; conflicting pattern recommendations |
| Traceability | ~0.78 | 0.82 | +0.04 | Source URLs in schema descriptions; test file rule citations; version-pinned `$id` URIs |

**Key observation:** The remediation work genuinely improved completeness, methodological rigor, and evidence quality. However, the security review artifacts appear to have been produced without checking whether their findings were already addressed in v1.1.0 — causing FIND-001/002 to read as open issues when they are closed, and causing the severity count to diverge from the vulnerability assessment without explanation. This introduces new internal consistency and actionability problems that partially offset the completeness gains.

---

## Remaining Items to Reach 0.92+

To cross the 0.92 threshold, the following specific changes are needed (estimated score impact shown):

| Change | Targeted Dimensions | Estimated Score After |
|--------|--------------------|-----------------------|
| Fix FIND-001/002 security review status + severity count reconciliation | Internal Consistency 0.72 → 0.85, Actionability 0.78 → 0.85 | 0.823 → ~0.87 |
| Add 4 reserved-word negative test cases | Methodological Rigor 0.86 → 0.91, Traceability 0.82 → 0.88 | ~0.87 → ~0.90 |
| Fix gap analysis stale OPEN row | Completeness 0.88 → 0.92, Internal Consistency → minor improvement | ~0.90 → ~0.92 |
| Correct agent schema `additionalProperties` description | Internal Consistency → minor improvement | ~0.92 → 0.92+ |

The gap is addressable with targeted revisions to 3 files: (1) the security review (FIND-001/002 status update + severity reconciliation paragraph), (2) the test suite (4 new negative test cases), (3) the gap analysis (stale OPEN row update). The schemas themselves are structurally sound.

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computation
- [x] Evidence documented for each score — specific line numbers, specific document sections, specific quotes
- [x] Uncertain scores resolved downward — Internal Consistency held at 0.72 despite overall strong work; Actionability held at 0.78 despite strong remediation tables
- [x] Post-remediation calibration applied: this is not a first draft; 0.82 is appropriate for "strong post-remediation work with specific, documented defects" not "good enough" territory
- [x] No dimension scored above 0.95 — highest dimension is 0.88 for Completeness and Evidence Quality, appropriate given documented gaps
- [x] FIND-001/002 confusion given full weight in scoring, not treated as a minor editorial issue

---

*Scored by: adv-scorer (S-014 LLM-as-Judge)*
*Constitutional Compliance: P-001 (evidence-based), P-002 (file persisted), P-003 (no subagents spawned), P-022 (no leniency inflation)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Iteration: 2 (C4 re-score after first review at 0.79)*
