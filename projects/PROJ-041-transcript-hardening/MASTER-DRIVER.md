# PROJ-041 Master Driver

> Self-contained orchestration prompt for driving PROJ-041-transcript-hardening to closure across many Claude Code sessions. Read this entire file at the start of every session before doing any work.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Mission](#mission) | What this project delivers |
| [Bootstrap](#bootstrap) | What to read in every fresh session |
| [Filesystem Reality Check](#filesystem-reality-check) | Detect uncommitted work, in-progress entities, recent commits |
| [Pick Work for this Session](#pick-work-for-this-session) | How to choose entities to open |
| [Execute Each Entity](#execute-each-entity) | The 9-step entity workflow |
| [Session-End Protocol](#session-end-protocol) | Checkpoint and handoff |
| [Cross-Session Constraints](#cross-session-constraints) | Rules that survive every clear |
| [Open Warnings](#open-warnings) | Known issues entity authors must address |
| [Out of Scope](#out-of-scope) | Things not to fix here |
| [Checkpoint Filename Convention](#checkpoint-filename-convention) | How to name session-checkpoint files |
| [Resume Prompt](#resume-prompt) | Three-line prompt to paste in every future session |

---

## Mission

Drive `EPIC-001-transcript-hardening` to closure. The Epic resolves the external `/transcript` skill audit (GitHub Issue #273) by:

- Vendoring ADR-007 from the jerry-core repository into this repo
- Promoting ADR-007 from PROPOSED to ACCEPTED
- Resolving 5 ADR contradictions (FEAT-002 Bugs)
- Building deterministic validators with a hardened SubprocessSandbox (FEAT-003)
- Extending schemas (FEAT-004)
- Hardening mindmap rendering (FEAT-005, including the bracket-escape "stop generating garbage" bug)
- Cross-cutting Enablers: DDD scaffolding, test harness, threat model, UX scoping, Diataxis docs, final review, final adversary tournament

Total scope: 36 parents (1 Epic, 5 Features, 7 Enablers, 16 Stories, 7 Bugs) + 215 Tasks + 3 Decisions.

This driver runs across MANY sessions. Each session does as much as it can within token limits, writes a checkpoint, and ends. The next session reads the checkpoint and continues.

---

## Bootstrap

At the start of EVERY session, in this exact order, before doing any work:

1. Read `projects/PROJ-041-transcript-hardening/PLAN.md` (project mission and scope)
2. Read `projects/PROJ-041-transcript-hardening/WORKTRACKER.md` (full hierarchy index)
3. Find and read the MOST RECENT session checkpoint per the [Checkpoint Filename Convention](#checkpoint-filename-convention) below.
4. Read `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/diagrams/dependencies-full.md` (the complete edge inventory; what is unblocked right now)
5. Read `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EPIC-001-transcript-hardening.md` (current child status rollup)
6. Read `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/audit-report-stories-only-20260430.md` (open warnings to honor; especially W-004 SPIDR review for 6 Stories with greater than 5 AC bullets)

Verify `JERRY_PROJECT` is set to `PROJ-041-transcript-hardening` per H-04. If unset, halt and ask the user.

---

## Filesystem Reality Check

A checkpoint may not capture the most recent state. Run these checks BEFORE picking work, after the bootstrap reads:

1. `git log --oneline -10` (run via Bash) — see commits since the checkpoint timestamp.
2. `git status --short` — see uncommitted work in the worktree.
3. Grep for entities currently in progress:
   - `grep -lr "^> \*\*Status:\*\* in_progress" projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/`
   - Also Grep for `Status: in_progress` (no blockquote prefix) in case a tool wrote a different style.
4. If `git status` shows uncommitted changes: investigate before continuing. These may be the prior session's in-flight work that needs to be either committed or abandoned per H-02 user authority. Do not silently overwrite.
5. If any entity is `status: in_progress`: that takes priority over starting new work. Finish it first.

Reconcile the bootstrap reads with the reality check. If commits or entity states diverge from the checkpoint, the checkpoint is stale. Trust the filesystem and update your understanding accordingly.

---

## Pick Work for this Session

After reality check is reconciled:

- If any entity is `in_progress`, finish it first.
- Otherwise pick the next set of unblocked entities from `dependencies-full.md`.
- Prefer parallel-safe groups (entities with no edges between them) so one session can close multiple items.
- Cap the session at one entity OR one parallel group. Do not open new work after the cap unless the prior items closed cleanly with token budget remaining.

If no work has been done yet (Wave 0), recommended starting set:

- BUG-006 (FEAT-005 mindmap bracket fix; the user's "stop generating garbage" quick win)
- BUG-007 (FEAT-005 mindmap false self-claim)
- STORY-001 (FEAT-001 vendor ADR-007; foundation that unblocks STORY-002, FEAT-002, FEAT-003)
- EN-001 (FEAT-003 DDD scaffolding)
- EN-002 (FEAT-003 test harness)

None of those block each other per the dependency graph.

---

## Execute Each Entity

For every entity selected, in dependency order:

1. **Open**: edit the entity's frontmatter `Status:` from `pending` to `in_progress`. Commit this change before starting the work. A fresh session detects in-flight work via the in_progress status, so the open commit must land before any work begins.
2. **Walk Agent Assignment**: execute the entity's Agent Assignment table top to bottom. Every row, every agent, in the prescribed order. Do not skip steps.
3. **BDD test-first** per H-20: write the failing test BEFORE any implementation. Red phase first. Never implement before the test fails.
4. **Quality gate**: at the prescribed gate, run `/adversary` C4 review at threshold greater than or equal to 0.95. This is a project-wide override. The SSOT default is 0.92; PROJ-041 uses 0.95.
5. **Persist outputs** per P-002: every agent's deliverable lands as a file inside the entity's directory. No agent output stays in conversation context only.
6. **Update Children Tasks** rows as each TASK completes: `pending` to `in_progress` to `completed`.
7. **Closure verification** per WTI-005: run `/worktracker` `wt-verifier` to confirm the artifact named in the AC actually exists at the path stated. No closure without delivery evidence.
8. **Close**: edit Status to `completed`. Update History with date, agents that ran, and a link to delivery evidence.
9. **H-32 parity**: if you discover a new defect or add a Story along the way, file a matching GitHub Issue against `geekatron/jerry` and link both directions (worktracker ID in the issue body, issue URL in the entity's Related Items).

Iterate: pick the next unblocked entity. Repeat steps 1 through 9. Continue until session is full or all reachable entities are closed.

---

## Session-End Protocol

Trigger: context fill nears 80 percent (per AE-006c CRITICAL or AE-006d EMERGENCY tier), OR you reach a natural break (entity closed and no in-progress work).

1. Stop picking new entities. If you are mid-flow on an entity and have token budget, finish it; otherwise note where you stopped.
2. Write a new session checkpoint per the [Checkpoint Filename Convention](#checkpoint-filename-convention).
3. The checkpoint must capture:
   - Branch name and HEAD SHA at session end
   - Commits this session (sha plus one-line summary, in chronological order)
   - Entities opened this session
   - Entities closed this session
   - Entities still `in_progress` with where execution stopped (e.g., "STORY-007 paused at Step 3, eng-qa tests written but Red phase not yet implemented")
   - Next-up unblocked entities for the next session
   - Any blockers requiring user input
   - Reference link to the previous checkpoint
4. Commit the checkpoint and any in-flight artifacts.
5. Tell the user what closed, what is next, and any blockers. Then end the session.

---

## Cross-Session Constraints

These survive every `/clear`. Honor them in every session:

- `/adversary` C4 review at threshold greater than or equal to 0.95 at every entity gate. No exceptions, no negotiation.
- BDD test-first per H-20. Never write implementation before a failing test.
- WTI-005 closure evidence required for every entity. The artifact must exist at the path the AC names.
- H-32 GitHub Issue parity for new defects and Stories you discover (against `geekatron/jerry`).
- Persist every agent output to project files per P-002.
- No skipping skills or quality gates. Execute governance IN ORDER.
- H-04: `JERRY_PROJECT` MUST be set before any work. Verify via `echo $JERRY_PROJECT`. If unset, halt and ask the user.
- H-05: UV-only Python (`uv run` for execution, `uv add` for dependencies). Never `python` or `pip` or `pip3`.
- H-31: Clarify before acting when the request is ambiguous. Do not assume.

---

## Open Warnings

You MUST address these when affected entities open:

| ID | Affected | Required Action |
|----|----------|-----------------|
| W-004 | STORY-005, STORY-007, STORY-008, STORY-009, STORY-012, STORY-015 | Acceptance Criteria bullet count is greater than 5. When opening any of these, run a SPIDR-style splitting review FIRST (Spike, Path, Interface, Data, Rules). Either split into sub-stories, or accept the scope with documented justification recorded in the Story's History section. |
| Stub Decision (FEAT-003) | STORY-009, STORY-010 | The hook mechanism Decision file `FEAT-003-deterministic-validation/DEC-001-hook-mechanism.md` is a stub. Resolve it (which mechanism: pre-commit hook, pipeline step, or post-write trigger?) before executing those Stories. |
| Stub Decision (FEAT-005) | BUG-007 | The capability-vs-claim-honesty Decision file `FEAT-005-mindmap-hardening/DEC-001-bug-007-capability-or-claim-honesty.md` is a stub. Resolve it (build the capability, or update prose to drop the unverified self-link claim?) before BUG-007 closes. |

---

## Out of Scope

These are open framework issues that affect this project but MUST NOT be fixed inside PROJ-041:

- GH #275 (schema validator silently skips Story files due to `^ST-` regex versus `STORY-` filename convention) — framework gap, deferred. The wt-auditor agent provides compensating coverage.
- GH #276 (no JSON Schemas for DEC, SPIKE, DISCOVERY, IMPEDIMENT entities) — framework gap, deferred.

If a fix to either gap would benefit your current entity, note the dependency in the entity's History and proceed without depending on the framework fix landing.

---

## Checkpoint Filename Convention

Format: `session-checkpoint-{YYYYMMDD}[-NN].md` placed under `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/`.

- First checkpoint of a calendar day: `session-checkpoint-{YYYYMMDD}.md` (no suffix).
- Same-day subsequent checkpoints: `session-checkpoint-{YYYYMMDD}-{NN}.md` where `NN` starts at `02` and increments.

To find the MOST RECENT checkpoint:

1. Glob `session-checkpoint-*.md` in the EPIC directory.
2. For each filename, extract:
   - `date_part` = the 8-digit YYYYMMDD substring
   - `suffix_part` = the optional NN integer following the date (default 1 if no suffix is present)
3. Sort the list by the tuple `(date_part, suffix_part)` in DESCENDING order.
4. The first entry is the most recent checkpoint.

Worked example. Suppose the EPIC directory contains:

- `session-checkpoint-20260430.md`
- `session-checkpoint-20260502.md`
- `session-checkpoint-20260502-02.md`
- `session-checkpoint-20260502-03.md`

Tuples: `(20260430, 1)`, `(20260502, 1)`, `(20260502, 2)`, `(20260502, 3)`. Sorted descending: `(20260502, 3)` first. The most recent is `session-checkpoint-20260502-03.md`.

If only one checkpoint exists, that is the most recent. If zero exist, this is the very first session — proceed without a prior checkpoint and note "no prior checkpoint found" in your bootstrap output to the user.

---

## Resume Prompt

Once this file is on disk, the resume prompt for every future session is just three lines. Paste this into Claude Code at the start of any new or cleared session:

```text
Working in: ~/workspace/GitHub/geekatron/jerry-wt/feat/PROJ-041-transcript-hardening
Project: PROJ-041-transcript-hardening

Resume per:
projects/PROJ-041-transcript-hardening/MASTER-DRIVER.md
```

Three lines. Always works. Survives `/clear`. Survives compaction. The full driver instructions live in this file, so they cannot be lost when context is truncated.

---

*Authored 2026-04-30 to replace the inline-pasted master driver pattern. This file is a project artifact, not a worktracker entity.*
