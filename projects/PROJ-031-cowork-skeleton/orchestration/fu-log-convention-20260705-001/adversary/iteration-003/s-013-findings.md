# Inversion Report: Feedback & Decision Log Convention (PROJ-031, FU.2)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverable, scope, blind protocol |
| [Summary](#summary) | Overall assessment and recommendation |
| [Step 1-2: Goals and Anti-Goals](#step-1-2-goals-and-anti-goals) | What would guarantee loss, at the goal level |
| [Step 3: Assumption Map](#step-3-assumption-map) | Explicit + implicit assumptions underlying the durability claim |
| [Findings Table](#findings-table) | IN-NNN stress-test results |
| [Finding Details](#finding-details) | Expanded Critical/Major findings with evidence |
| [Null-Alternative Comparison](#null-alternative-comparison) | Does the package beat memory files + transcripts only? |
| [Recommendations](#recommendations) | Prioritized, lightweight (anti-bloat) mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 6 dimensions |
| [Execution Statistics](#execution-statistics) | Finding counts |

---

## Execution Context

- **Strategy:** S-013 (Inversion Technique), per `.context/templates/adversarial/s-013-inversion.md`
- **Criticality:** C4 | **Engagement gate:** 0.95 (user-set)
- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
- **Iteration:** 3 (per the design doc's own Revision Changelog, iterations 1-2 already closed prior Critical/Major findings; this execution is blind to those adversary outputs per protocol and independently re-runs Inversion against the current package state)
- **Blind protocol:** Did not read any prior adversary iteration output. Read: the design doc, all 5 staging files, `FEEDBACK-LOG.md`, `LLM-DECISION-LOG.md`, ambient rule files (`project-workflow.md`, `quality-enforcement.md`, `mcp-tool-standards.md`, etc., auto-loaded in this session), and the current session's own `MEMORY.md` auto-load behavior as direct empirical evidence. `orchestration/.../ux/` directory does not currently exist (glob returned no files) — UX findings could not be cross-checked from that source; the design doc's own "UX Findings Disposition" section (lines 273-289) was used instead.
- **Posture applied:** Per instruction, this is a deliberately MINIMAL MEDIUM-tier convention; descoped-with-disclosure is a valid posture and is NOT penalized. Findings below are restricted to (a) gaps the package does not itself disclose anywhere, or (b) disclosed gaps whose disclosure is inadequate given the specific "guarantee loss" framing of this review. Already-disclosed-and-accepted residuals (per the deliverable's own Revision Changelog, lines 305-312) are down-weighted to Minor/confirmatory rather than re-raised as fresh Criticals.

---

## Summary

Inverting the deliverable's central claim ("once captured, [feedback and decisions] survive context compaction, session boundaries, and model swaps," design doc line 30) surfaces **two undisclosed mechanisms that would guarantee loss or effective loss even when the convention is followed exactly as written**: (1) nothing in the package links a log append to a git commit, so an entry can be created, then discarded by an ordinary git-destructive operation before the next "milestone" commit — a risk the null alternative's `MEMORY.md` store does not share, because it lives outside the git working tree; (2) nothing makes a new session actually *read* the log content (unlike `MEMORY.md`, which this very session's system-reminder shows is force-loaded automatically) — `project-workflow.md`'s "Before" phase and the design's own install plan never add the two log files to session-start orientation, so "survive session boundaries" is true only in the narrow sense of "the bytes are on disk somewhere," not in the practical sense of "the assistant will know about it." Both are Critical because they directly contradict an unqualified "survive" claim without disclosure, and both have cheap, wording-only fixes consistent with the package's own anti-bloat doctrine. Two further Major findings (a sealed-segment immutability contradiction in the correction workflow; the absence of any explicit comparison against the null alternative the task itself asks for) and three Minor/confirmatory findings round out the assessment. **Recommendation: REVISE** (not reject) — the fixes below add zero new machinery, matching the package's own remediation pattern from iterations 1-2.

---

## Step 1-2: Goals and Anti-Goals

**Primary goal (explicit, design doc line 30):** "user feedback and human↔LLM decisions, once captured, survive context compaction, session boundaries, and model swaps."

**Secondary/implicit goals:** (a) the convention is discoverable and actually consulted, not merely durable in principle; (b) the convention materially improves on doing nothing (memory files + raw transcripts alone) — this is the explicit counterfactual this review was asked to test; (c) integrity/immutability claims (sealed segments, git-backstop) hold under the package's own documented workflows, not just under "normal" use.

**Anti-goal 1 ("how would we guarantee an entry, once written, is later gone?"):** Write the entry to the markdown file but never commit it; let a git-destructive operation (checkout, clean, hard reset, branch switch over an untracked new file) run before the next commit. -> **The package does nothing to prevent this** (see IN-001).

**Anti-goal 2 ("how would we guarantee the convention fails to prevent the practical harm it exists to prevent — the assistant re-litigating settled feedback/decisions across a session boundary?"):** Simply never read the log at the start of a new session; nothing forces or even suggests it. -> **The package does nothing to prevent this** (see IN-002).

**Anti-goal 3 ("how would we guarantee a stated integrity property is contradicted by the package's own procedure?"):** Follow the documented correction workflow ("mark the old entry `Superseded by: FU.N`") against an entry that has already rotated into a sealed segment. -> **The package's own text creates this condition** (see IN-003).

---

## Step 3: Assumption Map

| # | Assumption | Type | Confidence (as stated by package) | Validation status |
|---|---|---|---|---|
| A1 | Once appended to the markdown file, an entry is durable across session boundaries | Implicit, load-bearing (design doc line 30) | Implied High | Not validated; not addressed anywhere against git-workspace risk |
| A2 | A future session will discover and consult the log's content | Implicit, load-bearing (whole point of "survive session boundaries") | Implied High | Not validated; contradicted by absence from `project-workflow.md` "Before" phase and the install plan |
| A3 | Sealed segments remain immutable-by-convention (design doc line 178) | Explicit | Medium (package itself says "there is no filesystem lock") | Not reconciled against the correction workflow's own instructions |
| A4 | The convention is an improvement over the "do nothing" baseline (memory files + transcripts only) | Implicit (motivates the whole deliverable) | Implied High | Only tested against `[internal-kb]` (Improvement Ledger, lines 239-255); never tested against the null baseline explicitly |
| A5 | Assistant-verbatim excerpt+pointer preserves full fidelity "while the transcript is retained" | Explicit, disclosed | Explicitly Low/unenforced ("[INFERENCE]: no transcript-retention policy is cited", line 119) | Disclosed and accepted per changelog — confirmatory only |
| A6 | The `PreCompact` reminder (Q3, unshipped) is the safety net for imminent-compaction loss | Explicit | Medium | Not cross-referenced against the already-existing AE-006e mandatory-checkpoint rule |
| A7 | Backfill Queue staleness ("source observed to have rotated") will be noticed | Explicit, disclosed as best-effort | Low, disclosed | Disclosed and accepted per changelog — confirmatory only |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-iter3 | A1: append = durable across session boundaries | Assumption | High (implied, unstated) | **Critical** | design doc line 30 (claim) vs. no commit-linkage anywhere in LOG-M-001..006 or the Adoption plan | Internal Consistency |
| IN-002-iter3 | A2: a new session will consult the log | Assumption | High (implied, unstated) | **Critical** | `.context/rules/project-workflow.md` "Before" row (no log mention); design doc lines 225-236 (Adoption plan, no session-start wiring); this session's own auto-loaded `MEMORY.md` (empirical contrast) | Completeness |
| IN-003-iter3 | A3: sealed segments immutable-by-convention vs. correction workflow | Anti-Goal / Contradiction | Medium | **Major** | design doc line 178 vs. `feedback-decision-logs-standards.md` line 38 and `examples-appendix.md` line 169 | Internal Consistency |
| IN-004-iter3 | A4: convention beats the null alternative | Completeness gap | Medium | **Major** | Improvement Ledger, design doc lines 239-255 (compares only to `[internal-kb]`, never to "no convention") | Methodological Rigor |
| IN-005-iter3 | A6: Q3 reminder vs. existing AE-006e | Anti-Goal | Low | Minor | design doc lines 163-166, 266 vs. `quality-enforcement.md` Auto-Escalation Rules (AE-006e) | Traceability |
| IN-006-iter3 | A5: transcript-retention policy unstated | Assumption | Low (disclosed) | Minor (confirmatory) | design doc lines 119, 121; already flagged `[INFERENCE]` by the package itself | Evidence Quality |
| IN-007-iter3 | A7: Backfill staleness-detection undefined | Assumption | Low (disclosed) | Minor (confirmatory) | design doc L2 step 6 ("no proactive detector for silent non-capture, per the L0 scope note") | Traceability |

**Finding ID format:** `IN-{NNN}-iter3` (this execution). No collision with iteration-1/2 `IN-NNN` ids referenced in the design doc's own changelog, since those are scoped to their own execution ids.

---

## Finding Details

### IN-001-iter3: Durability claim does not address uncommitted-loss [CRITICAL]

**Type:** Assumption (implicit, load-bearing)
**Original assumption:** "two append-only markdown ledgers so that user feedback and human↔LLM decisions, **once captured, survive** context compaction, session boundaries, and model swaps" (`design/feedback-decision-log-convention-design.md:30`). The only hedge attached to this sentence scopes *capture* ("they do not by themselves guarantee that every turn gets logged") — it says nothing about whether a *captured* (already-appended) entry is itself durable.
**Inversion:** Append N entries to `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` in the same turn they are given (as LOG-M-001 instructs), then let the working tree be affected by any ordinary git-destructive operation before the next commit — `git checkout -- <file>` / `git reset --hard` on a tracked file with unstaged edits, or `git clean -fdx` on a not-yet-tracked new file (both files are brand-new artifacts of this very design, i.e., untracked until first committed). All N entries are gone with **no backstop of any kind** — not git history (nothing was ever committed), not the L5 lint (which only runs "pre-commit and in CI," design doc line 229, so there is nothing to check against an event with no commit), not the "git-backstopped" integrity claim (design doc line 61, which assumes a commit history exists to diff against).
**Plausibility:** High. LOG-M-001 explicitly asks for same-turn appends (frequent, small writes), while the only commit-cadence directive in the package (`FEEDBACK-LOG.md` FU.3, "commit and push... at a regular cadence" tied to "milestone / workflow / phase boundaries") is coarser-grained and generic — it is not a rule of *this* convention and is never cross-referenced from LOG-M-001..006 or the design doc's Boundaries/Scoping sections.
**Confidence:** High that the gap exists (verified by reading all 6 package files plus the ambient `project-workflow.md`; no mention of "uncommitted," "working tree," or "dirty" state anywhere in the corpus).
**Consequence:** Directly falsifies the deliverable's own headline claim for exactly the population of entries most likely to be freshly captured and not yet committed — i.e., the newest, least-reviewed feedback/decisions.
**Evidence:** `design/feedback-decision-log-convention-design.md:30` (claim), `:61` (git-backstop claim, scoped to tamper-evidence not to un-committed loss), `:225-236` (Adoption/migration plan, no commit-linkage step); `FEEDBACK-LOG.md:71-81` (FU.3, generic cadence, not convention-specific).
**Dimension:** Internal Consistency (0.20)
**Mitigation:** Add one sentence to L0 (or a new sub-bullet under LOG-M-001) explicitly scoping the claim: *"Once appended AND committed, an entry survives compaction/session boundaries; an uncommitted append carries the same risk as any other uncommitted change in the repo and is not specially protected by this convention."* Cross-reference FU.3's commit-cadence directive by name as the (currently sole) mitigation, and consider recommending it fire at least once per session that touched either log — wording-only, no new machinery.
**Acceptance criteria:** L0 and/or Scoping section states the git-commit dependency explicitly; FU.3 (or an equivalent LOG-M rule) is cross-referenced by id from the log-specific rule file.

### IN-002-iter3: Nothing makes a new session actually consult the log [CRITICAL]

**Type:** Assumption (implicit, load-bearing)
**Original assumption:** The convention is meant to prevent the assistant from losing/re-litigating feedback and decisions "across... session boundaries" (design doc line 30). This requires that a *future* session actually reads the accumulated log content, not merely that the file continues to exist on disk.
**Inversion:** Ship the convention exactly as designed, install it exactly as planned, and start a brand-new session. Nothing in the ambient orientation procedure the framework already uses (`project-workflow.md`, Workflow Phases table, "Before" row: *"Set JERRY_PROJECT env var. Check PLAN.md. Review WORKTRACKER.md. Read relevant docs/knowledge/. Invoke /worktracker for structural guidance"*) mentions `FEEDBACK-LOG.md` or `LLM-DECISION-LOG.md`. The design doc's own Adoption/migration plan (lines 225-236, step 3: "register in CLAUDE.md skill/nav tables; add templates... add the trigger to `mandatory-skill-usage.md` if a skill wraps it") never proposes adding the two log files to any session-start read list. Result: the assistant proceeds with zero awareness of prior FU./DEC-LLM- entries unless the human operator explicitly tells it to go read the file that turn.
**Plausibility:** High — this is not a rare edge case, it is the *default* behavior of every new session under the plan as written.
**Confidence:** High, and directly falsifiable by comparison: this very conversation's system-reminder begins *"Contents of [home]/.../memory/MEMORY.md (user's auto-memory, persists across conversations)"* — i.e., `MEMORY.md` (the null-alternative store) is mechanically force-loaded into context at session start today, empirically, in this session. The proposed FEEDBACK-LOG/LLM-DECISION-LOG convention has no equivalent mechanism, disclosed or otherwise; the only enforcement-layer disclosure in the package (design doc line 219, "no L2 per-prompt re-injection... more context-rot-vulnerable than a HARD rule") is about the assistant *remembering to write new entries*, not about a *future session reading past ones* — a distinct read-side gap the package does not address at all.
**Consequence:** The convention can be fully installed and fully complied with (every entry captured, every disposition tracked) and still fail at its stated purpose the moment a new session starts, because "survive" collapses to "persist unread on disk," which is a materially weaker property than what line 30 claims.
**Evidence:** `.context/rules/project-workflow.md` "Workflow Phases" table, "Before" row (no log reference — ambient rule file, ranked among the auto-loaded rules for this very session); `design/feedback-decision-log-convention-design.md:219` (disclosed gap is write-side only); `:225-236` (install plan silent on session-start wiring); this session's own system-reminder (`MEMORY.md` auto-load, empirical contrast).
**Dimension:** Completeness (0.20)
**Mitigation:** Add one line to `project-workflow.md`'s "Before" row (which already lists "Review WORKTRACKER.md") — e.g., *"Review FEEDBACK-LOG.md / LLM-DECISION-LOG.md (if present) for open items and standing decisions."* Add the equivalent action to the design doc's Adoption/migration plan step 3 (install-time checklist) so it is not forgotten. Both are one-sentence documentation additions — no new machinery, no hook, no lint.
**Acceptance criteria:** `project-workflow.md` Before-phase row references the two log files; the design doc's install plan step 3 explicitly lists this as an install action with an owner.

---

## Null-Alternative Comparison

The task asks directly: **does the package beat the null alternative (memory files + transcripts only)?** The package itself never performs this comparison (its Improvement Ledger, lines 239-255, benchmarks only against `[internal-kb]`) — this is IN-004-iter3. Answering it directly from evidence gathered above:

| Dimension | Null alternative (MEMORY.md + transcripts) | This convention | Verdict |
|---|---|---|---|
| Organization / disposition tracking of *recognized* feedback | None — `MEMORY.md` is an unstructured bullet list, no disposition/evidence-link fields | Structured, disposition-tracked, evidence-linked (LOG-M-002/-004, lint check 3) | **Convention wins** |
| Raw-preservation ceiling (does the log capture more than the transcript already holds?) | Transcript = 100% of turns, no recognition filter | Log = a curated *subset* of what the transcript already has (only "recognized" turns, per capture-trigger heuristics, design doc lines 78-85) | **No gain** — the log cannot exceed the transcript's raw completeness; it only re-packages a slice of it |
| Session-start rediscoverability | `MEMORY.md` is auto-loaded into every session's context (empirically observed this session) | No auto-load mechanism proposed anywhere (IN-002-iter3) | **Null wins today** |
| Durability against uncommitted-loss | `MEMORY.md` lives outside the project git working tree (`[claude-home]/.../memory/`), immune to git-destructive operations on the repo | Both logs are ordinary project files inside the git working tree, with no commit-linkage rule (IN-001-iter3) | **Null wins today** |
| Retention guarantee for the assistant-verbatim pointer (DEC log) | N/A (transcripts have no stated retention policy either) | Same unresolved dependency, but at least disclosed (IN-006-iter3) | **Tie (both unresolved)** |

**Net:** the convention is a genuine improvement for *organizing and closing out recognized feedback/decisions*, but on the specific "guarantee against loss" framing this review was asked to test, it does **not** unambiguously beat the null alternative today — on two concrete axes (session-start rediscoverability, uncommitted-change durability) it is currently *weaker* than `MEMORY.md`, because `MEMORY.md`'s auto-load and outside-of-git placement are structural properties this convention does not share and does not compensate for. Both gaps have cheap fixes (IN-001-iter3, IN-002-iter3 mitigations above).

---

## Recommendations

**MUST mitigate (Critical):**
- IN-001-iter3 — add the durability-scope sentence + cross-reference FU.3 by id (wording-only).
- IN-002-iter3 — add the log files to `project-workflow.md`'s "Before" row and the install-plan checklist (wording-only).

**SHOULD mitigate (Major):**
- IN-003-iter3 — add one reconciling sentence to L1.4 or the correction workflow: sanction "Superseded by:"/status-pointer edits as the one explicit exception to sealed-segment immutability, since they touch no verbatim text.
- IN-004-iter3 — add a short "vs. the null alternative" paragraph (the [Null-Alternative Comparison](#null-alternative-comparison) table above can be adapted directly) to L0 or the Improvement Ledger.

**MAY mitigate (Minor):**
- IN-005-iter3 — one sentence cross-referencing AE-006e as today's interim compaction backstop while Q3 is unshipped.
- IN-006-iter3 / IN-007-iter3 — already disclosed and accepted per the deliverable's own changelog; no new action required, noted here only for completeness of the Inversion pass.

All four actionable mitigations are text-only additions to existing sections. None require a new lint check, a new file, or a new hook — consistent with the package's own anti-bloat doctrine and its iteration-1/2 remediation pattern (wording/deletion only, no new machinery).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-002-iter3 (session-start rediscovery unaddressed), IN-004-iter3 (no null-alternative test, which this C4 review explicitly required) |
| Internal Consistency | 0.20 | Negative | IN-001-iter3 (unqualified "survive" claim vs. no commit-linkage), IN-003-iter3 (sealed-segment immutability contradicted by the documented correction workflow) |
| Methodological Rigor | 0.20 | Negative | IN-004-iter3 (the Improvement Ledger's comparative method never tests the specific counterfactual this task poses) |
| Evidence Quality | 0.15 | Neutral | IN-006-iter3 is already extensively evidenced and disclosed by the package itself; no fresh evidence gap found here |
| Actionability | 0.15 | Positive | Every finding above has a concrete, low-cost, wording-only fix, consistent with the package's demonstrated iteration-1/2 remediation discipline |
| Traceability | 0.10 | Negative | IN-005-iter3 (no cross-reference to existing AE-006e), IN-007-iter3 (Backfill staleness detection undefined, disclosed but not resolved) |

**Overall assessment: REVISE.** Two Critical findings (IN-001-iter3, IN-002-iter3) block a PASS verdict under H-13/the 0.95 engagement gate, but both are text-only fixes with no new machinery required — consistent with the anti-bloat posture this package has correctly maintained through two prior remediation rounds.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 2 (IN-001-iter3, IN-002-iter3)
- **Major:** 2 (IN-003-iter3, IN-004-iter3)
- **Minor:** 3 (IN-005-iter3, IN-006-iter3 [confirmatory], IN-007-iter3 [confirmatory])
- **Protocol Steps Completed:** 6 of 6 (goals stated, anti-goals inverted, assumptions mapped, assumptions stress-tested, mitigations developed, scoring impact synthesized)
- **Goals analyzed:** 3 (1 explicit, 2 implicit) | **Assumptions mapped:** 7 | **Vulnerable assumptions:** 4 (2 Critical, 2 Major)

---

*Strategy: S-013 Inversion Technique | Template: `.context/templates/adversarial/s-013-inversion.md` | Executed: 2026-07-06*
