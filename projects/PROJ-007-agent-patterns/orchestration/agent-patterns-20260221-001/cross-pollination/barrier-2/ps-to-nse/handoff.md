# Barrier 2 Cross-Pollination: PS Pipeline -> NSE Pipeline

<!-- HANDOFF: barrier-2 | DIRECTION: ps-to-nse | DATE: 2026-02-21 -->

> Synthesized findings from Problem-Solving Phase 2 Analysis (3 agents) for consumption by NASA SE Phase 3 Synthesis agents (nse-verification-001, nse-integration-001).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Key Findings Summary](#key-findings-summary) | Critical analysis outcomes across all 3 PS agents |
| [Pattern Taxonomy](#pattern-taxonomy) | From ps-analyst-001: 57 patterns, 8 families |
| [Gap Analysis](#gap-analysis) | From ps-analyst-001: 12 identified gaps |
| [Routing Analysis](#routing-analysis) | From ps-analyst-002: scaling, anti-patterns, handoff schema |
| [Failure Mode Analysis](#failure-mode-analysis) | From ps-investigator-001: 28 FMEA modes, corrective actions |
| [NSE Phase 3 Guidance](#nse-phase-3-guidance) | Specific inputs for each NSE agent |

---

## Key Findings Summary

### Bottom Line

Jerry's agent patterns are **architecturally sound but have specific measurable gaps**. The analysis phase quantified these gaps across three dimensions: pattern coverage (67% overall, weakest in Testing at 43%), failure risk (28 modes, 5 critical), and routing scalability (breaks at ~15 skills). Three consensus priorities emerge:

1. **Schema validation** -- highest impact single enhancement (gaps GAP-01, GAP-02; FMEA CF-01 mitigation; requirement AR-004/QR-003)
2. **Structured handoff protocol** -- addresses #1 failure source (gap GAP-03; FMEA HF-01 RPN=336; JSON Schema proposed)
3. **Anti-pattern codification** -- 10 anti-patterns identified with detection heuristics and prevention rules

### Quantitative Summary

| Metric | Value | Source |
|--------|-------|--------|
| Total patterns identified | 57 across 8 families | ps-analyst-001 |
| Jerry implementation rate | 67% overall (46/57 partially+) | ps-analyst-001 |
| Maturity score | 3.3/5 (Defined level) | ps-analyst-001 |
| Gaps identified | 12 (3 P1, 4 P2, 5 P3) | ps-analyst-001 |
| Routing approaches evaluated | 6 across 7 dimensions | ps-analyst-002 |
| Keyword scaling limit | ~15 skills before breakdown | ps-analyst-002 |
| Anti-patterns codified | 8 routing + 10 general = 18 total | ps-analyst-002 + ps-investigator-001 |
| FMEA failure modes | 28 across 7 categories | ps-investigator-001 |
| Highest RPN | 392 (context rot at scale) | ps-investigator-001 |
| Corrective actions proposed | 12 (4 immediate, 5 structural, 3 preventive) | ps-investigator-001 |

---

## Pattern Taxonomy

### 8 Pattern Families with Implementation Rates

| Family | Total | Implemented | Rate | Strongest | Weakest |
|--------|-------|-------------|------|-----------|---------|
| Workflow | 7 | 6 | 86% | Prompt chaining, routing, parallelization | Evaluator-optimizer partially |
| Delegation | 9 | 5 | 56% | Orchestrator-worker (P-003) | Contract-first delegation missing |
| Quality | 10 | 8 | 80% | Creator-critic-revision, tournament mode | Schema validation missing |
| Context | 12 | 8 | 67% | Progressive disclosure, filesystem-as-memory | Context budget monitoring missing |
| Safety | 9 | 8 | 89% | Constitutional AI, guardrails, bounded autonomy | Prompt injection defense partial |
| Testing | 7 | 3 | 43% | LLM-as-Judge | Behavioral testing, drift detection missing |
| Integration | 7 | 3 | 43% | MCP, static tool assignment | Capability discovery, structured handoff missing |
| Governance | 5 | 5 | 100% | Human-in-the-loop, approval gates, audit trails | None |

### Maturity by Family (1-5 Scale)

- Governance: 4.5 (Managed/Optimizing) -- unique competitive advantage
- Safety: 4.3 (Managed)
- Quality: 4.2 (Managed)
- Workflow: 3.8 (Defined+)
- Context: 3.4 (Defined)
- Delegation: 3.0 (Defined)
- Integration: 2.6 (Repeatable)
- Testing: 2.1 (Repeatable) -- largest gap

---

## Gap Analysis

### Priority 1 (Critical)

| ID | Gap | Impact | Effort |
|----|-----|--------|--------|
| GAP-01 | Schema validation for agent definitions | Catches structural defects deterministically | Medium |
| GAP-02 | Schema validation as QA pre-check layer | Reduces critic workload, zero LLM cost | Medium |
| GAP-03 | Structured handoff protocol (JSON Schema) | Addresses #1 failure source per Google 2026 | Medium |

### Priority 2 (Strategic)

| ID | Gap | Impact | Effort |
|----|-----|--------|--------|
| GAP-04 | Agent behavioral testing framework | Closes largest maturity gap (Testing at 2.1) | High |
| GAP-05 | Routing interface abstraction | Enables layered routing without rewriting | Low |
| GAP-06 | Context budget monitoring | Prevents context rot (RPN=392 top risk) | Medium |
| GAP-07 | Iteration ceiling enforcement | Prevents infinite loops in critic cycles | Low |

### Priority 3 (Evolutionary)

| ID | Gap | Impact | Effort |
|----|-----|--------|--------|
| GAP-08 | LLM routing fallback | Handles ambiguous cases (~20% of requests) | Medium |
| GAP-09 | Capability discovery for tools | Future-proofs tool integration | High |
| GAP-10 | Drift detection | Catches quality degradation over time | High |
| GAP-11 | Contract-first delegation | Formal handoff contracts per DeepMind | High |
| GAP-12 | Scoring variance monitoring | Detects leniency drift in S-014 scoring | Low |

---

## Routing Analysis

### Current State

- 49 keywords across 7 skills in `mandatory-skill-usage.md`
- 4 keyword collision zones identified (e.g., "review" maps to multiple skills)
- ~45-55% semantic coverage (many valid requests don't match any keyword)
- No conflict resolution mechanism, no multi-intent handling

### Scaling Trajectory

| Skill Count | Routing Approach | Rationale |
|-------------|-----------------|-----------|
| 8 (current) | Keyword-only | Optimal -- collision zones manageable |
| 10-15 | Keyword + negative keywords + priority ordering | Collision zones multiply, need disambiguation |
| 15-20 | Keyword + rule-based decision tree | False negative rate rises to 35-45% |
| 20+ | Full layered (keyword + decision tree + LLM fallback) | Essential for novel/compound requests |

### Recommended Handoff Schema (JSON)

Required fields for every agent-to-agent handoff:
- `task` (string): What the receiving agent should do
- `success_criteria` (array): How to judge completion
- `artifacts` (array of paths): Files to read
- `key_findings` (array, 3-5 items): Orientation bullets
- `blockers` (array): Known impediments
- `confidence` (float 0-1): Sender's confidence in findings
- `criticality` (enum): C1/C2/C3/C4

### 8 Routing Anti-Patterns

1. **Keyword Tunnel** -- routing only by keywords, missing semantic intent
2. **Bag of Triggers** -- uncoordinated keyword lists with overlaps
3. **Telephone Game** -- information degrades through sequential handoffs
4. **Routing Loop** -- agents bounce without circuit breaker
5. **Over-Routing** -- too many hops before reaching the right agent
6. **Under-Routing** -- single agent handles everything
7. **Tool Overload Creep** -- agents accumulate tools beyond their need
8. **Context-Blind Routing** -- ignoring context fill level when routing

---

## Failure Mode Analysis

### Top 5 Failure Modes by Risk Priority Number

| ID | Failure Mode | RPN | Severity | Occurrence | Detection |
|----|-------------|-----|----------|------------|-----------|
| CF-01 | Context rot at scale | 392 | 8 | 7 | 7 |
| HF-01 | Free-text handoff information loss | 336 | 8 | 7 | 6 |
| PF-01 | Prompt drift over iterations | 288 | 8 | 6 | 6 |
| QF-02 | Quality gate false positive scoring | 280 | 7 | 8 | 5 |
| RF-04 | Routing loops without circuit breakers | 252 | 7 | 6 | 6 |

### Root Causes (5 Whys Analysis)

1. **Context rot** -> No monitoring of context fill -> No budget allocation -> Filesystem-as-memory not sufficient alone -> Need runtime awareness
2. **Handoff loss** -> Free-text format -> No schema validation -> No structured contract -> Need JSON Schema enforcement
3. **Prompt drift** -> Role instructions fade in deep context -> L2 re-injection only covers rules -> Agent identity not re-injected -> Need identity anchoring
4. **False positive scoring** -> LLM leniency bias -> Rubric allows subjective interpretation -> No cross-scorer calibration -> Need score stability checks
5. **Routing loops** -> No iteration counter on routing decisions -> No circuit breaker pattern -> Need max-hop enforcement

### Jerry Vulnerability Assessment

**Protected (9 modes):** P-003 prevents recursive agents, P-020 prevents unauthorized actions, H-13 threshold prevents low-quality acceptance, H-14 ensures multi-pass review, H-16 ensures steelman-first, Constitutional AI (S-007) catches governance violations, Static tool assignment prevents tool sprawl, Filesystem persistence prevents state loss, UV-only prevents environment corruption.

**Exposed (9 modes, prioritized):** Context rot at scale (P1), free-text handoff loss (P1), prompt drift (P2), scoring false positives (P2), routing loops (P3), keyword tunnel (P3), iteration ceiling (P3), critic independence (P3), effort scaling (P3).

### Corrective Actions

**Immediate (4):**
- IA-01: Max iteration caps on all looping constructs
- IA-02: Structured handoff schema (JSON Schema)
- IA-03: Anti-leniency scoring guidance in S-014 rubric
- IA-04: Context decomposition guidelines

**Structural (5):**
- SF-01: Intermediate quality gates within phases
- SF-02: Critic independence verification
- SF-03: Routing enhancement (negative keywords + priority)
- SF-04: Effort scaling proportional to criticality
- SF-05: Session segmentation for long-running agents

**Preventive (3):**
- PM-01: UV enforcement hook (existing)
- PM-02: Handoff validation hook (new)
- PM-03: Context fill monitoring (new)

---

## NSE Phase 3 Guidance

### For nse-verification-001 (V&V Planning)

Use these findings to design verification and validation criteria:
- **Requirements verification:** Map the 52 shall-statements from nse-requirements-001 to specific V&V methods (Inspection/Analysis/Test) -- already specified per-requirement
- **Gap verification:** Design tests that prove GAP-01 through GAP-12 are closed when addressed
- **FMEA validation:** Create acceptance criteria based on RPN reduction targets for the top 5 failure modes
- **Anti-pattern detection:** Define automated checks that detect the 18 anti-patterns in code/configuration
- **Routing validation:** Define test scenarios for keyword coverage, collision resolution, and scaling thresholds
- **Quality gate validation:** Verify scoring consistency across multiple runs (address QF-02 false positive risk)

### For nse-integration-001 (Integration Patterns)

Use these findings to design integration standards:
- **Handoff protocol:** Adopt the JSON Schema from ps-analyst-002 as the basis for structured handoff contracts
- **Context passing:** Design conventions for artifact references, key findings summaries, and confidence signaling
- **Routing integration:** Define how the 3-layer routing architecture interfaces with existing `mandatory-skill-usage.md`
- **Quality gate integration:** Specify how schema validation (Layer 1) integrates with self-review (Layer 2) and critic review (Layer 3)
- **Anti-pattern prevention:** Build detection heuristics into integration tests
- **Circuit breakers:** Design max-hop and iteration ceiling enforcement patterns
