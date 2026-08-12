# Audit Report: BUG-010 (Option C) and Parent Chain

> **Type:** audit-report
> **Generated:** 2026-08-12T00:00:00Z
> **Agent:** wt-auditor
> **Audit Type:** full (template compliance, relationships, orphans, status, ID format) + WTI-001..009
> **Scope:** `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/BUG-010-ast-project-root.md` and parent chain (FEAT-001, EPIC-001), `WORKTRACKER.md`, `CHANGELOG.md`, `RESUME-HERE.md`

---

## Summary

| Metric | Value |
|--------|-------|
| **Files Checked** | 8 (BUG-010 entity, FEAT-001 entity, EPIC-001 entity, WORKTRACKER.md, CHANGELOG.md, RESUME-HERE.md, adv-s014-final-score-optionc.md, adv-tournament-consolidated-optionc.md) |
| **Coverage** | 100% of stated scope |
| **Total Issues** | 8 |
| **Errors** | 0 |
| **Warnings** | 5 |
| **Info** | 3 |
| **Verdict** | PASSED (schema/structure) — TIDY-UP REQUIRED (governance-artifact lag) before merge |

**Bottom line:** No structural/schema errors. The code and evidence are genuinely done (C4 tournament PASS, S-014 0.928, 90%+ coverage, green suite). The gap is entirely in the worktracker/governance artifacts lagging the shipped state — the pattern the deliverable's own final S-014 score report (0.928 PASS) explicitly flagged and left open for the "main context" to close. This is a P-002/WTI-001 truthful-state gap, not a functional one.

---

## Issues Found

### Warnings

| ID | File | Issue | Remediation |
|----|------|-------|--------------|
| W-001 | `BUG-010-ast-project-root.md` (Acceptance Criteria, lines 88-117) | 12 of 14 active (non-superseded) AC checkboxes remain `- [ ]` despite verified completion evidence (History, eng-reviewer PASS 0.955, tournament PASS 0.928, `git log`). Only 2 of 14 are ticked. This is a WTI-003 (truthful state) violation — the entity understates its own completion. | Tick each of the 12 items below (see checklist). Leave the 2 struck-through "SUPERSEDED"/"REMOVED" lines (currently `- [ ]`) as-is — they are intentionally unticked N/A markers for a discarded design, not open work. |
| W-002 | `BUG-010-ast-project-root.md` (History) | No History row dated 2026-08-12 for the closure. Most recent row is 2026-08-11; it does not mention the second S-014 pass (0.909 REVISE → fixes → 0.928 PASS) or commits `a6240a4d`/`e00ed1c4`. Flagged by the deliverable's own final score report (Traceability 0.88, Internal Consistency 0.90) as the recurring gap across two scoring passes. | Add a 2026-08-12 History row: tournament final re-score PASS 0.928 (`adv-s014-final-score-optionc.md`), closure commits `a6240a4d` (tournament fixes A-1..A-7 + governance reconciliation) and `e00ed1c4` (S-014 gap closure: changelog, RESUME-HERE.md, write-time hint + regression test). State PR #341 is open, pending merge — status remains `in_progress` per the close-only-after-merge convention. |
| W-003 | `FEAT-001-claude-code-schema-validation.md` (Children Stories/Enablers, Work Item Links, Progress Summary/Metrics) | BUG-010 is entirely absent from its own parent's tracking artifacts. `Children Stories/Enablers` inventory table (lines 116-154), `Work Item Links` (156-194), `Progress Summary` bar chart and `Progress Metrics` table (198-228) all predate BUG-010's creation (2026-08-07) and were never updated — Bugs still show "7/7 100%" and Overall "97% (34/35)" with no reference to BUG-010 at all. This is a WTI-004/005 relationship-integrity gap: the child correctly declares `Parent: FEAT-001`, but the parent does not declare the child. | Add a BUG-010 row to the `Story/Enabler Inventory` table (status `in_progress`, priority `high`), add the corresponding entry to `Work Item Links`, update `Progress Summary`/`Progress Metrics` to reflect 8 bugs total / 7 completed / 1 in_progress, and recompute the Overall bar (35/36, not 34/35). |
| W-004 | `FEAT-001-claude-code-schema-validation.md` (History) | Last History row is 2026-03-30 and gives EN-004 as the sole reason FEAT-001 remains `in_progress`. It is silent on BUG-010, so a reader cannot tell why the feature is still open beyond EN-004. Not factually wrong (status is correctly `in_progress`), but incomplete. | Add a History row (2026-08-1x) noting BUG-010 was opened (#337, 2026-08-07) and is in flight on `fix/BUG-010-ast-project-root` / PR #341, pending merge; FEAT-001 remains `in_progress` for both EN-004 and BUG-010. |
| W-005 | `CHANGELOG.md` `[Unreleased]` | BUG-010 has two separate entries in the same `[Unreleased]` section: `### Security` (line 16, current — full Option C description) and `### Fixed` (line 27, stale — describes only the original `CLAUDE_PROJECT_DIR`/cwd base-fix framing from before the Option C redesign, with no mention of the redesign, the tournament, or `ast.trusted_roots`). A reader scanning the changelog sees BUG-010 twice with inconsistent scope. | Remove/fold the `### Fixed` entry (line 27) into the `### Security` entry (line 16), since the Security entry is the accurate, complete, current description. Keep only one BUG-010 entry in `[Unreleased]`. |

### Info

| ID | File | Issue | Remediation |
|----|------|-------|--------------|
| I-001 | `RESUME-HERE.md` | "Next actions" item 2 (line 38) still reads "In progress — final S-014 gate... 0.909 REVISE..." even though the final re-score (`adv-s014-final-score-optionc.md`) now shows **PASS 0.928**. Commit table (line 19) still shows an un-hashed `*(this pass)*` placeholder for the `e00ed1c4` closure commit, and there is no row at all for the still-uncommitted final-score report itself. | Update item 2 to reflect PASS 0.928 and move to "On PASS: PR #341 review + merge" as the sole remaining action. Replace the `*(this pass)*` placeholder with `e00ed1c4`. Add a new commit-table row once the tidy-up commit (History row, AC ticks, changelog fold, this audit report) lands, so the resume pointer is fully self-consistent. |
| I-002 | `adv-s014-final-score-optionc.md` | This file (the PASS 0.928 final gate score, dated 2026-08-12) is **untracked in git** (`git status` shows `??`) — it exists on disk but was never committed. Per P-002, agent deliverables that gate a merge decision should be persisted to the branch, not left as an uncommitted working-tree file. | `git add` and commit this file alongside the other tidy-up changes (or in its own governance commit) before opening PR #341 for review/merge. |
| I-003 | `adv-tournament-consolidated-optionc.md` | S-001's RT-004 (double config-layer read per `ast_modify` invocation) and RT-005 (`--quiet` suppressible by JSON-pipeline audience) have no explicit Disposition D/E entry — flagged as open by both the 0.909 and 0.928 score reports (lowest-priority, non-blocking). | Optional, non-blocking: add one-line Disposition D or E entries for RT-004/RT-005 for completeness. Does not block merge. |

---

## Detail: WTI Checklist Findings

1. **AC truthfulness (WTI-003/006):** See W-001. The tournament/score chain (`adv-s014-tournament-score-optionc.md` 0.909 REVISE → `adv-s014-final-score-optionc.md` 0.928 PASS) explicitly confirms the "changelog entry" clause of the bundled test/coverage/changelog AC line is now satisfied, and independently the branch's own History (lines 137-140) plus `eng-reviewer-optionc-gate-report.md` (297 tests passing, 100% coverage on new modules, ~97% on changed lines, H-20 RED-first "evident") substantiate every other active AC. None of the 12 flagged boxes have any documented counter-evidence.
2. **History completeness (WTI-001):** Confirmed missing — see W-002. No entry post-dates 2026-08-11; the 2026-08-12 tournament PASS and its two commits (`a6240a4d` git-confirmed via `git log`; `e00ed1c4` git-confirmed, HEAD of `fix/BUG-010-ast-project-root`) are undocumented in the entity itself.
3. **Manifest consistency (WTI-004/005):**
   - `WORKTRACKER.md` row 16 for BUG-010: `in_progress`, parent `FEAT-001` — **matches** entity status and parent. Correct, no drift.
   - `WORKTRACKER.md` rows 17-18 for EPIC-001/FEAT-001: both `in_progress` — **matches** entity status. Correct.
   - FEAT-001 entity: does **not** list BUG-010 as a child anywhere (Children table, Work Item Links, Progress Summary/Metrics) — see W-003/W-004. This is the one real orphan-adjacent gap: BUG-010 is reachable from `WORKTRACKER.md` and declares its parent correctly, but the parent-side backlink is absent, so a reader starting from FEAT-001 alone would not discover BUG-010 exists.
   - EPIC-001 entity: unaffected (BUG-010 is a grandchild via FEAT-001, not a direct EPIC-001 child); EPIC-001's own Progress Summary (`0/1 features, 10%`) is stale relative to FEAT-001's real 97% completion, but this predates BUG-010 and is a pre-existing, separate staleness issue outside this audit's remediation scope — noted for awareness only, not itemized in the checklist below.
4. **Schema/structure:** `jerry ast validate --schema bug` on `BUG-010-ast-project-root.md` returns `is_valid: true`, `schema_valid: true`, `nav_table_valid: true`, `violation_count: 0`. No structural defects.
5. **Parent rollup:** FEAT-001's `in_progress` status is correct (BUG-010 is genuinely open pending merge), but the rollup artifacts don't currently *say why* beyond EN-004 — addressed by W-003/W-004.
6. **Other:** W-005 (duplicate/stale CHANGELOG entry), I-001 (RESUME-HERE.md self-reference lag — an acknowledged, low-severity bootstrapping artifact per the score report), I-002 (uncommitted score report), I-003 (optional tournament disposition entries).

---

## Actionable Tidy-Up Checklist

> Ordered by file. Apply all WARNING items before merge; INFO items are recommended but non-blocking (I-003 is fully optional).

**1. `BUG-010-ast-project-root.md` — Acceptance Criteria (W-001):** tick these 12 lines (leave the 2 struck-through SUPERSEDED/REMOVED lines at `- [ ]`, and leave the 2 already-`[x]` lines unchanged):
- [ ] → [x] "Failing tests written first (H-20 Red)" (line 88)
- [ ] → [x] "`jerry ast` commands accept files within the user's project root..." (line 89-91)
- [ ] → [x] "Root resolution logic exists once (shared `project_root.py` helper)..." (line 92-93)
- [ ] → [x] "Default allowed roots = the project root plus explicitly-configured `ast.trusted_roots`..." (line 94-96)
- [ ] → [x] "`ast.trusted_roots` read via layered config..." (line 97-101)
- [ ] → [x] "`--root <path>` on all 10 `jerry ast` subcommands makes containment exclusive..." (line 102-104)
- [ ] → [x] "`--quiet` on all 10 subcommands suppresses stderr advisory notes..." (line 105-106)
- [ ] → [x] "M-08/M-10 containment + symlink-escape preserved... write-path TOCTOU closed (CWE-367)" (line 107-109)
- [ ] → [x] "Broad root... prints a one-line stderr WARNING..." (line 110-112)
- [ ] → [x] "A match via a configured (non-project) trusted root prints a one-line stderr transparency note..." (line 113-114)
- [ ] → [x] "`TestA07PathTraversal` green; full suite green with >= 90% coverage (H-21); changelog entry" (line 115-116)
- [ ] → [x] "C4 adversarial tournament re-score >= 0.92" (line 117)

**2. `BUG-010-ast-project-root.md` — History (W-002):** add a row:
```
| 2026-08-12 | in_progress | Final S-014 gate closure: three doc/consistency gaps from the 0.909 REVISE pass (CHANGELOG Option C entry, RESUME-HERE.md stale note, write-time containment-escape hint parity) fixed test-first at `e00ed1c4`. Re-scored PASS at 0.928 (`adv-s014-final-score-optionc.md`), closing the C4 gate opened at `a6240a4d`. Status remains in_progress pending PR #341 merge to main (Closes #337 on merge). |
```

**3. `FEAT-001-claude-code-schema-validation.md` (W-003, W-004):**
- Add a row to the `Story/Enabler Inventory` table: `| BUG-010 | Bug | jerry ast rejects files outside plugin install tree (#337) | in_progress | high | — |`
- Add a `Work Item Links` entry: `- [BUG-010: jerry ast rejects files outside plugin install tree](./BUG-010-ast-project-root/BUG-010-ast-project-root.md)`
- Update `Progress Summary`/`Progress Metrics`: Bugs 7/8 (was 7/7), Overall 35/36 (was 34/35), recompute the percentage bar.
- Add a History row noting BUG-010 (opened 2026-08-07, #337) as the reason FEAT-001 remains `in_progress` alongside EN-004.

**4. `CHANGELOG.md` (W-005):** remove or fold the stale `### Fixed` BUG-010 entry (line 27, pre-Option-C framing) into the accurate `### Security` entry (line 16); keep exactly one BUG-010 entry in `[Unreleased]`.

**5. `RESUME-HERE.md` (I-001):** update "Next actions" item 2 from "In progress... 0.909 REVISE" to reflect PASS 0.928, and replace the un-hashed `*(this pass)*` commit-table row with `e00ed1c4`.

**6. `adv-s014-final-score-optionc.md` (I-002):** `git add` and commit this file — it is currently untracked and gates the merge decision.

**7. (Optional, non-blocking) `adv-tournament-consolidated-optionc.md` (I-003):** add one-line Disposition D/E entries for RT-004 and RT-005.

**Not required:** `WORKTRACKER.md` rows for BUG-010/FEAT-001/EPIC-001 (already consistent); `BUG-010` schema/nav-table (already valid); EPIC-001 entity (BUG-010 is a grandchild, no direct reference needed — its separate progress-summary staleness is out of scope for this audit).

---

## Files Audited

- `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/BUG-010-ast-project-root.md`
- `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/FEAT-001-claude-code-schema-validation.md`
- `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/EPIC-001-schema-validation.md`
- `projects/PROJ-024-tactical-work/WORKTRACKER.md`
- `CHANGELOG.md`
- `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/RESUME-HERE.md`
- `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/adv-s014-final-score-optionc.md`
- `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/adv-tournament-consolidated-optionc.md`
- `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/eng-reviewer-optionc-gate-report.md` (cross-reference for coverage/H-20 evidence)

(total: 9 files; `jerry ast validate --schema bug` used per H-33 for the entity schema check.)
