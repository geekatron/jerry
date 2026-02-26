# GitHub Issue Draft: Extract Project Tracker from Plugin Repository

## Title

Extract project tracker to its own repo — 67% of tracked content is operational state that doesn't belong in the framework

## Labels

enhancement

## Body

**Related:** Part of PROJ-001 OSS release preparation. H-32 worktracker parity maintained.

### The problem

The `projects/` directory ships with the Jerry plugin repository. Every user who clones the Jerry framework repository gets 41 MB of operational project data they didn't ask for and will never use. 2,413 files. 635,075 lines. Fourteen project directories spanning oss-release planning, security research, agent pattern development, and article drafts. This is the framework author's workbench, not the framework.

**Relative impact:** The Jerry framework's git-tracked content totals 60 MB across 3,791 files. The `projects/` directory is 41 MB (67% by size) and 2,413 files (63% by count). Remove `projects/` and the framework is 19 MB and 1,378 files — the actual tools, skills, and code that make Jerry work.

Your plugin cache should be a quiver, not a garage sale. Ship the skis, not the trip journal.

**Distribution mechanism:** Jerry ships as a Claude Code plugin via the `.claude-plugin/` manifest. When users install Jerry through Claude Code's plugin system, the plugin installation performs a full `git clone` of the repository — including `projects/`. The `projects/` directory is not excluded by any distribution filter, `.gitattributes` export-ignore, or plugin manifest include/exclude rule. (Verified: inspected `.claude-plugin/` manifest and `.gitattributes` — no path exclusion rules present as of this writing.) Every plugin installation includes the full 41 MB of project data in the working tree, plus the git object store overhead from the clone.

### Data

| Metric | Value |
|--------|-------|
| Total Jerry repo (git-tracked) | 60 MB, 3,791 files |
| `projects/` directory | 41 MB, 2,413 files |
| Framework without `projects/` | 19 MB, 1,378 files |
| `projects/` as % of tracked content | 67% by size, 63% by file count |
| Total lines in `projects/` | 635,075 (`git ls-files projects/ \| xargs wc -l`) |
| Project directories | 14 (11 with content, 2 empty shells, 1 README) |
| Largest project (PROJ-001 oss-release) | 21 MB |

**Per-project breakdown:**

| Project | Size | Description |
|---------|-----:|-------------|
| PROJ-001 oss-release (`PROJ-001-oss-release/`) | 21 MB | OSS release preparation |
| PROJ-005 markdown-ast | 4.5 MB | AST-based markdown manipulation |
| PROJ-008 agentic-security | 3.2 MB | Security-first agentic platform |
| PROJ-009 llm-deception-research | 3.1 MB | LLM deception patterns research |
| PROJ-007 agent-patterns | 2.7 MB | Agent design patterns and routing |
| PROJ-010 cyber-ops | 2.1 MB | Eng-team and red-team skills |
| PROJ-011 saucer-boy-articles | 1.9 MB | Saucer Boy voice articles |
| PROJ-004 context-resilience | 1.9 MB | Context exhaustion detection |
| PROJ-003 je-ne-sais-quoi | 1.7 MB | Personality and voice layer |
| PROJ-006 multi-instance | 372 KB | Multi-instance Claude management |
| PROJ-001 oss-documentation (`PROJ-001-oss-documentation/`) | 232 KB | Documentation companion |
| PROJ-002 roadmap-next | 204 KB | Future capabilities planning |
| PROJ-020 oss-contributions | 0 KB | Empty shell |
| PROJ-001 plugin-cleanup (`PROJ-001-plugin-cleanup/`) | 0 KB | Empty shell |

**Note on PROJ-001 naming:** Three filesystem directories use the PROJ-001 prefix: `PROJ-001-oss-release/`, `PROJ-001-oss-documentation/`, and `PROJ-001-plugin-cleanup/`. These are separate sub-projects under the PROJ-001 umbrella — the naming convention evolved organically during early development. The directory names (shown in parentheses above) are the disambiguating identifiers.

None of this is framework code. It's operational state — PLAN.md files, WORKTRACKER.md manifests, entity files, orchestration artifacts, research outputs, decision records. The worktracker skill that reads and manages these files stays in Jerry. The data it operates on does not need to.

### What stays, what goes

| Component | Stays in Jerry | Moves out |
|-----------|:-:|:-:|
| `skills/worktracker/` (skill code, rules, agents) | X | |
| `skills/worktracker/rules/` (behavior rules, directory structure standards) | X | |
| `.context/rules/project-workflow.md` | X | |
| `src/domain/` and `src/infrastructure/` code that references `projects/` paths | X | |
| `projects/README.md` — stub pointing to external repo | X | |
| `projects/PROJ-*` directories (all project data) | | X |

### Affected components

The following code paths reference `projects/` and must be verified post-migration:

- [**`src/domain/markdown_ast/document_type.py`**](https://github.com/geekatron/jerry/blob/main/src/domain/markdown_ast/document_type.py#L98-L106) (path patterns at lines 98-106): `projects/*/WORKTRACKER.md`, `projects/*/work/**/*.md`, `projects/*/PLAN.md`, `projects/*/ORCHESTRATION_PLAN.md`, `projects/*/decisions/*.md`, `projects/*/analysis/*.md`, `projects/*/research/*.md`, `projects/*/synthesis/*.md`
- [**`src/infrastructure/adapters/configuration/layered_config_adapter.py`**](https://github.com/geekatron/jerry/blob/main/src/infrastructure/adapters/configuration/layered_config_adapter.py): Project config loading via `projects/PROJ-*/.jerry/config.toml`
- **`jerry projects list|context|validate` CLI commands**: Must handle absent `projects/` gracefully
- **`.context/rules/` reference files**: Informational provenance references to project artifacts (e.g., ADR sources citing `projects/PROJ-007-agent-patterns/...`)
- **GitHub Actions CI pipeline**: Any test steps that assume `projects/` exists

**Governance note:** This change formalizes the physical separation between the framework (tools, skills, code) and the framework author's workbench (project data, research artifacts, orchestration outputs). The conceptual distinction already exists in [worktracker directory structure standards](https://github.com/geekatron/jerry/blob/main/skills/worktracker/rules/worktracker-directory-structure.md) as the project-based vs. repository-based placement patterns. An ADR documenting this architectural separation decision SHOULD be created in `docs/design/`.

### Alternatives considered

| Approach | Description | Decision |
|----------|-------------|----------|
| Git submodule | `projects/` becomes a tracked submodule pointing to jerry-projects. Versioned dependency, no OS symlink required. | Rejected: submodule content is NOT included in a plain `git clone` (solving the distribution size problem), but the development workflow creates friction: contributors must run `git submodule update --init` after cloning or use `git clone --recurse-submodules`; uninitialized submodules appear as empty directories. More importantly, every change to `jerry-projects` requires a separate commit in Jerry to update the submodule pointer — ongoing maintenance overhead the symlink bridge avoids entirely. |
| Inline with `git subtree add` | Keep `projects/` inline in Jerry using `git subtree add` for bidirectional sync, but mark it clearly as non-framework content. | Rejected: Does not reduce installation size. All project data remains in the Jerry repository. The problem is the data being there, not how it's tracked. (Note: this is distinct from `git subtree split`, which is used in the selected approach for one-time history extraction.) |
| `.gitignore` only (no external repo) | Gitignore `projects/` and let the framework author maintain their projects locally without any repository. | Rejected: Loses git history for project data. The framework author's projects have meaningful commit history (decision records, phase synthesis outputs, orchestration artifacts) that should be preserved. |
| Sparse checkout | Keep `projects/` in Jerry but document that plugin users should enable sparse checkout to exclude it. | Rejected: Requires user action post-clone. Does not solve the default installation size problem. Adds complexity without benefit for most users who should never see `projects/` at all. |
| **Symlink bridge (selected)** | Move to external repo; symlink back for framework author development. Plugin users get no `projects/` directory. | **Selected:** Cleanest separation. Framework author retains full access to project data via a one-time symlink setup. Plugin users are completely unaffected — the directory simply does not exist. History is preserved in the external repository. |

### Proposed strategy: symlink bridge

Move `projects/` to a dedicated repository (`geekatron/jerry-projects`). For the framework author's development environment, symlink the external repo back to `projects/` in the Jerry working tree. For plugin users, the `projects/` directory simply doesn't exist — they create their own project data wherever they want.

Three phases. Same as any good line: scout the terrain, read the features, commit to the exit.

**Proposed symlink setup (framework author):**

```
jerry/                          # Main plugin repo
  projects/ -> <path-to-jerry-projects>/   # Symlink to external repo
  skills/worktracker/           # Skill code stays here
  src/                          # Framework code stays here
```

**Windows note:** Symlink creation requires Developer Mode enabled or Administrator privileges (`mklink /D projects <path-to-jerry-projects>`). Contributors on Windows SHOULD use WSL2 or a directory junction (`mklink /J`) as an alternative. Directory junctions do not require elevated privileges.

**Plugin user experience (no projects/ directory):**

Users who adopt Jerry's worktracker skill create projects in their own repositories using the repository-based placement pattern already defined in [`skills/worktracker/rules/worktracker-directory-structure.md`](https://github.com/geekatron/jerry/blob/main/skills/worktracker/rules/worktracker-directory-structure.md). The `projects/` directory pattern is the project-based placement variant used by the framework author — plugin users are not expected to use it.

### Implementation

**Phase 1: Prepare**
- **Repository visibility decision:** Create `geekatron/jerry-projects` as a **private** repository. Rationale: `projects/` contains security research artifacts (PROJ-008 agentic-security, PROJ-009 llm-deception-research) and OSS release planning that may include pre-release architectural decisions. Making this data public requires a deliberate content review of each project directory — that review is out of scope for this issue. Default to private; reassess visibility after content review.
- Create `git tag pre-extraction-$(date +%Y%m%d)` in Jerry before any history operations. This is the rollback checkpoint.
- Extract `projects/` history using `git subtree split --prefix=projects/ HEAD -b projects-split`, then push to the new repo: `git push <jerry-projects-remote> projects-split:main`. This is the recommended approach — it creates a new branch in the Jerry repo containing only the `projects/` history without modifying Jerry's main history. Avoid `git filter-branch` (deprecated since Git 2.24). Alternative: if `git-filter-repo` is preferred, first create a disposable clone to avoid operating on the live repository: `git clone <jerry-repo-path> /tmp/jerry-projects-extract && cd /tmp/jerry-projects-extract && git-filter-repo --path projects/ --subdirectory-filter projects/ && git remote add origin <jerry-projects-remote> && git push origin main`. **Do NOT run `git-filter-repo` directly in the Jerry working directory without a `--source` flag — it will rewrite Jerry's history, removing all non-`projects/` files. This is irreversible.**
- **Pre-flight checks** (run before the irreversible steps below):
  - `git remote -v` — confirm the correct `<jerry-projects-remote>` is configured before push
  - `git status --short` — confirm staging area is clean before `git rm -r --cached`
  - `git log --oneline -5` — confirm you are on the correct branch before any history operations
- Remove `projects/PROJ-*` directories from Jerry's git tracking: `git rm -r --cached projects/PROJ-*`
- Add `projects/PROJ-*` to Jerry's `.gitignore`
- Update `projects/README.md` to a stub: "Project data has moved to `geekatron/jerry-projects`. Framework author: see `docs/development/project-tracker-setup.md` for symlink configuration. Plugin users: use the worktracker skill to create projects in your own repositories."
- Document the symlink setup in `docs/development/project-tracker-setup.md`. Minimum content:
  1. **Prerequisites:** git clone of `geekatron/jerry-projects` to a local path
  2. **macOS/Linux setup:** `ln -s <path-to-jerry-projects> <path-to-jerry>/projects`
  3. **Windows setup (Developer Mode):** `mklink /D projects <path-to-jerry-projects>` (from Jerry root)
  4. **Windows alternative (no elevated privileges):** `mklink /J projects <path-to-jerry-projects>` (directory junction)
  5. **WSL2 alternative:** Use the macOS/Linux instructions inside WSL2
  6. **Verification:** `ls -la projects/` should show the symlink pointing to the external repo
  7. **Note:** The symlink is local to your machine — it is not tracked by git and must be recreated on each fresh clone
- Publish migration notice: add CHANGELOG entry documenting that `projects/PROJ-*` directories are no longer tracked in Jerry as of this commit. Existing contributors with local clones: run `git pull` to receive the removal. If you have local uncommitted changes in `projects/`, they are now untracked and preserved locally.

**Rollback procedure:** If the migration fails validation (Phase 3), revert using the pre-extraction tag:
1. `git tag -l | grep pre-extraction` — identify the checkpoint
2. `git reset --hard <pre-extraction-tag>` — restore Jerry to pre-migration state
3. Force-push only if the migration was already pushed to remote. Before force-pushing to main: (a) check for open PRs against the migration commit — `gh pr list --base main` — and close or re-target them; (b) verify branch protection rules permit force-push (temporary bypass may be required — re-enable immediately after); (c) inform any collaborators of the force-push — collaborators who pulled the migration commit must run `git fetch origin && git rebase origin/main` to realign their local branches with the restored history. GitHub does not automatically update PR base branches on force-push.
4. Delete the `jerry-projects` repo if it was already created, provided no external collaborators have cloned it. The repo will be private; deletion is clean if only the framework author has access. Confirm before deleting.

Do NOT remove the pre-extraction tag until Phase 3 validation gates pass and at least one full CI cycle succeeds on main.

**Phase 2: Update references**
- Audit all `projects/` path references in `.context/rules/` files (scope: run `grep -r 'projects/' .context/rules/ | wc -l` to get the reference count before starting) — these are informational references to source artifacts (ADR provenance, phase synthesis outputs). They remain valid as historical references but the files will resolve only when the symlink is in place. **Decision: keep the references as-is.** They document provenance and do not functionally depend on reading project files at runtime. The rule files describe where knowledge originated, not where to find it now.
- Verify `src/domain/markdown_ast/document_type.py` path patterns work correctly through a symlink. **Technical note:** `fnmatch.fnmatch()` operates on path strings, not filesystem lookups — it will match regardless of symlinks. The question is whether the path strings produced by `pathlib.Path.glob()` or `os.walk()` traversal include or exclude the symlink resolution. On macOS/Linux, `pathlib.Path.glob()` follows symlinks by default (Python 3.9-3.12 behavior; Python 3.13+ adds an explicit `follow_symlinks` parameter). This must be tested, not assumed.
- Verify `src/infrastructure/adapters/configuration/layered_config_adapter.py` project config loading works through symlinks.
- Verify `jerry projects list|context|validate` CLI commands work with the symlink in place and handle the absence of `projects/` for plugin users. **Note:** This graceful handling also covers the framework author's fresh clone before symlink setup — the experience should be identical to the plugin user case until the symlink is configured.
- Update GitHub Actions CI pipeline to ensure no test step assumes `projects/` exists. CI runs on a clean checkout without any symlink — CI MUST pass in this configuration. Add a CI comment or `.github/workflows/` annotation documenting that `projects/` is intentionally absent in CI.

**Phase 3: Validate**
- Jerry test suite passes with the symlink in place (framework author environment)
- Jerry test suite passes without `projects/` directory (plugin user environment / CI)
- `jerry projects list` with no `projects/` directory MUST return exit code 0 with a human-readable informational message (e.g., "No projects directory found. Use the worktracker skill to create projects in your repository."). It MUST NOT return a non-zero exit code or Python traceback.
- `jerry projects context` and `jerry projects validate` follow the same pattern: exit 0 with informational message when `projects/` is absent.
- Worktracker skill operates correctly on repository-based project placement (no `projects/` dependency)
- Plugin installation size reduced by >= 40 MB. Measurement: create two fresh clone directories — (1) `git clone <jerry-repo> /tmp/jerry-post && du -sh /tmp/jerry-post` (post-extraction HEAD); (2) `git clone <jerry-repo> /tmp/jerry-pre && cd /tmp/jerry-pre && git checkout <pre-extraction-tag> && du -sh /tmp/jerry-pre` (pre-extraction state). The size difference should be >= 40 MB. Fresh clone size represents what plugin users actually receive.
- Git clone time and disk usage reduced for new contributors

### Acceptance criteria

- [ ] `geekatron/jerry-projects` private repository created with history extracted from `projects/`. History preservation guarantee: per-file `git log` and `git blame` for files within `projects/` are preserved; commit SHAs will differ from Jerry's; cross-directory commit context (commits touching both `projects/` and framework files) is split across the two repos. Repository URL added to this issue after creation.
- [ ] Pre-extraction git tag created before any history operations
- [ ] `projects/PROJ-*` removed from Jerry's git tracking and added to `.gitignore`
- [ ] `projects/README.md` stub remains in Jerry, pointing to external repo and setup docs
- [ ] Symlink setup documented in `docs/development/project-tracker-setup.md` (macOS/Linux symlink, Windows junction alternative)
- [ ] All path references in `.context/rules/` audited; kept as historical provenance (documented)
- [ ] `document_type.py` path patterns verified to work through symlinks (test added with symlinked fixture)
- [ ] `layered_config_adapter.py` project config loading verified through symlinks (test added)
- [ ] `jerry projects list|context|validate` CLI commands return exit 0 with informational message when `projects/` is absent (test added)
- [ ] GitHub Actions CI pipeline updated to pass without `projects/` directory; no test step assumes its presence
- [ ] Full test suite passes in both environments (with symlink, without `projects/`)
- [ ] Plugin installation size reduced by >= 40 MB (measured via fresh `git clone` comparison — see Phase 3 measurement method)
- [ ] CHANGELOG entry published with migration notice for existing contributors
- [ ] Rollback procedure documented and pre-extraction tag preserved until validation passes
- [ ] Repository visibility confirmed as private; content review and long-term visibility reassessment deferred to a separate issue. Reassess when: (a) Jerry reaches first public OSS release with active external contributors, or (b) a second maintainer is added — whichever comes first.

### Why now

Jerry is preparing for open-source release (see [OSS Release milestone](https://github.com/geekatron/jerry/milestone/1)). Every megabyte of operational state that ships with the plugin is a megabyte that says "this framework is still a personal project." The `projects/` directory is 67% of all git-tracked content — two-thirds of the repository is someone else's project plans. Extracting it before the OSS release is the right sequence — do it now, while the audience is small, rather than after public users have cloned 41 MB of the framework author's planning artifacts.

The mountain doesn't care about your trip journal. But your pack weight cares a lot.
