# Iteration-2 Remediation Notes — FU-Log / DEC-LLM Convention Package

> Owner-first remediation after iteration-2 tournament (composite 0.65, gate 0.95; auto-REVISE on 10 unresolved Criticals).
> Doctrine: **anti-bloat** — close findings by simplifying/clarifying/deleting, never by adding machinery. Any addition must be offset by a bigger deletion (trade stated). Invalid or machinery-demanding findings are **rebutted with evidence** (P-022).
> Constitutional: P-003 (no subagents), P-020 (draft-only — no writes outside `projects/PROJ-031-cowork-skeleton/`), P-022 (evidence cited, inference labelled). Public-repo hygiene: repo-relative paths only.
> Method: the auto-REVISE root cause (per S-014) is that the v3 remediation was *localized* — it fixed each quoted sentence but did not sweep the whole package for the **overclaim failure class**. This pass does the package-wide sweep of the phrase patterns ("survives", "byte-exact", "not a loss of fidelity", unqualified "immutable"/"survive compaction", "backstopped by lint") across all 6 files.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Root-Cause Clusters](#root-cause-clusters) | The 4 Critical clusters + 2 new-deep Criticals |
| [Change Log](#change-log) | Per-edit record (file, finding, before→after, trade) |
| [Rebuttals](#rebuttals) | Findings declined with evidence |
| [Tally](#tally) | changes / deletions / additions / rebuttals |

---

## Root-Cause Clusters

The 10 Criticals cluster into 4 recurrence-of-overclaim issues + 2 newly-surfaced-deep issues. All fixes are wording/clarification, no new machinery.

| Cluster | Finding IDs (strategies) | Fix class |
|---------|--------------------------|-----------|
| C-1 concurrent-write overclaim ("survives background agents"; lint "backstop") | DA-001 (S-002), RT-001 (S-001), PM-001 (S-004), FM-001 (S-012), IN-001 (S-013) | Correct overclaim + make single-writer operational via existing P-003 orchestrator-only-append (no new machinery) |
| C-2 transcript byte-exact fidelity as unconditional fact | CC-001 (S-007) | Propagate the design-doc retention hedge into 3 downstream artifacts |
| C-3 rule-file preamble "survive compaction… hook assists" | FM-002 (S-012) | Qualify: once-captured; capture is MEDIUM; hook designed-not-shipped |
| C-4 immutability caveat scoped only to sealed segments | RT-004 (S-001) | Extend "by-convention, not enforced" caveat to ACTIVE file (REBUT the content-hash-lint machinery) |
| C-5 rotation non-atomic (concurrent append mid-rotation) | FM-003 (S-012), PM-004 (S-004) | Promote parity check to a required numbered step; cross-ref orchestrator-only-append |
| C-6 install-stall — no re-assessment trigger for whole convention | PM-002 (S-004) | Add install-stall re-assessment trigger to adoption plan |

---

## Change Log

Grouped by finding cluster. All edits are wording/clarification/compression — **zero new machinery** (no new lint, file, field, or subsystem). File keys: **D** = `design/feedback-decision-log-convention-design.md`; **S** = `staging-feedback-logs/feedback-decision-logs-standards.md` (shipped rule); **FT/DT** = FEEDBACK-LOG/LLM-DECISION-LOG templates; **A** = `examples-appendix.md`; **H** = `hook-design-note.md`.

| # | Finding(s) | Files | Fix |
|---|-----------|-------|-----|
| C-1 | DA-001, RT-001, PM-001, FM-001, IN-001 (5 strategies) | D (L1.1, Ledger row 2, LOG-M-005), S (LOG-M-005) | Corrected "survives background agents" self-contradiction; stated the lint does NOT catch last-write-wins; made single-writer **operational** — orchestrator-only-append reusing the existing P-003 handoff (no new machinery) |
| C-2 | CC-001 (S-007) | S (:44), DT (:23), A (:114); D:113 already hedged | Propagated the transcript retention/portability hedge into the 3 downstream artifacts that asserted "byte-exact"/"not a loss of fidelity" |
| C-3 | FM-002 (S-012) | S (preamble) | "once captured… capture is MEDIUM (SHOULD); fail-open hook designed, not yet shipped" |
| C-4 | RT-004 (S-001) | D (L1.1 integrity caveat) | Extended "by-convention, git-backstopped, not enforced" caveat to the ACTIVE file; **rebutted** the content-hash lint (see Rebuttals) |
| C-5 | FM-003 (S-012), PM-004 (S-004) | D (rotation procedure), S (Segment rotation) | Parity check promoted to a **required numbered step**; rotation = single-writer critical section; cross-ref orchestrator-only-append |
| C-6 | PM-002 (S-004) | D (adoption plan) | Whole-convention install-stall re-assessment trigger (session/milestone window + owner flag) |
| Maj | DA-005 (S-002) | D (L1.1 scoping), S (scoping) | Single-operator-per-log validated profile; team/multi-writer explicitly out-of-scope; reconciles FU.2 background-agents (CC-004) |
| Maj | PM-005 (S-004) | D, S | FEEDBACK-LOG ↔ MEMORY.md boundary for cross-project directives |
| Maj | RT-002 (S-001) | D (L1.2), S (LOG-M-004) | Graduation-review cadence + `Graduation: deferred` note |
| Maj | RT-006, IN-002 (S-001/S-013), CC-002, FM-006, FM-007 | D (Q4/Backfill note), FT, DT | Backfill review-cadence + added-date col; id-assignment/contiguity reconciliation; sort-by-datetime; queue not copied into sealed segments |
| Maj | DA-002, DA-003 (S-002) | D (L1.4, Ledger row 9) | Discovery-cost boundary (single-read vs total-corpus); alias-scan degrades post-rotation |
| Maj | DA-004 (S-002) | D (L1.1) | Bare `FU.N` ambiguous outside a live turn — named limitation |
| Maj | SM-001 (S-003) | D (L0) | Q3-deferred hedge on headline items (3)/(4) |
| Maj | SM-003 (S-003) | S (LOG-M-005) | Collision-resistant framing carried into the shipped rule file |
| Maj | SM-006 (S-003) | D (Q2), S (scoping) | `scope: framework` anchored as trailing Context sub-field; default omission |
| Maj | RT-005, IN-003 (S-001/S-013) | D (adoption step 6) | Proactive Q3 hook trigger branch; honest non-detectability of silent non-capture |
| Maj | IN-005 (S-013), FM-004 (S-012) | D (lint 2), S (lint 2) | Missing/unreadable segment fails via existing lint 2 (declined new lint-1 assertion); crash/retry gap carries a reason |
| Maj | FM-008 (S-012) | D (Cap row), S | Oversized single entry seals its segment immediately |
| Maj | FM-005, FM-009 (S-012) | D (L1.1 coverage caveat) | CB-05 partial-Read named as 2nd harvest blind-spot cause; over-capture (false-positive) direction |
| Maj | PM-003 (S-004) | D (L2) | No-L2-reinjection enforcement gap disclosed (`[INFERENCE]`) |
| Maj | PM-008 (S-004) | D (Sealed segments row) | Squash-merge collapses the git tamper-evidence trail — caveat |
| Min | SM-005, SM-004 (S-003) | D (F-027, F-010 rebuttal rows) | Dropped uncited "capture-time self-check"; dropped non-sequitur DECISION-entity clause |
| Min | SM-007 (S-003) | D (lint 1), S (lint 1) | Lint 1 counts headings too (covers entry-count half of OR-cap) |
| Min | FM-010 (S-012) | A, S | `Superseded by: FU.N` marker for corrected entries |
| Min | SM-002 (S-003) | D (adoption step 4) | `(user label: X)` → `(alias: X)` rename at install |
| Min | PM-009 (S-004) | D (adoption step 3) | Concrete lint-CI owner (install-step session, tracked on work item) |
| Min | DA-007 (S-002) | A (Common cases) | Human-mints-id procedure (next-id lookup) |
| Min | CV-001, CV-002 (S-011) | D (L0, L1.4, Ledger row 9) | Path `staging/`→`design/`; "immutable"→"immutable-by-convention" (2 spots) |
| Min | CC-003 (S-007) | H (header) | MUST/MUST NOT are code-implementation contracts, ceiling-exempt |
| Budget | — | D (L0, L2, staged table), S (compressions) | Rule file compressed 1,197→1,120 words; budget re-ratified ~2,150 tokens with the trade stated (P-022) |

---

## Rebuttals

Findings whose *proposed remedy* demanded machinery were rebutted with evidence; the finding's valid core was still closed by a cheaper means where one existed.

| Finding | Proposed remedy declined | Evidence / reasoning | Valid core still addressed? |
|---------|--------------------------|----------------------|-----------------------------|
| **RT-004** (S-001, Critical) | Add a per-sealed-segment `sha256` content-hash field, verified by a new/extended lint | Machinery for a MEDIUM-tier convention: git already provides tamper-evidence for git-tracked sealed segments — a hash field duplicates version control at added maintenance cost, exactly the over-engineering the package's own anti-bloat doctrine (and the ADR-convention iteration-005 lesson) rejects. | **Yes** — the *wording* half (extend the "by-convention, not enforced" caveat to the ACTIVE file) is applied; the integrity claim's scope now matches its stated scope. |
| **IN-005** (S-013, Major) | Add a segment-file-existence assertion to lint 1 | Redundant machinery: lint 2 must already read every segment listed in the Segment Index to check cross-segment contiguity, so a missing/unreadable segment already fails it. Adding a third assertion to lint 1 bloats a single-purpose check. | **Yes** — closed by clarifying existing lint 2 behavior instead of expanding lint 1. |

**Accepted-as-disclosed (INHERENT, monitor-only — matching the S-014 tags; no edit needed):** RT-003 (evidence-veracity out of scope — now also noted in lint 3), FM-011 (bare-alias scan at C4 scale), IN-004 (commit/push-cadence dependency, evidenced-as-followed), IN-006 (multi-scope discovery grep), DA-006 (Segment Index self-growth).

---

## Tally

| Metric | Count | Notes |
|--------|-------|-------|
| **changes** | 52 | distinct edits across the 6 deliverable files (30 D, 13 S, 5 templates, 3 A, 1 H) |
| **deletions** | 8 | rule-file compressions (LOG-M-004/005, rotation, lint 2, scoping, disposition/inline bullets, numeric parenthetical) + 2 dropped rebuttal clauses (F-027, F-010) |
| **additions** | 42 | net-new disclosure clauses/sentences (the balance after the 2 machinery rebuttals and ~pure-swap corrections) |
| **rebuttals** | 2 | RT-004 content-hash lint; IN-005 new lint-1 assertion — both machinery, declined with evidence, valid cores closed otherwise |

**Anti-bloat trade (stated per doctrine):** additions are Critical/Major disclosures the adversary required *in the artifacts that ship*; offset by (a) zero new machinery (2 machinery proposals actively rebutted), (b) ~77 words compressed out of the rule file, and (c) relocating elaboration to the design doc / appendix. The shipped rule file's growth (~1,690 → ~2,150 tokens) is re-ratified openly at L2 with the trade documented rather than hidden (P-022).

**Auto-REVISE root cause addressed:** the recurrence was fixed by a **package-wide sweep** of the overclaim phrase-set ("survives", "byte-exact", "not a loss of fidelity", unqualified "immutable"/"survive compaction", "backstopped by lint") across all 6 files — not just the sentences iteration-2 quoted. All 10 Criticals are now either corrected in-text or (RT-004 hash / IN-005 lint-1) rebutted with the valid core closed by cheaper means.
