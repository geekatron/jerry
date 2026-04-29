# PROJ-041 Dependency Chain Diagram

**Generated:** 2026-04-29T12:00:00Z

**Root Entity:** EPIC-001 (`/transcript` Skill Hardening)

**Diagram Type:** dependencies (flowchart LR)

**Entities Included:** 36 entities at Story/Bug/Enabler granularity (Tasks omitted)

**Max Depth Reached:** Cross-Feature dependency edges visualized

---

## Diagram

```mermaid
flowchart LR
    FEAT001["FEAT-001<br/>ADR-007 Foundation"]
    FEAT002["FEAT-002<br/>Contradictions<br/>Cleanup"]
    FEAT003["FEAT-003<br/>Deterministic<br/>Validation"]
    FEAT004["FEAT-004<br/>Schema<br/>Extensions"]
    FEAT005["FEAT-005<br/>Mindmap<br/>Hardening"]

    EN001["EN-001<br/>DDD Scaffolding"]
    EN002["EN-002<br/>Test Harness"]
    EN003["EN-003<br/>SubprocessSandbox"]
    EN004["EN-004<br/>/red-team<br/>Threat Model"]
    EN005["EN-005<br/>/UX<br/>JTBD+Feedback"]
    EN006["EN-006<br/>/diataxis<br/>Docs"]
    EN008["EN-008<br/>Final /adversary<br/>C4 Tournament"]

    S001["S-001<br/>Vendor ADR"]
    S002["S-002<br/>Promote ADR"]
    S003["S-003<br/>FILE-001..003"]
    S004["S-004<br/>CONTENT-001..003"]
    S005["S-005<br/>ANCHOR-001..003"]
    S006["S-006<br/>SCHEMA-001..008"]
    S007["S-007<br/>verify CLI"]
    S008["S-008<br/>update-anchors CLI"]
    S009["S-009<br/>Wire verify<br/>post-render"]
    S010["S-010<br/>Wire update-anchors<br/>pipeline"]
    S011["S-011<br/>Update ts-critic"]
    S012["S-012<br/>CI Validators"]
    S013["S-013<br/>editorial_<br/>conventions"]
    S014["S-014<br/>arithmetic_<br/>invariants"]
    S015["S-015<br/>discussions[]<br/>entity type"]
    S016["S-016<br/>audit_<br/>basis"]

    B001["B-001<br/>Token Caps"]
    B002["B-002<br/>chunk_id"]
    B003["B-003<br/>domain"]
    B004["B-004<br/>seg-NNN"]
    B005["B-005<br/>Backlinks"]
    B006["B-006<br/>Bracket<br/>Escaping"]
    B007["B-007<br/>Self-Claim"]

    %% Blocks relationships
    S001 -->|blocks| S002

    FEAT002 -->|blocks| S002

    FEAT001 -->|blocks| FEAT003
    FEAT002 -->|blocks| FEAT003

    FEAT001 -->|blocks| EN008
    FEAT002 -->|blocks| EN008
    FEAT003 -->|blocks| EN008
    FEAT005 -->|blocks| EN008
    EN004 -->|blocks| EN008
    EN005 -->|blocks| EN008
    EN006 -->|blocks| EN008

    EN004 -->|blocks| EN003

    EN001 -->|blocks| S003
    EN001 -->|blocks| S004
    EN001 -->|blocks| S005
    EN001 -->|blocks| S006
    EN002 -->|blocks| S003
    EN002 -->|blocks| S004
    EN002 -->|blocks| S005
    EN002 -->|blocks| S006

    S003 -->|blocks| S007
    S004 -->|blocks| S007
    S005 -->|blocks| S007
    S006 -->|blocks| S007

    S007 -->|blocks| S009
    S008 -->|blocks| S010

    S007 -->|blocks| S011
    S008 -->|blocks| S011

    S009 -->|blocks| S012
    S010 -->|blocks| S012

    S012 -->|blocks| EN008

    FEAT004 -->|blocks| EN008

    %% Cooperates relationships (dashed)
    S011 -.->|cooperates| S012
    EN005 -.->|cooperates| FEAT003
    EN006 -.->|cooperates| FEAT003
    EN006 -.->|cooperates| S011

    %% Color styling
    style FEAT001 fill:#FFF4E6,stroke:#FF8C00
    style FEAT002 fill:#FFF4E6,stroke:#FF8C00
    style FEAT003 fill:#FFF4E6,stroke:#FF8C00
    style FEAT004 fill:#FFF4E6,stroke:#FF8C00
    style FEAT005 fill:#FFF4E6,stroke:#FF8C00

    style EN001 fill:#F0F8FF,stroke:#4169E1
    style EN002 fill:#F0F8FF,stroke:#4169E1
    style EN003 fill:#F0F8FF,stroke:#4169E1
    style EN004 fill:#F0F8FF,stroke:#4169E1
    style EN005 fill:#F0F8FF,stroke:#4169E1
    style EN006 fill:#F0F8FF,stroke:#4169E1
    style EN008 fill:#F0F8FF,stroke:#4169E1

    style S001 fill:#F5F5F5,stroke:#555
    style S002 fill:#F5F5F5,stroke:#555
    style S003 fill:#F5F5F5,stroke:#555
    style S004 fill:#F5F5F5,stroke:#555
    style S005 fill:#F5F5F5,stroke:#555
    style S006 fill:#F5F5F5,stroke:#555
    style S007 fill:#F5F5F5,stroke:#555
    style S008 fill:#F5F5F5,stroke:#555
    style S009 fill:#F5F5F5,stroke:#555
    style S010 fill:#F5F5F5,stroke:#555
    style S011 fill:#F5F5F5,stroke:#555
    style S012 fill:#F5F5F5,stroke:#555
    style S013 fill:#F5F5F5,stroke:#555
    style S014 fill:#F5F5F5,stroke:#555
    style S015 fill:#F5F5F5,stroke:#555
    style S016 fill:#F5F5F5,stroke:#555

    style B001 fill:#FFE6E6,stroke:#CC0000
    style B002 fill:#FFE6E6,stroke:#CC0000
    style B003 fill:#FFE6E6,stroke:#CC0000
    style B004 fill:#FFE6E6,stroke:#CC0000
    style B005 fill:#FFE6E6,stroke:#CC0000
    style B006 fill:#FFE6E6,stroke:#CC0000
    style B007 fill:#FFE6E6,stroke:#CC0000
```

---

## Metadata

- **Entities Visualized:** EPIC-001 children at Story/Bug/Enabler granularity (16 Stories, 7 Bugs, 7 Enablers, 5 Features)
- **Relationships Shown:**
  - **Solid arrows (→):** `Blocks` dependencies (critical path ordering)
  - **Dashed arrows (-.->):** `Cooperates` relationships (parallel concerns, coordination points)
- **Critical Path Entries:**
  - FEAT-001 → FEAT-003 (governance foundation must precede validation implementation)
  - FEAT-002 → FEAT-003 (contradictions must be resolved before validators lock in behavior)
  - EN-004 → EN-003 (red-team threat model informs subprocess sandbox design)
  - EN-001/EN-002 → S-003/S-004/S-005/S-006 (enablers provide scaffolding & test harness)
  - S-003/S-004/S-005/S-006 → S-007 (all validator rule families must be implemented before CLI `verify` command)
  - S-007/S-008 → S-009/S-010 (CLI commands must exist before wiring into hooks/pipelines)
  - S-009/S-010 → S-012 (hooks and pipelines must be wired before CI validators run)
  - All Features/Enablers → EN-008 (final C4 tournament is Epic-level acceptance gate)
- **Cycles Detected:** No cycles. The dependency graph is a DAG (directed acyclic graph).
- **Parallelizable Phases:**
  - **Phase 1 (Governance):** FEAT-001, FEAT-002, EN-004 can run in parallel
  - **Phase 2 (Validation Infrastructure):** EN-001, EN-002, EN-003, FEAT-004, FEAT-005 can run in parallel (after Phase 1)
  - **Phase 3 (Validator Implementation):** S-003 through S-006 run in parallel (after EN-001/EN-002)
  - **Phase 4 (CLI & Integration):** S-007, S-008, EN-005, EN-006 in parallel; then S-009, S-010, S-011, S-012 in sequence per dependencies
  - **Phase 5 (Final Gate):** EN-008 C4 tournament (all prior phases complete)

---

## Notes

- **Execution Strategy:** The worktracker dependency chain (not `/orchestration` skill) coordinates execution order. Users implement entities in dependency order; CI enforces blockers via worktracker status checks.
- **Cross-Cutting Enablers:** EN-004 (/red-team threat model), EN-005 (/UX exploration), EN-006 (/diataxis documentation) apply across Features. Their primary `Blocks` relationship is to EN-008 (final tournament); secondary `Cooperates` edges to specific Features indicate collaboration points.
- **No Explicit Orchestration Plan:** User direction ("orchestration is overkill") — worktracker dependency chain serves as the execution plan.

---

*Generated by wt-visualizer v1.0.0*
