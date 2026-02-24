# C4 Tournament Execution Report: HARD Rule Budget Upper Boundary Derivation

> **Tournament Mode:** C4 Critical -- all 10 strategies required (9 non-scoring executed here)
> **Deliverable:** `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/adversary/hard-rule-budget/hard-rule-budget-upper-boundary-derivation.md`
> **Criticality:** C4 (Critical) -- governance constraint affecting constitutional enforcement architecture
> **Executor:** adv-executor (C4 tournament)
> **Date:** 2026-02-21
> **Execution ID:** 20260221T-C4T

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Tournament Summary](#tournament-summary) | Aggregate findings across all 9 strategies |
| [S-010: Self-Refine](#s-010-self-refine) | Self-review of the derivation |
| [S-003: Steelman](#s-003-steelman) | Strengthen the best version of the argument |
| [S-002: Devil's Advocate](#s-002-devils-advocate) | Challenge assumptions and key claims |
| [S-004: Pre-Mortem](#s-004-pre-mortem) | Imagine adoption failure scenarios |
| [S-001: Red Team](#s-001-red-team) | Adversarial exploitation of attack surfaces |
| [S-007: Constitutional AI](#s-007-constitutional-ai) | Constitutional compliance check |
| [S-011: Chain-of-Verification](#s-011-chain-of-verification) | Verify factual claims against evidence |
| [S-012: FMEA](#s-012-fmea) | Failure Mode and Effects Analysis |
| [S-013: Inversion](#s-013-inversion) | Invert key claims to find blind spots |
| [Cross-Strategy Synthesis](#cross-strategy-synthesis) | Patterns across strategies |
| [Tournament Verdict](#tournament-verdict) | Overall PASS/REVISE/REJECT determination |

---

## Tournament Summary

| Strategy | Findings | Critical | Major | Minor | Observation | Blocking? |
|----------|----------|----------|-------|-------|-------------|-----------|
| S-010 Self-Refine | 6 | 0 | 3 | 2 | 1 | No |
| S-003 Steelman | 5 | 0 | 3 | 2 | 0 | No |
| S-002 Devil's Advocate | 7 | 1 | 4 | 2 | 0 | **Yes** |
| S-004 Pre-Mortem | 6 | 1 | 3 | 1 | 1 | **Yes** |
| S-001 Red Team | 5 | 1 | 3 | 1 | 0 | **Yes** |
| S-007 Constitutional AI | 4 | 0 | 2 | 2 | 0 | No |
| S-011 Chain-of-Verification | 7 | 2 | 3 | 2 | 0 | **Yes** |
| S-012 FMEA | 8 | 1 | 4 | 3 | 0 | **Yes** |
| S-013 Inversion | 6 | 1 | 3 | 1 | 1 | **Yes** |
| **TOTAL** | **54** | **7** | **28** | **16** | **3** | **6 of 9 strategies block** |

**Aggregate Assessment:** The derivation is methodologically sound in its multi-constraint approach and arrives at a defensible conclusion. However, 7 CRITICAL findings across 6 strategies reveal factual inaccuracies in the L2-REINJECT claim counts, a missing sensitivity analysis, and a gap between the "25 rule" conclusion and the binding constraint that actually supports ~14. These must be resolved before the derivation can serve as a governance basis for changing the HARD rule ceiling.

---

## S-010: Self-Refine

**Strategy:** S-010 Self-Refine (Madaan et al. 2023)
**Execution Date:** 2026-02-21
**Objectivity Check:** Low attachment (first review). Proceeding.

### Findings

| ID | Finding | Classification | Affected Dimension |
|----|---------|---------------|-------------------|
| SR-001-20260221T-C4T | The derivation claims "5 independent constraints" but Constraint 4 (Signal Quality) explicitly cites Constraints 1, 3, and the original EN-404 design as corroborating evidence. If three constraints converge because they drew on overlapping analyses (the nse-risk-001 assessment likely incorporated ManyIFEval data), the "independence" is overstated. | MAJOR | Methodological Rigor |
| SR-002-20260221T-C4T | The "mean per-HARD-rule L1 cost" calculation (14,245 / 31 = ~410 tokens) includes non-rule content in the numerator (the files contain MEDIUM/SOFT standards, examples, metadata) but divides by the rule count only. This inflates per-rule cost. The derivation acknowledges "includes non-rule content" but then uses 410 tokens/rule in subsequent calculations without adjusting. | MAJOR | Evidence Quality |
| SR-003-20260221T-C4T | Constraint 5 (Rule Conflict Probability) provides no empirical data on actual conflict frequency -- only a combinatorial formula showing potential interactions. The three "observed conflicts" cited (H-16/H-14, H-20/prototyping, H-25..H-30 overlap) are assertions without evidence of operational impact. | MAJOR | Evidence Quality |
| SR-004-20260221T-C4T | The consolidation path (H-25..H-30 -> 2 rules, H-07..H-09 -> 1 rule) is proposed but no draft compound rules are provided. Whether 6 HARD rules can be meaningfully consolidated into 3 without losing enforcement specificity is unproven. | MINOR | Actionability |
| SR-005-20260221T-C4T | The quality threshold in the document header states ">= 0.95" but quality-enforcement.md SSOT states ">= 0.92 for C2+". The derivation applies a self-imposed higher threshold with no justification for the deviation. | MINOR | Internal Consistency |
| SR-006-20260221T-C4T | No sensitivity analysis exists for the "25" number. The derivation presents point estimates from each constraint without exploring what happens if key parameters change (e.g., if L2 budget increases to 900 tokens, or if L1 enforcement gets a 20% budget increase). | OBSERVATION | Completeness |

**Blocking:** No. No individual finding invalidates the core methodology or conclusion. Major findings require revision but the derivation approach is sound.

---

## S-003: Steelman

**Strategy:** S-003 Steelman Technique (Davidson 1973, Principle of Charity)
**Execution Date:** 2026-02-21
**H-16 Compliance:** S-003 runs before all critique strategies (confirmed).

### Charitable Interpretation

The derivation's core argument is strong: the current HARD rule ceiling of 35 lacks principled derivation, and the 5-constraint approach (token budget, L2 coverage, instruction-following research, signal quality, rule conflicts) represents a legitimate multi-perspective analysis. The convergence of independent analyses on the 20-25 range is genuinely persuasive. The two-tier model (Tier A: L2-protected, Tier B: L1-only) is an original contribution that resolves the tension between "how many rules can we reliably enforce" (14) and "how many rules do we need" (25+).

### Improvement Findings

| ID | Finding | Classification | Affected Dimension |
|----|---------|---------------|-------------------|
| SM-001-20260221T-C4T | The argument would be stronger if it explicitly modeled the "rule activation profile" -- which rules are co-activated by task type. The derivation notes this (line 166: "a given interaction might activate 5-8 HARD rules") but does not systematically profile it. Adding a table of 4-5 representative task types with their activated rule sets would transform the instruction-following analysis from suggestive to demonstrative. | MAJOR | Evidence Quality |
| SM-002-20260221T-C4T | The "original EN-404 design" (E-009, Constraint 0) mention is buried in Constraint 4 analysis. This is the strongest single piece of evidence (the original designer independently chose <= 25 before any rules existed). It should be elevated to a standalone constraint or featured prominently in the synthesis. | MAJOR | Methodological Rigor |
| SM-003-20260221T-C4T | The two-tier model would benefit from explicit criteria for Tier A vs Tier B classification. Currently, Tier A is described as "rules whose violation causes irreversible or systemic harm" -- but H-20 (test-first BDD) and H-21 (90% coverage) are arguably systemic yet would likely be Tier B. Explicit classification criteria with edge cases would strengthen the recommendation. | MAJOR | Actionability |
| SM-004-20260221T-C4T | The rule conflict analysis (Constraint 5) could be strengthened by referencing actual semantic conflict detection methods (formal methods, constraint satisfaction) rather than just the pairwise combinatorial formula. Even noting that no formal conflict resolution mechanism exists makes the argument stronger. | MINOR | Evidence Quality |
| SM-005-20260221T-C4T | The ManyIFEval citation (arXiv:2509.21051) has a date format suggesting September 2025, which is consistent with publication timing. The data quality of all 4 research citations is strong. | MINOR | Traceability |

**Blocking:** No. The derivation is already strong; these improvements would elevate it further.

---

## S-002: Devil's Advocate

**Strategy:** S-002 Devil's Advocate (Nemeth 2018, Janis 1982)
**Execution Date:** 2026-02-21
**H-16 Compliance:** S-003 Steelman executed first (confirmed above).

### Assumptions Challenged

1. **Explicit:** "L2 re-injection is the primary defense against context rot for critical rules" (line 129)
2. **Explicit:** "5 independent constraints" (line 62)
3. **Implicit:** That the research studies on instruction-following degradation apply to the Jerry enforcement architecture
4. **Implicit:** That rule consolidation preserves enforcement equivalence
5. **Implicit:** That the 25-rule boundary is optimal rather than merely a convergence point

### Findings

| ID | Finding | Classification | Affected Dimension |
|----|---------|---------------|-------------------|
| DA-001-20260221T-C4T | **The gap between the binding constraint (14) and the recommendation (25) is not justified.** The derivation identifies L2 coverage as the binding constraint at ~14 rules, then recommends 25 by introducing a two-tier model. But the two-tier model effectively admits that 11 of 25 "HARD" rules have no protection against context rot. The derivation itself states: "Rules without L2 coverage are effectively MEDIUM in enforcement reliability, despite being labeled HARD" (line 140). If this is true, recommending 25 HARD rules with only 14 being truly enforceable is recommending 14 HARD rules and 11 MEDIUM rules relabeled as HARD. This is a core logical inconsistency. | CRITICAL | Internal Consistency |
| DA-002-20260221T-C4T | **ManyIFEval data is misapplied.** The derivation cites "5-10 simultaneous constraints as the practical ceiling" from ManyIFEval, then argues the L2-protected 10-12 rules are "within the 5-10 range" (line 174). But L2 re-injection re-injects rule summaries (~50 tokens each), not full constraint specifications. The compliance data in ManyIFEval measures following fully-specified instructions, not token-compressed summaries. The L2 markers compress rules to approximately 10% of their full specification. Whether compressed re-injections achieve the same compliance as full specifications is untested. | MAJOR | Evidence Quality |
| DA-003-20260221T-C4T | **The token budget analysis contradicts itself.** Constraint 1 concludes "25-40 rules" at current overhead or "18-25 rules" if isolated, then declares this "not the binding constraint." But the very next constraint (L2 coverage) identifies 14 as the binding number. If token budget supports 18-25 and L2 supports 14, the recommendation of 25 exceeds BOTH the binding constraint AND the upper range of the "isolated" token budget estimate. | MAJOR | Internal Consistency |
| DA-004-20260221T-C4T | **The "original EN-404 design intent" (E-009) is given evidential weight it does not deserve.** A designer's pre-empirical cap of <= 25 is not evidence -- it is a prior belief that was itself overridden in practice (commit 936d61c raised it to 35). The fact that the designer chose 25 and it was later raised suggests 25 was too restrictive, not that 35 was wrong. Using the overridden value as corroboration is selection bias. | MAJOR | Evidence Quality |
| DA-005-20260221T-C4T | **No empirical measurement of context rot impact on L1-only rules.** The derivation asserts that L1-only rules are "VULNERABLE" to context rot (line 129, 132, 176) but provides no measurement of actual compliance degradation over session lifetime. The CRR rating (1-2) from ADR-EPIC002-002 is a risk assessment score, not an empirical measurement. Without before/after compliance data, the vulnerability claim is a theoretical risk, not a demonstrated problem. | MAJOR | Evidence Quality |
| DA-006-20260221T-C4T | **The "two-tier model" is presented as a resolution but is actually a concession.** Calling Tier B rules "HARD" when they have no L2 protection creates a governance fiction. Users reading quality-enforcement.md see "HARD rules CANNOT be overridden" but the derivation reveals that 13 of 25 HARD rules CAN be effectively overridden by context rot. The honest solution is either: (a) reduce to 14 truly HARD rules, or (b) acknowledge that "HARD" has two enforcement levels and document this distinction in the constitution. | MINOR | Completeness |
| DA-007-20260221T-C4T | **Consolidation arithmetic is internally contradictory.** Section "What This Means for PROJ-007's H-32..H-35" shows: consolidate (31 -> 25), then add 4 rules (25 -> 29), arriving at "over the 25 ceiling by 4." This demonstrates that the derived ceiling of 25 is immediately insufficient for the project that motivated the analysis. If the derivation's own sponsor cannot fit within the derived ceiling, the ceiling may be wrong. | MINOR | Actionability |

**Blocking:** **Yes.** DA-001 is CRITICAL: the logical gap between the binding constraint (14) and the recommendation (25) undermines the derivation's methodological integrity. The two-tier model either means 14 rules are truly HARD (and 11 are MEDIUM-relabeled) or the L2 binding constraint is not actually binding. The derivation must resolve this fundamental tension.

---

## S-004: Pre-Mortem

**Strategy:** S-004 Pre-Mortem Analysis (Klein 1998, Kahneman 2011)
**Execution Date:** 2026-02-21
**H-16 Compliance:** S-003 Steelman executed first (confirmed).

### Failure Scenario Declaration

"It is August 2026. The HARD rule ceiling was reduced from 35 to 25 based on this derivation. Six months later, the enforcement architecture has degraded: three legitimate governance needs were blocked by the ceiling, two 'consolidated' compound rules proved unenforceable, and the Tier A/Tier B distinction created confusion about which rules actually matter. The team reverted to an ad-hoc ceiling of 30."

### Findings

| ID | Finding | Classification | Affected Dimension |
|----|---------|---------------|-------------------|
| PM-001-20260221T-C4T | **Consolidation destroys enforcement granularity.** The derivation proposes consolidating H-25..H-30 (6 skill standard rules) into 2 compound rules. In practice, compound rules like "MUST follow skill naming (kebab-case folder, SKILL.md exact case, no README.md) AND registration (CLAUDE.md, AGENTS.md)" are harder to enforce deterministically (L3 AST checks work on specific patterns, not compound English sentences) and harder for agents to self-check (L1/L2 coverage of a compound rule requires remembering multiple sub-constraints). | CRITICAL | Methodological Rigor |
| PM-002-20260221T-C4T | **The ceiling creates perverse incentives for rule avoidance.** A 25-rule ceiling means every new HARD rule requires either consolidation or demotion of an existing rule. Project teams will be incentivized to avoid proposing HARD rules (classifying genuinely critical constraints as MEDIUM to avoid the budget fight), leading to under-enforcement of important constraints. | MAJOR | Completeness |
| PM-003-20260221T-C4T | **Tier A/Tier B distinction creates a two-class system without governance.** The derivation proposes Tier A (L2-protected) and Tier B (L1-only) but provides no governance mechanism for tier assignment disputes. When PROJ-007 wants H-32 in Tier A but the L2 budget has 0 remaining tokens, there is no resolution process. This will cause governance deadlocks. | MAJOR | Actionability |
| PM-004-20260221T-C4T | **The research evidence has a generalizability gap.** ManyIFEval and AGENTIF measure instruction-following in general-purpose tasks. The Jerry enforcement architecture has structural properties (L2 re-injection, domain partitioning, session-start loading) specifically designed to overcome the limitations these studies document. Applying general LLM research to a purpose-built enforcement system without accounting for the system's mitigations overstates the constraint. | MAJOR | Evidence Quality |
| PM-005-20260221T-C4T | **The derivation does not model the cost of under-enforcement.** It models the cost of too many rules (enforcement quality degradation) but not the cost of too few rules (governance gaps, unconstrained agent behavior, quality regression). An optimal ceiling should minimize total cost (over-enforcement + under-enforcement), not just minimize one side. | MINOR | Completeness |
| PM-006-20260221T-C4T | **The implementation path has no rollback plan.** Steps 1-7 propose irreversible changes to quality-enforcement.md (consolidating rules, changing the ceiling, updating L2 markers). If the 25-rule ceiling proves too restrictive, there is no documented reversal path. The implementation itself is a C4 change without a C4-level rollback strategy. | OBSERVATION | Methodological Rigor |

**Blocking:** **Yes.** PM-001 is CRITICAL: if compound rules cannot be enforced at the same granularity as the rules they replace, the consolidation path is invalid, and the "31 -> 25" reduction is not achievable without enforcement loss.

---

## S-001: Red Team

**Strategy:** S-001 Red Team Analysis (Zenko 2015, MITRE ATT&CK adaptation)
**Execution Date:** 2026-02-21
**H-16 Compliance:** S-003 Steelman executed first (confirmed).

### Threat Actor Profile

**Goal:** Exploit the derivation to either (a) permanently weaken the quality framework by reducing the HARD rule count below what is needed, or (b) create a governance logjam that prevents any new HARD rules from being added.
**Capability:** Full access to the codebase, understands the enforcement architecture, can cite the derivation's own logic to justify weakening rules.
**Motivation:** Reduce quality overhead to ship faster; or conversely, weaponize the ceiling to block governance improvements.

### Findings

| ID | Finding | Classification | Affected Dimension |
|----|---------|---------------|-------------------|
| RT-001-20260221T-C4T | **The 25-rule ceiling can be weaponized to block legitimate governance.** An adversary wanting to prevent a new HARD rule (e.g., a security constraint) can point to the derivation and say "we're at 25/25, you need to consolidate or demote an existing rule first." The consolidation requirement creates a procedural barrier that can be used to delay or block governance improvements indefinitely. The derivation provides no exception mechanism for critical governance needs. | CRITICAL | Completeness |
| RT-002-20260221T-C4T | **Tier B classification can be used to argue for demotion.** An adversary can argue: "The derivation itself says Tier B rules are 'effectively MEDIUM in enforcement reliability' (line 140). Since they are effectively MEDIUM, let us formally demote them to MEDIUM and free HARD rule slots." This is the derivation's own logic turned against it -- if Tier B rules are not truly HARD, they should not count against the HARD budget. | MAJOR | Internal Consistency |
| RT-003-20260221T-C4T | **The consolidation path creates attack surface for semantic weakening.** When H-25..H-30 (6 specific, enforceable rules) become 2 compound rules, the consolidated version inevitably uses more abstract language. An adversary can later argue that the abstract compound rule does not cover a specific case that was previously explicitly addressed by one of the 6 original rules. Consolidation is a one-way ratchet toward ambiguity. | MAJOR | Evidence Quality |
| RT-004-20260221T-C4T | **The research citations can be cherry-picked to argue for ANY ceiling.** ManyIFEval shows 5-10 as the range; AGENTIF shows 11.9; nse-risk-001 shows 20-25. An adversary wanting a ceiling of 10 can cite ManyIFEval exclusively. An adversary wanting 30 can argue domain partitioning overcomes the research limits. The derivation's synthesis is one interpretation of heterogeneous data, not a unique derivation. | MAJOR | Methodological Rigor |
| RT-005-20260221T-C4T | **No mechanism prevents silent re-raising of the ceiling.** The derivation documents that the original ceiling (25) was "silently exceeded" (line 52). No enforcement mechanism is proposed to prevent this from happening again with the new ceiling of 25. Without a deterministic L3 gate that rejects commits exceeding 25 HARD rules, the ceiling is advisory, not enforceable. | MINOR | Actionability |

**Blocking:** **Yes.** RT-001 is CRITICAL: the derivation proposes a hard governance ceiling without an exception or override mechanism, creating a tool that can be weaponized to block legitimate governance. Every governance ceiling needs an escape valve.

---

## S-007: Constitutional AI

**Strategy:** S-007 Constitutional AI Critique (Bai et al. 2022)
**Execution Date:** 2026-02-21

### Constitutional Context Loaded

- `JERRY_CONSTITUTION.md` (P-001 through P-043)
- `quality-enforcement.md` (H-01 through H-31)
- `markdown-navigation-standards.md` (H-23, H-24)

### Findings

| ID | Finding | Classification | Affected Dimension |
|----|---------|---------------|-------------------|
| CC-001-20260221T-C4T | **H-23 (Navigation table) and H-24 (Anchor links): COMPLIANT.** The derivation includes a Document Sections table with anchor links for all major sections. No violation. However, note that the HARD Rule Index in quality-enforcement.md lists H-01 through H-31 (31 rules), not 24 as referenced in the S-007 template's context requirements (which were written before H-25..H-31 were added). The deliverable correctly references 31 current rules. | OBSERVATION (not a finding against the deliverable) | N/A |
| CC-002-20260221T-C4T | **H-31 (Clarify when ambiguous): Potential tension.** The derivation recommends a specific number (25) without exploring the sensitivity range. Given that the constraints produce ranges (18-25, 14, 10-12, 20-25), the choice of the upper end (25) of the overlapping range is an interpretation, not a unique derivation. H-31 requires clarification when "multiple valid interpretations exist." The derivation should acknowledge that any number in the 20-25 range is equally defensible. | MAJOR | Methodological Rigor |
| CC-003-20260221T-C4T | **P-020 (User Authority): The derivation proposes changing a governance constant (the HARD rule ceiling) which directly affects all users.** P-020 mandates "NEVER override user intent." The derivation recommends reducing from 35 to 25, which would constrain the ability of future users to add HARD rules. This is a governance change requiring explicit user authorization per the constitution. The derivation correctly tags this as C4, but does not explicitly reference P-020 in its constitutional compliance narrative. | MAJOR | Traceability |
| CC-004-20260221T-C4T | **AE-002 applicability: COMPLIANT.** The derivation correctly identifies its implementation steps as C3 (AE-002) since they touch `.context/rules/`. The derivation itself is classified as C4, which is appropriate given it proposes changing a governance constant. | MINOR | N/A |
| CC-005-20260221T-C4T | **H-14 (Creator-critic-revision cycle, minimum 3 iterations): Status noted.** The deliverable is marked "DRAFT (iteration 1)." H-14 requires minimum 3 iterations for C2+ deliverables. This is not a violation (the derivation explicitly states it is iteration 1), but it must complete 2 more iterations before it can be accepted. | MINOR | Methodological Rigor |

**Constitutional Compliance Score:** 1.00 - (0 x 0.10 + 2 x 0.05 + 2 x 0.02) = 0.86 (REVISE band)

**Blocking:** No. No HARD rule violations. Two MEDIUM-level concerns (H-31 ambiguity acknowledgment and P-020 explicit reference) require revision but do not invalidate the deliverable.

---

## S-011: Chain-of-Verification

**Strategy:** S-011 Chain-of-Verification (Dhuliawala et al. 2023)
**Execution Date:** 2026-02-21
**Claims Extracted:** 12 | **Verified:** 5 | **Discrepancies:** 7

### Verification Protocol

Each claim was extracted, a verification question was generated, and the source document was read independently to answer the question.

### Findings

| ID | Finding | Classification | Affected Dimension |
|----|---------|---------------|-------------------|
| CV-001-20260221T-C4T | **Claim:** "H-rules with L2 coverage: 10 (H-01..H-03, H-05, H-06, H-13..H-15, H-19, H-31)" (line 123). **Source:** L2-REINJECT markers in `.context/rules/quality-enforcement.md`. **Independent verification:** quality-enforcement.md contains 8 L2-REINJECT markers, not 10. The markers cover: (1) H-01/H-02/H-03 (rank=1), (2) H-13/H-14 (rank=2), (3) H-31 (rank=2), (4) H-05/H-06 (rank=3), (5) S-014 leniency (rank=4), (6) H-15/S-010 (rank=5), (7) criticality levels (rank=6), (8) H-19 governance escalation (rank=8). While these 8 markers reference the listed H-rules, the count of "L2-protected H-rules" depends on interpretation: each marker may reference multiple H-rules. The claim of "10" appears to count individual H-rules mentioned across markers, which is defensible but conflates "L2 marker count" with "H-rule coverage count." | CRITICAL | Evidence Quality |
| CV-002-20260221T-C4T | **Claim:** "Engine reads from quality-enforcement.md only" (line 125). **Source:** `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py`. **Independent verification:** CONFIRMED. The engine's `_find_rules_path` method (line 243) constructs path to `.context/rules/quality-enforcement.md` only. However, L2-REINJECT markers ALSO exist in 8 other rule files (architecture-standards.md, skill-standards.md, python-environment.md, coding-standards.md, markdown-navigation-standards.md, mcp-tool-standards.md, testing-standards.md, mandatory-skill-usage.md) -- 8 additional markers with 8 additional H-rules. The derivation correctly identifies the engine limitation but understates the total L2-REINJECT marker ecosystem: there are 16 markers total across 9 files, not just 8 in one file. | CRITICAL | Completeness |
| CV-003-20260221T-C4T | **Claim:** "L1 enforcement budget (target): 12,476 tokens" (line 83). **Source:** ADR-EPIC002-002. **Independent verification:** The derivation cites this as sourced from ADR-EPIC002-002 (E-001). The value 12,476 is referenced in multiple downstream documents. However, the derivation also states "Total enforcement budget: 15,126 tokens (7.56%)" while quality-enforcement.md states "Total enforcement budget: ~15,100 tokens (7.6% of 200K context)." The derivation uses a more precise number (15,126 vs ~15,100). Both are within rounding tolerance, but the precision mismatch suggests the derivation may be citing a different source version. | MINOR | Traceability |
| CV-004-20260221T-C4T | **Claim:** "Current L2 markers (quality-enforcement.md only): 8 markers, 415 declared tokens" (line 122). **Source:** L2-REINJECT markers in quality-enforcement.md. **Independent verification:** Counting declared tokens across the 8 markers: rank=1 (50) + rank=2 (90) + rank=2 (50) + rank=3 (25) + rank=4 (30) + rank=5 (30) + rank=6 (100) + rank=8 (40) = **415 tokens**. VERIFIED. The declared token count matches. | VERIFIED | N/A |
| CV-005-20260221T-C4T | **Claim:** "ManyIFEval (arXiv:2509.21051, 2025): 5 simultaneous instructions: 32-72% accuracy. 10 instructions: 2-39% accuracy" (line 156). **Source:** arXiv paper. **Independent verification:** Cannot directly verify the exact percentages without reading the paper, but the arXiv ID 2509.21051 is formatted correctly for a September 2025 submission. The ranges cited (32-72% at 5, 2-39% at 10) are plausible given known instruction-following research. Marked as UNVERIFIABLE at the exact-value level but PLAUSIBLE at the directional level. | MAJOR | Evidence Quality |
| CV-006-20260221T-C4T | **Claim:** "AGENTIF (arXiv:2505.16944, NeurIPS 2025): 11.9 constraints avg: <30% perfect compliance across all models. Best model (o1-mini): 59.8% constraint success rate" (line 157). **Source:** arXiv paper. **Independent verification:** Same as CV-005 -- cannot verify exact values without paper access. The claim that o1-mini is the "best model" for constraint compliance is notable; o1-mini is a reasoning model, which is consistent with higher constraint adherence. PLAUSIBLE but UNVERIFIABLE at exact-value level. | MAJOR | Evidence Quality |
| CV-007-20260221T-C4T | **Claim:** "The original ceiling of <= 25 was silently exceeded when H-25..H-30 were added without updating the cap" (line 52). **Source:** Commit history, quality-enforcement.md. **Independent verification:** quality-enforcement.md currently states "<= 35" as the Max Count for HARD rules. The derivation references E-010 "Commit 936d61c: Retroactive ceiling update from 25 -> 35 with no justification." Commit 936d61c exists in the recent git log with message "feat(enforcement): add H-31 ambiguity clarification rule (EN-006)." This commit added H-31, not the ceiling change. The claim that 936d61c changed the ceiling may be inaccurate -- the ceiling change may have occurred in a different commit bundled with H-31, or H-31 was the trigger for the ceiling update. The evidence reference is imprecise. | MAJOR | Traceability |

**Blocking:** **Yes.** CV-001 and CV-002 are CRITICAL: the L2-REINJECT ecosystem is more complex than the derivation acknowledges. If the engine were updated to read all 16 markers from 9 files (a reasonable architectural improvement), the "14 rules with full L2 protection" analysis changes fundamentally. The derivation assumes the current engine limitation is a fixed architectural constraint rather than an implementation gap.

---

## S-012: FMEA

**Strategy:** S-012 FMEA (MIL-P-1629, AIAG/VDA 2019)
**Execution Date:** 2026-02-21

### Element Decomposition

| Element ID | Element | Description |
|-----------|---------|-------------|
| E-01 | Constraint 1: Token Budget | L1 token capacity analysis |
| E-02 | Constraint 2: L2 Coverage | L2 re-injection capacity analysis |
| E-03 | Constraint 3: Research Evidence | Instruction-following studies |
| E-04 | Constraint 4: Signal Quality | Diminishing returns analysis |
| E-05 | Constraint 5: Rule Conflicts | Combinatorial analysis |
| E-06 | Synthesis | Binding constraint determination |
| E-07 | Two-Tier Model | Tier A/Tier B recommendation |
| E-08 | Implementation Path | Consolidation and transition steps |

### Findings

| ID | Element | Failure Mode | S | O | D | RPN | Classification | Affected Dimension |
|----|---------|-------------|---|---|---|-----|---------------|-------------------|
| FM-001-20260221T-C4T | E-02 | L2 marker count conflated with H-rule count; 8 markers vs "10 rules" creates confusion about actual coverage capacity | 8 | 8 | 4 | 256 | CRITICAL | Evidence Quality |
| FM-002-20260221T-C4T | E-06 | Binding constraint (14) contradicts recommendation (25); synthesis chooses a number that exceeds its own binding analysis | 9 | 7 | 3 | 189 | MAJOR | Internal Consistency |
| FM-003-20260221T-C4T | E-03 | Research evidence applied without accounting for Jerry-specific mitigations (L2 re-injection, domain partitioning); overstates degradation for this specific system | 7 | 6 | 4 | 168 | MAJOR | Evidence Quality |
| FM-004-20260221T-C4T | E-07 | Two-tier model has no governance mechanism for tier assignment disputes or tier promotion/demotion processes | 7 | 7 | 3 | 147 | MAJOR | Actionability |
| FM-005-20260221T-C4T | E-08 | Compound rules (consolidation) may not be enforceable by L3 AST checks that depend on specific patterns | 8 | 5 | 4 | 160 | MAJOR | Methodological Rigor |
| FM-006-20260221T-C4T | E-01 | "Mean per-rule L1 cost" includes non-HARD content, inflating the estimate; true per-rule cost may be 200-300 tokens, changing the ceiling | 5 | 7 | 5 | 175 | MINOR (changes range, not conclusion) | Evidence Quality |
| FM-007-20260221T-C4T | E-04 | "20-25 sweet spot" from nse-risk-001 is circular if that assessment used this same data | 6 | 4 | 6 | 144 | MINOR | Methodological Rigor |
| FM-008-20260221T-C4T | E-05 | Conflict probability analysis is purely theoretical; no empirical conflict data exists | 5 | 6 | 3 | 90 | MINOR | Evidence Quality |

**Total RPN:** 1,329
**Highest RPN:** FM-001 (256) -- L2 marker count confusion
**Elements with highest total risk:** E-02 (L2 Coverage analysis) and E-06 (Synthesis)

**Blocking:** **Yes.** FM-001 (RPN 256) exceeds the Critical threshold (>= 200). The L2 coverage analysis is the foundation of the binding constraint, and its factual basis is imprecise.

---

## S-013: Inversion

**Strategy:** S-013 Inversion Technique (Jacobi, Munger, Bevelin 2007)
**Execution Date:** 2026-02-21

### Goals Identified

1. **G1:** Derive a principled upper boundary for HARD rules
2. **G2:** Provide a defensible alternative to the current unprincipled ceiling of 35
3. **G3:** Enable PROJ-007 to add new HARD rules within a sustainable budget

### Anti-Goals (Inverted)

"To guarantee this derivation fails, we would need to:
- Use a methodology that appears rigorous but reaches a predetermined conclusion
- Ignore evidence that contradicts the desired number
- Make the ceiling so restrictive that it cannot accommodate real governance needs
- Make the analysis unfalsifiable by using ranges wide enough to contain any answer"

### Findings

| ID | Finding | Classification | Affected Dimension |
|----|---------|---------------|-------------------|
| IN-001-20260221T-C4T | **Assumption: "The 5 constraints are independent."** Inversion: "What if they are NOT independent?" Constraints 1, 3, and 4 all converge on 20-25 because they measure related aspects of the same system (token budget limits attention capacity limits signal quality). If the underlying variable is "cognitive budget" and all three constraints are proxies for it, counting them as 3 independent data points overstates the evidence. The convergence is explained by shared causality, not independent corroboration. | CRITICAL | Methodological Rigor |
| IN-002-20260221T-C4T | **Assumption: "The current L2 architecture is fixed."** Inversion: "What if L2 coverage can be expanded?" The derivation treats the L2 600-token budget and quality-enforcement.md-only engine scope as fixed constraints. But these are implementation decisions, not architectural limits. If the engine is updated to read all 16 L2-REINJECT markers from 9 files (an afternoon's work), the "L2 coverage ceiling" jumps from 14 to potentially 20+. The derivation should distinguish between "current implementation constraints" and "architectural constraints." | MAJOR | Evidence Quality |
| IN-003-20260221T-C4T | **Assumption: "Reducing from 31 to 25 improves enforcement quality."** Inversion: "What if removal degrades quality?" If the 6 rules targeted for consolidation (H-25..H-30, H-07..H-09) are currently being enforced successfully (even without L2), removing them and replacing with compound rules could reduce enforcement. The derivation assumes consolidation is neutral or positive; the inversion reveals it could be negative. No measurement of current compliance for these rules is presented. | MAJOR | Evidence Quality |
| IN-004-20260221T-C4T | **Assumption: "25 is the right number from the convergence range of 20-25."** Inversion: "Why not 20?" The derivation selects the UPPER bound of the convergence range (25) without justifying why 25 is preferred over 20, 22, or 23. The token budget analysis supports 18-25. The L2 analysis supports 14. The research supports 10-12 simultaneously active. The "sweet spot" is 20-25. Selecting 25 (the maximum of the most generous range) appears to be motivated by the practical need to accommodate 31 - 6 = 25 current rules after consolidation, rather than being the optimal point in the convergence range. | MAJOR | Methodological Rigor |
| IN-005-20260221T-C4T | **Assumption: "The HARD rule count is the right metric to optimize."** Inversion: "What if the HARD rule count is irrelevant?" The research evidence suggests that SIMULTANEOUSLY ACTIVE constraints (not total defined constraints) determine compliance. If rules are domain-partitioned (coding rules activate during coding, governance rules during governance), the total count matters less than the maximum co-activation count. The derivation could arrive at a different architecture: instead of capping total rules at 25, cap the maximum co-activation profile at 10-12 rules per task type, with no limit on total defined rules. | MINOR | Completeness |
| IN-006-20260221T-C4T | **The derivation may be an exercise in motivated reasoning.** The original ceiling was 25. It was exceeded. This derivation concludes... 25. The convergence is suspicious: if the analysis truly started from first principles, arriving at exactly the original designer's number (which was itself a judgment call, not a derivation) suggests either the methodology was calibrated to reach this answer, or there is a genuine attractor at 25. The derivation should explicitly address this coincidence. | OBSERVATION | Methodological Rigor |

**Blocking:** **Yes.** IN-001 is CRITICAL: if the 5 constraints are not independent (and at least 3 appear to be proxies for the same underlying variable), the "convergence of 5 independent analyses" claim is the core methodological contribution of the derivation, and it may be overstated.

---

## Cross-Strategy Synthesis

### Recurring Themes (findings that appeared in 3+ strategies)

| Theme | Strategies | Severity |
|-------|-----------|----------|
| **Gap between binding constraint (14) and recommendation (25)** | S-002 (DA-001), S-012 (FM-002), S-013 (IN-004) | CRITICAL in S-002, MAJOR in S-012/S-013 |
| **L2 marker count imprecision (8 markers vs 10 H-rules vs 16 total markers)** | S-011 (CV-001, CV-002), S-012 (FM-001), S-010 (SR-002) | CRITICAL in S-011/S-012 |
| **Constraint independence questionable** | S-010 (SR-001), S-013 (IN-001), S-001 (RT-004) | CRITICAL in S-013, MAJOR in S-010/S-001 |
| **Consolidation feasibility unproven** | S-004 (PM-001), S-001 (RT-003), S-010 (SR-004) | CRITICAL in S-004, MAJOR in S-001 |
| **Research applicability to Jerry-specific architecture** | S-002 (DA-002), S-004 (PM-004), S-012 (FM-003) | MAJOR across all |
| **No exception/override mechanism for the ceiling** | S-001 (RT-001), S-004 (PM-002), S-002 (DA-007) | CRITICAL in S-001 |
| **Missing sensitivity analysis** | S-010 (SR-006), S-013 (IN-004), S-002 (DA-003) | MAJOR pattern |

### Unique Insights per Strategy

| Strategy | Unique Finding Not Captured by Others |
|----------|--------------------------------------|
| S-010 | SR-005: The 0.95 quality threshold in the header is inconsistent with the SSOT 0.92 |
| S-003 | SM-001: Need for explicit rule activation profiles by task type |
| S-002 | DA-005: No empirical measurement of context rot impact on L1 rules |
| S-004 | PM-003: Tier A/B governance dispute resolution gap |
| S-001 | RT-005: No deterministic enforcement of the ceiling itself |
| S-007 | CC-003: P-020 (User Authority) implications of reducing the ceiling |
| S-011 | CV-002: 16 total L2-REINJECT markers across 9 files (vs 8 in quality-enforcement.md only) |
| S-012 | FM-006: True per-HARD-rule L1 cost may be 200-300 tokens (not 410) |
| S-013 | IN-006: The coincidence of re-deriving exactly 25 (the original number) |

---

## Tournament Verdict

### CRITICAL Findings Summary (7 total)

| # | Finding | Strategy | Resolution Required |
|---|---------|----------|---------------------|
| 1 | Gap between binding constraint (14) and recommendation (25) not justified | S-002 DA-001 | Explicitly justify why the binding constraint does not actually bind, or lower the recommendation |
| 2 | Compound rules may be unenforceable at L3 level | S-004 PM-001 | Demonstrate consolidation feasibility with draft compound rules tested against L3 checks |
| 3 | Ceiling can be weaponized to block governance with no override | S-001 RT-001 | Add exception/escalation mechanism for governance ceiling |
| 4 | L2 marker count (8) conflated with H-rule coverage count (10) | S-011 CV-001 | Clarify and correct the L2 coverage analysis |
| 5 | L2 markers exist in 8 other files; engine limitation is implementation, not architecture | S-011 CV-002 | Distinguish implementation constraints from architectural constraints |
| 6 | L2 marker count imprecision undermines binding constraint foundation (RPN 256) | S-012 FM-001 | Correct the factual basis of the L2 analysis |
| 7 | Constraint independence questionable -- at least 3 of 5 may be proxies for "cognitive budget" | S-013 IN-001 | Explicitly acknowledge dependency structure; restate as "2-3 independent constraint families" |

### Overall Assessment

**Verdict: REVISE**

The derivation is a substantive and well-structured analytical contribution. Its multi-constraint methodology, evidence index, and two-tier model represent genuine intellectual work. The conclusion (25 HARD rules) is in the correct ballpark and directionally sound -- the current 35-rule ceiling is indeed too high based on the evidence presented.

However, 7 CRITICAL findings across 6 strategies prevent PASS:

1. **The factual foundation (L2 marker counts) is imprecise** and must be corrected before the derivation can serve as a governance basis.
2. **The logical gap between "14 is the binding constraint" and "we recommend 25"** must be explicitly resolved -- either by justifying the two-tier model more rigorously or by acknowledging that 25 includes 11 rules with degraded enforcement reliability.
3. **The constraint independence claim must be qualified** -- the "convergence of 5 independent analyses" is the derivation's strongest claim, and it may be overstated if 3 of 5 are proxies for the same variable.
4. **The governance implications (ceiling weaponization, consolidation feasibility, missing override mechanism)** must be addressed before this can be a constitutional change.

**Recommended Revision Actions (Priority Order):**

1. **P0:** Correct L2 coverage analysis with accurate marker/rule/file counts (resolves CV-001, CV-002, FM-001)
2. **P0:** Explicitly resolve the 14-vs-25 tension by either lowering the recommendation or providing rigorous justification for why the L2 binding constraint does not bind at 25 (resolves DA-001, FM-002)
3. **P0:** Add exception/override mechanism for the ceiling (resolves RT-001)
4. **P1:** Qualify constraint independence -- reframe as "2-3 constraint families with internal corroboration" rather than "5 independent constraints" (resolves IN-001, SR-001)
5. **P1:** Add sensitivity analysis showing how the recommendation changes with parameter variations (resolves SR-006, IN-004)
6. **P1:** Demonstrate consolidation feasibility with draft compound rules (resolves PM-001, RT-003)
7. **P1:** Add rule activation profile analysis by task type (resolves SM-001, DA-002, PM-004)
8. **P2:** Address the coincidence of re-deriving 25 = original designer's number (resolves IN-006)
9. **P2:** Add P-020 (User Authority) reference to constitutional compliance narrative (resolves CC-003)
10. **P2:** Fix header quality threshold from 0.95 to match SSOT 0.92 or justify deviation (resolves SR-005)

---

*Tournament execution completed: 2026-02-21*
*Executor: adv-executor (C4 tournament mode)*
*Strategies executed: 9 of 9 non-scoring*
*S-014 scoring: To be executed separately by adv-scorer*
