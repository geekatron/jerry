# Inversion Report: ADR-PROJ031-004 (ADR Identifier, Location, and Promotion Convention)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Protocol Deviation Disclosure](#protocol-deviation-disclosure-p-022) | Mandatory blind-protocol contamination disclosure |
| [Summary](#summary) | Overall assessment |
| [Goal Inventory](#goal-inventory-step-1) | Explicit + implicit goals |
| [Anti-Goal Inventory](#anti-goal-inventory-step-2) | What would guarantee failure |
| [Inverted-Goal Check](#inverted-goal-check-null-alternative) | Zero-governance null alternative comparison |
| [Assumption Map](#assumption-map-step-3) | Explicit + implicit assumptions |
| [Findings Table](#findings-table) | All IN-NNN findings |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Protocol completion |

---

## Header

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95, user-raised above SSOT 0.92)
**Date:** 2026-07-02
**Reviewer:** adv-executor (S-013, iteration 1, blind reviewer)
**H-16 Compliance:** S-003 Steelman is required to have run earlier in the C3+/C4 sequence per this template's Prerequisites; this executor did not read the S-003 output file (blind protocol) and instead verified goal/assumption content directly against the deliverable and independently-accessible evidence.
**Goals Analyzed:** 6 (5 explicit/decision-level + 1 implicit self-consistency goal) | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 5 (1 assumption confirmed robust/strength)

---

## Protocol Deviation Disclosure (P-022)

**Disclosure, made proactively and in full per P-022 (no deception).** During evidence-gathering (verifying whether "TBR-2" — the domain-slug taxonomy arbiter — was resolved anywhere in the accessible corpus), I ran a `Grep` for `TBR-2|TBR2` scoped to `projects/PROJ-031-cowork-skeleton` (the whole project directory) rather than to specific allowed subdirectories. The match output — visible to me in the tool result — included short excerpts (matched lines only, via ripgrep's line-context, not full file reads) from three **other reviewers' output files** under the `adversary/iteration-001/` directory that I was explicitly instructed not to read: `s-003-findings.md`, `s-004-findings.md`, and `s-001-findings.md`. This was a genuine violation of the blind-review protocol, caused by an insufficiently scoped search path, not intentional access.

**What I saw:** short matched lines referencing a "TBR-2" finding in those other reports, including finding identifiers (`SM-003-20260702T1200`, `PM-005-20260702-s004-i1`, `RT-004-20260702-i1`) and brief phrasing indicating those reviewers independently flagged the same TBR-2/arbiter gap.

**Containment action taken:**
1. I did not open, Read, or further Grep any of those three files.
2. The TBR-2 finding below (IN-003) is constructed **only** from evidence in files I am permitted to read: the deliverable itself (`ADR-PROJ031-004-adr-identifier-convention.md:320,340,355,370`) and `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/explore/trade-study.md:353` (explicitly an allowed evidence source per this task's instructions). I deliberately avoided reusing the other reviewers' exact finding IDs, wording, or framing to prevent any appearance of cross-contamination or manufactured independence.
3. I have not adjusted my severity classification, wording, or emphasis to match or diverge from what I glimpsed — the finding stands on its own evidentiary merits below.
4. I am flagging this to the orchestrator so it can decide whether this affects tournament validity (e.g., independence-of-reviewers assumptions for convergent-finding weighting).

**Corrective measure applied for the remainder of this execution:** all subsequent `Grep`/`Glob` calls were scoped to specific non-`adversary/` directories only.

---

## Summary

The package's central claim — that subject-encoded identity turns promotion into a zero-cost `git mv` — is well-argued, honestly sensitivity-tested against its own load-bearing assumption (promotion frequency), and factually accurate everywhere independently checked (BUG-006 F-002 self-correction verified correct; PROJ-007 stale-citation claim verified; `ADR-EPIC002-001`/`ADR-output-path-resolution-001` promotion split verified 3-of-5; `skills/architecture/SKILL.md` and `docs/knowledge/exemplars/templates/adr.md` defect citations verified byte-accurate). Inversion analysis nonetheless surfaces a **Critical** structural risk: the convention's entire distinguishing value (deterministic lint enforcement, not mere recommendation) rests on a to-do-list item (M-6) with no actual gate tying ratification to its completion, in a corpus with a documented, repeated track record of exactly this kind of recommended-fix-never-built (BUG-006's own `docs/design/README.md` index recommendation, still unbuilt; the `adr.md`/`SKILL.md` defects this ADR itself catalogs, apparently unfixed for an extended period). Three further **Major** findings show the convention's two soft dependencies — author self-classification (D-3) and taxonomy arbitration (TBR-2) — are unresolved, and that the trade study never benchmarked its ID-grammar options against a zero-governance, search-based null alternative as the invoking task explicitly requested. **Recommendation: REVISE** — close IN-001 (gate the lint to ratification, not just to a checklist row) and IN-002/IN-003 (name an arbiter; require domain-slug for anything framework-adjacent rather than leaving it to author judgment) before acceptance; IN-004 through IN-007 should be addressed but do not block ratification.

---

## Goal Inventory (Step 1)

| # | Goal | Type | Measurable form |
|---|------|------|------------------|
| G1 | Promotion (project → framework) becomes a pure file move, zero ID churn, zero citation breakage | Explicit | `git mv` only; zero `grep -rl` re-point operations required post-promotion for canonical (domain-slug) ADRs |
| G2 | ADR identity is discoverable/recognizable by subject, fixing BUG-006 F-001/F-003 | Explicit | `grep -r "ADR-{subject}"` clusters all decisions on a topic regardless of birth project |
| G3 | No central registry / shared counter; deterministically lint-able in a distributed, many-branch repo | Explicit (c-006) | Lint runs with no server process, no cross-branch coordination |
| G4 | No big-bang migration; legacy IDs grandfathered in place | Explicit (c-003, D-4) | Zero forced renames of the ~11 existing project-dialect ADRs |
| G5 | MEDIUM-tier, enforced by deterministic L5 CI lint rather than human memory | Explicit (D-5, c-001/c-002) | Lint exists, runs in CI, blocks/warns per rule class |
| G6 | Provenance (origin project/entity) preserved losslessly despite identity no longer encoding it | Explicit (c-005) | `origin_project`/`origin_entity` frontmatter present and populated |
| G7 (implicit) | The convention is actually adopted and enforced in practice — not merely documented, repeating the "zoo" problem it diagnoses | Implicit | New ADRs authored after ratification comply; lint catches non-compliance |
| G8 (implicit) | The governance artifact itself models the convention it establishes (self-consistency / dog-fooding) | Implicit | This ADR's own filename/identity complies, or its non-compliance is a bounded, explained exception |

---

## Anti-Goal Inventory (Step 2)

For each goal, "what would guarantee we FAIL to achieve it?"

| Goal | Anti-goal (guaranteed-failure condition) | Deliverable currently avoids it? |
|------|-------------------------------------------|-----------------------------------|
| G1 | Ship the recommendation but never build the lint; authors keep defaulting to the dialect for convenience, so Path-2 rename+tombstone becomes the norm, not the exception | **Not fully avoided** — see IN-001 (lint gating unenforced) and IN-002 (self-classification assumption) |
| G2 | Let domain slugs sprawl into synonyms with no arbiter, so `grep`-based clustering silently degrades | **Not avoided** — see IN-003 (TBR-2 unresolved) |
| G3 | Rely on a check that only catches exact-string duplicates, missing near-duplicate collisions | **Partially avoided** — L-3 catches exact dupes; does not catch synonymy (IN-003) or entity-dialect misfiling (IN-006) |
| G4 | Renumber legacy sets anyway under schedule pressure | **Avoided** — D-4/Migration Plan explicitly grandfathers; no evidence of contrary intent |
| G5 | Make every FAIL-class lint rule overridable via a one-line comment with no named approver | **Partially avoided** — MEDIUM-tier appropriately allows override-with-justification (by design, not a defect), but no approval workflow is specified, compounding IN-001 |
| G6 | Omit origin fields silently | **Avoided** — L-6 (WARN) checks provenance presence; frontmatter schema names the fields |
| G7 | Treat "MEDIUM + lint spec" as equivalent to "already enforced" | **Not avoided** — this is exactly IN-001; the corpus has a documented pattern (BUG-006's own recommended index, never built) of this anti-goal actually occurring |
| G8 | Author the founding ADR itself in the discouraged dialect, without disclosure | **Avoided on disclosure, not on practice** — the Meta-Note transparently discloses the dialect choice and remap path (P-020/P-022 compliant), but the practice itself (dialect used for a C4 framework-wide artifact) is the anti-goal instance — see IN-002 |

---

## Inverted-Goal Check (Null Alternative)

**Task-mandated inversion:** *"If we wanted maximum decision-findability with zero governance, what would we do — and does the package beat that null alternative?"*

**Null alternative constructed:** Do not touch ID grammar at all. Instead, build one deterministic, low-maintenance search surface — e.g., a generated or hand-curated `docs/DECISIONS-INDEX.md` (one line per decision: path, one-line title, tags) or a `grep`/`jerry`-based full-text search across all `decisions/` + `docs/design/` directories. This requires zero taxonomy to arbitrate, zero dialect-vs-canonical judgment call for authors, zero lint to build or maintain, and — critically — **zero rename risk for any ADR, ever**, because no ID grammar changes at all.

**Verification that this alternative was not evaluated:** targeted search of `trade-study.md` for "search index," "null alternative," "zero governance," "Option G," and "no naming convention" returned no matches. The trade study's Open Questions section (TBR-1 through TBR-5) and its six evaluated schemes (A–F) are exclusively ID-grammar variants; none is "invest in a search/index tool instead of an ID convention."

**Does the package beat the null alternative?** Plausibly yes on provenance-preservation and promotion-cost grounds (a flat index does not, by itself, preserve `origin_project`/`origin_entity` structurally, and doesn't make promotion free — a moved file still needs its index entry updated, though that is a much smaller edit than a rename). But the deliverable **never makes this argument explicitly** — it argues Scheme B beats Schemes A/C/D/E/F, not that a governed ID scheme beats no ID scheme plus tooling. This is a genuine unclosed comparison for a C4 decision, and it is materially relevant because the document's own recommended fix for the *discoverability* goal (G2) — a `docs/design/README.md` index — **is itself a version of the null alternative**, yet it is filed as an optional, non-gating action item (M-5, "No") rather than benchmarked as the alternative the whole ID-grammar apparatus must outperform. See IN-004.

---

## Assumption Map (Step 3)

| # | Assumption | Category | Explicit/Implicit | Confidence | Validation status |
|---|------------|----------|--------------------|------------|--------------------|
| AS-1 | Future authors can reliably self-classify "project-local-forever" vs. "framework-relevant" at authoring time (D-3) | Process | Implicit | Low | Logically inferred from n=5 promotion sample; contradicted by this ADR's own instance (see IN-002) |
| AS-2 | Repo-wide `sort \| uniq -d` on exact `{slug}-NNN` strings is sufficient collision protection in a distributed, many-branch repo | Technical | Explicit (c-006) | Medium | Correct for exact-string collisions; does not address synonymy (IN-003) |
| AS-3 | The L5 CI lint (M-6) will actually be built and wired into CI as a true gate, not merely documented as one | Process/Governance | Implicit | Low-Medium | Contradicted by base-rate evidence: two known template/skill defects and one prior BUG-006-recommended mitigation (docs/design/README.md) remain unbuilt (IN-001) |
| AS-4 | A "lightweight arbiter" for domain-slug taxonomy will emerge without being named as a role/process/cadence (TBR-2) | Governance/Resource | Implicit | Low | Unresolved in both the trade study (`trade-study.md:353`, listed as an open question) and the ADR itself (cited 4x, never assigned an owner) |
| AS-5 | Existing framework tooling (schema validation, AST parsing) will interoperate with the new ADR frontmatter contract | Technical/Tooling | Implicit | Medium | No `docs/schemas/*.json` schema exists for an "adr"/"decision" entity (verified); enforcement is designed as a standalone script, not integrated with the established `jerry ast validate --schema` pattern |
| AS-6 | The forward ADR-promotion rate will remain high enough (or the bimodal framework-mandate subset will remain distinguishable) to justify B over C | Temporal/Environmental | Explicit (already stress-tested by the deliverable) | Medium-High (0.78, author-stated) | **STRENGTH — already inverted and sensitivity-analyzed by the deliverable itself** (Promotion-Frequency Sensitivity section); the document names its own failure conjunction explicitly. No further finding needed; this is the assumption S-013 would normally surface, and the creator already did the work. |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260702-s013-i1 | AS-3: L5 lint will actually be built and gated before/at ratification | Assumption | Low-Medium | **Critical** | `ADR-PROJ031-004...md:357,367,391-402` (M-6 "Yes (gating)" but no CI/status-transition mechanism ties to it); `skills/architecture/SKILL.md:105,284` and `docs/knowledge/exemplars/templates/adr.md:1,182` (two pre-existing, apparently-unfixed defects this ADR itself catalogs); `trade-study.md:353` + absent `docs/design/README.md` (Glob-verified) — BUG-006's own recommended fix, never built | Methodological Rigor |
| IN-002-20260702-s013-i1 | AS-1: Authors can reliably self-classify promotion likelihood at birth (D-3) | Assumption | Low | Major | `ADR-PROJ031-004...md:182,495-503` (this ADR — C4, framework-wide — is itself authored in the discouraged `ADR-PROJ031-004` dialect, requiring a Path-2 rename on its own promotion) | Internal Consistency |
| IN-003-20260702-s013-i1 | AS-4: Domain-slug taxonomy arbiter (TBR-2) will keep slugs coherent | Assumption | Low | Major | `ADR-PROJ031-004...md:320,340,355,370` (arbiter cited 4x, never named); `trade-study.md:353` (open question, unresolved); `docs/design/README.md` absent (Glob-verified) | Completeness |
| IN-004-20260702-s013-i1 | Inverted-goal check: zero-governance null alternative never benchmarked | Anti-Goal | N/A | Major | `trade-study.md` (targeted search for search/index/null-alternative terms: no matches); `adr-standards-rule-draft.md:399` M-5 marked non-gating "No" | Methodological Rigor |
| IN-005-20260702-s013-i1 | AS-5: Enforcement will integrate with existing schema/AST tooling pattern | Assumption | Medium | Minor | `docs/schemas/*.json` (Glob: 8 schemas, none for adr/decision); `adr-standards-rule-draft.md:171-186` (bespoke `scripts/lint_adr_convention.py`) | Completeness |
| IN-006-20260702-s013-i1 | Anti-Goal: entity-embedded dialect (`ADR-{ENTITY-ID}-NNN`) placement is unchecked by L-4 | Anti-Goal | N/A | Minor | `adr-standards-rule-draft.md:180` (L-4 checks `PROJ{NNN}` only); `projects/PROJ-024-tactical-work/work/EPIC-001-schema-validation/FEAT-001-claude-code-schema-validation/STORY-015-tier-model-renumbering/ADR-STORY015-001-tier-model-renumbering.md` (Glob-verified location the lint spec never addresses) | Internal Consistency |
| IN-007-20260702-s013-i1 | Anti-Goal: deprecated separate-amendment-file style (ADR-M-009) has no corresponding lint rule | Anti-Goal | N/A | Minor | `adr-standards-rule-draft.md:53,145-153` (SHOULD NOT, no L-1..L-7 rule detects it) | Completeness |

**Finding ID Format:** `IN-{NNN}-20260702-s013-i1` (execution id: 2026-07-02, strategy S-013, iteration 1).

---

## Finding Details

### IN-001: L5 CI Lint Is a Migration-Plan Checklist Item, Not an Enforced Gate [CRITICAL]

**Type:** Assumption (AS-3)
**Original Assumption:** "This convention is RECOMMENDED... enforced by a deterministic L5 CI lint (spec below) plus L4 advisory" (D-5) and "M-6 | Implement + wire the L5 CI lint... | devsecops | **Yes** (gating)" (Migration Plan, `ADR-PROJ031-004...md:400`).
**Inversion:** What if the lint is never actually built or wired into CI, and the convention remains purely advisory text?
**Plausibility:** High. The deliverable's own evidence base shows this exact pattern occurring twice already in this corpus: (1) BUG-006 (an accepted, acted-upon Nielsen evaluation) recommended a `docs/design/README.md` domain index as its F-004 remediation — verified absent from disk via Glob, and the ADR's own text acknowledges it was "never implemented" (`ADR-PROJ031-004...md:307,320`); (2) the `docs/knowledge/exemplars/templates/adr.md` (`ADR-{NUMBER}` placeholder, dangling `docs/decisions/` path) and `skills/architecture/SKILL.md` (`ADR_NNN` underscore mismatch) defects this very ADR catalogs as long-standing, unfixed corpus problems (verified byte-accurate at the cited lines) have themselves sat unfixed through however many ADRs were authored referencing them.
**Consequence:** If ratified without the lint built and gating, the convention becomes exactly a fourth "family" alongside the seven the ADR already catalogs — documented, unenforced, and diverging from practice. Given the recognized incentive to default to the dialect (IN-002) absent enforcement, the two-grammar system (canonical + dialect) could compound the zoo problem rather than resolve it: readers would now need to know *both* that a convention exists *and* that it is not machine-checked, a strictly worse epistemic position than a single, if imperfect, converged-upon practice.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:357` (FM-1, "The L5 lint was never implemented; the convention stayed a suggestion"), `:367` (R-5, "MED... HIGH... Adoption action item makes the lint a gating deliverable, not optional"), `:391-402` (Migration Plan M-1 through M-8, none of which is a status-transition/CI mechanism — they are prose rows in a markdown table with no automated enforcement); `skills/architecture/SKILL.md:105,284` (verified: `docs/design/ADR_NNN_*.md`, `docs/design/ADR_001_sqlite_persistence.md`); `docs/knowledge/exemplars/templates/adr.md:1` (verified: `# ADR-{NUMBER}: {Title}`); no `docs/design/README.md` on disk (Glob, this session).
**Dimension:** Methodological Rigor
**Mitigation:** Do not mark this ADR `ACCEPTED` (or treat the companion rule draft as in force) until M-6 (lint built + wired into CI) is independently verified complete — i.e., make ratification conditional on the lint's existence, not merely list it as a gating row in a plan. Add a concrete verification step (e.g., a CI run log or PR link) as part of the ratification record.
**Acceptance Criteria:** `scripts/lint_adr_convention.py` (or equivalent) exists, is wired into a `.github/workflows/` job, and that job's first real run (against the current corpus) is attached to the ratification record before status flips from `PROPOSED`.

### IN-002: The Convention's Own Founding Document Is the Counter-Example to Its Load-Bearing Self-Classification Assumption [MAJOR]

**Type:** Assumption (AS-1)
**Original Assumption:** "the author usually knows the intent at birth" (D-3 supporting rationale) — future ADR authors will correctly judge whether a decision is "purely tactical, project-local" (dialect permitted) or framework-relevant (domain-slug recommended).
**Inversion:** What if authors — even highly-informed ones — cannot reliably make this call at authoring time?
**Plausibility:** High, and not merely hypothetical: this ADR is itself the test case. It is explicitly C4, framework-wide governance ("Criticality: C4 (framework-wide governance...)", line 8), authored by an agent with full visibility into the entire ADR corpus and its promotion history — arguably the best-informed possible author for this specific self-classification judgment — and yet it was written at the discouraged dialect path (`ADR-PROJ031-004`), per its own Meta-Note, "because the invoking task mandated this exact path" (line 499). The Meta-Note further states this ADR will require Path 2 (the discouraged rename + tombstone) on its own promotion (line 501) — the exact tax the decision exists to eliminate.
**Consequence:** If the most favorable possible case for correct self-classification still produces a dialect instance requiring the discouraged promotion path, ordinary future authors — writing routine ADRs without full corpus visibility and without an explicit task mandate forcing a specific path — are less likely to self-classify correctly, not more. This directly undermines G1 (promotion-as-file-move), the decision's headline value proposition, precisely at the margin (framework-relevant decisions authored under dialect identity) where it matters most.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:8` (Criticality: C4 framework-wide), `:182` (D-3 self-classification rationale), `:495-503` (Meta-Note: dialect filename, canonical remap identity `ADR-adr-convention-001`, Path-2 promotion required).
**Dimension:** Internal Consistency
**Mitigation:** Either (a) require domain-slug identity by default for any ADR whose Criticality is C3/C4 (removing author judgment from the highest-stakes case, where misjudgment is costliest), reserving the dialect exclusively for C1/C2 tactical ADRs where the promotion-tax consequence is genuinely low; or (b) explicitly self-correct this ADR's own filename/identity to the canonical form at ratification time rather than deferring to a described-but-not-executed "intended end-state" (line 503).
**Acceptance Criteria:** Either a Criticality-based override rule is added to ADR-M-003 (dialect NOT PERMITTED at C3/C4), or this ADR is promoted/renamed to its stated canonical identity as part of ratification rather than left as a documented future intention.

### IN-003: Domain-Slug Taxonomy Arbiter (TBR-2) Is Unresolved; Exact-Match Lint Cannot Substitute [MAJOR]

**Type:** Assumption (AS-4)
**Original Assumption:** "This needs a lightweight index (`docs/design/README.md`) and an arbiter (TBR-2)... Named here so it is owned, not discovered" (`ADR-PROJ031-004...md:320`).
**Inversion:** What if no one arbitrates domain-slug taxonomy, and near-duplicate slugs (`agent-design` vs. `agent-definition` vs. `agents`) proliferate?
**Plausibility:** High. The item is *named* but not *resolved*: `trade-study.md:353` lists it as an open question ("Under B, who arbitrates domain-slug taxonomy... A lightweight `docs/design/README.md` domain index... would serve") — a proposed mechanism, not an assigned owner. The ADR repeats the same unresolved reference three more times (`:340,355,370`) without ever naming a role, agent, or cadence. The proposed fix artifact (`docs/design/README.md`) does not exist on disk (Glob-verified this session) — and per the ADR's own citation, this is the identical fix BUG-006 recommended (F-004) and which "was never implemented" historically.
**Consequence:** L-3 (slug-uniqueness) only performs `sort | uniq -d` on exact `{slug}-NNN` strings — it structurally cannot detect near-duplicate or synonymous slugs. Two authors independently choosing `agent-design` and `agent-definition` for related decisions would both pass L-3 cleanly while defeating exactly the `grep`-clustering discoverability benefit (G2) that is Scheme B's primary claimed advantage over Schemes A/C.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:320` ("an arbiter (TBR-2)... Named here so it is owned, not discovered" — self-contradicted by remaining unresolved), `:340` (R-3), `:355` (FM-4), `:370` (Inversion self-check, S-013, already present in the deliverable but does not resolve TBR-2); `trade-study.md:353` (open question); `docs/design/README.md` absent (Glob, this session).
**Dimension:** Completeness
**Mitigation:** Resolve TBR-2 explicitly before or at ratification: name either a specific role/agent (e.g., "the ps-architect agent reviews new domain slugs against `docs/design/README.md` at each promotion, or on request during ADR authoring") or an automated fuzzy-match check (e.g., a Levenshtein-distance or token-overlap WARN rule added to the L5 lint) as the taxonomy arbiter, and make `docs/design/README.md` creation a concrete, owned Migration Plan item (elevate M-5 from "No" gating to at least a tracked, owned deliverable) rather than an optional aside.
**Acceptance Criteria:** TBR-2 has a named resolution (role, process, or automated check) documented in the ratified ADR or its companion rule file, and `docs/design/README.md` exists with at minimum the 3 current framework-ADR domain slugs indexed before new domain-slug ADRs are authored under this convention.

---

## Recommendations

**Critical (MUST mitigate before acceptance):**
- **IN-001-20260702-s013-i1:** Gate ratification (`PROPOSED` → `ACCEPTED`) on independently-verified completion of the L5 CI lint (M-6), not on a plan-table checklist row alone.

**Major (SHOULD mitigate before acceptance):**
- **IN-002-20260702-s013-i1:** Restrict the project-scoped dialect (D-3) from C3/C4-criticality ADRs, or self-correct this ADR's own identity/filename at ratification rather than deferring it as a described intention.
- **IN-003-20260702-s013-i1:** Name a concrete owner/process (or automated fuzzy-match check) for domain-slug taxonomy arbitration (TBR-2), and elevate `docs/design/README.md` creation (M-5) from optional to a tracked, owned action item.
- **IN-004-20260702-s013-i1:** Add an explicit comparison of the chosen scheme against a zero-governance, index/search-based null alternative to the trade study or the ADR's Rationale section, even if the conclusion (B still wins) is unchanged — the argument as written never closes this comparison.

**Minor (MAY mitigate):**
- **IN-005-20260702-s013-i1:** Note in the rule draft whether/how the ADR frontmatter contract will (or will not) get a `docs/schemas/*.json` entry consistent with other governed entity types, or explicitly justify the standalone-script approach.
- **IN-006-20260702-s013-i1:** Extend L-4 (or add L-8) to validate entity-embedded dialect placement (`ADR-{ENTITY-ID}-NNN` matches its containing entity folder), matching the coverage already given to the project dialect.
- **IN-007-20260702-s013-i1:** Add an L5 lint rule (WARN) flagging newly-created separate-amendment-style files (`ADR-*-amendment-*`) to make ADR-M-009 machine-checked, not merely stated.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-003 (taxonomy arbiter unresolved), IN-005 (no schema for frontmatter contract), IN-007 (amendment-style deprecation unenforced) — the convention's completeness gaps concentrate in "who/what actually enforces this," not in the ID grammar itself, which is thoroughly specified |
| Internal Consistency | 0.20 | Negative | IN-002 (the ADR's own filename contradicts the self-classification assumption it relies on); IN-006 (L-4 lint coverage inconsistent between the two permitted dialect forms) |
| Methodological Rigor | 0.20 | Negative | IN-001 (enforcement gating is asserted, not verified/mechanized); IN-004 (trade study never benchmarks against the zero-governance null alternative the task explicitly asked about) |
| Evidence Quality | 0.15 | Positive | All independently-checkable factual claims verified accurate on this pass (BUG-006 F-002 self-correction, PROJ-007 stale citations, 3-of-5 promotion split, SKILL.md/adr.md defect citations byte-exact) — a genuine strength worth preserving in revision |
| Actionability | 0.15 | Neutral-to-Negative | Findings above (IN-001/002/003) have concrete, verifiable acceptance criteria; but the deliverable's own existing action items (M-5, M-6) already had "gating"/"owned" labels that this Inversion shows are not self-enforcing, so actionability of the *original* document is weaker than its checklist format implies |
| Traceability | 0.10 | Positive | Every claim in the deliverable that was spot-checked traced correctly to a real file/line; the one already-self-identified gap (TBR-2) is at least named, even though unresolved |

---

## Execution Statistics

- **Total Findings:** 7 (IN-001 through IN-007)
- **Critical:** 1
- **Major:** 3
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6 (Goals stated; Anti-goals inverted; Assumptions mapped [6]; Assumptions stress-tested [6, including 1 confirmed strength]; Mitigations developed for Critical/Major; Synthesis + scoring impact produced)
- **Protocol Deviations:** 1 (blind-protocol contamination via over-broad Grep path — disclosed above; contained; no other-reviewer content reused in analysis or wording)
