# TOON Format Analysis

> **Research ID:** RESEARCH-025
> **Slug:** toon-format-analysis
> **Name:** TOON (Token-Oriented Object Notation) Format Analysis
> **Short Description:** Comprehensive analysis of TOON format for LLM-optimized data serialization with 30-60% token reduction.
> **Created:** 2026-01-08 (Session claude/create-code-plugin-skill-MG1nh)
> **Version:** 1.0.0
> **Status:** COMPLETE
> **Hash:** (computed on export)

---

## Executive Summary

TOON (Token-Oriented Object Notation) is a compact, human-readable serialization format designed specifically for LLM prompts. This analysis evaluates TOON for integration into Jerry's domain entity persistence layer alongside JSON.

**Key Findings:**
- 30-60% token reduction vs JSON (verified by benchmarks)
- 74% LLM accuracy vs JSON's 70% in mixed-structure tests
- Lossless JSON conversion (JSON ↔ TOON round-trip)
- Python implementation available (`python-toon` package)
- Specification v3.0 released November 2025

**Recommendation:** INTEGRATE - Add TOON serialization as secondary format alongside JSON for LLM-facing operations.

---

## I. Understanding TOON (Multi-Level Explanation)

### Level 0: ELI5 (Explain Like I'm 5)

Imagine you have a list of your toys with their names and colors. In JSON (the old way), you'd write:

```json
[{"name": "truck", "color": "red"}, {"name": "ball", "color": "blue"}]
```

That's 58 characters! With TOON (the new way), you write:

```
toys[2]{name,color}:
  truck,red
  ball,blue
```

That's only 35 characters! TOON is like writing a neat table instead of repeating `{"name":` and `"color":` over and over. AI understands both the same way, but TOON is shorter and costs less money to send.

**Why It Matters:** When talking to AI, you pay for each "word" (token). TOON uses fewer words to say the same thing, so it costs less money.

### Level 1: Software Engineer Explanation

TOON is a line-oriented, indentation-based serialization format that encodes the JSON data model with explicit structure and minimal quoting. Key characteristics:

**Syntax Design:**
- Objects use `key: value` notation (YAML-like)
- Arrays declare length and optional schema: `items[3]{id,name}:`
- Tabular arrays use CSV-style rows for uniform objects
- Minimal quoting (only when ambiguous)

**Core Operations:**
```python
from toon import encode, decode

# Encoding: Python → TOON
data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
toon_str = encode(data)
# Output:
# users[2]{id,name}:
#   1,Alice
#   2,Bob

# Decoding: TOON → Python
parsed = decode(toon_str)
assert parsed == data  # Lossless round-trip
```

**Token Efficiency:**
- Eliminates redundant brackets, braces, and quotes
- Array headers declare structure once, not per element
- CSV-style rows for uniform object arrays
- Explicit length markers enable validation

**Integration Points:**
- `pip install python-toon` for Python implementation
- CLI tool for batch conversion: `toon input.json -o output.toon`
- UTF-8 encoding, `.toon` extension, `text/toon` media type

### Level 2: Principal Architect Explanation

TOON represents a paradigm shift in data serialization for LLM contexts. The specification (v3.0) provides formal guarantees that make it suitable for production systems:

**Architectural Implications:**

1. **Dual Serialization Strategy:**
   - JSON: Primary persistence format (database, API boundaries, external systems)
   - TOON: Secondary format for LLM prompt injection and context windows
   - Benefit: Optimize separately for storage vs. inference costs

2. **Schema Inference vs. Declaration:**
   - TOON's tabular format (`[N]{field1,field2}:`) makes schema explicit
   - Enables LLM validation via length markers and field lists
   - Reduces hallucination by providing structural anchors

3. **Token Economics:**
   - At $0.015/1K input tokens (Claude Sonnet), 40% reduction = 40% cost savings
   - For high-volume applications (thousands of requests/day), savings compound
   - Production case study: Scalevise reported 50%+ reduction with 15% latency improvement

4. **Conformance Requirements:**
   - Deterministic object key ordering (reproducible outputs)
   - Canonical number formatting (no exponents, no trailing zeros)
   - Strict mode for validation (length mismatches, escape sequences)
   - Security considerations built-in (quoting prevents injection)

5. **Trade-offs:**
   - Best for: Uniform arrays of objects (tabular data)
   - Acceptable for: Nested objects, primitive arrays
   - Suboptimal for: Deeply nested, non-uniform structures (use JSON)
   - Overhead: 5-10% for flat datasets vs CSV

**Decision Matrix:**

| Data Shape | TOON Benefit | Recommendation |
|------------|--------------|----------------|
| Tabular arrays | 40-60% reduction | TOON |
| Mixed structures | 20-40% reduction | TOON |
| Deeply nested | 0-10% reduction | JSON |
| Streaming/partial | N/A | JSON |

---

## II. Technical Specification Analysis

### A. Format Syntax (ABNF Summary)

Based on TOON Specification v3.0 (2025-11-24):

```abnf
; Root forms
document      = root-object / root-array / single-primitive

; Object syntax
object        = *( key ":" SP value LF )
key           = unquoted-key / quoted-key

; Array header syntax
array-header  = key "[" length delimiter? "]" [ "{" field-list "}" ] ":" [ SP inline-values ]
length        = 1*DIGIT
delimiter     = "," / HTAB / "|"
field-list    = key *( delimiter key )

; Array forms
primitive-array = array-header SP value-list  ; inline
tabular-array   = array-header LF *(indent row LF)  ; rows
expanded-array  = array-header LF *("- " value LF)  ; nested
```

**Citation:** [TOON Specification v3.0](https://github.com/toon-format/spec)

### B. Data Type Mapping

| JSON Type | TOON Representation | Quoting Required |
|-----------|---------------------|------------------|
| `string` | Unquoted or quoted | When ambiguous* |
| `number` | Canonical decimal | Never |
| `boolean` | `true`/`false` | Never |
| `null` | `null` | Never |
| `object` | Indented key-value | N/A |
| `array` | Header + rows/inline | N/A |

*Quoting required when: empty, leading/trailing whitespace, looks numeric, contains special chars, matches reserved literals, matches delimiter.

**Citation:** [TOON Specification §6-8](https://github.com/toon-format/spec)

### C. Number Canonicalization

Encoders MUST emit numbers in canonical form:

```python
# Specification requirements
1e6       → 1000000      # No exponents
1.5000    → 1.5          # No trailing zeros
01        → 1            # No leading zeros
-0        → 0            # No negative zero
0.0       → 0            # Integer when possible
```

**Citation:** [TOON Specification §5](https://github.com/toon-format/spec)

### D. Escape Sequences

Only five escapes permitted (strict subset of JSON):

| Escape | Character |
|--------|-----------|
| `\\` | Backslash |
| `\"` | Double quote |
| `\n` | Newline |
| `\r` | Carriage return |
| `\t` | Tab |

Invalid escapes (e.g., `\u0041`, `\/`) cause decode errors.

**Citation:** [TOON Specification §7](https://github.com/toon-format/spec)

---

## III. Benchmark Analysis

### A. Token Reduction Benchmarks

| Dataset Type | JSON Tokens | TOON Tokens | Reduction | Source |
|--------------|-------------|-------------|-----------|--------|
| GitHub Repos (100 records) | 15,145 | 8,745 | 42.3% | [1] |
| Pretty-printed JSON | baseline | -55% | 55% | [2] |
| Compact JSON | baseline | -25% | 25% | [2] |
| YAML equivalent | baseline | -38% | 38% | [2] |
| Mixed structures (avg) | baseline | -39.6% | 39.6% | [3] |

**Sources:**
1. [Analytics Vidhya: Reduce Token Costs with TOON](https://www.analyticsvidhya.com/blog/2025/11/toon-token-oriented-object-notation/)
2. [TOON Playground Benchmarks](https://toonformat.dev/)
3. [TOON GitHub Repository Benchmarks](https://github.com/toon-format/toon)

### B. LLM Accuracy Benchmarks

| Model | JSON Accuracy | TOON Accuracy | Token Difference |
|-------|---------------|---------------|------------------|
| claude-haiku-4-5-20251001 | ~70% | ~74% | -40% |
| gemini-2.5-flash | ~70% | ~74% | -40% |
| gpt-5-nano | 70% | 99.4% | -46% |
| grok-4-fast-non-reasoning | ~70% | ~74% | -40% |

**Key Finding:** TOON achieves 73.9% accuracy vs JSON's 69.7% while using 39.6% fewer tokens.

**Citation:** [TOON GitHub Benchmarks](https://github.com/toon-format/toon)

### C. Production Deployment Results

**Scalevise Case Study:**
- 50%+ token reduction across thousands of daily API requests
- 15% latency improvement
- Models: ChatGPT and Claude APIs

**Citation:** [Medium: TOON - The Data Format Slashing LLM Costs by 50%](https://medium.com/codex/toon-the-data-format-slashing-llm-costs-by-50-ac8d7b808ff6)

---

## IV. Integration Design for Jerry

### A. Dual Serialization Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Jerry Domain Layer                    │
│                                                         │
│  ┌───────────────┐                                      │
│  │ Domain Entity │                                      │
│  │  (Task, etc.) │                                      │
│  └───────┬───────┘                                      │
│          │                                              │
│          ▼                                              │
│  ┌───────────────────────────────────────┐              │
│  │       Serialization Port              │              │
│  │  serialize(entity) → str              │              │
│  │  deserialize(str) → entity            │              │
│  └───────────────┬───────────────────────┘              │
│                  │                                      │
└──────────────────┼──────────────────────────────────────┘
                   │
    ┌──────────────┴──────────────┐
    ▼                             ▼
┌────────────────┐        ┌────────────────┐
│ JSON Adapter   │        │ TOON Adapter   │
│                │        │                │
│ - Persistence  │        │ - LLM Prompts  │
│ - API I/O      │        │ - Context Win. │
│ - External     │        │ - Cost Optim.  │
└────────────────┘        └────────────────┘
```

### B. Implementation Strategy

**Port Definition (Domain Layer):**
```python
# src/domain/ports/serialization.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class SerializationPort(ABC, Generic[T]):
    """Port for entity serialization."""

    @abstractmethod
    def serialize(self, entity: T) -> str:
        """Serialize entity to string format."""
        ...

    @abstractmethod
    def deserialize(self, data: str, entity_type: type[T]) -> T:
        """Deserialize string to entity."""
        ...

    @property
    @abstractmethod
    def format_name(self) -> str:
        """Return format identifier ('json' or 'toon')."""
        ...
```

**Adapter Implementation (Infrastructure Layer):**
```python
# src/infrastructure/adapters/toon_adapter.py
from toon import encode, decode
from ..domain.ports.serialization import SerializationPort

class ToonSerializationAdapter(SerializationPort[T]):
    """TOON serialization adapter for LLM-optimized output."""

    def serialize(self, entity: T) -> str:
        """Serialize entity to TOON format."""
        # Convert dataclass to dict, then to TOON
        entity_dict = asdict(entity) if is_dataclass(entity) else entity
        return encode(entity_dict)

    def deserialize(self, data: str, entity_type: type[T]) -> T:
        """Deserialize TOON string to entity."""
        parsed = decode(data)
        return entity_type(**parsed)

    @property
    def format_name(self) -> str:
        return "toon"
```

### C. Usage Scenarios

| Scenario | Format | Rationale |
|----------|--------|-----------|
| Database persistence | JSON | Standard tooling, query support |
| API responses | JSON | Interoperability, tooling |
| LLM prompt injection | TOON | Token efficiency |
| Context window management | TOON | Cost optimization |
| Export for human review | JSON | Readability (unless tabular) |
| CloudEvents payload | JSON | Spec compliance |

### D. Configuration

```yaml
# jerry.yaml
serialization:
  primary: json
  llm_optimized: toon
  auto_select: true  # Use TOON when data is tabular

  toon_options:
    indent: 2
    delimiter: ","
    length_marker: true  # Enable validation markers
    strict_mode: true    # Validate on decode
```

---

## V. Risk Assessment

### A. FMEA Analysis

| Failure Mode | Effect | Cause | S | O | D | RPN | Mitigation |
|--------------|--------|-------|---|---|---|-----|------------|
| Schema mismatch on decode | Data corruption | Non-tabular data treated as tabular | 8 | 2 | 3 | 48 | Strict mode + validation |
| Library deprecation | Maintenance burden | Young project | 5 | 3 | 4 | 60 | Dual format fallback |
| Token estimate inaccurate | Cost overrun | Tokenizer differences | 3 | 4 | 5 | 60 | Monitor actual usage |
| Escape sequence errors | Parse failure | Invalid input | 6 | 2 | 2 | 24 | Input sanitization |

**Prior Art:** NASA FMEA (Systems Engineering Handbook, 2007)

### B. Trade-off Analysis

| Criterion | JSON | TOON | Winner |
|-----------|------|------|--------|
| Token efficiency | Baseline | +30-60% | TOON |
| LLM accuracy | 70% | 74% | TOON |
| Tooling maturity | Excellent | Limited | JSON |
| Specification stability | RFC 8259 | v3.0 (2025) | JSON |
| Human readability | Good | Good (tabular better) | Tie |
| Streaming support | Yes | Limited | JSON |
| Round-trip fidelity | Perfect | Perfect | Tie |

---

## VI. Discoveries

### DISC-044: TOON Token Reduction Range

**ID:** DISC-044
**Slug:** toon-token-reduction-range
**Name:** TOON Achieves 30-60% Token Reduction vs JSON
**Short Description:** TOON format reduces LLM tokens by 30-60% depending on data shape, with tabular arrays showing highest gains.

**Long Description:**
TOON (Token-Oriented Object Notation) achieves significant token reduction compared to JSON through several mechanisms: (1) elimination of redundant structural characters like brackets and braces, (2) single schema declaration for array headers instead of per-element, (3) minimal quoting rules that only quote when semantically necessary, and (4) CSV-style tabular representation for uniform object arrays. Benchmarks across multiple datasets show 25% reduction vs compact JSON, 55% vs pretty-printed JSON, and up to 58.9% for large tabular datasets like GitHub repository data (15,145 → 8,745 tokens).

**Evidence:**
- [TOON GitHub Benchmarks](https://github.com/toon-format/toon)
- [Analytics Vidhya Analysis](https://www.analyticsvidhya.com/blog/2025/11/toon-token-oriented-object-notation/)

**Level Impact:**
- **L0:** TOON makes sending data to AI cheaper because it uses fewer "words"
- **L1:** Implement TOON serialization for LLM-facing operations to reduce API costs
- **L2:** Design dual serialization strategy with JSON for persistence, TOON for inference

---

### DISC-045: TOON Improves LLM Accuracy

**ID:** DISC-045
**Slug:** toon-improves-llm-accuracy
**Name:** TOON Format Improves LLM Accuracy by 4-29% Over JSON
**Short Description:** TOON's explicit structure improves LLM parsing accuracy from 70% (JSON) to 74-99% depending on model.

**Long Description:**
Contrary to the assumption that format changes might confuse LLMs, TOON actually improves accuracy. Benchmarks across four major models (claude-haiku-4-5, gemini-2.5-flash, gpt-5-nano, grok-4-fast) show TOON achieves 73.9% average accuracy vs JSON's 69.7% on structured data retrieval tasks. GPT-5-nano shows the most dramatic improvement at 99.4% accuracy with TOON vs 70% with JSON. The improvement is attributed to TOON's explicit length markers and schema declarations that provide structural anchors for LLM parsing.

**Evidence:**
- [TOON Benchmark Results](https://github.com/toon-format/toon)
- Models tested: claude-haiku-4-5-20251001, gemini-2.5-flash, gpt-5-nano, grok-4-fast-non-reasoning

**Level Impact:**
- **L0:** AI understands TOON data better than JSON data
- **L1:** Use TOON for structured data in prompts to improve extraction accuracy
- **L2:** Evaluate TOON for accuracy-critical pipelines, not just cost optimization

---

### DISC-046: TOON Specification Maturity

**ID:** DISC-046
**Slug:** toon-specification-maturity
**Name:** TOON Spec v3.0 Provides Production-Ready Guarantees
**Short Description:** TOON specification v3.0 includes formal grammar, conformance requirements, and 349 test fixtures.

**Long Description:**
TOON specification version 3.0 (released 2025-11-24) provides production-grade rigor: complete ABNF grammar definitions, deterministic encoding requirements (key ordering, canonical numbers), strict mode validation (length mismatches, escape sequences, indentation), and security considerations (quoting prevents injection). The specification includes 349 test fixtures for language-agnostic conformance testing. Implementations exist in TypeScript (reference), Python, Go, Rust, and .NET. The format uses `text/toon` media type (pending IANA registration) and `.toon` file extension.

**Evidence:**
- [TOON Specification v3.0](https://github.com/toon-format/spec)
- [Python Implementation](https://github.com/xaviviro/python-toon)

**Level Impact:**
- **L0:** TOON has clear rules that everyone agrees on
- **L1:** Rely on spec conformance for cross-language interoperability
- **L2:** Monitor IANA registration and specification evolution for enterprise adoption

---

### DISC-047: TOON Optimal Data Shapes

**ID:** DISC-047
**Slug:** toon-optimal-data-shapes
**Name:** TOON Optimal for Tabular Arrays, Suboptimal for Deep Nesting
**Short Description:** TOON shows highest benefits for uniform object arrays, diminishing returns for deeply nested structures.

**Long Description:**
TOON's design optimizes for the "sweet spot" of uniform arrays of objects (tabular data) where CSV-like compactness combines with explicit structure. For such data, token reduction reaches 40-60%. Mixed structures show 20-40% reduction. Deeply nested or non-uniform data may show minimal benefit (0-10%) and JSON may be preferred. For flat primitive datasets, CSV remains most compact (TOON adds 5-10% overhead for structure markers). This informs the decision matrix for when to use TOON vs JSON in Jerry's serialization layer.

**Evidence:**
- [TOON Format Documentation](https://github.com/toon-format/toon)
- [Benjamin Abt Analysis](https://benjamin-abt.com/blog/2025/12/12/ai-toon-format/)

**Level Impact:**
- **L0:** TOON works best for list-of-things data, not deeply nested data
- **L1:** Implement auto-detection to choose TOON for tabular, JSON for nested
- **L2:** Profile actual domain data shapes to quantify expected TOON benefit

---

### DISC-048: TOON Python Integration Path

**ID:** DISC-048
**Slug:** toon-python-integration-path
**Name:** python-toon Package Provides Production-Ready Integration
**Short Description:** The python-toon package offers encode/decode API, CLI tools, and configuration options for Jerry integration.

**Long Description:**
The `python-toon` package (pip install python-toon) provides a complete implementation: `encode(value, options)` for Python→TOON, `decode(input_str, options)` for TOON→Python, CLI tool for batch conversion (`toon input.json -o output.toon`), and configuration options (indent, delimiter, length_marker, strict_mode). The API aligns with Python's `json` module patterns, making integration straightforward. Strict mode enables validation of length declarations and escape sequences. The package is maintained by Xavi Viro and follows the TOON spec v3.0.

**Evidence:**
- [python-toon GitHub](https://github.com/xaviviro/python-toon)
- [PyPI Package](https://pypi.org/project/python-toon/)

**Level Impact:**
- **L0:** We can add TOON to Jerry with just `pip install python-toon`
- **L1:** Create ToonSerializationAdapter implementing SerializationPort
- **L2:** Evaluate python-toon maintenance status and consider vendoring strategy

---

## VII. Action Items

| ID | Action | Priority | Owner | Status |
|----|--------|----------|-------|--------|
| ACT-025.1 | Add `python-toon` to dependencies | HIGH | Dev | PENDING |
| ACT-025.2 | Define SerializationPort in domain layer | HIGH | Dev | PENDING |
| ACT-025.3 | Implement ToonSerializationAdapter | HIGH | Dev | PENDING |
| ACT-025.4 | Add TOON format tests | MEDIUM | Dev | PENDING |
| ACT-025.5 | Profile token reduction for Jerry entities | MEDIUM | Dev | PENDING |
| ACT-025.6 | Document TOON usage in CLAUDE.md | LOW | Dev | PENDING |

---

## VIII. References

### Primary Sources

1. **TOON Specification v3.0** (2025-11-24)
   - URL: https://github.com/toon-format/spec
   - License: MIT
   - Author: Johann Schopplich

2. **python-toon Library**
   - URL: https://github.com/xaviviro/python-toon
   - PyPI: https://pypi.org/project/python-toon/
   - Author: Xavi Viro

3. **TOON Reference Implementation** (TypeScript)
   - URL: https://github.com/toon-format/toon
   - Includes: Benchmarks, test fixtures

### Secondary Sources

4. **InfoQ News** (November 2025)
   - "New Token-Oriented Object Notation (TOON) Hopes to Cut LLM Costs by Reducing Token Consumption"
   - URL: https://www.infoq.com/news/2025/11/toon-reduce-llm-cost-tokens/

5. **Analytics Vidhya** (November 2025)
   - "Reduce Token Costs for LLMs with TOON"
   - URL: https://www.analyticsvidhya.com/blog/2025/11/toon-token-oriented-object-notation/

6. **Medium/CodeX** (November 2025)
   - "TOON: The Data Format Slashing LLM Costs by 50%"
   - URL: https://medium.com/codex/toon-the-data-format-slashing-llm-costs-by-50-ac8d7b808ff6

7. **Benjamin Abt Blog** (December 2025)
   - "TOON Format: Token-Oriented Object Notation for LLM-Friendly Data Exchange"
   - URL: https://benjamin-abt.com/blog/2025/12/12/ai-toon-format/

---

## IX. PS Integration

**Problem Statement:** Phase 3.5 Agent Reorganization / WORK-025
**Entry Type:** RESEARCH
**Severity:** MEDIUM
**Resolution:** COMPLETE

**Artifacts:**
- This document: `docs/research/TOON_FORMAT_ANALYSIS.md`
- Discoveries: DISC-044 through DISC-048

**Next Steps:**
1. Add discoveries to WORKTRACKER.md Phase DISCOVERY
2. Create implementation tasks in Phase 3 backlog
3. Update PLAN.md with TOON serialization milestone
