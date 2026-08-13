# Quality Score Report: BUG-010 Option C — `jerry ast` Containment Redesign (TRUE FINAL Gate Score @ `18ce85de`)

## L0 Executive Summary

**Score:** 0.917/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.88)
**One-line assessment:** The GH #371 stderr fix and the worktracker tidy are both real and mostly correct
— confirmed line-by-line against the source, tests, and (for the first time in this scoring lineage) an
independently-verified git commit chain — but the closure work has a gap of its own kind: it fixed
`ast_commands.py`'s diagnostics but missed one equivalent, reachable stdout leak in `main.py`'s `_handle_ast`
router, and it introduced a fresh self-contradiction in `RESUME-HERE.md` about the very issue it claims to
have closed. Neither is a security defect; both are concrete, fixable in minutes, and keep this build just
under the 0.92 gate rather than over it.

---

## Scoring Context

- **Deliverable:** Option C `jerry ast` containment redesign + GH #371 stdout->stderr fix + worktracker
  tidy — `src/interface/cli/ast_commands.py`, `main.py`, `parser.py`, `project_root.py`,
  `containment_policy.py`, `adapter.py` + test suite, at commit `18ce85dea84a1d5b1fbd639d1cc4e9d2d225eae7`
- **Deliverable Type:** Code (security-relevant CLI containment control) + governance/worktracker artifacts
- **Criticality Level:** C4 (final gate re-score closing a C4 adversarial cycle; AE-005 security-relevant)
- **Scoring Strategy:** S-014 (LLM-as-Judge), standalone final gate re-score, third pass in this lineage
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-08-12
- **Prior Score:** 0.928 PASS (`adv-s014-final-score-optionc.md`, scored against `e00ed1c4`)
- **Method:** Direct re-verification of every claim in the task framing against the current repository
  state — read `ast_commands.py` in full, read `main.py`'s `_handle_ast` routing, read the full test file
  (2022 lines) for the GH #371 test coverage, and — new this pass — independently confirmed the commit
  chain via the git worktree's reflog (`.git` -> `gitdir:` -> `logs/HEAD`), since this scorer has Read but
  not Bash/git-CLI access. This resolves the Traceability blocker ("no Bash/git tool access to confirm the
  hash exists") that recurred in both prior passes. Methodological Rigor and Evidence Quality baselines
  from the prior 0.928 pass (hexagonal purity, TDD discipline, structural TOCTOU fix, 9-strategy tournament,
  eng-reviewer 0.955 gate) are reconfirmed unaffected by this closure work and are not re-litigated in
  detail below except where the new commit's changes touch them directly.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.9165 (reported as 0.917) |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | **REVISE** — 0.0035 below threshold; targeted revision, not a redesign |
| **Strategy Findings Incorporated** | Yes — prior final score (0.928 PASS @ `e00ed1c4`), `wt-audit-optionc.md`, `eng-reviewer-optionc-gate-report.md` (0.955), `adv-tournament-consolidated-optionc.md`, direct source/test/git verification performed in this pass |
| **Critical/High findings this pass** | 0 (all new findings are completeness/consistency-class, not security defects) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-------------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 12 active BUG-010 ACs now genuinely ticked, FEAT-001 fully synced; but GH #371's own stated goal ("stdout must stay clean for JSON-consuming pipelines") is only partially met — one reachable diagnostic in `main.py` still prints to stdout, untested |
| Internal Consistency | 0.20 | 0.88 | 0.176 | BUG-010 entity + FEAT-001 now fully synchronized (genuine fix of the recurring gap); but `RESUME-HERE.md` self-contradicts on GH #371's status within the same file, and 2 governance artifacts are stale on the same point |
| Methodological Rigor | 0.20 | 0.93 | 0.186 | TDD execution on the identified scope is clean and correct; but the "find every diagnostic print reachable via `jerry ast`" sweep was scoped to one file, not the full command surface, missing a same-class instance one file away |
| Evidence Quality | 0.15 | 0.94 | 0.141 | Every claim independently verified against source, tests, and (new) git reflog; "verified end-to-end" framing in the entity slightly overstates completeness given the two gaps found |
| Actionability | 0.15 | 0.93 | 0.1395 | Strong recommendation-to-fix track record continues (multiple prior-pass items closed with concrete evidence again this pass); 4-5 new/carried items remain untracked anywhere but this report |
| Traceability | 0.10 | 0.94 | 0.094 | The recurring "unverifiable commit hash" blocker from both prior passes is resolved: `18ce85de` is independently confirmed via git reflog, exact commit-message match to the task framing |
| **TOTAL** | **1.00** | | **0.9165** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence — GH #371 fix, confirmed real and correct within its stated scope:**
- `src/interface/cli/ast_commands.py` — every diagnostic `print(...)` now carries `file=sys.stderr`:
  line 301 (`_read_file` containment error), line 308 (file not found), line 314 (`OSError` on read),
  line 453 (unknown `--schema` type), line 604 (`ast_modify` missing key), lines 630-634 (write-time
  containment escape), line 658 (`OSError` on write). All JSON/render payload `print()` calls (lines 348,
  374, 446, 492, 535, 562, 680, 716, 763, 810, 857) remain un-redirected (stdout), confirmed by direct
  reading — the split is exactly as claimed.
- `tests/unit/interface/cli/test_ast_commands.py` — 8 tests confirmed exercising this split: 7 carry an
  explicit `"""...(GH #371...)"""` docstring (`test_parse_file_not_found_prints_error` :256-262,
  `test_render_file_not_found_prints_error` :333-341, `test_validate_file_not_found_prints_error`
  :436-444, `test_validate_with_unknown_schema_prints_error_to_stderr_only` :446-456,
  `test_query_file_not_found_prints_error` :651-659, `test_modify_missing_key_prints_error_to_stderr_only`
  :777-786, `test_read_file_when_containment_escape_then_error_printed_to_stderr_only` :1592-1620); an
  8th, `test_ast_modify_when_write_time_escape_rejected_then_error_includes_containment_hint` (:1707-1756),
  has its assertion changed to `captured.err` — the prior 0.928 score report's own quoted evidence
  (`adv-s014-final-score-optionc.md:82`) shows this same test asserting `captured.out` before this
  commit, confirming the assertion was genuinely flipped as part of this fix, not merely re-described.
- Worktracker tidy claims verified true: BUG-010's 12 active ACs are `[x]` (`BUG-010-ast-project-root.md`
  :88-120; the 2 struck-through SUPERSEDED lines correctly remain `[ ]`), a 2026-08-12 History row exists
  (:141) naming the re-score, commits, GH #371 fold-in, and wt-audit; FEAT-001 now lists BUG-010 in its
  Story/Enabler Inventory (:153), Work Item Links (:196), Progress Summary/Metrics (:200-231, "88%
  Bugs 7/8", "94% Overall 34/36"), and History (:258); `CHANGELOG.md` has exactly one BUG-010 entry
  (`### Security`, :16) — the stale `### Fixed` duplicate flagged by `wt-audit-optionc.md` W-005 is gone
  (grep for `BUG-010` in `CHANGELOG.md` returns only the Security entry plus one unrelated historical
  `BUG-010` reference from a different, older numbering scheme, line 75).

**Gaps (new, this pass):**
- **GH #371's own stated purpose is not fully met.** The test docstrings frame the goal as "stdout must
  stay clean for JSON-consuming pipelines" for `jerry ast`. `src/interface/cli/main.py`'s `_handle_ast`
  function has two diagnostic `print()` calls with no `file=sys.stderr`: line 428
  (`print("No ast command specified. Use 'jerry ast --help'.")`) and line 461
  (`print(f"Unknown ast command: {args.command}")`). Of these, line 428 is genuinely reachable through
  normal CLI use (`ast_subparsers = ast_parser.add_subparsers(dest="command")` in `parser.py:647` has no
  `required=True`, so `jerry ast` with no subcommand reaches this branch with `args.command is None`);
  line 461 is effectively dead/defensive in real usage because argparse's own subcommand-choice validation
  would reject a truly unknown subcommand before `_handle_ast` runs (only reachable via the existing unit
  test's `FakeArgs` bypass). A user piping bare `jerry ast | jq` would still see this diagnostic land on
  stdout — the exact class of defect GH #371 exists to close, one file away from where it was fixed.
  Neither branch has a test asserting stdout/stderr separation (`test_main_ast_no_command_returns_1` only
  patches stdout wholesale and asserts the return code, not the stream).
- No `CHANGELOG.md` entry documents the GH #371 fix itself. The existing `### Security` entry (:16) is the
  Option C entry from `e00ed1c4` and does not mention stdout/stderr diagnostic routing or `#371` at all.
- S-001's RT-004/RT-005 disposition remains open in `adv-tournament-consolidated-optionc.md`, carried
  unchanged from both prior scoring passes (lowest priority, non-blocking).

**Improvement Path:** Route `main.py:428` (and, for defense-in-depth, `:461`) through `file=sys.stderr`,
add a regression test asserting `jerry ast` with no subcommand keeps stdout empty. Add a one-line
`### Fixed` or amend the `### Security` BUG-010 entry in `CHANGELOG.md` to mention the `#371` stderr fix.

### Internal Consistency (0.88/1.00)

**Evidence — the two artifacts flagged as recurring gaps in the prior two passes are now genuinely fixed:**
- `BUG-010-ast-project-root.md` and `FEAT-001-claude-code-schema-validation.md` are fully synchronized
  with the shipped/verified state (see Completeness evidence above) — this closes the specific
  History/AC-lag gap flagged by both the 0.909 REVISE and 0.928 PASS prior reports, and independently
  confirmed here, not merely re-asserted.

**New gap found (this pass) — a self-contradiction inside `RESUME-HERE.md` itself:**
- The same file, in the same closure pass, makes three different claims about GH #371's status:
  line 20 (commit table): `"*(next commit)* | Worktracker audit + tidy, GH #371 (Error:->stderr) folded
  in, end-to-end re-verified."`; line 39 (Next actions): `"GH #371 (Error:->stdout) folded into this unit
  and fixed"`; but line 34 (Owner decisions, settled section): `"Deferred: Error:->stdout routing (#371);
  session-local config-layer gap (#370)."` — still listing #371 as deferred, unmodified from its prior
  "owner-deferred" framing. A reader consulting only the "Owner decisions (settled)" section — the section
  most likely to be treated as authoritative for scope decisions — would conclude #371 remains out of
  scope, directly contradicting the same document's own commit table and Next-actions sections two dozen
  lines away. This is the same *class* of defect as the prior pass's IC-1/IC-2 findings (a governance
  artifact making mutually exclusive claims about the same fact) — a recurrence, not a new pattern,
  inside the very document meant to prevent exactly this kind of drift.
- Two further artifacts are stale (not self-contradictory, but out of sync with the shipped code):
  `DECISIONS-and-threat-model.md:26` still lists `Error:`->stdout (#371) as `Out of scope`; and
  `adv-tournament-consolidated-optionc.md:78` (Disposition D — Deferred/Tracked) still shows
  `GitHub #371 (owner-deferred)` with no update reflecting the fix now shipped in this same commit.
  Neither of these two files was touched by this closure pass, so their staleness is a pre-existing-gap
  question rather than a fresh error, but it means the governance record as a whole does not yet agree
  with itself on #371's status even after the code fix landed.

**Improvement Path:** Update `RESUME-HERE.md:34` to remove `#371` from the "Deferred" list (or annotate it
"Resolved at `18ce85de`, superseding the earlier deferral"). Add one-line updates to
`DECISIONS-and-threat-model.md:26` and `adv-tournament-consolidated-optionc.md:78` marking `#371` resolved
rather than deferred/owner-deferred.

### Methodological Rigor (0.93/1.00)

**Evidence:** The TDD execution on the identified scope is sound: the print-to-stderr changes in
`ast_commands.py` are minimal, surgical, and match the existing pattern already established for the
write-time hint in `e00ed1c4` (this commit's fix generalizes what was already proven correct there). Test
coverage for the in-scope changes is thorough (8 tests, both positive "error goes to stderr" and negative
"stdout stays empty" assertions per test) and follows the codebase's established `capsys`-based idiom.

**Gap:** The scoping methodology for "find every `jerry ast` diagnostic that needs this fix" was file-local
(`ast_commands.py` only) rather than command-surface-wide. A more rigorous approach — e.g., grepping for
`print(` across every module reachable from the `ast` namespace router (`main.py:_handle_ast` included)
before declaring the sweep complete — would have caught the `main.py:428` gap identified above in the same
pass. This does not indicate a flawed fix, only an incomplete problem-boundary definition; the fix that was
made is itself correct and well-tested.

**Improvement Path:** When closing the `main.py` gap, grep the full `src/interface/cli/` tree for
`print(` calls reachable from any `jerry ast` invocation path as a completeness check, not just the
already-known `ast_commands.py` module.

### Evidence Quality (0.94/1.00)

**Evidence:** Every claim made in the task framing and in the entity/RESUME-HERE/wt-audit artifacts was
independently checked against primary sources in this pass: the source code (`ast_commands.py`, `main.py`,
`parser.py`), the test file (all 2022 lines, not a sample), `CHANGELOG.md`, `WORKTRACKER.md`, and — new
this pass — the git worktree's reflog (`/Users/.../jerry/.git/worktrees/proj-024-tactical-work-6/logs/HEAD`),
which independently corroborates the exact commit hash `18ce85de` and its message
(`"fix(cli): route jerry ast errors to stderr (#371) + worktracker tidy (BUG-010)"`) without relying on any
in-repo document's self-report. This is materially stronger evidence than either prior pass could produce
(both explicitly disclaimed "no Bash/git tool access").

**Gap:** The BUG-010 entity's History row (:141) states the fix was "Verified end-to-end via a real
`.jerry/config.toml` + the live `jerry` CLI" — true for the scenarios it lists (project-root allow,
configured-root allow, untrusted reject, `--root` override, env-var path, `--quiet` suppression), but the
phrase "end-to-end" slightly overstates completeness given the `main.py` gap and the `RESUME-HERE.md`
self-contradiction found in this pass were not caught by that verification pass.

**Improvement Path:** None specific beyond closing the two gaps above; the verification methodology itself
is sound and should be extended, not replaced.

### Actionability (0.93/1.00)

**Evidence:** The recommendation-to-fix track record continues to be the strongest single quality signal
in this deliverable's history: of the prior pass's items, the `wt-audit-optionc.md` checklist (W-001
through W-005) is now closed in full with verifiable evidence at every item — AC ticks, History row,
FEAT-001 sync, CHANGELOG dedup — a precise, traceable follow-through from a specific, itemized audit to
concrete diffs, the strongest form of actionability evidence available.

**Gaps:** This pass's own new findings — the `main.py` stdout leak, the `RESUME-HERE.md` self-contradiction,
the two stale governance artifacts, and the missing CHANGELOG entry for `#371` — are not yet tracked
anywhere; this report is the first place they are recorded, consistent with how prior-pass findings were
initially handled before being closed in a subsequent commit. RT-004/RT-005 remains open and untracked,
carried unchanged across three scoring passes now.

**Improvement Path:** Close the `main.py` gap and the `RESUME-HERE.md`/governance-artifact staleness in the
next commit, using this report's findings list directly (each item above is independently actionable and
small).

### Traceability (0.94/1.00)

**Evidence:** The TR-1 pattern that recurred across both prior scoring passes — "this scorer has no
Bash/git tool access to independently confirm the [claimed final] hash exists" — is resolved in this pass.
Reading the git worktree metadata directly (`.git` file -> `gitdir:` pointer ->
`/Users/.../jerry/.git/worktrees/proj-024-tactical-work-6/{HEAD,logs/HEAD}`) independently confirms: (a)
the worktree's current branch is `fix/BUG-010-ast-project-root`; (b) its HEAD commit is
`18ce85dea84a1d5b1fbd639d1cc4e9d2d225eae7` — an exact match to the task's stated final commit; (c) the
commit's own message, `"fix(cli): route jerry ast errors to stderr (#371) + worktracker tidy (BUG-010)"`,
matches the task's framing of what changed almost verbatim; (d) the full commit chain
(`62b429e8 -> da34a8b8 -> cce557c5 -> a6240a4d -> e00ed1c4 -> 18ce85de`) matches `RESUME-HERE.md`'s own
commit table (rows 15-19) exactly for the first five commits, with `18ce85de` as the genuine next step.
This is a structural, not incremental, improvement in traceability strength versus both prior passes.

**Gaps:** `RESUME-HERE.md`'s commit table (:20) and the BUG-010 entity's History (:141) still cannot name
`18ce85de` by hash — an inherent bootstrapping limitation (a document cannot self-reference the hash of the
commit that includes its own final edit), the same structural gap noted in both prior passes, now
recurring a third time for this specific commit. It is lower severity than a genuine contradiction because
it is silent/incomplete rather than false. Separately, this scorer cannot independently confirm from the
working tree alone whether `adv-s014-final-score-optionc.md` and `wt-audit-optionc.md` are actually staged
in the `18ce85de` commit tree (`wt-audit-optionc.md` I-002 flagged the former as untracked as of the audit)
— git reflog confirms the commit happened and its message references "worktracker tidy," which is strong
circumstantial evidence, but not a direct tree-content check (no git-CLI access for `git show --stat`).

**Improvement Path:** Once this report is persisted and committed, add its own commit hash to
`RESUME-HERE.md`'s commit table and to a new BUG-010 entity History row — the same recommendation as the
prior two passes, now for a third consecutive commit. Consider breaking this self-referential cycle by
adopting a convention where the resume pointer references "HEAD at report-generation time" rather than a
literal hash, or by committing the report in a dedicated follow-up commit that names its own hash.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|-----------------|
| 1 | Completeness | 0.90 | 0.95+ | Route `main.py:428` (`_handle_ast`, "No ast command specified") through `file=sys.stderr`; add a regression test asserting stdout stays empty for a bare `jerry ast` invocation. Optionally also fix the defensive/unreachable `:461` branch for consistency. |
| 2 | Internal Consistency | 0.88 | 0.95+ | Fix `RESUME-HERE.md:34` — remove `#371` from the "Deferred" bullet or mark it "Resolved at `18ce85de`." Update `DECISIONS-and-threat-model.md:26` and `adv-tournament-consolidated-optionc.md:78` (Disposition D) to reflect the shipped fix rather than "owner-deferred." |
| 3 | Completeness | 0.90 | 0.93+ | Add a `CHANGELOG.md` entry (new bullet or amendment to the existing BUG-010 Security entry) documenting the `#371` stdout->stderr diagnostic-routing fix explicitly. |
| 4 | Actionability / Completeness | 0.93 / 0.90 | 0.96+ / 0.95+ | Add explicit Disposition D/E entries for S-001's RT-004 and RT-005 in `adv-tournament-consolidated-optionc.md` (carried over unaddressed across three scoring passes now). |
| 5 | Traceability | 0.94 | 0.96+ | Add this report's own commit hash to `RESUME-HERE.md`'s commit table and a new BUG-010 entity History row once persisted. |

None of the five items are security or design defects; all are small, well-scoped, low-risk documentation
or narrow-scope-code fixes consistent with a REVISE (not REJECTED) verdict — the composite is 0.0035 below
threshold, and items 1-3 alone are plausibly sufficient to cross it on the next pass.

---

## Leniency Bias Check

- [x] Each dimension scored independently — Completeness, Internal Consistency, Methodological Rigor, and
      Traceability were each re-derived from direct evidence gathered in this pass (source reads, full
      test-file read, git reflog read), not inherited from the prior 0.928 figure or from the task's
      framing that both closure items are simply "confirmed."
- [x] Evidence documented for each score — every score cites specific file:line, test name, or
      independently-read git-metadata evidence; nothing is asserted without a traceable source in this
      report.
- [x] Uncertain scores resolved downward — the composite (0.9165) sits just below 0.92; where a plausible
      case could be made for rounding Completeness or Internal Consistency slightly higher (e.g., 0.91 for
      Completeness, given the `main.py` gap affects only one narrow, low-traffic CLI path), the more
      conservative figure was kept because the gap is real, reachable, and undiscovered by the closure
      process itself — exactly the kind of thing anti-leniency scoring exists to catch rather than wave
      through because "most of it is done."
- [x] First-draft calibration considered — N/A; this is the same mature, heavily-reviewed C4 artifact as
      both prior passes, scored against the corresponding high bar (0.90-0.94 per-dimension range, not a
      first-draft 0.65-0.80 range).
- [x] No dimension scored above 0.95 without exceptional documented evidence — the highest score awarded
      (Methodological Rigor 0.93, Evidence Quality 0.94, Traceability 0.94) all stay below 0.95 despite
      strong evidence, because each dimension also carries a documented, non-trivial gap found in this
      pass.
- [x] Composite crossing (or in this case, *not* crossing) 0.92 was checked against the "Critical findings"
      override — no new Critical or High-severity finding was discovered this pass; all five findings are
      completeness/consistency-class. The verdict is REVISE strictly because the weighted composite itself
      is 0.0035 below 0.92, not because of a Critical-findings override. The prior CRITICAL (A-1/RT-001,
      write-path TOCTOU) remains confirmed fixed in code, unaffected by this commit's changes
      (`ast_commands.py:627-639`, unchanged since the prior pass's verification).

---

## Session Context (adv-scorer → orchestrator)

```yaml
verdict: REVISE
composite_score: 0.9165
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.88
critical_findings_count: 0  # all findings this pass are completeness/consistency-class, not security defects
iteration: 3  # third S-014 final-gate scoring pass in this lineage (0.909 REVISE -> 0.928 PASS -> 0.9165 REVISE)
improvement_recommendations:
  - "Route main.py:428 (_handle_ast, 'No ast command specified') through file=sys.stderr; add a regression test for stdout staying empty on bare 'jerry ast'"
  - "Fix RESUME-HERE.md:34 self-contradiction — remove #371 from the 'Deferred' bullet or mark it resolved at 18ce85de; update DECISIONS-and-threat-model.md:26 and adv-tournament-consolidated-optionc.md:78 to match"
  - "Add a CHANGELOG.md entry documenting the #371 stdout->stderr diagnostic-routing fix explicitly"
  - "Add explicit Disposition D/E entries for S-001's RT-004 and RT-005 in adv-tournament-consolidated-optionc.md (carried over three passes now)"
  - "Add this report's own commit hash to RESUME-HERE.md's commit table and a new BUG-010 entity History row once persisted"
```

---

*adv-scorer S-014 final gate score, third pass. No source, test, or worktracker file was modified by this
scoring pass — findings are reported for closure, not unilaterally applied (P-020). Persisted per P-002 at
`projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/adv-s014-final-score-18ce85de.md`.*
