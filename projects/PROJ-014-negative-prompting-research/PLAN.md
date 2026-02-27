# PROJ-014: Negative Prompting Research — Plan

> Deep research on whether telling LLMs what NOT to do outperforms telling them what to do.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Hypothesis](#hypothesis) | Core research question |
| [Scope](#scope) | What this project covers |
| [Constraints](#constraints) | Non-negotiable execution rules |
| [Phases](#phases) | High-level execution phases |
| [Deliverables](#deliverables) | Expected output artifacts |

---

## Hypothesis

**Negative unambiguous prompting reduces hallucination by 60% and achieves better results than explicit positive prompting.**

Evidence claims:
- "Never use jargon" outperforms "Write professionally"
- "Never write sentences over 20 words" outperforms "Write concisely"
- "Never assume technical knowledge" outperforms "Write for a general audience"

## Scope

1. **Literature Research**: 50+ sources from academic papers, vendor documentation, practitioner reports, and empirical studies
2. **Evidence Analysis**: Validate or refute the 60% hallucination reduction claim with primary sources
3. **Comparative Analysis**: Positive vs negative prompting effectiveness across dimensions
4. **Jerry Application**: Concrete update plans for Jerry skills, agents, rules, patterns, and templates
5. **Implementation Roadmap**: Prioritized changes to the Jerry framework

## Constraints

Per GitHub Issue #122 acceptance criteria (all expressed as negative constraints):

- Never use the main context to do all the work — delegate to specialized skill agents
- Never make assumptions — verify with sources
- Never state facts without sources (citations, evidence, references)
- Never use less than 50 sources
- Never rely on LLM training data — use Context7 and Web Search
- Never make decisions without querying Context7 and Web Search
- Never let creator output flow downstream without /adversary C4 quality gates (>= 0.95, up to 5 iterations)
- Never rely on generic Task agents — use specialized skill agents
- Never assume things stay in memory — persist to files
- Never start work without /worktracker entities
- Never leave /worktracker entities in inaccurate state
- Never leave documentation inaccurate or stale

## Phases

| Phase | Description | Skill Pipeline | Quality Gate |
|-------|-------------|----------------|-------------|
| 1 | Literature Research (academic + industry) | /problem-solving ps-researcher | /adversary C4 >= 0.95 |
| 2 | Evidence Analysis (validate claims) | /problem-solving ps-analyst | /adversary C4 >= 0.95 |
| 3 | Comparative Analysis (positive vs negative) | /problem-solving ps-analyst + ps-synthesizer | /adversary C4 >= 0.95 |
| 4 | Jerry Application Analysis | /problem-solving ps-analyst + ps-architect | /adversary C4 >= 0.95 |
| 5 | Implementation Planning | /problem-solving ps-architect + /nasa-se | /adversary C4 >= 0.95 |
| 6 | Final Synthesis & Recommendations | /problem-solving ps-synthesizer | /adversary C4 >= 0.95 |

## Deliverables

| Artifact | Path | Description |
|----------|------|-------------|
| Literature Survey | `research/literature-survey.md` | 50+ sources cataloged and analyzed |
| Evidence Analysis | `analysis/evidence-analysis.md` | Validation of hallucination reduction claims |
| Comparative Analysis | `analysis/comparative-analysis.md` | Positive vs negative prompting effectiveness |
| Jerry Application Plan | `analysis/jerry-application-plan.md` | How to apply findings to Jerry |
| Skills Update Plan | `decisions/skills-update-plan.md` | Specific changes to Jerry skills |
| Agents Update Plan | `decisions/agents-update-plan.md` | Specific changes to Jerry agents |
| Rules Update Plan | `decisions/rules-update-plan.md` | Specific changes to Jerry rules |
| Patterns Update Plan | `decisions/patterns-update-plan.md` | Specific changes to Jerry patterns |
| Templates Update Plan | `decisions/templates-update-plan.md` | Specific changes to Jerry templates |
| Final Synthesis | `synthesis/final-synthesis.md` | Unified findings and implementation roadmap |

---

*GitHub Issue: [#122](https://github.com/geekatron/jerry/issues/122)*
*Criticality: C4 (Critical)*
*Quality Threshold: >= 0.95*
*Created: 2026-02-27*
