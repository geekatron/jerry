# FMEA Report: Feedback & Decision Log Convention (iteration 3)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory) | Decomposition (Step 1) |
| [Findings Table](#findings-table) | All FM-NNN findings, RPN-ranked |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Header

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (blind, iteration 3)
**H-16 Compliance:** S-003 Steelman is not a direct S-012 prerequisite (H-16 names S-002/S-004/S-001); the C3+ sequence context confirms prior Steelman/critique rounds (iterations 1-2 already ran a full tournament — see design doc Revision Changelog v3/v4).
**Blind protocol:** No file under `adversary/` (other rounds' outputs) was read except this iteration's own output path. Findings are original to this pass; overlap with iteration 1/2 vocabulary (RT-/DA-/PM-/FM-/IN-/CC-/SM-/SR-/CV-) is coincidental convergence on the same artifact, not copied from prior reports.
**Elements Analyzed:** 10 | **Failure Modes Identified:** 9 | **Total RPN:** 1,881

---

## Summary

Two prior remediation rounds (v3, v4 per the design doc's own changelog) closed a large number of Critical/Major findings, and the package's MEDIUM-tier, anti-bloat posture is accepted as valid per the engagement brief (descoped-with-disclosure is not itself a defect). This pass finds the remediation is **incomplete in one directly falsifiable way** (FM-001: the design doc's own capture-trigger prose was never updated to match the standardized inline-marker fix it claims, in its own changelog, to have already made — an overclaim, not a disclosed trade) plus **two additional undetectable-by-design silent-failure paths** in the concurrency/rotation machinery that the existing disclosures do not fully cover (FM-002 multi-session concurrency scope gap, FM-005 no in-session rotation-cap detection). Five further Major findings identify unspecified or overstated mechanics (Backfill Queue at rotation, Segment Index omission, the P-003-handoff verbatim-payload claim, graduation-tracking parity claim, and an un-propagated capture-trigger insight). Recommendation: **REVISE** — all nine findings are closeable by wording/cross-reference fixes consistent with the project's own anti-bloat doctrine; none requires new machinery.

---

## Element Inventory

| ID | Element | Description |
|----|---------|-------------|
| E1 | Entry creation — chat channel | LOG-M-001 capture triggers 1-3; design doc capture-trigger list |
| E2 | Entry creation — inline-doc channel | Capture trigger 4; inline marker convention (`FU:`/`DEC:`) |
| E3 | Alias/canonical id mapping | LOG-M-005; FU.N / DEC-LLM-NNN logger-assigned ids |
| E4 | Rotation trigger / cap detection | LOG-M-006; lint check 1 (~50 entries / ~800 lines) |
| E5 | Rotation procedure / segment linking | L1.4 4-step rotation procedure; prev/next header |
| E6 | Segment Index | ACTIVE-file-only id-range table; lint check 2 |
| E7 | Cross-log navigation | Canonical-id-as-join-key between FEEDBACK-LOG and LLM-DECISION-LOG |
| E8 | Backfill | Backfill Queue mechanics, promotion, chronology |
| E9 | Multi-session / concurrent-writer handling | LOG-M-005 single-writer discipline; P-003 orchestrator-worker handoff |
| E10 | Graduation | LOG-M-004; DEC-NNN/ADR boundary; `Reflected in:` field |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-20260706-iter3 | E2 | Design doc capture-trigger #4 retains pre-fix ambiguous inline marker (`>AN: FU.n. …`, "or any inline directive") that directly contradicts the standardized `FU:`/`DEC:` marker shipped in the rule file + both templates + appendix, and contradicts the changelog's own claim that this ambiguity (F-015) was closed | 8 | 10 | 6 | 480 | Critical | Rewrite design doc line ~83 to cite the standardized `FU:`/`DEC:` marker; delete "or any inline directive" | Internal Consistency |
| FM-005-20260706-iter3 | E4 | Cap-crossing detection is commit/CI-lint-only; no in-session mechanism (until Q3 hook ships) prompts rotation mid-session, so a long uncommitted session can silently re-exceed the read-window/truncation limit the cap exists to prevent | 7 | 5 | 7 | 245 | Critical | Add one sentence to LOG-M-006 / the template instructing the model to self-count entries/lines each turn as a MEDIUM-tier interim discipline until Q3 ships | Methodological Rigor |
| FM-002-20260706-iter3 | E9 | "Single-writer-per-log" (LOG-M-005) is achieved only *within* one orchestrating context; the disclosed "concurrent-writer residual risk" text does not scope out (or in) the case of the same single operator running two independent top-level sessions against the same project — the orchestrator-only-append mitigation has no reach across sessions | 8 | 4 | 8 | 256 | Critical | Add an explicit disclosure: the single-writer mitigation is scoped to one live orchestrating session; concurrent top-level sessions on the same log are an undefended residual risk requiring the operator not to do this | Internal Consistency |
| FM-006-20260706-iter3 | E9 | Claim that "workers return feedback/decision candidates via the existing P-003 orchestrator-worker handoff" is unreconciled with CP-01 ("file paths only in handoffs, NEVER inline content") and the handoff-v2 schema, which has no field for a verbatim feedback/decision candidate payload | 6 | 5 | 6 | 180 | Major | Either specify a path-based candidate-file convention consistent with CP-01, or explicitly except feedback/decision candidates from CP-01 with a stated rationale | Actionability |
| FM-007-20260706-iter3 | E10 | Claim that ungraduated hardened decisions are "tracked in the same way the Backfill Queue tracks pre-log items" overstates parity: the Backfill Queue is a discrete reviewable table; graduation tracking is only an inline per-entry `Reflected in:` field with no consolidated list | 5 | 6 | 6 | 180 | Major | Either add a lightweight Graduation queue/marker convention (e.g., `grep`-able `Reflected in: —`) or soften the parity claim | Traceability |
| FM-008-20260706-iter3 | E1 | The interrogative/challenge-question capture-trigger category (validated by the real FU.9 entry, per hook-design-note.md's own admission) was folded into the future hook's reminder heuristics (Seam 2) but never propagated back into LOG-M-001 / the design doc's manual capture-trigger enumeration that governs capture today | 6 | 5 | 6 | 180 | Major | Add "poses a challenging question implying feedback" as a fifth manual capture trigger in both the design doc and the rule file | Completeness |
| FM-003-20260706-iter3 | E8 | Rotation procedure (L1.4 step 1) explicitly excludes the Backfill Queue from being copied into the sealed segment but never states it is carried forward into the new ACTIVE file, leaving the fate of pending backfill candidates at a rotation event unspecified | 6 | 4 | 7 | 168 | Major | Add a fifth rotation step: "carry forward any unresolved Backfill Queue rows into the new ACTIVE file" | Completeness |
| FM-004-20260706-iter3 | E6 | Lint check 2 (id integrity/contiguity) only reads segments *listed* in the Segment Index; an existing sealed segment file that was never added to the index during manual re-seeding is invisible to the check, silently orphaning its ids from validation and cross-log-navigation resolution | 7 | 3 | 8 | 168 | Major | Add a cross-check: lint 2 also enumerates segment files on disk (`ls FEEDBACK-LOG.*.md`) and flags any not present in the index | Methodological Rigor |
| FM-009-20260706-iter3 | E8 | Backfill Queue "sort by Context `datetime`, not canonical id" chronology guidance has no supporting tooling; purely a manual-reading convention | 2 | 4 | 3 | 24 | Minor | Note as an accepted anti-bloat trade; no action required | Traceability |

---

## Finding Details

### FM-001-20260706-iter3: Design doc capture-trigger prose contradicts the shipped inline-marker standard

| Attribute | Value |
|-----------|-------|
| **Element** | E2 — Entry creation, inline-doc channel |
| **S / O / D / RPN** | 8 / 10 / 6 / 480 |
| **Severity** | Critical |

**Evidence:** `design/feedback-decision-log-convention-design.md` (L1.1 "Capture triggers" list, item 4): *"Annotates a document inline with feedback (e.g. `>AN: FU.n. …`, review comments, or any inline directive)."* Compare `design/staging-feedback-logs/feedback-decision-logs-standards.md` ("FEEDBACK-LOG" section): *"Inline marker: a line beginning `FU:` / `DEC:`."* and `design/staging-feedback-logs/FEEDBACK-LOG.template.md` (Log Conventions): *"annotate any document with a line beginning `FU:` (or `DEC:` for a decision)."* The design doc's own Revision Changelog / UX Findings Disposition table lists F-015 ("inline-doc annotation syntax not standardized... ambiguity + silent failure," severity 3) as **FOLD**ed via "Standardize ONE inline marker (`FU:` / `DEC:` line, optionally blockquoted); removes 'any inline directive' ambiguity."

**Analysis:** The design doc is the narrative source-of-truth that the rule file and templates are staged from; a reader consulting the design doc's own capture-trigger section will encounter the *pre-fix* ambiguous syntax the changelog claims was removed. This is a direct, verifiable overclaim — the artifact set is not internally consistent about which inline-marker convention is canonical. Per the engagement brief, overclaimed coverage is Critical regardless of the package's otherwise-valid minimal posture.

**Corrective Action:** Replace the item-4 bullet with: *"Annotates a document inline with the standardized `FU:` / `DEC:` marker (see L1's inline marker convention). When the assistant reads a doc containing such a marker, it SHOULD harvest it into the log with `source: inline-doc` + path + line."* Delete the `>AN: FU.n.` example and "or any inline directive" language.

**Acceptance Criteria:** Design doc, rule file, both templates, and appendix all cite the identical single inline-marker syntax with no remaining reference to the pre-fix multi-format language.

**Post-Correction RPN estimate:** ~40 (S=4 residual documentation-hygiene risk, O=2, D=5).

---

### FM-005-20260706-iter3: No in-session rotation-cap detection until commit/CI lint runs

| Attribute | Value |
|-----------|-------|
| **Element** | E4 — Rotation trigger / cap detection |
| **S / O / D / RPN** | 7 / 5 / 7 / 245 |
| **Severity** | Critical |

**Evidence:** `feedback-decision-logs-standards.md` ("L5 Lint" item 1): the cap-crossing check is one of the "≤3" lint checks, explicitly described as running at "commit/CI time" (design doc L2, "Enforcement-layer disclosure"). `hook-design-note.md` Seam 3 (segment-cap reminder) is explicitly a **PROPOSED-DEFAULT, not yet shipped** (Q3). The design doc's own commit-cadence cue (FU.3, "milestone / workflow / phase boundaries") is not "every N entries" — commits can be infrequent relative to entry volume in a single long working session.

**Analysis:** The cap (~50 entries / ~800 lines) exists specifically to stay under the ~2,000-line Read window and the observed ~25k-token truncation point (PM-001, cited in the design doc's own L1.4). Until the Q3 hook ships, the *only* mechanism that detects a cap crossing is a lint that runs at commit/CI time — there is no instruction anywhere (design doc, rule file, or templates) telling the model to self-monitor the running entry/line count *during* a session and proactively propose rotation before the next commit. A single long session could therefore add entries 51-100+ with the file silently exceeding its designed safety margin, for the entire duration of that session — recreating, in miniature and mid-session, exactly the truncation failure FU.5 was built to prevent.

**Corrective Action:** Add one MEDIUM-tier sentence to LOG-M-006 (rule file) and the FEEDBACK-LOG/LLM-DECISION-LOG templates: *"Until the Q3 hook ships, the assistant SHOULD self-count entries/lines in the ACTIVE file each time it appends, and proactively propose rotation on approaching the cap, rather than relying solely on the commit-time lint."* No new machinery — a discipline addition, consistent with the anti-bloat doctrine.

**Acceptance Criteria:** LOG-M-006 explicitly states the interim (pre-hook) in-session self-check obligation.

**Post-Correction RPN estimate:** ~70 (S=7, O=2, D=5 — self-check remains model-executed, not harness-guaranteed, until Q3 ships).

---

### FM-002-20260706-iter3: Multi-session concurrency scope gap in the single-writer mitigation

| Attribute | Value |
|-----------|-------|
| **Element** | E9 — Multi-session / concurrent-writer handling |
| **S / O / D / RPN** | 8 / 4 / 8 / 256 |
| **Severity** | Critical |

**Evidence:** `feedback-decision-log-convention-design.md` (L1.1, "Concurrent-writer residual risk" bullet): *"Two writers appending to the *same* log file (e.g. parallel/background agents) can race... Making it operational (no new machinery): appends happen only in the orchestrating/main context; worker and background agents return feedback/decision *candidates* via the existing P-003 orchestrator-worker handoff, and the orchestrator serializes the append. A single writer cannot race itself..."* Compare the "Adoption profile" bullet: *"validated for a **single operator per log** with a continuously-mediating assistant **session**"* (singular).

**Analysis:** The stated mitigation ("a single writer cannot race itself") is scoped to workers/background agents subordinate to *one* orchestrating context (P-003 single-level nesting). It does not — and structurally cannot — prevent a race between two independent *top-level* sessions (e.g., the same operator running Jerry in two terminal windows, or a detached `background: true` agent task per `agent-development-standards.md` that outlives the orchestrating session's turn boundary) both appending to the same `FEEDBACK-LOG.md`. The "Adoption profile" bullet's use of "a... session" (singular) implies this is out of scope, but the concurrent-writer disclosure's own example ("parallel/background agents") reads as if the single-writer discipline already covers all multi-writer cases, which it does not. The L5 lint's disclosed blind spot (last-write-wins produces a contiguous, valid-looking file with an entry silently gone) applies with full force here, and detection is effectively impossible without git-diff archaeology.

**Corrective Action:** Add an explicit sentence clarifying the boundary: *"This single-writer discipline holds only within one live orchestrating session. Two independent top-level sessions (e.g., two terminals) appending to the same log concurrently are NOT covered by this mitigation and remain a full last-write-wins race; operators SHOULD NOT run concurrent sessions against the same project's logs."*

**Acceptance Criteria:** The scope boundary of the single-writer mitigation is stated affirmatively (what it does NOT cover), not left to be inferred from the word "a" in "a... session."

**Post-Correction RPN estimate:** ~96 (S=8, O=4, D=3 — disclosure does not eliminate the risk, but converts it from a silent to a *known/named* residual, consistent with the project's own disclosed-not-hidden practice elsewhere).

---

## Recommendations

Ordered by RPN (highest first). All are wording/cross-reference/one-sentence additions; none adds new lint checks, new files, or new subsystems, consistent with the package's stated anti-bloat doctrine.

1. **FM-001 (RPN 480, Critical):** Fix the design doc's stale inline-marker example; align it with the shipped `FU:`/`DEC:` standard.
2. **FM-002 (RPN 256, Critical):** Disclose the multi-session (not just multi-agent) concurrency boundary explicitly.
3. **FM-005 (RPN 245, Critical):** Add an interim in-session self-count discipline for rotation-cap detection pending the Q3 hook.
4. **FM-006 (RPN 180, Major):** Reconcile the P-003-handoff verbatim-candidate claim with CP-01 (file-paths-only handoffs).
5. **FM-007 (RPN 180, Major):** Soften or substantiate the Backfill-Queue/graduation-tracking parity claim.
6. **FM-008 (RPN 180, Major):** Propagate the interrogative-capture-trigger insight from the hook design note into the governing manual rule (LOG-M-001) and design doc.
7. **FM-003 (RPN 168, Major):** Specify Backfill Queue carry-forward across rotation.
8. **FM-004 (RPN 168, Major):** Extend lint check 2 to catch segments present on disk but absent from the Segment Index.
9. **FM-009 (RPN 24, Minor):** No action required; accepted anti-bloat trade.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-003 (backfill carry-forward unspecified), FM-008 (capture-trigger enumeration incomplete relative to its own evidence) |
| Internal Consistency | 0.20 | Negative | FM-001 (direct design-doc/rule-file contradiction, an overclaim of a closed finding), FM-002 (mitigation-scope vs. disclosure-text mismatch) |
| Methodological Rigor | 0.20 | Negative | FM-005 (no interim self-check discipline despite the cap's stated rationale), FM-004 (lint 2's one-directional blind spot) |
| Evidence Quality | 0.15 | Neutral | Findings and prior remediation both cite specific evidence; no new evidence-quality gap identified this pass |
| Actionability | 0.15 | Negative | FM-006 (handoff mechanics for verbatim candidates left unspecified, blocking a concrete implementation step) |
| Traceability | 0.10 | Negative | FM-007 (graduation-tracking claims a traceability mechanism that is not structurally present) |

---

*Strategy: S-012 FMEA | Elements: 10 | Findings: 9 (3 Critical, 5 Major, 1 Minor) | Total RPN: 1,881*
*Blind protocol observed: no prior-iteration adversary output read.*
