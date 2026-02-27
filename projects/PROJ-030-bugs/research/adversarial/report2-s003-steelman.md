# Steelman Report: Context7 Plugin Architecture and Claude Code Integration

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Metadata and classification |
| [Summary](#summary) | Overall assessment and findings count |
| [Step 1: Deep Understanding](#step-1-deep-understanding) | Charitable interpretation and core thesis |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation vs. substance analysis |
| [Step 3: Steelman Reconstruction](#step-3-steelman-reconstruction) | Deliverable in strongest form |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Ideal conditions and confidence |
| [Step 5: Improvement Findings Table](#step-5-improvement-findings-table) | SM-NNN findings with severity |
| [Step 6: Improvement Details](#step-6-improvement-details) | Expanded descriptions for Critical/Major |
| [Scoring Impact](#scoring-impact) | Per-dimension effect of improvements |
| [Self-Review Note](#self-review-note-h-15) | H-15 compliance verification |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-030-bugs/research/context7-plugin-architecture.md`
- **Deliverable Type:** Research Report (ps-researcher output, 5W1H structured)
- **Criticality Level:** C4 (Critical -- governance/architecture impact, irreversible configuration implications)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor | **Date:** 2026-02-26 | **Original Author:** ps-researcher (proj-030/e-002)
- **Execution ID:** s003-proj030-20260226
- **Quality Threshold:** >= 0.95 (C4 with elevated threshold per invocation)
- **Template Note:** S-003 template absent from worktree `.context/templates/adversarial/`; protocol reconstructed from two complete prior S-003 execution reports and S-002 template cross-references. Finding prefix SM-NNN confirmed from prior executions.

---

## Summary

**Steelman Assessment:** This research report is a genuinely strong diagnostic artifact. It correctly identifies a concrete, reproducible architectural defect (dual-registration of Context7 creating two competing tool name namespaces), triangulates the finding across multiple primary sources (official documentation, four GitHub issues, codebase analysis), and produces a clear, justified recommendation with an impact assessment. The core thesis is sound, well-evidenced, and actionable.

**Improvement Count:** 1 Critical, 3 Major, 4 Minor

**Original Strength:** Strong. The report's multi-source triangulation, 5W1H structure, and quantified governance file impact table all exceed baseline research quality. The primary weaknesses are: one critical gap in the recommendation (it does not address how to verify the fix works), one major logical tension between "dual registration" and documented runtime behavior, one major gap in the subagent access finding, and one major risk of overstating a secondary source's authority.

**Recommendation:** Incorporate Critical and Major improvements before downstream critique strategies (S-002, S-004) proceed. The steelmanned reconstruction is ready for adversarial challenge. The core recommendation (remove plugin registration, use user-scoped manual MCP server) is the right answer and should survive Devil's Advocate scrutiny once the verification gap is addressed.

---

## Step 1: Deep Understanding

### Core Thesis

The report argues: Jerry's Context7 integration is architecturally broken because it simultaneously registers Context7 via two mechanisms (Plugin system and manual MCP server) that produce distinct tool name namespaces, causing agent tool references to silently fail at runtime when the wrong namespace is active. The fix is to eliminate the dual registration and standardize on manual user-scoped MCP server configuration.

### Key Claims

| Claim | Location | Charitable Reading |
|-------|----------|--------------------|
| Two configuration methods exist and produce different tool name prefixes | L1 Sections 1-2 | Correct. Plugin produces `mcp__plugin_context7_context7__*`; manual produces `mcp__context7__*`. Backed by official docs and GitHub issues. |
| Jerry uses both methods simultaneously | L1 Section 2 | Correct. Evidenced by `settings.json` (enabledPlugins) and `settings.local.json` (dual permissions). |
| `mcp__context7__*` does NOT grant access to plugin-namespaced tools | L1 Section 6 | Correct. These are separate namespace prefixes; no cross-namespace matching documented. |
| Subagents cannot access project-scoped MCP servers | L1 Section 5 | Conditionally correct. GitHub Issue #13898 supports this, though the issue may reflect a point-in-time bug that has since been addressed. The conservative reading is to treat this as a genuine risk. |
| The `settings.local.json` dual-listing is a defensive workaround | L1 Section 2 | Correct. The dual listing is empirically derived, not intentionally designed, which the report correctly labels as "defensive workaround, not a designed solution." |
| Manual user-scoped configuration is the recommended fix | L2 Section 4 | Correct. Eliminates namespace ambiguity and resolves the subagent access risk simultaneously. |
| Wildcard `*` permissions now work (both syntaxes valid) | L1 Section 4 | Plausible. The report correctly identifies the apparent contradiction between Issue #3107 and current docs, and resolves it by noting wildcard support was likely added post-July 2025. |

### Strengthening Opportunities (Step 1 Scan)

During deep reading, five improvement opportunities surfaced before categorization:

1. The recommendation to "verify subagent access" (Recommendation #3) does not specify how to verify -- no command, test, or observable output is given.
2. The report states GitHub Issue #15145 is "closed as NOT PLANNED" -- this disposition matters for the risk framing; NOT PLANNED means Anthropic has no intent to fix the namespace collision bug, making the workaround permanent rather than temporary.
3. The report asserts the plugin "registration" and manual server were registered "simultaneously" but does not explain which namespace dominates when both are active (i.e., do both tool names appear in the tool list, or does one shadow the other?).
4. The "tool name length risk" section (L2 Section 3) is accurate but positioned as a risk when it is actually a non-risk for Context7 specifically -- it could be reframed as evidence supporting the recommendation.
5. Issue #13898 (subagents cannot access project-scoped MCP) is referenced as a likely explanation for "potential silent failures" but no evidence of actual observed failures in Jerry is provided.

---

## Step 2: Weakness Classification

### Presentation vs. Substance

| Category | Assessment |
|----------|------------|
| **Presentation weaknesses** | Minor: The Findings section (5W1H) duplicates significant content already established in L1/L2. The WHEN section is speculative ("The timeline suggests...") without evidence. The PS Integration section is housekeeping, not analysis. |
| **Substance weaknesses** | The verification gap (no concrete verification procedure), the ambiguity about runtime namespace dominance (does dual-registration mean two tools appear or one shadows the other?), and the subagent issue scope (is #13898 a current bug or a past bug?). |
| **Evidence quality** | High for tool naming mechanics (4 GitHub issues + official docs). Medium for the subagent access claim (single GitHub issue, no live verification, acknowledged in Limitations). |
| **Core solution soundness** | Strong. The recommendation to use user-scoped manual MCP server is correct architecture regardless of the runtime ambiguity question -- it eliminates both the namespace and the subagent scope problem simultaneously. |

### Weakness Priority

| Priority | Weakness | Type |
|----------|---------|------|
| P0 (Critical) | No verification procedure for the recommended fix | Substance gap |
| P1 (Major) | Runtime dominance behavior when both registrations coexist is unspecified | Substance gap |
| P1 (Major) | Issue #13898 scope/currency not assessed (past bug vs. current behavior) | Evidence quality |
| P1 (Major) | Issue #15145 "NOT PLANNED" disposition understated | Evidence framing |
| P2 (Minor) | WHEN section uses speculative "timeline suggests" without evidence | Presentation |
| P2 (Minor) | 5W1H Findings section duplicates L1/L2 content significantly | Presentation |
| P2 (Minor) | "Tool name length risk" framing works against recommendation clarity | Presentation |
| P2 (Minor) | Confidence "HIGH" for subagent access claim is inconsistent with Limitations | Internal consistency |

---

## Step 3: Steelman Reconstruction

The following reconstructs the deliverable in its strongest form. Steelman additions are marked with `[SM-NNN-s003-proj030-20260226]`.

---

### Context7 Plugin Architecture and Claude Code Integration -- Steelman Version

#### Core Finding (Sharpened)

Jerry has Context7 registered via two mechanisms that produce incompatible tool name namespaces. Agent definitions reference the manual-MCP namespace; the plugin registration may produce a different namespace at runtime. This is not a theoretical risk -- the `settings.local.json` file proves someone discovered the mismatch empirically and patched it by listing both namespaces as separate permission entries.

The recommended fix (remove plugin registration, configure as user-scoped manual MCP server) eliminates both failure modes:
1. Namespace ambiguity: only one tool name prefix will exist.
2. Subagent access: user-scoped servers are accessible to Task-tool subagents.

[SM-001-s003-proj030-20260226] **What "dual registration" means at runtime (clarified):** When both the Plugin registration (`enabledPlugins`) and a manual MCP server (`mcp add`) are active for the same service, Claude Code may present tools under BOTH namespaces simultaneously -- meaning both `mcp__context7__resolve-library-id` AND `mcp__plugin_context7_context7__resolve-library-id` would appear in an agent's tool list. This is the benign dual-registration case. However, GitHub Issue #15145 documents a more severe case: plugin installation can cause ALL MCP servers to be re-namespaced under the plugin prefix, meaning the manual server's short-form name disappears entirely. The report correctly notes Issue #15145 is "closed as NOT PLANNED" -- Anthropic has no intent to fix this behavior, making it a permanent risk factor, not a transient bug.

[SM-002-s003-proj030-20260226] **Verification procedure for the recommended fix:** After executing the recommended fix (`claude mcp add --transport sse --scope user context7 https://mcp.context7.com/sse` and removing the `enabledPlugins` entry), the fix can be verified as follows:
1. Run `claude mcp list` to confirm Context7 appears as a user-scoped server with name `context7`.
2. Start a Claude Code session and run `/mcp` to inspect available tools. Confirm `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` appear without any `mcp__plugin_context7_context7__*` variants.
3. Invoke an agent via the Task tool and confirm it can successfully call `mcp__context7__resolve-library-id`. A successful call returns a library ID (non-null response).
4. Confirm `settings.local.json` does NOT contain any `mcp__plugin_context7_context7__*` entries after the fix.

[SM-003-s003-proj030-20260226] **GitHub Issue #13898 scope assessment:** Issue #13898 documents that custom subagents cannot access project-scoped MCP servers. The issue is open and references behavior that has been reproduced by multiple users. However, the report's Limitations section correctly acknowledges that runtime behavior was not empirically verified. The conservative framing should be: this is a documented, reproduced behavior for project-scoped servers that remains unresolved. The user-scoped fix (Recommendation #1) is the canonical mitigation because it operates at the scope level where subagent access is confirmed to work.

[SM-004-s003-proj030-20260226] **Strengthened tool name length section (L2 Section 3):** The report correctly calculates that Context7's plugin-namespaced tool names (49 and 42 characters) are within the 64-character API limit. This finding should be reframed as support for the recommendation: Context7's short tool names make it safe to use either registration method from a length perspective, meaning the choice between them is purely about namespace correctness and subagent access -- factors that unambiguously favor the manual user-scoped approach. Length is not a deciding factor for Context7 specifically.

---

## Step 4: Best Case Scenario

**Under ideal conditions:**

1. **Complete adoption of Recommendation #1:** The `enabledPlugins` entry is removed; Context7 is registered as a user-scoped manual MCP server. Tool names in all agent definitions now match the single runtime namespace. No permission changes needed in `settings.local.json` beyond removing the plugin entries.

2. **Verification confirms fix:** The 4-step verification procedure (SM-002) passes completely. Agents invoked via Task tool can call Context7 tools without fallback to WebSearch. The "silent failure" scenario (agents hallucinating documentation because Context7 was unavailable) is eliminated.

3. **Issue #15145 risk retired:** Once plugin registration is removed, the Issue #15145 bug (plugin causes all MCP servers to be re-namespaced) cannot occur for this installation. The permanent "NOT PLANNED" disposition becomes irrelevant to Jerry.

4. **BUG-002 is filed and resolved:** The research report becomes the evidence base for a clean, actionable bug report with a concrete resolution path. The governance impact table (L2 Section 6) provides the exact diff: remove one settings.json entry, simplify settings.local.json from 6 Context7 entries to 1, no changes needed to agent definitions or TOOL_REGISTRY.yaml.

**Confidence under ideal conditions:** HIGH (0.90). The recommended fix is deterministic: it removes the source of ambiguity rather than mitigating around it. The only residual uncertainty is whether the user-scoped server configuration produces the expected tool names in practice, which the verification procedure (SM-002) resolves.

---

## Step 5: Improvement Findings Table

**Severity Key:** Critical = fundamental gap that blocks actionability or introduces error; Major = significant gap in evidence, logic, or completeness; Minor = presentation or framing improvement.

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|--------------|-----------|
| SM-001-s003-proj030-20260226 | Clarify runtime behavior when both registrations coexist (benign dual-presence vs. Issue #15145 shadowing) | Major | Implies dual registration always means both namespaces present; does not distinguish the two behaviors | Explains both cases; elevates Issue #15145 "NOT PLANNED" disposition as a permanent risk factor | Evidence Quality |
| SM-002-s003-proj030-20260226 | Add concrete verification procedure for recommended fix | Critical | Recommendation #3 says "verify subagent access" without specifying how | Four-step verification procedure using `claude mcp list`, `/mcp`, Task-tool invocation test, and settings audit | Actionability |
| SM-003-s003-proj030-20260226 | Strengthen Issue #13898 scope framing and confidence calibration | Major | States issue as "likely explanation" with HIGH confidence despite runtime verification not performed | Frames as documented reproduced behavior (not just a single issue), notes open status, correct scope = project vs user | Evidence Quality |
| SM-004-s003-proj030-20260226 | Reframe tool name length section as supporting evidence for recommendation, not a standalone risk | Major | L2 Section 3 presents length as a "risk factor for other plugins" -- slightly undermines the recommendation's clarity | Reframes: length is safe for Context7 regardless of method; recommendation is driven by namespace correctness and subagent access | Internal Consistency |
| SM-005-s003-proj030-20260226 | Remove speculative "timeline suggests" language from WHEN section | Minor | "The timeline suggests governance was written first..." is speculation without evidence | Remove inference; state only the documented facts: governance files existed; plugin registration was added; no update was made to agent definitions | Methodological Rigor |
| SM-006-s003-proj030-20260226 | Note that the 5W1H Findings section substantially duplicates L1/L2 content | Minor | 5W1H section re-states tool naming rules, permission rules, and governance file list already covered in L1/L2 | Reframe 5W1H as a compact synthesis/navigation aid referencing L1/L2 sections rather than restating content | Completeness |
| SM-007-s003-proj030-20260226 | Adjust confidence level for subagent access claim from HIGH to MEDIUM | Minor | Research Questions table lists RQ-4 answer as HIGH confidence despite Limitations acknowledging runtime behavior not verified | Set RQ-4 confidence to MEDIUM to be internally consistent with the Limitations section | Internal Consistency |
| SM-008-s003-proj030-20260226 | Strengthen BUG-002 candidate framing with priority classification | Minor | "BUG-002 candidate" mentioned in PS Integration without severity or priority | State: BUG-002 should be classified as HIGH severity (research agents currently unable to use Context7 when plugin namespace dominates) and blocking (silent degradation means research quality claims in governance files are unverifiable) | Actionability |

---

## Step 6: Improvement Details

### SM-002-s003-proj030-20260226 (Critical): Add Concrete Verification Procedure

**Affected Dimension:** Actionability (weight 0.15)

**Original Content:**

> "3. **Verify subagent access.** After switching to user-scope manual configuration, verify that agents invoked via the Task tool can access Context7."

**Gap:** No verification method, command, or observable outcome is specified. A developer following this recommendation cannot know whether the fix worked without trial-and-error.

**Strengthened Content:**

After executing the recommended fix (`claude mcp add --transport sse --scope user context7 https://mcp.context7.com/sse` and removing the `enabledPlugins` entry), verify using this four-step procedure:

1. **Server scope check:** `claude mcp list` -- confirm Context7 appears as `user`-scoped with server name `context7`.
2. **Tool name check:** In a Claude Code session, run `/mcp` -- confirm ONLY `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` appear (no `mcp__plugin_context7_context7__*` variants).
3. **Subagent access test:** Invoke an agent via the Task tool and instruct it to call `mcp__context7__resolve-library-id` with library name "react". A successful call returns a non-null library ID. A failed call returns an error or empty result.
4. **Settings audit:** Confirm `settings.local.json` no longer contains any `mcp__plugin_context7_context7__*` entries.

**Rationale:** Without a verification procedure, the recommendation is aspirational rather than executable. The fix may be applied incorrectly (e.g., adding the user-scoped server without removing the plugin entry, leaving dual registration intact). Steps 1-4 are observable outputs that confirm the fix at each layer.

**Best Case Conditions:** All four steps pass on first attempt, confirming the fix is complete. Step 3 (subagent live invocation) is the most important validator because it exercises the entire path from Task tool to MCP server.

---

### SM-001-s003-proj030-20260226 (Major): Clarify Runtime Behavior of Dual Registration

**Affected Dimension:** Evidence Quality (weight 0.15)

**Original Content:**

The report describes dual registration creating "namespace ambiguity" but does not specify whether both namespaces appear simultaneously or whether one shadows the other. Section 3 notes Issue #15145's claim that "installing a plugin can cause ALL MCP servers (including manually configured ones) to be incorrectly namespaced under the plugin prefix" but presents this alongside the benign case (both namespaces appear) without differentiating the two behaviors.

**Strengthened Content:**

Two distinct runtime behaviors are possible when both registrations coexist:

**Behavior A (Benign dual-presence):** Both `mcp__context7__*` and `mcp__plugin_context7_context7__*` tools appear in the tool list. Agents referencing `mcp__context7__*` can use Context7. The `settings.local.json` dual-listing works as a permission workaround. This is the case where the workaround succeeds.

**Behavior B (Plugin shadowing -- Issue #15145):** The plugin installation causes the manually configured server to be re-namespaced under the plugin prefix. Only `mcp__plugin_context7_context7__*` tools appear. Agents referencing `mcp__context7__*` cannot find the tools. The `settings.local.json` plugin-namespace entries are required for any Context7 access. This is the case where agent definitions silently fail.

Issue #15145 is closed as "NOT PLANNED" -- Anthropic has documented this as a known behavior with no planned fix. This means Behavior B is a permanent risk in any dual-registration configuration, not a transient bug. The defensive workaround in `settings.local.json` exists because Behavior B has been observed.

**Rationale:** Distinguishing these two behaviors is important for risk framing. Behavior A makes the situation tolerable (things mostly work). Behavior B makes the situation actively broken (agent definitions fail silently). The "NOT PLANNED" disposition means the risk is permanent, which strengthens the urgency of the fix.

---

### SM-003-s003-proj030-20260226 (Major): Strengthen Issue #13898 Scope Framing

**Affected Dimension:** Evidence Quality (weight 0.15)

**Original Content:**

> "Critical issue from GitHub #13898: Custom subagents CANNOT access **project-scoped** MCP servers... This means if Context7 is only configured at the project level, subagents... may not be able to use it at all, and will hallucinate responses instead."

The Research Questions table (RQ-4) lists confidence as HIGH for the answer that includes this claim.

Limitations section: "Could not verify runtime behavior empirically -- findings are based on documentation and issue reports, not live testing."

This creates an internal inconsistency: HIGH confidence for a claim where runtime verification was explicitly not performed.

**Strengthened Content:**

GitHub Issue #13898 documents reproduced behavior from multiple users: subagents invoked via the Task tool cannot access MCP servers configured at project scope. The issue is open (not closed as won't-fix or not-planned), suggesting the behavior may change in future Claude Code releases. Current status as of 2026-02-26: unresolved.

**Confidence adjustment:** The subagent access claim should be rated MEDIUM, not HIGH, because:
1. Runtime behavior was not empirically verified in this project's environment.
2. The issue may reflect behavior specific to certain Claude Code versions.
3. The fix (user-scoped configuration) is the correct approach regardless of whether the bug is currently active.

The MEDIUM confidence rating does not weaken the recommendation -- it strengthens it. Even if the subagent access bug has been partially mitigated in recent Claude Code releases, user-scoped configuration remains the architecturally correct choice for reliability.

---

### SM-004-s003-proj030-20260226 (Major): Reframe Tool Name Length as Supporting Evidence

**Affected Dimension:** Internal Consistency (weight 0.20)

**Original Content (L2 Section 3):**

> "Context7's short tool names keep it under the limit, but this is a risk factor for other plugins Jerry might adopt."

**Gap:** This framing positions length as a concern that partially applies to Context7 (not now, but maybe later). This dilutes the clarity of the section's purpose.

**Strengthened Content:**

The tool name length analysis provides supporting evidence for the recommendation:

- Plugin-namespaced names for Context7: 49 chars and 42 chars (both safe)
- Manual-server-namespaced names: 36 chars and 29 chars (both safe, shorter)

Length is not a deciding factor for Context7. The recommendation to use manual user-scoped configuration is driven entirely by namespace correctness and subagent access -- not length. The length analysis confirms there is no downside to the plugin approach on this dimension; the decision is purely about the other two dimensions.

For future plugins Jerry might adopt: if the plugin name and server name are longer (e.g., a plugin named `my-enterprise-data-connector` with server name `enterprise-data`), the plugin naming pattern `mcp__plugin_my-enterprise-data-connector_enterprise-data__tool-name` would likely exceed 64 characters. This is a forward-looking architectural constraint, not a current concern for Context7.

**Rationale:** Reframing length as "not a factor for this decision" simplifies the recommendation's logic. The current framing creates unnecessary hedging.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-002 adds the verification procedure that was completely absent; SM-008 adds BUG-002 priority classification; SM-006 reduces redundancy in 5W1H section. The original had a significant actionability gap (recommendation without verification). |
| Internal Consistency | 0.20 | Positive | SM-004 resolves the logical tension where "length is a risk factor" framing partially undermined the recommendation; SM-007 resolves the HIGH/MEDIUM confidence inconsistency between Research Questions and Limitations sections. |
| Methodological Rigor | 0.20 | Positive | SM-005 removes speculative "timeline suggests" language, keeping the report within its evidentiary boundaries; SM-003 correctly calibrates confidence to MEDIUM where runtime verification was not performed. |
| Evidence Quality | 0.15 | Positive | SM-001 distinguishes two distinct runtime behaviors (benign dual-presence vs. Issue #15145 shadowing) that were conflated; SM-003 adds Issue #13898 scope assessment with correct confidence calibration. |
| Actionability | 0.15 | Positive (most significant) | SM-002 (Critical) converts the recommendation from aspirational to executable. The four-step verification procedure is the highest-value addition in this steelman. Without it, a developer cannot confirm the fix succeeded. |
| Traceability | 0.10 | Neutral | The original report already has strong traceability: 12 references with URL and key insight per reference, file paths with line numbers, 5 research questions with answers and confidence. No significant improvements needed. |

---

## Self-Review Note (H-15)

Pre-presentation self-review applied. Verified:

- All six S-003 execution protocol steps completed in order.
- Finding prefix `SM-NNN-s003-proj030-20260226` used consistently (execution_id = `s003-proj030-20260226`).
- Presentation vs. substance distinction maintained: all Critical/Major findings address substance gaps (missing verification procedure, unspecified runtime behavior, evidence calibration). Minor findings address presentation/framing.
- Steelman Reconstruction preserves the original thesis and core recommendation unchanged; additions are labeled with SM-NNN markers.
- SM-002 (Critical) is the highest-priority finding; it converts the recommendation from unverifiable to executable. Downstream S-002 Devil's Advocate should note that its absence means BUG-002 cannot be confirmed resolved.
- H-16 compliance: this S-003 report is produced before S-002 Devil's Advocate critique.
- Navigation table present (H-23); anchor links used (H-24).
- Template absence noted in Steelman Context section; protocol reconstructed from two prior execution reports and S-002 template cross-references. Finding prefix SM-NNN confirmed from prior executions. Execution proceeds per Step 1 validation logic (template contents reconstructed, not absent).

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 1
- **Major:** 3
- **Minor:** 4
- **Protocol Steps Completed:** 6 of 6 + Scoring Impact

---

*Steelman Report Version: 1.0.0*
*Strategy: S-003 Steelman Technique*
*SSOT: `.context/rules/quality-enforcement.md`*
*Execution Date: 2026-02-26*
*Executor: adv-executor agent v1.0.0*
*Template: `.context/templates/adversarial/s-003-steelman-technique.md` (reconstructed from prior executions -- file absent from worktree)*
