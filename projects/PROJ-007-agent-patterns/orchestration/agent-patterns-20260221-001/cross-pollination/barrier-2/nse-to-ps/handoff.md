# Barrier 2 Cross-Pollination: NSE Pipeline -> PS Pipeline

<!-- HANDOFF: barrier-2 | DIRECTION: nse-to-ps | DATE: 2026-02-21 -->

> Synthesized findings from NASA SE Phase 2 Analysis (3 agents) for consumption by Problem-Solving Phase 3 Synthesis agents (ps-synthesizer-001, ps-architect-001, ps-architect-002).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Key Findings Summary](#key-findings-summary) | Critical analysis outcomes across all 3 NSE agents |
| [Requirements Specification](#requirements-specification) | From nse-requirements-001: 52 shall-statements, 6 domains |
| [Architecture Reference Model](#architecture-reference-model) | From nse-architecture-001: hexagonal mapping, 10 patterns, 3 ADRs |
| [Risk Assessment](#risk-assessment) | From nse-risk-001: 30 risks, 3 RED, mitigation priorities |
| [Cross-Agent Consensus](#cross-agent-consensus) | Where all 3 NSE agents converge |
| [PS Phase 3 Guidance](#ps-phase-3-guidance) | Specific inputs for each PS agent |

---

## Key Findings Summary

### Bottom Line

The NSE pipeline has produced a **comprehensive formal engineering foundation** for agent pattern codification. The three Phase 2 outputs are mutually reinforcing: requirements specify WHAT must be true, architecture defines HOW to achieve it, and risk assessment identifies WHERE things can go wrong. Three strategic themes emerge:

1. **Schema validation is the highest-value single enhancement** -- appears as the #1 priority in all three NSE analyses (AR-003 requirement, Pattern 8 quality gate pre-check in architecture, R-Q01 false positive mitigation in risk)
2. **Structured handoff protocol is non-negotiable** -- 6 handoff requirements (HR-001 through HR-006) formalized, JSON Schema defined in architecture, R-T02 error amplification mitigated
3. **Criticality-proportional enforcement must be preserved** -- C1-C4 mapping validated across all three analyses; avoid one-size-fits-all quality approaches

### Quantitative Summary

| Metric | Value | Source |
|--------|-------|--------|
| Requirements formalized | 52 shall-statements across 6 domains | nse-requirements-001 |
| Stakeholder needs traced | 15 needs across 4 stakeholder types | nse-requirements-001 |
| INCOSE quality criteria | 8/8 PASS | nse-requirements-001 |
| Design patterns cataloged | 10 across 5 categories | nse-architecture-001 |
| Architecture decisions documented | 3 ADRs (definition format, routing, QA) | nse-architecture-001 |
| Hexagonal layer mappings | 4 layers (domain, port, adapter, infrastructure) | nse-architecture-001 |
| Tool security tiers defined | 5 tiers (T1 read-only through T5 full) | nse-architecture-001 |
| Context budget rules | 5 (CB-01 through CB-05) | nse-architecture-001 |
| Risks identified | 30 across 7 categories | nse-risk-001 |
| RED-zone risks | 3 (context rot, error amplification, rule proliferation) | nse-risk-001 |
| YELLOW-zone risks | 14 | nse-risk-001 |
| Top mitigation actions | 5 (rule consolidation, schema pre-check, context monitor, handoff contracts, score monitoring) | nse-risk-001 |
| Open items requiring resolution | 7 | nse-requirements-001 |

---

## Requirements Specification

### 6 Requirement Domains with Counts

| Domain | ID Prefix | Count | Scope | Key Requirements |
|--------|-----------|-------|-------|-----------------|
| Agent Structure | AR | 12 | Definition format, nesting, isolation, tools, naming, registration | AR-001 (YAML+MD format), AR-003 (schema validation), AR-004 (single-level nesting) |
| Prompt Design | PR | 8 | Role, cognitive mode, expertise, progressive disclosure, persona, model selection | PR-002 (cognitive mode enum), PR-004 (progressive disclosure), PR-007 (model justification) |
| Routing | RR | 8 | Keywords, determinism, LLM fallback, negative keywords, loop prevention | RR-001 (keyword primary), RR-003 (LLM fallback), RR-006 (loop prevention max 3 hops) |
| Handoff | HR | 6 | Structured format, required fields, artifact validation, state preservation | HR-001 (structured format mandatory), HR-002 (required fields), HR-006 (quality gate at handoff) |
| Quality | QR | 9 | Criticality-proportional, self-review, schema validation, creator-critic, tournament | QR-001 (proportional enforcement), QR-005 (0.92 threshold), QR-008 (tournament for C4) |
| Safety & Governance | SR | 10 | Constitutional compliance, guardrails, user authority, audit trails, MCP governance | SR-001 (P-003/P-020/P-022), SR-007 (auto-escalation AE-001 to AE-006), SR-010 (H-31 ambiguity) |

### Priority Distribution

| Priority | Count | Examples |
|----------|-------|---------|
| MUST | 43 | AR-001, AR-004, RR-001, HR-001, QR-005, SR-001 |
| SHOULD | 9 | AR-003 (schema validation), RR-003 (LLM fallback), PR-005 (persona), SR-006 (audit trails) |

### Verification Method Distribution

| Method | Count | Notes |
|--------|-------|-------|
| Inspection | 28 (45%) | Schema validation, regex checks, field presence |
| Test | 24 (39%) | Behavioral tests, boundary conditions |
| Analysis | 18 (29%) | Cross-reference, consistency, cognitive mode alignment |

### Traceability Coverage

- 100% bidirectional traceability to Phase 1 research findings
- 100% traceability to existing Jerry rules (H-01 through H-31)
- 100% traceability to trade study recommendations (TS-1 through TS-5)
- 15 stakeholder needs (SN-01 through SN-15) fully covered

### Open Items for PS Phase 3 Resolution

| ID | Item | Related Requirement | Suggested Resolution |
|----|------|---------------------|---------------------|
| OI-01 | JSON Schema format for agent definition validation | AR-003 | Use JSON Schema Draft 2020-12 (widest tooling support) |
| OI-02 | Confidence threshold for LLM routing fallback | RR-003 | Empirically determine via logging |
| OI-03 | Open Agent Specification adoption | AR-002/AR-003 | Evaluate for compatible elements |
| OI-04 | Output schema variability across L0/L1/L2 levels | QR-003/PR-008 | Define base schema with optional level-specific sections |
| OI-05 | Maximum agent count before team-based grouping | AR-004/AR-011 | Monitor; TS-1 suggests ~50-agent threshold |
| OI-06 | Audit trail storage mechanism | SR-006 | Start with filesystem; migrate to Memory-Keeper if needed |
| OI-07 | Negative keyword data structure | RR-005 | Extend trigger map with "Negative Keywords" column |

---

## Architecture Reference Model

### Hexagonal Architecture Mapping

The architecture maps hexagonal concepts to agent design:

| Hexagonal Layer | Agent Equivalent | Contents |
|----------------|-----------------|----------|
| **Domain** | Reasoning Core | Cognitive mode, expertise, decision logic, quality standards, methodology |
| **Port** | Tool Interfaces | `capabilities.allowed_tools` -- abstract contracts for what the agent needs |
| **Adapter** | Prompt Strategies & Formatters | System prompt construction, input deserialization, L0/L1/L2 output formatting, handoff serialization |
| **Infrastructure** | Runtime Environment | Claude Code platform, context window, model selection, MCP server connections |

**Key Invariant:** Domain layer MUST NOT depend on any outer layer (maps to H-07).

### 10 Design Patterns

| # | Pattern | Category | Problem Solved | Jerry Validation |
|---|---------|----------|---------------|------------------|
| 1 | Specialist Agent | Structural | Context rot from generalist overload | 37 agents across 8 skills |
| 2 | Orchestrator-Worker | Structural | Uncoordinated "bag of agents" (17x amplification) | P-003, orch-planner/tracker |
| 3 | Creator-Critic-Revision | Quality | Self-review blind spots, leniency bias | H-14, ps-critic, adv-scorer |
| 4 | Progressive Disclosure | Context | Context window exhaustion from upfront loading | Three-tier skill loading |
| 5 | Tool Restriction | Security | Principle of least privilege violation | T1-T5 tiers, TOOL_REGISTRY.yaml |
| 6 | Structured Handoff | Integration | Free-text handoff information loss (#1 failure) | JSON Schema, session_context |
| 7 | Context Budget | Context | Mid-task context exhaustion | CB-01 through CB-05 |
| 8 | Quality Gate | Governance | Quality variance, undetected defects | H-13, 4-layer gate architecture |
| 9 | Cognitive Mode | Behavioral | Wrong reasoning approach for task type | 5 modes: divergent/convergent/integrative/systematic/forensic |
| 10 | Layered Routing | Integration | Single routing mechanism brittleness | Keyword -> decision tree -> LLM fallback |

### 3 Architecture Decision Records

| ADR | Decision | Status | Key Rationale |
|-----|----------|--------|---------------|
| ADR-001 | Agent Definition Format: YAML+MD with schema validation (B5) | Recommended | +0.45 over current B1; schema validation is deterministic pre-check |
| ADR-002 | Routing Architecture: Keyword-first with LLM fallback (C5) | Recommended | +0.05 over current C1; small delta validates keyword-first foundation |
| ADR-003 | QA Architecture: Layered (Schema + Self-Review + Critic) (D6) | Recommended | +0.40 over current D2; schema pre-check reduces critic workload |

### Tool Security Tiers

| Tier | Name | Tools | Use Case |
|------|------|-------|----------|
| T1 | Read-Only | Read, Glob, Grep | Evaluation, auditing, scoring |
| T2 | Read-Write | T1 + Write, Edit, Bash | Analysis, document production |
| T3 | External | T2 + WebSearch, WebFetch, Context7 | Research, exploration |
| T4 | Persistent | T2 + Memory-Keeper | Cross-session state management |
| T5 | Full | T3 + T4 + Task | Orchestration, delegation |

**Selection Rule:** Always select the lowest tier that satisfies requirements. T5 requires P-003 compliance verification.

### Context Budget Allocation

| Category | Allocation | Tokens |
|----------|-----------|--------|
| System Prompt | ~5% | ~10,000 |
| User Messages | ~10-20% | ~20,000-40,000 |
| Tool Results | ~40-50% | ~80,000-100,000 |
| Reasoning + Output | ~25-35% | ~50,000-70,000 |
| Safety Margin | ~5% | ~10,000 |

---

## Risk Assessment

### 3 RED-Zone Risks (Score 15-25)

| ID | Risk | Score | L x I | Core Concern | Top Mitigation |
|----|------|-------|-------|--------------|----------------|
| R-T01 | Context Rot at Scale | 20 | 5 x 4 | Agent reasoning degrades as context fills; L1 enforcement vulnerable | Context budget monitor (warn 60%, halt 80%) + agent self-diagnostics |
| R-T02 | Error Amplification | 15 | 3 x 5 | 17x amplification in uncoordinated topologies; handoff boundaries at risk | JSON Schema handoff contracts + validation gates |
| R-P02 | Rule Proliferation | 15 | 3 x 5 | 31/35 HARD rule slots used (89%); approaching ceiling | Rule consolidation audit (merge H-25 to H-30) |

### Top 5 Mitigation Actions by Net Priority

| Rank | Action | Addresses Risks | Net Priority |
|------|--------|----------------|--------------|
| 1 | Rule consolidation audit (merge H-25 to H-30 into ~2 compound rules) | R-P02 | 9.00 |
| 2 | Schema validation pre-check layer (deterministic, zero LLM cost) | R-Q01, R-A03 | 6.00 |
| 3 | Context budget monitor and degradation detection | R-T01 | 5.00 |
| 4 | JSON Schema handoff contracts for all agent-to-agent transitions | R-T02, R-A03 | 4.50 |
| 5 | Score stability and variance monitoring | R-T06, R-O01 | 4.00 |

### Risk Landscape Distribution

| Zone | Count | Percentage |
|------|-------|------------|
| RED (15-25) | 3 | 10% |
| YELLOW (5-12) | 14 | 47% |
| GREEN (1-4) | 13 | 43% |

### Key Risk Findings for PS Phase 3

1. **Context rot (R-T01) is the #1 risk** -- mitigated partially by progressive disclosure and filesystem-as-memory, but unmitigated in multi-agent orchestration (4+ handoffs) and long sessions
2. **Rule proliferation (R-P02) is a process risk** -- 31/35 slots consumed; the codification phase must consolidate rather than add rules
3. **Quality gate false positives (R-Q01) undermine trust** -- schema validation pre-check addresses this as a deterministic complement to LLM-as-Judge
4. **Token cost escalation (R-O01) compounds** -- C4 tournament can consume 100K+ tokens; proportional enforcement is essential
5. **Error amplification at handoff boundaries (R-T02)** -- Jerry's formal topology reduces 17x to ~1.3x, but structured handoffs are necessary to maintain this

---

## Cross-Agent Consensus

These findings appear consistently across all 3 NSE Phase 2 agents:

| # | Consensus Finding | Requirements | Architecture | Risk |
|---|-------------------|-------------|--------------|------|
| 1 | Schema validation is the highest-priority enhancement | AR-003 (SHOULD, highest-value) | ADR-001 (B5), Pattern 8 Layer 1 | R-Q01 mitigation #1 |
| 2 | Structured handoff protocol is non-negotiable | HR-001 through HR-006 (5 MUST) | Pattern 6, JSON Schema defined | R-T02 mitigation, R-A03 mitigation |
| 3 | Single-level nesting (P-003) is validated | AR-004 (MUST) | Pattern 2, TS-1 winner | Formal topology reduces 17x to 1.3x |
| 4 | Keyword-first routing is optimal for current scale | RR-001 (MUST), RR-003 (SHOULD) | ADR-002, Pattern 10 | No routing-specific RED risk |
| 5 | Criticality-proportional enforcement is essential | QR-001 (MUST) | Pattern 8 (4-layer gate) | R-P01 (governance overhead) mitigation |
| 6 | Progressive disclosure prevents context rot | PR-004 (MUST) | Pattern 4, CB-01 to CB-05 | R-T01 mitigation (partial) |
| 7 | Tool restriction by least privilege | AR-006 (MUST) | Pattern 5, T1-T5 tiers | R-S02 (tool misuse) controlled |
| 8 | Rule consolidation needed before adding more | Not addressed (existing rules sufficient) | Not addressed | R-P02 (#2 net priority action) |
| 9 | Cognitive mode specialization differentiates agents | PR-002 (MUST, enumerated set) | Pattern 9, 5 modes defined | Not risk-assessed (low concern) |
| 10 | Audit trail and observability gaps exist | SR-006 (SHOULD), RR-008 (SHOULD) | Not detailed | R-Q04 (scoring drift), R-T03 (model regression) |

---

## PS Phase 3 Guidance

### For ps-synthesizer-001 (Pattern Taxonomy Synthesis)

Use these findings to create a unified pattern taxonomy:
- **Map 10 architecture patterns to 8 PS pattern families** -- the architecture catalog (10 patterns) and PS taxonomy (57 patterns in 8 families) must be reconciled into a single coherent catalog
- **Anchor each pattern with requirements** -- every pattern in the taxonomy should trace to at least one requirement from the 52 shall-statements
- **Validate with risk assessment** -- patterns should address the 3 RED-zone risks; any pattern that does not mitigate at least one identified risk may be over-engineered
- **Resolve the open items** -- OI-01 through OI-07 from nse-requirements-001 need resolution or explicit deferral with justification
- **Incorporate the rule consolidation finding** -- the pattern taxonomy should recommend how to consolidate H-25 through H-30 (6 skill-standards rules) into compound rules to address R-P02

### For ps-architect-001 (Agent Design ADR)

Use these findings to design the agent design patterns ADR:
- **Adopt ADR-001 (YAML+MD + schema validation)** from nse-architecture-001 as the baseline, extending it with specific schema fields from the 12 AR-requirements
- **Reference the hexagonal mapping** -- the ADR should explain how agent definitions map to hexagonal layers (domain = reasoning core, ports = tools, adapters = prompts)
- **Define the canonical agent definition template** -- consolidate AR-001 through AR-012 into a concrete YAML+MD template with all required and recommended fields
- **Address the 5 tool security tiers** (T1-T5) as part of agent design, with selection guidelines from the architecture
- **Incorporate risk mitigations** -- the ADR must address R-T01 (context rot via progressive disclosure), R-T02 (error amplification via structured handoffs), and R-P02 (rule proliferation via consolidation)
- **Resolve OI-01** (JSON Schema format) and OI-03 (Open Agent Specification adoption) as part of the decision

### For ps-architect-002 (Routing/Trigger ADR)

Use these findings to design the routing framework ADR:
- **Adopt ADR-002 (keyword-first + LLM fallback)** from nse-architecture-001 as the baseline
- **Reference the 8 routing requirements** (RR-001 through RR-008) -- the ADR must satisfy all 8
- **Incorporate the layered routing pattern** (Pattern 10) with its 3-layer architecture: keyword -> decision tree -> LLM fallback
- **Design the negative keyword mechanism** -- resolve OI-07 and define how negative keywords integrate into the existing trigger map format
- **Address the scaling trajectory** from PS Phase 2: keyword-only optimal at 8 skills, breaks at ~15, needs full layered approach at 20+
- **Define circuit breaker specifications** -- RR-006 requires max 3 routing hops; specify the detection and termination mechanism
- **Resolve OI-02** (confidence threshold for LLM fallback activation) as part of the decision
- **Incorporate 8 routing anti-patterns** from ps-analyst-002 as negative examples with detection heuristics
