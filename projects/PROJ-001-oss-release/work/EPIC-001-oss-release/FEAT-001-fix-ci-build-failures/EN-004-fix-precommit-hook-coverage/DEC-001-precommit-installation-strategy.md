# EN-004:DEC-001: Pre-commit Hook Installation Strategy

> **Type:** decision
> **Status:** SUPERSEDED
> **Priority:** HIGH
> **Created:** 2026-02-11
> **Parent:** EN-004
> **Owner:** Adam Nowak
> **Related:** BUG-010

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of decision |
| [Decision Context](#decision-context) | Background and constraints |
| [Evidence](#evidence) | Research findings and data |
| [Decisions](#decisions) | Structured decision entries |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Changes |

---

## Summary

Decision on the pre-commit hook installation strategy for BUG-010. Research revealed that a comprehensive installation mechanism already exists via `make setup` (Makefile lines 16-22), documented in CONTRIBUTING.md (lines 11-30) and INSTALLATION.md (lines 374-407). The session start hook's detect-and-warn behavior (`scripts/session_start_hook.py` lines 104-139) is intentional and appropriate.

**Decisions Captured:** 3

**Key Outcomes:**
- BUG-010's original framing ("auto-install needed") is incorrect — the installation mechanism already exists
- The session start hook warning should be improved to reference `make setup`
- BUG-010 is reclassified from "missing auto-install" to "improve warning message"

---

## Decision Context

### Background

BUG-010 was filed with the assumption that the session start hook should auto-install pre-commit hooks when they are missing, because `check_precommit_hooks()` only warns without taking remediation action. However, systematic research using /problem-solving agents (ps-investigator, ps-researcher) revealed:

1. **`Makefile` (lines 16-22):** A `setup` target already exists that runs `uv sync` + `uv run pre-commit install`. This is the documented first-time setup mechanism.
2. **`Makefile` (line 24):** An `install` alias points to `setup`.
3. **`Makefile` (lines 76-77):** A dedicated `pre-commit-install` target exists for re-installation.
4. **`CONTRIBUTING.md` (lines 11-30):** Documents `make setup` as the **REQUIRED first step** after cloning.
5. **`CONTRIBUTING.md` (lines 67-85):** Documents `make setup` for git worktree workflows, notes hooks are shared across worktrees.
6. **`INSTALLATION.md` (lines 374-407):** Documents `make setup` in the "For Developers" section.
7. **Session start hook (lines 104-139):** Detection-only by design. Warning message says `"Run 'uv run pre-commit install' to install hooks."` — references the raw command but not `make setup`.

### Constraints

- Must not add surprising side effects to session start hook
- Must not duplicate existing installation infrastructure
- Warning message should reference the canonical setup mechanism
- Solution must work for both macOS/Linux (`make`) and Windows (`uv run` directly)

---

## Evidence

### Evidence Table

| # | Source | Finding | Impact |
|---|--------|---------|--------|
| E-1 | `Makefile:16-22` | `setup` target: `uv sync` + `uv run pre-commit install` | Installation mechanism already exists |
| E-2 | `Makefile:24` | `install: setup` alias | Multiple entry points to same mechanism |
| E-3 | `Makefile:76-77` | `pre-commit-install` dedicated target | Granular control available |
| E-4 | `CONTRIBUTING.md:11-30` | "First-Time Setup (REQUIRED)" documents `make setup` | Onboarding documentation exists |
| E-5 | `CONTRIBUTING.md:36-56` | Windows equivalent: `uv sync && uv run pre-commit install` | Cross-platform documented |
| E-6 | `CONTRIBUTING.md:67-85` | Worktree setup: `make setup` in new worktree | Edge case documented |
| E-7 | `INSTALLATION.md:374-407` | Developer setup section documents `make setup` | Installation guide exists |
| E-8 | `scripts/session_start_hook.py:104-139` | `check_precommit_hooks()` detect-and-warn only | Session hook is detection layer, not installation layer |
| E-9 | `scripts/session_start_hook.py:134-137` | Warning says `"Run 'uv run pre-commit install'"` | Warning references raw command, not `make setup` |
| E-10 | `pyproject.toml:116` | `pre-commit>=4.5.1` in dev dependencies | pre-commit is a managed dependency |
| E-11 | `.pre-commit-config.yaml:6-7` | Header comment says `pip install pre-commit` | Contradicts UV-only mandate (minor issue) |

### Research Method

Two parallel /problem-solving agents were used:
- **ps-investigator:** 5W2H analysis of pre-commit hook installation infrastructure
- **ps-researcher:** Analysis of pre-commit configuration and file type coverage

---

## Decisions

### D-001: Close BUG-010 as "won't fix" — installation mechanism already exists

**Date:** 2026-02-11
**Participants:** Adam Nowak, Claude

#### Question/Context

BUG-010 proposed auto-installing pre-commit hooks in the session start hook when they are missing. Research revealed that `make setup` already handles this, and it is documented in CONTRIBUTING.md and INSTALLATION.md. Should we:
- (A) Auto-install hooks in the session start hook anyway?
- (B) Close BUG-010 — the existing `make setup` mechanism is sufficient?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Auto-install in session hook** | Add `subprocess.run(["uv", "run", "pre-commit", "install"])` to `check_precommit_hooks()` | Fully automatic; zero user action needed | Surprising side effect during session start; duplicates `make setup`; adds subprocess call to every session; makes session hook an installer instead of a detector; muddies separation of concerns |
| **B: Close BUG-010 (Recommended)** | Acknowledge that `make setup` is the correct installation mechanism | Respects existing architecture; no code changes needed; clean separation of concerns (Makefile = setup, hook = detection) | Requires developers to read CONTRIBUTING.md (which they should) |

#### Decision

**We decided:** Option B — Close BUG-010 as "won't fix." The `make setup` target in the Makefile is the correct and documented installation mechanism. The session start hook's detect-and-warn role is intentional and appropriate.

#### Rationale

1. **Installation infrastructure exists** (E-1 through E-7) — `make setup`, `make install`, `make pre-commit-install` all provide hook installation.
2. **Documentation is comprehensive** (E-4, E-5, E-6, E-7) — CONTRIBUTING.md, INSTALLATION.md, and the Makefile help text all document the setup process.
3. **Separation of concerns** — The session start hook is a detection layer (E-8). Making it an installer conflates two responsibilities.
4. **Side effect risk** — Running `subprocess.run` during every session start adds latency and potential failure modes for zero benefit when hooks are already installed.
5. **The original bug was based on incomplete research** — The Makefile was not examined before filing BUG-010, leading to a wrong conclusion that no installation mechanism existed.

#### Implications

- **Positive:** No unnecessary code changes; respects existing architecture; corrects a false premise
- **Negative:** None — the existing mechanism is working as intended
- **Follow-up:** D-002 (improve warning message to reference `make setup`)

---

### D-002: Improve session hook warning to reference `make setup`

**Date:** 2026-02-11
**Participants:** Adam Nowak, Claude

#### Question/Context

The current warning message (E-9) says `"Run 'uv run pre-commit install' to install hooks."` This is technically correct but bypasses the documented setup mechanism. Should the warning reference `make setup` instead?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Reference make setup (Recommended)** | Change warning to suggest `make setup` as the primary action | Aligns with CONTRIBUTING.md; provides the documented happy path; `make setup` also runs `uv sync` | Assumes `make` is available (not on Windows) |
| **B: Keep current message** | Leave warning as-is: `"Run 'uv run pre-commit install'"` | No changes needed; works cross-platform | Doesn't reference the documented setup mechanism; misses `uv sync` step |
| **C: Dual message** | Suggest `make setup` with `uv run pre-commit install` as fallback | Cross-platform; covers both documented paths | Slightly longer message |

#### Decision

**We decided:** Option C — Update the warning to reference both `make setup` (primary) and `uv run pre-commit install` (fallback for Windows/no-make environments).

#### Rationale

1. **Alignment with documentation** — CONTRIBUTING.md documents `make setup` as the required first step, and the Windows alternative as the fallback.
2. **Completeness** — `make setup` also runs `uv sync`, ensuring dependencies are installed before hooks.
3. **Cross-platform** — Providing both commands covers macOS/Linux (make) and Windows (direct uv commands).

#### Proposed Warning Text

```
Pre-commit hooks are NOT installed. Tests will not run before commits.
Run 'make setup' to install dependencies and hooks.
(Windows: uv sync && uv run pre-commit install)
```

#### Implications

- **Positive:** Warning aligns with documented workflow; minor 1-line change
- **Negative:** None identified
- **Follow-up:** Update `.pre-commit-config.yaml` header comment (E-11) to use `uv run pre-commit install` instead of `pip install pre-commit` (minor UV-mandate compliance)

---

### D-003: Override D-001 — auto-install hooks on session start

**Date:** 2026-02-21
**Participants:** Adam Nowak

#### Decision

User overrides D-001 per P-020 (User Authority). The session start hook
MUST auto-install pre-commit hooks when they are missing, rather than
only warning. This ensures all worktrees get hooks installed automatically
on first Claude Code session.

#### Rationale

1. In practice, `make setup` was never run after creating worktrees
2. All 6 active worktrees had no hooks installed — the detection-only
   approach failed to achieve its goal
3. Auto-install during session start is low-risk: `pre-commit install`
   only creates hook shims (<2s), does not download environments

#### Implementation

- `check_precommit_hooks()` now accepts `uv_path` parameter
- When hooks are missing and `uv_path` is available, runs `uv run pre-commit install`
- On success: returns info message
- On failure/timeout: falls back to warning with manual instructions
- No `--install-hooks` flag: hook environments are created lazily on first commit

#### Implications

- **Positive:** All worktrees get hooks automatically; zero developer action required
- **Negative:** Adds a subprocess call on session start when hooks are missing (~2s one-time cost)
- **Supersedes:** D-001 (detection-only approach)

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Close BUG-010 as "won't fix" — installation mechanism already exists via `make setup` | 2026-02-11 | SUPERSEDED (by D-003) |
| D-002 | Improve session hook warning to reference `make setup` with Windows fallback | 2026-02-11 | ACCEPTED |
| D-003 | Override D-001 — auto-install hooks on session start (P-020 User Authority) | 2026-02-21 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-004](./EN-004-fix-precommit-hook-coverage.md) | Fix Pre-commit Hook Coverage |
| Feature | [FEAT-001](../FEAT-001-fix-ci-build-failures.md) | Fix CI Build Failures |
| Bug | [BUG-010](./BUG-010-session-hook-no-auto-install.md) | Session start hook warns but doesn't auto-install |
| File | `Makefile` | Setup target (lines 16-22) |
| File | `CONTRIBUTING.md` | Developer setup documentation (lines 11-30) |
| File | `INSTALLATION.md` | Installation guide (lines 374-407) |
| File | `scripts/session_start_hook.py` | Session start hook (lines 104-139) |
| File | `.pre-commit-config.yaml` | Pre-commit configuration (header comment) |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-11 | Claude | Created decision document with two decisions: D-001 (close BUG-010) and D-002 (improve warning message). Based on ps-investigator and ps-researcher findings. |
| 2026-02-21 | Claude | Added D-003: User override of D-001 per P-020. Auto-install hooks on session start. D-001 status changed to SUPERSEDED. |

---

## Metadata

```yaml
id: "EN-004:DEC-001"
parent_id: "EN-004"
work_type: DECISION
title: "Pre-commit Hook Installation Strategy"
status: SUPERSEDED
priority: HIGH
created_by: "Claude"
created_at: "2026-02-11"
updated_at: "2026-02-21"
decided_at: "2026-02-11"
participants: ["Adam Nowak", "Claude"]
tags: ["pre-commit", "makefile", "session-hook", "installation"]
decision_count: 3
superseded_by: "D-003"
supersedes: null
```
