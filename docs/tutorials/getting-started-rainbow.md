# Learn to Run a Security Assessment by Using /rainbow

> By the end of this tutorial, you will have created an engagement scope document, generated a software bill of materials with a vulnerability report, run a subdomain reconnaissance pipeline against an authorized target, and reviewed findings organized by security zone.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (T-01 through T-08) -->
<!-- Anti-patterns avoided: TAP-01 (abstraction), TAP-02 (extended explanation), TAP-03 (offering choices) -->
<!-- Voice: Encouraging, concrete, collaborative. See diataxis-standards.md Section 5. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [What You Will Achieve](#what-you-will-achieve) | The concrete end state |
| [Prerequisites](#prerequisites) | What you need before starting |
| [Step 1: Create the Engagement Scope](#step-1-create-the-engagement-scope) | Set the authorized boundaries |
| [Step 2: Generate an SBOM and Scan for Vulnerabilities](#step-2-generate-an-sbom-and-scan-for-vulnerabilities) | Run supply chain scanning |
| [Step 3: Run the Reconnaissance Pipeline](#step-3-run-the-reconnaissance-pipeline) | Enumerate subdomains and probe live hosts |
| [Step 4: Review Findings and Understand Security Zones](#step-4-review-findings-and-understand-security-zones) | Understand what was found and where |
| [What You Learned](#what-you-learned) | Skills you have now |
| [Related](#related) | Next steps |

---

## What You Will Achieve

By the end of this tutorial, you will have:

- A validated engagement scope document at `work/engagements/RBW-0001/SCOPE.md`
- A CycloneDX SBOM and a Grype vulnerability report for a container image
- A subdomain enumeration and HTTP probe results from `rainbow-recon-pipeline`
- A working understanding of Zone 1, Zone 2, and Zone 3 and why each step operated in the zone it did

---

## Prerequisites

Before starting, you need:

- **Jerry framework installed** with `/rainbow` skill available (verify by running `jerry session status`)
- **An active Jerry project** with `JERRY_PROJECT` set (verify by running `jerry projects list`)
- **Syft, Grype, Subfinder, and httpx installed** on your local machine or in your container environment -- install guides are at `docs/howto/tool-setup-by-tier.md`
- **An authorized test target**: a container image you own for supply chain scanning, and a domain name for which you hold written authorization to perform active reconnaissance
- **No prior /rainbow experience required** -- this tutorial starts from the beginning

---

## Step 1: Create the Engagement Scope

Tell `rainbow-orchestrator` you want to start a new engagement. The orchestrator will create a SCOPE.md file populated with your authorization boundaries.

Send the following request in your Jerry session:

```
Use rainbow-orchestrator to create an engagement scope for a security assessment.
Engagement ID: RBW-0001
Authorized targets: [your-domain.example.com]
Technique allowlist: [T1595, T1590]
Time window: today through 7 days from now
Escalation authority: [your name]
Output: work/engagements/RBW-0001/SCOPE.md
```

Replace `your-domain.example.com` with the domain you are authorized to test and `[your name]` with your name.

**Expected result:** A file is created at `work/engagements/RBW-0001/SCOPE.md`. The orchestrator confirms the scope document is complete and shows you the `authorized_targets` and `time_window` fields. You will see a message like:

```
Scope document created: work/engagements/RBW-0001/SCOPE.md
Status: SCOPED — awaiting operator approval
Required next action: add operator_approval field to proceed
```

Open `work/engagements/RBW-0001/SCOPE.md` and add your approval at the bottom:

```yaml
operator_approval:
  authorized_by: "Your Name"
  date: "2026-03-16"
  confirmation: "I confirm authorization for this engagement."
```

After saving, the scope status transitions to `AUTHORIZED` and Zone 2 operations are unlocked.

---

## Step 2: Generate an SBOM and Scan for Vulnerabilities

Ask `rainbow-sc-scanner` to generate a bill of materials for a container image you own, then scan it for known vulnerabilities. This is a Zone 1 operation -- it requires no engagement scope.

Send this request:

```
Use rainbow-sc-scanner to generate a CycloneDX SBOM for nginx:1.25-alpine
and then scan it with Grype for vulnerabilities.
Output SBOM: work/engagements/RBW-0001/supply-chain/nginx-sbom.json
Output vulnerabilities: work/engagements/RBW-0001/supply-chain/nginx-vulns.json
```

The agent runs two commands in sequence:

```bash
syft scan nginx:1.25-alpine -o cyclonedx-json=work/engagements/RBW-0001/supply-chain/nginx-sbom.json

grype sbom:work/engagements/RBW-0001/supply-chain/nginx-sbom.json --output json > work/engagements/RBW-0001/supply-chain/nginx-vulns.json
```

**Expected result:** Two files appear under `work/engagements/RBW-0001/supply-chain/`. The agent presents a summary like:

```
SBOM generated: 142 packages catalogued
Vulnerability scan complete:
  CRITICAL: 0
  HIGH:     3
  MEDIUM:   11
  LOW:      24
Report: work/engagements/RBW-0001/supply-chain/nginx-vulns.json
Zone: 1 (Analysis) — no engagement scope required
Credential filter: PASS — no credentials detected in output
```

The HIGH and MEDIUM findings name the affected package, the CVE identifier, and the fixed version. You do not need to take any action on them now -- reviewing findings is covered in Step 4.

---

## Step 3: Run the Reconnaissance Pipeline

Ask `rainbow-recon-pipeline` to enumerate subdomains for your authorized domain and probe the discovered hosts for live HTTP services. This is a Zone 2 operation and requires the engagement scope from Step 1 to be in `AUTHORIZED` state.

Send this request:

```
Use rainbow-recon-pipeline to run subdomain enumeration and HTTP probing
against your-domain.example.com under engagement RBW-0001.
Output subdomains: work/engagements/RBW-0001/recon/subdomains.json
Output live hosts: work/engagements/RBW-0001/recon/live-hosts.json
```

Replace `your-domain.example.com` with your authorized domain.

The agent first validates the engagement scope, then runs the pipeline:

```bash
subfinder -d your-domain.example.com -oJ -o work/engagements/RBW-0001/recon/subdomains.json

httpx -l work/engagements/RBW-0001/recon/subdomains.json -json \
  -o work/engagements/RBW-0001/recon/live-hosts.json
```

**Expected result:** The agent reports scope validation passing and then shows a pipeline summary:

```
Scope validation: PASS
  Target: your-domain.example.com — authorized
  Time window: CURRENT
  Technique: T1595 — on allowlist

Subfinder complete: 14 subdomains discovered
httpx complete: 8 live HTTP services found

Output:
  work/engagements/RBW-0001/recon/subdomains.json
  work/engagements/RBW-0001/recon/live-hosts.json

Zone: 2 (Active Reconnaissance) — engagement scope validated
Credential filter: PASS — no credentials detected in output
Audit log: work/engagements/RBW-0001/audit/zone-2/recon-pipeline.log
```

If you see `Scope validation: FAIL`, the most common cause is that the `operator_approval` field is missing from SCOPE.md. Return to Step 1 and verify you saved the approval block.

---

## Step 4: Review Findings and Understand Security Zones

Ask `rainbow-orchestrator` to summarize all findings produced during this engagement.

Send this request:

```
Summarize findings for engagement RBW-0001.
```

The orchestrator reads the artifacts from Steps 2 and 3 and produces a structured summary:

```
Engagement RBW-0001 — Finding Summary
======================================

Zone 1 (Supply Chain — nginx:1.25-alpine)
  HIGH:   3 findings (CVE references in nginx-vulns.json)
  MEDIUM: 11 findings
  LOW:    24 findings

Zone 2 (Reconnaissance — your-domain.example.com)
  Subdomains discovered: 14
  Live HTTP services:    8
  Technologies detected: nginx/1.25, Express 4.x, React 18

Zone 3 operations: none conducted

Next steps:
  - Remediate HIGH findings before production promotion
  - Review live services for unexpected exposure
  - Conduct Nuclei detection scan (Zone 2) to probe live services for known CVEs
```

You can see that supply chain scanning ran in Zone 1 (no authorization required), reconnaissance ran in Zone 2 (engagement scope required), and no Zone 3 exploitation was attempted (which would require per-operation human approval for every individual operation).

**Expected result:** You have a summary with findings from both sub-skills, organized by zone. All output files exist under `work/engagements/RBW-0001/`.

---

## What You Learned

You now know how to:

- Create a validated engagement scope document using `rainbow-orchestrator`, which unlocks Zone 2 and Zone 3 operations
- Generate a CycloneDX SBOM and vulnerability report for a container image using `rainbow-sc-scanner` in Zone 1
- Run a subdomain enumeration and HTTP probing pipeline using `rainbow-recon-pipeline` in Zone 2
- Read the zone label in every agent response and understand what authorization each zone requires

---

## Related

- **How-To Guide:** [How to set up /rainbow tools by tier](../howto/tool-setup-by-tier.md) -- Install Syft, Grype, Subfinder, httpx, and other /rainbow tools
- **Reference:** [Rainbow SKILL.md](../../skills/rainbow/SKILL.md) -- Full agent registry, zone enforcement rules, and routing decision tree
- **Reference:** [Engagement Lifecycle](../../skills/rainbow/rules/engagement-lifecycle.md) -- All five lifecycle phases and phase gate requirements
- **Explanation:** [About the three-zone security model](../../skills/rainbow/SKILL.md#security-zone-overview) -- Why zones exist and how they enforce authorization
