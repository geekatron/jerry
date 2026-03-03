# Remediation Report: User-Facing Documentation Gaps

> **Project:** PROJ-015-documentation-audit
> **Generated:** 2026-03-02
> **Source Data:** Diataxis audit (TASK-015-001), classification (TASK-015-002), skill inventory (TASK-015-003)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Key findings and metrics |
| [Existing Documentation Gaps](#existing-documentation-gaps) | Issues in current 6 user-facing docs |
| [Missing Documentation](#missing-documentation) | Documents that should exist but do not |
| [Skill Coverage Gaps](#skill-coverage-gaps) | Per-quadrant coverage across 15 skills |
| [Prioritized Remediation Plan](#prioritized-remediation-plan) | Ordered action items with severity |
| [Metrics](#metrics) | Quantitative gap summary |

---

## Executive Summary

The Jerry Framework has **strong reference documentation** (100% skill coverage) but **critical gaps in tutorials (0%), explanations (13%), and documentation purity**. All 6 audited user-facing documents mix content from multiple Diataxis quadrants. One document (`prompt-quality.md`) requires major rework (three-way decomposition).

**Key metrics:**
- **6 documents audited**: 0 PASS, 5 NEEDS REVISION, 1 MAJOR REWORK
- **15 skills inventoried**: 0% tutorial coverage, 93% how-to, 100% reference, 13% explanation
- **9 Major findings** across audited documents
- **7 missing documents** identified (needed for extraction/decomposition)
- **0 documents** declare their Diataxis quadrant

---

## Existing Documentation Gaps

### Audit Verdicts

| Document | Classification | Confidence | Major Findings | Minor Findings | Verdict |
|----------|---------------|------------|----------------|----------------|---------|
| `docs/BOOTSTRAP.md` | How-To Guide | 0.85 | 2 | 2 | NEEDS REVISION |
| `docs/INSTALLATION.md` | How-To Guide | 0.92 | 3 | 5 | NEEDS REVISION |
| `docs/CLAUDE-MD-GUIDE.md` | How-To (primary) / Explanation (secondary) | 0.80 | 1 | 3 | NEEDS REVISION |
| `docs/runbooks/getting-started.md` | Tutorial | 0.93 | 0 | 4 | NEEDS REVISION |
| `.context/rules/prompt-templates.md` | How-To + Reference (mixed) | 0.94 | 1 | 3 | NEEDS REVISION |
| `.context/rules/prompt-quality.md` | Multi-quadrant (3-way) | 0.70 | 2 | 4 | MAJOR REWORK |

### Cross-Document Issues

| Issue | Documents Affected | Category |
|-------|-------------------|----------|
| No Diataxis quadrant declared in metadata | All 6 | Structural |
| Explanation content embedded in procedural docs | 5 of 6 (all except getting-started.md) | Quadrant mixing |
| Marketing voice in how-to guides | INSTALLATION.md | Voice violation |
| Reference tables embedded in non-reference docs | 4 of 6 | Quadrant mixing |
| Tutorial branching (alternatives in learning path) | getting-started.md | Tutorial purity |

### Classifier vs. Auditor Agreement

| Document | Classifier Quadrant | Auditor Quadrant | Agreement |
|----------|-------------------|-----------------|-----------|
| BOOTSTRAP.md | How-To (0.95) | How-To (0.85) | Agree |
| INSTALLATION.md | How-To (0.92) | How-To (0.85) | Agree |
| CLAUDE-MD-GUIDE.md | Explanation (0.80) | How-To primary, Explanation secondary (0.85) | Partial -- classifier sees explanation as primary; auditor sees how-to as primary |
| getting-started.md | Tutorial (0.93) | Tutorial (1.00) | Agree |
| prompt-templates.md | How-To (0.94) | How-To + Reference mixed (0.85) | Partial -- classifier sees pure how-to; auditor detects reference mixing |
| prompt-quality.md | Reference (0.85) | Multi-quadrant (0.70) | Partial -- both detect mixing; disagree on primary |

**Documents requiring decomposition (both agents agree):** CLAUDE-MD-GUIDE.md, prompt-quality.md

---

## Missing Documentation

### Documents Needed for Extraction (from audit remediation)

These documents do not exist but are needed to receive content extracted from existing mixed-quadrant documents.

| # | Missing Document | Type | Source Extractions | Priority |
|---|-----------------|------|--------------------|----------|
| 1 | `docs/explanation/context-architecture.md` | Explanation | "Why two directories?" + "How It Works" (BOOTSTRAP.md), "Context Architecture" (CLAUDE-MD-GUIDE.md) | P1 -- resolves 3 Major findings |
| 2 | `docs/explanation/hooks-architecture.md` | Explanation | Hooks metaphor paragraph + capability matrix rationale (INSTALLATION.md) | P1 -- resolves 2 Major findings |
| 3 | How-to: "Review a Jerry Prompt" | How-To Guide | Pre-Submission Checklist (prompt-quality.md) | P1 -- resolves 1 Major finding |
| 4 | How-to: "Apply Adversarial Critique" | How-To Guide | Critique Loop invocation (prompt-quality.md) | P1 -- resolves 1 Major finding |
| 5 | How-to: "Choose and Use a Prompt Template" | How-To Guide | Template Quick-Select + usage guidance (prompt-templates.md) | P2 -- resolves 1 Major finding |
| 6 | Jerry Skills Reference | Reference | Available Skills table (INSTALLATION.md), agent selection table (prompt-quality.md) | P2 |
| 7 | Jerry CLI Reference | Reference | Command Reference table (BOOTSTRAP.md) | P3 |

### Documents Missing from Skill Coverage

These represent entire documentation categories that are absent.

| # | Missing Category | Affected Skills | Priority |
|---|-----------------|----------------|----------|
| 1 | Tutorials (0% coverage) | All 15 skills | P1 -- blocks adoption for new users |
| 2 | Explanations (87% gap) | 13 of 15 skills (all except saucer-boy variants) | P2 -- users understand *what* but not *why* |
| 3 | Worked examples | All 15 skills | P2 -- no end-to-end demonstrations |
| 4 | Skill-specific playbooks (73% gap) | 11 of 15 skills | P3 |
| 5 | Skill-specific runbooks (93% gap) | 14 of 15 skills | P3 |

---

## Skill Coverage Gaps

### Coverage Matrix (15 Skills x 4 Quadrants)

| # | Skill | Tutorial | How-To | Reference | Explanation | Agents |
|---|-------|----------|--------|-----------|-------------|--------|
| 1 | `/adversary` | -- | Yes | Yes | -- | 3 |
| 2 | `/ast` | -- | Yes | Yes | -- | 0 |
| 3 | `/bootstrap` | -- | Yes | Yes | -- | 0 |
| 4 | `/diataxis` | -- | Yes | Yes | -- | 6 |
| 5 | `/eng-team` | -- | Yes | Yes | -- | 10 |
| 6 | `/nasa-se` | -- | Yes | Yes | -- | 10 |
| 7 | `/orchestration` | -- | Yes | Yes | -- | 3 |
| 8 | `/problem-solving` | -- | Yes | Yes | -- | 9 |
| 9 | `/prompt-engineering` | -- | Yes | Yes | -- | 3 |
| 10 | `/red-team` | -- | Yes | Yes | -- | 11 |
| 11 | `/saucer-boy` | -- | Yes | Yes | Yes | 1 |
| 12 | `/saucer-boy-framework-voice` | -- | Yes | Yes | Yes | 3 |
| 13 | `/transcript` | -- | Yes | Yes | -- | 5 |
| 14 | `/worktracker` | -- | Yes | Yes | -- | 3 |
| 15 | `/architecture` | -- | Yes | Yes | -- | 0 |

### Coverage Percentages

| Quadrant | Coverage | Skills Missing |
|----------|----------|---------------|
| Tutorial | **0%** (0/15) | All 15 |
| How-To | 93% (14/15) | `/saucer-boy` (no standalone how-to) |
| Reference | **100%** (15/15) | None |
| Explanation | **13%** (2/15) | 13 skills (all except saucer-boy variants) |

### Recommended Tutorial Priority (Top 5)

| Rank | Skill | Rationale |
|------|-------|-----------|
| 1 | `/problem-solving` | Most-used skill, 9 agents, entry point for new users |
| 2 | `/orchestration` | Complex multi-agent coordination, high learning curve |
| 3 | `/worktracker` | Required for all project work (H-04), foundational |
| 4 | `/eng-team` | 10 agents, complex security methodology |
| 5 | `/prompt-engineering` | Newest skill, operationalizes PROJ-014 findings |

---

## Prioritized Remediation Plan

### P1: Critical (Blocks Adoption)

| # | Action | Effort | Documents Affected | Findings Resolved |
|---|--------|--------|-------------------|-------------------|
| 1.1 | Decompose `prompt-quality.md` into explanation + 2 how-to guides + reference | High | prompt-quality.md, 3 new docs | 2 Major |
| 1.2 | Create `docs/explanation/context-architecture.md` from BOOTSTRAP.md + CLAUDE-MD-GUIDE.md extractions | Medium | BOOTSTRAP.md, CLAUDE-MD-GUIDE.md, 1 new doc | 3 Major |
| 1.3 | Create `docs/explanation/hooks-architecture.md` from INSTALLATION.md extractions | Medium | INSTALLATION.md, 1 new doc | 2 Major |
| 1.4 | Remove marketing voice from INSTALLATION.md | Low | INSTALLATION.md | 1 Major + 4 Minor |
| 1.5 | Write `/problem-solving` tutorial (top-priority skill tutorial) | High | 1 new doc | Coverage gap |
| 1.6 | Write `/orchestration` tutorial | High | 1 new doc | Coverage gap |

### P2: High (Improves UX)

| # | Action | Effort | Documents Affected | Findings Resolved |
|---|--------|--------|-------------------|-------------------|
| 2.1 | Decompose `prompt-templates.md` into reference catalog + how-to guide | Medium | prompt-templates.md, 1 new doc | 1 Major |
| 2.2 | Fix title framing on BOOTSTRAP.md, CLAUDE-MD-GUIDE.md, prompt-templates.md | Low | 3 docs | 3 Minor |
| 2.3 | Write `/worktracker` tutorial | High | 1 new doc | Coverage gap |
| 2.4 | Write explanation docs for top 5 skills | High | 5 new docs | 5 explanation gaps |
| 2.5 | Create Jerry Skills Reference (consolidate fragmented tables) | Medium | 1 new doc | 2 Minor |

### P3: Medium (Polish)

| # | Action | Effort | Documents Affected | Findings Resolved |
|---|--------|--------|-------------------|-------------------|
| 3.1 | Fix tutorial branching in getting-started.md Step 3 | Low | getting-started.md | 1 Minor |
| 3.2 | Compress "why" digressions in getting-started.md | Low | getting-started.md | 2 Minor |
| 3.3 | Create Jerry CLI Reference | Low | BOOTSTRAP.md, 1 new doc | 1 Minor |
| 3.4 | Add Diataxis quadrant metadata to all docs | Low | All 6 audited docs | Structural |
| 3.5 | Write tutorials for remaining 10 skills | Very High | 10 new docs | 10 coverage gaps |

---

## Metrics

| Metric | Value |
|--------|-------|
| Documents audited | 6 |
| Documents passing audit | 0 (0%) |
| Documents needing revision | 5 (83%) |
| Documents needing major rework | 1 (17%) |
| Total Major findings | 9 |
| Total Minor findings | 21 |
| Skills inventoried | 15 |
| Tutorial coverage | 0% (0/15) |
| How-to coverage | 93% (14/15) |
| Reference coverage | 100% (15/15) |
| Explanation coverage | 13% (2/15) |
| New documents needed (extraction) | 7 |
| New documents needed (skill coverage) | 28+ (tutorials + explanations) |
| Classifier-auditor agreement rate | 50% full agree, 50% partial agree, 0% disagree |
