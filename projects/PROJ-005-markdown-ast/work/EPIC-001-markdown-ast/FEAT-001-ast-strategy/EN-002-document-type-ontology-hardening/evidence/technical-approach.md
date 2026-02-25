# EN-002: Technical Approach — Document Type Ontology Hardening

<!--
SOURCE: Extracted from EN-002-document-type-ontology-hardening.md
PURPOSE: Design document for implementation details (NOT a worktracker entity)
DATE: 2026-02-24
PARENT: EN-002
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [File Taxonomy](#file-taxonomy) | Complete inventory of 2,774 markdown files across 20+ categories |
| [Path Pattern Design](#path-pattern-design) | Tiered path pattern registry (65 patterns) |
| [Structural Cue Design](#structural-cue-design) | Precise structural fingerprints replacing buggy `"---"` cue |
| [UNKNOWN Fallback Design](#unknown-fallback-design) | Explicit fallback with structured diagnostics |
| [Regression Test Design](#regression-test-design) | Full-repo parametrized test suite (~5,500 files) |
| [Nav Table Analysis](#nav-table-analysis) | Nav table validation refinement disposition |

---

## File Taxonomy

Complete inventory of markdown file categories discovered in the repository (2,774 total files):

### Existing `DocumentType` Coverage

| DocumentType Enum Value | Path Patterns (Current) | File Count | Status |
|---|---|---|---|
| `AGENT_DEFINITION` | `skills/*/agents/*.md` | 58 | OK |
| `SKILL_DEFINITION` | `skills/*/SKILL.md` | 15 | OK |
| `RULE_FILE` | `.context/rules/*.md`, `.claude/rules/*.md` | 15 | OK but needs expansion |
| `ADR` | `docs/design/*.md` | 4 | OK but `docs/adrs/*.md` missing |
| `STRATEGY_TEMPLATE` | `.context/templates/adversarial/*.md` | 11 | OK |
| `WORKTRACKER_ENTITY` | `projects/*/WORKTRACKER.md`, `projects/*/work/**/*.md` | 811 | OK |
| `FRAMEWORK_CONFIG` | `CLAUDE.md`, `AGENTS.md` | 2 | OK |
| `ORCHESTRATION_ARTIFACT` | `projects/*/orchestration/**/*.md` | 198 | OK |
| `KNOWLEDGE_DOCUMENT` | `docs/knowledge/**/*.md` | 26 | OK but needs expansion |
| `PATTERN_DOCUMENT` | -- | 0 | No path patterns at all |
| `UNKNOWN` | -- | ~1,634 | Everything else falls here |

### Proposed New `DocumentType` Values

| New Enum Value | Covers | File Count | Rationale |
|---|---|---|---|
| `SKILL_RESOURCE` | Playbooks, skill rules, skill tests, skill docs, skill references, composition prompts | ~109 | Skill-scoped files that are NOT agent definitions and NOT the SKILL.md itself |
| `TEMPLATE` | `.context/templates/worktracker/*.md`, `.context/templates/design/*.md` | ~18 | Template files distinct from strategy templates |
| `PATTERN_DOCUMENT` (existing, unused) | `.context/patterns/**/*.md`, `.context/guides/*.md` | ~36 | Already in enum, just needs path patterns |

### Proposed Fallback: `UNKNOWN` with structured signal

Files that match no path pattern AND no structural cue should return `UNKNOWN` with a structured `unmatched_path` field so that:
1. The regression test can assert which files are intentionally `UNKNOWN` vs. accidentally uncovered
2. New file categories added to the repo get flagged in CI when they aren't classified
3. No file is ever *silently* misclassified -- every file either matches precisely or is explicitly `UNKNOWN`

---

## Path Pattern Design

### Phase 1: Expand ontology enum and path patterns (TASK-003, TASK-004)

**Enum additions:**
```python
class DocumentType(Enum):
    # Existing values unchanged...
    SKILL_RESOURCE = "skill_resource"      # NEW: playbooks, skill rules, tests, docs, refs, composition prompts
    TEMPLATE = "template"                  # NEW: non-adversarial templates
    # PATTERN_DOCUMENT already exists, just needs path patterns
```

**Path pattern expansion (ordered, first-match-wins):**
```python
PATH_PATTERNS: list[tuple[str, DocumentType]] = [
    # --- Tier 1: Most specific patterns ---
    ("skills/*/agents/*.md", DocumentType.AGENT_DEFINITION),
    ("skills/*/SKILL.md", DocumentType.SKILL_DEFINITION),
    (".context/rules/*.md", DocumentType.RULE_FILE),
    (".claude/rules/*.md", DocumentType.RULE_FILE),
    ("docs/design/*.md", DocumentType.ADR),
    ("docs/adrs/*.md", DocumentType.ADR),                            # NEW
    (".context/templates/adversarial/*.md", DocumentType.STRATEGY_TEMPLATE),

    # --- Tier 2: Skill resources (before broad skill/*) ---
    ("skills/*/PLAYBOOK.md", DocumentType.SKILL_RESOURCE),           # NEW
    ("skills/*/rules/*.md", DocumentType.RULE_FILE),                 # NEW (reuse RULE_FILE)
    ("skills/*/tests/*.md", DocumentType.SKILL_RESOURCE),            # NEW
    ("skills/*/composition/*.md", DocumentType.SKILL_RESOURCE),      # NEW
    ("skills/*/reference/*.md", DocumentType.SKILL_RESOURCE),        # NEW
    ("skills/*/references/*.md", DocumentType.SKILL_RESOURCE),       # NEW
    ("skills/*/templates/*.md", DocumentType.TEMPLATE),              # NEW
    ("skills/*/docs/*.md", DocumentType.SKILL_RESOURCE),             # NEW
    ("skills/*/validation/*.md", DocumentType.SKILL_RESOURCE),       # NEW
    ("skills/*/knowledge/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT), # NEW
    ("skills/shared/*.md", DocumentType.SKILL_RESOURCE),             # NEW

    # --- Tier 3: Worktracker entities ---
    ("projects/*/WORKTRACKER.md", DocumentType.WORKTRACKER_ENTITY),
    ("projects/*/work/**/*.md", DocumentType.WORKTRACKER_ENTITY),
    ("projects/*/PLAN.md", DocumentType.FRAMEWORK_CONFIG),           # NEW
    ("projects/*/decisions/*.md", DocumentType.ADR),                  # NEW
    ("projects/*/analysis/*.md", DocumentType.KNOWLEDGE_DOCUMENT),   # NEW
    ("projects/*/research/*.md", DocumentType.KNOWLEDGE_DOCUMENT),   # NEW
    ("projects/*/synthesis/*.md", DocumentType.KNOWLEDGE_DOCUMENT),  # NEW
    ("projects/*/critiques/*.md", DocumentType.KNOWLEDGE_DOCUMENT),  # NEW

    # --- Tier 4: Framework config ---
    ("CLAUDE.md", DocumentType.FRAMEWORK_CONFIG),
    ("AGENTS.md", DocumentType.FRAMEWORK_CONFIG),
    ("README.md", DocumentType.FRAMEWORK_CONFIG),                    # NEW
    ("CODE_OF_CONDUCT.md", DocumentType.FRAMEWORK_CONFIG),           # NEW
    ("projects/*/ORCHESTRATION_PLAN.md", DocumentType.FRAMEWORK_CONFIG), # NEW

    # --- Tier 5: Broader patterns ---
    ("projects/*/orchestration/**/*.md", DocumentType.ORCHESTRATION_ARTIFACT),
    (".context/templates/worktracker/*.md", DocumentType.TEMPLATE),   # NEW
    (".context/templates/design/*.md", DocumentType.TEMPLATE),        # NEW
    (".context/templates/**/*.md", DocumentType.TEMPLATE),            # NEW (catch-all for templates)
    (".context/patterns/**/*.md", DocumentType.PATTERN_DOCUMENT),     # NEW
    (".context/guides/*.md", DocumentType.PATTERN_DOCUMENT),          # NEW
    ("docs/knowledge/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
    ("docs/synthesis/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),     # NEW
    ("docs/governance/*.md", DocumentType.KNOWLEDGE_DOCUMENT),       # NEW
    ("docs/research/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),      # NEW
    ("docs/playbooks/*.md", DocumentType.KNOWLEDGE_DOCUMENT),        # NEW
    ("docs/reviews/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),       # NEW
    ("docs/scores/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),        # NEW
    ("docs/runbooks/*.md", DocumentType.KNOWLEDGE_DOCUMENT),         # NEW
    ("docs/blog/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),          # NEW
    ("docs/analysis/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),      # NEW
    ("docs/specifications/*.md", DocumentType.KNOWLEDGE_DOCUMENT),   # NEW
    ("docs/security/*.md", DocumentType.KNOWLEDGE_DOCUMENT),         # NEW
    ("docs/schemas/*.md", DocumentType.KNOWLEDGE_DOCUMENT),          # NEW
    ("docs/templates/*.md", DocumentType.TEMPLATE),                  # NEW
    ("docs/*.md", DocumentType.KNOWLEDGE_DOCUMENT),                  # NEW (catch-all for docs/)
]
```

---

## Structural Cue Design

### Phase 2: Fix structural cues (TASK-005)

Replace the buggy `"---"` cue with precise structural fingerprints:

```python
STRUCTURAL_CUE_PRIORITY: list[tuple[str, DocumentType]] = [
    # Agent definitions use XML-tagged sections (agent-development-standards.md)
    ("<identity>", DocumentType.AGENT_DEFINITION),
    ("<methodology>", DocumentType.AGENT_DEFINITION),
    ("<purpose>", DocumentType.AGENT_DEFINITION),
    # Worktracker entities use blockquote frontmatter
    ("> **Type:**", DocumentType.WORKTRACKER_ENTITY),
    # Rule files use L2-REINJECT markers
    ("<!-- L2-REINJECT", DocumentType.RULE_FILE),
    # Strategy templates use specific frontmatter
    ("> **Strategy:**", DocumentType.STRATEGY_TEMPLATE),
    # ADRs use Status/Context/Decision structure
    ("## Status", DocumentType.ADR),
    # Skill definitions have specific frontmatter
    ("> **Version:**", DocumentType.SKILL_DEFINITION),
]
```

Key design decisions:
- **No `"---"` cue.** Horizontal rules are ubiquitous and carry no type signal.
- **No `"<!--"` cue.** HTML comments are common in many file types. Only `<!-- L2-REINJECT` is distinctive enough.
- **`> **Type:**` instead of `> **`.** More specific blockquote matching prevents false positives from non-frontmatter blockquotes.
- **Structural cues are fallback only.** With comprehensive path patterns, structural cues should rarely activate.

---

## UNKNOWN Fallback Design

### Phase 3: UNKNOWN fallback with structured logging (TASK-005)

When both path and structure return `None`, the detector returns `UNKNOWN` with diagnostic data:

```python
# In detect() return path:
return (DocumentType.UNKNOWN, None, {"unmatched_path": normalized_path})
```

This enables the regression test to distinguish between:
- **Expected UNKNOWN:** Files intentionally outside the ontology (e.g., `SOUNDTRACK.md`)
- **Gap UNKNOWN:** Files that should have a pattern but don't -- flagged as test failure

---

## Regression Test Design

### Phase 4: Full-repo regression test (TASK-006)

A parametrized pytest suite that:

1. **Discovers all `.md` files** in the repo (excluding `.git/`, `.claude/worktrees/`)
2. **Runs `DocumentTypeDetector.detect()`** on each file
3. **Asserts no file returns `agent_definition` via structural cue** (the specific bug from BUG-004)
4. **Asserts no warnings** on path-matched files (structural mismatch warnings = 0)
5. **Maintains an allowlist** of expected `UNKNOWN` files (files intentionally outside ontology)
6. **Fails on any new `UNKNOWN`** file not in the allowlist -- forces explicit classification when new file categories are added

```python
# Sketch of the regression test
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ALL_MD_FILES = sorted(
    str(p.relative_to(REPO_ROOT))
    for p in REPO_ROOT.rglob("*.md")
    if ".git" not in p.parts and ".claude/worktrees" not in str(p)
)

# Files intentionally classified as UNKNOWN
EXPECTED_UNKNOWN = frozenset({
    "SOUNDTRACK.md",
    # ... other intentionally unclassified files
})

@pytest.mark.parametrize("file_path", ALL_MD_FILES)
def test_document_type_detection(file_path: str) -> None:
    """Every .md file in the repo must classify correctly or be in EXPECTED_UNKNOWN."""
    full_path = REPO_ROOT / file_path
    content = full_path.read_text(encoding="utf-8")
    doc_type, warning = DocumentTypeDetector.detect(file_path, content)

    # BUG-004 regression: no file should match agent_definition via structure
    if doc_type == DocumentType.AGENT_DEFINITION:
        path_type = DocumentTypeDetector._detect_from_path(
            _normalize_path(file_path)
        )
        assert path_type is not None, (
            f"{file_path} classified as agent_definition via STRUCTURE, not path. "
            "This is the BUG-004 regression."
        )

    # No warnings on path-matched files
    if warning and "structure suggests" in warning:
        pytest.fail(f"{file_path} has structural mismatch warning: {warning}")

    # UNKNOWN files must be in the allowlist
    if doc_type == DocumentType.UNKNOWN:
        assert file_path in EXPECTED_UNKNOWN, (
            f"{file_path} classified as UNKNOWN but not in allowlist. "
            "Add a PATH_PATTERN or add to EXPECTED_UNKNOWN."
        )
```

**Expected test count:** ~5,500 parametrized test cases, one per `.md` file.

---

## Nav Table Analysis

### Phase 5: Nav table validation refinement (TASK-007)

Separate concern from the type detector. The nav table validator reports `is_valid: false` when `##` headings exist without nav table entries, but many files intentionally use partial nav tables. Options:
- (a) Only flag missing entries as a warning, not a validity failure
- (b) Add a `<!-- NAV: partial -->` comment to declare partial coverage intent
- (c) Accept current behavior but document it clearly

**TASK-007 Disposition (closed):** Audited during implementation. Findings:
- Only `ADR_SCHEMA` among EN-002's new schemas has `require_nav_table=True` (correct).
- All other new schemas (`SKILL_RESOURCE_SCHEMA`, `TEMPLATE_SCHEMA`, etc.) have `require_nav_table=False`.
- Current nav table validation behavior is consistent with the schema design: files in categories that don't require nav tables are not penalized for missing them.
- Option (c) selected: current behavior is correct and documented. No code change needed. Nav table validation refinement for partial coverage (options a/b) is a separate concern outside EN-002 scope and would apply to the existing nav table validator, not the document type detector.

---

*Extracted from EN-002-document-type-ontology-hardening.md on 2026-02-24*
*Purpose: Separate implementation details from worktracker entity per content standards*
