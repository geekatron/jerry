# Quality Score Report: CG-007 Docker Image Pinning — Iteration 2 Re-Score

## L0 Executive Summary
**Score:** 0.774/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.72)
**One-line assessment:** Version-tag pinning is a meaningful improvement over :latest but the MC-08 header comments still assert digest pinning, creating a false compliance claim that must be corrected before the score can reach threshold.

## Scoring Context
- **Deliverable:** `.github/workflows/prompt-regression-smoke.yml`, `.github/workflows/prompt-regression-standard.yml`, `.github/workflows/prompt-regression-full.yml`
- **Deliverable Type:** Code (CI/CD workflow configuration)
- **Criticality Level:** C2 (supply chain security control across 3 workflow files)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Prior Score:** 0.695 (iteration 1 — `:latest` tag)
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.774 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No (direct deliverable review) |
| **Delta from Prior Score** | +0.079 (0.695 → 0.774) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.78 | 0.156 | Fix applied consistently across all 3 files; MC-08 header still claims digest pinning which is not achieved |
| Internal Consistency | 0.20 | 0.72 | 0.144 | All 3 files mutually consistent; internal contradiction between MC-08 header ("pinned to digest") and inline CG-007 comment (acknowledges version tag) |
| Methodological Rigor | 0.20 | 0.80 | 0.160 | Semver pinning is sound practice; SHA upgrade path documented; named constant pattern correct |
| Evidence Quality | 0.15 | 0.78 | 0.117 | CG-007 cited inline with honest rationale; upgrade path commands concrete; MC-08 compliance claim unsupported |
| Actionability | 0.15 | 0.82 | 0.123 | Files are merge-ready as-is; SHA upgrade path clearly documented for when Docker daemon is available |
| Traceability | 0.10 | 0.74 | 0.074 | CG-007 traceable in all 3 files; MC-08 → implementation chain is misleading (claims digest, delivers tag) |
| **TOTAL** | **1.00** | | **0.774** | |

---

## Detailed Dimension Analysis

### Completeness (0.78/1.00)

**Evidence:**
The version-tag fix is applied uniformly across all three workflow files:
- `prompt-regression-smoke.yml` line 228: `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:0.86.0"`
- `prompt-regression-standard.yml` line 325: `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:0.86.0"`
- `prompt-regression-full.yml` line 280: `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo:0.86.0"`

All three files scope the fix consistently. The CG-007 requirement is partially addressed — the most severe vulnerability (mutable :latest tag resolving to different images on each pull) is eliminated.

**Gaps:**
The original CG-007 requirement was SHA digest pinning. A version tag (`0.86.0`) is still mutable if the registry allows tag reassignment (which GHCR does not enforce by policy on non-official images). The MC-08 header comment in all three files still asserts "Docker image pinned to digest (not :latest tag)" — this overstates the implementation. A reader auditing MC-08 compliance would incorrectly conclude the control is fully implemented.

**Improvement Path:**
Correct the MC-08 header comment in all three files to state "Docker image pinned to version tag (not :latest); SHA digest upgrade path documented at CG-007 inline comment." This corrects the false compliance claim without requiring Docker daemon access.

---

### Internal Consistency (0.72/1.00)

**Evidence:**
The three workflow files are mutually consistent: identical image string, identical variable name `PROMPTFOO_IMAGE`, identical CG-007 comment structure, and identical SHA upgrade path documentation pattern. Cross-file consistency is excellent.

**Gaps:**
There is a direct intra-file contradiction in all three workflows:

The security controls header (all three files) states:
```
# MC-08: Docker image pinned to digest (not :latest tag)
```

The inline CG-007 comment (all three files) states:
```
# CG-007: Version-pinned Docker image (supply chain security).
# Previously :latest — pinned to 0.86.0 for reproducibility.
# To upgrade to SHA pinning: docker pull <tag> && docker inspect ...
```

The header claims digest pinning is done. The inline comment acknowledges it is not (and documents the path to do it). These two statements directly contradict each other in the same file. A reader following MC-08 would conclude digest pinning is complete; a reader following the CG-007 inline would understand it is not. This is a documentation integrity failure.

**Improvement Path:**
Update the MC-08 header comment in all three files to remove the false claim. Change `"Docker image pinned to digest (not :latest tag)"` to `"Docker image pinned to version tag 0.86.0 (not :latest); SHA digest pending Docker daemon availability — see CG-007 inline"`. This eliminates the contradiction.

---

### Methodological Rigor (0.80/1.00)

**Evidence:**
- Use of a named constant `PROMPTFOO_IMAGE` rather than an inline image string is good practice — single point of change per file
- Semver pinning to `0.86.0` eliminates the mutable `:latest` vulnerability
- The documented upgrade path (`docker pull <tag> && docker inspect --format='{{index .RepoDigests 0}}' <tag>`) is technically correct and provides a repeatable procedure
- The environmental constraint (no Docker daemon in the scoring environment) is legitimate and documented
- Docker hardening parameters (--read-only, --cap-drop=ALL, --no-new-privileges, etc.) remain intact

**Gaps:**
The SHA upgrade path is documented but not automated. A future CI step or Makefile target that resolves and records the digest would prevent the "forgot to upgrade" scenario. This is a medium-term gap rather than a blocking defect.

**Improvement Path:**
Consider adding a CI check or Makefile target that validates the pinned tag resolves to a known SHA (using a machine that has Docker access). This would catch tag reassignment and provide automated enforcement of the intent behind CG-007.

---

### Evidence Quality (0.78/1.00)

**Evidence:**
- CG-007 is cited inline in all three files with an honest explanation: version-pinned, not digest-pinned, previously :latest
- The concrete upgrade command (`docker pull` + `docker inspect`) is verifiable and correct
- The environmental constraint (no Docker daemon) is the stated reason for not completing full SHA pinning
- All three CG-007 inline comments are worded consistently and honestly

**Gaps:**
The MC-08 header comment in all three files makes a compliance claim ("pinned to digest") that is not supported by the implementation (version tag). This undermines evidence quality for anyone auditing MC-08 as a security control. The inline CG-007 evidence is honest; the header evidence is inaccurate.

**Improvement Path:**
Correct the MC-08 header comments to accurately reflect what was implemented. Accurate header comments would bring Evidence Quality to approximately 0.88 without requiring any changes to the actual Docker image reference.

---

### Actionability (0.82/1.00)

**Evidence:**
- The three workflow files are merge-ready in their current state
- The version-pinned tag provides immediate supply chain improvement over :latest
- The SHA upgrade path is documented with actionable shell commands that any developer with Docker daemon access can execute
- The upgrade path is self-contained (no additional context needed to follow it)

**Gaps:**
The actionability gap is the absence of a tracked work item for the SHA digest upgrade. The documented `docker inspect` command is present in code comments but is not linked to a worktracker task or GitHub issue that would ensure follow-through. Without a tracked item, the SHA upgrade could be indefinitely deferred.

**Improvement Path:**
Create a worktracker task or GitHub issue for "Upgrade CG-007 promptfoo image pin to SHA digest when Docker daemon is available" with the documented command as implementation guidance. This ensures the partial closure is not treated as permanent.

---

### Traceability (0.74/1.00)

**Evidence:**
- CG-007 is referenced in all three files via inline comments (lines 224, 322, 277 respectively)
- MC-08 is referenced in the security controls header of all three files
- FR-025 (promptfoo Docker isolation) is cited in the FR traceability header
- The scoring context links this to the prior iteration (0.695, iteration 1)
- The previous `:latest` reference is acknowledged inline ("Previously :latest")

**Gaps:**
The traceability from MC-08 to the actual implementation is broken by the inaccurate header claim. A security auditor following MC-08 → "Docker image pinned to digest" → actual implementation would find a version tag, not a digest. The traceability chain produces a misleading conclusion. The CG-007 inline traceability is accurate; the MC-08 traceability is not.

**Improvement Path:**
Fix MC-08 header comments to accurately state what is implemented. Optionally add a cross-reference from CG-007 inline comment to MC-08 noting the partial implementation status.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.72 | 0.85 | Fix MC-08 header comment in all 3 files: change "pinned to digest (not :latest tag)" to "pinned to version tag 0.86.0; SHA digest upgrade path at CG-007 inline comment." This is a 3-line edit with no logic change. |
| 2 | Traceability | 0.74 | 0.85 | After fixing MC-08 header, verify the traceability chain: MC-08 → version tag pinning (accurate), CG-007 → SHA upgrade path documented (accurate). No additional changes needed beyond priority 1. |
| 3 | Completeness | 0.78 | 0.88 | Create a worktracker task or GitHub issue for SHA digest upgrade to prevent indefinite deferral of the remaining CG-007 gap. Link from CG-007 inline comment. |
| 4 | Evidence Quality | 0.78 | 0.88 | Addressed by priority 1 (removing the inaccurate MC-08 claim). No additional action. |
| 5 | Actionability | 0.82 | 0.90 | Addressed by priority 3 (tracked work item). |

**Estimated score after priority 1 fix:** The MC-08 comment correction would raise Internal Consistency to approximately 0.88 (cross-file consistency remains excellent, contradiction eliminated) and Traceability to approximately 0.84. Revised composite estimate: (0.78×0.20) + (0.88×0.20) + (0.80×0.20) + (0.82×0.15) + (0.82×0.15) + (0.84×0.10) = 0.156 + 0.176 + 0.160 + 0.123 + 0.123 + 0.084 = **0.822**.

A further revision implementing priority 3 (tracked work item) would close Completeness to approximately 0.85 and Actionability to approximately 0.88, pushing the composite to approximately **0.847** — still below the 0.92 threshold. Reaching 0.92 requires actual SHA digest pinning or a documented, accepted deviation from the CG-007 SHA requirement.

**Path to PASS:** Full SHA pinning when Docker daemon access is available (resolves Completeness to 0.95, Internal Consistency to 0.95 after header fix). Estimated composite with full SHA pinning and header correction: approximately 0.934 — PASS.

---

## Leniency Bias Check
- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Internal Consistency at 0.72 rather than 0.75 due to direct contradiction in same file)
- [x] First-draft calibration considered (this is iteration 2; +0.079 delta from iteration 1 reflects genuine improvement)
- [x] No dimension scored above 0.95 without exceptional evidence
- [x] Composite math verified: (0.78×0.20)+(0.72×0.20)+(0.80×0.20)+(0.78×0.15)+(0.82×0.15)+(0.74×0.10) = 0.156+0.144+0.160+0.117+0.123+0.074 = 0.774

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.774
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.72
critical_findings_count: 0
iteration: 2
improvement_recommendations:
  - "Fix MC-08 header comment in all 3 workflow files — change 'pinned to digest' to 'pinned to version tag 0.86.0; SHA upgrade path at CG-007 inline comment' (3-line edit, no logic change)"
  - "Create worktracker task or GitHub issue for SHA digest upgrade when Docker daemon available — prevents indefinite deferral"
  - "Optionally cross-reference from CG-007 inline comment to linked work item for full traceability"
delta_from_prior: +0.079
path_to_pass: "SHA digest pinning (requires Docker daemon) + MC-08 header correction → estimated 0.934"
```
