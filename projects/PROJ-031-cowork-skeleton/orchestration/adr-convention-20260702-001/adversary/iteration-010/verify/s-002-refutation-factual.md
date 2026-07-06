# Refutation Panel — S-002 Findings, Factual-Accuracy Lens (Iteration 10)

> **Panel role:** Attempt to REFUTE every Critical finding in `adversary/iteration-010/s-002-findings.md`. Default to REFUTED if uncertain.
> **Lens:** Factual accuracy — does the cited defect actually exist in the CURRENT deliverables at the cited locations?
> **Scope:** Critical findings only (002-001, 002-002). 002-003 is Major and out of this panel's mandate.
> **Blind protocol:** Only the target report + the two deliverables + `subtraction-pass-notes.md` were read. No other refuters'/panels' outputs were read.

---

## 002-001: L-4 ID↔location undefined/broken for the corpus's own entity-dialect ADRs [CRITICAL]

**Verdict: VERIFIED**

**Reasoning:**

1. Re-read the Canonical Location Model at `ADR-PROJ031-004-adr-identifier-convention.md:384-393` (identical table at `adr-standards-rule-draft.md:77-86`). Confirmed the table has exactly 8 rows and only two dialect rows: "Project (permitted dialect)" (`projects/PROJ-NNN-*/decisions/` → `ADR-PROJ{NNN}-NNN` only, not the full closed set) and "Entity-embedded (permitted) — closed prefix set only" (`projects/.../work/.../{ENTITY}/` → the full `{PROJ|EPIC|FEAT|STORY}NNN-NNN` set, but only inside a `work/.../{ENTITY}/` home).

2. Independently verified via `Glob('projects/PROJ-001-oss-release/decisions/*')`: `ADR-EPIC002-001-strategy-selection.md` and `ADR-EPIC002-002-enforcement-architecture.md` both exist directly inside a plain project `decisions/` folder — not nested under any `work/.../{ENTITY}/` path. This is confirmed real, not hypothetical.

3. This location/ID-form combination (EPIC-prefixed dialect ID, physically in a project `decisions/` dir rather than an entity-embedded `work/` dir) genuinely matches neither Location Model row as literally written. L-4's spec text (`ADR:689` / `adr-standards-rule-draft.md:178`, both grep-verified) — "matches its containing project/entity dir" — has no stated resolution for this exact case.

4. Confirmed this is textually distinct from R-10 (`ADR:474`, `adr-standards-rule-draft.md:177/179/181`): R-10 is explicitly about **out-of-scan** locations (entity-embedded paths with no `decisions/` segment, and the repository-based topology). The EPIC002 pair sits fully **in-scan** (matched by the two-clause `find … -path '*/decisions/*'`), so R-10's disclosure does not cover this gap. No other residual (R-1 through R-17, R-A/B/C, `subtraction-pass-notes.md` residual table) names this specific combination.

5. Confirmed M-11 (`ADR:546`) names these exact two files and schedules a frontmatter git-modification on them — but M-11's own text scopes itself to "optional schema-completeness" for YAML fields and explicitly says only "the 5-rule core validates these ADRs' filenames (L-1)," never asserting anything about L-4. M-11 does not close this gap; it is silent on it while confirming the files are real, cited, SSOT-referenced, and scheduled for git-modification.

6. Checked whether the general "(git-added/modified files; pre-adoption grandfathered)" table-header qualifier saves L-4 here. The one clarification that operationalizes "grandfathered on subsequent edit" (`ADR:693`, IN-001-iter8/012-003) explicitly scopes its resolution to **L-1/L-2 only** ("grandfathered-exempt from L-1/L-2, not as a newly-minted ID") — it says nothing about L-4, so no textual escape hatch protects L-4's behavior for this pair upon the M-11 edit.

No factual misreading found; the cited table rows, file paths, line numbers, and residual-register absence all check out against the current corpus.

---

## 002-002: Rule draft not self-contained — R-N citations dead in every CoWork/plugin distribution [CRITICAL]

**Verdict: VERIFIED**

**Reasoning:**

1. Confirmed the rule draft's References row (`adr-standards-rule-draft.md:234`) states verbatim: the parent ADR holds "the full residual register (R-1…R-17, R-A/R-B/R-C) — the `R-N` shorthand used above resolves there." This is the rule draft's own internal admission of the dependency.

2. Grep-counted genuine (non-false-positive) `R-N`/`R-[ABC]` residual-ID citations in the rule draft body: R-15 (`:46`), R-14 (`:94`), R-11/R-6/R-17 (`:151`), R-9 (`:175`), R-10/R-13 (`:177`), R-11/R-10/R-16 (`:179`), R-10 (`:181`), R-13 (`:200`), R-10/R-B/R-6/R-7 (`:206`). Distinct IDs actually cited in the body: R-1, R-6, R-7, R-9, R-10, R-11, R-13, R-14, R-15, R-16, R-17, R-A, R-B, R-C = **exactly 14 distinct IDs**, matching the finding's count precisely. None of these IDs is itself defined anywhere in the rule draft — the definitions live only in the parent ADR's Risks register.

3. Confirmed via `Grep` on `phase3-skeleton-generation-design.md:159`: `git rm -r projects/ tests/ skills/.graveyard .github # retains everything else BY CONSTRUCTION` — the VALIDATED (not merely recommended) strip set unconditionally removes `projects/`. The parent ADR currently lives at `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (confirmed via its own frontmatter, `promoted_to: null`, and Migration Plan row M-9 = `TBD-Task`, i.e., not yet executed) — so today, the ADR is unconditionally absent from every distributed build.

4. Confirmed `phase3-skeleton-generation-design.md:168-170` lists `docs/` as a RECOMMENDED (SHOULD, not required) additional strip. Confirmed `phase3-skeleton-generation-design.md:328` lists `.context/` as part of the explicitly retained surface (`FOR dir IN [.claude-plugin/, skills/, commands/, .claude/, .context/, hooks/, src/, schemas/]`), i.e. `.context/rules/adr-standards.md` (M-2's target, the artifact that actually ships) is NOT in any strip list.

5. Verified this is a materially distinct claim from residual 012-001 (`subtraction-pass-notes.md` Iteration-9 Remediation table, row 4): 012-001's disclosure is scoped to the **pre-M-2 timing gap** ("until M-2 executes … a plugin install carries no trace of this convention at all"). Finding 002-002 is about the **post-M-2 (and even post-M-9) permanent state**: once `.context/rules/adr-standards.md` exists and ships (it is never stripped), its 14 bare `R-N` citations still resolve only in the ADR, which — under the current, non-executed M-9 state — remains inside the unconditionally-stripped `projects/` tree, and even after M-9 would sit in `docs/design/`, an optionally-stripped location. No residual or disposition entry in `subtraction-pass-notes.md` (Residuals Disclosed table, or the iteration-8/9 dispositions) addresses self-containedness of the shipped rule file itself.

One minor imprecision noted (not sufficient to refute): the counter-argument's parenthetical "(and even post-M-9, `docs/` is itself a recommended … strip target … which would keep it absent either way)" slightly overstates certainty — the `docs/` strip is optional, so a distributor who skips it would retain the post-M-9 ADR. This does not undermine the core, independently-verified claim, since (a) M-9 has not executed, so today the ADR is unconditionally absent regardless, and (b) the core self-containedness gap (14 dead cross-file references in the one artifact guaranteed to ship) holds independently of the M-9/`docs/` timing question.

---

## Summary

| ID | Severity | Verdict |
|----|----------|---------|
| 002-001 | Critical | VERIFIED |
| 002-002 | Critical | VERIFIED |

Both Critical findings in `s-002-findings.md` were checked line-by-line against the current ADR and rule-draft text, cross-verified with `Glob`/`Grep` against the live filesystem (`projects/PROJ-001-oss-release/decisions/`, `phase3-skeleton-generation-design.md`), and checked against the full residual register (R-1…R-17, R-A/B/C) and every Critical disposition table in `subtraction-pass-notes.md`. Neither finding restates a previously-disclosed residual; both identify genuine, evidenced gaps in the current deliverables.
