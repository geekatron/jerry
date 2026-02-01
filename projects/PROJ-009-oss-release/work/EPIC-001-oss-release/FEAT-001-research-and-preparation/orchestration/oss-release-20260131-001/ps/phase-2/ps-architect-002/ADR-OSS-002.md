# ADR-OSS-002: Repository Sync Process

> **Workflow ID:** oss-release-20260131-001
> **Phase:** 2 (ADR Creation)
> **Agent:** ps-architect-002
> **Created:** 2026-01-31
> **Status:** PROPOSED
> **Risk Reference:** RSK-P0-005 (RPN 192 - HIGH)
> **Supersedes:** None
> **Depends On:** ADR-OSS-001 (CLAUDE.md Decomposition Strategy)
> **Constitutional Compliance:** P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-022 (Honesty)

---

## Document Navigation

| Section | Audience | Purpose |
|---------|----------|---------|
| [L0: Executive Summary](#l0-executive-summary-eli5) | Executives, Stakeholders | High-level overview |
| [L1: Technical Details](#l1-technical-details-engineer) | Engineers, Developers | Implementation guidance |
| [L2: Strategic Implications](#l2-strategic-implications-architect) | Architects, Decision Makers | Trade-offs and decisions |

---

## L0: Executive Summary (ELI5)

### The Problem (Simple Analogy)

Imagine you have two notebooks: one for your private diary (including sensitive thoughts) and one you share with friends (a curated travel journal). When something happens in your life, you write it in your private diary first. Later, you copy the appropriate parts to your shared journal.

The challenge is: **How do you keep both notebooks in sync without accidentally sharing private thoughts or forgetting to update the shared journal?**

Jerry faces this exact problem. Per DEC-002 (Dual Repository Strategy), we will have:
- **source-repository** (internal): Contains proprietary extensions, internal projects, and development work
- **jerry** (public): The OSS version with curated, public-safe content

### The Solution

We will implement a **Unidirectional Push Sync** strategy with automated tooling:

1. **Direction:** Always internal-to-public (never the reverse)
2. **Frequency:** On every release (not continuous)
3. **Automation:** GitHub Actions workflow with safety checks
4. **Safety:** Explicit allowlist, secret scanning, manual approval gate

### Key Numbers

| Metric | Value | Rationale |
|--------|-------|-----------|
| Sync frequency | Per release | Reduces complexity vs. continuous sync |
| Automation effort | 4-6 hours | One-time GitHub Actions setup |
| Manual review time | 15-30 min/sync | Safety gate before public push |
| Drift detection | Automated | Scheduled check for divergence |

### Bottom Line

**RSK-P0-005 has RPN 192 (HIGH).** Without a defined sync process, the dual-repo strategy will inevitably lead to drift, confusion, and potential security incidents. This ADR defines the process, automation, and safeguards to make dual-repo sustainable.

---

## Context

### Background

Per DEC-002, Jerry will use a dual-repository strategy for OSS release:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Jerry Dual-Repository Strategy                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────┐      ┌──────────────────────────┐    │
│  │      source-repository          │      │         jerry            │    │
│  │       (internal)         │      │        (public)          │    │
│  │                          │      │                          │    │
│  │ ├── .claude/             │      │ ├── .claude/             │    │
│  │ ├── skills/              │ ───► │ ├── skills/              │    │
│  │ ├── src/                 │      │ ├── src/                 │    │
│  │ ├── docs/                │      │ ├── docs/                │    │
│  │ ├── projects/            │  X   │ └── ...                  │    │
│  │ │   ├── PROJ-009-oss     │      │                          │    │
│  │ │   └── PROJ-010-...     │      │ (No projects/ folder)    │    │
│  │ └── internal/            │  X   │                          │    │
│  │     └── proprietary/     │      │ (No internal/ folder)    │    │
│  └──────────────────────────┘      └──────────────────────────┘    │
│                                                                     │
│  Legend:                                                            │
│  ───► = Sync flow (internal to public)                             │
│   X   = Excluded from sync                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### The Problem: Sync Complexity

The root cause analysis (ps-analyst 5 Whys) identified **"Implicit Knowledge"** as a systemic pattern affecting RSK-P0-005:

```
WHY is sync complexity undefined?
  └─ The decision focused on structure, not operations
WHY wasn't operations included in the decision?
  └─ Operational details were deferred to implementation
WHY defer operational details?
  └─ DEC-002 was a strategic decision; tactics came later
WHY separate strategy from tactics?
  └─ Time pressure to make architectural decisions
WHY time pressure?
  └─ ROOT CAUSE: Big decisions made without full operational planning
```

**Pattern:** Decisions without operational definitions lead to "figure it out later" technical debt.

### Risk Register Reference (RSK-P0-005)

| Attribute | Value |
|-----------|-------|
| **Risk ID** | RSK-P0-005 |
| **Description** | Dual repository sync complexity |
| **Severity** | 8 |
| **Occurrence** | 6 |
| **Detection** | 4 |
| **RPN** | 192 (HIGH) |
| **Root Cause** | Implicit knowledge; no sync process defined |
| **Mitigation** | This ADR |

### Constraints

| ID | Constraint | Source | Priority |
|----|------------|--------|----------|
| C-001 | Sync must be auditable | OSS governance | HARD |
| C-002 | No credentials may flow to public | Security | HARD |
| C-003 | Sync must not break public builds | CI/CD | HARD |
| C-004 | Contribution flow must be clear | Community UX | MEDIUM |
| C-005 | Process must be maintainable by one person | Team size | MEDIUM |
| C-006 | Sync must be reversible | Risk mitigation | MEDIUM |

### Forces

1. **Automation vs Manual Oversight:** Automated sync is faster but riskier; manual sync is safer but slower
2. **Frequency vs Complexity:** Continuous sync is simpler conceptually but complex operationally; release-based is opposite
3. **Security vs Speed:** More safety checks slow the process
4. **Bidirectional vs Unidirectional:** Bidirectional enables external contributions but creates merge complexity

---

## Options Considered

### Option A: Continuous Bidirectional Sync

**Description:** Continuously synchronize both repositories in both directions using git-sync or similar tooling.

**Implementation:**
```
source-repository <──────────────────────────────────────────► jerry
           │                                            │
           │     git-sync service (continuous)          │
           │         runs every 5 minutes               │
           └────────────────────────────────────────────┘
```

**Pros:**
- Always in sync (no drift)
- External contributions flow back automatically
- Minimal manual intervention after setup

**Cons:**
- **CRITICAL:** Bidirectional increases secret leak risk
- Complex conflict resolution
- Requires always-on infrastructure
- Merge conflicts may break both repos
- External PR contamination risk

**Fit with Constraints:**
- C-001: PARTIAL (automated, but audit trail complex)
- C-002: **FAILS** (bidirectional flow increases risk)
- C-003: **FAILS** (conflicts may break builds)
- C-004: PASSES
- C-005: **FAILS** (complex to maintain)
- C-006: **FAILS** (hard to reverse continuous sync)

**Risk Assessment:** Creates more problems than it solves. **REJECTED.**

### Option B: Unidirectional Release-Based Sync (RECOMMENDED)

**Description:** Sync from internal to public only, triggered manually at each release milestone.

**Implementation:**
```
RELEASE WORKFLOW (Triggered at v0.3.0, v0.4.0, etc.)

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  1. PREPARE                    2. VALIDATE                         │
│  ┌───────────────┐            ┌───────────────┐                    │
│  │ Create sync   │            │ Run safety    │                    │
│  │ branch from   │──────────► │ checks:       │                    │
│  │ source-repository    │            │ - Gitleaks    │                    │
│  │               │            │ - Allowlist   │                    │
│  └───────────────┘            │ - Build test  │                    │
│                               └───────┬───────┘                    │
│                                       │                            │
│  3. REVIEW                           ▼                             │
│  ┌───────────────┐            ┌───────────────┐                    │
│  │ Human reviews │◄───────────│ Generate diff │                    │
│  │ changes:      │            │ report:       │                    │
│  │ - File list   │            │ - Added       │                    │
│  │ - Secrets     │            │ - Modified    │                    │
│  │ - Sensitive   │            │ - Removed     │                    │
│  └───────┬───────┘            └───────────────┘                    │
│          │                                                         │
│          ▼                                                         │
│  4. PUSH                       5. VERIFY                           │
│  ┌───────────────┐            ┌───────────────┐                    │
│  │ Push to       │──────────► │ Public CI     │                    │
│  │ jerry public  │            │ builds and    │                    │
│  │ repository    │            │ tests pass    │                    │
│  └───────────────┘            └───────────────┘                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Token Budget:** N/A (process, not context loading)

**Pros:**
- **Clear direction** (internal → public, never reverse)
- **Human gate** ensures no accidental exposure
- **Release-aligned** simplifies versioning
- **Auditable** with clear sync points
- **Manageable** by one person
- **Reversible** (public repo can be reset to previous sync point)

**Cons:**
- Drift between releases (acceptable if releases are regular)
- External contributions require manual port
- More manual steps per release

**Fit with Constraints:**
- C-001: **PASSES** (clear audit trail at each sync point)
- C-002: **PASSES** (explicit allowlist + secret scanning)
- C-003: **PASSES** (build verification before push)
- C-004: PARTIAL (external PRs require manual port)
- C-005: **PASSES** (simple workflow)
- C-006: **PASSES** (can reset public to previous state)

### Option C: Git Subtree Sync

**Description:** Use git subtree to maintain public-facing code as a subtree within internal repo.

**Implementation:**
```
source-repository/
├── .subtree-config
├── public/                    ← git subtree (maps to jerry repo)
│   ├── .claude/
│   ├── skills/
│   ├── src/
│   └── ...
├── internal/                  ← Internal-only code
│   └── proprietary/
└── projects/                  ← Internal-only projects
```

**Pros:**
- Single source of truth for editing
- Atomic commits include public changes
- Git-native (no external tooling)

**Cons:**
- **Complex git operations** (subtree push/pull)
- History can become convoluted
- Developers must understand subtree
- Subtree conflicts are difficult to resolve

**Fit with Constraints:**
- C-001: PASSES
- C-002: PARTIAL (depends on .gitattributes discipline)
- C-003: PARTIAL (subtree push may fail)
- C-004: PARTIAL (complex for contributors)
- C-005: **FAILS** (subtree expertise required)
- C-006: PARTIAL

### Option D: Git Submodule Pattern

**Description:** Keep public repo as a git submodule within internal repo.

**Implementation:**
```
source-repository/
├── .gitmodules
├── jerry-public/              ← git submodule (jerry repo)
│   ├── .claude/
│   └── ...
├── internal/
└── projects/
```

**Pros:**
- Clear separation of public/internal
- Submodule has independent history
- Standard git workflow

**Cons:**
- Submodule versioning confusion
- Two-step commits required
- Clone complexity (--recurse-submodules)
- Detached HEAD issues

**Fit with Constraints:**
- C-001: PASSES
- C-002: PASSES (submodule is isolated)
- C-003: PARTIAL (submodule version pinning issues)
- C-004: **FAILS** (confusing for contributors)
- C-005: PARTIAL
- C-006: PASSES

### Option E: Separate Development with Manual Cherry-Pick

**Description:** Develop independently in both repos; manually cherry-pick changes as needed.

**Implementation:**
- No automated sync
- Changes manually ported via cherry-pick
- Each repo has independent history

**Pros:**
- Maximum control
- No sync infrastructure
- Clear isolation

**Cons:**
- **High drift risk**
- Significant manual effort
- Cherry-pick conflicts accumulate
- Easy to forget to sync

**Fit with Constraints:**
- C-001: PARTIAL (manual = audit gaps)
- C-002: PASSES (human review each change)
- C-003: PARTIAL (if testing neglected)
- C-004: PARTIAL
- C-005: **FAILS** (unsustainable manual effort)
- C-006: PASSES

**Risk Assessment:** Does not scale. **REJECTED.**

---

## Decision

**We will use Option B: Unidirectional Release-Based Sync.**

### Rationale

1. **Security-First:** Unidirectional flow (internal → public) with explicit allowlisting minimizes secret exposure risk

2. **Sustainable:** Release-based cadence is maintainable by a single developer, avoiding continuous sync overhead

3. **Auditable:** Each sync point creates a clear audit trail with:
   - Sync commit on public repo
   - Diff report archived
   - Human approval recorded

4. **Aligned with Release Workflow:** Syncing at releases ensures:
   - Version parity between repos
   - Tested code before public push
   - Clear changelog for each sync

5. **External Contribution Handling:** While manual porting of external PRs adds work, it provides:
   - Code review opportunity
   - Opportunity to adapt for internal use
   - Clear attribution trail

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | **HIGH** | Meets 5/6 fully, 1/6 partially |
| Risk Level | **LOW** | Human gate prevents most failure modes |
| Implementation Effort | **M** (4-6 hours) | GitHub Actions + scripts |
| Maintainability | **HIGH** | Simple workflow, one person can operate |
| Reversibility | **HIGH** | Can reset public repo to any prior sync point |

---

## L1: Technical Details (Engineer)

### Sync Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Jerry Repository Sync Architecture                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                        source-repository (internal)                       │ │
│  ├───────────────────────────────────────────────────────────────────┤ │
│  │                                                                   │ │
│  │  SYNC-INCLUDED (allowlist)          SYNC-EXCLUDED (blocklist)    │ │
│  │  ┌─────────────────────────┐       ┌─────────────────────────┐   │ │
│  │  │ .claude/                │       │ projects/               │   │ │
│  │  │ .claude-plugin/         │       │ internal/               │   │ │
│  │  │ skills/                 │       │ .env*                   │   │ │
│  │  │ src/                    │       │ secrets/                │   │ │
│  │  │ scripts/                │       │ *.local.*               │   │ │
│  │  │ hooks/                  │       │ node_modules/           │   │ │
│  │  │ docs/                   │       │ .jerry/                 │   │ │
│  │  │ tests/                  │       │ transcripts/            │   │ │
│  │  │ CLAUDE.md               │       │ *.pem                   │   │ │
│  │  │ README.md               │       │ *.key                   │   │ │
│  │  │ LICENSE                 │       │ *credentials*           │   │ │
│  │  │ SECURITY.md             │       │ *secret*                │   │ │
│  │  │ CONTRIBUTING.md         │       │ .git-sync*              │   │ │
│  │  │ CODE_OF_CONDUCT.md      │       │                         │   │ │
│  │  │ CHANGELOG.md            │       │                         │   │ │
│  │  │ pyproject.toml          │       │                         │   │ │
│  │  │ uv.lock                 │       │                         │   │ │
│  │  │ requirements.txt        │       │                         │   │ │
│  │  │ .github/ (workflows)    │       │                         │   │ │
│  │  └─────────────────────────┘       └─────────────────────────┘   │ │
│  │                                                                   │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                              │                                          │
│                              │ SYNC WORKFLOW                            │
│                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                      .github/workflows/sync-to-public.yml          │ │
│  ├───────────────────────────────────────────────────────────────────┤ │
│  │                                                                   │ │
│  │  STEP 1: Checkout        STEP 2: Filter        STEP 3: Validate  │ │
│  │  ┌──────────────┐       ┌──────────────┐      ┌──────────────┐   │ │
│  │  │ git clone    │──────►│ rsync with   │─────►│ gitleaks     │   │ │
│  │  │ source-repository   │       │ --exclude    │      │ scan         │   │ │
│  │  │              │       │ patterns     │      │              │   │ │
│  │  └──────────────┘       └──────────────┘      └──────┬───────┘   │ │
│  │                                                       │          │ │
│  │  STEP 4: Build Test      STEP 5: Diff Report    STEP 6: Approve │ │
│  │  ┌──────────────┐       ┌──────────────┐      ┌──────────────┐   │ │
│  │  │ uv sync      │◄──────│ Generate     │◄─────│ Manual       │   │ │
│  │  │ pytest       │       │ markdown     │      │ review       │   │ │
│  │  │              │       │ diff report  │      │ (required)   │   │ │
│  │  └──────────────┘       └──────────────┘      └──────┬───────┘   │ │
│  │                                                       │          │ │
│  │  STEP 7: Push                                                    │ │
│  │  ┌────────────────────────────────────────────────────────────┐  │ │
│  │  │ git push to jerry (public) with sync commit message        │  │ │
│  │  │ Format: "sync: Sync from source-repository vX.Y.Z [YYYY-MM-DD]"   │  │ │
│  │  └────────────────────────────────────────────────────────────┘  │ │
│  │                                                                   │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                              │                                          │
│                              ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                        jerry (public)                              │ │
│  ├───────────────────────────────────────────────────────────────────┤ │
│  │                                                                   │ │
│  │  Synced content from source-repository (no projects/, internal/, etc.)  │ │
│  │                                                                   │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Sync Configuration Files

#### `.sync-config.yaml` (in source-repository root)

```yaml
# Jerry Repository Sync Configuration
# This file defines what content syncs from source-repository to jerry (public)

version: "1.0"
target_repo: "geekatron/jerry"
source_branch: "main"
target_branch: "main"

# Explicit allowlist - ONLY these paths are synced
include:
  - ".claude/"
  - ".claude-plugin/"
  - ".context/"
  - ".github/workflows/"
  - ".github/ISSUE_TEMPLATE/"
  - ".github/PULL_REQUEST_TEMPLATE.md"
  - "skills/"
  - "src/"
  - "scripts/"
  - "hooks/"
  - "docs/"
  - "tests/"
  - "CLAUDE.md"
  - "README.md"
  - "LICENSE"
  - "SECURITY.md"
  - "CONTRIBUTING.md"
  - "CODE_OF_CONDUCT.md"
  - "CHANGELOG.md"
  - "pyproject.toml"
  - "uv.lock"
  - "requirements.txt"
  - "pytest.ini"
  - ".pre-commit-config.yaml"
  - ".editorconfig"
  - ".gitignore"
  - "AGENTS.md"

# Explicit blocklist - these are NEVER synced (safety net)
exclude:
  - "projects/"
  - "internal/"
  - "transcripts/"
  - ".jerry/"
  - ".env"
  - ".env.*"
  - "*.local.*"
  - "secrets/"
  - "*.pem"
  - "*.key"
  - "*credentials*"
  - "*secret*"
  - "node_modules/"
  - "__pycache__/"
  - ".git-sync*"
  - ".sync-config.yaml"  # This config itself is internal
  - "orchestration/"      # Orchestration plans are internal

# Safety checks (all must pass before sync)
safety_checks:
  gitleaks: true
  build_test: true
  pytest: true
  human_approval: true

# Commit message template
commit_template: |
  sync: Sync from source-repository v{version} [{date}]

  Changes:
  {change_summary}

  Files: {file_count} modified, {added_count} added, {removed_count} removed

  Synced-By: {syncer}
  Sync-SHA: {source_sha}
```

### GitHub Actions Workflow

#### `.github/workflows/sync-to-public.yml`

```yaml
name: Sync to Public Repository

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version being synced (e.g., v0.3.0)'
        required: true
      dry_run:
        description: 'Dry run (generate report only, no push)'
        type: boolean
        default: true
      skip_tests:
        description: 'Skip pytest (use only if tests already passed)'
        type: boolean
        default: false

env:
  PUBLIC_REPO: geekatron/jerry
  SYNC_BRANCH: sync-${{ github.event.inputs.version }}

jobs:
  prepare-sync:
    name: Prepare Sync Package
    runs-on: ubuntu-latest
    outputs:
      sync_sha: ${{ steps.prepare.outputs.sha }}

    steps:
      - name: Checkout source-repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Read sync configuration
        id: config
        run: |
          # Parse .sync-config.yaml and set outputs
          echo "Configuration loaded"

      - name: Create sync directory
        id: prepare
        run: |
          mkdir -p sync-package

          # Copy allowlisted content only
          rsync -av --progress \
            --include-from=.sync-include \
            --exclude-from=.sync-exclude \
            . sync-package/

          # Record source SHA
          echo "sha=$(git rev-parse HEAD)" >> $GITHUB_OUTPUT

      - name: Upload sync package
        uses: actions/upload-artifact@v4
        with:
          name: sync-package
          path: sync-package/
          retention-days: 7

  security-scan:
    name: Security Scan
    needs: prepare-sync
    runs-on: ubuntu-latest

    steps:
      - name: Download sync package
        uses: actions/download-artifact@v4
        with:
          name: sync-package
          path: sync-package/

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        with:
          path: sync-package/
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Scan for sensitive patterns
        run: |
          echo "Scanning for sensitive patterns..."

          # Custom pattern scan
          PATTERNS=(
            "password"
            "secret"
            "api_key"
            "apikey"
            "token"
            "credential"
            "private_key"
          )

          for pattern in "${PATTERNS[@]}"; do
            if grep -ri "$pattern" sync-package/ --include="*.py" --include="*.md" --include="*.yaml" --include="*.json" | grep -v "# Example" | grep -v "placeholder"; then
              echo "::warning::Found potential sensitive pattern: $pattern"
            fi
          done

  build-test:
    name: Build and Test
    needs: prepare-sync
    runs-on: ubuntu-latest
    if: ${{ !inputs.skip_tests }}

    steps:
      - name: Download sync package
        uses: actions/download-artifact@v4
        with:
          name: sync-package
          path: sync-package/

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install UV
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        working-directory: sync-package
        run: uv sync

      - name: Run tests
        working-directory: sync-package
        run: uv run pytest tests/ -v --tb=short

      - name: Type check
        working-directory: sync-package
        run: uv run mypy src/ --ignore-missing-imports

  generate-diff-report:
    name: Generate Diff Report
    needs: [prepare-sync, security-scan, build-test]
    runs-on: ubuntu-latest
    if: always() && needs.prepare-sync.result == 'success'

    steps:
      - name: Download sync package
        uses: actions/download-artifact@v4
        with:
          name: sync-package
          path: sync-package/

      - name: Checkout public repo
        uses: actions/checkout@v4
        with:
          repository: ${{ env.PUBLIC_REPO }}
          path: public-repo/
          token: ${{ secrets.SYNC_PAT }}

      - name: Generate diff report
        id: diff
        run: |
          echo "# Sync Diff Report" > diff-report.md
          echo "" >> diff-report.md
          echo "**Version:** ${{ github.event.inputs.version }}" >> diff-report.md
          echo "**Date:** $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> diff-report.md
          echo "**Source SHA:** ${{ needs.prepare-sync.outputs.sync_sha }}" >> diff-report.md
          echo "" >> diff-report.md

          echo "## File Changes" >> diff-report.md
          echo "" >> diff-report.md

          # Compare directories
          diff -rq sync-package/ public-repo/ --exclude=".git" > changes.txt || true

          ADDED=$(grep "Only in sync-package" changes.txt | wc -l)
          REMOVED=$(grep "Only in public-repo" changes.txt | wc -l)
          MODIFIED=$(grep "differ" changes.txt | wc -l)

          echo "- **Added:** $ADDED files" >> diff-report.md
          echo "- **Removed:** $REMOVED files" >> diff-report.md
          echo "- **Modified:** $MODIFIED files" >> diff-report.md
          echo "" >> diff-report.md

          echo "### Added Files" >> diff-report.md
          grep "Only in sync-package" changes.txt >> diff-report.md || echo "None" >> diff-report.md
          echo "" >> diff-report.md

          echo "### Removed Files" >> diff-report.md
          grep "Only in public-repo" changes.txt >> diff-report.md || echo "None" >> diff-report.md
          echo "" >> diff-report.md

          echo "### Modified Files" >> diff-report.md
          grep "differ" changes.txt >> diff-report.md || echo "None" >> diff-report.md

      - name: Upload diff report
        uses: actions/upload-artifact@v4
        with:
          name: diff-report
          path: diff-report.md

      - name: Comment on PR (if exists)
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('diff-report.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: report
            });

  manual-approval:
    name: Manual Approval Gate
    needs: [security-scan, build-test, generate-diff-report]
    runs-on: ubuntu-latest
    if: ${{ !inputs.dry_run }}
    environment: production-sync

    steps:
      - name: Approval checkpoint
        run: |
          echo "Sync approved by manual review."
          echo "Proceeding with push to public repository."

  push-to-public:
    name: Push to Public Repository
    needs: [prepare-sync, manual-approval]
    runs-on: ubuntu-latest
    if: ${{ !inputs.dry_run }}

    steps:
      - name: Download sync package
        uses: actions/download-artifact@v4
        with:
          name: sync-package
          path: sync-package/

      - name: Checkout public repo
        uses: actions/checkout@v4
        with:
          repository: ${{ env.PUBLIC_REPO }}
          path: public-repo/
          token: ${{ secrets.SYNC_PAT }}

      - name: Sync files
        run: |
          # Remove all tracked files except .git
          cd public-repo
          git rm -rf . || true
          cd ..

          # Copy sync package content
          cp -r sync-package/* public-repo/

      - name: Commit and push
        working-directory: public-repo
        run: |
          git config user.name "Jerry Sync Bot"
          git config user.email "sync-bot@jerry.dev"

          git add -A

          # Generate commit message
          COMMIT_MSG="sync: Sync from source-repository ${{ github.event.inputs.version }} [$(date -u +%Y-%m-%d)]

          Synced from source-repository commit: ${{ needs.prepare-sync.outputs.sync_sha }}
          Triggered by: ${{ github.actor }}

          Workflow run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"

          git commit -m "$COMMIT_MSG" || echo "No changes to commit"
          git push origin main

      - name: Create release tag
        working-directory: public-repo
        run: |
          git tag -a "${{ github.event.inputs.version }}" -m "Release ${{ github.event.inputs.version }}"
          git push origin "${{ github.event.inputs.version }}"
```

### Handling External Contributions

External contributions (PRs to public jerry repo) require manual porting:

```
┌─────────────────────────────────────────────────────────────────────┐
│                  External Contribution Flow                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. PR submitted to jerry (public)                                  │
│     │                                                               │
│     ▼                                                               │
│  2. Maintainer reviews PR                                           │
│     │                                                               │
│     ├─── ACCEPT ───────────────────────────────────────────────┐    │
│     │                                                          │    │
│     │  3. Create corresponding branch in source-repository            │    │
│     │     │                                                    │    │
│     │     ▼                                                    │    │
│     │  4. Cherry-pick or re-implement changes                  │    │
│     │     │                                                    │    │
│     │     ▼                                                    │    │
│     │  5. Add to internal CI/tests                             │    │
│     │     │                                                    │    │
│     │     ▼                                                    │    │
│     │  6. Merge to source-repository main                             │    │
│     │     │                                                    │    │
│     │     ▼                                                    │    │
│     │  7. Merge original PR in jerry (public)                  │    │
│     │     │                                                    │    │
│     │     ▼                                                    │    │
│     │  8. Add attribution in CHANGELOG                         │    │
│     │                                                          │    │
│     └─── REJECT ───────────────────────────────────────────────┘    │
│          │                                                          │
│          ▼                                                          │
│     Close PR with explanation                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Implementation Checklist

| # | Task | Effort | Owner | Verification |
|---|------|--------|-------|--------------|
| 1 | Create `.sync-config.yaml` in source-repository | 30 min | DevOps | File exists with valid YAML |
| 2 | Create `.sync-include` and `.sync-exclude` pattern files | 15 min | DevOps | rsync test runs successfully |
| 3 | Implement `sync-to-public.yml` workflow | 2 hours | DevOps | Workflow appears in Actions |
| 4 | Create `production-sync` environment in GitHub | 15 min | Admin | Environment with protection rules |
| 5 | Generate `SYNC_PAT` with repo scope | 15 min | Admin | Secret added to source-repository |
| 6 | Test dry-run sync | 30 min | DevOps | Diff report generated |
| 7 | Test full sync to public | 30 min | DevOps | Public repo updated |
| 8 | Create RUNBOOK-OSS-SYNC.md | 1 hour | Docs | Runbook exists with procedures |
| 9 | Add drift detection workflow | 1 hour | DevOps | Weekly drift check runs |
| 10 | Document external contribution process | 30 min | Docs | CONTRIBUTING.md updated |

**Total Effort:** ~6-7 hours

### Drift Detection Workflow

To catch drift before it becomes problematic:

```yaml
# .github/workflows/drift-detection.yml
name: Drift Detection

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
  workflow_dispatch:

jobs:
  check-drift:
    name: Check Repository Drift
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source-repository
        uses: actions/checkout@v4
        with:
          path: internal/

      - name: Checkout jerry (public)
        uses: actions/checkout@v4
        with:
          repository: geekatron/jerry
          path: public/

      - name: Compare repositories
        run: |
          # Apply same filters as sync
          rsync -av --dry-run \
            --include-from=internal/.sync-include \
            --exclude-from=internal/.sync-exclude \
            internal/ filtered-internal/

          # Compare filtered internal with public
          DRIFT_COUNT=$(diff -rq filtered-internal/ public/ --exclude=".git" | wc -l)

          if [ $DRIFT_COUNT -gt 0 ]; then
            echo "::warning::Drift detected: $DRIFT_COUNT differences found"
            diff -rq filtered-internal/ public/ --exclude=".git" > drift-report.txt
            cat drift-report.txt
          else
            echo "No drift detected. Repositories are in sync."
          fi

      - name: Create issue if drift detected
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Repository drift detected',
              body: 'The drift detection workflow found differences between source-repository and jerry (public). Please review and sync.',
              labels: ['drift', 'sync-required']
            });
```

---

## L2: Strategic Implications (Architect)

### Trade-off Analysis

| Factor | Option A (Bidirectional) | Option B (Release-Based) | Option C (Subtree) | Option D (Submodule) |
|--------|--------------------------|--------------------------|--------------------|--------------------|
| Security risk | **HIGH** | **LOW** | MEDIUM | LOW |
| Operational complexity | HIGH | **LOW** | MEDIUM | MEDIUM |
| Drift risk | **LOW** | MEDIUM | LOW | MEDIUM |
| External contribution UX | **HIGH** | MEDIUM | LOW | LOW |
| Maintainability (1 person) | LOW | **HIGH** | LOW | MEDIUM |
| Reversibility | LOW | **HIGH** | MEDIUM | HIGH |
| Audit trail | MEDIUM | **HIGH** | MEDIUM | MEDIUM |
| **Recommendation** | REJECT | **SELECTED** | Consider | Alternative |

### One-Way Door Assessment

| Aspect | Reversibility | Assessment |
|--------|---------------|------------|
| Repository structure | **HIGH** | Can always merge repos later if needed |
| Sync workflow | **HIGH** | Workflow can be disabled/modified |
| Public repo state | **HIGH** | Can force-push to any prior sync state |
| External contributions | **MEDIUM** | May have community expectations to manage |
| Tooling investments | **HIGH** | GitHub Actions portable to other approaches |

**Conclusion:** This is a **TWO-WAY DOOR** decision. All aspects are reversible.

### Failure Mode Analysis

| Failure Mode | Probability | Impact | Detection | Mitigation |
|--------------|-------------|--------|-----------|------------|
| Secret accidentally synced | LOW | **CRITICAL** | Gitleaks scan | Allowlist + human review + immediate rotation runbook |
| Sync breaks public build | MEDIUM | HIGH | CI in workflow | Build test before push |
| Drift grows too large | MEDIUM | MEDIUM | Drift detection | Weekly automated check + issue creation |
| External PRs lost/forgotten | MEDIUM | MEDIUM | PR tracking | Monthly review of open external PRs |
| Sync PAT expires/revoked | LOW | MEDIUM | Workflow failure | Secret rotation reminder (quarterly) |
| Human approval bottleneck | LOW | LOW | Sync delays | Multiple authorized approvers |

### Design Rationale

#### Why Unidirectional?

Bidirectional sync creates a **category of failure modes** that unidirectional avoids:

1. **Merge conflicts** in shared files
2. **External malicious PRs** flowing to internal repo
3. **Untested external code** in internal codebase
4. **Attribution complexity** for license compliance

By making the sync strictly internal → public, we:
- Maintain internal repo as source of truth
- Control what becomes public at each release
- Simplify the mental model for developers

#### Why Release-Based (Not Continuous)?

| Continuous Sync | Release-Based Sync |
|-----------------|-------------------|
| Requires always-on infrastructure | Batch process at release time |
| Small drift, frequently | Larger drift, less frequently |
| Conflict resolution at any time | Conflict resolution at release |
| Complex failure recovery | Simple: revert and retry |

For a single-developer or small team, **release-based is sustainable**. Continuous sync requires monitoring, alerting, and 24/7 conflict resolution capability.

#### Why Human Approval Gate?

Despite automation reducing risk, the **human gate** provides:

1. **Final sanity check** before public exposure
2. **Legal compliance** (someone signs off on what's released)
3. **Forced pause** to review diff report
4. **Audit trail** for who approved each sync

The 15-30 minute review time is acceptable at release cadence (not continuous).

### Detection Improvement (FMEA)

Per FMEA analysis in the risk register, improving detection reduces RPN:

| Current State | Improved State | RPN Impact |
|---------------|----------------|------------|
| Detection = 4 (user reports drift) | Detection = 2 (automated drift check + alerting) | 192 → 96 (-50%) |

Implementing the drift detection workflow directly addresses the detection gap.

### Industry Precedent

| Project | Sync Strategy | Notes |
|---------|---------------|-------|
| **Chromium** | Merge from internal monorepo | Very sophisticated tooling |
| **Android** | AOSP ← Google internal | Release-based, large batches |
| **VS Code** | Single public repo | No dual-repo complexity |
| **React** | Single public repo | Facebook develops in public |
| **Kubernetes** | Multi-repo (SIGs) | Distributed ownership |

Most successful OSS projects avoid dual-repo complexity. Jerry's dual-repo is driven by specific IP protection needs (DEC-002), making the sync process a necessary operational cost.

---

## Consequences

### Positive Consequences

1. **Addresses RSK-P0-005:** Clear sync process with defined artifacts
2. **Security:** Multiple layers of protection against secret exposure
3. **Sustainability:** Maintainable by one person
4. **Auditability:** Clear trail of what was synced and when
5. **Reversibility:** Can reset to any prior state if issues arise
6. **Automation:** Reduces manual effort per sync to ~30 minutes

### Negative Consequences

1. **External contribution friction:** Manual porting adds latency
2. **Drift between releases:** If releases are infrequent, drift accumulates
3. **Operational overhead:** New process to learn and maintain
4. **Tooling dependency:** Relies on GitHub Actions and PAT management

### Neutral Consequences

1. **Initial setup effort:** One-time 6-7 hour investment
2. **Documentation:** RUNBOOK-OSS-SYNC.md must be maintained

### Residual Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Human approver unavailable | LOW | MEDIUM | Multiple authorized approvers |
| Gitleaks false negative | LOW | CRITICAL | Additional pattern scanning + quarterly audit |
| External contributors frustrated by process | MEDIUM | LOW | Clear CONTRIBUTING.md documentation |
| Sync process becomes stale | LOW | MEDIUM | Annual process review |

---

## Verification Requirements

This ADR links to the following Verification Requirements from the V&V Plan:

| VR ID | Requirement | Verification Method | Relevance |
|-------|-------------|---------------------|-----------|
| VR-006 | No credentials in git history | Gitleaks scan | Sync includes secret scanning |
| - | (New) Sync process documented | Inspection | RUNBOOK-OSS-SYNC.md exists |
| - | (New) Sync workflow functional | Demonstration | Dry-run produces expected output |
| - | (New) Drift detection operational | Test | Weekly check runs, creates issues |

**Note:** Additional VRs may need to be added to V&V Planning for sync-specific verification.

---

## Risk Traceability

| Risk ID | Description | RPN | Treatment |
|---------|-------------|-----|-----------|
| RSK-P0-005 | Dual repository sync complexity | 192 | **Directly addressed by this ADR** |
| RSK-P0-002 | Credential exposure in git history | 120 | **Partially addressed** (sync includes Gitleaks) |
| RSK-P0-008 | Schedule underestimation | 180 | Sync effort now estimated (6-7 hours setup) |

---

## Implementation

### Action Items

| # | Action | Owner | Priority | Due |
|---|--------|-------|----------|-----|
| 1 | Create `.sync-config.yaml` | DevOps | P1 | Day 1 |
| 2 | Implement sync workflow | DevOps | P1 | Day 1-2 |
| 3 | Create production-sync environment | Admin | P1 | Day 2 |
| 4 | Test dry-run sync | DevOps | P1 | Day 2 |
| 5 | Create RUNBOOK-OSS-SYNC.md | Docs | P1 | Day 3 |
| 6 | Document external contribution flow | Docs | P2 | Day 3 |
| 7 | Implement drift detection | DevOps | P2 | Day 4 |
| 8 | First production sync | DevOps | P1 | Release v0.3.0 |

### Validation Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Sync workflow operational | Passes dry-run | GitHub Actions success |
| Secret scanning active | 0 findings | Gitleaks output |
| Build passes after sync | Tests green | pytest exit code 0 |
| Diff report generated | Report artifact exists | Actions artifact download |
| Human approval required | Environment protection | GitHub settings verification |
| Drift detection scheduled | Weekly run | Actions schedule active |

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-OSS-001 | DEPENDS_ON | Decomposed CLAUDE.md must be synced |
| DEC-002 | IMPLEMENTS | This ADR implements the sync process for dual-repo strategy |
| ADR-OSS-003 (future) | RELATED_TO | Documentation strategy may affect what syncs |

---

## References

### Primary Sources

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | [DEC-002 Dual Repository Strategy](../../decisions/DEC-002-dual-repository.md) | Decision | Foundational decision requiring this sync process |
| 2 | [ps-analyst Root Cause 5 Whys](../../../ps/phase-1/ps-analyst/root-cause-5whys.md) | Analysis | RSK-P0-005 root cause analysis |
| 3 | [nse-explorer Divergent Alternatives](../../../nse/phase-0/nse-explorer/divergent-alternatives.md) | Exploration | Dual-repo risks and alternatives |
| 4 | [GitHub Actions Workflows](https://docs.github.com/en/actions/using-workflows) | Documentation | Workflow implementation reference |

### Phase 1 Analysis Sources

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 5 | phase-1-risk-register.md | Risk | RSK-P0-005 RPN 192 assessment |
| 6 | vv-planning.md | V&V | VR-006 (credential exposure) |
| 7 | ADR-OSS-001 | ADR | CLAUDE.md decomposition informs sync content |

### Industry References

| # | Reference | Relevance |
|---|-----------|-----------|
| 8 | [Gitleaks](https://github.com/gitleaks/gitleaks) | Secret scanning tool |
| 9 | [rsync](https://rsync.samba.org/) | File synchronization |
| 10 | [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment) | Manual approval gates |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ADR-OSS-002 |
| **Status** | PROPOSED |
| **Workflow** | oss-release-20260131-001 |
| **Phase** | 2 (ADR Creation) |
| **Agent** | ps-architect-002 |
| **Risk Addressed** | RSK-P0-005 (RPN 192 - HIGH) |
| **Decision Type** | Two-Way Door (Reversible) |
| **Implementation Effort** | 6-7 hours (setup), 30 min/sync (ongoing) |
| **Word Count** | ~5,800 |
| **Constitutional Compliance** | P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-022 (Honesty) |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-31 | ps-architect-002 | Initial ADR creation |

---

*This ADR was produced by ps-architect-002 for PROJ-009-oss-release Phase 2.*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-022 (Honesty)*
*Template: Michael Nygard ADR Format with Jerry L0/L1/L2 extensions*
