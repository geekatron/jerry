# Learn to run a split red-vs-blue engagement by working through information isolation

> By the end of this tutorial you will have run a complete split-team engagement using the `/rainbow` skill — with two operators assigned to separate teams, scope approved independently by each team, and red activity kept hidden from the blue operator until the cross-team correlation step.

## Document Sections

| Section | Purpose |
|---------|---------|
| [What You Will Achieve](#what-you-will-achieve) | Observable end state |
| [Prerequisites](#prerequisites) | What you need before starting |
| [Steps](#steps) | The 11-step guided split-team engagement lifecycle |
| [What You Learned](#what-you-learned) | Skills acquired |
| [Related](#related) | Next resources |

---

## What You Will Achieve

By the end of this tutorial, you will have:

- A filled-in engagement config at `work/engagements/ENG-SPLIT-001/engagement-config.yaml` with `mode: split`
- Two named operators assigned — one to the `red` team, one to the `blue` team
- Run the engagement from `DEFINED` through all seven states to `ARCHIVED`
- Confirmed that blue had no visibility into red findings during the `ACTIVE` phase
- Produced a cross-team correlation report and observed the first moment both teams see each other's data

---

## Prerequisites

Before starting, you need:

- **Two operators** — two separate people (or two separate terminal sessions), one acting as the red operator and one acting as the blue operator; this tutorial calls them `alice` (red) and `bob` (blue)
- **Jerry framework installed** — run `jerry session status` in both terminals and confirm each exits without error
- **Docker running** — run `docker ps` and confirm it responds; the proxy infrastructure requires Docker
- **DigitalOcean API key stored in macOS Keychain** — store it once with:
  ```
  security add-generic-password -a proxy.digitalocean.api-key \
    -s proxy.digitalocean.api-key -w "<your-api-key>"
  ```
- **An active Jerry project** — `JERRY_PROJECT` must be set in both terminals; run `jerry session status` and confirm you see a project ID
- **A shared authorization document on disk** — a signed letter or ticket authorizing the test target; this tutorial uses `~/auth/ENG-SPLIT-001-authorization.pdf`
- **A shared scope definition agreed before the engagement** — both operators must know the target list before starting; information isolation begins only after scope approval, not before

---

## Steps

### 1. Copy the split team template

In the **red terminal**, copy the split-team template into your engagement workspace:

```
cp skills/rainbow/templates/split-team-template.yaml \
   work/engagements/ENG-SPLIT-001/engagement-config.yaml
```

**Expected result:** The file `work/engagements/ENG-SPLIT-001/engagement-config.yaml` now exists and contains the `mode: split` field and six CHANGEME placeholders.

---

### 2. Fill in the engagement config

Open `work/engagements/ENG-SPLIT-001/engagement-config.yaml` in your editor. Replace every CHANGEME field with real values. Use the complete filled example below:

```yaml
engagement:
  id: "ENG-SPLIT-001"
  name: "Split Team Exercise — Internal Lab"
  type: "split_team"
  mode: "split"
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
    visibility: "red_only"
  blue:
    operator: "bob"
    role: "defender"
    visibility: "blue_only"

credentials:
  proxy_api_key:
    source: "keychain"
    key_name: "proxy.digitalocean.api-key"

rules_of_engagement:
  authorization: "~/auth/ENG-SPLIT-001-authorization.pdf"
  escalation_contact: "alice@example.com"
  emergency_stop: true
  data_handling: "evidence_vault_only"

split_team:
  information_barrier: true
  red_findings_path: "work/engagements/ENG-SPLIT-001/red-team/"
  blue_detections_path: "work/engagements/ENG-SPLIT-001/blue-team/"
  correlation_reveal_gate: "G5"

output:
  report_format: "markdown"
  report_template: "technical"
  retention_days: 90
```

**Expected result:** The file contains no remaining CHANGEME strings. Verify with:

```
grep -c CHANGEME work/engagements/ENG-SPLIT-001/engagement-config.yaml
```

The command prints `0`.

---

### 3. Create the engagement

In the **red terminal**, tell Jerry to start the engagement lifecycle:

```
Set up a new split team engagement using the config at
work/engagements/ENG-SPLIT-001/engagement-config.yaml
```

`rainbow-orchestrator` parses the YAML, validates the fields, records `information_barrier: true`, and writes the initial engagement state file.

**Expected result:** Jerry responds with the engagement summary and presents Gate G1. The output includes:

```
Lifecycle state: DEFINED
G1 — Scope Approval Required (RED operator)
Engagement: ENG-SPLIT-001 (split mode)
Information barrier: ACTIVE — red findings will not be visible to bob until G5
Targets: 10.0.1.100 (Lab web server — Ubuntu 22.04)
Red operator alice: approve this scope? [yes/no]
```

---

### 4. Red operator approves scope (G1 red)

Still in the **red terminal**, confirm the target IP matches the authorization document, then type:

```
yes
```

**Expected result:** Jerry records the red operator's G1 approval with username `alice` and a timestamp, then prints:

```
G1 red approved by alice.
Waiting for G1 blue approval from bob...
```

The engagement stays in `DEFINED` state until both operators approve.

---

### 5. Blue operator approves scope (G1 blue)

Switch to the **blue terminal**. Jerry presents the same G1 scope to `bob`:

```
Lifecycle state: DEFINED
G1 — Scope Approval Required (BLUE operator)
Engagement: ENG-SPLIT-001 (split mode)
Targets: 10.0.1.100 (Lab web server — Ubuntu 22.04)
Note: You will not see red team activity until the correlation gate (G5).
Blue operator bob: approve this scope? [yes/no]
```

Read the target list, confirm it matches what you agreed before the engagement, then type:

```
yes
```

**Expected result:** Jerry records the blue operator's G1 approval and immediately transitions state:

```
G1 blue approved by bob.
Both teams approved. Transitioning to PROVISIONING.
Lifecycle state: PROVISIONING
```

---

### 6. Approve infrastructure (G3)

`rainbow-orchestrator` provisions the proxy nodes and sensor, then presents Gate G3 in **both terminals**. In the **red terminal**, confirm the provisioning plan and type:

```
yes
```

**Expected result:** Infrastructure comes online and Jerry transitions to `ACTIVE` state:

```
[Provisioning] Proxy node 1/3 — nyc1 — OK
[Provisioning] Proxy node 2/3 — nyc1 — OK
[Provisioning] Proxy node 3/3 — nyc1 — OK
[Provisioning] Wazuh sensor — OK
G3 approved. Transitioning to ACTIVE.
Lifecycle state: ACTIVE
Information barrier enforced. Red findings isolated to red-team directory.
```

---

### 7. Red operator executes techniques (red terminal only)

In the **red terminal**, run the first technique. The blue terminal receives nothing from this step — the information barrier is active:

```
Use rainbow-exploit-ops to execute T1046 (Network Service Discovery)
against 10.0.1.100.
```

Gate G4 appears only in the **red terminal**:

```
G4 — Technique Approval Required
Technique: T1046 — Network Service Discovery
Target: 10.0.1.100
Barrier: findings written to red-team directory only (blue has no visibility)
Execute? [yes/no]
```

Type:

```
yes
```

**Expected result:** The technique executes. Findings are written to `work/engagements/ENG-SPLIT-001/red-team/findings/T1046-20260326.md`. The **blue terminal** receives no output. Jerry prints in the red terminal only:

```
Red: T1046 executed — 8 open ports discovered
Findings written to red-team directory (isolated from blue operator bob)
```

---

### 8. Blue operator monitors detections (blue terminal only)

In the **blue terminal**, run the detection hunt against the same period. The blue operator does not know what technique the red operator ran:

```
Use rainbow-recon-pipeline to run detection monitoring on 10.0.1.100.
```

**Expected result:** The Wazuh sensor events appear in the **blue terminal** only. Jerry writes them to `work/engagements/ENG-SPLIT-001/blue-team/detections/`:

```
Blue: Wazuh event logged — rule SYN-scan-threshold triggered (10.0.1.100)
Detection written to blue-team directory (isolated from red operator alice)
```

No technique attribution appears. Bob sees a detection event but not which specific technique triggered it.

---

### 9. Complete execution

In the **red terminal**, signal that the red execution phase is done:

```
Execution complete. Proceed to analysis.
```

**Expected result:** Jerry transitions state and begins cross-team correlation:

```
Lifecycle state: ANALYZING
Starting cross-team correlation...
Information barrier lifting at G5 (report review gate).
```

`rainbow-orchestrator` reads both the red findings directory and the blue detections directory.

---

### 10. Cross-team correlation and report review (G5)

`rainbow-orchestrator` writes the correlation report to `work/engagements/ENG-SPLIT-001/analysis/cross-team-correlation.md`. Read it in either terminal:

```
Read work/engagements/ENG-SPLIT-001/analysis/cross-team-correlation.md
```

The report shows each red technique alongside the blue detection result. This is the first moment `bob` can see what `alice` executed.

**Expected result:** The file contains a correlation table with at least one row for T1046:

```
| Technique | Red Finding | Blue Detection | Correlated | Confidence |
|-----------|-------------|----------------|------------|------------|
| T1046 | 8 ports discovered | SYN-scan-threshold | YES | HIGH |
```

Gate G5 then appears in both terminals:

```
G5 — Report Review Required
Information barrier lifted. Both teams can now see the full correlation.
Approve teardown? [yes/no]
```

Both operators type:

```
yes
```

**Expected result:** Jerry transitions state:

```
G5 approved. Transitioning to TEARDOWN.
Lifecycle state: TEARDOWN
```

---

### 11. Teardown and archive

`rainbow-orchestrator` presents Gate G6 with the full teardown list:

```
G6 — Teardown Confirmation Required
Archive: work/engagements/ENG-SPLIT-001/archive/2026-03-26T120000/
  Red team files: 6
  Blue team files: 4
  Correlation files: 2
  Total files to archive: 12
Destroy: 3 proxy nodes (DigitalOcean nyc1)
Revoke: 1 SOCKS5 credential, 1 API session token
Proceed? [yes/no]
```

Type:

```
yes
```

**Expected result:** Teardown completes and Gate G7 follows immediately:

```
[Archive] 12/12 files archived — OK
[Integrity] SHA-256 manifest written — OK
[Revoke] proxy.digitalocean.api-key session token — revoked
[Destroy] Proxy node 1/3 — destroyed
[Destroy] Proxy node 2/3 — destroyed
[Destroy] Proxy node 3/3 — destroyed

G7 — Archive Integrity Verification
12 files archived
SHA-256 manifest: work/engagements/ENG-SPLIT-001/archive/2026-03-26T120000/MANIFEST.sha256
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
Engagement ENG-SPLIT-001 complete.
```

Confirm the archive exists:

```
ls work/engagements/ENG-SPLIT-001/archive/
```

You see a timestamped directory containing all engagement artifacts and `MANIFEST.sha256`.

---

## What You Learned

You now know how to:

- Copy and fill in a split-team engagement config with `mode: split`, `information_barrier: true`, and separate `visibility` fields for each team
- Create a split engagement with `/rainbow` and confirm both operators must approve G1 before the state advances
- Observe that red findings written during `ACTIVE` stay in `red-team/findings/` and do not appear in the blue terminal until G5
- Observe that blue detections written during `ACTIVE` stay in `blue-team/detections/` and do not appear in the red terminal until G5
- Read the cross-team correlation report at the G5 gate — the first moment both operators see each other's data
- Complete teardown and confirm archive integrity across both teams' artifacts

---

## Related

- **How-To Guide:** [How to tune the information barrier for partial visibility](../howto/split-team-information-barrier.md) — Adjust what each team can see and when
- **Tutorial:** [Learn to run a single-team engagement by working through the standard lifecycle](single-team-engagement.md) — The simplest engagement mode — one operator, one team, 15 steps
- **Reference:** [Engagement Lifecycle State Machine](../../skills/rainbow/rules/engagement-lifecycle.md) — Full specification of the states, all gates, and transition conditions
- **Explanation:** [About the split-team information barrier](../explanation/split-team-information-barrier.md) — Why red and blue are isolated during ACTIVE and when the barrier lifts
