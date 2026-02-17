# C4 Tournament Strategy Selection Plan
## BUG-002 Hook Schema Validation Fixes

| Section | Purpose |
|---------|---------|
| [Criticality Classification](#criticality-classification) | C4 determination with rationale |
| [Strategy Set Selection](#strategy-set-selection) | All 10 required strategies at C4 |
| [Execution Order](#execution-order-per-h-16) | Sequence with focus areas and templates |
| [Deliverable Scope](#deliverable-scope) | Files under review |
| [Quality Threshold](#quality-threshold) | 0.92 weighted composite (H-13) |

---

## Criticality Classification

### Level: C4 (Critical)

**Classification Rationale:**

This deliverable meets C4 classification on multiple grounds per `.context/rules/quality-enforcement.md`:

1. **Irreversible Impact:** Hook infrastructure is foundational to all Jerry sessions. Changes affect system-wide behavior and cannot be easily rolled back without user intervention.

2. **Governance Escalation (AE-005):** PreToolUse hook contains security guardrails controlling tool use permissions. Security-relevant code triggers automatic auto-C3 minimum; combined with infrastructure scope = C4.

3. **Architecture Changes:** Fixes modify the hook output API contract (hookSpecificOutput schema), affecting the interface between hooks and caller code. All downstream callers must adapt.

4. **High Blast Radius:** Hooks are invoked in every Claude Code session. Broken hooks disable the entire quality framework (L2-REINJECT, enforcement architecture).

5. **User Directive:** User explicitly requested C4 tournament review with all 10 adversarial strategies (per ORCHESTRATION.yaml quality section).

### Scope Definition

- **Files Changed:** 4 hook scripts, 8 JSON schema files, 3 test suites, 1 configuration file
- **Reversibility:** >1 day to revert all changes; requires coordinated schema+hook+test updates
- **Enforcement Tier:** All tiers (HARD + MEDIUM + SOFT) apply

### Required Strategy Set

**All 10 selected strategies are MANDATORY at C4.** No optional strategies.

From quality-enforcement.md § Criticality Levels:
> C4 | Critical | Irreversible, architecture/governance/public | All tiers + tournament | **All 10 selected** | None

---

## Strategy Set Selection

### Source of Truth

Strategies derived from `.context/rules/quality-enforcement.md` § Strategy Catalog (ranked by composite score):

| ID | Strategy | Family | Score | Rank | Rationale for BUG-002 |
|----|----------|--------|-------|------|----------------------|
| S-014 | LLM-as-Judge | Iterative Self-Correction | 4.40 | #1 | Scoring mechanism (6-dim rubric) for quality gate threshold |
| S-003 | Steelman Technique | Dialectical Synthesis | 4.30 | #2 | Strengthen approach before critique (H-16 prerequisite) |
| S-013 | Inversion Technique | Structured Decomposition | 4.25 | #3 | How could these fixes still break systems downstream? |
| S-007 | Constitutional AI Critique | Iterative Self-Correction | 4.15 | #4 | Verify Jerry Constitution compliance (governance) |
| S-002 | Devil's Advocate | Role-Based Adversarialism | 4.10 | #5 | Challenge schema compliance assumptions |
| S-004 | Pre-Mortem Analysis | Role-Based Adversarialism | 4.10 | #5 | Imagine these fixes failed — what went wrong? |
| S-010 | Self-Refine | Iterative Self-Correction | 4.00 | #7 | Self-review before tournament (H-15 prerequisite) |
| S-012 | FMEA | Structured Decomposition | 3.75 | #8 | Systematic failure mode enumeration across hooks |
| S-011 | Chain-of-Verification | Structured Decomposition | 3.75 | #8 | Verify factual claims (schema fields, exit codes, API behavior) |
| S-001 | Red Team Analysis | Role-Based Adversarialism | 3.35 | #10 | Adversary simulation: attempt to bypass hook guardrails |

### Excluded Strategies (Not Applied)

Per quality-enforcement.md § Strategy Catalog § Excluded, the following are excluded with stated conditions for reconsideration:

| ID | Strategy | Exclusion Reason |
|----|----------|------------------|
| S-005 | Dialectical Inquiry | RED risk — requires cross-model LLM; unavailable |
| S-006 | Analysis of Competing Hypotheses | Redundant with S-013 (Inversion) + S-004 (Pre-Mortem) |
| S-008 | Socratic Method | Requires interactive multi-turn dialogue; single-pass execution |
| S-009 | Multi-Agent Debate | RED risk — requires cross-model LLM; unavailable |
| S-015 | Prompt Adversarial Examples | RED risk — adversarial prompt injection concern |

---

## Execution Order (per H-16)

**HARD Rule H-16:** "Steelman (S-003) MUST be applied before Devil's Advocate (S-002). Canonical review pairing."

The execution order enforces this constraint and sequences strategies by feedback loop structure:

### Order 1: S-010 (Self-Refine)

**Strategy:** Self-Refine
**Family:** Iterative Self-Correction
**Composite Score:** 4.00
**Template:** `.context/templates/adversarial/s-010-self-refine.md`

**Focus Area for BUG-002:**
- Self-review of complete fix package: hooks + schemas + tests
- Check for obvious gaps: missing error cases, undocumented schema fields
- Verify test coverage against all 7 root causes (RC-1 through RC-7)
- Identify obvious defects before submitting to critics

**Prerequisite for:**
- S-003 (Steelman requires refined input)

### Order 2: S-003 (Steelman Technique)

**Strategy:** Steelman Technique
**Family:** Dialectical Synthesis
**Composite Score:** 4.30
**Template:** `.context/templates/adversarial/s-003-steelman-technique.md`

**Focus Area for BUG-002:**
- Strengthen the schema validation approach: Why is hookSpecificOutput design sound?
- Identify the best possible defense of each hook's implementation
- Articulate the strongest version of "why these fixes work"
- Construct the most favorable interpretation before critique

**Prerequisite for:**
- S-002 (Devil's Advocate) — H-16 explicitly mandates S-003 before S-002

### Order 3: S-002 (Devil's Advocate)

**Strategy:** Devil's Advocate
**Family:** Role-Based Adversarialism
**Composite Score:** 4.10
**Template:** `.context/templates/adversarial/s-002-devils-advocate.md`

**Focus Area for BUG-002:**
- Challenge assumptions: Are all schema fields correctly constrained?
- Question the fix approach: Could callers misinterpret the API contract?
- Attack weaknesses in test coverage: Missing edge cases?
- Exploit the strongest arguments from S-003 (steelman) to find their breaking points

**Constraint:** Must execute AFTER S-003 (H-16)
**Prerequisite for:**
- S-007 (Constitutional check follows critique)

### Order 4: S-007 (Constitutional AI Critique)

**Strategy:** Constitutional AI Critique
**Family:** Iterative Self-Correction
**Composite Score:** 4.15
**Template:** `.context/templates/adversarial/s-007-constitutional-ai-critique.md`

**Focus Area for BUG-002:**
- Verify Jerry Constitution compliance (docs/governance/JERRY_CONSTITUTION.md)
- Check H-07 (domain layer: no external imports) in hook implementations
- Verify H-11 (type hints on public functions) and H-12 (docstrings)
- Confirm no violations of core principles (P-003 nesting, P-020 user authority, P-022 transparency)

**Prerequisite for:**
- S-014 (Scoring requires governance verification)

### Order 5: S-014 (LLM-as-Judge)

**Strategy:** LLM-as-Judge
**Family:** Iterative Self-Correction
**Composite Score:** 4.40
**Template:** `.context/templates/adversarial/s-014-llm-as-judge.md`

**Focus Area for BUG-002:**
- Apply 6-dimension weighted rubric (quality-enforcement.md § Quality Gate):
  - **Completeness (20%):** All 7 root causes addressed across all 4 files?
  - **Internal Consistency (20%):** All hooks follow same pattern as session_start_hook.py reference?
  - **Methodological Rigor (20%):** Fixes derived from authoritative Claude Code docs?
  - **Evidence Quality (15%):** Schema validation tests prove compliance?
  - **Actionability (15%):** Fixes directly applicable with no ambiguity?
  - **Traceability (10%):** Each fix traces to specific root cause (RC-1 through RC-7)?
- Produce quantitative composite score on [0.0, 1.0] scale
- Score must reach >= 0.92 threshold (H-13) for PASS band

**Prerequisite for:**
- Phase 5 revision decision (if score < 0.92)

### Order 6: S-004 (Pre-Mortem Analysis)

**Strategy:** Pre-Mortem Analysis
**Family:** Role-Based Adversarialism
**Composite Score:** 4.10
**Template:** `.context/templates/adversarial/s-004-pre-mortem-analysis.md`

**Focus Area for BUG-002:**
- Imagine we deployed these fixes and they failed in production
- What went wrong? (Possible failure scenarios):
  - Hook output doesn't match schema in production environments
  - Downstream callers still use old API, causing runtime errors
  - Edge cases not covered by 31 schema compliance tests
  - Performance regression in pre_tool_use hook (security check slowdown)
- Root cause analysis for each failure scenario
- Actionable prevention steps

**Prerequisite for:**
- S-013 (Inversion builds on pre-mortem scenarios)

### Order 7: S-013 (Inversion Technique)

**Strategy:** Inversion Technique
**Family:** Structured Decomposition
**Composite Score:** 4.25
**Template:** `.context/templates/adversarial/s-013-inversion-technique.md`

**Focus Area for BUG-002:**
- **How to break these fixes systematically:**
  - Invert: "Hooks output correct JSON" → "How to make hooks output invalid JSON?"
  - Invert: "Tests catch all errors" → "What errors escape test coverage?"
  - Invert: "Schema contract is clear" → "How is the API contract ambiguous?"
- **How to destroy the fix goals:**
  - Break schema validation → What fields are under-constrained?
  - Break permission semantics → Can pre_tool_use logic be bypassed?
  - Break exit codes → What error cases return wrong codes?
- Enumerate all inversion dimensions systematically

**Prerequisite for:**
- S-012 (FMEA refines inversion into structured failures)

### Order 8: S-012 (FMEA)

**Strategy:** FMEA (Failure Mode & Effects Analysis)
**Family:** Structured Decomposition
**Composite Score:** 3.75
**Template:** `.context/templates/adversarial/s-012-fmea.md`

**Focus Area for BUG-002:**
- **Systematic failure mode enumeration:**
  - user-prompt-submit.py: 4 hook events × 3-5 failure modes each
  - pre_tool_use.py: 7 decision paths × 2-3 failure modes each
  - subagent_stop.py: 2 control flows × 2-3 failure modes each
  - hooks.json: 5 event mappings × 1-2 failure modes each
- **Severity & likelihood assessment:**
  - High severity: Security guardrail bypass (PreToolUse)
  - Medium severity: Schema validation failure → downstream error
  - Low severity: Performance regression
- **Current mitigations:** Testing, schema validation, docstrings
- **Residual risk:** Gaps unaddressed by tests?

**Prerequisite for:**
- S-011 (Verification checks specific facts from FMEA)

### Order 9: S-011 (Chain-of-Verification)

**Strategy:** Chain-of-Verification
**Family:** Structured Decomposition
**Composite Score:** 3.75
**Template:** `.context/templates/adversarial/s-011-chain-of-verification.md`

**Focus Area for BUG-002:**
- **Factual verification chain:**
  1. ✓ Claim: "hookSpecificOutput exists in all hook outputs" → Verify against session_start_hook.py reference
  2. ✓ Claim: "user-prompt-submit.py outputs hookEventName: UserPromptSubmit" → Check hooks/user-prompt-submit.py line N
  3. ✓ Claim: "pre_tool_use.py returns allow/deny (not approve/block)" → Check scripts/pre_tool_use.py make_decision()
  4. ✓ Claim: "subagent_stop.py exits 0 on error (fail-open)" → Check scripts/subagent_stop.py exit codes
  5. ✓ Claim: "All 8 schema files validate successfully" → Run schema validation (tests prove this)
  6. ✓ Claim: "All 31 schema tests pass" → Check test_hook_schema_compliance.py line count
  7. ✓ Claim: "Full test suite 3159 passes" → Check pytest output from barrier-3

- **Verification gaps:** Are there assertions we cannot verify by inspection?

**Prerequisite for:**
- S-001 (Red team uses verified facts as constraints)

### Order 10: S-001 (Red Team Analysis)

**Strategy:** Red Team Analysis
**Family:** Role-Based Adversarialism
**Composite Score:** 3.35
**Template:** `.context/templates/adversarial/s-001-red-team-analysis.md`

**Focus Area for BUG-002:**
- **Adversary goal:** Bypass hook guardrails (specifically PreToolUse security checks)
- **Adversary constraints:** Operate within schema-compliant outputs (all verification chains pass)
- **Adversary tactics:**
  - Can we craft a hook event that passes schema validation but fails permission check?
  - Can we chain multiple hook events to defeat decision logic?
  - Can we exploit timing or concurrency in hook execution?
  - Can we abuse the fail-open behavior (exit 0 on error) to grant spurious permissions?
- **Assessment:** Can an attacker achieve their goal given the fixes?

**This is the final strategy.** No prerequisites.

---

## Deliverable Scope

### Files Under Tournament Review

**Hook Implementation Scripts (4 files):**
1. `/projects/PROJ-001-oss-release/hooks/user-prompt-submit.py` — UserPromptSubmit hook implementation
2. `/projects/PROJ-001-oss-release/scripts/pre_tool_use.py` — PreToolUse hook with permission logic
3. `/projects/PROJ-001-oss-release/scripts/subagent_stop.py` — SubagentStop hook implementation
4. `/projects/PROJ-001-oss-release/hooks/hooks.json` — Hook event configuration

**JSON Schema Files (8 files):**
5. `/projects/PROJ-001-oss-release/schemas/hooks.schema.json` — Root schema for hook configuration
6-13. `/projects/PROJ-001-oss-release/schemas/hooks/*.schema.json` — Event-specific schemas:
   - `session-start-hook.schema.json`
   - `user-prompt-submit.schema.json`
   - `pre-tool-use.schema.json`
   - `subagent-stop.schema.json`
   - `tool-error-hook.schema.json`
   - (3 additional event schemas per Phase 1 completion)

**Test Suites (3 files, 31 new tests):**
14. `/projects/PROJ-001-oss-release/tests/hooks/test_hook_schema_compliance.py` — 31 schema validation tests (new)
15. `/projects/PROJ-001-oss-release/tests/hooks/test_pre_tool_use.py` — PreToolUse function tests (updated)
16. `/projects/PROJ-001-oss-release/tests/integration/test_pretool_hook_integration.py` — Integration tests (updated)

**Supporting Files:**
17. `/projects/PROJ-001-oss-release/scripts/validate_schemas.py` — Schema validation utility (reference)

### Artifact References

All strategies operate on the complete deliverable package as it exists at the start of Phase 4:
- **Git Checkpoint:** CP-002 (commit a18d0a8)
- **All 3 barriers PASSED** at entry to Phase 4
- **All tests PASS:** 3159/3159 tests green (31 new schema tests + existing suite)
- **Schema validation:** 8/8 schemas validated

---

## Quality Threshold

### Gate Criteria

**Composite Quality Score Requirement (H-13):**
- **Threshold:** >= 0.92 weighted composite
- **Scoring Mechanism:** S-014 LLM-as-Judge with 6 dimensions
- **Dimension Weights:**
  - Completeness: 20%
  - Internal Consistency: 20%
  - Methodological Rigor: 20%
  - Evidence Quality: 15%
  - Actionability: 15%
  - Traceability: 10%

### Score Bands

| Band | Range | Outcome | Workflow |
|------|-------|---------|----------|
| PASS | >= 0.92 | Accepted | Proceed to BUG-002 closure |
| REVISE | 0.85 - 0.91 | Rejected (H-13) | Targeted revision, re-run tournament |
| REJECTED | < 0.85 | Rejected (H-13) | Significant rework, re-run from Phase 2 |

### Iteration Limits (H-14)

- **Minimum cycles:** 3 (creator → critic → revision)
- **Tournament iterations:** max 3 per ORCHESTRATION.yaml
- **Escalation:** After 3 failed iterations, human escalation per AE-006

---

## Execution Handoff

This plan is created by **adv-selector** agent. Execution proceeds with **adv-executor** agent, which will:

1. Load each strategy template from `.context/templates/adversarial/s-{NNN}-{slug}.md`
2. Apply the strategy in execution order (1 through 10)
3. Generate focus-area-specific deliverables for each strategy
4. Document findings in `adv-executor-tournament-results.md`

Upon **adv-executor** completion, **adv-scorer** will:
1. Consume all strategy outputs
2. Apply S-014 LLM-as-Judge 6-dimension rubric
3. Produce quantitative score with dimension breakdowns
4. Generate `adv-scorer-quality-score.md`

**Quality gate decision:**
- If score >= 0.92 → Proceed to Phase 5 closure
- If 0.85 <= score < 0.92 → Trigger fix-reviser (REVISE band)
- If score < 0.85 → Trigger fix-reviser with rework requirement (REJECTED band)

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | adv-selector-strategy-selection |
| **Created** | 2026-02-17 |
| **Agent** | adv-selector |
| **Criticality** | C4 |
| **Deliverable** | BUG-002 Hook Schema Validation Fixes |
| **Tournament Size** | 10 strategies (all selected mandatory) |
| **Quality Threshold** | >= 0.92 composite (H-13) |
| **Source of Truth** | `.context/rules/quality-enforcement.md` § [Strategy Catalog](#strategy-catalog), [Criticality Levels](#criticality-levels) |
| **Governance** | HARD rules H-13, H-14, H-15, H-16, H-17, H-18, H-22 apply |
| **Next Agent** | adv-executor (strategy execution) |
