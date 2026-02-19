# Architecture Patterns

> Python architecture standards (Hexagonal + DDD + CQRS), teaching-edition walkthroughs, and domain-specific playbooks for building well-structured LLM agent frameworks.

---

## Key Findings

- **Hexagonal Architecture + DDD + CQRS** combined pattern provides clear boundary enforcement for LLM agent frameworks
- **Zero-dependency domain layer** is the critical architectural constraint — domain logic must not import from infrastructure or interface layers
- **Port/adapter pattern** enables infrastructure swapping (database, LLM provider, CLI) without touching domain or application logic
- **Teaching editions** prove the patterns are learnable — the Work Tracker Architecture walkthrough demonstrates the full stack

---

## Python Architecture Standards

The authoritative architecture reference for the Jerry Framework, defining layer boundaries, dependency directions, and anti-patterns.

??? abstract "Key Data"
    - **DDD + Hexagonal + CQRS** combined pattern
    - Dependency direction rules: Domain ← Application ← Infrastructure/Interface
    - Zero-dependency domain: HARD constraint (H-07)
    - Port/adapter boundaries with naming conventions
    - Anti-patterns catalog with remediation guidance
    - One-class-per-file rule (H-10) with CQRS naming conventions

[:octicons-link-external-16: Python Architecture Standards (645 lines)](https://github.com/geekatron/jerry/blob/main/docs/design/PYTHON-ARCHITECTURE-STANDARDS.md)

---

## Work Tracker Architecture: Teaching Edition

A teaching-edition walkthrough of the Hexagonal DDD CQRS architecture applied to a real bounded context in the Jerry Framework.

??? abstract "Key Data"
    - 1,049 lines of educational walkthrough
    - Layered architecture with concrete code examples
    - DDD bounded contexts applied to work tracking domain
    - CQRS pattern implementation with command/query separation
    - Step-by-step progression from domain → application → infrastructure

[:octicons-link-external-16: Teaching Edition (1,049 lines)](https://github.com/geekatron/jerry/blob/main/docs/knowledge/exemplars/architecture/work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md)

---

## Domain-Specific Playbooks

Reference playbooks for applying architecture patterns to specific bounded contexts.

??? abstract "Key Data"
    - Domain playbook patterns for bounded context guidance
    - 315 lines of reference material

[:octicons-link-external-16: Domain Playbooks (315 lines)](https://github.com/geekatron/jerry/blob/main/docs/knowledge/exemplars/architecture/domain_specific_playbooks.md)

---

## Related Research

- [Skill Compliance Framework](skill-compliance-framework.md)
- [Claude Code Ecosystem](claude-code-ecosystem.md)
- [Context Management](context-management.md)
