# ADR-OSS-005: Repository Migration Strategy

> **Workflow ID:** oss-release-20260131-001
> **Phase:** 2 (ADR Creation)
> **Agent:** ps-architect-005
> **Created:** 2026-01-31
> **Status:** PROPOSED
> **Risk Reference:** RSK-P0-005 (RPN 192 - HIGH), RSK-P0-008 (RPN 180 - HIGH)
> **Supersedes:** None
> **Depends On:** ADR-OSS-001 (CLAUDE.md Decomposition Strategy), ADR-OSS-002 (Repository Sync Process)
> **Constitutional Compliance:** P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence)

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

Imagine you have a house full of all your belongings - some are heirlooms you want to share with family (public), and some are personal items you want to keep private (internal). You've decided to buy a second house specifically for family gatherings.

The challenge is: **How do you move the right items to the new house without:**
- Accidentally moving personal items you shouldn't share
- Breaking fragile items during the move
- Losing track of what went where
- Being unable to move back if the new house has problems

Jerry faces this exact challenge. Per DEC-002 (Dual Repository Strategy), we need to split from one repository (internal) to two repositories:
- **internal repository** (private): Contains proprietary extensions, internal projects, development work
- **jerry** (public): The OSS version with curated, public-safe content

### The Solution

We will implement a **Staged Progressive Migration** with clear checkpoints:

```
PHASE 1: PREPARE (Day 1)
└── Create public repo skeleton, test sync pipeline

PHASE 2: INITIAL SYNC (Day 2)
└── First filtered copy, verify no secrets, validate builds

PHASE 3: STABILIZATION (Days 3-4)
└── Multi-day testing, user acceptance, documentation sync

PHASE 4: CUTOVER (Day 5)
└── Public release, dual-repo operational mode begins
```

### Key Numbers

| Metric | Value | Rationale |
|--------|-------|-----------|
| Migration phases | 4 | Provides checkpoints for validation and rollback |
| Content boundary | 65% public / 35% internal | Based on directory analysis |
| History approach | Clean start | Prevents credential exposure, reduces complexity |
| Rollback window | 7 days | Post-cutover safety period |
| Validation checkpoints | 6 | One per major step |

### Bottom Line

**RSK-P0-005 (RPN 192 - HIGH) and RSK-P0-008 (RPN 180 - HIGH) require a well-defined migration strategy.** Without clear sequencing, boundary definitions, and rollback plans, the dual-repo transition will introduce drift, confusion, and potential security incidents. This ADR defines the complete migration playbook from monorepo to dual-repo.

---

## Context

### Background

Per DEC-002 and ADR-OSS-002, Jerry will operate with a dual-repository strategy:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  Jerry Repository Structure After Migration              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CURRENT STATE                      TARGET STATE                        │
│  ══════════════                     ════════════                        │
│                                                                         │
│  ┌───────────────────┐              ┌───────────────────┐              │
│  │  internal repo    │              │  internal repo     │              │
│  │    (private)      │              │    (private)      │              │
│  │                   │              │                   │              │
│  │ ├── .claude/      │              │ ├── .claude/      │──────┐      │
│  │ ├── skills/       │              │ ├── skills/       │──────┤      │
│  │ ├── src/          │              │ ├── src/          │──────┤      │
│  │ ├── docs/         │              │ ├── docs/         │──────┤ SYNC │
│  │ ├── projects/     │              │ ├── projects/     │  X   │      │
│  │ ├── internal/     │              │ ├── internal/     │  X   │      │
│  │ └── transcripts/  │              │ ├── transcripts/  │  X   │      │
│  │                   │              │ └── .sync-config  │      │      │
│  └───────────────────┘              └───────────────────┘      │      │
│           │                                                    │      │
│           │                                                    ▼      │
│           │                         ┌───────────────────┐             │
│           │                         │      jerry        │             │
│           └─── MIGRATION ─────────► │     (public)      │◄────────────┘
│                                     │                   │              │
│                                     │ ├── .claude/      │              │
│                                     │ ├── skills/       │              │
│                                     │ ├── src/          │              │
│                                     │ ├── docs/         │              │
│                                     │ ├── README.md     │              │
│                                     │ ├── LICENSE       │              │
│                                     │ └── SECURITY.md   │              │
│                                     │                   │              │
│                                     │ (No projects/)    │              │
│                                     │ (No internal/)    │              │
│                                     │ (No transcripts/) │              │
│                                     └───────────────────┘              │
│                                                                         │
│  Legend: ───► = Migration flow, X = Excluded from sync                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### The Problem: Migration Complexity

The transition from monorepo to dual-repo involves multiple interconnected concerns:

1. **Content Filtering:** What goes to public vs. stays internal?
2. **History Handling:** Do we preserve git history or start clean?
3. **Sequencing:** What order do we extract and validate?
4. **Rollback:** How do we recover if migration fails?
5. **Validation:** How do we verify successful migration?

The root cause analysis (ps-analyst 5 Whys) identified **"Implicit Knowledge"** as a pattern:

```
WHY is migration undefined?
  └─ DEC-002 focused on end-state, not transition
WHY wasn't transition planned?
  └─ Strategic decision deferred operational details
WHY defer operational details?
  └─ Time pressure to make architecture decision
WHY time pressure?
  └─ ROOT CAUSE: Big decisions without full operational planning
```

### Dependency on Prior ADRs

This ADR builds on decisions from:

| ADR | Decision | Relevance to Migration |
|-----|----------|----------------------|
| **ADR-OSS-001** | CLAUDE.md decomposition to 60-80 lines | CLAUDE.md must be decomposed BEFORE migration |
| **ADR-OSS-002** | Unidirectional release-based sync | Sync process defines AFTER-migration operations |

**Migration is the bridge between current state and ADR-OSS-002's operational model.**

### Constraints

| ID | Constraint | Source | Priority |
|----|------------|--------|----------|
| C-001 | No credentials may appear in public repo | RSK-P0-002 | HARD |
| C-002 | Public repo must build and test successfully | CI/CD | HARD |
| C-003 | Migration must be reversible for 7 days | Risk mitigation | HARD |
| C-004 | Migration downtime < 4 hours | Developer productivity | MEDIUM |
| C-005 | All OSS requirements met before cutover | Requirements spec | HARD |
| C-006 | Clear audit trail of migration steps | Compliance | MEDIUM |

### Forces

1. **Speed vs Safety:** Fast migration risks exposure; slow migration extends maintenance burden
2. **History vs Clean Slate:** Full history preserves context but may expose secrets; clean start is safe but loses context
3. **Big Bang vs Progressive:** Single migration is simpler to execute but riskier; phased is safer but longer
4. **Automation vs Manual:** Automated is faster but may miss edge cases; manual is thorough but error-prone

---

## Options Considered

### Option A: Big Bang Migration

**Description:** Single-day migration with full extraction, validation, and cutover.

**Implementation:**
```
Day 1:
├── 0800: Create jerry (public) repo
├── 0900: Run filtered copy from internal repo
├── 1000: Gitleaks scan
├── 1100: Build verification
├── 1200: Human review
├── 1300: Push to public
├── 1400: Announce release
└── 1500: Monitor for issues
```

**Pros:**
- Fastest time-to-public (1 day)
- Minimal maintenance window
- Clear cut-over point

**Cons:**
- **CRITICAL:** No validation time between steps
- **HIGH:** Single point of failure
- **MEDIUM:** Pressure may cause mistakes
- Rollback is complex mid-migration
- No user acceptance testing

**Fit with Constraints:**
- C-001: **PARTIAL** (compressed review window)
- C-002: PASSES (build verification included)
- C-003: **PARTIAL** (rollback more difficult)
- C-004: **PASSES** (< 4 hours)
- C-005: **FAILS** (no UAT time)
- C-006: PASSES (audit trail possible)

**Risk Assessment:** HIGH risk due to compressed timeline and no validation periods.

### Option B: Staged Progressive Migration (RECOMMENDED)

**Description:** Multi-phase migration with validation checkpoints between each stage.

**Implementation:**
```
PHASE 1: PREPARE (Day 1)
├── Create jerry (public) repo (skeleton)
├── Configure GitHub settings
├── Create sync workflow (dry-run mode)
├── Run first dry-run sync
├── CHECKPOINT 1: Skeleton validated
└── Duration: 4 hours

PHASE 2: INITIAL SYNC (Day 2)
├── Execute filtered copy
├── Run Gitleaks scan (full)
├── Run build verification
├── Run test suite
├── CHECKPOINT 2: Build passes, no secrets
├── Human review of diff report
└── Duration: 6 hours

PHASE 3: STABILIZATION (Days 3-4)
├── Internal team uses public repo copy
├── Documentation sync verification
├── README/CONTRIBUTING/LICENSE review
├── User acceptance testing
├── CHECKPOINT 3: All VRs passed
├── CHECKPOINT 4: Team sign-off
└── Duration: 2 days

PHASE 4: CUTOVER (Day 5)
├── Final sync from internal repo
├── Enable public visibility
├── GitHub Topics/Description set
├── CHECKPOINT 5: Public repo live
├── Post-cutover monitoring (24h)
├── CHECKPOINT 6: Stability confirmed
└── Duration: 4 hours + 24h monitoring
```

**Pros:**
- **Validation at each phase** reduces risk
- **Rollback possible** at any checkpoint
- **User acceptance testing** included
- **Clear audit trail** with checkpoints
- Matches ADR-OSS-002's sync process
- Time for documentation completion

**Cons:**
- Longer timeline (5 days)
- More coordination required
- Maintenance of two repos during transition
- Team coordination needed

**Fit with Constraints:**
- C-001: **PASSES** (multiple scan opportunities)
- C-002: **PASSES** (build verification at each phase)
- C-003: **PASSES** (rollback built into phases)
- C-004: **PASSES** (actual downtime < 4 hours)
- C-005: **PASSES** (UAT in Phase 3)
- C-006: **PASSES** (checkpoint audit trail)

### Option C: Git Filter-Branch Migration

**Description:** Use git filter-branch to create a filtered copy with partial history.

**Implementation:**
```bash
# Create filtered clone with selected paths
git filter-branch --subdirectory-filter src/
git filter-branch --index-filter 'git rm --cached --ignore-unmatch projects/'
```

**Pros:**
- Preserves some git history
- Single command per filter
- Can retain commit attribution

**Cons:**
- **CRITICAL:** History may contain secrets even in non-removed paths
- **HIGH:** Complex to configure correctly
- **MEDIUM:** Rewritten SHAs break references
- Cannot easily undo filter-branch
- Deprecated in favor of git-filter-repo

**Fit with Constraints:**
- C-001: **FAILS** (history may contain secrets)
- C-002: PASSES
- C-003: **FAILS** (hard to reverse filter-branch)
- C-004: **PARTIAL** (depends on repo size)
- C-005: N/A
- C-006: PARTIAL

**Risk Assessment:** Unacceptable secret exposure risk.

### Option D: GitHub Repository Fork with Cleanup

**Description:** Fork the internal repository publicly, then remove internal content.

**Implementation:**
```
1. Fork internal repo to jerry
2. Delete projects/, internal/, transcripts/
3. Force push cleaned history
4. Run secret scans
```

**Pros:**
- GitHub native workflow
- Simple to execute
- Maintains fork relationship

**Cons:**
- **CRITICAL:** Initial fork exposes ALL content briefly
- **CRITICAL:** GitHub may cache removed content
- Fork relationship may confuse contributors
- Cannot truly remove from git history

**Fit with Constraints:**
- C-001: **FAILS** (initial exposure window)
- C-002: PASSES
- C-003: **PARTIAL** (fork can be deleted)
- C-004: PASSES
- C-005: N/A
- C-006: PARTIAL

**Risk Assessment:** CRITICAL exposure risk during fork window. **REJECTED.**

### Option E: Clean Start with Content Copy

**Description:** Create new public repo with no git history, copy only current content.

**Implementation:**
```bash
# Create new repo
gh repo create jerry --public

# Copy filtered content (no history)
rsync -av --exclude-from=.sync-exclude internal-repo/ jerry/

# Initialize as new git repo
cd jerry && git init && git add . && git commit -m "Initial OSS release"
```

**Pros:**
- **Zero history risk** - no secrets in history possible
- **Simple mental model** - no history to manage
- **Fast execution** - just file copy
- Clean contribution graph

**Cons:**
- **No git history** - lose attribution context
- **No commit archaeology** - can't trace changes
- Contributors can't see evolution
- May seem unprofessional (empty history)

**Fit with Constraints:**
- C-001: **PASSES** (no history = no secrets)
- C-002: PASSES
- C-003: **PASSES** (trivial to delete and retry)
- C-004: PASSES
- C-005: N/A
- C-006: PASSES

---

## Decision

**We will use Option B: Staged Progressive Migration with Option E's history approach (clean start).**

This hybrid provides:
1. **Option B's phases** for structured validation and rollback
2. **Option E's clean history** for zero secret exposure risk

### Rationale

1. **Security First:** RSK-P0-002 (credential exposure, RPN 120) is addressed by clean-start history. There is NO risk of secrets in git history because there is no history to expose.

2. **Validated Transition:** Six checkpoints provide clear go/no-go decision points. Each phase can be rolled back without affecting others.

3. **Alignment with ADR-OSS-002:** The sync workflow defined in ADR-OSS-002 becomes operational after Phase 4. The migration prepares the target state for that workflow.

4. **OSS Requirements Completion:** Phase 3 provides time for:
   - CLAUDE.md decomposition (ADR-OSS-001)
   - Documentation completion
   - All 6 CRITICAL requirements from Requirements Specification

5. **Risk Mitigation:** Multi-phase approach reduces:
   - RSK-P0-005 (sync complexity) - Migration validates sync process
   - RSK-P0-008 (schedule underestimation) - Phased approach provides buffer

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | **HIGH** | Meets all 6 constraints |
| Risk Level | **LOW** | Multiple validation points, clean history |
| Implementation Effort | **M** (5 days) | Phased with clear checkpoints |
| Reversibility | **HIGH** | Can rollback at any checkpoint |

---

## L1: Technical Details (Engineer)

### Migration Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Jerry Repository Migration Architecture                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHASE 1: PREPARE (Day 1)                                                   │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1.1 Create Public Repository                                         │   │
│  │     gh repo create geekatron/jerry --public --description "..."      │   │
│  │                                                                       │   │
│  │ 1.2 Configure Repository Settings                                    │   │
│  │     ├── Enable Issues                                                 │   │
│  │     ├── Disable Wiki (use docs/)                                      │   │
│  │     ├── Set default branch: main                                      │   │
│  │     ├── Add topics: claude-code, ai-agents, workflow-automation      │   │
│  │     └── Configure branch protection (after initial push)             │   │
│  │                                                                       │   │
│  │ 1.3 Create Environment for Sync                                      │   │
│  │     ├── Create 'production-sync' environment in GitHub               │   │
│  │     ├── Configure environment protection rules                        │   │
│  │     └── Generate SYNC_PAT with repo scope                            │   │
│  │                                                                       │   │
│  │ 1.4 Copy Sync Workflow (Dry-Run Mode)                                │   │
│  │     ├── Copy .sync-config.yaml from ADR-OSS-002                      │   │
│  │     ├── Copy sync-to-public.yml workflow                             │   │
│  │     └── Set dry_run: true for initial tests                          │   │
│  │                                                                       │   │
│  │ CHECKPOINT 1: □ Repo exists □ Settings applied □ Workflow ready      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  PHASE 2: INITIAL SYNC (Day 2)                                              │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2.1 Execute Filtered Content Copy                                    │   │
│  │     ├── rsync with include/exclude patterns                          │   │
│  │     ├── Verify file counts match expected                            │   │
│  │     └── Generate manifest of copied files                            │   │
│  │                                                                       │   │
│  │ 2.2 Security Scan                                                    │   │
│  │     ├── Gitleaks scan on all files                                   │   │
│  │     ├── Custom pattern scan (passwords, tokens, keys)                │   │
│  │     └── Review any flagged items                                     │   │
│  │                                                                       │   │
│  │ 2.3 Build Verification                                               │   │
│  │     ├── uv sync (dependencies install)                               │   │
│  │     ├── uv run pytest (tests pass)                                   │   │
│  │     ├── uv run mypy src/ (type checks pass)                          │   │
│  │     └── uv run ruff check src/ (linting passes)                      │   │
│  │                                                                       │   │
│  │ 2.4 Initial Commit                                                   │   │
│  │     ├── git init                                                      │   │
│  │     ├── git add .                                                     │   │
│  │     ├── git commit -m "Initial OSS release - Jerry Framework v0.3.0" │   │
│  │     └── git push -u origin main                                       │   │
│  │                                                                       │   │
│  │ 2.5 Human Review                                                     │   │
│  │     ├── Generate diff report                                          │   │
│  │     ├── Review critical files (CLAUDE.md, skills/, src/)             │   │
│  │     └── Sign-off on content completeness                             │   │
│  │                                                                       │   │
│  │ CHECKPOINT 2: □ Build passes □ No secrets □ Human reviewed          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  PHASE 3: STABILIZATION (Days 3-4)                                          │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3.1 Internal Team Testing (Day 3)                                    │   │
│  │     ├── Clone public repo (fresh machine test)                       │   │
│  │     ├── Follow README quick-start                                    │   │
│  │     ├── Invoke each skill (/worktracker, /problem-solving, etc.)    │   │
│  │     ├── Run CLI commands (jerry session start, etc.)                │   │
│  │     └── Document any issues                                          │   │
│  │                                                                       │   │
│  │ 3.2 Documentation Completion (Day 3-4)                               │   │
│  │     ├── Verify README.md has quick-start                             │   │
│  │     ├── Verify CONTRIBUTING.md exists                                │   │
│  │     ├── Verify LICENSE is MIT                                        │   │
│  │     ├── Verify SECURITY.md has disclosure process                    │   │
│  │     ├── Verify CODE_OF_CONDUCT.md exists                             │   │
│  │     └── Verify CHANGELOG.md has v0.3.0 entry                         │   │
│  │                                                                       │   │
│  │ 3.3 Verification Requirements Audit (Day 4)                          │   │
│  │     ├── Run VR-001 to VR-030 checks                                  │   │
│  │     ├── Run VAL-001 to VAL-005 validations                          │   │
│  │     ├── Calculate OSS readiness score                                │   │
│  │     └── Address any failing requirements                             │   │
│  │                                                                       │   │
│  │ CHECKPOINT 3: □ VRs pass □ VALs pass □ Readiness >= 0.85            │   │
│  │                                                                       │   │
│  │ 3.4 Team Sign-Off (Day 4)                                            │   │
│  │     ├── Internal stakeholder review                                  │   │
│  │     ├── Final content approval                                       │   │
│  │     └── Go/No-Go decision for cutover                                │   │
│  │                                                                       │   │
│  │ CHECKPOINT 4: □ Stakeholder approved □ Go decision made             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                     │                                       │
│                                     ▼                                       │
│  PHASE 4: CUTOVER (Day 5)                                                   │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4.1 Final Sync (if changes since Phase 2)                           │   │
│  │     ├── Run sync workflow                                            │   │
│  │     ├── Verify no new secrets                                        │   │
│  │     └── Merge to main                                                 │   │
│  │                                                                       │   │
│  │ 4.2 Enable Public Visibility                                         │   │
│  │     ├── Repository is already public (created in Phase 1)            │   │
│  │     ├── Enable GitHub Discussions (if desired)                       │   │
│  │     ├── Configure branch protection rules                            │   │
│  │     └── Enable Dependabot                                            │   │
│  │                                                                       │   │
│  │ 4.3 Announcement (if applicable)                                     │   │
│  │     ├── Create GitHub Release for v0.3.0                             │   │
│  │     ├── Tag version                                                   │   │
│  │     └── Update any external references                               │   │
│  │                                                                       │   │
│  │ CHECKPOINT 5: □ Public repo live □ Release tagged □ Visible         │   │
│  │                                                                       │   │
│  │ 4.4 Post-Cutover Monitoring (24 hours)                               │   │
│  │     ├── Monitor GitHub Issues for reports                            │   │
│  │     ├── Watch for security scan alerts                               │   │
│  │     ├── Verify no unexpected traffic                                 │   │
│  │     └── Confirm sync workflow operational                            │   │
│  │                                                                       │   │
│  │ CHECKPOINT 6: □ 24h stable □ No incidents □ Sync working            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Content Boundary Definition

The following defines what content migrates to the public repository:

#### INCLUDED in Public Repository (jerry)

```yaml
# Files and directories that WILL be synced to public
include:
  # Core Claude Code integration
  - ".claude/"
  - ".claude-plugin/"
  - "CLAUDE.md"
  - "AGENTS.md"

  # Skills (on-demand loading)
  - "skills/"

  # Source code
  - "src/"

  # Scripts and hooks
  - "scripts/"
  - "hooks/"

  # Documentation
  - "docs/"
  - ".context/templates/"

  # Tests
  - "tests/"

  # OSS standard files
  - "README.md"
  - "LICENSE"
  - "SECURITY.md"
  - "CONTRIBUTING.md"
  - "CODE_OF_CONDUCT.md"
  - "CHANGELOG.md"

  # Python project files
  - "pyproject.toml"
  - "uv.lock"
  - "requirements.txt"
  - "pytest.ini"

  # Editor/linter config
  - ".pre-commit-config.yaml"
  - ".editorconfig"
  - ".gitignore"
  - ".python-version"

  # GitHub configuration
  - ".github/workflows/"
  - ".github/ISSUE_TEMPLATE/"
  - ".github/PULL_REQUEST_TEMPLATE.md"
  - ".github/dependabot.yml"
  - ".github/CODEOWNERS"
```

#### EXCLUDED from Public Repository (stays in internal repository)

```yaml
# Files and directories that NEVER sync to public
exclude:
  # Internal projects and work
  - "projects/"
  - "orchestration/"

  # Proprietary/internal code
  - "internal/"

  # User-specific content
  - "transcripts/"

  # Operational state
  - ".jerry/"

  # Secrets and credentials
  - ".env"
  - ".env.*"
  - "*.local.*"
  - "secrets/"
  - "*.pem"
  - "*.key"
  - "*credentials*"
  - "*secret*"

  # Build artifacts
  - "node_modules/"
  - "__pycache__/"
  - "*.pyc"
  - ".pytest_cache/"
  - ".mypy_cache/"
  - ".ruff_cache/"
  - "dist/"
  - "build/"
  - "*.egg-info/"

  # Sync configuration (internal only)
  - ".sync-config.yaml"
  - ".sync-include"
  - ".sync-exclude"
  - ".git-sync*"
```

### History Approach: Clean Start

**Decision:** The public repository will have **no git history** from the internal repository.

**Rationale:**

| Consideration | Full History | Clean Start |
|---------------|--------------|-------------|
| Secret exposure risk | **HIGH** - must scan entire history | **ZERO** - no history to scan |
| Implementation complexity | HIGH - filter-branch/filter-repo | LOW - simple file copy |
| Contributor perception | Professional (history shows evolution) | Acceptable (common for OSS forks) |
| Archaeology capability | Full (git blame, bisect work) | None (starts fresh) |
| Rollback complexity | HIGH | LOW |

**Mitigation for Clean Start Cons:**

1. **Contributor Attribution:** Include CONTRIBUTORS.md acknowledging prior contributors
2. **Evolution Context:** First commit message references internal development period
3. **Blame Capability:** Internal repo retains full history for reference

**Initial Commit Message Template:**

```
Initial OSS release - Jerry Framework v0.3.0

Jerry is a framework for behavior and workflow guardrails that helps
solve problems while accruing a body of knowledge, wisdom, and experience.

This represents the initial open-source release. Prior development
occurred in a private repository. See CONTRIBUTORS.md for attribution.

Core features:
- Claude Code integration (.claude/, skills/)
- Work tracking system (Canonical entity model)
- Problem-solving frameworks (5W2H, FMEA, 8D)
- Multi-agent orchestration
- Jerry Constitution for agent governance

Documentation: See README.md for quick start
License: MIT
```

### Rollback Strategy

Each phase has a defined rollback procedure:

```
ROLLBACK PROCEDURES BY PHASE
═══════════════════════════════════════════════════════════════════════════

PHASE 1 ROLLBACK: Delete public repo
┌─────────────────────────────────────────────────────────────────────────┐
│ Trigger: Configuration issues, settings wrong                           │
│ Action:  gh repo delete geekatron/jerry --yes                          │
│ Impact:  Zero - nothing public yet                                       │
│ Time:    5 minutes                                                       │
└─────────────────────────────────────────────────────────────────────────┘

PHASE 2 ROLLBACK: Reset public repo
┌─────────────────────────────────────────────────────────────────────────┐
│ Trigger: Secrets found, build fails, content issues                     │
│ Action:                                                                  │
│   1. Remove all commits: git update-ref -d HEAD                         │
│   2. Force push empty: git push --force                                  │
│   3. Re-run Phase 2 with fixes                                          │
│ Impact:  Low - internal testing only                                     │
│ Time:    1 hour                                                          │
└─────────────────────────────────────────────────────────────────────────┘

PHASE 3 ROLLBACK: Reset and defer
┌─────────────────────────────────────────────────────────────────────────┐
│ Trigger: VR failures, UAT failures, documentation gaps                  │
│ Action:                                                                  │
│   1. Document blocking issues                                            │
│   2. Reset public repo (same as Phase 2)                                │
│   3. Address issues in internal repo                                     │
│   4. Re-start from Phase 2                                              │
│ Impact:  Medium - delays timeline 2-3 days                              │
│ Time:    2-4 hours                                                       │
└─────────────────────────────────────────────────────────────────────────┘

PHASE 4 ROLLBACK: Archive and retry (7-day window)
┌─────────────────────────────────────────────────────────────────────────┐
│ Trigger: Post-cutover incidents, security issues discovered            │
│ Action:                                                                  │
│   1. Make repo private immediately: gh repo edit --visibility private   │
│   2. Create incident report                                              │
│   3. Address issues in internal repo                                     │
│   4. Option A: Fix and re-publish                                       │
│   5. Option B: Delete and restart from Phase 1                          │
│ Impact:  High - public visibility affected, need communication          │
│ Time:    Variable                                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Validation Checkpoints

Each checkpoint has explicit pass/fail criteria:

| Checkpoint | Phase | Pass Criteria | Fail Action |
|------------|-------|---------------|-------------|
| **CP-1** | 1 (Prepare) | Repo exists, settings match spec, workflow present | Fix and retry |
| **CP-2** | 2 (Initial Sync) | Build passes, Gitleaks clean, human approved | Rollback Phase 2 |
| **CP-3** | 3 (Stabilization) | VR-001 to VR-030 pass, VAL pass, score >= 0.85 | Defer to fix |
| **CP-4** | 3 (Stabilization) | Stakeholder sign-off received | Defer to address concerns |
| **CP-5** | 4 (Cutover) | Repo public, release tagged, accessible | Rollback Phase 4 |
| **CP-6** | 4 (Cutover) | 24h stable, no incidents, sync working | Investigate and fix |

### Implementation Checklist

| # | Phase | Task | Duration | Owner | Verification |
|---|-------|------|----------|-------|--------------|
| 1.1 | 1 | Create jerry repo | 15 min | DevOps | `gh repo view geekatron/jerry` |
| 1.2 | 1 | Configure repo settings | 15 min | DevOps | Settings match spec |
| 1.3 | 1 | Create production-sync environment | 15 min | Admin | Environment visible in Settings |
| 1.4 | 1 | Generate and store SYNC_PAT | 15 min | Admin | Secret in internal repository |
| 1.5 | 1 | Copy sync workflow (dry-run) | 30 min | DevOps | Workflow appears in Actions |
| 1.6 | 1 | Run first dry-run | 30 min | DevOps | Workflow completes successfully |
| 2.1 | 2 | Execute rsync copy | 30 min | DevOps | File counts verified |
| 2.2 | 2 | Run Gitleaks scan | 30 min | Security | 0 findings |
| 2.3 | 2 | Run build verification | 30 min | DevOps | pytest/mypy/ruff pass |
| 2.4 | 2 | Create initial commit | 15 min | DevOps | Commit on main |
| 2.5 | 2 | Human review | 2 hours | Team Lead | Sign-off documented |
| 3.1 | 3 | Fresh clone test | 2 hours | QA | All skills work |
| 3.2 | 3 | Documentation completion | 4 hours | Docs | All required files present |
| 3.3 | 3 | VR/VAL audit | 4 hours | QA | Score >= 0.85 |
| 3.4 | 3 | Stakeholder sign-off | 1 hour | Team Lead | Go decision documented |
| 4.1 | 4 | Final sync (if needed) | 1 hour | DevOps | Latest content |
| 4.2 | 4 | Enable features | 30 min | DevOps | Branch protection, Dependabot |
| 4.3 | 4 | Create release | 30 min | DevOps | v0.3.0 tag exists |
| 4.4 | 4 | 24h monitoring | 24 hours | Team | No incidents |

**Total Duration:** 5 days (including 24h monitoring buffer)

### Post-Migration: Transition to ADR-OSS-002 Operational Mode

After CHECKPOINT 6 passes, the repository enters the sync workflow defined in ADR-OSS-002:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Post-Migration Operational Mode                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  MIGRATION COMPLETE (This ADR)                                          │
│  ═══════════════════════════════                                        │
│          │                                                              │
│          ▼                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                   ADR-OSS-002 Sync Process                        │   │
│  │                   (Release-Based Unidirectional)                  │   │
│  │                                                                   │   │
│  │  internal repo ──────────────────────────────────► jerry          │   │
│  │  (private)         Sync at each release          (public)         │   │
│  │                                                                   │   │
│  │  Trigger: Manual workflow dispatch at release milestones          │   │
│  │  Frequency: Per release (v0.3.1, v0.4.0, etc.)                   │   │
│  │  Direction: Internal → Public (never reverse)                     │   │
│  │  Safety: Gitleaks, build test, human approval                     │   │
│  │                                                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  First Sync After Migration: v0.3.1 or next change requiring release   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## L2: Strategic Implications (Architect)

### Trade-off Analysis

| Factor | Option A (Big Bang) | Option B (Staged) | Option C (Filter-Branch) | Option D (Fork) | Option E (Clean Start) |
|--------|---------------------|-------------------|-------------------------|-----------------|------------------------|
| Time to public | **1 day** | 5 days | 2-3 days | 1 day | 2-3 days |
| Secret exposure risk | Medium | **Low** | **HIGH** | **CRITICAL** | **None** |
| Rollback capability | Medium | **High** | Low | Medium | **High** |
| History preservation | None | None | Partial | Full | None |
| Validation time | None | **Comprehensive** | Limited | None | Limited |
| Complexity | Low | Medium | High | Low | **Low** |
| Constraint satisfaction | 4/6 | **6/6** | 2/6 | 2/6 | 5/6 |
| **Recommendation** | Consider | **SELECTED** | Reject | **REJECT** | Use for history |

### One-Way Door Assessment

| Decision | Reversibility | Assessment |
|----------|---------------|------------|
| Create public repo | **HIGH** | Can delete at any time |
| Initial content push | **HIGH** | Can force push or delete |
| Go public (visibility) | **MEDIUM** | Can make private, but content may be cached |
| Release tag v0.3.0 | **MEDIUM** | Can delete tag, but may be downloaded |
| Clean history approach | **LOW** | Cannot add history after public |
| Announcement/marketing | **LOW** | Cannot unsay; reputation impact |

**Conclusion:** Most decisions are **TWO-WAY DOORS**. The low-reversibility items (clean history, announcements) are appropriate trade-offs for security and simplicity.

### Failure Mode Analysis

| Failure Mode | Probability | Impact | Detection | RPN | Mitigation |
|--------------|-------------|--------|-----------|-----|------------|
| Secrets exposed in initial sync | LOW (2) | CRITICAL (10) | HIGH (2) | 40 | Gitleaks + manual review + clean history |
| Build fails on public repo | MEDIUM (4) | MEDIUM (5) | HIGH (2) | 40 | Build verification in Phase 2 |
| Documentation incomplete at cutover | MEDIUM (5) | MEDIUM (5) | HIGH (2) | 50 | VR audit in Phase 3 |
| Stakeholder blocks at sign-off | LOW (3) | HIGH (7) | HIGH (2) | 42 | Early stakeholder alignment |
| Post-cutover critical issue | LOW (2) | HIGH (8) | MEDIUM (5) | 80 | 24h monitoring + rollback plan |
| Sync workflow fails after cutover | MEDIUM (4) | MEDIUM (5) | HIGH (2) | 40 | Test sync in Phase 1 (dry-run) |
| External contribution before ready | LOW (2) | LOW (3) | HIGH (2) | 12 | Defer GitHub Discussions until stable |

**Highest RPN:** Post-cutover critical issue (80) - mitigated by 24h monitoring window and rollback capability.

### Design Rationale

#### Why Staged Over Big Bang?

Big Bang migration (Option A) provides speed but sacrifices safety:
- No validation time means issues are discovered post-cutover
- Rollback during migration is complex
- Pressure leads to mistakes

Staged migration provides validation checkpoints that:
1. Catch issues before they become public
2. Allow targeted rollback (only affected phase)
3. Build confidence at each step
4. Align with NASA SE best practices (verification at each phase)

#### Why Clean History Over Filtered History?

Filtered history approaches (Options C, D) have fundamental risks:
- Git filter-branch is deprecated and complex
- Fork exposes content before cleanup
- Even filtered history may contain secrets in commit messages or unchanged files

Clean start provides:
- Zero secret exposure risk
- Simple implementation
- Clear mental model
- Acceptable trade-off (most OSS projects don't have visible history from day 1)

#### Why 5 Days Over Faster Options?

The 5-day timeline provides:
- Day 1: Setup (no pressure)
- Day 2: Initial sync (time for thorough validation)
- Days 3-4: Stabilization (UAT, documentation, VR audit)
- Day 5: Cutover (confident execution)

Faster timelines compress validation, which increases post-cutover incident risk. The 5-day approach addresses RSK-P0-008 (schedule underestimation) directly.

### Industry Precedent

| Project | Migration Approach | Outcome |
|---------|-------------------|---------|
| **Chromium** | Staged migration from internal | Successful, large-scale example |
| **Android AOSP** | Periodic internal → public sync | Established pattern for dual-repo |
| **Kubernetes** | Born open source | No migration needed (different model) |
| **VS Code** | Single repo (public from start) | No dual-repo complexity |
| **Blender** | Clean slate open source release | Successful transition after commercial period |

**Pattern Observation:** Projects transitioning from internal to public commonly use clean-slate or staged approaches. Big bang migrations are rare for security-sensitive transitions.

### Risk Traceability

| Risk ID | Description | RPN | Treatment by This ADR |
|---------|-------------|-----|----------------------|
| RSK-P0-005 | Dual repository sync complexity | 192 | **Directly addressed** - Migration validates sync process |
| RSK-P0-008 | Schedule underestimation | 180 | **Directly addressed** - 5-day timeline with buffer |
| RSK-P0-002 | Credential exposure | 120 | **Addressed** - Clean history + Gitleaks |
| RSK-P0-006 | Documentation not OSS-ready | 150 | **Addressed** - Phase 3 documentation completion |

---

## Consequences

### Positive Consequences

1. **Eliminates migration uncertainty:** Clear phases with validation checkpoints
2. **Zero secret exposure risk:** Clean history approach prevents history-based leaks
3. **Provides rollback capability:** Each phase can be rolled back independently
4. **Validates sync workflow:** Migration tests the sync process before operational use
5. **Addresses schedule risk:** 5-day timeline with buffer prevents underestimation
6. **Creates audit trail:** 6 checkpoints document migration progress
7. **Enables ADR-OSS-002:** Sets up the target state for ongoing sync operations

### Negative Consequences

1. **Longer timeline:** 5 days vs 1 day for big bang
2. **No git history:** Public repo starts fresh (acceptable trade-off)
3. **Coordination required:** Multiple checkpoints need team availability
4. **Maintenance window:** Dual-repo state during Phase 3

### Neutral Consequences

1. **Documentation created:** CONTRIBUTORS.md, migration runbook
2. **Process established:** Repeatable for future similar migrations

### Residual Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Unknown secret in non-scanned file | LOW | HIGH | Expand pattern list; post-cutover rotation |
| Stakeholder delays sign-off | MEDIUM | MEDIUM | Early alignment; escalation path |
| Post-cutover issue after 7-day window | LOW | HIGH | Incident response process |

---

## Verification Requirements

This ADR links to the following Verification Requirements from the V&V Plan:

| VR ID | Requirement | Verification Method | Phase |
|-------|-------------|---------------------|-------|
| VR-001 | LICENSE file exists | Inspection | Phase 2 |
| VR-002 | LICENSE content valid | Inspection | Phase 2 |
| VR-006 | No credentials in git history | Test (Gitleaks) | Phase 2 |
| VR-015 | Critical documentation complete | Inspection | Phase 3 |
| VR-029 | README exists and is helpful | Inspection | Phase 3 |
| VAL-001 | Repository cloneable | Demonstration | Phase 3 |
| VAL-002 | Tests pass in clean environment | Test | Phase 2 |
| VAL-005 | New user can complete quick-start | User Testing | Phase 3 |

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-OSS-001 | DEPENDS_ON | CLAUDE.md must be decomposed before migration |
| ADR-OSS-002 | ENABLES | Migration prepares target state for sync workflow |
| ADR-OSS-003 | RELATED | Worktracker extraction included in pre-migration |
| ADR-OSS-004 | RELATED | Multi-persona docs ready before cutover |

---

## Implementation

### Action Items

| # | Action | Owner | Priority | Due |
|---|--------|-------|----------|-----|
| 1 | Complete ADR-OSS-001 (CLAUDE.md decomposition) | Architecture | P0 | Pre-Phase 1 |
| 2 | Complete ADR-OSS-003 (Worktracker extraction) | Architecture | P0 | Pre-Phase 1 |
| 3 | Execute Phase 1 (Prepare) | DevOps | P1 | Day 1 |
| 4 | Execute Phase 2 (Initial Sync) | DevOps | P1 | Day 2 |
| 5 | Execute Phase 3 (Stabilization) | QA + Docs | P1 | Days 3-4 |
| 6 | Execute Phase 4 (Cutover) | DevOps | P1 | Day 5 |
| 7 | Create CONTRIBUTORS.md | Docs | P2 | Phase 3 |
| 8 | Create Migration Runbook | DevOps | P2 | Phase 1 |

### Validation Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| All checkpoints pass | 6/6 | Checkpoint sign-off |
| Gitleaks findings | 0 | Scan report |
| Build passes | 100% | CI status |
| VR completion | >= 90% | VR audit |
| OSS readiness score | >= 0.85 | Scoring formula |
| 24h post-cutover incidents | 0 | Incident tracking |

---

## References

### Primary Sources

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | ADR-OSS-001 | Decision | CLAUDE.md decomposition prerequisite |
| 2 | ADR-OSS-002 | Decision | Sync process (post-migration operations) |
| 3 | DEC-002 | Decision | Dual repository strategy foundation |
| 4 | Requirements Specification | Requirements | VRs to satisfy before cutover |
| 5 | Phase 1 Risk Register | Risk | RSK-P0-005, RSK-P0-008 context |

### Industry References

| # | Reference | Relevance |
|---|-----------|-----------|
| 6 | [GitHub Repository Migration](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository) | Official GitHub guidance |
| 7 | [Gitleaks](https://github.com/gitleaks/gitleaks) | Secret scanning tool |
| 8 | [git-filter-repo](https://github.com/newren/git-filter-repo) | History filtering (considered, rejected) |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ADR-OSS-005 |
| **Status** | PROPOSED |
| **Workflow** | oss-release-20260131-001 |
| **Phase** | 2 (ADR Creation) |
| **Agent** | ps-architect-005 |
| **Risks Addressed** | RSK-P0-005 (RPN 192), RSK-P0-008 (RPN 180), RSK-P0-002 (RPN 120) |
| **Decision Type** | Two-Way Door (Mostly Reversible) |
| **Implementation Effort** | 5 days |
| **Word Count** | ~7,200 |
| **Constitutional Compliance** | P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence) |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-31 | ps-architect-005 | Initial ADR creation |

---

*This ADR was produced by ps-architect-005 for PROJ-001-oss-release Phase 2.*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence)*
*Template: Michael Nygard ADR Format with Jerry L0/L1/L2 extensions*
