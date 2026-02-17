# Devil's Advocate Report: EN-934 Dependency License Compatibility Audit (Iteration 2)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-001-oss-release/orchestration/feat015-licmig-20260217-001/lic/phase-1-audit/audit-executor/audit-executor-dep-audit.md` (Revision 2)
**Criticality:** C4 (license migration is irreversible governance action; auto-C4 per AE rules)
**Date:** 2026-02-17
**Reviewer:** adv-executor (S-002 Devil's Advocate, Iteration 2)
**H-16 Compliance:** S-003 Steelman output not provided as prerequisite — same procedural gap as Iteration 1. H-16 non-compliance is recorded; execution proceeds under explicit task direction.
**Iteration Context:** QG-1 Iteration 2. Audit Revision 2 addresses iteration 1 findings (S-014: 0.825 REJECTED, S-002: 6 Major/4 Minor, S-007: 1 Major/3 Minor).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Role Assumption](#role-assumption) | Adversarial mandate and scope |
| [Prior Finding Resolution](#prior-finding-resolution) | Status of each DA-NNN finding from iteration 1 |
| [Assumption Inventory](#assumption-inventory) | Updated explicit and implicit assumptions |
| [Findings Table](#findings-table) | All findings (new and residual) with severity |
| [Finding Details](#finding-details) | Expanded Critical and Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized action list |
| [Scoring Impact Assessment](#scoring-impact-assessment) | Dimension-level impact for revised audit |
| [Overall Assessment](#overall-assessment) | Does the PASS verdict survive iteration 2 challenge? |

---

## Role Assumption

**Deliverable under challenge:** audit-executor-dep-audit.md (Revision 2), EN-934 Dependency License Compatibility Audit Report.
**Criticality:** C4 — irreversible governance decision (MIT-to-Apache 2.0 license migration). Any audit defect that permits an incompatible dependency to pass undetected cannot be undone after the migration is executed and the OSS release is published.
**Mandate:** Determine whether the PASS verdict in Revision 2 is adequately supported. Specifically: (1) verify that all 10 prior findings were substantively resolved, (2) identify any new issues introduced by the revision, and (3) construct the strongest remaining argument against the PASS verdict.
**Revision 2 claims:** The audit now covers 52 third-party packages, added a Supplemental Verification section, a Declared but Uninstalled Dependencies section, Standing Constraints, and explicit Methodology scope exclusions for build-system and pre-commit hook dependencies.

---

## Prior Finding Resolution

Each finding from the S-002 Iteration 1 report is evaluated against Revision 2.

| ID | Severity | Finding (Iter 1) | Resolution Status | Notes |
|----|----------|------------------|-------------------|-------|
| DA-001-20260217T1200 | Major | Summary/Verdict count inconsistency (8/41 vs 6/43) | RESOLVED | Both Summary and Verdict now consistently state 4+6+42=52. Tables corroborate. |
| DA-002-20260217T1200 | Major | pip-licenses coverage gap — 4 packages via undocumented supplemental method | PARTIALLY RESOLVED | Supplemental Verification section added with per-package table. Fields queried documented. However, pip-licenses appears in BOTH Dev Dependencies and Supplemental Verification — a new internal contradiction. |
| DA-003-20260217T1200 | Major | Absent deps verified by assertion ("known MIT"), no evidence | RESOLVED | Declared but Uninstalled section added with per-package PyPI JSON API citations and classifiers. Verification method cited per package. |
| DA-004-20260217T1200 | Major | MPL-2.0 compatibility argument relies on fallacious GPL transitivity | RESOLVED | Legal reasoning replaced with correct MPL-2.0 Section 3.3 "Distribution of a Larger Work" argument, with OSI/FSF citations. GPIO-transitivity chain removed. |
| DA-005-20260217T1200 | Major | certifi "No action required" without standing constraint | RESOLVED | Standing Constraints section added (SC-001) with explicit policy, monitoring requirement, and escalation trigger. |
| DA-006-20260217T1200 | Major | hatchling build dep excluded without documented justification | RESOLVED | Methodology section now explicitly documents build-system scope exclusion with three-part justification. hatchling MIT license noted via GitHub citation. |
| DA-007-20260217T1200 | Minor | Pre-commit hook repo deps not audited | RESOLVED | Pre-commit scope exclusion documented in Methodology with rationale. |
| DA-008-20260217T1200 | Minor | jsonschema[test] phantom extra | OPEN | pyproject.toml still declares `jsonschema[test]>=4.26.0`. Revision 2 audit lists jsonschema 4.26.0 in Direct Dependencies without acknowledging the `[test]` phantom extra or correcting the declaration. DA-008 was not addressed. |
| DA-009-20260217T1200 | Minor | Transitive table row count (42) vs stated count (43) | RESOLVED | Total revised to 52 packages (42 transitive). Table count (42 rows) now matches stated count (42). |
| DA-010-20260217T1200 | Minor | wcwidth License-Expression field accuracy | RESOLVED | Supplemental Verification table now documents `License-Expression` field query per package, including wcwidth. |

**Resolution Summary:** 8 RESOLVED, 1 PARTIALLY RESOLVED (DA-002), 1 OPEN (DA-008).

---

## Assumption Inventory

### Explicit Assumptions (Revision 2)

| Assumption | Location | Challenge |
|------------|----------|-----------|
| pip-licenses returned 49 packages (48 third-party + jerry), and 4 additional packages were not captured | Summary, Supplemental Verification | pip-licenses is listed both as a Dev Dependency (audited by pip-licenses) and in Supplemental Verification (not captured by pip-licenses). These are mutually exclusive claims. |
| certifi does not include an Exhibit B "Incompatible With Secondary Licenses" notice | License Notes, certifi | The audit asserts this as a fact, but no verification method or source is cited. A reader cannot confirm this without independently inspecting certifi's distribution files. |
| The virtual environment count of 52 third-party packages is stable and reproducible | Summary, Methodology | The audit confirms the environment is defined by uv.lock, but does not state which uv.lock hash or commit was scanned, leaving reproducibility unanchored. |
| Build-system dependencies (hatchling) impose no license obligations on the built artifact | Methodology | This is a legal assumption, not a verified fact. The scope exclusion cites three rationale points, but the legal theory (build tools cannot impose obligations on artifacts) is stated without authority citation. |
| Declared-but-uninstalled packages will carry the same license at the version uv resolves | Declared but Uninstalled | PyPI checks were performed against the current version, not the declared constraint floor (`>=1.5.0` for mypy, `>=0.0.6` for pytest-archon, etc.). The resolved version in uv.lock may differ from the current PyPI version checked. |

### Implicit Assumptions (Revision 2)

| Assumption | Evidence | Challenge |
|------------|----------|-----------|
| pip-licenses 5.5.1 correctly identifies all packages it reports | Never stated | If pip-licenses misreads a license field (e.g., reporting the metadata `License` classifier rather than the newer `License-Expression` field), an incorrect SPDX ID would propagate into the tables without detection. No independent cross-check validates pip-licenses output accuracy per-package. |
| The 4 declared-but-uninstalled packages (mypy, pytest-archon, pytest-bdd, pytest-cov) have no transitive dependencies with problematic licenses | Declared but Uninstalled | The section only verifies the top-level package license. A compatibility-breaking sub-dependency (e.g., a GPL helper library) in any of these packages would not be caught. |
| The Exhibit B absence from certifi is permanent | License Notes | Certifi's upstream maintainers could add an Exhibit B notice in a future release. No re-audit trigger for certifi upstream changes is defined beyond generic major-version upgrade monitoring. |
| Pre-commit hook repositories carry permissive licenses sufficient for developer use | Methodology (scope exclusion) | The scope exclusion for pre-commit hook repos is justified by "developer tooling, not distributed." This is asserted without verifying the actual licenses of the three hook repos referenced. |

---

## Findings Table

| ID | Severity | Finding | Section | Affected Dimension |
|----|----------|---------|---------|-------------------|
| DA-011-20260217T1400 | Major | pip-licenses double-counted: appears in Dev Dependencies AND Supplemental Verification | Supplemental Verification, Dev Dependencies | Internal Consistency |
| DA-012-20260217T1400 | Major | Declared-but-uninstalled verification checks current PyPI version, not uv.lock-resolved version | Declared but Uninstalled | Evidence Quality |
| DA-013-20260217T1400 | Major | Absent packages: no transitive dependency coverage | Declared but Uninstalled | Completeness |
| DA-014-20260217T1400 | Minor | Exhibit B claim for certifi is unverified and uncited | License Notes | Evidence Quality |
| DA-015-20260217T1400 | Minor | jsonschema[test] phantom extra remains in pyproject.toml and unaddressed in audit (DA-008 OPEN) | Direct Dependencies | Completeness |
| DA-016-20260217T1400 | Minor | Build-system scope exclusion legal basis asserted without authority citation | Methodology | Methodological Rigor |
| DA-017-20260217T1400 | Minor | uv.lock is cited as reproducibility anchor but specific lock file hash/commit not documented | Methodology | Traceability |

---

## Finding Details

### DA-011: pip-licenses Listed in Both Dev Dependencies and Supplemental Verification [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Dev Dependencies table (line "pip-licenses \| 5.5.1 \| MIT \| MIT \| Yes") and Supplemental Verification table ("pip-licenses \| 5.5.1 \| N/A \| MIT \| MIT \| importlib.metadata...") |
| **Strategy Step** | Step 2 (Document and Challenge Assumptions), Step 3 (Construct Counter-Arguments — Logical flaws lens) |

**Evidence:**
The Dev Dependencies section lists `pip-licenses 5.5.1` as a dev dependency verified by the normal pip-licenses audit. The Summary states: "The primary audit tool was `pip-licenses 5.5.1` via `uv run`, which returned 49 packages (48 third-party + jerry). Four additional packages not captured by pip-licenses (pip, pip-licenses, prettytable, wcwidth) were verified via `importlib.metadata`." The Supplemental Verification section lists `pip-licenses 5.5.1` with method `importlib.metadata.metadata('pip-licenses').get('License-Expression')`.

**Analysis:**
These two representations are mutually exclusive. If pip-licenses is a dev dependency that pip-licenses itself reports, it would appear in the "49 packages" pip-licenses returned, and its license is captured by the primary tool. But the Summary says pip-licenses is one of the "4 additional packages NOT captured by pip-licenses." This is a logical contradiction: pip-licenses either IS or IS NOT in its own output. If pip-licenses 5.5.1 is NOT in its own output (which is plausible, as some tools exclude themselves), then it should NOT appear in the Dev Dependencies table as a pip-licenses-captured entry. If it IS in its own output, then it should NOT appear in Supplemental Verification.

The effect: pip-licenses 5.5.1 is being counted once in Dev Dependencies (as one of the 6 dev packages) AND once in Supplemental Verification (as one of the 4 gap packages). If the Supplemental Verification packages are ADDITIONAL to the 49 pip-licenses reported, then pip-licenses appears in both groups — raising the actual total above 52. If pip-licenses is in the Supplemental Verification group and NOT in the pip-licenses output, then one of the 6 Dev Dependency rows has no primary tool verification, contradicting the methodology claim.

**Impact:**
This introduces a new internal consistency defect in Revision 2 — exactly the type of defect (DA-001) that Revision 2 was supposed to resolve. The mathematical foundation of the 52-package count and the 4-package supplemental method description may both be inaccurate. A reader cannot reconstruct which packages were verified by which method from the document as written.

**Recommendation:**
Clarify whether pip-licenses appears in its own output. If it does NOT (self-exclusion): remove pip-licenses from the Dev Dependencies table and document it only in Supplemental Verification; update the 6 dev dep count to 5 and the total accordingly. If it DOES appear in pip-licenses output: remove it from Supplemental Verification; the 4-package gap does not include pip-licenses.

**Acceptance Criteria:** pip-licenses 5.5.1 must appear in exactly one verification section. The total package count, categorical breakdown, and supplemental verification list must be internally consistent.

---

### DA-012: Declared-but-Uninstalled Version Mismatch — Current PyPI Version vs. uv.lock-Resolved Version [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Declared but Uninstalled Dependencies |
| **Strategy Step** | Step 2 (Unstated Assumptions), Step 3 (Counter-Arguments — Unstated assumptions lens) |

**Evidence:**
The Declared but Uninstalled Dependencies section lists mypy with "Declared Version: >=1.5.0" and verifies via "PyPI: mypy — Classifier: `License :: OSI Approved :: MIT License`." The same pattern applies to pytest-archon (`>=0.0.6`), pytest-bdd (`>=8.0.0`), pytest-cov (`>=4.0.0`). The verification sources link to `https://pypi.org/project/{package}/` — the current version of each package on PyPI.

**Analysis:**
The declared version constraints are floor bounds, not pinned versions. The PyPI link points to the latest version. These are not equivalent:

1. `mypy >=1.5.0` means uv will resolve a specific version based on the lock file. The uv.lock file contains the actual resolved version. The PyPI check at `https://pypi.org/project/mypy/` returns metadata for the CURRENT latest version (e.g., 1.15.x as of this audit date), not for the specific version that would be installed from the lock.
2. If `pytest-archon >=0.0.6` resolves to version 0.0.6 in uv.lock (the floor), but the PyPI check is for version 0.0.8 (latest), a license change between 0.0.6 and 0.0.8 would be invisible to this audit.
3. The audit's own Re-Audit Conditions section (Item 3) states "Major version upgrade: Any dependency upgraded to a new major version (licenses can change across major releases)." This acknowledges license change risk across versions — yet the Declared but Uninstalled verification ignores the version-pinning problem for the very packages most likely to undergo version drift (uninstalled optional dependencies).

**Impact:**
For a C4 governance audit, "compatible at the current PyPI version" is not equivalent to "compatible at the version that will be installed." If `pytest-archon` or `pytest-bdd` changed licenses between the locked version and the current PyPI version, this audit would have checked the wrong version. The PASS verdict for declared-but-uninstalled packages is therefore version-anchored to the wrong point in time.

**Recommendation:**
For each declared-but-uninstalled package: (a) check the uv.lock file for the resolved version pin; (b) verify the license at that specific version using `https://pypi.org/pypi/{package}/{version}/json`; (c) cite the specific version in the table. If the package is not in uv.lock (because it requires `uv sync --extra`), state that explicitly and note whether a separate lock for the extra exists.

**Acceptance Criteria:** Each declared-but-uninstalled package must be verified at the version that uv would install, not at the current PyPI version. The table must cite specific version numbers, not constraint bounds.

---

### DA-013: Absent Packages — No Transitive Dependency Coverage [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Declared but Uninstalled Dependencies |
| **Strategy Step** | Step 2 (Implicit Assumptions), Step 3 (Unaddressed Risks lens) |

**Evidence:**
The Declared but Uninstalled section verifies only the top-level package license for each of the 4 absent packages: mypy, pytest-archon, pytest-bdd, pytest-cov. The methodology states these packages were verified via PyPI JSON API. The Re-Audit Conditions section states (Item 4): "When `mypy`, `pytest-archon`, `pytest-bdd`, or `pytest-cov` are installed into the active environment, their transitive dependencies should be audited."

**Analysis:**
The DA-003 finding in iteration 1 was resolved by adding per-package PyPI citations. However, DA-003's acceptance criteria stated: "Each absent package must have a verifiable license record citing the specific version and a reproducible verification method." This is now met at the top level. But a deeper problem remains unaddressed: each of these 4 packages has its own transitive dependency tree.

- `mypy >=1.5.0` has known transitive dependencies including `mypy-extensions`, `typing_extensions`, and potentially others. `mypy-extensions` has historically been MIT, but this is not verified.
- `pytest-bdd >=8.0.0` has transitive dependencies including `gherkin-official` and `mako` in some configurations.
- `pytest-cov >=4.0.0` depends on `coverage[toml]`.
- `pytest-archon >=0.0.6` is a smaller package, but its transitive deps are unchecked.

The Re-Audit Conditions section acknowledges this gap exists ("when installed, their transitive dependencies should be audited") but frames it as a future action, not a current limitation. For a C4 governance audit that is certifying the Jerry Framework is safe to relicense, declaring 4 optional dependency trees entirely unchecked — while simultaneously acknowledging they need checking — is insufficient. The PASS verdict covers only the 52 currently-installed packages, but the framework's optional dependency surface is not covered.

**Impact:**
A developer who runs `uv sync --extra dev` or `uv sync --extra test` will install these 4 packages and their transitive dependencies. If any transitive dependency carries GPL-2.0, AGPL, or SSPL, the PASS verdict will have been issued for an incomplete scope. The audit's PASS applies to a partial view of the dependency tree.

**Recommendation:**
Either: (a) install the absent packages in a separate clean environment, run pip-licenses against them, and include their transitive audit results; OR (b) explicitly bound the PASS verdict to "currently installed packages only" and add a separate verdict for the optional dependency surface (PENDING until installed and audited). The current framing implies a complete PASS when the coverage is partial.

**Acceptance Criteria:** The PASS verdict must either cover all dependency surfaces (installed + optional) or be explicitly scoped to "installed packages only" with a separate PENDING status for the optional surfaces. The Verdict section must not imply complete coverage when 4 optional packages and their transitive deps are unaudited.

---

### DA-014: Exhibit B Absence Claim for certifi — Unverified and Uncited [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | License Notes — certifi |
| **Strategy Step** | Step 3 (Evidence Quality and Contradicting Evidence lens) |

**Evidence:**
The revised certifi analysis states: "certifi does not include an Exhibit B 'Incompatible With Secondary Licenses' notice, confirming it permits secondary license use." This is a new factual assertion added in Revision 2. The assertion is made without: (a) citing a source where Exhibit B presence/absence was checked, (b) providing the URL to certifi's distribution metadata or source repository, or (c) noting which version of certifi was inspected.

**Analysis:**
Under MPL-2.0, Exhibit B is an optional addendum that copyright holders may attach to indicate the software is "Incompatible With Secondary Licenses." Its absence matters because it determines whether certifi can be combined with Apache 2.0 code. The claim "certifi does not include an Exhibit B notice" is a falsifiable, version-specific fact. If a future version of certifi adds Exhibit B, this claim would become incorrect. More immediately, the current claim is unsupported — no reader can verify it from the document without independently inspecting certifi's files.

The citation for this claim should reference certifi's `METADATA` file, `LICENSE` file, or source repository. Given that certifi is a well-maintained package with transparent governance, this verification is straightforward, but it was not performed and documented here.

**Impact:**
Minor — the Exhibit B absence is almost certainly correct for current certifi (2026.1.4). However, an uncited factual claim in a C4 governance audit, even if correct, reduces the audit's evidentiary quality and cannot be relied upon by future auditors without re-verification.

**Recommendation:**
Add a citation for the Exhibit B check: URL to certifi's `LICENSE` file on GitHub or PyPI, with the specific certifi version (2026.1.4) noted.

**Acceptance Criteria:** The Exhibit B absence claim must reference a specific, inspectable source (e.g., `https://github.com/certifi/python-certifi/blob/main/LICENSE` or the certifi 2026.1.4 METADATA file).

---

### DA-015: jsonschema[test] Phantom Extra Remains Unaddressed (DA-008 OPEN) [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Direct Dependencies, Methodology |
| **Strategy Step** | Step 2 (Implicit Assumptions — declaration imprecision) |

**Evidence:**
pyproject.toml declares `jsonschema[test]>=4.26.0` as a direct runtime dependency (verified via Grep: `pyproject.toml`, line 32). The `[test]` extra does not exist in jsonschema's package metadata (available extras: `format`, `format-nongpl`). Revision 2 lists jsonschema 4.26.0 in the Direct Dependencies table without any note about the phantom extra. DA-008 in iteration 1 was classified as Minor and called for either correcting pyproject.toml or acknowledging that the phantom extra is harmless. Neither action was taken.

**Analysis:**
The finding was Minor in iteration 1 because the end state (only core jsonschema installed) is benign. But the iteration 2 audit was supposed to address all P2 (Minor) findings. DA-008 acceptance criteria stated: "Correct pyproject.toml to use a valid extra (e.g., `jsonschema[format]` or plain `jsonschema`), or acknowledge that the phantom extra is silently harmless." The revision did neither. The phantom extra remains in pyproject.toml, undetected by the audit.

**Impact:**
Low. The phantom extra is harmless in practice. However, it represents a pattern of pyproject.toml imprecision that the audit claimed to address. An OSS release audit that notes dependency declaration errors in one place should be consistent. The omission also means DA-008 remains on the open findings list, which could affect the overall PASS assessment if scored against the full finding set.

**Recommendation:**
Either correct pyproject.toml to remove `[test]` (change to `jsonschema>=4.26.0`), or add a note to the Direct Dependencies section: "jsonschema is declared as `jsonschema[test]>=4.26.0` in pyproject.toml. The `[test]` extra does not exist in jsonschema's current metadata; uv silently resolves to core jsonschema. The audit covers the installed package (core jsonschema 4.26.0, MIT-licensed)."

**Acceptance Criteria:** Acknowledgment of the phantom extra status in either the audit document or pyproject.toml correction. DA-008 must not remain silently open.

---

### DA-016: Build-System Scope Exclusion Legal Basis Asserted Without Authority Citation [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Methodology — Build-system dependencies (scope exclusion) |
| **Strategy Step** | Step 3 (Unstated Assumptions, Evidence Quality lens) |

**Evidence:**
The Methodology section states: "Build-system dependencies are installed in an isolated build environment by uv/pip at `uv build` time and are **not** present in the runtime virtual environment. They are excluded from this audit's primary scope because: (a) build tools are not distributed with the package artifact, (b) they do not impose license obligations on the built artifact, and (c) their license applies only to the build process itself."

**Analysis:**
Point (b) — "they do not impose license obligations on the built artifact" — is a legal claim, not a fact established by tool output. This is the core legal theory that justifies excluding hatchling from the audit. It is stated as a given, but the legal relationship between build-tool licenses and artifact licenses is nuanced and has been actively debated in OSS governance circles. For example: if hatchling compiled or statically linked code into the artifact (it does not, but the audit doesn't establish this), the legal analysis would differ.

The justification in point (a) — build tools are not distributed with the artifact — is generally correct for Python packages, which are source or wheel distributions. But for a C4 governance audit, "generally correct" should be replaced with "verified for this specific packaging configuration." The audit does note hatchling is MIT-licensed (mitigating the practical risk), but the scope exclusion justification is asserted without citing legal authority or published guidance (e.g., SPDX best practices, OSI guidance, FOSS Outreach guidelines).

**Impact:**
Low in this specific case because hatchling is MIT-licensed and the practical risk is negligible. However, as a precedent for future audits, an ungrounded scope exclusion rationale creates a template for incorrect exclusions in higher-risk scenarios.

**Recommendation:**
Add a parenthetical citation for point (b): e.g., "(per SPDX specification: build dependencies in isolated environments are not part of the distributed artifact's license obligations — see REUSE Specification §3.3 or equivalent)." Alternatively, note that the exclusion is specific to Python wheel/sdist packaging where build tools run in isolation and are not compiled into the artifact.

**Acceptance Criteria:** The legal basis for build-system scope exclusion must cite a published standard or guidance document, or explicitly note it as a project-level policy decision acknowledged without external authority.

---

### DA-017: uv.lock Cited as Reproducibility Anchor Without Hash or Commit Reference [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Methodology — Environment reproducibility |
| **Strategy Step** | Step 2 (Explicit Assumptions — environment stability) |

**Evidence:**
The Methodology section states: "The scanned environment is defined by `uv.lock` in the project root. Running `uv sync` from a clean state reproduces the same package set." The `pip list` count of 53 packages (sic — this is still "53" in Methodology but "52 third-party + jerry" in Summary) is cited.

**Analysis:**
The Methodology section retains "53 packages" in the environment reproducibility statement ("The `pip list` count of 53 packages (52 third-party + jerry) matches the uv.lock resolved set"). This is internally consistent with the 52 third-party count. However, the audit does not anchor the audit to a specific commit, uv.lock hash, or timestamp of the lock file. Without this:

1. A future re-reader cannot verify that the uv.lock at the time of audit matches the current uv.lock, because uv.lock may have been updated since the audit.
2. The "running uv sync reproduces the same package set" claim is only true if uv.lock has not changed.

This is a traceability gap: the audit document does not record which version of uv.lock was the ground truth for this scan.

**Impact:**
Low in the short term but meaningful for an audit that is intended to serve as a permanent governance record. If uv.lock changes between this audit and the actual release, the audit will have been performed against a different environment than the one being released.

**Recommendation:**
Add a line to Methodology: "Audit performed against uv.lock at git commit [short hash] / dated [date]. Any subsequent changes to uv.lock require re-audit per Re-Audit Conditions Item 2."

**Acceptance Criteria:** The specific uv.lock state (git commit hash or file hash) that was scanned must be cited, or a statement that the audit was performed in the same session as the git commit containing this report and uv.lock has not changed.

---

## Recommendations

### P0 — Critical (MUST resolve before acceptance)

*No Critical findings in Iteration 2. No finding rises to the level of invalidating the core PASS verdict.*

### P1 — Major (SHOULD resolve; require justification if not)

| ID | Finding | Action | Acceptance Criteria |
|----|---------|--------|---------------------|
| DA-011 | pip-licenses double-counted in Dev Dependencies AND Supplemental Verification | Determine whether pip-licenses appears in its own output. Remove from one section accordingly. Correct total count if needed. | pip-licenses appears in exactly one verification section. Total count is internally consistent. |
| DA-012 | Declared-but-uninstalled version mismatch — current PyPI vs. uv.lock-resolved version | Check uv.lock for resolved versions of mypy, pytest-archon, pytest-bdd, pytest-cov. Verify license at that specific version via `https://pypi.org/pypi/{package}/{version}/json`. | Each absent package verified at the specific version uv would install, not at PyPI current. |
| DA-013 | Absent packages — no transitive dependency coverage | Either install absent packages in a test environment and run pip-licenses, or explicitly bound PASS to "installed packages only" with PENDING status for optional surfaces. | PASS verdict is not overstated. Optional dependency coverage gap is either closed or explicitly scoped. |

### P2 — Minor (MAY resolve; acknowledgment sufficient)

| ID | Finding | Action |
|----|---------|--------|
| DA-014 | Exhibit B claim for certifi — unverified | Add citation to certifi 2026.1.4 LICENSE or source repository confirming Exhibit B absence. |
| DA-015 | jsonschema[test] phantom extra (DA-008 OPEN) | Correct pyproject.toml OR add explicit acknowledgment to audit. Either resolution closes this finding. |
| DA-016 | Build-system scope exclusion legal basis uncited | Add authority citation or policy statement for the claim that build tools impose no obligations on artifacts. |
| DA-017 | uv.lock not anchored to specific commit | Add git commit hash or lock file date to Methodology. |

---

## Scoring Impact Assessment

Impact assessed against Revision 2 relative to pre-revision state.

### Improvements Introduced by Revision 2

| Prior Finding | Was | After Revision |
|---------------|-----|----------------|
| Internal Consistency (DA-001, DA-009) | Negative (0.78) | Positive — main count contradiction resolved |
| Methodological Rigor (DA-002, DA-004) | Negative (0.83) | Positive — supplemental method documented, GPL-transitivity removed |
| Evidence Quality (DA-003, DA-010) | Negative (0.80) | Positive — absent packages cited, wcwidth field documented |
| Actionability (DA-005) | Negative (0.88) | Positive — SC-001 standing constraint added |
| Completeness (DA-006, DA-007) | Negative (0.82) | Positive — scope exclusions documented |

### Residual Impact from Iteration 2 Findings

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-013: 4 optional packages' transitive deps unaudited. PASS verdict implied as complete when coverage is partial. DA-015 (Minor): phantom extra still unaddressed. |
| Internal Consistency | 0.20 | Negative | DA-011: pip-licenses appears in both Dev Dependencies and Supplemental Verification — new contradiction introduced by the revision itself. |
| Methodological Rigor | 0.20 | Slightly Negative | DA-016 (Minor): build-system exclusion rationale uncited. Residual gap from DA-002 partial resolution. |
| Evidence Quality | 0.15 | Negative | DA-012: absent package versions checked at wrong version. DA-014 (Minor): Exhibit B claim uncited. |
| Actionability | 0.15 | Neutral | SC-001 standing constraint adequately addresses the actionability gap. Re-Audit Conditions comprehensive. Verdict is clear. |
| Traceability | 0.10 | Slightly Negative | DA-017 (Minor): uv.lock not anchored to commit. Otherwise, Traceability section is substantially improved in Revision 2 with QG-1, EN-934, WORKTRACKER, orchestration plan references. |

### Score Estimate

The iteration 1 composite was 0.825 (REJECTED). Revision 2 addressed 8 of 10 prior findings. Estimated dimension improvements:

- Internal Consistency: 0.78 → ~0.88 (DA-001, DA-009 resolved; DA-011 introduces a new, smaller inconsistency — net improvement substantial)
- Completeness: 0.82 → ~0.87 (DA-006, DA-007 resolved; DA-013, DA-015 remain)
- Methodological Rigor: 0.83 → ~0.90 (DA-002 partially resolved, DA-004 resolved; DA-016 minor residual)
- Evidence Quality: 0.80 → ~0.86 (DA-003, DA-010 resolved; DA-012 introduces a new gap)
- Actionability: 0.88 → ~0.93 (DA-005 fully resolved; no new actionability gaps)
- Traceability: 0.87 → ~0.93 (Traceability section added; DA-017 minor residual)

**Estimated composite (Revision 2):**
(0.87 × 0.20) + (0.88 × 0.20) + (0.90 × 0.20) + (0.86 × 0.15) + (0.93 × 0.15) + (0.93 × 0.10)
= 0.174 + 0.176 + 0.180 + 0.129 + 0.1395 + 0.093
= **0.892**

This places Revision 2 in the **REVISE band (0.85–0.91)** — REJECTED per H-13 (threshold >= 0.92), but significantly improved from the REJECTED band (< 0.85) of Revision 1. Targeted resolution of DA-011 (Major) and DA-013 (Major) is likely sufficient to cross the 0.92 threshold.

---

## Overall Assessment

**Does the PASS verdict survive the Iteration 2 Devil's Advocate challenge?**

**Not yet — but it is materially closer. The PASS verdict remains insufficiently supported on three grounds.**

**Positive developments in Revision 2:** The six Major findings from Iteration 1 (DA-001 through DA-006) have been substantively addressed. The audit is now a significantly stronger governance document: it has a Supplemental Verification section with documented evidence per package, a Declared but Uninstalled section with PyPI citations, Standing Constraints with a formal obligation record (SC-001), explicit scope exclusions with justification, and corrected MPL-2.0 legal reasoning. The count inconsistencies that undermined trust in Iteration 1 are resolved.

**Remaining grounds against PASS:**

**1. A new internal contradiction was introduced (DA-011 — Major):** pip-licenses 5.5.1 appears in both the Dev Dependencies table (audited via pip-licenses) and the Supplemental Verification table (not captured by pip-licenses). These are contradictory claims in the same document. Revision 2 corrected the DA-001 count inconsistency but introduced a different count/verification inconsistency in the process. The remedy was not fully reconciled.

**2. The version-mismatch gap in declared-but-uninstalled verification (DA-012 — Major):** The PyPI checks for mypy, pytest-archon, pytest-bdd, and pytest-cov verify the current latest version, not the version that uv.lock would resolve. For a C4 governance audit claiming to verify "all declared dependencies," this is a methodological gap. pytest-archon in particular is a low-visibility package where version-specific license verification is non-trivial.

**3. The optional dependency tree remains unchecked (DA-013 — Major):** The Declared but Uninstalled section verifies top-level licenses only. The transitive dependencies of these 4 optional packages are explicitly acknowledged as requiring future audit but are not covered. The PASS verdict is stated as covering "All 52 installed third-party packages... and all 4 declared-but-uninstalled packages" — but the latter is only partially true (top-level only, not transitives). The Re-Audit Conditions section acknowledges this gap but frames it as a future responsibility rather than a present limitation of the current PASS verdict.

**Strongest Remaining Argument Against PASS:**

The PASS verdict states: "All 4 declared-but-uninstalled packages (mypy, pytest-archon, pytest-bdd, pytest-cov) were independently verified as compatible via PyPI metadata." This claim, while improved from "known to be MIT-licensed," contains two unresolved defects: (1) the PyPI metadata checked is for the current version, not the uv.lock-resolved version; and (2) only the top-level package is verified, not the transitive dependencies that would be installed alongside them. For a C4 governance audit certifying an irreversible OSS license migration, a PASS that covers the optional dependency surface only at the top level and only at an unanchored version is insufficient. If pytest-archon 0.0.6 (the floor version) pulls in a GPL helper library, or if mypy's current PyPI version differs from the locked version by a license change, the PASS verdict will have been issued incorrectly. These are low-probability events, but C4 classification demands high-confidence verification, not low-probability arguments.

**Revision 3 Path to Clean PASS:**

Resolution of DA-011 (pip-licenses double-counting) and DA-013 (transitive deps for optional packages, or explicit scope re-bounding of PASS verdict) is required before this audit can support a clean PASS at the 0.92 quality gate. DA-012 (version anchoring for absent packages) should also be addressed. The four Minor findings (DA-014 through DA-017) are improvements but do not individually block PASS.

---

## Execution Statistics

- **Total New Findings (Iteration 2):** 7
- **Critical:** 0
- **Major:** 3 (DA-011, DA-012, DA-013)
- **Minor:** 4 (DA-014, DA-015, DA-016, DA-017)
- **Prior Findings Resolved:** 8 of 10 (RESOLVED: DA-001, DA-003, DA-004, DA-005, DA-006, DA-007, DA-009, DA-010)
- **Prior Findings Partially Resolved:** 1 (DA-002)
- **Prior Findings Open:** 1 (DA-008)
- **Estimated Composite Score (Revision 2):** ~0.892 (REVISE band — REJECTED per H-13)
- **Protocol Steps Completed:** 5 of 5

---

*Generated by adv-executor agent — S-002 Devil's Advocate strategy — QG-1 Iteration 2 — 2026-02-17*
*Deliverable: EN-934 audit-executor-dep-audit.md Revision 2 | Workflow: feat015-licmig-20260217-001*
*Execution ID: 20260217T1400*
