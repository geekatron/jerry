# BUG-006: red-team Output Path Audit Detail

> Persisted audit findings. Referenced by BUG-006 worktracker entity.
> Verification command: `grep -rn 'skills/red-team/output' skills/red-team/SKILL.md skills/red-team/agents/*.governance.yaml skills/red-team/composition/*.agent.yaml skills/red-team/templates/*.md`
> Result: 25 files (verified 2026-03-31)

---

## SKILL.md — 1 file, 20 references

| Line | Content |
|------|---------|
| 106 | `skills/red-team/output/{engagement-id}/red-lead-{topic-slug}.md` |
| 107 | `skills/red-team/output/{engagement-id}/red-recon-{topic-slug}.md` |
| 108 | `skills/red-team/output/{engagement-id}/red-vuln-{topic-slug}.md` |
| 109 | `skills/red-team/output/{engagement-id}/red-exploit-{topic-slug}.md` |
| 110 | `skills/red-team/output/{engagement-id}/red-privesc-{topic-slug}.md` |
| 111 | `skills/red-team/output/{engagement-id}/red-lateral-{topic-slug}.md` |
| 112 | `skills/red-team/output/{engagement-id}/red-persist-{topic-slug}.md` |
| 113 | `skills/red-team/output/{engagement-id}/red-exfil-{topic-slug}.md` |
| 114 | `skills/red-team/output/{engagement-id}/red-reporter-{topic-slug}.md` |
| 115 | `skills/red-team/output/{engagement-id}/red-infra-{topic-slug}.md` |
| 116 | `skills/red-team/output/{engagement-id}/red-social-{topic-slug}.md` |
| 188 | `skills/red-team/output/RED-0001/evidence/` (storage path) |
| 274 | `skills/red-team/output/RED-0001/red-lead-scope.md` (scope doc) |
| 521 | `skills/red-team/output/{engagement-id}/{agent-name}-{topic-slug}.md` (convention) |
| 525 | `skills/red-team/output/RED-0001/red-lead-scope.md` |
| 526 | `skills/red-team/output/RED-0001/red-recon-network-enumeration.md` |
| 527 | `skills/red-team/output/RED-0001/red-vuln-cve-analysis.md` |
| 528 | `skills/red-team/output/RED-0001/red-reporter-final-report.md` |
| 535 | `skills/red-team/output/{engagement-id}/evidence/` (evidence dir) |

## Agent Governance YAML — 11 files

| File | Line | `output.location` Value |
|------|------|-------------------------|
| `red-exfil.governance.yaml` | 32 | `skills/red-team/output/{engagement-id}/red-exfil-{topic-slug}.md` |
| `red-exploit.governance.yaml` | 35 | `skills/red-team/output/{engagement-id}/red-exploit-{topic-slug}.md` |
| `red-infra.governance.yaml` | 35 | `skills/red-team/output/{engagement-id}/red-infra-{topic-slug}.md` |
| `red-lateral.governance.yaml` | 31 | `skills/red-team/output/{engagement-id}/red-lateral-{topic-slug}.md` |
| `red-lead.governance.yaml` | 33 | `skills/red-team/output/{engagement-id}/red-lead-{topic-slug}.md` |
| `red-persist.governance.yaml` | 32 | `skills/red-team/output/{engagement-id}/red-persist-{topic-slug}.md` |
| `red-privesc.governance.yaml` | 31 | `skills/red-team/output/{engagement-id}/red-privesc-{topic-slug}.md` |
| `red-recon.governance.yaml` | 31 | `skills/red-team/output/{engagement-id}/red-recon-{topic-slug}.md` |
| `red-reporter.governance.yaml` | 33 | `skills/red-team/output/{engagement-id}/red-reporter-{topic-slug}.md` |
| `red-social.governance.yaml` | 32 | `skills/red-team/output/{engagement-id}/red-social-{topic-slug}.md` |
| `red-vuln.governance.yaml` | 33 | `skills/red-team/output/{engagement-id}/red-vuln-{topic-slug}.md` |

## Agent Composition YAML — 11 files

| File | Line | `output.location` Value |
|------|------|-------------------------|
| `red-exfil.agent.yaml` | 53 | `skills/red-team/output/{engagement-id}/red-exfil-{topic-slug}.md` |
| `red-exploit.agent.yaml` | 56 | `skills/red-team/output/{engagement-id}/red-exploit-{topic-slug}.md` |
| `red-infra.agent.yaml` | 56 | `skills/red-team/output/{engagement-id}/red-infra-{topic-slug}.md` |
| `red-lateral.agent.yaml` | 52 | `skills/red-team/output/{engagement-id}/red-lateral-{topic-slug}.md` |
| `red-lead.agent.yaml` | 54 | `skills/red-team/output/{engagement-id}/red-lead-{topic-slug}.md` |
| `red-persist.agent.yaml` | 53 | `skills/red-team/output/{engagement-id}/red-persist-{topic-slug}.md` |
| `red-privesc.agent.yaml` | 52 | `skills/red-team/output/{engagement-id}/red-privesc-{topic-slug}.md` |
| `red-recon.agent.yaml` | 52 | `skills/red-team/output/{engagement-id}/red-recon-{topic-slug}.md` |
| `red-reporter.agent.yaml` | 54 | `skills/red-team/output/{engagement-id}/red-reporter-{topic-slug}.md` |
| `red-social.agent.yaml` | 53 | `skills/red-team/output/{engagement-id}/red-social-{topic-slug}.md` |
| `red-vuln.agent.yaml` | 54 | `skills/red-team/output/{engagement-id}/red-vuln-{topic-slug}.md` |

## Templates — 2 files

| File | Line | Content |
|------|------|---------|
| `engagement-playbook.md` | 81 | `Scope document persisted to skills/red-team/output/{engagement-id}/` |
| `pentest-engagement.md` | 151 | `storage: "skills/red-team/output/RED-{NNNN}/evidence/"` |

## Sum Check

| Category | Files |
|----------|-------|
| SKILL.md | 1 |
| Governance YAML | 11 |
| Composition YAML | 11 |
| Templates | 2 |
| **Total** | **25** |
