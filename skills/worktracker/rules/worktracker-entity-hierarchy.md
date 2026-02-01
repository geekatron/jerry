# Worktracker Entity Hierarchy

> Rule file for /worktracker skill
> Source: CLAUDE.md (EN-201 extraction)
> Extracted: 2026-02-01

---

## 1: Entity Hierarchy

### 1.1 Complete Hierarchy Tree
```
WorkItem (abstract)
│
├── StrategicItem (abstract) ─────────────────── Long-term planning horizon
│   │
│   ├── Initiative ──────────────────────────── Portfolio-level strategic theme
│   │   └── Contains: Epic[]
│   │
│   ├── Epic ────────────────────────────────── Large initiative (weeks/months)
│   │   └── Contains: Capability[] | Feature[]
│   │
│   ├── Capability [OPTIONAL] ───────────────── SAFe Solution level (large solutions)
│   │   └── Contains: Feature[]
│   │
│   └── Feature ─────────────────────────────── Program-level feature (sprints)
│       └── Contains: Story[]
│
├── DeliveryItem (abstract) ─────────────────── Sprint-level execution
│   │
│   ├── Story ───────────────────────────────── User-valuable increment (days)
│   │   └── Contains: Task[]
│   │
│   ├── Task ────────────────────────────────── Atomic work unit (hours)
│   │   └── Contains: Subtask[]
│   │
│   ├── Subtask ─────────────────────────────── Indivisible work (hours)
│   │   └── Contains: (none - leaf node)
│   │
│   ├── Spike ───────────────────────────────── Timeboxed research/exploration
│   │   └── Contains: (none - leaf node)
│   │
│   └── Enabler ─────────────────────────────── Technical/infrastructure work
│       └── Contains: Task[]
│
├── QualityItem (abstract) ──────────────────── Defect and quality tracking
│   │
│   └── Bug ─────────────────────────────────── Defect requiring fix
│       └── Contains: Task[]
│
└── FlowControlItem (abstract) ──────────────── Workflow impediments
    │
    └── Impediment ──────────────────────────── Blocker requiring resolution
        └── Contains: (none - references blocked items)
```

### 1.2 Hierarchy Levels

| Level | Category  | Entities              | Planning Horizon | Typical Owner     |
|-------|-----------|-----------------------|------------------|-------------------|
| L0    | Portfolio | Initiative            | Quarters/Years   | Portfolio Manager |
| L1    | Strategic | Epic                  | Weeks/Months     | Product Manager   |
| L2    | Solution  | Capability (optional) | PIs              | Solution Manager  |
| L3    | Program   | Feature               | Sprints          | Product Owner     |
| L4    | Delivery  | Story, Enabler        | Days             | Development Team  |
| L5    | Execution | Task, Subtask, Spike  | Hours            | Individual        |
| -     | Quality   | Bug                   | Variable         | QA/Dev            |
| -     | Flow      | Impediment            | Immediate        | Scrum Master      |

---

## 2: Entity Classification and Properties

### 2.1 Classification Matrix

| Entity     | Category  | Level | Container | Atomic | Quality Gates | Optional |
|------------|-----------|-------|-----------|--------|---------------|----------|
| Initiative | Strategic | L0    | Yes       | No     | No            | Yes      |
| Epic       | Strategic | L1    | Yes       | No     | No            | No       |
| Capability | Strategic | L2    | Yes       | No     | No            | Yes      |
| Feature    | Strategic | L3    | Yes       | No     | No            | No       |
| Story      | Delivery  | L4    | Yes       | No     | Yes           | No       |
| Task       | Delivery  | L5    | Yes       | No     | Yes           | No       |
| Subtask    | Delivery  | L5    | No        | Yes    | Yes           | No       |
| Spike      | Delivery  | L5    | No        | Yes    | **No**        | No       |
| Enabler    | Delivery  | L4    | Yes       | No     | Yes           | No       |
| Bug        | Quality   | -     | Yes       | No     | Yes           | No       |
| Impediment | Flow      | -     | No        | Yes    | No            | No       |

### 2.2 Containment Rules Matrix

| Parent Type | Allowed Children            |
|-------------|-----------------------------|
| Initiative  | Epic                        |
| Epic        | Capability, Feature         |
| Capability  | Feature                     |
| Feature     | Story, Enabler              |
| Story       | Task, Subtask               |
| Task        | Subtask                     |
| Subtask     | (none)                      |
| Spike       | (none)                      |
| Enabler     | Task                        |
| Bug         | Task                        |
| Impediment  | (none - uses relationships) |
