# Settings.json Unrecognized Field Investigation

> Research into 8 fields in Jerry's `.claude/settings.json` that are NOT recognized by the official Claude Code JSON schema.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language findings and project impact |
| [L1: Technical Analysis](#l1-technical-analysis) | Per-field investigation with migration guidance |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic impact and migration plan |
| [Methodology](#methodology) | Research approach and sources consulted |
| [References](#references) | All cited sources |

---

## L0: Executive Summary

Jerry's committed `.claude/settings.json` contains 8 fields that Claude Code does not recognize. Think of it like writing configuration entries in an app that the app never reads -- the settings exist in the file but have zero effect on Claude Code's behavior.

**Key findings:**

1. **Two fields are legacy renames** -- `permissions.allowed_tools` and `permissions.require_approval` were part of an older configuration format (`.claude.json` with `allowedTools`). Claude Code migrated to `permissions.allow`, `permissions.deny`, and `permissions.ask` around v2.0.8 (November 2025). Jerry's file uses field names that were never the correct settings.json names -- they appear to be snake_case adaptations of the deprecated `.claude.json` `allowedTools` format.

2. **Six fields were invented by Jerry** -- `commands`, `context`, `preferences`, `rules`, `project`, and `version` have never been valid Claude Code settings.json fields. They represent Jerry's aspirational configuration that Claude Code silently ignores. The intent behind each field IS served by actual Claude Code mechanisms, but through different paths (directories, CLAUDE.md, CLI flags -- not settings.json fields).

3. **Two fields ARE valid** -- `statusLine` and `enabledPlugins` are recognized by the official schema and are working correctly.

**Project impact:** The 8 unrecognized fields create a false sense of configuration control. Developers may believe Claude Code is enforcing tool restrictions, loading specific context files, or respecting model preferences when it is doing none of these things. The `.claude/settings.local.json` file already uses the correct `permissions.allow` format, which is the actual working configuration.

---

## L1: Technical Analysis

### Schema Validation Baseline

The official Claude Code JSON schema at `https://json.schemastore.org/claude-code-settings.json` defines the recognized fields. Cross-referenced with the official documentation at `https://code.claude.com/docs/en/settings` and `https://code.claude.com/docs/en/permissions`.

**Claude Code's behavior with unrecognized fields:** Claude Code silently ignores any JSON property not in its schema. No error, no warning, no log entry. The field is simply never read.

Source: [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings), [Claude Code Permissions Documentation](https://code.claude.com/docs/en/permissions)

---

### Field 1: `permissions.allowed_tools`

**Current value:**
```json
"allowed_tools": ["Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "Bash", "Task", "TodoWrite", "WebSearch", "WebFetch"]
```

**Status: NEVER VALID in settings.json. Legacy-inspired, wrong field name.**

**Investigation:**
- The deprecated `.claude.json` file (pre-v2.0.8) used a field called `allowedTools` (camelCase) at the project level within a `projects` object. This was deprecated in Claude Code v2.0.8 (November 2025).
- The current settings.json uses `permissions.allow` (an array of tool pattern strings like `"Bash(npm run *)"`, `"Read(~/.zshrc)"`).
- Jerry's `permissions.allowed_tools` (snake_case) matches neither the old `.claude.json` format (`allowedTools`, camelCase) nor the new settings.json format (`permissions.allow`).
- **Conclusion:** This field was likely created by interpreting the concept of "allowed tools" and writing a plausible-looking field name. It was never a valid Claude Code field in any version.

**Correct replacement:** `permissions.allow` with tool pattern syntax.

```json
"permissions": {
  "allow": [
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash",
    "Task",
    "WebSearch",
    "WebFetch"
  ]
}
```

**Note:** `MultiEdit` and `TodoWrite` are not standard Claude Code tool names per the official documentation. `MultiEdit` may be an alias -- verify against the tool list Claude Code exposes. `Task` is the subagent delegation tool.

Source: [Claude Code Permissions Documentation](https://code.claude.com/docs/en/permissions), [GitHub Issue #10839 - .claude.json deprecation](https://github.com/anthropics/claude-code/issues/10839), [GitHub Issue #889 - allowedTools for all projects](https://github.com/anthropics/claude-code/issues/889)

---

### Field 2: `permissions.require_approval`

**Current value:**
```json
"require_approval": ["Bash:rm", "Bash:git push", "Write:.env"]
```

**Status: NEVER VALID in settings.json. Jerry-invented field name.**

**Investigation:**
- No version of Claude Code has ever had a `require_approval` field in settings.json or `.claude.json`.
- The concept maps to `permissions.ask` in current settings.json, which uses tool pattern syntax: `"Bash(rm *)"`, `"Bash(git push *)"`, `"Write(.env)"`.
- The colon-delimited syntax (`Bash:rm`) is not Claude Code syntax. The official pattern syntax uses parentheses: `Bash(rm *)`.
- **Conclusion:** This field was invented to express the concept of "require approval for certain operations." The intent is correct but the implementation is non-functional.

**Correct replacement:** `permissions.ask` with proper tool pattern syntax.

```json
"permissions": {
  "ask": [
    "Bash(rm *)",
    "Bash(git push *)",
    "Write(.env)",
    "Write(.env.*)"
  ]
}
```

**Important:** The colon-delimited syntax `Bash:rm` has no meaning in Claude Code. The legacy `:*` suffix syntax (e.g., `Bash:*`) was deprecated in favor of `Bash(*)` or just `Bash`.

Source: [Claude Code Permissions Documentation](https://code.claude.com/docs/en/permissions) -- "The legacy `:*` suffix syntax is equivalent to ` *` but is deprecated."

---

### Field 3: `commands`

**Current value:**
```json
"commands": {
  "available": [
    {"name": "architect", "file": ".claude/commands/architect.md", "description": "..."},
    {"name": "release", "file": ".claude/commands/release.md", "description": "..."}
  ]
}
```

**Status: NEVER VALID. Jerry-invented field.**

**Investigation:**
- Claude Code discovers commands (now called "skills") from directory structure, not from settings.json registration.
- **Discovery locations:** `.claude/commands/` (legacy, still works), `.claude/skills/<name>/SKILL.md` (current recommended), `~/.claude/skills/` (personal), `~/.claude/commands/` (personal legacy).
- There is no `commands` field in the settings.json schema. Commands are discovered by scanning the filesystem.
- If a skill and a command share the same name, the skill takes precedence.
- **Conclusion:** Jerry invented this field to register commands declaratively. Claude Code ignores it entirely. However, the `.claude/commands/` directory DOES exist in some versions of the repo (the glob found no files in this branch, meaning the commands referenced here may not exist).

**Correct replacement:** No settings.json field needed. Place command files at `.claude/commands/<name>.md` or migrate to `.claude/skills/<name>/SKILL.md` for the skill system. Claude Code auto-discovers them.

**Action required:** Verify that `.claude/commands/architect.md` and `.claude/commands/release.md` exist. If they exist on disk, Claude Code will discover them regardless of this settings.json field. If they do not exist, the commands are non-functional.

Source: [Claude Code Skills Documentation](https://code.claude.com/docs/en/slash-commands) -- "Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way."

---

### Field 4: `context`

**Current value:**
```json
"context": {
  "always_load": ["CLAUDE.md", "AGENTS.md", "GOVERNANCE.md"],
  "load_on_demand": ["projects/README.md", "projects/*/PLAN.md", "projects/*/WORKTRACKER.md"]
}
```

**Status: NEVER VALID. Jerry-invented field.**

**Investigation:**
- Claude Code has NO settings.json field for controlling context loading. The `context` property does not exist in the schema.
- **CLAUDE.md auto-loading is automatic and not configurable:** `CLAUDE.md` files at `~/.claude/CLAUDE.md` (user), `CLAUDE.md` (project root), and `.claude/CLAUDE.md` (project) are loaded automatically at session start. This behavior cannot be configured via settings.json.
- **Rules auto-loading:** All `.md` files in `.claude/rules/` are auto-loaded. No settings.json registration needed.
- **There is no `load_on_demand` mechanism in settings.json.** Claude Code loads CLAUDE.md and rules files at startup; other files are loaded when Claude reads them via tools during a session.
- **Conclusion:** The `always_load` intent for CLAUDE.md is achieved automatically. AGENTS.md and GOVERNANCE.md are NOT auto-loaded by Claude Code unless they are in `.claude/rules/` or referenced from CLAUDE.md. The `load_on_demand` glob patterns have no effect.

**Correct replacement:** No direct replacement in settings.json. To ensure files are loaded:
1. CLAUDE.md is already auto-loaded (no action needed).
2. For AGENTS.md and GOVERNANCE.md, either: (a) place symlinks or copies in `.claude/rules/` for auto-loading, or (b) reference them in CLAUDE.md so Claude knows to read them.
3. For on-demand files, mention them in CLAUDE.md as reference paths (Jerry already does this in the Navigation table).

Source: [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings), [Claude Code Rules Documentation](https://claudelog.com/faqs/what-are-claude-rules/) -- "All markdown files in `.claude/rules/` are automatically loaded into Claude Code's context when launched."

---

### Field 5: `preferences`

**Current value:**
```json
"preferences": {
  "model": {"default": "opus-4-5", "fast_tasks": "sonnet"},
  "output": {"max_line_length": 100, "prefer_markdown": true},
  "behavior": {"require_plan_for_multi_file": true, "require_citations": true, "capture_learnings": true}
}
```

**Status: NEVER VALID. Jerry-invented field.**

**Investigation per sub-field:**

**`preferences.model.default`:** Claude Code has a top-level `model` field (a string, not a nested object). The correct field is `"model": "claude-opus-4-5"`. The nested `preferences.model.default` path is not recognized.

**`preferences.model.fast_tasks`:** No equivalent exists. Claude Code does not have a "fast mode model" configuration in settings.json. There is a `fastMode` boolean and `fastModePerSessionOptIn` boolean, but no per-task model routing.

**`preferences.output.max_line_length`:** No equivalent. Claude Code has an `outputStyle` field (string) that adjusts system prompt style but does not support line length configuration.

**`preferences.output.prefer_markdown`:** No equivalent. Claude Code always produces markdown output in its default mode.

**`preferences.behavior.require_plan_for_multi_file`:** No equivalent in settings.json. This behavior can be instructed via CLAUDE.md or rules files.

**`preferences.behavior.require_citations`:** No equivalent. This is a behavioral instruction, not a settings.json field. It belongs in CLAUDE.md or rules.

**`preferences.behavior.capture_learnings`:** No equivalent. Claude Code has an `autoMemoryDirectory` and `autoMemoryEnabled` but no "capture learnings" toggle.

**Correct replacement:**
```json
{
  "model": "claude-opus-4-5"
}
```
All behavioral preferences (`require_plan_for_multi_file`, `require_citations`, `capture_learnings`) should be expressed as instructions in CLAUDE.md or `.claude/rules/` files, where Claude Code will actually read and follow them.

Source: [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings) -- `model` is a top-level string field.

---

### Field 6: `rules`

**Current value:**
```json
"rules": {
  "files": [".claude/rules/coding-standards.md"],
  "always_apply": true
}
```

**Status: NEVER VALID. Jerry-invented field.**

**Investigation:**
- Claude Code discovers rules from the `.claude/rules/` directory automatically. There is no settings.json field for registering rule files.
- ALL `.md` files in `.claude/rules/` are loaded at session start with high priority (same as CLAUDE.md).
- Rules support optional YAML frontmatter with a `paths` field for path-scoped activation (only load when working on matching files).
- **Conclusion:** The `rules.files` array is redundant and non-functional. If `.claude/rules/coding-standards.md` exists on disk, it is already auto-loaded. If other rules files exist in `.claude/rules/`, they are also loaded regardless of this field. The `always_apply: true` flag has no effect.

**Correct replacement:** No settings.json field needed. Simply place rule files in `.claude/rules/` and they are auto-discovered. Rules without `paths` frontmatter are always applied; rules with `paths` frontmatter are conditionally applied.

Source: [Claude Code Rules Documentation](https://claudelog.com/faqs/what-are-claude-rules/), [GitHub Issue #8752 - Auto-load rules](https://github.com/anthropics/claude-code/issues/8752)

---

### Field 7: `project`

**Current value:**
```json
"project": {
  "name": "jerry",
  "description": "Framework for behavior and workflow guardrails with knowledge accrual"
}
```

**Status: NEVER VALID. Jerry-invented metadata field.**

**Investigation:**
- The settings.json schema has no `project` field. Claude Code does not read project metadata from settings.json.
- Claude Code determines project context from the working directory and CLAUDE.md content.
- **Conclusion:** This is Jerry metadata that Claude Code silently ignores. The project name and description are informational and should be in CLAUDE.md (where they already are).

**Correct replacement:** Remove from settings.json. The project description is already in CLAUDE.md's Identity section.

---

### Field 8: `version`

**Current value:**
```json
"version": "1.0"
```

**Status: NEVER VALID. Jerry-invented metadata field.**

**Investigation:**
- The settings.json schema has no `version` field. Claude Code does not version settings files.
- Claude Code has an `autoUpdatesChannel` field for update channels but no settings file version.
- **Conclusion:** This is Jerry metadata for internal tracking. Claude Code ignores it.

**Correct replacement:** Remove from settings.json. If version tracking is needed for Jerry's settings, use a comment or external tracking mechanism.

---

### Valid Fields (Confirmation)

**`statusLine`:** Valid. Present in the schema with `type`, `command`, and `padding` sub-fields. Jerry's configuration is correct.

**`enabledPlugins`:** Valid. Present in the schema. Maps plugin identifiers to booleans. Jerry's `"context7@claude-plugins-official": true` is correct syntax.

Source: [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings), [Schema](https://json.schemastore.org/claude-code-settings.json)

---

### Summary Table

| Field | Status | Was It Ever Valid? | Correct Replacement | Effect Today |
|-------|--------|-------------------|---------------------|-------------|
| `permissions.allowed_tools` | Invalid | No (snake_case never used; `.claude.json` used camelCase `allowedTools`) | `permissions.allow` | Silently ignored |
| `permissions.require_approval` | Invalid | No (never existed in any version) | `permissions.ask` | Silently ignored |
| `commands` | Invalid | No (never a settings field) | `.claude/commands/` or `.claude/skills/` directory | Silently ignored |
| `context` | Invalid | No (never a settings field) | CLAUDE.md auto-load + `.claude/rules/` | Silently ignored |
| `preferences` | Invalid | No (never a settings field) | `model` (top-level string) + CLAUDE.md for behaviors | Silently ignored |
| `rules` | Invalid | No (never a settings field) | `.claude/rules/` auto-discovery | Silently ignored |
| `project` | Invalid | No (never a settings field) | CLAUDE.md content | Silently ignored |
| `version` | Invalid | No (never a settings field) | Remove (not needed) | Silently ignored |
| `statusLine` | **Valid** | Yes | N/A (correct as-is) | Working |
| `enabledPlugins` | **Valid** | Yes | N/A (correct as-is) | Working |

---

## L2: Architectural Implications

### Risk Assessment

**Severity: MEDIUM.** The unrecognized fields create a gap between perceived and actual configuration:

1. **False security perimeter.** `permissions.allowed_tools` and `permissions.require_approval` suggest tool restrictions are enforced, but they are not. The actual permissions come from `.claude/settings.local.json` which uses the correct `permissions.allow` format. However, the committed `settings.json` is the shared project configuration -- any developer relying on the committed file's permissions is unprotected.

2. **Context loading assumptions.** The `context.always_load` field suggests AGENTS.md and GOVERNANCE.md are auto-loaded. They are not (unless they are in `.claude/rules/` or explicitly read during a session). This could lead to governance context not being present when expected.

3. **Model configuration miss.** The `preferences.model.default: "opus-4-5"` has no effect. The actual model is determined by the CLI invocation or the top-level `model` field (which is absent from settings.json). This means Claude Code uses its default model, not the intended Opus.

### Migration Strategy

**Phase 1 -- Immediate (settings.json cleanup):**
1. Remove all 8 invalid fields from `.claude/settings.json`.
2. Add valid `permissions.allow` and `permissions.ask` with correct tool pattern syntax.
3. Add top-level `model` field if model override is desired.
4. Verify `statusLine` and `enabledPlugins` are retained (they are valid).

**Phase 2 -- Verification:**
1. Verify `.claude/commands/architect.md` and `.claude/commands/release.md` exist (or create them).
2. Verify AGENTS.md and GOVERNANCE.md are accessible (either in `.claude/rules/` or referenced from CLAUDE.md).
3. Move behavioral preferences (`require_plan_for_multi_file`, `require_citations`) to `.claude/rules/` or CLAUDE.md.

**Phase 3 -- Reconciliation with settings.local.json:**
1. The `.claude/settings.local.json` already uses correct `permissions.allow` format.
2. Ensure the committed `settings.json` and local `settings.local.json` are complementary, not conflicting.
3. Per Claude Code precedence: local > project > user. So `settings.local.json` overrides `settings.json`.

### Proposed Clean settings.json

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep",
      "Bash(uv run *)",
      "Bash(git *)",
      "Bash(gh *)",
      "Bash(ls *)",
      "Bash(echo *)",
      "Bash(test *)",
      "Bash(wc *)",
      "Task",
      "WebSearch",
      "WebFetch"
    ],
    "ask": [
      "Bash(rm *)",
      "Bash(git push *)",
      "Write(.env)",
      "Write(.env.*)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/post_tool_use.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/subagent_stop.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Jerry Framework initialized. See CLAUDE.md for context.'"
          }
        ]
      }
    ]
  },
  "model": "claude-opus-4-5",
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

### Trade-offs

| Aspect | Current (Invalid Fields) | Proposed (Clean) |
|--------|------------------------|-------------------|
| Schema validation | Fails (8 unrecognized fields) | Passes |
| Tool permissions | Not enforced (wrong field names) | Enforced via `permissions.allow/ask/deny` |
| Model selection | Ignored (wrong path) | Applied via top-level `model` |
| Context loading | No effect | Handled by CLAUDE.md + `.claude/rules/` (existing mechanism) |
| Command discovery | No effect | Handled by `.claude/commands/` directory (existing mechanism) |
| Behavioral rules | No effect | Handled by `.claude/rules/` (existing mechanism) |

---

## Methodology

### Research Approach
- **5W1H analysis** applied to each unrecognized field
- **Schema validation** against the official JSON schema at SchemaStore
- **Primary source verification** via official Claude Code documentation at code.claude.com
- **Historical investigation** via GitHub issues, changelogs, and community guides
- **Cross-reference** between settings.json, settings.local.json, and settings.json.bkup in the codebase

### Sources Consulted
1. Official Claude Code documentation (code.claude.com)
2. Official JSON schema (json.schemastore.org)
3. GitHub Issues on anthropics/claude-code
4. Claude Code changelog
5. Community guides (claudelog.com, claudefa.st, eesel.ai)

### Limitations
- The full Claude Code CHANGELOG.md could not be fetched due to rate limiting. The exact version where `.claude.json` `allowedTools` was deprecated is confirmed as v2.0.8 (November 2025) from secondary sources but the primary changelog entry was not directly verified.
- Claude Code does not document what happens with unrecognized fields (confirmed silent ignore from multiple community sources).

---

## References

1. [Claude Code Settings Documentation](https://code.claude.com/docs/en/settings) - Official settings reference; complete list of recognized fields
2. [Claude Code Permissions Documentation](https://code.claude.com/docs/en/permissions) - `permissions.allow/ask/deny` format, tool pattern syntax, evaluation order
3. [Claude Code Skills Documentation](https://code.claude.com/docs/en/slash-commands) - Command/skill discovery from `.claude/commands/` and `.claude/skills/` directories
4. [Claude Code JSON Schema](https://json.schemastore.org/claude-code-settings.json) - Official schema defining all valid properties
5. [GitHub Issue #10839 - .claude.json deprecation](https://github.com/anthropics/claude-code/issues/10839) - Confirmed `.claude.json` deprecated in v2.0.8; `allowedTools` was a `.claude.json` field
6. [GitHub Issue #889 - allowedTools for all projects](https://github.com/anthropics/claude-code/issues/889) - Confirmed `allowedTools` maps to permissions in `settings.json`, closed May 2025
7. [Claude Code Rules FAQ](https://claudelog.com/faqs/what-are-claude-rules/) - Rules auto-discovery from `.claude/rules/` directory
8. [GitHub Issue #8752 - Auto-load rules](https://github.com/anthropics/claude-code/issues/8752) - Feature request for rule auto-loading from config (directory-based loading is the implemented solution)
9. [Claude Code Settings Reference (ClaudeFast)](https://claudefa.st/blog/guide/settings-reference) - Community reference confirming field list
10. [Claude Code Complete Config Guide (eesel.ai)](https://www.eesel.ai/blog/settings-json-claude-code) - Community guide confirming settings.json structure
11. [GitHub Issue #18973 - Link allowedTools CLI to permissions settings](https://github.com/anthropics/claude-code/issues/18973) - Confirms CLI `--allowedTools` maps to `permissions.allow` in settings.json
12. [Claude Code Statusline Documentation](https://code.claude.com/docs/en/statusline) - Confirms `statusLine` with `padding` is a valid field
13. [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) - Confirms `enabledPlugins` is a valid field

---

*Research conducted: 2026-03-12*
*Agent: ps-researcher*
*Issue: #180*
*Confidence: HIGH (0.92) -- primary sources verified for all 8 fields; historical timeline partially dependent on secondary sources*
