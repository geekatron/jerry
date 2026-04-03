# AGENTS.md - Registry of Available Specialists

> This file documents the sub-agent personas available for task delegation.
> Each agent has specialized capabilities and context isolation.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Agent Philosophy](#agent-philosophy) | Core principles of agent-based work |
| [Agent Summary](#agent-summary) | Quick count by skill |
| [Problem-Solving Skill Agents](#problem-solving-skill-agents) | ps-* agents (9 total) |
| [NASA SE Skill Agents](#nasa-se-skill-agents) | nse-* agents (10 total) |
| [Orchestration Skill Agents](#orchestration-skill-agents) | orch-* agents (3 total) |
| [Adversary Skill Agents](#adversary-skill-agents) | adv-* agents (3 total) |
| [Worktracker Skill Agents](#worktracker-skill-agents) | wt-* agents (3 total) |
| [Transcript Skill Agents](#transcript-skill-agents) | ts-* agents (5 total) |
| [Framework Voice Skill Agents](#framework-voice-skill-agents) | sb-* agents (3 total) |
| [Session Voice Skill Agents](#session-voice-skill-agents) | sb-voice agent (1 total) |
| [Eng-Team Skill Agents](#eng-team-skill-agents) | eng-* agents (10 total) |
| [Red-Team Skill Agents](#red-team-skill-agents) | red-* agents (11 total) |
| [PM/PMM Skill Agents](#pmpmm-skill-agents) | pm-* agents (5 total) |
| [Prompt Engineering Skill Agents](#prompt-engineering-skill-agents) | pe-* agents (3 total) |
| [Diataxis Skill Agents](#diataxis-skill-agents) | diataxis-* agents (6 total) |
| [User-Experience Skill Agents](#user-experience-skill-agents) | ux-* agents (11 total) |
| [Use Case Skill Agents](#use-case-skill-agents) | uc-* agents (2 total) |
| [Test Spec Skill Agents](#test-spec-skill-agents) | tspec-* agents (2 total) |
| [Contract Design Skill Agents](#contract-design-skill-agents) | cd-* agents (2 total) |
| [MCP Tool Access](#mcp-tool-access) | Context7 and Memory-Keeper agent matrix |
| [Agent Handoff Protocol](#agent-handoff-protocol) | Multi-agent coordination |
| [Adding New Agents](#adding-new-agents) | Extension guide |

---

## Agent Philosophy

Jerry uses a **skill-based agent pattern** where specialized agents are scoped
to specific skills. This provides:

1. **Context Isolation** - Each agent has focused context
2. **Expertise Depth** - Specialists know their domain deeply
3. **Parallel Execution** - Multiple agents can work concurrently
4. **Quality Gates** - Handoffs enforce review checkpoints

---

## Agent Summary

| Category | Count | Scope |
|----------|-------|-------|
| Problem-Solving Agents | 9 | `/problem-solving` skill |
| NASA SE Agents | 10 | `/nasa-se` skill |
| Orchestration Agents | 3 | `/orchestration` skill |
| Adversary Agents | 3 | `/adversary` skill |
| Worktracker Agents | 3 | `/worktracker` skill |
| Transcript Agents | 5 | `/transcript` skill |
| Framework Voice Agents | 3 | `/saucer-boy-framework-voice` skill |
| Session Voice Agents | 1 | `/saucer-boy` skill |
| Eng-Team Agents | 10 | `/eng-team` skill |
| Red-Team Agents | 11 | `/red-team` skill |
| PM/PMM Agents | 5 | `/pm-pmm` skill |
| Diataxis Agents | 6 | `/diataxis` skill |
| Prompt Engineering Agents | 3 | `/prompt-engineering` skill |
| User-Experience Agents | 11 | `/user-experience` skill |
| Use Case Agents | 2 | `/use-case` skill |
| Test Spec Agents | 2 | `/test-spec` skill |
| Contract Design Agents | 2 | `/contract-design` skill |
| **Total** | **89** | |

> **Verification:** Agent counts verified against filesystem scan (`skills/*/agents/*.md`).
> 82 total files found; 4 template/extension files excluded from counts:
> `NSE_AGENT_TEMPLATE.md`, `NSE_EXTENSION.md`, `PS_AGENT_TEMPLATE.md`, `PS_EXTENSION.md`.
> Per-skill sum: 9 + 10 + 3 + 3 + 3 + 5 + 3 + 1 + 10 + 11 + 5 + 6 + 3 + 11 + 2 + 2 + 2 = 89 invokable agents.
> Last verified: 2026-03-09.

---

## Problem-Solving Skill Agents

These agents are scoped to the `problem-solving` skill and invoked via `/problem-solving`.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| ps-researcher | `skills/problem-solving/agents/ps-researcher.md` | Research Specialist | Divergent |
| ps-analyst | `skills/problem-solving/agents/ps-analyst.md` | Analysis Specialist | Convergent |
| ps-synthesizer | `skills/problem-solving/agents/ps-synthesizer.md` | Synthesis Specialist | Integrative |
| ps-validator | `skills/problem-solving/agents/ps-validator.md` | Validation Specialist | Systematic |
| ps-architect | `skills/problem-solving/agents/ps-architect.md` | Architecture Specialist | Strategic |
| ps-reviewer | `skills/problem-solving/agents/ps-reviewer.md` | Review Specialist | Critical |
| ps-critic | `skills/problem-solving/agents/ps-critic.md` | Quality Evaluator | Convergent |
| ps-investigator | `skills/problem-solving/agents/ps-investigator.md` | Investigation Specialist | Forensic |
| ps-reporter | `skills/problem-solving/agents/ps-reporter.md` | Reporting Specialist | Communicative |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| ps-researcher | Literature review, web research, source validation | Research findings |
| ps-analyst | Root cause analysis, trade-offs, gap analysis, risk | Analysis reports |
| ps-synthesizer | Pattern synthesis across multiple research outputs | Synthesis documents |
| ps-validator | Constraint verification, design validation | Validation reports |
| ps-architect | Architecture decisions, ADR production | Design documents, ADRs |
| ps-reviewer | Code review, design review, security review | Review reports |
| ps-critic | Quality evaluation for creator-critic-revision cycles | Critique reports with scores |
| ps-investigator | Failure analysis, debugging, 5 Whys | Investigation reports |
| ps-reporter | Status reports, phase progress, summaries | Status documents |

**Invocation**: Use `/problem-solving` skill which orchestrates these agents.

**Artifact Location**: `{project}/research/`, `{project}/analysis/`, `{project}/synthesis/`, `{project}/critiques/`

---

## NASA SE Skill Agents

These agents implement NASA Systems Engineering processes per NPR 7123.1D.

| Agent | File | Role | NASA Process |
|-------|------|------|--------------|
| nse-requirements | `skills/nasa-se/agents/nse-requirements.md` | Requirements Engineer | Processes 1, 2, 11 |
| nse-verification | `skills/nasa-se/agents/nse-verification.md` | V&V Specialist | Processes 7, 8 |
| nse-risk | `skills/nasa-se/agents/nse-risk.md` | Risk Manager | Process 13 |
| nse-architecture | `skills/nasa-se/agents/nse-architecture.md` | System Architect | Processes 3, 4 |
| nse-integration | `skills/nasa-se/agents/nse-integration.md` | Integration Engineer | Process 9 |
| nse-configuration | `skills/nasa-se/agents/nse-configuration.md` | CM Specialist | Process 10 |
| nse-qa | `skills/nasa-se/agents/nse-qa.md` | Quality Assurance | Process 12 |
| nse-reviewer | `skills/nasa-se/agents/nse-reviewer.md` | Review Coordinator | All reviews (SRR/PDR/CDR/TRR/FRR) |
| nse-reporter | `skills/nasa-se/agents/nse-reporter.md` | Status Reporter | Reporting and metrics |
| nse-explorer | `skills/nasa-se/agents/nse-explorer.md` | Domain Explorer | Research and discovery |

**Key Capabilities:**

| Agent | Primary Deliverable | Output Location |
|-------|---------------------|-----------------|
| nse-requirements | Requirements specs, VCRM | `{project}/requirements/` |
| nse-verification | VCRM, test procedures, validation plans | `{project}/verification/` |
| nse-risk | Risk registers, assessments | `{project}/risks/` |
| nse-architecture | Architecture docs, interface specs | `{project}/architecture/` |
| nse-integration | Integration plans, test results | `{project}/integration/` |
| nse-configuration | Baselines, change control | `{project}/configuration/` |
| nse-qa | Quality plans, audits | `{project}/quality/` |
| nse-reviewer | Review packages, findings | `{project}/reviews/` |
| nse-reporter | Status reports, metrics | `{project}/reports/` |
| nse-explorer | Domain research, trade studies | `{project}/research/` |

**Invocation**: Use `/nasa-se` skill which orchestrates these agents.

**All outputs include mandatory NASA disclaimer** per P-043.

---

## Orchestration Skill Agents

These agents manage multi-agent workflow orchestration and state tracking.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| orch-planner | `skills/orchestration/agents/orch-planner.md` | Orchestration Planner | Convergent |
| orch-tracker | `skills/orchestration/agents/orch-tracker.md` | State Tracker | Convergent |
| orch-synthesizer | `skills/orchestration/agents/orch-synthesizer.md` | Workflow Synthesizer | Integrative |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| orch-planner | Multi-agent workflow design, pipeline architecture, quality gate planning | ORCHESTRATION_PLAN.md, ORCHESTRATION.yaml |
| orch-tracker | State updates, artifact registration, quality score tracking, checkpoint creation | Updated ORCHESTRATION.yaml, WORKTRACKER.md |
| orch-synthesizer | Cross-pipeline synthesis, barrier aggregation, final reporting | Synthesis reports, workflow summaries |

**Invocation**: Use `/orchestration` skill for multi-phase workflows.

**Artifact Location**: `{project}/orchestration/{workflow-id}/`

---

## Adversary Skill Agents

These agents implement adversarial quality strategies for deliverable review.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| adv-selector | `skills/adversary/agents/adv-selector.md` | Strategy Selector | Convergent |
| adv-executor | `skills/adversary/agents/adv-executor.md` | Strategy Executor | Convergent |
| adv-scorer | `skills/adversary/agents/adv-scorer.md` | Quality Scorer | Convergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| adv-selector | Map criticality levels (C1-C4) to adversarial strategy sets per SSOT | Strategy selection plan |
| adv-executor | Execute strategy templates against deliverables, produce findings | Strategy execution reports |
| adv-scorer | Apply S-014 LLM-as-Judge scoring with dimension-level rubrics | Quality score reports |

**Invocation**: Use `/adversary` skill for standalone adversarial review or integrated into creator-critic-revision cycles.

**Strategy Templates**: `.context/templates/adversarial/s-{NNN}-{name}.md`

---

## Worktracker Skill Agents

These agents manage work item verification, visualization, and auditing.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| wt-verifier | `skills/worktracker/agents/wt-verifier.md` | Status Verification Specialist | Convergent |
| wt-visualizer | `skills/worktracker/agents/wt-visualizer.md` | Visualization Specialist | Divergent |
| wt-auditor | `skills/worktracker/agents/wt-auditor.md` | Integrity Auditor | Systematic |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| wt-verifier | Validate acceptance criteria, evidence, and completion readiness before DONE transitions | Verification reports |
| wt-visualizer | Generate burndown charts, dependency graphs, timeline views | Visual dashboards (ASCII/Mermaid) |
| wt-auditor | Cross-file integrity checks, template compliance, orphan detection | Audit reports |

**Invocation**: Use `/worktracker` skill for work item management.

**WTI Rules Enforced**: WTI-002 (No Closure Without Verification), WTI-003 (Truthful State), WTI-006 (Evidence-Based Closure)

**AST Enforcement (H-33):** All wt-* agents have Bash tool access and MUST use `jerry ast` CLI commands (`uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast frontmatter`, `jerry ast validate`, etc.) for frontmatter extraction and entity validation. Regex-based frontmatter parsing (`> **Status:**` grep) is prohibited.

---

## Transcript Skill Agents

These agents parse, extract, and format transcript files.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| ts-parser | `skills/transcript/agents/ts-parser.md` | Transcript Parsing Orchestrator | Convergent |
| ts-extractor | `skills/transcript/agents/ts-extractor.md` | Entity Extractor | Divergent |
| ts-formatter | `skills/transcript/agents/ts-formatter.md` | Output Formatter | Convergent |
| ts-mindmap-ascii | `skills/transcript/agents/ts-mindmap-ascii.md` | ASCII Mind Map Generator | Convergent |
| ts-mindmap-mermaid | `skills/transcript/agents/ts-mindmap-mermaid.md` | Mermaid Mind Map Generator | Convergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| ts-parser | VTT/SRT/plain text parsing with Python delegation (Strategy Pattern orchestrator) | canonical-transcript.json, chunks/ |
| ts-extractor | Extract entities (people, topics, decisions) from parsed transcripts | extraction-report.json |
| ts-formatter | Format transcripts as markdown, text, or structured output | Formatted transcript files |
| ts-mindmap-ascii | Generate ASCII mind maps from transcript structure | ASCII diagrams |
| ts-mindmap-mermaid | Generate Mermaid mind maps from transcript structure | Mermaid diagrams |

**Invocation**: Use `/transcript` skill for transcript processing.

**Hybrid Architecture**: ts-parser delegates VTT files to Python parser (1,250x cost reduction), uses LLM fallback for SRT/plain text.

---

## PM/PMM Skill Agents

These agents provide product management and product marketing capabilities.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| pm-product-strategist | `skills/pm-pmm/agents/pm-product-strategist.md` | Product Strategist | Integrative |
| pm-customer-insight | `skills/pm-pmm/agents/pm-customer-insight.md` | Customer Insight Researcher | Divergent |
| pm-market-strategist | `skills/pm-pmm/agents/pm-market-strategist.md` | Market Strategist | Convergent |
| pm-business-analyst | `skills/pm-pmm/agents/pm-business-analyst.md` | Business Analyst | Convergent |
| pm-competitive-analyst | `skills/pm-pmm/agents/pm-competitive-analyst.md` | Competitive Intelligence Analyst | Convergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| pm-product-strategist | PRDs, product vision, roadmaps, feature prioritization (RICE/Kano/WSJF) | Product strategy artifacts |
| pm-customer-insight | User personas (JTBD), journey maps, VOC research, customer discovery | Customer insight artifacts |
| pm-market-strategist | GTM plans, positioning (Dunford), MRDs, buyer personas, launch planning | Market strategy artifacts |
| pm-business-analyst | Business cases, market sizing (TAM/SAM/SOM), pricing analysis, financial models | Business analysis artifacts |
| pm-competitive-analyst | Competitive analysis, battle cards, win/loss analysis, Porter's Five Forces | Competitive intelligence artifacts |

**Invocation**: Use `/pm-pmm` skill for product management and product marketing work.

**Discovery/Delivery Mode**: All agents support dual-mode operation -- discovery mode (hypothesis-driven sketches) before delivery mode (validated production artifacts).

---

## Prompt Engineering Skill Agents

These agents implement structured prompt construction and quality validation through the `/prompt-engineering` skill. Operationalizes PROJ-014 negative prompting research findings (NPT-013: 100% compliance vs 92.2% positive-only, p=0.016).

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| pe-builder | `skills/prompt-engineering/agents/pe-builder.md` | Interactive prompt assembly (5-element anatomy) | Integrative |
| pe-constraint-gen | `skills/prompt-engineering/agents/pe-constraint-gen.md` | NPT pattern selector and constraint formatter | Systematic |
| pe-scorer | `skills/prompt-engineering/agents/pe-scorer.md` | Prompt quality scorer (7-criterion rubric) | Convergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| pe-builder | Walk users through 5-element prompt anatomy, generate XML-wrapped structured prompts | Structured prompts with routing, scope, data source, quality gate, output path |
| pe-constraint-gen | Convert intent to NPT-009/NPT-013 formatted constraints with XML wrapping | `<forbidden_actions>` and `<constraint>` XML blocks |
| pe-scorer | Evaluate prompts against 7-criterion rubric (C1-C7), return dimension scores | Dimension-level scores with weighted composite and improvement suggestions |

**Invocation**: Use `/prompt-engineering` skill. Keywords: build prompt, create prompt, NPT pattern, constraint generation, score prompt.

**Model Tiers:** pe-builder (opus), pe-constraint-gen (sonnet), pe-scorer (haiku).

---

## Diataxis Skill Agents

These agents implement Diataxis four-quadrant documentation methodology through the `/diataxis` skill. Four writer agents produce quadrant-specific documentation, a classifier routes requests to the correct quadrant, and an auditor evaluates existing documentation quality.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| diataxis-tutorial | `skills/diataxis/agents/diataxis-tutorial.md` | Tutorial Writer | Systematic |
| diataxis-howto | `skills/diataxis/agents/diataxis-howto.md` | How-To Guide Writer | Systematic |
| diataxis-reference | `skills/diataxis/agents/diataxis-reference.md` | Reference Writer | Systematic |
| diataxis-explanation | `skills/diataxis/agents/diataxis-explanation.md` | Explanation Writer | Divergent |
| diataxis-classifier | `skills/diataxis/agents/diataxis-classifier.md` | Documentation Classifier | Convergent |
| diataxis-auditor | `skills/diataxis/agents/diataxis-auditor.md` | Documentation Auditor | Systematic |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| diataxis-tutorial | Learning-oriented docs with step-by-step guided experience | Tutorial documents |
| diataxis-howto | Goal-oriented docs for competent users solving specific problems | How-to guide documents |
| diataxis-reference | Information-oriented docs with structured, neutral descriptions | Reference documents |
| diataxis-explanation | Understanding-oriented docs with context, connections, and rationale | Explanation documents |
| diataxis-classifier | Classify requests into Diataxis quadrants using two-axis test | Classification results |
| diataxis-auditor | Audit existing docs against per-quadrant quality criteria | Audit reports |

**Invocation**: Use `/diataxis` skill. Classifier routes requests; writer agents produce documents; auditor evaluates quality.

**Model Tiers:** diataxis-explanation (opus), diataxis-classifier (haiku); all others (sonnet).

**Tool Tiers:** diataxis-classifier and diataxis-auditor are T1 (read-only); all writer agents are T2 (read-write).

**Artifact Location**: `projects/${JERRY_PROJECT}/docs/{quadrant}/{topic-slug}.md`

---

## User-Experience Skill Agents

These agents implement AI-augmented UX methodology for tiny teams through the `/user-experience` skill. One parent orchestrator routes to 10 framework specialist agents deployed across 5 criteria-gated waves. Each agent encapsulates a proven UX framework with synthesis hypothesis confidence gates.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| ux-orchestrator | `skills/user-experience/agents/ux-orchestrator.md` | Parent orchestrator: routing, wave gating, cross-framework synthesis | Integrative |
| ux-heuristic-evaluator | `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` | Nielsen heuristic evaluation specialist | Systematic |
| ux-jtbd-analyst | `skills/ux-jtbd/agents/ux-jtbd-analyst.md` | Jobs-to-Be-Done research and analysis | Divergent |
| ux-lean-ux-facilitator | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` | Lean UX hypothesis and experiment facilitation | Systematic |
| ux-heart-analyst | `skills/ux-heart-metrics/agents/ux-heart-analyst.md` | HEART metrics framework specialist | Systematic |
| ux-atomic-architect | `skills/ux-atomic-design/agents/ux-atomic-architect.md` | Atomic design component taxonomy architect | Systematic |
| ux-inclusive-evaluator | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` | Inclusive design and accessibility auditor | Systematic |
| ux-behavior-diagnostician | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` | Fogg B=MAP behavior bottleneck diagnosis | Convergent |
| ux-kano-analyst | `skills/ux-kano-model/agents/ux-kano-analyst.md` | Kano model feature classification and prioritization | Convergent |
| ux-sprint-facilitator | `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` | AJ&Smart Design Sprint 2.0 facilitation | Systematic |
| ux-ai-design-guide | `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` | AI-first interaction design specialist (CONDITIONAL) | Divergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| ux-orchestrator | Route UX requests by product lifecycle stage, enforce wave gates, synthesize cross-framework findings | Synthesis reports, routing decisions |
| ux-heuristic-evaluator | Nielsen's 10 Heuristics with severity-rated findings | Heuristic evaluation reports |
| ux-jtbd-analyst | Switch interviews, job mapping, outcome-driven innovation | JTBD analysis reports |
| ux-lean-ux-facilitator | Hypothesis-driven build-measure-learn experiment cycles | Lean UX experiment plans |
| ux-heart-analyst | Google Goal-Signal-Metric framework for UX measurement | HEART metrics dashboards |
| ux-atomic-architect | Brad Frost 5-level component taxonomy and design tokens | Component inventories |
| ux-inclusive-evaluator | WCAG 2.2 compliance and Microsoft Inclusive Design evaluation | Accessibility audit reports |
| ux-behavior-diagnostician | Fogg B=MAP bottleneck analysis for action completion | Behavior diagnosis reports |
| ux-kano-analyst | Must-be / Performance / Attractive feature classification | Kano classification reports |
| ux-sprint-facilitator | AJ&Smart Design Sprint 2.0 four-day process facilitation | Sprint deliverables |
| ux-ai-design-guide | AI interface patterns, trust calibration, conversational UX | AI interaction design guides |

**Invocation**: Use `/user-experience` skill. Keywords: UX, user experience, usability, heuristic evaluation, JTBD, lean UX, HEART metrics, atomic design, inclusive design, behavior design, Kano model, design sprint.

**Model Tiers:** ux-orchestrator (opus), ux-sprint-facilitator (opus), ux-ai-design-guide (opus), ux-heuristic-evaluator (haiku*); all others (sonnet). *Haiku for high-volume checklist evaluation; escalates to Sonnet per AD-M-009.

**Tool Tiers:** ux-orchestrator is T5 (Orchestration, with Task for delegation); all sub-skill agents are T2 or T4 (no Task tool per P-003).

**Wave Architecture:** Sub-skills deploy in 5 criteria-gated waves. Wave 0 (Foundation) deploys the orchestrator. Waves 1-5 deploy sub-skills progressively based on team maturity criteria.

**Artifact Location**: `skills/{sub-skill}/output/{engagement-id}/ux-{agent}-{topic-slug}.md`

---

## Use Case Skill Agents

These agents implement guided use case authoring and decomposition through the `/use-case` skill, using Cockburn's 12-step writing process and Jacobson UC 2.0 progressive narrative levels and slicing methodology.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| uc-author | `skills/use-case/agents/uc-author.md` | Use Case Author (Cockburn 12-step, Jacobson UC 2.0 narrative levels) | Integrative |
| uc-slicer | `skills/use-case/agents/uc-slicer.md` | Use Case Slicer (Jacobson UC 2.0 Activities 2, 4, 5) | Systematic |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| uc-author | Create and elaborate use case artifacts through four progressive detail levels | Use case artifacts with YAML frontmatter |
| uc-slicer | Decompose use cases into implementation-ready slices; produce realization interaction sequences | Updated UC artifacts with slices and interactions |

**Invocation**: Use `/use-case` skill. Keywords: write use case, create use case, elaborate, Cockburn, slice, decompose, INVEST, interaction sequence.

**Model Tiers:** Both agents use sonnet.

**Artifact Location**: `projects/${JERRY_PROJECT}/use-cases/`

---

## Test Spec Skill Agents

These agents implement BDD test specification generation from use case artifacts through the `/test-spec` skill, using Clark's (2018) UC2.0-to-Gherkin deterministic transformation algorithm.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| tspec-generator | `skills/test-spec/agents/tspec-generator.md` | Clark Transformation -- UC flows to Gherkin scenarios | Systematic |
| tspec-analyst | `skills/test-spec/agents/tspec-analyst.md` | Coverage Analysis -- 7 Cs quality framework | Convergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| tspec-generator | Transform use case flows (basic, alternative, extensions) into Gherkin BDD Feature files | Feature files (.feature.md) with traceability |
| tspec-analyst | Analyze test coverage completeness against use case flows using 7 Cs framework | Coverage reports with gap remediation |

**Invocation**: Use `/test-spec` skill. Keywords: test spec, BDD, Gherkin, feature file, Given When Then, generate tests from use case, coverage analysis.

**Model Tiers:** Both agents use sonnet.

**Artifact Location**: `projects/${JERRY_PROJECT}/test-specs/`

---

## Contract Design Skill Agents

These agents implement API contract generation from use case artifacts through the `/contract-design` skill, using a novel UC-to-contract transformation algorithm producing OpenAPI 3.1 specifications with full traceability.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| cd-generator | `skills/contract-design/agents/cd-generator.md` | UC-to-OpenAPI Transformation (novel algorithm, 9-step mapping) | Convergent |
| cd-validator | `skills/contract-design/agents/cd-validator.md` | Contract Validation (9-step protocol, traceability verification) | Systematic |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| cd-generator | Transform UC interaction sequences into OpenAPI 3.1 contracts with HTTP method inference and schema derivation | OpenAPI contracts (.openapi.yaml) + mapping documents |
| cd-validator | Validate contracts against OpenAPI 3.1 structural standards and verify traceability from operations to source interactions | Validation reports with PASS/FAIL per check |

**Invocation**: Use `/contract-design` skill. Keywords: API contract, OpenAPI, contract design, generate contract, contract from use case, API specification.

**Model Tiers:** cd-generator uses opus; cd-validator uses sonnet.

**PROTOTYPE Label:** All generated contracts carry `x-prototype: true` until human reviewer validates and removes. Neither agent removes the label (P-020 user authority).

**Artifact Location**: `projects/${JERRY_PROJECT}/contracts/`

---

## MCP Tool Access

Agents with MCP (Model Context Protocol) tool access for external documentation lookup and cross-session memory.

### Context7 (Documentation Lookup)

| Agent | Skill | Tools |
|-------|-------|-------|
| ps-researcher | problem-solving | resolve-library-id, query-docs |
| ps-analyst | problem-solving | resolve-library-id, query-docs |
| ps-architect | problem-solving | resolve-library-id, query-docs |
| ps-investigator | problem-solving | resolve-library-id, query-docs |
| ps-synthesizer | problem-solving | resolve-library-id, query-docs |
| nse-explorer | nasa-se | resolve-library-id, query-docs |
| nse-architecture | nasa-se | resolve-library-id, query-docs |
| eng-architect | eng-team | resolve-library-id, query-docs |
| eng-lead | eng-team | resolve-library-id, query-docs |
| eng-backend | eng-team | resolve-library-id, query-docs |
| eng-frontend | eng-team | resolve-library-id, query-docs |
| eng-infra | eng-team | resolve-library-id, query-docs |
| eng-devsecops | eng-team | resolve-library-id, query-docs |
| eng-qa | eng-team | resolve-library-id, query-docs |
| eng-security | eng-team | resolve-library-id, query-docs |
| eng-reviewer | eng-team | resolve-library-id, query-docs |
| eng-incident | eng-team | resolve-library-id, query-docs |
| pm-customer-insight | pm-pmm | resolve-library-id, query-docs |
| pm-market-strategist | pm-pmm | resolve-library-id, query-docs |
| pm-competitive-analyst | pm-pmm | resolve-library-id, query-docs |
| red-lead | red-team | resolve-library-id, query-docs |
| red-recon | red-team | resolve-library-id, query-docs |
| red-vuln | red-team | resolve-library-id, query-docs |
| red-exploit | red-team | resolve-library-id, query-docs |
| red-privesc | red-team | resolve-library-id, query-docs |
| red-lateral | red-team | resolve-library-id, query-docs |
| red-persist | red-team | resolve-library-id, query-docs |
| red-exfil | red-team | resolve-library-id, query-docs |
| red-reporter | red-team | resolve-library-id, query-docs |
| red-infra | red-team | resolve-library-id, query-docs |
| red-social | red-team | resolve-library-id, query-docs |
| ux-atomic-architect | user-experience | resolve-library-id, query-docs |
| ux-inclusive-evaluator | user-experience | resolve-library-id, query-docs |
| ux-ai-design-guide | user-experience | resolve-library-id, query-docs |

### Memory-Keeper (Cross-Session Persistence)

| Agent | Skill | Tools |
|-------|-------|-------|
| orch-planner | orchestration | store, retrieve, search |
| orch-tracker | orchestration | store, retrieve, search |
| orch-synthesizer | orchestration | retrieve, search |
| ps-architect | problem-solving | store, retrieve, search |
| nse-requirements | nasa-se | store, retrieve, search |
| ts-parser | transcript | store, retrieve |
| ts-extractor | transcript | store, retrieve |

> **Not included (by design):** adv-* (self-contained strategy execution), sb-* (voice quality gate), wt-* (read-only auditing), ps-critic/ps-validator (quality evaluation), ps-reporter (report generation). eng-*/red-* agents do not use Memory-Keeper; their persistence model uses file-based output per P-002 (engagement-scoped output directories), not cross-session MCP storage.

---

## Framework Voice Skill Agents

These agents are scoped to the `saucer-boy-framework-voice` skill (internal, not user-invocable).

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| `sb-reviewer` | `skills/saucer-boy-framework-voice/agents/sb-reviewer.md` | Voice compliance review — evaluates text against 5 Authenticity Tests | convergent |
| `sb-rewriter` | `skills/saucer-boy-framework-voice/agents/sb-rewriter.md` | Voice transformation — rewrites framework output to Saucer Boy voice | divergent |
| `sb-calibrator` | `skills/saucer-boy-framework-voice/agents/sb-calibrator.md` | Voice fidelity scoring — scores text on 0-1 scale across 5 voice traits | convergent |

**Progressive Disclosure**: Agents load reference files on-demand to minimize context window usage. Always-load files vary by agent (sb-rewriter: voice-guide.md + vocabulary-reference.md; sb-calibrator: voice-guide.md; sb-reviewer: SKILL.md body only).

---

## Session Voice Skill Agents

This agent is scoped to the `saucer-boy` skill and invoked via `/saucer-boy`.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| `sb-voice` | `skills/saucer-boy/agents/sb-voice.md` | Session conversational voice — McConkey personality for work sessions | divergent |

**Two Modes**: Ambient session personality (always-on during session) and explicit McConkey invocation (on-demand persona responses). Personality disengages for hard stops, security, governance, and user override (P-020).

---

## Eng-Team Skill Agents

These agents implement secure software engineering methodology through the `/eng-team` skill, covering the full SDLC with security hardening at every phase. Follows an 8-step sequential phase-gate workflow with NIST SSDF governance, Microsoft SDL phases, OWASP ASVS verification, SLSA supply chain integrity, and DevSecOps automation patterns.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| eng-architect | `skills/eng-team/agents/eng-architect.md` | Solution Architect and Threat Modeler | Strategic |
| eng-lead | `skills/eng-team/agents/eng-lead.md` | Engineering Lead and Standards Enforcer | Convergent |
| eng-backend | `skills/eng-team/agents/eng-backend.md` | Secure Backend Engineer | Systematic |
| eng-frontend | `skills/eng-team/agents/eng-frontend.md` | Secure Frontend Engineer | Systematic |
| eng-infra | `skills/eng-team/agents/eng-infra.md` | Secure Infrastructure Engineer | Systematic |
| eng-devsecops | `skills/eng-team/agents/eng-devsecops.md` | DevSecOps Pipeline Engineer | Systematic |
| eng-qa | `skills/eng-team/agents/eng-qa.md` | Security QA Engineer | Systematic |
| eng-security | `skills/eng-team/agents/eng-security.md` | Security Code Review Specialist | Forensic |
| eng-reviewer | `skills/eng-team/agents/eng-reviewer.md` | Final Review Gate and Quality Enforcer | Convergent |
| eng-incident | `skills/eng-team/agents/eng-incident.md` | Incident Response Specialist | Forensic |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| eng-architect | System design, architecture decisions, threat modeling (STRIDE/DREAD/PASTA) | Architecture decision records, threat models |
| eng-lead | Implementation planning, code standards enforcement, dependency governance | Implementation plans, standards mappings |
| eng-backend | Server-side implementation with OWASP Top 10 and ASVS 5.0 compliance | Secure backend code, API security artifacts |
| eng-frontend | Client-side implementation with XSS prevention, CSP, CORS hardening | Secure frontend code, CSP configurations |
| eng-infra | IaC security, container hardening, SBOM generation, SLSA compliance | Infrastructure configurations, SBOMs |
| eng-devsecops | SAST/DAST pipeline integration, secrets scanning, dependency analysis | Pipeline configurations, scan reports |
| eng-qa | Security test strategy, fuzzing campaigns, property-based testing | Test artifacts, coverage reports |
| eng-security | Manual secure code review against CWE Top 25 and OWASP ASVS | Finding reports with CWE classifications |
| eng-reviewer | Final gate with /adversary integration for C2+ at >= 0.95 threshold | Quality scores, compliance status |
| eng-incident | Incident response runbooks, vulnerability lifecycle management | IR plans, monitoring configurations |

**Invocation**: Use `/eng-team` skill which orchestrates these agents in an 8-step sequential phase-gate workflow.

**Model Tiers:** eng-architect (opus), eng-reviewer (opus); all others (sonnet).

**Artifact Location**: `skills/eng-team/output/{engagement-id}/`

---

## Red-Team Skill Agents

These agents implement offensive security methodology through the `/red-team` skill, covering the full MITRE ATT&CK kill chain (14/14 tactics). Follows a non-linear workflow with mandatory scope authorization (red-lead first), circuit breaker checks at every agent transition, and RoE-gated agents for high-impact operations. Follows PTES, OSSTMM, and NIST SP 800-115 methodologies.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| red-lead | `skills/red-team/agents/red-lead.md` | Engagement Lead & Scope Authority | Strategic |
| red-recon | `skills/red-team/agents/red-recon.md` | Reconnaissance Specialist | Divergent |
| red-vuln | `skills/red-team/agents/red-vuln.md` | Vulnerability Analyst | Systematic |
| red-exploit | `skills/red-team/agents/red-exploit.md` | Exploitation Specialist | Systematic |
| red-privesc | `skills/red-team/agents/red-privesc.md` | Privilege Escalation Specialist | Systematic |
| red-lateral | `skills/red-team/agents/red-lateral.md` | Lateral Movement Specialist | Systematic |
| red-persist | `skills/red-team/agents/red-persist.md` | Persistence Specialist (RoE-GATED) | Systematic |
| red-exfil | `skills/red-team/agents/red-exfil.md` | Data Exfiltration Specialist (RoE-GATED) | Systematic |
| red-reporter | `skills/red-team/agents/red-reporter.md` | Engagement Reporter & Documentation Specialist | Integrative |
| red-infra | `skills/red-team/agents/red-infra.md` | Infrastructure & Tooling Specialist | Systematic |
| red-social | `skills/red-team/agents/red-social.md` | Social Engineering Specialist (RoE-GATED) | Divergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| red-lead | Scope establishment, RoE definition, authorization management | Scope documents, RoE YAML |
| red-recon | OSINT, network enumeration, service discovery, attack surface mapping | Reconnaissance reports |
| red-vuln | Vulnerability identification, CVE research, exploit availability assessment | Vulnerability reports with risk scores |
| red-exploit | Exploit methodology, payload crafting guidance, vulnerability chaining | Exploitation methodology reports |
| red-privesc | Local/domain privilege escalation, credential harvesting, token manipulation | Privilege escalation reports |
| red-lateral | Network pivoting, tunneling, living-off-the-land techniques | Lateral movement reports |
| red-persist | Backdoor placement methodology, scheduled tasks, rootkit analysis (RoE-GATED) | Persistence methodology reports |
| red-exfil | Data exfiltration channels, covert communication, DLP bypass (RoE-GATED) | Exfiltration methodology reports |
| red-reporter | Engagement reports, finding documentation, executive summaries | Final engagement reports |
| red-infra | C2 framework management, payload building, redirector infrastructure | Infrastructure methodology reports |
| red-social | Phishing campaigns, pretexting, vishing methodology (RoE-GATED) | Social engineering methodology reports |

**Invocation**: Use `/red-team` skill. red-lead MUST establish scope first (mandatory). After scope, any agent is invocable in any order.

**Model Tiers:** red-lead (opus), red-reporter (opus); all others (sonnet).

**Artifact Location**: `skills/red-team/output/{engagement-id}/`

**RoE-Gated Agents:** red-persist, red-exfil, red-social require explicit authorization in the Rules of Engagement beyond standard scope authorization.

---

## Agent Handoff Protocol

### Triggering Handoffs

Handoffs are triggered by:
1. **Hook-based**: `scripts/subagent_stop.py` detects completion
2. **Explicit**: Parent agent delegates via Task tool
3. **Skill-based**: Skill orchestrator routes to appropriate specialist

### Handoff Data

When handing off between agents, include:
```json
{
  "from_agent": "ps-researcher",
  "to_agent": "ps-analyst",
  "context": {
    "task_id": "WORK-123",
    "artifacts": ["research/proj-001-e-001-research.md"],
    "summary": "Completed initial research on architecture patterns"
  },
  "request": "Analyze findings and identify gaps"
}
```

---

## Adding New Agents

New agents should be added within their respective skill directory:

1. Create agent file in `skills/{skill-name}/agents/{agent-name}.md`
2. Define persona, responsibilities, and constraints
3. Register in this file (AGENTS.md) under the skill section
4. Update skill orchestrator to know about the new agent
5. Add relevant hooks if needed

### Agent File Template

```markdown
---
name: {agent-name}
description: |
  Use this agent when {trigger conditions}.
  <example>User: "{example prompt}"</example>
model: sonnet
tools:
  - Read
  - Grep
  - Glob
---

# {Agent Name}

## Persona
{One paragraph describing the agent's character and expertise}

## Responsibilities
- {Primary responsibility}
- {Secondary responsibility}
- ...

## Constraints
- {What this agent should NOT do}
- {Boundaries of authority}

## Input Format
{What information this agent needs to start work}

## Output Format
{What this agent produces when done}

## Handoff Triggers
{When this agent should hand off to another}
```
