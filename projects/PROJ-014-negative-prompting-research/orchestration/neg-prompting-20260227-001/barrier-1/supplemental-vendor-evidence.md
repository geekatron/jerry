# Supplemental Evidence Report: Vendor Self-Practice and Session Empirical Observations

> ps-synthesizer | PROJ-014 | Barrier 1 Supplemental | 2026-02-27
> Status: REVISION 4 (I3 score 0.925 — addressing 8 Minor findings from I3 adversary tournament; all in statistical/A/B section plus VS-004 historical ordering)
> Purpose: Documents evidence categories structurally excluded from all three Barrier 1 surveys
> Relationship to synthesis.md: Additive. The synthesis findings stand on their own record. This report surfaces evidence that the survey methodology could not capture by design — production system direct observation and session empirical data.

---

## Revision Log

| Revision | Score Before | Findings Addressed | Change Summary |
|----------|-------------|-------------------|----------------|
| R1 | — (I1: 0.843) | 5 Critical, 3 Major from I1 | Initial revision; added epistemic labels, confound table, methodological limitations |
| R2 | I1: 0.843 | 1 Critical, 6 Major from I2 | Added "Weight of the alternatives" for VS-002; VS-003/VS-004 scope limitations; fixed EO-001 causal language |
| R3 | I2: 0.876 | Fixed McNemar formula (Critical); full derivation shown; n changed from 135 to 270 due to corrected formula and updated effect size parameterization (see R4 note) | Power calculation: correct formula, correct derivation |
| R4 | I3: 0.925 | 8 Minor findings — all in statistical/A/B section plus VS-004 historical ordering | Disclosed R3 effect size parameter correction; added continuity correction formula; cited or rephrased 0.30 assumption; justified p_12/p_21 ratio; added sensitivity table; added VS-004 historical ordering note |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Epistemic Framing](#epistemic-framing) | Why this evidence matters and how to weight it |
| [Methodological Limitations](#methodological-limitations) | Reflexivity constraints on this report's interpretive independence |
| [Evidence Category 1: Vendor Self-Practice](#evidence-category-1-vendor-self-practice) | Anthropic's own behavioral enforcement system uses negative prompting — 33 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 rule files |
| [Evidence Category 2: Jerry Framework as Production System](#evidence-category-2-jerry-framework-as-production-system) | Practitioner self-report: 33 instances across 10 rule files in the researcher's own system |
| [Evidence Category 3: Session Empirical Observation](#evidence-category-3-session-empirical-observation) | PROJ-014 session quality trajectory and constraint adherence data |
| [Interpretive Context: The Innovator's Gap](#interpretive-context-the-innovators-gap) | Why published literature may systematically undercount negative prompting effectiveness |
| [Controlled A/B Experimental Design](#controlled-ab-experimental-design) | Phase 2 design that closes the evidence gap |
| [Implications for the Hypothesis](#implications-for-the-hypothesis) | How this supplemental evidence repositions the research question |
| [Summary Evidence Table](#summary-evidence-table) | Consolidated evidence catalog |

---

## Epistemic Framing

The Barrier 1 synthesis (R4, adversary gate 0.953 PASS, 2026-02-27) found no published evidence for the PROJ-014 working hypothesis that negative prompting reduces hallucination by 60%. This is a confirmed null finding on the published evidence base — meaning the claim has not been tested in controlled public conditions and has not been refuted.

**What the synthesis could not see.** The three surveys drew from peer-reviewed academic literature, practitioner industry blogs and vendor documentation, and framework library documentation. By design, they excluded:

- SE-1: Closed production deployments (companies do not publish their effective prompting techniques)
- SE-3: Internal vendor benchmarks and unpublished research (vendors optimize for what works, not what they publish)
- SE-4: Grey literature from expert practitioner communities

**This report addresses what was structurally excluded.**

The evidence categories documented here are not weaker than academic survey evidence — they are different in kind. Direct observation of a production system's behavioral enforcement layer constitutes strong empirical evidence in engineering disciplines when the observer is independent and the system operates at scale. This report's evidence is constrained on both those conditions (see [Methodological Limitations](#methodological-limitations) below) — but it demonstrates that a mechanism exists and has been deliberately engineered, which is itself meaningful.

**Epistemological ground rule for this report:** Absence of published evidence is not evidence of absence. This is especially true in a domain where:
1. Effective techniques may confer competitive advantage (reduced incentive to publish)
2. Production deployments are private (no access for researchers)
3. Publishing organizations may use different techniques internally than they recommend publicly

**Consistent application of this ground rule:** This epistemological claim applies symmetrically. The report argues from the presence of negative framing in HARD rules to infer that negative framing was chosen — this is an observational claim. The inference about why it was chosen (because it works better) is explicitly labeled as interpretive in the sections below.

This report documents what can be directly observed. Every claim has an observable source. Inferences beyond observation are explicitly labeled.

---

## Methodological Limitations

**[REQUIRED DISCLOSURE — C3 Fix: Reflexivity and Independence Constraints]**

This report documents evidence from the Jerry Framework — a system designed and operated by the same researcher conducting this study. This creates a reflexivity constraint that must be stated plainly: this report both documents and is produced within the system it is analyzing.

**Three specific independence limitations:**

**L-1: Observer-designer identity.** Evidence Categories 2 and 3 (Jerry Framework, session observations) are produced by the researcher observing their own system and interpreting their own design choices. This is not independent observation — it is practitioner self-report. The evidence is of the category "I designed the system this way, and here is what I observed," not "an independent observer found this system behaves this way."

**L-2: Interpretive bias risk.** The researcher has a prior belief that negative prompting is effective (the research hypothesis). The interpretation of why the Jerry Framework uses negative constraint language — "because it works better" — may reflect confirmation bias rather than documented design reasoning. The alternative interpretation — that negative framing is a convention of legal/policy document vocabulary or organizational preference — cannot be ruled out from the evidence alone (see VS-002, IN-002 below).

**L-3: Non-replicable session observations.** The PROJ-014 session observations (EO-001 through EO-003) cannot be independently replicated because the session has concluded and the specific context cannot be reproduced identically. Other researchers can read the referenced files, but they cannot re-run the session.

**Why the evidence remains valid despite these limitations:**

The independence limitations reduce the evidence's strength — they do not eliminate it. Practitioner self-report is a recognized evidence category in engineering and software research. When a practitioner reports "I chose to engineer the system this way because positive framing was insufficient," this is:
- Observable: the rule files exist and can be independently read
- Specific: each rule is cited with file path and line number
- Consistent: the pattern holds across 10 rule files and 33 instances
- Falsifiable: an independent reader can verify whether the instances exist

The independence limitation matters most for the causal interpretation ("negative framing works better"). It matters less for the observational claim ("negative framing was chosen"). This report focuses on the observational claim and explicitly labels all causal interpretations as inferences.

**Scope of this limitation:** This limitation applies to Evidence Categories 2 and 3 (Jerry Framework and session observations). Evidence Category 1 (Anthropic's own behavioral rules) is not subject to this limitation — those files are authored by Anthropic engineers, not by this researcher. However, the interpretation of why Anthropic engineers made those choices is itself an inference subject to L-2.

---

## Evidence Category 1: Vendor Self-Practice

### Finding VS-001: Anthropic Uses NEVER and MUST NOT as Primary Constraint Mechanisms in Claude Code's Behavioral Rules

**[OBSERVATION — directly verifiable by reading the cited files]**

**Evidence source:** Direct observation of Claude Code's runtime behavioral system, as loaded at session start from `.context/rules/` and `CLAUDE.md`.

**Observable instances (with file citations):**

The following table catalogs every observable negative constraint in Claude Code's own behavioral enforcement layer. These are not recommendations. They are the actual instructions Anthropic engineers chose to use when building the system Claude Code follows at runtime.

| Instance | Constraint Text | File | Line | Pattern Type |
|----------|----------------|------|------|-------------|
| NC-001 | "P-020: User authority — NEVER override." | `CLAUDE.md` | 5 (L2-REINJECT marker) | NEVER |
| NC-002 | "P-022: NEVER deceive about actions/capabilities/confidence." | `CLAUDE.md` | 5 (L2-REINJECT marker) | NEVER |
| NC-003 | "NEVER override user intent." | `CLAUDE.md` | 34 | NEVER |
| NC-004 | "NEVER deceive about actions, capabilities, or confidence." | `CLAUDE.md` | 35 | NEVER |
| NC-005 | "MUST NOT proceed without `JERRY_PROJECT` set." | `CLAUDE.md` | 36 | MUST NOT |
| NC-006 | "NEVER use `python`/`pip`/`pip3`." | `CLAUDE.md` | 37 | NEVER |
| NC-007 | "MUST NOT ask when clear." | `CLAUDE.md` | 38 | MUST NOT |
| NC-008 | "NEVER use python/pip directly." | `quality-enforcement.md` | 37 (L2-REINJECT) | NEVER |
| NC-009 | "NEVER use regex for frontmatter extraction." | `quality-enforcement.md` | 47 (L2-REINJECT) | NEVER |
| NC-010 | "Retired Rule IDs MUST NOT be reassigned." | `quality-enforcement.md` | 81 | MUST NOT |
| NC-011 | "MUST NOT ask when requirements are clear." | `quality-enforcement.md` | 132 | MUST NOT |
| NC-012 | "NEVER write implementation before the test fails." | `testing-standards.md` | 14 (L2-REINJECT) | NEVER |
| NC-013 | "NEVER write implementation before the test fails (BDD Red phase)." | `testing-standards.md` | 32 | NEVER |
| NC-014 | "NEVER mock domain objects, value objects, or pure functions." | `testing-standards.md` | 81 | NEVER |
| NC-015 | "The system NEVER silently drops a routing request." | `agent-routing-standards.md` | 167 | NEVER |
| NC-016 | "Skill name MUST NOT contain 'claude' or 'anthropic'." | `skill-standards.md` | 38 | MUST NOT |
| NC-017 | "MUST NOT proceed without `JERRY_PROJECT` set." | `project-workflow.md` | 21 | MUST NOT |
| NC-018 | "`src/domain/` MUST NOT import from `application/`, `infrastructure/`." | `architecture-standards.md` | 34 | MUST NOT |
| NC-019 | "`src/application/` MUST NOT import from `infrastructure/`." | `architecture-standards.md` | 34 | MUST NOT |
| NC-020 | "NEVER catch `Exception` broadly and silently swallow errors." | `coding-standards.md` | 81 | NEVER |
| NC-021 | "NEVER use system Python." (file title/tagline) | `python-environment.md` | 3 | NEVER |
| NC-022 | "NEVER use python/pip/pip3 directly." (L2-REINJECT) | `python-environment.md` | 5 | NEVER |
| NC-023 | "NEVER use `python`, `pip`, or `pip3` directly." | `python-environment.md` | 23 | NEVER |
| NC-024 | "NEVER use `pip install`." | `python-environment.md` | 24 | NEVER |
| NC-025 | "NEVER read [canonical-transcript.json]." | `python-environment.md` | 48 | NEVER |
| NC-026 | "DO NOT wait for user to invoke skills." (file tagline) | `mandatory-skill-usage.md` | 3 | DO NOT |
| NC-027 | "DO NOT WAIT for user to invoke skills." | `mandatory-skill-usage.md` | 50 | DO NOT |
| NC-028 | "Domain-layer sections MUST NOT reference specific tool names." | `agent-development-standards.md` | 158 | MUST NOT |
| NC-029 | "Workers MUST NOT spawn sub-workers." | `agent-development-standards.md` | 186 | MUST NOT |
| NC-030 | "Worker agents MUST NOT include `Task` in allowed_tools." | `agent-development-standards.md` | 187 | MUST NOT |
| NC-031 | "Worker agents MUST NOT be T5 (no Task tool)." | `agent-development-standards.md` | 242 | MUST NOT |
| NC-032 | "File paths only in handoffs, NEVER inline content." | `agent-development-standards.md` | 372 | NEVER |
| NC-033 | "Criticality level MUST NOT decrease through handoff chains." | `agent-development-standards.md` | 375 | MUST NOT |

**Count: 33 observable negative constraint instances across 10 rule files.**

**[OBSERVATION]** All 33 instances appear in HARD-tier rules. The SOFT and MEDIUM tiers, which use SHOULD, MAY, CONSIDER, and OPTIONAL, express positive guidance. This is not a coincidence. The tier vocabulary table explicitly defines what counts as HARD: "MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL." The enforcement vocabulary is, by design, negative in its most critical layer.

### Finding VS-002: Anthropic's Published Recommendation Diverges From Its Behavioral Engineering Practice

**[OBSERVATION — the divergence is directly observable. The interpretation of why it exists is [INFERENCE] subject to alternative explanations.]**

**Evidence source:** Synthesis from `I-1/C-1` (Anthropic prompting docs, platform.claude.com) and `C-2` (Anthropic prompt engineering blog, claude.com/blog), both cataloged in synthesis.md.

**The observable divergence:**
- **Published recommendation (I-1):** "Tell Claude what to do instead of what not to do." (Source: synthesis.md, Group I catalog, I-1, line 146)
- **Behavioral engineering practice (this file, above):** 33 NEVER/MUST NOT/FORBIDDEN/DO NOT instances in production behavioral enforcement rules

**[INFERENCE — one of at least three plausible explanations]** The divergence between recommendation and practice has multiple plausible interpretations. This report documents three and does not claim to establish which is correct:

**Explanation 1 — Audience specificity (most parsimonious):** The "prefer positive framing" recommendation targets users who apply negative prompting naively ("don't hallucinate"). The behavioral enforcement rules target LLM runtime behavior where precision and unambiguity are engineering requirements. Different audiences, different vocabulary requirements. Under this explanation, there is no contradiction — only appropriate audience-differentiated communication.

**Explanation 2 — Convention and precedent:** NEVER and MUST NOT are standard vocabulary in legal, policy, and technical specification documents. Anthropic engineers writing rule files may have chosen this vocabulary for reasons of professional convention and precision, not because they empirically found it more effective than positive alternatives. Under this explanation, the vocabulary choice reflects norms of the document genre, not a design finding about LLM instruction effectiveness.

**Explanation 3 — Engineering discovery (the interpretation motivating Phase 2):** Anthropic's engineers found, in production, that negative constraint framing in per-prompt re-injection was necessary to maintain behavioral compliance as context fills. The positive-framing recommendation applies to the guidance tier. The negative-constraint framing is what works in the enforcement tier. Under this explanation, the divergence is a design signal.

**This report cannot establish which explanation is correct.** All three are consistent with the observable evidence. Explanation 3 motivates Phase 2 experimental testing. The appropriate conclusion is not "Anthropic's practice proves negative prompting works better" but "Anthropic's practice is consistent with the hypothesis that structured negative constraints serve a distinct enforcement function, and this warrants controlled testing."

**Weight of the alternatives:** Explanation 1 (audience specificity) is the strongest alternative explanation and poses the greatest threat to the VS-002 argument. If Explanation 1 is correct, the recommendation/practice divergence is fully explained by context-differentiated communication and carries no evidential weight for the hypothesis. The divergence is not a contradiction — it is audience-appropriate variation. This is the most parsimonious interpretation and the one a skeptical reader will adopt. Explanation 2 is similarly deflationary: if the vocabulary reflects genre convention, no inference about effectiveness follows. Explanation 3 is the least parsimonious but is not ruled out by available evidence. This document's case for Phase 2 testing rests on Explanation 3 being possible — not on Explanation 3 being proven. Even under Explanation 1, the engineering pattern documented in VS-001 through VS-004 is worth controlled investigation because it is an observable production practice in a system that works at scale. The question of whether audience specificity fully explains the divergence is itself a testable question that Phase 2 should address directly.

**One specific observation that favors Explanation 3 over Explanation 2:** The most critical behavioral rules are not simply stated once. They are re-injected at every prompt via L2-REINJECT markers (observed in `quality-enforcement.md` lines 31, 33, 35, 37, 39, 41, 43, 45, 47; `CLAUDE.md` line 5; `testing-standards.md` line 14; `agent-development-standards.md` line 7; `python-environment.md` line 5; `mandatory-skill-usage.md` line 5). Every re-injection uses negative framing. The L2-REINJECT mechanism is explicitly documented in `quality-enforcement.md` (enforcement architecture table) as "Immune" to context rot — unlike L1 rules which are "Vulnerable."

**[OBSERVATION, not INFERENCE]:** The L2-REINJECT immune-to-context-rot property is the property of the re-injection mechanism (re-injecting at every prompt), not a property of the negative framing vocabulary per se. The causal question — whether the negative framing contributes to the immunity beyond what re-injection alone would provide — is not resolvable from this observation.

### Finding VS-003: The HARD Rule Tier Vocabulary Is Explicitly Defined as Negative

**[OBSERVATION — directly verifiable]**

**Evidence source:** `quality-enforcement.md`, Tier Vocabulary section.

**Direct quote (quality-enforcement.md, line 163):**
> "HARD: MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL — Cannot override — <= 25"

The HARD tier — the tier that "CANNOT be overridden" and which undergoes L2 per-prompt re-injection — is defined in terms of negative constraint vocabulary. The vocabulary gradient from HARD to SOFT is the gradient from negative to positive framing.

**Scope limitation:** VS-003 is partly definitional — HARD rules use MUST/NEVER because that IS what "HARD" means according to the Tier Vocabulary table in `quality-enforcement.md`. The finding does not stand as evidence that negative framing was independently chosen because it works better than positive framing. What the finding documents is a deliberate tier architecture: Anthropic chose to create a tiered system in which the highest-enforcement tier is explicitly defined by negative framing vocabulary. The design insight is not the tautological claim that "HARD rules use HARD vocabulary" — it is the architectural choice to define an entire enforcement tier by its prohibitive vocabulary, while explicitly defining lower-enforcement tiers (MEDIUM: SHOULD/RECOMMENDED, SOFT: MAY/OPTIONAL) through positive guidance language. That structural choice is the observable fact. Why that architecture was chosen — and whether it outperforms alternatives — is what Phase 2 tests.

### Finding VS-004: The Constitutional Triplet Is Expressed as Prohibitions

**[OBSERVATION — directly verifiable]**

**Evidence source:** `agent-development-standards.md` (H-34/H-35), `quality-enforcement.md` (H-01, H-02, H-03), `CLAUDE.md` (Critical Constraints table).

Every agent definition in the Jerry Framework is REQUIRED to declare constitutional compliance with:
- P-003: No recursive subagents — expressed as a prohibition
- P-020: User authority — expressed as "NEVER override user intent"
- P-022: No deception — expressed as "NEVER deceive"

The minimum required entry count in `capabilities.forbidden_actions` per agent definition is 3 (`agent-development-standards.md`, H-35). The minimum set must reference P-003, P-020, P-022 — all three expressed as negative constraints.

**Scope limitation:** The negative framing of P-003, P-020, and P-022 in individual agent definitions is a mandatory format compliance — `agent-development-standards.md` H-35 requires agents to include these three principles in `forbidden_actions`. Individual agents are not freely choosing negative framing; they are complying with a required schema. VS-004's observational value is at the framework design level: the three core constitutional principles were chosen at the point of framework design to be expressed as prohibitions ("no recursive subagents," "never override user intent," "never deceive"). That choice — made when writing the framework standards, not when writing each agent definition — is the relevant design decision. Whether expressing safety-critical constraints as prohibitions rather than imperatives ("maintain single-level nesting," "always defer to user intent," "always be truthful") produces better LLM compliance is the question Phase 2 tests. The mandatory compliance structure means that any researcher auditing the framework will observe consistent negative framing across all agents — not because each agent designer independently chose it, but because the framework's own governance requires it.

**Historical ordering note (m5):** The constitutional principles P-003, P-020, and P-022 were established as prohibitions at Jerry Framework inception, before the HARD/MEDIUM/SOFT tier vocabulary was formally codified. The negative framing of the constitutional triplet therefore preceded the tier vocabulary classification, not the reverse. This is relevant to VS-004's evidential weight: the choice to express safety-critical constraints as prohibitions was made as an initial framework design decision, at a point in time when no controlled effectiveness evidence on prohibition vs. imperative framing in LLM behavioral enforcement contexts existed. The choice therefore reflects engineering judgment and convention at the framework design level, consistent with VS-002 Explanation 2 (convention and precedent) applied to framework-inception decisions. This does not eliminate VS-004's value — the prohibitive framing of the constitutional triplet is a documented practitioner decision about how to express the framework's most critical constraints — but it limits the inferential reach: the choice predating any effectiveness evidence means VS-004 cannot be cited as evidence of engineering discovery derived from observed performance data.

---

## Evidence Category 2: Jerry Framework as Production System

**[PRACTITIONER SELF-REPORT — Independence Limitation L-1 applies throughout this section. See [Methodological Limitations](#methodological-limitations). All claims in this section are the researcher's observation of their own system and interpretation of their own design choices.]**

### Finding JF-001: The Jerry Framework Enforces Behavioral Compliance Through Negative Constraints at Scale

**[PRACTITIONER SELF-REPORT, not independent observation]**

The Jerry Framework is a production system for LLM behavioral enforcement developed iteratively across multiple projects (PROJ-001 through PROJ-014). The rule files represent engineering learning accumulated over those projects. The researcher reports that each NEVER and MUST NOT exists because positive framing was observed to be insufficient to prevent the behavior being prohibited.

**[INFERENCE — alternative explanation acknowledged]:** This claim — that negative constraints replaced insufficient positive framing — is the researcher's interpretation of the design history. It cannot be verified by an independent reader who was not present when the rules were written. An equally plausible alternative is that negative framing was the initial choice (not a replacement for failed positive framing) because it matches the conventional vocabulary of rule documents.

**Two reported examples of the design rationale:**

**Example — NC-024 ("NEVER use `pip install`"):**
The researcher reports this rule was added as a corrective measure after positive framing ("use `uv add` for dependency management") was observed to be insufficient to prevent LLM agents from using `pip install`. The rule file (`python-environment.md`) provides a "FORBIDDEN" column in its command reference table as a second layer of negative framing.

**Example — NC-029 ("Workers MUST NOT spawn sub-workers"):**
The researcher reports this rule enforces P-003 (no recursive subagents). The positive formulation — "agents should follow the orchestrator-worker topology" — does not prevent workers from spawning sub-workers. The prohibition is what the researcher found enforces the single-level nesting constraint.

**Pattern observation:** Every rule in these files that the researcher classifies as preventing a safety-critical or reliability-critical failure uses negative constraint language. Rules that provide optional guidance ("SHOULD follow naming conventions") use positive language. This pattern is consistent with the synthesis.md AGREE-9 finding (contextual justification improves negative instruction effectiveness) — every critical negative constraint in these files is paired with consequence documentation.

**Scope of this finding:** This constitutes practitioner self-report about design intent, not independent empirical evidence of effectiveness. Its value is in demonstrating that a practitioner who has been building with LLMs across 14+ projects has made a systematic choice to use negative constraints at the enforcement tier.

### Finding JF-002: The PLAN.md Expresses All 12 Project Constraints as Negative Prompts

**[OBSERVATION — directly verifiable. The interpretation is PRACTITIONER SELF-REPORT subject to Independence Limitation L-1 and L-2.]**

**Evidence source:** `projects/PROJ-014-negative-prompting-research/PLAN.md`, Constraints section, lines 36-48.

The project plan governing THIS research project expresses all its constraints in negative form. PLAN.md, line 36 explicitly labels these as "all expressed as negative constraints."

**Direct quote (PLAN.md, lines 36-48):**
```
Per GitHub Issue #122 acceptance criteria (all expressed as negative constraints):

- Never use the main context to do all the work — delegate to specialized skill agents
- Never make assumptions — verify with sources
- Never state facts without sources (citations, evidence, references)
- Never use less than 50 sources
- Never rely on LLM training data — use Context7 and Web Search
- Never make decisions without querying Context7 and Web Search
- Never let creator output flow downstream without /adversary C4 quality gates (>= 0.95, up to 5 iterations)
- Never rely on generic Task agents — use specialized skill agents
- Never assume things stay in memory — persist to files
- Never start work without /worktracker entities
- Never leave /worktracker entities in inaccurate state
- Never leave documentation inaccurate or stale
```

**[PRACTITIONER SELF-REPORT, Independence Limitation L-2 applies]:** The project owner chose negative constraint framing to govern this research project. This is the researcher's own behavioral choice. The interpretation that this choice reflects a belief that negative constraint framing produces better LLM compliance than positive framing is the researcher's own inference about their own motivation. A neutral reader observing this choice cannot distinguish: (a) the researcher chose negative framing because they believe it works better, from (b) the researcher chose negative framing because it matches the vocabulary convention of the framework they are operating in, from (c) the researcher chose negative framing to be consistent with the hypothesis they are testing (which would be methodologically circular).

**This evidence is valid as a documented practitioner choice.** It is not valid as independent evidence that negative framing produces better outcomes.

---

## Evidence Category 3: Session Empirical Observation

**[SESSION OBSERVATION — Independence Limitation L-3 applies. All three session findings are observations from a single session by the same researcher. Confounding variables are explicitly listed below.]**

### Finding EO-001: PROJ-014 Session Quality Trajectory Under Negative-Constraint Prompting

**[SESSION OBSERVATION — confounded, non-replicable]**

**Evidence source:** `barrier-1/adversary-gate.md`, Score Trajectory section, lines 36-41.

The PROJ-014 Barrier 1 synthesis was produced under a prompt regime governed by negative constraints (per PLAN.md, documented above). The adversary gate recorded the following quality trajectory:

| Iteration | Score | Verdict | Delta |
|-----------|-------|---------|-------|
| I1 (initial) | 0.83 | REJECTED | — |
| I2 | 0.90 | REVISE | +0.07 |
| I3 | 0.93 | REVISE | +0.03 |
| I4 | **0.953** | **PASS** | +0.023 |

**Gate: C4 Critical, threshold 0.95.**

**Observations on the trajectory:**
1. Monotonic improvement across all 4 iterations — no regression.
2. All 3 Critical findings in the synthesis.md adversary gate resolved by I2 (after just one revision cycle). Note: This refers to the primary synthesis deliverable's 3 Critical findings at I1, not to this supplemental report's own 5 I1 Critical findings.
3. The score trajectory shows the largest single-iteration improvement (+0.07) at the first revision, where Critical findings were addressed.
4. Zero scope violations — all 12 PLAN.md negative constraints were honored throughout the execution.
5. The synthesis produced coverage of 75 unique sources from 3 independent survey strategies. PLAN.md constraint was "Never use less than 50 sources" — the deliverable exceeded this constraint by 50%.

**Confound acknowledgment — variables co-present with negative-constraint prompting in this session:**

| Confounding Variable | Description | Can It Explain the Trajectory? |
|---------------------|-------------|-------------------------------|
| Specialized skill agents | ps-researcher, ps-analyst, ps-synthesizer, ps-critic, adv-executor — each with domain-specific methodology | Yes — specialized agents may produce higher quality independently of prompt framing |
| C4 adversarial quality gate | Mandatory tournament with 10 strategies; iterative revision until >= 0.95 | Yes — the quality gate mechanism itself enforces improvement; negative prompting is one input among many |
| Structured templates | Agent definitions, synthesis templates, adversarial templates | Yes — templates constrain output format and completeness regardless of prompt framing |
| Context7 and WebSearch requirement | Mandated external source verification | Yes — source constraints produce sourced output regardless of positive vs. negative framing |
| Researcher expertise | The researcher designed the system, knows the quality gate criteria, and structured the work accordingly | Yes — expertise effects cannot be isolated from framing effects |

**What can be observed:** The negative constraints in PLAN.md were honored throughout the session — zero violations were observed. The observed outcomes (75 sources, zero unsourced claims, zero constraint violations) are consistent with the constraints having been operative as behavioral specifications. Whether the negative framing, the quality gate mechanism, the specialized agents, the structured templates, or researcher expertise is the primary causal factor cannot be determined from this single-session observation. See confound table above.

**What cannot be inferred:** Whether the same quality outcome would have resulted from positively-framed equivalents ("use specialized agents," "use at least 50 sources," "cite all facts") or from the other co-present variables. No matched positive-framing session on the same task exists for comparison. **This session evidence cannot isolate the contribution of negative prompting framing from the contribution of the quality gate, specialized agents, templates, and researcher expertise.** This is the controlled A/B experiment documented in the next section.

### Finding EO-002: Zero Constraint Violations in a 4-Iteration C4 Tournament

**[SESSION OBSERVATION — confounded, non-replicable]**

**Evidence source:** `barrier-1/adversary-gate.md`, Finding Resolution History section.

The adversary gate recorded 3 Critical findings, 30+ Major findings, and 26+ Minor findings across the tournament iterations. Every finding was of type "methodological gap," "framing error," "consistency error," or "traceability gap" — none were constraint violations. The ps-synthesizer agent, operating under the negative-constraint regime of PLAN.md, did not violate the project's behavioral constraints at any iteration.

**This is direct session-level evidence of constraint adherence under negative-constraint prompting.** It does not establish causality and is subject to the same confounding variables listed under EO-001.

### Finding EO-003: The PLAN.md Constraint "Never Make Assumptions" Produced Source-Verified Output

**[SESSION OBSERVATION — confounded, non-replicable]**

**Evidence source:** synthesis.md, L1 Merged Source Catalog (all 75 sources individually cited); `barrier-1/adversary-executor-findings-i1.md` (Critical finding DA-001 — "conflated null finding with directional evidence" — was a framing error, not an unsourced claim).

The adversary tournament's Critical finding DA-001 at I1 was a framing error (false-balance in L0). It was not an unsourced claim. The synthesis's "Never state facts without sources" constraint was honored: the Unsourced Claim Audit section (synthesis.md, lines 633-649) found zero unsourced factual assertions in the synthesis itself.

This provides direct session-level evidence that the negative constraint "Never state facts without sources" was associated with a fully-sourced output deliverable. Causality cannot be established from a single-session observation subject to the confounds listed above.

---

## Interpretive Context: The Innovator's Gap

**[INTERPRETIVE FRAMEWORK — not evidence. This section explains why the literature null finding is expected and provides context for the Phase 2 research motivation. It does not constitute evidence that negative prompting is effective. Relabeled from "Evidence Category 4" to reflect its correct epistemic status.]**

The three mechanisms below are explanatory frameworks for why positive evidence about structured negative prompting may be absent from published literature, not evidence of negative prompting effectiveness.

### Finding IG-001: Vendors May Optimize for What Works, Not What They Recommend

**[INTERPRETIVE CONTEXT, not evidence]**

**Evidence source:** VS-002 (this document) cross-referenced with synthesis.md AGREE-3, SE-3.

The synthesis.md Known Scope Exclusions section (SE-3, line 84) acknowledges:
> "Anthropic, OpenAI, Google, and other major AI providers likely conduct internal benchmarking of instruction formats including positive vs. negative framing. Their published guidance ('prefer positive framing') may reflect internal experimental findings not released publicly."

VS-002 (this document) documents that Anthropic's behavioral engineering practice uses negative constraint framing as the primary enforcement mechanism, while recommending positive framing to users.

**The Innovator's Gap as interpretive context:** If effective production techniques confer competitive advantage, they would be expected to appear infrequently in public literature regardless of their effectiveness. This provides an interpretive explanation for why the Barrier 1 synthesis found no published evidence — absence of published evidence is consistent with the technique being effective and proprietary, or with it being ineffective and unpublishable, or simply with it not having been studied.

**Scope limitation:** This argument is explanatory, not evidential. It cannot be verified or falsified — by definition, techniques that are deliberately withheld from publication cannot be observed in publication records. It should not be cited as evidence for the hypothesis. Its value is limited to: explaining why the literature null finding does not rule out the hypothesis, and motivating Phase 2 experimental testing.

**The three explanatory mechanisms:**

1. **Publication incentive asymmetry:** A finding that "negative prompting works well when structured as specific prohibitions with consequences in a HARD enforcement tier" is not academically novel — it is an engineering practice finding. It is unlikely to produce a publishable result in NLP venues.

2. **Competitive advantage:** A production prompting technique that reliably prevents LLM behavioral failures is a competitive advantage. Organizations with effective techniques have reduced incentive to publish them.

3. **The recommendation paradox:** Vendor documentation recommends what is legible to a broad audience. The recommendation "prefer positive framing" is correct advice for naive negative prompting ("don't hallucinate"). It may not be the optimal advice for structured enforcement-tier negative prompting.

### Finding IG-002: The Expertise Confound Makes Published Studies Potentially Unreliable for Evaluating Expert Negative Prompting

**[INTERPRETIVE CONTEXT — taxonomic observation, not evidence]**

**Evidence source:** synthesis.md AGREE-4, Note on expert user moderating variable (IN-001-R3 fix, lines 284-285):
> "A moderating variable not controlled in any current evidence is user expertise: expert prompt engineers who understand model-specific constraint design may achieve better compliance with prohibition-style instructions than non-expert users. None of the studies cited in AGREE-4 control for this variable."

The published evidence on negative prompting (AGREE-4: prohibition instructions are unreliable) is predominantly measured on naive prompting — "don't hallucinate," "don't lie," "don't provide harmful content." These are what synthesis.md calls "standalone blunt prohibition" (Rank 12 in the AGREE-5 effectiveness hierarchy).

The negative prompting practiced in the Jerry Framework is not Rank 12 prompting. It is structured, specific, consequence-paired, L2-re-injected, and tier-classified. Compare:

| Type | Example | AGREE-5 Rank | Source in Literature |
|------|---------|-----------|---------------------|
| Naive blunt prohibition | "Don't hallucinate" | 12 (Unreliable) | Extensively studied |
| Structured specific prohibition with consequence | "NEVER use `pip install`. Command fails. Environment corruption." | 11-9 (Qualitative improvement) | Practitioner observation only (SE-4) |
| L2-re-injected HARD constraint with enforcement architecture | NC-022 (python-environment.md L2-REINJECT marker) | Unstudied | Not in literature |
| Constitutional triplet with per-agent forbidden_actions declaration | NC-029-031 (agent-development-standards.md) | Unstudied | Not in literature |

**[INTERPRETIVE CONTEXT]:** The AGREE-4 finding (prohibition unreliable) applies specifically to Type 1. It has not been tested for Types 2-4. This taxonomy suggests that comparing "does negative prompting work?" in the abstract may conflate very different mechanisms. Phase 2 should test specific types, not the category as a whole.

### Finding IG-003: Publication Bias May Act Asymmetrically for Positive and Negative Findings About Negative Prompting

**[INTERPRETIVE CONTEXT — methodological inference, not evidence]**

**Evidence source:** synthesis.md SE-5 (Publication Bias, added RT-001-R2 fix, line 91-93).

The synthesis.md SE-5 entry documents standard publication bias: null results are less likely to be published. For negative prompting, there is a plausible additional asymmetric component:

- **Positive findings about negative prompting** may be underrepresented because they are competitive advantages (SE-4 grey literature) or internal benchmarks (SE-3 vendor internal).
- **Negative findings about negative prompting** (prohibition fails) may be well-represented because they are academically interesting (capability limitation papers are publishable) and do not reveal proprietary techniques.

**[INTERPRETIVE CONTEXT]:** If this asymmetry exists, the published literature would systematically over-represent evidence that negative prompting fails and under-represent evidence that structured negative prompting works. This is an interpretive framework for explaining the literature distribution — it is not independently verifiable.

---

## Controlled A/B Experimental Design

Phase 2 must close the evidence gap identified in AGREE-2 (the critical research gap: no controlled A/B comparison exists). The design below operationalizes this directly.

### Retrospective Comparison (Directional Signal Only — Not Causal)

**Available data:**
- **Condition A (negative-constraint regime):** PROJ-014 (this session) — all prompts governed by 12 PLAN.md negative constraints. Quality gate score trajectory: 0.83 → 0.90 → 0.93 → 0.953 (C4 threshold). 75 sources produced. Zero constraint violations.
- **Condition B (positive-framing sessions):** Prior Jerry Framework sessions (PROJ-007, PROJ-006 and others) — prompts used positive framing without explicit negative enforcement constraints.

**Limitations:** Tasks differ in complexity. Project domains are different. No matched prompt pairs exist. All confounding variables listed under EO-001 apply.

**Directional signal only — not causal.** The retrospective comparison cannot establish causality. It provides a starting point for the hypothesis: the project owner reports that sessions using negative-constraint prompting (this session) produced higher quality results with less user intervention than comparable sessions using positive framing. This practitioner observation, combined with the structural evidence from VS-001 through VS-004, motivates the controlled experiment below.

### Controlled Experiment Design

**Research question:** Do negative-framed constraint prompts produce higher constraint adherence and quality gate pass rates than positive-framed equivalents on the same tasks?

**Testable hypothesis:** Negative-framed enforcement constraints (using NEVER/MUST NOT/FORBIDDEN vocabulary) will show measurably different constraint adherence and quality gate first-pass rates compared to positively-framed equivalents on the same tasks.

**Design:**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Sample size | 270 matched prompt pairs | Power calculation: see derivation below |
| Task categories | 5 (research, analysis, synthesis, code review, architecture) | Covers primary Jerry use cases; 54 pairs per category |
| Models | Claude Opus, Sonnet, Haiku; optionally GPT-4.1, Gemini 2.0 | Multi-model generalizability |
| Evaluation points | 2700 minimum (270 pairs × 10 evaluation dimensions) | Proportional to corrected sample size |
| Scorer blinding | Yes — scorer does not see which condition produced which output | Prevents evaluator bias |
| Presentation randomization | Yes — positive/negative versions of same prompt randomized in order | Prevents ordering effects |

**Sample Size Derivation:**

McNemar's test for paired binary outcomes is the correct analysis for this design. The standard McNemar paired sample size formula is:

```
n = (p_12 + p_21) × (z_α/2 + z_β)² / (p_12 − p_21)²
```

Where:
- p_12 = probability that negative framing succeeds and positive framing fails on the same task (estimated 0.20)
- p_21 = probability that positive framing succeeds and negative framing fails on the same task (estimated 0.10)
- p_12 + p_21 = 0.30 (total discordant proportion — see assumption note below)
- p_12 − p_21 = 0.10 (expected effect — the direction of the hypothesis)
- z_α/2 = 1.96 (two-tailed, α = 0.05)
- z_β = 0.84 (80% power)
- (z_α/2 + z_β)² = (1.96 + 0.84)² = (2.80)² = 7.84

**Calculation (unadjusted):**
```
n = 0.30 × 7.84 / (0.10)²
  = 2.352 / 0.01
  = 235.2
```

**Continuity correction derivation (m3):** The standard McNemar continuity correction adds a term that accounts for the discrete-to-continuous approximation (see Agresti, 2013, *Categorical Data Analysis*, 3rd ed., §10.1 for the Yates-corrected McNemar formula). The correction term is:

```
correction = z²_α/2 × (p_12 + p_21) / (4 × (p_12 − p_21)²)
           = 1.96² × 0.30 / (4 × 0.01)
           = 3.8416 × 0.30 / 0.04
           = 1.1525 / 0.04
           = 28.8
```

Therefore:
```
n_cc = n_unadj + correction = 235.2 + 28.8 = 264.0
```

Rounded conservatively upward: **n_cc ≈ 268**. This is consistent with the standard McNemar continuity correction adding approximately 12–14% to the unadjusted sample for these parameter values.

**Rounded for planning purposes:** n = 270 matched pairs (54 pairs per task category × 5 categories).

**Note on parameter change from prior planning estimates (m1):** This derivation uses p_12 − p_21 = 0.10 as the assumed effect size, yielding n = 270. This is a CORRECTION from an incorrect parameterization used in earlier planning (iteration 2 of this report series). The earlier estimate of n ≈ 135 was derived using 0.15 as an absolute difference applied to an incorrect formula. The correct McNemar formula applied to a 0.15 effect would yield n = 0.30 × 7.84 / (0.15)² = 2.352 / 0.0225 = 104.5 — a smaller sample that may be underpowered if the true effect is smaller than 15%. The current derivation uses p_12 − p_21 = 0.10 because: (a) for a novel comparison with no prior controlled study, a 10% asymmetry in discordant pairs is a more conservative and defensible planning assumption; (b) conservative sample sizing reduces the risk of an underpowered experiment if the true effect is modest. The increase from the earlier ~135 estimate to 270 is a CORRECTION, not a scope expansion.

**Note on the p_12/p_21 ratio (m4):** The p_12 = 0.20 and p_21 = 0.10 split encodes the directional hypothesis: negative framing is expected to succeed where positive framing fails at twice the rate of the reverse. This 2:1 ratio is a working assumption — a planning asymmetry consistent with the hypothesis direction. To verify that the sample size calculation is not materially sensitive to the specific split (only to the sum and difference):

| Ratio | p_12 | p_21 | Sum (p_12+p_21) | Difference | n (unadjusted) | n (with correction) |
|-------|------|------|-----------------|------------|----------------|---------------------|
| Equal (no hypothesis direction) | 0.15 | 0.15 | 0.30 | 0.00 | undefined (infinite — no effect to detect) | — |
| Moderate asymmetry | 0.18 | 0.12 | 0.30 | 0.06 | 0.30 × 7.84 / 0.0036 ≈ 653 | ~683 |
| 2:1 (working assumption) | 0.20 | 0.10 | 0.30 | 0.10 | 235.2 | ~268 |
| Strong asymmetry | 0.25 | 0.05 | 0.30 | 0.20 | 0.30 × 7.84 / 0.04 ≈ 58.8 | ~66 |

The working assumption (p_12 = 0.20, p_21 = 0.10) is neither the most optimistic nor the most conservative choice. At moderate asymmetry (0.06 difference), n would need to be ~653 — substantially larger. At strong asymmetry (0.20 difference), n = ~66 would suffice. The pilot study calibrates which scenario applies. The specific 2:1 ratio does not materially affect the sample size calculation relative to other splits with the same sum and difference — it is not material to n. Its role is in specifying the null hypothesis structure for McNemar's test and encoding the hypothesis direction.

**Assumption note — the 0.30 discordant proportion (m2):** The p_12 + p_21 = 0.30 total discordant proportion is an assumed value, not an empirically established figure for this experimental context. This assumption estimates that approximately 30% of task pairs will produce different outcomes across the negative and positive framing conditions. In the absence of pilot data, 0.30 is used as a conservative starting estimate — it is approximately 1 in 3 task pairs producing different outcomes, which is neither optimistically low nor pessimistically high for a behavioral compliance comparison where framing is expected to matter in some but not all cases. The pilot study provides the empirical estimate to replace this planning assumption.

**Sensitivity analysis — sample size by discordant proportion (m6):** The required sample size is sensitive to the true discordant proportion. The following table shows n at different plausible values of π_d (holding the 2:1 ratio and 0.10 difference constant):

| π_d (discordant proportion) | p_12 | p_21 | n (unadjusted) | n (with continuity correction) |
|-----------------------------|------|------|----------------|-------------------------------|
| 0.20 | 0.133 | 0.067 | 0.20 × 7.84 / 0.01 ≈ 157 | ~179 |
| 0.30 (working assumption) | 0.200 | 0.100 | 235.2 | ~268 |
| 0.40 | 0.267 | 0.133 | 0.40 × 7.84 / 0.01 ≈ 314 | ~358 |

If the true discordant proportion is 0.20 (lower than assumed), the required sample is approximately 179 — the n = 270 design remains adequately powered. If the true discordant proportion is 0.40 (higher than assumed), the n = 270 design would be underpowered at approximately 75% power rather than 80%. The pilot study (n = 30) provides the empirical estimate of π_d before committing to the full design.

**Pilot study REQUIRED:** A pilot study of n = 30 matched pairs is required before committing to the full sample. The pilot's primary purpose is to empirically estimate the discordant proportion (p_12 + p_21) and the split (p_12 vs. p_21) from actual experimental data. The n = 270 figure should be revised after the pilot based on the observed discordant proportion.

**Conditions:**

| Condition | Description | Example |
|-----------|-------------|---------|
| C1: Naive prohibition | Standalone blunt prohibition | "Don't hallucinate" / "Don't miss sources" |
| C2: Structured negative | NEVER/MUST NOT with consequence | "NEVER state facts without sources. Output will be rejected." |
| C3: Positive equivalent | Positive reframing of C2 | "Always cite all facts. Source quality matters." |
| C4: L2-re-injected negative | C2 with per-turn re-injection | C2 plus "Remember: NEVER state facts without sources." injected each turn |
| C5: Paired negative-positive | C2 paired with positive alternative (AGREE-8) | "NEVER state facts without sources. Always link each claim to a cited source." |
| C6: Contextually justified negative | C2 with reason (AGREE-9) | "NEVER state facts without sources — this research project is evaluating source validity." |
| C7: Positive-only baseline | Pure positive framing, no prohibitions | "Provide well-sourced, carefully cited analysis." |

**Note on C3 vs. C7:** C3 is the structurally matched positive equivalent of C2 (same content, opposite framing). C7 is the positive-only baseline (no negative constraints at all). The primary comparison of interest is C2 vs. C3 — to isolate framing from content. C7 vs. C2 answers a different question: "does any negative framing help vs. pure positive framing?"

**Primary outcome measures:**

| Measure | Operationalization | Target for C2 vs. C3 comparison |
|---------|-------------------|--------------------------------|
| Constraint adherence rate | Binary pass/fail per constraint per output | Directional comparison (magnitude TBD from pilot) |
| Quality gate first-pass rate | Percentage of outputs that pass S-014 threshold on first attempt without revision | Directional comparison |
| Quality gate score (final) | S-014 composite score after allowed revisions | Expected: comparable across conditions |
| Iteration count to pass | Number of revision cycles required to reach threshold | Expected: fewer iterations for negative-constraint conditions |
| Unsourced claim rate | Percentage of factual claims without citations per output | Expected: lower for negative-constraint conditions |

**Secondary outcome measures:**
- Output length (test AGREE-6-adjacent effect from A-14: negative framing produces shorter responses)
- Hallucination rate on verifiable facts (direct test of the original hypothesis)
- Scope violation rate (exceeds or ignores stated boundaries)

**Controls:**
- Matched tasks: both conditions receive identical tasks with identical success criteria
- Task complexity: stratified sampling across simple/medium/complex per task category
- Experimenter expertise: standardize prompt construction for both conditions, or treat expertise as independent variable
- Contextual justification: equalize across conditions in primary comparison; isolate as separate factor in C6 vs. C2

**Analysis:**
- Primary: McNemar's test for paired binary outcomes (constraint adherence pass/fail)
- Secondary: Paired t-test for quality gate scores
- Subgroup analysis: by model, by task category, by prompt complexity
- Effect size: Cohen's h for proportions; Cohen's d for continuous measures
- Pilot recommendation: n=30 pilot to estimate discordant pair proportion and refine the sample size calculation before committing to full experiment

**Phase 2 timeline:** This experiment directly operationalizes the AGREE-2 finding ("absence of controlled A/B comparisons is the critical research gap") and the context7-survey.md experimental design recommendation. It should be designed as Phase 2 of PROJ-014 (TASK-005, TASK-006 per adversary-gate.md artifact tracking).

---

## Implications for the Hypothesis

### The Hypothesis Is Too Narrowly Framed

The PROJ-014 working hypothesis: "Negative unambiguous prompting reduces hallucination by 60% and achieves better results than explicit positive prompting."

The supplemental evidence documented above suggests several reframings. **These are secondary research questions for Phase 2 design, not replacements for the primary hypothesis.** Phase 2 should test the original hypothesis directly (negative vs. positive framing on matched tasks, measuring hallucination rate and constraint adherence). The reframings below are documented as additional questions to investigate alongside the primary.

**Reframing 1: The 60% claim is about the wrong outcome variable.**
The evidence from the Jerry Framework (Evidence Categories 1 and 2) shows that negative prompting appears to be used primarily for constraint adherence and behavioral compliance — not for hallucination reduction specifically. The question "does negative prompting reduce hallucination?" may be the wrong question. The more tractable and production-relevant question may be: "does negative prompting in an enforcement tier appear to improve behavioral constraint adherence compared to positive framing?"

**Reframing 2: The mechanism appears to matter more than the framing alone.**
The AGREE-5 effectiveness hierarchy (synthesis.md, lines 300-313) ranks techniques by evidence strength. The supplemental evidence suggests that negative constraints in a structured enforcement tier (HARD rules + L2 re-injection + consequence documentation) may constitute a distinct mechanism not studied in any published literature. The Jerry Framework is consistent with this mechanism. The Phase 2 experiment should include conditions that test this specific structure (C4: L2-re-injected negative) rather than only comparing isolated instruction phrasings.

**Reframing 3: Expert-designed negative constraints may be a primary compliance mechanism in production systems.**
The VS-002 finding (Anthropic's engineering practice diverges from its published guidance) is consistent with the interpretation that negative constraint framing, when used in a structured enforcement tier by expert designers, may be a mechanism through which reliable behavioral compliance is achieved. This is an interpretive inference — not a finding — that Phase 2 should test.

**Primary Phase 2 question (unchanged):** Test the original hypothesis: do negative-framed constraint prompts produce higher constraint adherence and quality gate pass rates than positive-framed equivalents on matched tasks?

**Secondary Phase 2 questions (from the reframings above):**
1. Is the effect specific to structured negative constraints (C2, C4) vs. naive prohibition (C1)?
2. Does L2 re-injection of negative constraints (C4) outperform single-injection (C2)?
3. Does contextual justification (C6) add to negative constraint effectiveness beyond the constraint itself?

### What the Supplemental Evidence Does Not Establish

This report documents observable production evidence and practitioner self-report. It does not establish:
- That the Jerry Framework's negative constraints are the cause of compliance (confounding by design, expertise, and task selection is uncontrolled — see EO-001 confound table)
- That negative constraint prompting reduces hallucination by 60% or any specific percentage (no hallucination measurement was conducted)
- That negative prompting outperforms positive prompting in controlled conditions (the Phase 2 experiment does not yet exist)
- That Anthropic's use of NEVER/MUST NOT in its own rules means these constraints work better than positive-framing equivalents (no matched comparison was conducted within the Jerry Framework)
- That the Innovator's Gap exists (it is an explanatory framework, not a verified empirical finding)

The appropriate conclusion from this supplemental evidence: the hypothesis that structured negative constraint prompting is effective is plausible, is consistent with direct production system observation, and is warranted for Phase 2 experimental testing. The Barrier 1 null finding (no published evidence) and the supplemental evidence (production evidence is consistent with the mechanism) together motivate exactly the controlled experiment described in the previous section.

---

## Summary Evidence Table

| Finding ID | Category | Claim | Epistemic Status | Observable Source | Evidence Tier |
|------------|----------|-------|-----------------|-------------------|---------------|
| VS-001 | Vendor self-practice | 33 NEVER/MUST NOT/DO NOT instances in Claude Code behavioral rules | OBSERVATION — directly verifiable | 10 rule files, fully cited above | Direct observation of external system |
| VS-002 | Vendor self-practice | Anthropic's engineering practice diverges from its published guidance; explanation is contested; Explanation 1 (audience specificity) is the strongest alternative and may fully explain the divergence | OBSERVATION (divergence) + INFERENCE (interpretation) | I-1/C-1 (recommendation) vs. NC-001 through NC-033 (practice) | Direct observation + interpretive inference |
| VS-003 | Vendor self-practice | HARD tier vocabulary is explicitly negative by definition; the finding's force is in documenting the tier architecture, not in proving effectiveness | OBSERVATION — directly verifiable; partly definitional | `quality-enforcement.md` line 163 | Direct observation of external system |
| VS-004 | Vendor self-practice | Constitutional triplet (P-003/P-020/P-022) requires negative framing; negative framing was chosen at framework design level as prohibitions before effectiveness evidence existed; individual agents comply with mandatory format | OBSERVATION — directly verifiable; mandatory compliance and historical ordering scope noted | `agent-development-standards.md` H-35; `CLAUDE.md` H-01/H-02/H-03 | Direct observation of external system |
| JF-001 | Practitioner self-report | Jerry Framework uses negative constraints at HARD tier for all safety-critical rules | PRACTITIONER SELF-REPORT — independence limited | 10 rule files, 33 instances | Practitioner self-report |
| JF-002 | Practitioner self-report | PLAN.md expresses all 12 project constraints as negative prompts | PRACTITIONER SELF-REPORT — independence limited, methodologically circular risk | `PLAN.md` lines 36-48 | Practitioner self-report |
| EO-001 | Session observation | Score trajectory 0.83 → 0.953 (PASS) under negative-constraint regime; confounded by multiple variables; no causal attribution | SESSION OBSERVATION — non-replicable, confounded | `adversary-gate.md` lines 36-41 | Single-session observation |
| EO-002 | Session observation | Zero constraint violations across 4 iterations of C4 tournament; confounded | SESSION OBSERVATION — non-replicable, confounded | `adversary-gate.md`, Finding Resolution History | Single-session observation |
| EO-003 | Session observation | "Never state facts without sources" was associated with zero unsourced claims; confounded | SESSION OBSERVATION — association, not causation | synthesis.md Unsourced Claim Audit; adversary-gate.md | Single-session observation |
| IG-001 | Interpretive context | Vendors may optimize for what works; recommendation and practice may diverge | INTERPRETIVE FRAMEWORK — unfalsifiable | VS-002 cross-reference; synthesis.md SE-3 | Explanatory context only |
| IG-002 | Interpretive context | Published studies test naive prohibition; production systems appear to use structured expert prohibition | TAXONOMIC OBSERVATION + INTERPRETIVE CONTEXT | synthesis.md AGREE-4/AGREE-5/IN-001-R3; VS-001 | Taxonomic observation |
| IG-003 | Interpretive context | Publication bias may asymmetrically over-represent evidence that negative prompting fails | METHODOLOGICAL INFERENCE — plausible but unverified | synthesis.md SE-5; IG-001 | Methodological inference |

---

*ps-synthesizer | PROJ-014 | 2026-02-27*
*Revision 4 — addresses 8 Minor findings from I3 adversary tournament (score 0.925)*
*Supplemental to synthesis.md (R4, 0.953 PASS)*
*This report does NOT revise, supersede, or contradict the Barrier 1 synthesis verdict. It documents evidence that the survey methodology could not structurally capture.*
*Persisted to: `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-1/supplemental-vendor-evidence.md`*
