# GitHub Issue Draft: Agent Definition Optimization

## Title

Slim down agent definitions — 58 agents, 21K lines, time to ski lighter

## Labels

enhancement, infrastructure, quality

## Body

### Current state

58 agent definitions. 21,728 lines of markdown. Average 374 lines per agent. The top 10 individual agents account for 7,468 lines — 34% of all agent markdown. `ts-extractor.md` alone is 1,006 lines. nasa-se has 10 agents averaging 802 lines each — more than double the framework average.

These agents are carrying too much weight. Fat skis are great. Fat agent definitions are not.

Agent definitions load into the context window at Task invocation time. The framework's progressive disclosure architecture (Tier 1/2/3 per `agent-development-standards.md`) specifies that Tier 2 core agent definitions should run 2,000–8,000 tokens. At approximately 10 tokens per line of markdown (varies by content density; Phase 1 will measure actuals), the current 374-line average translates to ~3,700 tokens per agent — in the lower-middle of the Tier 2 range. But the top 10 agents average ~747 lines (~7,500 tokens), approaching the 8,000-token ceiling, and `ts-extractor.md` at 1,006 lines likely exceeds the Tier 2 upper bound at ~10,000 tokens before the agent even starts working. Every token of system prompt is a token unavailable for reasoning. Multiply across a multi-agent workflow and you're spending meaningful context budget before any work begins.

### Data

| Metric | Value |
|--------|-------|
| Total agent `.md` files | 58 |
| Total `.governance.yaml` files | 58 |
| Combined lines (`.md` + `.yaml`) | 26,184 |
| Average `.md` lines per agent | 374 |
| Largest agent (`ts-extractor.md`) | 1,006 lines |
| Top 10 agents by `.md` line count | 7,468 lines (34% of all `.md`) |
| Largest skill (nasa-se, 10 agents) | 8,023 combined lines |

**Per-skill breakdown:**

| Skill | Agents | Combined Lines | Avg Lines/Agent |
|-------|-------:|---------------:|----------------:|
| nasa-se | 10 | 8,023 | 802 |
| problem-solving | 9 | 5,452 | 606 |
| transcript | 5 | 3,175 | 635 |
| worktracker | 3 | 2,006 | 669 |
| red-team | 11 | 1,964 | 179 |
| eng-team | 10 | 1,827 | 183 |
| orchestration | 3 | 1,505 | 502 |
| adversary | 3 | 1,042 | 347 |
| saucer-boy-framework-voice | 3 | 970 | 323 |
| saucer-boy | 1 | 220 | 220 |

**Top 10 largest agents (by `.md` line count):**

| Lines | Agent |
|------:|-------|
| 1,006 | `ts-extractor.md` |
| 963 | `nse-architecture.md` |
| 778 | `nse-reviewer.md` |
| 762 | `nse-reporter.md` |
| 712 | `ps-critic.md` |
| 673 | `wt-verifier.md` |
| 649 | `nse-configuration.md` |
| 647 | `wt-auditor.md` |
| 645 | `nse-explorer.md` |
| 633 | `nse-risk.md` |

At the ~10 tokens/line approximation, an estimated 10–15 agents (those exceeding ~800 lines) likely approach or exceed the 8,000-token Tier 2 ceiling. Phase 1 will measure actual token counts to confirm.

eng-team and red-team prove lean agent definitions work — 10-11 agents each, averaging under 200 lines. Same dual-file architecture (`H-34`), same governance compliance. They just don't repeat themselves.

### Root cause categories

The bloat isn't uniform. Different skills are heavy for different reasons:

**Pattern A: Standards repetition.** Agents restate framework rules already loaded via `.context/rules/` or already declared in `.governance.yaml`. Methodology sections re-derive cognitive mode definitions from `agent-development-standards.md`. Guardrails sections restate constitutional principles beyond the minimum required triplet. This is the most common bloat pattern and the easiest to fix.

**Pattern B: Inline Tier 3 content.** Agents embed rich examples, output templates, and reference tables directly in the Tier 2 definition instead of referencing separate files. This is appropriate for small snippets but not for multi-page methodology walkthroughs.

**Pattern C: Legitimate complexity.** Some agents — particularly nasa-se agents (requirements engineering, V&V, trade studies) and problem-solving agents (multi-source synthesis, root cause analysis) — have genuinely complex multi-step methodologies. Length here reflects the cognitive depth the agent needs. This is NOT bloat and must be preserved.

The optimization targets Pattern A and Pattern B. Pattern C is protected.

**Decision boundary example:** If `nse-architecture.md` reproduces the full cognitive-mode taxonomy table from `agent-development-standards.md`, that's Pattern A — the agent can load the original at runtime. If `nse-architecture.md` describes how to apply V&V principles specifically to architecture review (content not available in any auto-loaded rule file), that's Pattern C — it stays. Most nasa-se and problem-solving agents will be a combination — Pattern A in their guardrails and preamble sections, Pattern C in their methodology core. The Phase 1 audit classifies each section, not just each agent.

### The optimization

Three phases, in order:

**Phase 1: Audit**
- Token budget analysis: measure actual token cost per agent definition (`.md` + `.governance.yaml`), current vs. Tier 2 target (2,000–8,000 tokens per `agent-development-standards.md`)
- H-34 compliance audit: verify `.md` frontmatter contains ONLY the 12 official Claude Code fields, verify `.governance.yaml` completeness, identify any governance content duplicated between the two files
- Categorize each agent's excess by root cause: Pattern A (standards repetition), Pattern B (inline Tier 3), or Pattern C (legitimate complexity)
- **Output:** per-agent optimization targets with specific bloat categories identified, persisted as `work/agent-optimization/phase1-audit.md` (this document is the input gate for Phase 2)

**Phase 2: Optimize**
- Trim Pattern A content: remove restated standards, remove re-derived taxonomies, trim guardrails to minimum + domain-specific additions
- Extract Pattern B content: move inline examples, output templates, and reference tables to `skills/{skill-name}/reference/{agent-name}-reference.md`
- Preserve Pattern C content: do NOT trim legitimately complex methodology
- Strip non-official frontmatter fields from `.md` files
- Work skill-by-skill for reviewability — NOT all 58 in one PR. Suggested sequence: start with already-lean skills (eng-team, red-team) to validate the approach with low risk, then mid-range skills, then repetition-heavy skills (nasa-se, problem-solving) last — highest impact, highest risk

**Phase 3: Validate**
- Behavioral validation protocol for each agent trimmed by >30%:
  - Document the 3 most critical methodology decisions the agent makes
  - Verify those decisions are still present and correctly expressed in the trimmed version
  - For the top-10 largest agents: perform structured before/after comparison
  - For agents trimmed under 30%, the Phase 1 root cause categorization and a self-review confirming Pattern C content is preserved constitute sufficient validation
  - Document validation findings in the PR description. The PR reviewer (not the person who did the trimming) verifies that the documented decisions are correctly preserved — self-attestation alone is insufficient for agents trimmed by >30%
- H-34 compliance verified across all 58 agents
- Progressive disclosure maintained: Tier 1 routing info preserved, Tier 2 core tightened, Tier 3 extracted to reference files
- Full test suite passes — no regressions

**What stays (do not trim):**
- Constitutional compliance guardrails (P-003/P-020/P-022 declarations)
- Agent-specific decision criteria that differentiate this agent from adjacent agents
- Handoff protocol `on_receive`/`on_send` structures used by downstream agents
- All `.governance.yaml` content — this is consolidation, not deletion
- Domain methodology for Pattern C agents — if it teaches the agent how to reason about its domain, it stays

### Reduction targets

Targets differentiated by skill category, not a blanket average:

| Category | Skills | Current Avg | Target Avg | Reduction |
|----------|--------|------------:|----------:|-----------:|
| Repetition-heavy | nasa-se, problem-solving, transcript, worktracker | 600-800 | 300-400 | 40-50% |
| Mid-range | orchestration, adversary, saucer-boy-framework-voice | 300-500 | 200-300 | 25-35% |
| Already lean | eng-team, red-team, saucer-boy | 175-220 | 160-200 | 10-15% |

The eng-team/red-team pattern is the benchmark for lean agents. It is not the blanket target for agents with legitimately complex methodology.

**Hard limits:**
- No agent `.md` exceeds 500 lines (currently: 10 agents exceed this)
- Framework-wide average `.md` lines per agent <= 275 (per-category targets yield ~270 at midpoint; 275 provides a small margin without being aspirationally disconnected from the differentiated targets)

### Acceptance criteria

- [ ] Phase 1 audit artifact produced at `work/agent-optimization/phase1-audit.md`: per-agent token budget report (actual vs. Tier 2 target) and root cause categorization (Pattern A, B, C, or combination for every agent)
- [ ] All 58 agent `.md` files reviewed; Pattern A and B content trimmed or extracted
- [ ] Tier 3 extracted content placed in `skills/{skill-name}/reference/` with naming convention `{agent-name}-reference.md`
- [ ] H-34 compliance verified: `.md` frontmatter audit (12 official fields only), `.governance.yaml` completeness audit
- [ ] Per-category reduction targets met (see table above)
- [ ] No agent `.md` exceeds 500 lines
- [ ] Framework-wide average `.md` lines per agent <= 275
- [ ] Behavioral validation documented in PR description for all agents trimmed by >30% and for all top-10 largest agents; PR reviewer independently verifies
- [ ] All existing tests pass — no regressions
- [ ] Progressive disclosure maintained: Tier 1 (routing) preserved, Tier 2 (core) tightened, Tier 3 (supplementary) extracted to reference files

### Related

- **Worktracker:** Enabler entity (to be created when this issue is filed — agent optimization is technical infrastructure with no direct user feature)
- **Standards:** `agent-development-standards.md` (H-34, Tier 2 size targets, dual-file architecture)
- **Registry:** `AGENTS.md` (full agent index)

### Where to find the agents

Agent definitions live in `skills/*/agents/*.md` with companion governance files at `skills/*/agents/*.governance.yaml`. See `agent-development-standards.md` (`H-34`) for the dual-file architecture specification and `AGENTS.md` for the full registry.

### Why now

The agent corpus has grown organically across 7 projects. Early agents (nasa-se, problem-solving) were authored before the dual-file architecture was standardized and before `agent-development-standards.md` codified Tier 2 size targets. Later agents (eng-team, red-team) were authored to the standard and are lean. The gap between old and new is now measurable and worth closing.

This is infrastructure work that pays compound interest. Every orchestration run, every multi-agent workflow, every quality gate cycle — they all load agent definitions. Smaller definitions mean more room for the actual work.

Powder's not going anywhere. But the lift line gets shorter when you pack lighter.
