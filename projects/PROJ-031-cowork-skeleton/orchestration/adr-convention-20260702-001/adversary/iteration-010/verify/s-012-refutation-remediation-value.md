# S-012 (FMEA) Critical Refutation Panel — Remediation-Value Lens (Iteration 10)

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What this panel reviewed |
| [Verdicts](#verdicts) | Per-Critical verdict with reasoning |
| [Summary](#summary) | Final tally |

---

## Scope

Target report: `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-012-findings.md` (S-012 FMEA, iteration 10).

**Lens:** remediation-value — would fixing this materially change real adoption outcomes, or is it churn? Findings whose fix is optional polish, already scheduled elsewhere, or would ADD machinery against the ratified subtraction doctrine are REFUTED. Default to REFUTED if uncertain.

**Criticals in scope:** exactly one — `012-004` (Findings Summary table, s-012-findings.md:92; the only row with Severity=Critical). `012-005` and `012-006` are Major and out of scope for this panel's mandate (Critical refutation only).

---

## Verdicts

### 012-004: Grandfather-baseline enumeration excludes PROJ-014's bare drafts, which L-2's unscoped wording would otherwise catch

**Verdict: REFUTED**

**Reasoning:**

The underlying textual observation is factually accurate — I independently verified it. `ADR-PROJ031-004:686` scopes L-1 explicitly to `projects/*/decisions/`, `docs/design/`, while `ADR-PROJ031-004:687`'s L-2 row carries no scope qualifier at all, and the rule draft's parallel L-2 row (`adr-standards-rule-draft.md:176`) uses the word "anywhere" verbatim. I also confirmed the operational baseline enumeration is a closed, named list — `ADR-PROJ031-004:226-229` defines "16 = the whole dialect corpus" as exactly `EPIC002×2, PROJ010×6, PROJ022×2, PROJ031×4, STORY015×1, 150×1 = 16`, with no `PROJ014` entry, even though `ADR-150-001` (which structurally fails both canonical and dialect grammar per line 686's own admission) is deliberately folded into that list as a named grandfather exception. The Frozen-and-Grandfathered-Legacy prose (`adr-standards-rule-draft.md:94`) separately asserts PROJ-014's bare files "are... grandfathered... as historical artifacts" — a claim that is not backed by inclusion in the operational 16/18/19 enumeration the lint's grandfather mechanism actually consults. This is a real, internally-inconsistent gap between prose-level and enumeration-level "grandfathered" claims.

However, under the remediation-value lens this does not clear the bar for VERIFIED. Three independent facts sharply bound the real-world consequence to near-zero: **(1)** the lint this finding concerns (`scripts/lint_adr_convention.py`, M-6) is Glob-verified not to exist and has "no committed timeline" (`ADR-PROJ031-004:501,680`) — there is no running enforcement mechanism today for this gap to bite against; **(2)** the Migration Plan itself dispositions PROJ-014's 4 files as "Low priority; rename to a domain slug... only if promoted" (`ADR-PROJ031-004:517`) — the design's own planned remediation path (rename) independently eliminates the bare-ID condition that would trigger L-2, making the false-positive scenario self-resolving before it can occur in the common case; **(3)** even in the residual edge case (an unrelated edit to a still-bare PROJ-014 file before rename), the consequence is a MEDIUM-tier, override-with-documented-justification-in-the-PR outcome (`subtraction-pass-notes.md:63`, `adr-standards-rule-draft.md:167`) — the exact zero-machinery compensating control this project has repeatedly and deliberately chosen over gates/ledgers for every comparable edge case (R-9, R-10, R-13, R-14, R-16 in the residual register are all structurally identical "scan-scope/enumeration edge case" disclosures, none escalated past Major/disclosed-residual in nine prior rounds). Fixing this changes zero observable behavior today (no lint runs), and even post-M-6 the fix only prevents a trivially-overridable warning on a "Low priority" file class the design already plans to eliminate by rename. This is optional textual/enumeration polish to a not-yet-built control's edge-case handling, not a defect with a material adoption consequence — squarely the "churn" category this lens is designed to filter, and the finder's own Summary (`s-012-findings.md:36`) independently concedes as much ("the same class of gap the package has repeatedly and honestly closed in prior rounds — text/disclosure fixes, not new machinery").

---

## Summary

| Verdict | Count | IDs |
|---|---|---|
| VERIFIED | 0 | — |
| REFUTED | 1 | 012-004 |

**Note:** `012-005` and `012-006` (Major severity) were read for context but are outside this panel's Critical-only mandate and are not scored above.
