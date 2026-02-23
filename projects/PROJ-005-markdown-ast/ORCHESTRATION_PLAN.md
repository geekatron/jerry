# PROJ-005 Universal Markdown Parser: Orchestration Plan

> **Document ID:** PROJ-005-AST-UNIVERSAL-ORCH-PLAN
> **Project:** PROJ-005-markdown-ast
> **Workflow ID:** `ast-universal-20260222-001`
> **Status:** PLANNED
> **Version:** 1.0
> **Criticality:** C4 (Critical -- architecture-level, irreversible)
> **Quality Threshold:** >= 0.95 (user-specified, above H-13 standard 0.92)
> **Created:** 2026-02-22
> **Last Updated:** 2026-02-22
> **Branch:** `feature/PROJ-005-ast-universal-markdown-parser`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Stakeholder-facing overview |
| [L1: Technical Architecture](#l1-technical-architecture) | Pipeline topology, phase definitions, agent registry |
| [L2: Strategic Implications](#l2-strategic-implications) | Risk analysis, quality tournament, cross-pollination design |
| [Workflow Architecture](#workflow-architecture) | ASCII pipeline diagram and topology |
| [Pipeline 1: Engineering](#pipeline-1-engineering-eng) | /eng-team phases 1-6 |
| [Pipeline 2: Red Team](#pipeline-2-red-team-red) | /red-team phases 1-4 |
| [Sync Barriers](#sync-barriers) | Cross-pollination barriers 1-4 |
| [Agent Registry](#agent-registry) | All agents with inputs, outputs, tools |
| [Quality Gate Definitions](#quality-gate-definitions) | C4 tournament configuration at every barrier |
| [Adversary Quality Configuration](#adversary-quality-configuration) | All 10 strategies, scoring, iteration model |
| [Path Scheme](#path-scheme) | Dynamic artifact paths |
| [State Management](#state-management) | ORCHESTRATION.yaml structure |
| [Execution Constraints](#execution-constraints) | Constitutional and architectural constraints |
| [Success Criteria](#success-criteria) | Per-phase and workflow exit criteria |
| [Risk Register](#risk-register) | Identified risks with mitigations |
| [Recovery Strategies](#recovery-strategies) | Failure modes and recovery procedures |
| [Resumption Context](#resumption-context) | Current state and next actions |
| [Disclaimer](#disclaimer) | Agent-generated content notice |

---

## L0: Executive Summary

This orchestration plan coordinates the enhancement of the Jerry AST skill and CLI from a worktracker-only parser to a **universal markdown parser** supporting all 10 Jerry document types. The work uses two cross-pollinated pipelines -- Engineering (/eng-team) and Red Team (/red-team) -- synchronized through 4 barriers with C4 tournament quality gates at each barrier.

**What changes:** The AST infrastructure gains YAML frontmatter parsing, XML-tag section extraction, HTML comment metadata parsing, document type auto-detection, and extended schema validation covering agent definitions, SKILL.md files, rule files, ADRs, strategy templates, CLAUDE.md, orchestration artifacts, pattern documentation, and knowledge documents.

**Why C4:** This is an architecture-level change affecting the core parsing infrastructure that all other Jerry tools depend on. The parser extension touches security-sensitive input validation paths (CWE-20, CWE-78, CWE-22). Changes are irreversible once downstream consumers depend on the new schemas.

**Scale:** 2 pipelines, 10 phases total (6 engineering + 4 red team), 4 sync barriers, 10 agent roles, C4 tournament with all 10 adversarial strategies at every barrier.

---

## L1: Technical Architecture

### Current State (Implemented -- FEAT-001 Complete)

| Component | Status | Files |
|-----------|--------|-------|
| JerryDocument facade | Complete | `src/domain/markdown_ast/jerry_document.py` |
| BlockquoteFrontmatter | Complete | `src/domain/markdown_ast/frontmatter.py` |
| Navigation table extraction | Complete | `src/domain/markdown_ast/nav_table.py` |
| L2-REINJECT directives | Complete | `src/domain/markdown_ast/reinject.py` |
| Schema validation (6 schemas) | Complete | `src/domain/markdown_ast/schema.py` |
| CLI commands | Complete | `src/interface/cli/ast_commands.py` |
| /ast skill | Complete | `skills/ast/SKILL.md` |

### Target State (This Workflow)

| New Component | Purpose | Domain File |
|---------------|---------|-------------|
| YamlFrontmatter | Parse `---` delimited YAML frontmatter | `src/domain/markdown_ast/yaml_frontmatter.py` |
| XmlSectionParser | Extract XML-tagged body sections | `src/domain/markdown_ast/xml_section.py` |
| HtmlCommentMetadata | Parse HTML comment metadata | `src/domain/markdown_ast/html_comment.py` |
| DocumentTypeDetector | Auto-detect file type from path + structure | `src/domain/markdown_ast/document_type.py` |
| Extended EntitySchema | New schemas for all 10 file types | `src/domain/markdown_ast/schema.py` (extend) |
| CLI extensions | Enhanced flags, new subcommands | `src/interface/cli/ast_commands.py` (extend) |
| UniversalDocument | Unified facade delegating to type-specific parsers | `src/domain/markdown_ast/universal_document.py` |

### File Types Supported (10 Total)

| # | Type | Frontmatter | Body Structure | Schema Required |
|---|------|-------------|----------------|-----------------|
| 1 | Agent definitions | YAML (`---`) | XML tags (`<identity>`, etc.) | Yes (JSON Schema exists) |
| 2 | SKILL.md | YAML (`---`) | Headings + triple-lens tables | Yes (new) |
| 3 | Rule files | None | L2-REINJECT + HARD/MEDIUM tables | Yes (new) |
| 4 | ADRs | HTML comments | Status/Context/Decision/Consequences | Yes (new) |
| 5 | Strategy templates | Blockquote | 8-section format | Yes (new) |
| 6 | Worktracker entities | Blockquote | Entity-specific | Yes (existing, 6 schemas) |
| 7 | CLAUDE.md / AGENTS.md | None | Tables + skill references | Yes (new) |
| 8 | Orchestration artifacts | Various | Plans, handoffs, synthesis | Yes (new) |
| 9 | Pattern documentation | Blockquote | Headings + patterns | Yes (new) |
| 10 | Knowledge documents | None | Navigation tables + content | Yes (new) |

---

## L2: Strategic Implications

### Architecture Impact

The universal parser becomes the **single point of structural truth** for all Jerry markdown. Every downstream consumer -- worktracker, skill routing, rule enforcement, quality gates -- depends on the correctness of this parsing layer. Defects here amplify across the entire framework (FMEA R-T01, RPN 392).

### Security Implications

Parser extensions introduce new attack surface:
- YAML deserialization (must enforce `safe_load` -- no arbitrary object construction)
- XML tag parsing (must handle nested, malformed, and injection attempts)
- HTML comment parsing (must reject embedded executable content)
- Path traversal via file path fields in frontmatter
- Denial-of-service via deeply nested structures

The dual-pipeline (eng + red) architecture ensures security is validated offensively, not just defensively.

### Irreversibility Assessment

Once downstream consumers (worktracker, skill routing, pre-commit hooks) depend on the extended schemas, rolling back requires coordinated migration of all consumers. This justifies C4 criticality.

---

## Workflow Architecture

### Master Pipeline Diagram

```
 PREREQUISITES (COMPLETE)
 +-- FEAT-001 implementation (10 stories, PG5 0.951)
 +-- GO decision: markdown-it-py + mdformat (Pattern D)
 +-- Branch: feature/PROJ-005-ast-universal-markdown-parser
 |
 |
 v
 ============================================================================
 PIPELINE 1: ENGINEERING (/eng-team)        PIPELINE 2: RED TEAM (/red-team)
 alias: "eng"                               alias: "red"
 ============================================================================
 |                                          |
 |  ENG PHASE 1                             |  RED PHASE 1
 |  Architecture & Threat Model             |  Scope & Authorization
 |  [eng-architect]                         |  [red-lead]
 |  Output: Threat model +                  |  Output: Scope document
 |          Architecture ADR +              |          (RED-XXXX format)
 |          Trust boundary diagram          |
 |                                          |
 +==========================================+
 |                                          |
 |          BARRIER 1: THREAT MODEL <-> SCOPE
 |          eng->red: Threat model findings inform targeting
 |          red->eng: Scope confirms attack surface boundaries
 |          Quality Gate: QG-B1 (C4 tournament, >= 0.95)
 |
 +==========================================+
 |                                          |
 |  ENG PHASE 2                             |
 |  Implementation Planning                 |
 |  [eng-lead]                              |
 |  Output: Impl plan + dependency          |
 |          assessment                      |
 |                                          |
 |  ENG PHASE 3                             |  RED PHASE 2
 |  Core Implementation                     |  Vulnerability Analysis
 |  [eng-backend]                           |  [red-vuln]
 |  Output: Domain objects +                |  Output: Vuln assessment
 |          CLI extensions +                |          with CVE/CWE
 |          unit tests                      |          mappings
 |                                          |
 +==========================================+
 |                                          |
 |          BARRIER 2: IMPLEMENTATION <-> VULN TESTING
 |          eng->red: Implemented code for testing
 |          red->eng: Early vuln findings for hardening
 |          Quality Gate: QG-B2 (C4 tournament, >= 0.95)
 |
 +==========================================+
 |                                          |
 |  ENG PHASE 4                             |  RED PHASE 3
 |  Testing & Fuzzing                       |  Exploitation Testing
 |  [eng-qa]                                |  [red-exploit]
 |  Output: Test strategy +                 |  Output: Exploitation
 |          implementations +               |          report with PoC
 |          coverage report                 |          evidence
 |                                          |
 |  ENG PHASE 5                             |
 |  Security Review                         |
 |  [eng-security]                          |
 |  Output: Security review                 |
 |          report + remediation            |
 |                                          |
 +==========================================+
 |                                          |
 |          BARRIER 3: RED FINDINGS <-> SECURITY HARDENING
 |          red->eng: Exploitation findings + PoC for hardening
 |          eng->red: Security review findings for validation
 |          Quality Gate: QG-B3 (C4 tournament, >= 0.95)
 |
 +==========================================+
 |                                          |
 |  ENG PHASE 6                             |  RED PHASE 4
 |  Final Quality Gate                      |  Findings & Remediation
 |  [eng-reviewer]                          |  [red-reporter]
 |  Output: Quality gate report +           |  Output: Final engagement
 |          release readiness               |          report + roadmap
 |                                          |
 +==========================================+
 |                                          |
 |          BARRIER 4: FINAL SYNTHESIS
 |          Both: Quality gate + engagement report -> synthesis
 |          Quality Gate: QG-B4 (C4 tournament, ALL 10 strategies)
 |          adv-executors as concurrent background agents
 |
 +==========================================+
 |
 v
 WORKFLOW COMPLETE
 Universal markdown parser validated, secured, documented
```

### Topology Summary

| Aspect | Value |
|--------|-------|
| Pattern | Dual-pipeline cross-pollinated with sync barriers |
| Pipelines | 2 (Engineering, Red Team) |
| Total phases | 10 (6 eng + 4 red) |
| Sync barriers | 4 |
| Quality gates | 4 (one per barrier, all C4 tournament) |
| Max concurrent agents | 2 (one per pipeline at barrier boundaries) |
| Max routing hops | 3 (H-36 circuit breaker) |
| Agent nesting | 1 level (H-01/P-003) |

---

## Pipeline 1: Engineering (eng)

### ENG Phase 1: Architecture & Threat Model

| Field | Value |
|-------|-------|
| Phase ID | `eng-phase-1` |
| Path ID | `eng/phase-1-architecture` |
| Agent | `eng-architect` |
| Model | opus |
| Execution Mode | SEQUENTIAL |
| Depends On | Prerequisites (FEAT-001 complete) |
| Blocked By | None |

**Agent Task:** Produce a threat model (STRIDE/DREAD) for the parser extension attack surface. Design the architecture for multi-format frontmatter, XML section parsing, and document type detection. Create an ADR for universal parser design decisions. Analyze trust boundaries between CLI input and domain objects.

**Inputs:**
- `src/domain/markdown_ast/` (all existing domain objects)
- `src/interface/cli/ast_commands.py` (existing CLI)
- `docs/schemas/agent-definition-v1.schema.json` (agent schema)
- `.context/rules/architecture-standards.md` (H-07 layer isolation)
- `.context/rules/coding-standards.md` (H-11 type hints)
- `.context/rules/agent-development-standards.md` (agent definition format)

**Outputs:**
- `orchestration/ast-universal-20260222-001/eng/phase-1-architecture/eng-architect/threat-model.md`
- `orchestration/ast-universal-20260222-001/eng/phase-1-architecture/eng-architect/architecture-adr.md`
- `orchestration/ast-universal-20260222-001/eng/phase-1-architecture/eng-architect/trust-boundary-diagram.md`

**Success Criteria:**
- STRIDE analysis covers all 6 threat categories for each new parser component
- DREAD risk scores calculated for each identified threat
- Architecture ADR follows ADR template format
- Trust boundaries identified between CLI input, file system reads, and domain object construction
- H-07 layer isolation maintained in proposed architecture
- H-10 one class per file enforced in all new domain objects

---

### ENG Phase 2: Implementation Planning

| Field | Value |
|-------|-------|
| Phase ID | `eng-phase-2` |
| Path ID | `eng/phase-2-planning` |
| Agent | `eng-lead` |
| Model | opus |
| Execution Mode | SEQUENTIAL |
| Depends On | Barrier 1 complete |
| Blocked By | QG-B1 |

**Agent Task:** Enforce coding standards. Break down the 7 enhancements into ordered work items with dependency graph. Assess dependency governance for any new libraries. Verify coding standards alignment (H-07, H-10, H-11).

**Inputs:**
- Barrier 1 handoff (threat model + scope document)
- `orchestration/ast-universal-20260222-001/eng/phase-1-architecture/eng-architect/architecture-adr.md`
- `orchestration/ast-universal-20260222-001/eng/phase-1-architecture/eng-architect/threat-model.md`
- `pyproject.toml` (current dependencies)
- `.context/rules/coding-standards.md`
- `.context/rules/architecture-standards.md`

**Outputs:**
- `orchestration/ast-universal-20260222-001/eng/phase-2-planning/eng-lead/implementation-plan.md`
- `orchestration/ast-universal-20260222-001/eng/phase-2-planning/eng-lead/dependency-assessment.md`

**Success Criteria:**
- All 7 enhancements decomposed into ordered work items
- Dependency graph identifies critical path
- No new external dependencies without justification (markdown-it-py + mdformat stack reuse preferred)
- Standards compliance checklist per work item

---

### ENG Phase 3: Core Implementation

| Field | Value |
|-------|-------|
| Phase ID | `eng-phase-3` |
| Path ID | `eng/phase-3-implementation` |
| Agent | `eng-backend` |
| Model | sonnet |
| Execution Mode | SEQUENTIAL |
| Depends On | ENG Phase 2 complete |
| Blocked By | `eng-phase-2` |

**Agent Task:** Implement all new domain objects following BDD test-first (H-20). Create `YamlFrontmatter`, `XmlSectionParser`, `HtmlCommentMetadata`, `DocumentTypeDetector`, `UniversalDocument`. Extend `EntitySchema` with new schemas for all 10 file types. Extend CLI commands.

**Inputs:**
- `orchestration/ast-universal-20260222-001/eng/phase-2-planning/eng-lead/implementation-plan.md`
- `src/domain/markdown_ast/` (existing code)
- `src/interface/cli/ast_commands.py` (existing CLI)
- `docs/schemas/agent-definition-v1.schema.json`
- `.context/rules/testing-standards.md`

**Outputs:**
- New domain files: `yaml_frontmatter.py`, `xml_section.py`, `html_comment.py`, `document_type.py`, `universal_document.py`
- Extended: `schema.py`, `ast_commands.py`
- Unit tests for all new domain objects
- `orchestration/ast-universal-20260222-001/eng/phase-3-implementation/eng-backend/implementation-report.md`

**Success Criteria:**
- All 7 enhancements implemented
- BDD test-first: tests written before implementation (H-20)
- H-10: One class per file for all new domain objects
- H-11: Type hints + docstrings on all public functions
- H-07: Domain layer imports only from domain; no infrastructure leakage
- H-33: AST-based parsing, no regex for frontmatter extraction
- Input validation for all parsers (CWE-20)
- `safe_load` enforced for YAML deserialization
- All 10 file types parseable with correct schema validation

---

### ENG Phase 4: Testing & Fuzzing

| Field | Value |
|-------|-------|
| Phase ID | `eng-phase-4` |
| Path ID | `eng/phase-4-testing` |
| Agent | `eng-qa` |
| Model | sonnet |
| Execution Mode | SEQUENTIAL |
| Depends On | Barrier 2 complete |
| Blocked By | QG-B2 |

**Agent Task:** BDD test strategy (H-20). Test coverage for all 10 file types. Fuzzing for parser robustness (malformed YAML, nested XML tags, injection via frontmatter values). Property-based testing for roundtrip fidelity. 90% line coverage enforcement (H-20).

**Inputs:**
- Barrier 2 handoff (implementation + early vuln findings)
- `src/domain/markdown_ast/` (all files including new)
- `tests/` (existing test suite)
- `orchestration/ast-universal-20260222-001/red/phase-2-vulnerability/red-vuln/vulnerability-assessment.md`

**Outputs:**
- `orchestration/ast-universal-20260222-001/eng/phase-4-testing/eng-qa/test-strategy.md`
- `orchestration/ast-universal-20260222-001/eng/phase-4-testing/eng-qa/coverage-report.md`
- New test files in `tests/`

**Success Criteria:**
- 90% line coverage on all new domain modules (H-20)
- Fuzz tests for malformed YAML, nested XML, HTML comment injection
- Property-based tests for parse-render roundtrip fidelity
- All 10 file types have dedicated test fixtures
- Red team early findings addressed in test cases
- Full existing test suite passes (no regression)

---

### ENG Phase 5: Security Review

| Field | Value |
|-------|-------|
| Phase ID | `eng-phase-5` |
| Path ID | `eng/phase-5-security` |
| Agent | `eng-security` |
| Model | opus |
| Execution Mode | SEQUENTIAL |
| Depends On | ENG Phase 4 complete, Barrier 3 inputs available |
| Blocked By | `eng-phase-4` |

**Agent Task:** Manual security code review of all new parser code. CWE-20 (input validation), CWE-78 (command injection via CLI args), CWE-22 (path traversal in file references). YAML deserialization safety. Data flow tracing from CLI input to domain objects.

**Inputs:**
- `src/domain/markdown_ast/` (all files)
- `src/interface/cli/ast_commands.py`
- `orchestration/ast-universal-20260222-001/red/phase-3-exploitation/red-exploit/exploitation-report.md` (if available from Barrier 3)
- `orchestration/ast-universal-20260222-001/eng/phase-1-architecture/eng-architect/threat-model.md`

**Outputs:**
- `orchestration/ast-universal-20260222-001/eng/phase-5-security/eng-security/security-review-report.md`

**Success Criteria:**
- All CWE categories reviewed (CWE-20, CWE-22, CWE-78)
- YAML deserialization verified as `safe_load` only
- No path traversal possible via frontmatter/metadata fields
- No command injection possible via CLI arguments
- Data flow diagram from input to domain objects
- All red team exploitation findings have corresponding mitigations

---

### ENG Phase 6: Final Quality Gate

| Field | Value |
|-------|-------|
| Phase ID | `eng-phase-6` |
| Path ID | `eng/phase-6-quality-gate` |
| Agent | `eng-reviewer` |
| Model | opus |
| Execution Mode | SEQUENTIAL |
| Depends On | ENG Phase 5 complete |
| Blocked By | `eng-phase-5` |

**Agent Task:** Final quality gate. Compliance verification against H-07, H-10, H-11, H-20, H-33. Release readiness assessment. Invoke /adversary for C4 quality scoring.

**Inputs:**
- All engineering phase outputs
- `src/domain/markdown_ast/` (final state)
- `tests/` (final test suite)
- Coverage reports
- Security review report

**Outputs:**
- `orchestration/ast-universal-20260222-001/eng/phase-6-quality-gate/eng-reviewer/quality-gate-report.md`
- `orchestration/ast-universal-20260222-001/eng/phase-6-quality-gate/eng-reviewer/release-readiness.md`

**Success Criteria:**
- H-07 layer isolation verified across all new files
- H-10 one class per file verified
- H-11 type hints + docstrings verified
- H-20 90% line coverage verified
- H-33 AST-based parsing verified (no regex for frontmatter)
- All security review findings resolved
- Full test suite passes
- Release readiness: GO or NO-GO with evidence

---

## Pipeline 2: Red Team (red)

### RED Phase 1: Scope & Authorization

| Field | Value |
|-------|-------|
| Phase ID | `red-phase-1` |
| Path ID | `red/phase-1-scope` |
| Agent | `red-lead` |
| Model | opus |
| Execution Mode | SEQUENTIAL |
| Depends On | Prerequisites (FEAT-001 complete) |
| Blocked By | None |

**Agent Task:** MANDATORY FIRST. Create scope document for AST parser security testing engagement. Define authorized targets, technique allowlist, exclusion list, rules of engagement.

**Inputs:**
- `src/domain/markdown_ast/` (existing code)
- `src/interface/cli/ast_commands.py`
- Project context (10 file types to support)

**Outputs:**
- `orchestration/ast-universal-20260222-001/red/phase-1-scope/red-lead/scope-document.md`

**Success Criteria:**
- Scope document follows RED-XXXX format
- Authorized targets explicitly listed (parser inputs, CLI arguments, file system access)
- Technique allowlist defined
- Exclusion list defined (no production data, no external systems)
- Rules of engagement documented
- Emergency contacts and escalation procedures defined

---

### RED Phase 2: Vulnerability Analysis

| Field | Value |
|-------|-------|
| Phase ID | `red-phase-2` |
| Path ID | `red/phase-2-vulnerability` |
| Agent | `red-vuln` |
| Model | opus |
| Execution Mode | SEQUENTIAL |
| Depends On | Barrier 1 complete, ENG Phase 3 available |
| Blocked By | QG-B1 |

**Agent Task:** Vulnerability analysis of markdown parsing. Malformed YAML frontmatter injection. XML tag nesting attacks. HTML comment injection. Path traversal. DoS via deeply nested structures. YAML deserialization attacks.

**Inputs:**
- `orchestration/ast-universal-20260222-001/red/phase-1-scope/red-lead/scope-document.md`
- `orchestration/ast-universal-20260222-001/eng/phase-1-architecture/eng-architect/threat-model.md`
- `src/domain/markdown_ast/` (implementation when available from ENG Phase 3)

**Outputs:**
- `orchestration/ast-universal-20260222-001/red/phase-2-vulnerability/red-vuln/vulnerability-assessment.md`

**Success Criteria:**
- CVE/CWE mappings for all identified vulnerabilities
- Risk scoring per vulnerability (CVSS or DREAD)
- Malformed input test vectors documented
- YAML deserialization attack vectors tested
- XML nesting depth limits verified
- Path traversal vectors identified and tested

---

### RED Phase 3: Exploitation Testing

| Field | Value |
|-------|-------|
| Phase ID | `red-phase-3` |
| Path ID | `red/phase-3-exploitation` |
| Agent | `red-exploit` |
| Model | opus |
| Execution Mode | SEQUENTIAL |
| Depends On | Barrier 2 complete |
| Blocked By | QG-B2 |

**Agent Task:** Craft proof-of-concept malicious markdown files. Test parser boundary validation. Verify input sanitization effectiveness. Command injection via frontmatter values. Path traversal via file path fields.

**Inputs:**
- `orchestration/ast-universal-20260222-001/red/phase-2-vulnerability/red-vuln/vulnerability-assessment.md`
- `src/domain/markdown_ast/` (implemented code)
- `src/interface/cli/ast_commands.py`

**Outputs:**
- `orchestration/ast-universal-20260222-001/red/phase-3-exploitation/red-exploit/exploitation-report.md`

**Success Criteria:**
- PoC malicious markdown files for each vulnerability class
- Parser boundary validation tested with evidence
- Input sanitization effectiveness verified
- Command injection attempts documented with results
- Path traversal attempts documented with results
- Each PoC includes: vulnerability, technique, evidence, impact, recommended fix

---

### RED Phase 4: Findings & Remediation

| Field | Value |
|-------|-------|
| Phase ID | `red-phase-4` |
| Path ID | `red/phase-4-findings` |
| Agent | `red-reporter` |
| Model | opus |
| Execution Mode | SEQUENTIAL |
| Depends On | Barrier 3 complete |
| Blocked By | QG-B3 |

**Agent Task:** Comprehensive findings documentation. Risk scoring. Remediation recommendations aligned with eng-security review. Executive summary. Evidence chain validation. Scope compliance attestation.

**Inputs:**
- All red team phase outputs
- `orchestration/ast-universal-20260222-001/eng/phase-5-security/eng-security/security-review-report.md`

**Outputs:**
- `orchestration/ast-universal-20260222-001/red/phase-4-findings/red-reporter/engagement-report.md`

**Success Criteria:**
- All findings risk-scored (Critical/High/Medium/Low/Informational)
- Remediation recommendations for each finding
- Remediation aligned with engineering security review
- Executive summary suitable for stakeholders
- Evidence chain validated for each finding
- Scope compliance attestation (stayed within authorized boundaries)
- Total findings count with breakdown by severity

---

## Sync Barriers

### Barrier 1: Threat Model <-> Red Team Scope

| Field | Value |
|-------|-------|
| Barrier ID | `barrier-1` |
| Path | `orchestration/ast-universal-20260222-001/cross-pollination/barrier-1/` |
| After (ENG) | ENG Phase 1 (eng-architect) |
| After (RED) | RED Phase 1 (red-lead) |
| Quality Gate | QG-B1 (C4 tournament, >= 0.95) |

**eng -> red handoff:**
- Threat model findings inform red team targeting priorities
- Trust boundary diagram defines attack surface boundaries
- STRIDE/DREAD scores prioritize vulnerability analysis focus areas
- Artifact: `cross-pollination/barrier-1/eng-to-red/handoff.md`

**red -> eng handoff:**
- Scope document confirms attack surface boundaries for architecture
- Rules of engagement constrain engineering decisions (what must be defended)
- Technique allowlist informs defensive design priorities
- Artifact: `cross-pollination/barrier-1/red-to-eng/handoff.md`

**Barrier 1 Quality Gate (QG-B1):**
- Threshold: >= 0.95
- All 10 strategies executed via concurrent adv-executor background agents
- H-16: S-003 (Steelman) before S-002 (Devil's Advocate)
- Max iterations: 5
- Gate artifact: `orchestration/ast-universal-20260222-001/quality/qg-b1/`

---

### Barrier 2: Implementation <-> Vulnerability Testing

| Field | Value |
|-------|-------|
| Barrier ID | `barrier-2` |
| Path | `orchestration/ast-universal-20260222-001/cross-pollination/barrier-2/` |
| After (ENG) | ENG Phase 3 (eng-backend) |
| After (RED) | RED Phase 2 (red-vuln) |
| Quality Gate | QG-B2 (C4 tournament, >= 0.95) |

**eng -> red handoff:**
- Implemented code for red team to test against
- New domain objects with their input validation boundaries
- CLI extension surface area
- Artifact: `cross-pollination/barrier-2/eng-to-red/handoff.md`

**red -> eng handoff:**
- Early vulnerability findings to inform remaining implementation hardening
- Specific input vectors that bypass current validation
- Priority-ordered list of vulnerabilities requiring immediate attention
- Artifact: `cross-pollination/barrier-2/red-to-eng/handoff.md`

**Barrier 2 Quality Gate (QG-B2):**
- Threshold: >= 0.95
- All 10 strategies executed via concurrent adv-executor background agents
- H-16: S-003 (Steelman) before S-002 (Devil's Advocate)
- Max iterations: 5
- Gate artifact: `orchestration/ast-universal-20260222-001/quality/qg-b2/`

---

### Barrier 3: Red Team Findings <-> Security Hardening

| Field | Value |
|-------|-------|
| Barrier ID | `barrier-3` |
| Path | `orchestration/ast-universal-20260222-001/cross-pollination/barrier-3/` |
| After (ENG) | ENG Phase 5 (eng-security) |
| After (RED) | RED Phase 3 (red-exploit) |
| Quality Gate | QG-B3 (C4 tournament, >= 0.95) |

**red -> eng handoff:**
- Exploitation findings with PoC evidence drive security hardening
- Validated vulnerability reproductions with impact assessment
- Priority-ordered remediation recommendations
- Artifact: `cross-pollination/barrier-3/red-to-eng/handoff.md`

**eng -> red handoff:**
- Security review findings for red team validation
- Defensive measures implemented for red team bypass testing
- Data flow analysis results for red team targeting
- Artifact: `cross-pollination/barrier-3/eng-to-red/handoff.md`

**Barrier 3 Quality Gate (QG-B3):**
- Threshold: >= 0.95
- All 10 strategies executed via concurrent adv-executor background agents
- H-16: S-003 (Steelman) before S-002 (Devil's Advocate)
- Max iterations: 5
- Gate artifact: `orchestration/ast-universal-20260222-001/quality/qg-b3/`

---

### Barrier 4: Final Synthesis

| Field | Value |
|-------|-------|
| Barrier ID | `barrier-4` |
| Path | `orchestration/ast-universal-20260222-001/cross-pollination/barrier-4/` |
| After (ENG) | ENG Phase 6 (eng-reviewer) |
| After (RED) | RED Phase 4 (red-reporter) |
| Quality Gate | QG-B4 (C4 tournament, >= 0.95, ALL 10 strategies) |

**Bidirectional synthesis:**
- Engineering quality gate report + red team engagement report merged into final synthesis
- All findings cross-referenced: security review vs. exploitation results
- Release readiness conditioned on both pipelines passing
- Artifact: `cross-pollination/barrier-4/synthesis/final-synthesis.md`

**Barrier 4 Quality Gate (QG-B4):**
- Threshold: >= 0.95
- ALL 10 strategies executed via concurrent adv-executor background agents
- H-16: S-003 (Steelman) before S-002 (Devil's Advocate)
- Max iterations: 5
- adv-executor agents run as individual background Task agents
- All 10 executors run concurrently; findings aggregated by adv-scorer
- Creator receives consolidated feedback for revision
- Gate artifact: `orchestration/ast-universal-20260222-001/quality/qg-b4/`
- Final synthesis artifact: `orchestration/ast-universal-20260222-001/synthesis/final-synthesis.md`

---

## Agent Registry

### Engineering Pipeline Agents

| Agent ID | Agent | Skill | Phase | Model | Tier | Status |
|----------|-------|-------|-------|-------|------|--------|
| `eng-architect-001` | eng-architect | /eng-team | ENG Phase 1 | opus | T3 | PLANNED |
| `eng-lead-001` | eng-lead | /eng-team | ENG Phase 2 | opus | T3 | PLANNED |
| `eng-backend-001` | eng-backend | /eng-team | ENG Phase 3 | sonnet | T3 | PLANNED |
| `eng-qa-001` | eng-qa | /eng-team | ENG Phase 4 | sonnet | T3 | PLANNED |
| `eng-security-001` | eng-security | /eng-team | ENG Phase 5 | opus | T3 | PLANNED |
| `eng-reviewer-001` | eng-reviewer | /eng-team | ENG Phase 6 | opus | T3 | PLANNED |

### Red Team Pipeline Agents

| Agent ID | Agent | Skill | Phase | Model | Tier | Status |
|----------|-------|-------|-------|-------|------|--------|
| `red-lead-001` | red-lead | /red-team | RED Phase 1 | opus | T3 | PLANNED |
| `red-vuln-001` | red-vuln | /red-team | RED Phase 2 | opus | T3 | PLANNED |
| `red-exploit-001` | red-exploit | /red-team | RED Phase 3 | opus | T3 | PLANNED |
| `red-reporter-001` | red-reporter | /red-team | RED Phase 4 | opus | T3 | PLANNED |

### Adversary Agents (Per Quality Gate)

| Agent ID | Agent | Skill | Purpose | Model | Execution |
|----------|-------|-------|---------|-------|-----------|
| `adv-selector-{gate}` | adv-selector | /adversary | Strategy selection per criticality | opus | Sequential (first) |
| `adv-executor-s001-{gate}` | adv-executor | /adversary | S-001 Red Team Analysis | sonnet | Background concurrent |
| `adv-executor-s002-{gate}` | adv-executor | /adversary | S-002 Devil's Advocate | sonnet | Background concurrent |
| `adv-executor-s003-{gate}` | adv-executor | /adversary | S-003 Steelman Technique | sonnet | Background concurrent |
| `adv-executor-s004-{gate}` | adv-executor | /adversary | S-004 Pre-Mortem Analysis | sonnet | Background concurrent |
| `adv-executor-s007-{gate}` | adv-executor | /adversary | S-007 Constitutional AI Critique | sonnet | Background concurrent |
| `adv-executor-s010-{gate}` | adv-executor | /adversary | S-010 Self-Refine | sonnet | Background concurrent |
| `adv-executor-s011-{gate}` | adv-executor | /adversary | S-011 Chain-of-Verification | sonnet | Background concurrent |
| `adv-executor-s012-{gate}` | adv-executor | /adversary | S-012 FMEA | sonnet | Background concurrent |
| `adv-executor-s013-{gate}` | adv-executor | /adversary | S-013 Inversion Technique | sonnet | Background concurrent |
| `adv-executor-s014-{gate}` | adv-executor | /adversary | S-014 LLM-as-Judge | sonnet | Background concurrent |
| `adv-scorer-{gate}` | adv-scorer | /adversary | Aggregate scoring | opus | Sequential (last) |

**Note:** `{gate}` is replaced with `b1`, `b2`, `b3`, `b4` for each barrier quality gate. Total adversary agent invocations: 12 per gate x 4 gates = 48 adversary agent invocations across the workflow.

---

## Quality Gate Definitions

### Gate Configuration (All Gates)

| Parameter | Value | Source |
|-----------|-------|--------|
| Criticality | C4 (Critical) | User-specified |
| Threshold | >= 0.95 | User-specified (above H-13 standard 0.92) |
| Max iterations | 5 | User-specified (above H-14 minimum 3) |
| Min iterations | 3 | H-14 |
| Strategies | All 10 selected | C4 tournament requirement |
| H-16 ordering | S-003 before S-002 | HARD rule |
| Plateau detection | Delta < 0.01 for 3 consecutive iterations | Circuit breaker |

### Strategy Execution Order (Per Iteration)

H-16 mandates S-003 (Steelman) before S-002 (Devil's Advocate). The full execution order:

| Order | Strategy | ID | Score Weight | Execution Model |
|-------|----------|----|-------------|-----------------|
| 1 | Self-Refine | S-010 | 4.00 | Background concurrent |
| 2 | Steelman Technique | S-003 | 4.30 | Background concurrent |
| 3 | Constitutional AI Critique | S-007 | 4.15 | Background concurrent |
| 4 | Devil's Advocate | S-002 | 4.10 | Background concurrent (after S-003) |
| 5 | Pre-Mortem Analysis | S-004 | 4.10 | Background concurrent |
| 6 | Inversion Technique | S-013 | 4.25 | Background concurrent |
| 7 | FMEA | S-012 | 3.75 | Background concurrent |
| 8 | Chain-of-Verification | S-011 | 3.75 | Background concurrent |
| 9 | Red Team Analysis | S-001 | 3.35 | Background concurrent |
| 10 | LLM-as-Judge | S-014 | 4.40 | Sequential (final scorer) |

**Execution model:** Strategies 1-9 run as individual adv-executor background Task agents concurrently. S-003 must complete before S-002 starts (H-16). S-014 (LLM-as-Judge) runs last via adv-scorer to produce the composite score incorporating all strategy findings.

### Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.20 | All required elements present |
| Internal Consistency | 0.20 | No contradictions, coherent narrative |
| Methodological Rigor | 0.20 | Sound methodology, defensible approach |
| Evidence Quality | 0.15 | Citations, data, empirical support |
| Actionability | 0.15 | Clear next steps, implementable |
| Traceability | 0.10 | Requirements traced to implementation |

### Gate Outcome Bands

| Band | Score Range | Outcome | Workflow Action |
|------|------------|---------|-----------------|
| PASS | >= 0.95 | Accepted | Phase proceeds to next barrier |
| REVISE | 0.85 - 0.94 | Rejected (H-13) | Creator receives consolidated findings, revision cycle continues (up to 5 iterations) |
| REJECTED | < 0.85 | Rejected (H-13) | Significant rework required, escalate to user |

### Per-Gate Specifics

| Gate | Barrier | Scope | Special Considerations |
|------|---------|-------|----------------------|
| QG-B1 | Barrier 1 | Threat model + scope document | Architecture decisions must be defensible; scope must be complete |
| QG-B2 | Barrier 2 | Implementation + vulnerability assessment | Code quality + security analysis cross-validated |
| QG-B3 | Barrier 3 | Exploitation results + security review | PoC evidence quality critical; remediation completeness |
| QG-B4 | Barrier 4 | Quality gate report + engagement report | Final synthesis; release readiness; all findings resolved |

---

## Adversary Quality Configuration

### C4 Tournament Model

```
 CREATOR (phase agent)
     |
     v  Produces deliverable
     |
 ADV-SELECTOR
     |  Selects all 10 strategies (C4)
     v
 +------------------------------------------+
 |  CONCURRENT ADV-EXECUTOR AGENTS (Task)   |
 |                                          |
 |  [S-010] Self-Refine          (bg)       |
 |  [S-003] Steelman             (bg)       |
 |  [S-007] Constitutional       (bg)       |
 |  [S-002] Devil's Advocate     (bg)*      |
 |  [S-004] Pre-Mortem           (bg)       |
 |  [S-013] Inversion            (bg)       |
 |  [S-012] FMEA                 (bg)       |
 |  [S-011] Chain-of-Verify      (bg)       |
 |  [S-001] Red Team             (bg)       |
 |                                          |
 |  * S-002 waits for S-003 (H-16)         |
 +------------------------------------------+
     |
     v  All findings aggregated
     |
 ADV-SCORER (S-014 LLM-as-Judge)
     |
     v  Composite score
     |
 +--- >= 0.95 ---> PASS (proceed)
 |
 +--- 0.85-0.94 --> REVISE (findings -> creator, iterate)
 |
 +--- < 0.85 -----> REJECTED (escalate to user)
```

### Iteration Flow

1. Creator produces deliverable
2. adv-selector identifies C4 -> all 10 strategies
3. 10 adv-executor agents launched as background Task agents (S-003 before S-002 per H-16)
4. All findings aggregated
5. adv-scorer produces composite score via S-014 LLM-as-Judge
6. If PASS (>= 0.95): barrier proceeds
7. If REVISE (0.85-0.94): consolidated findings sent to creator for revision; cycle repeats (max 5 iterations)
8. If REJECTED (< 0.85): escalate to user with current best result
9. Plateau detection: if score delta < 0.01 for 3 consecutive iterations, halt and escalate

---

## Path Scheme

All artifact paths use dynamic identifiers. No hardcoded pipeline names.

| Path Category | Template | Example |
|---------------|----------|---------|
| Base | `orchestration/ast-universal-20260222-001/` | -- |
| Eng pipeline | `orchestration/ast-universal-20260222-001/eng/{phase}/` | `.../eng/phase-1-architecture/` |
| Eng agent | `orchestration/ast-universal-20260222-001/eng/{phase}/{agent}/` | `.../eng/phase-1-architecture/eng-architect/` |
| Red pipeline | `orchestration/ast-universal-20260222-001/red/{phase}/` | `.../red/phase-1-scope/` |
| Red agent | `orchestration/ast-universal-20260222-001/red/{phase}/{agent}/` | `.../red/phase-1-scope/red-lead/` |
| Barrier | `orchestration/ast-universal-20260222-001/cross-pollination/{barrier}/` | `.../cross-pollination/barrier-1/` |
| Barrier direction | `orchestration/ast-universal-20260222-001/cross-pollination/{barrier}/{direction}/` | `.../cross-pollination/barrier-1/eng-to-red/` |
| Quality gate | `orchestration/ast-universal-20260222-001/quality/{gate}/` | `.../quality/qg-b1/` |
| Synthesis | `orchestration/ast-universal-20260222-001/synthesis/` | -- |

All paths are relative to `projects/PROJ-005-markdown-ast/`.

---

## State Management

### ORCHESTRATION.yaml

Machine-readable state file at `projects/PROJ-005-markdown-ast/ORCHESTRATION.yaml`. Contains:

| Section | Contents |
|---------|----------|
| `workflow` | ID, status, patterns, prerequisites, constraints |
| `quality` | C4 tournament config, dimensions, thresholds, gate scores |
| `paths` | Dynamic path templates |
| `pipelines` | Eng and red phase definitions with agents and dependencies |
| `barriers` | Cross-pollination barrier definitions with handoff directions |
| `quality_gates` | Per-barrier gate status, iterations, scores |
| `agents` | Full agent registry with status tracking |
| `execution_queue` | Ordered execution groups with dependencies |
| `checkpoints` | Recovery checkpoint log |
| `metrics` | Execution, quality, coverage, timing metrics |
| `blockers` | Active blockers |
| `next_actions` | Immediate and subsequent actions |
| `resumption` | Current state and next step for session recovery |

### Checkpoint Strategy

| Event | Checkpoint Action |
|-------|-------------------|
| Phase completion | Store phase summary + artifacts |
| Barrier sync | Store barrier handoff data |
| Quality gate iteration | Store iteration score + findings |
| Quality gate pass | Store final score + gate status |
| Agent failure | Store failure context + recovery instructions |

---

## Execution Constraints

### Constitutional Constraints (HARD)

| ID | Constraint | Impact on This Workflow |
|----|-----------|------------------------|
| H-01/P-003 | Single-level nesting only | Orchestrator -> worker agents only; workers do not spawn sub-workers |
| H-02/P-020 | User authority | User approves quality gates, escalations, and final release |
| H-03/P-022 | No deception | All scores, findings, and limitations reported honestly |
| H-05 | UV-only Python | `uv run` for execution, `uv add` for dependencies |
| H-07 | Hexagonal architecture | Domain layer imports only from domain; new parsers in domain layer |
| H-10 | One class per file | Each new domain object in its own file |
| H-11 | Type hints + docstrings | All public functions in new code |
| H-13 | Quality >= 0.92 (overridden to 0.95) | C4 tournament at every barrier |
| H-14 | Creator-critic-revision (3 min) | Minimum 3 iterations per quality gate |
| H-16 | Steelman before critique | S-003 before S-002 in every cycle |
| H-20 | BDD test-first, 90% coverage | Tests written before implementation |
| H-33 | AST-based parsing | No regex for frontmatter extraction |
| H-34 | Agent definition schema | New agent definitions must validate against schema |
| H-36 | Circuit breaker (3 hops max) | Routing depth enforced across barriers |

### Auto-Escalation Applicable

| Rule | Condition | Status |
|------|-----------|--------|
| AE-002 | Touches `.context/rules/` | Already C4 (above auto-C3 minimum) |
| AE-005 | Security-relevant code | Already C4 (above auto-C3 minimum) |

---

## Success Criteria

### Workflow-Level Exit Criteria

- [ ] All 10 file types parseable with correct frontmatter extraction
- [ ] All 10 file types have schema validation
- [ ] Document type auto-detection working for all supported paths
- [ ] YAML frontmatter parsing via `safe_load` only
- [ ] XML-tag section extraction for agent definitions
- [ ] HTML comment metadata extraction for ADRs
- [ ] CLI commands extended for all document types
- [ ] 90% line coverage on all new modules (H-20)
- [ ] Zero security findings at Critical or High severity unresolved
- [ ] Full existing test suite passes (no regression)
- [ ] All 4 barrier quality gates passed at >= 0.95
- [ ] Final synthesis document produced
- [ ] Release readiness: GO with evidence

### Per-Pipeline Exit Criteria

**Engineering:**
- [ ] Architecture ADR published and reviewed
- [ ] Threat model complete with STRIDE/DREAD
- [ ] All domain objects implemented with BDD test-first
- [ ] Security review complete with no unresolved Critical/High findings
- [ ] Quality gate report: GO

**Red Team:**
- [ ] Scope document published (RED-XXXX format)
- [ ] Vulnerability assessment complete with CVE/CWE mappings
- [ ] Exploitation testing complete with PoC evidence
- [ ] Engagement report published with remediation roadmap
- [ ] Scope compliance attestation: IN-SCOPE

---

## Risk Register

| Risk ID | Risk | Probability | Impact | Mitigation |
|---------|------|-------------|--------|------------|
| R-001 | YAML deserialization vulnerability | Medium | Critical | Enforce `safe_load` everywhere; red team validates |
| R-002 | XML parser DoS via deeply nested structures | Medium | High | Implement nesting depth limits; fuzz testing |
| R-003 | Path traversal via frontmatter fields | Low | Critical | Validate all paths against allowlist; no `..` components |
| R-004 | Regression in existing tests | Medium | High | Full test suite run at every phase gate |
| R-005 | Context budget exhaustion during C4 tournament | Medium | Medium | CB-02 tool result limit; checkpoint frequently |
| R-006 | Schema design locks in wrong structure | Low | Critical | C4 review of schema before implementation begins |
| R-007 | markdown-it-py plugin limitations for XML tags | Medium | High | PoC XML extraction before committing to approach |
| R-008 | Quality gate plateau (score stalls below 0.95) | Low | Medium | Plateau detection circuit breaker; escalate to user |

---

## Recovery Strategies

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Agent fails mid-phase | Agent status = FAILED in ORCHESTRATION.yaml | Retry with same inputs; if 2nd failure, escalate to user |
| Quality gate fails 5 iterations | Iteration count = 5, score < 0.95 | Escalate to user with best result + all findings |
| Quality gate plateau | Score delta < 0.01 for 3 iterations | Circuit breaker; present current best; ask user guidance |
| Barrier sync deadlock | Both pipelines blocked waiting for each other | Break deadlock: engineering proceeds with assumptions; red team validates later |
| Context budget exceeded | AE-006c/d activation | Auto-checkpoint; reduce verbosity; warn user |
| Test regression | Existing tests fail after new code | Revert new code; investigate; fix before proceeding |
| Session interruption | Incomplete phase in ORCHESTRATION.yaml | Resume from last checkpoint; re-read ORCHESTRATION.yaml |

---

## Resumption Context

| Field | Value |
|-------|-------|
| Last checkpoint | None (workflow not started) |
| Current state | PLANNED -- both pipelines ready to begin |
| Next step | Dispatch ENG Phase 1 (eng-architect) and RED Phase 1 (red-lead) in parallel |

**Files to read on resumption:**
1. `projects/PROJ-005-markdown-ast/ORCHESTRATION_PLAN.md` (this file)
2. `projects/PROJ-005-markdown-ast/ORCHESTRATION.yaml` (machine-readable state)
3. `src/domain/markdown_ast/` (current implementation)
4. `src/interface/cli/ast_commands.py` (current CLI)

**Key reference files:**
- `projects/PROJ-005-markdown-ast/orchestration/feat001-impl-20260220-001/ORCHESTRATION.yaml` (prior workflow, COMPLETE)
- `docs/schemas/agent-definition-v1.schema.json` (agent definition JSON Schema)
- `.context/rules/agent-development-standards.md` (agent format standards)

---

## Disclaimer

> **Agent-generated content.** This orchestration plan was produced by the `orch-planner` agent (v2.2.0) within the Jerry Framework. All architectural decisions, phase definitions, quality gate configurations, and risk assessments are recommendations subject to human review and approval. The criticality level (C4) and quality threshold (>= 0.95) were specified by the user. Constitutional constraints (P-003, P-020, P-022) and HARD rules (H-01 through H-36) are enforced by the framework and cannot be overridden by this plan.
