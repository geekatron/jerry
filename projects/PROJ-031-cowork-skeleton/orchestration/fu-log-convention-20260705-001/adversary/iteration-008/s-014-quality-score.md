# Quality Score Report: Feedback & Decision Log Convention Package (FU-Log / DEC-LLM) — Iteration 8, VERIFIED-CRITICALS Protocol

## Navigation

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, one-line assessment |
| [Scoring Context](#scoring-context) | Inputs, criticality, gates, protocol |
| [Score Summary](#score-summary) | Composite (both protocols), thresholds, verdict |
| [Verification Roll-Up](#verification-roll-up) | Per-Critical panel disposition, 2-of-3 rule |
| [Dimension Scores](#dimension-scores) | Per-dimension weighted table (verified protocol) |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement path per dimension |
| [Critical Findings Disposition](#critical-findings-disposition) | Auto-REVISE check against VERIFIED Criticals only |
| [Old-Protocol Composite (Transparency)](#old-protocol-composite-transparency) | Score if all raw claims counted, unfiltered |
| [Delta Reconciliation vs. Iteration 6](#delta-reconciliation-vs-iteration-6) | Why the composite moved from 0.460 |
| [Improvement Recommendations](#improvement-recommendations-priority-ordered) | Priority-ordered fix list |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency self-audit |

---

## L0 Executive Summary

**Score:** 0.72/1.00 | **Verdict:** REVISE | **Weakest Dimensions:** Completeness and Internal Consistency (tied, 0.66)
**One-line assessment:** After 8 remediation rounds — including a RESTORE pass that independently re-verified zero regressions on all 6 iteration-006 Criticals and added a user-requested visual layer (FU.10) — the package rebounded sharply from iteration-006's 0.46 (ESCALATE), but 6 newly-verified Criticals (all narrow, wording-only fixes, none requiring new machinery) still block the 0.95 engagement gate; one more targeted pass should clear them.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + all 5 files in `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/` (`feedback-decision-logs-standards.md`, `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md`, `examples-appendix.md`, `hook-design-note.md`)
- **Deliverable Type:** Design (multi-file Jerry convention: design doc + MEDIUM-tier rule draft + 2 templates + examples appendix + hook design note), post iteration-7 RESTORE pass (v9)
- **Criticality Level:** C4 (engagement gate 0.95, user-set); SSOT default H-13 threshold 0.92
- **Scoring Strategy:** S-014 (LLM-as-Judge), SSOT 6-dimension weighted composite, iteration 8, **VERIFIED-CRITICALS protocol**
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Protocol:** Automatic-REVISE fires only on **VERIFIED** Criticals (2-of-3 refutation-panel majority across factual / materiality / remediation-value lenses). Refuted findings and re-derived disclosed residuals carry **no weight**. Unrefuted Majors are **advisory only** (informative, non-blocking).
- **Inputs Read:** design doc (full, 363 lines), all 5 staging files (full), 8 iteration-008 adversary reports (S-001, S-002, S-003, S-004, S-007, S-011, S-012, S-013), 18 verification-panel files under `adversary/iteration-008/verify/` (factual / materiality / remediation-value lenses × 4 Critical-bearing reports: S-001, S-002, S-004, S-012), `adversary/iteration-007/restore-notes.md` (RESTORE disposition record), `adversary/iteration-006/s-014-quality-score.md` (delta reconciliation baseline)
- **Scored:** 2026-07-06

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite (VERIFIED-CRITICALS protocol)** | **0.72** |
| **Composite, old (unfiltered) protocol — transparency only** | 0.51 |
| **Engagement Gate (user-set)** | 0.95 — **NOT MET** |
| **SSOT Default Threshold (H-13)** | 0.92 — **NOT MET** |
| **Operational Band (quality-enforcement.md)** | 0.70–0.84 → REVISE (significant gaps, focused revision needed) |
| **Verdict** | **REVISE** |
| **Prior Iteration (iteration-006) Composite** | 0.460 (ESCALATE) |
| **Delta vs. iteration-006** | **+0.260** |
| **Strategy Findings Incorporated** | Yes — 8 complete iteration-008 reports + 18 verification-panel files |
| **Verified Criticals (auto-REVISE trigger)** | **6** — DA-001-i8, DA-002-i8, PM-002-iter8, RT-001-20260706-iter8, FM-001-i008fmea, FM-002-i008fmea |
| **Refuted Criticals (no weight)** | **1** — PM-001-iter8 (0-of-3 panel lenses; independently re-identified as a restatement of iteration-003's already-closed FM-006) |

---

## Verification Roll-Up

Each Critical-bearing report (S-001, S-002, S-004, S-012) was run through a 3-lens refutation panel (factual accuracy / materiality / remediation-value). A Critical stands as VERIFIED only on 2-of-3 lens agreement.

| Finding | Report | Factual | Materiality | Remediation-Value | Panel Result | Disposition |
|---------|--------|---------|-------------|--------------------|--------------|--------------|
| RT-001-20260706-iter8 | S-001 Red Team | VERIFIED | REFUTED | VERIFIED | 2-of-3 | **VERIFIED** |
| DA-001-i8 | S-002 Devil's Advocate | VERIFIED | REFUTED | VERIFIED | 2-of-3 | **VERIFIED** |
| DA-002-i8 | S-002 Devil's Advocate | VERIFIED | VERIFIED | VERIFIED | 3-of-3 | **VERIFIED** |
| PM-001-iter8 | S-004 Pre-Mortem | REFUTED | REFUTED | REFUTED | 0-of-3 | **REFUTED** |
| PM-002-iter8 | S-004 Pre-Mortem | VERIFIED | REFUTED | VERIFIED | 2-of-3 | **VERIFIED** |
| FM-001-i008fmea | S-012 FMEA | VERIFIED | REFUTED | VERIFIED | 2-of-3 | **VERIFIED** |
| FM-002-i008fmea | S-012 FMEA | VERIFIED | REFUTED | VERIFIED | 2-of-3 | **VERIFIED** |

**Notable pattern:** 5 of the 6 surviving Criticals were refuted specifically on the **materiality** lens (i.e., an independent panel judged them narrow/edge-case/low-probability relative to the convention's four purpose pillars), yet all 5 still cleared the 2-of-3 bar because they are real (factually accurate) and genuinely worth fixing (positive remediation-value, zero new machinery). This is informative for scoring: these are real, evidenced gaps that block H-13's "unresolved Critical" rule, but they are materially narrower in practical impact than iteration-006's Criticals (which the iteration-6 scorer assessed as core-purpose-threatening without the benefit of a materiality panel). Only **DA-002-i8** (inline-doc dedup silently drops edited markers) cleared materiality unanimously — this is the single highest-severity surviving gap, as it directly falsifies the package's own "over-capture, never lost" claim (`feedback-decision-log-convention-design.md:91`).

**PM-001-iter8 refutation is itself a process-quality signal.** The factual-lens panel discovered that PM-001-iter8 restates a tension (CP-01 vs. the P-003 candidate-handoff exception) that was raised, closed, and re-verified as closed in **iterations 3, 7, and 8** (S-011 #13, S-001, S-007 of this same round) — i.e., a "genuinely new" Critical claim that, on independent verification, was not new at all. This validates the refutation-panel mechanism: without it, this restated finding would have inflated the Critical count and depressed the composite on a non-issue.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Prior (iter-6) | Delta | Evidence Summary |
|-----------|--------|-------|----------|-----------------|-------|-------------------|
| Completeness | 0.20 | 0.66 | 0.132 | 0.42 | +0.24 | Zero regression on all iter-6 Completeness fixes (dedup-check existence, install-stall bound); one high-materiality VERIFIED Critical (DA-002-i8: dedup silently drops edited markers) plus one lower-materiality VERIFIED Critical (PM-002-iter8: cap number absent from templates/live logs) |
| Internal Consistency | 0.20 | 0.66 | 0.132 | 0.30 | +0.36 | Weakest dimension for 6 straight iterations, now measurably improved: all 4 iter-6 Criticals here closed with zero regression (independently re-verified by every iteration-8 strategy); 3 new VERIFIED Criticals surfaced (DA-001-i8, RT-001-iter8, FM-001-i008fmea), but **all 3 were refuted on materiality** — real, evidenced, narrow gaps, not core-purpose-blocking |
| Methodological Rigor | 0.20 | 0.76 | 0.152 | 0.44 | +0.32 | No VERIFIED Critical targets this dimension; anti-bloat discipline sustained across 8 rounds (every fix wording-only, zero new lint/file/field/subsystem); advisory-only Majors (CC-001, IN-005, PM-004) note a mild recurring self-consistency-checking weakness in the remediation process itself |
| Evidence Quality | 0.15 | 0.74 | 0.111 | 0.56 | +0.18 | S-011 CoVe's 7th consecutive pass: zero fabrications, 22/24 claims verified/closed; one VERIFIED Critical (FM-002-i008fmea: dedup key format unspecified, zero worked examples), refuted on materiality as a documentation gap, not a Critical block |
| Actionability | 0.15 | 0.80 | 0.120 | 0.64 | +0.16 | No VERIFIED Critical targets this dimension directly; universal convergence across all 8 strategies on wording-only, zero-machinery remediation paths sustained for the 8th consecutive round — a genuine, stable strength |
| Traceability | 0.10 | 0.74 | 0.074 | 0.48 | +0.26 | No VERIFIED Critical targets this dimension directly; citation discipline remains very strong (every claim across 6 files carries file+line evidence); advisory-only Majors (DA-004-i8, CV-001-20260706-I8) note residual cross-scope/lint-attribution nits |
| **TOTAL** | **1.00** | | **0.721** (rounds to **0.72**) | **0.460** | **+0.260** | |

---

## Detailed Dimension Analysis

### Completeness (0.66/1.00)

**Evidence:**
Every iteration-006 Completeness fix (FM-001-i6 dedup-check existence, PM-002 install-stall concrete bound, RT-002 supersession marker parity) re-verified present and stable — zero regression found by any of the 8 iteration-008 strategies. The FU.10 visual layer (2 Mermaid diagrams: segment-rotation `flowchart`, entry-lifecycle `stateDiagram-v2`) directly closes the user's own FU.10 feedback ("massive walls of text") with zero new machinery — a genuine completeness win this round.

**Gaps (VERIFIED):**
- **[Critical, materiality-VERIFIED]** DA-002-i8: the FM-001 inline-doc dedup check keys purely on `source: inline-doc` `path:line/anchor` **location**, never on marker **content** (`feedback-decision-logs-standards.md:51`; `FEEDBACK-LOG.template.md:25`; `examples-appendix.md:169`). An operator editing a marker's text in place at the same line is silently treated as an already-logged duplicate and the update is never captured — a deterministic, mechanism-level drop, not a remembered-to-log failure, and one that directly falsifies the package's own "over-capture, never lost" framing (`feedback-decision-log-convention-design.md:91`). This is the single highest-materiality surviving gap in the package.
- **[Critical, materiality-REFUTED but VERIFIED overall]** PM-002-iter8: the segment-rotation cap ("~50 entries or ~800 lines") is stated only in the design doc (`:195`) and staged rule file (`feedback-decision-logs-standards.md:28`) — never in `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md`, or the live bootstrap `FEEDBACK-LOG.md`, confirmed by direct read. The materiality panel notes this is mitigated by the framework's existing SSOT-plus-pointer pattern (the template already cites `feedback-decision-logs-standards.md` as its SSOT) and by the interim self-count fallback already being in context once the rule file installs — but the fix (restate the number in the artifacts a session actually touches) is cheap and directly load-bearing for the self-count mechanism.

**Improvement Path:** Amend the FM-001 dedup rule (rule file, both templates, appendix) to key on `path:line/anchor` **and** marker text — skip only if both are unchanged, mint a new entry (optionally `Related: <old id>`) if content differs (zero new field/lint). Restate the numeric cap directly in both templates' Segment Index sections and both live bootstrap log files.

### Internal Consistency (0.66/1.00)

**Evidence:**
All 4 of iteration-006's Internal Consistency Criticals (RT-001-old redaction-laundering, DA-001-old/FM-006 "Four safety functions," PM-001/IN-001-old AE-006e miscite, FM-003-old verbatim-vs-split-entry) independently re-verified closed by every one of the 8 iteration-008 strategies with **zero regression** — a materially stronger result than any prior iteration's regression check, given this is now the dimension's 8th consecutive review.

**Gaps (VERIFIED, all refuted on materiality):**
- **[Critical]** DA-001-i8: the git-worktree/branch merge-conflict id-renumbering rule (`feedback-decision-log-convention-design.md:79`; `feedback-decision-logs-standards.md:27`) repairs only the renumbered entry's own outbound `Superseded by:`/`Related:` fields — not inbound external citations (an ADR's `Reflected in:`, a worktracker DECISION's `Source:`) — for the exact class of record (graduated/cross-linked) the "ids never reset" invariant (`:198`) exists to protect. Materiality panel: scoped to an explicitly out-of-scope (SHOULD NOT) multi-writer/worktree path, already substantively disclosed as a named residual.
- **[Critical]** RT-001-20260706-iter8: the background-agent "candidate" handoff pathway (`:78`, LOG-M-005) has no stated requirement that the candidate preserve the operator's unaltered words, creating a theoretical gap in the "verbatim is the fidelity anchor" guarantee. Materiality panel: the pathway is a race-avoidance mechanism (concurrent-append serialization), not the primary or an unguarded live-speech relay channel; the one concrete content-relay case (inline-doc marker) already carries an agent-agnostic verbatim rule (`:88`).
- **[Critical]** FM-001-i008fmea: the design doc's "Five safety functions" paragraph (`:264`, this round's own DA-001-old fix) claims lint 2 "detects" Segment-Index-overflow, contradicted by the rule file's own Scope-limits item (e) (`feedback-decision-logs-standards.md:85`), which states Segment Index display accuracy is unchecked — a fresh instance of the package's own recurring "claim contradicts an adjacent disclosure" class, introduced by the very fix that closed a different instance of it. Materiality panel: the design doc's own text (`:199`) already discloses the bounded, non-lossy real consequence ("no entry is lost, only the per-segment count drifts down") independent of lint attribution — a wording-precision issue, not a pillar-blocking one.

**Improvement Path:** Add an explicit disclosed-residual clause to the worktree-merge rule naming the external-citation-breakage risk for graduated ids (DA-001-i8). Add one clause requiring the candidate payload to quote the operator's text unaltered as a distinct sub-field (RT-001-i8). Replace the "detected by lint 2" clause in the design doc's "One shared dependency" paragraph with an accurate framing matching the rule file's own Scope-limits (e) disclosure (FM-001-i008fmea).

### Methodological Rigor (0.76/1.00)

**Evidence:**
No VERIFIED Critical targets this dimension. The anti-bloat doctrine remains genuinely and consistently applied across 8 rounds: every one of the 6 VERIFIED Criticals' proposed corrective actions is a wording/one-clause/one-example fix — zero new lint, file, field, or subsystem, confirmed independently by every remediation-value panel. The RESTORE pass (iteration-007) explicitly re-verified all 6 prior Criticals against current text before adding the FU.10 diagrams, evidencing disciplined process hygiene.

**Gaps (advisory only, no scoring weight per protocol, noted for completeness):**
- CC-001-i8 (S-007, Major, refuted-for-weight but methodologically informative): the shipped rule file's own near-cap id-minting shortcut (LOG-M-006) is not cross-referenced against its own Scope-limits (e) disclosure of unverified index accuracy — the same self-consistency-checking gap pattern as FM-001-i008fmea, suggesting the remediation process itself would benefit from a systematic "grep every cross-referenced disclosure at the point of every related claim" step before each tournament round, a structural question this package's own changelog (SM-002/CV-003, iteration 5) has repeatedly raised and not yet resolved.
- IN-005-20260706-iter008 (S-013, Major): the IN-003 fix's claim that the session-start rotation-recovery check "does not depend on the model remembering" is itself an overclaim — it relocates, rather than removes, the memory dependency.
- PM-004-iter8 (S-004, Major): the whole-convention install-stall trigger lacks the "second consecutive deferral flagged explicitly" pattern already applied to the graduation and Backfill Queue triggers.

**Improvement Path (advisory):** Cross-reference LOG-M-006's near-cap shortcut against Scope-limits (e); reword the IN-003 "does not depend on the model remembering" claim to accurately scope what changed; add the second-deferral escalation clause to the install-stall trigger.

### Evidence Quality (0.74/1.00)

**Evidence:**
S-011 (Chain-of-Verification) completed its 7th pass over this package: 24 claims extracted, 22 verified/closed/disclosed with zero fabrications, including re-confirmation of all 5 previously-flagged CV findings (iterations 5 and 6) as closed with zero regression. Citation discipline (file+line evidence for every claim, across all 8 iteration-008 reports and all 18 verification-panel files) remains a sustained, genuine strength.

**Gaps (VERIFIED, refuted on materiality):**
- **[Critical]** FM-002-i008fmea: the inline-doc dedup key (`path:line/anchor`) that closed the tournament's single highest-RPN historical Critical (FM-001-i6, RPN 336) has no defined canonical format (raw line number vs. heading anchor vs. concatenation is never disambiguated) and has **zero worked examples** anywhere in the 6-file package, despite the package's own FU.8 doctrine of embedding a worked example for every other mechanism. Materiality panel: the check is executed by LLM judgment, not byte-exact string matching, making cross-session drift an improbable edge case rather than a likely failure; the design's own over-capture doctrine (`:91`) classifies the worst case (a duplicate re-mint) as low-severity and self-correcting, not data loss — a documentation-completeness gap (Major-consistent), not a Critical block.

**Improvement Path:** Pick one canonical key form (recommend: path + nearest stable heading anchor, edit-stable vs. line-number drift) and add one worked example to `examples-appendix.md`'s Common Cases section.

### Actionability (0.80/1.00)

**Evidence:**
No VERIFIED Critical targets this dimension. Every one of the 6 VERIFIED Criticals carries an explicit, minimal, wording-only acceptance criterion, and all 3 remediation-value panels independently confirmed none of the proposed fixes add machinery against the anti-bloat doctrine — a genuine, sustained strength across 8 consecutive rounds of this tournament.

**Gaps (advisory only, no scoring weight):**
- DA-003-i8 (S-002, Major): H-31 bare-alias enumeration has no bound/fallback for candidate-list size at scale.
- FM-004-i008fmea (S-012, Major): the new FU.10 diagram omits the dedup gate and reopen path it sits directly above, with no caption disclosing it as a simplified per-entry view.

**Improvement Path (advisory):** Add a candidate-count threshold triggering a narrowing question before H-31 enumeration; add a one-line caption to the FU.10 rule-file diagram noting it is a simplified per-entry view.

### Traceability (0.74/1.00)

**Evidence:**
No VERIFIED Critical targets this dimension directly. Citation discipline remains strong: every finding across all 8 iteration-008 reports and all refutation panels cites exact file+line evidence, cross-checked against `iteration-007/restore-notes.md` and `.context/rules/quality-enforcement.md`/`agent-development-standards.md` SSOT sources.

**Gaps (advisory only, no scoring weight):**
- DA-004-i8 (S-002, Major): `Related: <id>` cross-log citations omit the `<scope>:FU.N` prefix the design itself defines, leaving cross-scope citation ambiguous.
- CV-001-20260706-I8 (S-011, Major): the design doc's "One shared dependency" paragraph misattributes the Segment-Index-overflow detection mechanism to lint 2 (same underlying defect as FM-001-i008fmea, independently found by a second strategy).
- DA-005-i8 (S-002, Minor): nav-table coverage for a growing log's per-entry headings is undefined.

**Improvement Path (advisory):** Require the `<scope>:FU.N` prefix for cross-scope `Related:` citations, or explicitly disclose intra-scope-only support; correct the lint-2 misattribution (shared fix with FM-001-i008fmea, Internal Consistency).

---

## Critical Findings Disposition

Per instruction, automatic-REVISE applies only to Criticals that survive the 2-of-3 verification panel. All 7 raw Critical claims from iteration-008's 8 strategy reports were independently run through 3-lens refutation panels (factual / materiality / remediation-value).

| Finding | Strategy | Root Cause | Panel Result | Triggers Auto-REVISE? |
|---------|----------|------------|--------------|------------------------|
| RT-001-20260706-iter8 | S-001 Red Team | Background-agent candidate handoff has no stated verbatim-fidelity requirement | 2-of-3 (materiality REFUTED) | **Yes** |
| DA-001-i8 | S-002 Devil's Advocate | Worktree/branch merge id-renumbering has no repair path for external (graduated) citations | 2-of-3 (materiality REFUTED) | **Yes** |
| DA-002-i8 | S-002 Devil's Advocate | FM-001 inline-doc dedup keys on location only; edited markers silently dropped | 3-of-3 | **Yes** |
| PM-001-iter8 | S-004 Pre-Mortem | CP-01 exception exists only in this package's own text, not the SSOT | 0-of-3 — **restates iteration-3's already-closed FM-006** | **No** |
| PM-002-iter8 | S-004 Pre-Mortem | Segment-rotation cap number absent from templates/live bootstrap logs | 2-of-3 (materiality REFUTED) | **Yes** |
| FM-001-i008fmea | S-012 FMEA | "Five safety functions" paragraph misattributes Segment-Index-overflow detection to lint 2 | 2-of-3 (materiality REFUTED) | **Yes** |
| FM-002-i008fmea | S-012 FMEA | Inline-doc dedup key format unspecified; zero worked examples in the package | 2-of-3 (materiality REFUTED) | **Yes** |

**Net:** 6 distinct VERIFIED Criticals trigger automatic-REVISE per H-13, independent of the 0.72 composite (itself below both the 0.92 SSOT default and the 0.95 engagement gate, landing in the "significant gaps" REVISE band 0.70–0.84).

---

## Old-Protocol Composite (Transparency)

Per instruction, this section reports what the composite would be if **all raw claims** across the 8 iteration-008 reports were counted at face value — i.e., without the 2-of-3 refutation-panel filter that this iteration's VERIFIED-CRITICALS protocol applies. This is reported for transparency, not as the operative score.

**Unfiltered raw findings (iteration-008, all 8 reports):** 7 Critical (RT-001, DA-001, DA-002, PM-001, PM-002, FM-001-i008fmea, FM-002-i008fmea), 11 Major (DA-003, DA-004, SM-001, SM-002, PM-003, PM-004, CC-001, CV-001, FM-003-i008fmea, FM-004-i008fmea, IN-005), 6 Minor (DA-005, SM-003, CC-002, CC-003, CV-002, IN-006).

Without the verification panel: (a) PM-001-iter8 stands as a face-value Critical (its restatement-of-FM-006 status is only discoverable via the panel's targeted cross-check of iteration-3's remediation-notes.md — a check the raw report itself does not perform), inflating Internal Consistency's raw Critical count to 4; (b) all 11 Majors and 6 Minors count at full (unfiltered) weight rather than as advisory-only signals, further depressing every dimension, especially Internal Consistency (CC-001, CV-001, IN-005, SM-001/SM-002 all land here) and Completeness (FM-003-i008fmea).

| Dimension | Weight | Old-protocol score | Weighted |
|-----------|--------|---------------------|----------|
| Completeness | 0.20 | 0.52 | 0.104 |
| Internal Consistency | 0.20 | 0.28 | 0.056 |
| Methodological Rigor | 0.20 | 0.58 | 0.116 |
| Evidence Quality | 0.15 | 0.56 | 0.084 |
| Actionability | 0.15 | 0.60 | 0.090 |
| Traceability | 0.10 | 0.62 | 0.062 |
| **TOTAL** | **1.00** | | **0.512** (rounds to **0.51**) |

**Reading:** The old-protocol composite (0.51) sits only modestly above iteration-006's 0.460 (delta +0.05) — consistent with a naive, unfiltered reading that would see "7 raw Criticals this round vs. 6 last round" and conclude the recurring-class problem has not improved. The **VERIFIED-CRITICALS protocol's own value is the +0.21 delta between 0.51 (old) and 0.72 (verified)**: it correctly discounts one restated non-issue (PM-001-iter8) and reclassifies 11 Majors + 6 Minors from blocking evidence to advisory signal, revealing that the substance of this round's genuine defects is narrower and lower-materiality than a raw count would suggest — while still correctly holding the gate closed via the 6 findings that remain genuinely unresolved.

---

## Delta Reconciliation vs. Iteration 6

| Dimension | Iter-6 | Iter-8 (verified) | Delta | What moved it |
|-----------|--------|---------------------|-------|----------------|
| Completeness | 0.42 | 0.66 | +0.24 | 2 of iter-6's Completeness Criticals (FM-001-i6, PM-002) closed with zero regression; FU.10 diagrams added. 2 new VERIFIED Criticals surfaced this round (DA-002-i8, PM-002-iter8 — same rule, new instance), one of which (DA-002-i8) is genuinely high-materiality, capping the improvement. |
| Internal Consistency | 0.30 | 0.66 | +0.36 | Largest single-dimension movement. All 4 iter-6 ICS Criticals closed with zero regression across every one of 8 strategies — an unprecedented consistency result for this historically weakest dimension. 3 new VERIFIED Criticals surfaced, but **all 3 were independently refuted on materiality** (narrow/edge-case, not core-purpose-blocking) — a qualitatively different, lower-severity crop than iter-6's Criticals (which included a security-adjacent integrity-laundering gap and a live-data-confirmed fidelity contradiction). |
| Methodological Rigor | 0.44 | 0.76 | +0.32 | No Critical this round (down from indirect iter-6 involvement); anti-bloat discipline sustained across an 8th round; RESTORE pass's explicit re-verification-before-addition process is itself evidence of improved rigor. |
| Evidence Quality | 0.56 | 0.74 | +0.18 | S-011's 7th pass: zero fabrications, all 5 prior CV findings closed with zero regression. One new VERIFIED Critical (FM-002-i008fmea) refuted on materiality as a documentation gap. |
| Actionability | 0.64 | 0.80 | +0.16 | No Critical this round; universal 8-round convergence on wording-only fixes, now a well-established, durable pattern rather than a single-round observation. |
| Traceability | 0.48 | 0.74 | +0.26 | No Critical this round; the CV-003 (rule-file `project:` tag) and RT-003 (alias-count) gaps from iteration 6 both independently re-verified closed with zero regression. |
| **Composite** | **0.460** | **0.721** | **+0.260** | Driven primarily by (1) a historically unprecedented zero-regression result across all 6 iteration-006 Criticals, independently confirmed by all 8 iteration-008 strategies; (2) the FU.10 visual layer closing a genuine user-facing completeness gap; (3) the VERIFIED-CRITICALS protocol correctly discounting 1 restated non-issue (PM-001-iter8) and reclassifying 11 Majors/6 Minors as advisory rather than blocking; (4) the surviving 6 Criticals being materially narrower in scope than iteration-006's — 5 of 6 failed the materiality bar even while clearing the 2-of-3 verification threshold. |

**Does this jump make sense given the same "6 Criticals" pattern persists?** Yes, with an important qualification. Iteration-6's report explicitly worried that a "recurring class" (claims contradicting adjacent disclosures) would keep producing fresh Critical-severity instances indefinitely without closing the systemic root cause. Iteration-8's evidence is mixed on this point: the class **did** produce 3 fresh Internal-Consistency instances this round (DA-001-i8, RT-001-iter8, FM-001-i008fmea) — so the systemic question iteration-5/6 raised is **not yet resolved**. However, unlike iteration-6, this round benefits from an independent materiality lens that found all 3 of these fresh instances narrower in practical impact than their iteration-6 predecessors, and the zero-regression track record on the *previously* closed instances is now an 8-round-deep, unprecedented result. The composite reflects both facts: real, durable progress (justifying the large upward movement) alongside a still-open systemic pattern (justifying why the composite remains well short of the 0.92/0.95 gates and the verdict remains REVISE, not PASS).

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation | Corroboration |
|----------|-----------|---------|--------|-----------------|----------------|
| 1 | Completeness | 0.66 | 0.90+ | Key the FM-001 inline-doc dedup check on `path:line/anchor` **and** marker text (skip only if both match); mint a new entry on content mismatch, optionally noting `Related: <old id>` | DA-002-i8 (VERIFIED, 3-of-3, highest-materiality surviving gap) |
| 2 | Internal Consistency | 0.66 | 0.90+ | Replace the design doc's "detected by lint 2's contiguity/orphan check" clause (One shared dependency, `:264`) with an accurate framing matching the rule file's own Scope-limits (e) disclosure | FM-001-i008fmea (VERIFIED) + CV-001-20260706-I8 (advisory, same defect, second strategy) |
| 3 | Internal Consistency | 0.66 | 0.90+ | Add one clause requiring the P-003 candidate payload to quote the operator's text unaltered as a distinct sub-field, appended by the orchestrator as the entry's Verbatim | RT-001-20260706-iter8 (VERIFIED) |
| 4 | Internal Consistency | 0.66 | 0.90+ | Add an explicit disclosed-residual clause to the worktree/branch merge-renumbering rule naming the external-citation-breakage risk for graduated (ADR/DECISION-cross-linked) ids | DA-001-i8 (VERIFIED) |
| 5 | Completeness | 0.66 | 0.90+ | Restate the numeric segment cap ("~50 entries or ~800 lines") directly in both templates' Segment Index sections and both live bootstrap log files | PM-002-iter8 (VERIFIED) |
| 6 | Evidence Quality | 0.74 | 0.90+ | Fix the inline-doc dedup key to one canonical, edit-stable form (path + nearest stable heading anchor) and add one worked example to `examples-appendix.md` | FM-002-i008fmea (VERIFIED) |
| 7 (advisory) | Methodological Rigor | 0.76 | 0.85+ | Cross-reference LOG-M-006's near-cap id-minting shortcut against the Scope-limits (e) disclosure it currently contradicts | CC-001-i8 (Major, advisory) |
| 8 (advisory) | Methodological Rigor | 0.76 | 0.85+ | Reword the IN-003 fix's "does not depend on the model remembering" claim to accurately scope what changed (relocates, not removes, the memory dependency) | IN-005-20260706-iter008 (Major, advisory) |
| 9 (process) | — | — | — | For the next tournament round, explicitly cross-check any "new" Critical claim against prior iterations' remediation-notes.md/restore-notes.md before scoring it as unresolved — PM-001-iter8's restatement of iteration-3's FM-006 would have inflated the Critical count without this check | Process observation, this scorer |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite (no dimension's score adjusted to match another).
- [x] Evidence documented for every score — each dimension analysis cites specific VERIFIED finding IDs with file+line evidence and the panel disposition that produced the 2-of-3 result.
- [x] Uncertain scores resolved with attention to materiality nuance, not blanket credit: Internal Consistency (0.66) reflects genuine, durable improvement (zero regression across 4 previously-closed Criticals, all-3-refuted-on-materiality for the 3 new ones) but was **not** raised further, because the dimension's 8-round recurring-class pattern (a fresh instance of "claim contradicts adjacent disclosure" every round) remains open and unresolved as a systemic question.
- [x] Completeness (0.66) was **not** raised to match Internal Consistency's evidence profile, because DA-002-i8 is the one surviving Critical that cleared materiality unanimously (3-of-3) — a genuinely high-severity, core-purpose-threatening gap, not a narrow edge case; anti-leniency requires this to weigh more heavily than the lower-materiality PM-002-iter8 in the same dimension.
- [x] The old-protocol composite (0.51) is reported alongside the verified composite (0.72) specifically to make the verification protocol's effect auditable, not to inflate the headline number — the +0.21 gap between them is attributed explicitly to (a) 1 restated non-issue correctly discounted and (b) 11 Majors + 6 Minors correctly reclassified as advisory, not to score-shopping.
- [x] No dimension scored above 0.80 (highest is Actionability at 0.80) — none approaches the 0.92+ "genuinely excellent" band, consistent with 6 unresolved Criticals still blocking H-13.
- [x] Automatic-REVISE rule applied per instruction: all 6 VERIFIED Criticals are unresolved in current package text and are not rebutted-with-evidence or disclosed-as-accepted-residual — REVISE is mandatory regardless of the 0.72 composite, and the composite (0.70–0.84 band) independently corroborates REVISE rather than PASS or ESCALATE.
- [x] Deliberate minimalism (MEDIUM-tier posture, ≤3 lint checks, anti-bloat doctrine) was judged valid design per instruction and was **not** penalized in any dimension.
- [x] Score < 0.50 ESCALATE special case does **not** apply this iteration (composite 0.72 well above 0.50); the sixth-consecutive-sub-0.50 pattern from iterations 5–6 has been broken by the RESTORE pass's zero-regression result — this is disclosed explicitly, not silently assumed to continue.

---

*Scored by adv-scorer (S-014 LLM-as-Judge) | Iteration 8, VERIFIED-CRITICALS protocol | Inputs: design doc + 5 staging files (6 files, full read), 8 complete iteration-008 adversary reports (S-001, S-002, S-003, S-004, S-007, S-011, S-012, S-013), 18 verification-panel files (`adversary/iteration-008/verify/`, 3 lenses × 4 Critical-bearing reports + 2 extra RT-001/PM-002-scoped files), `adversary/iteration-007/restore-notes.md`, `adversary/iteration-006/s-014-quality-score.md` (delta baseline) | Constitutional: P-003 no subagents invoked; P-020 draft-only, no framework paths touched, all output under `projects/PROJ-031-cowork-skeleton/`; P-022 all scores evidence-cited with finding IDs, panel dispositions, and file+line references; all paths reported repo-relative per public-repo hygiene instruction; no employer-internal references or absolute `[home]/` paths introduced into this report.*
