# TASK-002: Implement SubprocessSandboxAdapter with all five defensive controls

> **Type:** task
> **Status:** pending
> **Priority:** critical
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** EN-003
> **Owner:** eng-infra

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Implement the `SubprocessSandboxAdapter` class at `src/jerry/transcript/validation/infrastructure/subprocess_sandbox.py` per the security boundary design captured in EN-003. The adapter must enforce all five defensive controls from the EN-003 threat model (command allowlist, path traversal guard, timeout, env sanitization, output cap). This is the security-critical Task for the entire FEAT-003 Feature — every grep-pattern execution in the validators routes through this adapter, so a bypass here defeats the deterministic substrate validation premise.

Priority is `critical` because a sandbox flaw enables shell injection via JSON-supplied patterns in `_anchors.json` (the threat surface that motivated EN-003).

---

## Acceptance Criteria

- [ ] Adapter rejects any command not in allowlist (`grep`, `wc`, `find`) with typed `SandboxRefusalError`
- [ ] Adapter resolves all path arguments via `pathlib.Path.resolve()` and refuses execution if any path leaves `packet_root`
- [ ] Adapter kills subprocess at 5s wall-clock by default; raises `SandboxTimeoutError` when exceeded
- [ ] Adapter passes only `PATH=/usr/bin:/bin` to subprocess env (strips all other vars including `LD_PRELOAD`, `PYTHONPATH`)
- [ ] Adapter caps captured stdout at 1 MB; raises `SandboxOutputOverflowError` when exceeded
