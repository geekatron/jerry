# TASK-001: Context Taxonomy for Strategy Applicability

<!--
DOCUMENT-ID: FEAT-004:EN-303:TASK-001
VERSION: 1.0.0
AGENT: ps-architect
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-303 (Situational Applicability Mapping)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DESIGN
REQUIREMENTS: FR-001, FR-002, FR-008, NFR-001, NFR-005
TARGET-ACS: 1, 10, 11
-->

> **Version:** 1.0.0
> **Agent:** ps-architect
> **Quality Target:** >= 0.92
> **Purpose:** Define the dimensions that determine which adversarial strategy to apply in a given context, producing a formal taxonomy consumable by both human users and automated orchestration

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this taxonomy delivers and why it matters |
| [Dimension 1: Review Target Type](#dimension-1-review-target-type) | What kind of artifact is being reviewed |
| [Dimension 2: Review Phase](#dimension-2-review-phase) | Where in the lifecycle the review occurs |
| [Dimension 3: Decision Criticality Level](#dimension-3-decision-criticality-level) | How critical the artifact is (C1-C4) |
| [Dimension 4: Artifact Maturity](#dimension-4-artifact-maturity) | How mature the artifact is in its lifecycle |
| [Dimension 5: Team Composition](#dimension-5-team-composition) | Who is performing the review |
| [Dimension 6: Enforcement Layer Availability](#dimension-6-enforcement-layer-availability) | Which enforcement layers are available in the environment |
| [Dimension 7: Platform Context](#dimension-7-platform-context) | What platform the review operates on |
| [Dimension 8: Token Budget State](#dimension-8-token-budget-state) | Whether token budget is available or constrained |
| [Cross-Dimension Interactions](#cross-dimension-interactions) | How dimensions combine and constrain each other |
| [Taxonomy Summary Table](#taxonomy-summary-table) | Consolidated quick-reference for all dimensions |
| [Traceability](#traceability) | Mapping to requirements and source documents |
| [References](#references) | Source citations |

---

## Summary

This document defines an 8-dimension context taxonomy that determines which adversarial strategies are applicable for a given review situation. Every review context within Jerry can be described by specifying a value along each of these 8 dimensions. The taxonomy is the foundational input to the per-strategy applicability profiles (TASK-003) and the strategy selection decision tree (TASK-004).

The taxonomy satisfies three constraints:

1. **Completeness** -- every plausible review situation in Jerry can be described by a combination of these dimensions (FR-001, FR-002).
2. **Orthogonality** -- each dimension captures an independent aspect of context; changing one dimension does not logically force a change in another (though some combinations are more common than others).
3. **Actionability** -- each dimension directly influences which strategies are appropriate; no dimension is included merely for classification (NFR-005, NFR-006).

The dimensions are derived from three authoritative sources:
- **ADR-EPIC002-001** (ACCEPTED): Decision criticality levels C1-C4, quality layer composition L0-L4, mechanistic family diversity.
- **Barrier-1 ENF-to-ADV handoff**: 5-layer enforcement architecture (L1-L5 + Process), platform portability constraints, token budget ceilings, 4 RED systemic risks.
- **EN-303 enabler specification**: Review target type, review phase, artifact maturity, team composition.

---

## Dimension 1: Review Target Type

**Definition:** The category of artifact under adversarial review. Different artifact types have different failure modes, quality criteria, and applicable strategies.

**Source:** EN-303 enabler specification, Technical Approach item 1.

### Enumeration

| Value | Code | Definition | Examples | Impact on Strategy Selection |
|-------|------|-----------|----------|------------------------------|
| **Code** | TGT-CODE | Source code files, including Python modules, scripts, tests, and configuration-as-code | `src/domain/aggregates/work_item.py`, `tests/unit/test_work_item.py`, `pyproject.toml` | Favors deterministic strategies: S-012 (FMEA for failure modes), S-011 (CoVe for factual verification of claims in docstrings), S-007 (Constitutional AI against coding standards). Enforcement layers L3/L5 can provide automated gating. |
| **Architecture** | TGT-ARCH | Design documents, ADRs, system diagrams, pattern selections, interface definitions | ADR-EPIC002-001, hexagonal architecture documents, bounded context maps | Favors analytical strategies: S-001 (Red Team for vulnerability simulation), S-004 (Pre-Mortem for failure imagination), S-002 (Devil's Advocate for challenging assumptions). Automated enforcement is limited; process-layer enforcement dominates. |
| **Requirements** | TGT-REQ | Shall statements, acceptance criteria, functional/non-functional specifications, verification matrices | FR-001 through FR-011 in EN-303, NPR 7123.1D-style requirements | Favors completeness-oriented strategies: S-013 (Inversion to generate anti-requirements), S-012 (FMEA for requirement failure modes), S-011 (CoVe for factual claims in requirements). Requires traceability verification. |
| **Research** | TGT-RES | Literature reviews, trade studies, analysis reports, synthesis documents, evidence catalogs | EN-301 research artifacts, EN-302 trade study, strategy catalogs | Favors evidence-quality strategies: S-011 (CoVe for factual verification), S-002 (Devil's Advocate for challenging conclusions), S-003 (Steelman for fair representation of sources). Low enforcement automation potential. |
| **Design Decisions** | TGT-DEC | ADRs, trade-off analyses, option evaluations, selection rationale, governance decisions | ADR-EPIC002-001, ADR-EPIC002-002, constitutional amendments | Favors dialectical strategies: S-003 (Steelman the chosen option), S-002 (Devil's Advocate the chosen option), S-004 (Pre-Mortem the decision), S-013 (Inversion the decision). **Auto-escalation to C3+ if touching governance artifacts** (FR-011). |
| **Process** | TGT-PROC | Workflow definitions, orchestration plans, skill configurations, agent definitions, runbooks | ORCHESTRATION.yaml, SKILL.md files, PLAYBOOK.md files | Favors operational strategies: S-004 (Pre-Mortem for process failure), S-012 (FMEA for process failure modes), S-007 (Constitutional AI against process rules). Process-layer enforcement is primary mechanism. |

### Strategy Affinity by Target Type

| Target Type | High Affinity Strategies | Medium Affinity | Low Affinity |
|-------------|-------------------------|-----------------|--------------|
| TGT-CODE | S-007, S-012, S-011, S-010, S-014 | S-013, S-002 | S-001, S-004, S-003 |
| TGT-ARCH | S-001, S-004, S-002, S-013 | S-003, S-007, S-012, S-014 | S-010, S-011 |
| TGT-REQ | S-013, S-012, S-011, S-007 | S-002, S-003, S-014 | S-001, S-004, S-010 |
| TGT-RES | S-011, S-002, S-003, S-014 | S-013, S-007 | S-001, S-004, S-010, S-012 |
| TGT-DEC | S-003, S-002, S-004, S-013, S-014 | S-001, S-007, S-012 | S-010, S-011 |
| TGT-PROC | S-004, S-012, S-007, S-013 | S-002, S-014, S-001 | S-003, S-010, S-011 |

**Note:** "Low affinity" does not mean "never use"; it means the strategy provides less value for that target type compared to high-affinity alternatives. At higher criticality levels (C3-C4), all strategies become candidates regardless of target-type affinity.

---

## Dimension 2: Review Phase

**Definition:** The stage in the artifact lifecycle at which the adversarial review occurs. Early phases benefit from exploratory, divergent strategies; late phases benefit from convergent, verification-oriented strategies.

**Source:** EN-303 enabler specification, Technical Approach item 1.

### Enumeration

| Value | Code | Definition | Impact on Strategy Selection |
|-------|------|-----------|------------------------------|
| **Early Exploration** | PH-EXPLORE | Initial brainstorming, research, option identification. Artifact is formless or draft. | Favor generative strategies: S-013 (Inversion to generate anti-patterns early), S-004 (Pre-Mortem to identify risks early). **Avoid** premature convergence strategies: S-007 (no constitution to evaluate against yet), S-014 (no rubric to score against yet). S-001 (Red Team) risk of "premature adversarial pressure" (TASK-002: R-001-QR=9) is highest here. |
| **Design** | PH-DESIGN | Structured design activity. Architecture decisions, interface definitions, requirement specification. Artifact has structure but is not implemented. | Full strategy palette available. S-003 (Steelman) + S-002 (DA) for dialectical challenge. S-012 (FMEA) for systematic failure analysis. S-013 (Inversion) for anti-pattern checklists. This is the highest-value phase for adversarial review -- errors caught here have the highest cost-avoidance multiplier. |
| **Implementation** | PH-IMPL | Coding, configuration, template creation. Artifact is concrete and testable. | Favor verification strategies: S-007 (Constitutional AI against standards), S-011 (CoVe for factual correctness), S-010 (Self-Refine for iterative improvement), S-014 (LLM-as-Judge for quality scoring). Enforcement layers L3/L5 provide automated coverage for code artifacts. |
| **Validation** | PH-VALID | Testing, review, quality gate evaluation. Artifact is nominally complete and undergoing acceptance. | Favor evaluation strategies: S-014 (LLM-as-Judge for rubric scoring), S-007 (Constitutional AI for compliance verification), S-011 (CoVe for claim verification). This is the final gating phase -- strategy emphasis shifts from finding new issues to confirming quality. |
| **Maintenance** | PH-MAINT | Post-delivery modifications, refactoring, regression. Artifact is baselined and being modified. | Favor regression-sensitive strategies: S-012 (FMEA for impact of changes), S-011 (CoVe for verifying existing claims still hold), S-007 (Constitutional AI for standards compliance after changes). Enforcement layers L5 (CI regression tests) are primary defense. |

### Phase-Strategy Interaction Matrix

| Phase | Recommended Strategies | Cautionary Strategies | Rationale |
|-------|----------------------|----------------------|-----------|
| PH-EXPLORE | S-013, S-004, S-003 | S-001 (premature pressure), S-007 (no constitution yet), S-014 (no rubric yet) | Divergent thinking needed; convergent evaluation premature |
| PH-DESIGN | S-003, S-002, S-012, S-013, S-004, S-001 | None -- full palette appropriate | Highest adversarial review value; all strategies applicable |
| PH-IMPL | S-007, S-011, S-010, S-014, S-012 | S-004 (too late for failure imagination), S-003 (less value for concrete code) | Verification and standards compliance dominate |
| PH-VALID | S-014, S-007, S-011 | S-013 (generative output adds noise during validation), S-004 (too late) | Scoring and confirmation, not exploration |
| PH-MAINT | S-012, S-011, S-007, S-014 | S-001 (full red team expensive for maintenance changes) | Regression detection and impact analysis |

---

## Dimension 3: Decision Criticality Level

**Definition:** The risk and impact classification of the artifact or decision under review, following the ADR-EPIC002-001 criticality levels. This is the primary branching dimension in the decision tree (TASK-004).

**Source:** ADR-EPIC002-001 Section "Quality Layer Composition" and "Decision Criticality Escalation".

### Enumeration

| Value | Code | Definition | Quality Layer Mapping | Strategy Intensity | Token Budget Expectation |
|-------|------|-----------|----------------------|--------------------|--------------------------|
| **C1: Routine** | CRIT-C1 | Low-risk, well-understood tasks. Standard code changes, documentation updates, routine configuration. Expected failure impact: localized, easily reversible. | L0 (Self-Check) + L1 (Light Review) | Minimal: S-010 (Self-Refine) + optional S-003 + S-014 | Ultra-Low: 2,000-5,600 tokens |
| **C2: Significant** | CRIT-C2 | Moderate-risk tasks. New feature implementation, interface changes, non-trivial refactoring. Expected failure impact: multi-component, requires investigation to reverse. This is Jerry's **target operating layer** per ADR-EPIC002-001. | L2 (Standard Critic) | Standard: S-007 (Constitutional AI) + S-002 (DA) + S-014 (Judge) | Low-Medium: 8,000-16,000 tokens |
| **C3: Major** | CRIT-C3 | High-risk tasks. Architecture decisions, cross-boundary changes, pattern introductions, security-relevant modifications. Expected failure impact: system-wide, costly to reverse. **Auto-escalation**: Any artifact touching `docs/governance/JERRY_CONSTITUTION.md` or `.claude/rules/` is automatically C3+ (FR-011). | L3 (Deep Review) | Intensive: L2 strategies + S-004 (Pre-Mortem) + S-012 (FMEA) + S-013 (Inversion) | Medium: 16,000-35,000 tokens |
| **C4: Critical** | CRIT-C4 | Highest-risk tasks. Governance changes, constitutional amendments, irreversible system decisions, security architecture. Expected failure impact: framework-threatening, potentially irreversible. | L4 (Tournament) | Maximum: L3 strategies + S-001 (Red Team) + S-011 (CoVe) | Medium-High: 35,000-55,000 tokens |

### Criticality Determination Guidelines

| Signal | Criticality Implication |
|--------|------------------------|
| Artifact modifies `docs/governance/JERRY_CONSTITUTION.md` | Auto-C3+ (FR-011) |
| Artifact modifies `.claude/rules/` | Auto-C3+ (FR-011) |
| Artifact introduces new architectural pattern | C3 minimum |
| Artifact modifies bounded context boundaries | C3 minimum |
| Artifact modifies security-relevant code (auth, crypto, access control) | C3 minimum |
| Artifact is a new ADR | C3 minimum |
| Artifact modifies existing baselined ADR | C4 |
| Artifact is routine code within established patterns | C1 default |
| Artifact is a new feature following existing architecture | C2 default |

### Strategy Allocation by Criticality

| Criticality | Required Strategies | Optional Strategies | Token Budget Range |
|-------------|--------------------|--------------------|-------------------|
| C1 | S-010 | S-003, S-014 | 2,000-5,600 |
| C2 | S-007, S-002, S-014 | S-003, S-010 | 8,000-16,000 |
| C3 | S-007, S-002, S-014, S-004, S-012, S-013 | S-003, S-010, S-011 | 16,000-35,000 |
| C4 | All 10 strategies | None -- all deployed | 35,000-55,000 |

**Cross-reference:** ADR-EPIC002-001 Section "Quality Layer Composition" defines L0-L4 quality layers. The strategy allocation above maps directly to those layers.

---

## Dimension 4: Artifact Maturity

**Definition:** The maturity stage of the artifact in its governance lifecycle. Maturity determines how disruptive adversarial findings can be -- challenging a draft is cheap; challenging a baselined artifact requires formal change management.

**Source:** EN-303 enabler specification, Technical Approach item 1.

### Enumeration

| Value | Code | Definition | Impact on Strategy Selection |
|-------|------|-----------|------------------------------|
| **Draft** | MAT-DRAFT | Initial creation, not yet reviewed. Author is still actively modifying. No governance approval. | Full strategy palette available. Findings can be incorporated immediately. Prefer generative strategies (S-013, S-004) to maximize early defect identification. Cost of change is lowest here. |
| **Reviewed** | MAT-REVIEW | Has undergone at least one adversarial review cycle. Known issues addressed. Awaiting approval or further iteration. | Focus on verification and validation strategies: S-014 (scoring), S-007 (compliance), S-011 (factual verification). Findings from this stage should be incremental, not fundamental. If fundamental issues are found, the artifact should be returned to Draft. |
| **Approved** | MAT-APPR | Formally approved by governance process (user ratification per P-020, quality gate per V-057). Ready for implementation or deployment. | Restrict to lightweight verification: S-014 (scoring confirmation), S-007 (compliance check). New adversarial challenges at this stage indicate process failure in earlier stages. Any significant finding requires formal change request. |
| **Baselined** | MAT-BASE | Committed to the repository as the canonical version. Changes require formal revision process (ADR amendment, version bump). | Restrict to regression detection: S-011 (verify existing claims still hold after related changes), S-007 (verify continued compliance). Full adversarial review only if the artifact is being formally revised (in which case maturity reverts to Draft for the revision scope). |

### Maturity-Strategy Interaction

| Maturity | Full Review Appropriate? | Strategy Restrictions | Governance Implication |
|----------|------------------------|-----------------------|----------------------|
| MAT-DRAFT | Yes | None | Findings incorporated directly |
| MAT-REVIEW | Incremental only | Avoid S-001 (full Red Team is expensive at this stage unless C3+) | Findings feed revision cycle |
| MAT-APPR | No (unless triggering formal revision) | Only S-014, S-007, S-011 | Findings require formal change request |
| MAT-BASE | No (unless formally reopened) | Only regression-oriented: S-011, S-007 | Findings require ADR amendment or version revision |

---

## Dimension 5: Team Composition

**Definition:** The agent/human configuration performing the review. This affects which strategies can be executed (some require multi-agent orchestration) and how P-020 (User Authority) is enforced.

**Source:** EN-303 enabler specification, Technical Approach item 1.

### Enumeration

| Value | Code | Definition | Impact on Strategy Selection |
|-------|------|-----------|------------------------------|
| **Single Agent** | TEAM-SINGLE | One agent performing self-review or applying a strategy to its own output. No orchestrator-worker separation. | Limited to single-agent strategies: S-010 (Self-Refine), S-013 (Inversion), S-014 (LLM-as-Judge self-scoring). Cannot execute strategies requiring a separate critic agent (S-002, S-001). P-003 compliant by definition. |
| **Multi-Agent Orchestration** | TEAM-MULTI | Orchestrator delegates to one or more worker agents in the creator-critic-revision pattern. Compliant with P-003 (max one level: orchestrator -> worker). | Full strategy palette available. S-002 (DA) and S-001 (Red Team) require separate critic agent. S-007 (Constitutional AI) can leverage multi-pass across agents. Enables the complete creator-critic-revision cycle (FR-009). |
| **Human-in-the-Loop** | TEAM-HIL | Human user actively participating in review, either as reviewer or as escalation target for agent findings. Per P-020, the human has final authority. | All strategies available, with human as ultimate arbiter. Human can override agent findings. Enables strategies that benefit from domain expertise humans provide (S-001 Red Team benefits from human adversary knowledge). Required for C4 decisions (P-020). Escalation path per FR-011. |

### Team Composition Constraints on Strategies

| Strategy | TEAM-SINGLE | TEAM-MULTI | TEAM-HIL |
|----------|-------------|------------|----------|
| S-001 Red Team | Not feasible (needs separate critic with adversary persona) | Full capability | Full capability + human adversary knowledge |
| S-002 Devil's Advocate | Limited (self-DA is weaker) | Full capability | Full capability |
| S-003 Steelman | Full capability (embedded in existing pass) | Full capability | Full capability |
| S-004 Pre-Mortem | Limited (self-Pre-Mortem is weaker) | Full capability | Full capability + human domain experience |
| S-007 Constitutional AI | Full capability (single-agent multi-pass) | Full capability | Full capability |
| S-010 Self-Refine | Full capability (designed for single agent) | Full capability | Full capability |
| S-011 CoVe | Limited (context isolation harder within single agent) | Full capability (separate verification agent) | Full capability |
| S-012 FMEA | Full capability (structured output) | Full capability | Full capability + human domain expertise |
| S-013 Inversion | Full capability (single-pass generative) | Full capability | Full capability |
| S-014 LLM-as-Judge | Full capability (single-agent rubric) | Full capability | Full capability + human calibration |

---

## Dimension 6: Enforcement Layer Availability

**Definition:** Which enforcement layers from the 5-layer architecture (Barrier-1 ENF-to-ADV handoff) are available in the current operating environment. This determines which strategy delivery mechanisms can be used.

**Source:** Barrier-1 ENF-to-ADV handoff, Section "5-Layer Enforcement Architecture".

### Enumeration

| Value | Code | Definition | Available Layers | Impact on Strategy Selection |
|-------|------|-----------|-----------------|------------------------------|
| **Full Stack** | ENF-FULL | All 5 layers + Process available. Claude Code environment with hooks enabled, CI configured, rules loaded. | L1, L2, L3, L4, L5, Process | All strategy delivery mechanisms available. Strategies can be enforced through hooks (L3/L4), rules (L1/L2), CI (L5), and process gates. Maximum enforcement strength. |
| **Portable Stack** | ENF-PORT | Only portable layers available. Non-Claude-Code environment, or hooks disabled. | L1, L5, Process | Strategies cannot be enforced via hooks (L3/L4 unavailable). Must rely on rules (L1, subject to context rot per R-SYS-001), CI/pre-commit (L5), and process gates. MODERATE enforcement per Barrier-1 classification. All strategies must have portable delivery via this stack (FR-010). |
| **Minimal Stack** | ENF-MIN | Only rules available. No CI, no hooks, no formal process. Emergency or degraded environment. | L1 only | Only rule-based strategy delivery. Subject to context rot (R-SYS-001). Effective for initial sessions but degrades beyond ~20K tokens. Strategies must be self-contained in prompts. Highest risk configuration. |

### Layer-Strategy Delivery Mapping

| Enforcement Layer | Strategy Delivery Mechanism | Strategies Delivered | Context Rot Vulnerability |
|-------------------|----------------------------|---------------------|--------------------------|
| L1 (Static Context) | Rules encoded in `.claude/rules/` loaded at session start | S-007 (constitutional principles), S-010 (self-refine instruction), S-003 (steelman guidance) | VULNERABLE -- degrades after ~20K tokens (R-SYS-001) |
| L2 (Per-Prompt Reinforcement) | V-024 re-injects critical rules every prompt | S-010 (self-refine reminder), S-007 (key constitutional principles) | IMMUNE by design -- fresh injection each prompt |
| L3 (Pre-Action Gating) | V-001 PreToolUse hook triggers strategy before tool execution | S-007 (constitutional check before write), S-014 (quality score before commit) | IMMUNE -- external hook, context-rot-independent |
| L4 (Post-Action Validation) | V-002 PostToolUse hook triggers strategy after tool execution | S-014 (quality scoring of output), S-011 (factual verification of output) | MIXED -- hook is immune but agent critique may degrade |
| L5 (Post-Hoc Verification) | Pre-commit hooks, CI pipeline checks | S-012 (FMEA checklist verification), S-007 (standards compliance) | IMMUNE -- external tools, deterministic |
| Process | Workflow gates, evidence-based closure, quality gates | S-002 (DA review gate), S-001 (Red Team gate), S-004 (Pre-Mortem gate), S-014 (scoring gate) | IMMUNE -- process-based, not context-dependent |

### Context Rot Impact by Layer

Per R-SYS-001 from Barrier-1 ENF-to-ADV handoff:

| Token Count | L1 Effectiveness | L2 Effectiveness | L3-L5/Process |
|-------------|-----------------|-------------------|---------------|
| 0-20K | ~100% | ~100% | ~100% |
| 20K-50K | ~60-80% | ~100% | ~100% |
| 50K+ | ~40-60% | ~100% | ~100% |

**Strategy mapping constraint (NFR-001):** Strategies that rely solely on L1 delivery (rule-encoded guidance) should be expected to have 40-60% effectiveness degradation at 50K+ tokens. Strategies delivered through L2-L5 or Process are context-rot-immune.

---

## Dimension 7: Platform Context

**Definition:** The software platform on which Jerry is operating. This determines hook availability and, consequently, which enforcement-layer-driven strategy delivery mechanisms are accessible.

**Source:** Barrier-1 ENF-to-ADV handoff, Section "Platform Constraints".

### Enumeration

| Value | Code | Definition | Hook Availability | Enforcement Level |
|-------|------|-----------|-------------------|-------------------|
| **Claude Code (Full)** | PLAT-CC | Claude Code IDE with all hooks enabled (PreToolUse, PostToolUse, SessionStart, UserPromptSubmit). macOS or Linux. | Full: V-001, V-002, V-003, V-005 | HIGH -- all 5 layers + Process |
| **Claude Code (Windows/WSL)** | PLAT-CC-WIN | Claude Code on Windows via WSL. Hooks available but with potential compatibility issues. | Partial: hooks work under WSL, 73% estimated compatibility | HIGH with caveats -- WSL layer may introduce friction |
| **Non-Claude-Code** | PLAT-GENERIC | Any LLM IDE without Claude Code hooks: Cursor, Windsurf, generic LLM, API-direct. | None: no PreToolUse, PostToolUse, SessionStart, UserPromptSubmit | MODERATE -- L1, L5, Process only |

### Platform-Strategy Portability Matrix

| Strategy | Portable Delivery (no hooks) | Hook-Enhanced Delivery | Notes |
|----------|-----------------------------|-----------------------|-------|
| S-001 Red Team | Process gate (manual trigger) | L3 hook triggers Red Team for security-tagged files | Fully portable via process |
| S-002 Devil's Advocate | Process gate (critic step in workflow) | L3 hook triggers DA for design-tagged files | Fully portable via process |
| S-003 Steelman | L1 rule (embedded in critic prompt) | L2 reinforcement + L3 hook | Fully portable; L1 delivery subject to context rot |
| S-004 Pre-Mortem | Process gate (planning phase step) | None -- process-triggered, not hook-triggered | Fully portable; no hook dependency |
| S-007 Constitutional AI | L1 rule (constitutional principles in `.claude/rules/`) | L3 hook for pre-write constitutional check | Portable via L1; hook enhances with real-time gating |
| S-010 Self-Refine | L1 rule (self-review instruction) + L2 reinforcement | L4 hook for post-output self-review trigger | Portable via L1+L2; hook adds automation |
| S-011 CoVe | Process gate (verification step) | L4 hook for post-output factual verification | Portable via process; hook enhances automation |
| S-012 FMEA | Process gate (risk analysis step) | L5 CI check for FMEA checklist verification | Fully portable; L5 CI is universal |
| S-013 Inversion | L1 rule (inversion prompt) | None -- single-pass, no hook benefit | Fully portable; no hook dependency |
| S-014 LLM-as-Judge | Process gate (quality scoring step) | L3/L4 hook for automatic scoring | Portable via process; hooks add automation |

**Constraint (FR-010, NFR-003):** Every strategy has a portable delivery mechanism that does not depend on Claude Code hooks. The portable stack (L1 + L5 + Process) provides MODERATE enforcement for all 10 strategies. Hooks enhance enforcement to HIGH level but are not required for any strategy's basic operation.

---

## Dimension 8: Token Budget State

**Definition:** Whether the available token budget is sufficient for the strategies being considered, or whether budget constraints require selecting lower-token alternatives.

**Source:** Barrier-1 ENF-to-ADV handoff, Section "Risk Summary" (R-SYS-002, R-SYS-004); ADR-EPIC002-001 token budget tiers.

### Enumeration

| Value | Code | Definition | Available Token Budget | Strategy Implications |
|-------|------|-----------|----------------------|-----------------------|
| **Unconstrained** | TOK-FULL | Sufficient tokens remain for any strategy or combination. Session is early or medium-length. | > 20,000 tokens remaining for adversarial review | Full strategy palette available. No token-based restrictions. Prefer quality-optimal strategy selection based on other dimensions. |
| **Constrained** | TOK-CONST | Token budget is limited. Session is long, or multiple prior review cycles have consumed budget. | 5,000-20,000 tokens remaining | Prefer Ultra-Low and Low token strategies: S-010 (2,000), S-003 (1,600), S-014 (2,000), S-013 (2,100), S-002 (4,600). Avoid Medium-token strategies unless criticality demands them: S-007 (8,000-16,000), S-012 (9,000). |
| **Exhausted** | TOK-EXHAUST | Near-zero token budget remaining for adversarial review. Context rot risk is severe (R-SYS-004 feedback loop active). | < 5,000 tokens remaining | Only Ultra-Low strategies feasible: S-010 (2,000), S-003 (1,600), S-014 (2,000), S-013 (2,100). **If criticality >= C3, escalate to human review** (P-020) because agent-based review quality is severely degraded. Consider ending session and starting fresh to reset context. |

### Token Cost Reference (from ADR-EPIC002-001)

| Token Tier | Cost per Invocation | Strategies |
|------------|-------------------|-----------|
| Ultra-Low | 1,600-2,100 | S-003 (1,600), S-010 (2,000), S-014 (2,000), S-013 (2,100) |
| Low | 4,600-5,600 | S-002 (4,600), S-004 (5,600) |
| Medium | 6,000-16,000 | S-011 (6,000), S-001 (7,000), S-007 (8,000-16,000), S-012 (9,000) |

**Constraint (FR-006, NFR-002, NFR-004):** Strategy recommendations must account for token budget state. In TOK-CONST or TOK-EXHAUST states, aggressive in-context adversarial patterns that consume large token volumes must be avoided to prevent worsening the context rot + token exhaustion feedback loop (R-SYS-004).

---

## Cross-Dimension Interactions

While the 8 dimensions are designed to be orthogonal, certain combinations create important interactions:

### Interaction 1: Criticality x Token Budget

| Combination | Resolution |
|-------------|-----------|
| C3/C4 + TOK-EXHAUST | **Escalate to human review** (P-020). Agent-based review at high criticality with exhausted budget is a quality risk. The decision tree must flag this as a mandatory escalation. |
| C1 + TOK-FULL | Use minimal strategies (S-010 alone). Do not over-invest adversarial effort in routine work. |
| C2 + TOK-CONST | Use Ultra-Low versions of C2 strategies: S-003 + S-014 instead of full S-007 + S-002 + S-014. Sacrifice depth for budget compliance. |

### Interaction 2: Enforcement Layer x Platform

| Combination | Resolution |
|-------------|-----------|
| ENF-FULL + PLAT-CC | Normal operation. All layers available. |
| ENF-PORT + PLAT-GENERIC | Use portable stack only. Shift strategy delivery from hooks to process gates. All strategies still applicable but enforcement intensity drops from HIGH to MODERATE. |
| ENF-MIN + any platform | Emergency mode. Only L1 rules available. Strategies are advisory only, with no automated enforcement. Human oversight essential. |

### Interaction 3: Phase x Maturity

| Combination | Resolution |
|-------------|-----------|
| PH-EXPLORE + MAT-DRAFT | Normal -- full exploratory strategy palette. |
| PH-VALID + MAT-APPR | Restricted -- only confirmation strategies (S-014, S-007). Finding fundamental issues at this combination indicates process failure. |
| PH-MAINT + MAT-BASE | Regression-only strategies. Full review only if artifact is formally reopened. |

### Interaction 4: Target Type x Enforcement Layer

| Combination | Resolution |
|-------------|-----------|
| TGT-CODE + ENF-FULL | Maximum automated enforcement. L3 hooks gate writes, L5 CI validates output, L1 rules guide generation. |
| TGT-ARCH + ENF-PORT | Process-dominated enforcement. Architecture review relies on process gates (V-057 quality gate, V-060 evidence-based closure), not hooks. |
| TGT-RES + any | Minimal automated enforcement possible for research artifacts. Process gates and agent-based strategies are the primary mechanisms. |

---

## Taxonomy Summary Table

| # | Dimension | Values | Primary Source | Primary Impact |
|---|-----------|--------|---------------|----------------|
| 1 | Review Target Type | TGT-CODE, TGT-ARCH, TGT-REQ, TGT-RES, TGT-DEC, TGT-PROC | EN-303 specification | Determines strategy affinity and applicable enforcement mechanisms |
| 2 | Review Phase | PH-EXPLORE, PH-DESIGN, PH-IMPL, PH-VALID, PH-MAINT | EN-303 specification | Determines divergent vs. convergent strategy preference |
| 3 | Decision Criticality | CRIT-C1, CRIT-C2, CRIT-C3, CRIT-C4 | ADR-EPIC002-001 | **Primary branching dimension**: determines strategy intensity and quality layer |
| 4 | Artifact Maturity | MAT-DRAFT, MAT-REVIEW, MAT-APPR, MAT-BASE | EN-303 specification | Determines review scope restrictions and governance implications |
| 5 | Team Composition | TEAM-SINGLE, TEAM-MULTI, TEAM-HIL | EN-303 specification | Determines which strategies are executable |
| 6 | Enforcement Layer Availability | ENF-FULL, ENF-PORT, ENF-MIN | Barrier-1 ENF-to-ADV | Determines strategy delivery mechanisms |
| 7 | Platform Context | PLAT-CC, PLAT-CC-WIN, PLAT-GENERIC | Barrier-1 ENF-to-ADV | Determines hook availability and enforcement level |
| 8 | Token Budget State | TOK-FULL, TOK-CONST, TOK-EXHAUST | Barrier-1 ENF-to-ADV (R-SYS-002, R-SYS-004) | Constrains strategy selection by token cost |

**Total context space:** 6 x 5 x 4 x 4 x 3 x 3 x 3 x 3 = **19,440 unique context combinations**.

Not all combinations are equally plausible or require distinct strategy recommendations. The decision tree (TASK-004) will collapse this space into a tractable set of decision paths by using criticality as the primary branching dimension and other dimensions as secondary modifiers.

---

## Traceability

### Requirements Coverage

| Requirement | How Addressed |
|-------------|--------------|
| FR-001 | All 10 strategies referenced in strategy affinity tables and delivery mappings |
| FR-002 | Each strategy profile dimension (when to use/avoid, pairings, preconditions, outcomes) is enabled by this taxonomy's structure |
| FR-008 | Enforcement gaps identified in Dimension 6 (ENF layer mapping) -- strategies that are sole defense for semantic quality, novel violations, and context rot are identifiable via the layer-strategy delivery mapping |
| NFR-001 | Context rot impact quantified in Dimension 6 with effectiveness degradation by token count |
| NFR-005 | Taxonomy is O(1) lookup -- each dimension is a simple enumeration; no iterative computation needed |

### Acceptance Criteria Coverage

| AC | How Addressed |
|----|--------------|
| AC-1 | Taxonomy defines 8 dimensions (exceeds "at least 4"), including decision criticality (C1-C4) and enforcement layer availability |
| AC-10 | Blue Team review inputs enabled -- taxonomy provides the structural basis for context rot, portability, and token budget scenarios |
| AC-11 | Traceability to ADR-EPIC002-001 (C1-C4 levels, quality layers, token tiers) and Barrier-1 ENF-to-ADV (5-layer architecture, platform constraints, systemic risks) confirmed throughout |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | Quality Layer Composition (L0-L4), Decision Criticality Escalation (C1-C4), Strategy token budgets, Synergy/Tension pairs |
| 2 | Barrier-1 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B1-ENF-TO-ADV | 5-Layer Enforcement Architecture, Platform Constraints, Implementation Capabilities, Risk Summary (R-SYS-001 through R-SYS-004) |
| 3 | EN-303 Enabler Specification -- FEAT-004:EN-303 | Functional Requirements FR-001 through FR-011, Non-Functional Requirements NFR-001 through NFR-007, Technical Approach |
| 4 | EN-302 TASK-004 -- FEAT-004:EN-302:TASK-004 | Scoring Matrix, Strategy token costs, Mechanistic families, Composition synergy verification |
| 5 | EN-302 TASK-002 -- FEAT-004:EN-302:TASK-002 | Risk profiles per strategy, RED/YELLOW/GREEN classifications, R-001-QR (premature adversarial pressure) |

---

*Document ID: FEAT-004:EN-303:TASK-001*
*Agent: ps-architect*
*Created: 2026-02-13*
*Status: Complete*
