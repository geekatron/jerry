# BUG-009: Research Section — Broken Icon Navigation, Poor Catalog Naming, No Link Validation

> **Type:** bug
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-19
> **Parent:** EPIC-001
> **Owner:** --
> **Found In:** 0.2.3
> **Fix Version:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Children (Tasks)](#children-tasks) | Task breakdown for fix |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

Three interrelated defects in the FEAT-027 Research Section deliverable degrade the public documentation site UX and reveal a gap in build-time validation:

1. **Broken icon navigation**: `:octicons-*:` icon references render as literal text (e.g., `:octicons-arrow-right-24:`) because the `pymdownx.emoji` extension with `material` icon sets is not configured in `mkdocs.yml`. This affects grid card navigation links and external link icons across all 11 research pages.

2. **Poor catalog naming**: The landing page (`docs/research/index.md`) links to `bug008-research-catalog.md` — an internal planning artifact with "bug" in the filename. Public visitors see a "bug" reference where they expect curated research content. The overview should link directly to the source research artifacts rather than an internal catalog index.

3. **No automated link validation**: `mkdocs build --strict` catches some broken cross-file links but does NOT validate octicon rendering failures, same-page anchor resolution, or external link liveness. There is no test infrastructure to prevent these regressions.

**Key Details:**
- **Symptom:** Grid card links display as `:octicons-arrow-right-24: Strategy Catalog` instead of icon + text; "Full catalog" link reveals internal `bug008-` filename
- **Frequency:** Every page load on all 11 research pages
- **Workaround:** Links are technically clickable despite missing icons; catalog content is accessible despite poor naming

---

## Reproduction Steps

### Prerequisites

- MkDocs site built with `uv run mkdocs build --strict`
- Site served with `uv run mkdocs serve`

### Steps to Reproduce

1. Navigate to `http://localhost:8000/research/`
2. Observe grid card links — icon syntax renders as literal text `:octicons-arrow-right-24:`
3. Scroll to bottom — "Full research catalog on GitHub" link URL contains `bug008-research-catalog.md`
4. Click any anchor link in the Research Domains table — verify if it scrolls to the correct section
5. Inspect any research sub-page (e.g., `/research/single-vs-multi-agent/`) — observe `:octicons-link-external-16:` renders as text

### Expected Result

- Grid card links show arrow icons with clickable text
- External links show link-external icons
- Catalog link uses a professional filename without "bug" prefix
- All anchor links scroll to correct sections

### Actual Result

- Icons render as literal `:octicons-*:` text strings
- Catalog link exposes internal `bug008-` naming
- Links are functionally clickable but visually broken

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS (Darwin 24.6.0) |
| **Runtime** | MkDocs + Material for MkDocs |
| **Application Version** | Jerry 0.2.3 |
| **Configuration** | `mkdocs.yml` — missing `pymdownx.emoji` extension |
| **Deployment** | jerry.geekatron.org (GitHub Pages) |

---

## Root Cause Analysis

### Investigation Summary

Built the MkDocs site and inspected the rendered HTML for `research/index.html`. Confirmed:
- Grid cards markup IS rendered (Material theme grid cards work)
- Octicons references appear as literal text — the `pymdownx.emoji` extension with `emoji_index: !!python/name:material.extensions.emoji.twemoji` and `emoji_generator: !!python/name:material.extensions.emoji.to_svg` is NOT configured
- Anchor links in the Research Domains table DO resolve correctly in the HTML (IDs match)
- The catalog file is genuinely named `bug008-research-catalog.md` because it was created during BUG-008 investigation work

### Root Cause

1. **Icon rendering**: `mkdocs.yml` `markdown_extensions` section does not include `pymdownx.emoji` with Material icon sets. The Material for MkDocs documentation requires this for `:octicons-*:` and `:material-*:` icon syntax.

2. **Poor naming**: The research catalog was created as a BUG-008 deliverable (`bug008-research-catalog.md`) and never renamed for public consumption. The landing page links to this internal artifact instead of providing direct navigation.

3. **No validation**: `mkdocs build --strict` validates cross-file links and missing nav entries but does NOT validate: (a) whether icon syntax resolves to actual icons, (b) same-page anchor integrity at the HTML level, (c) external link liveness.

### Contributing Factors

- FEAT-027 quality gate (EN-962) scored 0.93 but did not include icon rendering validation — the S-014 scorer evaluated markdown content, not rendered HTML output
- No CI/CD pipeline test for MkDocs rendering quality beyond `mkdocs build --strict`

---

## Children (Tasks)

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Configure `pymdownx.emoji`, `attr_list`, `md_in_html` extensions in mkdocs.yml | done | 1 |
| TASK-002 | Rename `bug008-research-catalog.md` to `research-catalog.md` and update all references | done | 1 |
| TASK-003 | Fix landing page overview links — catalog links updated with clean filename | done | 2 |
| TASK-004 | Add automated MkDocs link and icon validation test script | done | 3 |

---

## Acceptance Criteria

### Fix Verification

- [x] AC-1: All `:octicons-*:` icons render as SVG/HTML icons (not literal text) across all 11 research pages
- [x] AC-2: No public-facing links reference files with "bug" in the filename
- [x] AC-3: Landing page overview links navigate correctly to their target sections
- [x] AC-4: Automated validation script catches broken icons, broken anchors, and broken links
- [x] AC-5: `mkdocs build --strict` continues to pass with 0 warnings on research pages
- [x] AC-6: Validation script integrated into pre-commit or CI so regressions fail the build

### Quality Checklist

- [x] Regression tests added
- [x] Existing tests still passing
- [x] No new issues introduced
- [x] Documentation updated (if applicable)

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../../EPIC-001-oss-release/EPIC-001-oss-release.md)

### Related Items

- **Causing Change:** FEAT-027 (Research Section for Public Documentation Site) — introduced the research pages with octicon syntax
- **Related Feature:** [FEAT-027](../FEAT-027-research-docs-section/FEAT-027-research-docs-section.md) — the feature that introduced the defective pages
- **Related Enabler:** EN-961 (MkDocs Integration) — should have caught the missing extension
- **Related Enabler:** EN-962 (Quality Gate) — scorer evaluated markdown not rendered HTML

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Created. Three interrelated defects: broken icon rendering (missing pymdownx.emoji), poor catalog naming (bug008 prefix), no automated link validation. Found during user review of FEAT-027 PR #33. |
| 2026-02-19 | Claude | done | Fixed all 4 tasks: (1) Added pymdownx.emoji + attr_list + md_in_html extensions to mkdocs.yml, (2) renamed bug008-research-catalog.md to research-catalog.md, (3) updated all catalog references, (4) added e2e test suite (3 tests: icon rendering, link quality, anchor integrity). AC-6 deferred — CI integration requires pre-commit hook setup. |
| 2026-02-19 | Claude | done | /adversary C3 review (S-010, S-003, S-002, S-004, S-007, S-012, S-013, S-014). Iter1: 0.56 REJECTED — 1 CRITICAL (missing pytest markers + mkdocs not in pip CI deps), 6 MAJOR findings. Fixed: (a) added `pytestmark = [pytest.mark.e2e, pytest.mark.subprocess]`, (b) registered markers in pyproject.toml, (c) `build_site` fixture now cleans `site/` before build, (d) icon regex excludes `<code>`/`<pre>` blocks to prevent false positives. Note: `docs.yml` version skew (9.6.7 vs 9.7.2) is pre-existing, not introduced by BUG-009. |
| 2026-02-19 | Claude | done | /adversary C3 Iter2: 0.70 REJECTED — `test-uv` CI job uses `-m "not llm"` which does not exclude `subprocess`-marked tests, and `uv sync --extra test` lacks mkdocs-material (only in `dev` group). Fixed: added `and not subprocess` to test-uv marker filter in ci.yml (both coverage and skip-coverage paths). |
| 2026-02-19 | Claude | done | /adversary C3 Iter3: 0.80 REJECTED — no CI execution path for e2e tests (BLOCKING-001), AC-6 deferred without tracked follow-on (BLOCKING-002). Fixed: added MkDocs e2e validation step to `cli-integration` CI job (already has mkdocs-material via `--extra dev`). AC-6 now complete — all 6 ACs met. |

---
