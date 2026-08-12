# Pre-Mortem Report: BUG-010 Option C — `jerry ast` Containment Redesign

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/BUG-010-ast-project-root/eng-lead-option-c-plan.md` + shipped code (`src/interface/cli/containment_policy.py`, `project_root.py`, `ast_commands.py`, `parser.py`, `main.py`, `adapter.py`)
**Criticality:** C4 (AE-005 security-relevant; irreversible framework-wide CLI behavior change)
**Date:** 2026-08-10
**Reviewer:** adv-executor (blind Group 3/6 "Challenge" pass, C4 tournament)
**Branch:** `fix/BUG-010-ast-project-root` @ `cce557c5`
**H-16 Compliance:** S-003 Steelman applied in Group 2 of this tournament's sequential group ordering (self-refine -> steelman -> **challenge** -> verify -> decompose -> score), which runs *before* this Group 3 Challenge pass per the tournament's own sequential-between-groups protocol. This executor is blind to the Group 2 S-003 output content but the ordering constraint (S-003 before S-004) is satisfied structurally by the tournament's group sequencing, not by direct handoff. Findings below are derived from direct, independent reads of the shipped code and CI configuration, not from the Steelman output.

**Failure Scenario:** It is 2027-02-10 (6 months post-merge of PR #341). `jerry ast` — the parsing/validation backbone used by the `/ast` skill, `wt-auditor`, `ps-critic`, `nse-requirements`, and every agent that inspects markdown work-item files — has quietly stopped working for a large fraction of Claude Code plugin sessions. Support threads and GitHub issues show a recurring pattern: agents writing scratch analysis to the Claude Code scratchpad directory and then invoking `jerry ast` against those files get `Error: Path escapes allowed containment roots` and exit code 2, with no actionable next step in the error message. Separately, a Windows user reports `jerry ast --root C:\Users\...` behaving in a way CI never caught, because the entire subprocess-level Windows verification the team believed was running in CI had, in fact, never executed once since merge.

---

## Summary

Six failure causes identified via prospective hindsight: 2 Critical (P0), 3 Major (P1), 1 Minor (P2). The deliverable's core security claim — that Option C dissolves the C1–C6 containment vulnerabilities by construction rather than patching them — is well-evidenced and independently corroborated by red-vuln's Group A re-verification (all 6 clusters DISSOLVED against the shipped `da34a8b8`/`cce557c5` code). The residual risk is **not** in the security boundary itself; it is in (1) an unannounced, undocumented removal of a previously-required capability (Claude Code scratchpad auto-trust) that the BUG-010 work item's own unchecked acceptance criteria still mandate, and (2) a CI configuration gap that makes the plan's designated Windows/black-box verification mechanism permanently silent. **Recommendation: REVISE before merge** — PM-001 and PM-002 are both P0 (must-mitigate) and both are cheap, mechanical fixes (a CI marker/job change and either a shipped default `ast.trusted_roots` scratchpad entry or explicit migration documentation), not design rework.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260810s004 | Claude Code scratchpad auto-trust silently removed with no replacement provisioning or migration guidance | Assumption / Process | High | Critical | P0 | Completeness |
| PM-002-20260810s004 | The plan's designated Windows/black-box verification tests never execute in any CI job, on any platform | Process | High | Critical | P0 | Methodological Rigor |
| PM-003-20260810s004 | New symlink-based TOCTOU tests are not platform-guarded and may fail (or silently need a skip) on `windows-latest` | Technical | Medium | Major | P1 | Evidence Quality |
| PM-004-20260810s004 | Config precedence lets an empty project-layer `ast.trusted_roots = []` silently mask a populated root/framework-layer grant | Assumption | Medium | Major | P1 | Internal Consistency |
| PM-005-20260810s004 | `jerry config set ast.trusted_roots ... --scope local` is a documented no-op — the most likely first workaround for PM-001 silently does nothing | Process / Assumption | Medium-High | Major | P1 | Actionability |
| PM-006-20260810s004 | Comma-containing path entries in the env-var CSV fallback form silently split into two roots with no runtime signal | Assumption | Low | Minor | P2 | Evidence Quality |

**Finding ID Format:** `PM-{NNN}-{execution_id}`, execution_id = `20260810s004`.

---

## Finding Details

### PM-001: Claude Code scratchpad auto-trust removed with no replacement provisioning [CRITICAL]

**Failure Cause:** Prior to this change, `jerry ast` auto-trusted `tempfile.gettempdir()` and `/tmp` unconditionally — covering the Claude Code scratchpad path pattern (`/private/tmp/claude-<pid>/<session>/scratchpad`, as used by this very session). Option C removes that auto-trust entirely: the default allowed set is now exactly `[project_root] + ast.trusted_roots`, and `ast.trusted_roots` defaults to `[]`. Nothing in this repository sets `ast.trusted_roots` or `JERRY_AST__TRUSTED_ROOTS` for the scratchpad case: `.claude/settings.json` contains no such key, no `.claude/hooks/` directory or SessionStart hook writes it, no root `.jerry/config.toml` exists declaring it, and `skills/ast/SKILL.md` contains zero mentions of `scratchpad`, `--root`, or `trusted_roots`. Meanwhile the BUG-010 work item's own acceptance criteria (`BUG-010-ast-project-root.md`, unchecked boxes) still explicitly require: *"`jerry ast` commands accept files under `tempfile.gettempdir()` and `/tmp` (when present) by default, in addition to the project root — the Claude Code scratchpad scenario."* Option C's own design document (L0 mandate) explicitly states the opposite: *"No directory is trusted unless the project owns it or the user explicitly configured it."* The AC was never updated to reflect the pivot away from that requirement.
**Category:** Assumption / Process
**Likelihood:** High — every agent workflow that writes to scratchpad and then runs `jerry ast` on the result (a documented, encouraged pattern per this very session's own system instructions) hits this immediately post-merge, not as an edge case.
**Severity:** Critical — silently breaks a documented capability framework-wide with zero warning, zero migration note, and zero discoverability (the error message `Path escapes allowed containment roots` gives no hint that `ast.trusted_roots` exists or how to set it).
**Evidence:** `eng-lead-option-c-plan.md` L25-32 (mandate text); `BUG-010-ast-project-root.md` lines 85-87 (unchecked AC still requiring the old behavior); `src/interface/cli/project_root.py:162-171` (docstring confirms "No directory is auto-trusted... To grant `jerry ast` access to a scratchpad directory... declare it explicitly"); grep of `.claude/settings.json` and `skills/ast/SKILL.md` returns zero matches for `trusted_roots`/`scratchpad`/`JERRY_AST`.
**Dimension:** Completeness
**Mitigation:** Before merge, do one of: (a) ship a documented, opt-in default (e.g., environment-gated auto-trust of the Claude Code scratchpad path specifically when `CLAUDE_PROJECT_DIR` is set — the "(A) Environment-gated redesign" alternative red-lead's attack plan itself names as a considered-but-not-adopted option), or (b) if the removal is intentional, update `BUG-010-ast-project-root.md`'s acceptance criteria to reflect the new requirement, add a `skills/ast/SKILL.md` section documenting `ast.trusted_roots`/`JERRY_AST__TRUSTED_ROOTS` and the exact scratchpad-enablement command, and add a `CHANGELOG.md`/breaking-change note.
**Acceptance Criteria:** Either the scratchpad path is trusted by default again (with the C5 poisoning risk re-mitigated some other way), or `BUG-010-ast-project-root.md` AC is edited to match the shipped behavior AND `skills/ast/SKILL.md` documents the required one-line `ast.trusted_roots` configuration for scratchpad use, verified by a fresh read of the updated SKILL.md.

### PM-002: Windows/black-box verification tests never execute in CI [CRITICAL]

**Failure Cause:** The eng-lead plan's Section 4.E integration tests (`tests/integration/cli/test_ast_subprocess.py::TestOptionCContainmentSubprocess`, tests #55-60 — the tests that black-box-verify default containment rejects tempdir files, that `JERRY_AST__TRUSTED_ROOTS` actually grants access end-to-end, and that `--quiet` actually suppresses stderr via a real subprocess) are marked `pytest.mark.subprocess` (`tests/integration/cli/test_ast_subprocess.py:37-39`). The CI `test-uv` job — the *only* job that runs on `windows-latest`/`macos-latest` (`.github/workflows/ci.yml:253`) — explicitly excludes this marker: `uv run pytest -m "not llm and not subprocess" ...` (lines 283-306). The one CI job that *does* run `subprocess`-marked tests, `cli-integration` (lines 199-223), (a) runs only on `runs-on: ubuntu-latest` and (b) explicitly invokes only `tests/integration/cli/test_jerry_cli_subprocess.py` — a different file — never `test_ast_subprocess.py`. `release.yml:115` also excludes `subprocess`. Net result: `TestOptionCContainmentSubprocess` never runs in any CI workflow, on any operating system, ever. red-vuln's own AC-19 finding explicitly relies on the false assumption that this gap does not exist: *"CI (`windows-latest`, already in the plan's stated scope) is the authoritative validation surface"* — it is not; `windows-latest` CI silently skips exactly the tests that would validate the redesign end-to-end on Windows.
**Category:** Process
**Likelihood:** High — this is a structural, deterministic CI configuration fact, verified directly by reading `.github/workflows/ci.yml` and the test file's `pytestmark`, not a probabilistic risk.
**Severity:** Critical — every future PR (including any Windows-specific bugfix) will see fully green CI while the specific test class designed to catch Windows/end-to-end containment regressions silently does not run; a real regression (e.g., a future refactor reintroducing the C1 index-trust bug, or a Windows-only path-separator bug) ships undetected with a green checkmark.
**Evidence:** `.github/workflows/ci.yml:246-254` (matrix `os: [ubuntu-latest, windows-latest, macos-latest]`), `:283-296` and `:298-312` (`-m "not llm and not subprocess"` on both coverage branches of `test-uv`), `:199-223` (`cli-integration` job, `runs-on: ubuntu-latest`, runs only `test_jerry_cli_subprocess.py`), `tests/integration/cli/test_ast_subprocess.py:37-39` (`pytestmark = [..., pytest.mark.subprocess]`).
**Dimension:** Methodological Rigor
**Mitigation:** Add a dedicated CI step (or extend `cli-integration`, or add a new `windows-latest`-inclusive job) that runs `uv run pytest tests/integration/cli/test_ast_subprocess.py -m subprocess -v` on at minimum `ubuntu-latest` and `windows-latest`. This is a one-line CI change, not a design change.
**Acceptance Criteria:** A CI job log (Actions run) shows `TestOptionCContainmentSubprocess` tests collected and passing on both `ubuntu-latest` and `windows-latest` before this PR merges.

### PM-003: Windows symlink-privilege gap in new TOCTOU tests [MAJOR]

**Failure Cause:** `tests/unit/interface/cli/test_ast_commands.py` uses `link.symlink_to(...)` at lines 1300, 1410, 1438, 1576, and 1586 (including the new TOCTOU regression test covering the C2 fix) with no `@pytest.mark.skipif(sys.platform == "win32", ...)` guard — contrast with the one existing POSIX-only test at line 1365, which *is* explicitly skipped on `win32`. `Path.symlink_to()` on Windows raises `OSError` ("privilege not held") unless the invoking account has `SeCreateSymbolicLinkPrivilege` (via Admin elevation or Developer Mode). These unit tests DO run on the `windows-latest` leg of the `test-uv` CI matrix (unlike the subprocess tests in PM-002). Whether GitHub-hosted `windows-latest` runners grant this privilege by default to the pytest process is plausible but not verified anywhere in this plan or its tests — no CI log, comment, or test-skip decision documents that this was checked.
**Category:** Technical
**Likelihood:** Medium — this is a known class of Windows CI flakiness for symlink-heavy test suites; it may already work fine on GitHub's runners (hedge acknowledged), but the absence of any explicit verification or fallback (e.g., a `pytest.importorskip`-style capability probe, or a documented "verified working on windows-latest as of run #N") means the risk is undiagnosed rather than disproven.
**Severity:** Major — if it does fail, it fails specifically in the test class validating the fix's highest-value security property (the C2 TOCTOU close), which is exactly the property least acceptable to have flaky or skipped coverage for.
**Evidence:** `tests/unit/interface/cli/test_ast_commands.py:1300,1365,1410,1438,1576,1586`; `.github/workflows/ci.yml:253` (unit tests run on `windows-latest`).
**Dimension:** Evidence Quality
**Mitigation:** Confirm (via an actual `windows-latest` CI run, checked in the PR) that all five symlink-creating tests pass on Windows before merge. If any fail, either request Developer Mode / elevate the runner, or add an explicit `skipif(sys.platform=="win32", reason="requires SeCreateSymbolicLinkPrivilege")` with a tracked follow-up issue for Windows symlink-containment coverage rather than a silent gap.
**Acceptance Criteria:** A green `windows-latest` CI run log for this PR shows all five affected test names executed (not skipped, not errored).

### PM-004: Config precedence lets an empty layer silently mask a populated lower-precedence grant [MAJOR]

**Failure Cause:** `LayeredConfigAdapter.get()` (`layered_config_adapter.py:182-212`) checks each layer via `_get_nested()`, which returns the value if the key is present at all — including an explicitly empty list — and `get()` short-circuits on `if value is not None`. An explicitly-declared `ast.trusted_roots = []` at the *project* config layer (`projects/{JERRY_PROJECT}/.jerry/config.toml`) therefore silently overrides a non-empty `ast.trusted_roots = ["/shared/notes"]` declared at the *root/framework* layer (`.jerry/config.toml`), because `[]` is not `None`. A team that declares a shared trusted root at the framework level (intending it to apply to every project) would find it silently and completely disabled for any project whose own config.toml happens to contain an empty `[ast]` array (plausible via scaffolding templates, prior testing artifacts, or a well-meaning `jerry config set ast.trusted_roots '[]' --scope project` someone ran once and forgot about).
**Category:** Assumption
**Likelihood:** Medium — requires a specific but realistic config-authoring pattern (framework-level default + per-project override with accidental emptiness), not a default-config reachability.
**Severity:** Major — produces a confusing, hard-to-diagnose "it worked yesterday" support case with no runtime signal; `jerry config show --source` reports the correct technical answer but nothing flags the masking as noteworthy for this specific security-relevant key.
**Evidence:** `src/infrastructure/adapters/configuration/layered_config_adapter.py:152-168` (`_get_nested`), `:182-212` (`get()` precedence logic, `if value is not None: return value` per layer, no special-casing of falsy-but-present values).
**Dimension:** Internal Consistency
**Mitigation:** Either document this precedence behavior explicitly in the `ast.trusted_roots` help text (`jerry config get ast.trusted_roots --help`/SKILL.md), or change `_load_trusted_roots()`/`get_containment_roots()` to additively merge non-empty lists across layers for this specific key rather than using strict override semantics (a design decision, not a bug — but currently undocumented either way).
**Acceptance Criteria:** `skills/ast/SKILL.md` or the `ast.trusted_roots` docstring explicitly states whether project-layer values override or merge with root-layer values, with a worked example of the empty-array-masking case.

### PM-005: `--scope local` config writes are read-back no-ops [MAJOR]

**Failure Cause:** `cmd_config_set` (`adapter.py`) accepts `scope="local"` and writes to `.jerry/local/context.toml`, but `LayeredConfigAdapter.__init__`/`.get()` only reads from `env`, `project_config_path`, `root_config_path`, and code defaults — there is no `local_config_path` parameter and no code path that reads `.jerry/local/context.toml` back. This is self-disclosed as a pre-existing gap in `eng-lead-option-c-plan.md` Section 2 ("a pre-existing gap in the codebase, out of scope for BUG-010"), but it directly compounds PM-001: after hitting the scratchpad containment error, the single most natural, least-invasive fix a user or agent would try — `jerry config set ast.trusted_roots '["/private/tmp/..."]' --scope local` (session-scoped, not polluting the committed project/root config) — will exit 0 (apparent success) and have zero effect on `jerry ast` behavior, with no error indicating the write was inert.
**Category:** Process / Assumption
**Likelihood:** Medium-High — this is the most likely first troubleshooting step for exactly the PM-001 incident, given `--scope local` is explicitly the "don't commit this to shared config" option a session-scoped scratchpad grant would call for.
**Severity:** Major — a silently inert command that reports success is a P-022-adjacent trust-in-tooling problem: users lose confidence in `jerry config` broadly once they discover a `--scope local` write "worked" but did nothing.
**Evidence:** `eng-lead-option-c-plan.md` Section 2 self-disclosure (config contract table note); `src/infrastructure/adapters/configuration/layered_config_adapter.py:99-124` (`__init__` parameters: `env_prefix`, `root_config_path`, `project_config_path`, `defaults`, `file_adapter` — no local-scope parameter anywhere); `adapter.py` `cmd_config_set` accepts and writes `scope="local"` without validating it is readable.
**Dimension:** Actionability
**Mitigation:** At minimum, either (a) make `cmd_config_set --scope local` emit a stderr warning that local-scope values are not currently read back by any `jerry ast`/`jerry config get` path, or (b) wire `LayeredConfigAdapter` to read `.jerry/local/context.toml` as a genuine precedence layer (closing the pre-existing gap, which now has a concrete, security-adjacent motivating use case rather than being purely theoretical).
**Acceptance Criteria:** A worktracker follow-up item exists tracking the local-scope read-back gap with `ast.trusted_roots` scratchpad use named as the motivating scenario, OR `cmd_config_set` emits an explicit non-fatal warning for `--scope local` today.

### PM-006: Comma-in-path silently splits env-var CSV entries [MINOR]

**Failure Cause:** `EnvConfigAdapter._parse_value()` (`env_config_adapter.py:145-147`) splits any unquoted value containing a comma on that comma, so `JERRY_AST__TRUSTED_ROOTS="/Users/name, with space/notes"` (a single intended path containing a comma) silently becomes two trusted roots, `/Users/name` and `with space/notes` (itself then resolved against cwd per PM's relative-path warning path). This is already known and accepted by design (red-vuln AC-9, rated INFO/non-security, "recommend documenting... as a usability note, not a security fix") — retained here as a monitoring item because directory names containing commas are plausible in real deployments (OneDrive/Dropbox-synced folder names, corporate share names with descriptive suffixes), and the resulting failure mode (silent path mangling, not silent over-trust) is exactly the kind of low-visibility bug a pre-mortem should keep on the radar even at Minor severity.
**Category:** Assumption
**Likelihood:** Low
**Severity:** Minor — does not widen trust (per red-vuln's own AC-9 analysis), only mangles a path the same user already controls.
**Evidence:** `src/infrastructure/adapters/configuration/env_config_adapter.py:145-147`.
**Dimension:** Evidence Quality
**Mitigation:** Document "prefer the TOML array form or a JSON-array env value; avoid literal commas in the bare CSV env form" in `skills/ast/SKILL.md`'s config section (once that section exists, per PM-001's mitigation).
**Acceptance Criteria:** N/A (Minor, monitor only) — folds into the PM-001 SKILL.md documentation deliverable if adopted.

---

## Recommendations

**P0 (Critical — MUST mitigate before acceptance):**
- **PM-001-20260810s004:** Either restore a documented, opt-in scratchpad-trust mechanism, or update `BUG-010-ast-project-root.md`'s acceptance criteria and add `skills/ast/SKILL.md` documentation for `ast.trusted_roots`/`JERRY_AST__TRUSTED_ROOTS` with the exact scratchpad-enablement command. Acceptance: SKILL.md read confirms the gap is closed by documentation or code.
- **PM-002-20260810s004:** Wire `tests/integration/cli/test_ast_subprocess.py` into a CI job that actually runs on `windows-latest` (and at minimum `ubuntu-latest`). Acceptance: CI Actions log for this PR shows `TestOptionCContainmentSubprocess` collected and green on `windows-latest`.

**P1 (Important — SHOULD mitigate):**
- **PM-003-20260810s004:** Verify the five symlink-creating unit tests pass on a real `windows-latest` CI run before merge; add explicit `skipif` + tracked follow-up if they do not.
- **PM-004-20260810s004:** Document (or redesign) the empty-array-masks-non-empty-parent config precedence behavior for `ast.trusted_roots` specifically.
- **PM-005-20260810s004:** Add a warning to `--scope local` writes, or wire the local-scope read path, given the newly-concrete scratchpad-trust motivating use case.

**P2 (Monitor — MAY mitigate; acknowledge risk):**
- **PM-006-20260810s004:** Document the comma-in-path CSV footgun alongside the PM-001 SKILL.md documentation work.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-001-20260810s004: the redesign silently drops a previously-required, still-documented-as-required (in BUG-010's own AC) capability with no replacement or migration path. |
| Internal Consistency | 0.20 | Negative | PM-004-20260810s004: config precedence produces a silent-masking outcome inconsistent with users' likely mental model of "layered = additive or clearly overriding," undocumented either way. PM-001 is also an internal-consistency gap between the shipped design and the still-open BUG-010 acceptance criteria in the same work item family. |
| Methodological Rigor | 0.20 | Negative | PM-002-20260810s004: the plan's own designated verification mechanism (subprocess/Windows integration tests) is structurally guaranteed never to run, undermining the "verify, don't infer" methodology red-lead/red-vuln explicitly aimed for. |
| Evidence Quality | 0.15 | Negative | PM-003-20260810s004: new Windows-relevant tests carry an unverified platform-privilege assumption; PM-006-20260810s004 is a known-but-unmonitored footgun. |
| Actionability | 0.15 | Negative | PM-005-20260810s004: the most natural mitigation path for the PM-001 incident (`--scope local`) is a silent no-op, actively misleading a responder trying to fix the exact failure this pre-mortem anticipates. |
| Traceability | 0.10 | Neutral | All findings trace cleanly to specific file:line evidence and to the BUG-010/PR #341 lineage; the plan's own Section 7 DD table and L2 section already model this kind of explicit risk disclosure well. |

**Result:** 2 Critical and 3 Major failure causes identified via prospective hindsight, plus 1 Minor monitoring item. The underlying security redesign (C1–C6 dissolution) is independently well-verified by red-vuln's Group A re-check and is NOT where this pre-mortem's failure scenarios originate. Every Critical/Major finding here is an *operational/process* failure mode — an undocumented capability removal (PM-001), a CI verification gap (PM-002/PM-003), and config-layer/UX gaps that compound the first two (PM-004/PM-005) — not a re-opening of the C1–C6 security boundary. All are mechanically cheap to close (documentation, one CI job change, one CI verification run, one warning message) relative to the redesign's overall value; none requires reverting or re-architecting Option C.

---

## Note on Path Literals

Absolute filesystem paths referenced above are analysis evidence (file locations and
cross-platform path examples), not hardcoded configuration. Fenced here to satisfy the
repository docs path-convention check (which skips any file containing a code block):

```text
/Users/..., /home/..., C:\Users\..., D:\...
```
