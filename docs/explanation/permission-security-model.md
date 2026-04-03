# About Jerry's Permission and Security Model

> Jerry enforces security through a three-layer model where Claude Code settings provide coarse access control, a hook-based SecurityEnforcementEngine provides deterministic command blocking, and a PreToolEnforcementEngine provides architecture boundary validation. The blanket `Bash` permission in `settings.json` is an intentional design decision, not an oversight.

> **Scope:** This document explains why Jerry grants blanket Bash permission and how the hook-based enforcement pipeline compensates. It does not cover the architecture validation rules themselves (H-07, H-10), the staleness detection system, or the prompt reinforcement engine -- those are related but separate enforcement concerns.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (E-01 through E-07) -->
<!-- Anti-patterns to avoid: EAP-01 (instructional creep), EAP-05 (unbounded scope) -->
<!-- Voice: Thoughtful, discursive, contextual. No imperative instructions. See Section 5. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Why this design decision matters and what problem it solves |
| [The Three Layers and Their Responsibilities](#the-three-layers-and-their-responsibilities) | How settings, security hooks, and architecture hooks divide enforcement |
| [Why Blanket Bash Permission is Intentional](#why-blanket-bash-permission-is-intentional) | The design rationale behind granting unrestricted Bash access at the settings layer |
| [The Fail-Open Philosophy](#the-fail-open-philosophy) | Why enforcement errors result in approval rather than blocking |
| [Permission Inheritance and the Skill Gap](#permission-inheritance-and-the-skill-gap) | How permissions propagate to subagents and skills, and where they break down |
| [The Skill Permission Namespace](#the-skill-permission-namespace) | How `Skill()` entries work and why the fully-qualified form matters |
| [The Anti-Pattern: Per-Command Bash Patterns in Settings](#the-anti-pattern-per-command-bash-patterns-in-settings) | Why adding fine-grained Bash permissions to settings.json makes security worse |
| [Connections](#connections) | How this topic relates to other Jerry systems |
| [Alternative Perspectives](#alternative-perspectives) | Acknowledging the case for settings-level restrictions |
| [Related](#related) | Links to reference, investigation, and implementation files |

---

## Context

A future developer -- or a future Claude Code session -- looking at Jerry's `.claude/settings.json` and seeing `"Bash"` in the allow list might reasonably conclude this is a security gap. The instinct to replace it with a curated list of `Bash(git *)`, `Bash(uv *)`, `Bash(cat *)` patterns feels like an obvious improvement. It is not. It would actively degrade both security coverage and operational reliability.

This explanation exists because the permission model's design rationale is non-obvious. The safety of blanket Bash permission depends on understanding what happens *after* Claude Code grants access -- specifically, the hook-based enforcement pipeline that evaluates every Bash invocation before it executes. Without that context, the settings file looks negligent. With it, the settings file looks like what it is: the coarsest layer in a defense-in-depth architecture where the real security work happens elsewhere.

The decision to use blanket Bash permission was not made at the start of the project. It emerged from the consolidation of `scripts/pre_tool_use.py` into the structured enforcement engine (issue #150, ADR-150-001). Before that consolidation, the pre-tool-use logic was a standalone Python script with inline rule definitions. The move to an injectable, testable engine architecture made it possible to provide stronger security guarantees than settings patterns ever could -- and made the settings-level patterns redundant.

---

## The Three Layers and Their Responsibilities

Jerry's security enforcement operates across three distinct layers, each with a different scope, mechanism, and failure mode. Understanding why each layer exists -- and what it is *not* responsible for -- is essential to understanding why the overall model works.

**Layer 1: Claude Code Settings** (`settings.json` and `settings.local.json`) provides coarse-grained tool access control. The `permissions.allow`, `permissions.deny`, and `permissions.ask` arrays determine whether Claude Code will permit, block, or prompt for approval before invoking a tool. This layer operates at the tool-name level: it knows that a Bash command is being requested, but it evaluates command content only through pattern matching against the permission string. The evaluation order is `deny > ask > allow`, and deny is absolute -- no allow entry at any scope overrides a denial. Jerry's committed `settings.json` allows `Bash` without qualification, meaning all shell commands pass this layer without prompting.

**Layer 2: SecurityEnforcementEngine** (`src/infrastructure/internal/enforcement/security_enforcement_engine.py`) provides deterministic, pattern-based command blocking through the `PreToolUse` hook. Every time Claude Code attempts to invoke a Write, Edit, MultiEdit, NotebookEdit, or Bash tool, the hook fires and the security engine evaluates the request against a codified rule set. For Bash commands, this includes blocking destructive `rm` patterns (recursive force-delete targeting `/` or `~`), download-then-execute chains (`curl` piped to `bash`), `eval` invocations, disk formatting commands (`mkfs`, `dd`), force pushes to protected branches (`main`, `master`), null byte injection attempts, and `cd` commands that would corrupt the working directory. For file writes, it blocks writes to system paths (`/etc`, `/usr`, `~/.ssh`, `~/.aws`), credential files (`.env`, `.pem`, `.key`, `id_rsa`), and paths containing null bytes. The rule definitions live in `SecurityRules` as frozen dataclass tuples -- immutable at runtime, injectable for testing.

**Layer 3: PreToolEnforcementEngine** (`src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py`) provides AST-based architecture boundary validation. This layer parses Python source code and enforces structural rules: import boundary violations (H-07, domain cannot import from infrastructure), one-class-per-file (H-10), and governance file modification escalation (auto-C3 or auto-C4 for changes to constitution or rules files). This layer operates on the *content* of file writes and edits, not on shell commands.

All three layers are invoked through a single handler (`HooksPreToolUseHandler`) that processes the `PreToolUse` hook event. The security engine runs first because its checks are cheap (string matching and regex), and a security block terminates evaluation immediately. The architecture engine runs second, performing the more expensive AST parsing only if the security check passed. The staleness detector runs third, adding warnings about stale orchestration state.

The key insight is that these layers are not redundant -- they operate on different dimensions of the same request. Layer 1 decides *whether a tool type is accessible*. Layer 2 decides *whether a specific command is dangerous*. Layer 3 decides *whether the content being written is architecturally valid*.

---

## Why Blanket Bash Permission is Intentional

The decision to allow all Bash commands at the settings layer rests on three observations about how Claude Code's permission system interacts with hook-based enforcement.

The first observation is that **per-command Bash patterns in settings are redundant with the SecurityEnforcementEngine**. Consider the alternative: instead of `"Bash"` in the allow list, one might write `Bash(git *)`, `Bash(uv *)`, `Bash(cat *)`, `Bash(ls *)`, `Bash(find *)`, and so on. Each pattern would need to anticipate every legitimate command Claude Code might need to execute. The SecurityEnforcementEngine already does the inverse -- it blocks the small, well-defined set of *dangerous* commands rather than trying to enumerate the large, open-ended set of *safe* ones. The deny-list approach is more robust because dangerous commands are a finite, knowable set, while legitimate commands are effectively unbounded. An allowlist at the settings level would inevitably miss a legitimate command, creating a failure that is invisible during normal operation and catastrophic during background execution.

The second observation is that **the SecurityEnforcementEngine has a test suite; settings patterns have none**. The security engine's test file (`tests/unit/enforcement/test_security_enforcement_engine.py`) contains 29 test functions with extensive parametrized expansion covering blocked paths, dangerous commands, bypass vectors, force push protection, null byte injection, and download-execute detection. Each rule's behavior is verified against specific inputs. Settings-level patterns, by contrast, are untestable strings -- there is no mechanism to write a test that verifies `Bash(git *)` correctly blocks `git push --force origin main` while allowing `git push origin feature/xyz`. The enforcement engine can verify this distinction; the settings pattern cannot.

The third observation is that **background agents and subagents cannot prompt interactively**. When a command matches `ask` rather than `allow`, Claude Code pauses and waits for the user to approve or deny. This works in an interactive session. In a background agent or a skill invoked via the Task tool, there is no user to prompt. An unlisted command does not gracefully degrade to a prompt -- it fails. Adding per-command patterns to the allow list means that any command not explicitly listed will hard-fail in non-interactive contexts. Blanket Bash permission avoids this failure mode entirely, delegating security to the hook layer that executes deterministically regardless of the interaction context.

---

## The Fail-Open Philosophy

Both enforcement engines -- security and architecture -- are fail-open by design. When an internal error occurs during evaluation (a regex compilation failure, an unexpected input type, an AST parse error), the engine returns an approval decision rather than a block. This is a deliberate engineering trade-off, not a safety oversight.

The reasoning is that the enforcement layer should never become a reliability risk to the development workflow. A security engine bug that blocks all Bash commands would be more disruptive than the threats it prevents. The fail-open design bounds the blast radius of enforcement bugs: the worst case is that a dangerous command passes through (equivalent to not having the enforcement layer at all), not that all commands are blocked (equivalent to a denial-of-service on the developer).

This works because the enforcement engine is a *defense-in-depth* layer, not the *sole* security mechanism. Claude Code itself imposes constraints through its training, system prompt, and tool-use policies. The SecurityEnforcementEngine adds a deterministic check on top of those probabilistic constraints. If the deterministic check fails open, the probabilistic constraints still apply. If the deterministic check succeeds, it catches patterns that probabilistic constraints might miss -- like subtle variations on destructive commands that an LLM might not recognize as dangerous.

The implementation makes this explicit. The top-level `evaluate` method wraps `_evaluate_internal` in a bare `except Exception` that returns `_APPROVE`. Pattern library errors are similarly caught and swallowed. The non-string type guard for `file_path` and `command` inputs returns approval rather than raising. Every failure path converges on the same outcome: approval.

However, only *internal errors* trigger fail-open behavior. A command that *deterministically matches* a dangerous pattern -- `rm -rf /`, `curl | bash`, `eval` -- is always blocked. The fail-open boundary is between "the engine encountered an unexpected condition" and "the engine successfully evaluated the input and found a violation." The former approves; the latter blocks.

---

## Permission Inheritance and the Skill Gap

Claude Code's permission model has an inheritance asymmetry that directly shapes Jerry's security architecture. Subagents -- agents invoked via the Task tool -- inherit the parent conversation's permission context. A subagent in a session where `Bash` is allowed can execute Bash commands without additional prompting. This inheritance is documented by Anthropic and works as expected.

Skills, however, have a separate permission mechanism that does not reliably inherit parent permissions. GitHub issue #18950 reports that Bash permissions granted in the parent session do not propagate into skill execution contexts. A Bash command that executes without prompting in the main session may prompt (or fail silently in background mode) when executed from within a skill.

This asymmetry explains the `PreToolUse` hook entry in `.claude/settings.local.json` that matches `WebFetch|WebSearch` and returns a `permissionDecision: "allow"` response. This hook is defense-in-depth for the skill permission inheritance gap. Even though `WebSearch` and `WebFetch` appear in the `settings.json` allow list, the hook ensures that the permission decision propagates into skill and subagent contexts where the settings-level permission might not reach. The hook's `permissionDecisionReason` field documents this rationale explicitly.

The PreToolUse hooks defined in the plugin's `hooks.json` fire for all execution contexts -- the main session, subagents, and skills. The hook event payload includes `agent_id` and `agent_type` fields that identify the invoking context. Because hooks are executed as external processes by the Claude Code runtime itself, they are not subject to the same inheritance gaps that affect settings-level permissions. This is why the hook-based enforcement model is more reliable than the settings-level permission model for security enforcement: hooks fire universally, settings permissions may not propagate.

---

## The Skill Permission Namespace

Jerry's `.claude/settings.local.json` uses `Skill(jerry:*)` to pre-approve all skills registered under the `jerry` plugin namespace. This pattern deserves explanation because the namespace behavior is not immediately obvious from Claude Code's documentation.

Plugin skills register under a `plugin-name:skill-name` namespace to prevent naming conflicts. A skill named `adversary` in the `jerry` plugin becomes `jerry:adversary` at the plugin level. The `Skill(jerry:*)` wildcard matches all skills whose name begins with `jerry:`, covering both current and future Jerry skills without requiring individual entries.

Empirical testing (documented in the BUG-005 investigation) confirmed that both `Skill(adversary)` (short form) and `Skill(jerry:adversary)` (fully-qualified form) produce the same approval behavior. Claude Code's runtime writes the short form when auto-adding "don't ask again" entries during interactive use. The fully-qualified form, however, is the only collision-safe approach -- if another plugin also registered a skill named `adversary`, the short form would be ambiguous while the qualified form would unambiguously target the Jerry skill.

Jerry uses the fully-qualified `Skill(jerry:*)` wildcard rather than individual `Skill(adversary)`, `Skill(problem-solving)` entries because the wildcard provides forward compatibility. Adding a new skill to the Jerry plugin does not require a corresponding settings.local.json update. The trade-off is that this grants blanket skill approval -- there is no mechanism to selectively deny a specific Jerry skill while allowing others through the wildcard. For Jerry's use case, where all skills are first-party and trusted, this trade-off is appropriate.

---

## The Anti-Pattern: Per-Command Bash Patterns in Settings

The most likely well-intentioned mistake a developer or future session could make is to replace `"Bash"` in `settings.json` with a curated set of `Bash(command *)` entries. This section explains why this apparent improvement would make security worse while degrading reliability.

Adding per-command patterns creates a false sense of security. A pattern like `Bash(git *)` appears to restrict Bash to only git commands, but the SecurityEnforcementEngine already blocks the actually dangerous git operations (force push to protected branches) while allowing all safe ones. The settings pattern adds no security value over the hook -- it merely duplicates a subset of the hook's logic in an untestable format.

More importantly, adding patterns *removes* the safety net for background agents. Any command not covered by an explicit `Bash(command *)` entry will fail silently in non-interactive contexts. The failure is not obvious during development because interactive sessions degrade gracefully to a prompt. The developer adds their curated list, tests it interactively (everything seems to work because they approve any prompts), and ships it. Background agents then break on the first command that was not anticipated -- perhaps a `wc` invocation in a line-counting step, or a `head` command in a file inspection, or a `date` invocation in a timestamp generation. These failures are intermittent, context-dependent, and difficult to diagnose because they manifest as missing output rather than error messages.

The correct mental model is: settings.json controls *tool category access* (can this session use Bash at all?), while the SecurityEnforcementEngine controls *command-level safety* (is this specific command dangerous?). Mixing these concerns -- putting command-level decisions in the tool-category layer -- creates gaps in both.

---

## Connections

This topic connects to:

- **The enforcement architecture (L1-L5):** The three-layer permission model maps to layers L1 and L3 in Jerry's five-layer enforcement architecture defined in `quality-enforcement.md`. L1 (session start) loads the rules that inform the enforcement engines. L3 (pre-tool) is where both the SecurityEnforcementEngine and PreToolEnforcementEngine operate -- deterministic gating that is immune to context rot because it executes as external hook processes, not as LLM context.

- **The auto-escalation rules (AE-001 through AE-005):** The PreToolEnforcementEngine's governance file detection directly implements AE-001 (constitution modifications trigger auto-C4) and AE-002 (rules file modifications trigger auto-C3). The criticality escalation field in `EnforcementDecision` carries this information from the hook back to the Claude Code session, where it affects quality gate thresholds and review requirements.

- **The context monitoring system:** The staleness detector that runs as the third step in the `HooksPreToolUseHandler` pipeline connects the pre-tool enforcement to the orchestration state management. A stale `ORCHESTRATION.yaml` file triggers a warning that prevents agents from operating on outdated workflow state -- a different kind of safety concern than command blocking, but served by the same hook infrastructure.

---

## Alternative Perspectives

There is a legitimate argument for settings-level Bash restrictions in environments where the hook infrastructure is not available or not trusted. If Jerry's enforcement engines were removed or broken, the blanket Bash permission would leave no safety net between Claude Code's probabilistic judgment and the shell. In a deployment where the plugin hooks are not installed -- perhaps someone is using the Jerry repository without the plugin, or the hook registration is misconfigured -- the settings-level permission is the only control point.

A defense-in-depth purist might argue that *both* layers should enforce restrictions: settings patterns as the outer perimeter, hooks as the inner checkpoint. This is a reasonable position in theory. In practice, the asymmetry between interactive and background execution modes means that settings-level restrictions carry an operational cost (background agent failures) that hook-level restrictions do not. The decision to rely on hooks rather than settings for command-level security is a trade-off that prioritizes operational reliability over defense-in-depth layering -- a trade-off that is justified by the hook layer's test coverage and deterministic execution model.

It is also worth noting that Claude Code's permission system is evolving. The deprecated `:*` suffix syntax, the undocumented `allowed_tools`/`require_approval` field names discovered during the BUG-005 investigation, and the skill permission inheritance gap (GitHub #18950) all suggest that the settings-level permission system is not yet fully stable. Building security-critical logic on top of a changing API surface introduces maintenance risk. The hook-based enforcement engine, by contrast, is fully within Jerry's control and tested against known bypass vectors.

---

## Related

- **Reference:** [Claude Code Permission Syntax Reference](../reference/claude-code-permissions.md) -- Technical specification of permission patterns, evaluation order, and settings file format
- **Reference:** `src/infrastructure/internal/enforcement/security_rules.py` -- The frozen rule definitions that the SecurityEnforcementEngine evaluates against
- **Reference:** `src/infrastructure/internal/enforcement/security_enforcement_engine.py` -- The Layer 2 enforcement implementation
- **Reference:** `src/infrastructure/internal/enforcement/pre_tool_enforcement_engine.py` -- The Layer 3 architecture enforcement implementation
- **Reference:** `src/interface/cli/hooks/hooks_pre_tool_use_handler.py` -- The CLI handler that orchestrates all three enforcement steps
- **Investigation:** `projects/PROJ-030-bugs/work/BUG-005-skill-permission-pattern.md` -- The investigation that produced the empirical findings about Skill() permission behavior
