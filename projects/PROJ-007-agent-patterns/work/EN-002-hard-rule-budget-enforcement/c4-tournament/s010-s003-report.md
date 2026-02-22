# EN-002: S-010 Self-Refine + S-003 Steelman Report

> **Agent:** adv-executor
> **Strategies:** S-010 Self-Refine, S-003 Steelman Technique
> **Deliverable:** EN-002 HARD Rule Budget Enforcement Implementation
> **Date:** 2026-02-21
> **Tournament Level:** C4
> **Threshold:** >= 0.95 (C4 tournament)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [S-010 Self-Refine](#s-010-self-refine) | Strengths, weaknesses, blind spots from creator perspective |
| [S-003 Steelman](#s-003-steelman) | Strongest arguments FOR the implementation |
| [Findings](#findings) | Classified findings: CRITICAL / MAJOR / MINOR / OBSERVATION |

---

## S-010 Self-Refine

### Strengths

**1. Genuine architectural symmetry between L2 and L5.**
The most important structural decision — expanding the L2 engine to glob `*.md` from a directory rather than hard-coding file paths — produces a self-maintaining system. New rule files added to `.claude/rules/` are automatically included in per-prompt re-injection with zero engine changes. The L5 gate enforces the ceiling only in `quality-enforcement.md`, which is the SSOT, creating a clean separation: the L2 system is additive (more files = more coverage), while the L5 system is restrictive (ceiling enforced at the registration table). These two mechanisms operate orthogonally and do not interfere.

**2. The consolidation rationale is sound and selective.**
Rules consolidated into compound form (H-25..H-30 → H-25/H-26; H-07..H-09 → H-07) were correctly chosen for consolidation because they are enforced via L1/L2/L4 (behavioral), not via L3 (AST/deterministic). H-05 and H-06 — which do have L3 AST gating — were deliberately left as separate rules. This precision avoids a common failure mode: consolidating rules that need to be individually addressable by deterministic enforcement.

**3. The two-tier enforcement model is a genuine conceptual improvement.**
Classifying rules into Tier A (L2-protected) vs. Tier B (compensating controls) creates an explicit governance decision that was previously implicit. Before EN-002, no one could answer "which rules are most vulnerable to context rot?" with precision. After EN-002, the answer is explicit: H-04, H-16, H-17, H-18 are Tier B, with documented compensating controls (SessionStart hook, skill enforcement). This is better than the previous undifferentiated state.

**4. The backward-compatibility path handling is correct and minimal.**
`_read_rules_file` checks `is_file()` before `is_dir()`. This means all existing unit tests that pass single-file paths continue to work without modification. The path is not a breaking change — it is a strict extension. This is verified by the test suite: 3,377 tests, all pass.

**5. The exception mechanism is bounded and process-governed.**
The ceiling exception allows at most ceiling+3 = 28 slots for at most 3 months, requires a C4-reviewed ADR, and requires the L5 CI gate to be updated explicitly. This is not a backdoor — it is a governed escape hatch with an automatic expiry via the worktracker deadline. The maximum expansion (N=3) is smaller than the headroom needed for EN-001's H-32..H-35 (N=4), which forces the correct decision: further consolidation is needed before adding new rules. This constraint is a feature, not a bug.

**6. Test coverage is deep and purpose-specific.**
The new `TestMultiFileReading` class in `test_prompt_reinforcement_engine.py` covers cross-file rank ordering, non-`.md` file exclusion, empty directory handling, and backward compatibility with single-file paths. The new `TestActualFile` class in `test_hard_rule_ceiling.py` runs against the real `quality-enforcement.md`, making it a living integration check — not just a unit test against synthetic fixtures.

---

### Weaknesses

**1. The L5 gate is only triggered on `quality-enforcement.md` changes.**
The pre-commit hook configuration uses `files: \.context/rules/quality-enforcement\.md$` as the file filter. This means: if a developer adds a new HARD rule to `quality-enforcement.md` but the hook does not fire (e.g., only changes to rule documentation without touching the table), the gate may be bypassed. More seriously, the L5 gate cannot detect if a developer creates a *second* registration table elsewhere or adds rules to a SSOT fork without going through `quality-enforcement.md`. The gate enforces the SSOT contract only if that contract is respected. There is no enforcement that prevents HARD rules from being declared outside the SSOT file.

**2. The ceiling utilization is 100% (25/25) immediately post-implementation.**
The implementation succeeded in reducing 31 → 25 but simultaneously set the ceiling at 25. The "1 slot of headroom" from consolidation (31-6=25, not 24) was consumed by the ceiling being set at 25 exactly. Headroom = 0 is a fragile state. Any new capability requiring a HARD rule — including EN-001's H-32..H-35 — requires either an exception mechanism invocation or further consolidation. The exception mechanism's N=3 maximum is insufficient for the known 4-rule requirement from EN-001. This means the problem is deferred, not solved.

**3. The `tokens` metadata field in L2-REINJECT markers is parsed but unused.**
The engine parses the `tokens=N` field from each marker, but explicitly ignores it for budget decisions. The code comment says this is intentional — the engine recomputes its own estimate for consistency. However, this creates a silent divergence: marker authors write `tokens=50` but the engine may compute a different value. If the `tokens` field is wrong, no test or hook catches it. Over time, markers drift out of sync with their declared token counts, and no one notices because the field has no effect. Either the field should be removed from the marker format (reducing noise), or it should be validated against the computed estimate with a warning.

**4. The `generate_reinforcement` docstring still references a single file.**
The method-level docstring says: "Reads the quality-enforcement.md file, extracts L2-REINJECT markers..." This is stale — the engine now reads from a directory. The class-level docstring was updated correctly, but the method docstring was not. This is a documentation debt that will mislead future developers reading the code.

**5. The `_find_rules_path` fallback is asymmetric.**
When the `.claude/rules/` directory is not found, the engine falls back to `.context/rules/quality-enforcement.md` (a single file). This means the fallback silently drops coverage from 9 files to 1 file, with no warning or log output. The fail-open design is correct for not blocking the user, but the silent downgrade is undetectable. If the rules symlink is broken or the directory is misconfigured, the engine degrades silently and the degradation is not caught by any CI check.

**6. No validation that L2 markers cover the rules they are embedded near.**
The engine treats all L2-REINJECT markers in all `.md` files as equivalent. A marker in `skill-standards.md` that says "H-01: No recursive subagents" would be accepted and injected. There is no structural contract ensuring markers in a file actually relate to that file's rules. This creates a maintenance risk: markers can drift to cover different rules than the files they live in, without detection.

**7. The enforcement-effectiveness-report is based on self-measurement.**
TASK-028 measures pre/post by comparing the implementation's own metadata (number of markers, token usage, tier classification). It does not include external validation — no adversarial failure injection, no simulation of context rot at different context fill levels, no before/after comparison of actual rule compliance rates. The "84% coverage" claim is a structural metric (rules with L2 markers), not a behavioral metric (rules that the LLM actually complies with after context filling). These are different things.

---

### Blind Spots

**Blind spot 1: Rank collision behavior is undefined and untested.**
Multiple markers across different files can share the same rank (e.g., rank=2 appears twice in `quality-enforcement.md` itself). The engine sorts by rank ascending, but the sort is stable only if Python's `list.sort()` preserves insertion order for equal elements (which it does, by contract). However, the order within a rank is determined by file read order (alphabetical), which is itself determined by the OS filesystem. There are no tests for what happens when two rank=2 markers compete for the same budget slot. The behavior is deterministic on stable filesystems but is not explicitly documented or tested.

**Blind spot 2: The CI gate does not run in GitHub Actions.**
The pre-commit hook is installed locally. There is no evidence in the implementation that `check_hard_rule_ceiling.py` is also wired into a server-side CI pipeline (GitHub Actions, etc.). If a developer bypasses pre-commit with `git commit --no-verify` (which the pre-commit config itself documents as an "escape hatch"), the L5 gate is bypassed entirely and the ceiling violation reaches the remote repository undetected. For a gate designed to prevent "silent ceiling breaches," relying solely on pre-commit is insufficient — the failure mode that EN-002 was designed to prevent can still occur.

**Blind spot 3: The compound rule format changes how referenced rules are cited elsewhere.**
H-08 and H-09 have been retired and absorbed into H-07. H-27 through H-30 have been retired and absorbed into H-25 and H-26. Any existing documentation, ADRs, test comments, or worktracker entries that reference the retired IDs (H-08, H-09, H-27, H-28, H-29, H-30) now point to non-existent rules. No audit of existing references to retired IDs was performed or documented. Cross-reference integrity was not checked.

**Blind spot 4: The L2 budget increase has no empirical calibration.**
The 600→850 token budget change was derived from the observation that all 16 markers total approximately 840 tokens. However, the calibration factor (0.83) applied by `_estimate_tokens` may diverge from actual LLM tokenization for specific marker content. If actual token costs are higher than estimated, the 850-token "budget" may silently overflow in production. There is no production measurement of actual token costs vs. estimated token costs to validate the calibration factor.

---

## S-003 Steelman

### Strongest Arguments FOR the Implementation

**Core thesis:** EN-002 is not a governance adjustment — it is an enforcement architecture upgrade that converts a vulnerable, theoretically-grounded system into one with measurable enforcement coverage backed by deterministic L5 guarantees. The implementation is correct in priority, scope, and execution.

---

**Argument 1: The root problem was correctly identified and directly addressed.**

The two discoveries (DISC-001: unprincipled ceiling; DISC-002: L2 engine coverage gap) identified an enforcement system that was self-deceiving. The declared ceiling (35) had no derivation — it was arbitrary tolerance accumulation. The declared L2 protection claimed to cover HARD rules, but the engine only read 1 of 9 rule files, leaving 21/31 rules (68%) without per-prompt re-injection. EN-002 directly attacks both of these: the ceiling is now derived from three independent constraint families (cognitive load, token budget, governance burden), and the engine now reads all 9 rule files. The implementation matches the diagnosis with precision.

**Argument 2: The implementation chose forward-compatibility over expedience.**

Alternative D-001(B) — consolidating all L2 markers into `quality-enforcement.md` — would have solved the coverage problem without engine changes. This was correctly rejected because it would have violated separation of concerns and created a maintenance anti-pattern where markers for architecture rules lived in a quality enforcement file. The directory-glob approach means each rule file owns its own markers, and the engine discovers them automatically. This is the more expensive path (engine change required) but the correct one for long-term maintainability.

**Argument 3: The principled ceiling creates a self-governing system.**

At 25 HARD rules with a derived ceiling, the framework has a stable equilibrium: adding a new HARD rule requires either consolidating an existing one or invoking the exception mechanism, which requires a C4-reviewed ADR. This governance overhead is intentional. HARD rules should be expensive to add, because they consume cognitive budget, token budget, and maintenance overhead. The previous ceiling at 35 (arbitrary) created a false sense of capacity. The 25-slot ceiling with the L5 gate creates real accountability.

**Argument 4: The Tier A/B classification externalizes implicit knowledge.**

Before EN-002, every HARD rule was implicitly Tier B (dependent on L1 behavioral foundation only). The fact that some rules had L2 markers was an implementation detail known only to someone who read the engine code. After EN-002, the Two-Tier Enforcement Model is explicit governance: 21 rules are Tier A (L2-protected), 4 rules are Tier B (compensating controls), and the rationale for each Tier B classification is documented. This transforms implicit risk into explicit governance. The 4 Tier B rules (H-04, H-16, H-17, H-18) are exactly the rules whose compensating controls (SessionStart hook, /adversary skill, /problem-solving skill) are the strongest in the system — the classification is not a demotion but an acknowledgment of alternative enforcement paths.

**Argument 5: Zero headroom is a correct outcome, not a failure.**

Ending at 25/25 might appear to be a problem left unsolved. It is not. The implementation correctly reduced the count from 31 to 25, which required consolidating 7 rules without losing enforcement. Simultaneously leaving headroom would have required either raising the ceiling (which defeats the purpose) or further consolidating rules that should not be consolidated (H-04, H-05, H-06 cannot be meaningfully combined). The zero-headroom state forces the correct next action for EN-001: further consolidation or formal exception invocation with a C4-reviewed ADR. The implementation did not accidentally run out of headroom — it deliberately arrived at the principled boundary.

**Argument 6: The L5 gate addresses the failure mode that caused the original breach.**

The enforcement summary notes that the ceiling was silently breached before EN-002 (growing from 25 to 35 without detection). The root cause of that breach was L1-only enforcement: the ceiling existed in documentation but had no machine-enforceable check. The L5 pre-commit gate is deterministic and immune to context rot. Any future developer adding a HARD rule to `quality-enforcement.md` will trigger the gate on the next commit attempt. The gate failure message explicitly references EN-002 and the exception mechanism, providing actionable guidance rather than a cryptic failure. This directly closes the failure mode.

**Argument 7: The test suite depth matches the implementation's governance criticality.**

The implementation touches `.context/rules/` files (auto-C3 minimum per AE-002) and was treated as C4 (user-requested tournament). The test suite response is appropriate: 4 new unit tests for multi-file reading, 11 new unit tests for the ceiling enforcement script (including a `TestActualFile` class that runs against the real governance file), and e2e test updates that document the EN-002 consolidation explicitly via comments. The 3,377 passing tests with 0 failures validate that no existing enforcement behavior was regressed. This is the correct test posture for a governance-level change.

**Argument 8: The implementation follows the framework's own constitutional principles.**

Every decision in DEC-001 was made with explicit options analysis and documented rationale. The defer-and-measure approach (D-003, D-005) demonstrates epistemic humility: the implementation does not over-optimize beyond what the evidence supports. The exception mechanism respects P-020 (user authority) by requiring human approval via C4-reviewed ADR before any ceiling expansion. The fail-open engine design preserves P-003 compliance (no action blocking). The implementation models the framework's own governance values.

---

## Findings

### CRITICAL

**FINDING-001: CI gate is pre-commit only; server-side bypass possible.**
**Classification:** CRITICAL
**Location:** `.pre-commit-config.yaml`, `scripts/check_hard_rule_ceiling.py`
**Detail:** The L5 ceiling enforcement gate exists only as a pre-commit hook. Pre-commit can be bypassed with `git commit --no-verify` (documented in the config's own comment block as an "escape hatch"). If bypassed, a ceiling breach reaches the remote repository without detection. The entire motivation for EN-002's L5 gate was preventing silent ceiling breaches — the gate's bypass path is itself a silent breach path. EN-002 closes the L1-only gap but does not close the pre-commit bypass gap.
**Required action:** Add `check_hard_rule_ceiling.py` to the server-side CI pipeline (GitHub Actions or equivalent) so it runs independently of the local pre-commit hook. This converts the gate from "advisory with bypass" to "enforced at merge."

---

**FINDING-002: EN-001 requires N=4 ceiling exception slots; exception mechanism allows N=3 maximum.**
**Classification:** CRITICAL
**Location:** `quality-enforcement.md` (exception mechanism), `en-002-implementation-summary.md` (Risks), `enforcement-effectiveness-report.md` (EN-001 dependency note)
**Detail:** The enforcement-effectiveness report explicitly states: "TASK-016 (H-32..H-35) requires the exception mechanism to temporarily expand the ceiling from 25 to 29 (N=4 exceeds N<=3 maximum)." The exception mechanism's hard maximum is ceiling+3 = 28. EN-001 needs ceiling+4 = 29. This means EN-001 cannot unblock through the exception mechanism without first modifying the exception mechanism itself (which requires its own C4-reviewed ADR). The implementation acknowledges this but does not resolve it. The dependency is a known blocker that neither EN-002 nor EN-001 currently has a path to unblock.
**Required action:** Either (a) further consolidation to free 4 slots below the ceiling before EN-001 proceeds, or (b) a C4-reviewed ADR that modifies the exception mechanism's N=3 maximum to N=4 for this specific case. The current state leaves EN-001 blocked without a clear path.

---

### MAJOR

**FINDING-003: Retired rule IDs (H-08, H-09, H-27..H-30) not audited for cross-references.**
**Classification:** MAJOR
**Location:** Implementation changeset (all modified files)
**Detail:** Six rule IDs were retired through consolidation: H-08, H-09, H-27, H-28, H-29, H-30. These IDs may exist as references in ADRs, worktracker entities, test comments, SKILL.md files, and other documentation. The implementation did not include an audit of existing references to these retired IDs. Stale references are not immediately harmful but create maintenance confusion and may mislead future reviewers who search for "H-08" and find it referenced but not defined.
**Required action:** Run a codebase-wide search for all retired IDs (H-08, H-09, H-27, H-28, H-29, H-30) and update each reference to use the compound rule ID (H-07 or H-25/H-26 as appropriate) with a parenthetical noting the consolidation source.

**FINDING-004: `generate_reinforcement` method docstring is stale.**
**Classification:** MAJOR
**Location:** `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`, line 80-91
**Detail:** The method-level docstring for `generate_reinforcement` reads: "Reads the quality-enforcement.md file, extracts L2-REINJECT markers..." The engine now reads from a directory of files, not a single file. The class-level docstring was correctly updated, but the method-level docstring was not. This creates a documentation contract mismatch: a developer reading the method signature and docstring would infer single-file behavior when the actual behavior is multi-file. This is a correctness issue in H-12 (docstrings REQUIRED on public functions) compliance.
**Required action:** Update the `generate_reinforcement` docstring to reference the rules directory / all auto-loaded rule files, consistent with the class-level docstring.

**FINDING-005: `tokens` metadata field is parsed but never validated or enforced.**
**Classification:** MAJOR
**Location:** `prompt_reinforcement_engine.py` (`_parse_reinject_markers`), all L2-REINJECT markers across `.context/rules/*.md`
**Detail:** Every L2-REINJECT marker includes `tokens=N` but the engine ignores this value entirely, computing its own estimate. There is no validation that the declared `tokens=N` matches the computed estimate. Markers already show divergence: `quality-enforcement.md` rank=2 declares `tokens=90` for a 238-character string; the engine's formula computes ceil(238/4 * 0.83) = 50. The declared value is 80% higher than computed. Over time this divergence grows as markers are edited without updating the token annotation. Either remove the field from the marker format (since it has no effect) or add a validation step that warns when declared and computed tokens differ by more than 20%.
**Required action:** File a follow-up task to either (a) deprecate and remove the `tokens` field from the marker format in a future version, updating all 16 existing markers, or (b) add marker validation logic that fails with a warning when declared tokens diverge significantly from computed tokens.

---

### MINOR

**FINDING-006: `_find_rules_path` fallback degrades silently without warning.**
**Classification:** MINOR
**Location:** `prompt_reinforcement_engine.py`, `_find_rules_path` method (lines 252-272)
**Detail:** When `.claude/rules/` directory is not found but `CLAUDE.md` is present, the engine falls back to `.context/rules/quality-enforcement.md`. This downgrades coverage from 9 files to 1 file silently. The fail-open design prevents user blocking, but silent degradation means a misconfigured symlink or absent directory would go undetected until someone noticed that L2 enforcement felt weaker. No log statement, metric, or observable signal distinguishes "full coverage" from "fallback coverage" at runtime.
**Required action:** Add a log or metric emission (even at DEBUG level) when the engine falls back from directory to single-file mode, enabling operational detection of coverage degradation.

**FINDING-007: Rank collision behavior across files is untested.**
**Classification:** MINOR
**Location:** `test_prompt_reinforcement_engine.py`, `TestMultiFileReading`
**Detail:** Multiple markers across different files can share the same rank value. The current test suite verifies that markers are sorted globally by rank (`test_multi_file_when_directory_then_markers_sorted_by_rank_across_files`), but does not test tie-breaking behavior when two markers have identical ranks. The engine's behavior (alphabetical file order, then list insertion order) is deterministic but undocumented. If two markers both have rank=2 and one contains a higher-priority rule than the other, their relative ordering depends on file system alphabetical order — which is not a governed property.
**Required action:** Either add a test explicitly documenting the tie-breaking behavior, or extend the marker format to support sub-ranks (e.g., `rank=2.1`) for cases where ordering within a rank matters.

**FINDING-008: The enforcement-effectiveness measurement is structural, not behavioral.**
**Classification:** MINOR
**Location:** `enforcement-effectiveness-report.md`
**Detail:** The "84% L2 coverage" metric counts rules with L2 markers vs. total rules. It does not measure what it claims to measure — the probability that the LLM will comply with a rule after context has filled significantly. Structural coverage (marker exists) is necessary but not sufficient for behavioral coverage (LLM actually complies). A rule with an L2 marker could still be violated at high context fill if the marker content is ambiguous, the preamble is not prominent enough, or the rule conflicts with user intent. The 84% claim is a useful structural proxy, not a validated behavioral metric.
**Required action:** Acknowledge the structural-vs-behavioral distinction explicitly in the effectiveness report. Mark the 84% figure as "structural coverage" rather than "enforcement coverage" to prevent overconfidence.

---

### OBSERVATION

**OBSERVATION-001: Budget utilization at 65.8% represents meaningful headroom for Tier B rule promotion.**
The 291 remaining L2 token budget could accommodate 4-6 additional markers. The 4 Tier B rules (H-04, H-16, H-17, H-18) could each receive an L2 marker at approximately 30-50 tokens each, fitting within the remaining budget without a further budget increase. This does not require a rule count change and does not affect the ceiling. If empirical evidence shows enforcement failures in any Tier B rule, this path is immediately available with no blocking dependencies.

**OBSERVATION-002: The alphabetical sort of rule files produces a non-governance-driven ordering.**
The engine reads files in alphabetical order (`sorted(rules_path.glob("*.md"))`), which determines which markers are parsed first within the same rank. The current file names (architecture-standards, coding-standards, mandatory-skill-usage, etc.) produce a deterministic but unintended priority order. If two different files have rank=1 markers, `architecture-standards.md` precedes `mandatory-skill-usage.md` by filename sort, not by governance priority. This is acceptable currently (no rank collisions exist at the same rank across files) but should be documented as a known property.

**OBSERVATION-003: The `TestBudgetEnforcement` test class retains a 600-token assertion.**
In `test_prompt_reinforcement_engine.py`, `TestBudgetEnforcement.test_budget_enforcement_when_default_budget_then_within_limit` asserts `result.token_estimate <= 600`. The default budget was updated to 850 in EN-002, but this test still asserts the pre-EN-002 limit. It passes because the test fixture contains only 4 markers totaling well under 600 tokens. This is not a test failure but it is a stale assertion — the test is not exercising the new 850-token budget. A reader of the test would infer the budget is 600 when it is actually 850.

**OBSERVATION-004: The exception mechanism's 3-month duration has no automated enforcement.**
The exception mechanism requires "Consolidation or demotion must restore count to <= 25 within 3 months." This deadline is tracked in the worktracker, which is a governance record — not a deterministic check. If the worktracker entry is not updated or the deadline is missed, the L5 gate continues to pass at the temporarily expanded ceiling indefinitely. The 3-month reversion is not self-enforcing.

---

*Report generated by adv-executor agent under S-010 (Self-Refine) and S-003 (Steelman) strategies.*
*C4 tournament, EN-002 HARD Rule Budget Enforcement Implementation.*
*Date: 2026-02-21*
