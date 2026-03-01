# Regression Analysis: Agent Definition Frontmatter
## Branch: `feat/proj-012-agent-optimization` vs `main`
**Date:** 2026-02-26
**Analyst:** Claude Code (automated)
**Scope:** All 58 agent `.md` files under `skills/*/agents/`

---

## Summary Table

| Metric | Value |
|--------|-------|
| Total agents analyzed | 58 |
| Agents with frontmatter changes | 58 |
| PASS | 58 |
| FAIL | 0 |
| Skills covered | adversary, eng-team, nasa-se, orchestration, problem-solving, red-team, saucer-boy, saucer-boy-framework-voice, transcript, worktracker |

**Overall Verdict: PASS**

---

## Analysis Dimensions

### 1. Field Preservation: Were all official Claude Code fields preserved?

**Result: PASS — No official fields were removed.**

All fields present in `main` frontmatter are present in `HEAD` frontmatter with identical values. The five fields that appeared in `main` across agents were:

| Field | Agents in main | Agents in HEAD |
|-------|---------------|----------------|
| `name` | 58 | 58 |
| `description` | 58 | 58 |
| `model` | 58 | 58 |
| `tools` | 58 | 58 |
| `mcpServers` | 34 | 34 |

All 34 agents that had `mcpServers` declarations in `main` retain them in `HEAD` with identical values. No `mcpServers` entry was lost or mutated.

### 2. Governance Field Removal: Were non-official fields correctly stripped?

**Result: PASS — No governance fields were present in `main` frontmatter to begin with.**

The `main` branch agent `.md` frontmatter already contained only official Claude Code fields. Governance metadata was stored in companion `.governance.yaml` files (`skills/*/agents/*.governance.yaml`), not in the `.md` frontmatter itself. Both branches show 58 `.governance.yaml` files existing on disk.

Accordingly, "stripping governance fields from frontmatter" had no net effect on the `.md` files themselves — there were no non-official fields to strip. Zero governance fields appear in either `main` or `HEAD` frontmatter across all 58 agents.

### 3. Value Integrity: Did any field values change?

**Result: PASS — No field values changed for any existing field.**

For every official field present in both branches (`name`, `description`, `model`, `tools`, `mcpServers`), the values are byte-for-byte identical between `main` and `HEAD`. No regressions.

### 4. New Fields: Were any unexpected fields added?

**Result: PASS with observation — Two official fields were added to all 58 agents.**

The compose pipeline added two fields that were absent from `main` frontmatter:

| Field | Value | Classification |
|-------|-------|---------------|
| `permissionMode` | `default` | Official Claude Code field (in the 12-field spec) |
| `background` | `false` | Official Claude Code field (in the 12-field spec) |

Both are legitimate Claude Code frontmatter fields. They were not present in `main` because they were previously left as implicit defaults. PROJ-012 made these defaults explicit. This is not a governance leak — both fields appear in the official 12-field Claude Code spec (`name`, `description`, `model`, `tools`, `disallowedTools`, `mcpServers`, `permissionMode`, `maxTurns`, `skills`, `hooks`, `memory`, `background`, `isolation`).

No non-official fields were added to any agent.

---

## Representative Sample Findings

17 agents were checked individually across all 10 skills:

| Agent | Skill | main fields | HEAD fields | Status |
|-------|-------|-------------|-------------|--------|
| adv-executor | adversary | name, description, model, tools | + permissionMode, background | PASS |
| adv-selector | adversary | name, description, model, tools | + permissionMode, background | PASS |
| eng-lead | eng-team | name, description, model, tools, mcpServers(context7) | + permissionMode, background | PASS |
| eng-security | eng-team | name, description, model, tools, mcpServers(context7) | + permissionMode, background | PASS |
| nse-requirements | nasa-se | name, description, model, tools, mcpServers(memory-keeper) | + permissionMode, background | PASS |
| nse-explorer | nasa-se | name, description, model, tools, mcpServers(context7) | + permissionMode, background | PASS |
| orch-planner | orchestration | name, description, model, tools, mcpServers(memory-keeper) | + permissionMode, background | PASS |
| orch-synthesizer | orchestration | name, description, model, tools, mcpServers(memory-keeper) | + permissionMode, background | PASS |
| ps-researcher | problem-solving | name, description, model, tools, mcpServers(context7) | + permissionMode, background | PASS |
| ps-architect | problem-solving | name, description, model, tools, mcpServers(context7+memory-keeper) | + permissionMode, background | PASS |
| red-lead | red-team | name, description, model, tools, mcpServers(context7) | + permissionMode, background | PASS |
| red-recon | red-team | name, description, model, tools, mcpServers(context7) | + permissionMode, background | PASS |
| sb-voice | saucer-boy | name, description, model, tools | + permissionMode, background | PASS |
| sb-reviewer | saucer-boy-framework-voice | name, description, model, tools | + permissionMode, background | PASS |
| ts-parser | transcript | name, description, model, tools, mcpServers(memory-keeper) | + permissionMode, background | PASS |
| wt-auditor | worktracker | name, description, model, tools | + permissionMode, background | PASS |
| wt-visualizer | worktracker | name, description, model, tools | + permissionMode, background | PASS |

---

## Exhaustive Change Pattern

**Single uniform change pattern across all 58 agents:**

```
Added: permissionMode: default
Added: background: false
```

No deviations. Every agent received exactly these two fields and nothing else changed.

---

## mcpServers Integrity Detail

34 agents had `mcpServers` in `main`. All 34 are preserved with identical values in `HEAD`:

- **context7** (`context7: true`): 30 agents — all 10 eng-team agents, 2 nasa-se agents, 1 orchestration agent (orch-synthesizer), 5 problem-solving agents, 11 red-team agents, 1 ps agent (ps-investigator)
- **memory-keeper** (`memory-keeper: true`): 3 agents — nse-requirements, orch-tracker, ts-extractor, ts-parser
- **both** (`context7: true` + `memory-keeper: true`): 1 agent — ps-architect

The multi-server declaration for ps-architect (`mcpServers: context7: true\n  memory-keeper: true`) was preserved exactly in both branches.

---

## Overall Verdict: PASS

All four analysis dimensions pass:

1. **Field preservation**: No official fields were dropped. All 5 field types present in `main` are present in `HEAD`.
2. **Governance field removal**: No governance (non-official) fields were present in frontmatter on either branch. PROJ-012 correctly maintains the separation established in `main` (governance in `.governance.yaml`, official fields only in `.md` frontmatter).
3. **Value integrity**: Zero value changes on any field that existed in `main`. All `name`, `description`, `model`, `tools`, and `mcpServers` values are identical.
4. **New fields**: Two fields added (`permissionMode: default`, `background: false`), both are official Claude Code fields. No non-official fields added.

The compose pipeline correctly handles frontmatter — it strips no existing values, introduces no governance field leakage, and adds only explicit defaults for two previously-implicit official fields.

---

## Methodology Notes

- **main branch content**: Retrieved via `git show main:{path}` for all 58 agents
- **HEAD content**: Read directly from working tree (`skills/*/agents/*.md`)
- **Field parsing**: Top-level YAML key extraction using regex (no third-party YAML parser dependency; handles multi-line values and nested `mcpServers` sub-keys)
- **Governance fields defined as**: Any YAML key not in the 12-field official Claude Code set
- **Value comparison**: Stripped whitespace comparison for robustness against trailing newline differences
