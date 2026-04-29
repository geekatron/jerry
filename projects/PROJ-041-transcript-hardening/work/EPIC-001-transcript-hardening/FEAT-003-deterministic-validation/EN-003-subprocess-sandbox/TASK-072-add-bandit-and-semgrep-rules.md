# TASK-072: Add Bandit + Semgrep rules forbidding direct subprocess.run outside this adapter

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-003
> **Owner:** eng-devsecops

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Static-analysis rules force all future code to go through SubprocessSandbox.

---

## Acceptance Criteria

- [ ] Bandit config flags any direct subprocess.run/Popen call in src/jerry/transcript/
- [ ] Semgrep rule rejects PRs that add direct subprocess calls outside SubprocessSandboxAdapter
- [ ] CI integration confirmed
