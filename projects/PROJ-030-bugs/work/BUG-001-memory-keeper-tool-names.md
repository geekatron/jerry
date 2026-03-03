# BUG-001: Memory-keeper tool names mismatch across all governance files

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-26T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** PROJ-030-bugs
> **Owner:**
> **Found In:** 0.12.5
> **Fix Version:**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

All Jerry Framework governance files, agent definitions, TOOL_REGISTRY.yaml, and permission settings reference memory-keeper MCP tool names that do not exist. The actual mcp-memory-keeper server uses completely different tool names, causing MCP-002 (HARD rule) to be systematically violated -- no memory-keeper usage occurs despite rules mandating it.

**Key Details:**
- **Symptom:** Memory-keeper MCP tools are never invoked during normal workflow despite MCP-002 mandating usage at phase boundaries
- **Frequency:** Every session -- 100% failure rate
- **Workaround:** Manually call correct tool names (e.g., `mcp__memory-keeper__context_save` instead of `mcp__memory-keeper__store`)

---

## Steps to Reproduce

### Prerequisites

- Jerry Framework with mcp-memory-keeper MCP server configured
- Any orchestration workflow that triggers phase boundaries

### Steps to Reproduce

1. Start a Jerry session with an orchestration workflow
2. Complete a phase boundary where MCP-002 mandates `store` to persist phase state
3. Observe that the agent attempts to call `mcp__memory-keeper__store`
4. The tool call fails silently because `store` does not exist in the MCP server

### Expected Result

Memory-keeper `context_save` is called at phase boundaries per MCP-002, persisting phase state for cross-session handoff.

### Actual Result

No memory-keeper tool is called. The agent references nonexistent tool names (`store`, `retrieve`, `search`, `list`, `delete`) from governance files. MCP-002 is systematically violated.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS / Darwin 24.6.0 |
| **Browser/Runtime** | Claude Code CLI |
| **Application Version** | Jerry Framework 0.12.5 |
| **Configuration** | mcp-memory-keeper via `.claude/settings.local.json` |
| **Deployment** | Local development |

### Additional Environment Details

The mcp-memory-keeper npm package exposes 38 tools across 3 profiles (minimal=8, standard=22, full=38). None of the 5 tool names referenced by Jerry governance exist in the actual server API.

---

## Root Cause Analysis

### Investigation Summary

Research conducted via WebSearch and WebFetch (Context7 quota exceeded). Complete tool inventory documented in `projects/PROJ-030-bugs/research/memory-keeper-tool-name-audit.md`.

### Root Cause

The Jerry Framework governance was built against assumed tool names (`store`, `retrieve`, `search`, `list`, `delete`) that were never validated against the actual mcp-memory-keeper MCP server API. The actual server uses a `context_` prefix naming convention (`context_save`, `context_get`, `context_search`, `context_session_list`, `context_batch_delete`).

### Contributing Factors

- No validation step when MCP tool governance was created (FEAT-028)
- No integration test verifying tool name resolution
- Permission allowlist in `settings.local.json` grants access to nonexistent tools without error

---

## Acceptance Criteria

### Fix Verification

- [ ] `.context/rules/mcp-tool-standards.md` canonical tool names table references correct tool names (`context_save`, `context_get`, `context_search`, `context_session_list`, `context_batch_delete`)
- [ ] `.claude/settings.local.json` permission allowlist uses correct tool names
- [ ] `TOOL_REGISTRY.yaml` tool definitions and agent permissions use correct tool names
- [ ] L2-REINJECT markers in `mcp-tool-standards.md` reference correct tool names
- [ ] All 7 affected agent `.md` files reference correct tool names in methodology sections

### Quality Checklist

- [ ] All 30+ affected files updated with correct tool names
- [ ] Memory-keeper tools are successfully invoked during normal workflow
- [ ] No references to old tool names remain in governance files

---

## Related Items

### Hierarchy

- **Parent:** PROJ-030-bugs

### Related Items

- **GitHub Issue:** [#111](https://github.com/geekatron/jerry/issues/111)
- **Research Report:** [memory-keeper-tool-name-audit.md](../research/memory-keeper-tool-name-audit.md)
- **Affected Rule:** `.context/rules/mcp-tool-standards.md` (MCP-002 HARD rule)
- **Affected Registry:** `TOOL_REGISTRY.yaml`
- **Affected Settings:** `.claude/settings.local.json`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-26 | Claude | pending | Initial report. Research completed. 30+ affected files identified. |
