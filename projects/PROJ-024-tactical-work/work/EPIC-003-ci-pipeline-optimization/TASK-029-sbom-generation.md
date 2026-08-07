# TASK-029: Add SBOM Generation to Release Pipeline

> **Type:** task
> **Status:** completed
> **Priority:** medium
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

No Software Bill of Materials is generated during build or release. Consumers cannot programmatically enumerate the dependency tree. Add CycloneDX SBOM generation via `anchore/sbom-action` or `uv export --format cyclonedx` and attach as a release artifact.

**Finding:** eng-devsecops Finding 6 (MEDIUM), `release.yml` entire file
**Dependencies:**
- TASK-025: SLSA provenance must exist first so attestation covers SBOM artifact
- TASK-028: Release mechanism decision (softprops vs gh CLI) affects how SBOM is attached

---

## Acceptance Criteria

- [x] CycloneDX JSON SBOM generated during release build via `uv run --with cyclonedx-bom cyclonedx-py environment`
- [x] SBOM attached as release artifact via `gh release create` + covered by SLSA provenance attestation
- [x] SBOM covers all runtime + dev dependencies from installed environment (reflects exact uv.lock pins)

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| Decision | eng-infra | Option A (cyclonedx-py via uv ephemeral) — no third-party Action, no lockfile pollution |
| SBOM in build job | release.yml lines 198-206 | `cyclonedx-py environment --of JSON` generates CycloneDX 1.6 |
| SBOM in attestation | release.yml line 225 | `dist/sbom.cyclonedx.json` in subject-path |
| SBOM in release | release.yml line 286 | Attached via `gh release create` glob |
