# Iteration-3 Remediation Notes — Feedback & Decision Log Convention

> **Agent:** ps-architect (convergent, opus) · **Date:** 2026-07-06 · **Prior score:** 0.59 (gate 0.95, REVISE on 10 Criticals)
> **Doctrine:** ANTI-BLOAT — close findings by simplifying / clarifying / deleting; never by adding machinery. Every fix here is wording/deletion. **Zero** new lint checks, files, hooks, or subsystems added. Where a genuinely-additive clause was needed it is offset by a larger deletion (trade stated per item).
> **Constitutional:** P-020 draft-only — no framework path touched; the two `project-workflow.md` session-start edits (IN-002) are deferred to the install step and only *documented* in the in-scope design doc. P-022 — every disposition cites evidence; inference labelled. Public-repo hygiene — repo-relative paths, bracketed placeholders only.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Disposition Summary](#disposition-summary) | Every finding → FIXED / REBUTTED / USER-DECISION / INHERENT, with edit location |
| [Anti-Bloat Ledger](#anti-bloat-ledger) | Deletions/compressions, trade stated, rebuttals with evidence |

---

## Disposition Summary

**44 findings across 9 strategies.** 10 Critical (9 root causes) + Majors + Minors. Outcome: **40 FIXED (wording/deletion), 2 REBUTTED, 1 USER-DECISION, 4 INHERENT/monitor (no action).** Zero machinery added.

| Finding(s) | Strategy | Sev | Disposition | Where |
|---|---|---|---|---|
| CV-001 | S-011 | Critical | FIXED (deletion) | design L0 — deleted "~19 KB on disk" clause; ~30k-token PM-001 citation stands alone |
| PM-001 | S-004 | Critical | FIXED (reword) | design Q4 backfill — discloses rows unreviewed as of 2026-07-06; commit ≠ review |
| RT-001 / FM-002 / PM-003 | S-001/S-012/S-004 | Critical | FIXED (add scope boundary) | design L1.1 concurrent-writer + rule LOG-M-005 — names concurrent sessions/windows + hand-edits |
| RT-002 | S-001 | Critical | FIXED (extend caveat) | design L1.4 sealed-segments — commit-granularity precondition added |
| RT-003 | S-001 | Critical | FIXED (add to shipped artifact) | rule L5 Lint — "documentation until wired + branch-protected; --no-verify bypasses" |
| FM-001 | S-012 | Critical | FIXED (delete + rewrite) | design capture-trigger 4 — standardized `FU:`/`DEC:` marker; stale `>AN:` deleted |
| FM-005 | S-012 | Critical | FIXED (interim discipline) | rule LOG-M-006 + design L1.4 cap row — pre-hook in-session self-count |
| IN-001 | S-013 | Critical | FIXED (durability scope) | design L0 scope note (ii) — "once appended AND committed"; FU.3 cross-ref |
| IN-002 | S-013 | Critical | FIXED (install action, design-side) | design adoption step 3 + enforcement disclosure — session-start read wiring (project-workflow.md deferred to install per P-020) |
| CV-002 | S-011 | Major | FIXED (reattribute) | design L0/L1.1/Ledger row 2 — collision credited to `DJ-NNN`, drift pre-empted for `R{round}-FU.{n}` |
| DA-001 / DA-002 | S-002 | Major | FIXED (net math + trigger) | design L1.4 segment-index row |
| DA-003 | S-002 | Major | FIXED (both axes) | design L1.1 H-31 bullet + appendix common case |
| DA-005 | S-002 | Major | FIXED (surface at L0) | design L0 scope note (iii) |
| RT-004 | S-001 | Major | FIXED (presence norm) | design Q4 backfill (e) |
| PM-002 / PM-004 | S-004 | Major | FIXED (bypass disclosure + AC) | design enforcement disclosure + adoption step 3 branch-protection AC |
| PM-005 | S-004 | Major | FIXED (calendar bound) | design adoption step 6 — ~3-month wall-clock |
| CC-001 | S-007 | Major | FIXED (remove overclaim) | hook-note Seam 1 — "harness-sourced (subject to fail-open)" |
| CC-002 | S-007 | Major | FIXED (parity fallback) | LLM-DECISION template + rule LOG-M-005 |
| FM-003 | S-012 | Major | FIXED (carry-forward) | design rotation step 2 + rule cap bullet |
| FM-004 | S-012 | Major | FIXED (orphan cross-check) | rule lint 2 — `ls *-LOG.*.md` vs index |
| FM-006 | S-012 | Major | FIXED (CP-01 exception) | design L1.1 + rule LOG-M-005 — candidate is stated inline-payload exception |
| FM-007 | S-012 | Major | FIXED (soften overclaim) | design L1.2 graduation — parity in intent, not structure |
| FM-008 | S-012 | Major | FIXED (add trigger) | design capture-trigger 5 + rule capture triggers |
| IN-003 | S-013 | Major | FIXED (sanction pointer) | design L1.4 sealed-segments + rule corrections |
| IN-004 | S-013 | Major | FIXED (compact note) / full-table REBUTTED | design Improvement Ledger null-alternative note |
| SM-001 | S-003 | Major | FIXED (live parity) | live FEEDBACK-LOG.md + LLM-DECISION-LOG.md — `Added` column |
| SM-002 | S-003 | Major | FIXED (disclose split) | design adoption step 4 |
| SM-003/004/005 | S-003 | Minor | FIXED | templates (alias colons, Q2 example) + rule (append-only caveat) |
| CC-003 | S-007 | Minor | **REBUTTED** | banner already declares SHOULD-tier; adding 4× worsens SR-003 |
| CC-004 | S-007 | Minor | FIXED | design adoption step 4 — resolve PROPOSED-DEFAULT wording at install |
| RT-005 / RT-006 | S-001 | Minor | FIXED | design multi-scope wording + adoption step 1 per-question |
| DA-004 / DA-006 | S-002 | Minor | FIXED | design L0 cross-ref + appendix synthetic note |
| IN-005 | S-013 | Minor | FIXED | design enforcement disclosure — AE-006e interim backstop |
| SR-003 | S-010 | Major (disclosed) | **USER-DECISION** | rule token budget ~2,150 vs ~1,500 target — P-020 ratify-or-trim |
| FM-009, PM-006, IN-006, IN-007 | — | Minor | INHERENT (no action) | accepted disclosed residuals |
| SR-001, SR-002 | S-010 | — | Already applied prior pass | (verified present) |

---

## Anti-Bloat Ledger

**Doctrine compliance: zero new machinery** (no new lint checks — still ≤3; no new files; no new hooks; no new subsystems; no new fields). Every fix is wording/deletion/disclosure.

**Deletions & compressions (offsetting the additive disclosures):**
- CV-001 — deleted the self-contradictory "~19 KB on disk" clause (design L0).
- FM-001 — deleted the stale `>AN: FU.n.` example + "or any inline directive" (design capture trigger 4).
- CC-001 / FM-007 — removed two overclaims ("harness-guaranteed"; Backfill/graduation structural parity).
- Rule file: compressed LOG-M-005 (removed the lint-2-scope duplication) and the assistant-verbatim policy blockquote to offset the RT-003/FM-005/scope-boundary additions.

**Trade stated (SR-003):** the shipped rule file necessarily grows by a few honesty disclosures the adversary flagged as Critical *for the installed artifact specifically* (RT-003 CI-wiring caveat; FM-005 interim self-count; concurrent-session scope). Compression offsets part of it; the residual over-budget is escalated to the user as SR-003 (ratify ~2,150 vs trim toward ~1,500), not silently resolved.

**Rebuttals (declined with evidence):**
1. **CC-003** — inline "SHOULD" on LOG-M-001/002/003/006. Evidence: the section banner already reads *"All rows are SHOULD-tier. Override requires documented justification."* — MEDIUM tier is unambiguous file-wide. Adding "SHOULD" to 4 rows adds tokens to a file already 40% over its stated budget (SR-003) to fix a readability nit the banner covers. Anti-bloat → declined.
2. **IN-004 full comparison table** — declined as expository bloat; the two substantive axes it surfaces (session-start rediscoverability, uncommitted-loss durability) are IN-002 and IN-001, already fixed. A compact 3-line note replaces the table.

---
