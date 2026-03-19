# Cross-Workstream Synthesis: Documentation Update + Doc Module Engineering

> **Workflow:** doc-module-20260308-001
> **Agent:** orch-synthesizer
> **Project:** PROJ-0037-doc-module
> **Date:** 2026-03-08
> **Inputs:** Phase A2 (README-draft.md), Phase B4 (doc-module-spec.md)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Key findings and action items |
| [L1: Structural Compatibility Analysis](#l1-structural-compatibility-analysis) | Section-by-section comparison |
| [L2: Detailed Overlap Analysis](#l2-detailed-overlap-analysis) | Field-level discrepancies and reconciliation |

---

## L0: Executive Summary

1. **The README draft (A2) and auto-doc spec (B4) are structurally compatible.** The spec generates exactly the two sections that A2 manually authored: the skills table and the features bullet list. All other README sections remain manually authored in both approaches.

2. **The README draft is missing marker comments.** B4's marker-based injection (`<!-- BEGIN:GENERATED:SKILLS_TABLE -->` / `<!-- END:GENERATED:SKILLS_TABLE -->`) requires markers in the committed README. The A2 draft does not include these markers. **Action required before commit.**

3. **The skills table column structure matches exactly.** Both A2 and B4 use `| Skill | Purpose | Example |` columns. The auto-doc module will produce output structurally identical to the A2 draft.

4. **Description truncation creates a content gap.** A2's Purpose column contains manually crafted, readable descriptions. B4 truncates SKILL.md `description` fields at 60 characters. Some SKILL.md descriptions exceed 60 characters and will produce truncated, less readable output. **Seed SKILL.md descriptions or adjust truncation length.**

5. **Two static data files must be seeded from A2 content.** The B4 spec requires `skill-examples.yaml` and `features.yaml` as static inputs. A2 provides the initial content for both. These files should be created using A2's content as the source of truth.

---

## L1: Structural Compatibility Analysis

### Section Scope Comparison

| README Section | A2 (Manual) | B4 (Auto-Generated) | Compatibility |
|----------------|-------------|----------------------|---------------|
| Title + badges | Manual | Not generated | Compatible |
| What is Jerry? | Manual | Not generated | Compatible |
| Quick Start | Manual | Not generated | Compatible |
| Platform Support | Manual | Not generated | Compatible |
| Known Limitations | Manual | Not generated | Compatible |
| **Using Jerry (skills table)** | **Manual** | **Auto-generated** | **Overlap** |
| Example Session | Manual | Not generated | Compatible |
| **Features** | **Manual** | **Auto-generated** | **Overlap** |
| Documentation | Manual | Not generated | Compatible |
| For Contributors | Manual | Not generated | Compatible |
| References | Manual | Not generated | Compatible |
| License | Manual | Not generated | Compatible |

**Finding:** Overlap is confined to exactly two sections. The scope boundary in B4 ("skills table and features bullet list") precisely matches the sections A2 most urgently needed updating. No scope conflicts exist.

### Column Structure Comparison (Skills Table)

| Column | A2 Format | B4 Template | Match? |
|--------|-----------|-------------|--------|
| Skill | `` `/skill-name` `` | `` `/{{ skill.name }}` `` | Yes |
| Purpose | Free-text description | `{{ skill.description \| truncate(60) }}` | Partial (see L2) |
| Example | Quoted example text | `{{ skill.example }}` from `skill-examples.yaml` | Yes (source differs) |

### Features Section Comparison

| Element | A2 Format | B4 Template | Match? |
|---------|-----------|-------------|--------|
| Agent count headline | "58 Specialized Agents across 13 skills" | `{{ total_agents }} Specialized Agents across {{ total_skills }} skills` | Yes (dynamic vs. hardcoded) |
| Feature bullets | 9 manually authored bullets | `{% for feature in features %}` from `features.yaml` | Yes (source differs) |
| AGENTS.md link | Present | Present in template | Yes |

---

## L2: Detailed Overlap Analysis

### Discrepancy 1: Missing Marker Comments (Critical)

**A2 output** (README-draft.md lines 106-122):
```markdown
## Using Jerry

Jerry provides **skills**—natural language interfaces you invoke with slash commands:

| Skill | Purpose | Example |
|-------|---------|---------|
| `/problem-solving` | Research, analysis, root cause investigation | "Research OAuth2 patterns" |
...
```

**B4 requirement** (doc-module-spec.md lines 157-167):
```markdown
<!-- BEGIN:GENERATED:SKILLS_TABLE -->
| Skill | Purpose | Example |
...
<!-- END:GENERATED:SKILLS_TABLE -->

<!-- BEGIN:GENERATED:FEATURES -->
- **58 Specialized Agents** across 13 skills...
...
<!-- END:GENERATED:FEATURES -->
```

**Impact:** Without markers, the auto-doc module cannot locate the sections to replace. The `--check` mode will fail with exit code 2 ("Marker not found").

**Reconciliation:** Add marker comments to the A2 README draft around the skills table and features sections before committing. The introductory text ("Jerry provides **skills**...") should remain outside the markers as manually-authored content.

### Discrepancy 2: Description Truncation at 60 Characters

A2 crafted human-readable Purpose descriptions. B4 truncates SKILL.md `description` fields at 60 characters. Comparison of the first 5 skills:

| Skill | A2 Purpose | SKILL.md `description` (truncated to 60) | Differs? |
|-------|-----------|------------------------------------------|----------|
| `/problem-solving` | Research, analysis, root cause investigation | Structured problem-solving framework with s... | Yes |
| `/worktracker` | Task and work item management | Work item tracking and task management usin... | Yes |
| `/nasa-se` | Systems engineering (NPR 7123.1D) | NASA Systems Engineering skill implementing... | Yes |
| `/orchestration` | Multi-phase workflow coordination | Multi-agent workflow orchestration with stat... | Yes |
| `/adversary` | Adversarial quality reviews and scoring | On-demand adversarial quality reviews using ... | Yes |

**Impact:** All 13 skills will have different Purpose text after auto-generation. SKILL.md descriptions are technical and implementation-focused; A2 descriptions are user-facing and concise.

**Reconciliation options (choose one):**

| Option | Approach | Pros | Cons |
|--------|----------|------|------|
| **R-1** | Add a `readme-description` field to SKILL.md frontmatter | Clean separation of internal vs. public description | Requires updating all 13 SKILL.md files; adds a field |
| **R-2** | Use a static mapping file (`skill-descriptions.yaml`) | No SKILL.md changes; full control over README text | Another static file to maintain alongside `skill-examples.yaml` |
| **R-3** | Increase truncation to 100 chars and accept longer descriptions | Simplest change | Descriptions still differ from A2's crafted text; table may be wide |

**Recommendation:** **R-2** (static mapping file). This is consistent with the existing `skill-examples.yaml` pattern in B4. Create `skill-descriptions.yaml` with A2's Purpose text as initial content. The auto-doc module reads from this file instead of truncating SKILL.md descriptions.

### Discrepancy 3: Static Data Files Need Seeding

B4 defines two static data files that do not yet exist:

| File | Purpose | Seed Source |
|------|---------|-------------|
| `.context/templates/docs/skill-examples.yaml` | One-line examples per skill | A2 README-draft.md Example column |
| `.context/templates/docs/features.yaml` | Curated features list | A2 README-draft.md Features section |

**Seed content from A2:**

**skill-examples.yaml** (derived from A2 skills table):
```yaml
problem-solving: '"Research OAuth2 patterns"'
worktracker: '"Create a task for login feature"'
nasa-se: '"Define requirements for API"'
orchestration: '"Orchestrate the release pipeline"'
architecture: '"Create ADR for caching strategy"'
transcript: '"Parse the meeting notes"'
adversary: '"Run adversarial review on this ADR"'
eng-team: '"Threat model the auth service"'
red-team: '"Recon the target application"'
ast: '"Validate entity frontmatter"'
saucer-boy: '"Give me a pep talk"'
bootstrap: '"Bootstrap Jerry"'
saucer-boy-framework-voice: '"Auto-loaded for output text"'
```

**features.yaml** (derived from A2 features section):
```yaml
- title: "Structured Problem-Solving"
  description: "9 agents (researcher, analyst, architect, validator, synthesizer, reviewer, critic, investigator, reporter) with adversarial quality gates"
- title: "Work Tracking"
  description: "Local task management with status, priorities, dependencies, and template-enforced consistency"
- title: "Knowledge Accrual"
  description: "Persistent artifacts in `projects/` that survive session boundaries"
- title: "NASA Systems Engineering"
  description: "10 agents implementing NPR 7123.1D processes for mission-grade rigor"
- title: "Multi-Agent Orchestration"
  description: "Coordinate complex workflows with parallel pipelines, sync barriers, and checkpointing"
- title: "Adversarial Quality Reviews"
  description: "10 adversarial strategies (Red Team, Devil's Advocate, Pre-Mortem, FMEA, and more) with LLM-as-Judge scoring"
- title: "Secure Engineering"
  description: "10 agents covering threat modeling (STRIDE), secure code review (OWASP ASVS), DevSecOps pipelines, and incident response"
- title: "Offensive Security"
  description: "11 agents covering the full MITRE ATT&CK kill chain — reconnaissance through reporting — with mandatory scope authorization"
- title: "AST-Based Parsing"
  description: "Structured markdown frontmatter extraction for worktracker entities and validation"
```

### Discrepancy 4: Dynamic vs. Hardcoded Agent Count

| Source | Value | Mechanism |
|--------|-------|-----------|
| A2 (README-draft.md) | "58 Specialized Agents" | Hardcoded text |
| B4 (spec) | `{{ total_agents }}` | Dynamically counted from agent files |

**Impact:** Once the auto-doc module is implemented, the agent count will be dynamically computed. If agents are added or removed, the README updates automatically. No reconciliation needed — the dynamic approach supersedes the hardcoded value. The initial run should produce "58" matching A2.

### Discrepancy 5: Exclusion Rule Alignment

B4 specifies exclusion patterns for agent counting:
- `*TEMPLATE*` (e.g., `PS_AGENT_TEMPLATE.md`)
- `*EXTENSION*` (e.g., `PS_EXTENSION.md`)

A2's agent count of 58 was derived from the current AGENTS.md which already applies these exclusions. The exclusion rules are aligned.

---

## Reconciliation Action Items

| # | Action | Priority | Owner | Phase |
|---|--------|----------|-------|-------|
| 1 | Add `<!-- BEGIN:GENERATED:SKILLS_TABLE -->` and `<!-- END:GENERATED:SKILLS_TABLE -->` markers to README-draft.md around the skills table | **Critical** | Implementation | Before README commit |
| 2 | Add `<!-- BEGIN:GENERATED:FEATURES -->` and `<!-- END:GENERATED:FEATURES -->` markers to README-draft.md around the features section | **Critical** | Implementation | Before README commit |
| 3 | Create `.context/templates/docs/skill-examples.yaml` seeded from A2 content | **High** | Implementation | During doc module build |
| 4 | Create `.context/templates/docs/features.yaml` seeded from A2 content | **High** | Implementation | During doc module build |
| 5 | Decide on description source: add `skill-descriptions.yaml` (R-2 recommended) or add `readme-description` to SKILL.md frontmatter (R-1) | **Medium** | Design decision | Before doc module build |
| 6 | Verify initial auto-doc output matches A2 README content (golden file test) | **Medium** | Testing | After doc module build |

---

## Cross-Workstream Findings

### Pattern: Specification-First Pays Off

Workstream A produced the "what" (correct README content) while Workstream B produced the "how" (auto-generation mechanism). Running them in parallel revealed integration concerns (markers, description sources) that would have been discovered much later in a sequential approach. The synthesis barrier caught 5 discrepancies that, if unaddressed, would have caused the auto-doc module's first run to produce output incompatible with the intended README.

### Convergence Metrics

| Metric | Value |
|--------|-------|
| Total discrepancies found | 5 |
| Critical (blocks implementation) | 2 (missing markers) |
| High (requires new files) | 2 (static data seeding) |
| Medium (design decision) | 1 (description source) |
| A2/B4 structural compatibility | Compatible (2 sections overlap, 10 sections unaffected) |
| Column structure match | 100% (3/3 columns identical) |
| Agent count alignment | 100% (both produce 58) |
