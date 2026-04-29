# EN-008: Final `/adversary` C4 tournament

> **Type:** enabler
> **Enabler Type:** compliance
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** EPIC-001
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Enabler delivers |
| [Technical Approach](#technical-approach) | C4 tournament methodology |
| [Tournament Configuration](#tournament-configuration) | All 10 strategies, C4 protocol |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

After Phase 7 docs land, run a final `/adversary` C4 tournament against the merged Epic deliverable. C4 = all 10 selected adversarial strategies executed (S-001 Red Team, S-002 Devil's Advocate, S-003 Steelman, S-004 Pre-Mortem, S-007 Constitutional AI Critique, S-010 Self-Refine, S-011 Chain-of-Verification, S-012 FMEA, S-013 Inversion, S-014 LLM-as-Judge). Threshold: weighted composite ≥0.95.

This Enabler is **Phase 8** of the orchestration plan — final acceptance gate before EPIC-001 closes.

---

## Technical Approach

Run a C4 tournament against the merged Epic deliverable using the full `/adversary` skill chain: adv-selector → adv-executor (executes all 10 selected strategies) → adv-scorer (S-014 LLM-as-Judge weighted composite + dimension scores). FC-M-001 fresh-context second-reviewer runs independently to prevent anchoring. Reproduction test: re-run the audit author's original 9-iteration scenario; composite must reach ≥0.95 (the original ceiling at 0.90 must be broken). The Tournament Configuration section below specifies thresholds and protocol details.

---

## Tournament Configuration

| Aspect | Decision |
|--------|----------|
| Mode | C4 (all 10 strategies, tournament scoring) |
| Threshold | ≥0.95 weighted composite (S-014 LLM-as-Judge primary) |
| Iteration ceiling | 10 (per RT-M-010 C4) |
| Plateau detection | delta < 0.01 for 3 consecutive iterations triggers escalation per AE-006 |
| Fresh-context reviewer | C4 requires second independent reviewer per FC-M-001 |
| Scope | The merged Epic deliverable — all artifacts, ADRs, validators, schemas, agent prompts, hook integrations, docs |
| Reviewers | adv-selector + adv-executor + adv-scorer (full skill chain) |
| Escalation | If composite remains <0.95 after iteration 10, escalate to user with current state, blockers, and proposed scope adjustments |

This is the **same protocol** the audit author ran on the original packet — and the same protocol that surfaced #273 in the first place. By using C4 ≥0.95 here, we close the same gate that detected the gaps and prove they're closed.

---

## Acceptance Criteria

- [ ] All 10 strategies executed (S-001..S-014 selected set per `quality-enforcement.md`).
- [ ] S-014 LLM-as-Judge weighted composite ≥0.95.
- [ ] Per-dimension scores: Completeness ≥0.95, Internal Consistency ≥0.95, Methodological Rigor ≥0.95, Evidence Quality ≥0.92, Actionability ≥0.92, Traceability ≥0.95.
- [ ] FC-M-001 second-reviewer independent run also scores ≥0.95.
- [ ] Tournament report at `work/EPIC-001-transcript-hardening/EN-008-final-adversary-tournament/tournament-report.md` with full strategy outputs and dimension scores.
- [ ] Zero remaining Critical findings; Major findings either remediated or explicitly accepted with documented rationale.
- [ ] **Reproduction test:** Re-run the audit author's original 9-iteration scenario (with their packet, if available, or a synthetic equivalent). Composite should now reach ≥0.95 — the original ceiling at 0.90 is broken.
- [ ] EPIC-001 close-out: Issue #273 closed with comment linking to this tournament report + reproduction test result.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | adv-selector: select C4 strategy set | pending |
| TASK-002 | adv-executor: execute all 10 strategies | pending |
| TASK-003 | adv-scorer: S-014 weighted composite + dimension scores | pending |
| TASK-004 | FC-M-001 second-reviewer fresh-context run | pending |
| TASK-005 | Author tournament report | pending |
| TASK-006 | Reproduce audit author's 9-iter scenario; verify ≥0.95 reachable | pending |
| TASK-007 | Close issue #273 with summary comment | pending |
| TASK-008 | Move EPIC-001 to completed | pending |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | All Features (FEAT-001..FEAT-005) | Tournament evaluates merged deliverable |
| Blocked By | EN-004, EN-005, EN-006 | All cross-cutting enablers must close (threat model remediation, UX synthesis, documentation set) |
| Blocks | EPIC-001 closure | Final gate |
| Blocks | Issue #273 closure | This tournament's report is the closure evidence |

### Source

- User direction: "/adversary C4 ≥0.95 protocol"

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Cross-cutting Enabler created. Final gate. Same protocol that surfaced #273 — closing the same gate that detected the gaps. |
