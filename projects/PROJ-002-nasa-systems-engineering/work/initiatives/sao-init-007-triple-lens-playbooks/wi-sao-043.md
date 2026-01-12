---
id: wi-sao-043
title: "Add L0/L1/L2 concrete examples (5+ each domain)"
status: OPEN
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on:
  - wi-sao-042
blocks: []
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P1
estimated_effort: "6h"
entry_id: sao-043
token_estimate: 700
---

# WI-SAO-043: Add L0/L1/L2 Concrete Examples

> **Status:** 📋 OPEN
> **Priority:** P1 (HIGH - User-facing documentation)
> **Depends On:** WI-SAO-042 (Generator-Critic research)

---

## Description

Current playbooks have L0/L1/L2 sections but lack **concrete, real-world examples** that users can relate to. Users need:

1. **Software Engineering examples** - Debugging, architecture decisions, code reviews
2. **Product Management examples** - Feature prioritization, stakeholder alignment, roadmap planning
3. **User Experience examples** - Usability testing, design critique, accessibility reviews

Each example must demonstrate the L0 (ELI5), L1 (Engineer), and L2 (Architect) perspectives clearly.

---

## Acceptance Criteria

1. [ ] ≥5 Software Engineering examples across playbooks
2. [ ] ≥5 Product Management examples across playbooks
3. [ ] ≥5 User Experience examples across playbooks
4. [ ] Each example shows L0 (what/why), L1 (how), L2 (constraints/anti-patterns)
5. [ ] Examples are relatable and actionable
6. [ ] Examples distributed appropriately across playbooks

---

## Tasks

### T-043.1: Software Engineering Examples
- [ ] **T-043.1.1:** Example: Debugging a production incident (root cause analysis)
- [ ] **T-043.1.2:** Example: Architecture decision record (ADR) creation
- [ ] **T-043.1.3:** Example: Code review with generator-critic loop
- [ ] **T-043.1.4:** Example: Technical debt assessment
- [ ] **T-043.1.5:** Example: API design review

### T-043.2: Product Management Examples
- [ ] **T-043.2.1:** Example: Feature prioritization with trade-off analysis
- [ ] **T-043.2.2:** Example: Stakeholder requirement elicitation
- [ ] **T-043.2.3:** Example: Competitive analysis research
- [ ] **T-043.2.4:** Example: Sprint planning with risk assessment
- [ ] **T-043.2.5:** Example: Product roadmap validation

### T-043.3: User Experience Examples
- [ ] **T-043.3.1:** Example: Usability heuristic evaluation
- [ ] **T-043.3.2:** Example: Design critique with feedback loop
- [ ] **T-043.3.3:** Example: Accessibility compliance review
- [ ] **T-043.3.4:** Example: User journey mapping
- [ ] **T-043.3.5:** Example: A/B test analysis

### T-043.4: Integration
- [ ] **T-043.4.1:** Add SE examples to problem-solving PLAYBOOK.md
- [ ] **T-043.4.2:** Add PM examples to problem-solving PLAYBOOK.md
- [ ] **T-043.4.3:** Add UX examples to problem-solving PLAYBOOK.md
- [ ] **T-043.4.4:** Add relevant examples to orchestration PLAYBOOK.md
- [ ] **T-043.4.5:** Cross-reference with nasa-se PLAYBOOK.md where applicable

---

## Example Template

Each example MUST follow this structure:

```markdown
### Example: {Title}

**Domain:** Software Engineering | Product Management | User Experience
**Scenario:** {1-2 sentence real-world situation}

#### L0 (ELI5) - What & Why
> {Plain language explanation a non-technical person would understand}
> - What are we trying to accomplish?
> - Why does this matter?

#### L1 (Engineer) - How
{Technical implementation details}
- Agent sequence: {ps-researcher → ps-analyst → ...}
- Key commands/invocations
- Expected outputs

#### L2 (Architect) - Constraints & Anti-patterns
| Constraint | Impact | Mitigation |
|------------|--------|------------|
| {constraint} | {impact} | {mitigation} |

**Anti-patterns to avoid:**
- {anti-pattern 1}
- {anti-pattern 2}
```

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-043-001 | Content | ≥5 SE examples documented | ⏳ |
| E-043-002 | Content | ≥5 PM examples documented | ⏳ |
| E-043-003 | Content | ≥5 UX examples documented | ⏳ |
| E-043-004 | Quality | Examples follow template structure | ⏳ |
| E-043-005 | Integration | Examples integrated into playbooks | ⏳ |

---

## Example Ideas (Brainstorm)

### Software Engineering
1. "Production database is slow - need root cause analysis"
2. "Should we use microservices or monolith for new project?"
3. "PR has 50+ comments - need structured review synthesis"
4. "Legacy system modernization - where to start?"
5. "Security vulnerability discovered - impact assessment"

### Product Management
1. "Three features requested, budget for one - which to build?"
2. "Stakeholders disagree on requirements - need alignment"
3. "Competitor launched similar feature - strategic response?"
4. "Sprint commitments at risk - trade-off decisions"
5. "User feedback contradicts business metrics - what to prioritize?"

### User Experience
1. "Users abandoning checkout flow - usability review"
2. "Design mockup feedback from 5 stakeholders - synthesis"
3. "WCAG 2.1 AA compliance audit"
4. "New feature onboarding flow - friction analysis"
5. "Mobile vs desktop conversion gap - investigation"

---

*Source: DISCOVERY-012 (GAP-012-003)*
*Created: 2026-01-12*
