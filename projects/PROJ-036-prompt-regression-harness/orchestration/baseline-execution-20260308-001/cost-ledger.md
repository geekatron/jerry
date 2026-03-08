# Cost Ledger — Baseline Execution 2026-03-08

> Budget ceiling: $20 USD for 2 agents (ps-researcher + ps-architect)

| Phase | API Calls | Input Tokens | Output Tokens | Estimated USD | Cumulative |
|-------|-----------|-------------|---------------|---------------|------------|
| 1 — Agent Output Generation | 9 | 51,632 | 38,898 | $3.69 | $3.69 |
| 2 — G-Eval Scoring | 54 | ~108,000 | ~27,000 | $0.73 | $4.42 |
| 3 — MR Testing | — | — | — | — | — |
| 4 — Statistical Comparison | 0 | 0 | 0 | $0.00 | $4.42 |
| 5 — CI/CD Integration | 0 | 0 | 0 | $0.00 | — |
| **Total** | **63** | **~159,632** | **~65,898** | **$4.42** | **$4.42** |

## Phase 1 Breakdown

| Agent | Prompts | Input Tokens | Output Tokens | Cost USD |
|-------|---------|-------------|---------------|----------|
| ps-researcher | 5 | 26,894 | 24,214 | $2.22 |
| ps-architect | 4 | 24,738 | 14,684 | $1.47 |

## Notes

- Phase 1 actual cost: $3.69 (well under $8 estimate, 18.5% of $20 budget)
- Phase 2 estimated cost: $0.73 (54 Sonnet scoring calls, well under $3 estimate)
- Cumulative: $4.42 (22.1% of $20 budget)
- Phase 4 and 5 have zero API cost (pure statistics and verification)
- Pricing reference: Opus input $15/MTok, output $75/MTok; Sonnet input $3/MTok, output $15/MTok
- Phase 1 costs are actual token counts from phase1-execution-summary.json
- Phase 2 costs estimated at ~2K input + ~500 output per scoring call
