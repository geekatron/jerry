# Framework Registration Report -- PROJ-010 Cyber Ops Skills

> **Feature:** FEAT-054 Framework Registration
> **Project:** PROJ-010 Cyber Ops | EPIC-006 Documentation & Guides
> **Date:** 2026-02-22
> **Status:** Complete
> **Governing Rule:** H-26 (Register in CLAUDE.md + AGENTS.md + mandatory-skill-usage.md if proactive)
> **SSOT References:** `.context/rules/skill-standards.md` (H-25, H-26), `.context/rules/quality-enforcement.md`, `AGENTS.md`, `CLAUDE.md`, `.context/rules/mandatory-skill-usage.md`

## Document Sections

| Section | Purpose |
|---------|---------|
| [Registration Requirements](#registration-requirements) | H-26 checklist and scope of changes |
| [AGENTS.md Registration Block](#agentsmd-registration-block) | Ready-to-insert agent registry content for 21 agents |
| [CLAUDE.md Registration Block](#claudemd-registration-block) | Ready-to-insert Quick Reference skill table rows |
| [mandatory-skill-usage.md Registration Block](#mandatory-skill-usagemd-registration-block) | Ready-to-insert trigger map and H-22 rule entries |
| [MCP Tool Access Registration Block](#mcp-tool-access-registration-block) | Ready-to-insert Context7 agent matrix entries |
| [Verification Checklist](#verification-checklist) | H-25 and H-26 compliance verification for both skills |

---

## Registration Requirements

### Scope

PROJ-010 Cyber Ops has produced two skills containing 21 agents total:

| Skill | Agent Count | Agents | Skill File |
|-------|-------------|--------|------------|
| `/eng-team` | 10 | eng-architect, eng-lead, eng-backend, eng-frontend, eng-infra, eng-devsecops, eng-qa, eng-security, eng-reviewer, eng-incident | `skills/eng-team/SKILL.md` |
| `/red-team` | 11 | red-lead, red-recon, red-vuln, red-exploit, red-privesc, red-lateral, red-persist, red-exfil, red-reporter, red-infra, red-social | `skills/red-team/SKILL.md` |

### H-26 Registration Targets

Per H-26, new skills MUST be registered in three locations:

| Target File | Registration Type | Required |
|-------------|-------------------|----------|
| `AGENTS.md` | Agent registry entries for all 21 agents, navigation table update, agent summary update, MCP tool access update | Yes (H-26) |
| `CLAUDE.md` | Quick Reference Skills table -- 2 new rows | Yes (H-26) |
| `.context/rules/mandatory-skill-usage.md` | Trigger Map entries + H-22 rule update for proactive invocation | Yes (H-26, both skills require proactive invocation per H-22) |

### Auto-Escalation Note

Modifying `.context/rules/mandatory-skill-usage.md` triggers AE-002 (touches `.context/rules/`), which enforces auto-C3 minimum criticality. The `CLAUDE.md` and `AGENTS.md` modifications are standard registration operations and do not trigger auto-escalation.

---

## AGENTS.md Registration Block

### Navigation Table Update

Insert two rows into the existing `## Document Sections` navigation table, before the `[MCP Tool Access]` row:

```markdown
| [Eng-Team Skill Agents](#eng-team-skill-agents) | eng-* agents (10 total) |
| [Red-Team Skill Agents](#red-team-skill-agents) | red-* agents (11 total) |
```

### Agent Summary Update

Replace the existing `## Agent Summary` table with the following (adds 2 new rows and updates the total):

```markdown
## Agent Summary

| Category | Count | Scope |
|----------|-------|-------|
| Problem-Solving Agents | 9 | `/problem-solving` skill |
| NASA SE Agents | 10 | `/nasa-se` skill |
| Orchestration Agents | 3 | `/orchestration` skill |
| Adversary Agents | 3 | `/adversary` skill |
| Worktracker Agents | 3 | `/worktracker` skill |
| Transcript Agents | 5 | `/transcript` skill |
| Framework Voice Agents | 3 | `/saucer-boy-framework-voice` skill |
| Session Voice Agents | 1 | `/saucer-boy` skill |
| Eng-Team Agents | 10 | `/eng-team` skill |
| Red-Team Agents | 11 | `/red-team` skill |
| **Total** | **58** | |

> **Verification:** Agent counts verified against filesystem scan (`skills/*/agents/*.md`).
> Per-skill sum: 9 + 10 + 3 + 3 + 3 + 5 + 3 + 1 + 10 + 11 = 58 invokable agents.
> Last verified: 2026-02-22.
```

### Eng-Team Skill Agents Section

Insert after the `## Session Voice Skill Agents` section and before the `## MCP Tool Access` section:

```markdown
## Eng-Team Skill Agents

These agents implement secure software engineering methodology through the `/eng-team` skill, covering the full SDLC with security hardening at every phase. Follows an 8-step sequential phase-gate workflow with NIST SSDF governance, Microsoft SDL phases, OWASP ASVS verification, SLSA supply chain integrity, and DevSecOps automation patterns.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| eng-architect | `skills/eng-team/agents/eng-architect.md` | Solution Architect and Threat Modeler | Strategic |
| eng-lead | `skills/eng-team/agents/eng-lead.md` | Engineering Lead and Standards Enforcer | Convergent |
| eng-backend | `skills/eng-team/agents/eng-backend.md` | Secure Backend Engineer | Systematic |
| eng-frontend | `skills/eng-team/agents/eng-frontend.md` | Secure Frontend Engineer | Systematic |
| eng-infra | `skills/eng-team/agents/eng-infra.md` | Secure Infrastructure Engineer | Systematic |
| eng-devsecops | `skills/eng-team/agents/eng-devsecops.md` | DevSecOps Pipeline Engineer | Systematic |
| eng-qa | `skills/eng-team/agents/eng-qa.md` | Security QA Engineer | Systematic |
| eng-security | `skills/eng-team/agents/eng-security.md` | Security Code Review Specialist | Forensic |
| eng-reviewer | `skills/eng-team/agents/eng-reviewer.md` | Final Review Gate and Quality Enforcer | Convergent |
| eng-incident | `skills/eng-team/agents/eng-incident.md` | Incident Response Specialist | Forensic |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| eng-architect | System design, architecture decisions, threat modeling (STRIDE/DREAD/PASTA) | Architecture decision records, threat models |
| eng-lead | Implementation planning, code standards enforcement, dependency governance | Implementation plans, standards mappings |
| eng-backend | Server-side implementation with OWASP Top 10 and ASVS 5.0 compliance | Secure backend code, API security artifacts |
| eng-frontend | Client-side implementation with XSS prevention, CSP, CORS hardening | Secure frontend code, CSP configurations |
| eng-infra | IaC security, container hardening, SBOM generation, SLSA compliance | Infrastructure configurations, SBOMs |
| eng-devsecops | SAST/DAST pipeline integration, secrets scanning, dependency analysis | Pipeline configurations, scan reports |
| eng-qa | Security test strategy, fuzzing campaigns, property-based testing | Test artifacts, coverage reports |
| eng-security | Manual secure code review against CWE Top 25 and OWASP ASVS | Finding reports with CWE classifications |
| eng-reviewer | Final gate with /adversary integration for C2+ at >= 0.95 threshold | Quality scores, compliance status |
| eng-incident | Incident response runbooks, vulnerability lifecycle management | IR plans, monitoring configurations |

**Invocation**: Use `/eng-team` skill which orchestrates these agents in an 8-step sequential phase-gate workflow.

**Model Tiers:** eng-architect (opus), eng-reviewer (opus); all others (sonnet).

**Artifact Location**: `skills/eng-team/output/{engagement-id}/`

---
```

### Red-Team Skill Agents Section

Insert immediately after the Eng-Team Skill Agents section:

```markdown
## Red-Team Skill Agents

These agents implement offensive security methodology through the `/red-team` skill, covering the full MITRE ATT&CK kill chain (14/14 tactics). Follows a non-linear workflow with mandatory scope authorization (red-lead first), circuit breaker checks at every agent transition, and RoE-gated agents for high-impact operations. Follows PTES, OSSTMM, and NIST SP 800-115 methodologies.

| Agent | File | Role | Cognitive Mode |
|-------|------|------|----------------|
| red-lead | `skills/red-team/agents/red-lead.md` | Engagement Lead & Scope Authority | Strategic |
| red-recon | `skills/red-team/agents/red-recon.md` | Reconnaissance Specialist | Divergent |
| red-vuln | `skills/red-team/agents/red-vuln.md` | Vulnerability Analyst | Systematic |
| red-exploit | `skills/red-team/agents/red-exploit.md` | Exploitation Specialist | Systematic |
| red-privesc | `skills/red-team/agents/red-privesc.md` | Privilege Escalation Specialist | Systematic |
| red-lateral | `skills/red-team/agents/red-lateral.md` | Lateral Movement Specialist | Systematic |
| red-persist | `skills/red-team/agents/red-persist.md` | Persistence Specialist (RoE-GATED) | Systematic |
| red-exfil | `skills/red-team/agents/red-exfil.md` | Data Exfiltration Specialist (RoE-GATED) | Systematic |
| red-reporter | `skills/red-team/agents/red-reporter.md` | Engagement Reporter & Documentation Specialist | Integrative |
| red-infra | `skills/red-team/agents/red-infra.md` | Infrastructure & Tooling Specialist | Systematic |
| red-social | `skills/red-team/agents/red-social.md` | Social Engineering Specialist (RoE-GATED) | Divergent |

**Key Capabilities:**

| Agent | Primary Use Case | Output Type |
|-------|------------------|-------------|
| red-lead | Scope establishment, RoE definition, authorization management | Scope documents, RoE YAML |
| red-recon | OSINT, network enumeration, service discovery, attack surface mapping | Reconnaissance reports |
| red-vuln | Vulnerability identification, CVE research, exploit availability assessment | Vulnerability reports with risk scores |
| red-exploit | Exploit methodology, payload crafting guidance, vulnerability chaining | Exploitation methodology reports |
| red-privesc | Local/domain privilege escalation, credential harvesting, token manipulation | Privilege escalation reports |
| red-lateral | Network pivoting, tunneling, living-off-the-land techniques | Lateral movement reports |
| red-persist | Backdoor placement methodology, scheduled tasks, rootkit analysis (RoE-GATED) | Persistence methodology reports |
| red-exfil | Data exfiltration channels, covert communication, DLP bypass (RoE-GATED) | Exfiltration methodology reports |
| red-reporter | Engagement reports, finding documentation, executive summaries | Final engagement reports |
| red-infra | C2 framework management, payload building, redirector infrastructure | Infrastructure methodology reports |
| red-social | Phishing campaigns, pretexting, vishing methodology (RoE-GATED) | Social engineering methodology reports |

**Invocation**: Use `/red-team` skill. red-lead MUST establish scope first (mandatory). After scope, any agent is invocable in any order.

**Model Tiers:** red-lead (opus), red-reporter (opus); all others (sonnet).

**Artifact Location**: `skills/red-team/output/{engagement-id}/`

**RoE-Gated Agents:** red-persist, red-exfil, red-social require explicit authorization in the Rules of Engagement beyond standard scope authorization.

---
```

### MCP Tool Access -- Context7 Update

Insert the following rows into the existing `### Context7 (Documentation Lookup)` table in the `## MCP Tool Access` section:

```markdown
| eng-architect | eng-team | resolve-library-id, query-docs |
| eng-lead | eng-team | resolve-library-id, query-docs |
| eng-backend | eng-team | resolve-library-id, query-docs |
| eng-frontend | eng-team | resolve-library-id, query-docs |
| eng-infra | eng-team | resolve-library-id, query-docs |
| eng-devsecops | eng-team | resolve-library-id, query-docs |
| eng-qa | eng-team | resolve-library-id, query-docs |
| eng-security | eng-team | resolve-library-id, query-docs |
| eng-reviewer | eng-team | resolve-library-id, query-docs |
| eng-incident | eng-team | resolve-library-id, query-docs |
| red-lead | red-team | resolve-library-id, query-docs |
| red-recon | red-team | resolve-library-id, query-docs |
| red-vuln | red-team | resolve-library-id, query-docs |
| red-exploit | red-team | resolve-library-id, query-docs |
| red-privesc | red-team | resolve-library-id, query-docs |
| red-lateral | red-team | resolve-library-id, query-docs |
| red-persist | red-team | resolve-library-id, query-docs |
| red-exfil | red-team | resolve-library-id, query-docs |
| red-reporter | red-team | resolve-library-id, query-docs |
| red-infra | red-team | resolve-library-id, query-docs |
| red-social | red-team | resolve-library-id, query-docs |
```

### MCP Tool Access -- Not Included Update

Update the `> **Not included (by design):**` paragraph to append:

```markdown
> **Not included (by design):** adv-* (self-contained strategy execution), sb-* (voice quality gate), wt-* (read-only auditing), ps-critic/ps-validator (quality evaluation), ps-reporter (report generation). eng-*/red-* agents do not use Memory-Keeper; their persistence model uses file-based output per P-002 (engagement-scoped output directories), not cross-session MCP storage.
```

### Verification Note Update

Update the verification note at the bottom of Agent Summary to reflect new counts:

```markdown
> **Verification:** Agent counts verified against filesystem scan (`skills/*/agents/*.md`).
> 62 total files found; 4 template/extension files excluded from counts:
> `NSE_AGENT_TEMPLATE.md`, `NSE_EXTENSION.md`, `PS_AGENT_TEMPLATE.md`, `PS_EXTENSION.md`.
> Per-skill sum: 9 + 10 + 3 + 3 + 3 + 5 + 3 + 1 + 10 + 11 = 58 invokable agents.
> Last verified: 2026-02-22.
```

---

## CLAUDE.md Registration Block

### Quick Reference Skills Table

Insert the following two rows into the `## Quick Reference` > **Skills** table in `CLAUDE.md`, after the existing `/ast` row:

```markdown
| `/eng-team` | Secure software engineering methodology (10 agents: architecture, implementation, quality, incident response) |
| `/red-team` | Offensive security testing methodology (11 agents: recon, exploitation, post-exploitation, reporting) |
```

### Full Updated Skills Table for Reference

The complete Skills table after insertion:

```markdown
| Skill | Purpose |
|-------|---------|
| `/worktracker` | Task/issue management |
| `/problem-solving` | Research, analysis, root cause |
| `/nasa-se` | Requirements, V&V, reviews |
| `/orchestration` | Multi-phase workflows |
| `/architecture` | Design decisions |
| `/adversary` | Adversarial quality reviews, strategy templates, tournament execution, multi-strategy orchestration |
| `/saucer-boy` | Session conversational voice, McConkey personality |
| `/saucer-boy-framework-voice` | Internal: framework output voice quality gate, persona compliance |
| `/transcript` | Transcription parsing |
| `/ast` | Markdown AST: parse, query, validate, modify frontmatter |
| `/eng-team` | Secure software engineering methodology (10 agents: architecture, implementation, quality, incident response) |
| `/red-team` | Offensive security testing methodology (11 agents: recon, exploitation, post-exploitation, reporting) |
```

---

## mandatory-skill-usage.md Registration Block

### H-22 Rule Update

Update the H-22 rule description in the `## HARD Rules` table to include the new skills:

```markdown
| H-22 | MUST invoke `/problem-solving` for research/analysis. MUST invoke `/nasa-se` for requirements/design. MUST invoke `/orchestration` for multi-phase workflows. MUST invoke `/transcript` for transcript parsing and meeting note extraction. MUST invoke `/adversary` for standalone adversarial reviews outside creator-critic loops, tournament scoring, and formal strategy application (red team, devil's advocate, steelman, pre-mortem). MUST invoke `/ast` for worktracker entity frontmatter extraction, entity validation, and markdown structural analysis (H-33). MUST invoke `/eng-team` for secure software engineering, threat modeling, security architecture, DevSecOps, and security code review. MUST invoke `/red-team` for penetration testing, offensive security, reconnaissance, exploitation methodology, and engagement reporting. | Work quality degradation. Rework required. |
```

### Trigger Map Entries

Insert the following two rows into the `## Trigger Map` table, after the existing `/ast` entry:

```markdown
| secure development, secure design, threat model, security architecture, STRIDE, DREAD, SDLC, DevSecOps, SAST, DAST, code review for security, OWASP, ASVS, CWE, SSDF, SLSA, incident response, supply chain security, security requirements, CIS benchmark | `/eng-team` |
| penetration test, pentest, red team, offensive security, reconnaissance, exploit, privilege escalation, lateral movement, persistence, exfiltration, C2, command and control, social engineering, phishing, attack surface, kill chain, PTES, OSSTMM, ATT&CK, rules of engagement, vulnerability assessment | `/red-team` |
```

### L2-REINJECT Update

Update the L2-REINJECT comment at the top of the file to include the new skills:

```html
<!-- L2-REINJECT: rank=6, tokens=70, content="Proactive skill invocation REQUIRED (H-22). /problem-solving for research. /nasa-se for design. /orchestration for workflows. /transcript for transcript parsing and meeting notes. /adversary for standalone adversarial reviews, tournament scoring, formal strategy application. /ast for frontmatter extraction and entity validation (H-33). /eng-team for secure engineering, threat modeling, DevSecOps. /red-team for penetration testing, offensive security, engagement methodology." -->
```

### Full Updated Trigger Map for Reference

The complete Trigger Map table after insertion:

```markdown
## Trigger Map

| Detected Keywords | Skill |
|-------------------|-------|
| research, analyze, investigate, explore, root cause, why | `/problem-solving` |
| requirements, specification, V&V, technical review, risk | `/nasa-se` |
| orchestration, pipeline, workflow, multi-agent, phases, gates | `/orchestration` |
| transcript, meeting notes, parse recording, meeting recording, VTT, SRT, captions | `/transcript` |
| adversarial quality review, adversarial critique, rigorous critique, formal critique, adversarial, tournament, red team, devil's advocate, steelman, pre-mortem, quality gate, quality scoring | `/adversary` |
| saucer boy, mcconkey, talk like mcconkey, pep talk, roast this code, saucer boy mode | `/saucer-boy` |
| voice check, voice review, persona compliance, voice rewrite, voice fidelity, voice score, framework voice, persona review | `/saucer-boy-framework-voice` |
| frontmatter, entity metadata, status extraction, validate entity, parse markdown, blockquote frontmatter, nav table validation, schema validation | `/ast` |
| secure development, secure design, threat model, security architecture, STRIDE, DREAD, SDLC, DevSecOps, SAST, DAST, code review for security, OWASP, ASVS, CWE, SSDF, SLSA, incident response, supply chain security, security requirements, CIS benchmark | `/eng-team` |
| penetration test, pentest, red team, offensive security, reconnaissance, exploit, privilege escalation, lateral movement, persistence, exfiltration, C2, command and control, social engineering, phishing, attack surface, kill chain, PTES, OSSTMM, ATT&CK, rules of engagement, vulnerability assessment | `/red-team` |
```

### Trigger Map Disambiguation Note

The `/adversary` skill trigger map includes "red team" as a keyword (referring to adversarial quality review strategy S-001). The `/red-team` skill also uses "red team" as a keyword (referring to offensive security testing). To disambiguate:

| Context | Routes To | Rationale |
|---------|-----------|-----------|
| "Red team this deliverable" / "Red team review of this design" | `/adversary` | Quality review context -- S-001 Red Team Analysis strategy |
| "Red team engagement" / "Red team the target network" / "Red team penetration test" | `/red-team` | Offensive security testing context -- engagement-based work |
| "Red team" with no additional context | Clarify per H-31 | Ambiguous -- multiple valid interpretations exist |

This disambiguation follows H-31 (Clarify before acting when ambiguous). The presence of engagement-specific keywords (target, network, penetration, scope, engagement) resolves to `/red-team`. The presence of quality keywords (deliverable, review, critique, score) resolves to `/adversary`.

---

## MCP Tool Access Registration Block

### Context7 Integration

All 21 agents across both skills declare `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` in their `capabilities.allowed_tools` frontmatter. This follows MCP-001 (Context7 MUST be used when any agent task references an external library, framework, SDK, or API by name).

Neither skill uses Memory-Keeper. Persistence follows P-002 file-based output to engagement-scoped directories (`skills/{skill}/output/{engagement-id}/`), not MCP cross-session storage. This design decision aligns with the skills' engagement-scoped workflow model where all state is contained within the engagement output directory.

### mcp-tool-standards.md Agent Integration Matrix Update

Insert the following rows into the `## Agent Integration Matrix` table:

```markdown
| eng-architect | resolve, query | -- | Library/framework security research |
| eng-lead | resolve, query | -- | Standards and dependency research |
| eng-backend | resolve, query | -- | Backend framework security docs |
| eng-frontend | resolve, query | -- | Frontend framework security docs |
| eng-infra | resolve, query | -- | Infrastructure and container docs |
| eng-devsecops | resolve, query | -- | Security tooling documentation |
| eng-qa | resolve, query | -- | Testing framework documentation |
| eng-security | resolve, query | -- | Security standard documentation |
| eng-reviewer | resolve, query | -- | Standards verification research |
| eng-incident | resolve, query | -- | IR framework documentation |
| red-lead | resolve, query | -- | Methodology framework research |
| red-recon | resolve, query | -- | Reconnaissance tool documentation |
| red-vuln | resolve, query | -- | Vulnerability database research |
| red-exploit | resolve, query | -- | Exploitation framework docs |
| red-privesc | resolve, query | -- | OS and AD documentation |
| red-lateral | resolve, query | -- | Network protocol documentation |
| red-persist | resolve, query | -- | OS internals documentation |
| red-exfil | resolve, query | -- | Protocol and channel documentation |
| red-reporter | resolve, query | -- | Reporting framework docs |
| red-infra | resolve, query | -- | C2 framework documentation |
| red-social | resolve, query | -- | Social engineering methodology |
```

### Not-Included Rationale Update

Add to the `**Not included (by design):**` section:

```markdown
- **eng-*** -- File-based persistence per P-002 (engagement-scoped output); no cross-session state requirement
- **red-*** -- File-based persistence per P-002 (engagement-scoped output); scope documents and evidence stored in engagement directories
```

---

## Verification Checklist

### H-25: Skill File Naming

| Skill | File | Exact `SKILL.md` (case-sensitive) | Status |
|-------|------|-----------------------------------|--------|
| eng-team | `skills/eng-team/SKILL.md` | Yes | PASS |
| red-team | `skills/red-team/SKILL.md` | Yes | PASS |

### H-26: Folder Naming

| Skill | Folder | Kebab-case | Matches `name` field | Status |
|-------|--------|------------|----------------------|--------|
| eng-team | `skills/eng-team/` | Yes | Yes (`name: eng-team`) | PASS |
| red-team | `skills/red-team/` | Yes | Yes (`name: red-team`) | PASS |

### H-25: No README.md in Skill Folder

| Skill | README.md present | Status |
|-------|-------------------|--------|
| eng-team | No | PASS |
| red-team | No | PASS |

### H-26: Description Field Compliance

| Requirement | eng-team | red-team |
|-------------|----------|----------|
| Includes WHAT it does | Yes ("Secure engineering team skill providing methodology guidance for building security-hardened software") | Yes ("Offensive security team skill providing methodology guidance for penetration testing and red team engagements") |
| Includes WHEN to use it | Yes ("Invoked when users request system design, implementation, code review, testing, CI/CD security, or incident response with security considerations") | Yes ("Invoked when users request penetration testing, reconnaissance, vulnerability analysis, exploitation methodology, social engineering, C2 infrastructure, or engagement reporting") |
| Includes trigger phrases | Yes (20 activation keywords in frontmatter) | Yes (20 activation keywords in frontmatter) |
| Under 1024 characters | Yes (eng-team description: 486 chars) | Yes (red-team description: 374 chars) |
| No XML tags | Yes | Yes |
| Status | PASS | PASS |

### H-26: Full Repo-Relative Paths

| Skill | All file references repo-relative | Status |
|-------|-----------------------------------|--------|
| eng-team | Yes (e.g., `skills/eng-team/agents/eng-architect.md`, `skills/eng-team/output/{engagement-id}/`) | PASS |
| red-team | Yes (e.g., `skills/red-team/agents/red-lead.md`, `skills/red-team/output/{engagement-id}/`) | PASS |

### H-26: Registration Completeness

| Registration Target | eng-team | red-team | Status |
|---------------------|----------|----------|--------|
| `CLAUDE.md` Quick Reference Skills table | Content block produced (this report) | Content block produced (this report) | READY |
| `AGENTS.md` agent registry | Content block produced -- 10 agents with file paths, roles, cognitive modes, capabilities | Content block produced -- 11 agents with file paths, roles, cognitive modes, capabilities | READY |
| `AGENTS.md` Agent Summary update | Count updated (37 -> 58, +10 eng +11 red) | (included in same update) | READY |
| `AGENTS.md` MCP Tool Access update | Context7 entries for all 10 agents | Context7 entries for all 11 agents | READY |
| `.context/rules/mandatory-skill-usage.md` Trigger Map | 20 trigger keywords mapped to `/eng-team` | 21 trigger keywords mapped to `/red-team` | READY |
| `.context/rules/mandatory-skill-usage.md` H-22 rule update | Rule text expanded to include `/eng-team` | Rule text expanded to include `/red-team` | READY |
| `.context/rules/mcp-tool-standards.md` Agent Integration Matrix | 10 agents added with Context7 access | 11 agents added with Context7 access | READY |

### Agent Count Verification

| Source | eng-team Count | red-team Count | Total |
|--------|---------------|----------------|-------|
| SKILL.md `agents:` frontmatter list | 10 | 11 (inferred from Available Agents table) | 21 |
| `skills/eng-team/agents/*.md` filesystem | 10 files | -- | 10 |
| `skills/red-team/agents/*.md` filesystem | -- | 11 files | 11 |
| This report agent registry entries | 10 entries | 11 entries | 21 |
| **Status** | **MATCH** | **MATCH** | **21 VERIFIED** |

### Model Tier Verification

All model tiers verified against agent frontmatter `model:` field:

| Agent | Declared Model | Verified |
|-------|---------------|----------|
| eng-architect | opus | Yes |
| eng-lead | sonnet | Yes |
| eng-backend | sonnet | Yes |
| eng-frontend | sonnet | Yes |
| eng-infra | sonnet | Yes |
| eng-devsecops | sonnet | Yes |
| eng-qa | sonnet | Yes |
| eng-security | sonnet | Yes |
| eng-reviewer | opus | Yes |
| eng-incident | sonnet | Yes |
| red-lead | opus | Yes |
| red-recon | sonnet | Yes |
| red-vuln | sonnet | Yes |
| red-exploit | sonnet | Yes |
| red-privesc | sonnet | Yes |
| red-lateral | sonnet | Yes |
| red-persist | sonnet | Yes |
| red-exfil | sonnet | Yes |
| red-reporter | opus | Yes |
| red-infra | sonnet | Yes |
| red-social | sonnet | Yes |

**Opus agents (4):** eng-architect, eng-reviewer, red-lead, red-reporter -- used for critical decision-making (architecture, final quality gate, scope authorization, comprehensive reporting).

**Sonnet agents (17):** All remaining agents -- used for domain-specific execution work.

---

## Summary

This report provides complete, ready-to-insert registration content for all three H-26 registration targets plus the MCP tool standards file. All 21 agents across the `/eng-team` and `/red-team` skills have been verified against H-25 and H-26 compliance requirements.

**Registration blocks produced:**

1. **AGENTS.md** -- Navigation table update, Agent Summary update (37 -> 58), two full agent sections (10 + 11 agents each with file paths, roles, cognitive modes, and capabilities tables), MCP Tool Access Context7 entries for all 21 agents
2. **CLAUDE.md** -- Two Quick Reference Skills table rows
3. **mandatory-skill-usage.md** -- H-22 rule text expansion, two Trigger Map rows (20 + 21 keywords), L2-REINJECT comment update, trigger disambiguation note for "red team" keyword overlap with `/adversary`
4. **mcp-tool-standards.md** -- Agent Integration Matrix entries for all 21 agents

**No framework files were modified.** All content blocks are documented in this report for review and subsequent application by the framework maintainer.

---

*Report produced: 2026-02-22*
*FEAT-054: Framework Registration*
*PROJ-010: Cyber Ops -- EPIC-006 Documentation & Guides*
*Governing rule: H-26 (skill-standards.md)*
