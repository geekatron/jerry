# Prompt: GitHub Issue #148 — README & Doc Module

> Multi-skill orchestration prompt for PROJ-0037-doc-module.
> Copy the content inside the fenced code block below into a fresh Jerry session.

## Prompt

```
Use /worktracker to create a Feature titled "README & Doc Module — GitHub #148" under PROJ-0037-doc-module.
Create two child Stories under this Feature:
  - Story 1: "Update README.md to reflect current skills, agents, and repository state"
  - Story 2: "Design and implement auto-documentation module for skills and agents"

Use /problem-solving to invoke the following agents in order, coordinated
by /orchestration with orch-planner across two parallel workstreams.

---

## Workstream A — Documentation Update (Content Authoring)

### Phase A1 — Inventory (ps-researcher)

Use /problem-solving with ps-researcher to build a current-state inventory of
Jerry's skills, agents, and documentation surface.

Data sources (codebase — Read, Grep, Glob):
  - `skills/*/SKILL.md` (13 files: adversary, architecture, ast, bootstrap, eng-team,
    nasa-se, orchestration, problem-solving, red-team, saucer-boy,
    saucer-boy-framework-voice, transcript, worktracker)
  - `skills/*/agents/*.md` (58 invokable agents across 10 skill directories)
  - `AGENTS.md` (canonical agent registry with verified counts)
  - `README.md` (current state: 6 skills listed, "8 specialized agents" claim)
  - `CLAUDE.md` (skill table — lists 12 skills in Quick Reference)
  - `.context/rules/mandatory-skill-usage.md` (trigger map — lists 8 skill routes)
  - `docs/INSTALLATION.md`
  - `CONTRIBUTING.md`

Focus areas:
  - Skills present in repo but absent from README (at minimum: adversary, ast,
    bootstrap, eng-team, red-team, saucer-boy, saucer-boy-framework-voice)
  - Correct agent count per skill (58 total, not 8)
  - Documentation files that exist but are not linked from the Documentation table
  - Known limitations that are stale or resolved
  - Example session accuracy vs. current agent behavior
  - Discrepancies between CLAUDE.md skill table, AGENTS.md, and README

Output: projects/PROJ-0037-doc-module/research/current-state-inventory.md
  with L0 (summary of gaps) / L1 (per-skill delta table) / L2 (full inventory).

Include ps-critic adversarial critique after the research phase.
Quality threshold: >= 0.90.

### Phase A2 — README Rewrite (ps-architect)

Use /problem-solving with ps-architect to author the updated README.md content.

Input artifact: projects/PROJ-0037-doc-module/research/current-state-inventory.md

Updates required:
  1. **Skills table** (line 107-114): Expand from 6 to all 13 skills. Include all
     skills with SKILL.md files. Use the same table format (Skill | Purpose | Example).
  2. **Features section** (line 133-139): Replace "8 specialized agents" with accurate
     count (58 agents across 13 skills). Add feature bullets for: adversarial quality
     review, secure engineering, offensive security testing, AST-based markdown parsing,
     framework voice quality, session personality.
  3. **Documentation table** (line 143-148): Add links to any new documentation files
     discovered in Phase A1 (e.g., docs/guides/, docs/knowledge/).
  4. **Known Limitations** (line 98-101): Review each limitation against current state.
     Remove resolved items. Add any new limitations discovered in Phase A1.
  5. **Example session** (line 116-131): Verify the example reflects current agent
     naming and output path conventions. Update if stale.
  6. **Agent count consistency**: Ensure the README's agent count matches AGENTS.md
     (58 agents, last verified 2026-02-22). Do NOT duplicate agent detail — reference
     AGENTS.md as the canonical registry.

Constraints:
  - Preserve existing README structure and tone (user-facing, concise).
  - Do NOT add navigation tables or Jerry-internal conventions to README — this is
    a public-facing document.
  - Keep the README under 250 lines.
  - All skill names MUST use `/slash-command` format consistent with CLAUDE.md.

Output: projects/PROJ-0037-doc-module/drafts/README-draft.md
  (full replacement content, ready to overwrite README.md after review).

Include ps-critic adversarial critique after the authoring phase.
Quality threshold: >= 0.92.

---

## Workstream B — Doc Module (Engineering)

### Phase B1 — Research (ps-researcher)

Use /problem-solving with ps-researcher to research auto-documentation patterns
for agent/skill framework documentation.

Data sources:
  - Use Context7 to query Elixir Phoenix `mix docs` patterns and `@moduledoc` conventions.
  - Use Context7 to query Python documentation generation patterns (Sphinx autodoc,
    mkdocs-gen-files, pydoc-markdown).
  - Use WebSearch for "auto-generate README from plugin metadata" and
    "self-documenting agent framework" patterns.
  - Codebase: `skills/*/SKILL.md` YAML frontmatter structure (name, description,
    version, activation-keywords fields).
  - Codebase: `skills/*/agents/*.md` YAML frontmatter structure (name, description,
    model, tools fields).
  - Codebase: `AGENTS.md` structure and verification note format.

Focus areas:
  - Elixir Phoenix `@moduledoc` / `mix docs` pattern: how module docstrings become
    browsable documentation. Applicability to SKILL.md/agent .md frontmatter.
  - Python equivalents: Sphinx autodoc, mkdocs, pydoc-markdown — extracting docstrings
    from source into structured docs.
  - Template-based README generation: mustache/jinja patterns for injecting extracted
    metadata into README sections.
  - Pre-commit hook vs. CI step vs. CLI command trade-offs for doc generation.
  - Jerry-specific considerations: YAML frontmatter as structured metadata source,
    13 SKILL.md files as input, 58 agent definition files as input, governance
    constraints (H-05: uv-only, H-33: AST-based parsing).

Output: projects/PROJ-0037-doc-module/research/doc-module-patterns.md
  with L0/L1/L2 sections.

Include ps-critic adversarial critique after the research phase.
Quality threshold: >= 0.90.

### Phase B2 — Architecture Decision (ps-architect)

Use /problem-solving with ps-architect to evaluate design options for the
auto-documentation module.

Input artifacts:
  - projects/PROJ-0037-doc-module/research/doc-module-patterns.md

Options:
  A. Python CLI command (`jerry docs generate`) — extends existing Jerry CLI.
     Parses SKILL.md and agent .md frontmatter via jerry ast module. Renders
     README sections via Jinja2 templates. Runs as pre-commit hook or manual CLI.
  B. Shell script (`scripts/generate-docs.sh`) — lightweight. Uses grep/awk/sed
     to extract YAML frontmatter. Generates markdown via heredoc templates.
     Runs as pre-commit hook.
  C. CI-only generation — GitHub Action parses SKILL.md files on push to main.
     Generates README sections and opens PR if drift detected. No local tooling.

Evaluation dimensions:
  - Maintainability: How easy is it to update when skills/agents are added?
  - Accuracy: Can it reliably extract name, description, agent count from frontmatter?
  - Jerry compliance: Does it satisfy H-05 (uv-only), H-33 (AST-based parsing)?
  - Developer experience: How does a contributor verify docs are current before committing?
  - Failure mode: What happens when SKILL.md frontmatter is malformed?

Context: Jerry uses `uv run` for all Python (H-05). The jerry ast module already
parses markdown frontmatter (H-33). The existing pre-commit hook infrastructure
uses Python scripts in `scripts/`. README.md is a public-facing file that must
stay accurate.

Output: projects/PROJ-0037-doc-module/decisions/ADR-PROJ0037-001-doc-module-design.md
  in Nygard ADR format.

Include ps-critic adversarial critique after the architecture phase.
Quality threshold: >= 0.92.

### Phase B3 — Secure Design Review (eng-architect)

Use /eng-team with eng-architect to produce a threat model for the selected
doc module design from Phase B2.

Input artifact: projects/PROJ-0037-doc-module/decisions/ADR-PROJ0037-001-doc-module-design.md

Threat modeling focus:
  - STRIDE analysis on the doc generation pipeline (especially if pre-commit hook:
    can malformed SKILL.md inject content into README?)
  - Supply chain: if Jinja2 or other templating dependency is used, SLSA assessment.
  - File system trust boundary: does the generator trust all files in skills/ without
    validation?
  - Failure modes: what happens if the generator crashes mid-write? Partial README?

Output: projects/PROJ-0037-doc-module/security/threat-model-doc-module.md

Include ps-critic adversarial critique after the security review.
Quality threshold: >= 0.92.

### Phase B4 — Implementation Specification (ps-analyst)

Use /problem-solving with ps-analyst to produce a detailed implementation
specification for the doc module based on the ADR decision and threat model.

Input artifacts:
  - projects/PROJ-0037-doc-module/decisions/ADR-PROJ0037-001-doc-module-design.md
  - projects/PROJ-0037-doc-module/security/threat-model-doc-module.md

Specification must cover:
  - Input parsing: which YAML frontmatter fields to extract from SKILL.md and
    agent .md files (name, description, version, activation-keywords, model, tools).
  - Output rendering: template structure for README skills table and features section.
  - Drift detection: how to compare generated output against current README content.
  - Error handling: malformed frontmatter, missing required fields, empty directories.
  - Integration points: pre-commit hook registration, CI workflow, manual CLI invocation.
  - Test plan: unit tests for parser, integration tests for end-to-end generation,
    golden-file tests comparing generated vs. expected README sections.

Output: projects/PROJ-0037-doc-module/specifications/doc-module-spec.md

Include ps-critic adversarial critique after the specification phase.
Quality threshold: >= 0.92.

---

## Orchestration

Use /orchestration with orch-planner to sequence the above pipeline.

Workstream dependencies:
  - Workstreams A and B are independent and MAY execute in parallel.
  - Within Workstream A: Phase A1 must complete before Phase A2.
  - Within Workstream B: Phase B1 -> B2 -> B3 -> B4 (sequential).
  - Sync barrier after all phases: orch-synthesizer produces a final
    cross-workstream synthesis identifying overlaps (e.g., does the Phase B4
    spec match the Phase A2 README structure?).

Quality gates at every phase boundary per H-14 (creator-critic-revision, minimum 3
iterations). All C2+ phases require >= 0.92 weighted composite score before proceeding.

Output orchestration plan:
  projects/PROJ-0037-doc-module/orchestration/doc-module-20260308-001/ORCHESTRATION_PLAN.md

Output synthesis:
  projects/PROJ-0037-doc-module/orchestration/doc-module-20260308-001/synthesis/cross-workstream-synthesis.md
```

## Expected Artifacts

| Phase | Output Path | Type |
|-------|-------------|------|
| A1 | `research/current-state-inventory.md` | Inventory |
| A2 | `drafts/README-draft.md` | README replacement |
| B1 | `research/doc-module-patterns.md` | Research |
| B2 | `decisions/ADR-PROJ0037-001-doc-module-design.md` | ADR |
| B3 | `security/threat-model-doc-module.md` | Threat model |
| B4 | `specifications/doc-module-spec.md` | Implementation spec |
| Synthesis | `orchestration/.../cross-workstream-synthesis.md` | Synthesis |

All paths relative to `projects/PROJ-0037-doc-module/`.
