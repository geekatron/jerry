# EN-013: Context Injection Implementation

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** low
> **Impact:** medium
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 4
> **Effort Points:** 5
> **Gate:** GATE-6 (Final Review)

---

## Summary

Implement the context injection mechanism designed in EN-006 that allows existing Jerry agents (ps-researcher, ps-analyst, ps-synthesizer, etc.) to be leveraged with transcript-specific context and prompts. This is an advanced feature that enables reuse of battle-tested agents while specializing their behavior.

**Technical Justification:**
- Implements design from EN-006
- Enables agent reuse across domains
- Reduces need for new agent development
- Supports domain-specific customization

---

## Benefit Hypothesis

**We believe that** implementing context injection for existing agents

**Will result in** flexible agent reuse without duplicating agent logic

**We will know we have succeeded when:**
- Existing Jerry agents accept injected context
- Prompt overrides customize behavior
- Metadata flows through pipeline
- Human approval received at GATE-6

---

## Acceptance Criteria

### Definition of Done

- [ ] Context loader implemented
- [ ] Prompt template merger implemented
- [ ] Metadata passing mechanism implemented
- [ ] Integration with orchestration working
- [ ] Example context files created
- [ ] Integration tests passing
- [ ] ps-critic review passed
- [ ] Human approval at GATE-6

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Context files load correctly | [ ] |
| AC-2 | Prompt templates merge properly | [ ] |
| AC-3 | Variables substitute correctly | [ ] |
| AC-4 | Metadata passes through pipeline | [ ] |
| AC-5 | Works with ps-researcher agent | [ ] |
| AC-6 | Works with ps-analyst agent | [ ] |
| AC-7 | Works with ps-synthesizer agent | [ ] |
| AC-8 | Performance overhead < 500ms | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| TASK-063 | Implement Context Loader | pending | Claude | 2 | EN-006 |
| TASK-064 | Implement Prompt Merger | pending | Claude | 1 | TASK-063 |
| TASK-065 | Implement Metadata Passing | pending | Claude | 1 | TASK-064 |
| TASK-066 | Create Example Context Files | pending | Claude | 1 | TASK-063 |

---

## Implementation Details

### Context Loader

```python
# Pseudocode for context loading
class ContextLoader:
    def load(self, context_injection_config: dict) -> InjectedContext:
        """
        Load context from configuration.

        Args:
            context_injection_config: {
                "domain": "legal",
                "context_files": [
                    {"path": "contexts/legal-terms.yaml", "type": "entity_definitions"},
                    {"path": "contexts/legal-rules.md", "type": "extraction_rules"}
                ],
                "prompt_overrides": {
                    "entity_extraction": {
                        "template": "prompts/legal-entity-extraction.md",
                        "variables": {"jurisdiction": "US", "case_type": "contract"}
                    }
                }
            }

        Returns:
            InjectedContext with loaded and parsed content
        """
        pass
```

### Prompt Template Merger

```python
class PromptMerger:
    def merge(
        self,
        base_prompt: str,
        override_template: str,
        variables: dict
    ) -> str:
        """
        Merge base prompt with override template.

        Strategy:
        1. If override_template is complete replacement, use it
        2. If override_template has {{BASE_PROMPT}}, inject base there
        3. Substitute all {{variable}} patterns with values
        """
        pass
```

### Metadata Passing

```yaml
# Artifact metadata structure
metadata:
  context_injection:
    domain: "legal"
    loaded_contexts:
      - type: entity_definitions
        path: contexts/legal-terms.yaml
        version: "1.0.0"
    prompt_overrides_applied:
      - entity_extraction
    processing_timestamp: "2026-01-26T10:30:00Z"
```

---

## Example Context Files

### Domain-Specific Entity Definitions

```yaml
# contexts/legal-terms.yaml
domain: legal
version: "1.0.0"

entity_definitions:
  contract_terms:
    - term: "Force Majeure"
      category: "clause_type"
      extraction_hints: ["force majeure", "act of god", "unforeseeable circumstances"]

    - term: "Indemnification"
      category: "clause_type"
      extraction_hints: ["indemnify", "hold harmless", "defend"]

  legal_entities:
    - type: "Party"
      roles: ["plaintiff", "defendant", "third_party"]

    - type: "Counsel"
      roles: ["attorney", "counsel", "legal representative"]

extraction_priorities:
  - contract_terms
  - legal_entities
  - deadlines
  - monetary_values
```

### Domain-Specific Extraction Prompt

```markdown
# prompts/legal-entity-extraction.md

{{BASE_PROMPT}}

## Domain-Specific Instructions

You are extracting entities from a **legal** context transcript.

### Jurisdiction: {{jurisdiction}}
### Case Type: {{case_type}}

### Additional Entity Types to Extract

1. **Contract Terms**: Identify references to specific contract clauses
2. **Legal Deadlines**: Extract any mentioned deadlines or time limits
3. **Monetary Values**: Capture all monetary amounts with currency
4. **Party References**: Track references to legal parties

### Confidence Scoring Adjustments

- Increase confidence for entities matching domain definitions
- Decrease confidence for ambiguous legal terminology
- Flag for human review if entity could have multiple legal interpretations
```

---

## Integration with Orchestration

```yaml
# Example orchestration plan with context injection
orchestration:
  name: "Legal Transcript Analysis"
  version: "1.0.0"

context_injection:
  domain: "legal"
  context_files:
    - path: contexts/legal-terms.yaml
      type: entity_definitions
    - path: contexts/legal-extraction-rules.md
      type: extraction_rules
  prompt_overrides:
    entity_extraction:
      template: prompts/legal-entity-extraction.md
      variables:
        jurisdiction: "{{input.jurisdiction}}"
        case_type: "{{input.case_type}}"

pipeline:
  - stage: parse
    agent: transcript-parser
    context_injection: false  # Standard parsing

  - stage: extract
    agent: ps-analyst  # Existing Jerry agent
    context_injection: true  # Apply legal context

  - stage: synthesize
    agent: ps-synthesizer  # Existing Jerry agent
    context_injection: true  # Include domain context
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-006 | Design specification required |
| Depends On | EN-010 | Artifact packaging for metadata |

### Related Enablers

- EN-006: Context Injection Design (FEAT-001)
- Jerry problem-solving skill agents

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Architecture) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
