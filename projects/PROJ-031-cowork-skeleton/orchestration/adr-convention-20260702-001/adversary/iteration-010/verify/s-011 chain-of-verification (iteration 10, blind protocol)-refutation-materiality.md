# Materiality Refutation Panel — S-011 Chain-of-Verification (Iteration 10, Blind Protocol)

> **Lens:** Materiality — does the finding genuinely block the standard's purpose (collision-free identity, honest promotion, adoptable convention)? Negligible-probability x impact, cosmetic, and style-preference findings are REFUTED even if factually accurate.
> **Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-011-findings.md`
> **Protocol:** Blind — no other refuter/panel output read.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | Which findings are in scope |
| [Verdict](#verdict) | Verdict per Critical finding ID |
| [Reasoning](#reasoning) | Evidence-cited reasoning |
| [Summary](#summary) | Tally |

---

## Scope

The target report contains exactly **one** Critical finding: `CV-001-i010`. All other 18 verification-log entries are `VERIFIED` (clean, no discrepancy) and are out of scope for this refutation panel (only Criticals are refuted/verified per mandate).

---

## Verdict

| ID | Verdict |
|----|---------|
| CV-001-i010 | **REFUTED** (materiality) |

---

## Reasoning

### CV-001-i010: "Canonical Location Model omits the actual location pattern of the two grandfathered `EPIC002` dialect ADRs; L-4 would misfire on them"

**Underlying fact-check (not disputed).** The Canonical Location Model table (ADR `decisions/ADR-PROJ031-004-adr-identifier-convention.md:384-393`; rule-draft `design/adr-standards-rule-draft.md:77-88`) indeed has no row whose (location, ID-form) pair matches `ADR-EPIC002-001-strategy-selection.md` / `ADR-EPIC002-002-enforcement-architecture.md`, which live in `projects/PROJ-001-oss-release/decisions/` (a project-level `decisions/` folder) under the `EPIC002` dialect prefix — row 4 ("Project (permitted dialect)", ADR-PROJ031-004:389) sanctions only `ADR-PROJ{NNN}-NNN` at that location, and row 5 ("Entity-embedded", ADR-PROJ031-004:390) sanctions the `EPIC{NNN}` prefix only inside a `work/.../{ENTITY}/` folder. This factual gap is real and I do not dispute it.

**Why it does not clear the materiality bar for Critical, given the actual constraints on when/whether it could ever bite:**

1. **The lint does not exist.** `scripts/lint_adr_convention.py` is Glob-verified absent (ADR-PROJ031-004:659, rule-draft:165); enforcement is explicitly "advisory-only" today (Claim-Status Convention, ADR-PROJ031-004:659). There is zero live failure mode — the finding is entirely about what a not-yet-built tool *might* do.
2. **The triggering Migration-Plan action is itself optional and non-gating.** M-11 (ADR-PROJ031-004:546) is explicitly marked **"No (optional schema-completeness; not lint-gating)"** and is an unscheduled `TBD-Task` — it retrofits YAML `id`/`scope`/`origin_project` fields onto the two EPIC002 files, and does **not** rename or relocate them. Whether M-11 ever executes, and whether it executes *before or after* M-6 (the lint build, itself undated, with "nothing lands" rated the best-evidenced risk per M-6/FM-5 cross-reference at `subtraction-pass-notes.md:75` and ADR-PROJ031-004:659 Claim-Status framing), is a double-conditional the finding must assume resolves unfavorably to manifest at all.
3. **Even in the worst case, the blast radius is 2 named legacy files, not the scheme's forward-going collision-resistance property.** The convention's core purpose — collision-free identity for *new* ADRs — is untouched; this is a potential false-positive against 2 already-disclosed grandfathered legacy files, not a defect in the ID/location grammar authors follow going forward.
4. **A standing, zero-friction remedy already exists and is explicitly designed for exactly this class of issue.** Every lint FAIL, L-4 included, is "overridable with a documented justification in the PR" with no waiver ledger or CODEOWNERS gate (ADR-PROJ031-004:657, rule-draft:167) — the precise mechanism that would absorb a false-positive on these 2 files at zero process cost, the same mechanism the document relies on throughout for narrower analogous gaps.
5. **This finding is structurally identical in kind and cost to residuals the project's own 9-iteration remediation record already treats as Major/RESIDUAL-DISCLOSED, not Critical.** R-9 (case-fold shadowing, L-1), R-10 (entity-embedded out-of-scan), R-14 (frozen-dir new-file collision), R-15 (frontmatter `id:` uniqueness unchecked), R-16 (L-7 zero real targets today), and R-17 (concurrent-supersession race) are all narrow, disclosed, lint-design gaps affecting a bounded file set, each dispositioned by one-sentence disclosure with **no new machinery** (`subtraction-pass-notes.md:191-201`). CV-001-i010's own recommended remediation — "a small, targeted table/prose edit... no new lint rule required" (target report line 75) — is the identical remedy class as those Major-tier residuals, which is itself evidence this finding belongs in that tier, not Critical.
6. **The reviewer's own two competing readings both terminate in "disclose a residual," not "the standard is broken."** The finding's own §Correction offers option (b): "explicitly disclose a new residual (parallel to R-9/R-10)" as a fully sufficient fix (target report line 75) — i.e., even the finder concedes the deliverable's purpose survives with a one-line disclosure, which is the opposite of a Critical, blocking defect.

**Materiality conclusion:** the probability (lint built AND M-11 executed AND the literal interpretation holds) is compound-conditional and low, the impact is bounded to 2 named legacy files with a pre-built override valve, and the fix-cost/finding-class is identical to prior Major/residual-disclosed dispositions in this same review lineage. This does not "genuinely block collision-free identity, honest promotion, or adoptable convention" — it is a real but narrow documentation-completeness gap, not a Critical.

---

## Summary

- **Verified (Critical):** none
- **Refuted (Critical):** CV-001-i010
- Note: no other Critical findings existed in the target report to adjudicate.
