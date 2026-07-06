# Quality Score Report: ADR Identifier, Location, and Promotion Convention (ADR-PROJ031-004 + Companion Rule Draft) — Iteration 3

## Navigation

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, weakest dimension, one-line assessment |
| [Scoring Context](#scoring-context) | Deliverables, strategy, SSOT reference |
| [Score Summary](#score-summary) | Weighted composite, both gate comparisons |
| [Dimension Scores](#dimension-scores) | Six-dimension table with weighted contributions |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement path per dimension |
| [Findings Inventory Across All Iteration-3 Strategies](#findings-inventory-across-all-iteration-3-strategies) | Consolidated cross-strategy tally |
| [Priority-Ordered Remediation Table](#priority-ordered-remediation-table) | Owner-tagged, [FIXABLE-NOW] vs [INHERENT] |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency self-audit |
| [Session Context Handoff](#session-context-handoff) | Schema for orchestrator consumption |

---

## L0 Executive Summary

**Score:** 0.62/1.00 | **Verdict (0.95 engagement gate):** REJECTED | **Verdict (0.92 SSOT gate):** REJECTED | **Weakest Dimension:** Internal Consistency (0.55)

**One-line assessment:** This is an exceptionally well-engineered C4 governance package (95.7% independently-verified citation accuracy, full H-16 steelman discipline, unusually honest Claim-Status disclosures) that nonetheless carries 5 independently-discovered, evidence-backed Critical findings and roughly a dozen Major findings — most concentrated in same-document self-contradictions and an unenforced "gating" ratification mechanism — none of which have yet been remediated in this iteration; the core naming decision (Scheme B, subject-encoded ADR identity) is not in question, but the package as currently written does not meet either the 0.95 engagement gate or the standard 0.92 SSOT gate, and requires a fourth remediation pass before ratification.

---

## Scoring Context

- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (693 lines)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (300 lines)
- **Deliverable Type:** ADR + companion MEDIUM-tier rule draft (governance convention)
- **Criticality Level:** C4 (self-classified; AE-002/AE-003 independently set a C3 floor per the ADR's own CC-004 correction, C4 from the tier definition itself)
- **Scoring Strategy:** S-014 (LLM-as-Judge), Group F, iteration 3
- **Engagement Quality Gate:** 0.95 (user-raised above the SSOT default)
- **SSOT Reference:** `.context/rules/quality-enforcement.md` (Quality Gate section: dimension weights, 0.92 threshold, Operational Score Bands)
- **Strategy Findings Incorporated:** Yes — 9 iteration-3 adversarial reports read in full:
  `s-010-self-refine-findings.md`, `s-003-findings.md` (Steelman), `s-001-findings.md` (Red Team), `s-002-findings.md` (Devil's Advocate), `s-004-findings.md` (Pre-Mortem), `s-011-findings.md` (Chain-of-Verification), `s-007-findings.md` (Constitutional AI Critique), `s-012-findings.md` (FMEA), `s-013-findings.md` (Inversion) — all in `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-003/`. Also read `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/explore/trade-study.md` for cross-referenced weighted-sum figures.
- **Scored:** 2026-07-02

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | **0.62** |
| **User-Raised Engagement Gate** | 0.95 |
| **SSOT Default Threshold (H-13)** | 0.92 |
| **Verdict at Engagement Gate (0.95)** | **REJECTED** (0.33 below gate) |
| **Verdict at Standard SSOT Bands** | **REJECTED** (< 0.85; well below the 0.85–0.91 REVISE operational band) |
| **Unresolved Critical Findings (this scorer's own severity re-assessment)** | 5 (IN-001, RT-002, CC-002, FM-102, DA-002) — see [Findings Inventory](#findings-inventory-across-all-iteration-3-strategies) for the full 11-item raw-severity tally from the 8 blind strategies |
| **Strategy Findings Incorporated** | Yes — 9 reports, 46 independently-verified factual claims (S-011: 44/46 = 95.7% accurate) |

**Special-case application (per S-014 rubric):** Any Critical finding from adv-executor reports triggers automatic REVISE-or-worse regardless of composite. This package carries multiple unresolved Critical findings from independent blind strategies; combined with a composite already well under 0.85, the verdict is **REJECTED**, not merely REVISE — this is "significant rework required," not "near-threshold, targeted revision."

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-------------------|
| Completeness | 0.20 | 0.62 | 0.124 | Options/sensitivity/migration/lint fully specified; but RT-002 (Critical) and FM-102 (Critical) show the enforcement/topology coverage has real, population-scale gaps |
| Internal Consistency | 0.20 | 0.55 | 0.110 | 5-6 independently-discovered, non-overlapping same-document self-contradictions survive (CC-002, CV-002, DA-004, IN-002, IN-003) — the weakest dimension |
| Methodological Rigor | 0.20 | 0.62 | 0.124 | Steelman/trade-study methodology genuinely rigorous; enforcement machinery unevenly engineered (RT-001, IN-001, PM-101/102/103); self-correction apparatus itself failed twice (CV-001, CV-002) |
| Evidence Quality | 0.15 | 0.68 | 0.102 | 95.7% independent verification rate (S-011) is a real strength, but two headline claims (DA-001 "zero-churn"/"overwhelming majority"; FM-104 "lossless" provenance) are directly contradicted by available evidence |
| Actionability | 0.15 | 0.62 | 0.093 | Migration Plan M-1..M-14 is unusually well-owned/gated, but IN-001 (Critical) shows the single highest-leverage action — the ratification status flip — has zero technical enforcement |
| Traceability | 0.10 | 0.65 | 0.065 | Nav tables H-23/H-24 compliant; near-universal file+line citation discipline; but DA-002 (Critical) shows the two deliverables' own cross-links will break on their own scheduled promotion moves, unaddressed in the Migration Plan |
| **TOTAL** | **1.00** | | **0.618 ≈ 0.62** | |

---

## Detailed Dimension Analysis

### Completeness (0.62/1.00)

**Evidence:**
The package is comprehensive on its core decision surface: all six naming schemes (A–F) are steelmanned and scored against the trade study (`explore/trade-study.md:217-231`, independently re-verified exact by S-011 CL-008/CL-009), a full sensitivity analysis on the load-bearing promotion-frequency assumption is present, and the companion rule draft covers ID scheme, location model, frontmatter schema, promotion process, supersede/amend rules, status vocabulary, a 10-rule lint specification, and new-project onboarding.

**Gaps:**
- **RT-002 (Critical, S-001):** The only taxonomy-synonymy defense (L-10) is scoped exclusively to the `docs/design/README.md` framework registry (`adr-standards-rule-draft.md:209`; `ADR-PROJ031-004-adr-identifier-convention.md:598`), leaving the **numerically dominant, RECOMMENDED-default** project-scoped canonical population (16 of ~19 live ADRs) with zero near-duplicate-slug protection.
- **FM-102 (Critical, S-012):** The convention has zero provision for Jerry's documented **repository-based** worktracker topology (`skills/worktracker/rules/worktracker-directory-structure.md:19-44`, a `ONE-OF` alternative to project-based), despite PROJ-031's own stated audience including downstream plugin adopters who may run exactly that topology.
- **PM-103 (Major, S-004):** M-6 (GitHub Action) and M-13 (`uv run jerry lint adr` CLI subcommand) name two unreconciled delivery targets for "the lint" with no single implementation spec (`pyproject.toml:65,72-73` shows `scripts/` is not automatically wired into the `jerry` CLI package).
- **IN-002 (Major, S-013):** The Canonical Location Model's "Entity-embedded (permitted): `ADR-{ENTITY-ID}-NNN`" claim (unqualified) contradicts the actually-codified closed 4-prefix set `{PROJ|EPIC|FEAT|STORY}`, silently excluding live worktracker entity types (`BUG-`, `TASK-`, `DISC-`, `IMP-`).
- **DA-006/DA-007 (Minor, S-002):** Title-slug-tail freeze during promotion and promotion-*volume* forecasting (vs. slug-collision probability, already addressed) are unaddressed.

**Improvement Path:** Extend L-10 to a repo-wide fuzzy-match (not framework-registry-scoped); add a repository-based Canonical Location Model row and branch the lint/onboarding guidance on topology; unify M-6/M-13 into a single implementation-location spec; reconcile the Entity-embedded claim to the closed 4-prefix set (or widen the set to match).

### Internal Consistency (0.55/1.00 — weakest dimension)

**Evidence:**
Tier-vocabulary hygiene in the MEDIUM rule draft is genuinely clean (`grep` for `MUST|SHALL|REQUIRED|FORBIDDEN|NEVER` returns zero hits per S-010's own self-audit, confirmed independently by S-007's Compliance Positives). The DEC-NNN bare-vs-composite reconciliation and the CV-001 "resistant not immune" correction (self-refine, this iteration) are handled with real transparency.

**Gaps (multiple, independently discovered, non-overlapping — a systemic pattern, not isolated noise):**
- **CC-002 (Critical, S-007):** L-9 ("No new file under frozen dirs") retains the exact phrasing `FAIL (non-waivable-in-practice...)` (`adr-standards-rule-draft.md:208`; `ADR-PROJ031-004-adr-identifier-convention.md:597`) that the document *itself*, three table rows earlier, diagnoses as "de-facto HARD... a genuine contradiction" when fixing the identical pattern for L-2/L-3 (CC-001 tier reconciliation, `ADR:584`). The fix was never propagated to L-9.
- **CV-002 (Major, S-011):** The Context section's claim that the `ADR-EPIC002-001` collision was "resolved by renaming to `ADR-EPIC002-002`" directly contradicts the document's own [Related Decisions] and [Promotion-Frequency Sensitivity] sections, which correctly describe the actual resolution (domain-slug rename to `ADR-output-path-resolution-001`, commit `41539073`) — and `ADR-EPIC002-002` is now the ID of an unrelated, legitimately-issued ADR, making the erroneous claim a live mis-citation risk of exactly the class this convention exists to prevent.
- **DA-004 (Major, S-002):** Headline framing ("3/3 framework ADRs," L0 and Status sections) presents 3 independent trials; the document's own Bimodal Refinement section shows these are 2 correlated project-level outcomes — a materially weaker evidentiary base than the headline repeatedly states.
- **IN-002 / IN-003 (Major, S-013):** (i) Entity-embedded Location Model claim vs. closed dialect grammar (see Completeness); (ii) the null-alternative rebuttal's claim that B's index is "free and always current" (`ADR:234`) directly contradicts the document's own later characterization of the same index as "the new long-term liability... a soft process that can rot" requiring a gating arbiter (`ADR:363-364,455-456`).
- **RT-003 (Major, S-001):** The case-folded dialect-lookalike ban enumerates only `{proj|epic|feat|story}`, omitting real worktracker prefixes (`bug`, `task`, `spike`, `enabler`), inconsistent with the closed-set rationale used elsewhere.
- **FM-101 (recharacterized Major, S-012):** The ADR mandates YAML frontmatter for "every new ADR" (ADR-M-002/M-013) but does not itself carry that frontmatter — a self-compliance gap the document's own extensive Meta-Note self-audit addresses only for ID-naming, not for the frontmatter schema.

**Improvement Path:** Apply the CC-001 tier-reconciliation fix to L-9; correct the Context section's collision-resolution narrative to match Related Decisions; restate promotion-frequency evidence consistently as "2 correlated projects" everywhere; reconcile the Entity-embedded and "free index" claims; extend the lookalike-ban enumeration; add real YAML frontmatter to this ADR itself.

### Methodological Rigor (0.62/1.00)

**Evidence:**
The options-analysis methodology is exemplary: all six schemes lead with a steelman before critique (H-16 compliance verified independently by S-010, S-004, S-013), trade-study scores are traced and confirmed exact against source (`trade-study.md:217-231`, S-010 and S-011 both independently verified), and the confidence statement (0.70–0.75) is correctly capped at the trade study's own declared ceiling.

**Gaps:**
- **IN-001 (Critical, S-013):** The document's own central methodological principle — deterministic gates over prose promises — is not applied to its own highest-leverage transition: nothing prevents `status: PROPOSED` → `ACCEPTED` before any gating Migration-Plan item (including the lint itself, M-6) is complete. The document elsewhere states "a prose table row is a plan, not evidence of completion" (`ADR:444`) but does not apply that skepticism reflexively to its own ratification event.
- **RT-001 (Critical-leaning-Major, S-001):** An elaborately-engineered, audited waiver-ledger mechanism coexists with an entirely unguarded sibling exemption path (`scripts/adr-grandfather-allowlist.txt`) carrying none of the same review/audit protections — rigor applied unevenly to two mechanisms of equal power.
- **PM-101/PM-102/PM-103 (Major, S-004):** A gating Migration-Plan item (M-2b) rests on an apparently stale model of the `.claude/rules/` symlink mechanism (independently verified this iteration via `Glob`/`Read` diagnostic signature to likely be directory-level, not per-file); the "distinct second-reviewer" waiver design is unsatisfiable against the verified single-owner `.github/CODEOWNERS` state; M-6/M-13 are unreconciled delivery targets (also a Completeness finding).
- **CV-001/CV-002 (Major, S-011):** The self-verification apparatus itself failed twice this iteration — a "corrected per P-022" count (~6) is further from the true count (10) than the estimate it claims to correct, and a "resolved" historical claim contradicts the document's own other sections. This is notable because the package's entire credibility architecture rests on iterative P-022 self-correction; finding the correction process itself in error twice, independently, is a rigor concern about the process, not just isolated content.

**Improvement Path:** Add a concrete technical or single-sentence checklist gate directly beneath the `Status:` field itself; bring the grandfather allowlist under the same waiver protections (or freeze it at the adoption commit); verify the `.claude/rules/` symlink mechanism empirically before keeping M-2b as gating; define an explicit solo-maintainer waiver fallback.

### Evidence Quality (0.68/1.00)

**Evidence:**
Independently verified factual accuracy is genuinely high: S-011's Chain-of-Verification extracted 46 testable claims and found 44 (95.7%) exactly correct against source, spanning quoted line contents, corpus counts, and cross-references; S-003's Steelman independently confirmed ~20 additional load-bearing citations at 100% accuracy. This is a materially higher hit-rate than typical for a C4 document at this stage.

**Gaps:**
- **DA-001 (Critical, S-002):** The decisive, headline "zero-churn"/"overwhelming majority [of citations are] bare-ID" claim (`ADR:373,487`) is contradicted by the dominant citation style in Jerry's own SSOT rule files — `.context/rules/mcp-tool-standards.md:231` and `.context/rules/agent-development-standards.md:445,455` cite ADRs by full relative path, as does the ADR's own References table and the rule draft's own References table. The existing caveat (`ADR:487`) is scoped only to a single external example (`ci.yml`), understating the internal rule-corpus pattern.
- **FM-104 (Critical-leaning-Major, S-012):** "Provenance preserved losslessly" (`ADR:375`) is an unqualified claim; the only lint rule for provenance (L-6) checks *presence*, not *correctness* — nothing prevents (or detects) a copy-pasted, stale `origin_project` value.
- **CV-001 (Major, S-011):** A P-022 "correction" (~6 grammar-family instances in `ps-architect.md`) is itself wrong — the true count, independently re-verified via `Grep`, is 10, exactly matching the original estimate the correction dismisses.

**Improvement Path:** Provide a corpus-derived, `grep`-counted ratio of full-path-to-bare-ID ADR citations and scope the "overwhelming majority" claim accordingly (or schedule remediation of the cited rule files); soften "preserved losslessly" to "preserved by convention (presence-checked, not accuracy-checked)" or add an L-6b correctness check; correct the ps-architect.md occurrence count to 10.

### Actionability (0.62/1.00)

**Evidence:**
The Migration Plan (M-1 through M-14) is unusually operational for a governance ADR: every item is owned, most are explicitly gating-flagged, several carry named acceptance criteria, and the honest "zero worktracker Tasks/GH Issues exist yet" disclosure (`ADR:446`) models the exact transparency this framework expects.

**Gaps:**
- **IN-001 (Critical, S-013):** The 14-item gating apparatus has no technical enforcement on the one transition that activates it (the `status:` field flip) — every "Yes — ratification blocker" label is currently advisory prose only.
- **PM-102 (Major, S-004):** The redesigned waiver mechanism's core premise (a "distinct GitHub identity with review authority") is unsatisfiable given the verified single-owner `.github/CODEOWNERS:14` state (`@geekatron` for every governed path, including `.context/rules/`) — the mechanism cannot currently be exercised as specified.
- **DA-005 (Major, S-002):** Taxonomy governance (M-5b/arbiter) is a non-gating soft process assigned to `ps-architect`, an agent the same package documents as currently non-compliant (Fix 3) with the convention it would police.
- **RT-004/RT-005 (Major, S-001):** Waiver `expires` dates have no described automatic re-enforcement; the override model's own integrity checks (append-only ledger diff, API-verified reviewer) carry no rule ID and are excluded from the M-6 regression test.

**Improvement Path:** Add an explicit, falsifiable pre-ratification checklist directly beneath the Status field (e.g., "no status flip to ACCEPTED without a linked, closed M-6 CI run URL"); define a solo-maintainer waiver fallback; make M-5b gating with a defined cadence and an owner independent of `ps-architect`'s current compliance state, or disclose taxonomy governance as unenforced until M-12 ships.

### Traceability (0.65/1.00)

**Evidence:**
Both files carry navigation tables independently verified H-23/H-24 compliant (24 sections/24 nav rows in the ADR, 14/14 in the rule draft, all anchors resolving including punctuation-heavy headings) by the self-refine pass this iteration. The prior-review tag glossary (line 46) and near-universal file+line citation discipline (independently spot-checked by three separate strategies with a combined ~65+ citations, effectively 100% precise on location) are genuine strengths.

**Gaps:**
- **DA-002 (Critical, S-002):** The ADR and rule draft cross-cite each other via relative markdown links (`ADR:552,584`; `adr-standards-rule-draft.md:189`) that are provably dead-on-ratification once M-2 (moves rule draft content) and M-9 (moves/tombstones the ADR) execute — and no Migration-Plan row addresses either link. This is a self-referential instance of exactly the citation-continuity failure the convention exists to prevent, inside the convention's own founding documents.
- **RT-005 (Major, S-001):** The override model's own integrity mechanisms carry no L-N rule identifier and are excluded from the gating regression test alongside the 16/19-file grandfather test.
- **FM-107/FM-108 (Major, S-012):** No forward-link field exists for `DEPRECATED` → replacement (asymmetric with `SUPERSEDED`'s bidirectional L-7 check); the taxonomy arbiter (TBR-2) is cited without cross-referencing its sibling Open Questions (TBR-1/3/4/5) from the trade study.
- **CC-004 (Minor, S-007):** The "(H-23 / NAV-002)" citation for CLAUDE.md cross-file registration is imprecise — NAV-002 governs a document's own internal nav-table placement, not registration inside a different document's nav table.

**Improvement Path:** Add a Migration-Plan item fixing both cross-deliverable relative links at M-2/M-9 execution time; assign rule IDs to the waiver-ledger integrity checks and include them in the regression test; add a `deprecated_by` WARN-checked field; cross-reference all TBR items; correct the NAV-002 citation.

---

## Findings Inventory Across All Iteration-3 Strategies

Raw severity as assigned by each independently-executed blind strategy (not yet remediated as of this scoring pass — self-refine's own fixes, SM-101/SM-102, are already applied to the file and are excluded from this table since they are resolved):

| Strategy | Critical | Major | Minor | Notable Critical/Major IDs |
|---|---|---|---|---|
| S-001 Red Team | 2 | 3 | 2 | RT-001 (grandfather allowlist bypass), RT-002 (L-10 scope gap) |
| S-002 Devil's Advocate | 2 | 3 | 2 | DA-001 ("zero-churn" falsified), DA-002 (self-referential citation break) |
| S-003 Steelman | 0 | 2 | 3 | SM-201/SM-202 (evidence-completeness, additive not corrective) |
| S-004 Pre-Mortem | 0 | 3 | 4 | PM-101 (stale symlink model), PM-102 (unsatisfiable waiver), PM-103 (unreconciled lint targets) |
| S-007 Constitutional AI Critique | 2 | 1 | 1 | CC-001 (front-loaded overclaim), CC-002 (L-9 tier inconsistency) |
| S-011 Chain-of-Verification | 0 | 2 | 0 | CV-001 (count still wrong), CV-002 (self-contradictory history) |
| S-012 FMEA | 4 | 4 | 1 | FM-101 (self-compliance), FM-102 (topology gap), FM-103 (AE-004), FM-104 (lossless overclaim) |
| S-013 Inversion | 1 | 2 | 2 | IN-001 (ratification gate unenforced) |
| **Raw total** | **11** | **20** | **15** | |

**Scorer's independent severity re-assessment (anti-leniency discipline applied — see [Leniency Bias Check](#leniency-bias-check)):** Of the 11 raw-Critical findings, this scorer treats **5 as genuinely Critical** on independent review of the underlying evidence (IN-001, RT-002, CC-002, FM-102, DA-002) and **6 as high-Major** (RT-001, DA-001, CC-001, FM-101, FM-103, FM-104) — the downgrade reasoning is documented per-finding in [Detailed Dimension Analysis](#detailed-dimension-analysis). This re-assessment does not reduce the composite impact materially: even at high-Major, these findings still depress Internal Consistency, Methodological Rigor, Evidence Quality, and Actionability substantially, and the automatic Critical-finding override still applies because 5 findings remain genuinely Critical under independent scrutiny.

---

## Priority-Ordered Remediation Table

| Priority | ID(s) | Dimension | Owner | Recommendation | Residual Tag |
|----------|-------|-----------|-------|-----------------|--------------|
| 1 | IN-001 | Methodological Rigor, Actionability | ps-architect / governance | Add a single, falsifiable pre-ratification gate directly beneath the `Status:` field (e.g., "no `status: ACCEPTED` edit without a linked M-6 green-CI URL in this ADR's Changelog"); do not rely on the distributed 14-row Migration Plan alone. | [FIXABLE-NOW] — document-edit only |
| 2 | CC-002 | Internal Consistency | ps-architect | Reword L-9 from "FAIL (non-waivable-in-practice)" to "FAIL (waivable-in-principle; see tier reconciliation)" in both files, applying the identical CC-001 fix already made for L-2/L-3. | [FIXABLE-NOW] |
| 3 | RT-002 | Completeness | ps-architect / governance | Extend L-10 (or add a sibling rule) to fuzzy-match project-scoped canonical slugs repo-wide, not only the framework registry; or require one repo-wide index covering both tiers. | [FIXABLE-NOW] — spec edit; the actual fuzzy-match tool build is [INHERENT] pending M-6 |
| 4 | DA-002 | Traceability | ps-architect | Add an explicit Migration-Plan action item (fold into M-2/M-9) fixing both cross-deliverable relative links at the moment of each move. | [FIXABLE-NOW] |
| 5 | FM-102 | Completeness | ps-architect / governance | Add a repository-based Canonical Location Model row and branch the lint-path assumptions and onboarding section on which worktracker topology is in effect. | [FIXABLE-NOW] |
| 6 | CV-001, CV-002 | Evidence Quality, Internal Consistency | ps-architect | Correct "~6" to "10" (ps-architect.md grammar-instance count, both files); correct the Context section's ADR-EPIC002-001 collision-resolution narrative to match Related Decisions/Sensitivity. | [FIXABLE-NOW] |
| 7 | DA-001 | Evidence Quality | ps-architect | Provide a `grep`-derived corpus ratio of full-path vs. bare-ID ADR citations; scope the "overwhelming majority/zero-churn" claim accordingly or schedule rule-file citation remediation. | [FIXABLE-NOW] for the claim scoping; retrofitting `mcp-tool-standards.md`/`agent-development-standards.md` citations is [INHERENT] (out of this document's edit mandate, P-020) |
| 8 | RT-001 | Methodological Rigor | ps-architect / devsecops | Bring `scripts/adr-grandfather-allowlist.txt` under the same audited-waiver schema as `adr-lint-waivers.yaml`, or freeze it at the adoption commit with an L-9-style "no new entries" rule. | [FIXABLE-NOW] spec; actual script build is [INHERENT] pending M-6 |
| 9 | FM-101 | Internal Consistency | ps-architect | Add a real YAML frontmatter block to ADR-PROJ031-004 itself (values already exist in the blockquote header). | [FIXABLE-NOW] — trivial |
| 10 | CC-001 | Evidence Quality | ps-architect | Add a one-clause qualifier at the four present-tense enforcement claims (ADR L0, L1 testing section; rule-draft Tier-and-Scope) matching the existing Claim-Status honesty already present later in both files. | [FIXABLE-NOW] |
| 11 | IN-002, IN-003 | Internal Consistency, Completeness | ps-architect | Reconcile "Entity-embedded (permitted)" wording to the closed 4-prefix set; reword the "free and always current" index claim to match the "long-term liability/gating arbiter" framing elsewhere. | [FIXABLE-NOW] |
| 12 | DA-004 | Internal Consistency | ps-architect | Restate promotion-frequency evidence consistently as "2 correlated framework-mandate projects producing 3 ADRs" in every headline restatement (L0, Status, Rationale, Confidence), not only the Bimodal Refinement section. | [FIXABLE-NOW] |
| 13 | PM-101 | Methodological Rigor | governance | Empirically verify the `.claude/rules/` symlink structure (directory-level vs. per-file) before keeping M-2b gating; correct or remove the item accordingly. | [FIXABLE-NOW] verification + edit |
| 14 | PM-102 | Actionability, Internal Consistency | governance / devsecops | Define an explicit solo-maintainer waiver fallback, or honestly disclose FAIL rules are non-waivable in practice until a second maintainer exists; add the waiver ledger path to `.github/CODEOWNERS`. | [INHERENT] for the actual CODEOWNERS/staffing change; [FIXABLE-NOW] for the disclosure text |
| 15 | PM-103 | Completeness | devsecops / ps-architect | Add a single migration item unifying M-6 (CI Action) and M-13 (CLI subcommand) into one implementation-location spec. | [FIXABLE-NOW] spec; actual implementation is [INHERENT] pending engineering capacity |
| 16 | RT-003, RT-004, RT-005 | Internal Consistency, Traceability | ps-architect / devsecops | Extend the case-folded lookalike-ban to the full worktracker entity-prefix set; specify an automated waiver-expiry re-check; assign rule IDs to the override model's integrity checks and add them to the regression test. | [FIXABLE-NOW] spec edits |
| 17 | FM-104 | Evidence Quality | ps-architect / devsecops | Add an L-6b provenance-*correctness* check, or soften "preserved losslessly" to "preserved by convention (presence-checked, not accuracy-checked)". | [FIXABLE-NOW] soften now; L-6b build is [INHERENT] pending M-6 |
| 18 | FM-103 | Internal Consistency | ps-architect | Add an explicit AE-004 scoping clause to Promotion Path 1 (state whether metadata-only scope/location flips are exempt). | [FIXABLE-NOW] |
| 19 | CC-003 | Completeness, Methodological Rigor | ps-architect / devsecops | Reconcile the mandated YAML frontmatter with `jerry ast frontmatter`'s blockquote-only parsing — switch to blockquote form (zero new tooling) or explicitly scope a YAML-parsing extension into M-6. | [FIXABLE-NOW] decision; tooling extension (if chosen) is [INHERENT] |
| 20 | DA-003, DA-005 | Evidence Quality, Actionability | ps-architect / governance | Name a concrete future ADR to exercise Path 1, or downgrade "default path" framing honestly; make M-5b gating with a defined cadence/owner independent of ps-architect's current non-compliant state. | Framing = [FIXABLE-NOW]; an actual demonstrated Path-1 instance or a staffed arbiter role is [INHERENT] (depends on future events/resourcing) |
| 21 | CC-004, FM-105, FM-106, FM-107, FM-108, FM-109, RT-006, RT-007, DA-006, DA-007, IN-004, IN-005, SM-201..SM-205 | Various (mostly Traceability/Actionability/Completeness, Minor) | ps-architect | Batch of Minor precision/completeness polish items (NAV-002 citation, CLAUDE.md precedent citation, DEPRECATED forward-link, TBR cross-references, Fix-spec preconditions, title-slug freeze, promotion-volume forecast, waiver-substance audit note, stale-citation footprint extension, STORY-015 sensitivity-analysis inclusion). | [FIXABLE-NOW] — all are document-edit-only |
| 22 | R-6 (cross-branch collision race), forward promotion-rate (n=3/n=2-correlated), M-6/M-12 lint+agent implementation | All | devsecops / governance | Already honestly disclosed as monitored, not closed, residuals in the document itself (PM-009, R-6 commitments). No further document edit reduces these; they require either future engineering delivery or future observed data. | [INHERENT] |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing the weighted composite — no dimension score was adjusted to match another.
- [x] Evidence documented for each score, citing specific finding IDs, file paths, and line numbers from the 9 adversarial reports and the two deliverables.
- [x] Uncertain scores resolved downward — where this scorer disagreed with a reviewer's raw severity label (e.g., FM-101, FM-103, CC-001 downgraded from the reviewers' "Critical" to this scorer's "high-Major"), the composite impact was still treated conservatively rather than discounted to zero.
- [x] First-draft calibration considered and explicitly rejected as inapplicable — this is a 3rd-iteration document with two prior remediation cycles (scores 0.67, 0.54); persistence of Critical/Major findings at this stage is treated as more, not less, significant than in a first draft.
- [x] No dimension scored above 0.95 without exceptional documented evidence — the highest dimension score in this report is 0.68 (Evidence Quality), reflecting genuine strength (95.7% independent verification) tempered by two headline-claim contradictions.
- [x] Automatic Critical-finding override applied: composite alone (0.62) would already fall in the REJECTED band; the presence of 5 scorer-confirmed Critical findings removes any ambiguity about whether a marginal composite should round up to REVISE.

---

## Session Context Handoff

```yaml
verdict: REJECTED
composite_score: 0.62
threshold: 0.92
engagement_gate: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.55
critical_findings_count: 5
iteration: 3
improvement_recommendations:
  - "Add a technical or single-sentence checklist gate directly beneath the Status: field to block premature ratification (IN-001)"
  - "Apply the already-diagnosed CC-001 tier-reconciliation fix to L-9 (CC-002)"
  - "Extend L-10 taxonomy-synonymy coverage to project-scoped canonical ADRs, the recommended-default population (RT-002)"
  - "Fix the two self-referential relative links between the ADR and rule draft before/at M-2 and M-9 (DA-002)"
  - "Add a repository-based Canonical Location Model row and branch lint/onboarding on worktracker topology (FM-102)"
  - "Correct the ps-architect.md occurrence count (10, not ~6) and the ADR-EPIC002-001 collision-resolution narrative (CV-001, CV-002)"
  - "Scope the 'zero-churn'/'overwhelming majority' citation claim against a grep-derived corpus ratio (DA-001)"
```
