# PR #269 Terminal Verdict — /nuclear-sop Skill

> **Project:** PROJ-032 / EPIC-001 / FEAT-002 / STORY-005 (Phase 5 of 5)
> **Subject:** PR #269, branch `proj-0039-nuclear-engineer`; reviewed head `bda64202`, current head `c07033ce` (post-maintainer-remediation)
> **Audience:** Repository owner (decision) and contributor (rework contract)
> **Date:** 2026-08-07 | **Criticality:** C4
> This verdict is derived from the four preceding PROJ-032 phases; every claim below cites a persisted artifact or an observable (score, count, commit SHA, CI run).

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Recommendation](#l0-recommendation) | The verdict in one sentence, with a five-sentence rationale |
| [L1: Evidence Chain](#l1-evidence-chain) | What each phase found, with links and observables |
| [The 0.943 vs 0.52 Divergence](#the-0943-vs-052-divergence) | What the score gap does and does not imply (P-022) |
| [Maintainer Remediation: Done and Deliberately Not Done](#maintainer-remediation-done-and-deliberately-not-done) | Commit c07033ce scope and the current approved envelope |
| [The Rework Contract: Seven Open Blockers](#the-rework-contract-seven-open-blockers) | BUG-001..007 / issues #350–#356 with the redesign question each must answer |
| [Conditions for Merge After Rework](#conditions-for-merge-after-rework) | What evidence flips this recommendation, including the H-36 ruling and independent re-review |
| [What Would Flip the Recommendation to REJECT](#what-would-flip-the-recommendation-to-reject) | The honest failure conditions for the rework path |
| [Residual Risk If Merged Today](#residual-risk-if-merged-today) | What the owner accepts by merging at c07033ce |
| [PR Comment Draft](#pr-comment-draft) | Ready-to-post comment for PR #269 |
| [Self-Review Note](#self-review-note) | H-15 compliance record |

---

## L0: Recommendation

**REWORK — keep PR #269 open; do not merge at current head `c07033ce`, and do not close it: the contribution is salvageable and partially remediated, but seven named design defects that only the contributor can resolve (issues #350–#356) block merge.**

Three independent review passes converged on the same conclusion: the skill's ideas are genuinely valuable, but its core safety mechanisms cannot execute as written — the user-approval gate depends on a tool no agent is granted, the quality-gate step instructs an agent to do something the same file says it cannot do, and the "independent verifier" takes its acceptance criteria from the very artifact it is supposed to police. Independent C4 tournament scoring produced 0.52 against the 0.92 quality bar, versus an author-claimed 0.943 that no artifact in the PR supports. The maintainer has already fixed everything a maintainer legitimately can — all mechanical defects, at commit `c07033ce` with CI fully green — and conservatively withdrew the skill's C3+ approval, restricting it to C1–C2. What remains open are seven redesign decisions that only the contributor (plus one owner ruling) can make; 57% of the Critical finding mass falls in this category. REJECT is not warranted because every phase judged the design salvageable ("one focused revision cycle away"), and MERGE is not defensible because the first real invocation of the skill would stall or improvise at its own safety gates.

---

## L1: Evidence Chain

### Phase 1 — Standards compliance audit (six blind auditors)

**Artifact:** [phase-1-standards-report.md](../../FEAT-001-independent-review/STORY-001-standards-compliance/phase-1-standards-report.md)

**Observable facts:**
- **32 consolidated findings: 6 Critical / 15 Major / 11 Minor**, from six independent, context-isolated auditors reading subject files only at PR head `bda64202` and standards only from the current baseline worktree.
- **5 confirmed HARD-rule violations across 4 distinct HARD rules:** H-01/P-003 (P1-001: QG-HOLD instructs a T2 worker to invoke ps-critic — second-level delegation), H-02/P-020 (P1-002: USER-HOLD requires `AskUserQuestion`, absent from the tool grant and from every T1–T5 tier; zero of 89 fleet agents use it), H-34 ×2 (P1-004: `sop-brief.governance.yaml` fails the governance schema with 4 verbatim validator errors; P1-005: `sop-verifier.governance.yaml` fails with 2), H-23 (P1-006: three runtime-consumed long files with no navigation tables).
- **Deterministic, reproducible failures:** `composition/sop-verifier.agent.yaml` is not parseable YAML (`ScannerError` at line 9, P1-003); schema copies verified byte-identical on both branches, so the failures hold against either.
- Phase 1's verdict: "not mergeable as shipped," while also finding the HARD-rule fundamentals "mostly sound" and "none of the defects appears beyond straightforward repair."

### Phase 2 — Engineering review (eng-reviewer, blind to other phases)

**Artifact:** [phase-2-eng-review.md](../../FEAT-001-independent-review/STORY-002-engineering-review/phase-2-eng-review.md)

**Observable facts:**
- **30 findings: 4 Critical / 16 Major / 10 Minor** across three lenses (methodology, prompt engineering, security), with a STRIDE threat model over the skill's five attacker-influenceable runtime inputs.
- **Verdict: NO-GO for merge as shipped.** The four Criticals: P2-001 (mid-procedure delegation unimplementable — the flagship example cannot execute under the skill's own topology), P2-002 (NS-H-01 STAR rule is non-terminating as written; the skill's own baseline silently exempts what the rule's plain text covers), P2-015 (USER-HOLD grantless and semantically unavailable; the runtime execution model — subagent vs. main-context persona — is never pinned, and each candidate breaks a different guarantee), P2-022 (verifier authority inversion: acceptance criteria and expected paths originate inside the untrusted workflow definition — "crafted definitions self-certify").
- Phase 2's disposition line, quoted: "The skill is one focused revision cycle away from being a strong addition; it is not there at head `bda64202`."

### Phase 3 — C4 adversarial tournament (9 strategies + S-014 final score)

**Artifacts:** [s-014-tournament-score.md](../../FEAT-001-independent-review/STORY-003-c4-tournament/s-014-tournament-score.md); strategy detail in [strategies/](../../FEAT-001-independent-review/STORY-003-c4-tournament/strategies/) (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013)

**Observable facts:**
- The nine strategy executions produced **89 findings, 33 Critical** (per the Phase 3 tournament record); the S-014 scorer independently verified the majority of Critical claims by direct file reads before consulting them.
- **S-014 composite: 0.52 — REJECTED** (threshold 0.92 per H-13; REJECTED band is < 0.85). Weakest dimension: Internal Consistency at 0.35. Dimension arithmetic shown in full in the report (0.124 + 0.070 + 0.092 + 0.084 + 0.093 + 0.060 = 0.523).
- **9 deduplicated Critical clusters (CC-1..CC-9), each directly verified by the scorer**, each independently sufficient to block PASS. Convergence was high: CC-1 (registration self-contradiction) and CC-7 (OE extension conflict) were each flagged by 7 of 9 strategies; CC-6 (lapsed H-36 deadline) by 6 of 9.
- **Claimed prior composite 0.943 vs. independent 0.52: delta −0.423.** Exhaustive grep for the literal `0.943` across the full PR checkout returned **zero matches** (see next section).

### Phase 4 — Triage and maintainer remediation

**Artifacts:** [remediation-register.md](../STORY-004-remediation/remediation-register.md); [remediation-log.md](../STORY-004-remediation/remediation-log.md)

**Observable facts:**
- **114 normalized Critical/Major findings (44 Critical, 70 Major) → 59 unique defects → 14 remediation clusters**, with every one of the 114 source IDs mapped to exactly one cluster (register Traceability Appendix, consumption check sums to 114).
- **Disposition: 7 clusters FIX-NOW (REM-08..14), 7 clusters DEFER-REWORK (REM-01..07).** 25 of 44 Critical findings — **57% of the Critical mass** — sit in DEFER-REWORK: not maintainer-fixable without exercising design authority a maintainer does not have over a contribution.
- **Maintainer fix commit `c07033ce`** on `proj-0039-nuclear-engineer` implements all seven FIX-NOW clusters. **PR #269 CI at that head: 15/15 green** ([run 31174766440](https://github.com/geekatron/jerry/actions/runs/31174766440)). Independent fresh-context verification of the fix: 10/10 checks PASS (governance/canonical schema gate now 8/8 valid, diff scope audit, DEFER-REWORK-files-untouched audit).
- **C3+ approval WITHDRAWN** as part of REM-08 (the conservative direction required by REM-04's evidence invalidation): approved use is now **C1–C2 only**, stated consistently across SKILL.md, PLAYBOOK.md, rules, and reference docs.
- The seven open clusters are tracked as worktracker items [BUG-001](../../../BUG-001-qg-hold-delegation-topology/)..[BUG-007](../../../BUG-007-executor-command-gating/) with GitHub issues [#350](https://github.com/geekatron/jerry/issues/350)–[#356](https://github.com/geekatron/jerry/issues/356) (H-32 parity).

### Subject state

- Reviewed head: `bda64202`. Current head: `c07033ce` (maintainer remediation applied). All Phase 1–3 findings were made against `bda64202`; the FIX-NOW subset is resolved at `c07033ce`; the DEFER-REWORK subset is unchanged by design.

---

## The 0.943 vs 0.52 Divergence

**The facts.** The PR presents a C4 tournament composite of 0.943 (PASS). The PROJ-032 independent S-014 score of the same deliverable at head `bda64202` is 0.52 (REJECTED) — a delta of −0.423. The scorer performed an exhaustive search for the literal value `0.943` across the entire PR checkout, including the contributor's build-pipeline tree under «PR projects tree»/PROJ-0039-nuclear-engineer: **zero matches**. The nearest real figures are 0.934 (`qg-e6-score.md` — which scores the QG-E6 compliance *report's* document quality, and whose underlying verdict was **CONDITIONAL PASS with two OPEN C3+-blocking items**, SEC-008 and SEC-011), 0.933 (ADR-001), and 0.922 (requirements synthesis). None is 0.943; none is a tournament score of the shipped skill.

**What this does and does not imply — stated fairly.** Untraceable is not the same as fabricated. The most charitable and genuinely plausible explanation is the **pre-registration-snapshot hypothesis** (the S-014 report's own factor 4): if 0.943 was computed against an earlier artifact state — before the registration entries were spliced into CLAUDE.md, AGENTS.md, the trigger map, and plugin.json — then the largest single Critical cluster (CC-1, the registration self-contradiction) did not yet exist at scoring time, and the claimed score and the independent score legitimately describe two different points in the artifact's history. The remaining gap is well explained by documented self-scoring leniency: every gate in the contributor's pipeline was scored by same-framework agents with no independent reviewer, and every gate cleared or nearly cleared 0.92 — including QG-E6, whose own prose simultaneously recorded two OPEN blocking conditions.

**What is not contestable.** Two things stand regardless of snapshot history: (1) the score was never persisted — a quality claim that gates C3/C4 approval existed only as an assertion, with no dimension breakdown, no scorer identity, no scored-commit reference; and (2) the shipped SKILL.md asserted *"approved for all criticality levels (C1 through C4)"* while the author's own compliance gate said CONDITIONAL PASS with named open items — that specific shipped claim was false as shipped, whatever its provenance (this is the P-022 exposure, and it attaches to the claim, not necessarily to intent).

**The lesson for this repository.** Author-supplied quality-gate results are not load-bearing evidence for merge decisions. The divergence here is the empirical demonstration: a fully self-scored pipeline reported ≥0.92 at every phase for an artifact that independent review scored 0.52. Merge-gating scores for C3+/C4 contributions must be (a) persisted as in-PR artifacts with dimension breakdowns and the scored commit SHA, and (b) independently reproduced by a reviewer outside the authoring pipeline. That requirement is encoded in the merge conditions below.

---

## Maintainer Remediation: Done and Deliberately Not Done

### What commit `c07033ce` did (FIX-NOW, REM-08..14)

Per the [remediation-log](../STORY-004-remediation/remediation-log.md), all seven mechanically-fixable clusters, each traced to a worktracker item and GitHub issue (#357–#363):

| Fixed | Substance |
|-------|-----------|
| REM-08 Registration/status truth | False "NOT registered / NOT live-routable" note removed; stale priority-12 trigger-row copy deleted; **C3+ approval withdrawn conservatively** (see below) |
| REM-09 Enforcement surfaces | /nuclear-sop added to the H-22 rule sentence and L2-REINJECT comment; "nuclear workflow" compound trigger added (fixes the deterministic misroute); AGENTS.md total corrected 89→93 |
| REM-10 Schema/standards conformance | All H-34 governance and canonical schema failures cleared (8/8 files valid); AD-M-011 output declarations; hexagonal rewording; reasoning_effort |
| REM-11 OE artifact contract | `.yaml` standardized everywhere; workflow_id-primary retrieval; missing sop-capture Section 11 step added |
| REM-12 State machine/completion | Transitions aligned to the rules SSOT; `execution_log_final` path contract fixed; **SEC-008 verifier fail-closed fix applied** (the fix the contributor's own QG-E6 gate had drafted but never shipped) |
| REM-13 Composition drift | `agents/*.md` + governance declared normative, composition relabeled derived; SEC-001 injection response restored to strongest form in all copies; forbidden-action parity |
| REM-14 Navigation tables | H-23 tables added to the three runtime-consumed files; NAV-004 rows completed |

Verification: independent fresh-context verifier 10/10 PASS; local pre-commit suite green; **PR CI 15/15 green** at `c07033ce`.

### What it deliberately did not do (DEFER-REWORK, REM-01..07)

The maintainer did **not** touch the seven clusters that constitute the skill's safety architecture, because each requires a design decision that is the contributor's to make: a maintainer choosing the delegation topology, pinning the runtime model, inventing a trust anchor, manufacturing validation evidence, issuing a governance ruling unilaterally, redesigning the OE lifecycle, or replacing the command-gating model would be redesigning the contribution under the contributor's name. This restraint is itself part of the verdict's honesty: the PR at `c07033ce` is *cleaner*, not *fixed*.

### Current approved envelope

**C1–C2 only.** The skill's C3+ approval is withdrawn pending re-validation, because its sole empirical basis (the QG-E4 "3/3, 100%, empirically validated" claim) was invalidated: the test fixture embeds its own answer key in the file the executor reads, N=3, self-authored and self-scored, with the evidence artifact outside the shipped package (REM-04). The withdrawal is stated consistently across SKILL.md, PLAYBOOK.md, rules, and reference docs at `c07033ce`. Note that even the C1–C2 envelope is impaired by BUG-001/BUG-002 (below), which break execution at *all* criticality levels — the envelope statement governs what the skill claims, not what it can currently deliver.

---

## The Rework Contract: Seven Open Blockers

Each blocker is a DEFER-REWORK cluster from the [remediation register](../STORY-004-remediation/remediation-register.md), tracked as a worktracker BUG and a GitHub issue. For each, the one-line redesign question the contributor must answer (full detail and candidate architectures in the register's cluster sections):

| Blocker | Issue | Cluster | The question the contributor must answer |
|---------|-------|---------|------------------------------------------|
| [BUG-001](../../../BUG-001-qg-hold-delegation-topology/) | [#350](https://github.com/geekatron/jerry/issues/350) | REM-01 | Under P-003 (one delegation level) and H-36 (3-hop ceiling), **who invokes quality gates and external agents mid-procedure, and how does sop-executor suspend and resume place-keeping around them?** |
| [BUG-002](../../../BUG-002-user-hold-runtime-model/) | [#351](https://github.com/geekatron/jerry/issues/351) | REM-02 | **What is the pinned runtime execution model** (worker subagent vs. main-context persona), and how do USER-HOLD and sop-brief's six interactive gates actually reach the user under it — plus a terminating scope for NS-H-01? |
| [BUG-003](../../../BUG-003-trust-boundary-state-tamper/) | [#352](https://github.com/geekatron/jerry/issues/352) | REM-03 | **Where do the verifier's acceptance criteria, expected paths, and the effective criticality level come from, if not from the untrusted artifact they police** — and is PROCEDURE_STATE tamper evidence implemented for real or withdrawn everywhere it is claimed? |
| [BUG-004](../../../BUG-004-qg-e4-validation-evidence/) | [#353](https://github.com/geekatron/jerry/issues/353) | REM-04 | **What blind, independently executed, statistically meaningful validation** (answer keys stripped, live transcripts, independent authorship/scoring, N > 3) **replaces the invalidated QG-E4 walkthrough** before any C3+ approval claim returns? |
| [BUG-005](../../../BUG-005-h36-governance-ruling/) | [#354](https://github.com/geekatron/jerry/issues/354) | REM-05 | **What is the actual H-36 ruling** — C3+ keeps 4-hop mode with sop-verifier, or reverts to 3-hop without it — encoded with exactly one fallback semantics, one anchor date, and a fail-closed default? *(Requires owner input; see merge conditions.)* |
| [BUG-006](../../../BUG-006-oe-feedback-loop-design/) | [#355](https://github.com/geekatron/jerry/issues/355) | REM-06 | **What OE lifecycle allows synthesis entries to actually exist** (writable schema, one owner), thresholds that cannot deadlock unrelated executions repo-wide, and a provenance/trust model for a cross-criticality shared corpus? |
| [BUG-007](../../../BUG-007-executor-command-gating/) | [#356](https://github.com/geekatron/jerry/issues/356) | REM-07 | **What principled command-gating model** (allowlist, category-based holds, or delegation to the deterministic SecurityEnforcementEngine) **replaces the enumerable-badness substring denylist**, and what is the injection-screening scope across all definition-sourced fields that drive tool calls? |

Explicit descoping is an acceptable answer where the register says so — e.g., dropping mid-procedure composition and rewriting the example (REM-01 option c), or deleting `composition/` (REM-13 note) — provided the shipped text then matches the reduced scope.

---

## Conditions for Merge After Rework

The recommendation flips to MERGE when **all** of the following evidence exists:

1. **All seven blockers closed** (issues #350–#356), each with a shipped design answering its register question — or an explicit, text-consistent descope of the feature the blocker governs.
2. **The H-36 ruling is issued by the owner** — this is the one blocker that is not purely contributor work. The owner must rule whether the skill's predetermined internal agent sequence counts as routing hops under H-36. Phase 2 identified the relevant precedent: /eng-team runs a predetermined 8-step sequence over 10 worker agents with no hop-ceiling machinery, suggesting predetermined intra-skill sequences are not routing re-evaluations; adopting that reading resolves BUG-005 and removes the need for the skill's self-scheduled sunset clause entirely. Whatever the ruling, it must be encoded once (one fallback, one anchor date, fail-closed default) and tracked as a worktracker entity with H-32 GitHub-issue parity.
3. **For any C3+ re-enablement:** the BUG-004 re-validation evidence, shipped inside or resolvably cited from the package. Until then, the C1–C2 restriction stands in every shipped document (as it now does at `c07033ce`).
4. **Independent re-review of the post-rework head:** a fresh C4 tournament pass by context-isolated reviewers outside the authoring pipeline (FC-M-001), scoring **≥ 0.92 composite (H-13) with zero open Critical findings**, and — the lesson of the 0.943 episode — **the score persisted as an in-PR artifact** with dimension breakdown and the scored commit SHA. A partial re-score of changed files does not satisfy this; the S-014 report explicitly requires a full fresh pass after the consistency and rigor defects are addressed.
5. **CI green at the re-reviewed head** (currently satisfied at `c07033ce`; must remain true).

**A narrower early-merge variant** the owner may consider: a C1–C2-scoped merge before BUG-004 re-validation completes, but only if BUG-001, BUG-002, BUG-003, BUG-006, and BUG-007 are resolved (these break execution or security posture at *all* criticality levels), the C3+ withdrawal stays in force, BUG-005's contradictory normative text is reconciled, and condition 4's independent re-review still passes. BUG-004 then remains open solely as the C3+ re-enablement gate.

---

## What Would Flip the Recommendation to REJECT

Honesty requires stating the exit conditions for the rework path as well:

- **Abandonment:** the contributor declines the rework contract or the issues go stale past a reasonable window set by the owner — at that point close the PR, preserving the maintainer's FIX-NOW work and the register as the design record for any successor attempt.
- **Architectural infeasibility:** a good-faith redesign attempt demonstrates that no P-003-compliant delegation topology can preserve the skill's core value (e.g., suspend/resume overhead makes procedures unusable) — this would mean the approach, not the execution, is the defect.
- **Trust failure:** evidence emerges that the 0.943 claim was knowingly false rather than a snapshot/leniency artifact — that converts a quality problem into a trust problem, and the calculus changes accordingly. No current evidence supports this reading.

---

## Residual Risk If Merged Today

If the owner merged at `c07033ce` despite this recommendation, they would accept:

1. **A live-routable skill that cannot execute cleanly at any criticality.** The skill is registered, trigger-mapped, and (post-REM-09) L2-enforced — and its first real invocation hits BUG-002: sop-brief's six interactive gates and sop-executor's USER-HOLD depend on a tool no agent is granted, so the run stalls or the model improvises precisely at the moments the skill promises determinism; NS-H-01 remains non-terminating as written; QG-HOLD remains unexecutable (BUG-001). The failure mode is not a crash — it is undefined behavior inside a safety-branded workflow.
2. **A security posture whose differentiating control is void against its own primary threat.** The verifier accepts criteria authored by the artifact it polices; declared criticality de-rates every downstream protection with no auto-escalation cross-check; a poisoned state file steers RESUME past holds with post-hoc-only detection; the documented state_hash control does not exist in any code path (BUG-003); command gating is an enumerable-badness denylist (BUG-007).
3. **A repo-global, agent-written, cross-criticality memory (`docs/experience/`) landing without a framework policy** — the first of its kind in this repository, an attractive plant-at-C1/harvest-at-C4 persistence channel (BUG-006), plus the precedent of skill-local HARD rules and self-scheduled governance deadlines.
4. **Bounded upside of current mitigations:** the C1–C2 restriction, honest status text, schema-clean surfaces, and green CI at `c07033ce` genuinely reduce exposure — the risk is not that the framework breaks on merge, but that the first user who invokes the skill gets a stalled or improvising procedure, and that the OE/global-memory precedent enters the codebase unreviewed.

---

## PR Comment (as posted)

> Posted on PR #269 as [comment 5216673422](https://github.com/geekatron/jerry/pull/269#issuecomment-5216673422). Revised 2026-08-07 into self-contained plain language after owner feedback — internal codenames (strategy IDs, principle IDs, hold-point names) are spelled out or dropped, because the PR audience has no Jerry-governance context. Issues #350–#356 were likewise rewritten and retitled to be self-contained, each carrying its full design question inline.

Content summary of the posted comment: what the skill is in plain words; recommendation (rework, not merge, not close) with the runtime-safety rationale; a Mermaid diagram of the merge path (fix-state → 7 design decisions → independent re-review ≥ 0.92 → merge); the three-pass review method and the 0.52-vs-0.943 score gap stated without jargon and without alleging bad faith; the maintainer fixes at `c07033ce` including the low-risk-only restriction; the seven design decisions with one-line plain descriptions each; and the merge conditions. Full text: the posted comment itself (single source of truth).

---

## Self-Review Note

H-15 self-review performed before finalizing: (1) every score, count, SHA, CI run, and issue number above was re-checked against the four source artifacts (Phase 1 report, Phase 2 report, S-014 tournament score, remediation register + log) — no figure appears here that does not appear in a cited source; (2) the recommendation was derived after the evidence read, not before — the REJECT and MERGE cases were argued against the record (Phase 2's "salvageable" disposition and the 57% non-maintainer-fixable Critical mass respectively decide them); (3) the 0.943 divergence section was checked for fairness — the pre-registration-snapshot hypothesis is presented as the leading charitable explanation, the fabrication reading is explicitly not adopted, and the only P-022 assertion made is against the shipped C1–C4 approval claim, which is documented as false-as-shipped independent of intent; (4) all relative links were verified against the on-disk tree (FEAT-001 phase reports, strategies directory, STORY-004 artifacts, BUG-001..007 worktracker directories); (5) contradiction check: the "C1–C2 envelope" statement is qualified where BUG-001/002 impair even that envelope, so the document does not overstate the remediated state it elsewhere criticizes the PR for overstating.

---

*PROJ-032 STORY-005 terminal verdict | 2026-08-07 | Derived from PR #269 heads `bda64202` (reviewed) and `c07033ce` (remediated) | P-002 persisted | No subagents spawned (P-003); nothing posted externally by this agent*
