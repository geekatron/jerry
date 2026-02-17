# QG-1: S-002 Devil's Advocate Challenge

> **Gate:** QG-1
> **Deliverable:** EN-934 Dependency License Compatibility Audit Report
> **Strategy:** S-002 Devil's Advocate
> **Date:** 2026-02-17
> **Reviewer:** adv-executor (S-002 Devil's Advocate agent)
> **H-16 Compliance:** NOTE -- No S-003 Steelman output was provided as a prerequisite. This execution proceeds under explicit task direction; H-16 non-compliance is recorded here as a procedural gap in the QG-1 workflow, not a defect in this output.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Role Assumption](#role-assumption) | Adversarial mandate and scope |
| [Assumption Inventory](#assumption-inventory) | Explicit and implicit assumptions extracted |
| [Findings Table](#findings-table) | All DA-NNN findings with severity and dimension |
| [Finding Details](#finding-details) | Expanded Critical and Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized action list |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |
| [Overall Assessment](#overall-assessment) | PASS verdict survival under challenge |

---

## Role Assumption

**Deliverable under challenge:** audit-executor-dep-audit.md (EN-934 Dependency License Compatibility Audit Report)
**Criticality:** C4 (license migration is irreversible governance action; auto-C4 per AE rules)
**Mandate:** Construct the strongest possible case against the audit's PASS verdict. Find every gap, logical flaw, and unsupported assumption. The audit has declared that Jerry Framework may proceed with MIT-to-Apache 2.0 license migration without any dependency license blockers. This role challenges that declaration.

---

## Assumption Inventory

### Explicit Assumptions

| Assumption | Location | Challenge |
|------------|----------|-----------|
| "All 53 installed packages" are covered | Summary | The tool returned 49 packages; 4 were recovered via supplemental method with no documented verification process. |
| Absent deps (mypy, pytest-archon, pytest-bdd, pytest-cov) are "known to be MIT-licensed" | Dev deps note | No source cited. "Known" is an assertion, not a verification. |
| certifi files will remain unmodified in perpetuity | License Notes | Explicitly acknowledged as a future risk but dismissed without a monitoring or policy mechanism. |
| pip-licenses 5.5.1 correctly identifies all installed packages | Methodology | Demonstrably false: pip-licenses missed 4 packages from the 53 pip list total. |
| MPL-2.0 compatibility via GPL v3 transitivity is legally sound | License Notes | The chain (MPL-2.0 compat with GPL v2+ -> GPL v3 compat with Apache 2.0) is a non-trivial transitive inference that omits the one-way nature of GPL/Apache compatibility. |

### Implicit Assumptions

| Assumption | Evidence | Challenge |
|------------|----------|-----------|
| The virtual environment scope equals the distribution scope | Never stated | The audit scoped to the uv venv. OSS distribution may include build tooling or CI dependencies not in the venv. |
| Optional dependency extras do not add undisclosed packages | Never stated | `jsonschema[test]` is declared in pyproject.toml but `[test]` is not a valid jsonschema extra. This phantom extra is silently ignored by uv but indicates imprecision in dependency declarations. |
| Build-time dependencies (hatchling) need not be audited | Never stated | hatchling is a `[build-system]` dependency that is fetched at build time. It is absent from the venv but present during package building. Its license and transitive build-time deps were not audited. |
| Pre-commit hook repositories do not introduce license obligations | Never stated | Pre-commit fetches and installs isolated environments from external repos (pre-commit-hooks, ruff-pre-commit, commitizen). These are not in the uv venv and were not audited. |
| The 53 count in the Summary and the 53 count in the Verdict refer to the same breakdown | Summary vs. Verdict | They do not: Summary says "(4 direct runtime, 8 direct dev/test, and 41 transitive)" but Verdict says "(4 direct runtime, 6 direct dev, 43 transitive)." Both sum to 53, but the categorical breakdown disagrees. |

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260217T1200 | Internal inconsistency: Summary and Verdict disagree on dev/transitive count breakdown | Major | Summary: "8 direct dev/test, 41 transitive." Verdict: "6 direct dev, 43 transitive." Both sum to 53 but categorically differ. | Internal Consistency |
| DA-002-20260217T1200 | pip-licenses tool coverage gap: 4 packages verified only via undocumented supplemental method | Major | pip-licenses returned 49 packages; pip list returned 53. The 4-package gap (pip, pip-licenses, prettytable, wcwidth) was covered via `importlib.metadata` with no documented verification procedure or confidence statement. | Methodological Rigor |
| DA-003-20260217T1200 | Absent declared dependencies verified only by assertion, no evidence trail | Major | "mypy, pytest-archon, pytest-bdd, pytest-cov ... all known to be MIT-licensed. No risk." No source cited. No pip-licenses output. No importlib.metadata query. The word "known" is not a verification method. If any one of these had been relicensed in a recent version, this audit would not have caught it. | Evidence Quality |
| DA-004-20260217T1200 | MPL-2.0 compatibility legal chain contains a non-sequitur | Major | The audit states: "MPL-2.0 Section 3.3 (GPL Compatibility) explicitly states that MPL-2.0 is compatible with GPL v2+, and by extension with Apache 2.0 (which is GPL v3 compatible)." The "by extension" inference is legally unsound. Apache 2.0 compatibility with GPL v3 is one-way: GPLv3 can incorporate Apache 2.0 code, but Apache 2.0 projects do not thereby inherit blanket GPL-family compatibility for all licenses that are themselves GPL-compatible. The correct legal basis for MPL-2.0 + Apache 2.0 compatibility is their both being OSI-approved permissive/weak-copyleft licenses used in file-separation mode -- not a transitive chain through GPL. The conclusion may still be correct but the stated reasoning is fallacious. | Methodological Rigor |
| DA-005-20260217T1200 | Future certifi modification risk acknowledged but no control mechanism defined | Major | The audit correctly identifies that MPL-2.0 copyleft is triggered if certifi files are modified. It then asserts "No action required." This is insufficient for an OSS release governance audit. No policy, monitoring, or CI enforcement prevents a future developer from vendoring, patching, or forking certifi. The "no action required" finding should be "no action required NOW" paired with a standing constraint. | Actionability |
| DA-006-20260217T1200 | Build-time dependency (hatchling) not audited | Major | pyproject.toml [build-system] declares `requires = ["hatchling"]`. hatchling is not in the uv venv and was not audited. It is fetched at `uv build` time. For OSS distribution, the build toolchain's license is relevant: if hatchling or its deps carried a GPL or SSPL license, it could impose obligations on build artifacts. The audit methodology explicitly scoped to "all 53 packages in the active uv virtual environment" -- this exclusion is undocumented and unjustified. | Completeness |
| DA-007-20260217T1200 | Pre-commit hook repo dependencies not audited | Minor | Pre-commit fetches isolated virtualenvs from three external repos at install time: `pre-commit/pre-commit-hooks@v5.0.0`, `astral-sh/ruff-pre-commit@v0.9.2`, `commitizen-tools/commitizen@v4.4.1`. These are not in the project venv but are installed on developer machines. For a framework distributed to developers who run `pre-commit install`, the license obligations of these hook environments may be relevant. | Completeness |
| DA-008-20260217T1200 | `jsonschema[test]` phantom extra indicates declaration imprecision | Minor | pyproject.toml declares `jsonschema[test]>=4.26.0`. The `[test]` extra does not exist in jsonschema's package metadata (available extras: `format`, `format-nongpl`). uv silently ignores non-existent extras. This means the dependency declaration contains an error that went undetected by the audit. While the end state (only core jsonschema installed) is benign, it signals that pyproject.toml contains imprecision that the audit did not flag. | Completeness |
| DA-009-20260217T1200 | Transitive dep count in audit table (42 rows) contradicts stated count (43) | Minor | Manual count of the Transitive Dependencies table yields 42 rows. The Verdict claims 43 transitive packages. One package is unaccounted for in the transitive table, or the Summary's "41 transitive" count (vs. Verdict's "43 transitive") reflects different counting logic. | Internal Consistency |
| DA-010-20260217T1200 | `wcwidth` license determined via `License-Expression` field, not `License` field -- accuracy not verified | Minor | pip-licenses missed wcwidth. The `importlib.metadata` `License` field returns `None` for wcwidth. The `License-Expression` field returns `MIT`. The audit states wcwidth is MIT-licensed, which matches `License-Expression`, but the methodology section says it used `importlib.metadata` without specifying which field. The License-Expression field is a newer PEP 639 field not supported by all tools. If a different tool or field was queried, the result could differ. | Evidence Quality |

---

## Finding Details

### DA-001: Internal Inconsistency -- Dev/Transitive Count Breakdown [MAJOR]

**Claim Challenged:** Summary section: "53 installed packages (4 direct runtime, 8 direct dev/test, and 41 transitive)." Verdict section: "53 installed packages (4 direct runtime, 6 direct dev, 43 transitive)."

**Counter-Argument:** The two authoritative sections of the same document disagree on the categorical breakdown of the 53 packages. The Dev Dependencies table contains exactly 6 rows (pip-audit, pip-licenses, pre-commit, pyright, pytest, ruff). The Verdict's "6 direct dev, 43 transitive" is consistent with the table. The Summary's "8 direct dev/test, 41 transitive" implies 2 additional dev packages that are not in the table. The most likely explanation is that the Summary was drafted to include some absent dependencies (mypy, or pytest-archon/pytest-bdd/pytest-cov) in the dev count, while the Verdict excluded them because they are not installed. This is not a labeling issue -- it is a factual inconsistency about what was audited. A reader relying on the Summary and a reader relying on the Verdict would reach different understandings of audit scope.

**Evidence:** Direct comparison of Summary paragraph vs. Verdict paragraph in the same document. Dev table row count = 6 (verified by manual count). 4 + 6 + 43 = 53 and 4 + 8 + 41 = 53 both add to 53, but the categorical contents differ.

**Impact:** If the Summary's "8 dev" count is correct, then 2 dev packages were audited but not included in the Dev table -- their license data is missing from the record. If the Verdict's "6 dev" count is correct, the Summary overstates coverage, giving a false sense of completeness.

**Dimension:** Internal Consistency

**Response Required:** The creator must reconcile the two counts, identify which packages are counted as the "8 dev/test" in the Summary, and either add them to the Dev table or correct the Summary to "6 direct dev."

**Acceptance Criteria:** Summary and Verdict must agree on the same categorical breakdown. If additional packages were audited, they must appear in their respective tables. If fewer packages were audited, the Summary must be corrected.

---

### DA-002: pip-licenses Coverage Gap -- 4 Packages Unverified by Primary Tool [MAJOR]

**Claim Challenged:** "The audit was executed using `pip-licenses 5.5.1` via `uv run`" (Methodology). Implied: pip-licenses covered all 53 packages.

**Counter-Argument:** pip-licenses 5.5.1 returned 49 packages from the current environment. pip list returns 53. The 4 packages not returned by pip-licenses (pip, pip-licenses, prettytable, wcwidth) were recovered via "supplemental verification: `importlib.metadata`." This is not a documented, reproducible verification procedure. The Methodology section mentions this supplemental step in a single line without specifying: which packages were looked up, which metadata field was queried (License vs. License-Expression vs. Classifier), whether the query was confirmed correct, or whether a human judgment call was required. For wcwidth specifically, the `License` field returns `None` and the actual license determination requires reading `License-Expression` -- a field that not all tooling supports and that was only standardized in PEP 639 (2024). The supplemental method has unknown reproducibility.

**Evidence:** `uv run pip-licenses --format=json` returns 49 items. `uv run pip list` returns 53 items. `importlib.metadata.metadata('wcwidth').get('License')` returns `None`; `importlib.metadata.metadata('wcwidth').get('License-Expression')` returns `MIT`. The audit's Methodology does not document which field was queried for the supplemental 4 packages.

**Impact:** If any of the 4 supplementally-verified packages has a different actual license than what was asserted, the audit's PASS verdict could be invalid. The primary risk is low (pip, pip-licenses, prettytable, wcwidth are all well-known MIT/BSD packages), but the verification process is not documented to the standard required for a governance audit supporting an irreversible license migration decision.

**Dimension:** Methodological Rigor

**Response Required:** Document the exact supplemental verification method for each of the 4 packages: tool or API used, field queried, output received. Alternatively, install the 4 packages in a separate environment where pip-licenses can capture them, and add them to the formal pip-licenses output.

**Acceptance Criteria:** Each of the 4 supplementally-verified packages must have a cited, reproducible verification source (not "known to be").

---

### DA-003: Absent Declared Dependencies -- License Verified Only by Assertion [MAJOR]

**Claim Challenged:** "mypy, pytest-archon, pytest-bdd, pytest-cov are declared in pyproject.toml but not installed; all known to be MIT-licensed; no risk." (Methodology note)

**Counter-Argument:** "Known to be MIT-licensed" is not a verification statement. It is an assertion from memory or general reputation. No version-specific license lookup is performed. This is a material gap because:

1. `pytest-bdd` has historically been MIT-licensed, but any package can change its license on a new major version. The audit covers specific installed versions -- it cannot be applied to uninstalled packages without version-pinning.
2. `pytest-archon` is a newer, less widely known package (it enforces architecture boundaries via pytest). Its license provenance is less established than pytest or mypy.
3. `mypy` is MIT-licensed in current versions, but mypy's stubs (which may be declared as separate optional deps) have mixed licensing including some MIT and some packages with more restrictive terms.
4. The audit's methodology only verifies installed packages. The absent deps could be installed at any time by any contributor running `uv sync --extra test` without triggering any license re-audit.

**Evidence:** pyproject.toml [project.optional-dependencies].test declares: `pytest>=8.0.0`, `pytest-archon>=0.0.6`, `pytest-bdd>=8.0.0`, `pytest-cov>=4.0.0`. None of these appear in the pip-licenses or pip list output. The audit cites no PyPI lookup, no GitHub repo check, no version-pinned license file check for any of these four packages.

**Impact:** If pytest-bdd 8.x, pytest-archon 0.0.6, or a future version of mypy carries or acquires a non-permissive license (or a dependency with one), the audit's PASS verdict will have been issued without ever checking. The "no risk" declaration is unfalsifiable given that no check was performed.

**Dimension:** Evidence Quality

**Response Required:** Perform and document version-specific license verification for each of the 4 absent packages at the version pinned in pyproject.toml. Use PyPI metadata API, GitHub repo license detection, or a test environment installation.

**Acceptance Criteria:** Each absent package must have a verifiable license record citing the specific version and a reproducible verification method (e.g., PyPI JSON API URL, pip-licenses output from a test install, or GitHub SPDX license field).

---

### DA-004: MPL-2.0 Compatibility Argument Contains a Logical Non-Sequitur [MAJOR]

**Claim Challenged:** "MPL-2.0 Section 3.3 (GPL Compatibility) explicitly states that MPL-2.0 is compatible with GPL v2+, and by extension with Apache 2.0 (which is GPL v3 compatible)." (License Notes, certifi section)

**Counter-Argument:** The stated reasoning chain is: (1) MPL-2.0 is compatible with GPL v2+. (2) Apache 2.0 is compatible with GPL v3. (3) Therefore MPL-2.0 is compatible with Apache 2.0. This is not a valid logical inference. GPL compatibility does not form a transitive equivalence relation. Specifically:

- "Apache 2.0 is compatible with GPL v3" means GPLv3 code CAN combine with Apache 2.0 code, not that Apache 2.0 projects absorb all the compatibility properties of GPLv3.
- Apache 2.0 is explicitly INCOMPATIBLE with GPL v2 (due to the additional restrictions clause in Apache 2.0 conflicting with GPL v2's no-additional-restrictions requirement). GPLv3 resolved this by adding the compatibility clause. MPL-2.0's GPL compatibility runs through GPLv2-or-later, which includes GPLv3 but not Apache 2.0 directly.
- The correct basis for certifi + Apache 2.0 compatibility is: MPL-2.0 is a file-level weak copyleft license; when used as an unmodified dependency (not as a combined work in the copyleft sense), the MPL-2.0 copyleft does not propagate. This is the "separate file" argument, not the "both are GPL-compatible" argument.

The conclusion (certifi is compatible when unmodified) is almost certainly correct, but it must be supported by the correct legal reasoning. The stated chain of logic is fallacious and would not survive legal scrutiny.

**Evidence:** The audit itself cites MPL-2.0 Section 3.3 and the Apache 2.0 / GPLv3 compatibility. The GNU Project's own documentation explicitly states Apache 2.0 is incompatible with GPLv2 (https://www.gnu.org/licenses/license-list.html#apache2). The transitivity inference from "MPL-2.0 compat with GPL" + "Apache 2.0 compat with GPLv3" to "MPL-2.0 compat with Apache 2.0" is a non-sequitur.

**Impact:** The conclusion (certifi is safe) may survive on the correct "unmodified file-level copyleft" argument, but the stated legal reasoning is flawed. In an OSS governance audit, flawed legal reasoning is independently problematic: it could mislead future maintainers who rely on the audit's stated rationale rather than performing independent analysis.

**Dimension:** Methodological Rigor

**Response Required:** Remove or replace the GPL-transitivity chain. State the correct legal basis: MPL-2.0 is a file-level copyleft; use as an unmodified dependency does not trigger the copyleft provision; the OSI and FSF both recognize this as a safe use pattern. Cite the specific OSI or FSF source for this interpretation.

**Acceptance Criteria:** The legal reasoning for certifi/MPL-2.0 compatibility must be self-consistent and not rely on GPL transitivity. Must cite a primary source (OSI, FSF, or MPL-2.0 text directly) for the compatibility basis.

---

### DA-005: certifi Modification Risk -- "No Action Required" Is Insufficient for a Governance Audit [MAJOR]

**Claim Challenged:** "No action required. No source modification of certifi files occurs; the MPL-2.0 copyleft clause is not triggered." (License Notes, certifi section)

**Counter-Argument:** The audit correctly identifies the key condition for MPL-2.0 compliance: certifi files must remain unmodified. It then dismisses the risk with "No action required." In an OSS governance audit for an irreversible license migration, a discovered condition that WOULD trigger a license obligation if violated requires more than "No action required now." Specifically:

1. There is no documented policy prohibiting certifi modification or vendoring. Any developer could vendor certifi (e.g., to fix a CA bundle issue) without realizing this triggers the MPL-2.0 copyleft.
2. There is no CI enforcement. No linting rule, architecture boundary check, or pre-commit hook prevents modification of certifi's source files if they were vendored.
3. The audit does not note that this risk should be re-evaluated if certifi is ever vendored, replaced by a fork, or if a certifi file is bundled into the distribution artifact.
4. This is the only conditionally-compatible license in the audit. It deserves a standing guard, not a blanket dismissal.

**Evidence:** The certifi section explicitly states the condition under which MPL-2.0 would be triggered: "If an Apache 2.0 project uses certifi as a dependency without modifying the certifi source files." The response to this identified condition is "No action required." This creates a governance gap: the condition is documented but no control exists to enforce it.

**Impact:** If certifi is vendored or modified in the future (e.g., to bundle a custom CA bundle for enterprise deployment), and the project has already completed the MIT-to-Apache 2.0 migration relying on this audit's clean PASS, there will be no standing process to catch the MPL-2.0 obligation.

**Dimension:** Actionability

**Response Required:** Add a "Standing Constraint" or "Ongoing Obligation" section to the audit covering certifi's MPL-2.0 condition. The constraint must be: documented in a DECISION or ADR, and either enforced via CI or noted as a manual review requirement for any future certifi vendoring or bundling.

**Acceptance Criteria:** The audit must not issue "No action required" for a conditionally-compatible license without a mechanism to enforce the condition. Either add a standing constraint record, or reference an ADR/decision that formalizes the "do not modify certifi" rule.

---

### DA-006: Build-Time Dependency (hatchling) Excluded Without Documented Justification [MAJOR]

**Claim Challenged:** "Scope: All 53 packages in the active uv virtual environment (direct runtime + dev + all transitives)" (Methodology)

**Counter-Argument:** The audit explicitly scopes to the uv virtual environment. pyproject.toml declares `[build-system] requires = ["hatchling"]`. hatchling is fetched and executed at `uv build` time to produce the distribution artifact. It is not present in the runtime venv. The audit makes no mention of hatchling, its license, or the decision to exclude build-time dependencies from scope.

This exclusion is consequential because:
1. For OSS distribution on PyPI, the build process (and thus the build tool's license) is part of the distribution chain. If hatchling or one of its dependencies carried a GPL license, it could -- depending on the legal theory applied -- affect the artifact produced.
2. The audit's scope statement says "direct runtime + dev + all transitives" but does not say "excluding build-system dependencies." The omission is undocumented.
3. hatchling (MIT-licensed) is almost certainly safe, but the audit's job is to verify, not to assume.

**Evidence:** pyproject.toml line 63: `[build-system] requires = ["hatchling"]`. `uv run python3 -c "import importlib.metadata; importlib.metadata.version('hatchling')"` raises `PackageNotFoundError` -- hatchling is not in the venv. The audit methodology says "all 53 packages in the active uv virtual environment" without addressing this gap.

**Impact:** A complete OSS release governance audit must either verify build-time dependencies or explicitly document a scope exclusion with justification. The current audit does neither.

**Dimension:** Completeness

**Response Required:** Either (a) verify hatchling's license and any build-time transitive deps (e.g., by running pip-licenses in the build-time environment), or (b) explicitly document the scope exclusion for build-system dependencies with a justification for why build-time deps are out of scope for Apache 2.0 license compatibility.

**Acceptance Criteria:** The methodology section must explicitly state whether build-system dependencies are in or out of scope, and provide justification either way.

---

## Recommendations

### P0 -- Critical (MUST resolve before acceptance)

*No Critical findings were identified. No DA-NNN finding rises to the level of invalidating the core PASS verdict itself.*

### P1 -- Major (SHOULD resolve; require justification if not)

| ID | Finding | Action | Acceptance Criteria |
|----|---------|--------|---------------------|
| DA-001 | Summary/Verdict count inconsistency | Reconcile the "8 dev/test, 41 transitive" vs. "6 dev, 43 transitive" breakdown. Add any missing packages to their tables or correct the counts. | Summary and Verdict must agree on the same categorical breakdown. |
| DA-002 | pip-licenses coverage gap | Document supplemental verification method for pip, pip-licenses, prettytable, wcwidth: tool, field queried, output. | Each of the 4 packages must have a cited, reproducible verification source. |
| DA-003 | Absent deps verified by assertion | Perform version-specific license lookups for mypy, pytest-archon, pytest-bdd, pytest-cov at the versions declared in pyproject.toml. | Each package must have a verifiable license record with a cited source. |
| DA-004 | MPL-2.0 compatibility legal chain | Remove GPL-transitivity inference. State the correct basis (file-level copyleft, unmodified use pattern). Cite primary source. | Legal reasoning for certifi must be self-consistent and cite OSI/FSF/MPL-2.0 text. |
| DA-005 | certifi modification -- no control | Add a standing constraint or ADR referencing the MPL-2.0 condition for certifi. | An ADR or standing constraint record must formalize the "do not modify certifi" obligation. |
| DA-006 | hatchling not audited | Verify hatchling + build deps OR explicitly document and justify scope exclusion. | Methodology must address build-system dependencies explicitly. |

### P2 -- Minor (MAY resolve; acknowledgment sufficient)

| ID | Finding | Action |
|----|---------|--------|
| DA-007 | Pre-commit hook repo deps | Acknowledge scope exclusion for pre-commit isolated envs with brief rationale (e.g., developer tooling only, not distributed). |
| DA-008 | `jsonschema[test]` phantom extra | Correct pyproject.toml to use a valid extra (e.g., `jsonschema[format]` or plain `jsonschema`), or acknowledge that the phantom extra is silently harmless. |
| DA-009 | Transitive table row count (42) vs. stated count (43) | Reconcile. Either add the missing package row or correct the stated count to 42. |
| DA-010 | wcwidth license via License-Expression field | Document which field was queried for wcwidth (and the other 3 supplemental packages) to confirm the MIT determination is from the authoritative field. |

---

## Scoring Impact

Impact assessed against the pre-revision audit deliverable.

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-006: hatchling (build-time dep) not audited and exclusion undocumented. DA-007: pre-commit hook repo deps not audited. DA-008: phantom extra in pyproject.toml not flagged. Three distinct coverage gaps identified. |
| Internal Consistency | 0.20 | Negative | DA-001: Summary and Verdict disagree on dev/transitive count categorical breakdown (8/41 vs. 6/43). DA-009: Transitive table row count (42) contradicts stated count (43). Two independent internal contradictions in the same document. |
| Methodological Rigor | 0.20 | Negative | DA-002: Primary tool (pip-licenses) missed 4 packages; supplemental method undocumented. DA-004: MPL-2.0 legal reasoning relies on a fallacious GPL-transitivity inference. Two methodological flaws of differing severity. |
| Evidence Quality | 0.15 | Negative | DA-003: 4 declared-but-absent deps verified only by the word "known." DA-010: wcwidth license determination method not documented. Asserted facts without cited verification. |
| Actionability | 0.15 | Negative | DA-005: Identified MPL-2.0 condition (certifi must not be modified) receives "No action required" without a standing control. The audit surfaces a real risk and then fails to specify a durable response. |
| Traceability | 0.10 | Neutral | The audit traces correctly to pyproject.toml, pip-licenses output, and the specific packages. Package-level sourcing is adequate. Finding DA-002 slightly reduces traceability for the 4 supplementally-verified packages, but the bulk of the trace chain is intact. |

**Net assessment:** 5 of 6 dimensions have negative impact from DA findings. Completeness, Internal Consistency, and Methodological Rigor carry the heaviest weight (0.20 each) and all three are negatively impacted. The REVISE band (0.85-0.91) is the likely post-DA scoring zone before revision. Targeted revision on the 6 P1 findings is expected to restore the audit to the PASS band (>=0.92).

---

## Overall Assessment

**Does the PASS verdict survive the Devil's Advocate challenge?**

**Conditionally -- the PASS verdict is not invalidated but is insufficiently supported in its current form.**

No Critical finding was identified that would overturn the conclusion that all discovered dependencies are Apache 2.0 compatible. The fundamental claim -- that the Jerry Framework has no GPL, AGPL, or SSPL dependencies -- is almost certainly correct. The 49 packages verified by pip-licenses are all demonstrably permissive, and the certifi MPL-2.0 and regex CNRI-Python situations are genuine edge cases with plausible (if imperfectly argued) resolution paths.

However, the PASS verdict rests on an audit that has six Major findings:

1. It miscounts or miscategorizes packages between its own sections (DA-001, DA-009).
2. It used a primary tool that missed 4 packages and documented the recovery method inadequately (DA-002).
3. It verified 4 declared dependencies with an assertion rather than a lookup (DA-003).
4. Its legal reasoning for the most important compatibility question (certifi/MPL-2.0) contains a logical non-sequitur (DA-004).
5. It identified a real ongoing compliance condition (certifi modification risk) and dismissed it without a durable control (DA-005).
6. It excluded build-time dependencies without documenting the exclusion or justifying the scope decision (DA-006).

For a C4 governance audit supporting an irreversible license migration, the PASS verdict requires not just a correct answer but a demonstrably sound methodology. The current audit does not meet that bar. The verdict should be recorded as PASS-PROVISIONAL pending revision of the six P1 findings. If all P1 findings are addressed with evidence rather than assertion, the revised audit is expected to support a clean PASS.

**Strongest single argument against PASS:** The four packages verified only as "known to be MIT-licensed" (mypy, pytest-archon, pytest-bdd, pytest-cov) are declared runtime-reachable dependencies (a `uv sync --extra test` installs them). The audit provides no version-specific license verification for any of them. If any one carries a problematic sub-dependency in the declared version, the audit would not have caught it, and this PASS verdict would have permitted the license migration based on an unverified assumption. For a governance decision that is, by the project's own framework, classified as C4 (irreversible), this level of epistemic confidence is insufficient.

---

*Generated by adv-executor agent -- S-002 Devil's Advocate strategy -- QG-1 execution -- 2026-02-17*
*Deliverable: EN-934 audit-executor-dep-audit.md | Workflow: feat015-licmig-20260217-001*
