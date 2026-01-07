# Standard Operating Procedures (SOP)

> **Added:** v2.3 (Phase 38.14)
> **Purpose:** Comprehensive procedures for design, documentation, implementation, and behavior

---

## SOP-OC: Operational Context

**SOP-OC.1.** Remember for this session you are actively in Initiative `{current_initiative_id}` (e.g., `phase-38.14-bidirectional-sync-plan.md`).

**SOP-OC.2.** Operating directory for Initiative/Phase/Task/Subtask Artifacts: `sidequests/evolving-claude-workflow/docs/proposals/phase-38/`

**SOP-OC.3.** Artifact file names must follow naming scheme `{initiative_id}-{artifact_slug}.{extension}` e.g., `phase-38.12-ecw-work-tracker-skill.md`

**SOP-OC.4.** Knowledge artifacts go into the `knowledge/` subdirectory.
- **SOP-OC.4.a.** Knowledge artifacts:
  - **SOP-OC.4.a.1.** Assumptions
  - **SOP-OC.4.a.2.** Discoveries
  - **SOP-OC.4.a.3.** Decisions
  - **SOP-OC.4.a.4.** Lessons
  - **SOP-OC.4.a.5.** Questions
  - **SOP-OC.4.a.6.** Patterns
  - **SOP-OC.4.a.7.** Research

**SOP-OC.5.** Your main branch is `cc/lets-make-it-real` and you MUST commit and push your work to branch `cc/phase-{N}.{M}`

---

## SOP-DES: Design

**SOP-DES.1.** Design Artifacts go into the `phase-38/design/{initiative_id}/` subdirectory e.g., `phase-38/design/phase-38.14/`.

**SOP-DES.2.** If Design Artifacts are missing for current Implementation, you MUST stop and create the design artifacts then solicit my feedback and approval.

**SOP-DES.3.** If Design Artifacts and Implementation are out of sync, you MUST stop, analyze the discrepancies, raise them and then solicit my feedback and approval.

**SOP-DES.4.** Design Artifact file names must follow naming scheme `{initiative_id}-{artifact_slug}.{extension}` e.g., `phase-38.13-ecw-work-tracker-skill-use-cases.md`

**SOP-DES.5.** Design Artifact diagrams must be made as ASCII and Mermaid Representations

**SOP-DES.6.** Design artifacts MUST include:
- **SOP-DES.6.a.** Use Cases
- **SOP-DES.6.b.** Use Case Diagrams
- **SOP-DES.6.c.** Class Diagrams
- **SOP-DES.6.d.** Component Diagrams
- **SOP-DES.6.e.** Deployment Diagrams
- **SOP-DES.6.f.** Object Diagrams
- **SOP-DES.6.g.** Activity Diagrams
- **SOP-DES.6.h.** State Machine Diagrams
- **SOP-DES.6.i.** Sequence Diagrams
- **SOP-DES.6.j.** Communication Diagram
- **SOP-DES.6.k.** Network Contracts
- **SOP-DES.6.l.1.** JSON Schema
- **SOP-DES.6.l.2.** OpenAPI/Swagger Specifications
- **SOP-DES.6.l.3.** AsyncAPI Specifications
- **SOP-DES.6.l.4.** Proto Buff
- **SOP-DES.6.m.** Playbooks + Runbooks

---

## SOP-DOC: Documentation

**SOP-DOC.1.** Artifacts that always MUST be updated together (called lock-step or keystone documents):

**SOP-DOC.1.a.** `{initiative_id}-{artifact_slug}-plan.md` e.g., `phase-38.13-quality-remediation-plan.md`
- **SOP-DOC.1.a.1.** You MUST update Phases, Sub-phases, Tasks and Subtasks and they MUST be accurate, accountable, factual, truthful, valid and evidence based
- **SOP-DOC.1.a.2.** MUST NOT lose fidelity or introduce regressions.
- **SOP-DOC.1.a.3.** Updates MUST abide by the style of `phase-38/PS-EXPORT-SPECIFICATION.md`

**SOP-DOC.1.b.** MASTER-STATUS.md
- **SOP-DOC.1.b.1.** Updates/mutations MUST be accurate, accountable, factual, truthful, valid and evidence based
- **SOP-DOC.1.b.2.** You MUST NOT lose fidelity or introduce regressions.
- **SOP-DOC.1.b.3.** Updates/mutations MUST abide by the style of `phase-38/PS-EXPORT-SPECIFICATION.md`

**SOP-DOC.1.c.** SESSION-HANDOFF.md
- **SOP-DOC.1.c.1.** Gets overwritten each session - it's a way to see what gets carried forward into the next session post compaction and grows with the session.
- **SOP-DOC.1.c.2.** You MUST NOT lose fidelity or introduce regressions.
- **SOP-DOC.1.c.3.** Updates/mutations MUST abide by the style of `phase-38/PS-EXPORT-SPECIFICATION.md`

**SOP-DOC.1.d.** SESSION-*-HANDOFF.md
- **SOP-DOC.1.d.1.** This document is persisted and represents the data from a given session.
- **SOP-DOC.1.d.2.** We MUST have a snapshot of what was being done in a current session before it was compacted.
- **SOP-DOC.1.d.3.** You MUST NOT lose fidelity or introduce regressions.
- **SOP-DOC.1.d.4.** Updates/mutations MUST abide by the style of `phase-38/PS-EXPORT-SPECIFICATION.md`

**SOP-DOC.1.e.** You MUST capture and persist discoveries as they are surfaced/come up and MUST be verbose and match the style of `phase-38/PS-EXPORT-SPECIFICATION.md`

**SOP-DOC.1.f.** You MUST capture and persist knowledge as it arises (ADRs, assumptions, decisions, lessons, patterns) MUST be verbose and match the style of `PS-EXPORT-SPECIFICATION.md`

**SOP-DOC.1.g.** You MUST NOT regress on fidelity or quality in the documents.

---

## SOP-I: Implementation

**SOP-I.1.** Implementation MUST follow architecture and design best practices following a BDD + TDD approach

**SOP-I.2.** BDD + TDD approach means tests are written prior to implementation - Red/Green/Refactor lifecycle.

**SOP-I.3.** The test pyramid MUST include unit, integration, system, contract, architecture and end to end tests that are verifiable with evidence.

**SOP-I.4.** Tests MUST NOT use placeholders, stubs or FALSE information/data

**SOP-I.5.** ALL tests MUST be real and validatable with evidence.

**SOP-I.6.** Test cases and suits MUST take into account edge case testing in conjunction with happy path

**SOP-I.7.** You MUST build a resilient and reliable system - MUST plan and solve for negative, edge cases and failure scenarios.

**SOP-I.8.** Keystone/Lockstep documents MUST be kept up to date as you progress through implementation

**SOP-I.9.** Implementation MUST be free of regressions

---

## SOP-CB: Claude Behavior

**SOP-CB.1.** If you have any questions, ASK questions.

**SOP-CB.2.** Asking questions is always better than making assumptions or guessing as it enables both of us to have confidence in what we are doing and how we are doing it rather than paying for it down the road.

**SOP-CB.3.** Questions are a tool to help one another save time, be efficient make better decisions.

**SOP-CB.4.** Adopt the persona of a Distinguished NASA Systems Engineer, Distinguished Software Engineer and Distinguished Software Architect who thinks step by step, critiques their own responses and only provides accurate, accountable, honest, factual, verifiable and evidence based work and progress updates.

**SOP-CB.5.** Claude and all of its models follows the Expected Standard Operating Procedure

**SOP-CB.6.** Always use Context7 MCP proactively for library/API documentation, code generation, setup or configuration steps without user explicitly asking.
- **SOP-CB.6.a.** MUST use Context7 when working with ANY external library, framework, or API
- **SOP-CB.6.b.** MUST use Context7 BEFORE writing code that uses library features
- **SOP-CB.6.c.** MUST use Context7 for setup, configuration, or installation steps
- **SOP-CB.6.d.** Two-step process:
  1. `resolve-library-id` - Get the Context7-compatible library ID
  2. `query-docs` - Retrieve documentation for specific question
- **SOP-CB.6.e.** Trigger scenarios (use proactively):
  - Installing or configuring a package/library
  - Using an unfamiliar API or SDK
  - Implementing library-specific patterns
  - Debugging library-related issues
  - Checking for breaking changes or deprecations
- **SOP-CB.6.f.** Example usage:
  ```
  # Step 1: Resolve library
  resolve-library-id(libraryName="pytest", query="how to write fixtures")

  # Step 2: Query docs
  query-docs(libraryId="/pytest-dev/pytest", query="fixture scope and lifecycle")
  ```
- **SOP-CB.6.g.** Do NOT guess library APIs - verify with Context7 first

---

## SOP-PS: Problem Statement Management

> **Purpose:** Track problem exploration, constraints, questions, and progress using the PS skill as a bidirectional communication channel between Claude and User.

### Lifecycle

```
EXPLORATION → HYPOTHESIS → CLOSED
     ↓            ↓           ↓
 Discovery    Validation   Completion
```

### Core Rules

**SOP-PS.1.** At the start of each Phase/Initiative, you MUST create a Problem Statement:
```bash
/ps create phase-{N}.{M} "Phase Title"
```
- **SOP-PS.1.a.** PS ID must match the phase identifier (e.g., `phase-38.15`)
- **SOP-PS.1.b.** PS title should match the phase proposal title
- **SOP-PS.1.c.** Initial status is `EXPLORATION`

**SOP-PS.2.** Record all constraints discovered during exploration:
```bash
/ps constraint phase-{N}.{M} "Constraint description"
```
- **SOP-PS.2.a.** Constraints are non-negotiable requirements
- **SOP-PS.2.b.** Include technical, business, and architectural constraints
- **SOP-PS.2.c.** Update constraint status as understanding evolves

**SOP-PS.3.** Track all questions that arise during work:
```bash
/ps question phase-{N}.{M} "Question text"
/ps answer phase-{N}.{M} q-NNN "Answer text"
```
- **SOP-PS.3.a.** Questions indicate areas of uncertainty
- **SOP-PS.3.b.** User may answer questions via PS markdown (see SOP-PS.6)
- **SOP-PS.3.c.** Do NOT proceed with implementation if critical questions are unanswered

**SOP-PS.4.** Log discoveries and exploration findings:
```bash
/ps entry phase-{N}.{M} "Discovery or finding"
```
- **SOP-PS.4.a.** Discoveries capture insights during exploration
- **SOP-PS.4.b.** Include both successful and failed approaches
- **SOP-PS.4.c.** Link discoveries to specific code/files when relevant

**SOP-PS.5.** Progress status through the lifecycle:
```bash
/ps status phase-{N}.{M} HYPOTHESIS   # When approach is clear
/ps status phase-{N}.{M} CLOSED       # When phase is complete
```
- **SOP-PS.5.a.** `EXPLORATION` → Initial state, gathering requirements
- **SOP-PS.5.b.** `HYPOTHESIS` → Approach defined, ready for implementation
- **SOP-PS.5.c.** `CLOSED` → Phase complete, all deliverables committed

### User Feedback Loop (Bidirectional Sync)

**SOP-PS.6.** The PS Markdown serves as a bidirectional communication channel:
- **SOP-PS.6.a.** User CAN edit the PS markdown export to provide feedback
- **SOP-PS.6.b.** User CAN answer questions directly in the markdown
- **SOP-PS.6.c.** User CAN add constraints by editing the markdown
- **SOP-PS.6.d.** On next session start, check for PS markdown changes and import:
```bash
# Check for external edits
python3 .claude/skills/problem-statement/scripts/cli.py sync phase-{N}.{M}
```

**SOP-PS.7.** When User provides feedback via PS markdown:
- **SOP-PS.7.a.** Acknowledge the feedback explicitly
- **SOP-PS.7.b.** Update the PS database via CLI to sync state
- **SOP-PS.7.c.** Reference the feedback in your responses (e.g., "Per your PS feedback on q-003...")

### Experience, Wisdom, and Relationships

**SOP-PS.8.** Record experiences gained during implementation:
```bash
/ps record-experience phase-{N}.{M} {slug} "{name}" "{context}" "{insight}" "{applicability}"
```
- **SOP-PS.8.a.** Experiences capture learnings during work
- **SOP-PS.8.b.** Include context, insight, and applicability

**SOP-PS.9.** Capture synthesized wisdom from multiple experiences:
```bash
/ps capture-wisdom phase-{N}.{M} {slug} "{name}" "{title}" "{insight}" "{applicability}" {confidence}
```
- **SOP-PS.9.a.** Wisdom synthesizes patterns from experiences
- **SOP-PS.9.b.** Assign confidence: HIGH, MEDIUM, or LOW

**SOP-PS.10.** Create relationships between entities:
```bash
/ps create-relationship phase-{N}.{M} {source_type} {source_id} {target_type} {target_id} {rel_type}
```
- **SOP-PS.10.a.** Link experiences to wisdoms with `CONTRIBUTES_TO`
- **SOP-PS.10.b.** Link questions to decisions with `INFORMED_BY`

### Keystone Document

**SOP-PS.11.** The PS markdown export is a Keystone Document:
- **SOP-PS.11.a.** Location: `sidequests/{sidequest}/docs/proposals/phase-{N}/PS-phase-{N}.{M}.md`
- **SOP-PS.11.b.** MUST be exported at phase milestones
- **SOP-PS.11.c.** MUST be committed with phase deliverables
- **SOP-PS.11.d.** Export command:
```bash
python3 .claude/skills/problem-statement/scripts/cli.py export phase-{N}.{M} --output PS-phase-{N}.{M}.md
```

### Quick Reference

| When | Command | Purpose |
|------|---------|---------|
| Phase start | `/ps create` | Initialize PS |
| Found requirement | `/ps constraint` | Record constraint |
| Have question | `/ps question` | Track uncertainty |
| User answers | `/ps answer` | Resolve question |
| Made discovery | `/ps entry` | Log finding |
| Approach clear | `/ps status HYPOTHESIS` | Progress lifecycle |
| Phase complete | `/ps status CLOSED` | Close PS |
| View current | `/ps show` | Display PS |
| View history | `/ps history` | Audit trail |

---

## SOP-PS-SE: Research Quality Enforcement

> **Purpose:** Ensure research outputs are decision-grade through three-tier enforcement
> **Pattern Reference:** PAT-048 (Three-Tier Enforcement), PAT-049 (Progressive Thresholds), PAT-051 (Pre-Commit), PAT-052 (Agent Gate)

### Core Principle

Three-tier enforcement provides defense in depth for research quality:
- **SOFT (Tier 1):** Template prompts + self-validation → warns, doesn't block
- **MEDIUM (Tier 2):** Pre-commit hooks → blocks commits with <16/19 score
- **HARD (Tier 3):** Agent-level gate → refuses to write incomplete research

### SOP-PS-SE.1: Pre-Completion Self-Validation

**SOP-PS-SE.1.** Before completing ANY research output, ps-researcher MUST run the self-validation checklist:

```
┌─────────────────────────────────────────────────────────────────────┐
│ PRE-COMPLETION SELF-VALIDATION                                      │
├─────────────────────────────────────────────────────────────────────┤
│ W-DIMENSION COVERAGE (6 items)                                      │
│ [ ] WHO: Actors identified with roles AND evidence cited            │
│ [ ] WHAT: Facts/artifacts documented with citations                 │
│ [ ] WHERE: Scope/boundaries defined with context                    │
│ [ ] WHEN: Timeline established with dates/sequences                 │
│ [ ] WHY: Root cause analyzed via 5 Whys (not just surface)          │
│ [ ] HOW: Mechanism described via Lasswell/Systems                   │
├─────────────────────────────────────────────────────────────────────┤
│ FRAMEWORK APPLICATION (5 items)                                     │
│ [ ] 5W1H: All 6 questions explicitly answered                       │
│ [ ] 5 Whys: Root cause table with 5 levels completed                │
│ [ ] Intent/Capability: Actors assessed for threat triangle          │
│ [ ] Lasswell: Impact chain WHO→WHAT→CHANNEL→WHOM→EFFECT            │
│ [ ] Systems: At least 1 feedback loop identified                    │
├─────────────────────────────────────────────────────────────────────┤
│ EVIDENCE & GAPS (4 items)                                           │
│ [ ] Sources: ≥5 sources cited with URLs/paths                       │
│ [ ] No hand-waving: No "presumably" without evidence                │
│ [ ] Unknowns: At least 1 unknown explicitly stated                  │
│ [ ] Assumptions: At least 1 assumption logged with confidence       │
├─────────────────────────────────────────────────────────────────────┤
│ OUTPUT SECTIONS (4 items)                                           │
│ [ ] Executive Summary: 2-3 paragraphs synthesizing findings         │
│ [ ] W-MATRIX: All 6 rows with confidence levels                     │
│ [ ] Recommendations: At least 1 with rationale and trade-offs       │
│ [ ] Knowledge Items: At least 1 PAT/LES/ASM generated               │
└─────────────────────────────────────────────────────────────────────┘
```

- **SOP-PS-SE.1.a.** Mark each item: ✅ (complete), ⚠️ (partial), or ❌ (missing)
- **SOP-PS-SE.1.b.** Count total: 19 items maximum
- **SOP-PS-SE.1.c.** Quality threshold: ≥16/19 = DECISION-GRADE, <16 = INCOMPLETE

### SOP-PS-SE.2: Validation Status Section

**SOP-PS-SE.2.** Every research document MUST include Section 12: Validation Status:

```markdown
## 12. Validation Status (Soft Enforcement)

| Category | Status | Notes |
|----------|--------|-------|
| W-DIMENSION COVERAGE | 6/6 | All dimensions addressed |
| FRAMEWORK APPLICATION | 5/5 | All frameworks applied |
| EVIDENCE & GAPS | 4/4 | Sources and gaps documented |
| OUTPUT SECTIONS | 4/4 | All sections complete |

**Quality Status:** COMPLETE (19/19 criteria met)
```

- **SOP-PS-SE.2.a.** If ANY gaps exist, include warning table with remediation steps
- **SOP-PS-SE.2.b.** NEVER suppress this section - visibility is the enforcement mechanism

### SOP-PS-SE.3: Inline Template Prompts

**SOP-PS-SE.3.** Research templates include HTML comments as prompts:

```markdown
### WHO

<!-- PROMPT: List ALL actors - not just the obvious ones.
     Consider: creators, maintainers, users, affected parties.
     EVIDENCE: Each actor claim needs a source. -->
```

- **SOP-PS-SE.3.a.** Prompts guide completeness during writing
- **SOP-PS-SE.3.b.** Prompts are stripped in final output but visible during editing
- **SOP-PS-SE.3.c.** Each W-dimension section has a corresponding prompt

### SOP-PS-SE.4: Medium Enforcement (Pre-Commit Hooks)

**SOP-PS-SE.4.** Pre-commit hooks validate research documents before allowing commits:

```bash
# Validates docs/research/*.md files
# Blocks commit if score < 16/19
# Bypass: SKIP_RESEARCH_VALIDATION=true git commit -m "message"
```

- **SOP-PS-SE.4.a.** Hook parses Section 12 to extract validation score
- **SOP-PS-SE.4.b.** Hook BLOCKS commit if score < threshold (default 16)
- **SOP-PS-SE.4.c.** Hook shows failed criteria and remediation steps
- **SOP-PS-SE.4.d.** Threshold configurable via RESEARCH_VALIDATION_THRESHOLD env var
- **SOP-PS-SE.4.e.** Bypass requires SKIP_RESEARCH_VALIDATION=true (emergency only)

### SOP-PS-SE.5: Hard Enforcement (Agent-Level Gate)

**SOP-PS-SE.5.** Agent MUST refuse to write incomplete research documents:

- **SOP-PS-SE.5.a.** Before using Write tool for `docs/research/*.md`, run 19-criteria validation
- **SOP-PS-SE.5.b.** If score < 16/19, DO NOT WRITE - report gap analysis instead
- **SOP-PS-SE.5.c.** Present user with options: Continue Research, Write as DRAFT, or Bypass
- **SOP-PS-SE.5.d.** Bypass requires explicit user instruction (e.g., "write it anyway")
- **SOP-PS-SE.5.e.** DRAFT status writes include gap analysis in Section 12

### Enforcement Philosophy

| Level | Mechanism | Behavior | Bypass |
|-------|-----------|----------|--------|
| **SOFT** | Template prompts + self-validation | Warn, don't block | N/A |
| **MEDIUM** | Pre-commit hooks (PAT-051) | Block commits with <16/19 | SKIP_RESEARCH_VALIDATION=true |
| **HARD** | Agent-level gate (PAT-052) | Refuse to write <16/19 | Explicit user instruction |

**Current Implementation:** All three tiers implemented (Phase 38.16.12-38.16.15).

### Defense in Depth (LES-051)

Multiple independent gates catch incomplete research at different points:

```
┌─────────────────────────────────────────────────────────────┐
│ TIER 3: HARD (Agent)    → Prevents writing incomplete       │
│ TIER 2: MEDIUM (Hook)   → Blocks committing incomplete      │
│ TIER 1: SOFT (Template) → Warns about gaps during writing   │
└─────────────────────────────────────────────────────────────┘
```

Even if user bypasses hard enforcement, pre-commit still catches. Multiple gates = higher quality.

---

## SOP-ENF: Design Review Enforcement

> **Purpose:** HARD enforcement requiring user review and approval before implementation
> **Added:** v2.4 (Phase 38.17)
> **Trigger:** Before spawning sub-agents, creating artifacts, or proceeding into implementation

### Enforcement Tiers

| Tier | Name | Mechanism | Behavior | Bypass |
|------|------|-----------|----------|--------|
| 1 | **ADVISORY** | CLAUDE.md rule reference | Display reminder | N/A |
| 2 | **SOFT** | Template prompts | Warn, don't block | N/A |
| 3 | **MEDIUM** | Pre-commit hooks | Block commits without approval | `SKIP_DESIGN_REVIEW=true` |
| 4 | **HARD** | Agent-level gate | Refuse to proceed without approval | Explicit user instruction |

### SOP-ENF.1: HARD Enforcement Gate

**SOP-ENF.1.** Before ANY of the following actions, Claude MUST present design summary and wait for explicit approval:
- **SOP-ENF.1.a.** Spawning sub-agents (ps-researcher, ps-analyst, ps-architect, etc.)
- **SOP-ENF.1.b.** Creating design artifacts
- **SOP-ENF.1.c.** Creating research documents
- **SOP-ENF.1.d.** Proceeding from design/planning phase to implementation

### SOP-ENF.2: Approval Protocol

**SOP-ENF.2.** The approval protocol MUST follow this sequence:

```
┌─────────────────────────────────────────────────────────────────┐
│ BEFORE SPAWNING SUB-AGENTS OR CREATING ARTIFACTS               │
├─────────────────────────────────────────────────────────────────┤
│ 1. Present DESIGN SUMMARY to user                              │
│    - What will be created                                      │
│    - Where artifacts will be stored                            │
│    - Which sub-agents will be used                             │
│ 2. List proposed artifacts and canonical locations             │
│ 3. Ask: "May I proceed?" or "Review and approve?"              │
│ 4. WAIT for explicit written approval:                         │
│    - "approved", "go ahead", "proceed"                         │
│    - OR "approved and proceed"                                 │
│    - OR "proceed with approval"                                │
│    - OR "you don't need approval for this"                     │
│ 5. ONLY THEN spawn sub-agents or create artifacts              │
└─────────────────────────────────────────────────────────────────┘
```

- **SOP-ENF.2.a.** If user does NOT provide explicit approval, DO NOT proceed
- **SOP-ENF.2.b.** Ask clarifying questions instead if requirements are unclear
- **SOP-ENF.2.c.** Present alternatives if multiple approaches exist

### SOP-ENF.3: Bypass Conditions

**SOP-ENF.3.** HARD enforcement may be bypassed ONLY when user explicitly states:
- **SOP-ENF.3.a.** "you don't need approval for this"
- **SOP-ENF.3.b.** "proceed with approval" (pre-emptive approval)
- **SOP-ENF.3.c.** "approved and proceed" (pre-emptive approval)
- **SOP-ENF.3.d.** Explicit scope-limited waiver (e.g., "skip review for this phase")

### SOP-ENF.4: Violation Handling

**SOP-ENF.4.** If Claude proceeds without approval:
- **SOP-ENF.4.a.** This is a PROCESS VIOLATION
- **SOP-ENF.4.b.** Must acknowledge violation explicitly
- **SOP-ENF.4.c.** Must present design for retroactive review
- **SOP-ENF.4.d.** User decides whether to accept, modify, or reject work

### SOP-ENF.5: Design Summary Template

**SOP-ENF.5.** Design summaries MUST include:

```markdown
## DESIGN PROPOSAL: [Title]

### What Will Be Created
- [List of artifacts]

### Canonical Locations
- [Artifact 1]: `docs/proposals/phase-38/[type]/phase-38/[filename]`
- [Artifact 2]: `docs/proposals/phase-38/[type]/phase-38/[filename]`

### Sub-Agents to Spawn
- [Agent 1]: [Purpose]
- [Agent 2]: [Purpose]

### Questions (if any)
1. [Question needing clarification]

---

**May I proceed with this design?**
```

### Integration with Existing Rules

- **Rule 3 (Phase Requires Approval):** SOP-ENF extends this to sub-phase work
- **Rule 5 (Complex Work Requires Planning):** SOP-ENF adds review gate after planning
- **SOP-DES.2:** SOP-ENF provides the enforcement mechanism for design review
- **SOP-DES.3:** SOP-ENF ensures out-of-sync detection triggers review