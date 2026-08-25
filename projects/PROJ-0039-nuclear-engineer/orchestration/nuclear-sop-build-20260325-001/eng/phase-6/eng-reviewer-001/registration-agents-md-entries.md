# Registration: AGENTS.md Entries for /nuclear-sop

> **Purpose:** Draft entries for AGENTS.md agent registry.
> **Source:** SKILL.md Available Agents table + governance YAML files.
> **Apply after:** QG-E6 PASS. User splices into `AGENTS.md`.

## AGENTS.md Section

Add this section to `AGENTS.md` under a `/nuclear-sop` heading, maintaining skill alphabetical order:

```markdown
### /nuclear-sop

| Agent | File | Role | Model | Tool Tier |
|-------|------|------|-------|-----------|
| `sop-brief` | `skills/nuclear-sop/agents/sop-brief.md` | Pre-job briefing: context load, prerequisite check, OE history review, error trap identification; optional Step 0 workflow definition generation from natural language | sonnet | T2 |
| `sop-executor` | `skills/nuclear-sop/agents/sop-executor.md` | Step-by-step execution with STAR self-checking (Stop-Think-Act-Review), place-keeping, hold point activation, PROCEDURE_STATE.yaml state management | opus | T2 |
| `sop-verifier` | `skills/nuclear-sop/agents/sop-verifier.md` | Context-isolated independent verification (T1 read-only, fresh context via Task tool); evaluates work products against acceptance criteria for C3+ workflows | sonnet | T1 |
| `sop-capture` | `skills/nuclear-sop/agents/sop-capture.md` | Post-job OE capture with schema-enforced mandatory fields; integrated independent verification for C1-C2 workflows (3-hop mode with anchoring bias disclaimer) | sonnet | T2 |
```
