# Strategy Execution Report: FMEA (Failure Mode and Effects Analysis)

## Execution Context
- **Strategy:** S-012 (FMEA -- Failure Mode and Effects Analysis)
- **Template:** `.context/templates/adversarial/s-012-fmea.md`
- **Deliverable:** `projects/PROJ-030-bugs/research/context7-plugin-architecture.md`
- **Criticality:** C4
- **Quality Threshold:** >= 0.95
- **Executed:** 2026-02-26T12:00:00Z
- **Execution ID:** 20260226T1200
- **H-16 Status:** S-012 is not directly named in H-16. H-16 applies to S-002/S-004/S-001. Proceeding per template ordering guidance.

---

# FMEA Report: Context7 Plugin Architecture and Claude Code Integration

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-030-bugs/research/context7-plugin-architecture.md`
**Criticality:** C4
**Date:** 2026-02-26
**Reviewer:** adv-executor (S-012)
**H-16 Compliance:** S-012 operates within C4 sequence. H-16 specifically governs S-002/S-004/S-001.
**Elements Analyzed:** 18 | **Failure Modes Identified:** 32 | **Total RPN:** 5,334

---

## Summary

The research report on Context7 Plugin Architecture is substantively strong in documenting the dual-namespace problem and its effects, but exhibits critical weaknesses in three areas: (1) the recommendation section presents a binary false dichotomy without validating the recommended fix's feasibility against known constraints, (2) the permission system analysis contains a contradiction about wildcard syntax that was not reconciled, and (3) the subagent MCP access gap finding lacks a concrete verification procedure, leaving implementers unable to confirm whether the mitigation resolves the root cause. The overall assessment is **REVISE BEFORE ACCEPTANCE** -- the report correctly identifies the bug class and root cause but requires targeted corrections to recommendations (FM-001, FM-003, FM-009) and evidence gaps (FM-006, FM-012) before it can guide reliable remediation.

---

## Element Inventory

| ID | Element | Description |
|----|---------|-------------|
| E-01 | L0 Executive Summary | Non-technical framing of the dual-namespace problem |
| E-02 | L1.1 Dual Configuration Methods | Technical description of Plugin vs Manual MCP installation |
| E-03 | L1.2 Dual Registration Description | Analysis of Jerry's current `settings.local.json` hedge pattern |
| E-04 | L1.3 Tool Name Resolution Rules | Table of naming patterns by config method |
| E-05 | L1.4 Permission System Analysis | Analysis of wildcard vs server-level permission syntax |
| E-06 | L1.5 Agent Definition mcpServers Field | Behavior of `mcpServers` frontmatter in subagents |
| E-07 | L1.6 Wildcard Behavior Across Namespaces | Analysis of namespace non-transitivity |
| E-08 | L1.7 Context7 Actual Tools | Enumeration of Context7's two tools |
| E-09 | L2.1 Dual-Registration Anti-Pattern | Architectural analysis of dual-registration consequences |
| E-10 | L2.2 Subagent MCP Access Gap | Analysis of project-scope vs user-scope accessibility |
| E-11 | L2.3 Tool Name Length Risk | 64-character limit analysis |
| E-12 | L2.4 Recommended Architecture | Option table comparing plugin-only vs manual-only |
| E-13 | L2.5 Impact on TOOL_REGISTRY.yaml | Impact assessment on registry file |
| E-14 | L2.6 Governance File Impact Assessment | Per-file assessment of what changes are needed |
| E-15 | Research Questions (RQ-1 to RQ-5) | Five research questions with answers and confidence ratings |
| E-16 | Methodology | Sources, approach, and limitations |
| E-17 | Recommendations | Immediate, Short-Term, and Long-Term action items |
| E-18 | References | 12 cited sources |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action Summary | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|---------------------------|--------------------|
| FM-001-20260226T1200 | E-12 L2.4 Recommended Architecture | Recommendation validates only tool names but ignores whether user-scoped manual MCP server is compatible with Jerry's worktree isolation architecture | 9 | 7 | 8 | 504 | Critical | Add a validation step confirming user-scoped MCP survives worktree context switching | Completeness |
| FM-002-20260226T1200 | E-05 L1.4 Permission System | Contradictory claims: "wildcards not supported" (Issue #3107) vs "both syntaxes now work" (docs) -- contradiction acknowledged but left unresolved | 7 | 9 | 3 | 189 | Major | Explicitly state which syntax Jerry's `settings.local.json` should use, with rationale for choosing between the two | Internal Consistency |
| FM-003-20260226T1200 | E-17 Recommendations | Recommendation #1 omits a rollback plan if user-scoped Context7 does not work in subagents (no contingency for the recommended fix failing) | 8 | 6 | 7 | 336 | Critical | Add explicit contingency: if user-scoped fix does not resolve subagent access, escalate to plugin-only with updated agent definitions | Completeness |
| FM-004-20260226T1200 | E-16 Methodology | Limitation "could not verify runtime behavior empirically" is stated but not flagged as a threat to recommendation confidence; confidence rating remains HIGH despite unverified claims | 7 | 7 | 5 | 245 | Critical | Downgrade recommendation confidence to MEDIUM or annotate HIGH confidence with the caveat that runtime validation is pending | Evidence Quality |
| FM-005-20260226T1200 | E-10 L2.2 Subagent MCP Access Gap | Mitigation ("configure at user scope") is stated without a verification procedure -- implementer cannot confirm whether the fix worked | 8 | 6 | 7 | 336 | Critical | Add a verification command (e.g., `claude mcp list --scope user` output expected) and test step for subagent Context7 access | Actionability |
| FM-006-20260226T1200 | E-02 L1.1 Dual Configuration Methods | Plugin naming pattern documented as `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` but the source for WHY the server-name is also `context7` (same as plugin-name) is not cited -- circular naming origin is asserted without primary source | 5 | 6 | 6 | 180 | Major | Cite the specific documentation or source confirming that the plugin-internal MCP server name is `context7` and not a different identifier | Evidence Quality |
| FM-007-20260226T1200 | E-12 L2.4 Recommended Architecture | The option table marks "Cons" for manual-server-only as "Manual updates, no marketplace benefits" but omits the most significant con: user-scope MCP affects ALL Claude Code projects for that user, not just Jerry | 7 | 7 | 8 | 392 | Critical | Add "User-scope config is global -- affects all Claude Code projects on this machine" as a Con in the option table | Completeness |
| FM-008-20260226T1200 | E-14 L2.6 Governance File Impact | `settings.json` fix listed as "Remove plugin entry" but no verification that removing the plugin does not break other functionality that may depend on the plugin-form Context7 | 6 | 5 | 7 | 210 | Critical | Add a dependency check: confirm no other Jerry component depends on the plugin registration before recommending removal | Completeness |
| FM-009-20260226T1200 | E-17 Recommendations | Recommendation #4 ("add a pre-flight check") lacks an owner, toolchain, and concrete implementation path -- presented as a vague aspiration | 5 | 8 | 4 | 160 | Major | Specify: the pre-flight check should be a Jerry CLI command (`jerry mcp validate`) or a shell script, and identify which team/enabler owns implementation | Actionability |
| FM-010-20260226T1200 | E-03 L1.2 Dual Registration | The "defensive workaround" characterization is accurate but the report does not assess whether the dual-permission approach is currently WORKING -- it may be that the workaround is functional despite being non-ideal | 5 | 5 | 6 | 150 | Major | Add a section confirming or refuting whether the current dual-permission workaround achieves functional Context7 access for agents | Internal Consistency |
| FM-011-20260226T1200 | E-06 L1.5 Agent Definition mcpServers | "Subagents cannot access project-scoped MCP servers" is cited from a single GitHub issue (#13898); no corroborating source or official documentation confirms this as a designed behavior vs a bug that may be fixed | 7 | 6 | 6 | 252 | Critical | Cross-reference Issue #13898 against the official Claude Code subagent documentation to confirm this is documented behavior, not a bug pending fix | Evidence Quality |
| FM-012-20260226T1200 | E-15 Research Questions | RQ-4 answer conflates two distinct scenarios (tools omitted vs mcpServers specified) without clearly separating which applies to Jerry's actual subagent configuration | 5 | 6 | 5 | 150 | Major | Rewrite RQ-4 to separately answer for Jerry's specific case: does specifying `mcpServers: [context7]` in an agent definition work when Context7 is project-scoped? | Internal Consistency |
| FM-013-20260226T1200 | E-01 L0 Executive Summary | "Badge number" analogy is accessible but imprecise -- it suggests the two registrations refer to the SAME entity, while in reality they may be different runtime instances (plugin could auto-update independently) | 3 | 5 | 5 | 75 | Minor | Add a note that the two registrations may also differ in version/state, not just naming | Internal Consistency |
| FM-014-20260226T1200 | E-11 L2.3 Tool Name Length Risk | Character counts are stated (49, 42 chars) as "safe" but the 64-char limit source is not cited -- the claim that 64 chars is the limit is unverified | 5 | 4 | 5 | 100 | Major | Cite the source of the 64-character limit (Issue #20983 text or official Claude API documentation) | Evidence Quality |
| FM-015-20260226T1200 | E-09 L2.1 Dual-Registration Anti-Pattern | "Namespace ambiguity" consequence claims "depending on which registration wins at runtime" but does not document HOW the winner is determined -- load order? last-wins? conflict resolution behavior is unspecified | 6 | 6 | 7 | 252 | Critical | Document the runtime precedence rule: which registration wins when both Plugin and Manual MCP server configurations are present for the same tool name | Completeness |
| FM-016-20260226T1200 | E-07 L1.6 Wildcard Behavior | The negative answer ("NO, mcp__context7__* does not grant access to plugin namespace") is well-argued but the argument relies on interpretation of permission entries in `settings.local.json` as "empirical evidence" -- this is circular (the settings.local.json author may have listed both out of caution, not because one alone failed) | 6 | 5 | 6 | 180 | Major | Provide a non-circular evidence source for namespace non-transitivity -- cite Issue #20983 or docs directly proving the permission match is server-name-based | Evidence Quality |
| FM-017-20260226T1200 | E-17 Recommendations | Long-term recommendation #6 ("monitor Claude Code plugin/MCP evolution") has no trigger criteria -- what specific condition would prompt action? No SLA or review cadence defined | 3 | 7 | 5 | 105 | Major | Add: "Review on every Claude Code major release; action required if tool naming scheme changes or Issue #20983 is reopened" | Actionability |
| FM-018-20260226T1200 | E-16 Methodology | 5W1H framework is claimed as a structuring method but the Findings section labeled "5W1H" maps poorly -- "WHY" captures only historical causes, not the technical "why does this architecture work this way" | 3 | 4 | 6 | 72 | Minor | Note in methodology that "WHY" is limited to historical causation, and direct readers to L2 for architectural rationale | Completeness |
| FM-019-20260226T1200 | E-13 L2.5 TOOL_REGISTRY Impact | States "every reference would need to change" for plugin-only adoption but does not quantify the blast radius accurately: it says "7 agent definitions" but does not list which 7 | 4 | 5 | 5 | 100 | Major | List the specific 7 agent files that reference `mcp__context7__` tool names to make the impact concrete and actionable | Traceability |
| FM-020-20260226T1200 | E-04 L1.3 Tool Name Resolution | The tool name resolution table is accurate but does not document what happens when BOTH methods are configured simultaneously -- the table has two rows but no "Both" row | 5 | 6 | 5 | 150 | Major | Add a third row to the resolution table: "Both Plugin + Manual" with the observed precedence behavior | Completeness |
| FM-021-20260226T1200 | E-08 L1.7 Context7 Actual Tools | States Context7 exposes "exactly two tools" with "consistent" names regardless of install method -- but does not address whether both tools are available in all scopes (user, project, plugin) | 4 | 4 | 5 | 80 | Major | Confirm that both `resolve-library-id` and `query-docs` are available under all configuration methods and scopes | Completeness |
| FM-022-20260226T1200 | E-18 References | GitHub Issues are cited with "Key insight" annotations that are editorial interpretations, not direct quotes -- "Key insight: Subagents hallucinate MCP results" is a strong claim not present verbatim in Issue #13898 | 5 | 6 | 4 | 120 | Major | Either quote directly from the issue or qualify "Key insight" annotations as editorial interpretation rather than direct citations | Evidence Quality |
| FM-023-20260226T1200 | E-05 L1.4 Permission System | The conclusion that "both syntaxes now work" is drawn from a discrepancy between Issue #3107 (closed July 2025) and current documentation -- but no date on the documentation page is provided; it may pre-date the issue resolution | 6 | 5 | 6 | 180 | Major | Add a "documentation last verified" date and note that the wildcard support may have been added post-July 2025 | Evidence Quality |
| FM-024-20260226T1200 | E-10 L2.2 Subagent MCP Access Gap | Mitigation "configure Context7 at user scope" is recommended without confirming that Context7's SSE endpoint is reachable from the user-scoped context (network/auth constraints may differ) | 5 | 4 | 6 | 120 | Major | Note that user-scoped SSE MCP servers require network access to `mcp.context7.com` and that this may be blocked in restricted environments | Completeness |
| FM-025-20260226T1200 | E-12 L2.4 Recommended Architecture | The "Recommended?" column marks plugin-only as "No" and manual-only as "Yes" but the rationale section does not address the "subagent access issues" listed as a Con for plugin-only -- if user-scope resolves the subagent issue for manual-only, the comparison is incomplete because the Con is not equivalently resolved for plugin-only | 6 | 5 | 6 | 180 | Major | Explicitly address whether the "subagent access issues" Con for plugin-only can also be mitigated (e.g., by plugin + user-scope manual hybrid) before declaring manual-only as the recommended approach | Methodological Rigor |
| FM-026-20260226T1200 | E-09 L2.1 Dual-Registration Anti-Pattern | "Permission sprawl" is listed as a consequence but the 6-entry permission count is compared to "what should be 2 tools" -- this conflates tool count with permission entry count; the 2-tool count is correct but "2 permission entries" would still require one per tool unless server-level matching is used | 3 | 4 | 5 | 60 | Minor | Correct the comparison: with server-level matching, ONE permission entry covers both tools; the comparison should be "6 entries vs 1 entry (server-level matching)" | Internal Consistency |
| FM-027-20260226T1200 | E-14 L2.6 Governance File Impact | `settings.local.json` fix says "Remove `mcp__plugin_*` entries" but the actual entries use the full `mcp__plugin_context7_context7__*` pattern, not a bare `mcp__plugin_*` pattern -- the fix instruction is imprecise | 4 | 5 | 4 | 80 | Major | Specify the exact string to remove from `settings.local.json`: the three entries `"mcp__plugin_context7_context7__*"`, `"mcp__plugin_context7_context7__resolve-library-id"`, `"mcp__plugin_context7_context7__query-docs"` | Actionability |
| FM-028-20260226T1200 | E-15 Research Questions | RQ-3 answer has HIGH confidence for plugin naming pattern but the source cited (Issues #20983, #15145) are GitHub issues, not official documentation -- the naming pattern is inferred from issue reports, not formally documented by Anthropic | 5 | 5 | 5 | 125 | Major | Downgrade RQ-3 confidence to MEDIUM or find official documentation that specifies the `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` naming pattern | Evidence Quality |
| FM-029-20260226T1200 | E-01 L0 Executive Summary | The summary correctly identifies the `settings.local.json` hedge but does not mention the agent definition issue -- readers stopping at L0 may think the problem is only in permissions, not also in agent definitions | 5 | 5 | 6 | 150 | Major | Add to L0: "Additionally, all 7 agent definitions reference the short-form tool names, which will fail if the plugin namespace wins at runtime" | Completeness |
| FM-030-20260226T1200 | E-17 Recommendations | Short-term recommendation #5 ("document naming convention in mcp-tool-standards.md") lacks an acceptance criterion -- what specific content must be added to consider this complete? | 3 | 6 | 5 | 90 | Major | Add acceptance criterion: "mcp-tool-standards.md includes a section with a table comparing plugin vs manual server naming and explicitly states Jerry's configuration decision" | Actionability |
| FM-031-20260226T1200 | E-06 L1.5 Agent Definition mcpServers | The finding that "if tools field is omitted, all MCP tools inherited" creates a security implication: subagents without explicit `tools` lists inherit ALL MCP tools, including potentially dangerous ones -- this risk is not flagged | 6 | 5 | 8 | 240 | Critical | Flag the tool inheritance implication as a security risk: subagents without explicit tool lists inherit all MCP tools; recommend auditing agent definitions without explicit `tools` fields | Methodological Rigor |
| FM-032-20260226T1200 | E-11 L2.3 Tool Name Length Risk | The risk is dismissed as "safe for Context7" (49, 42 chars) without assessing the risk for other plugins Jerry might add -- the report identifies this as a risk "for other plugins" but does not list what those might be or how Jerry should monitor for it | 3 | 4 | 6 | 72 | Minor | Add a brief note that Jerry's governance process for adopting new plugins should include a tool name character count check | Actionability |

---

## Finding Details (Critical and Major)

### FM-001-20260226T1200: Recommendation Ignores Worktree Isolation Compatibility

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-12: L2.4 Recommended Architecture |
| **Strategy Step** | Step 2 (Missing lens) |
| **RPN** | 504 (S=9, O=7, D=8) |

**Evidence:**
The report states: "Remove the `enabledPlugins` Context7 entry and configure Context7 as a user-scoped manual MCP server." The repository uses worktree isolation (`isolation: worktree` in agent definitions, `.claude/worktrees/` directory noted in `.gitignore`). User-scoped MCP server configuration lives in `~/.claude.json` and is machine-global; it is not worktree-specific.

**Analysis:**
The recommendation assumes user-scoped MCP configuration is compatible with Jerry's worktree architecture. However, user-scoped configuration is global to the user's machine, not scoped to individual worktrees. This creates a risk: if different worktrees require different MCP configurations, the user-scoped approach cannot support per-worktree isolation. The report does not assess whether the worktree isolation model conflicts with user-scoped MCP. The severity is 9 because an incompatible recommendation could lead implementers to break worktree isolation while believing they have resolved the Context7 issue.

**Recommendation:**
Add a validation step before recommendation #1: "Confirm that user-scoped MCP server configuration is compatible with the worktree isolation model used by this repository. Check `.claude/worktrees/` configuration and verify that worktree-isolated sessions can access user-scoped MCP servers."

**Post-Correction RPN Estimate:** 504 -> 126 (S=9, O=3, D=7) -- Severity unchanged; occurrence reduced by adding the validation step.

---

### FM-003-20260226T1200: No Rollback Plan for Recommended Fix

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-17: Recommendations |
| **Strategy Step** | Step 2 (Missing lens) |
| **RPN** | 336 (S=8, O=6, D=7) |

**Evidence:**
Recommendation #1 states: "Remove `enabledPlugins.context7@claude-plugins-official` from `settings.json` and ensure Context7 is configured as a user-scoped manual MCP server." No rollback procedure is provided if this fix does not work.

**Analysis:**
The fix involves removing a currently-functioning (if imperfect) configuration element. If the user-scoped manual MCP server approach does not resolve subagent access (e.g., due to network constraints, version incompatibilities, or unreported Claude Code bugs), the implementer would have removed the plugin with no path back. Given that the report acknowledges runtime behavior could not be verified empirically, the risk that the recommended fix fails is non-negligible.

**Recommendation:**
Add a rollback procedure: "Before removing the plugin registration, verify that the user-scoped manual MCP server is working (`jerry mcp list` or `/mcp` command confirms `context7` is active with short-form names). If verification fails, restore the plugin entry and escalate to a plugin-only approach with updated agent definitions."

**Post-Correction RPN Estimate:** 336 -> 96 (S=8, O=2, D=6) -- Severity unchanged; occurrence and detection improved by adding verification gate.

---

### FM-004-20260226T1200: Confidence Rating Inconsistent with Unverified Empirical Claims

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-16: Methodology |
| **Strategy Step** | Step 2 (Incorrect lens) |
| **RPN** | 245 (S=7, O=7, D=5) |

**Evidence:**
Methodology states: "Confidence: HIGH (0.88)" in the report header. The Limitations section states: "Could not verify runtime behavior empirically -- findings are based on documentation and issue reports, not live testing of which tool names appear at runtime." The Research Questions table uniformly rates all five answers as HIGH confidence.

**Analysis:**
The HIGH confidence rating conflicts with the explicit limitation that runtime behavior was not verified. The claims most critical to the recommendations -- specifically, which namespace "wins" at runtime when both plugin and manual server are registered, and whether user-scoped MCP servers are accessible to subagents -- are precisely the claims that require empirical verification. The report acknowledges this gap but does not reduce confidence accordingly.

**Recommendation:**
Downgrade the overall confidence to MEDIUM (0.65-0.75) with annotation: "Runtime behavior not empirically verified; recommendations are based on documentation and issue analysis." For RQ-4 specifically, note that the answer is inferred from Issue #13898, not confirmed by testing.

**Post-Correction RPN Estimate:** 245 -> 105 (S=7, O=3, D=5) -- Occurrence reduced by accurate confidence signaling.

---

### FM-005-20260226T1200: Subagent MCP Access Mitigation Has No Verification Procedure

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-10: L2.2 Subagent MCP Access Gap |
| **Strategy Step** | Step 2 (Missing -- actionability gap) |
| **RPN** | 336 (S=8, O=6, D=7) |

**Evidence:**
Section L2.2 states: "Mitigation: Configure Context7 at user scope (`--scope user`) rather than project scope." No verification procedure follows.

**Analysis:**
The mitigation is a configuration change whose success cannot be confirmed without a test procedure. An implementer following this recommendation cannot determine whether subagents now have Context7 access without a concrete verification step. Given that the root cause involves runtime behavior that was explicitly stated as unverifiable through documentation alone, the absence of a verification procedure makes this recommendation incomplete. The severity is 8 because a failed mitigation with no verification step could go undetected, resulting in agents continuing to hallucinate while the developer believes the issue is resolved.

**Recommendation:**
Add a verification procedure: "After configuring user-scoped Context7, verify subagent access by: (1) running `claude mcp list` and confirming `context7` appears under user scope, (2) invoking a test agent that calls `mcp__context7__resolve-library-id` with a known library name and confirming a non-hallucinated response, (3) checking agent logs for fallback-to-WebSearch events."

**Post-Correction RPN Estimate:** 336 -> 96 (S=8, O=2, D=6) -- Occurrence and detection improved.

---

### FM-007-20260226T1200: Recommended Fix Omits Global Scope Risk of User-Scoped MCP

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-12: L2.4 Recommended Architecture |
| **Strategy Step** | Step 2 (Missing lens) |
| **RPN** | 392 (S=7, O=7, D=8) |

**Evidence:**
The option table marks manual-server-only as recommended with Cons listed as: "Manual updates, no marketplace benefits." The user-scoped MCP server (`--scope user`) stores configuration in `~/.claude.json`, which is machine-global and applies to all Claude Code projects on the user's machine.

**Analysis:**
User-scoped MCP configuration is not project-local. An implementer following recommendation #1 would be configuring Context7 for their entire development environment, not just for the Jerry project. This could affect other Claude Code projects that may have their own Context7 configuration or may not want Context7 at all. This is a significant architectural implication that the recommendation omits entirely from the Cons column.

**Recommendation:**
Add to the "Manual MCP server only (user scope)" Cons: "User-scope configuration is machine-global -- affects all Claude Code projects for this user, not just Jerry. Coordinate with other Claude Code users on shared machines."

**Post-Correction RPN Estimate:** 392 -> 126 (S=7, O=3, D=6) -- Occurrence and detection improved by making the scope implication explicit.

---

### FM-008-20260226T1200: Plugin Removal Recommendation Lacks Dependency Check

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-14: L2.6 Governance File Impact Assessment |
| **Strategy Step** | Step 2 (Missing lens) |
| **RPN** | 210 (S=6, O=5, D=7) |

**Evidence:**
The governance table states for `settings.json`: "Fix Needed: Remove plugin entry." No dependency check or impact analysis precedes this recommendation.

**Analysis:**
The Context7 plugin may provide functionality beyond MCP tool access -- for example, it may register plugin-level skills, participate in the plugin permissions system, or provide offline caching. The report does not investigate whether removing the plugin entry has any effects beyond the MCP namespace conflict. The report also does not confirm whether other Jerry components explicitly depend on the plugin form of Context7.

**Recommendation:**
Add a prerequisite to governance table fix: "Before removing plugin entry, audit `settings.json` and agent definitions for any reference to `plugin_context7_context7` or `context7@claude-plugins-official` that would indicate plugin-specific dependency. Confirm the `enabledPlugins` entry provides no functionality beyond the MCP server."

**Post-Correction RPN Estimate:** 210 -> 60 (S=6, O=2, D=5) -- Occurrence and detection improved.

---

### FM-011-20260226T1200: Project-Scope Inaccessibility Claim Relies on Single Issue Source

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-06: L1.5 Agent Definition mcpServers Field |
| **Strategy Step** | Step 2 (Insufficient evidence lens) |
| **RPN** | 252 (S=7, O=6, D=6) |

**Evidence:**
Section L1.5 states: "Critical issue from GitHub #13898: Custom subagents CANNOT access project-scoped MCP servers (from `.mcp.json`). They can only access user-scoped MCP servers (from `~/.claude.json` via `--scope user`)." The reference is a single GitHub issue with no Anthropic official confirmation visible in the citation.

**Analysis:**
Issue #13898 is the sole source for one of the most critical findings in the report -- that subagents cannot access project-scoped MCP servers. This claim shapes the recommendation to switch to user-scope configuration. If the issue describes a bug that has since been fixed, or if the behavior applies only to specific versions, the recommendation may be based on an outdated constraint. The report does not indicate whether Issue #13898 is open or closed, or whether Anthropic confirmed the behavior as designed.

**Recommendation:**
Add: "Issue #13898 status: [open/closed/as-designed]. Cross-reference this behavior against the official Claude Code subagent documentation at `https://code.claude.com/docs/en/sub-agents` to confirm it is not a fixed bug. If the issue is closed as 'fixed,' the user-scope recommendation may be unnecessary."

**Post-Correction RPN Estimate:** 252 -> 84 (S=7, O=2, D=6) -- Occurrence reduced by adding official documentation cross-reference.

---

### FM-015-20260226T1200: Runtime Precedence Rule Undocumented

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-09: L2.1 Dual-Registration Anti-Pattern |
| **Strategy Step** | Step 2 (Missing lens) |
| **RPN** | 252 (S=6, O=6, D=7) |

**Evidence:**
Section L2.1 states: "Namespace ambiguity: Depending on which registration 'wins' at runtime, tools may appear under either prefix." The mechanism determining the winner is not documented.

**Analysis:**
The report identifies the problem (namespace ambiguity) but does not explain the resolution mechanism. An implementer needs to understand the precedence rule to predict runtime behavior and to assess whether the current dual-registration arrangement is deterministically producing one namespace or randomly alternating. Without this knowledge, the report cannot confirm whether the current workaround is consistently functional or intermittently failing.

**Recommendation:**
Add a sub-section or note: "Investigate and document the runtime precedence rule when both Plugin and Manual MCP server configurations register the same logical service. Sources to check: Claude Code MCP documentation, Issue #15145 (which addresses namespace collision), and empirical testing via `/mcp` command output in a session with both configurations active."

**Post-Correction RPN Estimate:** 252 -> 84 (S=6, O=2, D=7) -- Occurrence reduced; detection unchanged (still requires investigation).

---

### FM-031-20260226T1200: Tool Inheritance Security Risk Not Flagged

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Element** | E-06: L1.5 Agent Definition mcpServers Field |
| **Strategy Step** | Step 2 (Missing lens) |
| **RPN** | 240 (S=6, O=5, D=8) |

**Evidence:**
Section L1.5 states in the tool inheritance table: "tools field omitted: Subagent inherits ALL tools from main thread, including MCP tools." The report does not note the security implication of this behavior.

**Analysis:**
If a subagent's agent definition omits the `tools` field, it inherits all MCP tools available in the main thread, which could include tools with elevated capabilities (file system access, memory-keeper write access, external network access). This is a security risk that transcends the Context7 naming issue: any agent definition without an explicit `tools` list is potentially over-permissioned. The report documents this behavior but does not flag it as a finding or connect it to the governance implications in L2.6.

**Recommendation:**
Add to L2.1 or L2.6: "Security implication: Agent definitions that omit the `tools` field inherit ALL MCP tools. Audit the 7 agent files referenced in L2.5 to confirm each has an explicit `tools` list. Agents without explicit tool lists should be treated as over-permissioned until audited."

**Post-Correction RPN Estimate:** 240 -> 72 (S=6, O=2, D=6) -- Occurrence and detection improved.

---

### FM-002-20260226T1200: Permission Syntax Contradiction Left Unresolved

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Element** | E-05: L1.4 Permission System Analysis |
| **Strategy Step** | Step 2 (Inconsistent lens) |
| **RPN** | 189 (S=7, O=9, D=3) |

**Evidence:**
Section L1.4 presents: "Key finding: MCP permissions do NOT support wildcard patterns in the traditional sense." Then immediately states: "However, the official resolution from Anthropic (Issue #3107, closed July 2025) states: 'The correct syntax here is `mcp__atlassian`. Permission rules do not support wildcards.'" Then: "This indicates that both syntaxes now work." The report concludes both syntaxes work without resolving which is authoritative.

**Analysis:**
The contradiction is acknowledged ("This indicates that both syntaxes now work") but not definitively resolved. For a governance document that shapes `settings.local.json` content, leaving this ambiguous means implementers cannot determine the correct syntax to use. The detection score is 3 (low) because the contradiction is explicitly visible in the text -- it does not require FMEA to surface it -- but it was not corrected.

**Recommendation:**
Add a definitive statement: "Jerry SHOULD use the server-level syntax `mcp__context7` (without `__*`) as it is confirmed by official resolution. The `mcp__context7__*` wildcard syntax is documented but may be a later addition. Either works as of the documentation date, but prefer the shorter server-level form for forward compatibility."

**Post-Correction RPN Estimate:** 189 -> 49 (S=7, O=1, D=7) -- Occurrence reduced dramatically; detection unchanged (still visible in text).

---

## Recommendations (Prioritized by Severity)

### Critical Findings (RPN >= 200) -- Mandatory Corrective Actions

| ID | Finding | Corrective Action | Acceptance Criteria | Current RPN | Estimated Post-Correction RPN |
|----|---------|-------------------|---------------------|-------------|-------------------------------|
| FM-001-20260226T1200 | Recommendation ignores worktree isolation compatibility | Add validation step confirming user-scoped MCP is compatible with worktree isolation | Section added confirming or denying worktree compatibility with evidence | 504 | 126 |
| FM-007-20260226T1200 | Recommended fix omits global scope risk of user-scoped MCP | Add "machine-global scope" to Cons column of recommended option | Cons column updated; reader informed of cross-project impact | 392 | 126 |
| FM-003-20260226T1200 | No rollback plan for recommended fix | Add rollback procedure with verification gate before removing plugin entry | Rollback section added with at least one verification command | 336 | 96 |
| FM-005-20260226T1200 | Subagent MCP mitigation has no verification procedure | Add step-by-step verification procedure for subagent Context7 access | Verification procedure with at least 3 concrete steps added | 336 | 96 |
| FM-004-20260226T1200 | HIGH confidence inconsistent with unverified claims | Downgrade overall confidence to MEDIUM; annotate RQ answers | Report confidence header updated; RQ-4 confidence downgraded | 245 | 105 |
| FM-031-20260226T1200 | Tool inheritance security risk not flagged | Add security implication note to L2.1 or L2.6 | Security note added; audit of agent definitions without explicit tools field recommended | 240 | 72 |
| FM-015-20260226T1200 | Runtime precedence rule undocumented | Add sub-section documenting how namespace winner is determined | Investigation plan or documented precedence rule added | 252 | 84 |
| FM-011-20260226T1200 | Project-scope inaccessibility claim relies on single issue | Cross-reference against official subagent docs; add issue status | Issue #13898 status noted; official doc reference added | 252 | 84 |
| FM-008-20260226T1200 | Plugin removal lacks dependency check | Add prerequisite: audit for plugin-specific dependencies before removal | Dependency check step added to governance table | 210 | 60 |

### Major Findings (RPN 80-199) -- Recommended Corrective Actions

| ID | Finding | Corrective Action | Current RPN | Estimated Post-Correction RPN |
|----|---------|-------------------|-------------|-------------------------------|
| FM-006-20260226T1200 | Plugin server-name origin uncited | Cite source confirming internal server name is `context7` | 180 | 60 |
| FM-016-20260226T1200 | Namespace non-transitivity argument is circular | Add non-circular evidence (Issue #20983 or official docs) | 180 | 60 |
| FM-025-20260226T1200 | Plugin-only "subagent access" Con not equivalently analyzed | Explicitly address whether plugin-only subagent issue is also resolvable | 180 | 72 |
| FM-023-20260226T1200 | Documentation date missing for wildcard syntax evolution | Add docs verification date; note possible post-July-2025 addition | 180 | 72 |
| FM-002-20260226T1200 | Permission syntax contradiction unresolved | Add definitive Jerry recommendation for permission syntax | 189 | 49 |
| FM-009-20260226T1200 | Preflight check recommendation lacks owner and implementation path | Specify toolchain and owner (jerry CLI command or shell script) | 160 | 48 |
| FM-022-20260226T1200 | GitHub Issue "Key insight" annotations are editorial, not direct quotes | Qualify annotations as editorial or quote directly | 120 | 48 |
| FM-024-20260226T1200 | User-scoped SSE endpoint reachability not confirmed | Add network/auth note for restricted environments | 120 | 40 |
| FM-028-20260226T1200 | Plugin naming pattern confidence HIGH but source is only GitHub issues | Downgrade RQ-3 confidence to MEDIUM or find official doc | 125 | 50 |
| FM-014-20260226T1200 | 64-character limit source uncited | Cite source of 64-char limit (Issue #20983 or official API docs) | 100 | 40 |
| FM-021-20260226T1200 | Context7 tool availability across scopes not confirmed | Confirm both tools available under all configuration methods | 100 | 40 |
| FM-019-20260226T1200 | "7 agent definitions" not enumerated | List specific agent files by name | 100 | 30 |
| FM-020-20260226T1200 | Tool resolution table missing "Both configured" row | Add third row documenting simultaneous plugin+manual behavior | 150 | 60 |
| FM-012-20260226T1200 | RQ-4 conflates two scenarios | Rewrite RQ-4 separately for Jerry's specific configuration | 150 | 50 |
| FM-010-20260226T1200 | Current workaround functional status not assessed | Add section confirming or refuting whether dual-permission workaround currently works | 150 | 50 |
| FM-029-20260226T1200 | L0 omits agent definition issue | Add agent definition impact to Executive Summary | 150 | 50 |
| FM-027-20260226T1200 | `settings.local.json` fix uses imprecise string reference | Specify exact strings to remove from `settings.local.json` | 80 | 24 |
| FM-017-20260226T1200 | Long-term recommendation lacks trigger criteria | Add release-based review trigger | 105 | 35 |
| FM-030-20260226T1200 | Recommendation #5 lacks acceptance criterion | Add acceptance criterion for `mcp-tool-standards.md` update | 90 | 30 |

### Minor Findings (RPN < 80) -- Improvement Opportunities

| ID | Finding | Corrective Action | Current RPN | Estimated Post-Correction RPN |
|----|---------|-------------------|-------------|-------------------------------|
| FM-013-20260226T1200 | Badge analogy imprecise | Add note that registrations may differ in version/state | 75 | 25 |
| FM-026-20260226T1200 | Permission count comparison imprecise | Correct "2 tools" vs "1 permission entry" distinction | 60 | 20 |
| FM-018-20260226T1200 | 5W1H WHY scope limited to historical causation | Note limitation in methodology section | 72 | 24 |
| FM-032-20260226T1200 | Tool name length risk monitoring not specified | Add plugin adoption checklist note | 72 | 24 |

---

## Scoring Impact

| Dimension | Weight | Impact | FM-NNN References | Rationale |
|-----------|--------|--------|-------------------|-----------|
| **Completeness** | 0.20 | Negative | FM-001, FM-003, FM-007, FM-008, FM-015, FM-020, FM-021, FM-024, FM-029, FM-031 | 10 failure modes involving missing content, including critical gaps: no worktree compatibility check, no rollback plan, undocumented runtime precedence, omitted global scope risk of user-scoped MCP, and security implication of tool inheritance |
| **Internal Consistency** | 0.20 | Negative | FM-002, FM-010, FM-012, FM-013, FM-026 | Permission syntax contradiction (FM-002) is the most damaging: the report simultaneously says wildcards are not supported and that they now work, without resolving which to use |
| **Methodological Rigor** | 0.20 | Negative | FM-004, FM-025, FM-031 | Confidence ratings are not calibrated to the acknowledged limitation of unverified runtime behavior; option comparison table is asymmetric (Cons not equivalently evaluated for both options); security implications of tool inheritance behavior not addressed as a finding |
| **Evidence Quality** | 0.15 | Negative | FM-006, FM-011, FM-014, FM-016, FM-022, FM-023, FM-028 | Seven failure modes related to evidence quality: circular reasoning for namespace non-transitivity, single-source for critical subagent claim, uncited 64-char limit, editorial annotations presented as citations |
| **Actionability** | 0.15 | Negative | FM-003, FM-005, FM-009, FM-017, FM-027, FM-030 | Six failure modes in recommendations: absent rollback plans, no verification procedures, imprecise fix strings, vague implementation paths, missing trigger criteria |
| **Traceability** | 0.10 | Mostly Neutral | FM-019 | Research questions map well to findings; findings trace to sections; only FM-019 (unnamed "7 agent files") weakens traceability |

**Overall FMEA Assessment: REVISE BEFORE ACCEPTANCE**

The deliverable correctly identifies the root cause (dual-namespace conflict from dual registration) and the general direction of the fix (choose one registration method). However, it requires targeted revisions in all six quality dimensions before it can serve as a reliable remediation guide. Priority order for revision: Completeness (address FM-001 and FM-007 first -- they affect the core recommendation), then Actionability (add verification procedures FM-005 and rollback FM-003), then Evidence Quality (resolve confidence calibration FM-004 and circular reasoning FM-016).

---

## Execution Statistics

- **Total Findings:** 32
- **Critical:** 9 (FM-001, FM-003, FM-004, FM-005, FM-007, FM-008, FM-011, FM-015, FM-031)
- **Major:** 19 (FM-002, FM-006, FM-009, FM-010, FM-012, FM-014, FM-016, FM-017, FM-019, FM-020, FM-021, FM-022, FM-023, FM-024, FM-025, FM-027, FM-028, FM-029, FM-030)
- **Minor:** 4 (FM-013, FM-018, FM-026, FM-032)
- **Total RPN:** 5,334
- **Estimated Post-Correction Total RPN:** 1,582 (70% RPN reduction)
- **Protocol Steps Completed:** 5 of 5
- **Elements Analyzed:** 18
- **Most Failure-Prone Element:** E-12 (L2.4 Recommended Architecture) and E-17 (Recommendations) -- combined 9 failure modes and 2,137 RPN points

---

## Self-Review (H-15)

Per H-15, before persisting this report:

1. **All findings have specific evidence:** Each FM-NNN references a specific section, quote, or assertion from the deliverable. No vague findings.
2. **Severity classifications justified:** Critical findings all involve gaps that could lead implementers to take actions that fail or cause harm (broken worktree config, failed fix with no rollback, undetected subagent failure). Major findings involve significant gaps that weaken reliability of recommendations. Minor findings are genuine improvement opportunities only.
3. **Finding identifiers follow FM-NNN-20260226T1200 format:** Verified across all 32 findings.
4. **Summary table matches detailed findings:** All 32 findings in the table appear in either the detailed section or the recommendations table. Critical findings all have expanded detail blocks.
5. **No findings omitted or minimized:** The permission syntax contradiction (FM-002) in particular was scrutinized -- it is visible in the text but was not corrected, making it a legitimate finding despite being self-acknowledged in the deliverable.

Report is internally consistent and ready for persistence.
