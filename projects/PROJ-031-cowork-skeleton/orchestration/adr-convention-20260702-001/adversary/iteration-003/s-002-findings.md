# Devil's Advocate Report: ADR-PROJ031-004 (ADR Identifier, Location, and Promotion Convention) + Companion Rule Draft

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.2) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (Draft 1.2)
**Criticality:** C4 (engagement quality gate 0.95, above SSOT 0.92)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind independent reviewer, iteration 3)
**H-16 Compliance:** **Not directly verifiable within blind-protocol constraints** — see disclosure below.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Blind Protocol Integrity Disclosure](#blind-protocol-integrity-disclosure) | Mandatory disclosure of an inadvertent scope breach during evidence-gathering (P-022) |
| [Role Assumption](#role-assumption-step-1) | Advocate role, scope, H-16 status |
| [Assumption Inventory](#assumption-inventory-step-2) | Explicit/implicit assumptions challenged |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All DA-NNN findings |
| [Finding Details](#finding-details-step-3) | Full Critical/Major finding writeups |
| [Response Requirements](#response-requirements-step-4) | P0/P1/P2 acceptance criteria |
| [Scoring Impact](#scoring-impact-step-5) | Dimension-level impact assessment |

---

## Blind Protocol Integrity Disclosure

**Mandatory honesty disclosure (P-022, no deception).** While gathering file+line evidence for citation-continuity claims, one `Grep` call was scoped to the whole `projects/PROJ-031-cowork-skeleton/` directory (searching for the strings `50+`/`scale`/`volume`/`corpus grow`) rather than being restricted to `explore/`, `research/`, and the two deliverables as the blind protocol requires. That call's results included matching lines from files I am explicitly prohibited from reading: `orchestration/adr-convention-20260702-001/adversary/iteration-001/s-002-findings.md`, `iteration-001/s-003-findings.md`, and `iteration-002/s-002-findings.md` + `iteration-002/s-014-quality-score.md`. I did not open these files directly — the exposure was via grep match-line snippets returned inline — but the snippets were substantive enough to reveal that a prior S-002 reviewer (iteration 2) raised a finding tagged `DA-004` challenging the "survives 50+ projects" claim, and that the current document (v1.2, the one under review) already contains a remediation for it (the "Collision-risk-at-scale estimate" paragraph, ADR lines 363-364, explicitly self-tagged `DA-004`).

**Mitigation applied:** I do not present the "50+ projects claim is asserted, not demonstrated" finding as a new discovery — the document itself shows it was already raised and partially remediated. Where my own independent reading (before this grep) had converged on a related but distinct concern, I have scoped my finding narrowly to the residual gap that the visible remediation text does **not** cover (promotion-event *volume* forecasting, as opposed to slug-*collision* probability, which the existing DA-004 remediation does address) — see DA-007. No other finding in this report depends on the exposed content. This disclosure is provided so the orchestrator can independently discount or re-weight this report if the exposure is judged to compromise independence.

---

## Role Assumption (Step 1)

- **Deliverable under challenge:** ADR-PROJ031-004 (canonical identity `ADR-adr-convention-001`, per its own Meta-Note) and its companion `.context/rules/adr-standards.md` review draft.
- **Criticality:** C4, engagement gate 0.95.
- **Scope of critique (per invoking task):** (1) the promotion-frequency assumption, (2) whether the promotion mechanic (identity handling) actually preserves citation continuity, (3) whether the scheme survives 50+ projects, (4) slug-governance failure modes.
- **H-16 status:** The invocation for this execution did not include a "Prior Strategy Outputs" field naming an S-003 Steelman output, and the blind protocol forbids me from reading sibling iteration-3 files (including any `s-003-findings.md`) to verify one exists. Per the orchestrator's documented 6-group sequential execution order (self-refine → steelman → challenge → verify → decompose → score), S-003 is expected to have already executed in this iteration's steelman group before this challenge-group (S-002) invocation. **This is disclosed as an assumption inherited from the orchestration design, not as directly-verified evidence** — I did not confirm it by reading an S-003 artifact, consistent with the blind-read prohibition. Given the explicit user instruction to execute this exact strategy now, I proceed rather than halt, and flag the unverified status here for the orchestrator's own H-16 audit trail.
- **Role assumed:** Argue against the convention's central load-bearing claims, with priority on the four targets above.

---

## Assumption Inventory (Step 2)

| # | Assumption (explicit/implicit) | Challenge |
|---|---|---|
| A-1 (explicit) | "Promotion of project decisions into the framework is a first-class, recurring operation" (Status, ADR:62), evidenced by "3/3 framework ADRs arrived by promotion." | Are these 3 independent trials, or 2 correlated project-level outcomes dressed as 3? See DA-004. |
| A-2 (explicit) | "Promotion becomes a plain file move with no rename and no broken citations" (L0, ADR:52) / "zero ID-string churn... zero breakage for the overwhelming bare-ID citation majority" (Consequences, ADR:373). | Is bare-ID citation actually the majority style in this repo's own governance files? See DA-001. Does the mechanism hold even for the ADR's own paired documents? See DA-002. |
| A-3 (implicit) | A WARN-class fuzzy-match lint (L-10) plus a named-but-soft arbiter role (M-5b) is sufficient taxonomy governance at 50+ projects. | Is the arbiter role real or aspirational, given the producing agent (ps-architect) is itself documented as non-compliant? See DA-005. |
| A-4 (implicit) | The Path-1 "pure file move" default will actually be the path exercised when promotions occur. | Has Path 1 ever been demonstrated, even in this document's own worked self-example? See DA-003. |
| A-5 (implicit) | "The identifier does not change" (Path 1, ADR:485) is sufficient to guarantee citation stability. | Does "identifier" include the optional title-slug tail that appears in real citations? See DA-006. |
| A-6 (explicit) | The qualitative order-of-magnitude estimate at L2 (ADR:364) resolves the "survives 50+ projects" question. | It addresses slug-collision probability only; it does not forecast promotion-event *volume*, which determines whether the soft governance process can keep pace. See DA-007. |

---

## Summary

Seven counter-arguments identified (2 Critical, 3 Major, 2 Minor), all mapped to the invoking task's four priority targets. The two Critical findings attack the decision's single decisive, headline-differentiating claim — that subject-encoded identity makes promotion a "zero-churn" file move — using evidence drawn from the live rule corpus this convention will itself be registered into (`mcp-tool-standards.md`, `agent-development-standards.md`) and from a self-referential citation break inside the two deliverables under review. Both show the "zero-churn" property protects only the bare-ID-in-prose citation style, not the full-path-in-a-References-table style that is this repo's dominant *governance-file* citation convention — including in the two documents proposing the scheme. The three Major findings attack the promotion-frequency evidence's independence (2 correlated projects presented as "3/3"), the total absence of any demonstrated or scheduled Path-1 (the supposedly-default path) instance, and the taxonomy-governance mechanism's dependence on a non-gating WARN lint plus an agent role that is itself currently non-compliant with the convention it is meant to police. Recommend **REVISE**: the core "zero-churn" marketing claim requires either hard qualification (scope it explicitly to bare-ID citations only) or a committed plan to retrofit/repair the demonstrated full-path exposure in the SSOT rule files before this convention is registered into them (M-7).

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260702iter3 | "Zero-churn" citation claim is falsified by the dominant citation style in Jerry's own SSOT rule files (full path, not bare ID) | Critical | `.context/rules/mcp-tool-standards.md:231`; `.context/rules/agent-development-standards.md:445,455`; ADR References table `ADR-PROJ031-004...md:646-658`; rule draft References table `adr-standards-rule-draft.md:284-291` | Evidence Quality |
| DA-002-20260702iter3 | The ADR and its companion rule draft cross-cite each other by relative path; both links are already guaranteed to break on this ADR's own scheduled ratification steps, with no Migration-Plan item to fix them | Critical | `ADR-PROJ031-004...md:552,584`; `adr-standards-rule-draft.md:189`; Migration Plan M-2/M-2b/M-7/M-9/M-10, `ADR-PROJ031-004...md:451-461` | Traceability |
| DA-003-20260702iter3 | The "default, zero-churn" Path 1 has zero demonstrated or scheduled instance anywhere; the ADR's own worked self-example exclusively exercises the discouraged Path 2 | Major | Meta-Note, `ADR-PROJ031-004...md:619-627`; Migration Plan M-9, `:460`; Promotion Process Path 1/2, `:482-500` | Evidence Quality |
| DA-004-20260702iter3 | Headline framing ("3/3 framework ADRs," L0/Status) presents 3 independent trials; the Bimodal Refinement section's own data shows these are 2 correlated project-level outcomes, a materially weaker evidentiary base than repeatedly stated | Major | `ADR-PROJ031-004...md:52,62` vs. `:250-253`; Confidence section `:270` | Internal Consistency |
| DA-005-20260702iter3 | Taxonomy-governance-at-scale (L-10 + M-5b arbiter) is non-gating, depends on a registry that does not exist on disk, and is assigned to an agent (ps-architect) the companion draft itself documents as non-compliant with this convention | Major | ADR Migration Plan M-5b gating column, `:456`; L-10, `:598`; rule draft L-10, `:209`; Fix 3, `adr-standards-rule-draft.md:252-264`; `docs/design/README.md` absent (Glob-verified 2026-07-02) | Methodological Rigor |
| DA-006-20260702iter3 | No rule states the filename's optional title-slug tail is frozen during Path-1 promotion, leaving citations that include the full filename (common in this repo) exposed even when the canonical `{domain-slug}-NNN` identity is preserved | Minor | `ADR-PROJ031-004...md:279,288,482-488`; example full-filename citation `mcp-tool-standards.md:231` | Completeness |
| DA-007-20260702iter3 | The "survives 50+ projects" remediation (L2, DA-004-prior) quantifies slug-*collision* risk qualitatively but never forecasts promotion-*event volume*, leaving the soft governance process's capacity to keep pace unassessed | Minor | `ADR-PROJ031-004...md:363-364` (collision-risk estimate) vs. Bimodal Refinement `:246-256` (rates, no forward volume projection) | Completeness |

**Finding ID Format:** `DA-{NNN}-20260702iter3`.

---

## Finding Details (Step 3)

### DA-001: "Zero-Churn" Citation Claim Falsified by Dominant Real-World Citation Style [CRITICAL]

**Claim Challenged:** "Promotion is a pure file move — zero ID-string churn for canonical (domain-slug) ADRs, and therefore zero breakage for the overwhelming bare-ID citation majority" (Consequences #1, `ADR-PROJ031-004-adr-identifier-convention.md:373`); Path 1 step 4: "Bare-ID citations require no re-pointing... This is the core win, and it covers the overwhelming majority of citations in the corpus" (`:487`).

**Counter-Argument:** The claim that bare-ID citation is "the overwhelming majority" is empirically false for the class of citation that matters most for governance traceability: References/Sources tables in the framework's own SSOT rule files. `.context/rules/mcp-tool-standards.md:231` cites `ADR-STORY015-001` by **full relative path**: `` `projects/PROJ-024-tactical-work/.../STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md` ``. `.context/rules/agent-development-standards.md:445` cites `ADR-agent-design-001` by full path: `` `docs/design/ADR-agent-design-001.md` ``, and `:455` cites `ADR-STORY015-001` again by its full deep path. This is not an isolated artifact like the single `ci.yml` example the ADR already discloses (`:84`, `:487` caveat) — it is the **standing house style** of References tables across at least two currently-loaded, auto-injected rule files, and (self-referentially) of the ADR's own References table (`:646-658`, e.g. `` `projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md` ``) and the rule draft's own References table (`adr-standards-rule-draft.md:284-291`, e.g. `` `docs/knowledge/exemplars/templates/adr.md` ``). Both documents proposing this scheme use full-path citation as their own default style. The one qualifying caveat the ADR does supply ("a small lint-surfaced residue," `:487`) materially understates prevalence — it is framed around a single external example (`ci.yml`) rather than the internal rule-corpus pattern that is directly discoverable by reading the very files this convention will be registered into (M-7, `.context/rules/adr-standards.md`; CLAUDE.md Navigation table).

**Evidence:** `.context/rules/mcp-tool-standards.md:231`; `.context/rules/agent-development-standards.md:445,455`; `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md:373,487,646-658`; `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:284-291`.

**Impact:** If valid, the decisive property distinguishing Scheme B from Scheme C/A ("promotion is free" vs. "promotion pays a citation tax") is overstated for exactly the citation style used in the framework's highest-value governance documents. Since L-8 (the only lint that would catch this) is Glob-verified absent (`ADR-PROJ031-004...:554`), every future Path-1 promotion risks silently breaking full-path citations in rule files with zero detection until L-8 ships — an unbounded window given M-6/M-13 have no committed date.

**Dimension:** Evidence Quality (the "overwhelming majority" claim is not supported, and is contradicted, by directly-available evidence).

**Response Required:** Either (a) narrow the claim explicitly to "bare-ID citations only, which are not the dominant style in this repo's own rule-file References tables," and add a corpus-wide count of full-path vs. bare-ID ADR citations (a `grep -rc` is trivial and deterministic, satisfying c-006), or (b) commit a gating action item to retrofit the cited rule files (`mcp-tool-standards.md`, `agent-development-standards.md`, this ADR's own References, the rule draft's own References) to bare-ID style before or immediately upon ratification, so the "overwhelming majority" claim becomes true going forward rather than remaining aspirational.

**Acceptance Criteria:** A stated, corpus-derived ratio of full-path-to-bare-ID ADR citations (not an assertion), and either a scoped claim or a scheduled remediation for the identified rule files.

---

### DA-002: Self-Referential Citation Break Inside the Deliverables Themselves, Unaddressed by the Migration Plan [CRITICAL]

**Claim Challenged:** Implicitly, that the Migration Plan (M-1 through M-14) comprehensively identifies the citation-repair work needed for this convention's own adoption (M-10 explicitly repairs one dangling citation, `ci.yml:2`).

**Counter-Argument:** The ADR and its companion rule draft cross-cite each other via relative markdown links, and both links are provably dead-on-ratification, yet no Migration-Plan row addresses them. `ADR-PROJ031-004-adr-identifier-convention.md:552` and `:584` both link to `` [L5 CI Lint Specification](../design/adr-standards-rule-draft.md#l5-ci-lint-specification) ``, a path relative to `projects/PROJ-031-cowork-skeleton/decisions/`. The rule draft reciprocally links back at `adr-standards-rule-draft.md:189`: `` [Enforcement Scope](../decisions/ADR-PROJ031-004-adr-identifier-convention.md#enforcement-scope-and-deployment-targets-p0-2--pm-001) ``. Per the ADR's own Migration Plan: M-2 moves the rule draft's content to `.context/rules/adr-standards.md` (`:451`); M-9 moves the ADR to `docs/design/ADR-adr-convention-001-*.md` (`:460`). After either move executes, both relative links resolve to nonexistent paths (`../design/adr-standards-rule-draft.md` no longer exists once M-2 is done and the file is superseded by the `.context/rules/` copy; `../decisions/ADR-PROJ031-004-...md` no longer exists at that path once M-9's tombstone-and-move executes). Scanning the Migration Plan (`:450-465`) for any item addressing these two specific links finds none — M-2/M-2b concern the new rule file's creation and symlinking, M-7 concerns CLAUDE.md registration, M-9 concerns the ADR's own rename/tombstone, and M-10 explicitly scopes only to `ci.yml`. This is the single most concrete, self-contained demonstration available — inside the very documents under review, requiring no external corpus evidence — that the promotion/ratification mechanic this ADR designs does not, by itself, guarantee citation continuity even for its own paired artifacts, after three adversarial iterations.

**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:552,584`; `adr-standards-rule-draft.md:189`; Migration Plan table `ADR-PROJ031-004-adr-identifier-convention.md:450-465` (absence of a matching row).

**Impact:** Undermines confidence that the Migration Plan is complete (a Completeness/Traceability concern) and directly contradicts the L-8 lint's stated purpose ("every referenced ID must resolve to a live ADR at its cited path," rule draft `:207`) — L-8, once built, should itself flag both of these links post-M-2/M-9, meaning the convention's own adoption sequence will trip its own lint on day one unless a fix is added now.

**Dimension:** Traceability.

**Response Required:** Add an explicit Migration-Plan action item (or fold into M-2/M-9) requiring both cross-links to be updated at the moment of the corresponding move, and verify no other relative link between the two deliverables exists uncaught.

**Acceptance Criteria:** A new or amended gating row naming both link updates, executed in the same commit as M-2 and M-9 respectively (not deferred as a follow-up), so the L-8 lint (once built) is not immediately red against the framework's own founding ADR.

---

## Response Requirements (Step 4)

**P0 (Critical — MUST resolve before acceptance):**
- **DA-001:** Provide a corpus-derived citation-style ratio (full-path vs. bare-ID) for existing ADR references, and either narrow the "overwhelming majority" claim accordingly or schedule remediation of the identified rule-file citations. Acceptance: a stated ratio plus a scoped claim or a gating Migration-Plan row.
- **DA-002:** Add an explicit action item fixing the two self-referential relative links before/at M-2 and M-9 execution. Acceptance: new/amended gating row, verified no other inter-deliverable relative link is missed.

**P1 (Major — SHOULD resolve; require justification if not):**
- **DA-003:** Either identify a concrete, scheduled future ADR that will exercise Path 1 (so the "default" path has at least one planned demonstration), or explicitly downgrade "the default, zero-churn path" framing to "the default path, not yet demonstrated in practice" until one occurs. Acceptance: a named future instance, or an honest Claim-Status caveat parallel to the existing lint Claim-Status disclosures.
- **DA-004:** Restate the promotion-frequency evidence base honestly as "2 correlated framework-mandate projects producing 3 promoted ADRs," and propagate this correction to every headline restatement (L0, Status, Rationale, Confidence) rather than only the Bimodal Refinement section. Acceptance: consistent n=2-projects framing everywhere the evidence is cited as support for the confidence range.
- **DA-005:** Either make M-5b a gating item with a defined cadence/owner-of-last-resort independent of ps-architect's current compliance state, or explicitly disclose that taxonomy governance is fully unenforced until both M-12 (agent fix) and a real `docs/design/README.md` registry exist. Acceptance: a gating commitment or an honest non-gating disclosure with a named interim owner.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- **DA-006:** Add one sentence to ADR-M-001/D-1 or Path 1 stating the title-slug tail SHOULD NOT be altered during promotion, or acknowledge the residual citation risk if it is. Acknowledgment sufficient.
- **DA-007:** Add a sentence distinguishing "slug-collision risk at scale" (already addressed) from "promotion-volume forecast at scale" (not addressed), acknowledging the latter is unestimated. Acknowledgment sufficient.

---

## Scoring Impact (Step 5)

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-006, DA-007: title-slug freeze and promotion-volume forecasting are unaddressed gaps in an otherwise extensively-scoped document |
| Internal Consistency | 0.20 | Negative | DA-004: headline "3/3 independent" framing (L0, Status, Rationale, Confidence) is inconsistent with the Bimodal Refinement section's own "2 correlated projects" data |
| Methodological Rigor | 0.20 | Negative | DA-005: the taxonomy-governance mechanism relies on a non-gating process and an agent role documented elsewhere in the same package as non-compliant, without reconciling that circularity |
| Evidence Quality | 0.15 | Negative | DA-001, DA-003: the "zero-churn"/"overwhelming majority" claim is contradicted by directly-available corpus evidence, and the "default path" has no demonstrated instance |
| Actionability | 0.15 | Negative | DA-005: no concrete cadence, owner-of-last-resort, or interim enforcement is specified for taxonomy governance before M-6/M-12 ship |
| Traceability | 0.10 | Negative | DA-002: the Migration Plan does not trace to (or repair) two citation breaks that exist inside the deliverables themselves |

**Overall assessment: Targeted revision required (P0 items block acceptance at the C4/0.95 engagement gate).** The convention's architecture and self-awareness of its own limitations (extensive existing Claim-Status disclosures, honest confidence-capping, disclosed residual risks) remain genuinely strong relative to typical C4 deliverables — this is not a fundamentally broken design. But its single most decisive, differentiating claim ("promotion is free") is measurably overstated against the citation style that actually dominates this repository's own governance corpus, and that overstatement is demonstrable using nothing but files already loaded into this framework's session context plus the deliverables' own cross-links. Addressing DA-001/DA-002 does not require new research — only an honest accounting of evidence already sitting in the repository.
