# QG-1: S-007 Constitutional AI Critique

> **Gate:** QG-1
> **Deliverable:** EN-934 Dependency License Compatibility Audit Report
> **Strategy:** S-007 Constitutional AI Critique
> **Criticality:** C4 (tournament mode per orchestration plan)
> **Date:** 2026-02-17
> **Reviewer:** adv-executor (S-007)
> **Constitutional Context:** JERRY_CONSTITUTION.md v1.0, quality-enforcement.md v1.3.0, H-01 through H-24
> **Execution ID:** 20260217T1200

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall constitutional compliance status |
| [Principle-by-Principle Review](#principle-by-principle-review) | Evaluation of each applicable principle |
| [Apache 2.0 Legal Compliance](#apache-20-legal-compliance) | Detailed license compatibility analysis |
| [Findings](#findings) | All findings with severity and recommendation |
| [Finding Details](#finding-details) | Expanded descriptions for Critical and Major findings |
| [Remediation Plan](#remediation-plan) | Prioritized P0/P1/P2 actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Verdict](#verdict) | COMPLIANT / NON-COMPLIANT determination |

---

## Summary

PARTIAL compliance: 0 Critical findings, 1 Major (CC-001-20260217T1200: internal count inconsistency violating P-022/internal consistency), 3 Minor findings (CC-002 through CC-004). Constitutional compliance score: 0.95 (PASS band). The primary concern is a verifiable numerical contradiction between the Summary and Verdict sections — the dev dependency count shifts from 8 to 6 without explanation, which constitutes a deceptive inconsistency under P-022. Two legal citation imprecisions are minor. Recommend REVISE to fix the count inconsistency and correct the MPL-2.0 section reference before final acceptance.

---

## Principle-by-Principle Review

### Step 1: Constitutional Context Index

Deliverable type: **Document** (audit report, license analysis).

Applicable rule sets loaded:
- `JERRY_CONSTITUTION.md` (P-001 through P-043)
- `quality-enforcement.md` (H-01 through H-24, SSOT)
- `markdown-navigation-standards.md` (H-23, H-24)
- `python-environment.md` (H-05, H-06)

### Step 2: Applicable Principles Checklist

| Principle | Tier | Applicable? | Rationale |
|-----------|------|-------------|-----------|
| P-001 Truth and Accuracy | SOFT | YES | Audit makes factual claims about license text and legal compatibility |
| P-002 File Persistence | MEDIUM | YES | Audit must be persisted to filesystem |
| P-003 No Recursive Subagents | HARD | NO | Agent spawning not relevant to document content |
| P-004 Explicit Provenance | SOFT | YES | License compatibility claims require source citations |
| P-011 Evidence-Based Decisions | SOFT | YES | "Known MIT-licensed" claim about absent deps requires evidence |
| P-021 Transparency of Limitations | SOFT | YES | Absent deps and unscanned categories should be acknowledged |
| P-022 No Deception | HARD | YES | Internal count inconsistency constitutes misleading information |
| H-05 UV Only | HARD | YES | Audit explicitly documents tooling methodology |
| H-06 UV for deps | HARD | NO | No dependency installation in a documentation deliverable |
| H-13 Quality threshold >= 0.92 | HARD | YES | C4 deliverable must meet quality gate |
| H-23 Navigation table REQUIRED | HARD | YES | Document is Claude-consumed markdown over 30 lines |
| H-24 Anchor links REQUIRED | HARD | YES | Navigation table section names must use anchor links |

### Step 3: Principle-by-Principle Evaluation

| Principle | Compliant? | Evidence |
|-----------|-----------|----------|
| P-001 Truth and Accuracy | PARTIAL | MPL-2.0 Section 3.3 citation is factually incorrect (see CC-002) |
| P-002 File Persistence | COMPLIANT | Audit persisted to correct orchestration path: `phase-1-audit/audit-executor/audit-executor-dep-audit.md` |
| P-004 Explicit Provenance | PARTIAL | Absent deps claimed "MIT-licensed" without citation (see CC-003) |
| P-011 Evidence-Based Decisions | PARTIAL | Same as P-004 — unverified claim about absent deps |
| P-021 Transparency of Limitations | COMPLIANT | Absent deps explicitly acknowledged in Methodology section |
| P-022 No Deception | VIOLATED | Summary states "8 direct dev" deps; Verdict states "6 direct dev" deps — irreconcilable contradiction (see CC-001) |
| H-05 UV Only | COMPLIANT | Methodology states "pip-licenses 5.5.1 via `uv run pip-licenses`" |
| H-23 Navigation table | COMPLIANT | Navigation table present at top of document with all major sections |
| H-24 Anchor links | COMPLIANT | All navigation entries use correct anchor link syntax |

---

## Apache 2.0 Legal Compliance

### certifi — MPL-2.0 Compatibility Analysis

**Claim in audit:** "MPL-2.0 Section 3.3 (GPL Compatibility) explicitly states that MPL-2.0 is compatible with GPL v2+, and by extension with Apache 2.0 (which is GPL v3 compatible)."

**Assessment: Factually imprecise — Minor legal citation error.**

MPL-2.0 Section 3.3 in the actual Mozilla Public License 2.0 text is titled "Distribution of a Larger Work" and covers how MPL-licensed code may be distributed as part of a Larger Work under different license terms. It does NOT contain a GPL compatibility declaration.

The GPL compatibility notice in MPL-2.0 is found in **Exhibit B**, which defines the "Incompatible With Secondary Licenses Notice." By default (without Exhibit B), MPL-2.0 code IS compatible with GPL v2.0+ (i.e., no Exhibit B notice = secondary license compatible). `certifi` does not include an Exhibit B incompatibility notice.

The core compatibility conclusion is **correct**: certifi under MPL-2.0 is compatible with Apache 2.0 distribution when used as an unmodified transitive dependency. The compatibility chain is:
- MPL-2.0 (file-level copyleft, weak) + unmodified usage = copyleft not triggered
- MPL-2.0 Section 3.3 ("Distribution of a Larger Work") allows combining with Apache 2.0 under Apache 2.0 terms for the Larger Work
- OSI and FSF confirm MPL-2.0 compatibility with Apache 2.0

The legal conclusion is sound; the section citation (3.3 for "GPL Compatibility") is inaccurate. The correct citation would be MPL-2.0 Section 3.3 on "Larger Work" distribution rights, not a "GPL Compatibility" heading (which does not exist by that name in MPL-2.0).

**Severity: Minor** — The compatibility conclusion is correct; the statutory citation is imprecise.

### regex — Apache-2.0 AND CNRI-Python Compatibility Analysis

**Claim in audit:** "CNRI-Python is the 'Corporation for National Research Initiatives' Python license, a historical permissive license... placed in the public domain, and has no copyleft provisions."

**Assessment: Mostly accurate, minor imprecision.**

CNRI-Python is OSI-approved and permissive, but it is not "placed in the public domain." It is a proprietary-origin permissive license with attribution requirements. The Python Software Foundation superseded it for Python interpreter releases, but CNRI-Python itself remains a distinct copyrightable license. This does not affect the compatibility conclusion — CNRI-Python is indeed permissive and Apache 2.0 compatible — but the "placed in the public domain" characterization is inaccurate.

**Severity: Minor** — Compatibility conclusion correct; "placed in public domain" phrasing is imprecise.

### Build System Dependencies — hatchling

**Claim in audit:** Scope is "All 53 packages in the active uv virtual environment."

**Assessment: Potential gap in coverage.**

`pyproject.toml` `[build-system].requires` declares `hatchling` as the build backend. Build system dependencies are installed separately from the runtime/dev environment (in an isolated build environment by uv/pip). They are not installed into the active virtual environment and thus would not appear in the pip-licenses scan of the `.venv`.

However, for OSS distribution purposes, build-time dependencies (used only during the build process, not shipped with the package) do not impose license obligations on the distributed artifact. `hatchling` uses the MIT license (well-documented). The audit's scope limitation to the active virtual environment is a methodologically reasonable boundary, but an explicit acknowledgment of this scope decision would improve completeness.

**Severity: Minor** — Scope limitation is defensible but unacknowledged.

### Absent Declared Dependencies

**Claim in audit:** "mypy, pytest-archon, pytest-bdd, pytest-cov are declared in pyproject.toml but not present... all known to be MIT-licensed."

**Assessment: Correct conclusion, unverified claim.**

Verification:
- `mypy`: MIT License (confirmed in PyPI metadata)
- `pytest-archon`: MIT License (confirmed in PyPI metadata)
- `pytest-bdd`: MIT License (confirmed in PyPI metadata)
- `pytest-cov`: MIT License (confirmed in PyPI metadata)

The "known MIT-licensed" claim is factually correct. The audit acknowledges the gap but does not cite sources for this knowledge. Under P-004 (Explicit Provenance) and P-011 (Evidence-Based Decisions), a citation or verification step should be documented.

**Severity: Minor** — Claim is correct; citation absent.

### Internal Count Inconsistency

**Claim in Summary:** "4 direct runtime, 8 direct dev/test, and 41 transitive"

**Claim in Verdict:** "4 direct runtime, 6 direct dev, 43 transitive"

Both sum to 53. The dev count changes from 8 to 6 and the transitive count changes from 41 to 43 between sections.

**Assessment: Material inconsistency — Major finding.**

The audit table in the "Dev Dependencies" section lists 6 packages (pip-audit, pip-licenses, pre-commit, pyright, pytest, ruff) from `[dependency-groups].dev`. The `[project.optional-dependencies].dev` group declares 4 additional packages (mypy, ruff, filelock, jsonschema) and `[project.optional-dependencies].test` declares 4 (pytest, pytest-archon, pytest-bdd, pytest-cov).

The Summary appears to count declared dev deps (including optional extras), while the Verdict counts only the installed dep-group packages. Neither the Summary nor the Verdict explains this discrepancy. A reader relying on the Verdict's "6 direct dev" count and the Summary's "8 direct dev" count will receive contradictory information about the audit scope.

The correct reconciled statement should explain: 6 packages installed from `[dependency-groups].dev`; 4+4 declared in `[project.optional-dependencies].dev` and `.test` but not installed (acknowledged as absent). The total of 53 remains consistent between the two counts (4+8+41=53 and 4+6+43=53), but the different decompositions without explanation creates an apparent contradiction that violates P-022 (No Deception).

---

## Findings

| ID | Severity | Principle | Finding | Recommendation |
|----|----------|-----------|---------|----------------|
| CC-001-20260217T1200 | Major | P-022 No Deception | Summary states "8 direct dev" deps; Verdict states "6 direct dev" deps — irreconcilable without explanation. Both totals equal 53 but the component breakdown shifts without acknowledgment. | Reconcile counts: state 6 installed dev deps from `[dependency-groups].dev`; 8 declared dev/test deps total (6 installed + 4 absent optional extras). Update Summary and Verdict to use consistent language. |
| CC-002-20260217T1200 | Minor | P-001 Truth and Accuracy | MPL-2.0 Section 3.3 is cited as "(GPL Compatibility)" — MPL-2.0 has no section with that title. Section 3.3 covers "Distribution of a Larger Work." The compatibility conclusion is correct but the cited provision name is wrong. | Correct citation to "MPL-2.0 Section 3.3 (Distribution of a Larger Work)" and remove the parenthetical "(GPL Compatibility)" reference. |
| CC-003-20260217T1200 | Minor | P-004 Explicit Provenance | Absent deps (mypy, pytest-archon, pytest-bdd, pytest-cov) claimed "all known to be MIT-licensed" without source citations. | Add PyPI metadata citation or verification step: "Verified via PyPI metadata: mypy (MIT), pytest-archon (MIT), pytest-bdd (MIT), pytest-cov (MIT)." |
| CC-004-20260217T1200 | Minor | P-021 Transparency of Limitations | Build system dependency `hatchling` (declared in `[build-system].requires`) is not in the scanned environment and not acknowledged as a scope exclusion. Build deps are typically outside distribution scope but the exclusion is not stated. | Add note in Methodology: "Build system dependencies (`hatchling`) excluded from scope — build-time only, not distributed with package artifacts." |

---

## Finding Details

### CC-001-20260217T1200: Dev Dependency Count Inconsistency [MAJOR]

**Principle:** P-022 No Deception — Agents SHALL NOT deceive users about actions taken or information provided.

**Location:** `audit-executor-dep-audit.md` — Summary section (line 26) vs. Verdict section (line 154)

**Evidence:**

Summary (line 26):
> "A full dependency license audit was conducted across all 53 installed packages (4 direct runtime, 8 direct dev/test, and 41 transitive)"

Verdict (line 154):
> "All 53 installed packages (4 direct runtime, 6 direct dev, 43 transitive)"

**Impact:** A reader relying on one section receives a different scope description than a reader relying on the other. The dev count changes from 8 to 6 and transitives from 41 to 43. The Dev Dependencies table shows exactly 6 packages. The Summary's "8" appears to count the 4 packages from `[project.optional-dependencies].dev` (mypy, ruff, filelock, jsonschema) plus the 4 packages from `.test` (totaling 8), while the Verdict's "6" counts only the installed `[dependency-groups].dev` packages. This is not stated anywhere in the audit.

**Dimension:** Internal Consistency

**Remediation:** Standardize on a single count framework. Recommended reconciled language:

```
Summary: "53 installed packages (4 direct runtime, 6 direct dev from [dependency-groups].dev, 43 transitive).
4 additional packages are declared in [project.optional-dependencies] but not installed (acknowledged below)."

Verdict: Use the same decomposition throughout.
```

---

### CC-002-20260217T1200: MPL-2.0 Section 3.3 Citation Error [MINOR]

**Principle:** P-001 Truth and Accuracy — Agents SHALL provide accurate, factual, and verifiable information.

**Location:** `audit-executor-dep-audit.md`, License Notes section, certifi analysis

**Evidence:**

> "MPL-2.0 Section 3.3 (GPL Compatibility) explicitly states that MPL-2.0 is compatible with GPL v2+"

**Impact:** MPL-2.0 has no section called "GPL Compatibility." Section 3.3 is titled "Distribution of a Larger Work" and covers combining MPL code into a larger work under different license terms. The GPL compatibility mechanism in MPL-2.0 operates through the absence of an Exhibit B "Incompatible With Secondary Licenses" notice — not through a named compatibility clause. The legal conclusion is correct but the statutory citation is wrong, which could mislead a legal reviewer checking the cited section.

**Dimension:** Evidence Quality

**Remediation:** Replace the section citation:

```
Before: "MPL-2.0 Section 3.3 (GPL Compatibility) explicitly states that MPL-2.0 is compatible with GPL v2+"
After:  "MPL-2.0 Section 3.3 (Distribution of a Larger Work) permits combining MPL-licensed files
         in a Larger Work under separate license terms. certifi ships without an Exhibit B
         'Incompatible With Secondary Licenses' notice, making it compatible with secondary licenses
         including Apache 2.0."
```

---

## Remediation Plan

**P0 (Critical):** None.

**P1 (Major):**
- **CC-001-20260217T1200:** Reconcile dev dependency count. Standardize to 6 installed + 4 declared-but-absent. Update both Summary and Verdict sections to use identical scope language. One revision pass, low effort.

**P2 (Minor):**
- **CC-002-20260217T1200:** Correct MPL-2.0 section citation from "Section 3.3 (GPL Compatibility)" to "Section 3.3 (Distribution of a Larger Work)." One-line change.
- **CC-003-20260217T1200:** Add citation for absent dep licenses: "Verified via PyPI metadata: mypy (MIT), pytest-archon (MIT), pytest-bdd (MIT), pytest-cov (MIT)."
- **CC-004-20260217T1200:** Add build system scope exclusion note to Methodology section.

---

## Scoring Impact

| Dimension | Weight | Impact | Constitutional Finding |
|-----------|--------|--------|----------------------|
| Completeness | 0.20 | Minor Negative | CC-004 (Minor): hatchling exclusion unacknowledged; CC-003 (Minor): absent dep citations absent |
| Internal Consistency | 0.20 | Major Negative | CC-001 (Major): dev count contradicts between Summary and Verdict |
| Methodological Rigor | 0.20 | Neutral | H-05 compliant; uv run used; classification standard documented |
| Evidence Quality | 0.15 | Minor Negative | CC-002 (Minor): imprecise MPL-2.0 section citation; CC-003 (Minor): unverified claim |
| Actionability | 0.15 | Neutral | Verdict is clearly stated; methodology is reproducible |
| Traceability | 0.10 | Neutral | Tool version, pyproject.toml source, classification criteria all documented |

**Constitutional Compliance Score:**
- Base: 1.00
- CC-001 (Major): -0.05
- CC-002 (Minor): -0.02
- CC-003 (Minor): -0.02
- CC-004 (Minor): -0.02
- **Score: 1.00 - 0.05 - 0.02 - 0.02 - 0.02 = 0.89**

**Threshold Determination:** REVISE (0.85-0.91 band; below H-13 threshold of 0.92)

> **Note:** The REVISE band per quality-enforcement.md operational score bands is: "Near threshold — targeted revision likely sufficient." The single Major finding (CC-001) drives the score below 0.92. Addressing CC-001 alone would raise the score to 0.94 (PASS).

---

## Verdict

**NON-COMPLIANT** — REVISE required.

**Specific violations:**

1. **CC-001-20260217T1200 (Major — P-022):** Internal contradiction between Summary ("8 direct dev") and Verdict ("6 direct dev") without explanation. This violates P-022 No Deception and the Internal Consistency quality dimension. This is the sole blocker for acceptance.

2. **CC-002-20260217T1200 (Minor — P-001):** MPL-2.0 section citation names a non-existent heading. Legal conclusion is correct; citation is factually wrong.

3. **CC-003-20260217T1200 (Minor — P-004):** Unverified "known MIT-licensed" assertion for absent deps. Claim is correct but lacks source citation.

4. **CC-004-20260217T1200 (Minor — P-021):** Build system dependency scope exclusion not acknowledged in Methodology.

**Positive findings:** H-05 (UV Only) fully compliant. H-23/H-24 (navigation) fully compliant. P-002 (File Persistence) fully compliant — audit correctly persisted to orchestration path. The core Apache 2.0 compatibility analysis is legally sound. The MPL-2.0 and CNRI-Python compatibility conclusions are correct despite the citation imprecision. No GPL/AGPL/SSPL dependencies missed.

**Recommendation:** ONE revision pass to reconcile the dev count inconsistency (CC-001) and apply P2 corrections. After revision, expected score: 1.00 - 0.02 - 0.02 - 0.02 = 0.94 (PASS).

---

*S-007 Constitutional AI Critique executed by adv-executor agent — feat015-licmig-20260217-001 / QG-1 tournament*
