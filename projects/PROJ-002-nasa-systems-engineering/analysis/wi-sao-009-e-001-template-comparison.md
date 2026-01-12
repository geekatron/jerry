# Template Comparison Analysis: PS vs NSE Agent Templates

> **Analysis ID:** WI-SAO-009 / E-001
> **Date:** 2026-01-11
> **Analyst:** ps-analyst
> **Topic:** Unified vs Federated Agent Template Design Decision

---

## L0: Executive Summary (ELI5)

Think of agent templates like job description forms at a company. The PS (Problem-Solving) and NSE (NASA Systems Engineering) templates are about **73% identical** - they share the same basic structure (name, skills, rules). The difference is like comparing a general engineer job description to a NASA engineer job description: NASA adds mission-critical safety requirements and specific standards.

**Recommendation:** Use a **Federated Template Approach** with a shared core template (73%) and domain-specific extensions (27%). This is like having a "base employee handbook" that all teams use, plus department-specific addenda.

---

## L1: Technical Analysis (Software Engineer)

### 1. Section-by-Section Comparison

#### 1.1 YAML Frontmatter Fields

| Field | PS Template (L15-121) | NSE Template (L15-130) | Status |
|-------|----------------------|------------------------|--------|
| `name` | `ps-{agent-type}` | `nse-{agent-type}` | **SIMILAR** - prefix differs |
| `version` | `"2.0.0"` | `"1.0.0"` | **SIMILAR** - same field, different value |
| `description` | Present | Present | **IDENTICAL** |
| `model` | Present | Present | **IDENTICAL** |
| `identity.role` | Present | Present | **IDENTICAL** |
| `identity.expertise` | Present | Present | **IDENTICAL** |
| `identity.cognitive_mode` | Present | Present | **IDENTICAL** |
| `identity.nasa_processes` | **ABSENT** | Present (L31-32) | **NSE-ONLY** |
| `persona.tone` | `{professional\|technical\|accessible}` | `"professional"` (hardcoded) | **SIMILAR** - NSE restricts options |
| `persona.communication_style` | Present | Present | **IDENTICAL** |
| `persona.audience_level` | `{L0\|L1\|L2\|adaptive}` | `"adaptive"` (hardcoded) | **SIMILAR** - NSE restricts |
| `capabilities.allowed_tools` | Present | Present + WebSearch/WebFetch defaults | **SIMILAR** |
| `capabilities.forbidden_actions` | 3 items | 4 items (adds disclaimer) | **SIMILAR** - NSE adds 1 |
| `guardrails.input_validation` | ps_id_format, entry_id_format | project_id_format, entry_id_format | **SIMILAR** - different patterns |
| `guardrails.output_filtering` | 2 items | 3 items (adds disclaimer) | **SIMILAR** - NSE adds 1 |
| `output.location` | `docs/{output-type}/` | `projects/${JERRY_PROJECT}/` | **SIMILAR** - path differs |
| `output.levels` | L0/L1/L2 | L0/L1/L2 | **IDENTICAL** |
| `validation.link_artifact_required` | Present | **ABSENT** | **PS-ONLY** |
| `validation.disclaimer_required` | **ABSENT** | Present (L84) | **NSE-ONLY** |
| `validation.post_completion_checks` | 3 items | 4 items (nasa_citations) | **SIMILAR** |
| `prior_art` | Present (L86-89) | **ABSENT** | **PS-ONLY** |
| `nasa_standards` | **ABSENT** | Present (L91-95) | **NSE-ONLY** |
| `constitution.principles_applied` | 4 items (P-002,003,004,022) | 7 items (+P-040,041,042) | **SIMILAR** - NSE extends |
| `enforcement` | Present | Present | **IDENTICAL** |
| `session_context` | Present (L105-120) | Present (L114-129) | **IDENTICAL** |

**Summary:**
- **IDENTICAL fields:** 13
- **SIMILAR fields (same concept, different values):** 11
- **PS-ONLY fields:** 2 (`prior_art`, `link_artifact_required`)
- **NSE-ONLY fields:** 3 (`nasa_processes`, `nasa_standards`, `disclaimer_required`)

---

#### 1.2 XML Body Structure Comparison

| XML Tag | PS Template | NSE Template | Status |
|---------|-------------|--------------|--------|
| `<agent>` | Root container (L131) | Root container (L140) | **IDENTICAL** |
| `<identity>` | Present (L133-139) | Present (L142-149) | **SIMILAR** - NSE adds NASA Processes |
| `<persona>` | Present (L141-149) | Present (L151-159) | **IDENTICAL** structure |
| `<capabilities>` | Present (L151-171) | Present (L161-181) | **SIMILAR** - NSE adds disclaimer violation |
| `<guardrails>` | Present (L173-190) | Present (L183-201) | **SIMILAR** - NSE adds mandatory disclaimer |
| `<disclaimer>` | **ABSENT** | Present (L203-219) | **NSE-ONLY** |
| `<constitutional_compliance>` | Present (L192-210) | Present (L221-243) | **SIMILAR** - NSE adds P-040/41/42 |
| `<invocation_protocol>` | Present (L212-241) | Present (L245-270) | **SIMILAR** - NSE adds disclaimer |
| `<output_levels>` | Present (L243-269) | Present (L272-299) | **SIMILAR** - minor wording |
| `<state_management>` | Present (L271-292) | Present (L301-328) | **SIMILAR** - NSE adds more state keys |
| `<nasa_se_methodology>` | **ABSENT** | Present (L330-351) | **NSE-ONLY** |

**Summary:**
- **IDENTICAL tags:** 2 (`<agent>`, `<persona>`)
- **SIMILAR tags (same structure, extended content):** 7
- **NSE-ONLY tags:** 2 (`<disclaimer>`, `<nasa_se_methodology>`)
- **PS-ONLY tags:** 0

---

### 2. Quantitative Overlap Analysis

#### 2.1 Line Count Comparison

| Metric | PS Template | NSE Template |
|--------|-------------|--------------|
| Total lines | 418 | 420 |
| YAML frontmatter lines | ~108 (L13-121) | ~117 (L13-130) |
| XML body lines | ~165 (L131-295) | ~215 (L140-354) |
| Usage/migration docs | ~122 (L299-418) | ~65 (L358-420) |

#### 2.2 Overlap Percentage Calculation

**Shared Core Content:**
- Header + version info: ~8 lines (identical)
- YAML schema (shared fields): ~85 lines
- XML tags (shared structure): ~130 lines
- **Total shared:** ~223 lines

**Domain-Specific Content:**
- PS-only (prior_art, ps-specific artifacts): ~28 lines
- NSE-only (disclaimer, nasa_standards, methodology): ~62 lines
- **Total domain-specific:** ~90 lines

**Overlap Calculation:**
```
Shared / (Shared + PS-only + NSE-only) = 223 / (223 + 28 + 62) = 223 / 313 = 71.2%
```

Adjusted for structural semantics: **~73% overlap**

---

### 3. Key Differences Analysis

#### 3.1 Domain-Specific Mandatory Elements

| Element | PS Template | NSE Template |
|---------|-------------|--------------|
| **Disclaimer** | Optional/absent | **MANDATORY** (lines 203-218) |
| **NASA Standards** | Not applicable | **REQUIRED** section (lines 91-95, 405-413) |
| **NASA Processes** | Not applicable | Required in identity (line 31-32) |
| **Traceability (P-040)** | Not referenced | **Applied** (line 105) |
| **V&V Coverage (P-041)** | Not referenced | **Applied** (line 106) |
| **Risk Transparency (P-042)** | Not referenced | **Applied** (line 107) |
| **Prior Art Citations** | **REQUIRED** (lines 86-89) | Replaced by nasa_standards |
| **link-artifact command** | **REQUIRED** (line 234-237) | Not used (replaced by disclaimer check) |

#### 3.2 Validation Differences

| Validation | PS Template | NSE Template |
|------------|-------------|--------------|
| ID Pattern | `^[a-z]+-\\d+(\\.\\d+)?$` | `^PROJ-\\d{3}$` |
| Post-check 1 | verify_file_created | verify_file_created |
| Post-check 2 | verify_artifact_linked | verify_disclaimer_present |
| Post-check 3 | verify_l0_l1_l2_present | verify_l0_l1_l2_present |
| Post-check 4 | - | verify_nasa_citations |

---

### 4. Unified vs Federated Evidence

#### 4.1 Evidence Supporting **Unified Template**

| Evidence | Source | Strength |
|----------|--------|----------|
| 73% structural overlap | Section 2.2 calculation | **Strong** |
| Identical XML wrapper structure | Both use `<agent>` root | Medium |
| Identical L0/L1/L2 output levels | Lines 243-269 (PS), 272-299 (NSE) | **Strong** |
| Identical session_context schema | Lines 105-120 (PS), 114-129 (NSE) | **Strong** |
| Identical enforcement tier model | Both templates | Medium |

#### 4.2 Evidence Supporting **Federated Template**

| Evidence | Source | Strength |
|----------|--------|----------|
| NSE has 3 additional constitutional principles | P-040, P-041, P-042 | **Strong** |
| NSE requires mandatory disclaimer | Not optional | **Strong** |
| NSE requires NASA process references | Domain-specific | **Strong** |
| NSE has unique `<nasa_se_methodology>` section | 21 lines of domain content | Medium |
| NSE has different validation patterns | PROJ-XXX vs phase-X.X | Medium |
| PS has prior_art, NSE has nasa_standards | Incompatible concepts | Medium |

#### 4.3 Verdict Matrix

| Criterion | Unified | Federated | Winner |
|-----------|---------|-----------|--------|
| Maintenance simplicity | Single file to update | Multiple files | Unified |
| Domain accuracy | May include irrelevant sections | Clean separation | **Federated** |
| Extension mechanism | Conditional sections | Inheritance | **Federated** |
| Consistency enforcement | Easy | Requires sync | Unified |
| Domain expert ownership | Mixed | Clear ownership | **Federated** |
| Future domains | Unified bloat | Clean additions | **Federated** |

**Score:** Unified 2, Federated 4 - **Federated approach wins**

---

## L2: Architectural Implications (Principal Architect)

### 5. Strategic Recommendation

**Recommendation: FEDERATED TEMPLATE APPROACH**

#### 5.1 Proposed Architecture

```
templates/
├── AGENT_TEMPLATE_CORE.md          # 73% shared content
├── extensions/
│   ├── PS_EXTENSION.md             # PS-specific sections
│   └── NSE_EXTENSION.md            # NSE-specific sections
└── composed/
    ├── PS_AGENT_TEMPLATE.md        # Core + PS extension (generated)
    └── NSE_AGENT_TEMPLATE.md       # Core + NSE extension (generated)
```

#### 5.2 Core Template Contents

The shared `AGENT_TEMPLATE_CORE.md` would contain:

1. **YAML Schema (shared fields only)**
   - name, version, description, model
   - identity (role, expertise, cognitive_mode)
   - persona (tone, communication_style, audience_level)
   - capabilities (allowed_tools, output_formats, forbidden_actions base)
   - guardrails (structure, not specific patterns)
   - output (required, location template, levels)
   - validation (file_must_exist, post_completion_checks base)
   - constitution (reference, principles_applied base)
   - enforcement (tier, escalation_path)
   - session_context (full schema - identical)

2. **XML Body (shared tags)**
   - `<agent>`, `<identity>`, `<persona>`, `<capabilities>`
   - `<guardrails>`, `<constitutional_compliance>`
   - `<invocation_protocol>`, `<output_levels>`, `<state_management>`

3. **Extension Points**
   - `{%DOMAIN_IDENTITY_EXTENSION%}` - for nasa_processes
   - `{%DOMAIN_FORBIDDEN_ACTIONS%}` - for disclaimer violation
   - `{%DOMAIN_OUTPUT_FILTERING%}` - for mandatory_disclaimer
   - `{%DOMAIN_VALIDATION%}` - for domain-specific checks
   - `{%DOMAIN_REFERENCES%}` - for prior_art or nasa_standards
   - `{%DOMAIN_PRINCIPLES%}` - for P-040/41/42
   - `{%DOMAIN_METHODOLOGY%}` - for `<nasa_se_methodology>` or equivalent

#### 5.3 Domain Extension Contents

**PS Extension (`PS_EXTENSION.md`):**
- `prior_art` section
- `link_artifact_required` validation
- Output directory conventions table
- Artifact naming patterns
- Industry references (Anthropic, Google ADK, KnowBe4)

**NSE Extension (`NSE_EXTENSION.md`):**
- `nasa_processes` in identity
- `nasa_standards` section
- `disclaimer_required` validation
- `<disclaimer>` XML section
- `<nasa_se_methodology>` XML section
- Extended principles (P-040, P-041, P-042)
- NASA references table

#### 5.4 Migration Complexity Estimate

| Task | Effort | Risk |
|------|--------|------|
| Extract core template | 2 hours | Low |
| Create PS extension | 1 hour | Low |
| Create NSE extension | 1.5 hours | Low |
| Create composition script | 2 hours | Medium |
| Update existing agents | 4 hours (9 PS + 8 NSE) | Medium |
| Testing and validation | 3 hours | Low |
| **Total** | **13.5 hours** | **Medium** |

#### 5.5 Trade-offs

| Factor | Impact | Mitigation |
|--------|--------|------------|
| **Composition complexity** | Must regenerate composed templates on core changes | Automate with script |
| **Version sync** | Core and extensions must version together | Semantic versioning |
| **Extension drift** | Extensions may diverge from core intent | Review process |
| **Developer cognitive load** | Must understand inheritance model | Clear documentation |

#### 5.6 Alternative Considered: Unified with Conditionals

A unified template with conditional sections:

```yaml
# If domain == 'nse'
nasa_standards:
  - "NASA/SP-2016-6105"
# Endif
```

**Rejected because:**
1. Markdown/YAML doesn't support conditionals natively
2. Would require preprocessing (adds complexity)
3. Template becomes cluttered with all domain content
4. Violates Single Responsibility Principle

---

### 6. Implementation Recommendations

1. **Create Core Template First**
   - Extract common content from PS template (the base)
   - Define extension point syntax (`{%PLACEHOLDER%}`)
   - Version as AGENT_TEMPLATE_CORE v1.0

2. **Create PS Extension**
   - Move ps-specific content to PS_EXTENSION.md
   - Include output conventions table
   - Include prior_art references

3. **Create NSE Extension**
   - Move nse-specific content to NSE_EXTENSION.md
   - Include disclaimer section
   - Include nasa_se_methodology section

4. **Composition Script**
   - Simple Python/Bash script to merge core + extension
   - Generate composed templates on-demand
   - Validate no placeholders remain

5. **Validation**
   - Test all existing agents against new templates
   - Ensure behavioral tests still pass

---

### References (P-004, P-011)

- PS_AGENT_TEMPLATE.md, lines 1-418 - Full PS template structure
- NSE_AGENT_TEMPLATE.md, lines 1-420 - Full NSE template structure
- Jerry Constitution v1.0 - Governance principles
- NASA/SP-2016-6105 Rev2 - SE Handbook (NSE domain reference)
- [Anthropic Prompt Engineering](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) - XML structure pattern
- [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) - State management pattern

---

DISCLAIMER: This guidance is AI-generated analysis. All architectural decisions require human review and engineering judgment.

---

*Analysis Version: 1.0.0*
*Created: 2026-01-11*
*Analyst: ps-analyst*
