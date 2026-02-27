# Strategy Execution Report: Pre-Mortem Analysis (S-004)

## Execution Context

- **Strategy:** S-004 (Pre-Mortem Analysis)
- **Template:** `.context/templates/adversarial/s-004-pre-mortem-analysis.md` (not present in this worktree; execution guided by canonical S-004 protocol from prior validated reports)
- **Deliverable:** `projects/PROJ-030-bugs/research/context7-plugin-architecture.md`
- **Executed:** 2026-02-26T00:00:00Z
- **Criticality:** C4
- **Quality Threshold:** >= 0.95
- **Finding Prefix:** PM

---

## Failure Scenario Declaration

### Temporal Perspective Shift

It is **August 2026**, six months after this research was produced on 2026-02-26. We are conducting a post-mortem on why the Context7 plugin architecture research report failed to produce the intended outcome: a stable, correctly configured MCP tool integration in the Jerry Framework.

**What failure looks like concretely:**

1. Jerry agents (particularly `ps-researcher`, `ps-architect`) continue to silently fall back to WebSearch or hallucinate library documentation because Context7 is still unreachable under the tool names they expect.
2. The research report identified BUG-002 as a candidate but no remediation was ever shipped -- the dual-registration configuration persists in `settings.json` and `settings.local.json`.
3. A new contributor follows the report's "Recommended approach" (`claude mcp add --transport sse --scope user context7 https://mcp.context7.com/sse`), removes the `enabledPlugins` entry, and finds Context7 is now completely unreachable -- because the URL cited in the report cannot be verified to be the correct, current SSE endpoint.
4. The `mcp-tool-standards.md` document was never updated with the plugin-vs-manual-server naming distinction documented in this research. A developer writing a new agent definition cannot find the guidance they need and repeats the same mistake.
5. The TOOL_REGISTRY.yaml governance file was not updated to reflect the resolution; it still implies the `mcp__context7__` short prefix is stable and correct without explaining why.
6. Subagent MCP access (GitHub Issue #13898 finding) was never operationally verified -- Jerry's CI and pre-flight checks do not catch silent tool-unavailability failures, so the problem may still exist undetected.

We now work backward from this failure state to identify what in the research report created the conditions for this outcome.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| PM-001 | Critical | No empirical verification of runtime tool name behavior -- research is entirely documentation-based with unverified claims | Limitations / L1 Technical Analysis |
| PM-002 | Critical | Recommended fix (`claude mcp add --transport sse`) cites an unverified SSE endpoint URL that may be incorrect or deprecated | Recommendations (Immediate #1) |
| PM-003 | Critical | Subagent access gap (GitHub #13898) is documented as an architectural implication but no verification step or actionable test exists | L2 Architectural Implications §2 |
| PM-004 | Major | Failure mode is irreversible without the fix: the deliverable surfaces the risk but provides no rollback or contingency if the recommended configuration fails | Recommendations §1 |
| PM-005 | Major | The claim that wildcard `mcp__context7__*` syntax is documented as "equivalent" relies on documentation that may change -- no version pin or snapshot | L1 Technical Analysis §4 |
| PM-006 | Major | Impact assessment on TOOL_REGISTRY.yaml states "no change needed" without specifying how the registry should document the chosen resolution | L2 Governance File Impact §6 |
| PM-007 | Major | The Limitations section acknowledges Context7 MCP quota was exceeded during research -- the tool under investigation was itself unavailable during investigation | Methodology / Limitations |
| PM-008 | Major | GitHub Issue #2928 cited in the session prompt does not exist per the report -- the actual relevant issues are #3107, #15145, #20983, #13898, but cross-linkage between this report and BUG-001 root cause documentation is incomplete | Research Questions / References |
| PM-009 | Minor | The confidence level is stated as HIGH (0.88) but the research did not empirically verify the core claim (dual-registration produces separate namespaces) -- 0.88 confidence overstates the evidence base | Frontmatter |
| PM-010 | Minor | No guidance on how to verify success after applying the recommended fix -- no acceptance criterion or test command provided | Recommendations |
| PM-011 | Minor | The "Short-Term" recommendation to add a pre-flight check is described but not assigned to any specific work item, owner, or timeline | Recommendations (Short-Term #4) |

---

## Detailed Findings

### PM-001: No Empirical Verification -- Research Is Entirely Documentation-Based

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Methodology / Limitations; L1 Technical Analysis throughout |
| **Strategy Step** | Technical failure lens -- gap between documented behavior and runtime behavior |

**Evidence:**

From the Limitations section (lines 275-277):

> "1. **Could not verify runtime behavior empirically** -- findings are based on documentation and GitHub issues, not live testing of which tool names appear at runtime."

From the L1 Technical Analysis Section 3 (lines 100-102):

> "Based on Claude Code documentation and GitHub issues, the tool naming rules are..."

The foundational claim of the entire research -- that the dual-registration creates a namespace collision that silently prevents agent tool access -- is never empirically confirmed. The report asserts with HIGH confidence that `mcp__context7__*` and `mcp__plugin_context7_context7__*` are separate namespaces, but this is inferred from documentation and closed GitHub issues, not from observing the actual tool names presented to a Jerry agent at runtime.

**Analysis:**

This is the most severe failure vector. If the runtime behavior does NOT match the documented behavior (a common occurrence with Claude Code, which evolves rapidly), the entire recommended remediation may be based on a false diagnosis. A developer removing the `enabledPlugins` entry based on this research could introduce a regression where Context7 becomes unavailable entirely -- without a verification step to catch it.

The research explicitly notes it could not observe runtime behavior, then assigns HIGH confidence and makes specific actionable claims. This is a contradiction that will cause downstream execution failures.

**Recommendation:**

Before any remediation is shipped, a developer MUST verify runtime tool names by:
1. Running `jerry` with the current configuration and checking which tool name prefix appears in the active tool list (via Claude Code's `/mcp` command or tool invocation logs).
2. Documenting the observed runtime names in the bug report before making configuration changes.
3. After applying the fix, running the same check to confirm the names match agent definitions.

This verification step must be added as a prerequisite gate in BUG-002, not an optional post-fix.

---

### PM-002: Recommended SSE Endpoint URL Is Unverified

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | Recommendations (Immediate #1) |
| **Strategy Step** | Process failure lens -- execution of recommendations produces incorrect result |

**Evidence:**

From the Recommendations section (lines 215-219):

> ```bash
> claude mcp add --transport sse --scope user context7 https://mcp.context7.com/sse
> ```

> "This ensures:
> 1. Tool names match agent definitions (`mcp__context7__resolve-library-id`)
> 2. Subagents can access Context7 (user-scoped servers are inherited)"

The URL `https://mcp.context7.com/sse` is cited as the correct SSE endpoint, but:
- The References section (Reference #10) points to `github.com/upstash/context7` but does not confirm this SSE URL from that source.
- Reference #11 (`claude.com/plugins/context7`) is the plugin listing, not the SSE endpoint documentation.
- The research Limitations note that Context7 was unavailable via MCP during the research (quota exceeded), meaning the SSE endpoint was not tested.

From the Methodology Sources table (lines 260-265): The Context7 GitHub Repository is rated HIGH credibility and the Context7 Claude Plugin Page is rated MEDIUM -- but neither is cited as confirming the specific SSE URL.

**Analysis:**

The SSE endpoint URL appears in the recommended command without a citation. If the URL is wrong, deprecated, or requires authentication, a developer following this recommendation verbatim will register a non-functional MCP server. The failure mode is silent: `claude mcp add` may succeed syntactically even if the SSE endpoint is unreachable, and the agent will fall back to WebSearch without a clear error.

The `npx -y @upstash/context7-mcp` alternative (line 75) is cited in the research as another valid approach but is NOT included in the final recommendation. The NPX approach may be more reliable because it pins to the published NPM package rather than a URL.

**Recommendation:**

Update the recommendation to:
1. Cite the specific source confirming `https://mcp.context7.com/sse` as the current SSE endpoint.
2. Add the NPX alternative as the primary option (more reliable, ties to versioned package):
   ```bash
   claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp
   ```
3. Add a verification step: after running the command, run `/mcp` in Claude Code to confirm the server appears under the `context7` name.

---

### PM-003: Subagent Access Gap Has No Verification Step or Test

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L2 Architectural Implications §2 |
| **Strategy Step** | Assumption failure lens -- assumed mitigation may not hold at runtime |

**Evidence:**

From L2 Architectural Implications §2 (lines 189-195):

> "Critical issue from GitHub #13898: Custom subagents CANNOT access **project-scoped** MCP servers (from `.mcp.json`). They can only access **user-scoped** MCP servers (from `~/.claude.json` via `--scope user`). This means if Context7 is only configured at the project level, subagents (which Jerry uses heavily via the Task tool) may not be able to access it at all, and will hallucinate responses instead."

> "**Mitigation:** Configure Context7 at **user scope** (`--scope user`) rather than project scope."

The mitigation is stated as "configure at user scope" but:
- There is no test or verification procedure to confirm subagent tool inheritance works as documented.
- GitHub Issue #13898 is described as a bug report -- its status (open/closed/fixed) is not stated.
- Whether the `--scope user` approach actually resolves the subagent access gap in the current Claude Code version is undocumented.

**Analysis:**

This is the highest-impact failure vector for Jerry's actual operation. If subagents cannot access Context7 even after the recommended configuration change, the entire remediation effort produces no observable improvement. Agents would still silently fall back to WebSearch, and without a verification test, the team would not know whether the fix worked.

The issue is compounded by the research not verifying the status of GitHub #13898. If it has been resolved in a recent Claude Code version, or if the behavior changed, the mitigation may be unnecessary or already broken in a different way.

**Recommendation:**

1. Verify GitHub Issue #13898 status before shipping BUG-002 remediation.
2. Add a concrete verification test: invoke a Jerry agent (e.g., `ps-researcher`) via the Task tool and check whether it can call `mcp__context7__resolve-library-id`. If it cannot, the subagent access problem persists.
3. Document the test result in the bug fix commit.

---

### PM-004: No Rollback Plan If Recommended Configuration Fails

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Recommendations (Immediate) |
| **Strategy Step** | Process failure lens -- remediation produces worse state than current |

**Evidence:**

From Recommendations Immediate #1 (lines 336-338):

> "1. **Choose one registration method.** Remove `enabledPlugins.context7@claude-plugins-official` from `settings.json` and ensure Context7 is configured as a **user-scoped manual MCP server**."

The current "dual registration" state is described as a "defensive workaround" -- but it is also the state where BOTH namespaces have permissions, meaning Context7 is accessible under at least one namespace depending on runtime behavior. Removing the plugin registration without confirming the manual server works first could result in zero Context7 access rather than the current partial/uncertain access.

The report does not include:
- A step-by-step ordered procedure (verify -> configure -> verify again -> then remove old config)
- A rollback path if the manual configuration fails to expose tools correctly
- A note that the plugin registration should NOT be removed until the manual server is confirmed working

**Analysis:**

The current state (dual registration with permission sprawl) is functional enough that research agents have been running without a complete outage. The recommended fix could break what currently works. The irreversibility risk is moderate: removing a plugin registration is recoverable, but the confusion and debugging time incurred if the fix breaks tool access is a real cost.

**Recommendation:**

Add an ordered procedure:
1. First, add the user-scoped manual MCP server (`claude mcp add --scope user ...`)
2. Verify tool names are correct (`/mcp` command, confirm `context7` server shows tools with short prefix)
3. Verify a subagent can invoke the tools (Task tool invocation test)
4. Only after steps 2-3 pass: remove `enabledPlugins.context7@claude-plugins-official` from `settings.json`
5. Verify behavior is unchanged after removal

---

### PM-005: Wildcard Permission Syntax Documentation May Change Without Notice

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1 Technical Analysis §4 |
| **Strategy Step** | External dependency failure lens -- third-party changes invalidate documented behavior |

**Evidence:**

From L1 Technical Analysis §4 (lines 122-133):

> "However, the official resolution from Anthropic (Issue #3107, closed July 2025) states: 'The correct syntax here is `mcp__atlassian`. Permission rules do not support wildcards.'"

> "**But the documentation page on permissions (code.claude.com/docs/en/permissions) states:** [...] `mcp__puppeteer__*` wildcard syntax that also matches all tools from the `puppeteer` server"

> "This indicates that **both syntaxes now work** (the wildcard support was likely added after Issue #3107 was filed in July 2025)."

The inference that both syntaxes work is based on comparing a closed GitHub issue (July 2025) with an undated documentation page. The word "likely" signals this is an inference, not a confirmed fact. The documentation page version and date are not recorded.

**Analysis:**

If Anthropic reverts the wildcard behavior or changes the permission matching logic again, Jerry's `settings.local.json` configuration could break silently. The research's conclusion ("both syntaxes work") is a reasonable inference but is presented as a settled fact without timestamp or version pin on the documentation. Claude Code is a rapidly evolving product -- documentation can change between the research date (2026-02-26) and the fix date.

**Recommendation:**

1. Record the documentation version/date consulted (URL with any available version tag or `Last updated` timestamp).
2. Test the wildcard behavior empirically in the current Claude Code version before relying on the inference.
3. The Recommendations section should advise using the server-level syntax (`mcp__context7`) rather than the wildcard (`mcp__context7__*`) since the server-level syntax was confirmed correct in the official GitHub response (Issue #3107).

---

### PM-006: Governance File Impact Assessment Understates TOOL_REGISTRY.yaml Update Needed

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L2 Architectural Implications §6 |
| **Strategy Step** | Assumption failure lens -- "no change needed" may cause the fix to be incomplete |

**Evidence:**

From the Governance File Impact table (lines 233-239):

| File | Current State | Issue | Fix Needed |
|------|--------------|-------|:----------:|
| `TOOL_REGISTRY.yaml` | Uses `mcp__context7__` prefix | Correct for manual server config | No |
| `mcp-tool-standards.md` | Uses `mcp__context7__` prefix | Correct for manual server config | No |

Both files are assessed as requiring "No" change. However:
- `mcp-tool-standards.md` currently documents the canonical tool names but does not explain WHY the short prefix is correct (i.e., because Jerry uses manual MCP server configuration, not plugin). A new developer reading this document cannot understand the naming convention choice.
- `TOOL_REGISTRY.yaml` contains the tool names without context about the configuration decision.

**Analysis:**

If the BUG-002 fix is applied but these governance files are not updated to document the naming convention decision and its rationale, the same mistake will be made again by the next developer who encounters the plugin marketplace option. The "No change needed" assessment perpetuates the undocumented state that caused the original problem.

**Recommendation:**

Update both files with a "Configuration Decision" note:
- `mcp-tool-standards.md`: Add a section documenting that Jerry uses manual MCP server configuration (not plugin), explaining the naming convention difference, and noting that the `mcp__context7__` short prefix is the canonical form.
- `TOOL_REGISTRY.yaml`: Add a comment explaining the `mcp__context7__` prefix assumption and linking to the BUG-002 resolution ADR or work item.

---

### PM-007: Investigation Tool Was Unavailable During Investigation

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Methodology / Limitations |
| **Strategy Step** | Resource failure lens -- key diagnostic capability lost at the moment of investigation |

**Evidence:**

From the Limitations section (lines 276-277):

> "2. **Context7 MCP quota exceeded** during research -- could not use Context7 to look up Claude Code's own documentation via the MCP tool."

The research report is an investigation into whether Context7 is correctly configured and accessible. During the investigation, Context7 itself was unavailable -- the very symptom of the problem being investigated prevented proper investigation of the problem.

**Analysis:**

This is a methodological self-reference problem. The research could not use Context7 to investigate Context7's configuration issues. As a result:
- Documentation lookups for Claude Code were done via WebSearch or other means, which may be less authoritative than Context7's curated docs.
- The report cannot confirm whether the "quota exceeded" was a side effect of the broken configuration or an independent quota limit.
- The investigation's methodology section lists Context7 documentation as sources (via URLs) but these were accessed via web, not via the Context7 MCP tool -- the difference in data freshness and authority is unacknowledged.

**Recommendation:**

1. The bug report (BUG-002) should document that Context7 was inaccessible during the investigation itself, as this is direct evidence of the bug's impact.
2. A separate verification step should re-run the research lookups via Context7 after the fix is applied, to confirm the tool is functional for its intended research use cases.
3. The quota exceeded condition should be investigated: was it a rate limit (transient) or a configuration failure (symptomatic of the bug)?

---

### PM-008: GitHub Issue Cross-Reference Is Incomplete Between BUG-001 and BUG-002

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Research Questions / References |
| **Strategy Step** | Assumption failure lens -- incomplete traceability causes remediation to miss related issues |

**Evidence:**

From the Research Questions table (lines 245-251), Reference #4 is listed as RQ-4 with HIGH confidence. The report notes (lines 276-278):

> "3. **Issue #2928 not found** -- the originally requested issue number does not exist or has been renumbered. The relevant issues are #3107, #15145, and #20983."

The PS Integration section (lines 377-394) states:

> "- **Related Bug:** BUG-001 (memory-keeper tool names -- same class of issue)"

But the research does not:
- Cross-reference the Memory-Keeper BUG-001 root cause document to check if the same dual-registration pattern applies.
- Investigate whether Memory-Keeper has a similar `mcp__plugin_*` vs `mcp__memory-keeper__*` namespace conflict.
- Confirm that the fix for Context7 (BUG-002) would not need to be applied identically for Memory-Keeper.

**Analysis:**

The report identifies BUG-001 and BUG-002 as "the same class of issue" but does not perform the systematic analysis to confirm whether they require the same fix or whether fixing Context7 alone leaves Memory-Keeper in the same broken state. If Memory-Keeper has the same dual-registration problem, half the fix is missing.

**Recommendation:**

1. Read the BUG-001 root cause document and confirm whether Memory-Keeper has a plugin registration in `settings.json`.
2. If yes, the fix scope should include Memory-Keeper in the same change as Context7.
3. The research report should explicitly state whether BUG-002 scope covers Memory-Keeper or explicitly defers it to BUG-003.

---

### PM-009: Confidence Level Overstated Given Documentation-Only Evidence Base

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Frontmatter (Confidence: HIGH (0.88)) |
| **Strategy Step** | Assumption failure lens -- confidence calibration |

**Evidence:**

From the frontmatter (line 8):

> `> **Confidence:** HIGH (0.88)`

From the Limitations section (lines 274-277):

> "1. **Could not verify runtime behavior empirically** -- findings are based on documentation and GitHub issues, not live testing of which tool names appear at runtime.
> 2. **Context7 MCP quota exceeded** during research..."

HIGH (0.88) confidence is stated on findings that:
- Cannot be empirically verified
- Were investigated while the tool under investigation was unavailable
- Rely on inference from documentation whose version is untracked
- Include a GitHub issue number that does not exist

**Analysis:**

0.88 is an overstatement. A calibrated confidence for this research -- given the limitations -- is closer to MEDIUM (0.65-0.75). The directional conclusions (dual registration creates namespace issues, plugin prefix is different from manual prefix) are likely correct, but the specific operational claims (subagent access will work with `--scope user`, both wildcard syntaxes work, SSE URL is correct) are unverified.

**Recommendation:**

Revise confidence to MEDIUM (0.70) and add a note: "Confidence pending empirical verification of runtime tool names and subagent access behavior."

---

### PM-010: No Acceptance Criterion for Successful Remediation

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Recommendations |
| **Strategy Step** | Process failure lens -- cannot verify fix worked |

**Evidence:**

The Recommendations section (lines 333-354) lists 6 recommendations across Immediate, Short-Term, and Long-Term categories. None of them include:
- A definition of "done" for the fix
- A specific test command to confirm Context7 is accessible under the correct tool name
- A test to confirm subagent inheritance works

**Analysis:**

Without an acceptance criterion, the BUG-002 fix cannot be verified. A developer could apply the configuration change, see no immediate error, and consider the bug resolved -- while agents continue silently falling back to WebSearch because the tool name still does not match, or because the SSE endpoint was not reachable.

**Recommendation:**

Add an acceptance criterion section to the research report or to BUG-002:

```
Acceptance Criteria:
1. `claude mcp list` shows `context7` server under user scope with 2 tools
2. `/mcp` in Claude Code shows tools as `mcp__context7__resolve-library-id` and `mcp__context7__query-docs`
3. A ps-researcher Task invocation successfully calls resolve-library-id (not WebSearch fallback)
4. `settings.json` no longer has `enabledPlugins.context7@claude-plugins-official`
5. `settings.local.json` no longer lists `mcp__plugin_context7_context7__*` entries
```

---

### PM-011: Pre-Flight Check Recommendation Lacks Owner and Timeline

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Recommendations (Short-Term #4) |
| **Strategy Step** | Resource failure lens -- recommendation will be deferred indefinitely |

**Evidence:**

From Recommendations Short-Term #4 (lines 348-350):

> "4. **Add a pre-flight check.** Create a validation script that compares tool names in agent definitions against actual MCP server tool names at runtime (via `/mcp` command output)."

This recommendation has no:
- Work item reference (no story, enabler, or task ID)
- Owner
- Timeline or trigger ("after BUG-002 is fixed" or "before any new agent definition ships")
- Estimated effort

**Analysis:**

Short-term recommendations without assigned owners and timelines are frequently deferred indefinitely. This is particularly important here because the pre-flight check is the systemic prevention mechanism -- without it, the same class of bug can recur whenever a new MCP server is added or when Claude Code changes its naming convention.

**Recommendation:**

Create a separate work item (e.g., BUG-003 or a Story) for the pre-flight check. Reference it from this research report and from BUG-002.

---

## Execution Statistics

- **Total Findings:** 11
- **Critical:** 3
- **Major:** 5
- **Minor:** 3
- **Protocol Steps Completed:** 5 of 5

---

## Failure Category Distribution

| Category | Findings | IDs |
|----------|---------|-----|
| Technical | 2 | PM-001, PM-002 |
| Assumption | 3 | PM-003, PM-005, PM-009 |
| Process | 3 | PM-004, PM-010, PM-011 |
| External | 1 | PM-005 (shared with Assumption) |
| Resource | 2 | PM-007, PM-011 (shared with Process) |

---

## Pre-Mortem Recommendation

**REVISE before shipping BUG-002 remediation.**

The 3 Critical findings (PM-001, PM-002, PM-003) create conditions where the recommended fix could fail silently or produce a worse state than the current configuration. Specifically:

1. **PM-001** (no empirical verification) means the entire diagnosis may rest on incorrect assumptions about runtime behavior.
2. **PM-002** (unverified SSE URL) means the fix command may register a broken server.
3. **PM-003** (no subagent verification test) means the fix's primary benefit (restoring Context7 to subagents) cannot be confirmed.

Before BUG-002 remediation is shipped, a developer MUST:
1. Observe the actual runtime tool names (not just infer from documentation)
2. Verify the SSE endpoint URL or use the NPX alternative
3. Run a subagent verification test (Task tool -> Context7 tool call)
4. Apply the fix in staged order (add new config -> verify -> remove old config)
5. Confirm acceptance criteria are all met

The 5 Major findings represent gaps that will cause the fix to be incomplete or fragile even if the Critical items are addressed. The 3 Minor findings are calibration and traceability improvements that should be incorporated into BUG-002.
