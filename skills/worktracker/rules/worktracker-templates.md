# Worktracker Templates

> Rule file for /worktracker skill
> Source: CLAUDE.md lines 244-356 (EN-201 extraction)
> Extracted: 2026-02-01

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Work Tracker (worktracker) Templates](#work-tracker-worktracker-templates) | Template descriptions and directory structure |
| [Templates (MANDATORY)](#templates-mandatory) | Template usage rules and complete reference |
| [Cross-References](#cross-references) | Links to other worktracker rule files |

---

## Work Tracker (worktracker) Templates

Description:
- Work tracker (worktracker) templates are stored in the `docs/templates/worktracker/` folder.
- These templates provide a standardized structure for creating various work tracker artifacts such as Bugs, Enablers, Epics, Features, Spikes, Stories, and Tasks.
- Using these templates ensures consistency and completeness across all work tracker items.

Directory Structure:
```
.context/                                                                                                       # Respository level Documents Folder (root)
└── templates/                                                                                              # Repository level Templates Folder
    └── worktracker/                                                                                        # Templates for Worktracker Artifacts
        ├── BUG.md                                                                                          # Template for Bug
        ├── DECISION.md                                                                                     # Template for Decision
        ├── DISCOVERY.md                                                                                    # Template for Discovery
        ├── ENABLER.md                                                                                      # Template for Enabler
        ├── EPIC.md                                                                                         # Template for Epic
        ├── FEATURE.md                                                                                      # Template for Feature
        ├── IMPEDIMENT.md                                                                                   # Template for Impediment
        ├── SPIKE.md                                                                                        # Template for Spike
        ├── STORY.md                                                                                        # Template for Story
        └── TASK.md                                                                                         # Template for Task
```

---

## Templates (MANDATORY)

> **CRITICAL:** You MUST use the repository templates when creating ANY work items or artifacts.
> **DO NOT** make up your own formats. Always check for existing templates first.

### Work Tracker (worktracker) Templates

**Location:** `.context/templates/worktracker/`

Description:
- Work tracker (worktracker) templates are stored in the `docs/templates/worktracker/` folder.
- These templates provide a standardized structure for creating various work tracker artifacts such as Bugs, Enablers, Epics, Features, Spikes, Stories, and Tasks.
- Using these templates ensures consistency and completeness across all work tracker items.

Work tracker templates provide standardized structure for all work item types:

| Template | Use For | Path |
|----------|---------|------|
| `ENABLER.md` | EN-* files | `.context/templates/worktracker/ENABLER.md` |
| `TASK.md` | TASK-* files | `.context/templates/worktracker/TASK.md` |
| `BUG.md` | BUG-* files | `.context/templates/worktracker/BUG.md` |
| `DISCOVERY.md` | DISC-* files | `.context/templates/worktracker/DISCOVERY.md` |
| `DECISION.md` | DEC-* files | `.context/templates/worktracker/DECISION.md` |
| `SPIKE.md` | SPIKE-* files | `.context/templates/worktracker/SPIKE.md` |
| `EPIC.md` | EPIC-* files | `.context/templates/worktracker/EPIC.md` |
| `FEATURE.md` | FEAT-* files | `.context/templates/worktracker/FEATURE.md` |
| `STORY.md` | STORY-* files | `.context/templates/worktracker/STORY.md` |
| `IMPEDIMENT.md` | IMP-* files | `.context/templates/worktracker/IMPEDIMENT.md` |

### Problem-Solving & Knowledge Templates

**Location:** `docs/knowledge/exemplars/templates/`

Templates for problem-solving artifacts and knowledge documents:

| Template | Use For | Path |
|----------|---------|------|
| `adr.md` | Architecture Decision Records | `docs/knowledge/exemplars/templates/adr.md` |
| `research.md` | Research artifacts | `docs/knowledge/exemplars/templates/research.md` |
| `analysis.md` | Analysis artifacts | `docs/knowledge/exemplars/templates/analysis.md` |
| `deep-analysis.md` | Deep analysis | `docs/knowledge/exemplars/templates/deep-analysis.md` |
| `synthesis.md` | Synthesis documents | `docs/knowledge/exemplars/templates/synthesis.md` |
| `review.md` | Review artifacts | `docs/knowledge/exemplars/templates/review.md` |
| `investigation.md` | Investigation reports | `docs/knowledge/exemplars/templates/investigation.md` |
| `jrn.md` | Journal entries | `docs/knowledge/exemplars/templates/jrn.md` |
| `use-case-template.md` | Use case specifications | `docs/knowledge/exemplars/templates/use-case-template.md` |

### Template Usage Rules

1. **ALWAYS** read the template before creating a new file
2. **NEVER** make up your own format - use the existing templates
3. **INCLUDE** all required sections from the template
4. **REFERENCE** the template in the file's HTML comment header
5. **ASK** the user if unsure which template to use

### Directory Structure

```
.context/                                                                      # Repository level context
└── templates/                                                                 # Repository level Templates
    └── worktracker/                                                           # Templates for Worktracker Artifacts
        ├── BUG.md                                                             # Template for Bug
        ├── DECISION.md                                                        # Template for Decision
        ├── DISCOVERY.md                                                       # Template for Discovery
        ├── ENABLER.md                                                         # Template for Enabler
        ├── EPIC.md                                                            # Template for Epic
        ├── FEATURE.md                                                         # Template for Feature
        ├── IMPEDIMENT.md                                                      # Template for Impediment
        ├── SPIKE.md                                                           # Template for Spike
        ├── STORY.md                                                           # Template for Story
        └── TASK.md                                                            # Template for Task

docs/knowledge/exemplars/templates/                                            # Problem-solving templates
├── adr.md                                                                     # ADR (Michael Nygard format)
├── analysis.md                                                                # Analysis artifacts
├── deep-analysis.md                                                           # Deep analysis
├── investigation.md                                                           # Investigation reports
├── jrn.md                                                                     # Journal entries
├── research.md                                                                # Research artifacts
├── review.md                                                                  # Review artifacts
├── synthesis.md                                                               # Synthesis documents
└── use-case-template.md                                                       # Use case specifications
```

---

## Cross-References

- **Entity Hierarchy Rules**: `worktracker-entity-hierarchy.md`
- **System Mappings Rules**: `worktracker-system-mappings.md`
- **Behavior Rules**: `worktracker-behavior-rules.md`
- **Directory Structure Rules**: `worktracker-directory-structure.md`
