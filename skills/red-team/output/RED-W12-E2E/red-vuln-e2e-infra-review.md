# Vulnerability Analysis: E2E Test Infrastructure
## Engagement: RED-W12-E2E

| Field | Value |
|-------|-------|
| Engagement ID | RED-W12-E2E |
| Analyst | red-vuln |
| Phase | Vulnerability Analysis |
| Scope | E2E test infrastructure -- 6 Docker compose clusters with Envoy proxies |
| Date | 2026-03-19 |
| Status | Complete |

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Severity counts, overall posture, key risk |
| [L1 Technical Findings](#l1-technical-findings) | Six findings with CVEs, CVSS, exploit availability |
| [L2 Strategic Implications](#l2-strategic-implications) | Attack path analysis, chains, recommendations |
| [Evidence Basis](#evidence-basis) | Source files reviewed |

---

## L0 Executive Summary

### Vulnerability Count by Severity

| Severity | Count |
|----------|-------|
| HIGH | 2 |
| MEDIUM | 3 |
| LOW | 1 |
| **Total** | **6** |

### Overall Risk Posture

**MEDIUM-HIGH.** The E2E test infrastructure has a sound architectural foundation. Network zone isolation is structurally correct (Docker `internal: true` + Envoy deny-by-default) and multiple security gates exist at the CLI layer. However, three design-level weaknesses create meaningful test-integrity risk and one creates a genuine blast-radius concern in shared CI environments. The highest priority finding (F-001) has no mitigation in the current conftest implementation.

### Top Exploitable Findings

1. **F-001 (HIGH):** No Docker compose project name isolation -- parallel CI jobs share container and network names, enabling cross-session traffic interception and false test results.
2. **F-002 (HIGH):** Stale containers from failed teardown can persist with active Envoy configs from prior engagements, causing Zone 2 tests to verify the wrong scope.
3. **F-004 (MEDIUM):** Neo4j ports 7474/7687 bound to `0.0.0.0` on the host -- accessible from the host network during test runs, not isolated to the Docker bridge.

### Key Recommendation

Add `COMPOSE_PROJECT_NAME` isolation per test session. This single change mitigates F-001 entirely and reduces the severity of F-002. All other mitigations are incremental.

---

## L1 Technical Findings

### F-001: Compose Project Name Collision in Parallel CI

| Attribute | Value |
|-----------|-------|
| Severity | HIGH |
| CVSS v3.1 Base | AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H -- 8.2 (High) |
| CWE | CWE-362 Race Condition / CWE-610 Externally Controlled Reference |
| ATT&CK | T1484.002 (Domain Trust Modification -- analogous: resource hijack in shared infra) |
| Exploit Availability | No public PoC required; reproducible with standard Docker CLI |
| Affected Files | `tests/e2e/tool_exec/conftest.py`, `skills/rainbow-supply-chain/tests/docker/docker-compose.yml`, `tests/e2e/tool_exec/test_envoy_proxy.py` |

**Description**

No compose project name is set anywhere in the conftest or compose files. Docker Compose derives the project name from the containing directory name by default. When two CI jobs run concurrently from the same checkout (e.g., two parallel pytest workers or two branches building at the same time on the same agent), both sessions will resolve to the same project name (`docker` or the directory basename). This means:

- Container names from `docker-compose.full.yml` are hardcoded (e.g., `container_name: rainbow-supply-chain`, `container_name: rainbow-neo4j`). Two concurrent sessions will attempt to create containers with identical names. Docker will refuse to start the second session's containers, causing test failures on the second runner.
- Network names (`zone1-offline`, `zone1-update`, `zone1-egress`, `zone2-active`, `zone2-egress`, etc.) are also shared. A stale network from session A may be picked up as a dependency by session B's `docker compose up`.
- The `_ensure_envoy_z2_restarted` fixture in `test_envoy_proxy.py` stops `envoy-z2` by name. If session A's test is stopping envoy-z2 while session B's test depends on it being healthy, session B will receive unexpected `CONTAINER_NOT_RUNNING (3)` errors, generating false negatives.

**Verification**

```bash
# Observe identical project names from two separate invocations:
docker compose -f skills/rainbow-supply-chain/tests/docker/docker-compose.yml \
  config --format json | jq '.name'
# Returns the same value regardless of invocation; no session-unique identifier
```

**Mitigation**

Pass a session-unique project name via `COMPOSE_PROJECT_NAME` environment variable or the `-p` flag in every `subprocess.run` call within `docker_compose_up` and `_compose_up`:

```python
import uuid
_SESSION_ID = str(uuid.uuid4())[:8]

# In conftest.py docker_compose_up fixture:
subprocess.run(
    ["docker", "compose", "-p", f"jerry-e2e-{_SESSION_ID}",
     "-f", compose_path, "build", "--quiet"],
    ...
)
```

The session ID must be propagated to all compose operations in the session (build, up, down, exec, stop, start) using a session-scoped fixture variable. The `_SUPPLY_CHAIN_COMPOSE` constant in `test_envoy_proxy.py` must also receive the project name for its module-scoped cluster fixture.

---

### F-002: Stale Containers Pollute Subsequent Test Sessions

| Attribute | Value |
|-----------|-------|
| Severity | HIGH |
| CVSS v3.1 Base | AV:L/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:L -- 7.0 (High) |
| CWE | CWE-459 Incomplete Cleanup |
| ATT&CK | T1036 (Masquerading -- stale Envoy config from prior engagement masquerades as current) |
| Exploit Availability | Exploitable by test crash (no attacker required) |
| Affected Files | `tests/e2e/tool_exec/conftest.py` (lines 133-146), `skills/rainbow/config/envoy/envoy-zone2-active.yaml` |

**Description**

The `docker_compose_up` teardown runs `docker compose down --volumes --remove-orphans`. This call has no `check=True` argument (line 134 of conftest.py). If `docker compose down` fails (due to a Python exception, pytest crash, SIGKILL of the test process, or OOM on the CI runner), the containers, networks, and named volumes continue to exist.

The specific risk for security testing:

1. **Zone 2 Envoy config state:** `envoy-zone2-active.yaml` is mounted read-only into the envoy-z2 container. This file is modified by `jerry tool exec --init-engagement` to inject scope targets. If a prior test session called `--init-engagement` and then crashed before teardown, the next session's Zone 2 tests begin with a non-default Envoy config that already contains authorized targets from the prior engagement. `TestZone2DenyAll.test_zone2_default_denies_all` validates the config file on disk, but the running container may have the stale config in memory or the config file may have been left modified.

2. **Engagement directory persistence:** The `engagement_cleanup` fixture uses `shutil.rmtree(eng_dir, ignore_errors=True)` for cleanup. If the test that appended the engagement ID to the cleanup list crashes before the fixture yield completes, the cleanup never runs. The `work/engagements/E2E-TEST-001` directory used by `test_fail_closed_when_envoy_z2_stopped` (line 750 of test_envoy_proxy.py) is referenced as "assumed to exist" from the broader E2E run. If a prior run left this directory from a crash, the test passes based on prior session state rather than current session initialization.

3. **Named volumes (`envoy-z1-logs`, `envoy-z2-logs`, `envoy-z3-logs`, `msf-pgdata`, `neo4j-data`) are removed by `--volumes` but only if `down` succeeds.** A surviving log volume from a prior session may contain Envoy access logs that are stale, causing `TestEnvoyAccessLogLive.test_access_log_is_json` to pass because it finds log entries from a previous run, not the current one.

**Mitigation**

1. Add `check=False` explicitly (current behavior) but add a pre-session cleanup step that runs `docker compose down --volumes --remove-orphans` before `up`, not just after. This acts as a fence against leftover state.
2. Use session-unique project names (see F-001 mitigation) -- this eliminates cross-session container reuse by design.
3. Add an explicit `os.remove` or config reset step for `envoy-zone2-active.yaml` at session start, restoring it to the canonical deny-all default before any engagement init.
4. The `test_fail_closed_when_envoy_z2_stopped` test must explicitly call `--init-engagement E2E-TEST-001` rather than relying on a shared assumption that the engagement exists.

---

### F-003: Engagement Directory Pollution Across Sessions

| Attribute | Value |
|-----------|-------|
| Severity | MEDIUM |
| CVSS v3.1 Base | AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L -- 6.1 (Medium) |
| CWE | CWE-459 Incomplete Cleanup / CWE-362 Race Condition |
| ATT&CK | T1070.004 (Indicator Removal: File Deletion -- inverted: failure to remove indicators affects test integrity) |
| Exploit Availability | Triggered by CI interruption; no external attacker required |
| Affected Files | `tests/e2e/tool_exec/conftest.py` (engagement_cleanup fixture, lines 282-301), `tests/e2e/tool_exec/test_engagement_lifecycle.py` |

**Description**

The `engagement_cleanup` fixture yields a mutable list and deletes engagement directories after the test returns. This cleanup runs only if:

- The test function returns (passes or raises an exception that pytest catches normally).
- The fixture teardown is not interrupted.

It does not run if pytest is SIGKILL'd, or if the test process is killed by the CI runner's timeout enforcement. The engagement directories are created under `work/engagements/` in the real project checkout.

The specific test-integrity risk:

- `test_init_is_idempotent` (test_engagement_lifecycle.py lines 127-153) verifies that a second `--init-engagement` call on the same ID preserves the original `created_at`. If `E2E-TEST-L007` already exists from a prior session, the test passes because the first call is actually the "second call" and the write-once DR-010 logic correctly preserves the timestamp -- but the test is not verifying what it claims to verify (that the current session correctly initializes and then protects the directory).

- More critically: `test_zone3_approval` and `test_fail_closed_when_envoy_z2_stopped` reference `E2E-TEST-001` as a pre-existing engagement. If this directory exists from a prior session with different scope content (different `envoy-zone2-active.yaml` targets), Zone 2 tests may behave differently than expected without any visible test failure signal.

**Note on existing mitigation:** The `E2E-TEST-` prefix convention documented in the conftest (line 17) is a good practice. It enables targeted pre-session cleanup scripts. The gap is that no such pre-session cleanup is implemented.

**Mitigation**

1. Add a session-scoped autouse fixture that runs before `docker_compose_up` and cleans all `work/engagements/E2E-TEST-*` directories unconditionally:

```python
@pytest.fixture(scope="session", autouse=True)
def pre_session_engagement_cleanup(project_root: Path) -> None:
    """Remove all E2E test engagement directories before the session starts."""
    import glob
    for d in glob.glob(str(project_root / "work" / "engagements" / "E2E-TEST-*")):
        shutil.rmtree(d, ignore_errors=True)
```

2. This fixture must be ordered before `docker_compose_up` using `pytest-order` or by placing it first in the conftest. Alternatively, include it in `docker_guard` since that fixture is already the session entry gate.

---

### F-004: Neo4j Ports Exposed on Host Network Interface

| Attribute | Value |
|-----------|-------|
| Severity | MEDIUM |
| CVSS v3.1 Base | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N -- 8.2 (High) without network controls; environment-adjusted to Medium for isolated CI |
| CWE | CWE-284 Improper Access Control |
| ATT&CK | T1046 (Network Service Discovery), T1078 (Valid Accounts -- default credentials) |
| Exploit Availability | CVE-2023-23926 (Neo4j path traversal, CVSS 7.5), default credentials trivially exploitable |
| Affected Files | `skills/rainbow/tests/docker/docker-compose.full.yml` (lines 205-213), `skills/rainbow/tests/docker/docker-compose.base.yml` (lines 196-210) |

**Description**

Both `docker-compose.base.yml` and `docker-compose.full.yml` bind Neo4j ports directly to the host:

```yaml
ports:
  - "7474:7474"   # HTTP API + web console
  - "7687:7687"   # Bolt protocol
```

No host IP binding restriction is specified (e.g., `127.0.0.1:7474:7474`). This means Neo4j is reachable on all host interfaces. The default test credentials are hardcoded as `NEO4J_AUTH: "neo4j/test-only-not-real"` -- this value is committed to source and visible in CI logs.

Risk factors:

1. **Default credentials:** The password `test-only-not-real` is committed in plaintext in two compose files. Any process with network access to the CI runner can authenticate to Neo4j using these credentials during a test run.
2. **Neo4j web console (port 7474):** The browser-based admin console is reachable without additional authentication beyond the committed credentials. An attacker with host network access can execute arbitrary Cypher queries.
3. **Scope for the engagement:** This is a test environment running `rainbow-cloud` tools that perform cloud security assessments. If graph data from prior cloud scans (account IDs, resource ARNs, IAM configurations) is stored in Neo4j and the database persists across runs (via the `neo4j-data` named volume), sensitive infrastructure details are accessible to any process with host network access.

**Note on environment context:** In a properly isolated CI environment (no external network access to the runner), this is a configuration weakness rather than an immediately exploitable remote vulnerability. On a developer's workstation or on a CI runner that accepts inbound connections, the risk is materially higher.

**Mitigation**

Restrict port bindings to loopback only, and replace the hardcoded password with a dynamically generated ephemeral credential:

```yaml
ports:
  - "127.0.0.1:7474:7474"
  - "127.0.0.1:7687:7687"
environment:
  NEO4J_AUTH: "neo4j/${NEO4J_TEST_PASSWORD:-neo4j-test-$(openssl rand -hex 12)}"
```

Alternatively, remove the port bindings entirely -- the `rainbow-cloud` container service connects to Neo4j via the `rainbow-isolated`/`rainbow-net` Docker bridge network where Neo4j is resolvable by service name without host port exposure.

---

### F-005: Host Network Behavior Observation During Network Isolation Tests

| Attribute | Value |
|-----------|-------|
| Severity | MEDIUM |
| CVSS v3.1 Base | AV:L/AC:H/PR:L/UI:R/S:C/C:L/I:L/A:N -- 4.4 (Medium) |
| CWE | CWE-290 Authentication Bypass by Spoofing / CWE-345 Insufficient Verification |
| ATT&CK | T1040 (Network Sniffing -- test verifies container behavior but host may bypass isolation) |
| Exploit Availability | Requires specific CI network topology; not remotely exploitable |
| Affected Files | `tests/e2e/tool_exec/test_envoy_proxy.py` (TestBypassDetection class, lines 468-526) |

**Description**

The `TestBypassDetection` tests verify that containers cannot reach the internet even without proxy environment variables. The tests assert `rc != 0` when `curl --noproxy '*'` is run inside the container. This is structurally sound because Docker `internal: true` networks have no default gateway.

However, the Envoy health check assertion in `test_envoy_is_only_egress_path` (lines 509-526) has a logical gap:

```python
assert rc_proxy != 0 or rc_listener == 0, "Cannot reach Envoy at all on internal network"
```

This assertion passes if *either* condition is true: (a) the admin port is unreachable (expected), OR (b) the proxy listener is reachable. If both fail (admin unreachable AND proxy unreachable), the assertion still passes because `rc_proxy != 0` is True. This means a completely broken Envoy container would still cause the test to pass -- the test does not verify that `rc_listener == 0` (proxy is functional), only that at least one condition holds.

The deeper structural issue: all `_compose_exec` calls route through `docker compose exec`, which uses the Docker daemon socket. The Docker daemon runs on the host. If the host has network access to the external internet and the Docker daemon's network namespace allows host routing, a misconfigured container could theoretically exit the internal network by exploiting a Docker bridge routing misconfiguration at the host level. The tests cannot distinguish between "container is isolated" and "host network topology prevents routing" -- they verify the functional outcome but not the mechanism.

This is a test-design vulnerability (testing the right thing for the wrong reason) rather than a production security flaw in the container topology itself.

**Mitigation**

1. Fix the logical gap in `test_envoy_is_only_egress_path`:

```python
# Verify proxy listener IS reachable (not just that one of two conditions holds)
assert rc_listener == 0, (
    "Envoy proxy listener on :3128 is unreachable from internal network -- "
    "structural isolation may be broken"
)
```

2. Add an explicit test that verifies the container's routing table has no default gateway on the internal network:

```python
rc, stdout, _ = _compose_exec(
    _SUPPLY_CHAIN_COMPOSE, "scanner",
    ["ip", "route", "show", "default"]
)
assert stdout.strip() == "", "Offline container has a default route -- isolation broken"
```

---

### F-006: Subprocess Tool Output Captured and Persisted Without Entropy-Based Secret Detection

| Attribute | Value |
|-----------|-------|
| Severity | LOW |
| CVSS v3.1 Base | AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N -- 2.5 (Low) |
| CWE | CWE-312 Cleartext Storage of Sensitive Information |
| ATT&CK | T1552.001 (Credentials In Files) |
| Exploit Availability | Requires CI log access; mitigated by existing credential filter |
| Affected Files | `src/tool_exec/domain/services/credential_filter.py`, `src/tool_exec/infrastructure/adapters/container_executor.py` |

**Description**

The credential filter in `CredentialFilterService` applies 15 regex patterns covering known credential formats (AWS keys, API tokens, private key headers, etc.). This is a solid implementation. The gap is that tools like prowler, kubescape, and impacket can produce output containing high-entropy strings that do not match any known pattern but are nonetheless secrets (e.g., Azure SAS tokens, custom HMAC signatures, cloud provider temporary session tokens with non-standard prefixes).

The `_BASE_CS_PATTERNS` list (lines 68-85 of credential_filter.py) is pattern-based with no entropy scoring component. The configuration at the base compose level acknowledges this with `CREDENTIAL_FILTER_ENTROPY_THRESHOLD: "4.5"` and `CREDENTIAL_FILTER_MIN_STRING_LENGTH: "16"` in `docker-compose.base.yml` and `docker-compose.full.yml`, but these environment variables are defined in the compose template and there is no implementation in `CredentialFilterService` that reads or uses these values. They are present in the environment of the tool containers, not the filter service, and there is no code path that consumes them.

**Verification**

```bash
grep -r "CREDENTIAL_FILTER_ENTROPY" \
  src/tool_exec/domain/services/credential_filter.py
# No results -- entropy threshold is not implemented
```

**Mitigation (MEDIUM priority, LOW severity):** Implement Shannon entropy scoring for high-entropy tokens in the sliding-window scan. A token exceeding 4.5 bits/char with length >= 16 should trigger the filter. This closes the gap between the declared configuration intent (`CREDENTIAL_FILTER_ENTROPY_THRESHOLD`) and the actual implementation. This is a defense-in-depth improvement, not a critical fix, because the regex patterns cover the most common credential formats already.

---

## L2 Strategic Implications

### Attack Path 1: Parallel CI Job Cross-Contamination (F-001 + F-002 Chain)

```
CI Trigger (branch push)
    |
    +-- Job A starts: docker compose up (project name = "docker")
    |       containers: rainbow-supply-chain, envoy-z1-update, ...
    |
    +-- Job B starts concurrently: docker compose up (SAME project name)
            container_name: rainbow-supply-chain (CONFLICT -- Docker rejects)
            OR Job B reuses Job A's running containers
            |
            +-- test_can_reach_github_via_proxy (Job B)
            |   Routes through Job A's Envoy container
            |   Envoy has Job A's in-memory state
            |   Test passes because network works, but tests Job A's infrastructure
            |
            +-- test_fail_closed_when_envoy_z2_stopped (Job B)
                Job B stops envoy-z2 -- this is Job A's envoy-z2
                Job A's zone 2 tests now fail with CONTAINER_NOT_RUNNING (3)
                Both jobs fail for reasons unrelated to code under test
```

**ATT&CK Mapping:** T1484.002 (analogous: trust modification in shared resource). This attack path does not require an external attacker -- it is triggered by normal CI parallelism.

**Exploitation Conditions:** Two CI jobs running on the same agent with the same compose project name. Reproducible deterministically. The `container_name` hardcoding in `docker-compose.full.yml` makes it guaranteed to fail on the second job rather than silently contaminating (Docker rejects duplicate container names), but the `docker-compose.yml` files for individual skills do not use `container_name`, making contamination silent there.

### Attack Path 2: Stale Engagement Scope Bypasses Zone 2 Deny-All Test (F-002 + F-003 Chain)

```
Test Session 1 (crashes mid-run):
    --init-engagement E2E-TEST-001
    scope_translator.py writes targets to envoy-zone2-active.yaml
    Session crashes before teardown
    envoy-zone2-active.yaml left in modified state (has authorized targets)
    work/engagements/E2E-TEST-001/ directory persists

Test Session 2 (next run):
    TestZone2DenyAll.test_zone2_default_denies_all
        reads envoy-zone2-active.yaml from disk
        finds authorized targets (left by Session 1)
        ASSERTION FAILS: len(virtual_hosts) != 1
        -- OR --
        new session re-initializes the config via --init-engagement
        but E2E-TEST-001 already exists with Session 1's created_at
        DR-010 write-once logic preserves Session 1's metadata
        test_init_is_idempotent passes based on Session 1's timestamp
        -- SESSION 2 IS TESTING SESSION 1'S STATE --
```

This path produces **false negative security results**: the Zone 2 deny-all test either fails (making the developer think the security control is broken) or passes while validating the wrong config state (making the developer think the current session is clean when it is not).

### Attack Path 3: Docker Socket Blast Radius (Defensive Context)

The test conftest runs `docker compose` commands via `subprocess.run`. The test process has implicit access to the Docker daemon socket (`/var/run/docker.sock`). This is intentional and required. The blast radius assessment:

- **Scope within normal operation:** The test process can start, stop, and manipulate any container on the host. This is acceptable for a trusted developer workstation.
- **CI scope concern:** If the CI runner uses a shared Docker daemon (not Docker-in-Docker isolation), a compromised test or a dependency in the supply chain (e.g., a malicious `uv` package) could manipulate other teams' containers on the shared runner. The existing supply chain tools (Syft, Grype) scan for this class of risk -- a recursive application of the security tooling to the test infrastructure itself.
- **Mitigation for CI:** Use Docker-in-Docker (`docker:dind`) or a dedicated agent per job. This is an infrastructure decision outside the conftest scope but worth noting given that the project explicitly builds and runs exploitation tools (Zone 3: Metasploit, Empire, Impacket).

### Priority Remediation Order

| Priority | Finding | Effort | Impact |
|----------|---------|--------|--------|
| 1 | F-001: Add `COMPOSE_PROJECT_NAME` session isolation | Low (2-4 hours) | Eliminates parallel CI contamination chain |
| 2 | F-003: Pre-session engagement directory cleanup fixture | Low (1 hour) | Eliminates stale engagement state |
| 3 | F-002: Add `check=False` fence + pre-session compose down | Low (2 hours) | Reduces stale container impact |
| 4 | F-005: Fix `test_envoy_is_only_egress_path` logical gap | Low (30 min) | Improves isolation test fidelity |
| 5 | F-004: Restrict Neo4j port bindings to `127.0.0.1` | Low (30 min) | Reduces host network exposure |
| 6 | F-006: Implement entropy-based credential scoring | Medium (4-8 hours) | Defense-in-depth for unknown credential formats |

### Engagement Objective Alignment

This infrastructure is the test harness for a security-sensitive toolkit (offensive tools: Metasploit, Empire, Impacket; defensive tools: YARA-X, Trivy, Ghidra). Test infrastructure integrity directly affects the trustworthiness of security control validation. F-001 and F-002 are particularly significant because they can cause the network isolation tests (Zone 1/2/3 Envoy enforcement) to report false passes -- meaning the test suite could assert that exploitation tools are properly isolated when they are not, which defeats the entire security testing purpose of the test suite.

The two HIGH findings should be treated as security defects in the test infrastructure itself, not merely as reliability issues.

---

## Evidence Basis

| File | Lines Reviewed | Finding Support |
|------|----------------|-----------------|
| `tests/e2e/tool_exec/conftest.py` | 1-302 | F-001, F-002, F-003 |
| `tests/e2e/tool_exec/test_envoy_proxy.py` | 1-760 | F-001, F-002, F-005 |
| `tests/e2e/tool_exec/test_engagement_lifecycle.py` | 1-232 | F-003 |
| `tests/e2e/tool_exec/test_error_paths.py` | 1-177 | F-003 (reference) |
| `tests/e2e/tool_exec/test_exploit.py` | 1-326 | F-001 (zone 3 gates) |
| `skills/rainbow-supply-chain/tests/docker/docker-compose.yml` | 1-108 | F-001, F-002 |
| `skills/rainbow-recon/tests/docker/docker-compose.yml` | 1-73 | F-001, F-002 |
| `skills/rainbow-exploit/tests/docker/docker-compose.yml` | 1-155 | F-001, F-004 (postgres) |
| `skills/rainbow/tests/docker/docker-compose.base.yml` | 1-228 | F-004, F-006 |
| `skills/rainbow/tests/docker/docker-compose.full.yml` | 1-324 | F-001, F-004 |
| `skills/rainbow/config/envoy/envoy-zone1-update.yaml` | 1-167 | F-002, F-005 |
| `skills/rainbow/config/envoy/envoy-zone2-active.yaml` | 1-110 | F-002, F-005 |
| `src/tool_exec/domain/services/credential_filter.py` | 1-400 | F-006 |
| `src/tool_exec/infrastructure/adapters/container_executor.py` | 1-302 | F-006 (reference) |
| `src/tool_exec/domain/services/engagement_initializer.py` | 1-256 | F-003 (reference) |

---

## Analyst Notes

**Coverage Feedback Envelope:** No CFE from /blue-team was available for this engagement. Standard CVSS + exploitability scoring applied per Graceful Degradation protocol. ATT&CK technique mappings are best-effort without detection coverage context.

**Methodology:** PTES Vulnerability Analysis phase. OWASP Testing Guide OTG-CONFIG-002 (Application Platform Configuration), OTG-CONFIG-004 (Network/Infrastructure Configuration). Manual code review of conftest.py, compose files, and supporting implementation; no active scanning performed.

**Scope Compliance:** Analysis is read-only. No exploit attempts. No container manipulation. Findings are based entirely on static analysis of source files.

---

*Agent: red-vuln v1.0.0*
*Engagement: RED-W12-E2E*
*Generated: 2026-03-19*
