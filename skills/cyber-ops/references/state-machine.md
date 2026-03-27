# Engagement Lifecycle State Machine

> Reference document for the `/cyber-ops` engagement lifecycle state machine.
> Source: ADR-PROJ023-010 Decision 1 (State Machine specification)

## Document Sections

| Section | Purpose |
|---------|---------|
| [States](#states) | 7 engagement states |
| [Transitions](#transitions) | State transition table |
| [Gates](#gates) | Confirmation gate specifications |
| [Diagram](#diagram) | Visual state machine |

---

## States

| State | Description | Entry Condition | Exit Condition |
|-------|-------------|-----------------|----------------|
| DEFINED | Engagement scope created but not approved | Engagement config YAML parsed | Operator approves scope (G1) |
| PROVISIONING | Infrastructure being stood up | Scope approved | All nodes healthy (G3) |
| ACTIVE | Operations in progress (red/blue/purple) | Infrastructure ready | Operator signals execution complete |
| ANALYZING | Cross-team correlation and gap analysis | Execution complete | Analysis artifacts generated |
| REPORTING | Report generation and review | Analysis complete | Operator reviews report (G5) |
| TEARDOWN | Infrastructure destruction + credential revocation | Report reviewed | Teardown complete + archive verified (G6, G7) |
| ARCHIVED | Engagement complete, evidence preserved | Teardown verified | Terminal state |

---

## Transitions

| From | To | Trigger | Gate | Fail-Safe Default |
|------|-----|---------|------|-------------------|
| DEFINED | PROVISIONING | Scope approved by operator | G1 (scope approval) | NO — do not provision |
| DEFINED | DEFINED | Scope rejected | None (revision loop) | — |
| PROVISIONING | ACTIVE | All infrastructure healthy | G3 (infra approval) | NO — do not activate |
| PROVISIONING | PROVISIONING | Provision failed | None (retry/abort) | — |
| ACTIVE | ANALYZING | Operator signals execution complete | None (operator decision) | — |
| ANALYZING | REPORTING | Analysis artifacts generated | None (automatic) | — |
| REPORTING | TEARDOWN | Operator reviews report | G5 (report review) | NO — do not tear down |
| TEARDOWN | ARCHIVED | Teardown complete + archive verified | G6 (teardown confirm), G7 (archive verify) | NO — do not archive |

---

## Gates

| Gate | Phase Boundary | Question to Operator | Fail-Safe | P-020 Enforcement |
|------|---------------|---------------------|-----------|-------------------|
| G1 | DEFINED → PROVISIONING | "Approve this engagement scope? [targets, techniques, exclusions listed]" | NO | Operator must explicitly approve |
| G2 | DEFINED → PROVISIONING (purple/split) | "Approve assessment scope for blue team? [sensors, monitoring listed]" | NO | Blue team scope separate approval |
| G3 | PROVISIONING → ACTIVE | "Infrastructure is ready. N nodes healthy. Approve activation?" | NO | Operator confirms before ops begin |
| G4 | ACTIVE (per-technique, purple only) | "Execute [technique] against [target]? Blue team monitoring active." | NO | Per-technique approval in purple mode |
| G5 | REPORTING → TEARDOWN | "Review the engagement report. Approve teardown?" | NO | Report must be reviewed before cleanup |
| G6 | TEARDOWN start | "Confirm teardown: destroy N nodes, revoke M credentials, archive P files?" | NO | Explicit destruction approval |
| G7 | TEARDOWN → ARCHIVED | "Archive integrity verified. N files, SHA-256 manifest complete." | YES | Automatic if integrity passes |

---

## Diagram

```
                    +---------+
                    | DEFINED |<----+
                    +----+----+     |
                         |          | (scope rejected — revise)
                    G1/G2|          |
                         v          |
                  +------+-------+  |
                  | PROVISIONING |--+
                  +------+-------+
                         |  ^
                    G3   |  | (retry on failure)
                         v  |
                    +----+----+
                    |  ACTIVE  |
                    +----+----+
                         |
                    (ops complete)
                         v
                  +------+-------+
                  |  ANALYZING   |
                  +------+-------+
                         |
                    (auto)
                         v
                  +------+-------+
                  |  REPORTING   |
                  +------+-------+
                         |
                    G5   |
                         v
                  +------+-------+
                  |   TEARDOWN   |
                  +------+-------+
                         |
                    G6/G7|
                         v
                  +------+-------+
                  |   ARCHIVED   |
                  +--------------+
```
