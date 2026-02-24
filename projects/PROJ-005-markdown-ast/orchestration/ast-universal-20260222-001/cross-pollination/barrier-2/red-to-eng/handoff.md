# Barrier 2 Handoff: Red Team → Engineering

> **From:** red-vuln-001 (RED Phase 2)
> **To:** eng-qa-001, eng-security-001 (ENG Phase 4-5)
> **Barrier:** barrier-2
> **Criticality:** C4
> **Confidence:** 0.88

---

## Key Findings (Orientation)

1. **27 vulnerabilities identified** across existing code (7), planned extensions (12), and threat model gaps (8) -- 2 Critical (DREAD >= 40), 8 High (DREAD 30-39)
2. **YAML deserialization is the #1 risk** (RV-001, DREAD 42, CWE-502) -- safe_load() enforcement is the single most critical mitigation; any bypass is a code execution vector
3. **L2-REINJECT governance injection is #2 risk** (RV-002, DREAD 41, CWE-94) -- ability to inject governance directives via HTML comments in untrusted files could manipulate agent behavior
4. **Path traversal confirmed in existing CLI** (RV-003, DREAD 37, CWE-22) -- _read_file() has zero containment; M-08 implementation critical
5. **8 additional threats not in original threat model** -- including schema poisoning via concurrent registration, mutable domain object exposure, and type detection confusion

## Artifacts

| Artifact | Path | Purpose |
|----------|------|---------|
| Vulnerability Assessment | `orchestration/ast-universal-20260222-001/red/phase-2-vulnerability/red-vuln-001/red-vuln-001-vulnerability-assessment.md` | Full 27-finding report with DREAD scores, CWE mappings, attack vectors |

## Engineering Implications

### Critical Findings Requiring Immediate Verification

| ID | Finding | DREAD | CWE | Engineering Action |
|----|---------|-------|-----|--------------------|
| RV-001 | YAML Deserialization Chain | 42 | CWE-502 | Verify M-01 (safe_load only) has zero bypass paths. Test yaml.load() blocked in all code paths. Verify S506 ruff rule catches all variants. |
| RV-002 | L2-REINJECT Governance Injection | 41 | CWE-94 | Verify M-13 (case-insensitive exclusion) handles Unicode folding. Verify M-22 (trusted path whitelist) prevents untrusted files from injecting directives. Test html_comment.py L2-REINJECT filter comprehensively. |
| RV-003 | Path Traversal in CLI | 37 | CWE-22 | Verify M-08 (path containment) in _resolve_and_check_path() handles: symlinks, double-encoding, null bytes, relative paths, UNC paths. Verify JERRY_DISABLE_PATH_CONTAINMENT env var cannot be set in production. |

### High Findings for Test Strategy

| ID | Finding | DREAD | Component | Test Focus |
|----|---------|-------|-----------|------------|
| RV-004 | ReDoS via Schema value_pattern | 35 | schema.py | Craft adversarial regex inputs for all value_pattern fields in 10 schemas |
| RV-005 | Schema Registry Poisoning | 34 | schema_registry.py | Verify freeze() prevents post-initialization mutation; test concurrent registration |
| RV-006 | XML Tag Injection Beyond Allowlist | 33 | xml_section.py | Test tag names with Unicode, embedded null bytes, case variations |
| RV-007 | YAML Billion Laughs (Alias Expansion) | 33 | yaml_frontmatter.py | Test M-20 (max 100 aliases) with nested alias chains approaching memory limits |
| RV-008 | YAML Deep Nesting Stack Overflow | 30 | yaml_frontmatter.py | Test depth limit enforcement; verify stack overflow protection |
| RV-009 | HTML Comment Metadata Injection | 30 | html_comment.py | Test `-->` within values, comment nesting, incomplete comments |
| RV-010 | Write-Back TOCTOU | 30 | ast_commands.py | Test race condition between path check and atomic write |
| RV-011 | Document Type Confusion | 30 | document_type.py | Test path spoofing combined with conflicting structural cues |

### Threat Model Gap Areas (New Threats Not in Original Model)

| Gap | Description | Recommendation |
|-----|-------------|----------------|
| TG-001 | Schema poisoning via race condition on registry | Ensure freeze() is called before any external input processing |
| TG-002 | Mutable domain object exposure through shallow copy | Verify all domain objects use frozen dataclass or return deep copies |
| TG-003 | Type detection confusion leading to wrong parser | Add explicit validation that detected type matches parser assumptions |
| TG-004 | Error message information disclosure | Audit all exception handlers for sensitive path/content leakage |
| TG-005 | YAML multi-document attack | Verify only first document is processed in multi-document streams |
| TG-006 | HTML comment unclosed tag DoS | Test resource consumption with unclosed `<!--` comments |
| TG-007 | XML section regex catastrophic backtracking | Test ReDoS-specific inputs against xml_section.py patterns |
| TG-008 | Universal document cascade failure | Test error propagation when one parser fails during multi-parser dispatch |

### DREAD Score Disagreements with Threat Model

6 findings where red-vuln-001 scored higher than eng-architect-001:

| Finding | Eng Score | Red Score | Delta | Disagreement Basis |
|---------|-----------|-----------|-------|--------------------|
| RV-001 (YAML deser) | 38 | 42 | +4 | Chain attack potential underestimated |
| RV-003 (Path traversal) | 30 | 37 | +7 | CI/CD impact not considered |
| RV-004 (ReDoS) | 29 | 35 | +6 | Schema validation ubiquity increases affected users |
| RV-005 (Schema poisoning) | N/A | 34 | New | Not in original threat model |
| RV-002 (L2-REINJECT) | N/A | 41 | New | Not in original threat model |
| RV-009 (HTML comment) | 26 | 30 | +4 | Comment nesting complexity underestimated |

## Testing Priorities for eng-qa-001

Based on findings, recommend test focus in this order:

1. **YAML safe_load enforcement** -- zero tolerance for unsafe deserialization paths
2. **Path containment** -- comprehensive path traversal test suite (symlinks, encoding, race)
3. **L2-REINJECT isolation** -- governance directive injection prevention
4. **Input bounds enforcement** -- boundary value testing at all limits
5. **Schema registry immutability** -- freeze() enforcement, concurrent access
6. **Parser robustness** -- malformed, oversized, adversarial inputs across all 3 new parsers
7. **Error handling** -- no sensitive data leakage in any error path

## Blockers

None.

---

> *Handoff generated by orchestrator for Barrier 2 cross-pollination.*
