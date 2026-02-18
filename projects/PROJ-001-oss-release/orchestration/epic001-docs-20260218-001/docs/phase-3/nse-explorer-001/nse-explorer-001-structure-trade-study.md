# FEAT-018 Structure Trade Study — Runbooks & Playbooks

> **Agent ID:** nse-explorer-001
> **Workflow ID:** epic001-docs-20260218-001
> **Phase:** 3 (FEAT-018 Scope & Structure)
> **Date:** 2026-02-18
> **Feature:** FEAT-018 — User Documentation: Runbooks & Playbooks
> **Method:** NASA Systems Engineering Trade Study (Weighted Additive Scoring)
> **Criticality:** C2 (Standard)

---

> **MANDATORY DISCLAIMER (P-043):** This document was produced using NASA Systems Engineering
> trade study methodology applied to a software documentation structure decision context. Alternatives
> were evaluated using a weighted additive scoring matrix against five criteria derived from FEAT-018
> acceptance criteria and quality enforcement rules. All scores represent agent-produced analysis and
> have not been independently verified. The recommendation in this document constitutes input to the
> EN-942 scope document; final ratification rests with the project owner.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Stakeholder-facing trade study conclusion |
| [L1: Trade Study](#l1-trade-study) | Decision statement, criteria, alternatives, scoring matrix |
| [L2: Recommendation](#l2-recommendation) | Recommended structure, file paths, migration path, risks |
| [Section Template Definitions](#section-template-definitions) | Runbook and playbook standard templates per EN-942 |
| [Scope Boundaries](#scope-boundaries) | In-scope and out-of-scope skills per REQ-942-003 |

---

## L0: Executive Summary

FEAT-018 requires a user documentation layer covering one getting-started runbook and three skill playbooks. Before content can be authored, the directory structure under `docs/` must be decided — this decision affects how users discover documentation, how content agents produce consistent output, and how the repository evolves when additional runbooks or playbooks are added in future features. Four structural alternatives were evaluated: a flat `docs/` root placement, a two-tier runbooks/playbooks split, a skill-grouped guides hierarchy, and a single merged guide per skill. The evaluation applied five weighted criteria derived from FEAT-018 acceptance criteria and the Jerry navigation standards. The two-tier split — `docs/runbooks/getting-started.md` plus `docs/playbooks/{skill}.md` — scores highest (4.05 / 5.00) because it maps the vocabulary distinction defined in EN-942 directly onto the directory structure, achieves the best discoverability for new users navigating from INSTALLATION.md, carries the lowest maintenance burden when individual skills evolve, and extends cleanly to future runbooks and playbooks without restructuring. This recommendation aligns with the directory structure proposed by nse-requirements-001.

---

## L1: Trade Study

### Decision Statement

**What is the optimal documentation structure for FEAT-018 runbooks and playbooks under the `docs/` directory?**

This is a one-time structural decision. Once content agents begin authoring under a chosen structure, path-level changes require cross-document link correction and impose rework. The decision must be made before Phase 4 (content creation) begins.

---

### Evaluation Criteria

Five criteria were selected. Each criterion maps to at least one FEAT-018 acceptance criterion or an established quality rule.

| ID | Criterion | Weight | Rationale |
|----|-----------|--------|-----------|
| C1 | **User discoverability** — How easily can a new user arriving from INSTALLATION.md locate the documentation they need? | 0.30 | Highest weight: discoverability is the primary purpose of the documentation layer (FEAT-018 scope statement). |
| C2 | **Maintenance burden** — How much effort is required to keep the structure correct as skills evolve, new playbooks are added, or existing runbooks are revised? | 0.25 | Second highest: version drift between SKILL.md and playbooks is identified as a HIGH likelihood risk in nse-requirements-001. Structure that minimizes cross-document coupling reduces this risk. |
| C3 | **Navigation standard compliance** — Does the structure support or constrain H-23/H-24 compliance (navigation tables with anchor links)? | 0.20 | H-23 and H-24 are HARD rules; non-compliance is a constitutional violation (AC-4). The structure must not make compliance harder to enforce. |
| C4 | **EN-942 vocabulary alignment** — Does the physical structure reflect the runbook/playbook distinction defined in REQ-942-001 through REQ-942-005? | 0.15 | The vocabulary distinction is the organizing principle of EN-942; a structure that contradicts it would require constant cognitive translation by users and content agents. |
| C5 | **Cross-reference coherence** — How well do links between documents hold together (from INSTALLATION.md to runbook to playbooks, and between playbooks)? | 0.10 | Cross-reference correctness is tested by REQ-943-002 (runbook references INSTALLATION.md) and REQ-944-007 (playbooks cross-reference each other and SKILL.md). |

**Scoring scale:** 1 = poor, 2 = below average, 3 = average, 4 = good, 5 = excellent.

---

### Alternatives

#### Alternative A: Flat `docs/` Structure

All FEAT-018 output files are placed directly in the `docs/` root alongside INSTALLATION.md and BOOTSTRAP.md.

```
docs/
├── INSTALLATION.md         (existing)
├── BOOTSTRAP.md            (existing)
├── getting-started.md      (EN-943 output)
├── problem-solving.md      (EN-944 output)
├── orchestration.md        (EN-944 output)
└── transcript.md           (EN-944 output)
```

**Strengths:**
- Minimal structure — no subdirectory navigation required.
- All docs discoverable from a single `ls docs/` inspection.
- Zero migration effort to establish structure.

**Weaknesses:**
- `docs/` root already contains ADRs, analysis, design, governance, knowledge, schemas, and specifications subdirectories plus two existing files. Adding four more root-level files increases visual noise significantly.
- Provides no structural signal distinguishing runbooks from playbooks — the vocabulary distinction of EN-942 is invisible at the filesystem level.
- Future growth (additional runbooks, additional playbooks) compounds the naming problem without a clear organizing principle.
- `problem-solving.md`, `orchestration.md`, and `transcript.md` are ambiguous filenames — they could be descriptions of concepts rather than usage guides. No type signal in the name or path.

**Score against criteria:**

| Criterion | Score | Justification |
|-----------|-------|---------------|
| C1 User discoverability | 3 | Files are reachable but names lack type signal. A user scanning `docs/` cannot distinguish a playbook from a specification or design document without reading each file. |
| C2 Maintenance burden | 4 | No subdirectory structure to maintain; adding a file is simple. Risk: file proliferation makes root-level organization harder over time. |
| C3 Nav standard compliance | 4 | Structure imposes no constraint on internal navigation tables; H-23/H-24 compliance is purely a per-file concern. |
| C4 EN-942 vocabulary alignment | 1 | Flat structure provides zero structural signal for runbook vs. playbook distinction. The vocabulary decision becomes invisible at the filesystem level. |
| C5 Cross-reference coherence | 3 | Relative paths are simple (`./problem-solving.md`) but provide no type context. |

**Weighted score:** (3×0.30) + (4×0.25) + (4×0.20) + (1×0.15) + (3×0.10) = 0.90 + 1.00 + 0.80 + 0.15 + 0.30 = **3.15**

---

#### Alternative B: Two-Tier Split (`docs/runbooks/` + `docs/playbooks/`)

Runbooks and playbooks are separated into two subdirectories. This is the structure recommended by nse-requirements-001.

```
docs/
├── INSTALLATION.md              (existing)
├── runbooks/
│   └── getting-started.md       (EN-943 output)
└── playbooks/
    ├── problem-solving.md        (EN-944 output)
    ├── orchestration.md          (EN-944 output)
    └── transcript.md             (EN-944 output)
```

**Strengths:**
- Directory names `runbooks/` and `playbooks/` map directly onto EN-942 vocabulary, reinforcing the distinction for both users and content agents.
- Users navigating from INSTALLATION.md can find the next step (`docs/runbooks/getting-started.md`) with a single path reference.
- Adding new runbooks (e.g., `project-lifecycle.md`) or playbooks (e.g., `adversary.md`) requires no structural change — only adding a file to the appropriate subdirectory.
- Separation of types enables future index files (`docs/runbooks/README.md`, `docs/playbooks/README.md`) if the number of files grows.
- Clean cross-reference paths: runbook references playbooks via `../playbooks/{skill}.md`.

**Weaknesses:**
- Requires two subdirectory creations before content can be placed.
- A user looking for "how to use orchestration" must navigate to `docs/playbooks/orchestration.md` rather than `docs/orchestration.md` — one additional path segment.
- If the runbook/playbook vocabulary distinction is later revised, the directory names would need renaming (low probability but nonzero).

**Score against criteria:**

| Criterion | Score | Justification |
|-----------|-------|---------------|
| C1 User discoverability | 4 | `docs/runbooks/getting-started.md` is the natural next step after INSTALLATION.md. Playbook directory is clearly named. New users following the runbook are pointed directly to `../playbooks/{skill}.md` per REQ-943-008. |
| C2 Maintenance burden | 5 | Clean separation means changes to a runbook never affect playbook paths, and vice versa. Adding new docs in either category is a single-file operation. |
| C3 Nav standard compliance | 4 | Structure is neutral with respect to H-23/H-24 — per-file navigation tables are unaffected by subdirectory placement. |
| C4 EN-942 vocabulary alignment | 5 | Subdirectory names ARE the vocabulary. The physical structure enforces the conceptual distinction without any additional explanation. |
| C5 Cross-reference coherence | 4 | Relative paths are unambiguous (`../playbooks/problem-solving.md` from runbook; `../runbooks/getting-started.md` from playbook). One extra `../` traversal compared to flat, but path is self-documenting. |

**Weighted score:** (4×0.30) + (5×0.25) + (4×0.20) + (5×0.15) + (4×0.10) = 1.20 + 1.25 + 0.80 + 0.75 + 0.40 = **4.40**

---

#### Alternative C: Skill-Grouped Guides Hierarchy

All documentation is organized by skill under a `docs/guides/` parent. Each skill gets a subdirectory containing both its runbook entry point and its playbook reference.

```
docs/
├── INSTALLATION.md
└── guides/
    ├── getting-started/
    │   └── index.md             (EN-943 output — the getting-started runbook)
    ├── problem-solving/
    │   ├── getting-started.md   (optional per-skill runbook)
    │   └── playbook.md          (EN-944 output)
    ├── orchestration/
    │   ├── getting-started.md   (optional per-skill runbook)
    │   └── playbook.md          (EN-944 output)
    └── transcript/
        ├── getting-started.md   (optional per-skill runbook)
        └── playbook.md          (EN-944 output)
```

**Strengths:**
- Groups all documentation about a single skill in one location — useful for developers working on one skill at a time.
- Scales well if every skill eventually needs both a runbook and a playbook.
- `docs/guides/` is a recognizable documentation convention (used by many open-source projects).

**Weaknesses:**
- The getting-started runbook (EN-943) covers a system-level user journey, not a single skill. Placing it under `guides/getting-started/` conflates two different concepts: a system runbook (which spans all skills) and per-skill guides.
- Introduces three additional subdirectory levels (`guides/problem-solving/playbook.md`) for content that could live at `docs/playbooks/problem-solving.md`. Increases path depth without commensurate benefit.
- For FEAT-018 scope (exactly 1 runbook + 3 playbooks), the per-skill directory model is over-engineered: each subdirectory contains only one file.
- Cross-reference paths between skill guides require multi-level traversal (`../../transcript/playbook.md`) which is error-prone and reduces readability.
- The runbook/playbook distinction is buried inside each skill subdirectory rather than expressed at the top level.

**Score against criteria:**

| Criterion | Score | Justification |
|-----------|-------|---------------|
| C1 User discoverability | 3 | Skill-centric organization works for developers who already know which skill they want. But new users following a linear journey (install → get started → learn skills) must navigate an additional level of hierarchy. The getting-started runbook does not naturally live under a skill directory. |
| C2 Maintenance burden | 3 | Per-skill directories are easy to update in isolation, but the directory structure itself is more complex to reason about. Adding a new runbook that spans multiple skills has no natural home. |
| C3 Nav standard compliance | 4 | Neutral — H-23/H-24 are per-file requirements unaffected by directory depth. |
| C4 EN-942 vocabulary alignment | 2 | The runbook/playbook distinction is flattened by skill grouping. The type of document (procedure vs. reference) is not visible at the directory level — users must look inside each skill directory to understand what each file is. |
| C5 Cross-reference coherence | 2 | Cross-references between skill guides require multi-level relative paths. The system-level runbook referencing three different skill subdirectories introduces fragile path dependencies. |

**Weighted score:** (3×0.30) + (3×0.25) + (4×0.20) + (2×0.15) + (2×0.10) = 0.90 + 0.75 + 0.80 + 0.30 + 0.20 = **2.95**

---

#### Alternative D: Single Guide Per Skill (Combined Runbook + Playbook)

One file per skill combines both the procedural runbook content and the reference playbook content into a single document.

```
docs/
├── INSTALLATION.md
└── guides/
    ├── getting-started.md       (EN-943 output — system runbook)
    ├── problem-solving.md       (EN-944 output — combined procedure + reference)
    ├── orchestration.md         (EN-944 output — combined procedure + reference)
    └── transcript.md            (EN-944 output — combined procedure + reference)
```

**Strengths:**
- Simplest user experience: one file per topic, no navigation between multiple documents required to understand a skill.
- Reduces total document count — fewer files to maintain, fewer cross-reference paths to manage.
- Aligns with how many open-source projects organize their documentation (single README-style guide per component).

**Weaknesses:**
- Directly contradicts EN-942's core vocabulary distinction: REQ-942-001 requires runbooks and playbooks to be defined as distinct document types with distinct structural templates. Merging them into a single file invalidates both template definitions.
- Combined files grow large and become harder to maintain as skills evolve. A change to the orchestration skill's procedures and reference material must be coordinated in a single large file.
- Users needing a quick reference lookup (the playbook use case) must scroll through procedural content to reach reference tables. Users following a step-by-step procedure are interrupted by conditional reference content.
- Cross-reference opportunities are lost: a user reading the problem-solving guide has no natural pointer to "see also: orchestration guide" because both are the same document type with no inter-guide navigation model.
- AC-1 of FEAT-018 explicitly requires a scope document defining the distinction; merged guides would make that scope document describe a distinction that the actual output files do not reflect.

**Score against criteria:**

| Criterion | Score | Justification |
|-----------|-------|---------------|
| C1 User discoverability | 3 | Fewer files means less navigation overhead, but the single-file model serves neither new users (runbook path) nor experienced users (quick reference lookup) optimally. |
| C2 Maintenance burden | 2 | Single large files accumulate technical debt faster. When a skill changes, the entire combined guide must be reviewed rather than only the affected section type (runbook or playbook). |
| C3 Nav standard compliance | 3 | H-23/H-24 still apply and can be satisfied by a long internal navigation table, but a single file containing both procedural and reference content requires a more complex internal structure to remain navigable. |
| C4 EN-942 vocabulary alignment | 1 | Combining runbook and playbook content in one file directly contradicts the vocabulary distinction that EN-942 is specifically designed to establish. |
| C5 Cross-reference coherence | 3 | References between combined guides are simpler (fewer target paths) but the guides cannot provide type-specific cross-references (e.g., "runbook for X" or "playbook for Y"). |

**Weighted score:** (3×0.30) + (2×0.25) + (3×0.20) + (1×0.15) + (3×0.10) = 0.90 + 0.50 + 0.60 + 0.15 + 0.30 = **2.45**

---

### Weighted Scoring Summary

| Alternative | C1 (0.30) | C2 (0.25) | C3 (0.20) | C4 (0.15) | C5 (0.10) | **Total** | Outcome |
|-------------|-----------|-----------|-----------|-----------|-----------|-----------|---------|
| A: Flat `docs/` | 3 | 4 | 4 | 1 | 3 | **3.15** | Not recommended |
| B: Two-tier split | 4 | 5 | 4 | 5 | 4 | **4.40** | **Recommended** |
| C: Skill-grouped guides | 3 | 3 | 4 | 2 | 2 | **2.95** | Not recommended |
| D: Single guide per skill | 3 | 2 | 3 | 1 | 3 | **2.45** | Not recommended |

Alternative B (two-tier split) scores highest with 4.40 / 5.00 and dominates on the two highest-weighted criteria (C1 discoverability and C2 maintenance burden) while achieving the maximum score on EN-942 vocabulary alignment (C4). No other alternative comes within 1.0 points.

---

## L2: Recommendation

### Recommended Structure

**Alternative B: Two-Tier Split** is the recommended documentation structure for FEAT-018.

**Exact file paths for all FEAT-018 output:**

```
docs/
├── INSTALLATION.md                    (existing — not modified by FEAT-018)
├── runbooks/
│   └── getting-started.md             (EN-943 output)
└── playbooks/
    ├── problem-solving.md             (EN-944 output — problem-solving skill)
    ├── orchestration.md               (EN-944 output — orchestration skill)
    └── transcript.md                  (EN-944 output — transcript skill)
```

**Cross-reference paths (relative, from each document's perspective):**

| Document | References | Relative Path |
|----------|-----------|---------------|
| `docs/runbooks/getting-started.md` | INSTALLATION.md | `../INSTALLATION.md` |
| `docs/runbooks/getting-started.md` | Problem-solving playbook | `../playbooks/problem-solving.md` |
| `docs/runbooks/getting-started.md` | Orchestration playbook | `../playbooks/orchestration.md` |
| `docs/runbooks/getting-started.md` | Transcript playbook | `../playbooks/transcript.md` |
| `docs/playbooks/problem-solving.md` | SKILL.md source | `../../skills/problem-solving/SKILL.md` |
| `docs/playbooks/orchestration.md` | SKILL.md source | `../../skills/orchestration/SKILL.md` |
| `docs/playbooks/transcript.md` | SKILL.md source | `../../skills/transcript/SKILL.md` |

### Rationale

1. **Vocabulary alignment (C4 = 5):** The directory names `runbooks/` and `playbooks/` are the vocabulary of EN-942 made physical. Any content agent writing under `docs/runbooks/` knows they are producing a linear procedure. Any content agent writing under `docs/playbooks/` knows they are producing a reference document. The structural signal eliminates ambiguity that the flat structure (Alternative A) or combined structure (Alternative D) would introduce.

2. **Discoverability (C1 = 4):** A new user completing INSTALLATION.md is directed to `docs/runbooks/getting-started.md` as the next step. This is a single, memorable path. Once inside the runbook, REQ-943-008 requires a Next Steps section pointing to `../playbooks/`. The two-step discovery path (runbook first, then playbooks) mirrors the intended user journey.

3. **Maintenance (C2 = 5):** Skills evolve independently. When the transcript skill's domain contexts change, only `docs/playbooks/transcript.md` needs updating. The runbook is unaffected. The clean boundary between `runbooks/` and `playbooks/` prevents coupling that would occur in merged (Alternative D) or skill-grouped (Alternative C) structures.

4. **Future extensibility:** Adding `docs/runbooks/project-lifecycle.md` or `docs/playbooks/adversary.md` in a future feature requires no structural change — only adding a file to the existing subdirectory. Alternative C would require a new skill subdirectory for each addition.

### Migration Path

1. Create `docs/runbooks/` directory (empty, no files yet).
2. Create `docs/playbooks/` directory (empty, no files yet).
3. Note: `docs/playbooks/PLUGIN-DEVELOPMENT.md` already exists. This file is a developer-facing internal playbook, not a user-facing skill playbook. It SHOULD be reviewed for placement but is outside FEAT-018 scope. The `docs/playbooks/` directory already exists at the filesystem level — only `docs/runbooks/` requires creation.
4. Phase 4 content agents (EN-943 writer, EN-944 writers) write directly to the paths specified above.
5. INSTALLATION.md SHOULD be updated (separate work item) to add a "Next Steps" reference to `docs/runbooks/getting-started.md` once EN-943 is complete.

**Pre-existing `docs/playbooks/` directory note:** The directory already contains `PLUGIN-DEVELOPMENT.md`. This is not a conflict — FEAT-018 playbooks will coexist alongside it. The EN-942 scope document should note this pre-existing file and confirm it does not need modification.

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Content agents write to wrong directory (e.g., placing a playbook under `runbooks/`) | Low | Medium | The EN-942 scope document must include exact file paths (REQ-942-002). Phase 4 agent invocations should include the target path explicitly. |
| `docs/runbooks/` path is unfamiliar to users expecting `docs/guides/` | Low | Low | `runbooks/` is a widely recognized documentation pattern (SRE, DevOps). The term is self-documenting. |
| INSTALLATION.md is not updated to reference the runbook, breaking the discovery chain | Medium | Medium | REQ-943-002 requires the runbook to reference INSTALLATION.md; the reverse reference (INSTALLATION.md to runbook) is a separate work item but SHOULD be added during or immediately after Phase 4. |
| New skills added in future features create playbooks without a corresponding EN-942 scope update | Medium | Low | FEAT-018 scope boundaries explicitly exclude future skills; future features that add playbooks should create their own scope documents referencing this structure. |

---

## Section Template Definitions

This section defines the standard section templates per EN-942 requirements (REQ-942-004 for playbooks, REQ-942-005 for runbooks). These templates MUST be used by Phase 4 content agents.

### Runbook Template (REQ-942-005)

Runbooks are linear, sequential procedures with a defined start state and end state. All sections listed below are REQUIRED.

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

```bash
{command if applicable}
```

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

**Section guidance:**

| Section | Required Content | Minimum Length |
|---------|-----------------|----------------|
| Prerequisites | Start-state checklist; reference to upstream docs | 3 items |
| Procedure | Numbered steps; command examples; expected output | 4 steps |
| Verification | Observable end-state checklist | 3 items |
| Troubleshooting | Failure mode table | 3 entries |
| Next Steps | Links to playbooks (REQ-943-008) | 1 link |

---

### Playbook Template (REQ-942-004)

Playbooks are reference-oriented documents consulted non-linearly. They contain conditional decision points and multiple usage paths. All sections listed below are REQUIRED.

```markdown
# {Skill Name} Playbook

> **Skill:** {skill-name}
> **SKILL.md:** [{relative path}]({relative-path-to-skill-md})
> **Trigger keywords:** {keywords from mandatory-skill-usage.md}

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

**Section guidance:**

| Section | Required Content | Minimum |
|---------|-----------------|---------|
| When to Use | Positive + at least one negative criterion | 3 positive, 1 negative |
| Prerequisites | Conditions for correct invocation | 2 items |
| Step-by-Step | Numbered steps for primary path | 4 steps |
| Examples | Both user phrase and system behavior | 2 examples |
| Troubleshooting | Failure mode table | 3 entries |
| Related Resources | SKILL.md link + at least one other playbook | 2 links |

---

### Coverage Map (REQ-942-006)

This map verifies that each planned playbook addresses the trigger keywords from `.context/rules/mandatory-skill-usage.md` for its skill.

| Skill | Trigger Keywords (from mandatory-skill-usage.md) | Playbook File | Coverage Status |
|-------|--------------------------------------------------|---------------|-----------------|
| problem-solving | research, analyze, investigate, explore, root cause, why | `docs/playbooks/problem-solving.md` | Covered — playbook must include these in "When to Use" |
| orchestration | orchestration, pipeline, workflow, multi-agent, phases, gates | `docs/playbooks/orchestration.md` | Covered — playbook must include these in "When to Use" |
| transcript | *(No mandatory-skill-usage.md entry — invoked by file path argument)* | `docs/playbooks/transcript.md` | Partial — playbook should document invocation syntax; no keyword triggers exist in the trigger map |

**Note on transcript trigger keywords:** The transcript skill is invoked via explicit CLI argument (`/transcript <file-path>`) rather than through keyword detection in mandatory-skill-usage.md. The transcript playbook SHOULD document the CLI syntax as the activation mechanism rather than keyword phrases. This is not a gap in coverage — it reflects the skill's architecture.

---

## Scope Boundaries

This section defines in-scope and out-of-scope skills per REQ-942-003 and FEAT-018 AC-3.

### In Scope (FEAT-018)

| Skill | Enabler | Output File | Rationale |
|-------|---------|-------------|-----------|
| problem-solving | EN-944 | `docs/playbooks/problem-solving.md` | Named in FEAT-018 AC-3. Highest-frequency skill. Entry point for new users (recommended first invocation per EN-943). |
| orchestration | EN-944 | `docs/playbooks/orchestration.md` | Named in FEAT-018 AC-3. Required for multi-phase workflows that users encounter within days of onboarding. |
| transcript | EN-944 | `docs/playbooks/transcript.md` | Named in FEAT-018 AC-3. Has mandatory CLI invocation constraint (Phase 1/Phase 2 distinction) that requires explicit documentation to prevent user errors. |

### Out of Scope (FEAT-018)

| Skill | Rationale for Exclusion |
|-------|------------------------|
| adversary | Not named in AC-3. `/adversary` skill is used in quality-enforcement workflows typically executed by experienced users; documenting it before new users understand the problem-solving foundation would create confusion. Candidate for a future feature (FEAT-019 or equivalent). |
| worktracker | Not named in AC-3. The `/worktracker` skill manages task state; its usage is ancillary to the core user journey covered by FEAT-018. Its operational documentation is embedded in project-workflow.md rules. |
| nasa-se | Not named in AC-3. `/nasa-se` is used by agent orchestration workflows, not directly by end users in their daily operation. It has no end-user activation keywords in the trigger map. |
| architecture | Not named in AC-3. `/architecture` is an advanced skill for design decision workflows; new users are not expected to invoke it during onboarding. |
| bootstrap | Not named in AC-3. Bootstrap is a one-time setup skill, not a recurring workflow. Its documentation belongs in an installation or setup context (FEAT-017 scope), not a runbooks/playbooks layer. |

**Exclusion is binding for FEAT-018 scope only.** Future features that add playbooks for excluded skills SHOULD use the two-tier directory structure ratified in this trade study, adding files to `docs/playbooks/` without structural change.

---

*Agent: nse-explorer-001*
*Workflow: epic001-docs-20260218-001*
*Phase: 3*
*Output: `projects/PROJ-001-oss-release/orchestration/epic001-docs-20260218-001/docs/phase-3/nse-explorer-001/nse-explorer-001-structure-trade-study.md`*
