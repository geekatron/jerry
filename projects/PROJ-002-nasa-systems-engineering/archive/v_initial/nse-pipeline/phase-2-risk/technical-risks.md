# Technical Risk Assessment: Skills and Agents Architecture

> **Document ID:** nse-k-002
> **Phase:** 2 - Risk (nse-* Pipeline)
> **Project:** PROJ-002-nasa-systems-engineering
> **Date:** 2026-01-09
> **Agent:** nse-risk

---

## L0: Executive Technical Risk Summary

Technical risk assessment of architecture gaps and framework additions identifies **16 technical risks** with **1 RED** (score 16), **9 YELLOW** (scores 8-14), and **6 GREEN** (scores 1-7). The highest technical risk is R-TECH-001: session_context schema incompatibility causing silent agent failures (Score: 16 RED). Framework additions (checkpointing, parallel execution, guardrails) carry moderate technical complexity risks. Migration from implicit to explicit state management presents the highest technical debt concern. All risks include implementation complexity ratings.

---

## L1: Technical Risk Register

### 1.1 Gap-Related Technical Risks

| Risk ID | Risk Statement | L | C | Score | Complexity |
|---------|----------------|---|---|-------|------------|
| R-TECH-001 | IF session_context schema is incompatible across agents THEN handoffs will fail silently | 4 | 4 | **16** | High |
| R-TECH-002 | IF interface contracts are not validated THEN type mismatches will cause runtime errors | 3 | 4 | **12** | Medium |
| R-TECH-003 | IF tool registry is not synchronized THEN tool conflicts will occur | 3 | 3 | **9** | Medium |
| R-TECH-004 | IF persona verification is too strict THEN valid variations rejected | 2 | 3 | **6** | Low |
| R-TECH-005 | IF cognitive mode routing is ambiguous THEN wrong agent selected | 3 | 3 | **9** | Medium |

### 1.2 Framework Addition Technical Risks

| Risk ID | Risk Statement | L | C | Score | Complexity |
|---------|----------------|---|---|-------|------------|
| R-TECH-006 | IF checkpointing serialization is slow THEN workflow latency increases | 3 | 3 | **9** | High |
| R-TECH-007 | IF checkpoint files grow unbounded THEN storage exhaustion | 2 | 4 | **8** | Medium |
| R-TECH-008 | IF parallel agents compete for file handles THEN I/O contention | 3 | 4 | **12** | High |
| R-TECH-009 | IF guardrail regex patterns are incorrect THEN false positives | 2 | 3 | **6** | Low |
| R-TECH-010 | IF guardrail hooks timeout THEN agent execution blocks | 3 | 4 | **12** | Medium |

### 1.3 Migration Technical Risks

| Risk ID | Risk Statement | L | C | Score | Complexity |
|---------|----------------|---|---|-------|------------|
| R-TECH-011 | IF state schema migration is incomplete THEN old agents break | 3 | 4 | **12** | High |
| R-TECH-012 | IF template unification drops optional fields THEN capability loss | 2 | 4 | **8** | Medium |
| R-TECH-013 | IF orchestrator handoff protocol differs from peer protocol THEN dual maintenance | 2 | 3 | **6** | Low |
| R-TECH-014 | IF JSON schema validation is too slow THEN performance degradation | 2 | 3 | **6** | Low |
| R-TECH-015 | IF backward compatibility shims accumulate THEN technical debt grows | 3 | 3 | **9** | Medium |
| R-TECH-016 | IF feature flags remain after migration THEN complexity increases | 2 | 2 | **4** | Low |

---

## L1: Gap-Related Risk Analysis

### GAP-AGT-003: session_context Contract

| Aspect | Assessment |
|--------|------------|
| **Current State** | No formal contract; agents assume ad-hoc JSON |
| **Technical Risk** | Schema drift, silent failures, debugging difficulty |
| **Root Cause** | Organic growth without API design |

**Risk R-TECH-001 Detail:**

```
IF session_context schema is incompatible across agents
THEN:
  1. Agent A passes {key_findings: [...]}
  2. Agent B expects {findings: [...]}
  3. Agent B receives empty/undefined
  4. Silent failure - no error raised
  5. Downstream outputs corrupted
```

**Technical Mitigation:**
1. Define canonical JSON Schema with required fields
2. Implement schema validation at agent boundaries
3. Add schema version field for evolution
4. Generate TypeScript/Python types from schema

**Implementation Complexity:** HIGH
- Requires touching all agent definitions
- Needs validation library integration
- Schema evolution strategy required

### GAP-SKL-002: Interface Contracts

| Aspect | Assessment |
|--------|------------|
| **Current State** | Informal handoff via file paths |
| **Technical Risk** | Type mismatches, missing fields, format drift |
| **Root Cause** | Skills developed independently |

**Risk R-TECH-002 Detail:**

```
IF skill interface contracts are not validated
THEN:
  1. ps-analyst outputs {risk_level: "HIGH"}
  2. nse-risk expects {risk_level: 5}
  3. Type coercion fails or produces wrong value
  4. Risk calculation incorrect
```

**Technical Mitigation:**
1. Define OpenAPI-style contracts per skill
2. Implement contract testing (consumer-driven)
3. Add runtime type validation
4. Document transformation rules

**Implementation Complexity:** MEDIUM
- Contract definition is straightforward
- Testing framework needs selection
- Transformation layer may be needed

---

## L1: Framework Addition Risk Analysis

### Checkpointing (OPT-003)

| Technical Risk | Analysis |
|----------------|----------|
| R-TECH-006 | JSON serialization of large context (~50KB) takes 10-50ms |
| R-TECH-007 | Without cleanup, 1000 checkpoints = 50MB storage |

**Technical Mitigation:**
```yaml
checkpointing:
  serialization: "msgpack"  # 3x faster than JSON
  compression: "lz4"        # Fast compression
  retention:
    max_checkpoints: 100
    max_age_hours: 24
  async_write: true         # Non-blocking
```

**Implementation Complexity:** HIGH
- Requires binary serialization library
- Cleanup daemon needed
- Recovery logic complex

### Parallel Execution (OPT-004)

| Technical Risk | Analysis |
|----------------|----------|
| R-TECH-008 | Multiple agents writing to same directory |

**Technical Mitigation:**
```yaml
parallel_execution:
  file_isolation:
    strategy: "namespace"   # agent_id prefix on all files
    lock_mode: "none"       # No shared locks
  output_dir_template: "{workflow_id}/{agent_id}/"
```

**Implementation Complexity:** HIGH
- Directory isolation logic
- Namespace collision prevention
- Aggregation complexity

### Guardrail Hooks (OPT-005)

| Technical Risk | Analysis |
|----------------|----------|
| R-TECH-009 | Regex false positives block valid output |
| R-TECH-010 | Slow hooks block agent execution |

**Technical Mitigation:**
```yaml
guardrails:
  timeout_ms: 100           # Fast fail
  mode: "warn"              # Don't block, just log
  async: true               # Non-blocking validation
  patterns:
    - name: "pii_detector"
      regex: "\\b\\d{3}-\\d{2}-\\d{4}\\b"  # SSN pattern
      action: "redact"
```

**Implementation Complexity:** MEDIUM
- Pattern library available
- Async execution straightforward
- False positive tuning ongoing

---

## L1: Migration Risk Analysis

### State Schema Migration

| Phase | Risk | Mitigation |
|-------|------|------------|
| 1. Define new schema | R-TECH-011 | Parallel run with old format |
| 2. Update agent templates | R-TECH-012 | Map all existing fields |
| 3. Validate existing workflows | R-TECH-015 | Compatibility test suite |
| 4. Remove compatibility shims | R-TECH-016 | Scheduled deprecation |

**Migration Sequence:**
```
v1.0: Implicit state (current)
    ↓
v1.1: Optional explicit schema (dual-mode)
    ↓
v1.2: Required explicit schema (warnings on implicit)
    ↓
v2.0: Explicit only (implicit removed)
```

**Implementation Complexity:** HIGH
- 3-phase rollout
- Extensive testing required
- Backward compatibility period

### Template Unification Migration

| Phase | Risk | Mitigation |
|-------|------|------------|
| 1. Superset schema | R-TECH-012 | All fields optional initially |
| 2. ps-* adoption | R-TECH-013 | Feature flag per agent |
| 3. nse-* adoption | R-TECH-013 | Feature flag per agent |
| 4. Cleanup | R-TECH-015 | Remove old template |

**Implementation Complexity:** MEDIUM
- Schema merge straightforward
- Migration scriptable
- Testing per agent

---

## L2: Technical Debt Assessment

### Current Technical Debt

| Debt Item | Severity | Origin | Payoff Effort |
|-----------|----------|--------|---------------|
| Implicit state management | HIGH | Organic growth | 40 hours |
| Dual template maintenance | MEDIUM | Domain split | 16 hours |
| Missing interface contracts | HIGH | Fast iteration | 24 hours |
| Unvalidated handoffs | HIGH | Trust assumption | 16 hours |
| No schema versioning | MEDIUM | Not anticipated | 8 hours |

**Total Technical Debt:** ~104 engineering hours

### Debt Accrual Risk

| Proposed Change | New Debt Risk | Mitigation |
|-----------------|---------------|------------|
| Checkpointing | Cleanup daemon maintenance | Automated retention |
| Parallel execution | Namespace complexity | Clear conventions |
| Guardrails | Pattern library maintenance | External library |
| Orchestrators | Control plane complexity | Simple delegation |

### Debt Reduction Priority

```
Priority 1: Interface contracts (unlocks automation)
Priority 2: State schema (unlocks reliability)
Priority 3: Template unification (reduces maintenance)
Priority 4: Schema versioning (unlocks evolution)
```

---

## Cross-Pollination Metadata

### Source Context (Barrier 1 Input)

| Source | Key Inputs Used |
|--------|-----------------|
| requirements-gaps.md | GAP-SKL-*, GAP-AGT-*, RGAP-* |
| research-findings.md | Framework gaps (parallel, checkpoint, guardrails) |

### Target Pipeline: nse-architecture (Phase 3)

**Artifacts for Architecture Design:**

| Risk | Architecture Requirement |
|------|-------------------------|
| R-TECH-001 | Schema validation at all boundaries |
| R-TECH-008 | File namespace isolation |
| R-TECH-011 | Dual-mode migration support |

### Handoff Checklist for Barrier 2

- [x] 16 technical risks identified
- [x] Implementation complexity rated
- [x] Technical debt quantified
- [x] Migration sequence defined
- [ ] nse-architecture acknowledges constraints

---

## Risk Acceptance Recommendation

| Decision | Rationale |
|----------|-----------|
| **PROCEED with R-TECH-001 mitigation FIRST** | Session_context is foundation for all other changes |
| **Implement schema validation early** | Catches issues before cascade |
| **Accept 104-hour debt payoff** | Investment justified by reliability gains |
| **Monitor R-TECH-008 in parallel impl** | Highest technical complexity |

---

*Risk Document: nse-k-002*
*Generated by: nse-risk (Phase 2)*
*Date: 2026-01-09*
*NPR 8000.4C Compliant*
