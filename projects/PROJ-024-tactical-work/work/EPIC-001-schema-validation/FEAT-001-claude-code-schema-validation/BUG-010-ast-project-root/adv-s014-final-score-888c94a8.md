# Quality Score Report: BUG-010 Option C — `jerry ast` Containment Redesign (FINAL Gate Score @ `888c94a8`)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, one-line assessment |
| [Scoring Context](#scoring-context) | Deliverable, criticality, method |
| [Score Summary](#score-summary) | Composite and threshold |
| [Dimension Scores](#dimension-scores) | Weighted table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence and gaps |
| [Improvement Recommendations](#improvement-recommendations-priority-ordered) | Priority-ordered follow-ups |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency self-audit |
| [Session Context](#session-context-adv-scorer--orchestrator) | Machine-readable handoff |

---

## L0 Executive Summary

**Score:** 0.9335/1.00 (reported as 0.934) | **Verdict:** PASS | **Weakest Dimension:** Traceability (0.91)

**One-line assessment:** Both gaps that held the prior pass to 0.9165 REVISE are verified fixed in the
repository — `main.py`'s `_handle_ast` router now routes both diagnostics to stderr with two new,
correctly-written regression tests, and every governance artifact that previously described GH #371 as
deferred/out-of-scope now says "Fixed in this unit" — clearing the 0.92 gate with margin, though a
persistent (now 4-scoring-pass-old) pattern of un-actioned commit-hash bookkeeping keeps this from scoring
higher.

---

## Scoring Context

- **Deliverable:** Option C `jerry ast` containment redesign + GH #371 stdout->stderr completion —
  `src/interface/cli/ast_commands.py`, `main.py`, `parser.py`, `project_root.py`, `containment_policy.py`,
  `adapter.py` + test suite, at commit `888c94a85b21fd9899d2dc08e570c0eb4743da09` (commit message: `fix(cli):
  finish #371 stderr routing across the ast router + reconcile docs (BUG-010)`), verified as the exact
  worktree HEAD via `.git`/`gitdir:` → `/Users/.../jerry/.git/worktrees/proj-024-tactical-work-6/logs/HEAD`
- **Deliverable Type:** Code (security-relevant CLI containment control) + governance/worktracker artifacts
- **Criticality Level:** C4 (final gate re-score closing a C4 adversarial cycle; AE-005 security-relevant)
- **Scoring Strategy:** S-014 (LLM-as-Judge), standalone final gate re-score, fourth pass in this lineage
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-08-12
- **Prior Score:** 0.9165 REVISE (`adv-s014-final-score-18ce85de.md`, scored against `18ce85de`, 0.0035
  below threshold on exactly the two gaps this pass re-verifies)
- **Method:** Direct re-verification of both cited gaps against the current repository state, not the
  task's claims alone: read `main.py:393-462` (`_handle_ast`) in full, re-scanned all 20 `print(` sites in
  `ast_commands.py` for stream correctness, read the new `TestMainAstRouting` tests (lines 1070-1198 of
  `tests/unit/interface/cli/test_ast_commands.py`), read `RESUME-HERE.md`, `DECISIONS-and-threat-model.md`,
  `adv-tournament-consolidated-optionc.md`, `CHANGELOG.md`, the BUG-010 and FEAT-001 entities, and
  `wt-audit-optionc.md` in full, plus a fresh grep sweep for `888c94a8`/`18ce85de` across the BUG-010
  folder and for `371` across the governance artifacts to catch any *new* inconsistency the closure work
  itself might have introduced. The git worktree reflog was read directly (Read tool on
  `.git/worktrees/.../logs/HEAD`) to independently corroborate the commit chain and message — this scorer
  has Read but not Bash/git-CLI access. Methodological Rigor and Evidence Quality baselines from the
  original 0.928 PASS pass (hexagonal purity, TDD discipline, structural TOCTOU fix, 9-strategy tournament,
  eng-reviewer 0.955 gate) are reconfirmed unaffected by this closure and are not re-litigated in full
  detail below except where this commit's changes touch them directly.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.9335 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | **PASS** |
| **Strategy Findings Incorporated** | Yes — prior final score (0.9165 REVISE @ `18ce85de`), `wt-audit-optionc.md`, `eng-reviewer-optionc-gate-report.md` (0.955), `adv-tournament-consolidated-optionc.md`, direct source/test/doc/git verification performed in this pass |
| **Critical/High findings this pass** | 0 |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-------------------|
| Completeness | 0.20 | 0.93 | 0.186 | Both cited gaps closed with code + tests; RT-004/RT-005 tournament disposition still open (carried 4 passes, non-blocking) |
| Internal Consistency | 0.20 | 0.93 | 0.186 | Zero remaining artifacts describe #371 as deferred/out-of-scope (verified across 4 files); governance History/commit tables still lag the last 2 commits (silent, not contradictory) |
| Methodological Rigor | 0.20 | 0.95 | 0.190 | Prior pass's identified gap ("sweep was file-scoped, not router-wide") is now closed — this pass's fix covers the full `jerry ast` command-surface, evidenced by both `ast_commands.py` and `main.py` being clean |
| Evidence Quality | 0.15 | 0.95 | 0.1425 | Every claim independently verified against primary sources (source, tests, git reflog); no overstated claims found this pass |
| Actionability | 0.15 | 0.92 | 0.138 | 3 of 3 task-cited items closed with concrete evidence; but RT-004/RT-005 and the commit-hash-row recommendation have now been repeated across 4 consecutive reports without closure |
| Traceability | 0.10 | 0.91 | 0.091 | `888c94a8` independently confirmed as exact HEAD via git reflog (verbatim commit-message match) — the strongest traceability evidence in this lineage — but no in-repo governance doc references it or `18ce85de` by hash, a pattern now unresolved for a 4th consecutive pass |
| **TOTAL** | **1.00** | | **0.9335** | |

---

## Detailed Dimension Analysis

### Completeness (0.93/1.00)

**Evidence — both cited gaps verified closed:**

- **Gap 1 (main.py router stdout leak) — CLOSED.** `src/interface/cli/main.py:428`:
  `print("No ast command specified. Use 'jerry ast --help'.", file=sys.stderr)` — the reachable branch
  (no `required=True` on the `ast` subparsers per `parser.py`) now carries `file=sys.stderr`.
  `main.py:461`: `print(f"Unknown ast command: {args.command}", file=sys.stderr)` — the defensive/dead
  branch is fixed too, for consistency. `sys` is imported at module top (`main.py:39`), so both calls are
  valid.
- `src/interface/cli/ast_commands.py` re-scanned in full (all 20 `print(` sites): every diagnostic
  (lines 301, 308, 314, 453, 604, 630, 658) carries `file=sys.stderr`; every JSON/render payload print
  (lines 348, 374, 446, 492, 535, 562, 680, 716, 763, 810, 857) remains un-redirected (stdout) — confirmed
  unchanged and correct, exactly as the task framing claims.
- Two new tests in `tests/unit/interface/cli/test_ast_commands.py::TestMainAstRouting` (lines 1142-1198)
  directly assert the fix: `test_main_ast_no_command_prints_error_to_stderr_only` (uses `capsys`, asserts
  `captured.out == ""` and `"no ast command specified" in captured.err.lower()`) and
  `test_handle_ast_unknown_command_prints_error_to_stderr_only` (same pattern via `FakeArgs`, asserting
  `captured.out == ""` and `"unknown ast command" in captured.err.lower()`). Both are correctly written —
  RED would have failed against the pre-fix `print()` calls without `file=sys.stderr` since `capsys`
  routes unredirected `print()` to `captured.out`, not `captured.err`.
- `CHANGELOG.md:16` (`### Security`, the single BUG-010 entry in `[Unreleased]`) now closes with: *"All
  `jerry ast` diagnostic/error messages now print to stderr, so stdout carries only the JSON/render
  payload for pipeline consumers (#337, #341, #371)"* — the missing CHANGELOG mention of #371 flagged by
  the prior pass is resolved. No duplicate/stale `### Fixed` BUG-010 entry exists (grepped `CHANGELOG.md`
  for `BUG-010`: one Security entry + one unrelated historical reference from a different numbering
  scheme, line 75).
- BUG-010's bundled AC line (`BUG-010-ast-project-root.md:115-116`, "...changelog entry") is now ticked
  `[x]`; all 12 active (non-superseded) ACs are `[x]`, matching `wt-audit-optionc.md`'s W-001 remediation
  checklist item-for-item.
- FEAT-001 fully synchronized (Story/Enabler Inventory :153, Work Item Links :196, Progress Metrics
  :227, History :258) — the W-003/W-004 gaps from `wt-audit-optionc.md` are closed.

**Gaps (carried forward, non-blocking):**
- S-001's RT-004 (double config-layer read per `ast_modify` invocation) and RT-005 (`--quiet`
  suppressible by the JSON-pipeline audience) remain undispositioned in `adv-tournament-consolidated-optionc.md`
  — confirmed by a targeted grep (`RT-004`/`RT-005`: zero matches). This is the fourth consecutive
  scoring pass in which this specific, lowest-priority item has been flagged and not closed.
- The BUG-010 entity's History table (last row 2026-08-12, ending at commit `e00ed1c4`/the prior #371
  fold-in) and `RESUME-HERE.md`'s commit table (last row `*(next commit)*`, un-hashed) do not name either
  `18ce85de` or `888c94a8` — a grep for both hashes across the entire BUG-010 folder returns matches only
  in the prior score report file itself (`adv-s014-final-score-18ce85de.md`), confirming no governance
  artifact has been updated to reference the two most recent commits.

**Improvement Path:** Add explicit Disposition D/E entries for RT-004/RT-005 (four passes overdue).
Add History rows for `18ce85de` and `888c94a8` to the BUG-010 entity and a corresponding commit-table
update to `RESUME-HERE.md`.

### Internal Consistency (0.93/1.00)

**Evidence — the specific #371 contradiction is fully resolved, verified across every artifact the task
named:**

- `RESUME-HERE.md:34` (Owner decisions, settled): *"**Fixed in this unit:** `Error:`→stdout routing (GH
  #371) — all `jerry ast` diagnostics now print to stderr; stdout carries only the JSON/render payload.
  Closes on merge."* — the prior self-contradiction (this same line previously read "Deferred") is gone.
  `RESUME-HERE.md:35` (Deferred list) no longer includes #371 — consistent with line 34.
- `DECISIONS-and-threat-model.md:26`: *"Folded in | `Error:`→stdout (#371) | **Fixed in this unit** |
  Demonstrated during end-to-end testing; all `jerry ast` diagnostic/error messages routed to stderr so
  stdout carries only the JSON/render payload. Closes on merge."* — no longer lists #371 as "Out of
  scope."
- `adv-tournament-consolidated-optionc.md:78`: *"`Error:` prints to stdout (SR-003, F-3, IN-002-adjacent)
  | **Fixed in this unit** (GH #371) — all `jerry ast` diagnostics routed to stderr; stdout stays clean
  JSON"* — no longer shows "Disposition D — Deferred/Tracked... (owner-deferred)."
- A grep for `371` across the entire BUG-010 folder confirms the only remaining "deferred" framing is the
  BUG-010 entity's own 2026-08-11 History row (line 139: *"...Error->stdout deferred (#371)..."*) — a
  time-ordered historical record of a decision later superseded on 2026-08-12, exactly the class of
  artifact the task instructed to exclude from this check. It is not contradicted by anything else in the
  same document (the 2026-08-12 row, line 141, is silent on #371's final status but does not restate the
  "deferred" claim either) and does not meet the bar of an active, currently-asserted false claim.

**New gap found this pass (minor, doc-bookkeeping class, not a contradiction):**
- Neither the BUG-010 entity's History table nor `RESUME-HERE.md`'s commit table has been updated with a
  row for `18ce85de` or `888c94a8` (see Completeness). This is the same *class* of governance-lag gap
  flagged in all three prior passes (IC-1/IC-2 in pass 1, entity History/AC lag in pass 2, the
  self-contradiction in pass 3), but it is meaningfully lower severity than any of those: it is silent on
  the closure rather than asserting anything false, and unlike the pass-3 finding, no reader consulting
  any single section of any artifact would be misled about #371's current status — every currently-live
  section (not superseded, not historical) says "Fixed."

**Improvement Path:** Add a 2026-08-12(-later) History row to the BUG-010 entity and update
`RESUME-HERE.md`'s commit table with `18ce85de` and `888c94a8`, finally closing the recurring lag pattern
noted across all four scoring passes in this lineage.

### Methodological Rigor (0.95/1.00)

**Evidence:** The specific rigor gap identified by the prior pass — *"the scoping methodology for 'find
every `jerry ast` diagnostic that needs this fix' was file-local (`ast_commands.py` only) rather than
command-surface-wide"* — is closed by this commit. The fix now covers both files on the `jerry ast`
routing path: `ast_commands.py` (already correct, re-verified unchanged) and `main.py`'s `_handle_ast`
router (the previously-missed file). The commit message itself (`"finish #371 stderr routing across the
ast router"`) reflects an explicit command-surface-wide framing, not a narrow patch. The two new tests
follow the codebase's established `capsys`-based idiom exactly (matching the seven prior GH #371 tests in
the same file), including asserting both the negative (`captured.out == ""`) and positive
(`"..." in captured.err.lower()`) conditions — the same dual-assertion discipline used throughout the
existing GH #371 test suite. The write-path TOCTOU fix (A-1/RT-001, `ast_commands.py:627-639`) remains
structurally unchanged and re-verified intact by this pass. Hexagonal purity, TDD discipline, and the
9-strategy tournament + eng-reviewer 0.955 gate baseline from the original PASS pass are unaffected.

**Gap:** The fix still does not extend to non-`ast` namespace routers in `main.py` (session, items,
projects, config, transcript, context, agents, ci, hooks all print router-diagnostics without
`file=sys.stderr`) — but this is explicitly out of scope for GH #371, which is scoped to `jerry ast` per
every governance artifact read (`DECISIONS-and-threat-model.md:26`, `CHANGELOG.md:16`). Not counted as a
rigor defect for this deliverable; noted for awareness only, since a security-conscious reviewer might
reasonably ask whether the same stdout-hygiene concern applies elsewhere.

**Improvement Path:** None required for this deliverable's scope. If a future ticket generalizes
stdout/stderr hygiene to the rest of the CLI, treat GH #371's fix pattern (and its test idiom) as the
template.

### Evidence Quality (0.95/1.00)

**Evidence:** Every claim in the task framing was independently verified against primary sources in this
pass, not accepted at face value: `main.py:428` and `:461` read directly and confirmed to carry
`file=sys.stderr`; the two new `TestMainAstRouting` tests read in full and confirmed to assert the correct
stream separation; `ast_commands.py`'s 20 `print(` sites re-scanned individually; the four governance
artifacts (`RESUME-HERE.md`, `DECISIONS-and-threat-model.md`, `adv-tournament-consolidated-optionc.md`,
`CHANGELOG.md`) read in full and grepped for stale "deferred"/"out of scope" language; and — new this
pass — the git worktree reflog read directly, independently corroborating commit `888c94a8` as the exact
HEAD with a commit message matching the task's own framing almost verbatim ("finish #371 stderr routing
across the ast router + reconcile docs"). The A-1/RT-001 TOCTOU fix was re-read at
`ast_commands.py:627-639` and confirmed structurally unchanged.

**Gap:** No new evidence-quality defect was found this pass (no overstated claims, no unverified
assertions in the artifacts read). The score is held at 0.95 rather than raised further because the
underlying evidence base is the same mature one carried from the original PASS pass, reinforced rather
than fundamentally strengthened.

**Improvement Path:** None specific; continue the established verification discipline.

### Actionability (0.92/1.00)

**Evidence:** All three items the task explicitly asked this pass to verify are closed with concrete,
independently-checked evidence: (1) `main.py` stdout leak — fixed, tested; (2) `RESUME-HERE.md` +
`DECISIONS-and-threat-model.md` + `adv-tournament-consolidated-optionc.md` reconciliation — fixed,
verified across all three files; (3) `CHANGELOG.md`'s Option C entry now mentions #371 explicitly — fixed,
verified. This is the fourth consecutive pass in this lineage where a specific, itemized set of prior
findings was closed with traceable, verifiable follow-through (not merely claimed) — the deliverable's
strongest and most consistent quality signal.

**Gaps:** Two specific recommendations have now been repeated, unclosed, across every pass in this
lineage: (a) RT-004/RT-005 explicit disposition (4 passes: 0.909, 0.928, 0.9165, this one), and (b) adding
the final commit hash to the BUG-010 entity History and `RESUME-HERE.md`'s commit table (3 passes: 0.928,
0.9165, this one, and the underlying pattern recurs a step further back to the very first 0.909 report's
CHANGELOG/consistency findings). A recommendation repeated four times without closure is a genuine
actionability weakness distinct from — and lower-severity than — a functional defect: the items are
individually trivial (single-line edits) but the process of actually closing them has not kept pace with
the process of fixing higher-priority items each pass.

**Improvement Path:** Close RT-004/RT-005 and the commit-hash rows in the *next* commit rather than
deferring them again; both are estimated at under 10 minutes combined and carry zero re-scoring risk.

### Traceability (0.91/1.00)

**Evidence:** The commit-chain verification method pioneered in the prior pass (reading the git worktree's
`gitdir:` pointer → `logs/HEAD`) was repeated and extended in this pass. The reflog independently confirms:
(a) the worktree is on branch `fix/BUG-010-ast-project-root`; (b) HEAD is
`888c94a85b21fd9899d2dc08e570c0eb4743da09` — an exact match to the task's stated commit; (c) the commit
message, `"fix(cli): finish #371 stderr routing across the ast router + reconcile docs (BUG-010)"`, matches
the task's framing of what changed almost verbatim; (d) the full commit chain
(`62b429e8 -> da34a8b8 -> cce557c5 -> a6240a4d -> e00ed1c4 -> 18ce85de -> 888c94a8`) is internally
consistent and matches every commit named in the prior three score reports plus the two new commits since.
This is the strongest single piece of traceability evidence produced in this lineage.

**Gaps:** Despite that strength, no in-repo governance document — not the BUG-010 entity's History table,
not `RESUME-HERE.md`'s commit table — has been updated to reference either `18ce85de` or `888c94a8` by
hash. This is the same structural "a document cannot self-reference the commit that includes its own final
edit" limitation noted in the prior two passes, but it has now compounded: where the prior pass had one
un-referenced commit (`18ce85de`), this pass has two (`18ce85de` and `888c94a8`), and the recommendation to
close this gap has been repeated without action across three consecutive reports. The gap remains lower
severity than a false claim (it is silent, not contradictory), but the compounding and the repeated
non-closure across passes is weighed here rather than treated as a fixed, static limitation.

**Improvement Path:** Once this report is persisted and committed, add its own commit hash to
`RESUME-HERE.md`'s commit table and to a new BUG-010 entity History row — the same recommendation as all
three prior passes, now covering two un-referenced commits instead of one. Consider the structural fix
suggested in the prior report: adopt a convention where the resume pointer references "HEAD at
report-generation time" rather than a literal hash that cannot include its own commit, breaking the
self-referential cycle permanently.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|-----------------|
| 1 | Traceability / Internal Consistency | 0.91 / 0.93 | 0.95+ / 0.96+ | Add `18ce85de` and `888c94a8` to `RESUME-HERE.md`'s commit table and a new BUG-010 entity History row — closes a gap repeated across 3 consecutive reports. |
| 2 | Actionability / Completeness | 0.92 / 0.93 | 0.95+ / 0.96+ | Add explicit Disposition D/E entries for S-001's RT-004 and RT-005 in `adv-tournament-consolidated-optionc.md` — the single item carried unaddressed across all 4 scoring passes in this lineage. |
| 3 | Traceability | 0.91 | 0.95+ | Consider a structural fix: have `RESUME-HERE.md` reference "HEAD at report-generation time" instead of a literal commit hash, to permanently close the self-referential bootstrapping gap rather than re-encountering it every pass. |

None of the three items are functional, security, or design defects — all are documentation/bookkeeping
polish. Unlike the prior pass, none is currently blocking the quality gate; they are listed for
completeness, and because a 3-4-pass pattern of repeated, unclosed low-priority recommendations is itself
worth surfacing as a process observation, not because any single item is individually significant.

---

## Leniency Bias Check

- [x] Each dimension scored independently — every dimension was re-derived from direct evidence gathered
      in this pass (source reads, full new-test reads, governance-artifact reads, git reflog read), not
      inherited from the prior 0.9165 figure or from the task's framing that both gaps are "now closed."
- [x] Evidence documented for each score — every score cites specific file:line, test name, or
      independently-read git-metadata evidence; the two gaps the task asked to verify were each checked
      against the actual source/tests/docs, not accepted on the task's word alone.
- [x] Uncertain scores resolved downward — where a dimension could plausibly be scored higher (e.g.,
      Completeness or Internal Consistency at 0.95+, given both cited gaps are cleanly closed), the more
      conservative figure (0.93) was kept because a real, if minor, gap was found in the same pass (the
      un-updated History/commit tables for the two newest commits) that a less careful review would have
      missed; Traceability was held at 0.91 rather than 0.94+ (matching the raw strength of the reflog
      evidence) specifically because the pattern of repeated, un-actioned recommendations across 3-4 passes
      is weighed as a real actionability/traceability weakness, not waved through because "the fix is
      individually trivial."
- [x] First-draft calibration considered — N/A; this is the same mature, heavily-reviewed C4 artifact as
      all three prior passes, scored against the corresponding high bar (0.90-0.95 per-dimension range).
- [x] No dimension scored above 0.95 without exceptional documented evidence — the highest scores awarded
      (Methodological Rigor 0.95, Evidence Quality 0.95) both stay at exactly 0.95, not higher, because
      each still carries a documented (even if out-of-scope or minor) observation in this pass.
- [x] Composite crossing 0.92 was checked against the "Critical findings" override — no new Critical or
      High-severity finding was discovered this pass; all findings are completeness/consistency/
      actionability-class bookkeeping items. The prior CRITICAL (A-1/RT-001, write-path TOCTOU) remains
      confirmed fixed in code, re-verified this pass at `ast_commands.py:627-639` (`target_path = resolved`
      unchanged). The PASS verdict is not blocked by the special-case override.

---

## Session Context (adv-scorer → orchestrator)

```yaml
verdict: PASS
composite_score: 0.9335
threshold: 0.92
weakest_dimension: traceability
weakest_score: 0.91
critical_findings_count: 0  # A-1/RT-001 confirmed fixed in code, re-verified this pass
iteration: 4  # fourth S-014 final-gate scoring pass (0.909 REVISE -> 0.928 PASS -> 0.9165 REVISE -> 0.9335 PASS)
improvement_recommendations:
  - "Add 18ce85de and 888c94a8 to RESUME-HERE.md's commit table and a new BUG-010 entity History row (repeated across 3 consecutive reports)"
  - "Add explicit Disposition D/E entries for S-001's RT-004 and RT-005 in adv-tournament-consolidated-optionc.md (carried unaddressed across all 4 scoring passes)"
  - "Consider having RESUME-HERE.md reference 'HEAD at report-generation time' instead of a literal commit hash to permanently close the self-referential bootstrapping gap"
```

---

*adv-scorer S-014 final gate score, fourth pass. No source, test, or worktracker file was modified by this
scoring pass — findings are reported for closure, not unilaterally applied (P-020). Persisted per P-002 at
`projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/adv-s014-final-score-888c94a8.md`.*
