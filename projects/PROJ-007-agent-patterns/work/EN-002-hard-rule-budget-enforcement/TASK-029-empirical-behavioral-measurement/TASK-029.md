# TASK-029: Empirical Behavioral Measurement of Enforcement Effectiveness

## Document Sections

| Section | Purpose |
|---------|---------|
| [Metadata](#metadata) | Type, status, priority, parent |
| [Summary](#summary) | What and why |
| [Scope](#scope) | Implementation steps |
| [Acceptance Criteria](#acceptance-criteria) | Done conditions |
| [Dependencies](#dependencies) | Blocks and blocked-by |
| [History](#history) | Change log |

---

## Metadata

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Criticality:** C2 (standard — reversible, research scope)
> **Parent:** EN-002
> **Source:** DEC-005 (deferred empirical measurement), C4 Tournament S-014 Round 3 (Evidence Quality gap)
> **Created:** 2026-02-21T23:50:00Z

---

## Summary

EN-002 improved HARD rule enforcement from 32% to 84% L2 coverage — but this is a structural metric, not a behavioral one. The structural-proxy acceptance argument (documented in en-002-implementation-summary.md) explains why structural coverage is a valid proxy, but empirical validation would strengthen the evidence.

This task creates a behavioral measurement baseline: how often do Tier B rules (H-04, H-16, H-17, H-18 — the 4 rules without L2 engine protection) fail to be followed in actual LLM sessions at context depth?

---

## Scope

1. **Design measurement protocol**: Define what "enforcement failure" means operationally for each Tier B rule. Identify observable signals in session transcripts or outputs.
2. **Establish pre-EN-002 baseline**: Using archived session transcripts (if available) or controlled experiments, measure Tier B rule compliance rates before L2 engine expansion.
3. **Measure post-EN-002 compliance**: Run N controlled sessions at varying context depths (10K, 50K, 100K tokens). Record compliance signals for all Tier A and Tier B rules.
4. **Compare and report**: Statistical comparison of Tier A (L2-protected) vs Tier B (compensating controls only) compliance rates. Report with confidence intervals.

---

## Acceptance Criteria

- [ ] Measurement protocol documented (what signals, what counts as failure)
- [ ] Post-EN-002 measurement data collected (minimum N=10 sessions per depth level)
- [ ] Tier A vs Tier B compliance rates compared with statistical significance test
- [ ] Results documented in `enforcement-behavioral-measurement-report.md`
- [ ] Results referenced from EN-002 implementation summary Evidence Quality section

---

## Dependencies

### Depends On

- EN-002 (DONE) — structural changes must be in place before behavioral measurement

### Blocks

- None (this is a follow-up measurement task, not a blocking dependency)

---

## Related Items

- **Parent:** [EN-002](../EN-002.md)
- **Source Decision:** DEC-005 (deferred empirical measurement)
- **Related:** [TASK-028](../TASK-028-measure-effectiveness/TASK-028.md) (structural measurement, completed)
- **Evidence Gap:** C4 Tournament S-014 Round 3 (Evidence Quality 0.86, primary bottleneck)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-21 | Created | Created during C4 Tournament Round 4 to track deferred empirical measurement (DEC-005). Addresses Evidence Quality gap identified by S-014 scoring. |
