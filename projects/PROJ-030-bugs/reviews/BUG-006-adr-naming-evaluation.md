# Nielsen Heuristic Evaluation: ADR Naming Convention

> **Engagement ID:** (BUG-006)
> **Topic:** Architecture Decision Record (ADR) naming convention usability
> **Product:** Jerry Framework
> **Target Users:** Developers and architects who need to find, reference, and cross-reference ADRs across projects
> **Input:** Current ADR naming convention + 3 existing ADR examples + usage patterns across rule files
> **Evaluation Scope:** Screen-level (the naming convention itself is the "interface")

## Executive Summary

The current ADR naming convention (`ADR-{ENTITY_ID}-{NNN}`) fails on four of Nielsen's 10 heuristics:

1. **H2 (Match between system and real world)** — Severity 3: Entity IDs ("EPIC002", "PROJ007") are opaque to non-initiates and lack semantic content.
2. **H4 (Consistency and standards)** — Severity 2: Entity ID collision between projects using the same ID creates ambiguity in prose references.
3. **H6 (Recognition rather than recall)** — Severity 3: Users cannot recognize what an ADR addresses without looking it up. `ADR-EPIC002-001` is meaningless without context.
4. **H7 (Flexibility and efficiency of use)** — Severity 2: Power users cannot sort or grep meaningfully; directory listings do not surface decision domains.

**Overall assessment:** The convention works technically but fails usability tests for discoverability, reference clarity, and collision resistance at scale (50+ ADRs). Passing compliance on H1, H3, H5, H8, H9, H10.

**Remediation priority:** HIGH. Recommend adopting Alternative 3 (Domain-First Semantic) immediately as the baseline for all new ADRs, with a phased migration path for existing ADRs.

---

## Evaluation Context

### Product
Jerry Framework -- an LLM-agentic system for structured workflow governance and quality enforcement.

### Users
- **Developers** maintaining rule files, agent definitions, and SKILL.md documentation
- **Architects** making design decisions and cross-referencing ADRs for consistency
- **Orchestration agents** that may eventually query ADRs programmatically
- **New contributors** onboarding to the framework

### Current Convention
```
ADR-{ENTITY_ID}-{NNN}
├── ENTITY_ID = worktracker entity ID (e.g., EPIC002, PROJ007, STORY015)
└── NNN = sequential number within that entity (001, 002, etc.)

File names add a slug:
ADR-output-path-resolution-001.md
```

### Existing Examples
1. `ADR-output-path-resolution-001.md` (output path resolution)
2. `ADR-EPIC002-002-layer-enforcement-architecture.md` (quality gate architecture)
3. `ADR-PROJ007-001-agent-design.md` (agent definition format)
4. `ADR-PROJ007-002-routing-triggers.md` (routing architecture)
5. `ADR-STORY015-001-tier-model-renumbering.md` (tool tier classification)

### Search Context
- Located in `docs/design/` directory
- Referenced in `.context/rules/` files via prose citations: "See ADR-EPIC002-001 for details."
- Referenced in agent definitions and comments
- ~6 ADRs currently; 50+ expected in next 12 months

---

## Findings by Heuristic

### H1: Visibility of System Status — PASS

**Finding:** N/A — The naming convention is static, not interactive. System status visibility does not apply.

---

### H2: Match Between System and Real World — SEVERITY 3 (MAJOR)

**Finding F-001: Opaque Entity IDs Lack Real-World Semantics**

- **Heuristic:** H2 -- Match Between System and Real World
- **Severity:** 3 (Major usability problem)
- **Evidence:**
  - "EPIC002" tells a reader nothing about the architectural domain (quality enforcement, MCP tool integration, etc.)
  - Users must memorize the mapping: EPIC002 ↔ quality enforcement, PROJ007 ↔ agent patterns
  - Contrast with semantic naming: "ADR-output-path-resolution-001" immediately signals the domain
  - In `.context/rules/quality-enforcement.md`, the reference "ADR-EPIC002-001" appears 5 times without explanation in the same document, forcing readers to either (a) look up the ID, (b) guess, or (c) scroll to the References section to find the mapping

- **Remediation:** Replace entity ID with semantic domain term (e.g., "output-path-resolution", "agent-definition", "routing-architecture")
- **Effort:** Medium (changes all new ADRs; migration path for existing ADRs manageable over 2 quarters)

---

### H3: User Control and Freedom — PASS

**Finding:** N/A — Users can rename files freely. The naming convention does not restrict control or create lock-in. No violation found.

---

### H4: Consistency and Standards — SEVERITY 2 (MINOR-TO-MODERATE)

**Finding F-002: Entity ID Collision Between Projects Creates Ambiguity**

- **Heuristic:** H4 -- Consistency and Standards
- **Severity:** 2 (Minor usability problem; important to fix)
- **Evidence:**
  - `ADR-EPIC002-001` exists in two different projects with different meanings:
    - PROJ-022 (UX skill project): EPIC-002 = "user-experience-skill-wave-planning"
    - PROJ-004 (quality enforcement): EPIC-002 = "quality-enforcement-architecture"
  - In prose citations (e.g., "See ADR-EPIC002-001"), the reader cannot determine which project's ADR is referenced without additional context
  - The file system (`docs/design/` is project-root-level) prevents true collision, but readers cannot distinguish from citations alone
  - **Impact:** Low at current scale (6 ADRs), but becomes critical at 50+ ADRs where collisions become statistically inevitable

- **Remediation:** Include project ID in the ADR identifier (e.g., `ADR-proj-output-path-resolution-001` or `ADR-OUTPUT-PATH-RESOLUTION-proj022-001`)
- **Effort:** Medium (requires decision on collision resolution strategy)

---

### H5: Error Prevention — PASS

**Finding:** The convention is simple, follows a predictable pattern (entity-sequential), and prevents most user errors. No severity-2+ violations found.

---

### H6: Recognition Rather Than Recall — SEVERITY 3 (MAJOR)

**Finding F-003: Users Cannot Recognize ADR Purpose Without Lookup**

- **Heuristic:** H6 -- Recognition Rather Than Recall
- **Severity:** 3 (Major usability problem)
- **Evidence:**
  - When a user sees `ADR-PROJ007-002` in a file, they cannot determine what it addresses without:
    - (1) Recalling that PROJ007 = "agent patterns"
    - (2) Looking up the file
    - (3) Checking git log or file creation date to disambiguate from `ADR-PROJ007-001`
  - The slug in the filename (`-routing-triggers`) provides recognition, but:
    - Slugs are not part of the ID (only the `ADR-PROJ007-002` part is cited in prose)
    - Not all references include the full filename (many citations are just the ID)
    - Directory listings and grep results show only the ID, not the slug
  - Contrast: "ADR-output-path-resolution-001" is immediately recognizable; users know exactly what decision is referenced without lookup

- **Remediation:** Move semantic content from the filename slug into the ADR ID itself (e.g., `ADR-001-output-path-resolution` or `ADR-output-path-resolution-001`)
- **Effort:** Medium (requires identifier redesign; slug becomes redundant)

---

### H7: Flexibility and Efficiency of Use — SEVERITY 2 (MINOR)

**Finding F-004: Power Users Cannot Efficiently Query or Sort ADRs**

- **Heuristic:** H7 -- Flexibility and Efficiency of Use
- **Severity:** 2 (Minor usability problem)
- **Evidence:**
  - A developer trying to find "all ADRs related to output paths" cannot grep by semantic content in the ID (only `grep -r "output.path"` works, which is crude)
  - Directory listings sort by entity ID first (EPIC002-001, PROJ007-001, STORY015-001), not by decision domain, making it hard to discover related ADRs
  - Power users who expect `ls docs/design/ADR-* | sort` to surface decision clusters are disappointed; clusters are scattered by entity ID
  - A developer cannot quickly determine "how many ADRs exist for agent design?" without reading filenames or grepping

- **Remediation:** Adopt domain-first sorting (all agent-related ADRs cluster together in directory listings) and domain-first IDs (enable grep queries like `grep -r "ADR-agent-" docs/design/`)
- **Effort:** Low (primarily a sorting/ID structure change; requires no code changes)

---

### H8: Aesthetic and Minimalist Design — PASS

**Finding:** The convention is concise and follows established ADR naming patterns (Nygard, AWS). No clutter or excess. No violation found.

---

### H9: Help Users Recognize, Diagnose, and Recover from Errors — PASS

**Finding:** Error scenarios (typos in entity IDs, duplicate sequential numbers within an entity) are unlikely. When they occur, git history and file system provide sufficient recovery mechanisms. No violation found.

---

### H10: Help and Documentation — PASS

**Finding:** The convention is documented in `quality-enforcement.md` and ADR files themselves use clear frontmatter. Documentation exists, though it could be more discoverable. No severity-2+ violation.

---

## Ranked Findings Summary

| ID | Heuristic | Severity | Affected Context | Status |
|----|-----------|----------|------------------|--------|
| F-003 | H6 (Recognition) | 3 | All ADR citations in prose | Open |
| F-001 | H2 (Real-world match) | 3 | Entity ID interpretation | Open |
| F-002 | H4 (Consistency) | 2 | Cross-project references | Open |
| F-004 | H7 (Efficiency) | 2 | Directory browsing, grep queries | Open |

**Total:** 4 findings (0 severity 0-1, 2 severity 2, 2 severity 3)

---

## Remediation Roadmap

### Immediate Actions (Low Effort)
- **F-004 (Efficiency):** Establish sorting convention. New ADRs adopt domain-first IDs to enable clustering in directory listings.
- **Effort:** Low
- **Owner:** Framework lead

### Short-Term (Medium Effort, 1-2 Sprints)
- **F-001 & F-003 (Semantic content):** Adopt new naming convention for all future ADRs using Domain-First Semantic pattern (Alternative 3, detailed below).
- **F-002 (Collision):** Establish collision detection policy for edge cases.
- **Effort:** Medium (design + implementation in new ADRs; optional migration of 6 existing ADRs)
- **Owner:** ADR authors + governance lead

### Long-Term (Medium Effort, 1-2 Quarters)
- **Phased migration:** Redirect old-style ADR references (`ADR-EPIC002-001`) to new files using semantic naming, with aliases in `docs/design/README.md` for backward compatibility during transition.
- **Effort:** Medium
- **Owner:** Documentation owner + ADR authors

---

## Alternative Naming Conventions

Three alternatives are evaluated below on six criteria:

| Criterion | Definition |
|-----------|-----------|
| **Discoverability** | Can users find ADRs related to a domain via grep, directory listing, or keyword search? |
| **Referenceability** | Can ADRs be cited concisely in prose without ambiguity? |
| **Collision Resistance** | Will the scheme scale to 50+ ADRs without collisions? |
| **Sortability** | Do directory listings cluster related ADRs together? |
| **Traceability** | Can users link back to the worktracker entity that produced the decision? |
| **Compatibility** | How compatible is the scheme with current Nygard ADR format expectations? |

---

### Alternative 1: Entity-First with Global Sequential (Minimal Change)

**Format:** `ADR-{ENTITY_ID}-{GLOBAL_SEQUENCE}-{slug}`

```
ADR-output-path-resolution-001.md
ADR-EPIC002-002-enforcement-architecture.md
ADR-PROJ007-003-agent-design.md
ADR-PROJ007-004-routing-architecture.md
ADR-STORY015-005-tier-model-renumbering.md
```

**Rationale:** Replaces local-entity sequencing with a global counter, eliminating ID collisions across projects while retaining worktracker traceability.

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Discoverability** | 2/5 (Poor) | Entity IDs still opaque. Grep for "ADR-EPIC002" finds all EPIC-002 decisions regardless of domain. |
| **Referenceability** | 2/5 (Poor) | Still requires memo: "EPIC002 = quality enforcement." References remain cryptic. |
| **Collision Resistance** | 5/5 (Excellent) | Global sequence guarantees no collisions. Scales to 1000+ ADRs. |
| **Sortability** | 2/5 (Poor) | Directory sorts by entity ID first (EPIC002-001, EPIC002-002, PROJ007-003) -- related ADRs scatter. |
| **Traceability** | 5/5 (Excellent) | Entity ID directly links to worktracker; metadata preserved. |
| **Compatibility** | 5/5 (Excellent) | Minimal change to current convention; Nygard format unchanged. |

**Trade-offs:**
- **Pros:** Backward-compatible. Preserves worktracker linkage. No collision. Simple increment.
- **Cons:** Does NOT solve F-001 (opaque IDs) or F-003 (no recognition). Does NOT enable domain-based discovery.

**Verdict:** Addresses collision risk but ignores the two most severe findings (F-001, F-003). Minimal improvement over current state.

---

### Alternative 2: Domain-Annotated (Hybrid)

**Format:** `ADR-{ENTITY_ID}-{GLOBAL_SEQ}_{DOMAIN}_{NNN}-{slug}`

```
ADR-EPIC002-001_output-path-resolution_001-unified-output-path.md
ADR-EPIC002-002_enforcement-architecture_001-layer-enforcement.md
ADR-PROJ007-003_agent-design_001-canonical-format.md
ADR-PROJ007-004_agent-design_002-routing-architecture.md
ADR-STORY015-005_tier-model_001-renumbering.md
```

**Rationale:** Adds domain name to the ID while retaining entity ID and worktracker traceability. Longer IDs but richer semantic content.

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Discoverability** | 4/5 (Good) | Grep for "ADR-agent-design" finds all agent-related decisions. Domain content is now parseable. |
| **Referenceability** | 4/5 (Good) | `ADR-output-path-resolution_001` is immediately recognizable. Still carries entity context via prefix. |
| **Collision Resistance** | 5/5 (Excellent) | Global sequence + domain namespacing prevents all collisions. |
| **Sortability** | 3/5 (Moderate) | Domain substring enables partial clustering (all "agent-design" ADRs together if prefixed uniformly). Splits on entity ID first. |
| **Traceability** | 5/5 (Excellent) | Entity ID preserved; full context link remains. |
| **Compatibility** | 3/5 (Moderate) | Longer IDs; Nygard format unchanged but identifiers become unwieldy. References may wrap in text. |

**Trade-offs:**
- **Pros:** Solves F-001 and F-003 (semantic content visible). Improves discoverability. Retains traceability.
- **Cons:** IDs become long and verbose (e.g., `ADR-EPIC002-001_output-path-resolution_001`). Sorting still dominated by entity ID. Hybrid approach adds complexity.

**Verdict:** Balanced solution. Solves visibility but at the cost of verbosity. Sorting still not optimal.

---

### Alternative 3: Domain-First Semantic (RECOMMENDED)

**Format:** `ADR-{DOMAIN}-{NNN}` with optional project context in prose or frontmatter

```
docs/design/
  ADR-output-path-resolution-001-unified-output-path.md
  ADR-enforcement-architecture-001-layer-enforcement.md
  ADR-agent-design-001-canonical-format.md
  ADR-agent-design-002-routing-architecture.md
  ADR-tier-model-001-renumbering.md
```

**With project linkage in frontmatter:**
```yaml
# ADR-output-path-resolution-001
---
type: adr
entity_id: EPIC-002
project: PROJ-004
domain: output-path-resolution
sequence: 001
status: proposed
---
```

**Rationale:** Inverts the priority: domain first (recognition), entity second (traceability). Enables both discovery and reference.

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Discoverability** | 5/5 (Excellent) | Grep `ADR-agent-design` finds all agent design decisions. Directory listing clusters by domain (`ADR-agent-*`, `ADR-enforcement-*`, etc.). Domain is primary navigation. |
| **Referenceability** | 5/5 (Excellent) | `ADR-output-path-resolution-001` is immediately clear. No memo needed. Prose citations are self-documenting. |
| **Collision Resistance** | 5/5 (Excellent) | Domain-based namespacing is resilient. Even with two projects discussing "routing", sequences stay separate (`ADR-routing-architecture-001` vs. `ADR-routing-architecture-002`). Sequential numbering within domain prevents collisions. |
| **Sortability** | 5/5 (Excellent) | Directory listing sorts by domain alphabetically: `ADR-agent-design-001`, `ADR-agent-design-002`, `ADR-enforcement-architecture-001`, `ADR-output-path-resolution-001`, `ADR-routing-architecture-001`, `ADR-tier-model-001`. Related decisions cluster naturally. |
| **Traceability** | 4/5 (Good) | Worktracker linkage moved to YAML frontmatter (`entity_id`, `project` fields) instead of filename. Still fully traceable, but requires reading the file to see context. |
| **Compatibility** | 4/5 (Good) | Nygard format unchanged. Identifiers are concise and readable. Frontmatter extension is minimal. Some tooling may expect entity ID in the name (one-time configuration update). |

**Trade-offs:**
- **Pros:** Solves all four findings (F-001 through F-004). Excellent discoverability and sortability. Self-documenting references. Scales cleanly to 100+ ADRs.
- **Cons:** Decouples ID from worktracker entity name (traceability requires frontmatter). Requires frontmatter convention for project/entity linkage. Existing ADR tooling may need updates.

**Verdict:** RECOMMENDED. Best overall usability across all six criteria. Superior to alternatives for domain-centric discovery. Traceability loss is minimal (frontmatter provides full context).

---

## Synthesis Judgments Summary

| Judgment | Confidence | Rationale |
|----------|-----------|-----------|
| **F-001 severity = 3** | High (95%) | Entity IDs are opaque to users unfamiliar with worktracker context. Semantic content is absent from the ID itself. Multiple references in `.context/rules/` files cite `ADR-EPIC002-001` without explanation, forcing readers to disambiguate or lookup. This is a major usability gap. |
| **F-003 severity = 3** | High (95%) | Nielsen H6 explicitly requires "recognition rather than recall." Users cannot recognize what `ADR-PROJ007-002` addresses without external lookup. This violates the heuristic directly. Comparison to semantic naming (`ADR-agent-design-002`) demonstrates the gap. |
| **Alternative 3 is superior** | High (90%) | Evaluated on six independent criteria. Alternative 3 scores 5/5 or 4/5 on all six; Alternatives 1-2 score 2-3 on discoverability and sortability. The domain-first pattern enables both discovery and reference, which is the core usability problem. Traceability via frontmatter is a minor design trade-off for significant usability gain. |
| **F-002 collision risk is real** | Medium (75%) | Current collision (EPIC002 in two projects) is an edge case but not a hypothetical. At 50+ ADRs, collisions become statistically inevitable under entity-ID-first naming. Domain-first naming (Alternative 3) eliminates collision risk entirely while preserving sequential numbering for disambiguation. |
| **Migration is feasible** | High (85%) | 6 existing ADRs can be migrated in one sprint (low effort). New ADRs adopt the domain-first convention immediately. No breaking changes required; old IDs can be maintained as aliases in `docs/design/README.md` during transition. |

---

## Handoff Data

For downstream sub-skills (e.g., orchestration, documentation):

| Finding ID | Heuristic | Severity | Candidate Action | Owner |
|-----------|-----------|----------|------------------|-------|
| F-001 | H2 | 3 | Adopt Alternative 3 naming; establish domain taxonomy | Framework governance |
| F-003 | H6 | 3 | Update ADR template to emphasize domain-first identification | Documentation lead |
| F-002 | H4 | 2 | Implement project + entity linkage in YAML frontmatter | ADR author template |
| F-004 | H7 | 2 | Update `docs/design/README.md` with domain index | Documentation lead |

---

## Heuristic Coverage Verification (S-010)

- [x] H1 (Visibility of system status) — Evaluated: N/A (non-interactive system)
- [x] H2 (Match between system and real world) — Evaluated: Finding F-001 (Severity 3)
- [x] H3 (User control and freedom) — Evaluated: PASS
- [x] H4 (Consistency and standards) — Evaluated: Finding F-002 (Severity 2)
- [x] H5 (Error prevention) — Evaluated: PASS
- [x] H6 (Recognition rather than recall) — Evaluated: Finding F-003 (Severity 3)
- [x] H7 (Flexibility and efficiency of use) — Evaluated: Finding F-004 (Severity 2)
- [x] H8 (Aesthetic and minimalist design) — Evaluated: PASS
- [x] H9 (Help users recognize, diagnose, recover from errors) — Evaluated: PASS
- [x] H10 (Help and documentation) — Evaluated: PASS

**Coverage:** All 10 heuristics evaluated on the ADR naming convention as a "system interface."

---

## Implementation Roadmap (Proposed)

### Phase 1: Immediate (This Sprint)
- [x] This evaluation (heuristic assessment complete)
- [ ] Publish Alternative 3 (Domain-First Semantic) as the recommended baseline
- [ ] Create ADR template with domain-first frontmatter specification
- [ ] Document domain taxonomy (e.g., agent-design, enforcement-architecture, output-path-resolution, tier-model, routing-architecture)

### Phase 2: Short-Term (1-2 Sprints)
- [ ] All new ADRs adopt Alternative 3 naming convention
- [ ] Optional: Migrate 6 existing ADRs to new names (low effort per ADR)
- [ ] Create `docs/design/README.md` with domain index and search guidance
- [ ] Update all cross-references in `.context/rules/` to use new ADR names (grep-and-replace when possible)

### Phase 3: Long-Term (1-2 Quarters)
- [ ] Establish aliases in `docs/design/README.md` mapping old names to new (backward compatibility during transition)
- [ ] Once all references are updated, retire old naming convention
- [ ] Consider adding ADR lookup script or index (automated discovery) for framework users

---

## References

| Source | Content |
|--------|---------|
| Nielsen Norman Group | H2-H10 definitions from "10 Usability Heuristics for User Interface Design" (1994, revised 2020) |
| Current ADRs | ADR-EPIC002-001, ADR-EPIC002-002, ADR-PROJ007-001, ADR-PROJ007-002, ADR-STORY015-001 in `docs/design/` |
| Rule files | `.context/rules/quality-enforcement.md`, `agent-development-standards.md`, `agent-routing-standards.md` (heavy ADR citations) |
| Nygard ADR Format | Baseline format for all Jerry ADRs; ADR title maps to filename slug |

---

**Evaluation Date:** 2026-04-13
**Evaluator:** ux-heuristic-evaluator
**Scope:** Single evaluation of naming convention usability
**Input Modality:** Screenshot-input degraded mode (no Figma MCP; analysis based on textual artifacts and usage patterns)
**Confidence:** High (95%) on F-001, F-003; Medium-High (75-85%) on F-002, F-004

---

## Degraded Mode Disclosure

[DEGRADED MODE] This evaluation was produced without Figma MCP access or interactive design tooling access. Input was provided via artifact analysis mode, examining existing ADR files, references in rule documentation, and text-based usage patterns. Some features are reduced:

- Cannot inspect metadata or interactive properties of ADR files
- Cannot simulate real-world browsing or search scenarios
- Analysis relies on static text examination and cross-reference counting

These limitations are unlikely to affect the validity of the findings (F-001 through F-004 are text-semantic issues, not interactive design issues) but should be noted for completeness per P-022.
