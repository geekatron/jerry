---
DISCLAIMER: This design is AI-generated guidance based on DevSecOps pipeline
engineering standards and the authoritative inputs listed under References.
It is advisory only. All workflow configurations require human review and
professional engineering judgment before Phase 6 implementation.
---

# Phase 3 CI Design: Regeneration Workflow and D7 Monitor

> **Document ID:** FAD-PROJ031-3B-001
> **Project:** PROJ-031-cowork-skeleton
> **Phase:** Phase 3 — Skeleton + CI DESIGN (sub-phase 3b, CI workflow)
> **Agent:** jerry:eng-devsecops
> **Criticality:** C4 (AE-002 `.github/` changes; AE-005 security-relevant; quality target >= 0.95)
> **Created:** 2026-06-30
> **Revised:** 2026-06-30 (QG-3 Round-2 consolidating fix — ROOT-1 DA-001 8-step digest monitor mirrored from eng-infra; ROOT-2 FM-007 $GITHUB_ENV determinism; ROOT-3 D6 known-injected allow-list; ROOT-4 FM-037 bundle HEAD checkout; ROOT-5 PM-003 D8 scanner spec; ROOT-6 PM-004 auto-revert circuit breaker)
> **Revised:** 2026-06-30 (QG-3 iter-2 Criticals — FM-001-i2 freshness annotated-tag date source; FM-002-i2 runner image pinning mandated; FM-003-i2 last-good-validated invariant guard)
> **Revised:** 2026-06-30 (QG-3 iter-2 Majors — FM-004-i2 circuit-breaker `--state all` monotonic counter; FM-005-i2 cowork-monitor.yml concurrency group serialization)
> **Revised:** 2026-07-02 (Phase-3 live-install mirror — c-007 fail-closed retention/dup-skill-name gate (STEP c007-retention-and-skill-name-validation) + plugin-smoke check (STEP plugin-smoke-check) added to generate-and-gate between D6 and D8; mirrors ADR-PROJ031-001 c-007/c-008 Mirror Hand-Off; gate would have caught fix-cycle #1 .graveyard/worktracker collision pre-push)
> **Status:** Design — pseudocode/structure only. No production YAML. Phase 6 implements.
> **Inputs (FINAL):** phase3-skeleton-generation-design.md (G1–G9, gates, hand-off scope, $GITHUB_ENV determinism constraint, D6 known-injected allow-list §3(c)); ADR-PROJ031-003 (D1–D8, gate sequence, per-job permissions, G-actions-write-safe, D7 monitor, auto-revert); phase1-requirements.md (REQ-011..055, NFR-001..006); phase3-attestation-provenance-design.md §3.3 MONITOR HAND-OFF (binding invariant + 8-step digest monitor — ROOT-1 mirror).
> **Claim-Status Convention (P-022):** All controls below are **Designed — operational validation pending** the named Phase-5 gate. Achieved present tense is reserved for Phase-5 post-validation. This document is a design artifact; nothing here is an achieved fact.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What this design covers and why the structure matters |
| [L1: Workflow Topology](#l1-workflow-topology) | Two-workflow topology overview |
| [cowork-skeleton.yml Design](#cowork-skeletonyml-design) | Triggers, job graph, gate-sequence pseudocode |
| [cowork-monitor.yml Design](#cowork-monitoryml-design) | Monitor triggers, jobs, integrity+freshness, auto-revert |
| [G-actions-write-safe Enforcement](#g-actions-write-safe-enforcement) | SHA-pin scope, gate conditions, enforcement |
| [Hook Bypass Note](#hook-bypass-note) | R-001 rationale for --no-verify on G6 commit |
| [L2: Architectural Implications](#l2-architectural-implications) | Systemic consequences, risks, Phase 6 gaps |
| [Traceability Matrix](#traceability-matrix) | Design element to REQ/ADR mapping |
| [Pending Validation P-022](#pending-validation-p-022) | Honest open items and Phase 6 details |
| [References](#references) | Cited inputs |

---

## L0: Executive Summary

This design specifies the **CI workflow structure** for the PROJ-031 skeleton regeneration pipeline. It does not produce production YAML (that is Phase 6); it produces the job graph, gate sequence, per-job permission model, and monitor topology that Phase 6 implements.

Two workflows are designed:

**`cowork-skeleton.yml`** (source repo, tag-triggered): a three-job pipeline that runs G1–G9 and all security gates, then produces a deterministic artifact, attests it in a permissions-isolated job, and force-pushes to the dedicated repo. The gate sequence is load-bearing: every gate must pass before attestation; attestation must succeed before the push job may run. No gate is bypassable by design.

**`cowork-monitor.yml`** (source repo, scheduled): a read-only backstop that downloads the attested artifact, verifies it with `gh attestation verify <artifact-file>`, confirms the dedicated-repo tip matches the expected tree-digest, checks freshness (latest source `v*` deployed within ≤ 2 h), fails closed on any error, and advances `last-good-validated` on a full pass. Auto-revert dispatches the normal gated path on failure — but only after the **G-actions-write-safe** dependency gate clears (REQ-017 all-workflow SHA-pin AND G-provenance operational).

The primary engineering novelty in this design is the **per-job permissions isolation** (REQ-020/ADR-PROJ031-003 D4 A-1): generation and push are in one job (`contents: write` only); attestation is a separate job (`id-token: write + attestations: write`, no `contents: write`). A git bundle bridges the generated commit between the generate-and-gate job and the push-and-release job (Phase 6 implementation detail, flagged below).

---

## L1: Workflow Topology

```
SOURCE REPO  geekatron/jerry
  ├── cowork-skeleton.yml
  │     Trigger: push tags v*  +  workflow_dispatch
  │     ┌──────────────────────────────────────────────────────────────────┐
  │     │ Job A: generate-and-gate   permissions: contents: read            │
  │     │   G1/G2 tag resolve + validate                                    │
  │     │   D5  provenance assertion (merge-base, REQ-038)                 │
  │     │   G3  checkout v* (fetch-depth: 0)                               │
  │     │   G4  git rm -r projects/ tests/                                 │
  │     │   G5  static stub + version sentinel                             │
  │     │   G6  deterministic commit (--no-verify, pinned dates)           │
  │     │   G7  retention completeness (plugin.json-derived)               │
  │     │   G8  multi-dim gate (file-count ∧ pack ∧ clone)                │
  │     │   D6  faithful-derivative + secret scan (REQ-022)                │
  │     │   c-007 dup-skill gate (.graveyard/+.github/ absent; SKILL.md names unique) │
  │     │   plugin-smoke (json parse + skills resolve + uv run jerry)       │
  │     │   D8  content-safety scan (REQ-052)                              │
  │     │   G9  git archive → artifact + git bundle                        │
  │     │   upload: artifact + bundle to Actions artifact store             │
  │     └──────────────────────────────┬───────────────────────────────────┘
  │                                    │ needs: generate-and-gate
  │     ┌──────────────────────────────▼───────────────────────────────────┐
  │     │ Job B: attest              permissions: id-token: write            │
  │     │                                         attestations: write        │
  │     │                                         (NO contents: write)       │
  │     │   download artifact from artifact store                           │
  │     │   gh attestation attest <artifact-file> --repo geekatron/jerry    │
  │     │   (fail: exit 1 → push job skipped by needs: dependency)         │
  │     └──────────────────────────────┬───────────────────────────────────┘
  │                                    │ needs: attest
  │     ┌──────────────────────────────▼───────────────────────────────────┐
  │     │ Job C: push-and-release    permissions: contents: write (sole)    │
  │     │   environment: skeleton-push (REQ-045, v*/main only)             │
  │     │   download artifact + git bundle from artifact store              │
  │     │   restore git state from bundle                                   │
  │     │   mint App installation token (1h, dedicated-repo contents: write)│
  │     │   git push --force <dedicated-remote> HEAD:<default-branch>      │
  │     │   gh release create --repo geekatron/jerry-claude-plugin v{N} <artifact>│
  │     │   advance last-good-validated ← gated on G-actions-write-safe    │
  │     │   push failure detection (if: failure(), REQ-037)                │
  │     │   $GITHUB_STEP_SUMMARY (if: always(), REQ-016)                  │
  │     └──────────────────────────────────────────────────────────────────┘
  │
  └── cowork-monitor.yml
        Trigger: schedule ≤6h  +  workflow_dispatch
        ┌──────────────────────────────────────────────────────────────────┐
        │ Job M1: integrity-and-freshness                                   │
        │   permissions: issues: write, contents: write (last-good tag)    │
        │   [actions: write added ONLY after G-actions-write-safe]         │
        │   (a) gh attestation verify <artifact-file> --repo geekatron/jerry│
        │   (b) git ls-remote tip-SHA == expected tree-digest              │
        │   (c) freshness: latest v* tag deployed within ≤2h (REQ-049)    │
        │   fail-closed: any error → CRITICAL issue + exit 1 (FM-033)     │
        │   on PASS: advance last-good-validated tag on source repo        │
        │   $GITHUB_STEP_SUMMARY (if: always())                           │
        ├──────────────────────────────────────────────────────────────────┤
        │ Job M2: auto-revert (if: failure() from M1)                      │
        │   [OMITTED until G-actions-write-safe; human-escalation mode]   │
        │   permissions: actions: write (post-G-actions-write-safe only)   │
        │   gh workflow run cowork-skeleton.yml --field target_tag=<lgv>   │
        │   Monitor pushes nothing to dedicated repo (loop-safe, CR-02)    │
        ├──────────────────────────────────────────────────────────────────┤
        │ Job M3: clone-weight-telemetry (separate, non-blocking)           │
        │   permissions: contents: read                                     │
        │   timed reference clone of geekatron/jerry-claude-plugin                │
        │   emit pack_size_mb + clone_secs → $GITHUB_STEP_SUMMARY          │
        │   informational issue if pack > 150MB or clone > 40s (REQ-034d) │
        └──────────────────────────────────────────────────────────────────┘

        (separate) cowork-meta-monitor.yml
              Trigger: schedule ≤24h
              Verifies cowork-monitor.yml ran successfully within prior 25h
              Opens informational issue if not (REQ-044)
              NOTE: Must be SEPARATE workflow — if cowork-monitor.yml fails
              entirely, a meta-monitor job inside it also fails (FM-033 gap)

        DEDICATED REPO  geekatron/jerry-claude-plugin
              No workflows that push (loop-safety by topology, CR-02)
              Default branch = skeleton (~1,417 files)
              Org-level ruleset: CI sole bypass, zero human write (D2/REQ-040)
```

---

## cowork-skeleton.yml Design

### Triggers and Concurrency

```yaml
# PSEUDOCODE — not production YAML; Phase 6 implements with SHA-pinned Actions

on:
  push:
    tags: ['v*']                  # REQ-011: only v* tag push
  workflow_dispatch:
    inputs:
      target_tag:
        description: 'v* release tag to regenerate from; defaults to latest if blank'
        required: false
        type: string
        # REQ-011: optional; blank → resolve latest

# No other trigger events (REQ-011, REQ-023)

concurrency:
  group: cowork-skeleton
  cancel-in-progress: false       # REQ-015: serialize; never cancel in-flight

# No workflow-level permissions: block (REQ-020: per-job only)
```

### Per-Job Permissions Table

| Job | GITHUB_TOKEN Permissions | Rationale |
|-----|--------------------------|-----------|
| generate-and-gate | `contents: read` | Checkout (fetch-depth: 0) only; no source-repo write; git commit is local |
| attest | `id-token: write, attestations: write` | Sigstore OIDC + attestation write; **NO `contents: write`** per REQ-020(b) |
| push-and-release | `contents: write` (sole) | Matches REQ-020(a); actual cross-repo push uses App token, not GITHUB_TOKEN |

> **Environment gate (REQ-045):** The `generate-and-gate` job declares `environment: skeleton-push` for fast-fail on unauthorized branches — rejects `workflow_dispatch` from feature branches before any generation work begins. The `push-and-release` job also declares `environment: skeleton-push` to gate App credential access. The `deployment_branch_policy` restricts activation to `main` and `v*` tag patterns only.

### Gate Sequence Pseudocode

All failures are **fail-closed**: non-zero exit, no artifact, no push (phase3-skeleton-generation-design.md §2).

```
# ═══ Job A: generate-and-gate ═════════════════════════════════
# permissions: contents: read
# environment: skeleton-push  (REQ-045: rejects non-main/v* triggers)

STEP resolve-and-validate-tag:
  # Event-discriminated resolution (REQ-036; ADR-PROJ031-001 IT3-005):
  # Context expressions bound via env:, NEVER interpolated into run: shell
  IF event == workflow_dispatch:
    TAG = env.INPUT_TARGET_TAG  # from env: binding of ${{ inputs.target_tag }}
    IF TAG is blank:
      TAG = newest_semver_tag()   # git tag -l 'v[0-9]*' --sort=-version:refname | head -1
  ELSE:                           # push: tags
    TAG = env.GITHUB_REF_NAME    # from env: binding of ${{ github.ref_name }}

  # Allow-list validation — one gate covers all input paths (REQ-036):
  ASSERT TAG matches ^v[0-9]+\.[0-9]+(\.[0-9]+)?$  OR  exit_1("rogue tag syntax")
  SRC_SHA  = git rev-parse "${TAG}^{commit}"        # full 40-char hex
  SRC_DATE = git show -s --format=%cI "${SRC_SHA}"  # ISO-8601 committer date

STEP d5-provenance-gate:
  # Tag-on-main assertion — BEFORE any generation (REQ-038; ADR-PROJ031-003 D5):
  git fetch origin main --depth=1
  git merge-base --is-ancestor "${SRC_SHA}" origin/main \
    OR  exit_1("[CRITICAL] SC-02 rogue-tag: ${TAG}/${SRC_SHA} not ancestor of main")
  # Non-ancestor → no artifact, no attestation, no push

STEP g3-checkout:
  git checkout "${TAG}"   # frozen released tree; fetch-depth: 0 already done

STEP g4-denylist-strip:
  git rm -r projects/ tests/              # REQ-002; retains all else BY CONSTRUCTION

STEP g5-static-stub:
  write_static(projects/README.md)        # REQ-004: empty-dir guard, static prose only
  write_static(<version-sentinel-path>)   # REQ-004a: Source-Tag + full 40-char SRC_SHA only
                                          # NEVER timestamp/run-id (breaks REQ-003 bit-stability)

STEP g6-deterministic-commit:
  # Pinned dates — DETERMINISM-CRITICAL (FM-007-QG3 / ROOT-2 fix / REQ-003/008):
  # A bare `export` does NOT survive GitHub Actions `run:` step boundaries (each step is a
  # fresh shell process). FORBIDDEN: `export GIT_AUTHOR_DATE=...` in a prior step.
  # CORRECT MECHANIC — eng-devsecops picks ONE of (mirroring phase3-skeleton-generation-design.md §2 G6):
  #   (i)  SAME-STEP INLINE (preferred): set vars in the SAME process that runs git commit.
  #        Combine G4–G6 in one `run:` block, or use inline env binding:
  #        GIT_AUTHOR_DATE="${SRC_DATE}" GIT_COMMITTER_DATE="${SRC_DATE}" git commit ...
  #   (ii) CROSS-STEP via $GITHUB_ENV (if G5 and G6 must be separate named steps):
  #        echo "GIT_AUTHOR_DATE=${SRC_DATE}"    >> "$GITHUB_ENV"
  #        echo "GIT_COMMITTER_DATE=${SRC_DATE}" >> "$GITHUB_ENV"
  #        (the subsequent git commit step reads them from the environment automatically)
  PIN_GIT_DATES(GIT_AUTHOR_DATE=SRC_DATE, GIT_COMMITTER_DATE=SRC_DATE)  # same-step or $GITHUB_ENV
  git commit \
    --no-verify \                         # intentional: bypass dev hooks (R-001; see §Hook Bypass Note)
    --author "github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>" \
    --message FIXED_TEMPLATE(TAG, SRC_SHA)  # 40-char SHA in subject + Source-Commit: trailer
    # UNSIGNED: a timestamped signature breaks bit-identity (§3 of generation design)
  COMMIT_SHA = git rev-parse HEAD

STEP g7-retention-completeness:
  # Verify presence (REQ-005):
  FOR dir IN [.claude-plugin/, skills/, commands/, .claude/, .context/, hooks/, src/, schemas/]:
    ASSERT git ls-tree --name-only HEAD "${dir}/"  non-empty  OR  exit_1("dir missing: ${dir}")
  ASSERT git ls-files .claude-plugin/plugin.json   non-empty  OR  exit_1("plugin.json missing")
  ASSERT git ls-files .claude-plugin/marketplace.json non-empty OR exit_1("marketplace.json missing")
  # Manifest-derived (no hard-coded list, drift-proof) (REQ-010):
  FOR path IN declared_paths(plugin.json: skills ∪ agents[] ∪ commands[]):
    ASSERT path in git_ls_files(HEAD)  OR  exit_1("manifest path missing: ${path}")
  # Negative (strip confirmed) (REQ-002/005):
  ASSERT git ls-files tests/     is EMPTY                 OR  exit_1("tests/ not stripped")
  # ROOT-3 / FM-020-QG3: projects/ must contain EXACTLY the two known-injected allow-list members
  # (both under projects/ so D6 ':!projects/' exclusion already covers them — gen design §3(c)):
  ASSERT git ls-files projects/  == {projects/README.md, projects/.jerry-skeleton-version}  \
    OR  exit_1("projects/ has unexpected files — only known-injected allow-list permitted")
  # Symlink integrity (REQ-009):
  ASSERT readlink -f .claude/rules    resolves to existing target  OR  exit_1("symlink broken")
  ASSERT readlink -f .claude/patterns resolves to existing target  OR  exit_1("symlink broken")

STEP g8-multi-dim-gate:
  file_count   = git ls-files | wc -l
  pack_size_mb = git count-objects -vH | grep size-pack | awk '{print $2}'  # in MB
  clone_secs   = timed_reference_clone()  # 10 Mbps reference network (30th-pct global broadband)

  # Emit telemetry EVERY run regardless of pass/fail (REQ-034d):
  emit_to_GITHUB_STEP_SUMMARY(file_count, pack_size_mb, clone_secs)

  # Early-warning bands (non-blocking, open informational issue):
  IF file_count   >= 3500:  open_informational_issue("[INFO] file-count approaching ceiling")  # REQ-050
  IF pack_size_mb >= 150:   open_informational_issue("[INFO] pack-size clone-weight warning")  # REQ-034d
  IF clone_secs   >= 40:    open_informational_issue("[INFO] clone-time clone-weight warning") # REQ-034d

  # Hard-fail (OR-combined, fail-closed) (REQ-006):
  ASSERT file_count   < 5000   OR  exit_1("[CRITICAL] file-count ceiling breach (REQ-006a)")
  ASSERT pack_size_mb < 250    OR  exit_1("[CRITICAL] pack-size ceiling breach (REQ-006b)")
  ASSERT clone_secs   < 60     OR  exit_1("[CRITICAL] clone-time ceiling breach (REQ-006c)")

STEP d6-faithful-derivative-and-secret-scan:
  # Faithful-derivative gate — compare against TAG (not a mutable branch, FM-09 fix) (REQ-022):
  # ROOT-3 / FM-020-QG3: ':!projects/' exclusion already covers BOTH known-injected allow-list
  # members: projects/README.md (stub) and projects/.jerry-skeleton-version (sentinel).
  # G7 independently asserts projects/ == exactly those two members, so the ':!projects/'
  # wholesale exclusion cannot mask an unexpected injected file outside the allow-list.
  # D6 does NOT need a pathspec change — the sentinel under projects/ is already excluded.
  git diff --quiet "${TAG}..HEAD" -- ':!projects/' ':!tests/' \
    OR  exit_1("[CRITICAL] skeleton not faithful to ${TAG}")
  # Secret scan of generated tree before public push (REQ-022 / ADR-PROJ031-003 D6 / V-05):
  <secret-scanner> --fail-on-find .  \
    OR  exit_1("[CRITICAL] secret detected in generated tree")

STEP c007-retention-and-skill-name-validation:
  # c-007 fail-closed retention/dup-skill-name gate (ADR-PROJ031-001 c-007/c-008; Mirror Hand-Off 2026-07-02).
  # PLACEMENT: after D6 faithful-derivative+secret-scan (tree confirmed faithful + clean);
  # before D8 content-safety scan (no point scanning a duplicate-skill tree) and before
  # attestation (no attested artifact may exist with a duplicate skill name or an unsafe strip).
  # This gate is what would have caught fix-cycle #1 (2026-07-02): skills/.graveyard/worktracker
  # name-collided with live skills/worktracker → marketplace BLOCKER.
  # The validated strip removes today's known collision; this gate is the durable guard.
  #
  # (a) Strip-correctness — validated strip-set members MUST be absent from generated tip:
  ASSERT git ls-files "skills/.graveyard/"  is EMPTY \
    OR  exit_1("[CRITICAL] c-007: skills/.graveyard/ present in tip — strip incomplete; fix-cycle #1 recurrence risk (duplicate skill name)")
  ASSERT git ls-files ".github/"            is EMPTY \
    OR  exit_1("[CRITICAL] c-007: .github/ present in tip — strip incomplete; CI-loop violation (fix-cycle #2 recurrence risk)")
  #
  # (b) Runtime-dependency retention (c-008; KEEP call verified 2026-07-02):
  #     Hooks fail-open: missing these three files makes uv run jerry silently no-op
  #     on every hook event — no H-04 bootstrap, no guardrails, no error surfaced.
  ASSERT git ls-files "pyproject.toml"  is non-empty \
    OR  exit_1("[CRITICAL] c-007/c-008: pyproject.toml absent — hooks will fail-open silently (uv run jerry entry-point undefined)")
  ASSERT git ls-files "uv.lock"         is non-empty \
    OR  exit_1("[CRITICAL] c-007/c-008: uv.lock absent — hooks will fail-open silently (uv run jerry dependency resolution fails)")
  #
  # (c) No-duplicate-skill-names — marketplace invariant (ADR-PROJ031-001 c-007; fail-CLOSED):
  skill_names = []
  FOR skill_md IN ( git ls-files "skills/" | grep "/SKILL.md$" ):
    # Resolve skill name: read YAML frontmatter `name` field if present;
    # fall back to the containing directory basename (parent dir of SKILL.md).
    name = frontmatter_field(skill_md, "name") OR basename( parent_dir(skill_md) )
    skill_names.append(name)
  duplicates = { n : count(n, skill_names) for n in skill_names if count(n, skill_names) > 1 }
  IF duplicates is non-empty:
    exit_1("[CRITICAL] c-007: duplicate skill name(s) in generated tip tree: "
           + str(sorted(duplicates))
           + " — Claude marketplace will REJECT this plugin; NO push, NO attestation")
  # PASS: all SKILL.md names unique. Any assertion failure: non-zero exit, no artifact,
  # no attestation, no push (consistent with fail-closed semantics of the gate train).

STEP plugin-smoke-check:
  # NEW step — cheap pre-push plugin loadability check (empirical lesson: 2026-07-02 install).
  # Claude's plugin validator rejected the generated tree at marketplace install-time.
  # This step catches that failure class in CI — before push, before attestation.
  # Fail-closed: non-zero exit → no D8 scan, no attestation, no push.
  # Phase-6 impl note (P-022): Phase 6 must ensure uv is available in the runner before
  # this step; exact invocation flags are Phase-6 details (CI-G-003 scope).
  #
  # (a) JSON validity — both plugin descriptor files must parse as valid JSON:
  jq empty .claude-plugin/plugin.json \
    OR  exit_1("[CRITICAL] smoke: .claude-plugin/plugin.json is not valid JSON — plugin loader will reject at install")
  jq empty .claude-plugin/marketplace.json \
    OR  exit_1("[CRITICAL] smoke: .claude-plugin/marketplace.json is not valid JSON — marketplace will reject at install")
  #
  # (b) Declared skills resolve — every skills[] entry in plugin.json must have a SKILL.md
  #     present in the tip tree (independent defense-in-depth, complements G7 manifest check):
  FOR skill_dir IN jq_extract_skill_dirs(.claude-plugin/plugin.json):
    ASSERT git ls-files "${skill_dir}/SKILL.md"  is non-empty \
      OR  exit_1("[CRITICAL] smoke: declared skill missing SKILL.md: ${skill_dir} — plugin registration will fail at install")
  #
  # (c) Hook runtime entrypoint reachability — uv can resolve the jerry CLI entry point (H-05):
  #     src/ is RETAINED per c-008 (KEEP call 2026-07-02). If retention is silently broken,
  #     uv run jerry fails-open on all hooks — no H-04 bootstrap, no guardrails, no error.
  #     Dry import confirms REACHABILITY before push; not a full hook execution in-sandbox.
  uv run --directory "." python -c "import src.interface.cli.main" \
    OR  exit_1("[CRITICAL] smoke: 'src.interface.cli.main' unresolvable via uv run — hooks will fail-open silently in CoWork (H-04 bootstrap dead, all guardrails dead)")
  # NOTE (P-022 / Phase-6): this dry-import check confirms entrypoint REACHABILITY only,
  # not hook EXECUTION in the CoWork sandbox. Full hook execution is a Phase-5 E2E
  # acceptance test (ADR-PROJ031-001 c-008 scope — install-validated ≠ hook-execution-validated).

STEP d8-content-safety-scan:
  # ROOT-5 / PM-003-Q3: D8 scanner specification (REQ-052/ADR-PROJ031-003 D8).
  # POSITIONING: after D6 faithful-derivative+secret-scan, before attestation (ADR-PROJ031-003 D4 C-7).
  # SCOPE: retained markdown surface only — the payload that becomes Claude behavior:
  #   skills/ commands/ .claude/ .context/  — projects/ and tests/ are already stripped, out of scope.
  #
  # PATTERN CATALOG: runbooks/content-safety-patterns.md (C1–C6 indicator set).
  # NOTE (P-022 honesty): The CATALOG FILE PATH is fixed here; the CATALOG CONTENT (patterns
  # C1–C6: role-reversal phrasing, system-override constructs, LLM control tokens, explicit
  # exfiltration/agentic-action directives) is an eng-architect deliverable — a Phase-6
  # prerequisite (CI-G-003). This gate CANNOT operate until eng-architect delivers the catalog.
  # The G-content Phase-5 gate MUST verify: (i) catalog file exists and is non-empty;
  # (ii) named scanner tool is pinned; (iii) synthetic positive test passes.
  #
  # SCANNER INVOCATION (design-level; Phase-6 finalizes the tool name and flags per CI-G-003):
  #   - reads patterns from runbooks/content-safety-patterns.md
  #   - runs pattern match over skills/ commands/ .claude/ .context/
  #   - exit 0 = no patterns matched AND scanner exited cleanly
  #   - exit non-zero = pattern matched OR scanner errored (BOTH treated as failure — fail-closed)
  PATTERN_CATALOG="runbooks/content-safety-patterns.md"
  ASSERT exists(PATTERN_CATALOG) AND non-empty(PATTERN_CATALOG)  \
    OR  exit_1("[CRITICAL] D8: pattern catalog absent or empty — gate cannot operate (CI-G-003)")
  <content-safety-scanner> --patterns "${PATTERN_CATALOG}" --fail-on-match --fail-on-error \
    skills/ commands/ .claude/ .context/ \
    OR  exit_1("[CRITICAL] D8 content-safety: prompt-injection indicator or scanner error (REQ-052)")
  # POST-D8 artifact is "explicit-pattern-scanned", NOT "content-safe" (R-004/ADR-PROJ031-003 D8)
  # Semantic/implicit injection is a KNOWN UNMITIGATED RESIDUAL bounded by REQ-051 two-reviewer

STEP g9-produce-deterministic-artifact:
  # FM-002-i2 RUNNER IMAGE CONSTRAINT (MANDATED — design level):
  # The generate-and-gate job MUST specify a pinned OS image (e.g., runs-on: ubuntu-24.04).
  # ubuntu-latest is FORBIDDEN for this job. Rationale: git archive pax header format is
  # git-version-dependent. If cowork-skeleton.yml (generation) and cowork-monitor.yml
  # (m1-5 re-derivation) run on different git binary versions, ATTESTED_DIGEST ≠ LIVE_DIGEST
  # → false CRITICAL tamper alarms on every monitor run (FM-002-i2, RPN 336).
  # BOTH workflows MUST pin the SAME OS image. See CI-G-007.
  # Archive the deterministic commit (not a bare tree) so mtime = committer date (ADR-PROJ031-001/ADR-PROJ031-003 D4):
  artifact = git archive --format=tar "${COMMIT_SHA}"
  # If compressed: MUST use gzip -n (strips mtime+OS byte) or digest is non-deterministic
  # Exact flag set and compression choice: Phase 6 implementation detail (pending eng-infra, §3 of gen design)
  artifact_digest = sha256(artifact)

  # Create git bundle for state transfer to push-and-release job (Phase 6 implementation detail):
  git bundle create <bundle-file> HEAD  # packages the commit for restore in Job C

  # Upload both to GitHub Actions artifact store (SHA-pinned actions/upload-artifact):
  upload_artifact(artifact, <bundle-file>)

  # Record expected_tip_sha in release metadata for monitor tree-digest match (M1 step 2):
  echo "COMMIT_SHA=${COMMIT_SHA}" >> job outputs   # used by push job and monitor

# ═══ Job B: attest ════════════════════════════════════════════
# permissions: id-token: write, attestations: write  (NO contents: write — REQ-020(b))
# needs: generate-and-gate

STEP download-artifact:
  download_artifact(<artifact-file>)   # SHA-pinned actions/download-artifact

STEP gh-attest:
  # File subject — bare SHA is NOT a valid subject (CV-005/R-006):
  gh attestation attest <artifact-file> --repo geekatron/jerry
  # Non-zero exit → push-and-release job is SKIPPED (needs: attest dependency)
  # No live-but-unattested artifact can exist (ADR-PROJ031-003 D4 ordering constraint)

# ═══ Job C: push-and-release ══════════════════════════════════
# permissions: contents: write (sole — REQ-020(a); no id-token: write, no attestations: write)
# environment: skeleton-push  (REQ-045: App credential gated to main/v* only)
# needs: attest

STEP mint-app-token:
  # App installation token (preferred) or deploy key (alternative) (REQ-041/ADR-PROJ031-003 D3):
  # 1h fixed expiry (CV-004); scoped to geekatron/jerry-claude-plugin contents: write ONLY
  # Classic PAT: REJECTED (ADR-PROJ031-003 D3)
  # NEVER echo token to logs or $GITHUB_STEP_SUMMARY (REQ-019)
  DEDICATED_TOKEN = gh_app_mint_installation_token(APP_ID, PRIVATE_KEY, repo=geekatron/jerry-claude-plugin)

STEP download-bundle-and-artifact:
  download_artifact(<artifact-file>, <bundle-file>)
  git bundle verify <bundle-file>
  git fetch <bundle-file> HEAD:refs/remotes/bundle/HEAD   # restore git objects
  # ROOT-4 / FM-037-QG3: reposition HEAD to the generated skeleton commit before push.
  # Without this step, HEAD points at the source repo's tip (not G6_SHA) and the push
  # sends the wrong commit to the dedicated repo — breaking the CI-G-001 digest invariant.
  git checkout refs/remotes/bundle/HEAD                   # HEAD = G6_SHA (CI-G-001)
  # SHA integrity assertion: confirm restored HEAD matches the COMMIT_SHA from Job A output.
  RESTORED_SHA = git rev-parse HEAD
  ASSERT RESTORED_SHA == COMMIT_SHA  \
    OR  exit_1("[CRITICAL] Bundle restore SHA mismatch: expected ${COMMIT_SHA}, got ${RESTORED_SHA} — CI-G-001 integrity breach")

STEP cross-repo-force-push:
  # NO continue-on-error: true (REQ-037)
  git push --force \
    "https://x-access-token:${DEDICATED_TOKEN}@github.com/geekatron/jerry-claude-plugin.git" \
    HEAD:<default-branch>

STEP publish-immutable-release:
  gh release create v{N} <artifact-file> \
    --repo geekatron/jerry-claude-plugin \
    --title "Jerry CoWork Skeleton ${TAG}" \
    --notes "Source-Commit: ${COMMIT_SHA}\nSource-Tag: ${TAG}"
  # Immutable release asset — the durable, CI-only-writable integrity surface (REQ-042)
  # Records expected_tip_sha as Source-Commit for D7 monitor tree-digest binding

STEP push-failure-detection:
  # if: failure()   (REQ-037)
  emit_structured_diagnostic(
    raw_push_exit_code,
    git_remote_rejection_message,
    "See REQ-040 (org-level ruleset) and ADR-PROJ031-003 §Credential Strategy for remediation"
  ) >> $GITHUB_STEP_SUMMARY

STEP job-summary:
  # if: always()   (REQ-016)
  emit_job_summary(TAG, COMMIT_SHA, artifact_digest, gate_results) >> $GITHUB_STEP_SUMMARY
```

---

## cowork-monitor.yml Design

### Triggers

```
on:
  schedule:
    - cron: '0 */6 * * *'    # Every 6 hours (≤6h cadence, REQ-035/NFR-006)
  workflow_dispatch:           # Manual trigger for testing and recovery

# FM-005-i2 FIX: concurrency group serializes cowork-monitor.yml runs to prevent TOCTOU race.
# Without this, two concurrent runs (e.g., scheduled + workflow_dispatch, or two overlapping
# schedules) can both read REVERT_ATTEMPT_COUNT < MAX_AUTO_REVERTS before either has finished
# writing, causing both to dispatch a revert — exceeding the cap and corrupting the counter.
# cancel-in-progress: false is REQUIRED (not true): cancelling an in-flight run would abandon
# its counter increment mid-flight, which is exactly the race this block is designed to prevent.
concurrency:
  group: cowork-monitor
  cancel-in-progress: false

# Source repo (geekatron/jerry), main branch  (ADR-PROJ031-003 D7)
# NOT in the dedicated repo (would be overwritten by each force-push — FM-015)
# NOT event-driven cross-repo (platform-impossible — ADR-PROJ031-003 D7 rationale)
```

### Job M1: Integrity and Freshness Pseudocode

**Permissions (before G-actions-write-safe):** `issues: write, contents: write`
**Permissions (after G-actions-write-safe):** add `actions: write`

```
# ROOT-1 / DA-001 fix: 8-step digest-based monitor (mirrors phase3-attestation-provenance-design.md
# §3.3 MONITOR HAND-OFF exactly). The prior design was WRONG in TWO ways:
#   (a) verify-attestation: did not specify --signer-workflow flag (workflow substitution gap).
#   (b) bind-to-live-tip: read G6_SHA from mutable release-body via jq '.body' → condemned by
#       ADR-PROJ031-003 SC-04 (mutable metadata); also used SHA comparison rather than digest comparison.
# The corrected binding invariant (from eng-infra):
#   sha256(git archive --format=tar <live G6_SHA>)
#     == sha256(published jerry-claude-plugin-${TAG}.tar release asset)
#     AND gh attestation verify <published tar> exits 0
#     AND LATEST source v* tag deployed within ≤ 2h
# The SLSA predicate gitCommit field records SRC_SHA (source trigger commit), NOT G6_SHA
# (generated skeleton commit). SRC_SHA ≠ G6_SHA always in Option A. NEVER compare them.
# No --format json, no jq predicate parsing — predicate is metadata only, NOT the verification key.

STEP m1-1-download-attested-artifact:
  # Step 1 of 8 — download published TAR from immutable release on SOURCE repo (geekatron/jerry):
  LATEST_TAG = resolve_latest_deployed_tag()    # see freshness-check below for derivation
  gh release download "${LATEST_TAG}" \
    --repo geekatron/jerry \
    --pattern "jerry-claude-plugin-${LATEST_TAG}.tar" \
    --dir "${WORK_DIR}"
  # Missing release asset → FAIL-CLOSED (FM-033):
  ASSERT exists("${WORK_DIR}/jerry-claude-plugin-${LATEST_TAG}.tar") AND non-empty \
    OR  exit_1("[CRITICAL] D7 monitor: release asset absent for ${LATEST_TAG} — cannot verify")

STEP m1-2-verify-attestation:
  # Step 2 of 8 — Sigstore exit-code is the SOLE integrity verdict (D7a / REQ-035 / ADR-PROJ031-003 D7):
  # File subject — bare SHA is NOT valid (CV-005/R-006). --signer-workflow rejects
  # attestations from any other workflow (defense-in-depth against workflow substitution).
  gh attestation verify "${WORK_DIR}/jerry-claude-plugin-${LATEST_TAG}.tar" \
    --repo geekatron/jerry \
    --signer-workflow .github/workflows/cowork-skeleton.yml
  # Non-zero exit → tamper or policy mismatch → FAIL-CLOSED. NO --format json / jq parsing.
  IF $? != 0:
    open_github_issue("[CRITICAL] D7 monitor: gh attestation verify failed for ${LATEST_TAG} — SC-04 path open")
    exit 1

STEP m1-3-compute-attested-digest:
  # Step 3 of 8 — ATTESTED_DIGEST is the verification key (not the SLSA predicate gitCommit):
  ATTESTED_DIGEST = sha256sum "${WORK_DIR}/jerry-claude-plugin-${LATEST_TAG}.tar" | cut -d' ' -f1
  ASSERT non-empty(ATTESTED_DIGEST)  \
    OR  exit_1("[CRITICAL] D7 monitor: sha256 of downloaded TAR returned empty — FAIL-CLOSED")

STEP m1-4-read-live-tip-sha:
  # Step 4 of 8 — read-only, no full clone (CV-006 / ADR-PROJ031-003 D7 no-clone constraint):
  G6_SHA = git ls-remote https://github.com/geekatron/jerry-claude-plugin.git HEAD | cut -f1
  ASSERT non-empty(G6_SHA)  \
    OR  exit_1("[CRITICAL] D7 monitor: git ls-remote returned empty HEAD — dedicated repo unreachable")

STEP m1-5-shallow-fetch-live-tar:
  # Step 5 of 8 — re-derive the TAR from the live tip (shallow fetch, not full clone — CV-006):
  # --depth=1 fetches only tree+blob objects for the tip commit; no history traversal.
  # FM-002-i2 RUNNER IMAGE CONSTRAINT (MANDATED — design level):
  # This step MUST run on the SAME pinned OS image used in cowork-skeleton.yml G9
  # (e.g., ubuntu-24.04). ubuntu-latest is FORBIDDEN here.
  # git archive pax header format is git-version-dependent; runner drift between the
  # generation job and this monitor step causes ATTESTED_DIGEST ≠ LIVE_DIGEST false tamper
  # alarms (FM-002-i2, RPN 336). See CI-G-007 for the pinning mandate and tree-hash option.
  git init --bare "${WORK_DIR}/cowork-fetch.git"
  git -C "${WORK_DIR}/cowork-fetch.git" fetch --depth=1 \
    "https://github.com/geekatron/jerry-claude-plugin.git" "${G6_SHA}"
  git -C "${WORK_DIR}/cowork-fetch.git" archive --format=tar "${G6_SHA}" \
    > "${WORK_DIR}/live-tip.tar"
  # Fetch/archive failure → FAIL-CLOSED:
  ASSERT exists("${WORK_DIR}/live-tip.tar") AND non-empty \
    OR  exit_1("[CRITICAL] D7 monitor: shallow-fetch or git-archive of live tip failed")
  # PHASE-6 RESIDUAL (P-022 / CI-G-007): byte-idempotency of shallow-fetch + git archive
  # MUST be empirically confirmed on the pinned OS image (same image in both workflows).
  # Runner image pinning (FM-002-i2 fix) eliminates git version drift; the empirical test
  # verifies no remaining source of non-determinism. See CI-G-007 for the tree-hash binding
  # as an alternative Phase-6 hardening path (content-addressed; git-version-stable).

STEP m1-6-compute-live-digest:
  # Step 6 of 8:
  LIVE_DIGEST = sha256sum "${WORK_DIR}/live-tip.tar" | cut -d' ' -f1
  ASSERT non-empty(LIVE_DIGEST)  \
    OR  exit_1("[CRITICAL] D7 monitor: sha256 of live-tip TAR returned empty — zero-byte or missing")

STEP m1-7-tree-digest-assert:
  # Step 7 of 8 — THE correct binding invariant (ROOT-1 fix / INF-07):
  # Tamper on the dedicated branch changes the tree → changes the TAR digest → mismatch → CRITICAL.
  # The SLSA predicate gitCommit (= SRC_SHA from geekatron/jerry) is NEVER compared to G6_SHA:
  #   they differ by design in Option A and that comparison is semantically wrong.
  IF ATTESTED_DIGEST != LIVE_DIGEST:
    open_github_issue(
      title="[CRITICAL] D7 monitor: tree-digest mismatch on geekatron/jerry-claude-plugin",
      body="ATTESTED=${ATTESTED_DIGEST} vs LIVE(G6=${G6_SHA})=${LIVE_DIGEST}. Tamper or failed regeneration."
    )
    exit 1   # fail-closed (FM-033)

STEP m1-8-freshness-check:
  # Step 8 of 8 — a green digest match on a STALE tip is a FRESHNESS FAILURE (IN-002 / REQ-049):
  latest_src_tag = git ls-remote --tags https://github.com/geekatron/jerry.git 'refs/tags/v*' \
    | sort -t/ -k3 -V | tail -1 | cut -f2 | sed 's|refs/tags/||'
  # FM-001-i2 FIX: NEVER source tag time from .committer.date on the tag object.
  # For annotated tags (which Jerry version-bump.yml creates via gh release create),
  # dereferencing .object.url yields the annotated tag object — it has {tagger: {date:...}}
  # but NO .committer field. .committer.date returns null → parse_time(null) → epoch(0) →
  # elapsed ≈ 1.75B s >> 2h → persistent false freshness-CRITICAL on every monitor run (RPN 343).
  # FORBIDDEN: gh api .../git/refs/tags/${tag} | jq '.object.url' | xargs gh api | jq '.committer.date'
  # CORRECT SOURCES (priority order):
  #   (1) GitHub Release publishedAt — always populated for any gh release create, tag-type agnostic:
  latest_src_tag_time = gh release view "${latest_src_tag}" --repo geekatron/jerry \
    --json publishedAt | jq -r '.publishedAt'
  IF latest_src_tag_time is null OR empty:
    #   (2) Tagged commit committer date — git-version-stable, works pre-release or lightweight tags:
    latest_src_tag_time = git log -1 --format=%cI "${latest_src_tag}^{commit}"
  IF latest_src_tag_time is null OR empty:
    exit_1("[CRITICAL] D7 freshness: cannot resolve tag time for ${latest_src_tag} — FAIL-CLOSED")
  deployed_release_version = gh api repos/geekatron/jerry-claude-plugin/releases/latest | jq -r '.tag_name'
  IF latest_src_tag != deployed_release_version:
    elapsed = now() - parse_time(latest_src_tag_time)
    IF elapsed > 2h:
      # ROOT-6c suppression (PM-004-Q3): before firing a freshness CRITICAL, check whether
      # latest_src_tag has an open generation-failure escalation issue. If yes, the stale state
      # is KNOWN and under human management — suppress the freshness CRITICAL.
      # FM-003-i2 FIX: suppression MUST set LGV_SKIP=true to block advance-last-good-validated.
      # ${latest_src_tag} is undeployed/failing and MUST NEVER become last-good-validated.
      escalation_open = count_open_issues(label="generation-failure-escalation:${latest_src_tag}")
      IF escalation_open > 0:
        LGV_SKIP = true   # FM-003-i2: blocks advance-last-good-validated step below
        emit_to_GITHUB_STEP_SUMMARY("[INFO] D7 freshness: ${latest_src_tag} stale but generation-failure escalation open — suppressed CRITICAL, human managing; last-good-validated advancement BLOCKED")
        # Do NOT exit 1; proceed to emit-summary. advance-last-good-validated SKIPPED via LGV_SKIP.
      ELSE:
        open_github_issue("[CRITICAL] D7 monitor: freshness failure — ${latest_src_tag} not deployed; ${deployed_release_version} deployed")
        exit 1   # fail-closed (FM-033)

STEP advance-last-good-validated:
  # FM-003-i2 FIX — INVARIANT (ADR-PROJ031-003 D7 / REQ-053 last-good-validated lifecycle):
  # last-good-validated advances ONLY when ALL three conditions hold simultaneously:
  #   (1) Attestation verified — gh attestation verify exited 0 (Step 2)
  #   (2) Digest match — ATTESTED_DIGEST == LIVE_DIGEST (Step 7)
  #   (3) Freshness SATISFIED — LGV_SKIP is not set (no open generation-failure escalation)
  # A tag with an open generation-failure-escalation MUST NEVER become last-good-validated.
  # In the suppressed path LGV_SKIP=true (set in m1-8); this step becomes a no-op.
  IF LGV_SKIP:
    emit_to_GITHUB_STEP_SUMMARY("[INFO] D7: last-good-validated unchanged (freshness suppressed; ${latest_src_tag} undeployed/failing — cannot advance)")
    # No state change; last-good-validated remains at the previously verified version.
  ELSE:
    # Advance to ${deployed_release_version} — the version whose digest was verified in Step 7.
    # In the fully passing path, deployed_release_version == latest_src_tag; using
    # deployed_release_version is explicit about what was actually verified.
    git tag -f last-good-validated ${deployed_release_version}
    git push origin refs/tags/last-good-validated --force
    # Requires contents: write on source repo GITHUB_TOKEN (see CI-G-005 / L2 §Permissions nuance)

STEP emit-summary:
  # if: always()
  emit_to_GITHUB_STEP_SUMMARY(
    verified_tip_sha=expected_tip_sha,
    attestation_result,
    freshness_result,
    last_good_validated_tag
  )
  # REQ-035 AC: records tip SHA, attestation result, freshness result on every run

STEP fail-closed-catch:
  # Catch-all for unhandled internal errors (FM-033):
  # Any code path that reaches this step after an unhandled exception:
  #   → exit 1 + CRITICAL issue
  # The monitor MUST NOT silently exit 0 on internal error
```

### Job M2: Auto-Revert

**Status before G-actions-write-safe:** OMITTED from workflow YAML. M1 opens a CRITICAL issue for human escalation only. No `actions: write` declared.

**Status after G-actions-write-safe:** job added to workflow with `actions: write`.

```
# if: failure() from integrity-and-freshness (M1)
# permissions (post-G-actions-write-safe): actions: write
# Monitor pushes NOTHING directly to dedicated repo (loop-safe, CR-02)

STEP auto-revert:
  # ROOT-6 / PM-004-Q3 / FM-022-QG3: circuit breaker for infinite-revert loop.
  # Without a cap: vN fails → revert to vN-1 → freshness check: vN still not deployed → CRITICAL
  # → revert to vN-1 again → ... endless loop; users permanently stale; no escalation ever.

  LATEST_SRC_TAG = resolve_latest_source_v_tag()  # same derivation as freshness-check
  last_good_tag = git describe --tags --exact-match $(git rev-parse last-good-validated)
  # If last-good-validated not yet defined: escalate to human, no dispatch (no change).
  IF last_good_tag is undefined:
    open_github_issue("[CRITICAL] D7 monitor: last-good-validated undefined — cannot auto-revert; HUMAN ESCALATION REQUIRED")
    exit 1

  # (a) Revert attempt cap — tracked via GitHub Issue labels per source tag:
  MAX_AUTO_REVERTS = 3  # configurable; document in runbooks/org-registration.md §Auto-Revert Cap
  # FM-004-i2 FIX: count ALL issues (open AND closed) using --state all.
  # FORBIDDEN: count_open_issues (--state open) — a maintainer who manually closes the
  # auto-revert label issue silently resets the counter to 0, re-arming the infinite-revert
  # loop the circuit breaker was designed to stop. Monotonic counting (all states) makes
  # closing an issue irrelevant to the cap: once MAX_AUTO_REVERTS label-bearing issues exist
  # in ANY state (open or closed), the cap is permanently enforced.
  REVERT_ATTEMPT_COUNT = gh issue list \
    --repo geekatron/jerry \
    --state all \
    --label "auto-revert:${LATEST_SRC_TAG}" \
    | wc -l

  # (b) Circuit breaker: cap exceeded → halt auto-revert, escalate to human:
  IF REVERT_ATTEMPT_COUNT >= MAX_AUTO_REVERTS:
    open_github_issue(
      title="[CRITICAL] D7 monitor: auto-revert cap exceeded for ${LATEST_SRC_TAG} — HUMAN ESCALATION REQUIRED",
      body="Auto-revert dispatched ${REVERT_ATTEMPT_COUNT}x for ${LATEST_SRC_TAG}; cap=${MAX_AUTO_REVERTS}. "
           "Automatic revert HALTED. Manual investigation required. Do NOT trigger further reverts "
           "until root cause is identified and the generation-failure-escalation issue is resolved.",
      labels=["auto-revert:${LATEST_SRC_TAG}", "generation-failure-escalation:${LATEST_SRC_TAG}"]
    )
    # generation-failure-escalation label suppresses freshness CRITICAL in M1 (ROOT-6c)
    exit 1   # stop; do not dispatch another revert

  # Dispatch re-generation of last-good-validated through normal gated path:
  # (REQ-053 / ADR-PROJ031-003 D7 auto-revert topology)
  gh workflow run cowork-skeleton.yml --field target_tag=${last_good_tag}
  # Re-generation path: D5 → D6 → D8 → attest → push (no gate bypass)
  # Loop-safety: source monitor → cowork-skeleton.yml → dedicated repo
  #   → (dedicated repo has no push-back workflows — CR-02) → source repo
  open_github_issue(
    title="[CRITICAL] D7 monitor: auto-revert dispatched (attempt ${REVERT_ATTEMPT_COUNT+1}/${MAX_AUTO_REVERTS}) for ${last_good_tag}",
    labels=["auto-revert:${LATEST_SRC_TAG}"]   # increments cap counter
  )
```

### Job M3: Clone-Weight Telemetry

```
# permissions: contents: read (dedicated repo is public)
# Separate job, non-blocking, distinct from integrity authority (ADR-PROJ031-003 D7 / CV-006)

STEP timed-reference-clone:
  START = now()
  git clone --depth=1 https://github.com/geekatron/jerry-claude-plugin.git /tmp/cowork-clone
  CLONE_SECS = now() - START
  PACK_SIZE_MB = du -sm /tmp/cowork-clone/.git | cut -f1

  emit_to_GITHUB_STEP_SUMMARY(pack_size_mb=PACK_SIZE_MB, clone_secs=CLONE_SECS)

  # Non-blocking early warnings (REQ-034d):
  IF PACK_SIZE_MB >= 150:
    open_informational_issue("[INFO] clone-weight: pack ${PACK_SIZE_MB}MB approaching 250MB trigger")
  IF CLONE_SECS >= 40:
    open_informational_issue("[INFO] clone-weight: clone ${CLONE_SECS}s approaching 60s hard-fail")

  rm -rf /tmp/cowork-clone   # immediately discarded; no integrity authority
```

### Meta-Monitor (`cowork-meta-monitor.yml` — Separate Workflow)

```
# MUST be a separate workflow — if cowork-monitor.yml fails entirely,
# a meta-monitor JOB inside it also fails (FM-033 gap if co-located)
# Trigger: schedule ≤24h
# permissions: issues: write

STEP check-monitor-liveness:
  # Verify cowork-monitor.yml ran successfully within prior 25h (REQ-044):
  last_success = gh run list --workflow cowork-monitor.yml \
    --status success --limit 1 | jq -r '.[0].createdAt'
  IF now() - parse_time(last_success) > 25h:
    open_informational_issue("[INFO] meta-monitor: cowork-monitor.yml has not run in >25h")
```

---

## G-actions-write-safe Enforcement

G-actions-write-safe is the named gate in ADR-PROJ031-003 and REQ-053 that must clear before `actions: write` is granted to the monitor workflow for auto-revert dispatch. This prevents the RT-002 compound path (unpinned Action + `actions: write` + pre-G-provenance D5 gap → rogue dispatch).

### Gate Conditions (both must hold)

| Condition | Verification | REQ |
|-----------|-------------|-----|
| (i) ALL `.github/workflows/` files have SHA-pinned Actions | `grep -rn '@v[0-9]' .github/workflows/` returns empty | REQ-017 |
| (ii) G-provenance PASSED | REQ-038 ancestor assertion + REQ-039 `v*` tag protection operational on live pipeline | REQ-038/039 |

**Scope (i) explicitly includes:**
- `cowork-skeleton.yml` (all three jobs)
- `cowork-monitor.yml` (all jobs)
- `cowork-meta-monitor.yml`
- All other existing workflows: `release.yml`, `docs.yml`, `version-bump.yml`, `ci.yml`

### SHA-Pin Enforcement

Every `uses:` line in all workflow files must reference a full 40-character commit SHA:

```
# CORRECT (REQ-017):
uses: actions/checkout@8ade135a41bc57ef5f3b8e7e2d5b71a18e5d9d6  # v4.1.0

# FORBIDDEN (REQ-017):
uses: actions/checkout@v4
uses: actions/checkout@v4.1.0
```

**Enforcement mechanism:**
- Phase 6 implementation: `grep -rn '@v[0-9]' .github/workflows/` in CI as a blocking check
- Dependabot configured to update SHA pins automatically (ADR-PROJ031-003 D6 item 3)
- G-actions-write-safe clearance: documented in `security/phase5-gate-evidence.md`

### Workflow Evolution After G-actions-write-safe

When G-actions-write-safe clears, `cowork-monitor.yml` is updated to add:
1. `permissions: actions: write` on the Job M2 job (or the workflow-level if only M2 needs it)
2. The Job M2 auto-revert step body (previously omitted)

This is a deliberate two-phase evolution: the workflow ships in human-escalation mode and graduates to auto-revert only when the compound-path dependency is satisfied.

---

## Hook Bypass Note

**R-001 finding from phase3-skeleton-generation-design.md:** `git commit --no-verify` is used in G6 (the deterministic commit step).

**Rationale:** The generation commit is a machine-controlled git operation producing a clean, deterministic artifact. Developer pre-commit hooks (linting, test execution, secrets scanning) are designed for human-authored code commits — not for an automated, formula-driven commit that has already passed the security gate train (D5, D6, D8). Running pre-commit hooks would:
1. Potentially break determinism if hooks modify files
2. Add indeterminate execution time to a CI workflow
3. Apply human-workflow policies to a machine-workflow step that is already gated differently

**Safe because:** The `--no-verify` bypasses only local git hooks. The security properties of the committed content are guaranteed by the upstream D5/D6/D8 gates, not by the commit hook. The secret scan (D6) runs before G6, so `--no-verify` does not bypass secret scanning.

---

## L2: Architectural Implications

### 1. The Three-Job Permission Isolation Is the Primary Security Property

The separation of attestation (`id-token: write + attestations: write`) from the push (`contents: write`) into distinct jobs is the key structural security control from ADR-PROJ031-003 D4 A-1 / REQ-020. A workflow that grants both in the same job (or at the workflow level) would allow the OIDC capability to be used alongside write access — a broader surface. The job dependency (`needs: attest`) also creates a hard ordering gate: if attestation fails, the push job is structurally skipped, not conditionally skipped. This cannot be accidentally bypassed by a `continue-on-error: true` on a single step.

### 2. The Monitor's Trust Position Is an Inherent Limitation

The D7 monitor shares its trust root with the generation pipeline — both run on source `main` under source-repo governance. A full compromise of `main`'s ruleset would compromise both. This is intrinsic to a "CI is the trusted builder" model. The external Sigstore transparency log (D4) is the only reference value that sits outside this trust root — which is exactly why `gh attestation verify` against that log is the integrity anchor, and a compromised monitor cannot forge a passing attestation for a tampered tree.

### 3. SLSA Trajectory

The three-job job graph, the Sigstore-backed build-provenance attestation, and the immutable release publishing put this pipeline on an **SLSA Level 3 trajectory**: hardened build platform, non-forgeable signed provenance, and a publicly verifiable attestation anchored in an immutable external log. The per-job permission isolation is a Level 3 control (isolation between high-privilege and write-privilege steps). A consumer-side verification hook in CoWork would close the RTB-5 gap (no install-time verification) and complete the SLSA end-to-end chain — currently the monitor is the sole automated verifier.

### 4. Phase 6 Gaps Surfaced in This Design

The following items are **not gaps in the architecture** (those are settled in ADR-PROJ031-003) but are **Phase 6 implementation details requiring explicit resolution before writing production YAML:**

| Gap ID | Description | Phase 6 Action |
|--------|-------------|----------------|
| CI-G-001 | **Git state transfer between jobs — bundle HEAD checkout (ROOT-4 fix applied).** The `git bundle` mechanism is specified including the `git checkout refs/remotes/bundle/HEAD` step and SHA assertion (FM-037-QG3). Bundle round-trip byte-idempotency must be empirically confirmed: two runs of Job C for the same tag must restore identical COMMIT_SHA values, and `git ls-remote jerry-claude-plugin HEAD` post-push must equal COMMIT_SHA. | Phase 6: test bundle round-trip including HEAD checkout; confirm post-push tip SHA matches expected COMMIT_SHA |
| CI-G-002 | ~~`derive_expected_tip` via Source-Commit release trailer~~ — **REMOVED (ROOT-1 / DA-001 fix).** The release-body jq parsing approach was condemned by ADR-PROJ031-003 SC-04. Replaced by the 8-step digest-based monitor that downloads the published TAR, sha256s it, re-derives a TAR from the live tip via shallow fetch + git archive, and compares digests. No release-body parsing anywhere in the monitor. | N/A — replaced by CI-G-007 |
| CI-G-003 | **D8 scanner tool and pattern catalog (ROOT-5 partial fix).** The pattern catalog PATH is now specified (`runbooks/content-safety-patterns.md`). The CONTENT (C1–C6 patterns) remains an eng-architect deliverable. The scanner invocation structure is specified (--patterns, --fail-on-match, --fail-on-error). The concrete tool name and final flags are Phase-6 details. | Phase 6: consume eng-architect C1–C6 catalog content; confirm tool name and flags; G-content Phase-5 gate BLOCKER |
| CI-G-007 | **Shallow-fetch + git archive byte-idempotency (FM-002-i2 — design constraint mandated).** Runner image pinning is REQUIRED at design level: both the G9 `git archive` step in `cowork-skeleton.yml` and the m1-5 shallow-fetch `git archive` step in `cowork-monitor.yml` MUST use the SAME pinned OS image (e.g., `ubuntu-24.04`). `ubuntu-latest` is FORBIDDEN for these steps — git archive pax header format is git-version-dependent; runner drift causes false CRITICAL tamper alarms (FM-002-i2, RPN 336). The empirical byte-stability test MUST use the pinned image in both workflows. **Phase-6 hardening option (recommended, not mandated at design level):** git-tree-object-hash binding — `git rev-parse <tip>^{tree}` is content-addressed and git-version-stable; using tree-hash comparison in the monitor eliminates the byte-idempotency dependency on `git archive` format entirely. If adopted, it changes the attestation/verification binding and requires **eng-infra** sign-off before Phase-6 implementation. | Phase 6: two-run idempotency test using pinned `ubuntu-24.04` in both workflows (REQ-003 AC; NFR-001 AC); engage eng-infra before implementing tree-hash binding if preferred |
| CI-G-004 | **Exact `git archive` flags and compression.** Phase 6 resolves with eng-infra the final flag set, whether to compress (and if so, enforce `gzip -n`), and the attestation tool invocation form (`gh attestation attest` vs `actions/attest-build-provenance@SHA`). Determinism contract (§3 of generation design) must be preserved. | Phase 6: validate artifact_digest stability across two independent workflow runs for same tag |
| CI-G-005 | **`cowork-monitor.yml` `contents: write` for `last-good-validated`.** The monitor is described as "read-only" with respect to the dedicated repo, but advancing `last-good-validated` requires writing a tag to the SOURCE repo (GITHUB_TOKEN `contents: write`). This is not a contradiction — "read-only" scopes to the dedicated repo — but the source-repo `contents: write` on the monitor job must be explicitly declared and REQ-017 SHA-pin applies to all Actions in that job. | Phase 6: declare `contents: write` on M1 explicitly; confirm SHA-pin status of all Actions used in M1 |
| CI-G-006 | **Meta-monitor co-location risk.** If `cowork-meta-monitor.yml` is accidentally co-located as a job in `cowork-monitor.yml`, a total `cowork-monitor.yml` failure also suppresses the meta-monitor — violating the watchdog independence requirement. | Phase 6: implement meta-monitor as a physically separate `.yml` file; add a CI check that no `cowork-monitor.yml` job is named `meta-monitor` |

### 5. Residuals Inherited From ADR-PROJ031-003 (Not New)

These are known, disclosed residuals from the input documents — not new findings:
- RTB-1: Org-owner ruleset-suppression — detect-and-respond only
- RTB-2: Trusted-maintainer rogue build — bounded by REQ-051 two-reviewer, not eliminated
- RTB-4: App private key custody — bounded by REQ-045/REQ-048 environment + rotation
- RTB-5: No install-time attestation verification — monitor is sole verifier

---

## Traceability Matrix

| Design Element | REQ | ADR | Gate |
|----------------|-----|-----|------|
| Tag triggers + workflow_dispatch + optional target_tag input | REQ-011 | ADR-PROJ031-003 D6 | — |
| Concurrency group, cancel-in-progress: false | REQ-015 | — | — |
| cowork-monitor.yml concurrency group (group: cowork-monitor, cancel-in-progress: false) — FM-005-i2 FIX: serializes monitor runs; two concurrent runs cannot both read REVERT_ATTEMPT_COUNT < MAX and both dispatch; cancel-in-progress: false prevents mid-flight counter abandonment | REQ-015 | FM-005-i2 | — |
| Per-job permissions isolation (three jobs) | REQ-020 | ADR-PROJ031-003 D4 A-1 | — |
| environment: skeleton-push fast-fail gate | REQ-045 | ADR-PROJ031-003 RTB-4 | G-provenance |
| Event-discriminated tag resolve + env: binding | REQ-036 | ADR-PROJ031-001 IT3-005 | — |
| D5 provenance assertion (merge-base, before G3) | REQ-038 | ADR-PROJ031-003 D5 | G-provenance |
| v* tag-protection ruleset on source repo | REQ-039 | ADR-PROJ031-003 D5 | G-provenance |
| G3 checkout fetch-depth: 0 | REQ-007 | ADR-PROJ031-001 §Determinism | — |
| G4 denylist strip (projects/ + tests/) | REQ-002 | ADR-PROJ031-001 c-003 | — |
| G5 static stub + version sentinel (no dynamic content) | REQ-004/004a | ADR-PROJ031-001 c-006 | — |
| G6 deterministic commit (pinned dates via same-step inline OR $GITHUB_ENV — ROOT-2 / FM-007-QG3) | REQ-003/008 | ADR-PROJ031-001 §Regeneration; gen-design §2 G6 | — |
| G7 retention completeness (plugin.json-derived); projects/ == {README.md, .jerry-skeleton-version} — ROOT-3 | REQ-005/010 | ADR-PROJ031-001 R-008; gen-design §3(c) FM-020-QG3 | — |
| G8 multi-dim gate (file-count ∧ pack ∧ clone), two bands | REQ-006/034d/050 | ADR-PROJ031-001 §Clone-Weight | G-headroom |
| D6 faithful-derivative gate (TAG..HEAD, not mutable branch) | REQ-022 | ADR-PROJ031-003 D6 / FM-09 | — |
| D6 ':!projects/' covers BOTH known-injected members (stub + sentinel) — ROOT-3 / FM-020-QG3 | REQ-022 | gen-design §3(c) | — |
| D6 secret scan before push | REQ-022 | ADR-PROJ031-003 D6 V-05 | — |
| c-007 retention/dup-skill gate (STEP c007-retention-and-skill-name-validation): skills/.graveyard/ + .github/ absent; pyproject.toml + uv.lock present (c-008); SKILL.md names unique in tip — fail-closed; positioned after D6, before D8 + attestation (Mirror Hand-Off 2026-07-02) | REQ-056 | ADR-PROJ031-001 c-007/c-008; Mirror Hand-Off 2026-07-02 | — |
| plugin-smoke check (STEP plugin-smoke-check): plugin.json + marketplace.json valid JSON; declared skills resolve to SKILL.md; uv run jerry entrypoint reachable (src/ retained per c-008) — fail-closed, before D8 + attestation (empirical lesson 2026-07-02) | REQ-056 | ADR-PROJ031-001 c-007/c-008; 2026-07-02 install validation | — |
| D8 content-safety scan: pattern catalog at runbooks/content-safety-patterns.md, fail-closed on match OR error | REQ-052 | ADR-PROJ031-003 D8 / PM-003-Q3 ROOT-5 | G-content |
| D8 explicit-pattern-scanned ≠ content-safe disclosure | REQ-052 | ADR-PROJ031-003 D8 R-004 | G-content |
| G9 git archive of deterministic commit (gzip-n trap) | REQ-042 | ADR-PROJ031-003 D4 / R-006 | — |
| Attestation job (id-token+attestations, no contents: write) | REQ-042 | ADR-PROJ031-003 D4 | G-monitor |
| Attestation precedes push (job dependency ordering) | REQ-042 | ADR-PROJ031-003 D4 C-7 | G-monitor |
| gh attestation attest <file> (not bare SHA) | REQ-042 | ADR-PROJ031-003 D4 CV-005 | G-monitor |
| App token mint (1h, dedicated-repo only) | REQ-041 | ADR-PROJ031-003 D3 | G-prevention |
| Cross-repo force-push (no continue-on-error) | REQ-041/037 | ADR-PROJ031-003 D3 | G-prevention |
| Push failure detection step (if: failure()) | REQ-037 | ADR-PROJ031-003 D6 | — |
| Job summary (if: always()) | REQ-016 | — | — |
| SHA-pin all Actions in ALL .github/workflows/ files | REQ-017 | ADR-PROJ031-003 D6 / RT-002 | G-actions-write-safe |
| cowork-monitor.yml scheduled ≤6h, source repo main | REQ-035 | ADR-PROJ031-003 D7 | G-monitor |
| D7 monitor 8-step digest binding: download tar → gh attestation verify --signer-workflow → sha256(tar) == sha256(shallow-fetch live-tip tar) → freshness (ROOT-1 / DA-001 fix) | REQ-035 | ADR-PROJ031-003 D7; attestation-design §3.3 MONITOR HAND-OFF INF-07 | G-monitor |
| gh attestation verify <artifact-file> --repo geekatron/jerry --signer-workflow .github/workflows/cowork-skeleton.yml (file subject; no --format json; no SLSA predicate parsing) | REQ-035 | ADR-PROJ031-003 D7 CV-005; attestation-design §3.1 | G-monitor |
| Tree-digest: sha256(shallow-fetch git archive of live tip) == sha256(attested published tar) (no SHA comparison, no release-body parsing — ROOT-1) | REQ-035 | ADR-PROJ031-003 D7 CV-006; attestation-design §3.2 | G-monitor |
| Bundle restore: git checkout refs/remotes/bundle/HEAD + SHA assertion before push (ROOT-4 / FM-037-QG3 / CI-G-001) | REQ-003 | CI-G-001; PM-001-Q3 | Phase 6 |
| Freshness co-equal condition (≤2h SLA) | REQ-049 | ADR-PROJ031-003 D7b IN-002 | G-monitor |
| Freshness suppression for tag with open generation-failure-escalation issue (ROOT-6c) | REQ-049/053 | PM-004-Q3 FM-022-QG3 | G-monitor |
| Fail-closed on any error (never silent exit 0) | REQ-035 | ADR-PROJ031-003 D7c FM-033 | G-monitor |
| last-good-validated tag advancement (full pass only) | REQ-053 | ADR-PROJ031-003 D7 R-008 | G-monitor |
| Auto-revert circuit breaker: ≤3 attempts per source tag (label-tracked); cap exceeded → halt + CRITICAL human-escalation issue (ROOT-6 / PM-004-Q3) | REQ-053 | ADR-PROJ031-003 D7d RT-005; FM-022-QG3 | G-monitor |
| Freshness date source: `gh release view --json publishedAt` (primary) + `git log -1 --format=%cI <tag>^{commit}` (fallback) + null guard exit 1; `.committer.date` on annotated tag object FORBIDDEN (returns null → false freshness-CRITICAL) (FM-001-i2 fix) | REQ-049 | ADR-PROJ031-003 D7b IN-002; FM-001-i2 RPN 343 | G-monitor |
| Runner image pinning MANDATED: same pinned OS image (`ubuntu-24.04`) for G9 (`cowork-skeleton.yml`) and m1-5 (`cowork-monitor.yml`); `ubuntu-latest` FORBIDDEN for these steps; tree-hash binding documented as Phase-6 hardening option requiring eng-infra if adopted (FM-002-i2 fix) | REQ-003, NFR-001 | CI-G-007; FM-002-i2 RPN 336 | Phase 6 |
| last-good-validated LGV_SKIP invariant guard: LGV_SKIP=true set in freshness suppression path; advance-last-good-validated blocked when LGV_SKIP is set; uses `${deployed_release_version}` (not `${latest_src_tag}`) on clean pass; tag with open generation-failure-escalation NEVER becomes last-good-validated (FM-003-i2 fix) | REQ-053 | ADR-PROJ031-003 D7 R-008; FM-003-i2 RPN 280 | G-monitor |
| G-actions-write-safe gate (SHA-pin + G-provenance) | REQ-053/017 | ADR-PROJ031-003 RT-002/R-003 | G-actions-write-safe |
| actions: write OMITTED until G-actions-write-safe | REQ-053 | ADR-PROJ031-003 D7 / RT-002 | G-actions-write-safe |
| Clone-weight telemetry separate from integrity | REQ-034d | ADR-PROJ031-003 D7 CV-006 | — |
| Meta-monitor as separate workflow (not co-located job) | REQ-044 | ADR-PROJ031-003 D7 SC-05 | G-monitor |
| Tiered alerts [CRITICAL] vs informational | REQ-055 | ADR-PROJ031-003 D7 | — |
| Loop-safety: dedicated repo has no push-back workflows | REQ-014/023 | ADR-PROJ031-003 CR-02 | — |
| Idempotency: workflow_dispatch same tag → same SHA | REQ-018 | ADR-PROJ031-001 idempotency | — |

---

## Pending Validation (P-022)

All items below are **Designed — operational validation pending** the named gate. None is an achieved fact.

| Item | Status | Resolved by |
|------|--------|-------------|
| Three-job permission isolation actually enforces separation | designed | Phase 6 inspection of YAML + G-prevention |
| Git bundle round-trip: git checkout refs/remotes/bundle/HEAD correctly repositions HEAD to G6_SHA; SHA assertion passes; git push --force sends exactly G6_SHA to dedicated repo (ROOT-4 / CI-G-001) | design gap (CI-G-001) | Phase 6 two-run idempotency test |
| ~~derive_expected_tip via Source-Commit release trailer~~ REMOVED (ROOT-1 / DA-001): release-body parsing is condemned by ADR-PROJ031-003 SC-04. Replaced by digest-based binding in 8-step monitor. | N/A — defect removed | N/A |
| Shallow-fetch + git archive byte-idempotency: runner image pinning MANDATED (FM-002-i2) — both G9 (`cowork-skeleton.yml`) and m1-5 (`cowork-monitor.yml`) MUST specify `ubuntu-24.04` (same image); `ubuntu-latest` FORBIDDEN for these steps. Empirical two-run idempotency test MUST use the pinned image in both workflows. If tree-hash binding adopted (Phase-6 hardening option), eng-infra engagement required before implementing (changes attestation/verification binding). | design constraint mandated (FM-002-i2) | Phase 6 two-run idempotency test on `ubuntu-24.04`; eng-infra if tree-hash binding adopted (REQ-003 AC; NFR-001 AC) |
| D8 scanner tool integration: eng-architect delivers (i) named pinned tool; (ii) runbooks/content-safety-patterns.md with C1–C6 patterns non-empty; (iii) interface contract; (iv) synthetic positive test (ROOT-5 / CI-G-003) | pending eng-architect — Phase-5 G-content BLOCKER | G-content |
| git archive flags + compression + attestation invocation | pending eng-infra | Phase 6 |
| `contents: write` for last-good-validated advancement on monitor | nuance (CI-G-005) | Phase 6 YAML review |
| Meta-monitor as separate workflow (CI-G-006) | design gap | Phase 6 implementation |
| Auto-revert circuit breaker: revert cap ≤3 per source tag verified via label count; cap-exceeded path opens CRITICAL human-escalation issue; generation-failure-escalation label suppresses freshness CRITICAL correctly (ROOT-6) | designed | G-monitor synthetic test |
| Freshness suppression: (a) FM-001-i2 fix — `gh release view --json publishedAt` correctly resolves annotated tag time (no null; synthetic test with annotated tag must produce non-null elapsed time within ≤2h of release publish); (b) FM-003-i2 fix — LGV_SKIP guard correctly blocks `last-good-validated` from advancing to a generation-failing/undeployed tag during suppression; `${deployed_release_version}` (not `${latest_src_tag}`) used in advance step on clean pass; (c) verify genuine tamper still fires CRITICAL when escalation label is absent | designed (FM-001-i2, FM-003-i2 fixes applied) | G-monitor synthetic test (acceptance criteria per FMEA iter-2 FM-001/FM-003) |
| G-actions-write-safe clearance (SHA-pin + G-provenance) | designed | G-actions-write-safe |
| actions: write added to monitor only after G-actions-write-safe | designed | Phase 6 gated YAML update |
| c-007 gate Phase-6 synthetic positive test: inject a dummy `skills/test-dup/SKILL.md` with a name colliding with an existing skill; confirm STEP c007-retention-and-skill-name-validation exits non-zero before push (no artifact, no attestation produced) | Phase-6 prerequisite | Phase 6 |
| plugin-smoke check Phase-6 synthetic test: (i) confirm jq + uv run import succeed on valid generated tree (exit 0); (ii) confirm exit non-zero on malformed plugin.json (synthetic invalid JSON); (iii) confirm exit non-zero if src/ is transiently absent | Phase-6 prerequisite | Phase 6 |

---

## References

| # | Source | Relevance |
|---|--------|-----------|
| 1 | `design/phase3-skeleton-generation-design.md` | G1–G9 algorithm, determinism contract, gate ownership, hand-off scope |
| 2 | `decisions/ADR-PROJ031-003-credential-protection-supply-chain.md` | D1–D8 decisions, gate sequence + ordering, per-job permissions A-1, G-actions-write-safe, D7 monitor topology, auto-revert, loop-safety |
| 3 | `requirements/phase1-requirements.md` | REQ-011..055, NFR-001..006, acceptance criteria, Phase-5 Authorization Checklist |

---

*Phase-3 live-install mirror (2026-07-02): STEP c007-retention-and-skill-name-validation added to generate-and-gate between D6 and D8 — asserts skills/.graveyard/ + .github/ stripped (validated strip-set), pyproject.toml + uv.lock present (c-008 KEEP), SKILL.md names unique in generated tip (c-007 marketplace invariant), all fail-closed; STEP plugin-smoke-check added adjacent — validates plugin.json + marketplace.json as valid JSON, declared skill SKILL.md paths resolve, uv run jerry entrypoint reachable. L1 topology, traceability matrix, and pending validation updated. Gate REQ IDs REQ-056. Settled gate-train structure and three-job graph unchanged (P-020). S-010 Self-review applied (H-15). No sub-agents spawned (P-003). Designed-but-unvalidated controls tagged per Claim-Status Convention (P-022).*

*Generated by jerry:eng-devsecops. Round-2 QG-3 consolidating fix (2026-06-30): ROOT-1 DA-001 8-step digest monitor mirrored from eng-infra §3.3 MONITOR HAND-OFF; ROOT-2 FM-007 $GITHUB_ENV determinism; ROOT-3 FM-020 D6 known-injected allow-list; ROOT-4 FM-037 bundle HEAD checkout + SHA assertion; ROOT-5 PM-003 D8 scanner pattern-catalog spec; ROOT-6 PM-004 auto-revert circuit breaker + freshness suppression. iter-2 QG-3 Critical fixes (2026-06-30): FM-001-i2 freshness date source — `gh release view --json publishedAt` primary, `git log -1 --format=%cI <tag>^{commit}` fallback, null guard exit 1; `.committer.date` FORBIDDEN on annotated tag objects. FM-002-i2 runner image pinning mandated — `ubuntu-24.04` required for G9 and m1-5; `ubuntu-latest` FORBIDDEN; tree-hash binding documented as Phase-6 hardening option (eng-infra engagement required if adopted; changes attestation/verification binding). FM-003-i2 last-good-validated invariant guard — LGV_SKIP=true blocks advance in suppression path; uses `${deployed_release_version}`; tag with open generation-failure-escalation NEVER becomes last-good-validated. iter-2 QG-3 Major fixes (2026-06-30): FM-004-i2 circuit-breaker counter — `count_open_issues` replaced by `gh issue list --state all | wc -l` (monotonic; human issue closure cannot reset cap below MAX_AUTO_REVERTS). FM-005-i2 TOCTOU race — `concurrency: group: cowork-monitor / cancel-in-progress: false` added to cowork-monitor.yml workflow triggers block; Traceability Matrix row added (REQ-015 / FM-005-i2). S-010 Self-review applied (H-15). Settled ADR-PROJ031-001/ADR-PROJ031-003 decisions consumed without reopening (P-020). No sub-agents spawned (P-003). Designed-but-unvalidated controls tagged per Claim-Status Convention (P-022).*
