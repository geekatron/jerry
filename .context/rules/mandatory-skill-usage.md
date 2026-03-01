# Mandatory Skill Usage

> Proactive skill invocation rules. DO NOT wait for user to invoke -- delayed invocation causes H-22 violation, skill context is not loaded, and work quality degrades. Instead: trigger skills proactively when keyword conditions in the trigger map match.

<!-- L2-REINJECT: rank=6, content="Proactive skill invocation REQUIRED (H-22). /problem-solving for research. /nasa-se for design. /orchestration for workflows. /transcript for transcript parsing and meeting notes. /adversary for standalone adversarial reviews, tournament scoring, formal strategy application. /ast for frontmatter extraction and entity validation (H-33). /eng-team for secure engineering, threat modeling, DevSecOps. /red-team for penetration testing, offensive security, engagement methodology." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Skill invocation constraint H-22 |
| [Trigger Map](#trigger-map) | Keywords to skill mapping |
| [Behavior Rules](#behavior-rules) | How to apply skill invocation |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence |
|----|------|-------------|
| H-22 | MUST invoke `/problem-solving` for research/analysis. MUST invoke `/nasa-se` for requirements/design. MUST invoke `/orchestration` for multi-phase workflows. MUST invoke `/transcript` for transcript parsing and meeting note extraction. MUST invoke `/adversary` for standalone adversarial reviews outside creator-critic loops, tournament scoring, and formal strategy application (red team, devil's advocate, steelman, pre-mortem). MUST invoke `/ast` for worktracker entity frontmatter extraction, entity validation, and markdown structural analysis (H-33). MUST invoke `/eng-team` for secure software engineering, threat modeling, security architecture, DevSecOps, and security code review. MUST invoke `/red-team` for penetration testing, offensive security, reconnaissance, exploitation methodology, and engagement reporting. | Work quality degradation. Rework required. |

---

## Trigger Map

> Phase 1 enhanced format (5-column) per `agent-routing-standards.md`. Backward-compatible: consumers parsing only columns 1+5 continue to function.

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| research, analyze, investigate, explore, root cause, why, debug, troubleshoot, diagnose, figure out, what went wrong, compare, evaluate | requirements, specification, V&V, adversarial, tournament, transcript, VTT, SRT, voice, persona | 6 | -- | `/problem-solving` |
| requirements, specification, V&V, technical review, risk, design, architecture, interface, trade study, compliance | root cause, debug, adversarial, tournament, research (standalone), transcript | 5 | "technical review" (both words required) | `/nasa-se` |
| orchestration, pipeline, workflow, multi-agent, phases, gates, plan, coordinate, break into steps, sequence | adversarial, transcript, root cause, debug | 1 | -- | `/orchestration` |
| transcript, meeting notes, parse recording, meeting recording, VTT, SRT, captions, audio, summarize this meeting | adversarial, requirements, design | 2 | "parse recording" OR "meeting recording" (phrase match) | `/transcript` |
| adversarial quality review, adversarial critique, rigorous critique, formal critique, adversarial, tournament, red team, devil's advocate, steelman, pre-mortem, quality gate, quality scoring | requirements, specification, design, research, investigate, penetration, exploit, engagement | 7 | "adversarial review" OR "quality gate" OR "quality scoring" (phrase match) | `/adversary` |
| saucer boy, mcconkey, talk like mcconkey, pep talk, roast this code, saucer boy mode | -- | 3 | -- | `/saucer-boy` |
| voice check, voice review, persona compliance, voice rewrite, voice fidelity, voice score, framework voice, persona review | -- | 4 | ("voice" OR "persona") AND ("review" OR "check" OR "score") | `/saucer-boy-framework-voice` |
| frontmatter, entity metadata, status extraction, validate entity, parse markdown, blockquote frontmatter, nav table validation, schema validation | -- | 8 | -- | `/ast` |
| secure development, secure design, threat model, security architecture, STRIDE, DREAD, SDLC, DevSecOps, SAST, DAST, code review for security, OWASP, ASVS, CWE, SSDF, SLSA, incident response, supply chain security, security requirements, CIS benchmark | adversarial, tournament, quality gate | 9 | -- | `/eng-team` |
| penetration test, pentest, red team, offensive security, reconnaissance, exploit, privilege escalation, lateral movement, persistence, exfiltration, C2, command and control, social engineering, phishing, attack surface, kill chain, PTES, OSSTMM, ATT&CK, rules of engagement, vulnerability assessment | adversarial quality review, quality gate, quality scoring | 10 | -- | `/red-team` |

> **Disambiguation: "red team" keyword overlap.** The `/adversary` skill uses "red team" for adversarial quality review (S-001 Red Team Analysis strategy). The `/red-team` skill uses "red team" for offensive security testing. Context determines routing: quality/review context -> `/adversary`; engagement/target/penetration context -> `/red-team`; ambiguous -> clarify per H-31.

---

## Behavior Rules

1. DO NOT WAIT for user to invoke skills -- use proactively when triggers apply.
2. COMBINE skills when appropriate (e.g., /orchestration + /problem-solving + /nasa-se).
3. INVOKE EARLY at start of work, not after struggling without them.
4. PERSIST all skill outputs to the repository.
5. See `skills/{name}/SKILL.md` for skill details. See `AGENTS.md` for agent registry.
