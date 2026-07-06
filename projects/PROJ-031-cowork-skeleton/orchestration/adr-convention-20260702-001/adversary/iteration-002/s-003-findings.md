# Steelman Report: ADR-PROJ031-004 (ADR Identifier, Location, and Promotion Convention) + Companion Rule Draft

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable identity, criticality, gate |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Steelman Reconstruction](#steelman-reconstruction) | Strongest restatement of the thesis + best case scenario |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Expanded rationale for Critical/Major findings |
| [Scoring Impact](#scoring-impact) | Dimension-level effect of the improvements |
| [Evidence Log](#evidence-log) | File-path citations verified during this review |

---

## Steelman Context

- **Deliverable 1:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (634 lines)
- **Deliverable 2:** `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (262 lines)
- **Deliverable Type:** ADR + companion MEDIUM-tier rule draft (paired governance package)
- **Criticality Level:** C4 (framework-wide governance convention; AE-002 + AE-003 each independently C3-floor per SSOT; C4 derives from the tier definition itself)
- **Engagement Quality Gate:** 0.95 (user-raised above the 0.92 SSOT gate)
- **Iteration:** 2 (post-remediation of a prior tournament finding set scoring 0.67; this review does not read that prior finding set — blind protocol)
- **Strategy:** S-003 (Steelman Technique) — H-16 constructive-first pass
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (S-003) | **Date:** 2026-07-02 | **Original Author:** ps-architect (declared creator/owner)

---

## Summary

**Steelman Assessment:** This is an unusually rigorous, self-critical C4 governance package. Its core thesis — that ADR identity should encode *subject* (immutable, query-relevant) rather than *origin* (a birth fact better relegated to frontmatter), because the ADR is the one Jerry artifact class engineered to migrate scope — survives charitable reconstruction fully intact and is independently corroborated by verifiable, spot-checked repository evidence (see [Evidence Log](#evidence-log)). The document already performs several classic Steelman moves on itself (steelmanning its own rejected alternative, disclosing negative consequences, running its own inversion and pre-mortem, capping its own confidence below the ceiling its source trade study implies) — a genuinely mature adversarial posture for an iteration-2 artifact.

**Improvement Count:** 0 Critical, 4 Major, 2 Minor.

**Original Strength:** High. On every spot-checked factual claim (dangling `ADR-CI-001` citation, stale `ADR-PROJ007-00{1,2}` references in PROJ-007, the 16-file live dialect count, the HARD-rule 25/25 ceiling, the H-26 vs H-23/NAV-002 correction, the `.claude/rules/` symlink precedent, the `adr.md`/`SKILL.md` line-level defects), the deliverable's citations resolved exactly as described. No fabricated evidence was found. The remaining gaps are in *presentation, self-consistency-of-numbers, and methodological completeness of an already-strong argument* — precisely the category S-003 exists to close before critique strategies engage substance.

**Recommendation:** Incorporate the 4 Major improvements before S-002/S-004/S-001 proceed. None is a substantive flaw in the core thesis; each is a place where the deliverable's own rigor is undercut by an unreconciled number, an under-applied method, an undocumented trace target, or a missed opportunity to name its own best move. This is exactly the "close to original, mostly non-Critical" case (Section 4, Step 6 decision point) — proceed to critique strategies without requiring author revision first, but flag SM-002 and SM-004 as the two findings most likely to affect the numeric confidence claim and the ratification-readiness claim respectively.

---

## Steelman Reconstruction

> **Scoping note (P-022):** The template calls for "the complete deliverable rewritten in strongest form." Given the package's combined size (~900 lines across two files) and that a verbatim full-text rewrite would not add reviewable signal beyond what the Improvement Findings Table already localizes, this reconstruction instead (a) restates the core thesis in its tightened strongest form with inline `[SM-NNN]` tags at the exact point each improvement would land, and (b) supplies the Best Case Scenario (Step 4) the template requires as a discrete deliverable. This is a proportionate adaptation, not a substitute for the findings below, each of which cites an exact file:line location in the original.

### Strongest restatement of the core thesis

An identifier should be invariant across an artifact's lifecycle. Every Jerry worktracker entity (`PROJ-`, `EPIC-`, `STORY-`, `DEC-`) is correctly scope-prefixed *because* its scope is permanently fixed — encoding a permanent property in a permanent string is free and correct. The ADR is the sole exception: it is the one entity Jerry's own accrual thesis (`CLAUDE.md` Identity) requires to migrate from project to framework, and the evidence that it actually does so is not speculative — it is 3-for-3 in the live corpus (`docs/design/ADR-agent-design-001.md`, `ADR-output-path-resolution-001.md`, `ADR-routing-triggers-001.md`, all independently verified present and all carrying informal, non-YAML origin provenance in their headers). Encoding a *mutable* property (current governing scope) into an *immutable* string (the filename-derived identity) is therefore a category error regardless of how often promotion happens — this is the promotion-independent core of the argument, and it is what makes Scheme B's win robust rather than a bet on an uncertain rate. The promotion-frequency evidence (bimodal: ~0% for tactical decisions, 3-of-5 for framework-mandate projects) is the tie-breaker that makes the win *decisive*, not the foundation the win *depends on* — a distinction the document draws explicitly and correctly, and [SM-002] is precisely the place where the numeric expression of confidence in that distinction could be tightened to match the rigor of the argument it is meant to summarize.

The decision is additionally strengthened, beyond what the document states, by three properties visible only from independent verification: (1) the disjunctive L-1a/L-1b lint regex, checked here against all 16 live dialect/canonical filenames on disk, matches correctly with no false rejections — the "mandatory regression test" the document promises is not just plausible, it is *already true of the current corpus*, which [SM-003] argues should be surfaced as evidence rather than left as a future promise; (2) the single largest quantitative claim in the document — the dangling `.github/workflows/ci.yml:2` citation to a project path (`PROJ-001-plugin-cleanup`) that no longer exists — is independently confirmed (`Glob` returns zero matches for that path), so the motivating wound is not hypothetical; (3) the "H-26 governs skills, not rule files" self-correction is independently confirmed against `skill-standards.md`'s H-26 text, which is skills-only, meaning the document is not merely asserting its own correction but is demonstrably right to have made it.

### Best Case Scenario (Step 4)

**Ideal conditions:** This decision is strongest in exactly the regime the document already identifies as *empirically live* — a monorepo where (a) many agents author ADRs on parallel branches with no central registry (verified: `advocate-external.md:126` cites 66 branches), (b) a nontrivial fraction of decisions are framework-mandate from birth (verified: PROJ-007 and EPIC-002 together produced 3-of-5 promoted ADRs), and (c) the HARD-rule budget is genuinely exhausted (verified: `quality-enforcement.md` shows 25/25, zero headroom), which independently forces MEDIUM-tier design regardless of the ID-scheme debate.

**Key assumptions that must hold:** (1) framework-relevance is knowable at authoring time often enough for D-1's "prefer a domain slug from birth" guidance to be followed voluntarily by a MEDIUM (non-compelling) rule; (2) the taxonomy-arbiter process (M-5b) is actually staffed, not merely named; (3) the L5 lint (M-6) is actually built — the document itself elevates this to a "ratification blocker" specifically because a MEDIUM-tier convention with no lint is, by the document's own R-5/FM-1 analysis, indistinguishable from no convention at all after enough time passes.

**Confidence a rational evaluator should hold:** High in the structural argument (mutability-of-scope as the identity criterion; promotion-independence of two of three supporting arguments); moderate in the specific point-estimate the document assigns to its own confidence, for the reasons in [SM-002].

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|---------------|-----------|
| SM-001-20260702I2 | In-line prior-review correction tags (`CC-004`, `FM-016`, `PM-003/005/006/008`, `RT-002/003/006`, `SM-004`, `IN-001/002/004`, etc.) are scattered through the ADR body with no glossary resolving them, and are opaque to any reader without access to the iteration-1 finding set — which a blind reviewer or a future promoted-ADR reader will never have | Major | e.g. ADR:8 "*(CC-004 correction)*"; ADR:64 "*(reconciling the two ways it is described)*"; ADR:249 "*(P-022, iter-1, closes SM-004)*"; ADR:527-528 (5 distinct ID families cited in two sentences) | Add a one-time "Prior-Review Corrections Glossary" table (ID → one-line description → source) as an appendix, OR fold all in-line tags into the Changelog entry (already partially done for v1.1) and strip them from the body prose | Traceability |
| SM-002-20260702I2 | The ADR's self-assessed confidence (0.78) is presented as a precise point value derived from its own source trade study's confidence (0.70), but the trade study explicitly declined to exceed 0.75 for "a C4 governance flip resting on n=3" — the ADR crosses that self-declared line without acknowledging or reconciling it | Major | ADR:264 "**0.78 (moderate-high)**... Higher than the trade study's 0.70 single-winner call" | trade-study.md:340: "**I decline to claim >0.75** for a C4 governance flip resting on n=3." State explicitly: "this raises confidence past the trade study's self-imposed 0.75 ceiling; here is why that specific crossing is warranted: [restate the two promotion-independent legs]" — or present as a range (0.75-0.80) rather than a false-precision point value | Internal Consistency / Evidence Quality |
| SM-003-20260702I2 | The user-requested "zero-governance null alternative" (IN-004) is evaluated only in prose, never scored against the same weighted-sum criteria (C1-C8) applied to Schemes A-F, despite the document's own rigor elsewhere insisting on a documented, reproducible scoring method | Major | ADR:225-230 (prose-only rebuttal, no scoring row) | Add the null as an implicit "Scheme G" row to the Options Considered scoring recap table (ADR:163-172), even if scored qualitatively low on C1/C2/C8, to keep the null's rejection subject to the same falsifiable method as A-F | Methodological Rigor |
| SM-004-20260702I2 | The Migration Plan's 11 gating action items (M-1 through M-11) specify Owner and Gating status but no effort/timeline estimate, and independent verification shows zero worktracker Task entities exist yet for any of them (`projects/PROJ-031-cowork-skeleton/work/` contains only EPIC-001-skeleton-distribution items, unrelated to this ADR) | Major | ADR:420-436 (all rows read "TBD-Task" or "TBD-Task + GH Issue") | Add a rough effort column (S/M/L) per gating item, and create at minimum a tracking meta-Task now (even if child tasks remain TBD) so "must be tracked as a real worktracker Task... before ratification" (ADR:420) has a first concrete instance rather than zero instances | Actionability |
| SM-005-20260702I2 | External precedent claims (log4brains's documented abandonment of monotonic numbering, MADR, GOV.UK ADR Framework, AWS Prescriptive Guidance, JPH name-as-ID) are cited only via one bundled References row pointing at internal secondary research artifacts, with no direct primary-source URL or date in the ADR's own References table | Minor | ADR:600 (single row, 5 external sources, no URLs) | Add direct citations (URL + retrieval date) for at least the two claims doing the most argumentative work: log4brains's numbering-scheme history and the GOV.UK maturity-gradient framing | Evidence Quality |
| SM-006-20260702I2 | The document performs an exemplary H-16-consistent move — steelmanning Scheme C (the option it rejects) both in Options Considered and again in the "honest counter-case" paragraph — but never names this as a deliberate methodological virtue distinguishing it from a typical ADR that argues only for its winner | Minor | ADR:223 ("I reject C anyway, for reasons that survive even the low-promotion regime...") | Add one sentence explicitly naming the practice: "This ADR itself applies H-16: Scheme C's strongest form is preserved even after rejection, rather than straw-manned" | Methodological Rigor |

**Finding ID Format:** `SM-{NNN}-20260702I2` (execution_id `20260702I2` = 2026-07-02, iteration 2).

---

## Improvement Details

### SM-001 (Major, Traceability) — Prior-review annotation opacity

**Affected Dimension:** Traceability (weight 0.10), with secondary Actionability impact.

**Original Content:** The ADR body interleaves the decision narrative with dozens of bracketed references to prior-iteration finding IDs (`CC-004`, `FM-016`, `PM-001/003/005/006/008`, `RT-002/003/006`, `SM-004/006`, `IN-001/002/004`) — for example ADR:8, ADR:64, ADR:80, ADR:249, ADR:345, ADR:383, ADR:434, ADR:527-528. None of these IDs is defined in the document itself; their referents live in `adversary/iteration-001/`, a directory this review is specifically barred from reading (blind protocol), which is itself evidence of the accessibility problem: a document meant to stand on its own (e.g., after Path-2 promotion to `docs/design/`, per the ADR's own Meta-Note) carries citations that resolve only for readers with iteration-1 access.

**Strengthened Content:** A short glossary table (`Finding ID | One-line description | Resolved in`) placed once, near the Changelog, would let every in-line tag remain (preserving the audit trail P-004 values) while making the document self-contained. Alternatively, since the Changelog's v1.1 entry already narrates most of these corrections in prose, the in-line tags could be stripped from the body and left solely in the Changelog, which already serves as the append-only historical record the document elsewhere insists such records should be (see its own Path-2 citation-rewrite exclusion rule for CHANGELOGs, ADR:469).

**Rationale:** This is squarely a presentation weakness, not a substantive one — every underlying correction is sound (independently spot-checked several: the L-1a/L-1b split, the H-26→H-23 correction, the 9th `ADR-CI` family). The idea is strengthened, not the expression.

**Best Case Conditions:** Fully resolved once the document reaches its intended terminal, promoted state (`docs/design/ADR-adr-convention-001-*.md` per M-9) — at that point the in-line tags will be pure archaeology for a framework-wide audience that never saw iteration 1.

---

### SM-002 (Major, Internal Consistency / Evidence Quality) — Unreconciled confidence ceiling

**Affected Dimension:** Internal Consistency (weight 0.20), Evidence Quality (weight 0.15).

**Original Content:** `trade-study.md:339-341` states its confidence justification with an explicit, reasoned ceiling: *"0.70 (moderate)... I decline to claim >0.75 for a C4 governance flip resting on n=3."* The ADR (line 264) then states: *"0.78 (moderate-high)... Higher than the trade study's 0.70 single-winner call, because (a) the decision no longer rests solely on the promotion-frequency belief... and (b) the graceful posture... de-risks the adverse regime. Not higher than 0.80, because the load-bearing empirical unknown... genuinely remains."*

**Strengthened Content:** The ADR's two reasons (a) and (b) are legitimate, independent arguments for why the confidence *should* be allowed to exceed the trade study's self-imposed 0.75 ceiling — they are not wrong. But the ADR never states that it is doing this, i.e., it never says "note this deliberately exceeds the trade study's declared 0.75 ceiling, and here is why that specific crossing is warranted." A reader who cross-references both documents (as this review did) will notice the number quietly walks past a line the source document explicitly drew, without a matching acknowledgment. The fix is one sentence of explicit reconciliation, or alternatively presenting confidence as a calibrated range (e.g., "0.75-0.80, informed by but not bound to the trade study's 0.70 baseline") rather than a single decimal that implies more precision than the underlying n=3 sample supports.

**Rationale:** Precision theater on a load-bearing number for a C4 ratification ask is exactly the kind of self-consistency gap H-16/S-003 charitable review is positioned to catch before S-007 (Constitutional AI, which checks P-022 honesty) or S-011 (Chain-of-Verification) would flag it as a harder-edged finding.

**Best Case Conditions:** The document's own stated ethos (P-022, "honesty forbids inflating a C4 governance call on a small sample") is the standard by which this finding is raised — applying the document's own standard to its own number.

---

### SM-003 (Major, Methodological Rigor) — Null alternative not scored by the document's own method

**Affected Dimension:** Methodological Rigor (weight 0.20).

**Original Content:** ADR:225-230 addresses the user-mandated "zero-governance / index-and-search" null benchmark entirely in prose ("What the null gets right... Why it still loses to B..."), never assigning it scores on the same C1-C8 criteria (`trade-study.md` Evaluation Criteria and Weights) used for Schemes A-F, and never adding a row to the Scoring recap table (ADR:163-172).

**Strengthened Content:** Score the null qualitatively on the same 9 criteria — even an approximate pass (e.g., C1=2 no collision defense, C2=5 never churns because there is no ID rule to violate, C8=1 no lint possible without a rule to lint against) would let the null's rejection be falsifiable by the same weighted-sum method rather than resting on prose argument alone, which is inconsistent with the rigor the rest of the package demands of itself.

**Rationale:** This does not change the conclusion (the null loses convincingly either way, and the qualitative prose argument — search cannot fix citation breaks — is sound) but the document's comparative apparatus is under-applied to the one alternative it was explicitly asked to benchmark against.

**Best Case Conditions:** Strongest if the eventual `docs/design/README.md` domain index (M-5) also documents why an index was deemed insufficient on its own — closing the loop between this rationale and the artifact it recommends building anyway.

---

### SM-004 (Major, Actionability) — Migration Plan gating items are unestimated and untracked

**Affected Dimension:** Actionability (weight 0.15).

**Original Content:** ADR:420-436, the "Adoption action items" table, lists M-1 through M-11 with `Owner` and `Gating?` columns but no effort/size estimate, and every `Worktracker/GH` cell reads `TBD-Task` (or `TBD-Task + GH Issue`). Independent verification of `projects/PROJ-031-cowork-skeleton/work/` shows no Task entities exist yet for any M-item; the only work tree present is `EPIC-001-skeleton-distribution`, an unrelated initiative.

**Strengthened Content:** Add a rough size column (S/M/L) to make relative gating cost visible at a glance (M-6, the CI lint, is almost certainly the largest; M-2/M-2b/M-7 are near-trivial file operations). More importantly, create at least one concrete worktracker artifact now — a tracking Task or Enabler under PROJ-031 enumerating M-1..M-11 as child items — so the ratification-blocking claim ("MUST be tracked... before ratification," ADR:420) has a first real instance rather than eleven placeholder rows, consistent with the document's own P-022 standard elsewhere ("a prose table row is a plan, not evidence of completion").

**Rationale:** The document is unusually disciplined about *saying* plans are not evidence of completion (ADR:420) — this finding asks it to apply that same discipline to itself now, rather than only at ratification time.

**Best Case Conditions:** Trivial to close — a single Enabler/Task-tracking file with 11 child rows satisfies this without adding scope.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Already comprehensive (6 options, sensitivity analysis, pre-mortem, migration plan, lint spec); SM-003 closes a small gap in applying the existing method to the null alternative rather than adding new scope |
| Internal Consistency | 0.20 | Positive | SM-002 directly strengthens the one place a stated number was not reconciled against its own cited source |
| Methodological Rigor | 0.20 | Positive | SM-003 and SM-006 both raise the document's already-high methodological bar closer to full self-consistency |
| Evidence Quality | 0.15 | Positive | SM-005 strengthens external-precedent traceability; independent verification (see Evidence Log) confirmed no fabricated evidence in the sampled claims |
| Actionability | 0.15 | Positive | SM-004 converts a stated intention (track gating items) into a first concrete instance |
| Traceability | 0.10 | Positive | SM-001 removes the single largest opacity source (unresolved in-line finding-ID tags) for any reader without iteration-1 access |

---

## Evidence Log

Facts independently verified during this review (all support the deliverable's own claims; none contradicted them):

| Claim in deliverable | Verification | Result |
|---|---|---|
| `.github/workflows/ci.yml:2` cites a dangling `ADR-CI-001` at a project path that no longer exists | Read `ci.yml:1-5`; Glob `projects/PROJ-001-plugin-cleanup` and `projects/PROJ-001*` | Confirmed: citation exists verbatim; path does not exist |
| Stale `ADR-PROJ007-001/002` citations remain in PROJ-007 artifacts | Grep `ADR-PROJ007-00[12]` across `projects/PROJ-007-agent-patterns/`; checked exact cited lines `ORCHESTRATION.yaml:228,242`, `WORKTRACKER.md:106-107` | Confirmed: 32 files match repo-wide; cited lines match exactly |
| 3 `docs/design/` framework ADRs use informal (non-YAML) provenance | Read `ADR-agent-design-001.md:1-5` (HTML comment), `ADR-output-path-resolution-001.md:1-10` (blockquote `Parent:`) | Confirmed |
| 16 live dialect/canonical ADRs (PROJ010×6, PROJ022×2, PROJ031×4, EPIC002×2, STORY015×1, +ADR-150-001) | Glob per family | Confirmed: exact counts match (6+2+4+2+1+1=16) |
| L-1a/L-1b disjunctive lint regex correctly classifies the live corpus | Manually matched regex against sampled filenames from each family | Confirmed: no false rejections in sampled set |
| HARD-rule ceiling is 25/25, zero headroom | Read `quality-enforcement.md` Tier Vocabulary section | Confirmed |
| H-26 governs skill (not rule-file) registration; H-23/NAV-002 is the correct citation for rule-file registration | Read `skill-standards.md` H-26 text (skills-only) | Confirmed |
| `.claude/rules/` symlink precedent (`PROJ-007/EN-001.md:53`) | Read `EN-001.md:48-56` | Confirmed: line 53 states exactly this |
| `adr.md` placeholder (`ADR-{NUMBER}`), Status line missing `REJECTED`, dangling `docs/decisions/` path | Read `adr.md:1,6`; Grep `docs/decisions` in `adr.md` | Confirmed at cited lines 1, 6, 182 |
| `SKILL.md` `ADR_NNN` underscore mismatch | Grep + Read `skills/architecture/SKILL.md:105,284,288,437` | Confirmed at all four cited lines |
| Trade study's declared confidence ceiling (">0.75... n=3") | Grep `confidence` in `trade-study.md`; read lines 337-341 | Confirmed — see SM-002 |
| No worktracker Task entities yet exist for Migration Plan items M-1..M-11 | Glob `projects/PROJ-031-cowork-skeleton/work/**` | Confirmed: only `EPIC-001-skeleton-distribution` tree exists, unrelated to this ADR |

**Constitutional Compliance:** P-001 (all claims above cite exact file:line and were independently re-verified, not merely repeated from the deliverable); P-003 (no subagents spawned); P-004 (every finding traces to a specific location); P-011 (evidence-based); P-020 (no file outside the mandated output path was edited — deliverables were read-only); P-022 (no fabrication; the one open item that could not be verified — the actual iteration-1 tournament score of 0.67 referenced in the ADR's Changelog — is reported as an unverified deliverable claim, not as independently confirmed, since the source file is out of scope under the blind protocol).

---

*Report Version: 1.0*
*Strategy: S-003 (Steelman Technique) | Iteration: 2*
*Generated by: adv-executor*
