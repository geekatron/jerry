# GitHub Issue Draft: Root README.md Accuracy Audit

## Document Sections

| Section | Purpose |
|---------|---------|
| [Title](#title) | Issue title |
| [Labels](#labels) | Issue labels |
| [Body](#body) | Full issue body |
| [Body: The problem](#the-problem) | Problem statement |
| [Body: Why this matters](#why-this-matters) | Motivation |
| [Body: Scope](#scope) | Work effort definition |
| [Body: What this does NOT include](#what-this-does-not-include) | Explicit exclusions |
| [Body: Acceptance criteria](#acceptance-criteria) | Verifiable completion conditions |
| [Body: Approach](#approach) | Implementation methodology |
| [Body: Verification standards](#verification-standards) | Claim verification methodology |
| [Body: Why now](#why-now) | Timing rationale |

---

## Title

Audit and update root README.md to be an accurate, factual representation of the project

## Labels

documentation, oss-prep

## Body

### The problem

The root `README.md` is the first thing anyone sees when they land on this repo. It's the trailhead sign. The chairlift map. The "you are here" marker before the first run. And right now, there's no guarantee it actually reflects what's on the mountain.

Jerry has evolved fast — 12 skills, 57 agents, a governance framework, CLI tooling, quality enforcement, multi-agent orchestration, offensive security methodology, and a documentation framework on the horizon. The root `README.md` may not accurately represent what the project is, what it does, how to get started, or what's changed since it was last touched. Features may be described that don't exist yet. Features that exist may not be described at all. The installation instructions might be stale. The architecture overview might describe a version of the project that's three refactors ago.

Nobody checks if the trailhead map still matches the mountain after every avalanche reshapes the terrain. This issue is that check.

### Why this matters

For open-source release, the `README.md` isn't just documentation — it's the project's handshake. It's the difference between "this looks interesting, let me try it" and "I have no idea what this is, moving on." A README that oversells, undersells, or misrepresents the project is worse than no README at all, because it sets expectations the project can't meet or hides capabilities the project actually has.

The goal is simple: every claim in the README must be factually true, every capability described must actually exist, and every instruction must actually work. No aspirational features. No stale examples. No dead links. Just the mountain as it actually is — which, frankly, is impressive enough without embellishment.

You don't need to exaggerate how sick the line is when the line is already sick. You just need to describe it accurately so people can find it.

### Scope

This issue covers a **full accuracy audit and update** of the root `README.md`. The work effort includes:

1. **Factual audit**: Compare every claim in the current README against the actual state of the codebase. Identify statements that are inaccurate, outdated, missing, or aspirational.
2. **Content update**: Rewrite the README so that every section accurately reflects the project as it exists today. Not as it existed six months ago. Not as it might exist next quarter. Today.
3. **Completeness check**: Ensure all major capabilities are represented — but only capabilities that actually work. If a feature is in-progress, it gets a clear status label (see acceptance criteria) or it stays out until it ships.
4. **Getting started verification**: Any installation, setup, or quickstart instructions must be tested and confirmed working from a fresh clone on at least one supported platform (macOS primary; Linux if possible).
5. **Link validation**: Every link in the README must resolve to a real, accessible destination.
6. **External perspective validation**: Before submitting the PR, have at least one person meeting the independence criterion in AC 6 read the draft README and confirm they can answer: What is Jerry? What does it do? How do I get started? Incorporate their feedback before submission.
7. **Audit baseline documentation**: Record the git commit SHA or release tag that was used as the codebase baseline for the audit. Include this in the PR description.
8. **In-progress feature labeling**: Identify any features in the current README that are not yet implemented and apply the standard "Status: Coming soon" label format consistently throughout the document.
9. **PR documentation**: Submit a PR with a diff summary of changes made and why, including the claim-verification log as a PR artifact or in the PR description.

### What this does NOT include

- Redesigning the README structure from scratch. If the audit reveals significant structural issues, the implementer MUST open a separate GitHub issue describing the proposed changes and receive explicit approval before restructuring. The audit PR MUST contain only content accuracy changes (factual corrections, dead link fixes, instruction updates). Structural changes are handled in a follow-on issue.
- Adding new sections for features that don't exist yet
- Marketing copy or promotional language — the README should be factual and direct. Note: this issue uses a metaphorical internal writing convention; the output README should use a neutral, professional technical voice appropriate for an open-source project. The audit deliverable is a factual, direct README — not a voice-styled document.
- Determining the content in advance — **the audit itself is the work effort**; this issue authorizes and scopes that work, it does not prescribe the outcome

### Acceptance criteria

- [ ] Every factual claim in the root `README.md` has been verified against the current codebase and MUST be documented in a claim-verification log per the requirements in [Verification standards](#verification-standards). The PR reviewer MUST verify that the log covers all factual claims by cross-checking against the README top-to-bottom. If entries appear to be missing, the reviewer flags for clarification before approving.
- [ ] Inaccurate, outdated, or aspirational statements have been corrected or removed
- [ ] All described features and capabilities actually exist and function as described
- [ ] Installation and setup instructions have been tested and confirmed working on at least one supported platform (macOS primary; Linux if possible). Testing SHOULD be performed from a fresh clone with no prior Jerry installation. At minimum, document any prerequisites the tester had pre-installed that a new user would need to install.
- [ ] All links resolve to valid destinations (no 404s, no dead anchors)
- [ ] The README accurately describes what Jerry is, what it does, and how to get started — nothing more, nothing less. This criterion MUST be assessed by at least one person who was not the primary implementer of the audit and has not actively contributed to Jerry in the past 90 days (or is not a current member of the Jerry team). If a suitable reviewer is unavailable, document this in the PR description. The PR reviewer should assess whether the external review was adequately independent.
- [ ] Any in-progress features mentioned are clearly labeled with a consistent indicator. Recommended format: `> **Status:** Coming soon — not yet implemented` or equivalent note that is visually distinct from feature descriptions and consistent throughout the document.
- [ ] The README reflects the current version. The implementer should document the git commit SHA or release tag that serves as the codebase baseline for this audit. All factual claims are verified against the codebase at that point in time.
- [ ] A diff summary of changes made is documented in the PR description for reviewer verification

### Approach

The implementer should:

1. Read the current `README.md` line by line
2. For each factual claim (see [Verification standards](#verification-standards)), verify it against the codebase using the appropriate verification type. Installation steps and CLI commands require behavioral verification; quantitative claims require quantitative verification; feature existence claims require existence verification at minimum.
3. Document every discrepancy found in the claim-verification log
4. Update the README to resolve all discrepancies
    - 4a. Validate all hyperlinks in the README resolve to accessible destinations (no 404s, no broken anchor fragments). Use an automated link checker or manual verification. Note: links valid at audit time may break before merge — re-validate within 24 hours of submitting the PR.
    - 4b. Identify any in-progress features and apply the standard label format from AC 7.
    - 4c. Document the git commit SHA or release tag used as the audit baseline.
5. If the initial review reveals that achieving full AC compliance requires work beyond content accuracy corrections (e.g., structural redesign, new sections, or rewrites touching more than half the document), flag this in a comment on the issue before proceeding. The issue author will provide guidance on scope priorities. If no response is received within 5 business days, proceed with content accuracy changes only and document the flagged concern in the PR description.
6. Test all instructions end-to-end. SHOULD use a fresh clone or a clean test environment. Document the test environment (OS, relevant pre-installed tools, Jerry version). If a fully clean environment is not feasible, explicitly note which pre-conditions were present during testing.
7. Before submitting the PR, have at least one person meeting the independence criterion in AC 6 review the draft README and confirm they can answer: What is Jerry? What does it do? How do I try it? Their feedback should be incorporated before submission.
8. Submit a PR with a clear summary of what changed and why, including the claim-verification log as a PR artifact or in the PR description

### Verification standards

This section defines how factual claims in the README should be verified.

**What constitutes a "factual claim":** Any statement that could be true or false as a matter of fact — feature existence, version numbers, command syntax, architecture descriptions, capability descriptions, agent/skill counts. This excludes rhetorical framing, metaphors, and opinions.

**Verification types:**

| Type | When to use | Example |
|------|------------|---------|
| **Existence verification** | A file, module, command, or feature is claimed to exist | "Jerry includes a `/problem-solving` skill" — verify the skill directory and SKILL.md exist |
| **Behavioral verification** | A command, workflow, or feature is claimed to produce a specific result | "Run `jerry session start` to begin a session" — verify the command runs successfully and produces the expected behavior |
| **Quantitative verification** | A specific count or metric is stated | "12 skills" — count the actual skill directories |

**Mandatory verification type assignments:**
- **All installation steps and setup instructions** MUST use behavioral verification. Run the command from a fresh clone, or from an environment that matches the prerequisites a new user would have. Document the test environment explicitly: OS version, pre-installed tools, any pre-conditions (e.g., active project configured, JERRY_PROJECT set). If a fresh clone is not feasible, document any pre-conditions that a new user would need to replicate your test environment. Configuration state that a new user would not have — such as an active project configured (JERRY_PROJECT set), a session already initialized, or project files pre-created — is NOT a new-user pre-condition and MUST be documented explicitly as a deviation. Reviewers MUST assess whether documented deviations affect the claim being verified and flag unacceptable deviations before approving.
- **All CLI command examples** MUST use behavioral verification. The command must run successfully and produce output consistent with what the README describes. Test from an environment representing new-user pre-conditions (see installation step guidance above). Document the command, the test environment, and the actual output. If the README describes a multi-step workflow (a sequence of commands that must be executed in order), behavioral verification MUST test the complete sequence from the starting state. Testing individual commands from the sequence without testing the full sequence does not satisfy behavioral verification for the described workflow.
- **All quantitative claims** (counts of skills, agents, versions) MUST use quantitative verification.
- **All capability descriptions and feature existence claims** MUST use existence verification at minimum; behavioral verification is RECOMMENDED for core workflow features (session management, skill invocation, quality enforcement).

**Evidence artifact:** The implementer MUST maintain a claim-verification log (a simple markdown table: claim, verification method, result, notes) and attach it as a PR artifact or include it in the PR description. This log enables independent reviewer verification of the audit's thoroughness.

**Log completeness:** The log must cover every factual claim in the README, enumerated top-to-bottom. As a quality check, the reviewer should be able to open the README and the log side-by-side and verify that no factual claims are missing from the log. A log with fewer entries than there are factual claims in the README MUST be flagged by the reviewer for clarification before approval.

This is not a creative writing exercise. It's a fact-checking exercise with a text editor. The mountain doesn't need a new marketing brochure — it needs an accurate trail map.

### Why now

Jerry is preparing for open-source release. The README is the front door. When new users and contributors arrive, the README is the first thing they read and the basis for their first impression. An inaccurate README at launch is a broken first impression that's hard to recover from.

This issue is part of the OSS release preparation work.

Get the map right before you open the resort. The skiing will speak for itself — but only if people can find the lifts.
