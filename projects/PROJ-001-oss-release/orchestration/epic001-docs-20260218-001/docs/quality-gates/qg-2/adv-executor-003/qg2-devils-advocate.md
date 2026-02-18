# Devil's Advocate Report: FEAT-018 User Documentation (Runbooks & Playbooks)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** 4 user-facing documentation files for Jerry Framework OSS release:
  1. `docs/runbooks/getting-started.md`
  2. `docs/playbooks/problem-solving.md`
  3. `docs/playbooks/orchestration.md`
  4. `docs/playbooks/transcript.md`
**Criticality:** C2 Standard
**Date:** 2026-02-18
**Reviewer:** adv-executor-003
**H-16 Compliance:** S-003 Steelman applied during 3-iteration creator-critic cycle (final score 0.937) (confirmed)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Assumptions Inventory](#assumptions-inventory) | Explicit and implicit assumptions challenged |
| [Findings Table](#findings-table) | All counter-arguments with severity and dimension mapping |
| [Finding Details](#finding-details) | Expanded analysis for Critical and Major findings |
| [Recommendations](#recommendations) | Prioritized action list (P0/P1/P2) |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 quality dimensions |

---

## Summary

10 counter-arguments identified (0 Critical, 5 Major, 5 Minor). The documentation set is structurally sound and internally consistent -- the four documents cover distinct skill domains, cross-reference each other appropriately, and provide actionable step-by-step procedures. However, the set relies on several unstated assumptions about the target audience's prior experience that could make the "Getting Started" path fail for genuine newcomers. Additionally, verifiability gaps across all four documents mean that a user following the instructions cannot always confirm whether they have executed a step correctly. The absence of any error recovery path for mid-workflow failures (especially in the orchestration and transcript playbooks) is the most consequential gap. Recommend **ACCEPT with targeted revisions** addressing the 5 Major findings.

---

## Assumptions Inventory

### Explicit Assumptions

| # | Assumption | Source | Challenge |
|---|-----------|--------|-----------|
| EA-1 | User has completed `INSTALLATION.md` before starting | `getting-started.md` line 19 | `INSTALLATION.md` does not exist in the repository. The prerequisite references a phantom document, meaning the stated start-state is unachievable. |
| EA-2 | `jerry-framework` is visible in Claude Code `/plugin` > Installed tab | `getting-started.md` line 24 | Jerry's actual installation mechanism is not documented here. If the plugin model changes (Claude Code plugin system is not publicly stable), this check becomes invalid. |
| EA-3 | Trigger keywords reliably activate the correct skill | `problem-solving.md` line 64, `orchestration.md` line 28 | Keyword activation depends on LLM interpretation, which is non-deterministic. A user saying "I want to explore orchestrating a research pipeline" could trigger either skill. |

### Implicit Assumptions

| # | Assumption | Source | Challenge |
|---|-----------|--------|-----------|
| IA-1 | User understands environment variables and shell profiles | `getting-started.md` Steps 1-2 | An OSS newcomer may not know what `export` does, what `~/.zshrc` is, or why environment variables do not persist between terminals. The document assumes Unix/shell fluency. |
| IA-2 | User has a working Claude Code installation with API access | All documents | None of the four documents verify that Claude Code itself is functional. A user whose API key is expired, rate-limited, or misconfigured will see failures not covered by any troubleshooting table. |
| IA-3 | Output directories exist or are automatically created by agents | `problem-solving.md` line 70-71, `orchestration.md` line 130 | Documents state agents persist output to `docs/research/`, `docs/analysis/`, etc. but never instruct the user to create these directories. If agents do not auto-create them, skill invocations fail silently. |
| IA-4 | The user's filesystem has write permissions on the project directory | `getting-started.md`, `orchestration.md` | No document checks or mentions filesystem permissions. A read-only clone would cause all artifact persistence to fail. |
| IA-5 | Cross-session resumption in orchestration works reliably | `orchestration.md` Example 3 | The YAML state file's durability depends on Claude Code session behavior. If the LLM modifies YAML incorrectly (malformed syntax, wrong checkpoint ID), resumption fails. No validation step is documented. |
| IA-6 | SRT and plain text transcript parsing works equivalently to VTT | `transcript.md` line 181-184, 248-249 | The document states SRT/plain text use "LLM-based parsing" while VTT uses the deterministic Python parser. This means SRT/TXT are 1,250x more expensive and non-deterministic, but the document presents all three formats as equivalent choices without warning about the cost or accuracy differential. |

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-qg2 | Phantom prerequisite: `INSTALLATION.md` does not exist | Major | `getting-started.md` line 19: "You have completed the Jerry installation documented in `../INSTALLATION.md`" -- this file is referenced but absent from the repository | Completeness |
| DA-002-qg2 | No error recovery paths for mid-workflow failures | Major | `orchestration.md` troubleshooting table covers only pre-start and post-completion states; no guidance for what to do if an agent fails mid-phase (e.g., Phase 2 agent crashes, partial artifacts written) | Actionability |
| DA-003-qg2 | Keyword-based activation model is presented as deterministic but is not | Major | `problem-solving.md` line 64: "State your request in natural language, using one of the trigger keywords"; `orchestration.md` line 28: "use the keyword orchestration in your request to trigger automatic invocation" -- these imply reliable keyword-to-skill mapping, but LLM keyword detection is probabilistic | Evidence Quality |
| DA-004-qg2 | Cost and accuracy implications of SRT/TXT parsing understated | Major | `transcript.md` lines 181-184, 247-249: SRT and plain text use "LLM-based parsing" vs. VTT's deterministic Python parser. The document explicitly states VTT is "1,250x cheaper" (line 75) but does not restate this differential in the Input Formats table where a user selects their format | Completeness |
| DA-005-qg2 | No version or compatibility information for any tool dependency | Major | All four documents reference `uv`, `jerry`, Claude Code, and the plugin system without specifying minimum versions. `getting-started.md` line 21 checks `uv --version` but does not state what version is required. A user with uv 0.1.x (hypothetical breaking change) would get opaque errors. | Evidence Quality |
| DA-006-qg2 | Output directory creation is never verified or instructed | Minor | `problem-solving.md` line 70-71: "The agent persists all output to a file in the project's `docs/` subdirectory (e.g., `docs/research/`, `docs/analysis/`, `docs/decisions/`)" -- the user is never told whether these directories are auto-created by agents or must be manually created | Actionability |
| DA-007-qg2 | Troubleshooting tables omit Claude Code API / authentication failures | Minor | All four documents' troubleshooting sections assume Claude Code is functional. No entry covers expired API keys, rate limiting, network errors, or model availability issues -- all of which would present as opaque failures during skill invocation. | Completeness |
| DA-008-qg2 | Windows PowerShell instructions are included but untested | Minor | `getting-started.md` provides parallel PowerShell commands (lines 42-43, 53-54, 72, 82) but no other document provides Windows instructions. The orchestration, problem-solving, and transcript playbooks all use Unix-only syntax. This creates an inconsistent cross-platform story. | Internal Consistency |
| DA-009-qg2 | Circuit breaker behavior in creator-critic cycle is vague | Minor | `problem-solving.md` lines 167-168: "After the minimum 3 iterations, if no improvement occurs over 2 consecutive cycles, the agent will either accept the deliverable with caveats documented or escalate to the user" -- "either/or" without specifying when each path is taken removes user predictability | Methodological Rigor |
| DA-010-qg2 | Cross-reference links use relative paths that assume specific directory structure | Minor | All four documents use relative links (e.g., `../../skills/problem-solving/SKILL.md`, `../playbooks/orchestration.md`). If a user reads these documents on GitHub (rendered Markdown) from a fork with a different directory depth, links break. | Traceability |

---

## Finding Details

### DA-001-qg2: Phantom Prerequisite -- `INSTALLATION.md` Does Not Exist [MAJOR]

**Claim Challenged:** `getting-started.md` line 19: "You have completed the Jerry installation documented in [`../INSTALLATION.md`](../INSTALLATION.md). Do not proceed until all three criteria below are met."

**Counter-Argument:** The Getting Started runbook's first sentence sends the user to a document that does not exist in the repository. This creates a dead-end at step zero of the onboarding path. A user following instructions exactly will click the link, get a 404, and have no way to proceed. The three prerequisite checks (uv installed, Jerry cloned, plugin installed) are listed but the "how to achieve them" document is missing. This is not a formatting issue -- it is a structural completeness gap in the onboarding funnel.

**Evidence:** Repository search for `INSTALLATION.md` in `docs/` returns no results. The relative path `../INSTALLATION.md` from `docs/runbooks/` would resolve to `docs/INSTALLATION.md`, which does not exist.

**Impact:** A new user's onboarding path is blocked at the first step. The three prerequisite checks cannot be achieved without installation instructions. This directly undermines the Getting Started runbook's stated purpose: "go from a freshly installed Jerry instance to your first successful skill invocation."

**Dimension:** Completeness (0.20 weight)

**Response Required:** Either create `docs/INSTALLATION.md` with the installation procedure (uv installation, Jerry clone, plugin registration), or inline the installation steps into the Getting Started runbook's Prerequisites section. The reference to a non-existent document must be resolved.

**Acceptance Criteria:** The Getting Started runbook must have a complete, self-contained or correctly-linked path from "I have nothing installed" to "all three prerequisites are met." Every hyperlink in the Prerequisites section must resolve to an existing document.

---

### DA-002-qg2: No Error Recovery Paths for Mid-Workflow Failures [MAJOR]

**Claim Challenged:** `orchestration.md` Troubleshooting table (lines 242-251) and `transcript.md` Troubleshooting table (lines 199-209) present troubleshooting entries that cover pre-start failures (wrong env var, missing files) and post-completion issues (stale state, quality threshold) but omit the most common failure mode: an agent fails mid-execution.

**Counter-Argument:** Real-world usage of multi-phase workflows involves agents that can fail partway through execution -- due to context window exhaustion, API rate limits, model errors, or unexpected input data. When this happens, the user is left with a partially-written artifact, a YAML state file that may or may not reflect the failure, and no documented procedure for recovery. The orchestration playbook's Step 5 ("Update state after each agent") assumes agents complete successfully. The transcript playbook's Phase 2-5 pipeline has no documented fallback if ts-extractor produces partial output.

**Evidence:**
- `orchestration.md` troubleshooting: 7 entries, none for "agent failed mid-execution with partial output"
- `transcript.md` troubleshooting: 7 entries, one covers `canonical-transcript.json` being read (a specific error) but none for "Phase 2 agent failed partway through chunk processing"
- `problem-solving.md` troubleshooting: 7 entries, the closest is "Creator-critic cycle runs more than 5 times" which covers slow convergence, not agent failure

**Impact:** When an agent fails mid-phase (which will happen in practice, especially for large transcripts or complex orchestrations), the user has no documented recovery path. They may: (a) re-run the entire workflow from scratch (wasteful), (b) manually edit YAML state to skip the failed phase (error-prone, undocumented), or (c) abandon the workflow. All three outcomes degrade the user experience and waste resources.

**Dimension:** Actionability (0.15 weight)

**Response Required:** Add at least one troubleshooting entry per playbook covering mid-execution agent failure. For the orchestration playbook, document how to use checkpoint recovery to resume from the last successful phase. For the transcript playbook, document that Phase 1 output (chunks) can be reused and only Phase 2+ needs re-running if a semantic agent fails.

**Acceptance Criteria:** Each playbook's troubleshooting table must include an entry for "agent fails mid-execution" with: (1) how to identify the failure state, (2) which artifacts can be salvaged, and (3) the specific recovery command or procedure.

---

### DA-003-qg2: Keyword Activation Model Presented as Deterministic but Is Not [MAJOR]

**Claim Challenged:** `problem-solving.md` line 64: "State your request in natural language, using one of the trigger keywords: research, analyze, investigate, explore, root cause, or why." `orchestration.md` line 28: "use the keyword orchestration in your request to trigger automatic invocation."

**Counter-Argument:** The documentation presents keyword-to-skill activation as a reliable, deterministic mapping. In reality, LLM-based keyword detection is probabilistic. A message containing multiple trigger keywords from different skills (e.g., "I want to research and orchestrate an analysis pipeline") creates ambiguity. The documentation does not acknowledge this non-determinism, does not explain what happens when keywords conflict, and does not provide a fallback mechanism beyond the problem-solving playbook's brief mention of explicit agent naming (line 78-84). The orchestration playbook has no equivalent explicit invocation path. A user who trusts the documentation's implied determinism will be confused when the wrong skill activates.

**Evidence:**
- `problem-solving.md` lines 117-127: Agent Selection Table maps keywords to agents but does not address multi-keyword ambiguity
- `orchestration.md` lines 28-36: Lists 6 trigger keywords but does not explain priority ordering when multiple match
- Neither document mentions `/problem-solving` or `/orchestration` as explicit slash-command alternatives that bypass keyword detection

**Impact:** Users who craft requests with multiple trigger keywords will get unpredictable skill activation. The documentation creates a false sense of reliability that will lead to confusion and wasted iterations.

**Dimension:** Evidence Quality (0.15 weight)

**Response Required:** (1) Add a disambiguation note acknowledging that keyword detection is probabilistic, (2) document what happens when keywords from multiple skills appear in the same request, and (3) provide an explicit invocation path (slash commands or direct agent naming) as the reliable alternative in all playbooks, not just problem-solving.

**Acceptance Criteria:** Each playbook must include either a disambiguation section or a note acknowledging non-deterministic keyword detection, plus an explicit invocation syntax that guarantees the intended skill is activated.

---

### DA-004-qg2: Cost and Accuracy Implications of SRT/TXT Parsing Understated [MAJOR]

**Claim Challenged:** `transcript.md` Input Formats table (lines 245-249) presents VTT, SRT, and plain text as three equivalent input format options. The Step-by-Step section states VTT uses a Python parser that is "1,250x cheaper than LLM parsing" (line 75), but the Input Formats section -- where a user would make their format selection decision -- does not restate this differential.

**Counter-Argument:** The cost and accuracy differential between VTT (deterministic, cheap, accurate) and SRT/TXT (LLM-based, expensive, non-deterministic) is a factor of 1,250x in cost and introduces non-deterministic timestamp accuracy. A user who has both a VTT and SRT version of the same meeting would not know from the Input Formats table that choosing VTT is dramatically better. The information asymmetry between the Step-by-Step section (which mentions the differential once in passing) and the Input Formats section (which omits it entirely) means users making decisions at the point of format selection lack the critical data to make an informed choice.

**Evidence:**
- `transcript.md` line 75-76: "1,250x cheaper than LLM parsing and produces 100% accurate timestamps" -- stated only in Step-by-Step context
- `transcript.md` lines 245-249: Input Formats table has columns for Format, Extension, Parsing Method, and Notes -- but the Notes column does not mention cost or accuracy differential
- `transcript.md` line 247: VTT Notes say "MUST use CLI" but do not say "strongly preferred over SRT/TXT"

**Impact:** Users with access to multiple format options (common with Zoom, which can export both VTT and SRT) will make a sub-optimal choice if they consult the Input Formats table without reading the entire Step-by-Step section. This could result in 1,250x higher token costs and reduced timestamp accuracy for no reason.

**Dimension:** Completeness (0.20 weight)

**Response Required:** Add a cost/accuracy note to the Input Formats table or section that explicitly states VTT is the strongly preferred format when available, with a quantified comparison. The information must be present at the decision point, not buried in a procedural section above.

**Acceptance Criteria:** The Input Formats section must contain a visible note or table annotation stating: (1) VTT is preferred when available, (2) the cost differential (quantified), and (3) the accuracy differential (deterministic vs. non-deterministic).

---

### DA-005-qg2: No Version or Compatibility Information for Tool Dependencies [MAJOR]

**Claim Challenged:** `getting-started.md` line 21: "uv is installed and on your PATH -- confirm with `uv --version`". All four documents reference `uv`, `jerry`, Claude Code, and the Jerry plugin without specifying version requirements.

**Counter-Argument:** OSS documentation that omits version compatibility information creates a latent failure mode. When `uv` releases a breaking change, when the Jerry CLI modifies its command structure, or when Claude Code changes its plugin API, every instruction in these documents becomes unreliable without any version pin to anchor against. The Getting Started runbook instructs the user to run `uv --version` but never states what version is acceptable. The Jerry CLI commands (e.g., `jerry session start`, `jerry transcript parse`) are presented without version context. A user following these instructions 6 months after writing may encounter breaking changes with no diagnostic path.

**Evidence:**
- `getting-started.md` line 21: Checks `uv --version` but specifies no minimum version
- `transcript.md` line 62: "verify with uv run jerry --help" -- does not specify Jerry CLI version
- No document mentions Claude Code version requirements or plugin API compatibility
- None of the four documents contain a "Tested with" or "Compatibility" section

**Impact:** Over time, as dependencies evolve, the documentation will silently drift from accuracy. Users will encounter errors that are not caused by their actions but by version incompatibility, with no way to diagnose the root cause from the documentation alone. This is a classic OSS documentation decay failure mode.

**Dimension:** Evidence Quality (0.15 weight)

**Response Required:** Add version information to the Getting Started runbook at minimum. State the Jerry CLI version these instructions were tested against, the minimum `uv` version required, and the Claude Code version or API compatibility assumption.

**Acceptance Criteria:** At least the Getting Started runbook must include a "Tested With" or "Compatibility" note listing specific versions of `uv`, `jerry` CLI, and Claude Code that the instructions have been verified against.

---

## Recommendations

### P0 -- Critical (MUST resolve before acceptance)

None. No Critical findings identified.

### P1 -- Major (SHOULD resolve; justification required if not)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-001-qg2 | Create `docs/INSTALLATION.md` or inline installation steps into `getting-started.md` Prerequisites | All hyperlinks in Prerequisites resolve to existing documents; a user can achieve all 3 prerequisites by following the linked instructions |
| DA-002-qg2 | Add "agent fails mid-execution" troubleshooting entry to each playbook's troubleshooting table | Each playbook has an entry covering: failure identification, artifact salvage, and recovery procedure |
| DA-003-qg2 | Add disambiguation note and explicit invocation syntax to all playbooks | Each playbook acknowledges non-deterministic keyword detection and provides a guaranteed-activation syntax |
| DA-004-qg2 | Add cost/accuracy note to the transcript playbook's Input Formats section | Input Formats section states VTT is preferred, quantifies cost differential, and notes accuracy difference |
| DA-005-qg2 | Add "Tested With" version information to at minimum the Getting Started runbook | Runbook lists specific versions of `uv`, `jerry` CLI, and Claude Code that instructions were verified against |

### P2 -- Minor (MAY resolve; acknowledgment sufficient)

| ID | Action | Acceptance Criteria |
|----|--------|---------------------|
| DA-006-qg2 | Clarify whether output directories (`docs/research/`, etc.) are auto-created by agents or require manual creation | Statement in problem-solving playbook's Step-by-Step or Prerequisites indicating whether directory creation is automatic |
| DA-007-qg2 | Add a troubleshooting entry for Claude Code API/authentication failures | At least the Getting Started runbook's troubleshooting table includes an entry for API key or authentication errors |
| DA-008-qg2 | Harmonize cross-platform support: either provide Windows instructions in all four documents or explicitly state "Unix/macOS only" for playbooks | Consistent cross-platform posture across all four documents |
| DA-009-qg2 | Specify circuit breaker behavior for the creator-critic cycle | `problem-solving.md` states the specific condition that determines "accept with caveats" vs. "escalate to user" |
| DA-010-qg2 | Consider adding a note about relative link behavior on GitHub forks | Acknowledgment that relative links assume the standard Jerry directory structure |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-001-qg2: Missing `INSTALLATION.md` creates a hole at the start of the onboarding funnel. DA-004-qg2: Cost/accuracy differential missing from the decision-point section. DA-007-qg2: API failure mode absent from troubleshooting. |
| Internal Consistency | 0.20 | Slightly Negative | DA-008-qg2: Windows instructions present in getting-started but absent from all three playbooks creates a cross-platform inconsistency. Otherwise the four documents are well-aligned. |
| Methodological Rigor | 0.20 | Neutral | DA-009-qg2: Minor vagueness in circuit breaker specification. The overall procedural structure (step-by-step, troubleshooting tables, prerequisites) is methodologically sound across all four documents. |
| Evidence Quality | 0.15 | Negative | DA-003-qg2: Keyword activation presented as deterministic without evidence or caveat. DA-005-qg2: No version information anchors the instructions to a tested configuration. Claims about tool behavior lack version-specific evidence. |
| Actionability | 0.15 | Negative | DA-002-qg2: No mid-workflow failure recovery documented. DA-006-qg2: Ambiguity about directory auto-creation. Users following instructions may hit a wall at failure points with no documented recovery. |
| Traceability | 0.10 | Neutral | DA-010-qg2: Minor relative-link concern. All four documents trace well to their SKILL.md authoritative references and cross-reference each other appropriately. |

**Overall Assessment:** The documentation set is structurally robust and demonstrates strong internal consistency, good cross-referencing, and clear procedural organization. The 5 Major findings target genuine gaps that would cause real user pain -- particularly DA-001 (phantom prerequisite blocking step zero) and DA-002 (no recovery from the most common real-world failure mode). Addressing the Major findings would move the set from a well-organized but optimistic-path-only documentation to resilient, production-grade OSS documentation. Estimated score impact of addressing all Major findings: +0.03 to +0.05 composite improvement.

---

<!-- VALIDATION: S-002 Devil's Advocate execution checklist
- [x] Step 1: Role assumption documented (deliverable, criticality, H-16 compliance)
- [x] Step 2: Assumptions inventory (3 explicit, 6 implicit, all challenged)
- [x] Step 3: 10 counter-arguments with DA-NNN-qg2 identifiers, severity, evidence, dimension mapping
- [x] Step 4: Response requirements with acceptance criteria for all 5 Major findings
- [x] Step 5: Scoring impact table with 6 dimensions, overall assessment, revision guidance
- [x] H-16 compliance: S-003 Steelman confirmed via 3-iteration creator-critic cycle (score 0.937)
- [x] Minimum 3 counter-arguments: 10 generated (5 Major, 5 Minor)
- [x] All 6 counter-argument lenses applied across findings
- [x] Finding prefix DA-NNN-qg2 used consistently
-->
