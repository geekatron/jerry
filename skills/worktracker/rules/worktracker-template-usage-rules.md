# WORKTRACKER (a.k.a worktracker, work-tracker, work tracker) Templates (MANDATORY)

1. **CRITICAL:** You MUST use the repository templates when creating ANY work items or artifacts. **ALWAYS** read the respective template before creating a new file.
2. **DO NOT** make up your own formats. Always check for existing templates first.
3. **INCLUDE** all required sections from the template
4. **REFERENCE** the template in the file's HTML comment header
5. **ASK** the user if unsure which template to use
6.

### WORKTRACKER Template Location
**Location:** `.context/templates/worktracker/`

Work tracker templates provide standardized structure for all work item types:

| Template        | Use For             | Path                                           |
|-----------------|---------------------|------------------------------------------------|
| `BUG.md`        | `*BUG-*.md` files   | `.context/templates/worktracker/BUG.md`        |
| `DECISION.md`   | `*DEC-*.md` files   | `.context/templates/worktracker/DECISION.md`   |
| `DISCOVERY.md`  | `*DISC-*.md` files  | `.context/templates/worktracker/DISCOVERY.md`  |
| `ENABLER.md`    | `*EN-*.md` files    | `.context/templates/worktracker/ENABLER.md`    |
| `EPIC.md`       | `*EPIC-*` files     | `.context/templates/worktracker/EPIC.md`       |
| `FEATURE.md`    | `*FEAT-*` files     | `.context/templates/worktracker/FEATURE.md`    |
| `IMPEDIMENT.md` | `*IMP-*` files      | `.context/templates/worktracker/IMPEDIMENT.md` |
| `SPIKE.md`      | `*SPIKE-*.md` files | `.context/templates/worktracker/SPIKE.md`      |
| `STORY.md`      | `*STORY-*` files    | `.context/templates/worktracker/STORY.md`      |
| `TASK.md`       | `*TASK-*.md` files  | `.context/templates/worktracker/TASK.md`       |




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
