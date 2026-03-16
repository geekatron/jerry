# The Hybrid B+C Architecture

> Understanding-oriented explanation of the architectural decisions behind the PROJ-023 Rainbow Series exploit framework. Covers why the composable sub-skill model was chosen, why the three-zone security model exists, why behavioral enforcement is built into the architecture, and how these decisions connect to Jerry framework governance.

## Document Sections

| Section | Purpose |
|---------|---------|
| [What This Document Covers](#what-this-document-covers) | Scope of this explanation |
| [The Design Forces](#the-design-forces) | Constraints that shaped the architecture |
| [Why Composable Sub-Skills](#why-composable-sub-skills) | Rationale for Option B hybrid structure |
| [Why a Three-Zone Security Model](#why-a-three-zone-security-model) | Rationale for graduated zone enforcement |
| [Why Behavioral Enforcement in Addition to Scope Documents](#why-behavioral-enforcement-in-addition-to-scope-documents) | Why declarations alone are insufficient |
| [The Trade-Offs Accepted](#the-trade-offs-accepted) | What the Hybrid B+C model gives up |
| [Connection to Jerry Governance](#connection-to-jerry-governance) | How P-003, H-01, and the tool tier model relate |
| [What Was Rejected and Why](#what-was-rejected-and-why) | The evaluated alternatives |

---

## What This Document Covers

This document explains the architectural reasoning behind the PROJ-023 Rainbow Series exploit framework. The architecture was formalized in ADR-PROJ023-001 (Hybrid B+C), which reached a C4 tournament score of 0.948 after four revision iterations.

The explanation here is bounded to these questions: why sub-skills are composable rather than monolithic, why security enforcement is graduated across three zones rather than binary, why the architecture combines structural constraints with behavioral ones, and what this design costs.

For the structural description of which agents exist and what tools they use, see `docs/reference/agent-registry-rainbow-blue.md` and `docs/reference/tool-cli-patterns.md`. For the design decision record itself, see `projects/PROJ-023-exploit-framework/work/design/skill-architecture.md`.

---

## The Design Forces

Any viable architecture for an offensive security toolkit operating inside an LLM framework must satisfy several forces simultaneously, and these forces pull in opposite directions.

**Context efficiency versus specialization depth.** Each loaded tool has an associated context cost of approximately 350--700 tokens for its description and invocation patterns. An architecture that loads all 30+ offensive tools into a single monolithic context would consume 10,000--21,000 tokens before any work begins. That represents 5--10% of a 200K context window, and it degrades agent focus because the LLM must reason across tools that are irrelevant to the current task. However, keeping tools entirely separate creates routing friction and prevents agents from combining capabilities when an operation legitimately spans domains.

**Security boundary clarity versus operational flexibility.** Offensive security operations span a spectrum from completely safe analysis (reading local SBOM files) to inherently dangerous exploitation (executing shellcode on a target). A single undifferentiated context for all these operations creates two problems: it makes it impossible to enforce a meaningful safety boundary, and it creates false risk signals that add friction to the safe operations that make up the majority of work.

**P-003 compliance versus multi-agent coordination.** The Jerry framework's P-003 constraint limits agent delegation to one level: an orchestrator may invoke worker agents, but worker agents may not spawn further workers. This rules out deep hierarchical coordination but does not preclude lateral composition -- a parent orchestrator that delegates to a set of peer sub-skill orchestrators, each of which then delegates to their own workers.

**Incremental delivery versus architectural completeness.** Building all 30+ tools and 26 agents simultaneously would require a single all-or-nothing delivery with no testable intermediate state. The architecture needed to accommodate wave-based delivery where each wave is independently useful.

The Hybrid B+C architecture was chosen because it addresses all four forces simultaneously.

---

## Why Composable Sub-Skills

The name "Hybrid B+C" refers to the two architectural options it combines. Option B was a single `/rainbow` skill with composable sub-skills; Option C was fully independent peer skills (one per capability domain). The hybrid takes the composable sub-skill structure from Option B and applies it to each capability domain, while maintaining a single parent `/rainbow` skill that provides routing and coordination.

The key insight is that sub-skills are not the same as sub-agents. A sub-skill is a logical grouping of related agents under a common SKILL.md, with its own context budget and trigger vocabulary, but it is not a separate process or context window. When `/rainbow-exploit` is invoked, the orchestrator loads only the exploit sub-skill's context -- not the supply chain scanner's tool descriptions, not the recon pipeline's DNS enumeration patterns. This is the context efficiency gain.

The composable structure also explains why the five sub-skills (`/rainbow-supply-chain`, `/rainbow-recon`, `/rainbow-cloud`, `/rainbow-exploit`, `/rainbow-runtime`) have distinct trigger vocabularies rather than sharing a single entry point. Supply chain and cloud security work is common, safe, and frequently needed in isolation. Routing "scan this container image" through an exploit framework context would be wasteful and potentially confusing. The sub-skill boundary creates a clean loading point: the user or orchestrator loads exactly the capability domain relevant to the task.

The parent `/rainbow` skill serves coordination functions that the sub-skills cannot perform independently: maintaining the scope document (which defines what is in-scope for Zone 2 and Zone 3 operations), tracking what has been executed across sub-skills in a multi-phase engagement, and producing a consolidated report that synthesizes findings from disparate domains. The `rainbow-orchestrator` agent holds this coordination role, and it is the only agent in the skill with T5 (Full) tier access to the Task tool.

The wave-gated delivery model that the composable architecture enables is not merely an implementation convenience. It represents a deliberate sequence: Wave 1 (supply chain) and Wave 2 (recon, cloud) deliver value for defensive-leaning use cases before the more sensitive Wave 3 capabilities (exploit, runtime) are introduced. This means the architecture can be audited and validated incrementally, with each wave representing a distinct and coherent security posture.

---

## Why a Three-Zone Security Model

The three-zone model distinguishes:

- **Zone 1** -- Analysis: operations on local files, static artifacts, and pre-collected data. No network contact.
- **Zone 2** -- Active Reconnaissance: network contact with in-scope targets. Engagement scope document required.
- **Zone 3** -- Exploitation: active exploitation, code injection, C2 operation. Per-operation human approval required.

The fundamental reason for three zones rather than a binary safe/unsafe model is that the risk profile of security operations is not binary. A binary model would either be too permissive (treating Subfinder subdomain enumeration the same as Metasploit exploit execution) or too restrictive (requiring human approval for every DNS query).

The three-zone model maps to a natural progression in operational risk. Zone 1 operations are zero-trust in that they do not contact any external system; they carry essentially no risk of unintended impact on target systems. Zone 2 operations touch in-scope systems but are non-destructive -- they observe, enumerate, and collect. The primary risk is scope creep (contacting out-of-scope systems) and stealth failure (leaving observable footprints). Zone 3 operations are inherently impactful -- exploitation changes state on target systems, C2 operations involve ongoing command channels, and traffic interception can disrupt legitimate operations.

This progression also corresponds to the authorization model required for each zone. Zone 1 requires no special authorization because it takes no actions outside the local filesystem. Zone 2 requires a scope document because the targets of reconnaissance need to be explicitly defined; without it, there is no way to verify that the agent is only touching authorized systems. Zone 3 requires per-operation human approval because the consequences of each operation are specific and non-reversible; the scope document's general authorization is insufficient for a specific exploit execution.

The architectural significance is that zone enforcement cannot be left to agent judgment. The zone assignments are baked into the tool definitions in each SKILL.md, and the agent definitions reference these assignments. When `rainbow-recon-pipeline` is described, its zone is Zone 2, and the constraint is that it requires an engagement scope document before executing. This is not a guideline the agent follows if it remembers to; it is a structural property of the agent's identity.

One useful way to think about the zone model is that Zone 2 and Zone 3 are different classes of trust delegation. Zone 2 trusts the scope document: a human has reviewed and authorized the targets, so the agent can operate within those bounds autonomously. Zone 3 trusts neither the scope document alone nor the agent's judgment alone: each operation requires a human to confirm the specific action being taken, because the consequences are too significant for pre-authorization to cover adequately.

---

## Why Behavioral Enforcement in Addition to Scope Documents

Scope documents establish what is authorized. Behavioral enforcement -- the zone model, tool tier assignments, and constitutional constraints -- establishes what the architecture will do regardless of what is requested.

The distinction matters because scope documents can be constructed incorrectly, amended by mistake, or misinterpreted. A system that relies entirely on a scope document to prevent unintended Zone 3 actions is making a single point of failure responsible for all safety guarantees. Behavioral enforcement provides defense in depth: even if a scope document is overly permissive, the per-operation human approval requirement for Zone 3 creates an independent check.

The tool tier model (T1 through T5) addresses a different category of behavioral enforcement: it governs what capabilities each agent can access, independent of what the agent is asked to do. A T2 agent cannot invoke the Task tool even if instructed to, because the Task tool is not in its `tools` frontmatter. This is structural rather than behavioral -- the capability is absent, not suppressed. This matters for P-003 compliance: the constraint against recursive subagents is enforced by the absence of the Task tool in worker agent definitions, not by a behavioral guideline that workers might forget.

There is a philosophical point here about the relationship between rules and architecture. The Jerry framework has learned, through the PROJ-007 agent patterns research, that behavioral rules degrade with context rot -- as the context window fills, earlier instructions receive less attention. Structural constraints, by contrast, are immune to context rot because they are enforced at the tool access layer. The Hybrid B+C architecture applies this lesson explicitly: the most important safety properties (Zone 3 requires human approval, workers cannot spawn sub-workers) are structural, while operational guidelines (scope document format, reporting conventions) are behavioral.

---

## The Trade-Offs Accepted

The Hybrid B+C architecture is not the highest-scoring option on every dimension. Understanding what it concedes is as important as understanding what it achieves.

**Routing complexity.** A fully monolithic architecture would have a single trigger vocabulary. The sub-skill model requires the trigger map to correctly route between `/rainbow-supply-chain`, `/rainbow-recon`, `/rainbow-cloud`, `/rainbow-exploit`, and `/rainbow-runtime`. Incorrect routing -- invoking the wrong sub-skill for a task -- creates friction and potentially invokes more powerful capabilities than needed. The architecture mitigates this through the `rainbow-orchestrator` parent coordinator, but the routing surface is larger than a monolithic design.

**Coordination overhead.** When an engagement requires capabilities from multiple sub-skills (a realistic scenario: recon followed by exploitation), the parent orchestrator must manage context passing between sessions. The checkpoint schema and the scope document act as coordination artifacts, but they add operational weight. A simpler monolithic design would not need this coordination layer.

**Incremental coverage gaps.** Wave-gated delivery means early adopters work with a subset of the intended capability. Wave 0 and Wave 1 provide supply chain capabilities but no exploitation. This is the intended behavior, but it creates an expectation gap: the `/rainbow` skill exists before all its documented capabilities are available.

**Context isolation cost.** Each sub-skill invocation creates a fresh context window for the sub-skill's agents. This is architecturally desirable (FC-M-001 pattern: fresh context reviewers have no sunk-cost bias), but it means that the full history of an engagement is never simultaneously available to any single agent. The checkpoint and handoff artifacts are the workaround, but they are a representation of context, not the context itself.

These trade-offs were evaluated against the alternatives during the ADR-PROJ023-001 tournament process and found acceptable given the design forces. The context efficiency gains, security clarity, and P-003 compliance of the Hybrid B+C approach outweigh the routing and coordination costs across the seven evaluation dimensions.

---

## Connection to Jerry Governance

The Hybrid B+C architecture is not designed in isolation from the Jerry framework governance model. Three governance elements have direct architectural consequences.

**P-003 (No Recursive Subagents)** is the most structurally constraining governance rule. The architecture must be able to coordinate across 26 agents without any agent invoking another agent directly. The parent orchestrator (`rainbow-orchestrator`, T5) is the sole coordination point; all sub-skill agents are T1--T4 with no Task tool access. This is why the sub-skill SKILL.md files define their own agents separately from the parent `/rainbow` skill: each sub-skill's agents are workers invoked by orchestrators, not orchestrators themselves.

**H-05 (UV-only Python)** shapes how the Python-based tools (pwntools, python-stix2, taxii2-client, Frida-based scripts) are invoked. All Python execution goes through `uv run`, which means the tool execution environment is deterministic and isolated. This is particularly relevant for exploitation tools where version-specific behavior matters.

**The tool tier model** from `agent-development-standards.md` maps directly onto the zone model. T1 agents (read-only) correspond to Zone 1 operations. T2 agents (read-write) are the base tier for agents that produce artifacts. T3 agents (external access) are used for agents that contact external data sources. T5 (Full, with Task) is reserved for orchestrators that coordinate workers. The zone model and the tier model reinforce the same principle -- least privilege -- from two different directions: the zone model controls what external targets an agent can contact, and the tier model controls what tools and delegation capabilities the agent can access.

The connection to Jerry governance is not merely that the architecture follows the rules; it is that the architecture was designed with the constraints as first-class design inputs. When the ADR evaluation matrix scored "DEC-006 Alignment" (weight 0.15), it was measuring exactly this: how well the architecture integrates with the existing governance model rather than working around it.

---

## What Was Rejected and Why

The C4 tournament process evaluated five architectural options. Understanding why the losing options were rejected clarifies what the Hybrid B+C model is optimizing for.

**Option A (Monolithic /rainbow, single context)** was rejected primarily on context efficiency grounds. Loading all tool descriptions into a single context window was estimated to consume 10,000--21,000 tokens before any work begins. For a 200K context window, that is 5--10% overhead simply from the skill definition. More significantly, a monolithic context makes it impossible to enforce the zone model structurally -- all tools and their zone assignments would be present simultaneously, making it harder to ensure that a Zone 1 task cannot inadvertently trigger Zone 3 tool invocations.

**Option C (Fully independent peer skills)** was rejected because it fragmented the security model. Five independent peer skills (`/rainbow-supply-chain`, `/rainbow-recon`, etc.) with no parent coordination would have no shared scope document, no unified engagement tracking, and no consolidated reporting. Each skill would need its own zone enforcement mechanism, and cross-skill operations (recon followed by exploitation using the same engagement scope) would require manual coordination. It also created a trigger map growth problem: five new skills with overlapping vocabulary would increase routing ambiguity significantly.

**Option D (Unified with blue-team)** was rejected because the operational posture of offensive and defensive security work is fundamentally different, even when they share targets and findings. Combining them would create a context window that simultaneously holds the detection rule authoring methodology and the exploit execution methodology -- two concerns that are deliberately separated in the zone model. The trust boundary between `/red-team` and `/blue-team` (discussed in the companion explanation document) would be impossible to maintain inside a unified skill.

**Option E (Blue-team sub-skills only, no /rainbow)** was rejected as out of scope for PROJ-023's stated objective: a composable offensive security framework. It was included in the tournament to ensure the decision space was complete.

The Hybrid B+C model occupies the space between Option A's excessive coupling and Option C's excessive fragmentation. The seven-dimension weighted evaluation gave it a score of 4.60, compared to 3.90 for Option A and 3.40 for Option C -- the margin reflects meaningful differences in security boundary clarity and context efficiency, not marginal preferences.

---

*Source: `projects/PROJ-023-exploit-framework/work/design/skill-architecture.md` (ADR-PROJ023-001, C4 tournament score 0.948).*
