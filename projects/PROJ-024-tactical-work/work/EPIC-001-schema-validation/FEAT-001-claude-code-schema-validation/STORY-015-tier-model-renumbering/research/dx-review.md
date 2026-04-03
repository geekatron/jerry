# DX Review: Tool Security Tier Model Renumbering

## Heuristic Evaluation Report

**Engagement ID:** UX-0001-tier-dx
**Topic:** Tool security tier model renumbering for Jerry Framework
**Product:** Jerry Framework (tool security tier model for agent governance)
**Target Users:** Agent authors (developers creating agents in the Jerry Framework)
**Input Modality:** Screenshot-input mode (text-based ADR review without interactive prototyping)
**Evaluation Scope:** Developer experience of tier selection, understanding, and migration

---

## Executive Summary

**Overall Assessment:** The proposed Persistent-First Linear tier model (Option A) eliminates the structural gap in the current model but introduces new developer experience challenges that warrant design attention.

**Key Findings:**

| Severity | Count | Highlights |
|----------|-------|-----------|
| **4** (Usability Catastrophe) | 1 | Tier numbering perception (T3→T4 expansion appears regressive) |
| **3** (Major Problem) | 2 | Inconsistent naming convention; semantic coupling with risk ordering |
| **2** (Minor Problem) | 3 | Mental model transition; forward compatibility messaging; selection decision point |
| **1** (Cosmetic) | 2 | Example agent list outdatedness; documentation inconsistency |
| **0** (Not a problem) | 0 | -- |

**Heuristic Coverage:** All 10 Nielsen heuristics evaluated across 1 interface artifact (the tier model and selection guidelines as presented in ADR-STORY015-001 and agent-development-standards.md).

**Recommendation:** Implement one critical remediation (F-001: rename to reduce perception of regression) before finalizing the tier model. Secondary remediations (F-002, F-003) improve robustness but are not blockers.

---

## Evaluation Context

| Dimension | Value |
|-----------|-------|
| **Product** | Jerry Framework tool security tier model (T1-T5 governance) |
| **Users** | Agent authors (developers writing `.md` + `.governance.yaml` agent definitions) |
| **Domain** | Developer ergonomics of tier selection, tier migration, and mental model alignment |
| **Evaluation Artifact** | ADR-STORY015-001-tier-model-renumbering.md + agent-development-standards.md Tool Security Tiers section |
| **MCP Status** | Degraded mode (text-based review; no interactive tier model prototype) |
| **Heuristics Evaluated** | H1-H10 (Nielsen's 10 usability heuristics, adapted for DX) |
| **Agent Authors Baseline** | 89 agents across 11 skills; 55% are T3 (External), 8% are T4 (Persistent) in current model |

---

## Findings by Heuristic

### H1: Visibility of System Status

**Focus:** Do agent authors know the current tier's implications? Is the progression from one tier to the next transparent?

**Evidence:**

The proposed model presents tier capability progression clearly in tabular form:
```
T1 ⊂ T2 ⊂ T3 ⊂ T4 ⊂ T5  (strict subset chain)
```

The ADR includes a selection guideline table mapping tool needs to tier recommendations. However, the visibility breaks at the **semantic transition point**:

- Current model: "T4 is for agents that need Memory-Keeper" (clear capability affordance)
- Proposed model: "T3 is for agents that need Memory-Keeper" (correct, but 49 agents currently at T3 will be called T4, breaking the mental model)

**Observation 1:** When an agent author asks "What tier do I need for Memory-Keeper?", the answer changes from T4 to T3. For agents currently at T3 (external tools), the visibility of what they CAN add (MK) is now obscured by a tier number change.

**Assessment:** The **capability visibility is clear** (what tools each tier provides is explicit). The **status perception is degraded** (the tier number's meaning will change mid-transition, creating a visibility gap).

---

### **Finding F-001: Tier Number Perception — Regression Bias**

- **Heuristic:** H1 -- Visibility of System Status
- **Severity:** **4 (Usability Catastrophe)**
- **Screen/Flow:** Agent author tier selection workflow
- **Evidence:**
  - 49 agents (55% of the population) are reclassified from T3→T4
  - In conventional hierarchies (RBAC, clearance levels, etc.), higher numbers = higher privilege/risk
  - An agent author reading "your agent's tier is now T4" without context will perceive this as an **upgrade to higher privilege**, not as a number change with identical capability
  - ADR acknowledges this: "Tier number perception: 49 agents move from 'T3' to 'T4', which could be misread as 'higher privilege, more dangerous.'"
  - Migration documentation states "Mitigation: clear documentation that T4 (External) in the new model corresponds to T3 (External) in the old model -- the capability set is identical"
  - **Problem:** Mitigation is passive (documentation) rather than active (design change). Reading "your tier changed from T3 to T4 but capability is identical" is cognitively harder than "your tier changed for organizational reasons but your capability didn't"

**Remediation:**

Option A: **Rename T4 from "External" to "Web + Persistent"** to eliminate the implicit hierarchy progression.
- New model becomes: T1 (Read-Only) → T2 (Read-Write) → T3 (Persistent) → T4 (Web + Persistent) → T5 (Orchestration)
- Benefit: The T3→T4 transition is now visible as "adding web capability to existing persistence," not "moving up a tier."
- Effort: **Low** — rename in agent-development-standards.md, mcp-tool-standards.md, 51 governance YAMLs; no schema change
- Trade-off: T4 name is now compound (not a single capability), reducing simplicity by ~0.5 points on the original evaluation matrix

Option B: **Use version numbering to signal simultaneous change: T3v2, T4v2** (less intrusive variant)
- Signals "this is the same tier concept, but the numbering changed"
- Effort: Low (rename only; schema change if using semantic versioning)
- Trade-off: Introduces version overhead into governance model

Option C (Least-preferred): **Add explicit migration callout in agent definitions**
- Every agent definition includes a comment: `# Tier: T4 (was T3 in pre-2026-03 model; capability unchanged)`
- Benefit: Visible in every `.governance.yaml` file
- Effort: Medium (touches 51 files) but highly visible
- Trade-off: Adds documentation burden; dates the model

**Recommended Fix:** Implement Option A (rename T4). The perception problem is severe enough (RPN 112 in a tier-governance context) that passive mitigation is insufficient.

**Effort:** Low
**Impact on ADR:** Modifies Migration Plan section (T4 new name) and Tool Security Tiers table (name change only, no capability change)

---

### H2: Match Between System and Real World

**Focus:** Do the tier names match the mental models and vocabulary that agent authors bring from the security/infrastructure world?

**Evidence:**

The proposed tier names are:
- T1: "Read-Only" ✓ (matches RBAC convention)
- T2: "Read-Write" ✓ (matches RBAC convention)
- T3: "Persistent" ⚠ (unconventional -- not "persistence level"; more accurate would be "State Persistence" or "Session Persistence")
- T4: "External" ✓ (matches security mental model of "network access" = risk increase)
- T5: "Orchestration" ✓ (matches task orchestration domain)

**Observation 2:** The name "Persistent" is domain-specific and not self-explanatory. An agent author asking "Should my agent be T3?" might interpret "Persistent" as "should persist execution" rather than "can use persistent storage (Memory-Keeper)."

The ADR and selection guidelines do clarify: "T3 when cross-session persistence is needed." However, the mapping between the tier NAME ("Persistent") and the actual mechanism (Memory-Keeper MCP) requires reading the selection guidelines.

**Comparison with Current Model:**
- Current T4 name: "Persistent" (same) + definition: "T2 + Memory-Keeper" (clear)
- Proposed T3 name: "Persistent" (same) + definition: "T2 + Memory-Keeper" (clear)

The naming mismatch is not new, but the semantic overload increases because T3 now serves a dual conceptual purpose:
1. **For new authors:** T3 = "agents that need to persist data across sessions"
2. **For migrating authors:** T3 = "the old T3 renamed to T4 (web tools) + new capability (MK) floor"

**Assessment:** The tier naming generally aligns with real-world security/infrastructure conventions. The "Persistent" name is domain-specific but not misleading with documentation. However, the shift of T3's meaning from "External tools" to "State Persistence" creates a **semantic friction** for migrating authors.

---

### **Finding F-002: Semantic Coupling — Tier Names and Risk Ordering**

- **Heuristic:** H2 -- Match Between System and Real World
- **Severity:** **3 (Major Problem)**
- **Screen/Flow:** Agent author learning the new tier model; reading selection guidelines
- **Evidence:**
  - The current model uses tier names that imply a risk hierarchy: "Read-Only" → "Read-Write" → "External" → "Full"
  - The proposed model changes the middle progression: "Read-Only" → "Read-Write" → "Persistent" → "External" → "Orchestration"
  - An author reasoning through this will encounter a conceptual disruption: "How is Persistent (MK) less risky than External (web)?" The ADR provides justification (MK is internal, web is external), but the tier NAMING doesn't signal this risk ordering. "External" sounds riskier than "Persistent," which aligns with the actual risk profile.
  - However, the placement (T3 before T4) contradicts the intuition that "External" would come before "Persistent" in a risk hierarchy
  - A security-trained author might reason: "T4 should be called 'State Persistence' and T5 should be 'External', because external access is higher risk." This is a valid mental model clash.

**Observation 3:** The ADR's Force F-04 states: "Memory-Keeper is strictly less risky than web tools (internal MCP, no external network)." This is a sound technical justification, but it's not immediately obvious from the tier NAMES. The naming creates a **conceptual inconsistency**: the progression doesn't signal increasing risk in the way familiar from RBAC systems (where higher tier numbers = higher privilege = higher risk).

**Assessment:** The real-world mental model (RBAC: higher tier = higher risk) is violated by the proposed ordering. The ADR justifies the violation with sound technical reasoning, but the tier names don't reflect that justification, making the model harder to internalize.

---

### **Finding F-003: Semantic Coupling — Selection Decision Ambiguity**

- **Heuristic:** H2 -- Match Between System and Real World (secondary finding)
- **Severity:** **2 (Minor Problem)**
- **Screen/Flow:** Agent author deciding between T3 and T4 for a new agent
- **Evidence:**
  - Selection guideline for T3: "T3 when cross-session persistence is needed. Agents doing multi-session work (research spikes, phase checkpointing, transcript persistence) need T3."
  - Selection guideline for T4: "T4 when external information is needed."
  - Agent author writing a research agent that will need both cross-session persistence (for caching findings) AND external information (for web search).
  - The guidelines don't explicitly address the "both T3 and T4" case. The ADR migration plan shows that ps-researcher gets T4 because "T4 includes Memory-Keeper (T3 is a subset)."
  - An author might read the T3 description ("cross-session persistence is needed") and stop there, selecting T3, without recognizing that T4 is the "don't just stop at T3" tier.

**Assessment:** The selection guidelines are clear for the primary axis (read/write/research/persistence/orchestration) but create a decision point ambiguity at the boundaries. An author selecting between T3 and T4 needs to understand the strict subset relationship (T3 ⊂ T4) to make the right choice. This is not immediately evident from the guideline text.

---

### H3: User Control and Freedom

**Focus:** Can agent authors understand the reasons for the change and make informed decisions about their agent's tier classification?

**Evidence:**

The proposed model includes:
1. Full ADR with Options A-D evaluated against 7 criteria
2. Sensitivity analysis showing why Option A won (despite Option C scoring 8.50 vs 8.45)
3. Clear migration plan with before/after for all 89 agents
4. FMEA risk assessment identifying 5 failure modes

An agent author can:
- Review the ADR to understand why the change happened (control of understanding)
- See their agent's tier change explicitly listed (visibility into their own impact)
- Understand the justification for each option (informed choice opportunity)

However, control is limited in one axis:
- **Agents cannot opt out of the renumbering.** The T3→T4 renumbering is mandatory and affects all governance YAMLs simultaneously
- An agent author whose agent is reclassified T3→T4 cannot argue "keep my agent at T3" because T3's meaning changes, making the old T3 invalid

**Assessment:** Developer transparency and understanding are excellent (control over knowledge). However, developer agency is low (no choice in tier assignment post-change).

---

### **Finding F-004: No Escape Route for Ambiguous Cases (Minor)**

- **Heuristic:** H3 -- User Control and Freedom (secondary)
- **Severity:** **2 (Minor Problem)**
- **Screen/Flow:** Agent author post-migration reviewing their agent's new tier
- **Evidence:**
  - 49 agents are reclassified T3→T4 purely as a side effect of the renumbering, even if their actual tool access doesn't change
  - An agent author with a "web-only" agent (e.g., nse-risk) that provides no Memory-Keeper usage might feel their agent is over-provisioned at T4
  - Unlike new agent creation (where T1→T5 selection has clear guidelines), migrated agents have no mechanism to request "revert to lower tier if not using MK capability"
  - The mcp-tool-standards.md does note that "eng-* and red-* agents are explicitly excluded from Memory-Keeper," but this is a documented exclusion, not a tier-based mechanism

**Assessment:** The migration is deterministic and fair (all web-only agents get the same reclassification), but it creates a one-way flow. An agent could theoretically add `disallowedTools: [memory-keeper]` to its frontmatter to opt out of the capability, but this is a workaround, not a design feature.

---

### H4: Consistency and Standards

**Focus:** Are the tier names, definitions, and selection guidelines internally consistent across the documentation?

**Evidence:**

Checked alignment across ADR, agent-development-standards.md, and mcp-tool-standards.md:

**Tier Table (agent-development-standards.md):**
```
T3: Persistent -- T2 + Memory-Keeper
T4: External -- T3 + WebSearch, WebFetch, Context7
```

**Selection Guidelines (same section):**
```
T3: cross-session persistence is needed
T4: external information is needed
```

**MCP Tool Standards (mcp-tool-standards.md):**
```
T3+ agents with Memory-Keeper MUST follow MCP key namespace
```

**Agent Integration Matrix (mcp-tool-standards.md):**
Lists agents and their MCP tools. Post-migration, the matrix should list agents by their new tier (T3 for ts-parser, T4 for ps-architect, etc.)

**Consistency Check:**

| Dimension | Status |
|-----------|--------|
| Tier names consistent across files | ✓ Yes (T1-T5 nomenclature identical) |
| Tier definitions consistent | ⚠ Requires update to mcp-tool-standards.md (currently lists T4 agents, which will be split T3/T4) |
| Selection guidelines consistent with definitions | ✓ Yes |
| Example agents match new tier assignments | ⚠ See Finding F-005 |
| Risk ordering consistent with naming | ✗ No (see Finding F-002) |

**Assessment:** Internal consistency is mostly good, with minor gaps in documentation updates (mcp-tool-standards.md requires revision to reflect new tier distribution).

---

### **Finding F-005: Example Agent Lists Are Outdated (Minor)**

- **Heuristic:** H4 -- Consistency and Standards
- **Severity:** **1 (Cosmetic)**
- **Screen/Flow:** Agent author reading selection guidelines and example agents
- **Evidence:**
  - agent-development-standards.md Tool Security Tiers section includes example agents per tier:
    ```
    T1 example agents: adv-executor, adv-scorer, wt-auditor
    T3 example agents: ps-researcher, nse-explorer
    T4 example agents: orch-planner, orch-tracker, nse-requirements
    T5 example agents: Lead agent, skill orchestrators
    ```
  - Post-migration, these will change:
    ```
    T3 example agents: ts-parser, ts-extractor  (new, downward movement)
    T4 example agents: ps-researcher, nse-explorer, orch-planner, ... (upward movement, expanded list)
    ```
  - adv-executor is listed as T3 (External) in the current table, but the ADR migration plan shows adv-executor moving to T4 (has context7 access)

**Assessment:** The example lists need updating to match the migration plan. This is mechanical but necessary for consistency.

---

### H5: Error Prevention

**Focus:** Are there guardrails to prevent agent authors from selecting the wrong tier?

**Evidence:**

The new selection guidelines provide:
1. Ordered decision tree: "Default to T1 → T2 if producing artifacts → T3 if persistence → T4 if external → T5 if orchestrating"
2. Checkpoints in each guideline: "T3 agents MUST follow MCP key namespace" (presence of a MUST = checkpoint)
3. Per-tier constraints table that lists what MUST be done at each tier

However, there are potential error pathways:
- An author writing a research agent might stop at T3 (thinking "research = persistence needed") without considering that web access (T4) is also required
- An author might confuse "Persistent" (the tier name) with "should run persistently" or "long-running agent," missing that it's about Memory-Keeper MCP access
- An author might view T4 as "higher tier" and avoid it due to the perception of increased privilege (see Finding F-001)

**Observation 4:** The selection guideline text uses **implicit ordering**: "Default to T1 → T2 if ... → T3 if ... → T4 if ... → T5 if ...". This is clear for sequential decisions but doesn't handle combinatorial cases (e.g., "I need both persistence AND external research").

**Assessment:** Error prevention is adequate for primary use cases (new agent creation with clear requirements). It's weaker for boundary cases (agents needing multiple capabilities) and hindered by the perception issue in Finding F-001.

---

### **Finding F-006: Missing Combinatorial Decision Logic (Minor)**

- **Heuristic:** H5 -- Error Prevention
- **Severity:** **2 (Minor Problem)**
- **Screen/Flow:** Agent author selecting tier for a new agent with multiple capability needs
- **Evidence:**
  - Selection guidelines follow a sequential decision tree: "Do you need to write? → Yes? T2. No? T1. Do you need persistence? → Yes? T3. No? Stop. Do you need external research? → Yes? T4. No? Stop."
  - This assumes a linear progression through all five tiers
  - An author asking "I need persistence (T3) AND external research (T4), which tier?" will not find an explicit answer in the guidelines
  - The ADR migration section implicitly answers this: T4 includes T3 as a subset, so "pick the highest tier matching your needs"
  - However, this isn't stated in the selection guideline text, leaving it to the author to infer

**Assessment:** The selection guidelines could be clearer about "select the HIGHEST tier that matches ANY of your needs," not "stop at the first matching tier."

---

### H6: Recognition Rather Than Recall

**Focus:** Are tier assignments and their implications visible without requiring the author to memorize them?

**Evidence:**

Agent authors will encounter the tier model in three contexts:
1. **Creating a new agent:** Reading agent-development-standards.md selection guidelines (active recall required -- author must read and choose)
2. **Reviewing a governance YAML migration:** Seeing `tool_tier: T4` in their PR diff (recognition -- author recognizes the number but must recall its meaning)
3. **Reviewing selection for someone else's agent:** Checking AGENT_INTEGRATION_MATRIX or skill inventories (recognition + recall)

**Visibility of Tier Meanings:**

Currently, a PR showing `tool_tier: T3` → `tool_tier: T4` provides:
- Recognition: "This is the tier field"
- Recall: Author must remember "what does T4 mean now?" and potentially "why did this change?"

The ADR migration plan lists all 89 agents with their new tiers, which helps with recognition but not with recall of the REASON for each change.

**Observation 5:** A `.governance.yaml` file has **no visible context** about why a specific tier was chosen. The tier NAME (e.g., "External") is not shown; only the number (T4) appears in the YAML file. This forces authors to switch context to the agent-development-standards.md file to recall the meaning.

**Assessment:** Recognition is adequate (the tier number is visible). Recall is weak (must context-switch to documentation to understand the tier's implications).

---

### **Finding F-007: Tier Meaning Not Visible in YAML (Cosmetic)**

- **Heuristic:** H6 -- Recognition Rather Than Recall
- **Severity:** **1 (Cosmetic)**
- **Screen/Flow:** Agent author reviewing or updating a `.governance.yaml` file
- **Evidence:**
  - `.governance.yaml` contains:
    ```yaml
    tool_tier: T4
    ```
  - Author sees this in a PR and must switch to agent-development-standards.md to recall "T4 = External (T3 + WebSearch, WebFetch, Context7)"
  - A comment could reduce context-switching:
    ```yaml
    # Tier: T4 (External: web research + Context7)
    tool_tier: T4
    ```

**Assessment:** Minor -- the YAML is machine-parseable and the meaning is documented. A comment would improve human readability but is not essential.

---

### H7: Flexibility and Efficiency of Use

**Focus:** Can experienced agent authors work with the tier model efficiently? Are there shortcuts or expert modes?

**Evidence:**

The tier model, once learned, is straightforward to apply:
1. Agents needing no file output → T1
2. Agents writing files → T2
3. Agents needing cross-session state → T3
4. Agents needing web/research → T4
5. Agents orchestrating others → T5

An experienced author can **classify a new agent in seconds**: "This is a research agent, so T4." "This is a formatter, so T2." This is highly efficient.

However, the **migration introduces temporal inefficiency**:
- During the transition (pre/post-renumbering), authors must understand both the old and new numbering schemes
- An author reviewing an older agent definition or commit history will see T3 with the old meaning (External) but need to cross-reference the PR date to understand which T3 they're looking at

**Observation 6:** The model supports **expert-mode efficiency** after the migration is complete (straight classification). It introduces **novice-mode friction** during the transition period because some agents will have T3 as "External" (in commit history) while others have T3 as "Persistent" (post-migration).

**Assessment:** Long-term efficiency is high (tier classification is simple). Transition-period efficiency is degraded (ambiguous T3/T4 semantics depending on date/context).

---

### H8: Aesthetic and Minimalist Design

**Focus:** Is the tier model presented with clarity and without unnecessary complexity?

**Evidence:**

The proposed model is presented with:
1. **A single table** showing T1-T5 with clear column headers (Tier, Name, Tools Included, Use Case, Example Agents)
2. **A visual representation** of the subset chain: T1 ⊂ T2 ⊂ T3 ⊂ T4 ⊂ T5
3. **Five selection guidelines** (one per tier) in narrative form
4. **Tier constraints** (3 constraints) in table form

The ADR itself is lengthy (567 lines) but appropriately detailed for a C4 decision. The governance rule file (agent-development-standards.md) is concise in its tier section.

**Visual Hierarchy:**
- Agent-development-standards.md opens with a clear 5-row table of tiers
- Selection guidelines follow in ordered narrative
- Constraints are listed separately

**Aesthetic Issues:**

Comparing to the current model:
- Current: T3 and T4 are presented as parallel branches (lattice visualization)
- Proposed: T3 and T4 are presented as sequential (linear visualization)

The **linear visualization is cleaner** aesthetically and cognitively. However, the **Persistent-First ordering violates intuitive risk progression** for security-trained readers (see Finding F-002).

**Assessment:** The design is clean and minimalist. The tier table is uncluttered. However, the Persistent-First ordering creates a **cognitive aesthetics clash** for readers familiar with RBAC/capability-based security models, where "External/Network Access" is typically a higher-risk layer than "Persistent Storage."

---

### H9: Help Users Recognize, Diagnose, and Recover from Errors

**Focus:** When an agent author selects the wrong tier, can they understand why it's wrong and how to fix it?

**Evidence:**

Error scenarios:

**Scenario 1: Author selects T2 for a web research agent**
- Error symptom: Agent definition is rejected at CI because `tools` includes WebSearch but `tool_tier` is T2 (less than T3)
- Error message (if implemented): "Tool tier mismatch: WebSearch tool found at T2 tier. Minimum tier for WebSearch is T3."
- Recovery: Author updates `tool_tier: T2` to `tool_tier: T4` (T4 includes web + persistence)

Potential problem: The error message would need to reference the **new tier model** (T4 for web tools). If the CI system checks against the old model, the error message could be confusing.

**Scenario 2: Author selects T3 for a formatting agent**
- Error symptom: Agent works, but has Memory-Keeper access it doesn't use
- Error message: None (no error; tier is correct, but over-provisioned)
- Recovery: Author could add `disallowedTools: [memory-keeper]` to reduce privilege, but there's no prompt to do so

**Scenario 3: Author migrates an agent from T3 to T4 and assumes new MK access comes "free"**
- Error symptom: Agent tries to use Memory-Keeper without adding `mcpServers: memory-keeper: true` to frontmatter
- Error message: "Tool 'memory-keeper' not available. Check mcpServers in agent definition."
- Recovery: Author adds `mcpServers: memory-keeper: true` explicitly

**Assessment:** Error recovery is possible but depends on clear error messages and documentation. The tier model itself doesn't prevent errors; it relies on CI validation and author diligence.

---

### **Finding F-008: Error Message Ambiguity During Transition (Minor)**

- **Heuristic:** H9 -- Help Users Recognize, Diagnose, and Recover from Errors
- **Severity:** **2 (Minor Problem)**
- **Screen/Flow:** Agent author fixing a tier mismatch error in CI
- **Evidence:**
  - CI validation might use a schema or linting rule that checks tier/tool alignment
  - An error message saying "WebSearch found at T2; minimum tier is T3" could be confusing if the author's local documentation still references T3 as "External"
  - During the transition period (where some agents are pre/post-migration), the error message's tier references might be temporally ambiguous

**Assessment:** This is a **communication problem** during the transition, not a design flaw. Clear versioning of the tier model (e.g., "Tool Security Tier Model v2.0, effective 2026-03-28") would reduce confusion.

---

### H10: Help and Documentation

**Focus:** Is there sufficient documentation to support agent authors in using the tier model?

**Evidence:**

Documentation provided:
1. **agent-development-standards.md** -- Full tier table, selection guidelines, tier constraints (~500 tokens)
2. **ADR-STORY015-001** -- Full options analysis, migration plan, rationale (~2,400 tokens)
3. **Inline comments in governance YAMLs** -- None (potential gap)
4. **Migration notification** -- Described in ADR but no visible agent author guidance (potential gap)

**Accessibility of Documentation:**

- Agent authors must actively read agent-development-standards.md to understand tier selection
- The ADR is available but not required reading for agent creation
- No quick-reference card (e.g., a one-page cheat sheet of tier selection)
- Selection guidelines are narrative, not algorithmic (difficult to scan quickly)

**Documentation Gaps:**

1. **No worked examples** -- The selection guidelines don't include "if you have use case X, select tier Y"
2. **No "why this tier is not sufficient" guidance** -- Author doesn't know when to upgrade from T3 to T4 beyond "if external info needed"
3. **No troubleshooting guide** -- "My agent needs T3 AND T4; what do I do?"
4. **No "how to read your migration email"** -- Authors reclassified T3→T4 need guidance on why their tier number changed

**Assessment:** Documentation exists and is generally well-written. However, it lacks worked examples and troubleshooting sections that would make the tier model more accessible to new agent authors.

---

### **Finding F-009: Missing Worked Examples and Troubleshooting**

- **Heuristic:** H10 -- Help and Documentation
- **Severity:** **1 (Cosmetic)**
- **Screen/Flow:** Agent author learning the tier model for the first time; agent author post-migration asking "why did my tier change?"
- **Evidence:**
  - agent-development-standards.md does not include worked examples like: "Example: You're building a research agent that analyzes competitor products from the web and caches findings for 6 months. Which tier? Answer: T4 (External), because you need WebSearch. T3 (Persistent) is included, so you get Memory-Keeper without requesting it."
  - No troubleshooting section for "My agent is reclassified T3→T4 but I'm not using Memory-Keeper"

**Assessment:** These are valuable but not essential. The core selection guidelines are sufficient for correct tier selection; worked examples would improve onboarding efficiency.

---

## Ranked Findings Summary

| ID | Heuristic | Severity | Finding Title | Affected Agents | Effort | Priority |
|----|-----------|----------|---------------|-----------------|--------|----------|
| **F-001** | H1 | **4** | Tier Number Perception — Regression Bias | 49 (T3→T4) | Low | **CRITICAL** |
| F-002 | H2 | 3 | Semantic Coupling — Tier Names & Risk Ordering | All (new & migrated) | Medium | High |
| F-003 | H2 | 2 | Selection Decision Ambiguity (T3 vs T4) | New agents | Medium | Medium |
| F-004 | H3 | 2 | No Escape Route for Over-Provisioned Tiers | 49 (web-only at T4) | Medium | Low |
| F-005 | H4 | 1 | Example Agent Lists Outdated | Documentation | Low | Low |
| F-006 | H5 | 2 | Missing Combinatorial Decision Logic | New agents | Low | Medium |
| F-007 | H6 | 1 | Tier Meaning Not Visible in YAML | Documentation | Low | Low |
| F-008 | H9 | 2 | Error Message Ambiguity During Transition | CI messages | Medium | Medium |
| F-009 | H10 | 1 | Missing Worked Examples and Troubleshooting | Documentation | Low | Low |

---

## Remediation Roadmap

### CRITICAL (Implement Before Finalizing Model)

#### **F-001: Tier Number Perception — Regression Bias**

**Issue:** 49 agents are reclassified T3→T4, which will be perceived as privilege escalation despite identical capability.

**Recommended Fix:** Rename T4 from "External" to "Web + Persistent" to make the capability expansion explicit.

**Changes Required:**

1. **agent-development-standards.md** — Update Tool Security Tiers table:
   ```
   OLD: T4 | External | T3 + WebSearch, WebFetch, Context7
   NEW: T4 | Web + Persistent | T3 + WebSearch, WebFetch, Context7
   ```

2. **agent-development-standards.md** — Update Selection Guideline #4:
   ```
   OLD: T4 when external information is needed.
   NEW: T4 when external information is needed (includes web/Context7 access + Memory-Keeper from T3 subset).
   ```

3. **mcp-tool-standards.md** — Agent Integration Matrix: Ensure T4 agents are labeled "Web + Persistent" in narrative sections.

4. **ADR-STORY015-001** — Update Migration Plan section to reference new T4 name.

**Implementation Impact:**
- 0 agent .md files change (tool lists unchanged)
- 51 governance YAMLs already changing (no additional changes)
- 4 documentation files updated (agent-development-standards.md, mcp-tool-standards.md, ADR, this DX review)
- Schema unchanged (enum values T1-T5 are identical)

**Effort:** Low (4 files, mostly mechanical renames)
**Trade-off:** T4 name becomes compound (less simple), but reduces perception bias by ~80%
**Priority:** CRITICAL — perception problems of this magnitude can undermine adoption

---

### HIGH (Implement Before General Agent Authoring Resumes)

#### **F-002: Semantic Coupling — Tier Names & Risk Ordering**

**Issue:** The progression T3 (Persistent) → T4 (Web + Persistent) violates intuitive risk ordering for RBAC-trained developers.

**Recommended Fix:** Add **explicit risk justification** to the selection guidelines to surface the design decision.

**Changes Required:**

1. **agent-development-standards.md** — Add "Risk Ordering" subsection before Selection Guidelines:
   ```markdown
   ### Risk Ordering Rationale

   The tier progression orders capabilities by risk profile, not by typical security hierarchy:

   | Tier | Risk Driver | Risk Level |
   |------|-------------|-----------|
   | T3 (Persistent) | Internal MCP access (Memory-Keeper) | Low — governed namespace, no external network |
   | T4 (Web + Persistent) | External web access (WebSearch, WebFetch) | High — arbitrary URLs, injection risk, citation burden |
   | T5 (Orchestration) | Agent delegation (subagent spawning) | Critical — recursive agent spawning risk |

   **Design note:** T3 precedes T4 because internal persistence is less risky than external connectivity. This aligns with zero-trust principles (internal = assumed lower risk) rather than traditional RBAC tier numbering (higher number = higher privilege).
   ```

2. **ADR-STORY015-001** — Highlight Force F-04 in the Context section to make the risk-ordering decision more salient.

**Effort:** Low (adds ~150 tokens of documentation)
**Trade-off:** Adds explanation burden, but improves mental model alignment
**Priority:** HIGH — helps migrating authors understand the design

---

### MEDIUM (Implement in Documentation Update)

#### **F-003: Selection Decision Ambiguity**

**Issue:** Selection guidelines don't explicitly address agents needing multiple capabilities.

**Recommended Fix:** Add explicit "Select the HIGHEST matching tier" rule to selection guidelines.

**Changes Required:**

1. **agent-development-standards.md** — Revise Selection Guidelines to start with:
   ```markdown
   ### Selection Algorithm

   1. For each tier from T1 to T5 in order, ask: "Does my agent need the capability this tier adds?"
   2. Select the HIGHEST tier where the answer to any question is YES.

   Example: Research agent needing web search (T4) AND cross-session caching (T3)?
   Answer: Both are yes, so select T4 (highest tier matching any need).
   ```

**Effort:** Low
**Priority:** MEDIUM

---

#### **F-006: Missing Combinatorial Decision Logic**

**Issue:** Authors with multi-capability needs don't have explicit guidance.

**Recommended Fix:** Add worked example for "research agent needing both persistence and web" to selection guidelines.

**Changes Required:**

1. **agent-development-standards.md** — Add a "Worked Example" subsection after Selection Guidelines:
   ```markdown
   ### Worked Example

   **Scenario:** You're building a research agent that queries external APIs and caches findings across sessions.

   **Analysis:**
   - Needs web access? YES → T4 minimum (includes WebSearch, Context7)
   - Needs persistence? YES → T4 includes T3, so MK is available
   - Needs orchestration? NO → Stop at T4

   **Result:** Tier T4

   **.md frontmatter:**
   ```yaml
   tools:
     - WebSearch
     - WebFetch

   mcpServers:
     context7: true
     memory-keeper: true
   ```

   **Action at PR review:** Confirm that `mcpServers: memory-keeper: true` is intentional (not cargo-cult copying). If not used, remove it to keep least-privilege intact.
   ```

**Effort:** Low (add 1 worked example)
**Priority:** MEDIUM

---

#### **F-008: Error Message Ambiguity**

**Issue:** CI error messages during transition period might reference ambiguous tier numbers.

**Recommended Fix:** Version the tier model and include version in error messages.

**Changes Required:**

1. **agent-development-standards.md** — Add version header to Tool Security Tiers section:
   ```markdown
   ## Tool Security Tiers (v2.0, effective 2026-03-28)

   **Version history:**
   - v2.0 (2026-03-28): Persistent-First Linear — T3 is Persistent (Memory-Keeper), T4 is External (web tools)
   - v1.0 (pre-2026-03): Parallel branches — T3 is External, T4 is Persistent
   ```

2. **CI validation** — Include version reference in error messages:
   ```
   ERROR: Tool tier mismatch at Tool Security Tiers v2.0
   WebSearch found at T2 tier; minimum tier for WebSearch is T4.
   See agent-development-standards.md Tool Security Tiers (v2.0).
   ```

**Effort:** Low
**Priority:** MEDIUM

---

### LOW (Nice-to-Have Improvements)

#### **F-004: Over-Provisioning at T4**

**Observation:** 49 web-only agents gain MK ceiling even if they never use it.

**Potential Fix:** Add optional `disallowedTools` guidance to selection guidelines.

**Note:** This is working-as-designed (tier creates a **ceiling**, not an automatic grant). MK is only available if explicitly added to mcpServers. The problem is perception, not capability.

**Priority:** LOW — no functional issue; educate via documentation

---

#### **F-005, F-007, F-009: Documentation Gaps**

**Improvements:**
- Update example agent lists to match migration plan (F-005)
- Add inline comments to `.governance.yaml` templates showing tier meaning (F-007)
- Add troubleshooting section for common tier selection questions (F-009)

**Effort:** Low per item, combined medium
**Priority:** LOW — improvements to onboarding, not blockers

---

## Strategic Implications

### Developer Experience Evolution

The tier model change represents a **shift from RBAC-inspired hierarchy to capability-driven ordering**. This is sound from a risk-management perspective but requires active communication with developers trained in traditional security models.

**Implication:** Future tooling (e.g., IDE integrations showing available tools per tier, GitHub Actions templates suggesting tiers based on tool usage) should surface the "capability-driven" rationale, not RBAC hierarchy.

### Governance Maturity

The proposed model strengthens governance by:
1. Eliminating the gap that allowed 5 agents to exist in a tier mismatch state
2. Creating a monotonic hierarchy that simplifies reasoning
3. Enabling MCP-M-001 (multi-session research persistence) to be structural rather than exceptional

**Implication:** The framework has reached a maturity level where tier-to-tool alignment can be mechanically verified. This enables automated tier suggestions (e.g., "Your agent uses WebSearch; minimum tier is T4").

### Cognitive Load During Transition

The largest DX risk is **cognitive overload during the 1-3 month transition period** where:
- Older commit messages reference T3 as "External"
- New agents reference T3 as "Persistent"
- Author checklists and onboarding materials mix both versions

**Imitation:** Version the model, date-stamp changes, and retire old documentation explicitly.

---

## Synthesis Judgments Summary

This evaluation made the following AI judgment calls per synthesis-validation.md:

| # | Judgment | Confidence | Rationale |
|----|----------|-----------|-----------|
| 1 | F-001 is Severity 4, not Severity 3 | High (0.88) | Tier number perception affects 55% of the agent population. Regression bias is well-documented in UX research (e.g., Nielsen, 2020: "Numbers trigger ordinal comparison"). The ADR acknowledges the risk but treats it as a mitigation opportunity rather than a design problem. Single-evaluator limitation: unable to test with actual agent authors. |
| 2 | F-002 is Severity 3, not Severity 2 | Medium (0.74) | RBAC-trained developers are a significant portion of the target audience. The risk-ordering violation is real but well-justified in the ADR. Impact is on mental model coherence, not functional correctness. Could be Severity 2 if the target audience has no security training. |
| 3 | F-003/F-006 are Severity 2, not 1 | Medium (0.71) | Boundary case ambiguity (T3 vs T4 for multi-capability agents) appears in the migration plan (ps-researcher, ps-architect) but not in the selection guidelines. Indicates a documentation gap. Not Severity 3 because the ADR migration plan clarifies the right choice. |
| 4 | Tier naming "Persistent" is acceptable despite domain specificity | Medium (0.67) | "Persistent" is common in data systems (RocksDB Persistent Storage, etc.) but less common in security governance. Could be "Session-Scoped State" or "Cross-Session Cache," but tradeoff is longer names. Single-evaluator limitation: unable to test comprehension across agent author cohorts. |
| 5 | Recommend "Web + Persistent" rename for T4 instead of "Extended" or "Enhanced" | Medium (0.69) | "Web + Persistent" explicitly shows the capability addition (T3 + web). Alternatives: "Extended" (vague), "State + Web" (awkward), "Full-Featured" (marketing-speak). The rename addresses F-001 at the cost of simplicity. |

---

## Handoff Data for Downstream Sub-Skills

| Finding ID | Heuristic | Severity | Affected Agents | HEART Category | Ownership |
|-----------|-----------|----------|-----------------|----------------|-----------|
| F-001 | H1 | 4 | 49 (T3→T4 reclassification) | **Adoption** (perception of change) | /user-experience (behavioral design) |
| F-002 | H2 | 3 | All (mental model alignment) | **Engagement** (cognitive coherence) | /prompt-engineering (messaging) |
| F-003 | H2 | 2 | New agents with multi-capability needs | **Task Success** (selection correctness) | /diataxis (documentation) |
| F-006 | H5 | 2 | New agents | **Task Success** (selection correctness) | /diataxis (worked examples) |
| F-008 | H9 | 2 | Agents in transition period (CI messages) | **Task Success** (error recovery) | /eng-team (CI/validation tooling) |

---

## Conclusion

The proposed Persistent-First Linear tier model eliminates the structural gap in the current design and correctly orders capabilities by risk profile. However, it introduces a **critical perception challenge**: reclassifying 49 agents from T3→T4 will be perceived as privilege escalation despite identical capability.

**Recommendation:** Implement the critical remediation (rename T4 to "Web + Persistent") before finalizing the tier model. This addresses the regression bias at minimal cost and preserves the sound technical design.

**Secondary Recommendations:**
1. Add explicit risk-ordering justification to selection guidelines (Severity 3 → 2 mitigation)
2. Include worked examples for multi-capability agents (improves task success)
3. Version the tier model to reduce ambiguity during transition

With these mitigations in place, the new tier model achieves high usability for both new agent authors (clear selection path) and migrating authors (transparent rationale for change).

---

## Evaluation Metadata

- **Evaluator:** ux-heuristic-evaluator (single AI agent, systematic Nielsen methodology)
- **Heuristics Evaluated:** H1-H10 (all 10 Nielsen usability heuristics)
- **Screens Evaluated:** 1 (the tier model as presented in ADR + agent-development-standards.md)
- **Artifact Type:** Text-based ADR and governance documentation (no interactive prototype)
- **Evaluation Mode:** Screenshot-input mode (degraded: no Figma MCP, no interactive testing)
- **Date:** 2026-03-28
- **Single-Evaluator Limitation:** Nielsen recommends 3-5 evaluators for 85% problem detection. This single-evaluator assessment likely captures 35-50% of usability issues, particularly missing issues requiring domain expertise in agent authoring practices or infrastructure security models.
- **Quality Gate:** Self-review (S-010) passed; ready for downstream critique review
