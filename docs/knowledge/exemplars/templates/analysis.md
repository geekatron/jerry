# Analysis: {TOPIC}

> **PS:** {PS_ID}
> **Exploration:** {ENTRY_ID}
> **Created:** {DATE}
> **Type:** ARCHITECTURAL | FEASIBILITY | IMPACT | SECURITY | PERFORMANCE
> **Agent:** ps-researcher
> **Session:** {SESSION_ID}

---

## Context

### Background

{Why this analysis was needed - the triggering event or question}

### Stakeholders

- **Requestor:** {Who asked for this analysis}
- **Affected:** {Who will be impacted by findings}

### Constraints

- {Time constraints}
- {Technical constraints}
- {Resource constraints}

---

## Scope

### In Scope

- {What was analyzed - specific components, files, patterns}
- {Boundaries of the analysis}

### Out of Scope

- {What was explicitly excluded}
- {Areas for future analysis}

### Assumptions

- {Key assumptions made during analysis}

---

## Current State Analysis

### Architecture

```
{ASCII or description of current architecture}
```

**Key Components:**
| Component | Purpose | Location |
|-----------|---------|----------|
| {Name} | {Role} | {file:line} |

### Implementation

**Patterns Used:**
- {Pattern 1}: {Where applied}
- {Pattern 2}: {Where applied}

**Dependencies:**
- {Dependency 1}: {Version, purpose}
- {Dependency 2}: {Version, purpose}

### Gaps Identified

| Gap | Severity | Impact |
|-----|----------|--------|
| {Gap description} | HIGH/MED/LOW | {What's affected} |

---

## Proposed State

### Target Architecture

```
{ASCII or description of proposed architecture}
```

### Implementation Approach

**Option A: {Name}**
- Description: {What this approach entails}
- Pros: {Benefits}
- Cons: {Drawbacks}
- Effort: S | M | L | XL
- Risk: LOW | MEDIUM | HIGH

**Option B: {Name}**
- Description: {What this approach entails}
- Pros: {Benefits}
- Cons: {Drawbacks}
- Effort: S | M | L | XL
- Risk: LOW | MEDIUM | HIGH

### Trade-off Matrix

| Criteria | Option A | Option B | Weight |
|----------|----------|----------|--------|
| Complexity | {1-5} | {1-5} | {%} |
| Maintainability | {1-5} | {1-5} | {%} |
| Performance | {1-5} | {1-5} | {%} |
| Risk | {1-5} | {1-5} | {%} |
| **Weighted Score** | {total} | {total} | 100% |

---

## Risk Assessment

| ID | Risk | Likelihood | Impact | Score | Mitigation |
|----|------|------------|--------|-------|------------|
| R1 | {Risk description} | HIGH/MED/LOW | HIGH/MED/LOW | {L×I} | {Strategy} |
| R2 | {Risk description} | HIGH/MED/LOW | HIGH/MED/LOW | {L×I} | {Strategy} |
| R3 | {Risk description} | HIGH/MED/LOW | HIGH/MED/LOW | {L×I} | {Strategy} |

### Risk Matrix

```
         │ LOW Impact │ MED Impact │ HIGH Impact │
─────────┼────────────┼────────────┼─────────────┤
HIGH     │            │     R2     │             │
Likely   │            │            │             │
─────────┼────────────┼────────────┼─────────────┤
MEDIUM   │            │            │     R1      │
Likely   │            │            │             │
─────────┼────────────┼────────────┼─────────────┤
LOW      │     R3     │            │             │
Likely   │            │            │             │
```

---

## Findings

### Finding 1: {Title}

**Severity:** HIGH | MEDIUM | LOW
**Category:** Architecture | Implementation | Security | Performance

**Description:**
{Detailed description of the finding}

**Evidence:**
- File: `{path}:{line}`
- Pattern: `{code or pattern}`

**Impact:**
{What happens if not addressed}

**Recommendation:**
{Specific action to take}

### Finding 2: {Title}

**Severity:** HIGH | MEDIUM | LOW
**Category:** Architecture | Implementation | Security | Performance

**Description:**
{Detailed description of the finding}

**Evidence:**
- File: `{path}:{line}`

**Impact:**
{What happens if not addressed}

**Recommendation:**
{Specific action to take}

---

## Recommendations

### Immediate Actions (P0)

1. **{Action}**
   - Rationale: {Why now}
   - Owner: {Who}
   - Effort: {S/M/L}

### Short-term Actions (P1)

1. **{Action}**
   - Rationale: {Why soon}
   - Owner: {Who}
   - Effort: {S/M/L}

### Long-term Actions (P2)

1. **{Action}**
   - Rationale: {Why eventually}
   - Owner: {Who}
   - Effort: {S/M/L}

---

## Decision Required

### Question for User

{What specific decision needs to be made based on this analysis?}

### Options

| Option | Description | Pros | Cons | Recommendation |
|--------|-------------|------|------|----------------|
| A | {Desc} | {+} | {-} | {Yes/No} |
| B | {Desc} | {+} | {-} | {Yes/No} |
| C | {Desc} | {+} | {-} | {Yes/No} |

### Agent Recommendation

**Recommended Option:** {A/B/C}

**Rationale:** {Why this option is recommended}

**Confidence:** HIGH | MEDIUM | LOW

---

## PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Exploration Entry | `add-entry {PS_ID} "{TOPIC}"` | Done |
| Entry Type | `set-entry-type {PS_ID} {ENTRY_ID} ANALYSIS` | Done |
| Severity | `assess-severity {PS_ID} {ENTRY_ID} {LEVEL}` | Done |
| Artifact Link | `link-artifact {PS_ID} {ENTRY_ID} FILE "docs/analysis/{slug}.md"` | Done |

---

## Appendix

### Technical Details

{Deep technical information that supports findings}

### Code Samples

```{language}
{Relevant code examples}
```

### References

- {Link to related documentation}
- {Link to related analysis}

---

**Generated by:** ps-researcher agent
**Template Version:** 1.0 (Phase 38.16.7)
