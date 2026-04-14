# About the Jerry Framework CI/CD Supply Chain Security Model

> Understanding why the CI/CD pipeline is hardened the way it is -- the threat model, the trade-offs, and the defense-in-depth reasoning behind SHA pinning, lockfile freezing, and workflow loop prevention.

> **Scope:** This document explains the security rationale behind the Jerry Framework's CI/CD supply chain controls. It does not cover how to update a pinned action SHA, how to configure Dependabot, or the exact syntax of each workflow file. For those details, see the companion reference at `docs/reference/ci-cd-pipeline-security.md`.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Why CI/CD pipelines are worth defending |
| [The Supply Chain as an Attack Surface](#the-supply-chain-as-an-attack-surface) | Threat model and real-world attack vectors |
| [The Mutability Problem with Git Tags](#the-mutability-problem-with-git-tags) | Why SHA pinning over tag pinning |
| [The Lockfile as a Security Boundary](#the-lockfile-as-a-security-boundary) | Why --frozen matters for reproducibility and integrity |
| [The Infinite Loop Problem](#the-infinite-loop-problem) | Why the skip-bump guard exists and why identity matters |
| [Defense in Depth](#defense-in-depth) | How the controls layer together |
| [The BUG-003 Story](#the-bug-003-story) | How debugging one failure exposed systemic infrastructure debt |
| [Connections](#connections) | How this topic relates to other parts of the Jerry Framework |
| [Alternative Perspectives](#alternative-perspectives) | Trade-offs and other valid approaches |
| [Related](#related) | Companion documentation in other Diataxis quadrants |

---

## Context

A CI/CD pipeline is trusted infrastructure. It runs with elevated permissions -- pushing to protected branches, creating releases, uploading artifacts, accessing secrets. When developers think about security, they tend to focus on the code they write: input validation, authentication, authorization. The pipeline that builds and deploys that code receives far less scrutiny, despite the fact that a compromise at the build layer can inject malicious code into every artifact the pipeline produces.

The Jerry Framework's CI/CD security posture was not designed proactively from day one. It emerged from a specific incident -- BUG-003, a version-bump workflow failure caused by a dirty lockfile -- that, once investigated, revealed a series of supply chain gaps spanning five workflow files. The controls documented here are the product of that investigation: a DevSecOps security review, a red-team attack surface analysis, and the subsequent EN-001 hardening enabler. Understanding this origin matters because it explains why these controls exist as a coherent system rather than as isolated configuration choices.

---

## The Supply Chain as an Attack Surface

Software supply chain attacks exploit the trust relationships between a project and the external code it depends on. A CI/CD pipeline has three distinct trust boundaries, each with its own attack vectors.

The first boundary is **action code** -- the GitHub Actions that perform checkout, setup, upload, and release tasks. Every `uses:` line in a workflow file pulls code from an external repository and executes it inside the CI runner. That external code runs with whatever permissions the workflow grants: `contents: write`, access to secrets like `VERSION_BUMP_PAT`, and the ability to push directly to protected branches. If an attacker can change what code a `uses:` line resolves to, they gain code execution inside the pipeline.

The second boundary is **tool binaries** -- the executables the pipeline downloads and runs. When a workflow installs `uv`, `bump-my-version`, `ruff`, or `pyright`, it is downloading binaries or packages from external registries (GitHub releases, PyPI) and executing them. A compromised `uv` binary, for example, could exfiltrate the `VERSION_BUMP_PAT` secret during what appears to be a routine `uv sync` call. A compromised `pip-audit` could suppress vulnerability findings -- the security scanning tool itself becoming the vulnerability.

The third boundary is **dependency resolution** -- the transitive closure of Python packages that `uv sync` or `pip install` resolves. Dependency confusion attacks, typosquatting, and re-upload attacks all target this boundary. A package name that looks correct (`reuqests` instead of `requests`) or a legitimate-looking version that has been re-uploaded with malicious content can silently enter the dependency graph during resolution.

These three boundaries are independent. Hardening one does not protect the others. A SHA-pinned GitHub Action still downloads an unpinned `uv` binary if the action's `version` input is set to `"latest"`. A locked dependency graph still executes inside an action whose code has been silently replaced via a tag force-push. This independence is why defense in depth -- layering controls across all three boundaries -- is the governing design principle for the Jerry pipeline.

---

## The Mutability Problem with Git Tags

Git tags are mutable references. A repository maintainer (or an attacker with push access) can delete a tag and recreate it pointing to a different commit. When a workflow file references an action by tag -- `uses: actions/checkout@v5` -- the tag `v5` resolves to whatever commit it happens to point to at the moment the runner fetches it. If that tag is force-pushed between one CI run and the next, the pipeline silently executes different code.

This is not a theoretical risk. The `codecov/codecov-action` incident of 2021 demonstrated the attack in practice: a compromised bash uploader was served through the action's tag reference, affecting thousands of CI pipelines that trusted the tag to point to reviewed code.

SHA references eliminate this class of attack entirely. A commit SHA is a content-addressed hash -- it resolves to exactly one commit, and that resolution is cryptographically immutable. Writing `uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8` means the pipeline will always fetch that exact commit. If the commit is deleted from the upstream repository, the workflow fails rather than silently executing different code. The failure mode is loud and debuggable; the tag-based failure mode is silent and undetectable.

The trade-off is readability and maintenance burden. A 40-character hex string conveys no version information to a human reader. The Jerry convention addresses this with inline comments -- `# v5.0.0` -- that preserve human readability without affecting the runtime reference. The maintenance burden -- tracking when new versions of pinned actions become available -- is handled by Dependabot, which monitors the `github-actions` ecosystem weekly and opens pull requests that update both the SHA and the version comment. This division of labor is deliberate: the pipeline gets cryptographic immutability; Dependabot absorbs the manual tracking cost.

There is a subtlety here that is easy to miss. SHA-pinning the `astral-sh/setup-uv` action protects the action's code, but the action itself downloads a `uv` binary whose version is specified by a separate `version` input. When that input was `"latest"`, the action was immutable but the binary it installed was not. The Jerry pipeline pins `uv` to `"0.10.9"` precisely because this second-order trust boundary exists. The EN-001 security review identified this gap as HIGH severity because the `uv` binary runs in the version-bump job alongside the `VERSION_BUMP_PAT` secret -- a malicious binary at that execution point could exfiltrate the most privileged credential in the repository.

---

## The Lockfile as a Security Boundary

A lockfile is a snapshot of a resolved dependency graph. It records not just which packages are required, but which specific versions were selected and (in the case of `uv.lock`) their content hashes. When the resolver runs without a lockfile constraint, it performs full resolution: evaluating version bounds, platform markers, and the current Python interpreter to select a compatible set of packages. The result depends on the state of the package registry at the moment of resolution.

The `--frozen` flag changes this behavior fundamentally. `uv sync --frozen` reads the existing lockfile verbatim and installs exactly what it describes. It does not contact PyPI. It does not evaluate version bounds against the current interpreter. If the lockfile is inconsistent with `pyproject.toml` -- because a dependency was added or a bound was changed -- `--frozen` fails with an error rather than silently updating the lockfile. The failure is the point: it forces the developer to regenerate the lockfile locally, commit it, and have it reviewed, rather than allowing CI to silently resolve to whatever packages happen to be available at build time.

This matters for security because a lockfile that mutates during CI is a lockfile that the CI runner -- not a human -- decided to trust. If a compromised package version is published to PyPI between the time a developer commits their code and the time CI runs, bare `uv sync` will happily resolve to that compromised version. `uv sync --frozen` will not, because the compromised version is not in the committed lockfile.

It also matters for reproducibility. The version-bump workflow uses `bump-my-version` with `allow_dirty = false`, which refuses to create a version-bump commit if the working directory contains uncommitted changes. When bare `uv sync` re-resolves dependencies against the CI runner's Python 3.14 interpreter -- which may differ from the developer's local Python version -- it updates platform markers and dependency bounds in `uv.lock`, making the working tree dirty. The version bump then fails. This is exactly what BUG-003 was: not a security incident, but a reproducibility failure whose root cause -- mutable dependency resolution in CI -- is the same mechanism that supply chain attacks exploit.

The `--frozen` flag closes both risks with a single control. The lockfile becomes a security boundary: it defines the exact dependency graph that the pipeline is authorized to install, and any deviation from that graph is an error, not a silent update.

---

## The Infinite Loop Problem

The version-bump workflow runs on every push to `main`. It detects the conventional commit type (feat, fix, etc.), determines the appropriate version bump (major, minor, patch), applies the bump, commits the change, and pushes the commit back to `main`. That push to `main` triggers the workflow again.

Without a guard, this creates an infinite loop: the bot pushes a version-bump commit, which triggers the workflow, which pushes another version-bump commit, which triggers the workflow, and so on until GitHub's concurrency limit or a human intervenes.

The guard has two components, and the distinction between them matters.

The first component is the `[skip-bump]` marker in the commit message. When `bump-my-version` creates its commit, the message contains `[skip-bump]`, and the workflow's `if` condition checks for this string. If present, the job does not run. This is straightforward and effective for push-triggered events. The EN-001 hardening extended this check to `workflow_dispatch` events as well, because a manual dispatch could otherwise double-bump a commit that already carried the marker.

The second component is the `github.actor` check, and this is where the security reasoning becomes more nuanced. Before BUG-003, the skip-bump guard checked `github.event.head_commit.author.name` -- the Git author name configured in the commit metadata. The problem is that `git config user.name` is a client-side setting. Any developer with push access could set their local Git configuration to `user.name "github-actions[bot]"` and push a commit that the workflow would treat as a bot commit, suppressing the version bump. This is a commit-message-level spoofing vector.

`github.actor`, by contrast, is the authenticated identity set by GitHub based on the token used to push the commit. It cannot be set by the committer. When the version-bump workflow pushes its commit using the `VERSION_BUMP_PAT`, GitHub records the push actor as `github-actions[bot]`. This value is set by the platform, not by `git config`, and cannot be forged by a collaborator. The guard now checks `github.actor != 'github-actions[bot]'`, which is a platform-authenticated identity assertion rather than a self-declared claim.

There is also an input validation concern. The `workflow_dispatch` trigger accepts a `prerelease` string input (e.g., "alpha", "beta", "rc"). Because this is a free-form string that eventually reaches a shell command, it is validated as alphanumeric-only before use. Without this validation, a carefully crafted prerelease label could inject shell commands via the `$PRERELEASE` variable interpolation. The alphanumeric regex (`^[a-zA-Z0-9]+$`) eliminates this vector.

---

## Defense in Depth

No single control protects against all supply chain attack vectors. The Jerry pipeline's security posture is the product of four controls that address different boundaries, and the value of the model lies in how they complement each other.

**SHA pinning** protects the action code boundary. It ensures that the GitHub Actions executed by the pipeline are the exact code that was reviewed when the SHA was committed. It does not protect against compromised tool binaries or dependencies -- those are separate trust boundaries.

**Binary version pinning** protects the tool integrity boundary. Pinning `uv` to `"0.10.9"` and `bump-my-version` to `"1.2.7"` ensures that the tools themselves are version-specific. This is weaker than SHA pinning (it relies on PyPI serving the same content for the same version number) but significantly stronger than `"latest"`, which delegates version selection to the upstream registry at runtime.

**Lockfile freezing** protects the dependency integrity boundary. `uv sync --frozen` ensures that the transitive dependency graph installed in CI is the one committed to the repository, not a runtime resolution that could incorporate compromised packages published after the commit.

**Dependabot** is the maintenance automation that makes the other controls sustainable. SHA pinning without Dependabot means pinned actions become stale and never receive security patches. Binary pinning without Dependabot means tool versions drift from upstream releases. Dependabot absorbs the manual tracking cost, opening pull requests that a human reviews before merging -- keeping the human in the approval loop while automating the discovery of available updates.

Together, these four controls form a layered defense:

- A compromised GitHub Action is blocked by SHA pinning.
- A compromised tool binary is mitigated by version pinning (and the `--frozen` flag prevents a compromised `uv` from altering dependency resolution).
- A compromised PyPI package is blocked by lockfile freezing.
- Staleness and maintenance drift are addressed by Dependabot.

Each control addresses a vector that the others do not. Removing any one layer leaves a specific attack surface undefended. This is the essence of defense in depth: redundancy across independent failure modes.

---

## The BUG-003 Story

The story of how these controls came to exist is instructive because it illustrates a pattern that recurs across software projects: a single, seemingly routine bug exposes systemic infrastructure debt that was invisible until something broke.

BUG-003 was a CI failure. The version-bump workflow was failing because `uv sync` -- running without `--frozen` -- re-resolved dependencies against the GitHub Actions runner's Python 3.14 interpreter, which differed from the local development Python version. The lockfile was updated, the working tree became dirty, and `bump-my-version` (configured with `allow_dirty = false`) refused to proceed. The immediate fix was straightforward: add `--frozen` to every `uv sync` call in CI.

But the investigation did not stop at the immediate fix. A DevSecOps security review examined the entire version-bump pipeline and found five additional findings. The `astral-sh/setup-uv` action was SHA-pinned, but the `uv` binary it installed was set to `"latest"` -- partially defeating the supply chain protection. All `actions/*` references used floating tags (`@v5`, `@v4`) rather than commit SHAs. The `bump-my-version` installation used an unversioned `uv tool install` command. The skip-bump guard relied on a spoofable Git author name. The `workflow_dispatch` trigger bypassed the skip-bump check entirely.

A red-team reconnaissance analysis mapped the attack surface of the version-bump pipeline and classified it as medium-to-high: the pipeline held a Personal Access Token capable of bypassing branch protection, and the most credible attack path was a supply chain compromise of `bump-my-version` on PyPI -- which, at the time, was installed without any version pin.

None of these findings were caused by BUG-003. They predated it. But they were invisible because the pipeline was working. The dirty-lockfile failure was the first crack in the facade, and the investigation that followed revealed the structural gaps behind it. This is a common pattern in infrastructure security: the absence of failures is not evidence of the absence of vulnerabilities. It takes a visible failure to motivate the investigation that finds the invisible ones.

The EN-001 enabler that resulted from this investigation addressed all five findings in a single hardening pass. The resulting security posture -- SHA-pinned actions, version-pinned binaries, frozen lockfiles, platform-authenticated identity checks, input validation, and Dependabot automation -- is coherent because it was designed as a system, responding to a mapped threat model, rather than as individual point fixes applied in isolation.

---

## Connections

This topic connects to several other areas of the Jerry Framework:

- **H-05 (UV-only Python environment):** The CI pipeline's use of `uv sync --frozen` is the CI-side enforcement of the same principle that H-05 mandates for local development. H-05 prohibits direct `python` and `pip` invocations; the pipeline enforces this by using `uv run` for all project Python execution. As of EPIC-003, all CI jobs use `uv sync --frozen` for dependency installation and `uv run` for tool execution — there are zero `pip install` commands in the pipeline. The security job audits the full dependency tree via `uv export --all-extras --no-emit-project` piped to `pip-audit`, ensuring every direct and transitive dependency is scanned against the PyPI advisory database.

- **The version-bump pipeline's relationship to the release pipeline:** The version-bump workflow creates a commit and a tag. The tag push triggers the release workflow. This is a two-stage chain where the security of the release depends on the integrity of the version bump. A compromised version-bump commit could inject malicious content that the release workflow then packages and publishes. This is why the version-bump job has the most stringent security controls -- it is the pipeline's highest-privilege execution context.

- **Dependabot's role in the maintenance lifecycle:** Dependabot is not a security tool in the traditional sense. It is a maintenance automation tool that makes security controls sustainable. The relationship is analogous to the role of testing in code quality: tests do not write correct code, but they make it sustainable to maintain correct code over time. Dependabot does not secure the pipeline, but it makes it sustainable to keep the pipeline secured.

---

## Alternative Perspectives

The approach described here is not the only valid one, and it carries real trade-offs.

SHA pinning adds visual noise to workflow files. A line like `uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8` is harder to read than `uses: actions/checkout@v5`. For projects with fewer security concerns -- small personal projects, internal tools with no external exposure -- tag-based references may be entirely appropriate. The Jerry Framework chose SHA pinning because its pipeline holds a PAT with branch-protection bypass privileges, which raises the stakes of a compromise. Not every project has this risk profile.

An alternative to `uv sync --frozen` is to generate the lockfile in CI and validate it against the committed version. This approach detects drift without preventing resolution, which can be useful when the development team works across multiple Python versions and wants CI to surface lockfile inconsistencies. The Jerry team chose `--frozen` because the priority was preventing mutable resolution in CI, not detecting it -- but the alternative is reasonable for teams with different priorities.

The `bump-my-version` installation via `uv tool install` with a version pin but without hash verification is an acknowledged gap. The EN-001 security review flagged it as MEDIUM severity. The trade-off is isolation: `uv tool install` keeps `bump-my-version` out of the project's virtual environment, which avoids dependency conflicts. Adding it to `pyproject.toml` and `uv.lock` would provide hash verification but would mix a CI-only tool into the project's dependency graph. The current approach accepts the residual risk of PyPI index integrity for the benefit of environment isolation.

There is also a broader question about how much security investment is appropriate for a given project. The Jerry Framework is an open-source Claude Code plugin with a small team. Its threat model is not equivalent to a financial services platform or a package registry. However, the pipeline holds secrets (`VERSION_BUMP_PAT`) and publishes artifacts (release archives) that other teams consume. The security posture is calibrated to that specific risk profile -- not maximal, but proportionate to the trust boundaries the pipeline crosses.

---

## Related

- **Reference:** [CI/CD Pipeline Security Controls](../reference/ci-cd-pipeline-security.md) -- Exact configurations, SHA-to-version mappings, and per-workflow control inventory
- **Work Item:** EN-001: CI Pipeline Hardening (`projects/PROJ-030-bugs/work/EN-001-ci-pipeline-hardening.md`) -- The enabler that drove this work
- **Work Item:** BUG-003: Version Bump uv.lock Dirty (`projects/PROJ-030-bugs/work/BUG-003-version-bump-uv-lock-dirty.md`) -- The bug that started the investigation
- **Security Review:** EN-001 DevSecOps Security Review (`projects/PROJ-030-bugs/reviews/en-001-devsecops-security-review.md`) -- Full security assessment with per-file findings
- **Attack Surface Analysis:** BUG-003 Red-Recon Attack Surface (`projects/PROJ-030-bugs/reviews/bug-003-red-recon-attack-surface.md`) -- Red-team reconnaissance of the version-bump pipeline
