# Quality Score Report: Prompt Engineering SKILL.md

## L0 Executive Summary
**Score:** 0.72/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.58)
**One-line assessment:** Multiple structural requirements missing (Document Audience triple-lens, agent files, registration in CLAUDE.md/AGENTS.md/mandatory-skill-usage.md, referenced rules file) -- targeted additions needed before C4 threshold of 0.95 can be reached.

## Scoring Context
- **Deliverable:** `/Users/anowak/workspace/github/jerry-wt/proj-014-negative-prompting-research/skills/prompt-engineering/SKILL.md`
- **Deliverable Type:** Skill Definition (SKILL.md)
- **Criticality Level:** C4
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Quality Threshold:** >= 0.95 (C4, user-specified)
- **Scored:** 2026-03-01T12:00:00Z
- **Iteration:** 1 of max 5 (FA-03)

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.72 |
| **Threshold** | 0.95 (user-specified, C4) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.58 | 0.116 | Missing 5 required structural elements per skill-standards.md |
| Internal Consistency | 0.20 | 0.82 | 0.164 | References to nonexistent files contradict deliverable integrity |
| Methodological Rigor | 0.20 | 0.78 | 0.156 | Follows skill standard structure but omits required sections |
| Evidence Quality | 0.15 | 0.80 | 0.120 | Research citations present; some references to nonexistent artifacts |
| Actionability | 0.15 | 0.72 | 0.108 | Agent routing guide and quick reference present but agents do not exist yet |
| Traceability | 0.10 | 0.68 | 0.068 | References section present but incomplete; missing registration traceability |
| **TOTAL** | **1.00** | | **0.732** | |

**Note:** Composite computed as 0.116 + 0.164 + 0.156 + 0.120 + 0.108 + 0.068 = 0.732. Rounded to 0.73 for summary; detail retained at 0.732.

## Detailed Dimension Analysis

### Completeness (0.58/1.00)

**Evidence:**

The deliverable addresses the core skill definition well: it has YAML frontmatter with name/description/version/allowed-tools/activation-keywords, a navigation table (H-23), Overview, When to Use, Available Agents, Quick Reference, Routing Disambiguation, Constitutional Compliance, and Architecture Notes sections.

However, against the skill-standards.md body structure requirements (14 sections, 8 marked Required), multiple required elements are missing:

1. **Document Audience (Triple-Lens) section -- MISSING (Required #3).** Skill-standards.md section #3 requires a "Document Audience (Triple-Lens)" table with L0/L1/L2 audience rows. Every other production skill in the repo includes this section (confirmed via grep: `/adversary`, `/problem-solving`, `/orchestration`, `/nasa-se`, `/ast`, `/transcript`, `/eng-team`, `/red-team`, `/saucer-boy`, `/saucer-boy-framework-voice`, `/bootstrap`, `/architecture` all have it). The prompt-engineering SKILL.md omits it entirely.

2. **Agent definition files -- MISSING.** The SKILL.md references three agents at specific paths (`skills/prompt-engineering/agents/pe-builder.md`, `pe-constraint-gen.md`, `pe-scorer.md`). None of these files exist (confirmed via `Glob: skills/prompt-engineering/agents/*.md` returning no results). A multi-agent skill without agent definitions is structurally incomplete.

3. **Registration in CLAUDE.md -- MISSING (H-26c HARD).** Grep for "prompt-engineering" in CLAUDE.md returns zero matches. H-26(c) states: "New skills MUST be registered in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md (if proactive per H-22)." This is a HARD rule violation.

4. **Registration in AGENTS.md -- MISSING (H-26c HARD).** Grep for "prompt-engineering" in AGENTS.md returns zero matches. AGENTS.md has no section for prompt-engineering agents.

5. **Registration in mandatory-skill-usage.md -- MISSING (H-26c conditional).** Grep for "prompt-engineering" in mandatory-skill-usage.md returns zero matches. If the skill is meant to be proactively invoked per H-22, it needs a trigger map entry.

6. **Referenced rules file -- MISSING.** Line 214 references `skills/prompt-engineering/rules/npt-pattern-reference.md`. This file does not exist (confirmed via `Glob: skills/prompt-engineering/rules/*.md` returning no results).

**Gaps:**
- Document Audience (Triple-Lens) section (Required #3 per skill-standards.md)
- Three agent definition files (pe-builder.md, pe-constraint-gen.md, pe-scorer.md)
- CLAUDE.md registration (H-26c HARD violation)
- AGENTS.md registration (H-26c HARD violation)
- mandatory-skill-usage.md trigger map entry (H-26c conditional)
- Referenced `npt-pattern-reference.md` rules file

**Improvement Path:**
- Add Document Audience (Triple-Lens) section between navigation table and Overview
- Create the three agent definition files in `skills/prompt-engineering/agents/`
- Register the skill in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md
- Create or remove reference to `npt-pattern-reference.md`
- These are all additive -- the existing content is well-structured and does not need rework

### Internal Consistency (0.82/1.00)

**Evidence:**

The document is internally consistent in its claims about:
- NPT-013 format definition (line 56) matches usage examples (lines 140-147)
- NPT-009 format definition (line 55) is consistent with `agent-development-standards.md` guardrails template
- P-003 compliance diagram (lines 100-118) correctly shows single-level hierarchy
- The 7-criterion rubric references match `.context/rules/prompt-quality.md`
- PROJ-014 research statistics (100% vs 92.2%, p=0.016, CONDITIONAL GO) are cited consistently in Overview and Architecture Notes

**Gaps:**
- Line 84 references `skills/prompt-engineering/agents/pe-builder.md` -- file does not exist. The Available Agents table describes capabilities of agents that have not been created. This is a consistency gap: the SKILL.md describes a multi-agent skill but the agents do not exist.
- Line 214 references `skills/prompt-engineering/rules/npt-pattern-reference.md` -- file does not exist. The References table promises a "NPT pattern catalog" that is absent.
- The description field says "Guides users through the 5-element prompt anatomy" -- this is a capability claim, but the agent that would implement it (pe-builder) does not exist yet.

**Improvement Path:**
- Create the referenced agent and rules files, or remove references until they exist
- Alternatively, mark the SKILL.md as a specification (not yet operational) to align claims with reality

### Methodological Rigor (0.78/1.00)

**Evidence:**

The deliverable follows established Jerry skill conventions:
- YAML frontmatter format matches `skill-standards.md` requirements (name, description, version, allowed-tools, activation-keywords)
- Navigation table follows NAV-001/NAV-006 format with section-purpose columns and anchor links (H-23)
- Routing Disambiguation uses NPT-013 "NEVER invoke" consequence format per TASK-037 standard (lines 71-74)
- Constitutional Compliance uses NPT-013 3-column format per TASK-035 standard (lines 191-194)
- Section ordering follows skill-standards.md recommended order (Overview -> When to Use -> Available Agents -> Quick Reference -> Routing Disambiguation -> Constitutional Compliance -> Architecture Notes)
- The skill correctly identifies its agents' cognitive modes (integrative for builder, systematic for constraint gen, convergent for scorer)

**Gaps:**
- Missing Document Audience (Triple-Lens) section -- this is a structural methodology gap, not just a content gap. The triple-lens pattern is a methodological standard for skill documentation.
- No "Invoking an Agent" section (Required #8 for multi-agent skills per skill-standards.md) showing the three invocation options (natural language, explicit agent, Task tool code).
- The `description` field in frontmatter includes WHAT and trigger phrases but the WHEN element is only implicit ("Guides users through..." implies "when constructing prompts" but does not state it explicitly). Skill-standards.md H-26(a) requires WHAT + WHEN + triggers.

**Improvement Path:**
- Add Document Audience (Triple-Lens) section
- Add "Invoking an Agent" section with the three invocation options
- Make WHEN explicit in the frontmatter description (e.g., "Invoke when building structured prompts, generating NPT constraints, or scoring prompt quality.")

### Evidence Quality (0.80/1.00)

**Evidence:**

Claims are generally well-supported:
- PROJ-014 research finding (NPT-013: 100% vs 92.2%, p=0.016) is cited with specific statistics and the PG-003 CONDITIONAL GO classification (lines 43, 215)
- NPT format definitions (lines 53-56) align with established patterns in `agent-development-standards.md`
- The 7-criterion rubric reference (line 49) traces to `.context/rules/prompt-quality.md` which is a real, verified file
- The 5-element prompt anatomy traces to `.context/rules/prompt-quality.md` (confirmed via the auto-loaded rules)
- Cross-references to `agent-development-standards.md`, `quality-enforcement.md`, and `prompt-templates.md` are valid references to existing files

**Gaps:**
- Reference to `skills/prompt-engineering/rules/npt-pattern-reference.md` (line 214) cites a nonexistent file -- this is an evidence quality failure since the "NPT pattern catalog" it promises does not exist to substantiate the claim
- Agent capability claims (lines 84-86) describe what each agent does, but the agents do not exist -- these are aspirational descriptions, not evidence-backed claims
- No link to the actual PROJ-014 research output files (e.g., the A/B testing report) -- only summary statistics are provided

**Improvement Path:**
- Create the `npt-pattern-reference.md` file or remove the reference
- Add direct file path references to PROJ-014 research deliverables for full evidence traceability
- Create agent files so that capability claims are substantiated

### Actionability (0.72/1.00)

**Evidence:**

The skill provides actionable guidance in several areas:
- Quick Reference section (lines 122-168) gives four concrete invocation examples with expected behavior
- Agent Routing Guide (lines 89-94) provides keyword-to-agent mapping for users
- Common Workflows table (lines 159-167) maps needs to agents with examples
- NPT Format Reference table (lines 53-56) gives copy-paste format strings
- "When to Use This Skill" section (lines 60-76) gives explicit trigger conditions and exclusions

**Gaps:**
- The primary actionability gap is that the agents referenced do not exist. A user following the Quick Reference examples would invoke agents that are not available. The actionability is aspirational rather than operational.
- No "Invoking an Agent" section showing the Task tool invocation code block. Users cannot act on delegation instructions without seeing the actual invocation syntax.
- The NPT constraint generation example (lines 140-147) shows the output format but not the step-by-step process the agent follows -- this is less actionable for understanding what will happen.

**Improvement Path:**
- Create the agent definition files to make the skill operational
- Add an "Invoking an Agent" section with the three invocation patterns (natural language, explicit agent name, Task tool code)
- Consider adding a step-by-step workflow description for each agent's methodology

### Traceability (0.68/1.00)

**Evidence:**

The References table (lines 209-217) provides six source references with file paths:
- `.context/rules/prompt-quality.md` -- valid
- `.context/rules/prompt-templates.md` -- valid
- `skills/prompt-engineering/rules/npt-pattern-reference.md` -- INVALID (file does not exist)
- PROJ-014 research findings -- referenced by name but no file path
- `.context/rules/agent-development-standards.md` -- valid
- `.context/rules/quality-enforcement.md` -- valid

**Gaps:**
- One of six references points to a nonexistent file (16.7% broken reference rate)
- PROJ-014 research findings are cited without a specific file path -- cannot trace the claim "100% vs 92.2%, p=0.016" back to its source document
- H-26(c) registration traceability is entirely absent -- no entry in CLAUDE.md, AGENTS.md, or mandatory-skill-usage.md means the skill is undiscoverable through standard Jerry mechanisms
- No version blockquote header references to specific ADRs or design decisions that motivated this skill's creation (the Architecture Notes section mentions PROJ-014 but no ADR identifier)
- Agent definition files are referenced but do not exist, breaking the traceability chain from SKILL.md -> agent definition -> governance YAML

**Improvement Path:**
- Fix or remove the broken reference to `npt-pattern-reference.md`
- Add a specific file path for the PROJ-014 research findings (e.g., the A/B testing report path)
- Complete H-26(c) registration in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md
- Consider adding an ADR reference for the skill creation decision

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.58 | 0.85+ | **Create the three agent definition files** (`pe-builder.md`, `pe-constraint-gen.md`, `pe-scorer.md` in `skills/prompt-engineering/agents/`). These are the largest single gap -- the SKILL.md describes a multi-agent skill but no agents exist. |
| 2 | Completeness | 0.58 | 0.85+ | **Register in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md** per H-26(c) HARD rule. Without registration, the skill is undiscoverable. |
| 3 | Completeness | 0.58 | 0.85+ | **Add Document Audience (Triple-Lens) section** between navigation table and Overview. Follow the format used by all other production skills. |
| 4 | Completeness | 0.58 | 0.85+ | **Add "Invoking an Agent" section** with three invocation options per skill-standards.md Required #8 for multi-agent skills. |
| 5 | Traceability | 0.68 | 0.85+ | **Create `skills/prompt-engineering/rules/npt-pattern-reference.md`** or remove the reference from line 214. Broken references degrade both traceability and evidence quality. |
| 6 | Evidence Quality | 0.80 | 0.90+ | **Add specific file paths to PROJ-014 research deliverables** in the References table (e.g., path to A/B testing report, path to research synthesis). |
| 7 | Methodological Rigor | 0.78 | 0.90+ | **Make WHEN explicit in the frontmatter description** per H-26(a). Add phrasing like "Invoke when building structured prompts, generating NPT constraints, or scoring prompt quality." |

## Critical Findings

| # | Finding | Severity | Source |
|---|---------|----------|--------|
| CF-01 | H-26(c) HARD violation: skill not registered in CLAUDE.md | Critical | H-26(c), grep confirms zero matches |
| CF-02 | H-26(c) HARD violation: skill not registered in AGENTS.md | Critical | H-26(c), grep confirms zero matches |
| CF-03 | Three referenced agent files do not exist | Critical | Glob confirms no files in `skills/prompt-engineering/agents/` |
| CF-04 | Referenced `npt-pattern-reference.md` does not exist | High | Glob confirms no files in `skills/prompt-engineering/rules/` |
| CF-05 | Document Audience (Triple-Lens) Required section missing | High | Skill-standards.md Required #3 |

**Note:** CF-01 and CF-02 are HARD rule violations (H-26c). Per scoring process rules, Critical findings from adv-executor reports trigger automatic REVISE regardless of score. These Critical findings have the same blocking effect.

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Completeness: chose 0.58 over 0.62 due to HARD rule violations; Traceability: chose 0.68 over 0.72 due to broken reference)
- [x] First-draft calibration considered (this is a first draft -- scores above 0.85 would require exceptional evidence; no dimension scored above 0.85)
- [x] No dimension scored above 0.95 without exceptional evidence (highest score: 0.82 for Internal Consistency)
- [x] Weighted composite verified: 0.116 + 0.164 + 0.156 + 0.120 + 0.108 + 0.068 = 0.732

---

## Session Context (adv-scorer -> orchestrator)

```yaml
verdict: REVISE
composite_score: 0.73
threshold: 0.95
weakest_dimension: Completeness
weakest_score: 0.58
critical_findings_count: 5
iteration: 1
improvement_recommendations:
  - "Create three agent definition files (pe-builder.md, pe-constraint-gen.md, pe-scorer.md)"
  - "Register skill in CLAUDE.md, AGENTS.md, and mandatory-skill-usage.md (H-26c HARD)"
  - "Add Document Audience (Triple-Lens) section (Required #3)"
  - "Add Invoking an Agent section (Required #8 for multi-agent)"
  - "Create or remove reference to npt-pattern-reference.md"
  - "Add specific PROJ-014 research file paths to References"
  - "Make WHEN explicit in frontmatter description (H-26a)"
```

---

*Scored by: adv-scorer (S-014 LLM-as-Judge)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Scored: 2026-03-01*
