# Alternative Analysis Template

> **Template Version:** 1.0.0
> **Based On:** NASA/SP-2016-6105 Rev2, NPR 7123.1D Process 17
> **Agent:** nse-explorer (divergent)
>
> _Copy this template for alternative generation and analysis_

---

```markdown
---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Alternative Analysis: {Topic}

> **Project:** {Project ID}
> **Entry:** {Entry ID}
> **Date:** {Date}
> **Status:** Draft | In Review | Approved
> **Author:** nse-explorer v1.0.0

---

## L0: Executive Summary

{2-3 sentences describing what alternatives were explored, why this exploration
matters, and the key insight gained. Written for non-technical stakeholders.}

---

## L1: Technical Analysis

### 1.1 Exploration Context

**Objective:**
{What are we trying to achieve? What problem space are we exploring?}

**Scope:**
| In Scope | Out of Scope |
|----------|--------------|
| {item} | {item} |

**Driving Requirements:**
| ID | Requirement | Priority |
|----|-------------|----------|
| REQ-XXX | {requirement} | {Must/Should/Could} |

### 1.2 Assumptions Challenged

{Divergent thinking requires challenging assumptions}

| Original Assumption | Challenge Question | Result |
|---------------------|-------------------|--------|
| {assumption we started with} | {what if this were false?} | {new insight or confirmed} |
| {assumption} | {challenge} | {result} |
| {assumption} | {challenge} | {result} |

### 1.3 Alternatives Explored

---

#### Category A: {Category Name}

**Category Description:** {What type of solutions are in this category?}

##### Alternative A1: {Name}

**Description:**
{Detailed description of this alternative}

**Strengths:**
- {strength with rationale}
- {strength with rationale}

**Weaknesses:**
- {weakness with rationale}
- {weakness with rationale}

**Key Differentiator:**
{What makes this alternative unique compared to others?}

**Technical Feasibility:** {High/Medium/Low} - {justification}

**Resource Requirements:**
- Development effort: {estimate}
- Skills needed: {skills}
- External dependencies: {dependencies}

---

##### Alternative A2: {Name}

{Same structure as A1}

---

#### Category B: {Category Name}

**Category Description:** {What type of solutions are in this category?}

##### Alternative B1: {Name}

{Same structure as A1}

---

#### Category C: Unconventional Options

**Purpose:** Document creative or outside-the-box ideas, even if not immediately feasible.

##### Alternative C1: {Unconventional Name}

**Description:**
{Description of unconventional approach}

**Why Consider This:**
{What makes this worth documenting even if not selected?}

**Barriers to Adoption:**
- {barrier 1}
- {barrier 2}

**Valuable Elements:**
{What elements might be borrowed into other alternatives?}

---

### 1.4 Comparison Matrix

| Aspect | Alt A1 | Alt A2 | Alt B1 | Alt C1 |
|--------|--------|--------|--------|--------|
| Technical Feasibility | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} |
| Resource Intensity | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} |
| Risk Level | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} |
| Innovation Level | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} |
| Alignment to Reqs | {H/M/L} | {H/M/L} | {H/M/L} | {H/M/L} |

### 1.5 Hybrid Possibilities

{Explore combinations of alternatives}

| Hybrid | Elements Combined | Potential Benefit | Potential Risk |
|--------|-------------------|-------------------|----------------|
| Hybrid 1 | {A1 feature} + {B1 feature} | {benefit} | {risk} |
| Hybrid 2 | {A2 feature} + {C1 element} | {benefit} | {risk} |

---

## L2: Systems Perspective

### 2.1 Strategic Implications

{High-level analysis of what each alternative means for the system}

| Alternative | Short-term Impact | Long-term Impact | Strategic Fit |
|-------------|-------------------|------------------|---------------|
| Alt A1 | {impact} | {impact} | {H/M/L} |
| Alt A2 | {impact} | {impact} | {H/M/L} |
| Alt B1 | {impact} | {impact} | {H/M/L} |

### 2.2 Trade-Space Visualization

```
                    High Performance
                          ^
                          |
                    A2 *  |  * A1
                          |
       Low Cost <---------+---------> High Cost
                          |
                    B1 *  |  * C1
                          |
                    Low Performance
```

{Adjust axes based on key trade-off dimensions}

### 2.3 Decision Readiness Assessment

| Alternative | Analysis Completeness | Data Confidence | Ready for Decision? |
|-------------|----------------------|-----------------|---------------------|
| Alt A1 | {%} | {H/M/L} | {Yes/No/Needs: X} |
| Alt A2 | {%} | {H/M/L} | {Yes/No/Needs: X} |
| Alt B1 | {%} | {H/M/L} | {Yes/No/Needs: X} |

### 2.4 Next Steps

{What should happen next based on this exploration?}

1. {Next step 1}
2. {Next step 2}
3. {Next step 3}

---

## Open Items

### Questions Requiring Resolution
| ID | Question | Impact on Decision | Owner |
|----|----------|-------------------|-------|
| Q-001 | {question} | {how it affects choice} | {owner} |

### Information Gaps
| ID | Missing Information | Where to Get It | Priority |
|----|---------------------|-----------------|----------|
| IG-001 | {what's missing} | {source} | {H/M/L} |

---

## References

- NASA/SP-2016-6105 Rev2, Section 6.8 - Decision Analysis
- NPR 7123.1D, Process 17 - Decision Analysis
- {Domain-specific references}
- {Prior art and industry examples}

---

*Generated by nse-explorer agent v1.0.0*
```

---

## Usage Notes

1. **Organize by category** - Group related alternatives for easier comparison
2. **Include unconventional options** - Even if not selected, they may provide valuable elements
3. **Challenge assumptions** - This is where divergent value comes from
4. **Explore hybrids** - Best solutions often combine elements from multiple alternatives
5. **Assess decision readiness** - Not all alternatives need same level of analysis

## Divergent Thinking Prompts

When generating alternatives, ask:
- What if the opposite were true?
- How would [other industry] solve this?
- What's the most extreme solution?
- What would we do with unlimited budget? Zero budget?
- What assumptions are we not questioning?

## Validation Checklist

- [ ] Disclaimer included at top
- [ ] L0/L1/L2 sections present
- [ ] Minimum 3 distinct alternatives documented
- [ ] At least one unconventional option explored
- [ ] Assumptions challenged and documented
- [ ] Each alternative has strengths and weaknesses
- [ ] Hybrid possibilities considered
- [ ] Next steps identified
- [ ] Open items documented
