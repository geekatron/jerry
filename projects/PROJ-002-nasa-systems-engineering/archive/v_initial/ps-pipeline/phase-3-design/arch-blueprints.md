# Architecture Blueprints: Parallel Execution and State Checkpointing

> **Document ID:** ps-d-003
> **Phase:** 3 - Design (ps-* Pipeline)
> **Project:** PROJ-002-nasa-systems-engineering
> **Date:** 2026-01-10
> **Agent:** ps-architect
> **PS ID:** SAO-CROSSPOLL
> **Entry ID:** ps-d-003

---

## L0: Executive Summary

This document defines architecture blueprints for three core infrastructure capabilities:

1. **Parallel Execution** - Fan-out/fan-in patterns with barrier synchronization
2. **State Checkpointing** - Persistent state snapshots with restoration capability
3. **Generator-Critic Loops** - Quality assurance through iterative refinement

All designs adhere to Jerry Framework constraints:
- **P-003**: Single-level agent nesting (orchestrator to worker only)
- **P-002**: File-based persistence for all state
- **P-022**: Transparency in all agent actions

Key architectural decisions:
- **Controlled concurrency** (max 5 parallel agents) per trade study TS-4
- **Full context isolation** between parallel agents (M-001 mitigation)
- **Circuit breaker pattern** for generator-critic loops (max 3 iterations, M-002)
- **Write-ahead logging** for checkpoint atomicity (M-004)

---

## L1: Parallel Execution Architecture

### 1.1 Overview

Parallel execution enables fan-out of independent tasks to multiple agents with subsequent fan-in aggregation. This addresses GAP-002 from industry practices research and implements recommendation TS-4 from trade study.

### 1.2 Component Architecture

```
                         PARALLEL EXECUTION ARCHITECTURE
    +-----------------------------------------------------------------+
    |                                                                 |
    |  +-------------------+                                          |
    |  |   ORCHESTRATOR    |  (Opus 4.5 - Coordinator Role)           |
    |  |  - Task planning  |                                          |
    |  |  - Fan-out logic  |                                          |
    |  |  - Aggregation    |                                          |
    |  +--------+----------+                                          |
    |           |                                                     |
    |           | spawn (respects P-003)                              |
    |           v                                                     |
    |  +------------------+                                           |
    |  |  PARALLEL ROUTER |                                           |
    |  |  - Concurrency   |                                           |
    |  |    control       |                                           |
    |  |  - Isolation     |                                           |
    |  |    enforcement   |                                           |
    |  +--------+---------+                                           |
    |           |                                                     |
    |       FAN-OUT (max 5)                                           |
    |           |                                                     |
    |  +--------+--------+--------+--------+--------+                 |
    |  |        |        |        |        |        |                 |
    |  v        v        v        v        v        v                 |
    | [W1]     [W2]     [W3]     [W4]     [W5]    [Queue]             |
    |  |        |        |        |        |                          |
    |  | (isolated context per worker)     |                          |
    |  |        |        |        |        |                          |
    |  +--------+--------+--------+--------+                          |
    |           |                                                     |
    |           v                                                     |
    |  +------------------+                                           |
    |  |  BARRIER SYNC    |                                           |
    |  |  - Wait for all  |                                           |
    |  |  - Timeout: 5min |                                           |
    |  |  - Partial mode  |                                           |
    |  +--------+---------+                                           |
    |           |                                                     |
    |           | FAN-IN                                              |
    |           v                                                     |
    |  +------------------+                                           |
    |  |   AGGREGATOR     |                                           |
    |  |  - Merge outputs |                                           |
    |  |  - Conflict res  |                                           |
    |  |  - Quality check |                                           |
    |  +------------------+                                           |
    |                                                                 |
    +-----------------------------------------------------------------+
```

### 1.3 Isolation Model

Each parallel worker receives an isolated execution context to prevent race conditions (R-IMP-001 mitigation):

```
                         CONTEXT ISOLATION MODEL
    +----------------------------------------------------------------+
    |                                                                |
    |  SHARED (Read-Only)              ISOLATED (Read-Write)         |
    |  +-------------------+           +------------------------+    |
    |  | - Input artifacts |           | Worker 1:              |    |
    |  | - Configuration   |  COPY-ON  | - /workflow/w1/        |    |
    |  | - Schema defs     |  ---------> - session_context.json |    |
    |  | - Skill prompts   |   SPAWN   | - output/              |    |
    |  +-------------------+           | - scratch/             |    |
    |                                  +------------------------+    |
    |                                  | Worker 2:              |    |
    |                                  | - /workflow/w2/        |    |
    |                                  | - session_context.json |    |
    |                                  | - output/              |    |
    |                                  | - scratch/             |    |
    |                                  +------------------------+    |
    |                                  | ...                    |    |
    |                                  +------------------------+    |
    |                                                                |
    |  ENFORCEMENT:                                                  |
    |  - No shared file handles                                      |
    |  - Namespace prefix: {workflow_id}/{agent_id}/                 |
    |  - Read-only access to shared resources                        |
    |                                                                |
    +----------------------------------------------------------------+
```

### 1.4 Fan-Out Strategy

```yaml
# parallel_config.yaml
fan_out:
  strategy: "topic_based"  # Alternatives: round_robin, capability_match
  max_concurrent: 5        # Per TS-4 recommendation
  queue_overflow: "wait"   # Alternatives: reject, priority_evict

  topic_routing:
    research:
      agents: ["ps-researcher-1", "ps-researcher-2"]
      affinity: "domain"   # Same domain topics to same agent
    analysis:
      agents: ["ps-analyst-1", "ps-analyst-2", "ps-analyst-3"]
      affinity: "none"     # Load balanced
```

### 1.5 Barrier Synchronization

```
                         BARRIER SYNC STATES
    +----------------------------------------------------------------+
    |                                                                |
    |    WAITING           PARTIAL            COMPLETE               |
    |   +-------+         +-------+          +-------+               |
    |   |       |         |       |          |       |               |
    |   | W: 5  | ------> | W: 2  | -------> | W: 0  |               |
    |   | C: 0  |   +3    | C: 3  |   +2     | C: 5  |               |
    |   | F: 0  |         | F: 0  |          | F: 0  |               |
    |   |       |         |       |          |       |               |
    |   +-------+         +-------+          +-------+               |
    |       |                 |                  |                   |
    |       |           TIMEOUT (5min)           |                   |
    |       |                 |                  |                   |
    |       |                 v                  |                   |
    |       |            +-------+               |                   |
    |       |            |       |               |                   |
    |       +----------->| PART- |<--------------+                   |
    |                    | IAL   |                                   |
    |                    | MODE  |                                   |
    |                    |       |                                   |
    |                    +-------+                                   |
    |                                                                |
    |    W = Waiting workers                                         |
    |    C = Completed workers                                       |
    |    F = Failed workers                                          |
    |                                                                |
    |    Partial Mode: Proceeds with completed results if            |
    |                  >= 50% workers completed                      |
    |                                                                |
    +----------------------------------------------------------------+
```

### 1.6 Parallel Execution Configuration Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ParallelExecutionConfig",
  "type": "object",
  "required": ["workflow_id", "fan_out", "barrier", "fan_in"],
  "properties": {
    "workflow_id": {
      "type": "string",
      "format": "uuid"
    },
    "fan_out": {
      "type": "object",
      "required": ["strategy", "tasks"],
      "properties": {
        "strategy": {
          "enum": ["topic_based", "round_robin", "capability_match"]
        },
        "max_concurrent": {
          "type": "integer",
          "minimum": 1,
          "maximum": 5,
          "default": 5
        },
        "tasks": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["task_id", "agent", "input_artifacts"],
            "properties": {
              "task_id": { "type": "string" },
              "agent": { "type": "string" },
              "input_artifacts": {
                "type": "array",
                "items": { "type": "string" }
              },
              "topic": { "type": "string" }
            }
          }
        }
      }
    },
    "barrier": {
      "type": "object",
      "properties": {
        "timeout_ms": {
          "type": "integer",
          "default": 300000
        },
        "partial_mode": {
          "type": "boolean",
          "default": true
        },
        "min_completion_ratio": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.5
        }
      }
    },
    "fan_in": {
      "type": "object",
      "required": ["aggregation_strategy"],
      "properties": {
        "aggregation_strategy": {
          "enum": ["merge", "select_best", "consensus", "custom"]
        },
        "conflict_resolution": {
          "enum": ["first_wins", "last_wins", "orchestrator_decides"]
        }
      }
    }
  }
}
```

---

## L1: State Checkpointing Architecture

### 2.1 Overview

State checkpointing provides persistent snapshots of workflow state enabling:
- **Recovery** from failures mid-workflow
- **Debugging** via state inspection
- **Time-travel** to replay from any checkpoint

This addresses GAP-001 from industry practices and implements recommendation TS-3.

### 2.2 Checkpoint Architecture

```
                         CHECKPOINTING ARCHITECTURE
    +----------------------------------------------------------------+
    |                                                                |
    |  WORKFLOW EXECUTION                                            |
    |  ==================                                            |
    |                                                                |
    |  [Start] --> [Agent 1] --> [Agent 2] --> [Agent 3] --> [End]   |
    |     |            |             |             |            |    |
    |     v            v             v             v            v    |
    |   CP-0         CP-1          CP-2          CP-3         CP-4   |
    |     |            |             |             |            |    |
    |     +------------+-------------+-------------+------------+    |
    |                            |                                   |
    |                            v                                   |
    |                  +------------------+                          |
    |                  | CHECKPOINT STORE |                          |
    |                  |                  |                          |
    |                  | - Write-ahead    |                          |
    |                  |   log (WAL)      |                          |
    |                  | - Atomic writes  |                          |
    |                  | - Compression    |                          |
    |                  |                  |                          |
    |                  +--------+---------+                          |
    |                           |                                    |
    |                           v                                    |
    |  +---------------------------------------------------+         |
    |  |              CHECKPOINT STORAGE                   |         |
    |  |                                                   |         |
    |  | checkpoints/                                      |         |
    |  |   {workflow_id}/                                  |         |
    |  |     CP-0-2026-01-10T14-00-00.json.lz4            |         |
    |  |     CP-1-2026-01-10T14-05-32.json.lz4            |         |
    |  |     CP-2-2026-01-10T14-12-18.json.lz4            |         |
    |  |     manifest.json                                 |         |
    |  |                                                   |         |
    |  +---------------------------------------------------+         |
    |                                                                |
    +----------------------------------------------------------------+
```

### 2.3 Checkpoint Data Model

```
                         CHECKPOINT STRUCTURE
    +----------------------------------------------------------------+
    |                                                                |
    |  +-------------------------+                                   |
    |  |     CHECKPOINT          |                                   |
    |  +-------------------------+                                   |
    |  | checkpoint_id: string   |                                   |
    |  | workflow_id: string     |                                   |
    |  | sequence_num: int       |                                   |
    |  | created_at: timestamp   |                                   |
    |  | agent_id: string        |                                   |
    |  | phase: string           |                                   |
    |  +------------+------------+                                   |
    |               |                                                |
    |     +---------+---------+                                      |
    |     |                   |                                      |
    |     v                   v                                      |
    |  +----------+    +-------------+                               |
    |  | STATE    |    | ARTIFACTS   |                               |
    |  +----------+    +-------------+                               |
    |  | session_ |    | path: str   |                               |
    |  | context  |    | hash: sha256|                               |
    |  | outputs  |    | size: int   |                               |
    |  | errors   |    | inline: bool|                               |
    |  +----------+    +-------------+                               |
    |                                                                |
    +----------------------------------------------------------------+
```

### 2.4 Write-Ahead Logging (WAL) Flow

Per M-004 mitigation for R-IMP-002 (non-atomic persistence):

```
                         WRITE-AHEAD LOG FLOW
    +----------------------------------------------------------------+
    |                                                                |
    |  1. PREPARE                                                    |
    |     +------------------+                                       |
    |     | Agent completes  |                                       |
    |     | task, outputs    |                                       |
    |     | ready            |                                       |
    |     +--------+---------+                                       |
    |              |                                                 |
    |              v                                                 |
    |  2. WAL WRITE                                                  |
    |     +------------------+                                       |
    |     | Write intent to  |  <-- Crash here = can replay          |
    |     | WAL file first   |                                       |
    |     +--------+---------+                                       |
    |              |                                                 |
    |              v                                                 |
    |  3. CHECKPOINT WRITE                                           |
    |     +------------------+                                       |
    |     | Write checkpoint |  <-- Crash here = WAL replay          |
    |     | data atomically  |                                       |
    |     +--------+---------+                                       |
    |              |                                                 |
    |              v                                                 |
    |  4. WAL COMMIT                                                 |
    |     +------------------+                                       |
    |     | Mark WAL entry   |                                       |
    |     | as committed     |                                       |
    |     +--------+---------+                                       |
    |              |                                                 |
    |              v                                                 |
    |  5. WAL CLEANUP                                                |
    |     +------------------+                                       |
    |     | Remove committed |  (periodic, not immediate)            |
    |     | WAL entries      |                                       |
    |     +------------------+                                       |
    |                                                                |
    +----------------------------------------------------------------+
```

### 2.5 Checkpoint Lifecycle

```
                         CHECKPOINT LIFECYCLE
    +----------------------------------------------------------------+
    |                                                                |
    |    CREATE          ACTIVE          ARCHIVED         DELETED    |
    |   +------+        +------+        +--------+       +-------+   |
    |   |      |  (age  |      |  (age  |        | (age  |       |   |
    |   | NEW  | < 1h)  | WARM | < 24h) | COLD   | >24h) | GONE  |   |
    |   |      | -----> |      | -----> |        | ----> |       |   |
    |   +------+        +------+        +--------+       +-------+   |
    |       |               |                |                       |
    |       |               |                |                       |
    |       |           RESTORE          RESTORE                     |
    |       |          (instant)       (decompress)                  |
    |       |               |                |                       |
    |       v               v                v                       |
    |  +---------------------------------------------------+         |
    |  |              RESTORED WORKFLOW                    |         |
    |  |                                                   |         |
    |  | - Context rebuilt from checkpoint                 |         |
    |  | - Artifacts restored to original paths            |         |
    |  | - Execution resumes from checkpoint agent         |         |
    |  |                                                   |         |
    |  +---------------------------------------------------+         |
    |                                                                |
    |  RETENTION POLICY:                                             |
    |  - max_checkpoints: 100 per workflow                           |
    |  - max_age_hours: 24 (then archived)                           |
    |  - archive_retention_days: 7                                   |
    |  - compression: lz4 after 1 hour                               |
    |                                                                |
    +----------------------------------------------------------------+
```

### 2.6 Checkpoint Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Checkpoint",
  "type": "object",
  "required": ["checkpoint_id", "workflow_id", "sequence_num", "created_at", "state"],
  "properties": {
    "checkpoint_id": {
      "type": "string",
      "format": "uuid"
    },
    "workflow_id": {
      "type": "string",
      "format": "uuid"
    },
    "sequence_num": {
      "type": "integer",
      "minimum": 0
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "agent_id": {
      "type": "string",
      "description": "Agent that triggered this checkpoint"
    },
    "phase": {
      "type": "string",
      "description": "Workflow phase (e.g., research, analysis, design)"
    },
    "state": {
      "type": "object",
      "required": ["session_context"],
      "properties": {
        "session_context": {
          "$ref": "#/definitions/SessionContext"
        },
        "outputs": {
          "type": "object",
          "additionalProperties": true
        },
        "errors": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "agent": { "type": "string" },
              "error": { "type": "string" },
              "timestamp": { "type": "string", "format": "date-time" }
            }
          }
        }
      }
    },
    "artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path", "hash"],
        "properties": {
          "path": { "type": "string" },
          "hash": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" },
          "size_bytes": { "type": "integer" },
          "inline": {
            "type": "boolean",
            "description": "If true, content is embedded in checkpoint"
          },
          "content": {
            "type": "string",
            "description": "Base64-encoded content if inline=true"
          }
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "compression": { "enum": ["none", "lz4", "zstd"] },
        "serialization": { "enum": ["json", "msgpack"] },
        "version": { "type": "string", "pattern": "^\\d+\\.\\d+$" }
      }
    }
  },
  "definitions": {
    "SessionContext": {
      "type": "object",
      "required": ["session_id", "source_agent", "target_agent", "payload"],
      "properties": {
        "session_id": { "type": "string", "format": "uuid" },
        "source_agent": { "type": "string" },
        "target_agent": { "type": "string" },
        "cognitive_mode": { "enum": ["divergent", "convergent", "mixed"] },
        "payload": {
          "type": "object",
          "properties": {
            "key_findings": { "type": "array", "items": { "type": "string" } },
            "open_questions": { "type": "array" },
            "blockers": { "type": "array" },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "artifact_refs": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

---

## L1: Generator-Critic Loop Architecture

### 3.1 Overview

Generator-Critic loops implement iterative refinement through paired agents. Per industry research, this pattern provides 15-25% quality improvement. Implements TS-5 recommendation with M-002 mitigation (circuit breaker).

### 3.2 Loop Architecture

```
                         GENERATOR-CRITIC LOOP
    +----------------------------------------------------------------+
    |                                                                |
    |  +-------------------+                                         |
    |  |   ORCHESTRATOR    |                                         |
    |  |  - Loop control   |                                         |
    |  |  - Iteration cap  |                                         |
    |  |  - Quality gate   |                                         |
    |  +--------+----------+                                         |
    |           |                                                    |
    |           v                                                    |
    |  +--------------------------------------------+                |
    |  |           ITERATION LOOP                   |                |
    |  |           (max: 3 iterations)              |                |
    |  |                                            |                |
    |  |  +----------+          +----------+        |                |
    |  |  |GENERATOR |  output  |  CRITIC  |        |                |
    |  |  |          | -------> |          |        |                |
    |  |  | - Draft  |          | - Review |        |                |
    |  |  | - Create |          | - Score  |        |                |
    |  |  | - Refine |  feedback| - Issues |        |                |
    |  |  |          | <------- |          |        |                |
    |  |  +----------+          +----------+        |                |
    |  |       |                     |              |                |
    |  |       |    QUALITY CHECK    |              |                |
    |  |       |         |           |              |                |
    |  |       |         v           |              |                |
    |  |       |    +--------+       |              |                |
    |  |       |    | score  |       |              |                |
    |  |       |    | >= 0.8 |       |              |                |
    |  |       |    +---+----+       |              |                |
    |  |       |        |            |              |                |
    |  |       |   YES  |  NO        |              |                |
    |  |       |        |            |              |                |
    |  +-------|--------+------------|------+       |                |
    |          |                     |      |       |                |
    |          v                     v      |       |                |
    |    [APPROVED]            [ITERATE]----+       |                |
    |          |                                    |                |
    |          v                                    |                |
    |  +------------------+                         |                |
    |  |  FINAL OUTPUT    |                         |                |
    |  |  - Best version  |                         |                |
    |  |  - Critique log  |                         |                |
    |  |  - Score history |                         |                |
    |  +------------------+                         |                |
    |                                               |                |
    +-----------------------------------------------+----------------+
```

### 3.3 Circuit Breaker Pattern (M-002)

Per R-IMP-003 mitigation (infinite loop prevention):

```
                         CIRCUIT BREAKER
    +----------------------------------------------------------------+
    |                                                                |
    |  ITERATION CONTROL                                             |
    |  =================                                             |
    |                                                                |
    |  Iteration 1:                                                  |
    |  +-------+     +-------+     +----------------+                |
    |  | GEN   | --> | CRIT  | --> | score < 0.8   |                |
    |  +-------+     +-------+     | improvement?  |                |
    |                              +-------+--------+                |
    |                                      |                         |
    |                            YES       |  NO                     |
    |                              |       |                         |
    |                              v       v                         |
    |                          Continue   STOP                       |
    |                              |    (no improvement)             |
    |                              |                                 |
    |  Iteration 2:                |                                 |
    |  +-------+     +-------+     +----------------+                |
    |  | GEN   | --> | CRIT  | --> | score < 0.8   |                |
    |  +-------+     +-------+     | improvement?  |                |
    |                              +-------+--------+                |
    |                                      |                         |
    |                            YES       |  NO                     |
    |                              |       |                         |
    |                              v       v                         |
    |                          Continue   STOP                       |
    |                              |                                 |
    |  Iteration 3:                |                                 |
    |  +-------+     +-------+     +----------------+                |
    |  | GEN   | --> | CRIT  | --> | FINAL         |                |
    |  +-------+     +-------+     | (max reached) |                |
    |                              +----------------+                |
    |                                                                |
    |  TERMINATION CONDITIONS:                                       |
    |  1. score >= 0.8 (quality threshold met)                       |
    |  2. iteration >= 3 (max iterations reached)                    |
    |  3. improvement < 0.05 (diminishing returns)                   |
    |                                                                |
    +----------------------------------------------------------------+
```

### 3.4 Generator-Critic State Machine

```
                         STATE MACHINE
    +----------------------------------------------------------------+
    |                                                                |
    |    INIT        GENERATING      CRITIQUING      COMPLETE        |
    |   +----+        +------+        +------+        +------+       |
    |   |    | start  |      | output |      | score  |      |       |
    |   | S0 | -----> | GEN  | -----> | CRIT | >=0.8  | DONE |       |
    |   |    |        |      |        |      | -----> |      |       |
    |   +----+        +--+---+        +--+---+        +------+       |
    |                    |               |                           |
    |                    |               | score < 0.8               |
    |                    |               | AND iter < 3              |
    |                    |               | AND improvement >= 0.05   |
    |                    |               |                           |
    |                    +<--------------+                           |
    |                    |  (refine with feedback)                   |
    |                    |                                           |
    |                    |               +-------+                   |
    |                    |               |       |                   |
    |                    +-------------->| ABORT |                   |
    |                    (max iter OR    |       |                   |
    |                     no improvement)+-------+                   |
    |                                        |                       |
    |                                        v                       |
    |                                   [Best Output]                |
    |                                                                |
    +----------------------------------------------------------------+
```

### 3.5 Loop Configuration Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GeneratorCriticConfig",
  "type": "object",
  "required": ["generator", "critic", "loop_control"],
  "properties": {
    "generator": {
      "type": "object",
      "required": ["agent_id"],
      "properties": {
        "agent_id": { "type": "string" },
        "cognitive_mode": { "const": "divergent" },
        "temperature": { "type": "number", "default": 0.7 }
      }
    },
    "critic": {
      "type": "object",
      "required": ["agent_id"],
      "properties": {
        "agent_id": { "type": "string" },
        "cognitive_mode": { "const": "convergent" },
        "temperature": { "type": "number", "default": 0.3 },
        "scoring": {
          "type": "object",
          "properties": {
            "rubric": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "criterion": { "type": "string" },
                  "weight": { "type": "number" }
                }
              }
            }
          }
        }
      }
    },
    "loop_control": {
      "type": "object",
      "properties": {
        "max_iterations": {
          "type": "integer",
          "minimum": 1,
          "maximum": 5,
          "default": 3
        },
        "quality_threshold": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.8
        },
        "improvement_threshold": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "default": 0.05,
          "description": "Minimum score improvement to continue"
        },
        "timeout_ms": {
          "type": "integer",
          "default": 600000,
          "description": "Per-iteration timeout"
        }
      }
    },
    "output": {
      "type": "object",
      "properties": {
        "keep_history": {
          "type": "boolean",
          "default": true,
          "description": "Preserve all iterations for debugging"
        },
        "output_best": {
          "type": "boolean",
          "default": true,
          "description": "Output highest-scoring version"
        }
      }
    }
  }
}
```

---

## L1: Integration with Jerry Framework

### 4.1 Jerry Constitution Alignment

| Blueprint | P-002 (Persistence) | P-003 (Nesting) | P-022 (Transparency) |
|-----------|---------------------|-----------------|---------------------|
| Parallel Execution | All outputs to isolated directories | Orchestrator -> Workers only | Fan-out/fan-in logged |
| Checkpointing | WAL + compressed storage | Checkpoints at agent boundaries | Full state captured |
| Generator-Critic | Iteration history preserved | Orchestrator manages loop | Critique log exposed |

### 4.2 Skill Integration

```
                         SKILL INTEGRATION
    +----------------------------------------------------------------+
    |                                                                |
    |  skills/orchestration/                                         |
    |  =====================                                         |
    |                                                                |
    |  +------------------------+                                    |
    |  | ORCHESTRATION_PLAN.md  |                                    |
    |  |                        |                                    |
    |  | parallel_execution:    |                                    |
    |  |   enabled: true        |                                    |
    |  |   config: <ref>        |                                    |
    |  |                        |                                    |
    |  | checkpointing:         |                                    |
    |  |   enabled: true        |                                    |
    |  |   retention: 24h       |                                    |
    |  |                        |                                    |
    |  | generator_critic:      |                                    |
    |  |   enabled: true        |                                    |
    |  |   max_iterations: 3    |                                    |
    |  +------------------------+                                    |
    |              |                                                 |
    |              v                                                 |
    |  +------------------------+                                    |
    |  | ORCHESTRATION.yaml     |  (Machine-readable SSOT)           |
    |  |                        |                                    |
    |  | workflows:             |                                    |
    |  |   - id: sao-crosspoll  |                                    |
    |  |     parallel_tasks:    |                                    |
    |  |       - ps-r-001       |                                    |
    |  |       - nse-req-001    |                                    |
    |  |     checkpoints:       |                                    |
    |  |       - barrier-1      |                                    |
    |  |       - barrier-2      |                                    |
    |  +------------------------+                                    |
    |                                                                |
    +----------------------------------------------------------------+
```

### 4.3 Agent Template Extensions

Per TS-1 (Superset Schema), add parallel execution and quality loop fields:

```yaml
# UNIFIED_AGENT_TEMPLATE v1.1 - Extended for Infrastructure
identity:
  role: string
  expertise: array
  cognitive_mode: enum
  model: enum
persona:
  tone: string
  style: string
  formality: enum
capabilities:
  allowed_tools: array
  forbidden_actions: array
state:
  output_key: string
  schema: object

# NEW: Parallel execution support
parallel:
  supports_isolation: boolean    # Can run in isolated context
  output_namespace: string       # Prefix for output files
  aggregation_role: enum         # none | producer | aggregator

# NEW: Generator-Critic support
quality_loop:
  role: enum                     # generator | critic | none
  scoring_rubric: array          # For critics only
  accepts_feedback: boolean      # For generators only

# NEW: Checkpointing support
checkpoint:
  triggers: array                # ["on_complete", "on_error"]
  include_artifacts: boolean
  max_size_kb: integer
```

---

## L2: Implementation Considerations

### 5.1 Implementation Priority

Based on trade study TS-4 and risk assessment:

```
PHASE 1: State Foundation (Weeks 1-2)
=========================================
1. Implement session_context JSON Schema (R-TECH-001 mitigation)
2. Add schema validation at agent boundaries
3. Deploy WAL infrastructure for atomic writes

PHASE 2: Checkpointing (Weeks 3-4)
===================================
4. Implement checkpoint create/restore
5. Add retention policy and cleanup daemon
6. Integrate with orchestration skill

PHASE 3: Parallel Execution (Weeks 5-6)
========================================
7. Implement context isolation (copy-on-spawn)
8. Add parallel router with concurrency control
9. Implement barrier synchronization

PHASE 4: Generator-Critic (Weeks 7-8)
======================================
10. Implement circuit breaker pattern
11. Add scoring infrastructure
12. Create ps-critic and nse-qa agents
```

### 5.2 Constraints and Limitations

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| P-003 single nesting | Cannot have parallel workers spawn sub-workers | Orchestrator handles all fan-out |
| 5 agent concurrency limit | Large fan-outs queued | Priority-based queuing |
| JSON-only state | Binary artifacts handled separately | Hash references in checkpoint |
| File-based persistence | I/O bottleneck at scale | Namespace isolation, async I/O |

### 5.3 Performance Targets

| Operation | Baseline | Target | Max Allowed |
|-----------|----------|--------|-------------|
| Checkpoint create | N/A | < 100ms | 500ms |
| Checkpoint restore | N/A | < 500ms | 2000ms |
| Fan-out (5 agents) | Sequential | < 1.2x sequential | 2x sequential |
| Barrier wait | N/A | < 10ms | 100ms |
| Critic scoring | N/A | < 5s | 30s |

### 5.4 Testing Strategy

| Test Type | Focus Area | Validation |
|-----------|------------|------------|
| Unit | Schema validation | All schemas valid |
| Unit | WAL atomicity | Crash recovery works |
| Integration | Context isolation | No cross-contamination |
| Integration | Barrier sync | Timeout handling |
| E2E | Full workflow | Checkpoint + restore |
| Chaos | Failure injection | Graceful degradation |

---

## Cross-Pollination Metadata

### Source Artifacts

| Artifact | Path | Key Inputs |
|----------|------|------------|
| Trade Study | ps-pipeline/phase-2-analysis/trade-study.md | TS-3, TS-4, TS-5 recommendations |
| Industry Practices | ps-pipeline/phase-1-research/industry-practices.md | LangGraph, ADK patterns |
| Risk Findings | cross-pollination/barrier-2/nse-to-ps/risk-findings.md | Mitigations M-001, M-002, M-004 |

### Target Pipelines

| Pipeline | Artifact Type | Input |
|----------|--------------|-------|
| nse-architecture | Architecture Spec | Parallel execution design |
| nse-implementation | Implementation Guide | Schema definitions |
| ps-synthesis | Synthesis Input | Integration patterns |

### Handoff Checklist

- [x] L0/L1/L2 sections complete
- [x] ASCII diagrams for all components
- [x] JSON Schemas defined
- [x] Integration with Jerry framework documented
- [x] Implementation priority defined
- [x] Performance targets specified
- [ ] nse-architecture acknowledges blueprints
- [ ] ps-synthesis integrates designs

---

*Architecture Blueprint: ps-d-003*
*Generated by: ps-architect (Phase 3 Design)*
*Date: 2026-01-10*
*NPR 7123.1D TA-5 (Design Definition) Aligned*
