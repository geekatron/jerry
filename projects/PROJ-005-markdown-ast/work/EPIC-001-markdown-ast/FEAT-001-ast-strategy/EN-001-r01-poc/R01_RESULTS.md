# R-01 Proof-of-Concept Results

> **Date:** 2026-02-20
> **Verdict:** PASS -- Proceed with standard implementation
> **Fallback activated:** None
> **Confidence post-R-01:** ~0.90 (up from 0.75)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Verdict and key findings |
| [Test Matrix](#test-matrix) | Per-file check results |
| [Token Analysis](#token-analysis) | AST parsing diagnostics |
| [Key Observations](#key-observations) | What we learned |
| [Normalization Behavior](#normalization-behavior) | How mdformat changes files |
| [Decision](#decision) | Path forward |
| [Evidence](#evidence) | Traceability |
| [Captured Execution Output](#captured-execution-output) | Full PoC stdout |
| [Adversarial Review](#adversarial-review) | Quality gate artifacts |

---

## Summary

The R-01 proof-of-concept validates that markdown-it-py v4.0.0 + mdformat v1.0.0 can successfully:

1. **Parse** real Jerry entity files (Spike, Epic, Enabler) into token streams
2. **Extract** blockquote frontmatter key-value pairs via regex on the `> **Key:** Value` pattern
3. **Modify** a frontmatter field (Status) in the normalized source
4. **Render** back with mdformat preserving all unmodified regions byte-for-byte
5. **Verify** mdformat roundtrip idempotency (stable after 2nd pass)

All 3 checks passed across all 3 test files. No fallback escalation required.

---

## Test Matrix

| File | Type | Fields | C1: Field Correct | C2: Regions Preserved | C3: Idempotent | Result |
|------|------|:------:|:-:|:-:|:-:|:------:|
| SPIKE-002-feasibility.md | Spike | 8 | PASS | PASS | PASS | **PASS** |
| EPIC-001-markdown-ast.md | Epic | 10 | PASS | PASS | PASS | **PASS** |
| EN-001-r01-poc.md | Enabler | 11 | PASS | PASS | PASS | **PASS** |

### Check Definitions

| Check | What it validates |
|-------|-------------------|
| C1 | Modified field value appears correctly in rendered output |
| C2 | After reverting the modified field, rendered output is byte-for-byte identical to the mdformat-normalized original |
| C3 | A second mdformat pass produces identical output (idempotency = proxy for HTML-equality) |

---

## Token Analysis

| File | Tokens | Blockquote Nodes | Tree Depth | Frontmatter Fields |
|------|:------:|:----------------:|:----------:|:------------------:|
| SPIKE-002 | 390 | 1 | 7 | 8 |
| EPIC-001 | 144 | 1 | 6 | 10 |
| EN-001 | 246 | 1 | 6 | 11 |

markdown-it-py correctly identifies blockquote nodes in all files. The SyntaxTreeNode API provides structured tree access with reasonable depth (6-7 levels).

---

## Key Observations

### 1. mdformat normalization adds content

All 3 files grew after mdformat normalization:
- SPIKE-002: +406 chars (4.8% larger)
- EPIC-001: +537 chars (8.6% larger)
- EN-001: +671 chars (8.5% larger)

This is expected behavior -- mdformat normalizes whitespace, list formatting, and table alignment. The normalization is consistent and idempotent.

### 2. Blockquote frontmatter format

The Jerry blockquote frontmatter pattern `> **Key:** Value` has the colon *inside* the bold markers. The extraction regex must account for this: `r"^>\s*\*\*(?P<key>[^*:]+):\*\*\s*(?P<value>.+)$"`. This is a stable pattern across all entity types tested.

### 3. Byte-for-byte preservation of unmodified regions

After normalizing the original with mdformat, modifying a field, and re-rendering, the only difference is the intended field change. Unmodified regions are byte-for-byte identical. This is the strongest possible result for C2.

### 4. Approach: normalize-then-modify

The PoC validates the "normalize-then-modify" workflow:
1. First pass: `mdformat.text(source)` normalizes the file
2. Modify the normalized source (string-level field replacement)
3. Second pass: `mdformat.text(modified)` renders the final output
4. The only diff between step 1 and step 3 output is the intended change

This means the write-back approach works by operating on mdformat-normalized text, not on the original source. Files must be normalized before modification.

### 5. Implications for implementation

- The `JerryDocument.parse()` method should normalize on parse (or provide a normalized view)
- The `JerryDocument.render()` method can use `mdformat.text()` directly
- First-time normalization of existing files will produce diffs -- this is a one-time migration cost
- All subsequent modifications will be clean, targeted diffs

---

## Normalization Behavior

mdformat normalization changes observed (non-exhaustive):
- Adds trailing newline if missing
- Normalizes table column alignment padding
- Normalizes list item spacing
- Preserves HTML comments (including `<!-- L2-REINJECT: ... -->`)
- Preserves blockquote frontmatter format
- Preserves code block content verbatim
- Does NOT reflow paragraph text within blockquotes

These are all acceptable normalizations for Jerry's use case.

---

## Decision

**Path: Standard implementation (no fallback needed)**

| Aspect | Decision |
|--------|----------|
| R-01 Verdict | PASS |
| Library Stack | markdown-it-py v4.0.0 + mdformat v1.0.0 (confirmed) |
| Write-back approach | Normalize-then-modify (validated) |
| Fallback needed | No |
| Confidence | ~0.90 (up from 0.75 pre-R-01) |
| Next step | ST-001 (JerryDocument facade) |

---

## Evidence

| Artifact | Location |
|----------|----------|
| PoC script | `EN-001-r01-poc/r01_poc.py` |
| This results document | `EN-001-r01-poc/R01_RESULTS.md` |
| Source: SPIKE-001 recommendation | `orchestration/spike-eval-20260219-001/ps/phase-3-synthesis/ps-synthesizer-001/library-recommendation.md` |
| Source: SPIKE-002 go-nogo | `orchestration/spike-eval-20260219-001/ps/phase-6-decision/ps-synthesizer-002/go-nogo-recommendation.md` |
| Source: R-01 decision tree | Go-nogo recommendation, Section "R-01 Decision Tree" |
| S-010 Self-Refine report | `EN-001-r01-poc/adversary/s010-self-refine-report.md` |
| S-014 Quality Score report | `EN-001-r01-poc/adversary/s014-quality-score-report.md` |

---

## Captured Execution Output

```
======================================================================
TEST: SPIKE-002 entity (Spike)
FILE: projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/SPIKE-002-feasibility/SPIKE-002-feasibility.md
======================================================================

  Token Analysis:
    Total tokens: 390
    Blockquote nodes: 1
    Tree depth: 7
    Frontmatter fields found: 8
      Type: spike
      Status: completed
      Priority: high
      Impact: high
      Created: 2026-02-19
      Parent: FEAT-001
      Owner: --
      Effort: 8

  Step 1: Normalize original with mdformat...
    Original: 8434 chars, Normalized: 8840 chars (growth: +406)

  Step 2: Modify field 'Status': 'completed' -> 'in-progress'...

  Step 3: Render modified source with mdformat...

  CHECK 1: Modified field renders correctly?
    PASS: Field 'Status' renders as 'in-progress' -- correct

  CHECK 2: Unmodified regions preserved?
    PASS: Unmodified regions are byte-for-byte identical

  CHECK 3: mdformat roundtrip idempotent?
    PASS: mdformat roundtrip is idempotent (stable after 2nd pass)

  FILE RESULT: PASS

======================================================================
TEST: EPIC-001 entity (Epic)
FILE: projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/EPIC-001-markdown-ast.md
======================================================================

  Token Analysis:
    Total tokens: 144
    Blockquote nodes: 1
    Tree depth: 6
    Frontmatter fields found: 10
      Type: epic
      Status: in-progress
      Priority: high
      Impact: high
      Created: 2026-02-19
      Due: --
      Completed: --
      Parent: PROJ-005-markdown-ast
      Owner: --
      Target Quarter: FY26-Q1

  Step 1: Normalize original with mdformat...
    Original: 6269 chars, Normalized: 6806 chars (growth: +537)

  Step 2: Modify field 'Status': 'in-progress' -> 'pending'...

  Step 3: Render modified source with mdformat...

  CHECK 1: Modified field renders correctly?
    PASS: Field 'Status' renders as 'pending' -- correct

  CHECK 2: Unmodified regions preserved?
    PASS: Unmodified regions are byte-for-byte identical

  CHECK 3: mdformat roundtrip idempotent?
    PASS: mdformat roundtrip is idempotent (stable after 2nd pass)

  FILE RESULT: PASS

======================================================================
TEST: EN-001 entity (Enabler)
FILE: projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-001-r01-poc/EN-001-r01-poc.md
======================================================================

  Token Analysis:
    Total tokens: 246
    Blockquote nodes: 1
    Tree depth: 6
    Frontmatter fields found: 11
      Type: enabler
      Status: in-progress
      Priority: critical
      Impact: critical
      Enabler Type: exploration
      Created: 2026-02-20
      Due: --
      Completed: --
      Parent: FEAT-001
      Owner: --
      Effort: 3

  Step 1: Normalize original with mdformat...
    Original: 7903 chars, Normalized: 8574 chars (growth: +671)

  Step 2: Modify field 'Status': 'in-progress' -> 'completed'...

  Step 3: Render modified source with mdformat...

  CHECK 1: Modified field renders correctly?
    PASS: Field 'Status' renders as 'completed' -- correct

  CHECK 2: Unmodified regions preserved?
    PASS: Unmodified regions are byte-for-byte identical

  CHECK 3: mdformat roundtrip idempotent?
    PASS: mdformat roundtrip is idempotent (stable after 2nd pass)

  FILE RESULT: PASS

======================================================================
R-01 PROOF-OF-CONCEPT SUMMARY
======================================================================

File                                        C1    C2    C3   Result
---------------------------------------- ----- ----- ----- --------
SPIKE-002 entity (Spike)                  PASS  PASS  PASS     PASS
EPIC-001 entity (Epic)                    PASS  PASS  PASS     PASS
EN-001 entity (Enabler)                   PASS  PASS  PASS     PASS

======================================================================
OVERALL R-01 VERDICT: PASS
  -> Proceed with standard implementation (no fallback needed)
======================================================================
```

---

## Adversarial Review

EN-001 deliverables were reviewed using /adversary skill at C1 criticality.

| Strategy | Agent | Findings | Report |
|----------|-------|----------|--------|
| S-010 Self-Refine | adv-executor | 1 Critical, 3 Major, 3 Minor | `adversary/s010-self-refine-report.md` |
| S-014 LLM-as-Judge | adv-scorer | Composite: 0.83 | `adversary/s014-quality-score-report.md` |

### Findings Addressed

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| SR-001 | Critical | Sign inversion in `norm_diff` | Fixed: renamed to `norm_growth`, reversed subtraction order |
| SR-004 | Major | `parents[6]` undocumented | Added path-level comment documenting each parent index |
| Evidence Quality | -- | No captured execution output | Added full stdout to this document |

### Findings Accepted (Out of Scope for C1 PoC)

| ID | Severity | Finding | Rationale |
|----|----------|---------|-----------|
| SR-002 | Major | Confidence estimate unsubstantiated | Sourced from go-nogo recommendation, not generated by PoC |
| SR-003 | Major | No edge case coverage | Edge cases are scope of subsequent stories (ST-002+) |
| SR-005 | Minor | "Byte-for-byte" vs whitespace | Comparison is post-normalization; claim is accurate |
| SR-006 | Minor | No interface signatures | Interface design is ST-001's scope |
| SR-007 | Minor | Evidence paths unvalidated | Standard repo-relative references |

---

*R-01 Proof-of-Concept. EN-001. FEAT-001. PROJ-005-markdown-ast.*
