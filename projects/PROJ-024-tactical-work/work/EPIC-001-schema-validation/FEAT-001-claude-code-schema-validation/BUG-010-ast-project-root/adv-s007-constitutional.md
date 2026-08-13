# Constitutional Compliance Report: BUG-010 `jerry ast` Containment Widening (PR #341)

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `src/interface/cli/{project_root,ast_commands,parser,main}.py` + associated tests, branch `fix/BUG-010-ast-project-root`, and `BUG-010-ast-project-root.md` entity
**Criticality:** C4 (tournament, Group D — security-adjacent path-containment change)
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind, Group D, S-007 only)
**Constitutional Context:** `quality-enforcement.md` HARD Rule Index (H-01–H-36), `architecture-standards.md` (H-07, H-10), `coding-standards.md` (H-11, H-12), `testing-standards.md` (H-20, H-21), `python-environment.md` (H-05), P-020/P-022 (`CLAUDE.md` H-02/H-03)

---

## Summary

**PARTIAL compliance.** 0 Critical, 2 Major, 1 Minor findings. All HARD architectural/typing/docstring rules checked (H-05, H-07, H-10, H-11, H-12) are COMPLIANT. The two Major findings are not HARD-rule violations but P-022-adjacent transparency/completeness gaps: (1) the BUG-010 entity's own Acceptance Criteria checklist is internally inconsistent with its History narrative and with the actual (verified) implementation state, and (2) the RED-BUG010 H-01 ownership-gate remediation has an unaddressed edge case where a project root that itself resolves under a shared temp directory silently bypasses the ownership check the checked-off AC implies is comprehensive. Constitutional Compliance Score: **0.88 (REVISE band, 0.85–0.91)**. Recommend targeted revision (sync the AC checklist; document or close the ownership-gate edge case) rather than full rejection — the core H-05/H-07/H-10/H-11/H-12 compliance is clean and the security posture is materially improved over the pre-change baseline.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260807T-S007 | H-07: Interface layer isolation | HARD | COMPLIANT | `project_root.py`/`ast_commands.py` import only `os`, `sys`, `tempfile`, `pathlib`, `markdown_it`, and `src.domain.markdown_ast` (interface→domain is permitted). Grep of `src/domain/` and `src/application/` for `from src.interface` / `import src.interface` → zero matches (no reverse contamination). | Methodological Rigor |
| CC-002-20260807T-S007 | H-10: One public class per file | HARD | COMPLIANT | `project_root.py` and `ast_commands.py` contain zero classes/protocols (function-only modules, confirmed via grep for `^class `). Matches eng-lead plan's own H-10 self-check. | Methodological Rigor |
| CC-003-20260807T-S007 | H-11: Type hints on public functions | HARD | COMPLIANT | All new/modified functions (`get_containment_roots`, `_is_broad_containment_root`, `_check_temp_root_ownership`, `_is_temp_default_root_match`, `_warn_if_temp_root_match`, all 10 `ast_*` `root: str \| None = None` params, `_add_root_argument`) carry full type annotations, verified by direct read. | Methodological Rigor |
| CC-004-20260807T-S007 | H-12: Docstrings on public functions/classes | HARD | COMPLIANT | Every function reviewed has a Google-style docstring with Args/Returns; `get_containment_roots` and `_check_temp_root_ownership` docstrings additionally embed the required user-discretion policy statement per the eng-lead plan's H-12 mapping. | Completeness |
| CC-005-20260807T-S007 | H-05: UV-only execution | HARD | COMPLIANT (by reference) | No direct `python`/`pip` invocation appears in the reviewed source; eng-lead plan and BUG-010 History both specify `uv run pytest` / `uv run mypy` / `uv run ruff` for verification commands. | Methodological Rigor |
| CC-006-20260807T-S007 | H-20/H-21: Test-first, coverage | HARD | COMPLIANT (evidence-limited) | Static grep confirms all named test functions from the eng-lead L1 Test Plan exist in `tests/unit/interface/cli/test_project_root.py` and `test_ast_commands.py` (T-1 through T-6, plus the RED-BUG010 ownership-gate class `TestTempRootOwnershipGate`), matching the BUG-010 History's RED→GREEN narrative. **Caveat:** this agent has no Bash/execution tool available in this session; the "149/149" / "371/371" pass counts and coverage percentage in the entity's History table were NOT independently re-executed, only corroborated by test-name presence. Recommend adv-scorer or a CI run cross-check this before merge. | Evidence Quality |
| CC-007-20260807T-S007 | P-022 / H-03: No deception — Acceptance Criteria checklist accuracy | MEDIUM | **Major** | `BUG-010-ast-project-root.md` lists 9 scope-widening Acceptance Criteria (lines 84–115); only 2 are checked `[x]` (the RED-BUG010 H-01 ownership gate and H-02/H-08 broad-root ancestor check). The remaining 7 — including "`--root` flag exists on all 10 subcommands," "temp/`/tmp` defaults accepted," "symlink-from-temp-root rejected," "`TestA07PathTraversal` re-verified green," and both R-3/R-4 stderr behaviors — remain `[ ]` unchecked, **despite** the entity's own `History` table (2026-08-07, third row) asserting all of this is implemented, test-covered, and green ("GREEN after — 149/149... 371/371... `ruff format --check` and `ruff check` both exit 0"), and despite this agent independently confirming matching test functions exist for every one of those 7 items (`test_ast_root_flag_available_on_every_subcommand`, `test_containment_when_file_in_gettempdir_with_different_project_dir_then_allowed`, `test_containment_when_symlink_escapes_from_temp_root_then_rejected`, `test_check_path_containment_when_explicit_root_is_broad_then_warns`, `test_check_path_containment_when_matched_via_temp_root_then_prints_transparency_note`, CHANGELOG.md BUG-010 follow-up bullet present). | Internal Consistency |
| CC-008-20260807T-S007 | P-022 / H-03: No deception — security-gate coverage claim | MEDIUM | **Major** | The RED-BUG010 H-01 ownership gate (`_check_temp_root_ownership`, gated via `_is_temp_default_root_match`) is checked off `[x]` in the BUG-010 entity as closing the multi-user shared-temp read/write gap "scoped strictly to temp-default matches, never the project root." However, `_is_temp_default_root_match` classifies a match as "project root" (`matched_root == allowed_roots[0]`) purely by **positional identity**, not by whether that root is actually outside a shared/temp filesystem area. If `CLAUDE_PROJECT_DIR` is unset and the user's cwd is itself `/tmp`, `tempfile.gettempdir()`, or any subdirectory of either (a plausible scenario — e.g., a CI job or ad hoc shell session `cd`'d into a scratch directory before invoking `jerry ast`), `get_project_root()` resolves to that same shared, world-writable directory tree, and `allowed_roots[0]` becomes that shared path. Every file under it now matches "project root" rather than a "temp-default match," so the H-01 ownership check (`_check_temp_root_ownership`) is **silently skipped** for exactly the multi-tenant location it was built to protect — the promised "never the project root" carve-out was designed to mean "the user's deliberately-chosen project," not "whatever cwd happens to structurally coincide with a shared temp path." No test in the reviewed suite exercises `get_project_root()` resolving into `gettempdir()`/`/tmp` territory, so this gap is untested as well as unremediated. | Methodological Rigor |
| CC-009-20260807T-S007 | H-12 / P-001: Docstring accuracy — read/write containment-set agreement claim | SOFT | Minor | `ast_modify`'s `root` parameter docstring states the value is "Threaded identically into the read-time check and the write-time TOCTOU recheck below, so a single invocation never disagrees on the allowed containment set between read and write." This is true for the `root` **argument** (same variable passed to both `_read_file` and the write-time `get_containment_roots(root)` recheck), but `get_containment_roots()` is not a pure function of `root` alone — it also depends on live environment state (`CLAUDE_PROJECT_DIR`, `tempfile.gettempdir()`, `_HARDCODED_TMP.exists()`) re-evaluated at each call. The claim technically holds only under the (near-certain, but not asserted-as-an-assumption) precondition that this state is stable across the milliseconds between the two calls within one synchronous invocation. Wording overclaims a guarantee ("never disagrees") that is actually "does not disagree absent concurrent environment mutation, which is not itself guarded against or disclaimed." Low practical exploitability (red-vuln's H-05 verdict already treats the residual TOCTOU window as accepted, bounded by `mkstemp`/`os.replace` atomicity) — this is a documentation-precision gap, not a functional one. | Evidence Quality |

**Finding ID Format:** `CC-{NNN}-20260807T-S007` (execution session identifier: `20260807T-S007`).

**Severity Definitions:** Critical = HARD violation (blocks acceptance). Major = MEDIUM violation (requires revision or documented justification). Minor = SOFT violation (improvement opportunity).

---

## Finding Details

### CC-007: BUG-010 Acceptance Criteria Checklist Inconsistent With Implementation State [MAJOR]

**Principle:** P-022 (no deception about state of work) / general traceability expectation for worktracker entities (H-33-adjacent; `project-workflow.md` GitHub-issue-parity spirit extended to internal AC tracking)
**Location:** `BUG-010-ast-project-root.md` lines 84–115 (Acceptance Criteria) vs. lines 124–125 (History)
**Evidence:**
```
- [ ] `--root <path>` flag exists on all 10 `jerry ast` subcommands ...
- [ ] `jerry ast` commands accept files under `tempfile.gettempdir()` and `/tmp` ...
...
| 2026-08-07 | in_progress | ... GREEN after -- 149/149 in the two changed test files,
371/371 across ... ruff format --check and ruff check both exit 0. |
```
**Impact:** A reviewer scanning only the AC checklist (the conventional "is this bug done" signal) would conclude 7 of 9 scope-widening criteria remain outstanding, contradicting the prose immediately below it in the same document. This is an internal-consistency defect in the deliverable itself, not merely a cosmetic nit — it undermines the entity's function as the authoritative completion record and could cause a merge reviewer or the next agent picking up this bug to redo already-completed work, or conversely to merge believing less was verified than actually was.
**Dimension:** Internal Consistency
**Remediation:** Before merge, re-run the 7 unchecked ACs against the current branch state and check off every criterion that the test suite (confirmed present by this review) actually satisfies. If any of the 7 is genuinely NOT yet satisfied despite an existing same-named test, that test's assertions should be re-verified for correctness rather than assumed sufficient, and the discrepancy documented in History.

### CC-008: H-01 Ownership Gate Silently Bypassed When Project Root Coincides With a Shared Temp Path [MAJOR]

**Principle:** P-022 (no deception about protection delivered) — the checked-off `[x]` AC states the gate is "scoped strictly to temp-default matches, never the project root or an explicit `--root`," implying the carve-out is safe by construction; it is not, under the identified precondition.
**Location:** `src/interface/cli/ast_commands.py:181-209` (`_is_temp_default_root_match`), used at `ast_commands.py:342` inside `_check_path_containment`
**Evidence:**
```python
def _is_temp_default_root_match(
    matched_root: Path, allowed_roots: list[Path], explicit_root: str | None
) -> bool:
    if explicit_root is not None:
        return False
    return matched_root != allowed_roots[0]
```
`allowed_roots[0]` is always `get_project_root().resolve()` (`project_root.py:171`), which is `CLAUDE_PROJECT_DIR` or, absent that, `Path.cwd()` — with **no validation that this resolved directory is actually outside a shared/temp filesystem area**. If cwd is `/tmp` or a subdirectory of `tempfile.gettempdir()`, the "project root" and a "temp-default root" become the same (or an ancestor/descendant) path, and the ownership gate that exists specifically to protect shared-temp locations never fires for it.
**Impact:** In the specific scenario the RED-BUG010 assessment was built to close (CI runner / shared host, no `--root`, no env-var bypass, `jerry ast parse <other-user-temp-file>`), if the operator's shell session happens to be sitting in a scratch/temp working directory when `CLAUDE_PROJECT_DIR` is unset, the exact multi-tenant read/write exposure H-01 was designed to close reopens silently, with the checked-off AC providing false assurance that it is closed.
**Dimension:** Methodological Rigor
**Remediation:** Either (a) apply the ownership check whenever the *resolved* matched root is under `tempfile.gettempdir()` or `_HARDCODED_TMP`, regardless of whether it also happens to be `allowed_roots[0]` (test membership by path, not by list position), or (b) explicitly document this as an accepted residual risk (consistent with the project's existing pattern of documenting accepted risks, e.g., R-1/R-5 in the eng-lead plan) and add a regression test proving the documented behavior. Add a dedicated test: `CLAUDE_PROJECT_DIR` unset, `monkeypatch.chdir()` into a directory under a monkeypatched `tempfile.gettempdir()`, foreign-UID file — assert current (gap) or corrected (fixed) behavior explicitly, so this stops being an untested code path.

### CC-009: `ast_modify` Docstring Overstates Read/Write Containment-Set Agreement Guarantee [MINOR]

**Principle:** H-12 (docstring accuracy) / P-001 (truth/accuracy in generated claims)
**Location:** `src/interface/cli/ast_commands.py:637-657` (`ast_modify` docstring, `root` Args entry)
**Evidence:** `"Threaded identically into the read-time check and the write-time TOCTOU recheck below, so a single invocation never disagrees on the allowed containment set between read and write."`
**Impact:** Low — the claim is true for the argument value but implicitly assumes environment stability (`CLAUDE_PROJECT_DIR`, `tempfile.gettempdir()`, filesystem existence of `/tmp`) across the two calls, which is not disclaimed. Practically bounded by red-vuln's H-05 REFUTED verdict (atomic `mkstemp`/`os.replace`), so this is a wording-precision issue, not a functional defect.
**Dimension:** Evidence Quality
**Remediation:** Soften to: "...so a single invocation cannot disagree on the allowed containment set between read and write **due to the `root` argument itself** (the same value is threaded to both calls); the underlying allowed-roots set is otherwise a function of live environment state re-evaluated at each call."

---

## Remediation Plan

**P0 (Critical):** None.

**P1 (Major):** CC-007: Reconcile BUG-010 AC checklist with actual implementation/test state before merge. CC-008: Close or explicitly document-and-test the project-root/shared-temp-path coincidence gap in the H-01 ownership gate.

**P2 (Minor):** CC-009: Tighten the `ast_modify` `root` docstring wording to avoid overstating the read/write agreement guarantee.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | H-12 docstring coverage is complete (CC-004); no completeness gap found in the reviewed code. |
| Internal Consistency | 0.20 | Negative | CC-007 (Major): AC checklist directly contradicts the entity's own History narrative. |
| Methodological Rigor | 0.20 | Negative | CC-008 (Major): RED-BUG010 H-01 remediation has an unaddressed, untested edge case that reopens the exact exposure it was built to close. |
| Evidence Quality | 0.15 | Negative | CC-009 (Minor): docstring precision gap. CC-006 evidence-limited (no independent test execution this round — noted, not penalized as a violation). |
| Actionability | 0.15 | Neutral | All findings include specific file/line evidence and concrete remediation. |
| Traceability | 0.10 | Negative | CC-007 directly undermines the AC checklist's role as the traceability mechanism for this bug. |

**Constitutional Compliance Score:** `1.00 - (0.10*0 + 0.05*2 + 0.02*1) = 1.00 - 0.12 = 0.88`

**Threshold Determination:** **REVISE** (0.85–0.91 band; below the H-13 SSOT threshold of 0.92). Recommend targeted revision of the two Major items before this deliverable proceeds through the remaining tournament groups' consolidation; do not treat as REJECTED — the HARD architectural/typing/docstring/layering principles (H-05, H-07, H-10, H-11, H-12) are all clean, and both Major findings have narrow, well-scoped, cheap fixes.

---

## Execution Statistics

- **Total Findings:** 9 (6 COMPLIANT confirmations + 3 violations)
- **Critical:** 0
- **Major:** 2 (CC-007, CC-008)
- **Minor:** 1 (CC-009)
- **Protocol Steps Completed:** 5 of 5 (Load Constitutional Context → Enumerate Applicable Principles → Principle-by-Principle Evaluation → Remediation Guidance → Score Constitutional Compliance)

---

*S-007 execution — Group D, blind review, C4 tournament. No coordination with other adv-executor invocations in this tournament round.*
