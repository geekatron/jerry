# GitHub Issue Draft — EPIC-001 Jerry CoWork Skeleton Distribution

> Ready-to-post GitHub issue for the PROJ-031 initiative (worktracker Epic EPIC-001). Per H-32, this jerry-repo Epic requires a corresponding GitHub Issue. Do NOT auto-create — the maintainer posts this via `gh`.

## Document Sections

| Section | Purpose |
|---------|---------|
| [How to Use This Draft](#how-to-use-this-draft) | Posting instructions |
| [Proposed Title](#proposed-title) | Issue title |
| [Proposed Labels](#proposed-labels) | Suggested labels |
| [Issue Body](#issue-body) | Copy-paste markdown body |

---

## How to Use This Draft

1. Review the title, labels, and body below.
2. Create the issue, e.g.: `gh issue create --title "<title>" --body-file <(sed -n '/^## Issue Body/,$p' this-file)` — or simply copy the [Issue Body](#issue-body) section into a new issue.
3. After creation, add `GitHub Issue: [#N](url)` to EPIC-001's Related Items and record the issue number in `WORKTRACKER.md` (H-32 parity).

---

## Proposed Title

`[EPIC] Jerry CoWork Skeleton Distribution — projects-stripped branch + CI sync (PROJ-031 / EPIC-001)`

---

## Proposed Labels

`epic`, `enhancement`, `distribution`, `ci`, `documentation`, `security`

---

## Issue Body

### Problem

Jerry cannot install as a plugin in Claude CoWork (Claude Desktop) because the repository exceeds CoWork's plugin-load limit of approximately 5,000 files. The `projects/` folder accounts for **4,600 of 6,344 tracked files (72%)**. Until the repository fits under the limit, CoWork users cannot install Jerry.

### Requirements

1. **Skeleton generation** — Produce a distributable Jerry that loads in CoWork under the ~5,000-file limit by stripping `projects/`, while keeping a minimal `projects/` stub so a fresh install still bootstraps (H-04).
2. **CI sync automation** — Keep the distribution automatically in sync with `main` on each release, without manual repository surgery, using a least-privilege, security-reviewed workflow.
3. **User documentation** — Provide Diataxis documentation (tutorial, how-to, reference, explanation) published to the MkDocs site so users can install and maintain the skeleton unaided.

### Confirmed Approach

1. **Derived skeleton branch.** Create a `cowork-skeleton` branch that is the Jerry repo with `projects/` stripped (tracked files drop from ~6,344 to ~1,744, well under 5,000), keeping a **minimal `projects/` stub** (empty `projects/` plus a README guiding users to create their own project so H-04/bootstrap work on a fresh install).
2. **CI automation (regenerate, never merge).** Development happens on normal feature branches and merges to `main`. A GitHub Actions workflow **regenerates** the skeleton from `main` (checkout `main`, remove `projects/`, add stub, commit, force-push to `cowork-skeleton`) on each release. Default trigger: GitHub Release published plus manual `workflow_dispatch`.
3. **User documentation (Diataxis).** Capture tutorial/how-to/reference/explanation in the repo and publish to the MkDocs site.

### Acceptance Criteria

- [ ] A generated `cowork-skeleton` has fewer than 5,000 tracked files (~1,744 expected).
- [ ] The skeleton still loads as a CoWork plugin: `.claude-plugin/`, `skills/`, `.claude/`, and `.context/` are intact.
- [ ] The skeleton ships a minimal `projects/` stub with a user-guidance README; a fresh install bootstraps and can set an active project (H-04).
- [ ] Skeleton generation is deterministic and idempotent (same `main` commit yields identical output).
- [ ] A GitHub Actions workflow regenerates the skeleton from `main` and force-pushes `cowork-skeleton` on Release published and on manual `workflow_dispatch` (regenerate, never merge).
- [ ] The workflow uses a least-privilege token and a documented branch-protection strategy; it refuses to publish when the acceptance gate fails and notifies on failure.
- [ ] A red-team STRIDE threat model of the derived-branch CI is produced (force-push, token/secrets, supply-chain) with eng-team remediations; no unmitigated critical or high findings remain.
- [ ] Diataxis tutorial, how-to, reference, and explanation are written and published in the MkDocs site navigation.
- [ ] Deliverables pass an orchestrated `/adversary` C4 quality gate at >= 0.95.

### Worktracker Reference

- **Epic:** `EPIC-001` — Jerry CoWork Skeleton Distribution
- **Project:** `PROJ-031-cowork-skeleton`
- **Decomposition:** 3 Features (Skeleton Generation, Security & Threat Model, User Documentation), 2 Enablers (CI Sync Automation, Adversarial Quality Gate), 9 Stories, 5 Tasks.
- **Manifest:** `projects/PROJ-031-cowork-skeleton/WORKTRACKER.md`
- **Plan:** `projects/PROJ-031-cowork-skeleton/PLAN.md`

> Per H-32, child work items (Features, Enablers, Stories, Tasks) also require their own GitHub Issues linked back to their worktracker IDs.
