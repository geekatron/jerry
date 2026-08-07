# BUG-010 (jerry ast widening) — Resume Pointer

> Checkpoint for resuming after session compaction. Read this first.

## Where this stands (2026-08-07)

- **GitHub issue:** [#337](https://github.com/geekatron/jerry/issues/337) — `jerry ast` rejected files outside the plugin install tree.
- **Branch:** `fix/BUG-010-ast-project-root` (open PR [#341](https://github.com/geekatron/jerry/pull/341), 15/15 green at last check). The base fix (anchor containment to the user's project root via `CLAUDE_PROJECT_DIR`/cwd) is committed as `62b429e8`.
- **Uncommitted-then-checkpointed on top:** the containment *widening* (auto-allow temp/scratchpad roots + a `--root` flag) plus two red-team remediations (H-01 temp-ownership gate, H-02 broad-root warning), plus the full C4 adversarial tournament artifacts. Committed as a WIP checkpoint labelled **DO NOT MERGE**.

## The blocker: C4 tournament verdict = REVISE (0.64)

The owner ran the full 10-strategy C4 adversarial tournament on the widening. Score **0.64** (gate 0.92) → REVISE. Deduped Critical clusters (see `adv-s014-tournament-score.md` for the full ranked, corroborated list):

1. **C1** — index-based (not location-based) trust: if the project root itself resolves inside a temp tree, the ownership gate + transparency note silently skip. (6 strategies; the eng-team gate had wrongly called this "correct".)
2. **C2** — `ast_modify` write path never runs the ownership gate → symlink-swap can overwrite another user's file. (5 strategies)
3. **C3** — ownership gate fails **open** on `stat()` OSError, attacker-forceable. (4 strategies)
4. **C4** — same-UID/root multi-tenant (containers/CI as uid 0) defeats the gate. (4 strategies)
5. **C5** — `TMPDIR`/`TEMP` env poisoning widens the default root set with no warning.
6. **C6** — the R-4 transparency note corrupts JSON output when stderr is merged (`2>&1`); no suppression flag.

## THE OPEN DECISION (owner must choose before eng-backend remediates)

**How to remediate:**
- **(A) Environment-gated redesign** (Inversion strategy DR-2, recommended): auto-widen to temp/scratchpad roots ONLY when `CLAUDE_PROJECT_DIR` is set (plugin context); project-root-only when standalone (pip/CI). Dissolves C1/C4/C5 at the root; still fix C2/C3/C6. Serves the "CLI extracted to a pip package" future the owner named.
- **(B) Patch the current always-widen model** — fix each Critical individually.

Owner has NOT yet chosen. Do not start remediation until they do.

## Owner decisions already locked (apply during remediation)

- `--root` stays an exclusive, full escape hatch (bypasses the ownership gate) — intended, "user's discretion"; future pip-package context.
- Broad `--root` → allow **with a cross-platform stderr warning** (POSIX `/`+home, Windows drive-root+`C:\Users`).
- Temp-match transparency note ships **now** (R-4), stderr-only.

## Artifacts (all under this folder)

`eng-lead-implementation-plan.md`, `red-lead-scope-and-attack-plan.md`, `red-vuln-findings.md`, `eng-reviewer-gate-report.md`, `adv-s0{01,02,03,04,07,10,11,12,13}-*.md`, `adv-s014-tournament-score.md`, `adv-tournament-plan.md`, `BUG-010-ast-project-root.md` (the entity).

## Next action on resume

1. Confirm the owner's remediation direction (A vs B above).
2. Route the fix through eng-backend (test-first) → red-team re-check → eng-reviewer + adversary re-score to ≥ 0.92 → then push to PR #341.

---

## Note on Path Literals

Cross-platform path forms referenced above (analysis literals, not hardcoded paths):

```text
/, /home, /Users, C:\Users
```
