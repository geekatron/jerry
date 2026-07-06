# Factual-Accuracy Refutation Panel — S-012 FMEA (iteration-007)

> Lens: **factual** — does the defect exist at the cited lines in the CURRENT deliverable files? Misreadings, stale refs, or restatements of already-disclosed residuals / RESTORE dispositions are REFUTED. Default REFUTED if uncertain.
> Target: `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-012-findings.md`
> Scope: all 3 Critical findings (FM-004-i7fmea is Major — out of scope for this panel per task instructions).

## FM-001-i7fmea — Redaction is a working-tree edit; git history keeps the secret forever

**VERDICT: VERIFIED**

Citations check out against current text: design doc `feedback-decision-log-convention-design.md:65` contains, verbatim, both quoted clauses ("Because the redaction is the *one sanctioned*... presence, not veracity..." and "Redaction is irreversible in the repo, and that transcript carries the same unenforced-retention / cross-machine-portability dependency already disclosed for Q1..."); rule file `staging-feedback-logs/feedback-decision-logs-standards.md:24` (LOG-M-002) contains the identical "Redaction is irreversible in the repo; its only recovery path is the out-of-repo transcript..." clause; design doc line 197 contains the quoted squash/rewrite-avoidance caveat. A repo-wide grep of all 6 staged files for `history|secret|redact` (design doc, rule file, both templates, appendix, hook-design-note) surfaces no passage disclosing that an in-place redaction of an already-sealed/committed entry leaves the pre-redaction commit fully readable via `git log -p`/`git show` — every located passage addresses only the inverse direction (losing recoverability of a false-positive redaction via the out-of-repo transcript). This is not a restatement of any RESTORE-closed Critical (RT-001 was about redaction category/size scrutiny, a different defect) nor of any Revision Changelog entry (v1–v9 reviewed; no entry names git-history retention of a leaked secret). The underlying git mechanic asserted (an in-place edit does not remove an earlier commit's blob from history absent a rewrite) is standard and consistent with the design's own squash-avoidance stance at line 197.

## FM-002-i7fmea — Single-writer scope boundary omits git-worktree/branch divergence as a 4th undefended category

**VERDICT: VERIFIED**

Design doc `feedback-decision-log-convention-design.md:79` quotes exactly as cited ("Scope boundary (what this does NOT cover)... Two independent top-level sessions... a detached `background: true` task... or a direct human hand-edit... undefended by this convention and invisible to lint 2"), and line 78 discusses the P-003 orchestrator-serialization mitigation as described. A grep for `worktree` across all 6 staged files (design doc + 5 staging files) returns zero matches, confirming the claimed omission. `agent-development-standards.md` (loaded project context) independently confirms `isolation: worktree` is a real, official frontmatter capability, supporting the finding's premise that background-task worktree dispatch is an actual framework mechanism, not a hypothetical. The failure-mode distinction drawn (asynchronous branch divergence reconciled by merge/rebase, vs. the disclosed live same-inode last-write-wins race) is a genuine structural difference from the already-disclosed "concurrent same-machine writers" residual (Non-Findings list, design L1.1/LOG-M-005), so this is not a restatement of that disclosed item, nor of any RESTORE-closed Critical.

## FM-003-i7fmea — Tamper-evidence backstop names two preconditions; clone depth is an unstated third

**VERDICT: VERIFIED**

Design doc line 63 and line 197 quote exactly as cited (confirmed against current file text, including the literal "two preconditions: (a)... and (b)..." enumeration at line 197), and line 254 (Adoption plan, install step 3) matches the cited "implement and wire the ≤3 L5 lint checks into the existing CI/lint pipeline... wired AND required (branch-protected)" language. A grep across all 6 staged files for `clone depth|fetch-depth|shallow` returns zero matches, confirming clone/checkout depth is genuinely never named as a precondition anywhere in the package. This is a distinct gap from the previously-added "commit granularity" precondition (v5 changelog, RT-002) — that precondition addresses same-commit-window edits, not checkout depth — so this is not a restatement of a disclosed residual or RESTORE disposition. The underlying technical premise (a `fetch-depth: 1` shallow clone, the `actions/checkout` default, cannot diff against history it does not hold locally) is accurate.

## Summary Table

| ID | Verdict | Basis |
|----|---------|-------|
| FM-001-i7fmea | VERIFIED | Citations (L65, rule L24, L197) accurate; git-history-retention-after-redaction gap confirmed absent from all 6 files; not a restatement of RT-001 or any changelog entry |
| FM-002-i7fmea | VERIFIED | Citation (L79, L78) accurate; "worktree" absent from all 6 files (grep-confirmed); `isolation: worktree` capability independently confirmed; distinct failure signature from disclosed live-clobber residual |
| FM-003-i7fmea | VERIFIED | Citations (L63, L197, L254) accurate; "two preconditions" literal enumeration confirmed; clone-depth/shallow-clone gap absent from all 6 files (grep-confirmed); distinct from the already-disclosed commit-granularity precondition |
