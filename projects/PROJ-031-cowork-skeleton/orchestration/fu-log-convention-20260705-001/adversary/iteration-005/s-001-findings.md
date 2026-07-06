# Red Team Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention (Iteration 5)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}` (all paths relative to `projects/PROJ-031-cowork-skeleton/`)
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-001, iteration-005, blind agent)
**H-16 Compliance:** S-003 Steelman inferred applied in this and every prior iteration of this tournament -- the design doc's own Revision Changelog (v3-v6) cites `SM-001`..`SM-007` (Steelman-family) findings folded on every round, and the "6-group blind-agent order" this tournament follows runs self-refine -> steelman -> challenge (this strategy) -> verify -> decompose -> score. Confirmed by the design artifact's own evidence trail, **not** by a direct read of the iteration-005 S-003 output file (blind-protocol restriction bars reading anything under `adversary/` except this agent's own output). `[INFERENCE]`: ordering compliance inferred from artifact evidence, not verified by direct file read.
**Threat Actor:** A time-pressured or careless single operator (or a hostile insider exploiting the single-writer/MEDIUM-tier trust assumptions) who wants the *appearance* of tamper-evident, non-lossy, fully-disclosed logging while minimizing effort -- motivated to (a) simply never write an entry, since nothing technical stops them; (b) run concurrent sessions or hand-edit sealed segments, since the lint cannot catch a last-write-wins race; and (c) exploit the gap between what the **design doc** discloses (very thorough) and what the **actually-shipping artifacts** (rule file, templates, appendix, hook note) carry forward -- because only the shipping artifacts govern behavior after install; the design doc is not installed anywhere.

_Status: COMPLETE._

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All 7 RT-NNN findings at a glance |
| [Finding Details](#finding-details) | Full evidence, analysis, countermeasures per finding |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized countermeasure plan |
| [Scoring Impact](#scoring-impact) | Mapping to the 6 S-014 dimensions |

---

## Summary

Threat actor: a careless-or-hostile single operator exploiting the gap between the design doc's rich, iteration-tested disclosures and what actually ships. Five attack vectors were enumerated across all 5 MITRE-style categories (Ambiguity, Boundary, Circumvention, Dependency, Degradation); **1 Critical, 3 Major, 3 Minor** findings resulted. The headline finding (RT-001) is a **recurrence of the exact failure class this tournament has fought for four prior iterations**: a Critical disclosure ratified in the design doc (Q5 -- silent non-capture has no proactive detector) never propagated into any of the five staged artifacts that actually install. Given the project's own doctrine that overclaimed/unpropagated coverage is Critical and that all fixes must be wording-only (anti-bloat), the recommendation is **REVISE** -- targeted, zero-new-machinery text propagation of the four non-Minor findings into the shipping artifacts, consistent with every prior remediation round in this project's history.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-001-20260706-iter5 | Q5's Critical "silent non-capture, no proactive detector" disclosure exists only in the design doc; absent from all 5 shipping artifacts, and even where stated, misdescribes an unshipped hook reminder as an extant backstop | Rule Circumvention | High | Critical | P0 | Missing (in shipped surface) | Internal Consistency |
| RT-002-20260706-iter5 | No `project` field anywhere in the Context schema (design doc, rule file, or both templates), yet repo-root logs are explicitly expected to span multiple projects | Ambiguity Exploitation | Medium | Major | P1 | Missing | Traceability |
| RT-003-20260706-iter5 | The git tamper-evidence backstop's commit-granularity precondition (commit an edit promptly, independent of milestone cadence) is an actionable SHOULD-directive stated only in the design doc, not in the shipped rule file's Segment Rotation section | Degradation Paths | Medium | Major | P1 | Missing (in shipped surface) | Actionability |
| RT-004-20260706-iter5 | The design's own "governing principle" (what depends on the model remembering will eventually be forgotten -- the entire rationale for the Q3 hook) is directly re-violated by its own stated interim mitigation for segment-rotation-cap detection (assistant self-counts entries/lines from memory), unflagged as a self-referential exception | Dependency Attack | Low-Medium | Major | P1 | Missing | Internal Consistency |
| RT-005-20260706-iter5 | "Graduation: deferred -- {reason}" has a first-cycle cap (next milestone / ~3 months) but no stated limit on *renewing* the deferral indefinitely, letting an operator perpetually dodge H-32 GitHub-parity ceremony for a decision that should graduate | Rule Circumvention | Low | Minor | P2 | Partial (calendar nudge only) | Completeness |
| RT-006-20260706-iter5 | "its Context line references the sidecar key rather than hand-typing the metadata" is ambiguous between (a) inlining resolved values sourced from the sidecar and (b) storing an opaque pointer that requires the sidecar to still exist to resolve later | Ambiguity Exploitation | Low | Minor | P2 | Partial (resolvable by context, not stated explicitly) | Evidence Quality |
| RT-007-20260706-iter5 | `FEEDBACK-LOG.template.md`'s inline prose "Corrections are append-only" is stated without the same "(convention-only, git-backstopped -- not a filesystem lock)" hedge the rule file carries at the identical claim | Boundary Violations | Low | Minor | P2 | Partial (hedge exists one file away) | Internal Consistency |

**Finding ID Format:** `RT-{NNN}-20260706-iter5` (iteration-005 execution).

---

## Finding Details

### RT-001: Q5's non-capture disclosure never propagated to the shipping artifacts [CRITICAL]

**Attack Vector:** A careless or hostile operator/session simply never appends anything to either log. Nothing technical prevents this: LOG-M-001 is a SHOULD-tier rule (HARD ceiling is full, per the project's own `.context/rules/quality-enforcement.md`), and the L5 lint checks are conditioned on the file already existing and having content -- Lint 1 ("nav table present + cap not exceeded") only fires "if `FEEDBACK-LOG.md` ... exists and is > 30 lines," so a log that is simply never populated triggers zero lint failures. The design doc is honest about this residual **at the design-doc layer**: it elevates it to an explicit ratification item, Q5, with the same per-item P-020 visibility as Q1-Q4 (design doc line 279): *"Accept as a disclosed residual with no proactive detector until the Q3 hook ships. The `Stop`/`PreCompact` reminder (best-effort, non-exhaustive -- L1.3) is the only backstop; capture stays a MEDIUM discipline."* But the design doc is a **planning artifact**, not an installed one -- per the Adoption plan (design doc lines 232-244), only `feedback-decision-logs-standards.md`, the two templates, and (separately, later) the hook move into `.context/rules/` / `.context/templates/` / `hooks/`. I re-read all five staged artifacts in full (`feedback-decision-logs-standards.md`, both templates, `examples-appendix.md`, `hook-design-note.md`) and **none of them contains the words "Q5," "non-capture," "residual," "no proactive detector," or any paraphrase of it.** The staged rule file's closest statement is its header line: *"Capture itself is a MEDIUM (SHOULD) discipline (HARD ceiling is full at 25/25; nothing auto-closes); a fail-open hook is designed to assist but is not yet shipped"* (`feedback-decision-logs-standards.md:3`) -- this discloses that capture is optional and unenforced, but never states the sharper Q5 fact that **there is no detector, ever, for a turn that should have been logged and was not.** An operator who reads only the installed rule file (the only artifact that survives past ratification) walks away with less awareness of this specific residual than the design doc that was supposedly fully ratified with per-item P-020 visibility.

**Category:** Rule Circumvention (a MEDIUM-tier obligation with literally zero detection surface, further weakened by inconsistent disclosure across the artifact set).

**Exploitability:** High -- requires zero technical skill; the "attack" is simply doing nothing. The only friction is social (the operator wants to appear compliant), and the installed rule file itself does not communicate how completely undetectable non-compliance is.

**Severity:** Critical -- this is precisely the overclaimed-coverage failure class the task brief calls out as automatically Critical, and it is precisely the failure class this project's own tournament has repeatedly found and fixed in iterations 1-4 (per the design doc's own changelog: iteration-4's "dominant failure mode this round was cross-artifact **propagation** of a fix, not the wording itself"). Its recurrence here, in the round immediately after a changelog entry claiming a "package-wide overclaim sweep... across all 6 files" (design doc line 326, v6 entry), is itself evidence that the sweep was incomplete for this specific residual, which was *elevated to Q5 in that very same v6 round*.

**Existing Defense:** Missing in every file that actually installs. Partial-only in the design doc, which is not one of the install targets (Adoption plan, design doc lines 236-238, lists only the rule file, two templates, and (separately, later) the hook -- the design doc itself is never named as an install target).

**Evidence:** `design/feedback-decision-log-convention-design.md:279` (Q5 row, full text quoted above) vs. absence in `design/staging-feedback-logs/feedback-decision-logs-standards.md` (full text read, lines 1-73, no match), `design/staging-feedback-logs/FEEDBACK-LOG.template.md` (full text read, no match), `design/staging-feedback-logs/LLM-DECISION-LOG.template.md` (full text read, no match), `design/staging-feedback-logs/examples-appendix.md` (full text read, no match), `design/staging-feedback-logs/hook-design-note.md` (full text read, no match). Compounding sub-issue: Q5's own phrasing overstates the current backstop's existence -- "the `Stop`/`PreCompact` reminder ... is the only backstop" reads as though this reminder is presently active, but Q3 (design doc lines 89, 168, 277) states the hook (which is what implements the `Stop`/`PreCompact` reminder, per `hook-design-note.md:31-35` Seam 2) is "designed in v1... but shipped as a separate gated change" -- i.e., **not yet built**. So even the design doc's own "only backstop" does not currently exist; today the true state is zero backstops of any kind.

**Dimension:** Internal Consistency (0.20) -- a Critical residual carries full P-020 ratification visibility in one artifact and zero visibility in the artifacts that actually govern post-install behavior; this is the same class of inconsistency (design-doc-says-X, shipped-artifact-says-less-than-X) that produced the weakest-dimension score (0.46 Internal Consistency) in iteration-1 of this same tournament.

**Countermeasure:** Add a one- to two-sentence disclosure to `feedback-decision-logs-standards.md`'s header or MEDIUM Standards table (e.g., appended to LOG-M-001: *"There is no proactive detector for a turn that should have been logged and was not; this is an accepted residual until the Q3 hook ships (not yet available)."*) -- pure text, zero new machinery, consistent with every prior remediation round's doctrine. Optionally add the same one-line disclosure to both template headers.

**Acceptance Criteria:** The phrase "no proactive detector" (or an equivalent unambiguous paraphrase) appears in `feedback-decision-logs-standards.md`, and Q3's "not yet shipped" status is stated adjacent to any reference to a `Stop`/`PreCompact` reminder as a "backstop," in both the design doc and the rule file.

---

### RT-002: No `project` field in the Context schema for a log the design expects to span multiple projects [MAJOR]

**Attack Vector:** The repo-root `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` is explicitly the destination whenever `JERRY_PROJECT` is unset (design doc L1.1 Scoping, line 94; rule file "Scoping" section, `feedback-decision-logs-standards.md:57`). The design doc itself names the exact failure scenario I am red-teaming: *"A feedback trail can span the project-scoped and repo-root logs..., and across several projects in one long session"* (design doc line 96, "Multi-scope discovery caveat"). Yet the Context schema -- defined identically in the design doc, the rule file, and both templates -- has no field for which project (if any) an entry concerns:
- Design doc L1.1: `datetime · session · model(s) · turn · agents/workflow · source` (line 59)
- Design doc L1.2: `datetime · session · model · agents/workflow · artifacts · Reflected in` (line 112)
- `FEEDBACK-LOG.template.md:22`: `datetime · session · model(s) · turn · agents/workflow · source`
- `LLM-DECISION-LOG.template.md:25`: `datetime · session · model · agents/workflow · artifacts · Reflected in`

Meanwhile the L1.3 automation table explicitly lists `project id + which log file` as harness-**stampable** (design doc line 154: *"YES | `JERRY_PROJECT` env → selects project-scoped vs repo-root"*) -- but "which log file" is a **routing** decision made at write time, not a value **retained in the entry** for later attribution. An operator reading the repo-root log six months later, after having worked in five different projects with `JERRY_PROJECT` unset at various points, has no field to `grep` for "which project was this about" -- only an opaque `session id`, resolvable only via a transcript that the design doc elsewhere concedes has an "unenforced" retention dependency (design doc L1.2 verbatim tradeoff, Option B). The Multi-scope discovery caveat solves *finding the right file*; it does not solve *attributing an entry once you are in the right (repo-root) file and it contains entries from several unrelated projects*.

**Category:** Ambiguity Exploitation (an undefined/unretained provenance value creates unintended interpretation risk for future readers).

**Exploitability:** Medium -- requires the normal, expected usage pattern of working across multiple Jerry projects in sessions where `JERRY_PROJECT` is sometimes unset; the design doc itself asserts this is a real scenario, not a hypothetical.

**Severity:** Major -- does not corrupt or lose the entry (the text is still captured verbatim), but defeats the log's own stated discoverability/traceability goal for a scenario the design explicitly anticipates.

**Existing Defense:** Missing across all three schema definitions (design doc, rule file is silent on the literal field list, both templates).

**Evidence:** `design/feedback-decision-log-convention-design.md:59,96,112,154`; `design/staging-feedback-logs/FEEDBACK-LOG.template.md:22`; `design/staging-feedback-logs/LLM-DECISION-LOG.template.md:25`.

**Dimension:** Traceability (0.10) -- findings/entries cannot be traced back to their originating project once they land in the shared repo-root surface.

**Countermeasure:** Add an explicit (optional, omit-if-project-scoped) `project` sub-field to the Context line, e.g., `datetime · session · model(s) · turn · project (— if repo-root and framework-level) · agents/workflow · source`, mirroring the already-present `scope: framework` trailing-tag convention (Q2). Zero new machinery -- one additional optional token in an existing line.

**Acceptance Criteria:** The Context field list in the rule file and both templates includes an explicit (nullable) project-attribution slot, and the L1.3 automation table's `project_id` row is cross-referenced to that slot.

---

### RT-003: Commit-granularity precondition for the git tamper-evidence backstop is design-doc-only [MAJOR]

**Attack Vector:** The rule file and templates all claim sealed segments are "immutable-by-convention (git-backstopped)" (`feedback-decision-logs-standards.md:51`: *"sealed segments are immutable-by-convention (git-backstopped), numbered `-LOG.001.md`, and so on"*). The design doc discloses two preconditions that must hold for this claim to actually deliver tamper-evidence: *"(a) reasonably linear history -- a squash-merge or history rewrite can collapse the per-edit tamper-evidence trail... and (b) commit granularity -- an edit made and committed together with the original entry inside one milestone-cadence commit window produces no separate diff to review, so an entry whose verbatim or terminal disposition is changed after initial capture SHOULD be committed promptly, independent of the routine milestone cadence"* (design doc line 180). Precondition (b) is an **actionable operator directive** ("commit promptly, independent of routine milestone cadence"), not mere background elaboration -- it changes what the operator should *do*, unlike, say, a worked example. Yet neither precondition appears in `feedback-decision-logs-standards.md`'s Segment Rotation section, nor in either template. This project has already exercised exactly the failure mode this precondition warns against once: FEEDBACK-LOG.md's own FU.3 entry records *"committed `--no-verify` once, disclosed in the commit message; debt tracked for fix before next commit"* (`FEEDBACK-LOG.md:78`) -- a real, evidenced instance of irregular/bypassed commit discipline in this exact project.

**Category:** Degradation Paths (the tamper-evidence guarantee silently erodes under a common, already-observed commit pattern, and the shipped artifact gives the operator no warning of the precondition that would prevent it).

**Exploitability:** Medium -- requires normal milestone-batched commit habits (already evidenced in this project's own history) rather than a deliberate attack.

**Severity:** Major -- the claim "immutable-by-convention (git-backstopped)" is stated unconditionally in the shipping rule file, while the condition that actually makes the backstop work is withheld from that same file.

**Existing Defense:** Missing in the shipped rule file's Segment Rotation section and both templates; present only in the design doc (which does not install).

**Evidence:** `design/feedback-decision-log-convention-design.md:180` (full caveat text); `design/staging-feedback-logs/feedback-decision-logs-standards.md:51` (unconditional claim, no precondition); `FEEDBACK-LOG.md:78` (this project's own prior `--no-verify` commit, evidencing the exact risk pattern).

**Dimension:** Actionability (0.15) -- the missing directive is precisely the kind of "specific action the creator/operator must take" the Actionability dimension measures; its absence from the shipped artifact leaves the operator unable to act on it post-install.

**Countermeasure:** Add one sentence to the rule file's Segment Rotation section: *"Commit an edited or newly-terminal entry promptly, independent of the routine milestone cadence -- a same-commit edit produces no separate diff to review."* Pure text; no new lint, no new file.

**Acceptance Criteria:** The commit-granularity precondition (or an equivalent one-sentence paraphrase) is present in `feedback-decision-logs-standards.md`.

---

### RT-004: The self-count interim mitigation re-violates the design's own governing principle [MAJOR]

**Attack Vector:** The design doc states its "governing principle" as: *"what depends on the model remembering will eventually be forgotten. Every field the harness can stamp deterministically ... is designed to be stamped by a fail-open hook; only judgment fields ... remain model/human-authored"* (design doc line 38). This principle is the explicit rationale for building the Q3 hook at all. Yet the **interim** (pre-hook) mitigation for detecting the FU.5 segment-rotation cap is: *"until the Q3 cap-reminder hook ships the assistant SHOULD self-count entries/lines in the ACTIVE file as it appends and proactively propose rotation on approaching the cap"* (design doc line 178) -- and the identical directive is repeated in the shipped rule file itself: *"Until the Q3 cap-reminder hook ships, the assistant SHOULD self-count entries/lines when it appends and propose rotation on approaching the cap"* (`feedback-decision-logs-standards.md:28`). Counting entries/lines "as it appends," turn after turn, across a long session and across compaction boundaries, is **exactly** the kind of model-memory-dependent bookkeeping the governing principle says will eventually be forgotten -- yet nothing in either artifact flags this interim mitigation as a deliberate, named exception to its own stated principle. The consequence is bounded (a delayed rotation, eventually caught by the commit-time lint), but the self-contradiction is unflagged and, per the Internal Consistency rubric, exactly the class of finding S-001 exists to surface.

**Category:** Dependency Attack (the interim path depends on the same fallible resource -- model attention/memory across turns -- that the whole automation effort exists to remove).

**Exploitability:** Low-Medium -- not exploitable by an external adversary in the security sense, but reliably triggered by ordinary long-session drift (the same drift class already evidenced by this project's own history of session crashes and interrupted workflows, e.g., `feedback-decision-log-convention-design.md` FU.1 disposition: "interrupted by a session crash, resumed from cache").

**Severity:** Major -- weakens Internal Consistency and Methodological Rigor without invalidating the overall design (the commit-time lint remains a backstop, just a later and coarser one than intended).

**Existing Defense:** Missing -- the eventual commit-time lint (Lint 1) is a real backstop, but it is not named as mitigating *this specific* self-contradiction; it is described as the "otherwise" detection path (design doc line 178), so the contradiction itself is undocumented, not the risk.

**Evidence:** `design/feedback-decision-log-convention-design.md:38` (governing principle) vs. `:178` (self-count mitigation); `design/staging-feedback-logs/feedback-decision-logs-standards.md:28` (same self-count directive, shipped).

**Dimension:** Internal Consistency (0.20) -- a stated first principle is contradicted by the artifact's own interim design without acknowledgment.

**Countermeasure:** Add a one-clause acknowledgment where the self-count directive appears (design doc line 178 and rule file line 28): *"(a deliberate, named exception to the governing principle above, accepted only until the Q3 hook ships)"*. Zero new machinery.

**Acceptance Criteria:** The self-count directive in both the design doc and the rule file carries an explicit acknowledgment that it is a temporary, named exception to the governing principle.

---

### RT-005: No limit on repeated "Graduation: deferred" renewal [MINOR]

**Attack Vector:** LOG-M-004 caps a *first* deferred-graduation cycle at "the next milestone or ~3 months, whichever first" (`feedback-decision-logs-standards.md:26`; design doc line 139), but neither artifact states what happens if, at that checkpoint, the operator simply writes a **new** `Graduation: deferred -- {reason}` note with a fresh 3-month/next-milestone window. This is a plausible vector for indefinitely avoiding H-32 GitHub-Issue-parity ceremony for a decision that should clearly graduate into a worktracker Story/Bug/Enabler, since H-32 attaches "only after graduation" (design doc line 230).

**Category:** Rule Circumvention.

**Exploitability:** Low -- requires deliberate, repeated intent across multiple checkpoints, and the correlated-SPOF disclosure already surfaces checkpoint-skipping as a named, accepted risk.

**Severity:** Minor -- already substantially mitigated by the existence of a periodic re-visibility nudge; the gap is only the absence of an explicit escalation after a *second* deferral.

**Existing Defense:** Partial -- the calendar cap forces periodic re-visibility, but does not prevent renewal.

**Evidence:** `design/feedback-decision-log-convention-design.md:139,230`; `design/staging-feedback-logs/feedback-decision-logs-standards.md:26`.

**Dimension:** Completeness (0.20, minor deduction).

**Countermeasure:** Note (no lint) that a second consecutive deferral on the same entry SHOULD be flagged to the user explicitly at the next checkpoint rather than silently renewed. Documentation-only; MAY mitigate.

---

### RT-006: "References the sidecar key" is ambiguous between inlining and opaque pointer [MINOR]

**Attack Vector:** Design doc line 165: *"When an entry is minted, its Context line references the sidecar key rather than hand-typing the metadata."* This could mean the assistant looks up and inlines the resolved values (robust) or literally writes an opaque `{session_id}#{promptId}` pointer into the Context line in place of `datetime`/`model` (fragile if the sidecar store's own retention is not durable -- itself unaddressed anywhere in the package). The literal entry-schema examples (both templates) show resolved-looking values (`datetime {YYYY-MM-DD}`, `model(s) {model-per-turn}`), suggesting inlining is intended, but the text never says so explicitly.

**Category:** Ambiguity Exploitation.

**Exploitability:** Low -- a documentation-clarity issue, not a live defect (the templates' own worked examples imply the safer reading already).

**Severity:** Minor.

**Existing Defense:** Partial -- resolvable by cross-referencing the templates, but not stated as a rule.

**Evidence:** `design/feedback-decision-log-convention-design.md:165`; `design/staging-feedback-logs/FEEDBACK-LOG.template.md:49` (resolved-looking Context values in the worked example).

**Dimension:** Evidence Quality (0.15, minor).

**Countermeasure:** Add one clause: "...references the sidecar key to source the values below, which are inlined at write time (not stored as a live pointer)."

---

### RT-007: Template states "Corrections are append-only" without the local convention-only hedge [MINOR]

**Attack Vector:** `FEEDBACK-LOG.template.md:24` states *"Corrections are append-only: to fix a verbatim or reopen a `DONE`, add a new entry referencing the old id"* with no adjacent reminder that this is convention-only and git-backstopped, not filesystem-enforced -- a hedge the rule file carries at the same claim (`feedback-decision-logs-standards.md:38`: *"Corrections are append-only (convention-only, git-backstopped — not a filesystem lock; see design doc L1.1)"*). A reader of only the template (the file an operator actually opens to start logging) sees a slightly stronger-sounding claim than the rule file it is meant to summarize.

**Category:** Boundary Violations (a claim crosses from the rule file into the template without carrying its full qualifier).

**Exploitability:** Low.

**Severity:** Minor.

**Existing Defense:** Partial -- the hedge exists one file away (the rule file the template's header links to).

**Evidence:** `design/staging-feedback-logs/FEEDBACK-LOG.template.md:3,24` vs. `design/staging-feedback-logs/feedback-decision-logs-standards.md:38`.

**Dimension:** Internal Consistency (0.20, minor).

**Countermeasure:** Add "(convention-only, git-backstopped)" to the template's phrasing, or leave as-is with documented rationale (templates are meant to be terse and link to the rule file for full nuance) -- a legitimate anti-bloat call either way; flagged for the owner's disposition.

---

## Recommendations

**P0 (MUST mitigate before acceptance):**
- RT-001 -- Propagate Q5's "no proactive detector" disclosure (and the fact that the Q3 hook/backstop does not yet exist) into `feedback-decision-logs-standards.md` at minimum. Acceptance: the phrase appears in the shipped rule file.

**P1 (SHOULD mitigate):**
- RT-002 -- Add an optional `project` sub-field to the Context schema in the rule file and both templates. Acceptance: field present in all three.
- RT-003 -- Add the commit-granularity precondition sentence to the rule file's Segment Rotation section. Acceptance: sentence present.
- RT-004 -- Acknowledge the self-count directive as a named, temporary exception to the governing principle, in both the design doc and the rule file. Acceptance: acknowledgment present in both.

**P2 (MAY mitigate):**
- RT-005 -- Note that repeated deferral renewals SHOULD be flagged explicitly, not silently renewed.
- RT-006 -- Clarify "references the sidecar key" means inline-at-write-time.
- RT-007 -- Either add the convention-only hedge to the template or explicitly accept the terser template wording as intentional (owner call; anti-bloat may justify leaving as-is).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-005: unlimited deferral-renewal is an unaddressed edge case in an otherwise-thorough graduation-cadence design. |
| Internal Consistency | 0.20 | Negative | RT-001 (Critical) and RT-004: a ratified Critical disclosure and a stated governing principle are each contradicted by what actually ships or by the design's own interim mitigation, unflagged. |
| Methodological Rigor | 0.20 | Negative | RT-004: the self-count mitigation was not stress-tested against the design's own first principle before shipping. |
| Evidence Quality | 0.15 | Negative | RT-006: an under-specified mechanism (sidecar reference) leaves the operator to infer intended behavior from worked examples rather than an explicit statement. |
| Actionability | 0.15 | Negative | RT-003: an actionable SHOULD-directive (commit promptly after an edit) that the backstop's own integrity depends on is missing from the artifact operators will actually consult post-install. |
| Traceability | 0.10 | Negative | RT-002: repo-root entries cannot be attributed to an originating project once multiple projects share that surface, despite the design's own acknowledgment that this scenario occurs. |

**Result:** 1 Critical and 3 Major attack vectors identified via adversarial emulation, plus 3 Minor. All seven are addressable with pure text propagation/clarification -- zero new lint, zero new files, zero new subsystems -- fully consistent with the project's established anti-bloat remediation doctrine. Overall assessment: **REVISE required** (RT-001 alone blocks acceptance at the C4 gate per this project's own precedent that a single unmitigated Critical triggers auto-REVISE); the fixes are small, targeted, and should not reintroduce the token-budget growth this project has repeatedly guarded against.
