# S-007: Constitutional AI Critique

<!-- VERSION: 1.0.0 | DATE: 2026-02-15 | ENABLER: EN-805 | FORMAT: 1.1.0
Implements H-18 via principle-by-principle constitutional review. C2+ REQUIRED. -->

> **Type:** adversarial-strategy-template
> **Status:** ACTIVE
> **Version:** 1.0.0
> **Date:** 2026-02-15
> **Format Compliance:** TEMPLATE-FORMAT.md v1.1.0
> **Source:** quality-enforcement.md, JERRY_CONSTITUTION.md

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Identity](#identity) | Strategy identification and classification |
| [Purpose](#purpose) | When and why to apply S-007 |
| [Prerequisites](#prerequisites) | Required constitutional context and inputs |
| [Execution Protocol](#execution-protocol) | Systematic principle-by-principle review |
| [Output Format](#output-format) | Constitutional compliance report structure |
| [Scoring Rubric](#scoring-rubric) | Meta-evaluation of strategy execution quality |
| [Examples](#examples) | Concrete C2 demonstration with findings |
| [Integration](#integration) | Pairing guidance and criticality mapping |
| [Validation Checklist](#validation-checklist) | Template compliance verification |

---

## Identity

| Field | Value |
|-------|-------|
| Strategy ID | S-007 |
| Strategy Name | Constitutional AI Critique |
| Family | Iterative Self-Correction |
| Composite Score | 4.15 |
| Finding Prefix | CC-NNN-{execution_id} |
| Version | 1.0.0 |
| Date | 2026-02-15 |

### Criticality Tier Table

| Level | Name | Status | Notes |
|-------|------|--------|-------|
| C1 | Routine | NOT USED | C1 enforces HARD rules only; constitutional review not required |
| C2 | Standard | REQUIRED | Part of C2 required set (S-007, S-002, S-014) |
| C3 | Significant | REQUIRED | Inherited from C2 set |
| C4 | Critical | REQUIRED | All 10 strategies required |

**Foundation:** Bai et al. 2022 Constitutional AI (Anthropic) — AI self-correction via explicit principles.

**Jerry Implementation:** Evaluates against Jerry Constitution, behavioral rules, quality framework. Implements H-18.

---

## Purpose

### When to Use

1. **C2+ Deliverable Review:** ALL Standard+ deliverables MUST undergo constitutional review (H-18)
2. **Governance Changes:** Modifications to `.context/rules/`, constitution, templates (AE-001, AE-002)
3. **Architecture/Design:** Deliverables establishing patterns, conventions, constraints
4. **Pre-Merge Quality Gate:** Work affecting shared infrastructure, APIs, framework behavior
5. **Post-Failure Analysis:** Root cause diagnosis for failed adversarial strategies

### When NOT to Use

1. **C1 Routine Work:** L3 deterministic checks sufficient for reversible changes
2. **Pure Data Files:** JSON, YAML, CSV without behavioral implications
3. **Constitution Unavailable:** Defer to S-014 with generic rubric; redirect to S-011 for data validation

### Expected Outcome

Systematic constitutional compliance report: enumerates applicable principles, classifies by tier (HARD/MEDIUM/SOFT), evaluates compliance, maps violations to quality dimensions/severity, provides actionable remediation, scores overall compliance for S-014 integration.

### Pairing Recommendations

**Required:** S-014 (findings feed dimension scoring), S-010 (H-15 self-review includes constitutional check)

**Recommended:** S-003 (H-16: strengthen before review), S-002 (evaluate attack compliance)

**Optimal order:** S-003 → S-007 → S-002 → S-014

---

## Prerequisites

### Required Inputs

- [ ] Deliverable artifact (document, code, design, decision record)
- [ ] Criticality level classification (C2, C3, or C4)
- [ ] Jerry Constitution (`docs/governance/JERRY_CONSTITUTION.md`)
- [ ] Applicable behavioral rules from `.context/rules/`
- [ ] Quality framework SSOT (`quality-enforcement.md`)
- [ ] Auto-escalation rules (AE-001 through AE-006) for criticality-based principle selection

### Context Requirements

Load: `JERRY_CONSTITUTION.md` (P-001–P-043), `.context/rules/*.md` (H-01–H-24), `quality-enforcement.md` (SSOT).

**Tier Mapping:** HARD (MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL→Critical), MEDIUM (SHOULD, RECOMMENDED, PREFERRED, EXPECTED→Major), SOFT (MAY, CONSIDER, OPTIONAL, SUGGESTED→Minor).

### Ordering Constraints

**Optimal (H-16):** S-003 → S-007 → S-002 → S-014
**Minimum:** S-007 before S-014 for dimensional evidence.

---

## Execution Protocol

### Step 1: Load Constitutional Context

**Action:** Systematically load all constitutional sources and applicable rules.

**Procedure:**

1. Read `docs/governance/JERRY_CONSTITUTION.md` in full
2. Identify deliverable type (code, document, design, template, rule)
3. Based on type, load applicable rules from `.context/rules/`:
   - Code deliverables: `architecture-standards.md`, `coding-standards.md`, `python-environment.md`, `testing-standards.md`
   - Document deliverables: `markdown-navigation-standards.md`, `quality-enforcement.md`
   - Template/rule deliverables: ALL rules (AE-002 triggers auto-C3)
   - Architecture/design: `architecture-standards.md`, `file-organization.md`
4. Read `quality-enforcement.md` for HARD rule index (H-01 through H-24), tier vocabulary, auto-escalation rules
   - **H-Rule Quick Reference:** 24 HARD rules exist (H-01 through H-24). See quality-enforcement.md lines 38-63 for the complete H-rule index with rule text and source files. Review this index before Step 2 to ensure no HARD rules are missed during principle enumeration.
5. Create index of all loaded principles with tier classification

**Decision Point:** AE-001 (constitution→C4), AE-002 (rules/templates→C3)

**Output:** Constitutional Context Index with principle ID, name, tier, source, applicability.

### Step 2: Enumerate Applicable Principles

**Action:** Filter constitutional principles to those relevant to the deliverable.

**Procedure:**

1. Review deliverable to identify scope categories (e.g., architecture, coding, testing, governance, work management)
2. For each loaded principle:
   - Determine if principle applies to deliverable scope
   - Mark as applicable or not applicable
   - Document rationale for applicability determination
3. Segregate applicable principles by tier (HARD, MEDIUM, SOFT)
4. Prioritize HARD principles first (violations block acceptance)
5. Create Applicable Principles Checklist

**Decision Point:** Zero principles→exit (not applicable). 10+ HARD→flag high-risk.

**Output:** Applicable Principles Checklist (ID, tier, rationale, priority).

### Step 3: Principle-by-Principle Evaluation

**Action:** Systematically evaluate deliverable compliance with each applicable principle.

**Procedure:**

For each principle in the Applicable Principles Checklist (HARD tier first):

1. **State the principle:** Quote the exact rule text from the constitutional source
2. **Identify compliance criteria:** What would constitute compliance? What would constitute violation?
3. **Search the deliverable:** Look for evidence of compliance or violation
4. **Classify result:**
   - **COMPLIANT:** Deliverable adheres to principle. Document supporting evidence.
   - **VIOLATED:** Deliverable violates principle. Document violation location, quote problematic content, explain why it violates.
   - **AMBIGUOUS:** Unclear whether deliverable complies. Flag for human review.
5. **Map to quality dimension:** Which S-014 dimension does this principle most affect? (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability)
6. **Assign severity:**
   - HARD tier violation → **Critical** (blocks acceptance per H-13)
   - MEDIUM tier violation → **Major** (requires revision)
   - SOFT tier violation → **Minor** (improvement opportunity)
   - **Edge cases:** If 5+ MEDIUM violations cluster in the same file, module, or design component, CONSIDER escalating aggregate severity to Critical. If 10+ SOFT violations cluster around the same architectural concern, CONSIDER escalating to Major. If a SOFT violation has architectural impact (e.g., violating an optional best practice that prevents a critical failure mode), CONSIDER escalating to Major. Document escalation rationale in findings.
7. **Document finding:** Record in findings table with CC-NNN-{execution_id} identifier

**Decision Point:** HARD violation→REJECTED (H-13). 3+ MEDIUM→recommend rejection. SOFT only→may PASS.

**Output:** Findings Table (CC-NNN-{execution_id}, principle, severity, evidence, dimension).

### Step 4: Generate Remediation Guidance

**Action:** Provide specific, actionable recommendations to address each violation.

**Procedure:**

1. For each violation finding (Critical and Major severity):
   - **Locate:** Specify exact file, line number, section, or artifact location
   - **Quote:** Excerpt the problematic content (2-5 lines context)
   - **Explain:** Why does this violate the principle? What harm does it cause?
   - **Recommend:** Specific action to remediate (not generic "fix this")
   - **Provide example:** If applicable, show corrected version inline
2. Prioritize recommendations:
   - **P0:** Critical violations (HARD rules) — MUST fix before acceptance
   - **P1:** Major violations (MEDIUM rules) — SHOULD fix; require justification if not
   - **P2:** Minor violations (SOFT rules) — CONSIDER fixing
3. Group recommendations by affected file or section for efficient remediation
4. Cross-reference related findings (e.g., multiple violations of same principle)

**Decision Point:** Unclear remediation→escalate. Architecture change→flag C3/C4.

**Output:** Prioritized Remediation Plan (P0/P1/P2 with specific actions).

### Step 5: Score Constitutional Compliance

**Action:** Assess overall constitutional compliance for integration with S-014 scoring.

**Procedure:**

1. Calculate violation distribution:
   - Critical violations: `N_critical`
   - Major violations: `N_major`
   - Minor violations: `N_minor`
2. Apply penalty model (template-specific operational values, NOT sourced from quality-enforcement.md SSOT):
   - Each Critical violation: -0.10 from composite score
   - Each Major violation: -0.05 from composite score
   - Each Minor violation: -0.02 from composite score
   - Base score starts at 1.00
   - **Note:** These penalty values are operational guidelines for constitutional compliance scoring. The authoritative threshold (0.92) and dimension weights are defined in quality-enforcement.md.
3. Calculate constitutional compliance score: `1.00 - (0.10 * N_critical + 0.05 * N_major + 0.02 * N_minor)`
4. Apply threshold:
   - Score >= 0.92: PASS constitutional gate
   - Score 0.85-0.91: REVISE (near threshold)
   - Score < 0.85: REJECTED (H-13 applies)
5. Map constitutional findings to S-014 dimensions using the Affected Dimension field from findings table
6. Document impact on each dimension (Positive/Negative/Neutral with rationale)
7. **Verify calculation:** Example verification: If 2 Critical + 3 Major + 5 Minor violations, penalty = 2(0.10) + 3(0.05) + 5(0.02) = 0.20 + 0.15 + 0.10 = 0.45. Base score 1.00 - 0.45 = 0.55 → REJECTED (below 0.85 threshold). See Example 1 (line 415) for additional verification.

**Decision Point:** Score <0.92→revision REQUIRED (H-13). Score >=0.92 with Major violations→recommend revision.

**Output:** Compliance Score, threshold (PASS/REVISE/REJECTED), Scoring Impact Table (S-014 dimensions).

---

## Output Format

### Required Output Sections

Every S-007 execution MUST produce a document with these sections:

#### 1. Header

```markdown
# Constitutional Compliance Report: {{DELIVERABLE_NAME}}

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** {{Artifact name, file path, or work item ID}}
**Criticality:** {{C1/C2/C3/C4}}
**Date:** {{ISO 8601 date}}
**Reviewer:** {{Agent ID or human name}}
**Constitutional Context:** {{Version of JERRY_CONSTITUTION.md, list of loaded rules}}
```

#### 2. Summary

2-3 sentence overall assessment:

- Constitutional compliance status (COMPLIANT / PARTIAL / NON-COMPLIANT)
- Count of Critical/Major/Minor findings
- Recommendation (ACCEPT / REVISE / REJECT)

_Example: "PARTIAL compliance: 1 Critical (H-07), 3 Major (naming), 2 Minor (docs). Score: 0.87 (REVISE). Recommend revision."_

#### 3. Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-{execution_id} | H-07: Domain layer imports | HARD | Critical | `domain/work_item.py:5` imports from `application/` | Methodological Rigor |
| CC-002-{execution_id} | M-03: Port naming convention | MEDIUM | Major | `IWorkItemRepo` should be `IWorkItemRepository` | Internal Consistency |
| CC-003-{execution_id} | S-12: Docstring detail level | SOFT | Minor | Public function lacks Args section | Completeness |

**Finding ID Format:** `CC-{NNN}-{execution_id}` where execution_id is a short timestamp or session identifier (e.g., `CC-001-20260215T1430`) to prevent ID collisions across tournament executions.

**Severity Definitions:**

- **Critical:** Violates HARD rule. Blocks acceptance per H-13.
- **Major:** Violates MEDIUM rule. Requires revision or documented justification.
- **Minor:** Violates SOFT rule. Improvement opportunity only.

#### 4. Finding Details

Expanded description for each Critical and Major finding:

```markdown
### CC-001: H-07 Domain Layer Import Violation [CRITICAL]

**Principle:** H-07 domain layer import restrictions
**Location:** `domain/work_item.py:5`
**Evidence:** `from application.commands import CreateWorkItemCommand`
**Impact:** Violates hexagonal architecture; couples domain to application layer
**Dimension:** Methodological Rigor
**Remediation:** Move shared interface to `shared_kernel/commands.py`
```

#### 5. Recommendations

Prioritized action list (P0 = Critical, P1 = Major, P2 = Minor):

```markdown
## Remediation Plan

**P0 (Critical):** CC-001: Refactor domain imports to shared_kernel
**P1 (Major):** CC-002: Rename ports per M-03. CC-004: Add Returns to docstrings
**P2 (Minor):** CC-003: Expand Args sections
```

#### 6. Scoring Impact

Map constitutional findings to S-014 scoring dimensions:

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | CC-003 (Minor): Missing Args sections reduce documentation completeness |
| Internal Consistency | 0.20 | Negative | CC-002 (Major): Inconsistent port naming violates framework conventions |
| Methodological Rigor | 0.20 | Negative | CC-001 (Critical): Layer dependency violation undermines hexagonal architecture |
| Evidence Quality | 0.15 | Neutral | No constitutional findings affect evidence quality |
| Actionability | 0.15 | Neutral | No constitutional findings affect actionability |
| Traceability | 0.10 | Neutral | No constitutional findings affect traceability |

**Constitutional Compliance Score:** 0.87 (1 Critical @ -0.10, 3 Major @ -0.15, 2 Minor @ -0.04)

**Threshold Determination:** REVISE (0.85-0.91 band; below H-13 threshold of 0.92)

---

## Scoring Rubric

### Threshold Bands

**SSOT threshold (quality-enforcement.md, MUST NOT redefine):** >= 0.92 weighted composite score. Below threshold = REJECTED; revision required per H-13.

**Operational bands for S-007 execution quality:**

| Band | Score Range | Outcome |
|------|------------|---------|
| PASS | >= 0.92 | Strategy execution demonstrates systematic constitutional review |
| REVISE | 0.85 - 0.91 | Strategy execution has gaps in principle coverage or evidence quality |
| REJECTED | < 0.85 | Strategy execution inadequate; missing key principles or unsupported findings |

> **Note:** These bands evaluate the STRATEGY EXECUTION quality (how well S-007 was performed), not the deliverable being reviewed. Deliverable scoring uses the Constitutional Compliance Score from Step 5.

### Dimension Weights

From quality-enforcement.md (MUST NOT redefine):

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

### Strategy-Specific Rubric

Scoring criteria for evaluating S-007 execution quality:

#### Strategy-Specific Rubric (All 6 Dimensions)

| Dimension (Weight) | 0.95+ | 0.90-0.94 | 0.85-0.89 | <0.85 |
|--------------------|-------|-----------|-----------|-------|
| **Completeness (0.20)** | ALL principles covered | 90%+ covered | 80-89% covered | <80%; HARD rules missed |
| **Internal Consistency (0.20)** | Zero contradictions; tier-aligned severity | 1-2 minor issues | 3-4 inconsistencies | 5+ contradictions; unreliable |
| **Methodological Rigor (0.20)** | ALL 5 steps executed; systematic | Minor deviations | Steps rushed/skipped | Major procedural failures |
| **Evidence Quality (0.15)** | ALL findings: location, quote, explanation, dimension | 90%+ full evidence | 80-89% adequate | <80%; assertions unverified |
| **Actionability (0.15)** | ALL P0/P1/P2 specific, implementable | 90%+ actionable | 80-89%; vague remediation | <80%; generic advice only |
| **Traceability (0.10)** | ALL principle ID, source, location, dimension | 90%+ traceable | 80-89%; missing refs | <80%; cannot trace to constitution |

---

## Examples

### Example 1: C2 Architecture Deliverable (Command Handler Implementation)

**Context:** Developer implemented a new command handler `CreateProjectCommandHandler` as part of standard (C2) feature work. Constitutional review required per H-18 before merge.

**Before (Problematic Code):**

```python
# src/application/commands/create_project_command_handler.py
from application.ports import ICommandHandler
from infrastructure.adapters.filesystem_project_adapter import FilesystemProjectAdapter  # CC-001 violation
from domain.project import Project

class CreateProjectCommandHandler(ICommandHandler):
    def handle(self, command):  # CC-002 violation (no type hints per H-11)
        adapter = FilesystemProjectAdapter()  # CC-003 violation (violates H-09 composition root)
        project = Project.create(command.project_id, command.name)
        adapter.save(project)
        # CC-004 violation (no docstring per H-12)
```

**Strategy Execution:**

**Step 1:** Loaded `JERRY_CONSTITUTION.md`, `architecture-standards.md`, `coding-standards.md`, `quality-enforcement.md`.

**Step 2:** Identified applicable principles:
- H-08: Application layer MUST NOT import from infrastructure (HARD)
- H-09: Only bootstrap.py SHALL instantiate infrastructure adapters (HARD)
- H-11: Type hints REQUIRED on public functions (HARD)
- H-12: Docstrings REQUIRED on public classes (HARD)
- M-05: Handler naming convention `{Command}Handler` (MEDIUM)

**Step 3:** Principle evaluation findings:

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| CC-001-20260215T1430 | H-08: Application layer imports | HARD | Critical | Line 3: imports `infrastructure.adapters` | Methodological Rigor |
| CC-002-20260215T1430 | H-11: Type hints required | HARD | Critical | Line 6: `handle(self, command)` lacks type annotations | Methodological Rigor |
| CC-003-20260215T1430 | H-09: Composition root exclusivity | HARD | Critical | Line 8: instantiates `FilesystemProjectAdapter` outside bootstrap | Methodological Rigor |
| CC-004-20260215T1430 | H-12: Docstrings required | HARD | Critical | Class lacks docstring | Completeness |
| CC-005-20260215T1430 | M-05: Handler naming | MEDIUM | Major | COMPLIANT (`CreateProjectCommandHandler`) | N/A |

**Step 4:** Remediation guidance (Critical findings only):

**CC-001-20260215T1430:** Remove infrastructure import. Inject adapter via constructor (dependency inversion).
**CC-002-20260215T1430:** Add type hints: `def handle(self, command: CreateProjectCommand) -> None:`
**CC-003-20260215T1430:** Remove adapter instantiation. Accept adapter as constructor parameter; bootstrap.py instantiates.
**CC-004-20260215T1430:** Add class docstring with Google-style format.

**Step 5:** Constitutional compliance score: `1.00 - (4 * 0.10) = 0.60` → REJECTED

**After (Corrected):**

```python
class CreateProjectCommandHandler(ICommandHandler):
    """Handles CreateProjectCommand by creating a new Project aggregate."""

    def __init__(self, repository: IProjectRepository) -> None:
        self._repository = repository

    def handle(self, command: CreateProjectCommand) -> None:
        """Execute project creation. Args: command with project_id, name."""
        project = Project.create(command.project_id, command.name)
        self._repository.save(project)
```

**Result:** 4 Critical violations resolved. Score: 0.60→1.00 (REJECTED→PASS). Now complies with H-08, H-11, H-09, H-12.

---

## Integration

### Canonical Pairings

1. **S-014:** REQUIRED. Findings map to dimensions. Run S-007 before S-014.
2. **S-010:** S-007 implements H-15 constitutional check within S-010 self-review.
3. **S-003:** RECOMMENDED (H-16). Strengthen before review.
4. **S-002:** Evaluate attack compliance. Run after S-007.

**Optimal:** S-003 → S-007 → S-002 → S-014 → S-010

### H-16 Compliance

S-007 is critique; run S-003 first per H-16. Exception: post-failure analysis reviews actual failed artifact.

### Criticality-Based Selection Table

From quality-enforcement.md (MUST NOT modify):

| Level | Required Strategies | Optional Strategies |
|-------|---------------------|---------------------|
| C1 | S-010 | S-003, S-014 |
| C2 | S-007, S-002, S-014 | S-003, S-010 |
| C3 | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 |
| C4 | All 10 selected | None |

**S-007 status:** REQUIRED at C2, C3, C4. NOT USED at C1 (C1 uses deterministic L3 HARD rule enforcement only).

### Auto-Escalation Integration

Check in Step 1: AE-001 (constitution→C4), AE-002 (rules/templates→C3), AE-003 (ADR→C3), AE-004 (baselined ADR→C4), AE-005 (security→C3). If triggered, escalate criticality and expand principle coverage.

### Cross-References

**Sources:** `quality-enforcement.md` (SSOT H-01–H-24), `JERRY_CONSTITUTION.md` (P-001–P-043), `architecture-standards.md` (H-07–H-10), `coding-standards.md` (H-11, H-12), `testing-standards.md` (H-20, H-21), `markdown-navigation-standards.md` (H-23, H-24)

**Templates:** s-003-steelman (before), s-002-devils-advocate (after), s-014-llm-as-judge (scoring), s-010-self-refine (H-15)

**Academic:** Bai et al. 2022 Constitutional AI, ADR-EPIC002-001/002

---

## Validation Checklist

Use this checklist to validate this S-007 template against TEMPLATE-FORMAT.md v1.1.0.

- [x] All 8 canonical sections present (Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration)
- [x] H-23: Navigation table present
- [x] H-24: Navigation table uses anchor links
- [x] Metadata blockquote header present
- [x] File length under 500 lines (currently ~480)
- [x] Identity: 7 required fields + criticality tier table
- [x] Purpose: 5+ "When to Use", 3 "When NOT to Use", measurable outcome, pairing recs
- [x] Prerequisites: Input checklist, context requirements, ordering constraints (H-16)
- [x] Execution Protocol: 5 steps with step format, decision points, CC-NNN-{execution_id} finding prefix, severity defs
- [x] Output Format: 6 output sections, scoring impact table with correct weights, evidence requirements
- [x] Scoring Rubric: Threshold bands match SSOT, weights match SSOT, strategy-specific 4-band rubric
- [x] Examples: 1 C2 example with Before/After, findings with CC-NNN-{execution_id} identifiers, severity applied
- [x] Integration: Pairings, H-16 compliance, criticality table matches SSOT, cross-references

---

<!-- VERSION: 1.0.0 | CREATED: 2026-02-15 | ENABLER: EN-805 | FORMAT: TEMPLATE-FORMAT.md v1.1.0 -->
