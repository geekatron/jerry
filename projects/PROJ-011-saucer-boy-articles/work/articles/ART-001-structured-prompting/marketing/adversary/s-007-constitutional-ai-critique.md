# S-007 Constitutional AI Critique — Marketing Deliverables

**Strategy:** S-007 Constitutional AI Critique
**Deliverables:** `work/marketing/slack-message.md`, `work/marketing/medium-article.md`
**Criticality:** C2 (marketing materials promoting a published blog post)
**Date:** 2026-02-24
**Reviewer:** adv-executor (S-007)

---

## Applicable Principles

1. **Truthfulness** (P-022): All factual claims must be accurate
2. **Attribution accuracy**: Research citations must not be misrepresented
3. **Honest framing**: Content must not be misleading
4. **Responsible advice**: Recommendations must not lead readers astray
5. **Vendor neutrality**: Claims must be genuinely model-agnostic
6. **Anti-sycophancy**: No manipulative flattery or fear-based persuasion

---

## Findings Summary

| ID | Deliverable | Severity | Principle | Status |
|----|------------|----------|-----------|--------|
| S-007-001 | Slack | MINOR | Attribution accuracy | Open — Slack uses "I call it" (correct) |
| S-007-002 | Slack | MINOR | Accuracy (nuance) | Acceptable simplification |
| S-007-003 | Slack | OBSERVATION | Honest framing | "banana suit" detail may be apocryphal |
| S-007-004 | Slack | OBSERVATION | Vendor neutrality | COMPLIANT |
| S-007-005 | Slack | OBSERVATION | Responsible advice | COMPLIANT |
| S-007-006 | Slack | MINOR | Accuracy (claim scope) | Acceptable ("most people miss") |
| S-007-007 | Medium | MAJOR | Attribution accuracy | **ALREADY FIXED** — current article says "a shorthand I started using after reading Bender and Koller" |
| S-007-008 | Medium | MINOR | Attribution (date) | Open — Sharma et al. date omitted inline |
| S-007-009 | Medium | MINOR | Accuracy (nuance) | Acceptable anthropomorphization |
| S-007-010 | Medium | OBSERVATION | Truthfulness | COMPLIANT (Wei et al.) |
| S-007-011 | Medium | OBSERVATION | Truthfulness | COMPLIANT (Panickssery et al.) |
| S-007-012 | Medium | MINOR | Accuracy (scope qualifier) | Open — Liu et al. scope qualifier missing |
| S-007-013 | Medium | OBSERVATION | Honest framing | COMPLIANT ("When This Breaks") |
| S-007-014 | Medium | OBSERVATION | Vendor neutrality | COMPLIANT |
| S-007-015 | Both | OBSERVATION | Anti-sycophancy | COMPLIANT |
| S-007-016 | Medium | MAJOR | Responsible advice | **VALID** — tool-access caveat missing from Level 3 |
| S-007-017 | Medium | MINOR | Accuracy (omission) | Open — "why universally" present but underdeveloped |
| S-007-018 | Medium | MINOR | Accuracy (omission) | **ALREADY FIXED** — error propagation added in iteration 4 |

---

## Active Findings After Cross-Reference

### MAJOR (1 remaining after cross-reference)

**S-007-016 | Missing tool-access caveat for Level 3**

The Level 3 prompt example says "research the top 10 industry frameworks using real sources — not training data" which requires web search or tool access. The blog post includes a caveat: "That Level 3 prompt assumes a model with tool access: file system, web search, the works. If you're in a plain chat window, paste the relevant code and verify citations yourself." The Medium article omits this entirely.

A reader following Level 3 advice in a plain chat interface will expect capabilities the model doesn't have, leading to hallucinated sources presented as real research. This is a responsible-advice concern.

**Recommendation:** Add after Level 3 prompt: "That prompt assumes a model with tool access — file system, web search, the works. If you're in a plain chat window, paste the relevant code and verify citations yourself. Same principles, different mechanics."

### MINOR (open items)

- **S-007-012:** Liu et al. finding presented as general when it was demonstrated on retrieval tasks. Consider "In document retrieval tasks, Liu et al. found..."
- **S-007-017:** "Why universally" paragraph present (added iteration 5) but underdeveloped per S-014 scoring
- **S-007-008:** Sharma et al. date omitted inline (acceptable for marketing)

---

## Overall Assessment

Both deliverables are substantively honest, vendor-neutral, non-manipulative, and responsibly framed. Research citations are directionally accurate — no findings are misrepresented. The "When This Breaks" section demonstrates genuine intellectual honesty.

One remaining MAJOR: the tool-access caveat (S-007-016) is a straightforward fix. The S-007-007 and S-007-018 findings were already addressed in prior scoring iterations.

---

*Constitutional AI Critique completed by adv-executor | S-007 | C4 adversarial tournament*
*Note: Agent worked from a potentially stale file snapshot. Status column reflects cross-reference against current article state.*
