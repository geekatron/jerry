# Functional Architecture Document Template

> Runtime template for nse-architecture agent. Load via Read tool when generating functional architecture output.

```markdown
# Functional Architecture: [System Name]

> **Document ID:** FAD-[PROJECT]-[NNN]
> **Version:** [X.Y]
> **Date:** [YYYY-MM-DD]
> **Status:** [Draft/Baseline]

---

## 1. System Context

### 1.1 System Overview
[High-level description of the system and its purpose]

### 1.2 External Interfaces
| Interface | External Entity | Type | Description |
|-----------|-----------------|------|-------------|
| IF-EXT-001 | | | |
| IF-EXT-002 | | | |

---

## 2. Functional Hierarchy

### 2.1 Top-Level Functions
| Function ID | Function Name | Description |
|-------------|---------------|-------------|
| F-001 | | |
| F-002 | | |
| F-003 | | |

### 2.2 Functional Decomposition Tree
```
F-000: [System Function]
├── F-001: [Function 1]
│   ├── F-001.1: [Sub-function 1.1]
│   ├── F-001.2: [Sub-function 1.2]
│   └── F-001.3: [Sub-function 1.3]
├── F-002: [Function 2]
│   ├── F-002.1: [Sub-function 2.1]
│   └── F-002.2: [Sub-function 2.2]
└── F-003: [Function 3]
    └── F-003.1: [Sub-function 3.1]
```

---

## 3. Functional Flow

### 3.1 Functional Flow Block Diagram (FFBD)
[Diagram or description of functional flow]

### 3.2 N2 Diagram (Functional)

|          | F-001 | F-002 | F-003 |
|----------|-------|-------|-------|
| **F-001** | -- | [Output] | [Output] |
| **F-002** | [Input] | -- | [Output] |
| **F-003** | [Input] | [Input] | -- |

### 3.3 Functional Interface List
| ID | From | To | Data/Signal | Description |
|----|------|----|-------------|-------------|
| FI-001 | F-001 | F-002 | | |
| FI-002 | F-002 | F-003 | | |

---

## 4. Function Allocation

### 4.1 Function-to-Element Allocation
| Function | Allocated Element | Rationale |
|----------|-------------------|-----------|
| F-001 | Element A | |
| F-002 | Element B | |
| F-003 | Element A, C | |

### 4.2 Allocation Matrix
| Element | F-001 | F-002 | F-003 |
|---------|-------|-------|-------|
| Element A | P | | S |
| Element B | | P | |
| Element C | | | P |

*P = Primary, S = Secondary*

---

## 5. Modes and States

### 5.1 Operational Modes
| Mode | Description | Active Functions |
|------|-------------|------------------|
| Initialization | | F-001 |
| Operational | | F-001, F-002, F-003 |
| Standby | | F-001 |
| Safe | | F-001.1 |

### 5.2 State Transition Diagram
[Description or reference to state diagram]

---

## 6. Traceability

### 6.1 Requirements to Functions
| Requirement | Allocated Functions |
|-------------|---------------------|
| REQ-001 | F-001, F-002 |
| REQ-002 | F-002 |
| REQ-003 | F-003 |

---

*DISCLAIMER: This architecture document is AI-generated based on NASA Systems
Engineering standards. It requires human review and professional engineering
judgment before use in actual system development.*
```
