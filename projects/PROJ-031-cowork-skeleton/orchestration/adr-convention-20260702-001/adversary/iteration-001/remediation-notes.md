# Remediation Notes — Iteration 1 (Owner-First, ps-architect creator/owner)

> **Deliverables remediated:**
> - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`
> - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
>
> **Inputs:** `s-014-quality-score.md` (priority-ordered remediation table) + all 9 findings files in `iteration-001/`.
> **Score before:** 0.67 (REVISE) | **Engagement gate:** 0.95 | **SSOT gate:** 0.92.
> **Constitutional:** P-003 (no subagents), P-020 (edited only the two mandated files + this notes file; did NOT touch `ci.yml`, template, SKILL.md, or create worktracker entities — those are documented as tracked Migration-Plan actions instead), P-022 (every factual claim cited to file:line; inference labeled).
>
> **This file is written incrementally** (P-002): sections are appended as each remediation lands so partial output survives an infrastructure stall.

## Navigation

| Section | Purpose |
|---------|---------|
| [Disposition Legend](#disposition-legend) | What each status means |
| [Verified Facts Used](#verified-facts-used) | On-disk confirmations feeding the edits |
| [P0 Remediations](#p0-remediations) | Critical gating items |
| [P1 Remediations](#p1-remediations) | Major items |
| [P2 Remediations](#p2-remediations) | Minor items |
| [P3 / Inherent Items](#p3--inherent-items) | Framed-not-closed + out-of-mandate |
| [Rebuttals](#rebuttals) | Findings judged invalid, with evidence |
| [Change Ledger](#change-ledger) | Every edit, file:anchor |

---

## Disposition Legend

| Status | Meaning |
|--------|---------|
| FIXED | Edited the deliverable(s) to fully close the finding |
| FIXED-DOC | Closed by documenting a tracked action (item is out-of-file, e.g. `ci.yml` fix) rather than performing an out-of-mandate edit (P-020) |
| FRAMED | [INHERENT] residual — added honest Claim-Status framing rather than pretending closure |
| REBUTTED | Judged invalid; rebutted with cited evidence, no silent ignore |

---

## Verified Facts Used

All confirmed on disk this session (P-022 provenance):

1. `.github/workflows/ci.yml:2` cites `projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md` — a **full-path** citation to a **9th ID family** (`ADR-CI`) at a project path absent from the repo. Confirms RT-003, FM-007, and FM-013 (full-path citations exist and break under `git mv`).
2. Framework-ADR frontmatter forms: `ADR-agent-design-001.md:3` = HTML comment; `ADR-routing-triggers-001.md:3` = HTML comment; `ADR-output-path-resolution-001.md:3-8` = blockquote with `**Parent:** EPIC-002`. **None** use YAML; none carry `origin_project`/`scope`. Confirms FM-003 / PM-006.
3. EPIC-002 ADRs on disk in `projects/PROJ-001-oss-release/decisions/`: exactly two — `ADR-EPIC002-001-strategy-selection.md`, `ADR-EPIC002-002-enforcement-architecture.md` (both local); plus `docs/design/ADR-output-path-resolution-001.md` (`Parent: EPIC-002`, promoted). So 3 ADRs were born under EPIC-002, 1 promoted. The cited advocate source (`advocate-domain-slug.md:125`) said "1 of EPIC-002's 2 ADRs" — it omitted `enforcement-architecture`. The ADR's "1-of-3" is the more accurate figure. Confirms SM-004 (reconciliation needed, not error).
4. `DEC-NNN` appears in bare form (`DEC-001-cli-hook.md`, `DEC-001-template-fidelity.md`) at Enabler/Story levels but composite (`EPIC-001--DEC-001-*`) at Epic/Feature levels (`worktracker-directory-structure.md:65,73,80,88`). Confirms FM-021 (bare `DEC-NNN` form exists).

---

## P0 Remediations

| ID | Finding(s) | Disposition | Edit |
|----|-----------|-------------|------|
| P0-1 | SM-001, PM-001, CC-001, FM-001, IN-001 (5/7 convergent) | FIXED | Split L-1 into disjunctive **L-1a (lowercase canonical) / L-1b (uppercase entity dialect `^ADR-(PROJ\|EPIC\|FEAT\|STORY)\d{3}-\d{3}...`)** in both files; a filename passes if it matches EITHER. Added a **mandatory 16-file grandfather regression test** gating L-1 completion, filesystem-verified this session. Rule draft [ID Scheme] + [L5 CI Lint Specification]; ADR [Enforcement Design]. |
| P0-2 | RT-002 | FIXED | Replaced the bare `adr-lint: ignore` override with a **structured, append-only `adr-lint-waivers.yaml`** (rule, path, >=40-char justification, second-reviewer `approved_by`, `expires`); made **L-2/L-3 non-waivable** (correctness, not style). Both files. |
| P0-3 | RT-003, FM-007 | FIXED (catalog + lint) / FIXED-DOC (ci.yml) | Added the **9th `ADR-CI` family** row + a corpus-survey correction note to the ADR; added **lint L-8 free-text/config citation scan** (both files). The actual `ci.yml:2` repair is tracked as **M-10** (not edited here, P-020). |
| P0-4 | FM-013 | FIXED | Added a full-path-citation caveat to **Promotion Path 1**: bare-ID citations survive `git mv`, but full-path citations (proven present at `ci.yml:2`) still need re-pointing; L-8 surfaces survivors. ADR [Path 1]. |
| P0-5 | FM-008, RT-006 | FIXED | Added **L-8** (repo-wide prose/path/config scan) alongside the renamed **L-7 (structured)** so the standard's traceability guarantee covers the exact stale-citation class it cites as motivation. Both files. |
| P0-6 | RT-001, PM-002, FM-015, IN-001 | FIXED (in-file) | Rewrote the Adoption table: every gating item now carries a **TBD-Task + GH Issue (H-32)** column; **M-6 marked a ratification blocker requiring independently-verified completion**; added the explicit rule that ratification is conditional on verified completion, not a checklist row. (Creating the actual worktracker/GH entities is out of the "edit two files" mandate — documented as the gating requirement instead, P-020.) |

## P1 Remediations

| ID | Finding(s) | Disposition | Edit |
|----|-----------|-------------|------|
| P1-1 | SM-003, PM-005, IN-003, FM-019 | FIXED | Named the taxonomy arbiter (TBR-2) as new **M-5b**: `ps-architect` runs an automated fuzzy-match of new slugs against the `docs/design/README.md` registry (M-5), near-duplicates flagged for human adjudication. **Elevated M-5** from optional to gating (it is the manual collision check until the lint ships). ADR Adoption table. |
| P1-2 | SM-002, PM-007, IN-006 | FIXED | Extended **L-4** to validate the `ADR-EPIC{NNN}-NNN` / `ADR-STORY{NNN}-NNN` entity-embedded dialect against `origin_entity` + containing `work/.../{ENTITY}/` path, matching the coverage `PROJ` already had. Both files. |
| P1-3 | PM-006, FM-003 | FIXED | Corrected the "Zero cost" Migration row to "**Low, not zero**" with the verified non-YAML frontmatter state (2 HTML comments, 1 blockquote); added **M-11** YAML-retrofit action. ADR Migration Plan. |
| P1-4 | SM-004 | FIXED | Added a **count-reconciliation blockquote** explaining 1-of-3 (corrected) vs the advocate source's 1-of-2 (omitted `enforcement-architecture`); noted the qualitative conclusion is denominator-independent. ADR [Bimodal refinement]. |
| P1-5 | PM-003 | FIXED | Added **M-2b**: create the `.claude/rules/adr-standards.md` symlink (precedent `PROJ-007/EN-001.md:53`), marked gating — without it the rule never auto-loads. ADR Adoption table. |
| P1-6 | CC-002, PM-008 | FIXED | Rewrote **M-7** to justify rule-file registration on **H-23/NAV-002 discoverability**, explicitly noting H-26 governs *skill* (not rule-file) registration. ADR Adoption table. |
| P1-7 | PM-004, IN-002, SM-006, FM-023 | FIXED | Took both offered routes: added **M-9** (execute this ADR's own Path-2 self-promotion, gating on acceptance) AND tightened **ADR-M-003** so known-framework-scope / C3–C4 ADRs SHOULD NOT use the dialect, with the parent ADR disclosed as the deliberate mandated exception. ADR Adoption table + rule draft ADR-M-003. |
| P1-8 | IN-004 | FIXED | Added a **zero-governance / index-search null-alternative** subsection to the Rationale: null wins on adoption cost but loses on citation-integrity (the load-bearing failure), collision-safety, and freshness; benchmark confirms a convention is warranted. ADR [Rationale]. |

## P2 Remediations

| ID | Finding(s) | Disposition | Edit |
|----|-----------|-------------|------|
| P2-1 | FM-016 | FIXED | Renamed template Fix F1-a placeholder `{SCOPE}` → `{DOMAIN-SLUG}` with an explicit note that `scope` is a reserved *mutable* frontmatter field and must not name the *immutable* identifier. Rule draft Fix 1. |
| P2-2 | FM-017 | FIXED | Made SKILL.md Fix F2-a/F2-d **location-conditional** (project-first default per AD-M-011, framework only when framework-scoped) instead of hardcoding all architecture-agent ADRs to `docs/design/`. Rule draft Fix 2. |
| P2-3 | FM-010 | FIXED | Added an explicit prohibition (both files): an amendment MUST NOT change `scope`/`origin_project`/location — those go through Promotion (scope/location) or are forbidden (origin). |
| P2-4 | FM-018 | FIXED | Published a locally-runnable **pre-flight slug-collision one-liner** (identical to lint L-3) in the ADR verification section, so collisions surface before commit, not only post-merge. |
| P2-5 | FM-021 | FIXED | Reframed the "sole ontology exception" in **4 places** (L0, L2, ADR-M-011, and via the DEC-NNN framing) around scope **mutability**, explicitly acknowledging `DEC-NNN`'s bare Enabler/Story form so the claim is no longer literally over-broad. |
| P2-6 | FM-014 | FIXED | Added an append-only/historical-records **exclusion list** (CHANGELOGs, commit messages, release notes) to Path 2's grep-replace step in both files, preventing silent rewriting of historically-accurate references. |

## P3 / Inherent Items

| ID | Finding(s) | Disposition | Handling |
|----|-----------|-------------|----------|
| P3-1 | RT-005 | FRAMED [INHERENT] | Added risk **R-6** with a `Claim-Status: MITIGATED-NOT-ELIMINATED` label: no registry-free scheme eliminates the cross-branch same-slug `NNN` race (a central counter is rejected by c-006); domain-slug partitioning lowers *frequency*, and L-3 + the pre-flight command *detect* it. Honestly bounded, not pretended closed. |
| P3-2 | S-002 halt | OUT-OF-MANDATE | Orchestrator-owned tournament-completeness item (re-invoke Devil's Advocate with a Prior-Strategy-Outputs reference). Not a deliverable defect; cannot be fixed by editing the two files. Flagged for the orchestrator. |
| P3-3 | S-013 blind-protocol contamination | OUT-OF-MANDATE | Orchestrator-owned tournament-independence review; already disclosed/contained per P-022. Not a deliverable defect. |

## Additional (Major FMEA gaps flagged in dimension analysis, not in the P-table)

| Finding | Disposition | Edit |
|---------|-------------|------|
| FM-005 (no draft→canonical procedure) | FIXED | Added **Path 0** (draft/orchestration → canonical `decisions/` home; no tombstone) to the Promotion Process in both files. |
| FM-020 (status-transition validity) | FIXED | Added a **valid-status-transition table** to the ADR Status Vocabulary (terminal states, invalid `PROPOSED`→`DEPRECATED`, etc.). |
| FM-009 (amendment-block ordering) | FIXED | Specified reverse-chronological ordering under a single `## Amendments` heading. ADR Status Vocabulary. |
| FM-011 (combined supersede+promotion) | FIXED | Specified that a simultaneous supersede+promote is handled as one Path-2 event (tombstone subsumes supersession). ADR Status Vocabulary. |
| FM-006 (`Frozen Legacy` heading vs grandfathered rows) | FIXED | Renamed the rule-draft section to **"Frozen and Grandfathered Legacy"** (+ nav anchor) with a disambiguating note. |
| CV-003 (BUG-006 "never adopted" vs "acted upon") | FIXED | Added a bridging clause in Context: finding accepted + one remediation acted upon, but never codified as a standing rule — both true, non-contradictory. |
| CC-002 / PM-008 (M-7 H-26 misattribution) | FIXED | See P1-6. |
| CC-004 (C4 vs AE-002/AE-003 C3 floor) | FIXED | Corrected the Criticality header + footer: AE-002/AE-003 set a C3 floor; C4 comes from the C4 tier definition itself. |

## Rebuttals

Two findings are accepted **in substance** (fix implemented) but I contest their **severity/interpretation** on evidence. These are severity rebuttals, not validity rebuttals — recorded transparently rather than silently downgrading.

1. **FM-013 severity (Critical / RPN 448) — contested; substance accepted & fixed.** The finding is right that full-path citations exist (`.github/workflows/ci.yml:2`, verified) and that Path 1's original "no re-pointing is required… every existing citation remains valid" was over-absolute; I added the caveat (P0-4) and lint L-8 (P0-5). **But the Critical/448 severity overstates real-world impact.** The dominant citation form in the corpus is the **bare ID in prose** (e.g. references to `ADR-agent-design-001`, entity IDs), for which Path 1 genuinely requires *zero* re-pointing; full-path citations are a small minority (one verified live instance repo-wide). The mechanism the ADR calls "the whole point" therefore holds for the overwhelming majority — the defect was over-absolute *phrasing*, not a broken *mechanism*. Fix kept; severity judged overstated.
2. **"M-6 lint unimplemented" as an ADR-quality defect — contested; actionability fix accepted.** I accept and strengthened the actionability guidance (M-6 now a tracked, owned, gating ratification blocker — P0-6). **But I push back on any reading that the lint's non-existence is a defect of the decision document itself.** A `PROPOSED` ADR's job is to *specify* enforcement; *building* it is M-6, explicitly post-ratification and gated behind M-1 (user ratification). Evidence: the Status section states the decision "is not in force until a human ratifies it," and M-1 gates all downstream items. Scoring the ADR down because a migration artifact it schedules for after ratification does not yet exist conflates "the decision" with "the executed migration." The gap is expected-state-of-a-proposal, not a document defect.

## Change Ledger

- **ADR** (`decisions/ADR-PROJ031-004-adr-identifier-convention.md`): 19 edits — header Criticality (CC-004), L0 mutability reframe (FM-021), Context 9th-family catalog + correction (P0-3), Context BUG-006 bridge (CV-003), bimodal count reconciliation (P1-4), Rationale null-alternative (P1-8), L2 ontology reframe (FM-021), Consequences risks R-5/R-6 (P3-1), Migration zero-cost row (P1-3), Adoption table M-1..M-11 (P0-6/P1-1/5/6/7, P0-3, P1-3), Promotion Path 0 (FM-005), Path 1 caveat (P0-4), Path 2 exclusion (P2-6), Amend boundary (P2-3), Status transitions + amendment ordering (FM-020/009/011), Enforcement Design intro+lint table (P0-1/2/3/5, P1-2), pre-flight command (P2-4), Criticality footer (CC-004), + changelog entry.
- **Rule draft** (`design/adr-standards-rule-draft.md`): 12 edits — ID Scheme L-1a/L-1b (P0-1), L5 lint spec table (P0-1/2/3/5, P1-2), regression-test + L-1 scope note (P0-1), ADR-M-003 dialect restriction (P1-7), Fix F1-a token (P2-1), Fix F2 location-conditional (P2-2), Supersede/Amend prohibition (P2-3), ADR-M-011 reframe (FM-021), Path 0 (FM-005), Path 2 exclusion (P2-6), Frozen-Legacy nav + heading (FM-006).
