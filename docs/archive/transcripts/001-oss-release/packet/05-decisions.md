# Decisions

> **Transcript:** Jerry Framework Open-Source Release
> **Total Decisions:** 4

---

## Summary

| ID | Description | Confidence |
|----|-------------|------------|
| [DEC-001](#DEC-001) | MIT License for OSS release | 98% |
| [DEC-002](#DEC-002) | Use orchestration with NASA SE and PS agents | 90% |
| [DEC-003](#DEC-003) | Dual repository strategy | 90% |
| [DEC-004](#DEC-004) | Decomposition with imports pattern | 90% |

---

## Decisions

<a id="DEC-001"></a>
### DEC-001: Release Jerry with MIT License

| Field | Value |
|-------|-------|
| **Status** | Decided |
| **Confidence** | 98% |
| **Impact** | Strategic |

**Decision:** Release Jerry as open source with MIT license

**Rationale:** To make the framework publicly available with minimal restrictions on usage and contribution

**Context:**
> "project with an MIT license."
> — [seg-0010](02-transcript.md#seg-0010)

**Implications:**
- Maximum adoption potential
- Low barrier to contribution
- Commercial use permitted
- Standard open source licensing

---

<a id="DEC-002"></a>
### DEC-002: Orchestration with NASA SE and Problem Solving Agents

| Field | Value |
|-------|-------|
| **Status** | Decided |
| **Confidence** | 90% |
| **Impact** | Technical |

**Decision:** Use orchestration skill with NASA SE and problem solving agents

**Rationale:** To coordinate skills and agents effectively for the OSS release effort

**Context:**
> "or the best available agents, in both the NASA SE and the problem solving skill through the orchestration skill."
> — [seg-0015](02-transcript.md#seg-0015)

**Implications:**
- Multi-agent coordination for complex work
- Leverages existing skill infrastructure
- Enables adversarial critic patterns

---

<a id="DEC-003"></a>
### DEC-003: Dual Repository Strategy

| Field | Value |
|-------|-------|
| **Status** | Decided |
| **Confidence** | 90% |
| **Impact** | Organizational |

**Decision:** Rename current Jerry repository and create new public-facing one

**Rationale:** To separate internal development from public release

**Context:**
> "We are going to rename the current Jerry repository to something different like Jerry Internal, JerryCore, or Saucer Boy."
> — [seg-0028](02-transcript.md#seg-0028)

**Options Considered:**
1. Jerry Internal
2. JerryCore
3. Saucer Boy

**Implications:**
- Clean public API surface
- Internal experimentation can continue
- Clear separation of concerns
- Requires repository migration work

---

<a id="DEC-004"></a>
### DEC-004: Decomposition with Imports Pattern

| Field | Value |
|-------|-------|
| **Status** | Decided |
| **Confidence** | 90% |
| **Impact** | Architectural |

**Decision:** Use decomposition with imports for always-loaded components, file references for contextual loading

**Rationale:** To optimize context window usage and load content only when needed

**Context:**
> "and it needs to get decomposed, and it should leverage imports for those decomposed components that should always be pulled into memory, and everything else should just be as file references"
> — [seg-0040](02-transcript.md#seg-0040)

**Implementation:**
- Always-loaded: Use `@import` directive
- On-demand: Use file references and hyperlinks
- Write rules for when to load what

**Implications:**
- Better context window efficiency
- Clearer separation of critical vs. optional content
- Requires rules for contextual loading
- Addresses context rot mitigation

---

## Decision Matrix

| Decision | Impact Level | Reversibility | Dependencies |
|----------|--------------|---------------|--------------|
| DEC-001 | Strategic | Low (hard to change license) | None |
| DEC-002 | Technical | High | Orchestration skill |
| DEC-003 | Organizational | Medium | GitHub access |
| DEC-004 | Architectural | Medium | Skill architecture |

---

## Related Action Items

| Decision | Related Actions |
|----------|-----------------|
| DEC-001 | [ACT-010](04-action-items.md#ACT-010) (Create public repository) |
| DEC-002 | [ACT-003](04-action-items.md#ACT-003), [ACT-004](04-action-items.md#ACT-004) |
| DEC-003 | [ACT-009](04-action-items.md#ACT-009), [ACT-010](04-action-items.md#ACT-010) |
| DEC-004 | [ACT-012](04-action-items.md#ACT-012), [ACT-013](04-action-items.md#ACT-013) |
