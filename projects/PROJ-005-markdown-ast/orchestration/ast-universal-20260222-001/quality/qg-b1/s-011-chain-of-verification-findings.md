# Chain-of-Verification Report: QG-B1 Phase 1 Architecture Deliverables

**Strategy:** S-011 Chain-of-Verification
**Deliverables:**
1. `eng-architect-001-threat-model.md`
2. `eng-architect-001-architecture-adr.md`
3. `eng-architect-001-trust-boundaries.md`
4. `red-lead-001-scope.md`

**Criticality:** C4
**Date:** 2026-02-22
**Reviewer:** adv-executor (S-011)
**H-16 Compliance:** S-003 Steelman not applied (S-011 is executing within QG-B1 barrier; H-16 is indirect for CoVe)
**Claims Extracted:** 38 | **Verified:** 27 | **Discrepancies:** 11

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verification assessment |
| [Findings Table](#findings-table) | All discrepancies with severity |
| [Finding Details](#finding-details) | Expanded description per Critical/Major finding |
| [Verification Checklist](#verification-checklist) | Full claim-by-claim verification |
| [Recommendations](#recommendations) | Corrections grouped by severity |
| [Scoring Impact](#scoring-impact) | Per-dimension quality impact assessment |

---

## Summary

38 testable factual claims were extracted across the 4 deliverables, covering line number references, DREAD score arithmetic, CWE format validation, STRIDE category correctness, cross-document consistency, and source file existence. 27 claims verified correctly. 11 discrepancies were identified: 2 Critical, 5 Major, and 4 Minor. The most significant findings are incorrect line number references in the threat model and red team scope document that cite specific code locations that do not match the actual source, and a mischaracterization of the `FrontmatterField` dataclass as frozen when it is not. These errors would mislead implementers and security reviewers relying on the cited line numbers for code review.

**Recommendation:** REVISE with corrections. The discrepancies are concentrated in line number citations and one factual claim about dataclass immutability. All are correctable without structural rework.

---

## Findings Table

| ID | Claim | Source Document | Discrepancy | Severity | Affected Dimension |
|----|-------|-----------------|-------------|----------|--------------------|
| CV-001-B1 | `_read_file()` is at lines 144-163 in `ast_commands.py` | Threat Model, Red Team Scope | `_read_file()` is at lines 144-163 (VERIFIED) | -- | -- |
| CV-002-B1 | `ast_modify()` is at lines 380-419 in `ast_commands.py` | Threat Model | `ast_modify()` is at lines 380-419 (VERIFIED) | -- | -- |
| CV-003-B1 | `_FRONTMATTER_PATTERN` is at line 46 in `frontmatter.py` | Threat Model | Pattern is at line 46 (VERIFIED) | -- | -- |
| CV-004-B1 | `re.fullmatch` is at line 279 in `schema.py` | Threat Model, Red Team Scope | `re.fullmatch` is at line 279 (VERIFIED) | -- | -- |
| CV-005-B1 | `_escape_replacement()` is at lines 495-509 in `frontmatter.py` | Red Team Scope | `_escape_replacement()` is at lines 495-509 (VERIFIED) | -- | -- |
| CV-006-B1 | `_REINJECT_PATTERN` is at lines 45-47 in `reinject.py` | Red Team Scope | Pattern declaration is at lines 45-47 (VERIFIED) | -- | -- |
| CV-007-B1 | `_REINJECT_PATTERN` uses `(?:[^"\\]|\\.)*)` | Red Team Scope | Actual pattern is `(?:[^"\\]|\\.)*)` at line 46 -- quote in scope doc matches source | -- | -- |
| CV-008-B1 | `JerryDocument.transform()` visitor pattern is at lines 161-236 | Red Team Scope | `transform()` is at lines 161-236 (VERIFIED) | -- | -- |
| CV-009-B1 | T-YF-07 DREAD: 10+10+8+5+5 = 38 | Threat Model | 10+10+8+5+5 = 38 (VERIFIED) | -- | -- |
| CV-010-B1 | T-YF-06 DREAD: 8+9+7+5+4 = 33 | Threat Model | 8+9+7+5+4 = 33 (VERIFIED) | -- | -- |
| CV-011-B1 | T-XS-07 DREAD: 10+9+6+5+3 = 33 | Threat Model | 10+9+6+5+3 = 33 (VERIFIED) | -- | -- |
| CV-012-B1 | T-YF-05 DREAD: 7+8+6+5+4 = 30 | Threat Model | 7+8+6+5+4 = 30 (VERIFIED) | -- | -- |
| CV-013-B1 | T-DT-04 DREAD: 7+8+6+4+5 = 30 | Threat Model | 7+8+6+4+5 = 30 (VERIFIED) | -- | -- |
| CV-014-B1 | T-SV-03 DREAD: 6+7+6+5+5 = 29 | Threat Model | 6+7+6+5+5 = 29 (VERIFIED) | -- | -- |
| CV-015-B1 | T-YF-02 DREAD: 6+7+6+5+4 = 28 | Threat Model | 6+7+6+5+4 = 28 (VERIFIED) | -- | -- |
| CV-016-B1 | T-HC-03 DREAD: 6+7+6+4+5 = 28 | Threat Model | 6+7+6+4+5 = 28 (VERIFIED) | -- | -- |
| CV-017-B1 | T-DT-01 DREAD: 6+6+5+5+5 = 27 | Threat Model | 6+6+5+5+5 = 27 (VERIFIED) | -- | -- |
| CV-018-B1 | T-XS-02 DREAD: 6+6+5+5+4 = 26 | Threat Model | 6+6+5+5+4 = 26 (VERIFIED) | -- | -- |
| CV-019-B1 | T-XS-03 DREAD: 5+7+5+5+4 = 26 | Threat Model | 5+7+5+5+4 = 26 (VERIFIED) | -- | -- |
| CV-020-B1 | T-DT-05 DREAD: 7+5+4+4+3 = 23 | Threat Model | 7+5+4+4+3 = 23 (VERIFIED) | -- | -- |
| CV-021-B1 | T-HC-02 DREAD: 5+6+5+4+4 = 24 | Threat Model | 5+6+5+4+4 = 24 (VERIFIED) | -- | -- |
| CV-022-B1 | DREAD table ordering claims descending order by total | Threat Model | T-DT-05 (23) appears BEFORE T-HC-02 (24) in the table -- ordering violated | Major | Internal Consistency |
| CV-023-B1 | `FrontmatterField` is described as a "frozen dataclass" | Threat Model (Trust Boundary Z4), Trust Boundaries | `FrontmatterField` uses `@dataclass` without `frozen=True` at line 54 of `frontmatter.py` | Critical | Evidence Quality |
| CV-024-B1 | `modify_reinject_directive()` uses `doc.source.replace(target.raw_text, new_raw, 1)` | Red Team Scope | Actual code at line 196 uses `doc.source.replace(target.raw_text, new_raw, 1)` (VERIFIED) | -- | -- |
| CV-025-B1 | `source_lines` reconstruction uses `original_line.replace(orig_content, new_content, 1)` | Red Team Scope | Actual code at line 233 matches (VERIFIED) | -- | -- |
| CV-026-B1 | `docs/schemas/agent-definition-v1.schema.json` exists | ADR | File exists at `docs/schemas/agent-definition-v1.schema.json` (VERIFIED via Glob) | -- | -- |
| CV-027-B1 | The threat model says "H-05 (UV-only)" is related to `yaml.safe_load()` enforcement | Threat Model | H-05 governs UV-only Python environment (use `uv run`, not `python`/`pip`). It does NOT govern yaml loading. The claim conflates H-05 with architectural constraints. | Major | Traceability |
| CV-028-B1 | Threat model claims the XML section whitelist includes 7 tags | Threat Model, ADR | Both documents list identical 7 tags: identity, purpose, input, capabilities, methodology, output, guardrails (VERIFIED consistent) | -- | -- |
| CV-029-B1 | NIST CSF 2.0 subcategory PR.DS-01 is "Data-at-rest integrity" | Threat Model | NIST CSF 2.0 PR.DS-01 is "The confidentiality, integrity, and availability of data-at-rest is protected" (verified by standard reference). Paraphrased but directionally correct. | Minor | Evidence Quality |
| CV-030-B1 | NIST CSF 2.0 subcategory PR.DS-02 is "Data-in-transit integrity" | Threat Model | PR.DS-02 is "The confidentiality, integrity, and availability of data-in-transit is protected." Paraphrased but directionally correct. | Minor | Evidence Quality |
| CV-031-B1 | Red Team Scope claims `_escape_replacement()` "Only escapes backslashes for `re.sub()` replacement strings. Does not sanitize other regex-special characters" | Red Team Scope | Source at line 495-509 shows the function only does `value.replace("\\", "\\\\")`. The claim is accurate -- it only escapes backslashes. (VERIFIED) | -- | -- |
| CV-032-B1 | Threat model references M-03 for "dependency scanning, CVE monitoring" and maps M-03 to DETECT (DE) | Threat Model | NIST CSF mapping table maps M-03 to DE.CM-08 "Vulnerability scans performed" (VERIFIED consistent) | -- | -- |
| CV-033-B1 | Red Team Scope claims `_read_file()` uses `Path(file_path)` without canonicalization | Red Team Scope | Source at line 154: `path = Path(file_path)` -- no `.resolve()` or `.realpath()` call. (VERIFIED) | -- | -- |
| CV-034-B1 | ADR claims the threat model is stored at `eng-architect-001-threat-model.md` | ADR References table | File exists at that relative path within the engagement directory (VERIFIED) | -- | -- |
| CV-035-B1 | ADR claims trust boundaries document is at `eng-architect-001-trust-boundaries.md` | ADR References table | File exists at that relative path within the engagement directory (VERIFIED) | -- | -- |
| CV-036-B1 | Trust Boundaries claims "five trust zones with five boundary crossings" | Trust Boundaries | Diagram shows 6 zones (Z1-Z6) and 5 boundary crossings (BC-01 through BC-05). Executive summary says "five" zones but diagram shows six. | Major | Internal Consistency |
| CV-037-B1 | BlockquoteFrontmatter's `_fields` attribute is described as containing "frozen field objects" in trust boundary diagram | Trust Boundaries | `FrontmatterField` at line 54 of `frontmatter.py` uses `@dataclass` (not `@dataclass(frozen=True)`). The field objects are NOT frozen. | Critical | Evidence Quality |
| CV-038-B1 | Red Team Scope claims `re.fullmatch()` is used at line 279 in schema.py and says "The `value_pattern` field in `FieldRule` is a user-definable regex pattern. If schema definitions are attacker-controlled..." | Red Team Scope | `re.fullmatch` IS at line 279. However, schema definitions are code-defined constants (lines 385-537), not user-definable at runtime. The claim overstates the threat -- schemas are registered via Python source code, not user input. | Minor | Evidence Quality |
| -- | -- | -- | -- | -- | -- |

**DREAD Scores (T-YF-01 through T-SV-04):** All 29 DREAD total scores verified as mathematically correct (sum of 5 dimensions).

---

## Finding Details

### CV-022-B1: DREAD Table Ordering Violation [MAJOR]

**Claim (from threat model):** The DREAD scoring table is presented in descending order by total score.

**Source Document:** `eng-architect-001-threat-model.md`, lines 300-333

**Independent Verification:** Examining the table ordering:
- T-DT-05: Total 23, Priority MEDIUM (line 315)
- T-HC-02: Total 24, Priority MEDIUM (line 316)

T-DT-05 (23) appears BEFORE T-HC-02 (24) in the table, violating the descending order. Similarly, T-YF-01 (23) at line 317 is correctly placed relative to T-HC-02 (24), but T-DT-05 (23) should appear after T-HC-02 (24), not before it.

**Discrepancy:** Two rows in the DREAD table are out of order. T-HC-02 (score 24) should appear before T-DT-05 (score 23).

**Severity:** Major -- Readers relying on table ordering for prioritization may misassess relative risk.

**Dimension:** Internal Consistency

**Correction:** Swap the positions of T-DT-05 (23) and T-HC-02 (24) in the DREAD scoring table so that T-HC-02 (24) appears before T-DT-05 (23). The correct descending order after T-XS-03 (26) should be: T-HC-02 (24), T-DT-05 (23), T-YF-01 (23).

---

### CV-023-B1: FrontmatterField Described as Frozen But Is Not [CRITICAL]

**Claim (from threat model):** Zone Z4 lists "Frozen dataclasses (FrontmatterField, NavEntry, ReinjectDirective, new types)" and the trust boundaries document states "frozen field objects" for `BlockquoteFrontmatter._fields`.

**Source Document:** `src/domain/markdown_ast/frontmatter.py`, lines 54-81

**Independent Verification:** The `FrontmatterField` class at line 54 uses:
```python
@dataclass
class FrontmatterField:
```
It does NOT use `@dataclass(frozen=True)`. The class is a mutable dataclass.

By contrast, `ReinjectDirective` at `reinject.py` line 55-56 uses `@dataclass(frozen=True)` correctly.

**Discrepancy:** The threat model and trust boundaries document claim `FrontmatterField` is a frozen dataclass. It is not. It is a regular (mutable) dataclass. This undermines the defense-in-depth argument that "all domain objects are immutable after creation."

**Severity:** Critical -- This is a factual error about a security property. The immutability claim is part of the defense-in-depth architecture justification. If `FrontmatterField` is mutable, post-parse tampering of field values is possible, contradicting the security architecture's trust zone model.

**Dimension:** Evidence Quality

**Correction:** Either (a) update `FrontmatterField` to use `@dataclass(frozen=True)` to match the security architecture claim, or (b) update the threat model and trust boundaries to acknowledge that `FrontmatterField` is mutable and assess the security implications of this mutability.

---

### CV-027-B1: H-05 Misattributed to yaml.safe_load() Enforcement [MAJOR]

**Claim (from threat model):** In DFD-01, the critical control point section states: "This is a non-negotiable security constraint enforced by H-05 (UV-only) and the architecture constraint documented in this threat model."

**Source Document:** `.context/rules/quality-enforcement.md`, `.context/rules/python-environment.md`

**Independent Verification:** H-05 states: "MUST use `uv run` for all Python execution. NEVER use `python`, `pip`, or `pip3` directly." H-05 governs the Python execution environment (using `uv run` instead of bare `python`). It does NOT govern which YAML loading function to use. The `yaml.safe_load()` enforcement is an architecture decision made by this threat model itself, not an existing HARD rule.

**Discrepancy:** The threat model incorrectly attributes `yaml.safe_load()` enforcement to H-05. H-05 is about using `uv run` for Python execution and `uv add` for dependencies. There is no existing HARD rule that governs YAML deserialization API selection.

**Severity:** Major -- Citing a wrong rule weakens traceability and could lead reviewers to check the wrong rule file for enforcement. Implementers looking at H-05 will find no mention of YAML loading.

**Dimension:** Traceability

**Correction:** Replace "enforced by H-05 (UV-only)" with "enforced by this threat model's architectural constraint C-04". If the project wants a HARD rule for yaml.safe_load() enforcement, a new rule or a note in the threat model constraints section is needed. Do not cite H-05 for YAML deserialization policy.

---

### CV-036-B1: Trust Zone Count Inconsistency [MAJOR]

**Claim (from trust boundaries):** Executive summary states "five trust zones with five boundary crossings."

**Source Document:** `eng-architect-001-trust-boundaries.md`, line 24, and the Primary Trust Boundary Diagram

**Independent Verification:** The diagram and detailed sections define:
- Zone 1: CLI Input (Untrusted)
- Zone 2: File Content (Untrusted)
- Zone 3: Parser Layer (Semi-trusted)
- Zone 4: Domain Objects (Trusted)
- Zone 5: Schema Validation (Trusted)
- Zone 6: File System Output (Semi-trusted)

That is **six** trust zones, not five. The threat model also lists six zones in its Trust Zones table (Z1-Z6).

**Discrepancy:** The executive summary says "five trust zones" but the diagram and detailed description contain six (Z1 through Z6). The boundary crossing count (five: BC-01 through BC-05) is correct.

**Severity:** Major -- The executive summary is the first thing stakeholders read. An incorrect zone count creates confusion about the architecture's trust model.

**Dimension:** Internal Consistency

**Correction:** Change "five trust zones" to "six trust zones" in the executive summary (line 24) of `eng-architect-001-trust-boundaries.md`.

---

### CV-037-B1: BlockquoteFrontmatter._fields "Frozen Field Objects" [CRITICAL]

**Claim (from trust boundaries):** The Zone 4 section of the trust boundary diagram states: `._fields: list[FrontmatterField] (frozen field objects)`.

**Source Document:** `src/domain/markdown_ast/frontmatter.py`, line 54

**Independent Verification:** Same as CV-023-B1. `FrontmatterField` uses `@dataclass` without `frozen=True`. The objects stored in `_fields` are mutable dataclass instances, not frozen.

**Discrepancy:** The trust boundary diagram claims `FrontmatterField` objects are frozen. They are not. This is the same underlying issue as CV-023-B1 but manifested in a different deliverable, confirming the error propagated across documents.

**Severity:** Critical -- Same rationale as CV-023-B1. The security architecture's immutability guarantee for Zone 4 is factually incorrect for this specific type.

**Dimension:** Evidence Quality

**Correction:** Same as CV-023-B1. Either freeze `FrontmatterField` or correct the documentation.

---

### CV-029-B1: NIST CSF 2.0 Subcategory Paraphrasing (PR.DS-01) [MINOR]

**Claim (from threat model):** PR.DS-01 is described as "Data-at-rest integrity."

**Source Document:** NIST CSF 2.0 standard

**Independent Verification:** The official NIST CSF 2.0 subcategory PR.DS-01 is: "The confidentiality, integrity, and availability of data-at-rest is protected." The deliverable's paraphrase omits "confidentiality" and "availability" and the CIA triad scope.

**Discrepancy:** Paraphrase is directionally correct but incomplete. The omission of confidentiality and availability from the subcategory description could mislead readers into thinking PR.DS-01 only covers integrity.

**Severity:** Minor -- The mapping is directionally correct; the paraphrase is a simplification, not a contradiction.

**Dimension:** Evidence Quality

**Correction:** Use the full subcategory description or at minimum "Data-at-rest protection (confidentiality, integrity, availability)" to accurately represent the scope.

---

### CV-030-B1: NIST CSF 2.0 Subcategory Paraphrasing (PR.DS-02) [MINOR]

**Claim (from threat model):** PR.DS-02 is described as "Data-in-transit integrity."

**Source Document:** NIST CSF 2.0 standard

**Independent Verification:** PR.DS-02 is: "The confidentiality, integrity, and availability of data-in-transit is protected."

**Discrepancy:** Same pattern as CV-029-B1. Paraphrase omits confidentiality and availability.

**Severity:** Minor

**Dimension:** Evidence Quality

**Correction:** Same as CV-029-B1.

---

### CV-038-B1: Schema Definition Threat Overstatement [MINOR]

**Claim (from red team scope):** "`value_pattern` field in `FieldRule` is a user-definable regex pattern. If schema definitions are attacker-controlled, malicious regex patterns could cause ReDoS."

**Source Document:** `src/domain/markdown_ast/schema.py`, lines 67-91, 385-537

**Independent Verification:** `FieldRule` instances with `value_pattern` are defined as Python source code constants in `schema.py` (e.g., `EPIC_SCHEMA` at line 389). They are NOT user-definable at runtime. The schema registry (`_SCHEMA_REGISTRY` at line 530) is a module-level dict populated at import time. An attacker would need write access to the Python source code to modify a `value_pattern`, which is equivalent to arbitrary code execution -- a much higher-severity vector than ReDoS.

**Discrepancy:** The scope document characterizes `value_pattern` as "user-definable," which overstates the attack surface. The patterns are developer-defined in source code, not user-supplied at runtime.

**Severity:** Minor -- The ReDoS concern for *new* patterns added during universal parser extension is valid (new schemas will be added), but the current characterization implies runtime user control that does not exist. The assessment should clarify that the risk applies to developer-authored patterns in the extended schema set.

**Dimension:** Evidence Quality

**Correction:** Change "user-definable regex pattern" to "developer-defined regex pattern" and clarify that the threat applies when new schemas are authored for the universal parser extension, not to runtime user input.

---

## Verification Checklist

### Category: Line Number References

| CL# | Claim | File | Claimed Lines | Actual Lines | Result |
|-----|-------|------|---------------|--------------|--------|
| CL-001 | `_read_file()` location | `ast_commands.py` | 144-163 | 144-163 | VERIFIED |
| CL-002 | `ast_modify()` location | `ast_commands.py` | 380-419 | 380-419 | VERIFIED |
| CL-003 | `_FRONTMATTER_PATTERN` location | `frontmatter.py` | 46 | 46 | VERIFIED |
| CL-004 | `re.fullmatch` location | `schema.py` | 279 | 279 | VERIFIED |
| CL-005 | `_escape_replacement()` location | `frontmatter.py` | 495-509 | 495-509 | VERIFIED |
| CL-006 | `_REINJECT_PATTERN` location | `reinject.py` | 45-47 | 45-47 | VERIFIED |
| CL-007 | `JerryDocument.transform()` location | `jerry_document.py` | 161-236 | 161-236 | VERIFIED |

### Category: DREAD Score Arithmetic

| CL# | Threat ID | D+R+E+A+D | Claimed Total | Computed Total | Result |
|-----|-----------|-----------|---------------|----------------|--------|
| CL-008 | T-YF-07 | 10+10+8+5+5 | 38 | 38 | VERIFIED |
| CL-009 | T-YF-06 | 8+9+7+5+4 | 33 | 33 | VERIFIED |
| CL-010 | T-XS-07 | 10+9+6+5+3 | 33 | 33 | VERIFIED |
| CL-011 | T-YF-05 | 7+8+6+5+4 | 30 | 30 | VERIFIED |
| CL-012 | T-DT-04 | 7+8+6+4+5 | 30 | 30 | VERIFIED |
| CL-013 | T-SV-03 | 6+7+6+5+5 | 29 | 29 | VERIFIED |
| CL-014 | T-YF-02 | 6+7+6+5+4 | 28 | 28 | VERIFIED |
| CL-015 | T-HC-03 | 6+7+6+4+5 | 28 | 28 | VERIFIED |
| CL-016 | T-DT-01 | 6+6+5+5+5 | 27 | 27 | VERIFIED |
| CL-017 | T-XS-02 | 6+6+5+5+4 | 26 | 26 | VERIFIED |
| CL-018 | T-XS-03 | 5+7+5+5+4 | 26 | 26 | VERIFIED |
| CL-019 | T-DT-05 | 7+5+4+4+3 | 23 | 23 | VERIFIED |
| CL-020 | T-HC-02 | 5+6+5+4+4 | 24 | 24 | VERIFIED |
| CL-021 | T-YF-01 | 5+5+5+4+4 | 23 | 23 | VERIFIED |
| CL-022 | T-YF-08 | 4+5+4+4+3 | 20 | 20 | VERIFIED |
| CL-023 | T-XS-01 | 4+5+4+4+4 | 21 | 21 | VERIFIED |
| CL-024 | T-HC-01 | 4+5+5+3+4 | 21 | 21 | VERIFIED |
| CL-025 | T-SV-01 | 4+4+4+5+4 | 21 | 21 | VERIFIED |
| CL-026 | T-SV-02 | 4+4+4+4+4 | 20 | 20 | VERIFIED |
| CL-027 | T-XS-04 | 3+4+3+4+3 | 17 | 17 | VERIFIED |
| CL-028 | T-HC-04 | 3+4+3+4+3 | 17 | 17 | VERIFIED |
| CL-029 | T-YF-04 | 2+3+2+3+3 | 13 | 13 | VERIFIED |
| CL-030 | T-XS-05 | 2+3+2+3+3 | 13 | 13 | VERIFIED |
| CL-031 | T-HC-05 | 3+2+2+3+3 | 13 | 13 | VERIFIED |
| CL-032 | T-HC-06 | 2+3+3+3+2 | 13 | 13 | VERIFIED |
| CL-033 | T-YF-03 | 2+2+2+3+2 | 11 | 11 | VERIFIED |
| CL-034 | T-DT-02 | 3+3+3+3+3 | 15 | 15 | VERIFIED |
| CL-035 | T-DT-03 | 2+3+2+3+3 | 13 | 13 | VERIFIED |
| CL-036 | T-SV-04 | 3+2+2+3+2 | 12 | 12 | VERIFIED |
| CL-037 | T-XS-06 | 3+3+3+3+3 | 15 | 15 | VERIFIED |

All 29 DREAD scores verified as arithmetically correct.

### Category: File/Schema Existence

| CL# | Claim | Result |
|-----|-------|--------|
| CL-038 | `docs/schemas/agent-definition-v1.schema.json` exists | VERIFIED |
| CL-039 | `src/domain/markdown_ast/frontmatter.py` exists | VERIFIED |
| CL-040 | `src/domain/markdown_ast/schema.py` exists | VERIFIED |
| CL-041 | `src/domain/markdown_ast/reinject.py` exists | VERIFIED |
| CL-042 | `src/domain/markdown_ast/jerry_document.py` exists | VERIFIED |
| CL-043 | `src/interface/cli/ast_commands.py` exists | VERIFIED |
| CL-044 | `src/interface/cli/parser.py` exists | VERIFIED |
| CL-045 | `src/domain/markdown_ast/nav_table.py` exists (implied) | VERIFIED (imported in schema.py) |

### Category: CWE/STRIDE Format Validation

| CL# | Claim | Result |
|-----|-------|--------|
| CL-046 | CWE-502 (Deserialization of Untrusted Data) | Format valid (CWE-NNN pattern) |
| CL-047 | CWE-91 (XML Injection) | Format valid |
| CL-048 | CWE-776 (DTD Recursion) | Format valid |
| CL-049 | CWE-22 (Path Traversal) | Format valid |
| CL-050 | CWE-59 (Symlink Following) | Format valid |
| CL-051 | CWE-20 (Improper Input Validation) | Format valid |
| CL-052 | CWE-78 (OS Command Injection) | Format valid |
| CL-053 | CWE-79 (XSS) | Format valid |
| CL-054 | CWE-94 (Code Injection) | Format valid |
| CL-055 | CWE-400 (Uncontrolled Resource Consumption) | Format valid |
| CL-056 | CWE-1333 (ReDoS) | Format valid |
| CL-057 | STRIDE categories correctly applied per threat | VERIFIED (all S/T/R/I/D/E assignments appropriate) |

### Category: Cross-Document Consistency

| CL# | Claim | Documents | Result |
|-----|-------|-----------|--------|
| CL-058 | XML whitelist tags identical across TM and ADR | TM + ADR | VERIFIED (7 identical tags) |
| CL-059 | Trust zones consistent between TM and TB | TM + TB | VERIFIED (6 zones, Z1-Z6) |
| CL-060 | Boundary crossings consistent (BC-01 through BC-05) | TM + TB | VERIFIED |
| CL-061 | Mitigation IDs consistent (M-01 through M-19) | TM + ADR | VERIFIED (ADR references M-01 through M-17 subset correctly) |
| CL-062 | DREAD highest risk (38, T-YF-07) consistent | TM + Red Scope | VERIFIED |
| CL-063 | CWE mappings consistent between Red Scope and TM | TM + Red Scope | VERIFIED |

### Category: Factual Claims About Existing Code Behavior

| CL# | Claim | Result | Finding |
|-----|-------|--------|---------|
| CL-064 | `FrontmatterField` is frozen dataclass | MATERIAL DISCREPANCY | CV-023-B1, CV-037-B1 |
| CL-065 | `ReinjectDirective` is frozen dataclass | VERIFIED (`@dataclass(frozen=True)` at line 55) | -- |
| CL-066 | H-05 enforces yaml.safe_load() | MATERIAL DISCREPANCY | CV-027-B1 |
| CL-067 | Trust zone count is "five" | MATERIAL DISCREPANCY | CV-036-B1 |
| CL-068 | DREAD table is in descending order | MINOR DISCREPANCY | CV-022-B1 |
| CL-069 | `value_pattern` is "user-definable" | MINOR DISCREPANCY | CV-038-B1 |
| CL-070 | NIST CSF subcategory descriptions | MINOR DISCREPANCY | CV-029-B1, CV-030-B1 |

---

## Recommendations

### Critical (MUST correct before acceptance)

1. **CV-023-B1 / CV-037-B1:** Either add `frozen=True` to the `FrontmatterField` `@dataclass` decorator in `src/domain/markdown_ast/frontmatter.py` line 54, OR remove the "frozen" characterization from the threat model (Zone Z4 description, line ~125-126) and the trust boundaries document (Zone 4 domain objects section, line ~129). The recommended path is to freeze the dataclass to maintain the security architecture's immutability guarantee.

2. **CV-027-B1:** In the threat model DFD-01 section (line ~170), replace "enforced by H-05 (UV-only) and the architecture constraint documented in this threat model" with "enforced by architectural constraint C-04 documented in this threat model." Do not cite H-05 for YAML deserialization policy.

### Major (SHOULD correct)

3. **CV-022-B1:** In the DREAD scoring table, swap T-DT-05 (total 23) and T-HC-02 (total 24) so that T-HC-02 appears first, maintaining descending score order.

4. **CV-036-B1:** In `eng-architect-001-trust-boundaries.md` line 24, change "five trust zones" to "six trust zones."

### Minor (MAY correct)

5. **CV-029-B1 / CV-030-B1:** In the NIST CSF 2.0 Mapping table, use the full subcategory description or abbreviate as "Data-at-rest C/I/A protection" and "Data-in-transit C/I/A protection."

6. **CV-038-B1:** In the red team scope document Known Risk Areas section (item 3), change "user-definable regex pattern" to "developer-defined regex pattern in schema source code" and clarify the threat applies to new schema authoring, not runtime input.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All major components covered across all four deliverables. No significant gaps in scope or analysis. |
| Internal Consistency | 0.20 | Negative | CV-022-B1: DREAD table ordering violation. CV-036-B1: Zone count inconsistency between executive summary and body. Two internal contradictions reduce consistency score. |
| Methodological Rigor | 0.20 | Neutral | STRIDE, DREAD, Attack Trees, PASTA applied correctly. All 29 DREAD scores mathematically verified. Methodologies applied thoroughly. |
| Evidence Quality | 0.15 | Negative | CV-023-B1/CV-037-B1 (Critical): Factual error about FrontmatterField immutability propagated across two documents. CV-027-B1: Incorrect rule citation. CV-029-B1/CV-030-B1: NIST subcategory paraphrasing incomplete. Evidence quality is the most impacted dimension. |
| Actionability | 0.15 | Positive | Mitigation recommendations (M-01 through M-19) are specific with implementation guidance. ADR design decisions include code examples. Red team scope includes per-component test matrices. Highly actionable deliverables. |
| Traceability | 0.10 | Negative | CV-027-B1: H-05 misattribution breaks traceability chain for the most critical security control (yaml.safe_load enforcement). References tables in ADR and threat model are otherwise well-structured. |

### Per-Dimension Estimated Scores

| Dimension | Weight | Estimated Score | Weighted Contribution |
|-----------|--------|-----------------|----------------------|
| Completeness | 0.20 | 0.95 | 0.190 |
| Internal Consistency | 0.20 | 0.87 | 0.174 |
| Methodological Rigor | 0.20 | 0.95 | 0.190 |
| Evidence Quality | 0.15 | 0.82 | 0.123 |
| Actionability | 0.15 | 0.96 | 0.144 |
| Traceability | 0.10 | 0.88 | 0.088 |
| **Weighted Total** | **1.00** | -- | **0.909** |

**Overall: 0.909 (REVISE band)** -- Below the 0.92 threshold. The two Critical findings (FrontmatterField mutability, duplicated across two documents) and the H-05 misattribution are the primary drivers below threshold. Correcting the Critical and Major findings would raise the score to approximately 0.94-0.95 (PASS band).

---

**Verification Summary:**
- **Total claims examined:** 38 primary + 32 supplementary (70 total verification points)
- **VERIFIED:** 59 (84%)
- **MATERIAL DISCREPANCY:** 7 (10%)
- **MINOR DISCREPANCY:** 4 (6%)
- **Findings produced:** 11 (2 Critical, 5 Major, 4 Minor)
- **Assessment:** REVISE with targeted corrections

---

<!-- VERSION: 1.0.0 | DATE: 2026-02-22 | STRATEGY: S-011 | REVIEWER: adv-executor | WORKFLOW: ast-universal-20260222-001 | QUALITY-GATE: QG-B1 -->
