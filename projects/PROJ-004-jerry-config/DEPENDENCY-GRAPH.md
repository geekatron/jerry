# PROJ-004-jerry-config Dependency Graph

> Complete work item dependency visualization for the Jerry Configuration System project.

---

## Full Dependency Graph

```
                            PROJ-004-jerry-config DEPENDENCY GRAPH
═══════════════════════════════════════════════════════════════════════════════════

PHASE-00: Project Setup
┌─────────┐   ┌─────────┐
│ WI-001  │──►│ WI-002  │
│ Folder  │   │ Tracker │
└────┬────┘   └────┬────┘
     └──────┬──────┘
            ▼
PHASE-01: Research & Discovery (Parallel)
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ WI-003  │ │ WI-004  │ │ WI-005  │ │ WI-006  │
│ JSON5   │ │Collision│ │Worktree │ │ Config  │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     └───────────┴───────────┴───────────┘
                      │
                      ▼
PHASE-02: Architecture & Design
              ┌─────────┐
              │ WI-007  │
              │ PLAN.md │
              └────┬────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        WI-008: Domain Model Design                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐                                     │
│  │WI-008a  │ │WI-008b  │ │WI-008c  │  ◄── Research (parallel)            │
│  │Codebase │ │  DDD    │ │ Skill   │                                     │
│  └────┬────┘ └────┬────┘ └────┬────┘                                     │
│       └───────────┼───────────┘                                          │
│                   ▼                                                       │
│          ┌──── Synthesize ────┐                                          │
│          ▼        ▼           ▼                                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐                                     │
│  │WI-008d  │ │WI-008e  │ │WI-008f  │  ◄── Design (parallel ADRs)         │
│  │Framework│ │ Project │ │ Skill   │                                     │
│  │  ADR    │ │  ADR    │ │  ADR    │                                     │
│  └────┬────┘ └────┬────┘ └────┬────┘                                     │
│       └───────────┼───────────┘                                          │
│                   ▼                                                       │
│             ┌─────────┐                                                   │
│             │WI-008g  │  ◄── Session Context ADR                         │
│             │ Session │                                                   │
│             │  ADR    │                                                   │
│             └────┬────┘                                                   │
│                  ▼                                                        │
│             ┌─────────┐                                                   │
│             │WI-008h  │  ◄── Validation                                  │
│             │Validate │                                                   │
│             └────┬────┘                                                   │
└──────────────────┼───────────────────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
PHASE-03: Domain         PHASE-04: Infrastructure
    (Parallel)               (Parallel)
┌─────────┐             ┌─────────┐
│ WI-009  │             │ WI-012  │
│ Value   │             │ Atomic  │
│ Objects │             │  File   │
└────┬────┘             └────┬────┘
     │                       │
┌─────────┐             ┌─────────┐
│ WI-010  │             │ WI-013  │
│Aggregate│             │  Env    │
└────┬────┘             │ Adapter │
     │                  └────┬────┘
┌─────────┐                  │
│ WI-011  │             ┌────┴────┐
│ Events  │             │ WI-014  │◄── Depends on WI-012, WI-013
└────┬────┘             │ Layered │
     │                  │ Config  │
     │                  └────┬────┘
     └───────────┬───────────┘
                 ▼
PHASE-05: Integration & CLI
           ┌─────────┐
           │ WI-015  │◄── Depends on WI-009 through WI-014
           │ Session │
           │  Hook   │
           └────┬────┘
                │
           ┌─────────┐
           │ WI-016  │
           │  CLI    │
           │Commands │
           └────┬────┘
                │
        ┌───────┴───────┐
        ▼               ▼
PHASE-06: Testing & Validation
┌─────────┐       ┌─────────┐
│ WI-017  │       │ WI-018  │◄── Depends on WI-016, WI-017
│  Arch   │       │ Integ   │
│ Tests   │       │ Tests   │
└────┬────┘       └────┬────┘
     └────────┬────────┘
              ▼
PHASE-07: Documentation & Polish
┌─────────┐   ┌─────────┐   ┌─────────┐
│ WI-019  │──►│ WI-020  │──►│ WI-021  │
│ PLAN.md │   │  ADRs   │   │  Final  │
│ Update  │   │ Review  │   │  Docs   │
└─────────┘   └─────────┘   └─────────┘
```

---

## Critical Path

```
═══════════════════════════════════════════════════════════════════════════════════
                              CRITICAL PATH
═══════════════════════════════════════════════════════════════════════════════════

WI-001 → WI-002 → WI-003..006 → WI-007 → WI-008a..c → WI-008d..f → WI-008g → WI-008h
                                                                              │
    ┌────────────────────────────────────────────────────────────────────────┘
    │
    └─► WI-009..011 ─┬─► WI-015 → WI-016 ─┬─► WI-018 → WI-019 → WI-020 → WI-021
    └─► WI-012..014 ─┘                    └─► WI-017 ─┘
```

---

## Parallelization Lanes

```
═══════════════════════════════════════════════════════════════════════════════════
                           PARALLELIZATION LANES
═══════════════════════════════════════════════════════════════════════════════════

Lane 1 (WT-Main):    WI-001 → WI-002 → WI-003..006 → WI-007 → WI-008
                                          │
Lane 2 (WT-Domain):                       └─► WI-009, WI-010, WI-011 ─────┐
                                          │                               │
Lane 3 (WT-Infra):                        └─► WI-012, WI-013, WI-014 ────┤
                                                                          │
Lane 4 (WT-CLI):                                          WI-015, WI-016 ◄┘
                                                                   │
Lane 5 (WT-Test):                                    WI-017, WI-018 ◄┘
                                                              │
Lane 6 (WT-Docs):                               WI-019, WI-020, WI-021 ◄┘
```

---

## Work Item Dependency Matrix

| Work Item | Depends On | Blocks | Phase |
|-----------|------------|--------|-------|
| WI-001 | - | WI-002 | PHASE-00 |
| WI-002 | WI-001 | WI-003..006 | PHASE-00 |
| WI-003 | WI-002 | WI-007 | PHASE-01 |
| WI-004 | WI-002 | WI-007 | PHASE-01 |
| WI-005 | WI-002 | WI-007 | PHASE-01 |
| WI-006 | WI-002 | WI-007 | PHASE-01 |
| WI-007 | WI-003..006 | WI-008 | PHASE-02 |
| WI-008 | WI-007 | WI-009..014 | PHASE-02 |
| WI-008a | - | WI-008d..f | PHASE-02 |
| WI-008b | - | WI-008d..f | PHASE-02 |
| WI-008c | - | WI-008d..f | PHASE-02 |
| WI-008d | WI-008a..c | WI-008g | PHASE-02 |
| WI-008e | WI-008a..c | WI-008g | PHASE-02 |
| WI-008f | WI-008a..c | WI-008g | PHASE-02 |
| WI-008g | WI-008d..f | WI-008h | PHASE-02 |
| WI-008h | WI-008g | WI-009..014 | PHASE-02 |
| WI-009 | WI-008h | WI-015 | PHASE-03 |
| WI-010 | WI-008h | WI-015 | PHASE-03 |
| WI-011 | WI-008h | WI-015 | PHASE-03 |
| WI-012 | WI-008h | WI-014, WI-015 | PHASE-04 |
| WI-013 | WI-008h | WI-014 | PHASE-04 |
| WI-014 | WI-012, WI-013 | WI-015 | PHASE-04 |
| WI-015 | WI-009..014 | WI-016, WI-017 | PHASE-05 |
| WI-016 | WI-015 | WI-018 | PHASE-05 |
| WI-017 | WI-015 | WI-018 | PHASE-06 |
| WI-018 | WI-016, WI-017 | WI-019 | PHASE-06 |
| WI-019 | WI-018 | WI-020 | PHASE-07 |
| WI-020 | WI-019 | WI-021 | PHASE-07 |
| WI-021 | WI-019, WI-020 | - | PHASE-07 |

---

## Phase Dependencies

```
┌──────────┐
│ PHASE-00 │ Project Setup
│ WI-001   │
│ WI-002   │
└────┬─────┘
     │
     ▼
┌──────────┐
│ PHASE-01 │ Research & Discovery
│ WI-003   │ (4 parallel items)
│ WI-004   │
│ WI-005   │
│ WI-006   │
└────┬─────┘
     │
     ▼
┌──────────┐
│ PHASE-02 │ Architecture & Design
│ WI-007   │
│ WI-008   │ (+ 8 sub-items)
└────┬─────┘
     │
     ├──────────────────┐
     ▼                  ▼
┌──────────┐      ┌──────────┐
│ PHASE-03 │      │ PHASE-04 │  ◄── Parallel execution
│ WI-009   │      │ WI-012   │
│ WI-010   │      │ WI-013   │
│ WI-011   │      │ WI-014   │
└────┬─────┘      └────┬─────┘
     │                 │
     └────────┬────────┘
              ▼
       ┌──────────┐
       │ PHASE-05 │ Integration & CLI
       │ WI-015   │
       │ WI-016   │
       └────┬─────┘
            │
            ▼
       ┌──────────┐
       │ PHASE-06 │ Testing & Validation
       │ WI-017   │
       │ WI-018   │
       └────┬─────┘
            │
            ▼
       ┌──────────┐
       │ PHASE-07 │ Documentation & Polish
       │ WI-019   │
       │ WI-020   │
       │ WI-021   │
       └──────────┘
```

---

## Legend

| Symbol | Meaning |
|--------|---------|
| `───►` | Dependency (A blocks B) |
| `┌─┐` | Work item box |
| `│` | Vertical connection |
| `├` | Branch point |
| `└` | End of branch |
| `▼` | Flow direction |

---

## Statistics

| Metric | Value |
|--------|-------|
| Total Work Items | 29 |
| Main Work Items | 21 |
| Sub-Items (WI-008) | 8 |
| Phases | 8 |
| Parallel Lanes | 6 |
| Critical Path Length | 15 items |

---

## Related Documents

- [WORKTRACKER.md](WORKTRACKER.md) - Work tracking document
- [PLAN.md](PLAN.md) - Implementation plan
- [decisions/README.md](decisions/README.md) - ADR index
