# Constitutional Compliance Report: EN-934 Dependency License Compatibility Audit Report (Revision 3)

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-001-oss-release/orchestration/feat015-licmig-20260217-001/lic/phase-1-audit/audit-executor/audit-executor-dep-audit.md` (Revision 3)
**Criticality:** C2 (Standard) — per ORCHESTRATION.yaml workflow.criticality (task-level override from C4 tournament mode per orchestration plan)
**Date:** 2026-02-17
**Reviewer:** adv-executor (S-007)
**Constitutional Context:** JERRY_CONSTITUTION.md v1.1, quality-enforcement.md v1.3.0, H-01 through H-24
**Execution ID:** 20260217T1600
**Iteration:** QG-1 Iteration 3 (FINAL)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall constitutional compliance status |
| [Prior Finding Resolution](#prior-finding-resolution) | CC-001-20260217T1500 resolution status |
| [Principle-by-Principle Review](#principle-by-principle-review) | Full re-evaluation for Revision 3 |
| [Fresh Findings](#fresh-findings) | Any new compliance issues introduced by Revision 3 |
| [Finding Details](#finding-details) | Expanded descriptions for all active findings |
| [Remediation Plan](#remediation-plan) | Prioritized P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Verdict](#verdict) | COMPLIANT / NON-COMPLIANT determination |

---

## Summary

Revision 3 of the EN-934 Dependency License Compatibility Audit Report is constitutionally **COMPLIANT**. All four prior iteration 1 findings remain resolved. The single iteration 2 Minor finding (CC-001-20260217T1500 — supplemental packages unlabeled in main tables) was **not addressed** in Revision 3 (the revision targeted S-014 and S-002 findings only), but as a Minor/P2 recommendation it does not block acceptance. No new constitutional violations were introduced by Revision 3. All HARD rules (P-022, H-05, H-23, H-24) remain fully compliant. Constitutional compliance score: **0.98 (PASS)**.

Findings summary: 0 Critical, 0 Major, 1 Minor (carried from iteration 2, unresolved).

Recommendation: **ACCEPT.** The P2 minor recommendation (CC-001-20260217T1500) may be applied in a future non-blocking pass.

---

## Prior Finding Resolution

The single open finding from QG-1 Iteration 2 (execution ID 20260217T1500) is assessed for resolution in Revision 3.

| Prior ID | Severity | Principle | Resolution |
|----------|----------|-----------|------------|
| CC-001-20260217T1500 | Minor | P-004 Explicit Provenance | NOT RESOLVED (carried forward) |

### CC-001-20260217T1500: Supplemental Packages Unlabeled in Main Tables — NOT RESOLVED

**Prior finding:** The 4 supplemental-verified packages (pip, pip-licenses, prettytable, wcwidth) are listed in the main Transitive Dependencies and Dev Dependencies tables without any inline annotation indicating their license determination method differs from the primary pip-licenses scan. A legal auditor cannot distinguish these rows from pip-licenses-verified rows without cross-referencing the Supplemental Verification section.

**Revision 3 assessment:** The revision metadata (line 5) explicitly states its scope: "addressing S-014 evidence gaps, S-002 DA-011/DA-012/DA-013/DA-014/DA-015/DA-016/DA-017." The S-007 Minor recommendation was not in scope for this revision cycle.

**Evidence:** Transitive Dependencies table (lines 97-141 in Revision 3): pip (line 119), prettytable (line 124), wcwidth (line 140) — no footnote markers. Dev Dependencies table (lines 63-72): pip-licenses (line 66) — no footnote marker. The Supplemental Verification section (lines 144-160) remains accurate and comprehensive but the main tables remain unannotated.

**Impact:** Severity remains Minor. The information is present and correct in the Supplemental Verification section. This is a presentation-layer traceability gap, not a substantive accuracy gap. No revision to constitutional compliance score warranted beyond the -0.02 already applied.

**Disposition:** Carried forward at P2 (Minor). Does not block PASS verdict.

---

## Principle-by-Principle Review

### Step 1: Constitutional Context Index

**Deliverable type:** Document (audit report, license analysis). Revision 3 addresses S-014 evidence gaps and S-002 devil's advocate findings.

**Loaded rule sets:**
- `JERRY_CONSTITUTION.md` v1.1 (P-001 through P-043)
- `quality-enforcement.md` v1.3.0 (H-01 through H-24, SSOT)
- `markdown-navigation-standards.md` (H-23, H-24)
- `python-environment.md` (H-05, H-06)

**Auto-escalation check:** Revision 3 does not touch `.context/rules/`, the constitution, or any ADR. AE-001, AE-002, AE-003, AE-004, AE-005 not triggered. C2 classification per orchestration plan maintained.

### Step 2: Applicable Principles Checklist

| Principle | Tier | Applicable? | Rationale |
|-----------|------|-------------|-----------|
| P-001 Truth and Accuracy | SOFT | YES | Audit makes factual claims about license text, section citations, and legal compatibility |
| P-002 File Persistence | MEDIUM | YES | Audit must be persisted to filesystem |
| P-003 No Recursive Subagents | HARD | NO | Agent spawning not relevant to document content |
| P-004 Explicit Provenance | SOFT | YES | License compatibility claims require source citations; verification methods must be documented |
| P-011 Evidence-Based Decisions | SOFT | YES | All license compatibility conclusions must be grounded in cited evidence |
| P-021 Transparency of Limitations | SOFT | YES | Scope exclusions, tool gaps, and methodological boundaries should be acknowledged |
| P-022 No Deception | HARD | YES | Internal counts, scope statements, and conclusions must be internally consistent |
| H-05 UV Only | HARD | YES | Audit documents tooling methodology involving uv |
| H-06 UV for deps | HARD | NO | No dependency installation in a documentation deliverable |
| H-13 Quality threshold >= 0.92 | HARD | YES | C2+ deliverable must meet quality gate |
| H-23 Navigation table REQUIRED | HARD | YES | Document is Claude-consumed markdown over 30 lines |
| H-24 Anchor links REQUIRED | HARD | YES | Navigation table section names must use anchor links |

No new principles are triggered by Revision 3 content changes relative to Revision 2. The principle checklist is unchanged.

### Step 3: Principle-by-Principle Evaluation

#### P-001: Truth and Accuracy (SOFT)

**Compliance criteria:** All factual claims are accurate and verifiable.

**Evidence review for Revision 3 content:**

1. **Package counts (no change from Rev 2):** Summary (line 32): "52 third-party packages: 4 direct runtime, 6 direct dev (from `[dependency-groups].dev`), and 42 transitive." Verdict (lines 234-236): "52 installed third-party packages (4 direct runtime, 6 direct dev, 42 transitive)." Arithmetic: 4+6+42=52. Consistent throughout.

2. **Declared-but-uninstalled section (line 76-89):** PyPI version pinning is accurately documented. "specific version resolved by `uv.lock`" language is present and correct. The scope limitation note ("top-level licenses only; transitive dependencies of these 4 optional packages are not audited") is correctly stated and consistent with Re-Audit Conditions Item 4.

3. **Revision 3 additions — Methodology section (lines 246-260):** The revision extended the Methodology section based on S-002 and S-014 findings. Key new content:
   - `uv.lock` commit reference ("last modified at git commit `1c108b4`, audit performed at commit `1fea04c`") — plausible, not independently verifiable from document context alone, no deception risk
   - "pip list count of 53 packages (52 third-party + jerry) matches the uv.lock resolved set" — factually consistent with Supplemental Verification's 4-package gap reconciliation
   - Pre-commit hook dependency exclusion rationale (line 259): "Pre-commit fetches and installs isolated environments..." — accurately describes pre-commit behavior
   - REUSE Specification citation (line 258): cited as a known standard for build tool treatment — accurate and appropriate

4. **jsonschema extras note (line 55):** "The `[test]` extra does not exist in jsonschema's current metadata (available extras: `format`, `format-nongpl`)." This is an accurately documented finding with practical impact. The recommendation ("change to `jsonschema>=4.26.0`") is actionable and correct.

5. **Incompatible Dependencies section (line 218-228):** "zero LGPL packages are present in the dependency tree" — consistent with full table review. The note that "LGPL is listed as 'Conditionally Compatible' in Methodology but was not exercised" is an honest transparency statement, not a gap.

6. **Revision history in Traceability (line 292):** "Rev 2: Addressed all iter 1 findings (scored 0.916 REVISE). Rev 3: Targeted evidence fixes (DA-011 through DA-017, S-014 gaps)." — Accurate. The S-014 iteration 2 score of 0.916 is consistent with the adv-scorer-s014-result-iter2.md artifact (score REVISE band at 0.916, which rounds into the 0.85-0.91 REVISE band). Consistent with prior review records.

**Result: COMPLIANT** — All factual claims in Revision 3 are accurate and internally consistent.

---

#### P-002: File Persistence (MEDIUM)

**Compliance criteria:** Audit persisted to correct filesystem path.

**Evidence:** Deliverable confirmed at `projects/PROJ-001-oss-release/orchestration/feat015-licmig-20260217-001/lic/phase-1-audit/audit-executor/audit-executor-dep-audit.md`. Revision metadata header (line 5) correctly states "Revision: 3." Traceability section (line 292) documents revision history correctly.

**Result: COMPLIANT**

---

#### P-004: Explicit Provenance (SOFT)

**Compliance criteria:** All compatibility conclusions cite authoritative sources; verification methods documented.

**Evidence:**
- Absent deps: PyPI JSON API with direct version-specific links and classifier evidence — present and enhanced in Revision 3 (line 78: "at the **specific version resolved by `uv.lock`**").
- MPL-2.0: OSI and FSF citations (lines 166-168). Exhibit B absence verified via GitHub source URL (line 167). Present.
- CNRI-Python: OSI approval link (line 180). Present.
- hatchling: GitHub source URL citation (line 258). Present.
- Primary tool: pip-licenses 5.5.1 version documented (line 248).
- Supplemental method: importlib.metadata License-Expression field, PEP 639 reference documented (lines 146-155).
- REUSE Specification citation for build tool scope exclusion (line 258) — new in Revision 3, strengthens provenance.

**Carried finding CC-001-20260217T1500:** 4 supplemental-verified rows in main tables lack inline footnote markers. Provenance is present at document level but not at table-row level. Minor gap, unchanged from iteration 2. Not a new violation.

**Result: COMPLIANT (with carried Minor finding CC-001-20260217T1500)**

---

#### P-011: Evidence-Based Decisions (SOFT)

**Compliance criteria:** All license compatibility conclusions grounded in cited evidence.

**Evidence:**
- All 52 packages have license field and SPDX ID in tables.
- Edge-case licenses have dedicated License Notes subsections with multi-source reasoning.
- Declared-but-uninstalled packages verified via PyPI JSON API at uv.lock-pinned versions.
- Supplemental verification uses PEP 639 authoritative field (License-Expression) with documented rationale.
- hatchling exclusion: three-part rationale cited (distribution model, REUSE Specification, isolation).
- Pre-commit hook exclusion: two-part rationale cited (developer tooling, not distributed with artifact).

**Result: COMPLIANT** — Evidence quality is strong and improved from prior iterations.

---

#### P-021: Transparency of Limitations (SOFT)

**Compliance criteria:** Scope exclusions, tool gaps, and methodological boundaries acknowledged.

**Evidence:**
- pip-licenses output gap (4 packages): explicitly acknowledged in Supplemental Verification.
- hatchling build-system exclusion: explicitly documented in Methodology with three-part rationale.
- Pre-commit hook deps: explicitly excluded in Methodology with rationale (line 259) — present in Revision 3.
- Declared-but-uninstalled scope limitation: explicitly noted ("top-level licenses only") in both Verdict and Declared but Uninstalled Dependencies sections.
- jerry project package exclusion: explicitly noted in Supplemental Verification (line 159).
- uv.lock environment reproducibility statement: documents what constitutes the audited environment and its git state (line 257).

**Result: COMPLIANT**

---

#### P-022: No Deception (HARD)

**Compliance criteria:** Internal counts, scope statements, conclusions, and section cross-references are mutually consistent.

**Evidence:**
- Package counts: Summary 52 (4+6+42), Verdict 52 (4+6+42), Supplemental 53 (52+jerry). All consistent.
- Declared-but-uninstalled: "4 packages" in Summary (line 36) and dedicated section header (line 76). Consistent.
- Total scope: "52 installed third-party packages and all 4 declared-but-uninstalled packages" in Verdict (line 236). Consistent with description throughout.
- Standing constraints: one (certifi SC-001) referenced in both Summary (line 40) and Verdict (line 240). Consistent.
- Incompatible Dependencies: "None found" (line 220) — consistent with all table entries showing "Yes" for Compatible.
- Revision history (Traceability, line 292): accurately records revision context without inflating claims.
- No section contradicts another on license compatibility conclusions.
- Verdict's "PASS (installed packages)" and "PASS (declared-but-uninstalled, top-level only)" distinction is accurate and transparent — the partial scope is explicitly labeled.

**Result: COMPLIANT** — P-022 remains fully resolved from iteration 1.

---

#### H-05: UV Only (HARD)

**Compliance criteria:** All Python tooling references in the document use `uv run`.

**Evidence:** Methodology (line 248): "pip-licenses 5.5.1 via `uv run pip-licenses --format=json --with-urls`." importlib.metadata usage (line 146-155) is a Python standard library module, not a pip-based tool — H-05 not triggered by documentation of standard library calls. No references to bare `python`, `pip`, or `pip3` commands.

**Result: COMPLIANT**

---

#### H-23: Navigation Table REQUIRED (HARD)

**Compliance criteria:** Navigation table present and covers all major sections (## headings).

**Evidence:** Navigation table present at lines 10-27 with 13 entries covering all ## sections: Summary, Direct Dependencies, Dev Dependencies, Declared but Uninstalled Dependencies, Transitive Dependencies, Supplemental Verification, License Notes, Standing Constraints, Incompatible Dependencies, Verdict, Methodology, Re-Audit Conditions, Traceability. Spot-verified: table has 13 rows matching 13 ## headings in the document body.

**Result: COMPLIANT**

---

#### H-24: Anchor Links REQUIRED (HARD)

**Compliance criteria:** All navigation table entries use anchor link syntax.

**Evidence:** All entries use `[Section Name](#anchor)` syntax. Spot check:
- `[Summary](#summary)` — correct
- `[Declared but Uninstalled Dependencies](#declared-but-uninstalled-dependencies)` — correct (spaces to hyphens, lowercase)
- `[Re-Audit Conditions](#re-audit-conditions)` — correct
- `[Traceability](#traceability)` — correct

All anchor links follow lowercase and hyphenation convention per H-24.

**Result: COMPLIANT**

---

#### H-13: Quality Threshold (HARD — process compliance)

**Compliance criteria:** The document is a C2+ deliverable undergoing the quality process. This principle evaluates whether the deliverable is participating in the quality gate process correctly, not the score outcome (which S-014 determines).

**Evidence:** QG-1 is the designated quality gate for Phase 1 of feat015-licmig-20260217-001. Three iterations have been completed (iterations 1, 2, and now 3), satisfying H-14's minimum 3-iteration requirement. The deliverable is in its third revision — correctly participating in the creator-critic-revision cycle.

**Result: COMPLIANT** — Process compliance satisfied.

---

### Step 3 Summary

| Principle | Tier | Result | Finding |
|-----------|------|--------|---------|
| P-001 Truth and Accuracy | SOFT | COMPLIANT | — |
| P-002 File Persistence | MEDIUM | COMPLIANT | — |
| P-004 Explicit Provenance | SOFT | COMPLIANT (with carried Minor) | CC-001-20260217T1500 (carried) |
| P-011 Evidence-Based Decisions | SOFT | COMPLIANT | — |
| P-021 Transparency of Limitations | SOFT | COMPLIANT | — |
| P-022 No Deception | HARD | COMPLIANT | — |
| H-05 UV Only | HARD | COMPLIANT | — |
| H-23 Navigation Table | HARD | COMPLIANT | — |
| H-24 Anchor Links | HARD | COMPLIANT | — |
| H-13 Process Compliance | HARD | COMPLIANT | — |

---

## Fresh Findings

### New Findings in Revision 3

A targeted review of Revision 3's new and modified content (the S-014/S-002 evidence additions: Declared but Uninstalled section enhancements, extended Methodology section, Supplemental Verification section updates, Traceability revision history) was conducted to identify any new constitutional issues introduced by this revision.

**No new constitutional violations were identified in Revision 3.**

The following items were inspected and found compliant:

1. **Revision header scope description** (line 5): Accurately describes what was addressed ("S-014 evidence gaps, S-002 DA-011 through DA-017"). No deception about revision scope.
2. **uv.lock commit references** (line 257): Git state documentation (`1c108b4`, `1fea04c`) is a scope declaration, not a verifiable claim requiring cross-system validation. Does not introduce P-022 risk.
3. **REUSE Specification citation** (line 258): Accurately attributed as an external standard. Does not misrepresent the specification's position on build tools.
4. **Pre-commit hook exclusion rationale** (line 259): Three characteristics stated (developer tooling, not distributed, no license obligations) are accurate descriptions of pre-commit's role.
5. **"pip list count of 53 packages" statement** (line 257): Consistent with 52 third-party + jerry = 53. No contradiction.
6. **Verdict dual-PASS structure** (lines 234-242): The "PASS (installed packages)" / "PASS (declared-but-uninstalled, top-level only)" format cleanly separates scope — no deception, transparent limitation acknowledgment.
7. **Footnote of final line** (line 299): "Revision 3 — addressing QG-1 iteration 2 findings (S-014: 0.916, S-002: ~0.892)" — accurately reflects the S-014 and S-002 scores from iteration 2 that drove this revision. No inflation of prior scores.

| Finding Type | Count |
|---|---|
| New Critical findings | 0 |
| New Major findings | 0 |
| New Minor findings | 0 |

---

## Finding Details

### Carried Finding: CC-001-20260217T1500 [MINOR — UNRESOLVED FROM ITERATION 2]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Principle** | P-004 Explicit Provenance |
| **Status** | Not addressed in Revision 3 |
| **Section** | Transitive Dependencies table; Dev Dependencies table |
| **Affected Dimension** | Traceability |

**Evidence:**

Transitive Dependencies table (lines 97-141): pip (line 119), prettytable (line 124), wcwidth (line 140) — no footnote markers distinguishing them from pip-licenses-verified entries. Dev Dependencies table (lines 63-72): pip-licenses (line 66) — no footnote marker.

The Supplemental Verification section (lines 144-160) is comprehensive and accurate, documenting the importlib.metadata verification method for all 4 packages. However, the presentation-layer gap identified in iteration 2 remains: a reader auditing a single table row cannot determine the verification method without reading the Supplemental Verification section.

**Status determination:** Revision 3 explicitly targeted S-014/S-002 findings. The S-007 P2 recommendation was correctly deferred as non-blocking. No new evidence changes the Minor severity assessment.

**Recommendation (unchanged from iteration 2):**
Add a superscript or footnote marker to the 4 supplemental-verified entries in the main tables:

```markdown
| pip | 26.0 | MIT | MIT | Yes ¹ |

¹ License verified via importlib.metadata (License-Expression field, PEP 639).
  See [Supplemental Verification](#supplemental-verification).
```

This remains a P2 (Minor) recommendation. It does not block acceptance.

---

## Remediation Plan

**P0 (Critical):** None.

**P1 (Major):** None.

**P2 (Minor):**
- **CC-001-20260217T1500 (carried, unresolved):** Annotate 4 supplemental-verified rows (pip in Transitive, prettytable in Transitive, wcwidth in Transitive, pip-licenses in Dev) with a footnote marker linking to the Supplemental Verification section. One-line change per row. Apply in any future non-blocking revision.

---

## Scoring Impact

| Dimension | Weight | Impact | Constitutional Finding |
|-----------|--------|--------|----------------------|
| Completeness | 0.20 | Positive | All 4 iteration-1 findings remain resolved. Revision 3 strengthens scope documentation. No gaps in coverage found. |
| Internal Consistency | 0.20 | Positive | P-022 fully compliant. All counts, scope statements, and verdicts internally consistent throughout Revision 3. No contradictions introduced. |
| Methodological Rigor | 0.20 | Positive | H-05 compliant. Methodology section is comprehensive with explicit scope exclusion rationale (build system, pre-commit hooks). REUSE Specification citation strengthens rigor. |
| Evidence Quality | 0.15 | Minor Negative | CC-001-20260217T1500 (Minor, unresolved): 4 supplemental-verified rows not annotated in main tables. Substantively correct; presentation-layer gap only. |
| Actionability | 0.15 | Neutral | No constitutional findings affect actionability. Standing constraint (SC-001) and Re-Audit Conditions remain correctly documented and actionable. |
| Traceability | 0.10 | Minor Negative | CC-001-20260217T1500 (Minor, unresolved): per-row verification method not immediately traceable from table entries; requires cross-reference to Supplemental Verification. |

**Constitutional Compliance Score (Revision 3):**
- Base: 1.00
- CC-001-20260217T1500 (Minor, carried): -0.02
- New findings: 0
- **Score: 1.00 - 0.02 = 0.98**

**Threshold Determination:** PASS (>= 0.92 threshold; score 0.98 is well within PASS band)

**Score comparison across iterations:**
| Iteration | Rev | Score | Band | Finding Summary |
|-----------|-----|-------|------|-----------------|
| 1 | Rev 1 | 0.89 | REVISE | 1 Major + 3 Minor |
| 2 | Rev 2 | 0.98 | PASS | 1 Minor (new) |
| 3 | Rev 3 | 0.98 | PASS | 1 Minor (carried, unresolved) |

Score is stable at 0.98. No regression from Revision 3 changes. All HARD rules remain fully compliant.

---

## Verdict

**COMPLIANT** — Constitutional compliance score: 0.98 (PASS band >= 0.92).

### Prior Finding Disposition

| Finding ID | Iteration | Severity | Resolution |
|------------|-----------|----------|------------|
| CC-001-20260217T1200 | 1 | Major | RESOLVED in Rev 2. Remains resolved in Rev 3. |
| CC-002-20260217T1200 | 1 | Minor | RESOLVED in Rev 2. Remains resolved in Rev 3. |
| CC-003-20260217T1200 | 1 | Minor | RESOLVED in Rev 2. Remains resolved in Rev 3. |
| CC-004-20260217T1200 | 1 | Minor | RESOLVED in Rev 2. Remains resolved in Rev 3. |
| CC-001-20260217T1500 | 2 | Minor | NOT RESOLVED in Rev 3 (out of scope for this revision). P2 only — does not block acceptance. |

### HARD Rule Compliance (Final Check)

All HARD rules applicable to this deliverable are fully compliant in Revision 3:

- **P-022 (No Deception):** Fully compliant. All counts, scope statements, and conclusions are internally consistent throughout.
- **H-05 (UV Only):** Fully compliant. All tooling references use `uv run`.
- **H-23 (Navigation table):** Fully compliant. 13-entry navigation table covers all ## headings.
- **H-24 (Anchor links):** Fully compliant. All navigation entries use correct lowercase hyphenated anchor syntax.
- **H-13 (Quality process):** Fully compliant. Three-iteration quality gate cycle completed per H-14.

### Constitutional Assessment

The EN-934 Dependency License Compatibility Audit Report (Revision 3) is constitutionally sound. The core Apache 2.0 compatibility analysis is legally accurate. License notes for MPL-2.0, CNRI-Python, and the OR expression remain correct. The standing constraint on certifi (SC-001) is properly identified, documented, and actionable. Re-Audit Conditions provide forward-looking governance. The audit methodology is reproducible via `uv.lock`. No GPL, AGPL, SSPL, or LGPL packages are present in any category.

Revision 3 improvements (Methodology expansion, pre-commit hook exclusion documentation, REUSE Specification citation, uv.lock commit state documentation) do not introduce any constitutional issues and positively reinforce P-021 (Transparency of Limitations) and P-011 (Evidence-Based Decisions).

The single carried Minor finding (CC-001-20260217T1500) is a non-blocking presentation-layer traceability gap. Its persistence across Revision 3 is expected — it was explicitly a P2 recommendation not targeted by this revision.

**Recommendation: ACCEPT.** The deliverable meets the constitutional gate for QG-1 Iteration 3. Apply P2 recommendation (CC-001-20260217T1500) in any future revision as a non-blocking improvement.

---

*S-007 Constitutional AI Critique — QG-1 Iteration 3 (FINAL)*
*Executed by adv-executor agent — feat015-licmig-20260217-001 / QG-1 tournament*
*Template: .context/templates/adversarial/s-007-constitutional-ai.md v1.0.0*
*Prior executions: adv-executor-s007-result-iter1.md (20260217T1200), adv-executor-s007-result-iter2.md (20260217T1500)*
