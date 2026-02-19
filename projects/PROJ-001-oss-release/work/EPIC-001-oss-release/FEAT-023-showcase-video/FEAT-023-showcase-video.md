# FEAT-023: Claude Code Birthday Showcase — Promotional Video

> **Type:** feature
> **Status:** done
> **Priority:** critical
> **Impact:** high
> **Created:** 2026-02-18
> **Due:** 2026-02-18
> **Completed:** 2026-02-18
> **Parent:** EPIC-001
> **Owner:** Adam Nowak

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature is about |
| [Context](#context) | Event details and requirements |
| [Acceptance Criteria](#acceptance-criteria) | What done looks like |
| [Children (Enablers)](#children-enablers) | Work breakdown |
| [History](#history) | Change log |

---

## Summary

Create a 2-minute promotional hype reel video for Jerry Framework to submit to Claude Code's 1st Birthday Party & Showcase (Feb 21, 2026 at Shack15, SF). The video uses InVideo AI platform and embodies the Saucer Boy persona from EPIC-005.

**Target audience:** Anthropic leadership, top investors, and developers at the showcase.

**Key angle:** The meta story — Claude Code built its own quality guardrails framework. Jerry is AI governing AI, and it has soul.

---

## Context

**Event:** Claude Code's 1st Birthday Party & Showcase
**Date:** February 21, 2026, 4:00 PM – 8:00 PM PST
**Location:** Shack15, 1 Ferry Building, Suite 201, San Francisco, CA 94111
**Format:** Science fair-style showcase, main stage presentations, fireside chat, awards
**Awards:** Best Demo of the Day, Investor's Choice (guaranteed investor intro)

**Application requires:**
- 2-minute demo video (YouTube, Loom, or similar)
- Project name and 2-3 sentence description
- Deployed product URL
- Public GitHub repository link
- Optional: Opus 4.6 capabilities showcased

---

## Acceptance Criteria

- [x] AC-1: 2-minute hype reel script written with Saucer Boy persona — v5 final (257 words)
- [x] AC-2: Script passes adversarial quality review (>= 0.92) — C4 tournament, 4 iterations, composite 0.92 (PASS)
- [x] AC-3: Application materials prepared (description, URLs, capabilities)
- [x] AC-4: Video produced via InVideo from script
- [x] AC-5: Application submitted to cerebralvalley.ai

---

## Children (Enablers)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| EN-945 | Video Script & Application Materials | done | critical |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-18 | Adam Nowak | in_progress | Feature created. Deadline: TODAY. Event: Claude Code 1st Birthday (Feb 21). InVideo hype reel approach. |
| 2026-02-18 | Claude | done | EN-945 complete. Orchestration `feat023-showcase-20260218-001`: 5 phases, C4 tournament (4 iterations). Script v5 final (257 words). Composite score: 0.92 (PASS at H-13 threshold). All 14 findings from iteration 3 addressed in v4/v5. Application submitted. |

## Delivery Evidence

| Evidence | Details |
|----------|---------|
| Final script | `orchestration/feat023-showcase-20260218-001/showcase/phase-3-tournament/iteration-5/ps-architect-001-hype-reel-script-v5.md` |
| Tournament score | Iteration 4 composite: 0.92 (C4, 10 strategies, H-13 PASS) |
| Iteration trajectory | iter-1: 0.83, iter-2: 0.86, iter-3: 0.89, iter-4: 0.92 |
| Orchestration workflow | `feat023-showcase-20260218-001` (5 phases) |
| Application | Submitted to cerebralvalley.ai |
