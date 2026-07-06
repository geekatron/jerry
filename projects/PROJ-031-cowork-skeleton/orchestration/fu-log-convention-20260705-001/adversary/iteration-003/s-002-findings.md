# Devil's Advocate Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention Package

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (blind background agent, iteration-003)
**H-16 Compliance:** No explicit "Prior Strategy Outputs" field was supplied in this invocation's ADV CONTEXT. Proceeding without a HALT because: (a) the project's established process (per session memory `feedback-adversary-blind-agents`) runs a fixed 6-group blind-agent order — self-refine → steelman → challenge → verify → decompose → score — so S-003 (steelman group) precedes S-002 (challenge group) by construction; (b) the deliverable's own Revision Changelog (design doc, "v3"/"v4" rows) documents DA-/RT-/PM- findings already closed in two prior tournament iterations on this same package, which is only possible if S-002 has already executed under this ordering before. This is recorded as a **procedural disclosure, not a verified certificate** — the orchestrator should confirm the current iteration's S-003 artifact exists before scoring this report.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All findings with severity and evidence |
| [Finding Details](#finding-details) | Expanded analysis for each Major finding |
| [Recommendations](#recommendations) | Prioritized action list |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

Six counter-arguments identified (0 Critical, 4 Major, 2 Minor), targeting the three assigned attack vectors: segment-rotation growth economics, alias/canonical-id reference ambiguity, and adoptability by operators other than the one this design was fitted to. **No Critical findings** — the core architecture (two append-only ledgers, logger-assigned monotonic ids, capped-collection segment rotation) withstands scrutiny and the package's extensive prior disclosure discipline (visible throughout the Revision Changelog) correctly anticipates most first-order attacks. The Major findings are all **second-order gaps in an already-disclosed risk**: the design discloses segment-index growth but doesn't complete the math on what it does to per-segment entry capacity; it discloses back-reference ambiguity but the stated H-31 mitigation doesn't explicitly cover the canonical-vs-alias collision case; and it discloses the single-operator validation scope but only below the L0 fold, on a deliverable explicitly framed as becoming "a Jerry convention." Recommendation: **REVISE** (wording/disclosure fixes only — consistent with this package's own anti-bloat doctrine; none of these findings require new machinery).

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter003 | Segment Index growth is measured in isolation ("well under the cap") but never netted against the same 800-line cap it shares with real entries — the design's own "~50 entries converges with ~800 lines" claim silently degrades as the log ages | Major | design doc L1.4 table rows "Cap" and "Segment index" | Completeness |
| DA-002-iter003 | The segment-index-growth "not a real-scale concern" dismissal is the *only* deferred/edge-case item in the whole package with no concrete re-assessment trigger, breaking the design's own established pattern (Q3 hook, Backfill staleness, install-stall all get one) | Major | design doc L1.4 (Segment index row); contrast with lines re: Q3 re-assessment trigger, Backfill staleness trigger, install-stall trigger | Internal Consistency |
| DA-003-iter003 | The H-31 back-reference disambiguation protocol is specified only as "enumerate entries whose *alias* matches the bare reference" — it does not instruct also checking whether the bare token is itself a live *canonical* id with a *different* alias, exactly where the design elsewhere tells users canonical ids are "the unambiguous" reference form | Major | design doc L1.1 (Back-reference disambiguation / Bare `FU.N` bullets); `examples-appendix.md` Common Cases | Methodological Rigor |
| DA-004-iter003 | L0 headline (improvement #2) presents the logger-assigned-id + alias scheme as a strict win over manual numbering without surfacing, at the same summary tier, the back-reference friction it introduces (disclosed only ~40 lines later in L1.1) | Minor | design doc L0 line ~36 vs. L1.1 lines ~70-71 | Traceability |
| DA-005-iter003 | The convention's validated adoption scope — "single operator per log," team/multi-writer explicitly out-of-scope — is disclosed only in L1.1/Scoping and the rule file, never in L0, even though the deliverable proposes installing into `.context/rules/` as a durable "Jerry convention" and Jerry's own trajectory (per project memory) is toward external plugin distribution | Major | design doc L1.1 "Adoption profile" bullet, `feedback-decision-logs-standards.md` "Scoping" section; absence check against L0 §28-43 | Completeness |
| DA-006-iter003 | The flagship FU.6 alias/canonical fix is validated only against a synthetic example (`examples-appendix.md` "Ids & aliases before/after"); the project's own real bootstrap data (FU.0-FU.9) contains zero actual alias collisions, so the mechanism this whole package leans on has not yet been exercised against real data | Minor | `examples-appendix.md` "Ids & aliases (before/after)" block; `FEEDBACK-LOG.md` FU.0-FU.9 (no repeated alias observed) | Evidence Quality |

**Finding ID Format:** `DA-{NNN}-iter003` (iteration-003 execution).

---

## Finding Details

### DA-001: Segment Index growth is unbudgeted against its own cap [MAJOR]

**Claim Challenged:** Design doc L1.4 table, "Segment index" row: *"Index growth is bounded to ≈1 row / 50 entries: a 10k-entry log yields ~200 rows (~200 lines) — well under the cap; at an implausible extreme it would itself compact into a sealed index segment (not a real-scale concern)."* Paired with the "Cap" row's convergence claim: *"50 entries is the human-eyeballable trip-wire; measured ~12–18 lines/entry lands the two thresholds together."*

**Counter-Argument:** These two rows are analyzed independently, but they interact. The Segment Index (and the Backfill Queue) live **only in the ACTIVE file** (explicitly stated at L1.1 line 74 and the rotation procedure step 1: "The Backfill Queue and Segment Index sections are not copied"), and the cap-check lint counts **the whole ACTIVE file's lines**, not just entry lines (`feedback-decision-logs-standards.md` L5 lint 1: "the same pass (counting both lines and `## FU.N` / `## DEC-LLM-NNN` headings) flags the ACTIVE file over the ~800-line or ~50-heading cap"). So every new segment's 800-line budget must be shared between fixed overhead (nav table, header), the Segment Index (which grows monotonically, 1 row per prior segment), the Backfill Queue (grows until reviewed), and new entries. At the design's own cited scale (10k entries → ~200 segments → ~200-line index), that segment's *available* budget for actual entries is ~600 lines, not 800 — roughly **40 entries at 15 lines/entry, not the claimed 50**. The "well under the cap" framing is true of the index's absolute size but never nets it against the entry capacity it displaces, so the "50 entries / 800 lines converge" claim used to justify the cap thresholds throughout the document quietly stops holding exactly in the long-running-log scenario segment rotation exists to serve (FU.5's own stated problem: "long running sessions and/or projects").

**Evidence:** design doc lines 176 and 180 (L1.4 table); `feedback-decision-logs-standards.md` L5 Lint item 1 (line 65).

**Impact:** Not a correctness failure (the lint still fires and rotation still happens — no entry is ever lost or a Read ever overflows). It is a **quantitative overclaim**: the document asserts a convergence that its own OR-based cap mechanics don't preserve at the scale the document itself uses as its worked example (10k entries). This is precisely "does segment rotation solve the growth problem or shard it" — segment rotation *shards* the read-size problem successfully, but the design's own proof that the shards stay a predictable size is incomplete.

**Dimension:** Completeness

**Response Required:** Either (a) exclude Segment Index / Backfill Queue lines from the cap check (only count entry-heading lines against the ~800/~50 thresholds), or (b) explicitly net the index's line cost against per-segment entry capacity and restate the convergence claim with the corrected numbers (or accept and disclose the drift, e.g. "each segment holds slightly fewer entries as the log ages; capacity floor is bounded by [formula]").

**Acceptance Criteria:** The design doc's Cap/Segment-index rows either share one worked calculation that accounts for index+backfill overhead, or explicitly state the lint counts entry headings only (not raw lines) so the interaction is moot.

---

### DA-002: The one deferred edge case with no re-assessment trigger [MAJOR]

**Claim Challenged:** Design doc L1.4, Segment index row: *"at an implausible extreme it would itself compact into a sealed index segment (not a real-scale concern)."*

**Counter-Argument:** This package has an established, repeatedly-applied house pattern for exactly this kind of deferred risk: give it a concrete, dated or event-based re-assessment trigger rather than an open-ended "not a concern." The design does this for the Q3 hook ("**Re-assessment trigger (not an open-ended 'someday')**... revisit the deferral at the first segment rotation, or after a fixed cadence checkpoint... or the first time a missed capture is discovered incidentally"), for Backfill Queue staleness ("**Staleness trigger (not open-ended):** Backfill Queue rows carry an added-date and are re-assessed at the same commit-cadence checkpoint... or sooner if a row's source... is observed to have rotated"), and for install-stall ("If the design is not ratified within a bounded window... the owner flags the stall at the next commit-cadence checkpoint"). The Segment Index growth dismissal is the sole deferred item in the entire package that gets neither a numeric revisit condition nor an event trigger — just "not a real-scale concern," which is exactly the unbounded-deferral language the document elsewhere goes out of its way to reject.

**Evidence:** design doc L1.4 Segment index row vs. the three counter-examples of re-assessment triggers cited above (Q3 hook, Backfill staleness, install-stall — all in the same document's L2/Adoption sections).

**Impact:** Minor in isolation, but it is a genuine internal-consistency gap — the same author, in the same document, treats structurally identical "I'm dismissing an edge case for now" situations inconsistently. Since this deliverable's Revision Changelog explicitly prizes closing findings by disclosure-with-a-trigger rather than silent deferral, this is the one spot where that discipline lapsed.

**Dimension:** Internal Consistency

**Response Required:** Add a one-line re-assessment trigger for the Segment Index dismissal, mirroring the existing pattern (e.g., "revisit if the index ever exceeds N rows / M lines in one segment, or at the same commit-cadence checkpoint used elsewhere").

**Acceptance Criteria:** The Segment index row (or L1.4 prose) carries an explicit, non-open-ended revisit condition matching the shape already used for Q3/Backfill/install-stall.

---

### DA-003: H-31 disambiguation is specified for alias collisions, not canonical/alias collisions [MAJOR]

**Claim Challenged:** Design doc L1.1: *"Because aliases repeat, a later bare-alias reference... is ambiguous — the same alias maps to several canonical ids across turns. The assistant enumerates the candidate canonical ids and asks which one is meant (per H-31)... Cross-references SHOULD use the unambiguous canonical `FU.N` / `<scope>:FU.N`."* And `examples-appendix.md` Common Cases: *"'What's the status of FU.0?'... the assistant lists the candidates (e.g. FU.0 (alias FU.0), FU.3 (alias FU.0), FU.5 (alias FU.0))... Referencing the canonical FU.N avoids the round-trip."*

**Counter-Argument:** The design explicitly tells users/assistants that a *canonical* `FU.N` reference is unambiguous and should be preferred to avoid the disambiguation round-trip — i.e., canonical-id usage is a sanctioned, expected reference pattern, not a hypothetical. But because canonical ids and aliases **share the same surface syntax** (design doc L1.1: "the only structural disambiguator is the `(alias: …)` suffix in the entry heading itself"), a bare token like `FU.7` is textually indistinguishable from either intent. The disambiguation procedure as written only describes searching for entries whose **alias** equals the bare token. It does not instruct also checking whether the bare token is itself a **live canonical id** attached to a *different* alias. Concretely: if canonical `FU.7` exists with `(alias: FU.0.3)`, and separately some other entry happens to have `(alias: FU.7)`, a user who was told earlier "logged as canonical FU.7" and later says "what about FU.7?" is doing exactly what the design recommends (using the canonical form) — yet an alias-only enumeration search would surface the *other* entry (the one whose alias literally is "FU.7") and could omit the canonical FU.7 entry the user actually means, since its alias doesn't textually match "FU.7" at all. The protocol description never names this second search axis.

**Evidence:** design doc L1.1 (Back-reference disambiguation, "H-31" bullet, and the "only structural disambiguator" bullet); `examples-appendix.md` Common Cases (canonical-reference recommendation).

**Impact:** This is squarely the requested attack ("does the alias/canonical-id split create ambiguity when the user references FU.1 from three turns ago") landing on the one case the design's own mitigation doesn't fully cover: a user who *did the recommended thing* (used the canonical id) can still be met with a candidate list that omits the entry they mean, because the search is specified as alias-only. In practice a capable LLM executing this protocol would likely check both axes without being told — but the document is the ratifying artifact and MUST NOT leave a load-bearing correctness property to implementer inference, especially for a mechanism the package repeatedly cites as its primary defense against reference ambiguity.

**Dimension:** Methodological Rigor

**Response Required:** Add one sentence to the H-31 bullet: the enumeration search MUST check both (a) entries whose alias matches the bare token, and (b) whether the bare token is itself a live canonical id (which should be reported as its own distinct candidate, not merged with alias-matches).

**Acceptance Criteria:** L1.1's back-reference disambiguation bullet (and/or the appendix Common Cases entry) explicitly names both search axes.

---

### DA-005: Single-operator validation scope is disclosed but not surfaced where a ratifier reads first [MAJOR]

**Claim Challenged:** L1.1: *"Adoption profile (validated scope, a disclosed boundary — not a defect). The convention is validated for a single operator per log with a continuously-mediating assistant session... Team / multi-writer adoption is an explicit out-of-scope extension."* This sentence, and its Scoping-section counterpart, is the **only** place this constraint appears; L0 (§28-43, the Executive Summary the user/ratifier is most likely to read in full) never mentions it.

**Counter-Argument:** This deliverable is explicitly framed, in the user's own verbatim requirement (FU.2, quoted in the design doc's own References/FEEDBACK-LOG): "I want this to be a Jerry convention." The Adoption/migration plan proposes installing the rule file into `.context/rules/` — a framework-wide location, not a project-scoped one — and this project's own memory record shows Jerry is actively moving toward external distribution (a Claude-plugin repo intended for other users). A convention destined for `.context/rules/` and framed at L0 as *the* Jerry answer to "don't lose feedback" is, by the document's own admission, validated for exactly one operator's habits and explicitly refuses to address multi-writer/team use — yet nothing in the L0 summary a ratifier is likely to skim signals that scope boundary. This is not a claim that the mechanism is *broken* for other single operators (the logger-assigned-id core generalizes reasonably); it is that the **claim of general "Jerry convention" status is made at the level a reader is most likely to act on, while the scope boundary that would qualify that claim is one section-and-a-half down.**

**Evidence:** design doc L1.1 "Adoption profile" bullet; `feedback-decision-logs-standards.md` "Scoping" section ("Adoption profile: validated for a single operator per log... Team/multi-writer use is an explicit out-of-scope extension"); absence check against L0 (lines ~28-43, no operator-count qualifier anywhere in that span).

**Impact:** For the current single adopter this is low-risk (they ARE the validated case). For anyone else who later reads the ratified rule file expecting a general framework capability, the "single operator" ceiling is a load-bearing scope fact that belongs in the same paragraph as the claim it qualifies, not one section removed.

**Dimension:** Completeness

**Response Required:** Add a one-clause qualifier to the L0 headline or the opening paragraph (e.g., "validated for single-operator adoption; team/multi-writer use is out of scope — see L1.1") so the scope constraint travels with the "Jerry convention" claim at the same reading tier.

**Acceptance Criteria:** L0 contains an explicit single-operator scope qualifier, or the rule file's own header (which already carries several qualifiers) gains one more clause naming the adoption-profile limit.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):** None.

**P1 (Major — SHOULD resolve; require justification if not):**
- **DA-001:** Either exclude Segment Index/Backfill lines from the cap-line-count, or restate the "50 entries / 800 lines" convergence claim with index overhead netted in.
- **DA-002:** Give the Segment Index growth dismissal the same re-assessment-trigger treatment already used for Q3/Backfill/install-stall.
- **DA-003:** Extend the H-31 disambiguation bullet to explicitly cover the canonical-id-as-bare-token search axis, not only alias matches.
- **DA-005:** Surface the single-operator validated-scope qualifier at L0 (or in the rule file's opening blockquote), not only in L1.1/Scoping.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- **DA-004:** Optionally add a half-sentence at the L0 FU.6 bullet pointing to the L1.1 disambiguation cost ("...operator never tracks a counter — see L1.1 for the back-reference disambiguation tradeoff this introduces").
- **DA-006:** Optionally note in the appendix that the alias-collision example is synthetic (no real collision yet observed in the bootstrap logs), so a future reader doesn't mistake it for an already-exercised case.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-001 (cap-convergence math incomplete for aged logs), DA-005 (adoption-scope constraint omitted from L0) |
| Internal Consistency | 0.20 | Negative | DA-002 (segment-index dismissal breaks the document's own re-assessment-trigger pattern) |
| Methodological Rigor | 0.20 | Negative | DA-003 (H-31 disambiguation procedure under-specified for the canonical-vs-alias collision case) |
| Evidence Quality | 0.15 | Negative | DA-006 (flagship alias/canonical fix validated only synthetically, not against the project's own real entries) |
| Actionability | 0.15 | Neutral | All findings carry concrete, low-cost (wording-only) fixes consistent with the package's own anti-bloat doctrine; no new machinery required |
| Traceability | 0.10 | Negative | DA-004 (L0 claim and its qualifying L1.1 disclosure are not co-located, weakening the summary-to-detail trace a ratifier would follow) |

**Result:** 0 Critical, 4 Major, 2 Minor. All fixes are disclosure/wording-level, in keeping with the deliverable's stated anti-bloat posture — none require new lint checks, new fields, or new subsystems. The core segment-rotation and id-scheme architecture is sound; the gaps are in the completeness of its own stated math (DA-001/002) and in one under-specified corner of its flagship disambiguation mechanism (DA-003), plus a documentation-prominence gap on adoption scope (DA-005) that matters specifically because this package is headed toward `.context/rules/` in a framework with an active external-distribution trajectory.
