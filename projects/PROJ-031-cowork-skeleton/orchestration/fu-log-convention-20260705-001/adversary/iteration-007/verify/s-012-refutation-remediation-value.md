# S-012 Refutation Panel — Remediation-Value Lens (iteration-007)

**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-012-findings.md`
**Lens:** remediation-value — would fixing the Critical materially change adoption outcomes, or is it churn? Fixes that add machinery against the package's own anti-bloat doctrine are refuted on sight.
**Scope:** the 3 Criticals only (FM-001-i7fmea, FM-002-i7fmea, FM-003-i7fmea). FM-004-i7fmea is Major and out of scope for this panel.
**Method:** read the target findings file, the current deliverable text it cites, and `restore-notes.md` only (blind protocol — no other iteration-007 panel output read).

## Verdicts

### FM-001-i7fmea — Redaction is a working-tree edit; git history keeps the secret forever — **VERIFIED**

The existing disclosure at `design/feedback-decision-log-convention-design.md:65` ("hygiene must precede capture, not follow a leak") and `:65`/`design/staging-feedback-logs/feedback-decision-logs-standards.md:24` ("Redaction is irreversible in the repo... a false-positive redaction of non-secret text can become permanently unrecoverable") both address the *false-positive* direction (legitimate text lost) and a general precedence philosophy, but neither states the inverse, more consequential fact: once a **real** secret is captured verbatim (the LOG-M-002 default) and later "redacted in place" on an already-sealed/committed entry, the prior commit's plaintext remains fully readable via ordinary `git log -p`/`git show` — redaction never touches history, only the current file text. This is a distinct risk direction from what is disclosed, not a restatement, and the fix is a genuine one-clause addition (no lint/field/subsystem), consistent with the package's own established closure pattern. Given this project's own stated public-repo hygiene practice and the package's target of at least one public repo, this gap has real consequence if left unstated, so the fix has material remediation value.

### FM-002-i7fmea — Single-writer scope boundary omits git-worktree divergence as a 4th category — **REFUTED**

`design/feedback-decision-log-convention-design.md:78` ("The scheme is collision-resistant, not collision-proof") and `:101` ("Team / multi-writer adoption is an explicit out-of-scope extension — a multi-writer project would need a coordination rule beyond the current post-hoc lint; that machinery is deliberately not built for an unstated requirement") already give the reader the operative bottom line directly and unambiguously: any writer path beyond the single orchestrating session is undefended and out of scope, full stop. Naming git-worktree divergence as one more specific illustrative sub-case, plus generic merge-conflict-resolution advice ("never discard a conflicting hunk") that applies to any append-only file under parallel branches, does not change that already-stated posture or a reader's behavior — it is an additional example inside an already-disclosed, open-ended "undefended if multi-writer" umbrella, added to a rule file the design doc itself flags as ~52% over its own soft token target (`design/feedback-decision-log-convention-design.md:220`). This is churn against the remediation-value bar, not a closure of a materially new gap.

### FM-003-i7fmea — Clone depth as an unstated third tamper-evidence precondition — **REFUTED**

The finding ties its Critical severity to "the exact CI system this design proposes wiring its own L5 lint into" (`design/feedback-decision-log-convention-design.md:254`), but the three L5 lint checks it is describing (`design/feedback-decision-log-convention-design.md:235-237`, restated at `design/staging-feedback-logs/feedback-decision-logs-standards.md:81-83`: nav-table+cap, id-integrity/contiguity, terminal-evidence-presence) are pure-text checks over the current file content only — none of them performs a `git diff` or reads prior commits, so none depends on clone depth to run correctly. The separate "git-backstopped" tamper-evidence claim at `design/feedback-decision-log-convention-design.md:63` and the two-preconditions caveat at `:197` describe a human/PR-review practice, which on GitHub is served by the server's full history regardless of any individual reviewer's local clone depth. The finding conflates these two distinct mechanisms; its central evidentiary link (CI-wired lint => clone-depth risk) does not hold, which undercuts both the Critical severity and the remediation value of the proposed fix — it would disclose a precondition against a mechanism (the lint) that was never actually gated by it.

## Summary Table

| ID | Verdict | Primary basis |
|----|---------|---------------|
| FM-001-i7fmea | VERIFIED | Distinct, non-restated risk direction (true-positive secret survives in history); low-cost disclosure fix; real public-repo consequence |
| FM-002-i7fmea | REFUTED | Already covered by explicit "multi-writer out of scope / collision-resistant not collision-proof" disclaimer; added example is churn against anti-bloat budget |
| FM-003-i7fmea | REFUTED | Conflates the pure-text L5 lint (clone-depth-independent) with the separate human/PR-review diff-backstop mechanism; evidentiary tie-in to CI wiring is a non-sequitur |
