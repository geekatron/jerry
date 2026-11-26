---
name: eng-team
description: >-
  Secure software engineering methodology for building security-hardened systems. Use when the user
  asks to design, implement, review, test, harden, or operate software with security in mind — threat
  modeling (STRIDE/DREAD/PASTA), secure architecture, secure backend/frontend/infra implementation,
  DevSecOps pipelines (SAST/DAST), security QA and fuzzing, manual secure code review (CWE/OWASP ASVS),
  release gating, and incident response. Routes to 10 specialized roles across an 8-step secure-SDLC
  workflow and integrates NIST SSDF, Microsoft SDL, OWASP ASVS, SLSA, and CIS guidance. Do NOT use for
  offensive security or penetration testing (that is a red-team task), for general non-security code
  review or debugging, or for pure structural architecture with no security requirement.
---

# Eng-Team — Secure Engineering Skill (Codex port)

> **Codex port version:** `codex-1.0.0` — versioned independently of the Jerry source skill.
> **Forked from:** Jerry `/eng-team` v1.0.0 (divergence point). This Codex port is a separate running
> version: it is **not** kept in lockstep with the Jerry original and may intentionally diverge. Bump
> this `codex-x.y.z` version on its own cadence when this port changes; do not assume parity with
> `skills/eng-team/`.

> Ported from the Jerry Framework `/eng-team` Claude skill (`skills/eng-team/SKILL.md`).
> Codex has a single execution context and no sub-agent spawning, so the 10 "agents" are represented
> here as **roles** you adopt one at a time by loading the matching file in `references/`. The
> methodology, standards, and per-role prompts are identical to the Claude original **as of the
> divergence point above**.

## What this skill does

Provides a structured secure-software-engineering method through 10 specialized roles. Each role
produces a persistent artifact, enforces security standards at its phase, and hands off to the next.
Adopt one role at a time: read its `references/<role>.md` file, then act as that role for the task.

## How to use it in Codex

1. **Pick the role** that matches the task using the routing table below (or run the full 8-step
   workflow for an end-to-end build).
2. **Load the role prompt:** open `references/<role>.md` and follow it as your operating instructions
   for that step.
3. **Produce the artifact** at L0/L1/L2 levels (see Output) and persist it to a file — do not leave it
   in chat only.
4. **Hand off:** pass the artifact path to the next role; later roles read prior artifacts as input.

Roles can be invoked individually (e.g. "threat-model this service" → `eng-architect`) or chained as
the full workflow. Only adopt one role at a time — Codex must not try to spawn parallel agents.

## Roles and routing

| Role | When to use it | Reference file |
|------|----------------|----------------|
| `eng-architect` | design, architecture, threat model, STRIDE, DREAD, ADR, trust boundary | `references/eng-architect.md` |
| `eng-lead` | implementation plan, coding standards, dependency governance, SAMM | `references/eng-lead.md` |
| `eng-backend` | server-side code, API, auth logic, database, input validation, OWASP Top 10 | `references/eng-backend.md` |
| `eng-frontend` | client-side code, XSS, CSP, CORS, output encoding | `references/eng-frontend.md` |
| `eng-infra` | IaC, container hardening, secrets, SBOM, SLSA, supply chain | `references/eng-infra.md` |
| `eng-devsecops` | CI/CD security, SAST, DAST, secrets/container/dependency scanning | `references/eng-devsecops.md` |
| `eng-qa` | security tests, fuzzing, property-based testing, coverage | `references/eng-qa.md` |
| `eng-security` | manual secure code review, CWE Top 25, OWASP ASVS verification | `references/eng-security.md` |
| `eng-reviewer` | final release gate, standards compliance, quality review | `references/eng-reviewer.md` |
| `eng-incident` | incident response runbooks, monitoring, post-deployment, remediation | `references/eng-incident.md` |

## 8-step secure-SDLC workflow

Run sequentially; each step consumes the prior artifacts. Step 3 covers three roles that, in Codex,
are adopted one after another (not in parallel).

```
1. eng-architect   Design + threat model (STRIDE/DREAD; deepen by criticality)
2. eng-lead        Implementation plan + security standards mapping
3. eng-backend / eng-frontend / eng-infra   Secure implementation
4. eng-devsecops   Automated security scans (SAST/DAST/secrets/deps/containers)
5. eng-qa          Security testing + fuzzing + coverage
6. eng-security    Manual secure code review (CWE Top 25, OWASP ASVS)
7. eng-reviewer    Final gate — standards + coverage compliance
8. eng-incident    Post-deployment IR plans + runbooks (runs independently)
```

State handoff: each role's artifact is the input for the next (`architect_output` → `lead_output` →
implementation outputs → `devsecops_output` → `qa_output` → `security_output` → `reviewer_output`;
`incident_output` is produced post-deployment).

## Output (every role)

Persist artifacts to files (do not leave them only in chat). Default location: the path the user
specifies, otherwise `./engagements/{engagement-id}/<role>-{topic-slug}.md`. If `engagement-id` is
unknown, ask before writing. Each artifact has three levels:

- **L0 — Executive summary:** what this means for the project, in plain language.
- **L1 — Technical detail:** specifics, code/config examples, tables, implementation guidance.
- **L2 — Strategic implications:** trade-offs, long-term risk, security-posture alignment.

## Criticality-based rigor

Scale threat-modeling and review depth to how risky/irreversible the change is:

| Level | Context | Threat modeling depth |
|-------|---------|-----------------------|
| C1 Routine | minor config/docs | STRIDE only |
| C2 Standard | feature/endpoint with auth | STRIDE + DREAD scoring |
| C3 Significant | architecture/IaC change | STRIDE + DREAD + Attack Trees |
| C4 Critical | security/auth architecture | + PASTA stages 4-7 |
| PII involved | any level | add LINDDUN |

`eng-reviewer` is the mandatory final gate for C2+ work. Always self-review a deliverable before
presenting it, and strengthen an argument (steelman) before critiquing it.

## Standards integrated

NIST SP 800-218 (SSDF) · Microsoft SDL · OWASP ASVS v5.0 · OWASP Top 10 · CWE Top 25 · Google SLSA v1.0
· OWASP SAMM v2.0 · CIS Benchmarks · NIST CSF 2.0 · NIST SP 800-61r3 (incident response).

## Self-containment

This skill is standalone — everything it needs is inside `.agents/skills/eng-team/`. The `eng-reviewer`
role mentions running an adversarial quality review for C2+ work; that is an **optional** enhancement,
not a dependency. `eng-reviewer` performs its own quality scoring inline. If the separate `adversary`
skill happens to be installed you may use it for deeper review, but eng-team works fully without it.

## When NOT to use this skill

- **Offensive security / penetration testing** → use a red-team methodology, not this defensive skill.
- **General code review or debugging with no security focus** → use a general engineering approach.
- **Pure structural architecture with no security requirement** → security governance here is overhead.

## Provenance

Source: Jerry Framework `/eng-team` skill (`skills/eng-team/SKILL.md`) and agent definitions in
`skills/eng-team/agents/*.md`. Architecture basis: ADR-PROJ010-001 (agent team architecture),
ADR-PROJ010-002 (routing), ADR-PROJ010-003 (LLM portability).
