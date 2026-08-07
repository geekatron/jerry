# Devil's Advocate Report: GitHub issue #356 (BUG-007 — executor command gating)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-356.md` (text of GH issue #356)
**Criticality:** C4 (tournament member)
**Date:** 2026-08-07
**Reviewer:** adv-executor (background)

## Summary

3 counter-arguments (1 Critical, 1 Major, 2 Minor). The core claim (substring denylist misses `nc`, `python -m http.server`, base64 exfil; duplicates the repo's deterministic engine, weaker) checks out against the ground-truth register. The blocking Critical finding is a scope mismatch: the opening paragraph describes the injection-screening gap as spanning *across document types* (workflow definitions, state files, OE/"lessons-learned" entries, hold-point logs), but the actual defect (register REM-07/G2) is entirely about *unscreened fields within the single workflow-definition document* — and the issue's own closing design question correctly uses the narrower "definition-sourced fields" framing, contradicting its own opening paragraph. Recommend REVISE to fix DA-001 before merge/close of this issue-quality pass.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001 | Injection-screening scope mischaracterized as cross-document; contradicts the issue's own closing question | Critical | Body: "...covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs)"; question: "...injection-screening scope across *all* definition-sourced fields" | Actionability / Internal Consistency |
| DA-002 | "Deterministic security enforcement engine" named but not located — contributor cannot evaluate the delegation option without a lookup | Major | Body: "the repository already has a deterministic security enforcement engine this duplicates" — no name/path given | Actionability |
| DA-003 | Low-risk interim mitigation (narrow sop-brief/sop-capture's Bash grants) omitted despite being maintainer-actionable now | Minor | Register REM-07: "Interim mitigations a maintainer *could* take without redesign... narrowing sop-brief/sop-capture's Bash grants" — not in issue text | Completeness |
| DA-004 | "register section REM-07" used without a one-clause gloss for a reader with zero repo-governance context | Minor | Tracking line: "(register section REM-07)" | Self-Containedness |

## Finding Details

### DA-001: Injection-screening scope mischaracterized as cross-document [CRITICAL]

**Claim Challenged:** "The skill's prompt-injection screening likewise covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs) that end up driving tool calls."

**Counter-Argument:** This sentence implies the screening gap is about *which document type* gets screened (workflow def vs. state file vs. OE entry vs. hold log). That is not what register REM-07/G2 says. G2's defect is entirely *intra-document*: "SEC-001 screens only WARNING/CAUTION annotation content while Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and Sections 2/3/9 prose are equally attacker-controlled" — all of those are fields/sections *inside the workflow definition file*, not separate document types. The "five attacker-influenceable inputs" language the issue is echoing comes from Phase 2's STRIDE threat model (workflow definition, executor-reported paths to verifier, OE corpus, state file, hold logs) — a broader threat-surface inventory that is a *different* finding (parts of it live in REM-06, a separate cluster/issue), not the REM-07 screening-scope defect this issue tracks.

**Evidence:** `remediation-register.md` REM-07 group G2 (quoted above) vs. the issue's own closing sentence: "what is the injection-screening scope across *all* definition-sourced fields that drive tool calls?" — "definition-sourced fields" (singular artifact, many fields) is the *correct* scope and directly contradicts the opening paragraph's "several... inputs (workflow definitions, state files, ...)" framing (multiple artifacts).

**Impact:** An external contributor reading only the opening paragraph could spend effort building injection screening for state files and hold-point logs — work outside this issue's actual scope and not what REM-07 asks for — while the real gap (unscreened Action/Target/Expected Result/Sign-off Criterion/Hold Reason/prose fields inside the workflow definition) goes unaddressed. This is exactly the "wrong path" failure mode the mission statement calls out.

**Dimension:** Actionability / Internal Consistency

**Response Required:** Rewrite the sentence to match REM-07/G2 scope, or explicitly split it into two sentences if both the intra-document gap (this issue) and the broader five-input threat surface (a different concern) are intended to be mentioned.

**Acceptance Criteria:** The opening paragraph and the closing design question describe the same scope. Suggested rewrite: "The skill's prompt-injection screening (SEC-001) also only covers WARNING/CAUTION-annotated text inside the workflow definition — other fields that drive tool calls the same way (Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and free-form prose sections) are equally attacker-controlled and unscreened."

### DA-002: Unnamed, unlocated "deterministic security enforcement engine" [MAJOR]

**Claim Challenged:** "Meanwhile the repository already has a deterministic security enforcement engine this duplicates, weaker, at the prompt level."

**Counter-Argument:** The design question later offers "delegation to the existing deterministic enforcement engine" as one of three candidate fixes, but a contributor with zero repo context has no way to find this engine — no name, no path. It exists in this codebase at `src/infrastructure/internal/enforcement/security_enforcement_engine.py` (verified in the PR worktree) and is referred to in the register as "SecurityEnforcementEngine, 82 tests." Omitting the name/path forces exactly the kind of lookup the mission statement says the text should avoid.

**Evidence:** Register REM-07/G3: "a bespoke, weaker prompt-level copy of a control the repo already provides deterministically (SecurityEnforcementEngine, 82 tests) with no integration or reference." Verified path: `src/infrastructure/internal/enforcement/security_enforcement_engine.py`.

**Impact:** The "delegation" option in the design question is effectively non-actionable as worded — the contributor must grep the repo themselves to find what to delegate to.

**Dimension:** Actionability

**Response Required:** Name the engine and give a resolvable path.

**Acceptance Criteria:** Text reads, e.g., "the repository already has a deterministic command-security engine (`src/infrastructure/internal/enforcement/security_enforcement_engine.py`, ~82 tests) this duplicates, weaker, at the prompt level."

## Recommendations

**P0 (must resolve):**
- DA-001: Reconcile the opening paragraph's cross-document framing with the closing question's "definition-sourced fields" framing; pick the correct (intra-document) scope per REM-07/G2 and use it consistently.

**P1 (should resolve):**
- DA-002: Name and path the "deterministic security enforcement engine."

**P2 (may resolve; acknowledgment sufficient):**
- DA-003: Optionally add one sentence noting the low-risk interim Bash-grant narrowing a maintainer could do today.
- DA-004: Optionally gloss "register section REM-07" (e.g., "remediation cluster REM-07") for a zero-context reader.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-003: interim mitigation omitted |
| Internal Consistency | 0.20 | Negative | DA-001: opening paragraph contradicts closing question's scope |
| Methodological Rigor | 0.20 | Neutral | Core claim and severity/disposition framing trace correctly to REM-07 |
| Evidence Quality | 0.15 | Neutral | Verifiable claims (nc/http.server/base64, SecurityEnforcementEngine duplication) are accurate |
| Actionability | 0.15 | Negative | DA-001, DA-002: scope confusion + unnamed dependency both force rework/lookup |
| Traceability | 0.10 | Neutral | Worktracker path and register citation resolve correctly on-disk |
