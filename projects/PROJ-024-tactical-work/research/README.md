# PROJ-024 Research Index

> Index of research artifacts for the PROJ-024 Tactical Work project. Research is organized into dated subdirectories, one per investigation. This index documents each subdirectory and its contents.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | How research is organized |
| [Dependabot Merge Analysis (2026-06-22)](#dependabot-merge-analysis-2026-06-22) | PR merge sequencing + CI root-cause investigation |
| [Security-Scan Hardening (2026-06-22)](#security-scan-hardening-2026-06-22) | Pipeline hardening design, audit, and proposal staging |

---

## Overview

Each investigation lives in its own dated subdirectory under `research/`, following the
`{slug}-{YYYYMMDD}` convention. This page is the navigable index over those subdirectories.
The two investigations below underpin EPIC-004 (Dependency Security-Scan Pipeline Hardening)
and the surrounding dependency-management work for this project.

---

## Dependabot Merge Analysis (2026-06-22)

Directory: [`dependabot-merge-analysis-20260622/`](dependabot-merge-analysis-20260622/)

Investigation into the open Dependabot pull requests, the correct merge order, and the
root cause of the CI / security-scan failures encountered while merging them.

| Document | Description |
|----------|-------------|
| [`RECOMMENDATION.md`](dependabot-merge-analysis-20260622/RECOMMENDATION.md) | Consolidated merge recommendation and sequencing for the open Dependabot PRs |
| [`PR-298-and-ci-rootcause.md`](dependabot-merge-analysis-20260622/PR-298-and-ci-rootcause.md) | Analysis of PR #298 plus the CI / security-scan failure root cause |
| [`PR-299-291-precommit.md`](dependabot-merge-analysis-20260622/PR-299-291-precommit.md) | Merge analysis for PR #299 and PR #291 (pre-commit hook bumps) |
| [`PR-300-uv-group.md`](dependabot-merge-analysis-20260622/PR-300-uv-group.md) | Analysis of PR #300 (uv-minor-patch group, 12 updates) |
| [`adversarial-review.md`](dependabot-merge-analysis-20260622/adversarial-review.md) | Adversarial review of the Dependabot merge plan |

---

## Security-Scan Hardening (2026-06-22)

Directory: [`security-scan-hardening-20260622/`](security-scan-hardening-20260622/)

Design and audit artifacts backing EPIC-004: hardening the dependency security-scan pipeline
into one shared, correct, owner-governed scanner.

| Document | Description |
|----------|-------------|
| [`github-issue-body.md`](security-scan-hardening-20260622/github-issue-body.md) | Body for the tracking GitHub issue (#301) describing the pipeline blind spot and plan |
| [`worktracker-audit.md`](security-scan-hardening-20260622/worktracker-audit.md) | Audit of the EPIC-004 worktracker entities against structure/containment rules |
| [`adversarial-review.md`](security-scan-hardening-20260622/adversarial-review.md) | Adversarial review of the security-CI hardening design (ADR-secscan-hardening-001) |
| [`proposal/`](security-scan-hardening-20260622/proposal/) | Staging directory for the proposed implementation: composite `action.yml`, CVE `audit-allowlist.yml`, `audit_allowlist.py` script, draft `ci.yml`/`security-scan.yml` jobs, `CODEOWNERS` addition, and a `VERIFY.md` runbook |

---
