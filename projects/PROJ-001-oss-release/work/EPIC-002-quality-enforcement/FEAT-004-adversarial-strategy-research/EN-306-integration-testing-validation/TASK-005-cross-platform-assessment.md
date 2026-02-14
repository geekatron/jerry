# TASK-005: Cross-Platform Compatibility Assessment

<!--
DOCUMENT-ID: FEAT-004:EN-306:TASK-005
VERSION: 1.0.0
AGENT: ps-validator-306
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-306 (Integration Testing & Validation)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: TESTING
-->

> **Version:** 1.0.0
> **Agent:** ps-validator-306
> **Quality Target:** >= 0.92
> **Purpose:** Assess cross-platform compatibility of adversarial strategy integrations across macOS, Linux, and Windows environments

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this assessment covers |
| [Platform Context](#platform-context) | Platform taxonomy from EN-303 |
| [Enforcement Layer Portability](#enforcement-layer-portability) | Which enforcement layers are available per platform |
| [Graceful Degradation Analysis](#graceful-degradation-analysis) | How adversarial capabilities degrade on constrained platforms |
| [Per-Skill Platform Assessment](#per-skill-platform-assessment) | Platform compatibility for PS, NSE, and Orchestration |
| [Configuration Portability Tests](#configuration-portability-tests) | Tests for configuration consistency across platforms |
| [Risk Assessment](#risk-assessment) | Platform-specific risks and mitigations |
| [Traceability](#traceability) | Mapping to EN-306 AC-5 and FEAT-004 NFC-4 |
| [References](#references) | Source citations |

---

## Summary

This document assesses the cross-platform compatibility of all adversarial strategy integrations across the three target platforms: macOS (PLAT-CC), Linux (PLAT-CC variant), and Windows (PLAT-CC-WIN). The assessment focuses on the design-phase artifacts from EN-304, EN-305, and EN-307, evaluating whether the specified adversarial enhancements are platform-agnostic in their design or require platform-specific considerations.

The key finding is that the adversarial strategy integration is designed primarily at the **specification level** (markdown agent specs, YAML configuration, prompt templates) rather than the Python code level, making the design inherently portable. Platform-specific concerns arise only in the enforcement layer stack (L1-L5) and file system operations (path separators, filesystem case sensitivity).

---

## Platform Context

### Platform Taxonomy (EN-303 TASK-001, Dimension 7)

| Platform ID | Environment | Claude Code Available | Hooks Available | Filesystem |
|-------------|-------------|----------------------|-----------------|-----------|
| **PLAT-CC** | macOS with Claude Code | Yes | Yes (L2-L4) | Case-insensitive HFS+ / APFS |
| **PLAT-CC** | Linux with Claude Code | Yes | Yes (L2-L4) | Case-sensitive ext4 / xfs |
| **PLAT-CC-WIN** | Windows with Claude Code | Yes | Yes (L2-L4) | Case-insensitive NTFS |
| **PLAT-GENERIC** | Any platform without Claude Code | No | No (L1 + L5 + Process only) | Varies |

### Enforcement Layer Availability by Platform

| Layer | PLAT-CC (macOS) | PLAT-CC (Linux) | PLAT-CC-WIN | PLAT-GENERIC |
|-------|-----------------|-----------------|-------------|--------------|
| **L1** (Constitutional Rules) | Available | Available | Available | Available |
| **L2** (Prompt Reinforcement) | Available | Available | Available | Limited (no hooks) |
| **L3** (Pre-Tool Hooks) | Available | Available | Available | Not Available |
| **L4** (Post-Tool Hooks) | Available | Available | Available | Not Available |
| **L5** (CLAUDE.md/Rules) | Available | Available | Available | Available |
| **Process** (Workflow) | Available | Available | Available | Available |

---

## Enforcement Layer Portability

### Portable Stack (L1 + L5 + Process)

The adversarial strategy integration relies on a **portable enforcement stack** that works on all platforms (per NFR-305-003, NFR-307-006):

| Component | Portability | Rationale |
|-----------|-------------|-----------|
| Agent specifications (markdown) | Fully portable | Text files, no platform dependencies |
| SKILL.md documentation | Fully portable | Text files, no platform dependencies |
| PLAYBOOK.md procedures | Fully portable | Text files, no platform dependencies |
| ORCHESTRATION.yaml state | Fully portable | YAML is platform-agnostic; stdlib parsing only (NFR-307-004) |
| Prompt templates | Fully portable | Embedded in agent specs as text |
| Strategy selection logic | Fully portable | Defined in specifications, not compiled code |
| Quality score rubrics | Fully portable | Text-based evaluation criteria |
| CLAUDE.md rules (L5) | Fully portable | Markdown rules loaded at session start |
| Constitutional principles (L1) | Fully portable | Text-based principles in markdown files |
| Process-level enforcement | Fully portable | Workflow procedures enforced by agent behavior |

### Hook-Dependent Features (L2-L4)

| Feature | Hook Layer | Degradation on PLAT-GENERIC |
|---------|-----------|---------------------------|
| L2-REINJECT tags | L2 (Prompt Reinforcement) | Tags ignored; equivalent content available in L5 rules |
| ContentBlock injection (anti-leniency) | L2 | Calibration text must be manually included in prompts |
| PreToolEnforcementEngine | L3 | File write restrictions not enforced; L1 + L5 compensate |
| Governance file escalation (AE-001 through AE-005) | L3 | Auto-escalation not triggered; manual escalation required |
| PostToolEnforcementEngine | L4 | Post-action validation not enforced; Process layer compensates |

### ENF-MIN Handling (PLAT-GENERIC)

When hooks are unavailable (ENF-MIN), the adversarial protocol degrades per EN-303 TASK-003:

| Rule | Behavior |
|------|----------|
| ENF-MIN-001 | C1/C2 reviews proceed with L1+L5 enforcement only |
| ENF-MIN-002 | C3 reviews add mandatory human escalation flag |
| ENF-MIN-003 | C4 reviews REQUIRE human-in-the-loop (TEAM-HIL) |
| ENF-MIN-004 | Anti-leniency calibration text included in agent spec prompt templates (not hook-injected) |

---

## Graceful Degradation Analysis

### Strategy Availability by Platform

All 10 adversarial strategies are available on all platforms because they are implemented as **agent behavioral specifications** (prompt-driven), not as code-dependent features:

| Strategy | PLAT-CC (macOS/Linux) | PLAT-CC-WIN | PLAT-GENERIC |
|----------|----------------------|-------------|--------------|
| S-001 Red Team | Full | Full | Full (L1+L5) |
| S-002 Devil's Advocate | Full | Full | Full (L1+L5) |
| S-003 Steelman | Full | Full | Full (L1+L5) |
| S-004 Pre-Mortem | Full | Full | Full (L1+L5) |
| S-007 Constitutional AI | Full | Full | Partial (no auto-escalation hooks) |
| S-010 Self-Refine | Full | Full | Full (L1+L5) |
| S-011 Chain-of-Verification | Full | Full | Full (L1+L5) |
| S-012 FMEA | Full | Full | Full (L1+L5) |
| S-013 Inversion | Full | Full | Full (L1+L5) |
| S-014 LLM-as-Judge | Full | Full | Full (L1+L5) |

### Degradation Impact Assessment

| Impact Area | PLAT-CC (Full) | PLAT-CC-WIN (Full) | PLAT-GENERIC (Degraded) |
|-------------|---------------|-------------------|----------------------|
| Strategy execution | All 10 | All 10 | All 10 (prompt-based) |
| Quality scoring | S-014 automated | S-014 automated | S-014 automated |
| Anti-leniency | Hook-injected + spec-embedded | Hook-injected + spec-embedded | Spec-embedded only |
| Auto-escalation | Hook-triggered | Hook-triggered | Manual (user responsibility) |
| Governance file detection | PreToolEngine auto-detects | PreToolEngine auto-detects | User must declare criticality |
| Token budget tracking | Automated via hooks | Automated via hooks | Manual estimation |

---

## Per-Skill Platform Assessment

### /problem-solving (EN-304)

| Feature | macOS | Linux | Windows | PLAT-GENERIC |
|---------|-------|-------|---------|--------------|
| ps-critic 10 adversarial modes | Compatible | Compatible | Compatible | Compatible |
| Explicit mode selection (`--mode`) | Compatible | Compatible | Compatible | Compatible |
| Automatic mode selection (decision tree) | Compatible | Compatible | Compatible | Compatible (reduced auto-escalation) |
| Multi-mode pipelines (SEQ-001 through SEQ-005) | Compatible | Compatible | Compatible | Compatible |
| Quality score tracking | Compatible | Compatible | Compatible | Compatible |
| Anti-leniency calibration | Full (L2 + spec) | Full (L2 + spec) | Full (L2 + spec) | Partial (spec only) |
| Backward compatibility (BC-304-001 through BC-304-003) | Compatible | Compatible | Compatible | Compatible |

**Platform-specific concerns for PS:**
- None identified. All PS adversarial features are specification-level and prompt-based.

### /nasa-se (EN-305)

| Feature | macOS | Linux | Windows | PLAT-GENERIC |
|---------|-------|-------|---------|--------------|
| nse-verification 4 adversarial modes | Compatible | Compatible | Compatible | Compatible |
| nse-reviewer 6 adversarial modes | Compatible | Compatible | Compatible | Compatible |
| Strategy-to-gate mapping (10x5) | Compatible | Compatible | Compatible | Compatible |
| Criticality-based mode activation | Compatible | Compatible | Compatible | Compatible (manual escalation) |
| NPR finding categories (RFA/RFI/Comment) | Compatible | Compatible | Compatible | Compatible |
| Backward compatibility (BC-305-001 through BC-305-005) | Compatible | Compatible | Compatible | Compatible |
| Governance file escalation (AE rules) | Full (L3 hooks) | Full (L3 hooks) | Full (L3 hooks) | Manual |

**Platform-specific concerns for NSE:**
- Governance file escalation (FR-305-034) depends on PreToolEnforcementEngine hooks (L3). On PLAT-GENERIC, the user must manually declare elevated criticality when reviewing governance files.

### /orchestration (EN-307)

| Feature | macOS | Linux | Windows | PLAT-GENERIC |
|---------|-------|-------|---------|--------------|
| Creator-critic-revision cycle generation | Compatible | Compatible | Compatible | Compatible |
| ORCHESTRATION.yaml state tracking | Compatible | Compatible | Compatible* | Compatible |
| Quality gate enforcement | Compatible | Compatible | Compatible | Compatible |
| Barrier quality gates | Compatible | Compatible | Compatible | Compatible |
| ADVERSARIAL_FEEDBACK pattern | Compatible | Compatible | Compatible | Compatible |
| Template generation | Compatible | Compatible | Compatible | Compatible |

**Platform-specific concerns for Orchestration:**
- *Windows ORCHESTRATION.yaml paths: File paths in YAML should use forward slashes (POSIX-style) for portability. Backslash paths (Windows-native) may cause parsing issues on other platforms. The orch-planner should normalize paths to forward-slash format.
- L2-REINJECT tags (IR-307-003): On PLAT-GENERIC, these tags are ignored by the enforcement engine but remain harmless in the markdown content.

---

## Configuration Portability Tests

### CPT-001: Agent Spec Parsing Across Platforms

| Field | Specification |
|-------|---------------|
| **Test ID** | CPT-001 |
| **Scenario** | Agent spec files (ps-critic v3.0.0, nse-verification v3.0.0, nse-reviewer v3.0.0) parsed on macOS, Linux, Windows |
| **Pass Criteria** | 1. YAML frontmatter parses correctly on all platforms. 2. No encoding issues (UTF-8 consistent). 3. No line-ending issues (LF vs CRLF). 4. Agent identity and mode definitions load correctly. |

### CPT-002: ORCHESTRATION.yaml Portability

| Field | Specification |
|-------|---------------|
| **Test ID** | CPT-002 |
| **Scenario** | ORCHESTRATION.yaml created on macOS, parsed on Linux and Windows |
| **Pass Criteria** | 1. YAML parses without error on all platforms. 2. File paths in YAML use forward slashes. 3. Constraint values (threshold, iterations) read correctly. 4. Quality scores are numeric (not locale-dependent string representation). |

### CPT-003: Quality Score Consistency

| Field | Specification |
|-------|---------------|
| **Test ID** | CPT-003 |
| **Scenario** | S-014 LLM-as-Judge scoring on different platforms |
| **Pass Criteria** | 1. Scoring rubric produces consistent results regardless of platform. 2. Anti-leniency calibration text is identical on all platforms. 3. Threshold comparison (>= 0.92) uses consistent numeric comparison. |

### CPT-004: Filesystem Path Handling

| Field | Specification |
|-------|---------------|
| **Test ID** | CPT-004 |
| **Scenario** | Artifact paths referenced in adversarial invocations |
| **Pass Criteria** | 1. Forward-slash paths work on all platforms. 2. No hardcoded backslash paths in specifications. 3. Relative paths resolve correctly from project root. 4. Case sensitivity handled (Linux is case-sensitive; macOS/Windows are case-insensitive). |

### CPT-005: Template Portability

| Field | Specification |
|-------|---------------|
| **Test ID** | CPT-005 |
| **Scenario** | ORCHESTRATION templates generated on one platform, used on another |
| **Pass Criteria** | 1. Template content is platform-agnostic. 2. No OS-specific shell commands in templates. 3. YAML templates parse on all platforms. 4. Markdown templates render on all platforms. |

---

## Risk Assessment

### Platform-Specific Risks

| Risk | Platform | Likelihood | Impact | Mitigation |
|------|----------|------------|--------|------------|
| **CRLF line ending corruption** | Windows | MEDIUM | LOW | .gitattributes enforces LF for markdown/YAML; agents generate LF |
| **Case-sensitive path mismatches** | Linux | LOW | MEDIUM | Consistent case naming conventions; automated path validation |
| **Locale-dependent number formatting** | Windows (non-English locales) | LOW | MEDIUM | All quality scores use period decimal separator (YAML standard) |
| **Missing auto-escalation on PLAT-GENERIC** | PLAT-GENERIC | HIGH | MEDIUM | ENF-MIN-002/003 mandate human escalation at C3+; documented in SKILL.md |
| **FRR token budget exceeds context window** | All platforms | MEDIUM | HIGH | C4 (~50,300 tokens) may approach context limits; phased execution mitigates |
| **Anti-leniency bypass on PLAT-GENERIC** | PLAT-GENERIC | MEDIUM | MEDIUM | Calibration text embedded in agent spec (not hook-only); process enforcement as backup |

### Mitigation Summary

| Risk Category | Primary Mitigation | Secondary Mitigation |
|--------------|-------------------|---------------------|
| File format | .gitattributes, UTF-8 encoding | Pre-commit hooks |
| Path handling | Forward-slash convention | Path normalization in templates |
| Enforcement gaps (PLAT-GENERIC) | ENF-MIN handling rules | Human escalation at C3+ |
| Token budgets | Phased execution, budget tracking | Strategy subset selection under TOK-CONST |

---

## Traceability

### To EN-306 Acceptance Criteria

| EN-306 AC | Coverage |
|-----------|----------|
| AC-5 (Cross-platform compatibility confirmed) | This entire document |

### To FEAT-004 Non-Functional Criteria

| FEAT-004 NFC | Coverage |
|--------------|----------|
| NFC-4 (Cross-platform compatibility verified -- macOS, Windows, Linux) | This entire document |

### To Enabler Requirements

| Requirement | Assessment |
|-------------|-----------|
| NFR-305-003 (Portable enforcement stack) | Enforcement Layer Portability section |
| NFR-307-006 (Platform portability) | Per-Skill Platform Assessment section |
| EN-303 TASK-003 (ENF-MIN handling) | Graceful Degradation Analysis section |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | EN-303 TASK-001 (Context Taxonomy) -- FEAT-004:EN-303:TASK-001 | Dimension 7 (Platform Context): PLAT-CC, PLAT-CC-WIN, PLAT-GENERIC |
| 2 | EN-303 TASK-003 (Applicability Profiles) -- FEAT-004:EN-303:TASK-003 | ENF-MIN handling rules, platform portability guidance |
| 3 | EN-305 TASK-001 (NSE Requirements) -- FEAT-004:EN-305:TASK-001 | NFR-305-003 (portable enforcement stack) |
| 4 | EN-307 TASK-001 (Orchestration Requirements) -- FEAT-004:EN-307:TASK-001 | NFR-307-006 (platform portability), NFR-307-004 (template compatibility) |
| 5 | Barrier-2 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B2-ENF-TO-ADV | 5-layer enforcement architecture, graceful degradation matrix |
| 6 | EN-306 TASK-001 (Integration Test Plan) -- FEAT-004:EN-306:TASK-001 | Coverage matrix, risk assessment |

---

*Document ID: FEAT-004:EN-306:TASK-005*
*Agent: ps-validator-306*
*Created: 2026-02-13*
*Status: Complete*
