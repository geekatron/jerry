# FEAT-024: Public Documentation Site — jerry.geekatron.org

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.3
CREATED: 2026-02-17 (Claude)
PURPOSE: MkDocs Material docs site with custom domain for Jerry OSS
-->

> **Type:** feature
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-17
> **Due:** --
> **Completed:** 2026-02-19
> **Parent:** EPIC-001-oss-release
> **Owner:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Research Findings](#research-findings) | Context7 + web search results |
| [Decisions](#decisions) | Architectural choices |
| [Discoveries](#discoveries) | Findings during research |
| [Enablers](#enablers) | Implementation work items |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Progress Summary](#progress-summary) | Tracking |
| [History](#history) | Change log |

---

## Summary

Set up `jerry.geekatron.org` as the public documentation site for the Jerry Framework, powered by **MkDocs Material** and deployed to **GitHub Pages** via GitHub Actions. The domain is hosted at Namesecure (`geekatron.org`).

**Key Objectives:**
- Install and configure MkDocs Material as the documentation site generator
- Curate existing `docs/` content into a public-facing documentation site
- Create a GitHub Actions workflow for automated deployment on push to `main`
- Configure DNS (Namesecure CNAME) and GitHub Pages custom domain for `jerry.geekatron.org`
- Validate end-to-end: push to main -> build -> deploy -> live at `jerry.geekatron.org`

---

## Research Findings

> Sources: Context7 (MkDocs Material docs, GitHub docs), web search, `gh api` inspection.

### Current GitHub Pages State

| Aspect | Current Value |
|--------|---------------|
| Status | `built` (serving) |
| URL | `geekatron.github.io/jerry/` |
| Source | `main` branch, root `/` |
| Build type | `legacy` (Jekyll, but `.nojekyll` disables it) |
| Custom domain | `null` (none configured) |
| HTTPS | Enforced |
| Content | No `index.html` — raw repo files, effectively unusable |

### MkDocs Material Setup (from Context7)

**Source:** [Material for MkDocs — Creating your site](https://squidfunk.github.io/mkdocs-material/creating-your-site/)

Minimal `mkdocs.yml`:
```yaml
site_name: Jerry Framework
site_url: https://jerry.geekatron.org
theme:
  name: material
```

Bootstrap: `mkdocs new .` creates scaffold, but Jerry already has `docs/` — only need `mkdocs.yml` and `docs/index.md`.

### GitHub Actions Deployment (from Context7)

**Source:** [Material for MkDocs — Publishing your site](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)

Official recommended workflow:
```yaml
name: ci
on:
  push:
    branches:
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configure Git Credentials
        run: |
          git config user.name github-actions[bot]
          git config user.email 41898282+github-actions[bot]@users.noreply.github.com
      - uses: actions/setup-python@v5
        with:
          python-version: 3.x
      - run: echo "cache_id=$(date --utc '+%V')" >> $GITHUB_ENV
      - uses: actions/cache@v4
        with:
          key: mkdocs-material-${{ env.cache_id }}
          path: ~/.cache
          restore-keys: |
            mkdocs-material-
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force
```

`mkdocs gh-deploy --force` builds the site and pushes to `gh-pages` branch. GitHub Pages source must then be set to `gh-pages` branch.

### Custom Domain Configuration (from Context7 + GitHub Docs)

**Source:** [GitHub Docs — Managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

For subdomain (`jerry.geekatron.org`):
1. **DNS (Namesecure):** Create CNAME record: `jerry` → `geekatron.github.io`
2. **GitHub:** Settings > Pages > Custom domain > `jerry.geekatron.org` > Save
3. **CNAME file gotcha:** When using `mkdocs gh-deploy`, a `CNAME` file containing `jerry.geekatron.org` must be placed in `docs/` so it gets included in the built output. Otherwise, each deploy wipes the custom domain setting.
4. **Verification:** `dig jerry.geekatron.org +nostats +nocomments +nocmd` should show CNAME to `geekatron.github.io`
5. **HTTPS:** GitHub auto-provisions Let's Encrypt cert after DNS propagates. Enforce HTTPS in Settings.

### CNAME File Critical Detail

When MkDocs deploys via `mkdocs gh-deploy --force`, it **force-pushes** to the `gh-pages` branch. If the `CNAME` file isn't in the build output, the custom domain config gets wiped on every deploy. Solution: place `docs/CNAME` containing the bare domain `jerry.geekatron.org`. MkDocs copies all files from `docs/` to the build output.

---

## Decisions

### DEC-006: MkDocs Material over Jekyll

| Aspect | Decision |
|--------|----------|
| **ID** | DEC-006 |
| **Status** | accepted |
| **Date** | 2026-02-17 |
| **Decision** | Use MkDocs Material for documentation site, not Jekyll |
| **Rationale** | (1) Jerry is a Python project — MkDocs is Python-native, installs via `uv add`. Jekyll requires Ruby toolchain. (2) `.nojekyll` already present — Jekyll was disabled because template placeholders in `docs/` and `.context/` trigger Liquid syntax errors (BUG-007). (3) MkDocs Material is the industry standard for Python project documentation (FastAPI, Pydantic, SQLAlchemy). (4) Existing `docs/` directory with real markdown content maps directly to MkDocs structure. |
| **Impact** | tactical |
| **Alternatives rejected** | Jekyll (Ruby dep + Liquid conflicts), Sphinx (RST-focused, heavier), Docusaurus (React, overkill), Hugo (Go, not Python ecosystem) |

---

## Discoveries

### DISC-003: GitHub Pages Legacy Build State

| Aspect | Detail |
|--------|--------|
| **ID** | DISC-003 |
| **Status** | validated |
| **Impact** | high |
| **Finding** | GitHub Pages is enabled with `legacy` build type (source: `main` branch, root `/`). No `index.html` exists at root, so the site is effectively broken — visitors get raw file listings or 404. The `.nojekyll` file disables Jekyll processing but nothing replaces it. Pages must be reconfigured to use `gh-pages` branch (created by `mkdocs gh-deploy`) as the publishing source. |

### DISC-004: CNAME File Wipe on Deploy

| Aspect | Detail |
|--------|--------|
| **ID** | DISC-004 |
| **Status** | validated |
| **Impact** | high |
| **Finding** | `mkdocs gh-deploy --force` force-pushes to `gh-pages` branch. If custom domain is configured via GitHub UI but no `CNAME` file exists in `docs/`, the custom domain setting is wiped on every deploy. Mitigation: create `docs/CNAME` containing `jerry.geekatron.org` (single line, bare domain). MkDocs includes all `docs/` files in the build output. |

---

## Enablers

### Enabler Inventory

| ID | Title | Status | Priority | Effort |
|----|-------|--------|----------|--------|
| EN-946 | MkDocs Material Project Setup | pending | high | 3 |
| EN-947 | Content Curation & Landing Page | pending | high | 5 |
| EN-948 | GitHub Actions Deployment Workflow | pending | high | 3 |
| EN-949 | DNS & Custom Domain Configuration | pending | high | 2 |
| EN-950 | Validation & Go-Live | pending | high | 2 |

**Total effort:** 15 points

### EN-946: MkDocs Material Project Setup

**Goal:** Install MkDocs Material and create the base configuration.

| Task | Description | Effort |
|------|-------------|--------|
| TASK-001 | Run `uv add --dev mkdocs-material` to add dependency | 1 |
| TASK-002 | Create `mkdocs.yml` at repo root with site config (site_name, site_url, theme, nav) | 1 |
| TASK-003 | Create `docs/CNAME` file containing `jerry.geekatron.org` | 1 |
| TASK-004 | Verify `uv run mkdocs serve` renders locally at `localhost:8000` | 1 |

**Acceptance Criteria:**
- [ ] AC-1: `mkdocs-material` is in `pyproject.toml` dev dependencies
- [ ] AC-2: `mkdocs.yml` exists at repo root with Material theme configured
- [ ] AC-3: `docs/CNAME` contains `jerry.geekatron.org`
- [ ] AC-4: `uv run mkdocs serve` runs without errors and renders the site locally

### EN-947: Content Curation & Landing Page

**Goal:** Select public-facing docs and create the site landing page.

| Task | Description | Effort |
|------|-------------|--------|
| TASK-001 | Create `docs/index.md` — landing page with project overview, key features, quick links | 2 |
| TASK-002 | Audit `docs/` directory: classify each file as public/internal/exclude | 1 |
| TASK-003 | Define `nav:` structure in `mkdocs.yml` — only public-facing content | 1 |
| TASK-004 | Create/update `docs/getting-started.md` or link existing `docs/runbooks/getting-started.md` | 1 |
| TASK-005 | Review all selected docs for internal references, broken links, sensitive content | 1 |

**Content candidates (from existing `docs/`):**

| File/Dir | Public? | Notes |
|----------|---------|-------|
| `INSTALLATION.md` | Yes | Core public doc |
| `runbooks/getting-started.md` | Yes | Onboarding |
| `playbooks/problem-solving.md` | Yes | Skill usage |
| `playbooks/orchestration.md` | Yes | Skill usage |
| `playbooks/transcript.md` | Maybe | Depends on scope |
| `BOOTSTRAP.md` | Yes | Setup guide |
| `CLAUDE-MD-GUIDE.md` | Yes | Developer guide |
| `governance/` | Partial | Constitution maybe, internals no |
| `knowledge/` | No | Internal exemplars and research |
| `adrs/` | Partial | Public ADRs only |
| `schemas/` | Maybe | Reference material |
| `research/` | No | Internal |
| `analysis/` | No | Internal |

**Acceptance Criteria:**
- [ ] AC-1: `docs/index.md` exists with project overview and navigation
- [ ] AC-2: Content audit complete — each `docs/` item classified public/internal/exclude
- [ ] AC-3: `nav:` structure in `mkdocs.yml` only references public content
- [ ] AC-4: No broken internal links in public-facing docs
- [ ] AC-5: No sensitive/internal content exposed in public navigation

### EN-948: GitHub Actions Deployment Workflow

**Goal:** Automate MkDocs build and deployment to `gh-pages` branch on push to `main`.

| Task | Description | Effort |
|------|-------------|--------|
| TASK-001 | Create `.github/workflows/docs.yml` with MkDocs Material CI workflow | 1 |
| TASK-002 | Ensure workflow does NOT conflict with existing CI workflows (`ci.yml`, `version-bump.yml`) | 1 |
| TASK-003 | Test workflow in PR — verify `gh-pages` branch is created with built site | 1 |

**Workflow spec:**
- Trigger: push to `main` (paths filter on `docs/**`, `mkdocs.yml` to avoid unnecessary builds)
- Permissions: `contents: write`
- Steps: checkout -> setup-python -> cache -> install mkdocs-material -> `mkdocs gh-deploy --force`

**Acceptance Criteria:**
- [ ] AC-1: `.github/workflows/docs.yml` exists and is valid
- [ ] AC-2: Workflow triggers on push to `main` when docs or mkdocs.yml change
- [ ] AC-3: `gh-pages` branch is created/updated with built HTML site
- [ ] AC-4: No conflicts with existing CI, version-bump, or release workflows

### EN-949: DNS & Custom Domain Configuration

**Goal:** Configure Namesecure DNS and GitHub Pages custom domain.

| Task | Description | Effort |
|------|-------------|--------|
| TASK-001 | Log into Namesecure, create CNAME record: `jerry` → `geekatron.github.io` | 1 |
| TASK-002 | In GitHub repo Settings > Pages, set custom domain to `jerry.geekatron.org` | 1 |
| TASK-003 | Reconfigure GitHub Pages source from `main /` (legacy) to `gh-pages` branch | 1 |
| TASK-004 | Verify DNS propagation: `dig jerry.geekatron.org` shows CNAME to `geekatron.github.io` | 1 |
| TASK-005 | Enable "Enforce HTTPS" in GitHub Pages settings (after cert provisioning) | 1 |

**Note:** TASK-001 and TASK-002 require manual user action (Namesecure login, GitHub UI). Claude can provide exact steps but cannot execute these.

**Acceptance Criteria:**
- [ ] AC-1: CNAME record exists at Namesecure: `jerry.geekatron.org` → `geekatron.github.io`
- [ ] AC-2: GitHub Pages custom domain set to `jerry.geekatron.org`
- [ ] AC-3: GitHub Pages source is `gh-pages` branch
- [ ] AC-4: `dig jerry.geekatron.org` resolves correctly
- [ ] AC-5: HTTPS enforced, valid cert serving

### EN-950: Validation & Go-Live

**Goal:** End-to-end verification that the full pipeline works.

| Task | Description | Effort |
|------|-------------|--------|
| TASK-001 | Push a docs change to `main`, verify GitHub Actions workflow runs successfully | 1 |
| TASK-002 | Verify `jerry.geekatron.org` serves the MkDocs Material site with correct content | 1 |
| TASK-003 | Verify HTTPS is active (no mixed content warnings) | 1 |
| TASK-004 | Verify search functionality works on the live site | 1 |
| TASK-005 | Smoke test all navigation links on the live site | 1 |

**Acceptance Criteria:**
- [ ] AC-1: Push-to-main triggers docs build and deploy automatically
- [ ] AC-2: `jerry.geekatron.org` serves the Jerry documentation site
- [ ] AC-3: HTTPS active with valid certificate
- [ ] AC-4: Site search returns results
- [ ] AC-5: All navigation links resolve correctly

---

## Acceptance Criteria (Feature-Level)

- [x] AC-1: `jerry.geekatron.org` serves a MkDocs Material documentation site — MkDocs Material 9.6.7, HTTP/2 200 confirmed
- [x] AC-2: Site is automatically rebuilt and deployed on push to `main` — docs.yml workflow active (ID 235984839), latest run success
- [x] AC-3: HTTPS enforced with valid certificate — https_enforced=true, Let's Encrypt cert approved (expires 2026-05-19)
- [x] AC-4: Landing page introduces Jerry Framework with clear navigation — docs/index.md with 4-section nav (12 pages)
- [x] AC-5: Only curated public-facing content is accessible — nav curated (13 PUBLIC from 57 total), exclude_docs blocks INTERNAL dirs, strict:true
- [x] AC-6: All 5 enablers (EN-946 through EN-950) pass their acceptance criteria — 5/5 complete, all ACs verified

---

## Progress Summary

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [████████████████████] 100% (5/5 completed)           |
| Tasks:     [████████████████████] 100% (18/18 completed)         |
+------------------------------------------------------------------+
| Overall:   [████████████████████] 100%                            |
+------------------------------------------------------------------+
```

| Metric | Value |
|--------|-------|
| **Total Enablers** | 5 |
| **Completed** | 5 |
| **In Progress** | 0 |
| **Pending** | 0 |
| **Total Tasks** | 18 |
| **Total Effort** | 15 points |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Feature created. Research via Context7 (MkDocs Material, GitHub Pages docs) + web search. DEC-006 (MkDocs over Jekyll). DISC-003 (legacy build state), DISC-004 (CNAME wipe gotcha). 5 enablers (EN-946–950), 18 tasks, 15 effort points. |
| 2026-02-19 | Claude | done | **FEAT-024 COMPLETE.** Orchestration feat024-docssite-20260217-001: 4 phases, 15 agents, 3 quality gates (QG-1: 0.9340, QG-2: 0.9440, QG-3: 0.9320). All 6 ACs satisfied. 5/5 enablers complete. Site live at https://jerry.geekatron.org. |

---

<!--
RESEARCH SOURCES:
- Context7: /websites/squidfunk_github_io_mkdocs-material (4035 snippets, High reputation)
- Context7: /websites/github_en (43828 snippets, High reputation)
- MkDocs Material docs: https://squidfunk.github.io/mkdocs-material/publishing-your-site/
- MkDocs Material docs: https://squidfunk.github.io/mkdocs-material/creating-your-site/
- GitHub Docs: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- GitHub Docs: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages
- GitHub API: gh api repos/geekatron/jerry/pages (live inspection)
-->
