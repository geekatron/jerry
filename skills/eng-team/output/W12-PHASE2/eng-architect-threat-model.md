# Threat Model: tool_exec Bounded Context (Multi-Family Plugin Architecture)

> **Engagement:** W12-PHASE2
> **Criticality:** C3 (Significant -- >10 files, API surface change, security-sensitive credential filter)
> **Methodology:** STRIDE + DREAD scoring per C3 escalation, with Attack Tree summaries for HIGH-severity threats
> **Date:** 2026-03-17
> **Agent:** eng-architect (convergent mode)
> **NIST CSF 2.0 Mapping:** Identify (ID.AM, ID.RA), Protect (PR.AC, PR.DS, PR.IP), Detect (DE.CM)
> **SSDF Mapping:** PO.1 (security requirements), PO.2 (architecture ownership), PO.5 (secure environments)
> **Source Artifacts:**
>   - `projects/PROJ-023-exploit-framework/work/design/jerry-tool-exec-cli-design-v2.md`
>   - `projects/PROJ-023-exploit-framework/work/design/ADR-PROJ023-002-addendum-001-multi-family.md`
>   - Source code at `src/tool_exec/`, `src/interface/cli/tool_exec_commands.py`, `src/interface/cli/parser.py`

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level threat posture and key security decisions |
| [L0: Key Findings](#l0-key-findings) | Top 5 threats by risk score with business impact |
| [L1: Trust Boundary Analysis](#l1-trust-boundary-analysis) | Six trust boundaries with data flow classification |
| [L1: STRIDE Analysis Per Component](#l1-stride-analysis-per-component) | 22 threats across 11 components with STRIDE classification |
| [L1: DREAD Scoring Matrix](#l1-dread-scoring-matrix) | Quantified risk for all 22 threats |
| [L1: Prioritized Threat Matrix](#l1-prioritized-threat-matrix) | Threats ranked by DREAD composite score |
| [L1: Attack Trees (C3 Depth)](#l1-attack-trees-c3-depth) | Chained attack path analysis for HIGH-severity threats |
| [L1: Mitigation Recommendations](#l1-mitigation-recommendations) | Specific mitigations mapped to NIST CSF functions |
| [L2: Architecture Security Posture](#l2-architecture-security-posture) | Long-term security evolution and trade-off analysis |
| [L2: Residual Risk Assessment](#l2-residual-risk-assessment) | Post-mitigation risk posture |

---

## L0: Executive Summary

The `tool_exec` bounded context implements a multi-family plugin architecture for executing cybersecurity tools and AI CLIs through `jerry tool exec`. The system processes untrusted user input (tool names, arguments, engagement IDs, family names), loads configuration from YAML files that control code execution paths, invokes external processes via `subprocess.run`, and filters potentially credential-bearing tool output before presenting it to the user or persisting it as evidence.

**Architecture security posture: MODERATE with identified HIGH-severity threats requiring mitigation.**

The design incorporates several sound security decisions already in place:

1. **No `shell=True` in subprocess calls.** Both `LocalExecutor` and `ContainerExecutor` pass command lists to `subprocess.run`, preventing shell injection. This is the single most important security decision in the codebase.
2. **`yaml.safe_load()` exclusively.** The `FamilyRegistryLoader` and `RainbowToolResolver` both use safe loading, preventing YAML deserialization attacks.
3. **Path traversal validation in `EngagementInitializer`.** The `_validate_id()` method rejects `..`, `/`, and `\` characters in engagement IDs.
4. **Credential filter as a shared service.** The filter cannot be replaced or disabled per-family (only extended), preventing a malicious family from stripping credential detection.

**Three HIGH-severity threat areas require additional mitigation before deployment:**

1. **T-01: Dynamic import from YAML-specified module paths** (`FamilyRegistryLoader._load_resolver`) -- if `tool_families.yaml` is compromised, arbitrary Python code executes at startup.
2. **T-03: Credential filter false negatives** -- the 8-pattern L1 regex set has coverage gaps for modern cloud provider token formats that are relevant given the AI CLI family extension.
3. **T-06: `--no-filter` flag bypasses credential protection** -- no enforcement prevents an AI agent from passing this flag, which suppresses all credential detection.

---

## L0: Key Findings

| Rank | Threat ID | Threat | DREAD Score | Business Impact |
|------|-----------|--------|-------------|-----------------|
| 1 | T-01 | Arbitrary code execution via `importlib.import_module()` on YAML-controlled module path | 38 | Full system compromise if registry file is tampered. Attacker gains code execution with user privileges at CLI startup. |
| 2 | T-03 | Credential filter false negatives allow secrets to leak to agent context or evidence files | 36 | Exposed credentials (API keys, cloud tokens, database passwords) persist in evidence files and agent context, creating a lateral movement vector. |
| 3 | T-06 | `--no-filter` flag disables all credential protection | 34 | Agent-invoked tool execution could bypass credential filtering without human awareness, allowing secrets into the AI context window. |
| 4 | T-04 | Tool name shadowing across families via auto-detection priority manipulation | 30 | Silent redirection of a security tool invocation to a different family's resolver, potentially executing an unexpected binary. |
| 5 | T-08 | Engagement ID used in filesystem path without character-class allowlisting | 28 | Directory creation with attacker-controlled names; potential for symlink-based attacks or filesystem abuse even with `..` blocked. |

---

## L1: Trust Boundary Analysis

Six trust boundaries are identified in the data flow from user input to filtered output.

```
+----------------------------------------------------------------------+
|  UNTRUSTED ZONE                                                       |
|                                                                       |
|  User/Agent Input                                                     |
|  - tool_command (positional)     -- arbitrary string                  |
|  - tool_args (positional list)   -- arbitrary strings                 |
|  - --family (optional)           -- arbitrary string                  |
|  - --engagement-id (optional)    -- arbitrary string                  |
|  - --evidence-dir (optional)     -- arbitrary path                    |
|  - --zone (choices: 1,2,3)       -- constrained by argparse          |
|  - --mode (choices: local,cont.) -- constrained by argparse          |
|  - --no-filter (boolean)         -- flag, no validation needed        |
|                                                                       |
+---+------------------------------------------------------------------+
    | TB-1: User -> CLI Parser
    | Data: raw argv strings
    | Classification: UNTRUSTED -> VALIDATED
    v
+---+------------------------------------------------------------------+
|  CLI PARSER (src/interface/cli/parser.py)                             |
|  argparse validates: --mode, --zone (choices enum)                    |
|  argparse does NOT validate: tool_command, tool_args, --family,       |
|    --engagement-id, --evidence-dir                                    |
+---+------------------------------------------------------------------+
    | TB-2: CLI -> Domain Services
    | Data: partially validated args namespace
    | Classification: PARTIALLY VALIDATED -> DOMAIN LOGIC
    v
+---+------------------------------------------------------------------+
|  DOMAIN LAYER                                                         |
|  FamilyRouterService, ModeResolverService, CredentialFilterService,   |
|  EngagementInitializer, EvidenceHasher                                |
+---+------------------------------------------------------------------+
    | TB-3: Domain -> Infrastructure Adapters
    | Data: resolved ToolResolutionEntry, SecurityPolicy
    | Classification: DOMAIN VALIDATED -> INFRASTRUCTURE
    v
+---+------------------------------------------------------------------+
|  INFRASTRUCTURE LAYER                                                  |
|  FamilyRegistryLoader (importlib), RainbowToolResolver (yaml.safe_load)|
|  LocalExecutor (subprocess.run), ContainerExecutor (subprocess.run)    |
+---+------------------------------------------------------------------+
    | TB-4: Infrastructure -> External Process
    | Data: command list [tool_command, *tool_args]
    | Classification: VALIDATED COMMAND -> OS PROCESS BOUNDARY
    v
+---+------------------------------------------------------------------+
|  EXTERNAL PROCESS (tool binary or Docker container)                   |
|  Runs with user privileges. Produces stdout/stderr.                   |
+---+------------------------------------------------------------------+
    | TB-5: Tool Output -> Credential Filter
    | Data: raw stdout (UNTRUSTED -- tool output is attacker-influenced)
    | Classification: UNTRUSTED -> FILTERED
    v
+---+------------------------------------------------------------------+
|  POST-PROCESSING                                                      |
|  CredentialFilterService.filter_output()                              |
|  EvidenceHasher.hash_string()                                         |
|  Engagement evidence/quarantine persistence                           |
+---+------------------------------------------------------------------+
    | TB-6: Filtered Output -> User/Agent
    | Data: filtered stdout + exit code
    | Classification: FILTERED -> CONSUMER
    v
+---+------------------------------------------------------------------+
|  USER / AGENT (receives filtered output)                              |
+----------------------------------------------------------------------+

  TB-CONFIG: Configuration File Trust Boundary (cross-cutting)
  tool_families.yaml, tool-exec.yaml -- version-controlled, mutable
  Classification: TRUSTED BUT MUTABLE (git-controlled, PR-reviewed)
```

### Trust Boundary Data Flow Summary

| Boundary | From | To | Data Classification | Validation Mechanism |
|----------|------|----|--------------------|--------------------|
| TB-1 | User/Agent | CLI Parser | Untrusted raw strings | argparse choices (partial), positional capture (no validation) |
| TB-2 | CLI Parser | Domain Services | Partially validated namespace | Domain service input validation (engagement ID only) |
| TB-3 | Domain | Infrastructure | Resolved domain objects | Type system (dataclass fields), port contract (ABC) |
| TB-4 | Infrastructure | External Process | Command list | `subprocess.run(shell=False)` -- no shell expansion |
| TB-5 | External Process | Credential Filter | Untrusted stdout | Regex pattern matching (8 base patterns + extensions) |
| TB-6 | Post-processing | User/Agent | Filtered output + exit code | Redaction on detection; pass-through on clean output |
| TB-CONFIG | Filesystem | Registry Loader | YAML configuration | `yaml.safe_load()`, schema validation (partial) |

---

## L1: STRIDE Analysis Per Component

### 1. CLI Parser (`src/interface/cli/parser.py`, lines 983-1085)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-09 | Unvalidated `tool_command` positional argument | Tampering | `tool_command` is captured as a raw string with no format validation. Any string is accepted, including strings with embedded whitespace, null bytes, or control characters. While `subprocess.run` with `shell=False` prevents shell injection, the string is used as-is in filesystem paths (evidence filenames) and log messages. |
| T-10 | `tool_args` captured via `nargs="*"` with no validation | Tampering | `tool_args` are passed directly to `subprocess.run` as the argument list. No length limit, no character validation. Individual args could contain `--` separator abuse for tools that interpret double-dash specially. |
| T-11 | `--family` accepts arbitrary string | Spoofing | The `--family` flag is not constrained by argparse `choices`. An attacker can supply any string, which flows to `FamilyRouterService.resolve()` where it is used as a dictionary key lookup. The lookup fails safely (NotFoundError), but the error message includes the attacker-controlled string in the registered families list. |

### 2. FamilyRegistryLoader (`src/tool_exec/infrastructure/registry/family_registry_loader.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-01 | Arbitrary code execution via `importlib.import_module()` | Elevation of Privilege | Line 147: `importlib.import_module(family_info.resolver_module)` imports whatever module path is specified in `tool_families.yaml`. If the YAML file is modified (compromised developer machine, malicious PR, git config injection), an attacker can point `resolver_module` to a module containing arbitrary code that executes at import time. The `issubclass` check on line 150 runs after import -- the damage is done. |
| T-12 | Denial of service via missing or malformed registry | Denial of Service | If `tool_families.yaml` is deleted, corrupted, or contains invalid YAML, the entire `jerry tool exec` command fails at startup. The error handling catches the exception but provides the raw error message which may leak filesystem paths. |

### 3. FamilyRouterService (`src/tool_exec/domain/services/family_router.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-04 | Tool name shadowing via auto-detection priority | Spoofing | `_resolve_auto()` iterates `self._resolvers.values()` and returns the first match. Dictionary iteration order in Python 3.7+ is insertion order, which is determined by `FamilyRegistryLoader.load()` parsing order. A malicious family registered before rainbow with a broad `can_resolve()` that returns True for common tool names (e.g., `nuclei`, `trivy`) would intercept those tool invocations silently. |
| T-13 | Information disclosure via error messages | Information Disclosure | The `NotFoundError` raised in `_resolve_auto()` includes the list of all registered family names in the error message. This leaks the plugin configuration to the user, which may reveal internal architecture details. |

### 4. RainbowToolResolver (`src/tool_exec/infrastructure/adapters/rainbow_tool_resolver.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-14 | Wildcard prefix matching abuse | Spoofing | The `_find_entry()` method supports wildcard prefixes ending in `-*` (e.g., `impacket-*`). If a tool-exec.yaml entry has a short wildcard prefix like `a-*`, it would match any tool command starting with `a-`, potentially intercepting commands intended for other resolution entries. The longest-prefix-wins algorithm mitigates this partially, but short wildcards remain a risk. |
| T-15 | Zone downgrade via misconfigured tool-exec.yaml | Elevation of Privilege | If a Zone 3 tool (exploitation) is misconfigured as Zone 1 (audit) in tool-exec.yaml, it executes without engagement requirements and without per-operation approval. The resolver trusts the YAML zone assignment unconditionally. |

### 5. CredentialFilterService (`src/tool_exec/domain/services/credential_filter.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-03 | False negatives: credential patterns that evade the 8-pattern set | Information Disclosure | The filter has 4 case-sensitive and 4 case-insensitive base patterns. Notable gaps: (a) GitHub fine-grained tokens (`github_pat_`), (b) Google Cloud service account keys (JSON structure), (c) Slack webhook URLs, (d) Stripe API keys (`sk_live_`, `rk_live_`), (e) OpenAI/Anthropic/Google AI API keys (`sk-proj-`, `sk-ant-`, `AIza`), (f) JWT tokens (base64-encoded `eyJ` prefix), (g) Azure connection strings. The AI CLI family extension is specifically intended to handle cloud AI API keys, but if the extension patterns are incomplete, credentials leak. |
| T-16 | Pattern ReDoS (Regular Expression Denial of Service) | Denial of Service | The credential filter compiles 8+ regex patterns and runs them against every line of tool output. The AWS secret key pattern `[A-Za-z0-9/+=]{40}` and API token pattern `[A-Za-z0-9_.\:/\-]{20,}` have unbounded quantifiers that could exhibit catastrophic backtracking on adversarial input crafted by a malicious tool or compromised tool binary. |
| T-17 | `extend_patterns()` accepts arbitrary regex from family config | Tampering | Family-specific patterns added via `extend_patterns()` are compiled with `re.compile()` without validation of pattern complexity or correctness. A malicious family could inject a pattern that causes ReDoS or matches too broadly (e.g., `.*`), causing all output to be quarantined. |

### 6. LocalExecutor (`src/tool_exec/infrastructure/adapters/local_executor.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-02 | Tool command executed as first element of subprocess command list | Elevation of Privilege | Line 87: `cmd = [tool_command] + (tool_args or [])`. The `tool_command` is the user-supplied first positional argument. With `shell=False`, there is no shell injection, but the string is used as a binary name for OS `exec`. If PATH contains a malicious directory, or if the user specifies a relative or absolute path to a malicious binary, that binary executes with user privileges. The system does not validate that `tool_command` resolves to a known-good binary before execution. |
| T-18 | Stderr passes through unfiltered | Information Disclosure | The credential filter is applied only to stdout (line 115). Stderr is returned to the caller without any filtering. Tools that emit credentials on stderr (e.g., verbose error messages containing connection strings, stack traces with embedded secrets) bypass the credential filter entirely. |

### 7. ContainerExecutor (`src/tool_exec/infrastructure/adapters/container_executor.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-19 | Compose file path injection | Tampering | The compose file path comes from `ToolResolutionEntry.compose_file`, which originates from tool-exec.yaml. If the YAML is modified to point to a malicious compose file, the container executor will use it. The compose file controls volume mounts, network access, and container privileges. |
| T-20 | Container escape via `exec_flags` | Elevation of Privilege | The `execute()` method accepts `exec_flags` defaulting to `["-T"]`. If this parameter is exposed to user control in a future refactor, flags like `--privileged` could be injected. Currently, the parameter is not exposed to CLI users, but the API surface permits it. |

### 8. EngagementInitializer (`src/tool_exec/domain/services/engagement_initializer.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-08 | Engagement ID filesystem abuse | Tampering | The `_validate_id()` method blocks `..`, `/`, and `\` characters. However, it does not restrict the character class to safe characters (e.g., `[a-zA-Z0-9_-]`). An engagement ID like `$(whoami)` or `` `id` `` passes validation and creates a directory with that name. While not exploitable via subprocess (no shell), the name pollutes the filesystem and could confuse downstream tools that parse directory listings. |
| T-21 | Quarantine directory permissions not restricted | Information Disclosure | The `.credential-quarantine/` directory is created with default permissions (umask-dependent). On a shared system, other users could read quarantined credential-bearing output. The directory name is dot-prefixed (hidden) but has no additional access controls. |

### 9. ModeResolverService (`src/tool_exec/domain/services/mode_resolver.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-22 | Environment variable override of security-relevant mode | Elevation of Privilege | The `RAINBOW_TOOL_MODE` environment variable (level 2 in precedence) can override the configuration file default. An agent or process that sets this variable to `local` forces tools to execute outside container isolation, bypassing Zone 3's `container_required` policy. The design document acknowledges this is intentional (env vars are under user control), but when the tool is invoked by an AI agent, the user may not be aware of the env var state. |

### 10. EvidenceHasher (`src/tool_exec/domain/services/evidence_hasher.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-23 | Hash-only integrity without signatures | Tampering | Evidence integrity relies on SHA-256 hashes stored in separate `.meta.json` files. An attacker with filesystem write access can modify both the evidence file and its hash. There is no cryptographic signature or HMAC that would require a secret to forge. |

### 11. tool_exec_commands.py (CLI Handler, `src/interface/cli/tool_exec_commands.py`)

| ID | Threat | STRIDE | Description |
|----|--------|--------|-------------|
| T-06 | `--no-filter` flag disables credential protection | Information Disclosure | Line 82: `no_filter = getattr(args, "no_filter", False)`. When True, the credential filter is bypassed entirely (passed to `LocalExecutor.execute(no_filter=True)`). There is no check for strict mode enforcement at this level. An AI agent invoking `jerry tool exec --no-filter nuclei -u target.com` receives unfiltered output including any credentials in the scan results. |
| T-07 | `--evidence-dir` accepts arbitrary filesystem path | Tampering | Line 80: `evidence_dir_override = getattr(args, "evidence_dir", None)`. The path is used directly in `_persist_evidence()` (line 383: `Path(evidence_dir_override).mkdir(parents=True, exist_ok=True)`). An attacker can write evidence files to any directory writable by the current user, including overwriting existing files if the evidence filename collides. No path validation or sandboxing is applied. |

---

## L1: DREAD Scoring Matrix

DREAD scores each threat on five dimensions (1-10 scale):

- **D**amage: How bad is the impact?
- **R**eproducibility: How easy is it to reproduce?
- **E**xploitability: How easy is it to exploit?
- **A**ffected Users: How many users are affected?
- **D**iscoverability: How easy is it to find?

| ID | Threat Summary | D | R | E | A | D | Total | Priority |
|----|----------------|---|---|---|---|---|-------|----------|
| T-01 | `importlib` arbitrary code execution via YAML | 10 | 7 | 6 | 8 | 7 | **38** | CRITICAL |
| T-03 | Credential filter false negatives | 9 | 8 | 7 | 7 | 5 | **36** | HIGH |
| T-06 | `--no-filter` bypasses all credential protection | 9 | 10 | 7 | 5 | 3 | **34** | HIGH |
| T-04 | Tool name shadowing via auto-detect priority | 8 | 6 | 5 | 6 | 5 | **30** | HIGH |
| T-08 | Engagement ID character-class gap | 5 | 8 | 7 | 4 | 4 | **28** | MEDIUM |
| T-07 | `--evidence-dir` arbitrary path write | 6 | 9 | 6 | 3 | 4 | **28** | MEDIUM |
| T-02 | Tool binary resolution via PATH | 7 | 5 | 5 | 5 | 5 | **27** | MEDIUM |
| T-15 | Zone downgrade via misconfigured YAML | 8 | 4 | 4 | 6 | 4 | **26** | MEDIUM |
| T-18 | Stderr bypasses credential filter | 7 | 7 | 3 | 5 | 3 | **25** | MEDIUM |
| T-19 | Compose file path injection via YAML | 8 | 4 | 4 | 5 | 4 | **25** | MEDIUM |
| T-21 | Quarantine directory default permissions | 6 | 8 | 4 | 3 | 3 | **24** | MEDIUM |
| T-22 | Env var override of container isolation | 6 | 7 | 5 | 3 | 3 | **24** | MEDIUM |
| T-23 | Hash-only integrity (no signatures) | 5 | 8 | 3 | 4 | 3 | **23** | LOW |
| T-09 | Unvalidated `tool_command` format | 4 | 7 | 4 | 4 | 3 | **22** | LOW |
| T-14 | Wildcard prefix matching abuse | 5 | 4 | 4 | 4 | 4 | **21** | LOW |
| T-16 | Regex ReDoS in credential filter | 4 | 3 | 3 | 5 | 5 | **20** | LOW |
| T-17 | `extend_patterns()` arbitrary regex | 5 | 4 | 3 | 4 | 4 | **20** | LOW |
| T-11 | `--family` arbitrary string (info disclosure) | 2 | 9 | 8 | 2 | 2 | **23** | LOW |
| T-12 | DoS via missing/malformed registry | 3 | 7 | 6 | 3 | 3 | **22** | LOW |
| T-13 | Family name leakage in error messages | 2 | 9 | 8 | 2 | 2 | **23** | LOW |
| T-10 | `tool_args` no length limit | 3 | 5 | 4 | 3 | 3 | **18** | LOW |
| T-20 | Container escape via `exec_flags` API | 7 | 2 | 2 | 3 | 2 | **16** | LOW |

---

## L1: Prioritized Threat Matrix

Threats sorted by DREAD score, grouped into action tiers.

### Tier 1: MUST mitigate before deployment (DREAD >= 34)

| Rank | ID | DREAD | Component | STRIDE | Mitigation Status |
|------|----|-------|-----------|--------|-------------------|
| 1 | T-01 | 38 | FamilyRegistryLoader | EoP | **UNMITIGATED** -- `importlib.import_module()` executes YAML-specified module |
| 2 | T-03 | 36 | CredentialFilterService | ID | **PARTIALLY MITIGATED** -- 8 patterns active, known gaps for modern token formats |
| 3 | T-06 | 34 | tool_exec_commands.py | ID | **UNMITIGATED** -- no strict-mode enforcement for `--no-filter` |

### Tier 2: SHOULD mitigate before deployment (DREAD 26-33)

| Rank | ID | DREAD | Component | STRIDE | Mitigation Status |
|------|----|-------|-----------|--------|-------------------|
| 4 | T-04 | 30 | FamilyRouterService | S | **PARTIALLY MITIGATED** -- insertion-order determinism, but no CI collision check |
| 5 | T-08 | 28 | EngagementInitializer | T | **PARTIALLY MITIGATED** -- blocks `../` but allows special characters |
| 6 | T-07 | 28 | tool_exec_commands.py | T | **UNMITIGATED** -- arbitrary path accepted for evidence directory |
| 7 | T-02 | 27 | LocalExecutor | EoP | **PARTIALLY MITIGATED** -- no shell=True, but no binary allowlisting |

### Tier 3: CONSIDER mitigating (DREAD 20-25)

| Rank | ID | DREAD | Component | STRIDE | Mitigation Status |
|------|----|-------|-----------|--------|-------------------|
| 8 | T-15 | 26 | RainbowToolResolver | EoP | **PARTIALLY MITIGATED** -- zone from config, but no cross-validation |
| 9 | T-18 | 25 | LocalExecutor | ID | **UNMITIGATED** -- stderr unfiltered |
| 10 | T-19 | 25 | ContainerExecutor | T | **PARTIALLY MITIGATED** -- compose files in git, but no path validation |
| 11 | T-21 | 24 | EngagementInitializer | ID | **UNMITIGATED** -- default umask permissions |
| 12 | T-22 | 24 | ModeResolverService | EoP | **BY DESIGN** -- env vars under user control; document risk for agent usage |

### Tier 4: Accept risk with monitoring (DREAD < 20)

All remaining threats (T-09, T-10, T-11, T-12, T-13, T-14, T-16, T-17, T-20, T-23) are assessed as LOW priority. Accept with documentation.

---

## L1: Attack Trees (C3 Depth)

Per C3 methodology, attack trees are provided for the three Tier 1 threats to analyze chained attack paths.

### Attack Tree 1: Arbitrary Code Execution via FamilyRegistryLoader (T-01)

```
GOAL: Execute arbitrary code on developer/CI machine via jerry tool exec
|
+-- [AND] Modify tool_families.yaml to point to malicious module
|   |
|   +-- [OR] Path 1: Malicious PR accepted
|   |   +-- Craft PR that modifies tool_families.yaml
|   |   +-- Social-engineer reviewer to approve
|   |   +-- IMPACT: Code executes on all users who pull the branch
|   |
|   +-- [OR] Path 2: Compromised developer workstation
|   |   +-- Gain write access to local clone
|   |   +-- Modify tool_families.yaml resolver_module to malicious path
|   |   +-- Wait for user to run jerry tool exec
|   |   +-- IMPACT: Immediate code execution
|   |
|   +-- [OR] Path 3: Git config injection
|       +-- Exploit git merge driver or smudge filter to modify YAML on checkout
|       +-- tool_families.yaml resolver_module now points to attacker module
|       +-- IMPACT: Persistent across checkouts
|
+-- [AND] Malicious module is importable
    |
    +-- [OR] Module exists in sys.path (any src/ or site-packages directory)
    +-- [OR] Module path references installed package (pip/uv install)
    +-- [OR] Module path uses relative import from project root
    |
    +-- issubclass check runs AFTER import -- arbitrary __init__.py code
        already executed at import time
```

**Chain analysis:** The most realistic attack path is Path 1 (malicious PR). The `tool_families.yaml` file is not typically scrutinized with the same rigor as Python source files during code review. A change from `src.tool_exec.infrastructure.adapters.rainbow_tool_resolver` to `src.tool_exec.infrastructure.adapters.rainbow_tool_resolver_v2` (a plausible-looking module name) could pass review, especially if the PR includes the malicious module file.

### Attack Tree 2: Credential Leakage via Filter Bypass (T-03 + T-06 chain)

```
GOAL: Extract credentials from tool output into agent context
|
+-- [OR] Path A: Direct filter bypass
|   +-- Pass --no-filter flag
|   +-- Tool output (including credentials) flows to stdout
|   +-- Agent receives unfiltered output
|   +-- IMPACT: Credentials in AI context window
|
+-- [OR] Path B: Filter evasion (false negative)
|   +-- Tool outputs credential in format not covered by 8 patterns
|   +-- [Examples of evasion]
|   |   +-- GitHub fine-grained PAT: github_pat_11AABBC...
|   |   +-- JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
|   |   +-- Google AI key: AIzaSy...
|   |   +-- Base64-encoded credential in JSON blob
|   |   +-- Credential split across two lines
|   +-- Filter returns detected=False
|   +-- IMPACT: Credentials in evidence file and agent context
|
+-- [OR] Path C: Stderr credential leakage
    +-- Tool outputs credential on stderr (error messages, debug output)
    +-- Credential filter only scans stdout
    +-- stderr passed through to user/agent unfiltered
    +-- IMPACT: Credentials in agent context via stderr
```

**Chain analysis:** Paths B and C are the most concerning because they are silent. Path A (--no-filter) is observable but currently has no enforcement mechanism. The combination of B + C means that even when the filter is active, credentials can leak through two separate channels.

### Attack Tree 3: Tool Name Shadowing (T-04 + T-01 chain)

```
GOAL: Redirect legitimate tool execution to attacker-controlled resolver
|
+-- [AND] Register malicious family with high priority
|   +-- Modify tool_families.yaml to add malicious family entry
|   +-- Set it as first entry (highest priority in auto-detection)
|
+-- [AND] Malicious family's can_resolve() returns True for target tools
|   +-- Implement broad can_resolve() matching common tool prefixes
|
+-- [AND] Malicious resolver returns ToolResolutionEntry pointing to
|   attacker binary
|   +-- resolve() returns entry with altered binary path or container config
|   +-- User invokes: jerry tool exec nuclei -u target.com
|   +-- Auto-detection hits malicious family first, never reaches rainbow
|   +-- IMPACT: Different binary executes, potentially with different
|     security constraints (no engagement, no container isolation)
```

**Chain analysis:** This attack requires the same initial access as T-01 (modify tool_families.yaml), but is more subtle -- the tool appears to execute normally, but the resolver has been silently substituted. This makes detection harder than T-01.

---

## L1: Mitigation Recommendations

Each mitigation is mapped to the NIST CSF 2.0 function it supports.

### Tier 1 Mitigations (MUST implement)

| ID | Threat | Mitigation | Implementation | CSF Function | Effort |
|----|--------|------------|----------------|-------------|--------|
| M-01 | T-01 | **Module path allowlist.** Add a `_ALLOWED_MODULE_PREFIXES` constant to `FamilyRegistryLoader` that restricts `resolver_module` values to `src.tool_exec.infrastructure.adapters.` or a configurable allowlist. Reject any import path outside the allowlist before calling `importlib.import_module()`. | Add validation in `_load_resolver()` before line 147. Pattern: `if not family_info.resolver_module.startswith(tuple(self._ALLOWED_MODULE_PREFIXES)): raise ValueError(...)`. | PR.IP-1 (Protect: baseline config) | 1 hour |
| M-02 | T-03 | **Expand credential filter patterns.** Add patterns for: (a) `github_pat_` (GitHub fine-grained PAT), (b) `eyJ` prefix (JWT tokens, case-sensitive), (c) `sk-proj-` / `sk-ant-` / `AIza` (AI provider keys), (d) `sk_live_` / `rk_live_` (Stripe keys), (e) `xoxb-` / `xoxp-` (Slack tokens). Add corresponding canary test fixtures. | Add to `_BASE_CS_PATTERNS` and `_BASE_CI_PATTERNS` in `credential_filter.py`. Create canary fixtures in `tests/credential-fixtures/`. | PR.DS-1 (Protect: data security) | 2 hours |
| M-03 | T-06 | **Strict mode enforcement for `--no-filter`.** Check `RAINBOW_STRICT_MODE` (or generic `JERRY_STRICT_MODE`) environment variable in `handle_tool_exec()`. When strict mode is active, reject `--no-filter` with exit code and error message. Log a warning when `--no-filter` is used even outside strict mode. | Add check in `tool_exec_commands.py` after line 82: `if no_filter and os.environ.get("JERRY_STRICT_MODE") == "true": print("Error: --no-filter is FORBIDDEN when strict mode is active"); return ExitCode.STRICT_MODE_VIOLATION`. | PR.AC-1 (Protect: access control) | 0.5 hours |

### Tier 2 Mitigations (SHOULD implement)

| ID | Threat | Mitigation | Implementation | CSF Function | Effort |
|----|--------|------------|----------------|-------------|--------|
| M-04 | T-04 | **CI tool name collision check.** Add a CI step that extracts all tool prefixes from all family config files and asserts zero collisions. Add `--verbose` logging to `FamilyRouterService._resolve_auto()` showing which family claimed the tool. | CI script: parse tool-exec.yaml and any future family configs, extract all `prefix` values, assert no intersection. Add `logging.info("Auto-detected family '%s' for tool '%s'", ...)` in `_resolve_auto()`. | DE.CM-1 (Detect: monitoring) | 1.5 hours |
| M-05 | T-08 | **Engagement ID character-class allowlist.** Replace the blocklist validation (`..`, `/`, `\`) with an allowlist: `re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$', engagement_id)`. This restricts IDs to alphanumeric characters, hyphens, and underscores, starting with an alphanumeric character. | Replace `_validate_id()` body in `engagement_initializer.py`. | PR.IP-1 (Protect: baseline config) | 0.5 hours |
| M-06 | T-07 | **Evidence directory path sandboxing.** Validate that `--evidence-dir` resolves to a path under the project root or a designated output directory. Use `Path.resolve()` and check that the resolved path starts with the allowed prefix. | Add validation in `handle_tool_exec()` after `evidence_dir_override` is captured. Pattern: `resolved = Path(evidence_dir_override).resolve(); if not str(resolved).startswith(str(project_root)): reject`. | PR.IP-1 (Protect: baseline config) | 0.5 hours |
| M-07 | T-02 | **Tool binary resolution validation.** After family resolution produces a `tool_command`, verify the binary exists via `shutil.which()` before calling `subprocess.run()`. Log the full resolved path for audit. This does not prevent PATH manipulation but makes it observable. | Add `import shutil; resolved_path = shutil.which(tool_command)` check in `LocalExecutor.execute()` before line 90. Log the resolved path. | ID.AM-2 (Identify: asset management) | 0.5 hours |

### Tier 3 Mitigations (CONSIDER implementing)

| ID | Threat | Mitigation | Implementation | CSF Function | Effort |
|----|--------|------------|----------------|-------------|--------|
| M-08 | T-18 | **Apply credential filter to stderr.** Extend `LocalExecutor.execute()` and `ContainerExecutor.execute()` to run the credential filter against stderr in addition to stdout. | After capturing `result.stderr`, apply `self._credential_filter.filter_output(result.stderr)`. Merge detection results. | PR.DS-1 | 1 hour |
| M-09 | T-15 | **Zone assignment cross-validation CI check.** Create a CI step that validates known high-risk tool prefixes (e.g., `msfconsole`, `impacket-*`, `pwntools`) are assigned to Zone 3. Maintain an explicit list of tools that MUST be Zone 3. | CI script: parse tool-exec.yaml, check that listed prefixes have `zone: 3`. | DE.CM-1 | 1 hour |
| M-10 | T-21 | **Restrict quarantine directory permissions.** Set permissions to `0o700` on the quarantine directory after creation. | Add `os.chmod(str(quarantine_dir), 0o700)` after `quarantine_dir.mkdir()` in `engagement_initializer.py`. | PR.DS-1 | 0.25 hours |
| M-11 | T-19 | **Compose file path validation.** Validate that compose file paths from tool-exec.yaml resolve to files within the project repository. Use `Path.resolve()` and prefix check. | Add validation in `ContainerExecutor.execute()` or in `RainbowToolResolver.resolve()`. | PR.IP-1 | 0.5 hours |

### Total Mitigation Effort

| Tier | Count | Estimated Effort |
|------|-------|-----------------|
| Tier 1 (MUST) | 3 mitigations | 3.5 hours |
| Tier 2 (SHOULD) | 4 mitigations | 3.0 hours |
| Tier 3 (CONSIDER) | 4 mitigations | 2.75 hours |
| **Total** | **11 mitigations** | **9.25 hours** |

---

## L2: Architecture Security Posture

### Strengths

1. **Hexagonal architecture provides natural trust boundaries.** The port/adapter pattern means the domain layer never directly interacts with external processes or the filesystem. Security constraints are expressed as domain-level `SecurityPolicy` objects, and infrastructure adapters enforce them. This is a structurally sound design.

2. **Credential filter is a shared service, not per-family.** The design decision (AD-V2-03) to have a single `CredentialFilterService` with profiles means no family can opt out of credential detection. Families can only extend the pattern set, not replace or reduce it. This is a defense-in-depth decision that constrains the plugin architecture's attack surface.

3. **subprocess.run with shell=False is the correct baseline.** Both executors consistently use list-based command construction without shell interpretation. This eliminates the most common class of command injection vulnerabilities.

4. **YAML safe_load prevents deserialization attacks.** Both config loaders use `yaml.safe_load()`, preventing arbitrary Python object instantiation from YAML.

### Weaknesses

1. **The `importlib` dynamic import in `FamilyRegistryLoader` contradicts the "no dynamic plugins" design decision.** ADR-PROJ023-002 Addendum 001, AD-V2-01 explicitly rejected dynamic discovery in favor of explicit registration. However, the implementation still uses `importlib.import_module()` with a module path from YAML. The registration is explicit (YAML-declared), but the loading mechanism is dynamic. This is the single largest attack surface gap.

2. **The credential filter is L1-only (regex).** The design document references a three-layer pipeline (L1 regex, L2 entropy, L3 structural), but only L1 is implemented. L2 and L3 would catch credentials that evade pattern matching (e.g., high-entropy strings, JSON structures containing key-value pairs). The absence of L2/L3 means the filter's effectiveness depends entirely on pattern coverage.

3. **No input validation schema at the CLI boundary.** The `argparse` parser validates `--mode` and `--zone` via `choices`, but `tool_command`, `tool_args`, `--family`, `--engagement-id`, and `--evidence-dir` are accepted as arbitrary strings. A validation layer between argparse and domain services would catch malformed inputs before they reach business logic.

4. **Evidence integrity is hash-based, not signature-based.** An attacker with filesystem write access can modify both the evidence file and its hash. For a cybersecurity framework producing evidence for engagements, this is below the expected integrity assurance level. HMAC or digital signatures would provide tamper evidence.

### Trade-off Analysis

| Decision | Security Gain | Security Cost | Net Assessment |
|----------|--------------|---------------|----------------|
| Plugin architecture via ports | Extensible without modifying core | Expands attack surface (T-01, T-04) | **NET POSITIVE** if M-01 (module allowlist) is implemented |
| Shared credential filter | Single enforcement point; no family can opt out | Single point of failure for false negatives | **NET POSITIVE** -- centralization enables systematic improvement |
| Auto-detection with priority | Backward compatibility; no breaking changes | Silent misdirection risk (T-04) | **NET NEUTRAL** -- convenience vs. security; `--family` flag provides escape hatch |
| `--no-filter` flag existence | Developer convenience for debugging | Credential protection bypass (T-06) | **NET NEGATIVE** unless strict mode enforcement (M-03) is added |

### Long-term Security Evolution

1. **Phase 1 (Current W12 scope):** Implement Tier 1 and Tier 2 mitigations. This addresses the three CRITICAL/HIGH threats and establishes the baseline security posture.

2. **Phase 2 (Post-W12):** Implement L2 entropy analysis in the credential filter. This would use Shannon entropy scoring on string segments to catch credentials that evade pattern matching. Estimated effort: 4-6 hours.

3. **Phase 3 (When AI CLI family ships):** Add the AI-provider-specific credential patterns (M-02 extends to cover `sk-proj-`, `AIza`, etc.). Add API key rotation detection (detect when a key appears in output that matches a known env var value, not just a pattern).

4. **Phase 4 (10+ families):** Replace `importlib` dynamic loading with a compile-time registry. Use a build step that generates a Python module mapping family names to resolver classes, eliminating runtime dynamic imports entirely. This closes T-01 permanently.

---

## L2: Residual Risk Assessment

Post-mitigation risk posture assuming all Tier 1 and Tier 2 mitigations are implemented.

| ID | Original DREAD | Mitigated By | Residual DREAD | Residual Priority |
|----|---------------|-------------|----------------|-------------------|
| T-01 | 38 | M-01 (module allowlist) | 18 | LOW (restricted to known-good module prefix) |
| T-03 | 36 | M-02 (pattern expansion) | 24 | MEDIUM (L1-only still has theoretical gaps; L2/L3 needed for further reduction) |
| T-06 | 34 | M-03 (strict mode enforcement) | 16 | LOW (blocked in strict mode; warned in permissive mode) |
| T-04 | 30 | M-04 (CI collision check) | 16 | LOW (CI prevents collisions; --verbose makes detection observable) |
| T-08 | 28 | M-05 (character allowlist) | 10 | LOW (only alphanumeric + hyphens + underscores allowed) |
| T-07 | 28 | M-06 (path sandboxing) | 12 | LOW (constrained to project root subtree) |
| T-02 | 27 | M-07 (binary resolution logging) | 20 | LOW-MEDIUM (observable but not preventable without binary allowlist) |

### Residual Risk Summary

| Priority | Pre-Mitigation Count | Post-Mitigation Count |
|----------|---------------------|----------------------|
| CRITICAL (DREAD >= 34) | 3 | 0 |
| HIGH (DREAD 26-33) | 4 | 0 |
| MEDIUM (DREAD 20-25) | 5 | 2 (T-03 residual, T-18 unmitigated) |
| LOW (DREAD < 20) | 10 | 20 |

**Post-mitigation posture: LOW-MEDIUM.** The two remaining MEDIUM risks (T-03 credential filter false negatives with expanded but still L1-only detection, and T-18 stderr bypass) are addressed by Phase 2 and Tier 3 mitigations respectively. The architecture is sound; the risks are operational (pattern coverage, output channel coverage) rather than structural.

---

*Threat Model Version: 1.0.0*
*Constitutional Compliance: P-001 (evidence-based -- all threats traced to source code lines and design documents), P-002 (persisted to file), P-022 (confidence levels explicit; gaps disclosed)*
*Created: 2026-03-17*
*Agent: eng-architect (convergent mode, STRIDE + DREAD per C3 escalation)*
