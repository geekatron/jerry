# Use Case Scenarios: Jerry CLI Output Path Resolver (GH #144)

> Cockburn casual format (BULLETED_OUTLINE). Five use cases at USER_GOAL goal level.
> Primary reference: GitHub issue #144 -- Deterministic Output Path Resolver.
> Produced by: uc-author (Jerry /use-case skill).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Background](#background) | Feature context and actors |
| [UC-PATH-001](#uc-path-001-configure-custom-output-root) | User configures custom output root |
| [UC-PATH-002](#uc-path-002-agent-resolves-output-path-at-invocation-time) | Agent resolves output path at invocation time |
| [UC-PATH-003](#uc-path-003-migrate-existing-outputs-from-legacy-locations) | User migrates existing outputs from legacy locations |
| [UC-PATH-004](#uc-path-004-skill-author-registers-output-path-pattern) | Skill author registers output path pattern |
| [UC-PATH-005](#uc-path-005-orchestrator-provides-engagement-base-path) | Orchestrator provides engagement base path |
| [Acceptance Criteria Map](#acceptance-criteria-map) | UC-to-AC traceability |

---

## Background

**Feature:** Replace LLM-interpreted 4-priority output path resolution in Jerry agents with a deterministic Python CLI command (`jerry path resolve`).

**Problem:** 89+ agents across 15+ skills each resolve their output path by prompting the LLM to follow a 4-priority chain (explicit path > base path > configured default > hardcoded fallback). This is probabilistic and inconsistent. Agents silently produce outputs at wrong locations, especially when `JERRY_PROJECT` is unset or caller context is missing.

**Solution scope:** A CLI subcommand (`jerry path resolve`) that takes caller context as structured arguments and emits a single, canonical output path. Agents call this command deterministically instead of asking the LLM to guess.

**Actors:**

| Actor | Description |
|-------|-------------|
| Framework User | Developer invoking Jerry skills to produce deliverables |
| Skill Author | Developer writing new Jerry agents or updating existing ones |
| Orchestrator | Main Claude Code session coordinating multi-agent workflows |
| Jerry CLI | The `jerry` Python command-line tool (supporting actor / system) |

---

## UC-PATH-001: Configure Custom Output Root

**ID:** UC-PATH-001
**Goal level:** USER_GOAL (!)
**Primary actor:** Framework User
**Scope:** Jerry CLI -- project output path configuration
**Trigger:** Framework User wants skill outputs to land in a directory other than `projects/${JERRY_PROJECT}/`.

### Main Success Scenario

1. Framework User sets a custom output root via the Jerry project configuration (e.g., `jerry config set output.root /custom/path`).
2. Jerry CLI persists the setting to the active project's configuration store.
3. Framework User invokes any Jerry skill as normal.
4. The skill's agent calls `jerry path resolve` to determine its output path.
5. Jerry CLI returns a path rooted under the custom output root instead of the default project-relative path.
6. The agent writes its artifact to the resolved path; the file appears in the user-configured location.

### Extensions

- At step 1: `JERRY_PROJECT` is not set -- Jerry CLI exits with a clear error: "No active project. Set JERRY_PROJECT or run `jerry projects use <id>`."
- At step 1: Provided path does not exist -- Jerry CLI asks whether to create it or rejects with an actionable message.
- At step 5: `output.root` is set but the domain subdirectory cannot be inferred -- Jerry CLI applies the default subdirectory convention and logs which fallback was used.

### Acceptance Criteria

- AC-001-1: `jerry config set output.root <path>` persists the path to the active project config.
- AC-001-2: All subsequent `jerry path resolve` calls for the project return paths rooted under the configured root.
- AC-001-3: Setting `output.root` does not affect other projects.
- AC-001-4: Removing the setting restores default `projects/${JERRY_PROJECT}/` behaviour.

---

## UC-PATH-002: Agent Resolves Output Path at Invocation Time

**ID:** UC-PATH-002
**Goal level:** USER_GOAL (!)
**Primary actor:** Orchestrator (acting on behalf of an agent)
**Scope:** Jerry CLI -- deterministic path resolution for agent output
**Trigger:** An agent is about to write a deliverable and needs to know where to write it.

### Main Success Scenario

1. Orchestrator assembles agent caller context: explicit output path (if provided by user), base path (if provided), domain, and artifact slug.
2. Orchestrator invokes the agent, passing caller context as structured fields in the agent prompt.
3. Agent calls `jerry path resolve --explicit <path> --base <base> --domain <domain> --slug <slug>` before writing output.
4. Jerry CLI evaluates the 4-priority resolution chain deterministically: explicit path > base path > project-configured default > framework fallback.
5. Jerry CLI emits exactly one resolved absolute path on stdout with exit code 0.
6. Agent writes its artifact to the emitted path; no LLM interpretation of path resolution is required.

### Extensions

- At step 3: `--explicit` path is provided but is not within the active project tree -- Jerry CLI warns and proceeds (P-020: does not override user intent).
- At step 4: `JERRY_PROJECT` is not set and no explicit or base path was provided -- Jerry CLI falls back to `work/` and logs a deprecation notice: "JERRY_PROJECT unset; output landing in work/ (legacy). Set JERRY_PROJECT to use project-relative paths."
- At step 4: All four priorities are absent -- Jerry CLI exits non-zero with: "Cannot resolve output path: no explicit path, base path, project config, or JERRY_PROJECT found."
- At step 5: Resolved path's parent directory does not exist -- Jerry CLI creates it (or returns the path with a `--mkdir` flag; agent decides).

### Acceptance Criteria

- AC-002-1: `jerry path resolve` with an explicit path returns that path unchanged.
- AC-002-2: With no explicit path but a base path provided, returns `<base>/<slug>`.
- AC-002-3: With neither explicit nor base path, returns a path under the project-configured output root.
- AC-002-4: With no configuration at all, returns a path under `work/` and exits with a non-zero warning code.
- AC-002-5: Output is a single line on stdout; no extra whitespace or debug output.
- AC-002-6: The command is idempotent: calling it twice with the same arguments returns the same path.

---

## UC-PATH-003: Migrate Existing Outputs from Legacy Locations

**ID:** UC-PATH-003
**Goal level:** USER_GOAL (!)
**Primary actor:** Framework User
**Scope:** Jerry CLI -- output migration from `skills/*/output/` to project-relative paths
**Trigger:** Framework User has outputs produced by pre-migration agents in `skills/*/output/` and wants them in project-relative paths per ADR-EPIC002-001.

### Main Success Scenario

1. Framework User runs `jerry path migrate --dry-run` to see which files would be moved.
2. Jerry CLI scans `skills/*/output/` directories, resolves the correct project-relative destination for each file, and prints a move plan.
3. Framework User reviews the plan and confirms (or adjusts individual destinations).
4. Framework User runs `jerry path migrate` to execute the moves.
5. Jerry CLI moves each file to its resolved destination, creating parent directories as needed.
6. Jerry CLI prints a migration summary: files moved, files skipped (already at correct location), errors.
7. Framework User verifies deliverables are at expected paths and deletes the now-empty `skills/*/output/` directories.

### Extensions

- At step 2: No files found under `skills/*/output/` -- Jerry CLI reports "No legacy output files found. Migration not needed." and exits 0.
- At step 2: A file's destination cannot be inferred (e.g., no `JERRY_PROJECT` hint in the file path or frontmatter) -- Jerry CLI marks it as `UNRESOLVED` in the plan; user must provide a destination manually.
- At step 5: Destination file already exists -- Jerry CLI skips the move and reports a conflict; does not overwrite without `--force`.
- At step 5: Move fails (permissions, path too long) -- Jerry CLI logs the error, continues remaining moves, and reports all failures in the summary.

### Acceptance Criteria

- AC-003-1: `jerry path migrate --dry-run` prints a move plan without touching the filesystem.
- AC-003-2: Each planned move shows: source path, destination path, and status (READY / UNRESOLVED / CONFLICT).
- AC-003-3: `jerry path migrate` executes only the READY moves from the plan.
- AC-003-4: No file is overwritten without an explicit `--force` flag.
- AC-003-5: Migration summary counts: moved, skipped, errors -- all non-zero counts are highlighted.

---

## UC-PATH-004: Skill Author Registers Output Path Pattern

**ID:** UC-PATH-004
**Goal level:** USER_GOAL (!)
**Primary actor:** Skill Author
**Scope:** Jerry agent definition -- output path declaration for new agents
**Trigger:** Skill Author is creating a new agent and needs to declare where its outputs go so `jerry path resolve` honours the agent's intended destination.

### Main Success Scenario

1. Skill Author creates a new agent definition file under `skills/{name}/agents/`.
2. Skill Author declares `output.location` in the agent's `.governance.yaml` using the project-relative template pattern: `projects/${JERRY_PROJECT}/{subdir}/{filename_pattern}`.
3. Skill Author calls `jerry path validate-agent skills/{name}/agents/{agent}.governance.yaml` to verify the declaration is valid.
4. Jerry CLI parses the governance file, validates `output.location` against the path pattern schema, and exits 0 with "Output path declaration: VALID".
5. At runtime, when the agent calls `jerry path resolve`, the resolver reads the agent's registered pattern as the project-configured default (Priority 3), filling in runtime values.
6. Skill Author confirms in a smoke test that the agent's output lands at the expected path.

### Extensions

- At step 2: Skill Author omits `output.location` but sets `output.required: true` -- Jerry CLI validation fails with: "output.location is required when output.required is true."
- At step 3: Governance file fails schema validation for unrelated reasons -- Jerry CLI reports all validation errors; path validation is one item in the list.
- At step 5: `${JERRY_PROJECT}` is not set at runtime -- resolver falls back to Priority 4 (`work/`) and logs a warning as in UC-PATH-002 extension.
- At step 5: Agent receives an explicit path from the caller -- explicit path (Priority 1) overrides the registered pattern.

### Acceptance Criteria

- AC-004-1: `output.location` in `.governance.yaml` accepts `projects/${JERRY_PROJECT}/` prefix templates.
- AC-004-2: `jerry path validate-agent` exits 0 when `output.location` matches the required pattern.
- AC-004-3: `jerry path validate-agent` exits non-zero and names the specific violation when `output.location` uses a disallowed pattern (e.g., `skills/*/output/`).
- AC-004-4: At runtime, `jerry path resolve` with no explicit or base path uses the agent's registered `output.location` as the default.
- AC-004-5: An explicit caller-provided path always takes precedence over the registered default.

---

## UC-PATH-005: Orchestrator Provides Engagement Base Path

**ID:** UC-PATH-005
**Goal level:** USER_GOAL (!)
**Primary actor:** Orchestrator
**Scope:** Jerry CLI -- multi-agent output co-location under a single engagement directory
**Trigger:** Orchestrator is coordinating multiple agents for a single engagement and wants all outputs grouped under one directory (e.g., `projects/PROJ-030-bugs/research/engagement-20260413/`).

### Main Success Scenario

1. Orchestrator determines the engagement directory path for this workflow run.
2. Orchestrator passes the engagement path as `--base <engagement-dir>` in each agent's invocation prompt.
3. First agent calls `jerry path resolve --base <engagement-dir> --slug <artifact-slug>` and receives `<engagement-dir>/<artifact-slug>`.
4. Agent writes its artifact to the resolved path.
5. Second agent (invoked by orchestrator) calls `jerry path resolve --base <engagement-dir> --slug <artifact-slug-2>` and receives `<engagement-dir>/<artifact-slug-2>`.
6. Both artifacts are co-located under the engagement directory; orchestrator can reference them by stable paths without needing to track per-agent output locations.

### Extensions

- At step 2: Orchestrator does not provide `--base` for one agent -- that agent falls back to Priority 3 (project default) or Priority 4 (`work/`); the artifact is not co-located. Orchestrator detects this when the returned path does not share the engagement directory prefix.
- At step 3: `<engagement-dir>` does not exist -- Jerry CLI creates it (equivalent to `mkdir -p`) before returning the path.
- At step 6: Two agents produce outputs with the same slug -- `jerry path resolve` returns the same path for both, causing a collision; agents must use distinct slugs. Jerry CLI does not detect this at resolve time (it resolves paths, not file contents).

### Acceptance Criteria

- AC-005-1: `jerry path resolve --base <dir> --slug <slug>` returns `<dir>/<slug>` regardless of `JERRY_PROJECT` or project config.
- AC-005-2: `--base` overrides the project-configured default (Priority 3) but is itself overridden by `--explicit` (Priority 1).
- AC-005-3: All agents in the same orchestration session receiving the same `--base` value produce outputs under the same directory.
- AC-005-4: `jerry path resolve` with `--base` creates the base directory if absent (or accepts a `--mkdir` flag to control this behaviour).

---

## Acceptance Criteria Map

> Traceability from use case to acceptance criteria. Each row is one AC from the use cases above.

| AC ID | Use Case | Criterion Summary | Testable? |
|-------|----------|-------------------|-----------|
| AC-001-1 | UC-PATH-001 | `jerry config set output.root` persists to project config | Yes -- check config file |
| AC-001-2 | UC-PATH-001 | All `jerry path resolve` calls return paths under configured root | Yes -- compare path prefix |
| AC-001-3 | UC-PATH-001 | Setting does not affect other projects | Yes -- multi-project fixture |
| AC-001-4 | UC-PATH-001 | Unsetting restores default behaviour | Yes -- before/after comparison |
| AC-002-1 | UC-PATH-002 | Explicit path returned unchanged | Yes -- exact string comparison |
| AC-002-2 | UC-PATH-002 | Base + slug = resolved path | Yes -- string concatenation check |
| AC-002-3 | UC-PATH-002 | Falls back to project-configured root | Yes -- mock project config |
| AC-002-4 | UC-PATH-002 | Falls back to `work/` with warning when unconfigured | Yes -- capture stderr |
| AC-002-5 | UC-PATH-002 | Single line stdout, no extra whitespace | Yes -- stdout parsing |
| AC-002-6 | UC-PATH-002 | Idempotent: same args return same path | Yes -- two calls, compare |
| AC-003-1 | UC-PATH-003 | Dry-run does not touch filesystem | Yes -- snapshot before/after |
| AC-003-2 | UC-PATH-003 | Plan shows source, destination, status per file | Yes -- output format check |
| AC-003-3 | UC-PATH-003 | Only READY entries are moved | Yes -- verify UNRESOLVED/CONFLICT untouched |
| AC-003-4 | UC-PATH-003 | No overwrite without `--force` | Yes -- conflict fixture |
| AC-003-5 | UC-PATH-003 | Summary shows moved/skipped/error counts | Yes -- count comparison |
| AC-004-1 | UC-PATH-004 | `output.location` accepts project-relative templates | Yes -- schema validation pass |
| AC-004-2 | UC-PATH-004 | `validate-agent` exits 0 for valid pattern | Yes -- exit code check |
| AC-004-3 | UC-PATH-004 | `validate-agent` exits non-zero for disallowed pattern | Yes -- exit code + message |
| AC-004-4 | UC-PATH-004 | Registered default used when no explicit/base path | Yes -- integration test |
| AC-004-5 | UC-PATH-004 | Explicit path overrides registered default | Yes -- priority test |
| AC-005-1 | UC-PATH-005 | `--base` + `--slug` = `<base>/<slug>` | Yes -- string comparison |
| AC-005-2 | UC-PATH-005 | `--base` overridden by `--explicit` | Yes -- priority test |
| AC-005-3 | UC-PATH-005 | All agents with same `--base` co-locate outputs | Yes -- multi-agent fixture |
| AC-005-4 | UC-PATH-005 | Base directory created if absent | Yes -- filesystem check |

---

*Use Case Author: uc-author (Jerry /use-case skill) | Detail level: BULLETED_OUTLINE*
*Goal level: All use cases are USER_GOAL (!) -- what the actor achieves in one session.*
*Target: GitHub Issue #144 -- Jerry CLI Output Path Resolver*
*Date: 2026-04-13*
