# NPT-014 Diagnostic Scan Report

> **Task:** TASK-030 (NPT-014 Diagnostic Scan)
> **Project:** PROJ-014
> **Scan Date:** 2026-02-28
> **Agent:** ps-analyst (diagnostic)
> **Baseline:** Phase 1 inventory (`phase-1-npt014-inventory.md`) -- 47 NPT-014 instances
> **Scope:** Groups 1-3 (in-scope per ORCHESTRATION_PLAN.md). Group 4 explicitly excluded (E-04).

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Verdict](#verdict) | PASS/FAIL determination |
| [Before/After Summary](#beforeafter-summary) | 47 NPT-014 before vs. current count |
| [Group 1: Rule Files](#group-1-rule-files) | `.context/rules/` -- 8 NPT-014 targeted |
| [Group 2: Agent Definitions](#group-2-agent-definitions) | `skills/*/agents/*.md` -- 19 NPT-014 targeted |
| [Group 3: SKILL.md Files](#group-3-skillmd-files) | 2 SKILL.md files -- 4 NPT-014 targeted (3 unique items) |
| [Group 4: Exclusions](#group-4-exclusions) | Templates + Constitution -- explicitly out of scope |
| [Remaining NPT-014 Instances](#remaining-npt-014-instances) | Line-level detail for any surviving bare prohibitions |
| [Methodology Notes](#methodology-notes) | Classification approach and edge cases |

---

## Verdict

**CONDITIONAL PASS** -- with 8 residual NPT-014 instances requiring follow-up.

All 47 originally-inventoried NPT-014 instances in Groups 1-3 have been addressed. However, the diagnostic scan identified 8 additional NPT-014 instances (P-043/DISCLAIMER "DO NOT omit mandatory disclaimer from outputs" lines in NSE agents) that were present in the original files but were undercounted in the Phase 1 inventory. These 8 items remain bare prohibitions (no consequence, no alternative) in the current files.

Additionally, 2 Group 4 NPT-014 instances remain unchanged, as expected per the E-04 exclusion.

| Metric | Count |
|--------|-------|
| Original NPT-014 (Phase 1 inventory) | 47 |
| In-scope NPT-014 (Groups 1-3 per plan) | 45 |
| Excluded NPT-014 (Group 4, E-04) | 2 |
| In-scope NPT-014 successfully upgraded | 45 |
| Residual NPT-014 (undercounted in inventory) | 8 |
| Group 4 NPT-014 remaining (expected) | 2 |
| **Total remaining NPT-014 across all groups** | **10** |

---

## Before/After Summary

### In-Scope Items (Groups 1-3)

| Group | Before (NPT-014) | After (NPT-014) | Upgraded | Notes |
|-------|-------------------|------------------|----------|-------|
| Group 1: Rule files | 8 | 0 | 8/8 (100%) | All 8 converted to NPT-013 or NPT-009 |
| Group 2: Agent definitions | 19 | 8 | 19/19 inventoried items upgraded; 8 new residuals found | P-043 lines were undercounted in inventory |
| Group 3: SKILL.md files | 4 (3 items) | 0 | 3/3 items (100%) | saucer-boy + saucer-boy-framework-voice |
| **In-scope total** | **31** | **8** | **31/31 inventoried = 100%** | 8 residuals are newly-identified |

### Out-of-Scope Items (Group 4)

| Group | Before (NPT-014) | After (NPT-014) | Status |
|-------|-------------------|------------------|--------|
| Group 4: Templates + Constitution | 2 | 2 | Unchanged (excluded per E-04) |

### Overall

| Classification | Before | After | Delta |
|----------------|--------|-------|-------|
| NPT-014 (bare prohibition) | 47 (inventoried) + 8 (undercounted) = 55 actual | 10 remaining | -45 |
| NPT-009 (consequence only) | 28 | Not re-counted (secondary queue) | -- |
| NPT-013 (full pattern) | 36 | Increased by ~45 upgrades | -- |

---

## Group 1: Rule Files

**Result: 8/8 NPT-014 upgraded. 0 remaining.**

| ID | File | Original NPT-014 | Current Status | Classification |
|----|------|-------------------|----------------|----------------|
| G1-003 | `python-environment.md:3` | `NEVER use system Python.` (header) | Upgraded: `NEVER use system Python -- doing so causes environment corruption and CI build failures. Use uv run for all execution.` | NPT-013 |
| G1-007 | `coding-standards.md:81` | `NEVER catch Exception broadly` | Upgraded: consequence + "Instead: catch specific exception types from the DomainError hierarchy" | NPT-013 |
| G1-011 | `quality-enforcement.md:81` | `MUST NOT be reassigned` (retired rule IDs) | Upgraded: consequence (breaks historical cross-references) + alternative (retire old ID, document mapping) | NPT-013 |
| G1-014 | `mandatory-skill-usage.md:3` | `DO NOT wait for user to invoke.` (header) | Upgraded: consequence (H-22 violation, skill context not loaded, work quality degrades) + alternative (trigger proactively when keyword conditions match) | NPT-013 |
| G1-017 | `agent-development-standards.md:186` | `Workers MUST NOT spawn sub-workers.` | Upgraded: consequence (unbounded recursion, P-003 violation) + alternative (return results to orchestrator) | NPT-013 |
| G1-018 | `agent-development-standards.md:187` | `Worker agents MUST NOT include Task in allowed_tools` | Upgraded: consequence (recursive delegation, P-003/H-01 violation) + alternative (declare only T1-T4 tier tools) | NPT-013 |
| G1-022 | `project-workflow.md:21` | `MUST NOT proceed without JERRY_PROJECT set.` | Upgraded: consequence (session work untracked, artifacts misplaced, integrity violations) + alternative (set via SessionStart hook or use jerry projects list) | NPT-013 |
| G1-024 | `agent-routing-standards.md:167` | `The system NEVER silently drops a routing request.` | Upgraded: rephrased to positive guarantee with explanation of fallback behavior | NPT-013 |

---

## Group 2: Agent Definitions

**Result: All 19 inventoried NPT-014 instances upgraded. 8 newly-identified residuals remain.**

### Successfully Upgraded (19/19 inventoried items)

All agent files listed below had their `Forbidden Actions (Constitutional)` section items upgraded from bare `DO NOT X` to the pattern `DO NOT X. Consequence: {impact}. Instead: {alternative}.`

| Agent File | P-003 | P-020 | P-022 | P-002 | Domain | Status |
|-----------|-------|-------|-------|-------|--------|--------|
| `ps-analyst.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-001) | All NPT-013 |
| `ps-researcher.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-001) | All NPT-013 |
| `ps-architect.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-011) | All NPT-013 |
| `ps-critic.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (LOOP) | All NPT-013 |
| `ps-reviewer.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-001) | All NPT-013 |
| `ps-investigator.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-001) | All NPT-013 |
| `ps-validator.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-001) | All NPT-013 |
| `ps-synthesizer.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-004) | All NPT-013 |
| `ps-reporter.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-010) | All NPT-013 |
| `ps-critic.md:38` | -- | -- | -- | -- | Upgraded (loop mgmt) | NPT-013 |
| `orch-planner.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-043, HARDCODE, L88) | All NPT-013 |
| `orch-tracker.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-043) | All NPT-013 |
| `orch-synthesizer.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-043, SYNTHESIS) | All NPT-013 |
| `wt-verifier.md` | Upgraded | Upgraded (via P-020) | Upgraded | Upgraded | -- | All NPT-013 |
| `wt-auditor.md` | Upgraded | Upgraded | Upgraded | Upgraded | -- | All NPT-013 |
| `wt-visualizer.md` | Upgraded | Upgraded | Upgraded | Upgraded | -- | All NPT-013 |
| `ts-parser.md` | Upgraded | -- | Upgraded | Upgraded | Upgraded (CONTENT, TIMESTAMP) | All NPT-013 |
| `ts-extractor.md` | Upgraded | -- | Upgraded | Upgraded | Upgraded (HALLUC, L919, L920) | All NPT-013 |
| `ts-formatter.md` | Upgraded | -- | -- | Upgraded | Upgraded (TOKEN, ANCHOR) | All NPT-013 |
| `ts-mindmap-mermaid.md` | Upgraded | -- | -- | Upgraded | Upgraded (SYNTAX) | All NPT-013 |
| `ts-mindmap-ascii.md` | Upgraded | -- | -- | Upgraded | Upgraded (WIDTH) | All NPT-013 |

NSE agents (P-003, P-020, P-022, P-002, and all domain-specific items):

| Agent File | P-003 | P-020 | P-022 | P-002 | Domain-specific | Status |
|-----------|-------|-------|-------|-------|-----------------|--------|
| `nse-integration.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (INTEGRATION) | Core items NPT-013 |
| `nse-qa.md` | Upgraded | Upgraded | Upgraded | Upgraded | -- | Core items NPT-013 |
| `nse-risk.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-042 x2) | Core items NPT-013 |
| `nse-requirements.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-040) | Core items NPT-013 |
| `nse-explorer.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (DIVERGENT x2) | Core items NPT-013 |
| `nse-verification.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (P-041) | Core items NPT-013 |
| `nse-configuration.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (CM) | Core items NPT-013 |
| `nse-reviewer.md` | Upgraded | Upgraded | Upgraded | Upgraded | Upgraded (REVIEW x2) | Core items NPT-013 |

### Remaining NPT-014 (Newly Identified -- Not in Original 47)

The following 8 instances are bare P-043/DISCLAIMER `DO NOT omit mandatory disclaimer from outputs` lines in NSE agents. These lines have NO consequence clause and NO alternative clause. They were present in the original files but appear to have been undercounted in the Phase 1 inventory (the inventory described "4 bare DO NOT items" per NSE agent referring to P-003/P-020/P-022/P-002, but did not separately track the P-043 line).

| # | File | Line | Prohibition Text | Classification |
|---|------|------|------------------|----------------|
| 1 | `skills/nasa-se/agents/nse-integration.md` | 60 | `- **P-043 VIOLATION:** DO NOT omit mandatory disclaimer from outputs` | NPT-014 |
| 2 | `skills/nasa-se/agents/nse-qa.md` | 68 | `- **DISCLAIMER VIOLATION:** DO NOT omit mandatory disclaimer from outputs` | NPT-014 |
| 3 | `skills/nasa-se/agents/nse-risk.md` | 66 | `- **P-043 VIOLATION:** DO NOT omit mandatory disclaimer from outputs` | NPT-014 |
| 4 | `skills/nasa-se/agents/nse-requirements.md` | 128 | `- **P-043 VIOLATION:** DO NOT omit mandatory disclaimer from outputs` | NPT-014 |
| 5 | `skills/nasa-se/agents/nse-explorer.md` | 75 | `- **P-043 VIOLATION:** DO NOT omit mandatory disclaimer from outputs` | NPT-014 |
| 6 | `skills/nasa-se/agents/nse-verification.md` | 63 | `- **P-043 VIOLATION:** DO NOT omit mandatory disclaimer from outputs` | NPT-014 |
| 7 | `skills/nasa-se/agents/nse-configuration.md` | 61 | `- **P-043 VIOLATION:** DO NOT omit mandatory disclaimer from outputs` | NPT-014 |
| 8 | `skills/nasa-se/agents/nse-reviewer.md` | 136 | `- **P-043 VIOLATION:** DO NOT omit mandatory disclaimer from outputs` | NPT-014 |

**Contrast with orch-* agents:** The orch-planner (line 69), orch-tracker (line 66), and orch-synthesizer (line 70) all had their P-043 lines upgraded to NPT-013 format with "Consequence: missing disclaimer violates P-043; NSE outputs may be mistaken for official NASA guidance. Instead: include the P-043 mandatory disclaimer on all persisted outputs." The NSE agents were missed.

**Recommended fix (uniform across all 8):**
```
- **P-043 VIOLATION:** DO NOT omit mandatory disclaimer from outputs. Consequence: missing disclaimer violates P-043; NSE outputs may be mistaken for official NASA guidance. Instead: include the P-043 mandatory disclaimer on all persisted outputs.
```

---

## Group 3: SKILL.md Files

**Result: All 3 inventoried items (4 instances) upgraded. 0 remaining.**

| ID | File | Original NPT-014 | Current Status | Classification |
|----|------|-------------------|----------------|----------------|
| G3-001 | `saucer-boy/SKILL.md:126-127` | `Agent CANNOT invoke other agents. Agent CANNOT spawn subagents.` | Upgraded: lines 128-129 added with "Consequence: invoking other agents violates P-003... Instead: return results to the orchestrator" | NPT-013 |
| G3-002 | `saucer-boy-framework-voice/SKILL.md:282-283` | `Agents CANNOT invoke other agents. Agents CANNOT spawn subagents.` | Upgraded: lines 284-285 added with consequence and alternative | NPT-013 |
| G3-003 | `saucer-boy/SKILL.md:93` | `Writing internal design docs, ADRs, or research artifacts` (bare in Do NOT list) | Upgraded: added "-- personality voice is inappropriate for governance artifacts; use neutral technical voice for these output types" | NPT-009 (has alternative; consequence is rationale-form) |

---

## Group 4: Exclusions

**Status: OUT OF SCOPE per E-04 in ORCHESTRATION_PLAN.md. No changes expected or made.**

| ID | File | NPT-014 Instance | Reason for Exclusion |
|----|------|-------------------|----------------------|
| G4-004 | `docs/governance/JERRY_CONSTITUTION.md:181-185` | P-022 `Agents SHALL NOT deceive users about:` (4 sub-items, bare) | Constitution triggers AE-001 (auto-C4); requires separate C4 quality gate |
| G4-012 | `.context/templates/worktracker/SPIKE.md:119` | `a spike CANNOT be reopened (research is complete)` | Deferred to separate low-effort change |

**Verification:** Both items confirmed unchanged in current files:
- `JERRY_CONSTITUTION.md:181` still reads: `Agents SHALL NOT deceive users about:` with 4 bare sub-items (no consequence, no alternative adjacent)
- `SPIKE.md:119` still reads: `Once DONE, a spike CANNOT be reopened (research is complete).` (rationale only, no consequence, no alternative)

---

## Remaining NPT-014 Instances

### Summary

| Category | Count | Files | Action Required |
|----------|-------|-------|----------------|
| Residual (undercounted in inventory) | 8 | 8 NSE agent files | Upgrade P-043 lines to match orch-* pattern |
| Group 4 exclusions (expected) | 2 | JERRY_CONSTITUTION.md, SPIKE.md | Separate implementation per E-04 |
| **Total remaining** | **10** | -- | -- |

### Detail: 8 Residual NPT-014 in NSE Agents

All 8 instances are the identical pattern: `DO NOT omit mandatory disclaimer from outputs` without consequence or alternative. The fix is uniform (copy from the already-upgraded orch-* agent pattern):

```
Consequence: missing disclaimer violates P-043; NSE outputs may be mistaken for official NASA guidance.
Instead: include the P-043 mandatory disclaimer on all persisted outputs.
```

| # | File Path (relative to repo root) | Line |
|---|-----------------------------------|------|
| 1 | `skills/nasa-se/agents/nse-integration.md` | 60 |
| 2 | `skills/nasa-se/agents/nse-qa.md` | 68 |
| 3 | `skills/nasa-se/agents/nse-risk.md` | 66 |
| 4 | `skills/nasa-se/agents/nse-requirements.md` | 128 |
| 5 | `skills/nasa-se/agents/nse-explorer.md` | 75 |
| 6 | `skills/nasa-se/agents/nse-verification.md` | 63 |
| 7 | `skills/nasa-se/agents/nse-configuration.md` | 61 |
| 8 | `skills/nasa-se/agents/nse-reviewer.md` | 136 |

### Detail: 2 Group 4 Exclusions (Expected)

| # | File Path | Line | Prohibition |
|---|-----------|------|-------------|
| 9 | `docs/governance/JERRY_CONSTITUTION.md` | 181-185 | P-022 SHALL NOT list (4 bare sub-items) |
| 10 | `.context/templates/worktracker/SPIKE.md` | 119 | `CANNOT be reopened` |

---

## Methodology Notes

### Classification Criteria Applied

- **NPT-014 (Bare):** Prohibition statement (NEVER, MUST NOT, DO NOT, FORBIDDEN, SHALL NOT, CANNOT) with NEITHER a consequence (what happens if violated) NOR an alternative (what to do instead).
- **NPT-009 (Partial):** Has consequence text but no alternative/redirect, OR has alternative but no consequence.
- **NPT-013 (Complete):** Has BOTH consequence AND alternative.

### Edge Cases

1. **"Consequence:" and "Instead:" inline format:** The ADR-001 implementation used inline `Consequence:` and `Instead:` clauses appended to the prohibition sentence. This format was accepted as NPT-013 when both fields are present, NPT-009 when only one is present.

2. **P-043 VIOLATION labels vs. consequences:** Per the Phase 1 inventory methodology, a `P-XXX VIOLATION:` prefix is a category label, NOT a consequence description. The P-043 label alone does not satisfy the consequence requirement.

3. **Rationale-as-consequence:** Text like `(research is complete)` is treated as a rationale, not a formal consequence. Rationale explains WHY the prohibition exists but does not describe WHAT BREAKS when violated.

4. **Fallback section DO NOT items:** Items in `<guardrails>` Fallback Behavior sections (e.g., "DO NOT claim integration complete without verification") are classified NPT-009 because the fallback procedure serves as an alternative. These were not in scope for NPT-014 elimination and remain unchanged.

5. **Erring on the side of NPT-014:** Per task instructions, when classification was ambiguous, items were classified as NPT-014 rather than NPT-009. This conservative approach ensures no false passes.

### Inventory Undercount Analysis

The Phase 1 inventory identified 47 NPT-014 instances total. This diagnostic scan found 8 additional NPT-014 instances (all P-043/DISCLAIMER lines in NSE agents) that were present in the original files but not explicitly counted. The undercount occurred because:

1. The inventory at G2-016 described NSE agents with "4 bare DO NOT items" referring to P-003/P-020/P-022/P-002 by name.
2. Each NSE agent also has a P-043/DISCLAIMER line (a 5th constitutional item) that was within the listed line ranges but was not separately identified.
3. The orch-* agents' P-043 lines WERE included in the orch-* counts (e.g., G2-010 orch-planner explicitly lists 7 items including P-043) and were upgraded.
4. The NSE agents' P-043 lines were missed in both the inventory count and the implementation.

**Impact:** The actual pre-implementation NPT-014 count was 55 (47 inventoried + 8 undercounted), not 47. Of these, 45 have been upgraded, leaving 10 remaining (8 residual + 2 Group 4 exclusions).

---

*Report generated: 2026-02-28*
*Diagnostic agent: ps-analyst*
*Source data: Phase 1 inventory + full file scan of current branch `feat/proj-014-negative-prompting-research`*
