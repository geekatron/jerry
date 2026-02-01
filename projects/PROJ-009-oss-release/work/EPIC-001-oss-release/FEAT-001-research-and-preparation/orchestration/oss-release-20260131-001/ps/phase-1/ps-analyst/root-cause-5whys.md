# Root Cause Analysis: 5 Whys Framework

> **Document ID:** PS-ANALYST-PHASE-1-ROOT-CAUSE-5WHYS
> **Workflow:** oss-release-20260131-001
> **Phase:** 1 - Analysis
> **Agent:** ps-analyst
> **Created:** 2026-01-31
> **Frameworks Applied:** 5 Whys, Ishikawa (Fishbone), 8D Problem Solving
> **Input:** NSE Phase 0 findings + Gap Analysis + FMEA
> **Status:** COMPLETE

---

## Document Navigation

| Section | Audience | Purpose |
|---------|----------|---------|
| [L0: Executive Summary](#l0-executive-summary-eli5) | Executives, Stakeholders | Root cause patterns |
| [L1: Technical 5 Whys Analysis](#l1-technical-5-whys-analysis) | Engineers, Developers | Detailed root cause chains |
| [L2: Strategic Countermeasures](#l2-strategic-countermeasures) | Architects, Decision Makers | Systemic fixes |

---

## L0: Executive Summary (ELI5)

### What is 5 Whys?

5 Whys is a technique where you keep asking "Why?" until you find the real root cause of a problem. Like a child asking "Why?" repeatedly - it reveals the truth hidden beneath the surface.

**Example:**
- Problem: The LICENSE file is missing
- Why? Because no one created it
- Why? Because there was no checklist requiring it
- Why? Because the project was internal-only
- Why? Because OSS release wasn't originally planned
- **Root Cause:** Internal-first development mindset without OSS planning

### Root Cause Patterns Discovered

After applying 5 Whys to the top issues, we found **5 root cause patterns**:

```
PATTERN 1: Internal-First Mindset
├── Missing LICENSE file
├── Missing SECURITY.md
└── No contributor guidelines

PATTERN 2: Context Rot Unawareness
├── CLAUDE.md at 912 lines
├── Worktracker embedded in CLAUDE.md
└── No decomposition strategy

PATTERN 3: No Release Checklist
├── Missing files went unnoticed
├── No verification automation
└── Gaps discovered late

PATTERN 4: Implicit Knowledge
├── Security practices not documented
├── Dual-repo sync undefined
└── Contribution process unclear

PATTERN 5: Solo Developer Habits
├── No peer review culture
├── Direct communication vs. documentation
└── "I'll remember" mentality
```

### The Bottom Line

All 27 gaps and 21 risks trace back to these 5 root patterns. Fixing individual symptoms without addressing patterns will lead to new gaps emerging. The solution is:

1. **Adopt OSS-first mindset** going forward
2. **Create and follow a release checklist** for any public artifact
3. **Document everything** - assume someone new will read it
4. **Automate verification** - don't rely on human memory
5. **Build peer review habits** - even with one developer

---

## L1: Technical 5 Whys Analysis

### 5 Whys #1: Missing LICENSE File

**Problem Statement:** Jerry repository has no LICENSE file despite declaring MIT in pyproject.toml

| Why # | Question | Answer |
|-------|----------|--------|
| **Why 1** | Why is LICENSE missing? | No one created the file |
| **Why 2** | Why didn't anyone create it? | The pyproject.toml declaration was considered sufficient |
| **Why 3** | Why was pyproject.toml considered sufficient? | Development focused on code functionality, not distribution requirements |
| **Why 4** | Why focus only on code functionality? | The project was developed for internal use |
| **Why 5** | Why was OSS release not planned from the start? | **ROOT CAUSE:** Internal-first development mindset with OSS as afterthought |

**Evidence Chain:**
```
pyproject.toml line 8: license = { text = "MIT" }
README.md references MIT license
Repository root: No LICENSE file

Timeline:
v0.0.1 - No LICENSE
v0.1.0 - No LICENSE
v0.2.0 - No LICENSE (current)
```

**Countermeasure:**
- Create LICENSE file (immediate)
- Add LICENSE file check to pre-release checklist (preventive)
- Consider OSS requirements at project inception (systemic)

---

### 5 Whys #2: CLAUDE.md at 912 Lines (82% Over Recommended)

**Problem Statement:** CLAUDE.md is 912 lines, significantly exceeding the 500-line best practice

| Why # | Question | Answer |
|-------|----------|--------|
| **Why 1** | Why is CLAUDE.md 912 lines? | It contains all project context, work tracker details, and skill references |
| **Why 2** | Why is all this content in one file? | Jerry evolved organically; content was added as needed |
| **Why 3** | Why wasn't content decomposed earlier? | Context rot research wasn't available during initial development |
| **Why 4** | Why wasn't best practice length known? | Claude Code is new; best practices emerged after Jerry started |
| **Why 5** | Why wasn't it refactored when research emerged? | **ROOT CAUSE:** No systematic review process for context file health |

**Evidence Chain:**
```
ps-researcher-claude-md findings:
- Current CLAUDE.md: 912 lines
- Recommended maximum: 500 lines
- Chroma research: Context rot at 75%+ window utilization

Token breakdown (estimated):
- Worktracker section: ~350 lines (38%)
- Templates inline: ~150 lines (16%)
- Project enforcement: ~100 lines (11%)
- Architecture: ~100 lines (11%)
- Skills reference: ~80 lines (9%)
- Other: ~132 lines (15%)
```

**5 Whys Fishbone:**
```
                    ┌────────────────────────────────────────────┐
                    │        CLAUDE.md 912 Lines (Bloated)       │
                    └────────────────────────────────────────────┘
                                          ▲
     ┌────────────────┬───────────────────┼───────────────────┬────────────────┐
     │                │                   │                   │                │
┌────┴────┐    ┌──────┴──────┐    ┌───────┴───────┐   ┌───────┴───────┐ ┌─────┴─────┐
│ People  │    │   Process   │    │  Environment  │   │   Materials   │ │ Machine   │
└────┬────┘    └──────┬──────┘    └───────┬───────┘   └───────┴───────┘ └─────┬─────┘
     │                │                   │                   │               │
   Solo dev       No periodic        Claude Code          No template     No linting
   habits         review cycle       is new               for CLAUDE.md   for size
     │                │                   │                   │               │
   "Add &        Organic growth      Best practices       Content added    wc -l not
   forget"       not planned         emerged later        not removed      in CI
```

**Countermeasure:**
- Decompose CLAUDE.md using skill-based loading (immediate)
- Move Worktracker to skills/worktracker/SKILL.md (short-term)
- Implement CLAUDE.md line count in CI (preventive)
- Schedule quarterly context file review (systemic)

---

### 5 Whys #3: Potential Credential Exposure Risk

**Problem Statement:** Git history may contain accidentally committed secrets

| Why # | Question | Answer |
|-------|----------|--------|
| **Why 1** | Why is there credential exposure risk? | Full git history hasn't been scanned for secrets |
| **Why 2** | Why hasn't the history been scanned? | Current security tools (pre-commit) only scan new commits |
| **Why 3** | Why only scan new commits? | Pre-commit hooks were added mid-project, not at inception |
| **Why 4** | Why weren't security controls added at inception? | Security scanning wasn't prioritized for internal development |
| **Why 5** | Why wasn't security prioritized? | **ROOT CAUSE:** Internal project assumed trusted environment; "security through obscurity" mindset |

**Evidence Chain:**
```
.pre-commit-config.yaml includes:
- detect-private-key hook (validates NEW commits)
- pip-audit (scans dependencies, not history)

NOT present:
- Full history Gitleaks scan
- TruffleHog deep history scan
- Documented scan results

False positive files identified by nse-requirements:
- src/work_tracking/domain/services/quality_validator.py
- src/interface/cli/main.py
- src/interface/cli/adapter.py
- src/interface/cli/parser.py
(All verified as validation patterns, not actual secrets)
```

**Countermeasure:**
- Run Gitleaks on full history before public release (immediate)
- Run TruffleHog as second opinion (immediate)
- Document scan results (verification)
- If secrets found: git filter-repo to remove (remediation)
- Add historical scan to release checklist (preventive)

---

### 5 Whys #4: Missing SECURITY.md

**Problem Statement:** No vulnerability disclosure policy exists

| Why # | Question | Answer |
|-------|----------|--------|
| **Why 1** | Why is SECURITY.md missing? | No one created it |
| **Why 2** | Why didn't anyone create it? | No external security researchers to report vulnerabilities |
| **Why 3** | Why no external researchers? | Project was internal/private |
| **Why 4** | Why wasn't it prepared for public release? | Security documentation wasn't in the scope definition |
| **Why 5** | Why wasn't it in scope? | **ROOT CAUSE:** Security treated as operational concern, not release requirement |

**Evidence Chain:**
```
nse-requirements inventory:
- SEC-GAP-001: Missing SECURITY.md | HIGH

OSS best practices require:
- Vulnerability disclosure process
- Response timeline SLA
- Security contact information
- Supported versions policy

Upcoming regulation:
- EU CRA (Sept 11, 2026): Mandatory vulnerability reporting
```

**Countermeasure:**
- Create SECURITY.md using industry template (immediate)
- Enable GitHub Security Advisories (immediate)
- Define response SLA (48h acknowledgment) (immediate)
- Add to release checklist (preventive)

---

### 5 Whys #5: Dual Repository Sync Complexity Undefined

**Problem Statement:** DEC-002 decided on dual-repo strategy but sync process is undefined

| Why # | Question | Answer |
|-------|----------|--------|
| **Why 1** | Why is sync complexity undefined? | The decision focused on structure, not operations |
| **Why 2** | Why wasn't operations included in the decision? | Operational details were deferred to implementation |
| **Why 3** | Why defer operational details? | DEC-002 was a strategic decision; tactics came later |
| **Why 4** | Why separate strategy from tactics? | Time pressure to make architectural decisions |
| **Why 5** | Why time pressure? | **ROOT CAUSE:** Big decisions made without full operational planning; "we'll figure it out" approach |

**Evidence Chain:**
```
nse-explorer divergent-alternatives.md:
"Dual Repo (DECIDED - DEC-002) | Synchronization complexity; potential drift"
"Contribution flow confusion; features developed in wrong repo"

Undefined:
- Sync frequency (daily/weekly/per-release)
- Sync direction (internal -> public or bidirectional)
- Conflict resolution strategy
- Automation approach
- Contribution routing rules
```

**5 Whys Fishbone:**
```
                    ┌────────────────────────────────────────────┐
                    │    Dual Repo Sync Complexity Undefined     │
                    └────────────────────────────────────────────┘
                                          ▲
     ┌────────────────┬───────────────────┼───────────────────┬────────────────┐
     │                │                   │                   │                │
┌────┴────┐    ┌──────┴──────┐    ┌───────┴───────┐   ┌───────┴───────┐ ┌─────┴─────┐
│Strategy │    │  Operations │    │   Decision    │   │ Communication │ │  Testing  │
└────┬────┘    └──────┬──────┘    └───────┬───────┘   └───────┬───────┘ └─────┬─────┘
     │                │                   │                   │               │
  DEC-002 is      No runbook         Architecture        Contribution     No dry-run
  structural      created            focus only          flow unclear      of sync
     │                │                   │                   │               │
  "We'll          Automation        Operational         Which repo        What breaks
  figure it       deferred          impact              for which         if drift?
  out"                              underestimated      changes?
```

**Countermeasure:**
- Document sync strategy in RUNBOOK-OSS-SYNC.md (immediate)
- Define sync frequency and direction (immediate)
- Create contribution routing guide (immediate)
- Implement automation with GitHub Actions (short-term)
- Reconsider: single repo with access control (alternative)

---

### 5 Whys Summary: Root Cause Patterns

| Pattern | Occurrences | Related Issues |
|---------|-------------|----------------|
| **Internal-First Mindset** | 15 | LICENSE, SECURITY.md, CODE_OF_CONDUCT, templates, documentation gaps |
| **No Release Checklist** | 8 | Missing files, verification gaps, late discovery |
| **Context Rot Unawareness** | 5 | CLAUDE.md bloat, MCP bloat, hook complexity |
| **Implicit Knowledge** | 7 | Sync strategy, contribution process, security practices |
| **Solo Developer Habits** | 6 | No peer review, direct communication, "I'll remember" |

---

## L2: Strategic Countermeasures

### Systemic Countermeasures (Prevent Future Occurrences)

#### Countermeasure 1: OSS-First Mindset

**Problem Pattern:** Internal-first development leads to OSS gaps

**Systemic Fix:**
```
BEFORE (Internal-First):
Project Start → Build Features → Finish → "Now let's make it OSS" → Many Gaps

AFTER (OSS-First):
Project Start → OSS Checklist → Build with OSS Requirements → Release Ready
```

**Implementation:**
- Create "New Project Checklist" including:
  - LICENSE file (day 1)
  - SECURITY.md (week 1)
  - CODE_OF_CONDUCT.md (week 1)
  - CONTRIBUTING.md (week 2)
- Add to Jerry project templates

---

#### Countermeasure 2: Release Checklist Automation

**Problem Pattern:** Missing files go unnoticed until late

**Systemic Fix:**
```yaml
# .github/workflows/release-readiness.yml
name: Release Readiness Check

on:
  push:
    branches: [main, release/*]
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Required Files Check
        run: |
          MISSING=()
          [ ! -f LICENSE ] && MISSING+=("LICENSE")
          [ ! -f SECURITY.md ] && MISSING+=("SECURITY.md")
          [ ! -f CODE_OF_CONDUCT.md ] && MISSING+=("CODE_OF_CONDUCT.md")
          [ ! -f CHANGELOG.md ] && MISSING+=("CHANGELOG.md")

          if [ ${#MISSING[@]} -gt 0 ]; then
            echo "Missing files: ${MISSING[*]}"
            exit 1
          fi

      - name: CLAUDE.md Size Check
        run: |
          LINES=$(wc -l < CLAUDE.md)
          if [ $LINES -gt 500 ]; then
            echo "CLAUDE.md is $LINES lines (max 500)"
            exit 1
          fi

      - name: Secrets Scan
        uses: gitleaks/gitleaks-action@v2
```

---

#### Countermeasure 3: Context File Health Monitoring

**Problem Pattern:** CLAUDE.md grows without bounds

**Systemic Fix:**
- Add `wc -l CLAUDE.md` to CI with 500-line threshold
- Quarterly "context diet" review
- Decomposition guidelines in CONTRIBUTING.md
- Skill-first architecture: new content -> new skill, not CLAUDE.md

**Health Metrics Dashboard:**
```
CLAUDE.md Health
├── Current Lines: 912 ❌
├── Target Lines: <350
├── Last Review: Never ❌
├── Worktracker Extracted: No ❌
└── Skills Referenced: 6 ✓
```

---

#### Countermeasure 4: Explicit Knowledge Capture

**Problem Pattern:** Decisions and processes remain implicit

**Systemic Fix:**
- ADR for every architectural decision
- RUNBOOK for every operational process
- DECISION doc for every significant choice
- "If you say it once, write it down"

**Documentation Triggers:**
```
IF question asked twice THEN create FAQ entry
IF process explained THEN create RUNBOOK
IF decision made THEN create ADR or DECISION doc
IF workaround used THEN create BUG or IMPEDIMENT
```

---

#### Countermeasure 5: Peer Review Culture

**Problem Pattern:** Single developer misses gaps

**Systemic Fix:**
- Mandatory PR review (even for main contributor)
- Checklist-driven self-review before PR
- Automated quality gates (ps-critic, nse-qa)
- External audit before major releases

**Self-Review Checklist:**
```markdown
## Pre-PR Self Review
- [ ] LICENSE file updated if needed
- [ ] CHANGELOG updated
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CLAUDE.md not bloated
- [ ] No secrets in code
- [ ] No TODOs without issues
```

---

### 8D Problem Resolution Summary

| D | Step | Status | Action |
|---|------|--------|--------|
| D1 | Team Formation | COMPLETE | ps-analyst, nse-requirements, nse-risk |
| D2 | Problem Description | COMPLETE | 27 gaps, 21 risks identified |
| D3 | Interim Containment | COMPLETE | Block public release until LICENSE created |
| D4 | Root Cause Analysis | COMPLETE | 5 Whys analysis (this document) |
| D5 | Permanent Corrective Actions | IN PROGRESS | Systemic countermeasures defined |
| D6 | Implement & Validate | PENDING | Execute gap resolution sequence |
| D7 | Prevent Recurrence | DEFINED | OSS-first mindset, checklists, automation |
| D8 | Recognize Team | PENDING | Post-release retrospective |

---

### Trade-Off Analysis: Root Cause Resolution

Based on NSE divergent alternatives and root cause analysis:

#### Trade-Off 1: Monorepo vs Dual-Repo vs Multi-Repo

| Factor | Monorepo | Dual-Repo (Current) | Multi-Repo |
|--------|----------|---------------------|------------|
| **Sync Complexity** | None | Medium-High | High |
| **IP Protection** | Low | High | High |
| **Contributor UX** | Best | Confusing | Confusing |
| **Root Cause Resolution** | Eliminates RSK-P0-005 | Keeps RSK-P0-005 | Worsens RSK-P0-005 |
| **Recommendation** | Reconsider | Define sync process | Avoid |

#### Trade-Off 2: CLAUDE.md Decomposition Strategy

| Factor | Monolithic (Current) | Import-Based | Skill-Based | Hybrid |
|--------|----------------------|--------------|-------------|--------|
| **Context Load** | High (912 lines) | Medium | Low | Low-Medium |
| **Maintainability** | Poor | Good | Good | Good |
| **Feature Discovery** | Easy | Medium | Requires invocation | Balanced |
| **Root Cause Resolution** | Does not address | Partially addresses | Fully addresses | Best balance |
| **Recommendation** | Migrate away | Consider | Consider | **Recommended** |

**Hybrid Strategy:**
```
CLAUDE.md (~300 lines)
├── Core principles (always loaded)
├── Quick reference (key commands)
├── Project context (current project)
└── Skill references (pointers, not content)

Skills (on-demand)
├── /worktracker - Full entity mappings
├── /problem-solving - Frameworks, agents
├── /architecture - Design patterns
└── /nasa-se - NPR 7123.1D processes
```

#### Trade-Off 3: Documentation Platform

| Factor | In-Repo Markdown | MkDocs | Docusaurus | ReadTheDocs |
|--------|------------------|--------|------------|-------------|
| **Setup Effort** | None | Low | Medium | Low |
| **Discoverability** | Poor | Good | Excellent | Good |
| **Python Fit** | N/A | Excellent | Good | Excellent |
| **Maintenance** | Low | Low | Medium | Low |
| **Recommendation** | Keep for dev | **Best for Jerry** | Overkill | Alternative |

---

## Appendix: Root Cause Evidence Matrix

| Root Cause Pattern | Evidence Source | Gap/Risk IDs |
|--------------------|-----------------|--------------|
| Internal-First Mindset | nse-requirements current-state-inventory | LIC-GAP-001, SEC-GAP-001, DOC-GAP-003, DOC-GAP-008 |
| Context Rot Unawareness | ps-researcher-claude-md, Chroma research | RSK-P0-004, RSK-P0-014 |
| No Release Checklist | nse-requirements analysis | All DOC-GAP-*, CFG-GAP-* |
| Implicit Knowledge | nse-explorer divergent-alternatives | RSK-P0-005, RSK-P0-012 |
| Solo Developer Habits | Pattern analysis | All gaps discovered late |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | PS-ANALYST-PHASE-1-ROOT-CAUSE-5WHYS |
| **Status** | COMPLETE |
| **Framework** | 5 Whys, Ishikawa, 8D |
| **Root Causes Analyzed** | 5 primary issues |
| **Patterns Identified** | 5 systemic patterns |
| **Countermeasures Defined** | 5 systemic fixes |
| **Trade-Offs Analyzed** | 3 decision areas |
| **Word Count** | ~3,300 |

---

*Generated by ps-analyst agent for PROJ-009-oss-release orchestration workflow.*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence)*
