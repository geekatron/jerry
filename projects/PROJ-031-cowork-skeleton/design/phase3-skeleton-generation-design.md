---
DISCLAIMER: This design is AI-generated guidance based on NASA Systems Engineering
standards (NPR 7123.1D Processes 3, 4, 17). It is advisory only and does not constitute
official NASA guidance. All architecture decisions require human review and professional
engineering judgment. Not for use in mission-critical decisions without SME validation.
---

# Phase 3 Design: Skeleton Generation Mechanism (3a)

> **Document ID:** FAD-PROJ031-3A-001
> **Project:** PROJ-031-cowork-skeleton
> **Phase:** Phase 3 — Skeleton + CI DESIGN (sub-phase 3a, skeleton generation)
> **Agent:** jerry:nse-architecture (NPR 7123.1D Process 3 logical decomposition + Process 4 design solution)
> **Criticality:** C4 (AE-002 `.github/` changes; AE-005 security-relevant; quality target >= 0.95)
> **Created:** 2026-06-30
> **Revised:** 2026-06-30 (QG-3 C4 remediation — ROOT-3/FM-020-QG3 version-sentinel placement + D6 known-injected allow-list; ROOT-2/FM-007-QG3 GIT_*_DATE cross-step propagation); **2026-07-02 (Phase-3 — mirror ADR-PROJ031-001 live-install amendment: validated strip-set `projects/ tests/ skills/.graveyard .github`; NEW no-duplicate-skill-names gate G8 / ADR-PROJ031-001 c-007; `src/`+`pyproject.toml`+`uv.lock` RETAIN call / ADR-PROJ031-001 c-008; positive-retention reframe; file counts 6,344 → 1,399 validated → ~1,114 with recommended additional strips)**
> **Status:** Draft — DESIGN (Phase-5 implements; nothing here is an achieved fact). **Phase-3 delta:** the retention strip-set below is now **install-validated** — the **1,399-file** tree pushed to `geekatron/jerry-claude-plugin` (default branch = skeleton) validated and **installed cleanly on Claude Web 2026-07-02** (marketplace synced, plugin validated + installed). **P-022:** install-validated ≠ update-propagation-validated (G-update still BLOCKED) ≠ hook-execution-validated (hooks fail-open); those remain pending.
> **Inputs (FINAL):** ADR-PROJ031-001 (Option A generation + determinism; **Phase-3 amendment — validated strip-set, c-007 no-dup-skill gate, c-008 runtime-dep KEEP, positive-retention surface**), ADR-PROJ031-003 (D1–D8 credential/supply-chain), requirements REQ-001..055, research R-001
> **Claim-Status Convention (P-022):** every control below is **Designed — operational validation pending [G-x]**, **except** the retention strip-set, which is **install-validated (2026-07-02)** per the Status note above. This is a design artifact; achieved present tense is otherwise reserved for Phase-5 post-validation.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language design and why it matters |
| [Scope and Non-Goals](#scope-and-non-goals) | What 3a owns vs. what is handed off |
| [L1: Generation Design](#l1-generation-design) | The engineered mechanism |
| [1. Functional Decomposition](#1-functional-decomposition-process-3) | Pipeline functional flow + ownership lanes |
| [2. Generation Algorithm](#2-generation-algorithm-g1g10) | Precise pseudocode (G1–G10) |
| [3. Determinism & Idempotency Contract](#3-determinism--idempotency-contract) | Commit SHA + artifact digest bit-stability |
| [4. Multi-Dimensional Pre-Push Gate](#4-multi-dimensional-pre-push-gate) | File-count / pack-size / clone-time, fail-closed, A→B flip |
| [5. Retention Completeness + No-Duplicate-Skill-Names Gate](#5-retention-completeness--no-duplicate-skill-names-gate-g7-g8) | Denylist strip + plugin.json-derived verification + c-007 marketplace invariant |
| [6. Fallback A: Version-Check Skill](#6-fallback-a-session-start-version-check-skill) | G-update mitigation, buildable now |
| [L2: Architectural Implications](#l2-architectural-implications) | Systemic consequences |
| [Decomposition & Hand-Off](#decomposition--hand-off) | eng-devsecops + eng-infra scope |
| [Traceability Matrix](#traceability-matrix) | Design element → REQ/ADR |
| [Pending Validation (P-022)](#pending-validation-p-022) | Honest open items |
| [References](#references) | Cited inputs |

---

## L0: Executive Summary

The skeleton generation mechanism turns a Jerry release tag into the plugin tree that Claude CoWork installs. Per **ADR-PROJ031-001 Option A** the mechanism is a short chain of plain git operations — check out the `v*` tag, **strip the non-distribution trees** (`git rm -r projects/ tests/ skills/.graveyard .github` — the ADR-PROJ031-001 Phase-3 **validated** strip-set), write a static `projects/` stub, make **one deterministic commit** whose parent is the tagged release commit — then a **no-duplicate-skill-names acceptance gate** (NEW, ADR-PROJ031-001 c-007), a **deterministic artifact** (`git archive` of the tip tree) for attestation, and a **cross-repo force-push** to the dedicated repo `geekatron/jerry-claude-plugin`. This design specifies that mechanism as an engineered algorithm (G1–G10), not final code; Phase 5 implements it.

**Retention, stated positively (ADR-PROJ031-001 Phase-3 reframe).** The distribution is **the plugin surface declared by `.claude-plugin/plugin.json` + `marketplace.json`, PLUS that surface's runtime dependencies** — `src/` + `pyproject.toml` + `uv.lock`, which the *fail-open* hooks shell out to via `uv run jerry` (**RETAIN**; ADR-PROJ031-001 c-008). The strip is only the *mechanism* that removes what is **not** on that surface — not a "`main` minus N directories" subtraction. **Empirically validated (2026-07-02):** with this strip-set the **1,399-file** tree installed cleanly on Claude Web. Reaching that took two fix-cycles the old subtractive framing had dragged in: an archived `skills/.graveyard/worktracker/SKILL.md` **name-collided** with the live `skills/worktracker` (the marketplace **rejects duplicate skill names** → motivates the G8/c-007 gate), and a retained `.github/docs.yml` spawned a gh-pages deploy inside the dedicated repo (loop-safety). **File counts:** 6,344 → **1,399 validated**; the ADR-PROJ031-001 recommended *additional* strips (`docs/ scripts/ mkdocs.yml CNAME .nojekyll` + dev/governance cruft) shrink it to **~1,114** (SHOULD, not required). Per P-022 the strip-set is **install**-validated; update-propagation (G-update) and hook-execution remain unproven.

Why it matters: two acceptance claims rest entirely on **bit-stability**. The file-count gate (**1,399 validated** < 5,000; ~1,114 with the recommended additional strips) is only meaningful if the same release always produces the same tree, and the **Iteration-8 attestation correction** (ADR-PROJ031-003 D4, 2026-06-30) anchors integrity to the **digest of the `git archive` artifact** — so that digest must also be invariant per release. This design therefore extends ADR-PROJ031-001's commit-SHA determinism contract to cover the **artifact digest** (including the gzip-mtime trap that would silently break it), defines the **multi-dimensional pre-push gate** (file count **and** pack size **and** clone time — because the CoWork ceiling may be size- or time-based, FM-062/IN-001), specifies the **R-008 retention-surface completeness check** (denylist strip verified against `plugin.json`), and designs the shape of **Fallback A** (a buildable-now session-start stale-version notice that mitigates the unverifiable G-update assumption). The CI workflow wiring, security gates, and attestation/provenance mechanics are decomposed to eng-devsecops and eng-infra.

---

## Scope and Non-Goals

**3a owns (this design):** the generation algorithm (resolve→validate→checkout→strip→stub→deterministic-commit→artifact→push), the determinism/idempotency contract (commit + artifact), the multi-dimensional pre-push gate, the retention-surface completeness check, and the Fallback A skill shape.

**Explicitly NOT in 3a (handed off — see [Decomposition & Hand-Off](#decomposition--hand-off)):**
- The **workflow structure** (triggers, jobs, per-job permissions, gate sequencing, loop-safety, concurrency, SHA-pin, the D7 monitor) → **eng-devsecops**.
- The **attestation/provenance mechanics** (Sigstore build-provenance over the artifact, immutable-release publishing, `gh attestation verify` invocation, repo/tag rulesets, credential provisioning, SBOM) → **eng-infra**.

**Settled and not re-opened (P-020):** Option A vs B/C (ADR-PROJ031-001), dedicated-repo distribution + credential + attestation anchor (ADR-PROJ031-003 D1–D8). This design *realizes* those decisions; it does not revisit them. The **Phase-3 amendment mirrored here** (validated strip-set, c-007 no-dup-skill gate, c-008 runtime-dep KEEP, positive-retention surface) **refines the retention surface and adds one acceptance gate only** — it does **not** reopen the Option A generation technique, the determinism/idempotency contract, or the AG-02 strategy (P-020).

---

## L1: Generation Design

### 1. Functional Decomposition (Process 3)

The generation pipeline is one fail-closed gate train. Each stage is a function with a single concern; the **load-bearing invariant** is that every gate passes **before** the artifact is produced, attested, and pushed — so the attested artifact is exactly the gated artifact (ADR-PROJ031-003 D4/D8 ordering). Ownership lanes show the decomposition boundary.

```
 SOURCE repo (geekatron/jerry), workflow on: push tags v* + workflow_dispatch
 ┌──────────────────────────────────────────────────────────────────────────┐
 │ [DEVSECOPS] trigger + event-discriminated context                         │
 │      │                                                                     │
 │ G1 resolve TAG ─▶ G2 validate TAG (allow-list)            ── 3a ──────────│
 │      │                                                                     │
 │ [DEVSECOPS+INFRA] PROVENANCE GATE  (D5: merge-base ancestor of main)      │
 │      │  fail ⇒ exit≠0, NO artifact, NO push                                │
 │ G3 checkout v* ─▶ G4 strip projects/ tests/ .graveyard .github ── 3a ─────│
 │      │                          ─▶ G5 write static stub + version sentinel │ 3a
 │ G6 deterministic commit (parent=SRC_SHA, pinned dates, 40-char SHA) ──────│
 │      │                                                                     │
 │ G7 retention-surface completeness (plugin.json-derived)   ── 3a ──────────│
 │ G8 no-duplicate-skill-names gate (marketplace invariant, c-007) ── 3a ────│
 │      │  dup skill name ⇒ exit≠0, NO artifact, NO push (fail-closed)         │
 │ G9 multi-dimensional gate (file-count ∧ pack-size ∧ clone-time) ── 3a ────│
 │      │  hard-fail ⇒ exit≠0, NO push   (warn-band ⇒ non-blocking issue)     │
 │ [DEVSECOPS] D6 faithful-derivative (diff TAG..HEAD) + secret scan         │
 │ [DEVSECOPS] D8 content-safety / prompt-injection scan                     │
 │      │  any gate fail / scanner error ⇒ fail-closed, NO push               │
 │ G10 produce deterministic artifact (git archive of tip) ── 3a ─▶ feeds ───│
 │ [INFRA] attestation job (Sigstore build-provenance over artifact, D4)     │
 │      │  attest fail ⇒ NO push                                              │
 │ [DEVSECOPS push job + INFRA credential] cross-repo force-push (App token) │
 │ [INFRA] publish immutable release (artifact as asset)                     │
 └──────────────────────────────────────────────────────────────────────────┘
            ▼ (default branch = skeleton — 1,399 files validated; ~1,114 with recommended strips)
       DEDICATED repo geekatron/jerry-claude-plugin  ── org-registered ─▶ CoWork users
       [INFRA] org-level ruleset (D2)   [DEVSECOPS] cowork-monitor.yml (D7, source-repo, read-only)
```

**Function-to-owner allocation (N²-style summary):**

| Function | Owner | Primary trace |
|----------|-------|---------------|
| G1 resolve / G2 validate tag | 3a | REQ-036; ADR-PROJ031-001 RT-04, IT3-005 |
| Provenance gate (D5) | eng-devsecops (build-time) + eng-infra (tag ruleset) | REQ-038/039; ADR-PROJ031-003 D5 |
| G3 checkout / G4 strip (validated set) / G5 stub+sentinel | 3a | REQ-002/004/004a/007; ADR-PROJ031-001 c-003 (validated strip-set)/c-006/**c-008** (retain `src/`+`pyproject.toml`+`uv.lock`); R-001; live install 2026-07-02 |
| G6 deterministic commit | 3a | REQ-003/008; ADR-PROJ031-001 §Regeneration Commit Determinism |
| G7 retention completeness | 3a | REQ-005/010; ADR-PROJ031-001 R-008/FM-030 |
| **G8 no-duplicate-skill-names gate** | 3a | **ADR-PROJ031-001 c-007** (marketplace invariant); live install 2026-07-02 |
| G9 multi-dim gate | 3a | REQ-006/034d/050; ADR-PROJ031-001 §Clone-Weight |
| D6 faithful-derivative + secret scan | eng-devsecops | REQ-022; ADR-PROJ031-003 D6 |
| D8 content-safety | eng-devsecops (gate) + eng-infra-adjacent catalog (eng-architect owns) | REQ-052; ADR-PROJ031-003 D8 |
| G10 deterministic artifact | 3a → eng-infra | REQ-042; ADR-PROJ031-003 D4 (R-006) |
| Attestation + immutable release | eng-infra | REQ-042; ADR-PROJ031-003 D4 |
| Cross-repo force-push | eng-devsecops (job) + eng-infra (credential) | REQ-041; ADR-PROJ031-003 D3; ADR-PROJ031-001 CC-005 |
| D7 monitor + auto-revert | eng-devsecops | REQ-035/049/053; ADR-PROJ031-003 D7 |

---

### 2. Generation Algorithm (G1–G10)

Language-agnostic pseudocode. The ADR-PROJ031-001 §Regeneration and ADR-PROJ031-003 §L1 bash sketches are the Phase-5 implementation seed; this is the engineered decomposition with semantics and fail-closed behavior. All failures are **fail-closed**: non-zero exit, **no artifact, no push** (no live-but-ungated state).

```
FUNCTION generate_skeleton(event_ctx, provenance_mode = OPTION_A) -> (commit_sha, artifact_digest):

  # ---- G1  Resolve source tag — EVENT-DISCRIMINATED (REQ-036; ADR-PROJ031-001 IT3-005) ----
  IF event_ctx.name == "workflow_dispatch":
      TAG <- event_ctx.inputs.target_tag
      IF TAG is blank:                                  # newest semver tag
          TAG <- newest( git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-version:refname )
  ELSE:                                                 # push: tags/v* -> ref name IS the tag
      TAG <- event_ctx.ref_name
  # NOTE: GITHUB_REF_NAME is the *branch* on workflow_dispatch, NOT a tag — never assign it blind.

  # ---- G2  Validate the RESOLVED tag (allow-list, BEFORE any use) (REQ-036; ADR-PROJ031-001 RT-04) ----
  ASSERT TAG matches ^v[0-9]+\.[0-9]+(\.[0-9]+)?$  ELSE fail_closed("rogue tag syntax")
  #  One gate covers all input paths (ref_name, target_tag, blank-resolved). Bind via env:,
  #  never interpolate ${{...}} into a shell line (script-injection). Syntax only — provenance
  #  (tag-on-main) is the D5 gate, owned downstream.

  SRC_SHA  <- git rev-parse "${TAG}^{commit}"          # full 40 hex chars, fixed length
  SRC_DATE <- git show -s --format=%cI "${SRC_SHA}"    # source committer date, ISO-8601

  # ---- [D5 provenance gate runs here — eng-devsecops; precondition for G3+] ----

  # ---- G3  Checkout the frozen released tree (REQ-007) ----
  #  fetch-depth: 0 (full history) — REQUIRED for Option A parent chain AND the D5 ancestor check.
  git checkout "${TAG}"

  # ---- G4  Denylist strip — VALIDATED SET (REQ-002; ADR-PROJ031-001 c-003 Phase-3 amendment; R-001; live install 2026-07-02) ----
  #  Distribution = plugin surface (plugin.json + marketplace.json) + its runtime deps
  #  (src/ + pyproject.toml + uv.lock — c-008 KEEP). The strip only removes what is NOT on that
  #  surface (positive-retention framing). VALIDATED set below installed cleanly on Claude Web:
  git rm -r projects/ tests/ skills/.graveyard .github  # retains everything else BY CONSTRUCTION
  #    projects/       ~4,600  work artifacts (a static projects/ stub is re-injected at G5, c-006)
  #    tests/          (bulk)  test suite; not load-bearing for plugin function
  #    skills/.graveyard/   2  archived skills; .graveyard/worktracker name-COLLIDED with live
  #                            skills/worktracker → marketplace REJECTED the plugin (→ G8/c-007)
  #    .github/            14  framework CI; docs.yml spawned a gh-pages deploy in the dedicated
  #                            repo → loop-safety violation
  #  → 6,344 → 1,399 tracked files (VALIDATED — installed cleanly on Claude Web 2026-07-02).
  #
  #  RECOMMENDED additional strips (SHOULD, not required — non-distribution, no runtime need;
  #  each git-verified unreferenced by src/interface/, plugin.json, marketplace.json, or the hooks):
  #    docs/ (247)   scripts/ (28)   mkdocs.yml + CNAME + .nojekyll (3)
  #    Makefile + .pre-commit-config.yaml + pytest.ini (3)
  #    CHANGELOG.md + CONTRIBUTING.md + CODE_OF_CONDUCT.md + GOVERNANCE.md (4)
  #  → −285 files → ~1,114. (LICENSE/NOTICE, README.md, AGENTS.md, CLAUDE.md, TOOL_REGISTRY.yaml
  #  are RETAINED — runtime/agent surface.) IF applied: G7 (§5) MUST also assert no retained file
  #  references a stripped path (additive-allow-set guard), and D6's pathspec MUST exclude them too.
  #  RETAINED (c-008): src/ + pyproject.toml + uv.lock — hooks fail-OPEN, so stripping them would
  #  silently no-op EVERY Jerry guardrail (`uv run jerry` fails) with NO error surfaced.

  # ---- G5  Write static stub + static version sentinel (REQ-004/004a; ADR-PROJ031-001 c-006) ----
  #  BOTH files are KNOWN-INJECTED artifacts placed UNDER projects/ — i.e. inside REQ-022's
  #  existing ':!projects/' faithful-derivative allow-list (§3(c); resolves FM-020-QG3). They are the
  #  ONLY two paths the generator adds on top of (TAG − projects/ − tests/).
  write_static( projects/README.md )                   # stub: empty-dir guard, static PROSE ONLY (REQ-004a — NO version string)
  write_static( projects/.jerry-skeleton-version )     # sentinel: embeds ONLY Source-Tag + 40-char SRC_SHA
                                                        # (invariant per tag; NO timestamp/run-id) — for Fallback A.
                                                        # MUST stay under projects/; a sentinel in .claude/ breaks D6 every release (FM-020-QG3).

  # ---- G6  Deterministic commit (REQ-003/008; ADR-PROJ031-001 §Regeneration Commit Determinism) ----
  #  DETERMINISM-CRITICAL (FM-007-QG3): the committer/author dates MUST reach the `git commit` PROCESS.
  #  A bare shell `export` does NOT survive across GitHub Actions `run:` step boundaries — if the
  #  date-pin and the commit land in SEPARATE steps, the export is LOST and git stamps the runner
  #  wall-clock ("now"), silently producing a NEW commit SHA — and thus a new artifact digest — on
  #  EVERY run (breaks the file-count AC, the D4 attestation subject, and the D7 tree-digest match).
  #  Pin by ONE of (eng-devsecops owns the YAML mechanic — see Decomposition & Hand-Off):
  #    (i)  SAME-STEP / inline — set both vars in the same process that runs the commit, e.g.
  #         `GIT_AUTHOR_DATE="$SRC_DATE" GIT_COMMITTER_DATE="$SRC_DATE" git commit ...`,
  #         or keep G4–G6 inside one `run:` block; OR
  #    (ii) CROSS-STEP — propagate via $GITHUB_ENV so later steps inherit it:
  #         `echo "GIT_AUTHOR_DATE=$SRC_DATE"  >> "$GITHUB_ENV"` and
  #         `echo "GIT_COMMITTER_DATE=$SRC_DATE" >> "$GITHUB_ENV"`.
  #  A bare cross-step `export` is FORBIDDEN.
  PIN_INTO_COMMIT_PROCESS( GIT_AUTHOR_DATE = SRC_DATE, GIT_COMMITTER_DATE = SRC_DATE )   # copy source date, NEVER "now"
  IF provenance_mode == OPTION_A:  base <- parent=SRC_SHA          # branch-from-tag (provenance)
  ELSE:                            base <- orphan                  # git checkout --orphan (constant weight)
  commit_sha <- git commit  --no-verify                            # --no-verify: clean op, bypass dev pre-commit (R-001)
                  --author "github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>"
                  --message FIXED_TEMPLATE(TAG, SRC_SHA)           # full 40-char SHA in subject + Source-Commit trailer
                  # UNSIGNED (a timestamped signature would break bit-identity)

  # ---- G7  Retention-surface completeness — plugin.json-derived (REQ-005/010; ADR-PROJ031-001 R-008) ----
  ASSERT verify_retention_surface(commit_sha)  ELSE fail_closed("retention surface incomplete")

  # ---- G8  No-duplicate-skill-names gate — FAIL-CLOSED, before artifact/push (ADR-PROJ031-001 c-007) ----
  #  The EXACT Claude-marketplace invariant the 2026-07-02 live test caught: a subtractive strip
  #  can retain an ARCHIVED skill whose name collides with a live one (skills/.graveyard/worktracker
  #  vs skills/worktracker), and the marketplace REJECTS duplicate skill names. Stripping
  #  skills/.graveyard/ (G4) removes today's KNOWN collision; THIS gate is the durable guard against
  #  any FUTURE archived/vendored skill silently re-introducing one. Operates on the generated tip.
  names <- []
  FOR skill_md IN git ls-files(commit_sha, 'skills/**/SKILL.md'):   # every retained SKILL.md
      names.append( skill_name(skill_md) )     # frontmatter `name`, else containing-dir basename
  ASSERT no_duplicates(names)  ELSE fail_closed("duplicate skill name(s): " + duplicates(names))
  #  fail_closed ⇒ non-zero exit, NO artifact, NO push. A duplicate is a HARD build failure, not advisory.

  # ---- G9  Multi-dimensional pre-push gate (REQ-006/034d/050; ADR-PROJ031-001 §Clone-Weight) ----
  m <- measure(commit_sha)   # {file_count, pack_size_mb, clone_seconds}
  emit_telemetry(m)          # to step-summary EVERY run (REQ-034d), pass or fail
  ASSERT multidim_gate(m)    ELSE fail_closed("multi-dim ceiling breach")   # see §4

  # ---- [D6 faithful-derivative + secret scan, then D8 content-safety — eng-devsecops] ----

  # ---- G10 Produce the DETERMINISTIC artifact for attestation (REQ-042; ADR-PROJ031-003 D4, R-006) ----
  artifact <- git archive --format=tar "${commit_sha}"            # archive the COMMIT (mtime=committer date)
  #  If compressed, MUST strip gzip mtime/OS byte (gzip -n) or the digest is non-deterministic (see §3).
  artifact_digest <- sha256(artifact)

  # ---- [attest artifact (D4, eng-infra) -> cross-repo push (D3) -> publish release (D4)] ----
  RETURN (commit_sha, artifact_digest)
```

> **Cross-repo push form (ADR-PROJ031-001 CC-005; ADR-PROJ031-003 D3).** `git push --force <dedicated-remote> HEAD:<default-branch>` authenticated with the **GitHub App installation token / single-repo deploy key** — never the source `GITHUB_TOKEN` (cannot push cross-repo). Wholesale tip replacement; no per-release accumulation.

> **Option A→B flip is a one-line, integrity-neutral change.** `provenance_mode` is a single parameter (G6). Flipping to `OPTION_B` (orphan) yields constant-weight history; tamper-evidence is unaffected because it rests on the deterministic artifact digest, not the parent chain (ADR-PROJ031-001 IT3-004). This operationalizes the ADR's "pre-designed one-line flip."

---

### 3. Determinism & Idempotency Contract

Two outputs must be **bit-identical for a given release tag**: the **commit SHA** (so the file-count AC is stable and re-runs do not drift) and the **artifact digest** (so the D4 attestation subject is stable). ADR-PROJ031-001 fixes the first; the Iteration-8 artifact-subject correction makes the second newly load-bearing, and this design fixes it.

**(a) Commit-SHA inputs — all pinned (ADR-PROJ031-001 §Regeneration Commit Determinism):**

| Commit input | Pin | Invariant because |
|--------------|-----|-------------------|
| Tree | `f(tree(TAG) − {validated strip-set} + known-injected allow-list)` where strip-set = `projects/ tests/ skills/.graveyard/ .github/` (+ recommended `docs/ scripts/ …` if applied) and allow-list = { `projects/README.md` stub, `projects/.jerry-skeleton-version` sentinel } (both under `projects/` — §3(c)) | tag tree frozen; `git rm` deterministic; the strip-set + both injected files are static/invariant per tag |
| Parent | `SRC_SHA` (Option A) or none (Option B orphan) | tag resolves to exactly one commit |
| Author/committer identity | `github-actions[bot]` / `41898282+...@users.noreply.github.com` | fixed bot identity |
| Author/committer **dates** | `SRC_DATE` via `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE`, pinned **into the commit process** (same-step inline **or** `$GITHUB_ENV` — never a bare cross-step `export`; FM-007-QG3) | copied from source commit, **never "now"** (the single most common break); on GitHub Actions a shell `export` does not cross `run:` step boundaries, so a separate-step commit would silently stamp wall-clock and drift the SHA every run |
| Message | fixed template + Source-Tag + **full 40-char** Source-Commit; no timestamp/run-id/`--short` SHA | tag + full SHA invariant & fixed-length (short-SHA length grows with repo size — FM-010) |
| Signature | **unsigned** | a timestamped signature varies per run |

**(b) Artifact-digest inputs — pinned by archiving the deterministic commit (NEW; design extension for D4/R-006):**

| Archive input | Pin | Invariant because |
|---------------|-----|-------------------|
| Content (tree) | archive the **commit** `${commit_sha}`, not a bare tree | tree already pinned in (a) |
| Embedded mtime | git-archive derives mtime from the **commit's committer date** | committer date pinned in (a) |
| Embedded commit-id | the deterministic `commit_sha` (git archive records it) | commit SHA pinned in (a) |
| uid/gid, file order, mode | `git archive` defaults (0/0, deterministic ordering) | git archive is reproducible by construction |
| **Compression wrapper** | prefer `--format=tar` (uncompressed); **if** `.gz`, use `gzip -n` | **gzip embeds a timestamp + OS byte by default → digest drifts every run** unless stripped |

→ `sha256(artifact)` is therefore bit-stable per release. **Idempotency proof (extends ADR-PROJ031-001):** `regenerate(T)` is a pure function of `T` over both outputs — `(commit_sha, artifact_digest) = h(T)` — so `workflow_dispatch` retries and replays reproduce both exactly; different tags differ (different parent/tree). **Precondition (CV-005/IN-007):** holds only while `T → SRC_SHA` is fixed; a force-moved tag intentionally yields a new artifact, which is why the **attestation on the artifact digest** (not the tag name) is the durable integrity reference.

> **Determinism sub-constraints owned here (P-022 honesty):** (i) the version sentinel (G5) is the dedicated static file `projects/.jerry-skeleton-version` and may embed only the Source-Tag + full Source-Commit (invariant per tag) — **never** a build timestamp/run-id, or it breaks (a)/(b); it MUST stay under `projects/` (inside the D6 allow-list — §3(c)), never `.claude/`; (ii) the **exact `git archive` flag set + compression choice is a Phase-5/eng-infra detail (pending)** — this design fixes the determinism *property* and the gzip-mtime hazard, not the final flag string; (iii) the GIT_*_DATE pin (G6) MUST reach the commit process via same-step inline binding **or** `$GITHUB_ENV`, never a bare cross-step `export` (FM-007-QG3 — see §2 G6).

**(c) Faithful-derivative known-injected allow-list — D6 consistency (resolves FM-020-QG3):**

The D6 faithful-derivative gate (REQ-022, eng-devsecops) asserts the generated tip equals **`TAG`-tree − {validated strip-set: `projects/`(original) `tests/` `skills/.graveyard/` `.github/`} + a fixed _known-injected allow-list_**, with **no other path added/modified/removed**. That allow-list has exactly **two static members, BOTH under `projects/`** — one placement rule keeps the gate green:

| Known-injected artifact | Path | Role | Why it does not break D6 |
|-------------------------|------|------|--------------------------|
| Empty-dir stub | `projects/README.md` | `projects/` empty-dir guard; **static prose only** (REQ-004/004a — no version string) | under `projects/` ⇒ inside REQ-022's `:!projects/` exclusion |
| Version sentinel | `projects/.jerry-skeleton-version` | Fallback A source: `Source-Tag` + 40-char `Source-Commit`, invariant per tag | under `projects/` ⇒ inside REQ-022's `:!projects/` exclusion |

Because **both** members live under `projects/`, REQ-022's mechanization `git diff --quiet "${TAG}..HEAD" -- ':!projects/' ':!tests/' ':!skills/.graveyard/' ':!.github/'` tolerates the stub+sentinel with **no pathspec change for them** (both under the already-excluded `projects/`) — the sentinel is therefore **not** an "other file added" outside the allow-list; the added `':!skills/.graveyard/'`/`':!.github/'` exclusions exist to cover the *validated strip-set* deletions (see Hand-Off item 6(b)), not the injected files. The **FM-020-QG3 failure mode** is a sentinel placed in `.claude/` (a *retained, faithful* surface that D6 **does** diff): it has no `TAG` pre-image, so `--quiet` exits non-zero and **D6 fails every release**. G7 (§5) independently pins `git ls-files projects/` to **exactly** these two members, so the wholesale `:!projects/` exclusion cannot mask an unexpected injected file. **Resolution = option (b)** (allow-list the sentinel like the stub), chosen over option (a) (delete the sentinel; read the version from the retained `pyproject.toml`) because (b) preserves ADR-PROJ031-001 Fallback A's settled "static version sentinel" file and its 40-char `Source-Commit`, and REQ-004a forbids folding the version into the prose `README.md` — only the unresolved placement defect is fixed, the settled architecture is unchanged (P-020).

---

### 4. Multi-Dimensional Pre-Push Gate

**Purpose (REQ-006/034d; FM-062/IN-001/IN-002):** a file-count-only gate cannot falsify a CoWork ceiling that is size- or time-based, and Option A's full-history `.git` grows monotonically (~2 MB/release) toward the 120 s git-timeout. The gate therefore measures **three orthogonal dimensions** and emits all three to `$GITHUB_STEP_SUMMARY` on **every** run (REQ-034d), pass or fail.

| Dim | Measures | Concern | Hard-fail (block + exit≠0) | Early-warn (non-blocking issue) | Target |
|-----|----------|---------|----------------------------|----------------------------------|--------|
| (a) file count | `git ls-files \| wc -l` (tip tree) | CoWork **install** ceiling | `>= 5,000` (REQ-006a) | `>= 3,500` ≈70% (REQ-050) | 1,399 validated; ~1,114 w/ recommended strips |
| (b) pack size | `git count-objects -vH` `size-pack` (full `.git`) | **clone weight** / 120 s timeout | `> 250 MB` (REQ-006b/034d) | `> 150 MB` ≈60% (REQ-034d) | grows ~2 MB/release |
| (c) clone time | timed reference clone, or pack×bandwidth @ 10 Mbps | 120 s git-op timeout | `> 60 s` (50% of 120 s) (REQ-006c) | `> 40 s` ≈60% (REQ-034d) | — |

**Semantics:**
- **Fail-closed, OR-combined:** **any** dimension breaching its hard threshold blocks the push (exit non-zero, dedicated repo unchanged). The three failures are independently testable (REQ-006 AC).
- **Two bands:** hard-fail blocks the release; the early-warning band opens a **non-blocking** GitHub issue and exits 0 (REQ-050/034d) — advance notice, not a stop.
- **Reference network:** document the bandwidth used (10 Mbps ≈ 30th-percentile global broadband) so (c) is reproducible.
- **Tiered alerts (REQ-055):** hard-fail = `[CRITICAL]`; early-warning = informational.

**Option A→Option B flip triggers (clone-weight, ADR-PROJ031-001 §Clone-Weight):**

| Signal | Source | Action |
|--------|--------|--------|
| Early-warning band: pack `> 150 MB` **or** clone `> 40 s` | scheduled telemetry (REQ-034d) | open issue → execute the **pre-designed orphan flip proactively** (`provenance_mode=OPTION_B`, §2) |
| Hard trigger: pack `> 250 MB` **or** clone `> 60 s` | per-release gate (REQ-006) | release blocked → **forced** flip decision |

The flip is integrity-neutral (tamper-evidence rests on the artifact digest, not the parent chain). Clone-weight telemetry is a **timed reference clone**, distinct from the D7 read-only integrity monitor (which never clones — CV-006).

---

### 5. Retention Completeness + No-Duplicate-Skill-Names Gate (G7, G8)

**Purpose (R-008/FM-030; ADR-PROJ031-001 c-007):** prove the generated tip contains **exactly** the expected plugin surface (G7, drift-proof as the codebase grows) **and no colliding skill names** (G8, the marketplace invariant the live test caught). Three deterministic-by-construction mechanisms — 1–2 are the G7 completeness check; 3 is the distinct fail-closed G8 gate:

1. **Generation is a denylist strip, not an allowlist copy.** `git rm -r projects/ tests/ skills/.graveyard .github` (validated strip-set; + recommended `docs/ scripts/ …`) **retains everything else automatically** — new `skills/*/agents/*.md`, `commands/*.md`, `.context/rules/*.md` are kept without a static keep-list to fall out of sync with. The retention surface is defined **positively** (plugin surface + its runtime deps `src/`+`pyproject.toml`+`uv.lock`, c-008); the denylist is the *mechanism* that reaches it, audited against that allow-set. The 8-directory table is a *verification* surface, not the generation mechanism.
2. **Completeness verified against `.claude-plugin/plugin.json`, dynamically (REQ-010).** The check derives its required-present set **at generation time from the manifest** — enumerating every declared `skills`, `agents[]`, and `commands[]` path and asserting each resolves in the tip via `git ls-files` — reading **declared paths exactly** (not a shallow `skills/*/agents/*.md` glob that assumes one-level nesting). "The manifest declares it ⇒ the skeleton contains it" is then a deterministic invariant.
3. **No-duplicate-skill-names — fail-closed, the EXACT marketplace invariant (G8; ADR-PROJ031-001 c-007).** Collect the resolved skill name of **every** `SKILL.md` under the retained `skills/**` (frontmatter `name`, else the containing-directory basename); if any name appears **more than once**, **abort with a non-zero exit and NO artifact / NO push**. This is a *hard build failure*, not advisory: it is the invariant that rejected fix-cycle #1 (`skills/.graveyard/worktracker` colliding with live `skills/worktracker`). G4's `skills/.graveyard/` strip removes today's known collision; **G8 is the durable guard** against any future archived/vendored skill silently re-introducing one. G8 runs on the committed tip **after G7 and before the multi-dim gate (G9), artifact (G10), and push** — the ADR-PROJ031-001 c-007 "generated tip tree, before the force-push" window. (The check needs only the stripped `skills/**`, not the commit object, so an implementer MAY additionally run it pre-commit on the working tree as a fail-*faster* optimization; the normative gate remains G8 on the committed tip, before any artifact or push.)

**`verify_retention_surface(commit)` — G7 (pseudocode):**

```
# Positive (presence) — REQ-005:
FOR dir IN [.claude-plugin/, skills/, commands/, .claude/, .context/, hooks/, src/, schemas/]:
    ASSERT git ls-tree --name-only HEAD dir/  is non-empty
ASSERT present(.claude-plugin/plugin.json) AND present(.claude-plugin/marketplace.json)
ASSERT present(pyproject.toml) AND present(uv.lock)     # runtime deps of the hook surface — c-008 KEEP
# Manifest-derived (no hard-coded list) — REQ-010:
FOR path IN declared_paths(plugin.json: skills ∪ agents[] ∪ commands[]):
    ASSERT path resolves in git ls-files(HEAD)
# Negative (VALIDATED strip confirmation) — REQ-002/005:
ASSERT git ls-files tests/ is empty
ASSERT git ls-files skills/.graveyard/ is empty         # removes fix-cycle-#1 dup collision (c-007)
ASSERT git ls-files .github/ is empty                   # removes fix-cycle-#2 framework-CI loop
ASSERT git ls-files projects/ == { projects/README.md, projects/.jerry-skeleton-version }   # known-injected allow-list ONLY: prose stub + version sentinel (§3(c); D6 consistency, FM-020-QG3)
# IF the recommended additional strips are applied (docs/ scripts/ mkdocs.yml CNAME .nojekyll +
# dev/governance cruft): ALSO assert each is empty AND that NO retained file references a stripped
# path at runtime (additive-allow-set guard — ADR-PROJ031-001 recommended-strip guard).
# Symlink integrity (CI-env) — REQ-009:
ASSERT readlink -f .claude/rules AND .claude/patterns resolve to existing targets
```

**`no_duplicate_skill_names(commit)` — G8, fail-closed (ADR-PROJ031-001 c-007):**

```
names <- [ skill_name(m) FOR m IN git ls-files(HEAD, 'skills/**/SKILL.md') ]  # frontmatter name | dir basename
dups  <- { n IN names : count(names, n) > 1 }
ASSERT dups is empty  ELSE fail_closed("duplicate skill name(s): " + dups)     # non-zero exit, NO artifact, NO push
```

Any failure in G7 or G8 is fail-closed (no artifact, no push). Note (REQ-009): CI verifies the Linux runner; CoWork-session symlink resolution (Windows `core.symlinks=false`) is a separate R-001/Phase-5 concern.

---

### 6. Fallback A: Session-Start Version-Check Skill

**Role (ADR-PROJ031-001 G-update Fallback Architecture; REQ-054/OQ-048).** The headline "automatically in sync" value depends on the **unverified, currently un-testable** assumption that CoWork propagates default-branch updates to already-installed users (G-update is BLOCKED by the removed marketplace "+"/add UI). Fallback A converts *silent* staleness into a *visible, user-actionable* notice. **It is buildable and unit-testable now** (it only reads a version and emits a signal); whether it is **needed** is G-update-pending — designed, not asserted (P-022).

**Design shape (two static components in the retained surface):**

| Component | Where | Behavior | Determinism / trace |
|-----------|-------|----------|---------------------|
| **A1 — version sentinel** | the dedicated static file **`projects/.jerry-skeleton-version`** (resolved — NOT `.claude/`; see §3(c)/FM-020-QG3), written by G5, distinct from the `projects/README.md` prose stub (REQ-004a forbids version strings in the README) | holds the installed skeleton's `Source-Tag` + full-40-char `Source-Commit` | static content; embeds only invariant-per-tag values → preserves §3 determinism (REQ-004a); under `projects/` ⇒ inside the D6 known-injected allow-list (REQ-022 `:!projects/`) |
| **A2 — version-check skill/hook** | `skills/` or `hooks/` (static markdown/script), in the retained surface | at session start: read A1's installed tag; GET latest `geekatron/jerry` release tag (public releases API); if different, emit a **non-blocking** statusline/banner: *"Jerry skeleton `<installed>` is stale; latest is `<current>` — reinstall to update."* | static skill content (deterministic, in D8 scan scope); if it shells to Jerry, it MUST use `uv run jerry` (H-05) |

**Properties:** passive, non-blocking, detection-only. **Requires:** outbound GitHub API egress from the CoWork sandbox; A1 (= `projects/.jerry-skeleton-version`) inside both the determinism contract and the D6 known-injected allow-list (§3(c)); A2 added to the retained surface (so D8 content-scans it). **Limits (honest):** informs, cannot update; useless to a user who never starts a fresh session; network-dependent. **Pairing:** ADR-PROJ031-001 recommends **A + C** (in-session detection + out-of-session changelog signal) with **B** (manual how-to) as the required backstop; none restores automatic propagation.

> **Sequencing (P-020):** the *decision to ship* Fallback A is a **G-update-pre Phase-5 ENTRY** outcome (PASS → not needed; FAIL/BLOCKED → ship A+C, re-scope STK-002). This design delivers the **buildable shape** so the team can build/unit-test it independently of the platform blocker; it does not pre-judge the entry-gate decision.

---

## L2: Architectural Implications

1. **Bit-stability is the spine of two independent claims.** The file-count AC and the D4 attestation digest both collapse to non-determinism if any commit or archive input drifts. Extending the determinism contract to the **artifact** (and naming the gzip-mtime trap) is the highest-leverage design act in 3a — it is the difference between a "verifiable, reproducible" supply chain and a flaky one.
2. **The gate train is one fail-closed sequence with two distinct authorities.** Generation-acceptance gates (G7 completeness / G8 no-duplicate-skill-names / G9 multi-dim) prove *correctness/size/marketplace-validity*; security gates (D5/D6/D8) prove *provenance/integrity/content*. They compose, but their order is load-bearing only at one point: **everything precedes artifact+attest+push**, so the attested artifact is the gated artifact (no live-but-ungated window). G8 is the design's direct response to the 2026-07-02 live-test finding — the marketplace duplicate-skill-name rejection — moved *upstream of the push* so the defect can never reach a user.
3. **Reversibility is engineered in.** `provenance_mode` makes the Option A→B flip a one-parameter, integrity-neutral change rather than a redesign — the clone-weight residual (IN-002/FM-007) is bounded by telemetry + a pre-wired escape.
4. **The deepest residual is external, not in the mechanism.** Whether the skeleton reaches *existing* users (G-update) and whether the real ceiling is file-count-based (G-headroom) are unverified/blocked; Fallback A and the multi-dim gate are honest mitigations, not closures (P-022).
5. **Determinism enables tamper-evidence without signing.** Because `regenerate(T)` is pure, anyone can recompute the expected artifact digest; the attestation corroborates it on a non-forgeable value — which is precisely why the orphan fallback is safe.

---

## Decomposition & Hand-Off

3a is complete when the algorithm, determinism contract, gates, completeness check, and Fallback A shape are accepted. The remaining Phase-3 design splits cleanly:

### → eng-devsecops (CI regeneration WORKFLOW structure + monitor)

Design (DESIGN, not implementation):

1. **Triggers (REQ-011):** `on: push: tags: ['v*']` + `workflow_dispatch` with optional `inputs.target_tag` (string, not required); **no other events**; `concurrency: cowork-skeleton`, `cancel-in-progress: false` (REQ-015).
2. **Job graph + per-job permissions (REQ-020; ADR-PROJ031-003 D4 A-1):** separate **attestation job** (`id-token: write` + `attestations: write`, **no** `contents: write`) and **push job** (`contents: write` only); no workflow-level grant spanning both; `needs:` ordering so attestation precedes push and a failed gate/attest skips the push (REQ-042 ordering).
3. **Gate sequence wiring (ADR-PROJ031-003 D4/D8 ordering):** event-discriminated tag resolution + **env-binding** of `${{ github.ref_name }}`/`${{ inputs.target_tag }}` (never `run:` interpolation — REQ-036) → **D5 build-time ancestor assertion** (`git merge-base --is-ancestor "${TAG}^{commit}" origin/main`, REQ-038) → invoke 3a generation (G3–G10, **including the G8 no-duplicate-skill-names gate — ADR-PROJ031-001 c-007, fail-closed before artifact/push**) → **D6 faithful-derivative** (`git diff --quiet "${TAG}..HEAD" -- ':!projects/' ':!tests/' ':!skills/.graveyard/' ':!.github/'` — the pathspec exclusions MUST mirror the **validated strip-set**, else D6 fails on the newly-stripped trees; add `':!docs/' ':!scripts/' ':!mkdocs.yml' …` if the recommended strips are applied) + secret scan (REQ-022) → **D8 content-safety** scan of `skills/ commands/ .claude/ .context/`, fail-closed (REQ-052) → hand the artifact to the attestation job.
4. **Loop-safety + hardening:** topological loop-safety (source triggers tags/dispatch only; dedicated repo has no push-back workflow — REQ-014/023, CR-02); **SHA-pin every Action across ALL `.github/workflows/`** incl. `cowork-monitor.yml` (REQ-017); `pull_request` never `pull_request_target` (ADR-PROJ031-003 D6); push-failure detection on `if: failure()`, no `continue-on-error` (REQ-037); job summary `if: always()` + failure step (REQ-016).
5. **D7 monitor workflow (`cowork-monitor.yml`, REQ-035/044/046/049/053/055; ADR-PROJ031-003 D7):** scheduled `≤ 6 h` **read-only** poll from source `main` (`git ls-remote`/`gh api`, **no clone**) performing **(a)** `gh attestation verify <artifact-file>` + bind to live tip via **tree-digest match** and **(b)** **freshness** (newest `v*` deployed within ≤ 2 h, REQ-049); **fail-closed** (any error/mismatch/freshness gap → issue + exit≠0, never silent `exit 0`, FM-033); **auto-revert** dispatch of the **`last-good-validated`** tag through the normal gated path; the **`actions: write`** grant is gated on **G-actions-write-safe** (REQ-017 all-workflow SHA-pin ∧ G-provenance) — until then, human-escalate only (REQ-053); meta-monitor heartbeat 25 h (REQ-044); tiered `[CRITICAL]` vs informational alerts (REQ-055).

6. **QG-3 determinism-critical step mechanics (FM-007-QG3 + FM-020-QG3 — eng-devsecops MUST enforce in the workflow YAML):**
   - **(a) G6 date pinning ($GITHUB_ENV mechanic, FM-007-QG3).** `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` MUST be pinned to `SRC_DATE` so they are in scope for the `git commit` *process* — either set **inline in the same `run:` step** as the commit, or propagated via `echo "GIT_AUTHOR_DATE=$SRC_DATE" >> "$GITHUB_ENV"` (and the committer date). A bare cross-step shell `export` is **FORBIDDEN**: it is lost between Actions steps, so git stamps wall-clock and the commit SHA — plus the D4 artifact digest and the D7 tree-digest — drift every run, silently. Add a **two-run idempotency check** (same tag ⇒ identical commit SHA) as a release gate. Committer *identity* SHOULD be pinned the same way (FM-014-QG3).
   - **(b) D6 faithful-derivative — stub+sentinel allow-list AND validated strip-set exclusions (FM-020-QG3 + Phase-3 strip amendment).** D6 is `git diff --quiet "${TAG}..HEAD" -- ':!projects/' ':!tests/' ':!skills/.graveyard/' ':!.github/'`. Two independent drivers of the pathspec: **(1) known-injected allow-list** — the `:!projects/` exclusion covers BOTH generated artifacts, `projects/README.md` (stub) **and** `projects/.jerry-skeleton-version` (version sentinel); no change is needed for them (both under `projects/`), and the implementer MUST NOT relocate the sentinel outside `projects/` (e.g. into `.claude/`) — such a file has no `TAG` pre-image and fails D6 on **every** release. **(2) validated strip-set** — because G4 now also removes `skills/.graveyard/` and `.github/`, the pathspec MUST exclude them (a stripped tree is a *deletion* vs `TAG`, which `--quiet` would otherwise flag); add `':!docs/' ':!scripts/' ':!mkdocs.yml' …` if the recommended strips are applied. 3a's G7 (§5) pins `projects/` to exactly the two injected files and asserts the stripped trees are empty; D6 + G7 together enforce `skeleton == TAG − {validated strip-set} + { stub, sentinel }` (REQ-022/D6).

### → eng-infra (artifact attestation / provenance / supply-chain infrastructure)

Design (DESIGN, not implementation):

1. **Build-provenance attestation (REQ-042; ADR-PROJ031-003 D4):** Sigstore-backed, SLSA-aligned attestation over the **3a deterministic artifact** (the `git archive`), bound to workflow run + source commit + repo; the exact `git archive` flag set / compression and the attestation tooling invocation are the **Phase-3 CI-design detail** ADR-PROJ031-003 D4 defers (consume the §3 determinism contract — including the gzip-mtime constraint — so the attested digest is stable).
2. **Immutable-release publishing (REQ-042):** publish the attested artifact as an immutable release asset per `v*` tag; this is the durable, CI-only-writable integrity surface.
3. **`gh attestation verify <artifact-file>` invocation (CV-005/R-006; ADR-PROJ031-003 D4/D7):** specify the **file-subject** verify form (a bare commit SHA is **not** a valid subject) and the tree-digest binding to the live default-branch tip — consumed by the D7 monitor; coordinate the artifact form with eng-devsecops's monitor.
4. **Supply-chain repo/credential infrastructure** *(infrastructure-adjacent; flagged for orchestrator confirmation per P-020 — could alternatively split to eng-devsecops):* dedicated-repo org-level ruleset with CI as **sole bypass actor**, zero human write (D2/REQ-040); **App installation token / single-repo deploy key** provisioning + private-key custody/rotation in a `main`/`v*`-restricted Actions Environment (D3/REQ-041/045/048); **`v*` tag-protection ruleset** on source (D5 push-time leg, REQ-039).
5. **SBOM (optional, SLSA trajectory; ADR-PROJ031-003 L2 §4):** assess whether to emit an SBOM for the artifact as a defense-in-depth provenance addition; **new/optional**, not required by any current REQ — propose, do not assume (P-020).

---

## Traceability Matrix

| # | Design element (3a) | Requirements | ADR / source |
|---|---------------------|--------------|--------------|
| D-01 | Event-discriminated tag resolve + allow-list validate | REQ-036 | ADR-PROJ031-001 RT-04, IT3-005 |
| D-02 | Checkout `v*` (frozen tree), `fetch-depth: 0` | REQ-007 | ADR-PROJ031-001 Decision; D5 dependency |
| D-03 | Denylist strip (validated): `projects/ tests/ skills/.graveyard .github` (+ SHOULD `docs/ scripts/ mkdocs.yml …`) | REQ-001/002 | ADR-PROJ031-001 c-003 Phase-3 amendment; live install 2026-07-02; R-001 |
| D-04 | Static stub `projects/README.md` (+`--no-verify`) | REQ-004/004a | ADR-PROJ031-001 c-006; R-001 |
| D-05 | Deterministic commit (pinned dates/parent/40-char SHA, unsigned) | REQ-003/008 | ADR-PROJ031-001 §Regeneration Commit Determinism; **FM-007-QG3** (GIT_*_DATE via same-step/`$GITHUB_ENV`, not `export`) |
| D-06 | Commit determinism contract | REQ-003/004a | ADR-PROJ031-001 idempotency proof |
| D-07 | **Artifact determinism contract** (archive + gzip-mtime trap) | REQ-042 | ADR-PROJ031-003 D4 (R-006, Iter-8) — design extension |
| D-08 | `git archive` deterministic artifact (G10) | REQ-042 | ADR-PROJ031-003 D4 |
| D-09 | Cross-repo force-push (App token) | REQ-041 | ADR-PROJ031-003 D3; ADR-PROJ031-001 CC-005 |
| D-10 | Multi-dim gate: file-count/pack/clone, fail-closed, two bands | REQ-006/034d/050/055 | ADR-PROJ031-001 §Clone-Weight; FM-062/IN-001/IN-002 |
| D-11 | Option A→B orphan flip parameter (`provenance_mode`) | REQ-006/034d | ADR-PROJ031-001 §Clone-Weight (IT3-004 integrity-neutral) |
| D-12 | Retention-surface completeness (denylist + plugin.json-derived) | REQ-005/009/010 | ADR-PROJ031-001 R-008/FM-030 |
| D-13 | Fallback A — version sentinel (`projects/.jerry-skeleton-version`, in D6 allow-list) + version-check skill | REQ-054 / OQ-048 / REQ-022 | ADR-PROJ031-001 G-update Fallback Architecture (Fallback A); **FM-020-QG3** (D6 known-injected allow-list) |
| D-14 | **No-duplicate-skill-names gate (G8, fail-closed before artifact/push)** | REQ (new — nse-requirements owns) | **ADR-PROJ031-001 c-007**; live install 2026-07-02 (marketplace dup-skill rejection) |
| D-15 | **Runtime-dep RETAIN: `src/` + `pyproject.toml` + `uv.lock`** (hooks shell `uv run jerry`) | REQ-005 | **ADR-PROJ031-001 c-008**; hooks fail-open ⇒ silent guardrail no-op if stripped |

---

## Pending Validation (P-022)

Honest status — this is a **DESIGN**; nothing below is achieved. Each defers to a named gate (ADR-PROJ031-003 Phase-5 Validation Gate Set / requirements Phase-5 Authorization Checklist).

| Item | Status | Resolved by |
|------|--------|-------------|
| File-count is the operative CoWork ceiling | unverified (may be size/time-based) | **G-headroom** (REQ-034 4-dim, incl. live install) |
| Update reaches already-installed users | **un-testable** (platform "+" UI removed) | **G-update-pre** (Phase-5 ENTRY; Fallback A/C + B if FAIL/BLOCKED) |
| Exact `git archive` flags / compression / attest invocation | design detail pending | eng-infra / Phase-5 (consume §3 contract) |
| D8 pattern catalog + detector tool | owned elsewhere | eng-architect (STRIDE) → **G-content** |
| Provenance gate, ruleset, credential operative on live target | designed-not-implemented | **G-provenance / G-prevention** |
| D7 monitor detects tamper + staleness, fails closed, reverts | designed | **G-monitor**; `actions: write` gated on **G-actions-write-safe** |
| Fallback A is *needed* | conditional | G-update-pre outcome (buildable now regardless) |

---

## References

| # | Source | Relevance |
|---|--------|-----------|
| 1 | `../decisions/ADR-PROJ031-001-skeleton-distribution-strategy.md` | Option A generation, determinism contract, clone-weight, R-008, G-update fallbacks |
| 2 | `../decisions/ADR-PROJ031-003-credential-protection-supply-chain.md` | D1–D8, gate ordering, D4 artifact attestation (R-006/CV-005), D7 monitor, Phase-5 gates |
| 3 | `../requirements/phase1-requirements.md` | REQ-001..055, acceptance criteria, Phase-5 Authorization Checklist |
| 4 | `../research/R-001-cowork-test-validation.md` | Proven strip (1,749 → ~1,417 for `projects/`+`tests/`; **superseded by the Phase-3 live-install validated set → 1,399**), test-coupling, `--no-verify` requirement |

---

**QG-3 remediation (2026-06-30):** **ROOT-3/FM-020-QG3** resolved via **option (b)** — the version sentinel is the dedicated static file `projects/.jerry-skeleton-version`, placed under `projects/` so it sits inside D6's existing `:!projects/` known-injected allow-list alongside the `projects/README.md` stub (§3(c), §5 G7 pin); the settled ADR-PROJ031-001 Fallback A sentinel file is preserved, not deleted (P-020). **ROOT-2/FM-007-QG3** resolved by requiring the G6 GIT_*_DATE pin to reach the commit process via same-step inline binding or `$GITHUB_ENV` — never a bare cross-step `export` (§2 G6, §3(a), Hand-Off item 6). Both fixes are design-level statements of constraint; eng-devsecops owns the workflow-YAML mechanics.

**Phase-3 amendment (2026-07-02) — mirror of the ADR-PROJ031-001 live-install revision:** (1) the G4 strip step is expanded to the **validated** set `projects/ tests/ skills/.graveyard .github` (6,344 → **1,399** files, install-validated on Claude Web 2026-07-02), with a documented SHOULD-strip of `docs/ scripts/ mkdocs.yml CNAME .nojekyll` + dev/governance cruft (Makefile, .pre-commit-config.yaml, pytest.ini, CHANGELOG.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, GOVERNANCE.md) → **~1,114**; `src/`+`pyproject.toml`+`uv.lock` are **RETAINED** (c-008 — hook runtime). (2) A **new fail-closed G8 no-duplicate-skill-names gate** (ADR-PROJ031-001 c-007) runs on the committed tip after G7 and before the multi-dim gate (G9), artifact (G10), and push — the exact marketplace invariant the live test caught; the downstream steps renumber accordingly (G1–G10). (3) Retention is reframed **positively** (plugin surface + runtime deps), and D6's pathspec is extended to mirror the validated strip-set. No change to the Option A technique, determinism contract, or AG-02 strategy (P-020).

*Generated by jerry:nse-architecture (NPR 7123.1D Processes 3, 4, 17). Self-review S-010 applied (H-15). Settled ADR decisions reused, not re-opened (P-020). No sub-agents spawned (P-003). Designed-but-unvalidated controls tagged per the Claim-Status Convention (P-022); the strip-set is install-validated (2026-07-02).*
