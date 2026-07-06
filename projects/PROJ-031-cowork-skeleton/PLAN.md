# PROJ-031-cowork-skeleton — Plan

> Distribute Jerry as a Claude CoWork plugin via a derived, projects-stripped `cowork-skeleton` branch kept in sync with `main` by CI.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Problem](#problem) | Why this project exists |
| [Goals](#goals) | What success looks like |
| [Confirmed Decisions](#confirmed-decisions) | The three decided approaches |
| [Scope](#scope) | What is in scope |
| [Out of Scope](#out-of-scope) | What is excluded |
| [Worktracker](#worktracker) | Pointer to the decomposition |
| [Status](#status) | Current phase |

---

## Problem

Jerry cannot install as a plugin in Claude CoWork (Claude Desktop) because the repository exceeds CoWork's plugin-load limit of approximately 5,000 files. The `projects/` folder accounts for 4,600 of 6,344 tracked files (72%). Until the repository fits under the limit, CoWork users cannot install Jerry.

---

## Goals

- Produce a distributable Jerry that loads in Claude CoWork under the ~5,000-file limit.
- Keep the distribution automatically in sync with `main` without manual repository surgery.
- Preserve a working fresh install (bootstrap and H-04 active-project requirement satisfiable out of the box).
- Ship the security hardening and user documentation needed to make the distribution safe and usable.

---

## Confirmed Decisions

> These three decisions were agreed with the user and are not re-litigated here.

1. **Derived skeleton branch.** Produce a `cowork-skeleton` branch that is the Jerry repo with `projects/` stripped (tracked files drop from ~6,344 to ~1,744, well under 5,000), keeping a **minimal `projects/` stub** — an empty `projects/` plus a README guiding users to create their own project so H-04 and bootstrap work on a fresh install.

2. **CI automation (regenerate, never merge).** Development happens on normal feature branches and merges to `main`. A GitHub Actions workflow **regenerates** the skeleton from `main` (checkout `main`, remove `projects/`, add stub, commit, force-push to `cowork-skeleton`) on each release. Default trigger: GitHub Release published plus manual `workflow_dispatch`.

3. **User documentation (Diataxis).** Capture tutorial, how-to, reference, and explanation documentation in the repo and publish it to the MkDocs site.

---

## Scope

- Deterministic, idempotent skeleton generation (strip `projects/`, add minimal stub) with file-count and plugin-load validation.
- GitHub Actions CI that regenerates the skeleton from `main` and force-pushes `cowork-skeleton`, with least-privilege token and branch-protection strategy.
- Red-team STRIDE threat model of the derived-branch CI plus eng-team remediations.
- Diataxis user documentation (tutorial, how-to, reference, explanation) wired into MkDocs.
- Orchestrated `/adversary` C4 quality gate (>= 0.95) across deliverables.

---

## Out of Scope

- The actual implementation of the `projects/` strip logic and CI workflow code (this project scaffolds the tracking artifacts; implementation is later work).
- Changing how Jerry stores or structures `projects/` on `main`.
- Alternative distribution channels (e.g., packaging Jerry outside the CoWork plugin model).
- Migrating existing user projects into the skeleton.

---

## Worktracker

See [WORKTRACKER.md](./WORKTRACKER.md) for the full entity decomposition (1 Epic, 3 Features, 2 Enablers, 9 Stories, 5 Tasks).

---

## Status

**Phase:** Active (scaffolding complete; implementation not started)
