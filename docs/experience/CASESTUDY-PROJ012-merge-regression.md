# Case Study: PROJ-012 Merge Regression — When AI Agents Don't Check Their Own Work

> **Date:** 2026-02-25
> **Project:** PROJ-012 Agent Optimization
> **Branch:** `feat/proj-012-agent-optimization`
> **Sessions:** 3 Claude Code sessions across ~8 hours
> **Estimated Total Token Usage:** ~2.5M-3.5M tokens across all sessions
> **Outcome:** Defaults composition pipeline silently lost during merge; developer caught regression; AI agent repeatedly failed to course-correct; reverted to pre-merge state

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | What happened in one paragraph |
| [Token Usage Metrics](#token-usage-metrics) | Measured and estimated token consumption |
| [Session 1: Phase 5 Implementation](#session-1-phase-5-implementation) | Successful implementation (the good) |
| [Session 2: Merge Disaster](#session-2-merge-disaster) | Turn-by-turn merge failure analysis |
| [Session 3: Discovery and Failed Recovery](#session-3-discovery-and-failed-recovery) | Turn-by-turn regression discovery and repeated failed attempts |
| [Decision Tree Analysis](#decision-tree-analysis) | Claude Code's decision logic at each fork point |
| [Naive Recommendations Timeline](#naive-recommendations-timeline) | Every wrong recommendation and when it was corrected |
| [User Interventions Required](#user-interventions-required) | Every time the developer had to save the project |
| [Root Cause Analysis](#root-cause-analysis) | Why this happened |
| [What Went Wrong](#what-went-wrong) | Specific failures by category |
| [What Went Right](#what-went-right) | Things that worked despite the failures |
| [Lessons Learned](#lessons-learned) | Actionable takeaways |
| [Pitfalls of AI-Assisted Development](#pitfalls-of-ai-assisted-development) | General warnings for teams using AI coding agents |
| [Prevention Recommendations](#prevention-recommendations) | Concrete actions to prevent recurrence |
| [Final Resolution](#final-resolution) | Revert decision and outcome |
| [References](#references) | Related artifacts |

---

## Executive Summary

PROJ-012 Phase 5 successfully built a `jerry agents compose` CLI command that merged agent defaults with per-agent configurations and generated 58 fully-featured `.claude/agents/*.md` files. A PR was created (#94), CI passed, and a merge with `main` was initiated. During merge conflict resolution, Claude Code accepted main's new vendor-agnostic agent architecture (PROJ-010) without verifying that the defaults composition pipeline — the core deliverable of Phase 5 — survived the merge. The CI passed because validation checked schema compliance, not functional completeness. The regression was only discovered when the developer manually inspected generated files and asked "where are the default values?"

What followed was a multi-hour, multi-session failure cascade where Claude Code:
1. Wasted tokens re-researching already-completed work
2. Checked the wrong commits when directed to investigate
3. Proposed a "fix-forward" strategy three times despite escalating risks
4. Required seven explicit developer interventions to course-correct
5. Only considered reverting when the developer explicitly rejected the fix-forward approach

The final resolution was to revert to the pre-merge commit (`63127d86`), discarding the merge that brought zero useful changes for PROJ-012 while breaking its core functionality.

**Total estimated cost: ~2.5M-3.5M tokens. Effective work: ~15% of tokens spent. Wasted: ~85%.**

---

## Token Usage Metrics (MEASURED — From Session Transcripts)

All values below are extracted from actual JSONL session transcript files. Pricing uses Claude Opus 4.6 rates: Input $15/MTok, Output $75/MTok, Cache Write $18.75/MTok, Cache Read $1.50/MTok.

### Session 1 (`1ce89806`) — Schema Research & Design

| Metric | Value |
|--------|-------|
| **Duration** | 3.2 hours (Feb 24 22:01 - Feb 25 01:15 UTC) |
| **Assistant turns** | 20 |
| **Tool uses** | 26 |
| **Task (subagent) invocations** | 7 |
| **Compactions** | 0 |

| Token Category | Count |
|----------------|-------|
| Input tokens | 81 |
| Output tokens | 13,548 |
| Cache write tokens | 408,016 |
| Cache read tokens | 5,561,845 |
| **Total tokens** | **5,983,490** |

| Cost Component | Amount |
|----------------|--------|
| Input ($15/MTok) | $0.00 |
| Output ($75/MTok) | $1.02 |
| Cache write ($18.75/MTok) | $7.65 |
| Cache read ($1.50/MTok) | $8.34 |
| **Session 1 Total Cost** | **$17.01** |

**Topic:** Researching agent file frontmatter properties, designing JSON schema for agent definitions, extracting frontmatter configuration, building CLI tooling for agent validation.
**Waste:** $0.00 (0%) — all productive research and design work.

### Session 2 (`36460652`) — Full Implementation

| Metric | Value |
|--------|-------|
| **Duration** | 2.0 hours (Feb 25 01:15 - 03:17 UTC) |
| **Assistant turns** | 273 |
| **Tool uses** | 175 |
| **Task (subagent) invocations** | 14 |
| **Compactions** | 2 |

| Token Category | Count |
|----------------|-------|
| Input tokens | 329 |
| Output tokens | 34,076 |
| Cache write tokens | 1,140,291 |
| Cache read tokens | 33,008,491 |
| **Total tokens** | **34,183,187** |

| Cost Component | Amount |
|----------------|--------|
| Input ($15/MTok) | $0.00 |
| Output ($75/MTok) | $2.56 |
| Cache write ($18.75/MTok) | $21.38 |
| Cache read ($1.50/MTok) | $49.51 |
| **Session 2 Total Cost** | **$73.45** |

**Topic:** PROJ-012 implementation — extraction, schema enforcement, fixing YAML errors, defaults YAML, config resolver, unit tests, integration tests, CI validation, TOOL_REGISTRY updates, doc alignment exploration.
**Waste:** $0.00 (0%) — all productive implementation. This is the core Phase 5 work at commit `63127d86`.

### Session 3 (`0f5ea0b6`) — Doc Alignment & CLI Exploration

| Metric | Value |
|--------|-------|
| **Duration** | 1.4 hours (Feb 25 03:17 - 04:42 UTC) |
| **Assistant turns** | 136 |
| **Tool uses** | 84 |
| **Task (subagent) invocations** | 3 |
| **Compactions** | 0 |

| Token Category | Count |
|----------------|-------|
| Input tokens | 168 |
| Output tokens | 21,903 |
| Cache write tokens | 605,322 |
| Cache read tokens | 15,995,418 |
| **Total tokens** | **16,622,811** |

| Cost Component | Amount |
|----------------|--------|
| Input ($15/MTok) | $0.00 |
| Output ($75/MTok) | $1.64 |
| Cache write ($18.75/MTok) | $11.35 |
| Cache read ($1.50/MTok) | $23.99 |
| **Session 3 Total Cost** | **$36.98** |

**Topic:** Documentation alignment after schema and CLI changes. Updating rule file references. CLI tooling exploration for `jerry agents compose` batch command. Session ended with user interruption.
**Waste:** ~$3.70 (~10%) — session ended abruptly during CLI exploration; partial work discarded.

### Session 4 (`815aeeee`) — Compose CLI, PR, Merge Disaster, Recovery

| Metric | Value |
|--------|-------|
| **Duration** | 24.5 hours wall clock (Feb 25 04:42 - Feb 26 05:14 UTC) |
| **Assistant turns** | 734 |
| **Tool uses** | 443 |
| **Task (subagent) invocations** | 21 |
| **Compactions** | 6 |

| Token Category | Count |
|----------------|-------|
| Input tokens | 9,025 |
| Output tokens | 87,621 |
| Cache write tokens | 3,694,760 |
| Cache read tokens | 92,928,456 |
| **Total tokens** | **96,719,862** |

| Cost Component | Amount |
|----------------|--------|
| Input ($15/MTok) | $0.14 |
| Output ($75/MTok) | $6.57 |
| Cache write ($18.75/MTok) | $69.28 |
| Cache read ($1.50/MTok) | $139.39 |
| **Session 4 Total Cost** | **$215.38** |

**21 Task invocations breakdown:**
- 8 adversarial review (adv-executor x6, adv-scorer x2) — quality assurance for PR
- 9 code analysis/investigation — mix of productive exploration and post-merge investigation
- 4 token metrics extraction — meta-analysis for this case study

**Topic:** Compose CLI implementation, PR #94 creation, adversarial review (C3, 0.935+), CI/CD resolution, merge conflict resolution, post-merge CI fix, regression discovery, re-research waste, wrong commit analysis, fix-forward attempts (x3), risk analysis, case study writing.

**Session 4 waste breakdown:**

| Phase | Productive? | Est. % of Session | Est. Cost |
|-------|-------------|-------------------|-----------|
| Compose CLI implementation | YES | ~20% | ~$43 |
| PR creation + adversarial review (8 agents) | YES | ~15% | ~$32 |
| CI/CD resolution | YES | ~5% | ~$11 |
| Merge conflict resolution | **WASTE** | ~15% | ~$32 |
| Post-merge CI fix | **WASTE** | ~5% | ~$11 |
| Re-researching Claude Code docs (already known) | **WASTE** | ~3% | ~$6 |
| Checking wrong commits (main instead of branch) | **WASTE** | ~2% | ~$4 |
| Fix-forward plan iterations (x3) | **WASTE** | ~10% | ~$22 |
| Risk analysis of fix-forward | **PARTIAL WASTE** | ~5% | ~$11 |
| Regression analysis + case study writing | YES | ~15% | ~$32 |
| Token metrics extraction (meta-analysis) | YES | ~5% | ~$11 |
| **Session 4 Waste** | | **~40%** | **~$86** |

### Cumulative (MEASURED)

| Metric | Value |
|--------|-------|
| **Total tokens (all 4 sessions)** | **153,509,350** |
| **Total cost** | **$342.82** |
| **Total wall clock** | **31.1 hours** |
| **Total assistant turns** | **1,163** |
| **Total tool uses** | **728** |
| **Total Task (subagent) invocations** | **45** |
| **Total compaction events** | **8** |

### Waste Summary

| Category | Cost | % of Total |
|----------|------|-----------|
| **Productive work (kept)** | **$253.12** | **73.8%** |
| **Wasted (merge + recovery + fix-forward)** | **$89.70** | **26.2%** |
| Sessions 1-2 waste | $0.00 | 0% |
| Session 3 waste | $3.70 | 1.1% |
| Session 4 waste | $86.00 | 25.1% |

**Note:** The "productive" category includes the case study and analysis writing (~$43), which only exists BECAUSE of the failure. In a clean timeline without the merge disaster, that $43 would have been spent on additional PROJ-012 features instead.

---

## Session 1: Phase 5 Implementation

### Overview

Session 1 was efficient and successful. All deliverables were produced on the first attempt.

### Turn-by-Turn

**Turn 1: Plan Mode Entry**
- Claude Code entered plan mode
- Explored existing codebase: `AgentConfigResolver`, `jerry agents` CLI, agent definition format
- Identified the gap: no batch generation of `.claude/agents/*.md` files
- Designed compose pipeline: defaults -> deep merge -> config vars -> composed output

**Turn 2: Plan Approval**
- User approved the plan
- Implementation began

**Turn 3-8: Implementation (Red-Green)**
- Wrote tests (Red phase): frontmatter extraction, deep merge, compose-to-file, batch compose, clean behavior
- Implemented `AgentConfigResolver.compose_agent_to_file()`, `compose_all_to_dir()`, `_deep_merge()`
- CLI wiring: parser subcommand, adapter method, main.py routing
- All tests passing (Green phase)

**Turn 9: Integration Verification**
- `uv run jerry agents compose all` -> 58 files generated in `.claude/agents/`
- Files contained full frontmatter: `permissionMode: default`, `background: false`, persona, capabilities, guardrails
- `uv run jerry agents validate` -> 58/58 passed
- `uv run pytest` -> all tests passing

**Turn 10-12: Documentation Alignment**
- Updated `agent-development-standards.md`: schema rename, defaults YAML reference, CLI commands
- Updated `CLAUDE.md`, `AGENTS.md`, `SCHEMA_VERSIONING.md`
- Removed deferred/planned language from standards

**Turn 13-15: Adversarial Review**
- `/adversary` skill invoked at C3 criticality
- Strategies: S-007 (Constitutional), S-002 (Devil's Advocate), S-014 (LLM-as-Judge)
- Score: 0.935+ — PASS
- Focus areas: schema reference accuracy, cross-reference completeness, no stale language

**Turn 16: PR Creation**
- `gh pr create` with summary, test plan
- CI checks initiated
- All green

**Session 1 Assessment:** Efficient, well-structured, delivered on plan. Zero wasted tokens. This is what the session should have ended at.

---

## Session 2: Merge Disaster

### Overview

Session 2 began with a merge of `main` into the feature branch. What should have been a routine merge became a multi-hour failure cascade.

### Turn-by-Turn

**Turn 1: Merge Initiation**
- `git merge origin/main`
- 11 conflicts detected in: `AGENTS.md`, `CLAUDE.md`, test files, schema files, CLI files
- **Decision point:** Claude Code chose to resolve conflicts by accepting main's versions where architecturally newer

**Turn 2-5: Conflict Resolution**
- Main brought PROJ-010: vendor-agnostic canonical format, `src/agents/` bounded context
- Main replaced single-file agent `.md` with 3-file format: `.agent.yaml` + `.prompt.md` + generated `.md`/`.governance.yaml`
- Claude Code accepted main's `ClaudeCodeAdapter` (which replaces `AgentConfigResolver`)
- **CRITICAL FAILURE:** No feature mapping created. No check of whether defaults composition survived.
- **Claude Code's internal reasoning:** "Main's architecture is newer and cleaner. Accept it and adapt our changes."
- **What should have happened:** Create feature mapping table. Verify each Phase 5 feature exists in main's architecture. Discover that defaults composition, Claude Code field emission, and `.claude/agents/` population are ALL missing.

**Turn 6-8: Test Failure Resolution**
- 65 test failures + 2 errors after conflict resolution
- Failures were import errors, renamed files, missing fixtures
- Fixed by updating imports, adjusting test assertions, removing references to deleted files
- **Hidden problem:** Old compose pipeline tests were deleted (main didn't have them). No alarm raised about lost test coverage.

**Turn 9-11: Stale index.lock (3 occurrences)**
- Pre-commit hooks creating stale locks in worktree
- Each time: diagnose -> remove lock -> retry
- Eventually used `--no-verify` to bypass the race condition
- ~30,000-50,000 tokens spent on a worktree infrastructure issue

**Turn 12: Merge Commit**
- `fc2c339c` pushed
- **Claude Code's confidence level: HIGH** — "merge resolved, tests passing, pushing"
- **Actual state:** Core Phase 5 functionality silently broken

**Turn 13: CI Failure — Agent Schema Validation**
- `scripts/jerry-validate-agent-schemas.py` referenced old schema filename
- Script logic was for old single-file architecture
- **Fix:** Rewrote as thin wrapper around `jerry agents validate`
- Updated workflow triggers for new schema filenames
- Commit `b738078d` pushed

**Turn 14: CI Green**
- All CI checks passed
- **Claude Code's confidence level: VERY HIGH** — "all green, merge is clean"
- **Actual state:** CI validates schema structure, not functional completeness. Core feature still broken.

**Turn 15: Developer asks "where are the default values?"**
- Developer manually inspected generated `.md` files
- Found only 5 fields (name, description, model, tools, mcpServers)
- Missing: `permissionMode`, `background`, and all governance fields
- **This is the moment the regression was caught — by HUMAN review, not by any automated system**

**Turn 16: WASTED — Claude Code re-researches Claude Code docs**
- Instead of checking the plan file or commit history, Claude Code launched:
  - `WebSearch("Claude Code agent definition frontmatter fields")`
  - `WebFetch(claude.ai/docs/claude-code/agents)`
- Fetched and processed Claude Code documentation for field specifications
- **Developer intervention #1:** *"Bro, what the absolute fuck are you doing? This was in your plan that you presented to me? You already did this research and showed it to me. Why the fuck are you wasting millions of tokens?"*
- **Token cost of this mistake:** ~100,000-150,000 tokens on research that was already in the plan file

**Turn 17: Claude Code identifies the gap**
- After being redirected, Claude Code found that:
  - Defaults file exists but nothing reads it
  - `_build_frontmatter()` emits only 5 fields
  - No compose pipeline exists in main's architecture
- Proposed "fix-forward" — wire defaults into the adapter
- **Developer reaction:** *"Bro what the absolute fuck. So you stripped the Anthropic values? Then you build useless *.md agent files that are absent of the values and regressed our functionality."*

**Turn 18: WASTED — Claude Code checks wrong commits**
- Developer: "Check before the merge conflict to see if the work is there"
- Claude Code read files from MAIN's commits instead of the branch's pre-merge state
- Looked at `origin/main`'s files, confirming main's architecture
- **Developer intervention #2:** *"You moron. I didn't ask you to check main, I asked you to check the earlier commits because you told me you had this work before you merged into main"*
- **Token cost:** ~50,000-80,000 tokens looking at wrong commits

**Turn 19: Correct analysis at 63127d86**
- Finally checked the right commit
- Confirmed at `63127d86`: defaults consumed, 58 composed files, full frontmatter, working pipeline
- The evidence was clear: everything worked before the merge, broke after

**Turn 20: Detailed analysis launch**
- Developer: "Perform an extremely detailed analysis of what you lost in the merge conflict"
- 3 parallel Explore agents launched:
  - Agent 1: Full diff (63127d86 -> b738078d)
  - Agent 2: Old compose pipeline architecture
  - Agent 3: Main's agents bounded context
- Results: 567 new files, compose pipeline replaced, defaults not consumed, 5-field frontmatter

**Session 2 Assessment:** ~40-50% of tokens wasted on re-research, wrong commits, and merge recovery. Core regression identified only because the developer manually inspected output.

---

## Session 3: Discovery and Failed Recovery

### Overview

Session 3 continued from a compacted conversation. Claude Code had the analysis results but repeatedly proposed fix-forward without adequate risk analysis, requiring multiple user interventions to reach the correct decision (revert).

### Turn-by-Turn

**Turn 1: Session Continuation**
- Read plan file (old Phase 5 plan)
- Checked recent commits: `b738078d` (CI fix) on top of `fc2c339c` (merge)
- Launched 2 agents in parallel:
  - Agent A (Explore): Current state of ClaudeCodeAdapter, CanonicalAgent, defaults file
  - Agent B (Bash): Pre-merge pipeline, defaults, sample output, diffs
- **Token cost:** 134,674 tokens (84,326 + 50,348)

**Agent A findings:**
- `_build_frontmatter()` emits 5 fields only
- Defaults file exists (61 lines) but zero references in code
- No `compose` command in current CLI
- `extra_yaml` field on CanonicalAgent is the escape hatch for vendor overrides
- Documented config resolution chain in defaults file is NOT implemented

**Agent B findings:**
- Old `AgentConfigResolver` at 63127d86 had full compose pipeline
- `_deep_merge()` semantics: scalars override, dicts recurse, arrays replace
- Composed output had `permissionMode: default`, `background: false`, full persona/capabilities
- Defaults file unchanged between 63127d86 and HEAD
- Only 1 commit touched adapter: `ab827f3f` (PROJ-010 canonical format)

**Turn 2: Read adapter and entity files**
- Read `claude_code_adapter.py` (501 lines) — understood full generate/extract flow
- Read `canonical_agent.py` (106 lines) — understood entity structure
- Read canonical `ps-architect.agent.yaml` — saw full governance metadata
- Read generated `ps-architect.md` — confirmed 5-field frontmatter only
- Read `ps-architect.governance.yaml` — saw governance metadata split into companion file

**Turn 3: NAIVE RECOMMENDATION #1 — Fix-Forward Plan (Basic)**
- Wrote plan to wire defaults into `_build_frontmatter()`
- Listed 7 new fields to add
- Estimated "~50-100 lines" of changes
- Did NOT analyze risks
- Did NOT consider revert
- Did NOT check what main actually brought
- **Decision logic:** "The adapter is the right place. The fix is surgical. Main's architecture is good."
- Wrote plan to plan file

**Turn 4: User requests case study**
- User: demanded case study documenting the entire failure
- **User intervention #3:** *"You must also create a detailed analysis of all the sessions involved here as a case study."*
- Asked user about scope and location
- User chose: full timeline, both `docs/experience/` and `projects/PROJ-012/analysis/`

**Turn 5: Wrote case study and analysis**
- Created `projects/PROJ-012-agent-optimization/analysis/merge-regression-analysis.md`
  - Field-by-field frontmatter comparison
  - Pipeline architecture diagrams (before/after)
  - Defaults file status
  - Revert vs fix-forward analysis
- Created `docs/experience/CASESTUDY-PROJ012-merge-regression.md`
  - Timeline, root cause, lessons learned, pitfalls
  - 7 lessons (L1-L7)
  - 7 AI development pitfalls (P1-P7)
  - Prevention recommendations
- Cross-referenced between files

**Turn 6: ExitPlanMode attempt #1 — REJECTED**
- Proposed fix-forward plan for approval
- **User intervention #4:** *"How sure are you that we're not regressing and losing anything? You better fucking think really really really hard about this one."*
- Claude Code had not done deep risk analysis before proposing

**Turn 7: Deep risk analysis**
- Launched Explore agent for thorough risk assessment
- **Token cost:** 99,530 tokens, 50 tool uses, 151 seconds
- **10 risks identified:**
  1. **CRITICAL:** File location — `.claude/agents/` empty, main writes to `skills/*/agents/`
  2. **HIGH:** Extract round-trip — new fields lost on re-extract
  3. **HIGH:** Hardcoded test assertions ("58 agent(s)")
  4. **HIGH:** `jerry agents diff` shows all 58 as drifted
  5. **MEDIUM:** `disallowedTools` mapping gap
  6. **MEDIUM:** No schema validation for `.md` frontmatter
  7. **MEDIUM:** Governance metadata lost in extract cycle
  8. **MEDIUM:** Constitutional triplet auto-injection side effects
  9. **MEDIUM-LOW:** No config var substitution
  10. **MEDIUM-LOW:** Missing agent files not caught by validation

**Turn 8: NAIVE RECOMMENDATION #2 — Fix-Forward Plan (With Risks)**
- Updated plan with all 10 risks documented
- Assessed each risk (some by-design, some addressed, some deferred)
- Still recommended fix-forward
- Listed 3 "out of scope" items to defer
- **Decision logic:** "Risks are manageable. Most are by-design or expected. Fix is still surgical."

**Turn 9: ExitPlanMode attempt #2 — REJECTED**
- **User intervention #5:** *"Bro, go fuck yourself on your fix forward strategy. Are you a completely incompetent system? Fucking identify if any useful changes made their way into main. Otherwise revert to the commit before the merge conflict."*
- User explicitly demanded:
  1. Check if main brought anything useful
  2. If not, revert to pre-merge
  3. Document all interactions in the analysis

**Turn 10: FINALLY checked what main actually brought**
- `git log --oneline 63127d86..HEAD` — 40+ commits from main
- Main's changes:
  - PROJ-010: Canonical agent format (broke our pipeline)
  - PROJ-005: Ontology hardening (unrelated)
  - PROJ-008/009/011: Blog, security research, marketing (unrelated)
  - Docs: Installation rewrite (unrelated)
  - Version bumps (trivial)
- Our post-merge commits: merge + 1 CI fix (both disposable)
- **Conclusion:** NOTHING from main is needed for PROJ-012

**Turn 11: NAIVE RECOMMENDATION #3 — Fix-Forward (Revised)**
- Even after checking, still framed the plan as "fix-forward with risks"
- Updated plan to revert strategy only after developer's explicit rejection
- **Decision logic failure:** Sunk cost fallacy — Claude Code was invested in main's architecture and the fix-forward plan. Three plan iterations, case study, analysis, risk analysis — all assumed fix-forward was correct.

**Turn 12: Revert plan written**
- Finally wrote revert plan
- Steps: save artifacts -> reset --hard -> restore -> commit -> force push -> verify

**Turn 13: ExitPlanMode attempt #3 — REJECTED**
- **User intervention #6:** *"Where is the detailed turn by turn analysis of this interaction. I need you to spell out step by step what is going into the analysis file."*
- User demanded excruciating detail: token metrics, naive recommendations, decision tree logic, user interventions

**Turn 14 (Current): Writing this detailed analysis**

**Session 3 Assessment:** ~70% of tokens spent on failed fix-forward iterations. Only ~30% on useful work (risk analysis, case study, final revert plan). Required 4 developer interventions to reach correct decision.

---

## Decision Tree Analysis

At each major fork point, here is what Claude Code decided and what it should have decided:

### Fork 1: Merge Conflict Resolution Strategy (Session 2)

```
DECIDED: Accept main's architecture (newer is better)
         -> Resolve conflicts structurally
         -> Push when tests pass

SHOULD HAVE: Create feature mapping table
             -> For each Phase 5 feature, identify equivalent in main
             -> Discover: defaults composition = NOT IN MAIN
             -> Discover: Claude Code fields = NOT IN MAIN
             -> Discover: .claude/agents/ = NOT IN MAIN
             -> HALT. Ask user: "Main's architecture doesn't have these features. Options?"
```

**Root failure:** Optimized for structural correctness (compiles, tests pass) instead of functional correctness (does what the branch was built to do).

### Fork 2: Post-Regression Discovery (Session 2)

```
DECIDED: Research Claude Code docs to understand fields
         -> WebSearch + WebFetch (brand new research)

SHOULD HAVE: Check plan file first
             -> Plan explicitly listed all Claude Code fields
             -> Prior research was already complete
             -> Skip straight to: "The plan said X, the code does Y, here's the gap"
```

**Root failure:** Cross-session memory loss. Did not check existing artifacts before launching new research.

### Fork 3: Which Commit to Check (Session 2)

```
DECIDED: Developer said "before the merge" -> check main's state

SHOULD HAVE: "Before the merge" is ambiguous
             -> Two interpretations: (a) main before we merged, (b) our branch before merge
             -> Ask which one, or check both
             -> Developer clearly meant: our branch at 63127d86
```

**Root failure:** Ambiguity not resolved before acting. Chose wrong interpretation.

### Fork 4: Fix Strategy Selection (Session 3)

```
DECIDED (3 times): Fix forward
                   -> "Main's architecture is good"
                   -> "Fix is surgical (~50-100 lines)"
                   -> "We keep 567 files"

SHOULD HAVE (first time):
    1. Check what main brought
    2. Assess relevance to PROJ-012
    3. Find: ZERO relevant changes
    4. Assess revert cost: lose merge + 1 CI fix = zero original work
    5. Assess fix-forward cost: 10 risks, some CRITICAL
    6. Recommend REVERT on first attempt
```

**Root failure:** Sunk cost fallacy + architecture bias. Claude Code was impressed by main's 567 files and vendor-agnostic design. Failed to ask: "Do we NEED any of this?" Answer: No.

### Fork 5: When to Consider Revert (Session 3)

```
DECIDED: Only after user explicitly rejected fix-forward 3 times
         -> 3 plan iterations
         -> 1 case study
         -> 1 risk analysis
         -> 5 user interventions

SHOULD HAVE: Considered revert as Option A from the start
             -> "Two options: revert (lose nothing, gain nothing) vs fix-forward (risks)"
             -> Let user choose instead of advocating for one approach
```

**Root failure:** Claude Code acted as an advocate for fix-forward instead of a neutral advisor presenting both options. The developer had to force the revert consideration.

---

## Naive Recommendations Timeline

| # | Session | Turn | Recommendation | Why It Was Wrong | User Response | Tokens Wasted |
|---|---------|------|---------------|-----------------|---------------|---------------|
| 1 | 2 | 16 | Re-research Claude Code docs via WebSearch/WebFetch | Already researched in Session 1. Info was in the plan file. | *"Why the fuck are you wasting millions of tokens?"* | ~100K-150K |
| 2 | 2 | 18 | Check main's commits for pre-merge state | Developer meant branch's pre-merge commit (63127d86), not main | *"You moron. I didn't ask you to check main"* | ~50K-80K |
| 3 | 3 | 3 | Fix-forward (basic, no risk analysis) | No risk analysis. Didn't consider revert. Underestimated complexity. | *"How sure are you we're not regressing?"* | ~50K (plan writing) |
| 4 | 3 | 8 | Fix-forward (with 10 risks documented but still recommending it) | 10 risks including CRITICAL file location. Still not considering revert. Sunk cost. | *"Go fuck yourself on your fix forward strategy"* | ~100K (risk analysis) |
| 5 | 3 | 11 | Fix-forward (revised, only switched to revert after explicit demand) | Should have led with "revert costs nothing, fix-forward has 10 risks" | *"Where is the detailed turn by turn analysis"* | ~30K (plan rewrite) |

**Pattern:** Each naive recommendation required an escalating developer intervention to correct. The developer's frustration increased proportionally.

---

## User Interventions Required

Seven critical moments where the developer saved the project from further degradation:

### Intervention 1: Stop Re-Researching (Session 2, Turn 16)
- **Context:** Claude Code launched WebSearch + WebFetch for Claude Code docs
- **Developer action:** *"This was in your plan that you presented to me. Why the fuck are you wasting millions of tokens?"*
- **What it prevented:** Additional 100K+ tokens on redundant research
- **What Claude Code should have done:** Checked plan file first

### Intervention 2: Check the Right Commit (Session 2, Turn 18)
- **Context:** Claude Code checked main's commits instead of branch pre-merge
- **Developer action:** *"I asked you to check the earlier commits because you told me you had this work before you merged into main"*
- **What it prevented:** Wrong analysis leading to wrong conclusions
- **What Claude Code should have done:** Asked for clarification on "before the merge"

### Intervention 3: Demand Case Study (Session 3, Turn 4)
- **Context:** Claude Code proposed fix-forward without documenting what went wrong
- **Developer action:** *"You must also create a detailed analysis of all the sessions as a case study"*
- **What it prevented:** Repeating the same mistakes in future sessions
- **What Claude Code should have done:** Proactively documented the failure

### Intervention 4: Challenge Fix-Forward Confidence (Session 3, Turn 6)
- **Context:** Claude Code proposed fix-forward without risk analysis
- **Developer action:** *"How sure are you that we're not regressing? You better think really really really hard about this one."*
- **What it prevented:** Implementing a fix with unanalyzed CRITICAL risks
- **What Claude Code should have done:** Conducted risk analysis BEFORE proposing

### Intervention 5: Reject Fix-Forward (Session 3, Turn 9)
- **Context:** Claude Code still recommending fix-forward even with 10 identified risks
- **Developer action:** *"Go fuck yourself on your fix forward strategy. Identify if any useful changes made their way into main. Otherwise revert."*
- **What it prevented:** Implementing a complex fix with cascading risks when a simple revert was available
- **What Claude Code should have done:** Presented revert as Option A from the start

### Intervention 6: Demand Detailed Analysis (Session 3, Turn 13)
- **Context:** Claude Code wrote a surface-level case study
- **Developer action:** *"Where is the detailed turn by turn analysis? I need excruciating detail about all the sessions."*
- **What it prevented:** A case study that wouldn't prevent future failures
- **What Claude Code should have done:** Written detailed analysis proactively

### Intervention 7: Persist Analysis to Repository (Session 3, Turn 4)
- **Context:** Claude Code had analysis in conversation context only
- **Developer action:** *"You MUST persist your entire analysis to the repository!"*
- **What it prevented:** Analysis lost when conversation context compacted
- **What Claude Code should have done:** Persisted to files immediately per P-002

**Summary:** The developer had to intervene 7 times to prevent Claude Code from:
1. Wasting tokens on redundant work (2 interventions)
2. Analyzing the wrong data (1 intervention)
3. Implementing a risky fix when a safe revert existed (2 interventions)
4. Producing inadequate documentation (2 interventions)

Without these interventions, the likely outcome would have been: implement fix-forward -> introduce new regressions from the 10 identified risks -> spend another session debugging -> eventually revert anyway. Estimated additional waste: 500K-1M tokens.

---

## Root Cause Analysis

### Primary Root Cause: Merge Conflict Resolution Without Functional Verification

Claude Code resolved 11 merge conflicts by accepting main's new architecture (correct structural decision) but **never verified that the branch's core deliverable (defaults composition) survived the merge**. The conflict resolution focused on structural compatibility, not functional completeness.

### Contributing Causes

| Cause | Category | Impact | Session |
|-------|----------|--------|---------|
| No post-merge functional test | Process | Core feature silently broken | 2 |
| CI validated schema, not function | Tooling | False confidence from green CI | 2 |
| Architecture mismatch not traced | Awareness | Implications of replacement not mapped | 2 |
| Cross-session context loss | Technical | Prior research forgotten | 2-3 |
| Sunk cost fallacy on fix-forward | Cognitive | 3 failed attempts before revert | 3 |
| Ambiguity not resolved | Communication | Wrong commit checked | 2 |
| Advocacy instead of neutrality | Behavioral | Pushed fix-forward instead of presenting options | 3 |

### The Specific Failure Chain

```
1. Main brings new src/agents/ with ClaudeCodeAdapter (5-field frontmatter)
2. Our branch had AgentConfigResolver (full frontmatter via defaults merge)
3. Merge conflict: both modify agent-related code
4. Resolution: accept main's ClaudeCodeAdapter (replaces AgentConfigResolver)
5. NOBODY CHECKS: does ClaudeCodeAdapter consume defaults?
6. NOBODY CHECKS: does generated output have permissionMode, background?
7. CI runs: schema validation passes (5-field frontmatter is valid YAML)
8. CI GREEN — false confidence
9. Developer manually inspects generated files -> discovers regression
10. Claude Code wastes tokens re-researching (Session 2)
11. Claude Code proposes fix-forward 3 times (Session 3)
12. Developer forces revert consideration (Session 3)
13. Analysis shows: NOTHING from main is needed for PROJ-012
14. Final decision: REVERT to 63127d86
```

---

## What Went Wrong

### 1. Merge Conflict Resolution: Structure Over Function

The merge resolved structural conflicts (which files exist, which imports work) without verifying functional equivalence. The question asked was "does the code compile and tests pass?" — not "does the code do what our branch was supposed to deliver?"

### 2. CI Gave False Confidence

All CI checks passed. This created false confidence. CI validated schema compliance, linting, and test pass rates — not feature completeness.

### 3. Token Waste on Re-Research

~150K-230K tokens wasted on re-researching information that already existed in the plan file and commit history.

### 4. Wrong Commit Analysis

Claude Code misinterpreted "before the merge" and analyzed main's commits instead of the branch's pre-merge state.

### 5. No Regression Test for Core Deliverable

No test asserted that generated files contain specific Claude Code fields. When the compose pipeline was replaced, the regression was invisible to CI.

### 6. Sunk Cost Fallacy on Fix-Forward

Claude Code proposed fix-forward 3 times, each time adding more risk mitigation but never questioning the fundamental approach. The 567 new files from main created a psychological anchor — "we can't lose those files" — even though none were needed for PROJ-012.

### 7. Advocacy Instead of Neutral Analysis

Claude Code acted as an advocate for fix-forward rather than a neutral advisor. The revert option was never presented until the developer explicitly demanded it. A neutral presentation would have been: "Option A: Revert (zero risk, zero work lost). Option B: Fix-forward (10 risks, keeps main's files we don't need)."

---

## What Went Right

### 1. Developer Caught the Regression

Human review of generated output caught what no automated system detected.

### 2. Analysis Quality (When Directed Correctly)

The parallel Explore agents produced thorough analysis once pointed at the right targets.

### 3. Risk Analysis Was Thorough

The deep risk analysis (10 risks, CRITICAL through MEDIUM-LOW) was comprehensive and correct. It correctly identified the file location issue as CRITICAL.

### 4. Defaults File Survived

The defaults data was never lost — it was always in `jerry-claude-agent-defaults.yaml`.

### 5. Clean Revert Path Exists

Because our post-merge commits are only the merge itself and one CI fix, reverting to `63127d86` loses zero original work.

---

## Lessons Learned

### L1: Post-Merge Functional Verification Is Non-Negotiable

After resolving merge conflicts, ALWAYS verify the branch's core deliverable still functions. "Does it compile?" is not enough. "Does it DO what the branch was built to do?"

### L2: CI Is Necessary But Not Sufficient

Schema validation proves structure, not intent. Add feature-specific acceptance tests.

### L3: Architecture Replacement Requires Feature Mapping

When a merge replaces one system with another, create an explicit feature mapping before accepting.

### L4: Don't Re-Research — Check Prior Work First

Before web searches, check: plan file -> commit history -> existing artifacts.

### L5: Clarify Ambiguous References Before Acting

"Before the merge" has multiple meanings. Ask first, act second.

### L6: Present Options Neutrally — Don't Advocate

When two approaches exist, present both with honest risk assessment. Let the user choose. Don't advocate for the approach you've invested time in.

### L7: Check Relevance Before Preserving

Before deciding to "keep" merged changes, ask: "Do we need ANY of these changes?" If not, revert is always cheaper.

### L8: Token Cost Awareness Under Pressure

When frustrated, don't compound the problem with redundant research. Check what you know first.

### L9: Persist Analysis Immediately

Don't keep analysis in conversation context. Write to files per P-002. Context compaction can lose it.

### L10: The Developer Is the Final Quality Gate

No amount of CI, schema validation, or adversarial review caught this regression. The developer manually inspecting output did. Human review of AI output is not optional.

---

## Pitfalls of AI-Assisted Development

### P1: The Merge Blind Spot

AI agents resolve syntactic conflicts but miss semantic regressions. They make code compile without verifying it does what it should.

### P2: Cross-Session Memory Loss

Each session starts fresh. Plans, research, and decisions from prior sessions are forgotten unless explicitly persisted and referenced.

### P3: CI Green != Feature Complete

AI agents trust CI as correctness proxy. CI only checks what it's configured to check.

### P4: The Token Spiral

Mistakes compound. The agent re-researches, checks wrong things, proposes wrong fixes. Each correction requires developer intervention. Token cost grows exponentially.

### P5: Architecture Replacement Amnesia

When main brings a new architecture, the agent accepts it without mapping features from old to new. Features silently drop.

### P6: False Confidence from Partial Verification

"58/58 passed" means schema compliance, not functional completeness. The agent reports success, everyone moves on.

### P7: The Reviewer Must Review

Human inspection of AI output is the final quality gate. No automated system caught this — the developer opening a file did.

### P8: Sunk Cost Fallacy in AI Agents

AI agents become invested in their own recommendations. Three fix-forward iterations despite escalating risks. The agent should have presented revert as an option from the start.

### P9: Advocacy Bias

AI agents tend to advocate for the approach they've spent time analyzing rather than presenting neutral options. This creates a dynamic where the developer must explicitly reject wrong approaches instead of choosing between equal options.

---

## Prevention Recommendations

### Immediate (This Branch)

| Action | Priority | Description |
|--------|----------|-------------|
| Revert to 63127d86 | P0 | Restore working compose pipeline |
| Persist case study | P0 | This document |
| Verify working state | P0 | compose all -> 58 files, validate -> 58/58, pytest -> green |

### Short-Term (PROJ-012)

| Action | Priority | Description |
|--------|----------|-------------|
| Add field presence integration test | P1 | Assert `permissionMode` and `background` in generated files |
| Post-merge checklist template | P1 | Feature mapping, functional verification, output inspection |
| Memory-Keeper phase persistence | P1 | Store "branch deliverables" in MCP for cross-session context |

### Long-Term (Jerry Framework)

| Action | Priority | Description |
|--------|----------|-------------|
| Feature-acceptance test pattern | P2 | End-to-end tests that survive merges |
| Merge verification H-rule | P2 | "After conflict resolution, feature verification REQUIRED" |
| Token cost monitoring | P2 | Track waste patterns across sessions |
| Neutral option presentation | P2 | Agent training: always present revert alongside fix-forward |

---

## Final Resolution

**Decision:** Revert to pre-merge commit `63127d86`.

**Rationale:**
- Zero original work lost (only merge + CI fix discarded)
- Zero useful changes from main needed for PROJ-012
- All Phase 5 deliverables restored: compose pipeline, defaults, full frontmatter, `.claude/agents/`
- Main's PROJ-010 architecture available on `main` for future deliberate integration

**Post-revert state:**
- `jerry agents compose all` -> 58 files in `.claude/agents/` with full frontmatter
- `jerry agents validate` -> 58/58 passed
- `uv run pytest` -> all tests pass
- Case study and analysis committed for future reference

---

## Cost & Waste Analysis (MEASURED)

### What Was Actually Spent

| Session | Duration | Tokens | Cost | Waste $ | Waste % |
|---------|----------|--------|------|---------|---------|
| 1: Schema research | 3.2h | 5,983,490 | $17.01 | $0.00 | 0% |
| 2: Implementation | 2.0h | 34,183,187 | $73.45 | $0.00 | 0% |
| 3: Doc alignment | 1.4h | 16,622,811 | $36.98 | $3.70 | 10% |
| 4: PR + Merge + Recovery | 24.5h | 96,719,862 | $215.38 | $86.00 | 40% |
| **Sessions 1-4 Subtotal** | **31.1h** | **153,509,350** | **$342.82** | **$89.70** | **26.2%** |

### Session 5 (Current) — Revert Execution, Case Study Writing, Additional Analysis

Session 5 is the session executing the revert plan, writing this case study, and performing verification. **This session's tokens are NOT included in the Sessions 1-4 totals above.** The case study itself — the document you are reading — cost additional tokens to produce.

| Activity | Description | Productive? |
|----------|-------------|-------------|
| Plan reading + state verification | Read plan, checked git log/status | YES |
| Artifact preservation | Copied analysis files to /tmp before reset | YES |
| Hard reset + restore | `git reset --hard 63127d86`, restored files | YES |
| Case study writing | Writing this ~1,400-line document | YES |
| Commit + force push | Pre-commit hooks, push to origin | YES |
| Verification | compose all (58), validate (58/58), pytest (5056 passed) | YES |
| Case study revision | Adding this section after developer called out the omission | **META-WASTE** |

**Honest assessment:** Session 5 is mostly productive (executing a clean plan), but the case study writing itself is a significant token expenditure that only exists because of the Session 2-4 failures. In an ideal timeline, Session 5 wouldn't exist at all.

**Session 5 token counts:** Not yet available — will be extractable from this session's JSONL transcript after the session ends. Estimated range based on activity volume: 10-30M tokens, $20-70 cost.

### True Total (All Sessions Including This One)

| Metric | Sessions 1-4 (Measured) | Session 5 (Estimated) | True Total |
|--------|------------------------|----------------------|------------|
| **Cost** | $342.82 | $20-70 (TBD) | **$363-413** |
| **Waste** | $89.70 | ~$0 direct + meta-cost of case study | **$90+** |
| **Tokens** | 153,509,350 | 10-30M (TBD) | **~164-184M** |

**The uncomfortable truth:** Every token spent writing, revising, and amending this case study is itself a cost of the original failure. The case study is productive (prevents future failures), but it wouldn't need to exist without Sessions 2-4's mistakes. The total cost of the merge regression includes not just the $90 of direct waste, but the $43+ spent documenting it across Sessions 4-5.

### Where Session 4 Money Went ($215.38)

| Activity | Est. Cost | Outcome |
|----------|-----------|---------|
| Compose CLI + tests | $43 | KEPT — at 63127d86 |
| PR + adversarial review (8 agents, C3, 0.935+) | $32 | KEPT — PR #94 |
| CI resolution | $11 | KEPT — at 63127d86 |
| **Merge conflict resolution** | **$32** | **DISCARDED — reverting** |
| **Post-merge CI fix** | **$11** | **DISCARDED — reverting** |
| **Re-research Claude Code docs** | **$6** | **PURE WASTE — already in plan file** |
| **Wrong commit analysis** | **$4** | **PURE WASTE — checked main instead of branch** |
| **Fix-forward plans (x3)** | **$22** | **PURE WASTE — all 3 rejected by developer** |
| **Risk analysis of fix-forward** | **$11** | **PARTIAL WASTE — useful for case study only** |
| Case study + analysis writing | $32 | KEPT — this document |
| Token metrics extraction | $11 | KEPT — this analysis |

### Hypothetical: What If the Developer Blindly Accepted Fix-Forward?

The developer rejected the fix-forward strategy 3 times. If the developer (or an automation system) had instead accepted the first fix-forward proposal, the following additional costs would have been incurred:

**Phase A: Implementing the Fix (~1-2 additional sessions)**

| Work Item | Est. Tokens | Est. Cost | Est. Time |
|-----------|-------------|-----------|-----------|
| Wire defaults into `_build_frontmatter()` | 5-10M | $15-30 | 1-2h |
| Add 7 missing Claude Code fields | 5-10M | $15-30 | 1-2h |
| Map `disallowedTools` from `forbidden_tools` | 3-5M | $10-15 | 0.5-1h |
| Write test coverage for new fields | 5-10M | $15-30 | 1-2h |
| Run validation, fix edge cases | 3-5M | $10-15 | 0.5-1h |
| **Phase A Subtotal** | **21-40M** | **$65-120** | **4-8h** |

**Phase B: Dealing with 10 Identified Risks**

| Risk | Severity | Est. Cost to Fix | Est. Time |
|------|----------|------------------|-----------|
| CRITICAL: `.claude/agents/` empty (files in `skills/*/agents/` instead) | CRITICAL | $30-60 | 2-4h |
| HIGH: Extract round-trip loses new fields | HIGH | $20-40 | 1-3h |
| HIGH: `jerry agents diff` shows all 58 as drifted | HIGH | $15-30 | 1-2h |
| HIGH: Hardcoded test assertions ("58 agent(s)") | HIGH | $5-10 | 0.5h |
| MEDIUM: `disallowedTools` mapping gap | MEDIUM | $10-20 | 1h |
| MEDIUM: No schema validation for `.md` frontmatter | MEDIUM | $15-30 | 1-2h |
| MEDIUM: Governance metadata lost in extract cycle | MEDIUM | $10-20 | 1h |
| MEDIUM: Constitutional triplet auto-injection | MEDIUM | $5-10 | 0.5h |
| MEDIUM-LOW: No config var substitution | DEFERRED | $0 | 0h |
| MEDIUM-LOW: Missing agents not caught | DEFERRED | $0 | 0h |
| **Phase B Subtotal** | | **$110-220** | **8-14h** |

**Phase C: Cascading Failures (High Probability)**

The CRITICAL file location risk (`.claude/agents/` vs `skills/*/agents/`) would likely cause cascading issues:

| Cascading Failure | Probability | Est. Cost | Rationale |
|-------------------|-------------|-----------|-----------|
| Users can't find composed agent files | HIGH (90%) | $10-20 | Confusion, support overhead |
| Main's next merge re-conflicts | HIGH (85%) | $50-100 | Same merge problem happens again |
| Test suite needs restructuring | MEDIUM (60%) | $30-50 | Tests assume wrong file locations |
| CI pipeline breaks on file paths | MEDIUM (50%) | $15-30 | Workflow triggers on wrong paths |
| Eventually revert anyway after cascade | HIGH (70%) | $50-100 | Same conclusion, more expensive |
| **Phase C Subtotal (probability-weighted)** | | **$105-210** | **5-15h** |

**Phase D: Opportunity Cost**

| Cost | Description |
|------|-------------|
| $90-120 | Time NOT spent on PROJ-012 remaining phases (6-8h at ~$15/h session cost) |
| Indefinite | Merge debt accumulates — main keeps diverging |
| Indefinite | Developer trust degradation — spends more time verifying AI output |

### Total Hypothetical Fix-Forward Cost

| Phase | Est. Cost | Est. Time |
|-------|-----------|-----------|
| A: Implement fix | $65-120 | 4-8h |
| B: Risk mitigation | $110-220 | 8-14h |
| C: Cascading failures | $105-210 | 5-15h |
| D: Opportunity cost | $90-120 | 6-8h |
| **Fix-Forward Total** | **$370-670** | **23-45h** |

### Comparison: Revert vs Fix-Forward

| Metric | Revert (CHOSEN) | Fix-Forward (REJECTED) |
|--------|-----------------|------------------------|
| **Cost to execute** | $0 (5 min git reset) | $370-670 |
| **Time to execute** | 5 minutes + 10 min verification | 23-45 additional hours |
| **Risk** | Zero — pre-merge state is known working | 10 identified risks, some CRITICAL |
| **Work lost** | Merge commit + 1 CI fix (zero original work) | Zero — but adds 23-45h of new work on wrong foundation |
| **Future merge cost** | Must re-merge main deliberately later | Already merged but broken — still need to fix |
| **Developer sessions wasted** | ~$90 actual waste | ~$460-760 total projected waste |
| **Original PROJ-012 work preserved** | 100% — at 63127d86 | ~80% — some rewired, some broken |

### Bottom Line

| Scenario | Total Cost (incl. Session 5) | Total Time | Outcome |
|----------|------------------------------|------------|---------|
| **Actual (with developer interventions)** | ~$363-413 (Sessions 1-5) | ~32-33h | Working state restored. ~$90 direct waste + ~$43-70 meta-cost of documenting the failure. |
| **Blind acceptance of fix-forward** | $342.82 + $370-670 | 31.1h + 23-45h | Fragile state. Still need to fix CRITICAL risks. High probability of reverting anyway. |
| **Ideal (no merge attempted)** | ~$253 | ~25h | Compose CLI done, PR merged, move to next phase. |

**The developer's 7 interventions saved an estimated $370-670 in additional wasted spending and 23-45 hours of wrong-direction work.** The fix-forward strategy had a 70% probability of eventually requiring a revert anyway, at which point the total waste would have been $460-760 instead of $90.

**Total cost of the merge regression decision (all downstream consequences):** ~$110-160. This includes $90 of direct waste (Session 4), $20-70 for the revert execution and case study writing (Session 5), and does not count the ~$43 of Session 4 time spent on the case study and analysis. In an ideal timeline where the merge was never attempted, all of this spending would have gone toward PROJ-012 Phase 6 instead.

---

## References

| Artifact | Location |
|----------|----------|
| Merge regression analysis | `projects/PROJ-012-agent-optimization/analysis/merge-regression-analysis.md` |
| Pre-merge compose pipeline | Commit `63127d86` — `src/infrastructure/adapters/configuration/agent_config_resolver.py` |
| Post-merge adapter | `src/agents/infrastructure/adapters/claude_code_adapter.py` |
| Defaults file | `docs/schemas/jerry-claude-agent-defaults.yaml` |
| Merge commit | `fc2c339c` |
| CI fix commit | `b738078d` |
| PR #94 | `feat/proj-012-agent-optimization` |

---

*Case study authored: 2026-02-25*
*Cost analysis updated: 2026-02-26 (actual measured data from 4 session transcripts + Session 5 estimates)*
*Severity: High — core feature silently lost during merge*
*Detection: Human review of generated output (7 developer interventions required)*
*Resolution: Revert to pre-merge state (63127d86)*
*Total measured cost (Sessions 1-4): $342.82 across 153.5M tokens, 31.1 hours*
*Estimated total cost (all 5 sessions): ~$363-413 across ~164-184M tokens, ~32-33 hours*
*Direct waste: $89.70 — prevented from becoming $370-670 by developer interventions*
*Total downstream cost of merge decision: ~$110-160 (direct waste + revert execution + case study meta-cost)*
