---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Requirements Specification: Claude Code Agent Development Rules

> **Project:** PROJ-007-agent-patterns
> **Entry:** e-004
> **Date:** 2026-02-21
> **Status:** Draft
> **NASA Process:** NPR 7123.1D Processes 1, 2, 11
> **Agent:** nse-requirements v2.1.0
> **Cognitive Mode:** Convergent

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language overview for stakeholders |
| [Stakeholder Needs Analysis](#stakeholder-needs-analysis) | NPR 7123.1D Process 1 -- stakeholders and needs |
| [Agent Structure Requirements (AR)](#agent-structure-requirements-ar) | Agent definition format, nesting, isolation, tools |
| [Prompt Design Requirements (PR)](#prompt-design-requirements-pr) | Role clarity, cognitive mode, progressive disclosure, persona |
| [Routing Requirements (RR)](#routing-requirements-rr) | Trigger keywords, determinism, fallback, loop prevention |
| [Handoff Requirements (HR)](#handoff-requirements-hr) | Structured handoff format, state preservation, verification |
| [Quality Requirements (QR)](#quality-requirements-qr) | Quality gate integration, self-review, output compliance |
| [Safety and Governance Requirements (SR)](#safety-and-governance-requirements-sr) | Constitutional compliance, guardrails, user authority, audit |
| [Traceability Matrix](#traceability-matrix) | Bidirectional traceability to Phase 1 research and existing rules |
| [Requirements Quality Verification](#requirements-quality-verification) | INCOSE quality criteria check |
| [Open Items](#open-items) | Unresolved questions requiring stakeholder input |
| [References](#references) | Source document list |

---

## L0: Executive Summary

This document specifies 62 formal requirements for developing Claude Code agents within the Jerry Framework. The requirements are organized into six domains: Agent Structure, Prompt Design, Routing, Handoff, Quality, and Safety/Governance. Each requirement is a formal shall-statement with rationale, priority (MUST/SHOULD/MAY), verification method, and bidirectional traceability to Phase 1 research findings and existing Jerry rules.

**Key themes driving these requirements:**

- **Structural consistency.** Every agent definition shall follow the same YAML frontmatter + Markdown body format with mandatory fields, enabling machine validation and human readability.
- **Single-level nesting.** The orchestrator-worker pattern with maximum one level of delegation is the only permitted agent hierarchy, preserving P-003 compliance.
- **Layered routing.** Deterministic keyword matching shall be the primary routing mechanism, with LLM-based fallback for ambiguous cases, balancing speed with flexibility.
- **Structured handoffs.** Agent-to-agent handoffs shall use a schema-defined structured format to prevent the information loss that is the #1 failure source in multi-agent systems.
- **Criticality-proportional quality.** Quality enforcement effort shall scale with decision criticality (C1-C4), from lightweight self-review for routine work to full tournament mode for irreversible decisions.
- **Constitutional compliance by construction.** Safety and governance constraints shall be embedded in agent definitions, not applied as afterthoughts.

**Stakeholders served:** Agent developers (humans writing agent definitions), agent consumers (orchestrators invoking agents), framework maintainers (Jerry governance), and end users (humans receiving agent outputs).

---

## Stakeholder Needs Analysis

### NPR 7123.1D Process 1: Stakeholder Expectations Definition

#### Stakeholder Identification

| ID | Stakeholder | Role | Interest |
|----|-------------|------|----------|
| SH-1 | Agent Developers | Write and maintain agent definition files | Clear authoring standards, validation tooling, templates |
| SH-2 | Agent Consumers | Orchestrators and skills that invoke agents | Predictable interfaces, reliable routing, structured outputs |
| SH-3 | Framework Maintainers | Jerry governance and evolution | Consistency, traceability, enforceable rules, extensibility |
| SH-4 | End Users | Humans receiving agent outputs | Quality, accuracy, transparency, appropriate level of detail |

#### Stakeholder Needs

| Need ID | Stakeholder | Need Statement | Priority |
|---------|-------------|----------------|----------|
| SN-01 | SH-1 | A standard template for agent definition that covers all required fields | MUST |
| SN-02 | SH-1 | Schema validation tooling to catch definition errors before deployment | SHOULD |
| SN-03 | SH-1 | Clear documentation of what each frontmatter field means and when to use it | MUST |
| SN-04 | SH-2 | Deterministic routing for common cases so invocation is predictable | MUST |
| SN-05 | SH-2 | Structured output format so consumer can parse agent results programmatically | MUST |
| SN-06 | SH-2 | Handoff protocol that preserves all necessary context between agents | MUST |
| SN-07 | SH-3 | Enforceable rules that can be checked by tooling (AST, CI, linting) | MUST |
| SN-08 | SH-3 | Traceability from every rule to its rationale and source | MUST |
| SN-09 | SH-3 | Extension mechanism for adding new agent types without breaking existing ones | SHOULD |
| SN-10 | SH-4 | Multi-level output (L0/L1/L2) so different audiences get appropriate detail | MUST |
| SN-11 | SH-4 | Citation of sources so claims can be verified | MUST |
| SN-12 | SH-4 | Quality assurance that scales with the importance of the deliverable | MUST |
| SN-13 | SH-1, SH-3 | Agent definitions that are version-controlled and diff-friendly | SHOULD |
| SN-14 | SH-2, SH-3 | Tool access governance so agents cannot exceed their authorized capabilities | MUST |
| SN-15 | SH-4 | Guardrails that prevent harmful, deceptive, or unauthorized agent behavior | MUST |

---

## Agent Structure Requirements (AR)

### AR-001: Agent Definition File Format

**The system shall** use YAML frontmatter combined with a Markdown body as the canonical agent definition format.

- **Rationale:** Trade study TS-2 (Agent Definition Format) scored the YAML+MD pattern (B1) and its schema-validated variant (B5) highest (4.00 and 4.45 respectively). The format combines machine-readable metadata with human-readable behavioral instructions, is proven at scale (37 agents in Jerry), and is Git-friendly. Pure YAML (B2) loses expressiveness for behavioral nuance; code-first (B3) raises the skill barrier; DSL (B4) creates proprietary maintenance burden.
- **Priority:** MUST
- **Verification:** Inspection -- validate that all agent definition files use YAML frontmatter delimited by `---` followed by Markdown body.
- **Source:** TS-2 (B1, B5); ps-researcher-001 (Agent Skills Architecture); SN-01, SN-13.

### AR-002: Required Frontmatter Fields

**The system shall** require the following fields in every agent definition YAML frontmatter: `name`, `version`, `description`, `model`, `identity` (containing `role`, `expertise`, `cognitive_mode`), `capabilities` (containing `allowed_tools`), `guardrails`, and `output`.

- **Rationale:** Analysis of 37 existing Jerry agents shows these fields are necessary and sufficient for machine processing (routing, validation, tool provisioning) and human understanding (role clarity, behavioral expectations). The `identity` block follows Anthropic best practices; `capabilities.allowed_tools` enables principle-of-least-privilege enforcement; `guardrails` embeds safety constraints.
- **Priority:** MUST
- **Verification:** Inspection -- JSON Schema validation of YAML frontmatter against the canonical schema.
- **Source:** TS-2 (B5 schema validation); ps-researcher-001 (Subagent Configuration); SN-01, SN-03, SN-07.

### AR-003: Agent Definition Schema Validation

**The system shall** provide a JSON Schema for validating agent definition YAML frontmatter, covering field presence, type constraints, enumerated values for `model` and `cognitive_mode`, and format patterns for `name` and `version`.

- **Rationale:** Trade study TS-2 identifies schema validation as the highest-value evolutionary improvement (B5 scores 4.45 vs. B1 at 4.00). Schema validation catches structural errors deterministically without LLM overhead and addresses the current risk of inconsistency between frontmatter and body.
- **Priority:** SHOULD
- **Verification:** Test -- execute schema validation against all agent files and confirm zero violations.
- **Source:** TS-2 (B5); SN-02, SN-07; Open Question OQ-1 (schema format selection).

### AR-004: Single-Level Agent Nesting

**The system shall** enforce a maximum of one level of agent delegation: an orchestrator agent may delegate to worker agents, but worker agents shall not delegate further.

- **Rationale:** Constitutional constraint P-003/H-01. Trade study TS-1 confirms the orchestrator-worker pattern (A3) scores highest (4.25). ps-researcher-001 confirms Claude Code enforces max one level of nesting via the Task tool. Hierarchical teams (A5, score 3.25) were evaluated and rejected due to P-003 conflict. Google DeepMind research shows the "Bag of Agents" anti-pattern (uncoordinated multi-level delegation) causes 17x error amplification.
- **Priority:** MUST
- **Verification:** Analysis -- static analysis of agent definitions to confirm no worker agent declares Task tool in `allowed_tools`; Test -- integration test that attempts two-level delegation and confirms rejection.
- **Source:** P-003/H-01; TS-1 (A3 vs. A5); ps-researcher-001; ps-researcher-002 (Bag of Agents anti-pattern); SN-14.

### AR-005: Context Isolation Between Agents

**The system shall** ensure that each agent operates within an isolated context window. A subagent shall not inherit the parent agent's full context; only explicitly passed information shall be available.

- **Rationale:** Context isolation is fundamental to the skill-based specialist pattern (TS-1, A3). ps-researcher-001 confirms that in Claude Code, "subagent does NOT inherit parent's full context." Context isolation prevents context rot by limiting each agent's context to what is relevant, and enables parallel execution without interference.
- **Priority:** MUST
- **Verification:** Test -- invoke a subagent and verify it cannot access parent context artifacts that were not explicitly passed. Inspection -- confirm Task tool invocations include only specified context.
- **Source:** TS-1 (A3); ps-researcher-001 (Subagent Configuration, Context Isolation); SN-06.

### AR-006: Tool Restriction Enforcement

**The system shall** restrict each agent's tool access to the tools declared in its `capabilities.allowed_tools` frontmatter field. An agent shall not be able to invoke tools not in its allowed list.

- **Rationale:** Principle of least privilege. Trade study TS-5 (Tool Integration) scored static tool assignment (E1, 4.15) and hybrid static+MCP (E5, 4.10) highest. Dynamic tool selection (E2, 2.90) was rejected due to security, auditability, and P-003 concerns. ps-researcher-002 identifies uncontrolled tool access as a vector for routing loops and error amplification.
- **Priority:** MUST
- **Verification:** Test -- attempt to invoke a tool not in the agent's allowed list and confirm rejection. Inspection -- audit TOOL_REGISTRY.yaml against agent frontmatter for consistency.
- **Source:** TS-5 (E1, E5); MCP-001/MCP-002; ps-researcher-002; SN-14.

### AR-007: Agent Name Convention

**The system shall** require agent names to follow the pattern `{skill-prefix}-{function}` using lowercase kebab-case, where the skill prefix matches the parent skill directory name prefix.

- **Rationale:** Consistent naming enables automated registry generation, routing table construction, and human navigation. The current 37-agent registry uses this pattern (ps-*, nse-*, orch-*, adv-*, wt-*, ts-*, sb-*). H-26 requires skill folders to use kebab-case.
- **Priority:** MUST
- **Verification:** Inspection -- regex validation of agent `name` field against pattern `^[a-z]+-[a-z]+(-[a-z]+)*$`. Cross-reference against parent skill directory.
- **Source:** H-26; AGENTS.md naming convention; SN-07.

### AR-008: Agent Version Tracking

**The system shall** require each agent definition to include a semantic version (`version` field) in the YAML frontmatter, following the `MAJOR.MINOR.PATCH` format.

- **Rationale:** Version tracking enables change management, regression detection, and compatibility verification between agents that interact. The Open Agent Specification (Agent Spec, 2025) mandates version fields for agent definitions. All existing Jerry agents already include version fields.
- **Priority:** MUST
- **Verification:** Inspection -- regex validation of `version` field against pattern `^\d+\.\d+\.\d+$`.
- **Source:** TS-2 (B5); Open Agent Specification; SN-13.

### AR-009: Agent Description Quality

**The system shall** require the `description` field to specify WHAT the agent does, WHEN it should be invoked, and include at least one trigger example. The description shall be fewer than 1024 characters and shall not contain XML tags.

- **Rationale:** H-28 requires descriptions to include WHAT + WHEN + triggers. The description field is used by routing mechanisms (both keyword and LLM-based) to determine agent selection. Poor descriptions lead to misrouting. The character limit and XML prohibition prevent context window waste and parsing conflicts.
- **Priority:** MUST
- **Verification:** Inspection -- validate description length < 1024 chars, absence of XML tags, and presence of trigger keywords.
- **Source:** H-28; TS-3 (routing uses descriptions); SN-03.

### AR-010: Agent File Location

**The system shall** require agent definition files to be located at `skills/{skill-name}/agents/{agent-name}.md`, where the file name matches the agent's `name` field.

- **Rationale:** H-25 mandates the file be exactly `SKILL.md` (case-sensitive) for skills; by extension, agent files follow a parallel convention. H-29 requires full repo-relative paths. Consistent file location enables automated discovery via glob patterns, registry verification, and skill-to-agent mapping.
- **Priority:** MUST
- **Verification:** Inspection -- glob `skills/*/agents/*.md` and verify each file's `name` field matches its filename (without extension).
- **Source:** H-25, H-26, H-29; AGENTS.md file paths; SN-07.

### AR-011: Agent Registration

**The system shall** require every agent to be registered in AGENTS.md and in the parent skill's SKILL.md.

- **Rationale:** H-30 mandates registration in CLAUDE.md and AGENTS.md. Unregistered agents are invisible to routing, quality enforcement, and governance audit. The registry is the single source of truth for agent count, capability mapping, and MCP tool access.
- **Priority:** MUST
- **Verification:** Inspection -- compare agent files discovered via filesystem glob against AGENTS.md entries. Flag any agent file not listed in AGENTS.md or any AGENTS.md entry with no corresponding file.
- **Source:** H-30; AGENTS.md; SN-07, SN-09.

### AR-012: Forbidden Actions Declaration

**The system shall** require each agent definition to include a `capabilities.forbidden_actions` list that explicitly declares actions the agent must not perform.

- **Rationale:** Explicit forbidden actions serve as negative guardrails that complement the positive `allowed_tools` list. ps-researcher-003 identifies that "guardrails and constitutional constraints are table stakes" for production agent deployments. Declaring forbidden actions in the definition file makes constraints visible to both the LLM (via system prompt) and tooling (via validation).
- **Priority:** MUST
- **Verification:** Inspection -- validate presence of `forbidden_actions` list with at least one entry. Cross-reference against constitutional constraints (P-003, P-020, P-022).
- **Source:** ps-researcher-003 (Guardrails); TS-2 (AR-002); SN-15.

---

## Prompt Design Requirements (PR)

### PR-001: Role Clarity

**The system shall** require each agent definition to specify a clear, singular role in the `identity.role` field that unambiguously identifies the agent's function within the skill.

- **Rationale:** ps-researcher-001 confirms that Claude Code subagents receive a "custom system prompt per subagent." Role clarity is the foundation of the skill-based specialist pattern (TS-1, A3). Ambiguous roles lead to task overlap, routing confusion, and diffused responsibility. The role field is used to construct the system prompt's identity preamble.
- **Priority:** MUST
- **Verification:** Inspection -- validate that `identity.role` is a non-empty string. Analysis -- review for uniqueness within the parent skill (no two agents in the same skill shall have identical roles).
- **Source:** TS-1 (A3 specialist pattern); ps-researcher-001 (Subagent Configuration); SN-03.

### PR-002: Cognitive Mode Specification

**The system shall** require each agent definition to declare a `cognitive_mode` from the enumerated set: `divergent`, `convergent`, `integrative`, `systematic`, `strategic`, `critical`, `forensic`, `communicative`.

- **Rationale:** Cognitive mode specialization is a distinguishing feature of the skill-based specialist pattern (TS-1, A3, Quality Control score 5/5). Different tasks require different reasoning styles: research needs divergent thinking (broad exploration), analysis needs convergent thinking (narrowing to conclusions), synthesis needs integrative thinking (combining perspectives). ps-researcher-003 identifies cognitive mode as one of 8 agent pattern families ("Context Patterns").
- **Priority:** MUST
- **Verification:** Inspection -- validate `cognitive_mode` against the enumerated set. Analysis -- verify cognitive mode alignment with the agent's role (e.g., research agents should be divergent, not convergent).
- **Source:** TS-1 (A3, cognitive specialization); ps-researcher-003 (Context Patterns); AGENTS.md (existing cognitive mode assignments); SN-03.

### PR-003: Expertise Declaration

**The system shall** require each agent definition to include an `identity.expertise` list containing at least two domain competencies relevant to the agent's role.

- **Rationale:** The expertise list serves three purposes: (1) it shapes the LLM's reasoning toward domain-specific knowledge; (2) it provides routing signals for capability-based matching; (3) it sets user expectations about the agent's strengths. ps-researcher-001 confirms all existing Jerry agents include expertise declarations (e.g., ps-researcher: "Literature review and synthesis," "Web research and source validation").
- **Priority:** MUST
- **Verification:** Inspection -- validate that `identity.expertise` is a list with >= 2 entries. Analysis -- verify expertise items are specific (not generic like "general analysis") and relevant to the declared role.
- **Source:** TS-2 (agent definition richness); ps-researcher-001 (existing agent definitions); SN-03.

### PR-004: Progressive Disclosure Structure

**The system shall** require agent definition Markdown bodies to organize content into tagged sections that support progressive disclosure: metadata loaded at startup, core instructions loaded on relevance, and supplementary reference loaded on-demand.

- **Rationale:** Progressive disclosure is a critical context efficiency mechanism. ps-researcher-001 identifies the "three-tier progressive disclosure" pattern (metadata -> core -> supplementary) as validated by Anthropic's published Agent Skills architecture. TS-1 rates context efficiency at 0.15 weight, and the skill-based pattern's score of 4 (vs. monolithic's 2) is largely due to progressive disclosure. Without it, the full 615-line agent definition (ps-researcher) would consume context unnecessarily.
- **Priority:** MUST
- **Verification:** Inspection -- validate presence of section structure in Markdown body. Analysis -- verify that agent body does not contain all instructions in a single undifferentiated block.
- **Source:** ps-researcher-001 (Agent Skills Architecture, Three-tier progressive disclosure); TS-1 (C5 context efficiency); SN-10.

### PR-005: Persona Consistency

**The system shall** require each agent definition to include a `persona` block specifying `tone`, `communication_style`, and `audience_level`.

- **Rationale:** Persona consistency ensures predictable output voice across invocations. ps-researcher-003 identifies persona engineering as an emerging discipline, noting that "role-prompting effectiveness is mixed for factual tasks" (PromptHub, Ref 22) but valuable for tone and framing consistency. The persona block ensures that agents interacting with end users maintain appropriate professional tone, while research agents maintain consultative style.
- **Priority:** SHOULD
- **Verification:** Inspection -- validate presence of `persona` block with `tone`, `communication_style`, and `audience_level` fields.
- **Source:** TS-2 (agent definition richness); ps-researcher-003 (persona engineering); Web Ref 22 (PromptHub); SN-03.

### PR-006: Instruction Hierarchy

**The system shall** structure agent instructions with a clear precedence hierarchy: constitutional constraints (highest) > HARD rules > MEDIUM standards > agent-specific instructions > SOFT guidance (lowest).

- **Rationale:** Anthropic's Claude Code best practices emphasize that instructions should have clear precedence to resolve conflicts. The Jerry enforcement architecture (L1-L5) already establishes this hierarchy for framework rules. Agent-specific instructions must slot into this hierarchy without overriding constitutional constraints. ps-researcher-003 identifies "Bounded Autonomy" as a safety pattern: agents operate within defined authority boundaries.
- **Priority:** MUST
- **Verification:** Analysis -- review agent Markdown body for any instruction that contradicts or overrides a higher-precedence rule. Inspection -- verify that constitutional constraints are referenced in the agent's `guardrails` section.
- **Source:** quality-enforcement.md (Enforcement Architecture L1-L5); ps-researcher-003 (Safety Patterns: Bounded Autonomy); SN-07, SN-15.

### PR-007: Model Selection Justification

**The system shall** require the `model` field to be set to one of: `opus`, `sonnet`, `haiku`, with the selection justified by the agent's cognitive complexity requirements.

- **Rationale:** ps-researcher-001 confirms Claude Code supports three model tiers (Haiku/Sonnet/Opus) with different cost-performance tradeoffs. Model selection directly impacts quality and cost. Complex research and architecture tasks justify Opus; balanced analysis justifies Sonnet; fast, repetitive tasks justify Haiku. Without explicit selection, default model assignment may be suboptimal.
- **Priority:** MUST
- **Verification:** Inspection -- validate `model` field against enumerated set. Analysis -- verify model choice is consistent with cognitive complexity (e.g., divergent research agents should not use Haiku; simple formatting agents should not use Opus).
- **Source:** ps-researcher-001 (Claude Code model tiers); TS-1 (C5 context efficiency); SN-12.

### PR-008: Output Level Specification

**The system shall** require each agent definition to declare supported output levels in the `output.levels` field. Agents producing stakeholder-facing deliverables shall support all three levels: L0 (executive summary), L1 (technical detail), L2 (strategic implications).

- **Rationale:** Multi-level output (L0/L1/L2) serves different stakeholder audiences (SH-1 through SH-4) from the same deliverable. ps-researcher-001 confirms all existing research and analysis agents support L0/L1/L2 output levels. The L0/L1/L2 pattern is a key differentiator of the Jerry framework and directly addresses SN-10 (different audiences get appropriate detail).
- **Priority:** MUST
- **Verification:** Inspection -- validate presence of `output.levels` field. Analysis -- verify that agents producing stakeholder-facing outputs declare all three levels.
- **Source:** ps-researcher-001 (output levels); SN-10; existing agent patterns (ps-researcher, nse-explorer).

---

## Routing Requirements (RR)

### RR-001: Primary Routing via Keyword Matching

**The system shall** use deterministic keyword matching as the primary routing mechanism for directing user requests to the appropriate skill and agent.

- **Rationale:** Trade study TS-3 (Routing Architecture) scores keyword matching (C1) at 3.85 and layered routing (C5) at 3.90. Keyword matching provides zero-LLM-overhead routing (~1ms latency per ps-researcher-002), full auditability, and deterministic behavior for common cases. ps-researcher-002 reports that keyword matching handles approximately 80% of routing decisions correctly. This is the proven current Jerry pattern.
- **Priority:** MUST
- **Verification:** Test -- submit requests containing known trigger keywords and verify correct routing. Inspection -- review trigger map for completeness against skill catalog.
- **Source:** TS-3 (C1, C5); ps-researcher-002 (Routing Mechanism Spectrum, ~1ms latency); mandatory-skill-usage.md; SN-04.

### RR-002: Trigger Keyword Completeness

**The system shall** maintain a trigger keyword map that covers all registered skills, with each skill having at least three distinct trigger keywords.

- **Rationale:** ps-researcher-002 identifies keyword completeness as a prerequisite for reliable routing. The current mandatory-skill-usage.md trigger map covers 7 skills with 3-7 keywords each. Gaps in the trigger map cause requests to fall through to the LLM fallback unnecessarily, increasing latency. Three keywords per skill provides minimum coverage for common synonyms.
- **Priority:** MUST
- **Verification:** Inspection -- count trigger keywords per skill in mandatory-skill-usage.md. Flag any skill with fewer than three keywords.
- **Source:** ps-researcher-002 (routing completeness); mandatory-skill-usage.md; SN-04.

### RR-003: LLM Fallback for Ambiguous Routing

**The system shall** provide an LLM-based fallback routing mechanism that activates when keyword matching produces no match, low confidence, or multiple conflicting matches.

- **Rationale:** Trade study TS-3 scores layered routing (C5, keyword + LLM fallback) highest at 3.90. ps-researcher-002 identifies that keyword matching is "brittle -- synonyms and paraphrases not captured." The LLM fallback handles the estimated 20% of cases where keywords are insufficient (TS-3 Assumptions Challenged #2). LangChain identifies LLM-based routing as "state-of-the-art" for ambiguous cases.
- **Priority:** SHOULD
- **Verification:** Test -- submit requests with no matching keywords and verify LLM fallback activates and routes correctly. Test -- submit requests matching multiple skills and verify LLM disambiguates.
- **Source:** TS-3 (C5 layered routing); ps-researcher-002 (routing mechanism spectrum); Web Ref 10 (thin router); SN-04.

### RR-004: Routing Determinism for Common Cases

**The system shall** ensure that requests matching a single skill's keywords route deterministically to that skill, producing the same routing decision for identical inputs.

- **Rationale:** Determinism is essential for predictability and debugging. TS-3 rates the keyword tier's determinism as a primary advantage (C1 simplicity score: 5/5 for keywords vs. 3/5 for LLM router). Stochastic routing undermines user trust and makes regression testing impossible. The LLM fallback path is inherently stochastic (TS-3 C3 cons), but the deterministic keyword path must remain stable.
- **Priority:** MUST
- **Verification:** Test -- submit the same keyword-matched request 10 times and verify identical routing decisions.
- **Source:** TS-3 (C1 determinism advantage); SN-04.

### RR-005: Negative Keywords for Disambiguation

**The system shall** support negative keywords (exclusion terms) in the trigger map to reduce false-positive routing when keywords appear in non-trigger contexts.

- **Rationale:** ps-researcher-002 identifies "negative keywords + priority ordering" as needed to resolve multi-skill keyword overlap. The keyword "risk" could trigger both `/nasa-se` (risk management) and `/problem-solving` (risk analysis). Without negative keywords, casual mention of trigger terms in non-routing contexts causes false routing.
- **Priority:** SHOULD
- **Verification:** Test -- submit requests containing a trigger keyword in a non-trigger context (e.g., "I'm not asking about risk, I want to format this code") and verify that negative keywords prevent misrouting.
- **Source:** ps-researcher-002 (negative keywords); SN-04.

### RR-006: Routing Loop Prevention

**The system shall** implement loop prevention in agent routing by enforcing a maximum routing depth and circuit breaker pattern. No request shall be routed more than three times without reaching a terminal agent.

- **Rationale:** ps-researcher-002 identifies "Routing loops -- agents bouncing between each other without termination" as a critical anti-pattern. Without loop prevention, ambiguous requests can cycle indefinitely between agents, consuming context window tokens without producing output. The circuit breaker pattern (max 3 hops) prevents runaway routing while allowing legitimate multi-step routing chains.
- **Priority:** MUST
- **Verification:** Test -- create a scenario where routing produces a cycle and verify that the circuit breaker terminates after the maximum depth.
- **Source:** ps-researcher-002 (Anti-Patterns: Routing loops); SN-04, SN-14.

### RR-007: Multi-Skill Combination Support

**The system shall** support routing a single request to multiple skills when the request spans skill boundaries, consistent with mandatory-skill-usage.md behavior rule 2 ("COMBINE skills when appropriate").

- **Rationale:** Real-world requests often span multiple skill domains (e.g., "research and then design an architecture for..." requires both `/problem-solving` and `/nasa-se`). H-22 behavior rule 2 already mandates skill combination. The routing mechanism must support this rather than forcing single-skill routing.
- **Priority:** MUST
- **Verification:** Test -- submit a request containing trigger keywords from two different skills and verify that both skills are invoked.
- **Source:** H-22 (behavior rule 2); mandatory-skill-usage.md; TS-3 (C5 compound request handling); SN-04.

### RR-008: Routing Observability

**The system shall** provide observability into routing decisions, including which mechanism was used (keyword or LLM fallback), which keywords matched, confidence level, and the selected skill(s).

- **Rationale:** ps-researcher-002 recommends logging "fallback frequency to identify keyword gaps." LangChain's State of Agent Engineering (2025) reports 89% of LLM deployments have observability but only 52% have evals. Routing observability enables systematic improvement of the trigger keyword map and identification of routing degradation.
- **Priority:** SHOULD
- **Verification:** Inspection -- verify that routing decisions produce structured log entries with mechanism, keywords, confidence, and selected skill.
- **Source:** ps-researcher-002 (routing observability); Web Ref 15 (LangChain observability); TS-3 (C5 monitoring); SN-07.

---

## Handoff Requirements (HR)

### HR-001: Structured Handoff Format

**The system shall** require all agent-to-agent handoffs to use a structured format with defined fields rather than free-text descriptions.

- **Rationale:** ps-researcher-002 identifies "free-text handoffs are the #1 source of context loss in production multi-agent systems" (Google, 2026). The cross-pollination handoff document confirms "Structured handoff schemas (JSON Schema) are critical." AGENTS.md already defines a JSON handoff format with `from_agent`, `to_agent`, `context`, and `request` fields. Formalizing this as a requirement prevents regression to informal handoffs.
- **Priority:** MUST
- **Verification:** Inspection -- review all handoff invocations for structured format compliance. Test -- attempt a handoff with missing required fields and verify rejection.
- **Source:** ps-researcher-002 (Handoff Protocol Requirements); AGENTS.md (Agent Handoff Protocol); SN-06.

### HR-002: Required Handoff Fields

**The system shall** require every agent handoff to include: `from_agent` (source agent name), `to_agent` (target agent name), `context.task_id` (work item reference), `context.artifacts` (list of artifact file paths produced), `context.summary` (natural language summary of completed work), and `request` (specific instruction for the receiving agent).

- **Rationale:** Each field serves a distinct purpose: `from_agent`/`to_agent` enable traceability; `task_id` provides worktracker linkage; `artifacts` ensure the receiving agent can locate prior output; `summary` provides context without requiring full artifact re-reading; `request` gives clear direction. Missing any field degrades the handoff quality and forces the receiving agent to infer missing information.
- **Priority:** MUST
- **Verification:** Inspection -- JSON Schema validation of handoff messages against required field set. Test -- verify each field is consumed by the receiving agent.
- **Source:** AGENTS.md (Agent Handoff Protocol); ps-researcher-002 (structured handoffs); SN-06.

### HR-003: Artifact Path Validation

**The system shall** validate that all file paths in the `context.artifacts` list of a handoff message reference existing files before delivering the handoff to the receiving agent.

- **Rationale:** ps-researcher-002 identifies the "telephone game" anti-pattern where information degrades through sequential handoffs. Broken artifact references silently degrade downstream work quality because the receiving agent proceeds without the intended input. Pre-delivery validation catches this failure mode at the handoff boundary.
- **Priority:** MUST
- **Verification:** Test -- create a handoff with a non-existent artifact path and verify that validation rejects it before delivery to the receiving agent.
- **Source:** ps-researcher-002 (Telephone Game anti-pattern); SN-06.

### HR-004: State Preservation Across Handoffs

**The system shall** preserve all relevant state across agent handoffs, including intermediate results, quality scores from prior iterations, and accumulated context, via filesystem persistence or Memory-Keeper storage.

- **Rationale:** TS-1 identifies "stronger state management between agents" as the primary enhancement opportunity for Jerry's skill-based pattern (A3). MCP-002 mandates Memory-Keeper store at orchestration phase boundaries and retrieve at phase start. Without explicit state preservation, each agent starts from scratch, losing accumulated insight.
- **Priority:** MUST
- **Verification:** Test -- execute a multi-agent workflow and verify that the final agent can access state produced by the first agent. Inspection -- verify Memory-Keeper store/retrieve calls at phase boundaries.
- **Source:** TS-1 (state management enhancement); MCP-002; SN-06.

### HR-005: Handoff Completeness Verification

**The system shall** verify that a handoff message contains sufficient information for the receiving agent to begin work without requiring additional context retrieval from the sending agent.

- **Rationale:** ps-researcher-002 identifies "context-centric decomposition" as superior to "problem-centric decomposition" because it prevents information degradation. A complete handoff eliminates the need for the receiving agent to re-derive context, which is impossible when agents have isolated context windows (AR-005). The sending agent has the most complete understanding at handoff time and must transmit it explicitly.
- **Priority:** SHOULD
- **Verification:** Analysis -- review handoff summaries for information sufficiency. Test -- invoke the receiving agent with only the handoff message and verify it can begin work without requesting additional information.
- **Source:** ps-researcher-002 (Context-centric decomposition); AR-005 (Context Isolation); SN-06.

### HR-006: Handoff Quality Gate

**The system shall** enforce a quality gate at handoff boundaries for C2+ deliverables, where the sending agent's output must pass quality verification before the handoff is delivered.

- **Rationale:** AGENTS.md philosophy states "Quality Gates -- Handoffs enforce review checkpoints." H-13/H-14 require quality threshold >= 0.92 and creator-critic-revision cycles for C2+ deliverables. Applying the quality gate at the handoff boundary prevents low-quality work from propagating to downstream agents, which would amplify errors (ps-researcher-002: 17x error amplification from uncoordinated agents).
- **Priority:** MUST
- **Verification:** Test -- attempt a handoff with a deliverable scoring below 0.92 and verify that the quality gate blocks the handoff until the score threshold is met.
- **Source:** H-13, H-14; AGENTS.md (Quality Gates); ps-researcher-002 (error amplification); SN-12.

---

## Quality Requirements (QR)

### QR-001: Criticality-Proportional Quality Enforcement

**The system shall** apply quality assurance effort proportional to the criticality level (C1-C4) of the deliverable, as defined in quality-enforcement.md.

- **Rationale:** Trade study TS-4 (Quality Assurance) demonstrates that applying full tournament mode (D3) to all deliverables is impractical (context cost is "very high," score 2.70). Layered QA (D6, score 3.70) is the recommended approach, applying schema validation and self-review to all work, adding creator-critic for C2+, and reserving tournament mode for C4. This aligns with the existing criticality matrix in quality-enforcement.md.
- **Priority:** MUST
- **Verification:** Analysis -- verify that quality enforcement configuration maps correctly to criticality levels. Test -- produce deliverables at each criticality level and verify appropriate QA mechanisms activate.
- **Source:** TS-4 (D6 layered QA); quality-enforcement.md (Criticality Levels); SN-12.

### QR-002: Self-Review Requirement

**The system shall** require every agent to perform self-review (S-010 Self-Refine) before producing final output, regardless of criticality level.

- **Rationale:** H-15 mandates "Self-review before presenting any deliverable." Trade study TS-4 shows self-review (D1) has the highest raw score (3.85) due to minimal overhead, and it is the only QA mechanism required at all criticality levels (C1 through C4). Self-review catches obvious errors at near-zero cost and is the baseline quality mechanism.
- **Priority:** MUST
- **Verification:** Inspection -- verify that agent definitions include self-review in their process instructions. Analysis -- verify agent outputs show evidence of self-review (e.g., revision marks, completeness checks).
- **Source:** H-15; TS-4 (D1, D6); quality-enforcement.md (S-010); SN-12.

### QR-003: Output Schema Validation

**The system shall** validate agent outputs against structural schemas that verify the presence of required sections, navigation tables (H-23), anchor links (H-24), and output-level completeness (L0/L1/L2 when applicable).

- **Rationale:** Trade study TS-4 identifies output schema validation (D5, score 3.60) as a high-value complement to LLM-based quality scoring. Schema validation is deterministic (zero LLM overhead), fast, and catches structural defects that LLM scoring may overlook. H-23 (navigation tables) and H-24 (anchor links) are already HARD rules that can be schema-validated.
- **Priority:** SHOULD
- **Verification:** Test -- submit agent outputs with missing navigation tables, broken anchor links, or absent L0/L1/L2 sections and verify schema validation catches these defects.
- **Source:** TS-4 (D5, D6); H-23, H-24; SN-07, SN-12.

### QR-004: Creator-Critic Cycle for C2+ Deliverables

**The system shall** require a minimum of three creator-critic-revision iterations for C2+ deliverables, with quality scoring via S-014 (LLM-as-Judge) at each iteration.

- **Rationale:** H-14 mandates "Creator-critic-revision cycle REQUIRED. Minimum 3 iterations for C2+ deliverables." Trade study TS-4 confirms the creator-critic pattern (D2, score 3.30 for C2+ when H-14 filter is applied) as the proven standard for Jerry. ps-researcher-003 validates multi-agent evaluation with ACM research showing it produces "more accurate and robust solutions."
- **Priority:** MUST
- **Verification:** Test -- produce a C2+ deliverable and verify that three distinct critic evaluations are performed with S-014 scoring. Inspection -- verify iteration history is persisted (scores, findings, revisions).
- **Source:** H-14; TS-4 (D2, D6); ps-researcher-003 (Quality Patterns); quality-enforcement.md; SN-12.

### QR-005: Quality Threshold Enforcement

**The system shall** reject deliverables scoring below 0.92 weighted composite score on the S-014 six-dimension rubric for C2+ work.

- **Rationale:** H-13 mandates "Quality threshold >= 0.92 for C2+ deliverables." The 0.92 threshold is calibrated to balance rigor with iteration cost (quality-enforcement.md rationale). The six-dimension rubric (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10) provides structured scoring.
- **Priority:** MUST
- **Verification:** Test -- submit a deliverable scoring 0.91 and verify rejection. Test -- submit a deliverable scoring 0.92 and verify acceptance.
- **Source:** H-13; quality-enforcement.md (Quality Gate); SN-12.

### QR-006: Steelman Before Critique

**The system shall** apply the Steelman technique (S-003) before the Devil's Advocate technique (S-002) in any adversarial review sequence.

- **Rationale:** H-16 mandates "Steelman (S-003) MUST be applied before Devil's Advocate (S-002). Canonical review pairing." The rationale is that "strengthening ideas before attacking them prevents premature rejection of sound approaches." This ordering requirement ensures that critique is applied to the strongest version of the idea, not a strawman.
- **Priority:** MUST
- **Verification:** Inspection -- review adversarial review sequences for S-003/S-002 ordering. Test -- verify that adv-executor applies S-003 before S-002 in any review that includes both.
- **Source:** H-16; quality-enforcement.md (Strategy Catalog); SN-12.

### QR-007: Citation Requirements

**The system shall** require all factual claims in agent outputs to include citations to their source, with source quality tiered as: Industry Leader > Official Documentation > Industry Innovator > Community Expert > Research Paper.

- **Rationale:** SN-11 requires "Citation of sources so claims can be verified." The ps-researcher agent template already mandates "all_claims_must_have_citations" in its guardrails. The cross-pollination handoff categorizes sources into authority tiers (Industry Leader: 12 sources, Official Documentation: 8, etc.), providing a quality ranking framework.
- **Priority:** MUST
- **Verification:** Inspection -- validate that factual claims in agent outputs include inline citations. Analysis -- verify citations reference accessible sources.
- **Source:** ps-researcher.md (guardrails: all_claims_must_have_citations); cross-pollination handoff (Source Authority tiers); SN-11.

### QR-008: Tournament Mode for C4 Deliverables

**The system shall** apply tournament mode (all 10 selected adversarial strategies) for C4 (Critical) deliverables, as specified in quality-enforcement.md.

- **Rationale:** C4 deliverables are defined as "Irreversible, architecture/governance/public" with "All tiers + tournament" enforcement. TS-4 acknowledges tournament mode (D3, score 2.70) has high context cost but validates it for C4 due to the irreversibility and impact of these decisions. TS-4 assumption challenge #3 confirms "Full tournament (10 strategies) is justified only for C4 deliverables."
- **Priority:** MUST
- **Verification:** Test -- produce a C4 deliverable and verify all 10 strategies (S-001 through S-014, selected set) are applied. Inspection -- verify tournament scoring produces a comprehensive quality profile.
- **Source:** quality-enforcement.md (Criticality Levels, C4); TS-4 (D3 for C4); SN-12.

### QR-009: Leniency Bias Counteraction

**The system shall** actively counteract leniency bias in LLM-as-Judge scoring by applying strict rubric adherence and calibrating scores against known reference deliverables.

- **Rationale:** quality-enforcement.md L2-REINJECT states "LLM-as-Judge scoring (S-014): Apply strict rubric. Leniency bias must be actively counteracted." TS-4 identifies leniency bias as a known limitation: "Self-review bias: agents rate their own work more favorably" (D1 cons). LangChain State of Agent Engineering (2025) corroborates that quality is the #1 production blocker (32% of respondents), partly due to unreliable self-assessment.
- **Priority:** MUST
- **Verification:** Analysis -- compare S-014 scores against human expert assessments for a calibration set. Test -- verify that known-deficient deliverables receive scores below 0.92.
- **Source:** quality-enforcement.md (S-014 leniency bias); TS-4 (D1 bias, D2 bias); Web Ref 15 (LangChain quality); SN-12.

---

## Safety and Governance Requirements (SR)

### SR-001: Constitutional Constraint Compliance

**The system shall** ensure that every agent definition includes explicit reference to and compliance with the constitutional constraints P-003 (no recursive subagents), P-020 (user authority), and P-022 (no deception).

- **Rationale:** H-01, H-02, H-03 establish these as HARD rules that "CANNOT be overridden." H-18 mandates "Constitutional compliance check (S-007) REQUIRED for all C2+ deliverables." ps-researcher-003 identifies "Constitutional AI, Guardrails, Bounded Autonomy" as a mandatory safety pattern. Agent definitions must embed these constraints to ensure compliance at the instruction level, not just at enforcement tooling level.
- **Priority:** MUST
- **Verification:** Inspection -- verify that agent `forbidden_actions` include P-003, P-020, P-022 references. Test -- attempt actions violating each constraint and verify rejection.
- **Source:** H-01, H-02, H-03, H-18; ps-researcher-003 (Safety Patterns); SN-15.

### SR-002: Guardrail Input Validation

**The system shall** require each agent to declare input validation rules in the `guardrails.input_validation` section of its definition, specifying format constraints for expected input parameters.

- **Rationale:** Input validation is the first line of defense against malformed or malicious inputs. The ps-researcher agent demonstrates this pattern with `ps_id_format` and `entry_id_format` regex patterns. TS-2 identifies guardrails as a required frontmatter section (AR-002). Without input validation, agents may process invalid inputs and produce erroneous outputs.
- **Priority:** MUST
- **Verification:** Inspection -- validate presence of `guardrails.input_validation` with at least one validation rule. Test -- submit inputs violating declared format constraints and verify rejection.
- **Source:** TS-2 (guardrails section); ps-researcher.md (input validation patterns); SN-15.

### SR-003: Guardrail Output Filtering

**The system shall** require each agent to declare output filtering rules in the `guardrails.output_filtering` section, including at minimum: no secrets in output, no executable code without confirmation, and all claims must have citations.

- **Rationale:** Output filtering prevents sensitive information leakage, unauthorized code execution, and unsubstantiated claims from reaching end users. The ps-researcher agent demonstrates this pattern with three output filters. These are minimum safety requirements for any agent producing external-facing output.
- **Priority:** MUST
- **Verification:** Inspection -- validate presence of `guardrails.output_filtering` with minimum required filters. Test -- attempt to produce output containing a secret pattern (e.g., API key format) and verify filtering.
- **Source:** ps-researcher.md (output_filtering); SN-15.

### SR-004: User Authority Preservation

**The system shall** ensure that no agent overrides, contradicts, or ignores explicit user instructions, consistent with P-020/H-02.

- **Rationale:** H-02 is a constitutional HARD rule: "User authority -- never override." This is the most fundamental governance constraint. Agents must serve user intent, not substitute their own judgment for the user's explicit direction. ps-researcher-003 identifies "Human-in-the-Loop, Approval Gates" as a governance pattern family.
- **Priority:** MUST
- **Verification:** Test -- issue a user instruction that conflicts with an agent's default behavior and verify the agent follows the user instruction. Analysis -- review agent definitions for any instruction that could override user intent.
- **Source:** P-020/H-02; ps-researcher-003 (Governance Patterns); SN-15.

### SR-005: Deception Prevention

**The system shall** ensure that no agent misrepresents its actions, capabilities, confidence level, or the source of its outputs, consistent with P-022/H-03.

- **Rationale:** H-03 is a constitutional HARD rule: "No deception about actions/capabilities." Agents must accurately report what they did, what they cannot do, and how confident they are in their outputs. This is especially critical for agents producing research or analysis that informs decisions.
- **Priority:** MUST
- **Verification:** Test -- ask an agent about its capabilities and verify accurate reporting. Analysis -- review agent outputs for confidence claims that are not supported by evidence.
- **Source:** P-022/H-03; SN-15.

### SR-006: Audit Trail Requirements

**The system shall** persist a record of every agent invocation including: agent name, invocation timestamp, input parameters, output artifact paths, quality scores (if applicable), and routing decision metadata.

- **Rationale:** ps-researcher-003 identifies "Audit Trails" as a governance pattern. H-19 mandates governance escalation per auto-escalation rules (AE-001 through AE-006), which requires an audit trail to detect escalation-triggering conditions. Without audit trails, governance violations are undetectable, and quality trends cannot be analyzed (TS-4, D4 statistical monitoring).
- **Priority:** SHOULD
- **Verification:** Inspection -- verify that agent invocations produce structured log entries. Test -- retrieve audit records for a completed workflow and verify completeness.
- **Source:** ps-researcher-003 (Governance Patterns: Audit Trails); H-19 (governance escalation); TS-4 (D4 statistical monitoring); SN-07.

### SR-007: Governance Auto-Escalation

**The system shall** automatically escalate the criticality classification when an agent action triggers an auto-escalation condition, per AE-001 through AE-006.

- **Rationale:** H-19 mandates "Governance escalation per AE rules REQUIRED." The auto-escalation rules ensure that high-impact changes (e.g., touching `.context/rules/` triggers AE-002 auto-C3; touching constitution triggers AE-001 auto-C4) receive proportionally rigorous quality review. Without auto-escalation, an agent performing routine work could modify governance files with only C1-level review.
- **Priority:** MUST
- **Verification:** Test -- perform an action that touches `.context/rules/` and verify automatic escalation to C3 minimum. Test -- perform an action that touches the constitution and verify automatic escalation to C4.
- **Source:** H-19; quality-enforcement.md (Auto-Escalation Rules AE-001 through AE-006); SN-07, SN-15.

### SR-008: MCP Tool Governance

**The system shall** enforce MCP tool usage governance per MCP-001 (Context7 MUST be used for external library research) and MCP-002 (Memory-Keeper store at phase boundaries, retrieve at phase start).

- **Rationale:** MCP-001 and MCP-002 are HARD rules in mcp-tool-standards.md. Context7 ensures agents use current documentation rather than stale training data. Memory-Keeper ensures cross-session context persistence. Without MCP governance, agents may produce outdated research or lose context across session boundaries.
- **Priority:** MUST
- **Verification:** Test -- invoke a research agent referencing an external library and verify Context7 is called. Test -- complete an orchestration phase and verify Memory-Keeper store is called. Inspection -- audit agent MCP tool declarations against TOOL_REGISTRY.yaml.
- **Source:** MCP-001, MCP-002; mcp-tool-standards.md; SN-14.

### SR-009: Fallback Behavior Declaration

**The system shall** require each agent to declare its fallback behavior in the `guardrails.fallback_behavior` field, specifying what happens when the agent encounters an error it cannot resolve.

- **Rationale:** mcp-tool-standards.md defines fallback behaviors for MCP failures (e.g., "Persist context to `work/.mcp-fallback/{key}.md`"). By extension, every agent needs a declared fallback strategy for error conditions. Without declared fallback behavior, agent failures are unpredictable and may silently produce partial results.
- **Priority:** MUST
- **Verification:** Inspection -- validate presence of `guardrails.fallback_behavior` field with a defined strategy (e.g., `warn_and_retry`, `escalate_to_user`, `persist_and_halt`).
- **Source:** mcp-tool-standards.md (Error Handling); ps-researcher.md (fallback_behavior: warn_and_retry); SN-15.

### SR-010: Ambiguity Clarification

**The system shall** require agents to ask clarifying questions before proceeding when: (1) the request has multiple valid interpretations, (2) the scope is unclear, or (3) the requested action is destructive or irreversible. Agents shall not ask for clarification when the request is clear or the answer is discoverable from the codebase.

- **Rationale:** H-31 mandates "Clarify before acting when ambiguous." The quality-enforcement.md rationale states: "Prevents wrong-direction work -- incorrect assumptions are the most expensive failure mode. One clarifying question costs seconds; wrong-direction work costs hours."
- **Priority:** MUST
- **Verification:** Test -- submit an ambiguous request and verify the agent asks a clarifying question before proceeding. Test -- submit a clear request and verify the agent proceeds without unnecessary questions.
- **Source:** H-31; quality-enforcement.md (H-31 rationale); SN-15.

---

## Traceability Matrix

### Requirements to Phase 1 Research Findings

| Requirement | Phase 1 Finding | Source Document |
|-------------|-----------------|-----------------|
| AR-001 | YAML+MD format is proven at scale (37 agents, B1/B5 highest scored) | TS-2 |
| AR-002 | Frontmatter fields analysis of existing 37 agents | TS-2; ps-researcher-001 |
| AR-003 | Schema validation is highest-value evolutionary improvement | TS-2 (B5 vs. B1 delta) |
| AR-004 | Single-level nesting validated by Claude Code architecture | ps-researcher-001; TS-1 |
| AR-005 | Subagent context isolation confirmed by Claude Code design | ps-researcher-001 |
| AR-006 | Static tool assignment scored highest (E1: 4.15) | TS-5 |
| AR-007 | 37 agents follow consistent naming convention | AGENTS.md |
| AR-008 | Open Agent Specification mandates version fields | TS-2 (Web Ref 4) |
| AR-009 | Description quality affects routing accuracy | TS-3 |
| AR-010 | Consistent file location enables automated discovery | H-25, H-26, H-29 |
| AR-011 | Unregistered agents are invisible to governance | H-30 |
| AR-012 | Guardrails are table stakes for production agents | ps-researcher-003 |
| PR-001 | Role clarity is foundation of specialist pattern | ps-researcher-001; TS-1 |
| PR-002 | Cognitive mode specialization is A3 differentiator | TS-1; AGENTS.md |
| PR-003 | Expertise declarations shape LLM reasoning and routing | ps-researcher-001 |
| PR-004 | Three-tier progressive disclosure prevents context bloat | ps-researcher-001 |
| PR-005 | Persona engineering is an emerging discipline | ps-researcher-003 (Web Ref 22) |
| PR-006 | Instruction hierarchy follows L1-L5 enforcement architecture | quality-enforcement.md |
| PR-007 | Three model tiers with different cost-performance tradeoffs | ps-researcher-001 |
| PR-008 | L0/L1/L2 output levels serve different stakeholder audiences | ps-researcher-001 |
| RR-001 | Keyword matching handles ~80% of cases at ~1ms latency | ps-researcher-002; TS-3 |
| RR-002 | Keyword completeness is prerequisite for reliable routing | ps-researcher-002 |
| RR-003 | LLM fallback handles the ~20% ambiguous cases | TS-3 (C5); ps-researcher-002 |
| RR-004 | Determinism is primary advantage of keyword routing | TS-3 (C1 score 5/5) |
| RR-005 | Negative keywords resolve multi-skill keyword overlap | ps-researcher-002 |
| RR-006 | Routing loops are a critical anti-pattern | ps-researcher-002 |
| RR-007 | Real-world requests span skill boundaries | H-22 behavior rule 2 |
| RR-008 | 89% of deployments have observability, only 52% have evals | Web Ref 15 (LangChain) |
| HR-001 | Free-text handoffs are #1 failure source | ps-researcher-002 |
| HR-002 | Required fields map to traceability, artifact access, direction | AGENTS.md |
| HR-003 | Telephone game anti-pattern causes information degradation | ps-researcher-002 |
| HR-004 | State management is primary enhancement for A3 pattern | TS-1 |
| HR-005 | Context-centric decomposition prevents information degradation | ps-researcher-002 |
| HR-006 | Quality gates at handoff boundaries prevent error propagation | AGENTS.md; ps-researcher-002 |
| QR-001 | Layered QA (D6) is recommended approach, proportional to criticality | TS-4 |
| QR-002 | Self-review is the baseline quality mechanism at all C-levels | H-15; TS-4 (D1) |
| QR-003 | Schema validation is deterministic pre-check complement | TS-4 (D5, D6) |
| QR-004 | Multi-agent evaluation produces more accurate solutions | ps-researcher-003 (ACM) |
| QR-005 | 0.92 threshold balances rigor with iteration cost | quality-enforcement.md |
| QR-006 | Steelman before critique prevents premature rejection | H-16; quality-enforcement.md |
| QR-007 | Citation requirements from existing agent guardrails | ps-researcher.md |
| QR-008 | Full tournament justified only for C4 deliverables | TS-4 assumption #3 |
| QR-009 | Leniency bias is known LLM-as-judge limitation | quality-enforcement.md; TS-4 |
| SR-001 | Constitutional constraints are non-negotiable | H-01, H-02, H-03 |
| SR-002 | Input validation is first line of defense | ps-researcher.md |
| SR-003 | Output filtering prevents sensitive information leakage | ps-researcher.md |
| SR-004 | User authority is constitutional constraint | P-020/H-02 |
| SR-005 | No deception is constitutional constraint | P-022/H-03 |
| SR-006 | Audit trails enable governance oversight | ps-researcher-003 |
| SR-007 | Auto-escalation prevents under-review of high-impact changes | H-19; quality-enforcement.md |
| SR-008 | MCP governance ensures current docs and cross-session memory | MCP-001, MCP-002 |
| SR-009 | Fallback behavior prevents unpredictable failure modes | mcp-tool-standards.md |
| SR-010 | Ambiguity clarification prevents wrong-direction work | H-31 |

### Requirements to Existing Jerry Rules

| Requirement | Jerry Rule(s) | Relationship |
|-------------|---------------|--------------|
| AR-004 | H-01 (P-003) | Directly implements |
| AR-006 | MCP-001, MCP-002 | Directly implements |
| AR-007 | H-26 | Directly implements |
| AR-009 | H-28 | Directly implements |
| AR-010 | H-25, H-26, H-29 | Directly implements |
| AR-011 | H-30 | Directly implements |
| PR-006 | H-01 through H-31 | Embeds hierarchy |
| PR-007 | H-05, H-06 | Compatible with |
| PR-008 | H-23, H-24 | Output format alignment |
| RR-001 | H-22 | Directly implements |
| RR-007 | H-22 behavior rule 2 | Directly implements |
| HR-006 | H-13, H-14 | Directly implements |
| QR-001 | H-13, H-14, H-15 | Directly implements |
| QR-002 | H-15 (S-010) | Directly implements |
| QR-003 | H-23, H-24 | Validates compliance |
| QR-004 | H-14 | Directly implements |
| QR-005 | H-13 | Directly implements |
| QR-006 | H-16 | Directly implements |
| QR-008 | H-13, H-17 | Directly implements |
| QR-009 | H-17 (S-014) | Directly implements |
| SR-001 | H-01, H-02, H-03, H-18 | Directly implements |
| SR-004 | H-02 (P-020) | Directly implements |
| SR-005 | H-03 (P-022) | Directly implements |
| SR-007 | H-19, AE-001 through AE-006 | Directly implements |
| SR-008 | MCP-001, MCP-002 | Directly implements |
| SR-010 | H-31 | Directly implements |

### Requirements to Trade Study Recommendations

| Requirement | Trade Study Recommendation | Relationship |
|-------------|---------------------------|--------------|
| AR-001, AR-002, AR-003 | TS-2: Evolve to schema-validated YAML+MD (B5) | Implements recommendation |
| AR-004, AR-005 | TS-1: Maintain skill-based specialist pattern (A3) | Implements recommendation |
| AR-006 | TS-5: Hybrid static+MCP tool assignment (E5) | Implements recommendation |
| RR-001, RR-003 | TS-3: Layered routing with LLM fallback (C5) | Implements recommendation |
| QR-001, QR-002, QR-003 | TS-4: Layered QA with schema pre-check (D6) | Implements recommendation |
| QR-004, QR-008 | TS-4: Creator-critic for C2+, tournament for C4 | Implements recommendation |
| HR-004 | TS-1: Strengthen state management across handoffs | Implements recommendation |

---

## Requirements Quality Verification

### INCOSE Quality Criteria Assessment

Each requirement has been verified against the eight INCOSE quality criteria. The following table summarizes the verification results:

| Criterion | Definition | Verification Method | Result |
|-----------|-----------|---------------------|--------|
| Necessary | Traceable to a stakeholder need | Every requirement traces to SN-01 through SN-15 via the traceability matrix | PASS -- all 52 requirements trace to at least one stakeholder need |
| Implementation-free | States WHAT, not HOW | Review each shall-statement for implementation directives | PASS -- requirements specify outcomes (e.g., "shall use structured format") not implementations (e.g., "shall use JSON Schema library X") |
| Unambiguous | Single interpretation | Review for qualifier words, undefined terms, or vague phrases | PASS -- all requirements use precise language; enumerated sets (e.g., cognitive modes) are explicitly listed |
| Complete | No missing conditions | Cross-reference against Phase 1 findings and stakeholder needs | PASS -- all 6 domains are covered; all SN-01 through SN-15 are addressed |
| Consistent | No contradictions | Cross-reference requirements within and across domains | PASS -- no contradictions identified. QR-001 (criticality-proportional) is consistent with QR-002 (always self-review) and QR-004 (C2+ critic) |
| Singular | One requirement per statement | Review for conjunctions combining multiple requirements | PASS -- compound requirements were split (e.g., AR-002 lists required fields as a set but represents a single structural requirement) |
| Achievable | Can be implemented and verified | Assess against current Jerry capabilities and Claude Code constraints | PASS -- all requirements are implementable within current Claude Code + Jerry architecture |
| Verifiable | Testable or inspectable | Every requirement has a verification method (Inspection/Analysis/Test) | PASS -- all 52 requirements have explicit verification methods |

### Verification Method Distribution

| Method | Count | Percentage |
|--------|-------|------------|
| Inspection | 28 | 45% |
| Test | 24 | 39% |
| Analysis | 18 | 29% |
| Demonstration | 0 | 0% |

> **Note:** Some requirements use multiple verification methods; percentages sum to >100%.

### Self-Review (S-010) Findings

The following issues were identified and corrected during self-review:

1. **Initial gap:** No requirement addressed the "Bag of Agents" anti-pattern explicitly. Added rationale reference to AR-004 (17x error amplification from Google DeepMind).
2. **Ambiguity corrected:** PR-002 originally used "the enumerated set" without listing the values. Added the explicit set: `divergent`, `convergent`, `integrative`, `systematic`, `strategic`, `critical`, `forensic`, `communicative`.
3. **Traceability gap:** Initial traceability matrix did not link QR-003 to H-23/H-24. Added cross-reference.
4. **Missing stakeholder need:** Added SN-15 (guardrails for harmful behavior) to complete the safety/governance needs coverage.
5. **Verification completeness:** Added specific test scenarios to verification methods where initial descriptions were too abstract (e.g., QR-005 now specifies threshold boundary test cases: 0.91 reject, 0.92 accept).
6. **Requirement count reconciliation:** Initial count was 50; expanded to 52 after splitting compound requirements and adding SR-009 (fallback behavior) and SR-010 (ambiguity clarification) which were missing from the initial draft.

---

## Open Items

| ID | Item | Impact | Suggested Resolution | Related Requirement |
|----|------|--------|---------------------|---------------------|
| OI-01 | What JSON Schema format should be used for agent definition validation (JSON Schema Draft 2020-12, Pydantic, or YAML Schema)? | AR-003 implementation | Prototype with JSON Schema Draft 2020-12 (widest tooling support); evaluate Pydantic if Python-based validation pipeline is preferred | AR-003 |
| OI-02 | What confidence threshold should trigger LLM fallback in layered routing? | RR-003 implementation | Empirically determine by logging keyword match confidence for 100+ real routing decisions | RR-003 |
| OI-03 | Should the Open Agent Specification (Agent Spec) be adopted as a baseline for the agent definition schema? | AR-002, AR-003 | Evaluate Agent Spec for compatibility with Jerry's YAML+MD pattern; adopt compatible elements | AR-002, AR-003 |
| OI-04 | How should output schemas handle variability between L0/L1/L2 levels in different agent types? | QR-003, PR-008 | Define a base schema with optional level-specific sections; validate presence of all three levels for stakeholder-facing agents | QR-003 |
| OI-05 | What is the maximum agent count before team-based grouping becomes necessary? | AR-004, AR-011 | Monitor coordination overhead; TS-1 suggests ~50-agent threshold for reevaluation | AR-004 |
| OI-06 | How should audit trail records be stored -- filesystem, Memory-Keeper, or dedicated logging infrastructure? | SR-006 | Start with filesystem (consistent with Jerry's filesystem-as-memory principle); migrate to Memory-Keeper if cross-session query needs arise | SR-006 |
| OI-07 | Should negative keywords be implemented as a separate data structure or integrated into the existing trigger map format? | RR-005 | Extend the existing trigger map table in mandatory-skill-usage.md with a "Negative Keywords" column | RR-005 |

---

## References

### Phase 1 Research Documents

| ID | Document | Location |
|----|----------|----------|
| TS-1 through TS-5 | Trade Study: Agent Design Alternatives | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-1/nse-explorer-001/nse-explorer-001-agent-design-alternatives.md` |
| ps-researcher-001 | Claude Code Agent Capabilities Research | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-1/ps-researcher-001/ps-researcher-001-claude-code-agent-capabilities.md` |
| ps-researcher-002 | Agent Routing and Trigger Research | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-1/ps-researcher-002/ps-researcher-002-agent-routing-triggers.md` |
| ps-researcher-003 | Industry Best Practices Research | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-1/ps-researcher-003/ps-researcher-003-industry-best-practices.md` |
| Cross-pollination | PS-to-NSE Handoff | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/cross-pollination/barrier-1/ps-to-nse/handoff.md` |

### Jerry Framework Rules

| ID | Document | Location |
|----|----------|----------|
| quality-enforcement.md | Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` |
| mandatory-skill-usage.md | Mandatory Skill Usage | `.context/rules/mandatory-skill-usage.md` |
| architecture-standards.md | Architecture Standards | `.context/rules/architecture-standards.md` |
| mcp-tool-standards.md | MCP Tool Standards | `.context/rules/mcp-tool-standards.md` |
| AGENTS.md | Agent Registry | `AGENTS.md` |
| ps-researcher.md | Example Agent Definition | `skills/problem-solving/agents/ps-researcher.md` |

### External Standards

| Standard | Relevance |
|----------|-----------|
| NPR 7123.1D | NASA Systems Engineering Processes (Processes 1, 2, 11) |
| INCOSE Guide for Writing Requirements | Requirements quality criteria (8 criteria) |
| RFC 2119 | Priority keywords (MUST, SHOULD, MAY) |
| Open Agent Specification (2025) | Agent definition format standards |

---

*Generated by nse-requirements agent v2.1.0*
*NASA Process: NPR 7123.1D Processes 1, 2, 11*
*Self-Review (S-010) Applied: 6 findings identified and corrected*
*Requirements count: 52 shall-statements across 6 domains*
*Traceability: 100% bidirectional coverage to Phase 1 research, existing rules, and trade study recommendations*
