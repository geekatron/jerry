# Learn to run a single-team engagement by working through the standard lifecycle

> By the end of this tutorial you will have run a complete single-team engagement using the `/rainbow` skill — from a YAML config file on disk to a verified archive in `ARCHIVED` state — in 15 steps with one operator and no cross-team coordination overhead.

## Document Sections

| Section | Purpose |
|---------|---------|
| [What You Will Achieve](#what-you-will-achieve) | Observable end state |
| [Prerequisites](#prerequisites) | What you need before starting |
| [Steps](#steps) | The 15-step guided single-team engagement lifecycle |
| [What You Learned](#what-you-learned) | Skills acquired |
| [Related](#related) | Next resources |

---

## What You Will Achieve

By the end of this tutorial, you will have:

- A filled-in engagement config at `work/engagements/ENG-0001/engagement-config.yaml` with `mode: single`
- Run the engagement as a single operator from `DEFINED` through all seven states to `ARCHIVED`
- Executed either a red-only (recon and exploitation) or blue-only (detection and threat hunting) workflow within the same lifecycle
- Produced an engagement report and a SHA-256-verified archive

---

## Prerequisites

Before starting, you need:

- **One operator** — a single person running a standard pentest or a standalone threat hunt; this tutorial uses the operator name `alice`
- **Jerry framework installed** — run `jerry session status` and confirm it exits without error
- **Docker running** — run `docker ps` and confirm it responds; the proxy infrastructure requires Docker
- **DigitalOcean API key stored in macOS Keychain** — store it with:
  ```
  security add-generic-password -a proxy.digitalocean.api-key \
    -s proxy.digitalocean.api-key -w "<your-api-key>"
  ```
- **An active Jerry project** — `JERRY_PROJECT` must be set; run `jerry session status` and confirm you see a project ID
- **An authorization document on disk** — a signed letter, ticket, or statement authorizing the test target; this tutorial uses `~/auth/ENG-0001-authorization.pdf`

---

## Steps

### 1. Copy the single-team template

Copy the pre-configured single-team template into your engagement workspace:

```
cp skills/rainbow/templates/single-team-template.yaml \
   work/engagements/ENG-0001/engagement-config.yaml
```

**Expected result:** The file `work/engagements/ENG-0001/engagement-config.yaml` now exists and contains the `mode: single` field and five CHANGEME placeholders.

---

### 2. Fill in the engagement type

Open `work/engagements/ENG-0001/engagement-config.yaml` in your editor. Set the `engagement_focus` field to reflect what this engagement will do. For a red-only pentest, use `red_only`. For a blue-only threat hunt, use `blue_only`.

This tutorial uses `red_only`. Set:

```yaml
engagement:
  id: "ENG-0001"
  name: "Pentest — Internal Lab"
  type: "single_team"
  mode: "single"
  engagement_focus: "red_only"
  start_date: "2026-03-26"
  classification: "confidential"
```

**Expected result:** The `engagement_focus` field reads `red_only` (not CHANGEME). Save the file.

---

### 3. Fill in the targets

Still in the editor, populate the `scope.targets` section with the authorized target. Use the IP and description from your authorization document:

```yaml
scope:
  targets:
    - host: "10.0.1.100"
      type: "ip"
      description: "Lab web server — Ubuntu 22.04"
```

**Expected result:** The `scope.targets` list contains at least one entry with a non-empty `host` and `description`.

---

### 4. Fill in the remaining fields

Complete the rest of the config. Below is the full filled example for this tutorial:

```yaml
infrastructure:
  proxy:
    enabled: true
    provider: "digitalocean"
    region: "nyc1"
    count: 2
    proxy_type: "direct_socks5"
    socks_port: 1080

teams:
  red:
    operator: "alice"
    role: "attacker"

credentials:
  proxy_api_key:
    source: "keychain"
    key_name: "proxy.digitalocean.api-key"

rules_of_engagement:
  authorization: "~/auth/ENG-0001-authorization.pdf"
  escalation_contact: "alice@example.com"
  emergency_stop: true
  data_handling: "evidence_vault_only"

output:
  report_format: "markdown"
  report_template: "technical"
  retention_days: 90
```

Verify there are no remaining CHANGEME strings:

```
grep -c CHANGEME work/engagements/ENG-0001/engagement-config.yaml
```

**Expected result:** The command prints `0`.

---

### 5. Create the engagement

Tell Jerry to start the engagement lifecycle:

```
Set up a new single-team engagement using the config at
work/engagements/ENG-0001/engagement-config.yaml
```

`rainbow-orchestrator` parses the YAML, validates the fields, and writes the initial engagement state file.

**Expected result:** Jerry responds with the engagement summary and presents Gate G1:

```
Lifecycle state: DEFINED
G1 — Scope Approval Required
Engagement: ENG-0001 (single mode, red_only)
Targets: 10.0.1.100 (Lab web server — Ubuntu 22.04)
Approve this engagement scope and proceed to provisioning? [yes/no]
```

---

### 6. Approve scope (G1)

Read the target list in the G1 prompt. Confirm the target IP matches your authorization document, then type:

```
yes
```

**Expected result:** Jerry records your G1 approval with username `alice` and a timestamp, then prints:

```
G1 approved by alice. Transitioning to PROVISIONING.
Lifecycle state: PROVISIONING
```

---

### 7. Review the provisioning plan

`rainbow-orchestrator` prints the infrastructure plan — proxy node count, region, and any sensors. Read the node count and region to confirm they are correct, then type:

```
yes
```

**Expected result:** Provisioning begins and Jerry prints progress lines as the two DigitalOcean proxy nodes come online:

```
[Provisioning] Proxy node 1/2 — nyc1 — OK
[Provisioning] Proxy node 2/2 — nyc1 — OK
```

---

### 8. Approve infrastructure (G3)

`rainbow-orchestrator` runs health checks and presents Gate G3:

```
G3 — Infrastructure Approval Required
2/2 proxy nodes healthy
Exchange directory: work/engagements/ENG-0001/exchange/
Approve activation? [yes/no]
```

Confirm the node count shows 2/2 healthy, then type:

```
yes
```

**Expected result:** Jerry transitions to `ACTIVE` state:

```
G3 approved. Transitioning to ACTIVE.
Lifecycle state: ACTIVE
```

---

### 9. Execute recon

With the engagement `ACTIVE`, run reconnaissance against the target. Gate G4 appears before the technique executes:

```
Use rainbow-recon-pipeline to run T1046 (Network Service Discovery)
against 10.0.1.100.
```

Jerry presents G4:

```
G4 — Technique Approval Required
Technique: T1046 — Network Service Discovery
Target: 10.0.1.100
Execute? [yes/no]
```

Type:

```
yes
```

**Expected result:** The reconnaissance technique executes and Jerry prints a summary:

```
Red: T1046 executed — 8 open ports discovered
Findings written to: work/engagements/ENG-0001/red-team/findings/T1046-20260326.md
```

---

### 10. Execute exploitation

Run one exploitation technique against a service discovered in the previous step. Gate G4 appears again:

```
Use rainbow-exploit-ops to execute T1190 (Exploit Public-Facing Application)
against 10.0.1.100 port 80.
```

Jerry presents G4:

```
G4 — Technique Approval Required
Technique: T1190 — Exploit Public-Facing Application
Target: 10.0.1.100:80
Execute? [yes/no]
```

Type:

```
yes
```

**Expected result:** The technique executes and findings are written alongside the recon output:

```
Red: T1190 executed — vulnerable endpoint identified on port 80
Findings written to: work/engagements/ENG-0001/red-team/findings/T1190-20260326.md
```

---

### 11. Complete execution

Signal that the execution phase is done:

```
Execution complete. Proceed to analysis.
```

**Expected result:** Jerry transitions state:

```
Lifecycle state: ANALYZING
Aggregating findings from work/engagements/ENG-0001/red-team/findings/...
```

`rainbow-orchestrator` reads all findings files automatically.

---

### 12. Read the analysis report

`rainbow-orchestrator` writes the report to `work/engagements/ENG-0001/reports/engagement-report.md`. Read it:

```
Read work/engagements/ENG-0001/reports/engagement-report.md
```

The report contains an executive summary (L0), per-technique findings table (L1), and risk prioritization with remediation recommendations (L2).

**Expected result:** The file exists and contains a findings table with at least two rows — one for T1046 and one for T1190. Each row shows the technique ID, the finding, and a severity rating (CRITICAL / HIGH / MEDIUM / LOW).

---

### 13. Transition to reporting

After reviewing the report, signal readiness to proceed:

```
Report reviewed. Proceed to teardown.
```

**Expected result:** Jerry presents Gate G5 and transitions state:

```
G5 — Report Review Required
Engagement report ready. Approve teardown? [yes/no]
```

Type:

```
yes
```

```
G5 approved. Transitioning to TEARDOWN.
Lifecycle state: TEARDOWN
```

---

### 14. Confirm teardown (G6)

`rainbow-orchestrator` presents Gate G6 with a full list of what will be archived and destroyed:

```
G6 — Teardown Confirmation Required
Archive: work/engagements/ENG-0001/archive/2026-03-26T120000/
  Files to archive: 8
Destroy: 2 proxy nodes (DigitalOcean nyc1)
Revoke: 1 SOCKS5 credential, 1 API session token
Proceed? [yes/no]
```

Verify the file count and resource list, then type:

```
yes
```

**Expected result:** Jerry runs the teardown sequence:

```
[Archive] 8/8 files archived — OK
[Integrity] SHA-256 manifest written — OK
[Revoke] proxy.digitalocean.api-key session token — revoked
[Destroy] Proxy node 1/2 — destroyed
[Destroy] Proxy node 2/2 — destroyed
```

---

### 15. Verify archive integrity (G7)

`rainbow-orchestrator` presents Gate G7 automatically after destruction:

```
G7 — Archive Integrity Verification
8 files archived
SHA-256 manifest: work/engagements/ENG-0001/archive/2026-03-26T120000/MANIFEST.sha256
Integrity check: PASS
No engagement resources remain in DigitalOcean nyc1.
Archive complete. Transition to ARCHIVED? [yes/no]
```

Type:

```
yes
```

**Expected result:** Jerry prints the final state transition:

```
G7 verified. Transitioning to ARCHIVED.
Lifecycle state: ARCHIVED
Engagement ENG-0001 complete.
```

Confirm the archive exists:

```
ls work/engagements/ENG-0001/archive/
```

You see a timestamped directory containing all engagement artifacts and `MANIFEST.sha256`.

---

## What You Learned

You now know how to:

- Copy and fill in `skills/rainbow/templates/single-team-template.yaml` with `mode: single` and `engagement_focus: red_only`
- Create a single-team engagement with `/rainbow` and confirm it enters `DEFINED` state
- Approve scope (G1), provisioning plan, and infrastructure health (G3) with a single operator
- Execute recon and exploitation techniques under per-technique approval (G4) with no second operator required
- Signal execution complete and observe the automatic transition to `ANALYZING`
- Read the engagement report at `work/engagements/{id}/reports/engagement-report.md`
- Approve teardown (G5, G6) and confirm archive integrity (G7) before the engagement closes

---

## Related

- **Tutorial:** [Learn to run a split red-vs-blue engagement by working through information isolation](split-team-engagement.md) — Add a second operator and enforce information isolation between red and blue during execution
- **Tutorial:** [Learn to run a purple team engagement by working through the full lifecycle](purple-team-engagement.md) — Single operator running both red and blue roles with real-time correlation
- **Reference:** [Engagement Lifecycle State Machine](../../skills/rainbow/rules/engagement-lifecycle.md) — Full specification of the states, all gates, and transition conditions
- **Explanation:** [About the cyber-ops engagement lifecycle](../explanation/cyber-ops-lifecycle.md) — Why the lifecycle uses fail-safe gates and archive-before-destroy ordering
