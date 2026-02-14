# TASK-003: Rule Enforcement End-to-End Testing

<!--
TEMPLATE: Task Deliverable
VERSION: 1.0.0
ENABLER: EN-406
AC: AC-3
CREATED: 2026-02-13 (ps-validator-406)
PURPOSE: End-to-end test specifications for rule-based enforcement mechanisms
-->

> **Type:** deliverable
> **Status:** complete
> **Parent:** EN-406-integration-testing-validation
> **AC Mapping:** AC-3 (Rule enforcement mechanisms pass end-to-end testing)
> **Agent:** ps-validator-406
> **Created:** 2026-02-13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Test scope for rule enforcement |
| [Tier Enforcement Tests](#tier-enforcement-tests) | HARD/MEDIUM/SOFT tier validation |
| [Token Budget Tests](#token-budget-tests) | L1 token budget compliance |
| [HARD Rule Inventory Tests](#hard-rule-inventory-tests) | 24 HARD rules verification |
| [L2 Re-injection Tests](#l2-re-injection-tests) | L2-REINJECT tag validation |
| [Quality SSOT Tests](#quality-ssot-tests) | quality-enforcement.md validation |
| [Content Quality Tests](#content-quality-tests) | Redundancy, clarity, accuracy |
| [Auto-Loading Tests](#auto-loading-tests) | Claude Code rule auto-loading |
| [Requirements Traceability](#requirements-traceability) | Test-to-requirement mapping |
| [References](#references) | Source documents |

---

## Overview

This document specifies end-to-end test cases for rule-based enforcement mechanisms defined in EN-404. Tests validate the three-tier enforcement system (HARD/MEDIUM/SOFT), token budget compliance, HARD rule inventory completeness, L2 re-injection tagging, quality SSOT file integrity, content quality (redundancy elimination), and auto-loading behavior.

### Test Summary

| Category | Test Count | ID Range |
|----------|------------|----------|
| Tier Enforcement | 12 | TC-TIER-001 through TC-TIER-012 |
| Token Budget | 8 | TC-TBUDG-001 through TC-TBUDG-008 |
| HARD Rule Inventory | 6 | TC-HARD-001 through TC-HARD-006 |
| L2 Re-injection | 5 | TC-L2R-001 through TC-L2R-005 |
| Quality SSOT | 4 | TC-SSOT-001 through TC-SSOT-004 |
| Content Quality | 5 | TC-CQUAL-001 through TC-CQUAL-005 |
| Auto-Loading | 4 | TC-ALOAD-001 through TC-ALOAD-004 |
| **Total** | **44** | |

---

## Tier Enforcement Tests

### TC-TIER-001: HARD Rule Language Compliance

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-001 |
| **Objective** | Verify all HARD rules use mandatory language (MUST, SHALL, NEVER, REQUIRED) |
| **Input** | All `.claude/rules/*.md` files |
| **Steps** | 1. Parse all rule files. 2. Identify HARD-tier rules. 3. Check language patterns. |
| **Expected Output** | Every HARD rule uses at least one mandatory keyword: MUST, SHALL, NEVER, REQUIRED |
| **Pass Criteria** | 100% compliance |
| **Requirements** | REQ-404-010, REQ-404-011 |
| **Verification** | Inspection |

### TC-TIER-002: HARD Rule Consequence Statements

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-002 |
| **Objective** | Verify every HARD rule has an explicit consequence statement |
| **Input** | All HARD rules across all rule files |
| **Steps** | 1. Identify all 24 HARD rules. 2. Check each for consequence statement. |
| **Expected Output** | Each HARD rule has a stated consequence (e.g., "violations will be blocked", "build will fail") |
| **Pass Criteria** | 24/24 HARD rules have consequences |
| **Requirements** | REQ-404-012 |
| **Verification** | Inspection |

### TC-TIER-003: HARD Rule Count Limit

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-003 |
| **Objective** | Verify total HARD rule count does not exceed 25 |
| **Input** | All `.claude/rules/*.md` files |
| **Steps** | 1. Count all rules with HARD-tier language. 2. Verify count <= 25. |
| **Expected Output** | Count: 24 (H-01 through H-24) |
| **Pass Criteria** | Count <= 25 |
| **Requirements** | REQ-404-013 |
| **Verification** | Analysis |

### TC-TIER-004: MEDIUM Rule Language Compliance

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-004 |
| **Objective** | Verify MEDIUM rules use advisory language (SHOULD, RECOMMENDED) |
| **Input** | All `.claude/rules/*.md` files |
| **Steps** | 1. Identify MEDIUM-tier rules. 2. Check language patterns. |
| **Expected Output** | MEDIUM rules use SHOULD, RECOMMENDED (not MUST/SHALL/NEVER) |
| **Pass Criteria** | No MEDIUM rule uses HARD language |
| **Requirements** | REQ-404-014 |
| **Verification** | Inspection |

### TC-TIER-005: SOFT Rule Language Compliance

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-005 |
| **Objective** | Verify SOFT rules use optional language (MAY, CONSIDER) |
| **Input** | All `.claude/rules/*.md` files |
| **Steps** | 1. Identify SOFT-tier rules. 2. Check language patterns. |
| **Expected Output** | SOFT rules use MAY, CONSIDER (not MUST/SHALL/SHOULD) |
| **Pass Criteria** | No SOFT rule uses HARD or MEDIUM language |
| **Requirements** | REQ-404-015 |
| **Verification** | Inspection |

### TC-TIER-006: Tier Separation - No Tier Mixing

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-006 |
| **Objective** | Verify no single rule mixes tier language |
| **Input** | All rules across all files |
| **Steps** | 1. Parse each rule. 2. Check for mixed tier language within single rules. |
| **Expected Output** | No rule contains both MUST and SHOULD for the same constraint |
| **Pass Criteria** | Zero mixed-tier rules |
| **Requirements** | REQ-404-016 |
| **Verification** | Inspection |

### TC-TIER-007: HARD Rule H-01 Verification (UV Only)

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-007 |
| **Objective** | Verify H-01 (UV-only Python environment) is correctly encoded |
| **Input** | `python-environment.md` |
| **Expected Output** | "NEVER use python, pip, pip3 directly" with HARD language and consequence |
| **Requirements** | REQ-404-010 |
| **Verification** | Inspection |

### TC-TIER-008: HARD Rule H-06 Verification (Import Boundaries)

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-008 |
| **Objective** | Verify H-06 (hexagonal import boundaries) is correctly encoded |
| **Input** | `architecture-standards.md` |
| **Expected Output** | Domain cannot import from application/infrastructure/interface with HARD language |
| **Requirements** | REQ-404-010 |
| **Verification** | Inspection |

### TC-TIER-009: HARD Rule H-12 Verification (One-Class-Per-File)

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-009 |
| **Objective** | Verify H-12 (one class per file) is correctly encoded |
| **Input** | `file-organization.md` or `architecture-standards.md` |
| **Expected Output** | "MANDATORY: Each Python file contains exactly ONE public class" with HARD language |
| **Requirements** | REQ-404-010 |
| **Verification** | Inspection |

### TC-TIER-010: HARD Rule H-20 Verification (No Recursive Subagents P-003)

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-010 |
| **Objective** | Verify H-20 (P-003 No Recursive Subagents) is correctly encoded |
| **Input** | Rule files or quality-enforcement.md |
| **Expected Output** | "Max ONE level: orchestrator -> worker" with HARD language and constitutional reference |
| **Requirements** | REQ-404-010 |
| **Verification** | Inspection |

### TC-TIER-011: Decision Criticality Encoding in Rules

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-011 |
| **Objective** | Verify C1-C4 decision criticality levels are encoded in rule files |
| **Input** | `quality-enforcement.md` |
| **Expected Output** | C1 (Routine), C2 (Standard), C3 (Significant), C4 (Critical) definitions present |
| **Requirements** | REQ-404-030, REQ-404-031 |
| **Verification** | Inspection |

### TC-TIER-012: Strategy Activation Mapping

| Field | Value |
|-------|-------|
| **ID** | TC-TIER-012 |
| **Objective** | Verify adversarial strategy activation mapped to criticality levels |
| **Input** | `quality-enforcement.md` |
| **Expected Output** | Mapping showing which strategies activate at C2, C3, C4 |
| **Requirements** | REQ-404-032, REQ-404-033 |
| **Verification** | Inspection |

---

## Token Budget Tests

### TC-TBUDG-001: Total L1 Token Count

| Field | Value |
|-------|-------|
| **ID** | TC-TBUDG-001 |
| **Objective** | Verify total L1 token count across all rule files <= 12,476 |
| **Input** | All `.claude/rules/*.md` files |
| **Steps** | 1. Measure character count of each file. 2. Apply chars/4 approximation. 3. Sum totals. |
| **Expected Output** | Total <= 12,476 tokens |
| **Pass Criteria** | Sum of all rule file tokens within budget |
| **Requirements** | REQ-404-001, REQ-404-002 |
| **Verification** | Test |

### TC-TBUDG-002: Per-File Token Budget - coding-standards.md

| Field | Value |
|-------|-------|
| **ID** | TC-TBUDG-002 |
| **Objective** | Verify coding-standards.md within allocated budget (~2,100 tokens) |
| **Input** | `.claude/rules/coding-standards.md` |
| **Expected Output** | Token count <= 2,100 |
| **Requirements** | REQ-404-003 |
| **Verification** | Test |

### TC-TBUDG-003: Per-File Token Budget - architecture-standards.md

| Field | Value |
|-------|-------|
| **ID** | TC-TBUDG-003 |
| **Objective** | Verify architecture-standards.md within allocated budget (~2,200 tokens) |
| **Input** | `.claude/rules/architecture-standards.md` |
| **Expected Output** | Token count <= 2,200 |
| **Requirements** | REQ-404-003 |
| **Verification** | Test |

### TC-TBUDG-004: Per-File Token Budget - quality-enforcement.md

| Field | Value |
|-------|-------|
| **ID** | TC-TBUDG-004 |
| **Objective** | Verify quality-enforcement.md within allocated budget (~2,200 tokens) |
| **Input** | `.claude/rules/quality-enforcement.md` |
| **Expected Output** | Token count <= 2,200 |
| **Requirements** | REQ-404-003 |
| **Verification** | Test |

### TC-TBUDG-005: Per-File Token Budget - testing-standards.md

| Field | Value |
|-------|-------|
| **ID** | TC-TBUDG-005 |
| **Objective** | Verify testing-standards.md within allocated budget (~1,500 tokens) |
| **Input** | `.claude/rules/testing-standards.md` |
| **Expected Output** | Token count <= 1,500 |
| **Requirements** | REQ-404-003 |
| **Verification** | Test |

### TC-TBUDG-006: Token Budget Buffer Verification

| Field | Value |
|-------|-------|
| **ID** | TC-TBUDG-006 |
| **Objective** | Verify sufficient buffer exists between actual and target token count |
| **Input** | All rule files |
| **Steps** | 1. Calculate total tokens. 2. Calculate buffer: 12,476 - actual. |
| **Expected Output** | Buffer >= 1,000 tokens (target ~1,300) |
| **Pass Criteria** | Meaningful buffer exists for future additions |
| **Requirements** | REQ-404-004 |
| **Verification** | Analysis |

### TC-TBUDG-007: Code Example Token Impact

| Field | Value |
|-------|-------|
| **ID** | TC-TBUDG-007 |
| **Objective** | Verify code examples have been optimized (currently ~60% of content per audit) |
| **Input** | All rule files |
| **Steps** | 1. Measure code block token count. 2. Calculate percentage of total. |
| **Expected Output** | Code examples reduced from ~60% to <= 40% of total content |
| **Pass Criteria** | Code block ratio reduced from audit baseline |
| **Requirements** | REQ-404-005 |
| **Verification** | Analysis |

### TC-TBUDG-008: XML Calibration Factor Application

| Field | Value |
|-------|-------|
| **ID** | TC-TBUDG-008 |
| **Objective** | Verify token counting uses 0.83x XML calibration factor where applicable |
| **Input** | All files containing XML/structured content |
| **Steps** | 1. Identify XML-heavy sections. 2. Verify calibration factor applied in token estimates. |
| **Expected Output** | XML-heavy content uses 0.83x calibration; plain text uses chars/4 |
| **Pass Criteria** | Consistent methodology applied |
| **Requirements** | REQ-404-006 |
| **Verification** | Analysis |

---

## HARD Rule Inventory Tests

### TC-HARD-001: Complete Inventory Presence

| Field | Value |
|-------|-------|
| **ID** | TC-HARD-001 |
| **Objective** | Verify all 24 HARD rules (H-01 through H-24) are present in rule files |
| **Input** | All `.claude/rules/*.md` files |
| **Steps** | 1. Extract all HARD-tier rules. 2. Map to H-01 through H-24 inventory. |
| **Expected Output** | All 24 HARD rules accounted for |
| **Pass Criteria** | 24/24 present |
| **Requirements** | REQ-404-010 |
| **Verification** | Inspection |

### TC-HARD-002: HARD Rule Source Traceability

| Field | Value |
|-------|-------|
| **ID** | TC-HARD-002 |
| **Objective** | Verify each HARD rule traces to its authoritative source |
| **Input** | HARD rules inventory from EN-404 TASK-003 |
| **Steps** | 1. For each HARD rule, verify source reference. 2. Cross-check source document. |
| **Expected Output** | Each rule traces to: Constitution, ADR, Pattern Catalog, or standard |
| **Pass Criteria** | All 24 rules have valid source traceability |
| **Requirements** | REQ-404-011 |
| **Verification** | Inspection |

### TC-HARD-003: HARD Rule Distribution Across Files

| Field | Value |
|-------|-------|
| **ID** | TC-HARD-003 |
| **Objective** | Verify HARD rules are distributed to correct files per allocation |
| **Input** | All rule files |
| **Expected Distribution** | coding-standards (H-01 through H-05), architecture-standards (H-06 through H-11), file-organization (H-12, H-13), quality-enforcement (H-14 through H-24) |
| **Pass Criteria** | Distribution matches EN-404 TASK-003 allocation |
| **Requirements** | REQ-404-010 |
| **Verification** | Inspection |

### TC-HARD-004: No Duplicate HARD Rules

| Field | Value |
|-------|-------|
| **ID** | TC-HARD-004 |
| **Objective** | Verify no HARD rule appears in multiple files |
| **Input** | All rule files |
| **Steps** | 1. Extract HARD rules from each file. 2. Check for duplicates across files. |
| **Expected Output** | Each HARD rule appears exactly once |
| **Pass Criteria** | Zero duplicates |
| **Requirements** | REQ-404-013 |
| **Verification** | Inspection |

### TC-HARD-005: HARD Rule Bypass Vector Assessment

| Field | Value |
|-------|-------|
| **ID** | TC-HARD-005 |
| **Objective** | Verify identified bypass vectors (BV-001 through BV-007) are mitigated |
| **Input** | HARD rules and their enforcement mechanisms |
| **Steps** | 1. For each bypass vector from EN-404 TASK-002. 2. Verify mitigation present. |
| **Expected Output** | All 7 bypass vectors have documented mitigation |
| **Pass Criteria** | 7/7 mitigated |
| **Requirements** | REQ-404-017 |
| **Verification** | Analysis |

### TC-HARD-006: Constitutional Principle Encoding

| Field | Value |
|-------|-------|
| **ID** | TC-HARD-006 |
| **Objective** | Verify P-003, P-020, P-022 are encoded as HARD rules |
| **Input** | quality-enforcement.md or relevant rule file |
| **Expected Output** | P-003 -> H-20, P-020 -> H-21, P-022 -> H-22 (or equivalent mapping) |
| **Pass Criteria** | All 3 constitutional principles mapped to HARD rules |
| **Requirements** | REQ-404-020 |
| **Verification** | Inspection |

---

## L2 Re-injection Tests

### TC-L2R-001: L2-REINJECT Tag Presence

| Field | Value |
|-------|-------|
| **ID** | TC-L2R-001 |
| **Objective** | Verify L2-REINJECT tags exist in rule files |
| **Input** | All `.claude/rules/*.md` files |
| **Steps** | 1. Search for L2-REINJECT HTML comment tags. 2. Count and catalog. |
| **Expected Output** | At least 8 L2-REINJECT tags present (8 ranked content items per EN-404 TASK-003) |
| **Pass Criteria** | >= 8 L2-REINJECT tags found |
| **Requirements** | REQ-404-050, REQ-404-051 |
| **Verification** | Inspection |

### TC-L2R-002: L2-REINJECT Tag Format

| Field | Value |
|-------|-------|
| **ID** | TC-L2R-002 |
| **Objective** | Verify L2-REINJECT tags follow correct format |
| **Input** | All L2-REINJECT tags found in rule files |
| **Expected Format** | `<!-- L2-REINJECT rank=N tokens=M content="description" -->` |
| **Pass Criteria** | All tags have rank, tokens, and content attributes |
| **Requirements** | REQ-404-052 |
| **Verification** | Inspection |

### TC-L2R-003: L2-REINJECT Rank Ordering

| Field | Value |
|-------|-------|
| **ID** | TC-L2R-003 |
| **Objective** | Verify L2-REINJECT ranks are unique and sequential |
| **Input** | All L2-REINJECT tags |
| **Steps** | 1. Extract ranks. 2. Verify unique sequential ordering (1, 2, 3...). |
| **Expected Output** | Ranks 1 through N with no gaps or duplicates |
| **Pass Criteria** | Unique, sequential ranks |
| **Requirements** | REQ-404-053 |
| **Verification** | Analysis |

### TC-L2R-004: L2-REINJECT Token Budget

| Field | Value |
|-------|-------|
| **ID** | TC-L2R-004 |
| **Objective** | Verify total L2-REINJECT token allocation <= ~510 tokens |
| **Input** | All L2-REINJECT tags |
| **Steps** | 1. Sum tokens attributes from all tags. 2. Verify total <= 510. |
| **Expected Output** | Total <= 510 tokens (within L2 600-token budget minus overhead) |
| **Pass Criteria** | Sum within budget |
| **Requirements** | REQ-404-054 |
| **Verification** | Analysis |

### TC-L2R-005: L2-REINJECT Content Alignment with V-024

| Field | Value |
|-------|-------|
| **ID** | TC-L2R-005 |
| **Objective** | Verify L2-REINJECT content aligns with UserPromptSubmit V-024 content blocks |
| **Input** | L2-REINJECT tags vs. PromptReinforcementEngine content blocks |
| **Steps** | 1. Map L2-REINJECT content to V-024 blocks. 2. Verify alignment. |
| **Expected Output** | L2-REINJECT content feeds into correct V-024 blocks |
| **Pass Criteria** | Alignment documented and verified |
| **Requirements** | REQ-404-050, REQ-403-011 |
| **Verification** | Inspection |

---

## Quality SSOT Tests

### TC-SSOT-001: quality-enforcement.md Existence

| Field | Value |
|-------|-------|
| **ID** | TC-SSOT-001 |
| **Objective** | Verify quality-enforcement.md exists as SSOT for enforcement constants |
| **Input** | `.claude/rules/quality-enforcement.md` |
| **Expected Output** | File exists |
| **Pass Criteria** | File present at expected path |
| **Requirements** | REQ-404-040 |
| **Verification** | Test |

### TC-SSOT-002: quality-enforcement.md Required Content

| Field | Value |
|-------|-------|
| **ID** | TC-SSOT-002 |
| **Objective** | Verify quality-enforcement.md contains all required enforcement constants |
| **Input** | `quality-enforcement.md` |
| **Expected Content** | Quality gate threshold (>= 0.92), HARD rule summary, adversarial strategy list, decision criticality levels, token budgets, constitutional principles |
| **Pass Criteria** | All required content categories present |
| **Requirements** | REQ-404-041, REQ-404-042 |
| **Verification** | Inspection |

### TC-SSOT-003: quality-enforcement.md Navigation Table

| Field | Value |
|-------|-------|
| **ID** | TC-SSOT-003 |
| **Objective** | Verify quality-enforcement.md has NAV-001 through NAV-006 compliant navigation |
| **Input** | `quality-enforcement.md` |
| **Expected Output** | Navigation table with anchor links after frontmatter, before content |
| **Pass Criteria** | Compliant with markdown navigation standards |
| **Requirements** | REQ-404-043 |
| **Verification** | Inspection |

### TC-SSOT-004: quality-enforcement.md Cross-Reference Consistency

| Field | Value |
|-------|-------|
| **ID** | TC-SSOT-004 |
| **Objective** | Verify enforcement constants in quality-enforcement.md match those in other rule files |
| **Input** | quality-enforcement.md + all other rule files |
| **Steps** | 1. Extract constants from SSOT. 2. Cross-reference with other files. 3. Check consistency. |
| **Expected Output** | No contradictions between SSOT and individual rule files |
| **Pass Criteria** | Zero inconsistencies |
| **Requirements** | REQ-404-044, REQ-404-045 |
| **Verification** | Inspection |

---

## Content Quality Tests

### TC-CQUAL-001: Cross-File Redundancy Elimination

| Field | Value |
|-------|-------|
| **ID** | TC-CQUAL-001 |
| **Objective** | Verify redundant content has been eliminated across rule files |
| **Input** | All `.claude/rules/*.md` files |
| **Steps** | 1. Compare content across files. 2. Identify remaining duplication. |
| **Expected Output** | No substantive content duplication across files |
| **Pass Criteria** | Any shared concepts reference SSOT rather than duplicating |
| **Requirements** | REQ-404-060 |
| **Verification** | Inspection |

### TC-CQUAL-002: File Consolidation Verification

| Field | Value |
|-------|-------|
| **ID** | TC-CQUAL-002 |
| **Objective** | Verify planned consolidations from EN-404 TASK-002 audit |
| **Input** | Current rule file inventory vs. audit recommendations |
| **Expected Output** | 10 files -> 8 optimized (error-handling merged into coding, file-org into architecture, tool-config into testing, quality-enforcement.md created) |
| **Pass Criteria** | Consolidation plan executed or documented deviation |
| **Requirements** | REQ-404-061 |
| **Verification** | Analysis |

### TC-CQUAL-003: Code Example Optimization

| Field | Value |
|-------|-------|
| **ID** | TC-CQUAL-003 |
| **Objective** | Verify code examples have been optimized for token efficiency |
| **Input** | All rule files |
| **Steps** | 1. Measure code block tokens. 2. Compare to audit baseline (~60% of content). |
| **Expected Output** | Code examples reduced to essential demonstrations only |
| **Pass Criteria** | Measurable reduction from ~60% baseline |
| **Requirements** | REQ-404-062 |
| **Verification** | Analysis |

### TC-CQUAL-004: Adversarial Strategy Encoding

| Field | Value |
|-------|-------|
| **ID** | TC-CQUAL-004 |
| **Objective** | Verify 10 selected adversarial strategies are encoded in rule files |
| **Input** | quality-enforcement.md |
| **Steps** | 1. Search for strategy references (S-001 through S-014 subset). 2. Verify 10 are present. |
| **Expected Output** | 10 strategies encoded with identifiers and descriptions |
| **Pass Criteria** | 10/10 strategies present |
| **Requirements** | REQ-404-020, REQ-404-021 |
| **Verification** | Inspection |

### TC-CQUAL-005: Context Rot Mitigation Encoding

| Field | Value |
|-------|-------|
| **ID** | TC-CQUAL-005 |
| **Objective** | Verify context rot mitigation guidance is encoded in rules |
| **Input** | quality-enforcement.md |
| **Expected Output** | Context rot awareness, L2 re-injection purpose, defense-in-depth explanation |
| **Pass Criteria** | Context rot mitigation content present |
| **Requirements** | REQ-404-063, REQ-404-064 |
| **Verification** | Inspection |

---

## Auto-Loading Tests

### TC-ALOAD-001: Rule File Auto-Loading

| Field | Value |
|-------|-------|
| **ID** | TC-ALOAD-001 |
| **Objective** | Verify all `.claude/rules/*.md` files are auto-loaded by Claude Code at session start |
| **Input** | Claude Code session initialization |
| **Steps** | 1. Start new Claude Code session. 2. Check which rule files are loaded. |
| **Expected Output** | All rule files in `.claude/rules/` directory are loaded |
| **Pass Criteria** | Every `.md` file in `.claude/rules/` present in session context |
| **Requirements** | REQ-404-001 |
| **Verification** | Test |
| **Note** | This test closes EN-405 conditional AC-5 (auto-loading verification) |

### TC-ALOAD-002: Symlink Resolution

| Field | Value |
|-------|-------|
| **ID** | TC-ALOAD-002 |
| **Objective** | Verify `.claude/rules/` symlinks to `.context/rules/` resolve correctly |
| **Input** | Symlink structure |
| **Steps** | 1. Verify symlinks exist. 2. Verify content accessible through symlinks. |
| **Expected Output** | Symlinks resolve; content identical through both paths |
| **Pass Criteria** | Content accessible and identical |
| **Requirements** | REQ-404-001 |
| **Verification** | Test |

### TC-ALOAD-003: New File Addition

| Field | Value |
|-------|-------|
| **ID** | TC-ALOAD-003 |
| **Objective** | Verify newly added rule files are automatically loaded in next session |
| **Input** | Add temporary test file to `.claude/rules/` |
| **Steps** | 1. Add file. 2. Start new session. 3. Verify file loaded. 4. Clean up. |
| **Expected Output** | New file appears in session context |
| **Pass Criteria** | Auto-loading picks up new files |
| **Requirements** | REQ-404-001 |
| **Verification** | Test |

### TC-ALOAD-004: Total Token Load Measurement

| Field | Value |
|-------|-------|
| **ID** | TC-ALOAD-004 |
| **Objective** | Measure actual token count loaded at session start |
| **Input** | Session start context dump |
| **Steps** | 1. Capture all loaded content. 2. Measure total tokens. 3. Compare to 12,476 budget. |
| **Expected Output** | Measurement <= 12,476 tokens |
| **Pass Criteria** | Within budget |
| **Requirements** | REQ-404-001, REQ-404-002 |
| **Verification** | Test |
| **Note** | Real tokenizer verification; helps close EN-405 conditional AC regarding tokenizer |

---

## Requirements Traceability

| Test ID | Requirements Verified |
|---------|----------------------|
| TC-TIER-001 | REQ-404-010, REQ-404-011 |
| TC-TIER-002 | REQ-404-012 |
| TC-TIER-003 | REQ-404-013 |
| TC-TIER-004 | REQ-404-014 |
| TC-TIER-005 | REQ-404-015 |
| TC-TIER-006 | REQ-404-016 |
| TC-TIER-007 through TC-TIER-010 | REQ-404-010 (specific rule verification) |
| TC-TIER-011 | REQ-404-030, REQ-404-031 |
| TC-TIER-012 | REQ-404-032, REQ-404-033 |
| TC-TBUDG-001 | REQ-404-001, REQ-404-002 |
| TC-TBUDG-002 through TC-TBUDG-005 | REQ-404-003 |
| TC-TBUDG-006 | REQ-404-004 |
| TC-TBUDG-007 | REQ-404-005 |
| TC-TBUDG-008 | REQ-404-006 |
| TC-HARD-001 | REQ-404-010 |
| TC-HARD-002 | REQ-404-011 |
| TC-HARD-003 | REQ-404-010 |
| TC-HARD-004 | REQ-404-013 |
| TC-HARD-005 | REQ-404-017 |
| TC-HARD-006 | REQ-404-020 |
| TC-L2R-001 | REQ-404-050, REQ-404-051 |
| TC-L2R-002 | REQ-404-052 |
| TC-L2R-003 | REQ-404-053 |
| TC-L2R-004 | REQ-404-054 |
| TC-L2R-005 | REQ-404-050, REQ-403-011 |
| TC-SSOT-001 | REQ-404-040 |
| TC-SSOT-002 | REQ-404-041, REQ-404-042 |
| TC-SSOT-003 | REQ-404-043 |
| TC-SSOT-004 | REQ-404-044, REQ-404-045 |
| TC-CQUAL-001 | REQ-404-060 |
| TC-CQUAL-002 | REQ-404-061 |
| TC-CQUAL-003 | REQ-404-062 |
| TC-CQUAL-004 | REQ-404-020, REQ-404-021 |
| TC-CQUAL-005 | REQ-404-063, REQ-404-064 |
| TC-ALOAD-001 | REQ-404-001, EN-405 AC-5 |
| TC-ALOAD-002 | REQ-404-001 |
| TC-ALOAD-003 | REQ-404-001 |
| TC-ALOAD-004 | REQ-404-001, REQ-404-002 |

---

## References

| Document | Path | Relevance |
|----------|------|-----------|
| EN-404 TASK-001 | `../EN-404-rule-based-enforcement/TASK-001-rule-requirements.md` | 44 rule requirements |
| EN-404 TASK-002 | `../EN-404-rule-based-enforcement/TASK-002-rule-audit.md` | Current state audit, redundancy analysis |
| EN-404 TASK-003 | `../EN-404-rule-based-enforcement/TASK-003-tiered-enforcement.md` | Tiered enforcement design, token budgets, HARD rules |
| EN-403 TASK-008 | `../EN-403-hook-based-enforcement/TASK-008-validation-report.md` | Combined EN-403/404 validation |
| TASK-001 Integration Test Plan | `TASK-001-integration-test-plan.md` | Master test plan |

---

*Generated by ps-validator-406 | 2026-02-13 | EN-406 AC-3*
