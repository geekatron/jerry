# Phase 2 Attack Surface — Jerry → CoWork Supply Chain

> **HISTORICAL — Phase-2 recon INPUT (2026-06-28), pre-ADR-PROJ031-003. SUPERSEDED for current state.**
> This document is the **point-in-time red-recon threat-intelligence input** that fed Phase-2 threat modeling. For the **current state**, consult **[ADR-PROJ031-003](../decisions/ADR-PROJ031-003-credential-protection-supply-chain.md)** and the **[STRIDE threat model](./phase2-stride-threat-model.md)** — they are the architecture of record. Specifically superseded here:
> - **Strip set:** this map shows `projects/`-only; the decided strip is **`projects/` AND `tests/`** (→ ~1,417 files, ADR-PROJ031-001 amendment / ADR-PROJ031-003 D1).
> - **Credential:** this map mentions a **PAT or deploy key**; the decided credential is a **GitHub App installation token** (short-lived, 1 h fixed expiry) or single-repo deploy key — **classic PAT is rejected** (ADR-PROJ031-003 D3).
> - **Control set:** this map predates the **D8 content-safety / prompt-injection gate**, the **D2** prevention-by-design ruleset (repository-admin-non-overridable; organization-owner detection-only), the **D4** immutable-release + attestation anchor, and the **D7** fail-closed + freshness + auto-revert monitor.
> - **CI trigger:** the "push to main OR v* tag" framing below is superseded by tags-`v*` + `workflow_dispatch` only (no push-to-main trigger).
>
> The analysis below is **retained UNEDITED as threat-intelligence provenance** (it honestly records what red-recon saw before the decisions were made). **Do not implement from this document** — use ADR-PROJ031-003 + the STRIDE model for current vectors, controls, claim-status, and the Phase-5 validation gates. This banner resolves the "wrong artifact" concern without revising the original recon.

> Adversary-perspective attack surface map for the Jerry → Claude CoWork distribution pipeline.
> Design-phase threat intelligence input for Phase 2 threat modeling and eng-architect Integration Point 1.
> Scope: `geekatron/jerry@main` through CI regeneration to `geekatron/jerry-claude-plugin` through org marketplace registration to CoWork user execution.
> Status: Design exercise on our own pipeline. No live target. Produced by red-recon, 2026-06-28.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Confirmed Pipeline Model](#confirmed-pipeline-model) | Validated distribution architecture and trust boundaries |
| [Vector Catalog](#vector-catalog) | Eight attack vectors with prerequisites, impact, rating, and blocking control |
| [V-01: Compromised Contributor](#v-01-compromised-contributor-write-access-to-main) | Direct write to main repo |
| [V-02: PR Expression Injection](#v-02-ci-workflow-injection-via-pr) | CI poisoning via zero-access PR attacker |
| [V-03: Malicious v-star Tag Rebuild](#v-03-malicious-v-tag-triggering-ci-rebuild) | Tag-triggered CI rebuild from attacker-controlled commit |
| [V-04: Compromised GitHub Action](#v-04-compromised-github-action) | Supply chain attack via third-party action |
| [V-05: Poisoned Generation Dependency](#v-05-poisoned-skeleton-generation-dependency) | Malicious Python or shell dependency in CI |
| [V-06: Push Credential Theft](#v-06-push-credential-theft-or-misuse) | Stolen PAT or deploy key used to push directly |
| [V-07: Dedicated Repo Tampering](#v-07-dedicated-repo-direct-tampering) | Direct write to jerry-claude-plugin without CI |
| [V-08: Org-Registration Spoofing](#v-08-org-registration-spoofing-and-typosquatting) | Lookalike repo registered as org marketplace |
| [Attack Path Prioritization](#attack-path-prioritization) | Vectors ranked by feasibility x impact |
| [Highest-Leverage Control](#highest-leverage-control) | Single control with broadest coverage |
| [Threat Intelligence for eng-architect](#threat-intelligence-for-eng-architect) | ATT&CK mapping and STRIDE summary (Integration Point 1) |

---

## Confirmed Pipeline Model

Based on `research/cowork-plugin-install-mechanism.md` (confirmed 2026-06-28):

```
geekatron/jerry@main
    |
    | [CI trigger: push to main OR v* tag]
    v
Skeleton Regeneration Job
  - checks out main (or tagged commit)
  - strips projects/ directory
  - validates file count (< 5,000)
  - writes marketplace.json, plugin.json
    |
    | [push credential: PAT or deploy key stored as GitHub secret]
    v
geekatron/jerry-claude-plugin  (DEFAULT branch = slim skeleton)
    |
    | [org admin registers via Anthropic server-side API]
    | [no per-user add path — org-level only; remote/account-managed]
    v
CoWork Org Marketplace
    |
    | [user clicks Install in CoWork GUI]
    v
CoWork Execution Context
  (isolated VM sandbox, account-scoped, embedded Claude Code)
  loads: SKILL.md files, agent .md files, plugin.json,
         marketplace.json, any included Python scripts
```

### Trust Boundaries

| ID | Boundary | Controls Required |
|----|----------|-------------------|
| TB-1 | GitHub identity → write access to `geekatron/jerry` | Branch protection, signed commits, 2-FA enforcement |
| TB-2 | GitHub Actions runner → push credential (GitHub secret) | Minimal secret scope, safe trigger events |
| TB-3 | Dedicated repo default branch → Anthropic CoWork serving | Branch protection on dedicated repo, PAT scope restriction |
| TB-4 | Anthropic org marketplace → individual CoWork user sessions | Org admin verification, canonical URL documentation |

### What "Malicious Content" Means in CoWork

CoWork loads markdown files as LLM context (skill instructions, agent definitions, system prompts). The attack payload is not a traditional binary; it is:

- **Prompt injection** — malicious instructions embedded in SKILL.md or agent .md files that hijack CoWork user sessions (exfiltrate context, execute unauthorized agentic actions)
- **Connector redirect** — modified `plugin.json` or `marketplace.json` declaring malicious MCP server URLs (attacker-controlled data exfiltration endpoint)
- **Script compromise** — modified Python scripts (e.g., jerry CLI) that execute in the CoWork VM sandbox with access to user files and network

---

## Vector Catalog

---

### V-01: Compromised Contributor (Write Access to main)

**Technique:** TA0001 Initial Access via valid account compromise; TA0195 Supply Chain Compromise

**Prerequisites:**
GitHub credentials for any account with push permission to `geekatron/jerry`. Viable paths: phishing a collaborator, credential stuffing against reused passwords, SSH key exfiltration from a developer's workstation, or session token theft via malicious OAuth app. Each additional collaborator on the repo is an independent attack surface.

**What the attacker achieves:**
Pushes a commit to `main` containing modified SKILL.md, agent .md files, `marketplace.json`, `plugin.json`, or Python scripts. The CI regeneration job fires on the push, checks out the poisoned `main`, produces the skeleton, and pushes it to `geekatron/jerry-claude-plugin`. All CoWork org users receive and execute the malicious skill/agent instructions on next CoWork plugin refresh. No special CI knowledge required — the attacker simply pushes valid-looking content.

**Feasibility x Impact:**
- Feasibility: MEDIUM — credential theft is a documented commodity attack; multiple collaborators multiply the attack surface
- Impact: HIGH — clean, uninterrupted path from push to all CoWork org users
- Rating: **HIGH (6/9)**

**Blocking control:**
Branch protection on `main` requiring a minimum of 2 approved reviews from named reviewers, signed commits (GPG/SSH), and no direct push allowed (including for repo admins). Combined with mandatory 2-FA for all collaborators at the org level.

---

### V-02: CI Workflow Injection via PR

**Technique:** T1059.004 Command and Scripting Interpreter; T1195.002 Supply Chain via compromised CI

**Prerequisites:**
None beyond a GitHub account. Any user can open a pull request against a public repository. This vector is exploitable with zero prior access to the repository.

**What the attacker achieves:**
Two sub-paths:

(a) **`pull_request_target` misconfiguration** — if the CI workflow uses the `pull_request_target` trigger, it runs in the context of the base branch with full access to repository secrets (including the push credential). An attacker opens a PR that modifies the workflow file or injects malicious steps. The workflow runs with secrets access, enabling the attacker to exfiltrate the push credential or push directly to the dedicated repo.

(b) **Expression injection** — if any `run:` step in the workflow interpolates PR metadata via `${{ github.event.pull_request.title }}`, `${{ github.event.pull_request.body }}`, or similar, a crafted PR title or description containing shell metacharacters executes arbitrary commands in the CI runner with access to the secrets environment. No workflow file modification required.

Both sub-paths result in arbitrary content being pushed to `geekatron/jerry-claude-plugin`, bypassing all code review.

**Feasibility x Impact:**
- Feasibility: HIGH — any GitHub user can open a PR; `pull_request_target` misconfiguration and expression injection are both extremely common and actively exploited in the wild
- Impact: HIGH — push credential exposure leads to direct dedicated repo compromise
- Rating: **CRITICAL (9/9)**

**Blocking control:**
Use only `pull_request` (not `pull_request_target`) for PR-triggered CI jobs — fork PRs cannot access secrets with `pull_request`. Never interpolate untrusted PR metadata in `run:` steps; use environment variables set from expressions instead of inline interpolation. Restrict the skeleton-push job to trigger exclusively on verified merges to `main` (a push event on the protected branch), not on pull request events.

---

### V-03: Malicious v-star Tag Triggering CI Rebuild

**Technique:** T1195.002 Supply Chain via poisoned source; T1078 Valid Accounts

**Prerequisites:**
Tag-push permission on `geekatron/jerry` (a subset of write access), combined with the CI workflow having a `push: tags: ['v*']` trigger. Requires the same initial credential theft as V-01 but targets tag-push specifically, which is often granted more broadly than direct branch push (and less frequently reviewed).

**What the attacker achieves:**
Creates a `v*` tag (e.g., `v99.0.0`) pointing to a commit containing malicious content — not necessarily on `main`, but on any commit the attacker controls. If the CI regeneration job runs on tag push, it checks out the tagged commit (not the protected `main` branch), builds the skeleton from attacker-controlled content, and pushes to the dedicated repo. Branch protection on `main` does not block this vector because the build source is the tagged commit, not `main`. The tag event bypasses code review entirely.

**Feasibility x Impact:**
- Feasibility: MEDIUM — requires contributor credentials; tag protection rules are often overlooked relative to branch protection
- Impact: HIGH — complete skeleton replacement with no review step between the tag and CoWork delivery
- Rating: **HIGH (6/9)**

**Blocking control:**
Configure GitHub Tag Protection Rules (or Ruleset) to restrict `v*` tag creation to a specific named set of repository admins. Alternatively, change the CI skeleton-push trigger to `workflow_dispatch` on a protected environment (requiring a named approver) rather than any tag push event. Verify the CI job explicitly checks out `main` by SHA rather than the triggering ref.

---

### V-04: Compromised GitHub Action

**Technique:** T1195.001 Supply Chain Compromise — Development Tools

**Prerequisites:**
Compromise of any GitHub Action referenced by the CI workflow. Common paths: maintainer account takeover of the action repository (phishing, credential stuffing); malicious PR merged to the action repo by a compromised reviewer; tag hijacking (pushing a new commit to a mutable tag such as `v4`). Real-world precedents with identical attack pattern: tj-actions/changed-files (March 2025), reviewdog/action-setup (March 2025), both of which exfiltrated CI secrets from thousands of repositories.

**What the attacker achieves:**
The compromised action executes in the CI runner with access to all environment variables, including the push credential stored as a GitHub secret. The action can: (a) directly push malicious content to `geekatron/jerry-claude-plugin` using the exfiltrated credential, (b) modify generated skeleton files in the runner workspace before the push step executes, or (c) exfiltrate the credential for later use (V-06). The repository's own code and review process are entirely bypassed.

**Feasibility x Impact:**
- Feasibility: MEDIUM — requires compromising a third-party action maintainer or repo, but multiple documented supply chain attacks demonstrate this is achievable at scale; mutable `@v4` style references are ubiquitous
- Impact: HIGH — full runner execution context with secrets access
- Rating: **HIGH (6/9)**

**Blocking control:**
Pin every GitHub Action reference to an immutable commit SHA (e.g., `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`). Enable Dependabot for automated action version tracking so SHA pins can be updated via reviewed PRs. Configure the organization's Actions policy to restrict which actions are permitted.

---

### V-05: Poisoned Skeleton-Generation Dependency

**Technique:** T1195.002 Supply Chain Compromise — Software Supply Chain

**Prerequisites:**
Compromise of a Python package, shell tool, or other dependency invoked by the CI skeleton-generation script. Viable paths: typosquatting a package name with a character transposition, dependency confusion (publishing a higher-versioned package to PyPI that shadows an internal name), or maintainer account compromise of an existing package. Requires no access to `geekatron/jerry` itself.

**What the attacker achieves:**
The malicious package executes during skeleton generation with file-system write access to the CI runner workspace. It can insert content into generated SKILL.md or agent .md files before the push step, modify `marketplace.json` or `plugin.json` to declare attacker-controlled MCP connector URLs, or exfiltrate the push credential via an outbound HTTP request. The repository's branch protection and code review are not triggered because the compromise occurs entirely within the CI runner execution.

**Feasibility x Impact:**
- Feasibility: LOW-MEDIUM — requires a successful supply chain attack on a Python dependency, which is harder than V-04 but is a documented attack class (PEP 508 dependency confusion, typosquatting campaigns)
- Impact: HIGH if the dependency has workspace write access; MEDIUM if sandboxed with restricted file access
- Rating: **MEDIUM-HIGH (5/9)**

**Blocking control:**
Pin all Python dependencies to exact content hashes in `uv.lock` and use `uv sync --frozen` in CI to enforce the lock file. Run the generation script in a minimal container with outbound network restricted to the GitHub API and verified PyPI allowlist. Enable GitHub's dependency review gate on PRs that modify `pyproject.toml` or `uv.lock`.

---

### V-06: Push Credential Theft or Misuse

**Technique:** T1552.001 Unsecured Credentials — Credentials in Files; T1078.004 Valid Accounts — Cloud Accounts

**Prerequisites:**
The CI job requires a credential (PAT or deploy key) to push to `geekatron/jerry-claude-plugin`. Exfiltration paths: debug logging that accidentally echoes the credential, successful V-02 or V-04 execution that exfiltrates secrets, over-scoped PAT used in other automation contexts that are separately compromised, or a developer who creates the PAT storing it insecurely outside GitHub's secrets store.

**What the attacker achieves:**
With the push credential, the attacker bypasses the entire CI regeneration pipeline and pushes arbitrary content directly to `geekatron/jerry-claude-plugin`'s default branch. No CI trigger, no regeneration job, no file-count validation, and no audit trail in the main repo's CI logs. The attacker pushes content that CoWork org users load on next plugin refresh. If the PAT is over-scoped (e.g., `repo` scope instead of contents-only on the dedicated repo), the attacker also gains read access to any private content the token can reach.

**Feasibility x Impact:**
- Feasibility: MEDIUM — GitHub secrets are reasonably protected in normal operation, but V-02 and V-04 are known exfiltration paths; PAT over-scoping is common; the credential must be treated as a high-value target
- Impact: HIGH — complete bypass of all upstream controls; dedicated repo fully under attacker control
- Rating: **HIGH (6/9)**

**Blocking control:**
Use a fine-grained PAT scoped exclusively to `geekatron/jerry-claude-plugin`, with only `Contents: Write` permission and no access to the main repo or any other resource. Apply branch protection to the dedicated repo's default branch requiring a PR with at least one approval — enforced even for the CI bot account — so that the credential alone cannot push directly. Rotate the credential on a quarterly schedule and alert on any use outside the expected CI job context (GitHub's secret scanning and audit log).

---

### V-07: Dedicated Repo Direct Tampering

**Technique:** T1505 Server Software Component; T1078 Valid Accounts

**Prerequisites:**
Direct write access to `geekatron/jerry-claude-plugin` outside the CI push flow. This could arise from: additional collaborators added to the dedicated repo beyond the CI bot account, an organization owner with inherited write access, a GitHub admin using bypass permissions on a branch protection rule, or the dedicated repo being inadvertently set to public write (unlikely but possible via settings drift).

**What the attacker achieves:**
Modifies the default branch of the dedicated repo directly, without triggering any CI on the main repo. Changes to SKILL.md, agent .md files, `plugin.json`, or `marketplace.json` take effect silently. CoWork loads from the dedicated repo's default branch; tampered content reaches org users on next plugin refresh with no alert generated in `geekatron/jerry` CI logs or PR history.

**Feasibility x Impact:**
- Feasibility: LOW — the dedicated repo is a narrow surface; if it is configured correctly, write access is minimal
- Impact: HIGH — direct, unaudited modification of what CoWork users execute
- Rating: **MEDIUM (4/9)**

**Blocking control:**
Lock the dedicated repo to exactly one writer: the CI bot account (a machine GitHub identity, not a human account). Enable branch protection on the default branch requiring PR + approval for all pushes, with no bypass for admins. Audit the collaborator list and any inherited organization membership monthly. Prefer a GitHub App over a PAT for the CI bot identity, so the credential is tied to the app and its usage is fully auditable in the org audit log.

---

### V-08: Org-Registration Spoofing and Typosquatting

**Technique:** T1608.001 Stage Capabilities — Upload Malware; T1566 Phishing (social engineering of admin)

**Prerequisites:**
Creation of a lookalike repository (e.g., `geekatron/jerry-c0work` with a zero instead of an "o", `geekatron-jerry/cowork` under a different org, or a public fork presented as the official distribution). Requires social engineering of an org admin into registering the wrong URL, OR relies on a weakness in Anthropic's server-side marketplace registration that does not validate GitHub org ownership or canonical URL.

**What the attacker achieves:**
If an org admin registers the spoofed repository as the org marketplace, all CoWork org users install and execute the attacker's plugin. Because CoWork marketplace registration is server-side and admin-managed (no per-user add path exists in the confirmed model), a single successful org-level registration poisons the entire org simultaneously. The attacker controls the content of the registered repo's default branch and can update it at will after registration. Users see the plugin listed under "Your organization" with no visible URL distinction.

**Feasibility x Impact:**
- Feasibility: LOW — requires social engineering a technical org admin who has a verified URL to compare against, OR a registration process flaw at Anthropic (lower probability); the confirmed model's org-admin gating actually reduces feasibility by requiring a human decision point
- Impact: HIGH if successful — all org CoWork users are affected in a single registration event
- Rating: **MEDIUM (3/9)**

**Blocking control:**
Publish and maintain a canonical, publicly verifiable URL for the official dedicated repo (e.g., pinned in the Jerry README, in the org's GitHub profile, and in any user-facing documentation). Require an out-of-band verification step for org admins: confirm the repo URL matches the documented canonical, verify the GitHub organization name matches `geekatron`, and check that the repo is owned by the same org GitHub account as `geekatron/jerry`. Pursue Anthropic directory listing for the official marketplace entry to eliminate URL-based distribution for end users.

---

## Attack Path Prioritization

### Risk Summary Table

| ID | Vector | Feasibility | Impact | F×I Score | Rating |
|----|--------|-------------|--------|-----------|--------|
| V-02 | CI PR expression injection / `pull_request_target` | HIGH | HIGH | 9 | CRITICAL |
| V-04 | Compromised GitHub Action | MEDIUM | HIGH | 6 | HIGH |
| V-01 | Compromised contributor (write to main) | MEDIUM | HIGH | 6 | HIGH |
| V-06 | Push credential theft | MEDIUM | HIGH | 6 | HIGH |
| V-03 | Malicious v* tag rebuild | MEDIUM | HIGH | 6 | HIGH |
| V-05 | Poisoned generation dependency | LOW-MEDIUM | HIGH | 5 | MEDIUM-HIGH |
| V-07 | Dedicated repo direct tampering | LOW | HIGH | 4 | MEDIUM |
| V-08 | Org-registration spoofing | LOW | HIGH | 3 | MEDIUM |

### Top Three Attack Paths

**Rank 1 — V-02 (PR Expression Injection): CRITICAL**
Exploitable by any GitHub user with zero prior repo access. If the CI regeneration workflow uses `pull_request_target` or interpolates PR metadata in `run:` steps, the attacker opens a crafted PR and gains full CI runner access including the push credential. No prerequisites beyond a GitHub account. The highest-feasibility path in the entire chain.

**Rank 2 — V-04 (Compromised GitHub Action): HIGH**
Real-world supply chain attacks (tj-actions, reviewdog) demonstrate this vector's viability at scale. Mutable tag references (e.g., `actions/checkout@v4`) are the norm rather than the exception. A single compromised action grants full CI runner access with secrets. Feasibility is MEDIUM only because it requires compromising a third-party maintainer rather than exploiting a configuration flaw.

**Rank 3 — V-01 (Compromised Contributor): HIGH**
The most direct path: credentials for a single collaborator with push access lead to unrestricted modification of `main`, which flows through CI to all CoWork users. Credential theft (phishing, credential stuffing, session token theft) is a commodity attack class. Branch protection without mandatory reviews does not prevent this vector.

---

## Highest-Leverage Control

**Secure CI workflow configuration — closing the top two vectors with a single engineering decision:**

1. **Use `pull_request` not `pull_request_target` as the PR trigger.** Fork pull requests cannot access repository secrets when using the `pull_request` event. This eliminates V-02(a) entirely.

2. **Never interpolate untrusted PR metadata in `run:` steps.** Replace inline expression interpolation (`${{ github.event.pull_request.title }}`) with environment variable indirection. This eliminates V-02(b).

3. **Pin all GitHub Actions to immutable commit SHAs.** Replace `actions/checkout@v4` with `actions/checkout@<sha>`. This removes the mutable reference that V-04 exploits.

These three practices share a single conceptual root: treating the CI runner environment as a trust boundary that must be defended against untrusted inputs (PRs, action tags). Together they close the two highest-feasibility vectors (V-02 and V-04) and force all remaining high-impact paths through V-01 (contributor credential compromise), which is then blocked by branch protection on `main`.

Secondary control with high leverage: **Branch protection on `main` + fine-grained PAT for the push credential.** This closes V-01 (requires reviewed PR to merge to main) and reduces V-06 impact (credential scoped to one repo, one operation).

---

## Threat Intelligence for eng-architect

> Integration Point 1 — Threat-Informed Architecture input for Phase 2 threat modeling.

### ATT&CK Technique Mapping

| Vector | Technique ID | Technique Name |
|--------|-------------|----------------|
| V-01 | T1078.003 | Valid Accounts: Local Accounts (contributor credential) |
| V-01 | T1195.002 | Supply Chain Compromise: Software Supply Chain |
| V-02 | T1059.004 | Command and Scripting Interpreter: Unix Shell (expression injection) |
| V-02 | T1552.001 | Unsecured Credentials: Credentials in Files (PAT exfil from CI) |
| V-03 | T1195.002 | Supply Chain Compromise: Software Supply Chain (via tag event) |
| V-04 | T1195.001 | Supply Chain Compromise: Development Tools (GitHub Action) |
| V-05 | T1195.002 | Supply Chain Compromise: Software Supply Chain (package) |
| V-06 | T1552.001 | Unsecured Credentials: Credentials in Files |
| V-06 | T1078.004 | Valid Accounts: Cloud Accounts (GitHub PAT misuse) |
| V-07 | T1505 | Server Software Component (direct repo modification) |
| V-08 | T1608.001 | Stage Capabilities: Upload Malware (lookalike repo) |
| V-08 | T1566 | Phishing (admin social engineering) |

All vectors ultimately deliver payload via **TA0040 Impact** in the CoWork user context — specifically T1565.001 (Stored Data Manipulation, modification of skill/agent markdown) rather than traditional code execution.

### STRIDE Threat Summary

| STRIDE Category | Applicable Vectors | Design Implication |
|-----------------|-------------------|-------------------|
| Spoofing | V-01, V-06, V-08 | Verified identity required at every trust boundary (TB-1 through TB-4) |
| Tampering | V-01, V-02, V-03, V-04, V-05, V-07 | Integrity verification (signing or hash pinning) needed on every artifact in the chain |
| Repudiation | V-06, V-07 | Audit log coverage needed on dedicated repo pushes; CI job provenance (SLSA level) |
| Information Disclosure | V-02, V-04, V-06 | Push credential must not be accessible to untrusted workflow contexts |
| Denial of Service | V-03, V-07 | Malformed push (exceeding file count, corrupt plugin.json) could block CoWork plugin load |
| Elevation of Privilege | V-02 | Zero-access GitHub user gains CI secrets; highest-priority fix |

### Architecture Recommendations for eng-architect

1. **SLSA Level 2 minimum** for the skeleton build: provenance attestation on the generated artifact (buildType: GitHub Actions) so CoWork org admins can verify the skeleton was built by the expected workflow from the expected source.

2. **Dedicated repo is write-once-except-CI**: enforce via branch protection requiring a PR even for the bot account. The dedicated repo should be considered a delivery artifact, not a collaboration surface.

3. **Secret rotation and scoping**: the push credential is the single most-valuable secret in the chain. Fine-grained PAT, quarterly rotation, and alert on any use outside the expected workflow `run_id` window.

4. **Canonical URL documentation**: publish the authoritative `geekatron/jerry-claude-plugin` URL in at least two independently verifiable locations before any org registration occurs. Reduces V-08 social engineering risk.

5. **Prompt injection audit gate**: before any skeleton push, CI should run a static check on all markdown files for patterns that could constitute prompt injection (unusual role-reversal instructions, `<|im_start|>` tokens, injected system-prompt delimiters). This is the payload delivery mechanism unique to this supply chain.

---

*Produced by: red-recon (Reconnaissance Specialist, /red-team skill)*
*Methodology: PTES Intelligence Gathering; OSSTMM Section V; ATT&CK TA0043 / T1195*
*Engagement: PROJ-031-cowork-skeleton, Phase 2 threat modeling*
*Date: 2026-06-28*
*Output level: L1 (Technical Detail) + L2 (Strategic Implications)*
*Output path: projects/PROJ-031-cowork-skeleton/security/phase2-attack-surface.md*
