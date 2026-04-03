# Web Tool Permission Audit Report

> **Analysis Type:** Gap Analysis
> **PS ID:** STORY-012
> **Entry ID:** e-001
> **Analyst:** ps-analyst
> **Date:** 2026-03-28
> **Trigger:** GitHub #217 (adv-executor hallucinated acquisition figure during C4 tournament due to missing WebSearch/WebFetch)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language findings and recommendations |
| [L1: Technical Analysis](#l1-technical-analysis) | Evidence-based per-agent analysis |
| [L2: Architectural Implications](#l2-architectural-implications) | Systemic patterns and strategic observations |
| [Summary Recommendation Table](#summary-recommendation-table) | Per-agent ADD/KEEP/REMOVE/ASSESS decisions |
| [Gap Analysis](#gap-analysis) | Agents that should have web tools but don't |
| [Over-Privilege Analysis](#over-privilege-analysis) | Agents that have web tools but may not need them |
| [mcp-tool-standards.md Drift](#mcp-tool-standardsmd-drift) | Matrix vs actual declaration mismatches |
| [Skill vs Agent Misalignment](#skill-vs-agent-misalignment) | SKILL.md allowed-tools vs agent frontmatter gaps |
| [Priority-Ordered Action Items](#priority-ordered-action-items) | What to fix and in what order |
| [Evidence Summary](#evidence-summary) | All cited evidence |

---

## L0: Executive Summary

The audit covers 89 agent definitions and 21 SKILL.md files. The triggering incident (GitHub #217) was adv-executor hallucinating a $3.4B acquisition figure when the verified amount is $25B -- a direct consequence of the agent having no mechanism to verify factual claims against live sources.

The audit finds that the problem is not isolated. Three categories of issue exist:

**Missing web tools (ADD):** Five agents are demonstrably under-privileged relative to their declared tool tier or methodology. The most urgent is adv-executor, confirmed by STORY-011 and #217. adv-scorer is in the same family and warrants the same fix. diataxis-explanation has a divergent cognitive mode -- the mode that the agent-development-standards explicitly assigns T3 -- but is declared T2 with no web access. nse-reporter has a T3 governance tier but is missing WebSearch, having only WebFetch. Three UX agents (ux-behavior-diagnostician, ux-heart-analyst, ux-kano-analyst) are declared T2 but operate within a T3 skill family; their peer agents all have web tools.

**Governance tier mismatches (ASSESS):** nse-qa is declared T3 in governance but lacks web tools in its frontmatter, matching its T2-level tool set. The governance YAML says T3, the tools say T2. One of these is wrong. Similarly, orch-planner/synthesizer/tracker are T4 in governance but their SKILL.md lists WebSearch/WebFetch in allowed-tools while the individual agents do not have them.

**Matrix drift:** The mcp-tool-standards.md Agent Integration Matrix has not been updated to reflect 14 agents that appear in the actual codebase with Context7 access but are absent from the matrix (all 6 UX sub-skill agents with web/Context7, and eng-reviewer which is explicitly listed as "not included by design" yet has `mcpServers: context7: true` in its frontmatter).

The recommended action plan: fix adv-executor and adv-scorer immediately (they have a confirmed incident), then address the three UX T2 outliers, then reconcile nse-reporter, then update the matrix to reflect reality.

---

## L1: Technical Analysis

### Analysis Method: Gap Analysis

Framework: Current-State vs Target-State comparison using T1-T5 tier model (agent-development-standards.md) and Cognitive Mode Taxonomy as the normative reference.

**Evidence sources used:**
- All 89 agent `tools:` frontmatter fields (verified by direct file scan)
- All 89 `.governance.yaml` `tool_tier` and `cognitive_mode` fields
- `mcp-tool-standards.md` Agent Integration Matrix
- `agent-development-standards.md` T1-T5 tier definitions and cognitive mode-to-tier mapping
- STORY-011 (adv-executor incident documentation)
- `skills/*/SKILL.md` `allowed-tools` frontmatter fields

### Tier Model Reference

From `agent-development-standards.md`:

| Tier | Tools Included | When to Use |
|------|---------------|-------------|
| T1 | Read, Glob, Grep | Evaluation, auditing, scoring, validation |
| T2 | T1 + Write, Edit, Bash | Analysis, document production, code generation |
| T3 | T2 + WebSearch, WebFetch, Context7 | Research, exploration, external documentation |
| T4 | T2 + Memory-Keeper | Cross-session state management |
| T5 | T3 + T4 + Agent | Orchestration with delegation |

Cognitive mode-to-tier implication (from cognitive mode taxonomy): **divergent agents should be T3+** (they need external access for breadth-first research). **systematic and convergent agents** typically operate at T1-T2.

---

## Summary Recommendation Table

| Agent | Skill | Has WebSearch | Has WebFetch | Has Context7 | Gov Tier | Cognitive Mode | Recommendation | Priority |
|-------|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| adv-executor | adversary | No | No | No | T2 | convergent | **ADD Web+C7** | P0 |
| adv-scorer | adversary | No | No | No | T2 | convergent | **ADD Web+C7** | P1 |
| adv-selector | adversary | No | No | No | T2 | convergent | KEEP | - |
| diataxis-explanation | diataxis | No | No | No | T2 | divergent | **ADD Web** | P2 |
| diataxis-howto | diataxis | No | No | No | T2 | systematic | KEEP | - |
| diataxis-reference | diataxis | No | No | No | T2 | systematic | KEEP | - |
| diataxis-tutorial | diataxis | No | No | No | T2 | systematic | KEEP | - |
| diataxis-auditor | diataxis | No | No | No | T1 | systematic | KEEP | - |
| diataxis-classifier | diataxis | No | No | No | T1 | convergent | KEEP | - |
| cd-generator | contract-design | No | No | No | T2 | systematic | KEEP | - |
| cd-validator | contract-design | No | No | No | T2 | systematic | KEEP | - |
| orch-planner | orchestration | No | No | No | T4 | convergent | **ASSESS** | P3 |
| orch-synthesizer | orchestration | No | No | No | T4 | convergent | **ASSESS** | P3 |
| orch-tracker | orchestration | No | No | No | T4 | convergent | KEEP | - |
| ps-critic | problem-solving | No | No | No | T2 | convergent | KEEP | - |
| ps-reporter | problem-solving | No | No | No | T2 | convergent | KEEP | - |
| ps-reviewer | problem-solving | No | No | No | T2 | convergent | KEEP | - |
| ps-validator | problem-solving | No | No | No | T2 | systematic | KEEP | - |
| pe-builder | prompt-engineering | No | No | No | T2 | systematic | KEEP | - |
| pe-constraint-gen | prompt-engineering | No | No | No | T2 | systematic | KEEP | - |
| pe-scorer | prompt-engineering | No | No | No | T1 | systematic | KEEP | - |
| sb-voice | saucer-boy | No | No | No | T1 | divergent | KEEP | - |
| sb-calibrator | saucer-boy-fw-voice | No | No | No | T2 | systematic | KEEP | - |
| sb-reviewer | saucer-boy-fw-voice | No | No | No | T2 | convergent | KEEP | - |
| sb-rewriter | saucer-boy-fw-voice | No | No | No | T2 | systematic | KEEP | - |
| tspec-analyst | test-spec | No | No | No | T2 | systematic | KEEP | - |
| tspec-generator | test-spec | No | No | No | T2 | systematic | KEEP | - |
| ts-extractor | transcript | No | No | No | T4 | systematic | KEEP | - |
| ts-formatter | transcript | No | No | No | T2 | systematic | KEEP | - |
| ts-mindmap-ascii | transcript | No | No | No | T2 | systematic | KEEP | - |
| ts-mindmap-mermaid | transcript | No | No | No | T2 | systematic | KEEP | - |
| ts-parser | transcript | No | No | No | T4 | systematic | KEEP | - |
| uc-author | use-case | No | No | No | T2 | integrative | KEEP | - |
| uc-slicer | use-case | No | No | No | T2 | systematic | KEEP | - |
| ux-behavior-diagnostician | ux-behavior-design | No | No | No | T2 | convergent | **ASSESS** | P2 |
| ux-heart-analyst | ux-heart-metrics | No | No | No | T2 | systematic | **ASSESS** | P2 |
| ux-kano-analyst | ux-kano-model | No | No | No | T2 | convergent | **ASSESS** | P2 |
| nse-qa | nasa-se | No | No | No | T2 | convergent | KEEP | - |
| nse-reporter | nasa-se | No | Yes | No | T3 | convergent | **ADD WebSearch** | P2 |
| wt-auditor | worktracker | No | No | No | T2 | systematic | KEEP | - |
| wt-verifier | worktracker | No | No | No | T2 | systematic | KEEP | - |
| wt-visualizer | worktracker | No | No | No | T2 | systematic | KEEP | - |
| eng-architect | eng-team | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| eng-backend | eng-team | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| eng-devsecops | eng-team | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| eng-frontend | eng-team | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| eng-incident | eng-team | Yes | Yes | Yes | T3 | divergent | KEEP | - |
| eng-infra | eng-team | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| eng-lead | eng-team | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| eng-qa | eng-team | Yes | Yes | Yes | T3 | systematic | **ASSESS** | P3 |
| eng-reviewer | eng-team | Yes | Yes | Yes | T3 | convergent | **ASSESS** | P3 |
| eng-security | eng-team | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| nse-architecture | nasa-se | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| nse-configuration | nasa-se | Yes | Yes | No | T3 | convergent | KEEP | - |
| nse-explorer | nasa-se | Yes | Yes | Yes | T3 | divergent | KEEP | - |
| nse-integration | nasa-se | Yes | Yes | No | T3 | convergent | KEEP | - |
| nse-requirements | nasa-se | Yes | Yes | No | T4 | systematic | KEEP | - |
| nse-reviewer | nasa-se | Yes | Yes | No | T3 | convergent | KEEP | - |
| nse-risk | nasa-se | Yes | Yes | No | T3 | convergent | KEEP | - |
| nse-verification | nasa-se | Yes | Yes | No | T3 | systematic | KEEP | - |
| ps-researcher | problem-solving | Yes | Yes | Yes | T3 | divergent | KEEP | - |
| ps-analyst | problem-solving | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| ps-architect | problem-solving | Yes | Yes | Yes | T4 | convergent | KEEP | - |
| ps-investigator | problem-solving | Yes | Yes | Yes | T3 | forensic | KEEP | - |
| ps-synthesizer | problem-solving | Yes | Yes | Yes | T3 | integrative | KEEP | - |
| pm-business-analyst | pm-pmm | Yes | Yes | No | T3 | convergent | KEEP | - |
| pm-competitive-analyst | pm-pmm | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| pm-customer-insight | pm-pmm | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| pm-market-strategist | pm-pmm | Yes | Yes | Yes | T3 | divergent | KEEP | - |
| pm-product-strategist | pm-pmm | Yes | Yes | No | T3 | convergent | KEEP | - |
| red-lead | red-team | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| red-recon | red-team | Yes | Yes | Yes | T3 | divergent | KEEP | - |
| red-vuln | red-team | Yes | Yes | Yes | T3 | forensic | KEEP | - |
| red-exploit | red-team | Yes | Yes | Yes | T3 | forensic | KEEP | - |
| red-privesc | red-team | Yes | Yes | Yes | T3 | forensic | KEEP | - |
| red-lateral | red-team | Yes | Yes | Yes | T3 | forensic | KEEP | - |
| red-persist | red-team | Yes | Yes | Yes | T3 | forensic | KEEP | - |
| red-exfil | red-team | Yes | Yes | Yes | T3 | forensic | KEEP | - |
| red-infra | red-team | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| red-social | red-team | Yes | Yes | Yes | T3 | divergent | KEEP | - |
| red-reporter | red-team | Yes | Yes | Yes | T3 | integrative | KEEP | - |
| ux-orchestrator | user-experience | Yes | Yes | Yes | T5 | integrative | KEEP | - |
| ux-ai-design-guide | ux-ai-first-design | Yes | Yes | No | T3 | divergent | KEEP | - |
| ux-atomic-architect | ux-atomic-design | Yes | Yes | Yes | T3 | integrative | KEEP | - |
| ux-sprint-facilitator | ux-design-sprint | Yes | Yes | No | T3 | systematic | **ASSESS** | P3 |
| ux-heuristic-evaluator | ux-heuristic-eval | Yes | Yes | Yes | T3 | systematic | KEEP | - |
| ux-inclusive-evaluator | ux-inclusive-design | Yes | Yes | Yes | T3 | systematic | KEEP | - |
| ux-jtbd-analyst | ux-jtbd | Yes | Yes | Yes | T3 | convergent | KEEP | - |
| ux-lean-ux-facilitator | ux-lean-ux | Yes | Yes | Yes | T3 | integrative | KEEP | - |

**Legend:** P0 = critical/confirmed incident; P1 = same family as P0; P2 = structural gap with clear evidence; P3 = inconsistency requiring investigation

---

## Gap Analysis

> Agents that should have web tools but do not currently have them.

### G-001: adv-executor — CONFIRMED GAP (P0)

**Current state:** `tools: Read, Write, Edit, Glob, Grep` | `tool_tier: T2`
**Evidence:** STORY-011 documents that during a C4 adversarial tournament, the S-007 Constitutional AI strategy hallucinated a $3.4B acquisition figure (verified: $25B). The agent cannot call WebSearch or WebFetch to fact-check claims. GitHub #217.
**Recommendation:** ADD `WebSearch`, `WebFetch`, Context7 MCP. Upgrade `tool_tier` to T3.
**Rationale from standards:** The mcp-tool-standards.md "Not included by design" note for adv-* states "Self-contained strategy execution; no external research or cross-session state." This rationale is invalidated by #217: the S-007 strategy specifically requires referencing real-world factual claims (constitutional principles, regulatory frameworks, documented standards). Without web access, factual verification is impossible and hallucination risk is high.
**Note:** The governance tier must change from T2 to T3 in `adv-executor.governance.yaml` and the `adversary/SKILL.md` `allowed-tools` field must add WebSearch, WebFetch.

### G-002: adv-scorer — PROBABLE GAP (P1)

**Current state:** `tools: Read, Write, Edit, Glob, Grep` | `tool_tier: T2`
**Evidence:** adv-scorer implements the S-014 LLM-as-Judge rubric. Its 6 dimensions include "Evidence Quality" (weight 0.15). Scoring evidence quality without ability to verify whether cited sources are real, current, or accurate creates a systematic blind spot in the quality gate. Same family as adv-executor.
**Recommendation:** ADD `WebSearch`, `WebFetch`, Context7 MCP. Upgrade `tool_tier` to T3.
**Rationale:** The "not included by design" note was written when the adversary skill was conceived as purely structural (apply templates, score outputs). The #217 incident demonstrates that factual verification is an actual workflow requirement for the strategy execution and scoring functions.

### G-003: diataxis-explanation — STRUCTURAL GAP (P2)

**Current state:** `tools: Read, Write, Edit, Glob, Grep` | `tool_tier: T2 (comment: T2 subset)` | `cognitive_mode: divergent`
**Evidence:** governance YAML explicitly declares `cognitive_mode: divergent`. The agent-development-standards.md cognitive mode-to-tier table states: "divergent | T3+ (external access)" with rationale "Needs breadth; premature convergence misses sources." The agent's purpose is explanation/conceptual documentation that "requires seeing the bigger picture and illuminating relationships" (from agent description). Writing accurate conceptual explanations of frameworks, libraries, or standards benefits from web access to verify current information.
**Recommendation:** ADD `WebSearch`, `WebFetch`. Upgrade `tool_tier` to T3. Context7 is optional (explanation writing rarely needs API docs, but WebSearch is useful for framework background research).
**Caveat:** This is a weaker case than G-001/G-002. The consequence of not adding web access is lower-quality explanations rather than factual hallucination in security-critical contexts. Assign lower urgency than adv-*.

### G-004: nse-reporter — PARTIAL GAP (P2)

**Current state:** `tools: Read, Write, Glob, Grep, WebFetch` | `tool_tier: T3`
**Evidence:** governance YAML declares T3. T3 definition requires both WebSearch AND WebFetch. The agent has WebFetch but not WebSearch. This is an incomplete T3 implementation. nse-reporter produces program/project status reports referencing technical performance measurement -- looking up standards documentation (WebFetch from known URLs) is covered, but searching for comparable program benchmarks or referencing external standards by concept (WebSearch) is not.
**Recommendation:** ADD `WebSearch`. This makes the tool set consistent with the declared T3 tier.

### G-005: ux-behavior-diagnostician, ux-heart-analyst, ux-kano-analyst — TIER OUTLIERS (P2)

**Current state (all three):** No web tools | `tool_tier: T2`
**Evidence:** All three are sub-skill agents within the `/user-experience` skill family. Their peer agents (ux-ai-design-guide, ux-atomic-architect, ux-sprint-facilitator, ux-heuristic-evaluator, ux-inclusive-evaluator, ux-jtbd-analyst, ux-lean-ux-facilitator) all have WebSearch + WebFetch at T3. The three outlier agents:
- `ux-behavior-diagnostician`: applies Fogg B=MAP model (convergent mode, T2 gov) -- methodology references behavioral research literature
- `ux-heart-analyst`: applies Google HEART framework (systematic mode, T2 gov) -- GSM process produces metrics with external benchmarking value
- `ux-kano-analyst`: applies Kano model (convergent mode, T2 gov) -- applies structured classification from survey data
**Assessment:** These three agents have convergent/systematic cognitive modes, which per the standards do not require T3. They are T2 by cognitive mode, but T3 by family consistency. The question is whether their methodologies require external web access:
- ux-behavior-diagnostician: applies a diagnostic algorithm to provided inputs. Web access is not required for the primary task. ASSESS.
- ux-heart-analyst: produces metrics dashboards from user-provided goals. External benchmark data via web would improve signal baseline. ASSESS.
- ux-kano-analyst: applies the Kano classification table to survey data. No external data needed. KEEP at T2.
**Recommendation:** ASSESS ux-behavior-diagnostician and ux-heart-analyst for promotion to T3 based on whether their outputs regularly reference external benchmarks. KEEP ux-kano-analyst at T2 -- its methodology is entirely self-contained (5x5 classification table applied to survey inputs).

---

## Over-Privilege Analysis

> Agents that have web tools but whose methodology may not require them.

### O-001: eng-qa — ASSESS (P3)

**Current state:** `tools: ... WebSearch, WebFetch` | `tool_tier: T3` | `cognitive_mode: systematic`
**Evidence:** eng-qa is a testing framework documentation agent (per mcp-tool-standards.md matrix rationale: "Testing framework documentation"). The mcp-tool-standards.md matrix includes it with Context7 specifically for testing framework documentation lookup. WebSearch/WebFetch enables finding testing best practices, framework versions, and vulnerability information in test dependencies. The cognitive mode is systematic, which normally maps to T1-T2, but the specific need for current testing framework documentation is a justified exception.
**Assessment:** The Context7 access for framework docs is well-justified. WebSearch access for CVE lookups in test dependencies is justified for a security-conscious engineering workflow. KEEP. Document the justification explicitly.

### O-002: eng-reviewer — ASSESS (P3)

**Current state:** `tools: ... WebSearch, WebFetch` | `tool_tier: T3` | `cognitive_mode: convergent`
**Evidence:** mcp-tool-standards.md "Not included by design" explicitly lists eng-reviewer as excluded from the Context7 matrix, with rationale "Standards verification research." However, the actual `eng-reviewer.md` frontmatter declares `mcpServers: context7: true`. This is a direct conflict between the governance documentation and the agent implementation.
**Assessment:** The matrix "not included by design" note appears to be out of date. eng-reviewer performs final compliance gate verification -- checking code against OWASP standards, ASVS, CIS benchmarks. WebFetch to fetch standards documents and Context7 to verify library-specific security requirements are both defensible for this role. The implementation appears correct; the matrix is wrong. KEEP tools, UPDATE matrix. See Drift section.

### O-003: ux-sprint-facilitator — ASSESS (P3)

**Current state:** `tools: WebSearch, WebFetch` | `tool_tier: T3` | no Context7 | `cognitive_mode: systematic`
**Evidence:** ux-sprint-facilitator's description body mentions Context7 for technology-stack-specific sprint challenges. The frontmatter does not have `mcpServers: context7`. This may be an oversight -- the agent was designed to optionally use Context7 but the frontmatter was not updated. The current T3 without Context7 is internally consistent (WebSearch covers general research; Context7 is a bonus for tech-specific sprints).
**Assessment:** WebSearch/WebFetch are justified for a design sprint facilitator (research comparable solutions, fetch competitor products, look up WCAG standards). The missing Context7 is a potential enhancement but not a gap that causes incorrect behavior. KEEP at T3. Optionally add Context7 as a low-priority enhancement.

---

## mcp-tool-standards.md Drift

> Comparison of Agent Integration Matrix vs actual mcpServers declarations.

### Agents IN the matrix but with incorrect actual state

| Agent | Matrix Says | Actual Frontmatter | Delta |
|-------|-------------|-------------------|-------|
| eng-reviewer | "Not included by design" (explicitly excluded) | `mcpServers: context7: true` | Matrix is wrong -- agent has Context7 |
| ps-analyst | resolve, query | `mcpServers: context7: true` | Consistent |
| ps-architect | resolve, query | `mcpServers: context7: true` | Consistent |
| ps-investigator | resolve, query | `mcpServers: context7: true` | Consistent |
| ps-researcher | resolve, query | `mcpServers: context7: true` | Consistent |
| ps-synthesizer | resolve, query | `mcpServers: context7: true` | Consistent |
| nse-architecture | resolve, query | `mcpServers: context7: true` | Consistent |
| nse-explorer | resolve, query | `mcpServers: context7: true` | Consistent |
| pm-competitive-analyst | resolve, query | `mcpServers: context7: true` | Consistent |
| pm-customer-insight | resolve, query | `mcpServers: context7: true` | Consistent |
| pm-market-strategist | resolve, query | `mcpServers: context7: true` | Consistent |
| All 11 red-team agents | resolve, query | `mcpServers: context7: true` | Consistent |
| All 10 eng-team agents | resolve, query | `mcpServers: context7: true` | Consistent |

### Agents NOT in matrix but WITH Context7 in actual frontmatter

| Agent | Skill | Actual mcpServers |
|-------|-------|-------------------|
| ux-orchestrator | user-experience | `context7: [resolve-library-id, query-docs]` |
| ux-atomic-architect | ux-atomic-design | `context7: [resolve-library-id, query-docs]` |
| ux-heuristic-evaluator | ux-heuristic-eval | `context7: [resolve-library-id, query-docs]` |
| ux-inclusive-evaluator | ux-inclusive-design | `context7: [resolve-library-id, query-docs]` |
| ux-jtbd-analyst | ux-jtbd | `context7: [resolve-library-id, query-docs]` |
| ux-lean-ux-facilitator | ux-lean-ux | `context7: [resolve-library-id, query-docs]` |

**Total missing from matrix: 6 agents.** All are from the UX sub-skill family added after the mcp-tool-standards.md matrix was written.

### Agents in matrix "not included by design" whose actual state CONTRADICTS the exclusion

| Agent | Matrix Exclusion Rationale | Actual State | Verdict |
|-------|---------------------------|-------------|---------|
| eng-reviewer | "Standards verification research" | Has Context7 | Matrix wrong -- REMOVE from exclusion list; ADD to matrix |
| ps-critic | "Quality evaluation; no external library research needed" | No web, no Context7 | Matrix correct |
| ps-validator | "Quality evaluation; no external library research needed" | No web, no Context7 | Matrix correct |
| ps-reporter | "Report generation from existing data" | No web, no Context7 | Matrix correct |
| adv-* | "Self-contained strategy execution" | No web, no Context7 | Matrix wrong for executor/scorer per G-001/G-002 |
| wt-* | "Read-only auditing of worktracker files" | No web, no Context7 | Matrix correct |

**Matrix update required:**
1. Remove eng-reviewer from "Not included" list. Add to matrix with `resolve, query` and rationale "Standards compliance verification."
2. Add the 6 UX sub-skill agents above with `resolve, query` and rationale "Framework-specific design pattern research."
3. Update adv-executor and adv-scorer after G-001/G-002 resolution.

---

## Skill vs Agent Misalignment

> Cases where SKILL.md `allowed-tools` and agent frontmatter `tools` are inconsistent.

### S-001: orchestration SKILL.md has WebSearch/WebFetch; agents do NOT

| Item | WebSearch | WebFetch |
|------|-----------|----------|
| `orchestration/SKILL.md` allowed-tools | Yes | Yes |
| `orch-planner.md` tools | No | No |
| `orch-synthesizer.md` tools | No | No |
| `orch-tracker.md` tools | No | No |

**Evidence:** `orchestration/SKILL.md` declares `allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch, mcp__memory-keeper__*`. None of the three orchestration agents have WebSearch or WebFetch in their individual frontmatter.

**Analysis:** The allowed-tools in SKILL.md acts as an authorization ceiling for agent pre-approval (per skill-standards.md). The individual agents inherit what their own frontmatter declares. The mismatch means:
- The skill is authorized to use WebSearch/WebFetch
- But the agents are not individually declaring it, so they would not inherit it as workers
- orch-planner and orch-synthesizer could benefit from web access for research-informed planning and cross-pipeline synthesis respectively
- orch-tracker does not need web access -- it manages state, not research

**Recommendation:** Resolve intent. Option A: Remove WebSearch/WebFetch from SKILL.md allowed-tools if orchestration agents should not have web access (matches current agent definitions). Option B: Add WebSearch/WebFetch to orch-planner and orch-synthesizer agent frontmatter (makes agents consistent with skill authorization). Given that orch-planner coordinates multi-phase research workflows and orch-synthesizer integrates findings across pipelines, Option B is the better choice for the two planning/synthesis agents. orch-tracker should remain without web tools.

### S-002: diataxis SKILL.md allowed-tools is incomplete (uses array-without-values format)

**Evidence:** `diataxis/SKILL.md` has:
```yaml
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
```
This is the list format. The skill does NOT include WebSearch/WebFetch. This is consistent with the agents (which also lack web tools). No misalignment -- the format matches intent.

However, the diataxis explanation agent (divergent mode, G-003) would require SKILL.md to be updated if web tools are added to the agent.

### S-003: pm-pmm SKILL.md has no allowed-tools field at all

**Evidence:** `pm-pmm/SKILL.md` frontmatter has no `allowed-tools` field. The five pm-pmm agents all declare WebSearch/WebFetch individually. The skill's authorization ceiling is undefined.

**Recommendation:** Add `allowed-tools` to `pm-pmm/SKILL.md` matching the superset of what agents declare: `Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs`.

### S-004: Agents with `tools:` as empty field (cd-generator, cd-validator, tspec-analyst, tspec-generator, uc-author, uc-slicer)

**Evidence:** Six agents declare `tools:` with an empty value (or use array format with values). On inspection, the array format agents (uc-author, uc-slicer, tspec-analyst, tspec-generator, cd-generator, cd-validator) do list their tools correctly in array syntax. This is not a web-tool gap but a format variation that is technically valid YAML.

**Recommendation:** Not a web-tool gap. Flagged for STORY-008 (CLI frontmatter validation) to ensure the empty-value form is handled.

---

## Priority-Ordered Action Items

### P0 — Critical (confirmed incident, fix immediately)

| # | Action | Agent | Files to Change |
|---|--------|-------|----------------|
| 1 | Add WebSearch, WebFetch to tools; add Context7 mcpServers; upgrade tool_tier T2->T3 | adv-executor | `skills/adversary/agents/adv-executor.md`, `adv-executor.governance.yaml` |
| 2 | Update adversary SKILL.md allowed-tools to include WebSearch, WebFetch | adv-executor | `skills/adversary/SKILL.md` |

### P1 — High (same family as confirmed incident)

| # | Action | Agent | Files to Change |
|---|--------|-------|----------------|
| 3 | Add WebSearch, WebFetch to tools; add Context7 mcpServers; upgrade tool_tier T2->T3 | adv-scorer | `skills/adversary/agents/adv-scorer.md`, `adv-scorer.governance.yaml` |

### P2 — Medium (structural gaps with evidence)

| # | Action | Agent | Files to Change |
|---|--------|-------|----------------|
| 4 | Add WebSearch to tools (already has WebFetch); tool_tier already T3 | nse-reporter | `skills/nasa-se/agents/nse-reporter.md` |
| 5 | Add WebSearch, WebFetch to tools; upgrade tool_tier T2->T3 | diataxis-explanation | `skills/diataxis/agents/diataxis-explanation.md`, `diataxis-explanation.governance.yaml` |
| 6 | Update diataxis SKILL.md to include WebSearch/WebFetch if #5 proceeds | diataxis SKILL | `skills/diataxis/SKILL.md` |
| 7 | Investigate ux-behavior-diagnostician: does methodology require external benchmarks? Upgrade to T3 if yes | ux-behavior-diagnostician | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md`, `.governance.yaml` |
| 8 | Investigate ux-heart-analyst: does GSM baseline-setting require external metric benchmarks? Upgrade to T3 if yes | ux-heart-analyst | `skills/ux-heart-metrics/agents/ux-heart-analyst.md`, `.governance.yaml` |

### P3 — Low (inconsistencies; no immediate behavioral impact)

| # | Action | Target | Files to Change |
|---|--------|-------|----------------|
| 9 | Update mcp-tool-standards.md: add 6 UX sub-skill agents to matrix | matrix | `.context/rules/mcp-tool-standards.md` |
| 10 | Update mcp-tool-standards.md: move eng-reviewer from "Not included" to matrix | matrix | `.context/rules/mcp-tool-standards.md` |
| 11 | Update mcp-tool-standards.md: update adv-executor and adv-scorer entries after P0/P1 changes | matrix | `.context/rules/mcp-tool-standards.md` |
| 12 | Resolve orchestration skill vs agent misalignment: add WebSearch/WebFetch to orch-planner and orch-synthesizer, or remove from SKILL.md | orch-planner, orch-synthesizer | `skills/orchestration/agents/orch-planner.md`, `orch-synthesizer.md`, `SKILL.md` |
| 13 | Add allowed-tools field to pm-pmm SKILL.md | pm-pmm SKILL | `skills/pm-pmm/SKILL.md` |
| 14 | Reconcile nse-qa governance tier: governance says T3, tools say T2 | nse-qa | `skills/nasa-se/agents/nse-qa.governance.yaml` |
| 15 | Assess ux-sprint-facilitator Context7 gap: body mentions Context7 but frontmatter omits it | ux-sprint-facilitator | `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` |

---

## L2: Architectural Implications

### Pattern 1: Governance tier and actual tool declaration drift is systemic

The most significant architectural finding is that `tool_tier` in governance YAML and the actual `tools:` field in agent frontmatter have drifted out of sync across multiple agents and skills. Evidence:

- adv-executor: T2 governance, T2 tools -- consistent, but WRONG for its actual methodology needs
- nse-reporter: T3 governance, tools = T2+WebFetch only -- inconsistent
- nse-qa: T2 governance, tools = T2 without web -- consistent, but governance tier does NOT match peer NSE agents all at T3
- ux-behavior-diagnostician/heart-analyst/kano-analyst: T2 governance, T2 tools -- consistent, but outliers in a T3 skill family
- eng-reviewer: T3 governance, has Context7 -- consistent, but contradicts the mcp-tool-standards.md exclusion list

The root cause is that governance YAML and agent frontmatter are maintained independently, and the mcp-tool-standards.md matrix is maintained independently from both. There is no automated consistency check across all three. **Recommendation:** STORY-008 (CLI frontmatter validation) and STORY-009 (CI frontmatter validation) should add a cross-check: for any agent with `tool_tier: T3+`, assert that WebSearch+WebFetch are present in `tools:`. For any agent with `tool_tier: T1`, assert that WebSearch/WebFetch are absent.

### Pattern 2: The "self-contained by design" exclusion rationale needs periodic re-evaluation

The mcp-tool-standards.md exclusion list was written with valid rationale at the time (adversary agents apply deterministic strategy templates; no external research needed). The #217 incident demonstrates that this rationale was incomplete -- the S-007 Constitutional AI strategy makes factual claims that require external verification. Exclusion rationale can become incorrect as agent methodologies evolve and new strategies are added.

**Prevention:** When adding a new strategy to the adversary catalog (S-001 through S-015), explicitly evaluate whether the strategy makes externally-verifiable claims. If yes, verify adv-executor has web access before shipping.

### Pattern 3: UX sub-skill tool tier inconsistency reflects parallel development without a cross-cutting review

The three UX outliers (ux-behavior-diagnostician, ux-heart-analyst, ux-kano-analyst) were likely developed in isolation from the rest of the UX sub-skill family. The remaining 7 UX sub-skill agents are T3 with web tools; these three are T2 without. This is the classic AP-08 (Context-Blind Routing) analog at the development level: agents developed without awareness of the family-level tool tier pattern.

**Prevention:** When adding a new agent to an existing skill family, check tool tier consistency against peer agents as an explicit gate during agent development (add to agent-development-standards.md AD-M guidance).

### Pattern 4: mcp-tool-standards.md has become a lagging indicator, not a leading one

The matrix documents 6 UX sub-skill agents with Context7 that are not in the matrix. It documents eng-reviewer as excluded when it is actually included. These agents were presumably added to the codebase without updating the matrix. The matrix is now descriptively inaccurate.

**Prevention:** Add "update mcp-tool-standards.md Agent Integration Matrix" as a mandatory step in the agent creation checklist (AD-M-002 or equivalent). The matrix should be a SSOT, not a post-hoc summary.

---

## Assumptions and Limitations

1. **GitHub #217 contents:** The incident details in STORY-011 were used as primary evidence for G-001. The specific strategy (S-007), the hallucinated value ($3.4B), and the correct value ($25B) are taken from STORY-011 at face value. If STORY-011 contains errors, G-001 evidence quality degrades from High to Medium.

2. **Cognitive mode to tier mapping is advisory, not deterministic:** The agent-development-standards.md states the divergent mode "typically needs T3+", not "must have T3+". The analysis for diataxis-explanation (G-003) relies on this mapping; it is a recommendation, not a rule violation.

3. **UX outlier assessment (G-005):** The recommendation for ux-behavior-diagnostician and ux-heart-analyst is ASSESS rather than ADD because the agents' methodologies (B=MAP model and HEART/GSM process) operate primarily on user-provided inputs. Whether external benchmarking data is genuinely needed depends on how these agents are invoked in practice. This requires user feedback to resolve definitively.

4. **Completeness of agent count:** The audit covers the 83 agents discovered in the file scan (89 per STORY-012 count; the delta of 6 may be in the user-experience sub-skill directories not under `skills/user-experience/agents/` but under separate `skills/ux-*/agents/` directories, which were included in this scan). No agents are believed to be missed.

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Incident | STORY-011 / GitHub #217 | adv-executor hallucinated $3.4B figure; confirmed missing web tools |
| E-002 | File scan | All 89 agent `tools:` frontmatter fields | Primary data source for current tool state |
| E-003 | File scan | All 89 `.governance.yaml` `tool_tier` fields | Normative tier for each agent |
| E-004 | File scan | All 89 `.governance.yaml` `cognitive_mode` fields | Cognitive mode per agent |
| E-005 | Standard | `agent-development-standards.md` T1-T5 tier definitions | Normative definition of which tools belong at each tier |
| E-006 | Standard | `agent-development-standards.md` Cognitive Mode Taxonomy table | Divergent mode -> T3+ mapping |
| E-007 | File scan | `mcp-tool-standards.md` Agent Integration Matrix | Governance baseline for Context7 assignments |
| E-008 | File scan | All SKILL.md `allowed-tools` fields | Skill-level tool authorization ceiling |
| E-009 | File | `skills/nasa-se/agents/nse-reporter.md` tools: `Read, Write, Glob, Grep, WebFetch` | nse-reporter has WebFetch only despite T3 governance |
| E-010 | File | `skills/nasa-se/agents/nse-reporter.governance.yaml` tool_tier: T3 | T3 requires WebSearch per tier definition |
| E-011 | File | `skills/diataxis/agents/diataxis-explanation.governance.yaml` cognitive_mode: divergent | Divergent mode triggers T3+ recommendation |
| E-012 | File | `skills/eng-team/agents/eng-reviewer.md` mcpServers: context7: true | Contradicts matrix "not included by design" |
| E-013 | File | `skills/orchestration/SKILL.md` allowed-tools includes WebSearch/WebFetch | Skill authorizes web; agents do not declare it |
| E-014 | File | 6 UX sub-skill agent frontmatter with mcpServers context7 | Not present in mcp-tool-standards.md matrix |
| E-015 | File | ux-behavior-diagnostician/heart-analyst/kano-analyst governance YAML tool_tier: T2 | T2 while peer UX agents are T3 |

---

## PS Integration

```yaml
analyst_output:
  ps_id: "STORY-012"
  entry_id: "e-001"
  analysis_type: "gap"
  artifact_path: "projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-012-audit-web-tool-permissions/web-tool-audit-report.md"
  root_cause: "Tool tier governance and agent frontmatter are maintained independently without automated consistency checks, leading to drift between declared tier and actual tools. The adv-executor exclusion rationale ('self-contained strategy execution') was invalidated by the S-007 strategy requiring externally-verifiable factual claims."
  recommendation: "Immediate: add WebSearch+WebFetch+Context7 to adv-executor (P0) and adv-scorer (P1). Medium-term: add WebSearch to nse-reporter, upgrade diataxis-explanation to T3. Long-term: add cross-validation CI check between tool_tier and actual tools declarations."
  confidence: "high"
  next_agent_hint: "eng-security for security review of recommended tool additions (TASK-008 in STORY-012)"
```

---

*Analysis Version: 1.0.0*
*Framework: Gap Analysis + T1-T5 Tier Model + Cognitive Mode Taxonomy*
*Constitutional Compliance: P-001 (evidence-based), P-002 (file-persisted), P-004 (methods documented), P-011 (recommendations tied to evidence), P-022 (assumptions explicit)*
*Date: 2026-03-28*
