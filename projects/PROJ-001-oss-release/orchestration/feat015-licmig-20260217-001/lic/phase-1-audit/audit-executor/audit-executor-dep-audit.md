# EN-934: Dependency License Compatibility Audit Report

> **Agent:** audit-executor
> **Date:** 2026-02-17
> **Revision:** 3 (QG-1 iteration 2 revision — addressing S-014 evidence gaps, S-002 DA-011/DA-012/DA-013/DA-014/DA-015/DA-016/DA-017)
> **Workflow:** feat015-licmig-20260217-001
> **Enabler:** EN-934
> **Verdict:** PASS

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | High-level findings and verdict |
| [Direct Dependencies](#direct-dependencies) | Main runtime dependencies from pyproject.toml |
| [Dev Dependencies](#dev-dependencies) | Development-only dependencies |
| [Declared but Uninstalled Dependencies](#declared-but-uninstalled-dependencies) | Deps in pyproject.toml not in current venv |
| [Transitive Dependencies](#transitive-dependencies) | Indirect dependencies pulled in transitively |
| [Supplemental Verification](#supplemental-verification) | Packages not captured by pip-licenses |
| [License Notes](#license-notes) | MPL-2.0, CNRI-Python, and OR-expression analysis |
| [Standing Constraints](#standing-constraints) | Ongoing license obligations requiring monitoring |
| [Incompatible Dependencies](#incompatible-dependencies) | GPL/AGPL/SSPL/LGPL findings |
| [Verdict](#verdict) | Final PASS/BLOCK determination |
| [Methodology](#methodology) | Audit approach, tooling, and scope decisions |
| [Re-Audit Conditions](#re-audit-conditions) | Triggers for future re-audit |
| [Traceability](#traceability) | Links to QG-1, EN-934, WORKTRACKER, orchestration plan |

---

## Summary

A full dependency license audit was conducted across all 52 third-party packages in the Jerry Framework environment: 4 direct runtime, 6 direct dev (from `[dependency-groups].dev`), and 42 transitive. The project package itself (`jerry 0.2.0`, currently MIT, subject of migration) was excluded from scope as it is the artifact being relicensed.

The primary audit tool was `pip-licenses 5.5.1` via `uv run`, which returned 49 packages (48 third-party + jerry). pip-licenses does not report 4 packages that are part of its own dependency chain or the base environment: pip, pip-licenses, prettytable, and wcwidth. These 4 packages were verified via `importlib.metadata` — see [Supplemental Verification](#supplemental-verification) for documented evidence. Note: these 4 packages are included in their respective category tables below (pip-licenses in [Dev Dependencies](#dev-dependencies); pip, prettytable, wcwidth in [Transitive Dependencies](#transitive-dependencies)), but their license data was obtained via importlib.metadata rather than pip-licenses. The raw pip-licenses JSON output is preserved as an audit artifact at [`pip-licenses-output.json`](pip-licenses-output.json) in this directory.

Four packages declared in `pyproject.toml` optional extras but not installed in the current environment (mypy, pytest-archon, pytest-bdd, pytest-cov) were verified independently via PyPI JSON API — see [Declared but Uninstalled Dependencies](#declared-but-uninstalled-dependencies).

All 52 installed third-party packages and all 4 declared-but-uninstalled packages carry permissive or compatible licenses. Two edge-case licenses required detailed analysis: `certifi` (MPL-2.0) and `regex` (Apache-2.0 AND CNRI-Python). One disjunctive license expression required acknowledgment: `packaging` (Apache-2.0 OR BSD-2-Clause). No GPL, AGPL, SSPL, LGPL, or other incompatible copyleft licenses were found in any category.

One **standing constraint** was identified: certifi's MPL-2.0 license is conditionally compatible — the condition (no modification of certifi source files) must be maintained. See [Standing Constraints](#standing-constraints).

---

## Direct Dependencies

Dependencies declared under `[project].dependencies` in `pyproject.toml`.

| Package | Version | License | SPDX ID | Compatible? |
|---------|---------|---------|---------|-------------|
| filelock | 3.20.3 | Unlicense | Unlicense | Yes |
| jsonschema | 4.26.0 | MIT | MIT | Yes |
| tiktoken | 0.12.0 | MIT License | MIT | Yes |
| webvtt-py | 0.5.1 | MIT License | MIT | Yes |

**Note on jsonschema extras:** `pyproject.toml` declares `jsonschema[test]>=4.26.0`. The `[test]` extra does not exist in jsonschema's current metadata (available extras: `format`, `format-nongpl`). uv silently resolves this to core jsonschema without error. The audit covers the installed package: core jsonschema 4.26.0, MIT-licensed. The phantom extra is harmless but should be corrected in pyproject.toml (change to `jsonschema>=4.26.0`).

---

## Dev Dependencies

Dependencies installed from `[dependency-groups].dev` in `pyproject.toml`.

| Package | Version | License | SPDX ID | Compatible? |
|---------|---------|---------|---------|-------------|
| pip-audit | 2.10.0 | Apache Software License | Apache-2.0 | Yes |
| pip-licenses | 5.5.1 | MIT | MIT | Yes |
| pre-commit | 4.5.1 | MIT | MIT | Yes |
| pyright | 1.1.408 | MIT | MIT | Yes |
| pytest | 9.0.2 | MIT | MIT | Yes |
| ruff | 0.14.14 | MIT License | MIT | Yes |

**Note:** pip-licenses does not appear in its own output (self-exclusion). Its license was verified via `importlib.metadata` — see [Supplemental Verification](#supplemental-verification). It is listed here because it is declared in `[dependency-groups].dev`.

---

## Declared but Uninstalled Dependencies

The following 4 packages are declared in `[project.optional-dependencies]` in `pyproject.toml` but are not installed in the current `uv` virtual environment. They were verified independently via the PyPI JSON API at the **specific version resolved by `uv.lock`** (not the current latest version), using `https://pypi.org/pypi/{package}/{version}/json`.

| Package | Constraint | uv.lock Version | PyPI License | SPDX ID | Verification Source | Compatible? |
|---------|-----------|-----------------|--------------|---------|---------------------|-------------|
| mypy | >=1.8.0 | 1.19.1 | MIT | MIT | [PyPI: mypy/1.19.1](https://pypi.org/project/mypy/1.19.1/) — Classifier: `License :: OSI Approved :: MIT License` | Yes |
| pytest-archon | >=0.0.6 | 0.0.7 | Apache Software License | Apache-2.0 | [PyPI: pytest-archon/0.0.7](https://pypi.org/project/pytest-archon/0.0.7/) — Classifier: `License :: OSI Approved :: Apache Software License` | Yes |
| pytest-bdd | >=8.0.0 | 8.1.0 | MIT | MIT | [PyPI: pytest-bdd/8.1.0](https://pypi.org/project/pytest-bdd/8.1.0/) — Classifier: `License :: OSI Approved :: MIT License` | Yes |
| pytest-cov | >=4.0.0 | 7.0.0 | MIT | MIT | [PyPI: pytest-cov/7.0.0](https://pypi.org/project/pytest-cov/7.0.0/) — License-Expression: `MIT`; Classifier: `License :: OSI Approved :: MIT License` | Yes |

**Scope limitation:** This table verifies the **top-level package license only**. The transitive dependencies of these 4 packages (e.g., `mypy-extensions`, `coverage`, `gherkin-official`) are not audited here because they are not installed in the current environment. A full transitive audit of these optional dependency surfaces should be performed when these packages are first installed — see [Re-Audit Conditions](#re-audit-conditions) Item 4.

**Note:** These packages will be installed when a contributor runs `uv sync --extra dev` or `uv sync --extra test`. Their top-level licenses are compatible with Apache 2.0. A re-audit should be triggered if any of these packages are upgraded to a new major version — see [Re-Audit Conditions](#re-audit-conditions).

---

## Transitive Dependencies

All remaining installed packages that are not direct runtime, dev, or project packages. Total: 42 packages.

| Package | Version | License | SPDX ID | Compatible? |
|---------|---------|---------|---------|-------------|
| attrs | 25.4.0 | MIT | MIT | Yes |
| boolean.py | 5.0 | BSD-2-Clause | BSD-2-Clause | Yes |
| CacheControl | 0.14.4 | Apache-2.0 | Apache-2.0 | Yes |
| certifi | 2026.1.4 | Mozilla Public License 2.0 (MPL 2.0) | MPL-2.0 | Yes (conditional — see [License Notes](#certifi--mpl-20-mozilla-public-license-20) and [Standing Constraints](#standing-constraints)) |
| cfgv | 3.5.0 | MIT | MIT | Yes |
| charset-normalizer | 3.4.4 | MIT | MIT | Yes |
| cyclonedx-python-lib | 11.6.0 | Apache Software License | Apache-2.0 | Yes |
| defusedxml | 0.7.1 | Python Software Foundation License | PSF-2.0 | Yes |
| distlib | 0.4.0 | Python Software Foundation License | PSF-2.0 | Yes |
| identify | 2.6.16 | MIT | MIT | Yes |
| idna | 3.11 | BSD-3-Clause | BSD-3-Clause | Yes |
| iniconfig | 2.3.0 | MIT | MIT | Yes |
| jsonschema-specifications | 2025.9.1 | MIT | MIT | Yes |
| license-expression | 30.4.4 | Apache-2.0 | Apache-2.0 | Yes |
| markdown-it-py | 4.0.0 | MIT License | MIT | Yes |
| mdurl | 0.1.2 | MIT License | MIT | Yes |
| msgpack | 1.1.2 | Apache-2.0 | Apache-2.0 | Yes |
| nodeenv | 1.10.0 | BSD License | BSD-3-Clause | Yes |
| packageurl-python | 0.17.6 | MIT License | MIT | Yes |
| packaging | 26.0 | Apache-2.0 OR BSD-2-Clause | Apache-2.0 OR BSD-2-Clause | Yes (see [License Notes](#packaging--apache-20-or-bsd-2-clause)) |
| pip | 26.0 | MIT | MIT | Yes |
| pip-api | 0.0.34 | Apache Software License | Apache-2.0 | Yes |
| pip-requirements-parser | 32.0.1 | MIT | MIT | Yes |
| platformdirs | 4.5.1 | MIT | MIT | Yes |
| pluggy | 1.6.0 | MIT License | MIT | Yes |
| prettytable | 3.17.0 | BSD-3-Clause | BSD-3-Clause | Yes |
| py-serializable | 2.1.0 | Apache Software License | Apache-2.0 | Yes |
| Pygments | 2.19.2 | BSD License | BSD-2-Clause | Yes |
| pyparsing | 3.3.2 | MIT | MIT | Yes |
| PyYAML | 6.0.3 | MIT License | MIT | Yes |
| referencing | 0.37.0 | MIT | MIT | Yes |
| regex | 2026.1.15 | Apache-2.0 AND CNRI-Python | Apache-2.0 AND CNRI-Python | Yes (see [License Notes](#regex--apache-20-and-cnri-python)) |
| requests | 2.32.5 | Apache Software License | Apache-2.0 | Yes |
| rich | 14.3.2 | MIT License | MIT | Yes |
| rpds-py | 0.30.0 | MIT | MIT | Yes |
| sortedcontainers | 2.4.0 | Apache Software License | Apache-2.0 | Yes |
| tomli | 2.4.0 | MIT | MIT | Yes |
| tomli_w | 1.2.0 | MIT License | MIT | Yes |
| typing_extensions | 4.15.0 | PSF-2.0 | PSF-2.0 | Yes |
| urllib3 | 2.6.3 | MIT | MIT | Yes |
| virtualenv | 20.36.1 | MIT | MIT | Yes |
| wcwidth | 0.6.0 | MIT | MIT | Yes |

---

## Supplemental Verification

`pip-licenses 5.5.1` returned 49 packages. `pip list` returned 53 packages. The 4-package gap consists of packages that pip-licenses does not report on itself: pip, pip-licenses, prettytable, and wcwidth (pip-licenses' own dependency chain plus pip itself). These 4 packages appear in their respective category tables above (pip-licenses in [Dev Dependencies](#dev-dependencies); pip, prettytable, wcwidth in [Transitive Dependencies](#transitive-dependencies)), but their license data was obtained via `importlib.metadata` rather than pip-licenses, using the `License-Expression` field (PEP 639):

| Package | Version | `License` Field | `License-Expression` Field | Determined SPDX | Method | Raw Output |
|---------|---------|-----------------|---------------------------|-----------------|--------|------------|
| pip | 26.0 | `None` | `'MIT'` | MIT | `importlib.metadata.metadata('pip').get('License-Expression')` | `'MIT'` |
| pip-licenses | 5.5.1 | `None` | `'MIT'` | MIT | `importlib.metadata.metadata('pip-licenses').get('License-Expression')` | `'MIT'` |
| prettytable | 3.17.0 | `None` | `'BSD-3-Clause'` | BSD-3-Clause | `importlib.metadata.metadata('prettytable').get('License-Expression')` | `'BSD-3-Clause'` |
| wcwidth | 0.6.0 | `None` | `'MIT'` | MIT | `importlib.metadata.metadata('wcwidth').get('License-Expression')` | `'MIT'` |

**Note on field selection:** For all 4 packages, the `License` metadata field returns `None` (confirmed via `importlib.metadata.metadata(pkg).get('License')` returning `'N/A'`). The `License-Expression` field (standardized in PEP 639, adopted 2024) returns the SPDX identifier shown in the "Raw Output" column above. This is the authoritative field for modern Python packages. All 4 packages are well-established ecosystem packages with long-standing permissive licenses.

**Note on double-listing:** These 4 packages are listed in both their categorical tables (Dev/Transitive) and in this Supplemental Verification section. The categorical tables classify packages by declaration source; this section documents the alternative verification method used because pip-licenses does not report these packages. There is no double-counting — the total of 52 third-party packages includes these 4 exactly once each.

**Note on jerry:** The `jerry` package (0.2.0, MIT License) appears in the pip-licenses output as the 49th package. It is excluded from this audit scope because it is the project being migrated from MIT to Apache 2.0.

---

## License Notes

### certifi — MPL-2.0 (Mozilla Public License 2.0)

**Status: Conditionally compatible with Apache 2.0 distribution.**

MPL-2.0 is a file-level weak copyleft license. The full license text is available at [https://www.mozilla.org/en-US/MPL/2.0/](https://www.mozilla.org/en-US/MPL/2.0/). The compatibility basis:

- **MPL-2.0 Section 1.6** ([license text](https://www.mozilla.org/en-US/MPL/2.0/)) defines "Covered Software" as the specific source files distributed under MPL-2.0. Copyleft obligations apply only to those files, not to the incorporating project.
- **MPL-2.0 Section 3.3 ("Distribution of a Larger Work")** ([license text](https://www.mozilla.org/en-US/MPL/2.0/)) permits MPL-2.0-licensed files to be distributed as part of a "Larger Work" under different license terms (including Apache 2.0), provided the MPL-licensed files themselves remain available under MPL-2.0 terms.
- The Jerry Framework uses `certifi` as an **unmodified transitive dependency** (installed via `requests`). No certifi source files are modified, vendored, or bundled. Under this use pattern, the MPL-2.0 copyleft provision is not triggered on the incorporating project.
- The [OSI license compatibility analysis](https://opensource.org/license/mpl-2-0) and [FSF license list](https://www.gnu.org/licenses/license-list.html#MPL-2.0) both recognize MPL-2.0 as a free software license compatible with Apache 2.0 in this use pattern (unmodified dependency, file-level separation).
- `certifi` (version 2026.1.4) does not include an Exhibit B "Incompatible With Secondary Licenses" notice, confirming it permits secondary license use. Verified by inspecting certifi's LICENSE file at [GitHub: certifi/python-certifi LICENSE](https://github.com/certifi/python-certifi/blob/master/LICENSE) — the file contains only the standard MPL-2.0 header with no Exhibit B addendum.

**Standing constraint:** The compatibility is conditional on certifi files remaining unmodified. See [Standing Constraints](#standing-constraints) for the ongoing obligation.

### regex — Apache-2.0 AND CNRI-Python

**Status: Compatible with Apache 2.0 distribution.**

The `regex` package carries a compound license expression: `Apache-2.0 AND CNRI-Python`.

- The Apache-2.0 portion is directly compatible with the Jerry Framework's target license.
- CNRI-Python is the "Corporation for National Research Initiatives" Python license, a historical permissive license originating from early Python interpreter releases. It is [OSI-approved](https://opensource.org/license/cnri-python) and carries attribution requirements but no copyleft provisions.
- The Python Software Foundation License (PSF), which superseded CNRI-Python for modern Python releases, is itself explicitly compatible with Apache 2.0.
- The `AND` compound means both licenses apply simultaneously to different portions of the `regex` package. Both are permissive. There are no conflicting obligations between Apache-2.0 and CNRI-Python.

**No action required.** Both license components are permissive and compatible with Apache 2.0.

### packaging — Apache-2.0 OR BSD-2-Clause

**Status: Compatible with Apache 2.0 distribution.**

The `packaging` package carries a disjunctive SPDX expression: `Apache-2.0 OR BSD-2-Clause`. The `OR` operator means either license may be chosen by the recipient. Both Apache-2.0 and BSD-2-Clause are permissive licenses compatible with Apache 2.0 distribution. Under either choice, no compatibility issue arises.

**No action required.**

---

## Standing Constraints

### SC-001: certifi MPL-2.0 — Do Not Modify or Vendor

**Condition:** The `certifi` package (MPL-2.0) is compatible with Apache 2.0 **only** when certifi source files remain unmodified. If certifi files are modified, vendored, forked, or bundled directly into the distribution artifact, MPL-2.0 copyleft obligations would be triggered, requiring the modified files to remain under MPL-2.0 terms.

**Required controls:**

1. **Policy:** Do not vendor, fork, or modify certifi source files. If a custom CA bundle is needed, use certifi's documented API (`certifi.where()`) rather than modifying its files.
2. **Monitoring:** This constraint should be re-evaluated if certifi is ever vendored or if the project's dependency installation pattern changes (e.g., bundling dependencies into a single artifact).
3. **Documentation:** This constraint is recorded here and should be referenced in any future license compliance review.

**Trigger for escalation:** If a future requirement necessitates modifying certifi files, escalate to a license compliance review before proceeding. The modification would require the affected files to carry MPL-2.0 headers and remain distributable under MPL-2.0 terms.

---

## Incompatible Dependencies

**None found.**

No packages carrying GPL, AGPL, SSPL, LGPL, EUPL, CC-BY-SA, or other non-permissive copyleft licenses were identified in any of the following categories:

- 52 installed third-party packages (4 runtime + 6 dev + 42 transitive)
- 4 declared-but-uninstalled packages (verified via PyPI)
- Build-system dependency (`hatchling` — MIT, see [Methodology](#methodology))

Specifically: **zero LGPL packages** are present in the dependency tree. The Methodology section lists LGPL as "Conditionally Compatible," but this classification was not exercised — no LGPL packages were found.

---

## Verdict

**PASS (installed packages)**: All 52 installed third-party packages (4 direct runtime, 6 direct dev, 42 transitive) carry licenses compatible with Apache 2.0 distribution. The build-system dependency (hatchling) is MIT-licensed. No GPL, AGPL, SSPL, LGPL, or other incompatible copyleft licenses are present among installed packages.

**PASS (declared-but-uninstalled, top-level only)**: All 4 declared-but-uninstalled packages (mypy 1.19.1, pytest-archon 0.0.7, pytest-bdd 8.1.0, pytest-cov 7.0.0) were independently verified as compatible at their uv.lock-resolved versions via PyPI JSON API. **Scope limitation:** This verification covers top-level package licenses only; the transitive dependencies of these 4 optional packages are not audited. A full transitive audit should be performed when these packages are first installed — see [Re-Audit Conditions](#re-audit-conditions) Item 4.

The two edge-case licenses (MPL-2.0 for `certifi`, Apache-2.0 AND CNRI-Python for `regex`) and one disjunctive expression (`packaging`'s Apache-2.0 OR BSD-2-Clause) are all compatible under the analyses documented in [License Notes](#license-notes).

One standing constraint was identified: certifi's MPL-2.0 compatibility is conditional on its source files remaining unmodified — see [Standing Constraints](#standing-constraints).

The Jerry Framework may proceed with the MIT-to-Apache 2.0 license migration without any dependency license blockers, subject to: (1) the standing constraint on certifi (SC-001), and (2) performing a transitive audit of optional dependency surfaces when first installed.

---

## Methodology

- **Primary tool:** `pip-licenses 5.5.1` via `uv run pip-licenses --format=json --with-urls`
  - Returned 49 packages (48 third-party + jerry project). Raw JSON output preserved as audit artifact: [`pip-licenses-output.json`](pip-licenses-output.json).
- **Supplemental verification:** `importlib.metadata` `License-Expression` field (PEP 639) for 4 packages not captured by pip-licenses (pip, pip-licenses, prettytable, wcwidth). See [Supplemental Verification](#supplemental-verification) for per-package documented evidence.
- **Declared-but-uninstalled verification:** PyPI JSON API (`https://pypi.org/pypi/{package}/{version}/json`) for 4 packages declared in `[project.optional-dependencies]` but not installed. Each package was verified at the **specific version resolved by `uv.lock`**, not the current latest version. See [Declared but Uninstalled Dependencies](#declared-but-uninstalled-dependencies) for per-package evidence with version-specific PyPI URLs. **Scope limitation:** Top-level licenses only; transitive dependencies of optional packages are not audited.
- **Classification standard:** Apache 2.0 compatibility per OSI license categorization:
  - **Compatible:** Apache-2.0, MIT, BSD (any clause), ISC, PSF/PSF-2.0, Unlicense, CC0, Zlib, WTFPL
  - **Conditionally Compatible (used as library, unmodified):** MPL-2.0, LGPL
  - **Incompatible:** GPL-2.0, GPL-3.0, AGPL-3.0, SSPL, CC-BY-SA
- **Scope:** All 52 third-party packages in the active uv virtual environment (direct runtime + dev + all transitives). The project package (`jerry 0.2.0`) was excluded as it is the artifact being relicensed.
- **Environment reproducibility:** The scanned environment is defined by `uv.lock` in the project root (last modified at git commit `1c108b4`, audit performed at commit `1fea04c`). Running `uv sync` from a clean state reproduces the same package set. The `pip list` count of 53 packages (52 third-party + jerry) matches the uv.lock resolved set. Any subsequent changes to uv.lock require re-audit per [Re-Audit Conditions](#re-audit-conditions) Item 2.
- **Build-system dependencies (scope exclusion):** `hatchling` is declared in `[build-system].requires` in `pyproject.toml`. Build-system dependencies are installed in an isolated build environment by uv/pip at `uv build` time and are **not** present in the runtime virtual environment. They are excluded from this audit's primary scope because: (a) build tools are not distributed with the package artifact (Python wheels/sdists do not bundle build backends), (b) they do not impose license obligations on the built artifact (this is consistent with the [REUSE Specification](https://reuse.software/spec/) treatment of build tools as non-distributed components), and (c) their license applies only to the build process itself. This exclusion is a project-level policy decision specific to Python's source/wheel distribution model where build backends run in isolation. For completeness: hatchling is MIT-licensed (verified via [GitHub: pypa/hatch LICENSE.txt](https://github.com/pypa/hatch/blob/master/backend/LICENSE.txt)).
- **Pre-commit hook dependencies (scope exclusion):** Pre-commit fetches and installs isolated environments from external repositories (`pre-commit/pre-commit-hooks`, `astral-sh/ruff-pre-commit`, `commitizen-tools/commitizen`). These are developer tooling environments, not distributed with the package, and do not impose license obligations on the project artifact. They are excluded from audit scope.
- **Source data:** `pyproject.toml` (repository root)

---

## Re-Audit Conditions

This audit should be re-executed when any of the following conditions occur:

1. **New dependency added:** Any addition to `[project].dependencies`, `[project.optional-dependencies]`, or `[dependency-groups]` in `pyproject.toml`.
2. **uv.lock updated:** Any change to the resolved dependency set (e.g., after `uv lock` or `uv add`).
3. **Major version upgrade:** Any dependency upgraded to a new major version (licenses can change across major releases).
4. **Absent deps installed:** When `mypy`, `pytest-archon`, `pytest-bdd`, or `pytest-cov` are installed into the active environment, their transitive dependencies should be audited.
5. **certifi vendored or modified:** Any vendoring, forking, or modification of certifi source files triggers the standing constraint in [SC-001](#sc-001-certifi-mpl-20--do-not-modify-or-vendor).
6. **Build system change:** If the build backend changes from hatchling to another tool.

**Remediation guidance for future incompatible findings:** If a future re-audit identifies a GPL, AGPL, or SSPL dependency, the standard resolution paths are: (a) remove the dependency, (b) find a permissively-licensed alternative, or (c) apply a license exception with explicit legal sign-off and documentation in an ADR.

---

## Traceability

| Reference | Path / ID |
|-----------|-----------|
| **Quality Gate** | QG-1 (Phase 1 — Dependency Audit), defined in `ORCHESTRATION.yaml` `quality_gates.qg-1` |
| **Enabler** | [EN-934](../../work/EPIC-001-oss-release/FEAT-015-license-migration/enablers/EN-934-dependency-license-audit.md) — Dependency License Compatibility Audit |
| **EN-934 Requirements** | All direct deps audited, all transitive deps audited, compatibility matrix produced, zero incompatible deps found OR replacement plan documented, pip-audit security scan passes |
| **Feature** | [FEAT-015](../../work/EPIC-001-oss-release/FEAT-015-license-migration/FEAT-015-license-migration.md) — License Migration (MIT to Apache 2.0) |
| **WORKTRACKER** | `projects/PROJ-001-oss-release/WORKTRACKER.md` — EN-934 entry |
| **Orchestration Plan** | `projects/PROJ-001-oss-release/ORCHESTRATION_PLAN.md` — Phase 1 definition |
| **Orchestration State** | `projects/PROJ-001-oss-release/ORCHESTRATION.yaml` — `pipelines.lic.phases[0]` |
| **Workflow ID** | `feat015-licmig-20260217-001` |
| **Agent** | `audit-executor` |
| **Revision History** | Rev 1: Initial draft (QG-1 scored 0.825 REJECTED). Rev 2: Addressed all iter 1 findings (scored 0.916 REVISE). Rev 3: Targeted evidence fixes (DA-011 through DA-017, S-014 gaps). |
| **Audit Artifacts** | [`pip-licenses-output.json`](pip-licenses-output.json) — raw pip-licenses JSON output at audit time |
| **Git State** | uv.lock at commit `1c108b4`; audit performed at commit `1fea04c` |

---

*Generated by audit-executor agent for orchestration workflow feat015-licmig-20260217-001*
*Revision 3 — addressing QG-1 iteration 2 findings (S-014: 0.916, S-007: 0.98, S-002: ~0.892)*
