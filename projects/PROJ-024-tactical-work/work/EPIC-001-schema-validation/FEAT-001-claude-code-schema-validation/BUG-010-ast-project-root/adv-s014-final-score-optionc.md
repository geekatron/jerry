# Quality Score Report: BUG-010 Option C — `jerry ast` Containment Redesign (FINAL Gate Score)

## L0 Executive Summary

**Score:** 0.928/1.00 | **Verdict:** PASS | **Weakest Dimension:** Traceability (0.88)
**One-line assessment:** All three doc/consistency blockers from the prior 0.909 REVISE score are
verified fixed in the repository (correct `CHANGELOG.md` entry replacing the two stale/superseded
entries, `RESUME-HERE.md` no longer describes the tournament fixes as uncommitted, and the write-time
containment error now carries the same remediation hint as the read-time error with a dedicated
regression test) — the deliverable now clears the 0.92 quality gate (H-13), with only minor,
non-blocking documentation-bookkeeping residue remaining (tracked below, none security- or
design-relevant).

---

## Scoring Context

- **Deliverable:** Option C `jerry ast` containment redesign — `src/interface/cli/containment_policy.py`,
  `project_root.py`, `ast_commands.py`, `parser.py`, `main.py`, `adapter.py` + test suite, at commit
  `e00ed1c4` (per task framing; this scorer has no Bash/git tool access to independently confirm the
  hash exists in git history — see Traceability)
- **Deliverable Type:** Code (security-relevant CLI containment control)
- **Criticality Level:** C4 (final gate re-score closing a C4 adversarial cycle; AE-005 security-relevant)
- **Scoring Strategy:** S-014 (LLM-as-Judge), standalone final gate re-score
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-08-12
- **Method:** Targeted re-verification of the three specific items named in the prior 0.909 REVISE
  report (`adv-s014-tournament-score-optionc.md`), read directly against the current repository state
  (not the task's claims alone), plus a fresh sweep for any *new* inconsistency introduced by the
  closure work itself. The broader methodology/evidence/design verification performed in the prior
  scoring pass (hexagonal purity, TDD, structural TOCTOU fix, 9-strategy tournament, eng-reviewer gate)
  is not re-litigated here since none of the closure changes touch that surface; those two dimensions
  carry forward unchanged from the prior score with a one-line confirmation of continued validity.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.928 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | **PASS** |
| **Strategy Findings Incorporated** | Yes — prior S-014 re-score (0.909 REVISE), eng-reviewer gate report (0.955), `adv-tournament-consolidated-optionc.md`, direct source/doc verification of the three closure items |
| **Prior Score** | 0.909 REVISE (`adv-s014-tournament-score-optionc.md`, 2026-08-12) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-------------------|
| Completeness | 0.20 | 0.92 | 0.184 | Changelog AC substantively satisfied (real entry exists); one Minor tournament item (RT-004/RT-005 disposition) and one entity checkbox remain un-ticked |
| Internal Consistency | 0.20 | 0.90 | 0.180 | All 3 prior contradictions (IC-1/IC-2/IC-3) verified fixed; new minor lag found in the BUG-010 entity's own AC checkbox/History |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Unchanged from prior score — closure work does not touch design/process; carried forward |
| Evidence Quality | 0.15 | 0.95 | 0.1425 | Unchanged from prior score, reinforced by one new, well-documented regression test for the write-time hint |
| Actionability | 0.15 | 0.94 | 0.141 | 3 of 4 prior recommendations closed with verified evidence (incl. a new test); 1 (RT-004/RT-005 disposition) still open |
| Traceability | 0.10 | 0.88 | 0.088 | TR-2 (changelog forward-trace) resolved; TR-1 pattern (final commit hash unverifiable in-repo) recurs for `e00ed1c4` even though the prior hash `a6240a4d` is now corroborated |
| **TOTAL** | **1.00** | | **0.928** | |

---

## Detailed Dimension Analysis

### Completeness (0.92/1.00)

**Evidence:**
- BUG-010's AC "changelog entry" (bundled into the AC line at
  `BUG-010-ast-project-root.md:115-116`) is now substantively satisfied:
  `CHANGELOG.md:16` (`### Security`) contains a complete, accurate entry titled
  `**BUG-010 (Option C — user-declared trusted roots):**` describing the shipped model precisely
  (default = project root + `ast.trusted_roots`, no OS temp auto-trust, `--root` override, `--quiet`,
  broad-root warning, config-input hygiene, and explicitly states the interim temp-auto-trust +
  ownership-gate approach "was removed").
- Write-time containment-escape message now carries `_CONTAINMENT_ESCAPE_HINT`
  (`ast_commands.py:630-633`), matching the read-time messages at `:245` and `:256` exactly (verified
  identical hint text `"configure ast.trusted_roots or pass --root"` used in both).
- A dedicated regression test exists:
  `test_ast_modify_when_write_time_escape_rejected_then_error_includes_containment_hint`
  (`tests/unit/interface/cli/test_ast_commands.py:1645-1693`), Windows-guarded via
  `@pytest.mark.skipif(sys.platform == "win32", ...)` matching the pattern used by the sibling A-1
  regression test, asserting `ast_commands_module._CONTAINMENT_ESCAPE_HINT in captured.out`.

**Gaps:**
- The AC line itself (`BUG-010-ast-project-root.md:115-116`, bundling test-suite-green + coverage +
  "changelog entry") remains unchecked (`- [ ]`) despite the changelog portion now being satisfied — a
  bookkeeping lag, not a functional gap.
- S-001's RT-004 (double config-layer read per `ast_modify` invocation) and RT-005 (`--quiet`
  suppressible by the JSON-pipeline audience) are still **not** explicitly dispositioned in
  `adv-tournament-consolidated-optionc.md` — confirmed by a targeted search (`RT-004`/`RT-005`: no
  matches in that file). This is the fourth (lowest-priority) item from the prior report's
  recommendations and was not in the set of three the task asked to verify; it remains open,
  unchanged from the prior score, and unlike the three verified items, was not addressed in this pass.

**Improvement Path:** Check the "changelog entry" AC box now that the entry exists. Add one-line
Disposition D/E entries for RT-004/RT-005 to `adv-tournament-consolidated-optionc.md` (still the
lowest-cost, lowest-risk item remaining across both scoring passes).

### Internal Consistency (0.90/1.00)

**Evidence — all three prior findings verified fixed:**
- **IC-1 (CHANGELOG, previously moderate) — RESOLVED.** Searched `CHANGELOG.md` for the two specific
  stale phrases previously flagged (`st_uid`/`geteuid` ownership-gate language, "widened... to include
  OS temp/scratchpad directories") — zero matches. The only Security-section entry referencing BUG-010
  is the new, accurate Option C entry at `CHANGELOG.md:16`, which explicitly states the superseded
  approach "was removed," consistent with `DECISIONS-and-threat-model.md` DD-2 ("Remove entirely" —
  verified same file, line 21) and the BUG-010 entity's own 2026-08-11 History entry.
- **IC-2 (RESUME-HERE.md, previously minor) — RESOLVED for the specific defect cited.**
  `RESUME-HERE.md`'s commit table (lines 11-19) now lists `a6240a4d` as a completed commit row
  ("Tournament fixes A-1..A-7 ... governance reconciliation, and the full tournament record") with no
  "(uncommitted)" or "Next checkpoint" language attached to it — the specific false claim previously
  flagged is gone. "Next actions" item 1 (line 37) now reads "Done — tournament fixes + governance
  committed at `a6240a4d`."
- **IC-3 (write-time hint, previously minor) — RESOLVED.** Confirmed under Completeness above; the
  write-time and read-time messages now use byte-identical hint text.

**New gap found (minor, doc-bookkeeping class, not previously flagged):**
- The BUG-010 entity (`BUG-010-ast-project-root.md`) has no History row dated 2026-08-12 documenting
  the closure of the three items or the final commit hash — its most recent History entry (line 140)
  is still dated 2026-08-11 and predates this closure pass. Combined with the unchecked "changelog
  entry" AC box (see Completeness), the entity's own tracking artifact has not been synchronized with
  the state this scoring task asserts. This is the same *class* of defect as the original IC-1/IC-2
  (a governance artifact lagging the shipped/closed state) but meaningfully lower severity: it does not
  assert anything actively false (unlike the original CHANGELOG entries, which described a removed
  security mechanism as if still active) — it is simply silent/stale on the closure, not contradictory.
- `RESUME-HERE.md`'s own commit table (line 19) still shows `*(this pass)*` with no commit hash for
  the CHANGELOG/RESUME-HERE/write-time-hint closure work itself, and "Next actions" item 2 (line 38)
  still frames the S-014 gate as "In progress" — which is literally accurate at the moment this scoring
  run executes, but means the document has not yet been updated to reflect that its own described
  fixes are complete and verified. This is an inherent bootstrapping characteristic of a resume pointer
  (it cannot self-document a commit hash that includes its own most recent edit) rather than a
  fabricated claim, and is judged lower-severity than the original defect.

**Improvement Path:** Add a 2026-08-12 History row to `BUG-010-ast-project-root.md` naming the closure
commit and this score. Update `RESUME-HERE.md`'s commit table with the actual final commit hash once
this scoring pass's own persistence is committed, and change "Next actions" item 2 from "In progress"
to reflect the PASS verdict.

### Methodological Rigor (0.96/1.00) — carried forward, unchanged

**Confirmation:** None of the three closure items touch design, architecture, or process — they are
documentation and one string-literal parity fix with a matching test. The hexagonal purity
(`containment_policy.py` remains stdlib-only), TDD discipline, structural (not patch) fix for the
write-path TOCTOU, and the 9-strategy blind tournament + eng-reviewer gate verified in the prior
scoring pass are unaffected by this closure work. No re-verification finding changes this score;
carried forward at 0.96 per the prior report's detailed evidence.

### Evidence Quality (0.95/1.00) — carried forward, reinforced

**Confirmation:** The prior evidence base (real behavioral PoCs, honest coverage reconciliation,
disclosed Windows-validation limitation) is unaffected by this closure. One new, small, well-formed
piece of evidence was added and verified in this pass: the write-time hint regression test uses the
same symlink-swap harness pattern as the A-1 regression test, is correctly Windows-guarded, and
directly asserts the exact string it claims to verify. This reinforces rather than changes the prior
0.95 assessment; not raised further since it is a small addition, not a step-change in evidence rigor.

### Actionability (0.94/1.00)

**Evidence:** Three of the prior report's four numbered recommendations are closed with concrete,
verifiable evidence: (1) CHANGELOG replacement — done, verified above; (2) RESUME-HERE.md commit-table
update — done for the specific defect cited (a6240a4d no longer "uncommitted"); (3) write-time hint +
regression test — done, verified above with exact file:line and test name. This is a precise,
traceable follow-through from a specific prior report's numbered action items to concrete commits/diffs
— the strongest form of actionability evidence (recommendation → verified fix, not just a claim of
having addressed it).

**Gaps:** Recommendation 4 (RT-004/RT-005 explicit disposition) remains open and untracked anywhere,
identical to the prior pass. The two new minor gaps found in this pass (entity History/AC lag,
RESUME-HERE.md self-referential commit-hash gap) are not yet tracked as follow-ups anywhere — this
report now serves that function, consistent with how the prior report's own findings were handled.

**Improvement Path:** Close recommendation 4. Add the entity History row and RESUME-HERE.md final-hash
update identified above (both < 5 minutes of doc editing, zero code changes, zero re-scoring risk).

### Traceability (0.88/1.00)

**Evidence:** TR-2 (CHANGELOG breaking the forward trace from "fixed in code" to "documented for
release") is resolved — `CHANGELOG.md:16` now closes that chain. TR-1's originally-cited commit
`a6240a4d` is now corroborated within the repository's own bookkeeping (`RESUME-HERE.md`'s commit
table), which is a genuine improvement over the prior pass where no artifact referenced it at all.

**Gaps:** The underlying TR-1 *pattern* recurs one commit later: this task's asserted final commit,
`e00ed1c4`, is not referenced by any in-repo artifact read for this score (`RESUME-HERE.md`'s commit
table ends at `a6240a4d` plus an un-hashed `*(this pass)*` row; the BUG-010 entity's History ends at
2026-08-11). This scorer has no Bash/git tool access to independently confirm `e00ed1c4` exists, is
descended from `a6240a4d`, or is the actual branch `HEAD` — identical tooling limitation to the prior
pass. The source-level verification performed in this report (which does independently confirm the
CHANGELOG content, the RESUME-HERE.md wording, and the write-time hint/test are present in the
currently-readable working tree) remains the strongest available substitute evidence, but is not
equivalent to a corroborated commit-hash chain for the specific commit named in this task.

**Improvement Path:** Once this score report is persisted and committed, add its own commit hash to
`RESUME-HERE.md`'s commit table and to a new History row in the BUG-010 entity, finally closing the
loop between "claimed final commit" and "artifact-corroborated final commit" that has now recurred
across two consecutive scoring passes.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|-----------------|
| 1 | Traceability | 0.88 | 0.95+ | Add the commit hash that includes this closure (and this score report) to `RESUME-HERE.md`'s commit table and to a new BUG-010 entity History row, replacing the un-hashed `*(this pass)*` placeholder. |
| 2 | Internal Consistency / Completeness | 0.90 / 0.92 | 0.95+ / 0.95+ | Add a 2026-08-12 History row to `BUG-010-ast-project-root.md` documenting the three-item closure; check the "changelog entry" AC box. |
| 3 | Actionability / Completeness | 0.94 / 0.92 | 0.96+ / 0.95+ | Add one-line explicit Disposition D/E entries for S-001's RT-004 and RT-005 to `adv-tournament-consolidated-optionc.md` (carried over unaddressed from the prior score). |
| 4 | Internal Consistency | 0.90 | 0.93+ | Update `RESUME-HERE.md`'s "Next actions" item 2 from "In progress" to reflect the PASS verdict once this report is persisted. |

None of the four remaining items are blocking (none is a functional, security, or design defect; all
are documentation/bookkeeping polish below the threshold that would force a REVISE). They are listed
for completeness and future closure, not as gate conditions.

---

## Leniency Bias Check

- [x] Each dimension scored independently — Internal Consistency, Completeness, Actionability, and
      Traceability were each re-derived from direct evidence of what changed (or didn't) since the
      prior pass, not inherited wholesale from the prior 0.909 figure or from the task's framing that
      "all three are closed."
- [x] Evidence documented for each score — every score cites specific file:line, test-name, or
      grep-verified-absence evidence; the "confirm, don't assume" instruction in the task was followed
      by independently re-reading `CHANGELOG.md`, `RESUME-HERE.md`, `ast_commands.py`, and the new
      test, rather than accepting the task's summary at face value.
- [x] Uncertain scores resolved downward — where a dimension could plausibly be scored higher (e.g.,
      Internal Consistency at 0.91-0.92 given three verified fixes) it was held to the more
      conservative figure (0.90) because a new, real (if minor) inconsistency was found in the same
      pass (entity History/AC lag) that a less careful review would have missed entirely; Traceability
      was similarly held at 0.88 rather than 0.90+ because the TR-1 gap pattern was found to recur for
      the newly-claimed commit hash rather than being fully closed.
- [x] First-draft calibration considered — N/A; this is the same mature, heavily-reviewed C4 artifact
      as the prior pass, scored against the corresponding high bar.
- [x] No dimension scored above 0.95 without exceptional documented evidence — Methodological Rigor
      (0.96) is carried forward unchanged from a pass that documented concrete, checkable evidence for
      it (structural TOCTOU fix, 9-strategy tournament); it was not re-raised in this pass despite the
      overall composite crossing threshold, since the closure work did not add new evidence to that
      specific dimension.
- [x] Composite crossing 0.92 was checked against the "Critical findings" override — the one prior
      CRITICAL (A-1/RT-001, write-path TOCTOU) remains confirmed fixed in code (re-verified at
      `ast_commands.py:627-636`: `target_path = resolved` derives directly from the write-time
      `_check_path_containment` call, unchanged from the prior pass's verification); no new Critical or
      High finding was discovered in this pass. The PASS verdict is therefore not blocked by the
      special-case override in the scoring process.

---

## Session Context (adv-scorer → orchestrator)

```yaml
verdict: PASS
composite_score: 0.928
threshold: 0.92
weakest_dimension: traceability
weakest_score: 0.88
critical_findings_count: 0  # A-1/RT-001 confirmed fixed in code, re-verified this pass
iteration: 2  # second S-014 final-gate scoring pass (prior: 0.909 REVISE)
improvement_recommendations:
  - "Add the closure commit hash to RESUME-HERE.md's commit table and a new BUG-010 entity History row (replaces the un-hashed '(this pass)' placeholder)"
  - "Add a 2026-08-12 History row to BUG-010-ast-project-root.md documenting the three-item closure; check the 'changelog entry' AC box"
  - "Add explicit Disposition D/E entries for S-001's RT-004 and RT-005 in adv-tournament-consolidated-optionc.md (carried over from prior score, still open)"
  - "Update RESUME-HERE.md's 'Next actions' item 2 from 'In progress' to reflect the PASS verdict"
```

---

*adv-scorer S-014 final gate score. No source, test, or worktracker file was modified by this scoring
pass — findings are reported for closure, not unilaterally applied (P-020). Persisted per P-002 at
`projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/adv-s014-final-score-optionc.md`.*
