# TASK-001: Formal Requirements for Hook-Based Enforcement

<!--
DOCUMENT-ID: FEAT-005:EN-403:TASK-001
TEMPLATE: Requirements Specification
VERSION: 1.1.0
AGENT: nse-requirements (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-403 (Hook-Based Enforcement Implementation)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
METHODOLOGY: NASA NPR 7123.1D (Requirements Engineering)
CONSUMERS: TASK-002 (UserPromptSubmit design), TASK-003 (PreToolUse design), TASK-004 (SessionStart design), TASK-005/006/007 (implementation), TASK-011 (verification)
-->

> **Version:** 1.1.0
> **Agent:** nse-requirements (Claude Opus 4.6)
> **Status:** COMPLETE
> **Created:** 2026-02-13
> **Methodology:** NASA NPR 7123.1D Section 6.1 (Technical Requirements Definition)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose and Scope](#purpose-and-scope) | Why this requirements document exists and what it covers |
| [Source Traceability](#source-traceability) | Mapping of authoritative inputs to requirements |
| [Requirements by Hook Type](#requirements-by-hook-type) | Formal shall-statements organized by hook |
| [Cross-Cutting Requirements](#cross-cutting-requirements) | Requirements applying to all hooks |
| [Adversarial Strategy Integration Requirements](#adversarial-strategy-integration-requirements) | Requirements for strategy enforcement touchpoints |
| [Decision Criticality Requirements](#decision-criticality-requirements) | Requirements for C1-C4 escalation |
| [Requirements Traceability Matrix](#requirements-traceability-matrix) | Full traceability from requirement to source and verification |
| [Verification Methods](#verification-methods) | How each requirement will be verified |
| [References](#references) | All source documents |

---

## Purpose and Scope

This document formalizes the requirements for hook-based enforcement mechanisms in the Jerry quality framework. Requirements are derived from three authoritative sources:

1. **ADR-EPIC002-002** (ACCEPTED) -- 5-layer hybrid enforcement architecture with hook layer assignments (L2, L3, L4)
2. **Barrier-1 ADV-to-ENF Handoff** -- Adversarial strategy enforcement touchpoints and quality gate integration
3. **EN-403 Enabler Definition** -- Functional requirements FR-001 through FR-012 and non-functional requirements NFR-001 through NFR-008

All requirements follow NASA NPR 7123.1D requirements engineering principles:
- Each requirement is uniquely identified (REQ-403-NNN)
- Each requirement is necessary, traceable, verifiable, and unambiguous
- Each requirement uses "shall" for mandatory, "should" for recommended, "may" for optional
- Each requirement has a defined verification method

### Scope Boundaries

**In scope:**
- UserPromptSubmit hook (L2 enforcement layer)
- PreToolUse hook (L3 enforcement layer)
- SessionStart hook (L1 enhancement)
- Cross-cutting concerns (fail-safe, portability, token budget, architecture compliance)

**Out of scope:**
- PostToolUse hook (L4) -- deferred to Phase 5 per ADR-EPIC002-002 Implementation Roadmap
- Stop hook (subagent) -- existing implementation adequate for current needs
- Pre-commit hooks (V-044) -- covered by EN-402 TASK-006 execution plans
- CI pipeline (V-045) -- covered by EN-402 TASK-006 execution plans

---

## Source Traceability

### Authoritative Source Documents

| Source ID | Document | Location | Content Used |
|-----------|----------|----------|-------------|
| SRC-001 | ADR-EPIC002-002 | `EN-402-enforcement-priority-analysis/TASK-005-enforcement-ADR.md` | 5-layer architecture, vector assignments, token budgets, defense-in-depth chain |
| SRC-002 | Barrier-1 ADV-to-ENF Handoff | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/adv-to-enf/barrier-1-adv-to-enf-handoff.md` | Strategy-to-hook touchpoints, quality gate integration, decision criticality escalation |
| SRC-003 | EN-403 Enabler Definition | `EN-403-hook-based-enforcement/EN-403-hook-based-enforcement.md` | FR-001 through FR-012, NFR-001 through NFR-008 |
| SRC-004 | EN-402 TASK-006 Execution Plans | `EN-402-enforcement-priority-analysis/TASK-006-execution-plans.md` | V-038 AST boundary validator architecture, code structure |
| SRC-005 | Existing PreToolUse Hook | `scripts/pre_tool_use.py` | Current implementation patterns, error handling |
| SRC-006 | Existing SessionStart Hook | `scripts/session_start_hook.py` | Current implementation patterns, output format |
| SRC-007 | hooks.json | `hooks/hooks.json` | Hook registration and routing configuration |
| SRC-008 | Architecture Standards | `.context/rules/architecture-standards.md` | Hexagonal architecture, layer dependencies |

### FR/NFR to Requirement Mapping

| EN-403 ID | Requirement Text (Summary) | Derived REQ-403 IDs |
|-----------|---------------------------|---------------------|
| FR-001 | UserPromptSubmit delivers V-024 on every prompt | REQ-403-010, REQ-403-011 |
| FR-002 | V-024 includes quality gate, constitution, self-review | REQ-403-012, REQ-403-013, REQ-403-014 |
| FR-003 | V-024 content shall not exceed ~600 tokens | REQ-403-015 |
| FR-004 | PreToolUse triggers AST validation before writes | REQ-403-030, REQ-403-031 |
| FR-005 | PreToolUse verifies constitutional compliance | REQ-403-032 |
| FR-006 | SessionStart injects quality gate and constitution | REQ-403-050, REQ-403-051 |
| FR-007 | All hooks fail-safe | REQ-403-070, REQ-403-071 |
| FR-008 | UserPromptSubmit injects S-014 scoring when deliverable expected | REQ-403-016 |
| FR-009 | UserPromptSubmit includes leniency bias calibration | REQ-403-017 |
| FR-010 | PreToolUse is deterministic and context-rot-immune | REQ-403-033 |
| FR-011 | Hexagonal architecture compliance | REQ-403-080 |
| FR-012 | Decision criticality escalation for governance files | REQ-403-060, REQ-403-061 |

---

## Requirements by Hook Type

### UserPromptSubmit Hook (L2: Per-Prompt Reinforcement)

**Purpose:** Deliver V-024 context reinforcement to counteract L1 context rot. Primary mechanism for re-injecting critical rules, quality gate thresholds, and adversarial strategy reminders into the LLM context on every user prompt.

**Delivery vector:** V-005 (UserPromptSubmit Hook) delivering V-024 (Context Reinforcement via Repetition)

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-010 | The UserPromptSubmit hook SHALL inject V-024 context reinforcement content into the LLM context on every user prompt submission. | HARD | SRC-001 (ADR L2 layer); SRC-003 (FR-001) | V-024 is the primary L1 context rot countermeasure. It must fire on every prompt to maintain the IMMUNE-by-design property (SRC-001, "Key architectural property"). |
| REQ-403-011 | The UserPromptSubmit hook SHALL use the `additionalContext` field of the hook JSON output to inject reinforcement content. | HARD | SRC-006 (existing pattern); SRC-007 (hooks.json) | The `additionalContext` field is the Claude Code-supported mechanism for injecting context into the LLM's context window, as demonstrated by the existing SessionStart hook (SRC-006, `output_json` function). |
| REQ-403-012 | The V-024 reinforcement content SHALL include the quality gate threshold value of >= 0.92. | HARD | SRC-002 (Quality Gate Integration); SRC-003 (FR-002) | The 0.92 threshold is the central quality requirement for EPIC-002. It must be present in every reinforcement injection to counteract context rot of the threshold value (SRC-002, "The 0.92 Threshold" section). |
| REQ-403-013 | The V-024 reinforcement content SHALL include a reminder of applicable constitutional principles from `docs/governance/JERRY_CONSTITUTION.md`. | HARD | SRC-002 (S-007 touchpoint); SRC-003 (FR-002) | S-007 (Constitutional AI) requires principle-by-principle evaluation. The constitution reference must be refreshed on every prompt to counteract degradation (SRC-002, "Enforcement Touchpoints" UserPromptSubmit S-007: "Always"). |
| REQ-403-014 | The V-024 reinforcement content SHALL include a self-review reminder. | HARD | SRC-002 (S-010 touchpoint); SRC-003 (FR-002) | S-010 (Self-Refine) is triggered "Always" per SRC-002 UserPromptSubmit touchpoints. Self-review is the baseline quality mechanism (L0, SRC-002 "Strategy Composition" table). |
| REQ-403-015 | The V-024 reinforcement content SHALL NOT exceed 600 tokens per prompt submission. | HARD | SRC-001 (Token Budget); SRC-003 (FR-003, NFR-001) | ADR-EPIC002-002 allocates exactly 600 tokens to V-024 in the standard enforcement budget (SRC-001, "Standard Enforcement Budget" table). **Clarification (v1.1.0):** The 600-token budget is per-injection (per prompt), not cumulative across the session. Each UserPromptSubmit invocation independently generates content within this budget. The ADR's "Standard Enforcement Budget" column lists per-injection costs for all layers. |
| REQ-403-016 | The UserPromptSubmit hook SHALL inject S-014 (LLM-as-Judge) scoring requirements when the current task context indicates a deliverable is expected. | MEDIUM | SRC-002 (S-014 touchpoint); SRC-003 (FR-008) | S-014 is the scoring backbone for the 0.92 quality gate (SRC-002, "S-014 as the Scoring Backbone"). Trigger condition: "When deliverable expected" (SRC-002, Enforcement Touchpoints). |
| REQ-403-017 | The V-024 reinforcement content SHALL include a leniency bias calibration reminder for S-014 scoring. | MEDIUM | SRC-002 (Quality Gate Integration, R-014-FN); SRC-003 (FR-009) | S-014 has a known leniency bias (R-014-FN, Score=12, SRC-002). Without calibration reminders, quality scores will systematically exceed actual quality (SRC-003 "Leniency bias warning"). |
| REQ-403-018 | The UserPromptSubmit hook SHALL inject S-003 (Steelman) reminders when the current task context indicates a review or critique is expected. | MEDIUM | SRC-002 (S-003 touchpoint) | S-003 ensures fair evaluation by requiring charitable reconstruction before critique. Trigger condition: "When review/critique expected" (SRC-002, Enforcement Touchpoints UserPromptSubmit). |
| REQ-403-019 | The UserPromptSubmit hook output SHALL conform to the Claude Code hook JSON schema with `hookSpecificOutput.additionalContext` for context injection. | HARD | SRC-006 (existing pattern); SRC-007 | Conformance to the Claude Code hook protocol is required for the hook to function. The existing SessionStart hook (SRC-006) establishes the output format precedent. |

### PreToolUse Hook (L3: Pre-Action Gating)

**Purpose:** Deterministically block non-compliant tool operations before execution. Context-rot-immune enforcement through external Python process execution with zero token cost.

**Delivery vectors:** V-001 (PreToolUse Blocking), V-038 (AST Import Boundary Validation)

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-030 | The PreToolUse hook SHALL trigger AST import boundary validation (V-038) before Write and Edit tool operations targeting Python files in `src/`. | HARD | SRC-001 (L3 layer, V-038); SRC-003 (FR-004); SRC-004 (V-038 execution plan) | V-038 has the highest WCS in the 62-vector catalog (4.92). AST validation must run before file writes to prevent architecture violations from being written (SRC-001, "prevent, then detect, then verify" principle). |
| REQ-403-031 | The PreToolUse AST validation SHALL check all four hexagonal layer boundaries: (a) domain shall not import application, infrastructure, or interface; (b) application shall not import infrastructure or interface; (c) infrastructure shall not import interface; (d) shared_kernel shall not import infrastructure or interface. | HARD | SRC-008 (Dependency Rules table); SRC-004 (boundary rules) | These are the authoritative layer boundaries defined in `.context/rules/architecture-standards.md` (SRC-008). The V-038 boundary rule engine encodes these rules as data per SRC-004 TASK-038-02. |
| REQ-403-032 | The PreToolUse hook SHALL verify that file write operations do not modify protected governance files (`docs/governance/JERRY_CONSTITUTION.md`, `.claude/rules/`) without triggering C3+ decision criticality escalation. | MEDIUM | SRC-002 (Mandatory escalation); SRC-003 (FR-005, FR-012) | Barrier-1 ADV-to-ENF requires mandatory escalation for governance files: "Any artifact touching `docs/governance/JERRY_CONSTITUTION.md` or `.claude/rules/` is automatically C3 or higher" (SRC-002, Decision Criticality Escalation). |
| REQ-403-033 | The PreToolUse hook enforcement logic SHALL execute as an external Python process with zero LLM context token cost. | HARD | SRC-001 (L3 properties); SRC-003 (FR-010, NFR-003) | L3 enforcement is defined as "IMMUNE (external)" with "0" token cost (SRC-001, Layer Summary table). Determinism and context-rot-immunity are defining properties of L3. |
| REQ-403-034 | The PreToolUse hook SHALL enforce one-class-per-file (V-041) via AST validation for Python files in `src/`. | MEDIUM | SRC-001 (V-041 at L3); SRC-004 (Phase 3 extended structural) | ADR-EPIC002-002 assigns V-041 (WCS 4.72) to L3/L5. This extends the AST validation framework established by V-038. Implemented in this phase. |
| REQ-403-034a | The PreToolUse hook SHOULD support type hint presence validation (V-039) via AST analysis in a future phase. | MEDIUM | SRC-001 (V-039 at L3); SRC-004 | ADR-EPIC002-002 assigns V-039 (WCS 4.72) to L3/L5. **Deferred:** Not implemented in Phase 3. The engine architecture supports adding this check as an additional validation step in `_validate_content()`. Target: Phase 5 or later. |
| REQ-403-034b | The PreToolUse hook SHOULD support docstring presence validation (V-040) via AST analysis in a future phase. | MEDIUM | SRC-001 (V-040 at L3); SRC-004 | ADR-EPIC002-002 assigns V-040 (WCS 4.72) to L3/L5. **Deferred:** Not implemented in Phase 3. The engine architecture supports adding this check as an additional validation step in `_validate_content()`. Target: Phase 5 or later. |
| REQ-403-035 | The PreToolUse hook SHALL detect dynamic import patterns (`importlib.import_module()`, `__import__()`) and flag them as warnings. | MEDIUM | SRC-004 (FM-038-02, RPN=98); SRC-004 (AC-038-02-06) | Dynamic imports bypass static AST analysis (SRC-004, Risk FM-038-02). Supplementary grep-based detection is the specified mitigation. |
| REQ-403-036 | The PreToolUse hook SHALL exempt the composition root (`src/bootstrap.py`) from import boundary validation. | HARD | SRC-008 (Composition Root section); SRC-004 (AC-038-02-04) | The composition root is the designated location for dependency wiring and must import from all layers (SRC-008, "bootstrap.py - The ONLY place infrastructure is instantiated"). |
| REQ-403-037 | The PreToolUse hook SHALL exempt `TYPE_CHECKING` conditional imports from boundary validation. | HARD | SRC-004 (FM-038-NEW, RPN=36) | TYPE_CHECKING imports are compile-time only and do not create runtime dependencies (SRC-004). Jerry coding standards explicitly require the TYPE_CHECKING pattern for circular import avoidance (SRC-008, "TYPE_CHECKING Pattern" section). |
| REQ-403-038 | The PreToolUse hook SHALL continue to enforce all existing security guardrails (blocked write paths, sensitive file patterns, dangerous commands) defined in the current implementation. | HARD | SRC-005 (existing pre_tool_use.py) | The existing PreToolUse hook (SRC-005) provides critical security guardrails. New enforcement capabilities must be additive, not replacement. |
| REQ-403-039 | The PreToolUse hook SHALL support the existing pattern library integration (AC-015-004) as an additional validation phase alongside AST validation. | MEDIUM | SRC-005 (Phase 2: Pattern-based validation) | The existing pattern library (SRC-005, `check_patterns` function) provides extensible rule-based validation. AST validation is a new phase, not a replacement of pattern validation. |

### SessionStart Hook (L1: Session Initialization)

**Purpose:** Inject quality framework context at session initialization. Provides the L1 behavioral foundation that L2 (UserPromptSubmit) subsequently reinforces.

**Delivery vector:** V-003 (SessionStart Injection)

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-050 | The SessionStart hook SHALL inject quality gate threshold information (>= 0.92) into the session context. | HARD | SRC-002 (SessionStart touchpoint, S-014); SRC-003 (FR-006) | S-014 (LLM-as-Judge) requires quality gate thresholds available from session start (SRC-002, SessionStart Hook table: "Quality gate thresholds (0.92) and scoring rubric reference"). |
| REQ-403-051 | The SessionStart hook SHALL inject references to applicable constitutional principles for the active project context. | HARD | SRC-002 (SessionStart touchpoint, S-007); SRC-003 (FR-006) | S-007 (Constitutional AI) requires constitution sections available from session start (SRC-002, SessionStart Hook table: "Relevant constitution sections for the active project context"). |
| REQ-403-052 | The SessionStart hook SHALL inject adversarial review requirements including the creator-critic-revision cycle (minimum 3 iterations). | MEDIUM | SRC-002 (Quality Gate Integration, Creator-Critic-Revision Cycle) | The minimum 3-iteration cycle is required by the quality framework (SRC-002, "Creator-Critic-Revision Cycle" section). Hooks must ensure the cycle is not bypassed. |
| REQ-403-053 | The SessionStart hook quality context injection SHALL complement the existing project context resolution without breaking current functionality. | HARD | SRC-006 (existing session_start_hook.py) | The existing SessionStart hook (SRC-006) handles project context, validation, and pre-commit warnings. Quality framework integration must be additive (SRC-003 TASK-004 enrichment: "complement existing `scripts/session_start_hook.py` without breaking project context resolution"). |
| REQ-403-054 | The SessionStart hook SHALL inject initial decision criticality defaults (C1-C4) for the session. | MEDIUM | SRC-002 (Decision Criticality Escalation) | The decision criticality framework (C1-C4) governs which adversarial strategies are triggered (SRC-002, Decision Criticality Escalation table). The session must have a default criticality assessment available from start. |
| REQ-403-055 | The SessionStart hook quality context SHALL contribute to the optimized 12,476 token L1 target from ADR-EPIC002-002. | MEDIUM | SRC-001 (Token Budget, L1: ~12,476) | SessionStart content is part of the L1 Static Context layer. The total L1 budget must not exceed 12,476 optimized tokens (SRC-001, Standard Enforcement Budget table). |

---

## Cross-Cutting Requirements

These requirements apply to ALL hook implementations (UserPromptSubmit, PreToolUse, SessionStart).

### Fail-Safe Behavior

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-070 | All hook implementations SHALL implement fail-open error handling: any exception or error in hook logic SHALL NOT prevent the user's intended operation from proceeding. | HARD | SRC-003 (FR-007, NFR-008) | User authority (P-020) requires that enforcement never blocks user work due to hook errors. "Never silently swallow errors, never block the user" (SRC-003, NFR-008). |
| REQ-403-071 | All hook error conditions SHALL be logged to stderr or a log file with sufficient detail for diagnosis. | HARD | SRC-003 (NFR-008); SRC-005 (existing pattern) | Fail-open must not mean fail-silent. The existing PreToolUse hook (SRC-005) logs warnings to stderr. All hooks must maintain observability (SRC-003, "never silently swallow errors"). |
| REQ-403-072 | The PreToolUse hook SHALL fail-open for non-Python files: AST validation SHALL only be attempted on files with `.py` extension. | HARD | SRC-004 (TASK-044-01, AC-044-01-05) | AST analysis is only applicable to Python files. Non-Python files must pass through without validation (SRC-004, pre-commit hook filters to `src/` and Python types). |
| REQ-403-073 | The PreToolUse hook SHALL fail-open when the AST parser encounters a `SyntaxError`: the file SHALL be skipped with a warning, not blocked. | HARD | SRC-004 (AC-038-01-05) | Developers may write syntactically incomplete Python during iterative development. Blocking on syntax errors would prevent the development workflow (SRC-004, "Handles SyntaxError gracefully"). |

### Platform Portability

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-075 | All hook implementations SHALL use only Python stdlib modules (`ast`, `json`, `pathlib`, `sys`, `os`, `re`, `dataclasses`) for core enforcement logic. | HARD | SRC-001 (R-SYS-003 mitigation); SRC-004 (platform portability) | Platform portability is user priority #2 (SRC-001). Using stdlib-only ensures hooks work on any Python 3.11+ installation without additional dependencies (SRC-004, V-038 uses "only Python stdlib"). |
| REQ-403-076 | All hook implementations SHALL use `pathlib.Path` for file path operations to ensure cross-platform path handling. | HARD | SRC-004 (V-038 portability); SRC-008 (coding standards, PTH rule) | `pathlib` handles `/` vs `\` automatically across platforms (SRC-004, "Path operations use pathlib which handles \ vs / automatically"). |
| REQ-403-077 | Hook implementations SHALL degrade gracefully on platforms where Claude Code hooks are unavailable: (a) enforcement logic SHALL be importable as a Python library independent of hook infrastructure; (b) non-Claude-Code platforms SHALL receive equivalent enforcement through alternative integration paths. | HARD | SRC-001 (R-SYS-003); SRC-003 (NFR-002) | Platform migration risk R-SYS-003 (score 16 RED) requires that enforcement survives loss of Claude Code hooks (SRC-001). Architecture must separate enforcement logic from hook infrastructure (SRC-003, NFR-002). |
| REQ-403-078 | File reading operations SHALL specify `encoding='utf-8'` explicitly to ensure consistent behavior across platforms. | MEDIUM | SRC-004 (V-038 Windows portability) | Windows may default to locale encoding (e.g., cp1252) when reading Python files, causing parsing errors (SRC-004, "specify encoding='utf-8' in open() calls"). |

### Architecture Compliance

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-080 | All hook implementations SHALL follow Jerry's hexagonal architecture patterns with enforcement logic separated from hook infrastructure. | HARD | SRC-003 (FR-011); SRC-008 | Enforcement logic (domain-level rules, validation algorithms) must be in the application/domain layers. Hook infrastructure (stdin/stdout handling, JSON parsing, exit codes) must be in the interface layer (SRC-008, layer structure). |
| REQ-403-081 | Enforcement logic SHALL be testable independently of hook infrastructure: enforcement functions SHALL accept typed parameters and return typed results, not read from stdin or write to stdout. | HARD | SRC-008 (testing standards); SRC-004 (V-038 design pattern) | The V-038 design separates the `ASTBoundaryValidator` class (testable library) from the `__main__.py` entry point (hook/CLI infrastructure) (SRC-004). This pattern must be followed by all hooks. |
| REQ-403-082 | Hook entry points (scripts/) SHALL be thin adapters that: (a) read input from stdin, (b) invoke enforcement logic, (c) format output to hook JSON schema, (d) handle errors with fail-open behavior. | HARD | SRC-005 (existing pattern); SRC-008 (interface layer) | The existing PreToolUse hook (SRC-005, `main()` function) follows this thin-adapter pattern: read JSON, invoke check functions, format output. All new hooks must follow this pattern. |

### Token Budget Validation

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-083 | All token budget calculations for V-024 content SHALL be validated against an actual tokenizer (tiktoken cl100k_base or equivalent) during implementation verification. The ~4 chars/token approximation used in design is acceptable for design-phase estimation but SHALL NOT be the sole basis for production budget compliance. | MEDIUM | SRC-001 (Token Budget); Critique B-001/M-001 | The `len//4` approximation has a known ~17% variance from actual tokenizer counts, particularly for XML-tagged content and structured text. Final budget compliance must use actual token counts. |

### Defense-in-Depth

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-085 | The UserPromptSubmit hook (L2) SHALL compensate for L1 (Static Context) context rot by re-injecting critical rules that degrade in the LLM's attention span beyond ~20K context tokens. | HARD | SRC-001 (Defense-in-Depth Compensation Chain); SRC-003 (NFR-007) | "L1 (Static Context) Primary Failure Mode: Context rot after ~20K tokens. Compensated By: L2 re-injects critical rules" (SRC-001, Compensation Chain table). This is the hook's primary mission. |
| REQ-403-086 | The PreToolUse hook (L3) SHALL provide enforcement independent of LLM compliance: if the LLM ignores L2 re-injected rules, L3 SHALL still block non-compliant operations. | HARD | SRC-001 (Defense-in-Depth Compensation Chain); SRC-003 (NFR-007) | "L2 (Per-Prompt Reinforcement) Primary Failure Mode: LLM ignores re-injected rules. Compensated By: L3 deterministically blocks regardless of LLM state" (SRC-001, Compensation Chain table). |
| REQ-403-087 | The L3 PreToolUse hook SHALL NOT depend on any information from the L2 UserPromptSubmit hook output or LLM context state for its enforcement decisions. | HARD | SRC-001 (L3 properties: "IMMUNE (external)"); SRC-003 (NFR-004) | Context-rot-immunity requires that L3 enforcement decisions are derived entirely from external state (file system, AST analysis) and never from LLM context (SRC-003, NFR-004). |

---

## Adversarial Strategy Integration Requirements

These requirements formalize the strategy-to-hook enforcement touchpoints defined in the Barrier-1 ADV-to-ENF handoff (SRC-002).

### Strategy Touchpoint Requirements

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-090 | The UserPromptSubmit hook SHALL support injection of S-007 (Constitutional AI) principle reminders on every user prompt. | HARD | SRC-002 (Enforcement Touchpoints, UserPromptSubmit, S-007: trigger "Always") | S-007 is rank 4 in the selected strategy set (composite score 4.15) and is "Always" triggered at UserPromptSubmit. Jerry's architecture was designed around this pattern (SRC-002). |
| REQ-403-091 | The UserPromptSubmit hook SHALL support injection of S-010 (Self-Refine) self-review reminders on every user prompt. | HARD | SRC-002 (Enforcement Touchpoints, UserPromptSubmit, S-010: trigger "Always") | S-010 is the universal pre-critic baseline (rank 7, score 4.00). "Always" triggered at UserPromptSubmit (SRC-002). |
| REQ-403-092 | The PreToolUse hook SHALL support S-007 (Constitutional AI) compliance verification for file write operations. | MEDIUM | SRC-002 (Enforcement Touchpoints, PreToolUse, S-007) | S-007 is triggered at PreToolUse for "File write operations" to "Verify output aligns with rules in `.claude/rules/`" (SRC-002). |
| REQ-403-093 | The PreToolUse hook SHALL support S-013 (Inversion) anti-pattern verification for architecture-impacting changes. | MEDIUM | SRC-002 (Enforcement Touchpoints, PreToolUse, S-013) | S-013 is triggered at PreToolUse for "Architecture changes" to "Verify that anti-pattern checklist was considered" (SRC-002). |
| REQ-403-094 | The enforcement content format SHALL use XML tags for structured injection to enable Claude to distinguish enforcement content from user content. | HARD | SRC-006 (existing pattern, `<project-context>` tags) | The existing SessionStart hook uses XML tags (`<project-context>`, `<project-error>`, `<project-required>`) for structured content (SRC-006). This pattern ensures Claude can parse enforcement-injected content reliably. |

### Quality Gate Requirements

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-095 | The hook-based enforcement system SHALL support the 0.92 quality threshold by ensuring it is present in both SessionStart context (L1) and UserPromptSubmit reinforcement (L2). | HARD | SRC-002 (0.92 Threshold); SRC-001 (L1+L2) | The quality threshold must survive context rot. Dual injection (L1 at session start + L2 on every prompt) provides redundancy per the defense-in-depth architecture (SRC-001, SRC-002). |
| REQ-403-096 | The hook-based enforcement system SHALL support the creator-critic-revision cycle by injecting cycle requirements into the session context and reinforcing them per-prompt when deliverables are expected. | MEDIUM | SRC-002 (Creator-Critic-Revision Cycle) | The minimum 3-iteration cycle "must be enforced -- hooks must ensure the cycle is not bypassed" (SRC-002, Quality Gate Integration Requirements). |

---

## Decision Criticality Requirements

| Req ID | Requirement | Priority | Source | Rationale |
|--------|-------------|----------|--------|-----------|
| REQ-403-060 | Hook-based enforcement SHALL support decision criticality classification at four levels: C1 (Routine), C2 (Standard), C3 (Significant), C4 (Critical). | MEDIUM | SRC-002 (Decision Criticality Escalation table) | Decision criticality determines which adversarial strategies are triggered and at what depth (SRC-002, Quality Layer to Strategy mapping). |
| REQ-403-061 | The PreToolUse hook SHALL automatically escalate to C3+ criticality for any write operation targeting `docs/governance/JERRY_CONSTITUTION.md` or any file in `.claude/rules/`. | HARD | SRC-002 (Mandatory escalation) | "Any artifact touching `docs/governance/JERRY_CONSTITUTION.md` or `.claude/rules/` is automatically C3 or higher" (SRC-002, Decision Criticality Escalation). |
| REQ-403-062 | The UserPromptSubmit hook SHALL adjust reinforcement content intensity based on the current decision criticality level: C3+ decisions SHALL receive enhanced reinforcement including pre-mortem (S-004) and FMEA (S-012) reminders. | MEDIUM | SRC-002 (Quality Layer mapping) | At C3 (Deep Review), strategies S-004 and S-012 are added to the standard L2 set (SRC-002, Strategy Composition at Each Quality Layer). |

---

## Requirements Traceability Matrix

| Req ID | Source FR/NFR | ADR Vector | Barrier-1 Strategy | Hook Type | Verification Method |
|--------|-------------|------------|---------------------|-----------|---------------------|
| REQ-403-010 | FR-001 | V-024, V-005 | -- | UserPromptSubmit | Test (T) |
| REQ-403-011 | FR-001 | V-005 | -- | UserPromptSubmit | Inspection (I) |
| REQ-403-012 | FR-002 | V-024 | S-014 | UserPromptSubmit | Test (T) |
| REQ-403-013 | FR-002 | V-024 | S-007 | UserPromptSubmit | Test (T) |
| REQ-403-014 | FR-002 | V-024 | S-010 | UserPromptSubmit | Test (T) |
| REQ-403-015 | FR-003, NFR-001 | V-024 | -- | UserPromptSubmit | Test (T) |
| REQ-403-016 | FR-008 | V-024 | S-014 | UserPromptSubmit | Test (T) |
| REQ-403-017 | FR-009 | V-024 | S-014 (R-014-FN) | UserPromptSubmit | Inspection (I) |
| REQ-403-018 | -- | V-024 | S-003 | UserPromptSubmit | Test (T) |
| REQ-403-019 | -- | V-005 | -- | UserPromptSubmit | Test (T) |
| REQ-403-030 | FR-004 | V-038, V-001 | -- | PreToolUse | Test (T) |
| REQ-403-031 | FR-004 | V-038 | -- | PreToolUse | Test (T) |
| REQ-403-032 | FR-005, FR-012 | V-001 | S-007 | PreToolUse | Test (T) |
| REQ-403-033 | FR-010, NFR-003 | V-001 | -- | PreToolUse | Analysis (A) |
| REQ-403-034 | -- | V-041 | -- | PreToolUse | Test (T) |
| REQ-403-034a | -- | V-039 | -- | PreToolUse | Test (T) -- deferred |
| REQ-403-034b | -- | V-040 | -- | PreToolUse | Test (T) -- deferred |
| REQ-403-035 | -- | V-038 | -- | PreToolUse | Test (T) |
| REQ-403-036 | -- | V-038 | -- | PreToolUse | Test (T) |
| REQ-403-037 | -- | V-038 | -- | PreToolUse | Test (T) |
| REQ-403-038 | -- | V-001 | -- | PreToolUse | Test (T) |
| REQ-403-039 | -- | V-001 | -- | PreToolUse | Test (T) |
| REQ-403-050 | FR-006 | V-003 | S-014 | SessionStart | Test (T) |
| REQ-403-051 | FR-006 | V-003 | S-007 | SessionStart | Test (T) |
| REQ-403-052 | -- | V-003 | S-014 | SessionStart | Test (T) |
| REQ-403-053 | FR-006 | V-003 | -- | SessionStart | Test (T) |
| REQ-403-054 | -- | V-003 | -- | SessionStart | Test (T) |
| REQ-403-055 | -- | V-003 | -- | SessionStart | Analysis (A) |
| REQ-403-060 | FR-012 | -- | -- | Cross-cutting | Inspection (I) |
| REQ-403-061 | FR-012 | V-001 | S-007 | PreToolUse | Test (T) |
| REQ-403-062 | -- | V-024 | S-004, S-012 | UserPromptSubmit | Test (T) |
| REQ-403-070 | FR-007, NFR-008 | -- | -- | Cross-cutting | Test (T) |
| REQ-403-071 | NFR-008 | -- | -- | Cross-cutting | Test (T) |
| REQ-403-072 | -- | V-001 | -- | PreToolUse | Test (T) |
| REQ-403-073 | -- | V-038 | -- | PreToolUse | Test (T) |
| REQ-403-075 | NFR-002 | -- | -- | Cross-cutting | Inspection (I) |
| REQ-403-076 | NFR-002 | -- | -- | Cross-cutting | Inspection (I) |
| REQ-403-077 | NFR-002 | -- | -- | Cross-cutting | Demonstration (D) |
| REQ-403-078 | NFR-002 | -- | -- | Cross-cutting | Inspection (I) |
| REQ-403-080 | FR-011 | -- | -- | Cross-cutting | Inspection (I) |
| REQ-403-081 | FR-011 | -- | -- | Cross-cutting | Inspection (I) |
| REQ-403-082 | FR-011 | -- | -- | Cross-cutting | Inspection (I) |
| REQ-403-085 | NFR-007 | V-024 | -- | UserPromptSubmit | Analysis (A) |
| REQ-403-086 | NFR-007 | V-001 | -- | PreToolUse | Test (T) |
| REQ-403-087 | NFR-004 | V-001 | -- | PreToolUse | Inspection (I) |
| REQ-403-090 | -- | V-024 | S-007 | UserPromptSubmit | Test (T) |
| REQ-403-091 | -- | V-024 | S-010 | UserPromptSubmit | Test (T) |
| REQ-403-092 | FR-005 | V-001 | S-007 | PreToolUse | Test (T) |
| REQ-403-093 | -- | V-001 | S-013 | PreToolUse | Test (T) |
| REQ-403-094 | -- | -- | -- | Cross-cutting | Inspection (I) |
| REQ-403-095 | -- | V-024, V-003 | S-014 | Cross-cutting | Test (T) |
| REQ-403-096 | -- | V-024, V-003 | S-014 | Cross-cutting | Test (T) |

**Coverage summary:**
- Total requirements: 44 (42 original + 2 split from REQ-403-034)
- Traced to EN-403 FR/NFR: 30 (68%)
- Traced to ADR-EPIC002-002 vectors: 37 (84%)
- Traced to Barrier-1 strategies: 20 (45%)
- With defined verification method: 44 (100%)
- Deferred requirements (V-039, V-040): 2 (explicitly marked for future implementation)

---

## Verification Methods

Each requirement is assigned one of four verification methods per NASA NPR 7123.1D Section 6.4.2:

| Method | Symbol | Description | Applicable When |
|--------|--------|-------------|-----------------|
| Test | T | Execute the system and observe measurable behavior | Requirement specifies a functional behavior that produces observable output |
| Inspection | I | Examine artifacts (code, documents) for compliance | Requirement specifies a structural property (architecture, format, encoding) |
| Analysis | A | Apply analytical techniques (token counting, performance modeling) | Requirement specifies a constraint that cannot be directly tested (token budget, context rot immunity) |
| Demonstration | D | Show the system working in a representative environment | Requirement specifies cross-platform or integration behavior |

### Verification Plan Summary

| Verification Method | Count | Percentage |
|--------------------|-------|-----------|
| Test (T) | 28 | 67% |
| Inspection (I) | 10 | 24% |
| Analysis (A) | 3 | 7% |
| Demonstration (D) | 1 | 2% |

### Key Verification Activities

| Activity | Requirements Verified | Method | Timing |
|----------|----------------------|--------|--------|
| Unit tests for UserPromptSubmit enforcement logic | REQ-403-010 through REQ-403-019 | T | TASK-005 |
| Unit tests for PreToolUse AST validation | REQ-403-030 through REQ-403-039 | T | TASK-006 |
| Unit tests for SessionStart quality injection | REQ-403-050 through REQ-403-055 | T | TASK-007 |
| Fail-safe error injection tests | REQ-403-070 through REQ-403-073 | T | TASK-005/006/007 |
| Token budget analysis (count V-024 tokens) | REQ-403-015, REQ-403-055 | A | TASK-005 |
| Code review for architecture compliance | REQ-403-080 through REQ-403-082 | I | TASK-008 |
| Code review for stdlib-only imports | REQ-403-075, REQ-403-076, REQ-403-078 | I | TASK-008 |
| Defense-in-depth scenario testing | REQ-403-085 through REQ-403-087 | T/A | TASK-009 |
| Platform portability demonstration | REQ-403-077 | D | TASK-012 |
| Adversarial review (bypass attempts) | REQ-403-070, REQ-403-086 | T | TASK-009 |

---

## References

### Primary Sources

| # | Citation | Used For |
|---|----------|----------|
| 1 | ADR-EPIC002-002 v1.2.0 (ACCEPTED) | 5-layer architecture, vector assignments, token budgets, defense-in-depth, implementation phasing |
| 2 | Barrier-1 ADV-to-ENF Handoff | Strategy-to-hook touchpoints, quality gate integration, decision criticality, token budget for V-024 |
| 3 | EN-403 Enabler Definition v2.0.0 | FR-001 through FR-012, NFR-001 through NFR-008, acceptance criteria |
| 4 | EN-402 TASK-006 Execution Plans v1.1.0 | V-038 AST validator architecture, boundary rules, CLI design |
| 5 | `scripts/pre_tool_use.py` | Current PreToolUse implementation patterns |
| 6 | `scripts/session_start_hook.py` | Current SessionStart implementation patterns |
| 7 | `hooks/hooks.json` | Hook registration configuration |
| 8 | `.context/rules/architecture-standards.md` | Hexagonal architecture boundary rules |

### Methodology Sources

| # | Citation | Used For |
|---|----------|----------|
| 9 | NASA NPR 7123.1D: Systems Engineering Processes and Requirements | Requirements engineering methodology (Section 6.1, 6.4.2) |
| 10 | NASA-STD-8739.8: Software Assurance and Software Safety Standard | Prevent-detect-verify enforcement principle |

---

*Agent: nse-requirements (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-403 Hook-Based Enforcement Implementation*
*Quality Target: >= 0.92*
*Target ACs: 1, 5, 8*
