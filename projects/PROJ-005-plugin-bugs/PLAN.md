# PROJ-005: Plugin Installation Bugs

> **Project ID:** PROJ-005-plugin-bugs
> **Status:** IN PROGRESS (Reopened for BUG-007)
> **Branch:** cc/jerry-plugin-bugs
> **Created:** 2026-01-13
> **Last Updated:** 2026-01-13
> **Current Phase:** PHASE-06 Planning

---

## Overview

This project addresses critical bugs preventing the Jerry Framework plugin from functioning correctly after installation via the local marketplace strategy in Claude Code.

### Problem Statement (Original - PHASE-01 to PHASE-04)

When attempting to install the jerry-framework plugin from a local marketplace, the installation fails with validation errors:

```
Error: Failed to install: Plugin has an invalid manifest file at
.claude/plugins/cache/temp_local_1768281191752_ah91ay/.claude-plugin/plugin.json.
Validation errors: hooks: Invalid input, commands: Invalid input, skills: Invalid input,
: Unrecognized keys: "$schema", "engines", "main", "configuration", "dependencies", "capabilities"
```

**Status:** RESOLVED (PHASE-01 to PHASE-04 completed)

### Problem Statement (BUG-007 - PHASE-05+)

After successful plugin installation, the SessionStart hook fails silently. The Jerry Framework startup message does not appear, preventing project context enforcement.

**Symptom:** No startup message when starting a new Claude Code session with the plugin installed.

**Root Cause:** `scripts/session_start.py` is a "legacy wrapper" that delegates to `src/interface/cli/session_start.py`, which requires `pip install -e .` to function. This violates the plugin self-containment principle.

**Evidence:**
- `scripts/session_start.py` lines 5-6: "DEPRECATED: This script is a legacy wrapper"
- `scripts/session_start.py` lines 29-49: All execution paths require pip installation
- `hooks/hooks.json` line 10: Hook invokes the broken script

### Root Causes Identified

1. **plugin.json** - Invalid schema fields and incorrect path formats (FIXED)
2. **marketplace.json** - Invalid fields in plugin entries (FIXED)
3. **scripts/session_start.py** - Requires pip installation (BUG-007 - OPEN)

---

## Phases

### PHASE-01: Project Setup (COMPLETED)
- Create project structure
- Initialize WORKTRACKER.md
- Register in projects/README.md

### PHASE-02: Fix plugin.json (COMPLETED)
- Remove unrecognized keys ($schema, engines, main, configuration, dependencies, capabilities)
- Fix skills format (file paths → directory path)
- Add ./ prefix to commands and hooks paths

### PHASE-03: Fix marketplace.json (COMPLETED)
- Remove invalid `skills` field from plugin entry
- Remove invalid `strict` field from plugin entry
- Fix email typo (gmial → gmail)
- Add recommended marketplace metadata (version, description, category)

### PHASE-04: Verification & Testing (COMPLETED)
- Test plugin installation locally
- Verify all components discovered correctly
- Document any additional issues found

### PHASE-05: Script Pip Dependency Audit (COMPLETED)
- Discovered BUG-007: session_start.py requires pip installation
- Audited all scripts in `scripts/` directory
- **Blast Radius:** LIMITED - Only session_start.py affected
- Created `work/PHASE-BUGS.md` with detailed bug report

### PHASE-06: Fix session_start.py (READY FOR IMPLEMENTATION)

**Objective:** Rewrite `scripts/session_start.py` as a standalone script that works immediately upon plugin installation without requiring pip.

**Status:** Planning COMPLETE. Validation PASSED with GO recommendation.

#### Research & Analysis Results

| Agent | Purpose | Output | Status |
|-------|---------|--------|--------|
| ps-investigator | Analyze what session_start.py MUST do | 12 functional requirements (FR-001 to FR-012) | COMPLETED |
| ps-researcher | Research Claude Code plugin patterns/constraints | 10 patterns (P-001 to P-010), constraint checklist | COMPLETED |
| ps-analyst | Analyze trade-offs between approaches | **Option B recommended** (score 4.1/5.0) | COMPLETED |
| ps-architect | Propose solution architecture | ADR-PROJ005-001 with implementation blueprint | COMPLETED |
| ps-validator | Validate solution against constraints | **GO recommendation** - all constraints passed | COMPLETED |

#### Approved Solution: Option B - Simplified Plugin Mode

**Decision:** Implement a single-file, stdlib-only solution (~80 lines).

| Aspect | Details |
|--------|---------|
| Effort | ~80 lines, Python stdlib only |
| Coverage | 10/12 functional requirements |
| Risk | Lowest (2 issues vs 3-4 for alternatives) |
| Trade-off | Defers local context loading, layered config |

#### Validation Summary

| Category | Pass | Fail | Result |
|----------|------|------|--------|
| Hard Constraints | 7/7 | 0 | PASS |
| Functional Requirements | 10/12 | 0 | PASS (2 deferred) |
| Contract Tests | 13/13 | 0 | PASS |
| Pattern Compliance | 7/7 | 0 | PASS |

#### Acceptance Criteria (Validated)

- [ ] `scripts/session_start.py` uses only Python stdlib (os, re, json, pathlib)
- [ ] SessionStart hook produces valid output for all 3 tag types
- [ ] Project context detection works correctly via JERRY_PROJECT env var
- [ ] No import errors when executed standalone
- [ ] Follows patterns from safe scripts (P-001 to P-010)
- [ ] Exit code is always 0
- [ ] All 13 contract test requirements satisfied

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

### Installation (PHASE-01 to PHASE-04) - COMPLETED
- [x] Plugin installs successfully via local marketplace
- [x] All skills discovered from ./skills/ directory
- [x] All commands discovered from ./commands/ directory
- [x] Hooks registered from ./hooks/hooks.json
- [x] No validation errors or warnings during installation

### Runtime (PHASE-05 to PHASE-06) - IN PROGRESS
- [ ] SessionStart hook executes successfully
- [ ] Jerry Framework startup message appears
- [ ] Project context detection works
- [ ] All hooks work without pip installation

---

## Related Files

| File | Purpose | Status |
|------|---------|--------|
| `.claude-plugin/plugin.json` | Plugin manifest | FIXED |
| `.claude-plugin/marketplace.json` | Local marketplace configuration | FIXED |
| `skills/` | Auto-discovered skills | OK |
| `commands/` | Slash commands | OK |
| `hooks/hooks.json` | Lifecycle hooks | OK |
| `scripts/session_start.py` | SessionStart hook script | **BUG-007** |
| `scripts/pre_tool_use.py` | PreToolUse hook script | OK (standalone) |
| `scripts/subagent_stop.py` | SubagentStop hook script | OK (standalone) |
| `scripts/post_tool_use.py` | PostToolUse hook script | OK (standalone) |
| `src/interface/cli/session_start.py` | Full session start implementation | Reference only |

---

## Research Artifacts (PHASE-06)

| Artifact | Location | Status |
|----------|----------|--------|
| Functional Requirements | `investigations/PROJ-005-e-006-functional-requirements.md` | COMPLETED |
| Plugin Patterns Research | `research/PROJ-005-e-007-plugin-patterns.md` | COMPLETED |
| Trade-off Analysis | `analysis/PROJ-005-a-001-tradeoffs.md` | COMPLETED |
| Architecture Decision | `decisions/ADR-PROJ005-001-standalone-session-start.md` | COMPLETED |
| Validation Report | `analysis/PROJ-005-a-002-validation.md` | COMPLETED |
