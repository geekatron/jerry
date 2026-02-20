# Adversarial Review: S-012 FMEA + S-013 Inversion
# Deliverable: `.context/rules/mcp-tool-standards.md`

> **Strategies:** S-012 (FMEA) + S-013 (Inversion Technique)
> **Deliverable:** `.context/rules/mcp-tool-standards.md` (97 lines)
> **Criticality:** C3 (AE-002: touches `.context/rules/`)
> **Executed By:** adv-executor
> **Date:** 2026-02-20
> **Source of Truth for Agent Matrix:** `TOOL_REGISTRY.yaml` + `AGENTS.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [S-012 FMEA Report](#s-012-fmea-report) | Failure modes, RPNs, mitigations |
| [S-012 Risk Priority Summary](#s-012-risk-priority-summary) | Ranked findings by RPN |
| [S-013 Inversion Report](#s-013-inversion-report) | Inversions and blind spots |
| [S-013 Severity Summary](#s-013-severity-summary) | Ranked inversion insights |
| [Cross-Strategy Synthesis](#cross-strategy-synthesis) | Convergent findings from both strategies |
| [Recommended Actions](#recommended-actions) | Prioritized remediation list |

---

## S-012 FMEA Report

> Failure Mode and Effects Analysis applied to all components of `mcp-tool-standards.md`.
> Scoring: **Severity** (impact if it fails), **Occurrence** (likelihood of failure), **Detection** (how detectable the failure is before runtime). RPN = S × O × D.

---

### FM-001

| Field | Value |
|-------|-------|
| **Component** | Canonical Tool Names — Context7 tool names |
| **Failure Mode** | Agents use `mcp__context7__resolve-library-id` per the rule file, but the tool is registered as `mcp__plugin_context7_context7__resolve-library-id` in `.claude/settings.local.json` |
| **Effect** | Tool calls fail silently or are rejected at the permission layer; Context7 protocol never executes; agent falls back to WebSearch without recognising the gap |
| **Evidence** | `.claude/settings.local.json` lines 27-29 register both `mcp__context7__*` AND `mcp__plugin_context7_context7__*`. The research report `EN-401-deep-research-enforcement-vectors/deliverable-001-claude-code-hooks-research.md:643` records `mcp__plugin_context7_context7__resolve-library-id -- Plugin variant was also denied`, confirming the name divergence is a live issue |
| **Severity** | 7 — Context7 protocol silently non-functional; WebSearch used instead (no data loss, but governance violated) |
| **Occurrence** | 5 — Dual registration in settings.local masks the issue partially but agent definitions reference only the short name |
| **Detection** | 7 — Failure is silent: agent receives permission denial or tool-not-found; no rule file validation catches mismatched canonical names |
| **RPN** | **245** |
| **Mitigation** | Add a note to the Canonical Tool Names section documenting both the short form (`mcp__context7__*`) and the plugin-prefixed form (`mcp__plugin_context7_context7__*`). Add a validation step to the quality gate for `mcp-tool-standards.md` that verifies canonical names appear in `settings.local.json`. |

---

### FM-002

| Field | Value |
|-------|-------|
| **Component** | Agent Integration Matrix — Completeness |
| **Failure Mode** | Matrix lists 13 agents but the full agent registry contains 33 agents (AGENTS.md). 20 agents are undocumented in the matrix, with no guidance on whether they MUST NOT use MCP tools or simply have no need. |
| **Effect** | New agents added to the framework have no explicit MCP access decision; developers default to either over-provisioning (capability creep) or under-provisioning (lost functionality). The "Not included (by design)" exclusion note covers only 9 named agents/families — leaving 4 documented agents unclassified: `nse-configuration`, `nse-integration`, `nse-qa`, `nse-reviewer`, `nse-verification`, `nse-risk`, `ps-validator`, `ps-reviewer`, `ps-reporter` (except the last is in the by-design note), and all `wt-*` agents beyond the generic wt-* wildcard. |
| **Evidence** | AGENTS.md lists 33 agents across 6 families. The matrix covers 13. The "Not included" footnote covers: adv-* (3), sb-* (implied, not in AGENTS.md), wt-* (3), ps-critic, ps-validator, ps-reporter = 8. That leaves 33 − 13 − 8 = 12 agents with no documented MCP stance. |
| **Severity** | 5 — Governance gap creates policy ambiguity; not an immediate operational failure |
| **Occurrence** | 8 — Every new agent addition recreates this ambiguity unless the matrix is actively maintained |
| **Detection** | 6 — No automated check exists to verify matrix coverage against AGENTS.md |
| **RPN** | **240** |
| **Mitigation** | Expand the "Not included (by design)" section into a full exclusion table listing every excluded agent by name with explicit rationale. Add a note stating the matrix is exhaustive and any agent not listed is excluded by design. Consider adding a linting rule that checks AGENTS.md agent count vs. matrix + exclusion list. |

---

### FM-003

| Field | Value |
|-------|-------|
| **Component** | Memory-Keeper Integration — Key Pattern specification |
| **Failure Mode** | The key pattern `jerry/{project}/{entity-type}/{entity-id}` is RECOMMENDED but the rule does not define allowed values for `{entity-type}`, nor does it specify whether `{project}` uses the full slug (`PROJ-001-oss-release`) or the short form (`PROJ-001`). The three examples use inconsistent formats: `feat028-mcp-20260220` (entity-id), `adversarial-strategies` (entity-id), `qg1-results` (entity-id) — no entity-type appears to follow a controlled vocabulary. |
| **Effect** | Memory-Keeper keys diverge across agents; `search` operations return incomplete results; cross-agent retrieval fails because `orch-synthesizer` cannot predict the key format written by `orch-tracker` |
| **Evidence** | The examples show `orchestration`, `research`, and `phase-boundary` as entity-types with no formal enumeration. TOOL_REGISTRY.yaml line 251 repeats the same unformalized pattern without vocabulary constraints. |
| **Severity** | 6 — Cross-agent retrieval breaks; cross-pipeline synthesis (the primary use case for `orch-synthesizer`) degrades |
| **Occurrence** | 7 — Without a controlled vocabulary, key format divergence is expected across agents and sessions |
| **Detection** | 5 — Key mismatches produce silent `null` returns from `retrieve`; agents may proceed without prior context rather than erroring |
| **RPN** | **210** |
| **Mitigation** | Add a controlled vocabulary table for `{entity-type}` values (e.g., `orchestration`, `research`, `phase-boundary`, `requirements`, `decision`, `session`). Specify whether `{project}` uses full slug or short ID. Mark the key pattern as REQUIRED (HARD tier) rather than implicitly informational. |

---

### FM-004

| Field | Value |
|-------|-------|
| **Component** | Context7 Integration — "Maximum 3 calls per question" limit |
| **Failure Mode** | The 3-call limit applies to both `resolve-library-id` + `query-docs` combined, but the rule is ambiguous: does a multi-library research task (e.g., comparing three SDKs) count as one question (3 calls total) or three questions (9 calls total)? |
| **Effect** | Agents researching multi-library topics either (a) arbitrarily truncate research at 3 total calls, missing coverage, or (b) treat each library as a new question and make unlimited calls — defeating the limit's intent |
| **Evidence** | The rule states "Maximum 3 calls per question" with no definition of "question". TOOL_REGISTRY.yaml lines 228, 240 repeat the same limit without elaboration. The Claude Code system prompt for Context7 states "Do not call this tool more than 3 times per question" — aligning with the registry but providing no clarification on multi-library scenarios. |
| **Severity** | 4 — Research quality degradation or token waste, no governance violation |
| **Occurrence** | 6 — Multi-library research tasks are common for ps-researcher and nse-explorer |
| **Detection** | 8 — No enforcement mechanism counts calls per question; all detection is behavioural/cognitive |
| **RPN** | **192** |
| **Mitigation** | Define "question" as "a single library/framework research objective". Clarify that multi-library tasks permit 3 calls per library. Add a note: "If the resolved ID is wrong after 3 calls, use the best available result." |

---

### FM-005

| Field | Value |
|-------|-------|
| **Component** | L2-REINJECT directive |
| **Failure Mode** | The L2-REINJECT comment at line 5 has rank=9 and tokens=40. The quality-enforcement.md L2-REINJECT comments have ranks 1-8. No rule in the framework defines what rank=9 means operationally, nor is there a maximum rank limit documented. |
| **Effect** | If the L2 re-injection system loads rules in rank order, rank=9 is injected last with lowest priority. If context is full, this rule may be truncated. The 40-token summary omits "Memory-Keeper is REQUIRED at orchestration phase boundaries" in compressed form, reducing to "Memory-Keeper REQUIRED at orchestration phase boundaries" — the loss of "is" is cosmetic but "Context7 REQUIRED for library/framework research" could be mistakenly applied to first-party libraries. |
| **Evidence** | quality-enforcement.md uses ranks 1, 2, 3, 4, 5, 6, 8 — rank 7 and 9 are unoccupied. No specification document defines the rank scale ceiling. |
| **Severity** | 4 — Potential context-rot vulnerability for this rule under heavy context load |
| **Occurrence** | 3 — Context rot at rank 9 only occurs in very long sessions |
| **Detection** | 9 — Invisible: when context is full, truncation of low-rank injections is undetectable by the agent |
| **RPN** | **108** |
| **Mitigation** | Document the rank scale (1 = highest priority, N = lowest) in quality-enforcement.md or a new L2-REINJECT spec. Consider raising this rule to rank 7 (the unused slot) to increase its priority. Expand the 40-token summary to explicitly exclude "first-party libraries" from the Context7 trigger. |

---

### FM-006

| Field | Value |
|-------|-------|
| **Component** | Memory-Keeper Integration — Trigger table: "Session resume" event |
| **Failure Mode** | The trigger "Session resume → Search for prior context" is assigned to no specific agent; it is a session-level event. However, no agent in the matrix is defined as the session-resume handler. The orch-planner performs planning, orch-tracker tracks state — but neither is designated as the session-resume agent. |
| **Effect** | When resuming a multi-session workflow, no agent is explicitly responsible for executing the `search` trigger; context from prior sessions may be silently omitted |
| **Evidence** | Agent matrix shows orch-planner and orch-tracker both have `retrieve, search` but neither's rationale mentions session resume. AGENTS.md describes orch-tracker as "state tracking, checkpoint creation" and orch-planner as "workflow design, pipeline architecture" — neither mentions session resume as a primary responsibility. |
| **Severity** | 5 — Session context loss degrades multi-session orchestration quality |
| **Occurrence** | 6 — Every resumed orchestration session triggers this gap |
| **Detection** | 7 — The absence of prior context retrieval is invisible to the agent unless it knows what it missed |
| **RPN** | **210** |
| **Mitigation** | Assign session-resume responsibility explicitly to orch-planner (as the first agent invoked in a new session). Add a note: "Session resume is the responsibility of the invoking orchestrator; orch-planner MUST execute a search before designing a new pipeline." |

---

### FM-007

| Field | Value |
|-------|-------|
| **Component** | Context7 Integration — Trigger definition |
| **Failure Mode** | The trigger "Any agent task involving external library/framework documentation lookup" is defined informally. The rule does not specify what constitutes an "external" library — whether first-party internal packages (e.g., the Jerry framework's own Python package published to PyPI) qualify as external. |
| **Effect** | Agents may or may not use Context7 for internal packages published publicly; inconsistent behaviour across agents for the same library type |
| **Severity** | 3 — Minor inconsistency; WebSearch is an adequate fallback |
| **Occurrence** | 4 — Ambiguity surfaces when Jerry is published to PyPI (PROJ-001 intent) |
| **Detection** | 8 — No detection mechanism |
| **RPN** | **96** |
| **Mitigation** | Add a clarification: "External = not in the current git repository. Self-hosted packages published to PyPI or npm ARE external for Context7 purposes." |

---

### FM-008

| Field | Value |
|-------|-------|
| **Component** | Agent Integration Matrix — orch-synthesizer Memory-Keeper access |
| **Failure Mode** | orch-synthesizer has `retrieve, search` but NOT `store`. If a synthesis produces a reusable cross-pipeline insight, the agent cannot persist it. The rationale "Cross-pipeline context retrieval" is retrieve-only, but synthesis tasks inherently produce new artifacts that should be persisted. |
| **Evidence** | TOOL_REGISTRY.yaml lines 673-676 confirm orch-synthesizer only has `mcp__memory-keeper__retrieve` and `mcp__memory-keeper__search`. AGENTS.md line 252 confirms the same. |
| **Severity** | 4 — Synthesis outputs lost across sessions; re-derivation cost |
| **Occurrence** | 5 — Every cross-pipeline synthesis that produces novel insight hits this gap |
| **Detection** | 6 — Agent will write synthesis to filesystem (P-002) but cannot persist to Memory-Keeper |
| **RPN** | **120** |
| **Mitigation** | Add `store` to orch-synthesizer's Memory-Keeper access. Update the rationale to "Cross-pipeline context retrieval + synthesis persistence". Update TOOL_REGISTRY.yaml accordingly. |

---

### FM-009

| Field | Value |
|-------|-------|
| **Component** | Context7 Integration — Scenario table completeness |
| **Failure Mode** | The scenario table covers 5 scenarios (Library API docs, Framework patterns, SDK usage, General concepts, Codebase-internal). Missing scenarios: (a) version-specific documentation where the library is known but the version matters, (b) deprecated library lookup where Context7 may have stale data. |
| **Effect** | Agents may query Context7 for deprecated versions and receive outdated information without realising Context7 coverage is version-dependent |
| **Severity** | 4 — Incorrect implementation guidance could be used if Context7's version coverage is incomplete |
| **Occurrence** | 3 — Only when working with versioned APIs or deprecated SDKs |
| **Detection** | 7 — Context7 response may not indicate coverage gaps |
| **RPN** | **84** |
| **Mitigation** | Add rows to the scenario table: "Version-specific docs: Use Context7 with version suffix in query; verify returned doc version matches target." and "Deprecated library: Use WebSearch to verify currency of Context7 results." |

---

### FM-010

| Field | Value |
|-------|-------|
| **Component** | Memory-Keeper Integration — Store action: value content guidance |
| **Failure Mode** | The rule specifies WHAT to store (phase summary, artifacts, key findings) but not HOW — specifically, whether to store full artifact text or summary references. TOOL_REGISTRY.yaml line 252 adds the constraint "Value should be concise summary, not full artifact content" but this constraint is absent from `mcp-tool-standards.md`. |
| **Effect** | Agents store full artifact content in Memory-Keeper (e.g., a 5,000-token synthesis report), bloating the memory store and potentially hitting Memory-Keeper storage limits |
| **Evidence** | TOOL_REGISTRY.yaml line 252: "Value should be concise summary, not full artifact content" — this constraint exists in the registry but not in the governance rule file that agents load via L1. |
| **Severity** | 5 — Storage bloat; cross-session search degrades as large values dominate results |
| **Occurrence** | 6 — Without explicit guidance, full-content storage is the intuitive choice |
| **Detection** | 7 — No runtime enforcement; Memory-Keeper accepts any value |
| **RPN** | **210** |
| **Mitigation** | Add a "Storage Guidance" note to the Memory-Keeper Integration section: "Store concise summaries (< 500 tokens), not full artifact content. Reference full artifacts by filesystem path. Full content storage bloats the memory store and degrades search quality." |

---

## S-012 Risk Priority Summary

| Rank | ID | Component | RPN | Primary Risk |
|------|----|-----------|-----|--------------|
| 1 | FM-001 | Canonical tool names — Context7 name mismatch | 245 | Silent tool call failure |
| 2 | FM-002 | Agent matrix — 20 agents undocumented | 240 | Policy ambiguity at framework scale |
| 3 | FM-003 | Memory-Keeper key pattern — no controlled vocabulary | 210 | Cross-agent retrieval failure |
| 3 | FM-006 | Memory-Keeper triggers — session resume unassigned | 210 | Session context loss |
| 3 | FM-010 | Memory-Keeper store — value size guidance absent | 210 | Storage bloat |
| 6 | FM-004 | Context7 3-call limit — "question" undefined | 192 | Research truncation or limit bypass |
| 7 | FM-008 | orch-synthesizer — store access missing | 120 | Synthesis outputs not persisted |
| 8 | FM-005 | L2-REINJECT rank=9 — no rank spec | 108 | Context-rot vulnerability |
| 9 | FM-007 | Context7 trigger — "external" undefined | 96 | Inconsistent first-party behaviour |
| 10 | FM-009 | Context7 scenario table — version/deprecated missing | 84 | Outdated doc risk |

**Critical threshold (RPN >= 200): FM-001, FM-002, FM-003, FM-006, FM-010**
**High threshold (RPN 100-199): FM-004, FM-008, FM-005**

---

## S-013 Inversion Report

> For each key claim in the document, the opposite is posited and evaluated for the insight it yields.

---

### INV-001

| Field | Value |
|-------|-------|
| **ID** | INV-001 |
| **Original Claim** | "Context7 is REQUIRED when researching any external library, framework, SDK, or API documentation." |
| **Inversion** | Context7 is NEVER required; WebSearch is always sufficient for external library research. |
| **Analysis** | If WebSearch were always sufficient: (a) agents already use WebSearch and are productive without Context7; (b) Context7 adds a mandatory two-step protocol (resolve then query) versus a single WebSearch call; (c) Context7 has coverage gaps — not all libraries are indexed, and the 3-call limit means a failed resolve leaves the agent worse off than if it had gone straight to WebSearch. The inversion reveals that REQUIRED is too strong for the general case. The real constraint is: Context7 SHOULD be attempted first for well-known libraries, with WebSearch as the fallback, not the other way around. The rule creates a compliance burden without a grace condition for Context7 coverage gaps. |
| **Blind Spot Exposed** | There is no graceful degradation clause. What should an agent do when `resolve-library-id` returns zero matches? The rule says "use WebSearch only for general concepts or when Context7 has no coverage" — but detecting "no coverage" requires a failed resolve call, and that failed call counts against the 3-call limit. The rule does not specify how to handle the resolve-failed state. |
| **Severity** | Major |
| **Recommendation** | Rewrite as: "Context7 SHOULD be the first attempt for well-known external libraries. If `resolve-library-id` returns no results or low-confidence results, fall back to WebSearch immediately. A failed resolve call DOES NOT count against the 3-call limit for the substantive query." |

---

### INV-002

| Field | Value |
|-------|-------|
| **ID** | INV-002 |
| **Original Claim** | "Memory-Keeper is REQUIRED at orchestration phase boundaries." |
| **Inversion** | Memory-Keeper is never required at phase boundaries; filesystem persistence (P-002) is sufficient for cross-phase context. |
| **Analysis** | The filesystem already provides WORKTRACKER.md, ORCHESTRATION.yaml, and phase artifact files. These are persistent, human-readable, version-controlled, and accessible to all agents without a tool call. Memory-Keeper provides cross-session semantic search — a capability the filesystem does not have. The inversion reveals the rule conflates two distinct needs: (a) cross-phase artifact handoff (filesystem is adequate) and (b) cross-session context retrieval (Memory-Keeper is genuinely valuable). By marking the entire class as REQUIRED, the rule creates unnecessary tool calls in single-session orchestrations where filesystem state is fully sufficient. Additionally, if Memory-Keeper is unavailable (not installed, API failure), the REQUIRED designation blocks orchestration with no documented fallback. |
| **Blind Spot Exposed** | The rule has no availability condition. Memory-Keeper is an external MCP dependency that can be absent. The rule needs a fallback: "If Memory-Keeper is unavailable, filesystem artifacts serve as the phase boundary record." The distinction between single-session (filesystem sufficient) and multi-session (Memory-Keeper adds value) is absent. |
| **Severity** | Major |
| **Recommendation** | Differentiate the rule: "Memory-Keeper store is REQUIRED for multi-session orchestration phase boundaries. For single-session orchestrations, filesystem artifacts (ORCHESTRATION.yaml) are sufficient. If Memory-Keeper is unavailable, filesystem artifacts serve as the mandatory fallback. Memory-Keeper MUST NOT be a single point of failure for orchestration." |

---

### INV-003

| Field | Value |
|-------|-------|
| **ID** | INV-003 |
| **Original Claim** | "Key Pattern: `jerry/{project}/{entity-type}/{entity-id}`" |
| **Inversion** | No key pattern is required; agents should use ad-hoc keys that make sense in context. |
| **Analysis** | Without a key pattern, cross-agent retrieval is impossible — agents cannot search or retrieve results produced by other agents. The key pattern is necessary. However, the inversion exercise reveals the pattern is under-specified rather than unnecessary: it specifies structure but not vocabulary. If `orch-planner` stores as `jerry/PROJ-001/orchestration/plan-001` and `orch-tracker` stores as `jerry/PROJ-001/phase-state/phase-1`, `orch-synthesizer` cannot predict either key for direct retrieval (it can search, but search requires knowing there IS something to search for). The pattern creates an illusion of structure without enforcing interoperability. |
| **Blind Spot Exposed** | The key pattern assumes agents will store keys in a centralised registry or that the key structure is self-discoverable via search. Neither is true. There is no mechanism for one agent to discover what keys another agent has created. The only recovery path is `search` — which requires semantic query construction. The pattern should be paired with a requirement to log stored keys in ORCHESTRATION.yaml or WORKTRACKER.md so agents can retrieve by known key rather than searching. |
| **Severity** | Major |
| **Recommendation** | Add a requirement: "After every `store` call, record the key and a one-line description in ORCHESTRATION.yaml under a `memory_keeper_keys` section. This creates a human-readable index that orch-planner can load to construct exact retrieval keys." Define controlled vocabulary for `{entity-type}` with at least 6 canonical values. |

---

### INV-004

| Field | Value |
|-------|-------|
| **ID** | INV-004 |
| **Original Claim** | The explicit agent exclusions (adv-*, sb-*, wt-*, ps-critic, ps-validator, ps-reporter) are correct and complete. |
| **Inversion** | The exclusions are wrong: at least some excluded agents should have MCP access, and at least one included agent should be excluded. |
| **Analysis** | Testing the exclusions: (a) **adv-executor**: excluded because "self-contained strategy execution" — but adv-executor applies strategies like S-001 Red Team and S-004 Pre-Mortem that may benefit from researching known failure modes of the library/framework under review. Context7 access for adv-executor researching security vulnerabilities in a third-party dependency could meaningfully improve strategy execution quality. The exclusion is defensible but not obviously correct. (b) **ps-validator**: excluded because "quality evaluation" — but validation of API integration requires checking against current API documentation, which is exactly the Context7 use case. The exclusion creates a gap: ps-validator validates implementations but cannot consult the docs the implementation claims to follow. (c) **ps-synthesizer** is included with Context7 access but only `resolve, query` — no Memory-Keeper. However, synthesis across multiple research sessions is precisely the multi-session persistence use case Memory-Keeper is designed for. The inclusion of ps-synthesizer in Context7 but exclusion from Memory-Keeper is internally inconsistent with the stated Memory-Keeper rationale. |
| **Blind Spot Exposed** | The matrix was constructed by analogy from the problem-solving skill's existing Context7 agents rather than from a systematic analysis of each agent's workflow. The exclusion rationale "quality evaluation" for ps-validator ignores that quality evaluation against external standards requires doc lookup. The exclusion rationale for ps-synthesizer's Memory-Keeper access was simply not considered. |
| **Severity** | Major |
| **Recommendation** | Review three specific cases: (1) Add Memory-Keeper `store, retrieve, search` to ps-synthesizer — multi-session synthesis is a primary Memory-Keeper use case. (2) Evaluate adding Context7 `resolve, query` to ps-validator for API compliance validation tasks. (3) Document the decision not to grant adv-executor Context7 access with an explicit rationale (e.g., "strategy execution is document-scoped; web research during execution would pollute the adversarial perspective"). |

---

### INV-005

| Field | Value |
|-------|-------|
| **ID** | INV-005 |
| **Original Claim** | "Maximum 3 calls per question; use best result after limit." |
| **Inversion** | There is no maximum call limit; agents should make as many Context7 calls as needed for thorough research. |
| **Analysis** | Removing the limit exposes why it exists: unconstrained Context7 calls create cost and context window inflation. A deep library research task with no limit could consume 20+ calls before the agent determines nothing useful is available. The limit is correct in intent. However, the inversion reveals that the "use best result after limit" instruction is brittle: if all 3 calls returned nothing useful (e.g., the library is not in Context7), "use best result" means "use nothing" — but the rule does not explicitly permit the agent to fall back to WebSearch after limit exhaustion in the library-research scenario. The rule only permits WebSearch "when Context7 has no coverage" but does not define how an agent determines that coverage is absent without exhausting the call limit. This creates a circular dependency: you cannot know coverage is absent without spending calls to find out. |
| **Blind Spot Exposed** | The 3-call limit and the "no coverage" fallback trigger are in tension. An agent that exhausts 3 calls on resolve attempts for a niche library has no documented path to WebSearch because it did not receive a formal "no coverage" signal — it just got poor matches. The rule needs an explicit "limit exhausted with no useful result" fallback clause. |
| **Severity** | Minor |
| **Recommendation** | Add: "If all 3 calls are exhausted without a useful result, treat this as 'no coverage' and proceed with WebSearch. Document the exhaustion in a comment or log entry." |

---

### INV-006

| Field | Value |
|-------|-------|
| **ID** | INV-006 |
| **Original Claim** | "Canonical Tool Names" section is the authoritative source for MCP tool identifiers used in agent definitions and TOOL_REGISTRY.yaml. |
| **Inversion** | `TOOL_REGISTRY.yaml` is the true authoritative source; `mcp-tool-standards.md` is a summary that can drift from the registry. |
| **Analysis** | The claim that the rule file is authoritative creates a dual-SSOT problem. TOOL_REGISTRY.yaml's header states: "Single Source of Truth for tool definitions and agent permissions" (line 5). The rule file also claims authority over canonical names. If these two sources diverge — as demonstrated by FM-001's tool name discrepancy — there is no tie-breaking rule. Agent definitions that read both sources will have no resolution strategy. The rule file is loaded at L1 (session start) and re-injected at L2, giving it higher operational priority than TOOL_REGISTRY.yaml. Yet TOOL_REGISTRY.yaml was designed as the SSOT. This inversion reveals an architectural conflict in the framework's information hierarchy. |
| **Blind Spot Exposed** | The framework has at minimum three competing claims to "authoritative" status for MCP tool names: (1) `mcp-tool-standards.md` (via the Canonical Tool Names section header), (2) `TOOL_REGISTRY.yaml` (via its header comment), and (3) `.claude/settings.local.json` (the actual enforcement layer). None of these documents reference each other for name resolution. The real authority is settings.local.json because it is the only file the runtime actually checks. |
| **Severity** | Critical |
| **Recommendation** | Establish a single SSOT for canonical tool names: TOOL_REGISTRY.yaml. Update `mcp-tool-standards.md` to read: "Canonical tool names are defined in `TOOL_REGISTRY.yaml` (SSOT). This table is a convenience reference; TOOL_REGISTRY.yaml takes precedence on any discrepancy." Add a note: "Runtime authority is `.claude/settings.local.json`; both the rule file and registry must match it." |

---

## S-013 Severity Summary

| Rank | ID | Original Claim | Severity | Core Blind Spot |
|------|----|----------------|----------|-----------------|
| 1 | INV-006 | Canonical names section is authoritative | Critical | Three-way SSOT conflict; runtime authority is settings.local.json |
| 2 | INV-001 | Context7 REQUIRED for all external library research | Major | No graceful degradation for resolve-failed state |
| 2 | INV-002 | Memory-Keeper REQUIRED at phase boundaries | Major | No single-session exception; no availability fallback |
| 2 | INV-003 | Key pattern is sufficient for interoperability | Major | No key registry; cross-agent retrieval relies on unpredictable search |
| 2 | INV-004 | Exclusions are correct and complete | Major | ps-synthesizer missing Memory-Keeper; ps-validator needs Context7 |
| 6 | INV-005 | 3-call limit with "use best result" | Minor | Limit-exhausted fallback not explicitly permitted |

---

## Cross-Strategy Synthesis

> Convergent findings: failure modes that both S-012 and S-013 independently surface.

| Finding | FMEA ID | Inversion ID | Convergent Insight |
|---------|---------|--------------|-------------------|
| Canonical name authority conflict | FM-001 | INV-006 | Three sources claim authority; runtime (settings.local.json) is the actual arbiter. The rule file and registry must explicitly defer to it. |
| Memory-Keeper operational conditions | FM-006, FM-010 | INV-002 | The REQUIRED designation has no availability fallback and no session-type qualifier. Single-session orchestrations pay unnecessary costs. |
| Agent matrix incompleteness | FM-002 | INV-004 | 20 agents lack MCP stance; specific omissions (ps-synthesizer, ps-validator) are analytically incorrect, not just undocumented. |
| Context7 fallback logic | FM-004 | INV-001, INV-005 | The relationship between the 3-call limit, the "no coverage" fallback, and the REQUIRED mandate creates a circular dependency that leaves agents in an undefined state after limit exhaustion with poor results. |
| Key pattern operationability | FM-003 | INV-003 | The key pattern specifies structure without enforcing vocabulary or discoverability, making cross-agent retrieval dependent on semantic search guessing. |

---

## Recommended Actions

> Prioritised by convergence (both strategies flagged) and RPN/severity.

| Priority | Action | Source | Impact |
|----------|--------|--------|--------|
| P1-CRITICAL | Resolve three-way SSOT conflict for canonical tool names. Declare `TOOL_REGISTRY.yaml` as SSOT; make `mcp-tool-standards.md` a reference that defers to it. Document both short-form and plugin-form Context7 names. | FM-001, INV-006 | Prevents silent tool-call failures across 7 Context7 agents |
| P2-HIGH | Define Memory-Keeper REQUIRED condition: multi-session only. Add single-session exception. Add availability fallback clause. | FM-006, INV-002 | Removes unnecessary tool calls in single-session work; prevents orchestration blocking if Memory-Keeper unavailable |
| P3-HIGH | Add controlled vocabulary for `{entity-type}` in key pattern. Add requirement to log stored keys in ORCHESTRATION.yaml. | FM-003, INV-003 | Enables reliable cross-agent key retrieval; prevents silent context loss |
| P4-HIGH | Expand agent matrix to cover all 33 agents. Add `store` to orch-synthesizer. Add Memory-Keeper to ps-synthesizer. Document ps-validator Context7 decision explicitly. | FM-002, INV-004 | Closes policy gaps; removes 12 undocumented agents |
| P5-HIGH | Add storage content guidance to Memory-Keeper section: summaries only, < 500 tokens, reference filesystem paths for full artifacts. | FM-010 | Prevents storage bloat; improves search quality |
| P6-MEDIUM | Add explicit fallback for Context7 limit exhaustion: "Treat as no coverage; proceed with WebSearch; do not block on limit." | FM-004, INV-001, INV-005 | Resolves circular dependency in Context7 fallback logic |
| P7-MEDIUM | Assign session-resume ownership to orch-planner. Add to rationale column and Memory-Keeper Integration triggers table. | FM-006 | Ensures prior session context is always retrieved at workflow start |
| P8-LOW | Raise L2-REINJECT rank from 9 to 7. Document rank scale in quality-enforcement.md. | FM-005 | Reduces context-rot vulnerability for this rule |
| P9-LOW | Add definition of "external" to Context7 trigger (external = not in current git repo; PyPI-published packages count as external). | FM-007 | Consistent behaviour for self-hosted public packages |
| P10-LOW | Add scenario rows to Context7 table for version-specific docs and deprecated library lookup. | FM-009 | Prevents use of stale documentation for versioned APIs |
