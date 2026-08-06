# TASK-025: Add SLSA Build Provenance to Release Pipeline

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-04-15
> **Completed:** 2026-04-16
> **Parent:** EN-006
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |
| [Evidence](#evidence) | Verification record |

---

## Summary

The release pipeline produces SHA256 checksums but no signed provenance attestations. Consumers cannot verify that artifacts were built from the claimed source by the claimed CI system. Currently SLSA Level 0. Adding `actions/attest-build-provenance` achieves Level 2 at near-zero cost.

**Finding:** eng-devsecops Finding 2 (HIGH), `release.yml` entire file

---

## Acceptance Criteria

- [x] `actions/attest-build-provenance` added to release job (SHA-pinned: `e8998f949152b193b063cb0ec769d69d929409be`)
- [x] Provenance attestation covers .tar.gz, .zip, and checksums.sha256 artifacts
- [x] Attestation is signed by GitHub Actions OIDC (SLSA Level 2)
- [x] `docs/reference/ci-cd-pipeline-security.md` updated with SLSA Level 2 status
- [x] `id-token: write` and `attestations: write` scoped to `release` job only (least privilege, per red-recon finding)

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| SHA resolution | eng-infra | Annotated tag dereferenced to commit `e8998f949152b193b063cb0ec769d69d929409be` |
| Action SHA-pinned | red-recon | CLOSED |
| Permissions scoped correctly | red-recon | CLOSED (moved to job-level after red-recon flagged workflow-level as over-broad) |
| Step ordering correct | red-recon | CLOSED — after download, before release creation |
| Reference doc updated | diataxis-reference | SLSA Build Provenance section + SHA Pinning table + Permission Model updated |
