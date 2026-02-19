# Jerry Prompt Quality Requirements Specification

> **Document ID:** PROJ-006-REQ-001
> **Entry ID:** e-002
> **Agent:** nse-requirements (nasa-se skill)
> **Version:** 1.0.0
> **Date:** 2026-02-18
> **Status:** COMPLETE
> **NPR 7123.1D Process:** Process 2 -- Stakeholder Expectations Definition / Requirements Definition
> **Source Artifacts:**
> - `analysis/prompt-quality-rubric-taxonomy.md` (ps-architect, PROJ-006-ARCH-001, v1.0.0)
> - `synthesis/jerry-prompt-best-practices-guide.md` (ps-synthesizer, PROJ-006-SYN-001, v1.0.0)

---

> **NASA SE Disclaimer:** This document applies NASA Systems Engineering (NPR 7123.1D) rigor
> to a software framework requirements context. It adapts Process 2 (Stakeholder Expectations
> Definition) and Process 3 (Requirements Definition) terminology to the Jerry prompt quality
> domain. NASA process references are used as a quality framework, not as a claim of NASA
> program affiliation. All SHALL statements follow IEEE 830 / NPR 7123.1D conventions:
> "SHALL" indicates a mandatory requirement; "SHOULD" indicates a recommended practice;
> "MAY" indicates an optional capability.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Requirements Summary Card](#l0-requirements-summary-card) | One-page overview of all requirements with IDs and verification methods |
| [L1: Stakeholder Needs](#l1-stakeholder-needs) | STK- definitions with forward traceability to requirements |
| [L1: Core Quality Criteria Requirements (C1-C7)](#l1-core-quality-criteria-requirements-c1-c7) | SHALL statements for each rubric criterion |
| [L1: Jerry Extension Requirements (JE1-JE4)](#l1-jerry-extension-requirements-je1-je4) | SHALL statements for Jerry-specific criteria |
| [L1: Prompt Classification Taxonomy Requirements](#l1-prompt-classification-taxonomy-requirements) | SHALL statements for the 6-type taxonomy and decision tree |
| [L1: Effectiveness Tier System Requirements](#l1-effectiveness-tier-system-requirements) | SHALL statements for the 4-tier scoring system |
| [L1: Anti-Pattern Detection Requirements](#l1-anti-pattern-detection-requirements) | SHALL statements for the 8 documented anti-patterns |
| [L2: Forward Traceability Matrix](#l2-forward-traceability-matrix) | Complete STK to REQ mapping |
| [L2: Verification Cross-Reference Matrix](#l2-verification-cross-reference-matrix) | All requirements with verification methods and acceptance criteria |
| [L2: Design Rationale and Evidence Mapping](#l2-design-rationale-and-evidence-mapping) | Traceability from requirements to source evidence |

---

## L0: Requirements Summary Card

> Quick-reference card listing all requirements with their verification methods.
> Full SHALL statements and rationale in L1 sections below.

### Core Quality Criteria Requirements

| ID | Title | Criterion | Verification | STK Trace |
|----|-------|-----------|-------------|-----------|
| REQ-JPQ-001 | Task Specificity Completeness | C1 | Inspection | STK-001, STK-002 |
| REQ-JPQ-002 | Specificity Gap Measurement | C1 | Test | STK-002, STK-003 |
| REQ-JPQ-003 | Skill Routing Syntax | C2 | Test | STK-001, STK-004 |
| REQ-JPQ-004 | Agent Naming in Multi-Agent Workflows | C2 | Inspection | STK-001, STK-004 |
| REQ-JPQ-005 | Context Relevance Ratio | C3 | Analysis | STK-001, STK-002 |
| REQ-JPQ-006 | Context Redundancy Bound | C3 | Analysis | STK-001, STK-003 |
| REQ-JPQ-007 | Numeric Quality Threshold Presence | C4 | Inspection | STK-001, STK-002 |
| REQ-JPQ-008 | Quality Threshold Override | C4 | Demonstration | STK-002, STK-004 |
| REQ-JPQ-009 | Multi-Step Decomposition | C5 | Inspection | STK-001, STK-002 |
| REQ-JPQ-010 | Output Specification Completeness | C6 | Inspection | STK-001, STK-002 |
| REQ-JPQ-011 | Positive Framing Ratio | C7 | Analysis | STK-001, STK-002 |

### Jerry Extension Requirements

| ID | Title | Extension | Verification | STK Trace |
|----|-------|-----------|-------------|-----------|
| REQ-JPQ-012 | Skill Invocation Correctness | JE1 | Analysis | STK-004 |
| REQ-JPQ-013 | Agent Composition Canonical Sequence | JE2 | Analysis | STK-004 |
| REQ-JPQ-014 | Orchestration Pattern Selection | JE3 | Analysis | STK-004 |
| REQ-JPQ-015 | Quality Gate Three-Component Specification | JE4 | Inspection | STK-002, STK-004 |

### Taxonomy and Tier Requirements

| ID | Title | Category | Verification | STK Trace |
|----|-------|----------|-------------|-----------|
| REQ-JPQ-016 | Prompt Type Classification Coverage | Taxonomy | Demonstration | STK-001, STK-003 |
| REQ-JPQ-017 | Decision Tree Determinism | Taxonomy | Test | STK-001, STK-003 |
| REQ-JPQ-018 | Tier Score Boundary Definitions | Tiers | Inspection | STK-002, STK-003 |
| REQ-JPQ-019 | Tier Observable Characteristics | Tiers | Analysis | STK-002, STK-003 |
| REQ-JPQ-020 | Weighted Score Formula Consistency | Tiers | Test | STK-003 |

### Anti-Pattern Detection Requirements

| ID | Title | Category | Verification | STK Trace |
|----|-------|----------|-------------|-----------|
| REQ-JPQ-021 | Anti-Pattern Catalog Completeness | Anti-Patterns | Inspection | STK-001, STK-002 |
| REQ-JPQ-022 | Anti-Pattern Before/After Examples | Anti-Patterns | Inspection | STK-001 |
| REQ-JPQ-023 | Anti-Pattern to Criterion Traceability | Anti-Patterns | Analysis | STK-003 |

### System-Level Requirements

| ID | Title | Category | Verification | STK Trace |
|----|-------|----------|-------------|-----------|
| REQ-JPQ-024 | Rubric Self-Assessment Under 5 Minutes | Usability | Demonstration | STK-002 |
| REQ-JPQ-025 | Rubric Evolution Backward Compatibility | Maintainability | Analysis | STK-003 |

---

## L1: Stakeholder Needs

### STK-001: Prompt Structure Guidance

| Field | Value |
|-------|-------|
| **Stakeholder** | Jerry users (all experience levels) |
| **Need Statement** | Jerry users need clear, actionable guidance on how to structure prompts so that the correct skills, agents, and quality mechanisms are activated reliably. |
| **Context** | Jerry's layered architecture (CLAUDE.md, skills, agents, orchestration) is activated by specific prompt structures. Without guidance, users write prompts that bypass Jerry's quality mechanisms entirely. The best-practices guide (PROJ-006-SYN-001) documents that vague prompts without skill routing syntax (AP-01) are the highest-impact anti-pattern. |
| **Success Measure** | A user following the guidance can construct a prompt that scores Tier 3 (Proficient, >= 75/100) or higher on the rubric. |
| **Traces To** | REQ-JPQ-001, REQ-JPQ-003, REQ-JPQ-004, REQ-JPQ-005, REQ-JPQ-009, REQ-JPQ-010, REQ-JPQ-011, REQ-JPQ-016, REQ-JPQ-017, REQ-JPQ-021, REQ-JPQ-022 |

### STK-002: Measurable Quality Criteria for Self-Assessment

| Field | Value |
|-------|-------|
| **Stakeholder** | Jerry users (intermediate and advanced) |
| **Need Statement** | Jerry users need measurable, objective quality criteria that enable self-assessment of prompt quality before submission, using count-based and ratio-based metrics rather than subjective judgment. |
| **Context** | The rubric (PROJ-006-ARCH-001) defines each criterion with a measurement method (count, presence/absence, percentage) to avoid subjective scoring. Users need these methods to be formally specified so they can apply them independently. |
| **Success Measure** | Two independent raters scoring the same prompt produce scores within 5 points of each other (inter-rater reliability). |
| **Traces To** | REQ-JPQ-001, REQ-JPQ-002, REQ-JPQ-005, REQ-JPQ-007, REQ-JPQ-009, REQ-JPQ-010, REQ-JPQ-011, REQ-JPQ-015, REQ-JPQ-018, REQ-JPQ-019, REQ-JPQ-020, REQ-JPQ-021, REQ-JPQ-024 |

### STK-003: Consistent Quality Metrics for Rubric Evolution

| Field | Value |
|-------|-------|
| **Stakeholder** | Framework maintainers (Jerry developers) |
| **Need Statement** | Framework maintainers need a stable, versioned set of quality metrics with defined measurement methods so that rubric updates preserve backward compatibility and metric comparisons remain valid across versions. |
| **Context** | As Jerry evolves (new skills, new agents, new patterns), the rubric must accommodate additions without invalidating existing scores. The weighted score formula must be the single source of truth for normalization. |
| **Success Measure** | A prompt scored under rubric v1.0 produces a score within 3 points when rescored under rubric v1.x (minor versions preserve comparability). |
| **Traces To** | REQ-JPQ-002, REQ-JPQ-005, REQ-JPQ-006, REQ-JPQ-016, REQ-JPQ-017, REQ-JPQ-018, REQ-JPQ-019, REQ-JPQ-020, REQ-JPQ-023, REQ-JPQ-025 |

### STK-004: Reliable and Predictable Skill/Agent Routing

| Field | Value |
|-------|-------|
| **Stakeholder** | Jerry users composing multi-agent workflows |
| **Need Statement** | Jerry users need skill and agent routing to behave predictably and correctly, such that invoking a skill with the correct syntax and naming the correct agent reliably activates the intended cognitive mode, output format, and quality mechanisms. |
| **Context** | Jerry's architecture routes prompts through YAML activation-keywords and `/skill` syntax. Incorrect routing (wrong skill, wrong agent, wrong orchestration pattern) produces output in the wrong cognitive mode. The Jerry extensions (JE1-JE4) measure routing correctness. |
| **Success Measure** | A prompt that names a skill with `/skill` syntax and names an agent by its canonical name activates the correct agent context 100% of the time. |
| **Traces To** | REQ-JPQ-003, REQ-JPQ-004, REQ-JPQ-008, REQ-JPQ-012, REQ-JPQ-013, REQ-JPQ-014, REQ-JPQ-015 |

---

## L1: Core Quality Criteria Requirements (C1-C7)

### REQ-JPQ-001: Task Specificity Completeness

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt SHALL contain zero specificity gaps to score Exemplary (3/3) on Task Specificity (C1). A "specificity gap" is defined as any of: (a) a vague descriptor without a concrete referent (e.g., "good," "appropriate," "relevant"), (b) a sentence fragment or trailing clause that names no object, (c) a constraint range without a unit (e.g., "keep it short"), or (d) a task verb with no object (e.g., "analyze things"). |
| **Criterion** | C1 -- Task Specificity (Weight: 20%) |
| **Rationale** | Anthropic's "golden rule" (Survey Section 1.2) and the Jerry internals analysis (User Prompt Analysis: "incomplete sentence leaves scope undefined") both identify specificity gaps as the primary prompt failure mode. Task specificity has the highest weight (20%) because all other quality improvements depend on a clear task statement. |
| **Scoring Scale** | 0 gaps = score 3 (Full); 1-2 gaps = score 2 (Partial); 3-4 gaps = score 1 (Vague); 5+ gaps or no actionable task = score 0 (Absent) |
| **Verification Method** | Inspection -- Manual review of prompt text counting specificity gaps per the four-category definition |
| **Acceptance Criteria** | A prompt evaluated by two independent raters produces gap counts within 1 of each other |
| **Traces To** | STK-001, STK-002 |
| **Source** | PROJ-006-ARCH-001, Section C1 |

---

### REQ-JPQ-002: Specificity Gap Measurement Method

| Field | Value |
|-------|-------|
| **Requirement** | The rubric SHALL define exactly four categories of specificity gaps with unambiguous definitions and at least one concrete example per category, such that the measurement method produces repeatable counts across independent raters. |
| **Criterion** | C1 -- Task Specificity (measurement standardization) |
| **Rationale** | STK-002 requires measurable, objective criteria. The gap count is the primary metric for C1; its categories must be precise enough for inter-rater reliability. STK-003 requires stability across rubric versions. |
| **Four Categories** | (a) Vague descriptor without concrete referent; (b) Sentence fragment or trailing clause with no object; (c) Constraint range without unit; (d) Task verb with no object |
| **Verification Method** | Test -- Apply the four-category definition to a corpus of 10+ sample prompts; verify inter-rater gap count agreement within 1 per prompt |
| **Acceptance Criteria** | Inter-rater agreement >= 85% (exact match on gap count) across the sample corpus |
| **Traces To** | STK-002, STK-003 |
| **Source** | PROJ-006-ARCH-001, Section C1 measurement method |

---

### REQ-JPQ-003: Skill Routing Syntax

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt that requires skill invocation SHALL use the explicit `/skill-name` syntax (e.g., `/problem-solving`, `/orchestration`, `/worktracker`) for each required skill. A prompt that omits the `/` prefix for a needed skill SHALL score no higher than 2/3 on Skill Routing (C2). |
| **Criterion** | C2 -- Skill Routing (Weight: 18%) |
| **Rationale** | Jerry's YAML `activation-keywords` and explicit `/skill` invocation are the primary mechanisms by which the correct skill context is loaded (jerry-internals-investigation.md, Finding 1, P-01). Without the `/` prefix, routing relies on keyword inference, which is less reliable. |
| **Scoring Formula** | Score = (skills correctly invoked / total skills needed) * 3, rounded to nearest integer. If no skill invocation is needed, score defaults to 3. |
| **Verification Method** | Test -- Parse prompt text for `/skill-name` pattern matches; compare against task type requirements to verify all needed skills are invoked |
| **Acceptance Criteria** | Regex pattern `/[a-z-]+` identifies all skill invocations in a prompt; false positive rate < 5% on a sample corpus |
| **Traces To** | STK-001, STK-004 |
| **Source** | PROJ-006-ARCH-001, Section C2 |

---

### REQ-JPQ-004: Agent Naming in Multi-Agent Workflows

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt targeting a multi-agent workflow SHALL name each required agent by its canonical identifier (e.g., `ps-researcher`, `ps-analyst`, `orch-planner`, `ps-critic`) when the prompt specifies a particular cognitive mode, output format, or pipeline sequence. |
| **Criterion** | C2 -- Skill Routing (agent specificity component) |
| **Rationale** | Agent names map to specific XML-structured agent identities with distinct cognitive modes, model tiers, and output frameworks. Unnamed references force Jerry to infer the agent, which may select the wrong cognitive mode (AP-04: Cognitive Mode Mismatch). |
| **Verification Method** | Inspection -- Review prompt text for canonical agent identifiers; cross-reference against the agent roster in the invoked skill's SKILL.md |
| **Acceptance Criteria** | Every agent named in the prompt exists in the invoked skill's agent roster; no phantom agent names present |
| **Traces To** | STK-001, STK-004 |
| **Source** | PROJ-006-ARCH-001, Section C2; PROJ-006-SYN-001, Agent Composition Guidelines |

---

### REQ-JPQ-005: Context Relevance Ratio

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt SHALL have zero absent context elements (context that would change Claude's behavior if present but is missing) to score Exemplary (3/3) on Context Provision (C3). Each context element SHALL be classifiable as Relevant, Redundant, or Absent using the following definitions: Relevant = would change Claude's behavior if absent; Redundant = already known from session/CLAUDE.md/skill spec; Absent = should be present but is not. |
| **Criterion** | C3 -- Context Provision (Weight: 15%) |
| **Rationale** | Survey Section 1.2 identifies task purpose, audience, workflow position, and success criteria as the four context dimensions that improve performance. Jerry's persistent context layer (Layer 5: CLAUDE.md) already handles background; user prompts need only supply what that layer does not provide. |
| **Scoring Scale** | 0 absent AND < 20% redundant = score 3; <= 1 absent OR 20-40% redundant = score 2; 2-3 absent OR 40-60% redundant = score 1; >= 4 absent OR > 60% redundant = score 0 |
| **Verification Method** | Analysis -- Enumerate all context elements in the prompt; classify each against the three-category system; compute absent count and redundancy ratio |
| **Acceptance Criteria** | Context element classification produces consistent results when the evaluator has access to the session's CLAUDE.md and loaded skill specs |
| **Traces To** | STK-001, STK-002, STK-003 |
| **Source** | PROJ-006-ARCH-001, Section C3 |

---

### REQ-JPQ-006: Context Redundancy Bound

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt SHALL maintain a redundant context ratio below 0.20 (less than 20% of all context elements are redundant with information already present in the session's auto-loaded context) to score Exemplary (3/3) on Context Provision (C3). |
| **Criterion** | C3 -- Context Provision (redundancy component) |
| **Rationale** | Jerry's architecture fights context rot by keeping CLAUDE.md sparse and loading skill context selectively. Prompts that repeat information already loaded by auto-loaded rules or skill specs waste shared context window budget (jerry-internals-investigation.md, Layer 5). |
| **Verification Method** | Analysis -- Compare prompt context elements against CLAUDE.md and loaded skill specs to identify redundancies; compute ratio |
| **Acceptance Criteria** | Redundancy ratio calculation is reproducible given the same session context |
| **Traces To** | STK-001, STK-003 |
| **Source** | PROJ-006-ARCH-001, Section C3; PROJ-006-SYN-001, AP-05 |

---

### REQ-JPQ-007: Numeric Quality Threshold Presence

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt targeting quality-sensitive tasks (architecture decisions, security analysis, research synthesis informing real decisions) SHALL include at least one numeric quality threshold (e.g., `>= 0.92`, `> 90%`) that specifies the acceptance bar for task completion or phase gate passage. |
| **Criterion** | C4 -- Quality Specification (Weight: 15%) |
| **Rationale** | Survey Section 6.1 establishes that a clear definition of success criteria is prerequisite to meaningful prompt engineering. Jerry's ps-critic circuit breaker operates on a numeric `quality_score`; without a numeric threshold in the user prompt, the circuit breaker defaults to 0.85 (generic), not the user's actual quality bar (jerry-internals-investigation.md, Finding 7, P-07). |
| **Quality Signal Points** | Numeric threshold = 2 points; Named rubric/checklist = 2 points; Verbal descriptor with concrete referent = 1 point; No signal = 0 points. Total max = 4. Map: 4 = score 3; 2-3 = score 2; 1 = score 1; 0 = score 0 |
| **Verification Method** | Inspection -- Scan prompt for numeric patterns (decimal thresholds, percentages) and named review mechanisms (ps-critic, adversarial review) |
| **Acceptance Criteria** | Numeric threshold extraction via pattern matching identifies all thresholds present; false negative rate < 5% |
| **Traces To** | STK-001, STK-002 |
| **Source** | PROJ-006-ARCH-001, Section C4 |

---

### REQ-JPQ-008: Quality Threshold Override of Default

| Field | Value |
|-------|-------|
| **Requirement** | When a Jerry prompt specifies a numeric quality threshold, that threshold SHALL override the ps-critic default `acceptance_threshold` of 0.85 for the scope of the invoked workflow. The override SHALL apply to all phase gates within the workflow unless phase-specific thresholds are provided. |
| **Criterion** | C4 -- Quality Specification (behavioral requirement) |
| **Rationale** | The ps-critic circuit breaker schema (jerry-internals-investigation.md, Finding 7) defaults to `quality_score >= 0.85`. The Salesforce prompt's `>=0.92` demonstrates that user-specified thresholds override this default. This override mechanism must be reliable for STK-004. |
| **Verification Method** | Demonstration -- Submit a prompt with a threshold of `>= 0.90` to a workflow that invokes ps-critic; verify that ps-critic uses 0.90 (not 0.85) as the circuit breaker stop condition |
| **Acceptance Criteria** | ps-critic quality gate records show the user-specified threshold, not the default 0.85 |
| **Traces To** | STK-002, STK-004 |
| **Source** | PROJ-006-ARCH-001, Section C4; PROJ-006-SYN-001, Quality Indicators section |

---

### REQ-JPQ-009: Multi-Step Decomposition

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt with more than one distinct deliverable or workflow phase SHALL explicitly decompose the task into named phases, ordered steps, or agent pipelines. Decomposition elements include: (a) explicitly named phases (e.g., "Phase 1: Research"), (b) explicitly named agent sequences (e.g., "ps-researcher then ps-analyst"), and (c) explicit sync barriers or gates (e.g., "only proceed after the spike is created"). A prompt with 2+ decomposition elements SHALL score 3/3 on Decomposition (C5). |
| **Criterion** | C5 -- Decomposition (Weight: 12%) |
| **Rationale** | Survey Section 3.1 identifies prompt chaining as producing dramatic accuracy improvements. The Salesforce prompt scores 2/3 (not 3/3) because its phase sequence is implied but not named (jerry-internals-investigation.md, User Prompt Analysis). |
| **Scoring Scale** | 2+ decomposition elements = score 3; exactly 1 = score 2; implied but not explicit = score 1; monolithic = score 0. Single-deliverable prompts (Atomic Query type) score 3 automatically. |
| **Verification Method** | Inspection -- Count named phases, named agent sequences, and explicit gates in the prompt text |
| **Acceptance Criteria** | Decomposition element count is unambiguous for prompts where phases/agents are explicitly named |
| **Traces To** | STK-001, STK-002 |
| **Source** | PROJ-006-ARCH-001, Section C5 |

---

### REQ-JPQ-010: Output Specification Completeness

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt SHALL specify the expected output along three sub-components: (a) Type -- the output artifact type is named (e.g., "research report," "ADR," "ORCHESTRATION_PLAN.md"), (b) Location -- the file path or artifact directory is stated or inferrable from skill invocation, and (c) Structure -- the required sections, format (markdown, YAML, JSON), or template is referenced. A prompt with all three sub-components SHALL score 3/3 on Output Specification (C6). |
| **Criterion** | C6 -- Output Specification (Weight: 12%) |
| **Rationale** | Survey Section 6.2 establishes output format specification as a quality signal that prevents superfluous text. Jerry's Mandatory Persistence Protocol (Finding 5, P-05) requires a concrete file path; prompts that omit this force Claude to use default paths, which may not match user intent. |
| **Scoring Scale** | All three = score 3; two of three = score 2; one of three = score 1; none = score 0 |
| **Verification Method** | Inspection -- Check prompt for presence of artifact type name, file path or directory reference, and format/template/section specification |
| **Acceptance Criteria** | Each sub-component is binary present/absent; total score is the sum |
| **Traces To** | STK-001, STK-002 |
| **Source** | PROJ-006-ARCH-001, Section C6 |

---

### REQ-JPQ-011: Positive Framing Ratio

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt SHALL state instructions in positive framing (what to do) rather than negative framing (what to avoid). The negative instruction ratio (negative clauses / total instructional clauses) SHALL be 0.00 (zero negatives) to score Exemplary (3/3) on Positive Framing (C7). |
| **Criterion** | C7 -- Positive Framing (Weight: 8%) |
| **Rationale** | Survey Section 2 (DAIR.AI: "say what to do instead of what to avoid") and Jerry Anti-Patterns table (jerry-internals-investigation.md) identify negative framing as a remedial anti-pattern. This criterion has the lowest weight (8%) because the other six criteria have larger impact on Jerry-specific output quality. |
| **Scoring Scale** | 0% negative = score 3; 1-20% negative = score 2; 21-40% negative = score 1; > 40% negative = score 0 |
| **Verification Method** | Analysis -- Classify all instructional clauses as positive or negative; compute the negative ratio |
| **Acceptance Criteria** | Clause classification distinguishes between positive ("use X," "produce Y") and negative ("don't use X," "avoid Y," "never Z") forms |
| **Traces To** | STK-001, STK-002 |
| **Source** | PROJ-006-ARCH-001, Section C7 |

---

## L1: Jerry Extension Requirements (JE1-JE4)

### REQ-JPQ-012: Skill Invocation Correctness

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt SHALL invoke only skills whose activation-keyword domain and agent capabilities match the task type. A skill invocation is correct if and only if: (a) the task type matches the skill's activation keywords defined in its SKILL.md YAML frontmatter, (b) the invoked skill has an agent capable of producing the required output, and (c) no skill is invoked whose output is not used in the workflow. A prompt with all invocations correct SHALL score 3/3 on Skill Invocation Correctness (JE1). |
| **Extension** | JE1 -- Skill Invocation Correctness |
| **Rationale** | Skills are not interchangeable; wrong invocation loads incorrect agent prompts and context. Invoking `/nasa-se` for a simple code review task or `/orchestration` for a single-step task introduces disproportionate overhead (PROJ-006-ARCH-001, JE1 evidence base). |
| **Scoring Scale** | 0 wrong skills = score 3; 1 incorrect/superfluous = score 2; 2 incorrect/superfluous = score 1; all incorrect or no skills when needed = score 0 |
| **Verification Method** | Analysis -- Cross-reference each invoked skill against its SKILL.md activation-keywords and the task's requirements |
| **Acceptance Criteria** | Every skill invocation in the prompt matches an activation keyword or explicit need from the task description |
| **Traces To** | STK-004 |
| **Source** | PROJ-006-ARCH-001, Section JE1 |

---

### REQ-JPQ-013: Agent Composition Canonical Sequence

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt specifying a multi-agent pipeline SHALL follow the canonical agent sequence defined by the `next_agent_hint` routing: `ps-researcher -> ps-analyst -> [ps-architect | ps-synthesizer] -> ps-validator -> ps-reporter`. Violations include: skipped agents that would improve quality for complex tasks, reversed order, or using a heavy agent (ps-architect/opus) for a task appropriate to a light agent (ps-validator/haiku). A prompt with zero violations SHALL score 3/3 on Agent Composition Quality (JE2). |
| **Extension** | JE2 -- Agent Composition Quality |
| **Rationale** | The `next_agent_hint` routing embedded in agent state schemas defines an implicit canonical pipeline. Deviations from this pipeline produce output in the wrong cognitive mode or at the wrong model tier, degrading quality (jerry-internals-investigation.md, Extended Agent Coverage). |
| **Scoring Scale** | 0 violations = score 3; 1 violation = score 2; 2 violations = score 1; completely non-canonical or no sequencing for multi-agent task = score 0 |
| **Verification Method** | Analysis -- Compare the stated agent sequence against the canonical pipeline; count deviations |
| **Acceptance Criteria** | Agent sequence comparison uses the documented canonical pipeline as the reference baseline |
| **Traces To** | STK-004 |
| **Source** | PROJ-006-ARCH-001, Section JE2 |

---

### REQ-JPQ-014: Orchestration Pattern Selection

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt requiring inter-agent coordination SHALL select an orchestration workflow pattern that matches the task's complexity and structure. The orchestration PLAYBOOK defines 8 patterns; the prompt SHALL either (a) name the pattern explicitly (score 3/3) or (b) describe the task characteristics such that the correct pattern is inferrable (score 2/3). A prompt that names a pattern not matching its task characteristics SHALL score 1/3. A prompt requiring coordination but specifying no orchestration pattern SHALL score 0/3 on Orchestration Pattern Selection (JE3). |
| **Extension** | JE3 -- Orchestration Pattern Selection |
| **Key Patterns** | Sequential Pipeline (strict ordering), Parallel with Barrier Sync (independent subtasks with shared next step), Adversarial Critique Loop (quality-sensitive with devil's advocate review), Generator-Critic-Revise (iterative improvement with quality gate) |
| **Rationale** | Mismatched patterns waste resources. Requesting adversarial critique at every phase when the workflow is parallel analyses needing only one shared review triples critique cost (PROJ-006-ARCH-001, JE3 failure mode example). |
| **Verification Method** | Analysis -- Compare the named or implied orchestration pattern against the task's structural characteristics |
| **Acceptance Criteria** | Pattern-task match is deterministic given the task's characteristics (ordering requirements, independence of subtasks, quality sensitivity) |
| **Traces To** | STK-004 |
| **Source** | PROJ-006-ARCH-001, Section JE3 |

---

### REQ-JPQ-015: Quality Gate Three-Component Specification

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry prompt invoking ps-critic quality gates SHALL specify all three quality gate components to score 3/3 on Quality Gate Specification (JE4): (a) a numeric threshold (e.g., `>= 0.92`), (b) the phases at which critique fires (e.g., "after research and after analysis"), and (c) criterion weighting or a named rubric reference (optional; defaults exist). Omitting the threshold causes ps-critic to default to 0.85; omitting phase specification causes critique to fire at unknown points; omitting criterion weighting applies equal weights. |
| **Extension** | JE4 -- Quality Gate Specification |
| **Scoring Scale** | Threshold + phases + criterion weighting = score 3; Threshold + phases = score 2; Threshold only or phases only = score 1; None = score 0 |
| **Rationale** | The ps-critic circuit breaker schema requires `quality_score >= acceptance_threshold` to stop and needs to know when to fire (which phases). Without all three components, the quality gate operates on defaults that may not match user intent (jerry-internals-investigation.md, Finding 7, P-07). |
| **Verification Method** | Inspection -- Check prompt for numeric threshold pattern, phase gate list, and criterion weighting or rubric reference |
| **Acceptance Criteria** | Each sub-component is binary present/absent; total score is the sum of present components |
| **Traces To** | STK-002, STK-004 |
| **Source** | PROJ-006-ARCH-001, Section JE4 |

---

## L1: Prompt Classification Taxonomy Requirements

### REQ-JPQ-016: Prompt Type Classification Coverage

| Field | Value |
|-------|-------|
| **Requirement** | The prompt classification taxonomy SHALL define exactly 6 prompt types that collectively cover the Jerry use-case space: (1) Atomic Query, (2) Implementation Task, (3) Research Spike, (4) Multi-Skill Orchestration, (5) Validation Gate, and (6) Decision Analysis. Each type SHALL have: (a) a description, (b) a "When to Use" clause, (c) key characteristics, (d) the top rubric criteria for that type, (e) at least one example, and (f) at least one anti-pattern. |
| **Category** | Taxonomy |
| **Rationale** | Different prompt types emphasize different rubric criteria. Without a classification system, users cannot determine which criteria to prioritize for their task. The 6 types were derived from the intersection of Jerry skill capabilities and observed user prompt patterns (PROJ-006-ARCH-001, Taxonomy Evidence Map). |
| **Verification Method** | Demonstration -- Classify a corpus of 20+ real Jerry prompts using the taxonomy; verify that every prompt maps to exactly one type |
| **Acceptance Criteria** | 100% of prompts in the corpus classify to exactly one type; zero prompts are unclassifiable |
| **Traces To** | STK-001, STK-003 |
| **Source** | PROJ-006-ARCH-001, Prompt Classification Taxonomy section |

---

### REQ-JPQ-017: Decision Tree Determinism

| Field | Value |
|-------|-------|
| **Requirement** | The prompt classification taxonomy SHALL include a decision tree that produces a single, deterministic prompt type classification for any given Jerry prompt. The decision tree SHALL consist of binary (yes/no) decision nodes, each testing for an observable characteristic of the prompt (e.g., "Does the prompt invoke exactly one skill?"). The tree SHALL have exactly 6 leaf nodes, one per prompt type, with a fallback classification for prompts that match no leaf (default: Type 2 with missing output specification). |
| **Category** | Taxonomy |
| **Decision Tree Structure** | Node 1: Factual answer, no persisted artifact? -> Type 1. Node 2: Exactly one skill, one artifact? -> Type 2 (or Type 3 if /problem-solving + ps-researcher). Node 3: /problem-solving + ps-researcher primary? -> Type 3. Node 4: Two+ skills or orch-planner named? -> Type 4. Node 5: Existing artifact + binary criteria? -> Type 5. Node 6: 2+ options with evaluation dimensions? -> Type 6. Fallback: Type 2. |
| **Rationale** | STK-001 requires clear guidance; a non-deterministic classification system forces users to make subjective judgments about prompt type, undermining the objectivity of subsequent criterion weighting. |
| **Verification Method** | Test -- Apply the decision tree to 20+ sample prompts; verify that every prompt reaches exactly one leaf node and that two independent evaluators classify the same prompt to the same type |
| **Acceptance Criteria** | Inter-rater agreement on prompt type classification >= 95% |
| **Traces To** | STK-001, STK-003 |
| **Source** | PROJ-006-ARCH-001, Prompt Type Decision Guide |

---

## L1: Effectiveness Tier System Requirements

### REQ-JPQ-018: Tier Score Boundary Definitions

| Field | Value |
|-------|-------|
| **Requirement** | The effectiveness tier system SHALL define exactly 4 tiers with non-overlapping, exhaustive score boundaries covering the full 0-100 raw score range: Tier 4 Exemplary (90-100, normalized 0.90-1.00), Tier 3 Proficient (75-89, normalized 0.75-0.89), Tier 2 Developing (50-74, normalized 0.50-0.74), Tier 1 Inadequate (0-49, normalized 0.00-0.49). Every possible raw score SHALL map to exactly one tier. |
| **Category** | Tiers |
| **Rationale** | STK-002 requires measurable criteria for self-assessment. Overlapping or gapped tier boundaries would create ambiguity. The four tiers were derived from the rubric's weighted score formula and validated against the Salesforce prompt scored example (76.3 = Tier 3). |
| **Verification Method** | Inspection -- Verify boundary definitions are non-overlapping and exhaustive over [0, 100] |
| **Acceptance Criteria** | Union of tier ranges = [0, 100]; intersection of any two tier ranges = empty set |
| **Traces To** | STK-002, STK-003 |
| **Source** | PROJ-006-ARCH-001, Effectiveness Tier Definitions |

---

### REQ-JPQ-019: Tier Observable Characteristics

| Field | Value |
|-------|-------|
| **Requirement** | Each effectiveness tier SHALL be defined by a set of observable characteristics that describe the prompt's structural properties at that quality level. Observable characteristics SHALL be verifiable without executing the prompt (they describe the prompt text, not its output). Each tier SHALL include at minimum: (a) the expected number of specificity gaps, (b) skill invocation quality, (c) quality specification level, (d) decomposition level, (e) output specification level, and (f) framing quality. |
| **Category** | Tiers |
| **Observable Characteristics per Tier** | Tier 4: Zero specificity gaps, all skills with exact syntax, numeric quality threshold, named phases, fully specified output, all positive framing. Tier 3: 1-2 gaps, core skills invoked, quality mechanism present, sequence implied, output partially specified, positive dominant. Tier 2: 3-4 gaps, partial/absent skill invocation, verbal quality only, implicit decomposition, type only output, mixed framing. Tier 1: 5+ gaps, no skill invocation, no quality signal, no decomposition, no output spec, negative dominant. |
| **Rationale** | Observable characteristics enable users to quickly estimate their prompt's tier without computing a full numeric score, satisfying STK-002's self-assessment need. |
| **Verification Method** | Analysis -- Verify that each listed observable maps to a specific rubric criterion and score level |
| **Acceptance Criteria** | Every observable characteristic can be verified by inspection of the prompt text alone |
| **Traces To** | STK-002, STK-003 |
| **Source** | PROJ-006-ARCH-001, Tier 4/3/2/1 Observable Characteristics tables |

---

### REQ-JPQ-020: Weighted Score Formula Consistency

| Field | Value |
|-------|-------|
| **Requirement** | The rubric SHALL use a single, deterministic weighted score formula as the sole method for computing prompt quality scores. The formula SHALL be: `final_score = sum(criterion_raw_score / 3 * criterion_weight)` where each `criterion_raw_score` is an integer in [0, 3] and `criterion_weight` is the percentage weight for that criterion. The normalized score SHALL be `normalized_score = final_score / 100`. The sum of all criterion weights SHALL equal exactly 100%. |
| **Category** | Tiers (scoring) |
| **Criterion Weights** | C1: 20%, C2: 18%, C3: 15%, C4: 15%, C5: 12%, C6: 12%, C7: 8%. Total: 100%. |
| **Rationale** | STK-003 requires consistent metrics for rubric evolution. A single formula ensures all scores are comparable. The weights reflect relative importance in a Jerry context, with evidence-based justification in the rubric's L2 section. |
| **Verification Method** | Test -- Compute the score for the documented Salesforce prompt worked example using the formula; verify the result matches the documented 76.3 |
| **Acceptance Criteria** | Formula produces 76.3 (within rounding tolerance of +/- 0.5) for the Salesforce prompt with the documented raw scores: C1=2, C2=3, C3=2, C4=3, C5=2, C6=1, C7=3 |
| **Traces To** | STK-003 |
| **Source** | PROJ-006-ARCH-001, Rubric Overview and Worked Example |

---

## L1: Anti-Pattern Detection Requirements

### REQ-JPQ-021: Anti-Pattern Catalog Completeness

| Field | Value |
|-------|-------|
| **Requirement** | The rubric SHALL document at least 8 anti-patterns that degrade Jerry prompt quality, each with: (a) a unique identifier (AP-NN), (b) a descriptive title, (c) an explanation of why it fails (linking to the specific Jerry architectural mechanism that is bypassed or misused), (d) a "Before" example showing the anti-pattern, and (e) an "After" example showing the corrected version. Anti-patterns SHALL be ordered by impact (highest-impact first). |
| **Category** | Anti-Patterns |
| **Documented Anti-Patterns** | AP-01: Vague Directives Without Skill Routing (highest impact). AP-02: Missing Quality Thresholds. AP-03: Monolithic Prompts Without Decomposition. AP-04: Cognitive Mode Mismatch. AP-05: Context Overload (Irrelevant Background). AP-06: Incomplete Clause Specification. AP-07: Conflicting Instructions Across Skill Boundaries (hypothesis-status). AP-08: Missing Output Specification. |
| **Rationale** | STK-001 requires clear guidance; anti-patterns provide the "what not to do" counterpart to positive structural guidance. Before/after examples are the most effective teaching format (Survey Section 4, multishot prompting). |
| **Verification Method** | Inspection -- Verify the catalog contains all 8 anti-patterns with all 5 required fields |
| **Acceptance Criteria** | 8/8 anti-patterns documented; each has all 5 fields populated; hypothesis-status items are flagged |
| **Traces To** | STK-001, STK-002 |
| **Source** | PROJ-006-SYN-001, Anti-Patterns Section |

---

### REQ-JPQ-022: Anti-Pattern Before/After Examples

| Field | Value |
|-------|-------|
| **Requirement** | Each documented anti-pattern SHALL include a Before example (exhibiting the anti-pattern) and an After example (corrected version). The After example SHALL score at least 2 tiers higher than the Before example on the criterion most affected by that anti-pattern, or SHALL score Tier 3+ if the Before example scores Tier 1. The After example SHALL include annotation explaining what changed and why. |
| **Category** | Anti-Patterns |
| **Rationale** | Before/after pairs demonstrate the concrete impact of anti-patterns and provide actionable remediation patterns. Annotations connect the correction to specific rubric criteria, reinforcing the quality model. |
| **Verification Method** | Inspection -- Score both Before and After examples using the rubric; verify the tier improvement meets the 2-tier or Tier 3+ threshold |
| **Acceptance Criteria** | All 8 After examples score at minimum Tier 3 on the affected criterion |
| **Traces To** | STK-001 |
| **Source** | PROJ-006-SYN-001, Anti-Patterns Section (AP-01 through AP-08) |

---

### REQ-JPQ-023: Anti-Pattern to Criterion Traceability

| Field | Value |
|-------|-------|
| **Requirement** | Each anti-pattern SHALL trace to at least one rubric criterion (C1-C7) or Jerry extension (JE1-JE4) that it most degrades. The traceability SHALL be documented in a mapping table showing which criterion's score is most reduced by the anti-pattern. |
| **Category** | Anti-Patterns |
| **Anti-Pattern to Criterion Map** | AP-01 -> C2 (Skill Routing); AP-02 -> C4 (Quality Specification), JE4 (Quality Gate Specification); AP-03 -> C5 (Decomposition); AP-04 -> JE1 (Skill Invocation Correctness), JE2 (Agent Composition); AP-05 -> C3 (Context Provision); AP-06 -> C1 (Task Specificity); AP-07 -> JE1 (Skill Invocation Correctness); AP-08 -> C6 (Output Specification) |
| **Rationale** | STK-003 requires consistent metrics for rubric evolution. Anti-pattern-to-criterion traceability enables maintainers to assess coverage: every criterion should be protected by at least one documented anti-pattern, and every anti-pattern should degrade at least one criterion. |
| **Verification Method** | Analysis -- Verify that every criterion (C1-C7, JE1-JE4) is the target of at least one anti-pattern; verify that every anti-pattern maps to at least one criterion |
| **Acceptance Criteria** | Coverage: 11/11 criteria have at least one anti-pattern; 8/8 anti-patterns have at least one criterion |
| **Traces To** | STK-003 |
| **Source** | PROJ-006-ARCH-001 and PROJ-006-SYN-001, synthesized |

---

## L1: System-Level Requirements

### REQ-JPQ-024: Rubric Self-Assessment Under 5 Minutes

| Field | Value |
|-------|-------|
| **Requirement** | A Jerry user SHALL be able to score any prompt using the Quick-Reference Rubric Card in under 5 minutes, without consulting the full rubric documentation. The Quick-Reference Card SHALL contain: (a) all 7 criteria with weights and quick tests, (b) the tier lookup table, and (c) the prompt type lookup table, all on a single screen/page. |
| **Category** | Usability |
| **Rationale** | STK-002 requires self-assessment capability. A rubric that takes more than 5 minutes discourages adoption. The L0 Quick-Reference Rubric Card was designed for this purpose (PROJ-006-ARCH-001, L0 section). |
| **Verification Method** | Demonstration -- Have 3 users unfamiliar with the rubric score a prompt using only the Quick-Reference Card; measure time to completion |
| **Acceptance Criteria** | Median time to score a prompt <= 5 minutes; all 3 users produce scores within 10 points of each other |
| **Traces To** | STK-002 |
| **Source** | PROJ-006-ARCH-001, L0 Quick-Reference Rubric Card |

---

### REQ-JPQ-025: Rubric Evolution Backward Compatibility

| Field | Value |
|-------|-------|
| **Requirement** | Minor version updates to the rubric (v1.x) SHALL preserve backward compatibility such that a prompt scored under v1.0 produces a score within 3 points when rescored under v1.x. Major version updates (v2.0+) MAY change criterion weights, add or remove criteria, or redefine tier boundaries, but SHALL document all changes in a migration guide. |
| **Category** | Maintainability |
| **Rationale** | STK-003 requires stable metrics for rubric evolution. Without backward compatibility, historical scores become meaningless, undermining longitudinal quality tracking. |
| **Verification Method** | Analysis -- Rescore a reference corpus of 5 prompts under both the old and new rubric versions; compute score deltas |
| **Acceptance Criteria** | All 5 reference prompts have score deltas <= 3 points for minor version updates |
| **Traces To** | STK-003 |
| **Source** | PROJ-006-ARCH-001, L2 Design Rationale; STK-003 success measure |

---

## L2: Forward Traceability Matrix

### Stakeholder Need to Requirement Mapping

| Stakeholder Need | Requirements |
|-----------------|-------------|
| **STK-001**: Prompt structure guidance | REQ-JPQ-001, REQ-JPQ-003, REQ-JPQ-004, REQ-JPQ-005, REQ-JPQ-009, REQ-JPQ-010, REQ-JPQ-011, REQ-JPQ-016, REQ-JPQ-017, REQ-JPQ-021, REQ-JPQ-022 |
| **STK-002**: Measurable quality criteria | REQ-JPQ-001, REQ-JPQ-002, REQ-JPQ-005, REQ-JPQ-007, REQ-JPQ-008, REQ-JPQ-009, REQ-JPQ-010, REQ-JPQ-011, REQ-JPQ-015, REQ-JPQ-018, REQ-JPQ-019, REQ-JPQ-020, REQ-JPQ-021, REQ-JPQ-024 |
| **STK-003**: Consistent metrics for rubric evolution | REQ-JPQ-002, REQ-JPQ-005, REQ-JPQ-006, REQ-JPQ-016, REQ-JPQ-017, REQ-JPQ-018, REQ-JPQ-019, REQ-JPQ-020, REQ-JPQ-023, REQ-JPQ-025 |
| **STK-004**: Reliable skill/agent routing | REQ-JPQ-003, REQ-JPQ-004, REQ-JPQ-008, REQ-JPQ-012, REQ-JPQ-013, REQ-JPQ-014, REQ-JPQ-015 |

### Coverage Analysis

| Stakeholder Need | Requirement Count | Criterion Coverage |
|-----------------|-------------------|-------------------|
| STK-001 | 11 requirements | C1, C2, C3, C5, C6, C7, Taxonomy, Anti-Patterns |
| STK-002 | 14 requirements | C1, C3, C4, C5, C6, C7, JE4, Tiers, Anti-Patterns, Usability |
| STK-003 | 10 requirements | C1, C3, Taxonomy, Tiers, Anti-Patterns, Maintainability |
| STK-004 | 7 requirements | C2, C4, JE1, JE2, JE3, JE4 |

All 4 stakeholder needs are traced to at least 7 requirements. All 25 requirements trace to at least 1 stakeholder need. No orphan requirements exist.

---

## L2: Verification Cross-Reference Matrix

### Verification Method Distribution

| Method | Count | Requirements |
|--------|-------|-------------|
| **Inspection** | 10 | REQ-JPQ-001, REQ-JPQ-004, REQ-JPQ-007, REQ-JPQ-009, REQ-JPQ-010, REQ-JPQ-015, REQ-JPQ-018, REQ-JPQ-021, REQ-JPQ-022 |
| **Test** | 5 | REQ-JPQ-002, REQ-JPQ-003, REQ-JPQ-017, REQ-JPQ-020 |
| **Analysis** | 8 | REQ-JPQ-005, REQ-JPQ-006, REQ-JPQ-011, REQ-JPQ-012, REQ-JPQ-013, REQ-JPQ-014, REQ-JPQ-019, REQ-JPQ-023, REQ-JPQ-025 |
| **Demonstration** | 3 | REQ-JPQ-008, REQ-JPQ-016, REQ-JPQ-024 |

### Verification Method Definitions (per NPR 7123.1D)

| Method | Definition | When Used |
|--------|-----------|-----------|
| **Inspection** | Visual examination of the prompt text or rubric documentation to verify presence/absence of required elements. No execution required. | Structural requirements where presence/absence is deterministic |
| **Test** | Execution of a defined procedure with quantitative pass/fail criteria. Produces repeatable results. | Measurement method validation, formula verification, pattern matching |
| **Analysis** | Evaluation using models, calculations, or documented reasoning. Requires evaluator judgment guided by defined criteria. | Ratio calculations, sequence comparisons, coverage assessments |
| **Demonstration** | Execution of the system (rubric applied to real prompts) to verify operational capability. | End-to-end usability, threshold override behavior, classification coverage |

### Full Verification Matrix

| Req ID | Method | Acceptance Criteria Summary | Priority |
|--------|--------|----------------------------|----------|
| REQ-JPQ-001 | Inspection | Gap counts agree within 1 between raters | HIGH |
| REQ-JPQ-002 | Test | Inter-rater agreement >= 85% on 10+ prompts | HIGH |
| REQ-JPQ-003 | Test | `/skill-name` regex < 5% false positive rate | HIGH |
| REQ-JPQ-004 | Inspection | All named agents exist in skill roster | HIGH |
| REQ-JPQ-005 | Analysis | Context classification consistent with session context | MEDIUM |
| REQ-JPQ-006 | Analysis | Redundancy ratio reproducible given same session | MEDIUM |
| REQ-JPQ-007 | Inspection | Numeric threshold extraction < 5% false negative | HIGH |
| REQ-JPQ-008 | Demonstration | ps-critic uses user threshold, not 0.85 default | HIGH |
| REQ-JPQ-009 | Inspection | Decomposition element count unambiguous | MEDIUM |
| REQ-JPQ-010 | Inspection | 3 binary sub-components scored correctly | MEDIUM |
| REQ-JPQ-011 | Analysis | Clause classification distinguishes positive/negative | LOW |
| REQ-JPQ-012 | Analysis | Skill-task match verified against SKILL.md | HIGH |
| REQ-JPQ-013 | Analysis | Sequence compared against canonical pipeline | MEDIUM |
| REQ-JPQ-014 | Analysis | Pattern-task match deterministic | MEDIUM |
| REQ-JPQ-015 | Inspection | 3 binary sub-components scored correctly | HIGH |
| REQ-JPQ-016 | Demonstration | 100% classification on 20+ prompt corpus | HIGH |
| REQ-JPQ-017 | Test | Inter-rater type agreement >= 95% | HIGH |
| REQ-JPQ-018 | Inspection | Tier ranges non-overlapping and exhaustive | HIGH |
| REQ-JPQ-019 | Analysis | Observables map to criterion score levels | MEDIUM |
| REQ-JPQ-020 | Test | Salesforce example scores 76.3 +/- 0.5 | HIGH |
| REQ-JPQ-021 | Inspection | 8/8 anti-patterns with 5/5 fields each | MEDIUM |
| REQ-JPQ-022 | Inspection | After examples score Tier 3+ on affected criterion | MEDIUM |
| REQ-JPQ-023 | Analysis | 11/11 criteria covered; 8/8 anti-patterns mapped | MEDIUM |
| REQ-JPQ-024 | Demonstration | Median scoring time <= 5 minutes | MEDIUM |
| REQ-JPQ-025 | Analysis | Score deltas <= 3 points for minor versions | LOW |

---

## L2: Design Rationale and Evidence Mapping

### Requirement to Evidence Traceability

| Req ID | Source Criterion | Primary Evidence | Secondary Evidence |
|--------|-----------------|-----------------|-------------------|
| REQ-JPQ-001 | C1 | Survey Section 1.2 (Anthropic "golden rule"); User Prompt Analysis (trailing fragment gap) | DAIR.AI General Tips |
| REQ-JPQ-002 | C1 | PROJ-006-ARCH-001 measurement method definition | STK-002 inter-rater reliability need |
| REQ-JPQ-003 | C2 | jerry-internals P-01 (YAML activation-keywords) | Survey Section 3.2 (skill discovery) |
| REQ-JPQ-004 | C2 | prompt-pattern-analysis.md, Category 1 Correlation Map | jerry-internals User Prompt Analysis |
| REQ-JPQ-005 | C3 | Survey Section 1.2 (four context dimensions) | Layer 5/CLAUDE.md (persistent context) |
| REQ-JPQ-006 | C3 | jerry-internals Layer 5 analysis | PROJ-006-SYN-001 AP-05 |
| REQ-JPQ-007 | C4 | Survey Section 6.1 (success criteria); jerry-internals P-07 circuit breaker | User Prompt Analysis (>=0.92 threshold) |
| REQ-JPQ-008 | C4 | jerry-internals Finding 7 (circuit_breaker stop_conditions) | PROJ-006-SYN-001 Quality Indicators section |
| REQ-JPQ-009 | C5 | Survey Section 3.1 (prompt chaining accuracy improvements) | User Prompt Analysis ("implicit scope" gap) |
| REQ-JPQ-010 | C6 | Survey Section 6.2 (output format as quality signal) | jerry-internals P-05 (mandatory persistence path) |
| REQ-JPQ-011 | C7 | Survey Section 2 (DAIR.AI "say what to do") | jerry-internals anti-patterns table |
| REQ-JPQ-012 | JE1 | jerry-internals P-01 (activation-keywords guide skill selection) | PROJ-006-ARCH-001 JE1 |
| REQ-JPQ-013 | JE2 | jerry-internals Extended Agent Coverage (next_agent_hint routing) | PROJ-006-ARCH-001 JE2 |
| REQ-JPQ-014 | JE3 | jerry-internals P-07 (circuit breaker schema, critique modes) | PROJ-006-ARCH-001 JE3 |
| REQ-JPQ-015 | JE4 | jerry-internals Finding 7 (ps-critic circuit breaker requires threshold + phases) | PROJ-006-ARCH-001 JE4 |
| REQ-JPQ-016 | Taxonomy | PROJ-006-ARCH-001 Taxonomy Evidence Map | jerry-internals skill capabilities |
| REQ-JPQ-017 | Taxonomy | PROJ-006-ARCH-001 Prompt Type Decision Guide | STK-001 clarity requirement |
| REQ-JPQ-018 | Tiers | PROJ-006-ARCH-001 Tier Definitions; Salesforce worked example validation | STK-002 measurability |
| REQ-JPQ-019 | Tiers | PROJ-006-ARCH-001 Tier 4/3/2/1 Observable Characteristics tables | STK-002 self-assessment |
| REQ-JPQ-020 | Tiers | PROJ-006-ARCH-001 Rubric Overview (formula) and Worked Example (76.3) | STK-003 consistency |
| REQ-JPQ-021 | Anti-Patterns | PROJ-006-SYN-001 Anti-Patterns Section (8 patterns documented) | PROJ-006-ARCH-001 design rationale |
| REQ-JPQ-022 | Anti-Patterns | PROJ-006-SYN-001 Before/After examples for AP-01 through AP-08 | Survey Section 4 (multishot patterns) |
| REQ-JPQ-023 | Anti-Patterns | PROJ-006-ARCH-001 criteria + PROJ-006-SYN-001 anti-patterns (synthesized) | STK-003 coverage |
| REQ-JPQ-024 | Usability | PROJ-006-ARCH-001 L0 Quick-Reference Rubric Card design | STK-002 self-assessment |
| REQ-JPQ-025 | Maintainability | STK-003 success measure (v1.0 vs v1.x within 3 points) | PROJ-006-ARCH-001 L2 weight justification |

### Intentional Exclusions

The following topics were intentionally excluded from requirements, consistent with the rubric's documented scope limitations:

| Excluded Topic | Reason | Source |
|----------------|--------|--------|
| Context window economics (token cost) | No empirical baseline in existing literature; unquantified | PROJ-006-ARCH-001, What This Rubric Does Not Cover, item 1 |
| Model-tier calibration for user prompts | Jerry handles model routing internally via YAML `model:` field; users do not select model tiers | PROJ-006-ARCH-001, item 2 |
| Few-shot example quality in user prompts | Jerry agent specs embed examples; users invoke skills, not construct examples | PROJ-006-ARCH-001, item 3 |
| Tool description quality | Relevant for MCP tool authors, not Jerry user prompt quality | PROJ-006-ARCH-001, item 4 |
| Skills not investigated in Phase 1 | worktracker, nasa-se, transcript, architecture skills not examined; patterns confirmed for problem-solving and orchestration only | PROJ-006-SYN-001, Scope Limitation S-001 |

### Hypothesis-Status Items

| Item | Status | Implication for Requirements |
|------|--------|------------------------------|
| Cognitive mode effectiveness (convergent/divergent declaration) | Hypothesis -- no controlled comparison exists | REQ-JPQ-013 (JE2) uses `next_agent_hint` routing (structural evidence) rather than cognitive mode declaration as the verification basis |
| AP-07 (Conflicting Instructions Across Skill Boundaries) | Hypothesis -- derived from P-003 constraint, not observed failure | REQ-JPQ-021 flags AP-07 as hypothesis-status; it counts toward the 8-pattern minimum but is not weighted in impact ordering |
| ReAct benchmark applicability to frontier models | Qualified -- 2022-era benchmarks used directionally, not as specific numbers | REQ-JPQ-007 and REQ-JPQ-008 use Jerry's own circuit breaker thresholds, not academic benchmarks |

---

*Document Version: 1.0.0*
*Agent: nse-requirements (nasa-se skill)*
*NPR 7123.1D Compliance: Process 2 (Stakeholder Expectations), Process 3 (Requirements Definition)*
*Constitutional Compliance: P-001 (all claims cited to source artifacts), P-002 (persisted to mandatory path), P-003 (no subagents), P-022 (hypothesis-status items and scope limitations documented)*
*Created: 2026-02-18*
*Source Artifacts: prompt-quality-rubric-taxonomy.md (v1.0.0), jerry-prompt-best-practices-guide.md (v1.0.0)*
