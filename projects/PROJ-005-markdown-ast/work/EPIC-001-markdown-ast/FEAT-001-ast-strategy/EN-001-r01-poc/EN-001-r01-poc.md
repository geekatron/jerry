# EN-001: R-01 Proof-of-Concept -- mdformat Blockquote Frontmatter Write-Back

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** exploration
> **Created:** 2026-02-20
> **Due:** --
> **Completed:** 2026-02-20
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this PoC validates |
| [Problem Statement](#problem-statement) | Why R-01 is the critical gate |
| [Business Value](#business-value) | What this enabler unlocks |
| [Technical Approach](#technical-approach) | PoC implementation and decision tree |
| [Acceptance Criteria](#acceptance-criteria) | Pass/fail conditions |
| [Risks and Mitigations](#risks-and-mitigations) | Fallback escalation ladder |
| [Dependencies](#dependencies) | What depends on this |
| [Related Items](#related-items) | Hierarchy and traceability |
| [History](#history) | Status changes |

---

## Summary

Validate that mdformat's plugin API can handle blockquote frontmatter write-back -- the one critical interaction not validated during SPIKE-001/SPIKE-002 research. This is the hard gate for the entire AST-first architecture. If R-01 passes, confidence rises from 0.75 to ~0.90 and all implementation stories are unblocked. If it fails, the fallback escalation ladder activates.

**Technical Scope:**
- Parse a real Jerry WORKTRACKER entity file with markdown-it-py
- Extract blockquote frontmatter key-value pairs
- Modify the `Status` field value
- Render back with mdformat
- Verify roundtrip fidelity (modified field correct, unmodified regions preserved)

---

## Problem Statement

Jerry's blockquote frontmatter (`> **Key:** Value`) is non-standard markdown. No library natively parses it as structured data. SPIKE-001 confirmed that all viable libraries require a custom extension for extraction (~220 LOC). However, **write-back** (modifying a field and rendering the document back) was not empirically validated. mdformat normalizes output, and we need to verify that:

1. Modified frontmatter fields render correctly
2. Unmodified regions are byte-for-byte identical (or only have acceptable whitespace normalization)
3. mdformat's HTML-equality verification passes

This is the single highest-risk unknown in the AST-first approach.

---

## Business Value

### Features Unlocked

- All 10 FEAT-001 implementation stories (ST-001 through ST-010)
- Schema validation for WORKTRACKER entities
- Structured AST manipulation of Jerry markdown files
- Pre-commit validation hooks

If R-01 fails and no fallback resolves it, the NO-GO Alternative 1 (Enhanced Template System) is pursued instead, saving ~1,340 LOC of wasted effort.

---

## Technical Approach

### PoC Implementation

```python
# R-01 Proof-of-Concept Script
# Run: uv run python scripts/r01-poc.py

from markdown_it import MarkdownIt
import mdformat

# 1. Parse a real Jerry entity file
with open("projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/"
          "FEAT-001-ast-strategy/SPIKE-002-feasibility/SPIKE-002-feasibility.md") as f:
    source = f.read()

md = MarkdownIt()
tokens = md.parse(source)

# 2. Find and modify the Status field in blockquote frontmatter
# (Custom extraction logic -- the core of the PoC)

# 3. Render back with mdformat
rendered = mdformat.text(modified_source)

# 4. Verify roundtrip
# CHECK 1: Modified field renders correctly
# CHECK 2: Unmodified regions preserved
# CHECK 3: mdformat HTML-equality verification passes
```

### R-01 Decision Tree

```
R-01: Blockquote frontmatter write-back validation
======================================================

PROOF-OF-CONCEPT (Days 1-3):
  Test: Parse SPIKE-002-feasibility.md
        Modify Status: pending -> completed
        Render back with mdformat
        Compare output

  CHECK 1: Does the modified field render correctly?
  +-- YES -> CHECK 2
  +-- NO  -> ESCALATE to Fallback A

  CHECK 2: Are unmodified regions byte-for-byte identical?
  +-- YES -> CHECK 3
  +-- NO  -> Assess: is the diff acceptable normalization?
             +-- YES (whitespace only) -> CHECK 3 (with normalization caveat)
             +-- NO  (semantic change) -> ESCALATE to Fallback A

  CHECK 3: Does mdformat HTML-equality verification pass?
  +-- YES -> R-01 RESOLVED: Proceed with standard implementation
  +-- NO  -> ESCALATE to Fallback A

FALLBACK A: String-level substitution (Days 3-4)
  Implementation: ~50 LOC regex-based field substitution
  Same checks (1, 2, 3) applied
  +-- All pass -> R-01 RESOLVED with fallback
  +-- Any fail -> ESCALATE to Fallback B

FALLBACK B: Mistletoe stack (Days 4-5)
  Implementation: ~200 LOC domain layer rewrite
  Same checks (1, 2, 3) applied
  +-- All pass -> R-01 RESOLVED with library switch
  +-- Any fail -> ESCALATE to Fallback C

FALLBACK C: Hybrid renderer (Week 2)
  Implementation: ~400 LOC custom renderer for modified sections
  +-- Pass -> R-01 RESOLVED with hybrid approach
  +-- Fail -> DECISION: NO-GO for AST. Pursue Alternative 1.

TIMELINE GATE: If R-01 is not resolved by end of Week 2,
               STOP and pursue NO-GO Alternative 1.
```

---

## Acceptance Criteria

### Definition of Done

- [x] PoC script implemented and runnable via `uv run`
- [x] All 3 checks pass (field renders, regions preserved, HTML-equality)
- [x] Test against at least 3 representative Jerry files (Spike, Epic, Enabler entity types)
- [x] Decision documented: which path was taken (standard / Fallback A / B / C / NO-GO)
- [x] Results committed to repository

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Modified blockquote frontmatter field renders correctly after mdformat roundtrip | [x] |
| TC-2 | Unmodified document regions are preserved (byte-for-byte or acceptable normalization) | [x] |
| TC-3 | mdformat HTML-equality verification passes on the full document | [x] |
| TC-4 | PoC works on 3+ representative Jerry file types | [x] |
| TC-5 | Decision and evidence documented | [x] |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| mdformat normalizes blockquote content destructively | Medium | High | Fallback A: string-level substitution within AST framework |
| mdformat reflows code blocks or tables | Low | High | Fallback A: targeted string substitution for affected regions |
| All library approaches fail write-back | Very Low | Critical | NO-GO path: pursue Alternative 1 (Enhanced Template System) |
| PoC passes but production edge cases fail | Medium | Medium | Expand test corpus to 10+ files before committing to full implementation |

---

## Dependencies

### Depends On

- [SPIKE-001: Library Landscape](../SPIKE-001-library-landscape/SPIKE-001-library-landscape.md) (completed)
- [SPIKE-002: Feasibility Assessment](../SPIKE-002-feasibility/SPIKE-002-feasibility.md) (completed)

### Enables

- [ST-001: JerryDocument facade](../ST-001-jerry-document/ST-001-jerry-document.md)
- [ST-002: Blockquote frontmatter extension](../ST-002-frontmatter-ext/ST-002-frontmatter-ext.md)
- All subsequent implementation stories (ST-003 through ST-010)

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)

### Traceability

- **Source:** Go/No-Go Recommendation R-01 Decision Tree (`orchestration/spike-eval-20260219-001/ps/phase-6-decision/ps-synthesizer-002/go-nogo-recommendation.md`)
- **Quality Gate:** QG2 passed at 0.97 (SPIKE-002 go-nogo recommendation quality gate, scored during orchestration `spike-eval-20260219-001`)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-20 | Claude | pending | Enabler created. Critical gate for AST-first architecture. Validates mdformat blockquote frontmatter write-back. 3 SP. |
| 2026-02-20 | Claude | in-progress | PoC implementation started. Added markdown-it-py, mdformat, mdit-py-plugins dependencies. |
| 2026-02-20 | Claude | completed | R-01 PASS. All 3 checks pass across 6 test cases (3 entity types + 3 field types). Adversarial review (S-010 + S-014) completed; all 7 findings addressed (SR-001 critical sign inversion fixed, SR-002 confidence grounded, SR-003 scope documented, SR-004 parents[6] documented, SR-005/006/007 minor fixes). Proceed with standard implementation. |
