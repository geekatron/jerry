# Mandatory Skill Usage

> Proactive skill invocation rules. DO NOT wait for user to invoke.

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
| H-22 | MUST invoke `/problem-solving` for research/analysis. MUST invoke `/nasa-se` for requirements/design. MUST invoke `/orchestration` for multi-phase workflows. | Work quality degradation. Rework required. |

---

## Trigger Map

| Detected Keywords | Skill |
|-------------------|-------|
| research, analyze, investigate, explore, root cause, why | `/problem-solving` |
| requirements, specification, V&V, technical review, risk | `/nasa-se` |
| orchestration, pipeline, workflow, multi-agent, phases, gates | `/orchestration` |

---

## Behavior Rules

1. DO NOT WAIT for user to invoke skills -- use proactively when triggers apply.
2. COMBINE skills when appropriate (e.g., /orchestration + /problem-solving + /nasa-se).
3. INVOKE EARLY at start of work, not after struggling without them.
4. PERSIST all skill outputs to the repository.
5. See `skills/{name}/SKILL.md` for skill details. See `AGENTS.md` for agent registry.
