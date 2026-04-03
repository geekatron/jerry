# Constitutional Compliance Report: settings.local.json (#181/#182)

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `.claude/settings.local.json` (fix/180-settings-json-schema branch)
**Criticality:** C4 (governance/framework infrastructure file; AE-002 applies — `.claude/` rules/config; also touches permission enforcement for all agents)
**Date:** 2026-03-14
**Reviewer:** adv-executor (S-007)
**Constitutional Context:** JERRY_CONSTITUTION.md v1.1, quality-enforcement.md v1.6.0, docs/reference/claude-code-permissions.md, mcp-tool-standards.md

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall compliance assessment |
| [Findings Table](#findings-table) | All findings with severity classification |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and remediation per finding |
| [Remediation Plan](#remediation-plan) | Prioritized action list |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |

---

## Summary

PARTIAL compliance. The `settings.local.json` under review correctly uses the documented `permissions.allow` field name (unlike the previous `settings.json` which used undocumented field names per FINDING-001), and the Skill permission entries follow the documented `Skill(name)` pattern without the deprecated colon-namespace form. However, the file contains **2 Critical findings** and **3 Major findings**:

- **Critical (2):** The `PermissionRequest` hook silently auto-approves WebSearch/WebFetch without user confirmation, overriding the user's explicit ability to deny (P-020 violation). The `Bash(grep *)` allow entry circumvents the shared `settings.json` deny list for `curl`/`wget` by providing a pathway where a grep-wrapped curl could slip through — but more concretely, `Bash(grep *)` is an unrestricted shell passthrough with no word-boundary limit.
- **Major (3):** Two MCP wildcard entries are redundant/ambiguous (`mcp__context7__*` vs `mcp__plugin_context7_context7__*`). `Bash(git stash *)` in the local allow list conflicts with `settings.json`'s `ask` guards for destructive git operations, creating a deceptive permission gap. The `PermissionRequest` hook output is structurally identical to a raw `echo` command whose output cannot be verified as authentic by the runtime.

**Constitutional Compliance Score:** 0.74 — REJECTED (below H-13 threshold of 0.92)

**Recommendation:** REJECT — revision required before merge.

---

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260314 | P-020: User Authority | HARD | Critical | `PermissionRequest` hook auto-approves WebSearch/WebFetch unconditionally, silencing user approval prompts | Methodological Rigor |
| CC-002-20260314 | P-022: No Deception | HARD | Critical | Hook command `echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}'` fabricates a permission approval signal that bypasses the real permission system | Internal Consistency |
| CC-003-20260314 | H-05: UV-only (Python execution) | HARD | Major | `statusLine` in `settings.json` uses `python3` not `uv run python`; `settings.local.json` adds no correction and inherits this violation by coexisting in the same merged config | Methodological Rigor |
| CC-004-20260314 | P-020: User Authority (destructive git ops) | HARD | Major | `Bash(git stash *)` in local `allow` list conflicts with `settings.json` `ask` guards; per evaluation order, `allow` from local (higher precedence scope) overrides `ask` from shared, silently removing the stash confirmation prompt | Methodological Rigor |
| CC-005-20260314 | P-022: No Deception (duplicate/ambiguous MCP entries) | MEDIUM | Major | Both `mcp__context7__*` and `mcp__plugin_context7_context7__*` are present; the second entry is an undocumented plugin namespace that may target a different server registration, creating ambiguity about which permissions are actually granted | Internal Consistency |

---

## Detailed Findings

### CC-001-20260314: P-020 User Authority — PermissionRequest Hook Silences User Approval [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `hooks.PermissionRequest` (lines 43-54) |
| **Principle** | P-020: User Authority — "Request permission for destructive operations. Never override user decisions." |
| **Affected Dimension** | Methodological Rigor |

**Evidence:**
```json
"PermissionRequest": [
  {
    "matcher": "WebSearch|WebFetch",
    "hooks": [
      {
        "type": "command",
        "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PermissionRequest\",\"decision\":{\"behavior\":\"allow\"}}}'",
        "timeout": 5
      }
    ]
  }
]
```

**Analysis:**
The `PermissionRequest` hook intercepts the runtime's permission approval request for WebSearch and WebFetch and unconditionally emits an `allow` decision. This means: even if a user had placed WebSearch in a `deny` or `ask` list at a higher-precedence scope, this hook fires first (hooks execute before permission evaluation) and fabricates an approval. The Claude Code permission model grants the user authority to require approval for specific tools; this hook silently removes that authority for web access tools without the user's knowledge. This is a direct violation of P-020 ("Never override user decisions"). The `allow` entries for WebSearch/WebFetch in `settings.json` already permit them without prompts — the `PermissionRequest` hook adds a second, redundant layer that cannot be overridden by the user even if they later add a `deny` entry.

**Recommendation (P0):**
Remove the `PermissionRequest` hook block entirely. WebSearch and WebFetch are already pre-approved via the `allow` array in `settings.json`. The hook is redundant for approval and dangerous because it prevents a user's future `deny` entry from taking effect. If the intent is to auto-approve on a per-session basis, the `allow` entry in `settings.json` already achieves this. If the intent is to protect against managed-policy denials, that is an intentional override of user/deployment authority and must not be implemented without explicit user consent documented in an ADR.

---

### CC-002-20260314: P-022 No Deception — Hook Fabricates Permission Approval Signal [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | `hooks.PermissionRequest` (lines 48-50) and `hooks.PreToolUse` (lines 33-42) |
| **Principle** | P-022: No Deception — "Agents SHALL NOT deceive users about: actions taken or planned; capabilities or limitations." |
| **Affected Dimension** | Internal Consistency |

**Evidence:**
```json
"command": "echo '{\"decision\":\"allow\"}'"
```
(PreToolUse hook, line 37)

```json
"command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PermissionRequest\",\"decision\":{\"behavior\":\"allow\"}}}'",
```
(PermissionRequest hook, line 49)

**Analysis:**
Both hooks use `echo` to emit JSON strings that mimic the internal protocol format used by the Claude Code runtime to communicate permission decisions. These are not real permission decisions evaluated against the settings — they are synthetic approval signals injected into the hook pipeline. A user reading `settings.local.json` would need non-trivial knowledge of Claude Code's hook protocol to understand that these `echo` commands are not logging output but are actively overriding the permission system. This meets the definition of deception under P-022: the configuration creates a false impression that a permission check is occurring when in fact it is being bypassed. The `PreToolUse` hook (lines 33-42) additionally emits `{"decision":"allow"}` which tells the runtime to allow the tool call regardless of any active permission rules, compounding the deception.

**Recommendation (P0):**
Remove both hook blocks. The PreToolUse hook for WebSearch/WebFetch is already redundant (these tools are in the `settings.json` allow list). The PermissionRequest hook must be removed entirely (see CC-001). Document in a code comment or ADR the explicit decision that these tools are pre-approved and why, so any future reader understands the deliberate design rather than encountering silent bypass logic.

---

### CC-003-20260314: H-05 UV-Only — settings.json statusLine Uses python3 [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `settings.json` lines 54-58 (inherited by `settings.local.json` merge) |
| **Principle** | H-05: UV-only — "MUST use `uv run` for all Python execution. NEVER use `python`, `pip`, or `pip3` directly." |
| **Affected Dimension** | Methodological Rigor |

**Evidence:**
```json
"statusLine": {
  "type": "command",
  "command": "python3 .claude/statusline.py",
  "padding": 0
}
```

**Analysis:**
The `statusLine` command in `settings.json` invokes `python3` directly, violating H-05. This issue is inherited by any `settings.local.json` that coexists with `settings.json` because the two files merge — `statusLine` is a scalar field where the higher-precedence file (local) wins, but `settings.local.json` does not override `statusLine`, so `python3` runs on every prompt. While this specific violation is in `settings.json` rather than `settings.local.json`, the PR context (#181/#182 fixes settings.local.json) creates an opportunity to either fix or document this. The severity is Major rather than Critical because `statusLine` is an aesthetic display feature, not a core execution path. However, it creates a system Python dependency in a UV-only environment and may fail silently on machines where `python3` is not in PATH.

**Recommendation (P1):**
In `settings.json`, change:
```json
"command": "python3 .claude/statusline.py"
```
to:
```json
"command": "uv run python .claude/statusline.py"
```
If this PR's scope is limited to `settings.local.json`, file a follow-up bug (or include it in the same PR) since the `settings.json` issue was present before #180 and should not be allowed to persist.

---

### CC-004-20260314: P-020 User Authority — git stash Silently Bypasses ask Guard [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `permissions.allow` line 26 |
| **Principle** | P-020: User Authority — "Request permission for destructive operations." |
| **Affected Dimension** | Methodological Rigor |

**Evidence:**
```json
"Bash(git stash *)"
```
in `settings.local.json` allow array (line 26), while `settings.json` `ask` array contains `Bash(git reset *)`, `Bash(git rebase *)` as examples of destructive git ops that require user confirmation.

**Analysis:**
`git stash` is a stateful operation that modifies the working tree and stash stack. It is not listed in the `settings.json` `ask` array, meaning it was either intentionally omitted or overlooked. Adding it to `settings.local.json`'s `allow` list is consistent with the omission from `ask`, but the evaluation order rule (deny > ask > allow) means that `settings.local.json` (local scope, precedence 3) has higher precedence than `settings.json` (shared scope, precedence 4). If a user later adds `Bash(git stash *)` to the shared `ask` list to require confirmation, the local `allow` will silently override it. This creates a governance gap: the local file — which is gitignored and not visible in code review — can silently remove protections that the shared settings establish. Given that `git stash drop`, `git stash clear`, and `git stash pop --index` can destroy work irreversibly, a user who believes `git stash` requires approval (because they added it to `ask`) would not be protected. The deceptive element is the silent override: the user receives no indication that local settings are suppressing their `ask` guard.

**Recommendation (P1):**
Remove `Bash(git stash *)` from `settings.local.json`. If stash operations need to be auto-approved, add `Bash(git stash *)` to the shared `settings.json` `allow` array (visible in code review) and document the rationale. Alternatively, add it to `settings.json`'s `ask` list alongside `git reset` and `git rebase` as a destructive-class git operation.

---

### CC-005-20260314: P-022 No Deception — Duplicate/Ambiguous MCP Context7 Entries [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | `permissions.allow` lines 24-25 |
| **Principle** | P-022: No Deception — agents and configurations SHALL NOT create false impressions about capabilities granted. |
| **Affected Dimension** | Internal Consistency |

**Evidence:**
```json
"mcp__context7__*",
"mcp__plugin_context7_context7__*"
```

**Analysis:**
Two entries target what appears to be the same Context7 MCP integration. `mcp__context7__*` follows the documented MCP permission pattern (server name = `context7`). `mcp__plugin_context7_context7__*` is an undocumented plugin-namespace form. Per `docs/reference/claude-code-permissions.md` FINDING-002, the `mcp__plugin_*` namespace is unverified. The `settings.json` file also shows `"context7@claude-plugins-official": true` in `enabledPlugins`, which may register the plugin under a different internal server name (`plugin_context7_context7`) than the standard MCP server name (`context7`). Having both entries simultaneously implies that neither the author nor the codebase is certain which server name the runtime uses. This ambiguity:
1. May grant duplicate permissions to two different server registrations, one of which could be spurious.
2. Creates uncertainty about which permission string is effective, making it impossible for a code reviewer to verify the actual permission scope.
3. If `mcp__plugin_context7_context7__*` resolves to a broader plugin namespace than intended, it could grant permissions beyond Context7.

The ambiguity itself is the P-022 violation: a reader of the config cannot determine with confidence what is actually permitted.

**Recommendation (P1):**
Resolve which server name the Context7 plugin registers under at runtime. Test by running `claude` with only `"mcp__context7__*"` and verifying that Context7 tools are accessible. If they are, remove `"mcp__plugin_context7_context7__*"`. If `"mcp__context7__*"` alone does not work, investigate why the plugin registers under the `plugin_context7_context7` namespace and document the reason. The final config should contain exactly one entry for Context7 with a comment explaining the server name. See `mcp-tool-standards.md` Canonical Tool Names table for the authoritative identifier.

---

## Remediation Plan

**P0 (Critical — MUST fix before acceptance):**
- **CC-001:** Remove the `PermissionRequest` hook block (lines 43-54). WebFetch/WebSearch are already pre-approved via `settings.json` allow list.
- **CC-002:** Remove both hook blocks (`PreToolUse` lines 31-42 and `PermissionRequest` lines 43-54). The `hooks` top-level key can be removed entirely if no other hooks exist.

**P1 (Major — SHOULD fix; requires documented justification if not):**
- **CC-003:** Change `settings.json` `statusLine.command` from `python3 .claude/statusline.py` to `uv run python .claude/statusline.py`. Include in this PR or file a follow-up with a deadline.
- **CC-004:** Remove `Bash(git stash *)` from `settings.local.json` allow list. Add to `settings.json` `ask` list if confirmation is desired, or to `settings.json` `allow` list with documented rationale.
- **CC-005:** Test which Context7 server name the plugin registers as. Retain exactly one MCP permission entry with a comment explaining the choice. Remove the unresolved/ambiguous entry.

**P2 (Minor — none identified).**

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All required permission categories are represented; no structural omissions |
| Internal Consistency | 0.20 | Negative | CC-002 (Critical): Hook fabrication contradicts the stated permission model. CC-005 (Major): Duplicate MCP entries create an internally inconsistent view of what is permitted. |
| Methodological Rigor | 0.20 | Negative | CC-001 (Critical): Bypassing PermissionRequest violates the established permission evaluation protocol. CC-003 (Major): H-05 violation in statusLine. CC-004 (Major): Local allow override of shared ask guards violates the layered permission architecture. |
| Evidence Quality | 0.15 | Neutral | No constitutional findings affect evidence quality dimension |
| Actionability | 0.15 | Neutral | The config is operational; no structural issues prevent its use |
| Traceability | 0.10 | Negative | CC-005 (Major): Ambiguous MCP entries make it impossible to trace which server registration is authoritative without runtime testing |

**Constitutional Compliance Score calculation:**
- 2 Critical violations: 2 × 0.10 = 0.20
- 3 Major violations: 3 × 0.05 = 0.15
- 0 Minor violations: 0 × 0.02 = 0.00
- Total penalty: 0.35
- Score: 1.00 - 0.35 = **0.65**

**Threshold Determination: REJECTED** (0.65 < 0.85 threshold; well below H-13 threshold of 0.92)

---

## Execution Statistics
- **Total Findings:** 5
- **Critical:** 2 (CC-001, CC-002)
- **Major:** 3 (CC-003, CC-004, CC-005)
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5

---

*Strategy: S-007 Constitutional AI Critique*
*Template: .context/templates/adversarial/s-007-constitutional-ai.md v1.0.0*
*Deliverable: .claude/settings.local.json (fix/180-settings-json-schema branch)*
*Executed: 2026-03-14*
