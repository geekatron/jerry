# EN-819 Critic Report -- Iteration 1

> **Critic:** ps-critic (opus) | **Protocol:** S-014 C4 LLM-as-Judge
> **Enabler:** EN-819 SSOT Consistency & Template Resilience
> **Date:** 2026-02-15
> **Iteration:** 1

---

## Findings

### F-001: S-003 REVISE Band Score Range Inconsistent with SSOT

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `.context/templates/adversarial/s-003-steelman.md` line 303 |

**Evidence:** S-003 defines the REVISE band as `0.85 - < 0.92`, while the SSOT (`quality-enforcement.md` line 95) defines it as `0.85 - 0.91`, and all other 9 templates consistently use `0.85 - 0.91`.

**Analysis:** This directly contradicts the purpose of TASK-002 (update all templates to reference REVISE band from SSOT instead of defining locally). While the template correctly includes the SSOT reference note at line 306, the table itself uses a different range notation (`< 0.92` vs `0.91`). Semantically, "0.85 - 0.91" and "0.85 - < 0.92" describe the same range (since scores are typically expressed to 2 decimal places), but the textual inconsistency undermines the SSOT principle. The entire purpose of EN-819 TASK-001/TASK-002 is to eliminate such local deviations.

**Recommendation:** Change line 303 from `0.85 - < 0.92` to `0.85 - 0.91` to exactly match the SSOT definition and the other 9 templates.

---

### F-002: quality-enforcement.md VERSION Not Bumped After SSOT Addition

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `.context/rules/quality-enforcement.md` line 3 |

**Evidence:** The VERSION comment reads `VERSION: 1.2.0 | DATE: 2026-02-14` despite the addition of the new "Operational Score Bands" subsection (lines 88-98) as part of TASK-001.

**Analysis:** Per the versioning protocol in TEMPLATE-FORMAT.md (lines 60-66), an additive clarifying change warrants a MINOR version bump (1.2.0 -> 1.3.0). Adding a new subsection with the PASS/REVISE/REJECTED table is an additive change that introduces new canonical content. Failing to bump the version means downstream consumers cannot detect that the SSOT has changed.

**Recommendation:** Update the VERSION comment to `VERSION: 1.3.0 | DATE: 2026-02-15` to reflect the addition of Operational Score Bands.

---

### F-003: Tests Use Relative Paths Instead of PROJECT_ROOT

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `tests/e2e/test_adversary_templates_e2e.py` lines 875, 882, 891, 997, 1008, 1023, 1029, 1038 |

**Evidence:** The `TestMalformedTemplateHandling`, `TestH16Enforcement`, `TestAutoEscalation`, and `TestP003SelfCheck` classes all use relative paths like `Path("skills/adversary/agents/adv-executor.md")`, while all other test classes in the same file correctly use `AGENT_FILES["adv-executor"]` which is built from the `PROJECT_ROOT` constant.

**Analysis:** This is an internal consistency failure within the test file. The file defines `PROJECT_ROOT` at line 35 and `AGENT_FILES` at lines 108-112 precisely to avoid relative path issues. Tests using relative paths will fail when pytest is invoked from any directory other than the project root, creating fragile CI behavior. The EN-819 TASK-004 tests at lines 873-926 are all affected by this issue.

**Recommendation:** Replace all 8 occurrences of `Path("skills/adversary/agents/adv-executor.md").read_text()` with `read_file(AGENT_FILES["adv-executor"])` (and similarly for adv-selector). This aligns with the existing pattern used throughout the file.

---

### F-004: SSOT REVISE Band Test Assertions Are Shallow

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **File** | `tests/e2e/test_adversary_templates_e2e.py` lines 898-903 |

**Evidence:** `test_ssot_when_read_then_contains_revise_band_definition` only asserts `"REVISE" in content` and `"0.85" in content`.

**Analysis:** These assertions are near-vacuous for verifying TASK-001 completion. They would pass even if "REVISE" appeared only in a comment or unrelated context, and "0.85" could match any occurrence of that string. The test does not verify: (a) the "Operational Score Bands" subsection heading exists, (b) the REVISE upper bound of 0.91, (c) the PASS/REVISE/REJECTED table structure, (d) the clarifying note that both REVISE and REJECTED trigger revision per H-13. A properly rigorous test should verify the specific structural addition that TASK-001 requires.

**Recommendation:** Strengthen the test to verify:
1. The heading `### Operational Score Bands` exists
2. The REVISE band row contains both `0.85` and `0.91`
3. The PASS band row contains `>= 0.92`
4. The note about REVISE not being a distinct acceptance state is present

---

### F-005: Malformed Template Test Does Not Verify Orchestrator Action Requirements

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `tests/e2e/test_adversary_templates_e2e.py` lines 870-896 |

**Evidence:** The `TestMalformedTemplateHandling` class tests for (1) malformed handling presence, (2) CRITICAL severity, and (3) HALT execution. It does not test for the orchestrator action requirements (log, decide skip/fix, blocks PASS) documented in adv-executor.md lines 217-220.

**Analysis:** TASK-003 specifies that the malformed template handling should include orchestrator action requirements. The tests verify the detect/emit/halt aspects but miss the fourth element (orchestrator action). While the orchestrator actions are documented in adv-executor.md (verified), the test coverage is incomplete for the full TASK-003 scope.

**Recommendation:** Add a test `test_adv_executor_when_read_then_malformed_documents_orchestrator_action` that verifies the presence of orchestrator requirements (e.g., "blocks PASS" or "skip the strategy or fix the template").

---

### F-006: Malformed Template Test Section Extraction Is Imprecise

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `tests/e2e/test_adversary_templates_e2e.py` lines 884, 892 |

**Evidence:** Lines 884 and 892 extract the "malformed section" using `content[content.find("Malformed"):]`, which captures everything from the first occurrence of "Malformed" to the end of the entire file.

**Analysis:** This means the CRITICAL and HALT assertions are tested against the entire remainder of the file, not just the Malformed Template Handling subsection. Since "Critical" appears in the severity classification table at Step 4 (line 250-252), and other content follows, the assertions would pass even if the Malformed Template Handling subsection itself lacked these terms. The test is not actually verifying that the severity and halt instructions are in the malformed handling section.

**Recommendation:** Extract the subsection more precisely by finding the start (`### Malformed Template Handling`) and end (the next `### Step` heading) markers, then assert within that bounded content only.

---

### F-007: Finding ID Format Mismatch Between Malformed Handling and Step 5

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `skills/adversary/agents/adv-executor.md` lines 208 vs 259 |

**Evidence:** The Malformed Template Handling subsection (line 208) uses the format `{PREFIX}-000-{execution_id}` which includes execution-scoped IDs. However, Step 5 (line 259) documents the format as `{FINDING-PREFIX}-{SEQUENCE}` without the `{execution_id}` suffix, and the prefix reference list (lines 261-271) uses `XX-001` format without execution scope.

**Analysis:** TEMPLATE-FORMAT.md (lines 86-89) defines the canonical format as `{PREFIX}-{NNN}-{execution_id}` with execution-scoped suffixes. The malformed template handling correctly follows this format, but Step 5 uses the older format without execution scope. This creates an internal inconsistency within adv-executor.md. While this pre-dates EN-819 (it was likely present before), the EN-819 addition should not introduce inconsistency with its surrounding context.

**Recommendation:** This is a pre-existing issue and does not directly fall within EN-819 scope, but the creator should be aware that the malformed handling format is inconsistent with Step 5. Consider noting this as a follow-up item or aligning Step 5 to use the execution-scoped format.

---

### F-008: No Test for Finding ID Format in Malformed Handling

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **File** | `tests/e2e/test_adversary_templates_e2e.py` lines 870-896 |

**Evidence:** No test verifies that the malformed template handling emits findings in the correct format (`{PREFIX}-000-{execution_id}`).

**Analysis:** TASK-003 specifies the finding format as `{PREFIX}-000-{execution_id}`. The test suite verifies CRITICAL severity and HALT behavior but not the finding ID format. This is a gap in test coverage for TASK-003.

**Recommendation:** Add a test that verifies `{PREFIX}-000-{execution_id}` or the pattern `PREFIX.*000.*execution_id` appears in the malformed handling section.

---

## Dimension Scores

| Dimension | Score | Weight | Weighted | Evidence |
|-----------|-------|--------|----------|----------|
| Completeness | 0.88 | 0.20 | 0.176 | All 4 tasks addressed. SSOT subsection added (TASK-001). All 10 templates updated with SSOT note (TASK-002). Malformed handling documented in adv-executor (TASK-003). Tests exist (TASK-004). However: S-003 band range inconsistent (F-001), version not bumped (F-002), tests miss orchestrator actions (F-005) and finding format (F-008). |
| Internal Consistency | 0.85 | 0.20 | 0.170 | 9 of 10 templates perfectly consistent. S-003 uses `0.85 - < 0.92` while SSOT and all others use `0.85 - 0.91` (F-001). Finding ID format inconsistency between malformed handling and Step 5 (F-007). Tests use relative paths while rest of file uses PROJECT_ROOT (F-003). |
| Methodological Rigor | 0.88 | 0.20 | 0.176 | SSOT-first approach is correct. TEMPLATE-FORMAT.md Constants Reference properly updated with Operational Score Bands table. Malformed template handling follows detect/emit/halt pattern with clear orchestrator actions. Tests follow BDD naming convention. Deductions for shallow SSOT test assertions (F-004) and imprecise section extraction (F-006). |
| Evidence Quality | 0.90 | 0.15 | 0.135 | All template changes are verifiable by grep. SSOT subsection is well-placed in Quality Gate section. TEMPLATE-FORMAT.md Constants Reference mirrors SSOT exactly. adv-executor malformed handling includes concrete finding format example. Minor gap: tests do not verify the specific structural elements added. |
| Actionability | 0.92 | 0.15 | 0.138 | All changes are implementable and specific. SSOT reference notes use consistent language across templates. Malformed handling provides clear, unambiguous instructions. Test recommendations are concrete and fixable. |
| Traceability | 0.93 | 0.10 | 0.093 | SSOT subsection correctly references H-13. Templates cite "quality-enforcement.md (Operational Score Bands section)". TEMPLATE-FORMAT.md version bumped to 1.1.0 with proper date. Test docstrings reference EN-819 scope. quality-enforcement.md version not bumped (F-002) is a minor traceability gap. |

**Weighted Composite: 0.888**

## Gate Decision

**REVISE** (0.888 < 0.920 threshold)

## Summary

EN-819 delivers substantial progress across all 4 tasks. The SSOT Operational Score Bands subsection is well-structured and correctly placed within the Quality Gate section of quality-enforcement.md. Nine of 10 templates have been correctly updated with consistent SSOT reference notes, and the TEMPLATE-FORMAT.md Constants Reference has been properly updated to mirror the SSOT. The malformed template handling in adv-executor.md is logically placed, covers the detect/emit/halt pattern, and includes orchestrator action requirements.

However, the deliverable falls short of the 0.92 threshold due to three areas requiring revision. First, S-003 (steelman) uses a REVISE band range of `0.85 - < 0.92` instead of the SSOT-canonical `0.85 - 0.91`, directly undermining the SSOT consistency goal of TASK-002 (F-001, Major). Second, the E2E tests use relative paths instead of the file's own `PROJECT_ROOT` constant, creating fragile CI behavior and internal inconsistency (F-003, Major). Third, the SSOT REVISE band test assertions are shallow and near-vacuous -- they verify keyword presence but not the specific structural content that TASK-001 added (F-004, Major). These three Major findings are the primary blockers. The Minor findings (F-002 version bump, F-005/F-006/F-007/F-008 test completeness and precision) should also be addressed but are not individually blocking.
