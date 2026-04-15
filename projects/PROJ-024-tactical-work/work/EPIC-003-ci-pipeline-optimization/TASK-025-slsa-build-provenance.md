# TASK-025: Add SLSA Build Provenance to Release Pipeline

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-15
> **Parent:** EN-006
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

The release pipeline produces SHA256 checksums but no signed provenance attestations. Consumers cannot verify that artifacts were built from the claimed source by the claimed CI system. Currently SLSA Level 0. Adding `actions/attest-build-provenance` achieves Level 2 at near-zero cost.

**Finding:** eng-devsecops Finding 2 (HIGH), `release.yml` entire file

---

## Acceptance Criteria

- [ ] `actions/attest-build-provenance` added to release job (SHA-pinned)
- [ ] Provenance attestation covers .tar.gz, .zip, and checksums.sha256 artifacts
- [ ] Attestation is signed by GitHub Actions OIDC (SLSA Level 2)
- [ ] `docs/reference/ci-cd-pipeline-security.md` updated with SLSA Level 2 status
