# Self-Healing Architecture - Technical Reference

> **Version:** 2.1.0 (Initiative 19)
> **Audience:** Software Architects, Senior Engineers
> **Classification:** Technical Reference
> **Created:** 2026-01-04
> **Standard:** ECSS-E-ST-40C Software Documentation

---

## Abstract

This document provides the complete technical architecture for the Work Tracker Self-Healing capability, implementing autonomic computing principles (Kephart & Chess, 2003) with the MAPE-K control loop and defense-in-depth enforcement using the Chain of Responsibility pattern (Gamma et al., 1994).

---

## 1. Introduction

### 1.1 Purpose

Define the architectural design for self-healing capabilities in the Work Tracker skill, enabling:

1. **Automatic error detection and recovery** (MAPE-K)
2. **Consent-based operation control** (Four-Level Enforcement)
3. **Cascade failure prevention** (Circuit Breaker)
4. **Knowledge accumulation** (Learning from failures)

### 1.2 Scope

This architecture covers:
- Domain model for self-healing (value objects, entities, services)
- MAPE-K control loop implementation
- Four-Level Enforcement chain
- Integration with existing Work Tracker infrastructure

### 1.3 Definitions

| Term | Definition | Source |
|------|------------|--------|
| MAPE-K | Monitor-Analyze-Plan-Execute-Knowledge control loop | Kephart & Chess, 2003 |
| Circuit Breaker | Pattern to prevent cascading failures | Nygard, 2007 |
| SSOT | Single Source of Truth | Domain-Driven Design |
| ADR | Architecture Decision Record | Nygard, 2011 |

### 1.4 References

| ID | Reference |
|----|-----------|
| [1] | Kephart, J.O. & Chess, D.M. (2003). "The Vision of Autonomic Computing." IEEE Computer, 36(1), 41-50 |
| [2] | Gamma, E. et al. (1994). Design Patterns. Addison-Wesley |
| [3] | Nygard, M.T. (2007). Release It! Pragmatic Bookshelf |
| [4] | Fowler, M. (2002). Patterns of Enterprise Application Architecture. Addison-Wesley |
| [5] | Evans, E. (2003). Domain-Driven Design. Addison-Wesley |
| [6] | Freeman, S. & Pryce, N. (2009). Growing Object-Oriented Software, Guided by Tests. Addison-Wesley |

---

## 2. Architectural Overview

### 2.1 System Context

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Work Tracker System                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌───────────┐     ┌─────────────────────────────────────────────────┐ │
│   │  wt.py    │────>│          Self-Healing Subsystem                 │ │
│   │   CLI     │     │                                                 │ │
│   └───────────┘     │  ┌────────────────────────────────────────────┐│ │
│                     │  │           MAPE-K Control Loop               ││ │
│                     │  │                                             ││ │
│                     │  │  Monitor → Analyze → Plan → Execute         ││ │
│                     │  │              ↑                    │         ││ │
│                     │  │              └─── Knowledge ←─────┘         ││ │
│                     │  └────────────────────────────────────────────┘│ │
│                     │                                                 │ │
│                     │  ┌────────────────────────────────────────────┐│ │
│                     │  │        Four-Level Enforcement              ││ │
│                     │  │                                             ││ │
│                     │  │  Advisory → Soft → Medium → HARD            ││ │
│                     │  └────────────────────────────────────────────┘│ │
│                     │                                                 │ │
│                     │  ┌────────────────────────────────────────────┐│ │
│                     │  │        Stability Patterns                   ││ │
│                     │  │                                             ││ │
│                     │  │  CircuitBreaker  |  RetryPolicy             ││ │
│                     │  └────────────────────────────────────────────┘│ │
│                     └─────────────────────────────────────────────────┘ │
│                                                                          │
│   ┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐  │
│   │   JSON    │────>│ Commands  │────>│ Markdown  │────>│   File    │  │
│   │   SSOT    │     │  (CQRS)   │     │ Generator │     │  System   │  │
│   └───────────┘     └───────────┘     └───────────┘     └───────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Architectural Principles

1. **Autonomic Computing** [1]: System self-manages based on high-level goals
2. **Defense in Depth** [3]: Multiple layers of validation
3. **Fail-Fast** [3]: Detect failures early, fail predictably
4. **Single Responsibility** [2]: Each component has one reason to change
5. **Domain-Driven Design** [5]: Rich domain model with value objects

---

## 3. MAPE-K Control Loop

### 3.1 Theoretical Foundation

The MAPE-K (Monitor-Analyze-Plan-Execute-Knowledge) control loop is the cornerstone of autonomic computing, introduced by IBM researchers Kephart and Chess in 2003 [1].

**Key Properties:**
- **Closed-loop control**: Continuous feedback from Execute to Monitor
- **Knowledge-driven**: Decisions informed by accumulated experience
- **Self-optimization**: Performance improves over time

### 3.2 Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MAPE-K Components                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                      HealthMonitor (Monitor)                         ││
│  │                                                                      ││
│  │  Responsibilities:                                                   ││
│  │  - Track operation latency (sliding window)                          ││
│  │  - Calculate success rate (operations in window)                     ││
│  │  - Emit health status (HEALTHY, DEGRADED, UNHEALTHY, CRITICAL)       ││
│  │                                                                      ││
│  │  Metrics Collected:                                                  ││
│  │  - total_count: Operations in window                                 ││
│  │  - success_rate: ratio [0.0, 1.0]                                    ││
│  │  - failure_count: Failed operations                                  ││
│  │  - average_latency_ms: Mean response time                            ││
│  │  - p95_latency_ms: 95th percentile latency                           ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                     │                                    │
│                                     ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                    SymptomAnalyzer (Analyze)                         ││
│  │                                                                      ││
│  │  Responsibilities:                                                   ││
│  │  - Classify errors into categories                                   ││
│  │  - Determine root cause                                              ││
│  │  - Calculate diagnosis confidence                                    ││
│  │                                                                      ││
│  │  Error Categories:                                                   ││
│  │  - TRANSIENT: Temporary failures (network, rate limit)               ││
│  │  - VALIDATION: Input errors (bad status, invalid ID)                 ││
│  │  - RESOURCE: Missing resources (file not found)                      ││
│  │  - CORRUPTION: Data integrity issues                                 ││
│  │  - UNKNOWN: Unclassified errors                                      ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                     │                                    │
│                                     ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                   RemediationPlanner (Plan)                          ││
│  │                                                                      ││
│  │  Responsibilities:                                                   ││
│  │  - Select recovery strategy based on diagnosis                       ││
│  │  - Consider alternative strategies                                   ││
│  │  - Provide rationale for selection                                   ││
│  │                                                                      ││
│  │  Recovery Strategies:                                                ││
│  │  - RETRY: Exponential backoff with jitter [AWS]                      ││
│  │  - NORMALIZE: Transform invalid input                                ││
│  │  - REPAIR: Restore from backup                                       ││
│  │  - ESCALATE: Request human intervention                              ││
│  │  - CIRCUIT_BREAK: Temporarily halt operations                        ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                     │                                    │
│                                     ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                     ActionExecutor (Execute)                         ││
│  │                                                                      ││
│  │  Responsibilities:                                                   ││
│  │  - Execute recovery plan                                             ││
│  │  - Apply circuit breaker protection                                  ││
│  │  - Track execution metrics                                           ││
│  │  - Report outcome to knowledge base                                  ││
│  │                                                                      ││
│  │  Stability Patterns Applied:                                         ││
│  │  - Circuit Breaker [3]: Prevent cascade failures                     ││
│  │  - Retry with Backoff [AWS]: Handle transient failures               ││
│  │  - Timeout [3]: Bound waiting time                                   ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                     │                                    │
│                                     ▼                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                      KnowledgeBase (Knowledge)                       ││
│  │                                                                      ││
│  │  Responsibilities:                                                   ││
│  │  - Store failure patterns                                            ││
│  │  - Track recovery outcomes                                           ││
│  │  - Provide statistics for optimization                               ││
│  │                                                                      ││
│  │  Data Stored:                                                        ││
│  │  - Failure patterns by category                                      ││
│  │  - Recovery success rates by strategy                                ││
│  │  - Time-to-recovery metrics                                          ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Class Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        MAPE-K Domain Model                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Value Objects (Immutable):                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐   │
│  │    Symptom      │  │   Diagnosis     │  │   RemediationPlan       │   │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────────────┤   │
│  │ command: str    │  │ category: Enum  │  │ selected_strategy: Enum │   │
│  │ error: Exception│  │ root_cause: str │  │ rationale: str          │   │
│  │ context: dict   │  │ confidence: f64 │  │ alternatives: list      │   │
│  │ duration_ms: int│  │ symptom: Symptom│  │ diagnosis: Diagnosis    │   │
│  │ timestamp: dt   │  │ recommended:Enum│  │ timeout_ms: int         │   │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────┘   │
│                                                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐   │
│  │ExecutionResult  │  │  HealthMetrics  │  │    HealthStatus         │   │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────────────┤   │
│  │ success: bool   │  │ total_count: int│  │ overall: HealthLevel    │   │
│  │ action_taken:str│  │ success_rate:f64│  │ latency: HealthLevel    │   │
│  │ duration_ms: int│  │ failure_count:in│  │ error_rate: HealthLevel │   │
│  │ attempts: int   │  │ avg_latency: int│  │ timestamp: datetime     │   │
│  │ error: Optional │  │ p95_latency: int│  └─────────────────────────┘   │
│  └─────────────────┘  └─────────────────┘                                 │
│                                                                           │
│  Enumerations:                                                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐   │
│  │  ErrorCategory  │  │RecoveryStrategy │  │    HealthLevel          │   │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────────────┤   │
│  │ TRANSIENT       │  │ RETRY           │  │ HEALTHY                 │   │
│  │ VALIDATION      │  │ NORMALIZE       │  │ DEGRADED                │   │
│  │ RESOURCE        │  │ REPAIR          │  │ UNHEALTHY               │   │
│  │ CORRUPTION      │  │ ESCALATE        │  │ CRITICAL                │   │
│  │ UNKNOWN         │  │ CIRCUIT_BREAK   │  └─────────────────────────┘   │
│  └─────────────────┘  └─────────────────┘                                 │
│                                                                           │
│  Services (Stateful):                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                    SelfHealingDispatcher                             │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ + health_monitor: HealthMonitor                                      │ │
│  │ + symptom_analyzer: SymptomAnalyzer                                  │ │
│  │ + remediation_planner: RemediationPlanner                            │ │
│  │ + action_executor: ActionExecutor                                    │ │
│  │ + knowledge_base: KnowledgeBase                                      │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ + dispatch_natural(intent: str, tracker_path: str) → HealingResult   │ │
│  │ + dispatch_with_healing(intent: str, tracker_path: str) → HealingRes │ │
│  │ + create_default() → SelfHealingDispatcher [Factory]                 │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### 3.4 Sequence Diagram: Error Recovery

```
┌─────┐    ┌────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│User │    │ Dispatcher │    │ Monitor  │    │ Analyzer │    │ Planner  │    │ Executor │
└──┬──┘    └─────┬──────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
   │             │                │               │               │               │
   │ command     │                │               │               │               │
   │────────────>│                │               │               │               │
   │             │                │               │               │               │
   │             │ execute()      │               │               │               │
   │             │───────────────>│               │               │               │
   │             │                │               │               │               │
   │             │ ERROR!         │               │               │               │
   │             │<───────────────│               │               │               │
   │             │                │               │               │               │
   │             │ create Symptom │               │               │               │
   │             │─────────────────────────────>  │               │               │
   │             │                │               │               │               │
   │             │                │   analyze()   │               │               │
   │             │                │──────────────>│               │               │
   │             │                │               │               │               │
   │             │                │   Diagnosis   │               │               │
   │             │                │<──────────────│               │               │
   │             │                │               │               │               │
   │             │                │               │    plan()     │               │
   │             │                │               │──────────────>│               │
   │             │                │               │               │               │
   │             │                │               │RemediationPlan│               │
   │             │                │               │<──────────────│               │
   │             │                │               │               │               │
   │             │                │               │               │   execute()   │
   │             │                │               │               │──────────────>│
   │             │                │               │               │               │
   │             │                │               │               │ExecutionResult│
   │             │                │               │               │<──────────────│
   │             │                │               │               │               │
   │             │ HealingResult  │               │               │               │
   │             │<───────────────────────────────────────────────────────────────│
   │             │                │               │               │               │
   │ result      │                │               │               │               │
   │<────────────│                │               │               │               │
   │             │                │               │               │               │
```

---

## 4. Four-Level Enforcement

### 4.1 Design Pattern: Chain of Responsibility

The Four-Level Enforcement model implements the **Chain of Responsibility** pattern (Gamma et al., 1994 [2], p. 223):

> "Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it."

**Adaptation for Enforcement:**
- Each level can **allow** or **block** an operation
- First blocking level **terminates** the chain
- All levels record their decision in the result

### 4.2 Enforcement Levels

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Four-Level Enforcement Chain                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Level 1: ADVISORY                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Source: CLAUDE.md instructions                                      ││
│  │  Behavior: Returns recommendations, NEVER blocks                     ││
│  │  Override: Claude discretion                                         ││
│  │                                                                      ││
│  │  Example: "Consider checking existing initiatives before creating"   ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                              │ (always passes)                           │
│                              ▼                                           │
│  Level 2: SOFT                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Source: SKILL.md instructions via ConsentManager                    ││
│  │  Behavior: Blocks if consent not granted for sensitive operations    ││
│  │  Override: --skip-consent flag                                       ││
│  │                                                                      ││
│  │  Protected Operations:                                               ││
│  │  - create_initiative                                                 ││
│  │  - delete_tracker                                                    ││
│  │  - bulk_status_change                                                ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                              │ (blocks without consent)                  │
│                              ▼                                           │
│  Level 3: MEDIUM                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Source: Agent restrictions via AgentRestrictionEnforcer             ││
│  │  Behavior: Blocks subagent operations on protected resources         ││
│  │  Override: Parent agent approval                                     ││
│  │                                                                      ││
│  │  Blocked for Subagents:                                              ││
│  │  - create_initiative                                                 ││
│  │  - modify_consent_state                                              ││
│  │  - execute_hooks                                                     ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                              │ (blocks unauthorized agents)              │
│                              ▼                                           │
│  Level 4: HARD                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Source: PreToolUse hook via HookEnforcer                            ││
│  │  Behavior: Exit code 1 blocks tool call completely                   ││
│  │  Override: --user-approved flag + hook allowlist                     ││
│  │                                                                      ││
│  │  Hook: .claude/hooks/initiative_consent_hook.py                      ││
│  │  Triggers:                                                           ││
│  │  - Write to docs/plans/**/{new-id}-*.md                              ││
│  │  - Bash calls containing generate_tracker.py                         ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                              │ (blocks unauthorized tool calls)          │
│                              ▼                                           │
│                     ┌─────────────────┐                                  │
│                     │ OPERATION ALLOWED │                                │
│                     └─────────────────┘                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Enforcement Class Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Four-Level Enforcement Classes                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                     FourLevelEnforcer (Composite)                    │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ + advisory: AdvisoryLevel                                            │ │
│  │ + soft: ConsentManager                                               │ │
│  │ + medium: AgentRestrictionEnforcer                                   │ │
│  │ + hard: HookEnforcer                                                 │ │
│  ├─────────────────────────────────────────────────────────────────────┤ │
│  │ + check(op: str, ctx: EnforcementContext) → EnforcementResult        │ │
│  │ + get_level_order() → List[str]                                      │ │
│  │ + with_defaults() → FourLevelEnforcer [Factory]                      │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                           │ uses                                          │
│           ┌───────────────┼───────────────┬───────────────┐              │
│           ▼               ▼               ▼               ▼              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │AdvisoryLevel│  │ConsentMgr   │  │AgentRestrict│  │HookEnforcer │     │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤     │
│  │+check()     │  │+check()     │  │+check_op()  │  │+check_tool()│     │
│  │→Recommend   │  │→Block|Allow │  │→Block|Allow │  │→Block|Allow │     │
│  │ (no block)  │  │ (consent)   │  │ (agent type)│  │ (exit code) │     │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                                           │
│  Supporting Classes:                                                      │
│  ┌─────────────────────┐  ┌─────────────────────┐                        │
│  │ EnforcementContext  │  │  EnforcementResult  │                        │
│  ├─────────────────────┤  ├─────────────────────┤                        │
│  │ operation: str      │  │ allowed: bool       │                        │
│  │ agent_context: Ctx  │  │ blocking_level: str │                        │
│  │ tool_name: str      │  │ level_results: dict │                        │
│  │ tool_input: dict    │  │ recommendations: [] │                        │
│  │ existing_file: bool │  └─────────────────────┘                        │
│  └─────────────────────┘                                                  │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Stability Patterns

### 5.1 Circuit Breaker

**Reference:** Nygard (2007) [3], Chapter 5 "Stability Patterns"

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Circuit Breaker State Machine                      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│                  ┌───────────────────────────────────┐                    │
│                  │            CLOSED                  │                    │
│                  │     (Normal operation)             │                    │
│                  │                                    │                    │
│                  │  allow_request() → true            │                    │
│                  │  record_success() → reset counter  │                    │
│                  │  record_failure() → increment      │                    │
│                  └──────────────┬────────────────────┘                    │
│                                 │                                          │
│                   failures > threshold                                     │
│                                 │                                          │
│                                 ▼                                          │
│                  ┌───────────────────────────────────┐                    │
│                  │             OPEN                   │                    │
│                  │     (Blocking requests)            │                    │
│                  │                                    │                    │
│                  │  allow_request() → false           │                    │
│                  │  (wait for timeout)                │                    │
│                  └──────────────┬────────────────────┘                    │
│                                 │                                          │
│                    timeout expired                                         │
│                                 │                                          │
│                                 ▼                                          │
│                  ┌───────────────────────────────────┐                    │
│                  │          HALF_OPEN                 │                    │
│                  │     (Testing recovery)             │                    │
│                  │                                    │                    │
│                  │  allow_request() → true (limited)  │                    │
│                  │  record_success() → go to CLOSED   │                    │
│                  │  record_failure() → go to OPEN     │                    │
│                  └───────────────────────────────────┘                    │
│                                                                           │
│  Configuration:                                                           │
│  - failure_threshold: 5 (default)                                         │
│  - reset_timeout_seconds: 60 (default)                                    │
│  - half_open_max_calls: 1 (default)                                       │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Retry with Exponential Backoff

**Reference:** AWS Architecture Blog, "Exponential Back-off and Jitter"

```
Delay Calculation:

  delay = min(base_delay * (2 ^ attempt), max_delay) + random_jitter

Example progression (base=1s, max=30s, jitter=±10%):

  Attempt 1: 1.0s  + jitter → ~1.0s
  Attempt 2: 2.0s  + jitter → ~2.0s
  Attempt 3: 4.0s  + jitter → ~4.0s
  Attempt 4: 8.0s  + jitter → ~8.0s
  Attempt 5: 16.0s + jitter → ~16.0s
  Attempt 6: 30.0s (capped) → ~30.0s
```

**Implementation:**

```python
class RetryPolicy:
    """
    Retry policy with exponential backoff and jitter.

    Reference: AWS Architecture Blog (2015)
    """

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 30.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number."""
        delay = self.initial_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            # Add ±10% random jitter
            jitter_range = delay * 0.1
            delay += random.uniform(-jitter_range, jitter_range)

        return delay
```

---

## 6. Integration Points

### 6.1 wt.py CLI Integration

```python
# wt.py integration point
from domain.self_healing import SelfHealingDispatcher

def main():
    dispatcher = SelfHealingDispatcher.create_default()

    result = dispatcher.dispatch_natural(
        intent=user_input,
        tracker_path=tracker_file
    )

    if result.recovered:
        print(f"✓ Recovered from: {result.recovery_strategy}")

    if not result.success:
        print(f"✗ Error: {result.error}")
```

### 6.2 Hook Integration

```python
# .claude/hooks/initiative_consent_hook.py

from domain.self_healing.enforcement import HookEnforcer

def pre_tool_use(tool_name: str, tool_input: dict) -> int:
    """PreToolUse hook for initiative consent enforcement."""

    enforcer = HookEnforcer.for_initiative_consent()

    decision = enforcer.check_tool_call(
        tool_name=tool_name,
        tool_input=tool_input,
        existing_file=path_exists(tool_input.get("file_path"))
    )

    if not decision.proceed:
        print(f"BLOCKED: {decision.reason}")
        return decision.exit_code  # 1 = block

    return 0  # allow
```

---

## 7. Testing Strategy

### 7.1 Test Pyramid

**Reference:** Fowler, M. (2012). "TestPyramid"

```
                    ┌─────────────┐
                    │    E2E      │  ← 15 tests (prove integration)
                   ─┴─────────────┴─
                  ┌─────────────────┐
                  │   Contract      │  ← 20 tests (prove APIs)
                 ─┴─────────────────┴─
                ┌───────────────────────┐
                │    Integration        │  ← 25 tests (prove composition)
               ─┴───────────────────────┴─
              ┌─────────────────────────────┐
              │          Unit               │  ← 40 tests (prove logic)
             ─┴─────────────────────────────┴─
```

### 7.2 Test Locations

| Level | Location | Purpose |
|-------|----------|---------|
| Unit | `tests/unit/` | Individual component behavior |
| Integration | `tests/integration/` | Component composition |
| Contract | `tests/contract/` | API contract verification |
| E2E | `tests/e2e/` | Full system workflows |
| Architectural | `tests/architectural/` | Dependency rules |
| BDD | `tests/features/` | Behavior scenarios |

---

## 8. Deployment Considerations

### 8.1 Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `WT_RETRY_MAX` | 3 | Maximum retry attempts |
| `WT_RETRY_DELAY` | 1.0 | Initial retry delay (seconds) |
| `WT_CIRCUIT_THRESHOLD` | 5 | Failures to open circuit |
| `WT_CIRCUIT_TIMEOUT` | 60 | Circuit reset timeout (seconds) |

### 8.2 Monitoring

Recommended metrics to export:
- `wt_operations_total` (counter): Total operations
- `wt_operations_success` (counter): Successful operations
- `wt_operations_duration_ms` (histogram): Operation latency
- `wt_circuit_state` (gauge): Circuit breaker state
- `wt_recoveries_total` (counter): Recovery attempts

---

## 9. References

### Academic Papers

1. Kephart, J.O. & Chess, D.M. (2003). "The Vision of Autonomic Computing." IEEE Computer, 36(1), 41-50. DOI: 10.1109/MC.2003.1160055

2. White, S.R. et al. (2004). "An Architectural Approach to Autonomic Computing." ICAC'04.

### Books

3. Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design Patterns: Elements of Reusable Object-Oriented Software. Addison-Wesley.

4. Nygard, M.T. (2007). Release It! Design and Deploy Production-Ready Software. Pragmatic Bookshelf.

5. Fowler, M. (2002). Patterns of Enterprise Application Architecture. Addison-Wesley.

6. Evans, E. (2003). Domain-Driven Design: Tackling Complexity in the Heart of Software. Addison-Wesley.

7. Freeman, S. & Pryce, N. (2009). Growing Object-Oriented Software, Guided by Tests. Addison-Wesley.

### Industry Resources

8. AWS Architecture Blog. "Exponential Back-off and Jitter." https://aws.amazon.com/blogs/architecture/exponential-back-off-and-jitter/

9. Google SRE Book. "Handling Overload." https://sre.google/sre-book/handling-overload/

10. Microsoft Azure. "Transient Fault Handling." https://docs.microsoft.com/en-us/azure/architecture/best-practices/transient-faults

---

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.1.0 | 2026-01-04 | Initiative 19 | Initial architecture document |

---

*This document follows ECSS-E-ST-40C (European Cooperation for Space Standardization) guidelines for software documentation structure.*
