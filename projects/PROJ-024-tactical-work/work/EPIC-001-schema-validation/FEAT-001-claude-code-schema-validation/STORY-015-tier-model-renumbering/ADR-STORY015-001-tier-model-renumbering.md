# ADR-STORY015-001: Tool Security Tier Model Renumbering

> Architecture Decision Record -- Nygard format
> Criticality: C4 (irreversible governance infrastructure change affecting 89 agents)
> Quality gate: >= 0.95 weighted composite

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | Decision lifecycle state |
| [Context](#context) | Problem statement and forces |
| [Decision](#decision) | Recommended option with justification |
| [Options Considered](#options-considered) | Five options with structural analysis |
| [Evaluation Matrix](#evaluation-matrix) | 7-criteria weighted scoring |
| [Migration Plan](#migration-plan) | Per-agent tier change inventory |
| [Schema and Rule Update Plan](#schema-and-rule-update-plan) | Files requiring modification |
| [Consequences](#consequences) | Positive, negative, neutral impacts |
| [DX Considerations](#dx-considerations) | Developer ergonomics findings and mitigations |
| [Compliance](#compliance) | H-35, AE-002, constitutional alignment |

---

## Status

**Accepted** -- implemented via STORY-017 (rule files), STORY-018 (governance YAML migration), STORY-019 (documentation), STORY-020 (security verification). C4 quality gate cleared at 0.953.

---

## Context

### The Structural Gap

The Jerry Framework's tool security tier model (T1-T5) governs which tools each of 89 agents may access. The model was designed as a linear hierarchy where each tier adds capability, but T3 and T4 form parallel branches:

```
Current topology (NOT monotonic):

T1 (Read-Only) --> T2 (Read-Write) -+-> T3 (External: +Web)      -+-> T5 (Full: +Agent)
                                    |                              |
                                    +-> T4 (Persistent: +MK)  ----+
```

T5 is the only tier combining web access with persistence, but T5 also includes the Agent tool which H-35 forbids for worker agents. **An agent needing web research AND cross-session persistence has no valid tier.**

### Evidence: The Gap Is Wider Than Previously Known

Audit of all 89 governance YAMLs and .md frontmatter reveals that **5 of 7 declared-T4 agents already straddle T3+T4**:

| Agent | Declared Tier | Actual Base Tools | MCP Servers | Actual Capability |
|-------|--------------|-------------------|-------------|-------------------|
| ps-architect | T4 | Read, Write, Edit, Glob, Grep, Bash, **WebSearch, WebFetch** | **context7 + memory-keeper** | T3 + T4 |
| nse-requirements | T4 | Read, Write, Edit, Glob, Grep, Bash, **WebSearch, WebFetch** | **memory-keeper** | T3 + T4 |
| orch-planner | T4 | Read, Write, Edit, Glob, Grep, Bash, **WebSearch, WebFetch** | **memory-keeper** | T3 + T4 |
| orch-tracker | T4 | Read, Write, Edit, Glob, Grep, Bash, **WebSearch, WebFetch** | **memory-keeper** | T3 + T4 |
| orch-synthesizer | T4 | Read, Write, Edit, Glob, Grep, Bash, **WebSearch, WebFetch** | **memory-keeper** | T3 + T4 |
| ts-parser | T4 | Read, Write, Glob, Bash | **memory-keeper** | T2 + MK only |
| ts-extractor | T4 | Read, Write, Glob | **memory-keeper** | T2 + MK only |

**Key finding:** The T4 tier definition (T2 + Memory-Keeper) matches only 2 of 7 agents classified under it. The tier model is already broken in practice.

### Current Tier Distribution

| Tier | Name | Agent Count | % |
|------|------|------------|---|
| T1 | Read-Only | 4 | 4.5% |
| T2 | Read-Write | 28 | 31.5% |
| T3 | External | 49 | 55.1% |
| T4 | Persistent | 7 | 7.9% |
| T5 | Full | 1 | 1.1% |

### Forces

| # | Force | Direction |
|---|-------|-----------|
| F-01 | Every valid tool combination must have a tier (no undocumented exceptions) | Toward completeness |
| F-02 | A monotonic hierarchy is easier to reason about than a lattice | Toward linear ordering |
| F-03 | The tier model creates governance checkpoints for tool additions | Toward granularity |
| F-04 | Memory-Keeper is strictly less risky than web tools (internal MCP, no external network) | Toward placing MK before web |
| F-05 | MCP-M-001 design intent: "Memory-Keeper SHOULD be used for multi-session research" -- currently a dead letter for T3 agents | Toward broader MK access |
| F-06 | User question: "Why wouldn't we want other agents to leverage Memory-Keeper?" | Toward broader MK access |
| F-07 | The original model conflated "external + persistent" with "orchestrating" (T5 root cause) | Toward separating persistence from orchestration |
| F-08 | Migration cost should be proportional to structural improvement | Toward low-change options |

### Memory-Keeper Risk Profile

Memory-Keeper's risk profile compared to web tools is a key force in this decision:

| Dimension | Memory-Keeper | WebSearch / WebFetch |
|-----------|--------------|---------------------|
| Network access | None (internal MCP server) | Arbitrary external URLs |
| Data flow direction | Write to governed namespace | Read from unverified sources |
| Injection risk | None | Prompt injection via web content |
| Collision risk | Key namespace collisions (governed by MCP-002) | N/A |
| Citation requirement | None | Required per T3+ guardrails |
| Blast radius | One project's state | Arbitrary external data enters context |

**Conclusion:** Memory-Keeper is objectively less risky than web tools. In a monotonic hierarchy ordered by risk, persistence should precede external connectivity.

---

## Decision

**Option A: Persistent-First Linear** -- Reorder the hierarchy so Memory-Keeper enters before web tools.

### New Tier Model

| Tier | Name | New Capability | Cumulative Tools |
|------|------|---------------|-----------------|
| **T1** | Read-Only | -- | Read, Glob, Grep |
| **T2** | Read-Write | Write, Edit, Bash | T1 + Write, Edit, Bash |
| **T3** | Persistent | Memory-Keeper | T2 + Memory-Keeper |
| **T4** | Persistent + External | WebSearch, WebFetch, Context7 | T3 + WebSearch, WebFetch, Context7 |
| **T5** | Orchestration | Agent | T4 + Agent |

> **DX note (F-001 mitigation):** T4 uses compound Full Name "Persistent + External" to signal it inherits T3's Memory-Keeper capability. The Short Name form "External" is used in the agent-development-standards.md tier table (highlighting what's new at this tier). See [DX Considerations](#dx-considerations) for the naming framework.

### Structural Properties

```
New topology (monotonic):

T1 --> T2 --> T3 --> T4 --> T5
              +MK    +Web   +Agent

T1 ⊂ T2 ⊂ T3 ⊂ T4 ⊂ T5  (strict subset chain)
```

- **Monotonic:** Each tier is a strict superset of the previous. No parallel branches.
- **Complete:** Every valid tool combination has a home.
- **Risk-ordered:** Each tier adds a higher-risk capability surface than the previous.
- **H-35 compliant:** Agent tool restricted to T5 only.

### Justification

1. **Correct risk ordering.** Memory-Keeper (internal, governed namespace) is less risky than web tools (external, arbitrary URLs). Placing the lower-risk capability earlier follows the same principle as RBAC systems where internal storage precedes network access.

2. **ts-parser and ts-extractor have exact-fit tiers.** These are the only 2 agents with T2 + MK (no web). Under Option A, T3 = T2 + MK -- a perfect match. No other option provides this.

3. **Answers the structural question.** 5 of 7 current T4 agents already have web + MK. Under Option A, they naturally classify as T4 (T3 + Web = T2 + MK + Web). The gap is eliminated.

4. **Fulfills MCP-M-001 design intent.** ps-researcher (currently T3) would become T4 under this model. T4 includes MK, enabling the multi-session research persistence that MCP-M-001 recommended. The SHOULD standard gains structural backing.

5. **Preserves governance checkpoints.** Unlike Option C (4-tier), Option A maintains a checkpoint between T2 (no MK) and T3 (MK). The 28 T2 evaluation/scoring/formatting agents do NOT gain MK access without an explicit tier change.

6. **Simpler than Option E with adequate precision.** Option E (Tier+Tags) achieves perfect least privilege and superior forward compatibility, but introduces a two-dimensional governance model for 89 agents where only 8 need tags. Option A provides exact-fit tiers for the 2 persistence-only agents (ts-parser, ts-extractor) that motivated this ADR without the schema change cost or ongoing cognitive burden of a 2D model. Option E is the natural evolution path if a third orthogonal capability emerges; until then, the linear model is sufficient.

---

## Options Considered

### Option A: Persistent-First Linear (5 tiers) -- RECOMMENDED

```
T1: Read-Only --> T2: Read-Write --> T3: Persistent --> T4: External --> T5: Orchestration
                                     (+MK)              (+Web)           (+Agent)
```

| Aspect | Assessment |
|--------|-----------|
| Monotonic | Yes -- strict T1 ⊂ T2 ⊂ T3 ⊂ T4 ⊂ T5 |
| Gap solved | Yes -- every tool combo has a home |
| ts-parser/extractor fit | Perfect -- T3 = T2 + MK |
| T3+T4 agents fit | Perfect -- T4 = T3 + Web = T2 + MK + Web |
| Migration cost | 51 governance YAML changes (mechanical find-replace) |
| Governance impact | T2 agents need explicit tier change to get MK (checkpoint preserved) |

**Key trade-off:** 49 current-T3 agents reclassify to T4. Their tier number increases, which could be perceived as "less secure" even though their actual tool access doesn't change. Mitigation: clear documentation that T4 (External) in the new model corresponds to T3 (External) in the old model -- the capability set is identical; only the number changes.

### Option B: External-First Linear (5 tiers)

```
T1: Read-Only --> T2: Read-Write --> T3: External --> T4: Extended --> T5: Orchestration
                                     (+Web)           (+MK)            (+Agent)
```

| Aspect | Assessment |
|--------|-----------|
| Monotonic | Yes |
| Gap solved | Partially -- T2+MK combination has no tier |
| ts-parser/extractor fit | **Poor** -- T4 = T3+MK = T2+Web+MK (gets web tools they don't use) |
| Migration cost | 0-2 governance YAML changes (lowest) |
| Governance impact | MK checkpoint preserved (T4+) |

**Decisive weakness:** ts-parser and ts-extractor genuinely need {T2 tools + MK, without web}. Under Option B, they must either: (a) accept T4 with unwanted web tools, or (b) drop to T2 and lose Memory-Keeper. Neither is correct. This recreates the SAME category of problem (no exact-fit tier for a valid tool combination) that motivates this ADR.

### Option C: Consolidated (4 tiers)

```
T1: Read-Only --> T2: Read-Write (+MK) --> T3: External (+Web) --> T4: Orchestration (+Agent)
```

| Aspect | Assessment |
|--------|-----------|
| Monotonic | Yes |
| Gap solved | Yes -- MK universal at T2+ |
| ts-parser/extractor fit | Good -- T2 now includes MK |
| Migration cost | 8 governance YAML changes |
| Governance impact | **MK governance checkpoint eliminated** -- all 77 T2+ agents gain MK ceiling |

**Key trade-off:** Simplest model (4 tiers) but most aggressive permission expansion. The 28 current-T2 agents (evaluation, scoring, formatting, validation) gain Memory-Keeper as a tier-level permission. While "having access != using it" is true at runtime, the tier model exists to create governance checkpoints that runtime enforcement alone does not provide. Eliminating the MK checkpoint means any T2+ agent can add `mcpServers: memory-keeper: true` in a PR without triggering a tier-change review.

**When to reconsider:** If future experience shows that MK tier-change reviews are always rubber-stamped (zero rejections), Option C's checkpoint elimination becomes a formality worth removing. Current data is insufficient to make that determination.

### Option D: Lattice with Merge (6 tiers)

```
T1 --> T2 --> T3: External (+Web)
           \-> T4: Persistent (+MK) --> T5: Extended (T3 U T4) --> T6: Orchestration (+Agent)
```

| Aspect | Assessment |
|--------|-----------|
| Monotonic | **No** -- T3 and T4 are parallel (T3 ⊄ T4, T4 ⊄ T3) |
| Gap solved | Yes -- T5 = T3 ∪ T4 provides the merge point |
| ts-parser/extractor fit | Perfect -- T4 = T2 + MK |
| Migration cost | 6 governance YAML changes |
| Governance impact | Most granular -- every capability set has its own tier |

**Decisive weakness:** Non-monotonic topology reproduces the structural complexity that caused the original gap. "T4 is not higher than T3; they're different directions" is precisely the cognitive model that the current T3/T4 split creates and that agent authors find confusing. This ADR exists because parallel branches are inherently harder to reason about than linear chains.

### Option E: Tier + Tags Hybrid (3 base tiers + orthogonal capability flags)

```
Base Tiers (linear):
  T1: Read-Only --> T2: Read-Write --> T3: External
                                       (+Web)

Capability Tags (orthogonal, independent of base tier):
  +persistent    Memory-Keeper access (requires MCP-002 key namespace)
  +delegate      Agent tool access (restricted to orchestrator agents per H-35)
```

> Source: `research/industry-tier-patterns.md`. This option was identified by the industry research phase and is precedented by Linux capabilities (base user model + CAP_* flags), Deno (deny-all + --allow-* flags), and emerging AI agent frameworks (MiniScope, FINOS).

| Aspect | Assessment |
|--------|-----------|
| Monotonic | Partial -- base tiers are monotonic (T1 ⊂ T2 ⊂ T3), but tags create orthogonal dimensions outside the linear chain |
| Gap solved | Yes -- every tool combination has an exact representation via base tier + applicable tags |
| ts-parser/extractor fit | Perfect -- T2 + `+persistent` describes their exact tool set |
| T3+T4 agents fit | Perfect -- T3 + `+persistent` describes ps-architect's exact tool set |
| Migration cost | 7 governance YAML changes + **schema change required** (new `capability_tags` array field in agent-governance-v1.schema.json) |
| Governance impact | Most precise per-agent control -- tags are individually governed; but introduces a second governance axis (tier + tags) that all 89 agent definitions must accommodate |

**How the five representative agents land:**

| Agent | Current | New Base | Tags | What Changed |
|-------|---------|----------|------|-------------|
| pe-scorer | T1 | T1 | (none) | Nothing |
| ps-critic | T2 | T2 | (none) | Nothing |
| eng-backend | T3 | T3 | (none) | Nothing |
| ts-parser | T4 | **T2** | **+persistent** | Base tier reflects actual tools. Tag adds MK. |
| ps-architect | T4 | **T3** | **+persistent** | Base tier reflects web tools. Tag adds MK. |
| ux-orchestrator | T5 | **T3** | **+delegate** | Base tier reflects tools. Tag adds Agent tool. |

**Key trade-off:** Option E decomposes the partially-ordered capability set into a product of a total order (base tier T1-T3) and a set of independent boolean dimensions (tags). This is the standard approach in capability-based security systems. However, it introduces a two-dimensional governance model for 89 agents where only 7 (8%) currently need the `+persistent` tag and 1 needs `+delegate`. The schema change (new `capability_tags` array field) cascades to validation logic, agent definition templates, CI schema checks, and documentation -- substantial machinery for a narrow current use case. (Scan confirmation: `capability_tags` is absent from the current `agent-governance-v1.schema.json` and is not referenced in any `.context/rules/` file; implementing Option E requires creating this infrastructure from scratch.)

**When to reconsider:** When the number of cross-cutting capabilities grows beyond 2. If a third orthogonal dimension emerges (e.g., a new MCP server that doesn't fit the linear chain), the Tier+Tags model accommodates it without restructuring. The linear models (A, B, C) would need another renumbering.

---

## Evaluation Matrix

### Criteria and Weights

| # | Criterion | Weight | What It Measures |
|---|-----------|--------|-----------------|
| 1 | Simplicity | 15% | How easy to understand and remember |
| 2 | Completeness | 20% | Whether every valid tool combination has a tier |
| 3 | Monotonicity | 15% | Whether each tier strictly adds capability over the previous |
| 4 | Migration cost | 10% | Number of governance YAMLs requiring update |
| 5 | Principle of least privilege | 15% | Whether the model encourages minimal tool access |
| 6 | Forward compatibility | 10% | Whether new tools/MCP servers can be added without restructuring |
| 7 | H-35 compliance | 15% | Whether the Agent tool remains restricted to the highest tier |

**Weight derivation:** Criteria are grouped into three priority bands based on the decision's nature (governance infrastructure restructuring):

- **Band 1 (20%):** Completeness — the primary motivation for this ADR is eliminating the structural gap. If the new model doesn't achieve completeness, the restructuring is unjustified.
- **Band 2 (15% each, 4 criteria):** Simplicity, Monotonicity, Least Privilege, and H-35 Compliance — these represent the four design principles of the tier model as stated in `agent-development-standards.md` ("Always select the lowest tier that satisfies requirements" = least privilege; "Each tier strictly adds capability" = monotonicity; H-35 = constitutional constraint).
- **Band 3 (10% each, 2 criteria):** Migration Cost and Forward Compatibility — implementation concerns that should inform but not drive an architectural decision. Migration cost is a one-time effort; forward compatibility is speculative.

### Scoring (1-10 scale)

| Criterion | Wt | A: Persistent-First | B: External-First | C: Consolidated | D: Lattice | E: Tier+Tags |
|-----------|----|--------------------|--------------------|----------------|-----------|--------------|
| 1. Simplicity | 15% | 8 | 8 | 10 | 4 | 5 |
| 2. Completeness | 20% | 10 | 6 | 10 | 10 | 10 |
| 3. Monotonicity | 15% | 10 | 10 | 10 | 4 | 7 |
| 4. Migration cost | 10% | 4 | 10 | 8 | 9 | 7 |
| 5. Least privilege | 15% | 7 | 7 | 4 | 10 | 10 |
| 6. Forward compat | 10% | 8 | 7 | 6 | 9 | 10 |
| 7. H-35 compliance | 15% | 10 | 10 | 10 | 10 | 8 |

### Score Justifications

**Criterion 2 (Completeness) -- Option B scored 6:** The "T2 + MK" combination (ts-parser, ts-extractor) has no exact-fit tier. These agents must either accept over-provisioned T4 (with unwanted web tools) or drop to T2 (losing MK). This is the same category of gap this ADR addresses.

**Criterion 3 (Monotonicity) -- Option D scored 4:** Parallel T3/T4 branches mean T3 ⊄ T4 and T4 ⊄ T3. Agent authors must understand "T4 is not higher than T3" -- the same cognitive burden as the current model.

**Criterion 5 (Least Privilege) -- Option A scored 7:** 49 agents reclassified from T3 to T4 gain MK as a tier-level ceiling. However, their .md frontmatter (the actual enforcement mechanism) doesn't change. The tier creates a permission ceiling, not an active grant. MK can be added via .md without a tier change, but the .md PR remains a review checkpoint.

**Criterion 5 (Least Privilege) -- Option C scored 4:** ALL 77 T2+ agents gain MK ceiling. The governance checkpoint between "can write files" and "can persist cross-session state" is eliminated entirely.

**Criterion 1 (Simplicity) -- Option E scored 5:** Introduces a two-dimensional governance model (base tier + capability tags). Agent authors must understand both axes and their interaction. The `capability_tags` schema field adds a new dimension to CI validation, agent templates, and documentation. For 89 agents where only 8 need tags (7 `+persistent`, 1 `+delegate`), this is substantial machinery for a narrow use case.

**Criterion 3 (Monotonicity) -- Option E scored 7:** Base tiers (T1 ⊂ T2 ⊂ T3) are strictly monotonic. However, the overall model is a product space, not a total order: a T2+persistent agent has more capability than a plain T3 agent. The "higher number = strictly more capability" mental model only holds within the base tier dimension.

**Criterion 4 (Migration cost) -- Option E scored 7:** Fewer YAML changes (7) than Options A (51) or C (8), but requires a schema change (new `capability_tags` array field in agent-governance-v1.schema.json). Schema changes cascade to CI validation logic, agent definition templates, and documentation. The one-time migration is moderate; the ongoing schema maintenance is the hidden cost.

**Criterion 7 (H-35 compliance) -- Option E scored 8:** Compliant via `+delegate` tag replacing T5 tier. However, this shifts the enforcement model from tier-number-based ("only T5 has Agent") to tag-presence-based ("only +delegate has Agent"). Requires updating H-35 enforcement logic, L2-REINJECT markers, and CI gates. Not a compliance gap, but an enforcement model change with cascading governance updates.

### Weighted Totals

| Option | Calculation | Total |
|--------|------------|-------|
| **A: Persistent-First** | 1.20 + 2.00 + 1.50 + 0.40 + 1.05 + 0.80 + 1.50 | **8.45** |
| B: External-First | 1.20 + 1.20 + 1.50 + 1.00 + 1.05 + 0.70 + 1.50 | **8.15** |
| C: Consolidated | 1.50 + 2.00 + 1.50 + 0.80 + 0.60 + 0.60 + 1.50 | **8.50** |
| D: Lattice | 0.60 + 2.00 + 0.60 + 0.90 + 1.50 + 0.90 + 1.50 | **8.00** |
| E: Tier+Tags | 0.75 + 2.00 + 1.05 + 0.70 + 1.50 + 1.00 + 1.20 | **8.20** |

**Ranking:** C (8.50) > A (8.45) > E (8.20) > B (8.15) > D (8.00)

### Sensitivity Analysis

Option C edges ahead of A by 0.05 points, driven by Simplicity (10 vs 8) and Migration cost (8 vs 4). However, C scores **4** on Least Privilege (the lowest score in the matrix for any recommended option). The margin is narrow enough that the qualitative least-privilege concern tips the recommendation to Option A.

**Sensitivity test 1 — Governance-weighted** (Least Privilege: 15%→20%, Simplicity: 15%→10%):
- A: (8×0.10) + (10×0.20) + (10×0.15) + (4×0.10) + (7×0.20) + (8×0.10) + (10×0.15) = 0.80 + 2.00 + 1.50 + 0.40 + 1.40 + 0.80 + 1.50 = **8.40**
- C: (10×0.10) + (10×0.20) + (10×0.15) + (8×0.10) + (4×0.20) + (6×0.10) + (10×0.15) = 1.00 + 2.00 + 1.50 + 0.80 + 0.80 + 0.60 + 1.50 = **8.20**
- E: (5×0.10) + (10×0.20) + (7×0.15) + (7×0.10) + (10×0.20) + (10×0.10) + (8×0.15) = 0.50 + 2.00 + 1.05 + 0.70 + 2.00 + 1.00 + 1.20 = **8.45**

**Sensitivity test 2 — Migration-weighted** (Migration Cost: 10%→20%, Completeness: 20%→10%):
- A: (8×0.15) + (10×0.10) + (10×0.15) + (4×0.20) + (7×0.15) + (8×0.10) + (10×0.15) = 1.20 + 1.00 + 1.50 + 0.80 + 1.05 + 0.80 + 1.50 = **7.85**
- C: (10×0.15) + (10×0.10) + (10×0.15) + (8×0.20) + (4×0.15) + (6×0.10) + (10×0.15) = 1.50 + 1.00 + 1.50 + 1.60 + 0.60 + 0.60 + 1.50 = **8.30**
- E: (5×0.15) + (10×0.10) + (7×0.15) + (7×0.20) + (10×0.15) + (10×0.10) + (8×0.15) = 0.75 + 1.00 + 1.05 + 1.40 + 1.50 + 1.00 + 1.20 = **7.90**

| Scenario | A | C | E | Winner | Margin |
|----------|---|---|---|--------|--------|
| Nominal | 8.45 | 8.50 | 8.20 | C | 0.05 (C over A) |
| Governance-weighted | 8.40 | 8.20 | 8.45 | E | 0.05 (E over A) |
| Migration-weighted | 7.85 | 8.30 | 7.90 | C | 0.40 (C over E) |

**Interpretation:** Option E scores highest in the governance-weighted scenario (8.45) due to its perfect Least Privilege (10) and Forward Compatibility (10) scores. However, the 0.05-point margin over Option A is within scoring uncertainty -- a single criterion shifting by 1 point reverses the ranking. Option A wins the governance-weighted scenario when accounting for three factors not fully captured by the quantitative criteria:

1. **Schema change risk is underweighted by Criterion 4.** Option E's `capability_tags` field requires a new schema dimension in `agent-governance-v1.schema.json`, cascading to CI validation logic, agent definition templates, and documentation. The Migration Cost criterion scores one-time file changes but not the ongoing schema maintenance burden.

2. **Two-dimensional complexity is an ongoing cost, not a one-time cost.** Simplicity (Criterion 1) scores the model at a point in time, but every future agent definition, review, and audit must reason about two governance axes. For 89 agents where only 8 need tags, the 2D model creates a permanent cognitive overhead that serves a narrow population.

3. **Option E's governance-weighted advantage comes entirely from Least Privilege (10 vs 7) and Forward Compatibility (10 vs 8).** The Least Privilege advantage assumes tags are individually governed -- but no tag governance mechanism exists today: `agent-governance-v1.schema.json` has no `capability_tags` field, `agent-development-standards.md` defines no tag review process, and no CI gate validates tag assignments. Option A's governance checkpoint (tier-change review for MK access) is a proven mechanism backed by existing schema validation and L5 CI enforcement; Option E's tag governance is a design promise requiring new infrastructure.

Option C wins on nominal weights (barely) and when migration cost is emphasized. Given this is a C4 decision modifying governance infrastructure per AE-002, the governance-weighted scenario is the most appropriate weighting -- but the qualitative factors above tip the decision to Option A over the quantitatively-superior Option E.

**Final ranking (governance-weighted, qualitative adjustment): A (8.40 + qualitative) > E (8.45 nominal) > C (8.20) > B (8.15 nominal) > D (8.00 nominal)**

**Recommendation: Option A (Persistent-First Linear)**

---

## Migration Plan

### Tier Reclassification Summary

| Current Tier | New Tier | Agent Count | Change Type |
|-------------|---------|------------|-------------|
| T1 (Read-Only) | T1 (Read-Only) | 4 | Unchanged |
| T2 (Read-Write) | T2 (Read-Write) | 28 | Unchanged |
| T3 (External) | **T4 (External)** | 49 | Number change only (T3 -> T4) |
| T4 (Persistent, pure MK) | **T3 (Persistent)** | 2 | Number change (T4 -> T3) |
| T4 (Persistent, MK+Web) | **T4 (External)** | 5 | Unchanged number, new meaning |
| T5 (Full) | **T5 (Orchestration)** | 1 | Unchanged number, renamed |

**Total governance YAML changes:** 51 files (49 T3->T4 + 2 T4->T3)
**Total .md frontmatter changes:** 0 files (tool lists and mcpServers are unchanged)

### Per-Agent Migration Table

#### T1 -> T1 (unchanged, 4 agents)

| Agent | Current Tools | New Tier | Action |
|-------|-------------|---------|--------|
| diataxis-classifier | Read, Glob, Grep | T1 | None |
| diataxis-auditor | Read, Glob, Grep | T1 | None |
| pe-scorer | Read, Glob, Grep | T1 | None |
| sb-voice | Read, Glob, Grep | T1 | None |

#### T2 -> T2 (unchanged, 28 agents)

| Agent | New Tier | Action |
|-------|---------|--------|
| adv-scorer | T2 | None |
| adv-selector | T2 | None |
| cd-generator | T2 | None |
| cd-validator | T2 | None |
| diataxis-howto | T2 | None |
| diataxis-reference | T2 | None |
| diataxis-tutorial | T2 | None |
| nse-qa | T2 | None |
| pe-builder | T2 | None |
| pe-constraint-gen | T2 | None |
| ps-critic | T2 | None |
| ps-reporter | T2 | None |
| ps-reviewer | T2 | None |
| ps-validator | T2 | None |
| sb-calibrator | T2 | None |
| sb-reviewer | T2 | None |
| sb-rewriter | T2 | None |
| tspec-analyst | T2 | None |
| tspec-generator | T2 | None |
| ts-formatter | T2 | None |
| ts-mindmap-ascii | T2 | None |
| ts-mindmap-mermaid | T2 | None |
| uc-author | T2 | None |
| uc-slicer | T2 | None |
| ux-behavior-diagnostician | T2 | None |
| wt-auditor | T2 | None |
| wt-verifier | T2 | None |
| wt-visualizer | T2 | None |

#### T3 -> T4 (49 agents, governance YAML: `tool_tier: T3` -> `tool_tier: T4`)

| Agent | Current MCP | New Tier | Note |
|-------|-----------|---------|------|
| adv-executor | context7 | T4 | Has Context7, gains MK ceiling |
| diataxis-explanation | -- | T4 | Web access only |
| eng-architect | context7 | T4 | Has Context7 |
| eng-backend | context7 | T4 | Has Context7 |
| eng-devsecops | context7 | T4 | Has Context7 |
| eng-frontend | context7 | T4 | Has Context7 |
| eng-incident | context7 | T4 | Has Context7 |
| eng-infra | context7 | T4 | Has Context7 |
| eng-lead | context7 | T4 | Has Context7 |
| eng-qa | context7 | T4 | Has Context7 |
| eng-reviewer | context7 | T4 | Has Context7 |
| eng-security | context7 | T4 | Has Context7 |
| nse-architecture | context7 | T4 | Has Context7 |
| nse-configuration | -- | T4 | Web access only |
| nse-explorer | context7 | T4 | Has Context7 |
| nse-integration | -- | T4 | Web access only |
| nse-reporter | -- | T4 | Web access only |
| nse-reviewer | -- | T4 | Web access only |
| nse-risk | -- | T4 | Web access only |
| nse-verification | -- | T4 | Web access only |
| pm-business-analyst | -- | T4 | WebSearch only |
| pm-competitive-analyst | -- | T4 | WebSearch only |
| pm-customer-insight | context7 | T4 | Has Context7 |
| pm-market-strategist | context7 | T4 | Has Context7 |
| pm-product-strategist | -- | T4 | WebSearch only |
| ps-analyst | context7 | T4 | Has Context7 |
| ps-investigator | context7 | T4 | Has Context7 |
| ps-researcher | context7 | T4 | Has Context7; primary MCP-M-001 target |
| ps-synthesizer | context7 | T4 | Has Context7 |
| red-exfil | -- | T4 | Web access only |
| red-exploit | -- | T4 | Web access only |
| red-infra | -- | T4 | Web access only |
| red-lateral | -- | T4 | Web access only |
| red-lead | context7 | T4 | Has Context7 |
| red-persist | -- | T4 | Web access only |
| red-privesc | -- | T4 | Web access only |
| red-recon | context7 | T4 | Has Context7 |
| red-reporter | context7 | T4 | Has Context7 |
| red-social | -- | T4 | Web access only |
| red-vuln | context7 | T4 | Has Context7 |
| ux-ai-design-guide | -- | T4 | Web access only |
| ux-atomic-architect | -- | T4 | Web access only |
| ux-heart-analyst | -- | T4 | Web access only |
| ux-heuristic-evaluator | -- | T4 | Web access only |
| ux-inclusive-evaluator | -- | T4 | Web access only |
| ux-jtbd-analyst | -- | T4 | Web access only |
| ux-kano-analyst | -- | T4 | Web access only |
| ux-lean-ux-facilitator | -- | T4 | Web access only |
| ux-sprint-facilitator | -- | T4 | Web access only |

#### T4 -> T3 (2 agents, governance YAML: `tool_tier: T4` -> `tool_tier: T3`)

| Agent | Tools | MCP | New Tier | Note |
|-------|-------|-----|---------|------|
| ts-parser | Read, Write, Glob, Bash | memory-keeper | **T3** | Perfect fit: T2 + MK |
| ts-extractor | Read, Write, Glob | memory-keeper | **T3** | Perfect fit: T2 + MK |

#### T4 -> T4 (5 agents, no file change needed -- number stays T4, meaning changes)

| Agent | Tools | MCP | New Tier | Note |
|-------|-------|-----|---------|------|
| ps-architect | T2 + Web | context7 + memory-keeper | T4 | Already T3+T4; new T4 = T3+Web is exact fit |
| nse-requirements | T2 + Web | memory-keeper | T4 | Already T3+T4; exact fit |
| orch-planner | T2 + Web | memory-keeper | T4 | Already T3+T4; exact fit |
| orch-tracker | T2 + Web | memory-keeper | T4 | Already T3+T4; exact fit |
| orch-synthesizer | T2 + Web | memory-keeper | T4 | Already T3+T4; exact fit |

#### T5 -> T5 (1 agent, no file change)

| Agent | New Tier | Note |
|-------|---------|------|
| ux-orchestrator | T5 | Renamed from "Full" to "Orchestration" |

### Migration Execution

The migration is mechanical and can be executed as a single PR. The script handles both quoted (`tool_tier: "T3"`) and unquoted (`tool_tier: T3`) YAML values, as 5 pm-pmm governance YAMLs use the quoted form.

```bash
# Step 0: Pre-migration snapshot (verification baseline)
echo "=== PRE-MIGRATION COUNTS ==="
echo "T1: $(grep -rl 'tool_tier:.*T1' skills/*/agents/*.governance.yaml | wc -l)"
echo "T2: $(grep -rl 'tool_tier:.*T2' skills/*/agents/*.governance.yaml | wc -l)"
echo "T3: $(grep -rl 'tool_tier:.*T3' skills/*/agents/*.governance.yaml | wc -l)"
echo "T4: $(grep -rl 'tool_tier:.*T4' skills/*/agents/*.governance.yaml | wc -l)"
echo "T5: $(grep -rl 'tool_tier:.*T5' skills/*/agents/*.governance.yaml | wc -l)"
# Expected: T1=4, T2=28, T3=49, T4=7, T5=1

# Step 0b: Pre-migration Memory-Keeper audit
# Verify no T3 agent already declares memory-keeper (would indicate existing governance anomaly)
echo "=== T3 AGENTS WITH MEMORY-KEEPER (should be empty) ==="
grep -rl 'memory-keeper' skills/*/agents/*.md | while read f; do
  if grep -q 'tool_tier:.*T3' "${f%.md}.governance.yaml" 2>/dev/null; then echo "ANOMALY: $f"; fi
done
# Expected: no output. Any hits require investigation before migration.

# Step 1: Protect ts-parser and ts-extractor from Step 2 by renaming to T3_HOLD
sed -i '' 's/tool_tier: T4/tool_tier: T3_HOLD/' skills/transcript/agents/ts-parser.governance.yaml
sed -i '' 's/tool_tier: T4/tool_tier: T3_HOLD/' skills/transcript/agents/ts-extractor.governance.yaml

# Step 2: Rename T3 -> T4 in all governance YAMLs (handles both quoted and unquoted)
for file in $(grep -rl 'tool_tier:.*T3' skills/*/agents/*.governance.yaml); do
  sed -i '' 's/tool_tier: T3$/tool_tier: T4/' "$file"       # unquoted
  sed -i '' 's/tool_tier: "T3"$/tool_tier: "T4"/' "$file"   # quoted
done

# Step 3: Finalize ts-parser and ts-extractor (T3_HOLD -> T3)
sed -i '' 's/tool_tier: T3_HOLD/tool_tier: T3/' skills/transcript/agents/ts-parser.governance.yaml
sed -i '' 's/tool_tier: T3_HOLD/tool_tier: T3/' skills/transcript/agents/ts-extractor.governance.yaml

# Step 4: Post-migration verification
echo "=== POST-MIGRATION COUNTS ==="
echo "T1: $(grep -rl 'tool_tier:.*T1' skills/*/agents/*.governance.yaml | wc -l)"
echo "T2: $(grep -rl 'tool_tier:.*T2' skills/*/agents/*.governance.yaml | wc -l)"
echo "T3: $(grep -rl 'tool_tier:.*T3' skills/*/agents/*.governance.yaml | wc -l)"
echo "T4: $(grep -rl 'tool_tier:.*T4' skills/*/agents/*.governance.yaml | wc -l)"
echo "T5: $(grep -rl 'tool_tier:.*T5' skills/*/agents/*.governance.yaml | wc -l)"
# Expected: T1=4, T2=28, T3=2, T4=54, T5=1

# Step 5: Verify T3 agents are exactly ts-parser and ts-extractor
echo "=== T3 AGENTS (should be exactly 2: ts-parser, ts-extractor) ==="
grep -rl 'tool_tier:.*T3' skills/*/agents/*.governance.yaml
```

**Three-step protection pattern:** Step 1 moves ts-parser and ts-extractor to a temporary value (T3_HOLD) to prevent them from being caught by the T3→T4 rename in Step 2. Step 3 finalizes them to their correct new tier (T3). This eliminates the ordering dependency risk.

### Rollback Procedure

If the migration needs to be reverted after execution:

```bash
# Rollback Step 1: Protect ts-parser and ts-extractor
sed -i '' 's/tool_tier: T3/tool_tier: T4_HOLD/' skills/transcript/agents/ts-parser.governance.yaml
sed -i '' 's/tool_tier: T3/tool_tier: T4_HOLD/' skills/transcript/agents/ts-extractor.governance.yaml

# Rollback Step 2: Rename T4 -> T3 in all governance YAMLs
# Note: grep 'tool_tier:.*T4' will include T4_HOLD files in the file list,
# but sed 's/tool_tier: T4$/...' uses end-of-line anchors so T4_HOLD lines
# will NOT match (they end in "T4_HOLD", not "T4"). This is safe by design.
for file in $(grep -rl 'tool_tier:.*T4' skills/*/agents/*.governance.yaml); do
  sed -i '' 's/tool_tier: T4$/tool_tier: T3/' "$file"
  sed -i '' 's/tool_tier: "T4"$/tool_tier: "T3"/' "$file"
done

# Rollback Step 3: Finalize ts-parser and ts-extractor
sed -i '' 's/tool_tier: T4_HOLD/tool_tier: T4/' skills/transcript/agents/ts-parser.governance.yaml
sed -i '' 's/tool_tier: T4_HOLD/tool_tier: T4/' skills/transcript/agents/ts-extractor.governance.yaml
```

### Post-Migration Verification Checklist

| Check | Command | Expected Result |
|-------|---------|----------------|
| T1 count | `grep -rl 'tool_tier:.*T1' skills/*/agents/*.governance.yaml \| wc -l` | 4 |
| T2 count | `grep -rl 'tool_tier:.*T2' skills/*/agents/*.governance.yaml \| wc -l` | 28 |
| T3 count | `grep -rl 'tool_tier:.*T3' skills/*/agents/*.governance.yaml \| wc -l` | 2 |
| T4 count | `grep -rl 'tool_tier:.*T4' skills/*/agents/*.governance.yaml \| wc -l` | 54 |
| T5 count | `grep -rl 'tool_tier:.*T5' skills/*/agents/*.governance.yaml \| wc -l` | 1 |
| T3 agents | `grep -rl 'tool_tier:.*T3' skills/*/agents/*.governance.yaml` | ts-parser.governance.yaml, ts-extractor.governance.yaml only |
| No T3_HOLD | `grep -rl 'T3_HOLD' skills/*/agents/*.governance.yaml` | (empty) |
| Total | Sum of T1+T2+T3+T4+T5 | 89 |

> **Scope note:** The migration script covers `skills/*/agents/*.governance.yaml` (89 files). Two additional pm-pmm draft governance YAMLs exist in the pm-pmm skill development project -- these are development drafts, not active agent definitions, and are excluded from the migration scope. They should be updated manually if/when they are promoted to `skills/`.

---

## Schema and Rule Update Plan

### Files Requiring Modification

| File | Change | Priority |
|------|--------|---------|
| `docs/schemas/agent-governance-v1.schema.json` | Update `tool_tier` enum: keep T1-T5 values unchanged (no schema change needed since enum values T1-T5 are the same) | P0 |
| `.context/rules/agent-development-standards.md` | Rewrite Tool Security Tiers table with new ordering; update tier descriptions, selection guidelines, tier constraints | P0 |
| `.context/rules/mcp-tool-standards.md` | Update MK namespace constraint wording (Change 1), MCP-M-001 text (Change 2), exclusion notes (Change 4). No matrix row changes needed (Change 3). See [mcp-tool-standards.md P0 Draft](#rule-file-update-mcp-tool-standardsmd-p0-draft). | P0 |
| 51 governance YAML files | `tool_tier` field update per Migration Plan | P0 |
| `.context/rules/quality-enforcement.md` | No change needed (tier model not referenced by tier number) | -- |
| `.context/rules/agent-routing-standards.md` | No change needed (routing is keyword-based, not tier-based) | -- |
| `docs/schemas/agent-governance-v1.schema.json` | Tool_tier enum values T1-T5 are unchanged; tier NAMES change but schema uses T-numbers | -- |
| `skills/*/SKILL.md` files | Grep for T3/T4 tier references; update any that reference tier meanings | P1 |
| `AGENTS.md` | Update any tier-number references in agent registry | P1 |

**Scope verification:** A grep for tier references across rule files confirms the change boundary:
- `.context/rules/agent-development-standards.md`: 30 lines with tier references (`grep -c 'T[1-5]' .context/rules/agent-development-standards.md`) — **P0 rewrite** (tier table, selection guidelines, constraints, cognitive mode table, guardrail selection table)
- `.context/rules/mcp-tool-standards.md`: 1 direct tier reference (`grep -c 'T[1-5]' .context/rules/mcp-tool-standards.md`), plus narrative text referencing tier concepts without tier numbers — **P0 update** (exclusion notes, key namespace rule wording, MCP-M-001 text; see [mcp-tool-standards.md P0 Draft](#rule-file-update-mcp-tool-standardsmd-p0-draft) for specific changes)
- `.context/rules/quality-enforcement.md`: References "T1-T5 tier model" generically — no change needed (meaning-independent)
- `.context/rules/agent-routing-standards.md`: References "T1-T5" in tool overload prevention — no change needed (count-based, not meaning-based)
- `skills/*/SKILL.md`: May contain tier references in agent descriptions — **P1 sweep**

### Schema Update Detail

The `agent-governance-v1.schema.json` `tool_tier` enum currently accepts: `T1`, `T2`, `T3`, `T4`, `T5`. Under the new model, these same values are used with different meanings:

| Value | Old Meaning | New Meaning |
|-------|------------|------------|
| T1 | Read-Only | Read-Only (unchanged) |
| T2 | Read-Write | Read-Write (unchanged) |
| T3 | External | **Persistent** (T2 + Memory-Keeper) |
| T4 | Persistent | **External** (T3 + WebSearch, WebFetch, Context7) |
| T5 | Full | **Orchestration** (T4 + Agent) |

**Schema file change: None required.** The enum values are the same; the semantic mapping changes in the documentation only.

### Rule File Update: agent-development-standards.md

The Tool Security Tiers section must be rewritten:

**New tier table:**

> **Naming convention:** The `Name` column below uses Short Name form. T4's Short Name is "External" (what's new at this tier); the compound Full Name "Persistent + External" (cumulative capability) is used in DX communication contexts. See [DX Considerations](#dx-considerations) for the Short Name / Full Name framework.

| Tier | Name | Tools Included | Use Case | Example Agents |
|------|------|---------------|----------|----------------|
| **T1** | Read-Only | Read, Glob, Grep | Evaluation, auditing, scoring | adv-scorer, pe-scorer |
| **T2** | Read-Write | T1 + Write, Edit, Bash | Analysis, document production, code generation | ps-critic, wt-auditor, uc-author |
| **T3** | Persistent | T2 + Memory-Keeper | Cross-session state: research caching, phase checkpointing, transcript persistence | ts-parser, ts-extractor |
| **T4** | External | T3 + WebSearch, WebFetch, Context7 | Research, exploration, external documentation, cross-session research | ps-researcher, eng-architect, red-recon |
| **T5** | Orchestration | T4 + Agent | Orchestration with delegation, full capability | ux-orchestrator |

**New selection guidelines:**

1. **Default to T1.** If an agent only reads and evaluates, T1 is sufficient.
2. **T2 when the agent produces artifacts.** Writing files requires T2 minimum.
3. **T3 when cross-session persistence is needed.** Agents doing multi-session work (research spikes, phase checkpointing, transcript persistence) need T3. T3 agents MUST follow the MCP key namespace: `jerry/{project}/{entity-type}/{entity-id}`.
4. **T4 when external information is needed.** T4 agents MUST include citation guardrails in `guardrails.output_filtering`. T4 includes Memory-Keeper (T3 is a subset).
5. **T5 requires explicit justification.** The Agent tool enables delegation; every T5 assignment MUST document why delegation is necessary.

**New tier constraints:**

| Constraint | Rationale |
|------------|-----------|
| Worker agents MUST NOT be T5 (no Agent tool) | Enforces H-01 single-level nesting |
| T3+ agents with Memory-Keeper MUST follow MCP key namespace | Prevents key collision across sessions |
| T4+ agents MUST declare citation guardrails | External data requires source attribution |
| Monitor per-agent tool count; alert at 15 tools | Tool selection accuracy degrades beyond 15 |

### Rule File Update: mcp-tool-standards.md (P0 Draft)

The following changes apply to `mcp-tool-standards.md`:

**1. Tier Constraints table update** (currently in agent-development-standards.md, cross-referenced from mcp-tool-standards.md):

Replace: `"T4+ agents MUST follow MCP key namespace: jerry/{project}/{entity-type}/{entity-id}"`
With: `"T3+ agents with Memory-Keeper MUST follow MCP key namespace: jerry/{project}/{entity-type}/{entity-id}"`

Rationale: Under the new model, T3 (Persistent) is the first tier with Memory-Keeper. The key namespace requirement must apply from T3, not T4.

**2. MCP-M-001 reference update:**

Replace: `"Memory-Keeper SHOULD be used for multi-session research that produces reusable findings."`
With: `"Memory-Keeper SHOULD be used for multi-session research that produces reusable findings. T4 (Persistent + External) agents are the primary target of this standard; T3 (Persistent) agents may also use Memory-Keeper for cross-session state management."`

**3. Agent Integration Matrix — no row changes needed.**

The matrix shows tool assignments per agent (Context7 columns, Memory-Keeper columns), not tier numbers. The single T[1-5] match in `mcp-tool-standards.md` (confirmed at 1 match per scope verification at line 548) is in the exclusion notes section ("T3 tools"), not in the matrix table rows. Tier reclassifications are reflected in governance YAML `tool_tier` fields, not in the matrix.

The only matrix-adjacent change: the MK namespace constraint text *above* the matrix is updated in Change 1 ("T3+ agents with Memory-Keeper MUST follow MCP key namespace").

**4. "Not included" exclusion notes:**

Add to the eng-* and red-* exclusion note: `"These agents are T4 (Persistent + External) under the new tier model but MUST NOT use Memory-Keeper. File-based persistence per P-002 (engagement-scoped output) remains the correct mechanism. The T4 tier permits MK as a ceiling; the .md frontmatter and this exclusion note prevent actual MK access."`

---

## Consequences

### Positive

1. **Every tool combination has a home.** The T3/T4 parallel branch gap is eliminated. No agent needs undocumented exceptions.
2. **Risk-ordered hierarchy.** The tier model now correctly reflects that internal persistence (MK) is less risky than external connectivity (web).
3. **MCP-M-001 gains structural backing.** T4 agents (which include all research agents) have Memory-Keeper available via T3 subset. ps-researcher, ps-synthesizer, and other research agents can add `mcpServers: memory-keeper: true` without a tier change.
4. **ts-parser and ts-extractor have exact-fit tiers.** T3 (Persistent) = T2 + MK -- the precise tool set these agents need.
5. **5 cross-tier T4 agents correctly classified.** ps-architect, nse-requirements, orch-planner, orch-tracker, orch-synthesizer were already T3+T4 in practice. Under the new model, T4 covers their actual capabilities.
6. **Monotonic hierarchy simplifies reasoning.** "Higher tier = strictly more tools" is now always true.

### Negative

1. **51 governance YAML file changes.** Mechanical but large. Risk of errors in bulk rename mitigated by the two-step migration script with verification.
2. **49 web agents gain MK as tier-level ceiling.** T4 includes T3 (MK), so web-only agents are classified at a tier that permits MK. However, actual MK access requires adding `mcpServers: memory-keeper: true` in the .md frontmatter, which still requires PR review.
3. **Tier number perception.** 49 agents move from "T3" to "T4", which could be misread as "higher privilege, more dangerous." Documentation must clearly communicate that T4 (External) in the new model is the direct successor of T3 (External) in the old model.
4. **eng-* and red-* agents at T4 with MK ceiling.** These agents are explicitly excluded from Memory-Keeper per mcp-tool-standards.md (engagement-scoped output uses P-002 file persistence). Under the new model, they're T4 which permits MK. The exclusion must be maintained via the .md frontmatter and documented in mcp-tool-standards.md.

### Neutral

1. **Schema file unchanged.** The `tool_tier` enum values (T1-T5) are the same; only the semantic mapping in documentation changes.
2. **Agent .md frontmatter unchanged.** No agent gains or loses actual tool access. The migration is entirely governance classification.
3. **T1 and T2 unchanged.** 32 agents (36%) are unaffected by the renumbering.

---

## DX Considerations

A heuristic evaluation (Nielsen's 10 heuristics) was conducted against the proposed tier model from the perspective of agent authors. Full report: `research/dx-review.md`.

### Critical Finding: F-001 — Tier Number Perception (Severity 4)

**Problem:** 49 agents reclassified T3→T4. In conventional RBAC, higher numbers = higher privilege. Agent authors may perceive this as privilege escalation despite identical capability.

**Mitigation adopted:** The tier table now uses **cumulative naming** to make it explicit that T4 builds on T3:

| Tier | Short Name | Full Name | What's New at This Tier |
|------|-----------|-----------|------------------------|
| T1 | Read-Only | Read-Only | -- |
| T2 | Read-Write | Read-Write | Write, Edit, Bash |
| T3 | Persistent | Persistent | Memory-Keeper |
| T4 | External | Persistent + External | WebSearch, WebFetch, Context7 |
| T5 | Orchestration | Orchestration (Persistent + External + Agent) | Agent |

The T4 full name "Persistent + External" explicitly signals that T4 is T3 plus web tools, not a fundamentally different capability. The selection guidelines will state: "T4 inherits all T3 capabilities including Memory-Keeper."

**Naming rationale:** The DX review (F-001) recommended "Web + Persistent" as the compound name. This ADR uses "Persistent + External" instead because: (1) it follows the accumulation order (T3 adds Persistent, T4 adds External on top), making the tier progression readable left-to-right; (2) "External" is the established term from the current T3 tier, maintaining continuity for migrating authors; (3) "Web" is a subset of what T4 adds (Context7 is not strictly "web"). The choice is stylistic; either ordering communicates the same compound capability.

### Major Finding: F-002 — Risk Ordering Not Obvious (Severity 3)

**Problem:** "Persistent before External" violates intuitive RBAC risk ordering for security-trained developers.

**Mitigation:** The selection guidelines will include a one-line risk rationale: "Memory-Keeper (internal MCP, governed namespace) is lower-risk than web tools (external network, arbitrary URLs). T3 before T4 reflects this risk ordering." This converts an implicit architectural rationale into an explicit selection guideline.

### Minor Finding: F-003 — Selection Ambiguity at T3/T4 Boundary (Severity 2)

**Problem:** Agent author needing both MK and web might stop at T3.

**Mitigation:** Selection guideline for T3 will include: "If your agent also needs web tools, use T4 instead (T4 includes all T3 capabilities)."

---

## Compliance

### Auto-Escalation

Per AE-002: modifying `.context/rules/agent-development-standards.md` = auto-C3 minimum. User has set C4 with >= 0.95 threshold.

### H-35 Compliance

Agent tool remains restricted to T5 (Orchestration). Worker agents MUST NOT be T5. No change from current model.

### Constitutional Alignment

| Principle | Impact |
|-----------|--------|
| P-003 (No Recursive Subagents) | No change -- Agent tool at T5 only |
| P-020 (User Authority) | User explicitly requested clean renumbering; decision follows user direction |
| P-022 (No Deception) | Tier model now accurately reflects agent capabilities (eliminates 5 undocumented T3+T4 exceptions) |
| MCP-002 (Phase boundary persistence) | orch-* agents at T4 have MK via T3 subset -- unchanged capability |
| MCP-M-001 (Research persistence) | Now structurally fulfilled -- T4 research agents can access MK |

---

## Risk Register

| ID | Risk | Severity | Status | Mitigation | Source |
|----|------|----------|--------|-----------|--------|
| RISK-001 | Policy drift: 49 agents reclassified T3→T4 gain MK as tier-level ceiling. Future MK additions no longer trigger tier-change review. | Medium | **Accepted** | PR review of `.md` mcpServers additions remains a checkpoint. MK namespace governance (MCP-002) provides secondary control. The T4 tier creates a permission ceiling, not an active grant. | `research/validation-red-team.md`, Consequences Negative 2, FMEA FM-2 |
| RISK-002 | eng-\*/red-\* MK exclusion becomes documentation-dependent rather than structural. | Medium | **Mitigated** | Exclusion documented at 5 independent locations: (1) `agent-development-standards.md` Selection Guideline 4, (2) `agent-development-standards.md` Tier Constraints table, (3) `mcp-tool-standards.md` exclusion notes for eng-\* and red-\*, (4) `agent-governance-v1.schema.json` tool_tier description, (5) `agent-governance-v1.schema.json` $comment. | `research/validation-red-team.md`, Consequences Negative 4 |

---

## FMEA Risk Assessment

| # | Failure Mode | Effect | Cause | S | O | D | RPN | Mitigation |
|---|-------------|--------|-------|---|---|---|-----|-----------|
| 1 | Bulk rename script errors | Wrong agents get wrong tier | sed targeting in 2-step script | 7 | 3 | 2 | 42 | Verify with grep after each step; compare before/after counts |
| 2 | Agent author adds MK to eng-* agent citing "already T4" | Cross-project state pollution for engagement-scoped agents | T4 includes MK ceiling; eng-* exclusion only in docs | 6 | 4 | 4 | 96 | Add explicit "eng-* and red-* MUST NOT use Memory-Keeper" guardrail to mcp-tool-standards.md |
| 3 | Agent author confuses old T3/T4 with new T3/T4 | Wrong tier selected for new agents | Transition period ambiguity | 4 | 5 | 3 | 60 | Version the tier model (v2.0); date-stamp the change |
| 4 | Documentation references old tier numbers | Confusion and incorrect reviews | Many files reference "T3" or "T4" | 3 | 6 | 5 | 90 | Grep for all tier references; update in same PR |
| 5 | MK key collisions increase due to broader access | Silent data overwrite in Memory-Keeper | More agents at tiers permitting MK; concurrent sessions | 7 | 3 | 5 | 105 | **Non-blocking** (post-migration): Strengthen MCP-002 key namespace governance; add collision detection in MK usage. Track as ENABLER under FEAT-001 (provisional ID: EN-MK-COLLISION-DETECT). The existing MCP-002 namespace standard provides adequate governance for the migration PR; enhanced collision detection is a defense-in-depth improvement that does not gate the tier renumbering. |
| 6 | Migration script misses quoted YAML values | 5 pm-pmm agents left at old-T3 after migration | Script uses pattern matching that doesn't handle `tool_tier: "T3"` (quoted) | 8 | 5 | 3 | 120 | Use `grep -rl 'tool_tier:.*T3'` pattern; handle both quoted and unquoted in sed; post-migration verification checklist |
| 7 | Stale tier references in SKILL.md and AGENTS.md | Documentation inconsistency; reviewers cite wrong tier for agent | SKILL.md files may reference "T3 agents" or "T4 agents" by old meaning | 4 | 6 | 4 | 96 | Run `grep -r 'T3\|T4' .context/rules/ skills/*/SKILL.md AGENTS.md` and update all references in same PR |
| 8 | (Option E) Schema change introduces validation errors across 89 agents | CI pipeline failures; blocked PRs; all agent definitions require updates | New `capability_tags` field added to agent-governance-v1.schema.json; existing governance YAMLs without the field fail validation unless field is optional | 7 | 4 | 3 | 84 | Make `capability_tags` optional in schema (default: empty array). Validate in phases: schema change first, then per-agent tag additions. (Not applicable -- Option A selected.) |
| 9 | (Option E) Tag proliferation as new cross-cutting concerns added without governance | Tier model complexity creeps upward; tag combinations become difficult to audit | No governance checkpoint for adding new tag types; any schema-valid tag can be defined without ADR | 5 | 3 | 5 | 75 | Require C3 ADR for new tag types. Maintain tag registry in agent-development-standards.md. (Not applicable -- Option A selected.) |
| 10 | (Option E) Agent authors omit required tags when configuring agents | Agent operates without Memory-Keeper despite needing cross-session state; silent data loss | Two-dimensional model requires author to set both tier AND tags correctly; forgetting +persistent tag is a configuration-level error not caught by tier validation alone | 6 | 4 | 4 | 96 | CI gate cross-referencing .md mcpServers against governance YAML tags. (Not applicable -- Option A selected.) |

> FMEA S/O/D scale: Severity (1-10, 10=catastrophic data loss), Occurrence (1-10, 10=near-certain), Detection (1-10, 10=undetectable). RPN=S×O×D. RPN > 100 = high priority action required. Scale adapted from SAE J1739 for governance artifacts.

**Highest RPN: 120 (migration script quoting bug, FM-6).** Mitigated by the three-step migration script with both quoted and unquoted pattern handling and the post-migration verification checklist (see [Migration Execution](#migration-execution)).

---

*ADR ID: ADR-STORY015-001*
*Project: PROJ-024-tactical-work*
*Author: ps-architect (convergent mode)*
*Date: 2026-03-28*
*Iteration: 7 (STORY-016: Option E added to evaluation matrix, sensitivity analysis, FMEA)*
*DX Review: research/dx-review.md (F-001 severity 4, F-002 severity 3, F-003 severity 2 -- all mitigated)*
*Adversarial Review 1: research/adversarial-review-iteration-1.md (0.852)*
*Adversarial Review 2: research/adversarial-review-iteration-2.md (0.889)*
*Adversarial Review 3: research/adversarial-review-iteration-3.md (0.919)*
*Adversarial Review 4: research/adversarial-review-iteration-4.md (0.935 -- 3 low findings)*
