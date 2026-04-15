# TASK-029: Add SBOM Generation to Release Pipeline

> **Type:** task
> **Status:** pending
> **Priority:** medium
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

No Software Bill of Materials is generated during build or release. Consumers cannot programmatically enumerate the dependency tree. Add CycloneDX SBOM generation via `anchore/sbom-action` or `uv export --format cyclonedx` and attach as a release artifact.

**Finding:** eng-devsecops Finding 6 (MEDIUM), `release.yml` entire file
**Dependencies:**
- TASK-025: SLSA provenance must exist first so attestation covers SBOM artifact
- TASK-028: Release mechanism decision (softprops vs gh CLI) affects how SBOM is attached

---

## Acceptance Criteria

- [ ] CycloneDX JSON SBOM generated during release build
- [ ] SBOM attached as release artifact alongside checksums
- [ ] SBOM covers all runtime dependencies from uv.lock
