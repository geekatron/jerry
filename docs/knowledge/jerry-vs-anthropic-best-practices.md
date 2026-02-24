# Jerry Framework vs. Anthropic Claude Code Best Practices

<!-- VERSION: 1.1.0 | DATE: 2026-02-22 | SOURCE: EN-003 (PROJ-007) | CRITICALITY: C2 -->

> Comprehensive comparison of Jerry Framework patterns against Anthropic's official Claude Code best practices. Demonstrates alignment, identifies innovations, and documents gap closures.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Alignment score, key findings, positioning |
| [Methodology](#methodology) | Sources, comparison framework, scoring approach |
| [Alignment Areas](#alignment-areas) | 9 areas of direct alignment with evidence |
| [Jerry Innovations Beyond Anthropic](#jerry-innovations-beyond-anthropic) | 14 innovations not covered in Anthropic docs |
| [Gaps Identified and Addressed](#gaps-identified-and-addressed) | 3 gaps closed via EN-003 |
| [Quantitative Comparison Matrix](#quantitative-comparison-matrix) | Feature-by-feature table |
| [Lessons for the Industry](#lessons-for-the-industry) | 7 actionable insights |
| [References](#references) | Anthropic docs URLs + Jerry file paths |

---

## Executive Summary

The Jerry Framework achieves **complete alignment** with all 7 Anthropic Claude Code best practice categories while extending significantly beyond them with 14 documented innovations. Three minor gaps were identified and closed via EN-003 as MEDIUM standards.

**Key findings:**

- **9 areas of direct alignment** -- Jerry independently developed patterns that match or exceed every Anthropic recommendation
- **14 innovations beyond Anthropic** -- Jerry codifies practices Anthropic does not document, including quantitative quality gates, adversarial review strategies, FMEA-based risk analysis, and constitutional governance
- **3 gaps closed** -- Plan mode workflow (PM-M-001), extended thinking allocation (ET-M-001), and fresh context review pattern (FC-M-001) formalized as MEDIUM standards
- **Zero HARD rule impact** -- All gap closures are SHOULD-level standards; HARD rule ceiling remains 25/25
- **Maturity difference** -- Anthropic provides advisory guidance ("do this"); Jerry provides enforceable governance ("this is REQUIRED at C2+, verified at L2/L5, with these consequences for violation")

**Positioning:** Jerry Framework is an **industry exemplar** for Claude Code agent governance. It implements everything Anthropic recommends, adds rigorous enforcement mechanisms Anthropic leaves to user discretion, and provides a research-backed pattern taxonomy spanning 66 patterns across 8 families.

---

## Methodology

### Sources

| Source | Type | Date Accessed |
|--------|------|---------------|
| [Anthropic Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview) | Official documentation | 2026-02-22 |
| [Anthropic Claude Code Best Practices](https://docs.anthropic.com/en/docs/claude-code/best-practices) | Official documentation | 2026-02-22 |
| Jerry Framework `.context/rules/` | Internal rule files (10 files) | 2026-02-22 |
| PROJ-007 Agent Patterns research corpus | 33 artifacts across 5 phases | 2026-02-21 |
| Jerry Framework `docs/governance/JERRY_CONSTITUTION.md` | Constitutional governance | 2026-02-22 |

### Comparison Framework

Each Anthropic recommendation is mapped to Jerry's implementation using three dimensions:

| Dimension | Description |
|-----------|-------------|
| **Coverage** | Does Jerry address this practice? (yes/no/partial) |
| **Enforcement** | How is compliance ensured? (advisory/MEDIUM/HARD/deterministic) |
| **Extension** | Does Jerry go beyond the Anthropic recommendation? (none/minor/significant) |

### Scoring Key

| Rating | Meaning |
|--------|---------|
| ALIGNED | Jerry implements the practice as recommended |
| EXCEEDS | Jerry implements the practice and extends significantly beyond it |
| GAP (CLOSED) | Jerry did not implement the practice; now addressed by EN-003 |

---

## Alignment Areas

### Area 1: Context Window as Primary Resource

**Anthropic says:** "The context window is the most important resource to manage." Performance degrades as context fills. Use `/clear` between tasks, subagents for investigation, compaction for context recovery.

**Jerry implements:**

| Jerry Feature | Evidence | Enforcement |
|---------------|----------|-------------|
| Context rot as core design problem | CLAUDE.md: "Core Problem: Context Rot" | L1 (session start) |
| AE-006 graduated escalation | 5-tier response: NOMINAL → WARNING → CRITICAL → EMERGENCY → COMPACTION | L2 (every prompt, rank 9) |
| CB-01 through CB-05 context budget standards | Reserve 5% for output, 50% tool result cap, file-path references, 500-line read limits | L4 (advisory) |
| Progressive disclosure (3-tier) | Tier 1: metadata (~500 tok), Tier 2: core (~2K-8K tok), Tier 3: supplementary (budget-aware) | L1 + schema |

**Rating: EXCEEDS.** Anthropic describes the problem and recommends manual management (`/clear`, `/compact`). Jerry operationalizes it with graduated escalation rules, token budgets per agent, and progressive disclosure tiers that automatically minimize context consumption.

### Area 2: Subagent Architecture (P-003)

**Anthropic says:** Custom subagents in `.claude/agents/` with own context and tool restrictions. Agent teams coordinate multiple sessions. "Since context is your fundamental constraint, subagents are one of the most powerful tools available."

**Jerry implements:**

| Jerry Feature | Evidence | Enforcement |
|---------------|----------|-------------|
| P-003: No recursive subagents | H-01, constitutional HARD rule | L2 (every prompt, rank 1) |
| Orchestrator-worker topology | Pattern 2 in `agent-development-standards.md` | H-35 (Task tool restriction) |
| Single-level nesting | Workers MUST NOT include Task in allowed_tools | L3 (pre-tool schema) + L5 (CI) |
| Error amplification analysis | ~1.3x with structured handoffs vs. 17x uncoordinated (Google DeepMind) | Research-backed derivation |

**Rating: EXCEEDS.** Anthropic describes subagents as a feature. Jerry enforces a specific topology (orchestrator-worker), prohibits recursive delegation constitutionally, and provides research-backed error amplification analysis justifying the constraint.

### Area 3: CLAUDE.md as Persistent Instructions

**Anthropic says:** CLAUDE.md in project root loaded every session. Keep it short. Include commands Claude can't guess, non-default code style, testing instructions, architectural decisions. Treat it like code. Prune regularly.

**Jerry implements:**

| Jerry Feature | Evidence | Enforcement |
|---------------|----------|-------------|
| Hierarchical CLAUDE.md | Root CLAUDE.md with navigation table linking to rule files | L1 (session start) |
| Rule distribution via `.claude/rules/` hardlinks | Auto-loaded rules separate from CLAUDE.md bloat | L1 (deterministic) |
| L2 re-injection engine | Critical rules re-injected every prompt via HTML comments | L2 (immune to context rot) |
| Skill-based on-demand loading | Domain knowledge loaded only when triggered (H-22) | L1 + L2 (rank 6) |

**Rating: EXCEEDS.** Anthropic recommends a single CLAUDE.md file with manual pruning. Jerry implements a multi-layer architecture: CLAUDE.md for navigation, `.context/rules/` for detailed standards (auto-loaded via hardlinks), L2 re-injection for context-rot-immune enforcement, and skills for on-demand domain loading.

### Area 4: Hooks for Deterministic Enforcement

**Anthropic says:** "Hooks are deterministic and guarantee the action happens, unlike CLAUDE.md instructions which are advisory." Run scripts at specific workflow points. Claude can write hooks for you.

**Jerry implements:**

| Jerry Feature | Evidence | Enforcement |
|---------------|----------|-------------|
| SessionStart hook | Validates active project (H-04), loads project context | L3 (deterministic) |
| L3 pre-tool gating | AST-based validation before tool execution (H-33) | L3 (deterministic, context-rot immune) |
| L5 CI gates | HARD rule ceiling enforcement, schema validation on PR | L5 (deterministic, context-rot immune) |
| 5-layer enforcement architecture | L1 (rules) → L2 (re-injection) → L3 (pre-tool) → L4 (post-tool) → L5 (CI) | Architecture-level design |

**Rating: EXCEEDS.** Anthropic describes hooks as a feature for ad-hoc automation. Jerry architecturally integrates deterministic gating across 5 enforcement layers, where hooks are one component of a comprehensive enforcement system that includes per-prompt re-injection, AST-based pre-tool validation, and CI pipeline gates.

### Area 5: Tool Selection and Scoping

**Anthropic says:** CLI tools are the "most context-efficient" way to interact with external services. Use `--allowedTools` to scope permissions. Connect MCP servers for external integrations.

**Jerry implements:**

| Jerry Feature | Evidence | Enforcement |
|---------------|----------|-------------|
| T1-T5 tool security tiers | Principle of least privilege; 5 tiers from Read-Only to Full | H-34 (agent schema) |
| Per-agent allowed_tools | YAML frontmatter declares exact tool set | L3 (schema validation) |
| Tool count monitoring | Alert at 15 tools per agent (AP-07 prevention) | Advisory (RT-M-011..015) |
| MCP-001/MCP-002 governance | Context7 REQUIRED for external libs; Memory-Keeper REQUIRED at phase boundaries | HARD (file-scoped) |
| UV-only Python | H-05: NEVER use python/pip directly | L2 (rank 3) |

**Rating: EXCEEDS.** Anthropic recommends scoping tool permissions. Jerry implements a formal 5-tier security model with schema-enforced per-agent tool declarations, proactive tool count monitoring, and MCP-specific governance rules.

### Area 6: Verification and Quality Assurance

**Anthropic says:** "This is the single highest-leverage thing you can do." Provide tests, screenshots, expected outputs. Without verification, "you become the only feedback loop."

**Jerry implements:**

| Jerry Feature | Evidence | Enforcement |
|---------------|----------|-------------|
| H-13 quality gate (>= 0.92) | Weighted composite score for C2+ deliverables | HARD, L2 (rank 2) |
| S-014 LLM-as-Judge | 6-dimension rubric (completeness, consistency, rigor, evidence, actionability, traceability) | Strategy template |
| H-14 creator-critic-revision | Minimum 3 iterations for C2+ | HARD, L2 (rank 2) |
| H-20 BDD test-first | Red-Green-Refactor, 90% line coverage | HARD, L2 (rank 5) |
| C4 tournament review | All 10 adversarial strategies | quality-enforcement.md |

**Rating: EXCEEDS.** Anthropic recommends providing verification criteria. Jerry implements a quantitative quality gate with dimensional scoring, mandatory multi-iteration review cycles, and a 10-strategy adversarial tournament for critical deliverables.

### Area 7: Ambiguity Resolution

**Anthropic says:** Provide specific context in prompts. Scope tasks, point to sources, reference existing patterns. "The more precise your instructions, the fewer corrections you'll need."

**Jerry implements:**

| Jerry Feature | Evidence | Enforcement |
|---------------|----------|-------------|
| H-31: Clarify when ambiguous | MUST ask when multiple interpretations exist, scope is unclear, or action is destructive | HARD, L2 (rank 2) |
| H-31 terminal in routing | When all routing layers fail, ask the user | `agent-routing-standards.md` |
| AskUserQuestion integration | Structured question format with options | Tool-level |

**Rating: ALIGNED.** Both Jerry and Anthropic recognize that ambiguity is the most expensive failure mode. Jerry codifies this as a HARD rule with explicit trigger conditions (multiple interpretations, unclear scope, destructive action) and makes it the terminal fallback in the routing architecture.

### Area 8: Skills and On-Demand Knowledge

**Anthropic says:** Skills in `.claude/skills/` with SKILL.md. Applied automatically when relevant, or invoked with `/skill-name`. "Use Skills instead of CLAUDE.md" for domain knowledge only relevant sometimes.

**Jerry implements:**

| Jerry Feature | Evidence | Enforcement |
|---------------|----------|-------------|
| H-22: Proactive skill invocation | MUST invoke skills when triggers apply; DO NOT WAIT for user | HARD, L2 (rank 6) |
| 5-column trigger map | Keywords, negative keywords, priority, compound triggers, skill | `mandatory-skill-usage.md` |
| 10 registered skills | /problem-solving, /nasa-se, /orchestration, /adversary, /transcript, /saucer-boy, etc. | CLAUDE.md quick reference |
| H-25/H-26: Skill standards | SKILL.md case, kebab-case folders, WHAT+WHEN+triggers description | HARD |

**Rating: EXCEEDS.** Anthropic describes skills as an opt-in feature. Jerry enforces proactive invocation via H-22, implements a sophisticated trigger map with negative keywords and priority ordering for disambiguation, and mandates structural standards for skill definitions.

### Area 9: Session Management

**Anthropic says:** Use `Esc` to stop, `/rewind` to restore, `/clear` between tasks. "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered." Resume sessions with `--continue`/`--resume`.

**Jerry implements:**

| Jerry Feature | Evidence | Enforcement |
|---------------|----------|-------------|
| AE-006 graduated escalation | WARNING at 70%, CRITICAL at 80%, EMERGENCY at 88%, COMPACTION event | L2 (rank 9) |
| Checkpoint architecture | `.jerry/checkpoints/` for orchestration state persistence | Orchestration skill |
| Session start validation | H-04 active project check, context loading | L3 (SessionStart hook) |
| Cross-session state | Memory-Keeper MCP for phase boundary persistence | MCP-002 |

**Rating: EXCEEDS.** Anthropic provides manual session management tools. Jerry automates context health monitoring with graduated escalation thresholds and provides structured checkpoint persistence for cross-session state recovery.

---

## Jerry Innovations Beyond Anthropic

The following 14 practices are implemented in Jerry but have no corresponding recommendation in Anthropic's official best practices documentation.

### Innovation 1: Constitutional Governance

Jerry implements a formal constitution (`docs/governance/JERRY_CONSTITUTION.md`) with three inviolable principles (P-003, P-020, P-022) that propagate through every agent definition, rule file, and quality gate. Anthropic provides no governance framework.

**Evidence:** H-01 (P-003), H-02 (P-020), H-03 (P-022), H-35 (constitutional triplet in every agent), S-007 (Constitutional AI Critique strategy).

### Innovation 2: 5-Layer Enforcement Architecture

Jerry distributes enforcement across 5 layers (L1-L5) with varying context-rot immunity, ensuring critical rules survive even when the context window is saturated. Anthropic describes hooks (one layer) and CLAUDE.md (one layer) without a systematic enforcement model.

**Evidence:** `quality-enforcement.md` Enforcement Architecture section. L1 (session start, ~12,500 tokens), L2 (per-prompt, ~850 tokens), L3 (pre-tool, 0 tokens), L4 (post-tool, 0-1,350 tokens), L5 (CI, 0 tokens).

### Innovation 3: L2 Per-Prompt Re-Injection

Jerry uses HTML comment markers (`L2-REINJECT`) to re-inject critical rules on every prompt, making them immune to context rot. This is architecturally unique -- no published framework documents this technique.

**Evidence:** 16 L2-REINJECT markers across 10 rule files, consuming 559/850 token budget (65.8%).

### Innovation 4: Quantitative Quality Gate (S-014)

Jerry implements a 6-dimension weighted scoring rubric with a 0.92 threshold for C2+ deliverables. Anthropic recommends "provide verification criteria" without specifying quantitative standards.

**Evidence:** H-13 (threshold), H-17 (scoring required), S-014 strategy template, operational score bands (PASS >= 0.92, REVISE 0.85-0.91, REJECTED < 0.85).

### Innovation 5: 4-Level Decision Criticality

Jerry classifies every decision into C1 (Routine) through C4 (Critical) with proportional review depth. Anthropic does not distinguish between trivial and critical changes.

**Evidence:** `quality-enforcement.md` Criticality Levels. C1: S-010 only. C2: S-007+S-002+S-014. C3: 6+ strategies. C4: all 10 strategies (tournament).

### Innovation 6: 10-Strategy Adversarial Review Catalog

Jerry maintains 10 ranked adversarial strategies (S-001 through S-015, 10 selected, 5 excluded with documented rationale) for systematic quality assurance. Anthropic has no adversarial review concept.

**Evidence:** `quality-enforcement.md` Strategy Catalog. Strategies scored by composite score (3.35-4.40). Implemented via `/adversary` skill with 3 specialized agents (adv-selector, adv-executor, adv-scorer).

### Innovation 7: FMEA-Based Risk Analysis

Jerry applies Failure Mode and Effects Analysis (S-012) to agent architecture, with Risk Priority Numbers (RPNs) for systematic risk identification. Anthropic provides no risk analysis framework.

**Evidence:** PROJ-007 V&V Plan. CF-01 Context Rot (RPN 392), HF-01 Handoff Info Loss (RPN 336), QF-02 False Positive Scoring (RPN 280), RF-04 Routing Loops (RPN 252). FMEA monitoring thresholds in RT-M-011 through RT-M-015.

### Innovation 8: HARD Rule Ceiling with Principled Derivation

Jerry caps HARD rules at 25 with a derivation from three independent constraint families (cognitive load, enforcement coverage, governance burden) and a controlled exception mechanism. Anthropic has no concept of rule budgets.

**Evidence:** `quality-enforcement.md` HARD Rule Ceiling Derivation. Current count: 25/25. Absolute maximum: 28 (L5 enforced). Exception process: C4-reviewed ADR, 3-month duration, maximum N=3 temporary slots.

### Innovation 9: Agent Definition Schema with JSON Validation

Jerry defines a canonical YAML+Markdown agent format validated against JSON Schema, with required fields, cognitive mode taxonomy, and tool security tiers. Anthropic's subagent definitions are free-form YAML with minimal structure.

**Evidence:** H-34 (schema validation), `docs/schemas/agent-definition-v1.schema.json`, `agent-development-standards.md` Required YAML Fields table (15 required fields).

### Innovation 10: Structured Handoff Protocol

Jerry defines a schema-validated handoff protocol (v2) with required fields (from_agent, to_agent, task, success_criteria, artifacts, key_findings, blockers, confidence, criticality) for inter-agent communication. Anthropic provides no handoff specification.

**Evidence:** `agent-development-standards.md` Handoff Protocol section. HD-M-001 through HD-M-005. Send-side (SV-01 through SV-07) and receive-side (RV-01 through RV-04) validation checklists.

### Innovation 11: Layered Routing with Circuit Breaker

Jerry implements a 4-layer routing architecture (L0: explicit, L1: keyword, L2: decision tree, L3: LLM-as-router) with a 3-hop circuit breaker and cycle detection. Anthropic relies on keyword matching and manual skill invocation.

**Evidence:** H-36 (circuit breaker), `agent-routing-standards.md` Layered Routing Architecture. Current: Phase 1 (enhanced keyword). Scaling roadmap through Phase 3 (20+ skills).

### Innovation 12: Anti-Pattern Catalog

Jerry documents 8 routing anti-patterns (AP-01 through AP-08) with detection heuristics and prevention rules. Anthropic documents 5 common failure patterns but does not systematize detection or prevention.

**Evidence:** `agent-routing-standards.md` Anti-Pattern Catalog. AP-01 Keyword Tunnel, AP-02 Bag of Triggers, AP-03 Telephone Game, AP-04 Routing Loop, AP-05 Over-Routing, AP-06 Under-Routing, AP-07 Tool Overload Creep, AP-08 Context-Blind Routing.

### Innovation 13: Cognitive Mode Taxonomy

Jerry classifies agent reasoning into 5 modes (divergent, convergent, integrative, systematic, forensic) with design implications for tool tier, model selection, and context budget. Anthropic does not classify agent reasoning patterns.

**Evidence:** `agent-development-standards.md` Cognitive Mode Taxonomy. Mode Selection Guide maps task types to modes. Mode-to-Design Implications maps modes to tool tiers and model recommendations.

### Innovation 14: Auto-Escalation Rules

Jerry automatically escalates review criticality based on what is being changed (AE-001 through AE-006). Touching the constitution triggers C4. Touching rules triggers C3 minimum. Anthropic has no concept of change-based review escalation.

**Evidence:** `quality-enforcement.md` Auto-Escalation Rules. AE-001: constitution → C4. AE-002: rules → C3. AE-003: new ADR → C3. AE-004: baselined ADR → C4. AE-005: security code → C3. AE-006: context fill graduated response.

---

## Gaps Identified and Addressed

Three areas where Anthropic recommends practices Jerry had not previously codified. All three were addressed by EN-003 as MEDIUM standards (SHOULD, not MUST), preserving the HARD rule ceiling at 25/25 and the L2 token budget at 559/850.

### Gap 1: Plan Mode Workflow

**Anthropic recommends:** "Separate research and planning from implementation." Four-phase workflow: Explore → Plan → Implement → Commit. Plan mode for read-only exploration. Skip planning when scope is clear and fix is small.

**Jerry gap:** Jerry had `/orchestration` for multi-agent workflows but did not codify plan mode as a workflow pattern for single-agent work. The "Workflow Phases" section in `project-workflow.md` described Before/During/After phases without an explicit explore-plan-approve sequence.

**EN-003 closure:** PM-M-001 added to `project-workflow.md`. SHOULD follow explore-plan-approve-implement-verify for C2+ work. Decision guide maps conditions to plan mode recommendations. Aligns with H-31 (ambiguity resolution) and complements `/orchestration`.

**Standard:** PM-M-001 in `.context/rules/project-workflow.md`

### Gap 2: Extended Thinking Allocation

**Anthropic recommends:** Extended thinking (budget tokens) can be allocated to give the model more reasoning space for complex tasks. Different tasks benefit from different thinking depths.

**Jerry gap:** Jerry had AD-M-009 (model selection mapped to cognitive demands) but did not address reasoning effort allocation. Model selection (which model) and thinking effort (how deeply it reasons) are orthogonal concerns.

**EN-003 closure:** ET-M-001 added to `agent-development-standards.md`. Agent definitions SHOULD declare `reasoning_effort` aligned with criticality: C1=default, C2=medium, C3=high, C4=max. Orchestrator agents SHOULD use high or max. Validation-only agents MAY use default.

**Standard:** ET-M-001 in `.context/rules/agent-development-standards.md`

### Gap 3: Fresh Context Review

**Anthropic recommends:** Writer/Reviewer pattern: "one session writes implementation, fresh session reviews (avoiding self-bias)." Subagents explore in separate context windows and report back summaries.

**Jerry gap:** Jerry's orchestrator-worker topology (Pattern 2) and creator-critic-revision cycle (Pattern 3, H-14) inherently provide context isolation when critics are invoked via Task tool. However, this architectural property was not explicitly formalized as a quality pattern.

**EN-003 closure:** FC-M-001 added to `agent-development-standards.md` as Pattern 4: Fresh Context Reviewer. For C3+ deliverables, review agents SHOULD be invoked via Task tool. For C4, a second independent reviewer SHOULD receive only artifact + criteria (no prior scores or revision history). Documents that Jerry already has this capability -- the closure formalizes what is architecturally true.

**Standard:** FC-M-001 in `.context/rules/agent-development-standards.md`

---

## Quantitative Comparison Matrix

| Practice Area | Anthropic | Jerry | Coverage | Enforcement | Extension |
|---------------|-----------|-------|----------|-------------|-----------|
| Context window management | Advisory ("manage aggressively") | AE-006 graduated escalation, CB-01..05 budgets, progressive disclosure | Full | HARD + L2 | Significant |
| Subagent architecture | Feature description (`.claude/agents/`) | P-003 constitutional, Pattern 2 orchestrator-worker, H-35 tool restriction | Full | HARD + L2 + L3 + L5 | Significant |
| CLAUDE.md instructions | Single file, manual pruning | Multi-layer: CLAUDE.md + rules + L2 re-injection + skills | Full | HARD + L1 + L2 | Significant |
| Hooks / deterministic enforcement | Feature description (run scripts) | 5-layer architecture (L1-L5), L3 AST gates, L5 CI gates | Full | Architecture-level | Significant |
| Tool scoping | `--allowedTools` flag | T1-T5 tiers, per-agent schema, tool count monitoring | Full | HARD + L3 + L5 | Significant |
| Verification / quality assurance | "Provide tests and criteria" | S-014 rubric (>= 0.92), H-14 creator-critic (3 min), C4 tournament | Full | HARD + L2 | Significant |
| Ambiguity resolution | "Be specific in prompts" | H-31 HARD rule, routing terminal, structured AskUserQuestion | Full | HARD + L2 | Minor |
| Skills / on-demand knowledge | Feature description (`.claude/skills/`) | H-22 proactive invocation, 5-column trigger map, H-25/H-26 standards | Full | HARD + L2 | Significant |
| Session management | `/clear`, `/rewind`, `/compact` | AE-006 auto-escalation, checkpoint persistence, Memory-Keeper | Full | HARD + L2 + MCP | Significant |
| Plan mode workflow | 4-phase: explore-plan-implement-commit | PM-M-001: explore-plan-approve-implement-verify (C2+) | Full | MEDIUM | Aligned |
| Extended thinking | Budget token allocation | ET-M-001: reasoning_effort mapped to criticality (C1-C4) | Full | MEDIUM | Minor |
| Writer/reviewer fresh context | Separate sessions for write and review | FC-M-001: Task tool isolation + independent C4 reviewer | Full | MEDIUM | Minor |
| Constitutional governance | Not documented | P-003/P-020/P-022 in every agent, S-007 compliance checks | Jerry only | HARD + L2 + L5 | N/A |
| Quality gate (quantitative) | Not documented | 0.92 threshold, 6 dimensions, 3 score bands | Jerry only | HARD + L2 | N/A |
| Criticality levels | Not documented | C1-C4 with proportional review depth | Jerry only | HARD + L2 | N/A |
| Adversarial strategies | Not documented | 10 strategies, scored, with templates | Jerry only | HARD + strategy templates | N/A |
| FMEA risk analysis | Not documented | RPN-scored failure modes, monitoring thresholds | Jerry only | Advisory (MEDIUM) | N/A |
| HARD rule ceiling | Not documented | 25 rules, 3-family derivation, exception mechanism | Jerry only | L5 CI gate | N/A |
| Agent definition schema | Minimal YAML (name, description, tools, model) | 15 required fields, JSON Schema validation, cognitive modes | Jerry only | HARD + L3 + L5 | N/A |
| Structured handoff protocol | Not documented | Schema-validated v2 with 9 required fields | Jerry only | MEDIUM + schema | N/A |
| Layered routing | Keyword matching only | 4-layer architecture with circuit breaker | Jerry only | HARD + L2 | N/A |
| Anti-pattern catalog | 5 failure patterns (advisory) | 8 anti-patterns with detection heuristics and prevention | Jerry only | Advisory + monitoring | N/A |
| Cognitive mode taxonomy | Not documented | 5 modes with design implications | Jerry only | MEDIUM + schema | N/A |
| Auto-escalation | Not documented | AE-001..006 change-based criticality escalation | Jerry only | HARD + L2 | N/A |

**Summary counts:**

| Category | Count |
|----------|-------|
| Areas where Jerry aligns with Anthropic | 9 |
| Areas where Jerry significantly exceeds Anthropic | 8 (of 9 aligned) |
| Practices unique to Jerry (no Anthropic equivalent) | 14 |
| Gaps where Anthropic led (now closed) | 3 |
| Total practice areas compared | 24 |

---

## Lessons for the Industry

Seven actionable insights from comparing a governance-first framework against vendor documentation.

### Lesson 1: Advisory Guidance Is Insufficient for Production

Anthropic's best practices are excellent advisory guidance. But "manage context aggressively" does not prevent context rot in practice. Jerry's graduated AE-006 escalation (WARNING → CRITICAL → EMERGENCY → COMPACTION) with automated responses at each tier demonstrates that **production systems need enforceable governance, not just good advice.**

### Lesson 2: The Enforcement Architecture Matters More Than the Rules

Jerry's 25 HARD rules would be meaningless without the 5-layer enforcement architecture (L1-L5). The critical insight: **rules written in CLAUDE.md are vulnerable to context rot.** L2 per-prompt re-injection and L3 deterministic gating provide context-rot-immune enforcement that CLAUDE.md instructions alone cannot achieve.

### Lesson 3: Context Rot Is a First-Class Architectural Concern

Both Jerry and Anthropic identify context window management as critical. Jerry goes further by treating context rot as a first-class failure mode with FMEA analysis (RPN 392 -- highest risk in the system), token budgets per agent (CB-01..05), and progressive disclosure tiers. **Framework authors should budget context tokens as carefully as they budget compute.**

### Lesson 4: Subagent Topology Needs Constitutional Limits

Anthropic describes subagents as flexible tools. Jerry's experience shows that **unconstrained delegation creates recursive depth and error amplification.** P-003's single-level nesting limit, backed by Google DeepMind's error amplification data (1.3x structured vs. 17x uncoordinated), demonstrates that topology constraints are not limitations but safety guarantees.

### Lesson 5: Quality Gates Need Dimensions, Not Just Pass/Fail

Anthropic recommends "provide tests and verification." Jerry's S-014 rubric adds dimensional scoring (completeness, consistency, rigor, evidence, actionability, traceability) with explicit weights. **Dimensional scoring enables targeted revision** -- an agent scoring 0.95 on completeness but 0.85 on traceability knows exactly what to fix.

### Lesson 6: Plan Mode Reduces Wrong-Direction Work

Anthropic's plan mode recommendation aligns with a fundamental insight: **the most expensive failure is solving the wrong problem.** Jerry's PM-M-001 formalizes this with a decision guide mapping conditions to plan mode usage, and H-31 provides the constitutional backstop (MUST ask when ambiguous).

### Lesson 7: Document Your Innovations, Not Just Your Compliance

Most framework documentation focuses on compliance with external standards. Jerry's comparison reveals that **the innovations beyond vendor guidance are the most valuable differentiators**: constitutional governance, adversarial review, FMEA-based risk analysis, and structured handoff protocols. Document what you do that nobody else does.

---

## References

### Anthropic Documentation

| Document | URL |
|----------|-----|
| Claude Code Overview | https://docs.anthropic.com/en/docs/claude-code/overview |
| Claude Code Best Practices | https://docs.anthropic.com/en/docs/claude-code/best-practices |

### Jerry Framework Files

| File | Content |
|------|---------|
| `CLAUDE.md` | Root context, navigation, identity |
| `.context/rules/quality-enforcement.md` | Quality gate SSOT, HARD rule index, enforcement architecture, strategy catalog |
| `.context/rules/agent-development-standards.md` | Agent definition schema, structural patterns, tool tiers, cognitive modes, handoff protocol |
| `.context/rules/agent-routing-standards.md` | Layered routing, circuit breaker, anti-patterns, scaling roadmap |
| `.context/rules/mandatory-skill-usage.md` | H-22 proactive invocation, 5-column trigger map |
| `.context/rules/project-workflow.md` | H-04, workflow phases, PM-M-001 plan mode |
| `.context/rules/python-environment.md` | H-05/H-06 UV-only |
| `.context/rules/mcp-tool-standards.md` | MCP-001/MCP-002 governance |
| `.context/rules/markdown-navigation-standards.md` | H-23/H-24 navigation tables |
| `docs/governance/JERRY_CONSTITUTION.md` | Constitutional principles P-003, P-020, P-022 |

### PROJ-007 Research Artifacts (Phase 1-2: Evidence Base)

> These artifacts contain the primary research that produced the evidence cited in this document. The orchestration root is `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/`.

| Artifact | Agent | Location (relative to orchestration root) | Claims Supported |
|----------|-------|------------------------------------------|-----------------|
| Claude Code Architecture & Capabilities | ps-researcher-001 | `ps/phase-1/ps-researcher-001/` | Areas 2-5 (subagent, CLAUDE.md, hooks, tools) |
| Agent Routing & Trigger Design | ps-researcher-002 | `ps/phase-1/ps-researcher-002/` | Innovation 11 (layered routing), 12 (anti-patterns), Area 8 (skills) |
| Industry Best Practices & Prior Art | ps-researcher-003 | `ps/phase-1/ps-researcher-003/` | Error amplification data (1.3x vs 17x), Innovation 6 (adversarial), Area 6 (verification) |
| LLM Instruction-Following Capacity | ps-researcher-004 | `ps/phase-1/ps-researcher-004/` | Innovation 8 (HARD rule ceiling), Innovation 2 (5-layer enforcement), Innovation 3 (L2 re-injection) |
| Agent Design Alternatives (Trade Study) | nse-explorer-001 | `nse/phase-1/nse-explorer-001/` | Innovation 9 (agent schema), Innovation 13 (cognitive modes) |
| Pattern Family Analysis | ps-analyst-001 | `ps/phase-2-analysis/ps-analyst-001/` | Innovation 13 (cognitive modes), Innovation 9 (agent schema) |
| Routing Pattern Analysis | ps-analyst-002 | `ps/phase-2-analysis/ps-analyst-002/` | Innovation 11 (layered routing), Area 8 (skills) |
| Context Rot Investigation | ps-investigator-001 | `ps/phase-2-analysis/ps-investigator-001/` | Area 1 (context window), Innovation 2 (5-layer enforcement) |
| Architecture Analysis | nse-architecture-001 | `nse/phase-2-analysis/nse-architecture-001/` | Innovation 2 (5-layer enforcement), Innovation 14 (auto-escalation) |
| Requirements Specification | nse-requirements-001 | `nse/phase-2-analysis/nse-requirements-001/` | H-34/H-35 source requirements (AR-*, SR-*, PR-*, HR-* IDs) |
| Risk Assessment (FMEA) | nse-risk-001 | `nse/phase-2-analysis/nse-risk-001/` | Innovation 7 (FMEA, RPN 392/336/280/252) |

### PROJ-007 Synthesis Artifacts (Phase 3-5: Derived Deliverables)

| Artifact | Location |
|----------|----------|
| Unified Pattern Taxonomy (66 patterns, 8 families) | `docs/knowledge/agent-pattern-taxonomy.md` |
| Phase 3 Synthesis | `ps/phase-3-synthesis/ps-synthesizer-001/` (relative to orchestration root) |
| ADR-PROJ007-001 (Agent Design) | `docs/design/ADR-PROJ007-001-agent-definition-format.md` |
| ADR-PROJ007-002 (Routing Framework) | `docs/design/ADR-PROJ007-002-agent-routing-framework.md` |
| V&V Plan | `nse/phase-3-synthesis/nse-verification-001/` (relative to orchestration root) |
| C4 Tournament Report | `ps/phase-5-review/adversary/` (relative to orchestration root) |
| Final Synthesis | `ps/phase-5-review/ps-reporter-001/` (relative to orchestration root) |
| EN-003 Gap Closures | `projects/PROJ-007-agent-patterns/WORKTRACKER.md` (TASK-030..036) |

---

<!-- VERSION: 1.1.0 | DATE: 2026-02-22 | SOURCE: EN-003 (PROJ-007) | REVISION: Added Phase 1-2 research artifact traceability -->
*Publication Version: 1.1.0*
*Source: PROJ-007 Agent Patterns -- EN-003 Gap Closure & Publication*
*Created: 2026-02-22*
*Criticality: C2 (knowledge artifact)*
