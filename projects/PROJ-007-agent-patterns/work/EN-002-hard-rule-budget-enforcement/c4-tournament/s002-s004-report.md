# EN-002: S-002 Devil's Advocate + S-004 Pre-Mortem Report

> **Strategy:** S-002 (Devil's Advocate) + S-004 (Pre-Mortem Analysis)
> **Agent:** adv-executor
> **Deliverable:** EN-002 HARD Rule Budget Enforcement Implementation
> **Date:** 2026-02-21
> **Tournament Level:** C4

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Challenges to each key claim and assumption |
| [S-004 Pre-Mortem](#s-004-pre-mortem) | Failure scenarios at 6-month horizon |
| [Findings](#findings) | Classified findings: CRITICAL / MAJOR / MINOR / OBSERVATION |

---

## S-002 Devil's Advocate

The following challenges each major claim and assumption in the EN-002 implementation. The role adopted is skeptical opposition: each claim is assumed false until the implementation demonstrates otherwise.

---

### Challenge 1: Is the ceiling of 25 truly principled or just another arbitrary number?

**The claim:** The ceiling of 25 is derived from three independent constraint families (cognitive load, enforcement coverage, governance burden), producing a convergence point that is "robust within the 20-28 range."

**The challenge:**

The convergence argument is circularly constructed. Constraint Family A (token/resource budget) was analyzed with the engine operating at 840 tokens — a number itself derived from operational data that predates the consolidation. Constraint Family B (enforcement coverage) produced a minimum of 14 (engine L2 only) and a maximum of 25+ (with compensating controls) — a range so wide that any target between 14 and 28 is justifiable. Constraint Family C (instruction-following capacity) cited "~25 total with partitioning" without empirical validation of what LLM attention budgets actually degrade at.

The three constraint families did not independently derive 25. They derived overlapping ranges, and 25 was selected because it is the current count after consolidation. The derivation retro-fitted the analysis to the achievable result. This is the same failure mode as the original ceiling breach: the ceiling is where the count lands, not where the constraint analysis independently points.

Furthermore, the claim that the derivation was scored 0.95 PASS at C4 tournament level is itself a self-certification. The same orchestrator that performed the work scored the work. No independent validator examined the derivation. The 0.95 score may reflect marker quality in the SSOT document rather than the soundness of the ceiling's mathematical basis.

**Verdict:** The 25-rule ceiling is better-rationalized than the previous 35, but "better-rationalized" is not the same as "principled." The convergence is constructed, not discovered.

---

### Challenge 2: Does consolidation actually preserve enforcement or does it weaken it?

**The claim:** Consolidating H-25..H-30 into 2 compound rules and H-07..H-09 into 1 compound rule "preserves enforcement for ALL existing constraints while reducing the attention budget."

**The challenge:**

Compound rules create a discrimination problem. When a rule has a single, crisp statement, a violation is immediately recognizable. When a rule reads "Skill naming and structure (SKILL.md case, kebab-case folder, no README.md)," the LLM must now parse a multi-part constraint and apply all three sub-tests. Cognitive load reduction at the rule-count level is not the same as cognitive simplicity at the enforcement level: you traded 6 simple rules for 2 complex ones.

Enforcement in the L3 layer (AST gating) is unambiguous — but the implementation summary explicitly states that compound rules are used for rules enforced via L1/L2/L4, not L3. L1 and L4 enforcement are LLM-mediated, which is exactly where complex compound rules are most likely to fail. The LLM under context rot may correctly recall that H-25 exists but fail to apply all three sub-tests of a compound rule.

The sub-item labeling (a), (b), (c) is a mitigation, not a solution. The L2-REINJECT marker for skill-standards is a single content string: it cannot differentiate between sub-items. If the marker fires, the LLM receives an undifferentiated summary — it does not receive three separate, callable rules.

The implementation presents no evidence that compound rules perform at parity with atomized rules under context rot. This is an untested assumption.

**Verdict:** Consolidation reduced the rule count without empirical evidence that enforcement fidelity is preserved. The mechanism by which compound rules are enforced at L2 is weaker than equivalent atomized rules.

---

### Challenge 3: Is the L2 engine expansion really necessary or just complexity?

**The claim:** Expanding the L2 engine to read all 9 auto-loaded files is "the highest-value, lowest-effort fix" and it "addresses the binding constraint."

**The challenge:**

The expansion increased token consumption from ~415 to 559 tokens per prompt. The implementation declares this "within budget" because the budget was simultaneously raised from 600 to 850. This is circular: the fix was justified by the budget increase, and the budget increase was justified by the fix. Neither change was derived independently.

The assumption that more L2 coverage is always better ignores attention dilution. When a single prompt injection contains 21 rules across 16 markers, the LLM receives a wall of text. Reinforcement research on LLMs suggests that concise, high-signal prompts outperform verbose, comprehensive ones. The previous 600-token engine injecting 10 rules may have had higher per-rule attention than the new 850-token engine injecting 21 rules.

There is also a fragility concern. The engine now performs a directory glob at runtime. If a new rule file is added to `.context/rules/` — one that was not intended for L2 injection and contains no markers, or worse, contains malformed markers — it is silently processed. The fail-open design means malformed markers from a new file are skipped, but the directory glob means any new file becomes part of the L2 processing pipeline without explicit opt-in.

The implementation explicitly states it has "not measured L2 reinforcement effectiveness empirically." DEC-005 defers measurement to after implementation. This sequencing means the expansion was implemented as an engineering assumption, not a measured improvement.

**Verdict:** The engine expansion is a reasonable hypothesis, not a demonstrated improvement. It may improve coverage at the cost of per-rule attention quality. It introduces a forward-compatibility risk by globbing all files unconditionally.

---

### Challenge 4: Is the exception mechanism a loophole that undermines the ceiling?

**The claim:** The exception mechanism provides "controlled temporary expansion" with five conditions (C4-reviewed ADR, N=3 maximum, 3-month duration, L5 gate update, consolidation plan).

**The challenge:**

The exception mechanism's conditions are mostly process gates, not technical enforcement. The L5 CI gate is the only deterministic enforcement point — and the gate reads the ceiling value directly from the SSOT document. This means the exception process reduces to: modify the SSOT to raise the ceiling, which the L5 gate then permits. The five conditions are honored-on-the-honor-system.

The implementation summary identifies that EN-001's TASK-016 (adding H-32..H-35) will require N=4 additional slots, which exceeds the stated N<=3 maximum. The exception mechanism was designed with the existing planned expansion in mind, and it already fails to accommodate that expansion. This is not a future risk — it is a present design contradiction documented in the implementation summary itself.

The three-month reversion deadline has no technical enforcement. Nothing in the CI pipeline, pre-commit hooks, or test suite verifies that an exception was reverted within three months. The duration condition is entirely self-policing, which is the same enforcement model that failed to prevent the original silent ceiling breach.

The "consolidation plan required" condition cannot be enforced before the exception is invoked. An ADR can assert a consolidation plan exists without the plan being technically sound or achievable.

**Verdict:** The exception mechanism codifies a procedural workaround for the ceiling that the implementation immediately needs to invoke. Its five conditions are almost entirely unenforceable. It is a documented loophole, not a controlled gate.

---

### Challenge 5: Does the zero-headroom problem make this whole effort pointless?

**The claim:** EN-002 "successfully addressed both discoveries" and the ceiling is now at its principled value of 25.

**The challenge:**

The implementation lands at 25/25 — zero headroom. The implementation summary acknowledges this explicitly: "Zero headroom (25/25) blocks EN-001 H-32..H-35 — Active risk." This is not a residual risk; it is the primary outcome of the work. EN-002 solved the wrong problem.

The project's motivation was to create space for H-32..H-35 from PROJ-007. EN-002 reduced the count from 31 to 25 — but the derived ceiling is also 25. Net available headroom for H-32..H-35: zero. The work consumed significant engineering effort (7 tasks, 11+ files modified, ~3400 tests run) to arrive at precisely the same blocked state: no room for the new rules.

The counter-argument is that EN-002 replaced an unprincipled ceiling with a principled one, which is valuable independent of headroom. This is correct but incomplete: the principled ceiling is useless if the first thing that must happen to use the framework is to exceed it via the exception mechanism. The derivation was completed, the exception mechanism was designed, and the exception mechanism must immediately be invoked. This suggests the derivation's ceiling is too tight for the system's actual operational requirements.

The zero-headroom state also means that any future HARD rule addition — for any reason — requires a C4-reviewed ADR and exception mechanism invocation. EN-002 has maximally constrained future governance agility in the name of principled ceilings.

**Verdict:** EN-002 successfully executed the work it was scoped to do, but that scope did not solve the upstream problem that motivated the work. The zero-headroom result means the immediate next step (EN-001 TASK-016) requires invoking the exception mechanism that EN-002 itself built. The circular dependency is a design smell.

---

## S-004 Pre-Mortem

It is August 2026 — six months after EN-002 was merged. EN-002 has failed. We are conducting a retrospective to understand what went wrong.

---

### Failure Scenario 1: The Exception Mechanism Was Invoked Immediately and Never Reverted

Within two weeks of EN-002 merging, TASK-016 (H-32..H-35) required the exception mechanism. A C4 ADR was filed, the ceiling was raised to 29, and the L5 gate was updated. The three-month reversion deadline passed. The deadline had no technical enforcement — it was a comment in the ADR. No one filed the follow-up consolidation work because the team had moved on to other priorities.

Six months later, the ceiling is still at 29 with 29 rules. The exception became permanent. The principled ceiling of 25 is now historical text in a derivation document. The L5 gate enforces 29, which was itself set ad-hoc to accommodate an immediate need. The framework is structurally identical to the pre-EN-002 state: an unprincipled ceiling set to accommodate the current count.

**What went wrong:** The exception mechanism had no technical reversion enforcement. The three-month deadline was honor-system governance. Honor-system governance fails under competing project priorities — the same root cause that produced the original silent breach from 25 to 35.

---

### Failure Scenario 2: Directory Globbing Caused Silent Enforcement Degradation

A developer added a new rule file to `.context/rules/` for a new skill. The file contained well-intentioned L2-REINJECT markers with rank=1 and rank=2 — the same ranks used by the constitutional rules. The engine now processes this file and the new markers compete with the constitutional constraints for the top ranks. Because the sort is global across all markers from all files, the new file's rank=1 marker displaces an existing rank=1 marker.

The displacement was not detected because:
1. No test validates the actual rank ordering of markers across files in the live rules directory
2. The L2 budget was at 65.8% utilization — all markers still fit, so no truncation occurred
3. The token estimate remained within budget — no alert was triggered

The constitutional constraint (H-01, H-02, H-03) was downgraded in effective priority without any developer being aware. Over weeks, compliance degraded subtly. The failure mode was invisible because the L5 gate only checks rule count, not marker quality or ordering.

**What went wrong:** The directory glob is unconditional. New files are processed without explicit opt-in. Rank collision across files has no detection mechanism. The fail-open design that protects against individual file errors also prevents detection of rank-ordering violations.

---

### Failure Scenario 3: Compound Rules Were Systematically Misapplied

H-07 (architecture layer isolation) consolidated three rules: domain imports, application imports, and composition root. Over six months, the LLM consistently enforced the domain import restriction (the first and most memorable sub-item) but sporadically missed the application import restriction and the composition root exclusivity requirement.

This was empirically measurable: code reviews began catching application-layer violations that previously would have been caught by H-08 as a standalone rule. The compound rule degraded enforcement of its later sub-items in proportion to context length.

The two-tier model classified H-07 as Tier A (L2-protected). The L2 marker for architecture-standards says "domain/ MUST NOT import application/" — which covers only the first sub-item. The marker content does not reinforce the application-layer or composition root sub-items. The L2 injection is structurally misaligned with the compound rule it claims to cover.

**What went wrong:** The consolidation rationale assumed compound rules would be enforced at parity with atomized rules. The L2 marker content was not updated to cover all sub-items of the compound rules. The Tier A classification promised L2 protection that the marker content did not deliver.

---

### Failure Scenario 4: The Cognitive Load Derivation Was Wrong

The ceiling of 25 was derived from cognitive load research that cited "20-25 rules as the practical upper bound for reliable enforcement." By August 2026, empirical measurement (prompted by persistent rule violations) showed that the effective enforcement reliability dropped significantly above 15-18 rules — not 25. The derivation was based on theoretical LLM capacity, not measured performance on the actual rule corpus.

The result: the framework is operating above the actual effective ceiling. All rules from H-13 onward in the L2 preamble show statistically lower compliance rates than H-01 through H-12, consistent with attention decay in a long rule injection.

**What went wrong:** The derivation's Constraint Family C ("instruction-following capacity ~25 total with partitioning") was theoretical. The actual measurement data was explicitly deferred by DEC-005. By the time measurement revealed the error, the ceiling was already enshrined with documented derivation, making it politically difficult to reduce.

---

### Failure Scenario 5: The L5 Gate Was Bypassed During a Hotfix

A production incident required an emergency rule addition. The hotfix process bypassed pre-commit hooks with `--no-verify` (an explicitly forbidden action under H-02, but enforceable only by the LLM — itself under context rot from the hotfix context). The ceiling was breached silently. The hotfix merged without triggering the L5 gate.

The L5 gate is implemented as a pre-commit hook. Pre-commit hooks are bypassable by any developer with local git access. The test suite includes `test_actual_file_count_within_ceiling` — but this test uses a relative path `Path(".context/rules/quality-enforcement.md")` and is skippable (`pytest.skip` if not found). The CI pipeline may not run this specific test class under all conditions.

**What went wrong:** The L5 gate's "immune to context rot" property assumes the hook runs. The hook is bypassable. The test that validates the actual file is skip-capable and path-dependent. The detection mechanism has gaps that are invisible during normal operation.

---

### Failure Scenario 6: Rule Count Became a Proxy for Enforcement Quality

EN-002's success was measured by: rule count reduced (31→25), L2 coverage increased (32%→84%), L5 gate added. These are structural metrics, not outcome metrics. No measurement was taken of actual rule compliance rates before or after EN-002.

By August 2026, the team had internalized "25 rules, 84% coverage" as the quality target. The framework was considered compliant if the count was at or below 25. No systematic measurement of actual enforcement failures was ever performed. The framework optimized for metric compliance, not behavioral outcome.

The enforcement effectiveness report (TASK-028) explicitly acknowledges this: it measures "H-rules with L2 coverage" as a proxy for enforcement, not actual compliance rates. DEC-005 deferred empirical measurement. That measurement was never scheduled as concrete follow-up work. Six months later, it still has not been done.

**What went wrong:** The success criteria were structural proxies, not outcome measurements. Proxy optimization without outcome validation is a known failure mode in engineering governance.

---

## Findings

### CRITICAL

| ID | Category | Finding | Source Scenario |
|----|----------|---------|-----------------|
| F-001 | Exception Mechanism | The exception mechanism's three-month reversion deadline has no technical enforcement. It will silently expire under competing priorities, reproducing the original ceiling breach failure mode. | S-004-01 |
| F-002 | L5 Gate | Pre-commit hooks are bypassable with `--no-verify`. The L5 gate's "immune to context rot" claim applies to normal operation only; hotfix bypass paths are unprotected. The test that validates the actual file uses a relative path and is skip-capable. | S-004-05 |
| F-003 | Exception Scope | TASK-016 (H-32..H-35) requires N=4 additional slots, which already exceeds the stated exception maximum of N<=3. The exception mechanism cannot accommodate the immediate use case it was designed for without violating its own rules. | S-002-04 |
| F-004 | Zero Headroom | EN-002 lands at 25/25 — the principled ceiling with zero headroom. This means the first action required after EN-002 completion is to invoke the exception mechanism that EN-002 built. The work did not create the headroom that motivated it. | S-002-05 |

---

### MAJOR

| ID | Category | Finding | Source Scenario |
|----|----------|---------|-----------------|
| F-005 | Compound Rule Enforcement | The L2 marker content for consolidated rules does not cover all sub-items. The architecture-standards marker covers only the domain import restriction. H-07's application-layer and composition root sub-items are not reinforced in the L2 injection. The Tier A classification for H-07 is unsupported by the marker content. | S-004-03, S-002-02 |
| F-006 | Ceiling Derivation | The ceiling of 25 was derived from three constraint families, but the families produced overlapping ranges (14-28+), and 25 was selected because it matches the achievable post-consolidation count. The derivation is rationalization of a practical outcome, not independent analysis. | S-002-01 |
| F-007 | Directory Globbing | The engine's unconditional directory glob creates a forward-compatibility risk. New rule files added by future developers are automatically enrolled in L2 processing without opt-in. Rank collision across files has no detection mechanism. | S-004-02 |
| F-008 | Empirical Validation Absent | The cognitive load constraint family cited "20-25 rules" without reference to measured LLM performance on the actual rule corpus. The effective ceiling may be materially lower. DEC-005 deferred measurement; no concrete follow-up schedule was created. | S-004-04, S-002-03 |

---

### MINOR

| ID | Category | Finding | Source Scenario |
|----|----------|---------|-----------------|
| F-009 | Budget Circularity | The L2 budget was raised from 600 to 850 to accommodate the engine expansion, and the engine expansion was justified by the budget increase. Neither change was derived independently. The 850 token budget has no principled derivation analogous to the ceiling derivation. | S-002-03 |
| F-010 | Self-Certification | The C4 tournament on the ceiling derivation was conducted by the same orchestrator that produced the derivation. The 0.95 PASS score reflects the orchestrator's own assessment of the orchestrator's work. No external validator reviewed the derivation. | S-002-01 |
| F-011 | Tier B Compensating Controls | H-04, H-16, H-17, H-18 are classified as Tier B with "adequate enforcement through deterministic mechanisms." However, H-16 (steelman before critique) and H-17 (quality scoring) are enforced by the `/adversary` skill — an LLM-mediated control that is itself vulnerable to context rot. The "deterministic" characterization is inaccurate for these two rules. | S-002-02 |
| F-012 | Test Path Dependency | `test_actual_file_count_within_ceiling` uses `Path(".context/rules/quality-enforcement.md")` — a relative path. If the test is executed from a directory other than the project root (e.g., in a CI environment with a non-standard working directory), it silently skips via `pytest.skip`. The L5 validation test may silently not run. | S-004-05 |

---

### OBSERVATION

| ID | Category | Finding |
|----|----------|---------|
| F-013 | Success Criteria | EN-002's success metrics (rule count, L2 coverage percentage, L5 gate active) are structural proxies. No outcome metrics (actual rule compliance rates, violation frequency by rule) were established or measured. The framework may have optimized the proxy without improving the outcome. |
| F-014 | Backward Compatibility | The engine's `is_file()` / `is_dir()` branching preserves backward compatibility for single-file callers. However, the `_find_rules_path` fallback returns `quality-enforcement.md` only if the `.claude/rules/` directory does not exist. In any environment where the symlink is broken or missing, the engine silently reverts to single-file mode — with no alert or log message differentiating this from intentional single-file use. |
| F-015 | ADR-EPIC002-002 Not Updated | The implementation summary states "L2 budget 600→850" was updated in `quality-enforcement.md`, but does not mention updating `ADR-EPIC002-002` (the baselined ADR that declared the 600-token budget). Modifying a baselined ADR is auto-C4 per AE-004. If ADR-EPIC002-002 was not updated, the ADR and the SSOT are inconsistent. If it was updated, an untracked auto-C4 governance event occurred. |
| F-016 | Deferred Work Without Schedule | DEC-005 (measure before optimizing) deferred empirical measurement as follow-up work. The worktracker and implementation summary do not reference a specific future task, epic, or deadline for this measurement. Deferred work without scheduled follow-up is systematically lost. |
