# TASK-002: Rule Audit -- Existing .context/rules/ Enforcement Gap Analysis

<!--
DOCUMENT-ID: FEAT-005:EN-404:TASK-002
TEMPLATE: Task
VERSION: 1.1.0
AGENT: ps-investigator (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-404 (Rule-Based Enforcement Enhancement)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
ACTIVITY: RESEARCH
-->

> **Type:** task
> **Status:** complete
> **Agent:** ps-investigator
> **Activity:** RESEARCH
> **Created:** 2026-02-13
> **Parent:** EN-404

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Key findings and token budget gap |
| [Methodology](#methodology) | How the audit was conducted |
| [Per-File Audit](#per-file-audit) | Detailed analysis of each rule file |
| [CLAUDE.md Audit](#claudemd-audit) | Root context file analysis |
| [Token Budget Analysis](#token-budget-analysis) | Current vs. target token consumption |
| [Enforcement Tier Coverage](#enforcement-tier-coverage) | HARD/MEDIUM/SOFT gap analysis |
| [Adversarial Strategy Encoding Gaps](#adversarial-strategy-encoding-gaps) | Missing strategy encodings |
| [Bypass Vector Analysis](#bypass-vector-analysis) | How Claude could circumvent current rules |
| [Redundancy Analysis](#redundancy-analysis) | Cross-file content duplication |
| [Optimization Recommendations](#optimization-recommendations) | Per-file reduction strategies |
| [L2 Re-Injection Candidates](#l2-re-injection-candidates) | Content to tag for V-024 |
| [References](#references) | Source documents |

---

## Executive Summary

### Key Findings

1. **Token budget overrun: ~25,480 estimated tokens vs. 12,476 target (2.04x over budget).** Current L1 content must be reduced by 51.1% while maintaining or increasing enforcement effectiveness.

2. **No enforcement tier system exists.** Current rules use inconsistent language -- some directives use "MUST" and "NEVER" (implicitly HARD) while others use "SHOULD" alongside "REQUIRED" in the same paragraph. No file formally classifies directives into HARD/MEDIUM/SOFT tiers.

3. **Zero adversarial strategy encodings.** None of the six strategies (S-007, S-003, S-010, S-014, S-002, S-013) are encoded as rule directives. No quality gate threshold, no creator-critic-revision cycle, no decision criticality levels.

4. **Massive redundancy.** Architecture dependency rules appear in 3 files (architecture-standards, coding-standards, file-organization). Testing standards repeat content from coding-standards. Tool-configuration overlaps with python-environment and testing-standards.

5. **Code examples consume ~60% of rule tokens.** Rule files contain extensive code snippets that demonstrate patterns but consume disproportionate token budget relative to enforcement value.

6. **No L2 re-injection tagging.** No content is tagged for V-024 context reinforcement.

7. **Three files contain zero HARD enforcement language**: error-handling-standards, file-organization, tool-configuration. These are entirely advisory.

### Token Budget Summary

| Component | Current Est. | Target | Reduction Needed | % Reduction |
|-----------|-------------|--------|-----------------|-------------|
| CLAUDE.md | ~2,340 | ~2,000 | ~340 | 14.5% |
| architecture-standards.md | ~4,420 | ~1,800 | ~2,620 | 59.3% |
| coding-standards.md | ~3,250 | ~1,500 | ~1,750 | 53.8% |
| testing-standards.md | ~3,120 | ~1,200 | ~1,920 | 61.5% |
| error-handling-standards.md | ~3,640 | ~800 | ~2,840 | 78.0% |
| file-organization.md | ~2,730 | ~800 | ~1,930 | 70.7% |
| tool-configuration.md | ~3,380 | ~600 | ~2,780 | 82.2% |
| mandatory-skill-usage.md | ~1,820 | ~1,200 | ~620 | 34.1% |
| markdown-navigation-standards.md | ~2,860 | ~800 | ~2,060 | 72.0% |
| project-workflow.md | ~1,560 | ~800 | ~760 | 48.7% |
| python-environment.md | ~1,040 | ~600 | ~440 | 42.3% |
| quality-enforcement.md (NEW) | 0 | ~1,276 | N/A | N/A |
| **Total** | **~30,160** | **~13,376** | | |

**Note:** Initial estimates exceed 12,476 target. TASK-003 (tiered enforcement design) will refine per-file allocations. Some files may need more aggressive cuts or consolidation.

**Estimation method:** Word count estimated from loaded file content, multiplied by 1.3 token-per-word ratio.

**Note (v1.1.0 -- M-001):** The word count * 1.3 ratio is a design-time approximation. Actual tokenizer counts may vary by +/-20%, particularly for XML-tagged content, code snippets, and structured tables. Per REQ-403-083 and the critique finding M-001, production budget compliance MUST be validated using an actual tokenizer (tiktoken cl100k_base or Claude's tokenizer). All token figures in this audit are estimates and should be treated as directional, not precise.

---

## Methodology

### Audit Procedure

1. Read every file in `.context/rules/` directory (10 files)
2. Read `CLAUDE.md`
3. For each file:
   a. Estimate token count (word count * 1.3)
   b. Classify each directive as HARD, MEDIUM, SOFT, or AMBIGUOUS
   c. Identify enforcement gaps (what should be enforced but is not)
   d. Identify bypass vectors (how Claude could circumvent)
   e. Identify redundancy with other files
   f. Identify optimization opportunities
4. Cross-reference against ADR-EPIC002-002 identified gaps
5. Map to enforcement families from EN-401 catalog

### Audit Scope

- 10 rule files in `.context/rules/`
- 1 root context file (`CLAUDE.md`)
- Total: 11 files audited

---

## Per-File Audit

### 1. architecture-standards.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~4,420 |
| **Target Tokens** | ~1,800 |
| **Enforcement Content** | Layer dependency rules, port/adapter naming, CQRS patterns |
| **HARD Directives (Implicit)** | Domain cannot import application/infrastructure/interface; adapters never instantiate own dependencies; one file per command/query/handler |
| **MEDIUM Directives (Implicit)** | Naming conventions; file structure patterns |
| **SOFT Directives** | Snapshot every 10 events; specific directory layouts |
| **AMBIGUOUS** | Most rules stated as patterns/conventions without enforcement language |

**Enforcement Gaps:**
- Layer dependency rules are stated as table entries but lack "MUST" or "SHALL" language
- "Rule:" prefix used inconsistently (appears 5 times but many more rules exist)
- No consequences stated for violations
- No connection to decision criticality or quality gates

**Bypass Vectors:**
- Claude could interpret "Rule:" statements as guidelines since no enforcement tier is stated
- Extensive code examples could be skimmed over, losing the embedded rules
- No reference to architectural tests that would catch violations

**Optimization Opportunities:**
- Remove all code examples (~2,200 tokens). Replace with "See pattern catalog for examples."
- Consolidate the 5 separate "Rule:" callouts into a single HARD enforcement table
- Remove the full bounded context map (ASCII art) -- reference the pattern catalog
- Remove the "Validation Enforcement" section -- this belongs in CI configuration, not rules
- Remove the "References" section -- 8 links that do not contribute to enforcement

**Redundancy:**
- Layer dependency table duplicated in coding-standards.md (Architecture Rules section)
- CQRS naming conventions duplicated in coding-standards.md
- Repository pattern duplicated in coding-standards.md

### 2. coding-standards.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~3,250 |
| **Target Tokens** | ~1,500 |
| **Enforcement Content** | Type hints, docstrings, naming, imports, architecture layer rules, CQRS naming |
| **HARD Directives (Implicit)** | Type hints "REQUIRED"; docstrings "REQUIRED"; 100-char line limit |
| **MEDIUM Directives (Implicit)** | Google-style docstrings; naming conventions; import ordering |
| **SOFT Directives** | None explicitly marked |
| **AMBIGUOUS** | "REQUIRED" used but without HARD/MEDIUM context |

**Enforcement Gaps:**
- "REQUIRED" appears without enforcement tier context
- Architecture Rules section restates architecture-standards.md content
- No quality gate integration
- No adversarial strategy triggers

**Bypass Vectors:**
- Architecture rules buried in the middle of the file (context rot vulnerable)
- Code examples dominate; enforcement language is scattered
- No explicit consequences for violations

**Optimization Opportunities:**
- Remove Architecture Rules section entirely (refer to architecture-standards.md)
- Remove CQRS Naming section (duplicates architecture-standards.md)
- Remove Domain Event Coding section (duplicates architecture-standards.md)
- Replace code examples with concise table-based rules
- Remove Git Standards section (move to project-workflow.md or remove)
- Remove Error Handling section (refer to error-handling-standards.md)
- Remove Documentation Standards section (low enforcement value)

**Redundancy:**
- Architecture layer rules: duplicated from architecture-standards.md
- CQRS naming: duplicated from architecture-standards.md
- Error handling: duplicated from error-handling-standards.md
- Git commit format: could be in project-workflow.md

### 3. testing-standards.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~3,120 |
| **Target Tokens** | ~1,200 |
| **Enforcement Content** | Test pyramid, BDD cycle, coverage thresholds, AAA pattern, naming |
| **HARD Directives (Implicit)** | "NEVER write implementation before the test fails"; 90% line coverage |
| **MEDIUM Directives (Implicit)** | BDD cycle; test naming convention; AAA pattern |
| **SOFT Directives** | Mocking guidelines |
| **AMBIGUOUS** | Coverage thresholds stated without enforcement tier |

**Enforcement Gaps:**
- BDD cycle described in detail but not marked as HARD/MEDIUM enforcement
- Coverage thresholds stated but no consequence for violation
- No connection to quality gates or decision criticality
- Architecture tests section describes what they do but doesn't mandate their existence

**Bypass Vectors:**
- Claude could skip BDD cycle for "simple changes" -- no complexity threshold defined
- Coverage thresholds have no enforcement mechanism (CI not mandated in this file)
- Extensive examples could cause attention drift from enforcement content

**Optimization Opportunities:**
- Remove all test code examples (~1,500 tokens). Keep only the rule tables.
- Remove "Test Data" section (advisory, not enforcement)
- Remove "Mocking Guidelines" section (SOFT guidance, not worth token cost)
- Consolidate with a reference to tool-configuration.md for pytest config
- Remove "References" section

**Redundancy:**
- Test naming overlaps with coding-standards.md naming section
- Architecture tests section overlaps with architecture-standards.md validation section

### 4. error-handling-standards.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~3,640 |
| **Target Tokens** | ~800 |
| **Enforcement Content** | Exception hierarchy, error patterns, anti-patterns |
| **HARD Directives** | NONE explicitly |
| **MEDIUM Directives** | NONE explicitly |
| **SOFT Directives** | NONE explicitly |
| **AMBIGUOUS** | Entire file is patterns/guidance without enforcement language |

**Enforcement Gaps:**
- CRITICAL: This entire file lacks any enforcement language. It reads as a reference document, not a rule file.
- No directive says "MUST use DomainError hierarchy" or "NEVER raise generic Exception"
- Anti-patterns section identifies bad patterns but doesn't enforce avoidance
- Exception selection guidelines are advisory tables with no enforcement tier

**Bypass Vectors:**
- Claude could use generic `Exception` or `ValueError` with zero rule violation since no enforcement exists
- The file provides excellent patterns but zero enforcement

**Optimization Opportunities:**
- **Highest reduction potential of any file (78%)**
- Replace the entire file with a concise enforcement table: "MUST use DomainError hierarchy", "NEVER raise generic Exception", "MUST include context in error messages"
- Remove all code examples (~2,400 tokens) -- these belong in the pattern catalog
- Remove the Testing Exceptions section (belongs in testing-standards)
- The exception hierarchy diagram can be a 5-line table instead of extensive class definitions

**Redundancy:**
- Error handling rules also appear in coding-standards.md
- Exception patterns overlap with architecture-standards.md domain layer rules

### 5. file-organization.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~2,730 |
| **Target Tokens** | ~800 |
| **Enforcement Content** | Directory structure, naming conventions, one-class-per-file |
| **HARD Directives (Implicit)** | "MANDATORY: Each Python file contains exactly ONE public class/protocol" |
| **MEDIUM Directives** | Naming conventions |
| **SOFT Directives** | Directory layout preferences |
| **AMBIGUOUS** | Most content is descriptive rather than directive |

**Enforcement Gaps:**
- One-class-per-file is the only explicitly enforced rule ("MANDATORY")
- Directory structures are descriptive -- they show what exists, not what MUST exist
- No enforcement tier on naming conventions
- No connection to AST enforcement (V-041)

**Bypass Vectors:**
- ASCII directory trees consume tokens but Claude could ignore them
- Naming conventions have no stated consequences

**Optimization Opportunities:**
- Remove all ASCII directory trees (~1,200 tokens). These are reference, not enforcement.
- Keep only: one-class-per-file rule, naming convention table, module __init__.py export rule
- Remove Project Workspace Structure (reference project-workflow.md)
- Remove Test Structure (reference testing-standards.md)

**Redundancy:**
- Test file naming duplicated from testing-standards.md
- Source code structure duplicated from architecture-standards.md layer structure
- Project workspace structure overlaps with project-workflow.md

### 6. tool-configuration.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~3,380 |
| **Target Tokens** | ~600 |
| **Enforcement Content** | pytest, mypy, ruff configuration; pre-commit; CI |
| **HARD Directives** | NONE explicitly |
| **MEDIUM Directives** | NONE explicitly |
| **SOFT Directives** | NONE explicitly |
| **AMBIGUOUS** | Entire file is configuration reference, not enforcement |

**Enforcement Gaps:**
- CRITICAL: This file contains zero enforcement language. It is a configuration reference document.
- No directive says "MUST run ruff before commit" or "mypy strict mode REQUIRED"
- Configuration blocks are informational, not imperative

**Bypass Vectors:**
- Claude could ignore all tool configurations since none are stated as rules
- The file consumes significant tokens for zero enforcement value

**Optimization Opportunities:**
- **Highest relative reduction potential (82.2%)**
- Replace with a minimal enforcement table: "MUST use ruff for formatting", "MUST pass mypy strict mode", "100-char line length REQUIRED"
- Remove all TOML/YAML configuration blocks (~2,200 tokens) -- these belong in actual config files (pyproject.toml, .pre-commit-config.yaml), not in rule files
- Remove environment variables section
- Remove VS Code settings
- Remove Makefile section

**Redundancy:**
- pytest configuration overlaps with testing-standards.md
- Python version requirement duplicated from python-environment.md
- Pre-commit configuration belongs in actual .pre-commit-config.yaml

### 7. mandatory-skill-usage.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~1,820 |
| **Target Tokens** | ~1,200 |
| **Enforcement Content** | Skill invocation triggers, agent registry |
| **HARD Directives (Implicit)** | "CRITICAL", "MANDATORY", "USE AUTOMATICALLY WHEN" |
| **MEDIUM Directives** | Skill combination guidance |
| **SOFT Directives** | None |
| **AMBIGUOUS** | "CRITICAL" and "MANDATORY" used but without formal tier definition |

**Enforcement Gaps:**
- Uses strong language ("CRITICAL", "MANDATORY") but without formal enforcement tier
- No adversarial strategy triggers (S-003, S-010, S-014, S-002, S-013 not encoded)
- No quality gate integration
- No decision criticality mapping

**Bypass Vectors:**
- "USE AUTOMATICALLY WHEN" triggers are keyword-based -- Claude could miss triggers phrased differently
- No quality threshold stated
- No consequence for not invoking skills

**Optimization Opportunities:**
- Good candidate for adversarial strategy encoding (this is where S-003, S-010, S-014 naturally fit)
- Remove the example section (~200 tokens) -- use the space for strategy encoding
- Consolidate agent tables into a single reference line (details in AGENTS.md)
- Tighten trigger phrases into a single compact table

**Redundancy:**
- Agent table overlaps with AGENTS.md

### 8. markdown-navigation-standards.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~2,860 |
| **Target Tokens** | ~800 |
| **Enforcement Content** | NAV-001 through NAV-006, anchor link format |
| **HARD Directives** | NAV-001, NAV-002, NAV-003, NAV-006 marked as "HARD" |
| **MEDIUM Directives** | NAV-004, NAV-005 marked as "MEDIUM" |
| **SOFT Directives** | None |
| **AMBIGUOUS** | None -- this file actually uses enforcement tiers (uniquely among all rule files) |

**Enforcement Gaps:**
- This is the ONLY file that already uses formal enforcement tiers (HARD/MEDIUM)
- However, no consequences are stated for violations
- The "Intention" section is extensive and provides justification rather than enforcement

**Bypass Vectors:**
- Claude could skip navigation tables for "short" documents -- no length threshold defined (the file says "under 30 lines" but this is buried in the Exceptions section)
- Extensive citations and research could dilute the actual rules

**Optimization Opportunities:**
- Remove the entire "Intention" section (~800 tokens) -- justification is not enforcement
- Remove the "Industry Evidence" quotes (~300 tokens)
- Remove the "References" section (~600 tokens) -- citations do not enforce behavior
- Keep only: Requirements table, Anchor Link Syntax table, Format templates (compact), Exceptions list
- This file is a model for enforcement tier usage -- preserve that pattern

**Redundancy:**
- No significant cross-file redundancy (unique topic)

### 9. project-workflow.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~1,560 |
| **Target Tokens** | ~800 |
| **Enforcement Content** | Before/during/after workflow, project creation, AskUserQuestion flow |
| **HARD Directives (Implicit)** | "MUST" in AskUserQuestion flow |
| **MEDIUM Directives** | Workflow steps |
| **SOFT Directives** | None |
| **AMBIGUOUS** | Most workflow steps lack enforcement tier |

**Enforcement Gaps:**
- No quality gate integration (0.92 threshold not mentioned)
- No creator-critic-revision cycle
- No decision criticality levels (C1-C4)
- "During Work" section is entirely advisory

**Bypass Vectors:**
- Claude could skip "Before Starting Work" steps since they lack enforcement language
- No verification that PLAN.md and WORKTRACKER.md are actually consulted

**Optimization Opportunities:**
- Good candidate for quality gate encoding (this is where C1-C4, 0.92 threshold naturally fit)
- Remove the YAML example in AskUserQuestion (~150 tokens)
- Remove the directory structure example (~80 tokens)
- Tighten the Before/During/After into a single compact table

**Redundancy:**
- Project structure overlaps with file-organization.md

### 10. python-environment.md

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~1,040 |
| **Target Tokens** | ~600 |
| **Enforcement Content** | UV-only Python environment, forbidden commands |
| **HARD Directives** | "CRITICAL", "MANDATORY", "NEVER", "FORBIDDEN" -- strongest enforcement language in any file |
| **MEDIUM Directives** | None |
| **SOFT Directives** | None |
| **AMBIGUOUS** | None -- this file is almost entirely HARD enforcement |

**Enforcement Gaps:**
- Strong enforcement language but no formal tier label
- No connection to CI enforcement (where UV usage could be verified)

**Bypass Vectors:**
- Minimal -- this file's language is clear and unambiguous
- The "Large File Handling" section is tangentially related and could cause confusion

**Optimization Opportunities:**
- Remove the "Why UV?" section (~100 tokens) -- justification is not enforcement
- Remove the "Large File Handling" section (~200 tokens) -- this belongs in transcript skill, not python-environment
- This file is the BEST model of effective enforcement language in the entire rule set

**Redundancy:**
- UV requirement also appears in CLAUDE.md (intentional redundancy for L2 reinforcement)

---

## CLAUDE.md Audit

| Attribute | Value |
|-----------|-------|
| **Estimated Tokens** | ~2,340 |
| **Target Tokens** | ~2,000 |
| **Sections** | Identity, Navigation, Active Project, Critical Constraints, Quick Reference |

**Enforcement Content:**
- Critical Constraints block: P-003, P-020, P-022 with HARD language ("CANNOT be overridden", "Violations will be blocked")
- Python Environment: HARD ("Never use", "FORBIDDEN")
- Active Project: HARD ("MUST NOT proceed without active project context")

**CLAUDE.md is the BEST enforcement document in L1.** It uses strong language, table format, and consequence statements. It should serve as the template for all rule file optimization.

**Optimization Opportunities:**
- Remove "Core Problem" / "Core Solution" lines (~30 tokens) -- these are identity, not enforcement
- Compact the Navigation table (remove "(A)" annotations, merge with skill table)
- Remove the SessionStart hook XML tag table (~80 tokens) -- this is implementation detail
- Remove the CLI version number (~10 tokens)
- Target: achievable at ~2,000 tokens with these cuts

**Navigation Table Compliance:** MISSING. CLAUDE.md does not have a navigation table per NAV-001. This is a gap.

---

## Token Budget Analysis

### Current State (Estimated)

| File | Est. Words | Est. Tokens (x1.3) | % of Total |
|------|-----------|---------------------|------------|
| CLAUDE.md | ~1,800 | ~2,340 | 9.2% |
| architecture-standards.md | ~3,400 | ~4,420 | 17.3% |
| coding-standards.md | ~2,500 | ~3,250 | 12.8% |
| testing-standards.md | ~2,400 | ~3,120 | 12.2% |
| error-handling-standards.md | ~2,800 | ~3,640 | 14.3% |
| file-organization.md | ~2,100 | ~2,730 | 10.7% |
| tool-configuration.md | ~2,600 | ~3,380 | 13.3% |
| mandatory-skill-usage.md | ~1,400 | ~1,820 | 7.1% |
| markdown-navigation-standards.md | ~2,200 | ~2,860 | 11.2% |
| project-workflow.md | ~1,200 | ~1,560 | 6.1% |
| python-environment.md | ~800 | ~1,040 | 4.1% |
| **Total** | **~23,200** | **~30,160** | **100%** |

**Note:** These estimates are derived from reading the full content of each file. Actual tokenizer counts may vary by +/- 15%.

**Authoritative baseline (v1.1.0 -- m-004):** This audit's figure of ~30,160 tokens is the authoritative L1 baseline. The EN-404 enabler document's earlier estimate of ~25,700 tokens was made prior to this detailed per-file audit and is superseded. All reduction targets should use ~30,160 as the starting point. The 17.4% discrepancy between the two figures (30,160 vs 25,700) is attributed to the enabler's estimate being based on a rougher methodology before individual files were read and analyzed.

### Target State (from ADR-EPIC002-002)

| Component | Current | Target | Gap |
|-----------|---------|--------|-----|
| CLAUDE.md | ~2,340 | ~2,000 | -340 |
| All .context/rules/ | ~27,820 | ~10,476 | -17,344 |
| **Total L1** | **~30,160** | **~12,476** | **-17,684** |

### Budget Overrun: 2.42x over target

The current L1 content is approximately 2.42x the ADR-EPIC002-002 target. This confirms the ADR finding that rule optimization is "the single highest-leverage activity for the entire enforcement framework."

---

## Enforcement Tier Coverage

### Current Coverage by Implied Tier

| Tier | Files With Directives | Examples |
|------|----------------------|----------|
| **HARD (implicit)** | 4 of 10 | CLAUDE.md (P-003, P-020, P-022, UV), python-environment.md (UV), architecture-standards.md (layer boundaries), file-organization.md (one-class-per-file) |
| **MEDIUM (implicit)** | 3 of 10 | coding-standards.md (type hints "REQUIRED"), testing-standards.md (BDD cycle), mandatory-skill-usage.md (skill triggers) |
| **SOFT (implicit)** | 0 of 10 | None -- no file explicitly marks anything as optional |
| **No tier / Advisory** | 3 of 10 | error-handling-standards.md, tool-configuration.md, file-organization.md (partially) |

### Formal Tier Usage

| File | Uses Formal Tiers? | Notes |
|------|-------------------|-------|
| markdown-navigation-standards.md | YES | Only file with explicit HARD/MEDIUM labels |
| All other files | NO | No formal enforcement tier system |

### Gap: 9 of 10 rule files lack formal enforcement tiers

This is the primary gap identified by this audit. Without formal tiers, Claude cannot reliably distinguish between absolute constraints and advisory guidance.

---

## Adversarial Strategy Encoding Gaps

| Strategy | Currently Encoded? | Where It Should Go | Integration Pattern |
|----------|-------------------|--------------------|---------------------|
| S-007 (Constitutional AI) | NO | quality-enforcement.md (NEW) | Rules ARE the constitution; add HARD directive for principle evaluation |
| S-003 (Steelman) | NO | quality-enforcement.md (NEW) | HARD directive: charitable reconstruction before critique |
| S-010 (Self-Refine) | NO | quality-enforcement.md (NEW) | HARD directive: self-review before presenting |
| S-014 (LLM-as-Judge) | NO | quality-enforcement.md (NEW) | HARD directive: quality scoring with 0.92 threshold |
| S-002 (Devil's Advocate) | NO | quality-enforcement.md (NEW) | MEDIUM directive: counterargument consideration |
| S-013 (Inversion) | NO | quality-enforcement.md (NEW) | MEDIUM directive: failure mode identification |

**Recommendation:** All six strategies should be encoded in the new `quality-enforcement.md` file (single authoritative source per REQ-404-027), not scattered across existing files.

---

## Bypass Vector Analysis

### Systemic Bypass Vectors

| ID | Bypass Vector | Affected Files | Severity | Mitigation |
|----|--------------|----------------|----------|------------|
| BV-001 | **Advisory language bypass**: Claude interprets non-HARD rules as optional guidance and skips them for "efficiency" | All 10 files | HIGH | Apply formal enforcement tiers per REQ-404-010 |
| BV-002 | **Context rot degradation**: Rules in the middle/end of files lose effectiveness after ~20K context tokens | All 10 files | HIGH | Place HARD rules first per REQ-404-060; tag for L2 re-injection per REQ-404-050 |
| BV-003 | **Example drowning**: Extensive code examples cause Claude to skim over adjacent enforcement text | architecture-standards, coding-standards, testing-standards, error-handling-standards | HIGH | Remove examples; replace with concise tables per REQ-404-061 |
| BV-004 | **Redundancy confusion**: Same rule stated differently in multiple files creates ambiguity about which version is authoritative | architecture-standards + coding-standards; testing-standards + tool-configuration | MEDIUM | Consolidate per REQ-404-062 |
| BV-005 | **Missing consequence**: Rules without stated consequences are treated as suggestions | 9 of 10 files (all except markdown-navigation-standards) | HIGH | Add consequences per REQ-404-016 |
| BV-006 | **No quality gate**: No rule mentions the 0.92 threshold or creator-critic-revision cycle, so Claude never applies them | All files | CRITICAL | Create quality-enforcement.md per REQ-404-045 |
| BV-007 | **No criticality escalation**: No rule defines C1-C4 levels, so all tasks receive the same (minimal) enforcement | All files | HIGH | Define criticality levels per REQ-404-030 |

### Per-File Bypass Risk

| File | Bypass Risk | Primary Vector | Notes |
|------|-------------|---------------|-------|
| error-handling-standards.md | CRITICAL | BV-001 (no enforcement language at all) | Entire file is bypassable |
| tool-configuration.md | CRITICAL | BV-001 (no enforcement language at all) | Entire file is bypassable |
| file-organization.md | HIGH | BV-001, BV-003 | Mostly descriptive content |
| architecture-standards.md | HIGH | BV-003 (examples), BV-004 (redundancy) | Good rules buried in examples |
| coding-standards.md | HIGH | BV-003, BV-004 | Redundant with architecture-standards |
| testing-standards.md | MEDIUM | BV-003 | Good enforcement intent, poor language |
| mandatory-skill-usage.md | MEDIUM | BV-005 (no consequences) | Strong language, no tier system |
| project-workflow.md | MEDIUM | BV-006 (no quality gates) | Workflow without quality enforcement |
| markdown-navigation-standards.md | LOW | BV-002 only | Best-tiered file in the set |
| python-environment.md | LOW | BV-002 only | Strongest enforcement language |

---

## Redundancy Analysis

### Cross-File Redundancy Map

| Content | Primary File | Also In | Action |
|---------|-------------|---------|--------|
| Layer dependency rules | architecture-standards.md | coding-standards.md | Remove from coding-standards |
| CQRS naming conventions | architecture-standards.md | coding-standards.md | Remove from coding-standards |
| Error handling patterns | error-handling-standards.md | coding-standards.md | Remove from coding-standards |
| Test file naming | testing-standards.md | file-organization.md | Remove from file-organization |
| Source directory structure | architecture-standards.md | file-organization.md | Keep in file-organization only |
| Project workspace structure | project-workflow.md | file-organization.md | Remove from file-organization |
| Python version | python-environment.md | tool-configuration.md | Remove from tool-configuration |
| pytest configuration | tool-configuration.md | testing-standards.md | Keep in testing-standards only |
| UV requirement | python-environment.md | CLAUDE.md | Keep in both (intentional L2 reinforcement) |
| Pre-commit config | tool-configuration.md | testing-standards.md | Remove from both; belongs in actual config files |
| Architecture test examples | architecture-standards.md | testing-standards.md | Remove from testing-standards |

### Estimated Token Savings from Deduplication

Removing redundant content could save approximately **3,000-4,000 tokens** across all files.

---

## Optimization Recommendations

### Priority-Ordered Reduction Strategy

| Priority | File | Action | Est. Savings |
|----------|------|--------|-------------|
| 1 | tool-configuration.md | Replace with ~15-line enforcement table; remove all config blocks | ~2,780 |
| 2 | error-handling-standards.md | Replace with enforcement table + exception hierarchy table only | ~2,840 |
| 3 | architecture-standards.md | Remove code examples; consolidate rules into tables; remove references | ~2,620 |
| 4 | markdown-navigation-standards.md | Remove Intention, Evidence, References sections; keep rules only | ~2,060 |
| 5 | file-organization.md | Remove ASCII trees; keep naming table + one-class-per-file rule | ~1,930 |
| 6 | testing-standards.md | Remove code examples; remove redundant sections; keep rule tables | ~1,920 |
| 7 | coding-standards.md | Remove redundant sections; replace examples with tables | ~1,750 |
| 8 | project-workflow.md | Compact workflow; add quality gate content | ~760 |
| 9 | mandatory-skill-usage.md | Compact; add adversarial strategy triggers | ~620 |
| 10 | python-environment.md | Remove non-enforcement sections | ~440 |
| 11 | CLAUDE.md | Compact navigation; remove implementation details | ~340 |
| **Total Potential Savings** | | | **~18,060** |

### Consolidation Recommendations

| Current Files | Consolidate Into | Rationale |
|--------------|-----------------|-----------|
| tool-configuration.md + testing-standards.md | testing-standards.md | Tool config is enforcement-free; merge the 3-4 actual tool rules into testing-standards |
| error-handling-standards.md + coding-standards.md | coding-standards.md | Error handling rules are coding standards; the exception hierarchy is a 10-line table |
| file-organization.md + architecture-standards.md | architecture-standards.md | File organization is an architecture concern; merge the 3 real rules |

**Post-consolidation file count:** 7 files (from 10) + 1 new (quality-enforcement.md) = 8 files total.

---

## L2 Re-Injection Candidates

Content ranked by priority for V-024 re-injection (~600 token budget):

| Rank | Content | Source | Est. Tokens | Rationale |
|------|---------|--------|-------------|-----------|
| 1 | Constitutional constraints (P-003, P-020, P-022) | CLAUDE.md | ~80 | Foundational behavioral constraints; highest bypass impact if forgotten |
| 2 | Quality gate threshold (>= 0.92) + creator-critic-revision cycle | quality-enforcement.md (NEW) | ~100 | Central quality requirement; most likely to be forgotten in long sessions |
| 3 | Python environment (UV only) | python-environment.md / CLAUDE.md | ~60 | Frequently violated; high-value reinforcement |
| 4 | HARD enforcement tier definition + top 5 HARD rules | quality-enforcement.md (NEW) | ~120 | Enforcement framework anchor |
| 5 | Decision criticality levels (C1-C4) with review layer mapping | quality-enforcement.md (NEW) | ~100 | Prevents enforcement bypass through criticality misclassification |
| 6 | Architecture layer boundary rules (domain cannot import infra) | architecture-standards.md | ~80 | Core architecture invariant |
| 7 | One-class-per-file rule | file-organization.md | ~40 | Frequently violated structural rule |
| **Total** | | | **~580** | Within 600-token V-024 budget |

---

## References

| # | Document | Location | Content Used |
|---|----------|----------|--------------|
| 1 | ADR-EPIC002-002 (ACCEPTED) | `EN-402-enforcement-priority-analysis/TASK-005-enforcement-ADR.md` | Token budget targets, L1 layer specification |
| 2 | Barrier-1 ADV-to-ENF Handoff | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/adv-to-enf/barrier-1-adv-to-enf-handoff.md` | Strategy encoding requirements |
| 3 | EN-404 Enabler | `EN-404-rule-based-enforcement/EN-404-rule-based-enforcement.md` | FR/NFR requirements |
| 4 | TASK-001 Requirements | `EN-404-rule-based-enforcement/TASK-001-rule-requirements.md` | REQ-404-001 through REQ-404-064 |
| 5 | All .context/rules/ files (10 files) | `.context/rules/` | Full content audit |
| 6 | CLAUDE.md | Root directory | Root context audit |

---

*Agent: ps-investigator (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-404 Rule-Based Enforcement Enhancement*
*Quality Target: >= 0.92*
*Files Audited: 11 (10 rules + CLAUDE.md)*
*Total Current Tokens: ~30,160*
*Target Tokens: ~12,476*
*Budget Overrun: 2.42x*
