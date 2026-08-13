# RESUME — GH #377 (grant Bash to adversary critics)

> Read this first after compaction. Updated 2026-08-13.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Where this stands](#where-this-stands) | Current state + the pending decision |
| [The change](#the-change) | What #377 actually does |
| [Verified facts](#verified-facts) | Load-bearing technical facts (do not re-derive) |
| [The plan](#the-plan) | Graph + worktracker decomposition |
| [Next action on resume](#next-action-on-resume) | Exactly what to do next |

## Where this stands

- **GitHub issue:** [#377](https://github.com/geekatron/jerry/issues/377) — "adversary: grant Bash to adv-executor and adv-scorer" (split from parent #344). Owner clarification comment already posted (declining the read-only-critic alternative — it burns main context; keep Write/Edit, add Bash).
- **Branch:** `feat/proj-024-adversary-bash-377`, cut clean from `origin/main`. BUG-010 work confirmed already in `main` (nothing lost).
- **Done:** orchestration plan + Graphviz graph authored (this folder). **Awaiting owner go-ahead to execute**, plus one decision (below).
- **PENDING DECISION (ask owner):** route the mechanical steps N4–N8 (red-test → edit → build → validate → diff) through **one background implementation agent** (recommended — keeps main context for orchestration, per the owner's "prefer background agents" rule) vs. main context. Entity creation (N1) stays main-context per worktracker rules unless owner wants it offloaded.
- **Owner opted into multi-agent orchestration (ultracode / Workflow).** Background agents at full effort. TDD Red/Green/Refactor.

## The change

Add `Bash` to `adv-executor` and `adv-scorer` so a critic can pin a revision (`git show`/`git diff`) and run counts (`grep -c`/`wc -l`). Keep their existing Write/Edit (so they keep persisting their own report files → main context holds only file references).

## Verified facts

- **Source-driven, via the canonical build pipeline — NOT a hand-edit of generated files.** Edit the SOURCE: `skills/adversary/composition/adv-executor.agent.yaml` and `adv-scorer.agent.yaml` (tools under `tools.native`, abstract names) + their `.prompt.md` files.
- Abstract name for `Bash` = **`shell_execute`** (`src/agents/infrastructure/mappings.yaml` maps it to `Bash` for claude_code). Add to `tools.native` in both, keep `file_write`/`file_edit`.
- Rebuild: `uv run jerry agents build` regenerates `skills/adversary/agents/<name>.md` + `<name>.governance.yaml`. Validate: `uv run jerry agents validate`. Drift: `uv run jerry agents diff`.
- **F9 trap (mandatory):** you MUST also update the `<p003_self_check>` "may ONLY use …" sentence in BOTH `.prompt.md` files to include `shell_execute`. If you edit only the YAML, the rebuilt agent self-halts on its first shell command citing a false P-003 violation (build/validate/diff still pass — they check schema/drift, not runtime self-consistency).
- Tiers unchanged: `adv-executor` stays T4, `adv-scorer` stays T2 (Bash is already inside the T2 ceiling).
- Acceptance (from #377): Bash in both generated `tools:` frontmatter; restatements updated in both `.md` bodies + both `.governance.yaml`; executor can `git show "<sha>:<path>"`; scorer can publish a self-derived count.

## The plan

- Full plan: `ORCHESTRATION_PLAN.md` (this folder). Graph: `graph.dot` (rendered `graph.svg`/`graph.png`).
- **13 nodes, failure-gated.** jerry agents doing real work: `eng-security` (N2 capability-grant risk check), `wt-auditor` (N3 entity audit), `adv-executor`/`adv-scorer` (N9/N10 real acceptance probes), `/adversary` adv-selector→executor→scorer (N11 C3 gate ≥0.92), `wt-verifier` (N12 AC verify). Failure edges loop to N5 (max 3 retries); GATE 0 escalates to owner on a genuinely new risk.
- **Criticality C3** (AE-005 security-relevant tool grant) → N11 adversarial gate required.
- **Worktracker (create on execute):** Enabler `EN-011` "Grant Bash to Adversary Critic Agents" under `EPIC-001-schema-validation` → `FEAT-001-claude-code-schema-validation` (sibling to `STORY-011-adversary-tool-access`, the analogous web-tools grant). Tasks `TASK-037`–`TASK-040`, one per #377 acceptance checkbox, all cross-linked to #377.

## Next action on resume

1. Get the owner's go-ahead + the N4–N8 background-agent decision.
2. Create `EN-011` + `TASK-037`–`TASK-040` (worktracker templates, linked #377).
3. Execute the graph via a Workflow (background agents, full effort), gated so a failed node halts its branch. TDD Red/Green/Refactor.
4. On green + adversarial gate ≥0.92 + wt-verifier PASS → push, open PR with `Closes #377`.
