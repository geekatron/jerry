# BUG-006: eng-team Output Path Audit Detail

> Persisted audit findings. Referenced by BUG-006 worktracker entity.
> Verification command: `grep -rn 'skills/eng-team/output' skills/eng-team/SKILL.md skills/eng-team/agents/*.governance.yaml skills/eng-team/composition/*.agent.yaml skills/eng-team/templates/*.md`
> Result: 22 files (verified 2026-03-31)

---

## SKILL.md — 1 file, 11 references

| Line | Content |
|------|---------|
| 119 | `skills/eng-team/output/{engagement-id}/eng-architect-{topic-slug}.md` |
| 120 | `skills/eng-team/output/{engagement-id}/eng-lead-{topic-slug}.md` |
| 121 | `skills/eng-team/output/{engagement-id}/eng-backend-{topic-slug}.md` |
| 122 | `skills/eng-team/output/{engagement-id}/eng-frontend-{topic-slug}.md` |
| 123 | `skills/eng-team/output/{engagement-id}/eng-infra-{topic-slug}.md` |
| 124 | `skills/eng-team/output/{engagement-id}/eng-devsecops-{topic-slug}.md` |
| 125 | `skills/eng-team/output/{engagement-id}/eng-qa-{topic-slug}.md` |
| 126 | `skills/eng-team/output/{engagement-id}/eng-security-{topic-slug}.md` |
| 127 | `skills/eng-team/output/{engagement-id}/eng-reviewer-{topic-slug}.md` |
| 128 | `skills/eng-team/output/{engagement-id}/eng-incident-{topic-slug}.md` |
| 261 | `skills/eng-team/output/` (directory structure diagram) |

## Agent Governance YAML — 10 files

| File | Line | `output.location` Value |
|------|------|-------------------------|
| `eng-architect.governance.yaml` | 31 | `skills/eng-team/output/{engagement-id}/eng-architect-{topic-slug}.md` |
| `eng-backend.governance.yaml` | 32 | `skills/eng-team/output/{engagement-id}/eng-backend-{topic-slug}.md` |
| `eng-devsecops.governance.yaml` | 32 | `skills/eng-team/output/{engagement-id}/eng-devsecops-{topic-slug}.md` |
| `eng-frontend.governance.yaml` | 31 | `skills/eng-team/output/{engagement-id}/eng-frontend-{topic-slug}.md` |
| `eng-incident.governance.yaml` | 35 | `skills/eng-team/output/{engagement-id}/eng-incident-{topic-slug}.md` |
| `eng-infra.governance.yaml` | 33 | `skills/eng-team/output/{engagement-id}/eng-infra-{topic-slug}.md` |
| `eng-lead.governance.yaml` | 31 | `skills/eng-team/output/{engagement-id}/eng-lead-{topic-slug}.md` |
| `eng-qa.governance.yaml` | 31 | `skills/eng-team/output/{engagement-id}/eng-qa-{topic-slug}.md` |
| `eng-reviewer.governance.yaml` | 31 | `skills/eng-team/output/{engagement-id}/eng-reviewer-{topic-slug}.md` |
| `eng-security.governance.yaml` | 31 | `skills/eng-team/output/{engagement-id}/eng-security-{topic-slug}.md` |

## Agent Composition YAML — 10 files

| File | Line | `output.location` Value |
|------|------|-------------------------|
| `eng-architect.agent.yaml` | 53 | `skills/eng-team/output/{engagement-id}/eng-architect-{topic-slug}.md` |
| `eng-backend.agent.yaml` | 53 | `skills/eng-team/output/{engagement-id}/eng-backend-{topic-slug}.md` |
| `eng-devsecops.agent.yaml` | 54 | `skills/eng-team/output/{engagement-id}/eng-devsecops-{topic-slug}.md` |
| `eng-frontend.agent.yaml` | 52 | `skills/eng-team/output/{engagement-id}/eng-frontend-{topic-slug}.md` |
| `eng-incident.agent.yaml` | 57 | `skills/eng-team/output/{engagement-id}/eng-incident-{topic-slug}.md` |
| `eng-infra.agent.yaml` | 54 | `skills/eng-team/output/{engagement-id}/eng-infra-{topic-slug}.md` |
| `eng-lead.agent.yaml` | 53 | `skills/eng-team/output/{engagement-id}/eng-lead-{topic-slug}.md` |
| `eng-qa.agent.yaml` | 52 | `skills/eng-team/output/{engagement-id}/eng-qa-{topic-slug}.md` |
| `eng-reviewer.agent.yaml` | 53 | `skills/eng-team/output/{engagement-id}/eng-reviewer-{topic-slug}.md` |
| `eng-security.agent.yaml` | 52 | `skills/eng-team/output/{engagement-id}/eng-security-{topic-slug}.md` |

## Templates — 1 file

| File | Line | Content |
|------|------|---------|
| `engagement-playbook.md` | 189 | `Create output directory: skills/eng-team/output/{engagement-id}/` |

## Sum Check

| Category | Files |
|----------|-------|
| SKILL.md | 1 |
| Governance YAML | 10 |
| Composition YAML | 10 |
| Templates | 1 |
| **Total** | **22** |
