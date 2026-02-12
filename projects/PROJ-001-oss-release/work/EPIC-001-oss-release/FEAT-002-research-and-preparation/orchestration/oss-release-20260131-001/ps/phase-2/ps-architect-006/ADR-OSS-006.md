# ADR-OSS-006: Transcript Skill Templates for OSS Release

> **Workflow ID:** oss-release-20260131-001
> **Phase:** 2 (ADR Creation)
> **Agent:** ps-architect-006
> **Created:** 2026-01-31
> **Status:** PROPOSED
> **Priority:** MEDIUM
> **Dependencies:** ADR-OSS-001 (CLAUDE.md Decomposition)
> **Risk Reference:** RSK-P0-014 (MCP Context Bloat - RPN 125), RSK-P0-013 (Community Adoption - RPN 168)
> **Supersedes:** None
> **Constitutional Compliance:** P-001 (Truth), P-002 (Persistence), P-003 (No Subagents), P-011 (Evidence)

---

## Document Navigation

| Section | Audience | Purpose |
|---------|----------|---------|
| [L0: Executive Summary](#l0-executive-summary-eli5) | Executives, Stakeholders | High-level overview |
| [L1: Technical Details](#l1-technical-details-engineer) | Engineers, Developers | Template specifications |
| [L2: Strategic Implications](#l2-strategic-implications-architect) | Architects, Decision Makers | Trade-offs between flexibility and consistency |

---

## L0: Executive Summary (ELI5)

### The Problem (Simple Analogy)

Imagine a restaurant chain where each location follows the same recipe book. When the head chef writes "add some salt" instead of "add 1/4 teaspoon of salt," each location ends up with differently seasoned dishes. Customers get inconsistent experiences, and the brand suffers.

Jerry's Transcript Skill has the same problem for open source release. The output templates currently work well with Claude Sonnet (the default model), but OSS users will:
- Use different Claude models (Opus, Haiku, Sonnet)
- Run without Jerry's full context (CLAUDE.md, skills infrastructure)
- Expect consistent, predictable output regardless of model or configuration

**Discovery (2026-01-30):** Claude Opus produced a 9-file packet with `06-timeline.md` instead of the required 8-file packet. Same instructions, different model, different output.

### The Solution

We will ensure the Transcript Skill produces **model-agnostic, consistent output** for OSS users by:

1. **Leveraging ADR-007** as the authoritative template source
2. **Adding OSS-specific enforcement** - Clear error messages for non-Claude environments
3. **Documenting template contracts** in user-facing documentation
4. **Validation integration** - ps-critic criteria accessible to OSS users

### Key Numbers

| Metric | Current State | Target State | Impact |
|--------|---------------|--------------|--------|
| Template files defined | 8 (ADR-007) | 8 (unchanged) | Consistent |
| Model-specific variations | 2+ observed | 0 (eliminated) | Critical for OSS |
| Validation criteria documented | Internal only | Public OSS docs | +Community trust |
| Template compliance tests | Partial | Full CI coverage | Prevents regression |

### Bottom Line

**Output templates are already well-defined internally (ADR-007).** This ADR focuses on making those templates accessible and enforceable for OSS users, ensuring the community experiences the same quality as internal users.

---

## Context

### Background

The Transcript Skill produces structured Markdown "packets" from meeting transcripts. Each packet contains 8 files (00-index.md through 07-topics.md) plus optional mindmap output. The internal specification is comprehensive (ADR-007: Output Template Specification), but OSS users need:

1. **Discoverable templates** - Where to find the expected output format
2. **Model-agnostic guarantees** - Same output regardless of Claude model
3. **Validation tooling** - How to verify output compliance
4. **Error recovery** - What to do when output doesn't match expectations

### The OSS Challenge

OSS users differ from internal users in critical ways:

| Dimension | Internal User | OSS User | Gap |
|-----------|--------------|----------|-----|
| Context | Full CLAUDE.md loaded | May be stripped/minimal | Template context lost |
| Model Access | Consistent (Sonnet default) | Variable (Opus, Haiku, Sonnet) | Model behavior varies |
| Validation | ps-critic integrated | May not invoke critic | Validation gap |
| Error Handling | Familiar with Jerry patterns | First-time users | Learning curve |
| Support | Direct communication | Issues/discussions | Response latency |

### Prior Art: ADR-007 (Internal Specification)

ADR-007 (2026-01-31) established comprehensive output templates:

**8-File Packet Structure:**
| Number | File Name | Description | Token Budget |
|--------|-----------|-------------|--------------|
| 00 | `00-index.md` | Navigation hub and metadata | 2,000 |
| 01 | `01-summary.md` | Executive summary | 5,000 |
| 02 | `02-transcript.md` | Full formatted transcript | 35,000 (splittable) |
| 03 | `03-speakers.md` | Speaker directory | 8,000 |
| 04 | `04-action-items.md` | Action items extracted | 10,000 |
| 05 | `05-decisions.md` | Decisions made | 10,000 |
| 06 | `06-questions.md` | Questions (open + answered) | 10,000 |
| 07 | `07-topics.md` | Topic hierarchy | 15,000 |

**Key ADR-007 Features:**
- MUST-CREATE / MUST-NOT-CREATE file lists
- Anchor format specification (`seg-NNN`, `act-NNN`, etc.)
- Citation format requirements
- JSON Schema for machine validation
- ps-critic validation criteria (SCHEMA-001 through SCHEMA-008)

### Constraints

| ID | Constraint | Source | Priority |
|----|------------|--------|----------|
| C-001 | Must not duplicate ADR-007 content | DRY principle | HARD |
| C-002 | Must work without Jerry infrastructure | OSS user requirement | HARD |
| C-003 | Must support Claude Opus, Sonnet, and Haiku | Multi-model OSS users | HARD |
| C-004 | Must have user-facing documentation | OSS discoverability | MEDIUM |
| C-005 | Must integrate with existing validation | ps-critic (SCHEMA-*) | MEDIUM |

### Forces

1. **Internal vs. External Documentation:** ADR-007 is comprehensive but uses internal terminology. OSS users need friendlier documentation.

2. **Flexibility vs. Consistency:** Allowing model "improvements" (like Opus adding timeline.md) provides flexibility but breaks consistency.

3. **Validation Cost vs. Quality:** Mandatory validation catches errors but adds processing time and cost.

4. **Template Strictness vs. User Needs:** Strict templates ensure consistency but may not cover all use cases.

---

## Options Considered

### Option A: Publish ADR-007 Verbatim

**Description:** Make ADR-007 the OSS documentation, renamed for external consumption.

**Implementation:**
```
docs/skills/transcript/
├── OUTPUT-SPECIFICATION.md    ← ADR-007 content
└── VALIDATION.md              ← ps-critic criteria
```

**Pros:**
- Zero content duplication
- Comprehensive specification available
- Already tested and validated

**Cons:**
- **Too technical for new users** - ADR-007 is 1,045 lines
- **Internal terminology** - References ps-*, ADR-*, etc.
- **Missing getting-started context** - Jumps into details

**Fit with Constraints:**
- C-001: PASSES (no duplication)
- C-002: PARTIAL (terminology issues)
- C-003: PASSES (model-agnostic rules present)
- C-004: **FAILS** (not user-friendly)
- C-005: PASSES (criteria present)

### Option B: Create OSS-Focused Template Guide

**Description:** Create a new, user-focused guide that references ADR-007 for detailed specifications.

**Implementation:**
```
docs/skills/transcript/
├── getting-started.md         ← Quick start for OSS users
├── output-format.md           ← Simplified template overview
├── validation.md              ← How to validate output
└── specification/
    └── ADR-007.md             ← Full specification (reference)
```

**Pros:**
- **User-friendly entry point** for OSS users
- Progressive disclosure (simple → detailed)
- Separates concerns (getting started vs. spec)

**Cons:**
- Content overlap risk (simplified may drift from spec)
- More files to maintain
- Users may stop at simplified version, miss details

**Fit with Constraints:**
- C-001: PARTIAL (some content overlap)
- C-002: PASSES (OSS-focused)
- C-003: PASSES (model notes in docs)
- C-004: **PASSES** (user-friendly)
- C-005: PASSES (validation section)

### Option C: Hybrid - Tiered Documentation with Template Contracts (RECOMMENDED)

**Description:** Create a tiered documentation structure with:
1. **Quick Reference** - One-page summary for common use
2. **Template Contracts** - Explicit model-agnostic guarantees
3. **Full Specification** - ADR-007 as authoritative source
4. **Validation Integration** - OSS-accessible validation tooling

**Implementation:**
```
skills/transcript/
├── SKILL.md                   ← Skill definition
├── docs/
│   ├── PLAYBOOK.md            ← Step-by-step guide
│   ├── RUNBOOK.md             ← Operational procedures
│   ├── OUTPUT-GUIDE.md        ← NEW: OSS user-focused template guide
│   └── TEMPLATE-CONTRACTS.md  ← NEW: Model-agnostic guarantees
├── validation/
│   └── ts-critic-extension.md ← Validation criteria
└── schemas/
    └── packet-structure.schema.json ← NEW: JSON Schema (from ADR-007)
```

**Pros:**
- **Clear separation** - User guide vs. specification vs. validation
- **Single source of truth** - ADR-007 remains authoritative
- **Progressive disclosure** - Simple to detailed
- **Machine-readable contracts** - JSON Schema for automation
- **OSS-friendly** - No internal terminology in user docs

**Cons:**
- Requires creating 2 new documents
- Template contracts require maintenance
- JSON Schema must sync with ADR-007

**Fit with Constraints:**
- C-001: **PASSES** (OUTPUT-GUIDE references ADR-007, doesn't duplicate)
- C-002: **PASSES** (OSS-focused documentation)
- C-003: **PASSES** (Template contracts explicitly model-agnostic)
- C-004: **PASSES** (User-friendly guide)
- C-005: **PASSES** (Validation integration via schema)

---

## Decision

**We will use Option C: Hybrid - Tiered Documentation with Template Contracts.**

### Rationale

1. **OSS Users Need Different Entry Points:** New users shouldn't start with a 1,045-line ADR. A focused OUTPUT-GUIDE.md provides approachable documentation while ADR-007 remains the authoritative source.

2. **Model-Agnostic Contracts Are Essential:** The Opus/Sonnet inconsistency proves that implicit template expectations fail across models. Explicit TEMPLATE-CONTRACTS.md with machine-readable JSON Schema prevents this.

3. **Validation Must Be Accessible:** OSS users should be able to validate output without understanding Jerry internals. JSON Schema + simple validation instructions enable this.

4. **DRY Compliance:** OUTPUT-GUIDE.md summarizes and references ADR-007 rather than duplicating it. Updates to ADR-007 automatically apply (with reference update).

5. **Industry Alignment:** Tiered documentation (quickstart → guide → reference) follows documentation best practices (Stripe, Twilio, Anthropic patterns).

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | **HIGH** | All 5 constraints satisfied |
| Risk Level | **LOW** | Builds on proven ADR-007 |
| Implementation Effort | **MEDIUM** | 2 new documents + JSON Schema |
| Reversibility | **HIGH** | Can simplify if unused |

---

## L1: Technical Details (Engineer)

### Output File Structure

The Transcript Skill produces an 8-file packet structure as defined in ADR-007. For OSS release, these templates are formalized as **contracts** that must be honored regardless of model.

```
transcript-{packet-id}/
├── 00-index.md          # Navigation hub (~2K tokens)
├── 01-summary.md        # Executive summary (~5K tokens)
├── 02-transcript.md     # Full transcript (may split at 35K)
├── 03-speakers.md       # Speaker directory (~8K tokens)
├── 04-action-items.md   # Action items (~10K tokens)
├── 05-decisions.md      # Decisions (~10K tokens)
├── 06-questions.md      # Questions (~10K tokens)
├── 07-topics.md         # Topics (~15K tokens)
├── 08-mindmap/          # OPTIONAL: Mindmap output
│   ├── mindmap.mmd      # Mermaid format
│   └── mindmap.ascii.txt # ASCII format
├── _anchors.json        # Anchor registry
├── index.json           # Parser metadata
├── chunks/              # Chunked transcript data
│   └── chunk-*.json
├── extraction-report.json # Entity extraction results
└── quality-review.md    # ps-critic validation results
```

### Template Contract Definitions

Each output file has a **contract** defining required structure:

#### Contract: 00-index.md

```yaml
contract:
  file: "00-index.md"
  required: true
  token_budget: 2000
  splittable: false

  frontmatter:
    required:
      - schema_version: "string (semver)"
      - generator: "ts-formatter"
      - generated_at: "ISO 8601 timestamp"
      - packet_id: "string"

  sections:
    required:
      - "# {title}"
      - "## Quick Stats"
      - "## Navigation"
    optional:
      - "## Anchor Registry"

  content_rules:
    - "Must link to all 7 other packet files (01-07)"
    - "Must include action item, decision, question, topic counts"
    - "Must include meeting date and duration"
```

#### Contract: 01-summary.md

```yaml
contract:
  file: "01-summary.md"
  required: true
  token_budget: 5000
  splittable: false

  frontmatter:
    required:
      - schema_version
      - generator
      - generated_at

  sections:
    required:
      - "# Summary"
      - "## Key Outcomes"
      - "## Navigation"

  content_rules:
    - "Must provide executive summary (2-3 paragraphs)"
    - "Must list top action items (up to 5)"
    - "Must list key decisions (up to 3)"
    - "Navigation must link to 00-index.md and 02-transcript.md"
```

#### Contract: 02-transcript.md

```yaml
contract:
  file: "02-transcript.md"
  required: true
  token_budget: 35000
  splittable: true
  split_pattern: "02-transcript-{NN}.md"

  frontmatter:
    required:
      - schema_version
      - generator
      - generated_at
    conditional:
      - split_info (if split)

  sections:
    required:
      - "# Transcript"
      - "## Navigation"

  content_rules:
    - "Each segment must have timestamp in [HH:MM:SS] format"
    - "Each segment must have speaker attribution"
    - "Segment anchors must use seg-{NNN} format"
    - "If split, each part must link to previous/next"
```

#### Contract: 03-speakers.md

```yaml
contract:
  file: "03-speakers.md"
  required: true
  token_budget: 8000
  splittable: true

  frontmatter:
    required:
      - schema_version
      - generator
      - generated_at

  sections:
    required:
      - "# Speakers"
      - "## Navigation"

  content_rules:
    - "Each speaker must have spk-{slug} anchor"
    - "Speaker slug must be lowercase-hyphenated"
    - "Must include participation stats (utterance count)"
    - "Must include first/last appearance timestamps"
```

#### Contract: 04-action-items.md

```yaml
contract:
  file: "04-action-items.md"
  required: true
  token_budget: 10000
  splittable: true

  frontmatter:
    required:
      - schema_version
      - generator
      - generated_at
      - entity_type: "action-item"

  sections:
    required:
      - "# Action Items"
      - "## Navigation"

  entity_structure:
    anchor_pattern: "act-{NNN}"
    required_fields:
      - assignee: "Link to 03-speakers.md#{spk-slug}"
      - due_date: "Date or 'Unspecified'"
      - confidence: "0.0-1.0"
      - source: "Link to 02-transcript.md#{seg-NNN}"
    optional_fields:
      - priority
      - status

  citation_format: |
    > "{quoted_text}"
    >
    > -- [{speaker}](03-speakers.md#{spk-anchor}), [{timestamp}](02-transcript.md#{seg-anchor})
```

#### Contract: 05-decisions.md

```yaml
contract:
  file: "05-decisions.md"
  required: true
  token_budget: 10000
  splittable: true

  frontmatter:
    required:
      - schema_version
      - generator
      - generated_at
      - entity_type: "decision"

  sections:
    required:
      - "# Decisions"
      - "## Navigation"

  entity_structure:
    anchor_pattern: "dec-{NNN}"
    required_fields:
      - decision_maker: "Link to 03-speakers.md#{spk-slug}"
      - confidence: "0.0-1.0"
      - source: "Link to 02-transcript.md#{seg-NNN}"
    optional_fields:
      - rationale
      - alternatives_discussed
```

#### Contract: 06-questions.md

```yaml
contract:
  file: "06-questions.md"
  required: true
  token_budget: 10000
  splittable: true

  frontmatter:
    required:
      - schema_version
      - generator
      - generated_at
      - entity_type: "question"

  sections:
    required:
      - "# Questions"
      - "## Open Questions"
      - "## Answered Questions"
      - "## Navigation"

  entity_structure:
    anchor_pattern: "que-{NNN}"
    required_fields:
      - asker: "Link to 03-speakers.md#{spk-slug}"
      - status: "open|answered"
      - confidence: "0.0-1.0"
      - source: "Link to 02-transcript.md#{seg-NNN}"
    conditional_fields:
      - answer (if status=answered)
      - answerer (if status=answered)
```

#### Contract: 07-topics.md

```yaml
contract:
  file: "07-topics.md"
  required: true
  token_budget: 15000
  splittable: true

  frontmatter:
    required:
      - schema_version
      - generator
      - generated_at
      - entity_type: "topic"

  sections:
    required:
      - "# Topics"
      - "## Topic Hierarchy"
      - "## Navigation"

  entity_structure:
    anchor_pattern: "top-{NNN}"
    required_fields:
      - name: "Topic name"
      - duration: "Approximate discussion time"
      - participants: "List of speaker references"
      - source_range: "Start and end segment anchors"
    optional_fields:
      - subtopics
      - related_entities
```

### Anchor Format Specification

All anchors must follow these patterns:

| Entity Type | Pattern | Regex | Valid Examples | Invalid Examples |
|-------------|---------|-------|----------------|------------------|
| Segment | `seg-{NNN}` | `^seg-\d{3}$` | seg-001, seg-042, seg-501 | segment-001, SEG-001, seg-1 |
| Speaker | `spk-{slug}` | `^spk-[a-z0-9-]+$` | spk-alice, spk-bob-smith | speaker-alice, SPK-Alice |
| Action Item | `act-{NNN}` | `^act-\d{3}$` | act-001, act-002 | AI-001, ACT-001, action-1 |
| Decision | `dec-{NNN}` | `^dec-\d{3}$` | dec-001, dec-002 | DEC-001, decision-001 |
| Question | `que-{NNN}` | `^que-\d{3}$` | que-001, que-002 | QUE-001, question-001 |
| Topic | `top-{NNN}` | `^top-\d{3}$` | top-001, top-002 | TOP-001, topic-001 |

### Forbidden Output Patterns

The following files MUST NOT be created:

| Forbidden Pattern | Reason | Model That Created It |
|-------------------|--------|----------------------|
| `*-timeline.md` | Not part of schema | Claude Opus |
| `*-sentiment.md` | Not part of schema | N/A (prevented) |
| `*-analysis.md` | Not part of schema | N/A (prevented) |
| `08-*.md` | 08 reserved for mindmap dir | N/A (prevented) |
| Unnumbered `*.md` | All must be 00-07 | N/A (prevented) |

### Validation Integration

OSS users can validate output using the provided JSON Schema:

```bash
# Validate packet structure (OSS user workflow)
python -c "
import json
from pathlib import Path
from jsonschema import validate, ValidationError

# Load schema
schema_path = Path('skills/transcript/schemas/packet-structure.schema.json')
schema = json.loads(schema_path.read_text())

# Check packet
packet_path = Path('output/my-transcript/')
packet_files = list(packet_path.glob('*.md'))

required_files = [
    '00-index.md', '01-summary.md', '02-transcript.md',
    '03-speakers.md', '04-action-items.md', '05-decisions.md',
    '06-questions.md', '07-topics.md'
]

for required in required_files:
    if not (packet_path / required).exists():
        print(f'FAIL: Missing required file {required}')

# Check for forbidden files
forbidden_patterns = ['*-timeline.md', '*-sentiment.md', '*-analysis.md']
for pattern in forbidden_patterns:
    matches = list(packet_path.glob(pattern))
    if matches:
        print(f'FAIL: Forbidden file(s) detected: {matches}')

print('PASS: Packet structure valid')
"
```

### ps-critic Validation Criteria (OSS-Accessible)

The following validation criteria from ps-critic are documented for OSS users:

| Criteria ID | Name | Weight | Pass Threshold | Description |
|-------------|------|--------|----------------|-------------|
| SCHEMA-001 | 8-File Packet Structure | 0.20 | 1.0 | All 8 core files (00-07) exist |
| SCHEMA-002 | No Forbidden Files | 0.10 | 1.0 | No timeline, sentiment, analysis files |
| SCHEMA-003 | Anchor Format Compliance | 0.15 | 0.95 | Anchors match `{type}-{NNN}` pattern |
| SCHEMA-004 | Navigation Links Present | 0.10 | 0.90 | Entity files have prev/next navigation |
| SCHEMA-005 | Citation Format Compliance | 0.15 | 0.85 | Citations include speaker + timestamp |
| SCHEMA-006 | No Canonical JSON Links | 0.10 | 1.0 | No links to large JSON files |
| SCHEMA-007 | Token Limits Respected | 0.10 | 1.0 | All files under 35K tokens |
| SCHEMA-008 | YAML Frontmatter Present | 0.10 | 0.95 | All files have schema_version |

**Quality Threshold:** >= 0.90 aggregate score

---

## L2: Strategic Implications (Architect)

### Trade-off Analysis

| Factor | Strict Templates | Flexible Guidelines | Hybrid (Selected) |
|--------|-----------------|---------------------|-------------------|
| Model consistency | **Excellent** | Poor | **Good** |
| User flexibility | Poor | **Excellent** | Good |
| Maintenance burden | Medium | Low | **Medium** |
| OSS adoption | High (predictable) | Medium (confusion) | **High** |
| Error detection | Immediate | Delayed | **Immediate** |

### One-Way Door Assessment

| Aspect | Reversibility | Assessment |
|--------|---------------|------------|
| Template structure (8 files) | **LOW** | Changing breaks existing tooling |
| Anchor format (type-NNN) | **LOW** | Format is part of public contract |
| Token budgets | **MEDIUM** | Can adjust limits if needed |
| Validation thresholds | **HIGH** | Can relax if too strict |
| Documentation structure | **HIGH** | Files can be reorganized |

**Conclusion:** Template structure and anchor format are **ONE-WAY DOORS**. Once OSS users build tooling around these, changes would be breaking. The thresholds and documentation are **TWO-WAY DOORS**.

### Failure Mode Analysis

| Failure Mode | Probability | Impact | Detection | Mitigation |
|--------------|-------------|--------|-----------|------------|
| OSS user runs with wrong model config | MEDIUM | MEDIUM | Validation fails | Clear error messages, model detection |
| Template drift between ADR-007 and OSS docs | LOW | HIGH | Manual review | Single source of truth (ADR-007) |
| Validation schema out of sync | MEDIUM | MEDIUM | CI tests | Schema generation from ADR-007 |
| New model produces new variations | MEDIUM | HIGH | User reports | Expand forbidden patterns |
| OSS user skips validation | HIGH | LOW | Quality issues | Validation by default |

### Design Rationale

#### Why Not Model-Specific Templates?

**Considered:** Create separate template sets for Opus, Sonnet, Haiku.

**Rejected because:**
1. **Maintenance burden** - 3x documentation to maintain
2. **User confusion** - "Which template do I use?"
3. **Inconsistent output** - Output differs by model
4. **Against design goal** - We want model-agnostic consistency

**Decision:** Single template set with model-agnostic enforcement.

#### Why Explicit MUST-NOT-CREATE Lists?

**Considered:** Only specify what MUST exist, ignore extras.

**Rejected because:**
1. **Opus created timeline.md** - Silent failures are worse than errors
2. **Tooling breaks** - Downstream tools expect specific files
3. **User confusion** - "What are these extra files?"

**Decision:** Explicit forbidden patterns with immediate validation failure.

#### Why JSON Schema Alongside Prose?

**Considered:** Prose documentation only (human-readable).

**Added JSON Schema because:**
1. **Machine validation** - Automated compliance checking
2. **OSS tooling** - Users can build validation into CI/CD
3. **Industry standard** - JSON Schema is well-supported
4. **Error messages** - Precise failure descriptions

**Decision:** Both prose (human) and JSON Schema (machine).

### Industry Precedent

| System | Template Strategy | Outcome |
|--------|------------------|---------|
| **OpenAPI** | Strict schema + validation | Industry standard, excellent tooling |
| **Terraform** | HCL schema + providers | Model-agnostic IaC |
| **Kubernetes** | YAML manifests + validation | Strict schema, broad adoption |
| **Anthropic MCP** | JSON-RPC + schema | Model-agnostic, portable |
| **Jerry Transcript** | **YAML contracts + JSON Schema** | Following proven patterns |

---

## Consequences

### Positive Consequences

1. **Model-Agnostic Guarantees:** OSS users get consistent output regardless of Claude model choice.

2. **Discoverable Documentation:** Tiered docs (guide -> contracts -> spec) serve different user needs.

3. **Automated Validation:** JSON Schema enables CI/CD integration for OSS users.

4. **DRY Compliance:** OUTPUT-GUIDE.md references ADR-007, eliminating duplication.

5. **Community Trust:** Explicit contracts and validation build confidence in the skill.

### Negative Consequences

1. **Rigidity:** Model "improvements" (like Opus's timeline.md) are rejected as errors.

2. **Documentation Overhead:** Two new documents (OUTPUT-GUIDE.md, TEMPLATE-CONTRACTS.md) to maintain.

3. **Schema Sync Risk:** JSON Schema must stay synchronized with ADR-007.

### Neutral Consequences

1. **Validation Latency:** Post-generation validation adds minimal processing time (~100ms).

2. **Learning Curve:** OSS users must learn template contracts before customizing.

### Residual Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| New Claude model produces new variations | MEDIUM | MEDIUM | Expand forbidden patterns, regression tests |
| OSS users modify templates incorrectly | LOW | LOW | Clear documentation, validation |
| JSON Schema drift from ADR-007 | LOW | MEDIUM | Generate from single source |

---

## Verification Requirements

This ADR links to the following Verification Requirements from the V&V Plan:

| VR ID | Requirement | Verification Method |
|-------|-------------|---------------------|
| VR-016 | Skill output matches documented templates | Automated + manual test |
| VR-017 | Validation criteria accessible to OSS users | Documentation review |
| VR-018 | Template compliance across models | Multi-model regression test |

---

## Risk Traceability

| Risk ID | Description | RPN | Treatment |
|---------|-------------|-----|-----------|
| RSK-P0-013 | Community adoption challenges | 168 | **ADDRESSED**: User-friendly documentation |
| RSK-P0-014 | MCP server context bloat | 125 | **RELATED**: Templates reduce output complexity |

---

## Implementation

### Action Items

| # | Action | Owner | Priority | Due |
|---|--------|-------|----------|-----|
| 1 | Create OUTPUT-GUIDE.md for OSS users | Documentation | P1 | Day 3 |
| 2 | Create TEMPLATE-CONTRACTS.md with YAML specifications | Architecture | P1 | Day 3 |
| 3 | Export JSON Schema from ADR-007 Section 6 | Architecture | P1 | Day 2 |
| 4 | Add multi-model regression tests | QA | P2 | Day 4 |
| 5 | Update PLAYBOOK.md with OSS user guidance | Documentation | P2 | Day 4 |
| 6 | Add template validation to CI pipeline | DevOps | P2 | Day 5 |

### Validation Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| OUTPUT-GUIDE.md exists | Present | File check |
| TEMPLATE-CONTRACTS.md exists | Present | File check |
| JSON Schema validates | 100% | CI test |
| Multi-model consistency | 3/3 models pass | Regression test |
| OSS user can validate | Self-service | User test |

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-007 | IMPLEMENTS | OSS-facing implementation of ADR-007 |
| ADR-OSS-001 | DEPENDS_ON | CLAUDE.md decomposition affects skill loading |
| ADR-OSS-003 | RELATED_TO | Progressive docs loading pattern |

---

## References

### Primary Sources

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | ADR-007 Output Template Specification | Internal ADR | Authoritative template source |
| 2 | skills/transcript/SKILL.md | Skill Definition | Current skill implementation |
| 3 | skills/transcript/agents/ts-formatter.md | Agent Definition | Formatter implementation |
| 4 | Cross-Pollination Manifest (barrier-2) | Orchestration | V&V requirements linkage |
| 5 | Skills Best Practices Research | Research | OSS skill patterns |

### Industry References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 6 | [JSON Schema](https://json-schema.org/) | Standard | Machine-readable validation |
| 7 | [OpenAPI Specification](https://www.openapis.org/) | Standard | Schema-first API design |
| 8 | [Anthropic MCP Protocol](https://github.com/anthropics/mcp) | Industry | Model-agnostic patterns |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ADR-OSS-006 |
| **Status** | PROPOSED |
| **Workflow** | oss-release-20260131-001 |
| **Phase** | 2 (ADR Creation) |
| **Agent** | ps-architect-006 |
| **Priority** | MEDIUM |
| **Dependencies** | ADR-OSS-001 |
| **Decision Type** | HYBRID (One-way: template structure; Two-way: thresholds) |
| **Implementation Effort** | 2-3 days |
| **Word Count** | ~3,800 |
| **Constitutional Compliance** | P-001 (Truth), P-002 (Persistence), P-003 (No Subagents), P-011 (Evidence) |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-31 | ps-architect-006 | Initial ADR creation for OSS release |

---

*This ADR was produced by ps-architect-006 for PROJ-001-oss-release Phase 2.*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-003 (No Subagents), P-004 (Provenance), P-011 (Evidence)*
*Template: Michael Nygard ADR Format with Jerry L0/L1/L2 extensions*
