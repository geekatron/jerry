# Iteration-007 Remediation Notes — OWNER-FIRST (post-score 0.83)

> Scope: remediate ONLY the 4 panel-VERIFIED Critical findings from
> `adversary/iteration-007/s-014-quality-score.md`. Anti-bloat doctrine binding —
> every fix is wording/disclosure only; zero new lint, file, field, or subsystem.
> The 3 REFUTED Criticals (PM-001, CV-001, FM-003-i7fmea) and all Major/Minor
> claims are out of scope per instruction (they carry no weight).

## Navigation

| Section | Purpose |
|---------|---------|
| [Verified Findings In Scope](#verified-findings-in-scope) | The 4 panel-verified Criticals |
| [Change Log](#change-log) | Per-finding edits, file+line, before/after intent |
| [Anti-Bloat Attestation](#anti-bloat-attestation) | No-new-machinery confirmation |
| [Out Of Scope](#out-of-scope) | Refuted/unweighted claims not touched |

## Verified Findings In Scope

| Finding ID | Strategy | Verdict | Dimension | One-line fix |
|---|---|---|---|---|
| FM-001-i7fmea | S-012 FMEA | VERIFIED 3/3 | Evidence / Internal Consistency | Disclose that in-place redaction edits only current file text, not git history; true secret removal needs a separate history rewrite (in tension with squash-avoidance) |
| RT-001-20260706-iter7 | S-001 Red Team | VERIFIED 2/3 | Internal Consistency | Reconcile "the one sanctioned edit to a sealed entry" — there are TWO (redaction; `Superseded by:` status pointer); name both at the L1.4 canonical row and drop "the one" elsewhere |
| DA-001-iter7 | S-002 Devil's Advocate | VERIFIED 2/3 | Methodological Rigor / Internal Consistency | Correct near-cap id-minting formula in all 3 locations: next id = segment starting id (from Segment-Index row) + `grep -c` count, not the bare file-local count |
| FM-002-i7fmea | S-012 FMEA | VERIFIED 2/3 | Completeness | Name git-worktree/branch divergence as a 4th scope-boundary category + a never-discard-a-hunk merge/renumber rule |

## Change Log

12 edits across 4 deliverable files. All wording/disclosure only.

| # | File (repo-relative) | Location | Finding(s) | Change intent |
|---|---|---|---|---|
| 1 | `design/feedback-decision-log-convention-design.md` | L1.4 "Sealed segments" row | RT-001 | Canonical reconciliation: "Exactly two edits are sanctioned" — names both status pointer and redaction (was: "the one sanctioned edit … is a status pointer", omitting redaction) |
| 2 | `design/feedback-decision-log-convention-design.md` | L1.1 redaction carve-out | RT-001 + FM-001 | "one of the two sanctioned … edits" (was "the *one sanctioned*"); "one of the two sanctioned edits to sealed-segment immutability" (was "the one exception"); added git-history disclosure (in-place redaction edits current text only; pre-redaction commit keeps secret; true removal needs history rewrite in tension with squash-avoidance) |
| 3 | `design/feedback-decision-log-convention-design.md` | L1.2 DEC-LLM reversal | RT-001 | "one of the two sanctioned edits" (was "the one sanctioned edit") |
| 4 | `design/feedback-decision-log-convention-design.md` | L1.4 "Cap" row | DA-001 | Corrected near-cap id-minting formula: next id = segment starting id (Segment-Index row) + `grep -c` count; explained bare count is file-local; offered heading-Read alternative |
| 5 | `design/feedback-decision-log-convention-design.md` | L1.1 scope-boundary bullet | FM-002 | Added 4th category: git-worktree/branch divergence (silent-loss failure signature, no id gap) + never-discard-a-hunk merge/renumber rule |
| 6 | `design/staging-feedback-logs/feedback-decision-logs-standards.md` | LOG-M-002 | RT-001 + FM-001 | "one of the two sanctioned edits" + git-history disclosure clause |
| 7 | `design/staging-feedback-logs/feedback-decision-logs-standards.md` | LOG-M-005 | FM-002 | Named git-worktree/branch case as undefended + on-conflict renumber-not-discard rule |
| 8 | `design/staging-feedback-logs/feedback-decision-logs-standards.md` | LOG-M-006 | DA-001 | Corrected near-cap formula (segment starting id + count; offset required after first segment) |
| 9 | `design/staging-feedback-logs/feedback-decision-logs-standards.md` | Corrections bullet | RT-001 | "one of the two sanctioned edits … the other is an in-place hygiene redaction" |
| 10 | `design/staging-feedback-logs/feedback-decision-logs-standards.md` | Reversal/supersession bullet | RT-001 | "one of the two sanctioned edits … the other is an in-place hygiene redaction" |
| 11 | `design/staging-feedback-logs/examples-appendix.md` | "editing by hand" common case | DA-001 | Corrected near-cap formula (segment starting id + count) |
| 12 | `design/staging-feedback-logs/LLM-DECISION-LOG.template.md` | Reversal/supersession bullet | RT-001 | "one of the two sanctioned edits … the other is an in-place hygiene redaction" |

**Deliberate non-edit (P-022 transparency):** the design-doc v7 changelog entry (line 349) retains its past-tense "redaction is the one sanctioned edit to a sealed entry" phrasing. It was **not** in RT-001-iter7's cited evidence list (which named the six normative locations above), it is a historical point-in-time record of the iteration-5 remediation rationale, and the verified defect vector (the L1.1→L1.4 cross-reference a verifying reader follows) does not pass through the changelog. Rewriting a historical changelog entry would misrepresent the record and add churn against the anti-bloat doctrine. The now-authoritative L1.4 definition ("exactly two sanctioned edits") governs.

## Anti-Bloat Attestation

- **Zero new machinery.** No new lint check, file, field, schema element, subsystem, or hook was added. The L5 lint count remains ≤3; the id/alias scheme, rotation mechanics, and file set are unchanged.
- Every edit is a wording/disclosure change to existing prose, consistent with the package's established 7-round remediation pattern.
- The FM-002 conflict rule is documentation-only, in the same register as the existing rotation procedure (design L1.4 Steps 1–4); the optional future CI check for leftover conflict markers named by the finder was **not** adopted (anti-bloat).
- The DA-001 fix reuses the already-referenced Segment Index and the existing `grep -c` parity tool; no new tooling.
- All finding-ID cross-references preserved; new reconciliations tagged with their verified finding IDs (`RT-001-iter7`, `FM-001-i7fmea`, `DA-001-iter7`, `FM-002-i7fmea`).

## Out Of Scope

- **PM-001 / CV-001-20260706T0000** (REFUTED, factual lens): the "8 no-suffix entries" adoption-plan claim was grammatically scoped and re-counted as still exactly accurate; no defect. Not touched.
- **FM-003-i7fmea** (REFUTED 1/3): clone-depth precondition — the CI-wired L5 lints are pure-text; clone depth does not affect enforcement. Not touched.
- **All Major/Minor claims** (RT-002/003/004, DA-002/003/004, PM-002/003, SM-001/002/003, CC-001/002/003, IN-001/002/003, FM-004-i7fmea): no weight this round per instruction. Not touched.
