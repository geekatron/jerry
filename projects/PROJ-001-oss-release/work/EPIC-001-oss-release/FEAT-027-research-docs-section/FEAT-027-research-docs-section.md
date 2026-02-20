# FEAT-027: Research Section for Public Documentation Site

> **Type:** feature
> **Status:** done
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-19
> **Parent:** EPIC-001
> **Owner:** --
> **Target Sprint:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children (Enablers)](#children-enablers) | Enabler inventory |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Hierarchy and related items |
| [History](#history) | Status changes |

---

## Summary

Expose ~47 research artifacts produced during PROJ-001 through a curated "Research" section on the public documentation site (jerry.geekatron.org). Uses a tiered presentation approach:

- **Key findings** inline on the docs site (summaries, methodology highlights)
- **Expandable details** via MkDocs Material admonitions (collapsible sections)
- **GitHub cross-links** to full artifacts in the repository for deep reading

Serves dual audience: developers/practitioners building similar frameworks AND AI/LLM community researchers interested in guardrails, adversarial quality, and context management.

### Research Domains Covered

| Domain | Artifacts | Public Value |
|--------|-----------|--------------|
| Adversarial Strategies & Quality | 14 | High -- novel approach to LLM quality enforcement |
| Context Management & LLM Performance | 4 | High -- addresses universal context rot problem |
| OSS Release Preparation | 8 | Medium -- practical OSS checklist |
| Agent Architecture & Multi-Agent | 2 | High -- evidence-based analysis with peer-reviewed sources |
| Skill Architecture & Patterns | 4 | Medium -- reusable Claude Code skill patterns |
| Claude Code & Plugin Ecosystem | 3 | Medium -- plugin/skill ecosystem patterns |
| Software Architecture & Design | 3 | Low-Medium -- teaching reference material |
| Governance & Constitutional AI | 3 | High -- constitutional AI governance for agents |
| Documentation & Knowledge Management | 6 | Low -- project-specific trade studies |

---

## Benefit Hypothesis

**If** we expose curated research through the public docs site **then** the Jerry Framework gains visibility as a serious research-backed project, attracts contributors who value evidence-based engineering, and provides reusable methodology templates (FMEA, trade studies, adversarial strategies) to the broader LLM tooling community.

---

## Acceptance Criteria

- [x] AC-1: Research section visible in MkDocs navigation with logical grouping by domain
- [x] AC-2: Tier 1 flagship research (7 artifacts) has dedicated summary pages with key findings, methodology, and GitHub cross-links
- [x] AC-3: Tier 2/3 research (16 artifacts) has curated entries with summaries and GitHub links
- [x] AC-4: All GitHub cross-links resolve correctly (no 404s)
- [x] AC-5: `mkdocs build --strict` passes with research section included
- [x] AC-6: Research catalog (`projects/PROJ-001-oss-release/research/research-catalog.md`) referenced as source of truth for artifact selection
- [x] AC-7: Quality gate PASS (>= 0.92) via /adversary review — scored 0.93

---

## Children (Enablers)

| ID | Title | Status | Effort | Priority |
|----|-------|--------|--------|----------|
| [EN-958](./EN-958-research-section-architecture/EN-958-research-section-architecture.md) | Research Section Architecture & Navigation | done | 3 | high |
| [EN-959](./EN-959-tier1-flagship-research/EN-959-tier1-flagship-research.md) | Tier 1 Flagship Research Pages | done | 5 | high |
| [EN-960](./EN-960-tier2-tier3-supporting-research/EN-960-tier2-tier3-supporting-research.md) | Tier 2 & 3 Supporting Research Pages | done | 5 | medium |
| [EN-961](./EN-961-mkdocs-integration/EN-961-mkdocs-integration.md) | MkDocs Integration & Build Validation | done | 3 | high |
| [EN-962](./EN-962-quality-gate/EN-962-quality-gate.md) | Quality Gate & Adversarial Review | done | 2 | high |

**Total Effort:** 18 points

---

## Progress Summary

| Metric | Value |
|--------|-------|
| Total Enablers | 5 |
| Completed | 5 |
| In Progress | 0 |
| Pending | 0 |
| Completion | 100% |

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../../EPIC-001-oss-release/EPIC-001-oss-release.md)

### Dependencies

- **FEAT-024** (Public Documentation Site) -- MkDocs infrastructure must be in place (COMPLETE)
- **Research Catalog:** `projects/PROJ-001-oss-release/research/research-catalog.md` -- artifact selection source

### Related Features

- FEAT-018 (Runbooks & Playbooks) -- existing docs site content
- FEAT-026 (Post-Public Docs Refresh) -- recent docs site updates

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Feature created. 47 research artifacts cataloged across 9 domains. Tiered presentation approach (inline + admonitions + GitHub links) selected per user preference. |
| 2026-02-19 | Claude | done | All 5 enablers complete. 10 research pages + landing page created. MkDocs integrated with 11-page Research nav section. Quality gate PASS: S-014 scored 0.93 after creator-critic-revision cycle (0.886 → 0.93). |

---
