# Canonical Documentation Structure

> **Version:** 1.0.0
> **Created:** 2026-01-05
> **Project:** 38.17
> **Purpose:** Master artifact defining the canonical directory structure for all documentation artifacts

---

## Planning Model

We operate on a **PROJECT (aka. INITIATIVE) -> PHASE -> TASK -> SUB-TASK** planning model.

---

## Directory Structure

```
projects/                                                # Root of the source repository
├── ├──PROJ-{XXX}-project_id}/                             # ALL ARTIFACTS for PROJECT
    └── analysis/                                        # All ANALYSIS artifacts for PROJECT - Resultant artifacts from analysis
│       └── PROJ-{proj_id}.{X}-{X}.md          # Examples:
│                                                        #   PROJ-001-e-007-implementation-gap.md
│                                                        #   PROJ-001-e-009-alignment-validation.md
│                                                        
│
├── designs/                                             # DESIGNs may become large so creating folders per Project # All design artifacts for PROJECT                       
│       └── project-{project_id}.{subproject_id}-*.md          # Design docs (use cases, diagrams, etc.)
│                                                        # Examples:
│                                                        #   project-38.17-e-191-signal-dispatcher-split-design.md
│                                                        #   project-38.17-c009-subagent-persistence-enforcement.md
│
├── investigations/                                      # All INVESTIGATION artifacts for PROJECT                             
│       └── project-{project_id}.{subproject_id}-*-proof.md    # Evidence-linked artifacts
│                                                        # SCOPE: Formal or systematic examination or research
│                                                        # Examples:
│                                                        #   project-38.17-e-043-investigation.md
│                                                        #   project-38.17-e-045-investigation.md
│
├── plans/                                                  # All PLAN artifacts for PROJECT
│       └── project-{project_id}.{subproject_id}-*-plan.md  # Refined plans from Claude Code Plans
│                                                           # Examples:
│                                                           #   project-38.14-bidirectional-sync-plan.md
│                                                           #   project-38.17-debt-resolution-plan.md
│
├── research/                                               # All RESEARCH artifacts for PROJECT
│       └── project-{project_id}.{subproject_id}-*-RES.md   # Evidence-linked artifacts (suffix: -RES)
│                                                           # Examples:
│                                                           #   project-38.17-e-165-documentation-audit-RES.md
│                                                           #   project-38.17-e-059-claudemd-triggers-RES.md
│                                                           #   project-38.17-high-fidelity-research-framework-RES.md
│
├── reviews/                                                # All REVIEW artifacts for PROJECT
│       └── project-{project_id}.{subproject_id}-*-REV.md   # REVIEW artifacts (suffix: -REV)
│                                                           # Examples:
│                                                           #   project-38.17-e-047-code-REV.md
│                                                           #   project-38.17-e-054-research-REV.md
│                                                           #   project-38.17-e-056-analysis-REV.md
│
├── synthesis/                                           # Folder for SYNTHESIZED Artifacts
│   └── project-{project_id}/                                # All SYNTHESIZED artifacts for PROJECT
│       └── project-{project_id}.{subproject_id}-*-SYN.md      # SYNTHESIZED artifacts (suffix: -SYN)
│                                                        # Examples:
│                                                        #   project-38.17-e-044-syntheses-SYN.md
│                                                        #   project-38.17-e-057-SYN.md
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
│   │   ├── project-{project_id}/                            # All ADR artifacts for PROJECT
│   │   │   └── project-{project_id}.{subproject_id}-*-ADR.md  # ADR artifacts (suffix: -ADR)
│   │   │                                                # Examples:
│   │   │                                                #   project-38.17-e-165-documentation-audit-ADR.md
│   │   │                                                #   project-38.17-high-fidelity-research-framework-ADR.md
│   │   └── ADR-{adr_id}-{adr_slug}.md                   # Promoted ADRs (project -> repository)
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
│   │   ├── project-{project_id}/                            # All ASSUMPTION artifacts for PROJECT
│   │   │   └── project-{project_id}.{subproject_id}-*-ASM.md  # ASSUMPTION artifacts (suffix: -ASM)
│   │   │                                                # Examples:
│   │   │                                                #   project-38.17-ASM-e-099-confluence-is-primary-ASM.md
│   │   └── ASM-{asm_id}-{asm_slug}.md                   # Promoted ASSUMPTIONS (project -> repository)
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
│   │   ├── project-{project_id}/                            # All DECISION artifacts for PROJECT
│   │   │   └── project-{project_id}.{subproject_id}-*-DEC.md  # DECISION artifacts (suffix: -DEC)
│   │   │                                                # Examples:
│   │   │                                                #   project-38.17-DEC-high-fidelity-research-framework.md
│   │   └── DEC-{dec_id}-{dec_slug}.md                   # Promoted DECISIONS (project -> repository)
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
│   │   ├── project-{project_id}/                            # All LESSON artifacts for PROJECT
│   │   │   └── project-{project_id}.{subproject_id}-*-LES.md  # LESSON artifacts (suffix: -LES)
│   │   │                                                # Examples:
│   │   │                                                #   project-38.17-LES-high-fidelity-research-framework.md
│   │   └── LES-{les_id}-{les_slug}.md                   # Promoted LESSONS (project -> repository)
│   │                                                    # Examples:
│   │                                                    #   LES-001-always-verify-before-claiming.md
│   │                                                    #   LES-030-hook-subprocess-isolation.md
│   │
│   └── patterns/                                        # PATTERNS and ANTI-PATTERNS
│       │                                                # Prefix: PAT (patterns), ANTI (anti-patterns)
│       │                                                # PATTERNS: Proven, reusable solutions (good practices)
│       │                                                # ANTI-PATTERNS: Common bad responses that seem right
│       │                                                #   but lead to negative, counterproductive results
│       ├── project-{project_id}/                            # All PATTERN/ANTI-PATTERN artifacts for PROJECT
│       │   ├── project-{project_id}.{subproject_id}-*-ANTI.md # ANTI-PATTERN artifacts (suffix: -ANTI)
│       │   └── project-{project_id}.{subproject_id}-*-PAT.md  # PATTERN artifacts (suffix: -PAT)
│       │                                                # Examples:
│       │                                                #   project-38.17-ANTI-high-fidelity-research-framework.md
│       │                                                #   project-38.17-PAT-defense-in-depth.md
│       ├── ANTI-{anti_id}-{anti_slug}.md                # Promoted ANTI-PATTERNS (project -> repository)
│       │                                                # Examples:
│       │                                                #   ANTI-001-vague-extensions.md
│       │                                                #   ANTI-002-missing-preconditions.md
│       └── PAT-{pat_id}-{pat_slug}.md                   # Promoted PATTERNS (project -> repository)
│                                                        # Examples:
│                                                        #   PAT-001-use-kebab-case.md
│                                                        #   PAT-048-three-tier-enforcement.md
│
└── problems/
    ├── project-{project_id}/                                # All PROBLEM STATEMENT artifacts for PROJECT
    │   ├── ps-{ps_id}-{short_slug}.md                   # Problem Statement artifact
    │   │                                                # Examples:
    │   │                                                #   ps-project-38.17-debt-resolution.md
    │   │
    │   ├── constraints/                                 # All CONSTRAINT artifacts for PROJECT
    │   │   └── c-{constraint_id}-{short_slug}.md        # Constraint artifacts
    │   │                                                # Examples:
    │   │                                                #   c-001-export-format-must-follow-spec.md
    │   │                                                #   c-002-all-domain-model-fields-exported.md
    │   │
    │   ├── discoveries/                                 # All DISCOVERY artifacts for PROJECT
    │   │   │                                            # DISCOVERY sparks EXPLORATION
    │   │   │                                            # Definition: Finding something previously unknown
    │   │   │                                            # Outcome-Oriented: The "aha!" moment
    │   │   └── d-{discovery_id}-{short_slug}.md         # Discovery artifacts
    │   │                                                # Examples:
    │   │                                                #   d-001-export-format-discrepancy.md
    │   │
    │   ├── explorations/                                # All EXPLORATION artifacts for PROJECT
    │   │   │                                            # EXPLORATION enables DISCOVERY
    │   │   │                                            # Definition: Searching to learn about something
    │   │   │                                            # Action-Oriented: The act of investigating
    │   │   └── e-{exploration_id}-{short_slug}.md       # Exploration artifacts
    │   │                                                # Examples:
    │   │                                                #   e-058-self-healing-hook.md
    │   │
    │   ├── evidence/                                    # All EVIDENCE artifacts for PROJECT
    │   │   └── ev-{evidence_id}-{short_slug}.md         # Evidence artifacts
    │   │                                                # Examples:
    │   │                                                #   ev-001-orchestration-proof.md
    │   │
    │   └── questions/                                   # All QUESTION artifacts for PROJECT
    │       └── q-{question_id}-{short_slug}.md          # Question artifacts
    │                                                    # Examples:
    │                                                    #   q-021-can-ps-orchestrator-be-skill.md
    │                                                    #   q-024-knowledge-only-stores-references.md
    │
    ├── constraints/                                     # Promoted CONSTRAINTS (project -> repository)
    │   └── CONS-{constraint_id}-{short_slug}.md         # Examples:
    │                                                    #   CONS-003-capture-decision-rationale.md
    │                                                    #   CONS-007-hard-enforcement-no-pipe-grep.md
    │
    ├── discoveries/                                     # Promoted DISCOVERIES (project -> repository)
    │   └── DISC-{discovery_id}-{short_slug}.md          # Examples:
    │                                                    #   DISC-001-enhanced-markdown-exporter.md
    │                                                    #   DISC-004-question-model-has-decisionitem.md
    │
    ├── explorations/                                    # Promoted EXPLORATIONS (project -> repository)
    │   └── EXPL-{exploration_id}-{short_slug}.md        # Examples:
    │                                                    #   EXPL-001-support-multiple-sub-agents.md
    │                                                    #   EXPL-004-industry-best-practices-cqrs.md
    │
    ├── questions/                                       # Promoted QUESTIONS (project -> repository)
    │   └── QUES-{question_id}-{short_slug}.md           # Examples:
    │                                                    #   QUES-001-constraint-validation-fields.md
    │                                                    #   QUES-003-rejectedalternative-fields.md
    │
    └── PS-{ps_id}-{short_slug}.md                       # Promoted PROBLEM STATEMENTS (project -> repository)
                                                         # Examples:
                                                         #   PS-001-exploration-resolution-debt.md
                                                         #   PS-002-bidirectional-sync.md
```

---

## File Naming Conventions

### Artifact Type Suffixes

| Artifact Type | Suffix | Example |
|---------------|--------|---------|
| Research | `-RES` | `project-38.17-e-058-self-healing-hook-RES.md` |
| Review | `-REV` | `project-38.17-e-047-code-REV.md` |
| Synthesis | `-SYN` | `project-38.17-e-057-SYN.md` |
| ADR | `-ADR` | `project-38.17-event-sourcing-ADR.md` |
| Assumption | `-ASM` | `project-38.17-confluence-is-primary-ASM.md` |
| Decision | `-DEC` | `project-38.17-use-kebab-case-DEC.md` |
| Lesson | `-LES` | `project-38.17-verify-before-claiming-LES.md` |
| Pattern | `-PAT` | `project-38.17-defense-in-depth-PAT.md` |
| Anti-Pattern | `-ANTI` | `project-38.17-completion-theater-ANTI.md` |
| Investigation | `-proof` | `project-38.17-e-043-investigation-proof.md` |
| Plan | `-plan` | `project-38.17-debt-resolution-plan.md` |

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

**Previous Location:** `sidequests/evolving-claude-workflow/docs/proposals/project-38/`
**New Location:** `docs/plans/project-38/`

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