# SPIKE-002 Phase 6: Go/No-Go Recommendation

> ps-synthesizer-002 | Phase 6 | spike-eval-20260219-001
> Date: 2026-02-20
> Input: Phase 4 integration patterns research, Phase 5 feasibility analysis, SPIKE-001 handoff
> Self-review (S-010) applied before writing.

<!-- VERSION: 1.2.0 | DATE: 2026-02-20 | SOURCE: SPIKE-002 Phase 6 Decision Synthesis | QG2: iteration-2 revision -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Decision Summary](#l0-decision-summary) | Go/no-go verdict for stakeholders |
| [L1: Integration Architecture](#l1-integration-architecture) | Pattern D specification, component breakdown, LOC budget |
| [L2: Migration Roadmap](#l2-migration-roadmap) | 4-phase implementation plan with milestones |
| [FEAT-001 Scope Definition](#feat-001-scope-definition) | What goes into the production feature |
| [Hypothesis Resolution](#hypothesis-resolution) | SPIKE-002 hypotheses tested against evidence |
| [NO-GO Alternative Strategy](#no-go-alternative-strategy) | What to do if the AST approach is rejected entirely |
| [GO/NO-GO Sensitivity Analysis](#gono-go-sensitivity-analysis) | Conditions that would flip the decision |
| [R-01 Decision Tree](#r-01-decision-tree) | Explicit thresholds and escalation paths for R-01 |
| [Conditions and Assumptions](#conditions-and-assumptions) | What must remain true for this recommendation to hold |
| [Decision Record](#decision-record) | Structured decision output |
| [Evidence Traceability](#evidence-traceability) | Claim-to-source mapping with section-level paths |
| [References](#references) | Source traceability |

---

## L0: Decision Summary

### Verdict: GO -- Bounded Scope, Conditional on R-01 Validation

**Recommendation:** Adopt the AST-first architecture for Jerry's schema-heavy markdown files using markdown-it-py v4.0.0 + mdformat v1.0.0, integrated via Pattern D (Hybrid: CLI commands for batch/CI operations + Claude skill for interactive operations), with a shared domain layer as the single source of truth.

**Scope boundary:** Apply AST-first to files with 3+ schematizable structural patterns (WORKTRACKER entities, skill definitions, rule files, templates, orchestration state). Exclude freeform files (research notes, ADR prose, experience reports) where the current Read + Edit approach is adequate.

**Critical condition:** R-01 (mdformat plugin API for blockquote frontmatter write-back) must be validated in the proof-of-concept before committing to production implementation. If R-01 materializes, the fallback path (string-level substitution within the AST framework, or switch to mistletoe) preserves the GO decision with reduced elegance.

**Confidence:** Medium-High (0.75). Calibration: 0.75 represents a subjective probability that the recommended approach will be successfully implemented without requiring a fallback beyond Fallback A (string substitution). The components: library selection confidence is high (~0.90, backed by SPIKE-001 QG1 score of 0.96), architecture pattern confidence is high (~0.85, Pattern D aligns with existing hexagonal design), and R-01 resolution confidence is moderate (~0.65, write-back is the one unvalidated interaction). The composite 0.75 reflects the bottleneck of R-01. If R-01 resolves favorably (proof-of-concept in Phase 1), confidence rises to ~0.90. The recommendation is supported by Phase 4 architecture analysis and Phase 5 feasibility assessment, with all 5 SPIKE-002 hypotheses partially or fully validated.

**Why GO despite partial token savings:** The primary benefit is structural correctness, not token efficiency. Token reduction (15-30% individual, 40-60% batch) is a secondary benefit that partially validates H1 but is not the decision driver. The decision driver is that 4 of 6 Jerry structural patterns currently have zero automated error detection; AST-based schema validation eliminates this gap (Phase 5, Schema Validation Capability, Section 2). Additionally, the AST approach enables batch operations (bulk validation, multi-file status updates) that are impractical with raw text manipulation.

**Key numbers:**
- ~720 LOC domain layer (470 LOC extensions + 250 LOC schema validation); ~1,740 LOC total including adapters, application layer, and tests
- ~250 LOC CLI adapter + ~150 LOC skill scripts + ~200 LOC application handlers + ~300 LOC tests
- ~20 files touched in migration across 6 skills
- 4-6 weeks to full migration; 1-2 weeks to usable state
- 15-30% token savings per individual operation; 40-60% for batch operations
- 5 of 6 Jerry structural patterns schematizable for validation

---

## L1: Integration Architecture

### Pattern D: Hybrid (CLI + Skill)

The architecture follows Jerry's hexagonal pattern with the markdown AST domain layer as the core, and two interface adapters (CLI and skill) that are thin wrappers calling the same application layer.

```
┌─────────────────────────────────────────────────────────┐
│                    INTERFACE LAYER                        │
│                                                          │
│  ┌──────────────────┐    ┌─────────────────────────┐    │
│  │  CLI Adapter      │    │  Skill Scripts           │    │
│  │  jerry ast ...    │    │  skills/ast/scripts/     │    │
│  │  (~250 LOC)       │    │  (~150 LOC)              │    │
│  └────────┬─────────┘    └───────────┬─────────────┘    │
│           │                          │                    │
│           ▼                          ▼                    │
│  ┌──────────────────────────────────────────────────┐    │
│  │              APPLICATION LAYER                     │    │
│  │  ParseDocumentCommand  | QueryNodesQuery           │    │
│  │  TransformDocumentCmd  | ValidateDocumentQuery     │    │
│  │  (~200 LOC handlers)                               │    │
│  └──────────────────────┬───────────────────────────┘    │
│                         │                                 │
│                         ▼                                 │
│  ┌──────────────────────────────────────────────────┐    │
│  │              DOMAIN LAYER                          │    │
│  │  JerryDocument (facade)     (~130 LOC)            │    │
│  │  BlockquoteFrontmatter      (~220 LOC)            │    │
│  │  L2ReinjectParser           (~120 LOC)            │    │
│  │  NavTableHelpers            (~120 LOC)            │    │
│  │  SchemaValidator            (~250 LOC)            │    │
│  │  ─────────────────────────────────────            │    │
│  │  Total domain:              (~840 LOC)            │    │
│  └──────────────────────┬───────────────────────────┘    │
│                         │                                 │
│                         ▼                                 │
│  ┌──────────────────────────────────────────────────┐    │
│  │              INFRASTRUCTURE LAYER                  │    │
│  │  markdown-it-py v4.0.0  |  mdformat v1.0.0       │    │
│  │  mdit-py-plugins (frontmatter)                    │    │
│  └──────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Component Breakdown

| Component | Location | LOC | Purpose |
|-----------|----------|:---:|---------|
| JerryDocument facade | `src/domain/markdown_ast/jerry_document.py` | ~130 | Unified API: parse(), query(), transform(), render(), validate() |
| Blockquote frontmatter | `src/domain/markdown_ast/frontmatter.py` | ~220 | Extract/modify `**Key:** Value` patterns in blockquotes |
| L2-REINJECT parser | `src/domain/markdown_ast/reinject.py` | ~120 | Parse/modify `<!-- L2-REINJECT: ... -->` comments |
| Navigation table helpers | `src/domain/markdown_ast/nav_table.py` | ~120 | Walk/query/modify navigation tables (H-23/H-24) |
| Schema validator | `src/domain/markdown_ast/schema.py` | ~250 | Jerry markdown schema definitions and validation engine |
| Application handlers | `src/application/markdown_ast/` | ~200 | CQRS commands and queries for AST operations |
| CLI adapter | `src/interface/cli/ast_commands.py` | ~250 | `jerry ast parse|query|transform|render|validate` |
| Skill scripts | `skills/ast/scripts/ast_ops.py` | ~150 | Thin wrapper importing domain layer |
| Skill definition | `skills/ast/SKILL.md` | -- | Skill instructions for Claude |
| Tests | `tests/domain/markdown_ast/` | ~300 | Unit tests (H-21: 90% coverage) |
| **Grand Total** | | **~1,740** | |

**Note on LOC growth from SPIKE-001 estimate:** SPIKE-001 estimated ~470 LOC for extensions only. The SPIKE-002 total of ~1,740 LOC includes: the original ~470 LOC extensions, ~250 LOC schema validation (not in SPIKE-001 scope), ~200 LOC application layer handlers, ~250 LOC CLI adapter, ~150 LOC skill scripts, and ~300 LOC tests. The extension LOC estimate from SPIKE-001 is confirmed; the total implementation LOC is larger because it includes the full architectural integration, not just the domain extensions.

### Dependency Configuration

```toml
# pyproject.toml additions
[project.dependencies]
# ... existing deps ...
markdown-it-py = ">=4.0.0,<5.0.0"
mdformat = ">=1.0.0,<2.0.0"
mdit-py-plugins = ">=0.4.0"
```

Day-1 setup: `uv add "markdown-it-py>=4.0.0,<5.0.0" "mdformat>=1.0.0,<2.0.0" mdit-py-plugins`

---

## L2: Migration Roadmap

### Phase 1: Foundation (Weeks 1-2)

**Objective:** Domain layer + CLI adapter. No existing code changes.

| Task | LOC | Dependencies | Exit Criteria |
|------|:---:|-------------|---------------|
| Implement JerryDocument facade | ~130 | markdown-it-py, mdformat | Parse and render a WORKTRACKER.md file with byte-for-byte fidelity on unmodified regions |
| Implement blockquote frontmatter extraction | ~140 | JerryDocument | Extract all key-value pairs from SPIKE-002 entity frontmatter |
| Implement blockquote frontmatter write-back | ~80 | Frontmatter extraction | Modify Status field, render, verify roundtrip (R-01 validation) |
| Implement L2-REINJECT parser | ~120 | JerryDocument | Parse all L2-REINJECT comments in quality-enforcement.md |
| Implement CLI adapter (parse, render, validate) | ~250 | Domain layer | `jerry ast parse WORKTRACKER.md` produces valid JSON |
| Unit tests for domain layer | ~200 | All domain components | 90% line coverage (H-21) |
| **Phase 1 Total** | **~920** | | R-01 resolved; foundation usable |

**R-01 Gate:** Phase 1 Task 3 (frontmatter write-back) is the R-01 validation. If it fails:
- Try string-level substitution fallback (add ~50 LOC)
- If string fallback fails: switch to mistletoe stack (rewrite ~200 LOC of domain layer)
- Decision point: end of Week 1

### Phase 2: Skill Integration (Week 3)

**Objective:** `/ast` skill operational. /worktracker pilot migration.

| Task | LOC | Dependencies | Exit Criteria |
|------|:---:|-------------|---------------|
| Create `/ast` skill (SKILL.md + scripts) | ~150 | Domain layer | Claude can invoke `/ast` and perform frontmatter operations |
| Migrate /worktracker agents to use AST ops | ~0 (edit existing) | /ast skill | 6 agent files updated; before/after comparison on 10 real files |
| Schema definitions for WORKTRACKER entities | ~100 | Schema validator | `jerry ast validate` catches missing required frontmatter fields |
| **Phase 2 Total** | **~250** | | /worktracker on AST; schema validation live |

### Phase 3: Schema Expansion (Weeks 4-5)

**Objective:** Schema coverage for skill definitions, rule files, templates.

| Task | LOC | Dependencies | Exit Criteria |
|------|:---:|-------------|---------------|
| Schema definitions for skill files | ~50 | Schema validator | Validate SKILL.md files |
| Schema definitions for rule files | ~50 | Schema validator | Validate .context/rules/*.md |
| Nav table validation (H-23/H-24) | ~120 | Nav table helpers | `jerry ast validate --nav` checks all nav tables |
| Migrate /orchestration agents | ~0 (edit existing) | /ast skill | 3 agent files updated |
| Pre-commit hook integration | ~30 | CLI adapter | `jerry ast validate --changed` in pre-commit |
| Additional tests | ~100 | Phase 3 components | 90% coverage maintained |
| **Phase 3 Total** | **~350** | | Schema validation across all schema-heavy file types |

### Phase 4: Remaining Migration (Week 6+)

**Objective:** Remaining skills migrated opportunistically.

| Task | LOC | Dependencies | Exit Criteria |
|------|:---:|-------------|---------------|
| Migrate /adversary agents (read-only AST) | ~0 (edit existing) | /ast skill | 3 agent files updated |
| Migrate /nasa-se agents (template instantiation) | ~0 (edit existing) | /ast skill | 3-4 agent files updated |
| Migrate /problem-solving agents (where beneficial) | ~0 (edit existing) | /ast skill | 2-3 agent files updated |
| Performance validation (50-file batch) | ~0 | CLI adapter | Sub-100ms confirmed |
| **Phase 4 Total** | **~0 new LOC** | | All migrations complete |

### Migration Timeline Summary

| Phase | Weeks | Cumulative LOC | Milestone |
|-------|:-----:|:--------------:|-----------|
| 1: Foundation | 1-2 | ~920 | R-01 resolved; domain layer + CLI usable |
| 2: Skill + Pilot | 3 | ~1,170 | /worktracker on AST; schema validation live |
| 3: Schema Expansion | 4-5 | ~1,520 | All schema-heavy files covered; pre-commit hooks |
| 4: Full Migration | 6+ | ~1,520 | All skills migrated |

---

## FEAT-001 Scope Definition

Based on this SPIKE-002 analysis, FEAT-001 (AST Strategy Evaluation and Library Selection) should be decomposed into the following stories:

| Story | Title | Phase | Priority | Effort |
|-------|-------|:-----:|:--------:|:------:|
| STORY-001 | Implement JerryDocument facade with markdown-it-py + mdformat | 1 | P0 | 5 |
| STORY-002 | Implement blockquote frontmatter extraction and write-back | 1 | P0 | 5 |
| STORY-003 | Implement L2-REINJECT parser and write-back | 1 | P0 | 3 |
| STORY-004 | Add `jerry ast` CLI commands | 1 | P1 | 3 |
| STORY-005 | Create `/ast` Claude skill | 2 | P1 | 3 |
| STORY-006 | Implement schema validation engine | 2-3 | P1 | 5 |
| STORY-007 | Migrate /worktracker agents to AST | 2 | P1 | 3 |
| STORY-008 | Implement navigation table helpers | 3 | P2 | 3 |
| STORY-009 | Add pre-commit validation hook | 3 | P2 | 2 |
| STORY-010 | Migrate remaining skills | 4 | P2 | 5 |

**Total effort estimate:** 37 story points across 10 stories.

---

## Hypothesis Resolution

SPIKE-002 defined 5 hypotheses. Resolution status:

| # | Hypothesis | Verdict | Evidence |
|---|-----------|---------|----------|
| H1 | AST will reduce token consumption by 30-50% | **Partially validated** | 15-30% individual, 40-60% batch. Below hypothesis for individual ops, within range for batch. Primary benefit is correctness, not token savings. (Phase 5, Token Reduction Modeling) |
| H2 | Schema validation will catch 80%+ of structural errors | **Validated** | 5/6 patterns schematizable. 4/6 currently have zero automated detection. >80% improvement. (Phase 5, Schema Validation Capability) |
| H3 | Jerry CLI command provides cleanest architecture | **Partially validated, refined** | CLI alone (Pattern A) is insufficient for Claude. Pattern D (Hybrid: CLI + Skill) is cleanest, preserving hexagonal architecture with dual audience support. (Phase 4, Pattern Analysis) |
| H4 | Hidden Claude-only skills create parallel tooling surface | **Validated** | Pattern B (skill-only) confirmed to create invisible tooling surface. Pattern D resolves by sharing domain layer. (Phase 4, Pattern B weaknesses) |
| H5 | AST is overkill for freeform files | **Validated** | Bounded scope recommendation excludes freeform files. Boundary: 3+ schematizable patterns = in scope. (Phase 5, Feasibility Verdict) |

---

## NO-GO Alternative Strategy

If the AST approach is rejected entirely (R-01 fails AND all fallbacks are insufficient, or the team decides the complexity premium is not justified), the following alternative strategies are available:

### Alternative 1: Enhanced Template System (Recommended NO-GO path)

Replace the AST approach with a structured template + validation system that operates on raw text:

| Aspect | Description |
|--------|-------------|
| Approach | Define Jerry markdown templates as annotated markdown files with `{{placeholder}}` markers. Use regex-based extraction/insertion for frontmatter fields. Add a standalone validation CLI (`jerry validate`) that checks structural patterns without parsing to AST. |
| LOC estimate | ~400-600 LOC (regex extractors + template engine + validator) |
| Advantage | No new library dependency. Simpler to implement and maintain. |
| Disadvantage | No roundtrip fidelity guarantee. Regex-based extraction is fragile to formatting variations. Cannot handle nested or complex structural modifications. |
| When to choose | If R-01 AND all fallbacks fail; if the team values simplicity over correctness guarantees; if the ~1,740 LOC budget is considered excessive. |

### Alternative 2: Structured Data Primary (YAML/JSON)

Migrate schema-heavy files from markdown to structured data formats:

| Aspect | Description |
|--------|-------------|
| Approach | Store WORKTRACKER entities, skill metadata, and rule definitions in YAML or JSON. Generate markdown views for human consumption. Modify structured data directly; re-render markdown as needed. |
| LOC estimate | ~800-1,200 LOC (YAML schemas + markdown renderer + migration scripts) |
| Advantage | Eliminates the markdown roundtrip problem entirely. Structured data is trivially parseable and validatable. |
| Disadvantage | Fundamental architecture change. Breaks Jerry's filesystem-as-memory principle (markdown is human-readable; YAML/JSON is not). Requires migrating all existing files. Claude's markdown generation workflow must change. |
| When to choose | Only if the markdown-first approach is fundamentally unworkable. This is a last-resort architectural pivot, not a lightweight alternative. |

### Alternative 3: Status Quo (Improved Read + Edit)

Continue with the current approach but add targeted improvements:

| Aspect | Description |
|--------|-------------|
| Approach | Add helper prompts to skill definitions that guide Claude on correct markdown patterns. Implement a standalone `jerry validate` command using regex-based checks. Improve Claude's tool usage instructions to reduce edit errors. |
| LOC estimate | ~100-200 LOC (validation script) |
| Advantage | Minimal implementation cost. No new dependencies. No architectural changes. |
| Disadvantage | Does not solve the structural correctness problem. Regex validation catches some errors but cannot enforce complex patterns (nested blockquotes, table structure). Token efficiency does not improve. |
| When to choose | If the cost-benefit analysis of all AST approaches is negative. This is a legitimate baseline: the current approach has been operating for months without documented structural corruption cases, and "working" is a strong baseline. The case against status quo is that silent errors are by definition undocumented -- the absence of evidence is not evidence of absence. However, if empirical testing of current error rates shows them to be acceptably low, this option avoids all AST complexity. |

---

## GO/NO-GO Sensitivity Analysis

Testing the robustness of the GO decision under altered assumptions:

| Test | Condition Changed | Decision Impact |
|------|-------------------|-----------------|
| **SA-1:** R-01 fails (mdformat write-back impossible) | String fallback viable | GO maintained (reduced elegance). Pattern D architecture unchanged; domain layer uses string substitution instead of token reconstruction. |
| **SA-2:** R-01 fails AND string fallback fails | Switch to mistletoe | GO maintained (different library). ~200 LOC domain rewrite. Timeline extends 1 week. |
| **SA-3:** R-01 fails AND mistletoe fails AND hybrid fails | No viable library approach | **FLIPS TO NO-GO.** Pursue Alternative 1 (Enhanced Template System). |
| **SA-4:** Token savings are 0% (no improvement over status quo) | Primary benefit must carry alone | GO maintained. Schema validation and batch operations justify adoption even with zero token savings. |
| **SA-5:** LOC estimate doubles (~3,500 LOC actual) | Implementation cost exceeds budget | **Conditional.** If 2x is due to edge cases in extensions (likely), GO maintained with extended timeline. If 2x is due to fundamental API mismatch (unlikely), re-evaluate at Phase 1 gate. |
| **SA-6:** Claude tool efficiency improves 50% in next model | Token savings become irrelevant | GO maintained. Correctness benefits are model-independent. |
| **SA-7:** Jerry abandons hexagonal architecture | Pattern D loses primary justification | **FLIPS TO NO-GO for Pattern D.** Reconsider Pattern B (skill-only) or Pattern C (MCP). Domain layer remains valid regardless. |

**Sensitivity conclusion:** The GO decision survives 5 of 7 perturbation tests. It flips to NO-GO only under SA-3 (all library approaches fail -- very low probability given 3 viable candidates) or SA-7 (architectural abandonment -- external decision, not an AST risk). The decision is robust.

---

## R-01 Decision Tree

Explicit thresholds and escalation paths for the critical R-01 risk:

```
R-01: Blockquote frontmatter write-back validation
======================================================

PROOF-OF-CONCEPT (Phase 1, Week 1, Days 1-3):
  Test: Parse SPIKE-002-feasibility.md
        Modify Status: pending -> in_progress
        Render back with mdformat
        Compare output

  CHECK 1: Does the modified field render correctly?
  ├── YES -> CHECK 2
  └── NO  -> ESCALATE to Fallback A

  CHECK 2: Are unmodified regions byte-for-byte identical?
  ├── YES -> CHECK 3
  └── NO  -> Assess: is the diff acceptable normalization?
             ├── YES (whitespace only) -> CHECK 3 (with normalization caveat)
             └── NO  (semantic change) -> ESCALATE to Fallback A

  CHECK 3: Does mdformat HTML-equality verification pass?
  ├── YES -> R-01 RESOLVED: Proceed with standard implementation
  └── NO  -> ESCALATE to Fallback A

FALLBACK A: String-level substitution (Days 3-4)
  Implementation: ~50 LOC regex-based field substitution
  Same checks (1, 2, 3) applied
  ├── All pass -> R-01 RESOLVED with fallback
  └── Any fail -> ESCALATE to Fallback B

FALLBACK B: Mistletoe stack (Days 4-5)
  Implementation: ~200 LOC domain layer rewrite
  Same checks (1, 2, 3) applied
  ├── All pass -> R-01 RESOLVED with library switch
  └── Any fail -> ESCALATE to Fallback C

FALLBACK C: Hybrid renderer (Week 2)
  Implementation: ~400 LOC custom renderer for modified sections
  ├── Pass -> R-01 RESOLVED with hybrid approach
  └── Fail -> DECISION: NO-GO for AST. Pursue Alternative 1.

TIMELINE GATE: If R-01 is not resolved by end of Week 2,
               STOP and pursue NO-GO Alternative 1.
```

---

## Conditions and Assumptions

### Conditions (must remain true)

| ID | Condition | Validation Method | Failure Action |
|----|-----------|-------------------|----------------|
| C-01 | R-01: mdformat write-back supports blockquote frontmatter | Proof-of-concept in Phase 1, Week 1 | String fallback -> mistletoe -> hybrid (escalation ladder) |
| C-02 | markdown-it-py v4.x SyntaxTreeNode API remains stable | Monitor upstream changelog | Pin to last known good version |
| C-03 | mdformat normalization is acceptable for Jerry documents | Corpus test in Phase 1 | Adopt diff-based validation or normalize corpus |
| C-04 | ~720 LOC domain estimate is within 2x of actual (~1,740 LOC total within 2x) | Validated during Phase 1 implementation | Re-scope if domain >1,500 LOC or total >3,500 LOC |

### Key Assumptions

| ID | Assumption | Risk if Wrong |
|----|-----------|---------------|
| A-01 | Jerry's markdown dialect will not require more than 4 custom extensions in the next 12 months | Additional extension development; manageable within the architecture |
| A-02 | Claude Code skill loading continues to work as documented | Skill-based interface may need redesign; CLI remains functional |
| A-03 | The hexagonal architecture pattern is maintained in Jerry | If abandoned, the adapter separation loses its primary justification |
| A-04 | Token efficiency improvement is secondary to correctness improvement | If token efficiency is the primary driver, MCP server (Pattern C) should be reconsidered |

---

## Decision Record

| Field | Value |
|-------|-------|
| **Decision** | GO -- adopt AST-first architecture with bounded scope |
| **Confidence** | Medium-High (0.75); rises to ~0.90 if R-01 resolves favorably |
| **Integration Pattern** | Pattern D: Hybrid (CLI + Skill with shared domain layer). Rejected: A (poor Claude DX), B (invisible to humans, partial architecture fit), C (operational complexity disproportionate to scope). See Phase 4 L2 Comparative Assessment. |
| **Library Stack** | markdown-it-py v4.0.0 + mdformat v1.0.0 + mdit-py-plugins |
| **Scope** | Schema-heavy files (WORKTRACKER, skills, rules, templates, orchestration state) |
| **Exclusion** | Freeform files (research notes, ADR prose, experience reports) |
| **Total LOC** | ~1,740 (domain: ~840, adapters: ~400, tests: ~300, application: ~200) |
| **Timeline** | 6 weeks to full migration; 2 weeks to usable foundation |
| **Critical Gate** | R-01 proof-of-concept (Phase 1, Week 1) |
| **Fallback** | String substitution fallback -> mistletoe switch -> hybrid renderer (escalation ladder) |
| **Primary Benefit** | Structural correctness (schema validation, targeted modification, roundtrip fidelity) |
| **Secondary Benefit** | Token efficiency (15-30% individual, 40-60% batch) |
| **FEAT-001 Stories** | 10 stories, 37 story points |
| **Next Step** | Proof-of-concept: parse WORKTRACKER entity, modify Status field, render back, verify roundtrip |

---

## Evidence Traceability

### Claims from Phase 4 (Integration Patterns Research)

| Claim | Phase 4 Section |
|-------|-----------------|
| Pattern D (Hybrid) is recommended integration pattern | L2: Comparative Assessment > Recommendation |
| Pattern A token efficiency is poor (stdout parsing overhead) | L1: Pattern Analysis > Pattern A > Token Efficiency |
| Pattern B creates invisible tooling surface | L1: Pattern Analysis > Pattern B > Weaknesses (items 1, 2) |
| Pattern C requires MCP server lifecycle management | L1: Pattern Analysis > Pattern C > Weaknesses (items 1, 2) |
| Pattern D aligns with hexagonal architecture | L1: Pattern Analysis > Pattern D > Architecture fit |
| Token savings 15-30% individual, 40-60% batch | L2: Comparative Assessment > Token Efficiency Deep Dive |
| Migration effort: ~20 files, 6 skills | L2: Comparative Assessment > Migration Path Analysis |
| Gradual migration possible (no big-bang) | L2: Comparative Assessment > Migration strategy |
| Microsoft MarkItDown as CLI+MCP precedent | L1: Pattern Analysis > Pattern A > Real-world precedent |

### Claims from Phase 5 (Feasibility Analysis)

| Claim | Phase 5 Section |
|-------|-----------------|
| Token reduction 15-30% individual operations | L1: Feasibility Dimensions > Section 1 > Token Reduction Modeling |
| Token reduction 40-60% batch operations | L1: Feasibility Dimensions > Section 1 > Token Reduction Modeling |
| 5/6 structural patterns schematizable | L1: Feasibility Dimensions > Section 2 > Schema Validation Capability |
| 4/6 patterns have zero current automated detection | L1: Feasibility Dimensions > Section 2 > Schema Validation Capability |
| Schema validation ~250 LOC additive | L1: Feasibility Dimensions > Section 2 > Schema implementation approach |
| Migration: ~20 files, 4-6 weeks, incremental | L1: Feasibility Dimensions > Section 3 > Migration Effort |
| /worktracker as pilot (highest value, lowest risk) | L1: Feasibility Dimensions > Section 3 > Migration Effort |
| No failure mode worse than status quo (S-013) | L2: Adversarial Analysis > S-013 Inversion > Inversion conclusion |
| Most plausible failure: schema maintenance burden (S-004) | L2: Adversarial Analysis > S-004 Pre-Mortem > PM-3 |
| Bounded scope: schema-heavy files only | Feasibility Verdict |

### Claims from SPIKE-001 Handoff

| Claim | Handoff Section |
|-------|-----------------|
| markdown-it-py v4.0.0 + mdformat v1.0.0 (composite: 4.20) | Top-Ranked Library |
| ~470 LOC extensions (4 extensions) | Extension Requirements |
| Build-from-scratch not recommended (5-7x cost) | Build-from-Scratch Assessment |
| R-01: mdformat write-back uncertainty (Medium likelihood, High impact) | Critical Risk R-01 |
| Fallback: mistletoe v1.5.1 (composite: 3.75) | Top-Ranked Library |
| 6 SPIKE-002 investigation priorities | SPIKE-002 Investigation Priorities |

---

## References

| Source | Content | Location |
|--------|---------|----------|
| Phase 4 Research | Integration patterns analysis, Pattern D recommendation | `ps/phase-4-arch-research/ps-researcher-002/integration-patterns-research.md` |
| Phase 5 Analysis | Feasibility dimensions, S-013/S-004 results | `ps/phase-5-feasibility/ps-analyst-002/feasibility-analysis.md` |
| SPIKE-001 Handoff | Library recommendation, extension requirements, R-01 risk | `cross-pollination/barrier-1/spike-001-handoff.md` |
| SPIKE-001 Synthesis | Full ranked recommendation (QG1 PASS at 0.96) | `ps/phase-3-synthesis/ps-synthesizer-001/library-recommendation.md` |
| SPIKE-002 Entity | Research question, hypotheses H1-H5 | `work/EPIC-001-markdown-ast/FEAT-001-ast-strategy/SPIKE-002-feasibility/SPIKE-002-feasibility.md` |
| Jerry CLI | Current hexagonal architecture | `src/interface/cli/main.py` |
| quality-enforcement.md | Quality gate thresholds, strategy catalog | `.context/rules/quality-enforcement.md` |

---

*Phase 6 Decision Synthesis. ps-synthesizer-002. spike-eval-20260219-001.*
