# Constitutional Compliance Report: BUG-010 Option C `jerry ast` Containment Redesign

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `eng-lead-option-c-plan.md` (design) + `src/interface/cli/{containment_policy.py, project_root.py, ast_commands.py, parser.py, main.py, adapter.py}` (implementation) + worktracker entity `BUG-010-ast-project-root.md` + GitHub Issue #337 / PR #341, branch `fix/BUG-010-ast-project-root` @ `cce557c5`
**Criticality:** C4 (adversarial tournament, security-relevant AE-005)
**Date:** 2026-08-10
**Reviewer:** adv-executor (blind S-007 pass, tournament Group 4/6 "Verify")
**Constitutional Context:** `docs/governance/JERRY_CONSTITUTION.md` (P-001–P-031), `.context/rules/quality-enforcement.md` (H-01–H-36 SSOT), `architecture-standards.md` (H-07, H-10), `coding-standards.md` (H-11, H-12), `testing-standards.md` (H-20, H-21), `project-workflow.md` (H-32)

---

## Summary

**PARTIAL compliance.** 2 Critical (H-32 GitHub Issue parity gap, H-07(c) infrastructure-instantiation-outside-bootstrap), 4 Major (stale worktracker Acceptance Criteria, undocumented DD-1–DD-4 owner sign-off, stale `RESUME-HERE.md` checkpoint, stale docstring contradicting the shipped security model). Constitutional compliance score: **0.60 (REJECTED, <0.85)**. The code implementation itself is materially sound (the six prior tournament Criticals are genuinely closed, per direct code inspection corroborating `eng-reviewer-optionc-gate-report.md`), but the surrounding governance/traceability artifacts (public GitHub Issue, worktracker Acceptance Criteria, resume checkpoint) have drifted out of sync with the Option C redesign, and one HARD architecture rule (H-07c) remains an unremediated, if disclosed, violation. **Recommendation:** REVISE the tracking artifacts before merge; the H-07(c) deviation requires an explicit governance decision (ADR-formalize-exception or route through `bootstrap.py`), not silent acceptance.

**Note on positive compliance (P-022):** The design plan itself demonstrates strong P-022 discipline in one respect worth crediting: Section 2 explicitly and proactively corrects a factual error in the task brief's stated config precedence/env-var name (`JERRY_AST_TRUSTED_ROOTS` → actual `JERRY_AST__TRUSTED_ROOTS`) rather than silently propagating it. This is the pattern the findings below ask to see applied consistently to the GitHub Issue, worktracker ACs, and resume checkpoint as well.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260810 | H-32: GitHub Issue parity ("Both MUST be kept in sync") | HARD | Critical | GitHub Issue #337 body still describes the original narrow bug and a proposed `JERRY_AST_REPO_ROOT` env var never implemented; zero mention of `ast.trusted_roots`, `--root`, `--quiet`, or the six-Critical tournament redesign | Traceability |
| CC-002-20260810 | H-07(c): "Only `src/bootstrap.py` SHALL instantiate infrastructure adapters" | HARD | Critical | `src/interface/cli/project_root.py:107-112` — `build_layered_config_adapter()` directly constructs `LayeredConfigAdapter` (infrastructure) from the interface layer, outside `bootstrap.py` | Methodological Rigor |
| CC-003-20260810 | P-010 (Task Tracking Integrity) / P-022 (No Deception) | HARD/MEDIUM | Major | `BUG-010-ast-project-root.md` AC checklist: `[x] H-01 ... temp-default-root match is additionally gated on file ownership` — but `_check_temp_root_ownership` no longer exists anywhere in `src/` (confirmed by grep); 8 further ACs describing the always-widen temp/scratchpad design remain listed unresolved with no note that Option C supersedes them | Internal Consistency |
| CC-004-20260810 | P-020 (User Authority) / P-004 (Explicit Provenance) | HARD/MEDIUM | Major | `eng-lead-option-c-plan.md:51-53` states DD-1–DD-4 sign-off is required "before eng-backend starts"; DD-2's "remove entirely" resolution is already implemented in shipped code (`cce557c5`) with no History entry or artifact recording owner approval | Traceability |
| CC-005-20260810 | P-022 (No Deception) / P-030 (Clear Handoffs) | MEDIUM | Major | `RESUME-HERE.md` (the designated compaction-resume pointer) still frames the open decision as binary Option A vs. Option B and states "Owner has NOT yet chosen. Do not start remediation until they do" — Option C (the path actually taken, implemented, tournament-cleared, and gate-approved) is never mentioned | Internal Consistency |
| CC-006-20260810 | H-12 (docstrings) / P-022 (No Deception) | MEDIUM | Major | `src/interface/cli/parser.py:578-580` (`_add_root_argument` docstring): "the default allowed roots are the user's project root plus OS temp/scratchpad directories" — describes the removed always-widen behavior; contradicts the correct `--help` text 3 lines below and the actual `get_containment_roots()` implementation | Internal Consistency |

**Finding ID Format:** `CC-{NNN}-20260810` (execution date used as the tournament-run identifier; this is a single-pass blind execution, no intra-run ID collisions expected).

**Severity Definitions:** Critical = HARD rule violated, blocks acceptance per H-13. Major = MEDIUM-tier / process-integrity gap requiring revision or documented justification. Minor = none found this pass.

---

## Finding Details

### CC-001: GitHub Issue #337 Not Synchronized With Option C Redesign (H-32) [CRITICAL]

**Principle:** H-32 — "all worktracker bugs, stories, enablers, and tasks MUST have a corresponding GitHub Issue... Both MUST be kept in sync." (`project-workflow.md`)

**Location:** GitHub Issue [#337](https://github.com/geekatron/jerry/issues/337) vs. `BUG-010-ast-project-root.md`, `eng-lead-option-c-plan.md`, and shipped code at `cce557c5`.

**Evidence:** Fetched Issue #337 directly. Its body describes only the original bug (`_get_repo_root()` anchoring to the plugin's own `__file__` tree) and proposes a three-tier precedence including an env var named `JERRY_AST_REPO_ROOT`. That env var was **never implemented** — the actual mechanism (per `project_root.py` and the shipped code) is `CLAUDE_PROJECT_DIR` plus, for the trusted-roots feature, `JERRY_AST__TRUSTED_ROOTS` (double underscore). The issue contains **zero** mention of: the PR #341 owner-directed scope widening, the C4 tournament (0.64 REVISE, six Critical findings), the Option C pivot, `ast.trusted_roots`, the `--root`/`--quiet` flags, or any of the security-hardening work now on the branch. By contrast, PR #341's own description (fetched independently) **is** accurately up to date through the `cce557c5` hardening commit — the drift is specific to the Issue, not the PR.

**Impact:** Issue #337 is the public, external collaboration surface for this work (public OSS repo `geekatron/jerry`). A contributor or user reading the issue today would form a materially wrong understanding of both the bug's actual final scope and the shipped fix's security model (e.g., they might attempt to set the never-implemented `JERRY_AST_REPO_ROOT` and get silently ignored behavior). This is exactly the failure mode H-32 exists to prevent, and it is a HARD rule regardless of whether the omission was intentional.

**Dimension:** Traceability.

**Remediation:** Before merging PR #341, update Issue #337's body (or add a synchronizing comment) to describe: (a) the scope widening directive from the owner review, (b) the pivot to Option C (`ast.trusted_roots` user-declared trust, not auto-widen), (c) the correct env var name `JERRY_AST__TRUSTED_ROOTS`, and (d) a link to the final `eng-reviewer-optionc-gate-report.md` verdict. Remove or correct the stale `JERRY_AST_REPO_ROOT` proposal so it is not mistaken for the shipped mechanism.

---

### CC-002: H-07(c) Composition-Root Violation in `project_root.build_layered_config_adapter()` [CRITICAL]

**Principle:** H-07(c) — "Only `src/bootstrap.py` SHALL instantiate infrastructure adapters." (`architecture-standards.md`, HARD)

**Location:** `src/interface/cli/project_root.py:81-112`

**Evidence:**
```python
def build_layered_config_adapter(defaults: dict[str, Any]) -> Any:
    ...
    from src.infrastructure.adapters.configuration.layered_config_adapter import (
        LayeredConfigAdapter,
    )

    ...
    return LayeredConfigAdapter(
        env_prefix="JERRY_",
        root_config_path=root / ".jerry" / "config.toml",
        project_config_path=project_config_path,
        defaults=defaults,
    )
```
`LayeredConfigAdapter` is an infrastructure adapter (`src/infrastructure/adapters/configuration/`). This function directly instantiates it from `src/interface/cli/` — not `src/bootstrap.py`. `adapter.py::CLIAdapter._create_config_adapter()` now delegates to this same factory (the plan's DD-4 refactor is already implemented), so the entire CLI config-read path funnels through this one non-bootstrap instantiation site.

**Impact:** This is a literal, direct violation of a stated HARD rule with no carve-out in `architecture-standards.md`'s text. The design plan (Section 1, lines 61-67) and `eng-reviewer-optionc-gate-report.md` (L1 Architecture Verification) both **disclose** this as a "pre-existing, precedented exception" rather than hiding it — which is good P-022 practice — but disclosure does not satisfy H-13's "HARD violation blocks acceptance" criterion, and the plan actively **adds a new instantiation site** (`project_root.build_layered_config_adapter()` is a new function introduced by this deliverable) rather than merely inheriting the old one unchanged. Characterizing this as "not one newly introduced by this plan" (plan line 65-67) is accurate for the *pattern* but understates that a *new call site* was created.

**Dimension:** Methodological Rigor.

**Remediation:** This requires an explicit governance decision, not silent continuation: (1) file an ADR formally carving out a documented CLI-configuration exception to H-07(c) (the codebase clearly has an established, repeated need for CLI namespaces to read config without a full bootstrap wiring pass), or (2) route `LayeredConfigAdapter` construction through `bootstrap.py` and inject it into the CLI layer. Option (1) is pragmatic given the pattern predates this bug fix and is now used identically by both `jerry ast` and `jerry config`; it should not remain an implicit, un-adjudicated "precedent."

---

### CC-003: Worktracker Acceptance Criteria Certify a Deleted Feature as Done (P-010/P-022) [MAJOR]

**Principle:** P-010 (Task Tracking Integrity — "Never mark tasks complete without evidence") and P-022 (No Deception — accuracy of represented state).

**Location:** `BUG-010-ast-project-root.md`, Acceptance Criteria section, line 104.

**Evidence:**
```
- [x] H-01 (RED-BUG010, CWE-552/CWE-668/CWE-281): a temp-default-root
      match is additionally gated on file ownership ...
```
Directly confirmed absent from the current codebase:
```
grep -r "_check_temp_root_ownership" src/   → no matches
```
The Option C design (`eng-lead-option-c-plan.md`, DD-2, "Remove entirely (default recommendation)") explicitly recommends deleting this exact function, and the shipped code has done so. The AC checkbox that certifies it as done (`[x]`) now certifies the existence of code that has been intentionally removed. Separately, 8 further unchecked ACs (lines 85-103) describe the always-widen temp/scratchpad default and the ownership-gate design point-by-point — the entire design surface these describe was superseded by Option C, but nothing in the entity marks them superseded, struck through, or reconciled. The `History` table's most recent entry (line 125) predates the Option C pivot entirely.

**Impact:** A reader (human or agent) auditing BUG-010 via the worktracker entity alone — the internal SSOT per `project-workflow.md` — would conclude the H-01 ownership-gate mitigation is live in production. It is not; Option C removed it by design (the ownership gate's rationale no longer applies once temp is never auto-trusted). This is a real accuracy gap in the SSOT for a security-relevant bug, not a cosmetic one.

**Dimension:** Internal Consistency.

**Remediation:** Add a `History` entry documenting the Option C pivot and its rationale. Uncheck or strike through the H-01 AC with a note "Superseded by Option C — ownership gate removed by design (DD-2); the underlying risk is dissolved because temp/scratchpad is no longer auto-trusted." Add a new AC block (or a synthesis note) covering the six C4-tournament Criticals actually closed under Option C, replacing the now-obsolete temp-widening AC list rather than leaving both side by side.

---

### CC-004: DD-1–DD-4 Owner Sign-off Gate Not Documented as Satisfied Before Implementation (P-020/P-004) [MAJOR]

**Principle:** P-020 (User Authority — "Never override user decisions") and P-004 (Explicit Provenance — "audit trail of actions taken").

**Location:** `eng-lead-option-c-plan.md`, L0 Executive Summary (lines 51-53) and Section 7 (lines 495-502), vs. shipped code at `cce557c5`.

**Evidence:** The plan states as a precondition: "Key standards decisions requiring explicit sign-off before eng-backend starts: see Section 7 — most consequential is DD-2 (remove vs. retain the ownership gate for configured roots)." Section 7 lists DD-1 through DD-4 with recommendations, framed as decisions the **owner** must confirm. The shipped code already reflects the recommended resolution of all four: DD-1 (broad-root warning extended to `configured` roots — implemented in `project_root.py:234-242`), DD-2 (ownership gate fully removed), DD-3 (`quiet=True` hardcoded at the `ast_modify` write-time recheck — implemented at `ast_commands.py:635`), and DD-4 (`adapter.py` refactored to call the shared factory — implemented). No `History` entry in the BUG-010 entity, and no artifact in the BUG-010 folder, records that the owner reviewed and approved DD-1–DD-4 before this implementation proceeded.

**Impact:** Two possible explanations exist and this report cannot distinguish them from the artifacts alone: (a) sign-off was obtained through a channel that was never persisted (a P-002/P-004 documentation gap), or (b) implementation proceeded past a self-declared human-approval gate without it (a P-020 risk). Given the plan's own text makes this an explicit precondition, the absence of any confirming record is itself a finding regardless of which explanation is true.

**Dimension:** Traceability.

**Remediation:** Add a `History` entry (or a dedicated `DD-Signoff.md`) recording the owner's actual decision on each of DD-1–DD-4, with a date and, ideally, a quote or reference to where the decision was made. If sign-off in fact has not yet occurred, this should be surfaced to the owner explicitly before PR #341 merges, since DD-2 in particular (removing a security control) is exactly the class of decision P-020 exists to protect.

---

### CC-005: `RESUME-HERE.md` Checkpoint Stale Relative to the Option C Decision (P-022/P-030) [MAJOR]

**Principle:** P-022 (No Deception) and P-030 (Clear Handoffs — "document current state completely").

**Location:** `RESUME-HERE.md`, lines 22-28.

**Evidence:**
```
## THE OPEN DECISION (owner must choose before eng-backend remediates)
**How to remediate:**
- (A) Environment-gated redesign ...
- (B) Patch the current always-widen model ...
Owner has NOT yet chosen. Do not start remediation until they do.
```
This file is explicitly designed as "Checkpoint for resuming after session compaction. Read this first." The actual remediation path taken — Option C, "user-declared trusted roots" — is a third path, distinct from both A and B as framed, and is now fully implemented, tournament-scored, red-team re-checked, and gate-approved (per `eng-reviewer-optionc-gate-report.md`, dated the same day as this review). `RESUME-HERE.md` was never updated to reflect this.

**Impact:** Given Jerry's stated core design purpose is context-rot mitigation via exactly this kind of checkpoint file (per `CLAUDE.md`: "Persist state to files; load selectively"), a stale checkpoint is a direct hit against the framework's own foundational design goal. An agent or human resuming from this file today would be misdirected into re-litigating an A-vs-B decision that was already superseded weeks ago by a superior C option.

**Dimension:** Internal Consistency.

**Remediation:** Update `RESUME-HERE.md` to reflect: the decision made (Option C), where its full design lives (`eng-lead-option-c-plan.md`), its current status (gate-approved, PR #341 pending owner merge), and remove or clearly mark obsolete the "Owner has NOT yet chosen" language.

---

### CC-006: Stale Docstring Misstates the Shipped Security Model (H-12/P-022) [MAJOR]

**Principle:** H-12 (docstring accuracy) and P-022 (No Deception).

**Location:** `src/interface/cli/parser.py:578-580`.

**Evidence:**
```python
def _add_root_argument(parser: argparse.ArgumentParser) -> None:
    """... Without this flag, the default allowed
    roots are the user's project root plus OS temp/scratchpad directories
    (see ``project_root.get_containment_roots``).
    ...
    """
```
This directly contradicts (a) the correct `--help` text three lines below in the same function (`"...project-root + configured-trusted-root allowed set"`), (b) `project_root.py`'s own module docstring, and (c) the actual runtime behavior verified in `get_containment_roots()` (no temp/scratchpad path is ever part of the default set). This is independently corroborated by `eng-reviewer-optionc-gate-report.md` finding F-1, confirmed here via direct code read for this blind pass.

**Impact:** On a security-relevant CLI surface, an internally inconsistent docstring (correct `--help` text, incorrect docstring three lines above it, in the same function) creates exactly the kind of documentation-vs-behavior mismatch P-022 exists to prevent, even though — as `eng-reviewer` correctly notes — it has no runtime impact since it is not user-facing output.

**Dimension:** Internal Consistency.

**Remediation:** Replace lines 578-580 with: "Without this flag, the default allowed roots are the user's project root plus zero-or-more user-declared `ast.trusted_roots` entries (no directory is auto-trusted; OS temp/scratchpad directories are never part of the default set)." (Matches the fix eng-reviewer already specified.)

---

## Recommendations

**P0 (Critical):**
- CC-001: Synchronize GitHub Issue #337 with the Option C redesign before PR #341 merges.
- CC-002: File an ADR formalizing (or eliminating) the H-07(c) CLI-config exception; do not leave it as an un-adjudicated "precedent."

**P1 (Major):**
- CC-003: Reconcile/strike-through the stale worktracker Acceptance Criteria; add a History entry for the Option C pivot.
- CC-004: Record explicit owner sign-off for DD-1–DD-4 (or surface the gap to the owner now).
- CC-005: Update `RESUME-HERE.md` to reflect the Option C decision and current gate-approved status.
- CC-006: Fix the stale `_add_root_argument` docstring in `parser.py` (already independently identified by `eng-reviewer` as F-1; corroborated here).

**P2 (Minor):** None identified this pass.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No findings directly affect completeness of the technical design or test coverage (both independently verified strong by `eng-reviewer-optionc-gate-report.md`) |
| Internal Consistency | 0.20 | Negative | CC-003, CC-005, CC-006: worktracker ACs, resume checkpoint, and a docstring all contradict the actual shipped design in different ways |
| Methodological Rigor | 0.20 | Negative | CC-002: unremediated H-07(c) HARD rule violation, newly-sited by this deliverable |
| Evidence Quality | 0.15 | Neutral | Design plan and code are well-evidenced; the gap is in surrounding governance artifacts, not evidence quality of the technical work itself |
| Actionability | 0.15 | Neutral | All findings carry specific file:line locations and concrete remediation |
| Traceability | 0.10 | Negative | CC-001, CC-004: the public GitHub Issue and the owner-sign-off audit trail are both broken traceability chains for a C4/security-relevant change |

**Constitutional Compliance Score:** `1.00 - (0.10 * 2 + 0.05 * 4) = 1.00 - 0.40 = 0.60`

**Threshold Determination:** REJECTED (< 0.85 band; well below the H-13 SSOT threshold of 0.92). The two Critical findings are governance/traceability gaps around an otherwise materially sound technical redesign, not defects in the containment logic itself — both are remediable without touching `containment_policy.py` or the closed security findings.

---

*S-007 Constitutional AI Critique — blind pass, C4 tournament Group 4/6 (Verify). Sources consulted directly: `eng-lead-option-c-plan.md`, `src/interface/cli/{containment_policy.py, project_root.py, ast_commands.py, parser.py, main.py, adapter.py}`, `BUG-010-ast-project-root.md`, `RESUME-HERE.md`, `eng-reviewer-optionc-gate-report.md`, `docs/governance/JERRY_CONSTITUTION.md`, `.context/rules/{quality-enforcement.md, architecture-standards.md, coding-standards.md, testing-standards.md, project-workflow.md}`, GitHub Issue #337, GitHub PR #341 (via WebFetch). Persisted per P-002.*
