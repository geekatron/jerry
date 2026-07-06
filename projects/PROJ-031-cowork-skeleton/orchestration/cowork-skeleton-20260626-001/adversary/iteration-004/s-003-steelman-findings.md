# S-003 Steelman Report: PROJ-031 CoWork Skeleton — Dedicated-Repo + Prevention + Attestation Design

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, deliverables under review |
| [Steelman Statement](#steelman-statement) | Strongest form of the design's core argument |
| [Findings Summary](#findings-summary) | All SM findings by severity |
| [Detailed Findings](#detailed-findings) | Evidence, under-stated argument, recommendation per finding |
| [Scoring Impact](#scoring-impact) | Dimension-level quality assessment |
| [Execution Statistics](#execution-statistics) | Counts and protocol coverage |

---

## Execution Context

- **Strategy:** S-003 (Steelman Technique)
- **Strategy ID:** S-003
- **Finding Prefix:** SM-NNN-it004
- **Template:** `.context/templates/adversarial/s-003-steelman.md`
- **Executed:** 2026-06-29
- **Iteration:** iteration-004 (RE-ADVERSARY gate, post Phase-2)
- **Criticality:** C4 (quality target >= 0.95)
- **Blindness:** No adversary/ directory content read; independent assessment from deliverables + template only

**Deliverables Under Review:**

| Deliverable | Role |
|-------------|------|
| `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` (amended: dedicated-repo model + `tests/` strip) | Primary — generation strategy |
| `projects/PROJ-031-cowork-skeleton/decisions/ADR-003-credential-protection-supply-chain.md` (new — credential, repo protection, attestation) | Primary — security posture |
| `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` (updated: REQ-038–044; REQ-035/NFR-006 demoted) | Primary — requirements specification |
| `projects/PROJ-031-cowork-skeleton/security/phase2-stride-threat-model.md` + `security/phase2-attack-surface.md` | Supporting evidence — NOT under review |
| `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` | Superseded — historical context only |

---

## Steelman Statement

The strongest form of this design:

The PROJ-031 dedicated-repo, prevention-first, attestation-anchored architecture is the *architecturally correct* response to distributing an executable plugin to an entire organization's user base. Its central insight — that for hook-executing artifacts, any detection window is a **guaranteed-harm interval, not a recovery interval** — makes prevention-by-default the only proportionate primary control. The dedicated-repo model unlocks this prevention at near-zero incremental cost: since a cross-repo push credential is mandatory for any inter-repo distribution, naming that same credential as the dedicated-repo ruleset's sole bypass actor costs exactly one configuration step.

The architecture achieves something structurally rare: **three independent, mutually corroborating integrity verification paths**:

1. **Deterministic SHA** (ADR-001) — any party can recompute the expected tip SHA from the source tag alone using only git, with no trust required in GitHub infrastructure or Sigstore.
2. **Sigstore-backed build-provenance attestation** (ADR-003 D4) — CI-only-writable, publicly verifiable via `gh attestation verify`, independently proving that a specific GitHub Actions workflow built the artifact from a specific source commit. The attestation proves *who*; the deterministic SHA proves *what*; together they are mutually corroborating proofs that defeat different attack vectors.
3. **Backstop integrity monitor** (NFR-006) — periodically asserts the live branch tip SHA matches the attested SHA, covering the residual paths (credential theft, admin suppression) that prevention cannot block.

No single-point failure defeats all three. Together they close the detection window that asynchronous monitoring inherently leaves open.

The supply-chain trust chain is end-to-end and every link is independently protected: `main` (branch-protected) → `v*` tag (tag-protected + ancestor-of-main provenance assertion) → CI build (attested + faithful-derivative gate + secret-scanned) → dedicated-repo default branch (CI sole bypass, zero human write) → org users (server-side marketplace, admin-gated registration). Defeating this chain requires simultaneously compromising multiple independent control systems.

Furthermore, the ADR-003 architecture makes the ADR-001 clone-weight decision **purely an engineering trade-off**: the attestation now provides provenance independently of the parent chain, making the orphan-branch fallback (Option B) fully equivalent to Option A in all three security-relevant dimensions — integrity, provenance, and supply-chain assurance. The clone-weight choice is therefore a pure bandwidth-vs.-convenience optimization with zero security dimension.

---

## Findings Summary

| ID | Severity | Finding | Target Deliverable |
|----|----------|---------|-------------------|
| [SM-002-it004](#sm-002-it004-detection-window--guaranteed-harm-interval-argument-absent) | Critical | Detection-window = guaranteed-harm interval argument absent; prevention called "disproportionate" without causal proof | ADR-003 §L2 Architectural Implications #3 |
| [SM-003-it004](#sm-003-it004-three-path-integrity-architecture-not-articulated-as-unified-thesis) | Critical | Three-path integrity architecture (SHA + attestation + monitor) never stated as unified architectural thesis | ADR-003 D4 + ADR-001 §Tamper-Evidence |
| [SM-006-it004](#sm-006-it004-orphan-flip-is-now-fully-neutral-synthesis-incomplete) | Critical | "Orphan flip is now fully neutral" synthesis across integrity AND provenance is incomplete; clone-weight is still framed as a partial security trade-off | ADR-001 §Clone-Weight Decision + ADR-003 Neutral #3 |
| [SM-001-it004](#sm-001-it004-prevention-is-nearly-free-argument-under-developed) | Major | "Prevention is nearly free" argument stated once without developing the architectural logic that makes it compelling | ADR-003 §Forces + D2 |
| [SM-004-it004](#sm-004-it004-attestation--deterministic-sha-dual-proof-synthesis-under-stated) | Major | Attestation + deterministic SHA combination defeats different attack vectors; the mutual complementarity is not stated as a positive claim | ADR-003 D4 |
| [SM-005-it004](#sm-005-it004-topological-loop-safety-is-structurally-stronger-than-the-guarantee-it-replaces) | Major | Topological loop-safety is framed as a cost (Negative #5); it is structurally more robust than the `GITHUB_TOKEN` platform-policy guarantee it replaces | ADR-003 Consequences Negative #5 + REQ-014 |
| [SM-009-it004](#sm-009-it004-tag-protection--provenance-assertion-double-compromise-argument-under-stated) | Major | Tag protection + provenance assertion require double-compromise to defeat; this mutual failure-mode argument is not stated | ADR-003 D5, REQ-038–039 |
| [SM-007-it004](#sm-007-it004-tests-strip-positive-quality-argument-under-stated) | Minor | `tests/` strip justified only by file-count margin; the positive quality argument (tests are actively harmful in a plugin distribution) is absent | ADR-001 §Canonical Plugin-Retention Surface + REQ-002 |
| [SM-008-it004](#sm-008-it004-adr-001-body-prose-inconsistency-should-be-tracked-as-a-blocker) | Minor | ADR-001 body prose still says `tests/` is "retained today"; this known inconsistency is noted-and-deferred in REQ-005 but should be a tracked blocker | requirements REQ-005 note |
| [SM-010-it004](#sm-010-it004-sigstore-user-facing-verifiability-concrete-claim-absent) | Minor | Attestation is described as "publicly verifiable" and "SLSA Level 3 trajectory" but the concrete user command (`gh attestation verify`) is never stated | ADR-003 D4, §L2 #4 |
| [SM-011-it004](#sm-011-it004-write-collaborator-surface-grows-org-admin-surface-is-bounded-argument-under-stated) | Minor | Write-collaborator surface grows over time; org-admin trust surface is bounded; this asymmetry makes the new model progressively better as the project scales | ADR-003 §L2 #1 |

---

## Detailed Findings

### SM-002-it004: Detection-Window = Guaranteed-Harm Interval Argument Absent

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Target** | ADR-003 §L2: Architectural Implications #3 |
| **Strategy Step** | Step 2 (Weakness: Structural — load-bearing claim asserted without causal proof) |

**Evidence — Current Text:**

ADR-003 L2 #3 states: "Executable hooks justify prevention-by-default. The artifact is code that runs on every user's session start, and one org registration reaches every user at once. That amplification is why detection-only (ADR-002) is no longer proportionate."

**Under-Stated Argument:**

The word "proportionate" implies detection-only is merely undersized, when the architectural argument is stronger: detection-only is *inadequate in principle* for hook-executing artifacts. The causal chain:

1. Hooks execute at session start without any user-initiated action.
2. A single org marketplace registration delivers to every member silently.
3. Any detection window — even one cycle of a daily monitor (up to 24 hours) — is a period during which *some* user's session start will execute the malicious hooks.
4. Detection + auto-revert can restore the branch. It **cannot un-execute hooks that have already run** on a user's workstation.
5. Therefore, for an auto-executing artifact, any non-zero detection window creates a guaranteed-harm interval proportional to session-start frequency across the org.

This makes prevention the only control that reduces the harm interval to zero — not a "more proportionate" choice, but the only logically sound one. Without this proof, ADR-003's prevention decision reads as a preference rather than a logical necessity, leaving the design vulnerable to an S-002 attack arguing "detection with auto-revert would have been sufficient."

**Recommendation:**

Add to ADR-003 L2 #3: "Detection-only is inadequate *in principle* (not merely disproportionate) because hooks execute at session start without user action. Any detection window — even minutes — is a **guaranteed-harm interval**: users whose sessions start during that window have already run malicious hooks before detection fires and auto-revert completes. Prevention reduces this interval to zero. No detection-and-revert architecture can achieve this for an auto-executing artifact."

---

### SM-003-it004: Three-Path Integrity Architecture Not Articulated as Unified Thesis

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Target** | ADR-003 D4 + ADR-001 §Tamper-Evidence and Supply-Chain Integrity |
| **Strategy Step** | Step 3 (Reconstruction: Supply missing architectural thesis) |

**Evidence — Current Text:**

The deliverables present the deterministic SHA (ADR-001 §Tamper-Evidence), the build-provenance attestation (ADR-003 D4), and the backstop monitor (ADR-003 D4 last paragraph; NFR-006) as separate mechanisms. No section states their *independence* or *mutual corroboration* as a unified architectural property.

**Under-Stated Argument:**

The design achieves three independent, mutually corroborating integrity verification paths:

1. **Deterministic SHA** — Any party who has read access to the source repo can recompute the expected tip SHA by running the documented generator against the same tag. This requires no trust in GitHub, no access to Sigstore, and no network connectivity beyond cloning the source repo. Verification is pure local computation against a mathematical invariant.

2. **Sigstore-backed build-provenance attestation** — A transparency-log-backed cryptographic proof that a specific GitHub Actions workflow produced the artifact from a specific source commit at a specific time. Verification requires access to the Sigstore transparency log (`gh attestation verify`), independent of the git hash computation in path 1.

3. **Backstop monitor** — Independently verifies the live branch tip SHA against the attestation on a scheduled cadence, covering the residual paths that prevention cannot block (credential theft, admin suppression). Verification is independent of both the git hash computation and the Sigstore log.

**Independence properties:** No single-point failure defeats all three. A SHA-1/SHA-256 preimage attack defeats path 1 but not paths 2 or 3. Suppressing the Sigstore log defeats path 2 but not paths 1 or 3. Silencing the monitor defeats path 3 but not paths 1 or 2. An attacker who wants to evade all three must simultaneously defeat the git hashing function, the Sigstore transparency log, and the scheduled monitor — a compound attack requiring no feasible single vector.

This triple-redundancy is the design's strongest integrity claim and is never stated.

**Recommendation:**

Add to ADR-003 D4 or L2: "The architecture achieves three independent integrity verification paths, each with distinct trust assumptions and verification mechanisms: (1) deterministic SHA recomputation (git only; no platform trust required), (2) Sigstore-backed build-provenance attestation (cryptographic proof of CI origin; independent of git hash), (3) scheduled backstop monitor (ongoing live-branch verification). No single control failure defeats all three. Together they provide defense-in-depth that goes beyond any single-mechanism integrity approach."

---

### SM-006-it004: "Orphan Flip is Now Fully Neutral" Synthesis Incomplete

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Target** | ADR-001 §Clone-Weight Decision + ADR-003 Consequences Neutral #3 |
| **Strategy Step** | Step 3 (Reconstruction: Strengthen logical connections between ADR-001 and ADR-003) |

**Evidence — Current Text:**

ADR-001 §Clone-Weight Decision states: "post-IT3-004 the flip is **integrity-neutral** (tamper-evidence does not depend on the parent chain)."

ADR-003 Consequences Neutral #3 states: "The dedicated repo's parent-chain provenance is further demoted: with the attestation carrying provenance (D4), the orphan-branch fallback (ADR-001 Option B) is now both integrity-neutral *and* provenance-neutral."

**Under-Stated Argument:**

Neither document draws the full architectural synthesis, which is the most important implication of ADR-003 for the ADR-001 clone-weight decision. Under the ADR-003 architecture:

- **Integrity-neutral** (ADR-001 IT3-004): The deterministic SHA is the integrity anchor; the parent chain is defense-in-depth only. Option B (orphan) has the same integrity guarantee as Option A.
- **Provenance-neutral** (ADR-003 D4): The build-provenance attestation proves that CI built the skeleton from a specific source commit, bound to the CI run and repo. This proof is attached to the attestation record, not to the git parent chain. Option B has the same provenance proof as Option A.
- **Supply-chain-neutral** (ADR-003 D5): The tag-on-main provenance assertion (`git merge-base --is-ancestor`) runs before generation, binding the skeleton to reviewed main history regardless of whether the committed tree carries a parent chain.

**Full synthesis:** Under ADR-003, the orphan branch (Option B) is *fully equivalent* to Option A in all three security-relevant dimensions: integrity, provenance, and supply-chain assurance. The clone-weight decision is therefore a **pure engineering optimization** — full history (Option A) for `git diff main..cowork-skeleton` convenience vs. orphan (Option B) for constant O(1) clone weight — with **zero security dimension**.

Without this synthesis, the clone-weight decision in ADR-001 still reads as having a partial security trade-off ("provenance vs. clone weight"), which is no longer accurate. This framing leaves the design vulnerable to critique that challenges the clone-weight monitoring approach as insufficient when the simpler Option B would eliminate the concern entirely.

**Recommendation:**

Add to ADR-001 §Clone-Weight Decision (after the Option B flip description): "Under the ADR-003 architecture (D4 attestation + D5 provenance assertion), Option B (orphan) is now **fully equivalent** to Option A in all security-relevant dimensions: the attestation carries provenance independently; the tag-on-main assertion carries supply-chain binding independently; the deterministic SHA carries integrity independently. The clone-weight decision is a pure engineering optimization. No security argument favors either option."

Also update ADR-003 Neutral #3 to state the synthesis explicitly rather than only noting "integrity-neutral and provenance-neutral."

---

### SM-001-it004: "Prevention is Nearly Free" Argument Under-Developed

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Target** | ADR-003 §Forces #1 + D2 |
| **Strategy Step** | Step 2 (Weakness: Structural — correct insight stated but not developed) |

**Evidence — Current Text:**

ADR-003 §Forces #1: "Locking the dedicated repo gives prevention; it costs a privileged cross-repo identity. But the cross-repo push *already* needs that identity — so prevention is nearly free."

**Under-Stated Argument:**

This is the correct insight but it needs the full architectural logic to be persuasive:

1. D1 (dedicated repo) is required independently of security — it is the confirmed CoWork org-registration distribution mechanism.
2. D3 (cross-repo credential) follows necessarily from D1 — any push to a repo outside the source repo requires a credential with cross-repo write access. This cost is paid regardless of the protection posture chosen.
3. D2 (prevention via org-level ruleset) then costs exactly one additional configuration step: naming the D3 credential as the ruleset's sole bypass actor.
4. **The old model's detection-only posture was not a neutral baseline** from which prevention is an upgrade. It was an *architectural artifact* of distributing the artifact inside the source repo, where branch protection would block CI's own push via `GITHUB_TOKEN`. The dedicated-repo model eliminates this constraint entirely.

Prevention is therefore not "a security upgrade at some cost" — it is the *naturally available state* for any dedicated-repo distribution that already has a cross-repo credential. Framing it as "nearly free" understates this: it is the default-correct posture, and *not* having it would require a deliberate decision to leave protection off.

**Recommendation:**

Expand ADR-003 D2 rationale or §Forces #1: "Prevention is not an upgrade from detection — it is the naturally available default for a dedicated-repo model. D1 (dedicated repo) is required by CoWork's org-registration mechanism. D3 (cross-repo credential) is required by D1. D2 then costs one configuration step: naming the D3 credential as the ruleset bypass actor. The detection-only posture of ADR-002 was an artifact of distributing inside the source repo, where `GITHUB_TOKEN` cannot be simultaneously the pusher and the bypass actor. The dedicated-repo model removes that constraint: prevention becomes the default at no additional credential cost."

---

### SM-004-it004: Attestation + Deterministic SHA Dual-Proof Synthesis Under-Stated

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Target** | ADR-003 D4 (Integrity Anchor) + ADR-001 §Tamper-Evidence |
| **Strategy Step** | Step 3 (Reconstruction: Supply missing synthesis) |

**Evidence — Current Text:**

ADR-003 Options Considered Dimension 4 (rejecting GPG-signed commits): "proves *who* committed, but the deterministic SHA proves *exactly what* the tree-and-parent must be for a given release." This correctly identifies the distinction between the two mechanisms but only in the context of *rejecting* a third option. The positive synthesis — what the attestation + SHA *together* achieve — is not stated.

**Under-Stated Argument:**

The deterministic SHA and the build-provenance attestation are complementary proofs that defeat *different* attack vectors:

- **Deterministic SHA alone**: Proves *what* (the content is exactly what an honest build from that tag would produce), but cannot prove *who* produced it — any party with source repo read access can recompute the expected SHA, but this does not prove CI ran the build.
- **Attestation alone**: Proves *who* (a specific GitHub Actions workflow produced this artifact from a specific source commit), but trusts CI to have built faithfully — a compromised CI workflow can produce a valid attestation for a malicious tree.
- **Together**: A compromised CI workflow that builds a malicious tree cannot change the independently-recomputable expected SHA (git hash preimage resistance), so the SHA check catches it. A stolen push credential that pushes a wrong-SHA artifact cannot produce a matching attestation (only the CI workflow that ran the build holds the signing key), so the attestation check catches it. Each proof closes the attack vector the other cannot see.

**Recommendation:**

Add to ADR-003 D4: "The deterministic SHA (ADR-001) and the build-provenance attestation are mutually complementary proofs. The SHA proves *what* (content invariant; verifiable without trusting CI). The attestation proves *who* (CI origin; cryptographically signed). A compromised CI cannot alter the independently-recomputable expected SHA. A stolen push credential cannot produce a matching attestation. Together they close both attack vectors that neither alone addresses."

---

### SM-005-it004: Topological Loop-Safety is Structurally Stronger Than the Guarantee it Replaces

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Target** | ADR-003 Consequences Negative #5 + REQ-014 |
| **Strategy Step** | Step 2 (Weakness: Presentation — correct finding framed as a cost when it is a net improvement) |

**Evidence — Current Text:**

ADR-003 Consequences Negative #5: "Loop-safety is no longer free. The `GITHUB_TOKEN` non-retrigger guarantee is gone; loop-safety now rests on topology (CR-02). *Mitigation:* dedicated repo has no push-back workflows; assert in config and review."

**Under-Stated Argument:**

The `GITHUB_TOKEN` non-retrigger guarantee is a **GitHub platform policy** that:
- Has changed historically as GitHub has updated Actions semantics.
- Can change again without deprecation notice.
- Is not documented as a permanent guarantee.
- Applies only as long as `GITHUB_TOKEN` is the push credential — which the dedicated-repo model already overrides.

Topological loop-safety, by contrast, is a **structural architectural property**:
- It holds regardless of GitHub platform policy choices.
- It holds regardless of credential type (App token, deploy key, PAT).
- It is verifiable by inspection of the dedicated repo's workflow directory.
- It is immune to future GitHub Actions policy changes.

Therefore, re-deriving loop-safety topologically is a *net architectural improvement* over the `GITHUB_TOKEN` non-retrigger guarantee, not a cost. The deliverable correctly identifies the mitigation (no push-back workflows) but frames it as a loss that needs mitigation rather than as a gain that exceeds what was lost.

**Recommendation:**

Move ADR-003 Consequence #5 from Negative to Positive or Neutral: "Loop-safety is re-derived topologically (CR-02). Topological loop-safety — the dedicated repo has no push-back workflows; the source triggers on tags + dispatch only — is structurally more robust than the `GITHUB_TOKEN` non-retrigger guarantee it supersedes: the latter is a platform policy that can change; the former is an architectural property independent of platform behavior. This is a net improvement, not a cost."

---

### SM-009-it004: Tag Protection + Provenance Assertion Double-Compromise Argument Under-Stated

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Target** | ADR-003 D5 + REQ-038–039 |
| **Strategy Step** | Step 3 (Reconstruction: Strengthen logical argument structure) |

**Evidence — Current Text:**

ADR-003 D5 states: "We will add (a) a tag-on-`main` provenance assertion in the generation workflow and (b) a `v*` tag-protection ruleset on the source repo." The two controls are presented as complementary without developing the mutual failure-mode analysis that demonstrates why both are necessary and why together they require a double-compromise.

**Under-Stated Argument:**

The strongest form of why both controls are needed and why their combination is powerful:

- **Tag protection alone fails** when a sufficiently privileged principal (a named maintainer with tag-creation rights) is compromised — they can create a `v*` tag pointing at an arbitrary commit.
- **Provenance assertion alone fails** when an attacker has *both* (a) tag-creation rights AND (b) has already merged malicious code onto `main` — a high-effort path that requires evading `main`'s branch protection ("Don't fuck with main" org ruleset) and code review.

**Together:**
- Tag protection closes the surface for all non-maintainer actors entirely.
- Provenance assertion closes the surface for a compromised maintainer who targets a non-main commit.
- To defeat *both simultaneously*, an attacker must: (1) compromise a maintainer's credentials AND (2) bypass `main`'s branch protection (the source repo's org-level "Don't fuck with main" ruleset) to land malicious code on `main`.

This combination requires defeating two independent protection systems simultaneously — tag protection and `main` branch protection — in addition to the maintainer compromise. No single-vector attack defeats both. The probability of the compound attack is far lower than either control alone.

**Recommendation:**

Add to ADR-003 D5: "The two controls are mutually compensating with distinct failure modes: tag protection blocks the non-maintainer vector entirely; provenance assertion blocks a compromised maintainer from targeting a non-main commit. Defeating both simultaneously requires a maintainer compromise PLUS bypassing `main`'s independent branch protection — a double-compromise against two independent control systems. No single-vector attack defeats both. This is the strongest available defense against SC-02 given the current threat model."

---

### SM-007-it004: `tests/` Strip Positive Quality Argument Under-Stated

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Target** | ADR-001 §Canonical Plugin-Retention Surface (footnote) + REQ-002 |
| **Strategy Step** | Step 2 (Weakness: Evidence gap — no positive justification for the `tests/` strip decision) |

**Evidence — Current Text:**

REQ-002 rationale: "`tests/` provides additional margin reduction." ADR-001 §Canonical Plugin-Retention Surface: "`tests/` [is] not load-bearing for plugin function and MAY be stripped later if the file-count margin tightens (R-002)."

**Under-Stated Argument:**

Stripping `tests/` is not merely a file-count accommodation — it is an active improvement to the distribution artifact's quality. Distributing `tests/` to plugin users is harmful:

1. `pytest` and dev dependencies (`pytest-asyncio`, fixture libraries, mock frameworks) are not in the production `pyproject.toml` `[project.dependencies]`; any user who runs `uv run pytest` on a CoWork install will encounter `ModuleNotFoundError` for dev imports.
2. Test import paths assume a development checkout structure (e.g., imports relative to the repo root with `src/` on the path in development mode).
3. Test fixtures and test data are meaningless outside a development context.
4. The presence of a `tests/` directory creates a false expectation that the plugin installation can be tested, leading to user confusion and support burden.

Stripping `tests/` is therefore not just acceptable — it is a positive quality decision that improves the plugin user experience and reduces confusion.

**Recommendation:**

Add to REQ-002 rationale and ADR-001: "Distributing `tests/` to plugin users is actively harmful to user experience: test imports depend on dev dependencies absent from the production requirements, and import paths assume a development checkout structure. A CoWork user who discovers `tests/` and attempts to run pytest will encounter import failures. Stripping is a positive quality improvement, not only a file-count accommodation."

---

### SM-008-it004: ADR-001 Body Prose Inconsistency Should Be Tracked as a Blocker

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Target** | `phase1-requirements.md` REQ-005 "Note for ps-architect" |
| **Strategy Step** | Step 2 (Weakness: Structural — known inconsistency deferred without a blocking mechanism) |

**Evidence — Current Text:**

REQ-005 Note: "ADR-001's body (§Canonical Plugin-Retention Surface) says `tests/` is 'retained today (1,744 ≪ 5,000)' but the ADR-001 amendment header (2026-06-28) and ADR-003 both strip `tests/`. This prose inconsistency in ADR-001's body should be corrected. Do NOT edit ADR-001; flagging for ps-architect."

**Under-Stated Argument:**

The inconsistency is correctly identified. However, the note defers the fix to ps-architect discovery without creating a tracked blocking item. At the RE-ADVERSARY gate, this remains an open known inconsistency in the deliverable set. An adversarial reviewer (S-002) could correctly cite this as a traceability gap: REQ-005 says it defers to ADR-001 c-003 as the SSOT, but ADR-001's body prose (§Canonical Plugin-Retention Surface last paragraph) contradicts the amendment header. The note's status — "flagging for ps-architect; Do NOT edit" — means the inconsistency is unresolved at the time the RE-ADVERSARY tournament runs.

The fix path is clear and narrow: update the last paragraph of ADR-001 §Canonical Plugin-Retention Surface from "retained today (1,744 ≪ 5,000)" to say `tests/` is stripped per the Phase-2 amendment. This is a one-sentence prose update, not a decision change.

**Recommendation:**

Upgrade the REQ-005 note from "flagging for ps-architect" to a tracked item (worktracker task or GitHub issue) that must be resolved before AG-04. The inconsistency is minor in substance but creates a verifiable traceability gap that will be raised in adversarial review.

---

### SM-010-it004: Sigstore User-Facing Verifiability Concrete Claim Absent

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Target** | ADR-003 D4 + §L2 Architectural Implications #4 |
| **Strategy Step** | Step 2 (Weakness: Evidence gap — abstract benefit without concrete verification path) |

**Evidence — Current Text:**

ADR-003 D4: "a GitHub immutable release plus a build-provenance attestation (Sigstore-backed, immutable public transparency log; SLSA-aligned) produced by CI on the SOURCE repo." L2 #4: "puts the project on an SLSA Level 3 trajectory and makes the skeleton's lineage cryptographically verifiable end-to-end."

**Under-Stated Argument:**

"Publicly verifiable" and "SLSA Level 3 trajectory" are abstract claims. The concrete user-facing statement is:

Any user who has installed the plugin can run `gh attestation verify <artifact-SHA> --owner geekatron` to confirm that: (a) the artifact was produced by the `geekatron/jerry` GitHub Actions workflow (`cowork-skeleton.yml`), (b) from a specific source commit SHA on a specific date, (c) at a specific workflow run URL that can be independently inspected. This is an independently verifiable, CI-only-signed trust claim that most open-source plugins — including popular ones — cannot make. It goes beyond a checksum: a checksum proves what you received; an attestation proves who built it and where.

**Recommendation:**

Add to ADR-003 D4: "Concretely: any user can verify the installed artifact via `gh attestation verify <skeleton-tip-SHA> --owner geekatron`, confirming it was produced by the `cowork-skeleton.yml` workflow from a specific source commit. This is a CI-only-writable trust claim that goes beyond checksum verification: a checksum proves content; the attestation proves provenance."

---

### SM-011-it004: "Write-Collaborator Surface Grows; Org-Admin Surface is Bounded" Argument Under-Stated

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Target** | ADR-003 §L2 Architectural Implications #1 |
| **Strategy Step** | Step 2 (Weakness: Incomplete framing of the trust model comparison over time) |

**Evidence — Current Text:**

ADR-003 L2 #1: "The model converts a broad write-collaborator exposure into two high-leverage, admin-gated points: the **org-admin registration** (one action authoritative for every user) and the **cross-repo credential** (one key that writes what everyone runs)."

**Under-Stated Argument:**

The old model's write-collaborator surface is not just "broad" — it is *growing*. Every new contributor added to `geekatron/jerry` expands the write-access surface. Every contributor who leaves may retain stale access if offboarding is incomplete. Over time, managing this surface becomes increasingly complex.

The new model's trust surface — the set of org admins authorized to perform marketplace registration plus the App private key custodian — is **bounded and independent of contributor count**. It will not grow as the project adds contributors or shrinks imperfectly as contributors leave. For a growing open-source project, this asymmetry is significant: the new model's relative security posture improves as the project scales, while the old model's degrades.

**Recommendation:**

Add to ADR-003 L2 #1: "This trade is structurally favorable over time: the write-collaborator surface grows with each new contributor and contracts incompletely when contributors depart; the org-admin + credential surface is bounded and contributor-count-independent. For a growing project, the new model's posture improves relative to the old model as the project scales."

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-002 adds the missing causal proof for prevention necessity (a load-bearing claim); SM-003 adds the unified three-path integrity thesis; SM-006 completes the ADR-001 ↔ ADR-003 cross-document synthesis |
| Internal Consistency | 0.20 | Positive | SM-006 resolves the implicit framing inconsistency in the clone-weight decision (still appears to have a security dimension when it does not); SM-008 closes a known prose inconsistency between ADR-001 body and its amendment |
| Methodological Rigor | 0.20 | Positive | SM-002 completes the deductive argument for prevention-first (inductive claim upgraded to deductive proof); SM-009 completes the dual-control failure-mode analysis consistent with defense-in-depth methodology |
| Evidence Quality | 0.15 | Positive | SM-004 supplies the mutual-complementarity synthesis for the attestation + SHA combination; SM-010 provides the concrete verification command that makes the "publicly verifiable" claim falsifiable |
| Actionability | 0.15 | Positive | All 11 findings provide specific textual additions to named sections; the original authors can incorporate directly without structural redesign |
| Traceability | 0.10 | Positive | SM-008 flags a tracked-inconsistency gap before the AG-04 gate; SM-006 completes the ADR-001 ↔ ADR-003 cross-document trace |

---

## Execution Statistics

- **Total Findings:** 11
- **Critical:** 3 (SM-002-it004, SM-003-it004, SM-006-it004)
- **Major:** 4 (SM-001-it004, SM-004-it004, SM-005-it004, SM-009-it004)
- **Minor:** 4 (SM-007-it004, SM-008-it004, SM-010-it004, SM-011-it004)
- **Protocol Steps Completed:** 6 of 6
- **Deliverables Reviewed:** 3 (ADR-001 amended, ADR-003, phase1-requirements.md)
- **Substantive weaknesses found:** 0 — all findings are presentation, structural, or evidence gaps; the core design decisions are sound
- **Blindness maintained:** Yes — no content under `adversary/` directory read; assessment formed independently from deliverables and template

---

*Strategy: S-003 (Steelman Technique)*
*Template: `.context/templates/adversarial/s-003-steelman.md` v1.0.0*
*SSOT: `.context/rules/quality-enforcement.md`*
*Executed: 2026-06-29*
*Agent: jerry:adv-executor*
