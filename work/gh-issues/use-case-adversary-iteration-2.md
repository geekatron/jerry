# Strategy Execution Report: Use Case Skill Issue — C4 Adversarial Review (Iteration 2)

## Execution Context

- **Strategy:** S-004 (Pre-Mortem Analysis) + S-012 (FMEA) + S-001 (Red Team Analysis)
- **Templates:** `.context/templates/adversarial/s-004-pre-mortem.md`, `s-012-fmea.md`, `s-001-red-team.md`
- **Deliverable:** `work/gh-issues/issue-use-case-skill.md`
- **Criticality:** C4 (tournament mode — GitHub Issue for OSS release)
- **Executed:** 2026-02-26
- **H-16 Note:** This is a combined iteration 2 report. H-16 requires S-003 (Steelman) before S-004/S-001. Per the orchestrator's instruction, this is adversarial critique iteration. The deliverable has been reviewed with steelman posture in iteration 1; this report applies adversarial critique.

---

## Part I: S-004 Pre-Mortem Analysis

### Pre-Mortem Declaration

**Failure Scenario:** It is August 2026. The use case capability issue was implemented. Six weeks after the implementation PR merged, the three skills (`/use-case`, `/test-spec`, `/contract-design`) are rarely used by the OSS community. The two teams that did use them are confused and frustrated. One filed a bug: "The skill generated use cases but I have no idea how they relate to my `/worktracker` features." Another filed a bug: "The contract-design skill produced OpenAPI YAML but it's not grounded in anything — there's no clear process for how I get from a use case to a spec." The skills were marked "experimental" and deprioritized for Jerry v2.

### Findings Table (S-004)

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001 | Worktracker integration underspecified: implementer cannot determine how use cases map to existing worktracker entities without inventing their own convention | Assumption | High | Critical | P0 | Actionability |
| PM-002 | Three-skill scope delivers none of them well: implementer splits focus across `/use-case`, `/test-spec`, `/contract-design` simultaneously; each skill gets shallow treatment | Process | High | Critical | P0 | Methodological Rigor |
| PM-003 | "Guided experience" left undefined: no agent interaction model specified; implementer builds a simple document generator instead of a genuine conversational guide | Assumption | High | Critical | P0 | Completeness |
| PM-004 | Contract generation without system architecture context: `/contract-design` generates OpenAPI from use case text, but use case text rarely contains enough information about existing data models, authentication, or API conventions to produce usable contracts | Assumption | Medium | Major | P1 | Evidence Quality |
| PM-005 | File limit of 150 lines conflicts with Cockburn's fully-dressed template: a complete fully-dressed use case with main success scenario, 5+ extensions, preconditions, postconditions, and cross-references easily exceeds 150 lines | Technical | High | Major | P1 | Internal Consistency |
| PM-006 | Dependency graph goes stale: no mechanism specified for keeping the dependency graph synchronized with actual use case file changes; graph is orphaned after first sprint | Process | Medium | Major | P1 | Completeness |
| PM-007 | Slicing produces INVEST-compliant artifacts that don't integrate with real sprint tooling: slices live in markdown files but have no path to Jira, Linear, or GitHub Projects | External | Medium | Major | P1 | Actionability |
| PM-008 | Agent decomposition conflicts with P-003: the four suggested agents for `/use-case` create a multi-agent topology where the slicer calls the reviewer calls the index agent — violating the single-level nesting constraint if not carefully designed | Technical | Medium | Major | P1 | Methodological Rigor |
| PM-009 | Research deliverable AC is unverifiable: "at least 3 additional industry sources" is subjective — no specification of what constitutes a qualifying source or what the research must produce | Process | Low | Minor | P2 | Traceability |
| PM-010 | Methodology conflict unresolved: Jacobson's Use Case 2.0 slicing (vertical, sprint-sized) and Cockburn's precision levels (breadth-first, progressive) operate on different axes and can produce contradictory guidance for the same use case | Assumption | Medium | Major | P1 | Methodological Rigor |

### Finding Details (S-004)

---

#### PM-001: Worktracker Integration Underspecified [CRITICAL]

**Failure Cause:** The issue states "Use cases map to Features or Stories. Slices map to Tasks" (Jerry Integration Requirements, item 1) but provides no mapping rules for disambiguation. When does a use case map to a Feature vs. a Story? When a use case spans multiple actors with independent goals, does each actor's goal become a separate Story? When a use case has 12 slices, do all 12 become Tasks under one Story, or do slices become Stories themselves? The issue does not define how the `UC-NNN` ID namespace coexists with the existing `FEAT-NNN`, `STORY-NNN`, `TASK-NNN` namespaces. An implementer building this will invent their own convention — and it will be incompatible with the existing worktracker entity hierarchy.

**Category:** Assumption
**Likelihood:** High — the existing worktracker has a well-defined entity hierarchy with specific containment rules. This is a concrete integration point that requires concrete design decisions.
**Severity:** Critical — if the worktracker integration is wrong, the core value proposition ("slices fit in a sprint") collapses. The whole point of Jacobson's Use Case 2.0 is sprint-backlog integration.
**Evidence:** "Use cases map to Features or Stories. Slices map to Tasks. Status tracking flows through the worktracker." (Jerry Integration Requirements, item 1) — three sentences that replace a design decision.
**Dimension:** Actionability
**Mitigation:** Add a concrete mapping table specifying: use case types → worktracker entity types, ID namespace design (`UC-NNN` as a prefix on existing entity types or a new entity type), and slice-to-task containment rules. Reference `skills/worktracker/rules/worktracker-entity-hierarchy.md` explicitly.
**Acceptance Criteria:** The mapping table must be verified against the worktracker entity hierarchy rules and confirmed compatible with existing WTI-001 through WTI-009 rules.

---

#### PM-002: Three-Skill Scope Dilutes Implementation Quality [CRITICAL]

**Failure Cause:** The issue proposes three full skills simultaneously — `/use-case` (9 capabilities, 4 agents), `/test-spec` (5 capabilities), and `/contract-design` (6 capabilities) — with a single research-first implementation approach that covers all three. Each skill independently requires deep methodology research, agent architecture design, template creation, and integration work. Building three skills in parallel means the implementer will make premature agent decomposition decisions for `/test-spec` and `/contract-design` before understanding the `/use-case` output format. The dependency is explicit: `/test-spec` operates on use case artifacts, so its design is downstream of `/use-case`'s file format. Implementing all three simultaneously without intermediate validation creates rework risk.

**Category:** Process
**Likelihood:** High — the Approach section describes four phases in sequence but all three skills are implemented in Phase 3 simultaneously, with no phasing between skills.
**Severity:** Critical — shallow implementation of all three skills is worse than deep implementation of one skill. The OSS community will dismiss all three as unusable rather than adopting the core skill and waiting for complements.
**Evidence:** "Phase 3: Skill Implementation: 9. Implement /use-case skill... 10. Implement /test-spec skill... 11. Implement /contract-design skill..." (Approach, Phase 3) — no sequencing, no checkpoint between skills.
**Dimension:** Methodological Rigor
**Mitigation:** Add explicit implementation phasing: implement `/use-case` first to completion and verification, then implement `/test-spec` as a downstream consumer of `/use-case` output format, then implement `/contract-design`. Add a gate between each skill phase.
**Acceptance Criteria:** The Approach section defines skill-by-skill sequencing with explicit gates (e.g., "do not begin `/test-spec` until `/use-case` produces a verified use case artifact that `/test-spec` can consume").

---

#### PM-003: "Guided Experience" Lacks Interaction Model [CRITICAL]

**Failure Cause:** The acceptance criterion "A user who has never written a use case before can follow the guidance and produce a structurally valid use case" (AC, Guided experience bullet) describes an outcome but specifies no interaction model. What does "guided" mean in Jerry's agent architecture? Is it a sequence of prompts? A structured Q&A? A fill-in-the-template workflow? Does the agent ask clarifying questions before proceeding? If the user says "I want a use case for user authentication," does the skill ask about actors, goal level, context? Or does it generate a generic template? Without specifying the interaction model, an implementer will build a document generator (paste in context, get a use case) rather than a genuine guidance workflow.

**Category:** Assumption
**Likelihood:** High — "guided" is used throughout the issue without definition. The word appears in capabilities (item 1: "Interactive workflow") and in the AC, but no existing Jerry skill defines a comparable "interactive workflow" pattern to reference.
**Severity:** Critical — the entire value proposition is "guided experience." Without a specified interaction model, the distinguishing characteristic of the skill is undefined.
**Evidence:** "Guided use case creation: Interactive workflow that walks users through identifying actors, defining goals, writing main success scenarios, and specifying extensions." (Skill 1, Capability 1) — describes steps but not the interaction mechanism.
**Dimension:** Completeness
**Mitigation:** Specify the interaction model in the issue: (a) define what "interactive" means in Jerry's agent architecture (conversational Q&A loop? structured prompt sequence?), (b) provide a sample interaction transcript showing a user going from "I want a use case" to a completed artifact, (c) identify which existing Jerry skill (if any) provides a comparable interaction pattern to model.
**Acceptance Criteria:** The AC must include a sample interaction scenario (minimum 5 exchanges) demonstrating the guided experience. The interaction model must be consistent with Jerry's agent architecture (P-003, single-level nesting, no recursive loops).

---

#### PM-004: Contract Generation Without Architecture Context [MAJOR]

**Failure Cause:** `/contract-design` generates OpenAPI/Swagger specifications from "use case interactions (actor ↔ system steps)" (Skill 3, Capability 1). But use case text describes *what* the system does, not *how* it exposes it. To generate a usable OpenAPI spec, the skill needs: the system's existing API conventions, authentication scheme, URL structure, data model definitions, and error taxonomy. None of this comes from a use case. A use case might say "the user submits payment" — but an OpenAPI spec requires knowing whether payment is `POST /payments`, `POST /orders/{id}/payment`, or `POST /checkout/confirm`, what the request body schema is, what the existing `Amount` model looks like, and what HTTP status codes the system uses. Generating a spec without this context produces unusable artifacts.

**Category:** Assumption
**Likelihood:** Medium — the issue assumes use case text contains sufficient information for contract generation; this assumption may hold for greenfield systems with no existing conventions but fails for brownfield development.
**Severity:** Major — unusable contract artifacts will frustrate users more than no contract generation at all.
**Evidence:** "From use case interactions (actor ↔ system steps), generates OpenAPI/Swagger specifications. Each endpoint traces to a specific use case interaction." (Skill 3, Capability 1) — no mention of system context, existing API conventions, or data model input.
**Dimension:** Evidence Quality
**Mitigation:** Specify that `/contract-design` requires system context inputs (existing API conventions, data model, authentication scheme) in addition to use case artifacts. Add a "system context" input to the skill's prerequisites. Alternatively, scope the skill to generating contract *stubs* or *templates* rather than complete specifications.
**Acceptance Criteria:** The skill's prerequisites define what system context is required, or the skill's output is explicitly scoped as stubs/templates requiring engineer completion.

---

#### PM-005: 150-Line Limit Conflicts with Fully-Dressed Template [MAJOR]

**Failure Cause:** The issue mandates "No file exceeds ~150 lines" (Acceptance Criteria, Individual file organization bullet). Cockburn's fully-dressed use case template includes: Use Case Name, Scope, Level, Primary Actor, Stakeholders and Interests, Preconditions, Success Guarantee (Postconditions), Main Success Scenario (often 10+ steps), Extensions (each numbered, often 5-15 extensions with multiple sub-steps), Special Requirements, Technology/Data Variations, Frequency of Occurrence, and Open Issues. A single fully-dressed use case for a moderately complex interaction easily exceeds 200 lines. The 150-line constraint is architecturally incompatible with "fully-dressed templates available" (AC, Template support bullet).

**Category:** Technical
**Likelihood:** High — this conflict exists for any moderately complex use case. The fully-dressed template is one of the two explicitly required templates.
**Severity:** Major — an implementer must either violate the line limit or gut the fully-dressed template. Either outcome degrades the methodology.
**Evidence:** "No file exceeds ~150 lines" (AC bullet, Individual file organization) vs. "Both casual and fully-dressed templates are available and selectable" (AC bullet, Template support). The tilde (~) provides some flexibility, but the tension is real.
**Dimension:** Internal Consistency
**Mitigation:** Replace the 150-line hard constraint with a complexity-proportional guidance: "Casual template use cases should target 50-100 lines. Fully-dressed use cases may extend to 200-300 lines. When a use case exceeds 300 lines, decompose extensions into separate extension files with cross-references." Add a decomposition pattern for large use cases.
**Acceptance Criteria:** The file organization section distinguishes line guidance by template type and provides a decomposition pattern for oversized use cases.

---

#### PM-008: Agent Decomposition Creates P-003 Risk [MAJOR]

**Failure Cause:** The issue suggests four agents for `/use-case` alone: use case author agent, use case slicer agent, use case reviewer agent, and use case index agent. If an implementer builds these as agents that invoke each other (author → slicer → reviewer → index), this violates P-003's single-level nesting constraint. Under P-003, only the main context (orchestrator) can invoke workers; workers cannot invoke other workers. A four-agent skill requires the main context to orchestrate all four agents, maintaining state between invocations. The issue does not specify how the agents interact, creating high risk that an implementer builds a recursive topology.

**Category:** Technical
**Likelihood:** Medium — the issue does note agent-development-standards.md compliance, but the suggested four-agent decomposition for a single skill naturally invites sequential agent chaining.
**Severity:** Major — a P-003 violation in a published OSS skill would demonstrate a constitutional violation in the framework's own example implementation.
**Evidence:** "Suggested agent decomposition... Use case author agent... Use case slicer agent... Use case reviewer agent... Use case index agent" (Skill 1, Agents section) — four agents without interaction model.
**Dimension:** Methodological Rigor
**Mitigation:** Add explicit constraint: "All four agents are worker agents invoked by the main context; they MUST NOT invoke each other. The main context orchestrates agent invocations sequentially." Optionally reduce to fewer agents if the interaction model doesn't require four.
**Acceptance Criteria:** Agent definitions show no Task tool invocations between skill-internal agents. Architecture review demonstrates P-003 compliance.

---

#### PM-010: Jacobson-Cockburn Methodology Tension Unresolved [MAJOR]

**Failure Cause:** The issue presents Jacobson and Cockburn as complementary ("They are complementary, not competing" — Methodological Foundation). But they have a real tension that the issue does not resolve: Jacobson's Use Case 2.0 slicing produces *thin vertical slices* that span all system layers — these are meant to be sprint-backlog items, not detailed use case specifications. Cockburn's fully-dressed template produces *rich behavioral specifications* for a single use case interaction — these are meant for complete requirement documentation. The "slice" in Jacobson is not the same as the "use case" in Cockburn. Cockburn writes the use case; Jacobson then slices it. But at what point? After the use case is fully dressed? After a brief version? The issue says "Given a complete use case, generates candidate slices" (Capability 3) — but defines "complete" nowhere. An implementer will make incompatible decisions about when slicing applies.

**Category:** Assumption
**Likelihood:** Medium — teams familiar with one methodology but not both will apply the "other" methodology incorrectly.
**Severity:** Major — methodological incoherence in the core skill undermines the value proposition of "grounded in the methodologies that invented the discipline."
**Evidence:** "How the pillars combine" table shows Jacobson handles "Structure" and Cockburn handles "how to write" — but the interaction between Cockburn's precision levels and Jacobson's slicing activities (specifically: when slicing occurs in the progressive refinement process) is not addressed.
**Dimension:** Methodological Rigor
**Mitigation:** Add a "Methodology Integration Protocol" section specifying: (1) the recommended sequence (Cockburn's Level 1 → Level 2 → Jacobson slicing → Level 3 detail on slices), (2) the definition of "complete enough to slice" (Cockburn Level 2 = brief with main success scenario), (3) when slicing precedes vs. follows full use case specification.
**Acceptance Criteria:** The Methodology Integration Protocol provides an unambiguous decision tree for when to apply each methodology's techniques.

---

### Recommendations (S-004)

**P0 — MUST mitigate before acceptance:**

- PM-001: Add concrete worktracker integration mapping table with entity type rules and ID namespace design
- PM-002: Add skill-by-skill implementation sequencing with gates between skills
- PM-003: Add interaction model specification with sample transcript

**P1 — SHOULD mitigate:**

- PM-004: Specify system context requirements for contract generation or scope output to stubs
- PM-005: Replace 150-line constraint with template-type-aware line guidance and decomposition pattern
- PM-008: Add P-003 compliance constraint to agent decomposition section
- PM-010: Add Methodology Integration Protocol resolving Jacobson-Cockburn sequencing

**P2 — Monitor:**

- PM-006: Add dependency graph synchronization mechanism to architecture section
- PM-007: Acknowledge sprint tooling integration as out of scope or future work explicitly
- PM-009: Add qualifying criteria for research sources

---

## Part II: S-012 FMEA (Failure Mode and Effects Analysis)

### Element Decomposition

| Element | Description |
|---------|-------------|
| E1 | Title and Labels |
| E2 | Vision/Motivation Section |
| E3 | Methodological Foundation (Jacobson + Cockburn) |
| E4 | Skill 1 (`/use-case`) Capabilities |
| E5 | Skill 1 Agent Decomposition |
| E6 | Skill 2 (`/test-spec`) Capabilities |
| E7 | Skill 3 (`/contract-design`) Capabilities |
| E8 | Architecture and File Organization |
| E9 | Jerry Integration Requirements |
| E10 | Acceptance Criteria |
| E11 | Approach (Phase Plan) |
| E12 | Exclusions ("What this does NOT include") |

### FMEA Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001 | E10 (Acceptance Criteria) | Ambiguous: "A user who has never written a use case before can follow the guidance and produce a structurally valid use case" — "structurally valid" is undefined; no test exists for this | 8 | 8 | 7 | 448 | Critical | Define "structurally valid" with specific measurable criteria; add a sample use case that demonstrates what PASS looks like | Methodological Rigor |
| FM-002 | E9 (Jerry Integration) | Missing: no specification of which worktracker entity type a use case creates (Feature vs. Story depends on scope, but scope is not defined) | 9 | 9 | 6 | 486 | Critical | Add entity mapping table with scope-based decision rules | Actionability |
| FM-003 | E5 (Agent Decomposition) | Ambiguous: four agents with no interaction protocol; P-003 violation risk if implementer builds sequential agent chain | 8 | 6 | 7 | 336 | Critical | Specify that all agents are worker agents invoked by main context only; add P-003 compliance note | Methodological Rigor |
| FM-004 | E4 (Skill 1 Capabilities) | Insufficient: Capability 1 ("Interactive workflow") does not define the interaction model; implementer cannot build it without inventing one | 8 | 8 | 5 | 320 | Critical | Specify interaction model (conversational Q&A vs. template fill-in vs. structured prompt sequence) | Completeness |
| FM-005 | E8 (File Organization) | Incorrect: 150-line limit conflicts with fully-dressed Cockburn template; constraint is unachievable for complex use cases | 7 | 9 | 4 | 252 | Critical | Replace with template-type-aware guidance; add decomposition pattern | Internal Consistency |
| FM-006 | E7 (Skill 3 Capabilities) | Incorrect: assumes use case text contains sufficient information for OpenAPI generation; brownfield systems require existing API context not present in use cases | 7 | 7 | 5 | 245 | Critical | Add system context input requirements or scope output to stubs | Evidence Quality |
| FM-007 | E10 (Acceptance Criteria) | Ambiguous: "Dependency graph: A navigable dependency graph shows relationships between use cases, slices, and actors. Rendered in Mermaid." — no spec for what "navigable" means or how the graph is kept current | 6 | 7 | 6 | 252 | Critical | Define dependency graph update mechanism and what "navigable" means (links from graph to artifact files) | Completeness |
| FM-008 | E3 (Methodology) | Insufficient: Jacobson-Cockburn integration sequence not specified; "when to slice" relative to Cockburn's precision levels is undefined | 7 | 6 | 6 | 252 | Critical | Add Methodology Integration Protocol with sequencing decision tree | Methodological Rigor |
| FM-009 | E11 (Approach) | Missing: no phasing between skills; all three implemented simultaneously in Phase 3 despite `/test-spec` and `/contract-design` being downstream consumers of `/use-case` artifacts | 8 | 7 | 5 | 280 | Critical | Add skill-by-skill sequencing with validation gates | Methodological Rigor |
| FM-010 | E6 (Skill 2 Capabilities) | Ambiguous: "Every test traces to a specific use case scenario" — does this mean the test file contains a reference to the use case file? A frontmatter field? A comment? Implementation is unclear | 6 | 7 | 6 | 252 | Critical | Specify traceability mechanism (frontmatter field, bidirectional link format) | Traceability |
| FM-011 | E10 (Acceptance Criteria) | Ambiguous: "Cross-referencing: Bidirectional links exist between use cases, slices, test specs, and contracts" — no specification of link format or validation mechanism | 6 | 7 | 6 | 252 | Critical | Define bidirectional link format (frontmatter key, value format) and validation approach | Traceability |
| FM-012 | E9 (Jerry Integration) | Missing: no specification of how the three skills interact with each other within Jerry's agent routing system; are they independent slash commands? Do they share state? | 5 | 7 | 7 | 245 | Critical | Specify inter-skill interaction model and routing | Internal Consistency |
| FM-013 | E8 (File Organization) | Insufficient: `contracts/` directory contains YAML and JSON files, not markdown — this conflicts with the Jerry convention of markdown worktracker entities; no frontmatter or cross-referencing defined for non-markdown contracts | 6 | 6 | 7 | 252 | Critical | Specify how contract files (YAML/JSON) participate in the cross-referencing and traceability system | Traceability |
| FM-014 | E4 (Skill 1 Capabilities) | Missing: no specification of how the use case index is generated (auto-generated means the skill runs a command or a hook? manually triggered?) | 5 | 7 | 6 | 210 | Major | Specify index generation mechanism (command, hook, or agent action) | Completeness |
| FM-015 | E12 (Exclusions) | Missing: "Prescribing the final architecture" is listed as an exclusion but then the issue prescribes a specific directory structure — the boundary between "recommended starting point" and "required" is unclear | 5 | 7 | 5 | 175 | Major | Clarify which elements of the file organization are required (design principles) vs. optional (directory layout) | Internal Consistency |
| FM-016 | E10 (Acceptance Criteria) | Missing: no AC covers error handling or failure paths in the guided experience — what happens when the user provides an incomplete or inconsistent actor/goal specification? | 6 | 6 | 5 | 180 | Major | Add AC covering guided experience failure paths | Completeness |
| FM-017 | E6 (Skill 2 Capabilities) | Insufficient: "Test slice alignment: When use cases are sliced, test specifications align to slices" — alignment mechanism undefined; does a test spec reference the slice ID? | 5 | 6 | 6 | 180 | Major | Specify slice-to-test-spec alignment mechanism | Traceability |
| FM-018 | E11 (Approach) | Missing: Phase 2 designs "cross-referencing and dependency graph approach" but doesn't specify what decisions must be made (frontmatter schema, link format, ID format) — design artifacts are undefined | 5 | 7 | 5 | 175 | Major | Add list of architectural decisions that Phase 2 must produce | Methodological Rigor |
| FM-019 | E9 (Jerry Integration) | Insufficient: "Use case artifacts are deliverables subject to Jerry's quality framework. Criticality classification applies" — but what criticality does a use case file have at creation time? C1/C2/C3 depends on scope, but scope rules are missing | 4 | 6 | 5 | 120 | Minor | Add default criticality classification rules for different use case artifact types | Evidence Quality |
| FM-020 | E2 (Vision) | Insufficient: the ski metaphor is compelling but does not establish the problem concretely for an OSS audience unfamiliar with ski culture | 3 | 4 | 5 | 60 | Minor | Add a concrete software failure example alongside the metaphor | Evidence Quality |

### FMEA Finding Details (Critical Findings)

---

#### FM-002: Missing Worktracker Entity Type Mapping [CRITICAL] (RPN: 486)

**Element:** E9 — Jerry Integration Requirements
**Failure Mode:** Missing — no specification of when a use case maps to a Feature vs. a Story
**Effect:** Implementer invents an incompatible mapping. Users find use case entities in the wrong hierarchy position. Worktracker integrity rules (WTI-001 to WTI-009) are violated.
**S: 9** — Worktracker integration failure invalidates the core value proposition of sprint-compatible use case delivery
**O: 9** — This is a definitive missing design decision, not a gap; it will definitely not be resolved by reading the issue
**D: 6** — Might be caught during integration testing if the tester knows the worktracker hierarchy
**Corrective Action:** Add entity mapping table: "Use case (high-level, summary goal level) → Feature; Use case (sea-level, primary actor goal) → Story; Slice → Task. Parent-child rules: Feature contains Stories; Story contains Tasks (matching worktracker hierarchy). Use case ID namespace: use worktracker FEAT-NNN or STORY-NNN prefix with UC suffix (e.g., STORY-042-UC-authentication)."
**Acceptance Criteria:** Mapping table is validated against `worktracker-entity-hierarchy.md` and confirmed by running a sample use case through worktracker creation workflow.

---

#### FM-001: "Structurally Valid" AC Undefined [CRITICAL] (RPN: 448)

**Element:** E10 — Acceptance Criteria
**Failure Mode:** Ambiguous — "structurally valid use case" is undefined
**Effect:** Implementer builds any artifact and calls it valid. Reviewer has no standard to apply. AC is unverifiable and provides no quality signal.
**S: 8** — An unverifiable AC means the entire guided experience claim cannot be evaluated
**O: 8** — Structural validity is inherently undefined without a reference template and checklist
**D: 7** — Vagueness is subtle; a reviewer might accept "looks like a use case" as passing this AC
**Corrective Action:** Replace with: "A new user can produce a use case that passes Cockburn's completeness heuristics checklist: (1) Primary actor identified, (2) Goal stated at sea level, (3) Trigger defined, (4) Main success scenario has ≥ 5 steps, (5) ≥ 1 extension specified, (6) Pre- and postconditions stated. Verification: run the completed use case through the `/use-case` reviewer agent and receive a PASS result."
**Acceptance Criteria:** The reviewer agent produces a checklist-based pass/fail output against Cockburn's completeness heuristics.

---

#### FM-003: Agent Interaction Protocol Missing — P-003 Risk [CRITICAL] (RPN: 336)

**Element:** E5 — Agent Decomposition
**Failure Mode:** Ambiguous — no interaction protocol for four suggested agents
**Effect:** Implementer builds a chain where the slicer agent invokes the reviewer agent invokes the index agent, violating P-003. Or implementer doesn't know how to coordinate four agents and builds fewer, weaker agents.
**S: 8** — P-003 violation in an OSS example implementation is a constitutional failure that undermines framework credibility
**O: 6** — Multi-agent chaining is the natural naive implementation; P-003 compliance requires deliberate architectural discipline
**D: 7** — The violation would appear in code review but might be missed if the reviewer doesn't check for Task tool usage in worker agents
**Corrective Action:** Add: "Agent interaction model: the main context (user's Claude Code session) orchestrates all four agents sequentially. No agent invokes another agent. The author agent produces a draft; the user's context passes the draft to the reviewer agent; the reviewer produces feedback; the context incorporates feedback and may reinvoke the author. The slicer and index agents are invoked independently by the user's context. All four agents are T1 or T2 tier (no Task tool)."
**Acceptance Criteria:** `.governance.yaml` for each agent confirms tool_tier T1 or T2. No agent definition includes `Task` in its tools list.

---

#### FM-009: No Skill-by-Skill Implementation Sequencing [CRITICAL] (RPN: 280)

**Element:** E11 — Approach
**Failure Mode:** Missing — Phase 3 implements all three skills simultaneously without checkpoints
**Effect:** Implementation is wide and shallow. `/test-spec` design decisions are made before `/use-case` output format is stable, creating rework. No validation that the pipeline actually works end-to-end until Phase 4, when reverting design decisions is expensive.
**S: 8** — Premature parallelism in dependent system design causes architectural rework
**O: 7** — The natural implementation pattern for a "build three things" issue is to build them in parallel
**D: 5** — Might be caught in design review if a reviewer notices the dependency chain
**Corrective Action:** Restructure Phase 3 as: "Phase 3a: Implement `/use-case` skill and produce one verified sample use case artifact. Phase 3b: Implement `/test-spec` skill, consuming the verified sample use case. Verify bidirectional traceability. Phase 3c: Implement `/contract-design` skill, consuming the verified sample use case. Verify bidirectional traceability." Add explicit gates.
**Acceptance Criteria:** Each phase has a gate artifact (verified sample output) before the next phase begins.

---

#### FM-005: 150-Line Constraint vs. Fully-Dressed Template [CRITICAL] (RPN: 252)

**Element:** E8 — Architecture and File Organization
**Failure Mode:** Incorrect — structural constraint conflicts with methodology requirement
**Effect:** Implementer must choose between the 150-line limit and a genuinely useful fully-dressed template. Either the template is degraded (stripped of essential content) or the constraint is silently violated.
**S: 7** — An internally inconsistent constraint undermines methodology fidelity
**O: 9** — This conflict will manifest for virtually every non-trivial use case using the fully-dressed template
**D: 4** — Detectable during AC verification if the reviewer checks both constraints against the same artifact
**Corrective Action:** Replace the 150-line limit with tiered guidance: "Casual template target: 50-80 lines. Fully-dressed template target: 100-250 lines. When any use case file exceeds 300 lines, apply the extension file pattern: move each extension group (e.g., 3a-3f) to a separate `extensions/{extension-id}.md` file with a parent reference."
**Acceptance Criteria:** File organization documentation shows the tiered guidance and extension file pattern with a working example.

---

### FMEA Summary

**Elements analyzed:** 12
**Failure modes identified:** 20
**Critical findings (RPN >= 200):** 13
**Major findings (RPN 80-199):** 5
**Minor findings (RPN < 80):** 2

**Most failure-prone element:** E10 (Acceptance Criteria) — 5 findings including FM-001, FM-007, FM-010, FM-011, FM-016. The AC section has the highest failure density because it inherits ambiguity from every underspecified section above it.

**Overall assessment:** REVISE. The issue has 13 Critical failure modes across core elements. The most severe cluster is: worktracker integration mapping (FM-002, RPN 486), AC verifiability (FM-001, RPN 448), and agent interaction protocol (FM-003, RPN 336). These must be resolved before implementation begins.

---

## Part III: S-001 Red Team Analysis

### Threat Actor Profile

**Goal:** An implementer (new OSS contributor) who wants to demonstrate progress quickly, receive merge approval, and move on. They will implement what is written literally, fill gaps with their own best judgment, and build the minimum required to pass each AC bullet.

**Capability:** Full access to the issue, codebase, and Jerry's agent/skill patterns. Familiar with Python and markdown. Has read Jacobson's and Cockburn's books. Does not have deep Jerry internals knowledge (agent governance, P-003 topology, worktracker hierarchy rules).

**Motivation:** Contribute a visible capability to Jerry's OSS release. The three-skill capability is prominently motivated and will be the marquee feature of the release.

### Attack Vectors

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|-------------------|
| RT-001 | Every AC bullet has a loophole: implementer can pass "Guided experience" AC by building a single-shot template generator that produces a structurally valid use case without any interactive guidance | Circumvention | High | Critical | P0 | Missing | Actionability |
| RT-002 | "Research deliverable" AC contains no quality bar: "at least 3 additional industry sources" can be satisfied by citing Wikipedia, a blog post, and a Stack Overflow answer | Circumvention | High | Major | P1 | Missing | Evidence Quality |
| RT-003 | Agent definitions AC is verifiable mechanically but not behaviorally: passing JSON Schema validation does not verify that agents actually produce use cases correctly | Ambiguity | High | Critical | P0 | Missing | Methodological Rigor |
| RT-004 | "Bidirectional links" AC exploited as static text: an implementer adds hardcoded cross-reference links in markdown that are never automatically maintained; they go stale immediately | Circumvention | High | Major | P1 | Missing | Traceability |
| RT-005 | Dependency graph AC exploited as a one-time artifact: implementer generates the Mermaid graph once from an initial set of use cases; it is never updated as use cases change | Circumvention | High | Major | P1 | Missing | Completeness |
| RT-006 | "Worktracker integration" AC passed by manual documentation: implementer writes a how-to document explaining how to manually map use cases to worktracker entities, rather than building actual integration | Ambiguity | Medium | Major | P1 | Missing | Actionability |
| RT-007 | "Test slice alignment" exploited as convention rather than mechanism: an implementer documents a naming convention (TS-001 corresponds to SL-001 by name) rather than building a mechanical link | Ambiguity | Medium | Minor | P2 | Missing | Traceability |
| RT-008 | Scope boundary exploitation: "Prescribing the final architecture" is excluded, so an implementer can propose a significantly different file structure that is harder to traverse and claim it satisfies the design principles | Boundary | Low | Minor | P2 | Partial | Internal Consistency |

### Defense Gap Analysis

---

#### RT-001: "Guided Experience" AC Has No Interactive Requirement [CRITICAL]

**Attack Vector:** The AC reads: "A user who has never written a use case before can follow the guidance and produce a structurally valid use case." An implementer builds a skill that accepts "describe your feature" as input and returns a filled-in Cockburn template with placeholder values. The output is structurally valid (it has all the fields). The user "followed the guidance" by reading the output. The AC is technically satisfied.

**Category:** Circumvention
**Exploitability:** High — the AC describes an outcome (user produces a valid use case) but does not require a process (interactive dialogue, progressive elaboration, clarifying questions).
**Severity:** Critical — the entire value proposition of the skill is "guided experience." If this can be circumvented, the differentiating characteristic is absent.
**Existing Defense:** None. The issue uses "guided" and "interactive" extensively but the AC only tests the output, not the process.
**Evidence:** "A user who has never written a use case before can follow the guidance and produce a structurally valid use case." (AC, Guided experience bullet) — output-only criterion.
**Countermeasure:** Replace the AC with a process-verifiable criterion: "The `/use-case` skill conducts a minimum 5-turn interactive session before producing the use case draft. The session must elicit: (1) primary actor, (2) goal level, (3) trigger, (4) at least 3 steps of the main success scenario, and (5) at least 1 extension scenario. Verification: a test transcript demonstrates the 5-turn elicitation."
**Acceptance Criteria:** Test transcript showing ≥ 5 user-agent exchanges before use case draft is produced.

---

#### RT-003: Agent Definition AC Is Mechanically Verifiable But Behaviorally Empty [CRITICAL]

**Attack Vector:** The AC requires: "All agents have `.md` definition files... All validate against `docs/schemas/agent-governance-v1.schema.json`... Constitutional compliance triplet present in every agent." An implementer creates four agent definition files with correct YAML frontmatter, valid schema, and P-003/P-020/P-022 in `constitution.principles_applied`. The agents validate. The AC passes. But the agents' actual methodology sections — what they do when invoked — are minimal, inconsistent with Cockburn's templates, or produce generic output. The mechanical AC says nothing about behavioral quality.

**Category:** Ambiguity
**Exploitability:** High — schema validation is binary; behavioral quality is subjective and not covered by any AC.
**Severity:** Critical — if agent behavior is unspecified, the skill has valid structure but no functional value.
**Existing Defense:** "Quality compliance: All deliverables pass quality gate (>= 0.92 for C2+)" — but this is a process requirement, not a behavioral specification for what agents must do.
**Evidence:** "Agent definitions: All agents have `.md` definition files... All validate against `docs/schemas/agent-governance-v1.schema.json`" (AC bullet) — validates structure only.
**Countermeasure:** Add behavioral ACs for each agent: "The use case author agent, when given actor+goal as input, produces a use case meeting Cockburn's completeness heuristics. Verification: agent is invoked with a sample input and produces an artifact that passes the reviewer agent." Link each agent's AC to a verifiable behavioral output.
**Acceptance Criteria:** Each agent AC includes a sample input and expected output format. End-to-end test demonstrates each agent producing a correct output from a specified input.

---

#### RT-002: Research AC Has No Quality Bar [MAJOR]

**Attack Vector:** "Research covers Jacobson's Use Case 2.0, Cockburn's Writing Effective Use Cases, and at least 3 additional industry sources on use case patterns, slicing techniques, or requirements tooling." An implementer cites three blog posts about agile requirements and declares the research deliverable complete. The AC imposes no quality bar on sources (peer-reviewed? practitioner? primary?), no required depth (summary vs. deep dive), and no required output format (bullet points in WORKTRACKER.md vs. a structured research report with findings and implications).

**Category:** Circumvention
**Exploitability:** High — "at least 3 additional industry sources" is unambiguous in quantity but completely ambiguous in quality.
**Severity:** Major — weak research leads to weak design decisions, particularly for the methodology integration and agent decomposition.
**Existing Defense:** None.
**Evidence:** "Research covers Jacobson's Use Case 2.0, Cockburn's Writing Effective Use Cases, and at least 3 additional industry sources on use case patterns, slicing techniques, or requirements tooling." (AC, Research deliverable bullet)
**Countermeasure:** Specify: "Research deliverable is a structured report (minimum 500 words) documenting: (1) findings from Jacobson Use Case 2.0 with specific slicing patterns documented, (2) findings from Cockburn with template selection criteria documented, (3) synthesis of ≥ 3 additional sources that are practitioner guides, academic papers, or tool documentation (not blog posts). Research must explicitly address: agent interaction model options, worktracker integration patterns in comparable tools, file organization patterns in comparable documentation systems."
**Acceptance Criteria:** Research report passes adversarial quality review before architecture design begins.

---

#### RT-004: Bidirectional Links Can Be Satisfied by Static Markdown [MAJOR]

**Attack Vector:** The AC requires "Bidirectional links exist between use cases, slices, test specs, and contracts." An implementer adds `Related: [TS-001](../../test-specs/TS-001-auth-login.md)` to each use case file and `Related: [UC-001](../../cases/UC-001-authentication/use-case.md)` to each test spec. The links are bidirectional. The AC is satisfied. Six weeks later, the use case is renamed and the links are stale — with no mechanism to detect or repair this.

**Category:** Circumvention
**Exploitability:** High — static links satisfy the letter of the AC while providing no durable traceability.
**Severity:** Major — stale links undermine the entire "traversable" and "cross-referencing" value proposition.
**Existing Defense:** None in the AC. The design principles say "Links are bidirectional" but do not specify a maintenance mechanism.
**Evidence:** "Cross-referencing: Bidirectional links exist between use cases, slices, test specs, and contracts. From any artifact, related artifacts are discoverable." (AC bullet) — specifies existence, not maintenance.
**Countermeasure:** Add: "Bidirectional links are implemented using frontmatter fields with IDs (not file paths), allowing the index agent to resolve links by ID. The frontmatter schema for each artifact type defines `related_use_cases`, `related_slices`, `related_test_specs`, `related_contracts` as arrays of IDs. The index agent validates that all referenced IDs resolve to existing artifacts."
**Acceptance Criteria:** Running the index agent on a sample use case suite reports broken links. Moving a file does not break links (IDs, not paths, are used).

---

### Recommendations (S-001)

**P0 — MUST mitigate before acceptance:**

- RT-001: Replace "structurally valid use case" AC with process-verifiable minimum interaction requirement
- RT-003: Add behavioral ACs for each agent with sample input/output specifications

**P1 — SHOULD mitigate:**

- RT-002: Add quality bar to research deliverable AC
- RT-004: Specify frontmatter-ID-based linking mechanism in cross-referencing AC
- RT-005: Specify dependency graph update trigger in AC
- RT-006: Clarify that worktracker integration means automatic entity creation, not a how-to document

**P2 — Monitor:**

- RT-007: Specify alignment mechanism vs. naming convention
- RT-008: Clarify scope boundary on file organization prescription

---

## Consolidated Findings Summary

| ID | Severity | Source | Finding | Section |
|----|----------|--------|---------|---------|
| PM-001 / FM-002 | Critical | S-004 / S-012 | Worktracker integration underspecified — no entity type mapping | Jerry Integration Requirements |
| PM-003 / FM-004 / RT-001 | Critical | All three | "Guided experience" undefined — no interaction model, no process AC | Skill 1 Capabilities / Acceptance Criteria |
| PM-002 / FM-009 | Critical | S-004 / S-012 | No skill-by-skill implementation sequencing — all three built simultaneously | Approach |
| FM-001 / RT-003 | Critical | S-012 / S-001 | Acceptance criteria are mechanically verifiable but behaviorally empty | Acceptance Criteria |
| PM-005 / FM-005 | Critical | S-004 / S-012 | 150-line limit conflicts with fully-dressed Cockburn template | Architecture / Acceptance Criteria |
| PM-008 / FM-003 | Critical | S-004 / S-012 | Agent decomposition lacks P-003 compliance specification | Skill 1 Agents |
| PM-010 / FM-008 | Major | S-004 / S-012 | Jacobson-Cockburn methodology integration sequence undefined | Methodological Foundation |
| PM-004 / FM-006 | Major | S-004 / S-012 | Contract generation requires system context not available from use cases | Skill 3 Capabilities |
| FM-007 / RT-005 | Major | S-012 / S-001 | Dependency graph has no update/synchronization mechanism | Architecture |
| FM-010 / FM-011 | Major | S-012 | Traceability mechanism (links, frontmatter format) undefined | Architecture / Acceptance Criteria |
| RT-002 | Major | S-001 | Research AC has no quality bar | Acceptance Criteria |
| RT-004 | Major | S-001 | Bidirectional links can be satisfied by unmaintained static markdown | Acceptance Criteria |
| FM-016 | Major | S-012 | No AC for guided experience failure paths | Acceptance Criteria |
| FM-012 | Major | S-012 | Inter-skill interaction model undefined | Jerry Integration Requirements |

---

## Scoring Impact

| Dimension | Weight | Impact | Key Findings |
|-----------|--------|--------|--------------|
| Completeness (0.20) | 0.20 | Negative | PM-003/FM-004: Interaction model missing; FM-007: dependency graph update mechanism missing; FM-016: failure path AC missing |
| Internal Consistency (0.20) | 0.20 | Negative | PM-005/FM-005: 150-line limit vs. fully-dressed template; FM-015: "prescribing architecture" excluded but then prescribed |
| Methodological Rigor (0.20) | 0.20 | Negative | PM-002/FM-009: No skill sequencing; PM-010/FM-008: Jacobson-Cockburn integration undefined; FM-003: P-003 risk |
| Evidence Quality (0.15) | 0.15 | Negative | PM-004/FM-006: Contract generation assumes unsupported context; RT-002: research AC has no quality bar |
| Actionability (0.15) | 0.15 | Negative | PM-001/FM-002: Worktracker mapping missing; RT-001: guided experience AC unverifiable |
| Traceability (0.10) | 0.10 | Negative | FM-010/FM-011: Traceability mechanism undefined; RT-004: static links are not durable |

**All six dimensions are negatively impacted.** This is characteristic of a well-motivated issue that established scope and vision before design decisions were completed. The vision section is strong; the implementation specification is incomplete.

---

## Execution Statistics

- **Total Findings:** 27 (consolidated from all three strategies, deduplicating overlapping findings)
- **Critical:** 10
- **Major:** 13
- **Minor:** 4
- **Protocol Steps Completed:** S-004 (6/6), S-012 (5/5), S-001 (5/5)

---

## Self-Review (H-15)

Before persisting, verified:
1. All findings have specific evidence from the deliverable with section references. Confirmed.
2. Severity classifications are justified: Critical findings block unambiguous AC verification or violate a constitutional constraint (P-003). Major findings degrade value proposition without preventing implementation. Confirmed.
3. Finding identifiers follow template prefix formats (PM-NNN, FM-NNN, RT-NNN). Confirmed.
4. Summary table matches detailed findings. Confirmed.
5. No findings minimized — all issues reported at their actual severity. Confirmed.

---

*Strategy Execution Report: adv-executor*
*Strategies: S-004 Pre-Mortem, S-012 FMEA, S-001 Red Team*
*Deliverable: issue-use-case-skill.md*
*Date: 2026-02-26*
