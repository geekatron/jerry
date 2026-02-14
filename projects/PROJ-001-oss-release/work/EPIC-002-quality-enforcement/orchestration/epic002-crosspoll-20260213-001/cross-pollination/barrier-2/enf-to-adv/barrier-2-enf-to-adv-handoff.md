# Barrier 2 Cross-Pollination Handoff: ENF to ADV

<!--
DOCUMENT-ID: EPIC002-CROSSPOLL-B2-ENF-TO-ADV
TYPE: Cross-Pollination Handoff Artifact
VERSION: 1.0.0
SOURCE: ENF Pipeline Phase 2 (EN-403: Hook-Based Enforcement, EN-404: Rule-Based Enforcement)
TARGET: ADV Pipeline Phase 3 (EN-304, EN-305, EN-307)
BARRIER: 2
DIRECTION: ENF -> ADV
DATE: 2026-02-13
PROJECT: PROJ-001-oss-release
EPIC: EPIC-002 (Quality Framework Enforcement)
-->

> **From:** ENF Pipeline (FEAT-005: Enforcement Mechanisms), Phase 2 complete
> **To:** ADV Pipeline (FEAT-004: Adversarial Strategy Research), Phase 3 (EN-304, EN-305, EN-307)
> **Barrier:** 2
> **Date:** 2026-02-13
> **Confidence:** HIGH -- all data traceable to EN-403 TASK-001 through TASK-004 and EN-404 TASK-001 through TASK-004; iteration 2 quality score 0.93 PASS

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | What ENF Phase 2 produced and what ADV Phase 3 needs |
| [Hook-Based Enforcement Architecture (EN-403)](#hook-based-enforcement-architecture-en-403) | Three hook designs with API contracts and capabilities |
| [Rule-Based Enforcement Architecture (EN-404)](#rule-based-enforcement-architecture-en-404) | Tiered enforcement, token optimization, HARD rule inventory |
| [5-Layer Architecture Update](#5-layer-architecture-update) | Phase 2 refinements to the hybrid layered approach |
| [Platform Constraints](#platform-constraints) | Updated portability and token budget constraints |
| [Implementation Capabilities](#implementation-capabilities) | What enforcement CAN and CANNOT do after Phase 2 |
| [Adversarial Strategy Integration Points](#adversarial-strategy-integration-points) | Concrete touchpoints for ADV Phase 3 enablers |
| [Risk Summary](#risk-summary) | Updated FMEA and residual risks |
| [ADR Reference](#adr-reference) | ADR-EPIC002-002 ratification status |
| [Source Traceability](#source-traceability) | Full citation chain to all 8 source artifacts |

---

## Executive Summary

### What ENF Phase 2 Produced

EN-403 (Hook-Based Enforcement) and EN-404 (Rule-Based Enforcement) completed all 8 artifacts (4 each) through a creator-critic-revision cycle achieving a final adversarial review quality score of **0.93 PASS** (threshold 0.92, delta +0.12 from iteration 1 score of 0.81). The analysis produced:

1. **88 formal requirements** -- 44 from EN-403 (REQ-403-010 through REQ-403-096) covering hook-based enforcement, and 44 from EN-404 (REQ-404-001 through REQ-404-064) covering rule-based enforcement. Combined: 75 HARD, 13 MEDIUM.

2. **Three hook enforcement designs** -- UserPromptSubmit (L2: per-prompt reinforcement, 600 tokens), PreToolUse (L3: pre-action gating, zero tokens, AST validation), SessionStart (L1: quality context injection, ~360 tokens). All hooks fail-open, stdlib-only, hexagonal architecture compliant.

3. **A tiered enforcement system** -- 24 HARD rules (H-01 through H-24, within the 25 maximum), exclusive tier vocabulary (HARD: MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL; MEDIUM: SHOULD/RECOMMENDED/PREFERRED/EXPECTED; SOFT: MAY/CONSIDER/OPTIONAL/SUGGESTED), and a `quality-enforcement.md` SSOT file for shared enforcement constants.

4. **Token budget optimization** -- Current L1 baseline of ~30,160 tokens reduced to ~11,176 allocated tokens (target 12,476, leaving 1,300 buffer). Achieved through file consolidation (10 files to 8), code example reduction (~60% of current tokens), and enforcement tier restructuring.

5. **L2 re-injection content design** -- ~510 tokens of priority-ranked content for V-024 context reinforcement, with L2-REINJECT tag format for automated extraction from rule files: `<!-- L2-REINJECT: rank=N, tokens=NN, content="..." -->`.

6. **HARD language pattern analysis** -- 6 effective enforcement patterns identified (~90-95% compliance) and 6 anti-patterns quantified (~40-75% bypass rates), providing empirical foundation for rule rewriting.

### What ADV Phase 3 Needs

ADV Phase 3 has three enablers that consume this handoff:

**EN-304 (Strategy-Skill Integration)** must integrate adversarial strategies into Jerry's skill system. This handoff provides:
- Hook trigger points where adversarial strategies can be invoked (UserPromptSubmit C1-C4 criticality, PreToolUse governance escalation, SessionStart strategy listing)
- L2 re-injection content format and the L2-REINJECT tag extraction algorithm
- SSOT file locations and the shared data model (quality-enforcement.md)
- Token budget constraints (600 per prompt, ~360 session start, 12,476 L1 total)

**EN-305 (Adversarial Skill Implementation)** must build the adversarial skill. This handoff provides:
- Enforcement layer capabilities (what each layer CAN and CANNOT enforce, with specific mechanisms)
- Hook API contracts (PromptReinforcementEngine, PreToolEnforcementEngine, SessionQualityContextGenerator class interfaces)
- Rule file structure (tiered enforcement, HARD rule inventory H-01 through H-24)
- ContentBlock system for L2 injection (7 blocks with priority rankings and token estimates)

**EN-307 (Cross-Strategy Validation)** must validate strategies work together. This handoff provides:
- Platform constraints (Claude Code hook exclusivity, Windows WSL requirement)
- Combined token budgets across layers and their interaction effects
- Shared data model (quality-enforcement.md as SSOT for C1-C4, 0.92 threshold, strategy encodings, cycle count, tier vocabulary)
- Defense-in-depth compensation chain showing how layers interact under failure

---

## Hook-Based Enforcement Architecture (EN-403)

### UserPromptSubmit Hook (L2: Per-Prompt Reinforcement)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Re-inject critical enforcement rules on every user prompt to counteract context rot |
| **Hook Entry Point** | `hooks/user-prompt-submit.py` |
| **Engine Class** | `PromptReinforcementEngine` |
| **Engine Location** | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` |
| **Token Budget** | 600 tokens per prompt submission (REQ-403-015, clarified v1.1.0) |
| **Output Format** | XML: `<enforcement-context criticality="C{N}">` wrapping selected content blocks |
| **Criticality Assessment** | C1-C4 keyword matching against user prompt content |
| **Fail Mode** | Fail-open (REQ-403-070) |
| **Dependencies** | stdlib-only (REQ-403-075) |

#### ContentBlock System

The engine uses a priority-ranked ContentBlock system. Blocks are selected based on criticality assessment and trimmed to the 600-token budget:

| Block ID | Content | Priority | Tokens |
|----------|---------|----------|--------|
| `quality-gate` | 0.92 threshold, scoring requirement | 1 | ~30 |
| `constitutional-principles` | P-003, P-020, P-022 constraints | 2 | ~65 |
| `self-review` | Self-review before submission | 3 | ~30 |
| `scoring-requirement` | S-014 LLM-as-Judge scoring | 4 | ~35 |
| `steelman` | S-003 Steelman requirement | 5 | ~30 |
| `leniency-calibration` | Anti-leniency bias instruction | 6 | ~25 |
| `deep-review` | Deep adversarial review trigger | 7 | ~40 |

**Total if all selected:** ~255 tokens (well within 600 budget, leaving room for L2-REINJECT content).

#### L2-REINJECT Tag Integration

The PromptReinforcementEngine is designed to extract V-024 content from L2-REINJECT tags in `.context/rules/` files as the primary content source, with the hardcoded ContentBlocks serving as fallback only. The tag extraction algorithm:

1. Scan `.context/rules/*.md` files for `<!-- L2-REINJECT: rank=N, tokens=NN, content="..." -->` tags
2. Parse `rank` and `tokens` attributes from each tag
3. Sort by rank ascending (rank 1 = highest priority)
4. Concatenate content values until 600-token budget is reached
5. Fall back to hardcoded ContentBlocks if no tags found or extraction fails

**ADV implication:** EN-304 and EN-305 can define adversarial strategy reinforcement content by placing L2-REINJECT tags in the appropriate rule files, with rank values determining injection priority.

#### Criticality Assessment (C1-C4)

| Level | Trigger | Strategy Activation |
|-------|---------|-------------------|
| C1 | Default (no special keywords) | S-010 Self-Refine only |
| C2 | "design", "architecture", "decision" | S-010 + S-003 Steelman + S-007 Constitutional + S-002 Devil's Advocate + S-014 LLM-as-Judge |
| C3 | "delete", "remove", "governance" | All C2 + S-004 + S-012 + S-013 Inversion |
| C4 | ".claude/rules/", "CONSTITUTION", "CLAUDE.md" | All 10 strategies |

#### Accepted Risks

| Risk ID | Description | RPN | Mitigation |
|---------|-------------|-----|------------|
| RISK-L2-001 | V-024 effectiveness degrades under context rot (inherent LLM limitation) | 336 (FM-403-07) | Defense-in-depth: L3 deterministically blocks regardless of LLM state |
| RISK-L2-002 | Keyword-based criticality assessment is gameable | 252 (FM-403-02) | L3 gating catches violations regardless of criticality classification |

---

### PreToolUse Hook (L3: Pre-Action Gating)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Deterministically block non-compliant write/edit operations before they execute |
| **Hook Entry Point** | `scripts/pre_tool_use.py` (modified with Phase 3 + Phase 4) |
| **Engine Class** | `PreToolEnforcementEngine` |
| **Engine Location** | `src/infrastructure/internal/enforcement/pretool_enforcement.py` |
| **Token Cost** | Zero (external process, does not consume context tokens) |
| **Context Rot Immunity** | IMMUNE -- runs as external Python process, not affected by LLM context state |
| **Fail Mode** | Fail-open (REQ-403-070) |
| **Dependencies** | stdlib-only (REQ-403-075), Python `ast` module for analysis |

#### API Contract

```python
class PreToolEnforcementEngine:
    def evaluate_write(self, file_path: str, content: str) -> EnforcementDecision: ...
    def evaluate_edit(self, file_path: str, old_string: str, new_string: str) -> EnforcementDecision: ...
```

The `evaluate_edit` method (v1.1.0 redesign) performs in-memory file reconstruction: reads the target file, applies the `old_string -> new_string` replacement, then runs AST analysis on the reconstructed content. This addresses the B-002 blocking finding from iteration 1.

#### Enforcement Checks

| Check | Vector | Description |
|-------|--------|-------------|
| **AST Import Boundary Validation** | V-038 | 4 layer boundary rules: domain cannot import application/infrastructure/interface; application cannot import infrastructure/interface; infrastructure cannot import interface; shared_kernel cannot import infrastructure/interface |
| **One-Class-Per-File** | V-041 | Counts top-level class definitions in AST; blocks if > 1 public class |
| **Governance File Escalation** | -- | Writes to `.claude/rules/`, `JERRY_CONSTITUTION.md`, `CLAUDE.md` trigger C3/C4 escalation |
| **Dynamic Import Detection** | -- | Detects `importlib.import_module()` and `__import__()` calls that could bypass static analysis |

#### Exemptions

- `bootstrap.py` (composition root) is exempt from import boundary rules
- `TYPE_CHECKING` imports are exempt (runtime-irrelevant)
- Test files (`tests/`) may have relaxed import rules

#### EnforcementDecision Dataclass

```python
@dataclass
class EnforcementDecision:
    action: str          # "allow" | "block"
    reason: str          # Human-readable explanation
    violations: list     # List of specific violations found
    criticality_escalation: str | None  # "C3" | "C4" if governance file affected
```

#### Phased Execution in pre_tool_use.py

| Phase | Function | Status |
|-------|----------|--------|
| Phase 1 | Security checks (existing) | Existing |
| Phase 2 | Pattern checks (existing) | Existing |
| Phase 3 | AST enforcement (V-038, V-041) | NEW |
| Phase 4 | Governance file escalation | NEW |
| Phase 5 | Approve if all phases pass | Existing |

---

### SessionStart Hook (L1: Quality Context Enhancement)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Inject comprehensive quality context once at session start |
| **Engine Class** | `SessionQualityContextGenerator` |
| **Engine Location** | `src/infrastructure/internal/enforcement/session_quality_context.py` |
| **Token Cost** | ~360 tokens (additive to existing SessionStart output) |
| **Integration** | Additive -- does not replace existing SessionStart functionality |

#### XML Output Sections

| Section | Content | Tokens |
|---------|---------|--------|
| `<quality-gate>` | 0.92 threshold, S-014 scoring, leniency bias warning, 3-iteration minimum cycle | ~90 |
| `<constitutional-principles>` | P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception), UV (Python environment) | ~80 |
| `<adversarial-strategies>` | All 10 strategies: S-002 Devil's Advocate, S-003 Steelman, S-004 Red Team, S-007 Constitutional AI, S-010 Self-Refine, S-012 Dialectical, S-013 Inversion, S-014 LLM-as-Judge, S-015 Meta-Cognitive, S-016 Perspective Rotation | ~120 |
| `<decision-criticality>` | C1-C4 framework with auto-escalation rules | ~70 |

#### L1+L2 Coordination Design

SessionStart (L1) provides comprehensive context once; UserPromptSubmit (L2) reinforces critical rules every prompt. The two layers are complementary:

- **L1** sets the full behavioral foundation (all strategies, all principles, full quality gate)
- **L2** re-injects only the highest-priority rules that must survive context rot
- **Combined budget:** ~360 (L1 quality context) + 600 (L2 per-prompt) = ~960 tokens per session start, then 600 per subsequent prompt

---

## Rule-Based Enforcement Architecture (EN-404)

### Token Budget Optimization

| Metric | Current Baseline | Target | Phase 2 Allocation |
|--------|-----------------|--------|-------------------|
| Total L1 tokens | ~30,160 | 12,476 (REQ-404-001) | ~11,176 |
| CLAUDE.md | N/A | 2,000 max (REQ-404-002) | Within budget |
| Rules files | ~30,160 | 10,476 max (REQ-404-003) | ~9,176 |
| Buffer remaining | -- | -- | ~1,300 |

#### Token Reduction Strategy

| Strategy | Token Savings |
|----------|--------------|
| Code example reduction (~60% of current tokens) | ~12,000 |
| File consolidation (10 files to 8) | ~3,000 |
| Enforcement tier restructuring | ~2,000 |
| Redundancy elimination | ~1,060 |
| **Total estimated savings** | **~18,060** |

#### File Consolidation Plan

| Action | Files | Result |
|--------|-------|--------|
| Merge error-handling into coding-standards | error-handling-standards.md + coding-standards.md | coding-standards.md |
| Merge file-organization into architecture-standards | file-organization.md + architecture-standards.md | architecture-standards.md |
| Merge tool-configuration into testing-standards | tool-configuration.md + testing-standards.md | testing-standards.md |
| NEW: Create quality-enforcement.md (SSOT) | -- | quality-enforcement.md |
| **Result** | 10 files | 8 files |

### Per-File Token Breakdown (Current Baseline)

| File | Current Tokens | Notes |
|------|---------------|-------|
| architecture-standards.md | ~4,420 | 3 files with zero HARD language |
| coding-standards.md | ~3,250 | |
| testing-standards.md | ~3,120 | |
| error-handling-standards.md | ~3,640 | |
| file-organization.md | ~2,730 | |
| tool-configuration.md | ~3,380 | |
| mandatory-skill-usage.md | ~1,820 | |
| markdown-navigation-standards.md | ~2,860 | |
| project-workflow.md | ~1,560 | |
| python-environment.md | ~1,040 | |
| **Total** | **~30,160** | 2.42x over 12,476 target |

### Systemic Bypass Vectors (7 identified)

| ID | Vector | Description | Severity |
|----|--------|-------------|----------|
| BV-001 | Advisory Language Bypass | Passive/hedging language allows non-compliance | HIGH |
| BV-002 | Context Rot Degradation | Rules effectiveness degrades with context length | HIGH |
| BV-003 | Example Drowning | Code examples (~60% of tokens) dilute enforcement directives | HIGH |
| BV-004 | Redundancy Confusion | Same concept stated differently across files causes ambiguity | MEDIUM |
| BV-005 | Missing Consequence | No stated consequence for violation | MEDIUM |
| BV-006 | No Quality Gate | No explicit quality threshold in rules | MEDIUM |
| BV-007 | No Criticality Escalation | No decision-criticality framework in rules | MEDIUM |

### Tiered Enforcement System

#### HARD Rules Inventory (24 rules, max 25 per REQ-404-017)

| ID | Category | Rule Summary |
|----|----------|-------------|
| H-01 | Constitutional | P-003: Max ONE level orchestrator -> worker |
| H-02 | Constitutional | P-020: User decides, never override |
| H-03 | Constitutional | P-022: Never deceive about actions/capabilities/confidence |
| H-04 | Constitutional | Constitution CANNOT be overridden |
| H-05 | UV/Python | Python 3.11+ with UV only, NEVER system Python |
| H-06 | UV/Python | NEVER use python/pip/pip3 directly |
| H-07 | Architecture | Domain layer: NO imports from application/infrastructure/interface |
| H-08 | Architecture | Application layer: NO imports from infrastructure/interface |
| H-09 | Architecture | One class per file (MANDATORY) |
| H-10 | Architecture | All dependency wiring in bootstrap.py ONLY |
| H-11 | Coding | Type hints REQUIRED on all public functions/methods |
| H-12 | Coding | Docstrings REQUIRED on all public functions/classes/modules |
| H-13 | Quality | Quality gate score >= 0.92 REQUIRED for completion |
| H-14 | Quality | Minimum 3 creator-critic iterations REQUIRED |
| H-15 | Quality | S-014 LLM-as-Judge scoring REQUIRED |
| H-16 | Quality | Anti-leniency calibration REQUIRED |
| H-17 | Quality | Evidence-based closure REQUIRED |
| H-18 | Quality | Acceptance criteria verification REQUIRED |
| H-19 | Quality | BDD Red/Green/Refactor cycle REQUIRED |
| H-20 | Testing | 90% line coverage REQUIRED |
| H-21 | Testing | Architecture tests REQUIRED for boundary enforcement |
| H-22 | Skills | Mandatory skill invocation for trigger phrases |
| H-23 | Navigation | Navigation table REQUIRED in all Claude-consumed markdown |
| H-24 | Navigation | Anchor links REQUIRED in navigation tables |

#### Tier Vocabulary (Exclusive)

| Tier | Keywords | Consequence |
|------|----------|-------------|
| **HARD** | MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL | Violation blocks completion; automated enforcement where possible |
| **MEDIUM** | SHOULD, RECOMMENDED, PREFERRED, EXPECTED | Violation triggers warning; documented waiver acceptable |
| **SOFT** | MAY, CONSIDER, OPTIONAL, SUGGESTED | Guidance only; no enforcement action |

### quality-enforcement.md (SSOT)

A new file `quality-enforcement.md` serves as the Single Source of Truth for 5 shared enforcement concepts consumed by both rule files and hook engines:

| Concept | SSOT Value | Consumers |
|---------|-----------|-----------|
| Decision Criticality (C1-C4) | C1=routine, C2=design, C3=governance, C4=constitutional | PromptReinforcementEngine, PreToolEnforcementEngine, SessionQualityContextGenerator, rule files |
| Quality Threshold | 0.92 | All quality gate checks |
| Strategy Encodings | 6 adversarial strategy encodings (~119 tokens total) | Rule files, SessionQualityContextGenerator |
| Iteration Cycle Count | Minimum 3 | Quality gate enforcement |
| Tier Vocabulary | HARD/MEDIUM/SOFT exclusive word lists | All rule files |

### L2 Re-Injection Content (~510 tokens)

Priority-ranked content for V-024 context reinforcement, extracted via L2-REINJECT tags:

| Rank | Category | Content Summary | Tokens |
|------|----------|----------------|--------|
| 1 | CONSTITUTIONAL | P-003, P-020, P-022 hard constraints | ~65 |
| 2 | ENVIRONMENT | UV-only Python, NEVER system Python | ~45 |
| 3 | QUALITY GATE | 0.92 threshold, S-014 scoring, leniency calibration | ~80 |
| 4 | ARCHITECTURE | Domain import prohibition, one-class-per-file, bootstrap-only wiring | ~75 |
| 5 | CRITICALITY | C1-C4 escalation triggers | ~60 |
| 6 | TESTING | 90% coverage, BDD cycle, architecture tests | ~55 |
| 7 | SKILLS | Mandatory skill invocation for trigger phrases | ~50 |
| 8 | NAVIGATION | Navigation tables with anchor links | ~40 |
| **Total** | | | **~510** |

**Budget:** 510 of 600 tokens consumed, leaving 90-token buffer for future additions.

#### L2-REINJECT Tag Format

```html
<!-- L2-REINJECT: rank=N, tokens=NN, content="The enforcement text to inject" -->
```

Tags are placed in `.context/rules/*.md` files alongside the rules they reinforce. The PromptReinforcementEngine scans for these tags, sorts by rank, and concatenates until the 600-token budget is reached.

### HARD Language Patterns

#### 6 Effective Patterns (Use These)

| Pattern | Compliance Rate | Example |
|---------|----------------|---------|
| Constitutional Constraint | ~95% | "This constraint CANNOT be overridden. Violations will be blocked." |
| Forbidden/Required Binary | ~90% | "NEVER use python/pip/pip3 directly." |
| Layer Boundary Declaration | ~90% | "Domain layer: NO imports from application/infrastructure/interface." |
| Quality Gate Declaration | ~90% | "Quality gate score >= 0.92 REQUIRED for completion." |
| Mandatory Skill Invocation | ~85% | "You MUST use the following skills PROACTIVELY." |
| Escalation Trigger | ~85% | "Writes to governance files trigger C3/C4 escalation." |

#### 6 Anti-Patterns (Avoid These)

| Anti-Pattern | Bypass Rate | Example |
|-------------|------------|---------|
| Passive Voice | ~60% | "Tests should be written" (vs. "You MUST write tests") |
| Hedging | ~55% | "It's important to..." (vs. "REQUIRED:") |
| Buried Constraint | ~45-75% | Constraint hidden in paragraph of advisory text |
| Contradictory | ~40% | HARD rule contradicted by SOFT guidance elsewhere |
| Enforcement-Free Examples | ~50% | Code examples without corresponding enforcement rules |
| Unquantified Threshold | ~70% | "Good coverage" (vs. "90% line coverage REQUIRED") |

---

## 5-Layer Architecture Update

Phase 2 refined the 5-layer architecture from Phase 1 (Barrier 1 handoff) with concrete implementations:

| Layer | Phase 1 Status | Phase 2 Status | Implementation |
|-------|---------------|---------------|----------------|
| **L1: Static Context** | Conceptual (token budget TBD) | Designed (~11,176 tokens, 24 HARD rules, tiered enforcement) | EN-404 TASK-003 tiered enforcement + TASK-002 token optimization |
| **L2: Per-Prompt Reinforcement** | Conceptual (V-024 identified) | Designed (PromptReinforcementEngine, 600 tokens, ContentBlock system, L2-REINJECT tags) | EN-403 TASK-002 + EN-404 TASK-004 re-injection content |
| **L3: Pre-Action Gating** | Conceptual (V-038 identified) | Designed (PreToolEnforcementEngine, AST validation, governance escalation, zero tokens) | EN-403 TASK-003 |
| **L4: Post-Action Validation** | Conceptual | Not yet designed (Phase 3 scope) | -- |
| **L5: Post-Hoc Verification** | Conceptual (V-044, V-045) | Not yet designed (Phase 3 scope) | -- |
| **Process** | Conceptual (V-057, V-060) | Not yet designed (Phase 3 scope) | -- |

### Updated Defense-in-Depth Compensation Chain

| Layer | Primary Failure Mode | Compensating Layer | Phase 2 Evidence |
|-------|---------------------|-------------------|-----------------|
| L1 (Static Context) | Context rot after ~20K tokens | L2 re-injects ~510 tokens of critical rules every prompt | EN-404 TASK-003 token budget; EN-403 TASK-002 ContentBlocks |
| L2 (Per-Prompt Reinforcement) | LLM ignores re-injected rules (FM-403-07, RPN 336) | L3 deterministically blocks regardless of LLM state | EN-403 TASK-003 zero-token AST gating |
| L3 (Pre-Action Gating) | Fail-open on hook error (REQ-403-070) | L4 detects violations in output | Not yet designed |
| L4 (Post-Action Validation) | Self-critique degraded by context rot | L5 catches violations at commit/CI | Not yet designed |
| L5 (Post-Hoc Verification) | Violations already in codebase | Process blocks task closure without evidence | Not yet designed |

---

## Platform Constraints

### Token Budget Summary (All Layers)

| Layer | Budget | Per-Event | Notes |
|-------|--------|-----------|-------|
| L1: Static Context | ~11,176 tokens | Once at session start | 24 HARD rules, 8 rule files |
| L1: SessionStart quality context | ~360 tokens | Once at session start | SessionQualityContextGenerator |
| L2: Per-Prompt Reinforcement | 600 tokens | Every user prompt | PromptReinforcementEngine (~510 active + ~90 buffer) |
| L3: Pre-Action Gating | 0 tokens | Every write/edit operation | External Python process |
| L4: Post-Action Validation | 0-1,350 tokens | After tool calls | Not yet designed |
| L5: Post-Hoc Verification | 0 tokens | At commit/CI | External process |
| **Session start total** | **~11,536** | Once | L1 + SessionStart context |
| **Per-prompt incremental** | **600** | Every prompt | L2 reinforcement |

### Hook Platform Availability (Unchanged from Barrier 1)

| Hook | Claude Code | Cursor | Windsurf | Generic LLM |
|------|------------|--------|----------|-------------|
| PreToolUse | YES | NO | NO | NO |
| PostToolUse | YES | NO | NO | NO |
| SessionStart | YES | NO | NO | NO |
| UserPromptSubmit | YES | NO | NO | NO |

**Phase 2 constraint:** All three hook designs (UserPromptSubmit, PreToolUse, SessionStart) are Claude Code-exclusive. However, L1 (static context via rule files) and L5 (CI/pre-commit) remain 100% portable. The architecture degrades gracefully: without hooks, enforcement drops from L1+L2+L3 to L1-only at runtime, with L5 as the commit-time backstop.

### Graceful Degradation Matrix

| Deployment | Available Layers | Enforcement Level |
|------------|-----------------|-------------------|
| Claude Code (full) | L1 + L2 + L3 + L4 + L5 + Process | HIGH |
| Claude Code (hooks disabled) | L1 + L5 + Process | MODERATE |
| Non-Claude Code LLM | L1 + L5 + Process | MODERATE |
| No CI/pre-commit | L1 only | LOW |

---

## Implementation Capabilities

### What Enforcement CAN Do (After Phase 2)

| Category | Mechanism | Layer | Token Cost | Context Rot Immune |
|----------|-----------|-------|------------|-------------------|
| Import boundary validation | AST analysis via PreToolEnforcementEngine | L3 | 0 | YES |
| One-class-per-file enforcement | AST analysis via PreToolEnforcementEngine | L3 | 0 | YES |
| Governance file protection | Criticality escalation (C3/C4) via PreToolEnforcementEngine | L3 | 0 | YES |
| Context rot countermeasure | Per-prompt re-injection via PromptReinforcementEngine | L2 | 600 | YES (by design) |
| Quality context at session start | SessionQualityContextGenerator | L1 | ~360 | NO (one-time injection) |
| Tiered rule enforcement | HARD/MEDIUM/SOFT vocabulary in rule files | L1 | ~11,176 | NO (subject to context rot) |
| Decision criticality assessment | C1-C4 keyword matching in PromptReinforcementEngine | L2 | 0 (part of 600 budget) | YES |
| Strategy-aware reinforcement | ContentBlock selection based on criticality level | L2 | 0 (part of 600 budget) | YES |
| Dynamic import detection | AST analysis for importlib/\_\_import\_\_ | L3 | 0 | YES |

### What Enforcement CANNOT Do

| Gap | Why | Current Mitigation | ADV Phase 3 Opportunity |
|-----|-----|-------------------|------------------------|
| **Prevent context rot** | Inherent LLM limitation | L2 compensates (600 tok/prompt) but cannot eliminate | EN-304: Strategy-skill integration for session management |
| **Enforce semantic quality** | AST checks structure, not meaning | Process vectors (future) | EN-305: Adversarial skill for semantic review patterns |
| **Detect novel violation types** | AST rules are pre-defined | Property-based testing (future) | EN-307: Cross-strategy validation for unknown categories |
| **Enforce type hint correctness** | V-039 not yet implemented in PreToolEnforcementEngine | Deferred to Phase 3 | EN-305: Could integrate type checking into skill |
| **Enforce docstring quality** | V-040 not yet implemented | Deferred to Phase 3 | EN-305: Adversarial review of documentation quality |
| **Verify L2-REINJECT tag extraction works** | Not yet implemented in engine code (advisory N-A-001) | ContentBlock fallback | EN-304: Integration testing of tag extraction |
| **Catch UnicodeDecodeError in evaluate_edit** | Not explicitly handled (minor N-m-002) | Fail-open behavior | EN-305: Error handling hardening |

---

## Adversarial Strategy Integration Points

This section maps concrete integration opportunities for each ADV Phase 3 enabler.

### For EN-304 (Strategy-Skill Integration)

| Integration Point | Hook/Mechanism | What EN-304 Should Build |
|-------------------|---------------|-------------------------|
| **C1-C4 criticality triggers** | PromptReinforcementEngine.\_assess\_criticality() | Skill integration that maps criticality levels to strategy activation sets |
| **L2-REINJECT tag system** | Tag format in rule files | Skill capability to author and maintain L2-REINJECT tags for strategy content |
| **quality-enforcement.md SSOT** | New shared constants file | Skill reads SSOT for strategy encodings, threshold, criticality definitions |
| **SessionStart strategy listing** | SessionQualityContextGenerator | Skill ensures all strategies are correctly listed in session context |
| **ContentBlock priority system** | PromptReinforcementEngine.\_select\_blocks() | Skill can influence block selection based on active strategy context |

### For EN-305 (Adversarial Skill Implementation)

| Integration Point | Hook/Mechanism | What EN-305 Should Build |
|-------------------|---------------|-------------------------|
| **PreToolEnforcementEngine API** | evaluate_write() / evaluate_edit() | Adversarial skill can invoke enforcement checks programmatically |
| **EnforcementDecision dataclass** | action/reason/violations/criticality_escalation | Adversarial skill consumes enforcement decisions for review context |
| **24 HARD rules** | H-01 through H-24 | Adversarial skill validates compliance against HARD rule inventory |
| **6 effective patterns / 6 anti-patterns** | Language pattern analysis | Adversarial skill uses patterns to evaluate rule file quality |
| **Governance file escalation** | C3/C4 triggers in PreToolEnforcementEngine | Adversarial skill applies maximum scrutiny for governance changes |
| **Defense-in-depth chain** | Layer compensation model | Adversarial skill validates that each layer compensates its predecessor |

### For EN-307 (Cross-Strategy Validation)

| Integration Point | Hook/Mechanism | What EN-307 Should Validate |
|-------------------|---------------|---------------------------|
| **Combined token budget** | L1 (~11,176) + L1-quality (~360) + L2 (600/prompt) | Total enforcement overhead does not exceed context window capacity |
| **SSOT consistency** | quality-enforcement.md | All consumers (hooks, rules, skills) reference consistent values |
| **Strategy encoding coverage** | 6 encodings in SSOT (~119 tokens) | All 10 strategies have appropriate encoding or documented exclusion |
| **Tier vocabulary exclusivity** | HARD/MEDIUM/SOFT word lists | No word appears in multiple tiers; rule files comply |
| **Layer interaction effects** | L1+L2+L3 combined behavior | Layers do not conflict; combined enforcement is coherent |
| **Fail-open coordination** | REQ-403-070 across all hooks | Multiple fail-open hooks do not create compounding failure modes |

### Adversarial Strategy to Enforcement Layer Mapping

This mapping shows where each adversarial strategy has enforcement touchpoints:

| Strategy | L1 (Rules) | L2 (Per-Prompt) | L3 (Pre-Action) | L4 (Post-Action) | L5 (Post-Hoc) | Process |
|----------|-----------|-----------------|-----------------|-------------------|---------------|---------|
| S-002 Devil's Advocate | Encoded | C2+ activation | -- | Future | -- | Review pattern |
| S-003 Steelman | Encoded | C2+ activation | -- | Future | -- | Review pattern |
| S-004 Red Team | -- | C3+ activation | -- | Future | -- | Review pattern |
| S-007 Constitutional AI | Encoded | C2+ activation | Governance escalation | Future | -- | P-003/P-020/P-022 |
| S-010 Self-Refine | Encoded | All criticality levels | -- | Future | -- | Iteration cycle |
| S-012 Dialectical | -- | C3+ activation | -- | Future | -- | Review pattern |
| S-013 Inversion | Encoded | C3+ activation | -- | Future | -- | Review pattern |
| S-014 LLM-as-Judge | Encoded | C2+ activation | -- | Future | -- | Scoring |
| S-015 Meta-Cognitive | -- | -- | -- | Future | -- | Session management |
| S-016 Perspective Rotation | -- | -- | -- | Future | -- | Review pattern |

**Key observation:** 6 of 10 strategies have L1 rule encodings (~119 tokens). All 10 are listed in SessionStart quality context. Strategies activate progressively with criticality level, from S-010-only at C1 to all 10 at C4.

---

## Risk Summary

### FMEA Update (Phase 2)

| Metric | Phase 1 (Barrier 1) | Phase 2 (Barrier 2) | Delta |
|--------|---------------------|---------------------|-------|
| RPN > 200 items | 0 (for Tier 1-2 vectors) | 2 | +2 (new items from detailed design) |
| Quality score | 0.923 | 0.93 | +0.007 |
| Quality threshold | 0.85 | 0.92 | +0.07 (higher bar) |

### Residual Risks (RPN > 200)

| FMEA ID | Description | RPN | Layer | Mitigation Status |
|---------|-------------|-----|-------|------------------|
| FM-403-07 | Context rot degrades V-024 effectiveness (inherent LLM limitation) | 336 | L2 | ACCEPTED -- defense-in-depth compensates via L3 deterministic blocking |
| FM-404-08 | Strategy encodings too compact for LLM comprehension (~119 tokens for 6 strategies) | 240 | L1 | DEFERRED -- empirical testing needed; SessionStart provides full expansion |

### Residual Risks (RPN < 200, Notable)

| FMEA ID | Description | RPN | Notes |
|---------|-------------|-----|-------|
| FM-403-02 | Keyword-based criticality assessment is gameable | 252 | Compensated by L3 gating |
| N-m-001 | CLAUDE.md governance check missing from PreToolEnforcementEngine | Minor | Should be added to governance file list |
| N-m-002 | UnicodeDecodeError not explicitly caught in evaluate_edit | Minor | Fail-open behavior covers this |
| N-A-001 | L2-REINJECT tag extraction not yet implemented in engine code | Advisory | ContentBlock fallback ensures functionality |

### 4 RED Systemic Risks (Status from Phase 1)

| Risk ID | Description | Phase 2 Impact |
|---------|-------------|---------------|
| R-SYS-001 | Context rot degrades VULNERABLE vectors (correlated failure) | MITIGATED: L2 re-injection design provides 600 tokens/prompt compensation; L3 provides context-rot-immune gating |
| R-SYS-002 | Token budget not optimized (25,700 vs. 12,476) | ADDRESSED: EN-404 TASK-002/TASK-003 reduce from ~30,160 to ~11,176 allocated tokens |
| R-SYS-003 | Platform migration renders hooks inoperative | UNCHANGED: Graceful degradation matrix defined; L1/L5/Process remain portable |
| R-SYS-004 | Context rot + token exhaustion feedback loop | MITIGATED: Token budget optimization reduces L1 footprint; L2 budget fixed at 600 |

---

## ADR Reference

**ADR-EPIC002-002: Enforcement Vector Prioritization for Jerry Quality Framework**

| Attribute | Value |
|-----------|-------|
| **Status** | ACCEPTED (user ratified) |
| **Location** | `FEAT-005-enforcement-mechanisms/EN-402-enforcement-priority-analysis/TASK-005-enforcement-ADR.md` |
| **Decision** | Adopt 5-layer hybrid enforcement architecture with 16 Tier 1 vectors |
| **Phase 2 Enablers** | EN-403 (Hook-Based Enforcement) + EN-404 (Rule-Based Enforcement) |
| **Quality Score** | Phase 1: 0.923 PASS; Phase 2: 0.93 PASS |
| **Downstream** | ADV Phase 3 (EN-304, EN-305, EN-307) consumes enforcement designs |

---

## Source Traceability

### ENF Phase 2 Artifacts Consumed

| Artifact | Document ID | Version | Quality Score | Key Data Extracted |
|----------|-------------|---------|--------------|-------------------|
| EN-403 TASK-001: Hook Requirements | FEAT-005:EN-403-TASK-001 | v1.1.0 | 0.92 | 44 formal requirements (REQ-403-010 through REQ-403-096), fail-open policy, stdlib-only constraint, defense-in-depth chain |
| EN-403 TASK-002: UserPromptSubmit Design | FEAT-005:EN-403-TASK-002 | v1.1.0 | 0.92 | PromptReinforcementEngine class, ContentBlock system (7 blocks), 600 token budget, C1-C4 criticality, L2-REINJECT integration, accepted risks (RPN 336, 252) |
| EN-403 TASK-003: PreToolUse Design | FEAT-005:EN-403-TASK-003 | v1.1.0 | 0.94 | PreToolEnforcementEngine class with evaluate_write/evaluate_edit API, AST import boundary validation (V-038), one-class-per-file (V-041), governance escalation, zero token cost, phased execution |
| EN-403 TASK-004: SessionStart Design | FEAT-005:EN-403-TASK-004 | v1.1.0 | 0.90 | SessionQualityContextGenerator class, ~360 tokens quality context, 4 XML sections, L1+L2 coordination design, all 10 strategies listed |
| EN-404 TASK-001: Rule Requirements | FEAT-005:EN-404-TASK-001 | v1.1.0 | 0.90 | 44 formal requirements (REQ-404-001 through REQ-404-064), 12,476 token target, tiered enforcement, strategy encodings, L2 re-injection tags |
| EN-404 TASK-002: Rule Audit | FEAT-005:EN-404-TASK-002 | v1.1.0 | 0.91 | Current baseline ~30,160 tokens (2.42x over budget), per-file breakdown, 7 bypass vectors (BV-001 through BV-007), file consolidation plan, ~18,060 potential savings |
| EN-404 TASK-003: Tiered Enforcement | FEAT-005:EN-404-TASK-003 | v1.1.0 | 0.94 | 24 HARD rules (H-01 through H-24), tier vocabulary, quality-enforcement.md SSOT, C1-C4 framework, token allocation ~11,176, L2-REINJECT format, adversarial strategy encoding map |
| EN-404 TASK-004: HARD Language Patterns | FEAT-005:EN-404-TASK-004 | v1.1.0 | 0.90 | 6 effective patterns (~90-95% compliance), 6 anti-patterns (~40-75% bypass), L2 re-injection content ~510 tokens, tag extraction algorithm |

### Adversarial Review Artifact

| Artifact | Document ID | Quality Score | Key Data Extracted |
|----------|-------------|--------------|-------------------|
| EN-403 TASK-007: Iteration 2 Critique | FEAT-005:EN-403-TASK-007 | 0.93 PASS (overall) | Score delta +0.12 from iter 1, all 4 blocking resolved, all 7 major resolved, all 5 minor resolved, 2 new minor + 1 advisory, RPN > 200 reduced from 5 to 2, per-artifact scores |

### ADV Phase 3 Targets

| Artifact | Expected Consumer Use |
|----------|----------------------|
| EN-304: Strategy-Skill Integration | Integrate adversarial strategies into Jerry skill system using hook trigger points, L2-REINJECT tags, SSOT file, and ContentBlock priority system |
| EN-305: Adversarial Skill Implementation | Build adversarial skill using enforcement API contracts, HARD rule inventory, language patterns, and governance escalation triggers |
| EN-307: Cross-Strategy Validation | Validate combined token budgets, SSOT consistency, strategy encoding coverage, tier vocabulary exclusivity, and layer interaction coherence |

---

*Handoff Agent: ps-synthesizer (Claude Opus 4.6)*
*Date: 2026-02-13*
*Barrier: 2*
*Direction: ENF -> ADV*
*Quality: Data fully traced to EN-403 TASK-001 through TASK-004, EN-404 TASK-001 through TASK-004, and iteration 2 critique (TASK-007)*
