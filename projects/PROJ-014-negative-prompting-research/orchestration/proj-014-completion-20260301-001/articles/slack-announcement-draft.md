# Slack Announcement Draft — PROJ-014 Completion

> TASK-029 Phase A | Technical draft (voice transformation in Phase B)
> Source: final-synthesis.md (phase-6), go-no-go-determination.md (ab-testing phase-3-analysis)
> Date: 2026-03-01

---

## Announcement Text

*PROJ-014 shipped: structured negation wins. 270 blind tests. The data is in.*

We completed a six-phase research program on negative prompting in LLM behavioral constraints. The headline result from our A/B experiment: *NPT-013 structured negation* achieved *100% compliance* across all 270 matched tests on three Claude models (haiku, sonnet, opus), while *positive-only framing* showed a *7.8% violation rate* (McNemar exact p=0.016). The effect was unidirectional — structured negation never underperformed positive framing on a single constraint, model, or scenario.

What this means in practice: how you write behavioral constraints in agent files and rules matters. The format `{PRINCIPLE} VIOLATION: NEVER {action} — Consequence: {impact}` reliably outperforms both bare `NEVER` statements and positive-only instruction framing, particularly under high-pressure scenarios and on lower-capability models.

*What changed in the framework:*
- NPT-013 adopted as the canonical constraint format across Jerry Framework
- 12 SKILL.md files upgraded with structured negation routing constraints
- New `/prompt-engineering` interactive skill created — generates NPT-013 constraints on demand
- 14-pattern NPT taxonomy documented (NPT-001 through NPT-014)

*Read more:*
[Jerry Docs Article](TBD) | [Medium Article](TBD)

Try `/prompt-engineering` in your next session to generate NPT-013 constraints for any behavioral rule you're writing.

---

## Word Count

~220 words (within 250-word limit)

## Notes for Phase B Voice Transformation

- Headline is flat — ready for McConkey energy injection
- "The data is in" is a natural hook point
- The 100% vs 92.2% contrast is the sharpest stat — lead with it in voice version
- "How you write constraints matters" is the plain-language translation of the finding
