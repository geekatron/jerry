# Session Entry Prompt — PROJ-032 Nuclear-SOP Review

> Prompt-design document (research category per Template 6 precedent). Paste [The Prompt](#the-prompt) into a fresh session.

> Copy the block below into a fresh Jerry session (with `JERRY_PROJECT=PROJ-032-nuclear-sop-review`) to start the review. It is self-contained; the session should not need this conversation's history.

## Document Sections

| Section | Purpose |
|---------|---------|
| [The Prompt](#the-prompt) | Ready-to-paste session entry |
| [Design Notes](#design-notes) | Why the prompt is shaped this way |

---

## The Prompt

```
Execute PROJ-032 (nuclear-sop skill review + remediation). Read
projects/PROJ-032-nuclear-sop-review/PLAN.md first — it is the authoritative scope.

Subject: PR #269 (branch proj-0039-nuclear-engineer) adding skills/nuclear-sop/
(SKILL.md, PLAYBOOK.md, 4 agents with .governance.yaml companions, rules/,
templates/, composition/, behavioral-baselines/). CI is green but content is
UNREVIEWED against current standards. Author self-reports C4 tournament 0.943 —
treat as unverified. Check out the PR branch in a separate git worktree for review.

Use /worktracker first: create the epic/feature/story decomposition for the five
phases in PLAN.md, with GitHub issue parity (H-32).

Phase 1 — Standards compliance: validate all 4 agents + SKILL.md against
agent-development-standards.md (H-34, H-35, tool tiers, AD-M-011 output paths)
and skill-standards.md (H-25/H-26), using jerry CLI validators where available.

Phase 2 — Engineering review: /eng-team eng-reviewer over methodology, prompts,
and security posture of the skill content.

Phase 3 — /adversary FULL C4 TOURNAMENT: all 10 strategies, each strategy as its
own blind background agent, honoring the 6-group order (self-refine → steelman →
challenge → verify → decompose → score, sequential between groups, parallel
within). Independent S-014 re-score; compare against the claimed 0.943.
Quality gate: >= 0.92 composite.

Phase 4 — Remediation: convert Critical/Major findings to worktracker items
(+ GitHub issues), fix them on the contributor branch (maintainer pushes are
precedented there), keep CI green.

Phase 5 — Verdict: synthesize a merge / rework / reject recommendation for
PR #269 with the evidence chain.

Operating rules: background agents at ultracode/maximum effort; main context
orchestrates only. Persist every deliverable under
projects/PROJ-032-nuclear-sop-review/ (P-002). Do NOT merge PR #269 — the
terminal deliverable is the recommendation. Honor the changelog gate. Closure
only with observable evidence (WTI-002/WTI-003).
```

## Design Notes

- **Self-contained** (AP-05 avoidance): the fresh session gets subject, phases, methods, gates, and constraints without needing this session's history; PLAN.md carries the durable detail.
- **Skill routing explicit** (/worktracker, /eng-team, /adversary) with agents named where it matters — per the 5-element prompt anatomy.
- **Tournament shape spelled out** (blind background agents, 6-group order) because the C4 tournament is the costliest phase and the ordering is a hard requirement (H-16 steelman-before-critique).
- **Author's 0.943 explicitly untrusted** so the session re-scores rather than anchors.
- **Merge withheld** (P-020): the owner decides on PR #269; the session recommends.
