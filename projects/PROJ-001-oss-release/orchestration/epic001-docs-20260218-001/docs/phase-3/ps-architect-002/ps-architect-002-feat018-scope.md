# FEAT-018 Scope Document — Runbooks & Playbooks

> **Agent ID:** ps-architect-002
> **Workflow ID:** epic001-docs-20260218-001
> **Phase:** 3 (FEAT-018 Scope & Structure)
> **Date:** 2026-02-18
> **Feature:** FEAT-018 — User Documentation: Runbooks & Playbooks
> **Criticality:** C2 (Standard)
> **Status:** RATIFIED — Alternative B (two-tier split) adopted

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Scope rationale and decision record |
| [Vocabulary Definitions](#vocabulary-definitions) | Runbook and playbook definitions with examples |
| [Directory Structure](#directory-structure) | Exact file paths for all FEAT-018 output |
| [Scope Boundaries](#scope-boundaries) | In-scope and out-of-scope skills with rationale |
| [Section Templates](#section-templates) | Standard runbook and playbook templates |
| [Coverage Map](#coverage-map) | Trigger keyword to playbook mapping |
| [Deliverable Inventory](#deliverable-inventory) | Complete list of files to be produced |
| [Requirements Traceability](#requirements-traceability) | REQ-942-* to document location mapping |

---

## L0: Executive Summary

FEAT-018 delivers the first formal user documentation layer for the Jerry framework — one getting-started runbook (EN-943) and three skill playbooks (EN-944). This scope document is the prerequisite artifact for all Phase 4 content creation. It answers three questions that must be decided before any content agent writes documentation:

1. **What are we building?** — A runbook covers a linear user journey from start state to end state. A playbook covers a recurring skill workflow as a reference document consulted non-linearly. These are structurally distinct document types requiring distinct templates (Section 5).

2. **Where does it live?** — All FEAT-018 output is placed under a two-tier split: `docs/runbooks/` for the getting-started runbook and `docs/playbooks/` for all three skill playbooks (Section 3). This structure was evaluated against four alternatives in the nse-explorer-001 trade study (score: 4.40 / 5.00) and is ratified here.

3. **What skills are covered?** — Three skills are in scope: problem-solving, orchestration, and transcript, per FEAT-018 AC-3. Five skills are explicitly out of scope with rationale (Section 4).

Phase 4 content agents (ps-synthesizer-001 through ps-synthesizer-004) MUST use this scope document as their primary structural reference. The templates in Section 5 and file paths in Section 3 are binding for all FEAT-018 output.

---

## Vocabulary Definitions

This section satisfies REQ-942-001.

### Runbook

**Definition:** A runbook is a linear, sequential procedure oriented around a specific user journey or operational task. It has a defined start state and a defined end state. It is intended to be followed step-by-step from beginning to end, without branching. The user is expected to execute every step in order.

**Structural signal:** A runbook answers "how do I accomplish this task from scratch?" — it tells the user what to do, in what order, and how to verify they succeeded.

**Example in Jerry:** `docs/runbooks/getting-started.md` — covers the complete journey from a freshly installed Jerry instance to a first successful skill invocation. The user starts with installation complete and ends with a persisted skill output artifact. Every step is required; there are no conditional paths.

**Additional examples of future runbooks (for illustration):**
- `docs/runbooks/project-lifecycle.md` — how to create a project, track work, and close it out
- `docs/runbooks/session-management.md` — how to start, monitor, and end a Jerry session

### Playbook

**Definition:** A playbook is a reference-oriented document covering a skill or recurring workflow pattern. It contains conditional decision points, multiple usage paths, and troubleshooting guidance. It is intended to be consulted non-linearly — a user may read only the "When to Use" section to decide whether to invoke the skill, then jump to "Examples" to find the right invocation phrase, without reading the entire document.

**Structural signal:** A playbook answers "how do I use this skill and when?" — it gives the user activation criteria, step-by-step primary paths, concrete examples, and a troubleshooting reference. It is not a linear procedure; different users will follow different paths through it based on their current need.

**Example in Jerry:** `docs/playbooks/problem-solving.md` — covers when to invoke the problem-solving skill, which of its 9 agents to use for a given task, how to phrase requests, what output to expect, and how to recover from common failures. A user researching a root cause follows a different path through this document than a user validating a deliverable.

**Additional examples of future playbooks (for illustration):**
- `docs/playbooks/adversary.md` — when and how to invoke the adversary skill for quality reviews
- `docs/playbooks/worktracker.md` — how to manage tasks and issues across projects

### Distinction Summary

| Dimension | Runbook | Playbook |
|-----------|---------|---------|
| User intent | Execute a defined procedure | Consult a reference for a recurring skill |
| Reading pattern | Linear, start to finish | Non-linear, section by section |
| Branching | None — sequential steps only | Multiple paths, conditional criteria |
| Start/end state | Explicitly defined | Not applicable (skill reference) |
| Structural template | Prerequisites, Procedure, Verification, Troubleshooting, Next Steps | When to Use, Prerequisites, Step-by-Step, Examples, Troubleshooting, Related Resources |
| Directory placement | `docs/runbooks/` | `docs/playbooks/` |

---

## Directory Structure

This section satisfies REQ-942-002.

### Ratified Structure: Alternative B (Two-Tier Split)

The nse-explorer-001 structure trade study evaluated four alternatives using five weighted criteria (user discoverability, maintenance burden, H-23/H-24 compliance, EN-942 vocabulary alignment, cross-reference coherence). Alternative B scored 4.40 / 5.00 — the highest score by a margin of 1.00 — and is ratified as the FEAT-018 directory structure.

```
docs/
├── INSTALLATION.md                    (existing — not modified by FEAT-018)
├── runbooks/
│   └── getting-started.md             (EN-943 output — getting-started runbook)
└── playbooks/
    ├── PLUGIN-DEVELOPMENT.md          (pre-existing — not modified by FEAT-018)
    ├── problem-solving.md             (EN-944 output — problem-solving skill playbook)
    ├── orchestration.md               (EN-944 output — orchestration skill playbook)
    └── transcript.md                  (EN-944 output — transcript skill playbook)
```

**Note on pre-existing `docs/playbooks/PLUGIN-DEVELOPMENT.md`:** This file is a developer-facing internal playbook that pre-dates FEAT-018. It is not a user-facing skill playbook, and FEAT-018 does not modify it. The `docs/playbooks/` directory already exists at the filesystem level. Only `docs/runbooks/` requires creation before Phase 4 content agents can write output.

### Cross-Reference Paths

Phase 4 content agents MUST use these relative paths when linking between documents:

| Document | References | Relative Path |
|----------|-----------|---------------|
| `docs/runbooks/getting-started.md` | INSTALLATION.md | `../INSTALLATION.md` |
| `docs/runbooks/getting-started.md` | Problem-solving playbook | `../playbooks/problem-solving.md` |
| `docs/runbooks/getting-started.md` | Orchestration playbook | `../playbooks/orchestration.md` |
| `docs/runbooks/getting-started.md` | Transcript playbook | `../playbooks/transcript.md` |
| `docs/playbooks/problem-solving.md` | Authoritative SKILL.md | `../../skills/problem-solving/SKILL.md` |
| `docs/playbooks/problem-solving.md` | Orchestration playbook | `./orchestration.md` |
| `docs/playbooks/problem-solving.md` | Transcript playbook | `./transcript.md` |
| `docs/playbooks/orchestration.md` | Authoritative SKILL.md | `../../skills/orchestration/SKILL.md` |
| `docs/playbooks/orchestration.md` | Problem-solving playbook | `./problem-solving.md` |
| `docs/playbooks/orchestration.md` | Transcript playbook | `./transcript.md` |
| `docs/playbooks/transcript.md` | Authoritative SKILL.md | `../../skills/transcript/SKILL.md` |
| `docs/playbooks/transcript.md` | Problem-solving playbook | `./problem-solving.md` |
| `docs/playbooks/transcript.md` | Orchestration playbook | `./orchestration.md` |

### Rationale for Two-Tier Split

1. **Vocabulary alignment:** Directory names `runbooks/` and `playbooks/` are the EN-942 vocabulary made physical. Content agents writing under `docs/runbooks/` know they are producing a linear procedure. Content agents writing under `docs/playbooks/` know they are producing a reference document. The structural signal eliminates ambiguity that a flat structure would introduce.

2. **Discoverability:** A new user completing INSTALLATION.md has one memorable next step: `docs/runbooks/getting-started.md`. The runbook then points to `docs/playbooks/` for the skill reference layer. The two-step discovery path mirrors the intended user journey.

3. **Maintenance isolation:** Skills evolve independently. When the transcript skill's domain contexts change, only `docs/playbooks/transcript.md` requires updating. The runbook is unaffected. Clean separation prevents coupling that would occur in merged or skill-grouped structures.

4. **Extensibility:** Future runbooks (e.g., `docs/runbooks/project-lifecycle.md`) and playbooks (e.g., `docs/playbooks/adversary.md`) are added as single files without structural change.

---

## Scope Boundaries

This section satisfies REQ-942-003.

### In-Scope Skills

The following three skills are in scope for FEAT-018 playbook creation, per AC-3:

| Skill | Enabler | Output File | Rationale |
|-------|---------|-------------|-----------|
| problem-solving | EN-944 | `docs/playbooks/problem-solving.md` | Named in FEAT-018 AC-3. Highest-frequency skill. Entry point for new users — recommended as the first skill to invoke per EN-943 (lowest friction, no additional prerequisites beyond project setup). |
| orchestration | EN-944 | `docs/playbooks/orchestration.md` | Named in FEAT-018 AC-3. Required for multi-phase workflows that users encounter within days of onboarding. Has explicit "when NOT to use" criteria (single-agent tasks) that must be documented to prevent over-application. |
| transcript | EN-944 | `docs/playbooks/transcript.md` | Named in FEAT-018 AC-3. Has a mandatory two-phase invocation constraint (CLI parse first, then LLM orchestration) that requires explicit documentation to prevent errors. Invoked by explicit CLI argument, not keyword triggers. |

### Out-of-Scope Skills

The following skills are explicitly excluded from FEAT-018. Exclusion applies to FEAT-018 only; future features that add playbooks for excluded skills SHOULD use the two-tier directory structure ratified in this document.

| Skill | Rationale for Exclusion |
|-------|------------------------|
| adversary | Not named in FEAT-018 AC-3. The `/adversary` skill is used in quality-enforcement workflows typically executed by experienced users familiar with the creator-critic-revision cycle and quality gate thresholds. Documenting it before new users have the problem-solving foundation would create confusion. Candidate for a future feature (FEAT-019 or equivalent). |
| worktracker | Not named in FEAT-018 AC-3. The `/worktracker` skill manages task state and is ancillary to the core new-user journey covered by FEAT-018. Its operational documentation is already embedded in `.context/rules/project-workflow.md`. A standalone playbook would largely duplicate existing rule documentation. |
| nasa-se | Not named in FEAT-018 AC-3. The `/nasa-se` skill is used by agent orchestration workflows (requirements definition, V&V, trade studies), not directly by end users in their daily operation. It has no end-user activation keywords in the trigger map and is typically invoked by other skill agents rather than by users directly. |
| architecture | Not named in FEAT-018 AC-3. The `/architecture` skill is an advanced skill for design decision workflows. New users are not expected to invoke it during onboarding. Its use cases presuppose familiarity with the problem-solving and orchestration foundations. |
| bootstrap | Not named in FEAT-018 AC-3. Bootstrap is a one-time setup skill, not a recurring workflow. Its documentation belongs in an installation or setup context (FEAT-017 scope, `docs/INSTALLATION.md`), not in the runbooks/playbooks layer which covers recurring operational workflows. |

---

## Section Templates

This section satisfies REQ-942-004 (playbook template) and REQ-942-005 (runbook template).

### Runbook Template

Runbooks are linear, sequential procedures with a defined start state and end state. The template below defines all required section headings. Phase 4 content agents producing EN-943 output MUST use this template. All five sections are REQUIRED.

**Key distinction from playbook template:** Runbooks use a `Procedure` section with numbered sequential steps (not a `Step-by-Step` with multiple paths). Runbooks include a `Verification` section with a checklist of observable end-state outcomes. Runbooks include a `Next Steps` section pointing to playbooks. Runbooks do not have a `When to Use` section (a runbook is invoked for a specific journey, not chosen from a set of alternatives) and do not have a `Related Resources` section.

```markdown
# {Runbook Title}

> Brief description of what the user will accomplish by following this runbook.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prerequisites](#prerequisites) | What you must have before starting |
| [Procedure](#procedure) | Step-by-step instructions |
| [Verification](#verification) | How to confirm success |
| [Troubleshooting](#troubleshooting) | Common failures and resolutions |
| [Next Steps](#next-steps) | Where to go after completing this runbook |

---

## Prerequisites

> **Start state:** {Describe the exact state the user must be in before following this runbook}

- [ ] Prerequisite 1 (with reference to source document if applicable)
- [ ] Prerequisite 2
- [ ] Prerequisite 3

---

## Procedure

### Step 1: {Step Name}

{Description of what this step does and why it is needed}

    {command if applicable}

Expected output: `{what the user should see}`

### Step 2: {Step Name}

{Continue for all steps. Number all steps. Each step should have one discrete action.}

---

## Verification

> **End state:** {Describe the exact state the user should be in after completing this runbook}

- [ ] Verification item 1 — {observable outcome}
- [ ] Verification item 2 — {observable outcome}
- [ ] Verification item 3 — {observable outcome}

---

## Troubleshooting

| Symptom | Cause | Resolution |
|---------|-------|------------|
| {Failure mode 1} | {Root cause} | {Resolution steps} |
| {Failure mode 2} | {Root cause} | {Resolution steps} |
| {Failure mode 3} | {Root cause} | {Resolution steps} |

---

## Next Steps

After completing this runbook, proceed to:

- [{Document title}]({relative-path}) — {brief description}
```

**Runbook section guidance:**

| Section | Required Content | Minimum |
|---------|-----------------|---------|
| Prerequisites | Start-state checklist; reference to upstream docs; H-04 compliance (JERRY_PROJECT requirement) | 3 checklist items |
| Procedure | Numbered steps; command examples; expected output per step | 4 discrete steps |
| Verification | Observable end-state checklist | 3 checklist items |
| Troubleshooting | Failure mode table (symptom, cause, resolution) | 3 entries |
| Next Steps | Links to playbooks per REQ-943-008 | 1 link minimum |

---

### Playbook Template

Playbooks are reference-oriented documents consulted non-linearly. They contain conditional decision points and multiple usage paths. The template below defines all required section headings. Phase 4 content agents producing EN-944 output MUST use this template. All six sections are REQUIRED.

**Key distinction from runbook template:** Playbooks begin with a `When to Use` section that includes both positive criteria (when to invoke) and negative criteria (when NOT to invoke). Playbooks use a `Step-by-Step` section covering the primary invocation path but may include multiple paths. Playbooks include an `Examples` section with concrete invocation phrases and system behavior descriptions. Playbooks include a `Related Resources` section pointing to SKILL.md and other playbooks. Playbooks do not have a `Verification` section (they are reference documents, not procedures) and do not have a `Next Steps` section.

```markdown
# {Skill Name} Playbook

> **Skill:** {skill-name}
> **SKILL.md:** [{relative-path-label}]({relative-path-to-skill-md})
> **Trigger keywords:** {keywords from mandatory-skill-usage.md, or "CLI invocation" if no keyword triggers}

## Document Sections

| Section | Purpose |
|---------|---------|
| [When to Use](#when-to-use) | Activation criteria and exclusions |
| [Prerequisites](#prerequisites) | What must be in place before invoking |
| [Step-by-Step](#step-by-step) | Primary invocation path |
| [Examples](#examples) | Concrete invocation examples |
| [Troubleshooting](#troubleshooting) | Common failure modes |
| [Related Resources](#related-resources) | Cross-references to other playbooks and SKILL.md |

---

## When to Use

### Use this skill when:

- {Positive criterion 1 — keyword or situation that triggers this skill}
- {Positive criterion 2}
- {Positive criterion 3}

### Do NOT use this skill when:

- {Negative criterion 1 — situations where this skill is NOT the right choice}
- {Negative criterion 2}

---

## Prerequisites

- {Prerequisite 1 — what must exist or be configured before invoking}
- {Prerequisite 2}

---

## Step-by-Step

### Primary Path: {Most common invocation pattern}

1. {Step 1}
2. {Step 2}
3. {Step 3}
4. {Continue as needed}

---

## Examples

### Example 1: {Example title}

**User request:** "{natural language phrase that invokes this skill}"

**System behavior:** {What Claude does — which agent is invoked, what artifact is produced, where it is saved}

### Example 2: {Example title}

**User request:** "{natural language phrase}"

**System behavior:** {What Claude does}

---

## Troubleshooting

| Symptom | Cause | Resolution |
|---------|-------|------------|
| {Failure 1} | {Cause} | {Resolution} |
| {Failure 2} | {Cause} | {Resolution} |
| {Failure 3} | {Cause} | {Resolution} |

---

## Related Resources

- [SKILL.md]({relative-path}) — Authoritative technical reference for this skill
- [{Other playbook}]({relative-path}) — {Why related}
```

**Playbook section guidance:**

| Section | Required Content | Minimum |
|---------|-----------------|---------|
| When to Use | Positive activation criteria + at least one negative criterion | 3 positive, 1 negative |
| Prerequisites | Conditions required for correct invocation (project setup, JERRY_PROJECT, input files, etc.) | 2 items |
| Step-by-Step | Numbered steps for primary invocation path | 4 steps |
| Examples | User request phrase + system behavior description | 2 examples |
| Troubleshooting | Failure mode table (symptom, cause, resolution) | 3 entries |
| Related Resources | SKILL.md link + at least one other playbook cross-reference | 2 links |

---

## Coverage Map

This section satisfies REQ-942-006.

The trigger keyword table in `.context/rules/mandatory-skill-usage.md` defines the keywords that automatically invoke each skill. The coverage map below verifies that each FEAT-018 playbook covers the trigger keywords for its skill. All trigger keywords from mandatory-skill-usage.md are sourced directly from that file.

| Skill | Trigger Keywords (from `.context/rules/mandatory-skill-usage.md`) | Playbook File | Coverage Requirement |
|-------|------------------------------------------------------------------|---------------|----------------------|
| problem-solving | `research`, `analyze`, `investigate`, `explore`, `root cause`, `why` | `docs/playbooks/problem-solving.md` | Playbook "When to Use" section MUST reference all 6 trigger keywords as positive activation criteria. Users must be able to read "When to Use" and recognize the natural language phrases that auto-invoke this skill. |
| orchestration | `orchestration`, `pipeline`, `workflow`, `multi-agent`, `phases`, `gates` | `docs/playbooks/orchestration.md` | Playbook "When to Use" section MUST reference all 6 trigger keywords as positive activation criteria. |
| transcript | *(No entry in mandatory-skill-usage.md trigger map)* | `docs/playbooks/transcript.md` | Playbook "When to Use" section MUST document the CLI invocation syntax (`uv run jerry transcript parse`) as the activation mechanism. There are no keyword triggers to cover; the invocation pattern is explicit CLI argument, not keyword detection. |

**Note on transcript trigger keyword gap:** The transcript skill is not listed in mandatory-skill-usage.md because it is invoked via explicit CLI argument (`uv run jerry transcript parse <file-path>`) rather than through keyword detection in Claude Code. This is not a coverage gap — it reflects the skill's architecture. The transcript playbook's "When to Use" section should explain this distinction explicitly so users understand that the transcript skill does not activate automatically on keyword detection.

**Coverage compliance rule for Phase 4 agents:** Each playbook's "When to Use" section MUST include the exact keywords listed in the table above. These keywords should appear in the positive activation criteria as user-facing guidance (e.g., "Use this skill when you need to research, analyze, or investigate a topic"). This ensures users who read a playbook and users who trigger the skill by natural language will have a consistent activation model.

---

## Deliverable Inventory

This section provides the complete list of files to be produced by EN-943 and EN-944 in Phase 4. Each file's responsible agent and structural template are identified.

### EN-943 Deliverables

| File | Content Agent | Template | Status |
|------|--------------|----------|--------|
| `docs/runbooks/getting-started.md` | ps-synthesizer-001 | Runbook Template (Section 5.1) | Pending Phase 4 |

### EN-944 Deliverables

| File | Content Agent | Template | Skill SKILL.md Source |
|------|--------------|----------|-----------------------|
| `docs/playbooks/problem-solving.md` | ps-synthesizer-002 | Playbook Template (Section 5.2) | `skills/problem-solving/SKILL.md` |
| `docs/playbooks/orchestration.md` | ps-synthesizer-003 | Playbook Template (Section 5.2) | `skills/orchestration/SKILL.md` |
| `docs/playbooks/transcript.md` | ps-synthesizer-004 | Playbook Template (Section 5.2) | `skills/transcript/SKILL.md` |

### Pre-Existing Files (Not Modified by FEAT-018)

| File | Status |
|------|--------|
| `docs/INSTALLATION.md` | Existing — referenced by EN-943; not modified |
| `docs/playbooks/PLUGIN-DEVELOPMENT.md` | Existing — coexists with EN-944 output; not modified |

### Directory Creation Required Before Phase 4

| Directory | Action |
|-----------|--------|
| `docs/runbooks/` | CREATE — does not yet exist |
| `docs/playbooks/` | EXISTS — no action required |

### Total FEAT-018 Output: 4 files (1 runbook + 3 playbooks)

---

## Requirements Traceability

This section satisfies REQ-942-007 (partial — H-23/H-24 compliance is also demonstrated by the navigation table at the top of this document). Each EN-942 requirement is mapped to the section in this document where it is satisfied.

| Requirement ID | Requirement Summary | Satisfied In | Verification Method |
|----------------|---------------------|--------------|---------------------|
| REQ-942-001 | Define "runbook" and "playbook" in Jerry context with examples | [Vocabulary Definitions](#vocabulary-definitions) — both terms defined with examples and distinction summary table | Inspection: both terms defined; each has at least two examples; distinction table present |
| REQ-942-002 | Specify complete directory structure with exact paths | [Directory Structure](#directory-structure) — exact paths for all 4 output files; cross-reference paths for all inter-document links | Inspection: all FEAT-018 output file paths listed; `docs/runbooks/getting-started.md` and all 3 playbook paths present |
| REQ-942-003 | State in-scope skills and explicitly list out-of-scope with rationale | [Scope Boundaries](#scope-boundaries) — 3 in-scope, 5 out-of-scope with per-skill rationale | Inspection: in-scope list matches AC-3 (problem-solving, orchestration, transcript); all 5 exclusions have documented rationale |
| REQ-942-004 | Define standard playbook section template (min: When to Use, Prerequisites, Step-by-Step, Examples, Troubleshooting) | [Section Templates — Playbook Template](#playbook-template) — 6 required sections with content guidance table | Inspection: all 5 minimum sections present (plus Related Resources as 6th); each heading has content guidance |
| REQ-942-005 | Define standard runbook section template (min: Prerequisites, Procedure, Verification, Troubleshooting); must differ from playbook | [Section Templates — Runbook Template](#runbook-template) — 5 required sections; differs from playbook by having Procedure/Verification/Next Steps instead of When to Use/Examples/Related Resources | Inspection: all 4 minimum sections present (plus Next Steps as 5th); structural difference from playbook documented |
| REQ-942-006 | Include coverage map showing trigger keyword coverage per playbook | [Coverage Map](#coverage-map) — table mapping mandatory-skill-usage.md keywords to playbook coverage requirements; transcript invocation gap explained | Analysis: problem-solving (6 keywords), orchestration (6 keywords), transcript (CLI invocation — no keyword triggers) |
| REQ-942-007 | Scope document itself complies with H-23 and H-24 | [Document Sections](#document-sections) — navigation table present after frontmatter; all ## headings use anchor links; document exceeds 30 lines | Inspection: navigation table at document top; anchor links used throughout; all 8 major sections listed in table |

### Constraint Compliance Notes

- **H-23 (navigation table REQUIRED):** Navigation table is present at document top, after frontmatter, listing all 8 major sections with anchor links. This document exceeds 30 lines — no exemption applies.
- **H-24 (anchor links REQUIRED):** All navigation table entries use anchor links in the format `[Section Name](#section-name)`. All `##` section headings are lowercase-hyphenated in their anchor targets.
- **P-002 (persist output):** This document is persisted to the repository under `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-3/ps-architect-002/`. It is an internal planning artifact, not user-facing documentation, and is correctly placed outside `docs/`.
- **P-022 (no deception):** The trade study recommendation from nse-explorer-001 was adopted without alteration. The trade study disclaimer (P-043) noting agent-produced analysis is preserved by reference; this scope document ratifies the recommendation on its merits, not by assertion.

---

*Agent: ps-architect-002*
*Workflow: epic001-docs-20260218-001*
*Phase: 3*
*Output: `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-3/ps-architect-002/ps-architect-002-feat018-scope.md`*
