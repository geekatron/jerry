# Jerry Projects Registry

> Index of all projects managed within the Jerry Framework.

---

## Active Projects

| Project ID | Name | Status | Branch | Created |
|------------|------|--------|--------|---------|
| `PROJ-001-plugin-cleanup` | Multi-Project Support | 🔄 IN PROGRESS | `cc/task-subtask` | 2026-01-09 |
| `PROJ-002-nasa-systems-engineering` | NASA Systems Engineering | 🆕 PLANNING | `cc/proj-nasa-systems-engineering` | 2026-01-09 |

---

## Project Convention

### Directory Structure
```
projects/
├── README.md                        # This file (registry)
├── PROJ-{nnn}-{slug}/               # Project folder
│   ├── PLAN.md                      # Project implementation plan
│   ├── WORKTRACKER.md               # Work tracking document
│   └── .jerry/                      # Hidden operational state
│       └── data/
│           └── items/               # Work item JSON files
└── archive/                         # Archived/completed projects
```

### Project ID Format
- Pattern: `PROJ-{nnn}-{slug}`
- `{nnn}`: Zero-padded sequential number (001, 002, ...)
- `{slug}`: Kebab-case descriptive name
- Examples:
  - `PROJ-001-plugin-cleanup`
  - `PROJ-002-task-subtask`
  - `PROJ-003-knowledge-graph`

### Activating a Project

Set the `JERRY_PROJECT` environment variable:

```bash
# Bash/Zsh
export JERRY_PROJECT=PROJ-001-plugin-cleanup

# Fish
set -x JERRY_PROJECT PROJ-001-plugin-cleanup

# PowerShell
$env:JERRY_PROJECT = "PROJ-001-plugin-cleanup"
```

If `JERRY_PROJECT` is not set, Claude will prompt you to specify which project to work on.

### Creating a New Project

1. Determine the next project number (check this registry)
2. Create directory: `mkdir -p projects/PROJ-{nnn}-{slug}/.jerry/data/items`
3. Create `PLAN.md` using `/architect` command or template
4. Create `WORKTRACKER.md` from template
5. Add entry to this registry
6. Set `JERRY_PROJECT` environment variable

### Archiving a Project

1. Update project status to COMPLETED in registry
2. Move folder: `mv projects/PROJ-{nnn}-{slug} projects/archive/`
3. Update this registry

---

## Archived Projects

| Project ID | Name | Status | Archived |
|------------|------|--------|----------|
| *(legacy)* | Knowledge Architecture | ✅ ARCHIVED | 2026-01-09 |

> Note: Legacy archived files in `projects/archive/` predate this convention.

---

## Quick Reference

| Task | Command |
|------|---------|
| List projects | `ls projects/` |
| Check active | `echo $JERRY_PROJECT` |
| Switch project | `export JERRY_PROJECT=PROJ-xxx-slug` |
| View plan | `cat projects/$JERRY_PROJECT/PLAN.md` |
| View tracker | `cat projects/$JERRY_PROJECT/WORKTRACKER.md` |

---

*Last Updated: 2026-01-09*