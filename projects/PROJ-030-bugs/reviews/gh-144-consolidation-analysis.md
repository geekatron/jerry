# GH #144 Consolidation Analysis — CLI Output Path Resolver

> **PS ID:** work-bug006
> **Entry ID:** e-099
> **Analysis Type:** gap
> **Date:** 2026-04-13
> **Analyst:** ps-analyst (convergent)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scope Decision](#scope-decision) | Framework-wide vs UX-only |
| [AC Status — #144](#ac-status--144) | Done / remaining / modified per AC |
| [Unique Contributions — #192 and #231](#unique-contributions--192-and-231) | What each adds beyond #144 |
| [Draft Consolidated ACs](#draft-consolidated-acs) | Merged, deduplicated, current-state acceptance criteria |
| [Suggested Title](#suggested-title) | Consolidated issue title |
| [Issue Body Draft](#issue-body-draft) | Ready-to-paste GitHub issue body for updating #144 |
| [Evidence Summary](#evidence-summary) | Source citations |

---

## Scope Decision

**Recommendation: Framework-wide.**

#144 was filed as UX-only because the UX skill was the trigger. Since then, the EPIC-002 / BUG-006 migration addressed ALL 13 affected skills (eng-team, red-team, 11 UX sub-skills) using the same P1/P2/P3/P4 layered resolution protocol (ADR-output-path-resolution-001, Option D). The CLI resolver work that remains — a Python `jerry resolve-output-path` command, `jerry config` integration, migration tooling, and unit tests — applies uniformly to every agent that implements the protocol, not just UX agents.

Keeping #144 UX-only after the migration has completed would require either:
- A parallel CLI issue for eng-team/red-team/all other skills (duplicates the same work), or
- Shipping a UX-specific resolver that immediately needs to be generalized

Neither is acceptable. Framework-wide is the correct scope for the remaining work.

**Consequence for #192 and #231:** Both issues are superseded by this consolidation. They should be closed as "merged into #144" once #144 is updated.

---

## AC Status — #144

Evaluated against what EPIC-002 / BUG-006 / ADR-output-path-resolution-001 actually delivered.

### AC-1 — Configuration contract

**Status: PARTIALLY DONE — modified scope remains**

What was delivered:
- Environment variable `JERRY_PROJECT` is already the control point for project-relative paths (P3 resolution)
- `output.location` templates in all 32+ agent governance YAMLs now use `projects/${JERRY_PROJECT}/` prefix
- `fallback_location` concept from #192 is implemented as the P4 work-directory fallback in ADR-output-path-resolution-001
- AD-M-011 MEDIUM standard codified in agent-development-standards.md

What remains:
- No `jerry config set output.base_path` command exists (from #192)
- No resolvable `${JERRY_OUTPUT_BASE}` variable (from #192)
- The configuration layer is LLM-interpreted per-agent prompt instructions, not a programmatic config system
- The UX-specific `ux.output_root` key proposed in #144 is now superseded by the framework-wide `output.base_path` key proposed in #192

**Revised scope:** Implement `jerry config get/set output.base_path` as a persistent configuration entry. This generalizes the `ux.output_root` concept from #144 AC-1 to the framework-wide `output.base_path` from #192.

---

### AC-2 — Runtime resolution via shared utility

**Status: REMAINING — this is the core gap**

What was delivered:
- ADR-output-path-resolution-001 Option D: each agent independently implements the 4-priority resolution chain through its `.md` system prompt instructions
- `filename_pattern` declarative field added to governance YAML schema (documentation only)
- Resolution logic specified as pseudocode in the ADR

What remains:
- No Python utility exists — resolution is LLM-interpreted per agent (32+ independent implementations)
- No `jerry resolve-output-path` CLI command (#231)
- Resolution cannot be unit-tested — it is an LLM behavior
- Drift between agents' interpretation is possible over time
- The `filename_pattern` field is documentation-only; no code reads it at runtime

**This is the primary remaining deliverable.** #231 correctly diagnoses and specifies the solution. The ADR explicitly deferred Option C (Python resolver) as DC-6 prohibited Python code changes during the immediate migration. That constraint no longer applies.

---

### AC-3 — Default path with H-04 fallback warning

**Status: DONE (via ADR Option D P3/P4 protocol)**

Delivered:
- P3 (project default): `projects/${JERRY_PROJECT}/engagements/{engagement-id}/...` when JERRY_PROJECT is set
- P4 (work fallback): `work/{agent}-{slug}.md` when JERRY_PROJECT not set
- Mandatory warning log when P4 triggers
- Pattern is consistent across all 32+ updated agents

No remaining work for this AC under the prompt-based protocol. The CLI resolver (AC-2 remaining) will encode this same fallback logic deterministically.

---

### AC-4 — Backward compatibility

**Status: DONE**

Delivered:
- Existing project-relative agent invocations continue to work unchanged
- P1 explicit path overrides are preserved — callers who specify exact paths are unaffected
- Old skill-internal paths (`skills/*/output/`) are not valid output locations for new invocations; BUG-006 removed committed artifacts and added `.gitignore` rules
- No agent that was previously working correctly was broken by the migration

No remaining work.

---

### AC-5 — Agent definition updates

**Status: DONE**

Delivered:
- All 107 config files updated (22 eng-team + 25 red-team + 60 UX)
- 32+ agent `.md` files updated to implement P1/P2/P3/P4 resolution via prompt instructions
- Governance YAML `output.location` fields updated to project-relative templates in all agents
- CI gate (L5) prevents regression: grep-based check that `skills/*/output/` paths cannot reappear

Verification: `grep -r 'skills/.*/output/' skills/` returns zero matches (confirmed 2026-04-01).

---

### AC-6 — Integration verification

**Status: PARTIALLY DONE**

Delivered:
- Agents now write to project-relative paths that wt-auditor and orch-synthesizer can discover
- HD-M-002 artifact path validation is satisfied for properly invoked agents

What remains:
- No explicit wt-auditor verification run documented for the updated paths
- No migration verification artifact captured in a project directory
- The verification procedure specified in #144 AC-6 (configure non-default path, run agent, confirm wt-auditor discovers it) has not been executed as a formal acceptance test

**This is a process gap, not a structural gap.** The paths are correct; the documented verification step hasn't been performed. This should become a test specification requirement for the CLI resolver issue, not a blocker.

---

### AC-7 — Migration tooling

**Status: REMAINING**

What was delivered:
- BUG-006 manually removed the 28 committed eng-team output files
- `.gitignore` updated to prevent future accumulation

What remains:
- No `jerry ux migrate-output` command (or framework-wide equivalent)
- No `--dry-run` capability for migrating artifacts from old to new locations
- Users who have existing skill-internal output artifacts from prior sessions cannot migrate them automatically

**Scope update:** The migration command should be framework-wide (`jerry migrate-output --skill {skill}` or `jerry migrate-output --engagement {id}`), not UX-specific. The pattern is identical across eng-team, red-team, and UX.

---

### AC-8 — Documentation

**Status: DONE**

Delivered:
- ADR-output-path-resolution-001 documents the full resolution protocol, priority chain, prompt recognition spec, agent integration spec
- AD-M-011 in agent-development-standards.md documents the MEDIUM standard
- Governance YAML schema updated with `filename_pattern` field and documentation
- All 32+ agent `.md` files contain Output Path Resolution sections

No remaining documentation work beyond what the CLI resolver issue naturally produces.

---

### AC-9 — Cross-skill pattern documentation

**Status: DONE**

Delivered:
- AD-M-011 in agent-development-standards.md is the named "Configurable Output Path Pattern" equivalent
- The pattern applies to all skills, not just UX
- The standard references the resolution protocol from ADR-output-path-resolution-001
- eng-team and red-team already adopted the pattern as part of BUG-006

Nothing further needed for this AC.

---

### AC Status Summary

| AC | Title | Status | Remaining Work |
|----|-------|--------|----------------|
| AC-1 | Configuration contract | Partial | `jerry config set output.base_path` command |
| AC-2 | Runtime resolution utility | Remaining | Python CLI resolver (core deliverable) |
| AC-3 | Default path + fallback warning | Done | None |
| AC-4 | Backward compatibility | Done | None |
| AC-5 | Agent definition updates | Done | None |
| AC-6 | Integration verification | Partial | Formal acceptance test for CLI resolver |
| AC-7 | Migration tooling | Remaining | Framework-wide `jerry migrate-output` command |
| AC-8 | Documentation | Done | None |
| AC-9 | Cross-skill pattern docs | Done | None |

**5 of 9 ACs are fully done. 2 are partially done. 2 are fully remaining.**

---

## Unique Contributions — #192 and #231

### From #192: configurable output base path for skill agents

| Contribution | Unique? | Assessment |
|-------------|---------|------------|
| `jerry config set output.base_path` command | Yes — #144 AC-1 uses a UX-specific `ux.output_root` key; #192 proposes the framework-wide `output.base_path` | Adopt #192's naming: `output.base_path` is more general and avoids UX-specific terminology |
| `${JERRY_OUTPUT_BASE}` resolvable variable | Yes — #144 does not mention a resolvable variable | Valuable: agents could reference `${JERRY_OUTPUT_BASE}` in their `output.location` templates, enabling runtime resolution without hardcoding project roots |
| `fallback_location` governance field concept | Superseded — ADR-output-path-resolution-001 P4 is the canonical fallback | Do not adopt: the ADR's P4 work-directory fallback is the correct mechanism; `fallback_location` is redundant |
| Explicit accommodation of repo-based (`work/`) placement pattern | Yes — #144 mentions fallback but #192 frames it as a first-class configuration option | Adopt: clarify in the consolidated issue that `jerry config set output.base_path work/` is a supported configuration |

**Net contribution from #192:** The `output.base_path` config key name and the `${JERRY_OUTPUT_BASE}` variable concept. Both should be adopted in the consolidated issue.

### From #231: Deterministic output path resolver CLI command

| Contribution | Unique? | Assessment |
|-------------|---------|------------|
| `jerry resolve-output-path` CLI command | Yes — #144 AC-2 describes a "shared utility" without specifying a CLI entry point | Adopt: the CLI command is the correct interface; it makes the resolver callable from agent Bash tool invocations |
| Python domain service (`output_path_resolver.py`) | Yes — architecture and file location specified | Adopt: `src/domain/services/output_path_resolver.py` + `src/interface/cli/commands/resolve_output_path.py` follows clean architecture (H-07) |
| Reading `filename_pattern` from governance YAML at runtime | Yes — this makes the declarative field programmatically consumed | Adopt: the resolver reads governance YAML `filename_pattern` field; this closes the gap where the field was documentation-only |
| Unit tests for all 4 priority levels and edge cases | Yes — #144 does not mention testing | Adopt: unit tests are required for deterministic behavior and are measurable |
| Agent migration from prompt-based to CLI-based resolution | Yes — explicitly proposes updating 32+ agents to call `uv run jerry resolve-output-path` | Adopt partially: at least one agent migrated as proof of concept in the initial PR; full migration is a follow-on story |
| Compatibility matrix against ADR-output-path-resolution-001 scenarios | Yes — requires output to match Option D for all scenarios | Adopt: this ensures the CLI resolver is a drop-in replacement for the LLM-interpreted protocol, not a behavioral change |

**Net contribution from #231:** The entire CLI resolver implementation design (command, domain service, governance YAML consumption, unit tests, compatibility requirement). This is the highest-value addition and should be the core of the consolidated issue.

---

## Draft Consolidated Acceptance Criteria

The following ACs replace #144's original 9. ACs that were fully satisfied by EPIC-002 are not carried forward (they are noted as done in the issue body). ACs that are new (from #192 or #231) are labeled with their source.

### AC-1 — Configuration command [from #192, replaces #144 AC-1]

A `jerry config` subcommand manages the framework-wide output base path setting:

```
jerry config set output.base_path <value>
jerry config get output.base_path
```

- The value is stored persistently in the Jerry config file (same persistence mechanism as any existing `jerry config` entry)
- Supported value types: (a) a relative directory name (e.g., `work/`, `projects/PROJ-007/`) used as the output root, or (b) an absolute path
- Setting this value causes `${JERRY_OUTPUT_BASE}` (see AC-2) to resolve to the configured value
- Falls back to `projects/${JERRY_PROJECT}/` when not set and JERRY_PROJECT exists
- Falls back to `work/` when neither is set (with warning per ADR P4 behavior)
- `jerry config get output.base_path` returns the current value or `[not set — using project default]`

### AC-2 — Resolvable variable [from #192]

The variable `${JERRY_OUTPUT_BASE}` is resolvable at CLI invocation time:

- When `output.base_path` config is set: resolves to that value
- When unset and JERRY_PROJECT is set: resolves to `projects/${JERRY_PROJECT}/`
- When neither is set: resolves to `work/`

This variable is documented for use in agent `output.location` governance YAML templates. Agents that reference `${JERRY_OUTPUT_BASE}` in their location template get correct resolution in all three contexts without hardcoding project prefixes.

### AC-3 — Python CLI resolver command [from #231, replaces #144 AC-2]

A deterministic `jerry resolve-output-path` CLI command exists and implements the 4-priority resolution chain from ADR-output-path-resolution-001:

```bash
uv run jerry resolve-output-path \
  --agent <agent-name> \
  [--engagement <engagement-id>] \
  [--topic <topic-string>] \
  [--base-path <base-path>]      # P2: base path + agent suffix
  [--explicit-path <full-path>]  # P1: explicit full path
```

- Returns the resolved absolute path as the sole stdout line (no extra output)
- P1 (explicit-path) wins over all other parameters
- P2 (base-path) wins over P3/P4
- P3 uses `${JERRY_OUTPUT_BASE}` resolution (AC-2) + agent's `filename_pattern` from governance YAML
- P4 (fallback) writes to `work/` and prints a warning to stderr
- Non-zero exit code when resolution fails (invalid path, permission error)
- Command reads `filename_pattern` from the agent's `.governance.yaml` file (not hardcoded)

### AC-4 — Domain service and clean architecture [from #231]

The resolver is implemented as a Python domain service following H-07 (layer isolation):

- Domain service: `src/domain/services/output_path_resolver.py`
  - Contains all resolution logic (P1/P2/P3/P4 chain, variable substitution, governance YAML reading)
  - No imports from CLI adapter layer or infrastructure layer
- CLI adapter: `src/interface/cli/commands/resolve_output_path.py`
  - Parses CLI arguments, calls domain service, prints result, handles exit codes
  - No resolution logic in the adapter
- Governance YAML reader: uses existing Jerry infrastructure for reading agent governance files

### AC-5 — Unit tests covering all priority levels [from #231]

Unit tests exist for the domain service covering:

- P1: explicit path returned verbatim
- P2: base path + filename_pattern interpolation with topic slugification
- P3: JERRY_PROJECT set, output.base_path not set → project default
- P3: output.base_path set, JERRY_PROJECT set → output.base_path value wins
- P4: neither JERRY_PROJECT nor output.base_path set → work/ fallback + warning to stderr
- Edge case: missing engagement-id (agent has no engagement context)
- Edge case: empty topic → "unnamed" slug used
- Edge case: agent governance YAML not found → descriptive error, non-zero exit
- Compatibility: output matches ADR-output-path-resolution-001 for all scenarios in its Compatibility Matrix

Minimum coverage: 90% line coverage on `output_path_resolver.py` per H-20.

### AC-6 — Proof-of-concept agent migration [from #231]

At least one agent (suggested: `eng-architect` as the original #231 spec, or `ps-researcher` as the framework reference) is updated to call `jerry resolve-output-path` via Bash instead of implementing resolution logic through prompt instructions:

```markdown
## OUTPUT PATH RESOLUTION
Before writing any output file:
1. Call: `uv run jerry resolve-output-path --agent eng-architect --engagement {engagement-id} --topic "{topic}"`
2. Use the returned path for all Write tool calls in this session
3. Do not compute or modify this path independently
```

The migrated agent must produce identical output paths to the prompt-based protocol in a side-by-side comparison for all scenarios in the ADR Compatibility Matrix.

### AC-7 — Framework-wide migration tooling [replaces #144 AC-7, generalizes UX-only scope]

A `jerry migrate-output` command migrates artifacts from old skill-internal paths to configured output locations:

```bash
jerry migrate-output \
  --skill <skill-name>          # e.g., eng-team, red-team, user-experience
  --engagement <engagement-id>  # scope to single engagement
  [--dry-run]                   # show moves without executing
  [--confirm]                   # skip interactive prompt (for scripts)
```

Specification:
- `--dry-run` output: `[MOVE] {source} -> {destination}` per file, with the configuration state used for resolution printed as a header
- Confirmation required before any file system operation (P-020) unless `--confirm` flag set
- Move semantics: source is not deleted until destination exists and is verified
- Collision behavior: prompt (overwrite / skip / abort) per file
- Scope: one engagement at a time
- Warning when handoff files in the engagement directory contain stale skill-internal path references (users must update manually)
- Implemented as clean architecture: domain service + CLI adapter + unit tests

### AC-8 — Integration verification [strengthens #144 AC-6]

After the CLI resolver is implemented, a formal integration verification must be performed and its artifact captured:

1. Set `output.base_path` to a non-default path (e.g., `work/resolver-test/`)
2. Invoke one agent with `jerry resolve-output-path` (the migrated proof-of-concept agent from AC-6)
3. Confirm the output file is written to the resolved path
4. Confirm wt-auditor discovers the artifact at that path
5. Capture the wt-auditor output as an artifact referenced in the PR description

This verification artifact must exist before the PR is merged.

---

## Suggested Title

```
feat: Deterministic CLI output path resolver with config and migration tooling
```

Rationale:
- "Deterministic" signals the key improvement over the current LLM-interpreted protocol
- "CLI" clarifies this is a Python command, not an agent-level change
- "with config and migration tooling" captures the full scope without being exhaustive
- Does not say "UX" — correctly signals framework-wide scope
- Drops the "(ADR-EPIC002-001 Option C)" suffix from #231's title to keep it user-readable

Alternative if the team prefers to keep it explicitly related to the ADR:
```
feat: Implement Option C deterministic output path resolver (ADR-output-path-resolution-001)
```

---

## Issue Body Draft

The following is ready to paste as the updated body for GH #144. It replaces the existing body in full.

---

### Draft Body

**NOTE TO MAINTAINER:** This issue has been updated to reflect the current state after the EPIC-002 / BUG-006 migration (PR: feat/PROJ-024-tactical-work-2 merged). The original UX-only scope has been expanded to framework-wide. Issues #192 and #231 are superseded by this update and can be closed as "merged into #144."

---

## Summary

ADR-output-path-resolution-001 (Option D) completed the immediate output path migration: all 32+ agents across eng-team, red-team, and user-experience skills now write to `projects/${JERRY_PROJECT}/` paths using a 4-priority layered resolution protocol implemented through agent prompt instructions. This resolved the blocking bug (BUG-006 / #230).

What Option D explicitly deferred — and what this issue now tracks — is **Option C: the deterministic Python CLI resolver**. The current prompt-based protocol has four structural limitations that justify the CLI resolver as a follow-on investment:

| Limitation | Impact |
|-----------|--------|
| 32+ independent LLM implementations of the same resolution logic | Drift risk; each agent can deviate |
| Not unit-testable | Cannot verify resolution correctness deterministically |
| No `jerry config` integration | Users cannot configure the output base path without editing governance YAMLs |
| No migration tooling | Users with pre-migration skill-internal artifacts cannot move them |

## What Is Already Done (not tracked here)

The following were delivered by BUG-006 / EPIC-002 and are NOT part of this issue:

- All agent output paths migrated to `projects/${JERRY_PROJECT}/` (107 config files, 32 agents)
- AD-M-011 standard in agent-development-standards.md
- ADR-output-path-resolution-001 (Option D protocol specification)
- P1/P2/P3/P4 prompt recognition spec in all agent `.md` files
- `filename_pattern` declarative field in governance YAML schema
- L5 CI gate preventing regression to skill-internal paths
- `.gitignore` rules blocking `skills/*/output/` accumulation
- 28 committed eng-team artifacts removed

## Problem / Use Case

### 1. Resolution logic is untestable

Each of 32+ agents independently interprets the same 4-priority resolution chain through its system prompt. There is no way to write a unit test that verifies "if the caller provides a base-path, does this agent correctly resolve to base-path + filename_pattern?". This is a structural quality gap — the resolution protocol is behaviorally specified but not deterministically enforced.

### 2. Drift between agents is inevitable

With 32+ implementations of the same logic spread across agent `.md` files, future edits will diverge. An agent updated to add a new output type may introduce a variation in how it interprets the P2 priority. There is no shared code path to update.

### 3. No user-facing configuration

Users who want all their Jerry outputs in `work/` (repo-based pattern, per `worktracker-directory-structure.md`) cannot configure this without modifying governance YAML files. A `jerry config set output.base_path work/` command is the correct interface.

### 4. No migration tooling

Pre-migration artifacts in `skills/eng-team/output/`, `skills/red-team/output/`, and `skills/ux-*/output/` that users may have from sessions prior to BUG-006 cannot be migrated automatically. A `jerry migrate-output` command is needed.

## Acceptance Criteria

### AC-1 — Configuration command
`jerry config set output.base_path <value>` and `jerry config get output.base_path` exist. The value persists across sessions. Supported values: relative directory name or absolute path. Falls back to `projects/${JERRY_PROJECT}/` when not set and JERRY_PROJECT exists. Falls back to `work/` when neither is set (with stderr warning).

### AC-2 — Resolvable variable
`${JERRY_OUTPUT_BASE}` is resolvable at CLI invocation time based on the AC-1 priority chain. Documented for use in agent `output.location` governance YAML templates.

### AC-3 — Python CLI resolver command
`jerry resolve-output-path --agent <name> [--engagement <id>] [--topic <topic>] [--base-path <path>] [--explicit-path <path>]` exists and implements the full P1/P2/P3/P4 resolution chain from ADR-output-path-resolution-001. Returns the resolved absolute path on stdout. Reads `filename_pattern` from the agent's `.governance.yaml` file at runtime.

### AC-4 — Domain service and clean architecture
Resolver implemented as `src/domain/services/output_path_resolver.py` (domain) + `src/interface/cli/commands/resolve_output_path.py` (CLI adapter). No resolution logic in the adapter. No framework imports in the domain service.

### AC-5 — Unit tests
Unit tests cover all 4 priority levels, edge cases (missing engagement-id, empty topic, missing governance YAML), and the full ADR Compatibility Matrix. 90% line coverage on `output_path_resolver.py`.

### AC-6 — Proof-of-concept agent migration
At least one agent updated to call `jerry resolve-output-path` via Bash instead of implementing resolution through prompt instructions. Output must match the prompt-based protocol for all ADR Compatibility Matrix scenarios.

### AC-7 — Framework-wide migration tooling
`jerry migrate-output --skill <skill> --engagement <id> [--dry-run] [--confirm]` migrates artifacts from skill-internal paths to configured output locations. Dry-run mode required. Move semantics with per-file verification. Collision prompting. Warning for stale handoff references.

### AC-8 — Integration verification
Formal verification artifact (wt-auditor output) captured and referenced in PR description.

## Implementation Scope

**Direct scope:**
- `src/domain/services/output_path_resolver.py` — new domain service
- `src/interface/cli/commands/resolve_output_path.py` — new CLI adapter
- `src/interface/cli/commands/config.py` — extend with `output.base_path` subcommand
- `src/interface/cli/commands/migrate_output.py` — new CLI adapter for migration
- Unit tests for all components
- One agent `.md` file updated (proof-of-concept migration, AC-6)
- ADR-output-path-resolution-001 updated: note that Option C is now implemented

**Out of scope:**
- Migrating all 32+ agents from prompt-based to CLI-based resolution (follow-on story)
- Updating stale handoff references during migration (AC-7 known limitation)

## Supersedes

- #192 (enhancement: configurable output base path) — AC-1 and AC-2 cover this entirely. Close #192 as "merged into #144".
- #231 (feat: Deterministic output path resolver CLI command) — AC-3, AC-4, AC-5, AC-6 cover this entirely. Close #231 as "merged into #144".

## Related

- #230 / BUG-006: The blocking bug this issue follows on from
- ADR-output-path-resolution-001: The protocol that this CLI resolver makes deterministic
- AD-M-011 (agent-development-standards.md): The MEDIUM standard this issue operationalizes

---

*Analysis produced by ps-analyst (work-bug006 / e-099). Evidence base: GH issues #144, #192, #231 (fetched live); BUG-006 worktracker entity; ADR-output-path-resolution-001; agent-development-standards.md AD-M-011.*

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Issue body | GH #144 | Original 9 ACs, UX-specific scope, C4 tournament score 0.9205 |
| E-002 | Issue body | GH #192 | `jerry config set output.base_path`, `${JERRY_OUTPUT_BASE}` variable concept |
| E-003 | Issue body | GH #231 | CLI resolver design, domain service spec, unit test requirement, compatibility matrix requirement |
| E-004 | Worktracker entity | projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md | Confirmed AC-1/3/4/5/7/8/9 done; history of EPIC-002 migration execution |
| E-005 | ADR | docs/design/ADR-output-path-resolution-001.md | Option C deferred (DC-6), Option D selected; P1/P2/P3/P4 protocol spec; pseudocode; DC satisfaction matrix |
| E-006 | Standards | .context/rules/agent-development-standards.md | AD-M-011 confirms cross-skill pattern doc delivered (AC-9 done) |
| E-007 | BUG-006 history | projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md:281 | "2026-04-01: all 9 tasks completed... Verification: grep returns zero matches. AC-1 through AC-7 all satisfied." |

---

*File: projects/PROJ-030-bugs/reviews/gh-144-consolidation-analysis.md*
*Created: 2026-04-13 by ps-analyst*
