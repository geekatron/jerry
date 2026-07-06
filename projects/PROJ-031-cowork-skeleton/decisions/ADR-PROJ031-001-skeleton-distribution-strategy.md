# ADR-PROJ031-001: Skeleton Derived-Tree Generation Strategy

> **AMENDED 2026-07-02 (Phase 3 — LIVE-INSTALL VALIDATED; retention surface refined + duplicate-skill-name gate added):** On 2026-07-02 the skeleton was force-pushed to the dedicated repo **`geekatron/jerry-claude-plugin`** (default branch = skeleton) and **installed successfully on Claude Web** — the marketplace synced `last_synced_sha` and the plugin validated + installed. **The dedicated-repo distribution model of [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) is therefore EMPIRICALLY VALIDATED for the install path** (see the honesty caveat below). Reaching a clean install took **two fix cycles**, both caused by the subtractive strip-set ("`main` minus `projects/`+`tests/`") dragging **repo-internal cruft** that broke Claude's plugin validator: **(1) duplicate skill name (BLOCKER)** — an archived skill `skills/.graveyard/worktracker/SKILL.md` collided by name with the live `skills/worktracker/SKILL.md`, and the marketplace **rejects duplicate skill names**; **(2) framework CI in the dedicated repo** — the retained `.github/` ran `docs.yml`, which spawned a gh-pages deploy inside `jerry-claude-plugin` → **loop-safety violation**. **Validated fix:** the strip-set was expanded to **`projects/ tests/ skills/.graveyard/ .github/`**, yielding a **1,399-file tree that installs cleanly**. This amendment therefore: (a) **reframes retention POSITIVELY** — the distribution IS the **plugin surface declared by `.claude-plugin/plugin.json` + `marketplace.json`, plus that surface's runtime dependencies**; the strip-set is only the *mechanism* to reach that surface, **not** a "`main` minus N directories" subtraction; (b) **records the validated strip-set** as decided; (c) **recommends additional non-distribution strips** and (d) makes the **`src/` + `pyproject.toml` + `uv.lock` runtime call = KEEP (verified required)** and (e) adds a **fail-closed no-duplicate-skill-names generation gate** — all specified in [Validated Retention Surface, Strip-Set, and Generation Gate (Phase 3)](#validated-retention-surface-strip-set-and-generation-gate-phase-3). **Honesty caveat (P-022): install-validated ≠ update-propagation-validated** — the 2026-07-02 test proves a *fresh install* works; it does **not** prove a later force-push reaches an **already-installed** user; gate **G-update** remains OPEN (see [L2 §6](#l2-architectural-implications) and [G-update Fallback Architecture](#g-update-fallback-architecture-and-phase-5-entry-gating)). The generation *technique*, determinism contract, tamper-evidence, and the AG-02 core strategy are **UNCHANGED** (P-020); this amendment refines the retention surface and adds a gate only.

> **AMENDED 2026-06-28 (Phase 2 — dedicated-repo model):** the confirmed distribution mechanism changes the artifact's *home* from an in-repo `cowork-skeleton` branch to the **default branch of a dedicated repo (`geekatron/jerry-claude-plugin`)**, and extends the strip set to include **`tests/`**. The generation *technique* in this ADR (checkout tag → strip → deterministic commit → force-push) and its deterministic-SHA tamper-evidence are UNCHANGED and remain valid; only the push target, credential, and integrity-anchor operationalization move to [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md). See [Phase 2 Update](#phase-2-update-2026-06-28--dedicated-repo-distribution-model) for the authoritative delta; it supersedes any in-body reference to "the in-repo `cowork-skeleton` branch," "`GITHUB_TOKEN`," or "Release-notes" anchoring.

> **PS:** cowork-skeleton-20260626-001 (Phase 1 — Requirements & Architecture; Phase 2 — Security & STRIDE incorporation)
> **Exploration:** ps-architect-001 (Phase 1); ps-architect (Phase 2 amendment)
> **Project:** PROJ-031-cowork-skeleton
> **Created:** 2026-06-26
> **Revised:** 2026-06-26 (iteration 3 — QG-1 C4 remediation); **2026-06-28 (Phase 2 — dedicated-repo distribution model + `tests/` strip)**; **2026-07-02 (Phase 3 — live-install validated; strip-set expanded to `projects/ tests/ skills/.graveyard/ .github/`; positive-retention reframe; `src/`+`pyproject`+`uv.lock` KEEP call; no-duplicate-skill-names gate)**
> **Status:** Proposed (Phase-3 — live-install validated)
> **Agent:** jerry:ps-architect
> **Criticality:** C4 (AE-003 auto-escalation → ADR is C3 minimum; this orchestration runs C4, quality target >= 0.95)
> **Approval Gate:** AG-02 (user approval of the derived-tree strategy)
> **Supersedes:** —
> **Superseded By:** — (amended by, not superseded by, [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md))

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language decision and why it matters |
| [Status](#status) | Decision status |
| [Phase 2 Update (2026-06-28)](#phase-2-update-2026-06-28--dedicated-repo-distribution-model) | Authoritative delta: dedicated-repo home, `tests/` strip, credential/anchor → ADR-PROJ031-003 |
| [Context](#context) | Problem, decisive framing, constraints, forces |
| [Canonical Plugin-Retention Surface](#canonical-plugin-retention-surface) | The one authoritative list of directories/files the skeleton MUST retain (c-003) |
| [Validated Retention Surface, Strip-Set, and Generation Gate (Phase 3)](#validated-retention-surface-strip-set-and-generation-gate-phase-3) | Live-install evidence: positive-retention reframe, validated strip-set, recommended additional strips, `src/` runtime call, no-duplicate-skill-names gate |
| [Options Considered](#options-considered) | Three generation techniques, steelmanned |
| [Decision](#decision) | Chosen strategy, clone-weight decision (Option A + continuous monitoring), and rationale |
| [Regeneration Commit Determinism](#regeneration-commit-determinism) | L1 idempotency, tamper-evidence, tag sanitization (pinned dates, parent, 40-char SHA) |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term and systemic consequences |
| [G-update Fallback Architecture and Phase-5 Entry Gating](#g-update-fallback-architecture-and-phase-5-entry-gating) | Fallback update paths if CoWork caches at install; G-update as a Phase-5 ENTRY decision (R-002) |
| [Consequences](#consequences) | Positive, negative, neutral, risks |
| [Related Decisions](#related-decisions) | Links to ADR-PROJ031-003 (amends), ADR-PROJ031-002 (superseded), and work items |
| [References](#references) | Cited evidence |
| [Mirror Hand-Off](#mirror-hand-off-nse-requirements--eng-architect) | What nse-requirements / eng-architect must mirror from this revision |
| [Approval and PS Integration](#approval-and-ps-integration) | AG-02 sign-off and traceability |

---

## L0: Executive Summary

Jerry cannot install as a Claude CoWork plugin because the repository has ~6,344 tracked files, over CoWork's ~5,000-file ceiling, and the `projects/` folder alone is 4,600 of them (72%). The fix is a **derived skeleton tree** (Phase-2: the default branch of the dedicated `geekatron/jerry-claude-plugin` repo — see the amendment header): it is `main` with `projects/` **and `tests/`** removed (dropping to ~1,417 files) plus a tiny `projects/` placeholder so Jerry still boots on a fresh install. CI rebuilds it on every release. **One honesty caveat for go-live (P-022):** rebuilding on every release keeps *new* installs current, but whether CoWork delivers those rebuilds to **already-installed** users is an **unverified CoWork behavior** — a load-bearing assumption that MUST be empirically proven (Phase-5 gate **G-update**; see [L2 §6](#l2-architectural-implications)). We do not assert it works for existing users. That test is, as of 2026-06-29, **blocked by an Anthropic platform-UI defect** (the marketplace "+"/add control was removed), so it cannot be run by anyone today; we therefore treat G-update as a **Phase-5 ENTRY decision** and design explicit **fallback update paths** (in-skeleton stale-version notice; manual re-install how-to; versioned-release/changelog signal) — see [G-update Fallback Architecture and Phase-5 Entry Gating](#g-update-fallback-architecture-and-phase-5-entry-gating).

This ADR decides **how** that branch is generated. We will **check out the release tag, delete `projects/`, inject the stub, make one deterministic commit whose parent is the tagged release commit, and force-push it to `cowork-skeleton`** — the same force-push-a-derived-branch pattern Jerry already uses for its `gh-pages` documentation branch. We reject the history-rewriting alternatives (git-filter-repo, subtree split): they are the wrong tool because a plugin install only materializes the **tip** of the branch, not its history, so there is nothing to gain by scrubbing `projects/` from past commits — and they are slow and non-repeatable.

Why this matters: the generation must be **deterministic** (same release in → same files out, so the file-count acceptance test is stable) and **idempotent** (safe to re-run a release without producing a different commit). We achieve true idempotency by pinning the commit's metadata (author/committer dates copied from the source commit via `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE`, parent set to the tagged commit, and the **full 40-character** source SHA embedded in the commit message — never a variable-length short SHA). Because the same release tag always reproduces a **bit-identical** commit, the published branch is **tamper-evident** on a non-forgeable value: an independent, continuously-running monitor recomputes the expected tip **SHA** (not the forgeable `Source-Commit` text) and detects any in-place modification within a bounded detection window — which is how this deliberately unsigned branch stays tamper-evident (the integrity architecture is now owned by [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) — D4 attestation anchor + D7 monitor). The single genuine trade-off — provenance versus clone weight — is resolved in favor of provenance **by default**; but because full history makes clone weight grow with every release, we convert the one-shot clone-time check into **continuous monitoring** with an early-warning band (~150 MB / ~40 s) ahead of the hard ~250 MB / ~60 s trigger, feeding a pre-designed, now **integrity-neutral** flip to a constant-weight orphan branch (see [Clone-Weight Decision](#clone-weight-decision-option-a-default-plus-continuous-monitoring) and [Consequences](#consequences)).

---

## Status

**Proposed** — awaiting user approval at gate AG-02. Per P-020 this ADR is not in effect until the user authorizes the derived-branch strategy. Per AE-003 an ADR is C3 minimum; this orchestration applies a C4 quality gate (>= 0.95).

**Phase-3 empirical status (2026-07-02):** the derived-tree technique this ADR specifies has now **produced a real, cleanly-installing plugin** (`geekatron/jerry-claude-plugin`, default branch = skeleton, installed on Claude Web) — the strategy is validated end-to-end **through the install path**. This does not move the ADR to ACCEPTED (AG-02 remains the user's authority per P-020) and does not close **G-update** (update-propagation to already-installed users is still unproven — P-022).

---

## Context

PROJ-031 ships Jerry as a Claude CoWork plugin. The repository exceeds CoWork's plugin-load ceiling (~5,000 files) at ~6,344 tracked files; stripping `projects/` (and, per the Phase-2 amendment, `tests/`) reduces this to ~1,417 (settled fact, well under the ceiling). The agreed solution (PLAN.md, Confirmed Decision 1 & 2) is a CI-regenerated `cowork-skeleton` branch equal to `main` minus `projects/`, plus a minimal `projects/` stub so the H-04 active-project bootstrap and the SessionStart hook still function. This ADR selects the **generation technique** for that branch; the **push credential** is selected in [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) D3 (which supersedes the ADR-PROJ031-002 `GITHUB_TOKEN` decision under the Phase-2 dedicated-repo model).

### Decisive Framing (eliminates an entire option family)

A Claude Code plugin install **clones the branch and materializes its working tree at the tip commit**, then copies that tree to a cache (`~/.claude/plugins/cache`). Gitignored artifacts (`.venv/`, `site/`, `__pycache__/`) are absent; **history is not part of the checked-out tree.** Therefore the only thing that affects the installed file count is **the tree at the branch tip** — not whether `projects/` ever existed in history (research §Q1 "Decisive framing"; §Q3 finding 2). This single fact removes any reason to rewrite history and is the spine of the decision below.

### Background

- The skeleton is Jerry's **third** CI-owned derived branch. Precedents already in the repo: `gh-pages` (force-pushed by `docs.yml` via `mkdocs gh-deploy --force`) and the tag-driven `release.yml` artifact flow. `cowork-skeleton` is `gh-pages`'s structural sibling: disposable, regenerated, force-pushed (research §L2 ¶1).
- **Git cannot track an empty directory.** A bare `mkdir projects/` does not survive a clone, so the stub MUST contain at least one tracked file (`projects/README.md`) acting as a sentinel; otherwise a fresh install arrives with no `projects/` at all and `jerry projects list` raises an uncaught `RepositoryError` (research §Q4 "load-bearing insight"). This makes the **stub content part of the generated tree** and therefore part of the determinism contract (see [Regeneration Commit Determinism](#regeneration-commit-determinism)). Stub authoring is STORY-002; this ADR constrains its determinism only.

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| c-001 | Generation MUST be **deterministic**: identical release input produces an identical tree (stable file-count assertion of ~1,417). | research §Q1; PLAN.md Scope |
| c-002 | Generation MUST be **idempotent**: re-running the same release MUST NOT drift the result. | research §Q1 step 2; PLAN.md Scope |
| c-003 | The installed artifact (tip tree) MUST retain the **canonical plugin-retention surface** — the 8 load-bearing directories (with `.claude-plugin/` holding both `plugin.json` and `marketplace.json`) enumerated in [Canonical Plugin-Retention Surface](#canonical-plugin-retention-surface). The **validated strip-set** (Phase-3, live-install-confirmed) removes **`projects/ tests/ skills/.graveyard/ .github/`** — see [Validated Retention Surface, Strip-Set, and Generation Gate](#validated-retention-surface-strip-set-and-generation-gate-phase-3). | `.claude-plugin/plugin.json`; `.claude-plugin/marketplace.json`; root tree (verified 2026-06-26); live install 2026-07-02; research §Q3/§Q4 |
| c-004 | Force-push to `cowork-skeleton` MUST be safe (CI-owned, never a development target). | research §Q2 branch-protection; §L2 ¶1 |
| c-005 | Approach MUST be simple and maintainable (minimal tooling, reuse existing operational patterns). | PLAN.md Goals; research §Q1 |
| c-006 | The stub MUST contain a tracked file inside `projects/` (empty-dir sentinel). | research §Q4 |
| c-007 | The generated tip tree MUST contain **no duplicate skill names** — every `SKILL.md` under `skills/` MUST resolve to a unique skill name. This is the exact marketplace invariant that rejected fix-cycle #1 (`skills/.graveyard/worktracker` collided with live `skills/worktracker`). Generation MUST **fail closed** on any duplicate before push. | live install 2026-07-02 (marketplace duplicate-skill rejection); `.claude-plugin/marketplace.json` |
| c-008 | The generated tip tree MUST retain the **runtime dependencies of the hook surface**: `src/`, `pyproject.toml`, and `uv.lock`. Every hook shells out to `uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry … hooks <event>`; `pyproject.toml` binds `jerry → src.interface.cli.main:main` (hatch `packages=["src"]`), and `uv.lock` pins the CLI's dependency closure. Stripping any of the three makes `uv run jerry` fail; because hooks **fail-open**, this does not crash install but **silently no-ops every Jerry guardrail**. | `hooks/hooks.json`; `hooks/*.py`; `pyproject.toml:65,72-73` (verified 2026-07-02) |

### Forces

1. **Determinism vs. flexibility:** a reproducible file-count test demands a fixed transformation; convenience features (timestamps, run IDs in the commit) would break reproducibility.
2. **Provenance vs. clone weight:** preserving a parent chain to the released tag gives auditable lineage and a working `diff` against `main`, but carries `main`'s history weight into the branch's `.git`, which is the input to CoWork's 120-second git-operation timeout.
3. **Idempotency vs. natural git behavior:** git stamps "now" into author/committer dates by default, which would make every re-run a *different* commit SHA unless dates are pinned.
4. **Wholesale regeneration vs. accumulation:** force-push must replace the tip cleanly so per-release skeletons do not pile up.

---

## Canonical Plugin-Retention Surface

*(Authoritative list for c-003. **REM-008 reconciliation — this ADR OWNS the list; the requirements' REQ-005 mirrors it verbatim.**)*

Iteration 1 found ADR-PROJ031-001 c-003 and the requirements' REQ-005 enumerating **different** directory sets (`commands/` in one, `src/` + `schemas/` in the other, `marketplace.json` in neither). Resolved here against **empirical ground truth** — `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and the actual `main` root tree (verified 2026-06-26). The **validated strip-set** (Phase-3, live-confirmed 2026-07-02) removes `projects/`, `tests/`, `skills/.graveyard/`, and `.github/` — see [Validated Retention Surface, Strip-Set, and Generation Gate](#validated-retention-surface-strip-set-and-generation-gate-phase-3); every load-bearing entry below MUST survive the strip and be present at the branch tip. There is **no** root-level `agents/` directory — all 88 agents resolve under `skills/*/agents/*.md` (confirmed against `plugin.json` `agents[]`).

The canonical surface is **8 load-bearing directories**, with `.claude-plugin/` required to contain **both** `plugin.json` and `marketplace.json` (rows 1–2):

| # | Entry (MUST retain) | Tier | Why the plugin needs it (verified) |
|---|---------------------|------|-------------------------------------|
| 1 | `.claude-plugin/plugin.json` | Plugin-load surface | Plugin manifest; declares `skills`, `agents`, `commands`. |
| 2 | `.claude-plugin/marketplace.json` | Plugin-load surface | Marketplace install entry (`source: "./"`). **Was missing from both prior lists** — a tree without it fails CoWork install silently (FM-006). |
| 3 | `skills/` | Plugin-load surface | `"skills": "./skills/"`; **all** `agents[]` paths resolve under `skills/*/agents/*.md`. |
| 4 | `commands/` | Plugin-load surface | `"commands": ["./commands/architect.md","./commands/release.md"]`. (Was in ADR c-003; **absent from REQ-005**.) |
| 5 | `.claude/` | Jerry-runtime | `settings.json` (statusline + hook registration), `rules/` symlinks (L1 auto-load), `patterns/`. Session bootstrap. |
| 6 | `.context/` | Jerry-runtime | Rule content (`.context/rules/*.md`) that `.claude/rules/` symlinks to. |
| 7 | `hooks/` | Jerry-runtime | `session-start.py` (H-04 project bootstrap), `hooks.json`, pre-tool / stop gates. |
| 8 | `src/` | Jerry-runtime | Jerry CLI (hexagonal Python); `jerry projects list` / `jerry session start` / the H-04 bootstrap live here. (Was in REQ-005; **absent from ADR c-003**.) |
| 9 | `schemas/` | Jerry-runtime | `hooks.schema.json`, `hooks/*` output schemas, `marketplace.schema.json`; referenced by `src/interface/cli/main.py` and hook validation. (Was in REQ-005; **absent from ADR c-003**.) |

**Plugin-load surface** (rows 1–4) is what the Claude Code plugin loader reads to install and register the plugin. **Jerry-runtime** (rows 5–9) is what the installed plugin needs to actually *function* — guardrails, hooks, and the H-04 first-run bootstrap (without `src/`, `jerry projects list` raises the uncaught `RepositoryError` of research §Q4). Both tiers are retained because the **validated strip-set** removes `projects/`, `tests/`, `skills/.graveyard/`, and `.github/` (Phase-3). `projects/` and `tests/` are non-load-bearing (test suite + work artifacts); `skills/.graveyard/` and `.github/` were added to the strip-set after the 2026-07-02 live install (duplicate-skill rejection + framework-CI loop — see the [Validated Retention Surface](#validated-retention-surface-strip-set-and-generation-gate-phase-3)). The resulting tip tree is **1,399 files** (measured; the earlier `projects/`+`tests/`-only estimate was ~1,417). Of the remaining non-load-bearing directories, **`runbooks/` is retained** (plugin surface), while **`docs/` and `scripts/` are now RECOMMENDED for stripping in Phase-3** (with `mkdocs.yml`/`CNAME`/`.nojekyll` and dev/governance cruft, −285 files → ~1,114; see the recommended-strips table) — superseding the earlier "retained today, MAY strip later (R-002)" posture for those two.

### Deterministic retention-surface verification (drift-proof — R-008 / FM-030)

The retention surface is enforced by **two mechanisms that are deterministic by construction**, so a newly-added agent or command can never be silently excluded as the codebase grows:

1. **Generation is a denylist strip, not an allowlist copy.** Generation runs `git rm -r projects/ tests/` against the frozen tag tree — i.e. it **retains everything except** the two stripped trees. New agents added under `skills/*/agents/*.md`, new `commands/*.md`, new `.context/rules/*.md`, etc. are therefore retained **automatically**; there is no static "keep list" for generation to fall out of sync with. The static 9-row table above is a **load-bearing verification surface**, not the generation mechanism.
2. **Completeness is verified against `plugin.json`, never against a hard-coded list.** The post-strip acceptance check (REQ-010) SHALL derive its required-present set **dynamically from `.claude-plugin/plugin.json`** at generation time — enumerating every declared `skills`, `agents[]`, and `commands[]` path and asserting each resolves in the generated tip tree via `git ls-files` — rather than checking a frozen enumeration. Because `plugin.json` is the single source of truth the plugin loader itself reads, deriving the check from it makes "the manifest declares it ⇒ the skeleton contains it" a deterministic invariant that cannot drift as agents are added (FM-030). The verification SHALL read declared paths exactly (not via a shallow `skills/*/agents/*.md` glob that assumes today's one-level nesting), so a future nested agent layout is covered. nse-requirements owns REQ-010's acceptance-criterion tightening; this ADR fixes the deterministic-generation property.
3. **No-duplicate-skill-names gate — fail-closed, BEFORE push (c-007; NEW Phase-3, marketplace-invariant).** The 2026-07-02 live install proved that a subtractive strip can retain an **archived** skill (`skills/.graveyard/worktracker/SKILL.md`) whose name **collides** with a live skill (`skills/worktracker/SKILL.md`), and that Claude's marketplace **rejects the plugin** on duplicate skill names. The generator MUST therefore, after the strip and before the force-push, enumerate every `SKILL.md` in the generated tip tree, resolve each to its skill name (frontmatter `name`, falling back to the containing directory basename), and **abort with a non-zero exit and NO push** if any name appears twice. This is a *fail-closed* safety gate, not an advisory check: a duplicate is a hard build failure. Stripping `skills/.graveyard/` (validated strip-set) removes today's known collision; the gate is the durable guard that prevents any *future* archived-or-vendored skill from silently re-introducing one. **Ownership:** nse-requirements adds the acceptance requirement, nse-architecture adds the generation step, eng-devsecops adds the CI enforcement gate (see [Mirror Hand-Off](#mirror-hand-off-nse-requirements--eng-architect)).

---

## Validated Retention Surface, Strip-Set, and Generation Gate (Phase 3)

*(Live-install evidence, 2026-07-02. This section refines the retention surface and adds a generation gate; it does NOT change the generation technique, determinism contract, or AG-02 core strategy — P-020.)*

### The retention principle, stated POSITIVELY (R-001 reframe)

The prior framing — *"the skeleton is `main` minus `projects/`, `tests/`, …"* — is **subtractive and unbounded**: it invites the question "minus what else?" and, worse, it silently **retains whatever nobody remembered to subtract**. The 2026-07-02 live install proved the concrete cost of that framing: two repo-internal artifacts nobody had listed (`skills/.graveyard/`, `.github/`) rode along and **broke the marketplace validator**. The correct, bounded framing is **additive**:

> **The distribution is the plugin surface — everything declared by `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — PLUS that surface's runtime dependencies. Nothing else belongs in the skeleton.** The strip-set is merely the *mechanism* that removes what is NOT in that set; it is not the definition of the artifact.

Under this principle the artifact is defined by an **allow-set** (the [Canonical Plugin-Retention Surface](#canonical-plugin-retention-surface) + runtime deps), and every repo-internal directory is presumed **strippable unless it is on the surface or a runtime dependency of it**. This inverts the burden of proof in the safe direction: an un-classified directory is a candidate for *removal*, not for silent *retention*. Generation still executes as a denylist strip for determinism (see [verification mechanisms 1–3](#deterministic-retention-surface-verification-drift-proof--r-008--fm-030)), but the denylist is now derived from, and audited against, this positive definition.

### Validated strip-set (DECIDED — live-install-confirmed 2026-07-02)

The strip-set below is **empirically validated**: with it applied, the 1,399-file tree pushed to `geekatron/jerry-claude-plugin` **validated and installed cleanly on Claude Web**. It supersedes the Phase-2 `projects/`+`tests/`-only strip.

| Stripped | Files | Why it is NOT distribution | Evidence |
|----------|-------|----------------------------|----------|
| `projects/` | ~4,600 | Work artifacts; not plugin surface. A minimal `projects/` **stub** is re-injected (c-006) so H-04 bootstrap works. | Phase-1 (file-count driver) |
| `tests/` | (bulk) | Test suite; not load-bearing for plugin function. | Phase-2 ([ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) D1) |
| `skills/.graveyard/` | 2 | Archived skills. `.graveyard/worktracker/SKILL.md` **name-collided** with live `skills/worktracker` → **marketplace rejected the plugin** (fix-cycle #1, BLOCKER). | **Live install 2026-07-02** |
| `.github/` | 14 | Framework CI/CD. Ran in the dedicated repo — `docs.yml` spawned a gh-pages deploy inside `jerry-claude-plugin` → **loop-safety violation** (fix-cycle #2). | **Live install 2026-07-02** |

**Net: 6,344 → 1,399 tracked files.** (Reconciles with the Phase-2 `~1,417` estimate: the two newly-stripped trees remove 16 further files; the residual delta is estimate-vs-measured.)

### Runtime-dependency call — `src/` + `pyproject.toml` + `uv.lock`: **KEEP (verified required, NOT a guess)**

This is the "big open" from the retention analysis. **Call: KEEP all three. They are runtime dependencies of the hook surface, verified by static analysis of the hook → CLI → entry-point chain** — the grep showing hooks do not `import src/jerry` is a **red herring**, because the coupling is a **subprocess CLI invocation, not a Python import**:

1. `hooks/hooks.json` wires all six lifecycle events (SessionStart, UserPromptSubmit, PreCompact, PreToolUse, SubagentStop, Stop) to `uv run --directory ${CLAUDE_PLUGIN_ROOT} …`.
2. Each wrapper (`hooks/*.py`) shells out to **`uv run --directory ${root} jerry --json hooks <event>`**.
3. `pyproject.toml:65` binds the `jerry` console script to **`src.interface.cli.main:main`**; `pyproject.toml:72-73` sets hatch `packages = ["src"]`; `uv.lock` pins the CLI's dependency closure that `uv run` syncs.

Therefore `uv run jerry` **requires all three**: `pyproject.toml` (declares the `jerry` entry point + deps), `src/` (the entry point's code — `jerry projects list`, the H-04 bootstrap), and `uv.lock` (deterministic dependency resolution). They are already rows 8 (`src/`) and — for their sibling — 9 (`schemas/`) of the [Canonical Plugin-Retention Surface](#canonical-plugin-retention-surface); this amendment adds `pyproject.toml` + `uv.lock` explicitly as the surface's build/runtime manifest (c-008).

> **P-022 — the failure mode if stripped, stated plainly.** Hooks **fail-open** (each wrapper catches all exceptions and returns "approve"/empty). So stripping `src/`/`pyproject`/`uv.lock` would **not crash the install** — it would silently make `uv run jerry` fail on every hook, turning the **entire Jerry guardrail layer into a no-op** (no H-04 bootstrap, no pre-tool enforcement, no context/stop gates) with **no error surfaced**. That is strictly worse than a crash. This is exactly the trap a "grep-clean ⇒ strip" guess would spring. **Do NOT strip on the grep.**
>
> **Residual (honest scope — P-022).** The KEEP call is conclusive for *dependency existence*. The 2026-07-02 test validated **install**, and because hooks fail-open, a successful install does **not** by itself prove the hooks **executed** correctly in the CoWork sandbox (install-validated ≠ hook-execution-validated). Recommended defense-in-depth (not a gate on KEEP): a post-install **hook-smoke check** that asserts `uv run jerry hooks session-start` returns non-empty in the installed tree. eng-devsecops owns this.

### Recommended ADDITIONAL strips (NOT decided — recommended; non-distribution, no runtime need)

These are **still-present repo-internal** directories/files that are **neither plugin surface nor runtime dependencies**. Stripping them further shrinks the tree and removes framework doc-site/dev/governance cruft. Each is git-verified runtime-safe (no reference from `src/interface/`, `plugin.json`, `marketplace.json`, or the hook path). Presented as a **recommendation** for nse-architecture to fold into the generation design — not asserted as decided (P-020/P-022).

| Recommended strip | Files | One-line rationale |
|-------------------|-------|--------------------|
| `docs/` | 247 | mkdocs **source** for the framework documentation website; the site is published from the *source* repo's gh-pages, never consumed by the plugin. |
| `mkdocs.yml` + `CNAME` + `.nojekyll` | 3 | Doc-site build config + GitHub-Pages custom-domain/Jekyll markers; meaningless in the dedicated plugin repo (and part of what made `.github/`'s `docs.yml` dangerous). |
| `scripts/` | 28 | Dev/release/CI helper scripts; the hook runtime calls the `jerry` CLI, not `scripts/` (verified: no `src/interface/` reference). |
| `Makefile` + `.pre-commit-config.yaml` + `pytest.ini` | 3 | Developer build/lint/test tooling; no runtime role in an installed plugin. |
| `CHANGELOG.md` + `CONTRIBUTING.md` + `CODE_OF_CONDUCT.md` + `GOVERNANCE.md` | 4 | Source-repo governance/contribution docs; not plugin surface. (`LICENSE`/`NOTICE` are **retained** for attribution; `README.md`, `AGENTS.md`, `CLAUDE.md`, `TOOL_REGISTRY.yaml` are **retained** as runtime/agent surface.) |

**Recommended-strip impact: −285 files → ~1,114-file tree** (from the validated 1,399). One honesty note (P-022): `commands/release.md` *writes* `docs/plans/RELEASE_*.md` — that is a maintainer-only command **creating** a path on demand, not a runtime **read** of the stripped `docs/` source, so the strip is safe; the generator's "no retained file references a stripped path" audit (below) covers any regression.

**Guard for the recommended strips.** Because these are broader, the generator SHOULD, after stripping, assert that **no retained file references a stripped path** at runtime (complementing the `plugin.json`-derived completeness check, mechanism 2). This keeps the additive-allow-set principle enforced deterministically as the recommendation lands.

---

## Options Considered

### Option A: Checkout `v*` tag → `git rm -r projects/` → inject stub → deterministic commit → force-push  (CHOSEN)

Build from the triggering `v*` tag (the frozen released tree), remove `projects/`, write the fixed stub, create one commit whose **parent is the tagged release commit** with pinned metadata, and force-push `cowork-skeleton`. Four plain git commands; no extra dependency. Mirrors the proven `gh-pages` force-push model.

**Pros:**
- **Deterministic tree** by construction: `tree = f(source tree − projects/ + fixed stub)` (c-001).
- **True idempotency achievable**: with pinned parent, identity, dates, and message, re-running the same tag yields a **bit-identical commit SHA** (c-002; see [Regeneration Commit Determinism](#regeneration-commit-determinism)).
- **Strong provenance**: parent chains to the exact `v*` release commit; `git log` and `git diff main..cowork-skeleton` work; an installed artifact is auditable back to a release.
- **Simplicity / maintainability**: no new tooling; reuses the existing force-push pattern reviewers already understand (c-005).
- **No history accumulation**: force-push replaces the tip wholesale; branch = `main` history + 1 commit.
- **Full plugin surface preserved**: strip removes only non-load-bearing trees (`projects/` and, per the Phase-2 amendment, `tests/`), leaving the entire plugin-retention surface intact (c-003).

**Cons:**
- Carries `main`'s history weight into the branch `.git` (clone-weight pressure on the 120s timeout) when full provenance (`fetch-depth: 0`) is preserved.
- Idempotency is **conditional** on disciplined metadata pinning; an un-pinned date silently breaks it.

**Fit with Constraints:** Satisfies c-001..c-006. Only c-002 carries an operational caveat (pinning discipline), addressed in [Regeneration Commit Determinism](#regeneration-commit-determinism).

### Option B: Orphan branch (`git checkout --orphan`) rebuilt each release

Create a parentless single squashed commit containing the stripped tree.

**Steelman:** This is genuinely attractive on **clone weight** — O(1) history means the lightest possible `.git`, directly easing the 120-second git-operation timeout that is the real-world clone-weight risk (research §L2 ¶4; §Q3 finding 4). The installed tip tree is identical to Option A's, so plugin-install compatibility is equally full. For a pure "smallest possible download" objective, orphan is the strongest option.

**Pros:**
- Lightest clone (O(1) history) — best timeout headroom.
- Same correct tip tree → full install compatibility.
- Idempotent if dates/message are pinned (same discipline as Option A).

**Cons:**
- **Weak provenance**: no parent chain to the released tag; lineage survives only as text in the commit message, and `diff against main` does not work for a cloner.
- Loses the auditable "this skeleton == this release" link that a C4 supply-chain argument benefits from.

**Fit with Constraints:** Satisfies c-001..c-006 except it weakens the (non-mandatory but valuable) provenance property. Retained as a **documented escape hatch**, not the default.

### Option C: `git-filter-repo` / `git subtree split` (history rewrite)

Rewrite history to remove `projects/` from every commit (filter-repo) or extract a subtree (subtree split).

**Steelman:** These tools are excellent when the requirement is *"`projects/` must never have existed in any commit a cloner can reach"* — e.g., purging leaked secrets, or carving out a sub-library **with** its own history. If CoWork did a full-depth clone and counted historical objects, filter-repo would be the correct instrument.

**Pros:**
- Deterministic tip tree (like A/B).
- The right tool for true historical erasure.

**Cons:**
- **Solves a problem we do not have**: the install materializes the **tip working tree**; history erasure changes nothing about the installed file count (decisive framing).
- **Non-idempotent**: rewritten commit SHAs differ on every run → violates c-002.
- **Slow and heavyweight** on a 6,344-file repo; adds an external dependency → violates c-005.
- `subtree split` does the **inverse** of the need (it *keeps* one subdirectory; we want everything *except* one).

**Fit with Constraints:** Fails c-002 (idempotency) and c-005 (simplicity). Rejected.

### Option Comparison

| Criterion | A: tag + rm + stub + force-push | B: Orphan | C: filter-repo / subtree |
|-----------|----------------------------------|-----------|--------------------------|
| Determinism (tree) | Deterministic | Deterministic | Deterministic |
| Idempotency (commit SHA) | **Bit-identical** (pinned) | Idempotent (pinned) | **Non-idempotent** |
| Derived-branch history size | `main` + 1 commit | **O(1)** | Full rewritten history |
| Force-push safety | Safe (CI-owned) | Safe | Safe but pointless |
| Plugin-install compatibility | Full | Full | Full (over-engineered) |
| Provenance to release | **Strong** (parent = tag) | Weak (message only) | Weak (SHAs rewritten) |
| Simplicity / maintainability | **High** (4 git cmds) | Medium | **Low** (dep + slow) |

---

## Decision

**We will use Option A:** generate `cowork-skeleton` by checking out the triggering `v*` tag, running `git rm -r projects/`, writing the fixed `projects/` stub, creating one deterministic commit whose parent is the tagged release commit, and force-pushing `cowork-skeleton`. **Option B (orphan) is adopted as a documented fallback**, triggered by a **measurable** threshold (not a hunch): switch to Option B if a clean `git clone` of `cowork-skeleton` (full-provenance, `fetch-depth: 0`) measured on the reference network (a 10 Mbps downlink) exceeds **60 s** wall-clock — 50% of CoWork's 120 s git-operation timeout — **or** its compressed pack (`git count-objects -vH` → `size-pack`) exceeds **250 MB**. **Option C is rejected** as the wrong tool for a tip-tree distribution.

### Clone-Weight Decision (Option A default plus continuous monitoring)

*(IT3 clone-weight / IN-002 / FM-007)*

Option A carries `main`'s full history, so under it the skeleton's `.git` clone weight grows **monotonically** — every release adds ~1 commit plus accumulated history (empirically ~2 MB/release on this repo). The iteration-2 R-001 clone-time gate (REQ-034) is a **single-shot** Phase-2 snapshot, which cannot certify a monotonically growing quantity: the pack could cross the 250 MB / 60 s flip trigger silently *between* the Phase-2 measurement and a future release (IN-002 Critical, FM-007 Major).

I evaluated the inverse — **making the orphan branch (Option B) the default** to get constant O(1) weight by construction (S-013 inversion; S-003 steelman of B). It is genuinely attractive: it *eliminates* the growth failure mode outright, and — critically — after IT3-002/IT3-004 the orphan flip is now **integrity-neutral**, because tamper-evidence rests on the independently-recomputable **deterministic SHA**, not on the parent chain (see [Tamper-Evidence](#tamper-evidence-and-supply-chain-integrity)). **I nonetheless retain Option A as the default**, for three reasons: (i) the growth is *slow and well-bounded* — at ~2 MB/release the 250 MB trigger is dozens of releases (1–3 years) away, not imminent; (ii) the parent chain retains genuine **defense-in-depth** value for an artifact that ships *executable hooks* to user workstations (a verifier can run `git merge-base --is-ancestor <skeleton-parent> main` as a cheap second check complementing SHA recomputation — relevant to the R-007b hook-injection risk, IT3-007); and (iii) reversing a deliberate, user-pending decision (AG-02) for a slow, now-integrity-neutral-to-flip risk is over-correction. **The correct fix for IN-002/FM-007 is therefore to convert the single-shot gate into continuous telemetry**, not to flip the default:

| Control | Mechanism | Threshold | Action |
|---------|-----------|-----------|--------|
| **Per-release weight emit** | `cowork-skeleton.yml` emits `git count-objects -vH` (`size-pack`) + a timed reference clone to `$GITHUB_STEP_SUMMARY` on every run | record always; **hard-fail** at > 250 MB pack | blocks the release; forces the Option B decision |
| **Scheduled weight telemetry** | a dedicated **clone-weight telemetry step** — scheduled on the SOURCE repo alongside, but operationally **distinct from**, the [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) D7 integrity monitor — performs a **timed reference clone** of the dedicated repo each cycle purely to record `size-pack` + clone time, then discards it | **early-warning band ≈ 150 MB pack / 40 s** (≈ 60% of the hard trigger) | open a GitHub issue: advance notice to execute the pre-designed orphan flip **proactively** |
| **Flip to Option B** | one-line change (`git checkout --orphan` instead of branch-from-tag); integrity-neutral post-IT3-004 | on warning-band breach or R-001 empirical pressure | constant-weight orphan becomes the new default |

> **R-001 reconciliation — telemetry clones; the integrity monitor does NOT (CV-006).** Iteration-006 found a factual contradiction: this ADR previously stated the integrity workflow "clones the skeleton every cycle," while [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) D7 specifies the integrity monitor is **read-only** (`git ls-remote` / `gh api`, explicitly **not** a clone). These are reconciled to **one consistent operation across both ADRs**: the D7 integrity monitor is read-only and never clones (the security-load-bearing design — a read-only poll cannot be coerced into pushing or into manufacturing a passing result). **Measuring clone *weight*, by definition, requires actually cloning** — so the clone-weight telemetry above is a **separate, clearly-scoped measurement step** (a timed reference clone whose only output is `size-pack` + elapsed seconds, immediately discarded). It MAY share the same scheduled `cowork-monitor.yml` workflow as a distinct job, but it is not the integrity check and carries no integrity authority. ADR-PROJ031-003 D7 carries the mirror of this note.

The early-warning band (60% of trigger) ensures the flip is **proactive on advance notice**, never a reactive migration under a live install-timeout failure. nse-requirements backs this with the clone-weight monitoring requirement (IT3-003d) and the continuous integrity workflow's telemetry duty.

### Rationale

Option A is the only option that simultaneously delivers determinism (c-001), achievable bit-identical idempotency (c-002), strong release provenance, and minimal tooling (c-005) while reusing the proven `gh-pages` force-push pattern. The decisive framing removes Option C's entire rationale, and Option A dominates Option B on provenance while matching it on the installed artifact. The provenance-vs-clone-weight tension (Force 2) is the one real trade-off; we choose provenance by default because (i) history weight affects only **clone bandwidth**, never installed file count, and (ii) if and only if clone timing becomes a problem, switching to Option B is a one-line, pre-designed change rather than a redesign.

> **Build from the tag, not from moving `main`.** The `v*` tag points at the version-bump commit on `main` (`version-bump.yml` → `release.yml`), so the tag's tree *is* the released `main` content, frozen. Building from the tag makes the skeleton reproducible for that exact release and removes any race with `main` advancing mid-run.

> **Correction carried from research (for eng-infra / requirements):** the earlier design note "checkout `main` with full history for accurate `git ls-files`" is inaccurate — `git ls-files` reads the index/working tree and needs **no** history. `fetch-depth: 1` suffices for the strip and the file-count assertion. `fetch-depth: 0` is required **only** to preserve `main`'s full ancestry in the skeleton (Option A with a real parent chain). Default to `fetch-depth: 0` to keep Option A's provenance benefit; this is the deliberate clone-weight cost noted above.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | c-001..c-006 met; c-002 needs pinning discipline (specified below). |
| Risk Level | MED | Top residual risk is external (unverified ~5,000-file limit, R-001), not in the technique. |
| Implementation Effort | S | Four git commands plus a generation script; no new dependency. |
| Reversibility | HIGH | Branch is regenerated wholesale every release; switching to Option B is one-line. |

---

## Regeneration Commit Determinism

*(L1 — Technical Implementation. This is the idempotency proof ADR-PROJ031-001 must cite.)*

A git commit SHA is the hash of: **tree object, parent SHA(s), author (name/email/date), committer (name/email/date), and commit message** (plus an optional signature). To make re-running the **same** `v*` tag produce a **bit-identical** commit SHA, every one of these inputs must be invariant for that tag:

| Commit input | Pinned value | Why it is invariant for a given tag |
|--------------|--------------|-------------------------------------|
| **Tree** | `f(tree(tag) − projects/ + fixed stub)` | The tag's tree is frozen; `git rm -r projects/` is deterministic; the stub content is static (no generated timestamps). |
| **Parent** | the tagged release commit SHA | The `v*` tag resolves to exactly one commit. |
| **Author / committer identity** | `github-actions[bot]` / `41898282+github-actions[bot]@users.noreply.github.com` | Fixed bot identity reused from `docs.yml` / `version-bump.yml`. |
| **Author date / committer date** | the **source commit's** committer date, set via `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` | Copied from the tagged commit — **not** "now". This is the single most important pin; default git would stamp the current time and break idempotency. |
| **Commit message** | fixed template embedding the source tag + the **full 40-char** source SHA in **both** the subject line and the `Source-Commit` trailer, with **no** build timestamp, run ID, or abbreviated (`--short`) SHA | The tag and its full SHA are invariant and fixed-length; run-specific and variable-length values are deliberately excluded (FM-010). |
| **Signature** | **unsigned** (or deterministically signed) | A timestamped GPG signature would vary per run and break the bit-identical SHA. Do not sign the regeneration commit. |

**Deterministic generation — pin both dates to the source commit (FM-009).** Author and committer dates MUST be copied from the **source** commit, never stamped as "now". The generation script exports them before committing:

```bash
# 1) Resolve the release TAG from the trigger context (IT3-005 — source-ref correctness).
#    push: tags/v*      -> GITHUB_REF_NAME *is* the tag name (correct as-is).
#    workflow_dispatch  -> GITHUB_REF_NAME is the *triggering branch* (e.g. "main"),
#                          NOT a tag. The tag comes from inputs.target_tag, or — when
#                          that input is blank — is resolved to the newest v* tag (REQ-011).
#    WARNING: the naive one-liner TAG="${INPUT_TARGET_TAG:-${GITHUB_REF_NAME}}" is UNSOUND:
#    on a *blank-input* workflow_dispatch it silently falls through to the branch ("main"),
#    so the event must be discriminated explicitly.
if [ "${GITHUB_EVENT_NAME}" = "workflow_dispatch" ]; then
  if [ -n "${INPUT_TARGET_TAG}" ]; then          # inputs.target_tag supplied (REQ-011)
    TAG="${INPUT_TARGET_TAG}"
  else                                            # blank input -> newest semver tag
    TAG="$(git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname | head -1)"
  fi
else                                              # push: tags/v* -> ref name IS the tag
  TAG="${GITHUB_REF_NAME}"
fi

# 2) Validate the RESOLVED tag against the allow-list BEFORE any further use (RT-04).
#    ONE gate covers GITHUB_REF_NAME, inputs.target_tag, AND the blank-resolved tag —
#    no resolved value reaches a shell, a git ref, or the commit object unvalidated.
if ! printf '%s' "${TAG}" | grep -Eq '^v[0-9]+\.[0-9]+(\.[0-9]+)?$'; then
  echo "::error::Refusing to build cowork-skeleton: tag '${TAG}' fails the v* allow-list." >&2
  exit 1   # non-zero exit, NO push
fi

# 3) Resolve the source commit and pin both dates to it (never "now").
SRC_SHA="$(git rev-parse "${TAG}^{commit}")"          # full 40 hex chars, fixed length
SRC_DATE="$(git show -s --format=%cI "${SRC_SHA}")"   # source committer date, ISO-8601
export GIT_AUTHOR_DATE="${SRC_DATE}"
export GIT_COMMITTER_DATE="${SRC_DATE}"
# ... git rm -r projects/ ; write static stub ; git commit (parent = SRC_SHA) ...
```

> **IT3-005 — why `GITHUB_REF_NAME` alone is wrong (CC-002).** `GITHUB_REF_NAME` equals the tag only for the `push: tags` trigger. On `workflow_dispatch` it equals the *triggering branch* (`main`), so assigning `TAG="${GITHUB_REF_NAME}"` verbatim would make `git rev-parse "main^{commit}"` resolve to the moving HEAD of `main` — non-deterministic, breaking c-001/c-002 and NFR-005 (re-runnable for a *past* tag). The event-discriminated block above resolves the correct source ref for **both** triggers; step 2 then applies the RT-04 allow-list to whichever value was resolved.

**Recommended commit message template (fixed-length inputs only):**

```
build(cowork-skeleton): regenerate from <tag> at <full-40-char-source-SHA>

Strips projects/ and tests/ for Claude CoWork plugin distribution (~1,417 files).
Source-Tag: <tag>
Source-Commit: <full-40-char-source-SHA>
Generated-By: .github/workflows/cowork-skeleton.yml
```

**Why the full 40-char SHA, never `--short` (FM-010).** Git's `--short` abbreviation length **grows with repository object count** (7 → 8 → … hex chars as ambiguity rises). A short SHA in the subject would therefore change for the *same* tag as the repo grows, mutating the commit message — and hence the commit SHA — and silently breaking the bit-identical idempotency guarantee (c-002). The subject embeds the **full, fixed-length 40-character** SHA; the `Source-Commit` trailer repeats it verbatim. The longer subject line is an accepted, deliberate trade for determinism.

**Tag-name sanitization (security — RT-04).** **Two** workflow inputs are attacker-influenceable and feed the same `TAG` variable, which the workflow embeds in the commit subject, the `Source-Tag` trailer, and (if mishandled) in git command lines:

- `GITHUB_REF_NAME` — controlled by anyone able to push a `v*` tag (the `push: tags` path).
- `inputs.target_tag` — controlled by **any repository collaborator with `workflow_dispatch` permission** (the manual-replay path, REQ-011). It is *exactly* as untrusted as `GITHUB_REF_NAME` and MUST NOT be treated as a privileged maintainer-only value.

Untrusted, either is a **shell-injection and commit-message/trailer-injection surface**. The generation script MUST therefore:
1. **Validate the resolved `TAG`** (whichever source produced it — `GITHUB_REF_NAME`, `inputs.target_tag`, **or** the blank-input fallback resolution) against the strict allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$`, and abort (non-zero exit, **no push**) on any non-match — rejecting tags containing whitespace, `$()`, backticks, newlines, `;`, or `-`-prefixed option-injection. The allow-list is checked **once, on the resolved value, BEFORE** that value is used in any shell command, git ref, or commit message (see step 2 of the pseudocode above).
2. **Pass it as an environment variable** (`TAG="…"`, `INPUT_TARGET_TAG="${{ inputs.target_tag }}"` bound in an `env:` block) consumed only by **quoted** expansions — **never** interpolate `${{ github.ref_name }}` or `${{ inputs.target_tag }}` directly into a `run:` shell string (which GitHub expands into the script *before* the shell parses it, the classic Actions script-injection vector).

This converts both release-driven workflow inputs into a single constrained, audited value before it can reach a shell or the commit object.

> **Scope boundary — syntax vs. provenance (RT-003, deferred to Phase 2 / STRIDE).** The allow-list validates the tag's **syntax** only; it does **not** establish the tag's **provenance**. A well-formed but illegitimate tag (e.g. an attacker pushes `v9.9.9` pointing at a malicious commit, or `workflow_dispatch` is invoked with a `target_tag` that does not correspond to a real `version-bump.yml`/`release.yml` release) passes the allow-list. Asserting that the resolved tag points at a commit reachable from `main` / produced by the release pipeline is a **provenance** control, not a sanitization control, and is delegated to the Phase-2 STRIDE threat model (STORY-004). Phase 1 commits only to syntactic safety here; the **provenance** control for a wrong-but-well-formed tag is decided in [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) D5 (tag-on-`main` ancestor assertion + `v*` tag protection). **Correction (aligned with ADR-PROJ031-003 D5):** the deterministic-SHA *monitor* can**not** catch a rogue-but-well-formed tag — CI faithfully builds *and attests* it — so monitoring is **not** the compensating control here; provenance is.

**Idempotency proof sketch:** Given tag `T` resolving to source commit `S` with committer date `D`, the regenerated commit's preimage `(tree, parent=S, identity, author_date=D, committer_date=D, message(T,S))` is a pure function of `T`. Therefore `regenerate(T)` is referentially transparent and yields one fixed SHA; re-running `T` (e.g., a `workflow_dispatch` retry or a replayed release) reproduces it exactly (c-002). Different releases produce different SHAs (different parent and tree), which is correct.

> **Precondition — tag immutability (CV-005 / IN-007).** Referential transparency holds only if the mapping `T → S` is **fixed**: the proof is "a pure function of `T`" *given that `T` resolves to the same source commit `S` on every run*. If a maintainer **force-moves** a `v*` tag to a different commit (bad practice, but not prevented by GitHub on a non-protected tag), then `regenerate(T)` correctly produces a *different* SHA for the new target — the function is still pure in `(T → S)`, but "same tag name" no longer implies "same SHA". This is the intended behaviour (the skeleton tracks whatever the tag points at), but it means the **build-provenance attestation** binding the published tip SHA ([ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) D4) — not the tag name — is the durable integrity reference. Treat release tags as immutable; the integrity monitor compares against the SHA recorded at publish time, so a silently force-moved tag surfaces as a monitored mismatch rather than as undetected drift.

**Stub determinism constraint (c-001/c-006):** the stub `projects/README.md` MUST be static content. Any generated date, version string, or run ID inside it changes the tree and breaks reproducibility. Authoring is STORY-002; this ADR fixes only its determinism property.

**Force-push semantics (Phase-2 dedicated-repo model — CC-005 correction).** Per the amendment header and [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) D1/D3, the regenerated tip is force-pushed **cross-repo to the dedicated repo's default branch**, NOT to an in-repo `cowork-skeleton` branch. The correct command is `git push --force <dedicated-remote> HEAD:<default-branch>` (e.g. a remote pointing at `geekatron/jerry-claude-plugin`) authenticated with the **GitHub App installation token / single-repo deploy key** (ADR-PROJ031-003 D3) — **never** the source `GITHUB_TOKEN`, which cannot push cross-repo. (The earlier `git push --force origin HEAD:cowork-skeleton` same-repo form is superseded.) It replaces the dedicated default-branch ref wholesale each release — structurally analogous to the `mkdocs gh-deploy --force` precedent, but targeting a separate repo. No per-release commits accumulate; the branch is always `main`-history + 1 (Option A) or a single orphan commit (Option B fallback).

### Tamper-Evidence and Supply-Chain Integrity

*(REM-013 / SM-001 / RT-02.)* Because `regenerate(T)` is a **pure function** of the release tag `T`, the expected `cowork-skeleton` tip SHA for any release is **independently computable** by re-running the generator against the same tag. This yields a strong supply-chain property **without** commit signing:

- **Tamper-evident by construction, on a NON-FORGEABLE value (IT3-004).** Any in-place modification of the published branch — a malicious direct push, a corrupted regeneration, a man-in-the-middle rewrite — changes the **tip SHA** (`git rev-parse cowork-skeleton`, equivalently the tip tree hash `…^{tree}`) away from the deterministically expected value and is **detectable** by anyone who recomputes it. The tip SHA is **non-forgeable**: git derives it from the actual published tree+parent+metadata, so to make a tampered tree present the expected SHA an attacker would need a hash preimage collision against content they do not control — infeasible. This is the load-bearing integrity anchor. **Contrast the `Source-Commit:` trailer, which is FORGEABLE** — it is free-form commit-message text any push actor can set to the correct value while shipping a different tree; the trailer can detect *lazy* staleness (CI never regenerated) but **cannot** detect targeted tampering, and MUST NOT be used as the integrity comparator (this is why [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md)'s D7 monitor compares the tip SHA via `gh attestation verify`, not the trailer).
- **Why this substitutes for a signature.** We deliberately do **not** GPG-sign the regeneration commit (a timestamped signature varies per run and would break the bit-identical SHA — see the Signature row above). Determinism gives a *verifiable, reproducible* integrity check that a per-run signature cannot: a signature proves *who* committed, but the deterministic SHA proves *exactly what* the tree-and-parent must be for a given release.
- **Provenance is defense-in-depth, NOT the integrity anchor.** Maintainer/CI provenance is additionally (not primarily) supported by the `github-actions[bot]` identity and the parent chain to the release commit (which itself lives on the ruleset-protected `main`). After this remediation the parent chain is **demoted** from "integrity anchor" to a *cheap second check* — a verifier MAY run `git merge-base --is-ancestor <skeleton-parent> main` to corroborate lineage — but the deterministic tip SHA carries the integrity guarantee on its own, which is why the orphan fallback (Option B, no parent chain) is integrity-neutral.
- **Operationalization — CONTINUOUS integrity monitoring, not an in-CI "pre-publication" gate (IT3-002).** A git branch is installable the **instant** it is pushed, so any integrity check placed *inside* the generating job after the force-push would merely assert the SHA that same job just created (tautological) and could not protect against a *later* direct push to the unprotected branch. The sound model is **publish-then-assert, asynchronously**: (1) `cowork-skeleton.yml` **publishes** the expected deterministic SHA for the release to a durable, off-branch, protected surface (the GitHub Release notes for the tag); (2) an **independent, continuously-running** integrity monitor (scheduled at least daily, plus an event-driven fast path) later retrieves that published SHA and asserts `git rev-parse cowork-skeleton == <published SHA>`, alerting and (recommended) auto-reverting on mismatch. This makes the unprotected-branch posture safe against the direct-write threat (RT-01) by **bounded-window detection** (not prevention). **Phase-2 supersession (consistency):** the two specific mechanics named in this bullet — publishing the expected SHA to **GitHub Release notes** and the **event-driven fast path** — are **RETIRED**. Under the confirmed dedicated-repo model the integrity anchor is a GitHub immutable-release + Sigstore build-provenance attestation, the dedicated-repo default branch is *protected* (prevention, not just detection), and the monitor is a **scheduled (≤ 6 h) read-only poll from the source repo** with no event-driven leg. The publish-then-assert-asynchronously *concept* remains valid; only the anchor and the monitor topology changed. The full architecture, automation mode, and detection SLA are owned by **[ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md)** (D4 attestation anchor; D7 monitor topology), which supersedes the ADR-PROJ031-002 §Continuous Integrity Monitoring design referenced here.

---

## L2: Architectural Implications

1. **The skeleton joins an established operational pattern, minimizing novel risk.** `gh-pages` and the `release.yml` artifact flow already exercise force-pushed / tag-driven derived outputs. Adopting the same conventions (force-push, `github-actions[bot]` identity, SHA-pinned actions, `concurrency` guard) keeps the C4 reviewer surface small and reuses battle-tested behavior (research §L2 ¶1).
2. **Provenance-vs-clone-weight is the one genuine, testable design tension — and Option A makes the weight grow.** Because install copies the **working tree** (history weight affects only clone bandwidth) and the 120s git timeout is the real clone-weight risk, the clean decision is **A by default, B behind a documented flag**. Under A the weight grows monotonically per release, so the choice is governed not by a one-shot check but by **continuous telemetry** with an early-warning band (~150 MB / ~40 s) ahead of the hard trigger (>60 s clean-clone or >250 MB pack on the 10 Mbps reference network). Crucially, this remediation **decoupled integrity from provenance** — the deterministic tip SHA, not the parent chain, is the integrity anchor (IT3-002/IT3-004) — so the flip to orphan is now **integrity-neutral** and can be taken purely on weight grounds without weakening the supply-chain story (research §L2 ¶4; OQ-2).
3. **Determinism makes the acceptance test meaningful.** A non-deterministic generator would make the ~1,417 file-count assertion flaky and the C4 supply-chain story weak. Pinned-metadata idempotency turns "the skeleton matches release `vX`" into a reproducible, verifiable claim.
4. **The strategy's validity rests on an external, still-unverified assumption.** Anthropic's public plugin docs document **no** file-count limit; the ~5,000 ceiling is a CoWork/Claude-Desktop runtime constraint (research §Q3 finding 3; §L2 ¶5; OQ-1/R-001). If CoWork instead counts a local working directory (`.venv` ≈ 24,636 files), branch-stripping is the wrong lever and the solution pivots to local-plugin configuration. This is honestly the top residual risk and is **not** resolved by this ADR; it is delegated to a mandatory requirements-level acceptance test before Phase 5. That test MUST be **multi-dimensional** — measuring tracked file count **and** compressed pack size (MB) **and** clone time (s) — because the ceiling could be size- or time-based rather than file-count-based (IN-001); a file-count-only check would falsely "pass" a size/time failure and must not be the sole gate.
5. **Forward evolution is incremental.** `tests/` is already stripped as of the Phase-2 amendment; if clone weight or the file-count margin tightens further, the same generation job can additionally strip non-product fixtures (`skills/transcript/test_data/` ~908 KB blobs, `docs/archive/`) behind a flag (research §L2 ¶7; R-002) — none of which is needed today, and the remaining margin is comfortable (~1,417 ≪ 5,000).
6. **The distribution's headline value rests on a load-bearing, currently-UNVERIFIED CoWork behavior (PM-001 / CV-001 — Phase-5 blocker).** The promise that the skeleton is "automatically in sync when a new Jerry ships" (and STK-002's "automatically in sync... without manual repository surgery") assumes that **updating the dedicated repo's default branch propagates to ALREADY-INSTALLED users.** Only CoWork's *install-time* behavior is confirmed (research §`cowork-plugin-install-mechanism`); its **update** behavior for existing users is an **unexamined black box.** If CoWork caches the plugin tree at install and refreshes only on explicit reinstall, a user-initiated "check for updates", or an unknown internal schedule, then every user runs the skeleton version from their first install date — potentially many releases stale — and "automatically in sync" is **false for existing users from day one** (the CI regeneration + cross-repo push work perfectly; the last mile CoWork→session is the gap). **Per P-022 this ADR does NOT assert that sync works for already-installed users — it is explicitly an unverified, load-bearing assumption.** It is bound to a **hard Phase-5 gate, G-update**, in the shared [ADR-PROJ031-003 Phase-5 Validation Gate Set](./ADR-PROJ031-003-credential-protection-supply-chain.md#phase-5-validation-gate-set-go-live-authorization): before go-live, empirically verify that a force-push to `geekatron/jerry-claude-plugin` reaches an already-installed user's session within a bounded window; **if CoWork caches at install, an alternate update path (or a documented manual-update procedure) is REQUIRED** and the "automatically in sync" claim must be re-scoped. The concrete fallback paths and the decision to evaluate G-update at **Phase-5 entry** are designed in [G-update Fallback Architecture and Phase-5 Entry Gating](#g-update-fallback-architecture-and-phase-5-entry-gating) below. nse-requirements adds the stated-assumption REQ / OQ-048.

---

## G-update Fallback Architecture and Phase-5 Entry Gating

*(R-002 — DA-001 / PM-001 / CV-001 / IN-001 / CC-002. This section designs the response to the case where CoWork does NOT propagate updates to already-installed users. Per P-022 it is an honest MITIGATION for an unverifiable assumption — it does not, and cannot, restore automatic propagation; it converts a silent-staleness failure into a visible, user-actionable one.)*

### Platform-bug blocker (P-022 — stated plainly)

As of 2026-06-29 the live test that **G-update** requires **cannot be performed by anyone** — an Anthropic CoWork **platform-UI change removed the marketplace "+"/add control**, so there is currently no path to install the dedicated repo into a live client and observe whether a force-push reaches an already-installed session. G-update is therefore **blocked on an external platform defect, not on our effort or design completeness.** This is decisive for the posture of this section: because we **cannot prove** propagation works (and cannot prove it fails), the fallback below is **not contingency-only — it is the required interim mitigation.** We design for the un-provable case rather than asserting the headline value. The two former-"OR a manual procedure is documented" half-sentences in the gate text are insufficient design content for a C4 deliverable; the candidates below supply it.

### Fallback candidates (≥2 required; three designed, A+C recommended)

> Status of every candidate: **Designed — operational validation pending [G-update]** per the [ADR-PROJ031-003 Claim-Status Convention](./ADR-PROJ031-003-credential-protection-supply-chain.md#claim-status-convention-p-022--foundational). Fallbacks A and C can be **built and unit-tested inside Jerry today** (they only read a version and emit a signal); what remains un-provable until the platform bug is fixed is whether they are *needed* — i.e. whether CoWork actually caches.

**Fallback A — Session-start version-check skill (in-skeleton "stale → reinstall" notice).**
- **Mechanism.** A small skill/hook shipped *in* the skeleton compares the installed skeleton's embedded version against the latest `geekatron/jerry` release and, when they differ, surfaces a non-blocking session-start notice: *"Jerry skeleton `<installed>` is stale; latest is `<current>` — reinstall to update."* The installed version is read from a **static version sentinel** baked into the skeleton (the `Source-Tag` / full-40-char `Source-Commit` already in the deterministic commit, surfaced into a `projects/`-stub or `.claude/` sentinel file); the latest version is read from the public GitHub releases API.
- **Requires.** A static version sentinel in the generated tree (it **MUST** be static content embedding the `Source-Tag` — never a build timestamp — to preserve the [determinism contract](#regeneration-commit-determinism), c-001); outbound GitHub API reachability from the user session; one hook/skill added to the retained surface (so it is also in D8's content-scan scope).
- **UX.** Passive, non-blocking banner/statusline at session start; the user reinstalls at their discretion. No silent staleness — the user always knows their version is behind.
- **Limits.** **Detection-only** — it informs, it cannot update anything. Depends on network egress from the CoWork sandbox. Does not help a user who never starts a fresh session. The sentinel must stay inside the determinism contract.

**Fallback B — Documented manual re-install / update procedure (WS-4 how-to).**
- **Mechanism.** A user-facing "How to update Jerry in CoWork" Diataxis how-to giving the explicit steps to refresh/re-install the plugin from the dedicated repo.
- **Requires.** WS-4 documentation authored before go-live; **a stable, documented CoWork re-install path — which is itself currently unknowable because of the same removed-UI platform bug**, so the exact steps must be finalized once the marketplace UI is restored.
- **UX.** Fully manual; the user follows the runbook when they choose to update.
- **Limits.** Relies on user initiative (most users will not re-install proactively); the precise UI steps cannot be written today; this is the minimum-viable backstop and on its own defeats "automatically in sync" — STK-002 must be re-scoped to *"current at install; manual refresh thereafter."*

**Fallback C — Versioned-release + changelog notification path.**
- **Mechanism.** Pair each skeleton release with the immutable versioned release already produced by [ADR-PROJ031-003 D4](./ADR-PROJ031-003-credential-protection-supply-chain.md#d4-integrity-anchor--immutable-release-attestation) plus a changelog / "what changed" surface (and optionally an opt-in notification), giving users an authoritative out-of-session signal that a newer skeleton exists — complementing Fallback A's in-session check.
- **Requires.** The immutable-release publishing already in the pipeline (reused, near-zero added cost); a changelog generation step; optionally a notification channel.
- **UX.** Out-of-session signal (release feed / changelog) the user can watch or subscribe to.
- **Limits.** Still a notification, **not** propagation — the user must act to re-install; effectiveness depends on users watching the channel.

**Selection.** A and C are complementary (in-session detection + out-of-session signal) and are the **recommended pair**; B is the minimum-viable backstop and is required regardless. **None restores automatic propagation.** Per P-022 these are mitigations for an unverifiable assumption, not a substitute for verifying it.

### G-update is a Phase-5 ENTRY gate (G-update-pre), not an exit gate

**Decision (sequencing).** Applying the **same precedent this ADR already uses for machine-checkable load-bearing assumptions** — verify *before* the phase that depends on the assumption, not after — and per **P-020 (user authority)**, the G-update decision is moved to **Phase-5 ENTRY** (gate **G-update-pre**). Before any Phase-5–8 CI implementation investment, the team attempts the empirical propagation test and presents the user an explicit go/no-go:

- **PASS** (propagation confirmed within a documented window): proceed with the continuous-delivery model.
- **FAIL** (caching confirmed) **or BLOCKED** (as today — the test is impossible due to the platform-UI defect): the user chooses, per P-020, between **(i)** proceeding with a designated fallback (A+C recommended) and a re-scoped STK-002, or **(ii)** pausing Phases 5–8 pending the platform fix / Anthropic engagement.

**P-020 rationale.** Placing this at *entry* means a propagation failure can **redirect the project before weeks of Phases 5–8 CI work are sunk**, rather than after — the user's decision shapes the implementation investment instead of the investment shaping (and pressuring) the decision. The empirical test costs at most a few controlled hours; the implementation it gates costs weeks. Because the test is **currently blocked by the platform bug**, the only interim entry-gate outcomes available are (ii) or (i)-with-fallback; **go-live on the unqualified "automatically in sync" claim is not authorized** while G-update remains unproven. ADR-PROJ031-003's [Phase-5 Validation Gate Set](./ADR-PROJ031-003-credential-protection-supply-chain.md#phase-5-validation-gate-set-go-live-authorization) carries the mirror (G-update annotated as a Phase-5 **entry** decision); nse-requirements mirrors G-update-pre into the Phase-5 authorization checklist and strengthens REQ-054 / OQ-048 with the fallback-selection acceptance criterion.

---

## Consequences

### Positive

1. **Auditable provenance** — the skeleton commit's parent is the exact `v*` release commit; `git log` and `diff against main` work, supporting the C4 supply-chain narrative.
2. **True, verifiable idempotency** — pinned metadata yields a bit-identical SHA on re-run; release replays and `workflow_dispatch` retries cannot drift the artifact.
3. **Stable acceptance test** — the deterministic tree makes the ~1,417 file-count assertion reproducible.
4. **Low complexity and high maintainability** — four plain git commands, zero new tooling, reusing the proven `gh-pages` force-push pattern.
5. **No history accumulation** — wholesale force-push keeps the branch at `main`-history + 1 commit.
6. **Full plugin surface preserved** — the validated strip-set (`projects/ tests/ skills/.graveyard/ .github/`) removes only non-distribution trees, leaving the entire [Canonical Plugin-Retention Surface](#canonical-plugin-retention-surface) (incl. `.claude-plugin/marketplace.json`, `commands/`, `src/`, `schemas/`) plus its runtime deps (`pyproject.toml`, `uv.lock`) intact — **empirically confirmed**: the 1,399-file tree validated and installed cleanly on Claude Web.
7. **Tamper-evident distribution without signing** — the deterministic tip SHA is independently recomputable on a non-forgeable value, so any in-place modification of the published branch is detectable by re-running the generator (see [Tamper-Evidence and Supply-Chain Integrity](#tamper-evidence-and-supply-chain-integrity) and ADR-PROJ031-003's D4 attestation anchor + D7 continuous integrity monitoring).
8. **The distribution model is EMPIRICALLY VALIDATED for the install path (2026-07-02)** — the technique produced a real plugin that the marketplace synced (`last_synced_sha`), validated, and installed on Claude Web. This retires the *install-time* leg of the ~5,000-file / installability risk (R-001) for the dedicated-repo model. **Honestly scoped (P-022):** it validates *fresh install* only — **not** update-propagation to already-installed users (G-update, still open), and not hook *execution* in-sandbox (hooks fail-open; see c-008 residual).
9. **Duplicate-skill and CI-loop failure modes are now gated, not just fixed** — fix-cycle #1 (duplicate skill name) becomes a fail-closed generation gate (c-007), and fix-cycle #2 (`.github/` CI loop) is closed by the validated strip; both are converted from one-time manual fixes into durable, deterministic guards.

### Negative

1. **Clone weight under full provenance grows MONOTONICALLY** — `fetch-depth: 0` carries `main`'s history into the skeleton `.git`, and every release adds to it (~2 MB/release empirically); on slow networks this risks CoWork's 120-second git-operation timeout (`CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`). A single Phase-2 snapshot cannot certify a growing quantity (IN-002/FM-007). *Mitigation (continuous, not single-shot):* the R-001 artifact records the baseline pack size + clone time, AND `cowork-skeleton.yml` emits per-release weight (hard-fail at > 250 MB), AND the continuous integrity workflow records weight every cycle with an **early-warning band (~150 MB / ~40 s, ≈60% of trigger)** that prompts a *proactive* flip to Option B. *Measurable hard fallback trigger:* switch to Option B (orphan) when a clean full-provenance clone exceeds **60 s** wall-clock **or** the compressed pack exceeds **250 MB**; post-IT3-004 the flip is **integrity-neutral** (tamper-evidence does not depend on the parent chain). *Further mitigation:* optional large-blob stripping (R-002).
2. **Idempotency is discipline-dependent** — bit-identical reproduction requires pinning parent, identity, both dates, and the message, and **not** signing. A single un-pinned input (e.g., default "now" dates) silently breaks it. *Mitigation:* encode all metadata in the generation script; add a CI assertion comparing the regenerated SHA where feasible.
3. **Force-push is destructive** — any contributor who mistakes `cowork-skeleton` for a development branch will have work overwritten on the next release. *Mitigation:* documentation + the dedicated-repo protection posture ([ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) D2 — org-level ruleset, CI sole bypass actor); never advertise it as a dev/PR target.
4. **Strategy depends on an unverified external limit (R-001)** — if the ~5,000-file CoWork limit is mischaracterized, the entire branch-stripping approach may not deliver installability. *Mitigation:* mandatory requirements-level acceptance test (reproduce the limit on a clean clone vs. a dev checkout) before Phase 5; owned by nse-requirements; consolidated as gate **G-headroom**.
5. **The "automatically in sync" value depends on an unverified CoWork update-propagation behavior (PM-001/CV-001)** — updating the dedicated repo's default branch may NOT reach already-installed users if CoWork caches the plugin tree at install. Honestly stated (P-022): this is a **load-bearing assumption, not a verified property**, and the headline distribution value is unproven for existing users — and **currently un-testable**, because the live test is blocked by the removed-marketplace-UI platform defect. *Mitigation:* the [G-update Fallback Architecture](#g-update-fallback-architecture-and-phase-5-entry-gating) — designed fallback update paths (in-skeleton stale-version notice; versioned-release/changelog signal; manual re-install how-to) plus **G-update-pre as a Phase-5 ENTRY decision** (P-020) so a propagation failure redirects the project before Phases 5–8 are sunk. The claim is re-scoped, never asserted. See [L2 §6](#l2-architectural-implications) and the [ADR-PROJ031-003 Phase-5 Validation Gate Set](./ADR-PROJ031-003-credential-protection-supply-chain.md#phase-5-validation-gate-set-go-live-authorization).

### Neutral

1. The skeleton is a **third** CI-owned derived branch alongside `gh-pages` and the release artifact flow — consistent with existing patterns, but one more branch to operate and reason about.
2. The orphan fallback (Option B) is pre-designed but dormant; selecting it later is a documented one-line trade-off, not a redesign.

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| CoWork does NOT propagate updates to already-installed users (PM-001/CV-001); "automatically in sync" is false for existing users | MED | HIGH (every user silently runs a stale Jerry; new skills/agents referenced by H-22 don't exist) | **Load-bearing UNVERIFIED assumption (P-022 — not asserted as working), and currently UN-TESTABLE: the live test is BLOCKED by the removed-marketplace-UI platform bug.** Treated as a **Phase-5 ENTRY** decision (**G-update-pre**, P-020) so a failure redirects before Phases 5–8 are sunk; designed **fallbacks** (A in-skeleton stale-notice + C versioned-release/changelog, with B manual how-to as backstop) convert silent staleness into a visible, user-actionable signal — see [G-update Fallback Architecture and Phase-5 Entry Gating](#g-update-fallback-architecture-and-phase-5-entry-gating). Mirrored in the [ADR-PROJ031-003 gate set](./ADR-PROJ031-003-credential-protection-supply-chain.md#phase-5-validation-gate-set-go-live-authorization). nse-requirements: stated-assumption REQ + OQ-048 + fallback-selection acceptance criterion. |
| ~5,000-file (or size/time-based) CoWork limit is undocumented/unverified (R-001); strategy may not yield installability | MED | HIGH | Mandatory **multi-dimensional** acceptance test before Phase 5 (nse-requirements, REQ-034), consolidated as gate **G-headroom** ([ADR-PROJ031-003 gate set](./ADR-PROJ031-003-credential-protection-supply-chain.md#phase-5-validation-gate-set-go-live-authorization)): measure tracked file count **and** compressed pack size (MB) **and** clone time (s) on a clean clone vs. dev checkout — a file-count-only check cannot falsify a size/time-based limit (IN-001/FM-062). |
| Clone weight (full history) grows monotonically and trips the 120s git timeout on slow networks (IN-002/FM-007) | LOW–MED (rising over releases) | MED | **Continuous monitoring (not single-shot):** per-release weight emit (hard-fail > 250 MB) + scheduled telemetry with an **early-warning band (~150 MB / ~40 s)**; on warning, execute the pre-designed **integrity-neutral** flip to Option B (orphan); hard trigger > 60 s clean-clone or > 250 MB pack on a 10 Mbps reference link; optionally strip large blobs (R-002); document `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`. |
| Idempotency drift from un-pinned commit metadata | LOW | MED | Pin all metadata in the generation script; CI SHA assertion; do not GPG-sign. |
| Empty-dir loss: stub ships without a tracked file → `projects/` vanishes on clone → `jerry projects list` `RepositoryError` | LOW | HIGH | Stub MUST contain tracked `projects/README.md` sentinel (c-006, STORY-002). |
| Stub content includes a generated value → tree non-determinism | LOW | MED | Enforce static stub content (c-001); review in STORY-002. |
| Retained archived/vendored skill re-introduces a **duplicate skill name** → marketplace rejects the plugin (**OBSERVED** 2026-07-02, fix-cycle #1) | LOW (post-gate) | HIGH (whole-plugin install failure) | Validated strip removes `skills/.graveyard/`; **fail-closed no-duplicate-skill-names generation gate (c-007)** catches any future recurrence before push. nse-requirements REQ + nse-architecture gen-step + eng-devsecops CI gate. |
| Retained framework CI (`.github/`) executes in the dedicated repo → gh-pages/`docs.yml` loop (**OBSERVED** 2026-07-02, fix-cycle #2) | LOW (post-strip) | MED (CI loop / loop-safety) | `.github/` is in the validated strip-set; eng-architect mirrors the loop-safety finding into the STRIDE model; retention audit asserts no `.github/` in the tip tree. |

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) | AMENDED_BY | Phase-2 architecture of record. Replaces the in-repo `cowork-skeleton` branch with the dedicated `geekatron/jerry-claude-plugin` repo, extends the strip set to `tests/`, and owns the push credential (D3), dedicated-repo protection (D2), integrity anchor (D4), and monitor topology (D7). |
| [ADR-PROJ031-002](./ADR-PROJ031-002-ci-token-push-strategy.md) | SUPERSEDED_BY ADR-PROJ031-003 | (Historical) Selected the source `GITHUB_TOKEN` push credential and the in-repo unprotected-branch posture. **Superseded in full by ADR-PROJ031-003** before AG-03 approval; retained as background only — MUST NOT be implemented as written. |
| STORY-001 (Skeleton Regeneration Script) | REALIZED_BY | Implements the four-command generation + deterministic commit. |
| STORY-002 (Minimal `projects/` Stub and README) | REALIZED_BY | Authors the static sentinel stub constrained here. |
| STORY-003 (Skeleton Validation and Acceptance) | VERIFIED_BY | File-count (~1,417) and plugin-load acceptance, incl. the R-001 limit-reproduction test. |
| TASK-002 (Regenerate-and-Push Job) | REALIZED_BY | CI job that runs the generation and force-push. |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | [`../research/phase1-skeleton-ci-research.md`](../research/phase1-skeleton-ci-research.md) — §Q1 Skeleton Generation Technique; §L2 ¶4 (provenance vs clone-weight); Recommendations Q1 | PRIMARY (internal) | Decisive framing, option comparison, idempotency steps. |
| 2 | [`../research/phase1-skeleton-ci-research.md`](../research/phase1-skeleton-ci-research.md) — §Q3 (install clones tip tree); §Q4 (empty-dir sentinel) | PRIMARY (internal) | Plugin-install compatibility; stub necessity. |
| 3 | [`../PLAN.md`](../PLAN.md) — Confirmed Decisions 1 & 2 | PRIMARY (internal) | Agreed derived-branch + regenerate-never-merge model. |
| 4 | git-scm — `git rm`, `git checkout --orphan`, clone materializes tip working tree | PRIMARY (vendor) | Established semantics underpinning Options A/B/C. |
| 5 | git-filter-repo (newren/git-filter-repo) | PRIMARY (vendor) | Basis for rejecting Option C (non-idempotent history rewrite). |
| 6 | Anthropic — "Create and distribute a plugin marketplace" (install copies whole repo to cache; 120s git timeout; no documented file limit) | PRIMARY (vendor) | Install-time tree materialization; clone-weight timeout; R-001 gap. |
| 7 | Repo `.github/workflows/docs.yml` (`mkdocs gh-deploy --force`, bot identity, `concurrency`) | PRIMARY (first-party) | Force-push precedent reused by this strategy. |

---

## Mirror Hand-Off (nse-requirements / eng-architect)

### Phase-3 mirror (2026-07-02 — live-install validation; MIRROR AFTER this owner)

The retention-surface refinement + gate below are owned here (ps-architect / ADR-PROJ031-001). Downstream owners mirror into their artifacts; the core architecture is unchanged (P-020).

- **eng-architect (STRIDE loop-safety + retention):** mirror fix-cycle #2 — a retained **`.github/`** ran framework CI (`docs.yml` → gh-pages) inside `geekatron/jerry-claude-plugin`, a **loop-safety violation**; add `.github/` removal to the STRIDE pipeline/loop-safety controls and reflect the **validated strip-set** (`projects/ tests/ skills/.graveyard/ .github/`) in the retention description. Confirm the cross-repo push (CC-005) is unchanged.
- **nse-requirements (REQ-002/003 strip-set + NEW dup-skill-gate REQ + R-001 evidence):** update the strip-set requirements (REQ-002/003) to the **validated `projects/ tests/ skills/.graveyard/ .github/`**; add a **NEW requirement + acceptance criterion for the fail-closed no-duplicate-skill-names gate** (c-007) — SKILL.md names unique in the tip tree, build fails on duplicate; record the **R-001 install-path evidence** (1,399-file tree installed on Claude Web 2026-07-02) while keeping G-update (update-propagation) OPEN and un-satisfied. Add `pyproject.toml`+`uv.lock` to the retained runtime-dependency set (c-008).
- **nse-architecture (gen-design strip-set + gate step):** update the generation design to the validated strip-set and **insert the no-duplicate-skill-names check as an explicit generation step** between strip and force-push (enumerate SKILL.md → resolve names → abort-no-push on duplicate); fold in the recommended additional strips (`docs/`, `mkdocs.yml`/`CNAME`/`.nojekyll`, `scripts/`, dev/governance cruft, −285 files → ~1,114) behind the "no retained file references a stripped path" audit.
- **eng-devsecops (CI dup-skill/retention gate):** add the **CI enforcement gate** for c-007 (duplicate-skill-name = fail-closed) and a retention assertion (`.github/`, `skills/.graveyard/` absent from the tip tree; `src/`+`pyproject.toml`+`uv.lock` present); add the recommended **post-install hook-smoke check** (`uv run jerry hooks session-start` returns non-empty) to catch the fail-open src/ regression.

### Iteration-005 mirror (carried forward)

This iteration-005 revision changes two things downstream owners must mirror:

**nse-requirements must mirror:**
1. **G-update (PM-001/CV-001/CC-002 — UPDATED R-002):** keep the **stated-assumption REQ-054 + OQ-048** (CoWork update-propagation-to-installed-users is UNVERIFIED and **currently un-testable** due to the removed-marketplace-UI platform bug); mirror **G-update as a Phase-5 ENTRY gate (G-update-pre)**, a user go/no-go before Phases 5–8 CI investment (P-020); add an acceptance criterion that REQ-054 is satisfied only by (a) empirical PASS, or (b) a **user-approved fallback selection** from the [G-update Fallback Architecture](#g-update-fallback-architecture-and-phase-5-entry-gating) (A in-skeleton stale-notice / B manual how-to / C versioned-release-changelog) **with STK-002 re-scoped** — never by silent deferral.
2. **REQ-010 (R-008 / FM-030):** tighten the acceptance criterion to derive the required-present set **from `.claude-plugin/plugin.json`** (exact declared paths, not a `skills/*/agents/*.md` glob) so new/nested agents cannot be silently excluded.
3. **G-headroom (R-001 / FM-062 / IN-001):** keep the R-001 gate **multi-dimensional** (file count **+** pack size MB **+** clone time s) and **remove any "MAY defer dimension (d)"** deferral clause (PM-002) — the live-CoWork dimension is mandatory before go-live.
4. All gates are consolidated in the shared [ADR-PROJ031-003 Phase-5 Validation Gate Set](./ADR-PROJ031-003-credential-protection-supply-chain.md#phase-5-validation-gate-set-go-live-authorization); mirror it as the Phase-5 authorization checklist, including the new **`phase5-gate-evidence.md`** proof-of-execution artifact (R-005, owned in ADR-PROJ031-003).

**eng-architect must mirror:**
1. **CC-005 (force-push):** the cross-repo dedicated-repo push model (`git push --force <dedicated-remote> HEAD:<default-branch>` with the App token/deploy key, never source `GITHUB_TOKEN`) is the canonical push — ensure the STRIDE pipeline/CI-01 description shows the cross-repo target, not an in-repo `cowork-skeleton` branch.

> The generation *technique*, determinism contract, and deterministic-SHA tamper-evidence in this ADR are **unchanged** by this revision (P-020) — only the update-propagation honesty, the Phase-5 gate references, and the stale force-push command were corrected.

---

## Approval and PS Integration

| Action | Detail | Status |
|--------|--------|--------|
| Approval gate | **AG-02** — approve the derived-branch strategy (rm `projects/`, stub injection, force-push regeneration, determinism approach) | PENDING (user) |
| Exploration entry | `ps-architect-001` (Phase 1 — Requirements & Architecture) | Done |
| Entry type | DECISION | Done |
| Artifact link | `link-artifact` to this file under PROJ-031 | PENDING (orchestrator; this agent is scoped to write only within `decisions/`) |

---

**Generated by:** jerry:ps-architect (ps-architect-001)
**Format:** Michael Nygard's ADR Format (2011)
**Self-review:** S-010 (Self-Refine) and S-003 (Steelman of Options B and C) applied before finalization per H-15/H-16.
**Iteration 2 (QG-1 C4 remediation, 2026-06-26):** REM-009 (full 40-char SHA in commit subject + explicit `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` pinning — FM-009/FM-010); REM-013 (Tamper-Evidence and Supply-Chain Integrity subsection — SM-001/RT-02); REM-016 (tag-name sanitization security note — RT-04); REM-008 (Canonical Plugin-Retention Surface — this ADR owns the list; added `marketplace.json`, `src/`, `schemas/`, `commands/`); R-001 clone-weight (measurable >60 s / >250 MB fallback trigger; multi-dimensional verification — IN-001). S-010 self-refine re-applied.
**Iteration 3 (QG-1 C4 remediation, 2026-06-26):** **IT3-005** — fixed the Regeneration pseudocode for the `workflow_dispatch` path (event-discriminated `TAG` resolution covering `push:tags`, `inputs.target_tag`, and blank-input fallback; CC-002), extended the RT-04 allow-list to `inputs.target_tag` with a syntax-vs-provenance scope boundary (RT-003, provenance deferred to Phase-2 STRIDE), and added the tag-immutability precondition to the idempotency proof (CV-005/IN-007). **IT3 clone-weight** — kept Option A as default but converted the single-shot R-001 gate into **continuous** clone-weight monitoring with a ~150 MB/~40 s early-warning band and a pre-designed, now **integrity-neutral** orphan flip (IN-002/FM-007); steelmanned and recorded the orphan-default counterfactual. **IT3-002/IT3-004 coupling** — demoted the parent chain from integrity anchor to defense-in-depth; marked the tip SHA as the **non-forgeable** comparator and the `Source-Commit` trailer as forgeable; replaced the unsound in-CI "pre-publication integrity gate" reference with ADR-PROJ031-002's asynchronous continuous integrity monitoring. S-010 self-refine re-applied.
**Iteration 4 (Phase-2 RE-ADVERSARY remediation, 2026-06-29):** **A-5 / A-6** — corrected the [Canonical Plugin-Retention Surface](#canonical-plugin-retention-surface) body to state `tests/` is **STRIPPED** (per the Phase-2 amendment / [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) D1), removed `tests/` from both the "retained today" set and the "future optional strip" set, and updated the post-strip file count from ~1,744 to **~1,417 throughout** (L0, Context, c-001, c-003, retention-surface intro + body, commit-message template, L2 §3/§5, Consequences §Positive 3, Related Decisions). The generation technique, determinism contract, and tamper-evidence are UNCHANGED. S-010 self-refine re-applied.
**Iteration 5 (owner-first remediation of the 0.724 blind tournament, 2026-06-29):** **CC-005** — corrected the stale `git push --force origin HEAD:cowork-skeleton` same-repo command to the cross-repo dedicated-repo push model (App token/deploy key per ADR-PROJ031-003 D3). **PM-001/CV-001** — added the CoWork update-propagation-to-installed-users **load-bearing UNVERIFIED assumption** (L0 caveat, L2 §6, Negative §5, Risks row) bound to the hard Phase-5 gate **G-update**; per P-022 the "automatically in sync" value is NOT asserted for existing users. Referenced the shared **Phase-5 Validation Gate Set** (G-update + G-headroom) from [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md#phase-5-validation-gate-set-go-live-authorization) and added a **Mirror Hand-Off**. The generation technique, determinism contract, and tamper-evidence are UNCHANGED (P-020). S-010 self-refine re-applied.
**Iteration 7 (owner-first FIXABLE-NOW remediation of the iteration-006 tournament, 0.82 REVISE, 2026-06-29):** **R-001 (CV-006)** — reconciled the monitor-operation contradiction: ADR-PROJ031-003 D7 integrity monitor is read-only (`git ls-remote`/`gh api`, no clone); the clone-weight telemetry is now a separate timed-reference-clone measurement step, consistent across both ADRs. **R-002 (DA-001/PM-001/CV-001/IN-001/CC-002) — priority** — added the [G-update Fallback Architecture and Phase-5 Entry Gating](#g-update-fallback-architecture-and-phase-5-entry-gating) section: the platform-bug blocker (live test impossible — removed marketplace "+" UI), three designed fallback candidates (A in-skeleton stale-notice, B manual how-to, C versioned-release/changelog) each with mechanism/requires/UX/limits, and the decision to make **G-update a Phase-5 ENTRY gate (G-update-pre)** with its P-020 rationale; cross-referenced from L0, L2 §6, Negative §5, Risks, and the Mirror Hand-Off. **R-008 (FM-030)** — added the deterministic, drift-proof retention-surface verification rule (denylist strip + `plugin.json`-derived completeness check). The generation technique, determinism contract, tamper-evidence, and the AG-02 core strategy are UNCHANGED (P-020) — claims were sharpened and fallbacks/sequencing added, not the architecture changed. S-010 self-refine re-applied.
**Iteration 8 (Phase-3 live-install validation, 2026-07-02):** Recorded the **empirically-validated** dedicated-repo install (`geekatron/jerry-claude-plugin`, default branch = skeleton, installed on Claude Web; marketplace synced `last_synced_sha`). **Positive-retention reframe (R-001):** distribution = plugin surface (`plugin.json`/`marketplace.json`) + runtime deps, not "`main` minus N dirs". **Validated strip-set** expanded from `projects/`+`tests/` to **`projects/ tests/ skills/.graveyard/ .github/`** (1,399 files) — driven by two live fix cycles: fix-#1 **duplicate skill name** (`.graveyard/worktracker` vs live `worktracker`) marketplace rejection (BLOCKER); fix-#2 **`.github/` framework CI** loop-safety violation. **`src/`+`pyproject.toml`+`uv.lock` runtime call = KEEP (verified)** via the hook→`uv run jerry`→`src.interface.cli.main:main` chain (grep-clean-of-imports is a red herring; fail-open hooks would silently no-op all guardrails if stripped). Added the **fail-closed no-duplicate-skill-names generation gate** (c-007, verification mechanism 3), **c-008** (runtime-dep retention), new section [Validated Retention Surface, Strip-Set, and Generation Gate](#validated-retention-surface-strip-set-and-generation-gate-phase-3) (incl. **recommended additional strips** `docs/`+`scripts/`+doc-site+dev/governance cruft, −285 → ~1,114 files), Positive #8/#9, two OBSERVED Risk rows, and a 4-agent Phase-3 Mirror Hand-Off. **P-022:** install-validated ≠ update-propagation-validated (G-update still OPEN) and ≠ hook-execution-validated (fail-open residual). Generation technique, determinism contract, tamper-evidence, AG-02 core strategy UNCHANGED (P-020). S-010 self-refine re-applied.
