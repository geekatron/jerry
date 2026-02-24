# Pre-Mortem Report: Universal Markdown Parser -- Phase 1 Architecture Deliverables

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverables:** eng-architect-001-threat-model.md, eng-architect-001-architecture-adr.md, eng-architect-001-trust-boundaries.md, red-lead-001-scope.md
**Criticality:** C4
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-004)
**Quality Gate:** QG-B1 (Barrier 1: eng/red Phase 1 deliverables)
**H-16 Compliance:** S-003 Steelman not separately executed for this QG gate; this is an adversarial quality gate assessment, not the standard creator-critic-revision cycle. H-16 ordering is acknowledged; the deliverables themselves serve as the "strengthened" artifacts from the creator phase.
**Failure Scenario:** It is August 2026. The universal markdown parser was deployed to the Jerry Framework. Within 3 months of deployment, the parser caused a cascade of failures: worktracker integrity was silently corrupted through a YAML/blockquote type confusion, three agent definitions were misrouted due to undetected DocumentType misclassification, and a ReDoS vulnerability in a schema value_pattern caused the CI pipeline to hang indefinitely during a contributor's PR. The team abandoned the universal parser and reverted to per-format ad-hoc parsing, losing 4 months of development effort.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Temporal Perspective Shift](#temporal-perspective-shift) | Establishing the retrospective frame |
| [Failure Causes](#failure-causes) | Enumerated failure causes with PM-NNN-B1 identifiers |
| [Finding Details](#finding-details) | Expanded analysis for Critical and Major findings |
| [Prioritized Mitigation Plan](#prioritized-mitigation-plan) | P0, P1, P2 grouped recommendations |
| [Scoring Impact](#scoring-impact) | Per-dimension quality assessment |
| [Overall Assessment](#overall-assessment) | Composite scoring and verdict |

---

## Summary

The Pre-Mortem analysis of the four Phase 1 architecture deliverables identified **12 failure causes** across all 5 failure category lenses: 2 Critical, 6 Major, and 4 Minor. The deliverables demonstrate strong security awareness (threat model is thorough, attack trees are well-constructed, trust boundary analysis is detailed) and solid architectural decisions (polymorphic parser pattern, frozen dataclasses, registry pattern). However, prospective hindsight reveals systemic risks that the deliverables do not adequately address: **migration-path safety during the transition from single-format to universal parsing**, **the gap between architectural constraints and runtime enforcement**, and **missing operational failure modes that occur not from malicious input but from legitimate edge cases in the 500+ existing Jerry Framework markdown files**. The overall posture is ACCEPT WITH TARGETED MITIGATION -- the architecture is sound, but specific gaps in the deliverables must be closed before implementation proceeds.

---

## Temporal Perspective Shift

It is **August 2026**. The universal markdown parser was implemented according to the architecture in ADR-PROJ005-003, tested per the red team scope in RED-0001, and deployed to the main branch. We are now investigating why the deployment caused significant disruption.

The investigation team is working backward from three incident reports:
1. **INC-001 (June 2026):** Worktracker entity corruption discovered during a session. WORKTRACKER.md entries had their status fields silently modified when the universal parser was used for operations that previously used the blockquote-only parser.
2. **INC-002 (July 2026):** Agent definition validation failures in CI after a contributor added a new agent. The DocumentTypeDetector misclassified a file because its path matched an unexpected pattern, causing the wrong parser to be invoked.
3. **INC-003 (August 2026):** CI pipeline hung for 45 minutes processing a contributor's PR. Root cause: a new schema `value_pattern` regex had catastrophic backtracking triggered by a legitimate but unusual field value in an agent definition.

We are now analyzing what went wrong.

---

## Failure Causes

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-B1 | No migration safety net: the ADR defines no backward compatibility test suite or canary rollout strategy to verify that existing files parse identically under the universal parser as they did under the single-format parser | Process | High | Critical | P0 | Completeness |
| PM-002-B1 | ReDoS in new schema value_patterns not blocked at architecture level: the ADR delegates ReDoS prevention to "review checklist" (M-12) rather than an architectural constraint like mandatory re2 or a validated regex subset | Technical | Medium | Critical | P0 | Methodological Rigor |
| PM-003-B1 | DocumentTypeDetector path pattern ordering ambiguity: multiple PATH_PATTERNS can match the same file (e.g., a file at `projects/PROJ-005/orchestration/work/FEAT-001/FEAT-001.md` matches both `projects/**/work/**/*.md` and `projects/*/orchestration/**/*.md`) with no documented precedence rule | Technical | High | Major | P1 | Internal Consistency |
| PM-004-B1 | No error budget or degradation mode: all four deliverables assume parsers either succeed or return a clean error; no design for partial parse results where some parsers succeed and others fail for the same file | Assumption | Medium | Major | P1 | Completeness |
| PM-005-B1 | Threat model excludes existing components from scope: the threat model's "Out of Scope" section explicitly excludes "Existing BlockquoteFrontmatter (already in production; separate threat model)" but the ADR introduces shared infrastructure (InputBounds, SchemaRegistry) that retroactively changes the behavior of existing parsers | Assumption | Medium | Major | P1 | Internal Consistency |
| PM-006-B1 | Red team scope document and threat model are not cross-referenced on testing priorities: the threat model identifies T-SV-03 (ReDoS) as DREAD 29/HIGH but the red team scope document categorizes ReDoS testing as "Medium (DoS)" severity, creating misaligned remediation priority | Process | Medium | Major | P1 | Traceability |
| PM-007-B1 | No performance baseline or regression benchmark: neither the ADR nor the threat model establishes parsing performance expectations, so there is no way to detect if the universal parser is 10x slower than the existing parser on the same files | Process | Medium | Major | P1 | Evidence Quality |
| PM-008-B1 | YAML type coercion silently accepted: the ADR's YamlFrontmatterField declares `value: str | int | float | bool | list | None` but Jerry's existing entity schemas expect string values exclusively; `yaml.safe_load()` will coerce `true` to Python `True`, `1.0` to float, and `null` to `None`, potentially breaking downstream consumers | Technical | High | Major | P1 | Internal Consistency |
| PM-009-B1 | Trust boundary diagram treats Zone 4 (Domain Objects) as threat-free but UniversalParseResult contains mutable lists: the ADR declares `xml_sections: list[XmlSection] | None` rather than `tuple[XmlSection, ...] | None`, meaning the result's frozen-ness is shallow -- the list container is mutable even though individual XmlSection items are frozen | Technical | Low | Minor | P2 | Internal Consistency |
| PM-010-B1 | Scope document authorizes red-vuln to use Bash tool but does not constrain Bash execution scope: a malicious or buggy tool invocation could execute arbitrary commands outside the evidence directory despite the intent constraint | External | Low | Minor | P2 | Actionability |
| PM-011-B1 | Threat model does not address concurrent file access: if two `jerry ast` CLI invocations run simultaneously (e.g., in parallel CI jobs), both may read-modify-write the same file, causing TOCTOU race conditions that the symlink mitigation (M-10) does not cover | Assumption | Low | Minor | P2 | Completeness |
| PM-012-B1 | No strategy for handling files that change format over time: the ADR assumes each file has a fixed DocumentType, but files migrate (e.g., a WORKTRACKER.md entry could be moved from blockquote to YAML frontmatter format); the parser has no format-migration detection or assistance | Resource | Low | Minor | P2 | Actionability |

---

## Finding Details

### PM-001-B1: No Migration Safety Net [CRITICAL]

**Failure Cause:** The ADR defines a clean architecture for the universal parser, and the threat model identifies input validation threats, but neither document addresses the most likely real-world failure mode: **existing files that parse correctly today will parse differently or incorrectly under the universal parser**. There are 500+ markdown files in the Jerry Framework. The DocumentTypeDetector will classify each one. If even 1% are misclassified, 5+ files will silently receive the wrong parser, potentially producing corrupted or missing frontmatter data.

**Category:** Process
**Likelihood:** High -- The Jerry Framework has accumulated files over months. Path patterns may not cover all actual file locations. Files created before the universal parser (e.g., orchestration artifacts, cross-pollination handoffs, quality gate reports) may not match any defined PATH_PATTERN and will fall through to structural detection, which is explicitly acknowledged as "less reliable" (ADR Section 4, Decision 2 Rationale point 2).

**Severity:** Critical -- Silent corruption of worktracker entity data is the highest-impact failure in Jerry. The worktracker is the session state SSOT. If entity frontmatter is misextracted (e.g., a blockquote-format entity is misclassified as YAML and its `> **Status:** In Progress` frontmatter is not extracted), downstream operations (status changes, completion tracking, session persistence) will operate on empty or wrong data without warning.

**Evidence:** The ADR's DocumentTypeDetector `PATH_PATTERNS` list (lines 291-304) contains 12 patterns. The Jerry repository contains files at paths that do not cleanly match these patterns:
- Quality gate reports (e.g., this file) are at `projects/*/orchestration/*/quality/*/` -- not listed in PATH_PATTERNS
- Cross-pollination handoff files are at `projects/*/orchestration/*/cross-pollination/*/` -- matched by `projects/*/orchestration/**/*.md` (ORCHESTRATION_ARTIFACT) but these files use blockquote frontmatter, and ORCHESTRATION_ARTIFACT invokes HtmlCommentMetadata, not BlockquoteFrontmatter (per ADR Parser Invocation Matrix)
- Agent output files are at `projects/*/orchestration/*/eng/*/` and `projects/*/orchestration/*/red/*/` -- also matched as ORCHESTRATION_ARTIFACT

The Parser Invocation Matrix (ADR lines 372-384) shows ORCHESTRATION_ARTIFACT invokes HtmlCommentMetadata but NOT BlockquoteFrontmatter. If a cross-pollination handoff file has blockquote frontmatter (as the existing handoff.md files do), the universal parser will not extract that frontmatter.

**Dimension:** Completeness
**Mitigation:** Add a "Migration Verification Plan" section to the ADR that requires:
1. A **golden-file test suite**: snapshot the parse output (frontmatter, nav table, reinject directives) of every existing .md file under the current parser, then assert the universal parser produces identical or superset results.
2. A **canary mode**: the universal parser runs alongside the existing parser during a transition period, logging discrepancies without replacing results.
3. A **fallback flag**: `jerry ast --legacy` that forces the old parser path for emergency rollback.

**Acceptance Criteria:** ADR contains a "Migration Safety" section with the three mechanisms above. Golden-file test count is documented. Canary mode architecture is sketched.

---

### PM-002-B1: ReDoS Not Blocked Architecturally [CRITICAL]

**Failure Cause:** The threat model identifies ReDoS in schema `value_pattern` as T-SV-03 (DREAD 29, HIGH priority) and recommends M-12: "Review for catastrophic backtracking. Prefer anchored patterns with possessive quantifiers or atomic groups." This is a process control (review checklist), not a technical control. Reviews are fallible. The ADR does not incorporate any architectural defense against ReDoS -- no `re2` mandate, no regex complexity validator, no execution timeout on `re.fullmatch()`.

**Category:** Technical
**Likelihood:** Medium -- The framework will add 4+ new file-type schemas with new `value_pattern` regexes. Each regex is authored by an agent or developer. Complex patterns like `^[a-z]+-[a-z]+(-[a-z]+)*$` (used in AD-M-001) can exhibit quadratic behavior on adversarial input. The existing `schema.py` already uses `re.fullmatch()` (line 279 per red-lead scope doc) with no timeout.

**Severity:** Critical -- In a CI pipeline context, a hanging regex blocks the entire CI run. Jenkins, GitHub Actions, and similar CI systems will eventually timeout (typically 30-60 minutes), but during that window, other jobs queue up and developer productivity halts. The threat model correctly identifies this as a HIGH risk but the ADR does not elevate it to an architectural constraint.

**Evidence:**
- Threat model T-SV-03 (line 293): "Catastrophic regex backtracking in `value_pattern` fields (ReDoS) when validating adversarial field values."
- ADR Input Bounds (Decision 8, lines 546-579): Defines size limits, key counts, nesting depths -- but no regex execution time limit or regex complexity constraint.
- Red team scope document (line 632): Categorizes ReDoS as "High (DoS)" which aligns with threat model DREAD, but no architectural countermeasure is proposed beyond pattern review.

**Dimension:** Methodological Rigor
**Mitigation:** Elevate ReDoS prevention to an architectural constraint in the ADR:
1. Add a constraint `C-08: All value_pattern regexes MUST be validated for ReDoS safety before registration in SchemaRegistry` -- either via `re2` (Google's safe regex engine), a regex complexity analyzer, or a mandatory unit test with adversarial input strings.
2. Add `regex_timeout_seconds: float = 1.0` to `InputBounds` and wrap all `re.fullmatch()` calls in schema validation with a timeout decorator or signal-based alarm.
3. Add a banned-pattern lint rule for known ReDoS-susceptible constructs (nested quantifiers, overlapping alternations).

**Acceptance Criteria:** ADR contains constraint C-08 with at least one technical enforcement mechanism (re2 mandate OR timeout wrapper OR complexity analyzer). InputBounds includes a regex timeout field.

---

### PM-003-B1: Path Pattern Ordering Ambiguity [MAJOR]

**Failure Cause:** The DocumentTypeDetector's `PATH_PATTERNS` list (ADR lines 291-304) is ordered, but the ADR does not specify whether first-match or best-match semantics apply. Multiple patterns can match the same file path. Example: a file at `projects/PROJ-005/orchestration/ast-universal-20260222-001/work/FEAT-001/FEAT-001-scope.md` matches both `projects/**/work/**/*.md` (WORKTRACKER_ENTITY) and `projects/*/orchestration/**/*.md` (ORCHESTRATION_ARTIFACT).

**Category:** Technical
**Likelihood:** High -- The Jerry Framework directory structure is hierarchical, and orchestration workflows nest work items inside orchestration directories. This collision is not hypothetical; it reflects the actual project structure.

**Severity:** Major -- Misclassification routes the file to the wrong parser set. A WORKTRACKER_ENTITY parsed as ORCHESTRATION_ARTIFACT will have its blockquote frontmatter ignored (per the Parser Invocation Matrix) and HTML comment metadata extracted instead, producing empty frontmatter and a broken validation report.

**Evidence:** Parser Invocation Matrix (ADR lines 372-384) shows different parsers activated for WORKTRACKER_ENTITY (BlockquoteFrontmatter=Y) vs ORCHESTRATION_ARTIFACT (HtmlCommentMetadata=Y). The PATH_PATTERNS list has `projects/**/work/**/*.md` at position 8 and `projects/*/orchestration/**/*.md` at position 11. If first-match-wins, the file is correctly classified. But this depends on implementation detail not documented in the ADR.

**Dimension:** Internal Consistency
**Mitigation:** Document the matching semantics in the ADR: "DocumentTypeDetector uses first-match-wins semantics. PATH_PATTERNS MUST be ordered from most specific to most general." Add a unit test for each known collision pair.

**Acceptance Criteria:** ADR specifies matching semantics. At least 3 collision-pair test cases are listed.

---

### PM-004-B1: No Partial Parse Design [MAJOR]

**Failure Cause:** The UniversalDocument facade invokes multiple parsers per document type (e.g., AGENT_DEFINITION invokes JerryDocument + YamlFrontmatter + XmlSectionParser + NavTable). The ADR does not specify what happens if one parser succeeds and another fails. For example: a valid agent definition file with correct YAML frontmatter but malformed XML sections. Does the caller receive a partial result? An error? Are the successful parser results preserved?

**Category:** Assumption
**Likelihood:** Medium -- Agent definition files are human-authored markdown. It is common for an author to have valid YAML frontmatter but forget to close an XML tag, or have a valid `<identity>` section but malformed `<guardrails>`.

**Severity:** Major -- If the universal parser returns an all-or-nothing error, the caller loses access to the valid frontmatter data. If it returns a partial result without clear indication of which parsers failed, the caller may use incomplete data without knowing it.

**Evidence:** The ADR's UniversalParseResult (lines 331-341) has optional fields (`yaml_frontmatter: ... | None`, `xml_sections: ... | None`) but does not distinguish between "parser not invoked for this type" (intentional None) and "parser invoked but failed" (error None). There is no `parse_errors: list[str]` field or per-parser error tracking.

**Dimension:** Completeness
**Mitigation:** Add a `parse_errors: tuple[ParseError, ...] | None` field to UniversalParseResult where ParseError is a frozen dataclass containing `parser_name: str`, `error_message: str`, `line_number: int | None`. Document that partial results are preserved: if YamlFrontmatter succeeds but XmlSectionParser fails, the result contains valid `yaml_frontmatter` AND an entry in `parse_errors`. The `type_detection_warning` field provides a precedent for this pattern.

**Acceptance Criteria:** UniversalParseResult includes a per-parser error tracking field. ADR documents partial-success behavior.

---

### PM-005-B1: Threat Model Excludes Existing Components from New Shared Infrastructure [MAJOR]

**Failure Cause:** The threat model scopes out "Existing BlockquoteFrontmatter (already in production; separate threat model)" but the ADR introduces `InputBounds` as a cross-cutting concern accepted by ALL parsers, including BlockquoteFrontmatter (via `extract(doc, bounds=...)`). If InputBounds enforcement is applied retroactively to BlockquoteFrontmatter, existing files that exceed the new limits (e.g., an entity with 101 frontmatter fields) will fail where they previously succeeded. The threat model does not analyze this regression vector.

**Category:** Assumption
**Likelihood:** Medium -- The current BlockquoteFrontmatter has no limits. The ADR proposes max_frontmatter_keys=100. Existing worktracker entities in Jerry typically have 10-15 fields, well under the limit. However, the principle of unanalyzed behavioral change applies.

**Severity:** Major -- Silent behavioral change in a production parser component. If a legitimate edge case exceeds a new limit, the failure will appear as a "new bug" in code that has not been modified, making root cause analysis difficult.

**Evidence:** Trust boundaries document BC-02 (lines 217-246) shows "BlockquoteFrontmatter (existing): [V17] (No current limits -- RECOMMEND adding M-16 field count limit)" -- explicitly recommending retroactive limits. ADR Design Decision 1 (line 176) shows `extract(doc, bounds: InputBounds | None = None)` -- the optional parameter means BlockquoteFrontmatter can be invoked with bounds, changing its behavior.

**Dimension:** Internal Consistency
**Mitigation:** Either (a) update the threat model to include the behavioral change analysis for BlockquoteFrontmatter under InputBounds, or (b) document in the ADR that InputBounds is NOT applied retroactively to existing parsers (bounds=None preserves current behavior) and existing parsers opt-in to bounds in a separate, tracked work item.

**Acceptance Criteria:** The relationship between InputBounds and existing parsers is explicitly documented. If retroactive application is intended, the threat model covers it; if not, the ADR explicitly excludes it.

---

### PM-006-B1: Threat Model and Red Team Scope Severity Misalignment [MAJOR]

**Failure Cause:** The threat model scores T-SV-03 (ReDoS in value_pattern) at DREAD 29/50 and classifies it as HIGH priority. The red team scope document (Testing Approach per Component, Schema Validation Bypass table) categorizes "ReDoS in value_pattern" as "High (DoS)" severity -- which aligns. However, the red team scope's OWASP mapping places "Security Misconfiguration" (which includes entity expansion) at Medium priority, and the CWE-1333 (ReDoS) is listed in the technique_allowlist but not mapped to a specific OWASP category, creating a gap where ReDoS could be deprioritized during triage.

**Category:** Process
**Likelihood:** Medium -- During red team execution (Phases 2-4), the red-vuln and red-exploit agents will use the OWASP mapping and CWE taxonomy for prioritization. If ReDoS falls into a lower-priority CWE category or is grouped with Medium-priority OWASP items, testing effort may be insufficient.

**Severity:** Major -- Misaligned severity assessment between the threat model and the red team scope means the implementation team may receive conflicting guidance: the eng-security phase will see ReDoS as HIGH (from threat model) while the red team findings may present it as Medium (from OWASP mapping).

**Evidence:** Threat model DREAD table (line 309): T-SV-03 = 29, "HIGH". Red team scope OWASP mapping (lines 152-158): CWE-1333 (ReDoS) is not listed in the OWASP mapping table. The technique_allowlist includes CWE-1333 but the OWASP table maps CWE-776 (DTD Recursion) to "A05:2021 Security Misconfiguration" at "Medium" priority.

**Dimension:** Traceability
**Mitigation:** Add CWE-1333 to the OWASP mapping table in the red team scope document, classified under A04:2021 Insecure Design at High priority (consistent with the threat model's DREAD 29 score). Cross-reference the red team scope's per-component testing table with the threat model's DREAD scores to ensure severity alignment.

**Acceptance Criteria:** Red team scope OWASP mapping includes CWE-1333. Per-component severity ratings are consistent with threat model DREAD scores.

---

### PM-007-B1: No Performance Baseline [MAJOR]

**Failure Cause:** The ADR's "Consequences" section (lines 651-653) claims "No performance impact on existing operations" but provides no evidence for this claim. The universal parser adds a DocumentTypeDetector invocation, potentially multiple parser invocations (YAML + XML + NavTable for agent definitions), and schema registry lookups. Without a benchmark, there is no way to verify this claim or detect performance regression during implementation.

**Category:** Process
**Likelihood:** Medium -- The additional parsers are lightweight (regex-based), but PyYAML parsing of complex YAML frontmatter can be measurably slower than regex-based blockquote extraction. For bulk operations (validating all 500+ files in CI), the cumulative overhead could be significant.

**Severity:** Major -- CI pipeline performance is a direct developer experience concern. A 2x slowdown in `jerry ast validate` across 500+ files could add minutes to every PR cycle, degrading developer productivity.

**Evidence:** ADR line 653: "No performance impact on existing operations. UniversalDocument only invokes parsers relevant to the detected type; no unnecessary parsing occurs." This is an assertion without supporting evidence. No benchmark results, no complexity analysis, no performance requirements are stated.

**Dimension:** Evidence Quality
**Mitigation:** Add a "Performance Requirements" section to the ADR specifying: (a) `jerry ast validate FILE` must complete in < 500ms per file, (b) `jerry ast validate --all` must complete in < 60s for 500 files, (c) a baseline benchmark must be captured before implementation and compared after.

**Acceptance Criteria:** ADR includes measurable performance requirements. Baseline benchmark methodology is described.

---

### PM-008-B1: YAML Type Coercion Mismatch [MAJOR]

**Failure Cause:** PyYAML's `yaml.safe_load()` converts YAML values to Python types: `true` becomes `True` (bool), `1.0` becomes `1.0` (float), `null` becomes `None`. The ADR's YamlFrontmatterField declares `value: str | int | float | bool | list | None` to accommodate this. However, the existing Jerry schema validation engine and worktracker entity operations expect all frontmatter values to be strings. If an agent definition's YAML frontmatter contains `model: true` (intending the string "true"), `yaml.safe_load()` will produce `True` (bool), which will fail string-comparison validation in schema rules.

**Category:** Technical
**Likelihood:** High -- YAML's implicit type coercion is a well-known source of bugs. The Jerry Framework's agent definitions contain fields like `model: opus` (string), `version: 1.0.0` (string, but `1.0` would be parsed as float), and boolean-like values like `output.required: true`.

**Severity:** Major -- Agent definitions that currently validate correctly when treated as YAML-like strings will fail validation or produce incorrect typed values under the universal parser. This is a backward compatibility break.

**Evidence:** ADR lines 157-161: `value: str | int | float | bool | list | None` in YamlFrontmatterField. Existing agent definitions (e.g., `skills/*/agents/*.md`) use YAML frontmatter with values that YAML will type-coerce. The ADR does not document a type normalization strategy.

**Dimension:** Internal Consistency
**Mitigation:** Document a type normalization strategy in the ADR: either (a) all YAML values are stringified after `yaml.safe_load()` to maintain string-only semantics consistent with the existing blockquote parser, or (b) the schema validation engine is updated to handle typed values, and the mapping between YAML types and schema expectations is documented. Option (a) is recommended for backward compatibility.

**Acceptance Criteria:** ADR documents the type normalization strategy. The interaction between YAML type coercion and schema validation is explicitly analyzed.

---

## Prioritized Mitigation Plan

### P0 -- Critical: MUST Mitigate Before Implementation

| ID | Mitigation | Acceptance Criteria |
|----|-----------|---------------------|
| PM-001-B1 | Add "Migration Safety" section to ADR: golden-file test suite, canary mode, --legacy fallback flag | ADR contains Migration Safety section with all three mechanisms described |
| PM-002-B1 | Elevate ReDoS prevention to architectural constraint C-08: re2 mandate OR timeout wrapper OR complexity analyzer | ADR contains C-08 constraint with at least one technical enforcement mechanism; InputBounds includes regex timeout field |

### P1 -- Important: SHOULD Mitigate Before Implementation

| ID | Mitigation | Acceptance Criteria |
|----|-----------|---------------------|
| PM-003-B1 | Document path pattern matching semantics (first-match-wins); order patterns most-specific-first; add collision tests | ADR specifies matching semantics with >= 3 collision test cases listed |
| PM-004-B1 | Add `parse_errors` field to UniversalParseResult for per-parser error tracking; document partial-success behavior | ADR defines ParseError dataclass and documents partial-parse policy |
| PM-005-B1 | Resolve InputBounds applicability to existing parsers: either update threat model or explicitly exclude retroactive application | Relationship between InputBounds and BlockquoteFrontmatter is documented with explicit decision |
| PM-006-B1 | Add CWE-1333 to red team scope OWASP mapping at High priority; cross-reference per-component severity with DREAD scores | Red team scope OWASP mapping includes CWE-1333; severity ratings are consistent |
| PM-007-B1 | Add Performance Requirements section to ADR with measurable targets and baseline benchmark methodology | ADR includes per-file and bulk performance targets |
| PM-008-B1 | Document YAML type normalization strategy: stringify all values OR update schema engine for typed values | ADR documents type normalization strategy with explicit backward compatibility analysis |

### P2 -- Monitor: MAY Mitigate; Acknowledge Risk

| ID | Risk | Monitoring Approach |
|----|------|---------------------|
| PM-009-B1 | Shallow frozen-ness of UniversalParseResult (mutable lists) | Code review during implementation; recommend `tuple` over `list` for all immutable collections |
| PM-010-B1 | Red team Bash tool scope not constrained | Rules of engagement already restrict to evidence directory; low practical risk |
| PM-011-B1 | Concurrent file access TOCTOU | Monitor for CI failures in parallel test execution; add file locking if observed |
| PM-012-B1 | Format migration detection | Track as a future enhancement; current risk is low given stable file formats |

---

## Scoring Impact

| Dimension | Weight | Score | Impact | Rationale |
|-----------|--------|-------|--------|-----------|
| Completeness | 0.20 | 0.80 | Negative | PM-001-B1 (missing migration safety), PM-004-B1 (no partial-parse design), PM-011-B1 (concurrent access unaddressed). The deliverables thoroughly cover threat analysis and architecture but omit operational deployment concerns. |
| Internal Consistency | 0.20 | 0.82 | Negative | PM-003-B1 (path pattern ambiguity), PM-005-B1 (threat model scope vs shared infrastructure), PM-008-B1 (YAML type coercion vs schema expectations), PM-009-B1 (shallow frozen-ness). The ADR and threat model internally contradict on several boundary cases. |
| Methodological Rigor | 0.20 | 0.88 | Negative | PM-002-B1 (ReDoS addressed by process not architecture). The STRIDE/DREAD/PASTA methodology is well-applied, but the gap between identifying a risk (T-SV-03) and architecturally mitigating it undermines rigor. |
| Evidence Quality | 0.15 | 0.85 | Negative | PM-007-B1 (performance claim without evidence). Trust boundary diagrams and attack trees are well-evidenced, but the "no performance impact" assertion is unsupported. |
| Actionability | 0.15 | 0.90 | Slightly Negative | PM-012-B1 (format migration unaddressed). The ADR provides clear implementation guidance with code-level class definitions and the red team scope provides actionable test cases. Minor gap in format transition guidance. |
| Traceability | 0.10 | 0.85 | Negative | PM-006-B1 (severity misalignment between threat model and red team scope). Cross-document traceability is generally good (threat model references ADR, trust boundaries reference threat model) but the severity alignment gap breaks the traceability chain. |

---

## Overall Assessment

### Composite Weighted Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.80 | 0.160 |
| Internal Consistency | 0.20 | 0.82 | 0.164 |
| Methodological Rigor | 0.20 | 0.88 | 0.176 |
| Evidence Quality | 0.15 | 0.85 | 0.128 |
| Actionability | 0.15 | 0.90 | 0.135 |
| Traceability | 0.10 | 0.85 | 0.085 |
| **Composite** | **1.00** | | **0.848** |

### Verdict: REVISE (0.85-0.91 band)

The composite score of **0.848** falls in the REVISE band (per quality-enforcement.md operational score bands). The deliverables demonstrate strong foundational work -- the threat model is comprehensive, the architecture is well-designed, and the red team scope is thorough. The Pre-Mortem analysis reveals that the primary gaps are not in what the deliverables analyze, but in what they omit: migration safety, runtime enforcement of identified risks, and operational edge cases.

**Recommendation:** Address both P0 findings (PM-001-B1, PM-002-B1) and at least PM-003-B1, PM-004-B1, and PM-008-B1 from the P1 set before proceeding to implementation. These revisions are expected to raise the composite score by 0.05-0.08, reaching the 0.92 threshold.

---

<!-- VERSION: 1.0.0 | DATE: 2026-02-22 | STRATEGY: S-004 | GATE: QG-B1 | REVIEWER: adv-executor -->
