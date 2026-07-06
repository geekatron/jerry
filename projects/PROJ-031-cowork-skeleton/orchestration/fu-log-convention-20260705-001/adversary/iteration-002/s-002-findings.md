# Devil's Advocate Report: Feedback & Decision Log Convention (v3, iteration-002)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (blind, iteration-002)
**H-16 Compliance:** **Not independently verifiable this iteration.** The BLIND PROTOCOL for this invocation forbids reading any file under `orchestration/fu-log-convention-20260705-001/adversary/` other than this agent's own output, so no S-003 Steelman output for iteration-002 could be inspected directly. `[INFERENCE]`: the orchestrating workflow's declared strategy order (self-refine → steelman → challenge → verify → decompose → score, per user memory `feedback-adversary-blind-agents`) implies S-003 precedes this S-002 invocation within the same group. This is a documented assumption, not a verified fact — flagged per P-022 rather than silently assumed.

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All findings with severity |
| [Finding Details](#finding-details) | Full evidence for Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 action list |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |

---

## Summary

7 counter-arguments identified (1 Critical, 5 Major, 2 Minor... table below lists 1 Critical / 5 Major / 2 Minor across DA-001..DA-007). The package's core mechanisms (logger-assigned ids, segment rotation, alias preservation) are sound engineering responses to the user's stated FU.5/FU.6 requirements, and most of the growth/ambiguity risk is already disclosed somewhere in the document. The strongest finding (DA-001, Critical) is a direct self-contradiction: the Improvement Ledger claims the id scheme "survives background agents" while the very next section (L1.1) discloses concurrent background-agent writes as an undefended residual risk ("collision-resistant, not collision-proof... detects... rather than prevents"). This is exactly the class of Internal-Consistency defect that scored 0.46 in the iteration-1 tournament per the design doc's own changelog, and it survived the v3 remediation pass. The remaining findings (DA-002 through DA-005, all Major) show that the three named attack vectors — segment-rotation growth, alias/canonical ambiguity, and adoptability by other users — are each *partially* addressed but each also has a genuine, evidenced residual gap the document does not surface with the same prominence as its stated disclosures. Recommend **REVISE**: fix DA-001 (a wording/deletion fix, consistent with the package's own anti-bloat doctrine) before this package can credibly claim the Internal Consistency dimension is closed; DA-002 through DA-005 should get proportionate one-line disclosures, not new machinery.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260706-i002 | Ledger claims id scheme "survives background agents"; L1.1 discloses the opposite (collision-resistant, not collision-proof) | **Critical** | `design/feedback-decision-log-convention-design.md:227` vs `:70` | Internal Consistency |
| DA-002-20260706-i002 | Segment rotation bounds per-file read size but does not solve (only relocates) total-corpus discovery cost; narrative under-discloses this vs. its own "Common cases" admission | Major | `design/...design.md:174-175,234` vs `staging-feedback-logs/examples-appendix.md:168` | Completeness / Evidence Quality |
| DA-003-20260706-i002 | H-31 alias-disambiguation ("enumerate candidate canonical ids") has no alias→canonical index; at scale it requires the same cross-segment scan segment rotation exists to avoid | Major | `design/...design.md:68` vs `design/...design.md:174` (Segment Index row) | Methodological Rigor |
| DA-004-20260706-i002 | Canonical ids and aliases share identical surface syntax (`FU.<n>`); disambiguation only fires inside an LLM-mediated turn, not for bare references in external/human-only contexts | Major | `design/...design.md:63-68`; `staging-feedback-logs/FEEDBACK-LOG.template.md:20` | Completeness |
| DA-005-20260706-i002 | "Single-writer-per-log" is the load-bearing assumption for id uniqueness, asserted not enforced, and never explicitly scoped as a convention limitation for team/multi-operator adoption | Major | `design/...design.md:70,193`; `staging-feedback-logs/feedback-decision-logs-standards.md:27` | Completeness / Actionability |
| DA-006-20260706-i002 | Segment Index's own unbounded growth is hand-waved ("would itself compact... not a real-scale concern") with no specified self-rotation mechanism | Minor | `design/...design.md:174` | Methodological Rigor |
| DA-007-20260706-i002 | No procedure for minting a canonical id when a human edits the log without an LLM in the loop | Minor | `staging-feedback-logs/FEEDBACK-LOG.template.md:22` | Completeness |

**Finding ID Format:** `DA-{NNN}-20260706-i002` (execution id = iteration-002, 2026-07-06).

---

## Finding Details

### DA-001: Ledger overclaims survival of concurrent background-agent writes [CRITICAL]

**Claim Challenged:** Improvement Ledger row 2 (`design/feedback-decision-log-convention-design.md:227`): *"Logger-assigned `FU.N` / `DEC-LLM-NNN` (monotonic across segments) + operator label kept as a verbatim alias + `<scope>:` reference | Removes the round crutch and the observed collision class; the operator never tracks a counter (FU.6); **survives background agents**."*

**Counter-Argument:** This same document, 150+ lines earlier in the L1.1 Id-scheme section (`:70`), states the opposite as a disclosed residual risk: *"Concurrent writers appending to the **same** log file (e.g. parallel/background agents) are a **disclosed residual risk** — the scheme is **collision-resistant, not collision-proof**; it is backstopped by the id-integrity lint (L5 #2), which **detects** a duplicate/gap rather than **preventing** the race."* "Survives" and "collision-resistant, not collision-proof... detects rather than prevents" cannot both be true descriptions of the same mechanism. A reader who only reads the Improvement Ledger (a summary table explicitly framed as the headline pitch "vs `[internal-kb]`") would reasonably conclude concurrent background-agent writes are a solved problem; the detailed section says the opposite. Per the task brief's own standing instruction — "overclaimed coverage IS Critical" — this is exactly that failure mode: a summary claim that is falsified by the document's own detailed disclosure, in the dimension (Internal Consistency) that the design doc's own changelog says scored 0.46 in the iteration-1 tournament (`design/...design.md:290`, v3 entry: *"weakest dimension Internal Consistency (0.46 → overclaims contradicting later disclosures)"*). This specific overclaim was not caught by the v3 remediation pass.

**Evidence:** `design/feedback-decision-log-convention-design.md:227` ("survives background agents") directly contradicted by `:70` ("collision-resistant, not collision-proof... detects... rather than prevents").

**Impact:** If left as-is, a downstream reader (or a future S-014 scorer) relying on the Improvement Ledger as the executive-summary source of truth would carry forward a false safety claim about concurrent-write robustness. It also casts doubt on the trustworthiness of the other 9 rows in the same Ledger table — if row 2 overclaims, a reviewer must now re-verify every other row against its corresponding detail section rather than trusting the table at face value.

**Dimension:** Internal Consistency (0.20 weight).

**Response Required:** Change the Ledger row 2 language from an unqualified "survives background agents" to language consistent with L1.1 — e.g., "collision-resistant (not collision-proof) under single-writer-per-log discipline; concurrent background-agent writes are a disclosed residual risk backstopped by the id-integrity lint." This is a wording-only fix, consistent with the package's own anti-bloat doctrine (no new machinery required).

**Acceptance Criteria:** The Improvement Ledger row and the L1.1 disclosure use consistent, non-contradictory language about what the id scheme does and does not guarantee under concurrent writers. A grep for "survives" or equivalent absolute-safety language in summary tables should not appear unqualified anywhere the same guarantee is hedged elsewhere in the document.

---

### DA-002: Segment rotation bounds per-read size, not total-corpus discovery cost [MAJOR]

**Claim Challenged:** `design/feedback-decision-log-convention-design.md:174` (Improvement Ledger row 9): *"Keeps every log loadable in one Read; cross-log navigation is free via canonical ids (FU.5)."* Also L1.4 table row "Cross-log navigation": *"No file paths in cross-references, no extra machinery — this is the elegant payoff of FU.6's logger-assigned monotonic ids"* (`:175`).

**Counter-Argument:** These framings foreground the part of the problem rotation actually solves (bounding the size of any single Read) but under-state, relative to their prominence, the part it does not solve: discovering an item you cannot already name by canonical id. The document's own `examples-appendix.md:168` "Common cases" answer concedes this directly: *"How do I find 'that feedback about X'? Use the Segment Index to pick the segment, then `grep` the slug / `Disposition: OPEN`."* But the Segment Index (`design/...design.md:174`, row "Segment index") only maps **canonical-id ranges to files** — it carries no content/keyword index. If the searcher does not already know an approximate id or date, "pick the segment" degenerates to grepping across *every* sealed segment file — the same total-bytes scan an unrotated log would require. Segment rotation genuinely fixes the "single Read blows the context budget" failure mode (FU.5's stated problem); it does not fix "find the feedback about X across a multi-year project's history," which scales linearly with total history regardless of rotation. The document states the narrower true claim ("loadable in one Read") but places it alongside language ("cross-log navigation is free... no extra machinery") that a reader could plausibly generalize into "growth is solved," which the document's own Common Cases section shows it is not.

**Evidence:** `design/...design.md:174-175` (rotation/navigation claims) vs. `staging-feedback-logs/examples-appendix.md:168` (grep-fallback answer, which is the only place the full-history-search limitation is stated at all).

**Impact:** An adopter evaluating whether this convention "solves log growth" at face value from the L1.4/Ledger sections could over-trust the mechanism for a use case (historical discovery) it was never built to serve, only discovering the real cost during a real multi-segment `grep -rn` when the project is already large.

**Dimension:** Completeness (0.20) / Evidence Quality (0.15).

**Response Required:** Add one explicit line to L1.4 (not the appendix, which is opt-in reading) stating the scope boundary plainly: segment rotation bounds *single-read* cost; it does not provide a full-text or cross-segment search index, and unindexed historical discovery still costs O(total history). This is a wording addition, not new machinery — consistent with the anti-bloat doctrine already governing the rest of the package.

**Acceptance Criteria:** L1.4's own table (not only the appendix) states the residual discovery-cost limitation with the same prominence given to the other disclosed residual risks in the same section (e.g., "collision-resistant, not collision-proof"; "index growth bounded").

---

### DA-003: The alias-disambiguation mechanism itself requires the cross-segment scan rotation exists to avoid [MAJOR]

**Claim Challenged:** `design/...design.md:68` — *"Back-reference disambiguation (H-31)... The assistant enumerates the candidate canonical ids and asks which one is meant (per H-31), rather than silently inferring from recency."* Reinforced by `examples-appendix.md:167`: *"the assistant lists the candidates (e.g. `FU.0 (alias FU.0)`, `FU.3 (alias FU.0)`, `FU.5 (alias FU.0)`) and asks which one is meant."*

**Counter-Argument:** To "enumerate the candidates" for a repeated alias like `FU.0`, the assistant must find every entry across the *entire* log — including every sealed segment — whose alias suffix matches the queried label. The design specifies exactly one index structure (`design/...design.md:174`, "Segment index" row): a table of **canonical-id ranges per segment file**, rebuildable by `ls`. There is no alias→canonical-id index anywhere in the design (not in the rule file, not in either template, not in the appendix). Consequently, honoring the H-31 mitigation as specified requires scanning every sealed segment's headings for a string match on the alias — precisely the "cross-segment search burden" the segment-rotation mechanism (DA-002) was designed to avoid. The two "earn their place" mechanisms (rotation for read-bounding; H-31 enumeration for alias safety) are therefore in unacknowledged tension: the safer the disambiguation guarantee, the more it depends on the exact operation rotation is supposed to make rare.

**Evidence:** `design/...design.md:68` (enumeration promise) vs. `:174` (only index structure specified, canonical-id-range only, no alias index) vs. `examples-appendix.md:167` (worked example assumes the enumeration "just happens" without specifying the underlying lookup).

**Impact:** For a project still within Segment 1 (< ~50 entries), this is free — the whole log is one Read and enumeration is trivial. The tension only bites once rotation has actually occurred (the exact point at which the convention's other selling point — bounded reads — is supposed to be paying off), which is a real, if delayed, cost the document does not disclose anywhere.

**Dimension:** Methodological Rigor (0.20).

**Response Required:** Either (a) explicitly disclose that alias back-reference resolution after the first rotation degrades to a multi-segment scan (accept it as a residual trade, consistent with the document's own disclosure style elsewhere), or (b) note that the Segment Index could — cheaply, without new lint — carry an optional alias column per entry if this cost proves material in practice. No new mechanism needs to ship now; a one-line disclosure suffices to close the gap honestly.

**Acceptance Criteria:** The H-31 disambiguation passage or the Segment Index row states the scan cost of enumeration after rotation, matching the disclosure rigor already applied to the id-collision and index-growth residual risks in the same table.

---

### DA-004: Canonical ids and aliases are visually indistinguishable outside an LLM-mediated turn [MAJOR]

**Claim Challenged:** The convention's entire disambiguation safety net (`design/...design.md:68`, "the assistant enumerates the candidate canonical ids and asks") depends on an assistant being in the loop at the moment of reference. The task prompt driving this very review is itself a worked instance of the ambiguity: *"does the alias/canonical-id split create ambiguity when the user references 'FU.1' from three turns ago?"* — a bare `FU.1` with no qualifier.

**Counter-Argument:** Canonical ids (`FU.0`, `FU.1`, `FU.2`, ...) and operator aliases (also written as `FU.0`, `FU.0.1`, `FU.1`, ... per `FEEDBACK-LOG.template.md:20`) use the **identical surface token format**. The *only* place the distinction is materialized is the `(alias: ...)` heading suffix inside the log file itself (`design/...design.md:52`, `:66`). Anywhere else a bare `FU.N` appears — a chat message, a commit message, this very adversarial-review prompt, an external design doc, a conversation between two humans without an LLM present — there is no textual signal to tell canonical from alias. The document's own recommended usage ("cross-references SHOULD use the unambiguous canonical `FU.N` / `<scope>:FU.N`," `:68`) is a *style guideline*, not a structural guard: nothing prevents a human from writing a bare `FU.1` believing it canonical when it is their own restarted alias, and the H-31 enumerate-and-ask mitigation (DA-003) only fires when an assistant is actively parsing that reference in a live turn — it does not help a human reading old chat transcript, a commit log, or another human's notes weeks later. This is a real, not-hypothetical instance of the exact scenario the review brief was asked to test.

**Evidence:** `FEEDBACK-LOG.template.md:20` (alias examples use the same `FU.N` token shape as canonical ids); `design/...design.md:68` (mitigation is a recommendation, not an enforced distinguishing syntax); the review-prompt's own phrasing ("FU.1 from three turns ago") is a live demonstration of the ambiguity with no assistant resolution available to the reader of this report.

**Impact:** For the *specific* single-operator-with-continuous-assistant workflow this design was built against, the risk is low (the assistant is present at nearly every reference point). For any adoption path where the log is read or referenced outside an active session — code review, a teammate reading the file cold, a human skimming old FEEDBACK-LOG entries — a bare `FU.N` is genuinely ambiguous with no resolution mechanism available.

**Dimension:** Completeness (0.20).

**Response Required:** State explicitly (one line, in the Id-scheme section or the Common Cases appendix) that bare `FU.N` outside an active assistant-mediated turn is inherently ambiguous by design and that the reader must check the `(alias: ...)` suffix in the actual entry heading to disambiguate — i.e., convert the current implicit assumption into a disclosed, named limitation rather than leaving it discoverable only by testing it against a live example.

**Acceptance Criteria:** The design doc or the standards file states, in one sentence, that the alias/canonical distinction is resolvable only by reading the entry heading (or via H-31 in a live turn) and is not resolvable from a bare `FU.N` token in isolation.

---

### DA-005: Single-writer-per-log is asserted, not enforced, and the convention is never explicitly scoped away from team/multi-operator adoption [MAJOR]

**Claim Challenged:** `design/...design.md:70` and `:193` (LOG-M-005): id uniqueness is guaranteed *"under a single-writer-per-log append discipline."* The design's Purpose/Improvement Ledger frame the deliverable as "a real, lightweight **Jerry convention**" (`:28`) intended for general framework adoption, not a PROJ-031-only artifact (per FU.2's own verbatim request: *"I want this to be a Jerry convention"*, `FEEDBACK-LOG.md:59`).

**Counter-Argument:** "Single-writer-per-log" is a *discipline* (a convention followed voluntarily), not something the design enforces structurally — the only backstop for a violation is the id-integrity lint detecting a collision or gap *after the fact* (`:70`, `:201`). The entire persona the document is written against is "the operator" (singular), modeled directly and explicitly on this one user's stated per-turn habit (FU.6, `FEEDBACK-LOG.md:113-124`). Nowhere does the design state, as an explicit scope boundary, that the convention is validated for and limited to single-human-operator projects, nor does it discuss what breaks (or what changes would be needed) if a second team member also writes feedback into the same project's log, or if a different Jerry adopter's workflow does not route every reference through one continuously-mediating assistant session. The task brief explicitly asks whether this convention is "adoptable by OTHER users than this one" — and the honest answer, on the document's own evidence, is: for a *different individual solo operator* the id-minting mechanism generalizes cleanly (it accommodates any alias habit, not just FU.6's specific restart pattern); but for *team* or *multi-writer* adoption, the design's only defense is a voluntary discipline plus post-hoc lint detection, and this boundary is never named as a boundary.

**Evidence:** `design/...design.md:70` ("single-writer-per-log append discipline"); `:193` (LOG-M-005 restates the same assumption); `staging-feedback-logs/feedback-decision-logs-standards.md:27` (rule text, same assumption, no scope note); `FEEDBACK-LOG.md:113-124` (FU.6, the single-operator persona the whole id scheme is built from).

**Impact:** A second Jerry adopter (or a team evaluating this convention for a multi-contributor project) has no explicit guidance on whether this convention applies to them as-is, needs modification, or is out of scope — they would discover the gap only by hitting an id collision in production, at which point the lint would catch it but the convention offers no guidance on how to recover the discipline going forward (only that the race is "detected... rather than prevented").

**Dimension:** Completeness (0.20) / Actionability (0.15).

**Response Required:** Add one explicit scope statement (in Prerequisites/Purpose-equivalent material, e.g. L1.1 or the standards file header) naming single-operator-per-log as the validated adoption profile, and noting team/multi-writer adoption as an explicitly out-of-scope extension (not a defect, a disclosed boundary — consistent with the anti-bloat doctrine of not building machinery for an unstated requirement).

**Acceptance Criteria:** The design states, in one place, who this convention is validated for (single operator, single continuously-mediating assistant session) and flags multi-operator/team use as a named future extension rather than leaving it undiscussed.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- **DA-001:** Correct the Improvement Ledger row 2 language to match L1.1's own hedged disclosure ("collision-resistant, not collision-proof" / "detects rather than prevents"). Wording-only fix; no new machinery. Acceptance: no unqualified "survives"/absolute-safety claim about concurrent writers remains anywhere in the document while the same guarantee is hedged elsewhere.

**P1 (Major — SHOULD resolve; require justification if not):**
- **DA-002:** Add one line to L1.4 disclosing that rotation bounds per-read size, not total-corpus discovery cost (the appendix already effectively concedes this; promote it to the main narrative).
- **DA-003:** Disclose that H-31 alias-back-reference enumeration degrades to a multi-segment scan once rotation has occurred, or note the Segment Index could optionally carry an alias column if this proves material.
- **DA-004:** State explicitly that a bare `FU.N` is ambiguous outside an assistant-mediated turn or the entry heading itself; this is a one-sentence disclosure, not new syntax.
- **DA-005:** Name single-operator-per-log as the validated adoption profile and flag team/multi-writer use as an explicit out-of-scope extension.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- **DA-006:** Acknowledge (already partially done) that the Segment Index's own growth has no specified self-rotation mechanism; note it as an accepted, disclosed trade at stated scale.
- **DA-007:** Note how a human editing the log without an LLM in the loop should safely mint the next canonical id (or explicitly defer this to the hook/Q3 timeline).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-002, DA-004, DA-005, DA-007: discovery-cost, syntax-ambiguity, adoption-scope, and manual-editing gaps are each real, evidenced, and currently under-disclosed relative to their real-world cost. |
| Internal Consistency | 0.20 | Negative | DA-001: direct, quotable self-contradiction between the Improvement Ledger and L1.1 on the same claim (background-agent survival). This is the dimension the design doc's own changelog names as the weakest in iteration-1 (0.46); this specific instance was not caught by the v3 remediation pass. |
| Methodological Rigor | 0.20 | Negative | DA-003, DA-006: two of the package's own "earn their place" mechanisms (segment rotation, alias disambiguation; segment rotation, index growth) are in unacknowledged tension or have an unspecified recovery procedure at their own stated edge case. |
| Evidence Quality | 0.15 | Negative | DA-002: the document's strongest scalability claims (Ledger row 9, L1.4) are less hedged than the document's own "Common cases" answer, which is evidence the doc contains contradicting its own headline framing. |
| Actionability | 0.15 | Negative | DA-005: no adopter guidance exists for the team/multi-writer case; the only stated recourse is post-hoc lint detection, not a corrective procedure. |
| Traceability | 0.10 | Neutral | All findings above trace to specific line-anchored quotes within the reviewed artifacts; no traceability gap identified in this pass. |

**Overall assessment:** Recommend **REVISE**. All P0/P1 fixes are wording/deletion/one-line-disclosure changes consistent with the package's own stated anti-bloat doctrine — none require new lint, new fields, or new subsystems. DA-001 (Critical) should be resolved before this package can credibly claim its previously-weakest dimension (Internal Consistency) is closed. DA-002 through DA-005 (Major) do not invalidate the design's core mechanisms, which remain proportionate to a MEDIUM-tier convention; they identify real, evidenced residual gaps that the document's own disclosure standard (applied consistently elsewhere: id-collision residual, index-growth residual, transcript-retention residual) has not yet been applied to.
