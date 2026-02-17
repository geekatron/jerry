# PROJ-005: Work Item Quality Improvements (Bugs, PBIs, Tasks)

> **Project:** PROJ-005-jerry-process-improvements
> **Status:** ACTIVE
> **Phase:** Implementation Planning (Research Complete)
> **Created:** 2026-02-16
> **Owner:** Tyler Zimmerman

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Problem statement and background |
| [Root Problem](#root-problem) | Core issue identified through research |
| [Research Findings](#research-findings) | Key findings from ps-researcher and ps-analyst |
| [Implementation Plan](#implementation-plan) | Consolidated changes with dependencies |
| [Work Breakdown](#work-breakdown) | Epic → Enabler → Task decomposition |
| [Verification](#verification) | How to validate the changes work |
| [Source Documents](#source-documents) | All referenced materials |

---

## Context

Tyler's ADO work items (Bugs, PBIs, Tasks) created across multiple sessions had recurring quality issues: missing or vague Acceptance Criteria, implementation details bleeding into AC, "wall of text" descriptions, and insufficient user collaboration before creation. These problems were validated through:

- **Sprint planning feedback** (LEARNINGS.md) -- 7 documented issues
- **Adam Nowak conversation** (Jerry.vtt) -- framework design intent
- **23 session analysis** (calm-stargazing-biscuit) -- recurring patterns
- **7 feedback themes** (jerry-process-feedback-2026-02-11.md)

**Focused Goal:** Fix work item creation quality for Bugs, PBIs (Stories), and Tasks -- the items engineers actually implement from.

**Target:** Jerry's worktracker (local rules and templates), NOT the ADO skill.

---

## Root Problem

Jerry's worktracker has **structural integrity rules** (WTI-001 through WTI-006) but **zero content quality rules**. The behavior rules enforce that state updates happen atomically and evidence is provided before closure -- but they say nothing about:

- Whether AC is populated, clear, or useful
- Whether descriptions are concise or walls of text
- Whether the content is user-focused or implementation-focused
- Whether the user validated the work item before creation

The templates (BUG.md=467 lines, STORY.md=492 lines, TASK.md=252 lines) serve as **ontology reference documents**, not practical creation guides. Only 38-47% of template content is creation-relevant.

---

## Research Findings

### From ps-researcher (proj-005-r-001)

| Finding | Implication |
|---------|-------------|
| **QUS Framework** (13 criteria) validates AC quality measurement | Jerry's rules should be explicit, measurable rubrics |
| **3-5 AC bullets** is industry consensus; 6+ signals scope issue | Hard limits: Story 5, Bug 3, Task 3, Enabler 5, Feature 5 |
| **LLMs achieve kappa 0.84-0.87** when given explicit criteria | Quality rules MUST be explicit -- vague guidance fails |
| **Rubber-stamp risk** is the #1 threat to human-in-the-loop | Smart checkpoints, not approval fatigue |
| **Diataxis framework** separates reference from how-to guides | Quick Creation Guides solve the "wall of text" template problem |
| **AC vs DoD** must be strictly separated | STORY.md DoD section actively teaches conflation |

### From ps-analyst (proj-005-a-001)

| Finding | Implication |
|---------|-------------|
| **11 ADO patterns** mapped to 0 WTI rules | Complete content quality gap |
| **BUG.md 47% creation-relevant**, STORY.md 41%, TASK.md 38% | Templates need embedded creation guidance |
| **STORY.md DoD section** (lines 289-313) conflates AC with DoD | Must reframe or remove |
| **wt-auditor has 5 check types**, none for content quality | New Phase 2.5 needed with regex patterns |
| **24 ADO patterns extracted** and mapped to proposed rules | Foundation for WTI-007 sub-rules |

### Key Decisions from Research

| Decision | Rationale |
|----------|-----------|
| **Two new WTI rules** (WTI-007, WTI-008) instead of six | Consolidate into sub-rules to avoid rule proliferation |
| **Embed guides in templates** (not separate files) | Quick Creation Guide at top of existing templates; avoids file sprawl |
| **Separate content-standards.md reference file** | Keep behavior-rules.md focused on rules; detailed examples in reference |
| **Tiered checkpoints** (not blanket approval) | Avoid rubber-stamp risk; only escalate when needed |
| **WTI-007 sub-rules (a-g)** for content quality | Granular, testable, detectable by auditor |
| **WTI-008 sub-rules (a-d)** for collaboration | Pre-creation, AC review, missing info flag, skip mechanism |

---

## Implementation Plan

### Phase A: Content Quality Rules (EN-001) -- Critical Path

Create the core rule infrastructure. All other changes depend on this.

| Change | File | Action |
|--------|------|--------|
| Content standards reference | `skills/worktracker/rules/worktracker-content-standards.md` | **CREATE** |
| WTI-007: Content Quality | `skills/worktracker/rules/worktracker-behavior-rules.md` | MODIFY |
| WTI-008: Collaboration | `skills/worktracker/rules/worktracker-behavior-rules.md` | MODIFY |

**worktracker-content-standards.md** contains:
- AC quality standards with the #1 Rule
- Hard bullet limits by work item type
- Anti-pattern table (DoD in AC, implementation details, hedge words)
- Concrete vs Vague examples table (6+ examples)
- Hemingway writing style directive
- Pre-finalization quality check (4 questions)
- AC vs DoD separation with shared DoD reference

### Phase B: Template Quick Creation Guides (EN-002) -- Depends on Phase A

Add practical creation guidance to the templates Claude reads during work item creation.

| Change | File | Action |
|--------|------|--------|
| Bug Quick Creation Guide | `.context/templates/worktracker/BUG.md` | MODIFY (prepend) |
| Story Quick Creation Guide | `.context/templates/worktracker/STORY.md` | MODIFY (prepend + reframe DoD) |
| Task Quick Creation Guide | `.context/templates/worktracker/TASK.md` | MODIFY (prepend) |

### Phase C: Skill Integration & Auditor (EN-003) -- Depends on Phase A

Connect the new rules to the skill loading system and enhance automated detection.

| Change | File | Action |
|--------|------|--------|
| Load content standards | `skills/worktracker/SKILL.md` | MODIFY |
| Content quality audit phase | `skills/worktracker/agents/wt-auditor.md` | MODIFY |

---

## Work Breakdown

### EPIC-001: Work Item Content Quality

```
EPIC-001: Work Item Content Quality
├── EN-001: Content Quality Rules & Standards [CRITICAL PATH]
│   ├── TASK-001: Create worktracker-content-standards.md
│   ├── TASK-002: Add WTI-007 to behavior-rules.md
│   └── TASK-003: Add WTI-008 to behavior-rules.md
├── EN-002: Template Quick Creation Guides [DEPENDS: EN-001]
│   ├── TASK-004: Add Quick Creation Guide to BUG.md
│   ├── TASK-005: Add Quick Creation Guide to STORY.md + reframe DoD
│   └── TASK-006: Add Quick Creation Guide to TASK.md
└── EN-003: Skill Integration & Auditor Enhancement [DEPENDS: EN-001]
    ├── TASK-007: Update SKILL.md to load content standards
    └── TASK-008: Add content quality audit phase to wt-auditor.md
```

### Dependencies

```
EN-001 ──┬──> EN-002 (guides reference the standards)
         └──> EN-003 (auditor enforces the standards)

TASK-001 ──> TASK-002 (WTI-007 references content-standards.md)
TASK-001 ──> TASK-003 (WTI-008 references content-standards.md)
TASK-002 ──> TASK-004, TASK-006 (guides enforce WTI-007 rules)
TASK-002 + TASK-009 ──> TASK-005 (STORY guide + DoD reframe needs DOD.md) [F-002]
TASK-002 ──> TASK-008 (auditor detects WTI-007 violations)
TASK-001 + TASK-002 + TASK-003 ──> TASK-007 (SKILL.md needs both WTI-007 and WTI-008) [F-003]
TASK-009 ──> (no dependencies, can start in parallel with Phase A)
```

**Note:** Dependencies corrected per nse-reviewer findings F-002 and F-003 (2026-02-16).

---

## Verification

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Content standards file exists | `ls skills/worktracker/rules/worktracker-content-standards.md` | File exists, 100+ lines |
| WTI-007 defined | Read behavior-rules.md | WTI-007 section with sub-rules a-g |
| WTI-008 defined | Read behavior-rules.md | WTI-008 section with sub-rules a-d |
| Quick Creation Guides present | Read BUG.md, STORY.md, TASK.md | Guide section at top of each |
| STORY.md DoD reframed | Read STORY.md DoD section | Explicit note that DoD ≠ AC |
| SKILL.md loads new rule | Read SKILL.md | `@rules/worktracker-content-standards.md` present |
| wt-auditor has content checks | Read wt-auditor.md | Phase 2.5 section with detection patterns |
| Creation test | Create a test Story via worktracker | Collaboration checkpoints fire |
| Audit test | Run wt-auditor on existing project | Content quality issues reported |

---

## Source Documents

### Research Artifacts (This Project)

| ID | Title | Path |
|----|-------|------|
| proj-005-r-001 | AC Quality Best Practices | `research/proj-005-r-001-ac-quality-best-practices.md` |
| proj-005-a-001 | Worktracker Gap Analysis | `research/proj-005-a-001-worktracker-gap-analysis.md` |
| proj-005-s-001 | Research Synthesis | `research/proj-005-s-001-content-quality-synthesis.md` |
| proj-005-e-001 | Requirements Review (nse-reviewer) | `reviews/proj-005-e-001-requirements-review.md` |

### External Sources

- `C:\Users\TZimmerman\Downloads\jerry-process-feedback-2026-02-11 (1).md` -- 7 feedback themes
- `C:\Users\TZimmerman\Downloads\Jerry .vtt` -- Adam Nowak conversation transcript
- `c:\AI\ClaudeDevelopment\skills\LEARNINGS.md` -- Active learnings from sprint planning
- Session analysis (calm-stargazing-biscuit) -- 23 sessions reviewed
- ADO Skill: `C:\Users\TZimmerman\.claude\skills\ado\SKILL.md`
- ADO AC Standards: `C:\Users\TZimmerman\.claude\skills\ado\references\acceptance-criteria-standards.md`
