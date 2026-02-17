# QG-1 Score Report: S-014 LLM-as-Judge

> **Gate:** QG-1 (Phase 1 — Dependency Audit)
> **Deliverable:** EN-934 Audit Report
> **Scorer:** adv-scorer
> **Strategy:** S-014 LLM-as-Judge
> **Date:** 2026-02-17

## Document Sections

| Section | Purpose |
|---------|---------|
| [Scoring Context](#scoring-context) | Deliverable metadata and criticality |
| [L0 Executive Summary](#l0-executive-summary) | Verdict and top finding at a glance |
| [Dimension Scores](#dimension-scores) | Weighted table with severity |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Per-dimension evidence, gaps, and improvement paths |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered actionable fixes |
| [Scoring Impact Analysis](#scoring-impact-analysis) | Contribution table and verdict rationale |
| [Leniency Bias Check](#leniency-bias-check) | H-15 self-review checklist |

---

## Scoring Context

- **Deliverable:** `projects/PROJ-001-oss-release/orchestration/feat015-licmig-20260217-001/lic/phase-1-audit/audit-executor/audit-executor-dep-audit.md`
- **Deliverable Type:** Analysis (Dependency License Audit Report)
- **Criticality Level:** C3 (Significant — OSS public release gate; >1 day to reverse if wrong license accepted)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored By:** adv-scorer
- **Scored:** 2026-02-17
- **Iteration:** 1 (first score, initial draft)
- **Prior Score:** N/A

---

## L0 Executive Summary

**Score:** 0.83/1.00 | **Verdict:** REJECTED | **Weakest Dimension:** Internal Consistency (0.78)

**One-line assessment:** The audit provides solid coverage and clear verdicts but is undermined by a factual count inconsistency between Summary and Verdict sections, unverified claims for absent packages, and unlinked authority assertions in the compatibility analysis — all of which must be resolved before this audit can serve as a reliable OSS release gate artifact.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Severity | Evidence Summary |
|-----------|--------|-------|----------|----------|-----------------|
| Completeness | 0.20 | 0.82 | 0.164 | Major | Count inconsistency (8 dev/41 transitive in Summary vs 6 dev/43 transitive in Verdict); 4 absent packages asserted MIT without verification; LGPL absence not explicitly stated |
| Internal Consistency | 0.20 | 0.78 | 0.156 | Major | Direct factual contradiction: Summary says "8 direct dev/test, 41 transitive"; Verdict says "6 direct dev, 43 transitive"; table has 6 rows; MPL-2.0 classified "Conditionally Compatible" in methodology but rendered as unconditional "Yes" in table without reconciliation |
| Methodological Rigor | 0.20 | 0.83 | 0.166 | Major | Classification taxonomy and tool invocation well-documented; however: supplemental `importlib.metadata` check is asserted without evidence; absent packages dismissed as "known MIT" without lookup; `packaging` dual SPDX expression (`Apache-2.0 OR BSD-2-Clause`) receives no License Notes analysis |
| Evidence Quality | 0.15 | 0.80 | 0.120 | Major | pip-licenses tool and version cited; pyproject.toml path documented; however: no raw output artifact attached; MPL-2.0 and CNRI-Python compatibility conclusions cite OSI/FSF positions without URLs or document references; section numbers cited (MPL-2.0 §1.6, §3.3) without link to license text |
| Actionability | 0.15 | 0.88 | 0.132 | Minor | Verdict is clear and unambiguous (PASS for the underlying question); "No action required" stated explicitly for certifi and regex; gate decision is immediately usable; minor gap: no re-audit trigger guidance and no remediation template for future incompatible findings |
| Traceability | 0.10 | 0.87 | 0.087 | Minor | Workflow ID (feat015-licmig-20260217-001), Enabler (EN-934), agent, date, and pyproject.toml path are present; gap: no link to QG-1 gate specification, no reference to EN-934 enabler requirements, no WORKTRACKER item reference |
| **TOTAL** | **1.00** | | **0.825** | | |

---

## Detailed Dimension Analysis

### Completeness (0.82/1.00) — Major

**Evidence:**

The audit covers three explicit categories: Direct Dependencies (4 packages), Dev Dependencies (6 packages), and Transitive Dependencies (41 packages). A navigation table is present. All 53 installed packages are nominally accounted for. Edge-case licenses (MPL-2.0, CNRI-Python compound) receive dedicated License Notes. The Incompatible Dependencies section explicitly states none found.

**Gaps:**

1. **Count inconsistency creates an unresolved ambiguity about coverage scope.** The Summary states "4 direct runtime, 8 direct dev/test, and 41 transitive" (total: 53). The Verdict states "4 direct runtime, 6 direct dev, 43 transitive" (total: 53). The Dev Dependencies table contains 6 rows. The difference (8 vs 6) is unexplained — it is unclear whether 2 dev packages are missing from the table or whether the Summary miscounted. This is not a minor rounding issue; it directly undermines confidence in whether the audit is complete.

2. **Absent declared packages handled by assertion, not verification.** Four packages (`mypy`, `pytest-archon`, `pytest-bdd`, `pytest-cov`) are noted as "declared in pyproject.toml but not present in the current virtual environment" with the claim that "They are all known to be MIT-licensed." No PyPI lookup, SPDX identifier, or citation is provided to substantiate this. If any of these packages carries a non-MIT component (e.g., a vendored dependency or plugin), the claim would be incorrect.

3. **LGPL absence not explicitly declared.** The methodology lists LGPL as "Conditionally Compatible (used as library, unmodified)" — a non-trivial classification. The Incompatible Dependencies section says "No packages carrying GPL, AGPL, SSPL, EUPL, CC-BY-SA, or other non-permissive copyleft licenses were identified" but does not explicitly state whether any LGPL packages were found and determined compatible, or whether zero LGPL packages are present. A reader cannot distinguish between "LGPL found and cleared" and "LGPL not present."

4. **`packaging` dual SPDX expression (`Apache-2.0 OR BSD-2-Clause`) receives no dedicated analysis** despite being a disjunctive compound expression (distinct from `AND`). The `OR` operator means either license applies, which is permissive-compatible, but deserves a one-sentence note comparable to what `regex` receives.

**Improvement Path:**

- Reconcile the dev package count: either add the 2 missing packages to the table or correct the Summary count with an explanation.
- Look up `mypy`, `pytest-archon`, `pytest-bdd`, `pytest-cov` on PyPI and record their SPDX identifiers in a sub-table with a note "not installed, declared in pyproject.toml."
- Add a sentence to the Incompatible Dependencies section explicitly stating whether any LGPL packages were present.
- Add a brief note to License Notes for `packaging` explaining the `OR` expression.

---

### Internal Consistency (0.78/1.00) — Major

**Evidence:**

Package verdicts within individual rows are consistent (same license in License column and SPDX ID column, matching Compatible verdict). The MPL-2.0 analysis is internally self-consistent in the License Notes section. The CNRI-Python analysis is internally self-consistent.

**Gaps:**

1. **Direct factual contradiction between Summary and Verdict on package counts.** The Summary (line 26) reads: "4 direct runtime, 8 direct dev/test, and 41 transitive." The Verdict (line 154) reads: "4 direct runtime, 6 direct dev, 43 transitive." Both sections add to 53. This is a directly contradictory claim within the same document. For an audit report, numerical precision is a trust anchor — a count discrepancy between two terminal sections (Summary and Verdict) is a material internal consistency defect.

2. **MPL-2.0 classification is inconsistent between Methodology and the package table.** The Methodology section classifies MPL-2.0 as "Conditionally Compatible (used as library, unmodified)" — acknowledging that the compatibility is conditional on use pattern. The Transitive Dependencies table lists certifi as "Yes" (unconditionally). The License Notes section correctly explains the condition, but the table entry does not acknowledge conditionality (e.g., "Yes (conditional — unmodified use only)") and the Methodology classification is never reconciled with the table verdict. This is a minor but real inconsistency in a document where every word in the verdict column is consequential.

3. **MPL-2.0 compatibility rationale contains a logical gap.** The License Notes state: "MPL-2.0 Section 3.3 (GPL Compatibility) explicitly states that MPL-2.0 is compatible with GPL v2+, and by extension with Apache 2.0 (which is GPL v3 compatible)." The phrase "by extension" papers over a non-trivial legal inference: GPL v3 compatibility does not automatically confer Apache 2.0 compatibility because the Apache License 2.0 and GPL v3 have distinct compatibility determinations that are transitive only in specific combinations. The FSF and OSI do recognize this compatibility, but stating it as a purely logical extension is imprecise.

**Improvement Path:**

- Align Summary and Verdict section counts. Choose one authoritative count and correct the other; add a reconciliation note if the definitions differ.
- Change certifi's Compatible verdict in the table to "Yes (conditional — see License Notes)" to match the Methodology classification.
- Revise the MPL-2.0 compatibility argument to cite the FSF/OSI determination directly rather than deriving it transitively.

---

### Methodological Rigor (0.83/1.00) — Major

**Evidence:**

The classification standard is explicitly documented with three tiers: Compatible (list of license families), Conditionally Compatible, and Incompatible (GPL-2.0, GPL-3.0, AGPL-3.0, SSPL, CC-BY-SA). This is a genuine strength — most ad-hoc audits lack an explicit classification taxonomy. The tool invocation command is documented (`pip-licenses --format=json --with-urls`). The scope is explicitly stated (53 packages, active uv virtual environment). The pyproject.toml source path is cited.

**Gaps:**

1. **Supplemental verification is asserted without evidence.** The Methodology states: "Supplemental verification: `importlib.metadata` for packages not shown in pip-licenses output (pip-licenses itself, prettytable, wcwidth, pip)." No output, script, or recorded result of this check is included. The assertion that this was performed is unverifiable from the document.

2. **Absent packages handled without systematic verification.** "mypy, pytest-archon, pytest-bdd, pytest-cov declared in pyproject.toml but not installed; all known MIT-licensed; no risk." For an audit document that is a QG gate artifact, "known" is not a sufficient methodological basis. At minimum, the PyPI license metadata for each should be checked and recorded.

3. **`packaging` dual SPDX `OR` expression receives no methodological treatment.** A disjunctive license expression (`A OR B`) has different legal implications than a conjunctive one (`A AND B`). The audit correctly handles `regex`'s `AND` expression but silently classifies `packaging`'s `OR` expression as "Yes" without any methodological note. This is inconsistent application of rigor across similar edge cases.

4. **No uv lock file reference.** The audit scans the active virtual environment but does not confirm that this environment is reproducibly defined by the uv lock file. A future `uv sync` could change the installed set. A rigorous audit would note whether a lock file was consulted.

**Improvement Path:**

- Include the raw output of the supplemental `importlib.metadata` check as an appendix or inline block.
- Add a "Declared but Uninstalled" sub-table with PyPI SPDX identifiers for the 4 absent packages.
- Add a brief License Notes entry for `packaging` explaining the `OR` disjunctive expression.
- Add a statement confirming whether the scanned environment matches the committed uv lock file.

---

### Evidence Quality (0.80/1.00) — Major

**Evidence:**

The primary data source is credible: `pip-licenses 5.5.1` is a widely-used, authoritative tool for Python dependency license scanning. The tool version and invocation syntax are documented. The pyproject.toml file path is cited, grounding the declared dependency scope.

**Gaps:**

1. **No raw output artifact.** The package tables are presumably generated from pip-licenses JSON output, but no raw output, script, or artifact is attached. A reviewer cannot independently verify that the table entries match the tool output without re-running the tool.

2. **License compatibility arguments cite authorities without URLs.** The MPL-2.0 analysis states "The OSI and FSF both recognize MPL-2.0 as compatible with Apache 2.0 in this use pattern" — no link to the OSI license compatibility list or FSF documentation. The CNRI-Python analysis states it is "OSI-approved" — no link to the OSI approved licenses list. Section numbers for the MPL-2.0 license (§1.6, §3.3) are cited without linking to the MPL-2.0 license text.

3. **Supplemental check produces no documented output.** The `importlib.metadata` supplemental verification is referenced but no output is provided, making it an unverifiable assertion (see also Methodological Rigor gap 1).

4. **"known to be MIT-licensed" for absent packages is a bare assertion.** No lookup, PyPI metadata record, or citation supports this claim.

**Improvement Path:**

- Attach the pip-licenses JSON output as an appendix (even abbreviated) or reference a saved artifact file.
- Add URLs to OSI and FSF compatibility documentation for MPL-2.0 and a link to the OSI approved license list for CNRI-Python.
- Record and inline the `importlib.metadata` check results.
- Add PyPI license metadata citations for the 4 absent packages.

---

### Actionability (0.88/1.00) — Minor

**Evidence:**

The Verdict section provides a clear, unambiguous gate decision: "PASS." The Incompatible Dependencies section explicitly states no incompatible packages were found. The License Notes provide clear "No action required" conclusions for certifi and regex. A downstream workflow (or human reviewer) can immediately use this audit to proceed with the MIT-to-Apache 2.0 migration.

**Gaps:**

1. **No re-audit trigger or cadence guidance.** The audit does not state when it should be repeated (e.g., "re-audit required when any new dependency is added"). For an OSS release workflow, this forward-looking guidance is an expected element.

2. **No remediation template for future incompatible findings.** The Incompatible Dependencies section currently says "None found." There is no guidance on what action to take if a future audit run identifies a GPL or AGPL package (e.g., remove, replace, or apply exception). This reduces the actionability of the audit as a reusable process artifact.

3. **Absent packages: no action defined for when they are installed.** The 4 absent packages are noted as "no risk" but there is no instruction to re-run the audit when they are installed, nor is there a placeholder for their verdicts.

**Improvement Path:**

- Add a "Re-Audit Conditions" section specifying triggers (new dependency added, uv lock file updated, new dev environment created).
- Add a brief "Remediation Guidance" subsection to Incompatible Dependencies explaining the standard resolution paths (remove dep, find alternative, apply license exception with legal sign-off).
- Add a note in the Dev Dependencies section specifying the action when the 4 absent packages are installed.

---

### Traceability (0.87/1.00) — Minor

**Evidence:**

The document header explicitly cites Workflow ID (`feat015-licmig-20260217-001`), Enabler (`EN-934`), Agent, and Date. The footer repeats the workflow ID. The pyproject.toml source path is cited. A navigation table with anchor links is present (H-23, H-24 compliant).

**Gaps:**

1. **No link to QG-1 gate specification.** The audit is filed under `quality-gates/qg-1/` but the document itself does not reference the QG-1 gate specification or what criteria the gate requires. A reader cannot verify that this audit satisfies all QG-1 acceptance criteria from the document alone.

2. **No reference to EN-934 enabler requirements.** The document cites EN-934 as the enabler but does not describe what EN-934 requires this audit to deliver. Without that, a reviewer cannot confirm that the audit scope matches the enabler specification.

3. **No WORKTRACKER item reference.** Standard Jerry workflow artifacts reference their WORKTRACKER item. This document does not.

4. **No reference to the feat015 orchestration plan document.** The workflow ID is cited but not the plan document path.

**Improvement Path:**

- Add a "Traceability" section listing: QG-1 gate spec path, EN-934 enabler requirement statement, WORKTRACKER item reference, and orchestration plan path.
- Or add these as header metadata fields.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Internal Consistency | 0.78 | 0.92 | Reconcile the dev package count discrepancy between Summary (8) and Verdict (6); change certifi table verdict to "Yes (conditional — see License Notes)"; revise the MPL-2.0 compatibility chain argument to cite FSF/OSI directly |
| 2 | Completeness | 0.82 | 0.92 | Add a "Declared but Uninstalled" sub-table for the 4 absent packages with PyPI SPDX IDs; add explicit LGPL absence statement to Incompatible Dependencies; add a License Notes entry for `packaging`'s `OR` expression |
| 3 | Methodological Rigor | 0.83 | 0.92 | Include raw supplemental `importlib.metadata` output; verify and record absent package license IDs; add a note on uv lock file consistency; add `packaging` OR-expression analysis |
| 4 | Evidence Quality | 0.80 | 0.92 | Add URLs for OSI and FSF MPL-2.0 and CNRI-Python compatibility documentation; attach or reference pip-licenses JSON output artifact; record importlib.metadata check results; add PyPI metadata citations for absent packages |
| 5 | Traceability | 0.87 | 0.92 | Add Traceability section with: QG-1 gate spec path, EN-934 requirement statement, WORKTRACKER item ID, orchestration plan path |
| 6 | Actionability | 0.88 | 0.92 | Add Re-Audit Conditions section; add Remediation Guidance for incompatible findings; add note on re-running audit when absent packages are installed |

**Implementation Guidance:**

Priority 1 (Internal Consistency) is the most critical fix — the Summary/Verdict count contradiction directly undermines trust in the audit as a gate artifact and should be resolved first. Priority 2 and 3 address the completeness and methodology gaps that together constitute the largest weighted drag on the composite score. Priorities 4-6 are targeted improvements that are lower effort and can be addressed in a single revision pass after the structural fixes are complete. The count reconciliation in Priority 1 may also resolve some of the Completeness gaps if it reveals that the 8-vs-6 discrepancy stems from missing table rows.

---

## Scoring Impact Analysis

### Dimension Impact on Composite

| Dimension | Weight | Score | Weighted Contribution | Gap to 0.92 Target | Weighted Gap |
|-----------|--------|-------|----------------------|-------------------|--------------|
| Completeness | 0.20 | 0.82 | 0.164 | 0.10 | 0.020 |
| Internal Consistency | 0.20 | 0.78 | 0.156 | 0.14 | 0.028 |
| Methodological Rigor | 0.20 | 0.83 | 0.166 | 0.09 | 0.018 |
| Evidence Quality | 0.15 | 0.80 | 0.120 | 0.12 | 0.018 |
| Actionability | 0.15 | 0.88 | 0.132 | 0.04 | 0.006 |
| Traceability | 0.10 | 0.87 | 0.087 | 0.05 | 0.005 |
| **TOTAL** | **1.00** | | **0.825** | | **0.095** |

**Interpretation:**

- **Current composite:** 0.83/1.00
- **Target composite:** 0.92/1.00 (H-13 threshold)
- **Total weighted gap:** 0.095
- **Largest improvement opportunity:** Internal Consistency (weighted gap 0.028, 29% of total gap)

### Verdict Rationale

**Verdict:** REJECTED

**Rationale:** The weighted composite score of 0.83 falls below the H-13 threshold of 0.92 and below the REVISE band floor of 0.85, placing this deliverable in the REJECTED band (< 0.85) per quality-enforcement.md Operational Score Bands. No single dimension has a Critical finding (score <= 0.50), so no special condition override applies. However, two dimensions score in the Major range (Internal Consistency: 0.78, Completeness: 0.82), and two additional dimensions are also Major (Methodological Rigor: 0.83, Evidence Quality: 0.80). The Internal Consistency defect — a direct factual contradiction between named sections — is particularly significant for an audit report that functions as an OSS release gate artifact. The six recommendations above, if implemented, should be sufficient to bring the composite above 0.92 in a single revision cycle.

---

## Leniency Bias Check (H-15 Self-Review)

- [x] Each dimension scored independently (no cross-dimension influence — each dimension analyzed separately before composite was computed)
- [x] Evidence documented for each score (specific section references, quotes, and gap descriptions provided for all six dimensions)
- [x] Uncertain scores resolved downward (Completeness: considered 0.84 initially, reduced to 0.82 on the factual count inconsistency; Internal Consistency: considered 0.82 initially, reduced to 0.78 on the severity of the direct count contradiction between named sections)
- [x] First-draft calibration noted (score of 0.83 is consistent with first-draft range; the audit is substantively well-structured but has correctable defects typical of first-pass technical audit documents)
- [x] No dimension scored above 0.95 (highest score is 0.88 for Actionability; no exceptional verification required)
- [x] High-scoring dimensions verified (Actionability 0.88: (1) Verdict section states "PASS" unambiguously; (2) "No action required" stated explicitly for both edge-case licenses; (3) Downstream workflow can immediately act on the gate decision without interpretation. Traceability 0.87: (1) Workflow ID feat015-licmig-20260217-001 in header; (2) Enabler EN-934 in header; (3) Agent and date documented.)
- [x] Low-scoring dimensions verified (Internal Consistency 0.78: direct count contradiction between Summary and Verdict — 8 dev/41 transitive vs 6 dev/43 transitive; Completeness 0.82: count inconsistency is unresolved, 4 absent packages unverified, LGPL absence unstated; Evidence Quality 0.80: no URLs for OSI/FSF authority claims, no raw output artifact, supplemental check unevidenced)
- [x] Weighted composite matches mathematical calculation (0.82*0.20 + 0.78*0.20 + 0.83*0.20 + 0.80*0.15 + 0.88*0.15 + 0.87*0.10 = 0.164 + 0.156 + 0.166 + 0.120 + 0.132 + 0.087 = 0.825, rounded to 0.83)
- [x] Verdict matches score range (0.825 < 0.85 → REJECTED band per quality-enforcement.md Operational Score Bands)
- [x] Improvement recommendations are specific and actionable (each recommendation identifies the specific section, content, or evidence to add; not generic)

**Leniency Bias Counteraction Notes:**

Two scores were adjusted downward from initial estimates. Completeness was initially estimated at 0.84 (Minor) but the factual count inconsistency between Summary and Verdict is not a minor editorial issue — it is a completeness defect in a numerical audit document, and 0.82 (Major) better reflects this. Internal Consistency was initially estimated at 0.82 but the direct contradiction between two terminal sections (Summary and Verdict) of an audit report is a material defect that warrants a Major finding at 0.78 rather than a near-threshold score. The MPL-2.0 transitivity argument gap and the methodology/table classification misalignment further support the lower score. No scores were inflated; where evidence was strong (Actionability, Traceability) the scores reflect genuine strengths without overclaiming.

---

*Generated by adv-scorer for orchestration workflow feat015-licmig-20260217-001, QG-1, strategy S-014 LLM-as-Judge*
*SSOT: `.context/rules/quality-enforcement.md`*
