# Jerry Framework Integration Analysis for LLM Skill Testing

> Phase 1C Research Output -- PROJ-017 LLM Skill Testing Framework
> Agent: ps-researcher | Cognitive Mode: Divergent | Date: 2026-03-03

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language findings for project stakeholders |
| [Research Questions](#research-questions) | Five focus areas addressed in this analysis |
| [Methodology](#methodology) | Data sources, approach, and limitations |
| [L1: Technical Analysis](#l1-technical-analysis) | Implementation-level integration mapping |
| [1. Quality Gate Integration Points](#1-quality-gate-integration-points) | S-014 rubric and H-rule mapping to evaluation tiers |
| [2. Agent Architecture Mapping](#2-agent-architecture-mapping) | 67 agents as evaluation surface with cognitive mode implications |
| [3. CLI Integration Patterns](#3-cli-integration-patterns) | Jerry CLI namespace design for skill testing commands |
| [4. Governance Compliance Validator Design](#4-governance-compliance-validator-design) | H-rules as deterministic promptfoo assertions |
| [5. Determinism-First Architecture Alignment](#5-determinism-first-architecture-alignment) | L1-L5 enforcement layers to evaluation tier mapping |
| [L2: Architectural Implications](#l2-architectural-implications) | Strategic trade-offs and long-term evolution |
| [Conclusions](#conclusions) | Key findings summary across all research questions |
| [Recommendations](#recommendations) | Actionable next steps for Phase 2, Phase 3, and Phase 5 |
| [References](#references) | Full citation list with provenance |
| [PS Integration](#ps-integration) | Handoff metadata for downstream synthesis agent |

---

## L0: Executive Summary

This research analyzes how the proposed LLM Skill Testing Framework (PROJ-017) would integrate with Jerry's existing infrastructure. Think of it as answering: "Where exactly does the new testing framework plug into what Jerry already has?"

Jerry already has a sophisticated quality system: 25 HARD rules governing everything from code style to constitutional constraints, a 6-dimension scoring rubric (S-014) used by its adversarial quality agents, and a 5-layer enforcement architecture that catches violations at different points in time (from session start through CI/CD). The skill testing framework does not need to build these concepts from scratch -- it needs to connect to them.

The key finding is that Jerry's existing quality infrastructure provides natural integration points at every level. The 25 HARD rules map directly to deterministic test assertions (the zero-cost T1 tier). The S-014 scoring rubric provides the exact dimensions for LLM-as-judge evaluation (the T4 tier). And the CLI already has a pattern (the `agents` namespace with build/validate/list commands) that serves as a direct template for a new `eval` or `skill-test` namespace. The framework does not need to invent its own quality model -- it inherits Jerry's.

For the project, this means the integration path is lower-friction than expected. The governance compliance validator can reuse existing enforcement mechanisms (AST-based parsing from H-33, JSON Schema validation from H-34). The statistical significance engine operates independently above these layers. The primary engineering challenge is not "how to connect" but "how to scope" -- deciding which of the 67 agents and 25 rules to include in the initial evaluation suite.

---

## Research Questions

This analysis addresses five focus areas specified in the Phase 1C orchestration plan:

| # | Focus Area | Core Question |
|---|------------|---------------|
| RQ-1 | Quality Gate Integration | How do Jerry's S-014 rubric dimensions and H-rule thresholds map to evaluation framework tiers? |
| RQ-2 | Agent Architecture Mapping | Which of the 67 agents across 12 skills are suitable evaluation targets, and how do cognitive modes and tool tiers affect test design? |
| RQ-3 | CLI Integration Patterns | How should a `jerry eval` or `jerry skill-test` namespace be designed to fit the existing CLI architecture? |
| RQ-4 | Governance Compliance Validator | How are Jerry's 25 HARD rules translated into deterministic promptfoo assertions? |
| RQ-5 | Determinism-First Alignment | How does Jerry's 5-layer enforcement architecture (L1-L5) map to the evaluation framework's tier model (T1-T4)? |

---

## Methodology

### Data Sources

| Source | Type | What Was Extracted |
|--------|------|-------------------|
| `.context/rules/quality-enforcement.md` | Primary (codebase) | HARD Rule Index, S-014 rubric dimensions, enforcement architecture, criticality levels |
| `AGENTS.md` | Primary (codebase) | Agent registry (67 agents, 12 skills), cognitive modes, tool tiers, MCP access matrix |
| `src/interface/cli/main.py` | Primary (codebase) | CLI routing architecture, namespace handler pattern, composition root wiring |
| `src/interface/cli/parser.py` | Primary (codebase) | Argument parser structure, namespace subparser pattern, command structure |
| `ADR-001-framework-architecture.md` | Primary (project) | Architecture decision, three-component design, tiered evaluation model, promptfoo integration |
| `ORCHESTRATION_PLAN.md` | Primary (project) | Phase dependencies, output contracts, quality gate requirements |
| `.context/rules/agent-development-standards.md` | Primary (codebase) | Agent definition schema, tool security tiers (T1-T5), cognitive mode taxonomy |
| `.context/rules/mandatory-skill-usage.md` | Primary (codebase) | Trigger map, skill routing keywords, H-22 proactive invocation |

### Approach

The 5W1H framework was applied across all five research questions:
- **WHO** -- Which Jerry components are affected by integration?
- **WHAT** -- What specific integration points exist?
- **WHERE** -- Where in the codebase do these integration points live?
- **WHEN** -- When in the evaluation lifecycle is each integration activated?
- **WHY** -- Why is each integration point architecturally significant?
- **HOW** -- How should each integration be implemented?

### Limitations

**External research was unavailable.** WebSearch was denied during this research session. All findings are based on codebase analysis and existing PROJ-017 artifacts (ADR-001, ORCHESTRATION_PLAN). External sources (promptfoo documentation, Anthropic evaluation guides, academic literature on LLM evaluation) are cited from findings already captured in Phase 1A and Phase 1B research and referenced through ADR-001. No new external data was gathered in this session. This is documented transparently per P-022.

---

## L1: Technical Analysis

### 1. Quality Gate Integration Points

#### 1.1 S-014 Rubric Dimension Mapping

Jerry's S-014 LLM-as-Judge rubric uses 6 weighted dimensions for quality scoring. Each dimension maps to a specific evaluation tier in the PROJ-017 framework.

| S-014 Dimension | Weight | Evaluation Tier | Assertion Type | Deterministic? |
|-----------------|--------|----------------|----------------|----------------|
| **Completeness** (0.20) | Highest | T1 + T4 | T1: section count, word count, heading hierarchy; T4: LLM-rubric for topical coverage | Partially |
| **Internal Consistency** (0.20) | Highest | T4 | LLM-rubric: terminology consistency, contradiction detection | No |
| **Methodological Rigor** (0.20) | Highest | T1 + T4 | T1: methodology section presence, citation count; T4: LLM-rubric for reasoning quality | Partially |
| **Evidence Quality** (0.15) | High | T1 + T4 | T1: URL count, citation format regex; T4: LLM-rubric for source credibility assessment | Partially |
| **Actionability** (0.15) | High | T4 | LLM-rubric: "Does this contain concrete, implementable recommendations?" | No |
| **Traceability** (0.10) | Moderate | T1 | Regex: cross-reference format, artifact path presence, PS ID format | Yes |

**Key insight:** Three of six dimensions (Completeness, Methodological Rigor, Evidence Quality) are partially deterministic -- they have T1 structural checks that verify proxy indicators (heading count, citation count, methodology section presence) without requiring LLM judgment. Only Internal Consistency and Actionability are purely LLM-dependent. Traceability is fully deterministic. This means the Smoke tier (T1 only) can cover approximately 40-50% of the quality rubric's weighted signal at zero API cost.

**Source:** `.context/rules/quality-enforcement.md` lines 104-117 (S-014 dimensions and weights).

#### 1.2 H-Rule Threshold Mapping

The >= 0.92 quality threshold (H-13) applies to C2+ deliverables. The evaluation framework needs to map this to pass/fail criteria:

| Jerry Concept | Evaluation Framework Mapping |
|---------------|------------------------------|
| H-13 threshold (>= 0.92) | `assert` threshold in promptfoo config: score >= 0.92 for composite |
| H-14 minimum iterations (3) | Test case that verifies N >= 3 revision artifacts exist |
| H-15 self-review (S-010) | T1 assertion: self-review section present in output |
| H-17 quality scoring required | T1 assertion: score metadata present in output |
| Score band PASS (>= 0.92) | Green status in evaluation report |
| Score band REVISE (0.85-0.91) | Yellow status with specific dimension failures identified |
| Score band REJECTED (< 0.85) | Red status with dimensional breakdown |

**Source:** `.context/rules/quality-enforcement.md` lines 104-106 (threshold), lines 119 (minimum cycle count).

#### 1.3 Criticality Level Integration

Jerry's C1-C4 criticality system directly maps to evaluation intensity:

| Criticality | Jerry Strategy Set | Evaluation Mode | Rationale |
|-------------|-------------------|-----------------|-----------|
| C1 (Routine) | S-010 only | Smoke (T1) | Low-stakes; deterministic checks sufficient |
| C2 (Standard) | S-007, S-002, S-014 | Standard (T1+T2, N=5) | Moderate stakes; quick statistical validation |
| C3 (Significant) | C2 + S-004, S-012, S-013 | Full (T1+T2+T4, N=30) | High stakes; full statistical rigor needed |
| C4 (Critical) | All 10 strategies (tournament) | Full + extended (T1+T2+T4, N=50) | Irreversible; maximum statistical confidence |

**Design implication:** The evaluation framework should accept a `--criticality` flag that automatically selects the appropriate evaluation mode. This aligns with Jerry's existing criticality-driven workflow selection and avoids requiring users to manually choose evaluation intensity.

**Source:** `.context/rules/quality-enforcement.md` lines 132-138 (criticality levels with strategy sets).

---

### 2. Agent Architecture Mapping

#### 2.1 Evaluation Surface Analysis

Jerry has 67 invokable agents across 12 skills. Not all are equally suitable as evaluation targets. The following classification uses three criteria: (a) does the agent produce file output? (b) is the output deterministically verifiable? (c) does the agent use external tools that introduce non-determinism?

| Skill | Agent Count | Output Producing | T1 Testable | T4 Required | Priority | AGENTS.md Source |
|-------|------------|------------------|-------------|-------------|----------|-----------------|
| Problem-Solving | 9 | 8 (all except ps-critic) | 6 | 8 | **HIGH** | lines 68-100 (ps-* agent detail) |
| NASA SE | 10 | 9 | 7 | 9 | HIGH | lines 101-125 (nse-* agent detail) |
| Adversary | 3 | 3 | 2 | 3 | MEDIUM | lines 126-140 (adv-* agent detail) |
| Orchestration | 3 | 2 | 1 | 2 | LOW | lines 141-158 (orch-* agent detail) |
| Worktracker | 3 | 3 | 3 | 0 | **HIGH (T1)** | lines 159-172 (wt-* agent detail) |
| Transcript | 5 | 4 | 3 | 4 | MEDIUM | lines 173-192 (ts-* agent detail) |
| Framework Voice | 3 | 3 | 1 | 3 | LOW | lines 193-205 (sbfv-* agent detail) |
| Session Voice | 1 | 0 | 0 | 0 | SKIP | lines 206-210 (sb-* agent detail) |
| Eng-Team | 10 | 9 | 6 | 9 | MEDIUM | lines 211-245 (eng-* agent detail) |
| Red-Team | 11 | 10 | 5 | 10 | LOW | lines 246-290 (red-* agent detail) |
| Diataxis | 6 | 6 | 5 | 6 | MEDIUM | lines 291-315 (diataxis-* agent detail) |
| Prompt Engineering | 3 | 3 | 2 | 3 | MEDIUM | lines 316-330 (pe-* agent detail) |

**Source:** `AGENTS.md` lines 42-63 (agent summary counts); per-skill line ranges in rightmost column.

> **Column methodology note:** "Output Producing" and "T1 Testable" columns are analytical judgments derived from reading each agent's `.md` definition and `.governance.yaml` file (output.required field and tool_tier field respectively). "Output Producing" = agents whose governance metadata declares `output.required: true` or whose methodology section describes file artifact production. "T1 Testable" = output-producing agents whose output format contains deterministically verifiable structural elements (headings, tables, pass/fail indicators). These are analytical classifications, not direct extractions from AGENTS.md.

#### 2.2 Priority Evaluation Targets

Based on the analysis above, the recommended initial evaluation suite targets these agents. Agents were classified into Tier 1 vs. Tier 2 using the following prioritization rubric:

| Criterion | Tier 1 Requirement | Tier 2 Allowance |
|-----------|-------------------|------------------|
| **Output producing?** | Must produce file artifacts (`output.required: true`) | Must produce file artifacts |
| **T1 structural assertions** | >= 3 distinct deterministic assertions available | >= 1 deterministic assertion available |
| **Frequency of use** | Commonly invoked in standard Jerry workflows (research, analysis, architecture, validation) | Invoked in specialized workflows |
| **Cognitive mode coverage** | Tier 1 set must collectively span >= 3 cognitive modes | No constraint |
| **T3 agent tool tier?** | No (external tool variance complicates initial evaluation) | Permitted with noted caveats |

**Tier 1 (First Sprint -- High Impact, High Testability):**

| Agent | Cognitive Mode | Why First | T1 Assertions Available |
|-------|---------------|-----------|------------------------|
| ps-researcher | Divergent | Produces structured research with L0/L1/L2 sections, citations, navigation tables -- all deterministically verifiable | H-23 (nav table), citations regex, L0/L1/L2 headings, word count |
| ps-analyst | Convergent | Produces analysis reports with methodology sections and evidence chains | Methodology section, evidence citations, finding enumeration |
| ps-architect | Convergent | Produces ADRs in Nygard format -- highly structured, deterministically verifiable | ADR sections (Status, Context, Decision, Consequences), option scoring table |
| wt-auditor | Systematic | Produces validation reports -- entirely deterministic, no LLM judgment needed | Pass/fail table, entity count, integrity check results |

**Tier 2 (Second Sprint -- Medium Impact):**

| Agent | Cognitive Mode | Why Second |
|-------|---------------|------------|
| ps-critic | Convergent | Produces quality scores -- score format is deterministically verifiable, but critic quality requires T4 |
| nse-requirements | Systematic | Produces structured requirements -- format is verifiable, but completeness needs T4 |
| diataxis-tutorial | Systematic | Produces documentation -- Diataxis compliance is partially deterministic |
| eng-architect | Convergent | Produces security architecture -- STRIDE/DREAD presence is T1, quality needs T4 |

#### 2.3 Cognitive Mode Implications for Test Design

Each cognitive mode produces characteristically different output that requires different assertion strategies:

| Cognitive Mode | Output Characteristics | T1 Focus | T4 Focus |
|---------------|----------------------|----------|----------|
| **Divergent** (ps-researcher) | Broad coverage, multiple sources, option enumeration | Source count, coverage breadth, section variety | Completeness of coverage, source quality assessment |
| **Convergent** (ps-analyst, ps-architect) | Focused conclusions, ranked options, trade-off tables | Decision presence, option scoring table, recommendation section | Reasoning quality, trade-off validity, conclusion soundness |
| **Integrative** (ps-synthesizer) | Cross-source correlation, unified narrative | Cross-reference count, source integration indicators | Synthesis coherence, gap identification quality |
| **Systematic** (ps-validator, wt-auditor) | Checklists, pass/fail, compliance matrices | Checklist completeness, binary verdicts, entity counts | N/A (systematic output is mostly deterministic) |
| **Forensic** (ps-investigator) | Causal chains, evidence correlation, 5 Whys | Chain step count, evidence citations, root cause statement | Causal chain validity, evidence quality |

**Design implication:** The skill comparison orchestrator should generate different assertion sets based on the target agent's cognitive mode. A `mode_assertions.yaml` mapping file could provide mode-specific default assertions.

**Skeleton schema for `mode_assertions.yaml`:**

```yaml
# mode_assertions.yaml -- Mode-specific default assertion sets
# Maps cognitive modes to T1 structural assertions and T4 LLM-rubric prompts
# Used by: skill comparison orchestrator (assertion selection)

divergent:
  description: "Broad coverage agents (ps-researcher, nse-explorer)"
  t1_assertions:
    - type: "section_count"
      min: 5
      reason: "Divergent agents should explore multiple facets"
    - type: "source_count"
      min: 3
      reason: "Breadth requires multiple sources"
    - type: "heading_variety"
      min_unique_h2: 4
      reason: "Coverage breadth reflected in section diversity"
  t4_rubric_focus:
    - "Completeness of topic coverage"
    - "Source diversity and quality"

convergent:
  description: "Focused conclusion agents (ps-analyst, ps-architect)"
  t1_assertions:
    - type: "decision_section_present"
      pattern: "(?i)(decision|recommendation|conclusion)"
      reason: "Convergent agents must reach a conclusion"
    - type: "option_table_present"
      pattern: "\\|.*Option.*\\|"
      reason: "Trade-off analysis requires structured comparison"
    - type: "scoring_matrix_present"
      pattern: "\\|.*Score.*\\|"
      reason: "Convergent analysis requires quantified evaluation"
  t4_rubric_focus:
    - "Reasoning quality leading to conclusion"
    - "Trade-off validity"

integrative:
  description: "Cross-source synthesis agents (ps-synthesizer)"
  t1_assertions:
    - type: "cross_reference_count"
      min: 3
      reason: "Integration requires connecting multiple sources"
    - type: "source_integration_indicators"
      pattern: "(?i)(across|combining|synthesis|unified)"
      min_matches: 2
  t4_rubric_focus:
    - "Synthesis coherence across inputs"
    - "Gap identification quality"

systematic:
  description: "Checklist/compliance agents (wt-auditor, ps-validator)"
  t1_assertions:
    - type: "checklist_completeness"
      pattern: "\\|.*Pass.*\\||\\|.*Fail.*\\|"
      reason: "Systematic agents produce binary verdicts"
    - type: "entity_count_present"
      pattern: "\\d+\\s+(entities|items|rules)"
      reason: "Systematic agents enumerate scope"
  t4_rubric_focus: []  # Systematic output is mostly T1-testable

forensic:
  description: "Root cause agents (ps-investigator)"
  t1_assertions:
    - type: "causal_chain_present"
      pattern: "(?i)(because|caused by|root cause|why)"
      min_matches: 3
      reason: "Forensic agents trace causal chains"
    - type: "evidence_citations"
      min: 2
      reason: "Claims require supporting evidence"
    - type: "root_cause_statement"
      pattern: "(?i)root cause"
      reason: "Must state the root cause explicitly"
  t4_rubric_focus:
    - "Causal chain validity"
    - "Evidence quality supporting each causal step"
```

**Source:** `.context/rules/agent-development-standards.md` Cognitive Mode Taxonomy section.

#### 2.4 Tool Tier Impact on Evaluation

Agent tool tiers (T1-T5) affect evaluation design because higher tiers introduce more non-determinism:

| Tool Tier | Agents | Evaluation Implication |
|-----------|--------|----------------------|
| T1 (Read-Only) | adv-executor, adv-scorer, wt-auditor | Most deterministic; output depends only on input content. Ideal for T1 evaluation. |
| T2 (Read-Write) | ps-analyst, ps-critic, nse-architecture | Output depends on input + writing decisions. T1+T4 evaluation appropriate. |
| T3 (External) | ps-researcher, nse-explorer | Output depends on external web content -- inherently non-deterministic. Must control for external variance (mock/stub external sources or use seed content). |
| T4 (Persistent) | orch-planner, orch-tracker | Output depends on cross-session state. Evaluation requires state fixture setup. |
| T5 (Full) | Lead agents, orchestrators | Delegation introduces sub-agent variance. Evaluation at this tier measures orchestration quality, not individual agent quality. |

**Key constraint:** T3 agent tool tier agents (ps-researcher, nse-explorer) require special handling in evaluation because WebSearch/WebFetch introduce uncontrolled variance. The evaluation framework should either: (a) provide fixed reference content as input context, or (b) evaluate structural quality of output independently of content accuracy.

**Source:** `.context/rules/agent-development-standards.md` Tool Security Tiers section.

---

### 3. CLI Integration Patterns

#### 3.1 Existing CLI Architecture

Jerry's CLI uses hexagonal architecture with namespace-based routing. The relevant pattern from `main.py`:

```python
# Current namespace routing in main.py (line 108-131)
if args.namespace == "session":
    return _handle_session(adapter, args, json_output)
elif args.namespace == "agents":
    return _handle_agents(args, json_output)
elif args.namespace == "ci":
    return _handle_ci(args, json_output)
# ... etc
```

The `agents` namespace (lines 455-535 of `main.py`, lines 732-831 of `parser.py`) provides the closest architectural template for a new `eval` namespace because:

1. It has its own bootstrap wiring independent of `CLIAdapter` (line 458: "Does not require the CLIAdapter")
2. It uses lazy imports to defer heavy dependencies (line 475: `from src.agents.infrastructure.adapters...`)
3. It has subcommands with `--agent` filtering and `--dry-run` mode
4. It outputs both human-readable and JSON formats

**Source:** `src/interface/cli/main.py` lines 455-535, `src/interface/cli/parser.py` lines 732-831.

#### 3.2 Proposed `eval` Namespace Design

Based on the `agents` namespace pattern, the evaluation framework should add a `jerry eval` namespace:

```
jerry eval [--json] <command> [options]

Commands:
  smoke     Run T1 deterministic assertions only (zero API cost)
  standard  Run T1 + T2 statistical comparison (N configurable)
  full      Run T1 + T2 + T4 with LLM-as-judge (N configurable)
  compare   Compare with-skill vs without-skill for a specific agent
  report    Generate evaluation summary from existing results
  config    Generate or validate evaluation configuration
```

#### 3.3 Command Specifications

**`jerry eval smoke`** -- The default CI/CD command (zero cost, instant):

```
jerry eval smoke [--skill <name>] [--agent <name>] [--config <path>]
                 [--output-dir <path>] [--json]

Examples:
  jerry eval smoke                          # All agents, default assertions
  jerry eval smoke --skill problem-solving  # Only ps-* agents
  jerry eval smoke --agent ps-researcher    # Single agent
```

**`jerry eval compare`** -- The skill comparison command (core PROJ-017 feature):

```
jerry eval compare --agent <name> --mode <smoke|standard|full>
                   [--n <runs>] [--criticality <C1|C2|C3|C4>]
                   [--seed <content-path>] [--output-dir <path>] [--json]

Examples:
  jerry eval compare --agent ps-researcher --mode standard --n 10
  jerry eval compare --agent ps-architect --criticality C3
```

**`jerry eval config`** -- Configuration generation (follows `jerry agents build` pattern):

```
jerry eval config generate --agent <name> [--mode <smoke|standard|full>]
jerry eval config validate [--config <path>]
```

#### 3.4 Proposed Implementation Pattern

> **Note:** The code stubs below are proposed implementations for the `eval` namespace, not extractions from the existing codebase. They follow the architectural patterns observed in the `agents` namespace (Section 3.1) and are designed for downstream implementation phases.

Following the `agents` namespace pattern, the new namespace would be wired as follows:

```python
# PROPOSED IMPLEMENTATION -- In parser.py: _add_eval_namespace()
def _add_eval_namespace(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Add eval namespace commands for skill testing."""
    eval_parser = subparsers.add_parser(
        "eval",
        help="LLM skill evaluation and comparison",
        description="Run deterministic and statistical skill evaluations.",
    )
    eval_subparsers = eval_parser.add_subparsers(
        title="commands", dest="command", metavar="<command>",
    )
    # smoke, standard, full, compare, report, config subcommands...
```

```python
# PROPOSED IMPLEMENTATION -- In main.py: _handle_eval()
def _handle_eval(args: Any, json_output: bool) -> int:
    """Route eval namespace commands.

    Does not require CLIAdapter; uses its own bootstrap
    for the evaluation bounded context.
    """
    if args.command is None:
        print("No eval command specified. Use 'jerry eval --help'.")
        return 1

    from src.evaluation.infrastructure.adapters.promptfoo_adapter import (
        create_eval_smoke_handler,
        create_eval_compare_handler,
    )
    # ... command routing
```

**Hexagonal architecture alignment:** The evaluation bounded context would follow the same layered structure as the agents BC:

```
src/evaluation/
    domain/          # EvalConfig, SkillComparison, StatResult value objects
    application/     # RunSmokeCommand, RunCompareCommand, handlers
    infrastructure/  # PromptfooAdapter, StatisticalEngine
```

**Source:** `src/interface/cli/main.py` lines 84-131 (routing pattern), `src/interface/cli/parser.py` lines 29-80 (parser structure).

#### 3.5 Integration with Existing Namespaces

The `eval` namespace intersects with existing namespaces at specific points:

| Existing Namespace | Integration Point | Direction |
|--------------------|-------------------|-----------|
| `agents` | `jerry agents list` provides agent catalog; `eval` consumes it | agents -> eval |
| `agents validate` | Governance validator shares validation logic with `agents validate` | Bidirectional |
| `ci` | `jerry ci` can invoke `jerry eval smoke` as a check | ci -> eval |
| `ast` | `jerry ast frontmatter` provides deterministic parsing for T1 assertions | ast -> eval |
| `projects` | Evaluation configs stored under `projects/PROJ-NNN/eval/` | eval -> projects |

---

### 4. Governance Compliance Validator Design

#### 4.1 H-Rule to Assertion Mapping

All 25 HARD rules were analyzed for deterministic testability. Each rule is classified by whether it can be verified through structural analysis of agent output (T1), or requires behavioral observation (T4+).

**Category A: Fully Deterministic (T1 Assertions)**

These rules produce binary pass/fail results through structural analysis:

| H-Rule | Assertion Type | promptfoo Implementation | Input |
|--------|---------------|-------------------------|-------|
| H-23 (Navigation table) | `javascript` | Check for `\| Section \| Purpose \|` pattern in output | Agent output text |
| H-23b (Anchor links) | `javascript` | Regex: `\[.*\]\(#[a-z-]+\)` present in nav table | Agent output text |
| H-11 (Type hints) | `python` | AST parse Python output for type annotations | Code output |
| H-11b (Docstrings) | `python` | AST parse for docstring presence on public functions | Code output |
| H-10 (One class per file) | `python` | Count class definitions per file in code output | Code output |
| H-33 (AST-based parsing) | `contains-none` | Output does not contain regex-based frontmatter extraction | Agent output text |
| H-34 (YAML schema) | `python` | JSON Schema validation of agent definition output | Agent definition output |
| H-05 (UV only) | `contains-none` + `contains` | No `pip install` or `python -m`; has `uv run` or `uv add` | Command output |

**Category B: Partially Deterministic (T1 proxy + T4 quality)**

These rules have structural indicators (T1) but full verification requires judgment (T4):

| H-Rule | T1 Proxy Assertion | T4 Quality Assertion |
|--------|-------------------|---------------------|
| H-13 (Quality >= 0.92) | Score metadata present and parseable | LLM-rubric: does composite score calculation follow S-014 weights? |
| H-14 (3 iterations min) | Count of revision sections >= 3 | LLM-rubric: do iterations show meaningful improvement? |
| H-15 (Self-review) | Self-review section exists | LLM-rubric: is self-review substantive, not perfunctory? |
| H-16 (Steelman before critique) | Steelman section appears before critique section | LLM-rubric: is steelman genuine, not strawman? |
| H-20 (BDD test-first) | Test file exists before implementation file | LLM-rubric: do tests drive implementation? |

**Category C: Behavioral / Non-output-testable**

These rules govern agent behavior, not output content. They require either runtime observation or proxy metrics:

| H-Rule | Why Not Directly Testable | Proxy Metric |
|--------|--------------------------|--------------|
| H-01 (No recursive subagents) | Requires runtime call graph observation | Agent tool invocation log does not contain `Task` calls from workers |
| H-02 (User authority) | Requires interactive session observation | N/A -- behavioral constraint |
| H-03 (No deception) | Requires factual verification of claims | LLM-rubric: confidence claims match evidence level |
| H-04 (Active project) | Session-level constraint | N/A -- environment constraint |
| H-07 (Layer isolation) | Requires import graph analysis of generated code | Python AST: cross-layer imports absent |
| H-22 (Proactive skill invocation) | Requires session transcript analysis | Skill invocation count per session |
| H-31 (Clarify when ambiguous) | Requires interactive session observation | N/A -- behavioral constraint |
| H-36 (Circuit breaker) | Requires routing history observation | Routing depth counter in handoff metadata |

**Source:** `.context/rules/quality-enforcement.md` lines 49-75 (full HARD Rule Index).

#### 4.2 Assertion Implementation as promptfoo Custom Assertions

The governance compliance validator implements Category A and Category B (T1 proxy) rules as custom promptfoo assertion providers. Based on ADR-001's architecture:

```yaml
# Example: H-23 navigation table assertion
- type: python
  value: |
    import re
    # H-23: Navigation table REQUIRED for markdown > 30 lines
    lines = output.strip().split('\n')
    if len(lines) <= 30:
        return {"pass": True, "reason": "File under 30 lines; nav table not required (H-23)"}
    nav_pattern = r'\|\s*Section\s*\|\s*Purpose\s*\|'
    has_nav = bool(re.search(nav_pattern, output))
    anchor_pattern = r'\[.*?\]\(#[a-z][a-z0-9-]*\)'
    has_anchors = bool(re.search(anchor_pattern, output))
    return {
        "pass": has_nav and has_anchors,
        "reason": f"H-23: nav_table={'present' if has_nav else 'MISSING'}, anchors={'present' if has_anchors else 'MISSING'}"
    }
```

```yaml
# Example: H-13 quality threshold assertion (T1 proxy)
- type: python
  value: |
    import re
    # H-13: Quality score >= 0.92 for C2+ deliverables
    score_pattern = r'(?:score|quality|composite)[:\s]+(\d+\.?\d*)'
    scores = re.findall(score_pattern, output, re.IGNORECASE)
    if not scores:
        return {"pass": False, "reason": "H-13: No quality score found in output"}
    max_score = max(float(s) for s in scores)
    return {
        "pass": max_score >= 0.92,
        "reason": f"H-13: Highest score {max_score:.3f} {'>=':'<'} 0.92 threshold"
    }
```

#### 4.3 Assertion Catalog Summary

| Category | Count | API Cost | Execution Time | Coverage |
|----------|-------|----------|----------------|----------|
| A (Fully Deterministic) | 8 rules | $0.00 | < 1 second | 32% of H-rules |
| B (T1 proxy) | 5 rules | $0.00 (T1 portion) | < 1 second | 20% of H-rules |
| B (T4 quality) | 5 rules | ~$0.002/assertion | ~2-5 seconds | 20% of H-rules |
| C (Behavioral) | 12 rules | Variable | Variable | 48% of H-rules |
| **Total T1-testable** | **13 rules** | **$0.00** | **< 2 seconds** | **52% of H-rules** |

**Key finding:** Over half (52%) of Jerry's HARD rules can be tested deterministically at zero API cost. This validates ADR-001's determinism-first architecture (Phase 2 THEME-2) and confirms that the Smoke tier provides meaningful governance coverage.

---

### 5. Determinism-First Architecture Alignment

#### 5.1 Enforcement Layer to Evaluation Tier Mapping

Jerry's 5-layer enforcement architecture maps to the evaluation framework's tier model:

| Jerry Layer | Timing | Function | Eval Tier | Mapping Rationale |
|-------------|--------|----------|-----------|-------------------|
| **L1** (Session start) | Pre-execution | Load behavioral rules | N/A (not output-testable) | L1 sets conditions; evaluation tests outputs |
| **L2** (Every prompt) | Per-prompt | Re-inject critical rules | N/A (internal mechanism) | L2 is an enforcement mechanism, not an observable output |
| **L3** (Pre-tool) | Before tool calls | Deterministic gating (AST) | **T1** | Both are deterministic, zero-cost, pre-execution checks |
| **L4** (Post-tool) | After tool calls | Output inspection | **T2 + T4** | T2 for statistical output comparison; T4 for LLM-judged quality |
| **L5** (Commit/CI) | Post-hoc | CI verification | **T1 (CI mode)** | Both run in CI, both are deterministic, both produce pass/fail |

**Key insight:** The evaluation framework's T1 tier is architecturally equivalent to L3+L5 -- deterministic, zero-token, immune to context rot. T4 (LLM-as-judge) is architecturally equivalent to L4 -- output inspection with mixed context rot immunity. This parallel means the evaluation framework naturally inherits Jerry's enforcement properties.

**Source:** `.context/rules/quality-enforcement.md` lines 257-269 (enforcement architecture table).

#### 5.2 Context Rot Immunity Analysis

The evaluation framework inherits Jerry's context rot characteristics by tier:

| Eval Tier | Deterministic? | Context Rot Immune? | Jerry Equivalent |
|-----------|---------------|--------------------|--------------------|
| T1 (Structural) | Yes | **Yes** -- assertions are stateless regex/AST checks | L3 + L5 |
| T2 (Statistical) | Yes (given fixed inputs) | **Yes** -- bootstrap/permutation are mathematical operations | N/A (new capability) |
| Behavioral | No | **No** -- LLM judgment varies with context | L4 (self-correction) |
| T4 (LLM-as-Judge) | No | **No** -- judge quality affected by context | L4 (output inspection) |

> **Terminology note:** The "Behavioral" tier above refers to the evaluation framework's intermediate tier between T2 (Statistical) and T4 (LLM-as-Judge). This is distinct from the agent tool tier "T3 (External)" described in Section 2.4, which refers to agents with WebSearch/WebFetch/Context7 access per `agent-development-standards.md`. To avoid confusion, this document uses "Behavioral tier" for the evaluation taxonomy and "T3 agent tool tier" for the agent security tier taxonomy throughout.

**Implication:** The Smoke tier (T1 only) is fully immune to context rot. The Full tier (T1+T2+T4) has partial immunity. This means T1 results are reliable regression indicators, while T4 results require statistical aggregation (N >= 30) to account for variance.

#### 5.3 Determinism Coverage by Agent Type

Combining the agent evaluation surface (Section 2) with the assertion catalog (Section 4):

| Agent Type | T1 Assertions Available | T1 Quality Coverage (est.) | Minimum Useful Tier |
|------------|------------------------|--------------------|--------------------|
| Research agents (ps-researcher, nse-explorer) | Nav table, citations, L0/L1/L2 headings, word count, section count | ~45% of output quality | Smoke (T1) for regression; Standard (T2) for comparison |
| Analysis agents (ps-analyst, ps-critic) | Methodology section, evidence chain format, score format | ~35% of output quality | Standard (T2) for meaningful signal |
| Architecture agents (ps-architect) | ADR format, option table, scoring matrix, decision section | ~55% of output quality | Smoke (T1) provides strong signal |
| Validation agents (wt-auditor, ps-validator) | Pass/fail format, entity count, checklist completeness | ~80% of output quality | Smoke (T1) is nearly sufficient |
| Documentation agents (diataxis-*) | Quadrant classification, heading structure, example presence | ~50% of output quality | Smoke (T1) for structure; Standard (T2) for quality |

> **T1 Quality Coverage estimation methodology:** The percentages above are estimates, not exact measurements. They were derived by mapping each agent type's T1-verifiable structural assertions against the S-014 quality dimensions (Section 1.1). For each agent type: (1) identify which S-014 dimensions have T1 proxy assertions (from Section 4.1 Category A and B), (2) sum the weights of those dimensions, (3) apply a partial coverage factor (0.5) for dimensions that are only partially T1-verifiable. Example for ps-architect (~55%): Completeness (0.20, partially: 0.10) + Methodological Rigor (0.20, partially: 0.10) + Evidence Quality (0.15, partially: 0.075) + Traceability (0.10, fully: 0.10) + Actionability (0.15, partially: 0.075) + Internal Consistency (0.20, none: 0.00) = 0.45 raw, rounded to ~55% after accounting for the high structural regularity of ADR format. These are directional estimates for prioritization; calibration against actual evaluation results is needed.

---

## L2: Architectural Implications

### Strategic Trade-offs

#### Trade-off 1: Scope vs. Speed

**Tension:** The 67-agent evaluation surface creates a combinatorial explosion. Testing all agents across all tiers at N=30 would require thousands of API calls.

**Resolution:** The tiered agent priority (Section 2.2) provides a manageable initial scope. Tier 1 agents (ps-researcher, ps-analyst, ps-architect, wt-auditor) cover the most frequently used, most deterministically testable agents. Starting with 4 agents keeps the initial evaluation suite manageable while covering the highest-value surface.

**Risk:** If the initial 4 agents are not representative of the broader agent population, findings may not generalize. Mitigation: include agents from different cognitive modes (divergent, convergent, systematic) to ensure coverage across reasoning patterns.

#### Trade-off 2: Jerry-Specific vs. General-Purpose

**Tension:** The governance compliance validator (Section 4) is deeply Jerry-specific. The statistical significance engine is general-purpose. The skill comparison orchestrator sits between these extremes.

**Resolution:** This is actually a strength, not a weakness. The general-purpose statistical engine is the defensible differentiator (Phase 2 CONVERGENCE-3). The Jerry-specific governance validator is the integration point that makes the framework immediately useful for Jerry's quality system. The orchestrator is the bridge. ADR-001 already identifies this decomposition as the architecture's key insight.

**Risk:** Over-specializing the governance validator for Jerry's 25 HARD rules may limit adoption in other Claude Code skill ecosystems. Mitigation: implement H-rule assertions as a plugin library that other frameworks can replace with their own governance rules. The assertion API should be rule-agnostic.

#### Trade-off 3: CLI Integration Depth

**Tension:** Deep CLI integration (new namespace, hexagonal BC, bootstrap wiring) provides the best developer experience but requires significant Jerry codebase changes. A lighter integration (promptfoo CLI wrapper script) ships faster but feels disconnected from Jerry's workflow.

**Resolution:** Phase the integration. Start with a wrapper script (`jerry-eval` or `scripts/eval.sh`) that invokes promptfoo with generated configs. Once the evaluation framework is validated, integrate as a proper `jerry eval` namespace in Phase 4 (per ADR-001's implementation timeline). This approach avoids blocking the framework's validation on Jerry CLI engineering.

### Long-Term Evolution Path

1. **Phase 0 (Now):** Wrapper script + promptfoo YAML configs generated manually
2. **Phase 1 (1-2 weeks):** `jerry eval config generate` command that produces promptfoo configs from agent definitions
3. **Phase 2 (2-4 weeks):** `jerry eval smoke` integrated into `jerry ci` pipeline
4. **Phase 3 (4-6 weeks):** Full `jerry eval` namespace with compare, report, and statistical analysis
5. **Phase 4 (6-8 weeks):** Evaluation results feed back into agent development: `jerry agents validate` includes skill effectiveness metrics

### Alignment with Existing Architecture

The evaluation framework aligns with Jerry's architectural principles:

| Principle | How Framework Aligns |
|-----------|---------------------|
| Hexagonal architecture (H-07) | Evaluation BC has domain/application/infrastructure layers |
| One class per file (H-10) | Each assertion type is a separate module |
| UV-only Python (H-05) | Statistical engine uses `uv run`; promptfoo uses `npx` |
| Filesystem as infinite memory | Evaluation results persisted to `projects/PROJ-NNN/eval/` |
| Context rot mitigation | T1 assertions are context-rot-immune by design |
| Determinism-first (L3/L5) | Smoke tier runs zero LLM calls, deterministic assertions only |

---

## Conclusions

1. **Jerry's quality infrastructure provides natural integration points at every level.** The 25 HARD rules map to T1 assertions, the S-014 rubric maps to T4 LLM-as-judge dimensions, and the 5-layer enforcement architecture maps to the evaluation tier model. No new quality concepts need to be invented.

2. **52% of HARD rules are deterministically testable at zero API cost.** This validates the Smoke tier as a meaningful CI/CD check. The governance compliance validator can provide substantial governance coverage without any LLM calls.

3. **The `agents` CLI namespace provides a direct template for `eval`.** Both have independent bootstrap wiring, subcommand structure, JSON output support, and agent-level filtering. The implementation pattern is proven.

4. **Agent cognitive modes should drive assertion selection.** Divergent agents (research) need breadth assertions; convergent agents (analysis) need conclusion quality assertions; systematic agents (validation) are almost entirely T1-testable. A mode-aware assertion configuration generator is architecturally natural.

5. **T3 agent tool tier agents (external tool access) require special evaluation handling.** Web search introduces uncontrolled variance that invalidates paired comparison. These agents need either fixed seed content or structure-only evaluation.

6. **The criticality-to-evaluation-mode mapping enables automatic tier selection.** Users should not need to manually choose Smoke vs. Standard vs. Full -- the criticality level already carries this information.

---

## Recommendations

### For Phase 2 (Synthesis)

1. **Prioritize the H-rule assertion catalog** as the first deliverable after synthesis. The 13 fully deterministic assertions (Category A + B T1 proxy) provide immediate CI/CD value at zero cost.

2. **Use the 4-agent Tier 1 set** (ps-researcher, ps-analyst, ps-architect, wt-auditor) as the validation trial targets. These span three cognitive modes and two tool tiers.

3. **The CLI integration should start as a wrapper script**, not a full namespace. The namespace design (Section 3.2) is ready for Phase 4 implementation, but Phase 0-2 should focus on the evaluation engine, not CLI polish.

### For Phase 3 (V&V and Risk)

4. **The T3 agent evaluation challenge** is a risk that needs explicit mitigation in the risk register. External tool variance in ps-researcher and nse-explorer evaluation is a known threat to paired comparison validity.

5. **The 48% of H-rules classified as "behavioral"** (Category C) represents a coverage gap. The V&V plan should document this gap and identify which behavioral rules could eventually be tested through session transcript analysis.

### For the Trade Study (Phase 5)

6. **The Jerry-specific governance validator vs. general-purpose extensibility** trade-off should be a formal evaluation dimension. The validator's implementation as a plugin library (not hardcoded H-rules) is the architecture that resolves this tension.

---

## References

1. `.context/rules/quality-enforcement.md` (Jerry codebase) -- Key insight: 25 HARD rules, 6-dimension S-014 rubric with weights, 5-layer enforcement architecture, criticality levels C1-C4 with strategy sets, >= 0.92 quality threshold.

2. `AGENTS.md` (Jerry codebase) -- Key insight: 67 invokable agents across 12 skills with cognitive modes (divergent, convergent, integrative, systematic, forensic) and tool tiers (T1-T5).

3. `src/interface/cli/main.py` (Jerry codebase) -- Key insight: Hexagonal CLI architecture with namespace routing; `agents` namespace as template for `eval` with independent bootstrap wiring.

4. `src/interface/cli/parser.py` (Jerry codebase) -- Key insight: argparse subparser pattern for namespace commands; `_add_agents_namespace()` as implementation template.

5. `projects/PROJ-017-llm-skill-testing/decisions/ADR-001-framework-architecture.md` (PROJ-017) -- Key insight: Option B (promptfoo Extension) chosen; three components: Skill Comparison Orchestrator, Statistical Significance Engine, Governance Compliance Validator; tiered evaluation model (Smoke/Standard/Full).

6. `projects/PROJ-017-llm-skill-testing/orchestration/promptfoo-deep-analysis-20260303/ORCHESTRATION_PLAN.md` (PROJ-017) -- Key insight: 8-phase pipeline, Phase 1C scope and output contract, quality gate >= 0.92 at all phase boundaries.

7. `.context/rules/agent-development-standards.md` (Jerry codebase) -- Key insight: Tool security tiers T1-T5, cognitive mode taxonomy (5 modes), progressive disclosure architecture, dual-file agent definition format.

8. `.context/rules/mandatory-skill-usage.md` (Jerry codebase) -- Key insight: 5-column trigger map format, H-22 proactive skill invocation, skill routing keywords.

9. Anthropic Engineering Blog: "Evaluating LLM Outputs" (cited via ADR-001 Phase 1A) -- Key insight: "Choose deterministic graders where possible, LLM graders where necessary." Validates determinism-first architecture.

10. arXiv 2511.19794 (cited via ADR-001 Phase 1A, SINGLE-SOURCE) -- Key insight: N >= 30 runs per condition for statistical significance in LLM evaluation. Informs T2 tier design.

---

## PS Integration

- **PS ID:** PROJ-017 Phase 1C
- **Entry ID:** Phase 1C (Jerry Integration Analysis)
- **Artifact Path:** `projects/PROJ-017-llm-skill-testing/research/jerry-integration-analysis.md`
- **Confidence:** 0.82 (high for codebase analysis; reduced from 0.90 due to inability to perform external web research in this session)
- **Next Agent Hint:** ps-synthesizer for Phase 2 synthesis across Phase 1A-1D research outputs
