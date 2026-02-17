# PROJ-005-A-001: Worktracker Content Quality Gap Analysis

> **Type:** analysis
> **PS ID:** proj-005
> **Entry ID:** a-001
> **Topic:** Worktracker Content Quality Gap Analysis
> **Agent:** ps-analyst (v2.0.0)
> **Date:** 2026-02-16
> **Status:** Complete

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Key gaps identified, priority ranking |
| [L1 Detailed Gap Analysis](#l1-detailed-gap-analysis) | Per-area analysis with file locations and line numbers |
| [L2 Architectural Fit](#l2-architectural-fit) | How changes fit Jerry's rule system and hexagonal architecture |
| [Recommendations](#recommendations) | Prioritized action items |

---

## L0 Executive Summary

### Critical Finding

Jerry's worktracker has strong **structural integrity** rules (WTI-001 through WTI-006) but **zero content quality** rules. The system enforces *that* files exist and *that* status is correct, but never enforces *what is written inside them*. This is the root cause of the recurring "wall of text" and "implementation details in AC" complaints documented in `LEARNINGS.md` and the feedback document.

### Top 5 Gaps (Priority Order)

| # | Gap | Severity | Impact |
|---|-----|----------|--------|
| 1 | **No Acceptance Criteria content quality rule** | Critical | AC contains DoD items, implementation details, vague language. Engineers cannot build from it. |
| 2 | **No content brevity/readability rule** | High | Templates produce "wall of text" output. Devs rewrite from scratch rather than read AI output. |
| 3 | **No collaboration checkpoint before creation** | High | Claude proceeds without validating understanding. User feedback #3: "not enough back-and-forth." |
| 4 | **Templates are 80% ontology reference, 20% creation guidance** | Medium | BUG.md is 467 lines. Claude reads all of it but only needs ~50 lines to create a good bug. |
| 5 | **wt-auditor checks structure but not content** | Medium | Auditor can detect missing AC section but cannot detect "all tests pass" inside AC. |

### Gap Category Summary

| Category | Current WTI Rules | ADO Skill Coverage | Gap |
|----------|-------------------|-------------------|-----|
| State integrity | WTI-001 to WTI-006 | N/A (different domain) | None |
| Content quality | None | AC standards, brevity rules, anti-pattern list | **Complete gap** |
| Collaboration | None | Approval process, quality check questions | **Complete gap** |
| Readability | None | Length constraints, Hemingway style directive | **Complete gap** |

---

## L1 Detailed Gap Analysis

### Area 1: WTI Rule Gap Analysis

#### Current WTI Rules (WTI-001 through WTI-006)

**Source:** `c:\AI\jerry\skills\worktracker\rules\worktracker-behavior-rules.md` (lines 27-113)

| Rule | Focus | What It Enforces |
|------|-------|------------------|
| WTI-001 | State timeliness | Status updated immediately after work |
| WTI-002 | Closure verification | AC verified + evidence before DONE |
| WTI-003 | State truthfulness | Status reflects reality |
| WTI-004 | State synchronization | Read current state before reporting |
| WTI-005 | Atomic updates | Parent + child updated together |
| WTI-006 | Evidence-based closure | Evidence section populated before closure |

**Observation:** All six rules focus on **operational state management** -- when to update, what to verify before closing, how to keep parent-child in sync. None address *what goes into the content fields* (Summary, AC, Description).

#### What the ADO Skill Enforces That WTI Rules Do Not

**Source:** `C:\Users\TZimmerman\.claude\skills\ado\SKILL.md` (lines 112-158)
**Source:** `C:\Users\TZimmerman\.claude\skills\ado\references\acceptance-criteria-standards.md` (full file)

| ADO Skill Enforcement | Worktracker Equivalent | Gap? |
|------------------------|------------------------|------|
| AC maximum bullet counts (Features: 5, PBIs: 4, Bugs: 3) | None | **YES** |
| "AC must not contain DoD items" (test coverage, code review, docs) | None | **YES** |
| Vague language prohibition ("should be able to", "might need to") | None | **YES** |
| Actor-first AC format ("Admin can...", "System validates...") | None | **YES** |
| Description brevity (2-3 sentences for PBIs, 1-2 for Bugs) | None | **YES** |
| "No file paths or code references" in content | None | **YES** |
| "No technical architecture decisions" in content | None | **YES** |
| Hemingway-style writing directive | None | **YES** |
| Quality check questions before finalizing | None | **YES** |
| Concrete vs vague examples table | None | **YES** |
| "If you need more bullets, the scope is too large -- split it" | None | **YES** |

#### Proposed New Rules

**WTI-007: Content Quality Standards (HARD)**

**Rule:** All work item content (Summary, Acceptance Criteria, Description) MUST meet content quality standards.

| Sub-Rule | Enforcement | Detail |
|----------|-------------|--------|
| WTI-007a | AC must not contain Definition of Done items | Reject: "tests pass", "code reviewed", "documentation updated", "deployed to staging" |
| WTI-007b | AC must not contain implementation details | Reject: file paths, class names, method names, architecture decisions |
| WTI-007c | AC must use actor-first format | Require: "User can...", "System validates...", "API returns..." |
| WTI-007d | AC must not use hedge words | Reject: "should be able to", "might need to", "could potentially" |
| WTI-007e | AC bullet count limits | Story: max 5, Bug: max 3, Task: max 3, Enabler: max 5 |
| WTI-007f | Summary must be 1-3 sentences | Reject summaries > 3 sentences or summaries that are implementation-focused |
| WTI-007g | Scope overflow signal | If AC exceeds bullet limit, flag that work item scope is too large -- recommend splitting |

**Anti-Pattern Examples (to include in rule definition):**

```markdown
# BAD AC (violates WTI-007a, WTI-007b):
- [ ] Update AssetTypeRepository.cs to add new method
- [ ] All unit tests pass with 90%+ coverage
- [ ] Code reviewed and approved
- [ ] Documentation updated

# GOOD AC (compliant):
- [ ] Admin can create a new asset type from the Asset Management page
- [ ] System validates asset type name is unique within the tenant
- [ ] API returns 409 Conflict when duplicate name is submitted
```

**WTI-008: Collaboration Before Creation (HARD)**

**Rule:** Claude MUST validate understanding with the user before creating work items that contain Acceptance Criteria (Stories, Bugs, Enablers).

| Sub-Rule | Enforcement | Detail |
|----------|-------------|--------|
| WTI-008a | Pre-creation checkpoint | Before writing the file, present a summary of what will be created and ask for confirmation |
| WTI-008b | AC review checkpoint | After drafting AC, present it to the user and ask: "Can an engineer build this without asking questions?" |
| WTI-008c | Missing information flag | If the user has not provided enough context to write specific AC, Claude MUST ask for clarification rather than generating vague AC |
| WTI-008d | Skip mechanism | User can say "skip" or "just create it" to bypass checkpoints, but Claude must acknowledge the quality risk |

---

### Area 2: Template Effectiveness Analysis

#### BUG.md (467 lines)

**Source:** `c:\AI\jerry\.context\templates\worktracker\BUG.md`

| Content Category | Lines | % of Template | Needed During Creation? |
|------------------|-------|---------------|------------------------|
| HTML comments (ontology references, design rationale) | ~95 | 20% | No |
| Frontmatter YAML schema reference | 55 (lines 103-158) | 12% | Partial (field names yes, comments no) |
| Template Structure diagram | 28 (lines 67-97) | 6% | No (redundant with actual sections) |
| State Machine Reference | 27 (lines 350-377) | 6% | No (reference only) |
| Containment Rules | 10 (lines 380-392) | 2% | No (reference only) |
| Invariants | 8 (lines 395-406) | 2% | Marginal |
| Severity Guide | 9 (lines 409-417) | 2% | Yes |
| System Mapping | 8 (lines 435-446) | 2% | No |
| Design Rationale footer | 17 (lines 449-466) | 4% | No |
| **Actual creation-relevant content** | ~220 | **47%** | **Yes** |

**Key Problem:** Over half the template is ontology reference material that Claude reads but does not need during the act of creating a bug. The creation-relevant sections are: Header block, Summary, Reproduction Steps, Environment, Evidence, Root Cause Analysis, Fix Description, Acceptance Criteria, History.

**Missing Content Quality Guidance:**
- No guidance on what makes a good bug summary (brevity, symptom-focused)
- No guidance on AC quality for bugs (the template just has placeholder checkboxes)
- No anti-patterns section showing what NOT to write
- No length limits on any section

**Proposed Quick Creation Guide for BUG.md:**

```markdown
## Quick Creation Guide

When creating a new bug, focus on these sections only:
1. **Header Block** - Fill in type, status, priority, severity, parent, created date
2. **Summary** - 1-2 sentences describing the symptom. NOT the root cause.
3. **Reproduction Steps** - 4-6 numbered steps maximum. Include Expected vs Actual.
4. **Environment** - Fill in the table with relevant environment details.
5. **Acceptance Criteria** - Maximum 3 bullets. Actor/system-first format.
   - MUST describe observable fix behavior, NOT implementation steps
   - BAD: "Update validation logic in FormValidator.cs"
   - GOOD: "System rejects empty email field with error 'Email is required'"

All other sections (Root Cause, Fix Description, Evidence) are populated
AFTER investigation/fix, not at creation time.
```

#### STORY.md (492 lines)

**Source:** `c:\AI\jerry\.context\templates\worktracker\STORY.md`

| Content Category | Lines | % of Template | Needed During Creation? |
|------------------|-------|---------------|------------------------|
| HTML comments (ontology references) | ~80 | 16% | No |
| Frontmatter YAML schema reference | 54 (lines 103-156) | 11% | Partial |
| Template Structure diagram | 35 (lines 44-75) | 7% | No |
| Document Sections nav table | 18 (lines 79-98) | 4% | Marginal |
| State Machine Reference | 25 (lines 348-374) | 5% | No |
| Containment Rules + Hierarchy Diagram | 22 (lines 378-400) | 4% | No |
| Invariants | 13 (lines 404-416) | 3% | No |
| System Mapping | 11 (lines 458-468) | 2% | No |
| Design Rationale footer | 22 (lines 472-491) | 4% | No |
| Estimation section | 15 (lines 272-286) | 3% | No (populated later) |
| Definition of Done section | 18 (lines 289-313) | 4% | Problematic (see below) |
| **Actual creation-relevant content** | ~200 | **41%** | **Yes** |

**Critical Problem -- Definition of Done in Template:**
Lines 289-313 contain a "Definition of Done" section with checkboxes like "Code complete and peer reviewed", "Unit tests written and passing", "Integration tests passing". This is the *exact* content that the ADO AC standards say does NOT belong in individual work items. It belongs in the team's shared DoD. Having it in the template teaches Claude to conflate AC with DoD.

**Missing Content Quality Guidance:**
- No guidance on AC quality (the Gherkin section at lines 197-206 is fine structurally but has no quality constraints)
- No maximum AC bullet count
- No "what is NOT acceptance criteria" guidance
- No anti-patterns section
- User Story format (As a / I want / So that) is RECOMMENDED but no guidance on what makes it good or bad

**Proposed Quick Creation Guide for STORY.md:**

```markdown
## Quick Creation Guide

When creating a new story, focus on these sections only:
1. **Header Block** - Fill in type, status, priority, parent feature, created date
2. **User Story** - "As a [role], I want [goal], So that [benefit]"
   - Role must be a specific user type, NOT "a user"
   - Goal must be an observable action, NOT an implementation task
   - Benefit must explain business value, NOT technical value
3. **Summary** - 2-3 sentences of additional context. Scope bullets.
4. **Acceptance Criteria** - Maximum 5 bullets. Actor/system-first format.
   - MUST describe user-observable outcomes
   - MUST NOT contain: test requirements, code review, documentation, deployment
   - Those items belong in the team's Definition of Done, not here
   - BAD: "Unit tests written and passing"
   - GOOD: "User sees confirmation toast after saving changes"
5. **Children (Tasks)** - Leave empty initially; populate during task breakdown

DO NOT populate: Definition of Done (team-level), Estimation (sprint planning),
Evidence (at completion), State Machine (reference only).
```

#### TASK.md (252 lines)

**Source:** `c:\AI\jerry\.context\templates\worktracker\TASK.md`

| Content Category | Lines | % of Template | Needed During Creation? |
|------------------|-------|---------------|------------------------|
| HTML comments | ~20 | 8% | No |
| Frontmatter YAML schema reference | 58 (lines 36-94) | 23% | Partial |
| State Machine diagram + table | 43 (lines 98-141) | 17% | No |
| Containment Rules | 10 (lines 144-153) | 4% | No |
| Invariants | 8 (lines 158-165) | 3% | No |
| System Mapping | 8 (lines 170-177) | 3% | No |
| Design Rationale footer | 10 (lines 243-251) | 4% | No |
| **Actual creation-relevant content** | ~95 | **38%** | **Yes** |

**Observation:** Task template is the most compact (252 lines vs 467/492) but still only 38% creation-relevant. The Content section (lines 180-200) is where the actual creation happens, and it is extremely sparse -- just placeholder variables with no quality guidance.

**Missing Content Quality Guidance:**
- No guidance on task description quality
- No guidance on task AC quality or limits (3 bullets max would be appropriate)
- No guidance that task AC should be verification-oriented ("verify X works") not implementation-oriented ("implement X")
- No anti-patterns

**Proposed Quick Creation Guide for TASK.md:**

```markdown
## Quick Creation Guide

When creating a new task, focus on:
1. **Header** - ID, title, status, parent, created date
2. **Description** - 1-2 sentences: what needs to be done and why
3. **Acceptance Criteria** - Maximum 3 bullets. Verification-oriented.
   - BAD: "Implement the repository pattern for asset types"
   - GOOD: "Asset types can be created, read, updated, and deleted via the API"
4. **Implementation Notes** - Technical details belong HERE, not in AC

DO NOT populate: Time Tracking (estimated during sprint), Evidence (at completion).
```

---

### Area 3: ADO Skill Pattern Extraction

Every pattern from the ADO skill and its AC standards reference that should become a worktracker rule, mapped to specific rules.

#### Content Generation Patterns (ADO SKILL.md lines 112-133)

| ADO Pattern | Source Line | Proposed WTI Mapping |
|-------------|-------------|---------------------|
| "Write brief, user-focused descriptions" | SKILL.md:114 | WTI-007f (summary brevity) |
| "Emulate Ernest Hemingway's concise and direct writing style" | SKILL.md:114 | WTI-007 preamble (writing style) |
| PBI Description: "2-3 sentences explaining the feature or change from a user perspective" | SKILL.md:121 | WTI-007f (summary length limits) |
| Bug Description: "1-2 sentences explaining the issue" | SKILL.md:125 | WTI-007f (bug summary limit) |
| "Repro Steps: 4-6 numbered steps maximum" | SKILL.md:126 | New sub-rule or bug-specific guidance in Quick Creation Guide |
| AC Maximum bullets: Features 5, PBIs 4, Bugs 3 | SKILL.md:118,122,128 | WTI-007e (bullet count limits) |
| "Do not include: File paths or code references" | SKILL.md:131 | WTI-007b (no implementation details) |
| "Do not include: Technical architecture decisions" | SKILL.md:132 | WTI-007b (no implementation details) |
| "Do not include: Implementation approach details" | SKILL.md:133 | WTI-007b (no implementation details) |

#### Acceptance Criteria Patterns (acceptance-criteria-standards.md)

| ADO Pattern | Source Line | Proposed WTI Mapping |
|-------------|-------------|---------------------|
| "#1 rule: If engineers/UX/QA need to ask clarifying questions, the AC has failed" | AC-standards:1-5 | WTI-007 preamble (clarity principle) |
| "Bullet points, 1 sentence per criterion" | AC-standards:10 | WTI-007c (format requirement) |
| "Start with actor or system" | AC-standards:12 | WTI-007c (actor-first format) |
| "No hedge words" | AC-standards:13 | WTI-007d (hedge word prohibition) |
| "If you need more bullets than the limit, the work item scope is too large" | AC-standards:20 | WTI-007g (scope overflow signal) |
| "NOT AC: Test coverage requirements" | AC-standards:25 | WTI-007a (DoD exclusion) |
| "NOT AC: Code review completion" | AC-standards:26 | WTI-007a (DoD exclusion) |
| "NOT AC: Documentation updates" | AC-standards:27 | WTI-007a (DoD exclusion) |
| "NOT AC: Deployment verification" | AC-standards:28 | WTI-007a (DoD exclusion) |
| "NOT AC: Performance baselines (unless specifically about performance)" | AC-standards:29 | WTI-007a (DoD exclusion, with exception) |
| "NOT AC: Implementation details (specific classes, methods, patterns)" | AC-standards:30 | WTI-007b (no implementation details) |
| "If it applies to every work item equally, it's a definition of done -- not acceptance criteria" | AC-standards:32 | WTI-007a (universal test) |
| Concrete vs Vague table (6 examples) | AC-standards:83-93 | WTI-007 reference examples |
| Anti-patterns list (5 examples) | AC-standards:96-100 | WTI-007 anti-pattern list |
| Quality check: "Can an engineer build this without asking questions?" | AC-standards:104 | WTI-008b (AC review checkpoint) |
| Quality check: "Can QA write test cases from this description?" | AC-standards:106 | WTI-008b (AC review checkpoint) |
| Quality check: "Are there any ambiguous terms remaining?" | AC-standards:108 | WTI-008b (AC review checkpoint) |

#### Auditing Patterns (ADO SKILL.md lines 160-166)

| ADO Pattern | Source Line | Proposed WTI Mapping |
|-------------|-------------|---------------------|
| "Systematic field-by-field review" | SKILL.md:162 | wt-auditor enhancement (content audit phase) |
| "Check EVERY field against the identified issue" | SKILL.md:163 | wt-auditor enhancement |
| "Don't mark audit complete until ALL fields reviewed" | SKILL.md:164 | wt-auditor enhancement |
| "Report findings per field" | SKILL.md:165 | wt-auditor report format enhancement |

---

### Area 4: Collaboration Checkpoint Design

**Sources:**
- `C:\Users\TZimmerman\Downloads\jerry-process-feedback-2026-02-11 (1).md` (items #1, #3, #4, #7)
- `c:\AI\ClaudeDevelopment\skills\LEARNINGS.md` (entries: 2026-02-10 "AC Contains Implementation Details", 2026-02-04 "AC Caused Confusion", 2026-02-04 "Epic Defined Problem Too Narrowly")

#### Checkpoint 1: Story Creation Pre-Check

**When:** Immediately before Claude starts writing a Story file (after the user says "create a story" or equivalent).

**Question:**
```
Before I create this story, let me confirm my understanding:

**User Role:** [extracted or "unclear -- please specify"]
**Goal:** [extracted or "unclear -- please specify"]
**Benefit:** [extracted or "unclear -- please specify"]
**Parent Feature:** [extracted or "not specified"]

Does this capture the intent? Any corrections?

(Recommended) Proceed with corrections
Skip -- create with what you have
```

**If user says "skip":** Claude creates the story but adds an HTML comment: `<!-- WTI-008: Pre-creation checkpoint skipped by user -->` and sets a lower confidence level on the AC.

#### Checkpoint 2: Bug Creation Pre-Check

**When:** Immediately before Claude starts writing a Bug file.

**Question:**
```
Before I create this bug report, let me confirm:

**Symptom:** [1 sentence]
**Where it occurs:** [page/API/component]
**Severity assessment:** [critical/major/minor/trivial] -- [rationale]
**Parent:** [extracted or "not specified"]

Is this accurate? Anything to add or correct?

(Recommended) Proceed with corrections
Skip -- create with what you have
```

**If user says "skip":** Same treatment as Checkpoint 1.

#### Checkpoint 3: AC Review (for Stories, Bugs, Enablers)

**When:** After Claude drafts the Acceptance Criteria but BEFORE writing the file.

**Question:**
```
Here are the acceptance criteria I've drafted:

- [ ] [AC item 1]
- [ ] [AC item 2]
- [ ] [AC item 3]

Quality check:
1. Can an engineer build this without asking questions?
2. Can QA write test cases from these criteria?
3. Are there any ambiguous terms?

(Recommended) Review and adjust
Approve as-is
Skip AC for now -- I'll add it later
```

**If user says "skip":** Claude creates the work item with an empty AC section and adds: `<!-- WTI-008: AC checkpoint skipped. AC required before in_progress (INV-ST03). -->`

#### Checkpoint 4: Scope Overflow Warning

**When:** When Claude's drafted AC exceeds the maximum bullet count for the work item type.

**Question:**
```
I've drafted [N] acceptance criteria, which exceeds the [MAX] limit for [TYPE].
This usually means the scope is too large. Options:

(Recommended) Split into multiple [TYPE]s -- I'll help you decompose
Trim to [MAX] most important criteria
Proceed anyway with [N] criteria (not recommended)
```

**Implementation Note:** The "(Recommended)" tag addresses feedback item #7 from the feedback document (line 122-124): "When presenting options to the user, mark the recommended choice."

---

### Area 5: wt-auditor Enhancement Specification

**Source:** `c:\AI\jerry\skills\worktracker\agents\wt-auditor.md`

The current wt-auditor (v1.0.0) has 5 audit check types (lines 79-121):
1. Template compliance (structural sections present)
2. Relationship integrity (parent-child links)
3. Orphan detection (unreachable files)
4. Status consistency (parent-child status alignment)
5. ID format (naming conventions)

**What is missing:** A **Phase 2.5: Content Quality Check** that sits between template compliance (Phase 2) and relationship integrity (Phase 3).

#### Proposed New Audit Check Type: Content Quality (severity: warning)

```yaml
content_quality:
  description: "Verify work item content meets quality standards (WTI-007)"
  severity: "warning"
  checks:
    - "AC does not contain Definition of Done items"
    - "AC does not contain implementation details"
    - "AC uses actor-first format"
    - "AC does not exceed bullet count limits"
    - "Summary meets length constraints"
    - "No hedge words in AC"
```

#### Specific Detection Patterns

**1. DoD Items in AC (WTI-007a violation)**

Detect checklist items that match common DoD patterns:

```
Regex patterns (case-insensitive, applied to AC section content):
- /\b(unit\s+)?tests?\s+(pass|written|passing|complete|added)\b/i
- /\bcode\s+review(ed)?\b/i
- /\bdocumentation\s+updated\b/i
- /\bdeployed?\s+to\s+(staging|production|dev)\b/i
- /\bcoverage\s+(meets?|above|>\s*\d+%)\b/i
- /\bintegration\s+tests?\s+(pass|passing)\b/i
- /\bQA\s+(sign-?off|testing\s+complete)\b/i
- /\bpeer\s+review(ed)?\b/i
- /\bno\s+(critical\s+)?bugs?\s+remaining\b/i
```

**2. Implementation Details in AC (WTI-007b violation)**

Detect file paths, class names, method patterns:

```
Regex patterns (applied to AC section content):
- /\b\w+\.(cs|py|ts|js|java|go|rs|md)\b/          # File extensions
- /\b(src|lib|app|components|services|controllers)\//  # Path fragments
- /\b[A-Z][a-z]+[A-Z]\w+\b/                          # PascalCase identifiers (likely class names)
- /\b(implement|refactor|migrate|update)\s+(the\s+)?\w+(Service|Repository|Controller|Handler|Manager|Factory)\b/i  # Implementation verbs + class names
- /\b(async|await|Task<|Promise<|Observable<)\b/      # Code patterns
- /\busing\s+(the\s+)?(repository|adapter|pattern|strategy)\s+pattern\b/i  # Architecture patterns
```

**3. Hedge Words in AC (WTI-007d violation)**

```
Regex patterns (applied to AC section content):
- /\bshould\s+be\s+able\s+to\b/i
- /\bmight\s+need\s+to\b/i
- /\bcould\s+potentially\b/i
- /\bpossibly\b/i
- /\bif\s+possible\b/i
- /\bideally\b/i
- /\bas\s+needed\b/i
- /\bwhen\s+appropriate\b/i
- /\bin\s+most\s+cases\b/i
```

**4. AC Bullet Count (WTI-007e violation)**

```python
# Count lines matching checkbox pattern in AC section
ac_bullets = re.findall(r'^\s*-\s*\[[ x]\]', ac_section_content, re.MULTILINE)
count = len(ac_bullets)

# Limits by entity type:
limits = {
    'STORY': 5,
    'BUG': 3,
    'TASK': 3,
    'ENABLER': 5,
    'FEATURE': 5,
}

if count > limits.get(entity_type, 5):
    report_warning(f"AC has {count} bullets, exceeds {limits[entity_type]} limit for {entity_type}")
```

**5. Summary Length (WTI-007f violation)**

```python
# Extract summary section content (between ## Summary and next ##)
summary_text = extract_section('Summary', file_content)

# Count sentences (rough: split on '. ' or '.\n')
sentences = re.split(r'(?<=[.!?])\s+', summary_text.strip())
sentences = [s for s in sentences if len(s) > 10]  # filter noise

if len(sentences) > 3:
    report_warning(f"Summary has {len(sentences)} sentences, maximum is 3")
```

**6. Actor-First AC Format (WTI-007c violation)**

```
Regex pattern for GOOD AC (should match):
- /^\s*-\s*\[[ x]\]\s*(User|Admin|System|API|Service|Manager|Operator|Customer)\s+(can|validates?|returns?|displays?|sends?|rejects?|logs?|creates?|updates?|deletes?)\b/i

If a bullet does NOT match this pattern, flag as INFO (not error -- too strict for error).
```

#### Updated Audit Workflow

Insert between current Phase 2 (Template Compliance) and Phase 3 (Relationship Integrity):

```markdown
### Phase 2.5: Content Quality Check (NEW)
1. For each file with an Acceptance Criteria section:
   a. Extract AC section content
   b. Run DoD detection patterns -- flag matches as WARNING
   c. Run implementation detail patterns -- flag matches as WARNING
   d. Run hedge word patterns -- flag matches as WARNING
   e. Count AC bullets -- flag over-limit as WARNING
   f. Check actor-first format -- flag non-conforming as INFO
2. For each file with a Summary section:
   a. Extract summary content
   b. Count sentences -- flag over-limit as WARNING
3. Log all violations with:
   - File path
   - Line number (approximate)
   - Matched text
   - Which WTI-007 sub-rule was violated
   - Suggested remediation
```

#### Updated Audit Report Format

Add a new subsection under "Issues Found":

```markdown
### Content Quality Issues

| ID | File | Sub-Rule | Matched Text | Remediation |
|----|------|----------|--------------|-------------|
| CQ-001 | ST-001-login.md | WTI-007a (DoD in AC) | "Unit tests written and passing" | Move to team DoD; replace with user-observable outcome |
| CQ-002 | EN-003-api.md | WTI-007b (Impl detail) | "Update AssetRepository.cs" | Rewrite as: "Assets can be persisted and retrieved" |
| CQ-003 | BUG-002-crash.md | WTI-007d (Hedge word) | "should be able to" | Replace with direct statement: "User can..." |
| CQ-004 | ST-002-export.md | WTI-007e (Bullet count) | 7 bullets (max: 5) | Split story or consolidate criteria |
```

---

## L2 Architectural Fit

### How These Changes Map to Jerry's Rule System

Jerry's rule system follows a hierarchical loading pattern:

```
CLAUDE.md (root)
  -> skills/worktracker/SKILL.md (skill definition)
    -> skills/worktracker/rules/worktracker-behavior-rules.md (auto-loaded via @rules)
    -> skills/worktracker/rules/worktracker-templates.md (reference)
    -> skills/worktracker/rules/worktracker-entity-hierarchy.md (reference)
    -> skills/worktracker/agents/wt-auditor.md (agent definition)
  -> .context/templates/worktracker/*.md (templates)
```

#### Where WTI-007 and WTI-008 Should Live

| Artifact | Location | Rationale |
|----------|----------|-----------|
| WTI-007 rule definition | `skills/worktracker/rules/worktracker-behavior-rules.md` | Extends existing WTI rules in the same file |
| WTI-008 rule definition | `skills/worktracker/rules/worktracker-behavior-rules.md` | Same file, same enforcement pattern |
| AC quality reference (anti-patterns, examples) | `skills/worktracker/rules/worktracker-content-quality.md` (NEW) | Separate file to avoid bloating behavior-rules.md. Loaded on-demand, not auto-loaded. |
| Quick Creation Guides | Prepended to each template (BUG.md, STORY.md, TASK.md) | Must be the FIRST thing Claude reads when opening the template |
| wt-auditor content checks | `skills/worktracker/agents/wt-auditor.md` | Extend existing audit_checks section |

#### Hexagonal Architecture Alignment

The worktracker skill operates at the **interface layer** (it is a Claude Code skill, which is a primary adapter). The rules are **application-layer concerns** (they define use-case behavior). The templates are **domain-layer schemas** (they define the structure of work item aggregates).

| Change | Layer | Justification |
|--------|-------|---------------|
| WTI-007/WTI-008 rules | Application | Use-case validation rules for work item creation |
| Quick Creation Guides | Interface | Adapter-specific guidance for how Claude interacts with templates |
| Content quality regex patterns | Infrastructure (wt-auditor) | Technical detection logic for content analysis |
| Collaboration checkpoints | Interface | User interaction pattern at the CLI/agent boundary |

This layering is clean: rules define *what*, guides define *how for Claude*, and the auditor provides *automated detection infrastructure*.

#### Template Refactoring Strategy

The templates should NOT be split or restructured (that would break template compliance checks in the wt-auditor). Instead:

1. **Prepend** a Quick Creation Guide section at the top of each template, between the HTML comment header and the Document Sections nav table
2. **Mark** ontology reference sections with `<!-- REFERENCE ONLY: Skip during creation -->` comments
3. **Remove** the Definition of Done section from STORY.md (lines 289-313) or reframe it as a "Team DoD Reference" with explicit note that these items do NOT go in individual work item AC

---

## Recommendations

### Priority 1 (Immediate -- blocks quality)

| # | Action | Effort | Files to Modify |
|---|--------|--------|-----------------|
| R-1 | **Define WTI-007 (Content Quality Standards)** in `worktracker-behavior-rules.md` | Medium | `skills/worktracker/rules/worktracker-behavior-rules.md` |
| R-2 | **Create `worktracker-content-quality.md`** reference file with anti-patterns, examples, AC standards | Medium | `skills/worktracker/rules/worktracker-content-quality.md` (NEW) |
| R-3 | **Add Quick Creation Guides** to BUG.md, STORY.md, TASK.md templates | Low | `.context/templates/worktracker/BUG.md`, `STORY.md`, `TASK.md` |

### Priority 2 (High -- addresses user feedback)

| # | Action | Effort | Files to Modify |
|---|--------|--------|-----------------|
| R-4 | **Define WTI-008 (Collaboration Before Creation)** in `worktracker-behavior-rules.md` | Medium | `skills/worktracker/rules/worktracker-behavior-rules.md` |
| R-5 | **Remove/reframe Definition of Done section** in STORY.md template | Low | `.context/templates/worktracker/STORY.md` |
| R-6 | **Update SKILL.md** to reference WTI-007, WTI-008, and new content quality file | Low | `skills/worktracker/SKILL.md` |

### Priority 3 (Medium -- automation)

| # | Action | Effort | Files to Modify |
|---|--------|--------|-----------------|
| R-7 | **Add Content Quality audit phase** to wt-auditor agent | High | `skills/worktracker/agents/wt-auditor.md` |
| R-8 | **Add `(Recommended)` tag support** to collaboration checkpoints | Low | Covered by WTI-008 rule definition |
| R-9 | **Add Quick Creation Guides** to ENABLER.md and FEATURE.md templates | Low | `.context/templates/worktracker/ENABLER.md`, `FEATURE.md` |

### Priority 4 (Low -- reference improvements)

| # | Action | Effort | Files to Modify |
|---|--------|--------|-----------------|
| R-10 | **Add `<!-- REFERENCE ONLY -->` markers** to ontology sections in all templates | Low | All `.context/templates/worktracker/*.md` files |
| R-11 | **Update wt-auditor report format** with Content Quality Issues section | Low | `skills/worktracker/agents/wt-auditor.md` |

### Dependency Graph

```
R-1 (WTI-007) ──┬──> R-2 (content-quality.md reference file)
                 ├──> R-3 (Quick Creation Guides in templates)
                 ├──> R-5 (Remove DoD from STORY.md)
                 └──> R-7 (wt-auditor content checks)

R-4 (WTI-008) ──┬──> R-8 (Recommended tag support)
                 └──> R-6 (SKILL.md update)

R-3 ────────────> R-9 (Extend to ENABLER.md, FEATURE.md)
R-7 ────────────> R-11 (Audit report format)
```

**Critical Path:** R-1 -> R-2 -> R-3 (enables content quality enforcement from rules through templates)

---

## Sources and Citations

| Source | Path | Key Lines Referenced |
|--------|------|---------------------|
| WTI Rules | `c:\AI\jerry\skills\worktracker\rules\worktracker-behavior-rules.md` | 27-113 (WTI-001 through WTI-006) |
| Worktracker SKILL.md | `c:\AI\jerry\skills\worktracker\SKILL.md` | 39-123 (capabilities, WTI rules enforced) |
| BUG template | `c:\AI\jerry\.context\templates\worktracker\BUG.md` | 310-328 (AC section), 449-466 (design rationale) |
| STORY template | `c:\AI\jerry\.context\templates\worktracker\STORY.md` | 189-213 (AC section), 289-313 (DoD section) |
| TASK template | `c:\AI\jerry\.context\templates\worktracker\TASK.md` | 180-200 (Content section) |
| ADO Skill | `C:\Users\TZimmerman\.claude\skills\ado\SKILL.md` | 112-158 (content generation, AC standards) |
| AC Standards | `C:\Users\TZimmerman\.claude\skills\ado\references\acceptance-criteria-standards.md` | Full file (111 lines) |
| Feedback Document | `C:\Users\TZimmerman\Downloads\jerry-process-feedback-2026-02-11 (1).md` | Items #1, #3, #4, #7 |
| LEARNINGS | `c:\AI\ClaudeDevelopment\skills\LEARNINGS.md` | Lines 21-55 (2026-02-10 entries) |
| wt-auditor | `c:\AI\jerry\skills\worktracker\agents\wt-auditor.md` | 79-121 (audit_checks), 409-460 (audit workflow) |
| Template Rules | `c:\AI\jerry\skills\worktracker\rules\worktracker-templates.md` | 45-98 (template usage rules) |
| Entity Hierarchy | `c:\AI\jerry\skills\worktracker\rules\worktracker-entity-hierarchy.md` | 99-113 (containment rules matrix) |

---

*Analysis Version: 1.0.0*
*Agent: ps-analyst v2.0.0*
*Created: 2026-02-16*
*PS ID: proj-005, Entry: a-001*
