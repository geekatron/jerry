# C4 Adversarial Tournament Deep-Dive Analysis: PROJ-030-bugs

> Cross-strategy analysis of the 20-strategy C4 tournament (10 strategies x 2 reports).
> Baseline scores: Report 1 = 0.823, Report 2 = 0.837. C4 threshold: >= 0.95.
> Produced by: ps-synthesizer | Date: 2026-02-26

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language findings for non-technical stakeholders |
| [L1: Technical Synthesis](#l1-technical-synthesis) | Strategy ranking, agreement map, strategy interactions, novel insights |
| [L2: Strategic Synthesis](#l2-strategic-synthesis) | Quality gate analysis, tournament process observations, knowledge items |
| [Appendix A: Cross-Reference Matrix](#appendix-a-cross-reference-matrix) | Strategy-x-finding corroboration table |
| [Appendix B: Strategy Effectiveness Data](#appendix-b-strategy-effectiveness-data) | Quantitative finding breakdown per strategy |
| [Source Summary](#source-summary) | Documents synthesized with key contributions |

---

## L0: Executive Summary

The PROJ-030-bugs C4 tournament ran all 10 adversarial strategies against two research reports about a real bug in the Jerry framework: Context7, a library documentation tool, was installed as a Claude Code plugin instead of a standalone MCP server. This caused tool names to use a long plugin-qualified namespace that did not match what agent definitions expected, silently breaking tool access.

Both reports started below the 0.92 standard quality gate, let alone the 0.95 C4 threshold. The tournament's job was to find exactly what was missing and why.

**The single biggest finding, agreed upon by 8 of 10 strategies:** neither report could empirically verify its core claim. The plugin naming formula — the keystone fact that proves the namespace mismatch — was derived from GitHub bug reports filed by third-party users in mid-2025, not from actually running Claude Code in February 2026 and observing the tool names. The reports correctly acknowledged this in their Limitations sections, but every strategy that touched the evidence layer independently flagged this as a Critical or Major gap. Acknowledging a limitation in a footnote does not neutralize it as a quality gap.

**The second biggest finding, agreed upon by 4-5 strategies:** the recommended fix — "remove the plugin, add a standalone server" — was incomplete as written. It omitted: which specific agent definition files need updating, what to do if the migration fails, how other team members set up their machines, whether CI runners need separate configuration, and whether the fix is compatible with Jerry's worktree isolation architecture.

**The three strategies that produced the most unique value:** S-012 FMEA (found the highest-severity individual finding: the fix may fail silently in worktree contexts, RPN 504), S-013 Inversion (found that a key GitHub issue the reports relied on was ambiguously closed, undermining the diagnosis), and S-001 Red Team (found that following the migration steps exactly would produce a half-migrated broken state with no error signal).

S-003 Steelman played a different and essential role: it confirmed the core thesis is directionally correct. This allowed later strategies to focus their attacks on the actionability layer rather than the analytical foundation, reducing false-positive findings.

After applying the tournament's prioritized revision list, both reports are estimated to reach 0.93-0.96, clearing the C4 threshold.

---

## L1: Technical Synthesis

### 1. Strategy Effectiveness Ranking

Strategies are ranked by net unique value: novel findings, severity of those findings, and actionability, with deduction for findings that duplicated what other strategies already found.

| Rank | Strategy | Unique High-Value Findings | Primary Contribution Mode | R1 Findings | R2 Findings |
|------|----------|---------------------------|--------------------------|-------------|-------------|
| 1 | **S-012 FMEA** | FM-001 R2 worktree isolation (RPN 504), FM-002 R1 migration commands (RPN 378), FM-006 R1 trade-off lacks evaluation criteria (RPN 294), FM-015 R2 namespace winner rule undocumented (RPN 252) | Systematic element decomposition exposes gaps invisible to holistic reading | 38 (8C/14Maj/16Min) | 32 (9C/19Maj/4Min) |
| 2 | **S-013 Inversion** | IN-002 Issue #15145 NOT PLANNED misinterpreted, IN-007 SSE transport vs. npx not evaluated, IN-006 subagent inheritance rule contradicts adjacent access gap claim | Goal-reversal exposes assumptions the report never knew it was making | 10 (3C/8Maj/2Min) | 10 (2C/6Maj/2Min) |
| 3 | **S-001 Red Team** | RT-001 migration produces half-migrated broken state (specific failure mechanism), RT-002 Memory-Keeper used as unverified justification for Approach A, RT-006 character count actually measured (49, 43 chars) | Practitioner-persona attack reveals recommendations unsafe to follow verbatim | 9 (3C/4Maj/2Min) | 9 (2C/4Maj/2Min) |
| 4 | **S-004 Pre-Mortem** | PM-003 no affected-files inventory, PM-002 migration omits agent tools frontmatter step, acceptance criteria framing | Scenario-building exposes project-level scope completeness gaps | 12 (3C/5Maj/4Min) | 11 (3C/5Maj/3Min) |
| 5 | **S-003 Steelman** | SM-001 L0 omits agent-level breakage mechanism, SM-003 Formula B caveat must be in-section not only in Limitations | Confirms valid claims; allows later strategies to focus on substantive gaps; fulfills H-16 ordering requirement | 9 (1C/5Maj/3Min) | 8 (1C/3Maj/4Min) |
| 6 | **S-002 Devil's Advocate** | DA-001 foundational claim unverifiable — researcher had Permission Denied on the user settings file, DA-002 R2 recommendation introduces per-developer config divergence and SSE reliability risk | Most uncomfortable epistemological challenge: the starting condition itself was not verified | 8 (1C/4Maj/3Min) | 7 (2C/3Maj/2Min) |
| 7 | **S-010 Self-Refine** | SR-003 confidence 0.90 overstated given access limitations, SR-005 Formula B caveat absent from the Formula B section itself | Internal consistency lens catches structural mismatches (level count, wildcard contradiction) | 7 (0C/3Maj/4Min) | 8 (1C/4Maj/3Min) |
| 8 | **S-007 Constitutional AI** | Report 1 passed (0.96), Report 2 failed on traceability (0.83); identified inline citation gaps in L2 and 5W1H sections | Constitutional compliance gate; Report 2's unique traceability failure identified here | Pass/Fail + targeted findings | Pass/Fail + targeted findings |
| 9 | **S-014 LLM-as-Judge** | Dimension-level scoring establishing baseline; Methodological Rigor identified as weakest shared dimension (0.80/0.82) | Baseline establishment; dimension weights make the stakes of all other findings explicit | 0.823 baseline | 0.837 baseline |
| 10 | **S-011 Chain-of-Verify** | Wildcard contradiction (R2 corroboration), character count verification | Factual claim checking, but narrow scope; lowest unique finding contribution | 4 (0C/1Maj/3Min) | 3 (0C/1Maj/2Min) |

**Ranking observations:**

The structured decomposition family (S-012 FMEA, S-013 Inversion) produced the highest ratio of novel-to-redundant findings. Holistic reading produces findings about what is obviously missing; structured decomposition produces findings about what is subtly missing inside specific elements. The FMEA finding that the trade-off analysis lacks evaluation criteria (FM-006 R1, RPN 294) would not emerge from a holistic read, because holistic reading finds the four approaches and their pros/cons and calls them sufficient.

The role-based adversarial family (S-001, S-002, S-004) produced the highest Critical-percentage findings (approximately 40% of their findings were Critical vs. 30% for the structured decomposition family and 6% for the self-correction family). Role-based strategies are best at finding actionability gaps because the persona framing ("a practitioner will follow this verbatim") naturally evaluates the migration path, not the analytical section.

---

### 2. Cross-Strategy Agreement Map

Findings corroborated by 3+ independent strategies are high-confidence revision targets. Agreement count correlates with confidence and with which quality gate dimension is most affected.

#### VERY HIGH Confidence (8 strategies): No Empirical Runtime Verification

**Corroborated by:** S-001 (both reports), S-002 (both), S-003 (both), S-004 (both), S-010 (R1), S-012 (both), S-013 (both), S-014 (both)
**Report coverage:** Both reports

Both reports acknowledged in their Limitations sections that runtime behavior was not empirically verified. The core claim — that the plugin namespace is `mcp__plugin_context7_context7__` — was derived from GitHub bug reports filed by third-party users in mid-2025, not from running `claude mcp list` or `/mcp` in February 2026.

Eight strategies flagged this independently because the gap affects five different evaluation lenses: Missing (the verification is absent), Insufficient (the Limitations acknowledgment is buried), Ambiguous (the claims are presented as current facts not historical observations), Incorrect (the claims may be wrong if Claude Code changed the naming), and Temporal (mid-2025 to Feb 2026 covers multiple Claude Code releases).

**Primary dimension impact:** Methodological Rigor (0.20 weight), Evidence Quality (0.15 weight), Completeness (0.20 weight)

---

#### HIGH Confidence (6-7 strategies): Formula B Sourced from Bug Reports, Cited as HIGH Credibility

**Corroborated by:** S-001 RT-003 (R1), S-002, S-003 SM-003, S-004 PM-004, S-010 SR-005, S-013 IN-001, S-014 Evidence Quality
**Report coverage:** Both reports (7 strategies R1; 6 strategies R2)

The Methodology table rated GitHub Issues #23149 and #15145 as HIGH credibility. The Limitations section correctly noted these are bug reports, not official specification. This creates an internal signal mismatch: a practitioner reading the Methodology table believes they are seeing primary-source evidence; a practitioner reading Limitations finds the qualification. S-001 Red Team made the sharpest observation: the credibility rating should be "HIGH for the specific behavior observed; MEDIUM for generalizability across Claude Code versions."

Multiple strategies also noted the in-section absence of the version caveat. The Formula B formula appears prominently in Section 1 and in the tool naming rules table. The caveat is only in the Limitations section. A practitioner who reads Section 1 and implements based on it will miss the qualification.

**Primary dimension impact:** Evidence Quality (0.15 weight), Methodological Rigor (0.20 weight)

---

#### HIGH Confidence (5 strategies): Missing Agent Impact Inventory (Report 1)

**Corroborated by:** S-001 R1 RT-005, S-003 R1 SM-002, S-004 R1 PM-003, S-012 R1 FM-005 (RPN 336), S-013 R1 IN-003/IN-004
**Report coverage:** Report 1

Report 1 identifies that agent definitions reference wrong Context7 tool names but does not enumerate which agents or how many files are affected. The `mcp-tool-standards.md` Agent Integration Matrix lists 28 agent categories with Context7 access, but neither the category count from documentation nor a codebase search of actual agent definition files (`skills/*/agents/*.md`) was included.

All five strategies converged on the same concrete fix: run `grep -r "mcp__context7__" skills/*/agents/*.md` and list the results. This is a one-command audit that would convert a qualitative scope claim into a verified quantitative one.

**Primary dimension impact:** Completeness (0.20 weight), Actionability (0.15 weight)

---

#### HIGH Confidence (5 strategies): Migration Path Incomplete (Report 1)

**Corroborated by:** S-001 R1 RT-001, S-004 R1 PM-002, S-013 R1 IN-005, S-012 R1 FM-002 (RPN 378), S-003 R1 SM-001/SM-002
**Report coverage:** Report 1

The 3-step migration path omits: (a) updating agent `tools` frontmatter, (b) updating `mcpServers` frontmatter in agent definitions, (c) updating `TOOL_REGISTRY.yaml`, (d) verification acceptance criteria, (e) rollback plan.

S-001 Red Team added the most acute observation about the mechanism of failure: if the practitioner simplifies `settings.local.json` before the plugin is fully removed, the plugin MCP server may still register tools under `mcp__plugin_context7_context7__` alongside the new standalone server tools. Permission rules for `mcp__context7__*` would cover the standalone server but not the plugin-namespace tools. The result is a half-migrated state where some invocations succeed and others silently fail — with no error message. S-012 FMEA added that the migration commands use `npx -y` without version pinning (RPN 378), making the migration non-reproducible.

**Primary dimension impact:** Actionability (0.15 weight)

---

#### HIGH Confidence (4 strategies): Memory-Keeper Analysis Omitted

**Corroborated by:** S-001 R1 RT-002, S-001 R2 RT-002, S-010 R1 SR-007, S-003 R2 (noted)
**Report coverage:** Both reports

Both reports acknowledge that Memory-Keeper is configured as a standalone MCP server. However, neither report verifies this claim. The Methodology sections note that `~/.claude/settings.json` was inaccessible (Permission Denied), so the user-level configuration of Memory-Keeper was not observed.

S-001 Red Team identified the sharpest consequence: Report 1 uses "consistent with how Memory-Keeper is configured" as a positive justification for Approach A — making the recommendation partially rest on an unverified assumption about a component that was not examined.

**Primary dimension impact:** Completeness (0.20 weight), Internal Consistency (0.20 weight)

---

#### HIGH Confidence (4 strategies): Wildcard Syntax Internal Contradiction (Report 2)

**Corroborated by:** S-001 R2 RT-003, S-010 R2, S-011 R2, S-013 IN-008
**Report coverage:** Report 2

Report 2 presents contradictory information about wildcard permission syntax: one section cites Issue #3107 where an Anthropic engineer stated "Permission rules do not support wildcards," while the recommendations section accepts wildcard entries as valid.

S-013 Inversion made the sharpest distinction: if wildcards do not work, then the `settings.local.json` entries using `mcp__context7__*` are not granting wildcard permission — only the explicitly listed tool names below them are active. This changes the semantics of the recommended permission simplification: `mcp__context7` (server-level, confirmed to work) is the only safe simplification, not `mcp__context7__*` (possibly inoperative wildcard).

**Primary dimension impact:** Internal Consistency (0.20 weight)

---

#### HIGH Confidence (4 strategies): User-Scope Deployment Gaps (Report 2)

**Corroborated by:** S-001 R2 RT-005, S-004 R2, S-012 R2 FM-007 (RPN 392) / FM-001 (RPN 504), S-013 R2 IN-005
**Report coverage:** Report 2

The recommendation to use `claude mcp add --scope user` makes Context7 available globally to all Claude Code projects on the developer's machine. The report does not address: (a) other team members need to run the command individually, (b) CI runners have no `~/.claude.json` and cannot run the command, (c) worktree contexts may not inherit user-scoped MCP configuration.

S-012 FMEA produced the highest-RPN single finding of the entire tournament for the worktree gap (FM-001 R2, RPN 504 — severity 9, occurrence 7, detectability 8). The recommendation was not validated against Jerry's worktree isolation architecture (`.claude/worktrees/`). If worktree contexts do not inherit user-scoped MCP servers, the fix works in the main repo and fails in worktrees — a silent regression in the most common Jerry development workflow.

**Primary dimension impact:** Completeness (0.20 weight), Actionability (0.15 weight)

---

#### MEDIUM Confidence (3 strategies): `allowed_tools` Field Unresolved (Report 1)

**Corroborated by:** S-001 R1 RT-007, S-010 R1 SR-003, S-014 Internal Consistency
**Report coverage:** Report 1

`.claude/settings.json` uses an `allowed_tools` field that "appears to be a legacy or custom field." The standard Claude Code schema uses `permissions.allow` and `permissions.deny`. Whether `allowed_tools` is honored, deprecated, or silently ignored is never resolved, leaving the shared project permission layer in an ambiguous state.

**Primary dimension impact:** Internal Consistency (0.20 weight)

---

### 3. Strategy Interaction Patterns

#### Complementary Interactions

**S-003 Steelman enabled S-001, S-002, S-004 to produce higher-precision findings (H-16 effect)**

H-16 (Steelman before critique) had a documented and measurable effect on this tournament. S-001 Red Team was executed twice: once before S-003 (H-16 violation, logged as RT-000), and once after. The pre-S-003 execution attacked both analytical weaknesses and actionability gaps. The post-S-003 execution operated against a strengthened deliverable and focused its attacks on the actionability layer — where the real gaps were — rather than spending findings on framing issues the Steelman had already addressed.

S-002 Devil's Advocate explicitly halted and waited for S-003 before proceeding. This produced a cleaner challenge: the Devil's Advocate attacked from a position of maximum charitable interpretation, finding the most uncomfortable epistemological gap (DA-001: the foundational premise could not be verified due to Permission Denied on the user settings file). Without the Steelman grounding, DA-001 would likely have been diluted by lower-quality challenges to valid claims.

**Interaction conclusion:** H-16 reduced false-positive rate in role-based adversarial strategies. The Steelman pass changed the attack surface from "everything including valid claims" to "only genuine gaps."

---

**S-012 FMEA + S-013 Inversion cross-validated each other's highest-severity findings**

The structured decomposition family attacked from opposite directions: FMEA asked "for each element, what could go wrong?" while Inversion asked "for each goal, what would failure look like?" Both converged independently on the empirical verification gap, the wildcard contradiction (R2), and the agent impact count being unverified (R1/R2). Because these were found by two structurally different methodologies, the findings have high confidence regardless of source count.

FMEA additionally found element-level gaps invisible to Inversion (navigation table ordering, PS integration metadata, character count arithmetic). Inversion additionally found assumption-level gaps invisible to FMEA (Issue #15145 NOT PLANNED ambiguity, SSE transport assumption, subagent inheritance tension). Together they form a near-complete coverage of the document's surface area.

---

**S-014 LLM-as-Judge scores anchored all other strategies' severity assessments**

The dimension weights (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10) functioned as a forcing function for the other nine strategies. When S-012 FMEA found the trade-off analysis lacked evaluation criteria (FM-006 R1, RPN 294), that finding mapped directly to Methodological Rigor — the weakest dimension. When S-007 Constitutional found Report 2 had inline citation gaps, that mapped to Traceability — the weakest R2 dimension. Without S-014's baseline, other strategies would have difficulty calibrating which findings most affected the quality gate.

---

#### Conflicting Interactions

**S-003 Steelman vs. S-001 Red Team: severity of migration guidance**

S-003 graded the migration guidance as "broadly correct with gaps." S-001 graded the same migration guidance as Critical (RT-001, P0 finding). The delta reflects different evaluation frames: S-003 evaluated analytical soundness; S-001 evaluated practitioner safety. For a C4 deliverable intended to drive infrastructure changes, the S-001 framing is correct. A C4 deliverable must have verified, actionable migration guidance. S-003's more lenient assessment was appropriate for the steelman role (strengthening the argument) but should not be read as endorsing the migration guidance as implementation-ready.

---

**S-014 LLM-as-Judge vs. S-007 Constitutional AI: scoring divergence on Report 1**

S-007 gave Report 1 a 0.96 PASS. S-014 gave Report 1 a 0.823 REVISE. The divergence reflects structurally different evaluation targets. S-007 checks constitutional compliance (P-003, P-020, P-022, governance adherence, traceability of claims to governance files). S-014 checks quality dimensions (completeness, rigor, evidence quality, actionability). A report can pass constitutional review while failing evidence quality — which is exactly what happened with Report 1. The tournament uses both correctly: S-007 as a constitutional gate and S-014 as a quality gate. Neither score alone is sufficient.

---

**S-011 Chain-of-Verify vs. broader tournament: low unique finding contribution**

S-011 Chain-of-Verify had the lowest unique finding contribution of any strategy: 4 findings (R1) and 3 findings (R2), all corroborating findings already surfaced by S-010 or S-013. The sequential factual verification approach is narrow: it checks whether specific claims are factually accurate, but does not expose structural gaps, reasoning failures, or recommendation completeness issues. At C4, where structural and reasoning gaps dominate, S-011 adds verification confidence but rarely unique insights. In future C4 tournaments against research reports (rather than code or architecture documents), S-011 could be replaced by a more differentiated strategy.

---

### 4. Novel Insights by Strategy

Findings that emerged exclusively from one strategy and were not corroborated by any other before their discovery.

| Finding | Strategy | Report | Why Novel |
|---------|----------|--------|-----------|
| **Worktree isolation incompatibility** (FM-001 R2, RPN 504) | S-012 FMEA | R2 | Only strategy to test the recommendation against Jerry's specific worktree architecture. No other strategy raised this; FMEA found it by examining the "Recommended Architecture" element against all of the element's known environment constraints. Highest single RPN in the tournament. |
| **Half-migrated broken state mechanism** (RT-001) | S-001 Red Team | R1 | Other strategies noted the migration was incomplete. S-001 uniquely identified the specific failure mechanism: plugin still active + permissions simplified = namespace collision with no error signal. The practitioner-persona framing made this obvious: "what happens if I follow these steps exactly?" |
| **Issue #15145 NOT PLANNED ambiguity** (IN-002) | S-013 Inversion | R2 | No other strategy questioned the interpretation of "NOT PLANNED" as "bug persists." Inversion found this by inverting the assumption that closed issues accurately reflect current behavior. The specific gap: Issue #20830 (of which #20983 is a duplicate) was not investigated; its resolution may confirm the bug was addressed differently. |
| **Character count actually measured** (RT-006) | S-001 Red Team | R1 | Other strategies noted the 64-character risk was unverified. S-001 uniquely performed the calculation: `mcp__plugin_context7_context7__resolve-library-id` = 49 chars, `mcp__plugin_context7_context7__query-docs` = 43 chars. The risk is real in principle but not for current tools. A future tool with a 20+ character name would exceed the limit. |
| **SSE transport vs. npx not evaluated** (IN-007) | S-013 Inversion | R2 | Inversion found this by inverting the recommendation's transport assumption. SSE transport depends on Upstash-hosted endpoint availability; npx runs a local process. No other strategy identified the transport choice as an unanalyzed assumption with meaningful consequences for reliability. |
| **Memory-Keeper used as active justification** (RT-002) | S-001 Red Team | R1 | Multiple strategies noted Memory-Keeper was unanalyzed. S-001 uniquely identified the consequence: Report 1 uses "consistent with Memory-Keeper" as positive justification for Approach A — so the recommendation partially rests on an unverified assumption. The gap is not merely omission; it is an omission that undermines the recommendation's rationale. |
| **Trade-off analysis lacks evaluation matrix** (FM-006 R1, RPN 294) | S-012 FMEA | R1 | No other strategy specifically identified the absence of a reproducible decision framework. FMEA found this by examining the Trade-Off Analysis element and applying the Missing lens: the recommendation cannot be derived from the trade-off table alone because there are no evaluation dimensions, weights, or scores. The conclusion ("Approach A is best") is asserted rather than demonstrated. |
| **Namespace winner rule undocumented** (FM-015 R2, RPN 252) | S-012 FMEA | R2 | When plugin and standalone registrations both exist, which one wins? Load order? Last-wins? No strategy other than FMEA examined this element-level gap. The "Dual-Registration Anti-Pattern" section claims "depending on which registration wins at runtime" without documenting how the winner is determined. |
| **L0 omits stakeholder action directive** (FM-001 R1, RPN 336) | S-012 FMEA (and S-003) | R1 | S-012 FMEA and S-003 Steelman both found this, but S-012 gave it Critical status. A stakeholder reading only L0 receives a problem description with no recommended action or decision owner. S-012 uniquely quantified the gap as RPN 336 and specified the fix: a bolded "Recommended Action" sentence naming the decision owner (ps-architect). |
| **Subagent inheritance contradicts access gap claim** (IN-006) | S-013 Inversion | R2 | Inversion found an internal tension within the same section: the tool inheritance table says "tools field omitted = subagent inherits ALL tools from main thread, including MCP tools," while the immediately adjacent text says "Custom subagents CANNOT access project-scoped MCP servers." These are presented as co-equal facts without reconciling the tension. The access gap may only apply to agents with explicit `tools` fields. |

---

## L2: Strategic Synthesis

### 5. Quality Gate Analysis

#### Dimensional Baseline

| Dimension | Weight | R1 Score | R1 Weighted | R2 Score | R2 Weighted |
|-----------|--------|----------|-------------|----------|-------------|
| Completeness | 0.20 | 0.82 | 0.164 | 0.87 | 0.174 |
| Internal Consistency | 0.20 | 0.88 | 0.176 | 0.88 | 0.176 |
| Methodological Rigor | 0.20 | 0.80 | 0.160 | 0.82 | 0.164 |
| Evidence Quality | 0.15 | 0.80 | 0.120 | 0.81 | 0.122 |
| Actionability | 0.15 | 0.82 | 0.123 | 0.84 | 0.126 |
| Traceability | 0.10 | 0.80 | 0.080 | 0.75 | 0.075 |
| **TOTAL** | | **0.823** | | **0.837** | |

#### Gap to 0.95 Threshold

R1 needs +0.127; R2 needs +0.113. These are substantial gaps. To reach 0.95, every dimension must improve, and the three highest-weight dimensions (each 0.20) must reach approximately 0.92-0.95.

#### Findings-to-Dimension Mapping

The tournament findings map directly to the weakest dimensions:

**Methodological Rigor (weakest at 0.80/0.82) — highest leverage, highest weight:**

- Empirical verification gap (8-strategy convergence): directly suppresses Methodological Rigor. Adding a "Verify First" Step 0 with `/mcp` inspection command moves this dimension.
- Trade-off analysis lacks evaluation matrix (FM-006 R1, RPN 294): FMEA's unique finding. A reproducible decision framework (named dimensions, scored options) converts an asserted recommendation into a demonstrated one.
- Migration commands unpinned and unverified (FM-002 R1, RPN 378): highest single RPN in R1. Version-pinning and a verification step are both Methodological Rigor items.

Estimated dimension improvement from Priority 1 + migration actions: 0.80 → 0.88-0.92

**Completeness (0.82 R1, 0.87 R2) — joint-highest weight:**

- Affected files inventory absent (5-strategy convergence R1): one grep command would provide the list. The impact claim is currently qualitative; the list makes it quantitative and actionable.
- Memory-Keeper scoping (4-strategy convergence, both reports): either verify it or explicitly scope it out. Either way resolves the gap.
- Deployment considerations missing (4-strategy convergence R2): team onboarding, CI runners, worktree isolation (FM-001 R2, RPN 504).

Estimated dimension improvement: R1: 0.82 → 0.90-0.93; R2: 0.87 → 0.92-0.95

**Evidence Quality (0.80/0.81):**

- Formula B version caveat (6-7-strategy convergence): "empirically observed from v1.0.x GitHub issues, verify on major upgrades" must appear in the Formula B section itself, not only in Limitations.
- Issue #15145 ambiguity (S-013 IN-002, R2): investigate #20830 resolution; qualify the "bug still present" framing.

Estimated dimension improvement: 0.80 → 0.86-0.90

**Traceability (R2 weakest at 0.75):**

- Inline citations absent from L2 and 5W1H sections (S-007 Constitutional finding): low-effort fix, high impact on this dimension.
- Timeline causality unsupported by git log or changelog (S-014 R2 finding).

Estimated dimension improvement: 0.75 → 0.88-0.92

**Internal Consistency (strongest at 0.88/0.88):**

- Level count mismatch — "four levels" stated, five enumerated (FM-004 R1, RPN 280): trivial fix.
- Wildcard syntax contradiction (4-strategy convergence R2): commit to one authoritative position with version-specific evidence.
- `allowed_tools` field unresolved (3-strategy convergence R1): either confirm functional or confirm ignored.

Estimated dimension improvement: 0.88 → 0.93-0.96

**Actionability (0.82/0.84):**

- Migration path completeness (5-strategy convergence R1): verified migration path with rollback, acceptance criteria, team onboarding note.
- User-scope deployment gaps (4-strategy convergence R2): deployment considerations section addressing team scale, CI runners, worktree isolation.

Estimated dimension improvement: R1: 0.82 → 0.90-0.93; R2: 0.84 → 0.91-0.94

#### Post-Revision Score Trajectory

| Report | Current | After Priority 1 Only | After Priority 1+2/3 | Reach 0.95? |
|--------|---------|----------------------|----------------------|-------------|
| R1 | 0.823 | ~0.87-0.89 | ~0.93-0.95 | Yes (with Priority 1+2 complete) |
| R2 | 0.837 | ~0.89-0.91 | ~0.93-0.96 | Yes (with Priority 1+3 complete) |

Both reports require Priority 1 actions plus their respective Priority 2 or 3 actions to reach 0.95. Priority 1 alone is not sufficient for either report.

---

### 6. Tournament Process Observations

#### Strategy Family Effectiveness Patterns

**Structured Decomposition Family (S-012 FMEA, S-013 Inversion): highest unique value**

These two strategies produced the highest ratio of novel-to-redundant findings. FMEA's element-by-element decomposition forced examination of every section including minor structural elements (navigation table ordering, PS integration metadata, character count arithmetic) that holistic reading skips. Inversion's goal-reversal forced the question "what would failure look like for each purpose this document serves?" — exposing assumptions the document never acknowledged making.

The FMEA finding count (38 R1, 32 R2) was the highest of any strategy, but volume is not the right metric. The critical observation is finding quality: FMEA found the highest-severity isolated finding (FM-001 R2, RPN 504: worktree isolation), the highest-RPN R1 finding (FM-002, RPN 378: migration commands), and the finding that no other strategy found (FM-006: trade-off analysis lacks reproducible decision framework). Inversion found the most uncomfortable evidence interpretation gap (IN-002: NOT PLANNED ambiguity) and the most operational oversight (IN-007: transport choice not evaluated).

**Recommendation for future C4 tournaments:** Schedule FMEA and Inversion before role-based strategies. Their element-level and assumption-level findings inform which sections the Red Team and Pre-Mortem should attack most aggressively.

---

**Role-Based Adversarial Family (S-001, S-002, S-004): highest Critical percentage, strongest on actionability**

This family's practitioner-persona framing ("a developer will follow this verbatim") naturally converged on actionability gaps — the migration path, the deployment considerations, the team-scale implications. S-001 Red Team had the highest Critical-to-total ratio (3 Critical out of 9 total = 33%) and found the mechanism of failure for an incomplete migration (RT-001), not just the fact of incompleteness.

S-002 Devil's Advocate found the most epistemologically uncomfortable challenge: the foundational claim (Context7 is installed plugin-only) could not be verified because `~/.claude/settings.json` returned Permission Denied. This is a gap that no amount of document analysis can address — it requires either gaining access to the user-level settings or using a different verification method (`claude mcp list`). S-002 also uniquely identified that the recommended fix introduces per-developer configuration divergence and loses Claude Code plugin auto-update behavior.

S-004 Pre-Mortem overlapped significantly with S-001 in both reports. In future C4 tournaments at this scope, S-004 could be replaced by a more differentiated strategy or scoped to a specific failure scenario not already covered by S-001 and S-013.

---

**Iterative Self-Correction Family (S-007, S-010, S-011): efficient but not differentiating**

S-007 Constitutional AI was unique in one respect: it was the only strategy whose primary output for one report was a passing grade (R1: 0.96 PASS). This confirmed that Report 1 meets constitutional constraints while failing quality dimensions — useful information for revising strategy. It also uniquely identified Report 2's traceability failures (inline citations absent from L2 and 5W1H sections).

S-010 Self-Refine found internal consistency issues (level count, confidence overstated, wildcard contradiction) that were all correct and all corroborated by other strategies. Its value was verification rather than discovery.

S-011 Chain-of-Verify had the lowest unique finding contribution of any strategy in this tournament. Sequential factual verification is well-suited to documents with many quantitative claims; research reports with qualitative analytical sections and recommendation completeness gaps are not its best application domain.

---

#### H-16 Ordering: Documented Tournament Effect

H-16 (Steelman before Devil's Advocate/Red Team) produced three concrete documented effects in this tournament:

1. **S-001 Red Team ran before S-003 (H-16 violation).** S-001 itself logged this as Critical process finding RT-000. The violation was noted and S-001 proceeded against the un-Steelmanned deliverable, explicitly flagging that its findings should be treated as provisional until S-003 was complete. The pre-S-003 S-001 findings were directionally correct but included broader attacks on the analytical framing.

2. **S-002 Devil's Advocate halted and waited for S-003.** This was the correct H-16 implementation. The resulting S-002 operated from maximum charitable interpretation and found the most uncomfortable epistemological gap (DA-001) rather than spending findings on framing issues.

3. **Post-S-003 strategies were more precise.** Strategies run after S-003 had the Steelman's confirmation that the core thesis was sound. This focused their attacks on the actionability and evidence layers, where the real C4 gaps existed.

**Process conclusion:** H-16 is not merely procedural. The Steelman pass changes the attack surface for subsequent strategies. Strategies run before Steelman have higher finding volume but higher false-positive rates. H-16 enforcement improves precision at the cost of one additional strategy execution.

---

#### Cross-Report Consistency

Eight of the eight convergence themes were shared across both reports (or were specifically identified as single-report issues where the other report was structurally different). Both reports shared the same fundamental weaknesses — empirical verification, Formula B sourcing — despite covering different technical content. This indicates that the weaknesses are research-methodology-level, not topic-specific.

**Strategic implication:** The Priority 1 revision actions improve both reports because they address the methodology, not the content. A methodology improvement (adding a "Verify First" step, adding Formula B version caveats) propagates across all downstream claims that depend on the same methodology. Conversely, Priority 2/3 actions are report-specific because they address content gaps unique to each report's scope.

---

### Knowledge Items Generated

#### PAT-001: Structured Decomposition Strategies for C4 Research Report Quality

```markdown
### PAT-001: Structured Decomposition Strategies First in C4 Tournament Sequencing

**Context:** C4 adversarial tournament against research reports where a holistic baseline
score (S-014) has already been established and dimension-level weaknesses are known.
**Problem:** Role-based adversarial strategies (Red Team, Pre-Mortem) attack the document
holistically and miss gaps embedded within specific subsections. Holistic reading produces
findings about what is obviously missing; structured decomposition produces findings about
what is subtly missing inside each element.
**Solution:** Schedule S-012 FMEA and S-013 Inversion before role-based strategies.
FMEA's element decomposition and Inversion's goal-reversal together cover the document's
surface area more completely than holistic reading, and their findings inform which sections
the Red Team and Pre-Mortem should attack most aggressively.
**Consequences:** (+) Highest novel finding rate; finds element-level gaps invisible to
holistic review. (+) FMEA's RPN quantification provides an objective severity ranking.
(-) Highest finding volume; requires triage effort to separate Critical from Minor findings.
(-) Adds one additional scheduling dependency (FMEA and Inversion should precede
role-based strategies).
**Quality:** HIGH — FMEA produced the highest single-finding RPN (504) and most Critical
findings; Inversion produced the most novel insights per finding. Both independently
corroborated the same highest-confidence convergence themes.
**Sources:** report1-s012-fmea.md, report2-s012-fmea.md, report2-s013-inversion.md,
c4-tournament-synthesis.md
```

#### PAT-002: H-16 Steelman-First Reduces Role-Based Adversarial False-Positive Rate

```markdown
### PAT-002: H-16 Steelman-First Ordering Reduces Red Team False Positive Rate

**Context:** C4 tournament where S-001 Red Team is required and may run before S-003.
**Problem:** Red Team run against a weakly-framed document attacks framing weaknesses
and analytical gaps simultaneously. Some framing weaknesses would be preemptively
addressed by a Steelman pass, inflating the Red Team's finding count with false-positives
(findings that correctly identify a weakness but would have been addressed by the
Steelman anyway, and thus are not substantive gaps in the analysis).
**Solution:** Enforce H-16 strictly: run S-003 Steelman before S-001. When S-001 runs
before S-003 (violation), log it as a process finding (RT-000 pattern), treat findings as
provisional, and re-run S-001 after S-003 completes. S-002 Devil's Advocate should
explicitly halt and wait for S-003 before proceeding.
**Consequences:** (+) Red Team findings are more precise — they attack only gaps that
survive the Steelman pass. (+) Devil's Advocate from maximum charitable interpretation
finds more uncomfortable epistemological gaps. (-) One additional strategy execution
added to tournament timeline if S-001 violation occurred. (-) If H-16 is violated, the
provisional S-001 findings require a second pass to validate.
**Quality:** HIGH — RT-000 violation documented in this tournament; post-S-003 S-001
demonstrably more focused than pre-S-003 execution; S-002 halt-and-wait produced
cleaner findings.
**Sources:** report1-s001-red-team.md RT-000, c4-tournament-synthesis.md H-16 row
```

#### LES-001: Acknowledging a Limitation in Methodology Does Not Neutralize It as a Quality Gap

```markdown
### LES-001: Limitations Acknowledged but Not Mitigated Still Fail Quality Review

**Context:** Research reports on runtime behavior of external systems where direct
verification access is limited (e.g., user-level settings returned Permission Denied,
live Claude Code session not available during research).
**What Happened:** Both reports acknowledged in their Limitations sections that runtime
behavior was not empirically verified. Despite the explicit acknowledgment, eight of ten
adversarial strategies independently flagged this as a Critical or Major quality gap.
The acknowledgment in the Limitations section did not prevent it from being found as
a gap — it was the gap.
**What We Learned:** Acknowledging a limitation does not immunize a deliverable from
that limitation suppressing quality scores. The gap must be either (a) resolved by
doing the verification, or (b) prominently labelled as a known risk in the sections that
make claims depending on the unverified data — not only in the Limitations section.
**Prevention:** For any deliverable making claims about runtime behavior that could not
be observed: (1) Add an explicit "Verify First" step as Step 0 in recommendations.
(2) Add a temporal limitation warning to the L0 summary (not only to Methodology).
(3) Label claims sourced from unverified data with an inline caveat in the section where
the claim appears, not only in the Limitations section.
(4) Distinguish between "we acknowledge we could not verify X" and "we took alternative
steps to verify X via Y method" — the latter is the required standard for C4 evidence quality.
**Sources:** c4-tournament-synthesis.md Convergence Theme 1, report1-s001-red-team.md,
report2-s013-inversion.md IN-001/IN-002, report1-s012-fmea.md FM-007
```

#### ASM-001: Closed GitHub Issues Accurately Represent Current Claude Code Runtime Behavior

```markdown
### ASM-001: Mid-2025 GitHub Issue Observations Assumed Current in February 2026

**Context:** Implicitly assumed by both research reports when deriving the plugin naming
formula and interpreting Issue #15145 closure status. The formula `mcp__plugin_context7_
context7__resolve-library-id` is presented as current fact without verification.
**Impact if Wrong:** The core diagnosis (dual-namespace collision is currently active,
plugin prefix is `mcp__plugin_context7_context7__`) could be incorrect for current Claude
Code. The fix recommendation remains architecturally valid as a simplification, but the
urgency framing changes if the underlying bug was already resolved in a Claude Code
update between mid-2025 and February 2026.
**Confidence:** LOW — S-013 IN-001 and IN-002 directly stress-tested this assumption
and found it unverified. Issue #15145 "NOT PLANNED" could mean the bug was addressed
through a different mechanism. Issue #20830 (the duplicate of #20983) was not investigated
and its resolution may confirm the bug was resolved differently.
**Validation Path:** (1) Run `/mcp` in Claude Code with Context7 installed as a plugin;
capture actual tool names and compare against the documented formula. (2) Investigate
Issue #20830 to understand its resolution status. (3) Check Claude Code release notes
between mid-2025 and February 2026 for plugin MCP naming changes.
**Sources:** report2-s013-inversion.md IN-001, IN-002, c4-tournament-synthesis.md
Convergence Theme 2, report1-s001-red-team.md RT-003
```

---

## Appendix A: Cross-Reference Matrix

Strategies as columns; convergence themes as rows. X = strategy corroborated the finding independently.

| Finding Theme | S-001 | S-002 | S-003 | S-004 | S-007 | S-010 | S-011 | S-012 | S-013 | S-014 | Count |
|---------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| No empirical runtime verification (both) | X | X | X | X | — | X | — | X | X | X | **8** |
| Formula B from bug reports not spec (both) | X | X | X | X | — | X | — | X | X | X | **8** |
| Agent impact inventory absent (R1) | X | — | X | X | — | — | — | X | X | — | **5** |
| Migration path incomplete (R1) | X | — | X | X | — | — | — | X | X | — | **5** |
| Memory-Keeper analysis omitted (both) | X | — | X | — | — | X | — | — | — | — | **3** |
| Wildcard syntax contradiction (R2) | X | — | — | — | — | X | X | X | X | — | **4** |
| User-scope deployment gaps (R2) | X | — | — | X | — | — | — | X | X | — | **4** |
| `allowed_tools` field unresolved (R1) | X | — | — | — | — | X | — | — | — | X | **3** |
| Worktree isolation incompatibility (R2) | — | — | — | — | — | — | — | X | — | — | **1** |
| Issue #15145 NOT PLANNED ambiguous (R2) | X | — | — | — | — | — | — | — | X | — | **2** |
| SSE vs. npx transport not evaluated (R2) | — | X | — | — | — | — | — | — | X | — | **2** |
| Namespace winner rule undocumented (R2) | — | — | — | — | — | — | — | X | — | — | **1** |
| Trade-off lacks evaluation matrix (R1) | — | — | — | — | — | — | — | X | — | — | **1** |
| Half-migrated broken state mechanism (R1) | X | — | — | — | — | — | — | — | — | — | **1** |

---

## Appendix B: Strategy Effectiveness Data

| Strategy | R1 Findings (C/Maj/Min) | R2 Findings (C/Maj/Min) | Unique Novel Findings (count) | Critical % (both reports) |
|----------|------------------------|------------------------|-------------------------------|---------------------------|
| S-012 FMEA | 8C / 14Maj / 16Min | 9C / 19Maj / 4Min | 5 | 24.3% |
| S-013 Inversion | 3C / 8Maj / 2Min | 2C / 6Maj / 2Min | 5 | 23.8% |
| S-001 Red Team | 3C / 4Maj / 2Min | 2C / 4Maj / 2Min | 4 | 31.3% |
| S-004 Pre-Mortem | 3C / 5Maj / 4Min | 3C / 5Maj / 3Min | 1 | 26.1% |
| S-003 Steelman | 1C / 5Maj / 3Min | 1C / 3Maj / 4Min | 1 | 11.8% |
| S-002 Devil's Advocate | 1C / 4Maj / 3Min | 2C / 3Maj / 2Min | 2 | 20.0% |
| S-010 Self-Refine | 0C / 3Maj / 4Min | 1C / 4Maj / 3Min | 1 | 6.7% |
| S-007 Constitutional | PASS 0.96 | REVISE 0.83 | 1 | N/A |
| S-014 LLM-as-Judge | 0.823 composite | 0.837 composite | 0 | N/A |
| S-011 Chain-of-Verify | 0C / 1Maj / 3Min | 0C / 1Maj / 2Min | 0 | 0% |

---

## Source Summary

| Source | Type | Key Contribution | Knowledge Items |
|--------|------|------------------|-----------------|
| `c4-tournament-synthesis.md` | Tournament Synthesis | All 8 convergence themes, baseline scores, revision priority list, H-16 compliance record | Primary input; all themes |
| `report1-s012-fmea.md` | Strategy Report (FMEA, R1) | 38 findings, RPN 6,546; FM-002 highest R1 RPN (378); FM-006 unique trade-off matrix gap | PAT-001, LES-001 |
| `report2-s012-fmea.md` | Strategy Report (FMEA, R2) | 32 findings, RPN 5,334; FM-001 highest tournament RPN (504, worktree isolation) | PAT-001, worktree novel finding |
| `report1-s001-red-team.md` | Strategy Report (Red Team, R1) | H-16 violation (RT-000); half-migrated state mechanism (RT-001); Memory-Keeper justification misuse (RT-002); character count measurement (RT-006) | PAT-002, LES-001, ASM-001 |
| `report2-s013-inversion.md` | Strategy Report (Inversion, R2) | Goal-inversion analysis; Issue #15145 NOT PLANNED ambiguity (IN-002); SSE vs. npx (IN-007); subagent inheritance tension (IN-006) | ASM-001, unique IN-002/IN-007 |
| `report1-s003-steelman.md` | Strategy Report (Steelman, R1) | Core thesis confirmed sound; L0 agent-breakage omission (SM-001); Formula B in-section caveat gap (SM-003); enabled H-16 compliance for subsequent strategies | PAT-002 |

---

*Deep-dive analysis date: 2026-02-26*
*Tournament: 20 strategies (10 per report), all complete*
*Source reports read for this analysis: 6 (synthesis + FMEA R1, FMEA R2 partial, Red Team R1, Inversion R2, Steelman R1)*
*Knowledge items generated: PAT-001, PAT-002, LES-001, ASM-001*
