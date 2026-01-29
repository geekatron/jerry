# DISC-005: EN-006 Context Injection Artifact Promotion Gap Analysis

<!--
TEMPLATE: Discovery
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
FEATURE: FEAT-002
FRAMEWORK: Jerry Problem-Solving (5W2H + Gap Analysis)
-->

> **Type:** discovery
> **Status:** resolved
> **Resolution:** Expand EN-014 with 6 additional tasks
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-28T12:00:00Z
> **Updated:** 2026-01-28T13:00:00Z
> **Parent:** FEAT-002
> **Owner:** Claude
> **Quality Score:** N/A (discovery)

---

## Executive Summary (L0: ELI5)

**The Problem:** EN-006 created detailed "recipe books" (domain specifications) for 6 different types of meetings (software engineering, architecture, product management, etc.). These recipe books tell the skill *exactly* how to extract information from each type of meeting.

**The Gap:** We only copied 2 basic recipe books to the skill (`general.yaml`, `transcript.yaml`). The 6 specialized recipe books are still sitting in the design folder - never promoted to the skill.

**The Impact:** The skill cannot specialize for different meeting types without these recipe books. It's like having a chef who can only cook generic food, even though we wrote detailed Italian, French, and Chinese cookbooks for them.

---

## Discovery Details

### 5W2H Analysis

| Question | Answer |
|----------|--------|
| **WHO** discovered this? | User review of EN-006 artifacts during EN-013 completion |
| **WHAT** is the gap? | 6 domain specifications from EN-006 TASK-038 not promoted to skill |
| **WHEN** should this have happened? | During EN-014 implementation (Domain Context Files) |
| **WHERE** are the missing artifacts? | EN-006 `docs/specs/domain-contexts/` → should be in `skills/transcript/` |
| **WHY** was this missed? | EN-014 scope only included `general.yaml`, `transcript.yaml`, `meeting.yaml` - not the 6 EN-006 domains |
| **HOW** should we fix it? | Create tasks to transform and promote EN-006 artifacts to skill |
| **HOW MUCH** effort? | Estimated 6-8 story points (6 domains × transformation work + validation) |

---

## Evidence: What EN-006 Produced

### TASK-038 Deliverables (Phase 3 - Domain Context Specifications)

EN-006 TASK-038 created **34 files** across **6 domains**:

```
EN-006/docs/specs/domain-contexts/
├── DOMAIN-SCHEMA.json              ← JSON Schema for domain validation
├── README.md                       ← Domain selection guide with flowchart
├── VCRM-domains.md                 ← Verification traceability matrix
│
├── 01-software-engineering/        ← 6 files
│   ├── SPEC-software-engineering.md   ← L0/L1/L2 domain specification
│   ├── entities/entity-definitions.yaml
│   ├── extraction/extraction-rules.yaml
│   ├── prompts/prompt-templates.md     ← Detailed extraction prompts
│   └── validation/acceptance-criteria.md
│
├── 02-software-architecture/       ← Same structure (6 files)
├── 03-product-management/          ← Same structure (6 files)
├── 04-user-experience/             ← Same structure (6 files)
├── 05-cloud-engineering/           ← Same structure (6 files)
└── 06-security-engineering/        ← Same structure (6 files)
```

### EN-006 Enabler Acceptance Criteria (from EN-006-context-injection-design.md)

```
**Phase 3 (Integration, Risk & Examples): ✅ COMPLETE**
- [x] 6 domain context specifications created (34 files total)
```

**Source:** EN-006-context-injection-design.md lines 76-77

### EN-006 README Explicitly States Implementation Deferred

From `domain-contexts/README.md`:

> **IMPORTANT:** These are design specifications only. The actual implementation
> (creating `contexts/{domain}.yaml` files, test transcripts, validation execution)
> is deferred to FEAT-002.

And:

> These specifications will be implemented in FEAT-002:
> 1. **Context Files**: `contexts/{domain}.yaml` for each domain
> 2. **Test Transcripts**: Real transcripts for validation
> 3. **Validation Tooling**: Schema validation + transcript testing

**Source:** domain-contexts/README.md lines 31-34, 182-188

---

## Evidence: What EN-014 Planned

### EN-014 Task Inventory (from EN-014-domain-context-files.md)

| ID | Title | Status |
|----|-------|--------|
| TASK-126 | Create general.yaml baseline domain schema | pending |
| TASK-127 | Create transcript.yaml core domain schema | pending |
| TASK-128 | Create meeting.yaml extended domain schema | pending |
| TASK-129 | Create JSON Schema validator for domain files | pending |
| TASK-130 | Validate all schemas against JSON Schema | pending |

**Total domains planned in EN-014:** 3 (general, transcript, meeting)

**EN-006 domains NOT in EN-014:** 6 (software-engineering, software-architecture, product-management, user-experience, cloud-engineering, security-engineering)

---

## Gap Analysis

### Artifact-by-Artifact Comparison

| EN-006 Artifact | Purpose | In Skill? | In EN-014? | Status |
|-----------------|---------|-----------|------------|--------|
| `DOMAIN-SCHEMA.json` | Validate domain files | ❌ | ❌ | **MISSING** |
| `01-software-engineering/` | SE meeting extraction | ❌ | ❌ | **MISSING** |
| `02-software-architecture/` | Architecture meeting extraction | ❌ | ❌ | **MISSING** |
| `03-product-management/` | PM meeting extraction | ❌ | ❌ | **MISSING** |
| `04-user-experience/` | UX research extraction | ❌ | ❌ | **MISSING** |
| `05-cloud-engineering/` | Ops/SRE meeting extraction | ❌ | ❌ | **MISSING** |
| `06-security-engineering/` | Security meeting extraction | ❌ | ❌ | **MISSING** |
| `README.md` (flowchart) | Domain selection guide | ❌ | ❌ | **MISSING** |
| `general.yaml` | Baseline domain | ✅ | ✅ | DONE (EN-013 TASK-121) |
| `transcript.yaml` | Core transcript domain | ✅ | ✅ | DONE (EN-013 TASK-122) |
| `meeting.yaml` | Meeting extension | ❌ | ✅ | TASK-128 pending |

### What Each Domain Contains (Runtime-Necessary)

Each EN-006 domain specification contains artifacts that **agents need at runtime**:

1. **entity-definitions.yaml** → Defines entities to extract (e.g., `commitment`, `blocker`, `risk`)
2. **extraction-rules.yaml** → Patterns to find entities (e.g., "I'm blocked on...")
3. **prompt-templates.md** → Detailed extraction prompts with template variables
4. **acceptance-criteria.md** → Validation criteria

**These are NOT just design documentation.** They contain:
- Entity schemas the extractor agent needs
- Extraction patterns the extractor uses
- Prompt templates that become `prompt_guidance` in consolidated YAML
- Validation criteria for testing

---

## Impact Assessment

### What Cannot Work Without These Artifacts

1. **Domain Specialization:** Users cannot invoke `/transcript --domain software-engineering` because that domain doesn't exist in the skill
2. **Entity Coverage:** The skill cannot extract domain-specific entities like `commitment`, `blocker`, `risk` (SE domain)
3. **Prompt Guidance:** Agents don't have domain-expert knowledge for specialized extraction
4. **Validation:** Cannot validate extraction against domain-specific acceptance criteria

### Risk: Skill Not Self-Contained

The user requirement was:
> "self-contained skill means all the additional context-integration ships with the skill"

**Current state:** The skill depends on artifacts that exist only in the design folder (EN-006). This violates the self-containment requirement.

---

## Root Cause Analysis (5 Whys)

**Problem:** EN-006 domain specifications not promoted to skill.

1. **Why?** EN-014 only planned for 3 domains (general, transcript, meeting)
2. **Why?** EN-014 was created during FEAT-002 restructuring, focused on "minimum viable" domains
3. **Why?** The restructuring didn't systematically map all EN-006 deliverables to implementation tasks
4. **Why?** No explicit traceability verification between EN-006 outputs and FEAT-002 implementation plan
5. **Why?** The "deferred to FEAT-002" statement in EN-006 README wasn't converted to specific tasks

**Root Cause:** Missing traceability verification between design phase (FEAT-001/EN-006) outputs and implementation phase (FEAT-002) task inventory.

---

## Proposed Resolution Strategy

### Option A: Expand EN-014 Scope (Recommended)

Add 6 new tasks to EN-014 for the missing domains:

| New Task | Description |
|----------|-------------|
| TASK-126A | Transform & create software-engineering.yaml |
| TASK-126B | Transform & create software-architecture.yaml |
| TASK-126C | Transform & create product-management.yaml |
| TASK-126D | Transform & create user-experience.yaml |
| TASK-126E | Transform & create cloud-engineering.yaml |
| TASK-126F | Transform & create security-engineering.yaml |

**Pros:** Keeps domain context work in one enabler
**Cons:** Increases EN-014 scope significantly

### Option B: Create New EN-017 Enabler

Create dedicated enabler for EN-006 artifact promotion:

```
EN-017: EN-006 Design Artifact Promotion
├── TASK-140: Promote JSON Schema (DOMAIN-SCHEMA.json)
├── TASK-141..146: Transform 6 domains to consolidated YAML
├── TASK-147: Promote domain selection guide to skill docs
├── TASK-148: Update SKILL.md with available domains
└── TASK-149: Validation execution
```

**Pros:** Clear scope, dedicated quality gate, explicit traceability
**Cons:** Adds new enabler to schedule

### Option C: Add to EN-015 (Validation)

Add artifact promotion as prerequisite to validation.

**Pros:** Validation needs the artifacts anyway
**Cons:** Conflates two different concerns (promotion vs validation)

---

## Transformation Required

The EN-006 artifacts are **decomposed** (separate files per concern). The skill expects **consolidated** YAML files. Transformation involves:

```
EN-006 Structure                          Skill Structure
─────────────────                          ──────────────
entities/entity-definitions.yaml  ─┐
extraction/extraction-rules.yaml  ─┼──►  software-engineering.yaml
prompts/prompt-templates.md       ─┘      (single consolidated file)
```

### Example Transformation

**From EN-006 entity-definitions.yaml:**
```yaml
entities:
  commitment:
    description: "Work item a team member commits to complete..."
    attributes:
      - assignee: "Person making the commitment"
      - work_item: "Description of the work"
```

**To skill consolidated YAML:**
```yaml
entity_definitions:
  commitment:
    description: "Work item a team member commits to complete..."
    attributes:
      - name: "assignee"
        type: "string"
        required: true
      - name: "work_item"
        type: "string"
```

**Plus merge from extraction-rules.yaml and prompt-templates.md into single file.**

---

## Human Decisions (2026-01-28)

### Question 1: SPEC Files Promotion
**Q:** Should `SPEC-{domain}.md` files be promoted to skill as documentation, or are they design-only?

**A: YES, promote SPEC files as documentation.**

The SPEC files contain valuable L0/L1/L2 domain documentation that users and agents benefit from:
- L0: Overview for stakeholders (what the domain covers)
- L1: Entity model diagrams and technical details for engineers
- L2: Architectural considerations for workflow designers

**Action:** SPEC files will be promoted to `skills/transcript/docs/domains/SPEC-{domain}.md`

---

### Question 2: Scope Decision
**Q:** Should we expand EN-014 (Option A) or create EN-017 (Option B)?

**A: OPTION A - Expand EN-014 with 6 additional tasks.**

Rationale:
- Keeps all domain context work in one enabler
- Maintains clear traceability (EN-006 design → EN-014 implementation)
- Dependencies updated to reflect correct graph

---

### Question 3: Priority
**Q:** Should this be done before or after EN-016 formatter completion?

**A: AFTER EN-016 is complete.**

Rationale:
- EN-016 formatter is core functionality, higher priority
- Domain specialization is enhancement, can wait
- EN-014 is already blocked by EN-013 (which is complete)
- New EN-014 tasks will be blocked by existing EN-014 tasks (TASK-126..130)

---

### Question 4: Transformation Approach
**Q:** Should we use decomposed files (4 files per domain) or consolidated YAML?

**A: CONSOLIDATED YAML (as designed in SPEC-context-injection.md).**

**Analysis of Design Impact:**

| Approach | Design Changes Required | Implementation Changes |
|----------|------------------------|----------------------|
| **Consolidated** | None - matches SPEC Section 3.3 | None - EN-013 already implements |
| **Decomposed** | SPEC-context-injection.md rewrite, new ADR | Reopen EN-013, modify context loader |

**Evidence from SPEC-context-injection.md Section 3.3 (lines 383-397):**
```
skills/transcript/
└── contexts/                    ← Domain schemas location
    ├── legal.yaml              ← Single file per domain
    ├── sales.yaml
    └── general.yaml
```

**Token Limit Analysis:**
- EN-006 software-engineering domain: ~140 (entities) + ~140 (rules) + ~300 (prompts) = **~580 lines**
- Read tool limit: **2000 lines** - plenty of headroom
- If a domain grows too large, split into sub-domains (e.g., `software-engineering-standup`)

**Decision:** Transform EN-006 decomposed artifacts into consolidated YAML during promotion. This:
1. Aligns with existing SPEC design
2. Avoids reopening EN-013 (already DONE and gate-passed)
3. Keeps implementation simple
4. Token limits not a concern for current domain sizes

---

## Resolution: EN-014 Expansion Plan

### New Tasks to Add to EN-014

| Task ID | Title | Blocked By | Effort |
|---------|-------|------------|--------|
| TASK-150 | Transform & create software-engineering.yaml | TASK-129 | 1 |
| TASK-151 | Transform & create software-architecture.yaml | TASK-129 | 1 |
| TASK-152 | Transform & create product-management.yaml | TASK-129 | 1 |
| TASK-153 | Transform & create user-experience.yaml | TASK-129 | 1 |
| TASK-154 | Transform & create cloud-engineering.yaml | TASK-129 | 1 |
| TASK-155 | Transform & create security-engineering.yaml | TASK-129 | 1 |
| TASK-156 | Promote DOMAIN-SCHEMA.json to skill schemas | TASK-129 | 0.5 |
| TASK-157 | Promote SPEC-*.md files to skill docs | TASK-150..155 | 1 |
| TASK-158 | Update SKILL.md with 6 new domains | TASK-150..155 | 0.5 |
| TASK-159 | Validation: All 8 domains load correctly | TASK-158, TASK-130 | 1 |

**Total Additional Effort:** 9 story points

### Dependency Graph

```
EN-014 EXPANDED DEPENDENCY GRAPH
================================

EXISTING TASKS (EN-014):
────────────────────────
TASK-126 (general.yaml)     ─┐
         │                   │
         ▼                   │
TASK-127 (transcript.yaml)   │
         │                   │
         ▼                   │
TASK-128 (meeting.yaml)      │
                             │
TASK-129 (JSON Schema) ◄─────┘
         │
         ▼
TASK-130 (Validate existing)

NEW TASKS (EN-006 Promotion):
─────────────────────────────
TASK-129 ─────┬──────┬──────┬──────┬──────┬──────┬───────┐
              │      │      │      │      │      │       │
              ▼      ▼      ▼      ▼      ▼      ▼       ▼
         TASK-150 TASK-151 TASK-152 TASK-153 TASK-154 TASK-155 TASK-156
         (SE)    (arch)   (PM)    (UX)    (cloud) (sec)  (schema)
              │      │      │      │      │      │
              └──────┴──────┴──────┴──────┴──────┘
                             │
                             ▼
                     TASK-157 (SPEC docs)
                             │
                             ▼
                     TASK-158 (SKILL.md update)
                             │
                             ▼
                     TASK-159 (Final validation)

EXTERNAL DEPENDENCIES:
──────────────────────
EN-014 (all new tasks) ←──blocked by──── EN-016 (must complete first)
```

### Target Skill Structure After Promotion

```
skills/transcript/
├── SKILL.md                          # Updated with 8 domains
├── agents/
│   ├── ts-parser.md
│   ├── ts-extractor.md
│   └── ts-formatter.md
├── contexts/
│   ├── general.yaml                  # Existing
│   ├── transcript.yaml               # Existing
│   ├── meeting.yaml                  # EN-014 TASK-128
│   ├── software-engineering.yaml     # NEW (TASK-150)
│   ├── software-architecture.yaml    # NEW (TASK-151)
│   ├── product-management.yaml       # NEW (TASK-152)
│   ├── user-experience.yaml          # NEW (TASK-153)
│   ├── cloud-engineering.yaml        # NEW (TASK-154)
│   └── security-engineering.yaml     # NEW (TASK-155)
├── schemas/
│   └── domain-schema.json            # NEW (TASK-156)
└── docs/
    ├── PLAYBOOK.md                   # Existing
    ├── RUNBOOK.md                    # Existing
    └── domains/                      # NEW folder
        ├── SPEC-software-engineering.md    # NEW (TASK-157)
        ├── SPEC-software-architecture.md
        ├── SPEC-product-management.md
        ├── SPEC-user-experience.md
        ├── SPEC-cloud-engineering.md
        ├── SPEC-security-engineering.md
        └── DOMAIN-SELECTION-GUIDE.md  # From EN-006 README flowchart
```

---

## Traceability

### Source References

| Reference | Location | Lines |
|-----------|----------|-------|
| EN-006 enabler definition | EN-006-context-injection-design.md | 76-77 (AC complete) |
| TASK-038 domain specs | EN-006-context-injection-design.md | 122 |
| README deferral statement | domain-contexts/README.md | 31-34 |
| Implementation scope | domain-contexts/README.md | 182-188 |
| EN-014 task inventory | EN-014-domain-context-files.md | 179-189 |

### Blocked Work

This discovery potentially blocks:
- Full domain specialization capability
- Validation of domain-specific extraction
- Self-contained skill deployment

---

## Related Items

- **Parent:** [FEAT-002: Implementation](../FEAT-002-implementation.md)
- **Source:** [EN-006: Context Injection Design](../../FEAT-001-analysis-design/EN-006-context-injection-design/EN-006-context-injection-design.md)
- **Affected:** [EN-014: Domain Context Files](./EN-014-domain-context-files/EN-014-domain-context-files.md)
- **Affected:** [EN-015: Transcript Validation](./EN-015-transcript-validation/EN-015-transcript-validation.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | OPEN | Discovery created via ps-analyst gap analysis. User identified during EN-013 completion review. |
| 2026-01-28 | **RESOLVED** | Human decisions received: (1) SPEC files promoted as docs, (2) Expand EN-014 not create EN-017, (3) After EN-016, (4) Consolidated YAML per SPEC design. Created expansion plan with 10 new tasks (TASK-150..159). |

---

## Next Steps

1. **Immediate:** Update EN-014-domain-context-files.md with new tasks (TASK-150..159)
2. **Immediate:** Update ORCHESTRATION.yaml with new task dependencies
3. **After EN-016:** Execute TASK-150..159 to promote EN-006 artifacts

---

*Document ID: DISC-005*
*Framework: Jerry Problem-Solving (5W2H + Gap Analysis)*
*Status: RESOLVED - Awaiting implementation after EN-016*
