# Iteration 4 Changelog

> **Date:** 2026-03-02
> **Trigger:** S-014 rescoring iteration 3 (D1=0.934, D2=0.942) — below 0.95 target
> **Deliverables:** D1 (orchestration-mega-prompt-template.md), D2 (orchestration-behavioral-constraints.md)

## Fixes Applied

### Fix 1: Broken empirical source path in D1 header (Priority 1)

**Finding:** S-014 iteration 3 identified `ab-testing/comparative-effectiveness.md` as a non-existent path. Actual file is at `phase-2/comparative-effectiveness.md`.

**D1 changes:**
- Line 7 (header blockquote): `ab-testing/comparative-effectiveness.md` → `phase-2/comparative-effectiveness.md`
- Line 140 (code fence comment block): `ab-testing/` → `phase-2/`

### Fix 2: Broken empirical source path in D2 header (Priority 1)

**D2 changes:**
- Line 5 (header blockquote): `ab-testing/comparative-effectiveness.md` → `phase-2/comparative-effectiveness.md`

### Fix 3: Inconsistent table name reference in D1 (Priority 2)

**Finding:** Line 472 references "Constraint Index table" but the actual table heading is "Constraint Inventory".

**D1 changes:**
- Line 472: "Constraint Index table above" → "Constraint Inventory table above"

### Fix 4: L2-REINJECT marker inaccuracy in D2 (Priority 2)

**Finding:** L2-REINJECT marker (line 7) said "C3+ only" but AQ-1 and AQ-2 were updated to C2+ enforcement in iteration 1.

**D2 changes:**
- Line 7: Removed "C3+ only" from L2-REINJECT marker; added "C2+ enforcement" annotations to AQ-1 and AQ-2 entries

## Verification

- `phase-2/comparative-effectiveness.md` confirmed present via Glob search
- All 5 edit locations confirmed via Grep search before applying
- No other occurrences of `ab-testing/` remain in deliverable files
