# ST-068: Work Item Decomposition -- Competitive Feature Roadmap

> **Agent:** nse-requirements-004
> **Pipeline:** NSE (NASA-SE)
> **Phase:** 3 (Work Item Decomposition)
> **Story:** ST-068
> **Feature:** FEAT-003 (Feature Architecture)
> **Orchestration:** comp-feat-20260222-001
> **Project:** PROJ-008 (Agentic Security)
> **Status:** complete
> **Criticality:** C4
> **Quality Score:** 0.953 (self-assessed, S-014)
> **Created:** 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [Decomposition Methodology](#decomposition-methodology) | How work items are derived from source artifacts |
| [Entity Summary](#entity-summary) | Counts and ID ranges for all new entities |
| [Epics](#epics) | 7 new Epics (EPIC-006 through EPIC-012) aligned to P1-P7 and shared infra |
| [Features](#features) | 14 new Features (FEAT-017 through FEAT-030) |
| [Enablers](#enablers) | 6 new Enablers (EN-004 through EN-009) for shared infrastructure |
| [Stories by Epic](#stories-by-epic) | Full story specifications with acceptance criteria, dependencies, FR-FEAT coverage |
| [Dependency Map](#dependency-map) | Implementation ordering reflecting Impl-1 through Impl-6 |
| [B-004 Impact Classification](#b-004-impact-classification) | Per-story B-004 dependency assessment |
| [Self-Scoring (S-014)](#self-scoring-s-014) | Quality gate assessment against six dimensions |
| [Citations](#citations) | Source artifact traceability |

---

## Decomposition Methodology

Work items are decomposed from the following inputs:

1. **Feature requirements** (nse-requirements-003): 33 FR-FEAT requirements (FR-FEAT-001 through FR-FEAT-033) organized by P1-P7 feature priority.
2. **Feature architecture** (ps-architect-002): Component designs, shared infrastructure identification, 4-phase implementation ordering, critical path analysis.
3. **PS-to-NSE handoff** (barrier-2): Implementation ordering (Impl-1 through Impl-6), work item decomposition inputs, B-004 fallback paths.
4. **NSE-to-PS handoff** (barrier-2): Trade study recommendations (TS-1 through TS-4), cross-study dependencies.

### Decomposition Rules

| Rule | Description |
|------|-------------|
| **Epic-to-Priority** | Each P1-P7 priority maps to one Epic; shared infrastructure gets a dedicated Epic |
| **Feature-to-Component** | Each architectural component or logical grouping within an Epic maps to one Feature |
| **Story-to-Requirement** | Each FR-FEAT requirement maps to at least one Story; complex requirements split into multiple Stories |
| **Enabler-to-Shared** | Cross-cutting infrastructure components (Section 8.1 shared components) map to Enablers |
| **Size estimation** | S = 1-2 files, 1-3 days; M = 3-5 files, 3-7 days; L = 6+ files, 1-2 weeks |
| **ID continuity** | New IDs continue from existing WORKTRACKER.md: EPIC-006+, FEAT-017+, EN-004+, ST-069+ |

---

## Entity Summary

| Entity Type | Count | ID Range | Status |
|-------------|-------|----------|--------|
| Epics | 7 | EPIC-006 -- EPIC-012 | pending |
| Features | 14 | FEAT-017 -- FEAT-030 | pending |
| Enablers | 6 | EN-004 -- EN-009 | pending |
| Stories | 55 | ST-069 -- ST-123 (incl. ST-074a, ST-077a, ST-088a, ST-107a) | pending |
| **Total** | **82** | | |

---

## Epics

| ID | Name | Impl Phase | Status | Features | Enablers | Priority |
|----|------|-----------|--------|----------|----------|----------|
| EPIC-006 | Shared Security Infrastructure | Impl-0 (foundation) | pending | -- | EN-004, EN-005, EN-006, EN-007 | Foundation |
| EPIC-007 | Progressive Governance | Impl-1 | pending | FEAT-017, FEAT-018 | EN-008 | P2 |
| EPIC-008 | Supply Chain Verification | Impl-2 | pending | FEAT-019, FEAT-020, FEAT-021 | -- | P1 |
| EPIC-009 | Multi-Model LLM Support | Impl-3 | pending | FEAT-022, FEAT-023 | -- | P3 |
| EPIC-010 | Secure Skill Marketplace | Impl-4 | pending | FEAT-024, FEAT-025, FEAT-026 | -- | P4 |
| EPIC-011 | Compliance-as-Code Publishing | Impl-6 | pending | FEAT-027, FEAT-028 | -- | P5 |
| EPIC-012 | Advanced Security Capabilities | Impl-5 | pending | FEAT-029, FEAT-030 | EN-009 | P6-P7 |

---

## Features

| ID | Name | Epic | Status | Stories | Pipeline |
|----|------|------|--------|---------|----------|
| FEAT-017 | Governance Profile Engine | EPIC-007 | pending | ST-075, ST-076, ST-077a, ST-078, ST-079 | PS + NSE |
| FEAT-018 | Onboarding and DX | EPIC-007 | pending | ST-080 | PS |
| FEAT-019 | Code Signing and Provenance | EPIC-008 | pending | ST-081, ST-082, ST-083, ST-084 | PS |
| FEAT-020 | MCP Supply Chain | EPIC-008 | pending | ST-085, ST-086, ST-087, ST-088a | PS + NSE |
| FEAT-021 | Runtime Integrity | EPIC-008 | pending | ST-089, ST-090, ST-091 | PS |
| FEAT-022 | Provider Abstraction | EPIC-009 | pending | ST-092, ST-093, ST-094, ST-095 | PS |
| FEAT-023 | Cross-Provider Security | EPIC-009 | pending | ST-096, ST-097, ST-098 | PS + NSE |
| FEAT-024 | Skill Registry and Distribution | EPIC-010 | pending | ST-099, ST-100, ST-101, ST-102, ST-103 | PS |
| FEAT-025 | Marketplace Security | EPIC-010 | pending | ST-104, ST-105, ST-106 | PS + NSE |
| FEAT-026 | Marketplace Operations | EPIC-010 | pending | ST-107a, ST-108, ST-109 | PS |
| FEAT-027 | Compliance Evidence Pipeline | EPIC-011 | pending | ST-110, ST-111, ST-112, ST-113 | NSE |
| FEAT-028 | Regulatory Framework Mappings | EPIC-011 | pending | ST-114, ST-115, ST-116 | NSE |
| FEAT-029 | Semantic Context Retrieval | EPIC-012 | pending | ST-117, ST-118, ST-119, ST-120 | PS |
| FEAT-030 | Aggregate Intent Monitoring | EPIC-012 | pending | ST-121, ST-122, ST-123 | PS + NSE |

---

## Enablers

| ID | Name | Epic | Status | Purpose |
|----|------|------|--------|---------|
| EN-004 | Code Signing Engine | EPIC-006 | pending | Ed25519 key management, signature generation/verification. Shared by P1 (FR-FEAT-001), P4 (FR-FEAT-019, FR-FEAT-021). Foundation for all supply chain and marketplace features. |
| EN-005 | Audit Trail and Action Accumulator | EPIC-006 | pending | Structured JSON-lines logging with session-level action accumulation. Shared by P1 (FR-FEAT-005 provenance), P7 (FR-FEAT-030), and all features for security event logging. |
| EN-006 | Provider Abstraction Layer | EPIC-006 | pending | Model-agnostic LLM invocation interface with pluggable adapters. Shared by P3 (FR-FEAT-011) and P4 (marketplace skills across models). Foundation for multi-model support. |
| EN-007 | Security Event Infrastructure | EPIC-006 | pending | Structured security event emission, collection, and alerting pipeline. Used by all features for security event logging, B-004 fallback notifications, and compliance evidence generation. |
| EN-008 | Governance Profile Engine | EPIC-007 | pending | Tier configuration loading, gate-strictness application, profile validation. Shared by P2 (FR-FEAT-006/007), P4 (FR-FEAT-018), P5 (FR-FEAT-022). Configuration-driven governance profiles for Lite/Team/Enterprise tiers. |
| EN-009 | Threat Pattern Library | EPIC-012 | pending | MITRE ATT&CK/ATLAS mapped threat patterns for aggregate intent analysis. Shared by P7 (FR-FEAT-031, FR-FEAT-032). Seed library of 10+ aggregate attack patterns with MITRE technique IDs. |

---

## Stories by Epic

### EPIC-006: Shared Security Infrastructure

> Foundation components shared across multiple feature Epics. Must be implemented first (Impl-0) before any feature work begins.

#### EN-004: Code Signing Engine

##### ST-069: Ed25519 Key Pair Generation and Management

| Field | Value |
|-------|-------|
| **ID** | ST-069 |
| **Title** | Ed25519 Key Pair Generation and Management |
| **Epic** | EPIC-006 |
| **Enabler** | EN-004 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-001 (partial: key generation component) |
| **Security Controls** | FR-SEC-027 (Skill Integrity), FR-SEC-004 (Provenance Tracking) |
| **Dependencies** | None (foundational) |
| **Description** | Implement Ed25519 key pair generation for skill/plugin authors via `jerry skill keygen`. Key storage in age-encrypted local keyring. Public key export for registry submission. Key rotation support with revocation of old keys. |
| **Acceptance Criteria** | (1) `jerry skill keygen` generates Ed25519 key pair and stores securely. (2) Private key encrypted at rest using age encryption. (3) Public key exportable in standard format for registry submission. (4) Key listing via `jerry skill keys list`. (5) Key revocation marks key as revoked with timestamp. (6) Unit tests cover key generation, storage, retrieval, and revocation. |

##### ST-070: Signature Generation and Verification

| Field | Value |
|-------|-------|
| **ID** | ST-070 |
| **Title** | Signature Generation and Verification |
| **Epic** | EPIC-006 |
| **Enabler** | EN-004 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-001 (partial: signing and verification component) |
| **Security Controls** | FR-SEC-027 (Skill Integrity), FR-SEC-025 (MCP Integrity) |
| **Dependencies** | ST-069 (key pairs must exist) |
| **Description** | Implement detached signature generation via `jerry skill sign <skill-path>` producing `.sig` files. Verification of signatures against public key registry. Deterministic signature verification suitable for L3/L5 enforcement (context-rot immune). |
| **Acceptance Criteria** | (1) `jerry skill sign <skill-path>` produces detached `.sig` file. (2) Signature covers all skill files (SKILL.md, agents/*.md, rules/*.md). (3) `jerry skill verify <skill-path>` validates signature against registered public key. (4) Invalid/missing signatures rejected with clear error message. (5) Verification is deterministic (same input always produces same result). (6) Integration tests cover sign-verify round trip. |

##### ST-071: Public Key Registry

| Field | Value |
|-------|-------|
| **ID** | ST-071 |
| **Title** | Public Key Registry |
| **Epic** | EPIC-006 |
| **Enabler** | EN-004 |
| **Status** | pending |
| **Size** | S |
| **FR-FEAT Coverage** | FR-FEAT-001 (partial: registry component), FR-FEAT-021 (partial: author identity) |
| **Security Controls** | FR-SEC-004 (Provenance Tracking), FR-SEC-001 (Unique Agent Identity) |
| **Dependencies** | ST-069 (key generation provides keys to register) |
| **Description** | Implement version-controlled public key registry (YAML/JSON) for author verification. Registry stores: author name, public key, GitHub identity link (optional), registration date, revocation status. Registry changes trigger AE-002 (auto-C3). |
| **Acceptance Criteria** | (1) Public key registry maintained as version-controlled YAML file. (2) `jerry author register <public-key>` adds key to registry. (3) Registry entries include author name, key, registration date, status. (4) Registry modifications tracked in git history. (5) Registry schema validated at L5 CI. |

#### EN-005: Audit Trail and Action Accumulator

##### ST-072: Structured Audit Event Logger

| Field | Value |
|-------|-------|
| **ID** | ST-072 |
| **Title** | Structured Audit Event Logger |
| **Epic** | EPIC-006 |
| **Enabler** | EN-005 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-030 (partial: accumulation infrastructure), FR-FEAT-005 (partial: provenance logging) |
| **Security Controls** | FR-SEC-029 (Audit Trail), FR-SEC-032 (Audit Log Integrity) |
| **Dependencies** | None (foundational) |
| **Description** | Implement structured JSON-lines audit event logger. Each event: timestamp, agent ID, tool name, sanitized arguments, result status, session ID. Append-only log with integrity hashing. Log queryable by L4 inspection hooks. Size bounded to 5% of context window per CB-01. |
| **Acceptance Criteria** | (1) Every tool invocation produces a structured audit event. (2) Events stored in JSON-lines format, one event per line. (3) Log is append-only with per-entry SHA-256 hash chain. (4) Log queryable by agent ID, tool name, time range. (5) Log rotation when size exceeds configurable threshold. (6) Unit tests verify event structure and integrity chain. |

##### ST-073: Session Action Accumulator

| Field | Value |
|-------|-------|
| **ID** | ST-073 |
| **Title** | Session Action Accumulator |
| **Epic** | EPIC-006 |
| **Enabler** | EN-005 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-030 (primary: session-level accumulation) |
| **Security Controls** | FR-SEC-029 (Audit Trail), FR-SEC-015 (Goal Integrity), FR-SEC-037 (Rogue Agent Detection) |
| **Dependencies** | ST-072 (audit logger provides event stream) |
| **Description** | Implement session-level action accumulator that maintains a running summary of all agent actions. Tracks: tools invoked, files accessed (read/written), external resources contacted, delegation events, security events. Accumulator queryable by any L4 inspection mechanism. Size managed to stay within CB-01 budget (5% context window). |
| **Acceptance Criteria** | (1) Accumulator tracks all tool invocations with sanitized arguments. (2) File access patterns (read/write) are tracked per agent. (3) External resource contacts logged with destination. (4) Delegation events (Task invocations) tracked. (5) Accumulator size does not exceed 5% of context window. (6) L4 hooks can query accumulator state. |

#### EN-006: Provider Abstraction Layer (Infrastructure)

See FEAT-022 (ST-088, ST-089) for implementation stories. EN-006 represents the shared infrastructure aspect; FEAT-022 contains the detailed implementation stories.

#### EN-007: Security Event Infrastructure

##### ST-074a: Security Event Emission Framework

| Field | Value |
|-------|-------|
| **ID** | ST-074a |
| **Title** | Security Event Emission Framework |
| **Epic** | EPIC-006 |
| **Enabler** | EN-007 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | Cross-cutting (supports all features) |
| **Security Controls** | FR-SEC-030 (Security Event Logging), FR-SEC-035 (Graceful Degradation) |
| **Dependencies** | ST-072 (audit logger for event persistence) |
| **Description** | Implement a structured security event emission framework. Event types: BLOCKED (L3 gate denial), WARNING (suspicious pattern), ALERT (aggregate intent), REVOKED (skill revocation). Each event includes: severity, source gate/inspector, affected entity, timestamp, remediation suggestion. Events feed into audit trail (EN-005) and governance dashboard (FR-FEAT-010). |
| **Acceptance Criteria** | (1) Security events emittable from any L3 gate or L4 inspector. (2) Event schema defines severity levels (INFO, WARNING, ERROR, CRITICAL). (3) Events include source, affected entity, timestamp, and remediation. (4) Events persisted via audit trail (ST-072). (5) Event emission does not block tool execution (async where possible). (6) Unit tests verify event emission and schema compliance. |

---

### EPIC-007: Progressive Governance (Impl-1)

> P2 features. No dependencies on other feature Epics or B-004. Lowest implementation risk, highest quick-win value. Duration: 2-3 weeks.

#### FEAT-017: Governance Profile Engine

##### ST-075: Governance Profile YAML Schema and Validation

| Field | Value |
|-------|-------|
| **ID** | ST-075 |
| **Title** | Governance Profile YAML Schema and Validation |
| **Epic** | EPIC-007 |
| **Feature** | FEAT-017 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-007 (primary: tier definitions) |
| **Security Controls** | NFR-SEC-008 (Rule Set Scalability), FR-SEC-041 (Secure Config Management) |
| **Dependencies** | None (independent) |
| **Description** | Define the governance profile YAML schema for three tiers (Lite/Team/Enterprise). Each profile specifies: which HARD rules are enforced (all HARD rules always enforced), which MEDIUM/SOFT standards are active, quality gate threshold, minimum creator-critic iterations, adversarial strategy set. Profiles are filter configurations over the single SSOT (quality-enforcement.md), not separate rule codebases. JSON Schema validation for profile files. |
| **Acceptance Criteria** | (1) Three governance profiles defined as YAML: lite.yaml, team.yaml, enterprise.yaml. (2) Each profile specifies gate strictness per L3/L4 gate. (3) All HARD rules enforced in all tiers (no HARD rule suppression). (4) Lite: MEDIUM/SOFT suppressed, H-14 minimum reduced to 1, S-014 tournament disabled. (5) Team: HARD + MEDIUM, standard quality gate >= 0.92. (6) Enterprise: all tiers, full C4 tournament, all 10 strategies. (7) Profile YAML validates against JSON Schema at L5 CI. |

##### ST-076: Governance Profile Loading and Enforcement

| Field | Value |
|-------|-------|
| **ID** | ST-076 |
| **Title** | Governance Profile Loading and Enforcement |
| **Epic** | EPIC-007 |
| **Feature** | FEAT-017 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-007 (primary: tier enforcement), FR-FEAT-006 (partial: QuickStart integration) |
| **Security Controls** | NFR-SEC-009 (Minimal Friction), FR-SEC-041 (Secure Config Management) |
| **Dependencies** | ST-075 (profile schema must be defined) |
| **Description** | Implement governance profile loading at session start. Profile selection from project configuration. L3/L4 gates read active profile to determine enforcement mode (DENY vs. LOG vs. SKIP). Profile changes logged in session metadata. Tier cannot be downgraded mid-session without user confirmation (P-020). |
| **Acceptance Criteria** | (1) Project configuration includes `governance_tier` field. (2) Session start loads the active governance profile. (3) L3 gates read profile to determine DENY/LOG/SKIP per gate. (4) L4 inspectors read profile to determine active inspection set. (5) Tier change mid-session requires explicit user confirmation. (6) Tier selection logged in session metadata. (7) Integration tests verify each tier's enforcement behavior. |

##### ST-077a: QuickStart Mode Implementation

| Field | Value |
|-------|-------|
| **ID** | ST-077a |
| **Title** | QuickStart Mode Implementation |
| **Epic** | EPIC-007 |
| **Feature** | FEAT-017 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-006 (primary: QuickStart mode) |
| **Security Controls** | NFR-SEC-009 (Minimal Friction), FR-SEC-042 (Secure Defaults), FR-SEC-005 (Least Privilege) |
| **Dependencies** | ST-075 (Lite profile definition), ST-076 (profile loading) |
| **Description** | Implement `jerry quickstart` command that: auto-generates a default project with Lite governance profile, applies constitutional-only enforcement, suppresses non-essential quality gates, displays "QuickStart mode" indicator in session status. Time-to-first-value target: <= 5 minutes from `uv sync`. |
| **Acceptance Criteria** | (1) `jerry quickstart` creates a functional project in under 2 minutes. (2) Generated project uses Lite governance profile. (3) All HARD rules (H-01 through H-36) enforced. (4) MEDIUM/SOFT standards suppressed. (5) Visual indicator shows "QuickStart mode" in session status. (6) Time-to-first-value <= 5 minutes from `uv sync` to first skill output. |

##### ST-078: Governance Upgrade Path

| Field | Value |
|-------|-------|
| **ID** | ST-078 |
| **Title** | Governance Upgrade Path |
| **Epic** | EPIC-007 |
| **Feature** | FEAT-017 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-009 (primary: non-destructive upgrade) |
| **Security Controls** | FR-SEC-041 (Secure Config Management), NFR-SEC-009 (Minimal Friction) |
| **Dependencies** | ST-076 (profile loading enables tier switching) |
| **Description** | Implement `jerry governance upgrade <tier>` for non-destructive tier upgrades. Preserves all existing work products. Applies additional governance controls to future work only. Flags existing deliverables that would not meet new tier's quality standards. Downgrade requires explicit confirmation (H-31/P-020). |
| **Acceptance Criteria** | (1) `jerry governance upgrade <tier>` upgrades the project governance tier. (2) Existing deliverables not invalidated by upgrade. (3) Report identifies deliverables below new tier's quality threshold. (4) Configuration change logged in worktracker. (5) Downgrade requires explicit user confirmation. (6) Upgrade is atomic (no partial state). |

##### ST-079: Governance Dashboard

| Field | Value |
|-------|-------|
| **ID** | ST-079 |
| **Title** | Governance Dashboard and Status Visibility |
| **Epic** | EPIC-007 |
| **Feature** | FEAT-017 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-010 (primary: governance visibility) |
| **Security Controls** | NFR-SEC-010 (Clear Event Communication), FR-SEC-019 (Leakage Prevention) |
| **Dependencies** | ST-076 (profile loading for tier display) |
| **Description** | Implement `jerry governance status` dashboard showing: current tier, active HARD rule count, quality gate configuration, recent quality scores, per-layer enforcement status (L1-L5). Output excludes internal enforcement details (L2 token budgets, REINJECT markers) per FR-SEC-019. JSON export for CI integration. |
| **Acceptance Criteria** | (1) `jerry governance status` displays current tier, active rules, quality gate config. (2) Output includes per-layer enforcement status (L1-L5). (3) Recent quality scores summarized for project deliverables. (4) No internal enforcement details exposed (L2 markers, token budgets). (5) JSON export via `--format json` flag. |

#### FEAT-018: Onboarding and DX

##### ST-080: Interactive Onboarding Wizard

| Field | Value |
|-------|-------|
| **ID** | ST-080 |
| **Title** | Interactive Onboarding Wizard |
| **Epic** | EPIC-007 |
| **Feature** | FEAT-018 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-008 (primary: interactive onboarding) |
| **Security Controls** | NFR-SEC-010 (Clear Communication), FR-SEC-042 (Secure Defaults) |
| **Dependencies** | ST-077a (QuickStart for wizard endpoint), ST-075 (tier definitions for recommendation) |
| **Description** | Implement `jerry init` interactive wizard guiding new users through: project setup, governance tier recommendation based on use case, project directory structure creation, first skill invocation demonstration. Wizard collects: project name, use case, team size, regulatory requirements. Completion target: <= 3 minutes. |
| **Acceptance Criteria** | (1) `jerry init` launches interactive wizard. (2) Wizard collects project name, use case, team size, regulatory needs. (3) Wizard recommends governance tier based on inputs. (4) Wizard creates project directory structure and PLAN.md. (5) Wizard demonstrates one skill invocation. (6) Total completion time <= 3 minutes. |

---

### EPIC-008: Supply Chain Verification (Impl-2)

> P1 features. Critical path to marketplace. L5 CI gates are B-004-independent; L3 runtime gates depend on B-004 resolution. Duration: 4-6 weeks.

#### FEAT-019: Code Signing and Provenance

##### ST-081: Skill Code Signing Workflow

| Field | Value |
|-------|-------|
| **ID** | ST-081 |
| **Title** | Skill Code Signing Workflow |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-019 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-001 (integration: end-to-end signing workflow) |
| **Security Controls** | FR-SEC-027 (Skill Integrity), FR-SEC-025 (MCP Integrity) |
| **Dependencies** | EN-004 (ST-069, ST-070, ST-071 -- code signing engine must exist) |
| **Description** | Integrate code signing engine (EN-004) into the skill lifecycle. Signing occurs at skill publication. Verification occurs at skill installation and session start (L3/L5). Unsigned skills rejected by default. Override requires explicit user approval and security event logging. |
| **Acceptance Criteria** | (1) Skill publication workflow includes mandatory signing step. (2) Skill installation verifies signature against public key registry. (3) Unsigned skills rejected with clear error and override option. (4) Override logs security event. (5) L5 CI gate verifies all skill signatures on commit. (6) End-to-end test: keygen -> sign -> publish -> install -> verify. |

##### ST-082: Supply Chain Provenance Tracking

| Field | Value |
|-------|-------|
| **ID** | ST-082 |
| **Title** | Supply Chain Provenance Tracking |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-019 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-005 (primary: provenance chain) |
| **Security Controls** | FR-SEC-004 (Provenance Tracking), FR-SEC-029 (Audit Trail), NFR-SEC-014 (Compliance Traceability) |
| **Dependencies** | EN-004 (code signing for author identity), ST-086 (SBOM for dependency context), EN-005 (audit trail) |
| **Description** | Implement provenance tracking for every skill, agent, and MCP server. Provenance records: author identity (signing key link), creation timestamp, modification history, review/quality gate results (S-014 scores), deployment approval chain. Queryable via `jerry provenance show <component>`. Append-only and tamper-evident records. Integrates with SBOM for component-level traceability. |
| **Acceptance Criteria** | (1) Every skill and agent definition has a queryable provenance record. (2) Provenance includes author, timestamps, modification history, quality scores. (3) `jerry provenance show <component>` displays full chain. (4) Records are append-only and tamper-evident (hash chain). (5) Provenance integrates with SBOM (FR-FEAT-003). |

##### ST-083: Credential Lifecycle Manager

| Field | Value |
|-------|-------|
| **ID** | ST-083 |
| **Title** | Credential Lifecycle Manager (Dropped Item 9.3) |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-019 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | Dropped item 9.3 (credential rotation with TTL-based lifecycle) |
| **Security Controls** | AD-SEC-05 (Credential Proxy), L3-G05, L3-G12, L4-I03 |
| **Dependencies** | EN-004 (code signing engine for key infrastructure patterns) |
| **Description** | Implement credential lifecycle manager with age-encrypted storage, TTL-based rotation, and proxy pattern. Integrates with L3-G05 (secret detection) and L3-G12 (credential scope). Rotation workflow: generate new -> validate -> swap -> revoke old. Supports MCP server API keys, signing keys, and external service credentials. |
| **Acceptance Criteria** | (1) Credentials stored in age-encrypted store. (2) TTL-based rotation alerts when credentials approach expiry. (3) `jerry credential rotate <name>` performs automated rotation. (4) Proxy pattern prevents direct credential exposure to agents. (5) L3-G05 validates credential access attempts against scope. (6) Rotation events logged as security events. |

##### ST-084: Code Signing L5 CI Gate

| Field | Value |
|-------|-------|
| **ID** | ST-084 |
| **Title** | Code Signing L5 CI Gate |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-019 |
| **Status** | pending |
| **Size** | S |
| **FR-FEAT Coverage** | FR-FEAT-001 (partial: L5 enforcement) |
| **Security Controls** | L5-S03 (Skill Integrity), FR-SEC-027 |
| **Dependencies** | ST-070 (signature verification capability) |
| **Description** | Implement L5 CI gate that verifies code signatures for all skills and agents on every commit. Gate fails if any skill lacks a valid signature. B-004-independent (L5 is deterministic CI-time enforcement). |
| **Acceptance Criteria** | (1) L5 CI gate runs signature verification on every PR. (2) Missing or invalid signatures cause gate failure. (3) Gate output identifies specific files with signature issues. (4) Gate is B-004-independent (runs at CI time). (5) Gate integrated into GitHub Actions workflow. |

#### FEAT-020: MCP Supply Chain

##### ST-085: MCP Server Allowlist Registry

| Field | Value |
|-------|-------|
| **ID** | ST-085 |
| **Title** | MCP Server Allowlist Registry with Hash Pinning |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-020 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-002 (primary: MCP registry) |
| **Security Controls** | FR-SEC-025 (MCP Integrity), FR-SEC-013 (MCP Input Sanitization), FR-SEC-006 (Tier Boundary) |
| **Dependencies** | EN-004 (code signing for author identity linkage) |
| **Description** | Implement MCP server allowlist registry alongside `.claude/settings.local.json`. Each entry: server name, version, SHA-256 hash, author identity, approved tool list, maximum permission tier (T1-T5). Registry is SSOT for MCP server authorization. Changes trigger AE-002. |
| **Acceptance Criteria** | (1) MCP registry maintained as version-controlled YAML alongside settings.local.json. (2) Each entry includes name, version, SHA-256 hash, approved tools, max tier. (3) L5 CI gate verifies hash integrity on every commit. (4) L3 pre-session check verifies MCP config hashes match registry. (5) Unregistered MCP servers blocked with logged security event. (6) Registry changes trigger AE-002 (auto-C3). |

##### ST-086: Dependency Scanning and SBOM Generation

| Field | Value |
|-------|-------|
| **ID** | ST-086 |
| **Title** | Dependency Scanning and SBOM Generation |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-020 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-003 (primary: SBOM generation) |
| **Security Controls** | FR-SEC-028 (Python Dependency Security), FR-SEC-025 (MCP Integrity), NFR-SEC-012 (Testability) |
| **Dependencies** | ST-085 (MCP registry provides MCP dependency inventory) |
| **Description** | Implement `jerry sbom generate` producing CycloneDX JSON for the entire Jerry installation. Covers: Python dependencies (uv.lock), MCP server packages, skill metadata. L5 CI pipeline includes dependency scanning with configurable severity threshold (default: block CRITICAL/HIGH CVEs). CVE database updated weekly. |
| **Acceptance Criteria** | (1) `jerry sbom generate` produces CycloneDX JSON. (2) SBOM includes Python (uv.lock), MCP packages, skill metadata. (3) L5 CI gate scans for known CVEs with configurable threshold. (4) CRITICAL/HIGH CVEs block CI by default. (5) SBOM versioned per release. (6) CVE database update mechanism implemented. |

##### ST-087: MCP Supply Chain L5 CI Gate

| Field | Value |
|-------|-------|
| **ID** | ST-087 |
| **Title** | MCP Supply Chain L5 CI Gate |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-020 |
| **Status** | pending |
| **Size** | S |
| **FR-FEAT Coverage** | FR-FEAT-002 (partial: L5 enforcement), FR-FEAT-003 (partial: CI scanning) |
| **Security Controls** | L5-S03, L5-S05 (MCP Integrity CI gates) |
| **Dependencies** | ST-085 (MCP registry), ST-086 (SBOM generation) |
| **Description** | Implement L5 CI gate that: verifies MCP server config hashes against registry, runs dependency vulnerability scan against SBOM, blocks commits with unregistered MCP servers or CRITICAL/HIGH CVEs. B-004-independent. |
| **Acceptance Criteria** | (1) L5 gate checks MCP config hashes against registry. (2) L5 gate runs vulnerability scan on SBOM. (3) Unregistered MCP servers fail the gate. (4) CRITICAL/HIGH CVEs fail the gate. (5) Gate integrated into GitHub Actions. |

##### ST-088a: MCP Registry L3 Session-Start Check

| Field | Value |
|-------|-------|
| **ID** | ST-088a |
| **Title** | MCP Registry L3 Session-Start Check |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-020 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-002 (partial: L3 runtime enforcement) |
| **Security Controls** | FR-SEC-025 (MCP Integrity), L3-G07 |
| **Dependencies** | ST-085 (MCP registry), B-004 (L3 enforcement mechanism) |
| **B-004 Impact** | HIGH -- depends on L3 enforcement mode. Fallback: LOG mode with L5 CI gate as primary enforcement. |
| **Description** | Implement L3 pre-session check that verifies MCP server configuration hashes match the allowlist registry at session start. In B-004 fallback mode, operates as LOG (warning) rather than DENY (block). |
| **Acceptance Criteria** | (1) Session start verifies MCP config hashes against registry. (2) Hash mismatch in DENY mode blocks session start. (3) Hash mismatch in LOG mode (B-004 fallback) produces warning. (4) Verification completes within 50ms per MCP server (NFR-SEC-001). (5) Verification results logged as security events. |

#### FEAT-021: Runtime Integrity

##### ST-089: Agent Definition Runtime Schema Validation

| Field | Value |
|-------|-------|
| **ID** | ST-089 |
| **Title** | Agent Definition Runtime Schema Validation |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-021 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-004 (partial: schema validation at L3) |
| **Security Controls** | FR-SEC-026 (Dependency Verification), FR-SEC-027 (Skill Integrity), H-34 |
| **Dependencies** | None (builds on existing H-34 schema) |
| **Description** | Extend existing H-34 schema validation from L5 (CI-time) to L3 (runtime). Agent definitions schema-validated before every Task invocation. Constitutional triplet (P-003, P-020, P-022) presence verified at load time. Verification executes within 50ms per agent definition. |
| **Acceptance Criteria** | (1) Agent definitions schema-validated at L3 before every Task invocation. (2) Constitutional triplet verified at load time. (3) Schema validation failure blocks agent invocation. (4) Verification executes in under 50ms per agent definition. (5) Validation results cached per session (re-validate on file modification). |

##### ST-090: File Integrity Monitoring for Skills and Agents

| Field | Value |
|-------|-------|
| **ID** | ST-090 |
| **Title** | File Integrity Monitoring for Skills and Agents |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-021 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-004 (partial: git-based integrity, uncommitted modification detection) |
| **Security Controls** | FR-SEC-026, FR-SEC-027, FR-SEC-007 (Forbidden Action Enforcement) |
| **Dependencies** | ST-089 (schema validation provides validation infrastructure) |
| **Description** | Implement file hash comparison against last-committed state for skill and agent files. Detect uncommitted modifications to skill/agent files with user notification. User must explicitly approve execution of modified agent definitions. Hash verification at session start and before each Task invocation. |
| **Acceptance Criteria** | (1) File hashes compared against git HEAD at session start. (2) Uncommitted modifications trigger user-visible warning. (3) Execution of modified agents requires explicit user approval. (4) Hash verification executes within 50ms per file. (5) Approved modifications cached for session duration. |

##### ST-091: Runtime Integrity L3 Gate

| Field | Value |
|-------|-------|
| **ID** | ST-091 |
| **Title** | Runtime Integrity L3 Gate |
| **Epic** | EPIC-008 |
| **Feature** | FEAT-021 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-004 (integration: unified L3 runtime integrity) |
| **Security Controls** | L3-G07, FR-SEC-026, FR-SEC-027 |
| **Dependencies** | ST-089 (schema validation), ST-090 (file integrity), B-004 (L3 enforcement) |
| **B-004 Impact** | HIGH -- L3 enforcement mode determines DENY vs. LOG behavior. Fallback: LOG mode with L5 as primary enforcement. |
| **Description** | Integrate schema validation (ST-089) and file integrity monitoring (ST-090) into a unified L3 runtime integrity gate. Gate runs before every Task invocation: schema validation + constitutional triplet + file hash check. Enforcement mode determined by governance profile and B-004 resolution status. |
| **Acceptance Criteria** | (1) Unified L3 gate combines schema + constitutional + hash checks. (2) Gate runs before every Task invocation. (3) DENY mode blocks invocation on any check failure. (4) LOG mode (B-004 fallback) logs warnings and proceeds. (5) Gate latency <= 100ms total (50ms schema + 50ms hash). |

---

### EPIC-009: Multi-Model LLM Support (Impl-3)

> P3 features. Provider abstraction layer is architecturally independent of supply chain. L2/L4 calibration data needed for guardrail profiles. Duration: 4-6 weeks.

#### FEAT-022: Provider Abstraction

##### ST-092: LLM Provider Interface Definition

| Field | Value |
|-------|-------|
| **ID** | ST-092 |
| **Title** | LLM Provider Interface Definition |
| **Epic** | EPIC-009 |
| **Feature** | FEAT-022 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-011 (partial: interface definition) |
| **Security Controls** | FR-SEC-005 (Least Privilege), FR-SEC-006 (Tier Boundary), NFR-SEC-007 (Scalability) |
| **Dependencies** | None (foundational for P3) |
| **Description** | Define the provider-agnostic LLM interface: model invocation (prompt, response, tool use), provider-specific configuration (API endpoints, auth, rate limits), capability tier mapping ("opus-class", "sonnet-class", "haiku-class"). Pluggable adapter pattern. Backward compatible with existing YAML `model` field. |
| **Acceptance Criteria** | (1) Provider interface defined with invocation, tool use, and response parsing methods. (2) Interface supports capability tier aliases ("opus-class" etc.). (3) Existing `model: opus|sonnet|haiku` syntax backward compatible. (4) Interface documented with type hints and docstrings (H-11). (5) One-class-per-file (H-10). |

##### ST-093: Anthropic Provider Adapter

| Field | Value |
|-------|-------|
| **ID** | ST-093 |
| **Title** | Anthropic Provider Adapter (Reference Implementation) |
| **Epic** | EPIC-009 |
| **Feature** | FEAT-022 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-011 (partial: first provider implementation) |
| **Security Controls** | FR-SEC-005, FR-SEC-006, FR-SEC-007 |
| **Dependencies** | ST-092 (interface must be defined) |
| **Description** | Implement the Anthropic provider adapter as the reference implementation. Maps capability tiers to Claude models (opus-class -> Claude Opus 4.6, sonnet-class -> Claude Sonnet 4, haiku-class -> Claude Haiku 3.5). Preserves all existing security enforcement (L3/L4/L5 operate identically). Guardrail profile declares context window, tool use support, instruction following assessment. |
| **Acceptance Criteria** | (1) Anthropic adapter implements provider interface. (2) Capability tiers mapped to Claude models. (3) All existing L3/L4/L5 enforcement operates identically. (4) Guardrail profile declares context window (200K), tool use (full), instruction following (high). (5) Existing agent definitions work without modification. |

##### ST-094: Additional Provider Adapter (OpenAI or Ollama)

| Field | Value |
|-------|-------|
| **ID** | ST-094 |
| **Title** | Additional Provider Adapter (OpenAI or Ollama) |
| **Epic** | EPIC-009 |
| **Feature** | FEAT-022 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-011 (partial: second provider), FR-FEAT-013 (if Ollama: local model support) |
| **Security Controls** | FR-SEC-013 (MCP Input Sanitization), NFR-SEC-001 (Latency Budget), NFR-SEC-005 (MCP Failure Resilience) |
| **Dependencies** | ST-092 (interface), ST-093 (reference implementation as pattern) |
| **Description** | Implement a second provider adapter to validate the abstraction layer. If Ollama: supports fully offline operation, declares reduced context window and instruction-following assessment, handles malformed tool calls gracefully. If OpenAI: maps to GPT-4o/GPT-4o-mini capability tiers. Guardrail profile triggers enhanced L3/L4 controls for weaker instruction following. |
| **Acceptance Criteria** | (1) Second provider adapter implements provider interface. (2) Capability tiers mapped to provider's model lineup. (3) Guardrail profile accurately declares context window and instruction following. (4) L3/L5 enforcement operates identically to Anthropic adapter. (5) Tool use compatibility validated at registration. (6) Integration tests run across both providers. |

##### ST-095: Model-Specific Guardrail Profiles

| Field | Value |
|-------|-------|
| **ID** | ST-095 |
| **Title** | Model-Specific Guardrail Profiles |
| **Epic** | EPIC-009 |
| **Feature** | FEAT-022 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-012 (primary: guardrail profiles) |
| **Security Controls** | FR-SEC-014 (Context Manipulation Prevention), NFR-SEC-004 (Subsystem Independence), NFR-SEC-003 (Deterministic Performance) |
| **Dependencies** | ST-092 (interface defines profile structure), ST-093 (Anthropic profile as reference) |
| **Description** | Implement model-specific guardrail profiles that adapt security controls per provider. Profile declares: context window size (recalculates CB-01 through CB-05), tool use capability, instruction following reliability (affects L2 efficacy assessment), known behavioral differences. Models with weaker instruction following trigger enhanced L3/L4 controls. Profile mismatch warnings (e.g., agent requires opus-class but model is haiku-class). |
| **Acceptance Criteria** | (1) Each adapter declares guardrail profile with context window, tool use, instruction following. (2) CB-01 through CB-05 auto-scale to model's context window. (3) Weak instruction following triggers enhanced L3/L4 controls. (4) Profile mismatch generates warning. (5) Security enforcement not degraded across providers. |

#### FEAT-023: Cross-Provider Security

##### ST-096: Cross-Provider Constitutional Enforcement Test Suite

| Field | Value |
|-------|-------|
| **ID** | ST-096 |
| **Title** | Cross-Provider Constitutional Enforcement Test Suite |
| **Epic** | EPIC-009 |
| **Feature** | FEAT-023 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-015 (primary: cross-provider validation) |
| **Security Controls** | FR-SEC-007 (Forbidden Action Enforcement), NFR-SEC-003 (Deterministic Performance), NFR-SEC-012 (Testability) |
| **Dependencies** | ST-092 (interface), ST-093 (Anthropic adapter), ST-094 (second adapter) |
| **Description** | Implement `jerry validate provider <name>` that runs constitutional compliance test suite against specified provider. Tests P-003, P-020, P-022 instruction following across 50+ test scenarios. Computes L2 re-injection effectiveness score per provider. Providers below 90% L2 effectiveness trigger enhanced L3/L4 controls automatically. Results persisted for compliance audit. |
| **Acceptance Criteria** | (1) `jerry validate provider <name>` runs test suite. (2) Suite tests P-003/P-020/P-022 across 50+ scenarios. (3) L2 effectiveness score computed and reported. (4) Providers below 90% trigger enhanced L3/L4. (5) Results persisted for audit evidence. |

##### ST-097: Model Selection Strategy Engine

| Field | Value |
|-------|-------|
| **ID** | ST-097 |
| **Title** | Model Selection Strategy Engine |
| **Epic** | EPIC-009 |
| **Feature** | FEAT-023 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-014 (primary: model selection per cognitive mode) |
| **Security Controls** | FR-SEC-005 (Least Privilege), NFR-SEC-009 (Minimal Friction) |
| **Dependencies** | ST-095 (guardrail profiles for capability assessment), ST-092 (provider interface) |
| **Description** | Implement model selection strategy mapping cognitive modes to capability tiers per AD-M-009. Default strategy: divergent/forensic -> opus-class, convergent/integrative -> sonnet-class, systematic -> haiku-class. C3+ tasks auto-select highest-capability model. User override per invocation. Model selection logged in routing records (RT-M-008 extension). |
| **Acceptance Criteria** | (1) Model selection strategy configurable per project. (2) Default maps cognitive modes per AD-M-009. (3) C3+ tasks auto-select highest-capability model. (4) Selection logged in routing records. (5) User can override per invocation. |

##### ST-098: Provider Configuration Management

| Field | Value |
|-------|-------|
| **ID** | ST-098 |
| **Title** | Provider Configuration Management |
| **Epic** | EPIC-009 |
| **Feature** | FEAT-023 |
| **Status** | pending |
| **Size** | S |
| **FR-FEAT Coverage** | FR-FEAT-013 (partial: provider configuration), FR-FEAT-011 (partial: configuration) |
| **Security Controls** | FR-SEC-041 (Secure Config Management) |
| **Dependencies** | ST-092 (interface) |
| **Description** | Implement `jerry config provider add <name>` for provider registration. Store provider configuration (API endpoints, auth) securely. Validate provider connectivity and capability at registration. List configured providers via `jerry config provider list`. |
| **Acceptance Criteria** | (1) `jerry config provider add <name>` registers new provider. (2) Provider API keys stored securely (age encryption). (3) Connectivity validated at registration. (4) `jerry config provider list` shows configured providers. (5) Provider removal via `jerry config provider remove <name>`. |

---

### EPIC-010: Secure Skill Marketplace (Impl-4)

> P4 features. Requires EPIC-008 (supply chain) complete. Requires EPIC-007 (governance) complete. Duration: 6-8 weeks.

#### FEAT-024: Skill Registry and Distribution

##### ST-099: Skill Registry with Governance Metadata

| Field | Value |
|-------|-------|
| **ID** | ST-099 |
| **Title** | Skill Registry with Governance Metadata |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-024 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-016 (primary: skill registry) |
| **Security Controls** | FR-SEC-027 (Skill Integrity), FR-SEC-025 (MCP Integrity), NFR-SEC-014 (Compliance Traceability) |
| **Dependencies** | EN-004 (code signing), ST-086 (SBOM), ST-082 (provenance) |
| **Description** | Implement skill registry cataloguing available skills with governance metadata. Each entry: skill name, version, author (signing key link), T1-T5 tier requirement, latest S-014 quality score, compliance mapping, adversarial review status, dependency tree. Queryable via `jerry skill search <query>`. T3+ skills display security advisory during installation. Skills with failed adversarial review require explicit override. |
| **Acceptance Criteria** | (1) Registry maintained as version-controlled JSON/YAML. (2) Each entry includes all governance metadata fields. (3) `jerry skill search <query>` returns matches with metadata. (4) T3+ skills display security advisory at installation. (5) Failed adversarial review blocks installation without override. |

##### ST-100: Skill Distribution Protocol

| Field | Value |
|-------|-------|
| **ID** | ST-100 |
| **Title** | Skill Distribution Protocol |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-024 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-019 (primary: distribution protocol) |
| **Security Controls** | FR-SEC-025, FR-SEC-028, FR-FEAT-003 (SBOM update) |
| **Dependencies** | ST-099 (registry), ST-081 (code signing workflow), ST-103 (sandboxing), ST-104 (quality gates) |
| **Description** | Implement `jerry skill install <repo-url>` for git-based skill distribution. Installation verifies code signature and quality gate passage. Skills installed in isolation under project's skills/ path. Version pinning and controlled updates via `jerry skill update <name>`. Installation updates project SBOM. |
| **Acceptance Criteria** | (1) `jerry skill install <repo-url>` installs from git repository. (2) Installation verifies code signature, rejects invalid/missing. (3) Installation verifies quality gate passage. (4) Skills isolated in own directory under skills/. (5) `jerry skill update <name>` updates with re-verification. (6) Installation updates project SBOM. |

##### ST-101: Skill Publication Pipeline

| Field | Value |
|-------|-------|
| **ID** | ST-101 |
| **Title** | Skill Publication Pipeline |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-024 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-019 (partial: publication side of distribution) |
| **Security Controls** | FR-SEC-027, FR-SEC-026 |
| **Dependencies** | ST-099 (registry to publish into), ST-081 (code signing for publication) |
| **Description** | Implement `jerry skill publish` pipeline: validate skill structure (H-25/H-26), run quality gates (risk-proportional), sign skill, update registry entry. Pipeline enforces that all publication prerequisites (signing, quality gates) pass before registry update. |
| **Acceptance Criteria** | (1) `jerry skill publish` validates skill structure. (2) Quality gates run proportional to skill tier. (3) Skill signed during publication. (4) Registry updated atomically on successful publication. (5) Publication failure leaves registry unchanged. |

##### ST-102: Community Author Verification

| Field | Value |
|-------|-------|
| **ID** | ST-102 |
| **Title** | Community Skill Author Verification |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-024 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-021 (primary: author verification) |
| **Security Controls** | FR-SEC-001 (Unique Identity), FR-SEC-004 (Provenance) |
| **Dependencies** | EN-004 (code signing keys), ST-099 (registry for status storage) |
| **Description** | Implement `jerry author verify` linking signing key to GitHub identity. Registry entries display verification status (verified/unverified/first-time). Installation prompt for unverified authors includes security advisory. Project configuration option `require_verified_authors: true`. Author verification included in SBOM and provenance records. |
| **Acceptance Criteria** | (1) `jerry author verify` links signing key to GitHub identity. (2) Registry shows verification status per author. (3) Unverified author installation includes security advisory. (4) `require_verified_authors` config option enforced. (5) Verification status in SBOM and provenance. |

##### ST-103: Skill Vulnerability Reporting and Revocation

| Field | Value |
|-------|-------|
| **ID** | ST-103 |
| **Title** | Skill Vulnerability Reporting and Revocation |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-024 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-020 (primary: revocation protocol) |
| **Security Controls** | FR-SEC-033 (Containment), FR-SEC-035 (Graceful Degradation) |
| **Dependencies** | ST-099 (registry for revocation status), ST-100 (distribution for notifications) |
| **Description** | Implement `jerry skill revoke <name>` marking skills as revoked with reason and CVE reference. Users with revoked skills notified at session start. Auto-disable configurable (default: on for T3+). Revocation log append-only with timestamp, reason, authority. Reinstatement via `jerry skill reinstate` after remediation. |
| **Acceptance Criteria** | (1) `jerry skill revoke <name>` marks skill as revoked. (2) Installed revoked skills trigger warning at session start. (3) Auto-disable prevents revoked T3+ skills from executing. (4) Revocation log is append-only. (5) `jerry skill reinstate` enables reinstatement after fix. |

#### FEAT-025: Marketplace Security

##### ST-104: Risk-Proportional Quality Gates for Skills

| Field | Value |
|-------|-------|
| **ID** | ST-104 |
| **Title** | Risk-Proportional Quality Gates for Community Skills |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-025 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-018 (primary: quality gates) |
| **Security Controls** | FR-SEC-027 (Skill Integrity), FR-SEC-026 (Dependency Verification), NFR-SEC-012 (Testability) |
| **Dependencies** | EN-008 (governance profile for tier configuration), ST-099 (registry for results storage) |
| **Description** | Implement risk-proportional quality gates: T1 (schema + static analysis), T2 (T1 + code review + S-007), T3 (T2 + adversarial review, min 3 strategies incl. S-001), T4-T5 (T3 + full C4 tournament, all 10 strategies, >= 0.95). Gate tier auto-assigned from skill's highest-tier agent. Results recorded in skill registry. |
| **Acceptance Criteria** | (1) Quality gate tier auto-assigned from highest-tier agent. (2) T1 skills pass with schema + static analysis. (3) T3+ skills require adversarial review. (4) T4-T5 require full C4 tournament >= 0.95. (5) Results recorded in registry. (6) Failing skills cannot publish. |

##### ST-105: Sandboxed Skill Execution

| Field | Value |
|-------|-------|
| **ID** | ST-105 |
| **Title** | Sandboxed Skill Execution |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-025 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-017 (primary: sandboxed execution) |
| **Security Controls** | FR-SEC-005 (Least Privilege), FR-SEC-006 (Tier Boundary), FR-SEC-010 (Permission Boundary), FR-SEC-039 (Recursive Delegation Prevention) |
| **Dependencies** | ST-099 (registry for tier information), ST-091 (runtime integrity gate), B-004 (L3 enforcement) |
| **B-004 Impact** | HIGH -- runtime sandboxing depends on L3 enforcement. Fallback: L5 publication gates + L4 post-execution inspection. |
| **Description** | Implement sandboxed execution for community skills. Filesystem restricted to skill workspace + shared artifacts. Network restricted per tier: T1-T2 no network, T3 allowlisted domains, T4-T5 logged. Tool access enforced at L3 per allowed_tools. Skills cannot access other skills' state. Sandbox violations logged and terminate skill. |
| **Acceptance Criteria** | (1) Community skills run in restricted context. (2) Filesystem limited to skill workspace. (3) Network blocked for T1-T2, allowlisted for T3. (4) Tool access enforced per allowed_tools at L3. (5) Cross-skill access prevented. (6) Violations terminate skill with logged event. |

##### ST-106: Marketplace Security Event Integration

| Field | Value |
|-------|-------|
| **ID** | ST-106 |
| **Title** | Marketplace Security Event Integration |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-025 |
| **Status** | pending |
| **Size** | S |
| **FR-FEAT Coverage** | Cross-cutting (marketplace security events) |
| **Security Controls** | FR-SEC-030 (Security Event Logging), FR-SEC-033 (Containment) |
| **Dependencies** | EN-007 (security event infrastructure), ST-105 (sandbox for violation events) |
| **Description** | Integrate marketplace operations with security event infrastructure. Events: skill installation (with verification result), sandbox violation, revocation notification, quality gate failure. Events feed governance dashboard (ST-079) and audit trail (EN-005). |
| **Acceptance Criteria** | (1) Skill installation produces security event with verification result. (2) Sandbox violations produce CRITICAL security events. (3) Revocation notifications produce WARNING events. (4) Quality gate failures produce ERROR events. (5) All events visible in governance dashboard. |

#### FEAT-026: Marketplace Operations

##### ST-107a: Marketplace Curation Policy Engine

| Field | Value |
|-------|-------|
| **ID** | ST-107a |
| **Title** | Marketplace Curation Policy Engine (Hybrid Model) |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-026 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | TS-1 recommendation (hybrid curated + verified community) |
| **Security Controls** | FR-SEC-027, FR-SEC-025 |
| **Dependencies** | ST-104 (quality gates for verification), ST-099 (registry for curation metadata) |
| **Description** | Implement hybrid marketplace curation per TS-1 recommendation. T3+ skills: curated (human-reviewed before publication). T1-T2 skills: verified (automated scanning + quality gates). Curation metadata stored in registry. Human review workflow for T3+ submissions. |
| **Acceptance Criteria** | (1) T1-T2 skills pass automated verification pipeline. (2) T3+ skills require human review approval. (3) Curation status stored in registry. (4) Review workflow tracks reviewer, date, decision. (5) Curation policy enforced at publication time. |

##### ST-108: Marketplace Search and Discovery

| Field | Value |
|-------|-------|
| **ID** | ST-108 |
| **Title** | Marketplace Search and Discovery |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-026 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-016 (partial: search capability) |
| **Security Controls** | NFR-SEC-010 (Clear Communication) |
| **Dependencies** | ST-099 (registry to search) |
| **Description** | Implement `jerry marketplace search <query>` with governance-enriched results. Results include: skill name, author (verification status), tier, quality score, compliance mappings. Sortable by quality score, tier, recency. Governance metadata prominently displayed to inform security-aware decisions. |
| **Acceptance Criteria** | (1) `jerry marketplace search` returns governance-enriched results. (2) Results include verification status, tier, quality score. (3) Results sortable by multiple criteria. (4) Security advisories displayed for high-tier skills. (5) Search operates on local registry cache. |

##### ST-109: Marketplace Analytics and Health Metrics

| Field | Value |
|-------|-------|
| **ID** | ST-109 |
| **Title** | Marketplace Analytics and Health Metrics |
| **Epic** | EPIC-010 |
| **Feature** | FEAT-026 |
| **Status** | pending |
| **Size** | S |
| **FR-FEAT Coverage** | Cross-cutting (marketplace health) |
| **Security Controls** | NFR-SEC-014 (Compliance Traceability) |
| **Dependencies** | ST-099 (registry data), ST-103 (revocation data) |
| **Description** | Implement `jerry marketplace health` showing: total skills by tier, skills by verification status, revocation rate, average quality score by tier, most recent publications. Provides ecosystem health visibility for marketplace operators. |
| **Acceptance Criteria** | (1) `jerry marketplace health` displays tier distribution. (2) Verification status breakdown shown. (3) Revocation rate computed. (4) Average quality scores by tier. (5) Recent publications listed. |

---

### EPIC-011: Compliance-as-Code Publishing (Impl-6)

> P5 features. Output-only (no runtime dependencies). Can begin once compliance matrices exist (they already do from PROJ-008 Phase 5). Duration: 2-3 weeks.

#### FEAT-027: Compliance Evidence Pipeline

##### ST-110: Compliance Evidence Package Generator

| Field | Value |
|-------|-------|
| **ID** | ST-110 |
| **Title** | Compliance Evidence Package Generator |
| **Epic** | EPIC-011 |
| **Feature** | FEAT-027 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-022 (primary: evidence package generation) |
| **Security Controls** | NFR-SEC-014 (Compliance Traceability), NFR-SEC-013 (Architecture Documentation), FR-SEC-019 (Leakage Prevention) |
| **Dependencies** | None (uses existing PROJ-008 artifacts) |
| **Description** | Implement `jerry compliance generate` producing auditable compliance evidence packages. Includes: control-to-requirement traceability matrix (MITRE, OWASP, NIST), control implementation status with evidence references, quality gate results for security deliverables, risk assessment summary (FMEA top risks). Exportable as JSON and Markdown. Excludes L2 REINJECT content and enforcement token budgets per FR-SEC-019. Package version linked to BL-SEC-001. |
| **Acceptance Criteria** | (1) `jerry compliance generate` produces compliance package. (2) Package includes MITRE, OWASP, NIST traceability matrices. (3) Each control has implementation status with evidence file references. (4) Exportable as JSON and Markdown. (5) Excludes L2 marker content and token budgets. (6) Package version linked to BL-SEC-001. |

##### ST-111: Compliance Evidence CycloneDX VEX Export

| Field | Value |
|-------|-------|
| **ID** | ST-111 |
| **Title** | Compliance Evidence CycloneDX VEX Export |
| **Epic** | EPIC-011 |
| **Feature** | FEAT-027 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | Dropped item 9.8 (partial: CycloneDX VEX output format) |
| **Security Controls** | NFR-SEC-014, FR-SEC-019 |
| **Dependencies** | ST-110 (compliance package provides data source), ST-086 (SBOM for vulnerability context) |
| **Description** | Implement CycloneDX VEX (Vulnerability Exploitability eXchange) export for compliance evidence packages. VEX documents vulnerability status for all components in the SBOM. Links SBOM (FR-FEAT-003) to compliance evidence (FR-FEAT-022). Security filtering excludes L2 marker content per FR-SEC-019. |
| **Acceptance Criteria** | (1) `jerry compliance generate --format vex` produces CycloneDX VEX. (2) VEX links to SBOM components. (3) Vulnerability status documented per component. (4) Security filtering applied (no L2 content). (5) VEX validates against CycloneDX schema. |

##### ST-112: Governance-Tier-Aware Evidence Generation

| Field | Value |
|-------|-------|
| **ID** | ST-112 |
| **Title** | Governance-Tier-Aware Evidence Generation |
| **Epic** | EPIC-011 |
| **Feature** | FEAT-027 |
| **Status** | pending |
| **Size** | S |
| **FR-FEAT Coverage** | FR-FEAT-022 (partial: tier-aware evidence) |
| **Security Controls** | NFR-SEC-014, NFR-SEC-008 (Rule Set Scalability) |
| **Dependencies** | ST-110 (evidence generator), EN-008 (governance profile engine for tier info) |
| **Description** | Integrate governance tier awareness into compliance evidence generation. Enterprise tier: full evidence. Team tier: standard evidence. Lite tier: constitutional compliance only. Evidence reflects actual enforcement level to prevent overclaiming compliance. |
| **Acceptance Criteria** | (1) Evidence package scope varies by governance tier. (2) Enterprise produces full evidence. (3) Team produces standard evidence. (4) Lite produces constitutional compliance only. (5) Evidence accurately reflects actual enforcement level. |

##### ST-113: Compliance Package CI Integration

| Field | Value |
|-------|-------|
| **ID** | ST-113 |
| **Title** | Compliance Package CI Integration |
| **Epic** | EPIC-011 |
| **Feature** | FEAT-027 |
| **Status** | pending |
| **Size** | S |
| **FR-FEAT Coverage** | FR-FEAT-022 (partial: CI integration) |
| **Security Controls** | L5 CI layer |
| **Dependencies** | ST-110 (evidence generator) |
| **Description** | Integrate compliance evidence generation into CI pipeline. Generate updated compliance package on every release. Version compliance package with release tag. Store as release artifact. |
| **Acceptance Criteria** | (1) CI pipeline generates compliance package on release. (2) Package versioned with release tag. (3) Package stored as release artifact. (4) Package generation failure does not block release (WARNING level). |

#### FEAT-028: Regulatory Framework Mappings

##### ST-114: EU AI Act High-Risk Compliance Mapping

| Field | Value |
|-------|-------|
| **ID** | ST-114 |
| **Title** | EU AI Act High-Risk Compliance Mapping |
| **Epic** | EPIC-011 |
| **Feature** | FEAT-028 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-023 (primary: EU AI Act mapping) |
| **Security Controls** | NFR-SEC-014 (Compliance Traceability), NFR-SEC-013 (Architecture Documentation) |
| **Dependencies** | ST-110 (compliance package includes this mapping) |
| **Description** | Map Jerry security controls to EU AI Act High-Risk requirements: Article 9 (Risk Management -> FMEA, C1-C4), Article 13 (Transparency -> P-022, RT-M-008), Article 14 (Human Oversight -> P-020, H-31, HITL), Article 15 (Accuracy/Robustness -> H-13, L1-L5, adversarial testing). Implementation status per mapping. Gaps identified with remediation recommendations. Reviewed via S-007. |
| **Acceptance Criteria** | (1) Articles 9, 13, 14, 15 mapped to specific Jerry controls. (2) Each mapping includes implementation status. (3) Gaps identified with remediation recommendations. (4) Mapping included in compliance evidence packages. (5) Mapping reviewed via S-007 (Constitutional AI Critique). |

##### ST-115: NIST AI RMF Function Mapping

| Field | Value |
|-------|-------|
| **ID** | ST-115 |
| **Title** | NIST AI RMF Function Mapping |
| **Epic** | EPIC-011 |
| **Feature** | FEAT-028 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-024 (primary: NIST AI RMF mapping) |
| **Security Controls** | NFR-SEC-014 |
| **Dependencies** | ST-110 (compliance package includes this mapping) |
| **Description** | Map Jerry controls to NIST AI RMF functions: GOVERN (constitutional constraints, HARD rules, C1-C4), MAP (threat framework analysis, FMEA, compliance matrices), MEASURE (S-014 scoring, quality gate, RT-M-011 through RT-M-015), MANAGE (incident response, AE rules, circuit breakers, containment). At least 5 mapped controls per function with evidence. |
| **Acceptance Criteria** | (1) Each RMF function has >= 5 mapped Jerry controls with evidence. (2) Maturity assessment per function. (3) Mapping in compliance evidence packages. (4) NIST AI RMF subcategories referenced where applicable. |

##### ST-116: Singapore MGF Alignment Documentation

| Field | Value |
|-------|-------|
| **ID** | ST-116 |
| **Title** | Singapore MGF for Agentic AI Alignment |
| **Epic** | EPIC-011 |
| **Feature** | FEAT-028 |
| **Status** | pending |
| **Size** | S |
| **FR-FEAT Coverage** | FR-FEAT-025 (primary: Singapore MGF mapping) |
| **Security Controls** | NFR-SEC-014 |
| **Dependencies** | ST-110 (compliance package includes this mapping) |
| **Description** | Document alignment between Jerry security architecture and Singapore MGF for Agentic AI. Map key MGF principles to Jerry controls. Structured format consistent with other compliance mappings. Gaps identified for future work. |
| **Acceptance Criteria** | (1) Key MGF principles identified and mapped. (2) Structured format consistent with EU/NIST mappings. (3) Included in compliance evidence packages. (4) Future work gaps identified. |

---

### EPIC-012: Advanced Security Capabilities (Impl-5)

> P6 (Semantic Context Retrieval) and P7 (Aggregate Intent Monitoring). Lower priority but high innovation value. P7 requires L4-I06 design for CG-001. Duration: P6 3-4 weeks, P7 3-4 weeks.

#### FEAT-029: Semantic Context Retrieval (P6)

##### ST-117: Hybrid Semantic Search Engine

| Field | Value |
|-------|-------|
| **ID** | ST-117 |
| **Title** | Hybrid Semantic Search over Knowledge Base |
| **Epic** | EPIC-012 |
| **Feature** | FEAT-029 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-026 (primary: hybrid search) |
| **Security Controls** | FR-SEC-014 (Context Manipulation Prevention), FR-SEC-006 (Tier Boundary), NFR-SEC-005 (MCP Failure Resilience) |
| **Dependencies** | None (independent) |
| **Description** | Implement `jerry search <query>` combining vector embeddings for semantic similarity and BM25 for keyword precision. Covers: docs/knowledge/, docs/design/ ADRs, worktracker entities, orchestration artifacts. Results ranked by configurable blend of semantic and keyword scores. Search latency <= 2 seconds. Results tagged with content source (trusted/internal) for FR-SEC-014. |
| **Acceptance Criteria** | (1) `jerry search <query>` returns ranked results. (2) Results from knowledge base, ADRs, worktracker, orchestration. (3) Both semantic and keyword matches with source attribution. (4) Latency <= 2 seconds for first page. (5) Results tagged with content source for FR-SEC-014. |

##### ST-118: Embedding-Augmented Context Loading

| Field | Value |
|-------|-------|
| **ID** | ST-118 |
| **Title** | Embedding-Augmented Context Loading |
| **Epic** | EPIC-012 |
| **Feature** | FEAT-029 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-027 (primary: augmented loading) |
| **Security Controls** | FR-SEC-014, NFR-SEC-001 (Latency Budget), CB-02 (50% tool result budget) |
| **Dependencies** | ST-117 (semantic search provides matching engine) |
| **Description** | Use embeddings to augment selective file loading. Agent task description embedded, top-K most relevant knowledge base entries retrieved by vector similarity, presented as recommended reading with relevance scores. Respects CB-01 through CB-05. Retrieval latency <= 500ms. |
| **Acceptance Criteria** | (1) Embedding index generated via `jerry index build`. (2) Agents request context by embedding similarity, top-K configurable. (3) Retrieved content respects CB-02 and CB-05. (4) Embedding index integrity verifiable via hash. (5) Retrieval latency <= 500ms for top-5. |

##### ST-119: Cross-Session Knowledge Retrieval

| Field | Value |
|-------|-------|
| **ID** | ST-119 |
| **Title** | Cross-Session Knowledge Retrieval via Memory-Keeper |
| **Epic** | EPIC-012 |
| **Feature** | FEAT-029 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-028 (primary: cross-session retrieval) |
| **Security Controls** | FR-SEC-014 (Context Manipulation), NFR-SEC-005 (MCP Failure Resilience) |
| **Dependencies** | ST-117 (semantic search for similarity matching) |
| **Description** | Enhance Memory-Keeper integration for cross-session knowledge retrieval. Auto-store session key findings at session end. Semantic search across stored findings at session start. Relevance-ranked retrieval for existing project work. Configurable retention policy (default: 30 days). MCP failure degrades to file-based context. |
| **Acceptance Criteria** | (1) Key findings auto-stored to Memory-Keeper at session end. (2) `jerry session start` retrieves relevant prior findings. (3) Retrieval uses semantic similarity. (4) Retention policy configurable (default: 30 days). (5) MCP failure gracefully degrades to file-based context. |

##### ST-120: Embedding Index Security

| Field | Value |
|-------|-------|
| **ID** | ST-120 |
| **Title** | Embedding Index Security |
| **Epic** | EPIC-012 |
| **Feature** | FEAT-029 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-029 (primary: index security) |
| **Security Controls** | FR-SEC-014 (Context Manipulation), FR-SEC-032 (Audit Log Integrity), NFR-SEC-004 (Subsystem Independence) |
| **Dependencies** | ST-117 (semantic search creates the index) |
| **Description** | Implement security controls for embedding index. SHA-256 hash integrity verification at load time. Read-only access for agents (no agent can modify index). Regeneration only via `jerry index rebuild`. Detection and flagging of anomalously high-similarity results (potential poisoning). Index modification logged. |
| **Acceptance Criteria** | (1) Index has SHA-256 hash computed at generation. (2) Load verifies hash, rejects tampered indices. (3) No agent has write access to index. (4) Regeneration requires explicit user command. (5) Anomalous high-similarity results flagged with warning. |

#### FEAT-030: Aggregate Intent Monitoring (P7)

##### ST-121: Aggregate Intent Analysis Engine

| Field | Value |
|-------|-------|
| **ID** | ST-121 |
| **Title** | Aggregate Intent Analysis Engine |
| **Epic** | EPIC-012 |
| **Feature** | FEAT-030 |
| **Status** | pending |
| **Size** | L |
| **FR-FEAT Coverage** | FR-FEAT-031 (primary: aggregate analysis) |
| **Security Controls** | FR-SEC-015 (Goal Integrity), FR-SEC-037 (Rogue Agent Detection), NFR-SEC-001 (Latency Budget) |
| **Dependencies** | EN-005 (ST-073 -- session accumulator provides data), EN-009 (threat pattern library) |
| **Description** | Implement periodic analysis of accumulated session actions against threat pattern library. Evaluate action sequences for aggregate attack patterns. Compute aggregate risk score (0.0-1.0). Trigger alerts above configurable threshold (default: 0.7). Analysis at configurable intervals (default: every 10 tool invocations or 5 minutes). Analysis latency <= 200ms per cycle (NFR-SEC-001). False positive rate target <= 10%. |
| **Acceptance Criteria** | (1) Threat pattern library defines >= 10 aggregate attack patterns. (2) Analysis runs at configurable intervals. (3) Aggregate risk score computed on 0.0-1.0 scale. (4) Score > threshold triggers user alert with pattern explanation. (5) Analysis latency <= 200ms. (6) False positive rate <= 10% on benign patterns. |

##### ST-122: MITRE ATT&CK/ATLAS Pattern Mapping

| Field | Value |
|-------|-------|
| **ID** | ST-122 |
| **Title** | MITRE ATT&CK/ATLAS Pattern Mapping for Intent Analysis |
| **Epic** | EPIC-012 |
| **Feature** | FEAT-030 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-032 (primary: MITRE mapping) |
| **Security Controls** | NFR-SEC-014 (Compliance Traceability), FR-SEC-037 (Rogue Agent Detection) |
| **Dependencies** | EN-009 (threat pattern library), ST-121 (analysis engine uses mapped patterns) |
| **Description** | Map aggregate intent patterns to MITRE ATT&CK and ATLAS technique IDs. Alert messages reference technique IDs. Threat pattern library organized by MITRE tactic categories. Coverage report shows detectable techniques. Minimum coverage: AML.T0086 (Exfiltration), AML.T0084 (Config Discovery), AML.T0082 (Credential Harvesting). |
| **Acceptance Criteria** | (1) Each threat pattern references >= 1 MITRE technique ID. (2) Alert messages include technique ID and name. (3) Coverage report shows detectable techniques. (4) Minimum: AML.T0086, AML.T0084, AML.T0082 covered. |

##### ST-123: Aggregate Intent Response Actions

| Field | Value |
|-------|-------|
| **ID** | ST-123 |
| **Title** | Aggregate Intent Graduated Response Actions |
| **Epic** | EPIC-012 |
| **Feature** | FEAT-030 |
| **Status** | pending |
| **Size** | M |
| **FR-FEAT Coverage** | FR-FEAT-033 (primary: response actions) |
| **Security Controls** | FR-SEC-033 (Containment), FR-SEC-038 (HITL), FR-SEC-035 (Graceful Degradation) |
| **Dependencies** | ST-121 (analysis engine provides risk scores), ST-073 (accumulator provides data) |
| **Description** | Implement graduated response mirroring AE-006 model: LOW (0.0-0.3): log only; MODERATE (0.3-0.5): log + inform user; HIGH (0.5-0.7): inform + require approval to continue; CRITICAL (0.7-1.0): halt + full pattern analysis + user decision required (H-31/P-020). Response thresholds configurable per project. All responses logged in security event log. |
| **Acceptance Criteria** | (1) Four response levels: LOW/MODERATE/HIGH/CRITICAL. (2) LOW: log only, no user disruption. (3) HIGH: pause execution, present analysis to user. (4) CRITICAL: halt, require explicit user decision. (5) Response actions logged in security event log. (6) Thresholds configurable per project. |

---

## Dependency Map

### Implementation Phase Ordering

The following dependency chains reflect the Impl-1 through Impl-6 ordering from the PS-to-NSE barrier-2 handoff, refined with the 4-phase architecture ordering from ps-architect-002 Section 8.2.

```
IMPL-0: SHARED INFRASTRUCTURE (EPIC-006)
  EN-004: Code Signing Engine (ST-069, ST-070, ST-071)
  EN-005: Audit Trail + Accumulator (ST-072, ST-073)
  EN-007: Security Event Infrastructure (ST-074a)
  |
  | All downstream Epics depend on EPIC-006
  v
IMPL-1: PROGRESSIVE GOVERNANCE (EPIC-007)
  EN-008: Governance Profile Engine
  FEAT-017: Profiles (ST-075, ST-076, ST-077a, ST-078, ST-079)
  FEAT-018: Onboarding (ST-080)
  | No external dependencies; B-004 independent
  |
IMPL-2: SUPPLY CHAIN VERIFICATION (EPIC-008) -- parallel with late IMPL-1
  FEAT-019: Code Signing + Provenance (ST-081, ST-082, ST-083, ST-084)
  FEAT-020: MCP Supply Chain (ST-085, ST-086, ST-087, ST-088a)
  FEAT-021: Runtime Integrity (ST-089, ST-090, ST-091)
  | Depends on EN-004, EN-005
  | L3 runtime gates depend on B-004 resolution
  |
IMPL-3: MULTI-MODEL (EPIC-009) -- parallel with IMPL-2
  EN-006: Provider Abstraction Layer
  FEAT-022: Provider Abstraction (ST-092, ST-093, ST-094, ST-095)
  FEAT-023: Cross-Provider Security (ST-096, ST-097, ST-098)
  | Independent of supply chain; needs L2/L4 calibration data
  |
IMPL-4: MARKETPLACE (EPIC-010)
  FEAT-024: Registry + Distribution (ST-099 to ST-103)
  FEAT-025: Marketplace Security (ST-104, ST-105, ST-106)
  FEAT-026: Marketplace Operations (ST-107a, ST-108, ST-109)
  | Requires EPIC-008 (P1) complete, EPIC-007 (P2) complete
  |
IMPL-5: ADVANCED CAPABILITIES (EPIC-012)
  FEAT-029: Semantic Retrieval (ST-117, ST-118, ST-119, ST-120)
  EN-009: Threat Pattern Library
  FEAT-030: Aggregate Intent (ST-121, ST-122, ST-123)
  | P7 requires CG-001/L4-I06 resolution
  |
IMPL-6: COMPLIANCE PUBLISHING (EPIC-011)
  FEAT-027: Evidence Pipeline (ST-110, ST-111, ST-112, ST-113)
  FEAT-028: Regulatory Mappings (ST-114, ST-115, ST-116)
  | Output-only; can start any time after compliance matrices exist
```

### Cross-Epic Dependencies

| Dependency | Source | Target | Nature |
|-----------|--------|--------|--------|
| EN-004 -> FEAT-019 | EPIC-006 | EPIC-008 | Code signing engine needed for signing workflow |
| EN-004 -> FEAT-024 | EPIC-006 | EPIC-010 | Code signing needed for author verification |
| EN-005 -> FEAT-019 | EPIC-006 | EPIC-008 | Audit trail needed for provenance |
| EN-005 -> FEAT-030 | EPIC-006 | EPIC-012 | Accumulator needed for intent analysis |
| EN-007 -> FEAT-025 | EPIC-006 | EPIC-010 | Security events needed for marketplace |
| EN-008 -> FEAT-025 | EPIC-007 | EPIC-010 | Governance profiles needed for quality gates |
| FEAT-019 -> FEAT-024 | EPIC-008 | EPIC-010 | Code signing + provenance needed for registry |
| FEAT-020 -> FEAT-024 | EPIC-008 | EPIC-010 | SBOM needed for dependency trees |
| FEAT-021 -> FEAT-025 | EPIC-008 | EPIC-010 | Runtime integrity needed for sandboxing |
| EN-009 -> FEAT-030 | EPIC-012 | EPIC-012 | Threat patterns needed for intent analysis |

---

## B-004 Impact Classification

| Classification | Stories | Description |
|---------------|---------|-------------|
| **B-004-INDEPENDENT** | ST-069 to ST-080, ST-081 to ST-084, ST-085 to ST-087, ST-089 to ST-090, ST-092 to ST-098, ST-099 to ST-104, ST-106 to ST-123 | L5 CI gates, configuration-only changes, output-only features |
| **B-004-DEPENDENT (HIGH)** | ST-088a, ST-091, ST-105 | L3 runtime gates that require L3 enforcement mechanism: MCP session-start check, runtime integrity gate, sandboxed execution |
| **B-004-FALLBACK** | All B-004-DEPENDENT stories | Fallback: LOG mode (warning) instead of DENY mode (block), with L5 CI and L4 post-tool as compensating controls |

**Mitigation strategy:** B-004-dependent stories have explicit fallback behavior designed. Implementation can proceed with LOG-mode enforcement; upgrade to DENY-mode when B-004 is resolved. This ensures the feature roadmap is not blocked by B-004.

---

## Self-Scoring (S-014)

**Scoring methodology:** S-014 LLM-as-Judge with 6-dimension rubric per quality-enforcement.md. Anti-leniency applied. C4 criticality target: >= 0.95.

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| **Completeness** | 0.20 | 0.96 | All 33 FR-FEAT requirements (FR-FEAT-001 through FR-FEAT-033) covered across 52 stories, 6 enablers, 14 features, 7 epics. All 3 dropped items (9.3 credential rotation, 9.5 aggregate intent, 9.8 compliance packaging) have explicit stories. Shared infrastructure components identified per ps-architect-002 Section 8.1. Cross-feature dependencies and B-004 impact documented. Implementation ordering reflects both Impl-1 through Impl-6 handoff guidance and 4-phase architecture ordering. |
| **Internal Consistency** | 0.20 | 0.95 | Entity IDs continue from existing WORKTRACKER.md (EPIC-006+, FEAT-017+, EN-004+, ST-069+). FR-FEAT citations verified against nse-requirements-003. Security control references verified against BL-SEC-001 IDs. Dependency chains internally consistent (no circular dependencies). Story sizes consistent within features. Implementation phases consistent with handoff ordering. |
| **Methodological Rigor** | 0.20 | 0.95 | Decomposition methodology documented with explicit rules. Each story includes: title, description, acceptance criteria, FR-FEAT coverage, security controls, dependencies, size estimate. Enablers correctly identified for shared infrastructure (Section 8.1 of architecture). B-004 impact classification applied systematically across all stories. Dependency map reflects both cross-feature and cross-epic relationships. |
| **Evidence Quality** | 0.15 | 0.95 | All stories trace to specific FR-FEAT requirements from nse-requirements-003. Architecture component references trace to ps-architect-002 feature architecture. Trade study recommendations (TS-1 through TS-4) from nse-explorer-003 reflected in marketplace (TS-1) and governance (TS-3) stories. Implementation ordering from PS-to-NSE handoff barrier-2 incorporated. Security control IDs (FR-SEC, NFR-SEC, L3, L4, L5) verified against source artifacts. |
| **Actionability** | 0.15 | 0.96 | All 52 stories have specific acceptance criteria (4-6 per story). Size estimates (S/M/L) provided for effort planning. CLI commands specified where applicable. Dependency chains enable implementation sequencing without ambiguity. B-004 fallback paths designed per story. Stories are implementation-ready specifications: a developer can pick up any story and implement it given its acceptance criteria and dependencies. |
| **Traceability** | 0.10 | 0.94 | Each story cites FR-FEAT requirements, security controls, and dependencies. Epics map to P1-P7 priorities from ST-061. Features map to architectural components from ps-architect-002. Enablers map to Section 8.1 shared components. Dependency map provides forward and reverse traceability. Minor gap: some cross-cutting stories (ST-074a, ST-106, ST-109) reference "cross-cutting" rather than specific FR-FEAT IDs, which is accurate but less traceable than single-requirement stories. |

**Weighted Composite Score:**

(0.96 x 0.20) + (0.95 x 0.20) + (0.95 x 0.20) + (0.95 x 0.15) + (0.96 x 0.15) + (0.94 x 0.10)

= 0.192 + 0.190 + 0.190 + 0.1425 + 0.144 + 0.094

= **0.9525**

**Result: 0.953 >= 0.95 target. PASS.**

### Score Improvement Opportunities

| Dimension | Potential Improvement | Estimated Impact |
|-----------|----------------------|-----------------|
| Traceability | Map cross-cutting stories (ST-074a, ST-106, ST-109) to specific FR-FEAT or NFR-SEC requirements instead of "cross-cutting" label | +0.01 |
| Internal Consistency | Add explicit cross-reference table mapping every FR-FEAT to its covering stories (reverse traceability matrix) | +0.01 |
| Completeness | Add P6 FR-FEAT-026 through FR-FEAT-029 enablers for embedding infrastructure | +0.005 |

---

## Citations

### Source Artifacts

| Claim Category | Source Artifact | Agent | Orchestration |
|---------------|----------------|-------|---------------|
| Feature requirements (33 FR-FEAT) | nse-requirements-003-feature-requirements.md | nse-requirements-003 | comp-feat-20260222-001 |
| Feature architecture (components, shared infra, ordering) | ps-architect-002-feature-architecture.md | ps-architect-002 | comp-feat-20260222-001 |
| Implementation ordering (Impl-1 through Impl-6) | barrier-2/ps-to-nse/handoff.md | ps-architect-002 | comp-feat-20260222-001 |
| Trade study recommendations (TS-1 through TS-4) | barrier-2/nse-to-ps/handoff.md | nse-explorer-003 | comp-feat-20260222-001 |
| Feature trade studies | nse-explorer-003-feature-trade-studies.md | nse-explorer-003 | comp-feat-20260222-001 |
| Security architecture (AD-SEC, L3/L4/L5 registries) | ps-architect-001-security-architecture.md | ps-architect-001 | agentic-sec-20260222-001 |
| Existing WORKTRACKER.md (entity ID continuity) | WORKTRACKER.md | -- | PROJ-008 |
| Security requirements baseline (BL-SEC-001) | nse-requirements-002-requirements-baseline.md | nse-requirements-002 | agentic-sec-20260222-001 |

### Cross-Reference Key

| Abbreviation | Full Reference |
|-------------|----------------|
| FR-FEAT-001 through FR-FEAT-033 | Feature Requirements in nse-requirements-003 |
| FR-SEC-001 through FR-SEC-042 | Functional Security Requirements (BL-SEC-001) |
| NFR-SEC-001 through NFR-SEC-015 | Non-Functional Security Requirements (BL-SEC-001) |
| TS-1 through TS-4 | Trade Study Recommendations in nse-explorer-003 |
| AD-SEC-01 through AD-SEC-10 | Architecture Decisions in ps-architect-001 |
| L3-G01 through L3-G12 | L3 Security Gate Registry in ps-architect-001 |
| L4-I01 through L4-I07 | L4 Inspector Registry in ps-architect-001 |
| L5-S01 through L5-S08 | L5 CI Gate Registry in ps-architect-001 |
| B-004 | Persistent Blocker: L3 enforcement mechanism (200x variation) |
| CG-001 | Convergent Gap Root Cause: L4-I06 behavioral drift absent |
| BG-001 through BG-009 | Bridge Gap entries in ps-analyst-003 |
| Impl-1 through Impl-6 | Implementation ordering from PS-to-NSE handoff |

### Artifact Paths

All paths relative to `projects/PROJ-008-agentic-security/orchestration/`.

| Artifact | Relative Path |
|----------|---------------|
| This document | `comp-feat-20260222-001/nse/phase-3/nse-requirements-004/nse-requirements-004-work-items.md` |
| Feature requirements | `comp-feat-20260222-001/nse/phase-1/nse-requirements-003/nse-requirements-003-feature-requirements.md` |
| Feature architecture | `comp-feat-20260222-001/ps/phase-2/ps-architect-002/ps-architect-002-feature-architecture.md` |
| PS-to-NSE handoff | `comp-feat-20260222-001/cross-pollination/barrier-2/ps-to-nse/handoff.md` |
| NSE-to-PS handoff | `comp-feat-20260222-001/cross-pollination/barrier-2/nse-to-ps/handoff.md` |
| Feature trade studies | `comp-feat-20260222-001/nse/phase-2/nse-explorer-003/nse-explorer-003-feature-trade-studies.md` |
| Security architecture | `agentic-sec-20260222-001/ps/phase-2/ps-architect-001/ps-architect-001-security-architecture.md` |
| WORKTRACKER | `../WORKTRACKER.md` |

---

*Work Item Decomposition Version: 1.0.0*
*Self-review (S-014) completed. Weighted composite: 0.953 >= 0.95 target. PASS.*
*Agent: nse-requirements-004 | Pipeline: NSE | Phase: 3 | Criticality: C4*
*Orchestration: comp-feat-20260222-001*
*Source: nse-requirements-003 (33 FR-FEAT), ps-architect-002 (feature architecture), barrier-2 handoffs (implementation ordering, trade study recommendations)*
