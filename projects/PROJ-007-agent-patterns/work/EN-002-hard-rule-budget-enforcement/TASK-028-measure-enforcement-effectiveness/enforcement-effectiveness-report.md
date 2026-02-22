# EN-002: Enforcement Effectiveness Measurement Report

> **Date:** 2026-02-21
> **Task:** TASK-028
> **Parent:** EN-002
> **Method:** Pre/post comparison of enforcement metrics

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Key findings |
| [Pre-EN-002 Baseline](#pre-en-002-baseline) | Metrics before implementation |
| [Post-EN-002 Metrics](#post-en-002-metrics) | Metrics after implementation |
| [Comparison](#comparison) | Side-by-side improvement analysis |
| [Conclusions](#conclusions) | Assessment and next steps |

---

## Summary

EN-002 achieved its primary objectives: L2 engine coverage increased from 32% to 84% of HARD rules, the rule count was reduced from 31 to 25 (matching the derived ceiling), and L5 CI enforcement prevents future silent ceiling breaches.

---

## Pre-EN-002 Baseline

| Metric | Value |
|--------|-------|
| HARD rule count | 31 |
| HARD rule ceiling | 35 (unprincipled) |
| Ceiling utilization | 89% (31/35) |
| L2 engine source | 1 file (quality-enforcement.md) |
| L2 markers processed | 8 |
| H-rules with L2 coverage | ~10 (32%) |
| L2 token usage | ~415 tokens/prompt |
| L2 token budget | 600 (declared) |
| L5 ceiling enforcement | None |
| Tier classification | None |

---

## Post-EN-002 Metrics

| Metric | Value |
|--------|-------|
| HARD rule count | 25 |
| HARD rule ceiling | 25 (derived from 3 constraint families) |
| Ceiling utilization | 100% (25/25, 0 headroom) |
| L2 engine source | 9 files (all .context/rules/*.md) |
| L2 markers processed | 16 |
| H-rules with L2 coverage (Tier A) | 21 (84%) |
| H-rules without L2 coverage (Tier B) | 4 (16%) — H-04, H-16, H-17, H-18 |
| L2 token usage | 559 tokens/prompt |
| L2 token budget | 850 |
| L2 budget utilization | 65.8% (291 tokens remaining) |
| L5 ceiling enforcement | Active (pre-commit hook + test) |
| Tier classification | Tier A (21) + Tier B (4) |

---

## Comparison

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| HARD rule count | 31 | 25 | -6 (19% reduction) |
| Ceiling | 35 | 25 | Principled derivation |
| L2 file coverage | 1 file | 9 files | +8 files |
| L2 markers | 8 | 16 | +8 (100% increase) |
| L2 H-rule coverage | ~10 (32%) | 21 (84%) | +11 rules (+52pp) |
| L2 tokens/prompt | ~415 | 559 | +144 tokens (34.7% increase) |
| L5 enforcement | None | CI gate | New capability |
| Context rot protection | Vulnerable (21 rules) | Vulnerable (4 rules) | -17 rules at risk |

### Key Improvements

1. **L2 coverage tripled:** 32% → 84% of HARD rules now have per-prompt L2 reinforcement
2. **Context rot exposure reduced:** 21 → 4 rules without L2 protection (81% reduction in vulnerable rules)
3. **Principled ceiling:** Unprincipled 35 → derived 25 with documented justification
4. **L5 enforcement added:** Deterministic CI gate prevents future silent breaches
5. **Token efficiency:** 559/850 = 65.8% budget utilization with room for future markers

### Remaining Gaps

1. **Zero headroom:** 25/25 rules at ceiling — no room for EN-001 H-32..H-35 without exception mechanism
2. **4 Tier B rules:** H-04, H-16, H-17, H-18 rely on compensating controls only
3. **L2 budget headroom:** 291 tokens available — sufficient for 4-6 additional markers if needed

---

## Conclusions

EN-002 successfully addressed both discoveries:

- **DISC-001 (unprincipled ceiling):** Ceiling updated to derived value of 25 with documented justification, two-tier model, and exception mechanism.
- **DISC-002 (L2 engine coverage gap):** Engine expanded to read all 9 auto-loaded rule files. L2 coverage increased from 32% to 84%.

**Recommendation:** Per DEC-005, further optimization (adding L2 markers for Tier B rules) should be driven by empirical evidence of enforcement failures in H-04, H-16, H-17, or H-18. Current compensating controls (SessionStart hook for H-04, skill enforcement for H-16/H-17/H-18) provide adequate protection.

**EN-001 dependency note:** TASK-016 (H-32..H-35 integration) requires the exception mechanism to temporarily expand the ceiling from 25 to 29 (N=4 exceeds N<=3 maximum). Alternative: further consolidation to create headroom before adding new rules.
