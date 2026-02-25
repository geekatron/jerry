# EN-002 Security QA Test Strategy: Document Type Ontology Hardening

<!-- AGENT: eng-qa | VERSION: 1.0.0 | DATE: 2026-02-24 | TASK: TASK-006 -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Coverage summary and security test assessment |
| [L1 Technical Detail](#l1-technical-detail) | Test case specifications and fuzzing design |
| [L2 Strategic Implications](#l2-strategic-implications) | Strategy effectiveness and risk analysis |
| [Test Environment](#test-environment) | Execution prerequisites and constraints |
| [OWASP Mapping](#owasp-mapping) | Category-to-test mapping |

---

## L0 Executive Summary

### Scope

This strategy covers TASK-006 (full-repo regression test) from EN-002, plus the unit-level coverage required for the expanded `DocumentTypeDetector`. The test work spans two files:

| File | Purpose | Test Count Estimate |
|------|---------|---------------------|
| `tests/integration/test_document_type_regression.py` | Parametrized full-repo regression, BUG-004 gate | ~2,774 parametrized cases + 5 assertion groups |
| `tests/unit/domain/markdown_ast/test_document_type.py` | Unit tests for expanded enum, new patterns, new cues | 26 existing + ~70 new = ~96 total |

### Security Threat Coverage

The `DocumentTypeDetector` is a security-critical component (threat model T-DT-01 through T-DT-05). The primary threat is **type confusion (CWE-843)**: a file that convinces the detector it belongs to a more-trusted type gains unwarranted schema selection, validation bypass, or automation routing. Three attack surfaces are tested:

| Threat | Test Surface | Assertion Type |
|--------|-------------|----------------|
| T-DT-01: Content spoofing structural cue | Structural cue precision tests | No path-miss file should gain agent_definition via "---" |
| T-DT-02: Path prefix confusion | Boundary pattern ordering tests | More-specific prefix wins over broader sibling |
| T-DT-03: Glob ambiguity injection | Pattern overlap zone tests | First-match-wins is deterministic at each overlap |
| T-DT-04: UNKNOWN escalation | Allowlist gate | No unclassified file is silently accepted |
| T-DT-05: Mismatch warning suppression | Dual-signal tests | Mismatch always produces warning when signals disagree |

### Overall Assessment (Confidence: HIGH)

The strategy is executable against the post-EN-002 implementation. All assertions are deterministic. The regression suite doubles as the CI gate for ongoing ontology integrity. Coverage target of >= 90% line coverage on `document_type.py` is achievable given the parametrized nature of the regression test.

---

## L1 Technical Detail

### Test Environment

| Requirement | Value |
|-------------|-------|
| Python execution | `uv run pytest` (H-05) |
| Test runner | pytest >= 8.0.0 |
| Coverage tool | pytest-cov (coverage.py backend) |
| Coverage target | >= 90% line coverage on `src/domain/markdown_ast/document_type.py` |
| Performance target | < 30 seconds for full 2,774-file parametrized suite (TC-4) |
| Test markers to use | `regression`, `integration`, `security`, `edge-case`, `boundary`, `happy-path` |
| Exclusion paths | `.git/`, `.claude/worktrees/`, `.venv/`, `node_modules/` |

---

### Part 1: Regression Test Structure

**File:** `tests/integration/test_document_type_regression.py`

#### 1.1 File Discovery Strategy

The test module discovers all `.md` files at import time using `pathlib.Path.rglob`. The collected list is stored as a module-level constant so parametrize can reference it.

**Discovery algorithm:**

```
REPO_ROOT = Path(__file__).resolve().parents[3]
# parents[3] navigates: test file -> integration/ -> tests/ -> repo root

EXCLUSION_PARTS = frozenset({
    ".git",
    "worktrees",    # catches .claude/worktrees/ at any depth
    "node_modules",
})

EXCLUSION_PATH_PREFIXES = frozenset({
    ".venv",        # virtual environment at repo root
})

def _should_exclude(path: Path) -> bool:
    # Check any component matches exclusion parts
    if any(part in EXCLUSION_PARTS for part in path.parts):
        return True
    # Check repo-relative prefix
    relative = path.relative_to(REPO_ROOT)
    first_component = relative.parts[0] if relative.parts else ""
    return first_component in EXCLUSION_PATH_PREFIXES
```

**Rationale for each exclusion:**

| Exclusion | Reason | Risk if omitted |
|-----------|--------|-----------------|
| `.git/` | Git object files, not project markdown | Millions of non-relevant paths; false UNKNOWN volume |
| `.claude/worktrees/` | Other feature branches; separate work trees with their own `.venv/` containing third-party `.md` files like `cyclonedx/contrib/README.md` | Cross-branch contamination; `.venv` inside worktrees contains pip/pyright/etc README.md files from packages |
| `.venv/` at repo root | Same issue -- third-party package README.md files (cycone-dx, pyright, markdown, etc) | ~20+ package README files all classify as UNKNOWN; allowlist bloat |
| `node_modules/` | Not present currently but standard guard | Future-proofing |

**Note on `skills/transcript/test_data/`:** These markdown files (transcript output packets like `00-index.md`, `01-summary.md`, etc.) are _intentional_ test fixtures that will not match any path pattern. They must be handled via the EXPECTED_UNKNOWN allowlist, NOT via exclusion. Excluding them would hide a real coverage gap. The allowlist entry provides documentation that they are intentionally unclassified.

**Note on `skills/.graveyard/`:** Two archived `SKILL.md` files live here. They will match the `skills/*/SKILL.md` pattern and classify as `SKILL_DEFINITION`. This is acceptable -- no exclusion needed.

#### 1.2 EXPECTED_UNKNOWN Allowlist Design

The allowlist is a `frozenset[str]` of repo-relative POSIX paths. Each entry MUST have an inline comment explaining why it is intentionally UNKNOWN.

**Population approach:** After implementing path patterns in TASK-004, run the regression test in a non-failing mode (using `pytest --collect-only` or a discovery script) to enumerate all files that still return `UNKNOWN`. Review each one:

- If a pattern should cover it: add the pattern to `PATH_PATTERNS` (not the allowlist).
- If it is genuinely outside the ontology (test fixture, transient, external): add to `EXPECTED_UNKNOWN` with justification comment.

**Target allowlist size:** EN-002 acceptance criteria states < 20 entries. Each entry requires a justification comment (per EN-002 risk table). Entries without justification comments fail code review.

**Allowlist governance rule:** The allowlist is append-only with prejudice. Removing an entry from the allowlist without a corresponding path pattern addition is a test integrity failure.

**Anticipated allowlist members based on current repo scan:**

| File Category | Representative Path | Justification |
|--------------|--------------------|-|
| Transcript packet outputs | `skills/transcript/test_data/expected_output/transcript-meeting-001/00-index.md` | Test fixture; classified by content domain not file type ontology |
| Transcript validation outputs | `skills/transcript/test_data/validation/live-output-meeting-006/packet/00-index.md` | Same as above |
| Root README | `README.md` | Repository root readme; if not covered by FRAMEWORK_CONFIG pattern |
| Graveyard READMEs | `skills/.graveyard/worktracker/README.md` | Archived skill reference; intentionally outside active ontology |

**Important:** The final allowlist is established by running the implementation, not by pre-specifying it. The above list is the design-time estimate; the implementation will produce the authoritative allowlist.

#### 1.3 Parametrized Test: Core Regression Cases

Each parametrized case receives one `file_path: str` (repo-relative POSIX path). The test body performs these assertions in order:

**Assertion Group A: No structural misclassification (BUG-004 regression gate)**

```
Purpose: Assert that no file gains AGENT_DEFINITION via the structural cue path.
         After EN-002, the "---" cue is removed. Any file classified as
         AGENT_DEFINITION must have matched a PATH_PATTERN.

Assertion logic:
    detected_type, warning = DocumentTypeDetector.detect(file_path, content)
    if detected_type == DocumentType.AGENT_DEFINITION:
        path_type = DocumentTypeDetector._detect_from_path(_normalize_path(file_path))
        ASSERT path_type is not None, with message:
            "{file_path} returned AGENT_DEFINITION but _detect_from_path returned None.
             This is the BUG-004 regression: structural cue is causing misclassification.
             Remove or tighten the structural cue that triggers agent_definition."

Security relevance: T-DT-01 (content spoofing). A file that lacks a skills/*/agents/*.md
path match should never gain agent_definition type -- doing so could grant unwarranted
schema selection to arbitrary files with section separators.
```

**Assertion Group B: No structural mismatch warnings on path-matched files**

```
Purpose: Path-matched files must not produce structural mismatch warnings.
         Warnings indicate the structural cue is firing on path-classified files,
         which means the structural cues are still too broad (BUG-004 partial fix).

Assertion logic:
    if path_type is not None and warning is not None:
        FAIL with message:
            "{file_path} is path-classified as {path_type.value} but produces
             structural warning: '{warning}'.
             This means a structural cue is firing on a file that is already
             path-classified. Tighten the structural cue or verify path ordering."

Security relevance: T-DT-05 (mismatch warning suppression). Spurious warnings
create noise that obscures genuine mismatch signals for actual type confusion.
```

**Assertion Group C: UNKNOWN files must be in allowlist**

```
Purpose: No file should silently fall through to UNKNOWN without deliberate classification
         or explicit allowlist justification.

Assertion logic:
    if detected_type == DocumentType.UNKNOWN:
        ASSERT file_path in EXPECTED_UNKNOWN, with message:
            "{file_path} classified as UNKNOWN but not in EXPECTED_UNKNOWN allowlist.
             Either add a PATH_PATTERN to classify this file type, or add to
             EXPECTED_UNKNOWN with a justification comment explaining why UNKNOWN is
             intentional. Target allowlist size: < 20 entries."

Security relevance: T-DT-04 (UNKNOWN escalation). An unchecked UNKNOWN file category
means a new file type was added to the repo without conscious classification. This is
an ontology gap that could be exploited if automation depends on classification.
```

**Assertion Group D: Enum completeness gate**

```
Purpose: Verify that the DocumentType enum covers the set expected post-EN-002.
         This is a module-level assertion, not per-file.

Assertion logic (module-level, not parametrized):
    ASSERT len(DocumentType) == 13  # 11 existing + SKILL_RESOURCE + TEMPLATE
    ASSERT DocumentType.SKILL_RESOURCE.value == "skill_resource"
    ASSERT DocumentType.TEMPLATE.value == "template"

Run once at module load to catch enum regression before parametrized tests run.
```

**Assertion Group E: Performance gate**

```
Purpose: Full suite must complete within 30 seconds (TC-4 from EN-002).

Implementation: pytest-benchmark or a wall-clock assertion in a separate non-parametrized
test that runs a sample of 100 randomly selected files and extrapolates.

Alternative: Use pytest --timeout marker. If the full parametrized suite exceeds
30 seconds, it signals that detect() has introduced expensive I/O or regex.

Acceptance threshold: detect() for one file < 10ms (pure string operations; no I/O
inside detect() itself; I/O happens in the test harness via read_text()).
```

---

### Part 2: Boundary Tests for First-Match-Wins Ordering

**File:** `tests/unit/domain/markdown_ast/test_document_type.py` (extend existing class or add new class `TestPatternOrdering`)

The first-match-wins semantics create security-relevant ordering boundaries. If a broader pattern precedes a more-specific one, the more-specific type is never reachable. These tests verify that the ordering in `PATH_PATTERNS` is correct.

#### 2.1 Overlap Zone Catalog

Based on the EN-002 proposed pattern list, these are the high-risk overlap zones:

| Zone | Competing Patterns | Correct Winner | Risk if Wrong |
|------|--------------------|----------------|---------------|
| OZ-01 | `skills/*/agents/*.md` vs `skills/*/SKILL.md` | Both exact: no overlap | Low |
| OZ-02 | `skills/*/rules/*.md` vs `.context/rules/*.md` | Separate prefixes: no overlap | Low |
| OZ-03 | `skills/*/composition/*.md` vs `skills/*/agents/*.md` | Must test `skills/X/composition/` does NOT match `skills/X/agents/` | Medium |
| OZ-04 | `skills/*/templates/*.md` vs `.context/templates/adversarial/*.md` | Separate prefixes: no overlap | Low |
| OZ-05 | `projects/*/work/**/*.md` vs `projects/*/orchestration/**/*.md` | `work/` before `orchestration/` in list; same `projects/*/` prefix | HIGH: a file at `projects/X/work/orchestration/foo.md` would match `work/**` first |
| OZ-06 | `projects/*/decisions/*.md` vs `projects/*/work/**/*.md` | `decisions/` is NOT under `work/`; no overlap | Low (verify anyway) |
| OZ-07 | `.context/templates/adversarial/*.md` vs `.context/templates/**/*.md` (catch-all) | `adversarial/` must come before the catch-all | HIGH |
| OZ-08 | `docs/design/*.md` vs `docs/*.md` (catch-all) | `docs/design/` must come before `docs/` | HIGH |
| OZ-09 | `skills/*/knowledge/**/*.md` vs `docs/knowledge/**/*.md` | Different prefixes: no overlap | Low |
| OZ-10 | `skills/*/PLAYBOOK.md` vs the `.md`-inclusive patterns in skills | Exact basename; no wildcard conflict | Medium |

#### 2.2 Boundary Test Cases for Each High-Risk Overlap

**OZ-05: work/ vs orchestration/ under projects/**

```
Test: Path in projects/*/work/**/ does NOT match orchestration pattern
Input: "projects/PROJ-XXX/work/orchestration-notes/plan.md"
Expected: WORKTRACKER_ENTITY  (matched by work/**/*.md)
NOT:       ORCHESTRATION_ARTIFACT
Rationale: A file under work/ is always a worktracker entity regardless of its
           folder name containing "orchestration". Confirms work/ comes before
           orchestration/ in the pattern list.

Test: Path in projects/*/orchestration/**/ does match orchestration pattern
Input: "projects/PROJ-XXX/orchestration/phase-1/output.md"
Expected: ORCHESTRATION_ARTIFACT
Test: projects/*/orchestration/WORKTRACKER.md edge case
Input: "projects/PROJ-XXX/orchestration/WORKTRACKER.md"
Expected: ORCHESTRATION_ARTIFACT (NOT WORKTRACKER_ENTITY -- no match for */WORKTRACKER.md here)
```

**OZ-07: adversarial/ vs .context/templates catch-all**

```
Test: Adversarial template is correctly classified before catch-all fires
Input: ".context/templates/adversarial/s-001-red-team.md"
Expected: STRATEGY_TEMPLATE

Test: Non-adversarial template matches TEMPLATE (via worktracker/ subdir)
Input: ".context/templates/worktracker/BUG.md"
Expected: TEMPLATE

Test: Catch-all fires for unknown template subdir
Input: ".context/templates/future-category/new-template.md"
Expected: TEMPLATE (catch-all .context/templates/**/*.md)
NOT: STRATEGY_TEMPLATE

Rationale: Verifies that the more-specific adversarial/ pattern precedes the
           catch-all, and that the catch-all correctly handles new subdirs.
```

**OZ-08: docs/design/ vs docs/ catch-all**

```
Test: ADR in docs/design/ classified as ADR, not KNOWLEDGE_DOCUMENT
Input: "docs/design/adr-epic002-001.md"
Expected: ADR

Test: Generic docs file falls to KNOWLEDGE_DOCUMENT
Input: "docs/BOOTSTRAP.md"
Expected: KNOWLEDGE_DOCUMENT  (docs/*.md catch-all)

Test: docs/adrs/ classified as ADR (new pattern)
Input: "docs/adrs/ADR-001-agent-architecture.md"
Expected: ADR

Test: docs/knowledge/ classified as KNOWLEDGE_DOCUMENT
Input: "docs/knowledge/patterns.md"
Expected: KNOWLEDGE_DOCUMENT

Security note: If docs/ catch-all fired before docs/design/, ADRs would be
classified as KNOWLEDGE_DOCUMENT, stripping them of the stricter ADR schema
validation and creating a type confusion opportunity (T-DT-02).
```

#### 2.3 Parametrized First-Match-Wins Tests

To test ordering systematically, use a parametrized class with each overlap zone as a test case:

```
@pytest.mark.parametrize("path, expected_type, description", [
    # OZ-01: agents vs skill.md (no actual overlap, confirm both work)
    ("skills/ast/agents/ast-parser.md", DocumentType.AGENT_DEFINITION, "agent in agents/"),
    ("skills/ast/SKILL.md", DocumentType.SKILL_DEFINITION, "skill root file"),

    # OZ-03: composition vs agents (must NOT cross-contaminate)
    ("skills/ps/composition/ps-analyst.prompt.md", DocumentType.SKILL_RESOURCE, "composition file"),
    ("skills/ps/agents/ps-analyst.md", DocumentType.AGENT_DEFINITION, "agent file"),

    # OZ-05: work vs orchestration
    ("projects/PROJ-XXX/work/deep/nested/entity.md", DocumentType.WORKTRACKER_ENTITY, "work entity"),
    ("projects/PROJ-XXX/orchestration/phase-1/plan.md", DocumentType.ORCHESTRATION_ARTIFACT, "orch artifact"),
    ("projects/PROJ-XXX/work/orchestration-notes/plan.md", DocumentType.WORKTRACKER_ENTITY, "OZ-05 boundary"),

    # OZ-07: adversarial vs catch-all templates
    (".context/templates/adversarial/s-014-llm-judge.md", DocumentType.STRATEGY_TEMPLATE, "adversarial template"),
    (".context/templates/worktracker/BUG.md", DocumentType.TEMPLATE, "worktracker template"),
    (".context/templates/design/TDD.template.md", DocumentType.TEMPLATE, "design template"),

    # OZ-08: docs/design vs docs catch-all
    ("docs/design/adr-epic005-003.md", DocumentType.ADR, "ADR in design/"),
    ("docs/BOOTSTRAP.md", DocumentType.KNOWLEDGE_DOCUMENT, "docs catch-all"),
    ("docs/adrs/ADR-001.md", DocumentType.ADR, "ADR in adrs/"),

    # skills/*/rules/ vs .context/rules/ (separate prefix zones, both should work)
    ("skills/worktracker/rules/worktracker-behavior-rules.md", DocumentType.RULE_FILE, "skill rules"),
    (".context/rules/quality-enforcement.md", DocumentType.RULE_FILE, "context rules"),

    # skills/*/knowledge/ vs docs/knowledge/
    ("skills/nasa-se/knowledge/standards/NASA-STANDARDS-SUMMARY.md", DocumentType.KNOWLEDGE_DOCUMENT, "skill knowledge"),
    ("docs/knowledge/architecture/patterns.md", DocumentType.KNOWLEDGE_DOCUMENT, "docs knowledge"),
])
def test_first_match_wins_ordering(path, expected_type, description):
    ...
```

#### 2.4 Negative Tests: Patterns That Must NOT Match

These verify that specific-sounding paths do NOT bleed into wrong types:

```
Test: skills/ file that is NOT agents/ does NOT match AGENT_DEFINITION via path
Input: "skills/problem-solving/PLAYBOOK.md"
Expected: SKILL_RESOURCE (after EN-002 fix)
NOT: AGENT_DEFINITION

Test: projects/ file that is NOT work/ does NOT match WORKTRACKER_ENTITY
Input: "projects/PROJ-XXX/PLAN.md"
Expected: FRAMEWORK_CONFIG
NOT: WORKTRACKER_ENTITY

Test: docs/ file that is NOT design/ does NOT match ADR
Input: "docs/governance/JERRY_CONSTITUTION.md"
Expected: KNOWLEDGE_DOCUMENT
NOT: ADR
```

---

### Part 3: New Enum Value Test Cases

**File:** `tests/unit/domain/markdown_ast/test_document_type.py` (add `TestSkillResourceType` and `TestTemplateType` classes)

#### 3.1 SKILL_RESOURCE Path Pattern Tests

SKILL_RESOURCE covers the following subpaths under `skills/*/`:

| Subpath | Representative File | Pattern |
|---------|--------------------|-|
| `skills/*/PLAYBOOK.md` | `skills/problem-solving/PLAYBOOK.md` | Exact basename |
| `skills/*/rules/*.md` | `skills/worktracker/rules/worktracker-behavior-rules.md` | Dir match |
| `skills/*/tests/*.md` | `skills/problem-solving/tests/BEHAVIOR_TESTS.md` | Dir match |
| `skills/*/composition/*.md` | `skills/problem-solving/composition/ps-analyst.prompt.md` | Dir match |
| `skills/*/docs/*.md` | `skills/nasa-se/docs/NASA-SE-MAPPING.md` | Dir match |
| `skills/*/references/*.md` | `skills/saucer-boy-framework-voice/references/voice-guide.md` | Dir match |
| `skills/*/validation/*.md` | `skills/transcript/validation/ts-critic-extension.md` | Dir match |
| `skills/shared/*.md` | `skills/shared/AGENT_TEMPLATE_CORE.md` | Shallow match |

**Test cases:**

```python
@pytest.mark.parametrize("path", [
    "skills/problem-solving/PLAYBOOK.md",
    "skills/adversary/PLAYBOOK.md",
    "skills/nasa-se/PLAYBOOK.md",
    "skills/shared/AGENT_TEMPLATE_CORE.md",
    "skills/shared/PLAYBOOK_TEMPLATE.md",
    "skills/worktracker/rules/worktracker-behavior-rules.md",
    "skills/worktracker/rules/worktracker-directory-structure.md",
    "skills/problem-solving/tests/BEHAVIOR_TESTS.md",
    "skills/nasa-se/tests/BEHAVIOR_TESTS.md",
    "skills/problem-solving/composition/ps-analyst.prompt.md",
    "skills/worktracker/composition/wt-auditor.prompt.md",
    "skills/nasa-se/docs/NASA-SE-MAPPING.md",
    "skills/orchestration/docs/PATTERNS.md",
    "skills/saucer-boy-framework-voice/references/voice-guide.md",
    "skills/saucer-boy-framework-voice/references/biographical-anchors.md",
    "skills/transcript/validation/ts-critic-extension.md",
])
def test_skill_resource_path_detection(path):
    doc_type, warning = DocumentTypeDetector.detect(path, "")
    assert doc_type == DocumentType.SKILL_RESOURCE
    assert warning is None  # No warning when no structural cue
```

**Negative: SKILL_RESOURCE paths that should NOT match agents/ or SKILL.md:**

```python
@pytest.mark.parametrize("path, wrong_type", [
    ("skills/ast/agents/ast-parser.md", DocumentType.SKILL_RESOURCE),
    ("skills/problem-solving/SKILL.md", DocumentType.SKILL_RESOURCE),
])
def test_skill_resource_does_not_overlap_agent_or_skill(path, wrong_type):
    doc_type, _ = DocumentTypeDetector.detect(path, "")
    assert doc_type != wrong_type
```

**SKILL_RESOURCE structural cue tests:**

Per EN-002 design, structural cues are the fallback for path-unmatched files. After EN-002, SKILL_RESOURCE has no dedicated structural cue (it relies entirely on path detection). Test that a SKILL_RESOURCE file with no structural signals returns SKILL_RESOURCE via path, not via structural cue:

```python
def test_skill_resource_relies_on_path_not_structure():
    """SKILL_RESOURCE must not be reachable via structural cue alone."""
    # A file with PLAYBOOK.md path but no structural content
    doc_type, warning = DocumentTypeDetector.detect("skills/foo/PLAYBOOK.md", "")
    assert doc_type == DocumentType.SKILL_RESOURCE
    assert warning is None

def test_skill_resource_path_wins_over_worktracker_cue():
    """Path classification as SKILL_RESOURCE wins over structural cue for worktracker."""
    # Content has "> **Type:**" worktracker cue, but path says SKILL_RESOURCE
    content = "> **Type:** resource\n"
    doc_type, warning = DocumentTypeDetector.detect("skills/foo/PLAYBOOK.md", content)
    assert doc_type == DocumentType.SKILL_RESOURCE
    assert warning is not None  # Mismatch warning expected (M-14)
    assert "worktracker_entity" in warning
```

#### 3.2 TEMPLATE Path Pattern Tests

TEMPLATE covers:

| Subpath | Representative File | Pattern |
|---------|--------------------|-|
| `.context/templates/worktracker/*.md` | `.context/templates/worktracker/BUG.md` | Dir match |
| `.context/templates/design/*.md` | `.context/templates/design/TDD.template.md` | Dir match |
| `skills/*/templates/*.md` | `skills/nasa-se/templates/alternative-analysis.md` | Dir match |
| `.context/templates/**/*.md` catch-all | `.context/templates/new-category/foo.md` | Recursive |

**Test cases:**

```python
@pytest.mark.parametrize("path", [
    ".context/templates/worktracker/BUG.md",
    ".context/templates/worktracker/ENABLER.md",
    ".context/templates/worktracker/EPIC.md",
    ".context/templates/worktracker/FEATURE.md",
    ".context/templates/design/TDD.template.md",
    ".context/templates/design/PLAYBOOK.template.md",
    "skills/nasa-se/templates/alternative-analysis.md",
    "skills/nasa-se/templates/trade-study.md",
    "skills/orchestration/templates/ORCHESTRATION_PLAN.template.md",
    "skills/orchestration/templates/ORCHESTRATION_WORKTRACKER.template.md",
    "skills/problem-solving/templates/critique.md",
])
def test_template_path_detection(path):
    doc_type, warning = DocumentTypeDetector.detect(path, "")
    assert doc_type == DocumentType.TEMPLATE
    assert warning is None

def test_template_catch_all_for_new_subdir():
    """Unknown template subdir falls to TEMPLATE via catch-all pattern."""
    doc_type, _ = DocumentTypeDetector.detect(
        ".context/templates/future-category/some-template.md", ""
    )
    assert doc_type == DocumentType.TEMPLATE

def test_adversarial_template_not_classified_as_template():
    """STRATEGY_TEMPLATE takes precedence over the TEMPLATE catch-all."""
    doc_type, _ = DocumentTypeDetector.detect(
        ".context/templates/adversarial/s-001-red-team.md", ""
    )
    assert doc_type == DocumentType.STRATEGY_TEMPLATE  # Not TEMPLATE
```

#### 3.3 PATTERN_DOCUMENT Path Pattern Tests

PATTERN_DOCUMENT exists in the enum but had zero path patterns. EN-002 adds patterns for `.context/patterns/**/*.md` and `.context/guides/*.md`:

```python
@pytest.mark.parametrize("path", [
    ".context/patterns/adapter/cli-adapter.md",
    ".context/patterns/aggregate/event-collection.md",
    ".context/patterns/architecture/hexagonal-architecture.md",
    ".context/patterns/cqrs/command-pattern.md",
    ".context/patterns/entity/aggregate-root.md",
    ".context/patterns/event/domain-event.md",
    ".context/patterns/identity/jerry-uri.md",
    ".context/patterns/repository/generic-repository.md",
    ".context/patterns/skill-development/some-pattern.md",
    ".context/guides/architecture-patterns.md",
    ".context/guides/error-handling.md",
])
def test_pattern_document_path_detection(path):
    doc_type, warning = DocumentTypeDetector.detect(path, "")
    assert doc_type == DocumentType.PATTERN_DOCUMENT
    assert warning is None
```

#### 3.4 Updated Enum Completeness Test

The existing test asserts `len(DocumentType) == 11`. After EN-002, update to 13:

```python
def test_enum_has_13_values_post_en002():
    """DocumentType enum expanded to 13 values after EN-002."""
    assert len(DocumentType) == 13
    # Verify new values
    assert DocumentType.SKILL_RESOURCE.value == "skill_resource"
    assert DocumentType.TEMPLATE.value == "template"
    # Verify existing values unchanged
    assert DocumentType.UNKNOWN.value == "unknown"
    assert DocumentType.AGENT_DEFINITION.value == "agent_definition"
```

#### 3.5 Mismatch Warning Tests for New Types

After EN-002, structural cues are precise. Verify that new enum values participate correctly in the M-14 dual-signal warning mechanism:

```python
def test_skill_resource_path_wins_no_warning_when_no_structural_cue():
    """SKILL_RESOURCE path classified with no structural cue produces no warning."""
    doc_type, warning = DocumentTypeDetector.detect("skills/foo/PLAYBOOK.md", "Plain text")
    assert doc_type == DocumentType.SKILL_RESOURCE
    assert warning is None

def test_template_path_wins_no_warning_when_no_structural_cue():
    """TEMPLATE path classified with no structural cue produces no warning."""
    doc_type, warning = DocumentTypeDetector.detect(
        ".context/templates/worktracker/BUG.md", "Plain text"
    )
    assert doc_type == DocumentType.TEMPLATE
    assert warning is None

def test_mismatch_warning_fires_when_template_path_has_agent_structural_cue():
    """Warning fires when TEMPLATE path has a structural cue suggesting agent."""
    content = "<identity>\nAgent identity section.\n</identity>\n"
    doc_type, warning = DocumentTypeDetector.detect(
        ".context/templates/worktracker/BUG.md", content
    )
    assert doc_type == DocumentType.TEMPLATE  # Path wins
    assert warning is not None
    assert "agent_definition" in warning

def test_mismatch_warning_fires_when_skill_resource_path_has_worktracker_cue():
    """Warning fires when SKILL_RESOURCE path has a worktracker structural cue."""
    content = "> **Type:** resource\n"
    doc_type, warning = DocumentTypeDetector.detect(
        "skills/foo/rules/foo-rule.md", content
    )
    assert doc_type == DocumentType.RULE_FILE  # Path wins (rules/ maps to RULE_FILE)
    assert warning is not None
    assert "worktracker_entity" in warning
```

---

### Part 4: Structural Cue Precision Tests (Post-EN-002)

**File:** `tests/unit/domain/markdown_ast/test_document_type.py` (add `TestStructuralCuePrecision` class)

The core BUG-004 fix is replacing `("---", DocumentType.AGENT_DEFINITION)` with precise XML-tag cues. These tests verify the new cues are precise and the old broad cue is gone.

#### 4.1 Regression Gate: "---" Cue Removed

```python
def test_horizontal_rule_does_not_classify_as_agent_definition():
    """BUG-004 regression: --- horizontal rule must NOT classify as agent_definition."""
    # A rule file with no path match and only --- content
    content = "---\n\nSome section content.\n\n---\n"
    doc_type, _ = DocumentTypeDetector.detect("unknown/path.md", content)
    assert doc_type != DocumentType.AGENT_DEFINITION, (
        "BUG-004 REGRESSION: '---' is still classified as agent_definition. "
        "The structural cue '---' must be removed per EN-002 TASK-005."
    )

def test_yaml_frontmatter_block_does_not_classify_as_agent_definition():
    """BUG-004 regression: YAML frontmatter alone must NOT classify as agent_definition."""
    content = "---\nname: test-file\nversion: 1.0\n---\n\n# Content\n"
    doc_type, _ = DocumentTypeDetector.detect("unknown/path.md", content)
    assert doc_type != DocumentType.AGENT_DEFINITION, (
        "BUG-004 REGRESSION: YAML frontmatter (---) is triggering agent_definition."
    )
```

#### 4.2 Positive Precision Tests for New Structural Cues

```python
@pytest.mark.parametrize("cue, expected_type, description", [
    ("<identity>\nRole: Analyst\n</identity>\n", DocumentType.AGENT_DEFINITION, "identity XML tag"),
    ("<methodology>\nStep 1.\n</methodology>\n", DocumentType.AGENT_DEFINITION, "methodology XML tag"),
    ("<purpose>\nWhy this agent.\n</purpose>\n", DocumentType.AGENT_DEFINITION, "purpose XML tag"),
    ("> **Type:** story\n", DocumentType.WORKTRACKER_ENTITY, "blockquote type frontmatter"),
    ("> **Type:** bug\n", DocumentType.WORKTRACKER_ENTITY, "blockquote bug type"),
    ('<!-- L2-REINJECT: rank=1, content="test" -->\n', DocumentType.RULE_FILE, "L2-REINJECT marker"),
    ("## Status\n\nProposed.\n", DocumentType.ADR, "ADR status heading"),
])
def test_structural_cue_precision(cue, expected_type, description):
    """New structural cues classify correctly on unmatched paths."""
    doc_type, _ = DocumentTypeDetector.detect("unmatched/arbitrary/path.md", cue)
    assert doc_type == expected_type, f"Failed for: {description}"
```

#### 4.3 Cue Isolation Tests (No Cross-Cue Contamination)

```python
def test_worktracker_cue_not_triggered_by_generic_blockquote():
    """> ** in content but not the specific "> **Type:**" pattern must not classify."""
    content = "> **Note:** This is a general callout block.\n"
    doc_type, _ = DocumentTypeDetector.detect("unmatched/path.md", content)
    # The new precise cue "> **Type:**" must NOT match "> **Note:**"
    assert doc_type != DocumentType.WORKTRACKER_ENTITY

def test_generic_html_comment_does_not_classify_as_adr():
    """A plain <!-- comment --> must not trigger ADR classification."""
    content = "<!-- This is a simple comment -->\n# Title\n"
    doc_type, _ = DocumentTypeDetector.detect("unmatched/path.md", content)
    # After EN-002, "<!--" is replaced by "## Status" for ADR detection
    assert doc_type != DocumentType.ADR

def test_unknown_returned_when_no_cue_matches():
    """Content with no structural cues and no path match returns UNKNOWN."""
    content = "# Plain Heading\n\nSome plain text. No special markers.\n"
    doc_type, _ = DocumentTypeDetector.detect("some/unclassified/file.md", content)
    assert doc_type == DocumentType.UNKNOWN
    assert _ is None  # No warning on UNKNOWN
```

---

### Part 5: Coverage Strategy

**Target:** >= 90% line coverage on `src/domain/markdown_ast/document_type.py`

**Coverage gap analysis against current implementation:**

| Code Section | Covered By | Gap Risk |
|---|---|---|
| `DocumentType` enum class | Part 3: enum completeness tests | Low -- trivially covered by any test that imports enum |
| `DocumentTypeDetector.detect()` main body | All path/structure tests | Low |
| `detect()` path_type is not None branch | Path tests | Covered |
| `detect()` warning generation (structure != UNKNOWN) | TestDualSignalWarning | Covered |
| `detect()` structure fallback (path_type is None) | Structural detection tests | Covered |
| `detect()` UNKNOWN return | edge_case tests | Covered |
| `_detect_from_path()` iteration | Path tests | Covered |
| `_detect_from_path()` no-match return | UNKNOWN tests | Covered |
| `_detect_from_structure()` empty content branch | edge_case empty string | Covered |
| `_detect_from_structure()` iteration | Structural cue tests | Covered |
| `_normalize_path()` forward slash conversion | Windows-style path test (if added) | MEDIUM GAP |
| `_normalize_path()` leading `./` strip | TestPathNormalization | Covered |
| `_normalize_path()` absolute path with marker | TestPathNormalization | Covered |
| `_normalize_path()` absolute path no marker | NEW: test path with no known marker | GAP |
| `_normalize_path()` basename extraction (CLAUDE.md/AGENTS.md) | TestPathNormalization | Covered |
| `_path_matches_glob()` no `**` branch | Single-star pattern tests | Covered by most path tests |
| `_path_matches_glob()` with `**` branch | `projects/*/work/**/*.md` tests | Covered |
| `_match_recursive_glob()` single `**` with prefix + suffix | `projects/*/work/**/*.md` | Covered |
| `_match_recursive_glob()` multiple `**` fallback | TestRecursiveGlobMatching | Covered |
| `_match_recursive_glob()` prefix too long | TestRecursiveGlobMatching | Covered |
| `_match_recursive_glob()` suffix too long | TestRecursiveGlobMatching | Covered |
| `_match_recursive_glob()` prefix segment mismatch | TestRecursiveGlobMatching | Covered |
| `_match_recursive_glob()` no suffix (suffix_pattern empty) | NEW: pattern like `docs/**` | GAP |
| `_match_recursive_glob()` no prefix (prefix_pattern empty) | NEW: pattern like `**/file.md` | GAP |

**Two new coverage tests to close identified gaps:**

```python
def test_normalize_path_absolute_with_no_known_marker():
    """Absolute path with no repo root marker falls back to the full path."""
    # /tmp/random/file.md has no skills/, docs/, etc. component
    doc_type, _ = DocumentTypeDetector.detect("/tmp/completely/random/file.md", "")
    # Should not crash; result is UNKNOWN (no pattern matches /tmp/... after normalization)
    assert doc_type is not None  # Just verify no exception

def test_recursive_glob_no_suffix_pattern():
    """Pattern with ** and no suffix (trailing **) matches recursively."""
    # If EN-002 adds a pattern like "docs/**" with no trailing filename segment:
    # _match_recursive_glob() suffix_pattern will be empty -> must return True
    # for any path starting with docs/
    # This is a coverage test for the suffix_pattern == "" branch
    # Test indirectly via a pattern that produces this code path
    # (requires internal access or a known pattern that uses trailing **)
    from src.domain.markdown_ast.document_type import _match_recursive_glob
    assert _match_recursive_glob("docs/knowledge/foo.md", "docs/**") is True
    assert _match_recursive_glob("docs/bar.md", "docs/**") is True
    assert _match_recursive_glob("other/foo.md", "docs/**") is False
```

**Coverage enforcement command:**

```bash
uv run pytest tests/unit/domain/markdown_ast/test_document_type.py \
              tests/integration/test_document_type_regression.py \
              --cov=src/domain/markdown_ast/document_type \
              --cov-report=term-missing \
              --cov-fail-under=90
```

---

### Part 6: Test Execution Order and Isolation

**Isolation guarantee:** The regression test calls `DocumentTypeDetector.detect()` which is a pure function (no I/O, no global state mutation). All state is in the arguments. Tests are fully parallelizable with `pytest-xdist` if needed for performance.

**Execution order recommendation:**

```
1. Unit tests first (fast, fail fast on enum/pattern regressions):
   tests/unit/domain/markdown_ast/test_document_type.py

2. Regression suite second (slow, validates full repo):
   tests/integration/test_document_type_regression.py

3. Coverage measurement covers both in one run.
```

**Marker usage:**

| Test Group | Markers |
|-----------|---------|
| BUG-004 regression gate | `@pytest.mark.regression`, `@pytest.mark.security` |
| Pattern ordering boundary tests | `@pytest.mark.boundary`, `@pytest.mark.security` |
| New enum value tests | `@pytest.mark.happy_path` |
| Structural cue precision tests | `@pytest.mark.security`, `@pytest.mark.edge_case` |
| UNKNOWN allowlist gate | `@pytest.mark.regression`, `@pytest.mark.integration` |

---

## L2 Strategic Implications

### Test Strategy Effectiveness Assessment

The two-file strategy (regression integration test + unit test extension) achieves distinct quality properties:

**Regression test strengths:**
- Scope is the entire repo, so ontology gaps cannot hide in uncovered path zones.
- The allowlist gate converts "silent classification failure" into an explicit, reviewable decision. Every new file category added to the repo creates a CI failure until it is explicitly classified or allowlisted.
- The BUG-004 regression gate (Assertion Group A) is a single-line guard that prevents the most damaging defect from returning: structural cue misclassification at scale.

**Regression test limitations:**
- Test count (2,774+) grows as the repo grows. At 10,000 files, execution time may exceed TC-4's 30-second limit. Mitigation: `detect()` is a pure O(n_patterns) string operation with no I/O -- should remain sub-10ms per call even at 10,000 files.
- The test discovers files at import time, making the parametrize list a static snapshot. Files added between test collection and test execution are not tested in the same run. This is acceptable since CI runs on commit.

**Unit test strengths:**
- Overlap zone boundary tests provide deterministic coverage of the security-critical ordering invariants that the regression test cannot isolate (a regression test failure does not identify WHICH pattern ordering was wrong).
- Mismatch warning tests cover M-14 dual-signal behavior independently of the full repo scan.

### Fuzzing ROI Analysis

Fuzzing is not the primary value-add for this component. `detect()` is a deterministic string matching function with no complex state machine. The security risks are structural (wrong ordering, wrong cue) not input-dependent (malformed input). Property-based testing is more appropriate than coverage-guided fuzzing for this use case.

**Property-based tests (Hypothesis) worth considering for future iterations:**

| Property | Hypothesis Strategy |
|----------|---------------------|
| Path classification is total: detect() never raises for any string input | `@given(st.text())` for both path and content |
| Path-classified results are stable: same path always returns same type | `@given(st.sampled_from(PATH_PATTERNS))` |
| UNKNOWN never triggers a warning: UNKNOWN result always has warning=None | `@given(st.text(), st.text())` |

These are MEDIUM priority for a future iteration; the parametrized regression suite and boundary unit tests provide sufficient coverage for TASK-006.

### Coverage Gap Risk Analysis

After EN-002 implementation, two coverage gaps remain in `_match_recursive_glob()`:

| Gap | Risk | Mitigation |
|-----|------|-----------|
| `suffix_pattern == ""` branch (trailing `**` pattern) | Low: no current pattern uses trailing `**` without suffix | Add direct unit test for `_match_recursive_glob` with trailing `**` pattern |
| Absolute path with no repo marker | Low: all real-world usage passes relative paths | Add edge case unit test |

Both gaps are < 5 lines total; closing them brings line coverage from estimated 87% to >= 90%.

### Regression Suite Maintenance Considerations

**When a new file category is added to the repo:**
1. CI fails because the new files return UNKNOWN and are not in `EXPECTED_UNKNOWN`.
2. The implementer must either: (a) add a `PATH_PATTERN` entry to classify the new category, or (b) add an `EXPECTED_UNKNOWN` entry with justification.
3. This is the intended design: the regression test acts as an ontology governance gate.

**When a pattern is changed:**
1. Run the regression suite to verify no previously-classified files now return UNKNOWN.
2. The boundary unit tests will catch ordering regressions independently.

**Allowlist maintenance:**
- The allowlist should be reviewed on each sprint cycle.
- If a file in `EXPECTED_UNKNOWN` becomes classifiable via a new pattern, remove it from the allowlist and add the pattern.
- Target: `EXPECTED_UNKNOWN` should never exceed 20 entries. If it grows beyond 20, that signals a pattern design problem (too many exceptional files) rather than genuinely unclassifiable content.

---

## OWASP Mapping

| OWASP TG Category | Test Coverage in This Strategy |
|---|---|
| INPVAL (Input Validation) | Structural cue precision tests; path normalization edge cases; arbitrary string inputs to detect() |
| BUSLOGIC (Business Logic) | First-match-wins ordering tests; BUG-004 regression gate; allowlist gate |
| CLNT (Client-side, interpreted as "consumer trust") | Mismatch warning tests (M-14); UNKNOWN safe default verification |

**SSDF Mapping:**
- PW.8.1: Testing executable code to find vulnerabilities -- regression parametrized suite
- PW.8.2: Using automated test infrastructure -- `uv run pytest` + `--cov-fail-under=90`

---

*Strategy Version: 1.0.0*
*Agent: eng-qa*
*Date: 2026-02-24*
*TASK-006 of EN-002 Document Type Ontology Hardening*
*Input sources: BUG-004 RCA, EN-002 design, document_type.py source, live repo file scan*
