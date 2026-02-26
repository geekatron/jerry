### The vision

Picture this: you open a PR, leave a comment — "this auth flow needs error handling for expired tokens" — and walk away. By the time you're back from the chairlift, Claude Code has read your comment, understood the context, checked out the branch, fired up a full Jerry session, made the fix, pushed the commit, and replied to your comment with what it did and why. No babysitting. No copy-pasting context. No "hey Claude, look at this PR." It just *listened* and *did the work*.

Now picture that at scale. Five PRs open. Three GitHub issues queued. You dispatch Claude Code instances like sending ski patrol to different runs — each one gets its assignment, loads its context, works its line, and reports back. One instance is resolving PR feedback on the auth refactor. Another is working a GitHub issue for the new API endpoint. A third is responding to a reviewer comment about test coverage. They're all running full Jerry sessions — worktracker, quality enforcement, the whole mountain.

This is the automation layer that turns Claude Code from a tool you *use* into a teammate that *works alongside you*. And we need to figure out the best way to build it.

### Why this matters

Right now, Claude Code is a single-player experience. You sit in a terminal, you give it work, you watch it work, you give it more work. That's powerful — but it doesn't scale. When you have multiple PRs open, multiple issues queued, and reviewer feedback piling up, you become the bottleneck. Not because Claude Code can't do the work, but because you have to be there to tell it what to do.

The gap isn't capability — it's *dispatch*. Claude Code can already:
- Read and understand PR diffs
- Make code changes based on feedback
- Run tests and verify its work
- Work within Jerry's guardrail framework

*Note: These capabilities are what Claude Code exhibits in interactive terminal sessions. Whether they extend fully to headless automated dispatch is the premise of Phase 0 verification. The strategies assessed in this issue should not assume these capabilities exist headlessly until Phase 0 confirms them.*

What it can't do today is *listen on its own*. It can't watch a PR for new comments. It can't pick up a GitHub issue and start working without you invoking it. It can't run N instances in parallel across different work items.

Closing that gap is the difference between "I use an AI coding tool" and "I have an AI engineering team." You don't tell every engineer on the team what to do every minute — you assign work, set expectations, and let them execute. That's what this issue is about.

The mountain doesn't ski itself — but the right infrastructure means you can have multiple people skiing different lines simultaneously instead of taking turns on a single run.

### Core capabilities

The solution MUST support these core capabilities. Each strategy assessed in this issue must address how it achieves each one.

> **Note:** This section uses CAP-1 through CAP-4 for capability identifiers. These are distinct from Jerry's C1-C4 criticality levels defined in `quality-enforcement.md`.

#### CAP-1: PR Comment Listening

Deploy one or more Claude Code instances that monitor an open PR for new comments and review feedback. When a comment is posted (by a human reviewer), the instance:

1. Detects the new comment event
2. Reads the comment content and surrounding diff context
3. Determines if the comment requires code changes, clarification, or acknowledgment
4. If code changes are needed: checks out the PR branch, makes the changes, pushes a commit, and replies to the comment with what was done
5. If clarification is needed: replies to the comment asking for clarification
6. If acknowledgment only: replies acknowledging the feedback

**Constraints:**
- MUST handle multiple comments on the same PR without race conditions
- MUST NOT push changes that break existing tests (run test suite before push)
- MUST respect branch protection rules and required reviews
- MUST handle concurrent reviewers commenting on the same PR

#### CAP-2: Issue-Driven Dispatch

Seed a Claude Code instance with a GitHub issue so it can work autonomously based on the issue description. The instance:

1. Reads the issue title, body, labels, and any linked PRs
2. Creates a working branch from the appropriate base branch
3. Implements the work described in the issue
4. Opens a PR referencing the issue
5. Responds to any PR feedback received (per CAP-1)

**Constraints:**
- MUST be dispatchable via a simple command or trigger (e.g., label assignment, slash command in issue, CLI invocation)
- MUST create meaningful commit messages and PR descriptions
- MUST handle issues of varying complexity (from single-file fixes to multi-file features)
- SHOULD be able to decompose complex issues into incremental commits

#### CAP-3: Multi-Instance Orchestration

Dispatch N-many Claude Code instances concurrently, each working on different PRs or issues.

> **Definition of concurrent:** For the purposes of this issue, "concurrent" means instances that are simultaneously active (in-progress, not queued) at the same time. A minimum of 5 instances must be capable of simultaneously executing work (reading comments, making code changes, running tests) without requiring any instance to wait for another to complete. Queue-based architectures where instances are limited to fewer than 5 simultaneously active workers do NOT satisfy this requirement.

**Constraints:**
- MUST support at minimum 5 concurrent instances (rationale: 5 is a conservative starting point for initial OSS launch; the researcher should validate or adjust this target based on comparable OSS project PR volume data obtained during research)
- MUST prevent instances from interfering with each other (branch conflicts, file locks, shared state)
- MUST provide visibility into instance status (running, completed, failed, waiting for feedback)
- MUST handle instance failures gracefully (crash recovery, timeout handling)
- MUST NOT spawn Claude Code instances that themselves spawn additional Claude Code instances (P-003 violation — max 1 level of agent recursion). Each strategy MUST document its instance spawning model and confirm that automated instances are terminal workers, not orchestrators.
- SHOULD support configurable concurrency limits
- SHOULD report aggregate status across all instances

#### CAP-4: Feedback Loop

Instances MUST be able to receive and respond to human feedback in a conversational loop.

**Constraints:**
- MUST support multi-turn conversations within a PR comment thread
- MUST maintain context across multiple feedback rounds (remember prior comments and changes)
- MUST respect a "stop" or "dismiss" signal from the human reviewer
- MUST NOT exceed 10 feedback rounds per comment thread (rationale: beyond 10 rounds, human escalation is more appropriate than continued automated iteration; this value should be validated during PoC testing and adjusted based on observed convergence rates). For the purposes of this requirement, a "feedback round" consists of one human comment (or comment set posted within the same GitHub review submission) followed by one Claude Code response. Each distinct human comment initiation that triggers a Claude Code response counts as one round.
- SHOULD support reviewer approval as a signal to stop iterating

### Strategy requirements

Each strategy assessed in this issue MUST address the following dimensions. The strategy comparison deliverable MUST use a consistent matrix across all strategies.

**Dimension tiering:** Dimensions are organized into three tiers to structure the comparison and recommendation decision:

| Tier | Dimensions | Assessment mode |
|------|-----------|----------------|
| **Tier 1: Must Pass** | Jerry integration, Security, Reliability | Binary pass/fail per criteria below — strategies failing any Tier 1 dimension are disqualified regardless of other scores |
| **Tier 2: Trade-off** | Architecture, Deployment model, Scalability | Comparative — scored and ranked relative to other strategies |
| **Tier 3: Inform** | Cost, Complexity, Latency, Limitations | Informational — documented but not decision-determining |

**Dimension definitions:**

| Dimension | Tier | What to assess |
|-----------|------|---------------|
| **Jerry integration** | 1 | How each instance runs a full Jerry session (JERRY_PROJECT, worktracker, quality enforcement, artifact persistence). See [Jerry integration requirements](#jerry-integration-requirements) for specifics. |
| **Security** | 1 | API key management, secret handling, repository permissions, least-privilege access. Each strategy MUST define the minimum permission scope for each secret/credential used — specifically: (a) repository write access scope (which branches? main-excluded?), (b) Claude API key scope (can it be scoped to a specific project?), (c) any third-party service credentials. The principle of least privilege MUST be explicitly applied and documented for each credential. MUST include adversarial input handling WITH PROPOSED MITIGATIONS. Documentation of a threat without a proposed mitigation is insufficient for Tier 1 compliance. Each threat category (prompt injection from untrusted external contributor comments, repository permission escalation, secret exfiltration via crafted PR content) MUST be accompanied by: (a) the specific attack vector for this strategy, (b) the proposed mitigation, and (c) the residual risk after mitigation. Strategies that cannot propose a viable mitigation for any Tier 1 security threat are DISQUALIFIED. **Mitigation quality standard:** A "viable mitigation" MUST meet all of: (a) the mitigation is implementable without modifying Claude Code itself, (b) the mitigation can be described specifically (e.g., "token sanitization using allowlist of permitted characters" not "sanitize inputs"), and (c) the residual risk after mitigation is explicitly assessed as LOW, MEDIUM, or HIGH. Mitigations assessed as HIGH residual risk require escalation to the issue author before the strategy can proceed to Tier 2 scoring. |
| **Reliability** | 1 | Failure modes, recovery mechanisms, data loss risks |
| **Architecture** | 2 | How the system is structured: event detection, instance lifecycle, state management. MUST also address: does the architecture respect P-003 (no recursive agent spawning)? Strategies proposing orchestrator-spawning-orchestrator topologies are disqualified. |
| **Deployment model** | 2 | Cloud-native (GitHub Actions, serverless), self-hosted (Docker, K8s), or hybrid |
| **Scalability** | 2 | How the strategy handles N concurrent instances, resource limits, cost scaling |
| **Cost** | 3 | Estimated cost per instance-hour, cost at N=5/10/20 concurrent instances |
| **Complexity** | 3 | Implementation effort, operational overhead, maintenance burden |
| **Latency** | 3 | Time from event (comment posted, issue assigned) to instance response |
| **Limitations** | 3 | What each strategy cannot do, known constraints, deal-breakers |

**Tier 1 pass criteria:**

| Dimension | Minimum pass criteria |
|-----------|----------------------|
| **Jerry integration** | The strategy can implement ALL eight Jerry integration requirements without architectural workarounds that invalidate the requirement. At minimum 6 of 8 must be achievable natively; the remaining 2 may require documented workarounds with acceptable trade-offs. |
| **Security** | ALL three threat categories (prompt injection, permission escalation, secret exfiltration) MUST have a proposed mitigation with stated residual risk. Additionally, for each proposed mitigation, the researcher MUST either: (a) cite a documented case study or benchmark demonstrating the mitigation's effectiveness in an analogous deployment (defined as: a system that executes code autonomously based on external user input AND operates with secrets present in the execution environment), OR (b) execute a minimal PoC demonstrating that the mitigation prevents the threat vector in the assessed environment. Paper mitigations without effectiveness evidence do NOT satisfy Tier 1. A strategy is DISQUALIFIED if any threat category has "no viable mitigation." |
| **Reliability** | The strategy must support: (a) instance failure recovery without data loss, (b) crash recovery for in-progress sessions, (c) graceful handling of GitHub API rate limiting, and (d) execution time limits: strategies where the maximum execution time of the deployment environment is less than the estimated maximum Claude Code session duration for complex issues are DISQUALIFIED, unless the strategy documents a session resumption mechanism that preserves context across execution boundaries. Strategies with "no recovery mechanism" for any of (a)-(c) are DISQUALIFIED. |

**Tier 2 Scoring Scale:** Each Tier 2 dimension MUST be scored on a 0-10 scale using the following anchors: 0-2 = not viable for this use case; 3-4 = viable but requires significant investment or workarounds; 5-6 = viable with reasonable implementation effort; 7-8 = strong fit for typical use case; 9-10 = ideal solution for this dimension. The comparison matrix MUST show individual dimension scores and a composite Tier 2 score per strategy. Scoring calibration: a strategy scoring 9+ on Architecture but 2 on Deployment Model should not be recommended to a team with no DevOps — dimensional balance matters.

**Score justification requirement:** Every Tier 2 score entry in the comparison matrix MUST be accompanied by a written justification of 2-4 sentences citing specific evidence (e.g., platform documentation, benchmark data, community reports, or empirical testing results). Scores without evidence justification are invalid. Example: "Architecture score: 7/10 — GitHub Actions provides native event-driven triggering via workflow files [cite: GitHub docs], but state persistence between workflow runs requires external storage [cite: testing evidence], reducing the score from a potential 9."

**Score calibration examples (for inter-rater alignment):**
- Architecture 3/10: Event-based architecture lacks native state management — every run requires rebuilding full context from scratch, requiring a persistent external DB with no native solution (e.g., GitHub Actions without caching)
- Architecture 7/10: Event-driven with native state via platform primitives (e.g., GitHub Actions + cache, Docker with volume mounts) — one integration point required
- Architecture 9/10: Dedicated orchestration layer with native state, retry, and observability (e.g., K8s operator with etcd-backed CRDs)
- Deployment Model 3/10: Requires dedicated infrastructure team to deploy, monitor, and maintain; 10+ configuration steps with no automation
- Deployment Model 7/10: Deploys via standard tooling (docker-compose, terraform); operational overhead manageable by 1-3 engineers
- Deployment Model 9/10: Zero-infrastructure deployment — runs entirely within existing CI/CD platform with standard configuration files
- Scalability 3/10: Single-process architecture; concurrent instances require manual process management with no built-in scaling
- Scalability 7/10: Horizontal scaling via platform primitives (e.g., container replicas, parallel workflow runs); requires configuration but no custom code
- Scalability 9/10: Auto-scaling based on demand with platform-native primitives; scales from 1 to 20+ instances without configuration changes

**Recommendation selection criteria:** A strategy is RECOMMENDED if it: (a) passes all Tier 1 dimensions, (b) scores highest in the Tier 2 comparison, AND (c) is operationally feasible for a team of 1-3 engineers with no dedicated DevOps. If multiple strategies pass Tier 1, the recommendation should include a primary recommendation (targeting 1-3 engineers with no dedicated DevOps) and a secondary recommendation (for teams with dedicated DevOps capacity where operational complexity is not a constraint). Document the specific infrastructure preference that differentiates the two (e.g., cloud-native vs. self-hosted).

### Minimum strategy set

The research MUST assess at minimum the following 6 strategies. The implementer MAY add additional strategies discovered during research. Each strategy MUST be assessed against the full [Strategy requirements](#strategy-requirements) dimension matrix.

#### Strategy 1: GitHub Actions Event-Driven Workflow

Use GitHub Actions workflows triggered by PR comment events (`issue_comment`, `pull_request_review_comment`) and issue events (`issues.labeled`, custom dispatch). Each workflow run spins up a Claude Code instance in the Actions runner environment.

**Key questions to answer:**
- How does Claude Code install and authenticate in a GitHub Actions runner?
- What are the runner timeout limits and how do they affect long-running sessions?
- How is state persisted between workflow runs (for multi-turn conversations)?
- What is the cost model (GitHub Actions minutes)?
- Can the runner environment support full Jerry session requirements?

#### Strategy 2: Docker Containers with Webhook Listener

Deploy a webhook listener service that receives GitHub webhook events and dispatches Docker containers running Claude Code. Each container is a self-contained Claude Code environment with Jerry configuration.

**Key questions to answer:**
- How is the webhook listener deployed and scaled?
- How are Docker containers provisioned and destroyed?
- How is state managed across container restarts?
- What infrastructure is required (container registry, orchestrator, persistent storage)?
- How are secrets injected into containers?

#### Strategy 3: Claude Code SDK / Claude Agent SDK Custom Orchestrator

Build a custom orchestrator using the Claude Code SDK or Claude Agent SDK that manages multiple Claude Code sessions programmatically. The orchestrator listens to GitHub events and dispatches SDK-managed sessions.

**SDK availability prerequisite:** Before researching this strategy in depth, the implementer must verify: (1) Is a public Claude Code SDK or Claude Agent SDK available? (2) Is it documented? (3) Can it manage multiple concurrent sessions? If SDK is not available: research Strategy 3 as a "future strategy" — document what the SDK would need to provide to enable this architecture, and estimate when this strategy becomes viable based on Anthropic's public roadmap and communications.

**Key questions to answer:**
- What is the current state of the Claude Code SDK / Agent SDK?
- Can the SDK manage multiple concurrent sessions?
- How does the SDK handle Jerry session lifecycle (start, worktracker updates, end)?
- What programming language and runtime does the orchestrator use?
- How does this compare to CLI-based approaches in terms of control and observability?

#### Strategy 4: GitHub App with Serverless Functions

Build a GitHub App that receives webhook events and dispatches serverless functions (AWS Lambda, Google Cloud Functions, Cloudflare Workers) that invoke Claude Code.

**Key questions to answer:**
- What are the execution time limits of serverless platforms (Lambda 15min, etc.)?
- How does Claude Code run in a serverless environment?
- How is the repository cloned and workspace managed in ephemeral environments?
- What is the cold start latency?
- How does the GitHub App model handle permissions and installation?

#### Strategy 5: Kubernetes Operator with Custom Resource Definitions

Build a Kubernetes operator that manages Claude Code instances as custom resources. Each PR or issue gets a CRD instance that the operator manages through its lifecycle.

**Key questions to answer:**
- What is the overhead of running a K8s cluster for this use case?
- How do CRDs map to PR/issue lifecycle?
- How is the operator built (kubebuilder, operator-sdk)?
- What are the scaling characteristics?
- Is K8s overkill for the typical use case (5-20 concurrent instances)?

#### Strategy 6: GitHub CLI Polling / Cron-Based Dispatch

The simplest possible architecture: a scheduled process (cron job, GitHub Actions schedule trigger, or polling daemon) that periodically calls `gh pr list` and `gh api` to check for new PR comments or issue assignments, then invokes `claude` CLI to handle each item.

**Key questions to answer:**
- What is the polling latency (minimum response time from comment to instance dispatch)?
- How are concurrent items handled in a single-process polling model?
- What is the operational overhead of a persistent polling process vs. event-driven architectures?
- Does simplicity of implementation and operation outweigh latency limitations for a 1-3 engineer team?
- How does this architecture compare to event-driven strategies for the CAP-3 (5 concurrent) requirement?

### Jerry integration requirements

Every strategy MUST address how Claude Code instances integrate with the Jerry Framework at the full-session level. This is not optional — Jerry integration is a first-class requirement, not an afterthought.

| Requirement | Description |
|-------------|-------------|
| **JERRY_PROJECT** | Each instance MUST have `JERRY_PROJECT` set to an appropriate project. The strategy must define how projects are assigned. Research MUST assess these three assignment models: (1) **Per-repo model** — all automated instances for a repository share one JERRY_PROJECT; (2) **Per-instance model** — each automated instance creates and uses a transient JERRY_PROJECT for its work duration; (3) **Per-work-item model** — each PR or issue gets a dedicated JERRY_PROJECT, enabling PR-scoped artifact isolation and audit trail. For each model, document: worktracker isolation characteristics, aggregate visibility across instances, artifact naming conventions, and cleanup procedure. **Assignment model recommendation criteria:** After documenting all three models, the researcher SHOULD recommend one based on: (a) per-repo if aggregate visibility across all automated instances is the priority; (b) per-work-item if PR-scoped audit trails and artifact isolation are the priority; (c) per-instance if ephemeral isolation with minimal overhead is the priority. For the Jerry OSS automation use case specifically, the researcher SHOULD assess whether PR-scoped audit trails (criterion b) are the highest priority given Jerry's worktracker and artifact persistence conventions, and document whether this assessment holds after strategy research. |
| **Session lifecycle** | Each instance MUST run `jerry session start` at the beginning of work and `jerry session end` at completion. Abandoned sessions (instance crash) must be recoverable. |
| **Worktracker** | Each instance MUST update the worktracker with its work items. The strategy must define how worktracker entries from automated instances are distinguished from human-initiated work. |
| **Quality enforcement** | Instances MUST follow `.context/rules/` quality standards. The strategy must define how criticality levels are assigned for automated work (suggested: C2 default, escalate to C3 for multi-file changes). |
| **Artifact persistence** | Work artifacts (research, analysis, decisions) MUST be persisted to the repository per Jerry conventions. The strategy must define how artifacts from N concurrent instances avoid conflicts. |
| **Context loading** | Each instance MUST load Jerry's `.context/rules/` and `.claude/` configuration at session start. The strategy must address how this works in containerized/ephemeral environments. |
| **Worktree isolation** | Each automated instance MUST operate in an isolated git worktree to prevent branch conflicts across concurrent instances. The strategy MUST define: how worktrees are created at dispatch time, how they are named (suggested convention: `{repo}-wt/auto-{pr-number}` or `{repo}-wt/auto-{issue-number}`), and how they are cleaned up on instance completion or failure. Strategies that cannot provide worktree isolation must document this as a known limitation. |
| **Headless escalation** | Jerry quality enforcement includes human escalation triggers (AE-006 graduated context fill escalation, H-19 governance escalation). Automated instances cannot escalate to a human interactively. Each strategy MUST define: how AE-006 CRITICAL/EMERGENCY conditions are handled when no human is available (e.g., instance self-terminates, posts GitHub comment requesting human review, writes to worktracker and pauses). The fallback behavior MUST be documented and must not silently continue with degraded quality. |
| **Governance file isolation** | Automated instances MUST NOT modify files in `.context/rules/`, `.claude/rules/`, or `docs/governance/` directories. These modifications trigger AE-002 (auto-C3 escalation) which requires a human reviewer — and no human is present in automated dispatch. Each strategy MUST define how its execution environment prevents automated modification of governance files (e.g., read-only bind mounts, file permission restrictions, `.gitignore`-equivalent exclusions for automated commits). |

### What this does NOT include

- **Implementation of any strategy.** This issue produces requirements and a strategy assessment. Implementation is a separate issue (or set of issues) based on the selected strategy.
- **Modifications to Claude Code itself.** Strategies must work with Claude Code as it exists today (or with documented assumptions about upcoming features). No "fork Claude Code and add webhook support" proposals.
- **CI/CD pipeline design.** This is about dispatching Claude Code for interactive PR work and issue resolution, not about integrating Claude Code into build/test/deploy pipelines (though strategies may leverage CI infrastructure).
- **Cost optimization.** The strategy assessment should estimate costs, but optimizing costs is a follow-on concern after strategy selection.
- **Multi-repository support.** Initial scope is single-repository. Multi-repo orchestration is a future enhancement.

### Acceptance criteria

- [ ] Phase 0 (Claude Code headless capability audit) has been completed and its findings are documented, including which capabilities were verified as working vs. which depend on assumptions about future features
- [ ] At minimum 6 deployment strategies have been researched and documented, each assessed against the full [Strategy requirements](#strategy-requirements) tiered dimension matrix
- [ ] Each strategy addresses all four core capabilities (CAP-1: PR Comment Listening, CAP-2: Issue-Driven Dispatch, CAP-3: Multi-Instance Orchestration, CAP-4: Feedback Loop) with specific architectural detail — not just "this is possible" but *how* it works for each capability
- [ ] Each strategy addresses all [Jerry integration requirements](#jerry-integration-requirements) with specific implementation detail
- [ ] A comparison matrix summarizes all strategies across all dimensions with quantitative data where available (cost estimates, latency ranges, concurrency limits) and qualitative assessments where quantitative data is not feasible
- [ ] Security considerations are documented for each strategy, including: API key management, repository permission model, secret injection, least-privilege analysis, and adversarial input handling from untrusted external contributors (prompt injection, permission escalation, secret exfiltration). Strategies that cannot propose a viable mitigation for any Tier 1 security threat are DISQUALIFIED per the [Strategy requirements](#strategy-requirements) security dimension
- [ ] A recommendation section identifies the top 1-2 strategies with rationale, trade-offs acknowledged, and conditions under which the recommendation would change
- [ ] Known risks and open questions are documented for each strategy, with specific follow-up research items for any question that could not be answered during this assessment
- [ ] The assessment explicitly states which Claude Code features/capabilities were verified as existing vs. assumed/hoped-for, so the reader knows what is buildable today vs. what depends on future Claude Code releases
- [ ] The research output (comparison matrix and recommendations document) has been reviewed using the `/adversary` skill (adv-scorer agent for S-014 scoring). Self-assessment alone is NOT acceptable — the S-014 execution report MUST be linked from the PR description. MUST achieve >= 0.92 (PASS threshold per quality-enforcement.md H-13). Per H-13, deliverables below 0.92 are REJECTED and revision is required. Deliverables in the REVISE band (0.85-0.91) are still rejected. A deliverable may only be submitted as a PR when the S-014 composite score is >= 0.92.

### Approach

The implementer should follow this phased approach. Phase 0 is a prerequisite gate — Phases 1-7 MUST NOT begin until Phase 0 passes.

**Phase 0 (Prerequisite gate): Claude Code headless capability verification**

Before any strategy research begins, the implementer MUST verify that Claude Code can operate in non-interactive/headless mode sufficient for automated dispatch. Specifically:
- Can Claude Code be invoked via CLI in a non-interactive session (no TTY attachment)?
- Can Claude Code operate in a GitHub Actions runner, Docker container, and/or serverless function?
- Does `JERRY_PROJECT` work as an environment variable in non-interactive sessions?
- Can `jerry session start` be executed without TTY attachment?
- What CLI flags, environment variables, or configuration are required for headless operation?

**Empirical execution REQUIRED:** Documentary answers are NOT acceptable for Phase 0. The implementer MUST execute a full Jerry session lifecycle in each assessed environment (GitHub Actions runner, Docker container) and document: (1) the exact commands run, (2) the environment context, (3) the output or error at each step, (4) pass/fail determination. Third-party blog posts or community reports are supplementary evidence only — they do not substitute for empirical execution by the implementer.

**Empirical execution standard:** `claude --version` or equivalent version/help commands are NOT acceptable as Phase 0 empirical evidence. Phase 0 MUST include at minimum: (1) invocation of `jerry session start` in the target environment, (2) a file modification made autonomously by Claude Code (not manually by the researcher) and committed to the repo, and (3) `jerry session end` — all executed without error. The exact commands, environment context, output (including Claude Code CLI version via `claude --version`), and pass/fail determination MUST be documented for each environment tested. If any step fails, that environment fails Phase 0 for that step.

**Gate decision:** If headless operation is not viable in any assessed environment, halt and report to the issue author before proceeding. Do NOT continue to strategy research if the foundational capability is unconfirmed. See [Infeasibility outcome](#infeasibility-outcome) for what to do if the gate fails.

**Partial viability:** If Claude Code operates headlessly in some environments but not others (e.g., works in Docker but not GitHub Actions), this is a partial Phase 0 pass. Document which environments pass and which fail. Continue to strategy research but restrict strategy assessment to environments where headless operation was empirically confirmed. Strategies that require environments where Phase 0 failed are NOT viable without additional Claude Code changes.

**Partial Phase 0 pass and recommendation constraints:** If Claude Code operates headlessly in some environments but not others, AND no strategy viable in the confirmed environments passes Tier 1 criteria, this is an infeasibility outcome — even if additional environments might have passed Phase 0. Do NOT continue to Phase 1 to research strategies in unconfirmed environments. Report the partial Phase 0 pass with confirmed environments and the Tier 1 failure, then follow the [Infeasibility outcome](#infeasibility-outcome) procedure.

**Phase 0 timeline:** MUST complete within 3 days of issue assignment to the implementer. If Phase 0 reveals a blocking issue, report within 3 days and do not proceed with Phase 1 without author acknowledgment.

**Phase 0 escalation trigger:** If Phase 0 has not completed within 3 calendar days of issue assignment, the implementer MUST immediately comment on this issue with: (a) the current Phase 0 status, (b) the blocking issue, and (c) a revised completion estimate. Do NOT silently continue Phase 0 beyond 3 days.

1. **Audit current Claude Code capabilities** (Phase 0 output): Document what Claude Code can do today — CLI flags, SDK availability, authentication mechanisms, session management, headless/non-interactive mode support, GitHub integration features. This becomes the capability baseline that all strategies build on.

2. **Research each strategy independently**: For each of the 5+ strategies, research the deployment model, assess against the tiered dimension matrix, and document findings. Use Context7 for any SDK/framework documentation. Use WebSearch for deployment patterns, cost models, and community examples.

3. **Build the comparison matrix**: After individual strategy research, compile the comparison matrix. Ensure consistent assessment criteria. Apply Tier 1 pass/fail first to eliminate non-viable strategies. Score remaining strategies on Tier 2 comparatively. Document Tier 3 informational dimensions. Quantify where possible; qualify with confidence levels where not.

4. **Assess Jerry integration feasibility**: For each strategy, work through the Jerry integration requirements concretely. Identify which requirements are straightforward, which require workarounds, and which are blockers. Assess all three JERRY_PROJECT assignment models for each strategy.

5. **Draft recommendations**: Based on the tiered matrix, Jerry integration feasibility, and overall trade-off analysis, recommend the top 1-2 strategies per the [recommendation selection criteria](#strategy-requirements). Document conditions under which the recommendation would change (e.g., "if Claude Code SDK adds feature X, Strategy 3 becomes preferred").

6. **Document risks and open questions**: For each strategy, list known risks and unresolved questions. Flag any assumptions that need validation before implementation begins.

7. **Quality gate and PR submission**: Before submitting the PR:
   - **Pre-quality-gate review cycle (H-14):** Complete at minimum 3 creator-critic-revision cycles on the comparison matrix and recommendations document. Required cycle composition: (1) Self-review using S-010 (required — H-15), (2) `/adversary` adv-executor **S-007 constitutional compliance check (required — H-18)**, and (3) one additional adversary strategy or external reviewer. S-007 MUST be one of the 3 required cycles. Omitting S-007 violates H-18. If both S-003 (Steelman) and S-002 (Devil's Advocate) are used as review cycles, S-003 MUST precede S-002 per H-16. The PR description MUST document that at minimum 3 review iterations were completed.
   - **H-14 cycle quality requirement:** Each critic phase in the creator-critic-revision cycle MUST produce at minimum one documented finding that requires a revision response from the creator. If a critic review produces zero findings, the cycle does not count toward the H-14 minimum. The "revision" phase of each cycle MUST document: (a) the finding from the critic, (b) the specific change made in response, and (c) confirmation that the change was applied.
   - **H-14 cycle counting:** The Phase 7 S-014 quality gate scoring run does NOT count as one of the 3 required H-14 creator-critic-revision cycles. The 3 cycles MUST be completed before Phase 7 quality gate scoring. The Phase 7 S-014 run is the quality gate check, not a review cycle.
   - **Quality gate scoring:** Run `/adversary` (adv-scorer) on the comparison matrix and recommendations document to obtain an S-014 score. Confirm score >= 0.92 (PASS threshold). If score is in the REVISE band (0.85-0.91), revise and re-score before submitting.
   - **PR submission:** All research artifacts must be persisted to the repository per Jerry conventions. The PR description MUST include: summary of recommendation, key trade-offs, S-014 composite score, and link to the full adversary execution report.

**Research depth definition:** For this issue, "research" means: documentary analysis, API/SDK documentation review, community report review, and targeted capability testing using free-tier or trial-tier infrastructure. Implementation of production-quality code is excluded. However, executing a minimal proof-of-concept (e.g., a single GitHub Actions workflow that invokes `claude --version` in a runner) to validate capability claims is WITHIN scope and REQUIRED where claims cannot be validated documentarily.

**Research project (H-04 compliance):** The research commissioned by this issue MUST be conducted under a dedicated JERRY_PROJECT. The implementer MUST use the next available `PROJ-{NNN}` identifier per `projects/README.md` (e.g., `PROJ-012-pr-automation` or similar, following the standard `PROJ-{NNN}-{slug}` naming convention). The actual identifier used MUST be documented in the first comment on this issue. The implementer MUST create this project directory structure before Phase 1 begins. All research artifacts referenced in this issue map to the project's work directory.

**Research artifacts location:** All research artifacts MUST be persisted to `work/research/pr-automation/` within the Jerry project. Artifact identifiers:
- Phase 0 report: `work/research/pr-automation/PR-AUTO-PHASE0.md`
- Strategy assessment documents: `work/research/pr-automation/strategies/`
- Comparison matrix: `work/research/pr-automation/PR-AUTO-MATRIX-v{N}.md` (increment N for each revision)
- Recommendations: `work/research/pr-automation/PR-AUTO-RECS-v{N}.md` (increment N for each revision)

**Research timeline:** Phase 0 (capability audit) MUST complete within 3 days. Phase 1 (strategy research): target 2-3 weeks. PR submission target: before OSS release. **OSS release anchor:** This timeline must be referenced to the target OSS release date. See the OSS release milestone for the current target date. The implementer MUST check the milestone date at issue assignment time and calculate the 2-week escalation trigger. If the research timeline is at risk of exceeding 2 weeks before the OSS release date, the implementer MUST comment on this issue with a revised timeline and escalation options. If Phase 0 reveals a blocking issue, report within 3 days and do not proceed with Phase 1 without author acknowledgment.

**Milestone date verification:** At issue assignment time, the implementer MUST verify that the OSS release milestone has a target date set. If the milestone has no date: comment on this issue requesting a date before proceeding with Phase 0. Do NOT use a date-less milestone as a timeline anchor.

**Security pre-assessment (before full strategy research):** Before beginning Phase 1 strategy research, the implementer MUST perform a 1-2 hour security pre-assessment: for each of the three Tier 1 threat categories (prompt injection, permission escalation, secret exfiltration), identify whether any viable mitigation class exists in principle for the assessed deployment environment. If no viable mitigation class exists for any category across all environments, halt and report as an infeasibility outcome before investing in full strategy research.

#### Infeasibility outcome

If Phase 0 reveals that Claude Code cannot operate headlessly in any assessed environment, or if the full strategy assessment concludes that no strategy achieves passing Tier 1 criteria without modifications to Claude Code itself, the research deliverable MUST: (1) document the specific blocking limitations, (2) identify what Claude Code changes would be required to unblock, (3) estimate a realistic timeline for when those changes might be available based on Anthropic's public communications, and (4) recommend the strategy most likely to become viable once those changes arrive. An "infeasibility" outcome is a valid research result and should be documented as clearly as a "here's the recommended strategy" outcome.

**Phase 0 failure and OSS release impact:** If Phase 0 reveals that Claude Code cannot operate headlessly in any assessed environment, the issue author MUST determine whether: (a) the OSS release should proceed without PR automation capability, (b) the release should be delayed pending Claude Code headless support, or (c) the automation strategy should be descoped from the OSS launch milestone. This decision MUST be made within 5 business days of the Phase 0 failure report and documented in this issue thread.

### Why now

Jerry is preparing for open-source release. When contributors start submitting PRs and opening issues, the ability to dispatch Claude Code instances to assist with PR feedback resolution and issue work becomes a force multiplier. It's the difference between one maintainer reviewing and resolving PR feedback manually, and having an automated engineering teammate that handles the routine work while the maintainer focuses on architectural decisions and community engagement.

The infrastructure for this needs to be assessed *before* launch — not after the PR queue starts growing. You don't build the ski patrol system after the resort opens. You have it ready on day one so when someone needs help on the mountain, the response is immediate.

This issue is the scouting run. We're assessing the terrain before we commit to a line. The actual construction comes after we know which line we're skiing.

This issue is part of the OSS release preparation work.
