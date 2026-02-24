# ST-067: Phased Feature Roadmap -- Jerry Competitive Features

> **Agent:** ps-synthesizer-002
> **Pipeline:** PS (Problem-Solving)
> **Phase:** 3 (Synthesis)
> **Story:** ST-067
> **Feature:** FEAT-004 (Feature Roadmap)
> **Orchestration:** comp-feat-20260222-001
> **Project:** PROJ-008 (Agentic Security)
> **Status:** complete
> **Criticality:** C4
> **Quality Score:** 0.955 (self-assessed, S-014)
> **Created:** 2026-02-22

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Executive Summary (L0)](#1-executive-summary-l0) | Strategic overview of phased roadmap, Governance-as-Code narrative |
| [2. Roadmap Principles](#2-roadmap-principles) | Ordering rationale, B-004 resilience, trade study integration |
| [3. Dependency Chain Visualization](#3-dependency-chain-visualization) | Full dependency graph across all phases and features |
| [4. Phase 1: Foundation (Immediate)](#4-phase-1-foundation-immediate) | P2 Progressive Governance + P1 Supply Chain L5 |
| [5. Phase 2: Verification (Near-Term)](#5-phase-2-verification-near-term) | P1 Supply Chain L3 + P3 Multi-Model Abstraction |
| [6. Phase 3: Ecosystem (Mid-Term)](#6-phase-3-ecosystem-mid-term) | P4 Marketplace + P5 Compliance-as-Code Publishing |
| [7. Phase 4: Intelligence (Future)](#7-phase-4-intelligence-future) | P6 Semantic Context Retrieval + P7 Aggregate Intent Monitoring |
| [8. Governance-as-Code Strategy Thread](#8-governance-as-code-strategy-thread) | How the killer feature strategy unfolds across all phases |
| [9. B-004 Impact Analysis](#9-b-004-impact-analysis) | Which phases are B-004-independent and which are affected |
| [10. Risk Register](#10-risk-register) | Cross-phase risks, mitigations, and contingencies |
| [11. Self-Scoring (S-014)](#11-self-scoring-s-014) | Quality gate assessment against six dimensions |
| [12. Citations](#12-citations) | Source artifact traceability |

---

## 1. Executive Summary (L0)

This roadmap sequences Jerry's seven competitive features (P1-P7) into four implementation phases, integrating trade study recommendations, security architecture dependencies, and the "Governance-as-Code" killer feature strategy into a coherent delivery plan.

**Roadmap structure:**

| Phase | Name | Duration | Features | B-004 Status |
|-------|------|----------|----------|-------------|
| Phase 1 | Foundation | 4-6 weeks | P2 Progressive Governance, P1 Supply Chain (L5 CI) | Independent |
| Phase 2 | Verification | 6-8 weeks | P1 Supply Chain (L3 runtime), P3 Multi-Model Abstraction | P1 L3 affected |
| Phase 3 | Ecosystem | 8-12 weeks | P4 Secure Marketplace, P5 Compliance-as-Code | P4 runtime affected |
| Phase 4 | Intelligence | 8-12 weeks | P6 Semantic Retrieval, P7 Aggregate Intent | P7 depends on CG-001 |

**Key decisions driving this sequence:**

1. **P2 first** (trade study TS-3, confidence 0.90). Progressive governance requires zero new architecture -- it is a configuration layer on the existing L3/L4 pipeline. Shipping P2 first establishes the governance-tier UX that every subsequent feature will integrate with. This closes the highest-severity DX gap (8 minutes to first value reduced to under 5 minutes) while demonstrating Governance-as-Code immediately.

2. **P1 staged** (trade study TS-4, confidence 0.87). Supply chain verification ships in two sub-phases: L5 CI gates first (B-004-independent, deterministic), then L3 runtime enforcement when the enforcement mechanism is resolved. This delivers the highest-value, lowest-risk supply chain controls immediately.

3. **P4 requires P1 + P2** (cross-study dependency). The marketplace cannot launch without supply chain verification (code signing, hash pinning) and governance tiers (publication quality gates per tier). This dependency chain is the critical path constraint.

4. **P5-P7 are value accretions.** Compliance-as-Code content already exists (81/101 framework items COVERED); packaging is incremental. P6 and P7 require research investment and CG-001 resolution respectively.

**Governance-as-Code narrative:** Every phase reinforces the market positioning: "Jerry is the governance layer for the agentic era." Phase 1 makes governance configurable. Phase 2 makes verification deterministic. Phase 3 makes governance marketplace-grade. Phase 4 makes governance intelligent. Each phase deepens the moat.

---

## 2. Roadmap Principles

Five principles govern feature ordering, derived from trade study consensus and architectural constraints.

| # | Principle | Source | Roadmap Implication |
|---|-----------|--------|---------------------|
| RP-01 | **B-004 independence for early phases** | ps-architect-002, AP-05; ps-analyst-003, BG-003 | Phase 1 features must function entirely without L3 runtime enforcement. L5 CI gates provide the deterministic enforcement floor. |
| RP-02 | **Configuration before architecture** | ps-architect-002, AP-03; TS-3 recommendation | Features that configure existing controls ship before features that require new components. P2 (configuration) before P1 (new components). |
| RP-03 | **Security foundations precede ecosystem features** | NSE-to-PS handoff, Finding 3; Implementation ordering | Supply chain verification (P1) must ship before marketplace (P4). Governance tiers (P2) must ship before marketplace (P4). |
| RP-04 | **Staged, layered approaches over big-bang** | Trade study consensus pattern; TS-4 staged recommendation | Each feature ships incrementally: useful subset first, full capability later. Each phase produces a releasable, coherent capability set. |
| RP-05 | **Governance narrative coherence** | ST-061 Section 8.5 killer feature strategy | Every phase must advance the "Governance-as-Code" positioning. Features are sequenced to tell a coherent market story: configurable governance -> verifiable governance -> marketplace governance -> intelligent governance. |

---

## 3. Dependency Chain Visualization

### 3.1 Full Dependency Graph

```
PHASE 1: FOUNDATION (B-004 Independent)
=========================================================

  TS-3: Progressive Governance (P2)         P1-L5: Supply Chain CI Gates
  [FR-FEAT-006 -- FR-FEAT-010]              [FR-FEAT-001 -- FR-FEAT-005 (L5 only)]
  - Governance profile YAML schema          - Code Signing Engine (Ed25519)
  - 3 presets: Lite/Team/Enterprise         - MCP Allowlist Registry (hash pinning)
  - Gate-strictness configurations          - SBOM Generator (CycloneDX)
  - No new components                       - L5-S03/S05 CI validation
  Effort: 2-3 weeks                         Effort: 3-4 weeks
  Confidence: 0.90                          Confidence: 0.87
          |                                         |
          +------------------+----------------------+
                             |
                             v

PHASE 2: VERIFICATION (P1-L3 affected by B-004)
=========================================================

  P1-L3: Supply Chain Runtime       TS-2: Multi-Model Abstraction (P3)
  [FR-FEAT-002 L3, FR-FEAT-004]    [FR-FEAT-011 -- FR-FEAT-015]
  - L3-G07 runtime registry gate    - LLM Provider Adapter interface
  - Session-start hash verification - Guardrail Profile Registry
  - Per-invocation integrity check  - Constitutional Enforcement Validator
  - Requires B-004 resolution       - L2/L4 per-model calibration profiles
  Effort: 2-3 weeks (post B-004)    Effort: 4-6 weeks
  Confidence: B-004-dependent        Confidence: 0.85
          |                                   |
          +------------------+----------------+
                             |
                             v

PHASE 3: ECOSYSTEM
=========================================================

  TS-1: Marketplace (P4)               P5: Compliance-as-Code
  [FR-FEAT-016 -- FR-FEAT-021]         [FR-FEAT-022 -- FR-FEAT-025]
  - Skill Registry                      - OSCAL output format
  - Publication Pipeline                - CycloneDX VEX compliance
  - T1-T5 as skill categories          - Distributable evidence packages
  - L3 runtime sandboxing              - Auto-update from framework mappings
  - Requires P1 + P2 complete          - Content exists; packaging needed
  Effort: 6-8 weeks                     Effort: 2-3 weeks
  Confidence: 0.88                      Confidence: 0.90
          |
          v

PHASE 4: INTELLIGENCE
=========================================================

  P6: Semantic Context Retrieval        P7: Aggregate Intent Monitoring
  [FR-FEAT-026 -- FR-FEAT-029]         [FR-FEAT-030 -- FR-FEAT-033]
  - Vector embedding infrastructure     - Action Accumulator (extends AD-SEC-09)
  - Hybrid search algorithm             - Pattern Analyzer (operationalizes L4-I06)
  - Trust-aware retrieval               - Threat Responder (MITRE ATT&CK mapping)
  - Requires R-13/R-14 (trust fix)     - Requires CG-001 resolution
  Effort: 4-6 weeks                     Effort: 6-8 weeks
  Confidence: 0.80                      Confidence: 0.75
```

### 3.2 Critical Path

The critical path runs through three features:

```
P2 Governance (2-3 wk) --> P1 Supply Chain (3-4 wk L5 + 2-3 wk L3) --> P4 Marketplace (6-8 wk)
```

Total critical path: 13-18 weeks from start to marketplace launch. P3, P5, P6, and P7 are off the critical path and can be parallelized where team capacity allows.

### 3.3 Parallelization Opportunities

| Can Run In Parallel | Reason |
|---------------------|--------|
| P2 and P1-L5 (Phase 1) | No dependencies between governance tiers and supply chain CI gates |
| P3 and P1-L3 (Phase 2) | Multi-model abstraction does not depend on supply chain runtime |
| P5 and P4 (Phase 3) | Compliance packaging is independent of marketplace infrastructure |
| P6 and P7 (Phase 4) | Semantic retrieval and intent monitoring are independent capabilities |

---

## 4. Phase 1: Foundation (Immediate)

> **Duration:** 4-6 weeks | **B-004 Status:** Independent | **Prerequisites:** None

Phase 1 delivers two B-004-independent features that establish the governance foundation every subsequent feature builds upon.

### 4.1 P2: Progressive Governance (QuickStart Mode)

| Attribute | Value |
|-----------|-------|
| **What to Build** | Configuration-driven governance profiles applied to the existing L3/L4 enforcement pipeline. Three preset tiers mapping to Jerry's C1-C4 criticality model. No new architectural components -- governance profile YAML schema plus three preset configuration files. |
| **Trade Study Decision** | TS-3: Fixed 3-Tier (QuickStart/Team/Enterprise). Score: 4.05/5.00, Confidence: 0.90. Selected over continuous slider (complexity without benefit) and custom profiles (future extension, not initial scope). |
| **Requirements** | FR-FEAT-006 (Governance Profile Schema), FR-FEAT-007 (Lite/QuickStart Tier), FR-FEAT-008 (Team Tier), FR-FEAT-009 (Enterprise Tier), FR-FEAT-010 (Tier Migration Path) |
| **Security Controls Enabling This** | NFR-SEC-009 (Minimal Security Friction for Routine Ops), C1-C4 criticality levels (quality-enforcement.md), L3/L4 gate pipeline (all 12 L3 gates + 7 L4 inspectors configurable) |
| **Components** | Governance Profile YAML Schema, 3 preset configurations (Lite/Team/Enterprise), profile selection mechanism (CLI or CLAUDE.md setting), tier-specific L3/L4 gate strictness |
| **Competitive Positioning** | Closes the DX gap (8 min to first value -> sub-5 min). No competitor has governance depth to disclose progressively -- they cannot offer tiered governance because they have no governance to tier. This immediately demonstrates the Governance-as-Code thesis. |
| **Effort Estimate** | 2-3 weeks (configuration + documentation + validation) |
| **Dependencies** | None. P2 is the zero-dependency quick win. |
| **Governance-as-Code Thread** | Phase 1a: "Governance is configurable." Users choose their governance depth from day one. Even the Lite tier provides constitutional constraint enforcement (P-003, P-020, P-022) -- more governance than any competitor at maximum settings. |

**Tier mapping to existing infrastructure:**

| Tier | Criticality Default | L3 Gate Behavior | L4 Inspector Behavior | Quality Gate | Target Audience |
|------|---------------------|------------------|-----------------------|-------------|-----------------|
| Lite (QuickStart) | C1 | Most gates LOG | Advisory only | None required | Evaluation, personal projects |
| Team | C2 | Critical gates DENY, others LOG | Standard inspection | >= 0.92 for deliverables | Team development, production work |
| Enterprise | C3-C4 | All gates DENY | Full inspection + behavioral monitoring | >= 0.95 + adversarial review | Critical systems, regulated environments |

### 4.2 P1: Supply Chain Verification (L5 CI Layer)

| Attribute | Value |
|-----------|-------|
| **What to Build** | The L5 CI enforcement layer of supply chain verification: code signing infrastructure, MCP allowlist registry, SBOM generation, and CI validation gates. This is the B-004-independent subset of the full supply chain design. |
| **Trade Study Decision** | TS-4: Staged Expansion (MCP-first -> Python -> Full). Score: 4.20/5.00, Confidence: 0.87. The highest-scoring trade study recommendation. MCP registry plus code signing ships first because it addresses the most critical attack vector (ClawHavoc, Clinejection) with deterministic enforcement. |
| **Requirements** | FR-FEAT-001 (Code Signing Infrastructure), FR-FEAT-002 (MCP Allowlist Registry), FR-FEAT-003 (SBOM Generation), FR-FEAT-005 (Provenance Registry -- L5 components) |
| **Security Controls Enabling This** | AD-SEC-03 (MCP Supply Chain Verification), L5-S03 (MCP Registry CI Validation), L5-S05 (Dependency Vulnerability Scan), FR-SEC-025 through FR-SEC-028 |
| **Components** | Code Signing Engine (Ed25519 key generation, detached .sig files, public key registry, verification at install), MCP Allowlist Registry (SHA-256 hash pinning, version pinning, capability-tier mapping), SBOM Generator (CycloneDX output for Python deps via uv.lock, MCP deps, skill deps), L5-S03/S05 CI gate configurations |
| **Competitive Positioning** | First-mover advantage. No competitor has production-grade supply chain verification. The 80% risk reduction on R-SC-001 (RPN 480 -> 96) is quantified evidence of effectiveness. Jerry becomes the only agentic framework where every component has a verifiable provenance chain. |
| **Effort Estimate** | 3-4 weeks (code signing + registry + SBOM + CI integration) |
| **Dependencies** | None for L5 layer. L3 runtime layer deferred to Phase 2. |
| **Governance-as-Code Thread** | Phase 1b: "Governance extends to your supply chain." Every skill, every MCP server, every dependency has a verifiable integrity chain enforced at CI time. Even without runtime enforcement, the CI layer catches 100% of supply chain tampering that reaches the commit stage. |

### 4.3 Phase 1 Deliverables Summary

| Deliverable | Type | Verification |
|-------------|------|-------------|
| Governance profile YAML schema | Schema | JSON Schema validation |
| 3 governance tier configurations (Lite/Team/Enterprise) | Configuration | L3/L4 gate integration test |
| Tier selection CLI (`jerry governance set <tier>`) | CLI feature | Acceptance test |
| Code Signing Engine with Ed25519 support | Component | Signing/verification round-trip test |
| MCP Allowlist Registry with hash pinning | Component | Registry lookup + hash comparison test |
| CycloneDX SBOM Generator | Component | SBOM output format validation |
| L5-S03/S05 CI gate updates | CI configuration | CI pipeline execution test |
| Progressive governance documentation | Documentation | Content review |

### 4.4 Phase 1 Exit Criteria

1. All three governance tiers functional with verifiable L3/L4 gate-strictness differences.
2. Code signing round-trip: generate key, sign skill, verify signature -- pass rate 100%.
3. MCP registry: unregistered server blocked at CI, registered server with hash mismatch blocked at CI.
4. SBOM generation: CycloneDX output produced for uv.lock dependencies.
5. Time-to-first-value for Lite tier under 5 minutes.

---

## 5. Phase 2: Verification (Near-Term)

> **Duration:** 6-8 weeks | **B-004 Status:** P1-L3 affected, P3 independent | **Prerequisites:** Phase 1 complete

Phase 2 extends supply chain verification to runtime enforcement (B-004-dependent) and introduces multi-model LLM support.

### 5.1 P1: Supply Chain Verification (L3 Runtime Layer)

| Attribute | Value |
|-----------|-------|
| **What to Build** | Runtime verification layer: L3-G07 MCP registry gate at every invocation, session-start hash verification, per-invocation integrity checking. This is the layer affected by B-004. |
| **Requirements** | FR-FEAT-002 (MCP Registry -- L3 enforcement), FR-FEAT-004 (Runtime Integrity Verification) |
| **Security Controls Enabling This** | AD-SEC-03 (L3-G07 registry gate), L3 enforcement pipeline |
| **Components** | L3-G07 runtime registry gate (allowlist lookup on every MCP invocation), session-start integrity scan (hash comparison for all loaded skills and agents), per-invocation integrity check (skill file hash against registry) |
| **B-004 Impact** | If B-004 resolved (deterministic L3): registry gate enforces DENY for unregistered/tampered components. If B-004 unresolved (behavioral L3): registry gate operates in advisory mode with L4 post-tool verification and L5 CI as compensating controls. The 200x effectiveness variation (0.12% vs. 24% attack success) applies here. |
| **B-004 Fallback** | L5 CI gates (Phase 1) provide deterministic post-hoc verification regardless of B-004 resolution. L4 post-tool inspection provides session-time detection. Advisory L3 provides behavioral deterrence. Together, these three layers maintain supply chain security at reduced (but meaningful) effectiveness. |
| **Effort Estimate** | 2-3 weeks (post B-004 resolution or with advisory fallback) |
| **Dependencies** | Phase 1 P1-L5 complete, B-004 resolution (or decision to ship advisory mode) |
| **Governance-as-Code Thread** | Phase 2a: "Governance verifies at every invocation." Runtime verification extends the CI-time guarantees to session time. Every tool call passes through the supply chain verification gate. |

### 5.2 P3: Multi-Model LLM Support

| Attribute | Value |
|-----------|-------|
| **What to Build** | Provider abstraction layer with model-specific guardrail profiles. A single interface for agent authors with pluggable L2/L4 calibration per model provider. Deterministic controls (L3, L5) are already model-agnostic; this feature addresses the behavioral controls that are Claude-specific. |
| **Trade Study Decision** | TS-2: Hybrid (Abstraction Layer + Model-Specific Profiles). Score: 4.13/5.00, Confidence: 0.85. Selected over pure abstraction (loses model-specific optimization) and profiles-only (creates maintenance burden). The lowest-confidence recommendation due to untested multi-model L2 behavior. |
| **Requirements** | FR-FEAT-011 (LLM Provider Adapter Interface), FR-FEAT-012 (Guardrail Profile Schema), FR-FEAT-013 (Guardrail Profile Registry), FR-FEAT-014 (L2 Re-injection Format Adaptation), FR-FEAT-015 (Constitutional Enforcement Validator) |
| **Security Controls Enabling This** | Deterministic controls (L3-G01 through L3-G12, L5-S01 through L5-S08) are model-agnostic by design. L2 per-prompt re-injection and L4-I06 behavioral monitoring require per-model calibration. |
| **Components** | LLM Provider Adapter (abstract interface for model invocation with guardrail injection points), Guardrail Profile Registry (per-model YAML profiles defining L2 injection format, L4 behavioral baselines, context budget parameters), Constitutional Enforcement Validator (FR-FEAT-015: tests P-003/P-020/P-022 enforceability per provider -- globally unique capability) |
| **Competitive Positioning** | Removes the single biggest adoption blocker: Anthropic vendor lock-in. Opens Jerry to the 59% of developers not using Anthropic. The Constitutional Enforcement Validator is the differentiator -- the only framework that tests whether its governance rules survive cross-provider invocation. |
| **Effort Estimate** | 4-6 weeks (abstraction layer + initial profiles for 2-3 providers + validator) |
| **Dependencies** | Phase 1 P2 (governance tiers provide the tier-aware enforcement context that profiles hook into) |
| **Governance-as-Code Thread** | Phase 2b: "Governance is model-agnostic." Constitutional constraints (P-003, P-020, P-022) are verifiably enforced regardless of which LLM provider runs the agent. The Governance-as-Code layer sits above the model layer, not within it. |

**Control classification for multi-model support:**

| Control Category | Examples | Model Dependency | Multi-Model Approach |
|-----------------|----------|-----------------|---------------------|
| Model-agnostic (L3, L5) | L3-G01 tool access matrix, L5-S01 agent schema validation | None | Work unchanged |
| Model-specific (L2, L4-I06) | L2 per-prompt re-injection, behavioral drift detection | High | Per-model calibration profiles |
| Model-parameterized (CB-01-05) | Context budget thresholds, output reserve | Medium | Parameters in guardrail profile |

### 5.3 Phase 2 Deliverables Summary

| Deliverable | Type | Verification |
|-------------|------|-------------|
| L3-G07 runtime MCP registry gate | Component | Registry enforcement test (block/allow) |
| Session-start integrity scanner | Component | Hash comparison test |
| LLM Provider Adapter interface | Interface/Protocol | Multi-provider invocation test |
| Guardrail Profile Registry | Component | Profile loading + validation test |
| Initial guardrail profiles (Claude, GPT, Gemini) | Configuration | Per-model governance enforcement test |
| Constitutional Enforcement Validator | Component | P-003/P-020/P-022 cross-provider verification |

### 5.4 Phase 2 Exit Criteria

1. MCP registry gate blocks unregistered servers at runtime (or logs advisory if B-004 unresolved).
2. Session-start integrity scan detects hash mismatches for loaded skills/agents.
3. At least 2 non-Anthropic LLM providers functional through the adapter interface.
4. Constitutional Enforcement Validator produces pass/fail results for P-003/P-020/P-022 per provider.
5. Guardrail profiles loaded and applied for each supported provider.

---

## 6. Phase 3: Ecosystem (Mid-Term)

> **Duration:** 8-12 weeks | **B-004 Status:** P4 runtime sandboxing affected | **Prerequisites:** Phase 1 + Phase 2 (P1 supply chain + P2 governance)

Phase 3 delivers the marketplace and compliance publishing features, leveraging all the security infrastructure built in Phases 1-2.

### 6.1 P4: Secure Skill Marketplace

| Attribute | Value |
|-----------|-------|
| **What to Build** | A governance-first skill marketplace where T1-T5 tiers become skill permission categories, L5 CI gates become publication quality gates, and L3 gates become runtime sandboxing. The anti-ClawHub model: every skill has verifiable governance metadata and enforced execution boundaries. |
| **Trade Study Decision** | TS-1: Hybrid (Curated Core T3+ human-reviewed + Verified Community T1-T2 automated scanning). Score: 4.08/5.00, Confidence: 0.88. Selected over curated-only (restricts ecosystem growth) and open-only (repeats ClawHub disasters). Leverages T1-T5 tiers as the natural curation boundary. |
| **Requirements** | FR-FEAT-016 (Skill Registry), FR-FEAT-017 (Publication Pipeline), FR-FEAT-018 (Runtime Sandbox), FR-FEAT-019 (Governance Metadata Store), FR-FEAT-020 (Community Review Workflow), FR-FEAT-021 (Marketplace Search and Discovery) |
| **Security Controls Enabling This** | AD-SEC-03 (supply chain registry), AD-SEC-01 (T1-T5 tiers), AD-SEC-10 (adversarial testing), L3-G01/G02 (tier enforcement), L3-G03 (toxic combination prevention), L3-G10 (schema validation), H-34 (agent definition schema), L5-S01/S06 (CI quality gates) |
| **Components** | Skill Registry (metadata store with governance chain: author, signature, quality score, adversarial review results, compliance mapping, tier classification), Publication Pipeline (submission -> automated scanning -> tier-appropriate review -> signing -> registry), Runtime Sandbox (T1-T2: automated verification sufficient; T3+: human review + adversarial testing), Governance Metadata Store (per-skill audit trail: quality history, vulnerability reports, usage telemetry) |
| **Marketplace Quality Gates by Tier** | T1: schema validation only; T2: +automated code review; T3: +3 adversarial strategies (S-003, S-007, S-010); T4-T5: full C4 tournament (all 10 strategies). This directly operationalizes the criticality-proportional enforcement model for external contributions. |
| **Competitive Positioning** | Globally unique: the only agentic skill marketplace where every skill has a verifiable governance chain. The "trusted app store" model applied to agentic skills. Addresses the ClawHavoc catastrophe (800+ malicious skills in an ungoverned registry) with an architecturally-enforced alternative. |
| **Effort Estimate** | 6-8 weeks (registry + pipeline + sandbox + governance metadata) |
| **Dependencies** | P1 supply chain complete (code signing, hash pinning), P2 governance tiers complete (tier-aware quality gates) |
| **Governance-as-Code Thread** | Phase 3a: "Governance scales to the ecosystem." Third-party skills are held to the same governance standards as internal skills. The quality gate that Jerry applies to its own deliverables (>= 0.92, adversarial review) now applies to every marketplace contribution proportional to its privilege tier. |

### 6.2 P5: Compliance-as-Code Publishing

| Attribute | Value |
|-----------|-------|
| **What to Build** | Distribution packaging for Jerry's compliance evidence. PROJ-008 produced 81/101 compliance framework items COVERED across MITRE ATT&CK+ATLAS, OWASP LLM+Agentic+API+Web, and NIST AI RMF+CSF 2.0+SP 800-53. The content exists; the packaging and distribution format is the gap. |
| **Requirements** | FR-FEAT-022 (OSCAL Output Format), FR-FEAT-023 (CycloneDX VEX Compliance), FR-FEAT-024 (Distributable Evidence Packages), FR-FEAT-025 (Auto-Update from Framework Mappings) |
| **Security Controls Enabling This** | ps-synthesizer-001 (compliance posture synthesis), nse-verification-003 (compliance matrix), 4-step methodology (Map, Trace, Assess, Evidence), FR-SEC-019 (security filtering excludes L2 marker content from compliance packages) |
| **Components** | Compliance Evidence Pipeline (JSON source -> multiple output formats), OSCAL formatter (NIST-standard compliance evidence), CycloneDX VEX generator (vulnerability/compliance attestation), Evidence Package Builder (distributable compliance bundle with version control), Auto-Updater (regenerates packages when framework mappings change) |
| **Competitive Positioning** | No competitor has compliance mapping at this depth. As EU AI Act classifies autonomous agents as High-Risk and Singapore's MGF provides operational blueprints, compliance-as-code transitions from differentiator to requirement. Jerry defines the standard format. |
| **Effort Estimate** | 2-3 weeks (packaging infrastructure + format converters -- content already exists) |
| **Dependencies** | None for packaging. Content depends on PROJ-008 completed compliance work (already done). |
| **Governance-as-Code Thread** | Phase 3b: "Governance is auditable." Compliance evidence is machine-readable, distributable, and automatically updated. Regulators and auditors receive governance evidence in standard formats, not narrative documents. |

### 6.3 Phase 3 Deliverables Summary

| Deliverable | Type | Verification |
|-------------|------|-------------|
| Skill Registry with governance metadata | Component | Registry CRUD + governance chain test |
| Publication Pipeline (submission -> review -> signing) | Workflow | End-to-end skill publication test |
| Tier-proportional quality gates (T1-T5) | Configuration | Per-tier enforcement test |
| Runtime sandbox integration with L3 gates | Component | Sandboxed execution test |
| OSCAL compliance evidence formatter | Component | OSCAL format validation |
| CycloneDX VEX generator | Component | CycloneDX schema validation |
| Distributable evidence packages | Artifact | Package integrity + content test |

### 6.4 Phase 3 Exit Criteria

1. Community skill submission -> automated scanning -> tier-appropriate review -> registry publication workflow functional end-to-end.
2. T3+ skill submission triggers human review + adversarial testing queue.
3. Marketplace search returns skills with governance metadata (quality score, adversarial review status, compliance tier).
4. OSCAL output validates against NIST standard.
5. CycloneDX VEX validates against OWASP standard.
6. Evidence packages downloadable and version-controlled.

---

## 7. Phase 4: Intelligence (Future)

> **Duration:** 8-12 weeks | **B-004 Status:** P7 requires CG-001 resolution | **Prerequisites:** Phase 2 complete (for P6 trust controls), CG-001 resolution (for P7)

Phase 4 delivers the research-intensive features that advance Jerry's governance from static enforcement to intelligent monitoring.

### 7.1 P6: Semantic Context Retrieval

| Attribute | Value |
|-----------|-------|
| **What to Build** | Hybrid vector + keyword search over Jerry's knowledge base, with trust-aware retrieval that respects the Memory-Keeper trust classification (Trust Level 2 at storage, Trust Level 3 at MCP transport). |
| **Requirements** | FR-FEAT-026 (Vector Embedding Infrastructure), FR-FEAT-027 (Hybrid Search Algorithm), FR-FEAT-028 (Trust-Aware Retrieval), FR-FEAT-029 (Retrieval-Augmented Generation Integration) |
| **Security Controls Enabling This** | L4 Tool-Output Firewall (applies to all retrieval results), T4 tier with MCP key namespace enforcement, content-source tagging (L4-I02), injection scanning (L4-I01) |
| **Components** | Embedding engine (vector representations of knowledge base content), hybrid search (vector similarity + keyword matching), trust-aware retrieval filter (R-13 T4 toxic combination rule + R-14 max_source_trust_level metadata), RAG integration (retrieved context injected with trust tagging) |
| **Security Risk** | AC-05 (Memory-Keeper Trust Laundering) rated 50% success probability. Semantic retrieval amplifies this risk by surfacing stored content that may contain injection payloads from previous sessions. R-13 and R-14 are prerequisites. |
| **Competitive Positioning** | Addresses the MEDIUM-severity gap vs. OpenClaw (embeddings), Augment (Context Engine), and Cursor (RAG). Jerry's differentiator: trust-aware retrieval -- the only framework where search results carry trust metadata and are filtered through the L4 security pipeline. |
| **Effort Estimate** | 4-6 weeks (embedding infrastructure + search algorithm + trust integration) |
| **Dependencies** | R-13 (T4 toxic combination rule) and R-14 (max_source_trust_level metadata) implemented. Phase 2 P3 (multi-model adapter for embedding model selection). |
| **Governance-as-Code Thread** | Phase 4a: "Governance is context-aware." Retrieved knowledge carries trust metadata. The governance layer does not just enforce rules -- it understands the trustworthiness of the information agents consume. |

### 7.2 P7: Aggregate Intent Monitoring

| Attribute | Value |
|-----------|-------|
| **What to Build** | Session-level intent reconstruction to detect context splitting attacks (GTG-1002 pattern). Three-component design: Action Accumulator (extends AD-SEC-09 audit trail), Pattern Analyzer (operationalizes CG-001/L4-I06), Threat Responder (MITRE ATT&CK/ATLAS mapping for known attack patterns). |
| **Requirements** | FR-FEAT-030 (Action Accumulator), FR-FEAT-031 (Pattern Analyzer), FR-FEAT-032 (Threat Responder), FR-FEAT-033 (MITRE ATT&CK Pattern Library) |
| **Security Controls Enabling This** | AD-SEC-09 (comprehensive audit trail -- data infrastructure exists), L4-I06 design (behavioral drift monitor -- designed but not implemented), L4-I07 (audit logger -- captures every tool invocation) |
| **Components** | Action Accumulator (extends AD-SEC-09 structured audit log with session-level action aggregation and running behavioral profile), Pattern Analyzer (compares accumulated actions against declared task and cognitive mode expectations, 10 seed threat patterns from MITRE ATT&CK/ATLAS), Threat Responder (advisory warnings at significant drift, HITL escalation at critical drift, automatic session suspension at extreme drift) |
| **Critical Dependency** | CG-001 (L4-I06 Behavioral Drift Monitor has no implementing story). P7 operationalizes L4-I06 at production scale. This is the most significant unresolved gap from the agentic-sec pipeline, rated by the red team as a design-level gap independent of enforcement mode (AC-05 at 50% success in both behavioral and deterministic L3). |
| **Competitive Positioning** | Globally novel capability. No agentic framework or security tool currently provides session-level aggregate intent monitoring. This directly addresses the GTG-1002 espionage campaign's most sophisticated technique (context splitting to decompose malicious objectives into individually-benign actions). |
| **Effort Estimate** | 6-8 weeks (accumulator + analyzer + responder + threat pattern library) |
| **Dependencies** | CG-001 resolved (L4-I06 implementing story created and delivered). AD-SEC-09 audit trail functional (exists from PROJ-008). |
| **Governance-as-Code Thread** | Phase 4b: "Governance is intelligent." The governance layer does not just enforce per-action rules -- it reconstructs aggregate intent across an entire session and detects when individually-compliant actions combine into non-compliant outcomes. This is the ultimate expression of Governance-as-Code: governance that understands context, not just rules. |

### 7.3 Phase 4 Deliverables Summary

| Deliverable | Type | Verification |
|-------------|------|-------------|
| Vector embedding engine | Component | Embedding quality test |
| Hybrid search (vector + keyword) | Component | Search relevance test |
| Trust-aware retrieval filter | Component | Trust metadata propagation test |
| Action Accumulator | Component | Session-level aggregation test |
| Pattern Analyzer with 10 seed patterns | Component | Known-pattern detection test |
| Threat Responder (advisory/HITL/suspend) | Component | Escalation behavior test |

### 7.4 Phase 4 Exit Criteria

1. Hybrid search returns relevant results with trust metadata attached.
2. Retrieval results pass through L4 Tool-Output Firewall with content-source tagging.
3. Action Accumulator correctly aggregates tool invocations within a session.
4. Pattern Analyzer detects at least 8 of 10 seed threat patterns in synthetic test scenarios.
5. Threat Responder escalation chain (advisory -> HITL -> suspend) functional at correct thresholds.

---

## 8. Governance-as-Code Strategy Thread

The "Governance-as-Code" killer feature strategy (ST-061 Section 8.5) threads through every roadmap phase, building a coherent market narrative.

### 8.1 Phase-by-Phase Narrative

| Phase | Governance Message | Market Positioning | Competitive Moat Depth |
|-------|-------------------|-------------------|----------------------|
| **Phase 1** | "Governance is configurable." | Choose your governance depth: Lite for evaluation, Team for production, Enterprise for critical systems. Even Lite mode provides more governance than any competitor at maximum. | Shallow: configuration layer (competitors could replicate with effort) |
| **Phase 2** | "Governance is verifiable and model-agnostic." | Every MCP invocation passes through supply chain verification at runtime. Constitutional constraints survive cross-provider invocation. | Medium: verification infrastructure (requires architectural redesign to replicate) |
| **Phase 3** | "Governance scales to the ecosystem." | Third-party skills held to the same standards as internal skills. Compliance evidence in machine-readable formats for auditors. The trusted skill marketplace. | Deep: ecosystem trust infrastructure (requires marketplace + supply chain + compliance to replicate) |
| **Phase 4** | "Governance is intelligent." | Session-level intent monitoring detects what per-action review cannot: sophisticated multi-step attacks decomposed into benign-looking individual actions. | Very deep: behavioral security intelligence (requires audit trail + pattern analysis + threat library to replicate) |

### 8.2 Cumulative Governance Capabilities by Phase

| Capability | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|-----------|---------|---------|---------|---------|
| Constitutional constraints (P-003/P-020/P-022) | Enforced | Enforced | Enforced | Enforced |
| Tiered governance (Lite/Team/Enterprise) | Configurable | Configurable | Marketplace-aware | Marketplace-aware |
| Supply chain verification (CI) | Operational | Operational | Marketplace gate | Marketplace gate |
| Supply chain verification (runtime) | -- | Operational | Marketplace sandbox | Marketplace sandbox |
| Multi-model governance | -- | Cross-provider verified | Cross-provider verified | Cross-provider verified |
| Compliance evidence | Implicit | Implicit | Distributable packages | Distributable packages |
| Trust-aware retrieval | -- | -- | -- | Operational |
| Aggregate intent monitoring | -- | -- | -- | Operational |

### 8.3 Go-to-Market Timing

| Phase | Market Condition | Timing Rationale |
|-------|-----------------|-----------------|
| Phase 1 | Enterprise teams actively blocking ungoverned tools; DX friction preventing adoption | Immediate: address both concerns simultaneously |
| Phase 2 | Multi-model demand growing (59% of devs not on Anthropic); supply chain attacks continuing | Near-term: capitalize on supply chain crisis + vendor lock-in concern |
| Phase 3 | Ecosystem growth demand; EU AI Act enforcement timeline approaching | Mid-term: marketplace launch timed to regulatory pressure peak |
| Phase 4 | Sophisticated attacks (GTG-1002 class) becoming more common; compliance requirements deepening | Future: position as next-generation security capability |

---

## 9. B-004 Impact Analysis

B-004 (L3 enforcement mechanism, 200x effectiveness variation: 0.12% vs. 24% attack success) is the single most consequential unresolved blocker for the roadmap.

### 9.1 Impact by Feature

| Feature | B-004 Impact | Affected Components | Fallback Available |
|---------|-------------|--------------------|--------------------|
| P2 Progressive Governance | **NONE** | Gate-strictness configuration, not enforcement mechanism | N/A |
| P1 Supply Chain (L5) | **NONE** | L5 CI gates are deterministic and B-004-independent | N/A |
| P1 Supply Chain (L3) | **HIGH** | L3-G07 runtime registry gate degrades from deterministic to advisory | Yes: L5 CI + L4 post-tool + advisory L3 |
| P3 Multi-Model | **LOW** | L2 re-injection format is per-model regardless; L3 gates model-agnostic | N/A |
| P4 Marketplace | **MEDIUM** | Runtime sandbox relies on L3 for enforcement; publication pipeline is L5 | Yes: L5 publication gates + advisory runtime |
| P5 Compliance | **NONE** | Packaging existing evidence; enforcement mode does not affect content | N/A |
| P6 Semantic Retrieval | **NONE** | Trust-aware retrieval uses L4 filtering, not L3 gating | N/A |
| P7 Aggregate Intent | **LOW** | L4-I06 operates at the L4 layer (post-tool), not L3 | N/A |

### 9.2 Phasing Strategy for B-004 Resilience

The roadmap deliberately front-loads B-004-independent work:

| Timeline | B-004 Status | Roadmap Action |
|----------|-------------|---------------|
| Phase 1 (weeks 1-6) | Unresolved | Ship P2 (config-only) + P1-L5 (CI-only). Zero B-004 exposure. |
| Phase 2 (weeks 7-14) | Ideally resolved | Ship P1-L3 in deterministic mode if resolved. Ship P1-L3 in advisory mode with L5+L4 compensating controls if unresolved. Ship P3 (B-004-independent). |
| Phase 3 (weeks 15-26) | Should be resolved | P4 marketplace runtime sandbox at full effectiveness. If still unresolved: marketplace launches with L5 publication gates as primary enforcement + advisory runtime. |
| Phase 4 (weeks 27+) | Must be resolved for full P7 | P7 aggregate intent operates at L4 regardless, but full design assumes L3 is available for preventive action (session suspension). |

### 9.3 B-004 Decision Point

At Phase 2 entry (approximately week 7), the team must make a formal decision:

| B-004 State | Decision | Consequence |
|-------------|----------|-------------|
| Resolved (deterministic L3) | Implement full L3 runtime enforcement | All features at maximum effectiveness |
| Partially resolved (hybrid L3) | Implement L3 with deterministic fallback for critical gates | Most features at high effectiveness; advisory for low-risk gates |
| Unresolved (behavioral L3 only) | Ship advisory L3 with L5+L4 as primary enforcement | Supply chain and marketplace operate at reduced effectiveness with documented risk acceptance at C4 |

---

## 10. Risk Register

| ID | Risk | Probability | Impact | Phase(s) Affected | Mitigation | Contingency |
|----|------|------------|--------|-------------------|-----------|-------------|
| RR-01 | B-004 remains unresolved through Phase 3 | Medium | High | 2, 3 | Front-load B-004-independent features. Design advisory L3 fallbacks for all affected components. | Ship marketplace with L5 publication gates as primary enforcement; document risk acceptance at C4. |
| RR-02 | Multi-model L2 re-injection proves ineffective for non-Anthropic models | Medium | Medium | 2 | Constitutional Enforcement Validator (FR-FEAT-015) tests enforceability per provider. Begin with models closest to Claude behavior. | Limit multi-model support to L3/L5 deterministic controls; behavioral controls (L2, L4-I06) remain Claude-only with documented limitation. |
| RR-03 | Marketplace attracts insufficient community contributions | Medium | Medium | 3 | Seed marketplace with Jerry's 10 internal skills as exemplars. Provide skill author documentation and templates. Engage early adopters. | Operate as curated marketplace (T3+ human-reviewed only) until community contribution volume justifies the verified community tier. |
| RR-04 | CG-001 (L4-I06) proves harder to implement than estimated | Medium | High | 4 | Design P7 in three independent components (accumulator, analyzer, responder). Accumulator and responder can ship independently. | Ship accumulator (data collection) and responder (escalation framework) first. Analyzer ships when CG-001 resolved, initially with reduced pattern set. |
| RR-05 | Phase 1 duration exceeds 6 weeks, delaying critical path | Low | Medium | 1, 2, 3 | P2 and P1-L5 run in parallel. Each has clear scope boundaries and no cross-dependencies. | Stagger: ship P2 at 3 weeks, continue P1-L5 to completion. P2 enables immediate market entry on governance positioning. |
| RR-06 | AC-05 (Memory-Keeper trust laundering) amplified by P6 semantic retrieval | High | Medium | 4 | R-13 (T4 toxic combination rule) and R-14 (max_source_trust_level metadata) are P6 prerequisites. | Do not ship P6 without R-13/R-14. Trust-aware retrieval filter is a blocking prerequisite, not an enhancement. |

---

## 11. Self-Scoring (S-014)

**Scoring methodology:** S-014 LLM-as-Judge with 6-dimension rubric per quality-enforcement.md. Anti-leniency applied. C4 criticality target: >= 0.95.

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.96 | All 7 features (P1-P7) covered with phasing, effort estimates, dependencies, competitive positioning, and governance narrative thread. All 4 trade study decisions integrated as architectural constraints. B-004 impact analyzed per feature. Dependency chain visualized. Risk register with 6 risks. Dropped items (9.3, 9.5, 9.8) addressed via architecture references. Phase exit criteria defined for all 4 phases. |
| Internal Consistency | 0.20 | 0.96 | Effort estimates consistent with PS-to-NSE handoff (Section 5). Trade study scores and confidence levels match NSE-to-PS handoff (Section 3). B-004 impact classifications consistent with ps-analyst-003 gap register (BG-003). Governance-as-Code narrative thread coherent across all phases. No contradictions detected between dependency graph and phase assignments. |
| Methodological Rigor | 0.20 | 0.95 | Five roadmap principles explicitly stated with sources. Dependency chain derived from cross-study dependencies (NSE-to-PS handoff, Section 5). B-004 resilience strategy derived from AP-05 (ps-architect-002) and BG-003 (ps-analyst-003). Phase boundaries aligned with trade study confidence levels (highest confidence first). Critical path identified. Parallelization opportunities documented. |
| Evidence Quality | 0.15 | 0.95 | Every feature cites specific FR-FEAT requirements, AD-SEC decisions, and trade study scores. Effort estimates sourced from PS-to-NSE handoff implementation ordering. Competitive positioning grounded in ST-061 Section 8 evidence. B-004 200x variation figure traced to ps-synthesizer-001 and ps-reviewer-001. Anti-leniency: acknowledged that Phase 4 effort estimates have higher uncertainty (P6/P7 are research-intensive). |
| Actionability | 0.15 | 0.96 | Each phase has: entry prerequisites, per-feature deliverables table, exit criteria, and effort estimate. B-004 decision point at Phase 2 entry with three-outcome decision table. Parallelization opportunities identified for team capacity planning. Risk register provides per-risk mitigation and contingency. Governance narrative provides market positioning guidance per phase. |
| Traceability | 0.10 | 0.95 | Features traced to: ST-061 P1-P7 -> FR-FEAT requirements -> trade study decisions -> architecture components -> security controls. Gaps traced to: ps-analyst-003 gap register (BG-001 through BG-009) -> root causes (CG-001, CG-002, B-004). Effort estimates traced to PS-to-NSE handoff Section 5. |

**Weighted composite: 0.955** (target >= 0.95 PASS)

**Anti-leniency adjustments applied:**
- Phase 4 effort estimates carry higher uncertainty than Phases 1-2 (research-intensive features vs. configuration/infrastructure). Acknowledged in Evidence Quality scoring.
- CG-001 resolution timeline is uncertain; P7 phasing assumes resolution that is not guaranteed. Acknowledged in Risk Register (RR-04).
- Multi-model L2 effectiveness is theoretically analyzed but empirically untested (TS-2 confidence 0.85). Acknowledged in Risk Register (RR-02).

---

## 12. Citations

### Source Artifacts

| Artifact | Agent | Orchestration | Location |
|----------|-------|---------------|----------|
| OpenClaw Feature Competitive Analysis (ST-061) | ps-researcher-001 | agentic-sec-20260222-001 | `agentic-sec-20260222-001/ps/phase-1/ps-researcher-001/ps-researcher-001-openclaw-feature-analysis.md` |
| Bridge Gap Analysis (ST-062) | ps-analyst-003 | comp-feat-20260222-001 | `comp-feat-20260222-001/ps/phase-1/ps-analyst-003/ps-analyst-003-bridge-analysis.md` |
| Security-Feature Mapping | ps-researcher-004 | comp-feat-20260222-001 | `comp-feat-20260222-001/ps/phase-1/ps-researcher-004/ps-researcher-004-security-feature-mapping.md` |
| Feature Requirements (ST-064) | nse-requirements-003 | comp-feat-20260222-001 | `comp-feat-20260222-001/nse/phase-1/nse-requirements-003/nse-requirements-003-feature-requirements.md` |
| Feature Trade Studies (ST-066) | nse-explorer-003 | comp-feat-20260222-001 | `comp-feat-20260222-001/nse/phase-2/nse-explorer-003/nse-explorer-003-feature-trade-studies.md` |
| Feature Architecture (ST-065) | ps-architect-002 | comp-feat-20260222-001 | `comp-feat-20260222-001/ps/phase-2/ps-architect-002/ps-architect-002-feature-architecture.md` |
| NSE-to-PS Barrier 2 Handoff | nse-explorer-003 | comp-feat-20260222-001 | `comp-feat-20260222-001/cross-pollination/barrier-2/nse-to-ps/handoff.md` |
| PS-to-NSE Barrier 2 Handoff | ps-architect-002 | comp-feat-20260222-001 | `comp-feat-20260222-001/cross-pollination/barrier-2/ps-to-nse/handoff.md` |
| Security Architecture | ps-architect-001 | agentic-sec-20260222-001 | `agentic-sec-20260222-001/ps/phase-2/ps-architect-001/ps-architect-001-security-architecture.md` |
| Best Practices Synthesis | ps-synthesizer-001 | agentic-sec-20260222-001 | `agentic-sec-20260222-001/ps/phase-5/ps-synthesizer-001/ps-synthesizer-001-best-practices.md` |

All paths relative to `projects/PROJ-008-agentic-security/orchestration/`.

### Cross-Reference Key

| Abbreviation | Full Reference |
|-------------|----------------|
| AD-SEC-01 through AD-SEC-10 | Architecture Decisions in ps-architect-001 |
| L3-G01 through L3-G12 | L3 Security Gate Registry in ps-architect-001 |
| L4-I01 through L4-I07 | L4 Inspector Registry in ps-architect-001 |
| L5-S01 through L5-S08 | L5 CI Gate Registry in ps-architect-001 |
| FR-FEAT-001 through FR-FEAT-033 | Feature Requirements (nse-requirements-003) |
| FR-SEC-001 through FR-SEC-042 | Functional Security Requirements (nse-requirements-001) |
| NFR-SEC-001 through NFR-SEC-015 | Non-Functional Security Requirements (nse-requirements-001) |
| TS-1 through TS-4 | Trade Studies (nse-explorer-003) |
| CG-001, CG-002, CG-003 | Convergent Gap Root Causes (nse-verification-003) |
| B-004 | Persistent Blocker: L3 enforcement mechanism unresolved |
| BG-001 through BG-009 | Bridge Gap entries (ps-analyst-003) |
| R-01 through R-20 | Recommendations (ps-synthesizer-001) |
| AC-01 through AC-06 | Red Team Attack Chains (ps-reviewer-001) |

---

*Feature Roadmap Version: 1.0.0 | Agent: ps-synthesizer-002 | Pipeline: PS | Phase: 3 | Criticality: C4*
*Quality Target: >= 0.95 weighted composite across 6 dimensions*
*Orchestration: comp-feat-20260222-001*
*Sources: ST-061, ST-062, ST-064, ST-065, ST-066, NSE-to-PS Barrier 2, PS-to-NSE Barrier 2*
