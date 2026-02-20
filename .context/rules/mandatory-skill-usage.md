# Mandatory Skill Usage

> Proactive skill invocation rules. DO NOT wait for user to invoke.

<!-- L2-REINJECT: rank=6, tokens=50, content="Proactive skill invocation REQUIRED (H-22). /problem-solving for research. /nasa-se for design. /orchestration for workflows. /transcript for transcript parsing and meeting notes. /adversary for standalone adversarial reviews, tournament scoring, formal strategy application." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Skill invocation constraint H-22 |
| [Trigger Map](#trigger-map) | Keywords to skill mapping |
| [Behavior Rules](#behavior-rules) | How to apply skill invocation |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence |
|----|------|-------------|
| H-22 | MUST invoke `/problem-solving` for research/analysis. MUST invoke `/nasa-se` for requirements/design. MUST invoke `/orchestration` for multi-phase workflows. MUST invoke `/transcript` for transcript parsing and meeting note extraction. MUST invoke `/adversary` for standalone adversarial reviews outside creator-critic loops, tournament scoring, and formal strategy application (red team, devil's advocate, steelman, pre-mortem). | Work quality degradation. Rework required. |

---

## Trigger Map

| Detected Keywords | Skill |
|-------------------|-------|
| research, analyze, investigate, explore, root cause, why | `/problem-solving` |
| requirements, specification, V&V, technical review, risk | `/nasa-se` |
| orchestration, pipeline, workflow, multi-agent, phases, gates | `/orchestration` |
| transcript, meeting notes, parse recording, meeting recording, VTT, SRT, captions | `/transcript` |
| adversarial quality review, adversarial critique, rigorous critique, formal critique, adversarial, tournament, red team, devil's advocate, steelman, pre-mortem, quality gate, quality scoring | `/adversary` |

---

## Behavior Rules

1. DO NOT WAIT for user to invoke skills -- use proactively when triggers apply.
2. COMBINE skills when appropriate (e.g., /orchestration + /problem-solving + /nasa-se).
3. INVOKE EARLY at start of work, not after struggling without them.
4. PERSIST all skill outputs to the repository.
5. See `skills/{name}/SKILL.md` for skill details. See `AGENTS.md` for agent registry.
