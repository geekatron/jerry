# Refutation Panel: S-012 FMEA Findings (Materiality Lens) — Iteration 007

> **Panel role:** adv-executor (blind refutation pass), materiality lens.
> **Target:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-012-findings.md`
> **Question per Critical:** does it genuinely block one of the convention's four purposes — feedback/decisions never lost, operator-burden-free capture, navigable growth, honest metadata? Default REFUTED if uncertain; improbable edge cases and style-only points REFUTED even if technically true.
> **Constitutional:** P-003 no subagents. P-020 draft-only (no writes outside `projects/`). P-022 file+line citations; inference labeled.

## Navigation

| Section | Purpose |
|---------|---------|
| [Verdicts Summary](#verdicts-summary) | Quick table |
| [FM-001-i7fmea](#fm-001-i7fmea-verified) | Redaction-vs-git-history |
| [FM-002-i7fmea](#fm-002-i7fmea-verified) | Worktree/branch divergence |
| [FM-003-i7fmea](#fm-003-i7fmea-refuted) | Clone-depth precondition |

## Verdicts Summary

| Finding | Verdict | One-line reason |
|---|---|---|
| FM-001-i7fmea | **VERIFIED** | Redaction is explicitly framed as the sanctioned edit to an already-*sealed* (i.e., already-committed) entry, yet no text discloses that the pre-redaction commit remains readable in git history — a genuine, materially relevant "honest metadata" gap for the design's own public-repo hygiene mandate. |
| FM-002-i7fmea | **VERIFIED** | The Scope-boundary bullet's three named undefended categories all assume a single shared working copy (live clobber); git-worktree/branch divergence (a real, framework-advertised capability, and this very review's own operating mode) produces an asynchronous, silently-loseable merge failure mode that is not named and not covered by the existing wording. |
| FM-003-i7fmea | **REFUTED** | Conflates the CI-wired L5 lint (three pure-text checks — nav table, id integrity, terminal evidence — none requires a git diff or any commit history) with the separate, human-performed "diff backstop" tamper-evidence practice; the mechanism actually wired into CI does not depend on clone depth at all, so the claimed break does not occur in the artifact's actual enforcement path. |

---

## FM-001-i7fmea: VERIFIED

**Citations:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:65` ("Because the redaction is the *one sanctioned*, lower-scrutiny edit to a sealed entry..." and "**This is the one exception to sealed-segment immutability (L1.4):** the unredacted original is never the log's job to keep..."); `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:24` (LOG-M-002: "Redaction is irreversible in the repo; its only recovery path is the out-of-repo transcript..."); design doc L1.4 sealed-segments row, `.../feedback-decision-log-convention-design.md:197` ("a squash-merge or history rewrite can collapse the per-edit tamper-evidence trail, so treat log files as squash-exempt where the workflow allows").

**Assessment:** Line 65's own wording confirms redaction targets an already-*sealed* entry — i.e., an entry that has already been rotated into an immutable-by-convention segment and, in ordinary operation, already committed one or more times over. This is not an improbable edge case grafted on by the reviewer; it is the design's own stated primary use case for the carve-out. Neither line 65 nor LOG-M-002 (line 24) discloses that the "redacted in place" edit only rewrites the current file text — the commit(s) that introduced the plaintext secret remain fully readable via ordinary `git log -p`/`git show` on that path. The design's own squash/history-rewrite-avoidance stance for these files (line 197, kept specifically for tamper-evidence) stands in real, undisclosed tension with the one operation that would actually purge a leaked secret. Given the design's own installation path targets a framework repo with public-repo hygiene obligations (design doc install step, `.../feedback-decision-log-convention-design.md:254`), an operator relying on the "redacted in place" language as a safety claim would be misled about whether a previously-committed secret is actually gone. This genuinely bears on "honest metadata" (the integrity claim is incomplete) and is not resolved by the design's separate, more general "hygiene must precede capture, not follow a leak" advice, which speaks to workflow ordering, not to what happens to history once a leak has already occurred.

---

## FM-002-i7fmea: VERIFIED

**Citations:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:79` (Scope-boundary bullet: "Two independent top-level sessions on the same project (e.g. two terminal windows), a detached `background: true` task that outlives its orchestrator's turn, or a **direct human hand-edit**... all bypass the orchestrator append path and remain a full last-write-wins race"); confirmed via grep that "worktree" does not appear anywhere in `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` or in `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/`.

**Assessment:** All three named categories in the Scope-boundary bullet describe processes racing on the *same* working copy at the *same* time (a live, simultaneous last-write-wins clobber). Git-worktree/branch isolation is a structurally different, framework-advertised capability (`isolation: worktree` is an official Claude Code agent-definition field per `.context/rules/agent-development-standards.md`, and this very review process is itself executing from a worktree checkout, confirming the pattern is in active use, not hypothetical). Two worktrees on two branches do not clobber a shared inode; they diverge asynchronously and are reconciled later by merge/rebase. A naive conflict resolution (accepting one side wholesale) discards the other branch's appended entries with no trailing gap and nothing for the contiguity/id-integrity lint to catch — a materially worse and *silent* variant of "never lost," and not covered by the existing "two terminal windows" wording, which presumes a single shared working directory. This is not an improbable edge case: worktree-per-branch is a documented, supported multi-session pattern in this same framework, and the omission is real (confirmed by grep, not merely asserted).

---

## FM-003-i7fmea: REFUTED

**Citations:** `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:78-85` (L5 Lint section: three checks — "Nav table + cap" (line 81), "Id integrity" (line 82), "Terminal evidence" (line 83) — each is described as operating on the current file text; none references git diff, git log, or commit history); design doc L1.4 sealed-segments row, `.../feedback-decision-log-convention-design.md:197` (the "diff backstop... two preconditions" language, describing a *separate*, human/manual tamper-evidence review practice, not the automated L5 lint); design doc install step, `.../feedback-decision-log-convention-design.md:254` (names the ≤3 L5 lint checks — id integrity, cap detection, terminal evidence — as what gets wired into CI, explicitly not "tamper-evidence via diff").

**Assessment:** The finding treats the CI job that will run the L5 lint as if it were also the mechanism providing "diff backstop" tamper-evidence, and argues a shallow clone in that job silently breaks the integrity claim. But per `feedback-decision-logs-standards.md:78-85`, the three L5 checks that actually get wired into CI are pure-text parses of the current file (nav-table presence, id uniqueness/monotonicity/contiguity, terminal-disposition evidence-presence) — none of them performs or requires a `git diff`/`git log` operation, so clone depth is irrelevant to whether they pass or fail. The "diff backstop" tamper-evidence claim (design doc line 63/197) is a separate, human-driven review practice (a reviewer noticing a reworded sealed entry as a reviewable diff), which in practice is exercised through full-history views (a hosting platform's PR/commit diff view, or an operator's own full local clone) rather than through the specific CI job's local shallow checkout. The design's own install-step language (line 254) names only the three enumerated lint checks as what CI enforces, confirming the tamper-evidence "diff backstop" and the CI-wired L5 lint are not the same mechanism operating in the same shallow-clone context. Because the actual automated, CI-enforced path this convention ships is unaffected by clone depth, the claimed break in "honest metadata" does not materially occur in the artifact's real enforcement surface — this is a conflation of two distinct integrity mechanisms rather than a genuine gap.

---

## Execution Notes

- Only the target S-012 findings file, the two named design/staging deliverables, and `restore-notes.md` were read, per instructions; no other panel outputs were consulted.
- All citations above are repo-relative paths with line numbers, verified directly against current file content (no employer-internal tokens, no absolute `[home]/` paths recorded in this deliverable).
