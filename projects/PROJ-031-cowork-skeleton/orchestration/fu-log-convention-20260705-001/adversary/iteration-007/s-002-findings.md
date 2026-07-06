# Devil's Advocate Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention (iteration-007, VERIFIED-CRITICALS)

> Strategy: S-002 Devil's Advocate. Criticality: C4. Gate: 0.95.
> H-16 check: S-003 (Steelman) output exists at `adversary/iteration-007/s-003-findings.md` (existence-only check per blind protocol; content not read). H-16 satisfied — proceeding.
> Blind protocol observed: no file under `adversary/iteration-007/` or `adversary/iteration-008/` was read except `restore-notes.md` (permitted) and this output.
> Scope discipline: findings below are restricted to defects not already disclosed anywhere in the six deliverable files, that plausibly block one of the four stated purposes (feedback/decisions never lost; operator-burden-free capture; navigable growth; honest metadata). The design's own six-round disclosure record is treated as authoritative — re-flagging an already-named residual is explicitly out of scope per the task brief.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverables, dates |
| [Summary](#summary) | Overall verdict |
| [Findings Table](#findings-table) | All findings, stable IDs |
| [Finding Details](#finding-details) | Full write-up per finding, with refutation-panel notes on the Critical |
| [Recommendations](#recommendations) | P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Execution Context

- **Strategy:** S-002 Devil's Advocate
- **Template:** `.context/templates/adversarial/s-002-devils-advocate.md`
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/FEEDBACK-LOG.template.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/LLM-DECISION-LOG.template.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/examples-appendix.md`
  - `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/hook-design-note.md`
- **Executed:** 2026-07-06
- **Reviewer:** adv-executor (S-002)
- **Attack angle (per assignment):** does the rotation/id/alias design survive real multi-session use? Is the lean posture hiding load-bearing gaps?

---

## Summary

Four counter-arguments identified (1 Critical, 2 Major, 1 Minor) — a smaller yield than prior rounds, consistent with six rounds of prior disclosure having already closed the shallow surface area. The one Critical is a genuine, previously-unflagged **correctness bug**, not a propagation/disclosure gap: the design's own "near-cap deterministic id-minting" shortcut (`grep -c` count as the next canonical id) is arithmetically wrong for every segment after the first, because it substitutes a local heading-count for a global heading-value with no stated offset correction — precisely in the id-uniqueness mechanism this whole convention exists to make more trustworthy than `[internal-kb]`'s `DJ-NNN` collision. This is the kind of thing a 3-lens refutation panel should stress-test hard, because it sits exactly on the design's most load-bearing claim (LOG-M-005, collision-resistant ids); I have tried to refute it myself below and it survives. The two Major findings concern asymmetric rigor (the read-side gap is asserted "closed" without the same hedging and hook-compensation the write-side gets everywhere else) and an under-specified recovery trigger (the interrupted-rotation detector has a blind sub-window). Recommendation: **REVISE** — all four are narrow, wording/spec-precision fixes consistent with the design's own anti-bloat doctrine (no new machinery required for any of them), but DA-001 should not be waved through as "already-disclosed" since it is not disclosed anywhere in the six files.

---

## Findings Table

| ID | Finding | Severity | Evidence (file:line) | Affected Dimension |
|----|---------|----------|------------------------|--------------------|
| DA-001-iter7 | Near-cap `grep -c` id-minting shortcut derives the wrong canonical id in every segment after the first, risking a real cross-segment id collision | Critical | `feedback-decision-log-convention-design.md:195`; `staging-feedback-logs/feedback-decision-logs-standards.md:28`; `staging-feedback-logs/examples-appendix.md:173` | Methodological Rigor / Internal Consistency |
| DA-002-iter7 | Read-side gap declared "closed" by an install-step instruction with no hook seam and none of the L1-fragility hedging the write-side gets everywhere else | Major | `feedback-decision-log-convention-design.md:244`; `:254`; `staging-feedback-logs/hook-design-note.md:6-15,21-50` | Internal Consistency / Traceability |
| DA-003-iter7 | Persisted interrupted-rotation trigger (IN-003) has an undetected sub-window between rotation steps 1 and 2, so the recovery-forcing-function it exists to provide can silently fail to fire | Major | `feedback-decision-log-convention-design.md:203-208`; `staging-feedback-logs/feedback-decision-logs-standards.md:67` | Completeness / Methodological Rigor |
| DA-004-iter7 | Worked example labels a self-described "standing — applies continuously" directive with terminal `Disposition: DONE`, blurring the schema's own closed-vs-ongoing semantics | Minor | `staging-feedback-logs/FEEDBACK-LOG.template.md:49`; `staging-feedback-logs/examples-appendix.md:54-55` | Evidence Quality |

**Finding ID format:** `DA-{NNN}-iter7` (stable across this iteration's disposition record).

---

## Finding Details

### DA-001-iter7: Near-cap `grep -c` id-minting shortcut silently miscounts after the first rotation [CRITICAL]

**Claim challenged:** The design's near-cap id-minting instruction, stated identically in three artifacts:
- `feedback-decision-log-convention-design.md:195` — *"At or near cap (within ~5 entries, PM-005), id-minting SHOULD derive the next id from a deterministic `grep -c '^## FU\.'` (or `'^## DEC-LLM-'`) count — reusing the parity-check tool, no new lint — rather than an LLM Read of a file that may already be truncated past its tail (PM-002)."*
- `staging-feedback-logs/feedback-decision-logs-standards.md:28` (LOG-M-006) — *"...and at or near cap (within ~5 entries), derive the next id from a `grep -c '^## FU\.'` / `'^## DEC-LLM-'` count, not an LLM Read of a possibly-truncated file (PM-002)."*
- `staging-feedback-logs/examples-appendix.md:173` — *"If the file is at or near the segment cap, count with `grep -c '^## FU\.'` rather than a Read that may truncate before the tail (PM-002)."*

**Counter-argument:** `grep -c '^## FU\.'` on the ACTIVE file returns the **count of headings physically present in that file**, not the **highest canonical id value in use across the log**. These are only the same number in Segment 1, where the first entry is `FU.0` and the count coincidentally equals `last-id + 1`. From Segment 2 onward, the ACTIVE file's first entry is `FU.50` (or whatever the segment's starting id is, per its own Segment Index row — e.g. `2 | FEEDBACK-LOG.md (ACTIVE) | FU.50 – …`), so a file containing 45 headings (`FU.50`…`FU.94`) yields `grep -c` = 45, not 95. Using that raw count "as the next id" (the only operation the text describes — no offset-by-segment-baseline step is stated anywhere near this instruction) would mint `FU.45`, which is **already in use in Segment 1**. This is exactly the failure mode LOG-M-005 exists to prevent ("unique, monotonic per log across all segments") and exactly the class of collision the whole design cites `[internal-kb]`'s `DJ-NNN` scheme as the cautionary precedent for (design doc Improvement Ledger row 2, and again at `feedback-decision-log-convention-design.md:78`).

Two design-internal facts make this worse, not better:
1. The **general-case** id-minting path (a plain Read of the last heading, described in `examples-appendix.md:173`'s own "editing by hand" bullet and implied throughout) is correct, because the heading text itself always carries the true global id (`## FU.83`, not a count). The bug is specific to the *shortcut* introduced to avoid that Read near the cap.
2. The stated rationale for the shortcut — avoiding "an LLM Read of a file that may already be truncated past its tail" — is itself in tension with the design's own cap-sizing math (`feedback-decision-log-convention-design.md:195` cap-derivation cell: "800 lines ≈ 40% of the 2,000-line Read window (2.5× headroom)"). A full-file Read of an 800-line ACTIVE file cannot truncate against a 2,000-line window; the only way a near-cap Read plausibly truncates before the tail is under the framework's own CB-05 practice of reading with `offset`/`limit` on files > 500 lines (`agent-development-standards.md` CB-05) — i.e. the shortcut is reacting to the agent's own partial-read habit, and its fix (a raw count) only works if that same single-file scope assumption holds, which is exactly what breaks the offset math post-rotation.

**Refutation panel (self-applied, 3 lenses, per the VERIFIED-CRITICALS protocol):**
1. **Textual-defense lens** — Is there language elsewhere that saves this (e.g., "count" implicitly means "count + segment-index baseline")? No. The Segment Index section (`feedback-decision-log-convention-design.md:199`) and the id-minting cells never cross-reference each other's arithmetic. The *parity check* (a different mechanism, same tool) sums two file-local counts against a *pre-recorded* total — it does not derive an absolute id either, so "reusing the parity-check tool" does not import a save.
2. **Frequency/materiality lens** — Is this a rare edge case? No — by the design's own math, a log rotates every ~50 entries, and this exact shortcut is invoked at every near-cap window of every segment after the first. It is the highest-traffic id-minting path a long-lived, multi-session log would exercise repeatedly.
3. **"A competent reader would just get it right anyway" lens** — Plausible, but self-defeating: the entire justification for moving to a "deterministic" `grep -c` step *instead of* an LLM Read was to remove reliance on model judgment ("what depends on the model remembering [or inferring] will eventually be forgotten [or gotten wrong]" — the design's own governing principle, `feedback-decision-log-convention-design.md:38`). Requiring the model to silently supply an un-stated segment-baseline correction reintroduces exactly the inference-dependency the shortcut was built to eliminate.

The finding survives all three lenses.

**Impact:** A silent cross-segment id collision breaks the "unique, monotonic, collision-resistant" guarantee that is this design's headline improvement over `[internal-kb]`. Two entries could legitimately claim the same canonical id across segments, which the id-integrity lint (L5 check 2) may not even catch — that lint verifies *contiguity within* the set of segments it reads, not that a *newly minted* id doesn't collide with an *older, sealed* segment's already-used id.

**Response Required:** Either (a) state the correct formula explicitly — "next id = (segment's starting canonical id, from the Segment Index row) + (grep -c count of the ACTIVE file)" — in all three locations, or (b) drop the shortcut and always resolve the next id by reading the ACTIVE file's actual last `## FU.N` / `## DEC-LLM-NNN` heading (which is already proven safe by the 2.5× headroom math and requires no arithmetic).

**Acceptance Criteria:** The corrected instruction must be restated, with the same wording, in all three locations it currently appears (`feedback-decision-log-convention-design.md:195`, `feedback-decision-logs-standards.md:28`, `examples-appendix.md:173`), so the propagation-gap class this project has repeatedly had to sweep for (v7-v9 changelog entries) is not reintroduced by fixing only one instance.

---

### DA-002-iter7: Read-side gap declared "closed" without the write-side's hedging or hook compensation [MAJOR]

**Claim challenged:** `feedback-decision-log-convention-design.md:244` names the gap honestly: *"nothing in the framework's session-start orientation makes a new session actually consult past entries (unlike `MEMORY.md`, which is force-loaded). That gap is **closed** by the install-step action added to the Adoption plan (step 3)..."* — and `:254` (Adoption step 3): *"add `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` to `project-workflow.md`'s session-start 'Before' orientation row'... so a new session is **instructed** to consult them... this **closes** the read-side gap."*

**Counter-argument:** The fix is, by its own wording, an *instruction* added to an L1-tier rule file — the same enforcement tier the design elsewhere explicitly calls "vulnerable" and "more context-rot-vulnerable than a HARD rule" for the *write*-side risk (`feedback-decision-log-convention-design.md:241`, Enforcement-layer disclosure). That disclosure names a concrete compensating control for the write-side (the Q3 hook: capture reminders at `Stop`/`PreCompact`). No equivalent compensating control exists for the read side: `hook-design-note.md`'s three seams (`:6-15` nav table, `:21-50` full definitions) are `UserPromptSubmit` (provenance stamping), `Stop`/`PreCompact` (capture reminder), and an optional segment-cap reminder — none of them remind or verify that a *new* session actually read the log. The word "closes" is therefore doing more work than the mechanism it describes actually delivers: an L1 orientation-row instruction is exactly as forgettable as the write-side's LOG-M-001..006 "SHOULD" disciplines, but unlike those, it gets no disclosed fragility caveat and no designed hook seam.

**Why this matters for the stated purpose:** "Feedback/decisions never lost" quietly depends on someone, some session, actually reading the log — otherwise a real (not disclosed) item sits captured-but-undiscovered indefinitely, which is functionally equivalent to loss for the operator even though the bytes persist. The document is careful to name this exact distinction everywhere else ("bytes persist on disk" vs. "the next session knows about them," `:254`) but stops short of applying its own honesty standard to the fix's residual fragility.

**Response Required:** Either (a) add the same L1-vulnerability hedge already used for the write side to the read-side "closes" claim (e.g., "mitigates, subject to the same L1 context-rot vulnerability disclosed above; no hook seam exists for this side yet"), or (b) design a fourth, cheap seam (e.g., a `SessionStart` hook that injects "N open FEEDBACK-LOG / LLM-DECISION-LOG items exist — review before proceeding" using the same fail-open shape as Seams 1-2) and note it as a Q3-equivalent follow-up rather than asserting the gap is already closed.

**Acceptance Criteria:** The word "closes" is either qualified with the same hedging language the write-side risk carries, or backed by a named (even if not-yet-shipped) hook seam, consistent with how every other MEDIUM-tier residual in this package is handled.

---

### DA-003-iter7: Interrupted-rotation trigger (IN-003) has an undetected sub-window [MAJOR]

**Claim challenged:** `feedback-decision-log-convention-design.md:203-208` defines rotation as four required steps (1: copy to sealed `.NNN.md`; 2: reset ACTIVE + re-seed index + carry forward Backfill; 3: required parity check; 4: resume appends), and adds: *"**Persisted trigger (IN-003,...):** before the first append of any session, if the Segment Index's last row does not match the ACTIVE file's actual last heading, treat it as a possible interrupted rotation and run the parity check before proceeding."* Restated identically at `staging-feedback-logs/feedback-decision-logs-standards.md:67`.

**Counter-argument:** Consider an interruption that lands **between step 1 and step 2** — the sealed copy (`.NNN.md`) has been written, but the ACTIVE file has not yet been reset (still segment N, full of the pre-rotation entries) and the Segment Index has not yet been re-seeded. In this state, the ACTIVE file is internally self-consistent: its own last heading and its own (stale, but still-current) Segment Index row still agree with each other, because nothing about the ACTIVE file changed yet. The stated trigger condition ("index row vs. actual last heading mismatch") therefore has nothing to detect — the only observable evidence of the interruption is an *extra*, duplicate-content sealed file sitting alongside a still-full, unreset ACTIVE file, which is external to what the stated check inspects. If the assistant does not independently think to `ls` for an unexpected `.NNN.md` matching the ACTIVE file's own current segment number, the interruption is invisible to the one mechanism (IN-003) explicitly built "so recovery does not depend on the model remembering a mid-flight rotation" (`:208`) — the recovery path is, in this specific sub-window, back to depending on exactly that.

**Why this is not merely the already-disclosed "crash mid-rotation" caveat:** The design already discloses that crashes mid-rotation are real ("a documented real scenario for this project," `:208`) and specifies what to do *once detected* (re-run parity; halt-and-escalate on mismatch). What is not disclosed is that the *detector itself* (IN-003) has a blind sub-window for one of the two natural places a crash can land. This is a gap in the detection mechanism, not a restatement of the already-accepted "crashes happen" risk.

**Impact (bounded, hence Major not Critical):** No data is destroyed in this scenario — the ACTIVE file still holds every entry. The residual is an undetected orphan sealed file and a delayed rather than data-losing failure; the existing L5 lint's orphan check (`feedback-decision-logs-standards.md:82`) would eventually surface the duplicate segment at commit time, if wired. That eventual backstop is why this is Major, not Critical.

**Response Required:** Extend the IN-003 trigger to also check, before the first append of a session, whether a sealed segment file matching the ACTIVE file's *own* current segment number already exists on disk (a one-line `ls` addition, no new lint, consistent with the design's own anti-bloat doctrine) — closing the step-1-to-step-2 blind window.

**Acceptance Criteria:** The trigger description in both locations names the on-disk existence check alongside the index-vs-heading check, so both natural interruption points are covered by the same forcing function.

---

### DA-004-iter7: Worked example blurs terminal `DONE` with an ongoing standing policy [MINOR]

**Claim challenged:** `staging-feedback-logs/FEEDBACK-LOG.template.md:49` and the parallel worked example at `staging-feedback-logs/examples-appendix.md:54-55` both give the commit-cadence directive a **Disposition: DONE (standing — applies continuously)**.

**Counter-argument:** The schema's own framing (`feedback-decision-logs-standards.md:26` diagram + prose) treats `DONE`/`WONTFIX` as terminal states with an evidence link, i.e. "this item is closed." A directive that "applies continuously" is not closed in that sense — it is an ongoing standing policy, closer in spirit to something that should never leave `OPEN`/`IN-PROGRESS` (or a dedicated state the schema does not have). Using `DONE` for it is a small semantic stretch that could teach an operator or future session the wrong lesson about what `DONE` certifies (a discrete accomplishment vs. a live policy).

**Response Required:** Either add one clause distinguishing "DONE (standing)" as a deliberate, named sub-case in the schema description (so it is a documented convention, not an ad hoc worked-example choice), or use a state that better fits an ongoing policy.

**Acceptance Criteria:** Acknowledgment sufficient (per Minor severity); no action required to proceed.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- DA-001-iter7: Correct the near-cap id-minting formula in all three locations (design doc L1.4 table, LOG-M-006, examples-appendix "Common cases" bullet) to include the segment-starting-id offset, or replace the shortcut with the already-safe heading-Read approach.

**P1 (Major — SHOULD resolve; require justification if not):**
- DA-002-iter7: Apply the same L1-fragility hedge to the read-side "closes the gap" claim that the write-side risk already carries, or name a concrete (even if deferred) hook seam for it.
- DA-003-iter7: Extend the IN-003 persisted trigger to also check for an on-disk sealed segment matching the ACTIVE file's own current segment number, closing the step-1/step-2 blind window.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- DA-004-iter7: Clarify or relabel the "DONE (standing)" worked example's disposition semantics.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-003: the interrupted-rotation forcing function omits one of its two natural trigger windows. |
| Internal Consistency | 0.20 | Negative | DA-001: the near-cap shortcut's arithmetic contradicts the (correct) general-case heading-Read approach used everywhere else; DA-002: the read-side "closes" claim is inconsistent with the rigor applied to the analogous write-side risk. |
| Methodological Rigor | 0.20 | Negative | DA-001: the one place the design substitutes a mechanical shortcut for model judgment is itself under-specified, reintroducing the exact inference-dependency it was built to remove. |
| Evidence Quality | 0.15 | Negative (minor) | DA-004: worked example's disposition choice is not fully evidenced against the schema's own terminal-state definition. |
| Actionability | 0.15 | Neutral | All four findings carry concrete, narrow, no-new-machinery fixes consistent with the design's own anti-bloat doctrine. |
| Traceability | 0.10 | Negative | DA-002: the asymmetry between write-side and read-side risk disclosure is untraceable to any stated rationale. |

**Overall assessment:** Targeted revision. None of the four findings require new lint, new files, or new subsystems — all are wording/formula corrections consistent with how this design has closed every prior round's Criticals. DA-001 is the one item that should not be treated as an already-accepted residual: it is a previously unflagged correctness defect in the id scheme's own core collision-resistance mechanism, discovered by attacking the specific angle assigned (rotation/id/alias survival under real multi-session use).

---

## Execution Statistics

- **Total Findings:** 4
- **Critical:** 1
- **Major:** 2
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5 (Assume Advocate Role; Document and Challenge Assumptions; Construct Counter-Arguments; Require Substantive Responses; Synthesize and Score Impact)
