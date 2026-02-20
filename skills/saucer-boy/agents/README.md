# Saucer Boy Skill Agents

> Voice quality gate agents for the Saucer Boy persona.

| Agent | File | Role | Model |
|-------|------|------|-------|
| `sb-reviewer` | `sb-reviewer.md` | Voice compliance review (5 Authenticity Tests) | sonnet |
| `sb-rewriter` | `sb-rewriter.md` | Voice transformation (current → Saucer Boy) | sonnet |
| `sb-calibrator` | `sb-calibrator.md` | Voice fidelity scoring (0-1 scale, 5 traits) | sonnet |

**P-003 Compliance:** All agents are workers invoked by the main context. No agent may spawn subagents.

**Reference Files:** Agents load reference files from `../references/` on-demand. See each agent's "Reference File Loading" section for always-load vs on-demand specifications.
