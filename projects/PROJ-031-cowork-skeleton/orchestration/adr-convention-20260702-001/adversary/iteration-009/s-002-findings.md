# Devil's Advocate Report: ADR-PROJ031-004 + adr-standards-rule-draft.md (Iteration 9)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy metadata |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | DA-NNN findings with severity |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 action list |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |

---

## Header

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.10) + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-002, iteration 9)
**H-16 Compliance:** S-003 Steelman applied this iteration prior to this critique (`adversary/iteration-009/s-003-findings.md` confirmed present via file-existence check; contents not read, per blind protocol).

---

## Summary

This iteration attacks the package's central, load-bearing empirical claim — that Scheme B's promotion mechanic ("`git mv`, no ID churn") delivers an **honest, low-citation-breakage promotion process** — and finds it **falsified by evidence already present in the live corpus**, not merely under-tested. The flagship promoted-ADR precedent the document cites as proof that "the corpus has already voted" for Scheme B currently contains at least 13 broken relative-path citations to its own origin-project supporting material (DA-001, Critical), a fact undetected through this ADR's own 9-iteration adversarial tournament, the cited document's own prior C4 tournament, and the original BUG-006 remediation that produced it. This same failure mode is independently reproduced, forward-looking, in this ADR's own scheduled self-promotion plan (M-9), which is explicitly under-scoped to fix only one of at least five relative links that will break on execution (DA-002, Critical). The root cause — the convention specifies ID/location/frontmatter grammar exhaustively but is silent on how an ADR should cite non-ADR sibling artifacts so those citations survive promotion — is itself an uncovered gap in the 13-standard MEDIUM core (DA-003, Major). These three findings are **not** among the disclosed R-1…R-17 / R-A/R-B/R-C residuals: R-B addresses *inbound* citations to an ADR's own identity going stale, not *outbound* citations from a promoted ADR to sibling project files. Recommend **REVISE**: DA-001 and DA-002 must be dispositioned (fix or explicitly registered as a new residual with owner+cadence) before this package can honestly claim its promotion process delivers what it promises.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260706-i9 | Flagship promoted-ADR precedent contains 13 currently-broken outbound citations, undetected for 3+ months across two C4 tournaments | Critical | `docs/design/ADR-output-path-resolution-001.md:380,481,529,593,602,632-635,642` | Evidence Quality, Internal Consistency |
| DA-002-20260706-i9 | This ADR's own self-promotion (M-9) is under-scoped: at least 5 relative links across both deliverables will break on execution and are not in the stated repair plan | Critical | ADR `:85,213,780` (`../FEEDBACK-LOG.md`); ADR `:652` (`../orchestration/.../subtraction-pass-notes.md`); rule-draft `:165` (`../decisions/ADR-PROJ031-003-...`); Migration Plan row M-2 (`ADR-PROJ031-004-adr-identifier-convention.md:530`) | Methodological Rigor, Completeness |
| DA-003-20260706-i9 | The 13-standard MEDIUM core (ADR-M-001…013) never addresses how an ADR should cite non-ADR sibling artifacts so citations survive promotion — the root cause enabling DA-001/DA-002 | Major | `adr-standards-rule-draft.md:44-58` (full ADR-M-001…013 list; no citation-style standard present) | Completeness, Actionability |

**Finding ID format:** `DA-NNN-{execution_id}` where `execution_id = 20260706-i9` (iteration 9, 2026-07-06).

---

## Finding Details

### DA-001: The "corpus has already voted" evidentiary claim rests on a precedent document that is itself silently broken [CRITICAL]

**Claim Challenged:** The ADR's Rationale argues (line "Jerry's own thesis picks the regime, and the corpus has already voted") that promoted framework ADRs are proof the promotion mechanic works, and the Related Decisions table (`ADR-PROJ031-004-adr-identifier-convention.md`, Related Decisions) names `ADR-output-path-resolution-001` explicitly as **PRECEDENT**: "Migrated in the ~150-reference BUG-006 remediation… the paid promotion tax this decision removes." Consequences §Positive-1 further claims promotion "removes the ID-string-churn *cause*" of citation breakage "for the bare-ID majority."

**Counter-Argument:** The cited precedent document is not clean. `docs/design/ADR-output-path-resolution-001.md` contains at least 13 markdown hyperlinks of the form `../../PROJ-030-bugs/work/BUG-006-*.md` (and one `TASK-008-*.md`) at lines 380 (4 links), 481, 529, 593, 602, 632, 633, 634, 635, 642. Relative to the file's actual location (`docs/design/`), `../../PROJ-030-bugs/...` resolves to `{repo-root}/PROJ-030-bugs/...`. That path does not exist. Verified via `Glob` (`PROJ-030-bugs`, `*/PROJ-030-bugs`, `docs/PROJ-030-bugs` — zero matches); the real file lives at `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md` (verified present). The links are missing the `projects/` path segment — they have been broken since authoring and have never been repaired.

**Evidence:** `docs/design/ADR-output-path-resolution-001.md:380` — `"(source: [BUG-006 audit details](../../PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md) with line-level audits in [eng-audit](../../PROJ-030-bugs/work/BUG-006-eng-audit-detail.md), [red-audit](../../PROJ-030-bugs/work/BUG-006-red-audit-detail.md), [ux-audit](../../PROJ-030-bugs/work/BUG-006-ux-audit-detail.md))."` — 4 broken links in one line; identical pattern repeats at `:481,529,593,602,632,633,634,635,642` (10 lines, 13 links total). Correct target confirmed to exist at `projects/PROJ-030-bugs/work/BUG-006-skill-output-path-hardcoded.md` (Glob-verified).

**Impact:** This is not a hypothetical worst case the disclosed R-B residual already covers — R-B is scoped to *inbound* citations (other documents citing an ADR's ID/path going stale after that ADR moves or renames). This is the opposite direction: a promoted ADR's own *outbound* citations to co-located project supporting material (audit files, task files) that never travel with it. The convention's central selling point — "promotion is a pure file move… zero-churn" — is evidenced only by an example that is itself silently broken, and no mechanism in the 5-rule lint core (L-1/L-2/L-3/L-4/L-7) or the disclosed residual register would ever catch this class of break (L-7 checks only YAML relationship-field targets, not markdown body hyperlinks). Two full C4 adversarial tournaments (BUG-006's own, and 8 prior iterations of this one) cited this file as clean precedent without anyone dereferencing its links. This directly undermines "honest promotion process": the honesty claim was never actually verified against the one real example available.

**Dimension:** Evidence Quality (the load-bearing empirical claim is unsupported — worse, contradicted — by its own cited evidence); Internal Consistency (Related Decisions table asserts a clean "PRECEDENT" that does not hold).

**Response Required:** Either (a) repair the 13 broken links in `docs/design/ADR-output-path-resolution-001.md` (out of this ADR's edit mandate per P-020, but MUST be tasked — extend Migration Plan M-10, which already handles "known live stale/dangling citations," to explicitly include this class), or (b) if left unrepaired, downgrade the Related Decisions / Rationale claim from "the corpus has already voted" / "PRECEDENT… works" to an honestly-qualified statement that the one available real-world example has NOT been verified clean and is known to contain unrepaired breakage.

**Acceptance Criteria:** M-10 (or a new Migration Plan row) explicitly names this class of break (outbound relative-links-to-sibling-project-files in already-promoted `docs/design/` ADRs) with an owner and a verification step (e.g., a markdown link-checker run over `docs/design/*.md`), OR the Rationale/Related-Decisions prose is corrected to state plainly that the promotion precedent's citation integrity has not been verified and is now known to be broken in at least one instance.

---

### DA-002: The ADR's own "worked example of self-compliance" (M-9) is planned to reproduce the exact failure it exists to prevent [CRITICAL]

**Claim Challenged:** The Meta-Note states this ADR's scheduled Path-2 self-promotion (M-9) "makes the ADR a **worked example of its own Path-2 promotion and grandfathering rules** — the discouraged rename it exists to help future authors avoid," and Migration Plan row M-2 states its cross-link repair scope explicitly: "(a) *this* rule file's inbound relative link to the parent ADR… to the ADR's post-M-9 canonical path… and (b) the parent ADR's outbound relative links to `../design/adr-standards-rule-draft.md`… to the new `.context/rules/adr-standards.md` path."

**Counter-Argument:** M-2's stated repair scope is textually limited to the single reciprocal ADR↔rule-draft link pair. It does not mention, and no other Migration Plan row mentions, at least five additional relative markdown links across the two deliverables that will break the moment M-9/M-2 execute:

1. `ADR-PROJ031-004-adr-identifier-convention.md:85` — `[FEEDBACK-LOG.md → FU.0](../FEEDBACK-LOG.md)`
2. `ADR-PROJ031-004-adr-identifier-convention.md:213` — same target, `../FEEDBACK-LOG.md`
3. `ADR-PROJ031-004-adr-identifier-convention.md:780` — same target, `../FEEDBACK-LOG.md` (Changelog v1.7 entry)
4. `ADR-PROJ031-004-adr-identifier-convention.md:652` — `[subtraction-pass-notes.md](../orchestration/adr-convention-20260702-001/subtraction-pass-notes.md)`
5. `adr-standards-rule-draft.md:165` — `[Claim-Status Convention precedent](../decisions/ADR-PROJ031-003-credential-protection-supply-chain.md#claim-status-convention-p-022--foundational)`

Relative to the ADR's *current* location (`projects/PROJ-031-cowork-skeleton/decisions/`), links 1–4 resolve correctly today. After M-9 moves the ADR to `docs/design/ADR-adr-convention-001-*.md`, the same unmodified relative syntax `../FEEDBACK-LOG.md` resolves to `docs/FEEDBACK-LOG.md` (nonexistent) and `../orchestration/.../subtraction-pass-notes.md` resolves to `docs/orchestration/.../subtraction-pass-notes.md` (nonexistent) — both broken, and neither is named anywhere in the Migration Plan, the Meta-Note, or the residual register. Link 5 is a *different* failure instance in the companion rule draft: it cites a **sibling** ADR (`ADR-PROJ031-003`, which is correctly grandfathered *in place* and never moves) — yet the mere relocation of the *citing* rule-draft file from `projects/PROJ-031-cowork-skeleton/design/` to `.context/rules/` (M-2) breaks this link regardless of whether the cited ADR ever moves, because `../decisions/ADR-PROJ031-003-...` relative to `.context/rules/` resolves to `.context/decisions/ADR-PROJ031-003-...` (nonexistent). M-2's stated repair scope names only the rule-draft's link to "the parent ADR" (ADR-004) — it never mentions ADR-003.

**Evidence:** Grep-verified relative-link inventory: `ADR-PROJ031-004-adr-identifier-convention.md:85,213,780` (`../FEEDBACK-LOG.md`, 3 occurrences) and `:652` (`../orchestration/adr-convention-20260702-001/subtraction-pass-notes.md`); `adr-standards-rule-draft.md:165` (`../decisions/ADR-PROJ031-003-credential-protection-supply-chain.md#claim-status-convention-p-022--foundational`). M-2's repair scope is quoted verbatim at `ADR-PROJ031-004-adr-identifier-convention.md:530` and covers only the ADR↔rule-draft (ADR-004) pair. **Inference labeled (P-022):** M-9/M-2 have not yet executed, so these links are not *currently* broken — this is a forward-looking prediction. Confidence in that prediction is high precisely because DA-001 demonstrates the *identical* failure mode (relative link to sibling project file, broken by relocation, unrepaired) already occurred, unnoticed, in the one comparable promotion this repo has performed.

**Impact:** The convention's flagship, explicitly-named pedagogical demonstration of "how to promote honestly" is currently planned to ship with at least 4 broken links in the ADR itself and to leave a 5th broken link permanently unaddressed in the companion rule draft (since it references a different ADR never contemplated by the ADR-004↔rule-draft reciprocal-repair framing). If M-9 executes as currently scoped, the convention's teaching artifact — the thing "future authors" are meant to model — will itself exhibit the citation-continuity failure the whole ADR exists to eliminate, at the moment of its own most-scrutinized self-application.

**Dimension:** Methodological Rigor (the self-compliance demonstration's own execution plan is incompletely specified); Completeness (Migration Plan does not enumerate all citation-repair targets for M-9/M-2).

**Response Required:** Before M-9 executes, extend M-2's cross-link repair scope (or add a new Migration Plan row) to explicitly enumerate and repair: the 3 `../FEEDBACK-LOG.md` links (repoint to `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` or an appropriate `docs/design/`-relative equivalent, or convert to a repo-root-relative citation style, per DA-003), the `subtraction-pass-notes.md` link, and the rule-draft's `ADR-PROJ031-003` link.

**Acceptance Criteria:** Migration Plan M-2/M-9 rows (or a new row) name all five links above by line number, with a stated repair action for each, before M-9 is marked as executable/complete.

---

### DA-003: No standard governs how an ADR cites non-ADR sibling artifacts — the root cause enabling DA-001 and DA-002 [MAJOR]

**Claim Challenged:** The companion rule draft's MEDIUM Standards (ADR-M-001 through ADR-M-013, `adr-standards-rule-draft.md:44-58`) claim to be the operative governance for "ADR identifiers, location, promotion, superseding, and amendment" — implicitly a complete authoring standard for the artifact class.

**Counter-Argument:** None of the 13 standards addresses how an ADR (or its companion documents) should cite *non-ADR* sibling project artifacts — research surveys, trade studies, advocate documents, audit files, FEEDBACK-LOG entries — such that those citations survive a promotion-triggered relocation. This ADR itself demonstrates two different, inconsistent citation styles in its own body: the References table (`ADR-PROJ031-004-adr-identifier-convention.md:742-753`) uses repo-root-relative inline-code paths (e.g., `` `projects/PROJ-031-cowork-skeleton/orchestration/.../trade-study.md` ``, robust to the *citing* document's own relocation), while the in-body prose throughout uses `../`-relative markdown hyperlinks (e.g., `../FEEDBACK-LOG.md`, `../design/adr-standards-rule-draft.md#...`) that DA-001/DA-002 show are exactly what breaks. The convention prescribes ID grammar, location, frontmatter, promotion mechanics, and supersession in exhaustive, multiply-revised detail, yet is silent on this specific, now twice-demonstrated failure surface.

**Evidence:** `adr-standards-rule-draft.md:44-58` (the complete ADR-M-001…013 list — none references citation style for non-ADR artifacts); contrast `ADR-PROJ031-004-adr-identifier-convention.md:742-753` (repo-root-relative References style) against the `../`-relative in-body style at the DA-002 evidence lines.

**Impact:** Without a stated standard, every future ADR promotion (Path 1 or Path 2) that cites project-local supporting material via `../`-relative markdown links is exposed to the identical, silent breakage demonstrated twice in this review — and, per the 5-rule lint's own descoped-items list (`adr-standards-rule-draft.md:201`), no future lint rule is even contemplated for this class, since it falls outside "structural frontmatter links" (L-7's only relationship-checking mechanism).

**Dimension:** Completeness (the standard omits a needed authoring rule); Actionability (future authors have no guidance to avoid the DA-001/DA-002 failure mode).

**Response Required:** Add a MEDIUM standard (e.g., ADR-M-014) recommending that ADRs cite non-ADR sibling artifacts using repo-root-relative paths (matching this ADR's own References-table convention) rather than `../`-relative markdown links, or explicitly disclose the residual with an owner and cadence (matching the rigor already applied to R-1…R-17) if the doctrine prefers not to add a 14th standard.

**Acceptance Criteria:** Either a new MEDIUM standard is added recommending a citation style robust to relocation, or the gap is named as a disclosed residual (with an R-18 entry, owner, and detection signal) rather than left silently absent from both the standards list and the residual register.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance/next gate):**
- DA-001: Extend Migration Plan M-10 (or add a new row) to name and repair the 13 broken outbound links in `docs/design/ADR-output-path-resolution-001.md`, or explicitly downgrade the "corpus has already voted" / "PRECEDENT… works" claims to reflect that the sole cited example is unverified and currently broken.
- DA-002: Before M-9 is treated as ready to execute, extend M-2's stated repair scope to cover all five identified relative links (3× `../FEEDBACK-LOG.md`, 1× `subtraction-pass-notes.md`, 1× rule-draft's `ADR-PROJ031-003` link).

**P1 (Major — SHOULD resolve; justify if not):**
- DA-003: Add a citation-style MEDIUM standard for non-ADR sibling references, or register it explicitly as a new disclosed residual (R-18) with owner and cadence, consistent with the rigor already applied elsewhere in this package.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-002 (Migration Plan under-scoped for M-9), DA-003 (no citation-style standard) |
| Internal Consistency | 0.20 | Negative | DA-001 (Related Decisions table's "PRECEDENT… works" claim contradicted by the cited document's actual state) |
| Methodological Rigor | 0.20 | Negative | DA-002 (the self-compliance demonstration's own execution plan is incomplete) |
| Evidence Quality | 0.15 | Negative | DA-001 (the load-bearing "corpus has already voted" claim is unsupported by its own cited evidence) |
| Actionability | 0.15 | Negative | DA-003 (no guidance for future authors to avoid the demonstrated failure mode) |
| Traceability | 0.10 | Neutral | Findings themselves are fully traceable to file+line; no traceability defect found in the reviewed material itself |

**Overall assessment:** REVISE. The package's central promotion-honesty claim is not merely under-evidenced (as already disclosed via R-B/R-A/R-C) — it is actively contradicted by verifiable, currently-live breakage in the one real example available, and the package's own forward plan (M-9) does not yet account for reproducing the same failure in its own flagship self-promotion. These are not cosmetic and are not already-disclosed residuals; they attack the "honest promotion process" pillar of the standard's purpose directly.

---

## Execution Statistics
- **Total Findings:** 3
- **Critical:** 2
- **Major:** 1
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5
