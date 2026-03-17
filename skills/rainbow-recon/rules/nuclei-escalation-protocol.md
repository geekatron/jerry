# Nuclei Dual-Zone Escalation Protocol

> Governs the Zone 2 to Zone 3 escalation boundary for Nuclei template execution within /rainbow-recon. Nuclei is a dual-zone tool: detection templates operate at Zone 2; exploit templates require Zone 3 per-operation human approval.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Zone Classification](#zone-classification) | Which Nuclei operations belong to which zone |
| [Escalation Triggers](#escalation-triggers) | Conditions that force Zone 3 escalation |
| [Classification Procedure](#classification-procedure) | Step-by-step template classification before execution |
| [Escalation Workflow](#escalation-workflow) | What happens when escalation triggers |
| [Operator Approval](#operator-approval) | How Zone 3 approval works for Nuclei |
| [Template Review Process](#template-review-process) | How custom templates are added to the allowlist |
| [Traceability](#traceability) | Source references |

---

## Zone Classification

Nuclei template classification is based on the specific template content -- not on agent judgment. The classification is deterministic: parse the template YAML, check against rules, and route to the correct zone.

| Operation | Zone | Classification Rule |
|-----------|------|-------------------|
| Detection templates: severity `info`, `low`, `medium`, `high`, `critical` WITHOUT deny tags | Zone 2 | Template is on the allowlist in `nuclei-template-allowlist.yaml`; no deny_tags present; no deny_extractor_fields present |
| Exploit templates: tagged `exploit`, `rce`, `upload`, `sqli-blind`, `intrusive`, `dos`, `fuzzing`, `brute-force`, `command-injection`, `deserialization`, `code-injection` | Zone 3 | Template matches deny_tags list; agent presents template metadata to user for per-operation approval per P-020 |
| Templates with extractors targeting credential/session fields | Zone 3 | Template extractors target fields in deny_extractor_fields list |
| Custom/community templates not on allowlist | Zone 3 (default) | Fail-closed: all custom templates default to Zone 3 until reviewed and added to allowlist |

---

## Escalation Triggers

The following conditions MUST trigger escalation from Zone 2 to Zone 3. The agent halts the current operation and returns control to the user (or rainbow-orchestrator) with the escalation reason.

| Trigger | Detection Method | Agent Action |
|---------|-----------------|--------------|
| Template tags include any deny_tag | Parse `info.tags` from template YAML | HALT; present template ID, name, severity, and tags to user |
| Template extractors target deny fields | Parse `extractors` section for `name` or `part` matching deny list | HALT; present extractor details to user |
| Template directory not in allowed list | Check template path against `zone_2_allowed.template_directories` | HALT; inform user template category not approved for Zone 2 |
| Template is custom or community-sourced | Template not in official nuclei-templates repository | HALT; request human review of template before execution |
| Unrecognized template format | Template does not parse correctly | HALT; fail-closed to Zone 3 |

---

## Classification Procedure

The `rainbow-recon-pipeline` agent MUST execute this procedure for EVERY Nuclei template before execution. No exceptions.

### Step 0: Parse Validation (Fail-Closed Default)

Attempt to parse the Nuclei template as valid YAML. If parsing fails for any reason (malformed YAML, missing `id` or `info` fields, unrecognized template format, I/O error):

- **HALT. Classify as Zone 3 immediately.**
- Present the parse failure details to the user.
- Log the failure in the audit log with escalation reason "template_parse_failure".
- Do NOT attempt to execute a template that cannot be parsed and classified.

This ensures that template format errors or corruption never bypass the classification procedure.

### Step 1: Parse Template YAML

Read the Nuclei template file and extract:
- `id` (template identifier)
- `info.name` (template name)
- `info.severity` (info/low/medium/high/critical)
- `info.tags` (comma-separated tag list)
- `info.classification` (optional: CVE, CWE, CVSS data)
- Presence and content of `extractors` section

### Step 2: Check Deny Tags

Compare `info.tags` against the `deny_tags` list in `nuclei-template-allowlist.yaml`:
- `exploit`, `rce`, `upload`, `sqli-blind`, `intrusive`, `dos`, `fuzzing`, `brute-force`, `command-injection`, `deserialization`, `code-injection`

If ANY deny_tag matches: **HALT. Escalate to Zone 3.**

### Step 3: Check Extractor Fields

If the template contains an `extractors` section, check whether any extractor targets fields matching the `deny_extractor_fields` list:
- `password`, `secret`, `token`, `key`, `credential`, `session`, `auth`, `cookie`, `api_key`, `access_key`, `private_key`, `connection_string`

If ANY deny field matches: **HALT. Escalate to Zone 3.**

### Step 4: Check Template Directory

Verify the template path is within a `zone_2_allowed.template_directories` category:
- `cves/`, `misconfiguration/`, `exposed-panels/`, `technologies/`, `dns/`, `ssl/`, `http/`, `network/`, `file/`, `headless/`

If NOT in an allowed directory: **HALT. Escalate to Zone 3.**

### Step 5: Execute at Zone 2

If all checks pass, execute the template at Zone 2 with standard engagement scope validation (target authorized, time_window current, technique on allowlist).

---

## Escalation Workflow

When escalation triggers:

1. **HALT execution.** Do NOT run the Nuclei template.
2. **Log the escalation event** in the audit log with:
   - Template ID, name, severity, tags
   - Triggering condition (deny_tag, deny_extractor, directory, custom)
   - Engagement ID and target
3. **Present to user:**
   - Template metadata (ID, name, severity, tags, description)
   - Specific reason for escalation
   - The deny_tag or deny_field that triggered escalation
   - Request for per-operation approval
4. **If user approves:** Execute the template with Zone 3 audit logging. Record approval in audit log.
5. **If user declines:** Skip the template. Log the skip. Continue with remaining Zone 2 templates.

---

## Operator Approval

Zone 3 Nuclei operations require explicit per-operation human approval per P-020.

### Approval Requirements

| Requirement | Description |
|-------------|-------------|
| Template metadata presented | User must see template ID, name, severity, tags, and description before approving |
| Escalation reason stated | User must see the specific deny_tag, deny_field, or directory causing escalation |
| Target confirmed | User must confirm the target is appropriate for the escalated template |
| Approval recorded | User approval timestamp and identity recorded in audit log |

### Approval Scope

- Approval is **per-template, per-target**. Approving template T1 for target A does not authorize T1 for target B.
- Approval does NOT carry over to future engagements. Each engagement requires fresh approval.
- Approval may be revoked by the operator at any time by updating the engagement scope document.

---

## Template Review Process

Custom or community Nuclei templates can be added to the Zone 2 allowlist through a structured review process.

### Review Steps

1. **Submit template for review:** Provide the YAML template file.
2. **Classification check:** Run the classification procedure (Steps 1-4 above).
3. **Manual review:** Human reviewer verifies:
   - Template does NOT perform exploitation or modify target state.
   - Template extractors do NOT target credential material.
   - Template is appropriate for Zone 2 (detection only).
4. **Add to allowlist:** If approved, add template ID to a `custom_approved` section in `nuclei-template-allowlist.yaml`.
5. **Review criticality:** C3 minimum (AE-005: security-relevant change).

### Custom Template Section (Future)

When custom templates are approved, they are added to `nuclei-template-allowlist.yaml` under:

```yaml
custom_approved:
  - template_id: "custom-example-001"
    reviewed_by: "operator-name"
    reviewed_at: "2026-03-16T00:00:00Z"
    justification: "Detection-only template for internal service fingerprinting"
```

---

## Traceability

| Reference | Location |
|-----------|----------|
| ADR-PROJ023-001 (Architecture Decision) | `projects/PROJ-023-exploit-framework/work/design/skill-architecture.md` |
| Zone 2 Guardrail Profile | `skills/rainbow/rules/zone-2-active.md` |
| Nuclei Template Allowlist | `skills/rainbow-recon/rules/nuclei-template-allowlist.yaml` |
| Credential Filter Specification | `skills/rainbow/rules/rainbow-credential-filter.md` |
| Nuclei Documentation | [ProjectDiscovery Nuclei Docs](https://docs.projectdiscovery.io/opensource/nuclei/running) |
| Nuclei Template Guide | [nuclei-templates GitHub](https://github.com/projectdiscovery/nuclei-templates) |
