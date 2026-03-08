# Quality Score Report: CG-007 Docker Image SHA Pinning

## L0 Executive Summary

**Score:** 0.695/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Evidence Quality (0.55)
**One-line assessment:** The format change from tag-based to SHA digest syntax is structurally complete across all three workflow files, but placeholder digests (`sha256:PLACEHOLDER_DIGEST_TO_BE_RESOLVED`) render the implementation non-deployable; resolve the actual digest values to close CG-007.

## Scoring Context

- **Deliverable:** `.github/workflows/prompt-regression-full.yml`, `.github/workflows/prompt-regression-standard.yml`, `.github/workflows/prompt-regression-smoke.yml`
- **Deliverable Type:** Code (CI/CD workflow configuration)
- **Criticality Level:** C2 (security hardening; reversible within a day; affects 3 files)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.695 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.62 | 0.124 | Format change present in all 3 files; placeholder digest blocks production use |
| Internal Consistency | 0.20 | 0.80 | 0.160 | Identical placeholder, consistent source tag comments, MC-08 claims consistent with intent |
| Methodological Rigor | 0.20 | 0.72 | 0.144 | Correct `@sha256:` format used; update procedure documented; execution deferred |
| Evidence Quality | 0.15 | 0.55 | 0.0825 | Source tag cited, update command provided; no actual digest value as evidence |
| Actionability | 0.15 | 0.75 | 0.1125 | Resolution command is copy-paste ready; not deployable without follow-on step |
| Traceability | 0.10 | 0.72 | 0.072 | MC-08 cited in all 3 headers; TODO labeled CG-007; no link to originating gap analysis |
| **TOTAL** | **1.00** | | **0.695** | |

## Detailed Dimension Analysis

### Completeness (0.62/1.00)

**Evidence:**
- All three workflow files contain the SHA digest format line: `PROMPTFOO_IMAGE="ghcr.io/promptfoo/promptfoo@sha256:PLACEHOLDER_DIGEST_TO_BE_RESOLVED"` (full.yml line 281, standard.yml line 326, smoke.yml line 220).
- The format transition from `:0.86.0` (tag) to `@sha256:` (digest) is structurally applied consistently.
- All three files have been addressed — scope coverage is 3/3.

**Gaps:**
- The digest value is `PLACEHOLDER_DIGEST_TO_BE_RESOLVED` in all three files. This is not a valid SHA-256 digest and will cause `docker run` to fail at runtime with an image resolution error.
- CG-007's security objective (prevent supply chain attacks via mutable Docker tags) is not achieved until the digest is a real, verified value. A placeholder offers no supply chain protection.
- The implementation is structurally complete but operationally incomplete. Production deployment is blocked.

**Improvement Path:**
Run `docker pull ghcr.io/promptfoo/promptfoo:0.86.0 && docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/promptfoo/promptfoo:0.86.0` in an environment with Docker access. Replace the placeholder with the resolved digest (format: `sha256:a1b2c3...` — 64 hex chars) in all three files. Score would rise to 0.90+ on this dimension.

---

### Internal Consistency (0.80/1.00)

**Evidence:**
- The placeholder string is byte-for-byte identical in all three files: `sha256:PLACEHOLDER_DIGEST_TO_BE_RESOLVED`. No accidental drift between workflow files.
- The source tag comment is consistent across all three: `# Source tag: ghcr.io/promptfoo/promptfoo:0.86.0`.
- The update command comment is consistent across all three: `# To update: docker pull <new-tag> && docker inspect --format='{{index .RepoDigests 0}}' <new-tag>`.
- The TODO label is consistent: `# TODO(CG-007): Resolve SHA digest when Docker is available in build environment.`
- Security control headers in all three files cite MC-08 ("Docker image pinned to digest") — this is internally consistent with the intent of the change even though the placeholder is not a real pin.

**Gaps:**
- The MC-08 header claim "Docker image pinned to SHA digest" is technically accurate as a description of intent, but the placeholder means the image is not actually pinned at runtime. This creates a minor inconsistency between the header's declarative assertion and the actual runtime behavior.
- No contradictions between the three files or between the header claims and the code structure.

**Improvement Path:**
Resolving the placeholder removes the minor header-vs-runtime inconsistency. Alternatively, updating the MC-08 comment to note "pending digest resolution" would make the current state more accurately described.

---

### Methodological Rigor (0.72/1.00)

**Evidence:**
- The approach follows established supply chain security methodology: transition from mutable `:tag` references to immutable `@sha256:digest` references. This is the correct SLSA / OWASP CI/CD Top-10 C-05 equivalent for Docker images.
- The update procedure is documented inline in all three files, showing awareness of how to maintain the pin going forward.
- All three workflow files receive the same treatment — no ad-hoc differences.
- The TODO explains the environmental constraint (Docker not available in build environment), which is a legitimate blocker for automated resolution during the workflow authoring session.

**Gaps:**
- The implementation stops at the format change without completing the resolution step, even though the documented procedure is available. A rigorous implementation would defer merge until the digest is resolved, rather than committing a placeholder.
- There is no verification step (e.g., a CI check that asserts the image reference is not a placeholder) to catch the placeholder before it reaches production.

**Improvement Path:**
Add a CI validation step that greps for `PLACEHOLDER` in workflow files and fails if found. This guards against future regressions and flags the current state as incomplete. Resolving the placeholder before merge is the primary improvement.

---

### Evidence Quality (0.55/1.00)

**Evidence:**
- The source tag is documented (`ghcr.io/promptfoo/promptfoo:0.86.0`) — provides traceability to the originating image version.
- The update command is documented — demonstrates the implementor knows how to obtain the real digest.
- The TODO(CG-007) annotation provides evidence that the gap is acknowledged and tracked.

**Gaps:**
- No actual SHA-256 digest is present. The definitive evidence that a real image pin is in place would be a 64-character hex digest (e.g., `sha256:a1b2c3d4e5f6...`). The placeholder string provides zero supply chain protection.
- The MC-08 security control claim in the workflow headers asserts completion ("pinned to digest") but the evidence in the code body contradicts it (placeholder).
- No cross-reference to the actual GHCR registry page or manifest for the 0.86.0 tag to establish that the source tag is current and uncompromised.

**Improvement Path:**
Provide the resolved digest. Score rises to 0.85+ when the placeholder is replaced with a real digest that can be independently verified against the GHCR registry.

---

### Actionability (0.75/1.00)

**Evidence:**
- The resolution path is unambiguous and copy-paste ready in all three files:
  ```
  docker pull <new-tag> && docker inspect --format='{{index .RepoDigests 0}}' <new-tag>
  ```
  Substituting `ghcr.io/promptfoo/promptfoo:0.86.0` for `<new-tag>` gives a complete, executable command.
- The `TODO(CG-007)` label makes the blocking item discoverable via code search (`grep -r CG-007`).
- The blocker is explicitly stated: "when Docker is available in build environment."

**Gaps:**
- The files are not immediately deployable. Any CI run against these workflow files will fail at the `docker run` step with an image resolution error, because `sha256:PLACEHOLDER_DIGEST_TO_BE_RESOLVED` is not a valid digest.
- No test or guard prevents accidental use of the placeholder in a live run.
- The TODO does not specify who is responsible for resolution or by what date, reducing actionability for follow-up prioritization.

**Improvement Path:**
Assign CG-007 resolution as a blocking task with an owner and a deadline. Add a CI guard (grep for `PLACEHOLDER` in workflow files). Both steps are low-effort and high-impact.

---

### Traceability (0.72/1.00)

**Evidence:**
- MC-08 is cited in all three workflow file security control comment blocks, providing a thread from the implementation back to the system-design.md threat model.
- `TODO(CG-007)` appears in all three files, linking the placeholder to the gap item identifier.
- The source tag (`ghcr.io/promptfoo/promptfoo:0.86.0`) is recorded, allowing the image version to be traced to the GHCR registry.
- FR-025 (promptfoo Docker isolation) is cited in all three FR traceability sections.

**Gaps:**
- No link to the gap analysis document where CG-007 was identified (e.g., no reference to `gap-analysis-20260307-001/` or the originating work item path).
- The MC-08 claim in the security controls header traces to a control that is not fully satisfied — the traceability chain says "complete" but the implementation says "placeholder."
- No reference to the system-design.md section where the threat model establishes why SHA pinning is required (the "why" is implicit, not explicit in the change).

**Improvement Path:**
Add a comment linking to the gap analysis document or CG-007 work item path. Update MC-08 comment to clarify current state (pending digest resolution vs. complete).

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness | 0.62 | 0.90 | Resolve the placeholder digest: run `docker pull ghcr.io/promptfoo/promptfoo:0.86.0 && docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/promptfoo/promptfoo:0.86.0` in a Docker-available environment and replace `PLACEHOLDER_DIGEST_TO_BE_RESOLVED` in all 3 files with the real 64-char hex digest. This is the blocking item for CG-007 closure. |
| 2 | Evidence Quality | 0.55 | 0.85 | The real digest is the missing evidence. Resolving P1 automatically resolves P2. Optionally add a comment with the verified digest alongside the GHCR registry URL for independent verification. |
| 3 | Methodological Rigor | 0.72 | 0.88 | Add a CI validation step (e.g., a `grep` in a workflow or pre-commit hook) that asserts no workflow file contains the string `PLACEHOLDER`. This prevents future regressions and flags the current state as incomplete if a merge is attempted before resolution. |
| 4 | Actionability | 0.75 | 0.90 | Assign the resolution task to a named owner with a specific deadline. The TODO(CG-007) comment documents what to do but not who will do it or when. |
| 5 | Traceability | 0.72 | 0.85 | Add a comment to each file linking to the gap analysis or CG-007 work item path. Update the MC-08 security control annotation to reflect that the control is "pending digest resolution" rather than claiming full completion. |
| 6 | Internal Consistency | 0.80 | 0.90 | After resolving P1, update the MC-08 header comment from "Docker image pinned to SHA digest" to include the actual digest short-form for at-a-glance verification. |

## Leniency Bias Check

- [x] Each dimension scored independently
- [x] Evidence documented for each score
- [x] Uncertain scores resolved downward (Completeness debated 0.62-0.68, chose 0.62; Evidence Quality debated 0.55-0.65, chose 0.55)
- [x] First-draft calibration considered (initial draft scores; implementation is in an intermediate "structurally complete but operationally blocked" state that warrants lower scores)
- [x] No dimension scored above 0.95 without exceptional evidence (max dimension score is 0.80)

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.695
threshold: 0.92
weakest_dimension: evidence_quality
weakest_score: 0.55
critical_findings_count: 0
iteration: 1
improvement_recommendations:
  - "Resolve placeholder SHA digest in all 3 workflow files (blocking item)"
  - "Add CI guard asserting no workflow file contains 'PLACEHOLDER'"
  - "Assign resolution owner and deadline for CG-007"
  - "Update MC-08 comment to reflect pending-resolution state"
  - "Add traceability link to gap analysis or CG-007 work item path"
```
