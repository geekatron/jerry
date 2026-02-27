# Strategy Execution Report: Inversion Technique (S-013)

## Execution Context

- **Strategy:** S-013 (Inversion Technique)
- **Template:** `.context/templates/adversarial/s-013-inversion.md`
- **Deliverable:** `projects/PROJ-030-bugs/research/context7-plugin-architecture.md`
- **Executed:** 2026-02-26T00:00:00Z
- **Criticality:** C4
- **Quality Threshold:** >= 0.95
- **Goals Analyzed:** 6 | **Assumptions Mapped:** 14 | **Vulnerable Assumptions:** 10

---

## Summary

The deliverable is a well-structured research report diagnosing the Context7 dual-registration namespace conflict in Jerry. Inversion analysis identified six primary goals, inverted each to expose anti-goal conditions, and mapped 14 assumptions (5 explicit, 9 implicit). Ten assumptions failed stress-testing: two Critical and six Major findings emerged, primarily around the temporal currency of documentation-sourced claims and gaps in the fix recommendation's completeness for team-scale and multi-transport scenarios. The core architectural insight -- that dual-registration is an anti-pattern producing separate namespaces -- is sound and robust to inversion. However, the deliverable presents several mid-2025 GitHub issue findings as confirmed Feb 2026 runtime facts without an empirical verification step, and the wildcard permission claim contains an unresolved internal contradiction. Recommendation: **REVISE** -- address the two Critical and six Major findings before using this report to drive an ADR or implementation change.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| IN-001-20260226 | Critical | Plugin prefix naming currency unverified -- mid-2025 issue docs assumed current | L1.1, L1.3, Recommendations |
| IN-002-20260226 | Critical | "NOT PLANNED" closure of #15145 interpreted as bug-still-present without verification | L1.3, L2.1 |
| IN-003-20260226 | Major | No integration test assumed without full codebase audit | L2 WHY section |
| IN-004-20260226 | Major | "7 agent definitions" count unverified -- audit scope not stated | L2.5 |
| IN-005-20260226 | Major | Fix recommendation assumes single-developer scope; team/CI implications absent | L2.4, Recommendations |
| IN-006-20260226 | Major | Subagent MCP access gap stated unconditionally; omits tools-field-omitted inheritance behavior | L1.5, L2.2 |
| IN-007-20260226 | Major | SSE transport recommended exclusively; npx alternative not evaluated | Recommendations |
| IN-008-20260226 | Major | Wildcard permission syntax reconciliation is an inference, not a confirmed finding | L1.4 |
| IN-009-20260226 | Minor | Temporal limitation not prominently flagged in executive summary or recommendations | Limitations |
| IN-010-20260226 | Minor | Plugin removal side effects (non-MCP capabilities) not analyzed | Recommendations |

---

## Detailed Findings

### IN-001-20260226: Plugin Prefix Naming Currency Unverified [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Assumption |
| **Section** | L1.1 (Two Configuration Methods), L1.3 (Tool Name Resolution Rules), Recommendations |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
The deliverable states that plugin-installed Context7 produces tool names with the prefix `mcp__plugin_context7_context7__`, based on GitHub Issues #20983 and #15145 which were filed and closed in mid-2025. The deliverable presents this as a confirmed, current naming fact.

**Inversion:**
Claude Code released one or more updates between mid-2025 (issue close dates) and Feb 2026 (research date) that changed the plugin MCP naming convention -- for example, simplifying to `mcp__plugin_<name>__<tool>`, unifying plugin and manual namespaces, or reverting to short names. The double `context7_context7` pattern may already be a historical artifact.

**Plausibility:** Medium -- Claude Code releases frequently, and the plugin naming issues (#20983, #15145) were both closed, which could indicate either "won't fix" or "fixed differently." The deliverable acknowledges it "could not verify runtime behavior empirically" but does not flag this as a risk to the conclusion's validity.

**Consequence:**
If the plugin naming has changed, the core diagnosis that "agent definitions reference short names but the plugin creates long names that don't match" may be incorrect for current Claude Code. The recommended fix (remove plugin, use manual server) would still be valid as an architectural simplification, but the urgency and framing would differ.

**Evidence:**
Section L1.3: "the tool naming rules are: Plugin MCP Server | `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` | `mcp__plugin_context7_context7__resolve-library-id`" -- presented as current fact, not as "documented in mid-2025 issues, unverified in Feb 2026."

Section L1 Note: "Critical insight from GitHub Issue #15145: There is a known bug where installing a plugin can cause ALL MCP servers to be incorrectly namespaced under the plugin prefix." Issue #15145 status is "Closed as NOT PLANNED" -- the deliverable interprets this as "bug persists" but does not verify this interpretation.

**Mitigation:**
Add a mandatory empirical pre-check as Step 0 of the Recommendations: "Before implementing any fix, run `/mcp` in Claude Code to inspect the actual tool names currently presented at runtime. Confirm whether plugin-registered Context7 tools appear as `mcp__plugin_context7_context7__*` or under a different prefix. This converts the documentation-based diagnosis into an empirically grounded starting point."

**Acceptance Criteria:**
Recommendation section includes an explicit "Verify First" step with the `/mcp` command and instructions for interpreting the output before proceeding to fix implementation.

---

### IN-002-20260226: "NOT PLANNED" Closure Interpreted as Bug-Still-Present [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Type** | Assumption |
| **Section** | L1.3 (Tool Name Resolution), L2.1 (Dual-Registration Anti-Pattern) |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
Issue #15145 (MCP servers incorrectly namespaced under plugin) was "Closed as NOT PLANNED." The deliverable interprets this as meaning the namespace collision bug was not fixed and will persist. This interpretation drives the conclusion that the dual-registration is an active, ongoing problem.

**Inversion:**
"NOT PLANNED" could mean "addressed through a different mechanism" -- for example, the plugin naming was standardized in a later release so the specific behavior reported in #15145 no longer manifests, or the issue was superseded by #20983 (closed as duplicate of #20830). The bug may have been resolved without reopening #15145.

**Plausibility:** Medium -- GitHub issue closure labels in the Anthropic repo are not always descriptive of the resolution path. "NOT PLANNED" in the context of platform issues often means "the product direction changed in a way that made this issue moot."

**Consequence:**
If the namespace collision has been resolved in a Claude Code release, the dual-registration in `settings.json` may already be harmless (both registrations produce the same or compatible tool names). The fix recommendation is still architecturally sound, but the deliverable overstates the current severity if the underlying bug is already resolved.

**Evidence:**
Section L1.3, bullet point 2: "GitHub Issue #20983 confirms the plugin naming pattern `mcp__plugin_<plugin>_<server>__<tool>` is a distinct namespace from `mcp__<server-name>__<tool-name>`." Issue #20983 was "closed as duplicate of #20830" -- the duplicate's resolution is not documented in the deliverable.

Section L2.1: "Namespace ambiguity: Depending on which registration 'wins' at runtime, tools may appear under either prefix." This is stated as a present condition, not a historical one.

**Mitigation:**
Investigate the duplicate issue #20830 to understand its resolution status. Add a note in the Limitations section: "Issue #15145 was closed as NOT PLANNED; the specific duplicate issue #20830 was not investigated. The current plugin naming behavior should be verified empirically via `/mcp` before concluding the namespace collision is still active."

**Acceptance Criteria:**
Reference to #20830 included in Research Questions or Limitations. The severity of the "active namespace collision" framing is qualified with a temporal note.

---

### IN-003-20260226: No Integration Test Assumed Without Full Codebase Audit [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | L2 WHY section, Recommendations Short-Term |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
The WHY section states: "No integration test validates that agent tool references match actual runtime tool names." This is presented as a factual finding, but the research methodology section does not describe an audit of the test suite or CI configuration to confirm this.

**Inversion:**
A validation script or CI check already exists somewhere in the codebase that the researcher did not find -- for example, in a `scripts/` directory, a GitHub Actions workflow, or a pre-commit hook that compares TOOL_REGISTRY.yaml entries against actual `/mcp` output.

**Plausibility:** Low -- the existence of such a check would likely be referenced in the governance files that were audited. However, the deliverable does not state it searched for such a check.

**Consequence:**
If a validation check exists, Short-Term Recommendation #4 ("Add a pre-flight check") is redundant and may cause confusion or duplication. More importantly, if the check exists but is failing silently, the diagnosis is different from "no check exists."

**Evidence:**
WHY section, bullet 3: "No integration test validates that agent tool references match actual runtime tool names." This is asserted without evidence of a negative -- the methodology does not state "searched `scripts/`, GitHub Actions, and CI config; found no such test."

**Mitigation:**
Add a codebase search for validation scripts to the methodology: grep for `/mcp` references in CI configs, search `scripts/` and `.github/workflows/` for tool name validation. State the result explicitly: either "no such check found in [searched locations]" or "check found at [path] but [issue]."

**Acceptance Criteria:**
Methodology section documents the search for existing validation and explicitly states what was found (or not found) and where.

---

### IN-004-20260226: "7 Agent Definitions" Count Unverified [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | L2.5 (Impact on TOOL_REGISTRY.yaml) |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
Section L2.5 states: "every reference would need to change to `mcp__plugin_context7_context7__*`... This would affect 7 agent definitions and the registry itself." The number 7 is stated without documentation of which 7 files or how they were identified.

**Inversion:**
Additional agent definitions exist outside the locations audited -- for example, in project-specific orchestration directories, the `eng-team` or `red-team` skills, or newly added agents -- that also reference `mcp__context7__` tools and were not counted. Or the count is 6 or 8, not 7.

**Plausibility:** Low-Medium -- the codebase has 30+ agent definitions across multiple skills. The research methodology describes auditing `TOOL_REGISTRY.yaml` and `mcp-tool-standards.md` but not a comprehensive grep of all agent definition files.

**Consequence:**
If the count is wrong, the impact assessment in L2.5 and the Governance File Impact table in L2.6 are incomplete. An implementation team following these recommendations would miss files that need updating.

**Evidence:**
L2.5: "every reference would need to change... This would affect 7 agent definitions" -- no list of the 7 files is provided. L2.6 Governance File Impact table lists `settings.json`, `settings.local.json`, `TOOL_REGISTRY.yaml`, `mcp-tool-standards.md`, and "Agent definitions (7 files)" without identifying which 7.

**Mitigation:**
Add a finding appendix listing the specific 7 agent definition files by path. If not already done, run a grep for `mcp__context7` across all agent files to confirm completeness.

**Acceptance Criteria:**
L2.6 Governance File Impact table or an appendix lists the specific file paths for all 7 (or N) agent definitions. The count is backed by an explicit search.

---

### IN-005-20260226: Fix Recommendation Assumes Single-Developer Scope [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | L2.4 (Recommended Architecture), Recommendations Immediate |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
The recommended fix is: "Remove the `enabledPlugins` Context7 entry and configure Context7 as a user-scoped MCP server: `claude mcp add --transport sse --scope user context7 https://mcp.context7.com/sse`." User-scoped configuration writes to `~/.claude.json`, which is machine-local and not captured in source control. The recommendation is presented as the complete solution without addressing team-scale or CI runner implications.

**Inversion:**
The Jerry framework is a shared repository used by multiple contributors. A user-scoped MCP server fix works on the person who runs the command but leaves other contributors with the broken dual-registration until each one manually runs the command. CI runners have no `~/.claude.json` and cannot run the command without infrastructure changes.

**Plausibility:** High -- this is a structural consequence of user-scoped configuration, not a speculative edge case.

**Consequence:**
Following this recommendation produces an inconsistent state: one developer's environment works correctly; others continue to experience the namespace collision. The fix is incomplete as a project-level solution.

**Evidence:**
L2.4: "Recommended approach: Remove the `enabledPlugins` Context7 entry and configure Context7 as a user-scoped MCP server." No mention of team-scale implications or onboarding documentation requirement.

Recommendations, Immediate #1: "Remove `enabledPlugins.context7@claude-plugins-official` from `settings.json` and ensure Context7 is configured as a user-scoped manual MCP server." The `settings.json` change IS captured in source control; the user-scoped MCP add is NOT.

**Mitigation:**
Add a team-scale note to Recommendation #1: "The `settings.json` change removes the plugin globally (source-controlled). The `claude mcp add --scope user` command must be run by each contributor individually. Add the setup command to the project's developer onboarding documentation (e.g., `CONTRIBUTING.md` or `docs/setup.md`)."

**Acceptance Criteria:**
Recommendation #1 explicitly states where the setup command should be documented for team members and, if applicable, how CI runners should be configured.

---

### IN-006-20260226: Subagent MCP Access Gap Stated Unconditionally [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | L1.5 (Agent Definition mcpServers Field), L2.2 (Subagent MCP Access Gap) |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
Section L2.2 states: "If Context7's MCP server is only available at project scope, subagents may not be able to access it." Section L1.5 states: "If Context7 is only configured at the project level, subagents... may not be able to use it at all, and will hallucinate responses instead." These claims are sourced from GitHub Issue #13898.

**Inversion:**
The deliverable itself states in Section L1.5's tool inheritance table: when the `tools` field is omitted, "Subagent inherits ALL tools from main thread, including MCP tools." Many Jerry agents omit the `tools` field. If they inherit all tools from the main thread -- including project-scoped MCP tools -- then issue #13898 may only apply to agents with explicit `tools` lists that name the MCP tool directly.

**Plausibility:** Medium -- the two statements in L1.5 ("tools omitted = inherits ALL tools" and "project-scoped servers may not be accessible to subagents") are presented adjacently without reconciling the tension between them. The inheritance rule may supersede the project-scope limitation for agents with omitted tools fields.

**Consequence:**
If agents with omitted `tools` fields can access project-scoped MCP tools via inheritance, the scope of the access gap is narrower than presented. The fix recommendation (user-scoped configuration) remains valid but the severity framing would change.

**Evidence:**
L1.5 Tool Inheritance table: "`tools` field omitted | Subagent inherits ALL tools from main thread, including MCP tools." Immediately followed by: "Critical issue from GitHub #13898: Custom subagents CANNOT access project-scoped MCP servers." These are presented as co-equal facts without explaining which condition overrides the other.

**Mitigation:**
Add a reconciliation note: "The project-scope access gap from #13898 may only affect agents with explicit `tools` fields that name MCP tools directly. Agents with `tools` omitted may inherit project-scoped MCP tools through the main thread. This should be verified empirically. If true, the access gap is limited to agents with explicit tool lists."

**Acceptance Criteria:**
L2.2 distinguishes between the two tool field scenarios and qualifies the access gap claim accordingly.

---

### IN-007-20260226: SSE Transport Recommended Exclusively Without Evaluating npx Alternative [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | L2.4 (Recommended Architecture), Recommendations Immediate |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
The recommended command is: `claude mcp add --transport sse --scope user context7 https://mcp.context7.com/sse`. This uses the SSE transport pointing to the Upstash-hosted endpoint. The deliverable documents the npx alternative in L1.1 ("claude mcp add context7 -- npx -y @upstash/context7-mcp") but recommends only the SSE approach.

**Inversion:**
The Upstash SSE endpoint (`https://mcp.context7.com/sse`) may become unavailable, rate-limited, or deprecated. The npx approach (`npx -y @upstash/context7-mcp`) runs a local process that does not depend on external endpoint availability. The deliverable does not analyze this trade-off.

**Plausibility:** Medium -- SaaS endpoints can change URLs, introduce authentication requirements, or impose rate limits. The npx approach is self-contained and dependency-isolated.

**Consequence:**
Teams following the recommendation who configure SSE-based Context7 may face issues if the endpoint changes, while the npx approach would continue to work with only a package version update. The recommendation may prescribe a less robust configuration.

**Evidence:**
Recommendations, Immediate #1: "ensure Context7 is configured as a user-scoped manual MCP server" with SSE command shown. L2.4 table shows "Manual MCP Server" as recommended but does not distinguish between SSE and npx variants.

**Mitigation:**
Present both variants in the recommendation with trade-offs:
- SSE: `claude mcp add --transport sse --scope user context7 https://mcp.context7.com/sse` -- simpler, no local Node.js required, but depends on Upstash endpoint availability.
- npx: `claude mcp add context7 -- npx -y @upstash/context7-mcp` -- runs locally, does not depend on external endpoint, requires Node.js/npx.

**Acceptance Criteria:**
Recommendation #1 includes both variants with the trade-off noted. The team can make an informed choice based on their environment.

---

### IN-008-20260226: Wildcard Permission Syntax Reconciliation Is Unverified Inference [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption |
| **Section** | L1.4 (Permission System for MCP Tools) |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
Section L1.4 states that Issue #3107 (closed July 2025) said wildcards do NOT work, but the current documentation page says both `mcp__context7` and `mcp__context7__*` work. The deliverable concludes "both syntaxes now work" -- treating this as a reconciled finding.

**Inversion:**
The documentation page may be outdated or incorrect in stating that `mcp__context7__*` works. Issue #3107's resolution ("The correct syntax here is `mcp__atlassian`. Permission rules do not support wildcards.") represents an Anthropic engineer's explicit statement; the documentation page may not have been updated to reflect a policy change, or the wildcard support was added for only some permission contexts. The reconciliation "both now work" is inferred, not confirmed by a dated source showing when wildcard support was added.

**Plausibility:** High -- the tension between the issue response and the docs page is real and the deliverable explicitly notes it ("This indicates that both syntaxes now work... the wildcard support was likely added after Issue #3107 was filed in July 2025"). The word "likely" signals inference, but the final sentence presents it as confirmed.

**Consequence:**
If wildcards do NOT work in the `mcp__context7__*` form, then the current `settings.local.json` entries using that form (e.g., `"mcp__context7__*"`) are not actually granting wildcard permission -- only the specific individual tool names listed below them (`mcp__context7__resolve-library-id`, `mcp__context7__query-docs`) are active. This changes the permission simplification recommendation: `mcp__context7` (server-level) would be the only safe simplification, and individual tool names should be listed as backup.

**Evidence:**
L1.4: "This indicates that both syntaxes now work (the wildcard support was likely added after Issue #3107 was filed in July 2025)." The hedge word "likely" is present but the conclusion is stated as fact in the Recommendations section where `mcp__context7` is recommended without the caveat.

**Mitigation:**
Flag the permission syntax uncertainty explicitly. Recommend the server-level form `mcp__context7` (confirmed to work per #3107 and documentation) as the authoritative simplification, and note that `mcp__context7__*` may or may not be equivalent. The implementation should use `mcp__context7` to eliminate ambiguity.

**Acceptance Criteria:**
L1.4 and Recommendation #2 clearly distinguish the confirmed syntax (`mcp__context7`, server-level match) from the uncertain syntax (`mcp__context7__*`, possibly wildcard). The recommendation uses only the confirmed syntax.

---

### IN-009-20260226: Temporal Limitation Not Prominent in Summary or Recommendations [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption |
| **Section** | Limitations, L0 Executive Summary |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
The temporal limitation ("could not verify runtime behavior empirically") is documented in the Limitations section but is not surfaced in the L0 Executive Summary or the Recommendations section where it would most influence an implementer's caution level.

**Consequence:**
Readers who consume only the L0 summary or the Recommendations section (the most common stakeholder reading pattern) will not see the temporal caveat and may implement the fix assuming the diagnosis is empirically confirmed.

**Mitigation:**
Add one sentence to the L0 Executive Summary and prepend to Recommendation #1: "Note: These findings are based on documentation and GitHub issues from mid-2025; actual runtime tool names should be verified via `/mcp` before implementing."

**Acceptance Criteria:**
Temporal limitation appears in at least one of: L0 Executive Summary or Recommendation #1.

---

### IN-010-20260226: Plugin Removal Side Effects Not Analyzed [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption |
| **Section** | L2.4 (Recommended Architecture), Recommendations |
| **Strategy Step** | Step 4: Stress-Test Each Assumption |

**Original Assumption:**
The recommended approach removes `context7@claude-plugins-official` from `enabledPlugins`. The deliverable assumes this only affects the MCP server registration and has no other consequences.

**Consequence:**
Claude Code plugins may bundle capabilities beyond MCP servers -- for example, slash commands (`/context7:*`), plugin-specific UI elements, or additional integrations. Removing the plugin entry would remove these if they exist for Context7.

**Plausibility:** Low -- Context7 appears to be an MCP-only plugin; the plugin page description focuses on the MCP server functionality. However, this was not explicitly verified.

**Mitigation:**
Add a brief note: "Before removing the plugin entry, verify that Context7's plugin does not bundle capabilities beyond the MCP server (e.g., slash commands). Check the plugin page or Claude Code plugin documentation."

**Acceptance Criteria:**
A one-sentence note in Recommendation #1 documents that plugin-only capabilities (if any) will be lost with plugin removal.

---

## Anti-Goal Assessment

| Goal | Anti-Goal (Inversion) | Deliverable Status |
|------|----------------------|-------------------|
| G-1: Accurately characterize tool naming | Describe naming ambiguously; conflate plugin/manual lifecycles | MOSTLY ADDRESSED -- naming is clearly described but temporal currency is unverified (IN-001) |
| G-2: Explain namespace conflict consequences | Understate conflict as cosmetic; skip wildcard namespace analysis | PARTIALLY ADDRESSED -- the conflict is well explained but the wildcard syntax has an internal inconsistency (IN-008) |
| G-3: Provide actionable fix recommendations | Recommend the inferior option; omit user-scope requirement; conflict with agent definitions | PARTIALLY ADDRESSED -- single transport option (IN-007), missing team scope (IN-005), otherwise correct |
| G-4: Be evidence-based enough to guide a safe fix | Present unverified claims as empirically confirmed | NOT FULLY MET -- IN-001 and IN-002 are the primary gaps |
| G-5: Be complete enough to inform file updates | Omit files needing updates; misstate impact scope | PARTIALLY MET -- 7-file count unverified (IN-004), plugin removal side effects unanalyzed (IN-010) |
| G-6: Accurately characterize subagent MCP access gap | Mischaracterize #13898; understate severity; present workarounds as solutions | PARTIALLY MET -- the inheritance vs. project-scope tension is unresolved (IN-006) |

---

## Recommendations

### Critical -- MUST Mitigate Before Use in ADR or Implementation

**IN-001 -- Verify Plugin Prefix Naming at Runtime**
Action: Add Step 0 to Recommendations: "Run `/mcp` in Claude Code and inspect actual tool names before implementing any fix. Confirm whether plugin-registered Context7 tools currently appear as `mcp__plugin_context7_context7__*` or under a different prefix."
Acceptance Criteria: Recommendations section includes an explicit empirical verification step with the `/mcp` command.

**IN-002 -- Investigate #15145 NOT PLANNED and #20830 Resolution**
Action: Add research task: Investigate GitHub Issue #20830 (of which #20983 was a duplicate) to determine its resolution status. Clarify whether "NOT PLANNED" for #15145 means the namespace collision is permanently unfixed or was resolved via a different mechanism.
Acceptance Criteria: Limitations section references #20830 and states whether its resolution affects the diagnosis.

### Major -- SHOULD Mitigate Before Implementation

**IN-005 -- Team-Scale Implications of User-Scoped Fix**
Action: Add to Recommendation #1: "The `settings.json` change is source-controlled; the `claude mcp add --scope user` command must be run by each contributor individually. Document the setup command in `CONTRIBUTING.md` or project onboarding documentation."
Acceptance Criteria: Onboarding documentation location is specified in the recommendation.

**IN-006 -- Qualify the Subagent Access Gap by tools Field Scenario**
Action: Add reconciliation note to L2.2: "The access gap from #13898 may be limited to agents with explicit `tools` fields. Agents with `tools` omitted may inherit project-scoped MCP tools via the main thread. Verify empirically."
Acceptance Criteria: L2.2 explicitly distinguishes the two scenarios.

**IN-007 -- Present npx Alternative Alongside SSE**
Action: Add both transport options to Recommendation #1 with trade-offs (SSE: simpler, depends on Upstash endpoint; npx: local process, no external dependency).
Acceptance Criteria: Both variants appear in the recommendation.

**IN-008 -- Flag Wildcard Permission Syntax as Uncertain**
Action: Revise L1.4 to state the uncertainty explicitly. Change Recommendation #2 to recommend only `mcp__context7` (confirmed) rather than `mcp__context7__*` (uncertain).
Acceptance Criteria: Recommendation #2 uses only the server-level `mcp__context7` form.

**IN-003 -- Document Negative Search for Existing Validation**
Action: Add to Methodology: "Searched `scripts/`, `.github/workflows/`, and `Makefile` for existing MCP tool name validation; none found." If not yet searched, run the search.
Acceptance Criteria: Methodology states explicitly that no existing validation was found in specified locations.

**IN-004 -- List Specific Agent Files by Path**
Action: Add a table to L2.6 listing the specific file paths for all 7 agent definitions. Confirm the count via `grep -r "mcp__context7" skills/ projects/ .context/`.
Acceptance Criteria: L2.6 names all affected files by full path.

### Minor -- MAY Mitigate

**IN-009 -- Surface Temporal Limitation in Summary**
Action: Add one sentence to L0 Executive Summary noting that findings are documentation-based and should be verified via `/mcp` before implementation.

**IN-010 -- Note Plugin Removal Side Effects**
Action: Add a one-sentence note in Recommendation #1 confirming that no slash commands or non-MCP capabilities are bundled in the Context7 plugin (or noting they would be lost if they exist).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-004 (agent file count unverified), IN-005 (team-scale gap), IN-010 (plugin removal side effects not analyzed) reduce coverage of the full problem space |
| Internal Consistency | 0.20 | Negative | IN-008 (wildcard syntax claim is self-contradictory within L1.4 -- issue says no wildcards, docs say both work, conclusion states "both work" without resolving which source is authoritative) |
| Methodological Rigor | 0.20 | Negative | IN-005 (fix recommendation not scoped for all deployment contexts), IN-001/IN-002 (empirical verification step absent from recommendation protocol despite explicit acknowledgment that runtime was not tested) |
| Evidence Quality | 0.15 | Negative | IN-001 (plugin naming assumed current from mid-2025 issues), IN-002 (NOT PLANNED interpreted without secondary verification), IN-006 (subagent access claim does not reconcile with adjacent inheritance rule) |
| Actionability | 0.15 | Negative | IN-007 (single transport option; npx not evaluated), IN-008 (permission syntax ambiguity creates implementation risk -- implementer may use wrong form) |
| Traceability | 0.10 | Positive | All claims trace to specific GitHub issue numbers, file locations, and code snippets. The 5W1H structure and Research Questions table provide strong traceability. Minor deduction for IN-004 (agent files unnamed). |

**Most Vulnerable Assumption Cluster:** Documentation currency cluster -- IN-001, IN-002, IN-009 all share the dependency that mid-2025 GitHub issue descriptions accurately reflect Feb 2026 Claude Code runtime behavior. This cluster is highest-consequence because the entire architectural recommendation flows from the diagnosis of which namespace is produced at runtime. If Anthropic updated plugin MCP naming between mid-2025 and Feb 2026, the core framing changes.

**Overall Assessment:** REVISE. The deliverable's core architectural insight (dual-registration is an anti-pattern; choose one registration method; use user-scoped manual MCP server) is directionally correct and robust to inversion. No finding invalidates this conclusion. However, two Critical and six Major findings require mitigation: the most important is adding an empirical verification step (IN-001) before any implementation, and resolving the internal inconsistency in the wildcard permission claim (IN-008). Once these are addressed, the deliverable provides a sound basis for a BUG-002 filing and a subsequent ADR.

---

## Execution Statistics

- **Total Findings:** 10
- **Critical:** 2
- **Major:** 6
- **Minor:** 2
- **Protocol Steps Completed:** 6 of 6
- **Goals Analyzed:** 6 (4 explicit, 2 implicit)
- **Assumptions Mapped:** 14 (5 explicit, 9 implicit)
- **Assumption Categories Covered:** Technical (A6, A7, A8), Process (A9, A10), Resource (A11), Environmental (A12, A13), Temporal (A14)
- **Anti-Goals Assessed:** 6 (one per primary goal)
- **H-15 Self-Review:** Completed -- all findings have specific evidence; severity classifications meet criteria; IN-NNN identifiers consistent; summary table matches detailed findings; no findings minimized
