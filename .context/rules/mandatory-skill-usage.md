# Mandatory Skill Usage

> Proactive skill invocation rules. DO NOT wait for user to invoke -- delayed invocation causes H-22 violation, skill context is not loaded, and work quality degrades. Instead: trigger skills proactively when keyword conditions in the trigger map match.

<!-- L2-REINJECT: rank=6, content="Proactive skill invocation REQUIRED (H-22). /problem-solving for research. /nasa-se for design. /orchestration for workflows. /transcript for transcript parsing and meeting notes. /adversary for standalone adversarial reviews, tournament scoring, formal strategy application. /ast for frontmatter extraction and entity validation (H-33). /eng-team for secure engineering, threat modeling, DevSecOps. /red-team for penetration testing, offensive security, engagement methodology. /pm-pmm for product strategy, customer insight, business analysis, competitive intelligence, and GTM planning. /diataxis for documentation creation, classification, and auditing. /prompt-engineering for structured prompt construction, NPT constraint generation, prompt quality scoring. /user-experience for UX evaluation, user research, design systems, usability audits. /rainbow for tool-assisted cybersecurity operations (supply chain scanning, reconnaissance, cloud posture, exploitation). /blue-team for defensive cybersecurity (detection, malware analysis, compliance, incident response, threat intelligence)." -->

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
| H-22 | MUST invoke `/problem-solving` for research/analysis. MUST invoke `/nasa-se` for requirements/design. MUST invoke `/orchestration` for multi-phase workflows. MUST invoke `/transcript` for transcript parsing and meeting note extraction. MUST invoke `/adversary` for standalone adversarial reviews outside creator-critic loops, tournament scoring, and formal strategy application (red team, devil's advocate, steelman, pre-mortem). MUST invoke `/ast` for worktracker entity frontmatter extraction, entity validation, and markdown structural analysis (H-33). MUST invoke `/eng-team` for secure software engineering, threat modeling, security architecture, DevSecOps, and security code review. MUST invoke `/red-team` for penetration testing, offensive security, reconnaissance, exploitation methodology, and engagement reporting. MUST invoke `/pm-pmm` for product management and product marketing work including product strategy (PRDs, vision, roadmaps), customer insight (personas, journey maps, VOC), business analysis (business cases, market sizing, pricing), competitive intelligence (battle cards, win/loss), and go-to-market planning (GTM plans, positioning, MRDs, buyer personas). MUST invoke `/diataxis` for documentation creation, classification, and auditing using Diataxis four-quadrant methodology. MUST invoke `/prompt-engineering` for structured prompt construction, NPT constraint generation, and prompt quality scoring. MUST invoke `/user-experience` for UX evaluation, user research, design systems, UX metrics, behavior diagnosis, feature prioritization, and usability audits. MUST invoke `/rainbow` for tool-assisted cybersecurity operations (supply chain scanning, reconnaissance, cloud posture, exploitation). MUST invoke `/blue-team` for defensive cybersecurity (detection, malware analysis, compliance, incident response, threat intelligence). | Work quality degradation. Rework required. |

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
| product strategy, PRD, product requirements, roadmap, prioritize, RICE, Kano, product vision, north star metric, opportunity solution tree, product kata, JTBD, customer insight, persona, customer interview, journey map, VOC, voice of customer, customer discovery, pain points, churn analysis, NPS, CSAT, CES, business case, financial model, market sizing, TAM, SAM, SOM, pricing model, unit economics, LTV, CAC, NRR, NPV, IRR, break-even, feasibility, revenue model, Van Westendorp, Lean Canvas, Rule of 40, Magic Number, payback period, competitive analysis, battle card, win/loss, competitor, Porter's, SWOT, competitive landscape, differentiation, market intelligence, competitive threat, Blue Ocean, value curve, Crossing the Chasm, GTM, go-to-market, positioning, messaging, MRD, launch plan, sales enablement, buyer persona, product marketing, PLG, product-led growth | code review, architecture, ADR, engineering, implementation, deployment, CI/CD, testing, test coverage, infrastructure pricing, cloud pricing, adversarial, tournament, transcript, VTT, SRT, penetration test, exploit, strategy | 9 | "product requirements" OR "product strategy" OR "market sizing" OR "go-to-market" OR "competitive analysis" OR "business case" OR "buyer persona" (phrase match) | `/pm-pmm` |
| secure development, secure design, threat model, security architecture, STRIDE, DREAD, SDLC, DevSecOps, SAST, DAST, code review for security, OWASP, ASVS, CWE, SSDF, SLSA, incident response, supply chain security, security requirements, CIS benchmark | adversarial, tournament, quality gate | 9 | -- | `/eng-team` |
| penetration test, pentest, red team, offensive security, reconnaissance, exploit, privilege escalation, lateral movement, persistence, exfiltration, C2, command and control, social engineering, phishing, attack surface, kill chain, PTES, OSSTMM, ATT&CK, rules of engagement, vulnerability assessment | adversarial quality review, quality gate, quality scoring | 10 | -- | `/red-team` |
| build prompt, create prompt, prompt template, NPT pattern, constraint generation, prompt quality, score prompt, prompt engineering, NPT-009, NPT-013, forbidden actions format, structured negation | adversarial, research, investigate, requirements, transcript | 11 | -- | `/prompt-engineering` |
| documentation, tutorial, how-to, howto, how-to guide, reference docs, explanation, diataxis, write docs, write documentation, write tutorial, create documentation, classify documentation, audit documentation, quadrant, doc type, user guide, getting started, quickstart, API docs, developer guide | adversarial, tournament, transcript, penetration, exploit, requirements, specification, architecture, root cause, debug, investigate, code review | 11 | "reference documentation" OR "technical documentation" OR "API documentation" OR "developer documentation" OR "create documentation" OR "write documentation" OR "write docs" OR "write tutorial" OR "classify documentation" OR "audit documentation" (phrase match) | `/diataxis` |
| UX, user experience, usability, heuristic evaluation, JTBD, jobs to be done, lean UX, HEART metrics, atomic design, inclusive design, behavior design, Kano model, design sprint, AI-first design, UX audit, accessibility, design system, user research, UX metrics, component taxonomy, usability audit | adversarial, tournament, quality gate, penetration, exploit, requirements, specification, transcript, code review | 12 | "UX audit" OR "usability evaluation" OR "design sprint" OR "user research" (phrase match) | `/user-experience` |
| SBOM, vulnerability scan, supply chain security, container scan, IaC scan, reconnaissance pipeline, subdomain enumeration, port scan, cloud security posture, exploit framework, exploit methodology, Nuclei, Trivy, Checkov, Syft, Grype, rainbow, tool-assisted pentest, OSINT tools, C2 framework, Prowler, Kubescape, Subfinder, httpx, pwntools, Impacket, Metasploit, mitmproxy, Frida, mobile security scan | code review for security, threat model, secure design, STRIDE, DREAD, SDLC, DevSecOps pipeline, adversarial quality review, quality gate, quality scoring, malware analysis, threat detection, YARA, reverse engineering, binary analysis, incident triage | 10 | "supply chain security" OR "vulnerability scan" OR "reconnaissance pipeline" OR "exploit framework" OR "cloud security posture" (phrase match) | `/rainbow` |
| threat detection, malware analysis, YARA, IOC, indicator of compromise, reverse engineering, binary analysis, malware family, blue team defense, defensive operations, compliance audit, CIS benchmark audit, NIST CSF assessment, incident triage, detection rules, threat hunting, decompile APK, decompile binary | penetration test, exploit, offensive, reconnaissance, red team, attack surface, code review, architecture, implementation, adversarial quality review, quality gate, supply chain, SBOM, container scan | 10 | "malware analysis" OR "threat detection" OR "compliance audit" OR "incident triage" OR "reverse engineering" (phrase match) | `/blue-team` |

> **Disambiguation: "red team" keyword overlap.** The `/adversary` skill uses "red team" for adversarial quality review (S-001 Red Team Analysis strategy). The `/red-team` skill uses "red team" for offensive security testing. Context determines routing: quality/review context -> `/adversary`; engagement/target/penetration context -> `/red-team`; ambiguous -> clarify per H-31.

> **Disambiguation: cybersecurity skill 4-way routing.** Four skills cover cybersecurity domains with overlapping vocabulary. Context determines routing: "malware analysis" or "YARA" -> `/blue-team` (defensive detection/analysis); "vulnerability scan" or "Nuclei" -> `/rainbow` (tool-assisted scanning); "penetration test methodology" or "PTES" -> `/red-team` (engagement methodology); "secure development" or "SAST pipeline" -> `/eng-team` (engineering methodology); ambiguous -> clarify per H-31.

---

## Behavior Rules

1. DO NOT WAIT for user to invoke skills -- use proactively when triggers apply.
2. COMBINE skills when appropriate (e.g., /orchestration + /problem-solving + /nasa-se).
3. INVOKE EARLY at start of work, not after struggling without them.
4. PERSIST all skill outputs to the repository.
5. See `skills/{name}/SKILL.md` for skill details. See `AGENTS.md` for agent registry.
