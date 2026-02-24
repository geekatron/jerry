# Steelman Report: Phase 1 Architecture Deliverables -- Universal Markdown Parser

## Steelman Context

- **Deliverables:**
  1. `eng-architect-001-threat-model.md` (634 lines)
  2. `eng-architect-001-architecture-adr.md` (725 lines)
  3. `eng-architect-001-trust-boundaries.md` (568 lines)
  4. `red-lead-001-scope.md` (691 lines)
- **Deliverable Types:** Threat Model, ADR, Trust Boundary Analysis, Security Testing Scope
- **Criticality Level:** C4
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (S-003) | **Date:** 2026-02-22 | **Original Authors:** eng-architect, red-lead

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Assessment overview and improvement counts |
| [Steelman Analysis: Threat Model](#steelman-analysis-threat-model) | Strongest interpretation of threat model decisions |
| [Steelman Analysis: Architecture ADR](#steelman-analysis-architecture-adr) | Strongest interpretation of architecture decisions |
| [Steelman Analysis: Trust Boundaries](#steelman-analysis-trust-boundaries) | Strongest interpretation of trust boundary analysis |
| [Steelman Analysis: Red Team Scope](#steelman-analysis-red-team-scope) | Strongest interpretation of security testing scope |
| [Cross-Deliverable Coherence](#cross-deliverable-coherence) | How the four deliverables reinforce each other |
| [Improvement Findings Table](#improvement-findings-table) | All SM-NNN findings with severity and dimension |
| [Improvement Details](#improvement-details) | Expanded descriptions for Critical and Major findings |
| [Per-Dimension Scoring](#per-dimension-scoring) | Scores with justification |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |
| [Best Case Scenario](#best-case-scenario) | Conditions under which this deliverable set is strongest |

---

## Summary

**Steelman Assessment:** This is an exceptionally strong Phase 1 architecture deliverable set. The four documents form a mutually reinforcing security-first architecture that demonstrates rare coherence between threat modeling, architectural decision-making, trust boundary analysis, and offensive testing scope definition. The deliverables show mature understanding of defense-in-depth principles and demonstrate that security was treated as an architectural constraint rather than an afterthought.

**Improvement Count:** 0 Critical, 3 Major, 8 Minor

**Original Strength:** Very High. The deliverables already meet the quality bar for C4 work. The threat model is comprehensive (29 threats, 5 STRIDE components, DREAD scoring, 3 attack trees, PASTA stages 4-7, NIST CSF 2.0 mapping). The ADR makes 8 well-justified design decisions with explicit hexagonal architecture compliance verification. The trust boundaries document provides a complete 6-zone ASCII diagram with per-boundary validation checks. The red team scope follows PTES methodology with CWE mapping and per-component test matrices.

**Recommendation:** Incorporate 3 Major improvements to strengthen already-strong deliverables before critique strategies proceed. The 8 Minor improvements are polish that would elevate from strong to exceptional.

---

## Steelman Analysis: Threat Model

### Design Decision: Multi-Methodology Threat Modeling (STRIDE + DREAD + Attack Trees + PASTA)

**Strongest interpretation:** The threat model uses four complementary methodologies rather than relying on a single approach. This is not over-engineering; it is the appropriate level of rigor for a C4-critical parser that processes untrusted content feeding directly into the framework's governance enforcement layer. Each methodology covers a distinct analytical concern:

- **STRIDE** provides systematic per-component threat identification, ensuring no threat category is overlooked. The 29 identified threats across 5 components demonstrate thorough coverage.
- **DREAD** provides quantitative risk scoring that enables rational prioritization. Without DREAD, all threats would receive equal attention, wasting effort on low-risk items while potentially under-resourcing critical ones.
- **Attack trees** provide causal chain analysis for the 3 highest-risk threats, revealing that the YAML deserialization threat (T-YF-07, DREAD 38) depends on a single control point (`yaml.safe_load()`), which directly motivates the defense-in-depth mitigations M-01 (lint rule) and M-04 (integration test).
- **PASTA stages 4-7** connect threats to realistic threat agents (malicious contributor, compromised dependency, accidental misuse, automated scanner), grounding the analysis in operational reality rather than abstract possibility.

**Why alternatives would be weaker:** A STRIDE-only analysis would identify threats but not prioritize them. A DREAD-only analysis would score threats without the systematic identification that STRIDE provides. Attack trees alone would be too narrow. PASTA alone would lack the per-component granularity of STRIDE. The combination ensures both breadth (STRIDE) and depth (attack trees, PASTA) with prioritization (DREAD).

**Hidden strength:** The DREAD scores are calibrated to the Jerry Framework's operational context (developer CLI tool, no network exposure) rather than inflated to a worst-case scenario. This honest calibration (per P-022) means the scores are actionable -- the "CRITICAL" and "HIGH" labels genuinely represent the threats most worth mitigating first. The disclaimer section (lines 624-631) explicitly notes that network-exposed deployment would increase scores, demonstrating intellectual honesty about scope limitations.

### Design Decision: 19 Mitigations with Priority Classification

**Strongest interpretation:** The mitigation catalog (M-01 through M-19) is organized by priority (CRITICAL, HIGH, MEDIUM, LOW) and each mitigation references the specific threats it addresses. This is not a generic checklist; it is a traceable set of specific countermeasures derived from the STRIDE/DREAD analysis. The 3 CRITICAL mitigations (M-01 banned API lint rule, M-04 integration test, M-11 no XML parser) address the 3 threats with DREAD scores >= 33.

**Why alternatives would be weaker:** Generic security guidelines ("validate all input") would lack specificity. A flat list without priority would not support resource allocation. Mitigations without threat traceability would be unjustified assertions.

**Hidden strength:** The mitigation recommendations include concrete implementation guidance (line-level code snippets, specific ruff rule suggestions, exact size limits). This converts security analysis from advisory to actionable -- an implementer can build directly from M-01 through M-19 without interpreting vague recommendations. [SM-001-B1]

### Design Decision: NIST CSF 2.0 Mapping

**Strongest interpretation:** Mapping mitigations to NIST CSF 2.0 functions provides governance alignment that connects the technical threat model to enterprise security frameworks. This is particularly valuable because it demonstrates that the parser security is not ad-hoc but fits within a recognized framework, which strengthens the case for institutional investment in the mitigations.

**Hidden strength:** The coverage summary (lines 590-597) honestly acknowledges that RESPOND and RECOVER functions are covered by existing mechanisms (Jerry incident response and git version control, respectively) rather than claiming new coverage. This shows mature understanding that not every framework function needs new implementation.

---

## Steelman Analysis: Architecture ADR

### Design Decision 1: Polymorphic Parser Pattern

**Strongest interpretation:** The choice to implement separate parser classes (YamlFrontmatter, XmlSectionParser, HtmlCommentMetadata) rather than a monolithic parser is the correct application of the Single Responsibility Principle to a security-critical domain. Each parser handles exactly one format, which provides three distinct advantages:

1. **Security isolation:** A vulnerability in YamlFrontmatter cannot propagate to XmlSectionParser. This is explicitly stated in the threat model's strategic implications (line 604): "a vulnerability in YamlFrontmatter does not affect XmlSectionParser." The blast radius of each parser is bounded by its format.

2. **Testability:** Each parser can be fuzzed and tested independently with format-specific adversarial inputs. The red team scope document confirms this with per-component test matrices (YamlFrontmatter: 7 test categories, XmlSectionParser: 7, HtmlCommentMetadata: 7, DocumentTypeDetector: 8).

3. **Existing precedent:** The current codebase already follows this pattern (BlockquoteFrontmatter, ReinjectDirective, NavEntry as separate domain classes). The new parsers are architecturally consistent with the existing design, reducing cognitive load and maintenance risk.

**Why alternatives would be weaker:** A single parser class (Alternative 1 in the ADR) would create a God class with mixed security profiles. Extending JerryDocument directly (Alternative 3) would violate H-10 (one class per file) and bloat the base parser. A plugin system (Alternative 5) would add dynamic loading complexity disproportionate to 10 file types.

**Hidden strength:** The `UniversalParseResult` frozen dataclass (lines 331-341) uses `| None` for optional parser results rather than empty collections. This makes the API self-documenting: `yaml_frontmatter: YamlFrontmatterResult | None` communicates that the YAML parser was not invoked (None) versus invoked and found nothing (empty fields). This prevents downstream consumers from confusing "not parsed" with "parsed and empty." [SM-002-B1]

### Design Decision 2: Path-First, Structure-Fallback Type Detection

**Strongest interpretation:** Prioritizing path-based detection over content-based detection is the correct security choice because path patterns are deterministic and immune to content manipulation. A malicious contributor who controls file content cannot spoof the detected type via content crafting if the file is in a known path. Structure-based detection is relegated to fallback status, used only when path matching fails, which appropriately limits the attack surface of content-based analysis.

The `UNKNOWN` default type is the fail-safe behavior -- unclassifiable files receive the most conservative parsing (markdown-only, no metadata extraction), which is the principle of least privilege applied to type detection.

**Why alternatives would be weaker:** Content-only detection (no path awareness) would be fully susceptible to content spoofing (T-DT-01). Path-only detection (no structure fallback) would fail on files outside standard directories. The path-first + structure-fallback combination provides deterministic security with graceful degradation.

**Hidden strength:** The dual-signal validation (M-14) that warns when path and structure signals disagree is a sophisticated defense-in-depth measure that existing CLI tools rarely implement. It transforms a silent miscategorization into a visible warning, enabling early detection of suspicious files.

### Design Decision 6: Regex-Only XML Section Parsing

**Strongest interpretation:** The explicit architectural prohibition against XML parser libraries (`xml.etree.ElementTree`, `lxml`, `xml.sax`) is the single strongest security decision in the entire deliverable set. This decision eliminates the XXE attack surface entirely by architecture rather than by configuration. The rationale is compelling:

- Jerry's XML-like tags are not real XML (no namespaces, no attributes, no entities, no DTDs). Using a full XML parser would import an entire class of vulnerabilities (XXE, entity expansion, DTD processing) for zero functional benefit.
- Even `defusedxml` (which mitigates XXE) would add a dependency with ongoing security maintenance burden for functionality that regex handles trivially.
- The regex pattern (lines 490-495) is well-constructed: `re.MULTILINE | re.DOTALL`, non-greedy content capture (`.*?`), named groups, and tag name back-reference (`(?P=tag)`).

**Hidden strength:** The tag validation rules (lines 507-514) form a complete set of defensive checks: whitelist-only tags, nested-tag rejection, unclosed-tag error handling, line-boundary anchoring, content trimming, and size limits. This is a textbook application of input validation constraints to a parsing operation.

### Design Decision 8: InputBounds Configuration Class

**Strongest interpretation:** Centralizing all resource limits in a single frozen dataclass (`InputBounds`) is architecturally superior to scattering magic numbers across parser implementations. The design provides:

1. **Auditability:** All limits are visible in one location (lines 556-571), making security review efficient.
2. **Testability:** Callers can inject custom `InputBounds` for testing boundary conditions without modifying parser code.
3. **Security-by-default:** `InputBounds.DEFAULT` provides conservative limits; relaxation requires explicit construction of a custom instance, making unsafe configurations self-documenting.
4. **Immutability:** The frozen dataclass prevents runtime tampering with limits.
5. **Traceability:** Each default value references its threat model mitigation (M-05, M-06, M-07, M-16, M-17).

**Why alternatives would be weaker:** Hardcoded constants scattered across parsers would be difficult to audit. Configuration files (YAML/JSON) would introduce another parsing surface. Environment variables would be invisible during code review.

---

## Steelman Analysis: Trust Boundaries

### Design Decision: Six-Zone Trust Architecture

**Strongest interpretation:** The six trust zones (Z1-Z6) with five boundary crossings (BC-01 through BC-05) provide a comprehensive mapping of how untrusted input flows through the parser to become trusted domain objects. The zone classification is well-calibrated:

- **Z1 (CLI Input) and Z2 (File Content) are correctly classified as "Untrusted."** Both accept data from external sources (user CLI arguments, file content) and should be treated as potentially hostile.
- **Z3 (Parser Layer) is correctly classified as "Semi-trusted."** Parsers are the components that transform untrusted input into trusted objects; they are trusted code processing untrusted data, which is the correct characterization.
- **Z4 (Domain Objects) is correctly classified as "Trusted."** Frozen dataclass construction is enforced by the Python runtime; once an object is constructed, its immutability is a language-level guarantee, not a convention.
- **Z5 (Schema Validation) is correctly classified as "Trusted."** Schema rules are defined by the framework maintainers, not by external input.
- **Z6 (File System Output) is correctly classified as "Semi-trusted."** The output path re-verifies path containment (M-08), correctly treating the write-back path as a potential attack vector even though the read path was already validated (TOCTOU awareness).

**Hidden strength:** The trust boundary diagram includes the TOCTOU (Time-of-Check-Time-of-Use) concern at the write-back path (lines 465-466): "Even though read was from the same path, re-verify in case of symlink race condition." This demonstrates awareness of a subtle security issue that many threat models miss.

### Design Decision: Three-Checkpoint Defense-in-Depth

**Strongest interpretation:** The strategic implications section (lines 539-549) articulates a defense-in-depth architecture with three checkpoints:

1. **Checkpoint 1 (BC-02): Input bounds** -- the cheapest and most effective layer. Rejecting oversized or malformed input before parsing begins is a near-zero-cost operation that prevents entire categories of DoS attacks.
2. **Checkpoint 2 (BC-03): Frozen dataclass construction** -- language-level immutability enforcement. This is defense-in-depth against parser bugs that might produce inconsistent state.
3. **Checkpoint 3 (BC-04): Schema validation** -- semantic checking that catches valid-structure-but-wrong-value errors.

The key observation that "Zone 3 is the Attack Surface" (line 547) is analytically correct: all DREAD >= 28 threats target the parser layer because parsers are the components that bridge the trust boundary between untrusted input and trusted objects. This insight directly motivates the testing prioritization recommendation (lines 551-557).

**Why alternatives would be weaker:** A single validation layer (e.g., schema validation only) would miss format-specific attacks. Two layers (input bounds + schema) would miss the immutability guarantee. The three-checkpoint architecture ensures that even if one layer is bypassed, the other two provide independent protection.

### Design Decision: Per-Boundary Validation Checklists

**Strongest interpretation:** Each boundary crossing has a numbered validation checklist (V1-V30) that specifies exactly what checks occur at that boundary. This is not merely documentation -- it is a verification contract that can be tested. Each `[Vn]` entry maps to a specific mitigation from the threat model, creating a traceable chain from threat to mitigation to validation checkpoint. [SM-003-B1]

**Hidden strength:** The validation checklist for BC-02 (lines 224-246) includes a note about existing components lacking bounds checking: "V17: (No current limits -- RECOMMEND adding M-16 field count limit)" and "V18: (No current limits -- RECOMMEND adding M-16 directive count limit)." This honest acknowledgment of gaps in the existing implementation (not just the new components) demonstrates thorough analysis and prevents the common blind spot of assuming that existing code is already secure.

---

## Steelman Analysis: Red Team Scope

### Design Decision: PTES + OSSTMM Methodology Selection

**Strongest interpretation:** The selection of PTES for engagement structure and OSSTMM Section III for control-based testing is well-justified and the "Why NOT Other Methodologies" section (lines 519-524) demonstrates that alternatives were considered and rejected for specific reasons:

- OWASP Testing Guide v4 was rejected because it is web-application focused, and the system under test is a CLI tool and Python library.
- NIST SP 800-115 was rejected as organizational-level overkill for a single component.
- ATT&CK was positioned as a supplementary taxonomy (used in `technique_allowlist`) rather than an engagement framework.

The combination provides both phase structure (PTES: pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, reporting) and control-based testing discipline (OSSTMM: process controls, access controls, trust controls).

**Why alternatives would be weaker:** PTES alone lacks the control-based testing discipline that OSSTMM provides for trust boundary verification. OSSTMM alone lacks the engagement lifecycle structure that ensures systematic coverage. OWASP would introduce web-specific testing overhead irrelevant to a CLI tool.

### Design Decision: Agent Team Composition with RoE-Gated Exclusions

**Strongest interpretation:** The decision to authorize only 4 agents (red-vuln, red-exploit, red-reporter, red-lead) and explicitly exclude 7 agents with documented reasons is a principled application of the principle of least privilege to the engagement itself. Each exclusion is justified:

- **red-recon** excluded because full source code access eliminates the need for reconnaissance.
- **red-privesc** excluded because there are no privilege boundaries in a CLI tool.
- **red-lateral** excluded because there is no network component.
- **red-persist**, **red-exfil**, **red-social**, **red-infra** excluded per rules of engagement.

This demonstrates mature engagement scoping: the scope is narrowed to what adds value (application-layer vulnerability analysis and exploitation) rather than running the full agent roster for completeness theater.

**Hidden strength:** The `agent_authorizations` YAML block (lines 389-468) specifies per-agent tool permissions and constraints. For example, `red-exploit` is permitted `Bash` (for PoC execution) but constrained to "MUST confine all PoC payloads to evidence directory." This granular authorization prevents scope creep during exploitation phases.

### Design Decision: Per-Component Test Matrices with CWE Mapping

**Strongest interpretation:** The testing approach section (lines 564-634) provides per-component test matrices with:
- Specific test cases (not abstract categories)
- Expected behavior (what should happen)
- Severity if vulnerable (consequence assessment)
- CWE classification (industry-standard vulnerability taxonomy)

This creates a testable specification for the security assessment. Each row in the test matrices is verifiable: either the parser exhibits the expected behavior or it does not. This is superior to vague testing guidelines like "test for injection attacks."

**Hidden strength:** The test matrices include tests for both new components (YamlFrontmatter, XmlSectionParser) and existing components' interaction with new functionality. The "L2-REINJECT spoofing" test case (line 598) is particularly insightful -- it tests whether a crafted HTML comment can inject an unauthorized governance directive, which is the highest-impact attack scenario given that L2-REINJECT directives control per-prompt rule injection across the entire Jerry Framework. [SM-004-B1]

### Design Decision: Success Criteria with Quantitative Thresholds

**Strongest interpretation:** The engagement completion criteria (lines 642-649) define measurable thresholds: 100% component coverage, >= 8 of 9 CWE categories tested, 100% finding quality (CVSS + CWE + remediation), >= 90% PoC coverage for Critical/High findings. These are not aspirational goals; they are pass/fail criteria that determine whether the engagement has met its objectives.

The quality gate for handoff to eng-security (lines 653-659) defines five dimensions (Completeness, Evidence, Actionability, Prioritization, Traceability) that align with the quality-enforcement.md dimensions. This structural alignment ensures the red team output is directly consumable by the engineering security phase.

---

## Cross-Deliverable Coherence

The strongest hidden quality of this deliverable set is its **internal coherence across all four documents**. This is not merely four independent analyses; it is a mutually reinforcing system:

1. **Threat model identifies T-YF-07 (YAML deserialization) as DREAD 38 (highest risk)** -> Architecture ADR responds with Design Decision 1 (mandatory `yaml.safe_load()`) and Constraint C-04 -> Trust boundaries mark the YAML parser as a "CRITICAL CONTROL POINT" in the Zone 3 diagram -> Red team scope defines 7 specific test cases for YamlFrontmatter including `!!python/object/apply:os.system`.

2. **Threat model identifies T-XS-07 (XXE) as DREAD 33** -> Architecture ADR responds with Design Decision 6 (regex-only, no XML parser library) and Constraint C-07 -> Trust boundaries annotate "NO XML PARSER ALLOWED" in the Zone 3 diagram -> Red team scope includes entity expansion and billion-laughs test cases for XmlSectionParser.

3. **Threat model identifies T-DT-04 (path traversal) as DREAD 30** -> Architecture ADR documents M-08 (repo-root containment) and M-10 (symlink resolution) -> Trust boundaries specify V2 (is_relative_to check) and V5 (realpath) at BC-01 -> Red team scope includes path traversal, symlink following, null byte, and Unicode normalization test cases.

4. **Threat model recommends M-05 through M-07 and M-16/M-17 (input bounds)** -> Architecture ADR responds with Design Decision 8 (InputBounds class with documented defaults traceable to mitigations) -> Trust boundaries place input bounds at Checkpoint 1 (BC-02) as the first line of defense -> Red team scope includes oversized value and memory exhaustion test cases.

This four-way traceability chain (threat -> architecture -> trust boundary -> test plan) is the hallmark of mature security engineering. Each document strengthens the others: the threat model justifies the architectural constraints, the architecture operationalizes the mitigations, the trust boundaries visualize the defense layers, and the test plan verifies the whole system. [SM-005-B1]

---

## Improvement Findings Table

| ID | Improvement | Severity | Original | Strengthened | Affected Dimension |
|----|-------------|----------|----------|-------------|-------------------|
| SM-001-B1 | Threat model mitigations could explicitly state which implementation phase they belong to | Major | M-01 through M-19 listed with priority but phase assignment only mentioned in strategic implications | Each mitigation gains a "Phase" column: Phase 2 (implementation prerequisite) vs Phase 3 (testing) vs Phase 4 (quality gate) | Actionability |
| SM-002-B1 | ADR Parser Invocation Matrix could document the rationale for each parser-to-type mapping | Major | Matrix shows Y/- per DocumentType x Parser but no per-cell rationale | Each cell gets a footnote explaining why that parser is/is not applicable to that document type | Traceability |
| SM-003-B1 | Trust boundary validation checks could include expected error behavior (not just check description) | Major | V1-V30 describe what is checked but not what happens on failure | Each check gains an "On Failure" column specifying the error code, message, and recovery behavior | Actionability |
| SM-004-B1 | Red team scope L2-REINJECT spoofing test could cross-reference the specific enforcement architecture layer at risk | Minor | Test case mentions "L2-REINJECT parser MUST NOT accept directives from untrusted files" | Cross-reference to quality-enforcement.md L2 enforcement layer and specific H- rules that would be compromised | Traceability |
| SM-005-B1 | Cross-deliverable traceability could be made explicit via a traceability matrix appendix | Minor | Traceability is implicit -- the four documents reference each other but no single table maps Threat -> ADR Decision -> Trust Boundary -> Test Case | Add a cross-reference appendix showing the complete traceability chain for each top-10 threat | Traceability |
| SM-006-B1 | ADR schema extension section could include example schema definitions for 2-3 new types | Minor | Schema names and key fields listed in a table but no concrete FieldRule/SectionRule examples | Add complete schema definitions for `agent_definition` and `adr` as illustrative examples | Evidence Quality |
| SM-007-B1 | Threat model could include a "Threats NOT Modeled" section beyond the disclaimer | Minor | Disclaimer lists out-of-scope areas but does not discuss threat categories deliberately excluded within the in-scope components | Add a section documenting threat categories considered but assessed as inapplicable (e.g., network-based threats, authentication bypass) with brief justification | Completeness |
| SM-008-B1 | Red team scope could include estimated effort per component to support resource allocation | Minor | Test matrices define test cases but not estimated complexity or time per component | Add effort estimates (Low/Medium/High) per component to help red-vuln and red-exploit plan their work | Actionability |
| SM-009-B1 | Trust boundaries document could reference the ADR design decisions by ID | Minor | Trust boundary diagram annotates constraints but uses descriptive text rather than ADR decision IDs | Annotate each control point with the corresponding ADR Design Decision number (e.g., "DD-6: regex-only") | Traceability |
| SM-010-B1 | ADR Alternatives Considered could include a structured comparison matrix | Minor | Alternatives are described in prose with individual "Rejected" rationale | Add a comparison matrix: Alternative x Criterion (Security, Complexity, Compatibility, Performance) | Methodological Rigor |
| SM-011-B1 | Threat model PASTA Stage 5 vulnerability analysis could reference specific line numbers in the existing codebase for existing vulnerabilities V-01 through V-04 | Minor | V-01 references "ast_commands.py:144-163" but the cross-reference is not systematic for all entries | All V- entries include file path and line number range, enabling direct verification | Evidence Quality |

---

## Improvement Details

### SM-001-B1: Mitigation Phase Assignment (Major)

**Affected Dimension:** Actionability (0.15 weight)

**Original Content:** The threat model's "Strategic Implications" section (lines 616-618) mentions phases: "Phase 2 (Implementation): Implement M-01 through M-08 before any parser code is written. Phase 3 (Testing): Include adversarial test cases. Phase 4 (Quality Gate)." However, the mitigation table itself (lines 540-559) only assigns Priority (CRITICAL/HIGH/MEDIUM/LOW) without a Phase column.

**Strengthened Content:** Adding a "Phase" column to the mitigation table would allow implementers to immediately see which mitigations are preconditions (must be implemented before parser code) versus post-conditions (verified during testing). For example, M-01 (banned API lint rule) and M-11 (no XML parser) are architectural preconditions, while M-04 (integration test) and M-12 (ReDoS-safe regex review) are testing-phase activities.

**Rationale:** An implementer reading the mitigation table without reading the strategic implications section would not know the intended implementation order. The phase assignment makes the mitigation table self-contained.

**Best Case Conditions:** The improvement is strongest when the mitigation table is consumed by a different team than the one that wrote the threat model, which is the expected scenario (eng-security receives the threat model from eng-architect).

### SM-002-B1: Parser Invocation Matrix Rationale (Major)

**Affected Dimension:** Traceability (0.10 weight)

**Original Content:** The Parser Invocation Matrix (ADR lines 372-384) shows which parsers are invoked for which document types using Y/- notation. For example, AGENT_DEFINITION invokes JerryDocument, YamlFrontmatter, XmlSectionParser, and NavTable -- but not BlockquoteFrontmatter or HtmlCommentMetadata.

**Strengthened Content:** Each non-obvious mapping could include a brief rationale. For example: "AGENT_DEFINITION uses YamlFrontmatter because agent definitions use `---` delimited YAML frontmatter per H-34. AGENT_DEFINITION uses XmlSectionParser because agent definition bodies use `<identity>`, `<methodology>`, etc. per agent-development-standards.md." The obvious mappings (JerryDocument always invoked, NavTable for all types) do not need rationale.

**Rationale:** The matrix is currently a design assertion. Adding rationale transforms it into a justified decision, enabling reviewers to verify that each mapping is correct without having to independently derive the reasoning.

**Best Case Conditions:** Most valuable when validating the matrix during implementation: an implementer can verify they are invoking the correct parsers for each document type by checking the rationale against the framework standards.

### SM-003-B1: Validation Check Failure Behavior (Major)

**Affected Dimension:** Actionability (0.15 weight)

**Original Content:** The trust boundaries document specifies 30 validation checks (V1-V30) with descriptions of what is checked at each boundary crossing. For example, V2: "Path(file_path).resolve().is_relative_to(repo_root) -> Reject traversal (M-08)."

**Strengthened Content:** Each validation check could include an "On Failure" specification: V2: "On failure: return `ParseError(code='PATH_TRAVERSAL', message='File path {path} is outside repository root', exit_code=3)`." This would define the error contract for each validation failure, enabling implementers to write consistent error handling without making ad-hoc decisions.

**Rationale:** Knowing what to check (V1-V30) is necessary but not sufficient for implementation. Knowing what to do when the check fails is equally important. The current document tells implementers *what* to validate but not *how to fail*, which is a gap that different implementers would fill inconsistently.

**Best Case Conditions:** Most valuable when multiple developers implement different parsers: consistent error handling across all parsers requires a defined error contract.

---

## Per-Dimension Scoring

### Completeness (Weight: 0.20)

**Score: 4.5 / 5.0**

**Justification:** The deliverable set covers all required elements for a C4 Phase 1 architecture:

- **Threat model:** 29 threats across 5 STRIDE categories for 5 components. DREAD scoring for all threats. 3 attack trees for top-3 risks. PASTA stages 4-7. 19 mitigations. NIST CSF 2.0 mapping. Strategic implications. Disclaimer.
- **Architecture ADR:** 8 design decisions with rationale. Hexagonal architecture compliance verification (H-07). One-class-per-file compliance verification (H-10). 5 alternatives considered. Consequences (positive, negative, neutral). Strategic implications with evolution path.
- **Trust boundaries:** 6-zone ASCII diagram. 5 boundary crossings with validation checklists (30 checks total). Per-parser data flow diagrams. Schema validation checkpoint diagram. Write-back path analysis with TOCTOU awareness. Threat overlay.
- **Red team scope:** YAML scope definition with authorized targets (15), technique allowlist (14 CWE/ATT&CK), exclusion list (11), rules of engagement, evidence handling. Per-component test matrices (6 components, 43 test cases total). Agent team composition with exclusion justifications. Success criteria with quantitative thresholds.

**Minor gap (SM-007-B1):** The threat model could include a "Threats NOT Modeled" section for threat categories deliberately excluded within in-scope components. This would strengthen completeness by making the boundary between "analyzed and found safe" versus "not analyzed" explicit.

### Internal Consistency (Weight: 0.20)

**Score: 5.0 / 5.0**

**Justification:** The four deliverables are internally consistent and mutually reinforcing:

- Threat IDs (T-YF-*, T-XS-*, T-HC-*, T-DT-*, T-SV-*) are used consistently across all documents.
- Mitigation IDs (M-01 through M-19) are referenced consistently in the threat model, ADR, and trust boundaries.
- DREAD scores in the threat model match the priority classifications used in the ADR and test matrices.
- The trust zone classifications (Z1-Z6) are consistent between the threat model and the trust boundaries document.
- The parser invocation matrix in the ADR is consistent with the data flow diagrams in the trust boundaries.
- The red team scope's test cases directly target the specific threats identified in the threat model.
- Constraint IDs (C-01 through C-07) in the ADR are traceable to specific threat model findings and framework HARD rules.
- The DocumentType enum values in the ADR are consistent across the component diagram, detection algorithm, and parser invocation matrix.

No contradictions, inconsistencies, or conflicting recommendations were identified across the 2,618 total lines of the four deliverables.

### Methodological Rigor (Weight: 0.20)

**Score: 4.5 / 5.0**

**Justification:** The methodological rigor is very strong:

- **Threat model** uses four complementary methodologies (STRIDE, DREAD, attack trees, PASTA) and applies each correctly. STRIDE is per-component. DREAD scoring uses the standard 5-dimension scale. Attack trees follow the standard AND/OR notation with likelihood and mitigation annotations. PASTA stages 4-7 include realistic threat agents with motivations.
- **ADR** follows the standard ADR format (Context, Decision, Consequences, Alternatives Considered) and adds hexagonal architecture compliance verification, which demonstrates architectural discipline beyond what most ADRs include.
- **Trust boundaries** use the standard zone-based trust model with boundary crossings and validation checkpoints. The ASCII diagram format is clear and annotated.
- **Red team scope** follows PTES methodology and supplements with OSSTMM Section III controls. The test matrices are structured as specification tables with expected behavior and severity assessment.

**Minor gap (SM-010-B1):** The ADR's Alternatives Considered section uses prose descriptions rather than a structured comparison matrix (Alternative x Criterion). A matrix would make the evaluation more systematic and enable reviewers to verify that each alternative was assessed against the same criteria.

### Evidence Quality (Weight: 0.15)

**Score: 4.0 / 5.0**

**Justification:** Evidence quality is good but has room for strengthening:

- **Quantitative evidence:** DREAD scores, NIST CSF 2.0 mappings, CWE classifications, OWASP Top 10 mappings, and ATT&CK technique IDs provide industry-standard evidence anchors.
- **Codebase evidence:** The threat model references specific code locations (e.g., "ast_commands.py:144-163" for _read_file, "frontmatter.py:46" for _FRONTMATTER_PATTERN). The red team scope identifies 5 specific known risk areas with line-level references.
- **Architectural evidence:** The ADR includes Python code snippets for proposed class interfaces, regex patterns, and data structures. These are testable specifications, not abstract descriptions.

**Gap (SM-006-B1):** The ADR's schema extension section lists new schema names and key fields but does not include example FieldRule/SectionRule definitions. Concrete examples would strengthen the evidence that the schema extension pattern works for the new file types.

**Gap (SM-011-B1):** The PASTA Stage 5 vulnerability analysis (V-01 through V-04) inconsistently references line numbers -- some entries have them (V-01: "ast_commands.py:144-163") and some do not (V-03: "frontmatter.py:46" references a single line but the pattern may span multiple lines).

### Actionability (Weight: 0.15)

**Score: 4.0 / 5.0**

**Justification:** The deliverables are highly actionable:

- **Threat model mitigations** include implementation-ready guidance (ruff rule specifications, exact size limits, specific Python API calls).
- **ADR design decisions** include class interfaces with type annotations, regex patterns, and import constraints that can be directly implemented.
- **Trust boundary validation checklists** specify exact checks (V1-V30) with mitigation cross-references.
- **Red team test matrices** specify exact test cases with expected behavior.

**Gap (SM-001-B1):** The mitigation table lacks phase assignment (which mitigations are preconditions vs. which are testing activities). This was identified as a Major improvement because it directly affects the implementer's ability to sequence their work correctly.

**Gap (SM-003-B1):** The validation checklists specify what to check but not what to do on failure (error codes, messages, recovery behavior). This was identified as a Major improvement because inconsistent error handling is a common implementation defect.

### Traceability (Weight: 0.10)

**Score: 4.0 / 5.0**

**Justification:** Traceability is good at the individual document level:

- The threat model traces threats to mitigations, mitigations to NIST CSF functions, and threats to DREAD scores.
- The ADR traces design decisions to constraints (C-01 through C-07) which trace to framework HARD rules (H-07, H-10, H-33).
- The trust boundaries trace validation checks to mitigations.
- The red team scope traces test cases to CWE classifications and engagement targets.

**Gap (SM-002-B1):** The Parser Invocation Matrix lacks per-cell rationale, making it an assertion rather than a traceable decision.

**Gap (SM-005-B1):** Cross-deliverable traceability is implicit rather than explicit. A traceability matrix showing Threat -> ADR Decision -> Trust Boundary Check -> Red Team Test Case would make the coherence visible and auditable.

**Gap (SM-009-B1):** The trust boundary diagram annotates constraints with descriptive text rather than ADR decision IDs, which weakens the cross-reference between the two documents.

---

## Scoring Impact

| Dimension | Weight | Pre-Steelman | Post-Steelman | Impact | Rationale |
|-----------|--------|-------------|---------------|--------|-----------|
| Completeness | 0.20 | 4.5 | 4.5 | Neutral | Already near-complete; SM-007-B1 (minor) would close the remaining gap |
| Internal Consistency | 0.20 | 5.0 | 5.0 | Neutral | Already at maximum; no inconsistencies found |
| Methodological Rigor | 0.20 | 4.5 | 4.5 | Neutral | Already strong; SM-010-B1 (minor) would add structured comparison |
| Evidence Quality | 0.15 | 4.0 | 4.0 | Neutral | SM-006-B1 and SM-011-B1 (minor) would strengthen |
| Actionability | 0.15 | 4.0 | 4.5 | Positive | SM-001-B1 (major: phase assignment) and SM-003-B1 (major: failure behavior) would improve |
| Traceability | 0.10 | 4.0 | 4.5 | Positive | SM-002-B1 (major: matrix rationale), SM-005-B1, SM-009-B1 (minor) would improve |

### Overall Weighted Score

**Pre-Steelman (current deliverable quality):**
```
(4.5 * 0.20) + (5.0 * 0.20) + (4.5 * 0.20) + (4.0 * 0.15) + (4.0 * 0.15) + (4.0 * 0.10)
= 0.90 + 1.00 + 0.90 + 0.60 + 0.60 + 0.40
= 4.40 / 5.0
= 0.88
```

**Post-Steelman (with Major improvements incorporated):**
```
(4.5 * 0.20) + (5.0 * 0.20) + (4.5 * 0.20) + (4.0 * 0.15) + (4.5 * 0.15) + (4.5 * 0.10)
= 0.90 + 1.00 + 0.90 + 0.60 + 0.675 + 0.45
= 4.525 / 5.0
= 0.905
```

**Post-Steelman (with all improvements incorporated):**
```
(4.75 * 0.20) + (5.0 * 0.20) + (4.75 * 0.20) + (4.5 * 0.15) + (4.75 * 0.15) + (4.75 * 0.10)
= 0.95 + 1.00 + 0.95 + 0.675 + 0.7125 + 0.475
= 4.7625 / 5.0
= 0.953
```

**Overall weighted score: 0.88 (pre-steelman) -> 0.905 (major improvements) -> 0.953 (all improvements)**

---

## Best Case Scenario

The deliverables are strongest under the following conditions:

1. **The universal parser is implemented as described in the ADR.** The architecture decisions (polymorphic parsers, regex-only XML, InputBounds, path-first detection) are security-optimal for the specific constraints of the Jerry Framework. If the implementation follows these decisions faithfully, the resulting parser will have a well-bounded attack surface with defense-in-depth at three checkpoints.

2. **The threat model's mitigations are treated as preconditions, not post-conditions.** The strategic implication that M-01 through M-08 should be implemented "before any parser code is written" (line 616) is the correct sequencing. If these mitigations are deferred to post-implementation, the codebase will spend time in a vulnerable state.

3. **The red team engagement executes as scoped.** The per-component test matrices provide a comprehensive testing specification. If red-vuln and red-exploit follow this specification, the resulting findings will be directly actionable by eng-security.

4. **The four documents are consumed as a coherent set, not individually.** The cross-deliverable traceability (Threat -> ADR -> Trust Boundary -> Test Plan) means each document gains strength from the others. An implementer who reads only the ADR would miss the threat-driven justification for design decisions. A tester who reads only the red team scope would miss the architectural context that informs expected behavior.

**Key assumptions that must hold:**
- PyYAML's `yaml.safe_load()` continues to restrict deserialization to basic Python types (as it has since PyYAML 5.1).
- The regex patterns in the XmlSectionParser and HtmlCommentMetadata parsers are implemented with non-greedy matching as specified.
- The `InputBounds.DEFAULT` values are not overridden without documented justification.
- The `DocumentTypeDetector` path patterns remain synchronized with the framework's directory structure.

**Confidence:** HIGH. The deliverables demonstrate comprehensive analysis, well-justified decisions, and actionable specifications. The 3 Major improvements identified are presentational/organizational enhancements, not substantive corrections -- the underlying analysis and decisions are sound.

---

*Steelman Report Version: 1.0.0*
*Strategy: S-003 (Steelman Technique)*
*SSOT: `.context/rules/quality-enforcement.md`*
*Date: 2026-02-22*
*Agent: adv-executor*
*Execution ID: B1*
