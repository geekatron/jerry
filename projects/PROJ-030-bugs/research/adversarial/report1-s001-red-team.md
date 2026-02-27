# Strategy Execution Report: Red Team Analysis (S-001)

## Execution Context

- **Strategy:** S-001 (Red Team Analysis)
- **Template:** `.context/templates/adversarial/s-001-red-team.md`
- **Deliverable:** `projects/PROJ-030-bugs/research/context7-permission-model.md`
- **Executed:** 2026-02-26T00:00:00Z
- **Criticality:** C4

---

## H-16 Compliance Notice

**S-003 Steelman output: NOT FOUND.**

Per template Step 1 Decision Point, S-003 (Steelman Technique) MUST be applied before S-001 (Red Team Analysis) per H-16. No S-003 execution artifact was found in `projects/PROJ-030-bugs/research/adversarial/`. Per H-16 the correct action is to STOP and flag a violation.

**Orchestrator notice:** This execution was performed because S-001 was explicitly requested at C4 criticality. The H-16 violation is recorded below as a process-level finding (RT-000). Red Team analysis proceeds against the un-Steelmanned deliverable, which means the analysis attacks the deliverable in its current form rather than its strongest-possible form. This may over-identify weaknesses that a Steelman pass would have addressed. The orchestrator MUST run S-003 before treating this Red Team output as authoritative.

---

## Threat Actor Profile

| Attribute | Description |
|-----------|-------------|
| **Goal** | Implement MCP tool access in a Jerry subagent and have that agent reliably invoke Context7 tools — without triggering permission prompts, silent denials, or tool-not-found errors — in a production multi-developer Jerry instance. |
| **Capability** | Full read access to the deliverable, Jerry codebase, `.claude/settings.json`, and agent definition files. Moderate Claude Code internals knowledge. Motivated to ship a working solution quickly and will take the report's recommendations at face value without independent verification. |
| **Motivation** | The practitioner trusts this research report as the authoritative SSOT for MCP permission configuration. If the report is incomplete, ambiguous, or contains untested recommendations, the practitioner's implementation will silently fail — causing tool invocation failures that are difficult to diagnose in production. |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| RT-000-20260226 | Critical | H-16 process violation: S-003 not run before S-001 | N/A (process) |
| RT-001-20260226 | Critical | Approach A migration path is partially incorrect and will cause tool access failure | L2: Architectural Implications, Migration Path |
| RT-002-20260226 | Critical | Memory-Keeper permission model is inconsistent with Context7 treatment, creating a latent configuration gap | L1: Technical Analysis, Level 4; L2: Recommendations |
| RT-003-20260226 | Major | Plugin naming formula is sourced from bug reports, not official specification — cited as HIGH credibility | Methodology, Limitations |
| RT-004-20260226 | Major | Wildcard permission status remains ambiguous but the report treats it as resolved | L1: Section 2 (Wildcard Permission Syntax) |
| RT-005-20260226 | Major | Agent `mcpServers` frontmatter treatment is incomplete and the claim is not substantiated | L1: Section 5, Impact on Jerry Framework Agent Definitions |
| RT-006-20260226 | Major | The 64-character tool name limit risk is dismissed as "Low" without measurement | L2: Risk Assessment |
| RT-007-20260226 | Minor | `allowed_tools` field discrepancy in `.claude/settings.json` noted but not resolved | L1: Section 3, Level 3 |
| RT-008-20260226 | Minor | Approach D's "all tools" consequence conflates agent-level inheritance with session-level inheritance | L2: Trade-Off Analysis |

---

## Detailed Findings

### RT-000-20260226: H-16 Process Violation — S-003 Not Applied [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | N/A (execution process) |
| **Strategy Step** | Step 1 (Define Threat Actor — H-16 compliance check) |

**Evidence:**
No S-003 Steelman execution artifact exists at any path under `projects/PROJ-030-bugs/research/adversarial/`. Template Step 1 Decision Point: "If S-003 Steelman output is missing: STOP. Flag H-16 violation."

**Analysis:**
H-16 is a HARD rule: "Steelman before critique." The S-001 template requires the deliverable to be strengthened before adversarial emulation begins, so that Red Team attacks the strongest version of the argument. Without S-003, the Red Team may identify weaknesses that a Steelman pass would have preemptively addressed, producing a false alarm rate that inflates the finding count. Conversely, the Steelman might have surfaced additional claims that create new attack surfaces — those would be missed by this Red Team run.

**Recommendation:**
Execute S-003 Steelman against `context7-permission-model.md`, persist the output to `projects/PROJ-030-bugs/research/adversarial/report0-s003-steelman.md`, then re-run S-001 Red Team against the Steelmanned version. Treat findings RT-001 through RT-008 as provisional until the S-003 pass is complete.

---

### RT-001-20260226: Approach A Migration Path is Partially Incorrect [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L2: Architectural Implications — Recommended Approach / Migration path |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors — Rule Circumvention + Dependency Attacks) |

**Attack Vector:**
A practitioner follows the recommended migration path verbatim. Step 2 of the migration path instructs:
```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp
```
This installs Context7 as a user-scoped standalone MCP server named `context7`. Step 3 then instructs: "Simplify `settings.local.json` permissions — remove plugin-prefixed entries / Keep only: `mcp__context7__*`, `mcp__context7__resolve-library-id`, `mcp__context7__query-docs`."

The attack: if the practitioner simplifies `settings.local.json` as instructed but the **plugin is NOT removed** from `.claude/settings.json` (Step 1 only says "Remove `context7@claude-plugins-official` from `.claude/settings.json` enabledPlugins"), the plugin MCP server may still register tools under the `mcp__plugin_context7_context7__` namespace alongside the new standalone server tools. Permission rules for `mcp__context7__*` would cover the standalone server but NOT the plugin-namespace tools. The practitioner would have a partial configuration where some tool invocations succeed and others silently fail, with no error message indicating a namespace collision.

Furthermore, the migration path provides no verification step. There is no instruction to confirm that after the migration, tool names are actually resolved as `mcp__context7__resolve-library-id` rather than the plugin-prefixed form. A practitioner cannot know if the migration succeeded without an explicit verification command.

**Category:** Dependency Attack (external tool and plugin system behavior) + Rule Circumvention (migration path incompleteness creates a loophole)
**Exploitability:** High — the migration path is the primary action item from the report; practitioners will follow it exactly
**Existing Defense:** None — the migration path contains no verification step and no warning about plugin-not-removed scenario
**Dimension:** Actionability

**Countermeasure:**
Add Step 1a to the migration path that explicitly verifies the plugin was removed:
```bash
# 1a. Verify plugin is disabled (no output = success)
grep -r "context7@claude-plugins-official" .claude/settings.json && echo "PLUGIN STILL ACTIVE — remove before continuing"
```
Add a Step 4 verification step after simplifying `settings.local.json`:
```bash
# 4. Verify tool names resolve correctly
claude mcp list  # should show 'context7' as a user-scoped MCP server
# Then confirm tool names in a fresh session via: /mcp (or equivalent)
```
Add a warning: "Do NOT simplify `settings.local.json` until you have confirmed the plugin is fully removed and the standalone MCP server is registered."

**Acceptance Criteria:** Migration path includes explicit plugin-removal verification, a rollback procedure if verification fails, and a final tool-name confirmation step that a practitioner can execute to confirm the migration succeeded.

---

### RT-002-20260226: Memory-Keeper Permission Model Inconsistency Creates Latent Gap [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | L1: Section 3 Level 4 (current `settings.local.json`); L2: Recommended Approach |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors — Boundary Violations) |

**Attack Vector:**
The deliverable correctly identifies that `settings.local.json` defensively covers both Context7 prefixes. However, the treatment of Memory-Keeper is asymmetric. The `settings.local.json` excerpt shows Memory-Keeper is covered only by:
```json
"mcp__memory-keeper__*",
"mcp__memory-keeper__store",
"mcp__memory-keeper__retrieve",
"mcp__memory-keeper__list",
"mcp__memory-keeper__delete",
"mcp__memory-keeper__search"
```

The report notes that Memory-Keeper "is configured as a standalone MCP server, not a plugin" (L2: Recommended Approach, item 3) — but the deliverable **does not verify this claim**. The Methodology section notes: "No access to `~/.claude/settings.json` — Permission denied when attempting to read user-level settings." If Memory-Keeper is configured at user scope (which `mcp-tool-standards.md` implies via its MCP integration matrix), the verification that it is truly a standalone server was not performed during this research.

The adversarial threat: if Memory-Keeper is also installed as a plugin (or migrates to plugin form in a future Claude Code update), its tools would be renamed to `mcp__plugin_memory-keeper_memory-keeper__store` etc., and the current `settings.local.json` entries would stop working. The report does not flag this as a risk for Memory-Keeper even though it applies identical logic to Context7.

Furthermore, the L2 Recommended Approach bases part of its Context7 recommendation (item 3: "consistent with how memory-keeper is configured") on an unverified assumption about Memory-Keeper's configuration method.

**Category:** Boundary Violation (asymmetric treatment of logically identical components)
**Exploitability:** Medium — requires Memory-Keeper to be affected by a similar plugin change, which hasn't happened but was observed for Context7
**Existing Defense:** None for Memory-Keeper in this scenario; partial for Context7
**Dimension:** Internal Consistency, Evidence Quality

**Countermeasure:**
1. Add explicit verification of Memory-Keeper's installation method to the Methodology section (attempt `claude mcp list` or equivalent to confirm it is standalone).
2. Add a parallel risk entry in the Risk Assessment table for Memory-Keeper plugin migration risk.
3. Revise Approach A recommendation item 3 to remove the unverified "consistent with memory-keeper" claim, or add a footnote: "Assuming Memory-Keeper is a standalone MCP server — verify with `claude mcp list`."
4. Add Memory-Keeper plugin-namespace coverage to `settings.local.json` as a defensive measure (analogous to how Context7 both prefixes are covered).

**Acceptance Criteria:** Report either verifies Memory-Keeper's installation type with evidence or explicitly scopes the comparison as an assumption with a caveat. Risk Assessment includes Memory-Keeper plugin migration risk. Report does not use unverified Memory-Keeper configuration as justification for Context7 recommendation.

---

### RT-003-20260226: Plugin Naming Formula Sourced from Bug Reports, Cited as HIGH Credibility [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Methodology — Sources Consulted; L1: Section 1 Formula B |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors — Evidence Quality / Ambiguity Exploitation) |

**Attack Vector:**
The deliverable's central factual claim — the Plugin-Bundled MCP tool naming formula `mcp__plugin_{plugin-name}_{server-name}__{tool-name}` — is sourced from GitHub Issue #23149 and confirmed by Issue #15145. Both are cited with **HIGH** credibility in the Methodology table.

However, the Limitations section acknowledges: "Plugin naming behavior is documented primarily through bug reports, not official specification. The `mcp__plugin_{plugin}_{server}__` formula is derived from observed behavior reported in GitHub issues, not from an official naming specification document."

The adversarial threat: the Methodology table rates both GitHub issues as HIGH credibility, but the Limitations section correctly identifies them as bug reports rather than official specification. This creates an internal signal mismatch. A practitioner reading the Methodology table in isolation would conclude these are high-quality primary sources on par with official documentation. In fact, they are secondary empirical observations from bug reporters who may have been using a specific Claude Code version, plugin version, or operating system where behavior differed from other environments.

The formula could be version-specific, OS-specific, or subject to change in a future Claude Code release without notice (since it is not part of the official specification). If the formula changes, the report's core finding becomes incorrect and any configuration built on it silently breaks.

**Category:** Ambiguity Exploitation (credibility rating inconsistent with source type)
**Exploitability:** Medium — requires the practitioner to rely on the plugin formula for configuration decisions, which the report directly encourages via Approach B and the defensive dual-prefix approach
**Existing Defense:** Partial — Limitations section notes the qualification, but it contradicts the Methodology table's HIGH rating
**Dimension:** Evidence Quality, Methodological Rigor

**Countermeasure:**
1. Downgrade GitHub Issues #23149 and #15145 credibility from HIGH to MEDIUM-HIGH with an annotation: "HIGH for the specific behavior observed; MEDIUM for generalizability across Claude Code versions."
2. Add a note to Formula B: "This formula is empirically derived from GitHub bug reports as of Q4 2025 — Q1 2026. Verify against current Claude Code version before implementing."
3. Add a "Formula Verification" subsection recommending the practitioner confirm the actual plugin tool names in their environment using `/mcp` inspection or a test agent invocation before implementing permissions or agent `tools` frontmatter.

**Acceptance Criteria:** Methodology credibility ratings are internally consistent with the Limitations section. Formula B includes a version-specificity caveat. A practitioner reading the report cannot implement plugin-prefix-based configuration without encountering an explicit verification step.

---

### RT-004-20260226: Wildcard Permission Status Treated as Resolved Despite Ambiguity [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1: Section 2 (Wildcard Permission Syntax) |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors — Ambiguity Exploitation) |

**Attack Vector:**
Section 2 documents a historical wildcard bug history across four GitHub issues (closed mid-to-late 2025). The section concludes: "The current official documentation now lists both `mcp__puppeteer` (bare name) and `mcp__puppeteer__*` (wildcard) as valid. This suggests the wildcard syntax may have been fixed in a later release, but the bare server name (without `__*`) is the more reliable and originally-supported form."

The word "suggests" in this conclusion is key — the report does not confirm wildcard support is fixed. Yet `settings.local.json` continues to use `mcp__context7__*` and `mcp__memory-keeper__*` wildcards as the first permission entries (before the explicit tool names). If wildcards silently fail (as they did in the bug reports), the wildcard entries provide a false sense of security and the system actually falls back to the explicit tool entries.

The adversarial threat: a practitioner might simplify `settings.local.json` to use only wildcards (`mcp__context7__*`) without the explicit tool entries, believing wildcards are now reliable based on the current documentation. This could cause silent permission failures for all Context7 tool calls if wildcard support is incomplete in their Claude Code version.

The report also does not specify which Claude Code version was current at time of research, making it impossible for a reader to determine whether the "suggests it may have been fixed" status applies to their installed version.

**Category:** Ambiguity Exploitation (unresolved technical uncertainty presented as resolved)
**Exploitability:** High — the `settings.local.json` example uses wildcards as the primary entry; practitioners may simplify by using only wildcards
**Existing Defense:** Partial — explicit tool entries are listed alongside wildcards in the example, providing a fallback, but the report does not explain that this is intentionally defensive
**Dimension:** Completeness, Actionability

**Countermeasure:**
1. Add a "Wildcard Safety Note" to Section 2: "Until wildcard support is confirmed stable in the current Claude Code release, always include explicit tool name entries alongside wildcard entries. Do NOT rely on wildcards alone."
2. Specify the Claude Code version (or version range) for which wildcard behavior was tested or observed in the referenced issues.
3. Add a recommendation to the `settings.local.json` example explaining that the combination of wildcard + explicit entries is intentionally defensive — wildcards provide convenience if they work; explicit entries are the reliable fallback.

**Acceptance Criteria:** Section 2 contains a clear guidance statement on wildcard reliability and when to use explicit tool names as fallback. `settings.local.json` example includes an explanatory comment. Practitioner cannot take wildcard-only approach based solely on this report.

---

### RT-005-20260226: Agent `mcpServers` Frontmatter Treatment is Incomplete [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L1: Section 5 — Impact on Jerry Framework Agent Definitions |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors — Boundary Violations) |

**Attack Vector:**
Section 5 identifies three mismatch impacts when Context7 is installed as a plugin:
1. Agent `tools` frontmatter — tool names won't match
2. Agent `mcpServers` frontmatter — "would need the plugin-qualified name"
3. Documentation and SOPs — all references assume non-plugin prefix

For impact #2, the deliverable states: "The `mcpServers` field in agent frontmatter references server names (e.g., `context7`), not tool names. This field would need the plugin-qualified name." This claim is not substantiated. The `mcpServers` frontmatter field behavior with plugin-bundled MCP servers is not explained in the deliverable, and the sub-agents documentation cited does not address how plugin server names are referenced in `mcpServers`.

The adversarial threat: a practitioner updating agent definitions per this report would not know how to correctly populate `mcpServers` for a plugin-bundled server. The report says "would need the plugin-qualified name" but gives no example of what that qualified name looks like, whether it is `context7@claude-plugins-official`, `plugin_context7_context7`, or some other form. An agent definition with an incorrectly populated `mcpServers` field may silently fail to load the MCP server, causing all tool invocations to fail.

**Category:** Boundary Violation (incomplete specification of the plugin-to-agent interface)
**Exploitability:** Medium — affects practitioners who update agent `mcpServers` fields per the report's guidance
**Existing Defense:** None — the claim "would need the plugin-qualified name" is stated without explanation or example
**Dimension:** Completeness, Actionability

**Countermeasure:**
1. Research and document the correct `mcpServers` frontmatter value for a plugin-bundled MCP server (test with a known agent that uses Context7 tools to determine what value works).
2. If `mcpServers` does not support plugin-bundled servers via any qualified name, state this explicitly: "Agent `mcpServers` frontmatter does not currently support plugin-bundled MCP servers — tool access must be achieved via `tools` allowlist instead."
3. Add a concrete example of the correct `mcpServers` value for Approach A (standalone server) and the limitation statement for Approach B/C (plugin configuration).

**Acceptance Criteria:** Section 5 provides a tested, concrete `mcpServers` value example for at least one configuration approach, or explicitly states that `mcpServers` cannot reference plugin-bundled servers with an authoritative source citation.

---

### RT-006-20260226: 64-Character Tool Name Limit Risk Dismissed Without Measurement [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | L2: Risk Assessment — "Tool name exceeds 64-char API limit with plugin prefix" |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors — Degradation Paths) |

**Attack Vector:**
The Risk Assessment table rates "Tool name exceeds 64-char API limit with plugin prefix" as Likelihood: Low with the justification "Context7 tools have short names." This justification is not supported by a character count.

GitHub Issue #23149 is titled "Plugin MCP tool names exceed 64-char limit" — it is literally the primary source for Formula B in this very report. The issue was opened because real tools exceeded the limit. The report cites this issue as evidence for the plugin naming formula but then dismisses the 64-char risk with "Context7 tools have short names" without performing the trivial verification of counting the characters.

**Measurement:**
- `mcp__plugin_context7_context7__resolve-library-id` = 49 characters (under 64)
- `mcp__plugin_context7_context7__query-docs` = 43 characters (under 64)

These are indeed under 64 characters. However, the report does not include this measurement. A practitioner reading the report cannot verify the "Low" likelihood claim without performing this calculation independently. More importantly, a future tool added to Context7 with a longer name (e.g., `resolve-library-id-with-fallback`) would produce a name of 70 characters, exceeding the limit — and nothing in the report alerts the practitioner to check new tools.

**Category:** Degradation Path (risk present for future Context7 tool additions, not verified for current tools)
**Exploitability:** Low for current tools (confirmed above), Medium for future tool additions
**Existing Defense:** Partial — Approach A recommendation mitigates this risk, but the reasoning for the "Low" likelihood rating is unverified
**Dimension:** Evidence Quality, Methodological Rigor

**Countermeasure:**
1. Add explicit character counts for all current Context7 plugin-prefixed tool names in the Risk Assessment entry.
2. Change likelihood justification from "Context7 tools have short names" to: "Current tools: `mcp__plugin_context7_context7__resolve-library-id` (49 chars), `mcp__plugin_context7_context7__query-docs` (43 chars) — both under the 64-char limit. Risk elevates to High if Context7 adds tools with names exceeding 15 characters."
3. Add a monitoring note: "If Context7 adds new tools, verify the plugin-prefixed name length before using Approach B or C."

**Acceptance Criteria:** Risk Assessment entry for the 64-char limit includes actual character counts for all current Context7 plugin-prefixed tool names, and the likelihood justification is verifiable by the reader.

---

### RT-007-20260226: `allowed_tools` Field Discrepancy Noted but Not Resolved [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | L1: Section 3, Level 3 (Project Settings / Shared) |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors — Ambiguity Exploitation) |

**Evidence:**
Section 3 Level 3 states: "Relevant finding: The Jerry project's `.claude/settings.json` uses `allowed_tools` (which appears to be a legacy or custom field). The standard Claude Code schema uses `permissions.allow` and `permissions.deny`."

The deliverable identifies this discrepancy but does not resolve it. "Appears to be a legacy or custom field" is hedged language that leaves the practitioner uncertain whether `allowed_tools` is functional, deprecated, silently ignored, or a known alias.

**Analysis:**
If `allowed_tools` in `.claude/settings.json` is silently ignored by Claude Code (not the same as `permissions.allow`), any tool permissions specified there are non-functional. This would mean the shared project settings have no effective tool permissions, making the local `settings.local.json` the only active permission layer. The deliverable does not verify this or alert practitioners to validate whether `allowed_tools` entries are being honored.

**Recommendation:**
Verify whether `allowed_tools` in `.claude/settings.json` is honored by Claude Code (test by adding a known permission and checking if permission prompts disappear). If it is not honored, add a Critical finding to the research report noting that shared project tool permissions are non-functional and all practitioners must rely on `settings.local.json`. Update the finding with the authoritative Claude Code schema documentation reference.

---

### RT-008-20260226: Approach D Consequence Conflates Agent-Level and Session-Level Inheritance [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | L2: Trade-Off Analysis — Approach D |
| **Strategy Step** | Step 2 (Enumerate Attack Vectors — Ambiguity Exploitation) |

**Evidence:**
Approach D states: "Cons: Agents get access to ALL tools, violating principle of least privilege (T1-T5 tier model in `agent-development-standards.md`)."

The deliverable's own L1 Section 5 states: "If [tools is] omitted, the subagent inherits ALL tools from the parent conversation." This is correct. However, the T1-T5 tier model in `agent-development-standards.md` defines tool tiers as a design-time constraint on agent definitions, not a runtime enforcement mechanism. Whether an agent "inherits all tools" depends on what tools are available in the parent conversation context — which is governed by the permission layers described in Section 3, not solely by the `tools` frontmatter.

**Analysis:**
The characterization of Approach D's consequence is directionally correct (omitting `tools` is a least-privilege violation) but overstates the risk slightly. An agent that omits `tools` inherits all tools the parent conversation has access to — which is already constrained by `settings.json` and `settings.local.json` permissions. It does not get access to tools the parent conversation doesn't have. This is a minor clarification opportunity rather than a fundamental error.

**Recommendation:**
Revise Approach D cons to: "Agents get access to ALL tools available in the parent conversation (constrained by session-level permissions, but unconstrained at the agent level), violating the T1-T5 least-privilege tier model." This preserves the accuracy of the least-privilege concern while not implying agents can exceed the parent's permission set.

---

## Recommendations

### P0 — Critical: MUST Mitigate Before Acceptance

**RT-000: H-16 Process Violation**
Run S-003 Steelman against the deliverable, persist the output, and re-run S-001 Red Team against the strengthened version. Treat this report as provisional until H-16 compliance is achieved.

**RT-001: Migration Path Verification Gap**
Add plugin-removal verification step, tool-name confirmation step, and rollback procedure to the Approach A migration path before it is presented as an actionable recommendation. Acceptance: migration path tested end-to-end with explicit verification commands.

**RT-002: Memory-Keeper Configuration Assumption**
Verify Memory-Keeper installation type (standalone vs plugin), remove unverified comparison from Approach A rationale, and add symmetric risk coverage for Memory-Keeper in the Risk Assessment table. Acceptance: Memory-Keeper's installation type is verified with evidence (`claude mcp list` output or equivalent).

### P1 — Important: SHOULD Mitigate

**RT-003: Plugin Formula Credibility Mismatch**
Downgrade GitHub issue credibility ratings to reflect their status as bug reports (not official specification), add version-specificity caveat to Formula B, and add a practitioner-facing verification step. Acceptance: no internal contradiction between Methodology table and Limitations section.

**RT-004: Wildcard Ambiguity**
Add explicit wildcard safety note, explain the defensive intent of wildcard + explicit entries combination, and add a Claude Code version specification. Acceptance: practitioner cannot rely on wildcards-only configuration based on this report.

**RT-005: `mcpServers` Frontmatter Gap**
Research and document correct `mcpServers` frontmatter for plugin-bundled and standalone server configurations. Acceptance: concrete tested example or explicit "not supported" statement with authoritative source.

**RT-006: 64-Char Limit Measurement**
Add actual character counts for current Context7 plugin-prefixed tool names and a monitoring note for future tools. Acceptance: likelihood justification is verifiable by the reader from report text alone.

### P2 — Monitor

**RT-007: `allowed_tools` Field**
Verify whether `allowed_tools` in `.claude/settings.json` is honored by Claude Code. Document finding and update shared project settings if non-functional.

**RT-008: Approach D Inheritance Clarification**
Refine Approach D cons statement to accurately describe agent-level vs session-level inheritance. Minor editorial improvement.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-001 (migration path missing verification steps), RT-005 (mcpServers frontmatter treatment incomplete), RT-006 (64-char measurement absent), RT-002 (Memory-Keeper analysis incomplete) — multiple coverage gaps in core recommendations |
| Internal Consistency | 0.20 | Negative | RT-002 (Memory-Keeper comparison based on unverified assumption), RT-003 (credibility ratings contradict Limitations section), RT-004 (wildcard status inconsistently treated as resolved) — report makes claims that contradict its own acknowledged limitations |
| Methodological Rigor | 0.20 | Negative | RT-003 (empirically-derived formula presented with same credibility as official docs), RT-006 (risk dismissed without measurement), RT-002 (key claim not verifiable due to access limitation but not flagged accordingly) — research methodology applied inconsistently across the findings |
| Evidence Quality | 0.15 | Negative | RT-003 (bug report sources rated as HIGH without qualification), RT-006 (no character counts for the risk being assessed), RT-005 (mcpServers claim not substantiated) — evidence quality varies significantly across sections |
| Actionability | 0.15 | Negative | RT-001 (migration path missing verification — primary action item is unsafe to follow as written), RT-004 (wildcard guidance leaves practitioner unable to choose safely), RT-005 (mcpServers guidance missing) — the report's primary value is actionable recommendations; gaps here are high-impact |
| Traceability | 0.10 | Neutral | Research questions are clearly documented, sources are cited with URLs, findings link to specific sections. Limitation: RT-003 shows credibility-to-source mapping is imprecise, but the sources themselves are traceable. |

**Overall Assessment:** REVISE — Major remediation required for P0 and P1 findings before the research report can be trusted as a practitioner guide. The core factual analysis (separate namespaces, two formulas, four permission levels) is sound and well-sourced. The vulnerability lies in the actionability layer: the migration path, risk assessment, and agent definition impact sections contain gaps that would cause practitioners to implement incorrect or incomplete configurations. After addressing RT-001 through RT-006, the report quality should improve substantially across Completeness, Actionability, and Internal Consistency dimensions.

---

## Execution Statistics

- **Total Findings:** 9 (including RT-000 process finding)
- **Critical:** 3 (RT-000, RT-001, RT-002)
- **Major:** 4 (RT-003, RT-004, RT-005, RT-006)
- **Minor:** 2 (RT-007, RT-008)
- **Protocol Steps Completed:** 5 of 5
- **H-16 Status:** VIOLATION — S-003 Steelman not applied prior to this execution
- **Recommendation:** REVISE (pending S-003 pass and P0/P1 mitigations)
