# S-002 Refutation Pass — Materiality Lens (Iteration 8)

> **Lens:** materiality — does the finding genuinely block the convention's purpose (no lost feedback/decisions, operator-burden-free capture, navigable growth, honest metadata)? Improbable edge cases and style points are REFUTED even if technically true.
> **Target:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-002-findings.md`
> **Scope:** the 2 Criticals only (DA-001-i8, DA-002-i8), per this panel's assignment.
> **Method:** direct-quote verification against the deliverable files at the cited lines, plus a check for whether each concern is already an accepted/disclosed residual per the design doc's own Revision Changelog / `iteration-007/restore-notes.md`.

## Navigation

| Section | Purpose |
|---------|---------|
| [DA-001-i8](#da-001-i8) | Worktree/branch merge renumbering vs. external citations |
| [DA-002-i8](#da-002-i8) | FM-001 location-only dedup vs. edited markers |
| [Verdict Summary](#verdict-summary) | Final table |

---

## DA-001-i8

**Claim:** the worktree/branch merge-conflict renumbering rule (design doc `feedback-decision-log-convention-design.md:79`; rule file `feedback-decision-logs-standards.md:27`) contradicts the "ids never reset" invariant (design doc `:198`) for graduated/externally-cross-linked ids, with no repair path for citations held outside the two log files (ADR `Reflected in:`, DECISION `Source:`).

**Verification of quotes:** confirmed accurate. Design doc line 79 (the "Scope boundary" bullet) does state the worktree/branch case and the renumber-never-discard rule; rule file line 27 (LOG-M-005) restates it; design doc line 198 (L1.4 linked-list/cross-log-nav row) does state "ids never reset, so a reference survives rotation."

**REFUTED (materiality).** Two independent reasons:

1. **The "ids never reset" invariant is scoped to rotation, not to the disclosed-residual multi-writer path.** Design doc line 198 states the invariant specifically in the context of *segment rotation* under the single-writer discipline ("`next` is written once at seal time — sealed segments never relink; ids never reset..."), i.e., the validated single-operator-per-log scope (`feedback-decision-logs-standards.md` Scoping section, "Adoption profile: validated for a single operator per log"). The very same paragraph the finding quotes (design doc line 79) already brackets the worktree/branch scenario as an explicitly out-of-scope case: *"Operators SHOULD NOT run concurrent sessions or direct hand-edits against the same log, and SHOULD resolve worktree/branch merge conflicts on log files by the never-discard rule above; these are named residuals, not covered cases."* There is no true logical contradiction between an invariant scoped to the supported single-writer path and a disclosed, SHOULD-NOT-do residual procedure for an explicitly unsupported concurrent-writer path.
2. **This is a compound, low-probability edge case that is already substantively disclosed.** It requires: (a) worktree/branch-isolated dispatch used against the *same* log path, (b) independent id collision across branches, (c) one colliding id having *already* graduated to an external ADR/DECISION cross-link before the merge, and (d) the merge-resolving operator not grepping for the old id string. The design doc's own Revision Changelog (v5/iter-3 entry, `feedback-decision-log-convention-design.md:347`) already added "a Scope boundary naming concurrent top-level sessions/windows and direct human hand-edits as an undefended last-write-wins race," and the git-worktree case's failure signature (silent entry loss with no id gap) is separately named (`FM-002-i7fmea` in rule file line 27 and design doc line 79) with the explicit "SHOULD NOT" operator guidance. DA-001-i8's own proposed remediation option (b) is "add an explicit disclosed-residual clause" — i.e., the finder's own fallback fix concedes this is a wording/disclosure gap on an already-named residual, not a novel blocking mechanism failure. Per this panel's materiality bar, an already-disclosed, SHOULD-NOT-do, compound edge case does not genuinely block "no lost feedback" for the convention's validated single-operator scope.

---

## DA-002-i8

**Claim:** FM-001's inline-doc dedup check keys purely on `source: inline-doc` `path:line/anchor` location, not content — so an operator's in-place edit to a marker at the same location is silently treated as an already-logged duplicate and the updated feedback is never captured.

**Verification of quotes:** confirmed accurate across all three cited artifacts:
- `feedback-decision-logs-standards.md:51` — "Before minting, check for an existing entry carrying the same `source: inline-doc` `path:line/anchor` — if one exists, do not re-mint (skip, or note the re-encounter on the existing entry)..."
- `FEEDBACK-LOG.template.md:25` — "Before minting, it checks for an existing entry with the same `source: inline-doc` path/anchor and does not re-capture a marker already logged (FM-001 — no doc is mutated)."
- `examples-appendix.md:169` — "The assistant checks for an existing entry carrying the same `source: inline-doc` path/anchor before minting; a marker already logged is not re-captured (FM-001)."

All three state the dedup key as location-only; none specifies a content comparison as a condition for skipping.

**VERIFIED (materiality).** This is a genuine mechanism-level gap, not an improbable edge case or a restatement of an already-disclosed residual:

1. **Distinct from the disclosed "Coverage caveat."** Design doc's inline-doc coverage caveat (`feedback-decision-log-convention-design.md:91`) discloses only two miss modes — the file is never revisited, or it is read via a partial/offset Read — and explicitly claims the opposite failure direction is safe: "the capture-trigger heuristics can also *over*-capture ... a false positive costs one reviewable entry, never a lost one." FM-001's location-only dedup is a case where the document *is* revisited and read in full, yet the mechanism itself — not an omission of coverage — silently drops a legitimate update. This falsifies the design's own "never a lost one" framing for this specific mechanism and is not the same gap already disclosed at line 91.
2. **Not an improbable edge case.** Editing a single-line inline marker in place (revising wording without adding/removing surrounding lines) is an ordinary, low-friction editing action for a one-line annotation — the same "lightweight pointer for short annotations" the design itself designed the marker to be (`feedback-decision-logs-standards.md:51`). It requires no unusual multi-session, multi-writer, or framework-feature combination — only a normal single-operator revising their own annotation, which this very design package's iterative multi-round revision history demonstrates is a routine occurrence.
3. **Confirmed as a regression, not a re-litigated closed item.** The Revision Changelog v8/iter-6 entry (`feedback-decision-log-convention-design.md:350`) shows FM-001 was introduced in iteration-006 specifically to close a *different* prior finding ("no dedup for repeated inline-doc marker harvest"); `iteration-007/restore-notes.md` row 5 confirms this closure was re-verified but only against the *original* finding text, not against new interactions the fix itself introduced. Nothing in the design doc, rule file, templates, or `iteration-007/restore-notes.md` Residuals Disclosed table names "an edited marker at the same location is dropped" as an accepted residual.
4. **Directly threatens the "no lost feedback" purpose pillar** — the option to "note the re-encounter" is optional phrasing ("skip, **or** note the re-encounter"), not a mandated content check, so the literal, simpler reading (skip) is a valid compliant implementation that silently discards the edited text.

---

## Verdict Summary

| ID | Verdict | Basis |
|----|---------|-------|
| DA-001-i8 | REFUTED | Invariant is scoped to the single-writer rotation path, not the disclosed multi-writer/worktree residual; compound low-probability edge case already substantively disclosed with explicit SHOULD-NOT operator guidance (design doc `:79`, rule file `:27`, changelog `:347`). |
| DA-002-i8 | VERIFIED | Genuine, common-path (not edge-case) mechanism-level under-capture: location-only dedup silently drops an edited marker's updated content, contradicting the design's own "over-capture, never lost" claim, and is not covered by the existing Coverage caveat or any disclosed residual (design doc `:91`, rule file `:51`, template `:25`, appendix `:169`). |
