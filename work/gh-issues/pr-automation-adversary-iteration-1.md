# C4 Tournament Adversarial Review: Claude Code PR Automation Issue
## Iteration 1 — Baseline Assessment

> **Execution ID:** it1
> **Criticality Level:** C4 (Critical — governance-adjacent, pre-OSS-release, public-facing)
> **Strategy Set:** All 10 (S-003, S-014, S-013, S-007, S-002, S-004, S-010, S-012, S-011, S-001)
> **H-16 Compliance:** S-003 executed FIRST per requirement
> **H-15 Compliance:** Self-review applied before persistence
> **C4 Threshold:** >= 0.95 weighted composite
> **Leniency Bias:** ACTIVE counteraction — scored against absolute standard, not "first draft" standard
> **Agent:** adv-executor (convergent cognitive mode)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Tournament metadata |
| [S-003 Steelman](#s-003-steelman-technique) | Constructive strengthening — FIRST per H-16 |
| [S-010 Self-Refine](#s-010-self-refine) | Creator-perspective self-review |
| [S-007 Constitutional AI](#s-007-constitutional-ai-critique) | Constitutional and HARD rule compliance |
| [S-013 Inversion](#s-013-inversion-technique) | Assumption stress-test via inversion |
| [S-002 Devil's Advocate](#s-002-devils-advocate) | Counter-argument construction |
| [S-004 Pre-Mortem](#s-004-pre-mortem-analysis) | Prospective failure analysis |
| [S-012 FMEA](#s-012-fmea) | Component-level failure mode decomposition |
| [S-011 Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification |
| [S-001 Red Team](#s-001-red-team-analysis) | Adversarial threat emulation |
| [S-014 LLM-as-Judge](#s-014-llm-as-judge-scoring) | Weighted composite scoring |
| [Tournament Verdict](#tournament-verdict) | Final verdict and recommendations |
| [Revision Recommendations](#revision-recommendations) | Ordered actionable improvements |

---

## Execution Context

- **Strategy:** C4 Tournament — All 10 strategies
- **Template Path:** `.context/templates/adversarial/`
- **Deliverable:** `work/gh-issues/issue-claude-code-pr-automation.md`
- **Deliverable Type:** GitHub Issue Draft (research/strategy request)
- **Executed:** 2026-02-25
- **Execution ID:** it1

**Deliverable Summary:** A GitHub Issue requesting research and strategy evaluation for deploying Claude Code instances as autonomous PR listeners and issue-driven workers. Written in Saucer Boy voice. Defines 4 core capabilities (C1-C4), 5+ required deployment strategies, Jerry integration requirements, explicit exclusions, and 8 acceptance criteria.

---

## S-003: Steelman Technique

*Finding Prefix: SM-NNN-it1 | Strategy: Constructive strengthening | Required at C4, FIRST per H-16*

### Step 1: Charitable Interpretation Summary

**Core thesis:** The deliverable argues that Claude Code's current "single-player" limitation is a capability gap in multi-PR/issue concurrency, and that the solution is a research-first approach to evaluate the best dispatch architecture before committing to implementation. The strongest interpretation: this is a scope-bounded, pre-implementation scouting issue that correctly defers architectural decisions to research outcomes.

**Key claims:**
1. The capability gap is dispatch, not intelligence — Claude Code can do the work; it cannot self-trigger
2. The problem space requires parallel instances (N-concurrent workers), not serial execution
3. Jerry integration is non-negotiable and must be first-class in any strategy
4. The issue deliberately scopes OUT implementation, CI/CD, and multi-repo support

**Strengthening opportunities (presentation, not substantive):**
- The "Why now" section is strong but the urgency argument could be sharpened with concrete data
- The acceptance criteria are well-structured but one criterion is underspecified (criteria #8 re: Claude Code feature verification)
- The strategy evaluation matrix lacks a weighting or prioritization signal for the dimensions
- The Jerry integration section has a gap: no mention of worktree isolation per MEMORY.md convention

### Step 2: Weakness Classification

| Type | Weakness | Magnitude |
|------|---------|-----------|
| Evidence | No quantitative benchmark for "success" (e.g., what latency from comment to commit is acceptable?) | Major |
| Structural | Strategy evaluation matrix has 10 dimensions but no signal about relative importance — all appear equal | Major |
| Structural | Jerry integration omits worktree isolation (MEMORY.md worktree convention critical for concurrent instances) | Critical |
| Evidence | No definition of "full Jerry session" as applied to automated instances (JERRY_PROJECT assignment logic unspecified) | Major |
| Presentation | "Circuit breaker" in C4 constraint says "suggest max 10 rounds" — weak language for a MUST constraint | Minor |
| Structural | Strategy 3 framing ("Claude Code SDK / Claude Agent SDK") acknowledges uncertainty about SDK state but accepts that uncertainty as normal — could be strengthened with explicit dependency flag | Minor |
| Evidence | The acceptance criterion for "verified vs. assumed" Claude Code features lacks a template or format specification | Minor |

### Step 3: Steelman Reconstruction

**SM-001-it1:** The worktree isolation requirement is the strongest version of the Jerry integration story. For N concurrent instances, each working on a different PR branch, file system isolation via worktrees (per `git worktree add`) is not optional — it prevents catastrophic file conflicts between instances. The steelmanned version explicitly requires: each instance MUST operate in an isolated git worktree, worktrees MUST be named per the MEMORY.md convention (`~/workspace/github/{repo}-wt/{branch}`), and the strategy must define how worktrees are created, monitored, and cleaned up.

**SM-002-it1:** The evaluation matrix becomes stronger with a signal of dimension weighting. Jerry integration, Security, and Reliability are existential — a strategy that scores poorly on these is disqualifying regardless of Architecture score. The steelmanned version adds a "tier" classification to the dimension matrix: Tier 1 (must pass: Jerry integration, Security, Reliability), Tier 2 (evaluate trade-offs: Architecture, Deployment model, Scalability), Tier 3 (inform decision: Cost, Complexity, Latency, Limitations).

**SM-003-it1:** The Claude Code capability audit (Approach step 1) is the strongest idea in the issue but is underemphasized. The steelmanned version elevates this to a prerequisite gate: if the capability audit reveals that Claude Code cannot operate headless/non-interactive at all, the entire issue scope is moot. This should be framed as "Phase 0" that must complete before Phase 1 (strategy research).

**SM-004-it1:** The JERRY_PROJECT assignment logic is critical for concurrent instances and needs specification. The steelmanned version proposes three models for evaluation: (a) per-repo project (one JERRY_PROJECT per repository, all instances share it), (b) per-instance project (each automated instance gets its own transient project), (c) per-PR project (each PR gets its own project, enabling PR-scoped artifact isolation). The issue should require the research to evaluate which model is viable.

### Step 4: Best Case Scenario

**Ideal conditions:** This issue is strongest when: (1) Claude Code's headless execution capability is confirmed before research begins, (2) the research team has hands-on access to all 5 strategy platforms (GitHub Actions, Docker, SDK, serverless, K8s), (3) Jerry worktree conventions are treated as architectural constraints on all strategies.

**Key assumptions that must hold:**
- Claude Code can be invoked non-interactively (without terminal attachment)
- `JERRY_PROJECT` can be set per-process, not just per-session
- Git worktree operations are safe under concurrent instance scenarios

**Confidence assessment:** 0.75. The issue is well-conceived but has addressable gaps that could significantly affect research scope if discovered mid-execution.

### Improvement Findings Table (S-003)

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|---------|---------|-------------|---------|
| SM-001-it1 | Missing worktree isolation requirement for concurrent instances | Critical | No mention of worktree isolation | Explicit worktree isolation per MEMORY.md convention required for each instance | Completeness |
| SM-002-it1 | Strategy evaluation matrix has no dimension weighting/tiering | Major | All 10 dimensions appear equally weighted | Tier 1/2/3 classification: Jerry integration/Security/Reliability are must-pass | Methodological Rigor |
| SM-003-it1 | Capability audit underemphasized — should be Phase 0 gate | Major | Step 1 of Approach section | Promoted to prerequisite gate before research begins | Actionability |
| SM-004-it1 | JERRY_PROJECT assignment models not specified | Major | "Strategy must define how projects are assigned" | Three concrete models proposed for research evaluation | Evidence Quality |
| SM-005-it1 | Circuit breaker language in C4 uses "suggest" not "MUST" | Minor | "suggest max 10 rounds per comment thread" | "MUST NOT exceed 10 rounds per comment thread (circuit breaker)" | Internal Consistency |
| SM-006-it1 | Acceptance criterion 8 lacks format specification | Minor | "explicitly states which features were verified vs. assumed" | Add required format: table with Feature/Verified/Source columns | Actionability |

---

## S-010: Self-Refine

*Finding Prefix: SR-NNN-it1 | Strategy: Creator-perspective self-review | Required C1+, H-15 compliance*

### Protocol Execution

**Reviewing through the creator's lens — what would I catch if I had written this?**

**Step 1: Structural completeness check**
The document has a navigation table (H-23 compliant), clear sections, and proper markdown formatting. All 8 AC items are checkboxes. The body flows logically from vision → motivation → capabilities → strategy requirements → strategy set → Jerry integration → exclusions → AC → approach → rationale.

**Gap found:** The navigation table lists "Body: Strategy requirements" but the actual heading is "Strategy requirements" (not prefixed with "Body:"). The anchor link in the nav table points to `#strategy-requirements` which matches, so this is a presentation inconsistency, not a broken link.

**Step 2: Internal consistency check**
- Core capabilities are numbered C1-C4, which collides with the Jerry framework's C1-C4 criticality levels. A reader of this issue who is familiar with Jerry's framework will experience confusion when reading "C1: PR Comment Listening" vs. "C4: Critical" criticality.
- Acceptance criterion #4 references "quantitative data where available (cost estimates, latency ranges, concurrency limits)" but the Strategy requirements section calls for cost and latency as evaluation dimensions without specifying what "quantitative" means. No ranges or orders-of-magnitude anchoring provided.
- Strategy 3 title says "Claude Code SDK / Claude Agent SDK" — these are different products with different APIs. The conflation is acknowledged ("the current state of the Claude Code SDK / Agent SDK") but not resolved.

**Step 3: Scope boundary check**
The exclusions section is crisp and well-scoped. However: "No modifications to Claude Code itself" conflicts with the fact that some strategies (particularly Strategy 4: GitHub App) may require GitHub App installation which involves configuring Claude Code's behavior via environment variables or config files. This is not "modifying Claude Code" but the boundary is blurry.

**Step 4: Voice check (Saucer Boy)**
The Saucer Boy voice is present and effective in "The vision" and "Why now" sections. The middle sections (Core capabilities, Strategy requirements, Jerry integration) are more technical and dry — appropriate for specificity, but the voice drops entirely. The Approach section has some voice ("scouting run," "terrain") but it's sparse compared to the opening. This is likely acceptable for a GitHub Issue, but inconsistent.

**Step 5: Actionability check**
Each of the 5 required strategies has "Key questions to answer" which is excellent. The acceptance criteria are verifiable. The Approach section provides a clear 7-step workflow. However, no time estimate or priority ordering is given for the research work — the issue doesn't indicate whether strategies should be researched in the listed order or in parallel.

### Self-Refine Findings

| ID | Description | Severity | Section | Dimension |
|----|-------------|---------|---------|-----------|
| SR-001-it1 | Core capability labels C1-C4 collide with Jerry criticality levels C1-C4 — major confusion risk for Jerry practitioners | Major | Core capabilities | Internal Consistency |
| SR-002-it1 | Strategy 3 conflates Claude Code SDK with Claude Agent SDK without resolving the distinction | Major | Minimum strategy set | Internal Consistency |
| SR-003-it1 | No time estimate or research priority ordering — implementer cannot sequence work | Minor | Approach | Actionability |
| SR-004-it1 | Quantitative data expected in AC#4 but no anchoring ranges provided (what order-of-magnitude cost is acceptable?) | Minor | Acceptance criteria | Evidence Quality |

---

## S-007: Constitutional AI Critique

*Finding Prefix: CC-NNN-it1 | Strategy: Constitutional and HARD rule compliance | Required C2+*

### Constitutional Compliance Check

**Evaluating against Jerry HARD rules and constitutional principles:**

**H-23 (Markdown navigation table):** PASS. Navigation table present with anchor links.

**H-31 (Clarify when ambiguous):** Partial PASS. The issue is itself a clarification document — it specifies scope clearly. However, the issue does not clarify whether "research" includes proof-of-concept prototyping or is documentation-only. This matters: running a GitHub Actions workflow or deploying a test Docker container is categorically different from writing about it. The distinction should be explicit.

**H-32 (GitHub Issue parity):** N/A — this IS the GitHub Issue being drafted. The internal worktracker entity presumably exists.

**H-04 (Active project REQUIRED):** The issue mentions JERRY_PROJECT requirements for the deployed instances but does not specify which project this research issue itself belongs to. This is a meta-gap: the issue that researches Jerry project assignment for automated instances doesn't specify its own project.

**Jerry Constitution alignment:**
- The issue is about external automation infrastructure — it must not create a mechanism that bypasses Jerry's quality enforcement, worktracker requirements, or constitutional constraints. The acceptance criterion that "Instances MUST follow .context/rules/ quality standards" is constitutionally correct but underspecified: which quality enforcement mechanisms work in automated contexts without human escalation paths?

**P-003 implications for the research scope:**
- The issue asks for research into "multi-instance orchestration." Any architecture where instances spawn sub-instances would violate P-003 (max 1 level of recursion). The issue should explicitly require that each evaluated strategy respect P-003 — currently the "C3: Multi-Instance Orchestration" section allows N instances from a human dispatcher, which is fine, but doesn't preclude instance-spawning-instance architectures that would violate P-003.

**P-022 (No deception) implications:**
- Acceptance criterion 8 ("explicitly states which Claude Code features were verified vs. assumed") is the correct P-022 implementation for this research context. This is well-designed.

**H-13/H-14 (Quality gate for the RESEARCH OUTPUT):**
- The issue does not specify quality gate requirements for the research output itself. If this is a C3+ research output, it should be subject to quality enforcement. The acceptance criteria are functional but don't specify a quality gate threshold or adversarial review requirement for the research deliverable.

### Constitutional Findings

| ID | Description | Severity | Section | Constitutional Rule |
|----|-------------|---------|---------|-------------------|
| CC-001-it1 | Research vs. prototyping boundary unspecified — does "research" include deploying test infrastructure? | Major | Approach | H-31 (Clarify when ambiguous) |
| CC-002-it1 | P-003 compliance not required of evaluated strategies — multi-instance orchestration could include instance-spawns-instance architectures | Critical | Core capabilities (C3) | P-003, H-01 |
| CC-003-it1 | Quality gate for research output not specified — no S-014 scoring requirement for the deliverable produced by this issue | Major | Acceptance criteria | H-13, H-17 |
| CC-004-it1 | Human escalation path for automated instances not defined — quality enforcement works differently without a human in the loop | Major | Jerry integration requirements | H-19, P-020 |
| CC-005-it1 | Issue's own JERRY_PROJECT not specified — the research issue belongs to no stated project | Minor | (Issue metadata) | H-04 |

---

## S-013: Inversion Technique

*Finding Prefix: IN-NNN-it1 | Strategy: Assumption stress-test via inversion | Required C3+*

### Inversion Protocol

**The deliverable succeeds if the research produces actionable deployment strategies for Claude Code PR automation with full Jerry integration. Now invert: How does this spectacularly fail?**

**Inversion 1: What if Claude Code cannot operate headlessly?**

The entire issue assumes Claude Code can be invoked non-interactively — in a GitHub Actions runner, in a Docker container, in a serverless function — without a terminal session. If this assumption is false, ALL 5 strategies fail simultaneously. The issue does mention "Audit current Claude Code capabilities" as Step 1 of the Approach, but it is listed as a research step, not a go/no-go gate. If Claude Code requires interactive terminal attachment for JERRY_PROJECT and jerry session start, none of the proposed strategies work at all.

**Finding IN-001-it1:** The capability audit is not framed as a blocking prerequisite — if headless execution is impossible, the entire research scope is invalidated.

**Inversion 2: What if Jerry's quality enforcement blocks automated instances?**

Jerry's quality enforcement includes human escalation paths (H-19, AE-006). If an automated Claude Code instance reaches a CRITICAL context fill level or hits a governance escalation condition, it must "escalate to human" — but there's no human attached. The issue says instances must follow quality enforcement but doesn't invert this: what happens when quality enforcement requires human input that no human is providing? The automated instance could loop forever, crash, or worse — skip the escalation and continue with degraded quality.

**Finding IN-002-it1:** Quality enforcement escalation paths assume human presence. Automated instances need a defined "headless escalation" protocol — not addressed.

**Inversion 3: What if the JERRY_PROJECT model creates worktracker conflicts?**

If multiple Claude Code instances run concurrently against the same `JERRY_PROJECT`, they may write conflicting worktracker entries simultaneously. The issue says "strategy must define how artifacts from N concurrent instances avoid conflicts" — but this is listed as an acceptance criterion, not a design constraint that each strategy must satisfy concretely. The inversion: what if the Jerry worktracker data model simply doesn't support concurrent write safety? The research might conclude "use per-instance projects" but that creates a different problem: no aggregate worktracker view across instances.

**Finding IN-003-it1:** Worktracker concurrency conflict is framed as "something strategies must address" without acknowledging that this may be an architectural limitation of the current Jerry data model requiring a change.

**Inversion 4: What if the open-source context changes the security model?**

The "Why now" section links this to OSS release. Post-OSS, external contributors will open PRs and issues. An automated Claude Code instance responding to external contributor comments is a significantly different security surface than an internal team scenario. The inversion: a malicious contributor could craft a PR comment designed to make Claude Code execute arbitrary code or exfiltrate secrets. The issue's security dimension in the strategy matrix mentions "API key management, secret handling, repository permissions, least-privilege analysis" but does not include adversarial input handling from untrusted external sources.

**Finding IN-004-it1:** Post-OSS adversarial input from external contributors is not listed as a security consideration — a critical gap given the "Why now" rationale is explicitly OSS-release.

**Inversion 5: What if all 5 strategies are evaluated and none are viable?**

The issue's acceptance criteria assume at least one strategy will emerge as recommendable. The inversion: what if the capability audit (Step 1) reveals that Claude Code headless execution is limited, and after full evaluation, no strategy is viable without modifications to Claude Code itself (which the issue explicitly excludes)? The issue doesn't define a decision path for "research concludes: not feasible without Claude Code changes." This is a possible valid research outcome that the issue doesn't acknowledge.

**Finding IN-005-it1:** No "infeasibility" outcome path defined — the issue assumes research will produce a viable recommendation, not that it might conclude "not feasible today."

### Inversion Findings

| ID | Description | Severity | Inverted Assumption |
|----|-------------|---------|-------------------|
| IN-001-it1 | Capability audit not a go/no-go gate — headless Claude Code is an unvalidated prerequisite | Critical | "Claude Code can run headlessly" |
| IN-002-it1 | Quality enforcement escalation assumes human presence — automated instances have no headless escalation protocol | Critical | "Quality enforcement works without human in the loop" |
| IN-003-it1 | Worktracker concurrency may be a fundamental data model limitation, not a strategy design choice | Major | "Concurrent worktracker writes can be resolved by strategy design" |
| IN-004-it1 | OSS post-release adversarial inputs from external contributors not addressed in security model | Critical | "Security threat model is internal team use only" |
| IN-005-it1 | No infeasibility outcome path — research could validly conclude "not feasible today" | Major | "Research will produce a viable recommendation" |

---

## S-002: Devil's Advocate

*Finding Prefix: DA-NNN-it1 | Strategy: Counter-argument construction | Required C2+, H-16 satisfied*

### H-16 Compliance

S-003 Steelman was applied first. Proceeding with adversarial critique of the steelmanned version.

### Assumption Extraction and Challenge

**Explicit Assumptions:**
1. Claude Code can be invoked programmatically without interactive terminal
2. Jerry sessions can run unattended without human oversight
3. Five strategies are sufficient for comprehensive evaluation
4. The research scope is achievable without implementation
5. Claude Code SDK is a viable option (despite uncertain state)

**Implicit Assumptions:**
1. GitHub's webhook/Actions infrastructure is suitable for low-latency PR response
2. Worktree-based isolation is sufficient to prevent instance interference
3. JERRY_PROJECT can be meaningfully assigned per automated instance
4. Quality enforcement (including human escalation hooks) can be adapted for automated contexts
5. The OSS-release timeline makes this research urgent rather than exploratory

**Counter-Arguments:**

**DA-001-it1 (Major — Internal Consistency):** The issue claims to be a "research only" scope but mandates that strategies "address all four core capabilities with specific architectural detail — not just 'this is possible' but *how* it works." That level of architectural specificity cannot be produced without at minimum proof-of-concept validation. Writing detailed "how C1 works in GitHub Actions" without running a GitHub Actions workflow is speculation, not research. The issue conflates documentation-depth with implementation-validation.

**DA-002-it1 (Critical — Completeness):** The issue requires research into 5+ strategies against 10 dimensions. That's 50+ evaluation cells, each requiring specific architectural detail, quantitative data "where available," and concrete Jerry integration analysis. A competent researcher could spend 40+ hours on this. The issue has no scope management mechanism — no prioritization between strategies, no indication of which cells are "must have" vs. "nice to have," no definition of "sufficient research depth." This is a recipe for open-ended research that never converges.

**DA-003-it1 (Major — Methodological Rigor):** Strategy 3 ("Claude Code SDK / Claude Agent SDK Custom Orchestrator") acknowledges that "the current state of the Claude Code SDK / Agent SDK" is uncertain. If the SDK is not publicly available, documented, or stable, this strategy cannot be meaningfully evaluated. Including it in the required set of 5 strategies when its foundational premise may be unresearchable is methodologically weak. The issue should either (a) define fallback research approach if the SDK is not accessible, or (b) make Strategy 3 conditional on SDK availability.

**DA-004-it1 (Major — Evidence Quality):** The "Why now" urgency argument relies on "Jerry is preparing for open-source release" — but open-source release of Jerry doesn't automatically generate PR volume requiring Claude Code automation. The urgency argument would be stronger with concrete data: how many PRs/month does the maintainer anticipate? What review latency is acceptable? The absence of quantitative grounding makes "Why now" feel like a framing choice rather than a data-driven assessment.

**DA-005-it1 (Minor — Actionability):** The Approach section's Step 7 says "Submit PR with findings." This means the research output is a PR. But the issue is opened on the OSS repository (implied by "oss-prep" label), and the research artifacts should go somewhere specific. Where? What's the target directory structure? The Approach section is operationally incomplete.

### Devil's Advocate Findings

| ID | Description | Severity | Counter-Argument |
|----|-------------|---------|----------------|
| DA-001-it1 | Research-only scope conflicts with required "how it works" specificity — this level of detail requires implementation/PoC | Major | Internal Consistency |
| DA-002-it1 | 50+ evaluation cells without scope management — research will not converge | Critical | Completeness |
| DA-003-it1 | Strategy 3 (SDK) may be unresearchable if SDK not publicly available — required strategy on uncertain premises | Major | Methodological Rigor |
| DA-004-it1 | Urgency argument lacks quantitative grounding — no PR volume or latency target data | Major | Evidence Quality |
| DA-005-it1 | Approach Step 7 incomplete — research output target directory not specified | Minor | Actionability |

---

## S-004: Pre-Mortem Analysis

*Finding Prefix: PM-NNN-it1 | Strategy: Prospective failure analysis | Required C3+, H-16 satisfied*

### Prospective Hindsight Protocol

**The research issue has been executed. Six months after the PR is merged, the project is in chaos. The research produced nothing actionable. What went wrong?**

**Failure Scenario 1: The Research Never Converged**

The implementer spent 80 hours researching all 5 strategies in equal depth. Each strategy writeup is thorough but the comparison matrix has no winner because all strategies have different strengths. The recommendation section says "it depends" on factors not determined by the research (organizational preference, existing infrastructure, cloud vendor). The issue produced no actionable recommendation because it specified breadth (5+ strategies, 10+ dimensions) without specifying depth constraints or selection criteria.

**Finding PM-001-it1:** No selection criteria or decision framework defined — research produces comprehensive coverage but no recommendation.

**Failure Scenario 2: The Capability Audit Invalidated Everything**

The capability audit revealed that Claude Code requires interactive mode for `jerry session start` due to TTY attachment. All strategies that use Docker containers, GitHub Actions runners, or serverless functions are non-viable because they cannot provide a persistent TTY-attached Claude Code session. The research issue was predicated on an unvalidated assumption. The issue was closed as "infeasible" after 3 weeks of work.

**Finding PM-002-it1:** No explicit validation of headless Claude Code operation before full research commitment.

**Failure Scenario 3: Security Blocked All Cloud Strategies**

The security review (in the acceptance criteria) revealed that GitHub Actions strategies require exposing the Anthropic API key in GitHub Secrets, and that GitHub Actions runners are a known target for secret exfiltration attacks. The serverless strategy had similar issues with API key lifecycle management. Only the self-hosted Kubernetes strategy passed the security bar, but it was deemed "too operationally complex for a small team." The research produced a viable strategy (K8s) that was not adoptable. The project stalled.

**Finding PM-003-it1:** No feasibility filter on strategies relative to the team's operational capacity — K8s may be technically correct but organizationally infeasible.

**Failure Scenario 4: Concurrent Instance Research Discovered Fundamental Jerry Architecture Gap**

The researcher discovered that concurrent Claude Code instances writing to the same Jerry worktracker creates git conflicts on worktracker files. The worktracker data model (markdown files in a git repository) doesn't support concurrent writes. Resolving this requires either a new Jerry feature (concurrent-safe worktracker) or a per-instance project model that creates N isolated worktrackers with no aggregate view. The research issue was blocked pending Jerry architectural changes, because the issue required "full Jerry session integration" but Jerry's architecture was incompatible with concurrent automated instances.

**Finding PM-004-it1:** Research may surface Jerry architectural limitations that block all viable strategies — no mechanism to escalate this as a blocking dependency to Jerry framework changes.

**Failure Scenario 5: OSS Release Happened Before Research Completed**

The research was estimated at 2-3 weeks. OSS release happened after 1.5 weeks. External contributors started opening PRs. The research was incomplete — only 2 of 5 strategies had been evaluated. The PR review queue grew while the automation research was still in progress. The "Why now" urgency was real, but the issue provided no timeline or milestone structure to ensure research completed before the release.

**Finding PM-005-it1:** No timeline or milestone structure in the issue — research completion date unanchored relative to OSS release.

### Pre-Mortem Findings

| ID | Description | Severity | Failure Mode |
|----|-------------|---------|-------------|
| PM-001-it1 | No selection criteria or decision framework — research produces "it depends" | Major | Research doesn't converge to recommendation |
| PM-002-it1 | Headless Claude Code operation unvalidated — research may be invalidated by capability gap | Critical | Prerequisite assumption fails post-commitment |
| PM-003-it1 | No operational feasibility filter — technically correct strategies may be organizationally infeasible | Major | Viable strategy not adoptable |
| PM-004-it1 | Jerry worktracker concurrency gap — concurrent instances may require Jerry framework changes | Critical | Blocking architectural dependency discovered mid-research |
| PM-005-it1 | No timeline or milestone structure relative to OSS release | Major | Research not complete when automation is needed |

---

## S-012: FMEA

*Finding Prefix: FM-NNN-it1 | Strategy: Component-level failure mode analysis | Required C3+*

### FMEA Component Decomposition

**Components analyzed:** Issue structure → Research scope → Jerry integration requirements → Security requirements → Acceptance criteria → Approach workflow

**RPN = Severity (1-10) × Occurrence (1-10) × Detectability (1-10)**

| ID | Component | Failure Mode | Effect | S | O | D | RPN | Finding |
|----|-----------|-------------|--------|---|---|---|-----|---------|
| FM-001-it1 | Capability audit (Approach Step 1) | Not treated as blocking gate | All subsequent research wasted if headless execution not viable | 9 | 7 | 6 | 378 | Critical |
| FM-002-it1 | Strategy 3 (SDK) | SDK not publicly available or documented | Strategy 3 cannot be evaluated; required strategy set fails | 8 | 6 | 5 | 240 | Major |
| FM-003-it1 | C1-C4 capability labeling | Collision with Jerry criticality levels | Implementer confusion, mis-assignment of criticality to capabilities | 6 | 8 | 7 | 336 | Major |
| FM-004-it1 | Worktracker concurrency | Concurrent writes create git conflicts | Research blocked or requires Jerry architectural change | 9 | 6 | 4 | 216 | Critical |
| FM-005-it1 | Security dimension | External contributor threat model omitted | Post-OSS security vulnerability in deployed automation | 10 | 5 | 6 | 300 | Critical |
| FM-006-it1 | Research scope (50+ evaluation cells) | Scope not managed | Research fails to converge; no recommendation delivered | 8 | 7 | 5 | 280 | Major |
| FM-007-it1 | Acceptance criterion 3 | Jerry integration "specific implementation detail" is vague | Implementer underspecifies Jerry integration; AC3 passed with insufficient depth | 6 | 7 | 6 | 252 | Major |
| FM-008-it1 | H-13 for research output | No quality gate on research deliverable | Research output may be substandard without adversarial review requirement | 7 | 6 | 7 | 294 | Major |
| FM-009-it1 | Approach Step 7 (PR submission) | No target directory specified | Research artifacts placed inconsistently | 4 | 7 | 8 | 224 | Minor |
| FM-010-it1 | P-003 compliance in strategies | Orchestration strategies not checked for recursive agent spawning | Evaluated strategies may include P-003-violating architectures | 8 | 5 | 6 | 240 | Major |

### High-RPN Findings Summary

| ID | RPN | Severity Classification |
|----|-----|----------------------|
| FM-001-it1 | 378 | Critical |
| FM-003-it1 | 336 | Major |
| FM-005-it1 | 300 | Critical |
| FM-008-it1 | 294 | Major |
| FM-006-it1 | 280 | Major |
| FM-010-it1 | 240 | Major |
| FM-002-it1 | 240 | Major |
| FM-004-it1 | 216 | Critical |

---

## S-011: Chain-of-Verification

*Finding Prefix: CV-NNN-it1 | Strategy: Factual claim verification | Required C3+*

### Verification Chain Protocol

**Verifying factual and technical claims in the deliverable:**

**Claim 1:** "Claude Code can already: Read and understand PR diffs, Make code changes based on feedback, Run tests and verify its work, Work within Jerry's guardrail framework"

**Verification:** These capabilities are stated as current facts in the "Why this matters" section. However:
- "Read and understand PR diffs" — **Verifiable.** Claude Code is designed to work with code and files; reading diffs is within scope.
- "Make code changes based on feedback" — **Verifiable** in interactive mode. Unverified for headless/non-interactive invocation.
- "Run tests and verify its work" — **Verifiable** in interactive mode. Not verified in containerized/runner environments where test dependencies may not be present.
- "Work within Jerry's guardrail framework" — **Partially verifiable.** Works in interactive sessions. Unverified for automated/unattended sessions.

**Finding CV-001-it1:** Capabilities presented as current facts are verified only for interactive mode — the non-interactive mode, which is the primary requirement, is unverified.

**Claim 2:** "Lambda 15min execution limit" referenced in Strategy 4 key questions

**Verification:** AWS Lambda has a maximum execution timeout of 15 minutes (900 seconds) as of current documentation. This is accurate. However, Google Cloud Functions has a 60-minute maximum for gen2, and Cloudflare Workers have a different model (CPU time, not wall time). The parenthetical "(Lambda 15min, etc.)" undersells the variability and the fact that gen2 Cloud Functions significantly extend viability.

**Finding CV-002-it1:** Lambda timeout cited accurately but with incomplete comparison — the "etc." obscures material differences between serverless platforms that affect strategy viability.

**Claim 3:** "you can have multiple people skiing different lines simultaneously" (mountain metaphor)

**Verification:** N/A — metaphorical claim, not factual.

**Claim 4:** "MUST support at minimum 5 concurrent instances" (C3 constraint)

**Verification:** This is a stated requirement, not a factual claim. However, it lacks derivation — why 5? Is this based on observed PR volume, anticipated OSS PR rate, or an arbitrary round number? The absence of justification makes this hard to evaluate — a strategy that supports exactly 5 concurrent instances technically passes but may be insufficient.

**Finding CV-003-it1:** "At minimum 5 concurrent instances" requirement lacks derivation — arbitrary threshold creates verification ambiguity.

**Claim 5:** "kubebuilder, operator-sdk" mentioned in Strategy 5

**Verification:** Both are real Kubernetes operator development frameworks. kubebuilder is CNCF-supported; operator-sdk is Red Hat's implementation. Both are currently maintained and appropriate for Kubernetes operator development. This claim is accurate.

**Claim 6:** "circuit breaker on feedback rounds — suggest max 10 rounds"

**Verification:** No external justification for "10 rounds" — this appears arbitrary. For context, GitHub's own review tools don't have explicit round limits. The number is not derived from any stated analysis.

**Finding CV-004-it1:** "Max 10 rounds" circuit breaker value is arbitrary — no derivation or justification provided.

**Claim 7:** Research approach implies Context7 should be used for SDK documentation

**Verification:** The Approach step 2 says "Use Context7 for any SDK/framework documentation." However, Context7 is a Jerry MCP tool. If this research issue is executed in an automated context (which is ironically what it's researching), the Context7 tool may or may not be available. This is an incidental self-referential gap but worth noting.

**Finding CV-005-it1 (Minor):** Approach Step 2 references Jerry-specific tool (Context7) without confirming Context7 availability in the research execution context.

### Chain-of-Verification Findings

| ID | Description | Severity | Claim Verified? |
|----|-------------|---------|----------------|
| CV-001-it1 | Claude Code capabilities claimed for interactive mode presented as universally true — headless mode unverified | Critical | Partially |
| CV-002-it1 | Lambda timeout accurate but serverless platform comparison incomplete (gen2 Cloud Functions, Workers differ) | Minor | Partially |
| CV-003-it1 | "5 concurrent instances" minimum lacks derivation — arbitrary threshold | Minor | Unverifiable |
| CV-004-it1 | "Max 10 rounds" circuit breaker value arbitrary — no justification | Minor | Unverifiable |
| CV-005-it1 | Context7 tool reference in Approach assumes tool availability in research context | Minor | Unverified |

---

## S-001: Red Team Analysis

*Finding Prefix: RT-NNN-it1 | Strategy: Adversarial threat emulation | Required C4, H-16 satisfied*

### Threat Actor Profile

**Goal:** Ensure this issue, when executed, produces research that enables Claude Code automation deployment without adequate security controls, governance compliance, or Jerry framework integrity — either through omission, underspecification, or scope ambiguity.

**Capability:** Full knowledge of the deliverable, Jerry framework architecture, GitHub API model, and Claude Code behavior. Insider knowledge of the team's OSS release timeline and resource constraints.

**Motivation:** Reduce scope of required research, skip uncomfortable security analysis, deploy automation quickly at the expense of rigor, or use the issue's ambiguities to rationalize inadequate research depth.

### Attack Vector Enumeration

**Vector 1: Exploit the "Research Only" Scope Boundary**

The issue explicitly excludes "Implementation of any strategy." An implementer who interprets "research" narrowly could write entirely speculative strategy analyses without actually testing any capability. The issue does not mandate PoC validation, API exploration, or hands-on testing. A threat actor (or a deadline-pressured implementer) could produce a research deliverable that is 100% speculative, cite the "research only" scope exclusion to avoid pushback, and pass acceptance criteria through superficially detailed architectural narratives that have never been validated. The acceptance criteria do not require any empirical evidence — only documentation.

**Finding RT-001-it1 (Major):** "Research only" scope with no empirical validation requirement enables entirely speculative research to pass acceptance criteria.

**Vector 2: Exploit Strategy 3 Ambiguity to Reduce Required Research**

Strategy 3 ("Claude Code SDK / Claude Agent SDK") acknowledges uncertain SDK state. The threat actor notes: if the implementer discovers early that the Claude Code SDK is not publicly documented, they can declare Strategy 3 unresearchable and reduce the required strategy set from 5 to 4. But the issue says "at minimum 5 strategies" without specifying that Strategy 3 must be resolvable. A motivated implementer could research 4 strategies thoroughly and include a thin Strategy 3 entry that says "SDK not publicly available, cannot research" — technically passing the 5-strategy count while materially reducing research scope.

**Finding RT-002-it1 (Minor):** Strategy 3 ambiguity enables count-compliance with minimal research depth.

**Vector 3: Exploit the Security Dimension's Omission of External Threat Actors**

The security dimension in the strategy matrix specifies: "API key management, secret handling, repository permissions, least-privilege analysis." None of these explicitly require analysis of external contributor threat vectors. Post-OSS, an external contributor submitting a PR with adversarially crafted content could manipulate the Claude Code automated response system. An implementer following the security dimension literally could produce a thorough internal security analysis while completely ignoring the external threat surface — and pass acceptance criterion 5 ("Security considerations are documented for each strategy, including: API key management, repository permission model, secret injection, and least-privilege analysis").

**Finding RT-003-it1 (Critical):** Security acceptance criterion does not require external/adversarial threat model — an internal-only security analysis passes while leaving a critical post-OSS attack surface unaddressed.

**Vector 4: Exploit Quality Gate Absence for Research Output**

The issue does not specify a quality gate (S-014 score threshold) for the research deliverable. An implementer producing shallow, hastily written strategy evaluations could submit the PR without any adversarial review of the research itself. The acceptance criteria are functional checklists, not quality gate thresholds. There is no mechanism to require the research output to meet H-13 standards before the issue is closed.

**Finding RT-004-it1 (Major):** No quality gate on research output — the research deliverable can be accepted without adversarial review or S-014 scoring.

**Vector 5: Exploit Timeline Absence to Defer Indefinitely**

The issue has no timeline, milestone structure, or deadline relative to OSS release. A threat actor could use this to justify indefinitely deferring the research ("we're still evaluating Strategy 4") while the OSS release proceeds without the automation infrastructure being understood. By the time research completes, the external PR volume may have exceeded the team's capacity to maintain quality without automation — the damage the issue was designed to prevent.

**Finding RT-005-it1 (Major):** No timeline structure — research can be deferred indefinitely relative to OSS release trigger.

### Red Team Findings

| ID | Description | Severity | Attack Vector |
|----|-------------|---------|--------------|
| RT-001-it1 | "Research only" scope with no empirical validation requirement enables speculative research to pass AC | Major | Research scope exploitation |
| RT-002-it1 | Strategy 3 ambiguity enables count-compliance with insufficient depth | Minor | SDK ambiguity exploitation |
| RT-003-it1 | Security AC does not require external/adversarial threat model from OSS contributors | Critical | Security scope exploitation |
| RT-004-it1 | No quality gate on research output — accepted without adversarial review | Major | Quality gate absence |
| RT-005-it1 | No timeline relative to OSS release — research can be deferred indefinitely | Major | Timeline absence exploitation |

---

## S-014: LLM-as-Judge Scoring

*Finding Prefix: LJ-NNN-it1 | Strategy: Weighted composite quality scoring | Required C2+*

### Leniency Bias Counteraction Active

**This is a first iteration — scored against absolute C4 standard, not "good for a first draft."**

### Step 2: Independent Dimension Scoring

---

#### Dimension 1: Completeness (Weight: 0.20)

**Rubric:** Does the deliverable contain all required sections, address all stated requirements, and leave no significant gaps?

**Evidence for scoring:**

Strong elements:
- Vision, motivation, core capabilities, strategy requirements, strategy set, Jerry integration, exclusions, AC, approach, rationale — all present
- Navigation table compliant
- 5 strategies defined with key questions
- 6 Jerry integration requirements with specific descriptions
- 8 acceptance criteria structured as checkboxes
- Explicit exclusions section

Gaps:
- Worktree isolation not mentioned (SM-001-it1) — critical for concurrent instances, it's an entire architectural constraint on all strategies
- JERRY_PROJECT assignment models not specified (SM-004-it1) — "the strategy must define how projects are assigned" without providing the candidate models to evaluate
- No quality gate specification for research output (CC-003-it1, RT-004-it1)
- P-003 compliance not required of evaluated strategies (CC-002-it1) — a strategy evaluator could recommend an instance-spawning architecture that violates Jerry's constitution
- No "infeasibility" outcome path (IN-005-it1)
- Research output target directory not specified (DA-005-it1)
- Timeline/milestone structure absent (PM-005-it1)

**Scoring:** The completeness is substantial but has 7 verifiable gaps, including 2 that are Critical (worktree isolation, P-003 compliance for strategies). The issue covers its core scope well but misses architectural constraints that are fundamental to Jerry's operation.

**Score: 0.72**

**Leniency check:** This is not lenient — the gaps are verifiable absences in the specification text, not interpretive judgments.

---

#### Dimension 2: Internal Consistency (Weight: 0.20)

**Rubric:** Are all claims, requirements, and sections mutually consistent? Are there contradictions or tensions that would confuse an implementer?

**Evidence for scoring:**

Consistent elements:
- Scope boundaries (exclusions) are consistently referenced
- Core capabilities reference the constraint model consistently
- Jerry integration requirements are consistent with the stated vision

Inconsistencies:
- **Critical:** C1-C4 capability labels collide directly with C1-C4 Jerry criticality labels (SR-001-it1). An implementer reading "this is a C3 requirement" will be confused about whether "C3" means the core capability or the criticality level.
- **Major:** "Research only" scope conflicts with the required "how it works" specificity demanded by the acceptance criteria (DA-001-it1). The issue cannot require architectural-level detail (which requires implementation/PoC knowledge) while also excluding implementation.
- **Minor:** "Circuit breaker — suggest max 10 rounds" uses SUGGEST language inside a MUST constraint (SM-005-it1)
- **Minor:** Strategy 3 conflates two different SDKs (SR-002-it1)

The C1-C4 collision is severe because it affects every occurrence of the core capabilities section — 4 headings and numerous references. This is not a minor terminology choice; it creates genuine ambiguity in a framework where C1-C4 is a fundamental vocabulary term.

**Score: 0.71**

**Leniency check:** The C1-C4 collision alone would reduce this dimension. The research/specificity tension adds a second major inconsistency. Score 0.71 reflects two major inconsistencies.

---

#### Dimension 3: Methodological Rigor (Weight: 0.20)

**Rubric:** Does the deliverable follow a sound, well-structured methodology? Are procedures systematic and defensible?

**Evidence for scoring:**

Strong elements:
- Structured capability definitions (C1-C4) with explicit constraints
- Strategy evaluation matrix with 10 consistent dimensions
- Jerry integration requirements as a parallel evaluation framework
- 7-step research Approach
- Key questions per strategy

Weaknesses:
- Strategy evaluation matrix has no weighting or tiering — all 10 dimensions appear equally important (SM-002-it1). A methodologically rigorous evaluation framework would distinguish between disqualifying criteria (security, Jerry integration) and trade-off criteria (cost, latency).
- Capability audit framed as Step 1 of research, not as a prerequisite gate (IN-001-it1, FM-001-it1, PM-002-it1). Rigorous methodology requires go/no-go gates before full research commitment.
- No decision framework for recommendation selection (PM-001-it1) — how does the researcher choose between strategies? The issue is silent on selection criteria.
- Strategy 3 is in the required set despite having an uncertain research premise (SDK availability) — a rigorous methodology would condition Strategy 3 on SDK availability verification
- 50+ evaluation cells with no scope management mechanism (DA-002-it1)

**Score: 0.68**

**Leniency check:** The absence of a go/no-go gate for the capability audit and the absence of a decision framework for strategy selection are fundamental methodological gaps, not editorial choices. Score 0.68 is not lenient.

---

#### Dimension 4: Evidence Quality (Weight: 0.15)

**Rubric:** Are claims supported by evidence? Are references authoritative? Are quantitative data used where available?

**Evidence for scoring:**

Strong elements:
- Strategy-specific key questions show domain knowledge
- Approach references Context7 and WebSearch for external validation
- Acceptance criterion 8 explicitly requires distinguishing verified vs. assumed capabilities

Weaknesses:
- "5 concurrent instances minimum" is arbitrary — no derivation (CV-003-it1)
- "Max 10 rounds" circuit breaker is arbitrary — no derivation (CV-004-it1)
- Lambda timeout cited (accurate) but platform comparison incomplete (CV-002-it1)
- No quantitative anchoring for success (what latency is "good enough"? what cost is "acceptable"?)
- Urgency argument ("Why now") cites OSS release without projected PR volume data (DA-004-it1)
- Core capabilities presented as verified for all execution modes, but verified only for interactive mode (CV-001-it1)

**Score: 0.70**

**Leniency check:** Multiple "numbers from nowhere" (5 instances, 10 rounds), the interactive-only capability claim, and the missing success metrics are verifiable evidence gaps. Score reflects this.

---

#### Dimension 5: Actionability (Weight: 0.15)

**Rubric:** Does the deliverable provide clear, specific direction that an implementer can follow without ambiguity?

**Evidence for scoring:**

Strong elements:
- Key questions per strategy are specific and actionable
- 7-step research Approach is ordered and concrete
- Acceptance criteria are structured as verifiable checkboxes
- Explicit exclusions reduce scope ambiguity

Weaknesses:
- Research output target directory not specified (DA-005-it1) — where do artifacts go?
- No timeline or milestone structure (PM-005-it1) — when is research expected to complete?
- No research priority ordering among strategies — in parallel or sequential?
- No scope management for 50+ evaluation cells (DA-002-it1) — how deep is "deep enough"?
- No infeasibility decision path (IN-005-it1) — what does the researcher do if all strategies fail?
- "Specific implementation detail" in AC#3 for Jerry integration is undefined — what level of detail passes?

**Score: 0.74**

**Leniency check:** Multiple missing operational details that an implementer would need to start work without confusion. Score 0.74 is appropriate given the strong key questions partially compensating.

---

#### Dimension 6: Traceability (Weight: 0.10)

**Rubric:** Can requirements be traced to their rationale? Are decisions documented and cross-referenced?

**Evidence for scoring:**

Strong elements:
- "Why now" section provides rationale for the issue
- Each core capability has explicit constraints
- "What this does NOT include" section provides rationale for exclusions
- "Why this matters" provides the business context

Weaknesses:
- The 5-strategy minimum ("at minimum the following 5 strategies") has no traceability — why these 5? Why not 3 or 7?
- The 10-dimension evaluation matrix has no traceability — why these 10 dimensions?
- Jerry integration requirements are stated but not traced to Jerry constitutional requirements (which HARD rules mandate each requirement?)
- The "oss-prep" label is mentioned but the connection to OSS preparation is not traced in the body

**Score: 0.80**

**Leniency check:** The traceability gaps are real but the issue does have rationale sections. The 5-strategy and 10-dimension gaps are notable. Score 0.80 is not lenient — strong traceability elements partially compensate.

---

### Step 3: Weighted Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|---------|
| Completeness | 0.20 | 0.72 | 0.144 |
| Internal Consistency | 0.20 | 0.71 | 0.142 |
| Methodological Rigor | 0.20 | 0.68 | 0.136 |
| Evidence Quality | 0.15 | 0.70 | 0.105 |
| Actionability | 0.15 | 0.74 | 0.111 |
| Traceability | 0.10 | 0.80 | 0.080 |
| **Composite** | **1.00** | | **0.718** |

**Mathematical verification:**
0.72 × 0.20 = 0.1440
0.71 × 0.20 = 0.1420
0.68 × 0.20 = 0.1360
0.70 × 0.15 = 0.1050
0.74 × 0.15 = 0.1110
0.80 × 0.10 = 0.0800
Sum = 0.1440 + 0.1420 + 0.1360 + 0.1050 + 0.1110 + 0.0800 = **0.718**

### Step 4: Verdict

**Composite: 0.72**
**C4 Threshold: 0.95**
**Gap: -0.23**

**Verdict: REJECTED**

Operational band: **REJECTED** (< 0.85 — significant rework required)

**Special condition check:**
- Dimension scores <= 0.50: None
- But all three major dimensions (Completeness, Internal Consistency, Methodological Rigor) score between 0.68-0.72, well below C4 requirements
- Multiple Critical findings from S-007 (CC-002-it1), S-013 (IN-001-it1, IN-002-it1, IN-004-it1), S-001 (RT-003-it1), S-014 (implicit in scoring)

### Step 6: Leniency Bias Self-Check

- [x] Each dimension scored independently — no cross-influence detected
- [x] Evidence documented for each score — specific gaps cited with finding IDs
- [x] Uncertain scores resolved downward — when uncertain between 0.70 and 0.74, chose 0.70
- [x] First-draft calibration noted: 0.72 is within typical first-draft range (0.65-0.80) — this is accurate
- [x] No dimension scored >= 0.95 — no exceptional score justification required
- [x] No dimension scored > 0.90 — only Traceability at 0.80
- [x] Lowest dimensions verified: Methodological Rigor (0.68), Internal Consistency (0.71), Evidence Quality (0.70) — all justified with specific evidence
- [x] Weighted composite verified: 0.718 ✓
- [x] Verdict matches score range: 0.718 falls in REJECTED band (< 0.85) ✓
- [x] Improvement recommendations are specific and actionable — see below

### LJ Findings Table

| ID | Finding | Severity | Evidence |
|----|---------|----------|---------|
| LJ-001-it1 | Completeness: 0.72/1.00 | Major | 7 verifiable gaps including worktree isolation, P-003 compliance requirement, quality gate for output |
| LJ-002-it1 | Internal Consistency: 0.71/1.00 | Major | C1-C4 capability/criticality collision; research-depth/scope-exclusion tension |
| LJ-003-it1 | Methodological Rigor: 0.68/1.00 | Major | No capability audit gate; no decision framework; no scope management; SDK conditionality missing |
| LJ-004-it1 | Evidence Quality: 0.70/1.00 | Major | Arbitrary thresholds (5 instances, 10 rounds); capabilities claimed for all modes but verified for interactive only |
| LJ-005-it1 | Actionability: 0.74/1.00 | Major | Missing target directory, timeline, research depth definition, infeasibility path |
| LJ-006-it1 | Traceability: 0.80/1.00 | Minor | Strategy selection rationale absent; dimension matrix rationale absent |

---

## Tournament Verdict

### Findings Consolidation

**Critical Findings (cross-strategy):**

| Finding | Strategy | Issue |
|---------|---------|-------|
| SM-001-it1 | S-003 | Worktree isolation requirement missing |
| CC-002-it1 | S-007 | P-003 compliance not required of evaluated strategies |
| CC-003-it1 | S-007 | Quality gate for research output not specified |
| CC-004-it1 | S-007 | Human escalation path unspecified for automated instances |
| IN-001-it1 | S-013 | Capability audit not a go/no-go gate (headless execution unvalidated) |
| IN-002-it1 | S-013 | Quality enforcement escalation assumes human presence |
| IN-004-it1 | S-013 | OSS external contributor threat model absent |
| FM-001-it1 | S-012 | Capability audit not a blocking gate (RPN 378) |
| FM-005-it1 | S-012 | External contributor security threat model absent (RPN 300) |
| FM-004-it1 | S-012 | Worktracker concurrency gap may require Jerry architecture change (RPN 216) |
| DA-002-it1 | S-002 | 50+ evaluation cells without scope management |
| PM-002-it1 | S-004 | Headless Claude Code operation unvalidated |
| PM-004-it1 | S-004 | Jerry worktracker concurrency may require Jerry framework changes |
| CV-001-it1 | S-011 | Claude Code capabilities claimed for all modes, verified for interactive only |
| RT-003-it1 | S-001 | Security AC omits external contributor adversarial threat model |

**Major Findings (cross-strategy):**

SM-002-it1, SM-003-it1, SM-004-it1, SR-001-it1, SR-002-it1, CC-001-it1, IN-003-it1, IN-005-it1, FM-002-it1, FM-003-it1, FM-006-it1, FM-007-it1, FM-008-it1, FM-010-it1, DA-001-it1, DA-003-it1, DA-004-it1, DA-005-it1, PM-001-it1, PM-003-it1, PM-005-it1, RT-001-it1, RT-004-it1, RT-005-it1, LJ-001-it1 through LJ-005-it1

**Total:** 15 Critical findings, 25 Major findings, 7 Minor findings

### Final Verdict

| Metric | Value |
|--------|-------|
| Weighted Composite Score | 0.72 |
| C4 Threshold | 0.95 |
| Gap to Threshold | -0.23 |
| **Verdict** | **REJECTED** |
| **Band** | REJECTED (significant rework required) |
| Critical Findings | 15 |
| Major Findings | 25 |
| Minor Findings | 7 |

**The deliverable scores 0.72 against a C4 threshold of 0.95. Gap of 0.23 requires significant rework. This is expected for a first-iteration baseline of a complex technical specification.**

---

## Revision Recommendations

*Ordered by weighted impact on composite score. Format: R-NNN-it1*

### Priority 1: Methodological Rigor (0.68 → target 0.90+)

**R-001-it1: Add Capability Audit as Phase 0 Gate**

Add an explicit Phase 0 to the Approach section before any strategy research begins:

> **Phase 0 (Prerequisite Gate): Claude Code Headless Capability Verification**
> Before any strategy research begins, the implementer MUST verify that Claude Code can operate in non-interactive/headless mode sufficient for automated dispatch. Specifically:
> - Can `jerry session start` be executed without TTY attachment?
> - Can Claude Code be invoked via CLI with all required flags in a GitHub Actions runner, Docker container, and Lambda function?
> - Does `JERRY_PROJECT` work as an environment variable in non-interactive sessions?
>
> **Gate decision:** If headless operation is not viable, halt and report to the issue author before proceeding. Do NOT continue to strategy research if the foundational capability is unconfirmed.

**Impact:** Addresses IN-001-it1, PM-002-it1, FM-001-it1, CV-001-it1. Estimated Methodological Rigor impact: +0.08.

---

**R-002-it1: Add Dimension Tiering to Strategy Evaluation Matrix**

Replace the flat 10-dimension evaluation matrix with a tiered framework:

> | Tier | Dimensions | Evaluation Mode |
> |------|-----------|----------------|
> | **Tier 1: Must Pass** | Jerry integration, Security, Reliability | Binary pass/fail — strategies failing any Tier 1 dimension are disqualified |
> | **Tier 2: Trade-off** | Architecture, Deployment model, Scalability | Comparative — scored and ranked relative to other strategies |
> | **Tier 3: Inform** | Cost, Complexity, Latency, Limitations | Informational — documented but not decision-determining |

**Impact:** Addresses SM-002-it1, PM-001-it1, FM-006-it1. Estimated Methodological Rigor impact: +0.06.

---

**R-003-it1: Add Decision Framework for Recommendation**

Add a "Recommendation selection criteria" subsection to the Strategy requirements section:

> **Selection criteria:** A strategy is RECOMMENDED if it: (a) passes all Tier 1 dimensions, (b) scores highest in the Tier 2 comparison, AND (c) is operationally feasible for a team of [1-3 engineers, no dedicated DevOps]. If multiple strategies pass Tier 1, the recommendation should include a primary recommendation and a secondary recommendation for teams with different infrastructure preferences (e.g., cloud-native vs. self-hosted).

**Impact:** Addresses PM-001-it1, FM-006-it1. Estimated Methodological Rigor impact: +0.04.

---

### Priority 2: Internal Consistency (0.71 → target 0.90+)

**R-004-it1: Rename Core Capabilities to Avoid C1-C4 Collision**

Replace the C1-C4 capability labels with CAP-1, CAP-2, CAP-3, CAP-4 (or PR-Listening, Issue-Dispatch, Multi-Instance, Feedback-Loop) to eliminate collision with Jerry's C1-C4 criticality vocabulary. Update all 4 headings and all references throughout the issue body.

**Impact:** Addresses SR-001-it1, FM-003-it1. Estimated Internal Consistency impact: +0.10.

---

**R-005-it1: Resolve Research-Depth / Scope Boundary Tension**

Add a "Research depth definition" paragraph to the Approach section:

> **Research depth:** For this issue, "research" means: documentary analysis, API/SDK documentation review, community report review, and targeted capability testing using free-tier or trial-tier infrastructure. Implementation of production-quality code is excluded. However, executing a minimal proof-of-concept (e.g., a single GitHub Actions workflow that invokes `claude --version` in a runner) to validate capability claims is WITHIN scope and REQUIRED where claims cannot be validated documentarily.

**Impact:** Addresses DA-001-it1. Estimated Internal Consistency impact: +0.05.

---

**R-006-it1: Resolve Strategy 3 SDK Ambiguity**

Replace the current Strategy 3 title and framing with:

> **Strategy 3: Claude Code SDK / Claude Agent SDK Custom Orchestrator**
> **SDK Availability Prerequisite:** Before researching this strategy, the implementer must verify: (1) Is a public Claude Code SDK or Claude Agent SDK available? (2) Is it documented? (3) Can it manage multiple concurrent sessions?
> **If SDK is not available:** Research Strategy 3 as a "future strategy" — document what the SDK would need to provide to enable this architecture, and estimate when this strategy becomes viable based on Anthropic's public roadmap.

**Impact:** Addresses SR-002-it1, DA-003-it1, FM-002-it1. Estimated Internal Consistency impact: +0.04.

---

### Priority 3: Completeness (0.72 → target 0.90+)

**R-007-it1: Add Worktree Isolation to Jerry Integration Requirements**

Add a new row to the Jerry integration requirements table:

> | **Worktree isolation** | Each automated instance MUST operate in an isolated git worktree per Jerry's worktree convention (`git worktree add ~/workspace/github/{repo}-wt/{branch-name}`). The strategy MUST define: how worktrees are created at dispatch time, how they are named (suggest: `{repo}-wt/auto-{pr-number}` or `{repo}-wt/auto-{issue-number}`), and how they are cleaned up on instance completion or failure. Strategies that cannot provide worktree isolation must document this as a known limitation. |

**Impact:** Addresses SM-001-it1. Estimated Completeness impact: +0.06.

---

**R-008-it1: Add P-003 Compliance Requirement to Multi-Instance Strategy Evaluation**

Add to the C3 Multi-Instance Orchestration capability constraints:

> - MUST NOT spawn Claude Code instances that themselves spawn additional Claude Code instances (P-003 violation — max 1 level of agent recursion). Each evaluated strategy MUST document its instance spawning model and confirm that automated instances are terminal workers, not orchestrators.

Add to Strategy requirements dimension table row for Architecture:

> **Architecture** also evaluates: Does the proposed architecture respect P-003 (no recursive agent spawning)? Strategies that propose orchestrator-spawning-orchestrator topologies are disqualified.

**Impact:** Addresses CC-002-it1, FM-010-it1. Estimated Completeness impact: +0.04.

---

**R-009-it1: Add Quality Gate Requirement for Research Output**

Add to the Acceptance Criteria:

> - [ ] The research output (comparison matrix and recommendations document) has been reviewed using at minimum S-010 (Self-Refine) and S-014 (LLM-as-Judge) before PR submission. The S-014 score MUST be documented in the PR description. Target: >= 0.85 for a research deliverable (C3 quality threshold).

**Impact:** Addresses CC-003-it1, RT-004-it1, FM-008-it1. Estimated Completeness impact: +0.03.

---

**R-010-it1: Add External Contributor Threat Model to Security Requirements**

Add to Strategy requirements table for Security dimension:

> **Security** evaluation MUST include: adversarial input handling from untrusted external contributors. For post-OSS scenarios, GitHub comments from external contributors are untrusted input. Each strategy must address: prompt injection risk (can a comment manipulate Claude Code into executing unintended commands?), repository permission escalation risk (can automated changes exceed the permissions of the triggering event?), and secret exfiltration risk (can an attacker extract API keys or tokens via crafted PR content?).

**Impact:** Addresses IN-004-it1, RT-003-it1, FM-005-it1. Estimated Completeness impact: +0.04.

---

### Priority 4: Evidence Quality and Actionability (0.70/0.74 → target 0.88+)

**R-011-it1: Add JERRY_PROJECT Assignment Models for Research Evaluation**

Add to the Jerry integration requirements table for JERRY_PROJECT:

> **JERRY_PROJECT assignment models:** Research MUST evaluate these three models: (1) **Per-repo model** — all automated instances for a repository share one JERRY_PROJECT; (2) **Per-instance model** — each automated instance creates and uses a transient JERRY_PROJECT for its work duration; (3) **Per-work-item model** — each PR or issue gets a dedicated JERRY_PROJECT, enabling PR-scoped artifact isolation and audit trail. For each model, document: worktracker isolation characteristics, aggregate visibility across instances, artifact naming conventions, and cleanup procedure.

**Impact:** Addresses SM-004-it1. Estimated Evidence Quality impact: +0.05.

---

**R-012-it1: Add Human Escalation Path for Automated Instances**

Add to Jerry integration requirements:

> | **Headless escalation** | Jerry quality enforcement includes human escalation triggers (AE-006 graduated escalation, H-19 governance escalation). Automated instances cannot escalate to a human interactively. Each strategy MUST define: how AE-006 CRITICAL/EMERGENCY conditions are handled when no human is available (e.g., instance self-terminates, posts GitHub comment requesting human review, writes to worktracker and pauses). The fallback behavior MUST be documented and must not silently continue with degraded quality. |

**Impact:** Addresses CC-004-it1, IN-002-it1. Estimated Actionability impact: +0.05.

---

**R-013-it1: Add Research Artifacts Target Directory and Timeline**

Add to the Approach section:

> **Research artifacts location:** All research artifacts MUST be persisted to `work/research/pr-automation/` within the Jerry project. Strategy evaluation documents go to `work/research/pr-automation/strategies/`. The comparison matrix goes to `work/research/pr-automation/comparison-matrix.md`. Recommendations go to `work/research/pr-automation/recommendations.md`.
>
> **Research timeline:** Phase 0 (capability audit) MUST complete within the first 3 days. Phase 1 (strategy research) target: 2-3 weeks. PR submission target: before OSS release. If Phase 0 reveals a blocking issue, report within 3 days and do not proceed with Phase 1 without author acknowledgment.

**Impact:** Addresses DA-005-it1, PM-005-it1, SR-003-it1. Estimated Actionability impact: +0.06.

---

**R-014-it1: Derive and Justify Quantitative Thresholds**

Replace arbitrary thresholds with derived values:

> **Concurrent instances minimum:** The issue currently specifies "at minimum 5 concurrent instances" without derivation. Replace with: "at minimum N concurrent instances where N = [anticipated PR volume at OSS launch estimated by author]. If unknown, default to 5 as an initial planning figure, with research explicitly noting this as a placeholder requiring calibration."
>
> **Feedback loop circuit breaker:** Replace "suggest max 10 rounds" with "MUST NOT exceed 10 feedback rounds per comment thread (rationale: beyond 10 rounds, human escalation is more appropriate than continued automated iteration; this value should be validated during PoC testing and adjusted based on observed convergence rates)."

**Impact:** Addresses CV-003-it1, CV-004-it1, SM-005-it1. Estimated Evidence Quality impact: +0.04.

---

**R-015-it1: Add Infeasibility Outcome Path**

Add to the Approach section:

> **Infeasibility outcome:** If Phase 0 reveals that Claude Code cannot operate headlessly in any evaluated environment, or if the full strategy evaluation concludes that no strategy achieves passing Tier 1 criteria without modifications to Claude Code itself, the research deliverable MUST: (1) document the specific blocking limitations, (2) identify what Claude Code changes would be required to unblock, (3) estimate a realistic timeline for when those changes might be available based on Anthropic's public communications, and (4) recommend the strategy most likely to become viable once those changes arrive. An "infeasibility" outcome is a valid research result and should be documented as clearly as a "here's the recommended strategy" outcome.

**Impact:** Addresses IN-005-it1. Estimated Actionability impact: +0.04.

---

### Ceiling Analysis

**Current composite: 0.72. C4 threshold: 0.95. Required gain: +0.23.**

If all priority recommendations are implemented:

| Dimension | Current | Estimated Gain | Target |
|-----------|---------|---------------|--------|
| Completeness | 0.72 | +0.17 | 0.89 |
| Internal Consistency | 0.71 | +0.19 | 0.90 |
| Methodological Rigor | 0.68 | +0.18 | 0.86 |
| Evidence Quality | 0.70 | +0.09 | 0.79 |
| Actionability | 0.74 | +0.15 | 0.89 |
| Traceability | 0.80 | +0.05 | 0.85 |

**Projected weighted composite (post-revision):**
0.89 × 0.20 = 0.178
0.90 × 0.20 = 0.180
0.86 × 0.20 = 0.172
0.79 × 0.15 = 0.119
0.89 × 0.15 = 0.134
0.85 × 0.10 = 0.085
**Projected composite: 0.868**

**Ceiling concern:** Even with all 15 recommendations implemented, the projected composite of 0.868 does not clear the C4 threshold of 0.95. This suggests that:

1. The Evidence Quality dimension (projected 0.79) represents a genuine constraint — a GitHub Issue draft cannot provide the empirical evidence that would push this dimension to 0.92+. Evidence quality above 0.85 in this dimension would require the capability audit results to be incorporated.
2. The Methodological Rigor dimension (projected 0.86) has a practical ceiling for a requirements/specification document — full methodological rigor requires the research itself to be completed.

**Ceiling recommendation:** This deliverable is a **GitHub Issue specification**, not a research report. A well-specified GitHub Issue has natural dimension ceilings due to its form:
- A specification cannot demonstrate Evidence Quality the way a research report can
- A specification cannot demonstrate Methodological Rigor at the level of an executed methodology

**Suggested C4 calibration:** For GitHub Issue specifications, the relevant threshold should be applied to the *specification quality*, not the research quality. The target should be: does the specification unambiguously enable a qualified implementer to produce a high-quality research deliverable? At that calibration, the realistic maximum for this form is approximately 0.90-0.92.

**Path to PASS:** Implement R-001 through R-015. Re-score at iteration 2. Project estimated composite: 0.87. If ceiling analysis is accepted (specification-type adjustment), this may achieve PASS. If not, iteration 3 targeting Evidence Quality elevation (adding derived quantities, capability verification pre-results, and traceability to Jerry HARD rules) would be required.

---

## Execution Statistics

| Metric | Value |
|--------|-------|
| **Total Findings** | 47 |
| **Critical** | 15 |
| **Major** | 25 |
| **Minor** | 7 |
| **Strategies Executed** | 10 of 10 |
| **H-16 Compliant** | Yes (S-003 first) |
| **H-15 Self-Review** | Applied before persistence |
| **Composite Score** | 0.72 |
| **C4 Threshold** | 0.95 |
| **Verdict** | REJECTED (significant rework required) |
| **Revision Recommendations** | 15 (R-001-it1 through R-015-it1) |
| **Projected Post-Revision Composite** | 0.87 |

---

*Report generated: 2026-02-25*
*Agent: adv-executor v1.0.0*
*Execution ID: it1*
*Constitutional Compliance: P-001 (evidence-based), P-002 (file persisted), P-003 (no subagents), P-004 (provenance cited), P-011 (specific evidence), P-022 (no minimization)*
