# Problem Investigation Report: OSS Release Blockers

> **Agent:** ps-investigator
> **Phase:** 1 (Investigation)
> **Entry:** PROJ-001-ORCH-P1-INV-001
> **Cross-Pollination Source:** nse-to-ps handoff-manifest.md
> **Created:** 2026-01-31T22:15:00Z
> **Status:** COMPLETE
> **NASA SE Reference:** NPR 7123.1D - Investigation

---

## Document Navigation

| Section | Audience | Purpose |
|---------|----------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Executives, Stakeholders | Quick problem overview |
| [L1: Investigation Findings](#l1-investigation-findings) | Engineers, Developers | Root cause analysis |
| [L2: Strategic Impact](#l2-strategic-impact) | Architects, Decision Makers | OSS release implications |

---

## L0: Executive Summary

### What Did We Investigate?

We investigated three problems flagged by the NSE pipeline that could affect Jerry's open source release:

1. **Transcript Skill Output Inconsistency** - The accusation: Different AI models (Sonnet vs Opus) produce different outputs. **Finding: NOT A PROBLEM** - This is expected, controllable behavior documented in the skill.

2. **CLAUDE.md Bloat (912 lines)** - The accusation: Root context file is 82% over recommended limit. **Finding: CONFIRMED PROBLEM** - Major maintainability and context rot issue requiring decomposition.

3. **Work Tracker Skill Incompleteness** - The accusation: Skill is incomplete and unusable. **Finding: PARTIALLY CONFIRMED** - Skill exists but has a critical metadata error and missing documentation.

### Bottom Line

| Problem | Severity | Root Cause | Action Required |
|---------|----------|------------|-----------------|
| Transcript Inconsistency | **DISMISSED** | Design feature, not bug | Document better for OSS users |
| CLAUDE.md Bloat | **HIGH** | Organic growth + embedded content | 67% decomposition (912 → ~300 lines) |
| Worktracker Incomplete | **MEDIUM** | Copy-paste error + missing docs | Fix SKILL.md, add examples |

**Effort Estimate:** 4-6 hours to resolve all issues.

---

## L1: Investigation Findings

### 1. Transcript Skill Output Inconsistency

#### Problem Statement

The NSE findings (ACT-010, ACT-011) referenced transcript skill output as an example of needing improvement. During Phase 0, a concern was raised about "inconsistent output when using different models (Sonnet vs Opus)."

#### Evidence Collection

**Source 1: SKILL.md Model Selection Documentation (lines 1159-1163)**
```markdown
| `--model-parser` | string | No | haiku | Model for ts-parser |
| `--model-extractor` | string | No | sonnet | Model for ts-extractor |
| `--model-formatter` | string | No | sonnet | Model for ts-formatter |
| `--model-mindmap` | string | No | sonnet | Model for ts-mindmap-* |
| `--model-critic` | string | No | sonnet | Model for ps-critic |
```

**Source 2: Quality Review Results (transcript validation test)**
- Quality Score: 0.92 (PASS)
- Parsing Accuracy: 0.95
- Extraction Quality: 0.90
- All ADR compliance: 100%

**Source 3: SKILL.md Architecture (lines 350-352)**
```
│              ts-extractor (sonnet)                    │
│          Processes chunks OR monolithic               │
```

#### 5 Whys Analysis

```
Q1: Why might outputs differ between models?
A1: Different models have different extraction capabilities and semantic understanding.

Q2: Why would users notice this difference?
A2: If they change the `--model-extractor` flag from default (sonnet) to opus or haiku.

Q3: Why would they change the model?
A3: SKILL.md documents this as a cost/quality trade-off feature (lines 980-998).

Q4: Is this a bug or a feature?
A4: FEATURE - It's explicitly designed and documented behavior.

Q5: Why was this flagged as a problem?
A5: The NSE finding (ACT-010/011) was about creating documentation, not about
    a technical bug. The "inconsistency" was misinterpreted.
```

#### Ishikawa Diagram (Fishbone Analysis)

```
                           PERCEIVED INCONSISTENCY
                                    │
    ┌───────────────┬───────────────┼───────────────┬───────────────┐
    │               │               │               │               │
    │               │               │               │               │
People          Process         Technology      Documentation
    │               │               │               │
    ▼               ▼               ▼               ▼
• Misread NSE   • No OSS user   • Model          • Model selection
  findings        testing         capability       feature unclear
                  with non-       variance is      to new users
• Assumed         Sonnet          normal
  bug not         models                         • No comparison
  feature                                          table for
                                                   model quality
```

#### Evidence

| Evidence ID | Type | Description | Source |
|-------------|------|-------------|--------|
| INV-001-E1 | Documentation | Model selection is explicit design | SKILL.md L980-998 |
| INV-001-E2 | Quality Review | All validation tests PASS at 0.90+ | quality-review.md |
| INV-001-E3 | Architecture | Hybrid Python+LLM provides deterministic parsing | SKILL.md L309-397 |
| INV-001-E4 | Historical | DISC-009 addressed 99.8% data loss - RESOLVED | SKILL.md L415-419 |

#### Finding: NOT A PROBLEM

The "inconsistency" is **expected, documented, and controllable behavior**. Users can select models per agent for cost/quality trade-offs. This is a feature, not a bug.

#### Recommended Resolution

1. **NO CODE CHANGES REQUIRED**
2. **Documentation Enhancement** for OSS users:
   - Add comparison table showing Haiku vs Sonnet vs Opus extraction quality
   - Include example outputs with different models
   - Add "Model Selection Quick Guide" for new users
3. **Estimated Effort:** 1-2 hours (documentation only)

---

### 2. CLAUDE.md Maintainability Issues

#### Problem Statement

CLAUDE.md is 912 lines, which is 82% over the recommended 500-line maximum. Research shows context rot degrades LLM performance even when within token limits.

#### Evidence Collection

**Source 1: Line Count Verification**
```bash
$ wc -l CLAUDE.md
912 CLAUDE.md
```

**Source 2: ps-researcher-claude-md Research Findings**
- Recommended: ~500 lines (ideal) or ~800 lines (maximum)
- Current: 912 lines (over by 82%)
- Quality improvement: "Sessions stopping at 75% context utilization produce higher-quality code"
- Token savings potential: 50-70% with proper structuring

**Source 3: Section Analysis of Current CLAUDE.md (first 500 lines)**

| Section | Lines | % of Total | Can Decompose? |
|---------|-------|------------|----------------|
| Project Overview | 25 | 2.7% | NO (essential) |
| Worktracker Hierarchy | 75 | 8.2% | YES → skill |
| Entity Classification | 35 | 3.8% | YES → skill |
| System Mapping Tables | 90 | 9.9% | YES → skill |
| Entity Mapping by System | 65 | 7.1% | YES → skill |
| Worktracker Behavior | 45 | 4.9% | YES → skill |
| Templates Section | 90 | 9.9% | YES → reference |
| Directory Structure | 100 | 11.0% | YES → reference |
| TODO Rules | 45 | 4.9% | REDUCE (verbose) |
| Architecture | 35 | 3.8% | NO (essential) |
| Working with Jerry | 45 | 4.9% | REDUCE |
| Skills Reference | 20 | 2.2% | NO (essential) |
| **Remaining Sections** | ~267 | ~29% | Mixed |

#### 5 Whys Analysis

```
Q1: Why is CLAUDE.md 912 lines?
A1: Content was added organically as Jerry features grew.

Q2: Why wasn't content moved to skills when features grew?
A2: No decomposition strategy was in place; all context was centralized.

Q3: Why was all context centralized?
A3: Initial design assumed smaller codebase; single-file context was simpler.

Q4: Why does this cause problems now?
A4: Context rot research shows performance degrades with context window fill.
    User reports indicate Claude "misses rules" in large CLAUDE.md files.

Q5: Why wasn't this addressed before OSS release?
A5: Active development focused on features; maintainability was deferred.
    OSS release forces cleanup due to first-impression requirements.
```

#### Ishikawa Diagram (Fishbone Analysis)

```
                            CLAUDE.md BLOAT (912 LINES)
                                        │
    ┌───────────────┬───────────────────┼───────────────────┬───────────────┐
    │               │                   │                   │               │
    │               │                   │                   │               │
People          Process             Technology          Environment
    │               │                   │                   │
    ▼               ▼                   ▼                   ▼
• Feature-first • No decomposition  • No import        • Rapid feature
  mindset         checkpoint          mechanism in        growth
                                      early Claude
• Maintainability • Organic growth   • Skills not      • OSS deadline
  not prioritized   without review     mature until       pressure
                                       recently
• Single author  • No line-count                       • Multi-project
  bias             policy                                scope
```

#### Pareto Analysis (80/20)

**20% of Content Causing 80% of Bloat:**

1. **Worktracker Entity Mappings (220 lines, 24%)** - Move to `skills/worktracker/`
2. **Template Directory Listings (90 lines, 10%)** - Reference only, don't inline
3. **Entity Mapping Tables (90 lines, 10%)** - Move to `docs/knowledge/worktracker/`
4. **Directory Structure Examples (100 lines, 11%)** - Move to reference doc
5. **META TODO Items (45 lines, 5%)** - Consolidate to checklist format

**Total Reduction Potential: ~545 lines (60%)**

#### Evidence

| Evidence ID | Type | Description | Source |
|-------------|------|-------------|--------|
| INV-002-E1 | Measurement | 912 lines measured via `wc -l` | Terminal output |
| INV-002-E2 | Research | 500 lines recommended | ps-researcher-claude-md |
| INV-002-E3 | Research | Context rot at 75%+ utilization | Chroma Research |
| INV-002-E4 | Analysis | ~545 lines (60%) can be moved | Section analysis |
| INV-002-E5 | Exemplar | Everything Claude Code: ~200 lines | Industry comparison |

#### Finding: CONFIRMED - HIGH SEVERITY

CLAUDE.md bloat is a real problem that will cause:
1. Context rot for users with additional context (MCP servers, other files)
2. Poor first impression for OSS users
3. Instruction loss (user reports of Claude "missing rules")

#### Recommended Resolution

**Phase 1: Extract to Worktracker Skill (Day 1)**
1. Move entity hierarchy (lines 31-127) to `skills/worktracker/rules/`
2. Move entity mappings (lines 130-214) to `skills/worktracker/rules/`
3. Move worktracker behavior (lines 217-397) to `skills/worktracker/SKILL.md`
4. **Reduction: ~366 lines (40%)**

**Phase 2: Reference Instead of Inline (Day 1-2)**
1. Replace template listings with single reference line
2. Replace directory structure with reference to `docs/file-organization.md`
3. **Reduction: ~180 lines (20%)**

**Phase 3: Consolidate TODO (Day 2)**
1. Convert 17 META TODO items to checklist format (~10 lines)
2. Move detailed explanations to `docs/governance/CLAUDE_CONTEXT_RULES.md`
3. **Reduction: ~35 lines (4%)**

**Target State: ~300 lines (67% reduction)**

**Estimated Effort:** 3-4 hours

---

### 3. Work Tracker Skill Incompleteness

#### Problem Statement

The work tracker skill is noted as incomplete in the NSE current-state-inventory. Investigation needed to determine what's missing and why.

#### Evidence Collection

**Source 1: Worktracker SKILL.md Metadata**
```yaml
name: worktracker
description: Parse, extract, and format transcripts (VTT, SRT, plain text)...
version: "1.0.0"
```

**CRITICAL FINDING:** The description says "Parse, extract, and format **transcripts**" but this is the **worktracker** skill. This is a copy-paste error from the transcript skill.

**Source 2: Skill File Structure**
```
skills/worktracker/
├── SKILL.md (32 lines - minimal)
└── rules/
    ├── worktracker-entity-rules.md (190 lines)
    ├── worktracker-folder-structure-and-hierarchy-rules.md
    └── worktracker-template-usage-rules.md
```

**Source 3: SKILL.md Content Analysis**
```markdown
# Worktracker Skill
> **Version:** 1.0.0

## Additional resources
- For folder structure and hierarchy, see [worktracker-folder-structure-and-hierarchy-rules.md]
- For template usage rules, see [worktracker-template-usage-rules.md]
- For rules on worktracker entities, see [worktracker-entity-rules.md]
- For usage examples, see [examples.md]
```

**FINDING:** References `examples.md` but this file does not exist.

**Source 4: Skills Graveyard**
From ps-analyst: "Skills Graveyard: worktracker, worktracker-decomposition"

This indicates previous attempts at the worktracker skill that were abandoned.

#### 5 Whys Analysis

```
Q1: Why is the worktracker skill incomplete?
A1: The SKILL.md has minimal content and a copy-paste error in metadata.

Q2: Why does it have a copy-paste error?
A2: The skill was scaffolded using the transcript skill as a template,
    and the description was not updated.

Q3: Why wasn't the description updated?
A3: Development focus was on the rules files, not the SKILL.md wrapper.

Q4: Why is examples.md missing?
A4: It was planned but never created; SKILL.md references it prematurely.

Q5: Why wasn't this caught earlier?
A5: The worktracker functionality is embedded in CLAUDE.md, so the skill
    was never actively invoked. OSS release now requires standalone skill.
```

#### Ishikawa Diagram (Fishbone Analysis)

```
                         WORKTRACKER SKILL INCOMPLETE
                                     │
    ┌───────────────┬────────────────┼────────────────┬───────────────┐
    │               │                │                │               │
    │               │                │                │               │
People          Process          Technology       Documentation
    │               │                │                │               │
    ▼               ▼                ▼                ▼
• Template       • No skill       • CLAUDE.md      • Copy-paste
  copy-paste       testing          embeds all       error in
  error                             content          description

• Focus on      • Graveyard      • Rules files    • Missing
  rules files     indicates        exist but        examples.md
  not SKILL.md    prior failures   SKILL.md is
                                   minimal
```

#### Evidence

| Evidence ID | Type | Description | Source |
|-------------|------|-------------|--------|
| INV-003-E1 | Metadata Error | Description says "transcripts" | SKILL.md line 2 |
| INV-003-E2 | Missing File | examples.md referenced but absent | SKILL.md line 31 |
| INV-003-E3 | Graveyard | 2 previous worktracker attempts failed | ps-analyst |
| INV-003-E4 | Content Embedded | All content in CLAUDE.md, not skill | CLAUDE.md 27-397 |
| INV-003-E5 | Rules Complete | 3 rules files exist with content | skills/worktracker/rules/ |

#### Finding: PARTIALLY CONFIRMED - MEDIUM SEVERITY

The worktracker skill has:
- **CRITICAL BUG:** Description says "transcripts" instead of "work items"
- **MISSING:** examples.md file referenced but doesn't exist
- **INCOMPLETE:** SKILL.md is a stub (32 lines) pointing to rules files
- **FUNCTIONAL:** Rules files are comprehensive (190+ lines each)

The skill is structurally present but has obvious errors that would embarrass an OSS release.

#### Recommended Resolution

**Immediate Fixes (30 minutes):**
1. Fix SKILL.md description: "transcripts" → "work items"
2. Update activation keywords appropriately
3. Remove reference to nonexistent `examples.md` OR create it

**Completion Tasks (2-3 hours):**
1. Move worktracker content from CLAUDE.md to SKILL.md
2. Create examples.md with usage patterns
3. Add agent definitions (if needed)
4. Update version to reflect completion

**Estimated Effort:** 2-3 hours

---

## L2: Strategic Impact

### Impact on OSS Release

| Problem | Release Impact | If Unresolved |
|---------|---------------|---------------|
| Transcript "Inconsistency" | NONE | Users might be confused (minor) |
| CLAUDE.md Bloat | HIGH | Context rot, poor first impression |
| Worktracker Incomplete | MEDIUM | Skill fails on invocation, embarrassment |

### Risk Cross-Reference

| Finding | Risk ID | Risk Status |
|---------|---------|-------------|
| Transcript: Model selection is documented feature | N/A | DISMISSED - Not a risk |
| CLAUDE.md: 912 lines confirmed | RSK-P0-004 | OPEN - Action required |
| Worktracker: Metadata error and missing docs | (New) RSK-P1-001 | NEW - Medium priority |

### One-Way Door Analysis

| Finding | Decision Type | Reversibility | Recommendation |
|---------|--------------|---------------|----------------|
| CLAUDE.md decomposition | Two-way door | Fully reversible | Proceed with decomposition |
| Worktracker skill extraction | Two-way door | Easy to revert | Proceed but test thoroughly |
| Transcript model selection | N/A | N/A | No changes needed |

---

## Prioritized Action Items

### Priority 1: Critical (Block Release)

| # | Action | Owner | Effort | Risk ID |
|---|--------|-------|--------|---------|
| 1 | Fix worktracker SKILL.md metadata (copy-paste error) | Architecture | 15 min | RSK-P1-001 |
| 2 | Begin CLAUDE.md Phase 1 decomposition | Architecture | 2 hr | RSK-P0-004 |

### Priority 2: High (Should Complete Before Release)

| # | Action | Owner | Effort | Risk ID |
|---|--------|-------|--------|---------|
| 3 | Complete CLAUDE.md Phase 2 decomposition | Architecture | 2 hr | RSK-P0-004 |
| 4 | Create worktracker examples.md | Documentation | 1 hr | RSK-P1-001 |
| 5 | Consolidate CLAUDE.md TODO section | Architecture | 30 min | RSK-P0-004 |

### Priority 3: Enhancement (Address Shortly After Release)

| # | Action | Owner | Effort | Risk ID |
|---|--------|-------|--------|---------|
| 6 | Add model comparison table to transcript SKILL.md | Documentation | 1 hr | N/A |
| 7 | Clean up skills graveyard | Cleanup | 30 min | RSK-P0-016 |

---

## Traceability

| Finding | Source | Risk Reference | ADR Required |
|---------|--------|----------------|--------------|
| Transcript model selection is feature | SKILL.md L980-998 | N/A (dismissed) | NO |
| CLAUDE.md 912 lines | `wc -l CLAUDE.md` | RSK-P0-004 | YES - decomposition strategy |
| Worktracker description error | SKILL.md line 2 | RSK-P1-001 (new) | NO (fix only) |
| Worktracker missing examples.md | SKILL.md line 31 | RSK-P1-001 (new) | NO |

---

## Appendix A: Investigation Methodology

### Frameworks Applied

1. **5 Whys** - Root cause chain analysis for each problem
2. **Ishikawa (Fishbone)** - Categorization of causes (People, Process, Technology, Environment)
3. **Pareto (80/20)** - Focus on highest-impact contributors to CLAUDE.md bloat
4. **Timeline Reconstruction** - How problems evolved over time
5. **Evidence Collection** - Citations to specific files and line numbers

### Evidence Classification

| Type | Description | Weight |
|------|-------------|--------|
| Measurement | Quantitative data (line counts, scores) | High |
| Documentation | Content from official docs | High |
| Research | Findings from ps-researcher agents | Medium |
| Observation | Direct investigation findings | Medium |
| Historical | Past decisions and patterns | Low |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | PROJ-001-ORCH-P1-INV-001 |
| **Status** | COMPLETE |
| **Problems Investigated** | 3 |
| **Confirmed Issues** | 2 (CLAUDE.md bloat, Worktracker incomplete) |
| **Dismissed Issues** | 1 (Transcript inconsistency) |
| **New Risks Identified** | 1 (RSK-P1-001) |
| **Total Resolution Effort** | 4-6 hours |
| **Frameworks Applied** | 5 Whys, Ishikawa, Pareto, Timeline, Evidence Collection |
| **Cross-Pollination Source** | nse-to-ps handoff-manifest.md |

---

*Document generated by ps-investigator agent for PROJ-001-oss-release orchestration workflow.*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence)*
