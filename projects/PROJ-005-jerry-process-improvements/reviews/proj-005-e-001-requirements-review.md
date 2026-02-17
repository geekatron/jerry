# Requirements Review: PROJ-005 WTI-007/WTI-008 Content Quality Rules

> **Type:** Requirements Review
> **Project:** PROJ-005-jerry-process-improvements
> **Entry:** e-001
> **Reviewer:** nse-reviewer (v1.0.0)
> **Date:** 2026-02-16
> **Review Standard:** NASA NPR 7123.1D (adapted)
> **Scope:** WTI-007, WTI-008 rule definitions; 9 task acceptance criteria; dependency chain

```
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
```

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Overall assessment, critical findings, key strengths |
| [L1 Detailed Review](#l1-detailed-review) | Six review areas with finding-level detail |
| [L2 Strategic Assessment](#l2-strategic-assessment) | Architectural fitness, risk areas, phasing recommendations |
| [Findings Table](#findings-table) | Consolidated findings with severity and recommendation |
| [Review Methodology](#review-methodology) | How this review was conducted |
| [References](#references) | Source documents consulted |

---

## L0 Executive Summary

### Overall Assessment: PASS WITH FINDINGS

The PROJ-005 implementation plan for WTI-007 and WTI-008 is well-researched, well-structured, and ready for implementation with minor corrections. The research synthesis (proj-005-s-001) provides strong traceability from industry best practices through gap analysis to concrete rules. The two-rule consolidation strategy (WTI-007 with 7 sub-rules, WTI-008 with 4 sub-rules) is appropriate and avoids rule proliferation.

| Metric | Count |
|--------|-------|
| **CRITICAL findings** | 0 |
| **MAJOR findings** | 3 |
| **MINOR findings** | 6 |
| **INFO observations** | 5 |
| **Total findings** | 14 |

### Key Strengths

1. **Strong research foundation.** Three completed research artifacts (r-001, a-001, s-001) with cross-referenced findings and explicit reconciliation of divergent positions.
2. **Testable sub-rules.** WTI-007 sub-rules are predominantly verifiable via regex pattern matching or counting. This enables automated enforcement in the wt-auditor.
3. **User autonomy preserved.** WTI-008d skip mechanism explicitly respects P-020 (User Authority). The "(Recommended)" tag pattern avoids coercion.
4. **Layered enforcement model.** The four-layer quality gate model (structural, content form, content semantics, human review) provides clear separation of automated vs interactive enforcement.
5. **Dependency chain is sound.** The critical path (TASK-001 -> TASK-002 -> TASK-004..006) correctly sequences foundation before consumers.

### Key Concerns

1. **TASK-009 (DOD.md) is missing from the dependency chain.** TASK-005 has a cross-reference to TASK-009 in its AC, but TASK-009 is not listed as a dependency of TASK-005. This creates an ordering risk.
2. **WTI-007c (Actor-First Format) has ambiguous testability for Enablers and Tasks.** The actor/system subject pattern works well for Stories ("User can...") but Tasks and Enablers may legitimately have AC that describe system-internal outcomes without an actor.
3. **TASK-008 AC does not cover WTI-007c (Actor-First Format) detection.** The auditor AC lists detection for WTI-007a, 007b, 007d, 007e, 007f but explicitly omits 007c. The severity table assigns actor-format as INFO, but the detection pattern is not listed in the AC.

---

## L1 Detailed Review

### 1. WTI-007 Testability Assessment

| Sub-Rule | Testable? | Verification Method | Ambiguity Assessment |
|----------|-----------|---------------------|----------------------|
| **WTI-007a** (No DoD in AC) | YES | Regex matching for DoD phrases: "test coverage", "code review", "documentation updated", "deployment verification", "QA sign-off". Universal test: "If it applies to every work item equally, it is DoD, not AC." | LOW ambiguity. The universal test is clear and actionable. The DoD keyword list is finite and enumerable. |
| **WTI-007b** (No Implementation Details in AC) | YES | Regex matching for file paths (`/`, `.cs`, `.py`, `.ts`), class names (PascalCase patterns), method names, architecture pattern names. | MEDIUM ambiguity. "Architecture patterns" and "technology-specific decisions" are broad. What about "REST API returns 409"? "REST" is a technology decision, "409" is an HTTP status code. The boundary between "observable behavior" and "implementation detail" needs explicit examples for edge cases. See Finding F-003. |
| **WTI-007c** (Actor-First Format) | PARTIAL | Regex for subject-first pattern: line starts with checkbox then actor/system word ("User", "System", "API", "Admin", etc.). | MEDIUM ambiguity. Works well for Stories (actor-focused by nature). For Tasks and Enablers, AC may legitimately describe non-actor outcomes: "Configuration file supports X format", "Index rebuilds in under 5 seconds". The rule says "should" (MEDIUM enforcement), which helps, but the actor word list needs expansion or the rule needs explicit carve-outs for non-story types. See Finding F-004. |
| **WTI-007d** (No Hedge Words) | YES | Regex matching for exact hedge phrases: "should be able to", "might need to", "could potentially", "if possible", "ideally", "as needed", "when appropriate". | LOW ambiguity. The hedge word list is explicit and finite. False positive risk is low because these are multi-word phrases, not single words. |
| **WTI-007e** (AC Bullet Count Limits) | YES | Count checkbox patterns (`- [ ]`) per work item type. Compare against limits: Story 5, Bug 3, Task 3, Enabler 5, Feature 5. | LOW ambiguity. Counting is deterministic. Work item type is determined by template/frontmatter. |
| **WTI-007f** (Summary Brevity) | YES | Sentence counting (period-delimited segments) in Summary section. Max 3 sentences. No implementation details (reuse WTI-007b patterns). Bug summaries check for symptom language vs root cause language. | LOW-MEDIUM ambiguity. Sentence counting has edge cases (abbreviations like "e.g.", numbered lists, URLs with periods). The "symptom vs root cause" distinction for bugs could benefit from explicit examples. |
| **WTI-007g** (Scope Overflow Signal) | YES | Triggered when WTI-007e count exceeds limit. Verification: SPIDR recommendation present when count exceeds. | LOW ambiguity. This is a conditional trigger, not a standalone check. Testability depends entirely on WTI-007e, which is deterministic. |

**WTI-007 Testability Verdict:** 5 of 7 sub-rules are clearly testable with low ambiguity. WTI-007b and WTI-007c have medium ambiguity that should be addressed with additional examples and edge case guidance in the content-standards reference file.

### 2. WTI-008 Testability Assessment

| Sub-Rule | Testable? | Verification Method | Ambiguity Assessment |
|----------|-----------|---------------------|----------------------|
| **WTI-008a** (Pre-Creation Checkpoint) | YES (behavioral) | Verify Claude presents summary before writing file. Check for type-specific fields: role/goal/benefit (stories), symptom/location/severity (bugs), what/why (enablers). | LOW ambiguity for the checkpoint trigger. MEDIUM ambiguity for what constitutes "sufficient" summary content. The rule specifies type-specific fields, which helps. |
| **WTI-008b** (AC Review Checkpoint) | YES (behavioral) | Verify Claude presents AC with three quality check questions before writing file. Questions are specified: (1) engineer build without questions, (2) QA write test cases, (3) ambiguous terms. | LOW ambiguity. The three questions are explicitly specified. The checkpoint is binary: it either fires or it does not. |
| **WTI-008c** (Missing Information Flag) | PARTIAL | Verify Claude asks for clarification when context is insufficient rather than generating vague AC. | HIGH ambiguity. "Insufficient context" is subjective. What threshold of information triggers the flag? This is the least testable sub-rule because it requires Claude to self-assess its own confidence level. There is no explicit rubric for "sufficient" vs "insufficient" context. See Finding F-001. |
| **WTI-008d** (Skip Mechanism) | YES | Verify: (1) user can say "skip" or "just create it", (2) Claude acknowledges quality trade-off, (3) HTML comment `<!-- WTI-008: Checkpoint skipped by user -->` is present in created file. | LOW ambiguity. The skip trigger phrases, acknowledgment requirement, and HTML comment are all explicit and verifiable. |

**WTI-008 Testability Verdict:** 3 of 4 sub-rules are testable. WTI-008c has high ambiguity because "insufficient context" is subjective. Recommendation: provide 2-3 explicit examples of when the flag should fire (e.g., "user says 'create a bug for the login issue' with no symptom, steps, or location").

### 3. Conflict Analysis with WTI-001 through WTI-006

| Existing Rule | Relationship to WTI-007/008 | Conflict? | Assessment |
|---------------|------------------------------|-----------|------------|
| **WTI-001** (Real-Time State Updates) | WTI-008 adds checkpoints before creation, which could delay state updates. | NO CONFLICT | WTI-001 requires updates "immediately after completing work." WTI-008 occurs BEFORE work (before writing the file), not after. The checkpoint happens in the creation workflow, not the state-update workflow. These are temporally separate. |
| **WTI-002** (No Closure Without Verification) | WTI-007 improves AC quality, making WTI-002 verification more meaningful. | SYNERGY | Better AC (WTI-007) means WTI-002 verification has clearer criteria to verify against. Reinforcing relationship. |
| **WTI-003** (Truthful and Accurate State) | WTI-007f (Summary Brevity) and WTI-007b (No Implementation Details in AC) could create tension if the "accurate" state requires implementation context. | MINOR TENSION | WTI-003 requires state to be "truthful" and "accurate." WTI-007b says AC must not contain implementation details. These are compatible because implementation details belong in the Description or Implementation Notes sections, not AC. However, the content-standards reference file should explicitly state where implementation details DO belong. See Finding F-005. |
| **WTI-004** (Synchronize Before Reporting) | No interaction. | NO CONFLICT | WTI-004 is about reading state before reporting. WTI-007/008 are about creating content. Orthogonal concerns. |
| **WTI-005** (Atomic Task State) | WTI-008 checkpoints add interactive pauses during creation, which could interrupt atomicity if Claude creates a child but pauses before updating the parent. | MINOR TENSION | If WTI-008a checkpoint fires during child creation and the user abandons the checkpoint, the parent may not be updated. However, this is a general creation-abandonment issue, not specific to WTI-008. WTI-005 is about state updates, not creation. LOW risk. |
| **WTI-006** (Evidence-Based Closure) | WTI-007 improves AC quality, making WTI-006 evidence requirements more specific. | SYNERGY | Better AC means the evidence table (WTI-006) has clearer criteria to evidence against. Reinforcing relationship. |

**Conflict Analysis Verdict:** No direct conflicts. Two synergies (WTI-002, WTI-006 both benefit from higher AC quality). Two minor tensions that are manageable with clarifying guidance. No changes to existing rules required.

### 4. Task AC Completeness Review

#### TASK-001: Create worktracker-content-standards.md

| AC Item | Complete? | Unambiguous? | Issue |
|---------|-----------|--------------|-------|
| File exists at path | YES | YES | - |
| Contains #1 Rule | YES | YES | - |
| Contains bullet limits table | YES | YES | - |
| Contains anti-pattern table with 5+ examples | YES | MOSTLY | Types of anti-patterns listed (DoD, impl details, hedge, vague, too broad) -- good |
| Contains concrete vs vague examples (6+ pairs) | YES | YES | - |
| Contains AC vs DoD separation + universal test | YES | YES | - |
| Contains Hemingway writing style directive | YES | PARTIAL | What specifically constitutes the "Hemingway directive"? Short sentences? Active voice? No adverbs? The AC should specify the key elements or reference a definition. See Finding F-006. |
| Contains pre-finalization quality check (4 questions) | YES | YES | The 4 questions are specified in the synthesis (engineer build, QA test cases, ambiguous terms, and implicitly a fourth). The AC should enumerate the 4 questions or reference where they are defined. See Finding F-007. |
| Follows markdown-navigation-standards | YES | YES | - |

**Missing AC:** No criterion for SPIDR splitting guide content, which the PLAN.md mentions as part of the content-standards file. See Finding F-008.

#### TASK-002: Add WTI-007 to behavior-rules.md

| AC Item | Complete? | Unambiguous? | Issue |
|---------|-----------|--------------|-------|
| WTI-007 section after WTI-006, HARD | YES | YES | - |
| All 7 sub-rules defined | YES | YES | Sub-rules enumerated by ID and name |
| Cross-references content-standards.md | YES | YES | - |
| Compatible with WTI-001-006 structure | YES | MOSTLY | "Compatible" is subjective. Should specify: same heading pattern, same table format, same enforcement level notation. See Finding F-009. |

#### TASK-003: Add WTI-008 to behavior-rules.md

| AC Item | Complete? | Unambiguous? | Issue |
|---------|-----------|--------------|-------|
| WTI-008 section after WTI-007, HARD | YES | YES | - |
| All 4 sub-rules defined | YES | YES | - |
| Checkpoint question templates | YES | YES | "Stories, Bugs, and general AC review" -- three template types |
| "(Recommended)" tag | YES | YES | References feedback item #7 for traceability |
| Skip mechanism + P-020 | YES | YES | - |

**Missing AC:** No criterion for the HTML comment format `<!-- WTI-008: Checkpoint skipped by user -->` being defined in the rule text. The sub-rule definition (WTI-008d) specifies this, but TASK-003's AC does not explicitly verify this detail is in the written rule. LOW risk -- implicit in "Sub-rules defined." See Finding F-010.

#### TASK-004: Add Quick Creation Guide to BUG.md

| AC Item | Complete? | Unambiguous? | Issue |
|---------|-----------|--------------|-------|
| Guide near top (after frontmatter, before Doc Sections) | YES | YES | - |
| Specifies summary, AC limits, repro steps, format | YES | YES | - |
| BAD/GOOD AC examples | YES | YES | "Specific to bugs" -- good specificity |
| Notes which sections to skip | YES | YES | Sections listed: Root Cause, Fix Description, Evidence |

**No issues found.** This AC is well-specified.

#### TASK-005: Add Quick Creation Guide to STORY.md + reframe DoD

| AC Item | Complete? | Unambiguous? | Issue |
|---------|-----------|--------------|-------|
| Guide near top | YES | YES | - |
| User Story format, 5 AC bullets, actor-first | YES | YES | - |
| "AC must NOT contain DoD items" statement | YES | YES | - |
| DoD section reframed with note | YES | YES | Specific line numbers (289-313) and exact note text provided |

**Dependency issue:** AC bullet 5 states "STORY.md DoD section (TASK-005) cross-references this file" in TASK-009's AC. This creates a bidirectional dependency: TASK-005 reframes the DoD section, and TASK-009 creates the file that TASK-005's reframe should reference. But TASK-009 is NOT listed as a dependency of TASK-005 in the dependency chain. See Finding F-002.

#### TASK-006: Add Quick Creation Guide to TASK.md

| AC Item | Complete? | Unambiguous? | Issue |
|---------|-----------|--------------|-------|
| Guide near top | YES | YES | - |
| Description, 3 AC bullets, verification-oriented | YES | YES | - |
| BAD/GOOD AC examples | YES | YES | "Specific to tasks" -- good |
| Implementation details belong elsewhere | YES | YES | - |

**No issues found.** This AC is well-specified.

#### TASK-009: Create shared DOD.md

| AC Item | Complete? | Unambiguous? | Issue |
|---------|-----------|--------------|-------|
| File exists at path | YES | YES | - |
| Contains DoD items from STORY.md lines 289-313 | YES | YES | Source material identified |
| Includes specific items (code reviewed, tests, docs, integration) | YES | YES | - |
| Explicit "do NOT belong in AC" statement | YES | YES | - |
| STORY.md cross-references this file | YES | YES | References TASK-005 |

**Missing AC:** No criterion for DOD.md following markdown-navigation-standards (unlike TASK-001 which explicitly requires it). See Finding F-011.

#### TASK-007: Update SKILL.md to load content standards

| AC Item | Complete? | Unambiguous? | Issue |
|---------|-----------|--------------|-------|
| `@rules/worktracker-content-standards.md` added | YES | YES | Exact string specified |
| WTI-007 and WTI-008 in WTI Rules Enforced table | YES | YES | - |
| Content quality in Core Capabilities | YES | PARTIAL | "Mentioned" is vague. Should the AC specify the capability text or just its presence? LOW risk. |

#### TASK-008: Add content quality audit phase to wt-auditor.md

| AC Item | Complete? | Unambiguous? | Issue |
|---------|-----------|--------------|-------|
| Phase 2.5 between template compliance and relationship integrity | YES | YES | Placement is specific |
| Detection patterns for 007a, 007b, 007d, 007e, 007f | YES | MOSTLY | WTI-007c (Actor-First Format) is missing from the detection list. This is consistent with the INFO severity assignment in the AC, but the omission should be explicit (e.g., "007c excluded from automated detection"). See Finding F-012. |
| Audit report format with 4 columns | YES | YES | Columns specified: file, sub-rule, matched text, remediation |
| Severity levels | YES | YES | WARNING for bullet count and DoD; INFO for hedge words and actor-format |

**Inconsistency:** The AC assigns "hedge words" as INFO severity, but WTI-007d is listed in the detection patterns (alongside 007a, 007b, 007e, 007f which are all at WARNING or higher enforcement). The synthesis document (s-001, line 238) also lists actor-first as INFO. This is internally consistent but worth noting: hedge words (MEDIUM enforcement) get INFO severity in the auditor, while bullet count (HARD enforcement) gets WARNING. The mapping from enforcement level to audit severity should be documented. See Finding F-013.

### 5. Gap Analysis

#### Gap 1: No Enabler-Specific or Feature-Specific AC Guidance in WTI-007c

WTI-007c (Actor-First Format) provides examples for Stories ("User can...") and system interactions ("System validates...", "API returns..."). However, Enablers and Features often have AC that describe infrastructure outcomes:

- "Build pipeline produces artifacts in under 10 minutes"
- "Configuration supports hot-reload without service restart"
- "Database migration runs forward and backward without data loss"

These are valid AC but do not start with an actor. The content-standards reference file should include Enabler/Feature-specific AC examples. The synthesis acknowledges this (ENABLER and FEATURE guides are Phase 3, P2 priority), but the current WTI-007c rule text does not carve out these types.

**Recommendation:** Add an explicit note to WTI-007c: "For Enablers and Features, the 'actor' may be a system component (e.g., 'Build pipeline...', 'Database migration...')."

#### Gap 2: No Guidance on AC for Sub-Tasks

The bullet count limits (WTI-007e) cover Story, Bug, Task, Enabler, and Feature. Sub-Tasks are not mentioned. The entity hierarchy allows Tasks to contain Sub-Tasks. Should Sub-Tasks have AC bullet limits?

**Recommendation:** Add Sub-Task limit (2 bullets) or explicitly state Sub-Tasks are exempt from WTI-007e.

#### Gap 3: No Retroactivity Guidance

The plan creates new rules but does not address existing work items. Will WTI-007 apply only to newly created items? Or should the wt-auditor flag existing items? The wt-auditor enhancement (TASK-008) will detect violations in existing items, but there is no guidance on whether remediation is required for historical items.

**Recommendation:** Add a decision or note in PLAN.md: "WTI-007/008 apply to newly created items. The wt-auditor will flag existing violations as INFO (advisory) to avoid a remediation avalanche."

#### Gap 4: No SPIKE Type in Bullet Count Limits

The entity hierarchy includes Spikes (research tasks), but WTI-007e does not define a bullet count limit for Spikes. Spikes have AC (research questions to answer).

**Recommendation:** Add Spike limit (3 bullets, same as Task) or explicitly exclude Spikes.

#### Gap 5: WTI-008 Scope -- Which Work Item Types Trigger Checkpoints?

WTI-008a says "before writing a work item file" and WTI-008 preamble says "work items that contain Acceptance Criteria." Discoveries, Decisions, and Impediments do not have AC. But the rule does not explicitly enumerate which types trigger WTI-008 checkpoints.

**Recommendation:** Add explicit list: "WTI-008 applies to: Story, Bug, Task, Enabler, Feature. Does NOT apply to: Discovery, Decision, Impediment, Sub-Task."

### 6. Dependency Chain Verification

#### Documented Dependency Chain

```
EN-001 --+---> EN-002 (guides reference the standards)
         +---> EN-003 (auditor enforces the standards)

TASK-001 ---> TASK-002 (WTI-007 references content-standards.md)
TASK-001 ---> TASK-003 (WTI-008 references content-standards.md)
TASK-002 ---> TASK-004..006 (guides enforce WTI-007 rules)
TASK-002 ---> TASK-008 (auditor detects WTI-007 violations)
TASK-001 ---> TASK-007 (SKILL.md loads content-standards.md)
```

#### Verification Results

| Dependency | Correct? | Issue |
|------------|----------|-------|
| TASK-001 -> TASK-002 | YES | TASK-002 references content-standards.md created by TASK-001 |
| TASK-001 -> TASK-003 | YES | TASK-003 references content-standards.md created by TASK-001 |
| TASK-002 -> TASK-004 | YES | BUG.md guide references WTI-007 rules from TASK-002 |
| TASK-002 -> TASK-005 | YES | STORY.md guide references WTI-007 rules from TASK-002 |
| TASK-002 -> TASK-006 | YES | TASK.md guide references WTI-007 rules from TASK-002 |
| TASK-002 -> TASK-008 | YES | Auditor detects WTI-007 violations defined in TASK-002 |
| TASK-001 -> TASK-007 | YES | SKILL.md loads content-standards.md from TASK-001 |
| EN-001 -> EN-002 | YES | Enabler-level dependency matches task-level dependencies |
| EN-001 -> EN-003 | YES | Enabler-level dependency matches task-level dependencies |

#### Missing Dependencies

| Missing Dependency | Reason | Severity |
|--------------------|--------|----------|
| **TASK-009 -> TASK-005** | TASK-005 AC states DoD section should reference DOD.md (created by TASK-009). TASK-005 cannot fully complete without TASK-009's output. | MAJOR |
| **TASK-003 -> TASK-007** | TASK-007 AC says "WTI-007 and WTI-008 added to WTI Rules Enforced table." TASK-007 depends on both TASK-002 (WTI-007) AND TASK-003 (WTI-008). Only TASK-001 is listed as dependency. | MAJOR |

#### Circular Dependencies

None detected. The dependency graph is a DAG (directed acyclic graph).

#### Ordering Recommendation

Based on the corrected dependency chain:

```
Phase A (Critical Path):
  TASK-001 (content-standards.md)
    |
    +---> TASK-002 (WTI-007)
    |       |
    +---> TASK-003 (WTI-008)
    |
    +---> TASK-007* (SKILL.md -- depends on TASK-002 AND TASK-003)

Phase B (Template Guides + DoD):
  TASK-009 (DOD.md -- no dependencies, can start in parallel with Phase A)
    |
    +---> TASK-005* (STORY.md guide + DoD reframe -- depends on TASK-002 AND TASK-009)

  TASK-002 ---> TASK-004 (BUG.md guide)
  TASK-002 ---> TASK-006 (TASK.md guide)

Phase C (Auditor):
  TASK-002 ---> TASK-008 (wt-auditor Phase 2.5)
```

*Items marked with `*` have corrected dependencies.

---

## L2 Strategic Assessment

### Architectural Fitness

The proposed changes fit well within Jerry's existing architecture:

1. **Layer separation is clean.** WTI-007 (content form) and WTI-008 (human review) occupy distinct layers in the quality gate model. Neither overlaps with the existing structural integrity layer (WTI-001-006).

2. **Extension pattern is correct.** Adding sub-rules under numbered WTI rules follows the established convention. The sub-rule pattern (WTI-007a through WTI-007g) is new to the worktracker but provides necessary granularity without inflating the top-level rule count.

3. **File organization is sound.** Separating the reference file (worktracker-content-standards.md) from the behavior rules file follows Jerry's existing pattern of behavior rules referencing detailed documentation elsewhere.

4. **Skill loading is appropriately scoped.** Loading content-standards.md via `@rules/` ensures it is available during worktracker operations but not at session start. This respects the context-rot mitigation strategy.

### Risk Areas for Implementation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Template modification breaks existing work items** | LOW | MEDIUM | Guides are PREPENDED; existing content unchanged. REFERENCE ONLY markers are additive. |
| **Checkpoint fatigue leads to universal skipping** | MEDIUM | MEDIUM | Already mitigated by two-checkpoint design (not four) and skip mechanism. Monitor skip rate via HTML comments. |
| **WTI-007b false positives on technical AC** | MEDIUM | LOW | Content-standards.md should include edge case examples. Auditor severity is WARNING, not ERROR. |
| **Ordering error during implementation** | MEDIUM | LOW | Corrected dependency chain (this review) addresses the two missing dependencies. |

### Recommendations for Ordering/Phasing

1. **Start TASK-009 (DOD.md) early.** It has no dependencies and is needed by TASK-005. Starting it in parallel with TASK-001 saves time.

2. **Complete TASK-002 and TASK-003 before TASK-007.** TASK-007 needs both WTI-007 and WTI-008 to update the SKILL.md rules table.

3. **TASK-008 (wt-auditor) should be last.** It is the most complex task (rated High) and depends on the rule definitions being stable. Implementing it after all rules and guides are complete reduces rework risk.

4. **Consider a "dry run" verification step** after Phase A completes: create a test work item using the new rules to validate the checkpoint flow before modifying templates.

---

## Findings Table

| ID | Severity | Category | Finding | Recommendation |
|----|----------|----------|---------|----------------|
| F-001 | MAJOR | WTI-008 Testability | WTI-008c ("Missing Information Flag") has no explicit rubric for "insufficient context." The threshold for triggering the flag is subjective, making it the least testable sub-rule. | Add 2-3 concrete examples to the rule definition: (1) "User says 'create a bug for the login issue' -- INSUFFICIENT: no symptom, steps, or location"; (2) "User says 'create a story for user profile editing' -- INSUFFICIENT: no role, goal, or benefit specified"; (3) "User provides detailed symptom with steps -- SUFFICIENT: proceed to creation." |
| F-002 | MAJOR | Dependency Chain | TASK-009 (DOD.md) is not listed as a dependency of TASK-005 (STORY.md + DoD reframe), but TASK-005 AC requires the DoD section to cross-reference DOD.md. TASK-009 AC also states "STORY.md DoD section (TASK-005) cross-references this file." | Add `TASK-009 -> TASK-005` to the dependency chain. Alternatively, make TASK-009 a prerequisite of TASK-005 explicitly. |
| F-003 | MAJOR | Dependency Chain | TASK-007 (SKILL.md update) lists only TASK-001 as dependency, but its AC requires "WTI-007 and WTI-008 added to WTI Rules Enforced table." WTI-008 is defined in TASK-003, which is not a dependency of TASK-007. | Add `TASK-003 -> TASK-007` to the dependency chain (alongside the existing TASK-001 -> TASK-007). |
| F-004 | MINOR | WTI-007 Testability | WTI-007c (Actor-First Format) does not account for Enabler/Feature/Task AC patterns that legitimately describe system-internal outcomes without a human or API actor (e.g., "Build pipeline produces artifacts", "Migration runs forward and backward"). | Add note to WTI-007c: "For Enablers, Features, and Tasks, the 'actor' may be a system component, infrastructure element, or process (e.g., 'Build pipeline...', 'Database migration...', 'Configuration file...')." |
| F-005 | MINOR | Conflict Analysis | WTI-007b prohibits implementation details in AC, but does not state where they DO belong. WTI-003 requires "accurate" state. Without guidance on where implementation details should go, there is a risk of information loss. | Add explicit guidance in content-standards.md: "Implementation details belong in the Description section, Implementation Notes section, or child Task descriptions -- never in AC." |
| F-006 | MINOR | Task AC Completeness | TASK-001 AC item "Contains Hemingway writing style directive" does not define what the Hemingway directive entails. | Expand AC to: "Contains Hemingway writing style directive (short sentences, active voice, concrete nouns, no adverbs, no hedge words)." |
| F-007 | MINOR | Task AC Completeness | TASK-001 AC item "Contains pre-finalization quality check (4 questions)" does not enumerate the 4 questions. The synthesis specifies 3 questions for WTI-008b, not 4. | Enumerate the 4 questions in the AC or reference the synthesis section where they are defined. Reconcile the count: are there 3 questions (from WTI-008b) or 4 (a different set for the content-standards file)? |
| F-008 | MINOR | Task AC Completeness | TASK-001 AC does not include a criterion for SPIDR splitting guide content, which the PLAN.md ("AC standards, concrete vs vague table, SPIDR splitting guide") lists as part of the content-standards file. | Add AC item: "Contains SPIDR splitting framework reference (Spike, Paths, Interfaces, Data, Rules) for scope overflow remediation." |
| F-009 | MINOR | Task AC Completeness | TASK-002 AC item "Compatible with existing WTI-001 through WTI-006 structure and formatting" is subjective. "Compatible" could mean many things. | Replace with: "Follows the same heading pattern (### WTI-NNN: Name (ENFORCEMENT)), table format, anti-pattern section, and 'Why' rationale as existing WTI-001 through WTI-006." |
| F-010 | INFO | Task AC Completeness | TASK-003 AC does not explicitly verify the HTML comment format `<!-- WTI-008: Checkpoint skipped by user -->` is defined in the WTI-008d rule text. This detail is in the synthesis but could be missed during implementation. | Consider adding: "WTI-008d rule text includes the exact HTML comment format for skip tracking." |
| F-011 | INFO | Task AC Completeness | TASK-009 (DOD.md) AC does not require the file to follow markdown-navigation-standards, unlike TASK-001 which explicitly requires it. | Add AC item: "Follows Jerry markdown-navigation-standards (Document Sections table with anchors)" or explicitly exempt short files (DOD.md may be under 30 lines). |
| F-012 | INFO | Task AC Completeness | TASK-008 AC lists detection patterns for WTI-007a, 007b, 007d, 007e, 007f but not WTI-007c (Actor-First Format). The severity table assigns actor-format as INFO. The omission appears intentional but is not explicit. | Add note to TASK-008 AC: "WTI-007c (Actor-First Format) excluded from automated detection patterns due to high false-positive risk; assigned INFO severity for manual review only." |
| F-013 | INFO | Task AC Completeness | The mapping from WTI rule enforcement level (HARD/MEDIUM) to auditor severity (ERROR/WARNING/INFO) is not documented. TASK-008 AC assigns severities but does not explain the mapping rationale. | Document the mapping: HARD + automated = WARNING, MEDIUM + automated = INFO, HARD + manual-only = not audited. This helps future rule additions. |
| F-014 | INFO | Gap Analysis | No bullet count limit defined for Sub-Tasks or Spikes. WTI-007e covers Story, Bug, Task, Enabler, Feature only. | Add limits for Sub-Task (2) and Spike (3), or explicitly exclude them from WTI-007e scope. |

---

## Review Methodology

This review was conducted by reading the following source documents:

1. **Existing rules:** `skills/worktracker/rules/worktracker-behavior-rules.md` (WTI-001 through WTI-006)
2. **Proposed rules:** `projects/PROJ-005-jerry-process-improvements/research/proj-005-s-001-content-quality-synthesis.md` (Consolidated Rule Set section)
3. **Task acceptance criteria:** `projects/PROJ-005-jerry-process-improvements/WORKTRACKER.md` (Task Details section)
4. **Implementation plan:** `projects/PROJ-005-jerry-process-improvements/PLAN.md` (Work Breakdown and Dependencies sections)
5. **SKILL.md:** `skills/worktracker/SKILL.md` (current state for TASK-007 baseline)
6. **wt-auditor.md:** `skills/worktracker/agents/wt-auditor.md` (current state for TASK-008 baseline)
7. **STORY.md template:** `.context/templates/worktracker/STORY.md` (DoD section lines 289-313)

The review applied six analysis categories:
1. Testability assessment for each WTI-007 sub-rule (a-g)
2. Testability assessment for each WTI-008 sub-rule (a-d)
3. Conflict analysis against WTI-001 through WTI-006
4. Acceptance criteria completeness for all 9 tasks
5. Gap analysis for missing requirements
6. Dependency chain verification

---

## References

### Source Documents

| Document | Path | Purpose in Review |
|----------|------|-------------------|
| Worktracker Behavior Rules | `c:\AI\jerry\skills\worktracker\rules\worktracker-behavior-rules.md` | WTI-001-006 conflict baseline |
| Research Synthesis | `c:\AI\jerry\projects\PROJ-005-jerry-process-improvements\research\proj-005-s-001-content-quality-synthesis.md` | Proposed WTI-007/008 definitions |
| WORKTRACKER.md | `c:\AI\jerry\projects\PROJ-005-jerry-process-improvements\WORKTRACKER.md` | Task AC under review |
| PLAN.md | `c:\AI\jerry\projects\PROJ-005-jerry-process-improvements\PLAN.md` | Dependency chain under review |
| SKILL.md | `c:\AI\jerry\skills\worktracker\SKILL.md` | TASK-007 baseline |
| wt-auditor.md | `c:\AI\jerry\skills\worktracker\agents\wt-auditor.md` | TASK-008 baseline |
| STORY.md template | `c:\AI\jerry\.context\templates\worktracker\STORY.md` | DoD section verification |

### Review Standards Applied

| Standard | Application |
|----------|-------------|
| NASA NPR 7123.1D (adapted) | Requirements review process, testability assessment, traceability verification |
| Jerry Constitution v1.0 | P-020 (User Authority) compliance check for WTI-008d |
| Jerry Coding Standards | Markdown navigation standards compliance check |

---

*Review completed: 2026-02-16*
*Reviewer: nse-reviewer v1.0.0*
*Project: PROJ-005, Entry: e-001*
*Verdict: PASS WITH FINDINGS (0 CRITICAL, 3 MAJOR, 6 MINOR, 5 INFO)*
