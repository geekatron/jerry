# Tier Model Renumbering: Options Explainer

> Standalone companion to ADR-STORY015-001. Explains each renumbering option at three audience levels with worked examples.

## Document Sections

| Section | Purpose |
|---------|---------|
| [The Problem](#the-problem) | Why the current model is broken |
| [Five Representative Agents](#five-representative-agents) | The agents used in every example |
| [Option A: Persistent-First Linear](#option-a-persistent-first-linear) | Memory-Keeper before web tools |
| [Option B: External-First Linear](#option-b-external-first-linear) | Web tools before Memory-Keeper |
| [Option C: Consolidated](#option-c-consolidated) | Merge into 4 tiers |
| [Option D: Lattice with Merge](#option-d-lattice-with-merge) | Keep parallel branches, add merge tier |
| [Option E: Tier + Tags Hybrid](#option-e-tier--tags-hybrid) | Linear base + orthogonal capability flags |
| [Side-by-Side Comparison](#side-by-side-comparison) | All 5 options, same 5 agents, one table |
| [Decision Guide](#decision-guide) | Which option fits your priorities |

---

## The Problem

### ELI5 (L0)

Imagine a building with 5 floors. Each floor has more stuff than the one below it.

- Floor 1: A reading room (you can look at things)
- Floor 2: A workshop (you can build things)
- Floor 3: A phone room (you can call the outside world)
- Floor 4: A filing cabinet room (you can save things for next time)
- Floor 5: A manager's office (you can tell other people what to do)

The problem: the phone room (Floor 3) and the filing cabinet room (Floor 4) are on *different floors*, not stacked. If you need to make a phone call AND save a file, you have to go to the manager's office on Floor 5 -- but then you also get the power to boss people around, which you shouldn't have.

There's no floor with both a phone AND a filing cabinet without also having the manager's desk.

### Engineer (L1)

The current T1-T5 tool security tier model has a structural gap. T3 (External: web tools) and T4 (Persistent: Memory-Keeper) branch in parallel from T2. They only merge at T5, which includes the Agent tool -- forbidden for worker agents by H-35.

```
Current topology (broken):

         +-- T3 (External: +Web) --------+
T1 -> T2 |                               +-> T5 (Full: +Agent)
         +-- T4 (Persistent: +MK) -------+

Problem: T3 + T4 without Agent = ???
```

Seven agents are declared T4 today. Five of them actually have *both* web tools and Memory-Keeper. They're operating outside the tier model because no valid tier describes their tool set.

### Architect (L2)

The tier model is a partially-ordered set that was designed as a total order (linear chain) but contains a non-comparable pair: T3 and T4 are incomparable elements (T3 ⊄ T4 and T4 ⊄ T3) pretending to be comparable. T5 is their join (least upper bound) but is polluted with the Agent tool. The renumbering options below are different strategies for restoring total ordering or making the partial order explicit.

---

## Five Representative Agents

Every option is illustrated with the same five agents. These were chosen to cover every interesting case in the tier model:

| Agent | What It Does | Current Tier | Actual Tools | Why It Matters |
|-------|-------------|-------------|-------------|----------------|
| **pe-scorer** | Scores prompt quality | T1 | Read, Glob, Grep | Baseline: unchanged in every option |
| **ps-critic** | Reviews deliverable quality | T2 | Read, Write, Edit, Glob, Grep | Pure read-write, no web or MK |
| **eng-backend** | Secure backend engineering | T3 | T2 + WebSearch, WebFetch, Context7 | Web tools but no MK -- the "web-only" case |
| **ts-parser** | Parses VTT transcripts | T4 | Read, Write, Glob, Bash + Memory-Keeper | MK but no web -- the "persistence-only" case |
| **ps-architect** | Architecture decisions | T4 | T2 + WebSearch, WebFetch + Context7 + Memory-Keeper | Both web AND MK -- the agent that exposed the gap |

---

## Option A: Persistent-First Linear

*Swap the order: Memory-Keeper comes before web tools.*

### ELI5 (L0)

We rearrange the floors so the filing cabinet room (persistence) is below the phone room (web). Now if you need a phone, you walk past the filing cabinets on the way up -- you automatically get both.

```
Floor 1: Reading room
Floor 2: Workshop
Floor 3: Filing cabinets (NEW position -- moved down from Floor 4)
Floor 4: Phone room + filing cabinets (phone is NEW; cabinets came with Floor 3)
Floor 5: Manager's office + everything below
```

The VTT parser (ts-parser) lives on Floor 3 -- filing cabinets, no phone. The architect (ps-architect) lives on Floor 4 -- phone AND filing cabinets. Everyone who makes calls also gets a filing cabinet.

**Trade-off:** Every agent with a phone (49 of them) now has a filing cabinet too, even if they never use it.

### Engineer (L1)

```
T1: Read-Only       (Read, Glob, Grep)
T2: Read-Write      (T1 + Write, Edit, Bash)
T3: Persistent      (T2 + Memory-Keeper)          <-- MK enters here
T4: External        (T3 + WebSearch, WebFetch, Context7)  <-- Web on top of MK
T5: Orchestration   (T4 + Agent)
```

**How the five agents land:**

| Agent | Current | New | What Changed |
|-------|---------|-----|-------------|
| pe-scorer | T1 | T1 | Nothing |
| ps-critic | T2 | T2 | Nothing |
| eng-backend | T3 | **T4** | Number goes up (T3→T4). Same tools. Gains MK *ceiling* but `.md` doesn't list it. |
| ts-parser | T4 | **T3** | Number goes down (T4→T3). Perfect fit: T2 + MK is exactly T3. |
| ps-architect | T4 | **T4** | Same number. New T4 = T3 + Web = T2 + MK + Web. Exact fit for the first time. |

**Migration:** 51 governance YAML file changes. No `.md` file changes. Scripted with a 3-step migration and rollback.

### Architect (L2)

Option A restores total ordering by placing the lower-risk capability (Memory-Keeper: internal MCP, governed namespace) below the higher-risk capability (web tools: external network, arbitrary URLs). This produces a strict monotonic chain: T1 ⊂ T2 ⊂ T3 ⊂ T4 ⊂ T5.

**Structural property:** Every tier is a strict superset of the one below. No exceptions. The partial order becomes a total order.

**Governance trade-off:** 49 web-only agents (eng-\*, red-\*, ux-\*, etc.) are reclassified from T3 to T4. Their tier ceiling now *permits* Memory-Keeper even though they don't use it. This widens the governance aperture: adding `mcpServers: memory-keeper: true` to any T4 agent's `.md` no longer requires a tier-change review. The MK namespace governance (MCP-002) and the `.md` PR review are the remaining checkpoints.

**ts-parser/ts-extractor fit:** Exact. T3 = T2 + MK describes their actual tool set with zero over-provisioning.

---

## Option B: External-First Linear

*Keep web tools at T3. Put Memory-Keeper on top at T4.*

### ELI5 (L0)

We keep the phone room where it is (Floor 3) and rename Floor 4. Now Floor 4 has both a phone AND a filing cabinet. The VTT parser (ts-parser) technically lives on Floor 4 even though it never uses the phone -- there's no "filing cabinet only" floor.

```
Floor 1: Reading room
Floor 2: Workshop
Floor 3: Phone room (unchanged)
Floor 4: Phone room + filing cabinets (filing cabinets NEW here)
Floor 5: Manager's office + everything below
```

**Trade-off:** The VTT parser has a phone it never uses. But nobody has to move -- all the room numbers stay the same.

### Engineer (L1)

```
T1: Read-Only       (Read, Glob, Grep)
T2: Read-Write      (T1 + Write, Edit, Bash)
T3: External        (T2 + WebSearch, WebFetch, Context7)  <-- unchanged
T4: Extended         (T3 + Memory-Keeper)                  <-- MK on top of Web
T5: Orchestration   (T4 + Agent)
```

**How the five agents land:**

| Agent | Current | New | What Changed |
|-------|---------|-----|-------------|
| pe-scorer | T1 | T1 | Nothing |
| ps-critic | T2 | T2 | Nothing |
| eng-backend | T3 | T3 | **Nothing** |
| ts-parser | T4 | T4 | Same number. But T4 now means T3+MK = T2+**Web**+MK. ts-parser gains a web *ceiling* it doesn't use. |
| ps-architect | T4 | T4 | Same number. New T4 = T3+MK. **Exact fit** for the first time. |

**Migration:** 0 governance YAML changes. The tier *numbers* don't change for any agent. Only the tier *definitions* change in 2 rule files.

### Architect (L2)

Option B linearizes the hierarchy by stacking MK on top of web access. This preserves T3's meaning (49 agents untouched) and redefines T4 from "T2 + MK" to "T3 + MK."

**Structural property:** Monotonic total order. T1 ⊂ T2 ⊂ T3 ⊂ T4 ⊂ T5.

**Key compromise:** The T2+MK combination (ts-parser, ts-extractor) has no exact-fit tier. These 2 agents are classified T4 but their `.md` frontmatter doesn't include WebSearch/WebFetch. This is an **over-classification** (ceiling > actual), not an under-classification (actual > ceiling). The agent can't do anything it shouldn't -- it just has a governance label that's higher than necessary.

**Governance trade-off:** 2 agents over-classified (vs. Option A's 49 agents with expanded MK ceiling). The governance aperture is narrower: only T4+ agents have MK ceiling, and T4 is a smaller set (7 agents) than Option A's T4 (54 agents).

**Migration risk:** Near zero. No files move. No migration script needed. The only change is definitional: update 2 rule files to describe what T3/T4/T5 mean.

---

## Option C: Consolidated

*Collapse to 4 tiers. Memory-Keeper becomes a basic worker capability at T2.*

### ELI5 (L0)

We knock down a wall and merge rooms. Now every workshop (Floor 2) has a filing cabinet built in. The phone room stays on Floor 3. The manager stays on Floor 4 (renumbered from 5).

```
Floor 1: Reading room
Floor 2: Workshop + filing cabinets (filing cabinets built into the workshop)
Floor 3: Phone room + workshop + filing cabinets
Floor 4: Manager's office + everything below
```

**Trade-off:** Everyone who can build things also has a filing cabinet -- even people who never save anything. But the building only has 4 floors now, which is simpler.

### Engineer (L1)

```
T1: Read-Only       (Read, Glob, Grep)
T2: Read-Write      (T1 + Write, Edit, Bash + Memory-Keeper)  <-- MK at T2!
T3: External        (T2 + WebSearch, WebFetch, Context7)
T4: Orchestration   (T3 + Agent)
```

**How the five agents land:**

| Agent | Current | New | What Changed |
|-------|---------|-----|-------------|
| pe-scorer | T1 | T1 | Nothing |
| ps-critic | T2 | T2 | Same number. T2 now includes MK ceiling. |
| eng-backend | T3 | T3 | Same number. T3 now includes MK ceiling (via T2). |
| ts-parser | T4 | **T2** | Drops from T4 to T2. T2 now includes MK = exact fit. |
| ps-architect | T4 | **T3** | Drops from T4 to T3. T3 = T2+Web = T2+MK+Web = exact fit. |

**Migration:** 8 governance YAML changes (5 old-T4-with-web → T3, 2 old-T4-pure-MK → T2, 1 old-T5 → T4).

### Architect (L2)

Option C answers the user's question "Why wouldn't we want other agents to leverage Memory-Keeper?" by saying: **you're right -- make it universal.** MK becomes a T2 capability, available to all 77 agents that can write files.

**Structural property:** Monotonic total order with 4 tiers. Simplest possible model.

**Governance trade-off:** The MK governance checkpoint is **eliminated**. Under the current model, an agent needing MK must justify a T4 tier. Under Option C, any T2+ agent can add `mcpServers: memory-keeper: true` without a tier change. The 28 current-T2 agents (scorers, validators, formatters, contract designers) gain MK ceiling even though none of them have cross-session state needs.

**When this is the right choice:** If MK tier-change reviews are always rubber-stamped (no rejections), the checkpoint is ceremony without value. Removing it reduces governance friction. If MK access has been denied in a tier review even once, the checkpoint has demonstrated value and Option C is premature.

---

## Option D: Lattice with Merge

*Keep T3 and T4 as parallel branches. Add T5 as their merge point. Bump T5→T6.*

### ELI5 (L0)

We keep the phone room and the filing cabinet room on separate floors, but we add a new floor between them and the manager that has BOTH a phone and a filing cabinet. The manager moves up one floor.

```
Floor 1: Reading room
Floor 2: Workshop
Floor 3: Phone room (same as today)
Floor 4: Filing cabinet room (same as today)
Floor 5: Phone room + filing cabinet room (NEW floor)
Floor 6: Manager's office
```

**Trade-off:** Everyone has an exact floor. But the building has 6 floors now, and Floors 3 and 4 are side-by-side, not stacked -- going from 3 to 4 doesn't mean "more stuff."

### Engineer (L1)

```
T1: Read-Only       (Read, Glob, Grep)
T2: Read-Write      (T1 + Write, Edit, Bash)
T3: External        (T2 + WebSearch, WebFetch, Context7)     ─┐
T4: Persistent      (T2 + Memory-Keeper)                     ─┤ parallel branches
T5: Extended        (T3 + T4 = T2 + Web + MK)                ─┘ merge point
T6: Orchestration   (T5 + Agent)
```

**How the five agents land:**

| Agent | Current | New | What Changed |
|-------|---------|-----|-------------|
| pe-scorer | T1 | T1 | Nothing |
| ps-critic | T2 | T2 | Nothing |
| eng-backend | T3 | T3 | Nothing |
| ts-parser | T4 | T4 | Nothing. T4 still means T2+MK. Perfect fit. |
| ps-architect | T4 | **T5** | Moves to new merge tier. T5 = T3+T4 = exact fit. |

**Migration:** 6 governance YAML changes (5 old-T4-with-web → T5, 1 old-T5 → T6).

### Architect (L2)

Option D is the only option that makes the partial order *explicit* rather than forcing it into a total order. T3 and T4 are incomparable elements with T5 as their join. This is a lattice, not a chain.

**Structural property:** NOT monotonic between T3 and T4. T3 ⊄ T4 and T4 ⊄ T3. Every other pair is comparable. This is the honest representation of the capability topology.

**Governance trade-off:** Most precise least privilege -- every agent gets exactly the tier it needs, no over-provisioning. But the non-monotonic T3/T4 pair creates cognitive burden: "T4 is not higher than T3" violates the intuition that higher numbers mean more capability. This is the same structural confusion that caused the original gap.

**When this is the right choice:** If the framework grows to 50+ agents with many distinct capability combinations, a lattice model becomes necessary. At 89 agents with only 2 agents needing T2+MK (ts-parser, ts-extractor), the lattice adds complexity for minimal precision gain.

---

## Option E: Tier + Tags Hybrid

*Keep a linear base tier. Add orthogonal capability flags for cross-cutting concerns.*

> Source: `research/industry-tier-patterns.md`. This option was identified by the industry research phase and is precedented by Linux capabilities (base user model + CAP_* flags), Deno (deny-all + --allow-* flags), and emerging AI agent frameworks (MiniScope, FINOS).

### ELI5 (L0)

Instead of putting everything on numbered floors, we give each room a base floor number AND stickers on the door. The floor tells you the basics; the stickers tell you the extras.

```
Floor 1: Reading room
Floor 2: Workshop
Floor 3: Workshop + phone room

Stickers (can go on any door):
  [MK] = Has a filing cabinet
  [AGENT] = Can boss people around
```

The VTT parser lives on Floor 2 with an [MK] sticker. The architect lives on Floor 3 with an [MK] sticker. Nobody gets extras they don't need.

**Trade-off:** Two things to check per agent (floor + stickers) instead of one (floor).

### Engineer (L1)

```
Base Tiers (linear):
  T1: Read-Only       (Read, Glob, Grep)
  T2: Read-Write      (T1 + Write, Edit, Bash)
  T3: External        (T2 + WebSearch, WebFetch, Context7)

Capability Tags (orthogonal, independent of base tier):
  +persistent          Memory-Keeper access (requires MCP-002 key namespace compliance)
  +delegate            Agent tool access (restricted to orchestrator agents per H-35)
```

**How the five agents land:**

| Agent | Current | New | Tags | What Changed |
|-------|---------|-----|------|-------------|
| pe-scorer | T1 | T1 | (none) | Nothing |
| ps-critic | T2 | T2 | (none) | Nothing |
| eng-backend | T3 | T3 | (none) | Nothing |
| ts-parser | T4 | **T2** | **+persistent** | Base tier reflects actual tools. Tag adds MK. |
| ps-architect | T4 | **T3** | **+persistent** | Base tier reflects web tools. Tag adds MK. |

**Migration:** 7 governance YAML changes (7 old-T4 agents get base tier + tag; 1 old-T5 gets +delegate tag). Schema change required: `tool_tier` becomes base tier, new `capability_tags` array field added.

### Architect (L2)

Option E decomposes the partially-ordered capability set into a product of a total order (base tier T1-T3) and a set of independent boolean dimensions (tags). This is the standard approach in capability-based security systems (POSIX capabilities, Deno permissions, WASI).

**Structural property:** Base tier is monotonic (T1 ⊂ T2 ⊂ T3). Tags are orthogonal -- `+persistent` can be applied at any base tier. The effective capability set is: `base_tier_tools ∪ tag_tools`.

**Governance trade-off:** Most expressive model. Every agent gets exactly what it needs. No over-provisioning. Each tag is an independent governance decision with its own review.

**Complexity cost:** Agent definitions now have two governance axes (tier + tags). The `agent-governance-v1.schema.json` needs a new `capability_tags` field. Tier selection guidelines need a second decision: "which tags?" Documentation must explain a 2D model instead of a 1D list. For 89 agents where only 7 need the `+persistent` tag, this is substantial machinery for a narrow use case.

**When this is the right choice:** When the number of cross-cutting capabilities grows beyond 2. If a third orthogonal dimension emerges (e.g., a new MCP server that doesn't fit the linear chain), the Tier+Tags model accommodates it without restructuring. The linear models (A, B, C) would need another renumbering.

---

## Side-by-Side Comparison

### Same Five Agents, All Five Options

| Agent | Current | Option A | Option B | Option C | Option D | Option E |
|-------|---------|----------|----------|----------|----------|----------|
| pe-scorer | T1 | T1 | T1 | T1 | T1 | T1 |
| ps-critic | T2 | T2 | T2 | T2 | T2 | T2 |
| eng-backend | T3 | **T4** | T3 | T3 | T3 | T3 |
| ts-parser | T4 | **T3** | T4 | **T2** | T4 | **T2+persistent** |
| ps-architect | T4 | T4 | T4 | **T3** | **T5** | **T3+persistent** |
| ux-orchestrator | T5 | T5 | T5 | **T4** | **T6** | **T3+delegate** |

### Migration Effort

| Metric | Option A | Option B | Option C | Option D | Option E |
|--------|----------|----------|----------|----------|----------|
| Governance YAML changes | 51 | **0** | 8 | 6 | 7 |
| Rule file changes | 2 | 2 | 2 | 2 | 2 |
| Schema change needed | No | No | No | No | **Yes** (new field) |
| Migration script needed | Yes | No | No | No | No |
| Total tiers | 5 | 5 | 4 | 6 | 3 + tags |

### Structural Properties

| Property | Option A | Option B | Option C | Option D | Option E |
|----------|----------|----------|----------|----------|----------|
| Monotonic (each tier > previous) | Yes | Yes | Yes | **No** (T3 parallel T4) | Yes (base tiers) |
| Gap fully solved | Yes | Yes | Yes | Yes | Yes |
| ts-parser exact fit | **Yes** (T3) | No (over at T4) | **Yes** (T2) | **Yes** (T4) | **Yes** (T2+persistent) |
| Over-classified agents | 49 (gain MK ceiling) | 2 (gain Web ceiling) | 77 (gain MK ceiling) | 0 | 0 |
| Simplest to explain | - | - | **Simplest** (4 tiers) | Most complex (6 tiers) | 2D model |
| Forward compatible | Moderate | Moderate | Limited | Good | **Best** |

---

## Decision Guide

**Pick your priority, find your option:**

| If you most value... | Choose | Because |
|---------------------|--------|---------|
| Lowest migration effort | **Option B** | 0 file changes. Only update 2 rule files. |
| Simplest model going forward | **Option C** | 4 tiers. One decision per agent. |
| Exact fit for every agent | **Option D** or **E** | Zero over-provisioning. |
| Risk-ordered hierarchy | **Option A** | MK (low risk) before Web (high risk). |
| Future extensibility | **Option E** | New capabilities = new tags, no restructuring. |
| Minimal governance change | **Option B** | No new checkpoints, no removed checkpoints. |

**Decision (2026-03-28):** **Option A (Persistent-First Linear) was selected and implemented** via STORY-017 (rule files) and STORY-018 (governance YAML migration). The current tier model is: T1=Read-Only, T2=Read-Write, T3=Persistent (+MK), T4=External (+Web, includes MK), T5=Orchestration (+Agent).

**What the research recommended:** Option E (Tier + Tags), based on industry precedent from RBAC systems, Deno, and emerging AI agent frameworks. Option E was evaluated in the ADR (scored 8.20 nominal, 8.45 governance-weighted) but was not selected due to schema change cost and 2D model complexity for 89 agents where only 8 need tags. Option E remains the recommended evolution path if a third orthogonal capability emerges.

**For the current tier model:** See `.context/rules/agent-development-standards.md` [Tool Security Tiers].
**For migration steps:** See `STORY-019-documentation-migration-guide/tier-migration-guide.md`.

---

*Explainer Version: 1.1.0*
*Source: ADR-STORY015-001 (Options A-E), research/industry-tier-patterns.md (Option E)*
*Date: 2026-03-28*
*Updated: Decision recorded — Option A implemented via STORY-017/STORY-018*
