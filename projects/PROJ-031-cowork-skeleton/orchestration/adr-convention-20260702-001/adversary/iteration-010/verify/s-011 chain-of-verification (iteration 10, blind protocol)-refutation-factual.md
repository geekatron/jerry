# Refutation Panel — Factual-Accuracy Lens

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-011-findings.md` (S-011 Chain-of-Verification, iteration 10, blind)
**Panel lens:** Factual accuracy — does the cited defect actually exist in the CURRENT deliverables at the cited locations?
**Reviewer:** adv-executor (blind refutation panel member, factual lens)
**Date:** 2026-07-06

---

## Method

Read the target report in full. Independently re-read the cited sections of both deliverables (`ADR-PROJ031-004-adr-identifier-convention.md`, `adr-standards-rule-draft.md`) at the cited line ranges, plus the residual register (R-1..R-17) and Critical/Major disposition tables in `subtraction-pass-notes.md`, to check whether the finding restates an already-disclosed residual or misreads current text. Did not read other refuters' or other panels' outputs (blind protocol).

---

## Finding-by-Finding Verdict

### CV-001-i010: Canonical Location Model omits the actual location pattern of the two grandfathered `EPIC002` dialect ADRs; L-4 (ID↔location) would misfire on them — CRITICAL

**Verdict: VERIFIED**

**Reasoning:**

1. **Table gap confirmed by direct re-read.** ADR Canonical Location Model (lines 384-393) has exactly two dialect-hosting rows: `Project (permitted dialect)` → home `projects/PROJ-NNN-*/decisions/`, ID form literally `ADR-PROJ{NNN}-NNN` (line 389, PROJ-prefix only, no `{EPIC|FEAT|STORY}` shown in that row's ID-form cell); and `Entity-embedded (permitted)` → home `projects/.../work/.../{ENTITY}/`, ID form `ADR-{PROJ|EPIC|FEAT|STORY}NNN-NNN` (line 390, but its canonical home is an entity `work/` folder, not a project `decisions/` folder). The rule-draft's mirror table (lines 77-88) is identical in this respect. Neither row's (location, ID-form) pair matches `ADR-EPIC002-001-strategy-selection.md`/`ADR-EPIC002-002-enforcement-architecture.md`, which are Glob/Read-confirmed to live at `projects/PROJ-001-oss-release/decisions/` (a project `decisions/` folder — row 1's location) while carrying an `EPIC{NNN}` prefix (row 2's ID grammar) — a combination the table does not enumerate. The document's own Context family table (line 103) independently corroborates the tension: it groups `ADR-EPIC002-001` with `ADR-STORY015-001` under "Entity-ID scoped... Origin (finer)," yet only STORY015 physically sits in an entity `work/` folder matching row 2's stated home; EPIC002-001/002 sit in a project `decisions/` folder instead.

2. **Grandfather-exemption scope is genuinely narrowed to L-1/L-2 in the operative text.** ADR line 693 ("How 'pre-adoption grandfathered' is operationalized...") states explicitly: "A git-modified file that is already on that baseline is treated as **grandfathered-exempt from L-1/L-2**, not as a newly-minted ID" — naming only L-1/L-2, not L-4 or L-7. The rule-draft's parallel clause (line 183) uses identical L-1/L-2-only language. This is narrower than the 5-rule table's generic header parenthetical "(git-added/modified files; pre-adoption grandfathered)" (ADR line 684 / rule-draft line 173), creating exactly the two-reading ambiguity the finding describes.

3. **M-11 is confirmed to schedule a git-modification of precisely these two files.** ADR line 546 (Migration Plan M-11): "Retrofit real YAML frontmatter (`id`/`scope`/`origin_project`) onto the 3 `docs/design/` framework ADRs and onto the framework-cited entity-dialect ADRs `ADR-EPIC002-001-strategy-selection`, `ADR-EPIC002-002-enforcement-architecture`... which today carry no `scope:` field at all." This is a git-modification (frontmatter addition, no rename) of the exact two files at issue, and the table header confirms lint rules run against "git-added/**modified** files," not only renamed/moved ones.

4. **Not a restated residual.** I checked all 17 named residuals (R-1 through R-17) plus the two "Post-ratification monitoring commitments" in the Risks section, and R-9/R-10/R-11/R-12/R-13/R-14/R-15/R-16/R-17 in `subtraction-pass-notes.md`. R-10 is the closest adjacent residual (out-of-scan location classes — entity-embedded no-`decisions/`-segment files like STORY015, and the repository-based topology) but it explicitly concerns files the scan **never reaches at all**; EPIC002-001/002 **are** within the scanned `projects/*/decisions/` path, so R-10's framing ("out-of-scan," "grandfathered in place but not lint-covered because unreached") does not describe this defect, which is instead an in-scan file whose location pattern is absent from the table. None of R-1..R-17, nor the Critical/Major disposition tables in `subtraction-pass-notes.md` (which list PM-001/PM-002/RT-001..007/FM-001..007/IN-013-005/CC-001/RT-101-104/DA-001/002/FM-001-i8..FM-003-i8/RT-001-i9/RT-002-i9/DA-002-i9/012-001/012-003), disclose this specific (location, ID-form) table incompleteness for the EPIC002 pair or its L-4 consequence. It is genuinely novel.

5. **Caveat (does not change the verdict).** A plausible alternate reading exists — that the generic table-header parenthetical ("pre-adoption grandfathered") could be read to exempt L-4 too, in which case there would be no future misfire, only a permanent, undocumented L-4 blind spot for these two files. The finder itself surfaces and reasons through both readings and shows **both** land on the same root defect: the Location Model table's completeness claim is false for these two files, and that incompleteness is undisclosed either way. My mandate here is factual accuracy (does the cited textual gap exist), not materiality or remediation cost — and on that narrow question, every citation checks out exactly at the stated lines, the quoted text is verbatim, and the underlying inconsistency between the general grandfather note and its L-1/L-2-scoped operationalization is real and unresolved elsewhere in either document.

All cited line anchors were independently re-verified and match: ADR L225-231 (D-4 reconciliation), ADR L384-393 (Location Model table), ADR L689 (L-4 spec), ADR L546 (M-11), rule-draft L77-88 (Location Model table), rule-draft L178 (L-4 spec).

---

## Summary

| Finding ID | Verdict |
|---|---|
| CV-001-i010 | VERIFIED |

**Verified: 1. Refuted: 0.**
