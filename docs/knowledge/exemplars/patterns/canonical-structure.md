# Canonical Documentation Structure

> **Version:** 1.0.0
> **Created:** 2026-01-05
> **Phase:** 38.17
> **Purpose:** Master artifact defining the canonical directory structure for all documentation artifacts

---

## Planning Model

We **CURRENTLY** operate on a **PHASE (aka. INITIATIVE) -> SUB-PHASE -> TASK -> SUB-TASK** planning model.

NOTE: In the **FUTURE** we will move to an INITIATIVE -> PAHSE -> TASK -> SUB-TASK planning model.

---

## Directory Structure

```
docs/                                                    # Root of the source repository
├── analysis/                                            # Folder for ANALYSIS Artifacts/Documents
│   └── phase-{phase_id}/                                # All ANALYSIS artifacts for PHASE
│       └── phase-{phase_id}.{subphase_id}-*.md          # Resultant artifacts from analysis
│                                                        # Examples:
│                                                        #   phase-38.17-e-051-root-cause-prevention.md
│                                                        #   phase-38.17-verification-analysis.md
│
├── designs/                                             # DESIGNs may become large so creating folders per Phase
│   └── phase-{phase_id}/                                # All design artifacts for PHASE
│       └── phase-{phase_id}.{subphase_id}-*.md          # Design docs (use cases, diagrams, etc.)
│                                                        # Examples:
│                                                        #   phase-38.17-e-191-signal-dispatcher-split-design.md
│                                                        #   phase-38.17-c009-subagent-persistence-enforcement.md
│
├── investigations/                                      # Folder for INVESTIGATION Artifacts
│   └── phase-{phase_id}/                                # All INVESTIGATION artifacts for PHASE
│       └── phase-{phase_id}.{subphase_id}-*-proof.md    # Evidence-linked artifacts
│                                                        # SCOPE: Formal or systematic examination or research
│                                                        # Examples:
│                                                        #   phase-38.17-e-043-investigation.md
│                                                        #   phase-38.17-e-045-investigation.md
│
├── plans/                                               # Folder for PLANS
│   └── phase-{phase_id}/                                # All PLAN artifacts for PHASE
│       └── phase-{phase_id}.{subphase_id}-*-plan.md     # Refined plans from Claude Code Plans
│                                                        # Examples:
│                                                        #   phase-38.14-bidirectional-sync-plan.md
│                                                        #   phase-38.17-debt-resolution-plan.md
│
├── research/                                            # Folder for RESEARCH Artifacts
│   └── phase-{phase_id}/                                # All RESEARCH artifacts for PHASE
│       └── phase-{phase_id}.{subphase_id}-*-RES.md      # Evidence-linked artifacts (suffix: -RES)
│                                                        # Examples:
│                                                        #   phase-38.17-e-165-documentation-audit-RES.md
│                                                        #   phase-38.17-e-059-claudemd-triggers-RES.md
│                                                        #   phase-38.17-high-fidelity-research-framework-RES.md
│
├── reviews/                                             # Folder for REVIEW Artifacts
│   └── phase-{phase_id}/                                # All REVIEW artifacts for PHASE
│       └── phase-{phase_id}.{subphase_id}-*-REV.md      # REVIEW artifacts (suffix: -REV)
│                                                        # Examples:
│                                                        #   phase-38.17-e-047-code-REV.md
│                                                        #   phase-38.17-e-054-research-REV.md
│                                                        #   phase-38.17-e-056-analysis-REV.md
│
├── synthesis/                                           # Folder for SYNTHESIZED Artifacts
│   └── phase-{phase_id}/                                # All SYNTHESIZED artifacts for PHASE
│       └── phase-{phase_id}.{subphase_id}-*-SYN.md      # SYNTHESIZED artifacts (suffix: -SYN)
│                                                        # Examples:
│                                                        #   phase-38.17-e-044-syntheses-SYN.md
│                                                        #   phase-38.17-e-057-SYN.md
│
├── knowledge/
│   ├── adrs/                                            # Architecture Decision Records (ADRs)
│   │   │                                                # Prefix: ADR
│   │   │                                                # SCOPE: Architecturally significant decisions (ASDs)
│   │   │                                                # - Choices impacting system structure
│   │   │                                                # - Non-functional requirements (NFRs)
│   │   │                                                # - Interfaces or technologies
│   │   │                                                # - Costly to change decisions
│   │   │                                                # MINIMUM KEY ELEMENTS:
│   │   │                                                # - Problem, Options, Decision, Consequences
│   │   │                                                # - Status (Proposed, Accepted, Rejected, Superseded)
│   │   ├── phase-{phase_id}/                            # All ADR artifacts for PHASE
│   │   │   └── phase-{phase_id}.{subphase_id}-*-ADR.md  # ADR artifacts (suffix: -ADR)
│   │   │                                                # Examples:
│   │   │                                                #   phase-38.17-e-165-documentation-audit-ADR.md
│   │   │                                                #   phase-38.17-high-fidelity-research-framework-ADR.md
│   │   └── ADR-{adr_id}-{adr_slug}.md                   # Promoted ADRs (phase -> repository)
│   │                                                    # Examples:
│   │                                                    #   ADR-001-Use-Cockburn-Use-Case-Methodology.md
│   │                                                    #   ADR-007-Port-Placement.md
│   │
│   ├── assumptions/                                     # ASSUMPTIONS
│   │   │                                                # Prefix: ASM
│   │   │                                                # SCOPE: Something taken as true without proof
│   │   │                                                # - Guides thoughts, actions, or designs
│   │   │                                                # - Can be dangerous if unchecked
│   │   │                                                # - Must be identified and tested
│   │   │                                                # USE: Track assumptions Claude makes during implementation
│   │   ├── phase-{phase_id}/                            # All ASSUMPTION artifacts for PHASE
│   │   │   └── phase-{phase_id}.{subphase_id}-*-ASM.md  # ASSUMPTION artifacts (suffix: -ASM)
│   │   │                                                # Examples:
│   │   │                                                #   phase-38.17-ASM-e-099-confluence-is-primary-ASM.md
│   │   └── ASM-{asm_id}-{asm_slug}.md                   # Promoted ASSUMPTIONS (phase -> repository)
│   │                                                    # Examples:
│   │                                                    #   ASM-001-Confluence-is-primary-authoring-tool.md
│   │                                                    #   ASM-005-Engineers-may-add-technical-details.md
│   │
│   ├── decisions/                                       # DECISIONS
│   │   │                                                # Prefix: DEC
│   │   │                                                # SCOPE: All choices (not all are architectural)
│   │   │                                                # PURPOSE: To solve problems and meet requirements
│   │   │                                                # WHAT: Any choice during software development
│   │   │                                                # - High-level architecture to low-level code
│   │   │                                                # ADR RELATIONSHIP: ADRs document KEY decisions
│   │   ├── phase-{phase_id}/                            # All DECISION artifacts for PHASE
│   │   │   └── phase-{phase_id}.{subphase_id}-*-DEC.md  # DECISION artifacts (suffix: -DEC)
│   │   │                                                # Examples:
│   │   │                                                #   phase-38.17-DEC-high-fidelity-research-framework.md
│   │   └── DEC-{dec_id}-{dec_slug}.md                   # Promoted DECISIONS (phase -> repository)
│   │                                                    # Examples:
│   │                                                    #   DEC-001-use-kebab-case.md
│   │                                                    #   DEC-007-prefer-markdown-for-user.md
│   │
│   ├── lessons/                                         # LESSONS
│   │   │                                                # Prefix: LES
│   │   │                                                # SCOPE: Insights from past experiences
│   │   │                                                # - What worked, what didn't, and why
│   │   │                                                # - Avoid repeating mistakes
│   │   │                                                # - Build on best practices
│   │   │                                                # - Bridge theory and real-world application
│   │   ├── phase-{phase_id}/                            # All LESSON artifacts for PHASE
│   │   │   └── phase-{phase_id}.{subphase_id}-*-LES.md  # LESSON artifacts (suffix: -LES)
│   │   │                                                # Examples:
│   │   │                                                #   phase-38.17-LES-high-fidelity-research-framework.md
│   │   └── LES-{les_id}-{les_slug}.md                   # Promoted LESSONS (phase -> repository)
│   │                                                    # Examples:
│   │                                                    #   LES-001-always-verify-before-claiming.md
│   │                                                    #   LES-030-hook-subprocess-isolation.md
│   │
│   └── patterns/                                        # PATTERNS and ANTI-PATTERNS
│       │                                                # Prefix: PAT (patterns), ANTI (anti-patterns)
│       │                                                # PATTERNS: Proven, reusable solutions (good practices)
│       │                                                # ANTI-PATTERNS: Common bad responses that seem right
│       │                                                #   but lead to negative, counterproductive results
│       ├── phase-{phase_id}/                            # All PATTERN/ANTI-PATTERN artifacts for PHASE
│       │   ├── phase-{phase_id}.{subphase_id}-*-ANTI.md # ANTI-PATTERN artifacts (suffix: -ANTI)
│       │   └── phase-{phase_id}.{subphase_id}-*-PAT.md  # PATTERN artifacts (suffix: -PAT)
│       │                                                # Examples:
│       │                                                #   phase-38.17-ANTI-high-fidelity-research-framework.md
│       │                                                #   phase-38.17-PAT-defense-in-depth.md
│       ├── ANTI-{anti_id}-{anti_slug}.md                # Promoted ANTI-PATTERNS (phase -> repository)
│       │                                                # Examples:
│       │                                                #   ANTI-001-vague-extensions.md
│       │                                                #   ANTI-002-missing-preconditions.md
│       └── PAT-{pat_id}-{pat_slug}.md                   # Promoted PATTERNS (phase -> repository)
│                                                        # Examples:
│                                                        #   PAT-001-use-kebab-case.md
│                                                        #   PAT-048-three-tier-enforcement.md
│
└── problems/
    ├── phase-{phase_id}/                                # All PROBLEM STATEMENT artifacts for PHASE
    │   ├── ps-{ps_id}-{short_slug}.md                   # Problem Statement artifact
    │   │                                                # Examples:
    │   │                                                #   ps-phase-38.17-debt-resolution.md
    │   │
    │   ├── constraints/                                 # All CONSTRAINT artifacts for PHASE
    │   │   └── c-{constraint_id}-{short_slug}.md        # Constraint artifacts
    │   │                                                # Examples:
    │   │                                                #   c-001-export-format-must-follow-spec.md
    │   │                                                #   c-002-all-domain-model-fields-exported.md
    │   │
    │   ├── discoveries/                                 # All DISCOVERY artifacts for PHASE
    │   │   │                                            # DISCOVERY sparks EXPLORATION
    │   │   │                                            # Definition: Finding something previously unknown
    │   │   │                                            # Outcome-Oriented: The "aha!" moment
    │   │   └── d-{discovery_id}-{short_slug}.md         # Discovery artifacts
    │   │                                                # Examples:
    │   │                                                #   d-001-export-format-discrepancy.md
    │   │
    │   ├── explorations/                                # All EXPLORATION artifacts for PHASE
    │   │   │                                            # EXPLORATION enables DISCOVERY
    │   │   │                                            # Definition: Searching to learn about something
    │   │   │                                            # Action-Oriented: The act of investigating
    │   │   └── e-{exploration_id}-{short_slug}.md       # Exploration artifacts
    │   │                                                # Examples:
    │   │                                                #   e-058-self-healing-hook.md
    │   │
    │   ├── evidence/                                    # All EVIDENCE artifacts for PHASE
    │   │   └── ev-{evidence_id}-{short_slug}.md         # Evidence artifacts
    │   │                                                # Examples:
    │   │                                                #   ev-001-orchestration-proof.md
    │   │
    │   └── questions/                                   # All QUESTION artifacts for PHASE
    │       └── q-{question_id}-{short_slug}.md          # Question artifacts
    │                                                    # Examples:
    │                                                    #   q-021-can-ps-orchestrator-be-skill.md
    │                                                    #   q-024-knowledge-only-stores-references.md
    │
    ├── constraints/                                     # Promoted CONSTRAINTS (phase -> repository)
    │   └── CONS-{constraint_id}-{short_slug}.md         # Examples:
    │                                                    #   CONS-003-capture-decision-rationale.md
    │                                                    #   CONS-007-hard-enforcement-no-pipe-grep.md
    │
    ├── discoveries/                                     # Promoted DISCOVERIES (phase -> repository)
    │   └── DISC-{discovery_id}-{short_slug}.md          # Examples:
    │                                                    #   DISC-001-enhanced-markdown-exporter.md
    │                                                    #   DISC-004-question-model-has-decisionitem.md
    │
    ├── explorations/                                    # Promoted EXPLORATIONS (phase -> repository)
    │   └── EXPL-{exploration_id}-{short_slug}.md        # Examples:
    │                                                    #   EXPL-001-support-multiple-sub-agents.md
    │                                                    #   EXPL-004-industry-best-practices-cqrs.md
    │
    ├── questions/                                       # Promoted QUESTIONS (phase -> repository)
    │   └── QUES-{question_id}-{short_slug}.md           # Examples:
    │                                                    #   QUES-001-constraint-validation-fields.md
    │                                                    #   QUES-003-rejectedalternative-fields.md
    │
    └── PS-{ps_id}-{short_slug}.md                       # Promoted PROBLEM STATEMENTS (phase -> repository)
                                                         # Examples:
                                                         #   PS-001-exploration-resolution-debt.md
                                                         #   PS-002-bidirectional-sync.md
```

---

## File Naming Conventions

### Artifact Type Suffixes

| Artifact Type | Suffix | Example |
|---------------|--------|---------|
| Research | `-RES` | `phase-38.17-e-058-self-healing-hook-RES.md` |
| Review | `-REV` | `phase-38.17-e-047-code-REV.md` |
| Synthesis | `-SYN` | `phase-38.17-e-057-SYN.md` |
| ADR | `-ADR` | `phase-38.17-event-sourcing-ADR.md` |
| Assumption | `-ASM` | `phase-38.17-confluence-is-primary-ASM.md` |
| Decision | `-DEC` | `phase-38.17-use-kebab-case-DEC.md` |
| Lesson | `-LES` | `phase-38.17-verify-before-claiming-LES.md` |
| Pattern | `-PAT` | `phase-38.17-defense-in-depth-PAT.md` |
| Anti-Pattern | `-ANTI` | `phase-38.17-completion-theater-ANTI.md` |
| Investigation | `-proof` | `phase-38.17-e-043-investigation-proof.md` |
| Plan | `-plan` | `phase-38.17-debt-resolution-plan.md` |

### Promotion Prefixes

| Entity Type | Prefix | Example |
|-------------|--------|---------|
| ADR | `ADR-` | `ADR-001-Use-Cockburn-Methodology.md` |
| Assumption | `ASM-` | `ASM-001-Confluence-is-primary.md` |
| Decision | `DEC-` | `DEC-001-use-kebab-case.md` |
| Lesson | `LES-` | `LES-030-hook-subprocess-isolation.md` |
| Pattern | `PAT-` | `PAT-048-three-tier-enforcement.md` |
| Anti-Pattern | `ANTI-` | `ANTI-001-vague-extensions.md` |
| Constraint | `CONS-` | `CONS-003-capture-decision-rationale.md` |
| Discovery | `DISC-` | `DISC-001-enhanced-markdown-exporter.md` |
| Exploration | `EXPL-` | `EXPL-001-support-multiple-sub-agents.md` |
| Question | `QUES-` | `QUES-001-constraint-validation-fields.md` |
| Problem Statement | `PS-` | `PS-001-exploration-resolution-debt.md` |

---

## Migration Notes

### From `sidequests/evolving-claude-workflow/docs/` to `docs/`

This structure replaces the previous sidequest-nested structure. All documentation now lives at the repository root under `docs/`.

**Previous Location:** `sidequests/evolving-claude-workflow/docs/proposals/phase-38/`
**New Location:** `docs/plans/phase-38/`

### Backward Compatibility

During migration:
1. Copy files to new canonical locations
2. Leave originals in place as backup
3. Update PS database artifact paths
4. Verify all code paths reference new locations
5. Remove originals after manual verification

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-05 | Initial canonical structure definition |