# Constitutional Compliance Report: EN-934 Dependency License Compatibility Audit Report (Revision 2)

**Strategy:** S-007 Constitutional AI Critique
**Deliverable:** `projects/PROJ-001-oss-release/orchestration/feat015-licmig-20260217-001/lic/phase-1-audit/audit-executor/audit-executor-dep-audit.md` (Revision 2)
**Criticality:** C4 (tournament mode per orchestration plan)
**Date:** 2026-02-17
**Reviewer:** adv-executor (S-007)
**Constitutional Context:** JERRY_CONSTITUTION.md v1.1, quality-enforcement.md v1.3.0, H-01 through H-24
**Execution ID:** 20260217T1500
**Iteration:** QG-1 Iteration 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Prior Finding Resolution](#prior-finding-resolution) | CC-001 through CC-004 resolution status |
| [Principle-by-Principle Review](#principle-by-principle-review) | Fresh evaluation of all applicable principles |
| [Fresh Findings](#fresh-findings) | New findings identified in Revision 2 |
| [Finding Details](#finding-details) | Expanded description for new findings |
| [Remediation Plan](#remediation-plan) | Prioritized P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Verdict](#verdict) | COMPLIANT / NON-COMPLIANT determination |

---

## Prior Finding Resolution

Each finding from QG-1 Iteration 1 (execution ID 20260217T1200) is assessed for resolution in Revision 2.

| Prior ID | Severity | Principle | Resolution |
|----------|----------|-----------|------------|
| CC-001-20260217T1200 | Major | P-022 No Deception | RESOLVED |
| CC-002-20260217T1200 | Minor | P-001 Truth and Accuracy | RESOLVED |
| CC-003-20260217T1200 | Minor | P-004 Explicit Provenance | RESOLVED |
| CC-004-20260217T1200 | Minor | P-021 Transparency of Limitations | RESOLVED |

### CC-001-20260217T1200: Dev Count Inconsistency — RESOLVED

**Prior finding:** Summary stated "8 direct dev" deps; Verdict stated "6 direct dev" deps — irreconcilable contradiction violating P-022 (No Deception).

**Revision 2 resolution:** Both sections now use identical scope language. Summary (line 32): "4 direct runtime, 6 direct dev (from `[dependency-groups].dev`), and 42 transitive." Verdict (line 226-227): "All 52 installed third-party packages (4 direct runtime, 6 direct dev, 42 transitive)." The previously ambiguous 4 optional-extras packages are now isolated in a dedicated "Declared but Uninstalled Dependencies" section, eliminating the 8 vs. 6 conflict entirely. Count arithmetic: 4 + 6 + 42 = 52 throughout. **RESOLVED.**

### CC-002-20260217T1200: MPL-2.0 Section 3.3 Citation Error — RESOLVED

**Prior finding:** MPL-2.0 Section 3.3 cited as "(GPL Compatibility)" — a heading that does not exist in the MPL-2.0 text.

**Revision 2 resolution:** License Notes section, certifi analysis (line 163-165) now reads: "MPL-2.0 Section 3.3 ('Distribution of a Larger Work') permits MPL-2.0-licensed files to be distributed as part of a 'Larger Work' under different license terms (including Apache 2.0)..." The erroneous "(GPL Compatibility)" parenthetical is removed. The GPL compatibility mechanism via absence of Exhibit B is now correctly stated (line 167). **RESOLVED.**

### CC-003-20260217T1200: Absent Deps "Known MIT" Without PyPI Citation — RESOLVED

**Prior finding:** `mypy`, `pytest-archon`, `pytest-bdd`, `pytest-cov` claimed "all known to be MIT-licensed" without source citations.

**Revision 2 resolution:** A new dedicated section "Declared but Uninstalled Dependencies" (lines 74-84) provides per-package verification from the PyPI JSON API with direct links and OSI Approved classifier evidence for all 4 packages. Verification method documented: "Verified independently via the PyPI JSON API (`https://pypi.org/pypi/{package}/json`)." **RESOLVED.**

### CC-004-20260217T1200: hatchling Scope Exclusion Unacknowledged — RESOLVED

**Prior finding:** Build-system dependency `hatchling` (declared in `[build-system].requires`) not in the scanned environment and not acknowledged as a scope exclusion.

**Revision 2 resolution:** The Methodology section (lines 248-249) now contains an explicit "Build-system dependencies (scope exclusion)" paragraph explaining: (a) build tools are not distributed with the package artifact, (b) they do not impose license obligations on the built artifact, (c) their license applies only to the build process itself. For completeness, hatchling's MIT license is verified via the GitHub source URL. The Incompatible Dependencies section (line 218) also references this explicitly. **RESOLVED.**

---

## Principle-by-Principle Review

### Step 1: Constitutional Context Index

**Deliverable type:** Document (audit report, license analysis).

**Loaded rule sets:**
- `JERRY_CONSTITUTION.md` v1.1 (P-001 through P-043)
- `quality-enforcement.md` v1.3.0 (H-01 through H-24, SSOT)
- `markdown-navigation-standards.md` (H-23, H-24)
- `python-environment.md` (H-05, H-06)

**Auto-escalation check:** No changes to `.context/rules/`, constitution, or ADRs in this deliverable. AE-001/AE-002 not triggered. Pre-existing C4 classification maintained per orchestration plan.

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
| H-13 Quality threshold >= 0.92 | HARD | YES | C4 deliverable must meet quality gate |
| H-23 Navigation table REQUIRED | HARD | YES | Document is Claude-consumed markdown over 30 lines |
| H-24 Anchor links REQUIRED | HARD | YES | Navigation table section names must use anchor links |

### Step 3: Principle-by-Principle Evaluation

#### P-001: Truth and Accuracy (SOFT)

**Compliance criteria:** All factual claims are accurate and verifiable.

**Evidence review:**

1. **Package counts:** Summary: 52 third-party packages (4+6+42=52). Verdict: 52 (4+6+42=52). Supplemental: 4 packages (pip, pip-licenses, prettytable, wcwidth) not in pip-licenses output but verified via importlib.metadata. Declared-but-uninstalled: 4 packages verified via PyPI. Arithmetic is internally consistent throughout.

2. **MPL-2.0 Section 3.3 citation (CC-002 prior finding):** Now correctly cited as "Distribution of a Larger Work." The Exhibit B absence mechanism for GPL compatibility is correctly explained. The OSI and FSF references are accurate. RESOLVED.

3. **CNRI-Python characterization:** Revision 2 (line 178): "CNRI-Python is the 'Corporation for National Research Initiatives' Python license, a historical permissive license originating from early Python interpreter releases. It is OSI-approved and carries attribution requirements but no copyleft provisions." This is accurate. The prior imprecision of "placed in the public domain" (noted informally in iteration 1 review) is corrected. Accurate.

4. **Transitive table count:** 42 rows enumerated. Cross-check: the 4 supplemental packages include pip (in transitive table, line 113), prettytable (line 118), wcwidth (line 134) — 3 of 4 in transitive. pip-licenses is in dev deps (line 64). 42 transitive entries are correctly listed.

5. **pip-licenses output count reconciliation:** Summary: pip-licenses returned "49 packages (48 third-party + jerry)." 48 third-party = 4 direct + 6 dev + 38 transitives not requiring supplemental. The 3 supplemental transitives (pip, prettytable, wcwidth) plus pip-licenses (dev) = 4 supplemental packages. 38+3=41? No — wait. The 49 packages from pip-licenses include jerry + 48 third-party. 48 = 4 direct + 6 dev (including pip-licenses? or not?). The Supplemental section states pip-licenses is NOT captured by pip-licenses. So: pip-licenses scan → 49 packages = jerry + 4 direct + X dev + Y transitive, where X + Y = 44. If pip-licenses is NOT in the scan, then dev from scan = 5 (pip-audit, pre-commit, pyright, pytest, ruff). 5+4=9 non-transitive. 44-9=35? That gives 35 transitive from scan + 3 supplemental = 38, not 42.

   Alternatively: pip-licenses IS in its own scan output (self-reporting). Then dev = 6 from scan. 6+4=10. 44-10=34 transitives from scan + 3 supplemental = 37, not 42.

   This count doesn't reconcile cleanly. However, the Supplemental section states the "4-package gap" between 49 (pip-licenses) and 53 (pip list), where 53 = 52 third-party + jerry. 49 packages from pip-licenses = 48 third-party + jerry. pip list = 53 = 52 third-party + jerry. So: 52 - 48 = 4 third-party packages not in pip-licenses output. Those are pip, pip-licenses, prettytable, wcwidth. This means: the 48 in pip-licenses output do NOT include those 4. The 42 transitives in the table include all 42 transitives: 39 from pip-licenses output + pip, prettytable, wcwidth (3 supplemental). 4 direct + 6 dev (with pip-licenses from supplemental) + 42 transitive = 52. This works if we accept that: the 48 from pip-licenses = 4 direct + 5 dev (excluding pip-licenses itself) + 39 transitive = 48. Then adding 4 supplemental (pip-licenses to dev, pip/prettytable/wcwidth to transitive) = 52. That gives 5+1=6 dev, 39+3=42 transitive. This reconciles correctly.

   The document states pip-licenses was NOT captured by its own scan (line 141: "pip-licenses not reporting certain packages that are part of its own dependency chain or the base environment"). This is the accepted explanation. The arithmetic is sound when traced through. No factual error — though the reconciliation path requires careful reading.

**Result: COMPLIANT** — all factual claims in Revision 2 are accurate. One minor clarity note addressed below as new finding CC-001-20260217T1500.

---

#### P-002: File Persistence (MEDIUM)

**Compliance criteria:** Audit persisted to correct filesystem path.

**Evidence:** Deliverable exists at `projects/PROJ-001-oss-release/orchestration/feat015-licmig-20260217-001/lic/phase-1-audit/audit-executor/audit-executor-dep-audit.md`. Revision 2 metadata correctly states "Revision: 2." Traceability section references the correct path.

**Result: COMPLIANT**

---

#### P-004: Explicit Provenance (SOFT)

**Compliance criteria:** All compatibility conclusions cite authoritative sources; verification methods documented.

**Evidence:**
- Absent deps: PyPI JSON API with direct links and classifier evidence. Verified.
- MPL-2.0: OSI and FSF citations (line 166). Verified.
- CNRI-Python: OSI approval link (line 178). Verified.
- hatchling: GitHub source URL citation (line 248). Verified.
- Primary tool: pip-licenses 5.5.1 version documented.
- Supplemental method: importlib.metadata field name (License-Expression, PEP 639 reference) documented.

**Result: COMPLIANT**

---

#### P-011: Evidence-Based Decisions (SOFT)

**Compliance criteria:** All license compatibility conclusions grounded in cited evidence.

**Evidence:**
- All 52 packages have license field and SPDX ID in tables.
- Edge-case licenses (MPL-2.0, CNRI-Python, OR expression) have dedicated License Notes subsections with reasoning.
- Standing constraints derive from documented license text analysis.
- Absent deps verified via PyPI JSON API with classifier evidence.

**Result: COMPLIANT**

---

#### P-021: Transparency of Limitations (SOFT)

**Compliance criteria:** Scope exclusions, tool gaps, and methodological boundaries acknowledged.

**Evidence:**
- pip-licenses output gap (4 packages): explicitly acknowledged in Supplemental Verification section.
- hatchling build-system exclusion: explicitly documented in Methodology with three-part rationale.
- Pre-commit hook deps: explicitly excluded in Methodology with rationale.
- Declared-but-uninstalled packages: dedicated section with re-audit trigger condition.
- jerry project package exclusion: explicitly noted in Supplemental Verification (line 151).

**Result: COMPLIANT**

---

#### P-022: No Deception (HARD)

**Compliance criteria:** Internal counts, scope statements, conclusions, and section cross-references are mutually consistent.

**Evidence:**
- Summary package count: 52 (4+6+42). Verdict package count: 52 (4+6+42). Consistent.
- Declared-but-uninstalled: consistently "4 packages" in Summary (line 36) and in dedicated section (line 74).
- Total scope: "52 installed third-party packages and all 4 declared-but-uninstalled packages" in Verdict (line 226). Consistent with scope description throughout.
- Summary and Verdict both list one standing constraint (certifi MPL-2.0). Consistent.
- No section contradicts another on license compatibility conclusions.

**Result: COMPLIANT** — the primary P-022 concern from iteration 1 (CC-001) is fully resolved.

---

#### H-05: UV Only (HARD)

**Compliance criteria:** All Python tooling references in the document use `uv run`.

**Evidence:** Methodology (line 239): "pip-licenses 5.5.1 via `uv run pip-licenses --format=json --with-urls`." Supplemental verification (line 147-148): importlib.metadata used — this is a Python standard library module, not a pip-based tool, so H-05 is not triggered by its mention. H-05 applies to execution, not documentation of standard library usage.

**Result: COMPLIANT**

---

#### H-23: Navigation Table REQUIRED (HARD)

**Compliance criteria:** Navigation table present, covers all major sections (## headings).

**Evidence:** Navigation table present at lines 12-26 with 12 entries. Major sections present: Summary, Direct Dependencies, Dev Dependencies, Declared but Uninstalled Dependencies, Transitive Dependencies, Supplemental Verification, License Notes, Standing Constraints, Incompatible Dependencies, Verdict, Methodology, Re-Audit Conditions, Traceability. All ## headings covered.

**Result: COMPLIANT**

---

#### H-24: Anchor Links REQUIRED (HARD)

**Compliance criteria:** All navigation table entries use anchor link syntax.

**Evidence:** All entries use `[Section Name](#anchor)` syntax. Spot check: `[Summary](#summary)`, `[Methodology](#methodology)`, `[Declared but Uninstalled Dependencies](#declared-but-uninstalled-dependencies)`. Lowercase and hyphenation consistent with H-24 anchor link syntax rules.

**Result: COMPLIANT**

---

## Fresh Findings

### New Findings in Revision 2

| ID | Severity | Principle | Finding | Section |
|----|----------|-----------|---------|---------|
| CC-001-20260217T1500 | Minor | P-004 Explicit Provenance | Supplemental-verified packages (pip, pip-licenses, prettytable, wcwidth) are integrated into main tables without inline annotation indicating their verification path differs from the pip-licenses primary scan. A legal auditor cannot distinguish which 42 transitive entries were verified by pip-licenses vs. importlib.metadata without cross-referencing the Supplemental Verification section. | Transitive Dependencies, Dev Dependencies |

---

## Finding Details

### CC-001-20260217T1500: Supplemental Packages Unlabeled in Main Tables [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Principle** | P-004 Explicit Provenance |
| **Section** | Transitive Dependencies table; Dev Dependencies table |
| **Strategy Step** | Step 3 — Principle-by-Principle Evaluation (P-004) |
| **Affected Dimension** | Traceability |

**Evidence:**

Transitive Dependencies table (lines 92-135) lists 42 packages, including pip (line 113), prettytable (line 118), and wcwidth (line 134). Dev Dependencies table (line 64) lists pip-licenses. None of these 4 entries are annotated to indicate they were verified via importlib.metadata rather than the primary pip-licenses scan.

The Supplemental Verification section (lines 140-152) correctly documents these 4 packages and their verification method, but only a reader who reads both sections can trace which table entries relied on supplemental verification.

**Analysis:**

P-004 (Explicit Provenance) requires that the source and rationale for decisions be documented. For an audit report, this includes the verification method for each package's license determination. The current document provides this information in aggregate (Supplemental Verification section) but not at the row level in the main tables. A legal reviewer performing a spot audit of a specific transitive dependency (e.g., `pip`) would not immediately know from the Transitive table that its license determination used importlib.metadata rather than the pip-licenses scan.

This is a presentation-layer gap, not a substantive coverage gap. All 4 packages are correctly verified and documented. The severity is Minor because the information is present in the document (Supplemental Verification section); it is simply not surfaced at the point of consumption (table row).

**Recommendation:**

Add a superscript or footnote marker to the 4 supplemental-verified entries in the main tables, with a note beneath each table pointing to the Supplemental Verification section. Example:

```markdown
| pip | 26.0 | MIT | MIT | Yes ¹ |

¹ License verified via importlib.metadata (License-Expression field, PEP 639). See [Supplemental Verification](#supplemental-verification).
```

Alternatively, add a column "Verification Method" to the Supplemental Verification table and cross-reference table entry rows. The Supplemental Verification section already exists and is comprehensive; inline notation in the main tables is the minimum change required.

---

## Remediation Plan

**P0 (Critical):** None.

**P1 (Major):** None.

**P2 (Minor):**
- **CC-001-20260217T1500:** Annotate 4 supplemental-verified rows (pip, pip-licenses, prettytable, wcwidth) in main tables with a footnote marker linking to the Supplemental Verification section. One-line change per row, low effort. Optional: add "Verification Method" column to main tables.

---

## Scoring Impact

| Dimension | Weight | Impact | Constitutional Finding |
|-----------|--------|--------|----------------------|
| Completeness | 0.20 | Positive | All 4 prior findings resolved. New Declared but Uninstalled section adds coverage. hatchling and pre-commit exclusions now explicitly documented. |
| Internal Consistency | 0.20 | Positive | CC-001 (Major) resolved — counts are now consistent throughout. No contradictions found in Revision 2. |
| Methodological Rigor | 0.20 | Neutral | H-05 compliant. Methodology section is comprehensive. No constitutional findings affect rigor in Revision 2. |
| Evidence Quality | 0.15 | Positive | CC-002 resolved (accurate MPL-2.0 citation). CC-003 resolved (PyPI citations added). Minor Negative: CC-001-20260217T1500 — supplemental verification path not visible at table row level. |
| Actionability | 0.15 | Neutral | No constitutional findings affect actionability in Revision 2. |
| Traceability | 0.10 | Minor Negative | CC-001-20260217T1500 (Minor): 4 supplemental-verified entries not flagged inline; auditor must cross-reference Supplemental section to determine verification method per package. |

**Constitutional Compliance Score (Revision 2):**
- Base: 1.00
- CC-001-20260217T1500 (Minor): -0.02
- **Score: 1.00 - 0.02 = 0.98**

**Threshold Determination:** PASS (>= 0.92 threshold; score 0.98 is well within PASS band)

**Comparison to Iteration 1:** Score improved from 0.89 (REVISE) to 0.98 (PASS). The single Major finding (CC-001) and three Minor findings from iteration 1 are all resolved. One new Minor finding (CC-001-20260217T1500) identified; it does not prevent PASS.

---

## Verdict

**COMPLIANT** — Constitutional compliance score: 0.98 (PASS band >= 0.92).

### Prior Finding Disposition

All four findings from QG-1 Iteration 1 S-007 review are RESOLVED in Revision 2:

- **CC-001 RESOLVED:** Dev count inconsistency eliminated. Summary and Verdict now consistently report 52 packages (4+6+42). Declared-but-uninstalled section isolates the previously-conflated 4 optional-extras packages.
- **CC-002 RESOLVED:** MPL-2.0 Section 3.3 correctly cited as "Distribution of a Larger Work." "(GPL Compatibility)" parenthetical removed.
- **CC-003 RESOLVED:** Absent deps now verified via PyPI JSON API with direct links and classifier evidence in dedicated section.
- **CC-004 RESOLVED:** hatchling build-system exclusion explicitly documented in Methodology with three-part rationale and MIT license verification.

### New Finding Disposition

One new Minor finding (CC-001-20260217T1500) identified: supplemental-verified packages (pip, pip-licenses, prettytable, wcwidth) are not annotated in the main dependency tables, requiring cross-reference to the Supplemental Verification section to determine per-package verification method. This is a presentation-layer gap that does not affect the correctness of the audit's conclusions. It does not block acceptance.

### Positive Constitutional Assessment

All HARD rules confirmed compliant in Revision 2:
- **P-022 (No Deception):** Fully compliant. No internal count contradictions.
- **H-05 (UV Only):** Fully compliant.
- **H-23 (Navigation table):** Fully compliant — all 13 major sections listed.
- **H-24 (Anchor links):** Fully compliant — all navigation entries use correct anchor syntax.

The core Apache 2.0 compatibility analysis remains legally sound. License notes for MPL-2.0, CNRI-Python, and the OR expression are accurate. The standing constraint on certifi (SC-001) is correctly identified and documented. No GPL, AGPL, SSPL, or LGPL packages missed. The audit methodology is reproducible via uv.lock.

**Recommendation:** ACCEPT. Apply P2 recommendation (CC-001-20260217T1500) as a non-blocking improvement in any future revision.

---

*S-007 Constitutional AI Critique — QG-1 Iteration 2*
*Executed by adv-executor agent — feat015-licmig-20260217-001 / QG-1 tournament*
*Template: .context/templates/adversarial/s-007-constitutional-ai.md v1.0.0*
*Prior execution: adv-executor-s007-result.md (20260217T1200)*
