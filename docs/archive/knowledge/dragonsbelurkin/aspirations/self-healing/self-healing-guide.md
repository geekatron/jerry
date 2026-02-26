# Self-Healing Work Tracker - User Guide

> **Version:** 2.1.0 (Initiative 19)
> **Audience:** All users (Beginner → Intermediate → Architect)
> **Created:** 2026-01-04
> **References:** MAPE-K Control Loop, Circuit Breaker Pattern, Four-Level Enforcement

---

## Table of Contents

1. [Quick Start (2 minutes)](#quick-start-2-minutes) - For beginners
2. [Feature Overview](#feature-overview) - Understanding self-healing
3. [User Guide](#user-guide) - Using self-healing features
4. [Advanced Configuration](#advanced-configuration) - For power users
5. [Architecture Reference](#architecture-reference) - For architects
6. [Troubleshooting](#troubleshooting) - Common issues
7. [References](#references) - Citations and prior art

---

## Quick Start (2 minutes)

### What is Self-Healing?

The Work Tracker automatically **detects, diagnoses, and recovers** from errors without losing your work. You don't need to do anything special - it just works.

### What Does This Mean for You?

| Situation | Before Self-Healing | With Self-Healing |
|-----------|---------------------|-------------------|
| Network timeout | Error, retry manually | Auto-retry with backoff |
| Invalid command | Error, figure it out | Helpful suggestion provided |
| Corrupted state | Data loss possible | Auto-repair from backup |
| Conflicting updates | Overwrite risk | Conflict resolution |

### Try It Now

```bash
# Run any command with --show-health to see health status
python3 scripts/wt.py --show-health --tracker docs/plans/my-project.md "show progress"

# Example output:
# Overall progress: 85%
# ...
# Health: HEALTHY (100.0% success rate)

# With --verbose for more details:
python3 scripts/wt.py --show-health --verbose --tracker docs/plans/my-project.md "show progress"
# Health: HEALTHY (100.0% success rate)
#   Operations: 1
#   Failures: 0
#   Avg latency: 50ms
```

### Quick Commands

| Command | What It Does |
|---------|--------------|
| `"show progress"` | Display current status with health metrics |
| `"mark task X complete"` | Update task with automatic verification |
| `"sync"` | Force synchronization with self-healing |

**That's it!** Self-healing works in the background. Continue reading for more details.

---

## Feature Overview

### The MAPE-K Control Loop

Self-healing is powered by the **MAPE-K** control loop (Kephart & Chess, 2003):

```
┌─────────────────────────────────────────────────────────────┐
│                     MAPE-K Loop                              │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐ │
│  │ Monitor  │───>│ Analyze  │───>│   Plan   │───>│Execute │ │
│  │  (M)     │    │   (A)    │    │   (P)    │    │  (E)   │ │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └───┬────┘ │
│       │               │               │              │      │
│       └───────────────┴───────────────┴──────────────┘      │
│                           │                                  │
│                    ┌──────▼──────┐                          │
│                    │  Knowledge  │                          │
│                    │     (K)     │                          │
│                    └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

**In Plain English:**

1. **Monitor**: Watches every operation for problems
2. **Analyze**: Classifies errors (transient vs. permanent)
3. **Plan**: Selects best recovery strategy
4. **Execute**: Performs recovery action
5. **Knowledge**: Learns from successes and failures

### Four-Level Enforcement

Operations are validated at four levels before execution:

| Level | What It Checks | Can Block? |
|-------|----------------|------------|
| **Advisory** | CLAUDE.md guidelines | No (recommendations only) |
| **Soft** | Consent for sensitive ops | Yes (without consent) |
| **Medium** | Agent restrictions | Yes (unauthorized agents) |
| **HARD** | Hook-based enforcement | Yes (unauthorized files) |

**You'll only notice enforcement if you try to do something unauthorized** (like creating a new initiative without permission).

---

## User Guide

### Understanding Health Status

Use `--show-health` flag to see health status after any operation:

```bash
python3 scripts/wt.py --show-health --tracker ... "your command"

# Output includes:
Health: HEALTHY (99.5% success rate)
```

| Status | Meaning | Action Needed |
|--------|---------|---------------|
| HEALTHY | All systems normal | None |
| DEGRADED | Some failures detected | Monitor |
| UNHEALTHY | Circuit breaker may trip | Investigate |
| CRITICAL | Operations may be blocked | Immediate attention |

### Automatic Recovery Examples

#### Example 1: Transient Error (Auto-Retry)

```
Command: mark task 5.3 complete

✓ Attempt 1: Timeout (network)
✓ Recovery: Exponential backoff retry
✓ Attempt 2: Success

Task 5.3 marked complete.
```

#### Example 2: Validation Error (Auto-Correct)

```
Command: update task 1.1 status to DONE

✓ Issue: Invalid status 'DONE'
✓ Recovery: Normalized to 'complete'
✓ Result: Task 1.1 status updated to complete
```

#### Example 3: File Conflict (Auto-Resolve)

```
Command: sync tracker

✓ Issue: JSON and Markdown out of sync
✓ Recovery: JSON is SSOT, regenerating Markdown
✓ Result: Markdown regenerated from JSON (0 data loss)
```

### Circuit Breaker Protection

The circuit breaker prevents cascading failures:

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│   CLOSED   │────>│ HALF_OPEN  │────>│    OPEN    │
│ (normal)   │     │  (testing) │     │ (blocked)  │
└────────────┘     └────────────┘     └────────────┘
      ↑                  │                   │
      └──────────────────┴───────────────────┘
```

**What this means:**
- **CLOSED**: Operations proceed normally
- **OPEN**: Too many failures, operations blocked temporarily
- **HALF_OPEN**: Testing if service recovered

**You'll see:**
```
⚠ Circuit OPEN: Operations paused (retry in 60s)
```

### Consent-Protected Operations

Some operations require your explicit consent:

```
Command: create initiative 20

? This operation requires consent.
  Creating new Initiative requires user approval.

  Respond with "yes" or "approved" to proceed.
```

**Operations requiring consent:**
- Creating new initiatives
- Deleting trackers
- Bulk status changes

**Bypass for trusted workflows:**
```bash
python3 scripts/wt.py --skip-consent --tracker ... "create initiative 20"
```

---

## Advanced Configuration

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `WT_RETRY_MAX` | 3 | Maximum retry attempts |
| `WT_RETRY_DELAY` | 1.0 | Initial retry delay (seconds) |
| `WT_CIRCUIT_THRESHOLD` | 5 | Failures before circuit opens |
| `WT_CIRCUIT_TIMEOUT` | 60 | Seconds before circuit retests |

### Custom Retry Policy

```python
# In your script
from domain.self_healing import RetryPolicy

policy = RetryPolicy(
    max_attempts=5,
    initial_delay=0.5,
    max_delay=30.0,
    exponential_base=2.0,
    jitter=True  # Random variation to prevent thundering herd
)
```

### Health Monitoring

```python
from domain.self_healing import HealthMonitor

monitor = HealthMonitor()

# Record operations
monitor.record_success(duration_ms=150)
monitor.record_failure(duration_ms=5000)

# Check health
status = monitor.get_health_status()
print(f"Health: {status.overall.name}")
print(f"Success Rate: {monitor.get_metrics().success_rate:.2%}")
```

### Consent State

Consent decisions are stored in `.ecw/consent-state.json`:

```json
{
  "session_id": "current-session",
  "approved_initiatives": [16, 17, 18, 19],
  "blanket_approval": false,
  "last_updated": "2026-01-04T10:00:00Z"
}
```

**Grant blanket approval:**
```
User: "you may create initiatives as needed"
Claude: Blanket approval granted for initiative creation.
```

---

## Architecture Reference

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Self-Healing Architecture                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐    ┌──────────────────────────────────────┐│
│  │   wt.py CLI     │───>│    SelfHealingDispatcher             ││
│  └─────────────────┘    │                                      ││
│                         │  ┌─────────────┐  ┌───────────────┐  ││
│                         │  │HealthMonitor│  │SymptomAnalyzer│  ││
│                         │  └─────────────┘  └───────────────┘  ││
│                         │                                      ││
│                         │  ┌─────────────┐  ┌───────────────┐  ││
│                         │  │RemediationP.│  │ActionExecutor │  ││
│                         │  └─────────────┘  └───────────────┘  ││
│                         │                                      ││
│                         │  ┌─────────────┐  ┌───────────────┐  ││
│                         │  │KnowledgeBase│  │CircuitBreaker │  ││
│                         │  └─────────────┘  └───────────────┘  ││
│                         └──────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              FourLevelEnforcer                               ││
│  │                                                              ││
│  │  Advisory ──> Soft ──> Medium ──> HARD                       ││
│  │  (CLAUDE.md)  (Consent) (Agent)   (Hook)                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### MAPE-K Implementation

#### Monitor Phase (HealthMonitor)

```python
class HealthMonitor:
    """
    Monitors system health using sliding window metrics.

    Reference: Kephart & Chess (2003), Section 3.1 "Monitor"
    """

    def record_success(self, duration_ms: int) -> None:
        """Record successful operation with latency."""

    def record_failure(self, duration_ms: int) -> None:
        """Record failed operation with latency."""

    def get_health_status(self) -> HealthStatus:
        """
        Returns current health level based on:
        - Success rate (< 90% = DEGRADED, < 70% = UNHEALTHY)
        - P95 latency (> 1000ms = DEGRADED)
        - Failure trend (increasing = DEGRADED)
        """
```

#### Analyze Phase (SymptomAnalyzer)

```python
class SymptomAnalyzer:
    """
    Classifies errors using pattern matching.

    Reference: Kephart & Chess (2003), Section 3.2 "Analyze"
    """

    def analyze(self, symptom: Symptom) -> Diagnosis:
        """
        Classifies error into categories:
        - TRANSIENT: Network timeouts, rate limits
        - VALIDATION: Invalid input, schema errors
        - RESOURCE: File not found, permission denied
        - CORRUPTION: Data integrity failures
        - UNKNOWN: Unclassified errors
        """
```

#### Plan Phase (RemediationPlanner)

```python
class RemediationPlanner:
    """
    Selects recovery strategy based on diagnosis.

    Reference: Kephart & Chess (2003), Section 3.3 "Plan"
    """

    def plan(self, diagnosis: Diagnosis) -> RemediationPlan:
        """
        Strategy selection:
        - TRANSIENT → RETRY with exponential backoff
        - VALIDATION → NORMALIZE input
        - RESOURCE → ESCALATE to user
        - CORRUPTION → REPAIR from backup
        - UNKNOWN → ESCALATE with context
        """
```

#### Execute Phase (ActionExecutor)

```python
class ActionExecutor:
    """
    Executes recovery actions with circuit breaker protection.

    Reference:
    - Kephart & Chess (2003), Section 3.4 "Execute"
    - Nygard (2007), Chapter 5 "Circuit Breaker"
    """

    def execute(self, plan: RemediationPlan) -> ExecutionResult:
        """
        Executes recovery with:
        - Retry logic (exponential backoff with jitter)
        - Circuit breaker protection
        - Timeout enforcement
        - Result tracking for knowledge base
        """
```

#### Knowledge Phase (KnowledgeBase)

```python
class KnowledgeBase:
    """
    Stores failure patterns and recovery outcomes.

    Reference: Kephart & Chess (2003), Section 3.5 "Knowledge"
    """

    def record_failure(self, diagnosis: Diagnosis) -> None:
        """Record failure pattern for future reference."""

    def record_recovery(self, diagnosis: Diagnosis, success: bool) -> None:
        """Record recovery outcome for strategy optimization."""

    def get_statistics(self) -> Dict[str, Any]:
        """Return aggregated failure/recovery statistics."""
```

### Four-Level Enforcement Implementation

#### Chain of Responsibility Pattern

```python
class FourLevelEnforcer:
    """
    Implements Chain of Responsibility pattern (Gamma et al., 1994).

    Levels are checked in sequence. First blocking level stops the chain.
    """

    def check(self, operation: str, context: EnforcementContext) -> EnforcementResult:
        """
        Check order:
        1. Advisory (never blocks)
        2. Soft (blocks without consent)
        3. Medium (blocks unauthorized agents)
        4. HARD (blocks via hook exit code)
        """
```

#### Level Implementations

| Level | Class | Behavior |
|-------|-------|----------|
| Advisory | `AdvisoryLevel` | Returns recommendations, never blocks |
| Soft | `ConsentManager` | Checks consent state, blocks if missing |
| Medium | `AgentRestrictionEnforcer` | Blocks subagent operations |
| HARD | `HookEnforcer` | Exit code 1 blocks tool call |

### Circuit Breaker States

```
State Transitions (Nygard, 2007):

CLOSED ──(failures > threshold)──> OPEN
   ↑                                  │
   │                                  │
   └──(success)── HALF_OPEN <─(timeout)
```

| State | Behavior | Transition |
|-------|----------|------------|
| CLOSED | All requests allowed | → OPEN after N failures |
| OPEN | All requests blocked | → HALF_OPEN after timeout |
| HALF_OPEN | One test request allowed | → CLOSED on success, → OPEN on failure |

### Error Categories

| Category | Examples | Recovery Strategy |
|----------|----------|-------------------|
| TRANSIENT | Timeout, 503, rate limit | Retry with backoff |
| VALIDATION | Invalid status, bad ID | Normalize or reject |
| RESOURCE | File not found, permission | Escalate to user |
| CORRUPTION | Checksum mismatch, invalid JSON | Repair from backup |
| UNKNOWN | Unclassified | Escalate with context |

---

## Troubleshooting

### Circuit Breaker Open

**Symptom:** Operations blocked with "Circuit OPEN" message

**Solution:**
1. Wait for timeout (default 60s)
2. Check underlying service health
3. If persistent, manually reset:
```python
from domain.self_healing import CircuitBreaker
cb = CircuitBreaker()
cb.reset()  # Force to CLOSED
```

### Consent Denied

**Symptom:** Operation blocked requiring consent

**Solution:**
1. Review the operation being attempted
2. Respond with "yes" or "approved"
3. For trusted workflows, use `--skip-consent`

### Health Degraded

**Symptom:** Health status shows DEGRADED or UNHEALTHY

**Solution:**
1. Check recent operations: `"show progress"`
2. Review error logs
3. Run sync: `"sync tracker"`
4. If persistent, check network/disk

### Self-Healing Loop

**Symptom:** Repeated recovery attempts

**Solution:**
1. Check if error is truly transient
2. If permanent, escalate manually
3. Review knowledge base stats

---

## References

### Academic Citations

1. **Kephart, J.O. & Chess, D.M. (2003)**. "The Vision of Autonomic Computing."
   *IEEE Computer*, 36(1), 41-50. DOI: 10.1109/MC.2003.1160055
   - Foundation for MAPE-K control loop

2. **Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994)**.
   *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
   - Chain of Responsibility pattern (p. 223)

3. **Nygard, M.T. (2007)**. *Release It! Design and Deploy Production-Ready Software*.
   Pragmatic Bookshelf.
   - Circuit Breaker pattern (Chapter 5)

4. **Fowler, M. (2012)**. "TestPyramid." martinfowler.com
   - Test pyramid structure for verification

5. **Freeman, S. & Pryce, N. (2009)**. *Growing Object-Oriented Software, Guided by Tests*.
   Addison-Wesley.
   - BDD approach for test design

### Industry Best Practices

- **AWS Architecture Blog**: "Exponential Backoff and Jitter"
  (https://aws.amazon.com/blogs/architecture/exponential-back-off-and-jitter/)

- **Google SRE Book**: "Handling Overload"
  (https://sre.google/sre-book/handling-overload/)

- **Microsoft Azure Well-Architected Framework**: "Transient Fault Handling"
  (https://docs.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-04 | Added MAPE-K self-healing, Four-Level Enforcement |
| 2.0.0 | 2025-12-28 | Initial work tracker with JSON SSOT |

---

*Document follows NASA/ESA documentation standards (ECSS-E-ST-40C) for software documentation.*
