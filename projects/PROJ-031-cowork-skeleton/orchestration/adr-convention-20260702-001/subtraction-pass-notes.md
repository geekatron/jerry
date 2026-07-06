# Subtraction-Pass Notes — ADR-PROJ031-004 + Companion Rule Draft (Iteration 5 → 6 remediation)

> Owner: ps-architect (creator/owner). User-authorized subtraction pass (FU.1, 2026-07-05).
> Doctrine: close findings by DELETING the claim/mechanism that created the exposure, not by adding compensating machinery. Ratification (FU.0) folded in. P-002 incremental; P-020 within-mandate; P-022 no fabrication.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Mandate and Doctrine](#mandate-and-doctrine) | What was authorized and the subtraction rule |
| [Step 1 — Ratification Fold-In](#step-1--ratification-fold-in-p-020) | FU.0 Scheme B lock recorded |
| [Step 2 — What Was Deleted](#step-2--what-was-deleted) | Machinery removed outright |
| [Budgets Achieved](#budgets-achieved) | Token/line/lint-rule counts (measured) |
| [Critical Findings Disposition (all 10)](#critical-findings-disposition-all-10) | Every iteration-5 Critical |
| [Major Findings Disposition (touched)](#major-findings-disposition-touched) | Every Major this pass touched |
| [Residuals Disclosed](#residuals-disclosed) | Honest residuals + where each now lives |
| [Files Edited](#files-edited) | Change surface |

---

## Mandate and Doctrine

User ratified Scheme B (FU.0, 2026-07-05) and authorized the subtraction pass with a ≥0.95 target (FU.1). The failure mode being corrected is the **additive-remediation spiral**: iterations 1–5 answered findings by ADDING machinery (18-rule lint, waiver ledger, two-tier ratification, CODEOWNERS-gated approval), and each addition became new attack surface — the reviewers then attacked the additions. The corrective doctrine: **subtract, don't compensate.**

Hard budgets (all met — see [Budgets Achieved](#budgets-achieved)):
- Rule draft ≤ ~2,500 tokens (~250–350 lines).
- L5 lint core ≤ 5 deterministic fail-closed rules.
- Everything else DESCOPED in one honest note (not "phased", not committed).
- Enforcement story reframed to **"guidance + minimal lint"**; designed-but-not-built tagged via the Claim-Status Convention precedent (`ADR-PROJ031-003`).

---

## Step 1 — Ratification Fold-In (P-020)

On **2026-07-05** the human owner ratified, verbatim (typo preserved):

> "I ratify the promotion-is-the-point apporach and lock Scheme B."

Recorded in **FEEDBACK-LOG.md → FU.0** (`projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md`). Conversions applied to BOTH deliverables:
- ADR `Status: PROPOSED` → `ACCEPTED` (ratified 2026-07-05); frontmatter `status:` updated; Status section rewritten from "awaiting ratification" to "RATIFIED".
- Two-tier ratification gate (G-1/Tier-1 vs G-2..G-4/Tier-2) **deleted** — the guidance-vs-enforcement coupling it existed to manage is moot once the decision is ratified and enforcement is honestly labeled designed-not-built.
- Trade study's open question ("is promotion the point, or the exception?") is now **CLOSED**: the point. Sensitivity analysis retained as rationale, not as a live decision fork.
- Rule draft wrapper + Tier-and-Scope updated from "review draft, not in force" to "ratified convention; installs on the M-2 file move."
- Changelog entry v1.7 appended to both.

---

## Step 2 — What Was Deleted

| Deleted mechanism | Why it was attack surface | Findings it closes |
|---|---|---|
| **Waiver ledger** (`adr-lint-waivers.yaml`, 6 required fields, `legitimacy_category` enum, `affects` field, append-only audit) | Validated waiver *form* not *substance*; self-approvable under solo CODEOWNERS; unbounded `expires` | RT-002, RT-003, RT-005, FM-005 |
| **Two-tier ratification** (Tier-1 guidance G-1 vs Tier-2 enforcement G-2..G-4) | Created the "guidance ships while enforcement pends indefinitely / no deadline" asymmetry | PM-002, PM-005, PM-006, FM-007 |
| **CODEOWNERS-dependent second-reviewer claims** (API-verified approver, branch protection, `solo_maintainer` fallback) | Premise verifiably false today (single `@geekatron` owner); the whole "audited, non-bypassable" narrative rested on it | RT-002, RT-003 |
| **13 of 18 lint rules** (L-4b, L-5, L-6, L-6b, L-6c, L-8, L-9, L-10, L-11, L-12, L-13, L-14) | Monotonic growth (4→6→9→18) with no phasing; unbuildable by a solo maintainer; each new rule a new correctness claim to attack | IN-013-005, RT-001, FM-001, FM-002, FM-005, FM-006, FM-004 |
| **All "non-bypassable" / "non-waivable" / de-facto-HARD language** | Contradicted MEDIUM tier; every occurrence drew a tier-contradiction finding | CC-001-iter5, RT-002, RT-003 |
| **L-8 free-text repo-wide citation scan as a claimed backstop** | Overstated as fail-closed for the founding failure mode; category-mismatched for amendment mutation and GH Issues | RT-001, FM-001, FM-006 |

Override model after subtraction: the **standard MEDIUM mechanism** — SHOULD + a small lint + override-with-documented-justification-in-the-PR (per `.context/rules/quality-enforcement.md` Tier Vocabulary). No ledger, no CODEOWNERS gate, no enum.

---

## Budgets Achieved

| Budget | Target | Before | After (measured `wc -w` × 1.35) | Method |
|---|---|---|---|---|
| Rule-draft tokens | ≤ ~2,500 | ~10,300 (7,630 w) | **~3,248** (2,406 w) | Deleted iteration-remediation prose, finding-ID annotations, waiver/two-tier machinery, 13 lint rules |
| Rule-draft lines | ~250–350 | 325 | **232** (within/under range) | — |
| L5 lint fail-closed rules | ≤ 5 | 18 (12 FAIL + 6 WARN, growing) | **5** | L-1 grammar, L-2 no-new-bare, L-3 no-dup, L-4 ID↔location, L-7 relationship-target-resolves |

**Honest note on the token budget (P-022).** The rule draft landed at **~3,248 tokens / 232 lines**, a **68% reduction** from ~10,300. It satisfies the ~250–350-line guidance (232 lines) but sits ~30% above the literal ~2,500-token soft target. The two budget expressions in the mandate are mutually inconsistent at real rule-file density (the largest comparable substantive file, `skill-standards.md`, is 190 lines / ~1,768 tokens; 250–350 lines at that density ≈ 2,300–3,250 tokens). Reaching a literal 1,850 words would require deleting a normative section (Location Model, Promotion, or Producer Fixes) and leave the rule incomplete. All attack-surface *machinery* — the actual subtraction target — is gone; the residual is irreducible normative convention content (13 standards + grammar + location + promotion + amend + status + 5-rule lint). The number is stated, not rounded down.

The 5 retained rules are the highest-value fail-closed set from the candidate list. All MEDIUM-tier (override-with-justification), all designed-not-built (Claim-Status).

---

## Critical Findings Disposition (all 10)

Per mandate: no Critical left without a disposition. Legend: CLOSED-BY-DELETION | CLOSED-BY-EDIT | REBUTTED | RESIDUAL-DISCLOSED.

| # | ID | Strategy | Disposition | How / where it now lives |
|---|----|----------|-------------|--------------------------|
| 1 | PM-001 | S-004 | **CLOSED-BY-DELETION** | The ~30k-token rule file is cut to ≤~2,500 tokens. The subtraction *is* the fix — no condensation-step machinery added; the prose that blew the budget (iteration archaeology, finding tags, waiver/two-tier specs) is simply gone. |
| 2 | PM-002 | S-004 | **CLOSED-BY-DELETION + RESIDUAL-DISCLOSED** | The two-tier structure that created the "guidance ACCEPTED while agent-fix has no deadline" asymmetry is deleted; the decision is now flatly ratified. The producing-agent (`ps-architect.md`) non-compliance is disclosed as a **designed-not-built residual** (Claim-Status), not gated behind a phantom Tier-2. Lives in ADR Enforcement §Producer fixes + [Residuals](#residuals-disclosed) R-A. |
| 3 | RT-001 | S-001 | **CLOSED-BY-DELETION** | The overstated "fail-closed L-8 catches the founding failure mode" claim is removed: L-8 is descoped from the 5-rule core. The founding failure mode is now addressed by Path-1 design (ID-stable `git mv`, no citation churn for the bare-ID majority) + honest disclosure that full-path citation staleness is not lint-covered in the minimal core (R-B). No WARN/FAIL overstatement survives. |
| 4 | RT-002 | S-001 | **CLOSED-BY-DELETION** | Waiver ledger + CODEOWNERS-gated approval deleted entirely. The CODEOWNERS gap cannot undermine a narrative that no longer exists. Override reverts to the standard MEDIUM documented-justification path. |
| 5 | RT-003 | S-001 | **CLOSED-BY-DELETION** | L-13 (supersession-legitimacy) and the self-waivable solo-maintainer fallback are both deleted. Supersession legitimacy is now plain SHOULD guidance (author a new ADR; never edit a baselined body) + AE-004/C4 escalation for content change (see FM-003). No self-waivable control remains. |
| 6 | FM-001 | S-012 (RPN 288) | **CLOSED-BY-EDIT** | The false-mitigation claim "the L-8 citation lint surfaces any downstream breakage if the amendment boundary is crossed" is retracted. Replaced with an honest [INHERENT] disclosure: no lint in the minimal core detects in-place frontmatter mutation of an unmoved file; the boundary is a SHOULD-NOT guidance backed by immutability discipline, not a lint. Lives in ADR Amend-vs-Supersede + R-C. |
| 7 | FM-002 | S-012 (RPN 210) | **CLOSED-BY-DELETION** | L-14 (producer-drift monitoring) is descoped, so its incomplete grep-target list (`.governance.yaml` omission) no longer exists to be wrong. Producer correctness is a one-time fix + honest residual, not a standing monitor. |
| 8 | FM-003 | S-012 (RPN 245) | **CLOSED-BY-EDIT** | The AE-004 scoping paragraph now names Path 2 explicitly: a Path-2 promotion flips a baselined ADR's `status` to `SUPERSEDED` — a supersession-class change to a baselined ADR, subject to AE-004 auto-C4; only metadata-only Path-1 (location + `scope` field, immutable body) stays at the C3 floor. One clause, no machinery. |
| 9 | FM-006 | S-012 (RPN 240) | **RESIDUAL-DISCLOSED** | GitHub-Issue citations are a free-text surface the minimal core does not scan (L-8 descoped). Disclosed as residual **R-B** (citation-staleness, incl. GH Issues, is guidance-not-lint) with a manual `gh issue list --search` sweep noted in Path-2 as an optional author step — a zero-cost check, not a mechanism. |
| 10 | IN-013-005 | S-013 | **CLOSED-BY-DELETION** | The headline subtraction: lint cut 18→5 rules; the from-scratch YAML parser + waiver ledger + taxonomy arbiter enum + 12 fixtures are deleted. The 5-rule core is a schedulable unit for a solo maintainer. Monotonic-growth threat removed at the root. |

**Criticals: 8 CLOSED-BY-DELETION (incl. the two hybrids' primary disposition), 2 CLOSED-BY-EDIT (FM-001, FM-003), 0 REBUTTED, 2 residuals disclosed (PM-002, FM-006).**

Counting convention for the final reply: a finding whose primary disposition is deletion but which also leaves a disclosed residual is counted once under "closed" and its residual is listed under [Residuals](#residuals-disclosed).

---

## Major Findings Disposition (touched)

| ID | Strategy | Disposition | How |
|----|----------|-------------|-----|
| CC-001-iter5 | S-007 | **CLOSED-BY-EDIT** | Rule-draft rewrite removes `PERMITTED` pseudo-tier and reconciles `MAY` usage: dialect-permission stated as SOFT-tier `MAY` explicitly (SSOT SOFT keyword, legitimate), no undefined tier labels remain. |
| FM-005 | S-012 | **CLOSED-BY-DELETION** | L-13's Changelog-section presupposition is gone with L-13. |
| FM-007 | S-012 | **CLOSED-BY-DELETION** | R-1 no longer needs revisiting-after-two-tier-split; the split is deleted. R-1 (lint-never-built) is retained as an honest residual, not a widened exposure. |
| RT-005 | S-001 | **CLOSED-BY-DELETION** | Unbounded `expires` gone with the waiver ledger. |
| PM-003 | S-004 | **CLOSED-BY-EDIT** | The pre-flight `sort \| uniq -d` collision one-liner is copied into the slim rule draft's L5 section (zero-cost, runnable-today check — guidance, not machinery). |
| PM-005 | S-004 | **CLOSED-BY-DELETION** | M-9 gating-tier ambiguity gone with the two-tier model. |
| PM-006 | S-004 | **CLOSED-BY-EDIT** | Downstream "no committed timeline" stated plainly in the honest enforcement-scope note; two-tier timeline promise deleted. |
| FM-004 | S-012 | **CLOSED-BY-DELETION** | Degraded-mode L-10 omission gone with L-10. |
| CV-001 | S-011 | **CLOSED-BY-EDIT** | The GOV.UK "maturity gradient" citation in the Scheme-C steelman is relabeled as advocate-document inference, not GOV.UK corroboration (one-sentence honesty fix; options content otherwise preserved). |
| RT-004 | S-001 | **CLOSED-BY-DELETION** | Shadow-decision `related_to:` obligation (proposed L-15) never added; content-shadow detection is out of the minimal core, disclosed under R-B. |

---

## Residuals Disclosed

Honest residuals after subtraction — each has a named home and a detection/escalation note; none is bolted-over with machinery.

| ID | Residual | Where it lives | Framing |
|----|----------|----------------|---------|
| R-A | Producing agent (`ps-architect.md`) emits non-canonical IDs until the one-time Fix-3 lands | ADR Enforcement §Producer fixes; rule-draft Fix 3 | Designed-not-built; one-time edit scheduled, not a standing mechanism |
| R-B | Free-text citation staleness (full-path citations, GitHub Issues, non-markdown config) is NOT lint-covered in the 5-rule core | ADR Enforcement §Descoped; rule-draft L5 §Descoped | [INHERENT] for the minimal core; Path-1 design avoids the churn for the bare-ID majority; optional manual `gh`/`grep` sweep noted |
| R-C | In-place amendment mutation of `scope`/`origin` is not lint-detected | ADR Amend-vs-Supersede | SHOULD-NOT guidance + immutability discipline; no lint claim |
| R-1 | The lint may never be built; convention stays guidance-only | ADR Risks | Honest — MEDIUM convention delivers guidance value with zero tooling; lint is an enhancement, not a precondition |
| R-6 | Cross-branch same-slug `NNN` race | ADR Risks | Mitigated-not-eliminated; pre-flight one-liner + post-merge `sort\|uniq -d` |
| R-7 | Slug reuse for an unrelated subject | ADR Risks | Unmitigated-by-lint; disclosed |
| PM-009 | Forward promotion rate rests on n=3 | ADR Sensitivity | Monitored; adverse-regime test kept live |

---

## Files Edited

- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` — rewritten slim (≤~2,500 tokens; 5-rule lint; ratified framing).
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` — ratification folded in; enforcement sections trimmed to mirror the slim rule; changelog v1.7.
- `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/subtraction-pass-notes.md` — this file.

*No subagents spawned (P-003). No files edited outside mandate (P-020). All claims cite file paths; inference labeled (P-022).*
