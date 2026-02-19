# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-001-ORCH-PLAN-FEAT024
> **Project:** PROJ-001-oss-release
> **Feature:** FEAT-024: Public Documentation Site — jerry.geekatron.org
> **Workflow ID:** `feat024-docssite-20260217-001`
> **Status:** ACTIVE
> **Version:** 1.0
> **Created:** 2026-02-17
> **Last Updated:** 2026-02-17

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#1-executive-summary) | Workflow purpose and outcome |
| [Workflow Architecture](#2-workflow-architecture) | Pipeline diagram and pattern classification |
| [Phase Definitions](#3-phase-definitions) | Per-phase agent and artifact specification |
| [Quality Gate Protocol](#4-quality-gate-protocol) | C2 adversarial review definitions |
| [Agent Registry](#5-agent-registry) | All agents across all phases |
| [State Management](#6-state-management) | Artifact paths and checkpoint strategy |
| [Execution Constraints](#7-execution-constraints) | Hard and soft constraints |
| [Success Criteria](#8-success-criteria) | Exit criteria per phase and for completion |
| [Risk Mitigations](#9-risk-mitigations) | Known risks and mitigations |
| [Resumption Context](#10-resumption-context) | Current state and next actions |

---

## 1. Executive Summary

This workflow orchestrates the implementation of FEAT-024 — the public documentation site for the Jerry Framework hosted at `jerry.geekatron.org`. The site will be powered by **MkDocs Material** and deployed to **GitHub Pages** via a GitHub Actions workflow, with DNS via a Namesecure CNAME record.

The workflow addresses five enablers:
- **EN-946:** MkDocs Material Project Setup (tool install, mkdocs.yml, docs/CNAME)
- **EN-947:** Content Curation & Landing Page (index.md, nav structure, public content audit)
- **EN-948:** GitHub Actions Deployment Workflow (docs.yml CI workflow)
- **EN-949:** DNS & Custom Domain Configuration (Namesecure CNAME + GitHub Pages reconfiguration) — **requires manual user steps**
- **EN-950:** Validation & Go-Live (E2E verification, HTTPS, search, links)

**Key Research Findings (pre-validated — do not redo):**
- MkDocs Material selected over Jekyll (DEC-006): Python-native, uv-compatible, no Liquid conflicts
- GitHub Pages currently in `legacy` build mode (main branch, root `/`, no index.html) — must migrate to `gh-pages` branch
- CNAME file gotcha (DISC-004): `mkdocs gh-deploy --force` wipes custom domain on each deploy unless `docs/CNAME` is present in the build
- DNS: Namesecure CNAME record `jerry` → `geekatron.github.io`
- Official MkDocs Material GitHub Actions workflow sourced from Context7

**Orchestration Pattern:** Sequential with parallel fan-out. EN-949 DNS portion starts immediately (propagation takes time). EN-946 foundation unblocks EN-947 and EN-948 in parallel. EN-949 GitHub Pages reconfiguration waits for EN-948 (needs gh-pages branch). EN-950 is the final integration gate.

**Current State:** Not started. All 5 enablers pending. 18 tasks, 15 effort points.

### 1.1 Workflow Identification

| Field | Value | Source |
|-------|-------|--------|
| Workflow ID | `feat024-docssite-20260217-001` | auto |
| ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | semantic-date-seq |
| Base Path | `orchestration/feat024-docssite-20260217-001/` | Dynamic |

**Artifact Output Locations:**
- Phase documents: `orchestration/feat024-docssite-20260217-001/docs/phase-{N}/{agent_id}/`
- Quality gate outputs: `orchestration/feat024-docssite-20260217-001/docs/quality-gates/qg-{N}/`
- Final synthesis: `orchestration/feat024-docssite-20260217-001/docs/phase-4/`

---

## 2. Workflow Architecture

### 2.1 Pipeline Diagram

```
SEQUENTIAL + FAN-OUT PIPELINE: feat024-docssite-20260217-001
=============================================================

[PARALLEL START — DNS propagation runs in background]
┌───────────────────────────────────────────────────────────────────────────┐
│  PHASE 0 (Parallel Track): EN-949 DNS Setup — MANUAL USER STEPS          │
│  ──────────────────────────────────────────────────────────────           │
│  • orch-planner provides DNS instructions (Namesecure CNAME record)       │
│  • User executes: Namesecure login -> create CNAME jerry->geekatron.github.io │
│  STATUS: PENDING — requires user action                                   │
│  NOTE: DNS propagation may take 24-48h. Run in background.               │
└───────────────────────────────────────────────────────────────────────────┘
         │ (background propagation continues throughout)
         ▼
┌───────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: Foundation — EN-946 MkDocs Material Setup                       │
│  ──────────────────────────────────────────────────                        │
│  • ps-implementer → uv add mkdocs-material, mkdocs.yml, docs/CNAME        │
│  • ps-reviewer    → verify local serve + AC compliance                    │
│  STATUS: PENDING                                                          │
└──────────────────────────────┬────────────────────────────────────────────┘
                               │
                 ╔═════════════════════════╗
                 ║  SYNC BARRIER: Phase 2  ║
                 ║  Blocked by: Phase 1    ║
                 ╚═════════════════════════╝
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
┌──────────────────────────┐  ┌──────────────────────────────────────────────┐
│  PHASE 2A: EN-947        │  │  PHASE 2B: EN-948                            │
│  Content Curation        │  │  GitHub Actions Deployment                   │
│  ─────────────────────── │  │  ──────────────────────────────────────────  │
│  • ps-architect → audit  │  │  • ps-implementer → create docs.yml          │
│    docs/, define nav,    │  │  • ps-reviewer   → verify no CI conflicts    │
│    create index.md       │  │  STATUS: PENDING                             │
│  • ps-critic   → review  │  └──────────────────────────────────────────────┘
│  STATUS: PENDING         │            │
└──────────────────────────┘            │
         │                              │
         └──────────────┬───────────────┘
                        │ [FAN-IN]
                        ▼
    ╔══════════════════════════════════════════════════════════╗
    ║              QUALITY GATE 1 (QG-1)                       ║
    ║  After Phase 2A + 2B: mkdocs.yml + content + docs.yml   ║
    ║  Strategies: S-010 (in creator loops) ->                 ║
    ║              S-003 (Steelman) ->                         ║
    ║              S-002 (Devil's Advocate) ->                 ║
    ║              S-007 (Constitutional) ->                   ║
    ║              S-014 (LLM-as-Judge scoring)                ║
    ║  Threshold:  >= 0.92 weighted composite                  ║
    ║  Agents:     adv-executor-001 -> adv-executor-002 ->     ║
    ║              adv-executor-003 -> adv-scorer-001          ║
    ║  Output:     docs/quality-gates/qg-1/                    ║
    ║  STATUS: PENDING                                         ║
    ╚══════════════════════════════════════════════════════════╝
                        │
                        ▼ [QG-1 PASS — gh-pages branch exists]
┌───────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: EN-949 GitHub Pages Reconfiguration                             │
│  ────────────────────────────────────────────                             │
│  • orch-planner provides GitHub Pages UI instructions                     │
│  • User executes: Settings -> Pages -> gh-pages branch + custom domain    │
│  • ps-verifier  → confirm gh-pages branch content and settings            │
│  STATUS: PENDING — requires user action                                   │
│  BLOCKED BY: QG-1 PASS (gh-pages branch must exist first)                │
└──────────────────────────────┬────────────────────────────────────────────┘
                               │
                               ▼
    ╔══════════════════════════════════════════════════════════╗
    ║              QUALITY GATE 2 (QG-2)                       ║
    ║  After Phase 3: DNS propagation + Pages configuration    ║
    ║  Strategy: S-014 (LLM-as-Judge) — configuration check   ║
    ║  Threshold: >= 0.92                                      ║
    ║  Agent: adv-scorer-002                                   ║
    ║  Output: docs/quality-gates/qg-2/                        ║
    ║  STATUS: PENDING                                         ║
    ╚══════════════════════════════════════════════════════════╝
                               │
                               ▼ [QG-2 PASS]
┌───────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: EN-950 Validation & Go-Live                                     │
│  ───────────────────────────────────                                      │
│  • ps-verifier   → push trigger, verify GitHub Actions workflow runs      │
│  • ps-verifier   → verify jerry.geekatron.org: content, HTTPS, search,   │
│                    all nav links                                           │
│  • orch-synthesizer → final synthesis report                              │
│  STATUS: PENDING — BLOCKED by QG-2 PASS                                  │
└──────────────────────────────┬────────────────────────────────────────────┘
                               │
                               ▼
    ╔══════════════════════════════════════════════════════════╗
    ║              QUALITY GATE 3 (QG-3)                       ║
    ║  Final cross-deliverable and live site verification      ║
    ║  Strategy: S-014 (LLM-as-Judge) — final composite       ║
    ║  Threshold: >= 0.92 aggregate                            ║
    ║  Agent: adv-scorer-003                                   ║
    ║  Output: docs/quality-gates/qg-3/                        ║
    ║  STATUS: PENDING                                         ║
    ╚══════════════════════════════════════════════════════════╝
                               │
                               ▼
                      [WORKFLOW COMPLETE]
```

### 2.2 Orchestration Pattern Classification

| Pattern | Applied | Description |
|---------|---------|-------------|
| Sequential | Yes | Primary pipeline — phases execute in strict order after barriers |
| Concurrent | Yes | Phase 2A + 2B fan-out: content curation and GH Actions workflow in parallel |
| Concurrent | Yes | Phase 0 (DNS) runs in background from start |
| Barrier Sync | Yes | Phase 1 complete before Phase 2A/2B fan-out |
| Barrier Sync | Yes | QG-1 PASS before Phase 3 (gh-pages branch must exist) |
| Hierarchical | Yes | Orchestrator (main Claude) delegates to agents via Task tool |

---

## 3. Phase Definitions

### 3.0 Phase 0: EN-949 DNS Setup (Parallel Background Track)

| Field | Value |
|-------|-------|
| Purpose | Initiate DNS propagation for `jerry.geekatron.org` immediately — DNS propagation takes time and must run in background while code work proceeds |
| Status | PENDING |
| Execution Mode | PARALLEL with all other phases (runs immediately, no blocker) |
| User Action Required | Yes — Namesecure login required |
| Exit Criteria | CNAME record created at Namesecure (verification deferred to Phase 3) |

| Step | Actor | Action |
|------|-------|--------|
| STEP-001 | User | Log into Namesecure, navigate to `geekatron.org` DNS management |
| STEP-002 | User | Create CNAME record: Host = `jerry`, Points to = `geekatron.github.io`, TTL = default (or 3600) |
| STEP-003 | Claude | Provide exact steps and expected DNS control panel fields |

**Acceptance Criteria (Phase 0):**
- CNAME record submitted at Namesecure for `jerry.geekatron.org` → `geekatron.github.io`
- Propagation verification deferred to Phase 3 (TASK-004 of EN-949)

---

### 3.1 Phase 1: Foundation — EN-946 MkDocs Material Setup

| Field | Value |
|-------|-------|
| Purpose | Install MkDocs Material via uv, create mkdocs.yml, create docs/CNAME, verify local serve |
| Status | PENDING |
| Blocked By | None (first code phase) |
| Exit Criteria | MkDocs serves locally without errors; all EN-946 ACs met |

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-implementer-001 | Execute EN-946 TASK-001 through TASK-003: run `uv add --dev mkdocs-material`, create `mkdocs.yml` (site_name, site_url, theme, nav stub), create `docs/CNAME` containing `jerry.geekatron.org` | FEAT-024 feature file (EN-946 spec), research findings | `docs/phase-1/ps-implementer-001/ps-implementer-001-en946-setup.md` |
| ps-reviewer-001 | Verify EN-946 TASK-004: confirm `uv run mkdocs serve` runs without errors; verify AC-1 through AC-4; check CNAME file content | ps-implementer-001 output, repo state | `docs/phase-1/ps-reviewer-001/ps-reviewer-001-en946-review.md` |

**EN-946 Acceptance Criteria Mapping:**

| AC | Validated By |
|----|-------------|
| AC-1: mkdocs-material in pyproject.toml dev dependencies | ps-implementer-001 (uv add output), ps-reviewer-001 (pyproject.toml check) |
| AC-2: mkdocs.yml exists at repo root with Material theme | ps-implementer-001 (creates file), ps-reviewer-001 (content verification) |
| AC-3: docs/CNAME contains `jerry.geekatron.org` | ps-implementer-001 (creates file), ps-reviewer-001 (content check, DISC-004 mitigation confirmed) |
| AC-4: `uv run mkdocs serve` runs without errors | ps-reviewer-001 (local serve verification) |

**Phase 1 Exit Criteria:**
- `mkdocs-material` added as dev dependency (pyproject.toml updated)
- `mkdocs.yml` exists at repo root with Material theme configured
- `docs/CNAME` contains `jerry.geekatron.org` (bare domain, single line)
- Local serve confirms no build errors

---

### 3.2 Phase 2A: Content Curation & Landing Page — EN-947

| Field | Value |
|-------|-------|
| Purpose | Create docs/index.md landing page, audit docs/ directory, define public-facing nav structure |
| Status | PENDING |
| Blocked By | Phase 1 complete (needs mkdocs.yml to define nav) |
| Execution Mode | PARALLEL with Phase 2B |
| Exit Criteria | Landing page created; content audit complete; nav structure finalized; no internal refs exposed |

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-architect-001 | Execute EN-947 TASK-001 through TASK-003: audit all docs/ files (classify public/internal/exclude), create docs/index.md (overview, key features, quick links), define nav: structure for mkdocs.yml | FEAT-024 EN-947 content candidate table, current docs/ directory state | `docs/phase-2a/ps-architect-001/ps-architect-001-content-audit.md` and `docs/phase-2a/ps-architect-001/ps-architect-001-index-md.md` |
| ps-architect-001 | Execute EN-947 TASK-004 through TASK-005: identify/link getting-started.md or existing runbooks/getting-started.md, review selected docs for broken links and sensitive content | Audit output, docs/ file contents | Updated outputs in same path |
| ps-critic-001 | Creator-critic review of landing page + nav structure (minimum 3 iterations per H-14); verify no internal docs in public nav; verify H-23/H-24 compliance on index.md | ps-architect-001 drafts | `docs/phase-2a/ps-critic-001/ps-critic-001-en947-review.md` |

**EN-947 Acceptance Criteria Mapping:**

| AC | Validated By |
|----|-------------|
| AC-1: docs/index.md with project overview and navigation | ps-architect-001 (creates), ps-critic-001 (review), QG-1 |
| AC-2: Content audit complete — each docs/ item classified | ps-architect-001 (audit artifact), ps-critic-001 |
| AC-3: nav: in mkdocs.yml only references public content | ps-architect-001 (defines nav), ps-critic-001 (verifies), QG-1 S-007 |
| AC-4: No broken internal links in public-facing docs | ps-architect-001 TASK-005, ps-critic-001 |
| AC-5: No sensitive/internal content exposed in navigation | ps-critic-001 (security-lens review), QG-1 S-007 |

**Phase 2A Exit Criteria:**
- Content audit document classifies all docs/ items as public/internal/exclude
- docs/index.md created with project overview, key features, and navigation links
- nav: structure in mkdocs.yml references only public-facing content
- No broken links in selected public docs
- Creator-critic loop complete (minimum 3 iterations)

---

### 3.3 Phase 2B: GitHub Actions Deployment Workflow — EN-948

| Field | Value |
|-------|-------|
| Purpose | Create .github/workflows/docs.yml with the official MkDocs Material CI workflow; verify no conflicts with existing CI |
| Status | PENDING |
| Blocked By | Phase 1 complete (needs mkdocs.yml to exist) |
| Execution Mode | PARALLEL with Phase 2A |
| Exit Criteria | docs.yml created and valid; workflow triggers correctly; no CI conflicts |

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-implementer-002 | Execute EN-948 TASK-001 through TASK-002: create `.github/workflows/docs.yml` using official MkDocs Material workflow (from FEAT-024 research: checkout, setup-python, cache, pip install mkdocs-material, mkdocs gh-deploy --force), add paths filter (docs/**, mkdocs.yml), check existing ci.yml and version-bump.yml for conflicts | FEAT-024 research (GH Actions workflow spec), existing .github/workflows/ directory | `docs/phase-2b/ps-implementer-002/ps-implementer-002-en948-workflow.md` |
| ps-reviewer-002 | Execute EN-948 TASK-003: verify docs.yml is valid YAML and follows workflow spec; verify no conflicts with ci.yml or version-bump.yml; verify permissions: contents: write is present; verify paths filter is correct | ps-implementer-002 output, docs.yml content, existing workflow files | `docs/phase-2b/ps-reviewer-002/ps-reviewer-002-en948-review.md` |

**EN-948 Acceptance Criteria Mapping:**

| AC | Validated By |
|----|-------------|
| AC-1: .github/workflows/docs.yml exists and is valid | ps-implementer-002 (creates), ps-reviewer-002 (YAML validation) |
| AC-2: Workflow triggers on push to main when docs or mkdocs.yml change | ps-reviewer-002 (trigger + paths filter check) |
| AC-3: gh-pages branch is created/updated with built HTML site | ps-reviewer-002 (workflow run verification — can only confirm after merge to main) |
| AC-4: No conflicts with existing CI, version-bump, or release workflows | ps-reviewer-002 (conflict analysis), QG-1 S-002 |

**Phase 2B Exit Criteria:**
- `.github/workflows/docs.yml` created with official MkDocs Material workflow
- Paths filter applied: triggers on `docs/**` and `mkdocs.yml` changes
- `permissions: contents: write` set
- No trigger, name, or job-id conflicts with existing workflows
- Workflow reviewed for correctness

---

### 3.4 Phase 3: EN-949 GitHub Pages Reconfiguration

| Field | Value |
|-------|-------|
| Purpose | Reconfigure GitHub Pages source from legacy main/root to gh-pages branch; set custom domain; verify DNS propagation; enable HTTPS |
| Status | PENDING |
| Blocked By | QG-1 PASS (gh-pages branch must exist — created by first docs.yml run after merge) |
| User Action Required | Yes — GitHub Settings UI required |
| Exit Criteria | GitHub Pages serves from gh-pages; custom domain set; DNS resolves; HTTPS enforced |

| Step | Actor | Action |
|------|-------|--------|
| STEP-001 | User | Merge PR to main (triggers docs.yml GitHub Actions workflow; creates gh-pages branch) |
| STEP-002 | User | GitHub repo Settings > Pages: change Source from `main /` to `gh-pages` branch |
| STEP-003 | User | GitHub repo Settings > Pages: set Custom domain to `jerry.geekatron.org` and Save |
| STEP-004 | Claude / ps-verifier-001 | Run `dig jerry.geekatron.org +nostats +nocomments +nocmd` and verify CNAME → `geekatron.github.io` |
| STEP-005 | User | GitHub repo Settings > Pages: tick "Enforce HTTPS" after Let's Encrypt cert provisions |

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-verifier-001 | Verify Phase 3 configuration: confirm gh-pages branch exists with built HTML, verify CNAME file present in gh-pages root (docs/CNAME mitigation from DISC-004), verify DNS resolution via dig, verify GitHub Pages settings match expected state | GitHub repo state, DNS dig output | `docs/phase-3/ps-verifier-001/ps-verifier-001-en949-config-check.md` |

**EN-949 Acceptance Criteria Mapping:**

| AC | Validated By |
|----|-------------|
| AC-1: CNAME record at Namesecure: jerry.geekatron.org → geekatron.github.io | Phase 0 user action + ps-verifier-001 dig verification |
| AC-2: GitHub Pages custom domain set to jerry.geekatron.org | User action STEP-003, ps-verifier-001 (gh api confirmation) |
| AC-3: GitHub Pages source is gh-pages branch | User action STEP-002, ps-verifier-001 |
| AC-4: dig jerry.geekatron.org resolves correctly | ps-verifier-001 (dig output) |
| AC-5: HTTPS enforced, valid cert serving | User action STEP-005, EN-950 final validation |

**Phase 3 Exit Criteria:**
- gh-pages branch exists with MkDocs-built HTML content
- CNAME file present in gh-pages root (DISC-004 mitigation confirmed)
- GitHub Pages source configured to gh-pages branch
- Custom domain set to `jerry.geekatron.org` in GitHub Settings
- DNS propagation confirmed (or in progress — HTTPS validation deferred to EN-950)
- QG-2 configuration quality score >= 0.92

---

### 3.5 Phase 4: EN-950 Validation & Go-Live

| Field | Value |
|-------|-------|
| Purpose | End-to-end verification that the full pipeline works: push triggers build, site serves correctly, HTTPS active, search works, all links resolve |
| Status | PENDING |
| Blocked By | QG-2 PASS |
| Exit Criteria | All EN-950 ACs met; site live at jerry.geekatron.org; final synthesis report created; QG-3 score >= 0.92 |

| Agent ID | Role | Input | Output Artifact Path |
|----------|------|-------|---------------------|
| ps-verifier-002 | Execute EN-950 TASK-001 through TASK-005: confirm GitHub Actions workflow ran successfully on push (check Actions tab), verify jerry.geekatron.org serves MkDocs Material site with correct content, verify HTTPS (no mixed-content warnings), verify search functionality returns results, smoke test all navigation links | GitHub Actions run logs, live site content | `docs/phase-4/ps-verifier-002/ps-verifier-002-en950-validation.md` |
| orch-synthesizer-001 | Create final workflow synthesis report: summary of all deliverables, decisions made (DEC-006), discoveries resolved (DISC-003, DISC-004), lessons learned, WORKTRACKER.md update instructions | All phase artifacts, verification output | `docs/phase-4/orch-synthesizer-001/orch-synthesizer-001-synthesis.md` |

**EN-950 Acceptance Criteria Mapping:**

| AC | Validated By |
|----|-------------|
| AC-1: Push-to-main triggers docs build and deploy automatically | ps-verifier-002 (Actions run log) |
| AC-2: jerry.geekatron.org serves the Jerry documentation site | ps-verifier-002 (live site check) |
| AC-3: HTTPS active with valid certificate | ps-verifier-002 (HTTPS verification) |
| AC-4: Site search returns results | ps-verifier-002 (search functionality test) |
| AC-5: All navigation links resolve correctly | ps-verifier-002 (smoke test all nav links) |

**Phase 4 Exit Criteria:**
- GitHub Actions docs.yml run confirmed successful
- jerry.geekatron.org serves MkDocs Material site with Jerry content
- HTTPS enforced and valid
- Search functional
- All navigation links resolve without 404
- Final synthesis report created
- QG-3 score >= 0.92

---

## 4. Quality Gate Protocol

### 4.1 Quality Gate Definitions (C2)

**Applicable C2 strategies per quality-enforcement.md:**
- **Required:** S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge)
- **Optional:** S-003 (Steelman), S-010 (Self-Refine)
- **Threshold:** >= 0.92 weighted composite
- **Minimum iterations:** 3 (creator-critic-revision) per H-14
- **H-16 ordering:** S-003 (Steelman) MUST precede S-002 (Devil's Advocate)

### 4.2 Quality Gate 1 (QG-1) — After Phases 2A + 2B

| Field | Value |
|-------|-------|
| Deliverable | mkdocs.yml (with nav), docs/index.md, content audit, .github/workflows/docs.yml |
| Path | `docs/quality-gates/qg-1/` |
| Strategy Sequence | S-010 (in Phase 2A creator loop) → S-003 (Steelman) → S-002 (Devil's Advocate) → S-007 (Constitutional) → S-014 (LLM-as-Judge scoring) |
| Threshold | >= 0.92 |
| Pass Action | Proceed to Phase 3 |
| Fail Action | Return to relevant implementer/architect agent for targeted revision; re-score (max 2 retries) |

| Agent | Task | Output |
|-------|------|--------|
| adv-executor-001 | Apply S-003 (Steelman) — strengthen the configuration and content choices before adversarial challenge (H-16 required ordering) | `docs/quality-gates/qg-1/adv-executor-001/qg1-steelman.md` |
| adv-executor-002 | Apply S-002 (Devil's Advocate) — challenge nav structure for exposed internal docs, docs.yml for CI conflicts, mkdocs.yml for misconfiguration, CNAME file presence and content | `docs/quality-gates/qg-1/adv-executor-002/qg1-devils-advocate.md` |
| adv-executor-003 | Apply S-007 (Constitutional AI Critique) — verify AC compliance, H-23/H-24 nav standards on index.md, P-022 accuracy of content, DISC-004 mitigation confirmed, UV-only compliance (H-05/H-06 — no pip in docs.yml) | `docs/quality-gates/qg-1/adv-executor-003/qg1-constitutional.md` |
| adv-scorer-001 | Apply S-014 (LLM-as-Judge) — 6-dimension weighted composite score across mkdocs.yml, index.md, docs.yml | `docs/quality-gates/qg-1/adv-scorer-001/qg1-score.md` |

**S-014 Scoring Dimensions:**

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

**QG-1 Focus Areas for Adversarial Review:**
- Does nav: include any `knowledge/`, `research/`, `analysis/` or other internal-only content?
- Is `docs/CNAME` present and does it contain the bare domain (not a URL)? (DISC-004)
- Does docs.yml use `pip install` instead of a uv-compatible approach? (Note: the official MkDocs Material workflow uses pip in the CI environment — this is acceptable because the CI is not the uv project environment)
- Does the workflow have correct `permissions: contents: write`?
- Does the workflow have a `paths:` filter to avoid unnecessary builds?
- Does index.md have a navigation table (H-23) and anchor links (H-24)?

### 4.3 Quality Gate 2 (QG-2) — After Phase 3

| Field | Value |
|-------|-------|
| Deliverable | GitHub Pages configuration state: gh-pages branch content, custom domain setting, DNS resolution, CNAME file in deployed output |
| Path | `docs/quality-gates/qg-2/` |
| Strategy | S-014 (LLM-as-Judge) — configuration verification scoring |
| Threshold | >= 0.92 |
| Pass Action | Proceed to Phase 4 |
| Fail Action | Identify misconfigured component; targeted fix; re-score (max 2 retries) |

| Agent | Task | Output |
|-------|------|--------|
| adv-scorer-002 | Apply S-014 — score the Phase 3 configuration state against all EN-949 ACs; verify gh-pages branch content, CNAME file in deployed root, DNS propagation status, GitHub Pages settings accuracy | `docs/quality-gates/qg-2/adv-scorer-002/qg2-config-score.md` |

**QG-2 Focus Areas:**
- Is CNAME file present at gh-pages root (not just in docs/)? Confirms DISC-004 mitigation worked.
- Does `dig jerry.geekatron.org` return CNAME to `geekatron.github.io`?
- Is GitHub Pages source set to gh-pages (not main)?
- Is the custom domain field populated with `jerry.geekatron.org`?

### 4.4 Quality Gate 3 (QG-3) — After Phase 4

| Field | Value |
|-------|-------|
| Deliverable | All FEAT-024 deliverables — live site + all configurations + synthesis |
| Path | `docs/quality-gates/qg-3/` |
| Strategy | S-014 (LLM-as-Judge) — final composite scoring |
| Threshold | >= 0.92 aggregate |
| Pass Action | Workflow COMPLETE |
| Fail Action | Identify failing component; targeted fix; re-score (max 2 retries) |

| Agent | Task | Output |
|-------|------|--------|
| adv-scorer-003 | Apply S-014 — final composite score across all FEAT-024 deliverables; verify all 6 feature-level ACs; check consistency between mkdocs.yml nav and live site navigation; verify CNAME persistence after deploy (DISC-004 confirmed resolved) | `docs/quality-gates/qg-3/adv-scorer-003/qg3-final-score.md` |

### 4.5 Quality Gate Scoring Protocol

Before QG entry, adv-executor agents MUST follow H-16 ordering:
1. Apply S-003 (Steelman) internally — strengthen the deliverable before critiquing
2. Apply S-002 (Devil's Advocate) — challenge from adversarial perspective
3. Apply S-007 (Constitutional AI Critique) — verify against Jerry Constitution and rules
4. Hand findings to adv-scorer for S-014 scoring

Below-threshold outcomes:

| Band | Score Range | Action |
|------|------------|--------|
| PASS | >= 0.92 | Proceed |
| REVISE | 0.85 - 0.91 | Targeted revision; re-score |
| REJECTED | < 0.85 | Significant rework; full creator loop reset |

---

## 5. Agent Registry

| Agent ID | Phase | Skill | Role | Inputs | Output Path |
|----------|-------|-------|------|--------|-------------|
| ps-implementer-001 | 1 | problem-solving | MkDocs Material setup (uv add, mkdocs.yml, docs/CNAME) | FEAT-024 EN-946 spec | `docs/phase-1/ps-implementer-001/` |
| ps-reviewer-001 | 1 | problem-solving | EN-946 AC verification, local serve check | ps-implementer-001 output | `docs/phase-1/ps-reviewer-001/` |
| ps-architect-001 | 2A | problem-solving | Content audit, index.md creation, nav definition | FEAT-024 EN-947 spec, docs/ directory | `docs/phase-2a/ps-architect-001/` |
| ps-critic-001 | 2A | problem-solving | Creator-critic review of index.md + nav (3+ iterations) | ps-architect-001 drafts | `docs/phase-2a/ps-critic-001/` |
| ps-implementer-002 | 2B | problem-solving | GitHub Actions docs.yml creation, conflict check | FEAT-024 EN-948 workflow spec | `docs/phase-2b/ps-implementer-002/` |
| ps-reviewer-002 | 2B | problem-solving | docs.yml YAML validation, trigger verification, conflict analysis | ps-implementer-002 output, existing workflows | `docs/phase-2b/ps-reviewer-002/` |
| adv-executor-001 | QG-1 | adversary | S-003 Steelman on Phase 1+2 deliverables | All Phase 1+2 outputs | `docs/quality-gates/qg-1/adv-executor-001/` |
| adv-executor-002 | QG-1 | adversary | S-002 Devil's Advocate on nav/config/workflow | adv-executor-001 steelman | `docs/quality-gates/qg-1/adv-executor-002/` |
| adv-executor-003 | QG-1 | adversary | S-007 Constitutional Critique on all deliverables | adv-executor-002 critique | `docs/quality-gates/qg-1/adv-executor-003/` |
| adv-scorer-001 | QG-1 | adversary | S-014 LLM-as-Judge composite scoring | All adv-executor outputs | `docs/quality-gates/qg-1/adv-scorer-001/` |
| ps-verifier-001 | 3 | problem-solving | Phase 3 config verification (gh-pages, CNAME, DNS) | Repo state, DNS output | `docs/phase-3/ps-verifier-001/` |
| adv-scorer-002 | QG-2 | adversary | S-014 configuration verification scoring | ps-verifier-001 output | `docs/quality-gates/qg-2/adv-scorer-002/` |
| ps-verifier-002 | 4 | problem-solving | E2E live site validation (all EN-950 tasks) | GitHub Actions logs, live site | `docs/phase-4/ps-verifier-002/` |
| orch-synthesizer-001 | 4 | orchestration | Final workflow synthesis report | All phase artifacts | `docs/phase-4/orch-synthesizer-001/` |
| adv-scorer-003 | QG-3 | adversary | S-014 final composite scoring | All deliverables | `docs/quality-gates/qg-3/adv-scorer-003/` |

**Manual Actor (User):**

| Step | Phase | Action |
|------|-------|--------|
| DNS CNAME creation | 0 | Namesecure login → create CNAME record |
| GitHub Pages reconfiguration | 3 | Settings → Pages → gh-pages source + custom domain |
| HTTPS enforcement | 3 | Settings → Pages → Enforce HTTPS |
| Merge PR to main | 3 | Triggers first docs.yml run → creates gh-pages branch |

---

## 6. State Management

### 6.1 State Files

| File | Purpose |
|------|---------|
| `ORCHESTRATION.yaml` | Machine-readable state (SSOT) — updated by orch-tracker after each phase |
| `ORCHESTRATION_PLAN.md` | This file — strategic context and execution instructions |

### 6.2 Artifact Path Structure

All artifacts stored under the workflow base path using dynamic identifiers:

```
orchestration/feat024-docssite-20260217-001/
├── ORCHESTRATION_PLAN.md
├── ORCHESTRATION.yaml
└── docs/
    ├── phase-1/
    │   ├── ps-implementer-001/
    │   │   └── ps-implementer-001-en946-setup.md
    │   └── ps-reviewer-001/
    │       └── ps-reviewer-001-en946-review.md
    ├── phase-2a/
    │   ├── ps-architect-001/
    │   │   ├── ps-architect-001-content-audit.md
    │   │   └── ps-architect-001-index-md.md
    │   └── ps-critic-001/
    │       └── ps-critic-001-en947-review.md
    ├── phase-2b/
    │   ├── ps-implementer-002/
    │   │   └── ps-implementer-002-en948-workflow.md
    │   └── ps-reviewer-002/
    │       └── ps-reviewer-002-en948-review.md
    ├── phase-3/
    │   └── ps-verifier-001/
    │       └── ps-verifier-001-en949-config-check.md
    ├── phase-4/
    │   ├── ps-verifier-002/
    │   │   └── ps-verifier-002-en950-validation.md
    │   └── orch-synthesizer-001/
    │       └── orch-synthesizer-001-synthesis.md
    └── quality-gates/
        ├── qg-1/
        │   ├── adv-executor-001/
        │   │   └── qg1-steelman.md
        │   ├── adv-executor-002/
        │   │   └── qg1-devils-advocate.md
        │   ├── adv-executor-003/
        │   │   └── qg1-constitutional.md
        │   └── adv-scorer-001/
        │       └── qg1-score.md
        ├── qg-2/
        │   └── adv-scorer-002/
        │       └── qg2-config-score.md
        └── qg-3/
            └── adv-scorer-003/
                └── qg3-final-score.md
```

### 6.3 Checkpoint Strategy

| Trigger | When | Purpose |
|---------|------|---------|
| PHASE_COMPLETE | After each of Phase 1, 2A, 2B, 3, 4 | Phase-level rollback point |
| QG_COMPLETE | After QG-1, QG-2, QG-3 (pass or fail) | Post-gate state preservation |
| USER_ACTION | After each manual user step | Track async user progress |
| MANUAL | User-triggered | Debug and inspection |

---

## 7. Execution Constraints

### 7.1 Hard Constraints (Jerry Constitution)

| Constraint | ID | Enforcement |
|------------|----|----|
| Single agent nesting | P-003 | Orchestrator (main Claude) invokes agents via Task tool — no recursive subagents |
| File persistence | P-002 | All phase outputs and quality gate artifacts persisted to filesystem before proceeding |
| No deception | P-022 | Quality scores reported as-is; no rounding up to meet threshold |
| User authority | P-020 | Quality gate PASS/FAIL decisions surfaced to user at each gate |
| UV only | H-05/H-06 | All Python execution uses `uv run`; `uv add` for deps. Note: docs.yml CI uses `pip install mkdocs-material` in the Ubuntu runner — this is correct and does NOT violate H-05/H-06, which apply to the local development environment. |
| Nav tables required | H-23/H-24 | All created markdown files over 30 lines must include navigation tables with anchor links |

### 7.1.1 Worktracker Entity Templates

> **WTI-007:** Any worktracker entities created during this workflow (FEATURE, ENABLER updates) MUST use canonical templates from `.context/templates/worktracker/`. Read the appropriate template before creating or updating. Do not create entity files from memory.

### 7.2 Soft Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 3 | Phase 2 fan-out: ps-architect-001 + ps-implementer-002 + their reviewers |
| Max QG retries | 2 | Circuit breaker — after 2 failed revisions, escalate to user |
| Checkpoint frequency | PHASE + QG + USER_ACTION | Recovery at phase, gate, and async user-step boundaries |
| Creator-critic minimum iterations | 3 | H-14 requirement (Phase 2A) |
| DNS propagation wait | Async | Phase 3 should not begin until DNS confirmed OR user confirms Phase 0 complete |

---

## 8. Success Criteria

### 8.1 Phase 0 Exit Criteria (DNS Setup)

| Criterion | Validation |
|-----------|------------|
| CNAME record submitted at Namesecure | User confirms action in ORCHESTRATION.yaml |
| DNS propagation in progress | Verified when Phase 3 runs dig check |

### 8.2 Phase 1 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| mkdocs-material in pyproject.toml dev deps | ps-reviewer-001 artifact |
| mkdocs.yml at repo root with Material theme | ps-reviewer-001 artifact |
| docs/CNAME contains jerry.geekatron.org | ps-reviewer-001 artifact (DISC-004 mitigation confirmed) |
| uv run mkdocs serve completes without errors | ps-reviewer-001 artifact |

### 8.3 Phase 2A Exit Criteria

| Criterion | Validation |
|-----------|------------|
| docs/ content audit complete with public/internal/exclude classification | ps-architect-001 audit artifact |
| docs/index.md created with overview, features, quick links | ps-architect-001 index-md artifact |
| nav: in mkdocs.yml references only public content | ps-architect-001 output, ps-critic-001 sign-off |
| No broken links in public-facing docs | ps-architect-001 TASK-005, ps-critic-001 review |
| Creator-critic loop complete (min 3 iterations) | ps-critic-001 artifact records iteration count |

### 8.4 Phase 2B Exit Criteria

| Criterion | Validation |
|-----------|------------|
| .github/workflows/docs.yml created and valid | ps-reviewer-002 artifact |
| Workflow triggers on push to main with paths filter | ps-reviewer-002 artifact |
| permissions: contents: write set | ps-reviewer-002 artifact |
| No conflicts with existing workflows | ps-reviewer-002 conflict analysis |

### 8.5 QG-1 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| QG-1 score >= 0.92 | adv-scorer-001 score artifact |
| No critical findings blocking proceed | adv-executor-002/003 artifacts clear |

### 8.6 Phase 3 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| gh-pages branch exists with MkDocs HTML content | ps-verifier-001 artifact |
| CNAME file present in gh-pages root | ps-verifier-001 artifact (DISC-004 confirmed resolved) |
| GitHub Pages source = gh-pages branch | ps-verifier-001 artifact |
| Custom domain = jerry.geekatron.org | ps-verifier-001 artifact |
| DNS propagation confirmed (or in progress with expected completion) | ps-verifier-001 dig output |

### 8.7 Phase 4 Exit Criteria

| Criterion | Validation |
|-----------|------------|
| GitHub Actions docs.yml run confirmed successful | ps-verifier-002 artifact |
| jerry.geekatron.org serves Jerry docs site | ps-verifier-002 artifact |
| HTTPS active with valid certificate | ps-verifier-002 artifact |
| Search functional | ps-verifier-002 artifact |
| All nav links resolve | ps-verifier-002 artifact |
| Final synthesis report created | orch-synthesizer-001 artifact |

### 8.8 Workflow Completion Criteria

| Criterion | Validation |
|-----------|------------|
| All phases COMPLETE | ORCHESTRATION.yaml phase statuses |
| QG-1, QG-2, QG-3 all PASS | Score artifacts in quality-gates/ |
| jerry.geekatron.org live and serving Jerry docs | Live site verification in ps-verifier-002 |
| CNAME persistence confirmed after deploy | DISC-004 resolved per ps-verifier-001 + ps-verifier-002 |
| WORKTRACKER.md reflects FEAT-024 and all ENs closed | orch-synthesizer-001 update confirmed |
| Feature-level ACs AC-1 through AC-6 verified | orch-synthesizer-001 traceability |

---

## 9. Risk Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| DNS propagation delay blocks Phase 3 | H | M | Start DNS in Phase 0 immediately (parallel); Phase 3 checks propagation; if not propagated, wait and recheck (async, not blocking workflow) |
| docs/CNAME wiped on deploy (DISC-004) | H (without fix) | H | Mitigation in Phase 1: create docs/CNAME containing bare domain. ps-reviewer-001 verifies. QG-1 S-007 confirms. ps-verifier-001 confirms CNAME in gh-pages root. |
| GitHub Pages source not switched from main to gh-pages | M | H | Phase 3 explicit user step with exact instructions. ps-verifier-001 checks via gh api. QG-2 scores this. |
| nav: in mkdocs.yml accidentally exposes internal docs | M | H | ps-architect-001 content audit classifies all docs/. ps-critic-001 adversarially checks nav. QG-1 S-007 performs constitutional check. |
| docs.yml conflicts with existing CI workflows | M | M | ps-implementer-002 reads all existing .github/workflows/ files first. ps-reviewer-002 explicitly checks trigger names and job IDs. QG-1 S-002 challenges for conflicts. |
| docs.yml uses pip in CI — confusion with H-05/H-06 | L | M | Explicitly documented in constraint 7.1: CI uses pip in Ubuntu runner (correct, not H-05/H-06 violation). ps-reviewer-002 confirms approach. |
| QG scoring leniency bias | M | H | adv-scorer agents MUST actively counteract leniency per S-014 rubric; scores must be justified per dimension. |
| Creator-critic loop stalls below 3 iterations | L | M | Enforced by orch-tracker; minimum 3 iterations logged before QG-1 entry (Phase 2A). |
| Context rot in Phase 2A (large docs/ audit) | M | M | ps-architect-001 receives focused input: EN-947 content candidate table + listing of docs/ files (not full content of each file). Reads individual files selectively. |
| Let's Encrypt cert not yet provisioned when Phase 4 runs | M | M | Phase 4 includes DNS/cert wait as precondition. ps-verifier-002 explicitly checks HTTPS. If cert not ready, STEP-005 deferred with note in synthesis. |

---

## 10. Resumption Context

### 10.1 Current Execution State

```
WORKFLOW STATUS AS OF 2026-02-17
=================================

Phase 0 (DNS CNAME Setup):             PENDING — requires user action (Namesecure)
Phase 1 (MkDocs Material Setup):        PENDING
Phase 2A (Content Curation):            PENDING — BLOCKED by Phase 1
Phase 2B (GitHub Actions Workflow):     PENDING — BLOCKED by Phase 1
Quality Gate 1:                         PENDING — BLOCKED by Phases 2A + 2B
Phase 3 (GH Pages Reconfiguration):     PENDING — BLOCKED by QG-1 + user action
Quality Gate 2:                         PENDING — BLOCKED by Phase 3
Phase 4 (Validation & Go-Live):         PENDING — BLOCKED by QG-2
Quality Gate 3:                         PENDING — BLOCKED by Phase 4

Overall Progress: 0/4 code phases complete (Phase 0 is async user action)
```

### 10.2 Next Actions

1. Instruct user to execute Phase 0 (DNS): log into Namesecure, create CNAME record `jerry` → `geekatron.github.io`
2. Invoke ps-implementer-001 (Phase 1): `uv add --dev mkdocs-material`, create mkdocs.yml, create docs/CNAME
3. Invoke ps-reviewer-001 (Phase 1): verify AC-1 through AC-4 of EN-946
4. Invoke orch-tracker to checkpoint Phase 1 complete
5. Invoke Phase 2A + Phase 2B in parallel:
   - ps-architect-001: content audit + index.md + nav definition
   - ps-implementer-002: docs.yml creation
6. Invoke ps-critic-001 (Phase 2A fan-in) after ps-architect-001
7. Invoke ps-reviewer-002 (Phase 2B) after ps-implementer-002
8. Invoke orch-tracker to checkpoint Phase 2 complete
9. Run Quality Gate 1: adv-executor-001 (Steelman) → adv-executor-002 (Devil's Advocate) → adv-executor-003 (Constitutional) → adv-scorer-001 (LLM-as-Judge)
10. Proceed to Phase 3 on QG-1 PASS; instruct user to merge PR and configure GitHub Pages

### 10.3 Invocation Pattern

All agents are invoked by the main Claude context via Task tool per P-003:

```
Task: [agent-id]
Context: Read ORCHESTRATION_PLAN.md Phase N definition.
         Read [input artifacts].
         Execute [agent role] and persist output to [output path].
         Confirm output path in response.
```

### 10.4 Key Reference Artifacts

| Artifact | Purpose |
|----------|---------|
| `projects/PROJ-001-oss-release/work/EPIC-001-oss-release/FEAT-024-public-docs-site/FEAT-024-public-docs-site.md` | Feature file — research findings, decisions, enabler specs |
| `pyproject.toml` | Add mkdocs-material dev dependency here |
| `mkdocs.yml` | Create at repo root |
| `docs/CNAME` | Create with `jerry.geekatron.org` (bare domain, DISC-004 mitigation) |
| `.github/workflows/docs.yml` | Create with official MkDocs Material CI workflow |
| `.github/workflows/ci.yml` | Read to check for conflicts |

---

*Document ID: PROJ-001-ORCH-PLAN-FEAT024*
*Workflow ID: feat024-docssite-20260217-001*
*Version: 1.0*
*Criticality: C2 (Standard) — documentation site tooling, reversible within 1 day*
*Cross-Session Portable: All paths are repository-relative*

---

> **DISCLAIMER:** This plan was generated by the orch-planner agent (v2.2.0) acting as a planning artifact producer. It does not execute agents — it defines the execution contract for the main Claude context (orchestrator). All agent invocations are performed by the main context via Task tool. This document is the authoritative strategic context for workflow `feat024-docssite-20260217-001`. Do not modify without updating ORCHESTRATION.yaml version field.
