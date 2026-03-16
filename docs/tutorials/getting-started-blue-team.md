# Learn to Detect Threats by Using /blue-team

> By the end of this tutorial, you will have created a defensive assessment scope, authored a YARA rule from threat intelligence indicators, validated and executed that rule against a sample file, and run a compliance audit against an IaC directory.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (T-01 through T-08) -->
<!-- Anti-patterns avoided: TAP-01 (abstraction), TAP-02 (extended explanation), TAP-03 (offering choices) -->
<!-- Voice: Encouraging, concrete, collaborative. See diataxis-standards.md Section 5. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [What You Will Achieve](#what-you-will-achieve) | The concrete end state |
| [Prerequisites](#prerequisites) | What you need before starting |
| [Step 1: Create the Assessment Scope](#step-1-create-the-assessment-scope) | Establish boundaries with blue-lead |
| [Step 2: Author a YARA Rule from Threat Intelligence](#step-2-author-a-yara-rule-from-threat-intelligence) | Turn IOCs into a detection rule |
| [Step 3: Validate and Execute the Rule](#step-3-validate-and-execute-the-rule) | Check syntax and scan with blue-detect |
| [Step 4: Run a Compliance Audit](#step-4-run-a-compliance-audit) | Scan IaC templates with blue-comply |
| [What You Learned](#what-you-learned) | Skills you have now |
| [Related](#related) | Next steps |

---

## What You Will Achieve

By the end of this tutorial, you will have:

- An assessment scope document at `work/blue-team/engagements/BLUE-0001/scope.md`
- A YARA rule file at `work/blue-team/ioc/tutorial-malware.yar` built from real indicator types
- A YARA-X validation result confirming the rule is syntactically correct
- A Checkov compliance scan report for a Terraform directory
- A working understanding of why `blue-lead` must always run first

---

## Prerequisites

Before starting, you need:

- **Jerry framework installed** with `/blue-team` skill available (verify by running `jerry session status`)
- **An active Jerry project** with `JERRY_PROJECT` set (verify by running `jerry projects list`)
- **YARA-X installed** (`yr` command available -- install guide at `docs/howto/tool-setup-by-tier.md`)
- **Checkov installed** (`checkov` command available -- install guide at `docs/howto/tool-setup-by-tier.md`)
- **A sample file to scan** -- create one with `echo "test" > /tmp/sample.bin` for this tutorial
- **A Terraform directory to audit** -- any directory containing `.tf` files works; use your project's infrastructure directory or create a minimal one
- **No prior /blue-team experience required** -- this tutorial starts from the beginning

---

## Step 1: Create the Assessment Scope

Every /blue-team operation requires an active scope document. `blue-lead` creates it and no other agent can run without it.

Send this request in your Jerry session:

```
Use blue-lead to create an assessment scope for a defensive security assessment.
Engagement ID: BLUE-0001
Assessment objectives: threat detection rule validation, IaC compliance audit
Assets in scope: /tmp/sample.bin, terraform/
Output: work/blue-team/engagements/BLUE-0001/scope.md
```

**Expected result:** A file is created at `work/blue-team/engagements/BLUE-0001/scope.md`. The agent confirms:

```
Assessment scope created: work/blue-team/engagements/BLUE-0001/scope.md
Engagement ID: BLUE-0001
Status: ACTIVE
Assets in scope:
  - /tmp/sample.bin (threat detection target)
  - terraform/ (compliance audit target)

All blue-team agents are now authorized for this engagement.
Zone 1 (Analysis) — no active response or system modification permitted.
```

You now have an active engagement. Every agent invoked in the following steps references this scope.

---

## Step 2: Author a YARA Rule from Threat Intelligence

Give `blue-ioc` a set of threat indicators and ask it to produce a YARA rule. In a real assessment these indicators would come from a threat intelligence report; for this tutorial, use the indicators provided below.

Send this request:

```
Use blue-ioc to author a YARA rule for engagement BLUE-0001
based on the following indicators from a hypothetical threat report:

Strings:
  - "MaliciousLoader"
  - "C2_BEACON"
  - "cmd.exe /c powershell -enc"

File size: less than 500KB
Output rule: work/blue-team/ioc/tutorial-malware.yar
Rule name: TutorialMalware_Loader
```

**Expected result:** The file `work/blue-team/ioc/tutorial-malware.yar` is created. The agent shows you the rule content:

```yara
rule TutorialMalware_Loader {
    meta:
        description = "Detects tutorial malware loader based on IOC report"
        date        = "2026-03-16"
        engagement  = "BLUE-0001"
    strings:
        $s1 = "MaliciousLoader" ascii wide
        $s2 = "C2_BEACON" ascii wide
        $s3 = "cmd.exe /c powershell -enc" ascii wide
    condition:
        filesize < 500KB and
        2 of ($s*)
}
```

The agent also confirms:

```
Rule written: work/blue-team/ioc/tutorial-malware.yar
Indicators encoded: 3 strings
Condition: filesize < 500KB AND 2 of 3 strings match
Next step: validate syntax with blue-detect before scanning
```

---

## Step 3: Validate and Execute the Rule

Ask `blue-detect` to first check the rule's syntax using YARA-X, then scan your sample file.

Send this request:

```
Use blue-detect to validate the YARA rule at work/blue-team/ioc/tutorial-malware.yar
and then scan /tmp/sample.bin.
Engagement: BLUE-0001
Output: work/blue-team/detection/tutorial-scan-results.md
```

The agent runs two commands:

```bash
yr check work/blue-team/ioc/tutorial-malware.yar

yr scan work/blue-team/ioc/tutorial-malware.yar /tmp/sample.bin
```

**Expected result:** The agent reports both steps:

```
Syntax validation: PASS
  yr check work/blue-team/ioc/tutorial-malware.yar
  Result: 1 rule — no syntax errors

Scan complete: /tmp/sample.bin
  Matches: 0
  Result: CLEAN — no rule matches detected

Report: work/blue-team/detection/tutorial-scan-results.md
Zone: 1 (Analysis) — read-only scan of provided artifact
```

A CLEAN result is expected here because `/tmp/sample.bin` contains only the text "test". The tutorial goal is confirming that the rule validates without syntax errors and the scan pipeline runs end-to-end. When you scan real malware samples, the match output will list matched strings and offsets.

---

## Step 4: Run a Compliance Audit

Ask `blue-comply` to scan your Terraform directory with Checkov against the CIS AWS Foundations benchmark.

Send this request:

```
Use blue-comply to run a Checkov compliance scan on the terraform/ directory.
Framework: terraform
Benchmark: CIS
Engagement: BLUE-0001
Output: work/compliance/BLUE-0001/checkov-results.md
```

If you do not have a `terraform/` directory, create a minimal one first:

```bash
mkdir -p terraform
cat > terraform/main.tf << 'EOF'
resource "aws_s3_bucket" "example" {
  bucket = "my-tutorial-bucket"
}
EOF
```

The agent runs:

```bash
checkov -d terraform/ --framework terraform --output json \
  --output-file work/compliance/BLUE-0001/checkov-results.json
```

**Expected result:** The agent presents a findings summary:

```
Checkov scan complete
  Framework:  terraform
  Directory:  terraform/
  Passed:     0
  Failed:     8
  Skipped:    0

Top findings (FAILED):
  CKV_AWS_18: S3 bucket does not have access logging enabled
  CKV_AWS_145: S3 bucket does not use KMS encryption
  CKV2_AWS_62: S3 bucket does not have event notifications configured
  ... (5 more)

Report: work/compliance/BLUE-0001/checkov-results.md
Zone: 1 (Analysis) — read-only IaC scan, no remediation applied
```

A minimal bucket without logging or encryption is expected to fail multiple checks. The findings show the check ID, a description, the file name, and the line number so you can locate and remediate each issue.

---

## What You Learned

You now know how to:

- Create an assessment scope using `blue-lead`, which is required before any other /blue-team agent can operate
- Author a YARA rule from structured threat indicators using `blue-ioc`, producing a `.yar` file ready for scanning
- Validate YARA rule syntax with `yr check` and run a file scan with `yr scan` using `blue-detect`
- Run a Checkov IaC compliance scan against a Terraform directory using `blue-comply`

---

## Related

- **How-To Guide:** [How to set up /blue-team tools by tier](../howto/tool-setup-by-tier.md) -- Install YARA-X, Checkov, and other /blue-team tools
- **Reference:** [Blue Team SKILL.md](../../skills/blue-team/SKILL.md) -- Full agent registry, Zone 1 enforcement, routing decision tree, and tool inventory
- **Explanation:** [About Zone 1 enforcement](../../skills/blue-team/SKILL.md#zone-1-universal-enforcement) -- Why all 12 agents operate read-only and what that means for your workflow
