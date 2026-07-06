# Iteration-7 Remediation Notes — ADR-PROJ031-004 + Companion Rule Draft

> Owner: ps-architect (creator/owner). OWNER-FIRST remediation after iteration-7 S-014 (score 0.64; engagement gate 0.95).
> **Binding doctrine (user-authorized FU.1, 2026-07-05): SUBTRACTION-FIRST.** Close findings by DELETING the exposing claim/mechanism, not by adding compensating machinery. Adding a mechanism requires deleting something bigger and stating the trade. If a finding cannot be closed by subtraction/edit, REBUT with evidence or DISCLOSE as an honest residual — never bolt on machinery.
> P-002 incremental (this file written before edits, updated as each lands). P-020 within-mandate. P-022 no fabrication — file:line cited; inference labeled.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Empirical Verifications](#empirical-verifications) | Shell-confirmed facts grounding the dispositions (P-022) |
| [Critical Dispositions (7)](#critical-dispositions-7) | Every iteration-7 Critical |
| [Major Dispositions](#major-dispositions) | Every fixable-now Major |
| [Declined / Rebutted](#declined--rebutted) | Findings closed by rebuttal or doctrine-decline |
| [INHERENT (already disclosed)](#inherent-already-disclosed) | Organizational/engineering actions outside a document edit |
| [Trade Ledger](#trade-ledger) | Every addition and the larger thing deleted to pay for it |
| [Files Edited](#files-edited) | Change surface |

---

## Empirical Verifications

All confirmed by shell this pass (2026-07-06), not accepted on report alone (P-022):

| # | Claim | Method | Result |
|---|-------|--------|--------|
| V-1 | **IN-001 L-3 regex false-negative is REAL** | Ran the exact one-liner extraction against `ADR-agent-design-001-port-443-config` + `ADR-agent-design-001-simple-tail` | Extracts `ADR-agent-design-001-port-443` vs `ADR-agent-design-001` → the duplicate is **MISSED** by `uniq -d`. Confirmed, not merely reasoned. |
| V-2 | An awk "first-3-digit-group" fix is **not a clean win** | Ran candidate awk extraction against the same set + `ADR-150-001` | Fixes the title-tail case but mis-extracts numeric-leading legacy `ADR-150-001` → `ADR-150`. Trades one edge case for another; adds complexity. Rejected per doctrine. |
| V-3 | **CC-001: no `ADR-PROJ007-*` file survives** | `find … -name 'ADR-PROJ007-*'` | Empty. L-7 structurally cannot have inspected this ID → the "(ADR-PROJ007-001/002 failure class)" attribution is an overclaim. |
| V-4 | **DA-001: the cited stale PROJ-007 citations still exist** | `grep -rn ADR-PROJ007-00 projects/PROJ-007-agent-patterns` | Live at `WORKTRACKER.md:106-107`, `ORCHESTRATION.yaml:228,242`, `EN-001.md:48-49,72-73` — exactly as the ADR's L0/Context cite. |
| V-5 | **CV-001: rule draft's true current size** | `wc -l/-w` | **238 lines / 2885 words / ~3894 tokens (×1.35)**. Changelog v1.7 says "233 lines/~3.3k"; notes "Files Edited" says "240 lines/~3.9k" — three unreconciled figures. Truth = 238 / ~3.9k. |

---

## Critical Dispositions (7)

Legend: DELETE-OVERCLAIM | CORRECT | DISCLOSE-RESIDUAL | RECONCILE. No Critical closed by adding machinery.

| # | ID | Disposition | How (subtraction-first) |
|---|----|-------------|-------------------------|
| 1 | FM-001-20260706I7 (DEPRECATED/SUPERSEDED self-contradiction) | **DELETE-OVERCLAIM + RECONCILE** | The exposure is the false claim that `DEPRECATED` is *terminal*. Reality (already stated at ADR:622): a `DEPRECATED` decision that later acquires a specific replacement transitions to `SUPERSEDED`. Deleted `DEPRECATED` from the "terminal states do not transition further" clause (only `SUPERSEDED` is terminal); added the `DEPRECATED→SUPERSEDED` row to the transition table. No new machinery — a false invariant removed and the table made consistent with the prose that was already correct. Both files. |
| 2 | FM-002-20260706I7 (grandfather "19" vs "18") | **CORRECT** | ADR:517 (M-6 row) said "16 dialect + 3 canonical = 19"; the correct, already-4×-stated figure is **18** (15 dialect reachable + 3 canonical; STORY015 out-of-scan per R-10). One-line edit to the single stale occurrence. |
| 3 | RT-001-20260706I7 ("Repo-wide" overclaim) | **DELETE-OVERCLAIM + DISCLOSE-RESIDUAL** | The scan roots are hard-coded `find projects docs/design -path '*/decisions/*'`, which never reach the repository-based topology's `{RepositoryRoot}/decisions/` home (ADR:376). Deleted the unqualified "Repo-wide"; replaced with the honest scanned-root scope + a disclosed residual (generalized R-10 to the **out-of-scan location class**: entity-embedded AND repository-based-topology homes), parallel to L-4's existing topology caveat. No scan-root machinery added (that would need the unbuilt M-6). |
| 4 | DA-001-20260706 (no task for founding stale citations) | **DISCLOSE-RESIDUAL** | Extended M-10 (which already handles the dangling `ci.yml` `ADR-CI-001` citation, "not edited by this ADR per P-020") to also name the verified-live stale `ADR-PROJ007-001/002` citations (`WORKTRACKER.md:106-107`, `ORCHESTRATION.yaml:228,242`, `EN-001.md:48-49,72-73`). Same class, same P-020 boundary, same owned-action framing. No new mechanism — a disclosure row that already had a precedent. |
| 5 | CC-001-20260706iter7 (L-7 overclaims PROJ007 class) | **DELETE-OVERCLAIM** | V-3 confirms no `ADR-PROJ007-*` file survives for L-7 to inspect. Deleted the "(the `ADR-PROJ007-001/002` failure class)" attribution; reworded L-7 to describe only the **forward-looking** structural-orphan scenario it actually catches (a half-completed Path-2 whose `promoted_to`/`superseded_by` target does not resolve). Both files. Same defect *pattern* the subtraction pass already fixed once on L-8 — now removed on L-7. |
| 6 | IN-001-20260706-iter007 (L-3 regex false-negative) | **DISCLOSE-RESIDUAL + bounded guidance** | Empirically CONFIRMED (V-1). Closed by **subtraction, not a regex swap**: (a) disclosed the false-negative as residual **R-13** with the worked counter-example; (b) added a bounded SHOULD-NOT guidance — title-slug tails SHOULD NOT contain standalone 3-digit tokens (mirrors R-9's case-fold SHOULD-NOT), which removes the trigger by convention. **Trade stated:** declined the awk "first-3-digit" rewrite because V-2 shows it trades the title-tail edge case for a numeric-leading-legacy edge case (`ADR-150-001`→`ADR-150`) and adds pipeline complexity — not a clean win, and complexity is the exact thing the doctrine subtracts. Disclosure adds zero attack surface. |
| 7 | PM-001-iter007 (Pre-Mortem omits compound non-adoption) | **MODEL (analysis completeness)** | Added Pre-Mortem row **FM-5** modeling the best-evidenced compound scenario: M-2 (relocation), M-6 (lint) and M-12 (producer fix) all stay untracked → the convention never takes effect beyond this document. This is completing an *analysis table* (honest risk modeling), not adding an enforcement mechanism. Detection/containment columns point at existing disclosures (M-2/M-12 Claim-Status), no new machinery. |

---

## Major Dispositions

| ID | Disposition | How |
|----|-------------|-----|
| PM-002-iter007 (disposition overclaims RT-002/003 closure) | **DISCLOSE + RECONCILE** | (a) In `subtraction-pass-notes.md`, softened RT-002/RT-003 from "CLOSED-BY-DELETION" to "CLOSED-BY-DELETION + RESIDUAL-DISCLOSED", naming the inherited condition. (b) In the ADR, added one honest line: the MEDIUM documented-justification override is self-approvable under the solo `@geekatron` maintainer — **inherent to MEDIUM tier + solo maintenance, not a gate to rebuild**. The deletion removed the ledger's *structure*; the underlying single-approver reality is disclosed, not papered over. |
| PM-003-iter007 (M-9 no non-execution fallback) | **DISCLOSE** | Added an honest fallback to the Meta-Note/M-9: if M-9 never executes, the self-compliance demonstration stays *described, not performed* — an honest residual (the Meta-Note already labels it inference-not-action), monitored the same way as PM-009, not backed by new machinery. |
| DA-002-20260706 ("eliminates" overclaim) | **SOFTEN-OVERCLAIM** | ADR:423 Positive-1 "Eliminates the demonstrated failure mode" → "Removes the ID-string-churn *cause* of the demonstrated failure mode for the bare-ID majority; the full-path/free-text minority is a disclosed residual (R-B)." The 72%/28% scope limitation is already disclosed at ADR:549; the headline claim is narrowed to match it. |
| DA-004-20260706 (L-4 zero coverage repo-based) | **DISCLOSE** | Strengthened ADR:383/662 wording from "inapplicable/scoped to project-based" to explicitly state L-4 has **zero operative effect** (not degraded) under the repository-based topology — PROJ-031's named downstream audience. |
| DA-005-20260706 ("not committed" vs named thresholds) | **RECONCILE** | Clarified that "not phased, not committed" scopes the **descoped lint items** (no future lint rules promised); the R-6/R-7/PM-009 monitoring commitments are a distinct category (honest residual monitoring with named detection signals), not lint promises. One clause each in the ADR + rule-draft descoped notes. |
| FM-003-20260706I7 (L-4 omits FEAT) | **CORRECT** | Added `FEAT{NNN}` to L-4's dialect enumeration in both files, matching the closed `{PROJ\|EPIC\|FEAT\|STORY}` set the grammar already declares. |
| FM-005-20260706I7 (R-11 consequence untraced) | **DISCLOSE** | Added one sentence to R-11 naming the concrete consequence: a new ADR can set `supersedes:` while its predecessor's `status`/`superseded_by` go unchecked, leaving a superseded ADR still reading `ACCEPTED`. |
| FM-006-20260706I7 (M-9 cost "Trivial") | **CORRECT** | ADR:492 corpus-state cost "Trivial" → "Low (multi-part; reciprocal-link atomicity — see M-9)". |
| CC-002-20260706iter7 (AE-004 narrowed w/o SSOT authority) | **DISCLOSE** | Added "this is the ADR's own interpretation of AE-004's scope, pending SSOT harmonization" to the Path-1-C3 scoping clause. The actual SSOT amendment is [INHERENT] (separate governance action), disclosed as such. |
| CC-003-20260706iter7 (MUST vs must, ADR:314) | **HYGIENE** | Lowercased the uppercase `MUST` in the ID-grammar code-block comment (tool/grammar mechanics, not an author obligation), matching the rule draft's CC-001 mechanism-scoping convention. |
| RT-002-20260706I7 (R-10 bounded vs class) | **DISCLOSE (merged with #3)** | R-10 reworded from a single STORY015 instance to the entity-embedded **location class** — and, per RT-001, extended to also cover the repository-based-topology out-of-scan home. One residual now covers the out-of-scan location class. |
| CV-001-20260706T1 (rule-draft count 3 figures) | **CORRECT** | Reconciled to the V-5 measured truth (238 lines / ~3.9k tokens) in the rule-draft changelog and the notes' Files-Edited row. |
| CV-002-20260706T1 (M-14 dual "15") | **CORRECT** | Disambiguated the two populations: "15 pre-existing dialect ADRs" vs "15 incl. this in-flight ADR" — added a one-word qualifier to each. |
| RT-004-20260706I7 (case-fold FS collision) | **DISCLOSE** | Extended R-9 to note that case-insensitive filesystems (macOS/Windows default) can also collide two canonical slugs differing only in case — same SHOULD-NOT-guidance disposition, no lint. |
| DA-006/007/008 (P2 optional) | **ACKNOWLEDGE** | DA-008 (lost override observability): added a note that override-frequency sampling can ride the M-5b review cadence rather than a standing ledger. DA-006/007 tone/severity: acknowledged, no wording churn (P-022: severity is reviewer judgment). |

---

## Declined / Rebutted

| ID | Disposition | Rationale (doctrine-aligned) |
|----|-------------|------------------------------|
| FM-004-20260706I7 (no consolidated onboarding narrative) | **REBUT / DECLINE** | Adding a 10–15-line "Authoring your first ADR" checklist is the **exact additive move the subtraction doctrine forbids**, and it would push the rule draft further past its HARD token budget (already 238 lines / ~3.9k vs ~2.5k target, V-5). The onboarding narrative was **deliberately deleted** in the subtraction pass. Guidance is intentionally distributed across the ID-Scheme / Location / Promotion sections. Disclosed as a deliberate design posture, not an omission. Major, not Critical; not automatic-REVISE-triggering. |
| SM-003-iter007 (cite subtraction doctrine as reusable precedent inside the ADR) | **DECLINE (budget)** | Purely additive pedagogy; the doctrine is already recorded in `subtraction-pass-notes.md` and the changelog. Adding it to the ADR body grows surface for zero correctness gain. |
| SM-002/004/005/006-iter007 (quick-start, L0 rigor pointer, best-case consolidation, tag-prefix disclosure) | **DECLINE (budget / additive)** | Additive strengthening opportunities; declined under the subtraction mandate and token discipline. SM-001 (grandfather count) overlaps Critical #2 and is **fixed** there. |

---

## INHERENT (already disclosed)

| ID | Why not a document edit |
|----|-------------------------|
| IN-002-20260706-iter007 (M-2/M-12 untracked) | Opening real worktracker Tasks + GH Issues is organizational action, not a markdown edit. Already disclosed as pending-not-fabricated at ADR:506 (Claim-Status). No fabricated IDs (P-022). |
| A1 (lint build, M-6) | Engineering time; disclosed as designed-not-built (R-1, Claim-Status). |
| A2 (producer-agent fix, M-12) | Edit to `ps-architect.md` outside this ADR's mandate; disclosed as R-A. |
| A3 (forward promotion rate n=3) | Requires 2–3 more framework-relevant projects; disclosed and monitored (PM-009). |
| SSOT AE-004 harmonization (CC-002 tail) | An actual amendment to `quality-enforcement.md` is a separate governance action; disclosed as pending. |

---

## Trade Ledger

Per doctrine, every *addition* names the *larger* thing deleted to pay for it:

| Addition | Size | Paid for by deleting | Net |
|----------|------|----------------------|-----|
| R-13 residual + SHOULD-NOT title-slug guidance (IN-001) | ~3 lines | The false implication that L-3's one-liner is collision-complete (an overclaim larger than the disclosure) + declined an awk rewrite (net-negative complexity avoided) | Honest, smaller |
| FM-5 Pre-Mortem row (PM-001) | 1 table row | Removes the silent gap where the best-evidenced risk was unmodeled | Neutral (analysis, not machinery) |
| `DEPRECATED→SUPERSEDED` transition row (FM-001) | 1 table row | Deletes the false "DEPRECATED is terminal" invariant | Net-negative (a false rule removed) |
| Out-of-scan location-class disclosure (RT-001/RT-002) | ~2 lines | Deletes 2× unqualified "Repo-wide" overclaims | Net-negative |
| `FEAT` in L-4 (FM-003) | ~5 chars ×2 | — (pure completeness of an existing closed set) | Trivial |

No lint rule, ledger, gate, matrix, or "non-bypassable" language added anywhere.

---

## Files Edited

- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` — Critical + Major dispositions; changelog v1.9.
- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` — L-7 reword, L-4 FEAT, L-3 Repo-wide qualifier + R-13 residual, count reconciliation; changelog v1.9.
- `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/subtraction-pass-notes.md` — RT-002/RT-003 disposition softened (PM-002); Files-Edited count reconciled (CV-001).
- `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-007/remediation-notes.md` — this file.

*No subagents spawned (P-003). No files edited outside mandate (P-020). All claims cite file:line; inference labeled (P-022).*
