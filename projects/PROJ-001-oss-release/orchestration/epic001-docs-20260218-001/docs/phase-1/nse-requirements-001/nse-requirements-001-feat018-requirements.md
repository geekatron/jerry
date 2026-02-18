# FEAT-018 Documentation Requirements — Runbooks & Playbooks

> **Agent ID:** nse-requirements-001
> **Workflow ID:** epic001-docs-20260218-001
> **Phase:** 1 (Requirements & Gap Analysis)
> **Date:** 2026-02-18
> **Feature:** FEAT-018 — User Documentation: Runbooks & Playbooks
> **Method:** NASA Systems Engineering Requirements Definition (ADIT V&V)

---

> **MANDATORY DISCLAIMER (P-043):** This document was produced using NASA Systems Engineering
> requirements definition practices applied to a software documentation context. Requirements
> use the SHALL/SHOULD/MAY tier vocabulary defined in `.context/rules/quality-enforcement.md`.
> All requirements are traceable to FEAT-018 acceptance criteria. Verification methods use the
> ADIT (Analysis, Demonstration, Inspection, Test) framework. This document is an agent-produced
> artifact and has not been independently reviewed. All SHALL statements reflect documented
> FEAT-018 scope; they do not impose obligations beyond what the parent feature defines.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Non-technical stakeholder summary |
| [L1: Technical Requirements — EN-942](#l1-technical-requirements--en-942-scope--structure) | Scope and structure requirements |
| [L1: Technical Requirements — EN-943](#l1-technical-requirements--en-943-getting-started-runbook) | Getting-started runbook requirements |
| [L1: Technical Requirements — EN-944](#l1-technical-requirements--en-944-skill-usage-playbooks) | Skill playbook requirements |
| [L2: Systems Perspective](#l2-systems-perspective) | Traceability, directory structure, risks, integration |

---

## L0: Executive Summary

FEAT-018 delivers the first formal user documentation layer for the Jerry framework — specifically, the runbooks and playbooks that transform Jerry from a system that experts can use into a system that new users can successfully operate. Without this documentation, the gap between a successful installation (covered by FEAT-017) and productive daily use remains unbridged. Users who complete installation have no structured guidance on how to configure a project, activate skills, or work within Jerry's quality-enforcement model.

The feature is organized into three enablers. EN-942 establishes definitions and structure: it answers the question "what are we building and where does it live?" before any content is written. EN-943 delivers the getting-started runbook — a linear, user-journey-oriented guide that takes a freshly-installed Jerry user from zero context to their first successful skill invocation. EN-944 delivers three skill-specific playbooks covering the problem-solving, orchestration, and transcript skills, giving users reference material for their most common daily workflows.

All documentation produced under FEAT-018 must comply with the Jerry markdown navigation standards (H-23, H-24), which require navigation tables and anchor links in all markdown files exceeding 30 lines. This is a non-negotiable compliance requirement, not a style preference. The requirements in this document are organized by enabler, verified using the ADIT method, and traced to the four FEAT-018 acceptance criteria.

---

## L1: Technical Requirements — EN-942 (Scope & Structure)

### EN-942 Context

EN-942 defines the vocabulary and directory organization for all FEAT-018 documentation. Its output — a scope document — is a prerequisite for EN-943 and EN-944. Content agents for those enablers cannot produce consistent, correctly-organized output without a ratified scope document.

In the Jerry context, the distinction between runbook and playbook is:
- **Runbook:** A linear, sequential procedure oriented around a specific user journey or operational task. Has a defined start state and end state. Intended to be followed step-by-step. Example: getting started, project setup, session lifecycle.
- **Playbook:** A reference-oriented document covering a skill or recurring workflow pattern. Contains conditional decision points, multiple paths, and troubleshooting guidance. Intended to be consulted non-linearly. Example: how to use problem-solving, how to orchestrate a multi-phase workflow.

This distinction governs naming, placement, and structural templates for all FEAT-018 output.

### EN-942 Requirements Table

| ID | Requirement (SHALL statement) | Rationale | Parent AC | V-Method | Priority |
|----|-------------------------------|-----------|-----------|----------|----------|
| REQ-942-001 | The scope document SHALL define the terms "runbook" and "playbook" in the Jerry context with examples of each. | Eliminates ambiguity for content agents in Phases 3 and 4; ensures EN-943 and EN-944 outputs are structurally consistent. | AC-1 | Inspection: verify both terms defined with at least one example each | High |
| REQ-942-002 | The scope document SHALL specify the complete directory structure under `docs/` for all FEAT-018 output files, including exact paths for the getting-started runbook and each skill playbook. | Directory structure decided once prevents path inconsistency across multiple content agents. | AC-1 | Inspection: verify all FEAT-018 output file paths are listed | High |
| REQ-942-003 | The scope document SHALL state which skills are in scope for FEAT-018 playbooks and explicitly list out-of-scope skills with rationale. | Prevents scope creep during content creation; aligns with AC-3 requirement for exactly 3 playbooks. | AC-1 | Inspection: verify in-scope list matches AC-3 (problem-solving, orchestration, transcript); verify at least one exclusion is documented | High |
| REQ-942-004 | The scope document SHALL define a standard playbook section template with required section headings (at minimum: When to Use, Prerequisites, Step-by-Step, Examples, Troubleshooting). | Structural consistency across all three playbooks reduces cognitive load for users switching between them. | AC-1 | Inspection: verify template headings are listed and each heading has a brief description of expected content | Medium |
| REQ-942-005 | The scope document SHALL define a standard runbook section template with required headings (at minimum: Prerequisites, Procedure, Verification, Troubleshooting). | Consistent runbook structure enables users to build procedural muscle memory across multiple runbooks. | AC-1 | Inspection: verify template headings listed; differ from playbook template | Medium |
| REQ-942-006 | The scope document SHALL include a coverage map showing which skill trigger keywords (from `.context/rules/mandatory-skill-usage.md`) are addressed by each planned playbook. | Ensures playbook coverage is aligned with actual skill invocation patterns; closes the loop between trigger-based activation and documentation. | AC-1 | Analysis: verify each playbook's coverage section includes trigger keywords from mandatory-skill-usage.md for that skill | Medium |
| REQ-942-007 | The scope document itself SHALL comply with H-23 and H-24 (navigation table with anchor links, required for documents over 30 lines). | The scope document is a Claude-consumed markdown file and is not exempt from the navigation standards it is defining. | AC-4 | Inspection: verify navigation table present; verify all section headings use anchor links | High |

---

## L1: Technical Requirements — EN-943 (Getting-Started Runbook)

### EN-943 Context

EN-943 produces the getting-started runbook. The user journey it covers begins at the point after installation is complete (FEAT-017 output) and ends at the moment the user successfully invokes their first Jerry skill. This journey has four distinct milestones:

1. **Project initialization** — creating a project directory using `jerry projects` CLI and confirming `JERRY_PROJECT` is set
2. **Session start** — running `jerry session start` and interpreting the `<project-context>` tag in the hook output
3. **Skill invocation** — invoking one skill (recommended: problem-solving, as the lowest-friction entry point)
4. **Verification** — confirming the skill produced a persisted output artifact

The runbook must not duplicate INSTALLATION.md content. Where setup steps are required as prerequisites, the runbook SHALL reference INSTALLATION.md by path rather than repeating its content.

### EN-943 Requirements Table

| ID | Requirement (SHALL statement) | Rationale | Parent AC | V-Method | Priority |
|----|-------------------------------|-----------|-----------|----------|----------|
| REQ-943-001 | The getting-started runbook SHALL cover the complete user journey from post-installation state through first successful skill invocation, without gaps that require user inference. | Users arriving from FEAT-017 have no Jerry domain knowledge; any gap in the runbook produces a support escalation. | AC-2 | Demonstration: follow the runbook as written from a clean post-install state; verify no step requires knowledge not provided | High |
| REQ-943-002 | The runbook SHALL begin with an explicit "Prerequisites" section that references `docs/INSTALLATION.md` by relative path and states what a completed installation means (uv present, jerry cloned, plugin installed in Claude Code). | Prerequisites define the assumed start state; without this, users at different stages of installation will have inconsistent experiences. | AC-2 | Inspection: verify Prerequisites section present; verify INSTALLATION.md referenced; verify exactly 3 completion criteria listed | High |
| REQ-943-003 | The runbook SHALL include a step for setting the `JERRY_PROJECT` environment variable, with both a command example and an explanation of why this variable is required (H-04 compliance). | H-04 makes this variable mandatory; users will be blocked without it; explanation builds mental model for the hard constraint. | AC-2 | Inspection: verify `JERRY_PROJECT` command example present; verify H-04 is cited or explained | High |
| REQ-943-004 | The runbook SHALL include a step for running `jerry session start`, show expected output (including the `<project-context>` hook tag), and explain what each hook tag response means. | SessionStart hook output is non-obvious; users who do not understand `<project-context>` vs `<project-required>` vs `<project-error>` cannot proceed correctly. | AC-2 | Inspection: verify `jerry session start` command shown; verify all three hook tag variants documented | High |
| REQ-943-005 | The runbook SHALL guide the user through invoking the problem-solving skill as the recommended first skill, including an example invocation phrase and the expected location of the output artifact. | Problem-solving is the lowest-friction entry point (no prerequisites beyond project setup); demonstrates the core value proposition of Jerry. | AC-2 | Demonstration: execute the invocation phrase shown; verify a persisted artifact is created at the stated location | High |
| REQ-943-006 | The runbook SHALL include a "Verification" section that gives the user a checklist of observable outcomes confirming the runbook was followed successfully. | Checklist provides a binary success/failure signal; reduces user uncertainty about whether they completed the workflow correctly. | AC-2 | Inspection: verify Verification section present with at least 3 checklist items covering project setup, session start, and skill output | Medium |
| REQ-943-007 | The runbook SHALL include a "Troubleshooting" section covering at minimum: `JERRY_PROJECT` not set (H-04 violation), session start with `<project-required>` response, and no output artifact created after skill invocation. | These are the three highest-probability failure modes for new users; documented resolution steps prevent abandonment. | AC-2 | Inspection: verify Troubleshooting section has all three failure modes with resolution steps | Medium |
| REQ-943-008 | The runbook SHALL include a "Next Steps" section pointing to the skill playbooks created by EN-944, referenced by relative path. | Guides the user from the linear runbook into the reference-oriented playbooks; closes the documentation flow. | AC-2 | Inspection: verify Next Steps section present; verify at least one skill playbook path referenced | Low |
| REQ-943-009 | The runbook SHALL comply with H-23 and H-24 (navigation table with anchor links). | Document is over 30 lines; no exemption from Jerry navigation standards applies. | AC-4 | Inspection: verify navigation table present after frontmatter; verify all ## headings use anchor links | High |

---

## L1: Technical Requirements — EN-944 (Skill Usage Playbooks)

### EN-944 Context

EN-944 produces three skill playbooks. The skills are specified by FEAT-018 AC-3: problem-solving, orchestration, and transcript. Each playbook is a reference document — not a linear tutorial — that an experienced user can consult when choosing or executing a skill workflow.

The skill definitions (SKILL.md files) provide the authoritative content source for each playbook. Playbook authors must read the corresponding SKILL.md before drafting. Key content to extract per skill:

- **problem-solving:** 9 specialized agents (researcher, analyst, architect, critic, validator, synthesizer, reviewer, investigator, reporter), activation keywords, creator-critic-revision cycle, criticality levels C1-C4, output artifact structure under `docs/`
- **orchestration:** 3 agents (orch-planner, orch-tracker, orch-synthesizer), cross-pollinated pipeline pattern, sync barrier concept, ORCHESTRATION.yaml state schema, when NOT to use orchestration (single agent task)
- **transcript:** VTT/SRT/plain text parsing, mandatory CLI invocation via `uv run jerry transcript parse`, 9 domain contexts (general, transcript, meeting, software-engineering, software-architecture, product-management, user-experience, cloud-engineering, security-engineering), Phase 1 (CLI parse) vs Phase 2+ (LLM agent orchestration) distinction

### EN-944 Requirements Table — Structural Requirements (All Playbooks)

| ID | Requirement (SHALL statement) | Rationale | Parent AC | V-Method | Priority |
|----|-------------------------------|-----------|-----------|----------|----------|
| REQ-944-001 | Each playbook SHALL include a "When to Use" section with positive activation criteria (when to invoke the skill) and at least one negative criterion (when NOT to use). | Without negative criteria, users over-apply skills, creating unnecessary complexity. The orchestration skill explicitly warns against single-agent use; this pattern must be replicated. | AC-3 | Inspection: verify When to Use section present; verify at least one negative criterion documented | High |
| REQ-944-002 | Each playbook SHALL include a "Prerequisites" section specifying what the user must have completed or have available before invoking the skill. | Prevents mid-workflow failures when users invoke skills without required context (e.g., no project set, JERRY_PROJECT unset, no input file for transcript). | AC-3 | Inspection: verify Prerequisites section present in all three playbooks | High |
| REQ-944-003 | Each playbook SHALL include a "Step-by-Step" section with numbered, discrete steps for the most common invocation path. | Numbered steps are the primary reference pattern for users who are executing but not yet expert; discrete steps allow users to resume after interruption. | AC-3 | Inspection: verify Step-by-Step section present; verify steps are numbered; verify at least one complete invocation path is covered | High |
| REQ-944-004 | Each playbook SHALL include an "Examples" section with at least two concrete invocation examples showing both the user's natural language request and the resulting agent/CLI behavior. | Concrete examples reduce the translation gap between "what should I say?" and "what will happen?"; single examples are insufficient as they suggest only one valid pattern. | AC-3 | Inspection: verify Examples section with >= 2 examples; verify each example shows both user request and system behavior | High |
| REQ-944-005 | Each playbook SHALL include a "Troubleshooting" section with at least three common failure modes and their resolutions. | Three failure modes is the minimum for a non-trivial skill; fewer entries suggest incomplete coverage of known failure paths. | AC-3 | Inspection: verify Troubleshooting section with >= 3 entries per playbook | Medium |
| REQ-944-006 | Each playbook SHALL comply with H-23 and H-24 (navigation table with anchor links, for documents over 30 lines). | All three playbooks will exceed 30 lines; no exemption applies. | AC-4 | Inspection: verify navigation table present in all three playbooks; verify anchor links used | High |
| REQ-944-007 | Each playbook SHALL include a cross-reference section linking to related playbooks and to the SKILL.md source document. | Cross-references allow users to navigate between related skills (e.g., problem-solving and orchestration are frequently combined); SKILL.md link provides the authoritative technical reference. | AC-3 | Inspection: verify Related Resources or equivalent section present; verify SKILL.md path cited; verify at least one other playbook cross-referenced | Medium |

### EN-944 Requirements Table — Problem-Solving Playbook

| ID | Requirement (SHALL statement) | Rationale | Parent AC | V-Method | Priority |
|----|-------------------------------|-----------|-----------|----------|----------|
| REQ-944-010 | The problem-solving playbook SHALL document all 9 available agents with their roles, invocation triggers, and output locations. | The agent selection decision is the primary cognitive challenge for problem-solving skill users; documentation of all 9 agents in one place eliminates the need to read SKILL.md for basic agent selection. | AC-3 | Inspection: verify all 9 agents listed (researcher, analyst, architect, critic, validator, synthesizer, reviewer, investigator, reporter) with role and output location | High |
| REQ-944-011 | The problem-solving playbook SHALL document the creator-critic-revision cycle (H-14) and quality threshold (H-13 >= 0.92 for C2+) as a behavioral expectation users will observe during C2+ workflows. | Users who do not understand the creator-critic cycle are confused when Claude produces multiple revision rounds; framing this as expected behavior prevents premature interruption. | AC-3 | Inspection: verify H-14 creator-critic cycle documented; verify H-13 threshold cited; verify at least one example of when it activates (C2+ deliverable) | Medium |
| REQ-944-012 | The problem-solving playbook SHALL include an agent selection decision table mapping user keywords to recommended agents. | Keyword-to-agent mapping is the fastest path from user intent to correct invocation; reduces reliance on user expertise in agent capabilities. | AC-3 | Inspection: verify decision table or equivalent mapping present; verify coverage of at least 8 keywords from SKILL.md activation-keywords list | Medium |

### EN-944 Requirements Table — Orchestration Playbook

| ID | Requirement (SHALL statement) | Rationale | Parent AC | V-Method | Priority |
|----|-------------------------------|-----------|-----------|----------|----------|
| REQ-944-020 | The orchestration playbook SHALL explain the three workflow patterns (cross-pollinated pipeline, sequential with checkpoints, fan-out/fan-in) with ASCII diagram or equivalent visual representation for each. | Visual representation of workflow patterns is essential for users to match their coordination need to the correct pattern; text description alone is insufficient for structural concepts. | AC-3 | Inspection: verify all three patterns named; verify at least one ASCII diagram or equivalent visual present | High |
| REQ-944-021 | The orchestration playbook SHALL document the three core artifacts (ORCHESTRATION_PLAN.md, ORCHESTRATION_WORKTRACKER.md, ORCHESTRATION.yaml) with their purposes and audiences. | Users who do not understand the three-artifact model cannot track or resume orchestrated workflows; this is the minimum viable mental model for the skill. | AC-3 | Inspection: verify all three artifacts documented with purpose and audience | High |
| REQ-944-022 | The orchestration playbook SHALL include the criterion for when NOT to use orchestration (single agent task, simple sequential flow, no cross-session state needed) as stated in the SKILL.md. | Over-application of orchestration is a known anti-pattern (SKILL.md documents it explicitly); the playbook must preserve this negative criterion to prevent unnecessary complexity. | AC-3 | Inspection: verify "Do NOT use when" criteria present; verify all three conditions from SKILL.md listed | High |
| REQ-944-023 | The orchestration playbook SHALL document the P-003 compliance constraint — orchestration agents are workers invoked by main context, not recursive subagents — and explain its practical implication for users. | P-003 is a constitutional hard constraint; users who attempt to invoke orchestration agents recursively will receive unexplained failures; proactive documentation prevents this. | AC-3 | Inspection: verify P-003 compliance mentioned; verify practical implication stated (e.g., "do not ask orch-planner to spawn other orchestration agents") | Medium |

### EN-944 Requirements Table — Transcript Playbook

| ID | Requirement (SHALL statement) | Rationale | Parent AC | V-Method | Priority |
|----|-------------------------------|-----------|-----------|----------|----------|
| REQ-944-030 | The transcript playbook SHALL document the mandatory two-phase workflow: Phase 1 (CLI parse via `uv run jerry transcript parse`) and Phase 2+ (LLM agent orchestration on chunk output). | The CLI invocation is mandatory (SKILL.md states it explicitly); users who attempt to have Claude parse VTT directly will produce errors or severely degraded results. | AC-3 | Inspection: verify Phase 1 CLI command documented with correct syntax including `uv run`; verify Phase 2 agent workflow described | High |
| REQ-944-031 | The transcript playbook SHALL document all three supported input formats (VTT, SRT, plain text) with the command syntax variant for each. | Users present transcripts in all three formats; format-specific guidance prevents CLI invocation errors. | AC-3 | Inspection: verify all three formats documented; verify command example shown for at least VTT (primary) and one other | High |
| REQ-944-032 | The transcript playbook SHALL document the 9 available domain contexts (general, transcript, meeting, software-engineering, software-architecture, product-management, user-experience, cloud-engineering, security-engineering) with a brief description of when each applies. | Domain selection determines extraction quality; users who default to general lose professional entity types; a domain selection guide in the playbook enables correct domain choice without consulting SKILL.md. | AC-3 | Inspection: verify all 9 domains listed; verify at least one-line description of applicable meeting type for each | Medium |
| REQ-944-033 | The transcript playbook SHALL warn users NEVER to read `canonical-transcript.json` into context and explain the recommended alternative (use `index.json` and `chunks/chunk-*.json`). | This is a documented constraint in SKILL.md's large file handling guidance; violation causes context window exhaustion; a warning in the playbook is the primary mitigation. | AC-3 | Inspection: verify NEVER read canonical-transcript.json warning present; verify index.json and chunks alternative documented | High |

---

## L2: Systems Perspective

### Traceability Matrix

| Requirement ID | Parent Enabler | Parent AC | Feature |
|----------------|---------------|-----------|---------|
| REQ-942-001 through REQ-942-007 | EN-942 | AC-1, AC-4 | FEAT-018 |
| REQ-943-001 through REQ-943-009 | EN-943 | AC-2, AC-4 | FEAT-018 |
| REQ-944-001 through REQ-944-007 | EN-944 (all playbooks) | AC-3, AC-4 | FEAT-018 |
| REQ-944-010 through REQ-944-012 | EN-944 (problem-solving) | AC-3 | FEAT-018 |
| REQ-944-020 through REQ-944-023 | EN-944 (orchestration) | AC-3 | FEAT-018 |
| REQ-944-030 through REQ-944-033 | EN-944 (transcript) | AC-3 | FEAT-018 |

#### AC Coverage Verification

| AC | Description | Covering Requirements |
|----|-------------|----------------------|
| AC-1 | Scope document defines runbook vs playbook distinction and coverage plan | REQ-942-001, REQ-942-002, REQ-942-003, REQ-942-006 |
| AC-2 | Getting-started runbook covers initial setup through first skill invocation | REQ-943-001 through REQ-943-008 |
| AC-3 | At least 3 skill playbooks created (problem-solving, orchestration, transcript) | REQ-944-001 through REQ-944-007, REQ-944-010 through REQ-944-033 |
| AC-4 | All documentation follows Jerry markdown navigation standards (H-23, H-24) | REQ-942-007, REQ-943-009, REQ-944-006 |

All four FEAT-018 acceptance criteria are covered. No AC is uncovered.

---

### Directory Structure Recommendation

The following directory structure is recommended for all FEAT-018 output. This recommendation SHALL be ratified by the EN-942 scope document; content agents in Phases 3 and 4 must use this structure or the structure ratified by EN-942.

```
docs/
├── INSTALLATION.md                          # Existing (FEAT-017 output, not modified by FEAT-018)
├── runbooks/
│   └── getting-started.md                   # EN-943 output
└── playbooks/
    ├── problem-solving.md                    # EN-944 output (problem-solving skill)
    ├── orchestration.md                      # EN-944 output (orchestration skill)
    └── transcript.md                         # EN-944 output (transcript skill)
```

**Rationale for `docs/runbooks/` and `docs/playbooks/` separation:**
- Runbooks and playbooks have distinct information architectures (linear procedure vs. reference); separate directories signal this to users and content agents.
- Separation allows future addition of runbooks (e.g., `project-lifecycle.md`) and playbooks (e.g., `adversary.md`) without restructuring.
- Consistent with the vocabulary distinction defined in EN-942.

**Note on `docs/` scope document:**
- The EN-942 scope document is an internal planning artifact, not user-facing documentation. It SHOULD be placed under `projects/PROJ-001-oss-release/work/en-942-scope.md`, not under `docs/`. The `docs/` directory is reserved for user-facing documentation.

---

### Risk Assessment

#### EN-942 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Scope document is too prescriptive and over-constrains content agents in later phases | Low | Medium | Scope document should define structure and required sections, not prescribe word-for-word content; leave authorial discretion to content agents |
| Runbook/playbook distinction is insufficiently clear, causing content agents to blur the boundary | Medium | Medium | Requirements REQ-942-001 through REQ-942-005 require templates for both types; structural differences (numbered steps vs. conditional paths) enforce the distinction |
| Coverage map omits a skill that should be documented | Low | Low | AC-3 explicitly names three skills; EN-942 coverage map need only match AC-3; additional skills are out of scope for FEAT-018 |

#### EN-943 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Runbook assumes FEAT-017 content (INSTALLATION.md) that has not yet been finalized when EN-943 is authored | Medium | High | REQ-943-002 requires a reference to INSTALLATION.md rather than duplication; if INSTALLATION.md changes, only the reference needs updating, not the runbook content |
| `jerry session start` hook output varies by project state, causing runbook examples to be wrong for some users | Medium | Medium | REQ-943-004 requires documentation of all three hook tag variants; the runbook SHOULD use a generic project context example, not a project-specific one |
| User journey has gaps that only appear during real user testing | Medium | High | REQ-943-001 requires the Demonstration V-method; the requirements document cannot itself close this gap — it must be closed by Phase 4 content creation with an actual test walkthrough |

#### EN-944 Risks

| Risk | Likelihood | Impact | Mitionale |
|------|-----------|--------|------------|
| Playbook content becomes stale as SKILL.md files are updated (version drift) | High | Medium | REQ-944-007 requires each playbook to cite its SKILL.md source; a note in each playbook header stating the SKILL.md version used at authoring time provides traceability. Phase governance should treat SKILL.md version updates as a trigger for playbook review. |
| Transcript playbook Phase 1/Phase 2 distinction is misunderstood by content agents, leading to incorrect CLI examples | Medium | High | REQ-944-030 requires the CLI command with exact syntax (`uv run jerry transcript parse`); the V-method (Inspection) catches omission of `uv run` |
| Problem-solving agent table becomes the entire playbook, with insufficient workflow guidance | Medium | Medium | REQ-944-010 requires the table; REQ-944-012 requires a keyword-to-agent decision table; REQ-944-011 requires creator-critic cycle documentation; together these require at least three substantive sections beyond a simple list |

---

### Integration with Existing Documentation

#### INSTALLATION.md (FEAT-017 Output)

The getting-started runbook (EN-943) is a downstream consumer of INSTALLATION.md. The integration contract is:

- EN-943 SHALL reference INSTALLATION.md by relative path: `../INSTALLATION.md`
- EN-943 SHALL state the assumed post-installation state (three observable outcomes: uv present, jerry cloned, plugin installed) rather than restating installation steps
- If INSTALLATION.md is modified after EN-943 is authored, the INSTALLATION.md owner is responsible for verifying the three assumed outcomes remain accurate

#### CLAUDE.md (Root Context)

CLAUDE.md contains the Quick Reference skill table — the authoritative list of available skills and their purposes. The FEAT-018 playbooks are complementary to, not a replacement for, CLAUDE.md. The integration contract is:

- CLAUDE.md skill table entries remain the single-line authoritative trigger reference
- EN-944 playbooks expand each skill entry into full reference documentation
- FEAT-018 documents SHOULD NOT modify CLAUDE.md; if the skill table needs updating, that is a separate work item outside FEAT-018 scope

#### mandatory-skill-usage.md (Trigger Keywords)

The trigger keyword table in `.context/rules/mandatory-skill-usage.md` defines when skills are invoked. The EN-942 coverage map (REQ-942-006) must align playbook coverage with these triggers. The integration contract is:

- EN-942 scope document SHALL read `.context/rules/mandatory-skill-usage.md` before defining the coverage map
- Each playbook SHOULD include the trigger keywords for its skill as user-facing activation guidance (so users know which phrases invoke the skill automatically)

#### Quality Enforcement (SSOT)

Requirements REQ-944-011 (creator-critic cycle) and REQ-944-023 (P-003 constraint) reference quality enforcement and constitutional rules. The integration contract is:

- Playbooks referencing H-13, H-14, H-23, H-24, or P-003 SHALL cite the rule ID (not paraphrase without citation), ensuring traceability to `.context/rules/quality-enforcement.md`

---

*Agent: nse-requirements-001*
*Workflow: epic001-docs-20260218-001*
*Phase: 1*
*Output: `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-1/nse-requirements-001/nse-requirements-001-feat018-requirements.md`*
