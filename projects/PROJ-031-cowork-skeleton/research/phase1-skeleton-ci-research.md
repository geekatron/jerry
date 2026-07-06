# Phase 1 Research — Derived Skeleton Branch + CI Regeneration + CoWork Plugin Install

> **PS ID:** cowork-skeleton-20260626-001 (Phase 1) · **Entry:** ps-researcher-001 · **Project:** PROJ-031-cowork-skeleton
> **Date:** 2026-06-26 · **Agent:** jerry:ps-researcher · **Criticality:** C4 (quality target >= 0.95)
> **Scope:** Four research questions feeding `nse-requirements` (requirements.md) and `ps-architect` (ADR-PROJ031-001 skeleton strategy, ADR-PROJ031-002 token strategy).
> **Settled facts (not re-investigated):** strip `projects/` -> 1,744 tracked files; CI trigger = push of `v*` tag; docs auto-publish via `docs.yml` -> `gh-pages`; `marketplace.json` `source: "./"` is branch-relative; install = marketplace/branch ref (clone of tracked files; `.venv` not counted).

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language answer + recommendation per question |
| [Methodology and Source Credibility](#methodology-and-source-credibility) | What was searched, Context7 status, source tiers |
| [L1: Technical Analysis](#l1-technical-analysis) | Per-question findings with evidence |
| [Q1: Skeleton Generation Technique](#q1-skeleton-generation-technique) | rm+force-push vs orphan vs filter-repo/subtree |
| [Q2: GitHub Actions Patterns](#q2-github-actions-patterns) | Trigger, checkout, identity, token, loop-safety, branch protection, notification |
| [Q3: Claude Code Plugin Install from a Branch](#q3-claude-code-plugin-install-from-a-branch) | Add syntax, manifest locations, structure constraints |
| [Q4: Failure Modes When projects/ Is Absent](#q4-failure-modes-when-projects-is-absent) | CLI, SessionStart hook, H-04 bootstrap, stub mitigation |
| [L2: Architectural Implications](#l2-architectural-implications) | Cross-cutting trade-offs, risks, ADR inputs |
| [Recommendations Summary](#recommendations-summary) | One-line recommendation per question |
| [Open Questions and Gaps](#open-questions-and-gaps) | Honest unknowns for downstream phases |
| [References](#references) | Cited sources |

---

## L0: Executive Summary

We need to ship Jerry as a Claude CoWork plugin, but the repo is too big (6,344 tracked files vs CoWork's ~5,000 limit). The fix is a **derived `cowork-skeleton` branch** that is `main` with the `projects/` folder removed (dropping to 1,744 files) plus a tiny `projects/` placeholder so Jerry still boots. CI rebuilds this branch on every release. This research answers four questions about how to do that safely.

**Q1 — How to generate the stripped branch?** Recommend **checkout the release tag, `git rm -r projects/`, add a stub, commit, and force-push to `cowork-skeleton`** (the approach already chosen in the plan). It mirrors how Jerry already maintains its `gh-pages` docs branch by force-push, it preserves a clear link back to the exact released version, and re-running it on the same tag produces the same result. The history-rewriting alternatives (git-filter-repo, subtree split) are the wrong tool: they scrub `projects/` from *every past commit*, are slow, and are designed for one-time surgery, not repeatable per-release regeneration. We only need `projects/` gone from the *tip* of the branch that users clone — not from history.

**Q2 — How to run it safely in GitHub Actions?** Recommend the **default `GITHUB_TOKEN` with `permissions: contents: write`** (not a Personal Access Token). Counter-intuitively this is *both* safer and sufficient: a `GITHUB_TOKEN` auto-expires, is scoped to this repo, and — by GitHub design — a push it makes **cannot re-trigger any workflow**, which gives us free loop-safety. This is the opposite of Jerry's `version-bump.yml`, which *needs* a PAT precisely because it *wants* its tag push to trigger `release.yml`. The skeleton must trigger nothing, so `GITHUB_TOKEN` is the right call. Trigger on `push: tags: ['v*']` + `workflow_dispatch`, SHA-pin actions, add a `concurrency` group, keep `cowork-skeleton` unprotected (like `gh-pages`), and emit a job-summary + `if: failure()` notification.

**Q3 — How do users install it?** They add the marketplace pinned to the branch: **`/plugin marketplace add geekatron/jerry@cowork-skeleton`**. Both manifests already live in the right place (`.claude-plugin/marketplace.json` and `.claude-plugin/plugin.json` at repo root), and `source: "./"` is valid. Two critical constraints from Anthropic's docs: (a) because `source: "./"` is a *relative path*, users **must** add via the Git repo (the `owner/repo@ref` form), **not** via a raw `marketplace.json` URL — relative paths do not resolve in URL-based marketplaces; (b) install **clones the whole branch tree and copies it to a cache**, so the file count that matters is exactly the branch's tracked tree — which is what stripping `projects/` reduces. Notably, **Anthropic's public plugin docs do not document any ~5,000-file limit** — that limit is a CoWork/Claude-Desktop runtime constraint per the project's settled facts and still warrants empirical confirmation (recon R-001).

**Q4 — What breaks when `projects/` is gone?** The load-bearing finding: **Git cannot commit an empty directory**, so the stub's `README.md` is not just guidance — it is the file that makes `projects/` *exist* on a fresh clone. With it present, `jerry projects list` returns an empty list cleanly and the SessionStart hook still emits `<project-required/>` to prompt first-project creation (H-04 bootstrap works). **Without** any `projects/` directory, `jerry projects list` raises an uncaught `RepositoryError` ("Projects directory does not exist"). The minimal stub (`projects/` + `README.md`) mitigates every runtime dependency we found.

---

## Methodology and Source Credibility

**Frameworks applied:** 5W1H source survey; source-tier credibility weighting; direct code-grounding for repo-specific claims (Q2 alignment, Q4 failure modes).

**Context7 status (MCP-001 compliance):** Per MCP-001, Context7 is the required source for named tools/frameworks (Claude Code, GitHub Actions, git). **Context7 MCP tools were unavailable in this execution environment** (`mcp__context7__resolve-library-id` and `mcp__context7__query-docs` both returned "No such tool available"). Per the MCP error-handling standard ("Context7 returns no results / unavailable -> fall back to WebSearch; note the gap"), I fell back to **primary-source web documentation** (official Anthropic Claude Code docs and official GitHub Docs) plus the repository itself. This is disclosed for P-022 honesty; it does not lower confidence for Q2/Q3/Q4 because the substitute sources are themselves primary (vendor docs + first-party code).

**Source tiers used:**

| Tier | Source | Used for |
|------|--------|----------|
| PRIMARY (HIGH) | Anthropic Claude Code docs — "Create and distribute a plugin marketplace" | Q3 install syntax, manifest paths, structure constraints |
| PRIMARY (HIGH) | GitHub Docs — `GITHUB_TOKEN`, "Triggering a workflow" | Q2 recursion/loop-safety, token behavior |
| PRIMARY (HIGH) | Repo source files (workflows, hooks, CLI handlers, adapters) | Q2 alignment, Q4 grounded failure modes |
| PRIMARY (HIGH) | Canonical git documentation (git-scm) + git-filter-repo project | Q1 tool semantics (established git behavior) |
| SECONDARY/LOW (corroborating) | Community discussions + practitioner blogs | Q2 cross-checks only; never sole basis for a claim |

**Confidence:** Q2 HIGH, Q3 HIGH, Q4 HIGH (code-grounded), Q1 HIGH (established git semantics + existing `gh-pages` precedent).

---

## L1: Technical Analysis

### Q1: Skeleton Generation Technique

**Goal:** deterministically produce a branch = `main` minus `projects/` (plus stub), suitable for CI regeneration that users install from.

**Decisive framing:** A plugin install **clones the branch and materializes its working tree at the tip commit** (`.venv`, `site/`, `__pycache__` are gitignored and absent; history is not part of the checked-out tree). Therefore the only thing that affects the installed file count is **the tree at the branch tip** — not whether `projects/` ever existed in history. This single fact eliminates the history-rewriting options.

**Option comparison:**

| Criterion | (a) checkout tag + `git rm -r projects/` + stub + commit + force-push | (b) Orphan branch rebuilt each release | (c) git-filter-repo / `git subtree split` |
|-----------|------------------------------------------------------------------------|----------------------------------------|--------------------------------------------|
| Determinism (tree) | Deterministic: tree = f(source tree − `projects/` + fixed stub) | Deterministic (same tree) | Deterministic tree but full-history rewrite |
| Idempotency (commit SHA) | Idempotent *if* parent=source-tag-commit, fixed message (embeds source SHA), pinned author/committer dates | Idempotent if dates/message pinned | **Non-idempotent**: rewritten SHAs differ every run |
| Derived-branch history size | = `main`'s history + 1 commit (replaced wholesale via force-push; no accumulation) | **O(1)** — single squashed commit (lightest clone) | New rewritten history of comparable length; expensive to compute |
| Force-push safety | Safe — CI-owned branch, regenerated wholesale (mirrors `gh-pages`) | Safe (same) | Safe but pointless overhead |
| Simplicity | **High** — 4 plain git commands; no extra tooling | Medium — `git checkout --orphan` + clean staging | **Low** — extra dependency, slow on a 6,344-file repo, easy to misuse |
| Provenance to released version | **Strong** — parent chains to the exact `v*` tag commit; `git log`/diff-against-main work | Weak — provenance only via commit message | Weak — rewritten SHAs break traceability |
| Plugin-install compatibility | Full (tip tree correct) | Full (tip tree correct) | Full but over-engineered |

**Why (c) is the wrong tool (steelman then reject):** `git-filter-repo` and `git subtree split` are legitimately excellent when the requirement is *"`projects/` must never have existed in any commit a cloner can reach"* — e.g., purging secrets or extracting a sub-library with its own history. If CoWork did a *full-depth* clone and counted *historical* objects, filter-repo would matter. **But** the installed artifact is the **tip working tree**, and `subtree split` does the *inverse* of our need (it keeps one subdirectory; we want everything *except* one). filter-repo rewrites all history (slow, SHA-non-idempotent, one-time-surgery-oriented). Both fail the idempotency and simplicity criteria for a per-release regeneration job.

**Recommended: (a)**, refined for an idempotency proof ADR-PROJ031-001 can cite:
1. **Build from the triggering `v*` tag**, not a moving `main`. The `v*` tag points at the bump commit on `main` (per `version-bump.yml` → `release.yml`), so the tag's tree *is* the released `main` content, frozen. This makes the skeleton reproducible for that exact release and removes any race with `main` advancing mid-run.
2. **Deterministic commit metadata:** fixed message embedding the source tag + 40-char source SHA; set `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` to the source commit's dates. Result: re-running the job on the same tag yields a **bit-identical commit SHA** (true idempotency). Tree determinism is automatic (`git rm` + fixed stub).
3. **Force-push** `cowork-skeleton` (CI-owned, regenerated wholesale) — directly analogous to `mkdocs gh-deploy --force` in `docs.yml`.
4. **Lighter-history fallback:** if clone weight ever becomes a problem (relevant to Q3's 120s git-operation timeout and recon R-002 blobs), switch to **(b) orphan** for O(1) history, accepting the loss of provenance/diff-to-main. Recommend (a) as default; gate (b) behind a documented trade-off in ADR-PROJ031-001.

> **Correction to a stated plan rationale (for nse-requirements):** the design note "checkout `main` with full history for accurate `git ls-files`" is inaccurate — `git ls-files` reads the index/working tree and needs **no history**. `fetch-depth: 1` is sufficient for the strip + file-count assertion. `fetch-depth: 0` is required **only if** you choose to *preserve `main`'s full history* in the skeleton (approach (a) with a real parent chain). This distinction belongs in ADR-PROJ031-001/ADR-PROJ031-002.

---

### Q2: GitHub Actions Patterns

All recommendations are aligned with Jerry's three proven workflows (`release.yml`, `version-bump.yml`, `docs.yml`), read this session.

**Trigger.** `on: push: tags: ['v*']` + `workflow_dispatch`. This is exactly `release.yml`'s trigger (proven live: tags `v0.31.0`…`v0.31.5`). The skeleton pushes a **branch** (`cowork-skeleton`), which is not a tag, so it cannot re-fire any tag-keyed workflow. `version-bump.yml` and `docs.yml` listen on **`main` only** → unaffected.

**Checkout.** SHA-pin `actions/checkout` to the same pin the repo already standardizes on (`actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2`). Use `ref: ${{ github.ref }}` (the triggering tag). `fetch-depth: 1` suffices for strip + `git ls-files` count; use `fetch-depth: 0` only if preserving full history (see Q1). `actions/checkout` defaults to `fetch-depth: 1` (shallow) [GitHub Docs].

**Git identity.** Reuse the established bot identity from `docs.yml`/`version-bump.yml`:
`git config user.name github-actions[bot]` / `git config user.email 41898282+github-actions[bot]@users.noreply.github.com`.

**Token — recommend `GITHUB_TOKEN` with `permissions: contents: write` (NOT a PAT).** Rationale, with the recursion question answered explicitly:
- **`GITHUB_TOKEN` can push branches** under `contents: write` (this is what `docs.yml` does for `gh-pages`).
- **`GITHUB_TOKEN`-pushed commits do NOT re-trigger workflows.** GitHub states: *"events triggered by the `GITHUB_TOKEN`, with the exception of `workflow_dispatch` and `repository_dispatch`, will not create a new workflow run"* — an intentional recursion guard [GitHub Docs: GITHUB_TOKEN; Triggering a workflow]. For the skeleton this is a **feature**: defense-in-depth loop-safety *in addition to* the branch-vs-tag trigger design.
- **Least privilege / R-004 mitigation:** `GITHUB_TOKEN` is repo-scoped and auto-expires at job end — no long-lived secret to exfiltrate. A PAT (like `VERSION_BUMP_PAT`) carries broader, persistent scope and is the exact asset recon R-004 / Risk R-004 warn about.
- **Contrast with `version-bump.yml`:** that workflow *must* use `VERSION_BUMP_PAT` because it *wants* its pushed tag to trigger `release.yml` (a `GITHUB_TOKEN` push would not). The skeleton has the **opposite** requirement (trigger nothing), so the PAT's only differentiating capability is unwanted here.

**Avoiding recursion (summary):** three independent guarantees — (1) trigger is tag-only, skeleton output is a branch; (2) `main`-listening workflows ignore the branch; (3) `GITHUB_TOKEN` pushes can't re-trigger at all. Add a `concurrency:` group (e.g., `group: cowork-skeleton`, `cancel-in-progress: false`) to serialize overlapping releases, mirroring `version-bump.yml`'s `concurrency: version-bump`.

**Branch-protection interaction (security-relevant, AE-005).** `GITHUB_TOKEN` **cannot push to a *protected* branch** that forbids force-push, and force-push to a protected branch requires either a ruleset **bypass actor** (grant the "Write"/Actions role bypass) or a **GitHub App token** [practitioner sources, corroborating]. **Recommendation: keep `cowork-skeleton` unprotected**, exactly like `gh-pages` — it is a disposable, CI-regenerated derivative, never a development target. If org policy mandates protection, add a ruleset that (a) allows force-push and (b) lists the GitHub Actions actor as the sole bypass. Document either way in `branch-protection-config.md` (Phase 6). For supply-chain integrity (R-007), optionally require the build's CI status to pass before the branch is advertised as installable.

**Failure notification.** Mirror the existing job-summary pattern: a `Job summary` step writing to `$GITHUB_STEP_SUMMARY` with `if: always()` (as in `version-bump.yml`), plus an `if: failure()` step for an explicit failure surface (optional Slack/webhook). No `pat-monitor.yml`-style expiry monitoring is needed because `GITHUB_TOKEN` has no expiry to track — a secondary benefit of dropping the PAT.

**Supply-chain hardening (carry into Phase 2/6):** SHA-pin every action (the repo already does this consistently); minimal `permissions:` block; `concurrency` guard; consider build-provenance/attestation parity with `release.yml` if the skeleton is treated as a released artifact.

---

### Q3: Claude Code Plugin Install from a Branch

Grounded in Anthropic's official "Create and distribute a plugin marketplace" documentation.

**How users add the marketplace pinned to the branch:**
- GitHub shorthand with `@ref`: **`/plugin marketplace add geekatron/jerry@cowork-skeleton`** (interactive) or **`claude plugin marketplace add geekatron/jerry@cowork-skeleton`** (CLI). Docs: *"To pin to a branch or tag, append `@ref` to the GitHub shorthand or `#ref` to a git URL."*
- Then install the plugin: **`/plugin install jerry@jerry-framework`** (`plugin-name@marketplace-name`, where `jerry-framework` is the marketplace `name` from `marketplace.json`).
- **Marketplace source supports `ref` (branch/tag) but NOT `sha`** (only *plugin* sources support `sha`). So pinning the *marketplace* to `cowork-skeleton` is by branch ref — exactly the model here.

**Where the manifests must live in the installed ref (both already correct in Jerry):**
- `marketplace.json` → **`.claude-plugin/marketplace.json` at the repo root** (the marketplace root = the directory containing `.claude-plugin/`). Confirmed present and version-synced (`jerry-framework` v1.0.0).
- `plugin.json` → **`.claude-plugin/plugin.json`** in the plugin root. Jerry's plugin uses **`source: "./"`**, so the plugin root *is* the repo root → `.claude-plugin/plugin.json` at root. Valid. A relative-path `source` *must start with `./`* and resolves against the marketplace root.
- **`projects/` removal does not touch `.claude-plugin/`, `skills/`, `commands/`, `.claude/`, `.context/`, `hooks/`, `schemas/`** — so the entire declared plugin surface (88 agents, skills tree, 2 commands) survives the strip. (Cross-check: `ci.yml` plugin-validation already enforces `plugin.json` agent-path integrity; stripping only `projects/` keeps it green.)

**Documented structure constraints that matter here:**
1. **Relative-path sources require Git-based marketplace add.** *"Relative paths only work when users add your marketplace via Git… If users add your marketplace via a direct URL to the `marketplace.json` file, relative paths will not resolve correctly."* Since Jerry is `source: "./"`, the install docs (Phase 4 tutorial) **must** instruct the `geekatron/jerry@cowork-skeleton` (Git) form and **must not** suggest a raw-URL marketplace add.
2. **Install clones the whole repo and copies it to a cache.** *"When users install a plugin, Claude Code copies the plugin directory to a cache location"* (`~/.claude/plugins/cache`), and *"Git-based marketplaces clone the entire repository."* For `source: "./"` the "plugin directory" is the entire branch tree → the **branch's tracked tree is exactly what is cloned and cached**. This validates the whole strategy: shrinking the branch tree (strip `projects/`) directly shrinks what CoWork materializes.
3. **No documented file-count or repo-size limit.** The Anthropic marketplace docs specify **no** maximum file count or repository size for plugins/marketplaces. The **~5,000-file CoWork limit is not stated in public Claude Code plugin docs** — it is a CoWork/Claude-Desktop runtime constraint per the project's settled facts. **P-022 gap:** this confirms recon Open-Question 1 / Risk R-001 remains *empirically* unverified by vendor documentation; requirements should keep the "reproduce the limit on a clean clone" verification step.
4. **120-second git-operation timeout.** *"Claude Code uses a 120-second timeout for all git operations"* (override via `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`). A large branch can time out on slow networks — a clone-weight argument for stripping `projects/` (and, optionally, the two ~908 KB transcript blobs per recon R-002) and a candidate troubleshooting note for the how-to doc.
5. **Version/update model fits per-release regeneration.** Version resolves as `plugin.json.version` → marketplace-entry `version` → commit SHA. Jerry **pins** `plugin.json.version` (synced by `bump-my-version`), so users receive an update only when the version string changes — i.e., **once per release**, which is exactly when CI regenerates the skeleton. No change needed; document it in the reference doc.

> **Context7 note:** the above is sourced from Anthropic's official docs (primary). Context7 ("Claude Code") was unavailable this session; no third-party Context7 library entry was consulted. Treat vendor docs as authoritative.

---

### Q4: Failure Modes When projects/ Is Absent

Grounded by reading the SessionStart hook, its CLI handler, the project-scan adapter, the `projects list` CLI path, and bootstrap path resolution.

**Runtime dependencies on `projects/` and how the minimal stub (`projects/` + `README.md`) mitigates each:**

| Consumer | Behavior if `projects/` is **entirely absent** | Behavior with **stub** (`projects/` exists, only `README.md` inside) | Mitigation verdict |
|----------|------------------------------------------------|----------------------------------------------------------------------|--------------------|
| **`jerry projects list`** (`cmd_projects_list` → `ScanProjectsQueryHandler` → `FilesystemProjectAdapter.scan_projects`) | **Uncaught `RepositoryError`**: `scan_projects` raises *"Projects directory does not exist"* when the dir is missing (adapter lines 52–53); the scan handler does **not** catch it → error/stack trace, non-zero path. | `scan_projects` iterates an empty dir, returns `[]`; CLI prints *"No projects found. / Total: 0 project(s)"* and exits 0. `README.md` is a **file**, so it is skipped (`if not item.is_dir(): continue`) and never mistaken for a project. | **Mitigated.** Stub turns a hard failure into a clean empty list. |
| **SessionStart hook** (`HooksSessionStartHandler` → `RetrieveProjectContextQuery`) | Resilient **either way**: the retrieve handler wraps the scan in `try/except RepositoryError: pass` (lines 119–121), and the hook step is itself fail-open. With `JERRY_PROJECT` unset it still emits `<project-context>…<project-required/>`. | Same `<project-required/>` emission, and the directory now physically exists for the "create your first project" flow to write into. | **Mitigated / already resilient.** Stub additionally guarantees a writable target for first-project creation. |
| **H-04 bootstrap (active-project requirement)** | On a fresh install `JERRY_PROJECT` is unset → hook emits `<project-required/>` → per `project-workflow.md` the agent uses AskUserQuestion to select/create a project. Without a `projects/` dir, the create-new flow has no parent directory and the next-number/`projects/README.md` guidance is missing. | Stub `README.md` provides the bootstrap explanation + H-04 guidance and a real `projects/` parent; user creates `PROJ-001-…`, sets `JERRY_PROJECT`, proceeds. `next_number` computes to 1 from an empty scan. | **Mitigated.** H-04 is satisfiable out of the box. |
| **WORKTRACKER.md injection** (`_read_worktracker`) | Returns `None` when `JERRY_PROJECT` unset (fresh install) — no failure. | Same; activates correctly once a project is created. | No issue. |
| **`get_projects_directory()` / bootstrap wiring** | Returns a path string; does not check existence. Only fails when a *consumer* (e.g., `scan_projects`) hits the missing dir. | Path exists; consumers succeed. | Mitigated via the consumers above. |

**The load-bearing insight (must be explicit in the stub spec / ADR-PROJ031-001):** **Git does not track empty directories.** A bare `mkdir projects/` will **not** survive a clone — so a plugin install would arrive with **no `projects/` directory at all**, re-triggering the `jerry projects list` `RepositoryError`. The stub's **`projects/README.md` is the sentinel file that forces `projects/` to materialize on a fresh clone.** Its content (bootstrap explanation, link to the main repo, H-04 first-project guidance) is secondary to its structural necessity. **Requirement for nse-requirements:** the stub MUST contain at least one tracked file inside `projects/`.

**Non-dependencies (confirmed safe):** `ci.yml` plugin-validation, `marketplace.json`/`plugin.json` integrity, and the symlinks `.claude/rules → ../.context/rules` / `.claude/patterns → ../.context/patterns` do **not** reference `projects/`; stripping it leaves all of them intact (recon §5; `.context/` is retained).

---

## L2: Architectural Implications

**1. The skeleton is a third CI-owned derived branch — and Jerry already operates this pattern twice.** `gh-pages` (force-pushed by `docs.yml`) and the tag-driven `release.yml` artifact flow are both precedents. `cowork-skeleton` is `gh-pages`'s structural sibling: disposable, regenerated, force-pushed, unprotected. Adopting the *same* operational conventions (force-push, bot identity, `concurrency`, SHA-pinned actions) minimizes novel risk and reviewer surface for the C4 gate.

**2. Token choice is the central security trade-off (ADR-PROJ031-002).** The analysis collapses to: *"Do we need the skeleton push to trigger anything? No."* → therefore `GITHUB_TOKEN` dominates a PAT on every axis (least privilege, no expiry to monitor, built-in recursion immunity, smaller blast radius for R-004). A PAT would only be justified if a downstream workflow had to fire on the skeleton branch — which the design explicitly forbids for loop-safety. ADR-PROJ031-002 should record the PAT option as **considered and rejected**, with the `version-bump.yml` PAT contrast as the illustrative counter-case.

**3. Loop-safety is over-determined, which is good for a C4 irreversibility argument.** Three independent mechanisms (tag-only trigger; `main`-only listeners; `GITHUB_TOKEN` non-retrigger) each individually prevent the infinite-push loop in Risk R-005. The Phase 6 "formal loop-safety argument" can therefore be stated as a conjunction of three documented invariants rather than a single assertion.

**4. Provenance vs clone-weight is the one genuine design tension (ADR-PROJ031-001).** Approach (a) gives strong provenance (parent chains to the released tag) at the cost of carrying `main`'s history weight into `.git`; orphan (b) gives O(1) history at the cost of provenance. Because (i) install copies the **working tree** (history weight affects only clone bandwidth, not installed file count) and (ii) the 120s git timeout is the real clone-weight risk, the recommendation is **(a) by default, (b) as a documented escape hatch** if real-world clones approach the timeout. This is a clean, testable ADR decision.

**5. The unverified ~5,000-file limit is the project's top residual risk (R-001), and vendor docs do not resolve it.** Q3 confirms Anthropic's plugin docs impose no documented file-count limit; the constraint is CoWork-specific and, per recon, *believed* to count the tracked/clone tree (hypothesis (a), HIGH but unverified). The entire solution's validity rests on this. **Strong recommendation:** nse-requirements must keep an explicit acceptance test — *reproduce the limit error on a clean clone vs a dev checkout* — before Phase 5 implementation. If CoWork instead counts a local working dir (`.venv` = 24,636 files), the strategy pivots to local-plugin configuration guidance, not branch stripping.

**6. Install-path documentation is a correctness requirement, not polish.** Because `source: "./"` is a relative path, the *only* supported install path is the Git `owner/repo@ref` form; a raw-URL marketplace add will silently fail to resolve the plugin. The Phase 4 tutorial/how-to must encode this precisely (and the troubleshooting how-to should name the 120s timeout + `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` and the relative-path-vs-URL pitfall).

**7. Forward evolution.** If clone weight or the 5,000-limit margin tightens later, the same CI job can additionally strip non-product test fixtures (`skills/transcript/test_data/` two ~908 KB blobs, `tests/`, `docs/archive/`) behind a flag (recon R-002) — but none of that is needed for the file-count goal today (1,744 ≪ 5,000).

---

## Recommendations Summary

| Q | Recommendation (one line) | Confidence |
|---|---------------------------|------------|
| **Q1** | **Checkout the `v*` tag → `git rm -r projects/` → inject stub → deterministic commit (parent=tag, pinned dates, SHA in message) → force-push `cowork-skeleton`.** Reject filter-repo/subtree (wrong tool: history rewrite, non-idempotent). Orphan = documented lighter-history fallback. | HIGH |
| **Q2** | **`GITHUB_TOKEN` + `permissions: contents: write`** (not a PAT); trigger `push: tags: ['v*']` + `workflow_dispatch`; SHA-pinned `actions/checkout` at `github.ref`; `github-actions[bot]` identity; `concurrency` group; keep `cowork-skeleton` **unprotected** (gh-pages parity); job-summary + `if: failure()` notification. `GITHUB_TOKEN` push cannot re-trigger workflows → free loop-safety. | HIGH |
| **Q3** | Users run **`/plugin marketplace add geekatron/jerry@cowork-skeleton`** then **`/plugin install jerry@jerry-framework`**. Manifests stay at root `.claude-plugin/`; `source: "./"` valid. **Must** add via Git (relative paths fail on raw-URL adds). Install clones the whole branch tree → strip directly reduces it. **No vendor-documented file limit** (R-001 stays empirically open). | HIGH |
| **Q4** | Ship the **minimal stub: `projects/` + a tracked `projects/README.md`.** Git can't track empty dirs, so the README is the sentinel that makes `projects/` exist on clone — preventing the uncaught `RepositoryError` in `jerry projects list` and keeping H-04 bootstrap + SessionStart `<project-required/>` working. | HIGH (code-grounded) |

---

## Open Questions and Gaps

| # | Gap | Owner / Next step |
|---|-----|-------------------|
| OQ-1 | **The ~5,000-file CoWork limit is undocumented by Anthropic** and unverified empirically (recon R-001). Whole solution depends on it. | nse-requirements: mandatory acceptance test (reproduce on clean clone vs dev checkout) before Phase 5. |
| OQ-2 | Does CoWork shallow-clone (depth 1) or full-clone marketplace/plugin sources? Affects whether history weight (Q1 (a) vs (b)) matters for the 120s timeout. | Phase 3 design: test install timing on the generated branch; default to (a), keep (b) ready. |
| OQ-3 | Context7 was unavailable; Anthropic-docs claims are current as of fetch (2026-06-26) but vendor docs change. | Phase 3/4: re-verify install syntax against `code.claude.com/docs` at implementation time. |
| OQ-4 | Exact branch-protection posture of the live repo (is any ruleset applied to arbitrary branches?). | Phase 6 (`branch-protection-config.md`): confirm `cowork-skeleton` is unprotected or add a scoped force-push bypass for the Actions actor. |

---

## References

1. [Anthropic Claude Code Docs — Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) — Branch-pin install syntax (`owner/repo@ref`, `#ref`); manifest locations (`.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`); relative-path `source: "./"` rules; install copies whole repo to `~/.claude/plugins/cache`; relative paths require Git-based add; 120s git timeout (`CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`); version-resolution order; **no documented file-count/size limit**. (PRIMARY, HIGH)
2. [GitHub Docs — GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token) — `GITHUB_TOKEN` is repo-scoped and job-expiring; pushes made with it do not create new workflow runs (recursion guard). (PRIMARY, HIGH)
3. [GitHub Docs — Triggering a workflow](https://docs.github.com/actions/using-workflows/triggering-a-workflow) — Events triggered by `GITHUB_TOKEN` (except `workflow_dispatch`/`repository_dispatch`) do not trigger further workflow runs; default `actions/checkout` is shallow (`fetch-depth: 1`). (PRIMARY, HIGH)
4. [git-scm — git documentation](https://git-scm.com/docs) — `git rm`, `git checkout --orphan`, clone materializes the tip working tree; established semantics for Q1. (PRIMARY, HIGH; established behavior, not re-fetched this session)
5. [git-filter-repo (newren/git-filter-repo)](https://github.com/newren/git-filter-repo) — History-rewriting tool; designed for one-time path removal across all history; rewritten SHAs are non-idempotent. Basis for rejecting option (c). (PRIMARY, HIGH; tool semantics)
6. [DeKu — Why GitHub Actions Workflows Don't Re-trigger (GITHUB_TOKEN, PAT, GitHub Apps)](https://deku.posstree.com/en/github_actions/github-actions-workflow-retrigger/) — Corroborates §Q2 recursion behavior. (SECONDARY/LOW, corroborating)
7. [GitHub Community Discussion #25702 — Push from Action does not trigger subsequent action](https://github.com/orgs/community/discussions/25702) — Corroborates `GITHUB_TOKEN` non-retrigger. (LOW, corroborating)
8. [Ninjaneers (Medium) — Letting GitHub Actions Push to Protected Branches](https://medium.com/ninjaneers/letting-github-actions-push-to-protected-branches-a-how-to-57096876850d) — `GITHUB_TOKEN` cannot push to a protected branch; GitHub App / ruleset bypass actor approaches. (LOW, corroborating)
9. [GitHub Community Discussion #25305 — Allowing github-actions[bot] to push to a protected branch](https://github.com/orgs/community/discussions/25305) — Ruleset "Write" bypass / allowed-actor mechanics. (LOW, corroborating)

**Repository sources (PRIMARY, first-party — read this session):**
10. `.github/workflows/release.yml` — `on: push: tags: ['v*']`; `permissions: contents: write`; SHA-pinned `actions/checkout@de0fac2…`; `gh release create`. (Q2 alignment)
11. `.github/workflows/version-bump.yml` — `VERSION_BUMP_PAT` used *because* a `GITHUB_TOKEN` tag push would not trigger `release.yml`; `concurrency: version-bump`; `github-actions[bot]` identity; `if: always()` job summary. (Q2 token contrast)
12. `.github/workflows/docs.yml` — `gh-pages` via `mkdocs gh-deploy --force`; `permissions: contents: write`; `concurrency: docs-deploy`; bot identity. (Q1/Q2 force-push precedent)
13. `src/session_management/infrastructure/adapters/filesystem_project_adapter.py` — `scan_projects` raises `RepositoryError` when `projects/` dir is missing (lines 52–53); files skipped via `is_dir()`. (Q4)
14. `src/application/handlers/queries/scan_projects_query_handler.py` — does **not** catch `RepositoryError` → `jerry projects list` propagates it. (Q4)
15. `src/application/handlers/queries/retrieve_project_context_query_handler.py` — wraps scan in `try/except RepositoryError: pass` (lines 119–121); SessionStart resilience. (Q4)
16. `hooks/session-start.py`, `hooks/hooks.json`, `src/interface/cli/hooks/hooks_session_start_handler.py` — fail-open SessionStart; emits `<project-required/>` when no active project. (Q4)
17. `src/bootstrap.py` (`get_projects_directory`) & `src/interface/cli/adapter.py` (`cmd_projects_list`) — projects-dir resolution and the `projects list` path. (Q4)
18. Recon report `proj-030-recon.md` (scratchpad) — settled facts, file distribution, R-001/R-002, existing-CI survey. (Internal PRIMARY)

---

*Prepared by jerry:ps-researcher for PROJ-031 Phase 1 (Requirements & Architecture). Feeds: nse-requirements (requirements.md), ps-architect (ADR-PROJ031-001 skeleton strategy, ADR-PROJ031-002 token strategy). Context7 unavailable this session (disclosed per P-022); primary vendor docs + first-party code used as substitutes.*
