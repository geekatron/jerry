# Pre-Mortem Report: ADR Identifier, Location, and Promotion Convention (ADR-PROJ031-004 + adr-standards-rule-draft.md)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy metadata, H-16 compliance disclosure |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All PM-NNN failure causes, prioritized |
| [Finding Details](#finding-details) | Full evidence/analysis per Critical and Major finding |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 six dimensions |
| [What the Package Already Prevents](#what-the-package-already-prevents) | Credit for existing mitigations |

---

## Header

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, iteration 5)
**H-16 Compliance disclosure:** Per the BLIND PROTOCOL I cannot read `.../adversary/iteration-00N/s-003-*.md` files from any iteration, so I cannot independently confirm a discrete per-iteration S-003 artifact exists for iteration 5. The deliverable itself discloses (ADR lines 65-68) that S-003 influence is "embedded, not separately-tagged" — every Option A-F in the ADR's Options Considered section leads with a blind advocate's steelman (sourced from `explore/advocate-*.md`, ADR References #2-4), and the owner explicitly states they cannot self-verify per-iteration orchestrator execution. Treating this honestly (P-022): the deliverable is demonstrably strengthened-before-critiqued in substance (Options A-F all carry genuine steelmans, including the losing Scheme E), so I proceed with Pre-Mortem on that basis rather than halting, while flagging that I cannot certify iteration-5-specific S-003 execution from outside the blind boundary.
**Failure Scenario:** It is 2027-07-02. The convention has failed in four compounding ways: (1) the companion rule file, meant to be lightweight auto-loaded guidance, is known among contributors as "the giant ADR file" that gets skimmed or collapsed by session-start attention budgets; (2) `ps-architect` (the sole ADR-producing agent) is *still* emitting `{ps_id}-{entry_id}-adr-{slug}.md` files, because the Tier-2 fix that would correct it was never prioritized once Tier-1 "shipped" and the team declared victory; (3) new ADRs mix bare-`NNN`, dialect, and domain-slug forms because the lint never ran in CI; (4) downstream CoWork/plugin adopters received the guidance file but no enforcement, ever. Governance is now debating whether the convention was worth adopting at all.

---

## Summary

This package is unusually self-aware — it already contains 4 iterations of adversarial remediation and a self-authored Pre-Mortem/FMEA section (FM-1..FM-4). My job as an independent iteration-5 blind reviewer is to find failure paths *not yet examined*, including regressions introduced by the package's own prior fixes. I found **7 failure causes**, including **2 Critical (P0)** that the existing self-critique does not cover: (1) the companion rule file scheduled for permanent `.context/rules/` auto-load is measured at roughly 25,600+ tokens for just 83% of its length — likely 30,000+ tokens total, dwarfing the framework's own documented ~12,500-token L1 session-start rule budget, an ironic instance of Context Rot from a document meant to fight governance rot; and (2) the iteration-4 "two-tier ratification" fix (designed to un-block free guidance value) has a side effect nobody pre-mortem'd: it lets `status: ACCEPTED (guidance)` ship while the sole ADR-producing agent remains verified, present-tense non-compliant, with no deadline on the Tier-2 fix that would correct it — reproducing the exact "convention becomes a suggestion nobody follows" failure the package already fears, at higher likelihood than before the split existed. **Recommendation: REVISE** — both P0 items are cheaply fixable (trim/relocate the rule file; add a G-1.5-style condition requiring the producing-agent fix before Tier-1 status flips to ACCEPTED) and should be closed before ratification proceeds.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260702-I5 | Companion rule file (`adr-standards.md`) scheduled for permanent L1 auto-load is measured at ~25,600+ tokens for 83% of its length -- likely 30,000+ tokens total, vs. the framework's documented ~12,500-token L1 budget | Technical/Resource | High | Critical | P0 | Completeness |
| PM-002-20260702-I5 | Two-tier ratification split (iter-4 fix) lets `status: ACCEPTED (guidance)` ship while the sole ADR-producing agent (`ps-architect.md`) remains verified non-compliant, with no deadline on the Tier-2 fix | Process | High | Critical | P0 | Actionability |
| PM-003-20260702-I5 | The one already-runnable, zero-cost collision safeguard (the pre-flight `sort \| uniq -d` one-liner) lives only in the parent ADR, not in the auto-loaded companion rule file | Process | High | Major | P1 | Actionability |
| PM-004-20260702-I5 | Unmeasured assumption that a MEDIUM-tier SHOULD convention changes agent/author behavior absent HARD enforcement, when the package's own evidence (ps-architect.md) argues the opposite | Assumption | High | Major | P1 | Evidence Quality |
| PM-005-20260702-I5 | M-9 (this ADR's own self-promotion) is gated "on acceptance" without stating whether that means Tier-1 or Tier-2 acceptance under the newer two-tier model | Process | Medium | Major | P2 | Internal Consistency |
| PM-006-20260702-I5 | Downstream CoWork/plugin adopters receive Tier-1 guidance (ships via `.context/rules/`, not stripped) but zero enforcement backstop for an indefinite period, and sit outside `@geekatron`'s CODEOWNERS reach entirely | External | Medium | Major | P2 | Actionability |
| PM-007-20260702-I5 | WARN-class lint rules (L-5/L-6/L-6c) will fire persistently against the 3 existing framework ADRs until the separately-gated M-11 retrofit also lands, risking alert fatigue that could mask a genuinely new L-14 producer-drift violation | Technical | Medium | Minor | P2 | Traceability |

**Finding ID Format:** `PM-{NNN}-20260702-I5` (iteration 5, 2026-07-02).

---

## Finding Details

### PM-001: Companion Rule File Is Scheduled for Permanent L1 Auto-Load at an Estimated 30,000+ Tokens [CRITICAL]

**Failure Cause:** `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` is the literal content that becomes `.context/rules/adr-standards.md` on ratification ("this content -- minus this wrapper note -- becomes `.context/rules/adr-standards.md`," `adr-standards-rule-draft.md:3`), and per CLAUDE.md's own Navigation semantics, `.context/rules/` files are marked "(A) = Auto-loaded into Claude Code context at session start via `.claude/rules/` symlink" (`CLAUDE.md` Navigation table) -- confirmed structurally correct by the ADR's own PM-101 fix ("`.claude/rules` is a directory-level symlink... any file authored under `.context/rules/` is exposed automatically," `ADR-PROJ031-004-adr-identifier-convention.md:526`, M-2b). When I read `adr-standards-rule-draft.md` with `Read(offset=0)`, the tool's own truncation message reported: "showing lines 1-270 of 326 total (25609 tokens, cap 25000)" -- i.e., 83% of the file already consumes ~25,600 tokens (~95 tokens/line), implying a full-file token count on the order of 30,000+ tokens. This is not a stylistic quibble: `.context/rules/quality-enforcement.md`'s Enforcement Architecture table states the entire L1 layer ("Session start... Behavioral foundation via rules") is budgeted at **~12,500 tokens total** across all 17 existing `.context/rules/` files combined. Adding this one file, unmodified, would roughly triple that budget on its own.

**Category:** Technical/Resource
**Likelihood:** High -- this is a measured fact from the current draft, not a projection, and the Migration Plan (M-2, `ADR-PROJ031-004-adr-identifier-convention.md:525`) instructs authoring the live rule file directly "from Deliverable 2," with no trim, condensation, or token-budget review step named anywhere in the 14-row Migration Plan.
**Severity:** Critical -- the framework's own stated Identity/Core Problem is "Context Rot -- LLM performance degrades as context fills" (`CLAUDE.md` Identity). A convention whose entire purpose is preventing citation/governance rot would, if shipped as drafted, materially *worsen* the exact problem the framework exists to fight, at every single session start, for every user, forever (not a one-time cost). This also directly threatens the convention's own practical adoption: a rule file this dense is the textbook precondition for being skimmed, collapsed, or ignored -- i.e., it is a structural contributor to the very "PROPOSED convention becomes a suggestion nobody reads" failure mode (FM-1) the package already tracks, via a mechanism (L1 token bloat) FM-1 does not name.
**Evidence:** `adr-standards-rule-draft.md:1-326` (measured token density via Read-tool truncation at offset 0); `CLAUDE.md` Navigation table "(A)" annotation; `.context/rules/quality-enforcement.md` Enforcement Architecture table (~12,500 token L1 budget, 5-layer table); `ADR-PROJ031-004-adr-identifier-convention.md:525-526` (M-2/M-2b).
**Dimension:** Completeness (the Migration Plan's 14 rows omit a token-budget/condensation step entirely)
**Mitigation:** Before M-2 executes, run a dedicated condensation pass on the rule draft: move the extensive per-line P-022 correction narrative, iteration disclosures, and rationale prose (currently interleaved with the normative ADR-M-001..013 rows) into a Level-3 reference document (e.g., `docs/knowledge/exemplars/adr-standards-rationale.md`), leaving `.context/rules/adr-standards.md` as a lean, MEDIUM-tier rule file matching the size profile of comparable files (e.g., `mcp-tool-standards.md`, `error-handling-standards.md` are both under 100 lines). This is exactly the pattern the framework already uses for its own skill documentation (`skill-standards.md`'s "Progressive Disclosure" table: "Level 3 (references/): Detailed docs... loaded only as needed").
**Acceptance Criteria:** The file actually installed at `.context/rules/adr-standards.md` measures under ~1,500 tokens (comparable to the shortest existing `.context/rules/*.md` files), with detailed rationale/disclosure content relocated to an on-demand reference, before M-2 is marked complete.

---

### PM-002: Two-Tier Ratification Split Permits `ACCEPTED (guidance)` While the ADR-Producing Agent Remains Verified Non-Compliant, With No Deadline [CRITICAL]

**Failure Cause:** The iteration-4 "two-tier ratification" redesign (`ADR-PROJ031-004-adr-identifier-convention.md:89-98`, tagged IN-001/PM-001) decouples `status: PROPOSED -> ACCEPTED` into Tier 1 (guidance, gate = **G-1 only**, "a human approval recorded on the ratifying PR/commit," line 104) from Tier 2 (enforcement, gate = G-2..G-4, including **G-3**: "the producing agent (`ps-architect.md`, M-12) emits compliant IDs," line 111). This means Tier-1 `ACCEPTED (guidance)` status requires *nothing* about the producing agent's actual behavior. I independently verified (outside the blind boundary, permitted per task instructions) that `skills/problem-solving/agents/ps-architect.md` is, as of this review, still fully non-compliant with the very grammar this ADR decides: line 218 hardcodes `# ADR-{NUMBER}: {Title}` (matches neither the canonical nor dialect grammar), line 260 mandates writing to `projects/${JERRY_PROJECT}/decisions/{ps_id}-{entry_id}-adr-{slug}.md` (the ungoverned 10th filename grammar the ADR itself names as a defect, `ADR-PROJ031-004-adr-identifier-convention.md:537` M-12), and line 267 references a phantom `python3 scripts/cli.py` (also H-05-violating). The fix for this (Fix 3 / M-12) is explicitly a **Tier-2, non-gating-for-Tier-1** item (M-12 maps to G-3, which is *not* part of the Tier-1 gate). Unlike the package's own monitored residuals (e.g., PM-009's "re-examine after 2-3 more framework projects," R-6's "≥2 collisions in 90 days" threshold, line 480), **Tier 2 carries no deadline, no escalation trigger, and no time-boxed review commitment anywhere in the document.** Combined with the disclosed single-CODEOWNERS reality (`@geekatron` alone, `ADR-PROJ031-004-adr-identifier-convention.md:676`), the same bottlenecked party who can ratify Tier 1 in minutes is also the sole party who must build the lint, fix the agent, and staff the taxonomy arbiter -- with zero forcing function connecting the two once Tier 1 ships.

**Category:** Process
**Likelihood:** High -- this is not speculative: the producing agent's non-compliance is a verified, present-tense fact (not a future risk), the Tier-2 gate that would fix it has no deadline, and the package's own FM-1/FM-3 pre-mortem entries (line 492, 494) already independently worry about exactly this outcome ("the L5 lint was never implemented; the convention stayed a suggestion" / "authors overused the project dialect... the promotion-rename tax reappeared") -- meaning the *mechanism* enabling that outcome is now demonstrably present, at a higher-than-previously-assessed likelihood, because the very fix (Tier split) that was supposed to unblock guidance value also removed the pressure that would have forced Tier 2 to completion.
**Severity:** Critical -- this would invalidate the ADR's own headline claim that "the convention can start delivering value immediately" upon Tier-1 ratification (`ADR-PROJ031-004-adr-identifier-convention.md:95`), because the majority of new ADRs are agent-produced (via `/problem-solving` -> `ps-architect`), not hand-typed by a human who happens to have read the new rule file. If the agent is not fixed, "guidance ships immediately" is true only for the minority of ADRs a human names by hand -- a materially weaker claim than the document asserts, and exactly the "nobody follows it" failure the invoking task's pre-mortem framing names directly.
**Evidence:** `skills/problem-solving/agents/ps-architect.md:218,260,267` (verified non-compliant, present tense); `ADR-PROJ031-004-adr-identifier-convention.md:93-98,104,111,531,537` (Tier gate table, M-6/M-12 gating); no deadline/escalation clause found for Tier 2 anywhere in the Ratification Gate section (lines 85-117) or Migration Plan (lines 501-540), by contrast with the explicit deadlines given for PM-009/R-6 (lines 479-480).
**Dimension:** Actionability (the Tier-1 gate, as specified, cannot actually deliver its claimed "value immediately" for agent-produced ADRs)
**Mitigation:** Add a lightweight Tier-1.5 condition: Tier-1 `ACCEPTED (guidance)` status flip requires, in addition to G-1, a *time-boxed* commitment record (e.g., "Tier-2 G-3 producing-agent fix targeted within N days of Tier-1 ratification, tracked as a worktracker Task with a review-by date," mirroring the `expires`/`review_by` pattern already used for waivers and the R-6 90-day threshold) -- not full G-3 completion, just a deadline and an owner, so Tier-1 acceptance cannot be mistaken by future readers for "the convention is now generally true of agent-produced ADRs."
**Acceptance Criteria:** The Ratification Gate section states an explicit review-by date for G-3 (producing-agent fix) at the moment Tier-1 flips to ACCEPTED, and that date is tracked as a worktracker Task per H-32.

---

### PM-003: The Zero-Cost Pre-Flight Collision Check Is Not Reproduced in the Auto-Loaded Rule File [MAJOR]

**Failure Cause:** `ADR-PROJ031-004-adr-identifier-convention.md:414-425` documents a runnable, zero-new-tooling bash one-liner (`find ... | sort | uniq -d`) that any author can run *today*, before M-6 ships, to catch slug collisions pre-commit (labeled FM-018). I grepped `adr-standards-rule-draft.md` for "pre-flight" / "FM-018" and found only one unrelated hit (line 285, a mention that the *agent* "MAY surface a pre-flight `uv run jerry lint adr` warning" -- a different, Tier-2-gated CLI concept, not the bash one-liner). The actual collision-check command that requires zero new tooling and could protect authors from day one of Tier-1 guidance is documented exclusively in the parent ADR's "L1: Technical Implementation" section -- a document that is **not** the artifact scheduled for session-start auto-load (that is `.context/rules/adr-standards.md`, sourced from the rule draft, per M-2).

**Category:** Process
**Likelihood:** High -- verified by direct grep; the gap exists in the current draft as written, and nothing in the Migration Plan schedules copying this command into the rule draft.
**Severity:** Major -- this is precisely the safeguard that could operate with zero infrastructure during the (potentially long, per PM-002) gap between Tier-1 guidance and Tier-2 enforcement. Its absence from the actually-distributed rule file means the collision-prevention story for that gap period is weaker than the parent ADR implies.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:414-425` (command present); `adr-standards-rule-draft.md` (Grep for "pre-flight|FM-018|Pre-flight" returns only line 285, a distinct concept).
**Dimension:** Actionability
**Mitigation:** Copy the FM-018 bash one-liner (or a pointer to it) into `adr-standards-rule-draft.md`'s "L5 CI Lint Specification" section, so it ships as part of the auto-loaded rule file, not only the parent ADR.
**Acceptance Criteria:** `adr-standards-rule-draft.md` contains the runnable pre-flight command (or an unambiguous cross-file pointer with the command inline) before M-2 executes.

---

### PM-004: Unmeasured Assumption That a MEDIUM-Tier SHOULD Convention Changes Behavior Without Enforcement [MAJOR]

**Failure Cause:** The document's Confidence section (`ADR-PROJ031-004-adr-identifier-convention.md:324-326`) carefully calibrates confidence (0.70-0.75) for the question "is Scheme B the right identity model," citing the trade study's declared ceiling. But a distinct, load-bearing assumption -- that authors and agents will actually *follow* a MEDIUM-tier, lint-free SHOULD convention in the gap before Tier-2 ships -- is never separately confidence-scored anywhere in either document, despite the package containing direct evidence bearing on it: `ps-architect.md`'s own present-tense non-compliance (see PM-002) is not merely a future risk to be fixed by M-12 -- it is *current evidence* about how a documented-but-unenforced convention performs in this exact repo, and it is negative evidence, not neutral. No base rate for "SHOULD-tier compliance without lint" is cited from Jerry's own history (e.g., existing MEDIUM standards like `AD-M-001` through `AD-M-011` in `agent-development-standards.md`, or `MCP-M-001`/`MCP-M-002` in `mcp-tool-standards.md`) despite those being directly analogous precedents available in the same repo.
**Category:** Assumption
**Likelihood:** High -- the negative evidence (ps-architect.md) already exists in-repo and is cited by this very package (as M-12/Fix-3) without being connected to the broader behavioral-compliance question.
**Severity:** Major -- if the base rate for "SHOULD convention, no lint" compliance is in fact low (which the one directly-available data point suggests), the entire Tier-1 "guidance delivers value immediately" framing is optimistic by construction, not merely by bad luck.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:324-326` (Confidence section scoped only to the identity-scheme choice); `skills/problem-solving/agents/ps-architect.md:218,260,267` (available negative evidence, not cross-referenced to a behavioral-compliance confidence estimate).
**Dimension:** Evidence Quality
**Mitigation:** Add an explicit, separately-labeled confidence statement (or at minimum an honest inference-flagged sentence, per the document's own P-022 practice) addressing "will Tier-1 guidance actually be followed absent Tier-2 enforcement," citing the ps-architect.md evidence as a negative data point rather than only as an isolated M-12 action item.
**Acceptance Criteria:** A new sentence or subsection under Confidence (or the Pre-Mortem/Failure-Modes section) states the behavioral-compliance confidence separately from the identity-scheme confidence, with the ps-architect.md evidence cited.

---

### PM-005: M-9 Self-Promotion Gating Is Ambiguous Under the Newer Two-Tier Model [MAJOR]

**Failure Cause:** Migration Plan row M-9 (`ADR-PROJ031-004-adr-identifier-convention.md:534`) states "Gating? Yes (on acceptance)" for this ADR's own Path-2 self-promotion (rename to `docs/design/ADR-adr-convention-001-*.md`). This wording predates the iteration-4 Tier split (M-9's row text itself is unchanged from the single-gate model), and it does not specify whether "acceptance" means Tier-1 (guidance, G-1 only) or Tier-2 (enforcement, G-2..G-4) acceptance. This matters concretely: if M-9 fires at Tier-1, the ADR performs its flagship "worked example of its own Path-2 promotion" (line 753) *before* the lint, waiver ledger, or producing-agent fix exist -- meaning the self-compliance demonstration teaches a rename-and-tombstone pattern while the very enforcement machinery it's meant to model-for-others is still vaporware, weakening the demonstration's pedagogical value. If M-9 is implicitly deferred to Tier-2, it inherits the same no-deadline risk as PM-002.
**Category:** Process
**Likelihood:** Medium -- this is an interpretive ambiguity in already-written text, not a certainty of harm; a careful reader might infer Tier-2 from context, but the row itself does not say so.
**Severity:** Major -- affects Internal Consistency between the (newer) Tier-split model and an (older) Migration-Plan row that was not fully re-threaded through it, and affects the credibility of the self-compliance "worked example" if timed prematurely.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:534` (M-9 row, "Yes (on acceptance)," no tier specified); `ADR-PROJ031-004-adr-identifier-convention.md:93-98` (Tier-1/Tier-2 gate definitions added iter-4, not cross-referenced from M-9's row).
**Dimension:** Internal Consistency
**Mitigation:** Amend the M-9 row to explicitly state "Tier-2 acceptance (all of G-2..G-4)" or "Tier-1 acceptance," whichever is intended, and add one sentence explaining why that timing best serves the "worked example" pedagogical goal.
**Acceptance Criteria:** M-9's row unambiguously names the triggering tier.

---

### PM-006: Downstream CoWork/Plugin Adopters Get Guidance With No Enforcement Backstop, Outside CODEOWNERS Reach [MAJOR]

**Failure Cause:** I verified `projects/PROJ-031-cowork-skeleton/design/phase3-skeleton-generation-design.md:159` confirms the strip-set is `projects/ tests/ skills/.graveyard .github` (+ recommended `docs/`) -- `.context/rules/` is *not* stripped, so the Tier-1 guidance genuinely ships to plugin installs (this specific claim in the ADR is accurate). However, the Enforcement Scope table (`ADR-PROJ031-004-adr-identifier-convention.md:653-657`) shows the *only* enforcement path for a downstream plugin adopter is `uv run jerry lint adr` -- a Tier-2, M-13 item (bundled with M-6, no deadline, same solo-maintainer bottleneck as PM-002). Worse than the source-repo case: a downstream fork is entirely outside `@geekatron`'s CODEOWNERS/governance reach, so even the weak "eventually the solo maintainer gets to it" hope that (partially) bounds the source-repo risk does not transfer to downstream repos at all -- they either build their own enforcement or have none, indefinitely. This is a distinct population from PM-002 (a different repo, not covered by the same eventual-fix path), so it is not redundant with it.
**Category:** External
**Likelihood:** Medium -- depends on how many downstream adopters actually author their own ADRs at all in the near term (unverifiable from this repo); the mechanism is certain, the population's exposure is not.
**Severity:** Major -- for the exact audience PROJ-031 exists to serve (per the package's own framing, `ADR-PROJ031-004-adr-identifier-convention.md:659` PM-002 degraded-mode disclosure), the "central enforcement mechanism" claim is silently weaker than for the source repo, with no independent path to closing that gap.
**Evidence:** `phase3-skeleton-generation-design.md:159,168` (strip-set verified, `.context/` retained); `ADR-PROJ031-004-adr-identifier-convention.md:642-661` (Enforcement Scope and Deployment Targets, M-13); `.github/CODEOWNERS` reality already disclosed at `ADR-PROJ031-004-adr-identifier-convention.md:676` (single-identity, source-repo-scoped, does not extend to forks).
**Dimension:** Actionability
**Mitigation:** State explicitly in the Enforcement Scope table that downstream-repo enforcement has no committed timeline and is entirely dependent on the downstream adopter's own initiative (already partially true in the PM-002 degraded-mode disclosure at line 659, but not connected there to the "no CODEOWNERS reach" point); optionally, prioritize shipping the CLI-only lint form (`uv run jerry lint adr`) as an early, cheap M-13 sub-slice independent of the full CI/waiver-ledger machinery, since a downstream single-repo lint run has none of the multi-reviewer/waiver complexity the source repo needs.
**Acceptance Criteria:** The Enforcement Scope table's downstream row explicitly discloses "no committed timeline; adopter-dependent" rather than only describing the intended mechanism.

---

### PM-007: WARN-Rule Alert Fatigue From Un-Retrofitted Framework ADRs [MINOR]

**Failure Cause:** Once M-6 ships, WARN rules L-5 (Framework home), L-6 (Provenance presence), and L-6c (Scope-declaration presence) will fire against the 3 existing `docs/design/` framework ADRs, because those files currently lack the proposed YAML frontmatter (`ADR-PROJ031-004-adr-identifier-convention.md:507`, M-11: "**None** carry the proposed YAML `origin_project`/`scope` schema"). M-11 (the retrofit) is a *separate* gating item from M-6, with its own independent completion timeline. There is a window in which M-6 is green (its FAIL-class 19-file regression test does not depend on M-11) while these 3 flagship ADRs generate expected, known WARNs on every CI run. Persistent "known-noise" WARNs are a documented alert-fatigue risk (analogous to `agent-routing-standards.md`'s own RT-M-009 concern about unreviewed routing signals): a genuinely new WARN (e.g., the package's own highest-RPN self-identified defect, L-14 producer-side drift) could be lost in that noise.
**Category:** Technical
**Likelihood:** Medium -- depends on the actual gap between M-6 and M-11 completion, which is unspecified.
**Severity:** Minor -- WARN-class only, does not block CI, and the underlying facts (frontmatter gap) are already disclosed by the package itself.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:507` (M-11, "None carry... schema"), `:531,:536` (M-6 and M-11 as separately-gated items), `:692-693,:701` (L-5/L-6/L-6c WARN specs).
**Dimension:** Traceability
**Mitigation:** Sequence M-11 to land in the same PR/commit window as M-6, or add a temporary, dated allowlist entry (mirroring the L-12 grandfather-allowlist pattern) suppressing L-5/L-6/L-6c specifically for the 3 named framework ADRs until M-11 completes.
**Acceptance Criteria:** M-6's initial CI run shows zero WARNs for the 3 framework ADRs (either because M-11 landed first, or because of a dated, visible suppression entry).

---

## Recommendations

**P0 (MUST mitigate before Tier-1 acceptance):**
- PM-001: Condense `adr-standards-rule-draft.md` to a lean rule file (target: under ~1,500 tokens installed) before M-2 executes; relocate detailed rationale/disclosure prose to a Level-3 reference document. Acceptance: measured token count of the installed `.context/rules/adr-standards.md`.
- PM-002: Add a time-boxed commitment (deadline + owner) for the Tier-2 G-3 producing-agent fix as a precondition of the Tier-1 status flip to `ACCEPTED`, so "ACCEPTED (guidance)" cannot be mistaken for "true of agent-produced ADRs." Acceptance: an explicit review-by date recorded at the Tier-1 flip, tracked as an H-32 worktracker Task.

**P1 (SHOULD mitigate):**
- PM-003: Copy the FM-018 pre-flight collision one-liner into the rule draft's L5 lint section.
- PM-004: Add a behavioral-compliance confidence statement distinct from the identity-scheme confidence, citing the ps-architect.md evidence.

**P2 (MAY mitigate; acknowledge risk):**
- PM-005: Disambiguate which tier gates M-9.
- PM-006: Disclose "no committed timeline" explicitly in the downstream Enforcement Scope row.
- PM-007: Sequence M-11 with M-6 or add a dated suppression entry for the 3 known-gap framework ADRs.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-001: the 14-row Migration Plan has no token-budget/condensation step for the file it schedules for permanent auto-load |
| Internal Consistency | 0.20 | Negative | PM-005: M-9's gating clause was not re-threaded through the iteration-4 Tier split |
| Methodological Rigor | 0.20 | Negative | PM-002: the Tier-split fix (a remediation for a prior finding) was not itself pre-mortem'd for side effects before this iteration |
| Evidence Quality | 0.15 | Negative | PM-004: available in-repo negative evidence (ps-architect.md) is cited for M-12 but not connected to a behavioral-compliance confidence estimate |
| Actionability | 0.15 | Negative | PM-002, PM-003, PM-006: the "guidance delivers value immediately" claim is weaker than stated for the agent-produced-majority and downstream-plugin populations |
| Traceability | 0.10 | Neutral | Cross-file citations between the ADR and rule draft remain internally consistent and resolvable (spot-checked); PM-007 is a downstream CI-noise risk, not a traceability defect in the document itself |

**Result:** 2 Critical and 4 Major failure causes identified via prospective hindsight, plus 1 Minor. Both Critical findings (PM-001 token bloat, PM-002 Tier-decoupling side effect) are cheap to remediate and neither invalidates the underlying identity-scheme decision (Scheme B) -- they are execution/rollout defects in the ratification and file-distribution mechanics layered on top of an otherwise well-argued decision. Overall assessment: **REVISE** — mitigate PM-001 and PM-002 before Tier-1 ratification proceeds; PM-003/PM-004 are cheap improvements that should accompany the same revision pass; PM-005/PM-006/PM-007 may be tracked and monitored per the package's own existing INHERENT-residual pattern.

---

## What the Package Already Prevents

Credit where due, per the task's instruction to check what the package already prevents: the existing FM-1..FM-4 table (`ADR-PROJ031-004-adr-identifier-convention.md:486-497`) already covers "lint never built" (FM-1), "same-slug collision across projects" (FM-2), "dialect overuse re-creating rename tax" (FM-3), and "taxonomy sprawl" (FM-4) with named detection/containment. The L-1a/L-1b grandfather split, the R-6 cross-branch race disclosure with a concrete 90-day/≥2-collision threshold, the solo-maintainer waiver fallback with `solo_maintainer: true` visibility, and the PM-009 forward-promotion-rate re-examination commitment are all genuine, well-specified monitored residuals that this review does not need to repeat. My findings above are additive to that existing work: PM-001/PM-003/PM-007 identify gaps in what actually gets *shipped* to the auto-loaded rule file (as opposed to what the parent ADR merely *describes*), and PM-002/PM-005/PM-004/PM-006 identify a specific, previously-unexamined class of risk -- that the iteration-4 Tier-split *remediation itself* introduces a regression the package's own pre-mortem table (written before the split existed) does not cover.

---

## Execution Statistics
- **Total Findings:** 7
- **Critical:** 2 (PM-001, PM-002)
- **Major:** 4 (PM-003, PM-004, PM-005, PM-006)
- **Minor:** 1 (PM-007)
- **Protocol Steps Completed:** 6 of 6

---

*Generated by: adv-executor (blind reviewer, S-004 Pre-Mortem, iteration 5)*
*Constitutional Compliance: P-003 (no subagents spawned), P-020 (no files edited outside this output path), P-022 (all claims cite file+line; the blind-boundary constraint on H-16 verification is disclosed, not concealed)*
