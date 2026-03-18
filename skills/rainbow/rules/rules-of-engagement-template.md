# Rules of Engagement Template -- /rainbow

> Template for defining operational constraints during /rainbow engagements. Copy and customize for each engagement. Companion to the engagement scope template (`engagement-scope-template.yaml`).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Engagement Information](#engagement-information) | Engagement identifiers and dates |
| [Operational Constraints](#operational-constraints) | Rate limits, timing, stealth |
| [Communication Protocol](#communication-protocol) | Escalation contacts and channels |
| [Emergency Stop Procedure](#emergency-stop-procedure) | How to halt all operations |
| [Data Handling](#data-handling) | Evidence retention and destruction |
| [Scope Boundaries](#scope-boundaries) | Explicit in/out of scope |
| [Zone 3 Escalation Authorization](#zone-3-escalation-authorization) | Who approves escalation |
| [Approval](#approval) | Operator signature |

---

## Engagement Information

| Field | Value |
|-------|-------|
| **Engagement ID** | RBW-NNNN |
| **Scope Document** | `work/engagements/RBW-NNNN/SCOPE.md` |
| **Start Date** | YYYY-MM-DDTHH:MM:SSZ |
| **End Date** | YYYY-MM-DDTHH:MM:SSZ |
| **Operator** | [Name] |
| **Engagement Type** | [Reconnaissance / Assessment / Penetration Test / Red Team] |

---

## Operational Constraints

### Rate Limiting

| Constraint | Value | Rationale |
|-----------|-------|-----------|
| Max requests per second | 10 | Avoid triggering rate-based WAF/IDS rules |
| Max concurrent scans | 3 | Limit resource consumption on target infrastructure |
| Port scan rate | 1000 ports/sec | Naabu default safe rate |
| Web crawl depth | 3 levels | Katana depth limit to avoid deep recursive crawling |
| DNS query rate | 100 queries/sec | dnsx default rate |

### Timing Constraints

| Constraint | Value |
|-----------|-------|
| Authorized hours | [All hours / Business hours only / Off-hours only] |
| Timezone | [UTC / Local timezone] |
| Blackout periods | [None / List specific periods] |

### Stealth Requirements

| Requirement | Enabled | Notes |
|-------------|---------|-------|
| User-Agent randomization | [Yes/No] | httpx, Katana user-agent customization |
| Rate jitter | [Yes/No] | Random delay between requests |
| Source IP rotation | [Yes/No] | Multiple source IPs if available |
| DNS over HTTPS | [Yes/No] | Prevent DNS monitoring |

---

## Communication Protocol

| Role | Contact | Channel |
|------|---------|---------|
| Primary operator | [Name] | [Email / Slack / Phone] |
| Backup operator | [Name] | [Email / Slack / Phone] |
| Escalation authority | [Name] | [Email / Slack / Phone] |
| Target system owner | [Name] | [Email / Slack / Phone] |

### Status Reporting

| Event | Report To | Frequency |
|-------|-----------|-----------|
| Phase completion | Primary operator | Per phase |
| Critical finding (CVSS >= 9.0) | Primary operator | Immediate |
| Zone 3 escalation request | Escalation authority | Per occurrence |
| Credential quarantine event | Primary operator | Immediate |
| Emergency stop | All contacts | Immediate |

---

## Emergency Stop Procedure

1. **Operator communicates "STOP"** via the designated communication channel.
2. **rainbow-orchestrator** immediately halts all active Zone 2/3 operations.
3. **All agents** cease tool execution within the current operation.
4. **Partial results** are persisted to the engagement artifact directory.
5. **Emergency stop event** is logged with timestamp, reason, and operator identity.
6. **Engagement transitions** to REPORTING phase with partial results.
7. **Post-stop review** conducted within 24 hours.

### Emergency Stop Triggers

- [ ] Operator decision (any reason)
- [ ] Target system instability or degradation observed
- [ ] Unintended impact on non-target systems
- [ ] Legal or compliance concern
- [ ] Uncontained credential exposure
- [ ] Time window expiration

---

## Data Handling

### Evidence Classification

| Classification | Examples | Handling |
|---------------|----------|---------|
| Findings | Vulnerability reports, reconnaissance data | Retained per retention period |
| Credentials | Any credential material from tool output | Quarantined via credential filter; never stored in reports |
| Raw tool output | JSONL files, scan artifacts | Retained per retention period |
| Audit logs | Zone 2/3 operation logs | Retained per retention period; immutable |

### Retention and Destruction

| Parameter | Value |
|-----------|-------|
| Retention period | [90 days / Custom] |
| Storage location | `work/engagements/{engagement-id}/` |
| Destruction method | [secure-delete / cryptographic-erasure] |
| Destruction confirmation | Operator signs off on destruction |

### Credential Quarantine

All /rainbow engagements apply the credential filter pipeline (3-layer: L1 regex, L2 entropy, L3 structural). Credential material is NEVER included in reports, context windows, or handoffs.

Quarantine location: `work/.credential-quarantine/`

---

## Scope Boundaries

### Explicitly In Scope

List all authorized targets and techniques. Reference the engagement scope document for the authoritative list.

- [ ] Targets: [per SCOPE.md authorized_targets]
- [ ] Techniques: [per SCOPE.md technique_allowlist]
- [ ] Zone 2 operations: [per zone-2-active.md permitted operations]

### Explicitly Out of Scope

- [ ] All targets in SCOPE.md excluded_targets
- [ ] All techniques not in SCOPE.md technique_allowlist
- [ ] Zone 3 operations without per-operation approval
- [ ] Any target not explicitly listed in authorized_targets
- [ ] [Additional exclusions specific to this engagement]

---

## Zone 3 Escalation Authorization

| Authority | Name |
|-----------|------|
| Primary escalation authority | [Name from SCOPE.md] |
| Backup escalation authority | [Name or "None"] |

### Zone 3 Approval Process

1. Agent halts and presents escalation details.
2. Operator reviews template/technique metadata.
3. Operator explicitly approves or declines.
4. Approval is per-operation, per-target.
5. All approvals logged in Zone 3 audit log.

---

## Approval

| Field | Value |
|-------|-------|
| **Prepared by** | [rainbow-orchestrator / red-lead] |
| **Reviewed by** | [Operator name] |
| **Approved by** | [Operator name] |
| **Approval date** | [ISO 8601 timestamp] |
| **Confirmation** | [Free-form statement confirming understanding and agreement] |

---

*Template Version: 1.0.0*
*Source: ADR-PROJ023-001, /red-team red-lead engagement methodology*
*See also: `skills/rainbow/rules/engagement-lifecycle.md`, `skills/rainbow/rules/engagement-scope-template.yaml`*
