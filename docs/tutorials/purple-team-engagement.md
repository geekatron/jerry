# Learn to run a purple team engagement by working through the full lifecycle

> By the end of this tutorial you will have run a complete purple team engagement using the `/cyber-ops` skill — from a YAML config file on disk to a verified archive in `ARCHIVED` state — with every lifecycle gate confirmed along the way.

## Document Sections

| Section | Purpose |
|---------|---------|
| [What You Will Achieve](#what-you-will-achieve) | Observable end state |
| [Prerequisites](#prerequisites) | What you need before starting |
| [Steps](#steps) | The 12-step guided engagement lifecycle |
| [What You Learned](#what-you-learned) | Skills acquired |
| [Related](#related) | Next resources |

---

## What You Will Achieve

By the end of this tutorial, you will have:

- A filled-in engagement config at `work/engagements/ENG-0001/engagement-config.yaml`
- Run the engagement from `DEFINED` through all seven states to `ARCHIVED`
- Observed the G1, G3, G4, G5, G6, and G7 confirmation gates in action
- Produced a cross-team correlation report and a SHA-256-verified archive

---

## Prerequisites

Before starting, you need:

- **Jerry framework installed** — `jerry session status` exits without error
- **Docker running** — the proxy infrastructure depends on Docker; run `docker ps` and confirm it responds
- **DigitalOcean API key stored in macOS Keychain** — the purple team template reads the key from `proxy.digitalocean.api-key`; store it with:
  ```
  security add-generic-password -a proxy.digitalocean.api-key \
    -s proxy.digitalocean.api-key -w "<your-api-key>"
  ```
- **An active Jerry project** — `JERRY_PROJECT` must be set; run `jerry session status` and confirm you see a project ID
- **An authorization document on disk** — a signed letter, ticket, or statement authorising the test target; this tutorial uses `~/auth/ENG-0001-authorization.pdf`

---

## Steps

### 1. Copy the purple team template

Copy the pre-configured purple team template into your engagement workspace:

```
cp skills/cyber-ops/templates/purple-team-template.yaml \
   work/engagements/ENG-0001/engagement-config.yaml
```

**Expected result:** The file `work/engagements/ENG-0001/engagement-config.yaml` now exists and contains six CHANGEME placeholders.

---

### 2. Fill in the CHANGEME fields

Open `work/engagements/ENG-0001/engagement-config.yaml` in your editor and replace every CHANGEME field with real values. Below is the complete filled example for this tutorial:

```yaml
engagement:
  id: "ENG-0001"
  name: "Purple Team Exercise — Internal Lab"
  type: "purple_team"
  mode: "purple"
  start_date: "2026-03-26"
  classification: "confidential"

scope:
  targets:
    - host: "10.0.1.100"
      type: "ip"
      description: "Lab web server — Ubuntu 22.04"

infrastructure:
  proxy:
    enabled: true
    provider: "digitalocean"
    region: "nyc1"
    count: 3
    proxy_type: "direct_socks5"
    socks_port: 1080
  sensors:
    enabled: true
    type: "wazuh"

teams:
  red:
    operator: "alice"
    role: "attacker"
  blue:
    operator: "alice"
    role: "defender"

credentials:
  proxy_api_key:
    source: "keychain"
    key_name: "proxy.digitalocean.api-key"

rules_of_engagement:
  authorization: "~/auth/ENG-0001-authorization.pdf"
  escalation_contact: "alice@example.com"
  emergency_stop: true
  data_handling: "evidence_vault_only"

purple_team:
  technique_approval: "per_technique"
  pivot_mode: "sequential"
  correlation_mode: "real_time"

output:
  report_format: "markdown"
  report_template: "technical"
  retention_days: 90
```

**Expected result:** The file contains no remaining CHANGEME strings. Run `grep -c CHANGEME work/engagements/ENG-0001/engagement-config.yaml` — it prints `0`.

---

### 3. Create the engagement

Tell Jerry to start the engagement lifecycle:

```
Set up a new purple team engagement using the config at
work/engagements/ENG-0001/engagement-config.yaml
```

`cyber-ops-lead` parses the YAML, validates the fields, and writes the initial engagement state file.

**Expected result:** Jerry responds with the engagement summary and presents Gate G1. The output includes a line such as:

```
Lifecycle state: DEFINED
G1 — Scope Approval Required
Targets: 10.0.1.100 (Lab web server — Ubuntu 22.04)
Approve this engagement scope and proceed to provisioning? [yes/no]
```

---

### 4. Approve scope (G1)

Read the targets and techniques listed in the G1 prompt. Confirm the target IP matches your authorization document, then type:

```
yes
```

**Expected result:** Jerry records G1 as approved with your username and a timestamp, then prints:

```
G1 approved. Transitioning to PROVISIONING.
Lifecycle state: PROVISIONING
```

---

### 5. Review the provisioning plan (G2)

`cyber-ops-provision` reads the engagement config and prints the infrastructure plan — proxy node count, region, sensor type, and exchange directory path. Read through it to confirm the resource count and region are correct, then type:

```
yes
```

**Expected result:** Infrastructure provisioning begins. Jerry prints progress lines as the three DigitalOcean proxy nodes and the Wazuh sensor come online:

```
[Provisioning] Proxy node 1/3 — nyc1 — OK
[Provisioning] Proxy node 2/3 — nyc1 — OK
[Provisioning] Proxy node 3/3 — nyc1 — OK
[Provisioning] Wazuh sensor — OK
```

---

### 6. Approve infrastructure (G3)

`cyber-ops-provision` runs health checks against all provisioned resources and presents Gate G3:

```
G3 — Infrastructure Approval Required
3/3 proxy nodes healthy
Wazuh sensor receiving events
Exchange directory: work/engagements/ENG-0001/exchange/
Approve activation? [yes/no]
```

Confirm the node count shows 3/3 healthy, then type:

```
yes
```

**Expected result:** Jerry transitions state and prints:

```
G3 approved. Transitioning to ACTIVE.
Lifecycle state: ACTIVE
```

---

### 7. Execute a red team technique

With the engagement ACTIVE, ask the red team to run an initial reconnaissance technique against the target. In purple mode this also hands the action to the blue team monitor in real time:

```
Use red-lead to execute T1046 (Network Service Discovery) against 10.0.1.100.
Blue team monitoring is active.
```

Jerry presents Gate G4 before the technique runs:

```
G4 — Technique Approval Required
Technique: T1046 — Network Service Discovery
Target: 10.0.1.100
Blue team monitoring: active
Execute? [yes/no]
```

Type:

```
yes
```

**Expected result:** The technique executes, red team findings are written to `work/engagements/ENG-0001/red-team/findings/`, and the blue team detection event (if triggered) is written to `work/engagements/ENG-0001/blue-team/detections/`. Jerry prints a summary line such as:

```
Red: T1046 executed — 8 open ports discovered
Blue: Detection event logged — rule SYN-scan-threshold triggered
```

---

### 8. Complete execution

Signal that the execution phase is done:

```
Execution complete. Proceed to analysis.
```

**Expected result:** Jerry transitions state and prints:

```
Lifecycle state: ANALYZING
Starting cross-team correlation...
```

`cyber-ops-analyze` begins reading the findings and detections directories automatically.

---

### 9. Review the analysis report

`cyber-ops-analyze` writes its report to `work/engagements/ENG-0001/analysis/cross-team-correlation.md`. Read it:

```
Read work/engagements/ENG-0001/analysis/cross-team-correlation.md
```

The report contains three sections: an executive gap summary (L0), a per-technique correlation table (L1), and a strategic detection posture assessment (L2). The correlation table shows each technique attempted, whether the blue team detected it, and the confidence rating (HIGH / MEDIUM / LOW).

**Expected result:** The file exists and contains a table with at least one row for T1046. The row shows the detection event ID, confidence rating, and whether the technique was detected or missed.

---

### 10. Approve the report (G5)

`cyber-ops-lead` presents Gate G5 after the analysis report is ready:

```
G5 — Report Review Required
Analysis complete. Engagement report ready for review.
Approve teardown? [yes/no]
```

Confirm the report looks correct, then type:

```
yes
```

**Expected result:** Jerry transitions state and prints:

```
G5 approved. Transitioning to TEARDOWN.
Lifecycle state: TEARDOWN
```

---

### 11. Confirm teardown (G6)

`cyber-ops-teardown` presents Gate G6 with a full list of what will be archived and destroyed:

```
G6 — Teardown Confirmation Required
Archive: work/engagements/ENG-0001/archive/2026-03-26T120000/
  Files to archive: 14
Destroy: 3 proxy nodes (DigitalOcean nyc1)
Revoke: 1 SOCKS5 credential, 1 API session token
Proceed? [yes/no]
```

Verify the file count and resource list, then type:

```
yes
```

**Expected result:** Jerry runs the teardown sequence and prints progress lines:

```
[Archive] 14/14 files archived — OK
[Integrity] SHA-256 manifest written — OK
[Revoke] proxy.digitalocean.api-key session token — revoked
[Destroy] Proxy node 1/3 — destroyed
[Destroy] Proxy node 2/3 — destroyed
[Destroy] Proxy node 3/3 — destroyed
```

---

### 12. Verify archive integrity

`cyber-ops-teardown` automatically presents Gate G7 after destruction completes:

```
G7 — Archive Integrity Verification
14 files archived
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

Confirm the archive manifest exists:

```
ls work/engagements/ENG-0001/archive/
```

You should see a timestamped directory containing your engagement artifacts and `MANIFEST.sha256`.

---

## What You Learned

You now know how to:

- Copy and fill in `skills/cyber-ops/templates/purple-team-template.yaml` to define an engagement
- Create an engagement with `/cyber-ops` and confirm it enters `DEFINED` state
- Approve scope (G1), provisioning plan (G2), and infrastructure health (G3) before operations begin
- Execute a red team technique under per-technique approval (G4) with real-time blue team monitoring
- Signal execution complete and observe the automatic transition to `ANALYZING`
- Read the cross-team correlation report at `work/engagements/{id}/analysis/cross-team-correlation.md`
- Approve teardown (G5, G6) and confirm archive integrity (G7) before the engagement closes

---

## Related

- **How-To Guide:** [How to run a split red-vs-blue engagement](../howto/split-team-engagement.md) — Run the same lifecycle with isolated teams and no shared visibility during execution
- **Reference:** [Engagement Lifecycle State Machine](../../skills/cyber-ops/references/state-machine.md) — Full specification of the seven states, all gates, and transition conditions
- **Reference:** [Purple Team Template fields](../../skills/cyber-ops/templates/purple-team-template.yaml) — Every YAML field with its type and default value
- **Explanation:** [About the cyber-ops engagement lifecycle](../explanation/cyber-ops-lifecycle.md) — Why the lifecycle is designed with fail-safe gates and archive-before-destroy ordering
