## Summary

The dependency security-scanning pipeline has a critical blind spot plus accumulated drift. The CI audit (`ci.yml`) correctly detects transitive CVEs and is currently **RED**, but the **scheduled** scan (`security-scan.yml`) is **false-green** — it audits only the local project and misses everything. The two scans duplicate logic and have drifted apart; the silent-failure guard is ineffective; and there are 9 known transitive CVEs in the lockfile.

This issue tracks hardening the pipeline into **one shared, correct, owner-governed scanner**.

> Internal SSOT: worktracker `EPIC-004` (PROJ-024-tactical-work). This is the umbrella issue; per-entity child issues (H-32) to follow at implementation if desired.

## Root cause

- **`ci.yml` `security` job** exports the full dependency set then runs `pip-audit --requirement … --strict` → correctly finds **9 vulnerabilities in 5 packages**. RED, and correct.
- **`security-scan.yml` (scheduled)** runs bare `uv run pip-audit --strict` (no `--requirement`) → audits only the local `jerry` package, logs `Dependency not found on PyPI … jerry`, exits 0 → **false green**. Its guard only checks output ≥ 1 line, so the 1-line error message fools it.
- **`dependabot.yml`** uses `allow: dependency-type: direct` (intentional), so transitive CVEs never get Dependabot version-update PRs. The scheduled scan was meant to be the compensating detector — but it has been silently detecting nothing.

## Current open CVEs (also the red/green test fixture)

| Package (transitive) | Have | Fix | IDs |
|---|---|---|---|
| urllib3 | 2.6.3 | 2.7.0 | PYSEC-2026-141, PYSEC-2026-142 |
| pip | 26.0 | 26.1.2 | PYSEC-2026-196, CVE-2026-3219, CVE-2026-6357 |
| mako | 1.3.10 | 1.3.12 | CVE-2026-44307 |
| pydantic-settings | 2.13.1 | 2.14.2 | GHSA-4xgf-cpjx-pc3j |
| msgpack | 1.1.2 | 1.2.1 | GHSA-6v7p-g79w-8964 |

All fixable with non-major bumps. None require the accept-list.

## Plan

1. **DRY** — one local composite action (`.github/actions/security-audit/`) called by both `ci.yml` and `security-scan.yml`, so they can never drift again.
2. **Owner CVE accept-list** (`.github/security/audit-allowlist.yml`) — per-entry `review_by` expiry; expired entries auto-resurface; approval = code-owner-reviewed PR (requires CODEOWNERS coverage of the new paths). Fails **closed** on any malformed/missing entry.
3. **Alerting** — scheduled scan opens/updates one rolling "Open transitive CVEs" issue assigned to the owner, plus Dependabot native alerts.
4. **Fix the silent-failure guard** — require a real verdict line AND ≥ 20 audited packages (kills the false-green).
5. **Non-blocking policy** — CI audit warns but does not block merges (pending owner Option A/B decision).
6. **Remediate** the 9 current CVEs.
7. **Confirm** Dependabot security updates + vulnerability alerts are enabled.

## Worktracker (PROJ-024)

- `EPIC-004` Security-Scan Pipeline Hardening
  - `FEAT-002` Security-scan pipeline hardening
    - `BUG-008` Scheduled scan false-green
    - `STORY-026` Unify CI + scheduled audit into one composite action (DRY)
    - `STORY-027` Owner-governed CVE accept-list with expiry
    - `STORY-028` Owner alerting via auto-managed rolling issue
    - `STORY-029` Fix the silent-failure guard
    - `STORY-030` Remediate the 9 current transitive CVEs
    - `EN-007` Pipeline hardening enabler → `TASK-035` Confirm Dependabot settings

## Design & verification artifacts

- ADR: `projects/PROJ-024-tactical-work/decisions/ADR-secscan-hardening-001.md`
- Adversarial review (2 rounds, verdict **SAFE TO IMPLEMENT AS-IS**): `projects/PROJ-024-tactical-work/research/security-scan-hardening-20260622/adversarial-review.md`
- Draft artifacts: `projects/PROJ-024-tactical-work/research/security-scan-hardening-20260622/proposal/`

## Implementation (on approval)

- **PR 1 — scanner fix:** composite action + accept-list + alerting + guard fix + CODEOWNERS. Its own CI security check will be RED until PR 2 lands — *by design* (it proves the detector works).
- **PR 2 — dependency remediation:** bump the 5 packages → CI goes green.

## Pending owner decision

**CI blocking policy:** Option A (non-blocking warning, recommended) vs Option B (block only on lockfile-changing PRs that introduce a *new* vuln). See ADR §D3.
