---
DISCLAIMER: This design is AI-generated guidance based on infrastructure security
engineering standards (CIS Benchmarks, SLSA, NIST SSDF). It is advisory only and
does not constitute official certification. All architecture decisions require human
review and professional engineering judgment. Not for use in mission-critical
deployments without SME validation.
---

# Phase 3 Attestation & Provenance Design (3b — Infrastructure)

> **Document ID:** FAD-PROJ031-3B-001
> **Project:** PROJ-031-cowork-skeleton
> **Phase:** Phase 3 — Skeleton + CI DESIGN (sub-phase 3b, attestation/provenance/supply-chain infrastructure)
> **Agent:** jerry:eng-infra (Secure Infrastructure Engineer)
> **Criticality:** C4 (AE-005 security-relevant supply-chain; quality target >= 0.95)
> **Created:** 2026-06-30
> **Status:** Draft — DESIGN (Phase-6 implements; no control below is an achieved fact)
> **Inputs (FINAL — P-020, not re-opened):** phase3-skeleton-generation-design.md (G9 deterministic artifact, gzip-mtime trap §3), ADR-PROJ031-003 (D2/D3/D4/D5/D6/D7, RTB-1..5), requirements REQ-038/039/040/041/042/045/048
> **Claim-Status Convention (P-022):** Every control is **Designed — operational validation pending [G-x]**. Achieved present tense is reserved for Phase-5/6 post-validation.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Infrastructure security posture, SLSA level, supply-chain risk summary |
| [Claim-Status Convention (P-022)](#claim-status-convention-p-022) | Honest framing tag for designed-not-validated controls |
| [Scope and Non-Goals](#scope-and-non-goals) | eng-infra deliverables vs. eng-devsecops boundary |
| [L1: Technical Detail](#l1-technical-detail) | Five design areas: artifact, attest, verify, release, hardening |
| [1. Deterministic Artifact Recipe](#1-deterministic-artifact-recipe--gzip-mtime-trap-resolution) | Root cause, canonical plain-TAR solution, compressed alternative |
| [2. Sigstore Attestation](#2-sigstore-attestation-actionsattest) | actions/attest step, permissions isolation, SLSA predicate |
| [3. Verification](#3-verification--gh-attestation-verify-invocation) | Exact gh attestation verify form; D7 monitor flow; digest-based binding (ROOT-1 corrected); MONITOR HAND-OFF |
| [4. Immutable Release Publishing](#4-immutable-release-publishing) | Release asset layout; immutability assurance |
| [5. Repo & Credential Hardening](#5-repo--credential-hardening) | Org ruleset D2; App token D3; Actions Environment; key rotation |
| [6. Tag Protection & Provenance Gate (D5)](#6-tag-protection--provenance-gate-d5) | v* ruleset; merge-base assertion placement |
| [7. SBOM: CycloneDX of Python Dependency Surface](#7-sbom-cyclonedx-of-python-dependency-surface) | In/out recommendation with rationale |
| [L2: Strategic Implications](#l2-strategic-implications) | Supply-chain risk landscape, SLSA maturity roadmap, evolution path |
| [Traceability Matrix](#traceability-matrix) | Design element to REQ/ADR |
| [Pending Validation (P-022)](#pending-validation-p-022) | Honest open items deferred to Phase-5/6 |
| [References](#references) | Cited inputs |

---

## L0: Executive Summary

The skeleton artifact (`jerry-claude-plugin`) is executable code (Python hooks, skill markdown) that runs on every user's session start the moment an org admin registers `geekatron/jerry-claude-plugin`. That blast radius justifies a three-layer supply-chain posture:

1. **Prevention** — org-level ruleset locks the dedicated repo's default branch against all principals except the named CI identity (D2/REQ-040); a `v*` tag-protection ruleset on the source repo prevents rogue-tag injection (D5/REQ-039).
2. **Attestation** — a Sigstore-backed SLSA build-provenance attestation over a **bit-stable artifact** (the deterministic TAR from G9) anchors integrity in an immutable, publicly verifiable transparency log independent of any GitHub permission (D4/REQ-042).
3. **Detection** — the D7 backstop monitor downloads the attested artifact, runs `gh attestation verify` (Sigstore exit-code verdict), re-derives the deterministic TAR from the live dedicated-repo tip via a shallow fetch, compares sha256 digests (tree-digest match — the SLSA predicate gitCommit is metadata only, not the verification key), and checks freshness — all fail-closed (REQ-035/049; ROOT-1 corrected 2026-06-30).

**Gzip-mtime trap — resolved here.** The upstream design (phase3-skeleton-generation-design.md §3) flags that piping `git archive` output through a standard `gzip` call embeds the current wall-clock timestamp and OS byte in the gzip header, silently breaking the digest between runs. This design resolves the trap: the **canonical attested artifact is a plain uncompressed TAR** produced with `git archive --format=tar "${COMMIT_SHA}"`. No gzip wrapper means no drift surface; the TAR entry mtimes derive from the G6-pinned committer date, which is invariant per release tag.

**SLSA target level: 3** — hosted platform (GitHub Actions), signed non-falsifiable provenance in the public Rekor transparency log, and hardened runner configuration (D6) all satisfy L3 requirements. L4 (hermetic builds, two-party review) is the next milestone; the current architecture does not yet close it.

**SBOM: IN** — a CycloneDX Software Bill of Materials of the skeleton's Python dependency surface (`pyproject.toml`/`uv.lock`) is generated using the existing `cyclonedx-py` tooling already in the release pipeline. It covers the actionable executable surface (`src/`, hooks) that installs into every user's session and is published as an attested release asset without inflating the skeleton tree.

**Key residuals (P-022 honesty):** no control in this design achieves install-time verification (RTB-5 — CoWork does not invoke `gh attestation verify` at plugin install); an organization owner can suppress the ruleset (RTB-1); credential theft enables forgery within the ≤ 6 h D7 detection window (RTB-4). These are bounded, not closed, by the controls below.

---

## Claim-Status Convention (P-022)

> Every security control below is **Designed — operational validation pending**. The dedicated repo `geekatron/jerry-claude-plugin` does not yet exist, no ruleset is applied, no attestation has been produced, and no monitor has run. Achieved present tense ("is prevented", "is attested") is **FORBIDDEN** in this document. Write "is designed to prevent", "will produce once G-x passes."

| Tag | Meaning |
|-----|---------|
| **Designed — operational validation pending [G-x]** | Fully specified; enabling infrastructure does not yet exist; empirical proof is the named Phase-5 gate |
| **Implemented & validated** | Infrastructure exists AND the control has been exercised — NO Phase-3 control is here yet |

Default classification for all controls in this document: **Designed — operational validation pending**.

---

## Scope and Non-Goals

**eng-infra owns (this design):**

- Deterministic artifact recipe (gzip-mtime fix; canonical TAR form; artifact naming)
- Sigstore build-provenance attestation step configuration (`actions/attest`, permissions, predicate)
- `gh attestation verify` invocation form for the D7 monitor
- Immutable release asset publishing layout
- Org-level ruleset configuration intent (D2), GitHub App token custody (D3), Actions Environment gating (REQ-045), key rotation policy (REQ-048)
- `v*` tag-protection ruleset on the source repo (D5 push-time leg)
- SBOM generation and attestation (CycloneDX)

**Explicitly NOT in this design (handed off — settled in other documents, P-020):**

- Workflow job graph, triggers, concurrency, gate sequencing, D6 runner hardening details → **eng-devsecops**
- D5 build-time provenance assertion (`git merge-base --is-ancestor`) → **eng-devsecops** (build-time, placed in workflow before G3)
- D8 content-safety pattern catalog and scanner tool → **eng-architect**
- D7 monitor full workflow (fail-closed logic, auto-revert dispatch, freshness check code) → **eng-devsecops**; this design provides the `gh attestation verify` invocation that the monitor uses

**Settled and not re-opened (P-020):** Option A generation, dedicated-repo distribution model (ADR-PROJ031-001/ADR-PROJ031-003 D1), per-job `permissions:` isolation (ADR-PROJ031-003 D4 A-1), gate ordering (deterministic commit → D6/D8 → attest → push, ADR-PROJ031-003 D4 C-7).

---

## L1: Technical Detail

### 1. Deterministic Artifact Recipe — Gzip-Mtime Trap Resolution

#### 1.1 Root Cause: What the Gzip Header Embeds

The gzip format (RFC 1952) includes a 10-byte header:

| Bytes | Field | Problem |
|-------|-------|---------|
| 4–7 | MTIME (Unix timestamp) | Defaults to wall-clock time at compression; **changes every run** |
| 9 | OS byte | Operating system identifier (3=Unix, 11=NTFS, 0=FAT); **varies by platform** |

If any step in the pipeline produces the artifact with `gzip` (without special flags), or uses `tar.gz` via a tool that writes the MTIME field, the SHA256 digest of the compressed artifact drifts between runs even when the content is identical. Because ADR-PROJ031-003 D4 anchors the attestation to the artifact's digest, a drifting digest means:

- The same release tag produces different digests → attestation on run N cannot be verified on run N+1
- `gh attestation verify` will fail on the re-downloaded artifact
- The D7 monitor's tree-digest match breaks

This is the trap flagged in phase3-skeleton-generation-design.md §3 ("Compression wrapper" row).

Note: `git archive --format=tar.gz` may internally zero the MTIME field in modern git versions, but its behavior regarding the OS byte is not standardized across git builds and is therefore unreliable as the sole determinism guarantee. The canonical fix below avoids the ambiguity entirely.

#### 1.2 Canonical Solution: Plain TAR (REQUIRED for Attested Artifact)

**Production form (G9 implementation seed):**

```bash
# Called at G9 in the generation algorithm, after G7+G8 gates pass and
# before the attestation job. COMMIT_SHA = the G6 deterministic commit.
ARTIFACT_NAME="jerry-claude-plugin-${TAG}.tar"
git archive --format=tar "${COMMIT_SHA}" > "${ARTIFACT_NAME}"
ARTIFACT_DIGEST=$(sha256sum "${ARTIFACT_NAME}" | cut -d' ' -f1)
```

**Why plain TAR eliminates the trap:**

| TAR artifact input | Pin | Invariant because |
|--------------------|-----|-------------------|
| Archive content (file tree) | `git archive` of `${COMMIT_SHA}` | tree pinned by G3–G5 |
| TAR entry mtimes | Git derives from the commit's committer date | committer date pinned in G6 (`GIT_COMMITTER_DATE = SRC_DATE`) |
| File ordering in archive | `git archive` uses deterministic lexicographic order | no filesystem readdir randomness |
| Compression header | **None — plain TAR has no compression header** | no MTIME field, no OS byte |

Result: `sha256(jerry-claude-plugin-${TAG}.tar)` is bit-stable across all runs for a given release tag on any Linux runner.

**Artifact naming convention:** `jerry-claude-plugin-${TAG}.tar` where `${TAG}` is the allow-list-validated `v{N}.{N}.{N}` form from G2 (e.g., `jerry-claude-plugin-v0.31.5.tar`). This name encodes the release identity deterministically.

#### 1.3 Alternative: Compressed Asset (NOT the Attested Artifact)

If download size is a concern, a `.tar.gz` companion MAY be published alongside the attested `.tar` as an unattested convenience download. To produce it deterministically on Linux-only GitHub Actions runners:

```bash
# Pipe through gzip -n: suppresses MTIME (set to 0) and FNAME fields.
# OS byte = 3 (Unix) is consistent across GitHub Actions ubuntu-latest.
# This produces a deterministic .tar.gz ONLY on the same OS type.
git archive --format=tar "${COMMIT_SHA}" | gzip -n > "jerry-claude-plugin-${TAG}.tar.gz"
```

**Design constraint:** The `.tar.gz` MUST NOT be the attestation subject. The plain `.tar` is the canonical integrity reference. The `.tar.gz` is a convenience download with no attestation binding. This avoids any residual OS-byte ambiguity from affecting supply-chain integrity.

#### 1.4 Determinism Proof (Extends ADR-PROJ031-001 + phase3-skeleton-generation-design.md §3)

For a given release tag `T`, `artifact_digest(T) = sha256(git archive --format=tar COMMIT_SHA(T))` where `COMMIT_SHA(T)` is the G6 deterministic commit SHA (proven bit-stable in phase3-skeleton-generation-design.md §3a). Since COMMIT_SHA(T) is invariant per T, and `git archive --format=tar` is a pure function of the commit SHA, `artifact_digest(T)` is invariant per T. Both `commit_sha(T)` and `artifact_digest(T)` are determined by T and nothing else — no wall-clock time, no runner identity, no GitHub run ID.

---

### 2. Sigstore Attestation: actions/attest

#### 2.1 Tooling Selection (P-022)

Per current GitHub documentation (confirmed 2026-06-30): `actions/attest-build-provenance` v4+ is a thin wrapper over `actions/attest`. New implementations should use `actions/attest` directly. This design specifies `actions/attest` as the canonical action.

SLSA predicate type: `https://slsa.dev/provenance/v1` (the default when `actions/attest` is called without an explicit `predicate-type`). This produces SLSA Build L3-compatible provenance bound to the workflow run, source commit SHA, and source repository.

Transparency log: `geekatron/jerry` is a public repository, so attestations are published to the **public-good Sigstore Rekor instance** (`rekor.sigstore.dev`) — an immutable, append-only, publicly auditable log. Attestations are non-deletable from this log by design; integrity does not depend on GitHub uptime.

#### 2.2 Required Permissions (Attestation Job)

Per ADR-PROJ031-003 D4 A-1, the attestation job is **isolated** from the push job with separate `permissions:` blocks:

```yaml
# Attestation job (conceptual — Phase-6 implementation detail)
attestation-job:
  needs: [quality-gate-job]    # Runs ONLY after D6 faithful-derivative + D8 content-safety PASS
  permissions:
    id-token: write            # Mint OIDC token for Sigstore signing certificate
    attestations: write        # Persist the attestation to GitHub's attestation store
    # artifact-metadata: write # Current actions/attest v4 documentation lists this as required;
    #                          # Phase-6 MUST confirm exact permission set for the pinned version.
    # contents: write is ABSENT from this job (ADR-PROJ031-003 D4 A-1)
```

The push job remains `contents: write` only, with no attestation permissions. No single job holds both capability sets (REQ-020).

#### 2.3 Attestation Step Configuration

```yaml
# Conceptual sketch — Phase-6 finalizes the pinned SHA per REQ-017
- name: Generate deterministic artifact
  run: |
    git archive --format=tar "${COMMIT_SHA}" > "jerry-claude-plugin-${TAG}.tar"

- name: Attest build provenance (D4)
  id: attest
  uses: actions/attest@{PINNED_40CHAR_SHA}    # Pin to commit SHA per REQ-017; never @v4
  with:
    subject-path: "jerry-claude-plugin-${TAG}.tar"
    # predicate-type omitted: defaults to SLSA build provenance v1
```

**Outputs consumed downstream:**
- `steps.attest.outputs.bundle-path` — path to the Sigstore bundle JSON; upload as a release asset alongside the `.tar` for offline verification
- `steps.attest.outputs.attestation-url` — shareable Sigstore transparency log URL for audit

#### 2.4 Ordering (C-7, ADR-PROJ031-003 D4)

The attested artifact MUST be produced after all quality and content gates and before the cross-repo push. The load-bearing sequence is:

```
G9 produce deterministic artifact (.tar)
  │
  ▼ attestation job starts (needs: quality-gate-job)
D4 actions/attest → artifact signed in Rekor
  │
  ▼ push job starts (needs: attestation-job)
D3 cross-repo force-push (App token / deploy key)
D4 gh release create (publish .tar + SBOM as release assets)
```

If the attestation step exits non-zero, the `needs:` graph prevents the push job from executing — no live-but-unattested artifact window.

---

### 3. Verification: gh attestation verify Invocation

#### 3.1 Canonical Verification Form

```bash
# File-path subject — the only form gh attestation verify accepts
# (a bare git commit SHA is NOT a valid subject; CV-005/R-006)
gh attestation verify "jerry-claude-plugin-${TAG}.tar" \
  --repo geekatron/jerry \
  --signer-workflow .github/workflows/cowork-skeleton.yml
```

**Flag rationale:**

| Flag | Value | Purpose |
|------|-------|---------|
| `[file-path]` | `jerry-claude-plugin-${TAG}.tar` | The deterministic attested artifact (§1.2) |
| `--repo` | `geekatron/jerry` | Scopes lookup to attestations produced by the source repo's CI |
| `--signer-workflow` | `.github/workflows/cowork-skeleton.yml` | Restricts acceptance to the canonical generation workflow only; prevents a compromised but differently-named workflow from producing a valid attestation |

The `--signer-workflow` flag provides defense-in-depth against workflow substitution attacks: even if an attacker could produce an attestation using a different workflow in `geekatron/jerry`, this flag would reject it.

**Exit codes:** 0 = attestation valid and policy satisfied; non-zero = invalid, absent, or policy mismatch. The D7 monitor treats any non-zero exit as a tamper/failure trigger (REQ-035, fail-closed FM-033).

#### 3.2 D7 Monitor Verification Flow — Corrected (ROOT-1 / DA-001 fix)

> **ROOT-1 correction (2026-06-30):** The prior design bound verification to `ATTESTED_COMMIT` (the `gitCommit` field extracted from the SLSA predicate) and compared it to `LIVE_TIP` (`git ls-remote jerry-claude-plugin HEAD`). These two values are **always unequal by design**: the SLSA predicate records `SRC_SHA` (the source commit in `geekatron/jerry` that triggered the generation workflow), while `LIVE_TIP` is `G6_SHA` (the generated skeleton commit pushed to `geekatron/jerry-claude-plugin`, which has `SRC` as its parent but is a different object). `SRC_SHA ≠ G6_SHA` always — the check could never pass. The SLSA predicate `gitCommit` is **metadata only and is not the verification key.** The corrected design binds on the **deterministic TAR digest**: `sha256(git archive --format=tar)` is identical for identical tree content regardless of which commit holds it. Removing the SHA comparison also removes the implicit fallback to mutable release-body content that ADR-PROJ031-003 condemned (SC-04). See also §3.3 MONITOR HAND-OFF.

The D7 monitor runs on schedule from `geekatron/jerry` `main`. Its verification sequence (conceptual — eng-devsecops owns the full workflow implementation; see §3.3 for the binding hand-off):

```bash
# Step 1: Download the attested artifact from the immutable release
gh release download "${LATEST_TAG}" \
  --repo geekatron/jerry \
  --pattern "jerry-claude-plugin-${LATEST_TAG}.tar" \
  --dir "${WORK_DIR}"

# Step 2: Verify the attestation (Sigstore exit-code is the sole integrity verdict)
# gh attestation verify computes sha256 of the provided file and looks up the
# matching attestation in the Rekor transparency log. A locally-derived file works
# identically to the published asset when content is identical (verified 2026-06-30).
gh attestation verify "${WORK_DIR}/jerry-claude-plugin-${LATEST_TAG}.tar" \
  --repo geekatron/jerry \
  --signer-workflow .github/workflows/cowork-skeleton.yml
# Non-zero exit → open issue + exit non-zero (fail-closed, FM-033). No --format json
# needed: the SLSA predicate gitCommit field is metadata only, NOT the verification key.

# Step 3: Compute the attested artifact digest — THE verification key
ATTESTED_DIGEST=$(sha256sum "${WORK_DIR}/jerry-claude-plugin-${LATEST_TAG}.tar" | cut -d' ' -f1)

# Step 4: Read the live dedicated-repo tip SHA (read-only, no full clone — CV-006/ADR-PROJ031-003 D7)
G6_SHA=$(git ls-remote https://github.com/geekatron/jerry-claude-plugin.git HEAD | cut -f1)

# Step 5: Re-derive the deterministic TAR from the live tip (shallow fetch — NOT a full clone)
# --depth=1 fetches only tree+blob objects for the single tip commit; no history traversal.
# This satisfies the CV-006 "no full clone" constraint while providing the exact git-archive
# byte stream needed to reproduce the attested artifact's sha256.
git init --bare "${WORK_DIR}/cowork-fetch.git"
git -C "${WORK_DIR}/cowork-fetch.git" fetch --depth=1 \
  "https://github.com/geekatron/jerry-claude-plugin.git" "${G6_SHA}"
git -C "${WORK_DIR}/cowork-fetch.git" archive --format=tar "${G6_SHA}" \
  > "${WORK_DIR}/live-tip.tar"

# Step 6: Compute the live-tip digest
LIVE_DIGEST=$(sha256sum "${WORK_DIR}/live-tip.tar" | cut -d' ' -f1)

# Step 7: Tree-digest match — the correct binding invariant (ROOT-1 fix)
# Invariant: tree(skeleton) → git archive --format=tar → sha256 is identical for
# identical content regardless of which commit holds it. Tamper on the dedicated branch
# changes the tree → changes the tar digest → ATTESTED_DIGEST ≠ LIVE_DIGEST → fail-closed.
# The SLSA predicate's gitCommit (= SRC_SHA from geekatron/jerry) is NEVER compared to
# G6_SHA (the generated skeleton commit): they differ by design and that comparison is wrong.
if [ "${ATTESTED_DIGEST}" != "${LIVE_DIGEST}" ]; then
  echo "[CRITICAL] Tree-digest mismatch: attested=${ATTESTED_DIGEST}, live-tip(G6=${G6_SHA})=${LIVE_DIGEST}" >&2
  gh issue create \
    --title "[CRITICAL] Tree-digest mismatch on geekatron/jerry-claude-plugin" \
    --body "Attested artifact digest: ${ATTESTED_DIGEST}. Live-tip (G6_SHA=${G6_SHA}) digest: ${LIVE_DIGEST}. Tamper or failed regeneration detected."
  exit 1
fi

# Step 8: Freshness check (IN-002 — REQ-049 co-equal condition)
# A green tree-digest match on a STALE tip is a FRESHNESS FAILURE, not a pass.
# Assert: the newest source v* tag produced a matching dedicated-repo deployment within ≤ 2h.
# Implementation detail: compare LATEST_TAG push timestamp vs. G6_SHA commit timestamp.
```

**Fail-closed mandate (FM-033):** Any unhandled error (network failure, missing `gh` CLI, missing `git`, empty `G6_SHA`, zero-byte tar, unexpected exit from the shallow fetch) MUST exit non-zero and open an issue. The monitor MUST NOT `exit 0` when it cannot complete a valid check.

---

#### 3.3 MONITOR HAND-OFF for eng-devsecops

> **This subsection is the binding specification for the D7 monitor CI implementation.** eng-devsecops MUST mirror these exact steps in `cowork-monitor.yml`. No deviation from the digest-based binding is permitted; in particular, no SHA-comparison against SLSA-predicate fields and no fallback to release-body content (SC-04 regression).

**The invariant eng-devsecops enforces:**

```
sha256( git archive --format=tar <G6_SHA from live jerry-claude-plugin tip> )
  ==
sha256( published jerry-claude-plugin-${TAG}.tar release asset )
  AND
gh attestation verify <published tar> --repo geekatron/jerry exits 0
  AND
LATEST source v* tag deployed to jerry-claude-plugin within ≤ 2 h
```

**Exact monitor steps (all three conditions are co-equal; failure of any → FAIL-CLOSED):**

| Step | Action | Failure mode |
|------|--------|-------------|
| 1 | `gh release download ${LATEST_TAG} --repo geekatron/jerry --pattern "jerry-claude-plugin-${LATEST_TAG}.tar" --dir ${WORK_DIR}` | Missing release asset → FAIL-CLOSED |
| 2 | `gh attestation verify ${WORK_DIR}/jerry-claude-plugin-${LATEST_TAG}.tar --repo geekatron/jerry --signer-workflow .github/workflows/cowork-skeleton.yml`; exit code 0 required | Non-zero exit → tamper detected → FAIL-CLOSED |
| 3 | `ATTESTED_DIGEST=$(sha256sum ${WORK_DIR}/jerry-claude-plugin-${LATEST_TAG}.tar \| cut -d' ' -f1)` | Empty digest → FAIL-CLOSED |
| 4 | `G6_SHA=$(git ls-remote https://github.com/geekatron/jerry-claude-plugin.git HEAD \| cut -f1)` — read-only, no clone | Empty SHA → FAIL-CLOSED |
| 5 | Shallow fetch + `git archive --format=tar ${G6_SHA}` → `${WORK_DIR}/live-tip.tar` (see §3.2 Step 5) | Fetch/archive failure → FAIL-CLOSED |
| 6 | `LIVE_DIGEST=$(sha256sum ${WORK_DIR}/live-tip.tar \| cut -d' ' -f1)` | Empty or zero-byte → FAIL-CLOSED |
| 7 | Assert `${ATTESTED_DIGEST} == ${LIVE_DIGEST}` | Mismatch → tamper on dedicated branch → open CRITICAL issue + FAIL-CLOSED |
| 8 | Freshness: assert LATEST source `v*` tag deployed to `jerry-claude-plugin` within ≤ 2 h of tag push timestamp (REQ-049) | Stale tip with green digest match → open STALENESS issue + FAIL-CLOSED |

**What the monitor MUST NOT do:**
- Extract `gitCommit` from the SLSA predicate and compare to the live tip SHA — this always fails by design (SRC_SHA ≠ G6_SHA) and was the ROOT-1 defect
- Use `--format json` with `jq` to parse the attestation predicate as a verification key — the predicate is metadata only
- Fall back to release-body text content for any integrity assertion (SC-04 regression, condemned by ADR-PROJ031-003)
- Exit 0 on any unhandled error (FM-033 silent-failure prohibition)

**Clarification on `gh attestation verify` with a locally-derived file (verified 2026-06-30):** The command computes sha256 of the provided file path and looks up the matching attestation in the Rekor transparency log / GitHub attestation API. A locally re-derived tar produced by `git archive --format=tar ${G6_SHA}` will be accepted and will verify successfully if and only if its sha256 matches an entry attested by CI — which holds when the live tip has the same tree as the attested artifact. The command does NOT require the file to be the originally published download; digest identity is sufficient.

**Residual for Phase-6 (P-222):** The shallow-fetch approach (Step 5) must be empirically confirmed on `ubuntu-latest` GitHub Actions runners: (a) `git fetch --depth=1` + `git archive` produces byte-identical output to the original CI `git archive` step for the same commit SHA; (b) no unexpected mtime injection from the runner's pinned `git` version. Validation gate: two-run idempotency test during Phase-6 implementation (REQ-003 AC, NFR-001 AC).

#### 3.4 Third-Party Verification

Any external party (security auditor, user) can verify a release without any GitHub credentials:

```bash
# 1. Download the artifact
gh release download vN.N.N --repo geekatron/jerry --pattern "jerry-claude-plugin-vN.N.N.tar"

# 2. Verify against the public Rekor log (public repo → public Sigstore instance)
gh attestation verify "jerry-claude-plugin-vN.N.N.tar" \
  --repo geekatron/jerry \
  --signer-workflow .github/workflows/cowork-skeleton.yml

# 3. Optionally verify against Rekor directly (without gh CLI dependency)
cosign verify-attestation "jerry-claude-plugin-vN.N.N.tar" \
  --certificate-identity-regexp "^https://github.com/geekatron/jerry/" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

The Rekor transparency log entry is the durable, GitHub-independent integrity reference. It cannot be forged or deleted by any GitHub actor.

---

### 4. Immutable Release Publishing

#### 4.1 Release Asset Layout

The immutable GitHub Release for each `v*` tag contains the following assets:

| Asset | Description | Attested? |
|-------|-------------|-----------|
| `jerry-claude-plugin-${TAG}.tar` | Deterministic skeleton TAR (canonical artifact) | **Yes** (SLSA build provenance) |
| `sbom-jerry-claude-plugin-${TAG}.cdx.json` | CycloneDX SBOM of Python dependency surface | **Yes** (SBOM attestation) |
| `jerry-claude-plugin-${TAG}.tar.gz` | Compressed convenience download (`gzip -n`) | No (unattested; for download size only) |
| `jerry-claude-plugin-${TAG}.bundle` | Sigstore bundle JSON from attestation | No (attestation metadata; offline verify) |

The release is created by the push job after the attestation job completes:

```bash
# Conceptual — Phase-6 finalizes gh release create flags
gh release create "${TAG}" \
  "jerry-claude-plugin-${TAG}.tar" \
  "sbom-jerry-claude-plugin-${TAG}.cdx.json" \
  "jerry-claude-plugin-${TAG}.bundle" \
  "jerry-claude-plugin-${TAG}.tar.gz" \
  --repo geekatron/jerry \
  --notes-from-tag \
  --verify-tag
```

#### 4.2 Immutability Assurance

GitHub Releases are not immutable by default (release notes are editable with `contents: write`), but the **attestation is immutable** — it is anchored in the public Rekor log and cannot be altered regardless of what happens to the Release notes. ADR-PROJ031-003 D4 establishes that the attestation (not the Release notes) is the integrity anchor; editable Release notes are explicitly NOT used as integrity evidence.

Additional immutability assurance from the `v*` tag-protection ruleset (§6): once a `v*` tag is created and attested, the ruleset prevents the tag from being moved or deleted by non-CI principals, binding the release to the exact commit that was attested.

---

### 5. Repo & Credential Hardening

#### 5.1 Org-Level Ruleset — Dedicated Repo (D2, REQ-040)

**Designed — operational validation pending [G-prevention].**

Configuration intent for the org-level ruleset targeting `geekatron/jerry-claude-plugin` `~DEFAULT_BRANCH`:

| Ruleset parameter | Value | Rationale |
|-------------------|-------|-----------|
| Scope | Org-level (non-overridable by repo admins) | Repository admins CANNOT override org-level rulesets; only org owners CAN (RTB-1) |
| Target | `geekatron/jerry-claude-plugin` `~DEFAULT_BRANCH` | The artifact distribution surface |
| Rules enabled | `non_fast_forward`, `update` (deny push), `deletion`, `tag_immutability` | Prevents direct push, deletion, and tag mutation |
| `bypass_actors` | Exactly one: the GitHub App identity (by App ID) | CI is the sole push principal; zero human write |
| Human collaborators on dedicated repo | Zero with write access | Enforced by keeping the repo under org ownership with no explicit collaborator grants |
| Audit controls | Alert on: ruleset change, default-branch rename, visibility change, bypass-actor modification | Detects org-owner suppression (RTB-1/DR-02/DR-04/DR-05) within the ≤ 6 h D7 window |

**Residual (RTB-1):** A GitHub organization owner can modify or delete the org-level ruleset and push directly. This path is **not prevented at any maturity**; it is detection-only, bounded by org-owner-count minimization, mandatory 2FA/SSO, and the attestation backstop (D4/D7).

**Verification (Phase-6):** `gh api orgs/geekatron/rulesets` confirms an active non-overridable ruleset targeting `geekatron/jerry-claude-plugin` with exactly one bypass actor. A direct push by a non-CI credential is rejected (live test, G-prevention).

#### 5.2 GitHub App Installation Token (D3, REQ-041)

**Designed — operational validation pending [G-prevention].**

| Property | Value | Source |
|----------|-------|--------|
| Credential type | GitHub App installation token (PREFERRED) | ADR-PROJ031-003 D3 |
| App installation scope | `geekatron/jerry-claude-plugin` only, `contents: write` | Least privilege (c-201/c-202) |
| Token TTL | 1 hour (GitHub platform fixed expiry; CV-004) | Automatic rotation; no long-lived token at push time |
| Long-lived secret | App private key (stored in source-repo Actions secret, environment-gated) | c-208/CR-03 |
| Ruleset bypass eligibility | The App identity (by App ID) is the sole bypass actor (D2) | Enables CI force-push while blocking all humans |
| Classic PAT | **REJECTED** (broad multi-repo scope; elevation risk CI-05/CR-01) | ADR-PROJ031-003 D3 |

**Token mint sketch (Phase-6 implementation seed):**

```yaml
# In the push job (NOT the attestation job)
- uses: actions/create-github-app-token@{PINNED_SHA}  # Pin per REQ-017
  id: app-token
  with:
    app-id: ${{ vars.COWORK_APP_ID }}
    private-key: ${{ secrets.COWORK_APP_PRIVATE_KEY }}  # Environment-secret (REQ-045)
    repositories: jerry-claude-plugin

- name: Cross-repo force-push (D3)
  env:
    TOKEN: ${{ steps.app-token.outputs.token }}
  run: |
    git push --force \
      "https://x-access-token:${TOKEN}@github.com/geekatron/jerry-claude-plugin.git" \
      "HEAD:refs/heads/main"
```

The token is never written to `$GITHUB_STEP_SUMMARY` or logs (REQ-019).

#### 5.3 Protected Actions Environment (REQ-045)

A GitHub Actions Environment named `skeleton-push` (or equivalent) SHALL be declared on `geekatron/jerry` with:

```yaml
# Environment configuration intent (Phase-6 implementation detail)
environment:
  name: skeleton-push
  deployment_branch_policy:
    protected_branches: false       # "protected" setting is for the branch, not triggers
    custom_branch_policies: true    # Allow only specific patterns
  # Allowed triggers: main branch AND v* tag patterns
```

The App private key (`COWORK_APP_PRIVATE_KEY`) and App ID (`COWORK_APP_ID`) are stored as **environment-level secrets**, not repository-level secrets. A `workflow_dispatch` run initiated from a non-protected branch is rejected before any secret is accessed, bounding the lateral-movement attack surface (RTB-4).

**Verification (Phase-6):** Trigger `workflow_dispatch` from a non-protected feature branch; confirm the environment gate rejects the run before any secret-access step executes (REQ-045 AC b).

#### 5.4 Key Rotation Policy (REQ-048, RTB-4)

The App private key is the project's single long-lived secret. Its custody policy:

| Policy dimension | Requirement |
|------------------|-------------|
| Maximum rotation interval | ≤ 12 months (REQ-048) |
| Personnel-change trigger | Immediate rotation when any principal loses source-repo secrets access |
| Rotation procedure | Documented in `runbooks/org-registration.md` §Key Rotation with next-rotation deadline |
| Key storage | Source-repo `skeleton-push` environment secrets only; never in workflow files, commits, or logs |
| Short-lived token scope | Per-run minted installation token (1 h TTL) means no push-usable secret rests at scale even if the private key is leaked between rotations — theft enables forgery only within the D7 ≤ 6 h detection window |

**Verification (Phase-6):** `runbooks/org-registration.md` contains the rotation procedure and last-rotation date; computed interval ≤ 12 months; immediate-rotation procedure documented (REQ-048 AC a/b/c).

---

### 6. Tag Protection & Provenance Gate (D5)

**Designed — operational validation pending [G-provenance] (FM-032). This is the top residual (SC-02) and a Phase-5 go-live BLOCKER.**

#### 6.1 v* Tag-Protection Ruleset on Source Repo (REQ-039 — push-time leg)

A source-repo (`geekatron/jerry`) ruleset restricting `v*` tag creation:

| Ruleset parameter | Value |
|-------------------|-------|
| Target pattern | `refs/tags/v*` (semver tags) |
| Rules enabled | `creation` (deny to non-bypass actors), `deletion`, `non_fast_forward` |
| `bypass_actors` | Release pipeline CI identity + designated maintainers only |
| Any collaborator | Cannot create a `v*` tag |

This closes the push-time leg of SC-02: an arbitrary collaborator cannot mint a release tag at a malicious commit in the first place.

**Verification (Phase-6):** Attempt by a non-designated collaborator to push a `v*` tag is rejected (REQ-039 AC).

#### 6.2 Tag-on-Main Provenance Assertion (REQ-038 — build-time leg)

This is the build-time complement owned by **eng-devsecops** (placed in `cowork-skeleton.yml` before G3). Reproduced here for completeness:

```bash
# After G2 allow-list validation, BEFORE git rm (G4)
SRC_SHA="$(git rev-parse "${TAG}^{commit}")"
if ! git merge-base --is-ancestor "${SRC_SHA}" origin/main; then
  echo "::error::SC-02 rogue-tag: ${TAG} (${SRC_SHA}) is not an ancestor of main" >&2
  exit 1   # NO artifact, NO attestation, NO push
fi
```

If the provenance assertion fails, the workflow exits non-zero before G3 executes. No attestation is produced for a rogue tag (D4 ordering is preserved).

**Scope boundary:** The provenance gate asserts the tag commit is on `main`; it does NOT assert the content is benign. SC-06 (trusted-maintainer rogue build, content passing the ancestor check) is bounded by D8 + REQ-051, not by D5. See ADR-PROJ031-003 RTB-2.

---

### 7. SBOM: CycloneDX of Python Dependency Surface

**Recommendation: IN — Generate and Attest a CycloneDX SBOM**

#### 7.1 Rationale (In)

| Factor | Assessment |
|--------|------------|
| Actionable dependency surface | The skeleton retains `src/` (Jerry Python package), `pyproject.toml`, and `uv.lock` — the executable runtime hooks are Python code with real transitive dependencies (the `src/` surface executes on every user session start) |
| Existing tooling | The repo already uses `cyclonedx-py` in the release pipeline (fix merged as of `fc522319`) — cost is near-zero to reuse |
| SLSA trajectory | ADR-PROJ031-003 L2 §4 identifies SBOM as the next supply-chain depth layer; including it here advances the SLSA L3→L4 roadmap |
| Skeleton tree neutral | The SBOM is published as a release asset (`sbom-jerry-claude-plugin-${TAG}.cdx.json`), NOT committed into the skeleton tree — no impact on the file-count gate (REQ-006), no drift in deterministic commit SHA |
| Attestation binding | The SBOM is attested via a second `actions/attest` call, binding dependency provenance to the same Rekor entry as the artifact — auditors get a single queryable source for both code and dependency provenance |

**Explicit scope boundary:** The SBOM covers the **Python dependency surface** derived from `pyproject.toml`/`uv.lock` — NOT a file-level inventory of all 1,417 skeleton files (which would be a manifest, not an SBOM). The markdown instructions (skills, commands) are not software components with declared dependencies; they are excluded from the SBOM.

#### 7.2 Generation Step (Phase-6 Implementation Seed)

```bash
# H-05: MUST use uv run for all Python execution
uv run cyclonedx-py environment \
  -o "sbom-jerry-claude-plugin-${TAG}.cdx.json" \
  --output-format JSON \
  --schema-version 1.5
# The environment reflects the pyproject.toml dependencies in the generated skeleton tree
```

#### 7.3 SBOM Attestation Step

```yaml
# In the attestation job, after the build-provenance attestation step
- name: Attest SBOM (D4 extension)
  uses: actions/attest@{PINNED_SHA}
  with:
    subject-path: "jerry-claude-plugin-${TAG}.tar"      # The attested artifact is still the TAR
    sbom-path: "sbom-jerry-claude-plugin-${TAG}.cdx.json"  # Associates SBOM with the artifact
```

**Phase-6 detail:** Confirm whether `actions/attest` v4+ accepts both `subject-path` and `sbom-path` in a single call or requires two separate calls. If two calls, the second call uses `predicate-type: https://cyclonedx.org/bom`.

---

## L2: Strategic Implications

### Supply-Chain Risk Landscape

The skeleton's risk profile is unusual: it is not binary code but natural-language instructions that become live LLM behavior. This creates a **content-as-attack-surface** threat model that differs from conventional supply-chain security:

1. **Integrity controls (D2/D4/D5/D7) are necessary but not sufficient.** They prove the skeleton is faithfully built and delivered, but cannot prove the build input is benign. D8 closes the explicit-pattern gap; the semantic residual remains (RTB-2, inherent to static analysis).

2. **Trust concentrates at two high-leverage points.** The org-admin registration and the App private key replace the previous broad write-collaborator surface. This is a net improvement, but disciplines of org-owner minimization, 2FA/SSO, and rotation (§5) must compensate for the narrowed but elevated trust concentration.

3. **The Rekor log is the durable integrity anchor, not GitHub.** Attestations in the public Sigstore transparency log are non-deletable and GitHub-independent. Even if a GitHub outage or compromise affects release assets, the attestation remains verifiable via `cosign verify-attestation`. This is the strongest independent integrity signal available without a dedicated HSM.

4. **Install-time verification is an open gap (RTB-5).** The D7 monitor is the sole automated verification path; it is post-publication, not at user install. CoWork does not expose a consumer-side attestation hook. If Anthropic adds such a hook in a future CoWork release, this design's `gh attestation verify` invocation is the ready-to-integrate verification form.

### SLSA Maturity Roadmap

| SLSA Level | Status (designed, pending G-x validation) | Gap to close |
|------------|------------------------------------------|--------------|
| **L1** | Designed — documentation of build process exists | G-prevention + G-provenance must pass |
| **L2** | Designed — hosted build platform (GitHub Actions) + signed provenance (Sigstore) | Same gates as L1 |
| **L3** | Designed — hardened build (D6 runner hardening) + non-falsifiable provenance (Rekor log) | Same + G-content, G-monitor |
| **L4** | Not yet designed — requires hermetic builds + two-party review | D6 hermetic builds + REQ-051 two-reviewer; out of Phase-3 scope |

Current honest claim: the architecture is on a **SLSA L3 trajectory**. Stating L3 is achieved requires Phase-5 gate evidence for G-prevention, G-provenance, G-content, and G-monitor.

### Infrastructure Security Evolution Path

1. **Phase-5/6 (immediate):** Validate the five Phase-5 gates. First real attestation produced; G-prevention confirmed; credential provisioned; SBOM pipeline running.

2. **Near-term (post go-live):** Add `--signer-workflow` enforcement to the D7 monitor's verify call (already included in this design). Enable auto-revert (`actions: write`) once `G-actions-write-safe` passes. Track `last-good-validated` tag lifecycle.

3. **Medium-term:** Evaluate hermetic build requirements for SLSA L4 (pinned dependency fetches, sandboxed runner). The current use of `uv sync --frozen` (pyproject.toml lock file) is a partial hermetic control.

4. **Long-term:** If CoWork exposes consumer-side attestation verification, the `gh attestation verify` invocation designed here is the ready integration form. If the org grows to multiple distributable plugins, the GitHub App single-installation-per-repo model scales naturally without credential proliferation.

### Vendor Dependency Risk Assessment

| Dependency | Risk | Mitigation |
|------------|------|------------|
| `actions/attest` (GitHub) | Supply-chain attack on the action itself; action behavior change | SHA-pin per REQ-017; Dependabot for updates |
| Sigstore / Rekor public instance | Instance availability (verification fails); log integrity compromise | Rekor is independently operated; cosign offline verification as fallback |
| GitHub App platform | GitHub outage; App token API change | Deploy key as fallback (ADR-PROJ031-003 D3 alternative); 1 h TTL limits exposure window |
| `cyclonedx-py` (for SBOM) | Upstream vulnerability or output format change | Pin version in `pyproject.toml`; `uv.lock` ensures reproducible installs |
| `gh` CLI (D7 monitor) | CLI API change for `attestation verify`; version mismatch | Pin `gh` version in monitor workflow; test with exact version used |

---

## Traceability Matrix

| # | Design element | Requirements | ADR / Source |
|---|----------------|--------------|--------------|
| INF-01 | Plain TAR artifact (`git archive --format=tar`) | REQ-042 | ADR-PROJ031-003 D4 (R-006); phase3-skeleton-generation-design.md §3, G9 |
| INF-02 | Gzip-mtime trap resolution (`--format=tar` preferred, `gzip -n` for `.tar.gz`) | REQ-003, REQ-042 | phase3-skeleton-generation-design.md §3 "Compression wrapper" |
| INF-03 | Artifact naming: `jerry-claude-plugin-${TAG}.tar` | REQ-008 (source tag embedded) | ADR-PROJ031-001 §Artifact Naming |
| INF-04 | `actions/attest` with `subject-path` (SLSA build provenance) | REQ-042 | ADR-PROJ031-003 D4; SLSA L3 |
| INF-05 | Per-job `permissions:` isolation (attestation vs. push) | REQ-020, REQ-042 | ADR-PROJ031-003 D4 A-1 |
| INF-06 | `gh attestation verify <file> --repo geekatron/jerry --signer-workflow …` | REQ-035, REQ-042, NFR-006 | ADR-PROJ031-003 D4 (CV-005/R-006); D7 |
| INF-07 | D7 monitor (ROOT-1 corrected): download published tar → `gh attestation verify` (Sigstore exit-code only; no SLSA-predicate SHA extraction) → sha256 digest comparison (ATTESTED_DIGEST vs LIVE_DIGEST from shallow-fetch + `git archive`) → freshness | REQ-035, REQ-049, NFR-006 | ADR-PROJ031-003 D7; IN-002; ROOT-1/DA-001 fix (2026-06-30) |
| INF-08 | Immutable GitHub Release with attested `.tar` + SBOM + bundle as assets | REQ-042 | ADR-PROJ031-003 D4 |
| INF-09 | Rekor transparency log anchor (public Sigstore instance for public repo) | REQ-042 | ADR-PROJ031-003 D4; SLSA L3 non-falsifiable provenance |
| INF-10 | Org-level ruleset on `geekatron/jerry-claude-plugin` (CI sole bypass, zero human write) | REQ-040, REQ-021 | ADR-PROJ031-003 D2 |
| INF-11 | GitHub App installation token (1 h TTL, `contents: write` to `jerry-claude-plugin` only) | REQ-041, NFR-004 | ADR-PROJ031-003 D3 (CV-004) |
| INF-12 | Actions Environment `skeleton-push` with `deployment_branch_policy` | REQ-045 | ADR-PROJ031-003 RTB-4/B-1 |
| INF-13 | App private key rotation ≤ 12 months; immediate on personnel change | REQ-048 | ADR-PROJ031-003 RTB-4/B-5; CR-03 |
| INF-14 | `v*` tag-protection ruleset on source repo (creation restricted to CI + maintainers) | REQ-039 | ADR-PROJ031-003 D5; SC-02 |
| INF-15 | CycloneDX SBOM from `pyproject.toml`/`uv.lock` via `cyclonedx-py` | REQ-042 (SLSA trajectory) | ADR-PROJ031-003 L2 §4; SSDF PW.4 |
| INF-16 | SBOM attestation via `actions/attest` (separate attestation call) | REQ-042 | ADR-PROJ031-003 D4; CycloneDX SBOM attestation |
| INF-17 | `--signer-workflow` flag in verify command | REQ-035 (integrity) | ADR-PROJ031-003 D7; defense-in-depth against workflow substitution |

---

## Pending Validation (P-022)

Honest status — nothing below is an achieved fact. Each item defers to a named Phase-5 gate.

| Item | Status | Resolved by |
|------|--------|-------------|
| `git archive --format=tar` produces bit-identical bytes on ubuntu-latest for the same COMMIT_SHA | Designed; must confirm empirically | Phase-6 two-run idempotency test (REQ-003 AC; NFR-001 AC) |
| `actions/attest` v4 permissions: whether `artifact-metadata: write` is required alongside `id-token: write` + `attestations: write` | Designed; current documentation indicates it may be required; pin the exact action version in Phase-6 and confirm | Phase-6 implementation (REQ-020 AC) |
| `gh attestation verify --signer-workflow` flag: confirm the workflow path form for the source repo | Designed; confirm against live CLI version pinned in monitor workflow | Phase-6 implementation (REQ-035 AC, REQ-042 AC b) |
| ~~Exact jq path to extract `gitCommit` from `gh attestation verify --format json` output~~ — **REMOVED (ROOT-1 fix):** the SLSA predicate `gitCommit` field is `SRC_SHA` (jerry source commit), not the generated skeleton commit `G6_SHA`. Comparing this field to the live dedicated-repo tip SHA always fails by design. The jq-parsing step is eliminated; verification binds on the deterministic TAR digest instead | **N/A — verification approach corrected** | Replaced by shallow-fetch validation below |
| Shallow-fetch approach for live-tip TAR derivation: confirm `git fetch --depth=1` + `git archive --format=tar ${G6_SHA}` on `ubuntu-latest` produces byte-identical output to the original CI `git archive` step for the same commit SHA; no unexpected mtime injection from pinned `git` version | Designed; confirm during Phase-6 implementation | Phase-6 two-run idempotency test (REQ-003 AC, NFR-001 AC; D7 monitor, NFR-006 AC) |
| `actions/attest` accepting both `subject-path` + `sbom-path` in single call vs. two calls | Designed; confirm against pinned version | Phase-6 SBOM implementation |
| Org-level ruleset bypass-actor semantics proven on live `geekatron/jerry-claude-plugin` | Designed — operational validation pending [**G-prevention**] | Phase-5 live ruleset test (REQ-040 AC; ADR-PROJ031-003 D2) |
| `v*` tag-protection ruleset rejecting non-CI tag creation on source repo | Designed — operational validation pending [**G-provenance**] | Phase-5 live tag push test (REQ-039 AC; ADR-PROJ031-003 D5) |
| D7 monitor: synthetic-tamper fires issue + non-zero exit; freshness failure fires correctly | Designed — operational validation pending [**G-monitor**] | Phase-5 synthetic test (REQ-035 AC b/c/f/g; NFR-006 AC) |
| SBOM CycloneDX schema version (1.5 specified; confirm cyclonedx-py version supports it) | Designed; pin exact cyclonedx-py version in `pyproject.toml` | Phase-6 implementation |

---

## References

| # | Source | Relevance |
|---|--------|-----------|
| 1 | `phase3-skeleton-generation-design.md` | G9 deterministic artifact algorithm; §3 determinism contract; gzip-mtime trap ("Compression wrapper" row); G6 committer-date pinning |
| 2 | `../decisions/ADR-PROJ031-003-credential-protection-supply-chain.md` | D2 (ruleset), D3 (App token), D4 (attestation, R-006/CV-005), D5 (provenance + tag protection), D6 (runner hardening), D7 (monitor topology + freshness), RTB-1..5 |
| 3 | `../requirements/phase1-requirements.md` | REQ-038/039 (provenance/tag protection), REQ-040 (ruleset), REQ-041 (App token), REQ-042 (attestation), REQ-045 (Environment), REQ-048 (key rotation), REQ-049 (freshness), REQ-035/NFR-006 (monitor) |
| 4 | GitHub CLI manual: `gh attestation verify` | Confirms file-path subject form; `--signer-workflow` flag; exit-code semantics (https://cli.github.com/manual/gh_attestation_verify) |
| 5 | `actions/attest` GitHub repository | Current action (supersedes `actions/attest-build-provenance` as of v4); `subject-path`, `sbom-path`, and permission requirements (https://github.com/actions/attest) |
| 6 | RFC 1952 (GZIP file format) | Defines MTIME (bytes 4–7) and OS byte (byte 9) that cause non-determinism |
| 7 | Sigstore / Rekor public instance | Immutable public transparency log; `cosign verify-attestation` for GitHub-independent verification |

---

*Generated by jerry:eng-infra (Secure Infrastructure Engineer). S-010 Self-Refine applied (H-15). Settled ADR decisions consumed, not re-opened (P-020). No sub-agents spawned (P-003). Designed-but-unvalidated controls tagged per Claim-Status Convention (P-022). H-05 (uv run) applied to all Python execution sketches.*
