# PROJ-032: Nuclear-SOP Skill Review & Remediation

> **Status:** ACTIVE
> **Created:** 2026-08-07
> **Target:** Merge-or-reject recommendation for PR [#269](https://github.com/geekatron/jerry/pull/269)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Why this project exists |
| [Objective](#objective) | What done looks like |
| [Review Subject](#review-subject) | Exactly what is being reviewed |
| [Phases](#phases) | The five-phase review + remediation arc |
| [Constraints](#constraints) | Ground rules for the review session |

---

## Context

External contributor PR [#269](https://github.com/geekatron/jerry/pull/269) adds the `/nuclear-sop` skill — nuclear-power-plant procedural discipline for AI workflows: 4 agents (sop-brief, sop-executor, sop-verifier, sop-capture) plus rules, templates, composition prompts, and behavioral baselines. Authored **April 2026**, predating several current standards (governance-file conventions, tier-model renumbering, output-path resolution protocol).

As of 2026-08-07 the PR is **CI-green (15/15)** after maintainer fixes (commits `8839891b`, `bda64202`: SKILL.md YAML repair, `tools`→`allowed-tools`, plugin.json registration of the 4 agents, changelog entry). **Green means it validates — the content has never been reviewed against current standards.** The author self-reports a C4 tournament pass at 0.943; that score is unverified.

## Objective

Owner-approved scope (2026-08-07): **review + remediation in one project, full C4 tournament depth.**

1. Independent, evidence-based review of the entire skill against current Jerry standards.
2. Findings tracked as worktracker items (GitHub issue parity per H-32) and remediated on the contributor's branch (`proj-0039-nuclear-engineer`, same-repo — maintainer pushes allowed and already precedented).
3. Terminal deliverable: a merge/reject/rework recommendation for PR #269 with the full evidence chain.

## Review Subject

| Artifact | Path (on the PR branch) |
|----------|------------------------|
| Skill definition | `skills/nuclear-sop/SKILL.md`, `PLAYBOOK.md` |
| Agents (4) | `skills/nuclear-sop/agents/sop-{brief,executor,verifier,capture}.md` + `.governance.yaml` companions |
| Support content | `skills/nuclear-sop/{rules,templates,composition,behavioral-baselines,docs,examples}/` |
| Registration | `.claude-plugin/plugin.json` (4 agent entries), `CHANGELOG.md` entry |

## Phases

| # | Phase | Method | Gate |
|---|-------|--------|------|
| 1 | Standards compliance | Validate all 4 agents + skill against `agent-development-standards.md` (H-34 dual-file architecture, H-35 constitutional triplet, tool tiers per ADR-STORY015-001, AD-M-011/output-path protocol per ADR-output-path-resolution-001) and `skill-standards.md` (H-25/H-26) | Zero HARD-rule violations or each tracked as a finding |
| 2 | Engineering review | `/eng-team` eng-reviewer over the skill's methodology, prompts, and security posture | Findings report |
| 3 | Adversarial tournament | `/adversary` **full C4 tournament** — all 10 strategies as blind background agents (6-group order: self-refine → steelman → challenge → verify → decompose → score), independent S-014 re-score of the author's claimed 0.943 | Composite ≥ 0.92 to PASS |
| 4 | Remediation | Findings → worktracker items (+ GitHub issues per H-32) → fixes pushed to the contributor branch → CI green | All Critical/Major findings closed |
| 5 | Verdict | Synthesis: merge / rework / reject recommendation with evidence | Owner decision on PR #269 |

## Constraints

- **Do not merge PR #269** — the terminal act is a recommendation; the owner merges.
- Background agents at **ultracode/maximum effort**; main context orchestrates only.
- All review artifacts persist under `projects/PROJ-032-nuclear-sop-review/` (P-002).
- Worktracker discipline: entities before work, closure only with evidence (WTI-002/WTI-003), no closure for branch-only fixes until effects are observable.
- Changelog gate honored — no `[skip-changelog]` without owner approval.
