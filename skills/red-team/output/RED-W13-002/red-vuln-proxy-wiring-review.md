# RED-W13-002: Vulnerability Analysis -- ContainerExecutor Proxy Injection and Path Reference Migration

> **Engagement ID:** RED-W13-002
> **Agent:** red-vuln
> **Date:** 2026-03-19
> **Phase:** Vulnerability Analysis
> **Scope:** ContainerExecutor HTTP_PROXY injection (T13-021, T13-022) and STORY-W12-002 path reference migration
> **Authorization Level:** Analysis scope; read-only; no exploitation
> **Classification:** Internal Security Review

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Severity counts, key findings, overall risk posture |
| [L1 Technical Findings](#l1-technical-findings) | Per-finding CVE correlation, CVSS, mitigations |
| [L2 Strategic Implications](#l2-strategic-implications) | Attack path analysis, chaining, prioritization |

---

## L0 Executive Summary

### Vulnerability Count by Severity

| Severity | Count | Change Area |
|----------|-------|-------------|
| HIGH | 3 | Proxy injection (VULN-001, VULN-002, VULN-003) |
| MEDIUM | 2 | Proxy injection (VULN-004, VULN-005) |
| LOW | 2 | Path migration (VULN-006, VULN-007) |
| **Total** | **7** | |

### Top Exploitable Findings

1. **VULN-001 (HIGH):** Proxy URL injection via `engagement_id` -- attacker-controlled proxy URL can redirect all tool traffic through an attacker-controlled endpoint. The current design takes the Envoy service name from the engagement ID without sanitizing it into the proxy URL construction path. CVSS 7.4.
2. **VULN-002 (HIGH):** `exec_flags` injection vector -- the `exec_flags` parameter passed through `_build_command` is appended to the Docker command list without validation. A caller controlling `exec_flags` can inject `-e VAR=value` entries that override the intended proxy settings. CVSS 7.1.
3. **VULN-003 (HIGH):** Fail-open on Envoy container down -- no design decision has been codified for what happens when the Envoy proxy container is unreachable. The current architecture silently falls through to unproxied execution, which means tool traffic bypasses the engagement-scoped network boundary. CVSS 6.9 (no authentication bypass, but scope boundary violated).

### Overall Risk Posture

**MEDIUM-HIGH.** The proxy injection feature adds a network-routing trust boundary to the Container Executor that does not currently exist. Before this change, the Executor's threat surface was local process isolation. After the change, the proxy URL becomes a security-sensitive parameter whose integrity is required for proper network segmentation between zones. The path migration change carries low residual risk, limited to a transient dual-invocation window during the migration period.

### Key Recommendations

- Do not accept the proxy URL as a string; derive it deterministically from a validated zone number and a fixed hostname pattern.
- Whitelist `exec_flags` entries; reject any entry that matches `-e ` or `--env`.
- Enforce fail-closed on proxy unavailability for Zone 2 and Zone 3 tools; fail-open is acceptable for Zone 1 only.
- Complete path migration atomically (single commit, verified grep) to eliminate the dual-invocation window.

---

## L1 Technical Findings

### VULN-001: Proxy URL Injection via Engagement-Derived Input (HIGH)

**Severity:** HIGH
**CWE:** CWE-88 Improper Neutralization of Argument Delimiters in a Command (Argument Injection)
**CVSS 3.1 Base Score:** 7.4 (AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:N)
**ATT&CK Technique:** T1090 (Proxy)
**Exploit Availability:** No public PoC; requires internal attacker with engagement initialization access

**Description:**

The proposed proxy injection constructs the `-e HTTP_PROXY=http://envoy-zN:3128` value where `envoy-zN` encodes the zone number. If the proxy hostname or port is sourced from any user-controllable input -- such as the engagement scope file's `authorized_targets`, the engagement ID, a config field, or a CLI flag -- an attacker with write access to that input can redirect all tool HTTP traffic to an arbitrary host.

Concretely, in `tool_exec_commands.py`, the `_generate_envoy_configs` function at line 796 derives Envoy config paths from the `scope_file` argument. The scope file is user-supplied (`--scope-file`). If the proxy hostname used in `_build_command`'s `-e HTTP_PROXY=...` value is constructed from the scope file content rather than a statically-bound constant, the attack path is:

1. Attacker supplies a crafted `--scope-file` with a malicious `authorized_targets` entry.
2. `generate_envoy_config()` writes or overwrites `envoy-zone2-active.yaml` with attacker-controlled routes.
3. ContainerExecutor injects `-e HTTP_PROXY=http://attacker-controlled-proxy:3128`.
4. All reconnaissance or exploitation tool traffic is routed through the attacker proxy.
5. The attacker observes tool output including credentials, target responses, and raw tool data -- bypassing the credential filter at the network layer (credentials are in transit, not yet filtered by the Python filter).

Even if the proxy hostname is statically derived as `envoy-zN`, a malicious engagement scope file that changes the Envoy config YAML content can cause the Envoy sidecar to proxy traffic to attacker-controlled upstreams.

**Code-Level Mitigation:**

In `ContainerExecutor._build_command`, the proxy env var values MUST be derived from a compile-time constant or a validated allowlist, not from any runtime user input:

```python
# SECURE: derive proxy URL from zone integer, never from string input
_ENVOY_PROXY_HOSTS: dict[int, str] = {
    1: "envoy-z1",
    2: "envoy-z2",
    3: "envoy-z3",
}
_ENVOY_PROXY_PORT = 3128

def _proxy_env_flags(self, zone: int) -> list[str]:
    host = _ENVOY_PROXY_HOSTS.get(zone)
    if host is None:
        raise ValueError(f"No proxy defined for zone {zone}")
    url = f"http://{host}:{_ENVOY_PROXY_PORT}"
    return ["-e", f"HTTP_PROXY={url}", "-e", f"HTTPS_PROXY={url}"]
```

The zone integer MUST be validated as `int` and checked to be in `{1, 2, 3}` before calling `_proxy_env_flags`. It MUST NOT be derived from any string that originated in user input.

---

### VULN-002: exec_flags Injection -- Proxy Override via Flag Injection (HIGH)

**Severity:** HIGH
**CWE:** CWE-77 Improper Neutralization of Special Elements used in a Command (Command Injection via argument list)
**CVSS 3.1 Base Score:** 7.1 (AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N)
**ATT&CK Technique:** T1574.006 (Hijack Execution Flow: Dynamic Linker Hijacking -- closest analogue for env var override)
**Exploit Availability:** Requires caller-controlled `exec_flags`; exploitable by any code path that constructs `exec_flags` from untrusted input

**Description:**

`ContainerExecutor._build_command` (line 259) appends `exec_flags` directly to the command list before the service name and tool:

```python
cmd.append("exec")
cmd.extend(exec_flags)      # <-- no validation
cmd.append(service)
cmd.append(tool_command)
cmd.extend(tool_args)
```

The `execute()` method receives `exec_flags` as a caller-supplied parameter. If the proxy injection logic sets the correct `-e HTTP_PROXY=...` flags in `exec_flags` but a caller (e.g., a test helper, a future CLI flag, or a direct API consumer) also supplies `exec_flags` containing `-e HTTP_PROXY=http://attacker:3128`, Docker's last `-e` wins for `docker compose exec`.

Attack vector: any code path that calls `executor.execute(..., exec_flags=["-T", "-e", "HTTP_PROXY=http://attacker:3128"])` overrides the intended Envoy proxy. Because `exec_flags` is a public parameter, this attack does not require modifying the executor itself.

Furthermore, if the proxy flags are injected by appending to the default `exec_flags or ["-T"]`, a caller who supplies an explicit `exec_flags` list that omits the proxy entries will silently execute without proxy routing.

**Code-Level Mitigation:**

The proxy env var flags MUST be injected by the executor itself after all caller-supplied `exec_flags` have been validated. The executor should:

1. Validate `exec_flags` against an allowlist that explicitly rejects `-e` and `--env` entries:

```python
_FORBIDDEN_EXEC_FLAG_PREFIXES = ("-e", "--env", "-E", "--env-file")

def _validate_exec_flags(self, flags: list[str]) -> None:
    for flag in flags:
        if any(flag.startswith(p) for p in _FORBIDDEN_EXEC_FLAG_PREFIXES):
            raise ValueError(
                f"exec_flags must not contain environment variable flags: {flag!r}. "
                "Proxy env vars are injected by the executor."
            )
```

2. Append the proxy flags at a fixed position after validation, so they cannot be overridden by caller-supplied flags.

---

### VULN-003: Fail-Open on Envoy Container Unavailability (HIGH)

**Severity:** HIGH
**CWE:** CWE-636 Not Failing Securely (Fail-Open)
**CVSS 3.1 Base Score:** 6.9 (AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:N)
**ATT&CK Technique:** T1090.002 (External Proxy); T1562 (Impair Defenses)
**Exploit Availability:** Exploitable by stopping the Envoy container before tool execution

**Description:**

The current `ContainerExecutor.health_check()` method checks whether a Docker Compose service is running. However, the proposed design has no decision on what happens when `health_check("envoy-zN")` returns `False` at execution time.

If the implementation fails open (proceeds with execution without proxy), the network segmentation boundary is silently violated. Zone 2 reconnaissance tools (Subfinder, Naabu, Nuclei) and Zone 3 exploitation tools (Metasploit, Impacket) would egress directly from the container's default network interface, bypassing:
- Envoy's outbound domain allowlist
- Zone-specific traffic inspection
- Engagement scope target restriction enforcement at the network layer

An attacker with access to the Docker host can reliably trigger this condition by stopping the Envoy container (`docker stop envoy-z2`) immediately before an operator initiates a Zone 2/3 tool execution.

**Code-Level Mitigation:**

Zone 2 and Zone 3 tool executions MUST fail-closed when the proxy is unavailable:

```python
def _assert_proxy_available(self, zone: int) -> None:
    """Raise RuntimeError if the zone's Envoy proxy is not running.

    Zone 1 allows fail-open (proxy is a convenience, not a boundary).
    Zone 2 and Zone 3 require fail-closed (proxy enforces scope boundary).
    """
    if zone not in (2, 3):
        return  # Zone 1: fail-open acceptable
    proxy_service = f"envoy-z{zone}"
    if not self.health_check(proxy_service, compose_file=self._compose_file):
        raise RuntimeError(
            f"[SECURITY] Zone {zone} execution blocked: "
            f"Envoy proxy service '{proxy_service}' is not running. "
            "Start the proxy before executing Zone 2/3 tools."
        )
```

This check MUST be called before `subprocess.run()` in `execute()`. The `health_check()` timeout (currently 30 seconds per line 226) should be reduced to 5 seconds for this pre-execution check to avoid unacceptable latency.

Zone 1 tools (supply-chain scanning, cloud posture) MAY fail-open because they do not require network scope enforcement -- their traffic is limited to public package registries and cloud APIs. This distinction is already reflected in the zone model.

---

### VULN-004: NO_PROXY Injection to Bypass Proxy for Specific Hosts (MEDIUM)

**Severity:** MEDIUM
**CWE:** CWE-284 Improper Access Control
**CVSS 3.1 Base Score:** 5.3 (AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N)
**ATT&CK Technique:** T1090 (Proxy)
**Exploit Availability:** Requires attacker-controlled input to the `exec_flags` list or to a future `no_proxy_hosts` parameter

**Description:**

`docker compose exec -e NO_PROXY=10.0.0.0/8 ...` causes the container process to bypass the HTTP_PROXY for any host matching the `NO_PROXY` value. If `NO_PROXY` can be injected -- either via the `exec_flags` parameter (see VULN-002) or via a future `no_proxy_hosts` configuration option -- an attacker can direct traffic for specific target hosts around the Envoy proxy entirely.

This is lower severity than VULN-002 because it requires two conditions: (1) the VULN-002 exec_flags injection path must be open or a NO_PROXY configuration option must exist, and (2) the attacker must know specific target host addresses in advance.

**Code-Level Mitigation:**

The executor MUST NOT accept or propagate `NO_PROXY` from any caller-supplied source. The only permissible `NO_PROXY` value is the static list of Docker internal hosts that must always bypass the proxy (e.g., `localhost,127.0.0.1,host-gateway`). This list MUST be compiled into the executor:

```python
_STATIC_NO_PROXY = "localhost,127.0.0.1,::1,host-gateway"

def _proxy_env_flags(self, zone: int) -> list[str]:
    ...
    return [
        "-e", f"HTTP_PROXY={url}",
        "-e", f"HTTPS_PROXY={url}",
        "-e", f"NO_PROXY={_STATIC_NO_PROXY}",
    ]
```

If the executor also sets `NO_PROXY`, it overrides any attacker-injected value (because the executor's flags are appended last, after caller-supplied `exec_flags` are validated and rejected for env var entries per VULN-002 mitigation).

---

### VULN-005: Proxy URL Reflected in Subprocess Arguments -- Sensitive Data in Process List (MEDIUM)

**Severity:** MEDIUM
**CWE:** CWE-214 Invocation of Process Using Visible Sensitive Information
**CVSS 3.1 Base Score:** 4.7 (AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N)
**ATT&CK Technique:** T1057 (Process Discovery)
**Exploit Availability:** Local; `ps aux` on the Docker host during execution window

**Description:**

`subprocess.run(cmd, ...)` where `cmd` contains `-e HTTP_PROXY=http://envoy-z2:3128` will make the proxy URL (and any authentication credentials in the URL, if any are ever added) visible in the process argument list on the Docker host via `ps aux`. This is a medium severity finding because:
- The current proxy URL has no embedded credentials.
- The window is narrow (subprocess lifetime).
- Requires local access to the Docker host.

If proxy credentials are ever added to the URL (e.g., `http://user:password@envoy-z2:3128`), this becomes a HIGH finding.

**Code-Level Mitigation:**

Never embed credentials in the proxy URL. The URL passed to `-e HTTP_PROXY=...` MUST be a hostname:port only. If Envoy authentication is ever required, it must be handled via a Docker secret or a mounted credential file, not via the proxy URL.

Document this constraint explicitly in the executor's docstring and in the proxy URL derivation function.

---

### VULN-006: Transient Dual-Invocation Window During Path Migration (LOW)

**Severity:** LOW
**CWE:** CWE-706 Use of Incorrectly-Resolved Name or Reference
**CVSS 3.1 Base Score:** 3.1 (AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:N)
**ATT&CK Technique:** T1574 (Hijack Execution Flow)
**Exploit Availability:** Requires partial migration state on disk; exploitable only during migration window

**Description:**

STORY-W12-002 migrates ~75 path references from `skills/rainbow/output/` to `work/engagements/` across ~28 files. During a partial migration (after some but not all files are updated, and before `EN-W12-001` deletes the bash script), two execution paths exist simultaneously:
- Agent `.md` files already updated to reference `jerry tool exec` route through the Python CLI to `work/engagements/`.
- Agent `.md` files not yet updated still reference `rainbow-tool-exec` and write to `skills/rainbow/output/`.

An attacker with read access to `skills/rainbow/output/` (which may be world-readable inside the repo, depending on `.gitignore`) can observe tool output that the operator believes is being written to the protected `work/engagements/` tree.

This is low severity because: (1) it requires the attacker to know a migration is in progress, (2) the window is bounded by the migration duration, and (3) it does not allow active injection.

**Code-Level Mitigation:**

Perform STORY-W12-002 as a single atomic commit that updates all files simultaneously, followed immediately by `EN-W12-001` in a dependent commit. The acceptance criterion `grep -r "skills/rainbow/output/" skills/ docs/ AGENTS.md` returns 0 results already captures this requirement.

During CI, add an explicit guard that fails the build if both `skills/rainbow/bin/rainbow-tool-exec` and any `skills/rainbow/output/` reference exist simultaneously in the tree:

```bash
# In CI gate:
if git ls-files "skills/rainbow/bin/rainbow-tool-exec" | grep -q .; then
  if grep -r "skills/rainbow/output/" skills/ docs/ AGENTS.md 2>/dev/null | grep -q .; then
    echo "ERROR: Partial migration state detected: bash script present AND old paths present"
    exit 1
  fi
fi
```

---

### VULN-007: Old Bash Script Path Resolution via Symlink After Deletion (LOW)

**Severity:** LOW
**CWE:** CWE-61 UNIX Symbolic Link Following
**CVSS 3.1 Base Score:** 2.5 (AV:L/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N)
**ATT&CK Technique:** T1574.010 (Hijack Execution Flow: Services File Permissions Weakness)
**Exploit Availability:** Requires local write access to the `skills/rainbow/bin/` directory; theoretical

**Description:**

After `EN-W12-001` deletes `skills/rainbow/bin/rainbow-tool-exec`, any external script, CI step, or Docker bind mount that still references the old path will receive a `FileNotFoundError` (or the bind mount will silently fail). However:

1. If the directory `skills/rainbow/bin/` is not deleted, an attacker with local filesystem write access could create a symlink at `skills/rainbow/bin/rainbow-tool-exec` pointing to an arbitrary executable. Any remaining reference to the old path would execute the attacker's binary.

2. If Docker bind mounts include `skills/rainbow/bin:/usr/local/bin` (volume-style exposure rather than individual file mounts), the entire `bin/` directory is exposed in the container, and any attacker-created file in that directory is executable inside containers.

3. The git status output in this engagement shows `skills/rainbow/bin/rainbow-tool-exec` as deleted (`D skills/rainbow/bin/rainbow-tool-exec`), confirming the file has already been removed. The risk applies if the directory itself persists in the repository tree.

**Code-Level Mitigation:**

As part of `EN-W12-001`, also remove the `skills/rainbow/bin/` directory from the repository (not just the file). If the directory must be retained for other content, add a `.gitkeep` file and a `README` that documents the directory is now empty and the script has been migrated to `jerry tool exec`.

In CI, verify that no bind mount entry in any `docker-compose.yml` under `skills/` references `skills/rainbow/bin/`:

```bash
grep -r "skills/rainbow/bin" skills/*/tests/docker/
```

This should return 0 results after migration.

---

## L2 Strategic Implications

### Attack Path Analysis: Proxy Trust Boundary Exploitation

The proxy injection feature creates a new trust boundary: the ContainerExecutor previously had no network-level constraints; after the change, it enforces zone-specific egress routing through Envoy. This trust boundary is only as strong as the proxy URL's integrity.

**Multi-step attack chain (VULN-001 + VULN-002):**

```
[Attacker with engagement init access]
        |
        v
Step 1: Submit crafted --scope-file with malicious authorized_targets
        |
        v
Step 2: generate_envoy_config() writes attacker-controlled Envoy upstream routes
        |
        v
Step 3: Operator initializes engagement with scope file; Envoy config is persisted
        |
        v
Step 4: Operator executes Zone 2 tool (e.g., nuclei, subfinder)
        |
        v
Step 5: ContainerExecutor injects -e HTTP_PROXY=http://envoy-z2:3128
        |
        v
Step 6: Container routes tool traffic through Envoy
        |
        v
Step 7: Envoy proxies to attacker-controlled upstream (due to crafted routes)
        |
        v
IMPACT: Tool output (target responses, discovered assets, credentials)
        exfiltrates through attacker-controlled proxy
        -- bypasses Python credential filter at the network layer
```

This chain bypasses the credential filter because the filter operates on subprocess stdout/stderr, not on HTTP response bodies. A reconnaissance tool that writes discovered credentials to stdout will still be filtered, but credentials embedded in HTTP responses that the tool processes internally (e.g., a Nuclei template that captures auth tokens in its output JSON) may not be fully sanitized.

**Fail-open chain (VULN-003):**

```
[Attacker on Docker host]
        |
        v
Step 1: Stop Envoy container before tool execution
        docker stop envoy-z2
        |
        v
Step 2: Operator triggers Zone 2 tool execution (unaware proxy is down)
        |
        v
Step 3: ContainerExecutor injects -e HTTP_PROXY=http://envoy-z2:3128
        but Envoy is not listening
        |
        v
Step 4: Container tool fails to connect to proxy, falls back to direct routing
        (tool-dependent; many HTTP clients fall back silently)
        |
        v
IMPACT: Zone 2 traffic exits via container's default network interface
        -- scope boundary violated silently
        -- no indication in logs that proxy routing failed
```

### Threat Model Gap: Proxy as Security Control vs. Convenience

The current architecture treats Envoy proxies as a convenience (zone-specific egress routing) with no formal fail-safe behavior specified. The proposed T13-021/T13-022 change elevates the proxy to a security control (network-level enforcement of engagement scope). This architectural transition requires:

1. **Explicit fail-closed semantics** for Zone 2/3 (VULN-003 mitigation).
2. **Proxy integrity validation** -- the URL must be statically derived, not from user input (VULN-001 mitigation).
3. **Documentation in zone-3-exploit.md and zone-2-active.md** of the proxy dependency and its security role.
4. **Pre-execution proxy health check** as a mandatory gate, not an informational check.

The current `health_check()` method returns `bool` and its return value is not checked by `_execute_container()`. This means even if a health check were called before execution, the absence of a mandatory gate means the check is advisory only. The fix requires adding the mandatory `_assert_proxy_available()` call inside `execute()` itself.

### Risk Scoring Summary

| ID | Finding | CVSS | Exploitability | Impact | Priority |
|----|---------|------|----------------|--------|----------|
| VULN-001 | Proxy URL injection via scope file | 7.4 | Medium (requires scope file access) | HIGH (traffic exfiltration) | P1 |
| VULN-002 | exec_flags injection override | 7.1 | Medium (requires caller access) | HIGH (proxy bypass) | P1 |
| VULN-003 | Fail-open on Envoy down | 6.9 | High (stop container) | HIGH (scope bypass) | P1 |
| VULN-004 | NO_PROXY bypass injection | 5.3 | Low (VULN-002 prereq) | MEDIUM (partial bypass) | P2 |
| VULN-005 | Proxy URL in process args | 4.7 | Low (local access) | MEDIUM (credential leak if URL gains creds) | P2 |
| VULN-006 | Dual-invocation migration window | 3.1 | Low (timing attack) | LOW (output exposure) | P3 |
| VULN-007 | Symlink after bash deletion | 2.5 | Very low (write access) | LOW (execution hijack) | P3 |

### Prioritization for Engineering Remediation (eng-team handoff)

**Before T13-021/T13-022 are merged:**

- P1 items (VULN-001, VULN-002, VULN-003) MUST be addressed in the same PR as the proxy injection feature. They are architectural design flaws in the proposed change, not implementation bugs in existing code.
- VULN-001: Add `_ENVOY_PROXY_HOSTS` constant dict; derive URL from zone integer only.
- VULN-002: Add `_validate_exec_flags()` allowlist check rejecting `-e`/`--env` prefixes.
- VULN-003: Add `_assert_proxy_available()` with fail-closed for Zone 2/3; fail-open for Zone 1.
- VULN-004: Compile `NO_PROXY` statically into `_proxy_env_flags()`.

**During STORY-W12-002 execution:**

- VULN-006: Enforce atomic migration; add CI guard against partial migration state.

**During EN-W12-001 execution:**

- VULN-007: Remove `skills/rainbow/bin/` directory; verify no docker-compose bind mounts reference it.

### Engagement Objectives Alignment

This analysis focused exclusively on the architectural design vulnerability surface introduced by the proxy injection change and the migration. No active exploitation was performed or is within scope. All findings are based on static code analysis of:

- `/src/tool_exec/infrastructure/adapters/container_executor.py`
- `/src/interface/cli/tool_exec_commands.py`
- `/skills/rainbow/config/tool-exec.yaml`
- `/skills/rainbow/SKILL.md`
- `/skills/rainbow/rules/zone-3-exploit.md`
- `/projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/EN-W12-001-delete-bash/EN-W12-001.md`
- `/projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/STORY-W12-002-output-paths/STORY-W12-002.md`

---

## Evidence and Citations

| Finding | Source Code Location | Line Reference |
|---------|---------------------|---------------|
| VULN-001 | `tool_exec_commands.py` `_generate_envoy_configs()` | Lines 796-834 |
| VULN-001 | `tool_exec_commands.py` `_handle_init_engagement()` | Lines 782-784 |
| VULN-002 | `container_executor.py` `_build_command()` | Lines 258-259 |
| VULN-002 | `container_executor.py` `execute()` | Line 110 |
| VULN-003 | `container_executor.py` `health_check()` | Lines 203-231 |
| VULN-003 | `tool_exec_commands.py` `_execute_container()` | Lines 1286-1297 |
| VULN-004 | `container_executor.py` `_build_command()` | Lines 253-263 |
| VULN-005 | `container_executor.py` `execute()` | Lines 113-119 |
| VULN-006 | EN-W12-001 acceptance criteria | EN-W12-001.md lines 95-97 |
| VULN-007 | Git status: `D skills/rainbow/bin/rainbow-tool-exec` | Engagement context |

---

*Agent: red-vuln*
*Constitutional Compliance: P-001 (evidence-based), P-002 (output persisted), P-003 (no recursive subagents), P-020 (user authority), P-022 (no deception)*
*Engagement: RED-W13-002*
*Output: /skills/red-team/output/RED-W13-002/red-vuln-proxy-wiring-review.md*
*Created: 2026-03-19*
