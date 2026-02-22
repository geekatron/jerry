---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Configuration Baseline: Claude Code Agent Development Patterns

> **Project:** PROJ-007-agent-patterns
> **Date:** 2026-02-21
> **Status:** Draft
> **NASA Process:** NPR 7123.1D Process 9 (Configuration Management)
> **Agent:** nse-configuration-001 v1.0.0
> **Cognitive Mode:** Systematic
> **Criticality:** C4 (Configuration baseline for architecture/governance patterns)
> **Inputs:** nse-requirements-001 (52 requirements), nse-verification-001 (V&V plan), nse-integration-001 (integration patterns), PS-to-NSE barrier-3 handoff (8 configuration items), ADR-PROJ007-001, ADR-PROJ007-002

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language overview of the configuration baseline |
| [1. Baseline Definition](#1-baseline-definition) | What constitutes the v1.0.0 agent patterns baseline |
| [2. Configuration Items (CIs)](#2-configuration-items-cis) | All baselined artifacts with naming, versioning, and status |
| [3. Change Control Process](#3-change-control-process) | How to propose, review, and approve changes |
| [4. Versioning Strategy](#4-versioning-strategy) | Semantic versioning rules specific to agent patterns |
| [5. Baseline Validation Criteria](#5-baseline-validation-criteria) | Acceptance tests and quality gate requirements |
| [6. Traceability Matrix](#6-traceability-matrix) | CIs mapped to requirements and ADR decisions |
| [Self-Review (S-010)](#self-review-s-010) | Pre-delivery quality verification |
| [References](#references) | Source document traceability |

---

## L0: Executive Summary

This document establishes the configuration management baseline for the Claude Code agent development patterns produced by PROJ-007. It answers the question: **what artifacts are controlled, how are they versioned, and what process governs changes?**

The baseline comprises 8 configuration items (CIs) that together define how agents are structured, validated, routed, handed off, quality-gated, and governed within the Jerry framework. These CIs range from a JSON Schema for agent definition validation (the highest-priority single deliverable) to circuit breaker parameters that govern iteration and routing depth limits.

Key elements of this configuration baseline:

1. **8 Configuration Items.** Each CI has a unique identifier (CI-001 through CI-008), a semantic version, a defined owner, and a criticality classification that determines the change control rigor required for modifications.

2. **Change Control Process.** Changes to baselined CIs follow a criticality-proportional review process aligned with quality-enforcement.md. Changes to CI-001 (JSON Schema) or CI-002 (ADR-001) trigger AE-004 (auto-C4). Changes to CI-004 (trigger map rules) trigger AE-002 (auto-C3).

3. **Semantic Versioning.** All CIs use MAJOR.MINOR.PATCH versioning with explicit criteria for when each version component increments. Schema evolution follows the rules established in ADR-PROJ007-001: MINOR for additions (new optional fields, new enum values), MAJOR for breaking changes (field removal, constraint tightening).

4. **Baseline Validation.** A baseline release must pass 7 validation gates: schema self-consistency, agent definition compliance, cross-CI consistency, V&V plan coverage, quality gate threshold, constitutional compliance, and regression non-degradation.

This is a C4-criticality document because it establishes the governance framework for all future agent pattern changes. Once accepted, modifications to this baseline trigger AE-004 (auto-C4).

---

## 1. Baseline Definition

### 1.1 Baseline Scope

The agent patterns baseline (designated **APB-1.0.0**) encompasses all artifacts that define, validate, route, integrate, and govern Claude Code agents within the Jerry framework. The baseline is the set of approved, controlled configuration items from which all future agent development derives.

**Baseline boundary:** The baseline covers agent development standards and their supporting artifacts. It does not cover individual agent definition files (those are governed by the baseline but are not CIs themselves), operational worktracker data, or session-specific orchestration artifacts.

### 1.2 Baseline Contents (v1.0.0)

| Category | Artifacts | Count |
|----------|-----------|-------|
| Architecture Decision Records | ADR-PROJ007-001 (Agent Definition Format), ADR-PROJ007-002 (Routing and Trigger Framework) | 2 |
| JSON Schemas | Agent definition schema (Draft 2020-12), Handoff protocol schema v2 | 2 |
| Rule Files | Enhanced trigger map rules (mandatory-skill-usage.md enhancements) | 1 |
| Templates | Canonical agent definition template | 1 |
| Catalogs | Anti-pattern catalog (8 routing + 10 general), Pattern taxonomy (66 patterns, 8 families) | 2 |
| Parameters | Cognitive mode enum, tool security tiers, circuit breaker parameters, context budget rules | 4 (grouped into CIs) |
| **Total Configuration Items** | | **8** |

### 1.3 Artifact Inventory

All paths are relative to the repository root.

| # | Artifact | Current Location | Baseline Target Location | Format |
|---|----------|------------------|--------------------------|--------|
| 1 | Agent Definition JSON Schema | ADR-PROJ007-001 Section 2 (inline) | `docs/schemas/agent-definition-v1.0.0.json` | JSON Schema Draft 2020-12 |
| 2 | Handoff Protocol JSON Schema | nse-integration-001 Section 1.2 (inline) | `docs/schemas/agent-handoff-v2.0.0.json` | JSON Schema Draft 2020-12 |
| 3 | Canonical Agent Definition Template | ADR-PROJ007-001 Section 1 (inline) | `docs/templates/agent-definition-template-v1.0.0.md` | YAML + Markdown |
| 4 | ADR-PROJ007-001: Agent Definition Format | PS Phase 3 synthesis | `docs/design/ADR-PROJ007-001.md` | Markdown (Nygard ADR format) |
| 5 | ADR-PROJ007-002: Routing and Trigger Framework | PS Phase 3 synthesis | `docs/design/ADR-PROJ007-002.md` | Markdown (Nygard ADR format) |
| 6 | Enhanced Trigger Map Specification | ADR-PROJ007-002 Section 2.2 | `.context/rules/mandatory-skill-usage.md` (update) | Markdown table |
| 7 | Anti-Pattern Catalog | ADR-PROJ007-002 Section 5; nse-verification-001 Section 4 | `docs/knowledge/anti-pattern-catalog.md` | Markdown |
| 8 | Pattern Taxonomy | ps-synthesizer-001 synthesis | `docs/knowledge/agent-pattern-taxonomy.md` | Markdown |

### 1.4 Baseline Identification

| Property | Value |
|----------|-------|
| **Baseline ID** | APB-1.0.0 |
| **Baseline Name** | Agent Patterns Baseline v1.0.0 |
| **Effective Date** | Pending acceptance of ADR-PROJ007-001 and ADR-PROJ007-002 |
| **Predecessor** | None (first baseline for agent patterns) |
| **Governing Document** | This configuration baseline (nse-configuration-001) |
| **Quality Gate** | >= 0.92 weighted composite per quality-enforcement.md |
| **Criticality** | C4 (irreversible architecture/governance baseline) |

---

## 2. Configuration Items (CIs)

### 2.1 CI Naming Convention

Configuration items follow the pattern: `CI-{NNN}: {Short Name}`

- **NNN:** Zero-padded three-digit sequential identifier.
- **Short Name:** Human-readable descriptor.
- **Version:** Semantic versioning (MAJOR.MINOR.PATCH) per Section 4.
- **Status Lifecycle:** Draft -> Proposed -> Accepted -> Baselined -> Superseded | Deprecated.

### 2.2 CI Registry

#### CI-001: Agent Definition JSON Schema

| Property | Value |
|----------|-------|
| **ID** | CI-001 |
| **Name** | Agent Definition JSON Schema |
| **Version** | 1.0.0 |
| **Status** | Proposed |
| **Format** | JSON Schema Draft 2020-12 |
| **Target Path** | `docs/schemas/agent-definition-v1.0.0.json` |
| **Schema ID** | `https://jerry-framework.dev/schemas/agent-definition/v1.0.0` |
| **Owner** | Framework Maintainers (SH-3) |
| **Criticality** | C4 (modification triggers AE-004) |
| **Source** | ADR-PROJ007-001 Section 2 |
| **Content Summary** | JSON Schema validating YAML frontmatter of agent definitions. Covers 9 required top-level fields, 4 recommended fields, enum constraints for `model` (3 values), `cognitive_mode` (5 values), `fallback_behavior` (3 values), name pattern `^[a-z]+-[a-z]+(-[a-z0-9]+)*$`, version pattern `^\d+\.\d+\.\d+$`, `allowed_tools` enum (16 tools across T1-T5 tiers), minimum counts for `expertise` (2), `forbidden_actions` (3), `output_filtering` (3), `principles_applied` (3). |
| **Dependencies** | CI-003 (template defines the fields schema validates), CI-005 (cognitive mode enum) |

#### CI-002: ADR-PROJ007-001 (Agent Definition Format and Design Patterns)

| Property | Value |
|----------|-------|
| **ID** | CI-002 |
| **Name** | ADR-PROJ007-001: Agent Definition Format |
| **Version** | 1.0.0 |
| **Status** | Proposed |
| **Format** | Markdown (Nygard ADR format) |
| **Target Path** | `docs/design/ADR-PROJ007-001.md` |
| **Owner** | Framework Maintainers (SH-3) |
| **Criticality** | C4 (baselined ADR; modification triggers AE-004) |
| **Source** | ps-architect-001 synthesis |
| **Content Summary** | Architecture Decision Record codifying 7 design components: canonical template, JSON Schema, hexagonal architecture mapping, T1-T5 tool security tiers, 5-mode cognitive taxonomy, progressive disclosure structure, guardrails template. Resolves OI-01, OI-03, OI-04. Includes migration path for 37 existing agents. |
| **Dependencies** | CI-001 (schema is a component of this ADR), CI-003 (template is a component) |

#### CI-003: Canonical Agent Definition Template

| Property | Value |
|----------|-------|
| **ID** | CI-003 |
| **Name** | Canonical Agent Definition Template |
| **Version** | 1.0.0 |
| **Status** | Proposed |
| **Format** | YAML frontmatter + Markdown body |
| **Target Path** | `docs/templates/agent-definition-template-v1.0.0.md` |
| **Owner** | Framework Maintainers (SH-3) |
| **Criticality** | C3 (template change affects all new agent development; AE-002 if placed in rules) |
| **Source** | ADR-PROJ007-001 Section 1 |
| **Content Summary** | Complete YAML + Markdown template consolidating AR-001 through AR-012 and PR-001 through PR-008. Fields classified as REQUIRED (9 top-level) or RECOMMENDED (4 top-level: persona, validation, session_context, enforcement). Includes inline documentation of field purposes, constraints, and selection criteria. |
| **Dependencies** | CI-001 (schema validates this template), CI-005 (cognitive mode enum) |

#### CI-004: ADR-PROJ007-002 (Routing and Trigger Framework)

| Property | Value |
|----------|-------|
| **ID** | CI-004 |
| **Name** | ADR-PROJ007-002: Routing and Trigger Framework |
| **Version** | 1.0.0 |
| **Status** | Proposed |
| **Format** | Markdown (Nygard ADR format) |
| **Target Path** | `docs/design/ADR-PROJ007-002.md` |
| **Owner** | Framework Maintainers (SH-3) |
| **Criticality** | C4 (baselined ADR; modification triggers AE-004) |
| **Source** | ps-architect-002 synthesis |
| **Content Summary** | Architecture Decision Record codifying 7 design components: layered routing architecture (L0-L3 + terminal), enhanced trigger map (5-column format with negative keywords, priority, compound triggers), circuit breaker specification (max 3 hops), multi-skill combination protocol, 8 anti-pattern catalog, scaling roadmap (4 phases), routing observability format. Resolves OI-02, OI-07. |
| **Dependencies** | CI-006 (trigger map is the operational implementation of this ADR's routing decisions) |

#### CI-005: Cognitive Mode Enum and Tool Security Tiers

| Property | Value |
|----------|-------|
| **ID** | CI-005 |
| **Name** | Cognitive Mode Enum and Tool Security Tiers |
| **Version** | 1.0.0 |
| **Status** | Proposed |
| **Format** | Embedded in CI-001 (JSON Schema) and CI-002 (ADR) |
| **Target Path** | Governed by CI-001 schema; reference documentation in CI-002 Sections 4-5 |
| **Owner** | Framework Maintainers (SH-3) |
| **Criticality** | C3 (enum changes propagate to schema and all agent definitions) |
| **Source** | ADR-PROJ007-001 Sections 4-5 |
| **Content Summary** | **Cognitive Modes (5):** `divergent`, `convergent`, `integrative`, `systematic`, `forensic`. Consolidated from 8 modes with documented subsumption rationale: `strategic` -> `convergent`, `critical` -> `convergent`, `communicative` -> `divergent`. **Tool Security Tiers (5):** T1 (Read-Only: Read/Glob/Grep), T2 (Read-Write: +Write/Edit/Bash), T3 (External: +WebSearch/WebFetch/Context7), T4 (Persistent: +Memory-Keeper), T5 (Full: +Task). Selection rule: lowest tier that satisfies requirements. |
| **Dependencies** | CI-001 (schema enforces these enums), CI-003 (template references these values) |

#### CI-006: Enhanced Trigger Map Specification

| Property | Value |
|----------|-------|
| **ID** | CI-006 |
| **Name** | Enhanced Trigger Map Specification |
| **Version** | 1.0.0 |
| **Status** | Proposed |
| **Format** | Markdown table (4-column: Keywords, Negative Keywords, Priority, Skill) |
| **Target Path** | `.context/rules/mandatory-skill-usage.md` (update existing file) |
| **Owner** | Framework Maintainers (SH-3) |
| **Criticality** | C3 (AE-002: touches `.context/rules/`, auto-C3 minimum) |
| **Source** | ADR-PROJ007-002 Section 2.2; nse-integration-001 Section 4.1.1 |
| **Content Summary** | Enhanced trigger map expanding from 2-column format to 4-column format. Covers all 7 triggered skills with: positive keywords (expanded), negative keywords (new), priority ordering (1=highest, new), skill target. Priority rationale: `/orchestration` (1), `/transcript` (2), `/saucer-boy` (3), `/saucer-boy-framework-voice` (4), `/nasa-se` (5), `/problem-solving` (6), `/adversary` (7). 4 documented collision zones resolved with negative keywords. |
| **Dependencies** | CI-004 (ADR-002 defines the design rationale for this operational configuration) |

#### CI-007: Circuit Breaker and Iteration Parameters

| Property | Value |
|----------|-------|
| **ID** | CI-007 |
| **Name** | Circuit Breaker and Iteration Parameters |
| **Version** | 1.0.0 |
| **Status** | Proposed |
| **Format** | Embedded in CI-004 (ADR) and nse-integration-001 Section 6 |
| **Target Path** | Governed by CI-004; operational parameters in orchestration code |
| **Owner** | Framework Maintainers (SH-3) |
| **Criticality** | C3 (parameter changes affect all orchestration workflows) |
| **Source** | ADR-PROJ007-002 Section 3; nse-integration-001 Section 6 |
| **Content Summary** | **Routing Depth:** Max 3 hops before circuit breaker (RR-006). **Iteration Ceilings:** C1=3 max, C2=5 max, C3=7 max, C4=10 max. **Quality Score Plateau:** Delta < 0.01 for 3 consecutive iterations triggers circuit breaker. **Context Budget Rules:** CB-01 (reserve >= 5% for output), CB-02 (tool results <= 50% context), CB-03 (file paths over inline content), CB-04 (key_findings 3-5 bullets), CB-05 (offset/limit for files > 500 lines). **LLM Routing Confidence Threshold:** 0.70 (provisional, pending empirical calibration). |
| **Dependencies** | CI-004 (ADR-002 defines the design rationale), quality-enforcement.md (H-14 defines minimum iterations) |

#### CI-008: Handoff Protocol Schema v2

| Property | Value |
|----------|-------|
| **ID** | CI-008 |
| **Name** | Handoff Protocol JSON Schema v2 |
| **Version** | 2.0.0 |
| **Status** | Proposed |
| **Format** | JSON Schema Draft 2020-12 |
| **Target Path** | `docs/schemas/agent-handoff-v2.0.0.json` |
| **Owner** | Framework Maintainers (SH-3) |
| **Criticality** | C4 (handoff schema change affects all agent-to-agent communication) |
| **Source** | nse-integration-001 Section 1.2 |
| **Content Summary** | Complete JSON Schema for agent-to-agent handoffs. 9 required fields: `from_agent`, `to_agent`, `task`, `success_criteria`, `artifacts`, `key_findings`, `blockers`, `confidence`, `criticality`. 5 optional fields: `constraints`, `routing_metadata`, `quality_context`, `task_id`. Send-side validation (SV-01 through SV-09) and receive-side validation (RV-01 through RV-05). Extends AGENTS.md v1 protocol (4 fields) to validated API contract (14 fields). |
| **Dependencies** | CI-002 (ADR-001 `session_context` references handoff schema), CI-004 (ADR-002 routing metadata flows into handoff) |

### 2.3 CI Status Summary

| CI ID | Name | Version | Status | Criticality |
|-------|------|---------|--------|-------------|
| CI-001 | Agent Definition JSON Schema | 1.0.0 | Proposed | C4 |
| CI-002 | ADR-PROJ007-001 | 1.0.0 | Proposed | C4 |
| CI-003 | Canonical Agent Definition Template | 1.0.0 | Proposed | C3 |
| CI-004 | ADR-PROJ007-002 | 1.0.0 | Proposed | C4 |
| CI-005 | Cognitive Mode Enum and Tool Security Tiers | 1.0.0 | Proposed | C3 |
| CI-006 | Enhanced Trigger Map Specification | 1.0.0 | Proposed | C3 |
| CI-007 | Circuit Breaker and Iteration Parameters | 1.0.0 | Proposed | C3 |
| CI-008 | Handoff Protocol Schema v2 | 2.0.0 | Proposed | C4 |

---

## 3. Change Control Process

### 3.1 Change Proposal

Any modification to a baselined CI requires a formal change proposal. The proposal mechanism depends on the change type:

| Change Type | Proposal Mechanism | Required Content |
|-------------|-------------------|------------------|
| New CI addition | New ADR or amendment to existing ADR | Context, decision, consequences, traceability |
| CI field addition (non-breaking) | MINOR version proposal in worktracker entry | Field specification, backward compatibility analysis, affected agents |
| CI field removal or constraint tightening (breaking) | MAJOR version proposal as new ADR | Migration plan, impact assessment on all consumers, deprecation timeline |
| Parameter tuning | PATCH version proposal in worktracker entry | Current value, proposed value, justification, test results |
| Bug fix or clarification | PATCH version proposal in worktracker entry | Defect description, correction, regression verification |

### 3.2 Review Requirements by Criticality

Change review rigor is proportional to the CI's criticality classification, following the criticality levels in quality-enforcement.md:

| CI Criticality | Minimum Review | Quality Gate | Required Strategies | Approval Authority |
|---------------|----------------|-------------|---------------------|-------------------|
| C3 (CI-003, CI-005, CI-006, CI-007) | Creator-critic-revision cycle (H-14, minimum 3 iterations) | >= 0.92 weighted composite (H-13) | S-007 (Constitutional), S-002 (Devil's Advocate), S-014 (LLM-as-Judge) | Framework Maintainer + 1 reviewer |
| C4 (CI-001, CI-002, CI-004, CI-008) | Full tournament mode (all 10 strategies) | >= 0.92 weighted composite (H-13) | All 10 selected strategies (S-001 through S-014 selected set) | Framework Maintainer + human sign-off |

### 3.3 Auto-Escalation Rules for CIs

The following auto-escalation rules from quality-enforcement.md apply to CI changes:

| Rule | Trigger | Escalation | Affected CIs |
|------|---------|------------|-------------|
| AE-002 | Touches `.context/rules/` or `.claude/rules/` | Auto-C3 minimum | CI-006 (trigger map lives in `.context/rules/mandatory-skill-usage.md`) |
| AE-003 | New or modified ADR | Auto-C3 minimum | CI-002 (ADR-001), CI-004 (ADR-002), any new ADR |
| AE-004 | Modifies baselined ADR | Auto-C4 | CI-002 (ADR-001), CI-004 (ADR-002) after baselining |
| AE-001 | Touches `docs/governance/JERRY_CONSTITUTION.md` | Auto-C4 | Any CI change that requires constitutional amendment |

**Escalation precedence:** When multiple AE rules apply, the highest escalation level governs. For example, modifying a baselined ADR (AE-004, C4) that also touches `.context/rules/` (AE-002, C3) is classified as C4.

### 3.4 Approval Workflow

```
PROPOSER submits change proposal
       |
       v
[1. TRIAGE: Determine CI and criticality]
  - Identify affected CI(s)
  - Apply auto-escalation rules (AE-001 through AE-006)
  - Classify change type (MAJOR/MINOR/PATCH)
       |
       v
[2. IMPACT ANALYSIS]
  - List all CIs affected by the change (direct and via dependencies)
  - List all agent definitions affected (via CI-001 schema changes)
  - Estimate migration effort if MAJOR version
  - Document backward compatibility assessment
       |
       v
[3. QUALITY REVIEW per criticality]
  - C3: Creator-critic-revision (3 min iterations), S-014 scoring >= 0.92
  - C4: + Tournament mode (all 10 strategies), human sign-off
       |
       v
[4. ACCEPTANCE]
  - Update CI version number
  - Update baseline ID (APB-MAJOR.MINOR.PATCH)
  - Persist change record in worktracker
  - Update artifact at target path
       |
       v
[5. DEPLOYMENT]
  - For schema changes (CI-001, CI-008): validate all affected agents
  - For rule changes (CI-006): validate trigger map coverage
  - For ADR changes (CI-002, CI-004): update all downstream references
  - Run baseline validation gates (Section 5)
```

### 3.5 Change Record Format

Every approved change to a baselined CI must produce a change record with the following fields:

| Field | Description |
|-------|-------------|
| **Change ID** | `CHG-{CI-NNN}-{YYYYMMDD}-{seq}` (e.g., `CHG-CI-001-20260301-001`) |
| **CI Affected** | CI identifier(s) |
| **Version Transition** | From version -> To version |
| **Change Type** | MAJOR / MINOR / PATCH |
| **Criticality** | C1 / C2 / C3 / C4 (after auto-escalation) |
| **Description** | What changed and why |
| **Impact Assessment** | Affected agents, affected CIs, migration required |
| **Quality Score** | S-014 weighted composite from review |
| **Approver** | Name or role of approving authority |
| **Date** | Acceptance date |

---

## 4. Versioning Strategy

### 4.1 Semantic Versioning for Agent Pattern CIs

All CIs follow Semantic Versioning 2.0.0 (semver.org): **MAJOR.MINOR.PATCH**.

The version components have CI-type-specific increment criteria:

#### 4.1.1 JSON Schema CIs (CI-001, CI-008)

| Component | Increment When | Examples |
|-----------|---------------|----------|
| **MAJOR** | Breaking change: field removed from `required`, enum value removed, constraint tightened (e.g., `maxLength` decreased), `additionalProperties` changed from `true` to `false` | Remove `persona` from schema; remove `forensic` from cognitive_mode enum; decrease description maxLength from 1024 to 512 |
| **MINOR** | Non-breaking addition: new optional field added, new enum value added, new `allowed_tools` entry, constraint relaxed (e.g., `minItems` decreased) | Add `session_context` as optional field; add new cognitive mode; add new MCP tool to `allowed_tools` enum |
| **PATCH** | Clarification: description text updated, example added, documentation improved, no structural change | Improve `description` field's `description` text; add example to `task` field |

**Schema evolution rules** (from ADR-PROJ007-001):
- MINOR version for additions (new enum values, new optional fields)
- MAJOR version for breaking changes (removing fields, tightening constraints)
- Schema `$id` URI includes the major version: `https://jerry-framework.dev/schemas/agent-definition/v{MAJOR}.0.0`
- Schema `$id` URI updates only on MAJOR version increments
- All agent definitions must specify which schema major version they target

#### 4.1.2 ADR CIs (CI-002, CI-004)

| Component | Increment When | Examples |
|-----------|---------------|----------|
| **MAJOR** | Decision reversed or fundamentally altered; affects all downstream CIs | Switch from YAML+MD to pure YAML format; replace keyword routing with LLM-only routing |
| **MINOR** | Decision extended with new component or significant elaboration that does not contradict the original decision | Add new tool security tier T6; add Layer 4 to routing architecture; add new anti-pattern to catalog |
| **PATCH** | Clarification, correction of errors, updated references, improved examples | Fix typo in routing algorithm pseudocode; update evidence source with newer publication |

**ADR lifecycle interaction:** When an ADR is modified:
- PATCH changes do not require re-acceptance.
- MINOR changes require AE-003 review (auto-C3 minimum) since they represent substantive ADR modification.
- MAJOR changes require AE-004 review (auto-C4) and effectively produce a superseding ADR.

#### 4.1.3 Template and Specification CIs (CI-003, CI-005, CI-006, CI-007)

| Component | Increment When | Examples |
|-----------|---------------|----------|
| **MAJOR** | Structural change that invalidates existing usage; new REQUIRED fields; removed sections | Add a new REQUIRED field to agent template; remove a cognitive mode from the enum |
| **MINOR** | New RECOMMENDED field; new optional section; parameter range expansion | Add `session_context` as RECOMMENDED; add new compound trigger syntax to trigger map |
| **PATCH** | Documentation improvement; example update; parameter value tuning within existing ranges | Update iteration ceiling from 7 to 8 for C3; improve trigger map keyword examples |

### 4.2 Baseline Versioning

The overall baseline version (APB-X.Y.Z) reflects the aggregate state of all CIs:

| Component | Increment When |
|-----------|---------------|
| **MAJOR** | Any CI has a MAJOR version increment, OR a new CI is added, OR a CI is removed |
| **MINOR** | Any CI has a MINOR version increment (and no CI has a MAJOR increment) |
| **PATCH** | Only PATCH-level changes across all CIs |

**Version synchronization:** Individual CIs version independently. The baseline version is the aggregate indicator. A single CI MAJOR bump causes a baseline MAJOR bump regardless of other CIs' states.

### 4.3 MCP Tool Enum Maintenance

The `allowed_tools` enum in CI-001 (JSON Schema) includes current MCP tools. Per the PS-to-NSE handoff open question #6, MCP tool enum changes are coupled with TOOL_REGISTRY.yaml updates:

| Event | Schema Action | Version Impact |
|-------|--------------|---------------|
| New MCP tool added to TOOL_REGISTRY.yaml | Add tool to `allowed_tools` enum in CI-001 | CI-001 MINOR version increment |
| MCP tool removed from TOOL_REGISTRY.yaml | Remove tool from `allowed_tools` enum in CI-001 | CI-001 MAJOR version increment (breaking) |
| MCP tool renamed | Remove old name, add new name | CI-001 MAJOR version increment (breaking) |
| New non-MCP tool added to Claude Code | Add tool to `allowed_tools` enum in CI-001 | CI-001 MINOR version increment |

**Coupling rule:** TOOL_REGISTRY.yaml updates and CI-001 schema enum updates MUST be performed in the same change proposal. Independent updates create drift between the registry and the schema.

### 4.4 Cognitive Mode Enum Evolution

The cognitive mode enum (CI-005) is embedded in CI-001 (JSON Schema) and referenced by CI-003 (template). Changes require coordinated updates:

| Event | Action | Version Impact |
|-------|--------|---------------|
| Add new cognitive mode | Add to CI-001 enum; update CI-005 documentation; update CI-003 selection criteria | CI-001 MINOR, CI-005 MINOR, CI-003 MINOR |
| Remove a cognitive mode | Remove from CI-001 enum; document subsumption; migrate affected agents | CI-001 MAJOR, CI-005 MAJOR, CI-003 MAJOR |
| Rename a cognitive mode | Remove old, add new in CI-001; update CI-005 subsumption mapping | CI-001 MAJOR, CI-005 MAJOR, CI-003 MAJOR |

### 4.5 Discrepancy Resolution: Rule Consolidation

The PS-to-NSE barrier-3 handoff identifies a discrepancy in rule consolidation proposals:

| Source | Proposal | Result |
|--------|----------|--------|
| ps-synthesizer-001 | Consolidate H-25 through H-30 into 2 compound rules | 27/35 HARD rule slots (77%) |
| ps-architect-001 | Consolidate into 3 rules (H-25c, H-28, H-29c) | 28/35 HARD rule slots (80%) |

**Configuration decision:** This discrepancy is **deferred to a separate AE-002-triggered change proposal** per barrier-3 handoff recommendation #2. The v1.0.0 baseline records the current state (31/35 slots, 89%) and both proposed consolidation options. The consolidation itself is out of scope for APB-1.0.0 because it modifies `.context/rules/quality-enforcement.md` (AE-002 auto-C3) and is a distinct governance action from the agent patterns baseline.

---

## 5. Baseline Validation Criteria

### 5.1 Validation Gates

A baseline release (new or updated) must pass all 7 validation gates before acceptance. Gates are ordered by execution priority (deterministic checks first, LLM-based checks last).

| Gate | Name | Type | Criteria | Failure Action |
|------|------|------|----------|---------------|
| BV-01 | Schema Self-Consistency | Deterministic | CI-001 JSON Schema is valid per JSON Schema Draft 2020-12 specification. CI-008 JSON Schema is valid. No circular `$ref` dependencies. All `$id` URIs are unique. | BLOCK: Fix schema errors before proceeding. |
| BV-02 | Agent Definition Compliance | Deterministic | All 37+ existing agent definitions validate against CI-001 JSON Schema with zero errors. Known deviations are documented with remediation timeline. | BLOCK: Either fix schema to accommodate existing agents (if schema is too strict) or document agent remediation plan (if agents are non-compliant). |
| BV-03 | Cross-CI Consistency | Analysis | CI-001 schema enums match CI-005 documented enums. CI-003 template fields match CI-001 schema required fields. CI-006 trigger map skills match CLAUDE.md registered skills. CI-007 iteration parameters are consistent with quality-enforcement.md H-14 minimums. CI-008 handoff fields are consistent with CI-004 routing metadata definitions. | BLOCK: Resolve inconsistencies between CIs. |
| BV-04 | V&V Plan Coverage | Analysis | Every CI maps to at least one V&V test procedure in the nse-verification-001 V&V plan. Every requirement satisfied by a CI has a corresponding verification method. | BLOCK: Add missing V&V coverage. |
| BV-05 | Quality Gate Threshold | LLM-based | Each C4 CI artifact (CI-001, CI-002, CI-004, CI-008) achieves >= 0.92 weighted composite score via S-014 LLM-as-Judge scoring across 6 dimensions. C3 CI artifacts (CI-003, CI-005, CI-006, CI-007) achieve >= 0.92 via creator-critic cycle. | REJECT: Enter revision cycle per H-13 until threshold is met. |
| BV-06 | Constitutional Compliance | Analysis | S-007 Constitutional AI Critique applied. No CI introduces rules or patterns that violate P-003, P-020, or P-022. No CI overrides or weakens existing HARD rules without explicit governance approval. | BLOCK: Remove non-compliant content. |
| BV-07 | Regression Non-Degradation | Test | Applying the new baseline does not cause any previously-passing V&V test to fail. Existing agent definitions that were compliant remain compliant. Routing decisions that were correct remain correct. | BLOCK: Identify regression cause. Fix baseline or adjust test expectations with documented rationale. |

### 5.2 Validation Gate Execution Order

```
[BV-01: Schema Self-Consistency]     (0 tokens, deterministic)
       |
       v  (schemas are valid)
[BV-02: Agent Compliance]            (0 tokens, deterministic)
       |
       v  (agents validate against schema)
[BV-03: Cross-CI Consistency]        (~500 tokens, analysis)
       |
       v  (CIs are internally consistent)
[BV-04: V&V Coverage]                (~300 tokens, analysis)
       |
       v  (all CIs have V&V coverage)
[BV-06: Constitutional Compliance]   (~1,000-2,000 tokens, S-007)
       |
       v  (no constitutional violations)
[BV-07: Regression Non-Degradation]  (variable, test execution)
       |
       v  (no regressions)
[BV-05: Quality Gate Threshold]      (~5,000-30,000 tokens, S-014)
       |
       v  (>= 0.92 scored)
BASELINE ACCEPTED
```

**Rationale for ordering:** Deterministic checks (BV-01, BV-02) run first because they are zero-cost and catch structural defects that would invalidate LLM-based scoring. Analysis checks (BV-03, BV-04, BV-06) run next to ensure consistency and compliance before investing tokens in quality scoring. Quality gate scoring (BV-05) runs last because it is the most expensive and should only evaluate structurally sound, consistent, compliant artifacts.

### 5.3 Quality Dimensions for Baseline CIs

Each CI is scored against the standard S-014 6-dimension rubric from quality-enforcement.md, with baseline-specific interpretation:

| Dimension | Weight | Baseline-Specific Interpretation |
|-----------|--------|----------------------------------|
| Completeness | 0.20 | CI covers all aspects identified in its source artifacts. No gaps in field definitions, enum values, or validation rules. |
| Internal Consistency | 0.20 | CI does not contradict itself. Schema constraints match template documentation. ADR decisions align with evidence cited. |
| Methodological Rigor | 0.20 | CI decisions trace to evidence (trade studies, requirements, risk analysis). Versioning rules follow established standards (semver). Change control follows quality-enforcement.md escalation model. |
| Evidence Quality | 0.15 | Citations reference accessible source documents. Authority tiers are appropriate. No unsupported claims. |
| Actionability | 0.15 | A developer can use the CI to create a compliant agent, validate an existing agent, propose a change, or understand versioning impact without additional guidance. |
| Traceability | 0.10 | CI traces to source requirements (Section 6). Requirements trace to CI. Bidirectional traceability is complete. |

---

## 6. Traceability Matrix

### 6.1 CIs to Requirements

This matrix maps each CI to the formal requirements it satisfies from nse-requirements-001.

| CI | Requirements Satisfied | Coverage Notes |
|----|----------------------|----------------|
| CI-001 (JSON Schema) | AR-001, AR-002, AR-003, AR-007, AR-008, AR-009, AR-012, PR-002, PR-003, PR-007, SR-002, SR-003, SR-009 | Primary validation mechanism for structural requirements. AR-003 is the driving requirement for this CI. |
| CI-002 (ADR-001) | AR-001 through AR-012, PR-001 through PR-008, SR-001, SR-002, SR-003, SR-009 | Comprehensive ADR covering all agent structure and prompt design requirements. Authoritative rationale for each decision. |
| CI-003 (Template) | AR-001, AR-002, AR-009, AR-012, PR-001, PR-002, PR-003, PR-004, PR-005, PR-007, PR-008, SR-001, SR-002, SR-003 | Operational implementation of the template that developers use to create new agents. |
| CI-004 (ADR-002) | RR-001 through RR-008, HR-001 (partially, via routing metadata in handoffs) | Comprehensive ADR covering all routing requirements and circuit breaker specification. |
| CI-005 (Enums/Tiers) | PR-002 (cognitive mode), AR-006 (tool restriction via tiers), PR-007 (model selection criteria) | Cross-cutting parameters that are embedded in CI-001 and CI-003. |
| CI-006 (Trigger Map) | RR-001, RR-002, RR-004, RR-005, RR-007 | Operational configuration of keyword routing. Directly implements the routing decision from CI-004. |
| CI-007 (Circuit Breaker) | RR-006, QR-001, QR-004 (iteration constraints) | Operational parameters for loop prevention and iteration limits. Complements H-14 minimum with maximum bounds. |
| CI-008 (Handoff Schema) | HR-001, HR-002, HR-003, HR-005, HR-006, HR-004 (via Memory-Keeper integration) | Complete handoff protocol. Directly addresses the #1 identified failure source (free-text handoffs). |

### 6.2 CIs to ADR Decisions

| CI | Source ADR Decision(s) | ADR Section |
|----|----------------------|-------------|
| CI-001 | JSON Schema for YAML frontmatter validation (B5 approach) | ADR-PROJ007-001 Section 2 |
| CI-002 | Seven-component agent definition standard | ADR-PROJ007-001 (entire Decision section) |
| CI-003 | Canonical template consolidating AR/PR requirements | ADR-PROJ007-001 Section 1 |
| CI-004 | Layered routing with L1 immediate implementation | ADR-PROJ007-002 (entire Decision section) |
| CI-005 | 5-mode cognitive taxonomy; T1-T5 tool security tiers | ADR-PROJ007-001 Sections 4, 5 |
| CI-006 | Enhanced trigger map (5-column format) | ADR-PROJ007-002 Section 2 |
| CI-007 | Circuit breaker (max 3 hops); iteration ceilings | ADR-PROJ007-002 Section 3 |
| CI-008 | Structured handoff as API contract | nse-integration-001 Section 1 (synthesizing ADR-001 session_context and ADR-002 routing_metadata) |

### 6.3 CIs to Risk Mitigations

| CI | Risk(s) Mitigated | RPN | Mitigation Mechanism |
|----|-------------------|-----|---------------------|
| CI-001 (JSON Schema) | R-T02 Error Amplification (336), R-Q01 Quality Gate Bypass | 336 | Deterministic pre-check catches structural defects at zero LLM cost |
| CI-003 (Template) | R-P02 Rule Proliferation | -- | Single authoritative template prevents inconsistent agent definitions |
| CI-004 (ADR-002) | RF-04 Routing Loops (252), RF-01 Misrouting (150) | 252, 150 | Circuit breaker and negative keywords prevent routing failures |
| CI-006 (Trigger Map) | RF-01 Misrouting (150), RF-02 No-Route (120) | 150, 120 | Enhanced keywords with negative keywords reduce false positives and false negatives |
| CI-007 (Circuit Breaker) | RF-04 Routing Loops (252), CF-01 Context Rot (392) | 252, 392 | Iteration ceilings and routing depth prevent unbounded resource consumption |
| CI-008 (Handoff Schema) | HF-01 Free-Text Info Loss (336), HF-04 Telephone Game (245) | 336, 245 | Structured schema with validation prevents information degradation at handoff boundaries |

### 6.4 CIs to Gap Closure

| CI | Gap(s) Addressed | Priority |
|----|-----------------|----------|
| CI-001 | GAP-01 (Schema Validation for Agent Definitions) | P1 (Critical) |
| CI-001, CI-008 | GAP-02 (Schema Validation as QA Pre-Check Layer) | P1 (Critical) |
| CI-008 | GAP-03 (Structured Handoff Protocol) | P1 (Critical) |
| CI-007 | GAP-07 (Iteration Ceiling Enforcement) | P2 (Strategic) |
| CI-006 | GAP-05 (Routing Interface Abstraction, partially) | P2 (Strategic) |

### 6.5 Requirements Coverage Summary

| Requirement Domain | Total Reqs | CIs Providing Coverage | Coverage Rate |
|--------------------|-----------|----------------------|---------------|
| AR (Agent Structure) | 12 | CI-001, CI-002, CI-003 | 12/12 (100%) |
| PR (Prompt Design) | 8 | CI-002, CI-003, CI-005 | 8/8 (100%) |
| RR (Routing) | 8 | CI-004, CI-006, CI-007 | 8/8 (100%) |
| HR (Handoff) | 6 | CI-008 | 6/6 (100%) |
| QR (Quality) | 9 | CI-001, CI-007, CI-008 (via quality gates) | 7/9 (78%) |
| SR (Safety/Governance) | 9 | CI-001, CI-002, CI-003 | 7/9 (78%) |
| **Total** | **52** | | **48/52 (92%)** |

**Coverage gaps (4 requirements not directly addressed by CIs):**

| Requirement | Gap Reason | Resolution |
|-------------|-----------|------------|
| QR-007 (Citation Requirements) | Citation enforcement is an agent behavioral property, not a configuration item. | Governed by CI-003 template (guardrails.output_filtering includes `all_claims_must_have_citations`) but enforcement is behavioral, not schema-validatable. |
| QR-009 (Leniency Bias Counteraction) | Scoring calibration is a runtime quality concern, not a static configuration. | Addressed by quality-enforcement.md S-014 anti-leniency guidance. Calibration procedures defined in nse-verification-001 Section 5.2. |
| SR-005 (Deception Prevention) | Deception prevention is constitutional (P-022), enforced by L1/L2 layers. | CI-003 template includes P-022 in `constitution.principles_applied`. Enforcement is behavioral, not schema-validatable. |
| SR-006 (Audit Trail Requirements) | Audit infrastructure is an operational concern, not a baseline CI. | Deferred to implementation. CI-004 routing observability format provides the design specification. |

---

## Self-Review (S-010)

### Completeness Check

| Required Section | Status | Coverage |
|-----------------|--------|----------|
| Navigation table (H-23, H-24) | COMPLETE | 9 sections with anchor links |
| NASA SE disclaimer | COMPLETE | Standard disclaimer at document top |
| Baseline Definition | COMPLETE | Scope, contents inventory, artifact paths, baseline identification |
| Configuration Items | COMPLETE | 8 CIs with naming, versioning, status, dependencies |
| Change Control Process | COMPLETE | Proposal types, criticality-based review, auto-escalation, approval workflow, change record format |
| Versioning Strategy | COMPLETE | Semver for 3 CI types (schemas, ADRs, specs), baseline versioning, MCP tool coupling, cognitive mode evolution |
| Baseline Validation Criteria | COMPLETE | 7 validation gates with execution order, quality dimensions, failure actions |
| Traceability Matrix | COMPLETE | CIs to requirements (52), CIs to ADR decisions, CIs to risks, CIs to gaps, coverage summary |

### Quality Verification

| Criterion | Assessment |
|-----------|------------|
| **Source Traceability** | All 8 CIs trace to PS Phase 3 synthesis artifacts (ADR-001, ADR-002, ps-synthesizer-001) and NSE Phase 3 synthesis (nse-integration-001, nse-verification-001). Barrier-3 handoff's per-agent guidance for nse-configuration-001 is fully addressed (all 8 identified artifacts mapped to CIs). |
| **Consistency with Existing Governance** | Change control aligns with quality-enforcement.md criticality levels (C1-C4), auto-escalation rules (AE-001 through AE-006), quality gate threshold (0.92), and tier vocabulary (HARD/MEDIUM/SOFT). No new governance mechanisms invented. |
| **Discrepancy Resolution** | Rule consolidation discrepancy (2 vs. 3 compound rules) explicitly deferred with rationale (separate AE-002 change, out of scope for APB-1.0.0). Cognitive mode consolidation (8 to 5) documented with subsumption mapping. |
| **Actionability** | A developer can use this document to: identify which CI governs a given concern, determine the review requirements for a proposed change, understand version increment criteria, and verify a baseline release against the 7 validation gates. |
| **Barrier-3 Open Questions** | OQ-5 (ADR acceptance workflow) addressed in Section 3.4. OQ-6 (MCP tool enum maintenance) addressed in Section 4.3. OQ-7 (iteration ceiling as HARD rule) deferred per Section 4.5 rationale. |

### Identified Limitations

1. **CI-005 and CI-007 are parameter collections, not standalone artifacts.** Their values are embedded in CI-001 (schema) and CI-004 (ADR). They are tracked as separate CIs for independent versioning and change control, but they do not have dedicated files -- changes are applied to the host artifacts. This is a pragmatic trade-off between configuration granularity and artifact proliferation.

2. **Validation gate BV-02 requires the JSON Schema to exist as a deployable file.** Currently, the schema is inline in ADR-PROJ007-001. Baseline acceptance requires extracting the schema to `docs/schemas/agent-definition-v1.0.0.json`. This extraction is a prerequisite, not a validation gate outcome.

3. **Quality gate scoring (BV-05) is inherently stochastic.** The 0.92 threshold applies to LLM-based scoring, which has known variance (per nse-verification-001 Section 5). Score variance of up to 0.05 means a CI scoring 0.90 in one run might score 0.95 in another. The mitigation is to require 3 scoring runs with all scores >= 0.92, per the score stability protocol.

4. **Coverage gap of 8% (4/52 requirements).** Four requirements are not directly addressed by configuration items because they concern behavioral enforcement (citation, leniency, deception) or operational infrastructure (audit trails) rather than static configuration. These are documented in Section 6.5 with resolution paths.

5. **Baseline versioning granularity.** The current scheme uses a single APB version for all 8 CIs. An alternative would be per-CI baselining with independent release cycles. The single-version approach is chosen for simplicity at the current scale (8 CIs). If CI count exceeds 15, per-CI baselining should be reconsidered.

---

## References

### Phase 3-4 Artifacts

| ID | Document | Location |
|----|----------|----------|
| ADR-001 | ADR-PROJ007-001: Agent Definition Format | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-3-synthesis/ps-architect-001/ps-architect-001-adr-agent-design.md` |
| ADR-002 | ADR-PROJ007-002: Routing and Trigger Framework | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-3-synthesis/ps-architect-002/ps-architect-002-adr-routing-triggers.md` |
| SYNTH-001 | Unified Pattern Taxonomy | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-3-synthesis/ps-synthesizer-001/ps-synthesizer-001-synthesis.md` |
| INT-001 | Integration Patterns | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-3-synthesis/nse-integration-001/nse-integration-001-integration-patterns.md` |
| VV-001 | V&V Plan | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-3-synthesis/nse-verification-001/nse-verification-001-vv-plan.md` |
| REQ-001 | Requirements Specification | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-2-analysis/nse-requirements-001/nse-requirements-001-requirements.md` |
| B3-HANDOFF | PS-to-NSE Barrier 3 Handoff | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/cross-pollination/barrier-3/ps-to-nse/handoff.md` |

### Jerry Framework Rules

| ID | Document | Location |
|----|----------|----------|
| QE | Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` |
| MSU | Mandatory Skill Usage | `.context/rules/mandatory-skill-usage.md` |
| MCP | MCP Tool Standards | `.context/rules/mcp-tool-standards.md` |
| AGENTS | Agent Registry | `AGENTS.md` |

### External Standards

| Standard | Relevance |
|----------|-----------|
| NPR 7123.1D Process 9 | Configuration Management |
| Semantic Versioning 2.0.0 (semver.org) | Versioning standard for all CIs |
| JSON Schema Draft 2020-12 | Schema format for CI-001 and CI-008 |
| IEEE 828-2012 | Configuration Management in Systems and Software Engineering (reference for CM process design) |

---

*Generated by nse-configuration-001 agent v1.0.0*
*NASA Process: NPR 7123.1D Process 9 (Configuration Management)*
*Criticality: C4 (configuration baseline for architecture/governance patterns)*
*Self-Review (S-010) Applied: 5 limitations identified and documented*
*Coverage: 8 CIs, 52 requirements (92% direct coverage), 7 validation gates, 6 auto-escalation rules integrated*
*Traceability: Bidirectional to requirements (nse-requirements-001), ADR decisions (ADR-PROJ007-001, ADR-PROJ007-002), risk mitigations (top 5 FMEA modes), and gap closures (5 of 12 gaps)*
