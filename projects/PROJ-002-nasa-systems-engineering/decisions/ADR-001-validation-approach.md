# ADR-001: Validation Approach Decision

> Architecture Decision Record for NASA SE Skill Validation Strategy

---

## Status

**ACCEPTED** | 2026-01-09

---

## Context

After completing all 6 implementation phases of the NASA SE skill (10,183 lines, 19 files, 8 agents, 30 BDD tests), the question arose: should we perform additional iterations using ps-* subagents for validation?

### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A | Additional ps-researcher validation | Cross-check NASA citations | AI validating AI; circular |
| B | ps-analyst gap re-analysis | Verify 37 requirements covered | Already addressed in plan v3.0 |
| C | ps-analyst risk re-assessment | Show residual risk reduction | Doesn't address human judgment need |
| D | User SME validation (selected) | Human review per plan | Requires user time |
| E | Dog-fooding with real artifacts | Prove skill works end-to-end | Requires effort but proves value |

---

## Decision

**Selected: Options D + E (User SME Validation + Dog-fooding)**

We will NOT perform additional ps-* agent iterations for validation. Instead:

1. **User SME Validation** - Per plan Section 10 (Governance Model)
2. **Dog-fooding** - Demonstrate each agent produces real artifacts

---

## Rationale

### Why NOT additional AI iterations:

1. **Plan specified user SME validation**
   - Quote: "SME Validation: User serves as SME proxy for NASA SE accuracy"
   - This was an explicit design decision captured in the plan

2. **Top risks require human judgment**
   - R-01 (AI hallucination): Score 20 (RED) - Cannot be mitigated by more AI
   - R-11 (Over-reliance on AI): Score 20 (RED) - Explicitly requires human review
   - R-06 (Process misrepresentation): Score 16 (RED) - Needs SME validation

3. **Circular validation problem**
   - ps-analyst validating work informed by ps-researcher = AI validating AI
   - Does not address fundamental accuracy concern
   - Creates false confidence

4. **Mitigations already implemented**
   - P-043: Mandatory disclaimer on all outputs ✓
   - Human-in-loop gate checkpoints ✓
   - SME review protocol defined ✓

5. **Diminishing returns**
   - 10,183 lines across 19 files
   - 30 BDD tests with full coverage
   - More iterations = completeness theater, not quality

### Why dog-fooding IS valuable:

1. **Proves real functionality** - Not just tests, actual artifacts
2. **Identifies gaps in templates** - Using them reveals issues
3. **Demonstrates value proposition** - Shows what skill produces
4. **Self-referential validation** - Apply SE to SE skill itself

---

## Consequences

### Positive
- Avoids circular AI validation trap
- Respects governance model (user authority)
- Produces tangible evidence of skill capability
- Identifies practical usability issues

### Negative
- Requires user time for SME validation
- Dog-fooding effort needed
- May find issues requiring rework

### Risks Mitigated
- R-01: Disclaimer + human review (not more AI)
- R-11: Explicit human-in-loop, not AI-in-loop
- R-06: SME validation, not AI validation

---

## Evidence

### Implementation Risk Assessment Reference
From `analysis/proj-002-e-007-implementation-risk-assessment.md`:

| Risk ID | Risk | Score | Required Mitigation |
|---------|------|-------|---------------------|
| R-01 | AI hallucination | 20 (RED) | Human review, citations |
| R-11 | Over-reliance on AI | 20 (RED) | Human-in-loop checkpoints |
| R-06 | Process misrepresentation | 16 (RED) | SME validation |

These risks explicitly require HUMAN validation, not additional AI cycles.

### Plan Governance Model Reference
From plan v3.0 Section 10.1 RACI Matrix:

| Activity | Responsible | Accountable | Consulted | Informed |
|----------|-------------|-------------|-----------|----------|
| Accuracy Validation | SME | User | - | Claude Code |

SME (user) is responsible for accuracy validation, not Claude Code.

---

## Related Decisions

- ADR-002: Dog-fooding approach (to be created)
- Plan v3.0 Section 10: Governance Model
- Risk Assessment: R-01, R-06, R-11

---

*Decision Author: Claude Code (Opus 4.5)*
*Reviewed By: Pending user review*
*Date: 2026-01-09*
