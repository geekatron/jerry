# STORY-019 Updated Acceptance Criteria with UX Enhancements

> Revised acceptance criteria based on Nielsen heuristic evaluation. These updates address documentation usability gaps while keeping the story achievable within effort estimate 5 (or 6 if DX improvements are prioritized).

## Format Note

Original STORY-019 acceptance criteria are marked **[ORIGINAL]**. Updated/new criteria are marked **[NEW]**. Optional criteria that increase effort are marked **[OPTIONAL +N]**.

---

## /diataxis (Documentation Quality)

**[ORIGINAL]**
- [ ] Migration guide follows how-to format: goal statement, prerequisites, numbered steps, no explanation of why
- [ ] Tier selection reference follows reference format: structured, neutral, complete, mirrors the tier model
- [ ] No quadrant mixing: how-to doesn't explain theory; reference doesn't include tutorials
- [ ] Both documents pass diataxis-auditor quality check

**[NEW]**
- [ ] Quick-reference card has clear one-page structure: card header (option chosen + rationale), lookup table (agent → old tier → new tier → action), footer (cross-references)
- [ ] How-to guide introduces the explainer: "This guide assumes you've read the Tier Model Options Explainer..."
- [ ] Quick-reference card introduces the how-to guide in footer: "For step-by-step migration, see the Tier Migration Guide"

---

## /user-experience (ux-heuristic-evaluator): Documentation DX

**[ORIGINAL]**
- [ ] Migration guide answers "what do I need to do?" in < 2 minutes of reading
- [ ] Tier selection reference provides a decision flowchart or decision table
- [ ] The T3/T4 swap is explained in one paragraph with a before/after comparison
- [ ] No Nielsen severity 3+ findings in documentation DX review
- [ ] Worked examples use real agents (not hypothetical) to illustrate tier selection

**[NEW — H2: Real-world match]** [OPTIONAL +0.25]
- [ ] Technical terms from the explainer (monotonic total order, lattice, partial order) are explained in plain language in the how-to guide glossary
- [ ] OR how-to guide avoids these terms and uses plain-English analogies instead (e.g., "stacked in a line" vs. "monotonic total order")

**[NEW — H3: Control & freedom]** [OPTIONAL +0.25]
- [ ] How-to guide includes "Rollback" section: how to revert changes if something breaks
- [ ] Rollback section specifies Git commands and what to check after revert

**[NEW — H5: Error prevention]** [OPTIONAL +0.25]
- [ ] How-to guide or quick-reference card includes conflict-resolution guidance: "If you want [competing priorities], here's the guidance"
- [ ] Example: "I want minimal governance change AND exact-fit tiers" → recommendation on which option best matches

**[NEW — H7: Efficiency of use]** [REQUIRED]
- [ ] Quick-reference card available as one-page lookup (agent name → new tier), enabling authors to skip the full explainer if they only need a tier lookup
- [ ] Quick-reference card linked from /diataxis skill intro and the how-to guide intro

**[NEW — H9: Error recovery]** [OPTIONAL +0.25]
- [ ] How-to guide includes "Troubleshooting" section covering common mistakes:
  - [ ] "I updated my `.md` file but the agent still shows the old tier" → Check `.governance.yaml`, not just the `.md`
  - [ ] "My agent failed validation" → Most common cause: schema mismatch; how to diagnose
  - [ ] "My agent is over-provisioned now" → Explanation of why (trade-off of the chosen option)

**[NEW — H10: Documentation orientation]** [OPTIONAL +0.1]
- [ ] All three documents (explainer, migration guide, quick-reference card) cross-link each other in their introductions
- [ ] Clear statement: "Read the Explainer for complete comparison → How-to Guide for step-by-step migration → Quick-Reference Card for tier lookup"

---

## /problem-solving (ps-researcher): Reference Sweep

**[ORIGINAL]**
- [ ] All tier references in `skills/*/SKILL.md` identified and updated
- [ ] All tier references in `AGENTS.md` identified and updated
- [ ] All tier references in `docs/knowledge/` identified and updated
- [ ] All tier references in `.context/rules/prompt-*.md` identified and updated
- [ ] Grep verification: no remaining references to "T3 (External)" or "T4 (Persistent)" with old meanings

**[No changes — this is technically solid]**

---

## Summary of Optional Enhancements

| Enhancement | Heuristic | Effort | Priority |
|-------------|-----------|--------|----------|
| Glossary of technical terms | H2 | +0.25 | Medium |
| Rollback procedure | H3 | +0.25 | Medium |
| Conflict-resolution guide | H5 | +0.25 | Low |
| Quick-reference card | H7 | (already 0.5) | **High** |
| Troubleshooting section | H9 | +0.25 | Medium |
| Documentation cross-links | H10 | +0.1 | Low |

**Total optional effort: 1.1**

**Recommendation:**
- **REQUIRED (Keeps effort = 5):** Quick-reference card, cross-links
- **RECOMMENDED (Increases effort to 5.5):** Glossary, Rollback procedure, Troubleshooting section
- **OPTIONAL (Increases effort to 6):** Conflict-resolution guide

---

## Deliverables: Original vs. Updated

### Original STORY-019 Deliverables

| Document | Type | Effort |
|----------|------|--------|
| Tier Migration Guide | How-to (diataxis) | 1.5 |
| Tier Selection Reference | Reference (diataxis) | 1.5 |
| DX Review | Evaluation | 0.5 |
| File Updates | Textual changes | 2.0 |
| Overhead | Coordination | 0.5 |
| **Total** | | **5.5** |

### Updated STORY-019 Deliverables

| Document | Type | Effort | Notes |
|----------|------|--------|-------|
| Tier Migration Guide | How-to (diataxis) | 1.5 | Same, but add glossary + rollback + troubleshooting if RECOMMENDED option chosen |
| Tier Quick-Reference Card | Lookup card (diataxis, ~1 page) | 0.5 | Replaces full reference; enables express lane |
| DX Review | Evaluation | 0.5 | Same, but now reviews both new documents |
| File Updates | Textual changes | 2.0 | Same |
| Overhead & Cross-linking | Coordination | 0.5 | Same |
| **Total (Base)** | | **5.0** | |
| **+ Recommended enhancements** | (glossary, rollback, troubleshooting) | **+0.5** | Brings total to 5.5 |
| **+ Optional enhancements** | (conflict-resolution) | **+0.5** | Brings total to 6.0 |

---

## Effort Impact Analysis

| Scenario | Total Effort | Notes |
|----------|--------------|-------|
| **Scope as revised, base only** | 5.0 | No UX enhancements beyond original acceptance criteria. Sufficient for minimum acceptable usability. |
| **Scope + recommended enhancements** | 5.5 | Addresses top 5 Nielsen heuristics. Significant UX improvement. Recommended path. |
| **Scope + all enhancements** | 6.0 | Addresses all 10 Nielsen heuristics. Comprehensive documentation. Worth it if timeline allows. |

**Recommendation:** Target effort 5.5 (base + recommended enhancements). This balances usability improvement with schedule.

---

## Updated Tasks Breakdown

| Task | Original | Updated | Effort | Notes |
|------|----------|---------|--------|-------|
| TASK-001 | Grep sweep + verify | Same | 0.5 | No change |
| TASK-002 | Update SKILL.md files | Same | 1.5 | No change |
| TASK-003 | Update AGENTS.md | Same | 0.5 | No change |
| TASK-004 | Write migration guide | + Glossary, rollback, troubleshooting | 1.75 (+0.25) | +0.25 if recommended enhancements |
| TASK-005 | Write tier selection reference | Write quick-reference card | 0.5 | Net -1 (reference was 1.5, card is 0.5) |
| TASK-006 | DX review | Evaluate both new docs + optional items | 0.5-0.75 | +0.25 if enhancements included |
| Overhead | Coordination | + Cross-linking docs | 0.5-0.6 | +0.1 for cross-link review |

---

## Revised Story Definition Template

Use this to update STORY-019 in the worktracker:

```markdown
## Documentation Scope (REVISED)

### P1: Existing File Updates
[No change to original — sweep and update ~10 files]

### P1: New Documentation (REVISED)
| Document | Diataxis Quadrant | Purpose | Format |
|----------|---|---|---|
| Tier Migration Guide | **How-to** | Goal: Update your agent's tier after renumbering. Format: prerequisites, numbered steps, glossary, rollback, troubleshooting. Length: 2-3 pages. |
| Tier Quick-Reference Card | **Reference** (1-page) | Goal: Fast lookup of agent name → new tier. Format: table with agent names and tier assignments. Length: 1 page. |

## Acceptance Criteria (REVISED)
[Use updated criteria from the "Updated Acceptance Criteria" section above]

## Deliverables
1. Updated SKILL.md files (9 files)
2. Updated AGENTS.md (1 line)
3. Tier Migration Guide (how-to, 2-3 pages)
4. Tier Quick-Reference Card (1 page)
5. DX Review Report (Nielsen heuristic evaluation, pass/fail per criteria)

## Effort
- Base: 5 story points
- + Recommended enhancements (glossary, rollback, troubleshooting): +0.5
- Target: 5.5 story points

## Dependencies
STORY-017 (tier model decision), STORY-018 (YAML migration)
```

---

*Validation completed per `/user-experience` skill methodology (Nielsen H1-H10 heuristic evaluation applied to documentation UX). Single evaluator assessment. Effort estimates are conservative and assume 10-15% overhead for meetings and communication.*
