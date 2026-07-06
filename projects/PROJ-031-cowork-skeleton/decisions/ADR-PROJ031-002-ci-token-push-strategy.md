# ADR-PROJ031-002: CI Token and Push Strategy for `cowork-skeleton`

> **SUPERSEDED BY [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md) (2026-06-28):** the confirmed dedicated-repo distribution model invalidates this ADR's three load-bearing decisions — a source `GITHUB_TOKEN` cannot push cross-repo (use a GitHub App token / deploy key), the artifact branch is now protected rather than unprotected, and the integrity anchor moves from editable Release notes to an immutable release attestation. Content retained for provenance; do not implement from this ADR.

> **PS:** cowork-skeleton-20260626-001 (Phase 1 — Requirements & Architecture)
> **Exploration:** ps-architect-001
> **Project:** PROJ-031-cowork-skeleton
> **Created:** 2026-06-26
> **Revised:** 2026-06-26 (iteration 3 — QG-1 C4 remediation)
> **Status:** **Superseded by ADR-PROJ031-003** (Phase 2 — dedicated-repo model)
> **Agent:** jerry:ps-architect
> **Criticality:** C4 (AE-003 ADR → C3 minimum; orchestration runs C4; AE-005 security-relevant → C3 minimum). Quality target >= 0.95.
> **Approval Gate:** AG-03 (superseded — credential/posture now decided at AG-04 in ADR-PROJ031-003)
> **Supersedes:** —
> **Superseded By:** [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language decision and why it matters |
| [Status](#status) | Decision status |
| [Context](#context) | Problem, the pivotal question, constraints, forces |
| [Options Considered](#options-considered) | GITHUB_TOKEN vs PAT vs GitHub App token, steelmanned |
| [Decision](#decision) | Chosen credential and permission block |
| [Branch-Protection Posture and Continuous Integrity Monitoring](#branch-protection-posture-and-continuous-integrity-monitoring) | Empirical ruleset finding, unprotected posture, coverage/push-failure checks, and the asynchronous publish-then-assert integrity monitor (with detection SLA) |
| [Loop-Safety Argument](#loop-safety-argument) | Three independent guarantees |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term and systemic consequences |
| [Consequences](#consequences) | Positive, negative, neutral, risks |
| [Related Decisions](#related-decisions) | Links to ADR-PROJ031-001 and work items |
| [References](#references) | Cited evidence |
| [Approval and PS Integration](#approval-and-ps-integration) | AG-03 sign-off and traceability |

---

## L0: Executive Summary

The CI workflow that rebuilds the `cowork-skeleton` branch each release needs a credential to **push** that branch. There are two obvious candidates: GitHub's built-in `GITHUB_TOKEN`, or a Personal Access Token (PAT) stored as a secret. We will use the **built-in `GITHUB_TOKEN` with a minimal `contents: write` permission** — not a PAT.

This is counter-intuitive but correct: the `GITHUB_TOKEN` is **both safer and sufficient**. It is scoped to this one repository, it **auto-expires** when the job ends (no long-lived secret to leak, rotate, or monitor), and — by GitHub's design — a push it makes **cannot re-trigger any workflow**. That last property gives us **free loop-safety**: the skeleton job must trigger nothing, and `GITHUB_TOKEN` guarantees it. The only thing a PAT would add is the ability to *trigger downstream workflows on the push* — which is exactly what we do **not** want here. (For contrast, Jerry's `version-bump.yml` *needs* a PAT precisely because it *wants* its tag push to fire `release.yml`; the skeleton has the opposite requirement.)

Why it matters: choosing the least-privileged, auto-expiring credential shrinks the blast radius if CI is ever compromised, removes an entire class of secret-management toil, and hardens the loop-safety story for a C4 review. We also record the branch-protection posture: keep `cowork-skeleton` **unprotected** (exactly like `gh-pages`), because it is a disposable, CI-regenerated derivative — a stance now **confirmed empirically** (the repo's only ruleset, `"Don't fuck with main"`, guards `main` alone with no bypass actors; there are no org rulesets — verified 2026-06-26, so `cowork-skeleton` is uncovered and force-pushable today). We keep the unprotected branch *safe by detection*: two **push-time** checks (a **pre-deploy ruleset-coverage check** and **runtime push-failure detection**) plus **continuous integrity monitoring** of the published branch. That monitor is the important reframe in this iteration: because a git branch is installable the *instant* it is pushed, an in-CI "pre-publication gate" would only re-assert the SHA the same job just created (a tautology) and would never see a *later* direct push — so we replace it with an **asynchronous publish-then-assert** model. CI publishes the expected deterministic SHA to the protected GitHub Release notes; a separate monitor — event-driven (a direct push to the branch trips it, while CI's own `GITHUB_TOKEN` push does not) plus a scheduled backstop (**≤ daily**, the explicit detection SLA) — then asserts the live tip **SHA** (a *non-forgeable* value, never the forgeable `Source-Commit` text) equals the published SHA, alerting and optionally **auto-reverting** on mismatch. This bounds (and can auto-heal) the tamper-exposure window rather than preventing it; a documented upgrade path (branch-protection ruleset force-push bypass, or a GitHub App token) covers any future org mandate to protect all branches — and is the route to *prevention* if Phase-2 deems the executable-hook blast radius to require it.

---

## Status

**Superseded by [ADR-PROJ031-003](./ADR-PROJ031-003-credential-protection-supply-chain.md)** (2026-06-28). This ADR was never approved at AG-03; before approval, Phase-2 research confirmed the dedicated-repo distribution model, which invalidates this ADR's premises (in-repo unprotected branch + source `GITHUB_TOKEN` push + Release-notes anchor). The credential, branch-protection, and integrity-anchor decisions are now made in ADR-PROJ031-003 and approved at AG-04. The analysis below — especially the `GITHUB_TOKEN` vs PAT vs GitHub App comparison and the loop-safety conjunction — remains useful background and is cited by ADR-PROJ031-003; it MUST NOT be implemented as written.

---

## Context

ADR-PROJ031-001 generates `cowork-skeleton` and force-pushes it on each release. This ADR decides the **credential** used for that push and the **branch-protection posture** of the target branch. The choice is dominated by one question:

> **Does the skeleton push need to trigger any downstream workflow?** — **No.** The design requires the skeleton push to **trigger nothing** (loop-safety; research §Q2, §L2 ¶3).

That single answer reframes the whole trade-off. A PAT's *only* differentiating capability over `GITHUB_TOKEN` is that PAT-pushed commits **can** re-trigger workflows; `GITHUB_TOKEN`-pushed commits cannot (an intentional GitHub recursion guard). Since we explicitly want no downstream firing, the PAT's distinguishing feature is not just unnecessary — it is **counter to** the requirement.

### Background

- **`GITHUB_TOKEN` can push branches** under `permissions: contents: write` — this is exactly what `docs.yml` does to force-push `gh-pages`. The skeleton is `gh-pages`'s operational sibling (research §Q2; ADR-PROJ031-001 §L2 ¶1).
- **`GITHUB_TOKEN`-pushed events do not create new workflow runs.** GitHub: *"events triggered by the `GITHUB_TOKEN`, with the exception of `workflow_dispatch` and `repository_dispatch`, will not create a new workflow run"* (research §Q2; GitHub Docs).
- **Contrast — `version-bump.yml` uses `VERSION_BUMP_PAT` on purpose** so its pushed **tag** triggers `release.yml`; a `GITHUB_TOKEN` tag push would not. The skeleton's requirement is the inverse (research §Q2 token contrast; reference [10]).
- **Branch protection interaction:** `GITHUB_TOKEN` cannot force-push to a **protected** branch that forbids force-push without a ruleset **bypass actor** or a GitHub App token (research §Q2 branch-protection, AE-005).
- **Empirical ruleset inventory (verified 2026-06-26):** the repository has exactly **one** active ruleset — `"Don't fuck with main"` (id 12387947) — and **no** organization-level rulesets (`gh api orgs/geekatron/rulesets` → HTTP 404). That ruleset targets **only** `~DEFAULT_BRANCH` (`main`) with rules `non_fast_forward`, `deletion`, `pull_request` and **`bypass_actors: null`**. **`cowork-skeleton` is covered by no ruleset** → it is force-pushable by `GITHUB_TOKEN` today, with no bypass actor required. The posture below is therefore the *observed current state*, not an assumption.

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| c-101 | The push credential MUST follow least-privilege (narrowest scope, shortest life). | PLAN.md Scope; research §Q2 (R-004) |
| c-102 | The skeleton push MUST NOT re-trigger any workflow (loop-safety). | research §Q2; §L2 ¶3 |
| c-103 | The credential MUST be able to **force-push** `cowork-skeleton` (wholesale regeneration per ADR-PROJ031-001). | ADR-PROJ031-001 c-004 |
| c-104 | Secret-exposure and maintenance surface SHOULD be minimized (storage, rotation, expiry monitoring). | research §Q2 (R-004); PLAN.md Goals |
| c-105 | The branch-protection posture of `cowork-skeleton` MUST be explicitly documented. | research §Q2; OQ-4; PLAN.md Scope |
| c-106 | Before each publish, the workflow MUST verify no ruleset has begun covering `cowork-skeleton` in a push-blocking way, and MUST fail **loudly** if the force-push is rejected (no silent staleness). | REM-002/003; AE-005 |
| c-107 | Because the regeneration commit is **unsigned** (ADR-PROJ031-001 determinism), artifact integrity MUST rest on a compensating control: deterministic-SHA tamper-evidence asserted by **continuous integrity monitoring** that compares the **non-forgeable** live tip SHA (never the forgeable `Source-Commit` trailer) against an independently-published expected SHA, within an explicit detection SLA; maintainer/CI provenance MUST be documented (as defense-in-depth, not the anchor). | REM-003; IT3-002/IT3-004; ADR-PROJ031-001 §Tamper-Evidence |

### Forces

1. **Least privilege vs. capability:** the most capable credential (broad PAT) is also the largest liability; the question is whether any extra capability is actually needed (it is not).
2. **Loop-safety vs. trigger capability:** the very feature that distinguishes a PAT (its pushes can trigger workflows) is the feature we must avoid.
3. **Branch protection vs. force-push:** protecting the branch would block `GITHUB_TOKEN`'s force-push without a bypass actor — but the branch has nothing worth protecting.
4. **Maintenance surface:** a PAT is a long-lived secret needing storage, rotation, and expiry monitoring (`pat-monitor.yml`-style); `GITHUB_TOKEN` has none of these.

---

## Options Considered

### Option A: Built-in `GITHUB_TOKEN` with `permissions: contents: write`  (CHOSEN)

Use the automatically provisioned, job-scoped `GITHUB_TOKEN`, granting only `contents: write` (all other permissions default to `none` once a `permissions:` block is declared).

**Pros:**
- **Least privilege (c-101):** repo-scoped and **auto-expires at job end** — no long-lived secret to exfiltrate (smallest blast radius for the R-004 credential-theft risk).
- **Free loop-safety (c-102):** `GITHUB_TOKEN` pushes **cannot** re-trigger workflows — defense-in-depth on top of the tag-vs-branch trigger design.
- **Force-push capable (c-103):** `contents: write` permits branch force-push to an **unprotected** branch (proven by `docs.yml` on `gh-pages`).
- **Zero maintenance (c-104):** nothing to store, rotate, or monitor; no PAT-expiry workflow needed.
- **Operational parity:** identical mechanism to `docs.yml`; small reviewer surface.

**Cons:**
- **Cannot push to a *protected* `cowork-skeleton`** without a ruleset bypass actor (c-105 interaction).
- **Cannot trigger downstream workflows** — irrelevant here, but a constraint if requirements ever change.

**Fit with Constraints:** Satisfies c-101..c-104 directly; c-103 holds **given** the unprotected posture chosen below; c-105 documented in [Branch-Protection Posture and Continuous Integrity Monitoring](#branch-protection-posture-and-continuous-integrity-monitoring).

### Option B: Scoped (fine-grained) Personal Access Token

Store a fine-grained PAT (Contents: Read/Write on this repo only) as an Actions secret and use it for the push.

**Steelman:** A fine-grained PAT *can* be scoped tightly (single repo, Contents-only) and is the **only** standard mechanism that lets the skeleton push **trigger a downstream workflow** if we ever need one — e.g., an automated post-push install-verification or a marketplace-refresh workflow keyed on the branch. It is also the pattern already in the repo (`VERSION_BUMP_PAT`), so it is familiar to maintainers. If the requirement were "push **and** fire a verification workflow," a PAT would be the pragmatic choice.

**Pros:**
- Can re-trigger workflows on push (the one capability `GITHUB_TOKEN` lacks).
- Can be granted force-push as a bypass actor more easily than `GITHUB_TOKEN` in some ruleset setups.
- Familiar (mirrors `VERSION_BUMP_PAT`).

**Cons:**
- **Violates least-privilege intent (c-101):** a **long-lived** secret with persistent scope — the exact asset the R-004 threat warns about; larger blast radius if leaked.
- **Re-trigger capability is counter to the requirement (c-102):** its distinguishing feature actively undermines loop-safety; we would have to *rely on* the other two guarantees instead of getting a third for free.
- **Maintenance burden (c-104):** storage, rotation, and expiry monitoring (a `pat-monitor.yml`-style workflow) — recurring toil with no offsetting benefit here.

**Fit with Constraints:** Fails the **intent** of c-101/c-104 and is adverse to c-102. Justified **only** if a future requirement mandates downstream firing on the skeleton push — which the design forbids. **Considered and rejected.**

### Option C: GitHub App installation token

Provision a GitHub App, install it on the repo, and mint a short-lived installation token in-workflow (e.g., via an action that exchanges App ID + private key for a token).

**Steelman:** This is the strongest option **if branch protection becomes mandatory**. An App installation token is **short-lived** (≈1 hour, unlike a PAT), can be **scoped** to this repo, can serve as a ruleset **bypass actor** (so it *can* force-push a protected branch), and — unlike `GITHUB_TOKEN` — its pushes **can** trigger workflows. It therefore satisfies a hypothetical future "protected branch **and** downstream trigger **and** short-lived credential" requirement that neither A nor B fully meets.

**Pros:**
- Short-lived token (much smaller exposure window than a PAT).
- Can be a branch-protection bypass actor (force-push a protected branch).
- Can trigger downstream workflows if ever needed.

**Cons:**
- **Setup complexity:** create/install an App, then store **App ID + private key** as secrets — which **reintroduces a long-lived secret** (the private key), just a different shape, partially defeating the least-privilege win (c-101/c-104).
- **Unneeded today:** we want **no** downstream trigger and an **unprotected** branch, so its differentiating capabilities are dormant (YAGNI).

**Fit with Constraints:** Over-provisioned for current constraints; reintroduces a long-lived secret. **Considered; retained as the documented upgrade path** if org policy later forces branch protection on `cowork-skeleton`.

### Option Comparison

| Criterion | A: GITHUB_TOKEN | B: Scoped PAT | C: GitHub App token |
|-----------|-----------------|---------------|---------------------|
| Least privilege (scope) | Repo-scoped | Repo-scoped (fine-grained) | Repo-scoped (installation) |
| Credential lifetime | **Job-expiring** | Long-lived | Short-lived (~1h) + long-lived private key |
| Loop-safety (cannot re-trigger) | **Yes (built-in)** | No (can re-trigger) | No (can re-trigger) |
| Force-push unprotected branch | Yes | Yes | Yes |
| Force-push **protected** branch | No (needs bypass) | Possible as bypass actor | **Yes** (bypass actor) |
| Secret-management surface | **None** | Store + rotate + monitor | Store private key + mint token |
| Maintainability | **High** | Medium | Low–Medium |

---

## Decision

**We will use Option A:** the built-in `GITHUB_TOKEN` with a minimal, job- or workflow-level permissions block:

```yaml
permissions:
  contents: write   # push/force-push the cowork-skeleton branch; everything else defaults to none
```

**Branch posture:** keep `cowork-skeleton` **unprotected** (gh-pages parity), so `GITHUB_TOKEN`'s force-push (ADR-PROJ031-001 c-004) succeeds without a bypass actor. **Option B (PAT) is rejected**; its only differentiating capability (re-triggering workflows) is contrary to the loop-safety requirement. **Option C (GitHub App token) is retained as the documented upgrade path** for the single scenario where org policy later mandates branch protection on `cowork-skeleton`.

### Rationale

With the pivotal question answered "no downstream trigger needed," `GITHUB_TOKEN` **dominates** a PAT on every axis that matters here: least privilege (c-101), loop-safety (c-102), force-push capability against an unprotected branch (c-103), and near-zero maintenance surface (c-104). It also matches the existing `docs.yml`/`gh-pages` mechanism, minimizing novelty for the C4 gate. A PAT would *remove* a free loop-safety guarantee and *add* a long-lived secret — strictly worse for this job. The App token is genuinely better only under a future protection mandate, so it is recorded as the upgrade path rather than adopted now (avoiding the premature reintroduction of a long-lived private key).

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | c-101..c-104 met; c-103 holds under the unprotected posture; c-105 documented. |
| Risk Level | LOW | Smallest credential blast radius; residual risk is a future org policy change. |
| Implementation Effort | S | A `permissions:` block; no secret provisioning. |
| Reversibility | HIGH | Switching to Option C is additive (App + token-mint step) if protection is mandated. |

---

## Branch-Protection Posture and Continuous Integrity Monitoring

*(L1 — the posture this ADR commits to; full ruleset config is STORY-005 / Phase 6 `branch-protection-config.md`.)*

### Empirical finding (not an assumption)

The ruleset landscape was **inventoried**, not presumed (verified 2026-06-26 via `gh api`):

| Scope | Result |
|-------|--------|
| Org rulesets (`orgs/geekatron/rulesets`) | **None** (HTTP 404). |
| Repo rulesets (`repos/geekatron/jerry/rulesets`) | **One** active: `"Don't fuck with main"` (id 12387947). |
| Its `conditions.ref_name.include` | `["~DEFAULT_BRANCH"]` — `main` **only**; `exclude: []`. |
| Its `rules` | `non_fast_forward`, `deletion`, `pull_request`. |
| Its `bypass_actors` | `null` (none). |

**Consequence:** `cowork-skeleton` is **outside every ruleset's coverage** and is force-pushable by `GITHUB_TOKEN` today with **no** bypass actor. The unprotected posture below is therefore the *observed current state*; the decision is whether to **leave it** unprotected or add protection.

### Decision: keep `cowork-skeleton` UNPROTECTED + add drift/failure detection

**Recommended posture: `cowork-skeleton` remains UNPROTECTED** (gh-pages parity), because:

- **Nothing to guard.** The branch is a disposable, CI-regenerated derivative, reconstructed wholesale every release from the authoritative `main`/tag (ADR-PROJ031-001). There is no human work on it to protect.
- **Protection would fight our own credential.** A `non_fast_forward`-style rule on `cowork-skeleton` would *block* the `GITHUB_TOKEN` force-push (c-103) unless a bypass actor is added — reintroducing exactly the machinery (App token / PAT) ADR-PROJ031-002 chose to avoid. Protecting this branch trades a real capability for no security gain.
- **The integrity risk is handled by detection, not prevention** (below) — a strictly better fit than a write-control rule for a deterministically-regenerated artifact.

Two **mandatory** *push-time* compensating controls keep the force-push itself safe and non-silent (c-106). These protect the **moment of the push**; the *standing* integrity of the published branch over time is handled separately by the continuous integrity monitor below.

1. **Pre-deploy ruleset-coverage check.** Before the force-push, the workflow asserts that no ruleset has begun covering `cowork-skeleton` in a push-blocking way — e.g. `gh api repos/geekatron/jerry/rulesets/branches/cowork-skeleton` returns no `non_fast_forward`/`update` rule lacking a `github-actions[bot]` bypass. If coverage appears (a future org/policy change), the job **fails fast with an actionable message** pointing to the upgrade table below — rather than discovering it as a raw push rejection.
2. **Runtime push-failure detection.** The `git push --force` step is followed by an explicit success assertion (`if: failure()` → annotate `$GITHUB_STEP_SUMMARY` and exit non-zero). A rejected push (new protection, revoked permission) is surfaced **loudly**, so the skeleton can never go stale undetected.

### Continuous Integrity Monitoring (publish-then-assert) — replacing the unsound in-CI "pre-publication gate" (c-107, IT3-002)

The regeneration commit is intentionally **unsigned** (ADR-PROJ031-001 determinism — a timestamped signature would break the bit-identical SHA). Because the branch is also **unprotected**, a repository collaborator could push a malicious commit directly to `cowork-skeleton` without CI (threat **RT-01**, distinct from "CI compromised"). Iteration 2 proposed a "pre-publication integrity gate" to mitigate this. **That framing is architecturally unsound and is retired here:**

> **Why an in-CI "pre-publication" gate cannot work.** A git branch is installable the **instant** it is pushed — `claude plugin marketplace add geekatron/jerry@cowork-skeleton` resolves the live branch tip with no "publication" step CI can gate. A SHA-equality check placed *inside* `cowork-skeleton.yml` immediately after the force-push would merely assert the SHA **that same job just computed and pushed** — a **tautology** that always passes and protects nothing. And it runs **only at release time**, so a direct push that tampers with the branch *after* the job finishes (the actual RT-01 threat) is never seen by it. "Pre-publication, inside the generating job" is therefore the wrong place and the wrong time.

The sound model is **asynchronous publish-then-assert with continuous monitoring** — the assert is temporally and contextually **independent** of the job that created the branch, and it compares a **non-forgeable** value (IT3-004):

**(1) Publish (synchronous, in `cowork-skeleton.yml`).** After the force-push, CI publishes the expected deterministic tip SHA for the release to a **durable, off-branch, protected surface** — the GitHub **Release notes** for the `v*` tag (Releases are governed by `main`/release permissions, not by the unprotected branch). This is *not* a gate; it establishes the **reference value** that later asserts compare against. Backed by **REQ-035**.

**(2) Assert — event-driven fast path (near-real-time).** A workflow `on: push: branches: [cowork-skeleton]` recomputes/retrieves the expected SHA and asserts the live tip matches. This **leverages the same `GITHUB_TOKEN` non-retrigger property** that gives loop-safety guarantee (3): the CI regeneration force-push (made with `GITHUB_TOKEN`) does **not** fire this workflow — so there is no loop and no false positive — whereas a **non-CI direct push** (the RT-01 actor, using their own credentials) **does** fire it. Detection latency for the exact tamper event is therefore **≈ Actions scheduling latency (seconds–minutes)**, not days.

**(3) Assert — scheduled backstop (bounded SLA).** The NFR-006 integrity/staleness workflow runs on a fixed cadence and independently recomputes the expected SHA and asserts the live tip matches. It also catches *lazy* staleness (CI never regenerated) and any tamper path that somehow evaded layer 2 (defense-in-depth). Backed by the **NFR-006 revision** (dual-check, below).

**Non-forgeable comparator (IT3-004).** Every assert compares `git rev-parse cowork-skeleton` (the live tip **SHA**; equivalently the tip tree hash `…^{tree}`) against the independently-recomputed/published expected SHA. The tip SHA is **non-forgeable** — git derives it from the actual published tree+parent+metadata, so presenting a tampered tree under the expected SHA would require a hash preimage collision (infeasible). The assert **MUST NOT** use the `Source-Commit:` trailer: that is free-form commit-message text any push actor can set to the correct value while shipping a different tree (**forgeable**). The trailer is retained only as the *lazy-staleness* signal (did CI regenerate against the latest tag?), never as the *tampering* signal.

**Detection SLA (explicit).** Event-driven path: **minutes** (best effort, not guaranteed — a push event could be missed). Scheduled backstop: the **guaranteed** worst-case detection window equals **one scheduled interval**; this ADR sets the interval at **≤ 24 hours (daily)** for the tamper assertion, given that the skeleton ships **executable hooks** to user workstations (IT3-007) and a weekly window is too long for that blast radius. The lazy-staleness check MAY remain weekly. The SLA is a Phase-1 requirement (cadence); the precise value and residual-risk acceptance are confirmed in Phase-2 (STRIDE, P-042/AE-005).

**Automation mode (explicit).** Mandatory floor: **detect-and-alert** — on mismatch, open a GitHub issue and fail the run loudly (requires `issues: write`, IN-003). Recommended: **auto-revert** — because the correct tip is *deterministically regenerable*, the monitor can re-run the generator for the affected tag and force-push the correct SHA back, converting the metric from *time-to-detect* into *time-to-restore*. Auto-revert is a security-response design decision finalized in Phase-2 (STORY-004/005); Phase-1 mandates the detect-and-alert floor.

**What this actually defends — and does NOT.** This is a **detection** control, not **prevention**. It does **not** make the instant-of-push tamper impossible; between a tamper event and the next successful assert, a tampered tip is installable (the residual exposure window — best-effort minutes via layer 2, guaranteed ≤ one interval via layer 3). It **does** bound that window and, with auto-revert, automatically heal it; and it makes any tamper **provable** via the non-forgeable SHA. For **zero-exposure synchronous prevention**, the documented upgrade is **branch protection** on `cowork-skeleton` with `github-actions[bot]` as the *sole* force-push bypass actor (Option C credential) — see the upgrade table below. Phase-2 STRIDE decides whether the executable-hook blast radius (IT3-007) warrants escalating from detection to that prevention.

**Maintainer / CI provenance (defense-in-depth, not the anchor).** In lieu of commit signing, provenance is *additionally* supported by: (i) the `github-actions[bot]` committer identity, (ii) the parent chain to the release commit (which sits on the ruleset-protected `main`), and (iii) the published expected-SHA per release. After this remediation the parent chain is **defense-in-depth**, not the integrity anchor — the non-forgeable deterministic tip SHA carries integrity on its own (which is why ADR-PROJ031-001's orphan fallback is integrity-neutral).

**Build-status precondition (R-007).** Require the build/validation CI status to pass before the expected SHA is published, so a broken (but correctly-SHA'd) regeneration is never advertised.

### Compensating Controls → Backing Requirements (for nse-requirements to mirror as SHALL)

The controls above are **mandatory**; iteration 2's gap was that they lived only in ADR prose with no backing requirement (IN-001/PM-001/RT-002). Each now maps to a WS-3 requirement so Phase-5/6 implementers have a contract and the ADR→REQ trace is closed:

| # | Compensating control | Backing requirement | Phase |
|---|----------------------|---------------------|-------|
| CC-1 | Publish expected deterministic SHA to GitHub Release notes (reference value) | **REQ-035** | P1 |
| CC-2 | Continuous integrity monitor — event-driven (`push:` on `cowork-skeleton`) + scheduled (≤ daily) assert of live tip SHA vs. published SHA | **REQ-035** (operationalized) + **NFR-006** revision (scheduled leg) | P1 |
| CC-3 | Non-forgeable staleness/integrity comparison — tip SHA / tree hash, dual-check (trailer → lazy staleness; SHA → tampering) | **NFR-006** revision | P1 |
| CC-4 | Tag-name sanitization allow-list covering `GITHUB_REF_NAME` **and** `inputs.target_tag`; no direct `${{ }}` interpolation in `run:` | **REQ-036** (aligned with ADR-PROJ031-001 RT-04) | P1 |
| CC-5 | Runtime push-failure detection (non-zero exit + structured diagnostic) | **REQ-037** | P1 |
| CC-6 | Pre-deploy ruleset-coverage check (fail-fast on new push-blocking coverage) | **REQ-037** (or sibling) | P1 |
| CC-7 | Continuous clone-weight telemetry + early-warning band (≈150 MB/40 s) ahead of the 250 MB/60 s flip trigger | **REQ-034d** (ADR-PROJ031-001 clone-weight decision) | P1 |
| CC-8 | Detection-SLA cadence declaration (≤ daily tamper assert) + `issues: write` permission for alerting | **NFR-006** revision + monitor implementation STORY | P1 |
| — | Auto-revert response automation; provenance (tag-on-main) assertion; escalation to branch-protection *prevention*; R-007b consequence re-rating | **deferred to Phase 2** (STRIDE / STORY-004/005, P-042/AE-005) | P2 |

### If org policy later mandates protection on all branches

Documented now so the change is a config delta, not a redesign:

| Upgrade path | What to do | Credential implication |
|--------------|------------|------------------------|
| Ruleset bypass for the Actions actor | Add a ruleset on `cowork-skeleton` that allows force-push and names `github-actions[bot]` as the **sole** bypass actor. | Keep Option A (`GITHUB_TOKEN`). |
| GitHub App bypass actor | Switch to **Option C**: a GitHub App installation token as the ruleset bypass actor. | Adopt Option C (short-lived token; store App private key). |

**Failure notification (no downstream workflow):** because the posture is "trigger nothing," surface failures **inside** the workflow — a `$GITHUB_STEP_SUMMARY` job summary with `if: always()` (mirroring `version-bump.yml`) plus an `if: failure()` step (optional Slack/webhook). No PAT-expiry monitoring is needed — there is no expiry to track (a secondary benefit of dropping the PAT).

---

## Loop-Safety Argument

Loop-safety is **over-determined** — three independent guarantees each individually prevent an infinite regenerate-push loop (research §L2 ¶3). For a C4 irreversibility argument this is stated as a conjunction of three documented invariants:

1. **Trigger shape:** the workflow triggers on `push: tags: ['v*']` + `workflow_dispatch`; its output is a **branch** (`cowork-skeleton`), which is **not** a tag and cannot re-fire any tag-keyed workflow.
2. **Listener shape:** `version-bump.yml` and `docs.yml` listen on **`main` only**, and `release.yml` listens on **`push: tags: 'v*'` only**; a push to `cowork-skeleton` (neither `main` nor a tag) is invisible to every workflow that listens on `main` or on tags (the watched set enumerated in REQ-014).
3. **Credential shape (this ADR):** `GITHUB_TOKEN` pushes **cannot re-trigger** any workflow at all.

Option A supplies guarantee (3) **for free**. Option B (PAT) would **remove** guarantee (3), leaving only (1) and (2) — a strictly weaker loop-safety posture. This is a concrete reason the security choice favors `GITHUB_TOKEN` beyond least-privilege alone.

> **The continuous integrity monitor is loop-safe by the same guarantee.** The event-driven monitor (`on: push: branches: [cowork-skeleton]`, IT3-002) deliberately fires on a *branch* push, so guarantee (1) does not suppress it — that is the point: a **non-CI direct push** must trip it. It does not loop, because guarantee (3) does: CI's own regeneration push and the monitor's optional auto-revert push are both made with `GITHUB_TOKEN`, which cannot re-trigger the monitor. Thus a direct push trips the monitor exactly once; the auto-revert that follows is silent to it. The very `GITHUB_TOKEN` property chosen here both prevents the regenerate loop **and** makes near-real-time tamper detection possible without a downstream-trigger credential.

---

## L2: Architectural Implications

1. **Token choice is the central security trade-off of the project, and it collapses cleanly.** The analysis reduces to one question — "must the skeleton push trigger anything? No" — after which `GITHUB_TOKEN` dominates a PAT on every axis (research §L2 ¶2). Recording the PAT as *considered and rejected*, with the `version-bump.yml` counter-case, gives the C4 review a crisp, defensible narrative.
2. **Least-privilege here is also least-maintenance.** Dropping the PAT removes a long-lived secret **and** its operational tail (rotation, expiry monitoring). The security win and the maintainability win point the same direction — an unusually clean decision.
3. **The loop-safety conjunction strengthens the C4 case.** Three independent invariants (trigger/listener/credential) mean no single misconfiguration reopens the loop risk (R-005). `GITHUB_TOKEN` is the credential leg of that conjunction.
4. **The one real future contingency is branch-protection policy — and it is currently empty for this branch.** The only active ruleset (`"Don't fuck with main"`) covers `main` alone with no bypass actors, and there are no org rulesets (verified 2026-06-26); `cowork-skeleton` is uncovered and force-pushable today. The posture adds two drift guards — a **pre-deploy ruleset-coverage check** and **runtime push-failure detection** — so a future policy change surfaces as a fast, actionable failure rather than silent staleness, and the upgrade (Actions-actor bypass or GitHub App token) is a configuration delta, not a redesign (research §Q2; OQ-4).
5. **Posture parity with `gh-pages` minimizes novel risk.** Treating `cowork-skeleton` as another unprotected, CI-owned derivative reuses an operational model already trusted in the repo, shrinking reviewer surface.
6. **Integrity is achieved by determinism + continuous monitoring, not by protection or signing — but it is DETECTION, not prevention.** Pairing ADR-PROJ031-001's recomputable deterministic SHA with an *asynchronous* publish-then-assert monitor (event-driven + scheduled, comparing the non-forgeable tip SHA) gives a *verifiable* integrity property that an unprotected, unsigned branch would otherwise lack — a cleaner supply-chain story for the C4 gate than per-run signing (which would break idempotency). The honest limit is that this **bounds** the tamper-exposure window (to a stated detection SLA) rather than **closing** it; branch protection is the only *preventive* control and remains the documented upgrade. The architecture deliberately exploits the `GITHUB_TOKEN` non-retrigger property twice — once for loop-safety, once to make a direct-push tamper trip a near-real-time monitor that CI's own pushes do not — which is an unusually economical reuse of a single primitive.

---

## Consequences

### Positive

1. **Smallest credential blast radius** — repo-scoped, auto-expiring `GITHUB_TOKEN`; nothing long-lived to steal (R-004 mitigation).
2. **Free, built-in loop-safety** — `GITHUB_TOKEN` pushes cannot re-trigger workflows; defense-in-depth and the third leg of the loop-safety conjunction.
3. **Zero secret-management toil** — no storage, rotation, or expiry monitoring; no PAT-monitor workflow.
4. **Operational parity** — same force-push mechanism as `docs.yml`/`gh-pages`; small C4 reviewer surface.
5. **Simple least-privilege wiring** — one `permissions: contents: write` block; all other scopes default to `none`.
6. **Verifiable-integrity posture for an unprotected branch** — continuous integrity monitoring (event-driven + scheduled ≤ daily) asserts the non-forgeable live tip SHA equals ADR-PROJ031-001's recomputable deterministic SHA, making the unprotected, unsigned branch tamper-evident and bounding the direct-write threat (RT-01) to a stated detection SLA (with optional auto-revert). This is detection, not prevention; prevention remains the documented branch-protection upgrade.

### Negative

1. **Cannot force-push a *protected* `cowork-skeleton`** — if org policy later mandates protection, `GITHUB_TOKEN` fails without a ruleset bypass actor. *Mitigation:* keep the branch unprotected (recommended); documented upgrade to an Actions-actor bypass or a GitHub App token.
2. **Cannot trigger downstream workflows** — if a future requirement needs the skeleton push to fire a verification/notification workflow, `GITHUB_TOKEN` cannot. *Mitigation:* current design deliberately wants none; if it changes, prefer a **GitHub App token** (short-lived) over a PAT (long-lived).
3. **Default `GITHUB_TOKEN` permission depends on repo/org settings** — if the org default is read-only and the `permissions:` block is omitted, the push fails. *Mitigation:* always declare explicit `permissions: contents: write` at workflow/job level; CI lint for its presence.

### Neutral

1. No secret provisioning is required — the workflow simply declares the permissions block, so onboarding a maintainer needs no token handoff.
2. Notifications live **inside** the workflow (job summary + `if: failure()`), consistent with the "trigger nothing" posture rather than a downstream notifier workflow.
3. The unprotected posture is the repository's **observed** current state (ruleset inventory, 2026-06-26), not an assumption; the pre-deploy coverage check guards against future drift.

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| New ruleset/org policy starts covering `cowork-skeleton` → `GITHUB_TOKEN` force-push blocked | LOW | MED | **Pre-deploy ruleset-coverage check** + **runtime push-failure detection** (fail loud, never silent); documented upgrade to Actions-actor bypass or GitHub App token (Option C). Record in `branch-protection-config.md` (STORY-005). |
| Direct malicious/erroneous push to the **unprotected** `cowork-skeleton` (no CI involvement) — RT-01. Note: blast radius includes **executable hooks** on user workstations (IT3-007), so exposure-window length matters. | MED (any collaborator/compromised credential) | MED–HIGH | **Bounded-window detection (not prevention):** continuous integrity monitor — event-driven (`push:` on the branch, near-real-time) + scheduled (≤ daily SLA) — asserts the **non-forgeable** live tip SHA equals ADR-PROJ031-001's recomputable deterministic SHA; mismatch alerts and (recommended) auto-reverts. Residual exposure = up to one SLA interval. *Prevention upgrade:* branch protection with `github-actions[bot]` sole bypass (Phase-2 STRIDE decides if the hook blast radius requires it). |
| Unsigned regeneration commit weakens provenance (no GPG attestation) | LOW | LOW–MED | Deterministic-SHA tamper-evidence (ADR-PROJ031-001) + documented `github-actions[bot]`/parent-chain provenance + published expected SHA per release; signing deliberately omitted to preserve bit-identical idempotency (c-107). |
| `permissions:` block omitted/misconfigured → push fails or token over-broad | LOW | MED | Explicit job-level `permissions: contents: write`; CI lint; code review. |
| Org default `GITHUB_TOKEN` is read-only → push fails (fails closed, visible) | LOW | LOW | Explicit `permissions` override at workflow/job level. |
| Future need to trigger a downstream workflow on the push | LOW | LOW–MED | Revisit credential; prefer short-lived GitHub App token over a PAT (preserve loop-safety reasoning). |

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| [ADR-PROJ031-001](./ADR-PROJ031-001-skeleton-distribution-strategy.md) | SUPPORTS | Provides the credential and unprotected-branch posture that make ADR-PROJ031-001's force-push safe and loop-safe. |
| TASK-001 (Workflow Triggers and Permissions) | REALIZED_BY | Encodes triggers + `permissions: contents: write`. |
| TASK-003 (Token and Branch-Protection Strategy) | REALIZED_BY | Implements this credential choice and branch posture. |
| STORY-004 / STORY-005 (STRIDE Threat Model + Remediations) | INFORMS | Threat model consumes the `GITHUB_TOKEN` decision; STORY-005 finalizes `branch-protection-config.md`. |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | [`../research/phase1-skeleton-ci-research.md`](../research/phase1-skeleton-ci-research.md) — §Q2 (token, recursion, branch protection); §L2 ¶2–3 | PRIMARY (internal) | Token analysis, loop-safety, PAT contrast. |
| 2 | GitHub Docs — `GITHUB_TOKEN` (repo-scoped, job-expiring; pushes do not create new workflow runs) | PRIMARY (vendor) | Least-privilege + built-in recursion guard. |
| 3 | GitHub Docs — "Triggering a workflow" → "Triggering a workflow from a workflow": *"events triggered by the `GITHUB_TOKEN`, with the exception of `workflow_dispatch` and `repository_dispatch`, will not create a new workflow run."* — `https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/triggering-a-workflow#triggering-a-workflow-from-a-workflow` [accessed 2026-06-26] | PRIMARY (vendor) | Loop-safety guarantee (3); the GITHUB_TOKEN non-retrigger invariant. |
| 4 | Repo `.github/workflows/docs.yml` (`gh-pages` via `--force`, `permissions: contents: write`, bot identity, `concurrency`) | PRIMARY (first-party) | Force-push precedent for the chosen credential. |
| 5 | Repo `.github/workflows/version-bump.yml` (`VERSION_BUMP_PAT` used *because* it wants the tag push to trigger `release.yml`) | PRIMARY (first-party) | The PAT contrast / counter-case. |
| 6 | Practitioner sources — `GITHUB_TOKEN` cannot push to a protected branch; ruleset bypass actor / GitHub App approaches | SECONDARY (corroborating) | Branch-protection interaction and upgrade paths. |
| 7 | [`../PLAN.md`](../PLAN.md) — Scope (least-privilege token and branch-protection strategy) | PRIMARY (internal) | Project mandate for this decision. |
| 8 | First-party `gh api` inventory (2026-06-26): `repos/geekatron/jerry/rulesets/12387947` (`"Don't fuck with main"`, target `~DEFAULT_BRANCH`, rules `non_fast_forward`/`deletion`/`pull_request`, `bypass_actors: null`); `orgs/geekatron/rulesets` → HTTP 404 (no org rulesets). | PRIMARY (first-party) | Empirical basis for the unprotected `cowork-skeleton` posture and the pre-deploy coverage check. |

---

## Approval and PS Integration

| Action | Detail | Status |
|--------|--------|--------|
| Approval gate | **AG-03** — approve the token strategy (`GITHUB_TOKEN` vs PAT) and the granted permission scope (`contents: write`) and branch posture (unprotected) | PENDING (user) |
| Exploration entry | `ps-architect-001` (Phase 1 — Requirements & Architecture) | Done |
| Entry type | DECISION | Done |
| Artifact link | `link-artifact` to this file under PROJ-031 | PENDING (orchestrator; this agent is scoped to write only within `decisions/`) |

---

**Generated by:** jerry:ps-architect (ps-architect-001)
**Format:** Michael Nygard's ADR Format (2011)
**Self-review:** S-010 (Self-Refine) and S-003 (Steelman of Options B and C) applied before finalization per H-15/H-16.
**Iteration 2 (QG-1 C4 remediation, 2026-06-26):** REM-002 (empirical org+repo ruleset inventory — only `"Don't fuck with main"` on `~DEFAULT_BRANCH`, no org rulesets, `cowork-skeleton` uncovered/force-pushable); REM-003 (keep unprotected + pre-deploy ruleset-coverage check + runtime push-failure detection + pre-publication integrity gate + unsigned-commit provenance — c-106/c-107); REM-017 (GITHUB_TOKEN docs URL + access date); REM-018 (`release.yml` added to loop-safety guarantee #2). S-010 self-refine re-applied.
**Iteration 3 (QG-1 C4 remediation, 2026-06-26):** **IT3-002** — retired the architecturally unsound in-CI "pre-publication integrity gate" (a git branch is installable the instant it is pushed, so an in-job post-push SHA check is tautological and blind to later direct-push tampering) and replaced it with **asynchronous publish-then-assert continuous integrity monitoring**: CI publishes the expected deterministic SHA to the protected GitHub Release notes; an event-driven monitor (`push:` on `cowork-skeleton`, fired by direct pushes but not by `GITHUB_TOKEN`) plus a scheduled backstop (**≤ daily detection SLA**) assert the live tip SHA matches, with detect-and-alert (mandatory) and auto-revert (recommended). **IT3-004** — specified the comparator as the **non-forgeable** tip SHA / tree hash, never the forgeable `Source-Commit` trailer (trailer = lazy-staleness signal only). Renamed §Branch-Protection Posture → §Branch-Protection Posture and Continuous Integrity Monitoring; added a **Compensating Controls → Backing Requirements** table (REQ-035/036/037, NFR-006 revision, REQ-034d) closing the ADR→REQ trace (IN-001/PM-001/RT-002), with Phase-2 deferrals marked. Fixed loop-safety guarantee #2 count (CV-006) and documented the monitor's own loop-safety. S-010 self-refine re-applied.
