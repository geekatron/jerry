# Phase 4 Quality Gate -- Barrier 4b (/red-team)

> **Scorer:** adv-scorer (S-014 LLM-as-Judge)
> **Date:** 2026-02-22
> **Scoring Method:** S-014 with strict leniency bias counteraction
> **Specification Baseline:** ADR-PROJ010-001, ADR-PROJ010-002, ADR-PROJ010-006

## Gate Configuration

- **Criticality:** C4 (Critical)
- **Threshold:** >= 0.95
- **Scoring Method:** S-014 LLM-as-Judge with 6 weighted dimensions
- **Deliverables:** 12 files (SKILL.md + 11 agents), 2,766 total lines
- **Exemplar Comparison:** skills/problem-solving/SKILL.md (v2.2.0), skills/problem-solving/agents/ps-researcher.md (v2.3.0)

---

## Scoring Results

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Completeness | 0.20 | 0.97 | All 11 agents are defined with full agent definition files. SKILL.md contains all required sections: Purpose, When to Use, Available Agents (with ATT&CK mapping table), Mandatory Authorization (with full YAML schema), P-003 Compliance, Invoking an Agent (3 options), Orchestration Flow (non-linear kill chain diagram), Cross-Skill Integration Points (all 4 documented with attribute tables), Safety Alignment Compatibility, Circuit Breaker Integration (full protocol), Authorization Architecture (all 3 layers with component tables), Mandatory Persistence, Adversarial Quality Mode, Constitutional Compliance, Quick Reference, Defense Evasion Ownership table, and References. The three-layer authorization architecture is documented with structural/dynamic/retrospective layers and 7 enforcement components. All 14 ATT&CK tactics are mapped across agents (TA0001, TA0002, TA0003, TA0004, TA0005, TA0006, TA0007, TA0008, TA0009, TA0010, TA0011, TA0040, TA0042, TA0043). Kill chain workflow is documented with ASCII diagram. Cross-skill integration points (4) are fully specified. Defense evasion ownership model is complete with 6 owners. Circuit breaker integration is documented. Minor deduction: SKILL.md does not have a navigation table as specified by H-23/H-24 (it uses Triple-Lens audience table but not a Section/Purpose navigation table -- though the Triple-Lens format IS an accepted format per markdown-navigation-standards.md). red-vuln is listed in the Available Agents table without an explicit ATT&CK tactic ID (listed as "Analysis support" rather than a TA number), which is accurate per the ADR but could be viewed as incomplete mapping. |
| Internal Consistency | 0.20 | 0.96 | The non-linear kill chain workflow is consistently described across SKILL.md and all agent files. Every agent references the same scope document requirements, the same P-003 compliance model (workers, not orchestrators), and the same authorization verification pattern. ATT&CK tactic assignments are non-overlapping: red-recon owns TA0043, red-exploit owns TA0001/TA0002/TA0040, red-privesc owns TA0004/TA0006, red-lateral owns TA0008/TA0007, red-persist owns TA0003, red-exfil owns TA0009/TA0010, red-infra owns TA0042/TA0011, red-social owns TA0043(social)/TA0001(phishing). Defense evasion (TA0005) is correctly distributed per ADR-001 Section 6: red-infra (tool-level), red-exploit (execution-time), red-privesc (credential-based), red-lateral (network-level), red-persist (persistence-phase), red-exfil (exfiltration-phase). All agents enforce scope compliance identically. RoE-gated agents (red-persist, red-exfil, red-social) consistently declare their gating requirements in both SKILL.md and their own definitions with matching guardrails input_validation fields. Authorization requirements in SKILL.md match agent definitions. Minor deduction: red-social and red-recon share TA0043 Reconnaissance -- this is documented and intentional (social vs. technical reconnaissance), but could be viewed as partial overlap. red-exploit and red-social share TA0001 Initial Access (exploitation vs. phishing) -- also documented and intentional per ADR-001 but technically overlapping tactic IDs. The SKILL.md accurately lists these shared assignments. |
| Methodological Rigor | 0.20 | 0.96 | All agents are explicitly grounded in PTES, OSSTMM, and NIST SP 800-115. Each agent's Methodology section cites specific PTES phases (e.g., red-recon cites "PTES Intelligence Gathering," red-exploit cites "PTES Exploitation Phase," red-reporter cites "PTES Reporting Phase"). ATT&CK technique mappings are specific with technique IDs (not just tactic-level): red-recon lists T1595, T1592, T1589, T1590, T1591, T1593, T1594, T1596, T1597, T1598; red-exploit lists T1190, T1133, T1078, T1059, T1203, T1485, T1486, T1489, T1055, T1218; etc. RoE-gated agents are properly marked with explicit gating requirements (red-persist checks `persistence_authorized`, red-exfil checks `exfiltration_authorized` with `data_types_permitted`, red-social checks `social_engineering_authorized`). The authorization model is properly layered per ADR-006: Layer 1 Structural (scope document, target allowlist, technique allowlist, time window, exclusions, RoE), Layer 2 Dynamic (Scope Oracle, Tool Proxy, Network Enforcer, Credential Broker), Layer 3 Retrospective (action log review, evidence verification, compliance report). The AD-001 Methodology-First Design Paradigm is consistently applied across all agents. Minor deduction: OSSTMM and NIST SP 800-115 are cited by name but without specific version numbers in most agent files (PTES similarly lacks versioning -- though these standards do not have versioned releases in the same way as OWASP ASVS). The OWASP Testing Guide is cited without version in some agents. |
| Evidence Quality | 0.15 | 0.93 | Agents reference specific ATT&CK tactic IDs (TA0001-TA0043) and technique IDs (T1055, T1218, T1134, T1205, T1572, T1070, T1099, T1014, T1027, T1480, T1497, etc.) throughout. Methodology standards are cited (PTES, OSSTMM, NIST SP 800-115, OWASP Testing Guide). Tool references are specific and current (Metasploit, Burp Suite, Nmap, Shodan, Amass, theHarvester, Nuclei, Nessus, LinPEAS, WinPEAS, BloodHound, Mimikatz, Impacket, CrackMapExec, Chisel, GoPhish, Cobalt Strike, Sliver, Mythic). Authorization requirements trace to ADR-006 (referenced in every agent footer as "SSOT: ADR-PROJ010-001, ADR-PROJ010-006"). SKILL.md references section with specific artifact IDs (A-002, A-003, A-004, B-001, B-002, S-001). Deductions: (1) Some ATT&CK technique IDs appear to use deprecated numbering -- T1076 (Remote Desktop Protocol) in red-lateral was renumbered to T1021.001 in ATT&CK v8; T1099 (Timestomp) in red-persist was renumbered to T1070.006; T1028 (Windows Remote Management) was renumbered to T1021.006. These are substantive accuracy issues in a C4 deliverable that claims "real offensive techniques" per R-018. (2) PTES and OSSTMM lack publication date or version citations. (3) Agent files do not include inline citations to specific ADR sections (e.g., "per ADR-001 Section 6") -- they cite ADR IDs in footers only. |
| Actionability | 0.15 | 0.96 | The engagement workflow is clear and followable. SKILL.md provides 3 invocation options (natural language, explicit agent request, Task tool invocation) with concrete examples. The red-lead mandatory first agent requirement is clearly enforced in multiple locations: Section "Mandatory Authorization," Orchestration Rules #1, and the flow diagram. Agent routing is clear through the Quick Reference section with keywords-to-agent mapping and Common Workflows table. Output locations are explicit with consistent naming convention: `skills/red-team/output/{engagement-id}/{agent-name}-{topic-slug}.md`. Handoff protocols are explicit: phase cycling is documented with concrete examples (red-exploit findings trigger red-recon, red-privesc discovers vulnerabilities trigger red-vuln, red-lateral reveals new segments trigger red-recon). The scope document YAML schema in SKILL.md is complete with all fields documented. Minor deduction: The Task tool invocation example (Option 3 in SKILL.md) shows a Python-like syntax that is specific to the Jerry framework but lacks clarity on where the scope document path resolution happens at invocation time. The "What Happens Without Authorization" section is clear but brief (3 steps). |
| Traceability | 0.10 | 0.92 | Every agent file includes footer traceability: "SSOT: ADR-PROJ010-001, ADR-PROJ010-006" and "Constitutional Compliance: Jerry Constitution v1.0". SKILL.md References section cites ADR-PROJ010-001, ADR-PROJ010-002, ADR-PROJ010-003, ADR-PROJ010-006, plus research artifacts A-002, A-003, A-004, B-001, B-002, S-001. Cross-skill integration points trace to ADR-001 Section 5 and A-002 Finding 7. Defense evasion ownership model is traceable to ADR-001 Section 6. The scope document specification traces to ADR-006. Deductions: (1) Individual agent files do NOT trace to specific AD decisions (AD-001 through AD-012) inline -- they reference ADR IDs in footers but do not cite specific architecture decisions like "per AD-001" or "per AD-010" inline in the body text, even though the exemplar ps-researcher does not do this either. (2) The defense evasion ownership in agent files references the concept but does not cite "ADR-001 Section 6" by name (SKILL.md does cite this). (3) No agent file traces to specific A-004 recommendations (R-ROSTER-001 through R-ROSTER-014) despite these being the design-level justifications. (4) ADR-PROJ010-002 (routing) is referenced in SKILL.md References but the routing architecture is not traced inline in the Invoking an Agent or Quick Reference sections. |

## Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.97 | 0.1940 |
| Internal Consistency | 0.20 | 0.96 | 0.1920 |
| Methodological Rigor | 0.20 | 0.96 | 0.1920 |
| Evidence Quality | 0.15 | 0.93 | 0.1395 |
| Actionability | 0.15 | 0.96 | 0.1440 |
| Traceability | 0.10 | 0.92 | 0.0920 |

**Weighted Composite: 0.9535**

**Result: PASS (0.9535 >= 0.95)**

---

## Deficiencies Found

### Evidence Quality Issues (Score Impact: -0.07)

1. **Deprecated ATT&CK technique IDs.** Three technique IDs in agent files use deprecated numbering from pre-v8 ATT&CK:
   - `red-lateral.md` line 129: `T1076` (Remote Desktop Protocol) -- should be `T1021.001`
   - `red-lateral.md` line 129: `T1028` (Windows Remote Management) -- should be `T1021.006`
   - `red-persist.md` line 134: `T1099` (Timestomp) -- should be `T1070.006`

   **Severity:** MEDIUM. R-018 requires "real offensive techniques." Using deprecated technique IDs reduces mapping accuracy and could confuse practitioners who reference current ATT&CK Navigator.

2. **Missing version citations for methodology standards.** PTES, OSSTMM, and OWASP Testing Guide are cited without version or date across all agents. While these standards do not have frequent versioned releases like OWASP ASVS, professional engagement methodology should cite the version used.

   **Severity:** LOW. Standards are correctly identified; version ambiguity is minor.

3. **Footer-only ADR traceability in agent files.** Agent body text does not cite specific ADR sections or architecture decisions inline. All traceability is concentrated in the footer line "SSOT: ADR-PROJ010-001, ADR-PROJ010-006". This is consistent with the exemplar (ps-researcher) but insufficient for a C4 deliverable where traceability carries 0.10 weight.

   **Severity:** LOW. Traceability exists but is not granular.

### Traceability Issues (Score Impact: -0.08)

4. **No inline references to AD-001 through AD-012 decisions in agent files.** The SKILL.md references AD-001 (Methodology-First Design) and AD-010 (Standalone Capable) by name, but agent files do not reference these architecture decisions inline despite implementing them directly.

   **Severity:** LOW. The design intent is implemented; the citation linkage is implicit.

5. **No references to A-004 roster recommendations.** Agent files do not reference the R-ROSTER recommendations that justified their existence (e.g., red-infra does not cite R-ROSTER-003 or R-ROSTER-012; red-social does not cite R-ROSTER-004).

   **Severity:** LOW. SKILL.md references A-004 but individual agents do not.

### Internal Consistency Issues (Score Impact: -0.04)

6. **Shared ATT&CK tactic IDs between agents.** red-recon and red-social share TA0043; red-exploit and red-social share TA0001. While documented and intentional (social vs. technical domains), this creates a potential routing ambiguity that the ADR-002 routing architecture must resolve. The SKILL.md acknowledges this in the Available Agents table but does not document the disambiguation explicitly within SKILL.md itself.

   **Severity:** LOW. Documented, intentional overlap with different technique subsets.

### Completeness Issues (Score Impact: -0.03)

7. **red-vuln has no explicit ATT&CK tactic assignment.** In the Available Agents table, red-vuln is listed as "Analysis support" rather than a tactic ID. While this is accurate per ADR-001 (vulnerability analysis spans the gap between reconnaissance and exploitation), it means one agent lacks a formal tactic assignment.

   **Severity:** LOW. Architecturally intentional per ADR-001.

---

## Strengths

### Architectural Strengths

1. **Comprehensive authorization architecture.** The three-layer defense-in-depth model (structural/dynamic/retrospective) is thoroughly documented in SKILL.md with specific enforcement components, YAML schema, and failure modes. This exceeds what the exemplar problem-solving skill provides for its domain.

2. **Consistent agent schema across all 11 files.** Every agent follows an identical structural pattern: YAML frontmatter (name, version, description, model, identity, persona, capabilities, guardrails, output, validation, portability) followed by markdown body (Identity, Methodology, Authorization & Scope, Workflow Integration, Output Requirements, Tool Integration, Safety Alignment, Constitutional Compliance). This consistency is excellent and surpasses the exemplar in uniformity.

3. **Non-linear workflow documentation.** The kill chain diagram, orchestration rules (7 rules), and phase cycling documentation are thorough and actionable. The explicit statement "The kill chain organizes capability, not workflow sequence" is a critical design insight that is well-communicated.

4. **Defense evasion distribution model.** The distributed ownership model with 6 owners and specific technique assignments per agent is well-documented in both SKILL.md (Defense Evasion Ownership table) and each owning agent (Defense Evasion Ownership section with specific ATT&CK techniques).

### Methodological Strengths

5. **Methodology-First Design consistency.** Every agent includes an "AD-001 Methodology-First Design" subsection in its Methodology section, consistently framing guidance within professional methodology rather than autonomous execution. This is rigorously applied across all 11 agents without exception.

6. **Safety Alignment Compatibility section.** SKILL.md dedicates a full section to safety alignment with a friction-point table identifying the 4 agents most likely to trigger safety classifiers (red-exploit, red-persist, red-social, red-exfil) with specific mitigations per agent.

7. **Three-level tool degradation.** Every agent documents Level 0 (Full Tools), Level 1 (Partial Tools), and Level 2 (Standalone) degradation with specific tools and uncertainty markers per level, implementing AD-010 thoroughly.

### Quality Strengths

8. **RoE-gating enforcement.** The three RoE-gated agents (red-persist, red-exfil, red-social) each declare their gating requirement in three places: YAML frontmatter guardrails (input_validation field), identity section (bold "RoE-GATED" notice), and methodology section (Step 1: RoE Authorization Verification). This triple enforcement is thorough.

9. **Cross-skill integration documentation.** Four integration points are documented with attribute tables (Source, Target, Data Exchanged, Value, Workflow) providing concrete operational detail for purple team scenarios.

10. **Scope document YAML schema.** The complete YAML schema in SKILL.md with all required fields (engagement_id, authorized_targets, technique_allowlist, time_window, exclusion_list, rules_of_engagement, agent_authorizations, evidence_handling, signature) provides a usable specification for implementation.

---

## Comparison with Exemplar

The /red-team SKILL.md (657 lines) is substantially more comprehensive than the exemplar /problem-solving SKILL.md (442 lines), which is appropriate given the authorization and safety requirements of offensive security operations. Key differences:

| Dimension | /problem-solving (exemplar) | /red-team (scored) | Assessment |
|-----------|---------------------------|-------------------|------------|
| Authorization section | None (not applicable) | Full 3-layer architecture with YAML schema | Exceeds exemplar (domain-appropriate) |
| Safety alignment | None (not applicable) | Dedicated section with friction-point analysis | Exceeds exemplar (domain-appropriate) |
| Circuit breaker | None | Full protocol with 6-step check sequence | Exceeds exemplar (domain-appropriate) |
| Agent count documentation | 9 agents in table | 11 agents in table with ATT&CK mappings | Exceeds exemplar |
| Workflow diagram | Sequential chain text example | ASCII diagram with non-linear flow | Exceeds exemplar |
| Triple-Lens audience | Present | Present | Matches exemplar |
| Quick Reference | Present | Present with agent selection hints and defense evasion table | Exceeds exemplar |

Agent files: red-lead (204 lines) vs. ps-researcher (615 lines). The exemplar ps-researcher uses XML tags in its body (`<agent>`, `<identity>`, `<capabilities>`, etc.) reflecting the older Anthropic-specific format, while /red-team agents use `body_format: markdown` per E-001 finding that XML is Anthropic-specific. The /red-team agents are more concise but cover all required sections. The exemplar includes session_context validation schema, Context7 integration protocol, and adversarial quality strategies sections that /red-team agents do not include -- however, these are /problem-solving-specific operational patterns, not requirements for /red-team agents.

---

## Recommendation

**PASS with advisory notes.** The deliverables meet the 0.95 threshold. Three advisory items for future iteration:

1. **Update deprecated ATT&CK technique IDs** (T1076, T1028, T1099) to current numbering in red-lateral.md and red-persist.md. This is the highest-priority correction.

2. **Add inline ADR decision references** in agent body text (e.g., "per AD-001," "per AD-010") to strengthen traceability from 0.92 to target 0.95+.

3. **Consider adding version citations** for PTES and OSSTMM where available to strengthen evidence quality.

---

*Quality Gate Report Version: 1.0.0*
*Scorer: adv-scorer (S-014 LLM-as-Judge)*
*Leniency Bias Counteraction: Active -- scored on what IS present, not what could be inferred*
*Report Generated: 2026-02-22*
