# GitHub Issue Draft: Use Case Capability — Use Cases, Testing Specifications, and Contract Design

## Document Sections

| Section | Purpose |
|---------|---------|
| [Title](#title) | Issue title |
| [Labels](#labels) | Issue labels |
| [Body](#body) | Full issue body |
| [Body: The vision](#the-vision) | What we're building and why it matters |
| [Body: Why this matters](#why-this-matters) | Motivation for structured use case methodology |
| [Body: Methodological foundation](#methodological-foundation) | Jacobson's Use Case 2.0, Cockburn's Writing Effective Use Cases, integration sequence |
| [Body: Skill 1 — Use Case Authoring](#skill-1--use-case-authoring) | Core use case skill capabilities and capability-to-agent mapping |
| [Body: Skill 2 — Testing Specifications](#skill-2--testing-specifications) | Complementary testing specification skill |
| [Body: Skill 3 — Contract Design](#skill-3--contract-design) | Complementary contract design skill |
| [Body: Architecture and file organization](#architecture-and-file-organization) | Individual files, dependency graphs, indexes, strategic overview |
| [Body: Jerry integration requirements](#jerry-integration-requirements) | Worktracker, quality enforcement, existing skill integration |
| [Body: What this does NOT include](#what-this-does-not-include) | Explicit exclusions |
| [Body: Acceptance criteria](#acceptance-criteria) | Verifiable completion conditions |
| [Body: AC-to-approach traceability](#ac-to-approach-traceability) | Cross-reference mapping |
| [Body: Approach](#approach) | Research-first implementation methodology |
| [Body: Why now](#why-now) | Timing rationale |

---

## Title

Build use case capability: guided use case authoring, testing specifications, and contract design skills

## Labels

enhancement, oss-prep

## Body

### The vision

You know that feeling when you're standing at the top of a line you've never skied? You can see the entry. You can see the exit. But everything between — the chutes, the mandatory airs, the blind rollovers — that's the part that separates "I think this goes" from "I know exactly where every turn happens."

That's what use cases do for software. They're the topo map of what happens between "user wants something" and "system delivers it." Every actor, every interaction, every alternative path, every failure scenario — mapped out before anyone writes a line of code. Not in a 300-page requirements document that nobody reads. In clean, navigable, individually-scoped files that trace the exact line from goal to outcome.

This issue proposes building a **three-skill capability** for Jerry that gives users a guided, structured experience for creating effective use cases, deriving test specifications from them, and designing implementation contracts — all grounded in the methodologies that invented the discipline.

The three skills:

1. **`/use-case`** — Guided use case authoring with slicing, powered by Ivar Jacobson's Use Case 2.0 and Alistair Cockburn's *Writing Effective Use Cases*
2. **`/test-spec`** — Generate TDD and BDD test plans directly from use case artifacts
3. **`/contract-design`** — Design implementation contracts (OpenAPI/Swagger, CloudEvents, AsyncAPI, JSON Schema) from use case interactions

Each skill stands alone. Together, they form a pipeline: *understand what the system does* → *define how to verify it* → *specify how to build it*.

### Why this matters

Most projects skip use cases. They jump straight to user stories, or worse, straight to code. And then six months later, everyone's arguing about what the system is supposed to do because nobody wrote it down, or they wrote it down in a 47-page Word doc that exists on someone's laptop and describes a version of the system from three sprints ago.

The industry has already solved this problem — twice. Jacobson solved the structural problem with Use Case 2.0: lightweight, sliceable, sprint-compatible, value-delivering. Cockburn solved the writing problem: how to describe interactions at the right level of detail, with the right goal hierarchy, in formats that range from a napkin sketch to a fully-dressed specification. But most teams don't use either methodology because the tooling doesn't make it easy.

Jerry should make it easy.

Not by dumbing it down. By guiding people through it — the way a good ski instructor doesn't tell you "just turn," they show you where to initiate, where your weight should be, and what the snow's going to do under your edges. The methodology is the mountain. The skill is the guide.

And once you've mapped the use cases, the rest of the mountain opens up: tests that trace to specific use case scenarios, contracts that implement specific interactions, and a clear line from "what should happen" to "does it happen" to "how do we build it."

### Methodological foundation

This capability is built on **two mandatory methodological pillars**. Both are required. They are complementary, not competing.

#### Pillar 1: Ivar Jacobson's Use Case 2.0

Jacobson invented use cases. Use Case 2.0 is his modern evolution — lightweight, agile, and designed for iterative delivery. The core innovations:

- **Use case slicing**: Breaking use cases into thin, vertical slices that span all system layers (UI, backend, data, tests). Each slice is independently implementable, testable, and valuable. Each fits in a single sprint.
- **Six first principles** (Jacobson, Ch. 2): (1) Keep it simple by telling stories, (2) Understand the big picture, (3) Focus on value, (4) Build the system in slices, (5) Deliver the system in increments, (6) Adapt to meet the team's needs.
- **Seven activities** (Jacobson, Ch. 3): Find actors and use cases → slice the use cases → prepare a slice → analyze a slice → implement a slice → test a slice → inspect and adapt.
- **Slice lifecycle states** (Jacobson, Ch. 4): Scoped → Prepared → Analyzed → Implemented → Verified → (optionally) Retired.
- **Agile integration**: Use cases as epic-like containers; slices as sprint backlog items. Compatible with Scrum, Kanban, and Lean workflows.
- **Slicing patterns** (Jacobson, Ch. 5): Basic flow (happy path), precondition variation, simple alternative, error/edge-case handling, enhancement (non-functional or optimization).

**Source**: Jacobson, I., Spence, I., & Bittner, K. *Use-Case 2.0: The Guide to Succeeding with Use Cases*. Ivar Jacobson International.

#### Pillar 2: Alistair Cockburn's Writing Effective Use Cases

Cockburn wrote the definitive guide on *how to write* use cases that are actually useful. His methodology provides the quality framework:

- **Template spectrum** (Cockburn, Ch. 1 & Appendix A): From casual (paragraph form) to fully-dressed (numbered fields, structured extensions). Projects choose the formality level that fits their needs.
- **Goal-level hierarchy** (Cockburn, Ch. 4): Summary level ("cloud level"), user-goal level ("sea level" — the sweet spot), and subfunction level ("fish level"). Most use cases should be at sea level.
- **Precision levels** (Cockburn, Ch. 5): Breadth-first from lower to higher precision. Level 1 = actor + goal. Level 2 = brief or main success scenario. Level 3 = full scenario with extensions.
- **Actor classification** (Cockburn, Ch. 3): Primary actors (initiators), supporting actors (assistants), offstage actors (stakeholders with interests but no direct interaction).
- **Scenario structure** (Cockburn, Ch. 6-7): Main success scenario (happy path) + numbered extensions for alternatives and error conditions.
- **Completeness heuristics** (Cockburn, Ch. 10): Every use case should answer: Who is the primary actor? What is the goal? What triggers the use case? What is the main success scenario? What can go wrong? What are the preconditions and postconditions?

**Source**: Cockburn, A. *Writing Effective Use Cases*. Addison-Wesley, 2001.

#### How the pillars combine

| Concern | Jacobson (Use Case 2.0) | Cockburn (Writing Effective) |
|---------|------------------------|------------------------------|
| **Structure** | How to organize and slice | How to write each use case |
| **Granularity** | Slicing patterns for delivery | Goal levels for abstraction |
| **Lifecycle** | Slice states for tracking | Precision levels for progressive detail |
| **Agile fit** | Sprint-sized slices, backlog integration | Lightweight templates, iterative refinement |
| **Quality** | Slice quality: independently implementable, testable, valuable (per Jacobson Ch. 5) | Completeness heuristics, scenario structure (per Cockburn Ch. 10) |

Together: Jacobson tells you *what to build and when*. Cockburn tells you *how to describe it so everyone understands*.

#### Methodology integration sequence

The two pillars operate at different points in the use case lifecycle. Recommended integration sequence:

1. **Discover** (Cockburn Level 1): Identify actors and goals. One line per use case: actor + goal.
2. **Outline** (Cockburn Level 2): Write brief main success scenarios using Cockburn's templates.
3. **Slice** (Jacobson): Once a use case has a Level 2 outline, apply Jacobson's slicing patterns. A use case is "complete enough to slice" when it has a main success scenario and at least a brief enumeration of alternative paths.
4. **Detail** (Cockburn Level 3 + Jacobson slice detail): Elaborate each slice with full extensions, preconditions, and postconditions. Fully-dressed templates apply here.
5. **Verify and adapt** (Jacobson activity 7): Review slices, validate completeness per Cockburn's heuristics, and iterate.

This sequence resolves the tension between Cockburn's breadth-first progressive refinement and Jacobson's vertical slicing by establishing that slicing occurs *after* Level 2 outlining but *before* Level 3 full specification. (Note: this integration sequence is a synthesis by the issue author, not a prescription from either source. Both Jacobson and Cockburn acknowledge the other's work but neither prescribes a combined workflow. This sequence represents one defensible integration point; the implementer may adjust based on research findings.)

### Skill 1 — Use Case Authoring (`/use-case`)

The core skill. Provides a guided experience for creating, organizing, slicing, and maintaining use cases.

#### Capabilities

1. **Guided use case creation**: Interactive workflow that walks users through identifying actors, defining goals, writing main success scenarios, and specifying extensions. Follows the methodology integration sequence: Discover (Cockburn Level 1, Ch. 5) → Outline (Cockburn Level 2) → Detail (Cockburn Level 3). Progressively elaborates from actor + goal to full scenario.

2. **Template support**: Both Cockburn's casual and fully-dressed templates available. The skill selects (or recommends) the appropriate template based on project context, criticality, and user preference.

3. **Use case slicing**: Implements Jacobson's slicing methodology. Given a complete use case, generates candidate slices following established patterns (basic, precondition, alternative, error, enhancement). Each slice satisfies Jacobson's quality criteria: independently implementable, independently testable, and delivering demonstrable value to a stakeholder.

4. **Dependency graph**: Maintains a dependency graph across use cases and slices. Visualizable. Shows which use cases depend on others, which slices must be implemented before others, and which actors participate across multiple use cases.

5. **Use case index**: Auto-generated index of all use cases in a project. Filterable by actor, goal level, status, and domain. The index is the entry point — the trail map. It answers "what use cases exist and where are they?"

6. **Strategic overview**: Dashboard-style artifact showing: (a) actor-goal matrix mapping each actor to their use cases, (b) domain coverage summary identifying which functional areas have use cases and which have gaps, (c) slice status counts per use case (how many slices in each lifecycle state). Not a massive document — a concise reference that tells you where you stand.

7. **Goal-level management**: Enforces Cockburn's goal hierarchy (Ch. 4). Flags use cases at wrong levels (too detailed for sea level, too vague for fish level). Recommends decomposition or aggregation.

8. **Completeness checking**: Validates use cases against Cockburn's completeness heuristics (Ch. 10). Flags missing actors, unspecified preconditions, scenarios without extensions, and other structural gaps.

9. **Cross-referencing**: Links between use cases, their slices, related test specifications, and implementation contracts. Every artifact knows where it fits in the bigger picture.

#### Agents

The skill should define specialized agents following Jerry's agent architecture (see `agent-development-standards.md`). Suggested agent decomposition (the implementer should refine based on research):

- **Use case author agent** — Guides creation, applies templates, writes scenarios
- **Use case slicer agent** — Decomposes use cases into independently implementable, testable slices per Jacobson's patterns
- **Use case reviewer agent** — Validates completeness, goal levels, and quality
- **Use case index agent** — Maintains the index, dependency graph, and strategic overview

**P-003 compliance constraint**: All four agents are worker agents invoked by the main context (orchestrator). They MUST NOT invoke each other via the Task tool. The main context orchestrates agent invocations and maintains state between calls. This follows the orchestrator-worker topology in `agent-development-standards.md` (Pattern 2).

#### Capability-to-agent mapping

| Capability | Primary Agent | Notes |
|------------|---------------|-------|
| Guided use case creation | Use case author | Collects actor, goal, scenario via structured prompts |
| Template support | Use case author | Selects template based on context |
| Use case slicing | Use case slicer | Applies Jacobson's slicing patterns |
| Dependency graph | Use case index | Dynamically generated from frontmatter |
| Use case index | Use case index | Auto-generated, filterable |
| Strategic overview | Use case index | Actor-goal matrix, coverage, slice status |
| Goal-level management | Use case reviewer | Validates goal hierarchy per Cockburn |
| Completeness checking | Use case reviewer | Validates against Cockburn's heuristics (Ch. 10) |
| Cross-referencing | Use case index | Bidirectional link maintenance |

### Skill 2 — Testing Specifications (`/test-spec`)

Complementary skill that derives test specifications from use case artifacts.

#### Capabilities

1. **TDD plan generation**: From use case scenarios (main success + extensions), generates test-driven development plans. Each plan maps to specific use case steps and postconditions. Grounded in Jacobson's "test a slice" activity (Ch. 3) — each slice produces a verifiable test plan.

2. **BDD scenario generation**: Converts use case scenarios into BDD specifications using Given/When/Then format. The specific BDD framework (Cucumber/Gherkin, Behave, or framework-agnostic plain text) is an implementation decision for the research phase. Main success scenario → happy path. Extensions → alternative and error scenarios. Grounded in Cockburn's scenario structure (Ch. 6-7) — the main success scenario and numbered extensions map directly to Given/When/Then patterns.

3. **Test coverage mapping**: Shows which use case scenarios have corresponding test specifications and which don't. Identifies coverage gaps — "this use case has 7 extensions but only 3 have test specs." Implements Cockburn's completeness heuristics (Ch. 10) from a testing perspective.

4. **Traceability**: Every test specification traces back to a specific use case, scenario, and step. The connection is bidirectional — from test to use case and from use case to tests.

5. **Test slice alignment**: When use cases are sliced, test specifications align to slices. Each slice's acceptance criteria are derived from the corresponding test specifications. Implements Jacobson's "test a slice" activity (Ch. 3) — slices are not "done" until their test specifications pass.

#### Agents (provisional)

- **Test plan generator agent** — Converts use case scenarios into TDD plans and BDD specifications (Given/When/Then format)
- **Test coverage analyst agent** — Identifies gaps between use case scenarios and existing test specifications

Same P-003 constraint applies: both are worker agents invoked by the main context.

### Skill 3 — Contract Design (`/contract-design`)

Complementary skill that designs implementation contracts from use case interactions.

#### Capabilities

1. **API contract generation**: From use case interactions (actor ↔ system steps), generates OpenAPI/Swagger specifications. Each endpoint traces to a specific use case interaction. Grounded in Cockburn's scenario structure (Ch. 6-7) — actor-system interaction steps in the main success scenario and extensions map to API request-response pairs.

2. **Event contract generation**: For event-driven architectures, generates CloudEvents specifications from use case triggers and system responses. Event triggers correspond to use case preconditions and postconditions (Cockburn, Ch. 6-7); system responses map to steps in the main success scenario and extensions.

3. **AsyncAPI support**: For asynchronous communication patterns identified in use case scenarios — such as event-triggered extensions, background processing steps, and notification flows described in alternative paths (per Cockburn's extension notation, Ch. 6-7) — generates AsyncAPI specifications.

4. **Schema generation**: Extracts data entities from use case scenarios and generates JSON Schema definitions. Entities that appear across multiple use cases get unified schemas. Data entities are identified from the nouns in use case steps and the data requirements implied by preconditions and postconditions (Cockburn, Ch. 6-7).

5. **Contract-to-use-case traceability**: Every contract artifact traces to the use case interaction it implements. Changes to use cases surface as contract change candidates. Implements the same bidirectional traceability principle as Jacobson's slice-to-use-case relationship (Ch. 5).

6. **Contract validation**: Validates generated contracts against the use case scenarios they implement. Flags mismatches between what the use case describes and what the contract specifies. Applies validation logic analogous to Cockburn's completeness heuristics (Ch. 10) — every use case interaction should have a corresponding contract element, and every contract element should trace to a use case interaction.

**Note on system context**: Contract generation from use case text alone may produce incomplete specifications, particularly for brownfield systems with existing API conventions, authentication schemes, and data models. The skill should accept optional system context inputs (existing OpenAPI specs, data model references) and scope its output appropriately — generating contract *stubs* with clear TODO markers when system context is unavailable, and enriched specifications when context is provided.

#### Agents (provisional)

- **Contract generator agent** — Produces OpenAPI, CloudEvents, AsyncAPI, and JSON Schema artifacts from use case interactions, enriched by optional system context
- **Contract validator agent** — Validates generated contracts against their source use case scenarios

Same P-003 constraint applies: both are worker agents invoked by the main context.

### Architecture and file organization

This is critical. The whole point is to **avoid massive files**. Every artifact is an individual, navigable markdown file. The architecture must make it easy to find things, understand relationships, and traverse between related artifacts.

#### File structure (recommended starting point)

```
use-cases/
  index.md                        # Auto-generated index of all use cases
  strategic-overview.md            # Actor-goal mapping, domain coverage
  dependency-graph.md              # Cross-use-case dependencies (Mermaid)
  actors/
    {actor-slug}.md                # Actor profile (one per actor)
  cases/
    {UC-NNN}-{slug}/
      use-case.md                  # The use case itself (Cockburn template)
      slices/
        {SL-NNN}-{slug}.md         # Individual slice (one per slice)
  test-specs/
    {TS-NNN}-{slug}.md             # Individual test specification
  contracts/
    api/
      {endpoint-slug}.yaml         # OpenAPI spec per endpoint
    events/
      {event-slug}.yaml            # CloudEvents spec per event
    schemas/
      {entity-slug}.json           # JSON Schema per entity
```

#### Design principles

- **One artifact, one file**: No 500-line mega-documents. Each use case, slice, test spec, and contract is its own file.
- **Navigable**: Every file has frontmatter with ID, status, and cross-references. The index is the entry point. From any artifact, you can navigate to related artifacts.
- **Traversable**: Dependency graph shows relationships. Links are bidirectional. From a use case, find its slices, test specs, and contracts. From a contract, find the use case it implements.
- **Decomposed**: Strategic overview is concise. Index is dynamically generated by reading frontmatter. Details live in individual files. Casual-template files target 50-100 lines; fully-dressed files may extend to 200-250 lines.
- **Compatible**: File structure MUST work with `/worktracker` entity hierarchy. Use cases map to Features or Stories (see Jerry integration requirements for mapping rules). Slices map to Tasks.

### Jerry integration requirements

1. **`/worktracker` integration**: Use cases and slices MUST integrate with the worktracker entity hierarchy per `skills/worktracker/rules/worktracker-entity-hierarchy.md`. Recommended mapping: use cases at sea-level (user-goal) map to Features; use cases at fish-level (sub-function) map to Stories under their parent Feature; slices map to Tasks under their parent use case entity. The `UC-NNN` and `SL-NNN` IDs are use-case-domain identifiers — the worktracker entity gets its own `FEAT-NNN`/`STORY-NNN`/`TASK-NNN` ID per existing conventions, with the use case ID in frontmatter cross-references. The implementer MUST verify compatibility with WTI-001 through WTI-009 containment rules.

2. **Quality enforcement**: Two distinct quality scopes apply. (a) *Implementation deliverables* (SKILL.md files, agent definitions, templates) are subject to Jerry's quality gate (>= 0.92 for C2+) per `quality-enforcement.md`. (b) *Use case artifacts produced by the skill* (individual use cases, slices, test specs, contracts) should have quality validation workflows built into the skill — e.g., the reviewer agent validates completeness per Cockburn's heuristics. Criticality classification for implementation deliverables: the skills themselves are C3+ (multi-file, API surface). Criticality classification for skill-produced artifacts is determined by the user's project context.

3. **Existing skill compatibility**: The three skills must work alongside existing Jerry skills. `/problem-solving` for research phases. `/adversary` for quality reviews. `/orchestration` for multi-phase workflows when building out a full use case suite.

4. **Agent architecture compliance**: All agents must follow `agent-development-standards.md`. YAML frontmatter validates against JSON Schema. Constitutional compliance triplet (P-003, P-020, P-022) in every agent. Tool tiers per least-privilege principle.

5. **Skill standards compliance**: Skills follow `skill-standards.md`. SKILL.md with proper frontmatter. Kebab-case folders. No README.md inside skill folders. Registered in CLAUDE.md and AGENTS.md.

6. **Anthropic best practices**: Skills follow Anthropic's skill authoring best practices. Concise SKILL.md (under 500 lines). Progressive disclosure — SKILL.md as overview, detailed guidance in separate files loaded on demand. Descriptions in third person. Gerund-form or action-oriented naming. Evaluations built before extensive documentation.

7. **Individual file discipline**: Casual-template use cases should target 50-100 lines. Fully-dressed use cases may extend to 200-250 lines (Cockburn's fully-dressed template with 5+ extensions naturally requires this). When a use case exceeds 250 lines, decompose extensions into separate linked files (e.g., `extensions/{ext-slug}.md`). Slices, test specs, and contracts should target 50-100 lines each. The index and strategic overview are reference artifacts, not content dumps.

### What this does NOT include

- **Implementing the use cases themselves**: These skills help *write* use cases, test specs, and contracts. They don't implement the described system.
- **Replacing user stories**: Use cases and user stories coexist. Slices can function as enhanced user stories with traceability. This is an addition, not a replacement.
- **UML diagramming**: While use case diagrams are mentioned in methodology, this issue focuses on textual artifacts. Mermaid diagrams for dependency graphs and actor-goal maps are in scope; full UML tooling is not.
- **Prescribing the final architecture**: The file structure above is a recommended starting point. The implementer should research industry patterns and may propose alternatives with justification. The design principles (one file per artifact, navigable, traversable, decomposed, compatible) are the constraints; the specific directory layout is not.
- **CI/CD integration**: Automated validation of use case artifacts in CI pipelines is a future concern, not in scope for this issue.

### Acceptance criteria

- [ ] **Research deliverable**: Industry best practices for use case methodology, tooling, and file organization have been researched and documented. Research covers Jacobson's Use Case 2.0 (with chapter-level references), Cockburn's Writing Effective Use Cases (with chapter-level references), and at least 3 additional industry sources. The research deliverable MUST document specific findings that influenced design decisions — not just source enumeration.
- [ ] **Skill definitions**: All three skills (`/use-case`, `/test-spec`, `/contract-design`) have SKILL.md files that follow Anthropic's skill authoring best practices and Jerry's skill standards (H-25, H-26).
- [ ] **Agent definitions**: All agents have `.md` definition files with official Claude Code frontmatter and companion `.governance.yaml` files. All validate against `docs/schemas/agent-governance-v1.schema.json`. Constitutional compliance triplet present in every agent (H-34, H-35).
- [ ] **Guided experience**: The `/use-case` skill provides an interactive, guided workflow for creating use cases. The workflow collects actor, goal, scope, and scenario information through a structured prompt sequence (minimum 5 exchanges). Verification: the skill completes a full creation workflow for a simple use case (single actor, single goal, 1-2 extensions) and produces an artifact that passes the completeness checker against Cockburn's heuristics.
- [ ] **Template support**: Both casual and fully-dressed templates are available and selectable based on context.
- [ ] **Use case slicing**: The skill can decompose a use case into slices following Jacobson's slicing patterns (basic, precondition, alternative, error, enhancement). Each slice satisfies Jacobson's quality criteria: independently implementable, independently testable, and delivering demonstrable value.
- [ ] **Individual file organization**: Every use case, slice, test specification, and contract is an individual file. Casual-template use cases target 50-100 lines; fully-dressed use cases may extend to 200-250 lines; use cases exceeding 250 lines decompose extensions into separate files. All files have frontmatter with IDs and cross-references following a shared frontmatter schema defined during Phase 2.
- [ ] **Dependency graph**: A navigable dependency graph shows relationships between use cases, slices, and actors. Rendered in Mermaid. The graph is dynamically generated by the index agent reading use case frontmatter — not a static file that goes stale.
- [ ] **Index**: An auto-generated index lists all use cases with filtering by actor, goal level, status, and domain.
- [ ] **Strategic overview**: A concise overview shows: (a) an actor-goal matrix mapping actors to their use cases, (b) domain coverage summary (which functional areas have use cases and which don't), and (c) slice status counts (how many slices per use case, how many in each lifecycle state). The overview is a dashboard, not a narrative.
- [ ] **TDD/BDD generation**: The `/test-spec` skill generates TDD plans and BDD scenarios (in Given/When/Then format; specific BDD framework is an implementation decision) from use case artifacts. Every test traces to a specific use case scenario.
- [ ] **Contract generation**: The `/contract-design` skill generates at least one of: OpenAPI/Swagger, CloudEvents, AsyncAPI, or JSON Schema from use case interactions (which contract types are generated depends on the patterns identified in the use case). Every contract traces to a specific use case interaction.
- [ ] **Worktracker integration**: Use cases integrate with `/worktracker`. Use cases map to worktracker entities (Features/Stories). Slices map to Tasks.
- [ ] **Cross-referencing**: Bidirectional links exist between use cases, slices, test specs, and contracts. From any artifact, related artifacts are discoverable.
- [ ] **Shared frontmatter schema**: A shared frontmatter schema (documented in the architecture design phase) defines the data contract between the three skills. All three skills read and write use case artifact frontmatter using this schema.
- [ ] **Trigger map registration**: All three skills are registered in `mandatory-skill-usage.md` with trigger keywords, negative keywords, and priority per the enhanced 5-column format (H-22). Suggested trigger keywords: `/use-case` — "use case, actor, scenario, main success, extension, slice, goal level, precondition, postcondition"; `/test-spec` — "test specification, BDD, TDD, test plan, Given/When/Then, test coverage, acceptance criteria"; `/contract-design` — "contract, OpenAPI, Swagger, CloudEvents, AsyncAPI, JSON Schema, API spec, endpoint". Negative keywords and priority are determined during implementation. Skills are also registered in CLAUDE.md and AGENTS.md (H-26).
- [ ] **Quality compliance**: Implementation deliverables (SKILL.md, agent definitions) pass quality gate (>= 0.92 for C2+) per `quality-enforcement.md`.

#### AC-to-approach traceability

| Acceptance Criterion | Producing Phase | Key Steps |
|---------------------|----------------|-----------|
| Research deliverable | Phase 1 | Steps 1-5 |
| Skill definitions | Phase 3 | Steps 9-11 |
| Agent definitions | Phase 3 | Steps 9-11 |
| Guided experience | Phase 3 | Step 9 |
| Template support | Phase 3 | Step 9 |
| Use case slicing | Phase 3 | Step 9 |
| Individual file organization | Phase 2 | Steps 6-7 |
| Dependency graph | Phase 3 | Step 9 (index agent) |
| Index | Phase 3 | Step 9 (index agent) |
| Strategic overview | Phase 3 | Step 9 (index agent) |
| TDD/BDD generation | Phase 3 | Step 10 |
| Contract generation | Phase 3 | Step 11 |
| Worktracker integration | Phase 4 | Step 12 |
| Cross-referencing | Phase 4 | Step 13 |
| Shared frontmatter schema | Phase 2 | Step 7 |
| Trigger map registration | Phase 4 | Step 12 |
| Quality compliance | Phase 4 | Step 14 |

### Approach

The implementer should follow a research-first methodology:

#### Phase 1: Research

1. Deep-dive into Jacobson's Use Case 2.0 methodology. Read the e-book. Understand slicing patterns, the seven activities, and slice lifecycle states.
2. Deep-dive into Cockburn's Writing Effective Use Cases. Understand templates, goal levels, precision levels, and completeness heuristics.
3. Research at least 3 additional industry sources on use case patterns, modern requirements tooling, or use-case-driven development. Document findings.
4. Research Anthropic's skill authoring best practices. Understand progressive disclosure, token budgets, evaluation-driven development.
5. Analyze existing Jerry skills for patterns to follow (agent decomposition, file organization, integration patterns).

#### Phase 2: Architecture Design

6. Design the file organization for use case artifacts. Apply the design principles (one file per artifact, navigable, traversable, decomposed, compatible). Validate against the `/worktracker` entity hierarchy.
7. Design the cross-referencing and dependency graph approach. Define a **shared frontmatter schema** for use case artifacts — this is the data contract that all three skills consume and produce. The schema defines required fields (ID, type, status, actor, goal-level, cross-references) and how they map to `/worktracker` entity metadata. The schema should be defined as a formal specification (JSON Schema or equivalent) that can be validated programmatically — e.g., using `jerry ast validate` for frontmatter verification.
8. Design the skill decomposition — which agents handle which concerns, how they interact, what tools they need. Ensure all agents follow the orchestrator-worker topology (P-003 compliant).

#### Phase 3: Skill Implementation (sequential, with gates)

9. Implement `/use-case` skill — SKILL.md, agent definitions, templates, guided workflow. The guided workflow collects actor, goal, scope, and scenario information through a structured prompt sequence (minimum 5 exchanges per the Guided Experience AC). **Gate**: verify that the `/use-case` skill produces a complete use case artifact with frontmatter cross-references before proceeding. Create a sample use case to validate the output format — this sample is reused in Step 13 for end-to-end verification.
10. Implement `/test-spec` skill — SKILL.md, agent definitions, BDD/TDD generation. Build against the validated `/use-case` output format from step 9. **Gate**: verify that `/test-spec` can consume a `/use-case` artifact and produce test specifications with bidirectional traceability.
11. Implement `/contract-design` skill — SKILL.md, agent definitions, contract generation. Build against the validated `/use-case` output format. **Gate**: verify contract artifacts trace to use case interactions.

#### Phase 4: Integration and Verification

12. Integrate with `/worktracker`. Verify use cases and slices map to worktracker entities.
13. End-to-end verification: using the sample use case created in Step 9, slice it → generate test specs → generate contracts → verify all cross-references work. The sample should exercise at least: one sea-level use case with a primary actor, 2+ extensions, and a supporting actor. This sample serves as both a verification fixture and a usage example for new users.
14. Quality gate all deliverables per `quality-enforcement.md`.

### Why now

Jerry is preparing for open-source release. When users arrive, they're going to be building things — and building things right means knowing what you're building before you build it. Use cases are the bridge between "we need a feature" and "here's exactly what that feature does, how to verify it, and how to implement it."

Right now, Jerry has skills for tracking work (`/worktracker`), solving problems (`/problem-solving`), enforcing quality (`/adversary`), and orchestrating workflows (`/orchestration`). What's missing is the front end of the pipeline — the part where you figure out *what the system should do* in enough detail that everything downstream has a clear target.

You can't ski a line you can't see. Use cases are how you see the line. And once you see it, everything else — tests, contracts, implementation — is just following the fall line.

This issue is part of the OSS release preparation work.
