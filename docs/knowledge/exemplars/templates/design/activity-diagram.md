# {{TITLE}} - Activity Diagram

## Overview

{{OVERVIEW_DESCRIPTION}}

---

## Mermaid Activity/Flow Diagram

```mermaid
flowchart TD
    %% Start and End Points
    Start([{{START_LABEL}}]) --> {{FIRST_ACTION}}

    %% Actions
    {{FIRST_ACTION}}[{{ACTION_1_LABEL}}] --> {{DECISION_1}}

    %% Decision Point 1
    {{DECISION_1}}{{{DECISION_1_LABEL}}}
    {{DECISION_1}} -->|{{DECISION_1_YES}}| {{ACTION_2}}
    {{DECISION_1}} -->|{{DECISION_1_NO}}| {{ERROR_1}}

    %% Action Chain
    {{ACTION_2}}[{{ACTION_2_LABEL}}] --> {{ACTION_3}}
    {{ACTION_3}}[{{ACTION_3_LABEL}}] --> {{DECISION_2}}

    %% Decision Point 2 (Fork/Multiple Paths)
    {{DECISION_2}}{{{DECISION_2_LABEL}}}
    {{DECISION_2}} -->|{{DECISION_2_OPTION_1}}| {{PATH_1_ACTION}}
    {{DECISION_2}} -->|{{DECISION_2_OPTION_2}}| {{PATH_2_ACTION}}

    %% Path 1
    {{PATH_1_ACTION}}[{{PATH_1_ACTION_LABEL}}] --> {{PATH_1_RESULT}}
    {{PATH_1_RESULT}}[{{PATH_1_RESULT_LABEL}}] --> {{JOIN_POINT}}

    %% Path 2
    {{PATH_2_ACTION}}[{{PATH_2_ACTION_LABEL}}] --> {{PATH_2_RESULT}}
    {{PATH_2_RESULT}}[{{PATH_2_RESULT_LABEL}}] --> {{JOIN_POINT}}

    %% Join Point (Merge)
    {{JOIN_POINT}}[{{JOIN_POINT_LABEL}}] --> {{FINAL_DECISION}}

    %% Final Decision
    {{FINAL_DECISION}}{{{FINAL_DECISION_LABEL}}}
    {{FINAL_DECISION}} -->|{{FINAL_YES}}| Success
    {{FINAL_DECISION}} -->|{{FINAL_NO}}| {{ERROR_2}}

    %% Success End
    Success([{{SUCCESS_LABEL}}])

    %% Error Handling
    {{ERROR_1}}[{{ERROR_1_LABEL}}] --> ErrorEnd
    {{ERROR_2}}[{{ERROR_2_LABEL}}] --> ErrorEnd
    ErrorEnd([{{ERROR_END_LABEL}}])

    %% Notes (as subgraphs)
    subgraph {{SWIMLANE_1}} [{{SWIMLANE_1_LABEL}}]
        {{FIRST_ACTION}}
        {{ACTION_2}}
        {{DECISION_1}}
    end

    subgraph {{SWIMLANE_2}} [{{SWIMLANE_2_LABEL}}]
        {{ACTION_3}}
        {{PATH_1_ACTION}}
        {{PATH_2_ACTION}}
    end

    subgraph {{SWIMLANE_3}} [{{SWIMLANE_3_LABEL}}]
        {{PATH_1_RESULT}}
        {{PATH_2_RESULT}}
        {{JOIN_POINT}}
    end
```

---

## ASCII Activity Diagram (Terminal-Friendly)

```
[{{START_LABEL}}]
       │
       ▼
┌──────────────────┐
│ {{ACTION_1_LABEL}}│
└────┬────────┬────┘
     │        │
  {{DECISION_1_YES}}    {{DECISION_1_NO}}
     │        │
     ▼        ▼
┌─────────┐ [{{ERROR_1_LABEL}}]
│{{ACTION_2_LABEL}}│
└────┬────┘
     │
     ▼
┌──────────────────┐
│ {{ACTION_3_LABEL}}│
└────┬─────────────┘
     │
     ▼
     ◇ {{DECISION_2_LABEL}}
    ╱ ╲
   ╱   ╲
  ▼     ▼
┌────────────┐    ┌────────────┐
│{{PATH_1}}  │    │{{PATH_2}}  │
└─────┬──────┘    └──────┬─────┘
      │                  │
      ▼                  ▼
┌────────────┐    ┌────────────┐
│{{RESULT_1}}│    │{{RESULT_2}}│
└─────┬──────┘    └──────┬─────┘
      │                  │
      └────────┬─────────┘
               │
               ▼
┌──────────────────┐
│ {{JOIN_POINT_LABEL}}│
└────┬─────────────┘
     │
     ▼
     ◇ {{FINAL_DECISION_LABEL}}
    ╱ ╲
   ╱   ╲
  ▼     ▼
[✅ {{SUCCESS_LABEL}}]   [❌ {{ERROR_END_LABEL}}]
```

---

## Actions

| Action ID       | Name                    | Description       | Input              | Output              | Exception              |
| --------------- | ----------------------- | ----------------- | ------------------ | ------------------- | ---------------------- |
| {{ACTION_1_ID}} | {{ACTION_1_LABEL}}      | {{ACTION_1_DESC}} | {{ACTION_1_INPUT}} | {{ACTION_1_OUTPUT}} | {{ACTION_1_EXCEPTION}} |
| {{ACTION_2_ID}} | {{ACTION_2_LABEL}}      | {{ACTION_2_DESC}} | {{ACTION_2_INPUT}} | {{ACTION_2_OUTPUT}} | {{ACTION_2_EXCEPTION}} |
| {{ACTION_3_ID}} | {{ACTION_3_LABEL}}      | {{ACTION_3_DESC}} | {{ACTION_3_INPUT}} | {{ACTION_3_OUTPUT}} | {{ACTION_3_EXCEPTION}} |
| {{PATH_1_ID}}   | {{PATH_1_ACTION_LABEL}} | {{PATH_1_DESC}}   | {{PATH_1_INPUT}}   | {{PATH_1_OUTPUT}}   | {{PATH_1_EXCEPTION}}   |
| {{PATH_2_ID}}   | {{PATH_2_ACTION_LABEL}} | {{PATH_2_DESC}}   | {{PATH_2_INPUT}}   | {{PATH_2_OUTPUT}}   | {{PATH_2_EXCEPTION}}   |

---

## Decision Points

| Decision           | Condition                      | True Path           | False Path           | Business Rule       |
| ------------------ | ------------------------------ | ------------------- | -------------------- | ------------------- |
| {{DECISION_1}}     | `{{DECISION_1_CONDITION}}`     | {{DECISION_1_TRUE}} | {{DECISION_1_FALSE}} | {{DECISION_1_RULE}} |
| {{DECISION_2}}     | `{{DECISION_2_CONDITION}}`     | {{DECISION_2_TRUE}} | {{DECISION_2_FALSE}} | {{DECISION_2_RULE}} |
| {{FINAL_DECISION}} | `{{FINAL_DECISION_CONDITION}}` | {{FINAL_TRUE}}      | {{FINAL_FALSE}}      | {{FINAL_RULE}}      |

---

## Swimlanes / Responsibilities

| Swimlane       | Component                | Responsibility                |
| -------------- | ------------------------ | ----------------------------- |
| {{SWIMLANE_1}} | {{SWIMLANE_1_COMPONENT}} | {{SWIMLANE_1_RESPONSIBILITY}} |
| {{SWIMLANE_2}} | {{SWIMLANE_2_COMPONENT}} | {{SWIMLANE_2_RESPONSIBILITY}} |
| {{SWIMLANE_3}} | {{SWIMLANE_3_COMPONENT}} | {{SWIMLANE_3_RESPONSIBILITY}} |

---

## Error Handling Flow

```mermaid
flowchart TD
    UseCase[{{USE_CASE_NAME}}] --> Try{Try}

    Try --> Domain[{{DOMAIN_LAYER}}]
    Domain --> DomainEx{Domain<br/>Exception?}

    DomainEx -->|{{DOMAIN_ERROR_1}}| Handle1[{{DOMAIN_ERROR_1_HANDLER}}]
    DomainEx -->|{{DOMAIN_ERROR_2}}| Handle2[{{DOMAIN_ERROR_2_HANDLER}}]
    DomainEx -->|No error| Persist[{{PERSISTENCE_LAYER}}]

    Persist --> PersistEx{Persistence<br/>Exception?}

    PersistEx -->|{{PERSIST_ERROR_1}}| Handle3[{{PERSIST_ERROR_1_HANDLER}}]
    PersistEx -->|{{PERSIST_ERROR_2}}| Handle4[{{PERSIST_ERROR_2_HANDLER}}]
    PersistEx -->|No error| Success([Success])

    Handle1 --> End([End])
    Handle2 --> End
    Handle3 --> End
    Handle4 --> End
```

---

## Pre-conditions

| ID     | Condition          | Validation                    |
| ------ | ------------------ | ----------------------------- |
| PRE-01 | {{PRECONDITION_1}} | {{PRECONDITION_1_VALIDATION}} |
| PRE-02 | {{PRECONDITION_2}} | {{PRECONDITION_2_VALIDATION}} |
| PRE-03 | {{PRECONDITION_3}} | {{PRECONDITION_3_VALIDATION}} |

---

## Post-conditions

| ID      | Condition           | Verification                     |
| ------- | ------------------- | -------------------------------- |
| POST-01 | {{POSTCONDITION_1}} | {{POSTCONDITION_1_VERIFICATION}} |
| POST-02 | {{POSTCONDITION_2}} | {{POSTCONDITION_2_VERIFICATION}} |
| POST-03 | {{POSTCONDITION_3}} | {{POSTCONDITION_3_VERIFICATION}} |

---

## Performance Targets

| Operation       | Baseline           | Expected           | Max Allowed   | Notes           |
| --------------- | ------------------ | ------------------ | ------------- | --------------- |
| {{OPERATION_1}} | {{OP_1_BASELINE}}  | {{OP_1_EXPECTED}}  | {{OP_1_MAX}}  | {{OP_1_NOTES}}  |
| {{OPERATION_2}} | {{OP_2_BASELINE}}  | {{OP_2_EXPECTED}}  | {{OP_2_MAX}}  | {{OP_2_NOTES}}  |
| Full workflow   | {{TOTAL_BASELINE}} | {{TOTAL_EXPECTED}} | {{TOTAL_MAX}} | {{TOTAL_NOTES}} |

---

## Use Case Catalog

| Use Case       | Domain Methods         | Persistence            | Memory                |
| -------------- | ---------------------- | ---------------------- | --------------------- |
| {{USE_CASE_1}} | {{USE_CASE_1_METHODS}} | {{USE_CASE_1_PERSIST}} | {{USE_CASE_1_MEMORY}} |
| {{USE_CASE_2}} | {{USE_CASE_2_METHODS}} | {{USE_CASE_2_PERSIST}} | {{USE_CASE_2_MEMORY}} |
| {{USE_CASE_3}} | {{USE_CASE_3_METHODS}} | {{USE_CASE_3_PERSIST}} | {{USE_CASE_3_MEMORY}} |

---

## Related Diagrams

- [Sequence Diagram](./{{RELATED_SEQUENCE_DIAGRAM}})
- [State Machine](./{{RELATED_STATE_MACHINE}})
- [Class Diagram](./{{RELATED_CLASS_DIAGRAM}})

---

## Implementation Location

{{IMPLEMENTATION_LOCATION}}

---

## Template Metadata

> **Template Version:** 1.0.0
> **Based On:** Phase-38 use-case-flows.md
> **Fidelity Level:** Production
> **Max Nodes:** 20 (as per diagramming standards)
