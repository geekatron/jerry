# Agent Development Standards

<!-- VERSION: 1.2.0 | DATE: 2026-02-22 | SOURCE: ADR-PROJ007-001, PROJ-007 Phase 3 Synthesis, V&V Plan, EN-003 | REVISION: EN-003 gap closures (ET-M-001 extended thinking, FC-M-001 fresh context review) -->

> Canonical standards for agent definition format, structural patterns, behavioral constraints, and handoff protocols within the Jerry Framework. All agent definitions MUST reference this file.

<!-- L2-REINJECT: rank=5, content="Agent definitions: YAML frontmatter MUST validate against JSON Schema (H-34). Required YAML fields: name, version, description, model, identity, capabilities, guardrails, output, constitution. Tool tiers T1-T5: always select lowest tier satisfying requirements. Cognitive modes: divergent, convergent, integrative, systematic, forensic. Constitutional triplet (P-003, P-020, P-022) REQUIRED in every agent (H-35)." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Agent definition constraints H-34, H-35 |
| [MEDIUM Standards](#medium-standards) | Overridable agent design standards with documented justification |
| [Agent Definition Schema](#agent-definition-schema) | Required and recommended YAML frontmatter fields |
| [Structural Patterns](#structural-patterns) | Identity, capabilities, guardrails, output, constitution sections (incl. FC-M-001) |
| [Tool Security Tiers](#tool-security-tiers) | T1-T5 tiered tool access with selection guidelines |
| [Cognitive Mode Taxonomy](#cognitive-mode-taxonomy) | Five modes with selection criteria and design implications |
| [Progressive Disclosure](#progressive-disclosure) | Three-tier content structure with context budget rules |
| [Guardrails Template](#guardrails-template) | Required guardrail sections per agent type |
| [Handoff Protocol](#handoff-protocol) | Structured handoff schema and context passing conventions |
| [Verification](#verification) | How compliance is verified per enforcement layer |
| [References](#references) | Source document traceability |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence | Source Requirements | Verification |
|----|------|-------------|---------------------|--------------|
| H-34 | Agent definition YAML frontmatter MUST validate against the canonical JSON Schema (`docs/schemas/agent-definition-v1.schema.json`). Required top-level fields: `name`, `version`, `description`, `model`, `identity`, `capabilities`, `guardrails`, `output`, `constitution`. Schema validation MUST execute before LLM-based quality scoring for C2+ deliverables. | Agent definition rejected at CI. Structural defects propagate to runtime. | AR-001 (YAML+MD format), AR-002 (required fields), AR-003 (schema validation), QR-003 (output schema) | L5 (CI): JSON Schema validation on PR. L3 (pre-tool): Schema check before agent invocation. |
| H-35 | Every agent MUST declare constitutional compliance with at minimum P-003 (no recursive subagents), P-020 (user authority), and P-022 (no deception) in `constitution.principles_applied`. Worker agents (invoked via Task) MUST NOT include `Task` in `capabilities.allowed_tools`. Every agent MUST declare at minimum 3 entries in `capabilities.forbidden_actions` referencing the constitutional triplet. | Constitutional constraint bypass. Unauthorized recursive delegation. | SR-001 (constitutional compliance), AR-004 (single-level nesting), AR-006 (tool restriction), AR-012 (forbidden actions) | L3 (pre-tool): Schema validates minItems=3. L5 (CI): Grep for P-003/P-020/P-022 presence. |

**H-34 Implementation Note:** The schema file (`docs/schemas/agent-definition-v1.schema.json`) will be created as part of the Phase 5 implementation. Until the schema file exists, L3 schema validation is deferred; L5 CI enforcement activates when the schema file is committed. The HARD rule is immediately enforceable for its structural requirements (required fields, YAML delimiter presence) via pattern-matching pre-schema. The inline schema in ADR-PROJ007-001 Section 2 serves as the authoritative specification until the extracted schema file is available.

**HARD Rule Budget:** H-34 and H-35 are consolidated into compound H-34 in `quality-enforcement.md` HARD Rule Index (H-35 retired as sub-item b). Current budget: 25/25 rules at ceiling.

---

## MEDIUM Standards

> Override requires documented justification.

### Agent Structure Standards

| ID | Standard | Guidance | Source Requirements |
|----|----------|----------|---------------------|
| AD-M-001 | Agent name SHOULD follow the `{skill-prefix}-{function}` kebab-case pattern matching the filename without `.md` extension. | Pattern: `^[a-z]+-[a-z]+(-[a-z]+)*$`. Skill prefix SHOULD match parent skill directory name. | AR-007 (naming convention) |
| AD-M-002 | Agent version SHOULD use semantic versioning (`MAJOR.MINOR.PATCH`). | Increment MAJOR for breaking behavioral changes, MINOR for capability additions, PATCH for fixes. Pattern: `^\d+\.\d+\.\d+$`. | AR-008 (versioning) |
| AD-M-003 | Agent description SHOULD include WHAT the agent does, WHEN to invoke it, and at least one trigger keyword. Maximum 1024 characters. No XML tags. | Aligns with H-28 (skill description standards). Description quality directly affects routing accuracy (AP-01 Keyword Tunnel prevention). | AR-009 (description quality), H-28 |
| AD-M-004 | Agents producing stakeholder-facing deliverables SHOULD declare all three output levels (`L0`, `L1`, `L2`) in `output.levels`. | L0: Executive summary. L1: Technical detail. L2: Strategic implications. Internal-only agents MAY omit L0. | PR-008 (output levels) |
| AD-M-005 | Agent `identity.expertise` SHOULD contain at minimum 2 specific domain competencies. | Generic expertise ("analysis", "writing") degrades routing signal quality. Prefer specific: "FMEA risk analysis", "hexagonal architecture patterns". | PR-003 (expertise domains) |
| AD-M-006 | Agents SHOULD declare `persona` (tone, communication_style, audience_level) for consistent output voice. | Enum values -- tone: professional, technical, consultative. communication_style: consultative, directive, analytical. audience_level: adaptive, expert, intermediate, beginner. | PR-005 (persona) |
| AD-M-007 | Agents SHOULD declare `session_context` with `on_receive` and `on_send` processing steps for structured handoff participation. | Defines how the agent processes inbound handoff data and constructs outbound handoffs. See [Handoff Protocol](#handoff-protocol). | HR-001 (structured format), HR-002 (required fields) |
| AD-M-008 | Agents SHOULD declare `validation.post_completion_checks` listing verifiable post-completion assertions. | Examples: `verify_file_created`, `verify_navigation_table`, `verify_citations_present`. Enables deterministic quality checking before LLM scoring. | QR-003 (output validation) |
| AD-M-009 | Agent model selection SHOULD be justified per cognitive demands. | `opus` for complex reasoning, research, architecture, synthesis. `sonnet` for balanced analysis, standard production tasks. `haiku` for fast repetitive tasks, formatting, validation. | PR-007 (model selection) |
| AD-M-010 | New agents SHOULD declare MCP tool usage in `capabilities.allowed_tools`. Research/documentation agents SHOULD use Context7; cross-session agents SHOULD use Memory-Keeper. | Aligns with MCP-M-002 from `mcp-tool-standards.md`. | AR-006 (tool restriction), MCP-M-002 |
| ET-M-001 | Agent definitions SHOULD declare `reasoning_effort` aligned with criticality level. Mapping: C1=default, C2=medium, C3=high, C4=max. Orchestrator agents SHOULD use `high` or `max`. Validation-only agents (e.g., ps-validator, wt-auditor) MAY use `default`. | Orthogonal to AD-M-009 (model selection): model determines *which* model reasons, reasoning_effort determines *how deeply* it reasons. Extended thinking allocation scales with decision criticality to balance thoroughness against token cost. | Anthropic best practices (extended thinking), quality-enforcement.md criticality levels |

### Context Budget Standards

> These operationalize progressive disclosure (PR-004) and mitigate context rot (R-T01, RPN 392). Override with documented justification.

| ID | Standard | Guidance | Rationale | Derivation |
|----|----------|----------|-----------|------------|
| CB-01 | Reserve >= 5% of context window for output generation. | Prevents truncated output when context fills during reasoning. | PR-004 Tier 3 loading discipline | Based on observed output truncation at > 95% context fill: when context usage exceeds 95%, output generation competes with retained context and produces truncated or degraded responses. The 5% reserve provides a minimum safe buffer for output tokens. Provisional -- calibrate against observed truncation rates across agent types. |
| CB-02 | Tool results SHOULD NOT exceed 50% of total context window. | Prefer targeted reads over bulk reads. Leave room for reasoning. | R-T01 context rot mitigation | Reasoning quality requires proportional context allocation: if tool results consume > 50%, the remaining context must accommodate the agent definition, user prompt, reasoning chain, and output generation. Empirical observation from Phase 1 analysis shows agents producing lower-quality synthesis when tool result content dominates the context window. The 50% limit ensures reasoning has at least parity with input data. Provisional -- calibrate per cognitive mode (divergent agents may need higher tool allocation). |
| CB-03 | Prefer file-path references over inline content in handoffs. | Avoids duplicating large content across handoff + tool result reads. | PR-004 Tier 1/Tier 2 boundary | Derives from the Tier 1/Tier 2 boundary in PR-004: file-path references keep handoff payloads at Tier 1 size (~500 tokens) while deferring full content to Tier 2 loading by the receiving agent, preventing N-fold duplication when the same content traverses multi-agent handoff chains. |
| CB-04 | Use `key_findings` (3-5 bullets) for quick orientation; defer detail to file reads. | 500-token orientation prevents 5,000-token cold read. | HR-002 handoff efficiency | The 500-token checkpoint summary vs. 5,000-token full state comparison implies a 10:1 compression ratio. Key findings bullets provide sufficient orientation signal at 10% of the cost of loading the full upstream artifact, enabling the receiving agent to decide whether a full read is necessary. |
| CB-05 | For files > 500 lines, use offset/limit parameters on Read. | Prevents single-file context exhaustion. | R-T01 mitigation | 500 lines approximates 5,000-10,000 tokens depending on line length. For a 200K-token context window, a single unconstrained read of a large file (1,000+ lines) can consume 5-10% of the context in one operation, compounding rapidly across multiple reads. The 500-line threshold provides a practical breakpoint where offset/limit usage becomes beneficial. Provisional -- adjust based on observed average tokens-per-line in the codebase. |

### Handoff Standards

| ID | Standard | Guidance | Source Requirements |
|----|----------|----------|---------------------|
| HD-M-001 | Handoff data SHOULD validate against the canonical handoff schema (`docs/schemas/handoff-v2.schema.json`). | Required fields: `from_agent`, `to_agent`, `task`, `success_criteria`, `artifacts`, `key_findings`, `blockers`, `confidence`, `criticality`. | HR-001 (structured format), HR-002 (required fields) |
| HD-M-002 | Artifact paths in handoffs SHOULD be validated for existence before delivery. | Prevents downstream agents from reading nonexistent files. `artifacts` array entries are expected to resolve to files that exist. | HR-003 (artifact path validation) |
| HD-M-003 | Quality gate SHOULD be passed (S-014 score >= 0.92 for C2+) before handoff delivery. | Sending agent's output meets quality standards before cross-boundary transfer. | HR-006 (quality gate at handoff) |
| HD-M-004 | Criticality level SHOULD NOT decrease through a handoff chain. Auto-escalation increases are expected to propagate to downstream agents. | Prevents downstream agents from under-reviewing high-criticality work. | CP-04 (criticality propagation) |
| HD-M-005 | Persistent blockers SHOULD be marked with `[PERSISTENT]` prefix in the `blockers` array and propagated through all subsequent handoffs. | Ensures systemic blockers are not silently dropped. | CP-05 (blocker escalation) |

---

## Agent Definition Schema

The canonical agent definition uses YAML frontmatter (validated by JSON Schema, H-34) followed by a structured Markdown body. The schema is stored at `docs/schemas/agent-definition-v1.schema.json` (JSON Schema Draft 2020-12).

### Required YAML Fields

| Field | Type | Constraint | Source |
|-------|------|------------|--------|
| `name` | string | Pattern: `^[a-z]+-[a-z]+(-[a-z]+)*$` | AR-001, AR-007 |
| `version` | string | Pattern: `^\d+\.\d+\.\d+$` | AR-008 |
| `description` | string | Max 1024 chars, no XML tags | AR-009, H-28 |
| `model` | enum | `opus`, `sonnet`, `haiku` | PR-007 |
| `identity.role` | string | Unique within parent skill | PR-001 |
| `identity.expertise` | array | Min 2 entries | PR-003 |
| `identity.cognitive_mode` | enum | `divergent`, `convergent`, `integrative`, `systematic`, `forensic` | PR-002 |
| `capabilities.allowed_tools` | array | From authorized tool enum; principle of least privilege | AR-006 |
| `capabilities.forbidden_actions` | array | Min 3 entries; MUST include P-003, P-020, P-022 references | AR-012 |
| `guardrails.input_validation` | array | Min 1 validation rule | SR-002 |
| `guardrails.output_filtering` | array | Min 3 entries (strings) | SR-003 |
| `guardrails.fallback_behavior` | enum | `warn_and_retry`, `escalate_to_user`, `persist_and_halt` | SR-009 |
| `output.required` | boolean | Whether agent produces file artifact | PR-008 |
| `output.location` | string | Required when `output.required` is `true` | AR-010 |
| `constitution.principles_applied` | array | Min 3 entries; MUST include P-003, P-020, P-022 | SR-001 |

### Recommended YAML Fields

| Field | Type | Purpose | Source |
|-------|------|---------|--------|
| `persona` | object | Tone, communication_style, audience_level | PR-005 |
| `output.levels` | array | `L0`, `L1`, `L2` disclosure levels | PR-008 |
| `validation.post_completion_checks` | array | Declarative verification assertions | QR-003 |
| `session_context` | object | Handoff on_receive/on_send protocol | HR-001, HR-002 |
| `reasoning_effort` | enum | Extended thinking allocation: `default`, `medium`, `high`, `max` (mapped to criticality per ET-M-001) | Anthropic best practices (extended thinking) |
| `enforcement` | object | Quality gate tier and escalation path | QR-001 |

### Markdown Body Sections

The agent definition Markdown body MUST be organized using XML-tagged sections. Each section maps to a hexagonal architecture layer.

| Section Tag | Purpose | Hexagonal Layer | Content |
|-------------|---------|-----------------|---------|
| `<identity>` | Who the agent is and how it reasons | Domain | Role title, expertise elaboration, cognitive mode behavior, distinctions from similar agents |
| `<purpose>` | Why the agent exists | Domain | Problem addressed, existence justification |
| `<input>` | What the agent receives | Adapter (inbound) | Session context fields, expected input format |
| `<capabilities>` | What tools the agent uses and how | Port | Tool usage patterns, constraints, tools NOT available |
| `<methodology>` | How the agent works | Domain | Step-by-step process, decision criteria, quality standards |
| `<output>` | What the agent produces | Adapter (outbound) | Artifact location, L0/L1/L2 structure, format requirements |
| `<guardrails>` | What the agent must not do | Domain | Constitutional compliance, input validation, output filtering, failure modes |

**Hexagonal dependency rule:** Domain-layer sections (`<identity>`, `<purpose>`, `<methodology>`, `<guardrails>`) MUST NOT reference specific tool names, output format details, model-specific instructions, or MCP key patterns. Use capability descriptions instead (e.g., "search the codebase" not "use Grep"). This applies the same directional discipline as H-07 (domain layer import restrictions) to agent definition content.

---

## Structural Patterns

### Pattern 1: Specialist Agent

Each agent addresses a single, well-defined concern. No agent combines research with scoring, or analysis with orchestration. This ensures:
- Clear routing signals from `identity.cognitive_mode` and `identity.expertise`
- Minimal tool requirements (lower security tier)
- Focused methodology sections

**Selection rule:** If an agent's `<methodology>` section contains two distinct workflows for different task types, it should be split into two specialist agents.

### Pattern 2: Orchestrator-Worker (P-003 Compliant)

Jerry enforces a strict single-level nesting constraint (H-01/P-003). The orchestrator-worker topology operates as:

```
MAIN CONTEXT (orchestrator)
    |
    +-- Worker A (via Task tool)
    +-- Worker B (via Task tool)
    +-- Worker C (via Task tool)
```

**Constraints:**
- Only one nesting level: orchestrator to worker. Workers MUST NOT spawn sub-workers.
- Worker agents MUST NOT include `Task` in `capabilities.allowed_tools` (H-35).
- Orchestrator agents MUST be T5 (Full) tier to access the Task tool.
- Error amplification is ~1.3x with structured handoffs (vs. 17x for uncoordinated topologies per Google DeepMind).

### Pattern 3: Creator-Critic-Revision (H-14 Integration)

For C2+ deliverables, the quality pattern operates as:

| Layer | Mechanism | Token Cost | Criticality |
|-------|-----------|------------|-------------|
| Layer 1: Schema Validation | JSON Schema check (deterministic) | 0 | All |
| Layer 2: Self-Review (S-010) | Agent reviews own output (H-15) | ~500-1,000 | All |
| Layer 3: Critic Review (S-014) | External critic with 6-dimension rubric (H-13, H-14) | ~2,000-4,000 | C2+ |
| Layer 4: Tournament | All 10 strategies executed (quality-enforcement.md) | ~100K+ | C4 |

**Iteration bounds:** Minimum 3 iterations per H-14. Maximum iterations by criticality: C2=5, C3=7, C4=10 (provisional values derived from Phase 3 Synthesis consensus analysis; calibrate against observed revision convergence rates). Plateau detection: delta < 0.01 for 3 consecutive iterations triggers circuit breaker (provisional; see `agent-routing-standards.md` for circuit breaker specification and calibration guidance).

### Pattern 4: Fresh Context Reviewer (FC-M-001)

For C3+ deliverables, review agents SHOULD be invoked via the Task tool to ensure context isolation and bias-free evaluation.

| ID | Standard | Guidance | Source |
|----|----------|----------|--------|
| FC-M-001 | For C3+ deliverables, review agents SHOULD be invoked via Task tool to obtain fresh context isolation. For C4 deliverables, a second independent reviewer SHOULD be invoked with a separate Task call, receiving only the artifact and evaluation criteria. | The Task tool inherently provides context isolation: each subagent starts with a clean context window, free from the creator's reasoning artifacts and confirmation bias. When Pattern 3 (Creator-Critic-Revision) uses the Task tool for critic invocation (H-14), the critic already benefits from this isolation. FC-M-001 formalizes this architectural property as an explicit quality pattern. | Anthropic best practices (writer/reviewer fresh context), H-14 (creator-critic-revision), P-003 (single-level nesting) |

**Why this works in Jerry:** The orchestrator-worker topology (Pattern 2, P-003 compliant) naturally creates fresh context boundaries. Each Task invocation gives the worker agent only what the orchestrator explicitly passes -- no accumulated reasoning, no sunk-cost bias, no anchoring to prior iterations. This is architecturally equivalent to Anthropic's recommendation to use separate context windows for writers and reviewers.

**C4 independent review:** At C4 criticality, the tournament review (Pattern 3, Layer 4) already executes all 10 adversarial strategies. FC-M-001 adds an explicit second reviewer invocation that receives only: (a) the artifact file path, (b) the quality gate rubric, and (c) the success criteria -- deliberately excluding prior critic scores and revision history to prevent anchoring.

---

## Tool Security Tiers

Five security tiers implement the principle of least privilege (AR-006). **Always select the lowest tier that satisfies the agent's requirements.**

| Tier | Name | Tools Included | Use Case | Example Agents |
|------|------|---------------|----------|----------------|
| **T1** | Read-Only | Read, Glob, Grep | Evaluation, auditing, scoring, validation | adv-executor, adv-scorer, wt-auditor |
| **T2** | Read-Write | T1 + Write, Edit, Bash | Analysis, document production, code generation | ps-analyst, nse-architecture, ps-critic |
| **T3** | External | T2 + WebSearch, WebFetch, Context7 | Research, exploration, external documentation | ps-researcher, nse-explorer |
| **T4** | Persistent | T2 + Memory-Keeper | Cross-session state management, orchestration | orch-planner, orch-tracker, nse-requirements |
| **T5** | Full | T3 + T4 + Task | Orchestration with delegation, full capability | Lead agent, skill orchestrators |

### Selection Guidelines

1. **Default to T1.** If an agent only reads and evaluates, T1 is sufficient.
2. **T2 when the agent produces artifacts.** Writing files (reports, analysis, code) requires T2 minimum.
3. **T3 when external information is needed.** T3 agents MUST include citation guardrails in `guardrails.output_filtering`.
4. **T4 when cross-session state is required.** T4 agents MUST follow the MCP key pattern: `jerry/{project}/{entity-type}/{entity-id}`.
5. **T5 requires explicit justification.** The Task tool enables delegation; every T5 assignment MUST document why delegation is necessary.

### Tier Constraints

| Constraint | Rationale | Source |
|------------|-----------|--------|
| Worker agents MUST NOT be T5 (no Task tool) | Enforces H-01 single-level nesting | AR-004, P-003 |
| T3+ agents MUST declare citation guardrails | External data requires source attribution | SR-003 |
| T4+ agents MUST follow MCP key namespace | Prevents key collision across sessions | MCP-002, mcp-tool-standards.md |
| Monitor per-agent tool count; alert at 15 tools | Industry-observed threshold where tool selection accuracy degrades (identified in Phase 1 research, ps-researcher-003 external patterns analysis; consistent with general LLM tool-use guidance recommending minimal tool sets for reliable selection) | AP-07 Tool Overload Creep prevention (see `agent-routing-standards.md` Anti-Pattern Catalog) |

---

## Cognitive Mode Taxonomy

Five cognitive modes classify how agents reason. The mode is declared in `identity.cognitive_mode` and shapes methodology, output structure, and iteration behavior.

| Mode | Description | Reasoning Pattern | Output Pattern | Iteration Behavior |
|------|-------------|-------------------|----------------|-------------------|
| **divergent** | Explores broadly, generates options, discovers patterns | Wide search, multiple hypotheses, creative association | Multiple alternatives, options lists, broad coverage | Expands search space on each iteration |
| **convergent** | Analyzes narrowly, selects options, produces conclusions | Focused evaluation, criteria-based selection, synthesis | Ranked recommendations, selected alternatives, focused analysis | Narrows from options to decision on each iteration |
| **integrative** | Combines inputs from multiple sources into unified output | Cross-source correlation, pattern merging, gap filling | Unified narratives, cross-reference tables, gap analysis | Builds coherence across inputs on each iteration |
| **systematic** | Applies step-by-step procedures, verifies compliance | Checklist execution, protocol adherence, completeness verification | Checklists, pass/fail tables, compliance matrices | Processes items sequentially without skipping |
| **forensic** | Traces causes backward from symptoms to root causes | Causal chain analysis, evidence correlation, hypothesis testing | Root cause chains, evidence correlation, 5 Whys | Narrows hypothesis space on each iteration |

### Mode Selection Guide

| Agent Task Type | Recommended Mode | Rationale |
|----------------|-----------------|-----------|
| Research, exploration, brainstorming | divergent | Needs breadth; premature convergence misses sources |
| Analysis, evaluation, scoring, review, architecture | convergent | Needs focused conclusion from alternatives |
| Synthesis, cross-pipeline merging, taxonomy building | integrative | Needs to unify multiple perspectives |
| Validation, auditing, compliance checking, formatting | systematic | Needs procedural completeness |
| Root cause analysis, debugging, failure investigation | forensic | Needs backward causal tracing |

### Mode-to-Design Implications

| Mode | Typical Tool Tier | Model Recommendation | Context Budget Priority |
|------|-------------------|---------------------|------------------------|
| divergent | T3+ (external access) | opus (complex reasoning) | Up to 50% tool result allocation per CB-02; may request exception with documented justification |
| convergent | T1 or T2 (focused input) | sonnet or opus | Balanced allocation |
| integrative | T2 (multiple file reads) | opus (complex synthesis) | Larger user message allocation for multi-source input |
| systematic | T1 (read-only preferred) | sonnet or haiku (procedural) | Smaller allocation; systematic work is compact |
| forensic | T2 or T3 (investigation) | opus (complex reasoning) | Larger reasoning allocation (~35%) |

**Consolidation note:** This taxonomy consolidates from 8 modes (nse-requirements-001 PR-002) to 5 modes. The 3 removed modes are subsumed: `strategic` maps to `convergent` (decision-making), `critical` maps to `convergent` (evaluation), `communicative` maps to `divergent` (conversational exploration). The `<methodology>` section captures mode-specific variations that the YAML enum cannot express.

---

## Progressive Disclosure

Agent definition content is organized into three tiers that load progressively, minimizing context window consumption and mitigating context rot (R-T01).

| Tier | Content | Max Size | Loading Mechanism |
|------|---------|----------|-------------------|
| **Tier 1: Metadata** | Agent name, description, trigger keywords, cognitive mode | ~500 tokens per skill | SKILL.md `description` field, loaded at session start |
| **Tier 2: Core** | Full YAML frontmatter + Markdown body (identity, purpose, methodology, guardrails, capabilities, output) | ~2,000-8,000 tokens per agent | Agent definition file, loaded when Task tool invokes the agent |
| **Tier 3: Supplementary** | Output templates, prior work artifacts, strategy templates, reference documents, cross-pollination data | Variable (budget-aware) | Read tool during agent execution; governed by CB-01 through CB-05 |

**Tier boundaries:** Tier 1 content MUST be sufficient for routing decisions. Tier 2 content MUST be sufficient for agent execution without Tier 3 loading for routine tasks. Tier 3 loading SHOULD be selective and driven by task-specific needs.

---

## Guardrails Template

Every agent definition MUST include guardrails addressing four areas (H-34 schema requirement).

### Required Guardrail Sections

```yaml
guardrails:
  # --- INPUT VALIDATION (SR-002) ---
  # At least one validation rule.
  input_validation:
    - field_format: "^{pattern}$"

  # --- OUTPUT FILTERING (SR-003) ---
  # Minimum 3 entries.
  output_filtering:
    - no_secrets_in_output
    - no_executable_code_without_confirmation
    - all_claims_must_have_citations

  # --- FALLBACK BEHAVIOR (SR-009) ---
  fallback_behavior: "warn_and_retry"

capabilities:
  # --- FORBIDDEN ACTIONS (AR-012) ---
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Misrepresent capabilities or confidence (P-022)"
```

> **Minimum set notice:** The entries above represent the MINIMUM required set per H-34 and H-35. Agent definitions SHOULD add domain-specific entries beyond these minimums. For example, a T3 research agent should add citation guardrails to `output_filtering`; an orchestration agent should add delegation boundary guardrails to `forbidden_actions`. See [Guardrail Selection by Agent Type](#guardrail-selection-by-agent-type) for type-specific guidance on extending beyond minimums.

### Guardrail Selection by Agent Type

| Agent Type | Additional Input Validation | Additional Output Filtering | Recommended Fallback |
|-----------|---------------------------|---------------------------|---------------------|
| Research (divergent, T3) | URL format validation, source tiering | Source authority tier required, stale data warnings | warn_and_retry |
| Analysis (convergent, T2) | Input schema validation, artifact path existence | Confidence bounds required, methodology citation | escalate_to_user |
| Validation (systematic, T1) | Criteria format validation | Binary pass/fail with evidence | persist_and_halt |
| Orchestration (T4-T5) | Phase state validation, predecessor completion | Progress percentage, blocker enumeration | escalate_to_user |
| Scoring (convergent, T1) | Rubric schema validation, score range validation | Anti-leniency statement, dimension-level breakdown | warn_and_retry |

---

## Handoff Protocol

Handoff protocol defines how agents exchange context at boundaries. Structured handoffs mitigate error amplification (R-T02, RPN 336) by replacing free-text summaries with schema-validated data contracts.

### Handoff Schema (v2)

The canonical handoff schema is stored at `docs/schemas/handoff-v2.schema.json` (JSON Schema Draft 2020-12).

**Required fields:**

| Field | Type | Constraint | Purpose |
|-------|------|------------|---------|
| `from_agent` | string | Non-empty, must match a registered agent | Identity of sending agent |
| `to_agent` | string | Non-empty, must match a registered agent | Identity of receiving agent |
| `task` | string | Non-empty | Description of the delegated work |
| `success_criteria` | array | Min 1 entry | Verifiable criteria for downstream agent |
| `artifacts` | array | File paths, validated for existence | Prior output file paths |
| `key_findings` | array | 3-5 entries per CB-04 | Orientation bullets from upstream |
| `blockers` | array | May be empty; persistent items prefixed `[PERSISTENT]` | Known impediments |
| `confidence` | number | 0.0 to 1.0 | Sending agent's self-assessed confidence. Calibration guidance: 0.0-0.3 = low confidence (significant gaps or unknowns); 0.4-0.6 = moderate (partial coverage with known limitations); 0.7-0.8 = high (comprehensive coverage, minor gaps); 0.9-1.0 = very high (complete, verified, no known gaps). Agents SHOULD calibrate against this scale rather than defaulting to high values. |
| `criticality` | string | Enum: C1, C2, C3, C4 | Work criticality level |

**Optional fields:** `constraints`, `routing_metadata`, `quality_context` (prior_score, critic_findings), `task_id`.

### Context Passing Conventions

| ID | Convention | Tier | Rationale |
|----|-----------|------|-----------|
| CP-01 | File paths only in handoffs, NEVER inline content | MEDIUM | Prevents context duplication; receiving agent loads content via Read |
| CP-02 | 3-5 key findings bullets in every handoff | MEDIUM | Enables quick orientation without full-document reads |
| CP-03 | Confidence score (0.0-1.0) mandatory in every handoff | MEDIUM | Enables downstream quality calibration |
| CP-04 | Criticality level MUST NOT decrease through handoff chains; auto-escalation increases propagate | MEDIUM | Prevents under-review of escalated work |
| CP-05 | Persistent blockers marked with `[PERSISTENT]` prefix | MEDIUM | Ensures systemic blockers are not silently dropped |

### Send-Side Validation

Before delivering a handoff, the sending agent SHOULD verify:

| Check | Description |
|-------|-------------|
| SV-01 | All required fields present and non-empty |
| SV-02 | `from_agent` matches the sending agent's own `name` |
| SV-03 | `key_findings` contains 3-5 entries |
| SV-04 | All `artifacts` paths resolve to existing files |
| SV-05 | `confidence` is between 0.0 and 1.0 |
| SV-06 | `criticality` matches or exceeds the orchestration-assigned level |
| SV-07 | Quality gate passed (S-014 score >= 0.92) for C2+ before delivery |

### Receive-Side Validation

Upon receiving a handoff, the receiving agent SHOULD verify:

| Check | Description |
|-------|-------------|
| RV-01 | All required fields present in received handoff |
| RV-02 | All `artifacts` paths resolve to readable files |
| RV-03 | `routing_metadata.routing_depth` (if present) is below circuit breaker threshold (max 3 hops) |
| RV-04 | `criticality` is consistent with expected level for this work item |

---

## Verification

Each standard maps to an enforcement layer for compliance checking.

| Enforcement Layer | Standards Verified | Mechanism | Context Rot Immunity |
|-------------------|-------------------|-----------|---------------------|
| L1 (Session start) | Progressive disclosure Tier 1 loading | Rules auto-loaded via `.claude/rules/` | Vulnerable |
| L2 (Every prompt) | H-34, H-35 re-injection via L2-REINJECT comments | HTML comment re-injection | Immune |
| L3 (Pre-tool) | Schema validation before agent invocation | JSON Schema validation (deterministic) | Immune |
| L4 (Post-tool) | CB-01 through CB-05 context budget monitoring | Advisory -- see note below | Mixed |
| L5 (CI/commit) | Full schema validation on all `skills/*/agents/*.md` files | CI pipeline JSON Schema check | Immune |

**L4 Context Budget Note:** CB-01 through CB-05 are currently advisory standards. Operational monitoring of context budget usage (e.g., measuring tool result token consumption against CB-02's 50% threshold) requires future tooling that does not yet exist. Until such tooling is available, agent authors self-assess context budget compliance during development, and reviewers verify compliance qualitatively during the creator-critic-revision cycle (H-14). When L4 monitoring tooling becomes available, CB enforcement will transition from advisory to instrumented.

### Pass/Fail Criteria

| Standard | PASS | FAIL |
|----------|------|------|
| H-34 (Schema validation) | 100% of agent files validate against JSON Schema. Zero validation errors. | Any file missing YAML delimiters, required fields, or failing schema constraints. |
| H-35 (Constitutional compliance) | All agents include P-003, P-020, P-022 in `constitution.principles_applied`. No worker agent has `Task` in `allowed_tools`. All agents have >= 3 `forbidden_actions`. | Any agent missing constitutional triplet. Any worker with Task tool access. Any agent with < 3 forbidden actions. |
| AD-M-001 through AD-M-010 | Agent follows the standard. | Agent deviates without documented justification. |
| CB-01 through CB-05 | Context budget guidelines followed during agent execution. | Context budget exceeded without justification. |
| HD-M-001 through HD-M-005 | Handoff follows protocol. | Handoff validation fails without documented exception. |

---

## References

| Source | Content | Location |
|--------|---------|----------|
| ADR-PROJ007-001 | Agent definition format, JSON Schema, tool tiers, cognitive modes, progressive disclosure, guardrails template | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-3-synthesis/ps-architect-001/` |
| Phase 3 Synthesis | Unified pattern taxonomy (66 patterns, 8 families), gap closure roadmap, maturity assessment | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-3-synthesis/ps-synthesizer-001/` |
| V&V Plan | Verification methods, pass/fail criteria, gap closure tests, FMEA reduction targets | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-3-synthesis/nse-verification-001/` |
| Integration Patterns | Handoff Protocol v2, quality gate integration, context passing conventions | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-3-synthesis/nse-integration-001/` |
| Barrier 3 NSE-to-PS Handoff | V&V criteria for rule files, per-agent guidance | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/cross-pollination/barrier-3/nse-to-ps/handoff.md` |
| quality-enforcement.md | Quality gate SSOT (H-13, H-14, criticality levels, enforcement architecture) | `.context/rules/quality-enforcement.md` |
| mandatory-skill-usage.md | H-22 proactive skill invocation, trigger map | `.context/rules/mandatory-skill-usage.md` |
| mcp-tool-standards.md | MCP-001, MCP-002, tool governance | `.context/rules/mcp-tool-standards.md` |
| skill-standards.md | H-25 through H-30, skill structure standards | `.context/rules/skill-standards.md` |
| Agent Routing Standards | Circuit breaker specification, keyword-first routing, anti-pattern catalog | `.context/rules/agent-routing-standards.md` |

---

<!-- VERSION: 1.2.0 | DATE: 2026-02-22 | SOURCE: ADR-PROJ007-001, PROJ-007 Phase 3 Synthesis, EN-003 | REVISION: EN-003 gap closures (ET-M-001, FC-M-001) -->
*Standards Version: 1.2.0*
*SSOT: `.context/rules/quality-enforcement.md` (H-34 compound registered, H-35 retired as sub-item)*
*Source: PROJ-007 Agent Patterns -- ADR-PROJ007-001, Phase 3 Synthesis, V&V Plan, Integration Patterns*
*Created: 2026-02-21*
*Agent: ps-architect-003*
