# NPT-013 Constraints -- Use Case Skill Implementation (Issue #109)

<!-- VERSION: 1.0.0 | DATE: 2026-03-08 | SOURCE: pe-constraint-gen for PROJ-021 -->

> Domain-specific constraints for implementing three skills (`/use-case`, `/test-spec`, `/contract-design`) per GitHub Issue #109. These constraints supplement the general Jerry operating tenets (C-001 through C-030) with implementation-specific guardrails.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Methodology Adherence](#methodology-adherence) | Jacobson and Cockburn fidelity constraints |
| [Skill Boundary Discipline](#skill-boundary-discipline) | Clean separation between three skills |
| [Agent Architecture Compliance](#agent-architecture-compliance) | H-34 and structural pattern adherence |
| [File Organization and Frontmatter](#file-organization-and-frontmatter) | One-artifact-one-file and schema discipline |
| [Cross-Referencing and Traceability](#cross-referencing-and-traceability) | Bidirectional link integrity |
| [Sequential Gate Discipline](#sequential-gate-discipline) | Phase ordering and gate enforcement |
| [Template and Research Fidelity](#template-and-research-fidelity) | Source faithfulness and citation integrity |
| [Integration Compatibility](#integration-compatibility) | Compatibility with existing Jerry skills |
| [Summary Table](#summary-table) | Constraint ID to domain area mapping |

---

## Methodology Adherence

<constraint id="UC-001" format="NPT-013">
NEVER invent use case methodology concepts that do not exist in the source texts (Jacobson Use Case 2.0, Cockburn Writing Effective Use Cases, or additional Phase 1 research sources).
  -- Consequence: Fabricated methodology contaminates the skill's theoretical foundation, producing artifacts that mislead users and cannot be validated against authoritative references.
  Instead: Reference methodology concepts structurally (e.g., "goal-level hierarchy per Cockburn", "slice concept per Jacobson") and defer precise definitions to Phase 1 research verification against actual source material.
</constraint>

<constraint id="UC-002" format="NPT-013">
NEVER conflate Jacobson's Use Case 2.0 slice concept with Cockburn's goal-level hierarchy as if they are interchangeable.
  -- Consequence: Mixing incompatible abstractions produces a hybrid methodology that is neither Jacobson nor Cockburn, confusing users who know the source material and producing internally inconsistent artifacts.
  Instead: Treat Jacobson's slicing and Cockburn's goal-level structuring as complementary but distinct lenses. Phase 1 research must explicitly map where they align, where they diverge, and how the `/use-case` skill synthesizes them.
</constraint>

<constraint id="UC-003" format="NPT-013">
NEVER reduce use case authoring to a template fill-in exercise that bypasses the analytical thinking each methodology requires (goal identification per Cockburn, narrative flow per Jacobson).
  -- Consequence: Users produce structurally valid but analytically hollow use cases -- templates filled with placeholder-quality content that cannot drive meaningful test specs or contracts downstream.
  Instead: The `/use-case` skill must guide analytical decisions (goal level selection, actor identification, scope bounding, slice decomposition) before presenting templates. Templates are the output format, not the methodology.
</constraint>

---

## Skill Boundary Discipline

<constraint id="UC-004" format="NPT-013">
NEVER allow `/use-case` agents to generate test specifications or contract schemas as part of use case authoring.
  -- Consequence: Capability bleed between skills makes `/test-spec` and `/contract-design` redundant, breaks the sequential gate model, and produces untraceable artifacts that bypass quality gates.
  Instead: `/use-case` produces use case artifacts (use cases, slices, actor catalogs). Test generation is exclusively `/test-spec`. Contract generation is exclusively `/contract-design`. Cross-skill outputs are linked via frontmatter references, never inlined.
</constraint>

<constraint id="UC-005" format="NPT-013">
NEVER allow `/test-spec` to modify or extend the use case artifacts it consumes as input.
  -- Consequence: Upstream artifacts become inconsistent with the source-of-truth use case, breaking bidirectional traceability and invalidating other downstream consumers (e.g., `/contract-design`) that depend on the original use case.
  Instead: `/test-spec` reads use case artifacts as immutable inputs. If the test generation process reveals gaps in the use case, `/test-spec` must emit a structured gap report referencing the specific use case artifact and section -- the user then returns to `/use-case` to resolve the gap.
</constraint>

<constraint id="UC-006" format="NPT-013">
NEVER duplicate domain logic (actor resolution, goal-level classification, scope validation) across multiple skills.
  -- Consequence: Duplicated logic drifts out of sync across skills, producing inconsistent classifications and validation results depending on which skill the user invoked.
  Instead: Define shared domain concepts in the shared frontmatter schema. Each skill reads the schema-defined fields from upstream artifacts rather than re-deriving them. If a domain concept (e.g., goal-level classification) is needed by multiple skills, it must be set once during `/use-case` authoring and consumed read-only downstream.
</constraint>

---

## Agent Architecture Compliance

<constraint id="UC-007" format="NPT-013">
NEVER create agent definition files that omit the dual-file architecture required by H-34: both an `.md` file (with official Claude Code frontmatter only) and a companion `.governance.yaml` file (validated against `docs/schemas/agent-governance-v1.schema.json`).
  -- Consequence: Agent definitions that skip the governance YAML bypass schema validation at L3 and L5, miss the constitutional triplet check (P-003, P-020, P-022), and cannot be verified for tool tier compliance.
  Instead: Every agent across all three skills must have both files. Create the `.governance.yaml` first (schema-first), then write the `.md` file. Validate governance YAML against the JSON Schema before writing the agent markdown body.
</constraint>

<constraint id="UC-008" format="NPT-013">
NEVER assign a worker agent the Task tool or a T5 tool tier.
  -- Consequence: Workers with Task tool access can spawn recursive subagents, violating P-003 (H-01) and breaking the orchestrator-worker topology. This causes unbounded recursion and context exhaustion.
  Instead: Worker agents must be T1 through T4. Only the SKILL.md orchestrator context (the main context invoking agents via Task) operates at T5. Verify each agent's `tool_tier` in `.governance.yaml` and `tools` in `.md` frontmatter -- no worker lists `Task`.
</constraint>

<constraint id="UC-009" format="NPT-013">
NEVER select a cognitive mode without justifying it against the cognitive mode taxonomy in agent-development-standards.md.
  -- Consequence: Mismatched cognitive modes degrade agent output quality. A research agent assigned `systematic` mode will procedurally check items rather than divergently exploring sources. An auditor assigned `divergent` mode will explore broadly rather than systematically verifying compliance.
  Instead: Match mode to agent function per the taxonomy: `divergent` for research/exploration agents, `convergent` for analysis/evaluation agents, `integrative` for synthesis agents, `systematic` for validation/auditing agents. Document the selection rationale in the `.governance.yaml` identity section.
</constraint>

---

## File Organization and Frontmatter

<constraint id="UC-010" format="NPT-013">
NEVER produce a multi-entity artifact file that combines multiple use cases, multiple slices, or multiple test specifications into a single document.
  -- Consequence: Multi-entity files break frontmatter-based metadata extraction (H-33 AST parsing), prevent granular cross-referencing, and make individual entity status tracking impossible via `/worktracker`.
  Instead: One artifact per file. Each use case gets its own file with its own frontmatter. Each slice gets its own file. Each test specification gets its own file. Each contract gets its own file. Directory structure provides the grouping that mega-files attempt to provide inline.
</constraint>

<constraint id="UC-011" format="NPT-013">
NEVER create use case, slice, test spec, or contract artifact files without YAML frontmatter containing at minimum: entity type, entity ID, title, status, parent reference, and creation date.
  -- Consequence: Artifacts without frontmatter are invisible to Jerry's AST-based tooling (H-33), cannot be tracked by `/worktracker`, cannot be cross-referenced by downstream skills, and cannot participate in status rollup or traceability reporting.
  Instead: Design the shared frontmatter schema in Phase 2 before any artifact creation in Phase 3. Every artifact file must begin with a YAML frontmatter block that validates against the shared schema. The schema must be defined as a JSON Schema document and referenced by all three skills.
</constraint>

---

## Cross-Referencing and Traceability

<constraint id="UC-012" format="NPT-013">
NEVER create a downstream artifact (test spec, contract) without including a frontmatter field that references the specific upstream use case or slice it derives from.
  -- Consequence: Without upstream references, traceability is broken. Users cannot navigate from a contract back to its originating use case. Gap analysis becomes impossible -- there is no way to determine which use cases lack test coverage or contract definitions.
  Instead: Every test spec frontmatter must include a `source_use_case` (or `source_slice`) field with the entity ID of its upstream artifact. Every contract must include the same. These references must be validated for existence before the artifact is considered complete.
</constraint>

<constraint id="UC-013" format="NPT-013">
NEVER allow a partial update to a use case artifact without propagating a staleness signal to its downstream dependents (test specs, contracts).
  -- Consequence: Downstream artifacts silently become stale when their upstream use case changes. Users trust test specs and contracts that no longer reflect the current use case definition, producing false confidence in coverage.
  Instead: Define a `last_modified` or `revision` field in the shared frontmatter schema. When `/use-case` modifies an artifact, downstream artifacts referencing it should be flaggable as potentially stale. The mechanism may be a simple date comparison or a revision counter -- design the specific approach in Phase 2 architecture.
</constraint>

---

## Sequential Gate Discipline

<constraint id="UC-014" format="NPT-013">
NEVER begin Phase 3 skill implementation for `/test-spec` before `/use-case` has passed its quality gate (H-13, score >= 0.92).
  -- Consequence: Building test generation against an unfinished or substandard use case skill produces downstream work that must be reworked when `/use-case` changes. The sequential dependency is the core architectural decision -- bypassing it undermines the entire three-skill pipeline.
  Instead: Phase 3 proceeds strictly: `/use-case` implementation and quality gate, then `/test-spec` implementation and quality gate, then `/contract-design` implementation and quality gate. Each gate must be explicitly passed before the next skill's implementation begins.
</constraint>

<constraint id="UC-015" format="NPT-013">
NEVER begin `/contract-design` implementation before `/test-spec` has been implemented and gated, even if `/use-case` artifacts are available.
  -- Consequence: Contracts designed without the test specification intermediate step may miss interaction patterns that test generation surfaces. The three-skill pipeline is sequential by design -- `/test-spec` validates use case completeness before `/contract-design` encodes it into technical contracts.
  Instead: Respect the full sequence: `/use-case` -> gate -> `/test-spec` -> gate -> `/contract-design` -> gate. If time pressure demands parallel work, document the deviation with justification per MEDIUM override protocol and accept the rework risk.
</constraint>

---

## Template and Research Fidelity

<constraint id="UC-016" format="NPT-013">
NEVER ship use case templates (casual or fully-dressed per Cockburn terminology) that have not been verified against the actual source text during Phase 1 research.
  -- Consequence: Templates that misrepresent the methodology teach users incorrect practices. Once shipped, incorrect templates propagate through every use case authored with the skill and are expensive to remediate.
  Instead: Phase 1 research must produce explicit template validation artifacts that cite the source text section, page, or chapter where each template element is defined. Templates produced in Phase 3 must trace every field and section back to a Phase 1 research citation.
</constraint>

<constraint id="UC-017" format="NPT-013">
NEVER cite fewer than 3 additional sources beyond Jacobson and Cockburn in Phase 1 research.
  -- Consequence: A two-source research base is too narrow to validate methodology synthesis. Additional sources (industry patterns, comparative analyses, practitioner guides) provide the triangulation needed to identify where the primary sources have gaps or where industry practice has evolved beyond the original texts.
  Instead: Phase 1 research must include Jacobson (Use Case 2.0), Cockburn (Writing Effective Use Cases), and at minimum 3 additional sources. Additional sources may include: industry pattern catalogs, Jerry skill implementation patterns (existing skills as structural references), modern use case practice surveys, or domain-specific adaptations. Each source must be cited with enough specificity to be verifiable.
</constraint>

<constraint id="UC-018" format="NPT-013">
NEVER fabricate bibliographic references, page numbers, chapter citations, or direct quotes attributed to Jacobson or Cockburn.
  -- Consequence: Fabricated citations are unverifiable and constitute a P-022 (no deception) violation. Users who attempt to verify the methodology against source material will discover the fabrication, destroying trust in the skill and the framework.
  Instead: Use structural references ("per Jacobson's slice concept", "per Cockburn's goal-level hierarchy") rather than specific page or chapter citations unless the exact reference has been verified via Context7 or direct source consultation during Phase 1. Mark any unverified structural reference with a `[VERIFY-PHASE-1]` tag for explicit verification during research.
</constraint>

---

## Integration Compatibility

<constraint id="UC-019" format="NPT-013">
NEVER design artifact frontmatter schemas that are incompatible with Jerry's existing AST-based parsing (H-33) or worktracker entity hierarchy.
  -- Consequence: Artifacts that cannot be parsed by `jerry ast frontmatter` or validated by `jerry ast validate` are invisible to the framework's tooling layer. This breaks worktracker integration, status tracking, and the quality enforcement pipeline.
  Instead: Design artifact frontmatter to be a superset of Jerry's standard entity frontmatter pattern. Include the standard fields (type, id, title, status, parent) that worktracker expects, then extend with domain-specific fields (goal_level, actors, slices). Validate the schema against existing AST parsing capabilities during Phase 2 architecture.
</constraint>

<constraint id="UC-020" format="NPT-013">
NEVER design the three skills' trigger keywords to collide with existing skill trigger maps in mandatory-skill-usage.md without adding negative keywords for disambiguation.
  -- Consequence: Keyword collisions cause misrouting (AP-02 Bag of Triggers anti-pattern). Users saying "requirements" could route to `/nasa-se` instead of `/use-case`, or vice versa. Without negative keywords, the routing layer cannot disambiguate.
  Instead: During Phase 2 architecture, cross-reference all proposed trigger keywords against the existing trigger map (mandatory-skill-usage.md). Add negative keywords to both the new skills and any existing skills that share vocabulary. Register all three skills in the 5-column enhanced trigger map format with priority ordering and compound triggers.
</constraint>

<constraint id="UC-021" format="NPT-013">
NEVER register the three new skills in CLAUDE.md, AGENTS.md, or mandatory-skill-usage.md before they have passed their Phase 3 quality gates.
  -- Consequence: Registering incomplete skills causes them to be routed to by the trigger map, invoked by H-22 proactive skill invocation, and loaded into session context -- all before they are ready. Users experience broken skill invocations and corrupted session context.
  Instead: Registration is the final step of Phase 4 (Integration and Verification). Skills are developed and gated in Phase 3 without registration. Phase 4 performs integration testing, then registers all three skills simultaneously in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md.
</constraint>

<constraint id="UC-022" format="NPT-013">
NEVER design `/use-case` skill output in a format that `/adversary` cannot consume for quality scoring via S-014 LLM-as-Judge.
  -- Consequence: Use case artifacts that lack clear structure, section boundaries, or evaluable content prevent the adversary skill from applying its 6-dimension quality rubric. This means use case artifacts bypass the quality gate (H-13), undermining the entire quality enforcement pipeline.
  Instead: Design use case artifact structure with explicit sections that map to the S-014 quality dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability). The artifact format must be reviewable by `/adversary` without skill-specific customization.
</constraint>

---

## Summary Table

| Constraint ID | Domain Area | Prohibited Action (Summary) |
|---------------|-------------|----------------------------|
| UC-001 | Methodology Adherence | Inventing methodology concepts not in source texts |
| UC-002 | Methodology Adherence | Conflating Jacobson slicing with Cockburn goal-levels |
| UC-003 | Methodology Adherence | Reducing authoring to template fill-in without analytical guidance |
| UC-004 | Skill Boundary Discipline | `/use-case` generating test specs or contracts |
| UC-005 | Skill Boundary Discipline | `/test-spec` modifying upstream use case artifacts |
| UC-006 | Skill Boundary Discipline | Duplicating domain logic across skills |
| UC-007 | Agent Architecture Compliance | Omitting dual-file architecture (H-34) |
| UC-008 | Agent Architecture Compliance | Assigning Task tool or T5 tier to worker agents |
| UC-009 | Agent Architecture Compliance | Selecting cognitive mode without taxonomy justification |
| UC-010 | File Organization and Frontmatter | Multi-entity artifact files |
| UC-011 | File Organization and Frontmatter | Artifact files without YAML frontmatter |
| UC-012 | Cross-Referencing and Traceability | Downstream artifacts without upstream references |
| UC-013 | Cross-Referencing and Traceability | Partial updates without staleness propagation |
| UC-014 | Sequential Gate Discipline | Starting `/test-spec` before `/use-case` gates |
| UC-015 | Sequential Gate Discipline | Starting `/contract-design` before `/test-spec` gates |
| UC-016 | Template and Research Fidelity | Shipping unverified templates |
| UC-017 | Template and Research Fidelity | Citing fewer than 3 additional research sources |
| UC-018 | Template and Research Fidelity | Fabricating bibliographic references |
| UC-019 | Integration Compatibility | Frontmatter incompatible with AST parsing (H-33) |
| UC-020 | Integration Compatibility | Trigger keyword collisions without disambiguation |
| UC-021 | Integration Compatibility | Registering skills before quality gates pass |
| UC-022 | Integration Compatibility | Output format incompatible with `/adversary` scoring |

---

<!-- VERSION: 1.0.0 | DATE: 2026-03-08 | SOURCE: pe-constraint-gen for PROJ-021, Issue #109 -->
*Constraints Version: 1.0.0*
*Agent: pe-constraint-gen v1.0.0*
*Domain: Use Case Skill Implementation (Issue #109)*
*Constraint Count: 22 (range: 15-25)*
*Format: NPT-013*
*Created: 2026-03-08*
