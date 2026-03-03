*PROJ-014 shipped. 270 tests. CONDITIONAL GO.*

NPT-013 hit 100% compliance across haiku, sonnet, and opus. Positive-only framing landed at 92.2%. That gap — 7.8% violation rate, McNemar exact p=0.016 — held across every constraint, every model, every scenario we tested. Structured negation never lost a single matchup.

The format that wins: `{PRINCIPLE} VIOLATION: NEVER {action} — Consequence: {impact}`

It outperforms bare `NEVER` statements and positive framing both — especially under high-pressure scenarios and on lower-capability models, where it matters most.

*What shipped:*
- NPT-013 is now the canonical constraint format across Jerry Framework
- 12 SKILL.md files upgraded with structured negation routing constraints
- New `/prompt-engineering` skill — generates NPT-013 constraints on demand
- 14-pattern NPT taxonomy documented (NPT-001 through NPT-014)

[Jerry Docs Article](../articles/jerry-docs-negative-prompting.md) | [Medium Article](../articles/medium-negative-prompting.md)

Try `/prompt-engineering` in your next session — it generates NPT-013 constraints on demand. The data already made the case.
