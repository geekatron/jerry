# Quality Score Report: CG-007 Docker Image Pinning — Iteration 3

## L0 Executive Summary
**Score:** 0.845/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Methodological Rigor (0.82)
**One-line assessment:** The MC-08 header contradiction is fully resolved — a genuine +0.071 improvement — but the SHA digest gap in CG-007 (version tag only, not digest) keeps Completeness and Methodological Rigor from reaching threshold; reaching PASS requires actual SHA digest pinning or a formally accepted deviation.

## Scoring Context
- **Deliverable:** `.github/workflows/prompt-regression-smoke.yml`, `.github/workflows/prompt-regression-standard.yml`, `.github/workflows/prompt-regression-full.yml`
- **Deliverable Type:** Code (CI/CD workflow configuration)
- **Criticality Level:** C2 (supply chain security control across 3 workflow files)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.774 (iteration 2) | 0.695 (iteration 1)
- **Scored:** 2026-03-07T00:00:00Z
- **Iteration:** 3

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.845 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Delta from Prior Score** | +0.071 (0.774 → 0.845) |
| **Strategy Findings Incorporated** | No (direct deliverable review) |

---

## FIX-WI2-D Verification

The iteration 2 review (adv-wi2d-cg007-rescore.md) identified a single blocking fix: correct the MC-08 header comment in all 3 files from the false claim "Docker image pinned to digest (not :latest tag)" to accurately state version-tag pinning with digest pending.

**Verification result — APPLIED CORRECTLY in all 3 files:**

| File | Line | New MC-08 Header Text |
|------|------|----------------------|
| prompt-regression-smoke.yml | 23 | `MC-08: Docker image pinned to version tag 0.86.0 (not :latest); SHA digest pending Docker daemon availability — see CG-007 inline` |
| prompt-regression-standard.yml | 35 | `MC-08: Docker image pinned to version tag 0.86.0 (not :latest); SHA digest pending Docker daemon availability — see CG-007 inline` |
| prompt-regression-full.yml | 38 | `MC-08: Docker image pinned to version tag 0.86.0 (not :latest); SHA digest pending Docker daemon availability — see CG-007 inline` |

The fix is consistent, accurate, and applied uniformly. The contradiction that drove the iteration 2 Internal Consistency score (0.72) is eliminated.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.83 | 0.166 | Version pin consistent across all 3 files; MC-08 no longer overstates; SHA digest gap remains open per CG-007 original requirement |
| Internal Consistency | 0.20 | 0.88 | 0.176 | FIX-WI2-D eliminates the MC-08 vs. CG-007-inline contradiction; all 3 files mutually consistent; minor stylistic variation in upgrade-path phrasing only |
| Methodological Rigor | 0.20 | 0.82 | 0.164 | Named-constant pattern, semver pin, documented upgrade path, correct hardening flags all intact; SHA automation gap (no digest-validation CI step) persists |
| Evidence Quality | 0.15 | 0.85 | 0.1275 | MC-08 header now accurate; CG-007 inline honest; upgrade commands verifiable; no remaining inaccurate compliance claims |
| Actionability | 0.15 | 0.83 | 0.1245 | Files merge-ready; upgrade path documented inline; absence of tracked work item for SHA completion is the residual gap |
| Traceability | 0.10 | 0.87 | 0.087 | MC-08 → version-tag implementation chain now accurate; CG-007 inline traceability was already correct; FR-025, FR-023 cited correctly |
| **TOTAL** | **1.00** | | **0.845** | |

---

## Detailed Dimension Analysis

### Completeness (0.83/1.00)

**Evidence:**
Version-tag pinning is applied uniformly across all three files:
- `prompt-regression-smoke.yml` line 228: `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:0.86.0"`
- `prompt-regression-standard.yml` line 325: `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:0.86.0"`
- `prompt-regression-full.yml` line 280: `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:0.86.0"`

The MC-08 header now correctly scopes the implementation. The CG-007 inline comments are honest about the partial state. The false compliance claim gap (which penalized completeness in iteration 2) is closed.

**Gaps:**
CG-007 originally targeted SHA digest pinning. The implementation delivers version-tag pinning, which is a meaningful improvement but not the complete requirement. A version tag (`0.86.0`) remains mutable at the registry level — while GHCR does not enforce immutability on non-official image tags by policy, this is an assumption rather than a guarantee. The upgrade path is documented but unautomated and untracked. Score rises from 0.78 to 0.83 because the false-claim gap is closed; the SHA gap is the only remaining substantive incompleteness.

**Improvement Path:**
Pin to SHA digest (`ghcr.io/promptfoo/promptfoo@sha256:<digest>`) when Docker daemon access is available. The upgrade commands are already documented inline. Alternatively, file a formally accepted deviation from the SHA requirement with documented rationale — this would close the completeness gap at the requirements level without requiring implementation.

---

### Internal Consistency (0.88/1.00)

**Evidence:**
The FIX-WI2-D correction eliminates the primary contradiction. The MC-08 header in all three files now reads:

```
# MC-08: Docker image pinned to version tag 0.86.0 (not :latest); SHA digest pending Docker daemon availability — see CG-007 inline
```

The CG-007 inline in all three files states:
```
# CG-007: Version-pinned Docker image (supply chain security).
# Previously :latest — pinned to 0.86.0 for reproducibility.
# To upgrade to SHA pinning: docker pull <tag> && docker inspect --format='{{index .RepoDigests 0}}' <tag>
# Then replace the tag with the @sha256: digest.
```

These two are now consistent: both acknowledge version-tag pinning, both acknowledge SHA is future work. Cross-file consistency remains excellent — identical image string, identical variable name, identical comment structure in all three files.

**Gaps:**
Minor stylistic variation: the MC-08 header says "SHA digest pending Docker daemon availability" while the CG-007 inline says "To upgrade to SHA pinning" with explicit commands. These are consistent in intent (SHA is deferred, upgrade path is documented) and not contradictory. The small gap from 0.88 to 1.00 reflects that the phrasing between the summary claim (MC-08 header) and the detail (CG-007 inline) uses slightly different framing — "pending availability" vs. "how to upgrade" — which an auditor would need to read together to understand the full picture.

**Improvement Path:**
The consistency is substantially resolved. A marginal additional improvement would be adding a cross-reference within the CG-007 inline comment to MC-08 (e.g., "MC-08 partial compliance — full digest pinning pending") but this is not required for passing.

---

### Methodological Rigor (0.82/1.00)

**Evidence:**
- Named-constant pattern (`PROMPTFOO_IMAGE` variable) provides a single point of change per file — correct practice.
- Semver pinning to `0.86.0` eliminates the mutable `:latest` vulnerability, which was the most exploitable CG-007 weakness.
- Documented upgrade path (`docker pull <tag> && docker inspect --format='{{index .RepoDigests 0}}' <tag>`) is technically correct, repeatable, and portable.
- Docker hardening parameters (`--read-only`, `--cap-drop=ALL`, `--no-new-privileges`, `--memory`, `--cpus`, `--tmpfs`) remain intact and correct in all three files per MC-07, MC-13, MC-14.
- The stated environmental constraint (no Docker daemon in scoring environment) is legitimate.

**Gaps:**
The SHA upgrade path is documented but not automated or enforced. A rigorous supply chain security methodology would include one of: (a) a CI step that resolves the tag to a digest and validates it matches a known-good value, (b) a Makefile target for human-assisted digest resolution, or (c) a formal risk acceptance record for the version-tag-only approach. None of these exist. The methodology is sound at the implementation level but incomplete at the enforcement level. This is the weakest dimension post-fix.

**Improvement Path:**
Add automated digest validation: a CI step using `docker manifest inspect ghcr.io/promptfoo/promptfoo:0.86.0 | jq -r '.config.digest'` (or equivalent) that records the current digest and alerts on tag reassignment. This would be a methodological completion, not just documentation.

---

### Evidence Quality (0.85/1.00)

**Evidence:**
- CG-007 is cited inline in all three files with an honest, complete explanation: version-pinned to 0.86.0, not digest-pinned, previously :latest, upgrade path provided.
- MC-08 header is now accurate: "version tag 0.86.0 (not :latest); SHA digest pending Docker daemon availability."
- The concrete upgrade command (`docker pull <tag> && docker inspect --format='{{index .RepoDigests 0}}' <tag>`) is verifiable and correct.
- No remaining inaccurate compliance claims. The false claim that drove the iteration 2 evidence quality penalty is removed.

**Gaps:**
Evidence quality is limited by the absence of a SHA digest value in the code. A reader can verify version-tag pinning; they cannot verify digest binding without running the upgrade command themselves. The evidence for the partial CG-007 compliance is honest but necessarily incomplete — the full evidence (a recorded digest) does not yet exist in the codebase. Score stays at 0.85 rather than 0.90+ because "we have the version tag and documented how to get the digest" is qualitatively weaker evidence than "we have the digest."

**Improvement Path:**
Record the resolved SHA digest as a comment after completing the upgrade path. For example: `# Resolved digest: sha256:<hex> (validated YYYY-MM-DD)`. This adds verifiable evidence without requiring ongoing daemon access after the initial resolution.

---

### Actionability (0.83/1.00)

**Evidence:**
- All three workflow files are merge-ready in their current state.
- The version-pinned image provides immediate supply chain improvement over `:latest`.
- The SHA upgrade path is self-contained with actionable shell commands: `docker pull ghcr.io/promptfoo/promptfoo:0.86.0 && docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/promptfoo/promptfoo:0.86.0`.
- The upgrade path is present in the same location in all three files (within the Docker run step comment block).

**Gaps:**
The SHA digest upgrade is documented in code comments but not tracked as a work item. Without a GitHub issue or worktracker task, the "pending" state of the SHA pinning may be indefinitely deferred. The iteration 2 review recommended creating a tracked work item; this has not been done within the scope of the workflow files (as expected — workflow files are the deliverable, not the work item tracker). This remains an actionability gap at the process level: the commands exist, but there is no mechanism to ensure they are executed.

**Improvement Path:**
Create a GitHub issue titled "CG-007: Upgrade promptfoo image pin from version tag to SHA digest" and add a reference (issue URL or number) to the CG-007 inline comment. This transforms the "upgrade path" from an undirected note to a tracked commitment.

---

### Traceability (0.87/1.00)

**Evidence:**
- MC-08 → "version tag 0.86.0 (not :latest); SHA digest pending" → `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:0.86.0"` — this chain is now accurate in all three files.
- CG-007 inline traceability was already accurate in iteration 2 and remains so.
- FR-025 (promptfoo Docker isolation) cited in the FR traceability headers.
- FR-023 (UV-only Python, H-05) cited in headers.
- The "Previously :latest" acknowledgment in the CG-007 inline provides change-history traceability.

**Gaps:**
The traceability chain from MC-08 to the security control intent (digest pinning) to the actual implementation (version tag) now requires a reader to understand that "pending" means "not yet done." This is honest and correct — but a security auditor checking MC-08 compliance still needs to consult the CG-007 inline to understand the gap. The traceability is accurate but not self-contained within the MC-08 reference alone. Minor gap at 0.87 rather than 0.90+ reflects this two-step lookup requirement.

**Improvement Path:**
The existing cross-reference ("see CG-007 inline") in the MC-08 header directly addresses this. The traceability is as good as it can be given the partial implementation state. No further improvement recommended here until SHA pinning is complete.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.83 | 0.95 | Pin to SHA digest: `docker pull ghcr.io/promptfoo/promptfoo:0.86.0 && docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/promptfoo/promptfoo:0.86.0`. Replace version tag with `@sha256:<digest>` in all 3 files. Resolves the primary remaining CG-007 gap. |
| 2 | Methodological Rigor | 0.82 | 0.90 | Add a CI verification step or Makefile target that validates the pinned tag resolves to the recorded digest. Prevents silent tag reassignment. |
| 3 | Actionability | 0.83 | 0.88 | Create a GitHub issue for "CG-007: Upgrade promptfoo image pin to SHA digest" and add the issue URL to the CG-007 inline comment in all 3 files. Prevents indefinite deferral of the SHA upgrade. |
| 4 | Internal Consistency | 0.88 | 0.93 | After SHA upgrade, update MC-08 header to `"Docker image pinned to digest sha256:<hash> (not :latest); see CG-007 inline"`. Completes the consistency at full implementation state. |
| 5 | Evidence Quality | 0.85 | 0.93 | After SHA upgrade, record the resolved digest as a comment: `# Resolved digest: sha256:<hex> (validated YYYY-MM-DD)`. Adds verifiable, time-stamped evidence. |

**Estimated score with priority 1 only (SHA digest pinning):**
```
Completeness:        0.95 × 0.20 = 0.190
Internal Consistency: 0.93 × 0.20 = 0.186  (MC-08 header updated with digest)
Methodological Rigor: 0.88 × 0.20 = 0.176  (SHA-pinned; automation gap remains minor)
Evidence Quality:     0.92 × 0.15 = 0.138  (digest value recorded = verifiable evidence)
Actionability:        0.88 × 0.15 = 0.132  (merge-ready with complete control)
Traceability:         0.92 × 0.10 = 0.092  (MC-08 → digest → runtime = complete chain)
Composite estimate:                  0.914  → PASS (>= 0.92)
```

SHA digest pinning is the single change that crosses the PASS threshold.

---

## Leniency Bias Check
- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with line references
- [x] Uncertain scores resolved downward (Methodological Rigor at 0.82 not 0.85 — automation gap is real, not minor)
- [x] Calibration: 0.845 is consistent with "strong improvement, clear remaining gap" — appropriate for iteration 3 with a well-scoped fix applied
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] Composite math verified: (0.83×0.20)+(0.88×0.20)+(0.82×0.20)+(0.85×0.15)+(0.83×0.15)+(0.87×0.10) = 0.166+0.176+0.164+0.1275+0.1245+0.087 = **0.845**
- [x] Prior iteration delta checked: +0.071 from 0.774 is appropriate — the single-point fix (MC-08 header) was targeted and its benefit is bounded by the remaining SHA gap

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.845
threshold: 0.92
weakest_dimension: methodological_rigor
weakest_score: 0.82
critical_findings_count: 0
iteration: 3
delta_from_prior: +0.071
improvement_recommendations:
  - "SHA digest pinning: docker pull ghcr.io/promptfoo/promptfoo:0.86.0 && docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/promptfoo/promptfoo:0.86.0 — replace version tag with @sha256:<digest> in all 3 files (crosses PASS threshold alone)"
  - "Add CI step or Makefile target to validate pinned tag resolves to recorded digest (prevents silent tag reassignment)"
  - "Create GitHub issue for SHA digest upgrade and reference it in CG-007 inline comment (prevents indefinite deferral)"
path_to_pass: "SHA digest pinning in all 3 files → estimated composite 0.914 → PASS"
blocking_change: "One change required: pin to SHA digest instead of version tag"
```
