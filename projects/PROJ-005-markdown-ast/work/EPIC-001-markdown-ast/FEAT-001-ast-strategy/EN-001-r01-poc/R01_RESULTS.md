# R-01 Proof-of-Concept Results

> **Date:** 2026-02-20
> **Verdict:** PASS -- Proceed with standard implementation
> **Fallback activated:** None
> **Confidence post-R-01:** ~0.90 (up from 0.75; see [Confidence Basis](#confidence-basis))

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Verdict and key findings |
| [Test Matrix](#test-matrix) | Per-file check results |
| [Token Analysis](#token-analysis) | AST parsing diagnostics |
| [Scope and Exclusions](#scope-and-exclusions) | What was and was not tested |
| [Key Observations](#key-observations) | What we learned |
| [Normalization Behavior](#normalization-behavior) | How mdformat changes files |
| [Confidence Basis](#confidence-basis) | Evidence for confidence calibration |
| [Decision](#decision) | Path forward |
| [Evidence](#evidence) | Traceability |
| [Captured Execution Output](#captured-execution-output) | Full PoC stdout |
| [Adversarial Review](#adversarial-review) | Quality gate artifacts |

---

## Summary

The R-01 proof-of-concept validates that markdown-it-py v4.0.0 + mdformat v1.0.0 can successfully:

1. **Parse** real Jerry entity files (Spike, Epic, Enabler) into token streams
2. **Extract** blockquote frontmatter key-value pairs via regex on the `> **Key:** Value` pattern
3. **Modify** frontmatter fields of varying types (status, date, numeric, placeholder) in the normalized source
4. **Render** back with mdformat preserving all unmodified regions (byte-for-byte identical post-normalization)
5. **Verify** mdformat roundtrip idempotency (stable after 2nd pass)

All 3 checks passed across all 6 test cases (3 entity types x Status field + 3 additional field types). No fallback escalation required.

---

## Test Matrix

### Entity Type Tests (Status field)

| File | Type | Fields | C1: Field Correct | C2: Regions Preserved | C3: Idempotent | Result |
|------|------|:------:|:-:|:-:|:-:|:------:|
| SPIKE-002-feasibility.md | Spike | 8 | PASS | PASS | PASS | **PASS** |
| EPIC-001-markdown-ast.md | Epic | 10 | PASS | PASS | PASS | **PASS** |
| EN-001-r01-poc.md | Enabler | 11 | PASS | PASS | PASS | **PASS** |

### Field Type Tests (diverse value types)

| File | Field Modified | Old Value | New Value | C1 | C2 | C3 | Result |
|------|---------------|-----------|-----------|:-:|:-:|:-:|:------:|
| SPIKE-002-feasibility.md | Created (date) | 2026-02-19 | 2026-01-15 | PASS | PASS | PASS | **PASS** |
| EN-001-r01-poc.md | Effort (numeric) | 3 | 5 | PASS | PASS | PASS | **PASS** |
| EN-001-r01-poc.md | Due (placeholder) | -- | 2026-03-15 | PASS | PASS | PASS | **PASS** |

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

## Scope and Exclusions

### What was tested

- 3 entity types: Spike, Epic, Enabler (all worktracker entities with blockquote frontmatter)
- 4 field value types: status (single word), date (ISO-8601), numeric (integer), placeholder (`--`)
- Single-field modification per test case
- Happy path: well-formed files with the target field present and matching the expected value

### What was NOT tested (deferred to ST-002)

- Malformed frontmatter lines (e.g., `> **Key Value` without colon in bold markers)
- Multiple blockquote sections in a single file
- Duplicate field keys within a single blockquote
- Empty files or files with no blockquote frontmatter
- Multi-field modification in a single pass
- Values containing markdown special characters (links, bold, code spans)
- Non-entity files (skill definitions, rule files) -- these use different structural patterns and do not have blockquote frontmatter; the PoC scope is limited to the `> **Key:** Value` pattern used by worktracker entities

These edge cases are explicitly deferred to ST-002 (blockquote frontmatter extension), which will implement production-grade extraction and validation.

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

After normalizing the original with mdformat, modifying a field, and re-rendering, the only difference is the intended field change. Unmodified regions are byte-for-byte identical when compared post-normalization. The PoC's Check 2 implementation also accepts trailing-whitespace-only differences as a PASS (mdformat may normalize trailing newlines), but in all 6 test cases the comparison was exact -- no whitespace-only fallback was needed. This is the strongest possible result for C2.

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

Preliminary interface signatures (refined in ST-001):

```python
class JerryDocument:
    """Facade for AST-based markdown manipulation of Jerry entity files."""

    @classmethod
    def parse(cls, path: Path) -> "JerryDocument":
        """Parse and normalize a Jerry markdown file."""
        ...

    def get_field(self, key: str) -> str | None:
        """Extract a blockquote frontmatter field value."""
        ...

    def set_field(self, key: str, value: str) -> None:
        """Modify a blockquote frontmatter field value."""
        ...

    def render(self) -> str:
        """Render the document to normalized markdown text."""
        ...
```

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

## Confidence Basis

The confidence calibration from 0.75 to ~0.90 is sourced from the go-nogo recommendation (`orchestration/spike-eval-20260219-001/ps/phase-6-decision/ps-synthesizer-002/go-nogo-recommendation.md`, L0 Decision Summary):

> "If R-01 resolves favorably... confidence rises to ~0.90"
> "pre-R-01 confidence: 0.75"

The post-R-01 estimate of ~0.90 (not higher) is grounded in:

| Factor | Contribution | Limitation |
|--------|-------------|------------|
| 6/6 test cases passed all 3 checks | Strong positive signal | Happy-path only (see [Scope and Exclusions](#scope-and-exclusions)) |
| 4 field value types validated | Regex is type-agnostic | No special markdown characters tested |
| Byte-for-byte C2 in all cases | Strongest possible preservation result | Single-field modification only |
| Idempotent C3 in all cases | Roundtrip stability confirmed | No multi-field modification tested |

Confidence is capped below 1.0 due to the scope exclusions documented above. The remaining ~0.10 gap reflects untested edge cases that will be addressed by ST-002 (production extraction) and the expanded test corpus.

---

## Decision

**Path: Standard implementation (no fallback needed)**

| Aspect | Decision |
|--------|----------|
| R-01 Verdict | PASS |
| Library Stack | markdown-it-py v4.0.0 + mdformat v1.0.0 (confirmed) |
| Write-back approach | Normalize-then-modify (validated) |
| Fallback needed | No |
| Confidence | ~0.90 (up from 0.75 pre-R-01; see [Confidence Basis](#confidence-basis)) |
| Next step | ST-001 (JerryDocument facade) |

---

## Evidence

> All paths are relative to `projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/` unless prefixed with `orchestration/` (relative to `projects/PROJ-005-markdown-ast/`). Paths verified at 2026-02-20.

| Artifact | Location |
|----------|----------|
| PoC script | `EN-001-r01-poc/r01_poc.py` |
| This results document | `EN-001-r01-poc/R01_RESULTS.md` |
| Source: SPIKE-001 recommendation | `../../orchestration/spike-eval-20260219-001/ps/phase-3-synthesis/ps-synthesizer-001/library-recommendation.md` |
| Source: SPIKE-002 go-nogo | `../../orchestration/spike-eval-20260219-001/ps/phase-6-decision/ps-synthesizer-002/go-nogo-recommendation.md` |
| Source: R-01 decision tree | Go-nogo recommendation (above), Section "R-01 Decision Tree" |
| S-010 Self-Refine report | `EN-001-r01-poc/adversary/s010-self-refine-report.md` |
| S-014 Quality Score report | `EN-001-r01-poc/adversary/s014-quality-score-report.md` |

---

## Captured Execution Output

Output from `uv run python r01_poc.py` (2026-02-20, post-revision run with 6 test cases):

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

  Step 1: Normalize original with mdformat...
    Original: 8434 chars, Normalized: 8840 chars (growth: +406)
  Step 2: Modify field 'Status': 'completed' -> 'in-progress'...
  Step 3: Render modified source with mdformat...

  CHECK 1: PASS: Field 'Status' renders as 'in-progress' -- correct
  CHECK 2: PASS: Unmodified regions are byte-for-byte identical
  CHECK 3: PASS: mdformat roundtrip is idempotent (stable after 2nd pass)
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

  Step 1: Normalize original with mdformat...
    Original: 6269 chars, Normalized: 6806 chars (growth: +537)
  Step 2: Modify field 'Status': 'in-progress' -> 'pending'...
  Step 3: Render modified source with mdformat...

  CHECK 1: PASS: Field 'Status' renders as 'pending' -- correct
  CHECK 2: PASS: Unmodified regions are byte-for-byte identical
  CHECK 3: PASS: mdformat roundtrip is idempotent (stable after 2nd pass)
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

  Step 1: Normalize original with mdformat...
    Original: 8270 chars, Normalized: 8941 chars (growth: +671)
  Step 2: Modify field 'Status': 'completed' -> 'in-progress'...
  Step 3: Render modified source with mdformat...

  CHECK 1: PASS: Field 'Status' renders as 'in-progress' -- correct
  CHECK 2: PASS: Unmodified regions are byte-for-byte identical
  CHECK 3: PASS: mdformat roundtrip is idempotent (stable after 2nd pass)
  FILE RESULT: PASS

======================================================================
TEST: SPIKE-002 date field (Created)
FILE: projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/SPIKE-002-feasibility/SPIKE-002-feasibility.md
======================================================================

  Step 2: Modify field 'Created': '2026-02-19' -> '2026-01-15'...

  CHECK 1: PASS: Field 'Created' renders as '2026-01-15' -- correct
  CHECK 2: PASS: Unmodified regions are byte-for-byte identical
  CHECK 3: PASS: mdformat roundtrip is idempotent (stable after 2nd pass)
  FILE RESULT: PASS

======================================================================
TEST: EN-001 numeric field (Effort)
FILE: projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-001-r01-poc/EN-001-r01-poc.md
======================================================================

  Step 2: Modify field 'Effort': '3' -> '5'...

  CHECK 1: PASS: Field 'Effort' renders as '5' -- correct
  CHECK 2: PASS: Unmodified regions are byte-for-byte identical
  CHECK 3: PASS: mdformat roundtrip is idempotent (stable after 2nd pass)
  FILE RESULT: PASS

======================================================================
TEST: EN-001 placeholder field (Due)
FILE: projects/PROJ-005-markdown-ast/work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/EN-001-r01-poc/EN-001-r01-poc.md
======================================================================

  Step 2: Modify field 'Due': '--' -> '2026-03-15'...

  CHECK 1: PASS: Field 'Due' renders as '2026-03-15' -- correct
  CHECK 2: PASS: Unmodified regions are byte-for-byte identical
  CHECK 3: PASS: mdformat roundtrip is idempotent (stable after 2nd pass)
  FILE RESULT: PASS

======================================================================
R-01 PROOF-OF-CONCEPT SUMMARY
======================================================================

File                                        C1    C2    C3   Result
---------------------------------------- ----- ----- ----- --------
SPIKE-002 entity (Spike)                  PASS  PASS  PASS     PASS
EPIC-001 entity (Epic)                    PASS  PASS  PASS     PASS
EN-001 entity (Enabler)                   PASS  PASS  PASS     PASS
SPIKE-002 date field (Created)            PASS  PASS  PASS     PASS
EN-001 numeric field (Effort)             PASS  PASS  PASS     PASS
EN-001 placeholder field (Due)            PASS  PASS  PASS     PASS

======================================================================
OVERALL R-01 VERDICT: PASS
  -> Proceed with standard implementation (no fallback needed)
======================================================================
```

---

## Adversarial Review

EN-001 deliverables were reviewed using /adversary skill at C1 criticality. Initial score: 0.83. All 7 findings addressed in revision.

| Strategy | Agent | Findings | Report |
|----------|-------|----------|--------|
| S-010 Self-Refine | adv-executor | 1 Critical, 3 Major, 3 Minor | `adversary/s010-self-refine-report.md` |
| S-014 LLM-as-Judge | adv-scorer | Initial composite: 0.83 | `adversary/s014-quality-score-report.md` |

### All Findings Addressed

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| SR-001 | Critical | Sign inversion in `norm_diff` | Fixed: renamed to `norm_growth`, reversed subtraction order in r01_poc.py |
| SR-002 | Major | Confidence estimate unsubstantiated | Added [Confidence Basis](#confidence-basis) section with observable outcome derivation |
| SR-003 | Major | No edge case coverage documented | Added [Scope and Exclusions](#scope-and-exclusions) section; added 3 field-type tests (date, numeric, placeholder) |
| SR-004 | Major | `parents[6]` undocumented | Added path-level comment documenting each parent index in r01_poc.py |
| SR-005 | Minor | "Byte-for-byte" vs whitespace ambiguity | Qualified claim in Key Observation #3: "byte-for-byte identical when compared post-normalization" with whitespace fallback documented |
| SR-006 | Minor | No interface signatures | Added preliminary `JerryDocument` interface signatures in Key Observation #5 |
| SR-007 | Minor | Evidence paths unvalidated | Added path anchoring note and verification date to Evidence section; paths verified to exist |

### S-014 Dimension Improvements (Revision Actions)

| Dimension | Initial Score | Revision Action |
|-----------|:------------:|-----------------|
| Completeness | 0.82 | Added 3 field-type tests; added Scope and Exclusions section |
| Internal Consistency | 0.92 | Fixed SR-001 sign inversion; qualified byte-for-byte claim |
| Methodological Rigor | 0.80 | Added diverse field types (date, numeric, placeholder); documented scope exclusions |
| Evidence Quality | 0.74 | Added captured execution output; grounded confidence estimate |
| Actionability | 0.87 | Added preliminary interface signatures |
| Traceability | 0.80 | Anchored evidence paths; verified all references |

---

*R-01 Proof-of-Concept. EN-001. FEAT-001. PROJ-005-markdown-ast.*
