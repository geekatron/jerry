# Architecture Design: Corrected .claude/settings.json (#180)

> System design for the corrected settings.json with threat model, migration mapping, and architecture decisions.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level design decisions and security impact |
| [L1: Technical Design](#l1-technical-design) | Complete field mapping, threat model, corrected file specification |
| [L2: Strategic Implications](#l2-strategic-implications) | Precedence model, settings.local.json relationship, evolution path |

---

## L0: Executive Summary

The current `.claude/settings.json` contains 8 fields that Claude Code silently ignores, including 2 permission fields that create a false security perimeter. This design produces a corrected file using only schema-recognized fields, with properly structured `permissions.allow`/`permissions.ask` replacing the non-functional `permissions.allowed_tools`/`permissions.require_approval`.

**Key design decisions:**

1. **Permissions use the shared baseline pattern.** The committed `settings.json` defines the minimum tool set that all collaborators need. The `settings.local.json` (also committed in this repo) extends permissions with personal workflow additions.

2. **No model override in settings.json.** The `model` field is omitted from the committed file. Model selection is a personal/billing decision -- collaborators should control this via their own environment (`ANTHROPIC_MODEL`) or CLI flags, not a committed project file.

3. **Hooks are NOT included.** The research proposed hooks in the corrected file, but no hook scripts exist in `.claude/hooks/`. The `settings.local.json` already defines working hooks. Adding non-existent hook references would cause runtime errors.

4. **Six removed fields are documented with WHERE their intent is served.** No configuration capability is lost -- every removed field's intent is already handled by an existing Claude Code mechanism.

**Security impact:** The corrected file closes the false-perimeter gap where developers believed tool restrictions and approval gates were enforced when they were not.

---

## L1: Technical Design

### Field Migration Map

| Removed Field | Intent | Where Intent Is Actually Served |
|---------------|--------|--------------------------------|
| `commands` | Register slash commands | `.claude/commands/` directory (auto-discovered by Claude Code). Note: no command files currently exist in this repo on this branch. |
| `context` | Control which files are auto-loaded | `CLAUDE.md` is auto-loaded by Claude Code. `.claude/rules/` directory files are auto-loaded. The Navigation table in `CLAUDE.md` already lists reference paths. |
| `preferences.model` | Set default and fast-task models | Top-level `model` field (string) in settings.json. Per-class pinning via `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` env vars. |
| `preferences.output` | Line length, markdown preference | Not configurable via settings.json. Claude Code always produces markdown. Line length is not a settings.json property. |
| `preferences.behavior` | Plan-for-multi-file, citations, learnings | `.claude/rules/` files and `CLAUDE.md` behavioral instructions. Jerry already has `project-workflow.md` (PM-M-001 plan mode) and `quality-enforcement.md` (P-001 citations) covering these. |
| `rules` | Register rule files | `.claude/rules/` directory (auto-discovered). All `.md` files in that directory are loaded at session start. |
| `project` | Project name and description metadata | `CLAUDE.md` Identity section already contains this. |
| `version` | Settings file version tracking | Not a Claude Code concept. Remove. |

### Permission Migration

**Old (non-functional):**
```json
"permissions": {
  "allowed_tools": ["Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "Bash", "Task", "TodoWrite", "WebSearch", "WebFetch"],
  "require_approval": ["Bash:rm", "Bash:git push", "Write:.env"]
}
```

**New (schema-valid):**
```json
"permissions": {
  "allow": [
    "Read",
    "Write",
    "Edit",
    "MultiEdit",
    "Glob",
    "Grep",
    "Bash(uv *)",
    "Bash(git status *)",
    "Bash(git diff *)",
    "Bash(git log *)",
    "Bash(git branch *)",
    "Bash(git checkout *)",
    "Bash(git add *)",
    "Bash(git commit *)",
    "Bash(git fetch *)",
    "Bash(git pull *)",
    "Bash(git mv *)",
    "Bash(git ls-tree *)",
    "Bash(git check-ignore *)",
    "Bash(gh pr *)",
    "Bash(gh run *)",
    "Bash(gh issue *)",
    "Bash(ls *)",
    "Bash(test *)",
    "Bash(wc *)",
    "Bash(echo *)",
    "Bash(find *)",
    "Task",
    "WebSearch",
    "WebFetch",
    "TodoWrite"
  ],
  "ask": [
    "Bash(rm *)",
    "Bash(git push *)",
    "Bash(git reset *)",
    "Bash(git rebase *)",
    "Write(.env)",
    "Write(.env.*)"
  ],
  "deny": [
    "Bash(curl *)",
    "Bash(wget *)"
  ]
}
```

**Design rationale for permission structure:**

| Decision | Rationale |
|----------|-----------|
| Bash commands are pattern-scoped, not blanket `"Bash"` | Blanket Bash permission allows arbitrary shell commands including `curl`, `wget`, `rm -rf /`. Pattern-scoping is the defense-in-depth approach. |
| `uv *` as a single pattern | Covers `uv run`, `uv add`, `uv sync`, `uv pip` -- all legitimate Jerry development commands per H-05. |
| Git read operations auto-allowed | `git status`, `git diff`, `git log`, `git branch` are read-only and safe for all collaborators. |
| Git write operations auto-allowed except push/reset/rebase | `git add`, `git commit`, `git checkout`, `git fetch`, `git pull` are standard workflow. Push, reset, and rebase are destructive and require confirmation. |
| `curl`/`wget` denied | Prevents data exfiltration via arbitrary HTTP requests. WebSearch and WebFetch provide controlled external access. |
| `rm *` requires approval | Destructive file deletion must be confirmed. |
| `.env` writes require approval, reads not denied | The research proposed denying `.env` reads, but Claude Code agents may need to verify `.env` structure. Requiring approval for writes prevents accidental secret overwrite while allowing read access. |

### Threat Model (STRIDE per Trust Boundary)

**Trust Boundary:** settings.json is a committed file that all collaborators clone. It defines the permission baseline that Claude Code enforces.

| STRIDE Category | Threat | Current Exposure | Mitigation in Corrected File | DREAD Score |
|-----------------|--------|------------------|------------------------------|-------------|
| **Spoofing** | Non-functional permission fields create illusion of enforcement | HIGH -- developers believe tools are restricted when they are not | Remove non-functional fields; use only schema-valid `permissions.allow/ask/deny` | D:7 R:8 E:9 A:8 D:7 = 7.8 |
| **Tampering** | Malicious PR could add `"Bash"` (blanket) to `permissions.allow` | MEDIUM -- code review is the control | Pattern-scoped Bash permissions make blanket additions visually obvious in diff review. `deny` list blocks known-dangerous commands. | D:5 R:6 E:5 A:6 D:6 = 5.6 |
| **Repudiation** | No audit trail of which permissions were actually enforced vs. silently ignored | HIGH -- current file mixes valid and invalid fields | Clean file validates against `$schema`; any editor or CI can detect non-schema fields | D:6 R:7 E:8 A:7 D:5 = 6.6 |
| **Information Disclosure** | `.env` files could be read or exfiltrated via Bash commands | MEDIUM -- `curl`/`wget` could exfiltrate | `deny` list blocks `curl`/`wget`. `.env` writes require approval. | D:7 R:7 E:6 A:7 D:8 = 7.0 |
| **Denial of Service** | Hook references to non-existent scripts cause startup failures | LOW -- only affects developer experience | No hooks in committed file (hooks are in `settings.local.json` which references existing patterns) | D:3 R:4 E:7 A:3 D:2 = 3.8 |
| **Elevation of Privilege** | Blanket `"Bash"` permission enables arbitrary command execution | HIGH -- current file has `"Bash"` in `allowed_tools` (non-functional but misleading) | Pattern-scoped Bash prevents execution of commands not explicitly listed | D:8 R:8 E:7 A:8 D:9 = 8.0 |

### NIST CSF 2.0 Mapping

| CSF Function | How Corrected File Addresses It |
|--------------|--------------------------------|
| **Identify** | `$schema` field enables automated validation; invalid fields become detectable |
| **Protect** | Pattern-scoped permissions enforce least-privilege for Bash; `deny` blocks exfiltration vectors |
| **Detect** | Schema validation in CI can detect permission drift in PRs |
| **Respond** | `ask` list ensures destructive operations pause for human confirmation |
| **Recover** | `git push`, `git reset`, `git rebase` in `ask` list prevents irreversible repository state changes without approval |

### Corrected File Specification

The complete corrected `settings.json` content follows. Design constraints:

1. **Only schema-recognized fields** -- validated against `https://json.schemastore.org/claude-code-settings.json`
2. **No duplication with settings.local.json** -- the local file adds personal workflow permissions (MCP tools, skill shortcuts, additional Bash patterns)
3. **No hooks** -- no hook scripts exist at `.claude/hooks/`; hook definitions live in `settings.local.json`
4. **No model override** -- model is a personal/billing decision; use env vars or CLI

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "MultiEdit",
      "Glob",
      "Grep",
      "Bash(uv *)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git branch *)",
      "Bash(git checkout *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git fetch *)",
      "Bash(git pull *)",
      "Bash(git mv *)",
      "Bash(git ls-tree *)",
      "Bash(git check-ignore *)",
      "Bash(gh pr *)",
      "Bash(gh run *)",
      "Bash(gh issue *)",
      "Bash(ls *)",
      "Bash(test *)",
      "Bash(wc *)",
      "Bash(echo *)",
      "Bash(find *)",
      "Task",
      "WebSearch",
      "WebFetch",
      "TodoWrite"
    ],
    "ask": [
      "Bash(rm *)",
      "Bash(git push *)",
      "Bash(git reset *)",
      "Bash(git rebase *)",
      "Write(.env)",
      "Write(.env.*)"
    ],
    "deny": [
      "Bash(curl *)",
      "Bash(wget *)"
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "python3 .claude/statusline.py",
    "padding": 0
  },
  "enabledPlugins": {
    "context7@claude-plugins-official": true
  }
}
```

---

## L2: Strategic Implications

### Precedence Model

Claude Code evaluates settings in this precedence order (highest wins):

```
Managed settings (enterprise) > Local settings > Project settings > User settings
```

In this repository:
- **Project settings** = `.claude/settings.json` (committed, shared baseline)
- **Local settings** = `.claude/settings.local.json` (also committed in this repo, despite the name)

Since both are committed and both are "project-level" in spirit, the local file's permissions MERGE with (and override where conflicting) the project file's permissions. The `permissions.allow` arrays from both files are combined. If a tool appears in `deny` at one level and `allow` at another, `deny` takes precedence.

**Architectural concern:** `settings.local.json` is normally gitignored (personal overrides). In this repo, it is tracked. This means every collaborator gets the same local overrides, which defeats the purpose of the local/project split. This is a pre-existing condition outside the scope of issue #180 but should be addressed: either gitignore the local file (and move shared permissions into settings.json), or acknowledge that both files are effectively "project settings" with the local file providing an extension layer.

### What settings.local.json Provides Beyond settings.json

| Category | settings.local.json Additions | Rationale for local-only |
|----------|------------------------------|--------------------------|
| MCP permissions | `mcp__memory-keeper__*`, `mcp__context7__*`, `mcp__plugin_context7_context7__*` | MCP server availability depends on local setup |
| Skill permissions | `Skill(jerry:adversary)`, `Skill(jerry:problem-solving)`, etc. | Skill routing is Jerry-specific workflow |
| Additional Bash | `Bash(python3:*)`, `Bash(grep:*)` | Personal workflow convenience |
| Hooks | `PreToolUse`, `PermissionRequest` (WebSearch/WebFetch auto-allow) | Personal automation preference |

### Evolution Path

1. **Immediate (#180):** Replace current settings.json with the corrected version specified above.
2. **Near-term:** Add `.claude/settings.local.json` to `.gitignore`. Move any shared permissions from the local file into `settings.json`.
3. **Future:** If hook scripts are created at `.claude/hooks/`, add hook definitions to `settings.json` for shared enforcement. Consider `permissions.defaultMode` if the team wants a consistent permission posture.

### Trade-off Analysis

| Aspect | Current File | Corrected File | Trade-off |
|--------|-------------|----------------|-----------|
| Schema validation | Fails (8 unrecognized fields) | Passes | No downside |
| Tool permissions | Silently ignored | Actually enforced | Collaborators may need to approve Bash commands they previously ran silently (this is the intended behavior) |
| Bash scope | Blanket (non-functional) | Pattern-scoped | Some Bash commands not in the allow-list will require one-time approval. This is defense-in-depth, not a limitation. |
| Model override | Non-functional nested object | Omitted (personal choice) | Collaborators set their own model via env vars. If a shared model is desired later, add `"model": "claude-opus-4-5"` to this file. |
| File size | 83 lines (mostly non-functional) | ~50 lines (all functional) | Smaller, every line has effect |

---

*Design produced: 2026-03-12*
*Agent: eng-architect*
*Issue: #180*
*Criticality: C2 (Standard) -- reversible configuration change, <10 files, affects developer workflow*
*NIST CSF Functions: Identify, Protect, Detect, Respond, Recover*
*SSDF Practices: PO.1 (security requirements), PO.2 (architecture ownership)*
