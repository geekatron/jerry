# GH #144 Consolidated Issue Draft

> For review before updating the GitHub issue.

---

## Title

```
feat: Deterministic CLI output path resolver with config and migration tooling
```

## Body

> **Updated 2026-04-13.** This issue has been consolidated from three overlapping issues (#144, #192, #231) to track the remaining CLI output path resolver work. The original UX-only scope has been expanded to framework-wide. Issues #192 and #231 are superseded and should be closed as duplicates.

## Summary

ADR-output-path-resolution-001 (Option D) completed the immediate output path migration: all 32+ agents across eng-team, red-team, and user-experience skills now write to `projects/${JERRY_PROJECT}/` paths using a 4-priority layered resolution protocol implemented through agent prompt instructions. This resolved the blocking bug (#230 / BUG-006). C4 tournament PASS 0.955.

What Option D explicitly deferred — and what this issue now tracks — is **Option C: the deterministic Python CLI resolver**. The current prompt-based protocol has four structural limitations:

| Limitation | Impact |
|-----------|--------|
| 32+ independent LLM implementations of the same resolution logic | Drift risk; each agent can deviate |
| Not unit-testable | Cannot verify resolution correctness deterministically |
| No `jerry config` integration | Users cannot configure the output base path without editing governance YAMLs |
| No migration tooling | Users with pre-migration skill-internal artifacts cannot move them |

## What Is Already Done (not tracked here)

Delivered by BUG-006 / EPIC-002 Phase 2-3 (commits `86799bf7` through `8cc67126` on `feat/PROJ-024-tactical-work-2`; C4 tournament PASS reports at `projects/PROJ-030-bugs/reviews/BUG-006-c4-rescore-iter5.md` (0.955) and `BUG-012-013-014-c4-rescore-iter3.md` (0.952)):

- All agent output paths migrated to `projects/${JERRY_PROJECT}/` (107+ config files, 32+ agents, 13 skills)
- AD-M-011 standard in agent-development-standards.md
- ADR-output-path-resolution-001 (Option D protocol specification)
- P1/P2/P3/P4 prompt recognition spec in all agent `.md` files
- `filename_pattern` declarative field in governance YAML schema
- L5 CI gate (pre-commit hook) preventing regression to skill-internal paths
- `.gitignore` rules blocking `skills/*/output/` accumulation
- Domain-first ADR naming convention (`ADR-output-path-resolution-001`)
- [#245](https://github.com/geekatron/jerry/issues/245) / BUG-012 (pm-pmm paths), [#246](https://github.com/geekatron/jerry/issues/246) / BUG-013 (prompt-eng variable), [#247](https://github.com/geekatron/jerry/issues/247) / BUG-014 (governance completeness) — all resolved

**Note:** The formal wt-auditor integration verification acceptance test (original #144 AC-6) was not executed as a recorded artifact. The paths are structurally correct (verified via `grep -r 'skills/.*/output/' skills/` returning zero matches, and a full 89-agent framework audit documented in `projects/PROJ-030-bugs/reviews/gh-144-consolidation-analysis.md` Evidence E-007), but no formal wt-auditor acceptance test output was captured. This is why AC-8 below remains as a deliverable.

## Use Cases

### UC-PATH-001: Configure Custom Output Root

**Actor:** Framework User | **Goal:** All skill outputs land in a user-specified directory

1. User runs `jerry config set output.base_path <value>`
2. Jerry CLI persists the setting
3. User invokes any skill — agent calls `jerry resolve-output-path` and gets a path under the configured root
4. Output lands where the user expects

**Extensions:** JERRY_PROJECT not set -> error. Path doesn't exist -> prompt to create.

### UC-PATH-002: Agent Resolves Output Path Deterministically

**Actor:** Orchestrator | **Goal:** Agent gets a deterministic output path without LLM interpretation

1. Orchestrator passes caller context (explicit path, base path, or nothing)
2. Agent calls `uv run jerry resolve-output-path --agent <name> --engagement <id> --topic "<topic>"`
3. CLI returns exactly one resolved path on stdout (P1 > P2 > P3 > P4)
4. Agent writes to that path — no prompt parsing required

**Extensions:** All priorities absent -> non-zero exit. Parent dir missing -> create.

### UC-PATH-003: Migrate Legacy Outputs

**Actor:** Framework User | **Goal:** Move pre-migration `skills/*/output/` artifacts to project-relative paths

1. User runs `jerry migrate-output --dry-run --skill eng-team`
2. CLI shows move plan: source -> destination for each file
3. User confirms -> CLI executes moves with per-file verification
4. Summary shows moved/skipped/error counts

**Extensions:** No legacy files -> report clean. Destination exists -> prompt (overwrite/skip/abort).

### UC-PATH-004: Skill Author Declares Output Pattern

**Actor:** Skill Author | **Goal:** New agent's output location works with the resolution protocol

1. Author declares `output.location` and `filename_pattern` in governance YAML
2. Author validates with `jerry validate-schema` (existing command covers governance YAML validation)
3. At runtime, `jerry resolve-output-path` uses the declared pattern as P3 default

### UC-PATH-005: Orchestrator Co-locates Multi-Agent Outputs

**Actor:** Orchestrator | **Goal:** All agents in an engagement write to the same directory

1. Orchestrator determines engagement directory
2. Passes `--base-path <engagement-dir>` to each agent invocation
3. Each agent calls `jerry resolve-output-path --base-path <dir>` and gets `<dir>/<agent-filename>`
4. All artifacts co-located

## Use Case to Acceptance Criteria Map

| Use Case | Primary AC | Supporting ACs | Description |
|----------|-----------|----------------|-------------|
| UC-PATH-001 | **AC-1** | AC-2 | Config command + resolvable variable |
| UC-PATH-002 | **AC-3** | AC-4, AC-5 | CLI resolver (primary driver) + architecture + tests |
| UC-PATH-003 | **AC-7** | — | Migration tooling |
| UC-PATH-004 | **AC-4** | AC-3 | Governance YAML consumption by resolver (existing `jerry validate-schema` covers validation) |
| UC-PATH-005 | **AC-6** | AC-3, AC-8 | Base-path resolution + proof-of-concept + integration verification |

## Acceptance Criteria

### AC-1 — Configuration command
`jerry config set output.base_path <value>` and `jerry config get output.base_path` exist. Persists across sessions. Falls back to `projects/${JERRY_PROJECT}/` when `output.base_path` is not configured but `JERRY_PROJECT` env var is set. Falls back to `work/` when neither `output.base_path` nor `JERRY_PROJECT` is set (with stderr warning).

### AC-2 — Resolvable variable
`${JERRY_OUTPUT_BASE}` is resolvable at CLI invocation time: the Jerry CLI substitutes this variable when executing `jerry resolve-output-path`, reading the value from the AC-1 priority chain (configured `output.base_path` > `projects/${JERRY_PROJECT}/` > `work/`). When resolving to the `work/` fallback, the CLI emits a stderr warning: `"WARNING: Neither output.base_path nor JERRY_PROJECT is set — output written to work/ fallback. Set JERRY_PROJECT or run jerry config set output.base_path <path>."` Documented for use in governance YAML `output.location` templates.

### AC-3 — Python CLI resolver command
`jerry resolve-output-path --agent <name> [--engagement <id>] [--topic <topic>] [--base-path <path>] [--explicit-path <path>]` implements the full P1/P2/P3/P4 chain from ADR-output-path-resolution-001. Returns resolved absolute path on stdout (single line, no extra output). Reads `filename_pattern` from governance YAML at runtime. Non-zero exit on resolution failure.

### AC-4 — Domain service and clean architecture
`src/domain/services/output_path_resolver.py` (domain) + `src/interface/cli/commands/resolve_output_path.py` (adapter). H-07 compliant. No resolution logic in the adapter.

### AC-5 — Unit tests
All 4 priority levels + edge cases (missing engagement-id, empty topic, missing governance YAML) + all 7 ADR Compatibility Matrix scenarios (ADR-output-path-resolution-001, Compatibility Matrix table). 90% line coverage on `output_path_resolver.py` (H-20).

### AC-6 — Proof-of-concept agent migration
*Depends on: AC-3 complete.* At least one agent calls `jerry resolve-output-path` via Bash instead of prompt-based resolution. Match is defined as: resolved path string equality after normalizing to absolute paths (`os.path.abspath()` comparison). Must match for all ADR Compatibility Matrix scenarios.

### AC-7 — Framework-wide migration tooling
`jerry migrate-output --skill <skill> --engagement <id> [--dry-run] [--confirm]`. Move semantics with per-file verification. Collision prompting (overwrite/skip/abort; default on Enter: skip). `--dry-run` output format: header line `Config: output.base_path={value}, JERRY_PROJECT={value}` followed by `[MOVE] {source} -> {destination}` per file. Stale handoff reference warning: emitted when any `.md` file in the engagement directory contains a string matching `skills/*/output/` (indicating a handoff or reference that points to the pre-migration location).

### AC-8 — Integration verification artifact
*Depends on: AC-6 complete.* Formal wt-auditor verification with non-default `output.base_path`: (1) `jerry config set output.base_path work/resolver-test/`, (2) invoke proof-of-concept agent from AC-6, (3) confirm output file exists at the resolved path, (4) run `wt-auditor` and confirm its JSON output includes the artifact path under the configured `work/resolver-test/` base. Verification output captured as a file in the project directory and referenced in the PR description.

## Implementation Scope

**Direct:**
- `src/domain/services/output_path_resolver.py` — domain service
- `src/interface/cli/commands/resolve_output_path.py` — CLI adapter
- `src/interface/cli/commands/migrate_output.py` — migration CLI
- Config integration for `output.base_path`
- Unit tests
- One proof-of-concept agent migration (AC-6)
- ADR-output-path-resolution-001 update: note Option C implemented

**Out of scope:**
- Migrating all 32+ agents from prompt-based to CLI-based (follow-on story)
- Stale handoff reference auto-update during migration (known limitation)
- `jerry validate-agent` governance path validation subcommand (covered by existing `jerry validate-schema`)

## Supersedes

- **#192** (configurable output base path) — #192's `jerry config set output.base_path` -> consolidated AC-1. #192's `${JERRY_OUTPUT_BASE}` -> consolidated AC-2. #192's `fallback_location` concept -> superseded by ADR P4 fallback. #192's repo-based `work/` support -> covered by AC-1 fallback chain.
- **#231** (deterministic CLI resolver) — #231's `jerry resolve-output-path` command -> consolidated AC-3. #231's domain service architecture -> consolidated AC-4. #231's unit test requirement -> consolidated AC-5. #231's proof-of-concept migration -> consolidated AC-6. #231's compatibility matrix requirement -> consolidated AC-5 + AC-6.

## Related

- [#230](https://github.com/geekatron/jerry/issues/230) / BUG-006 — the blocking bug this follows from
- [#245](https://github.com/geekatron/jerry/issues/245) / BUG-012, [#246](https://github.com/geekatron/jerry/issues/246) / BUG-013, [#247](https://github.com/geekatron/jerry/issues/247) / BUG-014 — follow-on consistency bugs (resolved)
- ADR-output-path-resolution-001 (`docs/design/ADR-output-path-resolution-001.md`) — the protocol this CLI resolver makes deterministic
- AD-M-011 (`agent-development-standards.md`) — the MEDIUM standard this operationalizes

## Companion Artifacts

These artifacts provide detailed backing for this issue and are committed to the repository:

- **Consolidation analysis:** `projects/PROJ-030-bugs/reviews/gh-144-consolidation-analysis.md` — AC-by-AC status, unique contributions from #192/#231, scope decision rationale
- **Use case scenarios:** `projects/PROJ-030-bugs/reviews/gh-144-use-cases.md` — 5 use cases in Cockburn casual format with 24-row AC traceability map
