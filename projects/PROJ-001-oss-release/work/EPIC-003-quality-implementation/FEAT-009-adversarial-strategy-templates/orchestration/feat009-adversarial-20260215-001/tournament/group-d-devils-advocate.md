# C4 Tournament — S-002 Devil's Advocate

**Strategy:** S-002 Devil's Advocate
**Deliverable:** FEAT-009 Adversarial Strategy Templates & /adversary Skill
**Criticality:** C4 (Critical) — Framework governance templates
**Date:** 2026-02-15
**Reviewer:** adv-executor (S-002)
**H-16 Compliance:** S-003 Steelman applied 2026-02-15 (confirmed via Group B report)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [H-16 Compliance](#h-16-compliance) | Verification of Steelman execution order |
| [Counterarguments](#counterarguments) | Challenge to each Steelman strength |
| [Summary](#summary) | Consolidated findings table |
| [Verdict](#verdict) | Overall assessment and revision requirements |

---

## H-16 Compliance

**S-003 Steelman executed:** 2026-02-15 (Group B: Dialectical + Risk Strategies)
**S-002 Devil's Advocate executing after S-003:** COMPLIANT

**Steelman Output Reference:** `tournament/group-b-dialectical-risk.md`

**Steelman Strengths Identified (Targets for Counterargument):**
1. SM-001: 8-section canonical template format provides comprehensive, reproducible guidance
2. SM-002: 3-agent architecture provides clean separation of concerns
3. SM-003: SSOT integration prevents constant drift across templates
4. SM-004: H-16 ordering enforcement is documented in 6+ locations
5. SM-005: E2E test suite (138 tests) provides structural validation
6. SM-006: Criticality-based strategy selection maps effort to risk

---

## Counterarguments

### DA-001: Challenge to SM-001 (8-Section Format)

**Steelman Claim:** "The 8-section canonical format (TEMPLATE-FORMAT.md) provides exceptional structural rigor... represents months of design synthesis... balances comprehensiveness with standardization."

**Counterargument:** The 8-section format is OVER-ENGINEERED for its purpose, creating unnecessary cognitive load and violating the framework's own principle of minimizing context consumption.

**Evidence:**

1. **Format Bloat**: TEMPLATE-FORMAT.md is 405 lines. Each instantiated template averages 470 lines (S-003: 476, S-004: 463, S-013: 481 per Group B evidence). The format specifies 200-400 line target but actual templates EXCEED this by 17-20%. This is a spec violation at the format level.

2. **Section Redundancy**: Analysis of the 8 sections reveals functional overlap:
   - "Purpose" (Section 2) and "Prerequisites" (Section 3) both answer "when to use this"
   - "Scoring Rubric" (Section 6) duplicates dimension definitions already in SSOT quality-enforcement.md
   - "Integration" (Section 8) duplicates criticality tables already in SKILL.md and PLAYBOOK.md
   - Actual unique sections: Identity (metadata), Execution Protocol (procedure), Output Format (structure), Examples (demonstration) = **4 sections**. The other 4 are presentational or duplicative.

3. **No Empirical Validation**: The Steelman states the format was "designed via synthesis from EPIC-002/003 work" but provides ZERO evidence that LLM agents or human users actually benefit from all 8 sections during execution. No user testing. No A/B comparison of "4-section minimal" vs "8-section comprehensive." The assumption that "more structure = better execution" is unvalidated.

4. **Self-Defeating Design**: The Jerry framework exists to combat context rot via filesystem-based selective loading. Yet the adversary templates consume 20,400 tokens (10.2% of context window) for a C4 tournament per IN-001 evidence. This EXCEEDS the allocated enforcement budget of 15,100 tokens (7.6%) by 34%. The format creates the exact problem it's designed to prevent.

**Severity:** CRITICAL

**Dimension Impact:** Methodological Rigor (framework violates its own design principle: minimize context consumption)

**Alternative Design:** A 4-section format (Identity, Execution Protocol, Output Format, Examples) would reduce templates from 470 to ~280 lines (40% reduction), dropping total corpus from 4,700 to 2,800 lines (~8,400 tokens vs 14,100 tokens). This fits within the 7.6% enforcement budget. The sacrificed sections (Purpose, Prerequisites, Scoring Rubric, Integration) can be centralized in SKILL.md and PLAYBOOK.md, referenced by link rather than duplicated 10 times.

**Response Required:** Demonstrate empirically that all 8 sections contribute to execution quality, OR refactor to 4-section minimal format with centralized reference material.

---

### DA-002: Challenge to SM-002 (3-Agent Architecture)

**Steelman Claim:** "The adv-selector / adv-executor / adv-scorer separation is exemplary... Each agent has a single, well-defined responsibility... P-003 compliance is correctly documented."

**Counterargument:** The 3-agent split adds orchestration complexity without proportional benefit. A 2-agent architecture (selector-executor + scorer) or even a single parameterized agent would achieve the same outcomes with simpler orchestration.

**Evidence:**

1. **Minimal Differentiation Between Agents**:
   - adv-selector performs deterministic lookup: criticality level → strategy set. This is a **table lookup**, not complex reasoning requiring a dedicated agent. The logic fits in 50 lines of Python (dictionary mapping + H-16 ordering insertion). Invoking a haiku agent for this is architectural gold-plating.
   - adv-executor and adv-scorer both use sonnet and both perform analytical tasks (finding generation vs scoring). The boundary is artificial: scoring IS a form of execution (executing the S-014 rubric).

2. **Orchestration Overhead**: PLAYBOOK.md documents 5-11 agent invocations for C2-C4 reviews. Each invocation requires context setup (ADV CONTEXT block), file I/O (read deliverable, read template, write report), and orchestrator state management (track which strategies have run, collect findings). A single parameterized agent could execute "run strategies [S-003, S-007, S-002, S-014] against deliverable X" in ONE invocation with internal looping, reducing orchestration from 4 invocations to 1 (75% reduction).

3. **Testing Validates Structure, Not Necessity**: test_adversary_templates_e2e.py (line 465-532) validates that the 3 agent files exist and contain correct references. But existence =/= necessity. The tests would pass if the 3 agents were consolidated into 1 agent with 3 operational modes. No test validates "3 agents is better than 1 agent."

4. **P-003 Compliance is a Red Herring**: The Steelman argues "P-003 compliance is correctly documented (workers, not orchestrators)." True, but this is a minimum bar, not an architectural achievement. A single agent with 3 modes (SELECT/EXECUTE/SCORE) is equally P-003 compliant. The separation doesn't add compliance value.

**Severity:** MAJOR

**Dimension Impact:** Internal Consistency (architecture optimizes for separation of concerns but creates orchestration complexity that undermines usability)

**Alternative Design:**
- **Option 1**: 2-agent architecture: `adv-workflow` (handles selection + execution) + `adv-scorer` (handles S-014 scoring). Selection logic moves into adv-workflow as a first step. Reduces invocations by 1 per review.
- **Option 2**: 1-agent architecture with modes: `adv-agent --mode=select|execute|score`. Orchestrator specifies mode per invocation. Internal implementation identical, but invocation surface simplified.

**Response Required:** Demonstrate empirically that 3-agent orchestration provides measurable benefit over 2-agent or 1-agent alternatives (e.g., improved error isolation, clearer separation enabling parallel development), OR consolidate to reduce orchestration complexity.

---

### DA-003: Challenge to SM-003 (SSOT Integration)

**Steelman Claim:** "The SSOT discipline prevents the common anti-pattern of 'authoritative constants duplicated in N places with drift over time'... Templates explicitly state 'MUST NOT be redefined'... E2E tests validate SSOT consistency."

**Counterargument:** SSOT integration creates a FALSE SENSE OF SECURITY. Templates reference SSOT but nothing ENFORCES correct references at runtime. A template could hardcode wrong values and still pass E2E tests if the test checks format compliance without validating content accuracy.

**Evidence:**

1. **Tests Validate Structure, Not Accuracy**: test_adversary_templates_e2e.py lines 403-437 (`test_template_dimension_weights_when_mentioned_then_not_hardcoded_differently`) parse dimension weight tables from templates and compare to SSOT values. BUT this test only fires IF a dimension weight table EXISTS in the template. If a template author writes narrative text like "We use standard dimension weights" WITHOUT a table, the test passes. The test validates "if you mention weights, they match SSOT" not "you must derive weights from SSOT."

2. **No Runtime Validation**: adv-scorer.md lines 110-122 document the SSOT dimension weights. But when adv-scorer executes, it reads these weights from its own specification file, NOT from quality-enforcement.md. If adv-scorer.md falls out of sync (e.g., someone edits line 116 to change Completeness from 0.20 to 0.25), the scorer will use 0.25 and quality-enforcement.md won't know. There is no runtime assertion `assert loaded_weight == SSOT_weight`.

3. **SSOT is a File, Not an Enforcement Mechanism**: quality-enforcement.md is a markdown file. It can be edited. If someone changes the threshold from 0.92 to 0.90 in quality-enforcement.md, ALL templates now reference 0.90 as "SSOT" and the tests pass. The SSOT itself is mutable without cross-checks. The Steelman claims "prevents drift" but drift can occur AT THE SSOT LEVEL.

4. **Threshold REVISE Band is NOT in SSOT**: TEMPLATE-FORMAT.md lines 222-229 define operational bands: PASS (>=0.92), REVISE (0.85-0.91), REJECTED (<0.85). The REVISE band is explicitly noted as "template-specific operational category (not sourced from quality-enforcement.md)." This is a violation of SSOT discipline: templates are defining threshold semantics that should be in the SSOT. Every template now duplicates this REVISE band definition (appears in S-002 line 326, S-003, S-004, S-013 equivalents). This IS the drift anti-pattern the SSOT was supposed to prevent.

**Severity:** MAJOR

**Dimension Impact:** Evidence Quality (SSOT provides documentation of intended consistency, not enforcement of actual consistency)

**Response Required:**
1. Add runtime validation: adv-scorer and adv-executor MUST load dimension weights, thresholds, and criticality mappings directly from quality-enforcement.md (parse the markdown) OR from a compiled artifact derived from quality-enforcement.md. Do not duplicate constants in agent spec files.
2. Move REVISE band definition to quality-enforcement.md as SSOT. Remove duplication from templates.
3. Add CI check: if quality-enforcement.md is modified, all templates must be re-validated against the new values.

---

### DA-004: Challenge to SM-004 (H-16 Enforcement)

**Steelman Claim:** "H-16 is not merely documented — it's operationalized... templates specify ordering constraints, agents enforce them, PLAYBOOK provides flowcharts... implemented across 7 different artifacts."

**Counterargument:** H-16 enforcement is DOCUMENTATION-HEAVY but ENFORCEMENT-LIGHT. Documenting a constraint in 6+ locations doesn't make it enforceable if there's no CI gate or runtime check preventing violations.

**Evidence:**

1. **No CI Enforcement**: There is no pre-commit hook, no CI test, no Git hook preventing someone from running S-002 before S-003. The H-16 "enforcement" is honor-system: adv-executor.md line 126 says "Read the S-003 Steelman output... if no S-003 output exists, STOP and flag H-16 violation." But this requires:
   - The orchestrator correctly invokes S-003 first
   - S-003 produces output
   - adv-executor receives the S-003 output path as input
   - adv-executor checks for the file and halts if missing

   If the orchestrator simply omits the S-003 step and invokes S-002 directly, adv-executor flags the violation... but the violation has already occurred. There's no PREVENTIVE gate.

2. **Orchestrator Can Violate H-16**: adv-selector produces an ordered strategy list (S-003 before S-002). But adv-selector is an ADVISOR, not an ENFORCER. The orchestrator (main context) receives the ordered list and is responsible for executing strategies in order. If the orchestrator is malformed (user manually invokes "/adversary run S-002" without S-003), H-16 is violated. adv-selector has no authority to prevent this.

3. **Test Validates Documentation, Not Enforcement**: test_adversary_templates_e2e.py line 669 (`test_h16_ordering_when_documented_then_s003_before_s002`) checks that:
   - SSOT contains "H-16"
   - S-002 template contains "H-16" and "S-003"
   - SKILL.md contains "H-16"

   This validates that H-16 is MENTIONED, not that it is ENFORCED. A test that actually enforces H-16 would attempt to invoke S-002 without S-003 and assert that the invocation is blocked or produces an error.

4. **6+ Locations is a Weakness, Not a Strength**: Documenting H-16 in 7 different artifacts (SKILL.md, PLAYBOOK.md, adv-selector.md, S-002 template, S-003 template, S-004 template, quality-enforcement.md) creates 7 places where the documentation can drift. If H-16 ordering changes (e.g., future ADR decides S-010 must run before S-003), all 7 locations must be updated. This is the DRY violation the SSOT is supposed to prevent.

**Severity:** MAJOR

**Dimension Impact:** Methodological Rigor (constraint is documented but not systematically enforced)

**Response Required:**
1. Add runtime enforcement: adv-executor MUST receive `prior_strategies_executed: [S-003]` as input. If S-002 is invoked and S-003 is not in the list, adv-executor HALTS with error, not warning.
2. Add E2E test: `test_h16_enforcement_when_s002_invoked_without_s003_then_execution_blocked`. Actually attempt the violation and assert it fails.
3. Consolidate H-16 documentation: Define H-16 ordering in quality-enforcement.md ONLY. All other artifacts reference quality-enforcement.md by link.

---

### DA-005: Challenge to SM-005 (E2E Test Suite)

**Steelman Claim:** "E2E test coverage is substantial and well-structured... 794 lines, 11 test classes, 40+ test methods... BDD-named... parametrized... strict validation... production-grade testing."

**Counterargument:** The E2E tests validate STRUCTURE, not QUALITY. 138 tests check that templates have the right sections, tables, and cross-references, but only 2 tests check CONTENT QUALITY (step count, example length). The tests cannot verify: Can an LLM actually follow the Execution Protocol? Are examples realistic? Are findings actionable?

**Evidence:**

1. **Content Quality Coverage is <2%**: Of 138 tests, content quality tests are:
   - Line 699: `test_template_execution_protocol_when_read_then_has_at_least_4_steps` — checks step count >= 4. Does NOT validate steps are coherent, complete, or executable.
   - Line 723: `test_template_examples_when_read_then_has_at_least_one_example` — checks examples section length > 200 chars and contains "Before/After/Example" text. Does NOT validate example demonstrates meaningful quality improvement.

   That's 2 tests out of 138 (1.4%) checking content beyond structure.

2. **No LLM Execution Validation**: The tests parse markdown, extract tables, and validate format compliance. But templates are executed by LLM AGENTS, not regex parsers. There is no test that:
   - Invokes adv-executor with a template against a test deliverable
   - Validates that adv-executor actually completes all steps in the Execution Protocol
   - Validates that findings are specific, evidence-based, and actionable
   - Validates that the deliverable quality improves after addressing findings

   The tests assume "if the template is structurally valid, execution will succeed." This assumption is UNVALIDATED per IN-003 from Group B.

3. **Example Quality is Unvalidated**: S-002 template lines 363-430 contain an example (C2 Architecture Decision — Event Sourcing). The example has 5 findings (DA-001 through DA-005). But there is no test validating:
   - Are these findings realistic? (Would a real reviewer identify these issues?)
   - Are severity assignments correct? (Is "no event versioning strategy" actually MAJOR?)
   - Does the "After" section show measurable improvement? (Is the revised ADR genuinely better?)

   The Steelman claims examples are "substantive enough to show measurable quality improvement" but provides no measurement. Test line 738 checks length > 200 chars. A 200-char trivial example would pass.

4. **Test Fragility Signal**: test_adversary_templates_e2e.py has 1 skipped test per Group B evidence ("1 skipped test indicates fragility"). The test suite is structurally comprehensive but behaviorally incomplete.

**Severity:** MAJOR

**Dimension Impact:** Evidence Quality (tests provide structural assurance, not execution assurance)

**Response Required:**
1. Add integration tests: Execute adv-executor with each template against a canonical test deliverable. Validate findings are generated and contain required fields (ID, severity, evidence, dimension).
2. Add content quality tests: For each template example, validate that findings reference specific deliverable content (not generic observations) and that severity aligns with impact.
3. Add behavioral tests: Execute full C2 review workflow (S-003 -> S-007 -> S-002 -> S-014) against test deliverable. Assert composite score is within expected range and findings are actionable.

---

### DA-006: Challenge to SM-006 (Criticality Mapping)

**Steelman Claim:** "Criticality tables accurately reflect quality-enforcement.md SSOT... consistent across 13+ referencing files... no drift detected... non-trivial to achieve and maintain."

**Counterargument:** Criticality mapping is UNTESTED IN PRACTICE. Has anyone actually run a C2 review using only 3-4 strategies and validated that it produces useful results? The mapping is THEORETICAL, derived from SSOT, not from empirical evidence of what works.

**Evidence:**

1. **No Usage Validation**: The Steelman provides zero evidence that the C2 strategy set (S-007, S-002, S-014 required, S-003/S-010 optional) has been applied to a real C2 deliverable and produced a quality score that accurately reflects deliverable quality. The mapping exists because quality-enforcement.md says it exists, not because it was validated empirically.

2. **C4 Requiring All 10 Strategies May Be Overkill**: PLAYBOOK.md lines 337-436 document C4 tournament mode requiring all 10 strategies (11 agent invocations, ~60 minutes). But for what C4 deliverable is this necessary? The FEAT-009 deliverables themselves are C4. Are all 10 strategies genuinely needed, or is this ceremonial rigor? Group B applied S-003/S-004/S-013 (3 strategies, not 10) and identified 1 Critical + 7 Major findings. If 3 strategies found critical issues, what value do the other 7 add beyond token consumption?

3. **No Guidance on Marginal Value**: PLAYBOOK.md documents WHICH strategies run at each criticality level but not WHY or WHAT INCREMENTAL VALUE each strategy provides. For example:
   - C2 requires S-007, S-002, S-014. What specific quality gaps does S-007 catch that S-002 misses?
   - C3 adds S-004, S-012, S-013. What defect types do these catch that C2 strategies don't?
   - Without this, the mapping is "we run more strategies for higher criticality" without justification.

4. **Consistency is Not Correctness**: The Steelman celebrates "no drift detected between SSOT and 13+ referencing files." But if the SSOT mapping is WRONG (e.g., C2 should require 5 strategies, not 3), then perfect consistency means the error is replicated 13 times. Consistency of a bad design is worse than inconsistency that reveals the problem.

5. **C1 Usage is Unclear**: C1 requires S-010 (Self-Refine). But S-010 is a self-review strategy, not an adversarial strategy. Why is it in the /adversary skill? If C1 deliverables only need self-review, why not direct users to run S-010 outside the adversary skill? The SKILL.md line 64 says "Do NOT use [adversary skill] when you need a creator-critic-revision loop (use /problem-solving with ps-critic instead)." But C1 routing is contradictory: adversary skill is invoked for S-010, which IS a creator-critic pattern.

**Severity:** MAJOR

**Dimension Impact:** Actionability (users don't know if the prescribed strategy set is sufficient or excessive for their criticality level)

**Response Required:**
1. Conduct empirical validation: Apply C2 strategy set to 5 real C2 deliverables. Measure: Does the review catch defects? Does composite score correlate with manual quality assessment? Document results.
2. Provide marginal value guidance: For each criticality level, document WHAT DEFECT TYPES each strategy is designed to catch. Example: "S-007 catches HARD rule violations. S-002 catches unstated assumptions. S-014 scores completeness."
3. Clarify C1 routing: Either remove S-010 from adversary skill (route to /problem-solving) OR document why C1 deliverables use adversary skill for self-review.

---

## Summary

| ID | Target | Severity | Dimension | Finding |
|----|--------|----------|-----------|---------|
| DA-001 | SM-001 (8-section format) | CRITICAL | Methodological Rigor | Format is over-engineered, consumes 20,400 tokens (34% above enforcement budget), violates framework's own anti-context-rot principle. No empirical validation of all 8 sections. 4-section minimal format would reduce corpus by 40%. |
| DA-002 | SM-002 (3-agent architecture) | MAJOR | Internal Consistency | 3-agent split adds orchestration complexity without proportional benefit. adv-selector is a table lookup, not complex reasoning. 2-agent or 1-agent architecture would simplify orchestration (75% fewer invocations). |
| DA-003 | SM-003 (SSOT integration) | MAJOR | Evidence Quality | SSOT provides documentation, not enforcement. Templates reference SSOT but no runtime validation. REVISE band is duplicated across templates (SSOT violation). quality-enforcement.md is mutable without cross-checks. |
| DA-004 | SM-004 (H-16 enforcement) | MAJOR | Methodological Rigor | H-16 is documented in 6+ locations but not enforced. No CI gate prevents S-002 before S-003. Orchestrator can violate H-16 without prevention. Tests validate documentation, not enforcement. |
| DA-005 | SM-005 (E2E test suite) | MAJOR | Evidence Quality | 138 tests validate structure, only 2 validate content quality (<2%). No tests verify LLM agents can execute protocols. No validation of example realism or finding actionability. Tests assume structural validity = execution success. |
| DA-006 | SM-006 (Criticality mapping) | MAJOR | Actionability | Mapping is theoretical, not empirically validated. No evidence C2 set works for real C2 deliverables. C4 requiring all 10 strategies may be overkill. No marginal value guidance per strategy. C1 routing contradictory. |

---

## Verdict

**Overall Assessment:** FEAT-009 does NOT survive the Devil's Advocate challenge without substantial revision.

**Findings:** 1 Critical (DA-001), 5 Major (DA-002 through DA-006), 0 Minor

**Critical Issue (DA-001):** The template format violates the framework's foundational principle (minimize context consumption). The 8-section format is over-engineered, creating 20,400 tokens of corpus (34% above allocated enforcement budget). This is an existential threat: context rot is the root problem Jerry solves; the adversary templates must not recreate it. The Steelman's claim that the format "balances comprehensiveness with standardization" is contradicted by the format's own spec violation (templates exceed 400-line target) and the lack of empirical validation.

**Major Issues:** The remaining 5 Steelman strengths (3-agent architecture, SSOT integration, H-16 enforcement, E2E tests, criticality mapping) all share a common flaw: **design without validation**. The architecture is well-documented, structurally consistent, and test-covered, but there is ZERO empirical evidence that:
- The 3-agent split improves outcomes vs. simpler alternatives
- SSOT references remain accurate at runtime
- H-16 is enforced preventively (not just detected after violation)
- LLM agents can execute templates as designed
- Criticality-mapped strategy sets work for real deliverables

**Pattern:** FEAT-009 optimizes for **design elegance** and **structural rigor** but under-invests in **operational validation** and **empirical testing**. The framework is beautiful on paper but unproven in practice.

**Revision Requirements (P0 — MUST resolve before acceptance):**

1. **DA-001 (CRITICAL):** Reduce template corpus to fit within enforcement budget. Implement lazy loading (load Execution Protocol only, not full template) OR refactor to 4-section minimal format. Validate context consumption <= 10,000 tokens for C4 tournament.

**Revision Requirements (P1 — SHOULD resolve; require justification if not):**

2. **DA-002:** Demonstrate empirical benefit of 3-agent architecture OR consolidate to 2-agent/1-agent to reduce orchestration complexity.

3. **DA-003:** Add runtime validation of SSOT values (load from quality-enforcement.md, not duplicate in specs). Move REVISE band to SSOT. Add CI check for SSOT modification.

4. **DA-004:** Add runtime enforcement of H-16 (block S-002 if S-003 not in prior_strategies_executed). Add E2E test that attempts H-16 violation and asserts failure.

5. **DA-005:** Add integration tests that execute templates with LLM agents against test deliverables. Validate findings are generated, evidence-based, and actionable. Add content quality validation for examples.

6. **DA-006:** Conduct empirical validation of C2 strategy set on 5 real deliverables. Document marginal value per strategy. Clarify C1 routing (adversary vs problem-solving).

**Recommendation:** The framework has a solid design foundation but is premature for production use. The Critical finding (template bloat) undermines framework viability. The Major findings reveal systematic gap between "designed to work" and "validated to work." REVISE before accepting FEAT-009.

---

*Devil's Advocate Report Version: 1.0.0*
*Strategy: S-002*
*H-16 Compliant: YES (S-003 executed first per Group B report)*
*Findings: 1 Critical, 5 Major, 0 Minor*
*Date: 2026-02-15*
