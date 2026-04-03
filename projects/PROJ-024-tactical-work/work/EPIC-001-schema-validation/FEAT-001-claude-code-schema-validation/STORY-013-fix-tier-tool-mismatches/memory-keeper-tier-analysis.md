# Memory-Keeper Tier Restriction: Design Analysis

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language finding and recommendation |
| [Analysis Scope and Method](#analysis-scope-and-method) | What was analyzed and how |
| [Current Design Reconstruction](#current-design-reconstruction) | What the current model actually is |
| [Root Cause Analysis: Why T4 Only?](#root-cause-analysis-why-t4-only) | 5 Whys tracing the restriction's origins |
| [L1: Technical Findings](#l1-technical-findings) | Evidence-based analysis for engineers |
| [Trade-off Analysis: Four Options](#trade-off-analysis-four-options) | Weighted matrix across four redesign options |
| [Risk Assessment (FMEA)](#risk-assessment-fmea) | Failure mode analysis for broader access |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic and systemic perspective |
| [Recommendation](#recommendation) | Primary recommendation with rationale |
| [Evidence Summary](#evidence-summary) | All evidence cited |

---

## L0: Executive Summary

Memory-Keeper is currently only available to a small set of orchestration and long-running state agents (T4 tier). The design rationale was sound at the time: keeping worker agents stateless makes them easier to reason about, prevents different agents from accidentally overwriting each other's stored data, and avoids situations where an agent loads stale cached findings and acts on them without knowing they are outdated.

However, the current tier model has a structural flaw. T3 (External: WebSearch + Context7) and T4 (Persistent: Memory-Keeper) are parallel branches that never merge below T5. An agent doing multi-session research -- which is explicitly called out in MCP-M-001 as a recommended use case for Memory-Keeper -- is currently forced into T5 just to combine external access with persistence. That is too much privilege for a worker agent, and T5 includes the Agent tool which workers are forbidden from having (H-35).

The best fix is to add a T3.5 tier (External + Persistent) that combines T3 and T4 capabilities without the Agent tool. This gives research agents like ps-researcher and ps-synthesizer the ability to persist cross-session findings without granting them orchestration delegation powers they should not have.

---

## Analysis Scope and Method

**Scope:** Memory-Keeper access policy within the Jerry Framework's tool security tier model. Specifically: whether the current restriction to T4/T5 is the correct design, or whether lower tiers should gain access.

**Method:**
- 5 Whys root cause analysis to reconstruct design rationale from source evidence
- Steelman of all four redesign options (S-003, H-16)
- Weighted trade-off matrix (Kepner-Tregoe)
- FMEA risk assessment (NASA Systems Engineering Handbook) for broader access scenarios

**Assumptions explicitly stated:**
1. The original T4 restriction rationale is not explicitly documented in the source files. The reconstruction in the 5 Whys section is an inference from structural patterns in the code. This is labeled as inference where applicable.
2. The Agent Integration Matrix in `mcp-tool-standards.md` is the authoritative statement of current assignments.
3. MCP-M-001 ("Memory-Keeper SHOULD be used for multi-session research") is treated as expressing design intent, not just guidance.

---

## Current Design Reconstruction

### The Tier Model as Written

| Tier | Name | Tools | Memory-Keeper? |
|------|------|-------|----------------|
| T1 | Read-Only | Read, Glob, Grep | No |
| T2 | Read-Write | T1 + Write, Edit, Bash | No |
| T3 | External | T2 + WebSearch, WebFetch, Context7 | No |
| T4 | Persistent | T2 + Memory-Keeper | Yes |
| T5 | Full | T3 + T4 + Agent | Yes |

Source: `agent-development-standards.md`, Tool Security Tiers table.

### The Structural Problem

T3 and T4 are parallel branches from T2. They are not a linear hierarchy. The model implies:

```
T2
 ├── T3 (T2 + External)
 ├── T4 (T2 + Memory-Keeper)
 └── T5 (T3 + T4 + Agent)
```

T5 is the only tier that gets BOTH external access AND persistent state. But T5 also includes the Agent tool, which worker agents are explicitly forbidden from having (H-35, H-01/P-003). This creates a gap: an agent that legitimately needs T3 + T4 capabilities (external research + cross-session persistence) has no valid tier to occupy. It is currently either underpowered (T3 only, loses persistence) or overpowered (T5, gains the forbidden Agent tool).

### Agents Currently Affected by the Gap

From the Agent Integration Matrix in `mcp-tool-standards.md`:

| Agent | Current Tier (inferred) | What It Gets | What It's Missing |
|-------|------------------------|--------------|-------------------|
| ps-researcher | T3 | External research | Memory-Keeper for MCP-M-001 multi-session findings |
| ps-synthesizer | T3 | External research | Memory-Keeper for cross-pipeline synthesis state |
| ps-architect | T4 + Context7 | Persistence + library docs | Appears to straddle T4 and T3 -- an undocumented exception |
| nse-requirements | T4 | Persistence | No external research (Context7 excluded) |

The `ps-architect` case is particularly revealing: the Agent Integration Matrix grants it both `context_save/get/search` (Memory-Keeper) AND `resolve, query` (Context7). Under the current strict tier model, that combination has no home. It is effectively T3+T4 without the Agent tool -- exactly the gap described above.

Source: `mcp-tool-standards.md`, Agent Integration Matrix (E-003).

---

## Root Cause Analysis: Why T4 Only?

**Problem statement:** Memory-Keeper is restricted to T4/T5, leaving research and specialist agents without cross-session persistence even when they have a legitimate need.

### 5 Whys

| Level | Question | Answer | Evidence |
|-------|----------|--------|----------|
| Why 1 | Why is Memory-Keeper restricted to T4? | T4 was defined as "Persistent" tier specifically for cross-session state management | `agent-development-standards.md`: "T4: Persistent -- Cross-session state management, orchestration" |
| Why 2 | Why was cross-session state management scoped only to orchestration? | At design time, the primary use case for Memory-Keeper was phase boundary checkpointing in orchestration workflows (MCP-002) | `mcp-tool-standards.md`: "MCP-002: Memory-Keeper context_save MUST be called at orchestration phase boundaries" |
| Why 3 | Why was the research persistence use case (MCP-M-001) not given its own tier? | MCP-M-001 was a SHOULD (secondary), MCP-002 was a MUST (primary). The tier was built around the primary use case. The secondary case was left as guidance without a structural home. | `mcp-tool-standards.md`: MCP-M-001 is MEDIUM; MCP-002 is HARD |
| Why 4 | Why was the T3+T4 combination not created as a named tier? | The tier model was built linearly (T1 -> T5) with T5 as the "full" ceiling. The assumption was that any agent needing both external access and persistence would be orchestrating, therefore T5 was sufficient. | `agent-development-standards.md`: T5 = "T3 + T4 + Agent" -- conflates the combination with orchestration delegation |
| Why 5 (Root Cause) | Why was "external + persistent" assumed to imply "orchestrating"? | **Inference:** The tier model was likely designed top-down from the orchestration use case, not bottom-up from per-agent capability needs. The research agent use case (ps-researcher needing cross-session persistence for multi-week research spikes) was either not considered or was considered acceptable as T3-only because file-based persistence (P-002) was seen as sufficient. | Supporting evidence: MCP-M-001's guidance says "store key findings with `jerry/{project}/research/{slug}`" -- implying Memory-Keeper for research was anticipated but never structurally accommodated |

**Root cause:** The tier model was shaped around the MUST use case (orchestration phase boundaries) and did not create a tier for the secondary SHOULD use case (multi-session research persistence). T5 conflated "external + persistent" with "orchestrating", leaving agents that need the former but not the latter without a valid tier.

---

## L1: Technical Findings

### Finding 1: The Tier Model Has a Structural Gap

The T3/T4 split creates a logical gap. T5 is the only tier combining external access with persistence, but T5 also includes the Agent tool which worker agents cannot have. An agent requiring T3+T4 without Agent has no valid home in the current model.

**Evidence:** `agent-development-standards.md` tier table (E-001); H-35 forbidding Agent tool in worker agents (E-002).

**Confidence:** High. This is a logical consequence of the documented tier definitions, not an inference.

### Finding 2: ps-architect Is Already an Undocumented Exception

The Agent Integration Matrix shows ps-architect has both Context7 (`resolve, query`) and Memory-Keeper (`context_save, context_get, context_search`). No existing tier definition covers this combination except T5. But ps-architect is not an orchestrator. This is either an undocumented exception or a signal that the tier model needs a T3+T4 tier.

**Evidence:** `mcp-tool-standards.md`, Agent Integration Matrix entry for ps-architect (E-003).

**Confidence:** High. The matrix entry is explicit; the tier gap is the logical conclusion.

### Finding 3: MCP-M-001 Creates an Unfulfilled Design Intent

MCP-M-001 ("Memory-Keeper SHOULD be used for multi-session research") creates a design intent without a tier to support it. ps-researcher is T3. T3 has no Memory-Keeper. The rule is a dead letter for the agents it most naturally applies to.

**Evidence:** `mcp-tool-standards.md`: MCP-M-001 explicitly targets "multi-session research that produces reusable findings" (E-004). `mcp-tool-standards.md`: ps-researcher Memory-Keeper column shows "—" (E-005).

**Confidence:** High. The contradiction between MCP-M-001 and ps-researcher's actual access is directly visible.

### Finding 4: Statelessness Has Real Value -- Do Not Abandon It Wholesale

The restriction has legitimate benefits:
- Worker agents that are stateless are easier to test (no setup/teardown of Memory-Keeper state)
- Stateless workers produce deterministic behavior given the same inputs
- Key namespace collisions are easier to prevent when fewer agents write to Memory-Keeper
- The file-based fallback (P-002 file persistence to `projects/`) satisfies most single-session needs without Memory-Keeper

**Evidence:** `mcp-tool-standards.md`: "T4 agents MUST follow MCP key namespace: `jerry/{project}/{entity-type}/{entity-id}`" -- the key governance exists precisely because writes are a coordination hazard (E-006). `mcp-tool-standards.md`: eng-*** and red-*** excluded from Memory-Keeper because "file-based persistence per P-002 (engagement-scoped output)" is sufficient (E-007).

**Confidence:** High. The rationale for statelessness is explicit in the exclusion notes.

### Finding 5: Broader Access Without Governance Would Create Key Collision Risk

If Memory-Keeper access is simply granted to all T3 agents without additional governance, two ps-researcher instances running in parallel on the same project could both write to `jerry/PROJ-001/research/auth-patterns` and produce a last-write-wins collision that silently discards one session's findings.

**Evidence:** E-006 (key namespace requirement); the fact that the namespace standard was created specifically to address this concern implies the concern is real.

**Confidence:** High.

---

## Trade-off Analysis: Four Options

**Options as stated:**
- A: Keep current model, allow documented exceptions
- B: Make Memory-Keeper available at T3+ (any external agent can persist)
- C: Add T3a (External + Memory-Keeper) between T3 and T5
- D: Decouple Memory-Keeper from the tier model entirely (orthogonal concern)

**Steelman of each option (S-003, H-16):**

**Steelman A:** The current model is simple and has 5 tiers, not 6. Exceptions are documented and visible in the Agent Integration Matrix. ps-architect's undocumented T3+T4 combination already works in practice. Adding tiers creates governance complexity and may confuse agent authors about which tier to select. The SSOT for actual MCP access is TOOL_REGISTRY.yaml, not the tier table -- fixing TOOL_REGISTRY.yaml is lower risk than changing the tier taxonomy.

**Steelman B:** Consistency is simpler than exceptions. If any T3 agent can persist, you eliminate the gap by making T3 the "full worker tier." The key namespace standard (E-006) already provides collision governance. Memory-Keeper is a low-risk MCP server (no execution, no external network calls, no secrets access). Broadening access maximizes framework utility with minimal security surface increase.

**Steelman C:** A T3a tier is the most precise surgical fix. It acknowledges the real capability combination that exists (ps-architect already has it), gives it a name and governance, and does not change anything about agents that correctly sit at T3 or T4. It expresses the design intent of MCP-M-001 structurally. The tier number is not critical -- it could be called "T3.5", "T3+", or "T4a."

**Steelman D:** The tier model is about tool access control and security surface. Memory-Keeper access is fundamentally a business need decision (does this agent have multi-session state requirements?) that is orthogonal to whether it uses external sources. Decoupling into a boolean flag (`memory_keeper: true/false`) alongside the existing tier means the tier stays clean and per-agent decisions are explicit. This is the most granular and transparent model.

**Weighted Decision Matrix (Kepner-Tregoe):**

| Criterion (Weight) | A: Exceptions | B: T3+ Blanket | C: T3a Tier | D: Decouple |
|--------------------|--------------|----------------|-------------|-------------|
| Correctness: Fixes the structural gap (25%) | 3 (partial -- gap persists in the model, only in practice resolved) | 8 (eliminates gap) | 9 (eliminates gap precisely) | 9 (eliminates gap via different mechanism) |
| Safety: Prevents key collision (20%) | 9 (fewest agents write) | 5 (all T3 agents can write; depends purely on governance adherence) | 8 (new tier has its own governance) | 8 (per-agent flag with explicit review) |
| Simplicity: Easy for agent authors (20%) | 7 (current docs unchanged; just add exceptions) | 8 (no new tier to learn) | 6 (6th tier to understand) | 5 (two orthogonal axes to configure) |
| Fidelity to MCP-M-001 intent (15%) | 4 (MCP-M-001 remains a dead letter for T3 agents) | 9 (all T3 agents can fulfill MCP-M-001) | 9 (T3a agents fulfill MCP-M-001) | 9 (flag enables any agent to fulfill MCP-M-001) |
| Governance overhead (10%) | 8 (no new standards needed) | 6 (collision governance must be re-audited for all T3 agents) | 7 (one new tier to document) | 5 (two standards axes, potential for confusion) |
| Compatibility: Minimal breaking changes (10%) | 9 (nothing changes) | 6 (all T3 agents gain capability -- existing audit may not reflect) | 8 (backward compatible; existing tiers unchanged) | 7 (requires per-agent flag addition -- schema change) |
| **Weighted Total** | **6.00** | **7.10** | **8.05** | **7.65** |

Score calculation:
- A: (3×0.25)+(9×0.20)+(7×0.20)+(4×0.15)+(8×0.10)+(9×0.10) = 0.75+1.80+1.40+0.60+0.80+0.90 = **6.25**
- B: (8×0.25)+(5×0.20)+(8×0.20)+(9×0.15)+(6×0.10)+(6×0.10) = 2.00+1.00+1.60+1.35+0.60+0.60 = **7.15**
- C: (9×0.25)+(8×0.20)+(6×0.20)+(9×0.15)+(7×0.10)+(8×0.10) = 2.25+1.60+1.20+1.35+0.70+0.80 = **7.90**
- D: (9×0.25)+(8×0.20)+(5×0.20)+(9×0.15)+(5×0.10)+(7×0.10) = 2.25+1.60+1.00+1.35+0.50+0.70 = **7.40**

**Ranking:** C (7.90) > D (7.40) > B (7.15) > A (6.25)

---

## Risk Assessment (FMEA)

Applying FMEA to the top two options (C: T3a tier, D: Decouple).

| Failure Mode | Effect | Cause | S | O | D | RPN | Action |
|---|---|---|---|---|---|---|---|
| **Option C** | | | | | | | |
| Agent author assigns T3a but skips key namespace governance | Two agents write to same key; one's findings are silently overwritten | T3a tier documentation omits the namespace MUST requirement | 7 | 4 | 3 | 84 | T3a tier definition MUST inherit T4's key namespace constraint |
| Agent author confuses T3a vs T4 (which to use?) | T4 agents (orchestration) get externalized; T3a agents do work that belongs to T4 | Similar capability sets with subtle distinction | 4 | 5 | 5 | 100 | Clear selection rule: "T3a = research/specialist agents needing multi-session memory; T4 = orchestrators managing phase state" |
| Schema validator does not recognize T3a | CI passes agents that are in an invalid state | JSON Schema enum not updated | 8 | 2 | 1 | 16 | Update `agent-governance-v1.schema.json` enum on same PR as tier documentation |
| **Option D** | | | | | | | |
| Agent author sets flag without understanding collision risk | Key namespace collision; stale data poisoning | Two-axis configuration is less self-documenting | 7 | 6 | 4 | 168 | Require explicit collision review in agent PR checklist |
| Flag creates confusion with `tool_tier` declaration | Agent definition audit tools may not correctly compute actual MCP access | Two sources of truth for MCP capability | 6 | 5 | 3 | 90 | TOOL_REGISTRY.yaml remains SSOT; flag is a secondary annotation |

S=Severity (1-10), O=Occurrence probability (1-10), D=Detection difficulty (1-10), RPN=S×O×D. RPN > 100 = High priority action required.

**FMEA summary:** Option C's highest RPN is 100 (tier confusion), addressable with a clear selection rule. Option D's highest RPN is 168 (collision risk from two-axis config), harder to mitigate structurally. Option C is lower risk.

---

## L2: Architectural Implications

### The Statelessness Question

The user asks directly: "Is this to keep them stateless and only have the orchestration skills use Memory-Keeper?"

**Yes, partially -- but incompletely.** The statelessness rationale is real and valuable. However, the current model conflates two distinct concerns:

1. **Worker statelessness** (legitimate): Worker agents should not accumulate state that affects subsequent invocations in the same orchestration run. This prevents non-determinism and makes the orchestrator's coordination logic easier to reason about.

2. **Cross-session persistence** (legitimate for some workers): Some workers do multi-session work (research spikes spanning weeks). For those agents, cross-session persistence is not "statefulness" in the problematic sense -- it is caching reusable findings that were expensive to produce. This is architecturally analogous to how databases cache query results: the cache is persistent but does not change the agent's behavior given the same session inputs.

The current model's error is treating both concerns the same way. A better framing:

- **Stateless per invocation:** All worker agents. No agent should carry state between one orchestrator invocation and the next within a session.
- **Cross-session finding cache:** Selected worker agents with multi-session scope. Memory-Keeper for research findings is a cache, not session state.

### Systemic Patterns Identified

1. **Tier model was designed for the MUST use case, not the SHOULD use case.** MCP-002 (orchestration phase boundaries) drove the T4 tier. MCP-M-001 (research findings) was added as a SHOULD but was never given structural expression in the tier model.

2. **ps-architect is already a T3a agent.** Its documented capabilities straddle T3 and T4. Either the Agent Integration Matrix is wrong (it should not have Memory-Keeper) or the tier model is wrong (T3a should exist). The matrix is more recent and reflects actual operational need. The tier model needs to catch up.

3. **The eng-*** and red-*** exclusion rationale is correct and should be preserved.** Those agents use file-based persistence (P-002) scoped to engagement directories. Memory-Keeper for them would create cross-project state pollution -- the wrong kind of persistence. Their exclusion is not a gap; it is correct design. The analysis only addresses agents doing multi-session, cross-project-scoped work (research, synthesis, architecture decisions).

### Long-Term Prevention

If a T3a tier is added, the following should be formalized to prevent future gaps:

1. **Tier selection guide must be updated** with a question: "Does this agent need to persist findings across multiple sessions, separate from the current orchestration workflow?" Yes + T3 needs = T3a.

2. **MCP-M-001 should reference the T3a tier** explicitly, so the connection between the SHOULD rule and the structural enabler is clear.

3. **The Agent Integration Matrix should derive from the tier assignment**, not exist independently. If ps-architect is T3a, its matrix row should be derivable from the T3a definition. Divergence between the matrix and the tier table is a maintenance hazard.

---

## Recommendation

**Recommendation: Option C -- Add a T3a tier (External + Persistent, without Agent tool).**

**Rationale:**

1. It is the highest-scoring option in the trade-off matrix (7.90 vs 7.40 for D, 7.15 for B, 6.25 for A).
2. It has the lowest FMEA RPN for its primary failure mode (100 vs 168 for D), and the primary risk is mitigated by a clear selection rule.
3. It reflects what already exists in practice (ps-architect already has T3+T4 capabilities).
4. It fulfills the design intent of MCP-M-001 structurally, not just as advisory guidance.
5. It preserves the statelessness benefit for agents that do not need cross-session persistence (T1, T2, T3 remain stateless).
6. It does not grant the Agent tool to any worker agent (H-35 compliance preserved).

**Implementation:**

1. Add T3a to the tier table in `agent-development-standards.md`:
   - **T3a** | Extended | T3 + Memory-Keeper | Research/specialist agents with multi-session scope | ps-researcher, ps-synthesizer, ps-architect

2. Update the tier selection guidelines to add: "T3a when the agent needs external research AND cross-session finding persistence. Distinct from T4 (orchestration phase state). T3a agents use Memory-Keeper as a research cache; T4 agents use it for workflow coordination."

3. Reclassify ps-architect from its current ambiguous state to T3a in `agent-development-standards.md` and TOOL_REGISTRY.yaml.

4. Update `agent-governance-v1.schema.json` to include `T3a` in the `tool_tier` enum.

5. Update MCP-M-001 to reference T3a: "Memory-Keeper SHOULD be used for multi-session research. T3a agents are the primary target of this standard."

6. Preserve current T3 for agents that do not need cross-session persistence (ps-investigator, nse-explorer, eng-*, red-*, etc.).

**What should NOT change:**

- eng-*** and red-*** agents: file-based persistence is correct for engagement-scoped work. Do not add Memory-Keeper.
- adv-*** agents: self-contained per invocation. No cross-session state needed.
- The statelessness principle for per-invocation worker behavior.
- The key namespace standard (T3a agents inherit the T4 namespace requirement).

**Uncertainty acknowledgment:** The original design rationale for the T4 restriction is inferred from structure, not from a documented ADR. If an ADR exists that explicitly chose to exclude research agents from Memory-Keeper access for reasons not visible in `mcp-tool-standards.md` or `agent-development-standards.md`, that rationale should be reviewed before implementing T3a.

---

## Evidence Summary

| Evidence ID | Type | Source | Relevance |
|-------------|------|--------|-----------|
| E-001 | Standard | `agent-development-standards.md`: Tool Security Tiers table | Defines T1-T5 and their tool compositions |
| E-002 | Hard rule | `agent-development-standards.md`: H-35 | Worker agents MUST NOT have Agent tool; T5 workers are forbidden |
| E-003 | Matrix entry | `mcp-tool-standards.md`: Agent Integration Matrix, ps-architect row | ps-architect has both Context7 and Memory-Keeper -- an undocumented T3+T4 combination |
| E-004 | Medium standard | `mcp-tool-standards.md`: MCP-M-001 | Memory-Keeper SHOULD be used for multi-session research -- design intent without structural home |
| E-005 | Matrix entry | `mcp-tool-standards.md`: Agent Integration Matrix, ps-researcher row | ps-researcher has no Memory-Keeper despite being the primary multi-session research agent |
| E-006 | Tier constraint | `agent-development-standards.md`: "T4 agents MUST follow MCP key namespace" | Key namespace governance exists because writes are a coordination hazard |
| E-007 | Exclusion note | `mcp-tool-standards.md`: "Not included" section | eng-*** and red-*** excluded because file-based persistence is sufficient -- confirms the exclusion is deliberate, not an oversight |
| E-008 | Tier definition | `agent-development-standards.md`: T5 = "T3 + T4 + Agent" | T5 conflates "external + persistent" with "orchestrating"; root of the structural gap |

---

*Analysis Type: trade-off*
*PS ID: STORY-013*
*Entry ID: e-001*
*Method: 5 Whys (root cause reconstruction) + Kepner-Tregoe weighted matrix (option evaluation) + FMEA (risk assessment) + S-003 Steelman*
*Confidence: High on structural findings (logical from documented evidence); Medium on original design rationale (inferred from structure, not from ADR)*
*Analyst: ps-analyst (convergent mode)*
*Date: 2026-03-28*
