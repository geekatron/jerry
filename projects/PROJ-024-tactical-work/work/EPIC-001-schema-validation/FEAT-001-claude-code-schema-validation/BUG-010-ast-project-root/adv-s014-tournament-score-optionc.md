# Quality Score Report: BUG-010 Option C — `jerry ast` Containment Redesign (Final Tournament Re-Score)

## L0 Executive Summary

**Score:** 0.909/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.85)
**One-line assessment:** The security redesign itself is genuinely excellent and independently
verified in code (the critical write-path TOCTOU is structurally eliminated, not just patched), but
two governance/documentation artifacts (`CHANGELOG.md`, `RESUME-HERE.md`) still describe the
**superseded** always-widen behavior or an uncommitted state — close this narrow, low-risk gap
(estimated < 30 minutes of doc edits, zero code changes) and this clears the 0.92 gate on the next
pass.

---

## Scoring Context

- **Deliverable:** Option C `jerry ast` containment redesign — `src/interface/cli/containment_policy.py`,
  `project_root.py`, `ast_commands.py`, `parser.py`, `main.py`, `adapter.py` + 5 test files, at commit
  `a6240a4d` (claimed final; see Traceability finding TR-1 on commit-hash corroboration)
- **Deliverable Type:** Code (security-relevant CLI containment control)
- **Criticality Level:** C4 (tournament re-score closing a C4 adversarial cycle; AE-005 security-relevant)
- **Scoring Strategy:** S-014 (LLM-as-Judge), standalone final gate re-score
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-08-12
- **Method:** Direct read of the shipped source (not the reports' claims alone), cross-checked against
  every design section, the 9-strategy blind tournament, the eng-reviewer gate report (0.955), and the
  red-vuln behavioral PoC report. Two governance-artifact findings below were discovered independently
  during this scoring pass — not previously flagged by the tournament, eng-reviewer, or red-team.

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.909 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE (near-threshold band, 0.85–0.91) |
| **Strategy Findings Incorporated** | Yes — eng-reviewer gate report, red-vuln findings, adv-tournament-consolidated-optionc.md, S-001 red team, plus direct source verification |
| **Prior Score (eng-reviewer, pre-scope docs)** | 0.955 (did not audit `CHANGELOG.md`/`RESUME-HERE.md` against the final state) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-------------------|
| Completeness | 0.20 | 0.90 | 0.180 | All 6 original Criticals + 3 red-vuln findings + tournament A-1..A-7 verified fixed in code with tests; one stated AC ("changelog entry") not fulfilled |
| Internal Consistency | 0.20 | 0.85 | 0.170 | Code/design/tests fully consistent; `CHANGELOG.md` and `RESUME-HERE.md` contradict the claimed final state |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | Pure/impure hexagonal split, TDD, 9-strategy blind tournament + eng-reviewer + red-team, structural (not patch) fix for the write-path TOCTOU |
| Evidence Quality | 0.15 | 0.95 | 0.1425 | Real behavioral PoCs incl. live CLI transcript and a genuine symlink-swap regression test; file:line citations throughout |
| Actionability | 0.15 | 0.93 | 0.1395 | AC→fix→test chains precise; deferred items tracked as GH issues (#370–#373); the two new gaps found here are not yet tracked anywhere |
| Traceability | 0.10 | 0.85 | 0.085 | AC→fix→test chain excellent for code; no artifact in the repo corroborates commit `a6240a4d`; `CHANGELOG.md` doesn't trace to Option C |
| **TOTAL** | **1.00** | | **0.909** | |

---

## Detailed Dimension Analysis

### Completeness (0.90/1.00)

**Evidence:**
- All six original tournament Criticals (C1–C6) verified dissolved-by-design or fixed in the current
  source: `grep`-level confirmation of zero index-based matching (`containment_policy.py:143-173`,
  `ast_commands.py:242`), the ownership gate fully removed (no `st_uid`/`geteuid` anywhere), the default
  allowed set is exactly `[project_root]` + configured roots with zero `tempfile`/`TMPDIR` influence,
  and `--quiet` verified to suppress advisory text only, never the allow/deny outcome.
- All three red-vuln residual findings fixed at the correct chokepoint, each with dedicated regression
  tests: AC-11 blank-entry filter (`project_root.py:150-155`, tests `test_load_trusted_roots_when_env_var_is_whitespace_only_then_returns_empty_list`,
  `test_get_containment_roots_when_trusted_roots_env_blank_and_cwd_outside_project_then_cwd_not_trusted`),
  AC-18 `JERRY_PROJECT` traversal fail-closed (`project_root.py:89-106`, tests
  `test_load_trusted_roots_when_jerry_project_traverses_outside_projects_tree_then_project_layer_ignored`),
  AC-10 relative-entry warn-and-honor (`project_root.py:213-235`, tests `..._trusted_root_relative_then_still_trusted_and_warns`).
- The tournament's one confirmed **CRITICAL** code defect — A-1/RT-001, the write-path check≠use TOCTOU
  (CWE-367) — is fixed **structurally**, not by patching: `target_path = resolved` (`ast_commands.py:633`)
  now comes directly from the write-time `_check_path_containment` call's return value; the previously
  separate, unvalidated `Path(file_path).resolve()` capture is gone entirely. This closes not only
  RT-001 but its sibling RT-003 (parent-directory symlink swap) as a structural consequence, since
  `target_path.parent` now derives from the same single resolved value. Verified by
  `test_ast_modify_when_write_time_check_resolves_swapped_target_then_write_lands_on_validated_path`,
  which is explicitly documented as RED against the pre-fix code and correctly isolates "which file
  receives the write" from "is the write accepted/rejected."
- A-2 through A-7 (broad-project-root warning, whitespace-entry stripping, stale docstring, dead-code
  removal, remediation hint, Windows `skipif` guards) all verified present in the current source.

**Gaps:**
- BUG-010's own Acceptance Criteria list includes "changelog entry" as a required item (see
  `BUG-010-ast-project-root.md` AC list, unchecked item). `CHANGELOG.md` has **not** been updated for
  the Option C redesign at all (see IC-1 under Internal Consistency) — this AC is not satisfied.
- S-001's RT-004 (each `ast_modify` invocation performs two independent full config-layer reads,
  widening the window for concurrent `jerry config set` drift) and RT-005 (`--quiet` is suppressible by
  precisely the audience — agent/scratchpad JSON pipelines — most likely to be operating under a
  widened trust store) are Minor findings that are not explicitly dispositioned anywhere in
  `adv-tournament-consolidated-optionc.md`'s Disposition A–E tables. RT-004's practical risk is largely
  moot post-A-1-fix (the race it worried about no longer exists), and RT-005 is consistent with the
  documented "best-effort, not a security boundary" threat model — but neither is explicitly recorded
  as an accepted/deferred item the way F-2/F-3/F-4 and #370–#373 are.

**Improvement Path:** Add a `CHANGELOG.md` entry describing the Option C redesign (supersedes the
existing "widen to temp/scratchpad" entry) and check off the "changelog entry" AC. Add one line each
to `adv-tournament-consolidated-optionc.md`'s Disposition D/E tables explicitly accepting RT-004/RT-005
as no-action-required (with one-sentence rationale, mirroring the existing IN-002/IN-004 entries).

### Internal Consistency (0.85/1.00)

**Evidence:**
- Code, tests, and design docs (`eng-lead-option-c-plan.md`, `DECISIONS-and-threat-model.md`) are fully
  mutually consistent — every design claim I checked against the live source held exactly as stated
  (classification is origin-derived not index-derived; write-time recheck is literally the same
  function call as read-time; default allowed set excludes temp/`TMPDIR` entirely).
- The one internal-consistency defect the prior eng-reviewer gate found (F-1, stale `parser.py`
  docstring claiming OS temp/scratchpad defaults) is confirmed **fixed** in the current source
  (`parser.py:578-582` now correctly describes the `ast.trusted_roots` model).

**Gaps (found independently during this pass — not previously flagged):**
- **IC-1 (governance artifact, moderate).** `CHANGELOG.md` still contains two "Fixed"/"Security"
  entries (lines 16 and 28) that describe the **superseded** design: a temp-root ownership gate keyed
  on `st_uid`/`geteuid()`, and containment defaults "widened... to include OS temp/scratchpad
  directories." Both mechanisms were **removed** by the Option C redesign (per `DECISIONS-and-threat-model.md`
  DD-2 and the BUG-010 entity's 2026-08-11 History entry). There is **no** `CHANGELOG.md` entry for
  Option C at all. A reader of the changelog alone — the most public-facing artifact of this repo —
  would believe `jerry ast` still auto-trusts OS temp directories with an ownership gate, which is
  false as of the shipped code. This is the same class of defect as the already-caught F-1 (a
  security-relevant doc contradicting the shipped model), just in a different file that the tournament
  did not audit.
- **IC-2 (governance artifact, minor).** `RESUME-HERE.md` (dated "Updated 2026-08-12," the same date
  claimed for the final commit) still lists the tournament fixes A-1..A-7 as "*(uncommitted)*... **Next
  checkpoint**" in its commit table, and its "Next actions" list still reads "1. Checkpoint the
  tournament fixes... 2. Run the S-014 scorer... 3. On PASS: PR review + merge" — i.e., the resume
  pointer describes exactly the state *before* this scoring run, not the "commit `a6240a4d`, all
  findings remediated" state asserted in this scoring task's input context. Either the artifact lags
  the actual commit, or the commit hash `a6240a4d` is not yet reflected anywhere in the repository's
  own bookkeeping (see Traceability TR-1). Low severity (it is a resume pointer, not user-facing), but
  a genuine internal-consistency gap between the claimed final state and the project's own tracking
  artifact.
- **IC-3 (code, minor).** The write-time rejection message (`ast_commands.py:630`,
  `f"Error: Path escapes allowed containment roots at write time: {file_path}"`) does **not** include
  the `_CONTAINMENT_ESCAPE_HINT` remediation text ("configure ast.trusted_roots or pass --root") that
  the read-time equivalents at `ast_commands.py:245` and `:256` do carry. A-6 was scoped as "add a
  remediation hint to the escape message" without specifying read-only; the write-time path is the one
  most likely to surface for `ast_modify` — an inconsistency in applying the same fix uniformly.

**Improvement Path:** Update `CHANGELOG.md` (IC-1, required — ties to the unmet AC). Update
`RESUME-HERE.md`'s commit table and "Next actions" to reflect the actual final commit and status
(IC-2). Append `_CONTAINMENT_ESCAPE_HINT` to the write-time error message for consistency with the
read-time messages (IC-3, one-line fix, add a regression test asserting the hint substring is present).

### Methodological Rigor (0.96/1.00)

**Evidence:** Textbook hexagonal separation — `containment_policy.py` is a genuinely zero-I/O pure
decision core (confirmed: only stdlib imports), with the I/O boundary (env, filesystem, config)
confined to `project_root.py`/`adapter.py`. TDD discipline is evident in test naming
(`test_{scenario}_when_{condition}_then_{expected}`) and in tests explicitly documented as "RED against
the pre-fix code" (e.g., the A-1 regression test). The security process itself is exceptionally
rigorous for a single bug fix: an eng-lead implementation plan → TDD implementation → red-team 21-case
attack-plan re-check with real behavioral PoCs → a full 9-strategy blind adversarial tournament
(self-refine, steelman, red team, devil's advocate, pre-mortem, constitutional, chain-of-verification,
inversion, FMEA) → eng-reviewer final gate → consolidated deduplication → targeted fixes → this final
re-score. The A-1 fix is structural (eliminates the vulnerable code path entirely) rather than a
symptom patch, which is the correct depth of fix for a C4 security finding.

**Gaps:** None material. The only nit is that the double config-layer read per `ast_modify` invocation
(RT-004) is a minor architectural inefficiency that survives, though it is no longer security-relevant
post-A-1-fix.

**Improvement Path:** None required to pass this dimension; already exceeds the 0.92 bar in isolation.

### Evidence Quality (0.95/1.00)

**Evidence:** The red-vuln report is unusually rigorous for this class of artifact — it includes an
actual `uv run jerry ast` CLI invocation transcript (not just in-process function calls) for the
highest-value finding (AC-11), and a genuine read→write symlink-swap PoC against the shipped
`ast_modify()` with byte-for-byte "unmodified" verification of the outside file. `ruff`/`mypy` clean
claims are consistent with the code style observed. Coverage figures are reconciled honestly (73%
module-level vs. ~97% changed-lines, with the discrepancy explained rather than cherry-picked). The
Windows validation limitation (AC-19/AC-21, reasoning + same-flavor-mocked, no live win32 host) is
disclosed plainly rather than glossed over — a genuine P-022 compliance signal.

**Gaps:** No live-Windows execution (disclosed, not concealed — this is a quality-of-disclosure
strength, not a scoring penalty beyond what's already reflected). I could not independently verify the
GitHub #337 comment claim (no network tool available to this scorer) or the existence of commit
`a6240a4d` in the actual git history (no Bash/git tool available to this scorer) — both are accepted
as claimed per the task's framing, but are flagged in Traceability since no *internal* artifact
corroborates the commit hash either.

**Improvement Path:** None required to pass this dimension.

### Actionability (0.93/1.00)

**Evidence:** Every finding across the red-vuln report and the consolidated tournament carries an exact
file:line location and a specific, verified-applied fix. Deferred/out-of-scope items are tracked as
concrete GitHub issues (#370 session-local config gap, #371 stdout error routing, #372 scratchpad
turnkey provisioning, #373 composition-root cleanup) rather than left implicit. Owner decisions (DD-1
through DD-4) are recorded with explicit choices and rationale in `DECISIONS-and-threat-model.md`.

**Gaps:** The two governance-artifact findings identified in this pass (IC-1 CHANGELOG, IC-2
RESUME-HERE) are not yet tracked as follow-up items anywhere — unlike F-2/F-3/F-4, which the
eng-reviewer explicitly scheduled as follow-ups. This score report itself now serves that tracking
function, but the gap existed at scoring time.

**Improvement Path:** Add IC-1/IC-2/IC-3 as either immediate fixes (recommended — they are small,
low-risk documentation edits) or explicitly tracked follow-up issues if deferred.

### Traceability (0.85/1.00)

**Evidence:** Within the code/test surface, the AC → fix → test chain is explicit and strong: every
one of A-1 through A-7 and AC-10/AC-11/AC-18 maps to a named, greppable test function. The BUG-010
worktracker entity's History section documents the 62b429e8 → da34a8b8 → cce557c5 commit progression
and the pivot rationale (0.64 REVISE → Option C → 0.955 gate).

**Gaps:** **TR-1** — none of the artifacts read for this score (`BUG-010-ast-project-root.md`,
`RESUME-HERE.md`, `eng-reviewer-optionc-gate-report.md`, `red-vuln-option-c-findings.md`,
`adv-tournament-consolidated-optionc.md`) reference the commit hash `a6240a4d` given as this task's
"final" commit — the most recent commit hash appearing anywhere in the repository's own bookkeeping is
`cce557c5`. This scorer has no git/Bash tool access to independently confirm `a6240a4d` exists, is
descended from `cce557c5`, or is the actual `HEAD` of `fix/BUG-010-ast-project-root`; the source-code
verification in this report (which *does* independently confirm every claimed A-1..A-7 fix is present
in the currently-readable working tree) is the strongest available substitute evidence, but it is not
the same as a corroborated commit-hash chain. **TR-2** — `CHANGELOG.md` (see IC-1) breaks the
traceability chain forward from "fixed in code" to "documented for release," which is otherwise
complete for every other dimension of this redesign.

**Improvement Path:** Add a History entry to `BUG-010-ast-project-root.md` and a line to
`RESUME-HERE.md` explicitly naming the final commit hash once identified/confirmed, closing the loop
between "claimed final commit" and "artifact-corroborated final commit." Fix `CHANGELOG.md` per IC-1.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|-----------------|
| 1 | Internal Consistency / Completeness | 0.85 / 0.90 | 0.95+ / 0.95+ | Update `CHANGELOG.md`: replace or supersede the two stale "Security"/"Fixed" entries (lines 16, 28) describing the removed ownership gate and temp/scratchpad auto-trust with an entry describing the Option C redesign (`ast.trusted_roots`, `--quiet`, TOCTOU close). Check off the "changelog entry" AC in `BUG-010-ast-project-root.md`. |
| 2 | Traceability / Internal Consistency | 0.85 / 0.85 | 0.92+ / 0.92+ | Update `RESUME-HERE.md`'s commit table to add the final commit (currently claimed as `a6240a4d`) and rewrite "Next actions" to reflect the post-checkpoint, scoring-complete state. Add the same commit hash to the BUG-010 entity's History table. |
| 3 | Internal Consistency | 0.85 | 0.92+ | Append `_CONTAINMENT_ESCAPE_HINT` to the write-time error message at `ast_commands.py:630` for consistency with the read-time messages at `:245`/`:256`; add one regression test asserting the hint substring is present in the write-time rejection message. |
| 4 | Completeness | 0.90 | 0.95+ | Add one-line explicit dispositions for S-001's RT-004 and RT-005 to `adv-tournament-consolidated-optionc.md` (Disposition D or E), mirroring the existing IN-002/IN-004 treatment, so no tournament finding is left un-dispositioned. |

None of the four items require code-behavior changes, new tests beyond one small addition (item 3),
or re-running the tournament — this is a documentation-consistency closure pass, not a redesign.

---

## Leniency Bias Check

- [x] Each dimension scored independently — Internal Consistency and Traceability were scored down
      based on artifacts (`CHANGELOG.md`, `RESUME-HERE.md`) discovered during this pass, not inherited
      from the eng-reviewer's 0.955 figure, which did not audit those files.
- [x] Evidence documented for each score — every score cites specific file:line or test-name evidence.
- [x] Uncertain scores resolved downward — the composite (0.909, computed from the boundary-case
      dimension scores) was rounded/held at the lower REVISE band rather than rounded up to PASS; where
      IC-1/IC-2 severity was ambiguous (documentation-only vs. AC-blocking), the AC-blocking
      interpretation (lower score) was used per BUG-010's own explicit "changelog entry" AC item.
- [x] First-draft calibration considered — N/A; this is a mature, heavily-reviewed C4 artifact, not a
      first draft, and is scored against the corresponding high bar (multiple dimensions at 0.93–0.96).
- [x] No dimension scored above 0.95 without exceptional documented evidence — Methodological Rigor
      (0.96) and Evidence Quality (0.95) are the two dimensions at or near that ceiling, each backed by
      concrete, checkable artifacts (real PoC transcripts, a genuinely structural not cosmetic fix for
      the CRITICAL finding, a 9-strategy blind tournament).

---

## Session Context (adv-scorer → orchestrator)

```yaml
verdict: REVISE
composite_score: 0.909
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.85
critical_findings_count: 0  # the one prior CRITICAL (A-1/RT-001) is confirmed fixed in code
iteration: 1  # first S-014 tournament final re-score at the "all findings remediated" checkpoint
improvement_recommendations:
  - "Update CHANGELOG.md to replace the two stale ownership-gate/temp-widen entries with an Option C entry; check off the 'changelog entry' AC"
  - "Update RESUME-HERE.md commit table and BUG-010 entity History with the final commit hash"
  - "Append _CONTAINMENT_ESCAPE_HINT to the write-time error message (ast_commands.py:630) for consistency with read-time messages"
  - "Add explicit Disposition D/E entries for S-001's RT-004 and RT-005 in adv-tournament-consolidated-optionc.md"
```

---

*adv-scorer S-014 final re-score. No source, test, or worktracker file was modified by this scoring
pass — findings are reported for closure, not unilaterally applied (P-020). Persisted per P-002 at
`projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/adv-s014-tournament-score-optionc.md`.*
