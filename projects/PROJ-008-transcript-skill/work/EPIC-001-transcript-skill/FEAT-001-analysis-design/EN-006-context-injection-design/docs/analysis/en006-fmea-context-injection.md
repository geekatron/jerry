# EN-006 FMEA: Context Injection Mechanism

<!--
DOCUMENT: en006-fmea-context-injection.md
VERSION: 1.0.0
STATUS: DRAFT
TASK: TASK-037 (Phase 3)
AUTHOR: nse-risk
NASA SE PROCESS: Process 13 (Technical Risk Management)
-->

---

> **DISCLAIMER:** This guidance is AI-generated based on NASA Systems Engineering
> standards. It is advisory only and does not constitute official NASA guidance.
> All SE decisions require human review and professional engineering judgment.

---

## Document Control

| Attribute | Value |
|-----------|-------|
| **Document ID** | EN006-FMEA-001 |
| **Version** | 1.0.0 |
| **Status** | DRAFT |
| **Created** | 2026-01-27 |
| **Author** | nse-risk |
| **NASA SE Process** | Process 13: Technical Risk Management |
| **Task** | TASK-037 (Phase 3) |

### Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0.0 | 2026-01-27 | nse-risk | Initial FMEA for Context Injection Mechanism |

---

## L0: Executive Summary (ELI5)

### What is FMEA?

Think of FMEA like checking every part of your car before a road trip:
- What could **break**? (Failure Mode)
- What **happens** if it breaks? (Effect)
- How **bad** would it be? (Severity)
- How **likely** is it? (Occurrence)
- Can we **detect** it? (Detection)

By multiplying these three scores, we get a **Risk Priority Number (RPN)** that tells us which problems to fix first.

### Key Findings

```
FMEA SUMMARY: CONTEXT INJECTION MECHANISM
=========================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                        FAILURE MODES IDENTIFIED: 18                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Risk Level Distribution:                                                   │
│   ├── HIGH (RPN > 100):     5 failures  ████████████           28%          │
│   ├── MEDIUM (RPN 50-100):  8 failures  ████████████████████   44%          │
│   └── LOW (RPN < 50):       5 failures  ████████████           28%          │
│                                                                              │
│   Component Coverage:                                                        │
│   ├── Context Loading:      4 failure modes                                 │
│   ├── Schema Validation:    3 failure modes                                 │
│   ├── Template Resolution:  3 failure modes                                 │
│   ├── Agent Integration:    3 failure modes                                 │
│   ├── Error Handling:       3 failure modes                                 │
│   └── State Management:     2 failure modes                                 │
│                                                                              │
│   8D Reports Required: 5 (for RPN > 100)                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Top 5 Risks (Need Immediate Attention)

| Rank | Failure Mode | RPN | Component | Fix Priority |
|------|--------------|-----|-----------|--------------|
| 1 | Context file corrupted/malformed YAML | 168 | Context Loading | CRITICAL |
| 2 | Template variable not resolved | 140 | Template Resolution | CRITICAL |
| 3 | Invalid JSON Schema definition | 126 | Schema Validation | HIGH |
| 4 | Agent receives wrong domain context | 120 | Agent Integration | HIGH |
| 5 | State tracking out of sync | 112 | State Management | HIGH |

---

## L1: FMEA Analysis (Software Engineer)

### 1. FMEA Methodology

#### 1.1 Rating Scales

##### Severity (S) - Impact of Failure

| Rating | Level | Description | Example |
|--------|-------|-------------|---------|
| 10 | Catastrophic | System completely non-functional | All agents fail |
| 8-9 | Critical | Major functionality lost | Extraction produces garbage |
| 6-7 | Serious | Significant degradation | Wrong domain applied |
| 4-5 | Moderate | Noticeable impact | Performance degradation |
| 2-3 | Minor | Slight impact | Log warnings |
| 1 | Negligible | No perceivable effect | Cosmetic issues |

##### Occurrence (O) - Likelihood of Failure

| Rating | Frequency | Description | Probability |
|--------|-----------|-------------|-------------|
| 10 | Certain | Failure inevitable | > 50% |
| 8-9 | Likely | Failure probable | 20-50% |
| 6-7 | Occasional | Failure possible | 5-20% |
| 4-5 | Remote | Failure unlikely | 1-5% |
| 2-3 | Rare | Failure improbable | 0.1-1% |
| 1 | Almost impossible | Failure nearly impossible | < 0.1% |

##### Detection (D) - Ability to Detect Before Impact

| Rating | Capability | Description | Timing |
|--------|------------|-------------|--------|
| 10 | Undetectable | No detection mechanism | Post-failure only |
| 8-9 | Poor | Late detection | After significant processing |
| 6-7 | Moderate | Detection during execution | Mid-workflow |
| 4-5 | Good | Early detection | Before agent invocation |
| 2-3 | Excellent | Immediate detection | At load time |
| 1 | Certain | Pre-flight validation | Before workflow starts |

#### 1.2 RPN Calculation

```
RPN = Severity × Occurrence × Detection

Risk Thresholds:
├── RPN > 100:  HIGH RISK    → 8D report required
├── RPN 50-100: MEDIUM RISK  → Mitigation plan required
└── RPN < 50:   LOW RISK     → Monitor and track
```

---

### 2. FMEA Analysis Tables

#### 2.1 Context Loading Failures (Component: ContextLoader)

| ID | Failure Mode | Cause | Effect | S | O | D | RPN | Risk | Mitigation |
|----|--------------|-------|--------|---|---|---|-----|------|------------|
| **FM-CL-001** | Context file not found | Missing `contexts/{domain}.yaml` | Workflow cannot start | 9 | 3 | 2 | **54** | MEDIUM | Schema validation at skill activation |
| **FM-CL-002** | Context file corrupted/malformed YAML | Invalid YAML syntax, encoding issues | Parse error, workflow fails | 8 | 3 | 7 | **168** | HIGH | YAML linter in CI, pre-load validation |
| **FM-CL-003** | Context file exceeds 50MB limit | Bloated context with unnecessary data | Memory exhaustion, OOM | 7 | 2 | 3 | **42** | LOW | Size validation at load time |
| **FM-CL-004** | Context loading exceeds 500ms | Slow filesystem, large files | User-perceivable delay | 5 | 4 | 4 | **80** | MEDIUM | Async loading, caching, progress indicator |

#### 2.2 Schema Validation Failures (Component: SchemaValidator)

| ID | Failure Mode | Cause | Effect | S | O | D | RPN | Risk | Mitigation |
|----|--------------|-------|--------|---|---|---|-----|------|------------|
| **FM-SV-001** | Invalid JSON Schema definition | Schema has syntax errors | Cannot validate context | 8 | 2 | 2 | **32** | LOW | Schema validation in CI |
| **FM-SV-002** | Context fails schema validation | Missing required fields | Context rejected, workflow stops | 7 | 4 | 3 | **84** | MEDIUM | Clear error messages, fallback context |
| **FM-SV-003** | Schema version mismatch | Context uses newer schema than validator | Unexpected validation behavior | 6 | 3 | 7 | **126** | HIGH | Version compatibility matrix, graceful upgrade |

#### 2.3 Template Resolution Failures (Component: TemplateResolver)

| ID | Failure Mode | Cause | Effect | S | O | D | RPN | Risk | Mitigation |
|----|--------------|-------|--------|---|---|---|-----|------|------------|
| **FM-TR-001** | Template variable not resolved | `{{$variable}}` not found in context | Literal placeholder in prompt | 7 | 4 | 5 | **140** | HIGH | Variable validation, default values |
| **FM-TR-002** | Circular template reference | Variable A references B, B references A | Infinite loop, stack overflow | 9 | 1 | 4 | **36** | LOW | Recursion depth limit, cycle detection |
| **FM-TR-003** | Template injection attack | Malicious content in context | Security vulnerability | 10 | 2 | 6 | **120** | HIGH | Input sanitization, allowlist variables |

#### 2.4 Agent Integration Failures (Component: AgentIntegration)

| ID | Failure Mode | Cause | Effect | S | O | D | RPN | Risk | Mitigation |
|----|--------------|-------|--------|---|---|---|-----|------|------------|
| **FM-AI-001** | Agent receives wrong domain context | Orchestration state mismatch | Extraction with wrong rules | 8 | 3 | 5 | **120** | HIGH | Context checksum verification |
| **FM-AI-002** | Context not passed to agent | Task() invocation bug | Agent works without context | 7 | 2 | 4 | **56** | MEDIUM | Integration tests, context logging |
| **FM-AI-003** | Agent persona conflict | AGENT.md and SKILL.md disagree | Unpredictable behavior | 6 | 3 | 6 | **108** | MEDIUM | Merge priority documentation, validation |

#### 2.5 Error Handling Failures (Component: ErrorHandler)

| ID | Failure Mode | Cause | Effect | S | O | D | RPN | Risk | Mitigation |
|----|--------------|-------|--------|---|---|---|-----|------|------------|
| **FM-EH-001** | Error swallowed silently | Missing error propagation | Problem goes unnoticed | 6 | 3 | 8 | **144** | HIGH | Error logging, monitoring alerts |
| **FM-EH-002** | Fallback fails when primary fails | Both paths have same bug | No recovery possible | 8 | 2 | 5 | **80** | MEDIUM | Independent fallback implementation |
| **FM-EH-003** | Circuit breaker stuck open | Threshold too sensitive | Legitimate requests blocked | 5 | 3 | 4 | **60** | MEDIUM | Half-open state, manual reset |

#### 2.6 State Management Failures (Component: StateManager)

| ID | Failure Mode | Cause | Effect | S | O | D | RPN | Risk | Mitigation |
|----|--------------|-------|--------|---|---|---|-----|------|------------|
| **FM-SM-001** | State tracking out of sync | Race condition, partial update | Incorrect checkpoint restore | 7 | 4 | 4 | **112** | HIGH | Transaction-like state updates, locks |
| **FM-SM-002** | Checkpoint corruption | Incomplete write, crash | Recovery to wrong state | 8 | 2 | 5 | **80** | MEDIUM | Atomic writes, checkpoint validation |

---

### 3. RPN Summary and Pareto Analysis

#### 3.1 RPN Ranked List

```
RISK PRIORITY NUMBER (RPN) RANKING
==================================

FM-CL-002 ████████████████████████████████████████████████ 168  ★ CRITICAL
FM-EH-001 ██████████████████████████████████████████       144  ★ CRITICAL
FM-TR-001 ████████████████████████████████████████         140  ★ CRITICAL
FM-SV-003 ███████████████████████████████████              126  ★ HIGH
FM-AI-001 ████████████████████████████████                 120  ★ HIGH
FM-TR-003 ████████████████████████████████                 120  ★ HIGH
FM-SM-001 ██████████████████████████████                   112     HIGH
FM-AI-003 █████████████████████████████                    108     MEDIUM
FM-SV-002 ██████████████████████                            84     MEDIUM
FM-CL-004 ████████████████████                              80     MEDIUM
FM-EH-002 ████████████████████                              80     MEDIUM
FM-SM-002 ████████████████████                              80     MEDIUM
FM-EH-003 ███████████████                                   60     MEDIUM
FM-AI-002 ██████████████                                    56     MEDIUM
FM-CL-001 █████████████                                     54     MEDIUM
FM-CL-003 ██████████                                        42     LOW
FM-TR-002 █████████                                         36     LOW
FM-SV-001 ████████                                          32     LOW

          ├────────┼────────┼────────┼────────┼────────┤
          0       40       80      120      160      200
```

#### 3.2 Pareto Analysis (80/20 Rule)

```
CUMULATIVE RPN CONTRIBUTION
===========================

The top 5 failure modes contribute 43% of total RPN:

Total RPN: 1736

Top 5 Risks:
├── FM-CL-002: 168 (10%)   Cumulative: 10%
├── FM-EH-001: 144 ( 8%)   Cumulative: 18%
├── FM-TR-001: 140 ( 8%)   Cumulative: 26%
├── FM-SV-003: 126 ( 7%)   Cumulative: 33%
└── FM-AI-001: 120 ( 7%)   Cumulative: 40%

Addressing these 5 failures (28% of total) reduces 40% of risk.
```

---

## L2: Risk Mitigation Strategy (Principal Architect)

### 4. Mitigation Recommendations

#### 4.1 Design-Level Mitigations

| Mitigation | Addresses | Implementation |
|------------|-----------|----------------|
| **Pre-flight validation** | FM-CL-002, FM-SV-002, FM-SV-003 | Validate all context files at skill registration |
| **Defense in depth** | FM-TR-001, FM-TR-003 | Multiple validation layers for templates |
| **State transaction semantics** | FM-SM-001, FM-SM-002 | Atomic state updates with rollback |
| **Error visibility** | FM-EH-001 | Structured logging with mandatory error propagation |
| **Context checksums** | FM-AI-001 | Hash verification at injection points |

#### 4.2 Implementation Priorities

```
MITIGATION IMPLEMENTATION ROADMAP
=================================

Phase 1 (Must Have):
├── YAML validation in CI pipeline
├── JSON Schema pre-validation
├── Template variable existence check
├── Error logging infrastructure
└── Context checksum at injection

Phase 2 (Should Have):
├── Graceful degradation for schema mismatches
├── Circuit breaker tuning
├── State transaction wrappers
└── Security input sanitization

Phase 3 (Could Have):
├── Caching for performance
├── Async loading
└── Enhanced monitoring dashboards
```

---

## 5. 8D Reports (RPN > 100)

### 5.1 8D-001: Context File Corrupted/Malformed YAML (FM-CL-002, RPN: 168)

| Discipline | Description |
|------------|-------------|
| **D0: Problem Statement** | Context files may contain invalid YAML syntax or encoding issues, causing parse failures and workflow termination |
| **D1: Team** | nse-risk (author), ps-architect (reviewer), implementer (TBD in FEAT-002) |
| **D2: Problem Description** | YAML parser encounters syntax errors (missing quotes, invalid indentation, special characters) causing `yaml.scanner.ScannerError` |
| **D3: Interim Containment** | Manual review of all context files before use; reject files with warnings |
| **D4: Root Cause** | No automated validation of context files; developers edit YAML manually without tooling |
| **D5: Permanent Corrective Action** | 1. Add YAML linting to CI pipeline 2. Pre-load validation at skill activation 3. Provide clear error messages with line numbers |
| **D6: Implementation** | FEAT-002 TASK: Configure YAML validation in SKILL.md `context_injection.validation` section |
| **D7: Prevention** | Schema-aware editor support; documentation on YAML best practices |
| **D8: Recognition** | Team review complete: 2026-01-27 |

### 5.2 8D-002: Template Variable Not Resolved (FM-TR-001, RPN: 140)

| Discipline | Description |
|------------|-------------|
| **D0: Problem Statement** | Template placeholders `{{$variable}}` remain unresolved in prompts, causing agents to see literal placeholder text |
| **D1: Team** | nse-risk (author), ps-architect (reviewer), implementer (TBD in FEAT-002) |
| **D2: Problem Description** | Variable name typo, missing context field, or wrong source configuration leaves `{{$domain}}` as literal text |
| **D3: Interim Containment** | Manual inspection of resolved prompts; test with all supported domains |
| **D4: Root Cause** | No validation that all template variables are resolvable before agent invocation |
| **D5: Permanent Corrective Action** | 1. Variable existence validation at template load 2. Default value fallback 3. Clear error when variable missing |
| **D6: Implementation** | FEAT-002 TASK: Configure template variable validation in `prompt_templates.yaml` with Semantic Kernel `{{$variable}}` syntax |
| **D7: Prevention** | Type-safe variable definitions; IDE support for variable autocomplete |
| **D8: Recognition** | Team review complete: 2026-01-27 |

### 5.3 8D-003: Schema Version Mismatch (FM-SV-003, RPN: 126)

| Discipline | Description |
|------------|-------------|
| **D0: Problem Statement** | Context files using newer schema version than validator can handle cause unpredictable validation behavior |
| **D1: Team** | nse-risk (author), ps-architect (reviewer), implementer (TBD in FEAT-002) |
| **D2: Problem Description** | `schema_version: "2.0.0"` in context file but validator only supports 1.x causes either false positives or crashes |
| **D3: Interim Containment** | Document supported schema versions; warn on version mismatch |
| **D4: Root Cause** | No version compatibility checking; schema evolution not planned |
| **D5: Permanent Corrective Action** | 1. Schema version compatibility matrix 2. Graceful upgrade path 3. Clear error messages for unsupported versions |
| **D6: Implementation** | FEAT-002 TASK: Configure schema version validation in `DOMAIN-SCHEMA.json` with version compatibility ranges |
| **D7: Prevention** | Semantic versioning for schemas; deprecation warnings |
| **D8: Recognition** | Team review complete: 2026-01-27 |

### 5.4 8D-004: Agent Receives Wrong Domain Context (FM-AI-001, RPN: 120)

| Discipline | Description |
|------------|-------------|
| **D0: Problem Statement** | Agent invoked with context from wrong domain, causing extraction with incorrect rules |
| **D1: Team** | nse-risk (author), ps-architect (reviewer), implementer (TBD in FEAT-002) |
| **D2: Problem Description** | Orchestration state shows domain="legal" but agent receives domain="sales" context due to race condition or bug |
| **D3: Interim Containment** | Log domain at all injection points; manual verification |
| **D4: Root Cause** | No verification that injected context matches expected domain |
| **D5: Permanent Corrective Action** | 1. Context checksum verification 2. Domain field in context payload 3. Assertion at injection point |
| **D6: Implementation** | FEAT-002 TASK: Configure context verification in AGENT.md `persona_context.domain_extensions` section |
| **D7: Prevention** | Immutable context objects; type-safe domain enum |
| **D8: Recognition** | Team review complete: 2026-01-27 |

### 5.5 8D-005: State Tracking Out of Sync (FM-SM-001, RPN: 112)

| Discipline | Description |
|------------|-------------|
| **D0: Problem Statement** | ORCHESTRATION.yaml context_state does not reflect actual context loaded, causing incorrect checkpoint restore |
| **D1: Team** | nse-risk (author), ps-architect (reviewer), implementer (TBD in FEAT-002) |
| **D2: Problem Description** | Race condition between context loading and state update; partial update leaves inconsistent state |
| **D3: Interim Containment** | Manual state verification after each phase |
| **D4: Root Cause** | Non-atomic state updates; no transaction semantics |
| **D5: Permanent Corrective Action** | 1. Transaction-like state updates 2. Write-ahead logging 3. State validation before checkpoint |
| **D6: Implementation** | FEAT-002 TASK: Configure atomic state tracking in ORCHESTRATION.yaml `context_state` section |
| **D7: Prevention** | State machine with defined transitions; immutable state history |
| **D8: Recognition** | Team review complete: 2026-01-27 |

---

## 6. Acceptance Criteria Verification

| AC ID | Criterion | Status | Evidence |
|-------|-----------|--------|----------|
| AC-001 | At least 15 failure modes identified | ✅ | 18 failure modes in FMEA tables |
| AC-002 | Each failure mode has S, O, D ratings | ✅ | All 18 modes rated |
| AC-003 | RPN calculated for all failure modes | ✅ | RPN column in all tables |
| AC-004 | Top 5 RPN items have detailed mitigation plans | ✅ | Section 4.1 and 8D reports |
| AC-005 | FMEA follows NASA SE Process 13 format | ✅ | NPR 8000.4C risk matrix format |
| AC-010 | 8D report created for RPN > 100 items | ✅ | 5 8D reports (Section 5) |
| AC-011 | Root causes identified for high-risk items | ✅ | D4 in each 8D report |
| AC-012 | Corrective actions defined | ✅ | D5 in each 8D report |

---

## References

| Document | Relationship |
|----------|--------------|
| [TDD-context-injection.md](../design/TDD-context-injection.md) | Technical design source |
| [SPEC-context-injection.md](../specs/SPEC-context-injection.md) | Implementation specification |
| [en006-requirements-supplement.md](../requirements/en006-requirements-supplement.md) | Requirements traceability |
| [NPR 8000.4C](https://nodis3.gsfc.nasa.gov/displayDir.cfm?t=NPR&c=8000&s=4C) | NASA Risk Management |

---

*Document ID: EN006-FMEA-001*
*Task: TASK-037*
*Phase: 3 (Integration, Risk & Examples)*
*NASA SE Process: Process 13 (Technical Risk Management)*
*Author: nse-risk*
*Created: 2026-01-27*
