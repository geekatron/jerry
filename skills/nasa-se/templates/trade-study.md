# Trade Study Template

> **Template Version:** 1.0.0
> **Based On:** NASA/SP-2016-6105 Rev2, NPR 7123.1D Process 17
> **Agent:** nse-explorer (divergent)
>
> _Copy this template for trade study documentation_

---

```markdown
---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Trade Study: {Topic}

> **Project:** {Project ID}
> **Entry:** {Entry ID}
> **Date:** {Date}
> **Status:** Draft | In Review | Approved
> **Author:** nse-explorer v1.0.0

---

## L0: Executive Summary

{2-3 sentence overview of the decision space, options considered, and why this
decision matters to mission success. Written for non-technical stakeholders.}

---

## L1: Technical Analysis

### 1.1 Decision Context

**Problem Statement:**
{Clear statement of what decision needs to be made and why}

**Driving Requirements:**
| ID | Requirement | Source |
|----|-------------|--------|
| REQ-XXX | {requirement text} | {source document} |

**Constraints:**
| Constraint | Type | Impact |
|------------|------|--------|
| {constraint} | {hard/soft} | {how it limits options} |

**Assumptions:**
| ID | Assumption | Validation Status |
|----|------------|-------------------|
| ASM-001 | {assumption} | {validated/pending/challenged} |

### 1.2 Evaluation Criteria

| ID | Criterion | Weight (1-5) | Rationale | Requirement Trace |
|----|-----------|--------------|-----------|-------------------|
| C1 | {criterion name} | {weight} | {why important} | REQ-XXX |
| C2 | {criterion name} | {weight} | {why important} | REQ-XXX |
| C3 | {criterion name} | {weight} | {why important} | REQ-XXX |
| C4 | {criterion name} | {weight} | {why important} | REQ-XXX |
| C5 | {criterion name} | {weight} | {why important} | REQ-XXX |

**Weighting Methodology:**
{Describe how weights were assigned - stakeholder input, AHP, team consensus}

### 1.3 Alternatives Generated

#### Alternative 1: {Name}

**Description:**
{Detailed technical description of this alternative}

**Key Characteristics:**
- {characteristic 1}
- {characteristic 2}
- {characteristic 3}

**Pros:**
- {advantage 1 with rationale}
- {advantage 2 with rationale}

**Cons:**
- {disadvantage 1 with rationale}
- {disadvantage 2 with rationale}

**Feasibility Assessment:**
| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Technical | {H/M/L} | {justification} |
| Schedule | {H/M/L} | {justification} |
| Cost | {H/M/L} | {justification} |
| Risk | {H/M/L} | {justification} |

---

#### Alternative 2: {Name}

{Same structure as Alternative 1}

---

#### Alternative 3: {Name}

{Same structure as Alternative 1}

---

### 1.4 Evaluation Matrix

| Criterion (Weight) | Alt 1 | Alt 2 | Alt 3 | Notes |
|--------------------|-------|-------|-------|-------|
| C1: {criterion} (W={w}) | {1-5} | {1-5} | {1-5} | {notes} |
| C2: {criterion} (W={w}) | {1-5} | {1-5} | {1-5} | {notes} |
| C3: {criterion} (W={w}) | {1-5} | {1-5} | {1-5} | {notes} |
| C4: {criterion} (W={w}) | {1-5} | {1-5} | {1-5} | {notes} |
| C5: {criterion} (W={w}) | {1-5} | {1-5} | {1-5} | {notes} |
| **Weighted Total** | {sum} | {sum} | {sum} | |

**Scoring Legend:**
- 5: Excellent - Fully meets criterion
- 4: Good - Mostly meets criterion
- 3: Adequate - Partially meets criterion
- 2: Poor - Marginally meets criterion
- 1: Unacceptable - Does not meet criterion

---

## L2: Systems Perspective

### 2.1 Trade-Off Analysis

{Narrative analysis of the key trade-offs between alternatives. Discuss:
- What you gain with each option
- What you give up with each option
- Which trade-offs are most significant}

### 2.2 Lifecycle Implications

| Alternative | Development Phase | Operations Phase | Maintenance | Decommissioning |
|-------------|-------------------|------------------|-------------|-----------------|
| Alt 1 | {impact} | {impact} | {impact} | {impact} |
| Alt 2 | {impact} | {impact} | {impact} | {impact} |
| Alt 3 | {impact} | {impact} | {impact} | {impact} |

### 2.3 Risk Comparison

| Alternative | Technical Risk | Schedule Risk | Cost Risk | Overall Risk | Key Mitigations |
|-------------|----------------|---------------|-----------|--------------|-----------------|
| Alt 1 | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} | {mitigations} |
| Alt 2 | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} | {mitigations} |
| Alt 3 | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} | {mitigations} |

### 2.4 Interface and Integration Impact

| Alternative | Interface Complexity | Integration Risk | External Dependencies |
|-------------|---------------------|------------------|----------------------|
| Alt 1 | {H/M/L} | {H/M/L} | {list dependencies} |
| Alt 2 | {H/M/L} | {H/M/L} | {list dependencies} |
| Alt 3 | {H/M/L} | {H/M/L} | {list dependencies} |

### 2.5 Recommendation Framework

{Provide decision criteria, NOT final decision. Enable stakeholder choice.}

**Select Alternative 1 IF:**
- {condition 1}
- {condition 2}

**Select Alternative 2 IF:**
- {condition 1}
- {condition 2}

**Select Alternative 3 IF:**
- {condition 1}
- {condition 2}

---

## Open Items

### TBDs (To Be Determined)
| ID | Item | Owner | Due Date | Status |
|----|------|-------|----------|--------|
| TBD-001 | {item needing resolution} | {owner} | {date} | {status} |

### TBRs (To Be Resolved)
| ID | Item | Data Needed | Source | Status |
|----|------|-------------|--------|--------|
| TBR-001 | {item awaiting data} | {what data} | {where from} | {status} |

---

## References

- NASA/SP-2016-6105 Rev2, Section 6.8 - Decision Analysis Process
- NPR 7123.1D, Process 17 - Decision Analysis
- NASA-HDBK-1009A, Trade Study Work Products
- {Project-specific references}

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | {date} | nse-explorer | Initial draft |

---

*Generated by nse-explorer agent v1.0.0*
```

---

## Usage Notes

1. **Always generate minimum 3 alternatives** before evaluation
2. **Challenge assumptions** - question constraints that limit options
3. **Trace to requirements** - every criterion should link to a driving requirement
4. **Provide framework, not decision** - stakeholders make final choices
5. **Document uncertainty** - use TBDs/TBRs for unresolved items

## Validation Checklist

- [ ] Disclaimer included at top
- [ ] L0/L1/L2 sections present
- [ ] Minimum 3 alternatives documented
- [ ] Each alternative has pros, cons, feasibility
- [ ] Evaluation criteria traced to requirements
- [ ] Weighted scoring matrix complete
- [ ] Risk comparison included
- [ ] Recommendation framework (not recommendation) provided
- [ ] Open items documented
- [ ] References to NASA standards included
