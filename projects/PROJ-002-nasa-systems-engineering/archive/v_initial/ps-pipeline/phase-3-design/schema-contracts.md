# JSON Schema Contracts for Agent Handoffs

> **Document ID:** ps-d-002
> **Phase:** 3 - Design (ps-* Pipeline)
> **Project:** PROJ-002-nasa-systems-engineering
> **Date:** 2026-01-10
> **Agent:** ps-architect
> **Topic:** Schema Contracts

---

## L0: Executive Summary

This document defines the JSON Schema contracts that enable reliable agent-to-agent handoffs in the Jerry Framework. Think of these schemas as "shipping labels" that ensure agents can pass work to each other without losing information or misunderstanding what they received.

We define three categories of schemas:
1. **Session Context** - The envelope that wraps all agent handoffs (already exists, extended here)
2. **Agent Output Schemas** - Specific formats for what each of the 16 agents produces
3. **Common Types** - Reusable building blocks shared across schemas

These contracts ensure that when an nse-requirements agent hands work to an nse-verification agent, both understand exactly what data to expect, what's required vs optional, and how to validate correctness.

---

## L1: Technical Specification

### 1. Schema Architecture Overview

```
docs/schemas/
├── session_context.json          # Master envelope schema (exists, v1.0.0)
├── common/
│   ├── types.json                # Shared type definitions
│   ├── findings.json             # Finding/question/blocker types
│   └── artifacts.json            # Artifact reference types
├── agents/
│   ├── ps/
│   │   ├── researcher_output.json
│   │   ├── analyst_output.json
│   │   ├── architect_output.json
│   │   ├── investigator_output.json
│   │   ├── reporter_output.json
│   │   ├── reviewer_output.json
│   │   ├── synthesizer_output.json
│   │   └── validator_output.json
│   └── nse/
│       ├── requirements_output.json
│       ├── risk_output.json
│       ├── architecture_output.json
│       ├── reviewer_output.json
│       ├── verification_output.json
│       ├── integration_output.json
│       ├── configuration_output.json
│       └── reporter_output.json
└── workflows/
    └── cross_pollination.json    # Cross-family handoff extensions
```

### 2. Session Context Schema (Extended v1.1.0)

The existing `session_context.json` (v1.0.0) provides the foundation. This design extends it with agent-specific payload validation.

#### 2.1 Schema Version Strategy

| Version | Breaking Change? | Description |
|---------|------------------|-------------|
| 1.0.0 | N/A | Initial release |
| 1.1.0 | No | Add `payload_schema_ref` field for agent-specific validation |
| 1.2.0 | No | Add `workflow_state` for cross-pollination tracking |
| 2.0.0 | Yes | Reserved for major restructure if needed |

#### 2.2 Extended Session Context (v1.1.0 Additions)

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/session_context/v1.1.0",
  "title": "Session Context Schema v1.1.0",
  "description": "Extended schema with agent-specific payload validation and cross-pollination support",
  "type": "object",
  "required": ["schema_version", "session_id", "source_agent", "target_agent", "payload", "timestamp"],
  "properties": {
    "schema_version": {
      "type": "string",
      "pattern": "^1\\.[0-9]+\\.[0-9]+$",
      "description": "Schema version (semver, must be 1.x.x for backward compatibility)"
    },
    "payload_schema_ref": {
      "type": "string",
      "description": "URI reference to agent-specific output schema for payload validation",
      "format": "uri-reference",
      "examples": [
        "agents/nse/requirements_output.json",
        "agents/ps/architect_output.json"
      ]
    },
    "workflow_state": {
      "$ref": "#/definitions/workflow_state",
      "description": "Cross-pollination workflow tracking (optional)"
    }
  },
  "definitions": {
    "workflow_state": {
      "type": "object",
      "description": "Tracks position in cross-pollination workflow",
      "properties": {
        "workflow_id": {
          "type": "string",
          "pattern": "^WF-[A-Z]{3}-\\d{3}$",
          "description": "Workflow instance identifier"
        },
        "phase": {
          "type": "string",
          "enum": ["research", "analysis", "design", "synthesis", "validation"],
          "description": "Current workflow phase"
        },
        "step_number": {
          "type": "integer",
          "minimum": 1,
          "description": "Sequential step in workflow"
        },
        "total_steps": {
          "type": "integer",
          "minimum": 1,
          "description": "Total steps in workflow"
        },
        "cross_family_handoff": {
          "type": "boolean",
          "description": "True if this handoff crosses ps/nse boundary"
        },
        "sync_barrier": {
          "type": "object",
          "description": "Synchronization point for parallel agents",
          "properties": {
            "barrier_id": {
              "type": "string"
            },
            "agents_expected": {
              "type": "array",
              "items": { "type": "string" }
            },
            "agents_completed": {
              "type": "array",
              "items": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

### 3. Common Type Definitions

#### 3.1 Base Types (common/types.json)

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/common/types.json",
  "title": "Common Type Definitions",
  "description": "Reusable types for agent output schemas",
  "definitions": {
    "agent_id": {
      "type": "string",
      "pattern": "^(ps|nse|orch)-[a-z]+(-[a-z]+)*$",
      "description": "Agent identifier following family-role pattern",
      "examples": ["ps-researcher", "nse-requirements", "orch-planner"]
    },
    "project_id": {
      "type": "string",
      "pattern": "^PROJ-\\d{3}(-[a-z0-9-]+)?$",
      "description": "Project identifier",
      "examples": ["PROJ-002", "PROJ-002-nasa-systems-engineering"]
    },
    "entry_id": {
      "type": "string",
      "pattern": "^e-\\d+$",
      "description": "Entry identifier within a problem-solving session",
      "examples": ["e-001", "e-042"]
    },
    "requirement_id": {
      "type": "string",
      "pattern": "^REQ-[A-Z]{3}-\\d{3}$",
      "description": "Requirement identifier",
      "examples": ["REQ-NSE-001", "REQ-SYS-042"]
    },
    "risk_id": {
      "type": "string",
      "pattern": "^RISK-\\d{3}$",
      "description": "Risk identifier",
      "examples": ["RISK-001", "RISK-042"]
    },
    "test_id": {
      "type": "string",
      "pattern": "^TST-[A-Z]{3}-\\d{3}$",
      "description": "Test case identifier",
      "examples": ["TST-VER-001", "TST-INT-042"]
    },
    "interface_id": {
      "type": "string",
      "pattern": "^IF-[A-Z]{3}-\\d{3}$",
      "description": "Interface identifier",
      "examples": ["IF-SYS-001", "IF-HW-042"]
    },
    "cognitive_mode": {
      "type": "string",
      "enum": ["convergent", "divergent", "mixed"],
      "description": "Agent's cognitive processing mode"
    },
    "severity": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Severity/priority level"
    },
    "confidence_score": {
      "type": "object",
      "required": ["overall"],
      "properties": {
        "overall": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0,
          "description": "Overall confidence (0-1)"
        },
        "reasoning": {
          "type": "string",
          "description": "Explanation for confidence level"
        },
        "breakdown": {
          "type": "object",
          "additionalProperties": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0
          },
          "description": "Component confidence scores"
        }
      }
    },
    "artifact_reference": {
      "type": "object",
      "required": ["path", "type"],
      "properties": {
        "path": {
          "type": "string",
          "description": "Repository-relative path to artifact"
        },
        "type": {
          "type": "string",
          "enum": [
            "requirement", "risk", "architecture", "verification",
            "review", "integration", "configuration", "report",
            "analysis", "synthesis", "research", "decision"
          ]
        },
        "format": {
          "type": "string",
          "enum": ["markdown", "yaml", "json", "text"],
          "default": "markdown"
        },
        "size_bytes": {
          "type": "integer",
          "minimum": 0
        },
        "checksum": {
          "type": "string",
          "pattern": "^sha256:[a-f0-9]{64}$",
          "description": "SHA-256 checksum for integrity verification"
        }
      }
    },
    "nasa_process_reference": {
      "type": "object",
      "required": ["process_number", "name"],
      "properties": {
        "process_number": {
          "type": "integer",
          "minimum": 1,
          "maximum": 17,
          "description": "NPR 7123.1D process number (1-17)"
        },
        "name": {
          "type": "string",
          "description": "Process name"
        },
        "npr_section": {
          "type": "string",
          "pattern": "^\\d+\\.\\d+(\\.\\d+)?$",
          "description": "NPR section reference"
        }
      }
    },
    "output_level": {
      "type": "object",
      "description": "Multi-level output structure per template requirements",
      "properties": {
        "l0_eli5": {
          "type": "string",
          "description": "Executive/non-technical summary",
          "maxLength": 1000
        },
        "l1_technical": {
          "type": "string",
          "description": "Software engineer implementation focus"
        },
        "l2_strategic": {
          "type": "string",
          "description": "Principal architect strategic perspective"
        }
      }
    }
  }
}
```

### 4. Agent Output Schemas

#### 4.1 ps-researcher Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/ps/researcher_output.json",
  "title": "PS Researcher Output Schema",
  "description": "Output schema for ps-researcher agent (divergent research)",
  "type": "object",
  "required": ["agent_id", "research_topic", "findings", "sources", "confidence"],
  "properties": {
    "agent_id": {
      "const": "ps-researcher"
    },
    "cognitive_mode": {
      "const": "divergent"
    },
    "research_topic": {
      "type": "string",
      "description": "Topic researched"
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "summary", "category"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^F-[0-9]{3}$"
          },
          "summary": {
            "type": "string",
            "maxLength": 500
          },
          "category": {
            "type": "string",
            "enum": ["insight", "pattern", "gap", "prior_art", "best_practice"]
          },
          "evidence": {
            "type": "array",
            "items": { "type": "string" }
          },
          "relevance_score": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        }
      },
      "minItems": 1
    },
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["title", "url_or_path"],
        "properties": {
          "title": { "type": "string" },
          "url_or_path": { "type": "string" },
          "source_type": {
            "type": "string",
            "enum": ["web", "file", "nasa_standard", "academic", "industry"]
          },
          "credibility": {
            "type": "string",
            "enum": ["authoritative", "reliable", "informational", "unverified"]
          }
        }
      }
    },
    "open_questions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "question"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^Q-[0-9]{3}$"
          },
          "question": { "type": "string" },
          "priority": { "$ref": "../../common/types.json#/definitions/severity" },
          "suggested_approach": { "type": "string" }
        }
      }
    },
    "research_gaps": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Areas requiring further investigation"
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["ps-analyst", "ps-architect", "nse-requirements"],
      "description": "Recommended next agent for processing"
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    }
  }
}
```

#### 4.2 ps-analyst Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/ps/analyst_output.json",
  "title": "PS Analyst Output Schema",
  "description": "Output schema for ps-analyst agent (convergent analysis)",
  "type": "object",
  "required": ["agent_id", "analysis_type", "conclusions", "confidence"],
  "properties": {
    "agent_id": {
      "const": "ps-analyst"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "analysis_type": {
      "type": "string",
      "enum": ["gap_analysis", "trade_study", "impact_assessment", "pattern_recognition", "synthesis"]
    },
    "input_sources": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Artifacts or agent outputs analyzed"
    },
    "conclusions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "conclusion", "evidence_basis"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^C-[0-9]{3}$"
          },
          "conclusion": { "type": "string" },
          "evidence_basis": {
            "type": "array",
            "items": { "type": "string" },
            "minItems": 1
          },
          "strength": {
            "type": "string",
            "enum": ["strong", "moderate", "weak", "speculative"]
          }
        }
      },
      "minItems": 1
    },
    "gaps_identified": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "description", "impact"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^GAP-[0-9]{3}$"
          },
          "description": { "type": "string" },
          "impact": { "$ref": "../../common/types.json#/definitions/severity" },
          "remediation": { "type": "string" }
        }
      }
    },
    "patterns": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "pattern_name": { "type": "string" },
          "occurrences": { "type": "integer", "minimum": 1 },
          "significance": { "type": "string" }
        }
      }
    },
    "recommendations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "recommendation", "priority"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^REC-[0-9]{3}$"
          },
          "recommendation": { "type": "string" },
          "priority": { "$ref": "../../common/types.json#/definitions/severity" },
          "rationale": { "type": "string" }
        }
      }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["ps-architect", "ps-synthesizer", "nse-architecture"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    }
  }
}
```

#### 4.3 ps-architect Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/ps/architect_output.json",
  "title": "PS Architect Output Schema",
  "description": "Output schema for ps-architect agent (ADR creation)",
  "type": "object",
  "required": ["agent_id", "adr", "confidence"],
  "properties": {
    "agent_id": {
      "const": "ps-architect"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "adr": {
      "type": "object",
      "required": ["number", "title", "status", "context", "decision", "consequences"],
      "properties": {
        "number": {
          "type": "string",
          "pattern": "^ADR-[0-9]{3}$"
        },
        "title": { "type": "string" },
        "status": {
          "type": "string",
          "enum": ["PROPOSED", "ACCEPTED", "DEPRECATED", "SUPERSEDED"],
          "default": "PROPOSED"
        },
        "context": {
          "type": "string",
          "description": "Problem/motivation for decision"
        },
        "decision": {
          "type": "string",
          "description": "The chosen solution"
        },
        "consequences": {
          "type": "object",
          "properties": {
            "positive": {
              "type": "array",
              "items": { "type": "string" }
            },
            "negative": {
              "type": "array",
              "items": { "type": "string" }
            },
            "neutral": {
              "type": "array",
              "items": { "type": "string" }
            }
          }
        },
        "options_considered": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "pros", "cons"],
            "properties": {
              "name": { "type": "string" },
              "pros": {
                "type": "array",
                "items": { "type": "string" }
              },
              "cons": {
                "type": "array",
                "items": { "type": "string" }
              },
              "score": {
                "type": "integer",
                "minimum": 1,
                "maximum": 10
              },
              "chosen": { "type": "boolean" }
            }
          },
          "minItems": 2
        },
        "supersedes": {
          "type": "string",
          "pattern": "^ADR-[0-9]{3}$"
        },
        "superseded_by": {
          "type": "string",
          "pattern": "^ADR-[0-9]{3}$"
        }
      }
    },
    "implementation_notes": {
      "type": "string",
      "description": "Technical implementation guidance"
    },
    "migration_steps": {
      "type": "array",
      "items": { "type": "string" }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["ps-validator", "ps-reviewer", "nse-architecture"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    }
  }
}
```

#### 4.4 ps-investigator Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/ps/investigator_output.json",
  "title": "PS Investigator Output Schema",
  "description": "Output schema for ps-investigator agent (root cause analysis)",
  "type": "object",
  "required": ["agent_id", "investigation_subject", "root_causes", "confidence"],
  "properties": {
    "agent_id": {
      "const": "ps-investigator"
    },
    "cognitive_mode": {
      "const": "divergent"
    },
    "investigation_subject": {
      "type": "string",
      "description": "Issue or problem being investigated"
    },
    "symptoms": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Observable symptoms of the issue"
    },
    "root_causes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "cause", "evidence", "likelihood"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^RC-[0-9]{3}$"
          },
          "cause": { "type": "string" },
          "evidence": {
            "type": "array",
            "items": { "type": "string" },
            "minItems": 1
          },
          "likelihood": {
            "type": "string",
            "enum": ["confirmed", "likely", "possible", "unlikely"]
          },
          "contributing_factors": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      },
      "minItems": 1
    },
    "investigation_timeline": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "timestamp": { "type": "string", "format": "date-time" },
          "event": { "type": "string" },
          "significance": { "type": "string" }
        }
      }
    },
    "remediation_options": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["option", "addresses_cause"],
        "properties": {
          "option": { "type": "string" },
          "addresses_cause": {
            "type": "array",
            "items": { "type": "string" }
          },
          "effort": {
            "type": "string",
            "enum": ["trivial", "low", "medium", "high", "significant"]
          },
          "risk": { "$ref": "../../common/types.json#/definitions/severity" }
        }
      }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["ps-architect", "ps-analyst", "nse-risk"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    }
  }
}
```

#### 4.5 ps-reporter Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/ps/reporter_output.json",
  "title": "PS Reporter Output Schema",
  "description": "Output schema for ps-reporter agent (status synthesis)",
  "type": "object",
  "required": ["agent_id", "report_type", "executive_summary", "status"],
  "properties": {
    "agent_id": {
      "const": "ps-reporter"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "report_type": {
      "type": "string",
      "enum": ["status", "progress", "milestone", "incident", "summary"]
    },
    "executive_summary": {
      "type": "string",
      "maxLength": 1000,
      "description": "L0-level summary for executives"
    },
    "status": {
      "type": "string",
      "enum": ["on_track", "at_risk", "blocked", "completed", "cancelled"]
    },
    "metrics": {
      "type": "object",
      "properties": {
        "tasks_completed": { "type": "integer", "minimum": 0 },
        "tasks_in_progress": { "type": "integer", "minimum": 0 },
        "tasks_blocked": { "type": "integer", "minimum": 0 },
        "completion_percentage": {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        }
      }
    },
    "key_accomplishments": {
      "type": "array",
      "items": { "type": "string" }
    },
    "blockers": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["description", "severity"],
        "properties": {
          "description": { "type": "string" },
          "severity": { "$ref": "../../common/types.json#/definitions/severity" },
          "owner": { "type": "string" },
          "eta_resolution": { "type": "string", "format": "date" }
        }
      }
    },
    "next_steps": {
      "type": "array",
      "items": { "type": "string" }
    },
    "risks_escalated": {
      "type": "array",
      "items": { "type": "string" }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    }
  }
}
```

#### 4.6 ps-reviewer Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/ps/reviewer_output.json",
  "title": "PS Reviewer Output Schema",
  "description": "Output schema for ps-reviewer agent (quality validation)",
  "type": "object",
  "required": ["agent_id", "review_subject", "review_criteria", "findings", "verdict"],
  "properties": {
    "agent_id": {
      "const": "ps-reviewer"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "review_subject": {
      "type": "string",
      "description": "Artifact or work product reviewed"
    },
    "review_criteria": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["criterion", "result"],
        "properties": {
          "criterion": { "type": "string" },
          "result": {
            "type": "string",
            "enum": ["pass", "fail", "partial", "not_applicable"]
          },
          "notes": { "type": "string" }
        }
      },
      "minItems": 1
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type", "description"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^RVW-[0-9]{3}$"
          },
          "type": {
            "type": "string",
            "enum": ["defect", "improvement", "question", "observation"]
          },
          "severity": { "$ref": "../../common/types.json#/definitions/severity" },
          "description": { "type": "string" },
          "location": { "type": "string" },
          "suggested_fix": { "type": "string" }
        }
      }
    },
    "verdict": {
      "type": "string",
      "enum": ["approved", "approved_with_comments", "needs_revision", "rejected"]
    },
    "revision_required": {
      "type": "boolean"
    },
    "blocking_issues_count": {
      "type": "integer",
      "minimum": 0
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["ps-validator", "ps-synthesizer", null]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    }
  }
}
```

#### 4.7 ps-synthesizer Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/ps/synthesizer_output.json",
  "title": "PS Synthesizer Output Schema",
  "description": "Output schema for ps-synthesizer agent (multi-source integration)",
  "type": "object",
  "required": ["agent_id", "sources_integrated", "synthesis", "confidence"],
  "properties": {
    "agent_id": {
      "const": "ps-synthesizer"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "sources_integrated": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source", "contribution"],
        "properties": {
          "source": { "type": "string" },
          "agent_id": { "$ref": "../../common/types.json#/definitions/agent_id" },
          "contribution": { "type": "string" }
        }
      },
      "minItems": 2
    },
    "synthesis": {
      "type": "object",
      "required": ["narrative", "key_themes"],
      "properties": {
        "narrative": {
          "type": "string",
          "description": "Integrated narrative from all sources"
        },
        "key_themes": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "contradictions_resolved": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "sources": {
                "type": "array",
                "items": { "type": "string" }
              },
              "contradiction": { "type": "string" },
              "resolution": { "type": "string" }
            }
          }
        },
        "gaps_remaining": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "coherence_assessment": {
      "type": "object",
      "properties": {
        "score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "issues": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["ps-reporter", "ps-reviewer", "nse-reporter"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    }
  }
}
```

#### 4.8 ps-validator Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/ps/validator_output.json",
  "title": "PS Validator Output Schema",
  "description": "Output schema for ps-validator agent (correctness verification)",
  "type": "object",
  "required": ["agent_id", "validation_subject", "test_results", "validation_verdict"],
  "properties": {
    "agent_id": {
      "const": "ps-validator"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "validation_subject": {
      "type": "string",
      "description": "What is being validated"
    },
    "validation_scope": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Aspects covered by validation"
    },
    "test_results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["test_id", "description", "result"],
        "properties": {
          "test_id": { "type": "string" },
          "description": { "type": "string" },
          "result": {
            "type": "string",
            "enum": ["pass", "fail", "skip", "error"]
          },
          "expected": { "type": "string" },
          "actual": { "type": "string" },
          "error_message": { "type": "string" }
        }
      }
    },
    "validation_verdict": {
      "type": "string",
      "enum": ["valid", "invalid", "partial", "inconclusive"]
    },
    "coverage": {
      "type": "object",
      "properties": {
        "total_tests": { "type": "integer", "minimum": 0 },
        "passed": { "type": "integer", "minimum": 0 },
        "failed": { "type": "integer", "minimum": 0 },
        "skipped": { "type": "integer", "minimum": 0 },
        "coverage_percentage": {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        }
      }
    },
    "blocking_failures": {
      "type": "array",
      "items": { "type": "string" }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["ps-reporter", "ps-reviewer", "nse-verification"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    }
  }
}
```

### 5. NSE Agent Output Schemas

#### 5.1 nse-requirements Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/nse/requirements_output.json",
  "title": "NSE Requirements Output Schema",
  "description": "Output schema for nse-requirements agent (NASA SE requirements)",
  "type": "object",
  "required": ["agent_id", "nasa_processes", "requirements", "traceability", "confidence"],
  "properties": {
    "agent_id": {
      "const": "nse-requirements"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "nasa_processes": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/nasa_process_reference" },
      "description": "NPR 7123.1D processes applied"
    },
    "stakeholder_needs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "stakeholder", "need", "priority"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^STK-[0-9]{3}$"
          },
          "stakeholder": { "type": "string" },
          "need": { "type": "string" },
          "priority": {
            "type": "string",
            "enum": ["high", "medium", "low"]
          },
          "source": { "type": "string" }
        }
      }
    },
    "requirements": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "requirement", "rationale", "verification_method", "priority"],
        "properties": {
          "id": { "$ref": "../../common/types.json#/definitions/requirement_id" },
          "requirement": {
            "type": "string",
            "description": "Formal shall statement",
            "pattern": ".*shall.*"
          },
          "rationale": { "type": "string" },
          "parent_need": {
            "type": "string",
            "pattern": "^STK-[0-9]{3}$"
          },
          "verification_method": {
            "type": "string",
            "enum": ["Analysis", "Demonstration", "Inspection", "Test"],
            "description": "ADIT verification method"
          },
          "priority": {
            "type": "string",
            "enum": ["Must", "Should", "Could", "Wont"]
          },
          "status": {
            "type": "string",
            "enum": ["Draft", "Under Review", "Approved", "Deprecated"]
          },
          "allocated_to": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      },
      "minItems": 1
    },
    "traceability": {
      "type": "object",
      "properties": {
        "coverage_status": {
          "type": "string",
          "enum": ["complete", "partial", "incomplete"]
        },
        "orphan_requirements": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Requirements without parent traces"
        },
        "unverified_requirements": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Requirements without verification method"
        }
      }
    },
    "quality_assessment": {
      "type": "object",
      "properties": {
        "complete": { "type": "boolean" },
        "consistent": { "type": "boolean" },
        "verifiable": { "type": "boolean" },
        "traceable": { "type": "boolean" },
        "unambiguous": { "type": "boolean" },
        "issues": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["nse-verification", "nse-architecture", "nse-integration"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    },
    "disclaimer_included": {
      "type": "boolean",
      "const": true,
      "description": "P-043: Mandatory disclaimer present"
    }
  }
}
```

#### 5.2 nse-risk Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/nse/risk_output.json",
  "title": "NSE Risk Output Schema",
  "description": "Output schema for nse-risk agent (NASA SE risk management)",
  "type": "object",
  "required": ["agent_id", "nasa_processes", "risks", "risk_matrix", "confidence"],
  "properties": {
    "agent_id": {
      "const": "nse-risk"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "nasa_processes": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/nasa_process_reference" }
    },
    "risks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "likelihood", "consequence", "risk_score"],
        "properties": {
          "id": { "$ref": "../../common/types.json#/definitions/risk_id" },
          "title": { "type": "string" },
          "description": { "type": "string" },
          "category": {
            "type": "string",
            "enum": ["technical", "cost", "schedule", "programmatic", "safety"]
          },
          "likelihood": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5,
            "description": "1=Remote, 2=Unlikely, 3=Possible, 4=Likely, 5=Near Certain"
          },
          "consequence": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5,
            "description": "1=Minimal, 2=Minor, 3=Moderate, 4=Significant, 5=Catastrophic"
          },
          "risk_score": {
            "type": "integer",
            "minimum": 1,
            "maximum": 25,
            "description": "Likelihood x Consequence"
          },
          "risk_level": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"]
          },
          "condition": {
            "type": "string",
            "description": "If [condition]..."
          },
          "consequence_statement": {
            "type": "string",
            "description": "...then [consequence]"
          },
          "mitigation_strategy": {
            "type": "string",
            "enum": ["accept", "avoid", "mitigate", "transfer", "watch"]
          },
          "mitigations": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["action", "owner", "status"],
              "properties": {
                "action": { "type": "string" },
                "owner": { "type": "string" },
                "due_date": { "type": "string", "format": "date" },
                "status": {
                  "type": "string",
                  "enum": ["planned", "in_progress", "completed", "cancelled"]
                },
                "effectiveness": {
                  "type": "string",
                  "enum": ["high", "medium", "low", "unknown"]
                }
              }
            }
          },
          "residual_likelihood": { "type": "integer", "minimum": 1, "maximum": 5 },
          "residual_consequence": { "type": "integer", "minimum": 1, "maximum": 5 },
          "residual_risk_score": { "type": "integer", "minimum": 1, "maximum": 25 },
          "traced_to_requirements": {
            "type": "array",
            "items": { "$ref": "../../common/types.json#/definitions/requirement_id" }
          }
        }
      }
    },
    "risk_matrix": {
      "type": "object",
      "description": "5x5 Risk matrix summary",
      "properties": {
        "critical_risks": { "type": "integer", "minimum": 0 },
        "high_risks": { "type": "integer", "minimum": 0 },
        "medium_risks": { "type": "integer", "minimum": 0 },
        "low_risks": { "type": "integer", "minimum": 0 }
      }
    },
    "risk_trends": {
      "type": "object",
      "properties": {
        "new_risks": { "type": "integer", "minimum": 0 },
        "closed_risks": { "type": "integer", "minimum": 0 },
        "elevated_risks": { "type": "integer", "minimum": 0 },
        "reduced_risks": { "type": "integer", "minimum": 0 }
      }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["nse-requirements", "nse-reviewer", "nse-reporter"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    },
    "disclaimer_included": {
      "type": "boolean",
      "const": true
    }
  }
}
```

#### 5.3 nse-architecture Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/nse/architecture_output.json",
  "title": "NSE Architecture Output Schema",
  "description": "Output schema for nse-architecture agent (NASA SE architecture design)",
  "type": "object",
  "required": ["agent_id", "nasa_processes", "architecture", "trade_studies", "confidence"],
  "properties": {
    "agent_id": {
      "const": "nse-architecture"
    },
    "cognitive_mode": {
      "const": "divergent"
    },
    "nasa_processes": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/nasa_process_reference" }
    },
    "architecture": {
      "type": "object",
      "required": ["system_elements", "functional_decomposition"],
      "properties": {
        "system_elements": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "name", "type"],
            "properties": {
              "id": {
                "type": "string",
                "pattern": "^SE-[A-Z]{3}-[0-9]{3}$"
              },
              "name": { "type": "string" },
              "type": {
                "type": "string",
                "enum": ["system", "segment", "element", "subsystem", "component"]
              },
              "parent": { "type": "string" },
              "allocated_requirements": {
                "type": "array",
                "items": { "$ref": "../../common/types.json#/definitions/requirement_id" }
              }
            }
          }
        },
        "functional_decomposition": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["function_id", "name"],
            "properties": {
              "function_id": {
                "type": "string",
                "pattern": "^FN-[0-9]{3}$"
              },
              "name": { "type": "string" },
              "description": { "type": "string" },
              "allocated_to": { "type": "string" }
            }
          }
        },
        "interfaces": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "name", "source", "destination"],
            "properties": {
              "id": { "$ref": "../../common/types.json#/definitions/interface_id" },
              "name": { "type": "string" },
              "source": { "type": "string" },
              "destination": { "type": "string" },
              "type": {
                "type": "string",
                "enum": ["mechanical", "electrical", "data", "thermal", "fluid"]
              },
              "icd_reference": { "type": "string" }
            }
          }
        }
      }
    },
    "trade_studies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "alternatives", "selected"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^TS-[0-9]{3}$"
          },
          "title": { "type": "string" },
          "criteria": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": { "type": "string" },
                "weight": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              }
            }
          },
          "alternatives": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["name", "scores"],
              "properties": {
                "name": { "type": "string" },
                "description": { "type": "string" },
                "scores": {
                  "type": "object",
                  "additionalProperties": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 10
                  }
                },
                "weighted_score": { "type": "number" }
              }
            },
            "minItems": 2
          },
          "selected": { "type": "string" },
          "rationale": { "type": "string" }
        }
      }
    },
    "design_decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["decision", "rationale"],
        "properties": {
          "decision": { "type": "string" },
          "rationale": { "type": "string" },
          "alternatives_considered": {
            "type": "array",
            "items": { "type": "string" }
          },
          "constraints": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["nse-integration", "nse-reviewer", "nse-verification"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    },
    "disclaimer_included": {
      "type": "boolean",
      "const": true
    }
  }
}
```

#### 5.4 nse-reviewer Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/nse/reviewer_output.json",
  "title": "NSE Reviewer Output Schema",
  "description": "Output schema for nse-reviewer agent (NASA SE technical assessment)",
  "type": "object",
  "required": ["agent_id", "nasa_processes", "review_type", "assessment", "rrids", "verdict"],
  "properties": {
    "agent_id": {
      "const": "nse-reviewer"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "nasa_processes": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/nasa_process_reference" }
    },
    "review_type": {
      "type": "string",
      "enum": ["SRR", "SDR", "PDR", "CDR", "TRR", "ORR", "FRR", "peer_review", "technical_assessment"],
      "description": "NASA review type per NPR 7123.1D"
    },
    "review_subject": {
      "type": "string"
    },
    "assessment": {
      "type": "object",
      "required": ["entry_criteria_met", "exit_criteria_met"],
      "properties": {
        "entry_criteria_met": { "type": "boolean" },
        "exit_criteria_met": { "type": "boolean" },
        "criteria_details": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["criterion", "status"],
            "properties": {
              "criterion": { "type": "string" },
              "status": {
                "type": "string",
                "enum": ["met", "partially_met", "not_met", "not_applicable"]
              },
              "evidence": { "type": "string" },
              "notes": { "type": "string" }
            }
          }
        }
      }
    },
    "rrids": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "type", "severity", "status"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^RRID-[0-9]{3}$",
            "description": "Review Report Item Discrepancy ID"
          },
          "title": { "type": "string" },
          "description": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["action", "concern", "observation", "recommendation"]
          },
          "severity": { "$ref": "../../common/types.json#/definitions/severity" },
          "status": {
            "type": "string",
            "enum": ["open", "in_progress", "closed", "deferred"]
          },
          "owner": { "type": "string" },
          "due_date": { "type": "string", "format": "date" },
          "resolution": { "type": "string" }
        }
      },
      "description": "Review Report Item Discrepancies (NASA review findings)"
    },
    "verdict": {
      "type": "string",
      "enum": ["proceed", "proceed_with_rfa", "conditional", "no_proceed"],
      "description": "Review board verdict"
    },
    "recommendations": {
      "type": "array",
      "items": { "type": "string" }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["nse-reporter", "nse-configuration", null]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    },
    "disclaimer_included": {
      "type": "boolean",
      "const": true
    }
  }
}
```

#### 5.5 nse-verification Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/nse/verification_output.json",
  "title": "NSE Verification Output Schema",
  "description": "Output schema for nse-verification agent (NASA SE V&V)",
  "type": "object",
  "required": ["agent_id", "nasa_processes", "verification_matrix", "test_cases", "confidence"],
  "properties": {
    "agent_id": {
      "const": "nse-verification"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "nasa_processes": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/nasa_process_reference" }
    },
    "verification_matrix": {
      "type": "object",
      "description": "Requirements to Verification Cross-Reference Matrix (VCRM)",
      "properties": {
        "total_requirements": { "type": "integer", "minimum": 0 },
        "requirements_verified": { "type": "integer", "minimum": 0 },
        "coverage_percentage": {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        },
        "entries": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["requirement_id", "verification_method", "status"],
            "properties": {
              "requirement_id": { "$ref": "../../common/types.json#/definitions/requirement_id" },
              "verification_method": {
                "type": "string",
                "enum": ["Analysis", "Demonstration", "Inspection", "Test"]
              },
              "test_id": { "$ref": "../../common/types.json#/definitions/test_id" },
              "status": {
                "type": "string",
                "enum": ["not_started", "in_progress", "passed", "failed", "blocked", "waived"]
              },
              "evidence": { "type": "string" }
            }
          }
        }
      }
    },
    "test_cases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "verifies", "procedure"],
        "properties": {
          "id": { "$ref": "../../common/types.json#/definitions/test_id" },
          "title": { "type": "string" },
          "description": { "type": "string" },
          "verifies": {
            "type": "array",
            "items": { "$ref": "../../common/types.json#/definitions/requirement_id" },
            "minItems": 1
          },
          "preconditions": {
            "type": "array",
            "items": { "type": "string" }
          },
          "procedure": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["step", "action"],
              "properties": {
                "step": { "type": "integer", "minimum": 1 },
                "action": { "type": "string" },
                "expected_result": { "type": "string" }
              }
            },
            "minItems": 1
          },
          "pass_criteria": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["planned", "ready", "executed", "passed", "failed"]
          },
          "execution_date": { "type": "string", "format": "date" },
          "actual_result": { "type": "string" },
          "defects_found": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "validation_activities": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["activity", "objective"],
        "properties": {
          "activity": { "type": "string" },
          "objective": { "type": "string" },
          "stakeholder_involvement": { "type": "boolean" },
          "status": {
            "type": "string",
            "enum": ["planned", "in_progress", "completed"]
          },
          "outcome": { "type": "string" }
        }
      }
    },
    "defect_summary": {
      "type": "object",
      "properties": {
        "total_defects": { "type": "integer", "minimum": 0 },
        "critical_defects": { "type": "integer", "minimum": 0 },
        "open_defects": { "type": "integer", "minimum": 0 },
        "closed_defects": { "type": "integer", "minimum": 0 }
      }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["nse-reviewer", "nse-reporter", "nse-configuration"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    },
    "disclaimer_included": {
      "type": "boolean",
      "const": true
    }
  }
}
```

#### 5.6 nse-integration Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/nse/integration_output.json",
  "title": "NSE Integration Output Schema",
  "description": "Output schema for nse-integration agent (NASA SE integration and interfaces)",
  "type": "object",
  "required": ["agent_id", "nasa_processes", "interfaces", "n2_diagram", "confidence"],
  "properties": {
    "agent_id": {
      "const": "nse-integration"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "nasa_processes": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/nasa_process_reference" }
    },
    "interfaces": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type", "source", "destination", "status"],
        "properties": {
          "id": { "$ref": "../../common/types.json#/definitions/interface_id" },
          "name": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["mechanical", "electrical", "data", "thermal", "fluid", "optical", "rf"]
          },
          "source": {
            "type": "object",
            "required": ["element", "port"],
            "properties": {
              "element": { "type": "string" },
              "port": { "type": "string" }
            }
          },
          "destination": {
            "type": "object",
            "required": ["element", "port"],
            "properties": {
              "element": { "type": "string" },
              "port": { "type": "string" }
            }
          },
          "icd_version": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["defined", "agreed", "verified", "controlled"]
          },
          "owner": { "type": "string" },
          "characteristics": {
            "type": "object",
            "additionalProperties": true,
            "description": "Interface-specific parameters (data rate, voltage, force, etc.)"
          }
        }
      }
    },
    "n2_diagram": {
      "type": "object",
      "description": "N-squared (N2) interface diagram data",
      "properties": {
        "elements": {
          "type": "array",
          "items": { "type": "string" }
        },
        "matrix": {
          "type": "array",
          "items": {
            "type": "array",
            "items": {
              "type": ["string", "null"]
            }
          }
        },
        "diagram_reference": { "type": "string" }
      }
    },
    "integration_plan": {
      "type": "object",
      "properties": {
        "strategy": {
          "type": "string",
          "enum": ["bottom_up", "top_down", "big_bang", "incremental", "sandwich"]
        },
        "phases": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["phase", "elements"],
            "properties": {
              "phase": { "type": "integer", "minimum": 1 },
              "name": { "type": "string" },
              "elements": {
                "type": "array",
                "items": { "type": "string" }
              },
              "interfaces_verified": {
                "type": "array",
                "items": { "$ref": "../../common/types.json#/definitions/interface_id" }
              },
              "dependencies": {
                "type": "array",
                "items": { "type": "integer" }
              }
            }
          }
        }
      }
    },
    "interface_issues": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "interface_id", "description", "severity"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^IFI-[0-9]{3}$"
          },
          "interface_id": { "$ref": "../../common/types.json#/definitions/interface_id" },
          "description": { "type": "string" },
          "severity": { "$ref": "../../common/types.json#/definitions/severity" },
          "resolution": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["open", "in_progress", "resolved", "deferred"]
          }
        }
      }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["nse-verification", "nse-configuration", "nse-reviewer"]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    },
    "disclaimer_included": {
      "type": "boolean",
      "const": true
    }
  }
}
```

#### 5.7 nse-configuration Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/nse/configuration_output.json",
  "title": "NSE Configuration Output Schema",
  "description": "Output schema for nse-configuration agent (NASA SE configuration management)",
  "type": "object",
  "required": ["agent_id", "nasa_processes", "baselines", "configuration_items", "confidence"],
  "properties": {
    "agent_id": {
      "const": "nse-configuration"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "nasa_processes": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/nasa_process_reference" }
    },
    "baselines": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type", "status"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^BL-[A-Z]{3}-[0-9]{3}$"
          },
          "name": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["functional", "allocated", "product", "developmental", "operational"]
          },
          "description": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["draft", "proposed", "approved", "released", "superseded"]
          },
          "approval_date": { "type": "string", "format": "date" },
          "approver": { "type": "string" },
          "configuration_items": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    "configuration_items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type", "version", "status"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^CI-[A-Z]{3}-[0-9]{3}$"
          },
          "name": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["hardware", "software", "document", "interface", "data"]
          },
          "version": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["development", "under_change", "released", "obsolete"]
          },
          "baseline": { "type": "string" },
          "parent_ci": { "type": "string" },
          "child_cis": {
            "type": "array",
            "items": { "type": "string" }
          },
          "change_history": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "version": { "type": "string" },
                "date": { "type": "string", "format": "date" },
                "change_id": { "type": "string" },
                "description": { "type": "string" }
              }
            }
          }
        }
      }
    },
    "change_requests": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "type", "status"],
        "properties": {
          "id": {
            "type": "string",
            "pattern": "^CR-[0-9]{4}$"
          },
          "title": { "type": "string" },
          "description": { "type": "string" },
          "type": {
            "type": "string",
            "enum": ["engineering_change", "deviation", "waiver", "document_change"]
          },
          "priority": { "$ref": "../../common/types.json#/definitions/severity" },
          "status": {
            "type": "string",
            "enum": ["submitted", "under_review", "approved", "rejected", "implemented", "closed"]
          },
          "affected_cis": {
            "type": "array",
            "items": { "type": "string" }
          },
          "impact_assessment": { "type": "string" },
          "ccb_date": { "type": "string", "format": "date" },
          "disposition": { "type": "string" }
        }
      }
    },
    "cm_metrics": {
      "type": "object",
      "properties": {
        "total_cis": { "type": "integer", "minimum": 0 },
        "released_cis": { "type": "integer", "minimum": 0 },
        "pending_changes": { "type": "integer", "minimum": 0 },
        "average_change_cycle_days": { "type": "number", "minimum": 0 }
      }
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "next_agent_hint": {
      "type": "string",
      "enum": ["nse-reporter", "nse-reviewer", null]
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    },
    "disclaimer_included": {
      "type": "boolean",
      "const": true
    }
  }
}
```

#### 5.8 nse-reporter Output Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/agents/nse/reporter_output.json",
  "title": "NSE Reporter Output Schema",
  "description": "Output schema for nse-reporter agent (NASA SE status aggregation)",
  "type": "object",
  "required": ["agent_id", "nasa_processes", "report_type", "executive_summary", "se_metrics"],
  "properties": {
    "agent_id": {
      "const": "nse-reporter"
    },
    "cognitive_mode": {
      "const": "convergent"
    },
    "nasa_processes": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/nasa_process_reference" }
    },
    "report_type": {
      "type": "string",
      "enum": ["monthly_status", "review_package", "metrics_dashboard", "milestone_report", "risk_report"]
    },
    "reporting_period": {
      "type": "object",
      "properties": {
        "start_date": { "type": "string", "format": "date" },
        "end_date": { "type": "string", "format": "date" }
      }
    },
    "executive_summary": {
      "type": "string",
      "maxLength": 2000,
      "description": "L0 executive summary"
    },
    "se_metrics": {
      "type": "object",
      "description": "Systems Engineering metrics per NASA-HDBK-1009A",
      "properties": {
        "requirements": {
          "type": "object",
          "properties": {
            "total": { "type": "integer" },
            "approved": { "type": "integer" },
            "traced": { "type": "integer" },
            "verified": { "type": "integer" },
            "volatility_percentage": { "type": "number" }
          }
        },
        "risks": {
          "type": "object",
          "properties": {
            "total": { "type": "integer" },
            "critical": { "type": "integer" },
            "mitigated": { "type": "integer" },
            "burn_down_trend": {
              "type": "string",
              "enum": ["improving", "stable", "degrading"]
            }
          }
        },
        "verification": {
          "type": "object",
          "properties": {
            "total_tests": { "type": "integer" },
            "tests_passed": { "type": "integer" },
            "tests_failed": { "type": "integer" },
            "coverage_percentage": { "type": "number" }
          }
        },
        "interfaces": {
          "type": "object",
          "properties": {
            "total": { "type": "integer" },
            "defined": { "type": "integer" },
            "verified": { "type": "integer" },
            "issues_open": { "type": "integer" }
          }
        },
        "configuration": {
          "type": "object",
          "properties": {
            "baselines_established": { "type": "integer" },
            "pending_changes": { "type": "integer" },
            "ccb_actions_open": { "type": "integer" }
          }
        }
      }
    },
    "lifecycle_phase": {
      "type": "string",
      "enum": ["pre_phase_a", "phase_a", "phase_b", "phase_c", "phase_d", "phase_e", "phase_f"],
      "description": "NASA project lifecycle phase"
    },
    "upcoming_reviews": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "review_type": { "type": "string" },
          "scheduled_date": { "type": "string", "format": "date" },
          "readiness_status": {
            "type": "string",
            "enum": ["on_track", "at_risk", "not_ready"]
          }
        }
      }
    },
    "key_issues": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["issue", "severity", "status"],
        "properties": {
          "issue": { "type": "string" },
          "severity": { "$ref": "../../common/types.json#/definitions/severity" },
          "status": { "type": "string" },
          "owner": { "type": "string" },
          "action_required": { "type": "string" }
        }
      }
    },
    "source_agents": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/agent_id" },
      "description": "Agents whose outputs were aggregated"
    },
    "confidence": {
      "$ref": "../../common/types.json#/definitions/confidence_score"
    },
    "output_levels": {
      "$ref": "../../common/types.json#/definitions/output_level"
    },
    "artifacts": {
      "type": "array",
      "items": { "$ref": "../../common/types.json#/definitions/artifact_reference" }
    },
    "disclaimer_included": {
      "type": "boolean",
      "const": true
    }
  }
}
```

### 6. Validation Rules and Error Handling

#### 6.1 Validation Strategy

| Layer | Validation Type | Timing | Error Handling |
|-------|-----------------|--------|----------------|
| Schema | JSON Schema Draft-07 | Pre-parse | Reject with error details |
| Semantic | Business rules | Post-parse | Warn or reject based on severity |
| Constitutional | P-* principle checks | Post-parse | Enforce per principle tier |
| Cross-reference | ID existence checks | Post-parse | Warn with suggestions |

#### 6.2 Error Response Schema

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://jerry.dev/schemas/common/error.json",
  "title": "Validation Error Response",
  "type": "object",
  "required": ["error_code", "message", "severity"],
  "properties": {
    "error_code": {
      "type": "string",
      "pattern": "^(SCH|SEM|CON|REF)-[0-9]{3}$",
      "description": "SCH=Schema, SEM=Semantic, CON=Constitutional, REF=Cross-reference"
    },
    "message": {
      "type": "string",
      "description": "Human-readable error message"
    },
    "severity": {
      "type": "string",
      "enum": ["error", "warning", "info"]
    },
    "path": {
      "type": "string",
      "description": "JSON path to the problematic field"
    },
    "expected": {
      "description": "Expected value or pattern"
    },
    "actual": {
      "description": "Actual value received"
    },
    "remediation": {
      "type": "string",
      "description": "Suggested fix"
    },
    "constitutional_principle": {
      "type": "string",
      "pattern": "^P-[0-9]{3}$",
      "description": "Violated principle if applicable"
    }
  }
}
```

#### 6.3 Common Validation Errors

| Code | Severity | Message | Remediation |
|------|----------|---------|-------------|
| SCH-001 | error | Missing required field: {field} | Add the required field to payload |
| SCH-002 | error | Invalid type for {field}: expected {type} | Correct the field type |
| SCH-003 | error | Pattern mismatch for {field} | Use correct ID format (e.g., REQ-NSE-001) |
| SEM-001 | warning | Empty findings array | Add at least one finding |
| SEM-002 | warning | Confidence score unusually low (<0.3) | Review analysis quality |
| CON-001 | error | P-043: Disclaimer not included | Add mandatory disclaimer |
| CON-002 | error | P-040: Orphan requirements detected | Add parent traces |
| REF-001 | warning | Referenced artifact not found | Verify artifact path |
| REF-002 | warning | Referenced requirement ID unknown | Check requirement registry |

### 7. Schema Versioning Strategy

#### 7.1 Versioning Rules

1. **MAJOR** (X.0.0): Breaking changes requiring migration
   - Removing required fields
   - Changing field types
   - Renaming fields

2. **MINOR** (x.Y.0): Backward-compatible additions
   - New optional fields
   - New enum values
   - New definitions

3. **PATCH** (x.y.Z): Documentation and non-breaking fixes
   - Description updates
   - Example additions
   - Typo fixes

#### 7.2 Migration Support

```json
{
  "migrations": {
    "1.0.0_to_1.1.0": {
      "description": "Add payload_schema_ref and workflow_state",
      "automatic": true,
      "steps": [
        "Add payload_schema_ref: null (optional field)",
        "Add workflow_state: null (optional field)"
      ]
    },
    "1.1.0_to_2.0.0": {
      "description": "Reserved for breaking changes",
      "automatic": false,
      "migration_script": "scripts/migrate_schema_v2.py"
    }
  }
}
```

#### 7.3 Deprecation Policy

- **Announcement**: 2 minor versions before deprecation
- **Warning Period**: 1 minor version with runtime warnings
- **Removal**: Next major version

---

## L2: Strategic Implications

### 1. Cross-Pollination Architecture

The schema design enables seamless handoffs between ps-* and nse-* agent families through:

1. **Unified Session Context**: Both families use the same envelope schema
2. **Common Type Library**: Shared definitions prevent translation errors
3. **Family-Specific Extensions**: Each agent family can extend base types
4. **Cross-Family Workflow State**: `workflow_state.cross_family_handoff` flag triggers validation

#### Cross-Pollination Handoff Matrix

| Source Agent | Target Agent | Payload Mapping | Validation |
|--------------|--------------|-----------------|------------|
| ps-researcher | nse-requirements | findings -> stakeholder_needs | REQ-001 patterns |
| ps-analyst | nse-risk | gaps_identified -> risks | RISK format |
| ps-architect | nse-architecture | adr.decision -> design_decisions | Trade study format |
| ps-validator | nse-verification | test_results -> verification_matrix | Test ID mapping |
| nse-requirements | ps-reviewer | requirements -> review_subject | Review criteria |
| nse-risk | ps-investigator | risks -> investigation triggers | Root cause mapping |

### 2. Constitutional Compliance Integration

The schemas enforce constitutional principles through:

| Principle | Schema Enforcement |
|-----------|-------------------|
| P-002 (Persistence) | `artifacts` array required; file paths validated |
| P-003 (No Recursion) | `trace.depth` maximum enforced at 1 |
| P-022 (No Deception) | `confidence` required with reasoning |
| P-040 (Traceability) | Cross-reference IDs validated |
| P-043 (Disclaimer) | `disclaimer_included: true` for nse-* agents |

### 3. Evolution Path

#### Phase 1 (Current): Core Schemas
- Session context v1.1.0
- 16 agent output schemas
- Common type library

#### Phase 2 (Future): Advanced Features
- Async handoff support (message queuing)
- Schema composition for specialized workflows
- Runtime schema evolution

#### Phase 3 (Future): Intelligence Layer
- Schema-aware validation suggestions
- Automatic type coercion for minor mismatches
- Cross-reference auto-resolution

### 4. Implementation Recommendations

1. **Schema Registry Service**: Centralized schema storage with version management
2. **Validation Middleware**: Pre-flight validation before agent invocation
3. **Migration Tooling**: Automated schema upgrade scripts
4. **Documentation Generation**: Auto-generate API docs from schemas

---

## Example Payloads

### Example 1: ps-researcher to nse-requirements Handoff

```json
{
  "schema_version": "1.1.0",
  "session_id": "sess-2026-01-10-xyz789",
  "source_agent": {
    "id": "ps-researcher",
    "family": "ps",
    "cognitive_mode": "divergent",
    "model": "opus"
  },
  "target_agent": {
    "id": "nse-requirements",
    "family": "nse",
    "cognitive_mode": "convergent",
    "model": "sonnet"
  },
  "timestamp": "2026-01-10T14:30:00Z",
  "workflow_id": "WF-SAO-001",
  "payload_schema_ref": "agents/ps/researcher_output.json",
  "workflow_state": {
    "workflow_id": "WF-SAO-001",
    "phase": "research",
    "step_number": 1,
    "total_steps": 8,
    "cross_family_handoff": true
  },
  "payload": {
    "agent_id": "ps-researcher",
    "cognitive_mode": "divergent",
    "research_topic": "NASA SE Agent Best Practices",
    "findings": [
      {
        "id": "F-001",
        "summary": "Multi-agent systems benefit from hierarchical orchestration with 10% efficiency improvement",
        "category": "best_practice",
        "evidence": ["agent-research-004-persona-compatibility.md"],
        "relevance_score": 0.95
      },
      {
        "id": "F-002",
        "summary": "Cognitive mode diversity (divergent + convergent) prevents groupthink",
        "category": "insight",
        "evidence": ["agent-research-003-persona-theory.md"],
        "relevance_score": 0.88
      }
    ],
    "sources": [
      {
        "title": "Persona Theory Research",
        "url_or_path": "projects/PROJ-002/research/agent-research-003-persona-theory.md",
        "source_type": "file",
        "credibility": "reliable"
      }
    ],
    "open_questions": [
      {
        "id": "Q-001",
        "question": "How should cognitive modes transition during agent chaining?",
        "priority": "high",
        "suggested_approach": "Analyze successful multi-agent workflows"
      }
    ],
    "research_gaps": [
      "Optimal agent team size for SE workflows",
      "Metrics for measuring agent collaboration effectiveness"
    ],
    "confidence": {
      "overall": 0.82,
      "reasoning": "Strong primary source documentation, limited empirical validation",
      "breakdown": {
        "source_quality": 0.90,
        "coverage": 0.75,
        "recency": 0.80
      }
    },
    "next_agent_hint": "nse-requirements",
    "output_levels": {
      "l0_eli5": "Research found that NASA SE agents work best when different types (explorers vs analyzers) work together, similar to how a good team has both creative thinkers and detail-oriented reviewers.",
      "l1_technical": "Analysis of 20 agent definitions across three families (ps-*, nse-*, orchestrator) reveals consistent patterns for persona definition, tool access, and output formatting. Key finding: All nse-* agents are currently convergent-mode, missing divergent exploration phases recommended by persona theory.",
      "l2_strategic": "The cognitive mode homogeneity in nse-* agents represents a systematic gap that could lead to groupthink in trade studies and risk identification. Recommendation: Introduce divergent phases for nse-architecture and nse-risk agents, paired with Generator-Critic loops for quality improvement."
    },
    "artifacts": [
      {
        "path": "projects/PROJ-002/ps-pipeline/phase-1-research/agent-design.md",
        "type": "research",
        "format": "markdown",
        "size_bytes": 18500
      }
    ]
  },
  "trace": {
    "trace_id": "tr-SAO-001-2026-01-10",
    "span_id": "sp-001",
    "parent_span_id": null,
    "depth": 0
  }
}
```

### Example 2: nse-requirements Output

```json
{
  "agent_id": "nse-requirements",
  "cognitive_mode": "convergent",
  "nasa_processes": [
    {
      "process_number": 1,
      "name": "Stakeholder Expectations Definition",
      "npr_section": "3.2.1"
    },
    {
      "process_number": 2,
      "name": "Technical Requirements Definition",
      "npr_section": "3.2.2"
    }
  ],
  "stakeholder_needs": [
    {
      "id": "STK-001",
      "stakeholder": "SE Framework User",
      "need": "Reliable agent handoffs without data loss",
      "priority": "high",
      "source": "ps-researcher F-001"
    },
    {
      "id": "STK-002",
      "stakeholder": "Orchestrator",
      "need": "Validate agent outputs before routing",
      "priority": "high",
      "source": "REQ-AGT-ORCH-001"
    }
  ],
  "requirements": [
    {
      "id": "REQ-NSE-001",
      "requirement": "The session context shall include a schema_version field following semantic versioning pattern X.Y.Z",
      "rationale": "Enables backward compatibility checking and migration support",
      "parent_need": "STK-001",
      "verification_method": "Test",
      "priority": "Must",
      "status": "Approved",
      "allocated_to": ["session_context.json"]
    },
    {
      "id": "REQ-NSE-002",
      "requirement": "Each agent output payload shall include a confidence score between 0.0 and 1.0",
      "rationale": "Enables downstream agents to assess reliability of received information",
      "parent_need": "STK-002",
      "verification_method": "Test",
      "priority": "Must",
      "status": "Approved",
      "allocated_to": ["all agent_output schemas"]
    },
    {
      "id": "REQ-NSE-003",
      "requirement": "The nse-* agent outputs shall include disclaimer_included field with value true",
      "rationale": "P-043 constitutional compliance requires disclaimer on all NASA SE outputs",
      "parent_need": "STK-001",
      "verification_method": "Inspection",
      "priority": "Must",
      "status": "Approved",
      "allocated_to": ["nse/*.json schemas"]
    }
  ],
  "traceability": {
    "coverage_status": "complete",
    "orphan_requirements": [],
    "unverified_requirements": []
  },
  "quality_assessment": {
    "complete": true,
    "consistent": true,
    "verifiable": true,
    "traceable": true,
    "unambiguous": true,
    "issues": []
  },
  "confidence": {
    "overall": 0.92,
    "reasoning": "Requirements derived from formal analysis with clear traceability",
    "breakdown": {
      "completeness": 0.90,
      "consistency": 0.95,
      "verifiability": 0.90
    }
  },
  "next_agent_hint": "nse-verification",
  "output_levels": {
    "l0_eli5": "We have defined 3 core requirements that ensure agents can reliably pass information to each other. Think of it like establishing standard shipping label formats - everyone knows what to expect.",
    "l1_technical": "Requirements REQ-NSE-001 through REQ-NSE-003 establish schema contracts for agent handoffs. All requirements are traceable to stakeholder needs and have assigned verification methods (Test or Inspection).",
    "l2_strategic": "These requirements form the foundation for the Jerry Framework's multi-agent orchestration layer. Schema versioning enables evolution without breaking existing workflows. The confidence score requirement addresses the P-022 transparency principle."
  },
  "artifacts": [
    {
      "path": "projects/PROJ-002/requirements/schema-requirements.md",
      "type": "requirement",
      "format": "markdown",
      "size_bytes": 8500
    }
  ],
  "disclaimer_included": true
}
```

---

## References

1. **JSON Schema Draft-07**: https://json-schema.org/draft-07/json-schema-release-notes.html
2. **NASA NPR 7123.1D**: Systems Engineering Processes and Requirements
3. **NASA-HDBK-1009A**: NASA Systems Engineering Work Products
4. **Jerry Constitution v1.0**: docs/governance/JERRY_CONSTITUTION.md
5. **NSE Agent Template v1.0**: skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md
6. **Session Context v1.0.0**: docs/schemas/session_context.json
7. **Agent Design Research**: projects/PROJ-002/ps-pipeline/phase-1-research/agent-design.md
8. **Agent Requirements**: projects/PROJ-002/nse-pipeline/phase-1-scope/agent-requirements.md

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-10 | ps-architect (ps-d-002) | Initial schema contracts design |

---

*Generated by ps-architect agent v2.0.0 for PROJ-002 NASA Systems Engineering*
