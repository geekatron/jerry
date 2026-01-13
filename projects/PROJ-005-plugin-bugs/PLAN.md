# PROJ-005: Plugin Installation Bugs

> **Project ID:** PROJ-005-plugin-bugs
> **Status:** IN PROGRESS
> **Branch:** cc/jerry-plugin-bugs
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13

---

## Overview

This project addresses critical bugs preventing the Jerry Framework plugin from being installed via the local marketplace strategy in Claude Code.

### Problem Statement

When attempting to install the jerry-framework plugin from a local marketplace, the installation fails with validation errors:

```
Error: Failed to install: Plugin has an invalid manifest file at
.claude/plugins/cache/temp_local_1768281191752_ah91ay/.claude-plugin/plugin.json.
Validation errors: hooks: Invalid input, commands: Invalid input, skills: Invalid input,
: Unrecognized keys: "$schema", "engines", "main", "configuration", "dependencies", "capabilities"
```

### Root Causes Identified

1. **plugin.json** - Invalid schema fields and incorrect path formats
2. **marketplace.json** - Invalid fields in plugin entries

---

## Phases

### PHASE-01: Project Setup
- Create project structure
- Initialize WORKTRACKER.md
- Register in projects/README.md

### PHASE-02: Fix plugin.json (COMPLETED)
- Remove unrecognized keys ($schema, engines, main, configuration, dependencies, capabilities)
- Fix skills format (file paths → directory path)
- Add ./ prefix to commands and hooks paths

### PHASE-03: Fix marketplace.json
- Remove invalid `skills` field from plugin entry
- Remove invalid `strict` field from plugin entry
- Fix email typo (gmial → gmail)
- Add recommended marketplace metadata (version, description, category)

### PHASE-04: Verification & Testing
- Test plugin installation locally
- Verify all components discovered correctly
- Document any additional issues found

---

## Evidence Sources

All changes are validated against Context7 documentation for Claude Code:

| Source | Library ID | Description |
|--------|------------|-------------|
| Context7 | `/anthropics/claude-code` | Official Claude Code plugin documentation |
| GitHub | `anthropics/claude-code/plugins/plugin-dev` | Plugin development reference |

### Key Documentation References

1. **Manifest Reference** - `plugins/plugin-dev/skills/plugin-structure/references/manifest-reference.md`
2. **Plugin Structure** - `plugins/plugin-dev/skills/plugin-structure/SKILL.md`
3. **Marketplace Schema** - Context7 "Configure Plugin Marketplace with JSON Schema"

---

## Success Criteria

- [ ] Plugin installs successfully via local marketplace
- [ ] All skills discovered from ./skills/ directory
- [ ] All commands discovered from ./commands/ directory
- [ ] Hooks registered from ./hooks/hooks.json
- [ ] No validation errors or warnings during installation

---

## Related Files

| File | Purpose |
|------|---------|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `.claude-plugin/marketplace.json` | Local marketplace configuration |
| `skills/` | Auto-discovered skills |
| `commands/` | Slash commands |
| `hooks/hooks.json` | Lifecycle hooks |
