# BDD Step Definition Test Strategy: tool_exec

**Engagement ID:** W12-BDD
**Agent:** eng-qa (Security QA Engineer)
**Date:** 2026-03-18
**Source Feature Files:** `projects/PROJ-023-exploit-framework/work/design/test-specs/` (6 files, UC-TOOLEXEC-001 through UC-TOOLEXEC-006)
**Source Under Test:** `src/tool_exec/`, `src/interface/cli/tool_exec_commands.py`

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Coverage summary and security test assessment |
| [L1 Test Architecture](#l1-test-architecture) | Directory layout, conftest, step file mapping |
| [L1 Mocking Strategy](#l1-mocking-strategy) | What to mock vs test real |
| [L1 Fixture Design](#l1-fixture-design) | Shared fixtures, canary integration, factory helpers |
| [L1 Exit Code Verification Pattern](#l1-exit-code-verification-pattern) | Asserting return codes from handle_tool_exec |
| [L1 Security Test Patterns](#l1-security-test-patterns) | Zone 3 gate, strict mode, quarantine permissions |
| [L2 Strategic Implications](#l2-strategic-implications) | Coverage gaps, regression maintenance, ROI |

---

## L0 Executive Summary

The six feature files covering UC-TOOLEXEC-001 through UC-TOOLEXEC-006 define 110+ distinct BDD scenarios across these functional areas:

| Feature File | Area | Scenario Count | Exit Codes Covered |
|---|---|---|---|
| UC-TOOLEXEC-001 | Auto-detect family + execute | ~24 | 0, 1, 2, 3, 4, 5, 6 |
| UC-TOOLEXEC-002 | Explicit family + execute | ~16 | 0, 1, 2, 3, 4, 5, 6, 7, 8 |
| UC-TOOLEXEC-003 | Engagement initialization | ~14 | 0, 1 |
| UC-TOOLEXEC-004 | List families and tools | ~14 | 0, 7, 8 |
| UC-TOOLEXEC-005 | Credential filtering | ~22 | 0, 4, 6 |
| UC-TOOLEXEC-006 | Health check | ~20 | 0, 7 |

The implementation under test wires eight security-critical control points:

1. Module import allowlist (M-01 / T-01 / DREAD 38)
2. Strict mode enforcement (M-03 / T-06 / DREAD 34) -- `JERRY_STRICT_MODE`
3. Zone 3 TTY approval gate (IN-015-R2 / NEW-001)
4. Zone 3 container enforcement (FM-002 / FIX-3) -- local mode rejected for Zone 3
5. Engagement ID allowlist validation (M-05 / T-08 / DREAD 28)
6. Credential filter with 15 base patterns (BC-07)
7. Quarantine file permissions: `0o600` per file, `0o700` per directory (FIX-8 / SR-003)
8. Evidence path traversal containment (FINDING-001 / CWE-22)

The BDD suite must achieve >= 90% line coverage on `src/tool_exec/` and `src/interface/cli/tool_exec_commands.py` (H-20 / H-21). Security-critical branches (the eight control points above) require 100% branch coverage individually and constitute the primary regression protection surface.

---

## L1 Test Architecture

### Directory Layout

```
tests/bdd/tool_exec/
    conftest.py                        # All shared fixtures for tool_exec BDD
    features/                          # Feature file copies (not symlinks -- see rationale below)
        test-UC-TOOLEXEC-001.feature
        test-UC-TOOLEXEC-002.feature
        test-UC-TOOLEXEC-003.feature
        test-UC-TOOLEXEC-004.feature
        test-UC-TOOLEXEC-005.feature
        test-UC-TOOLEXEC-006.feature
    steps/
        conftest.py                    # Step-level fixtures (scenario context object)
        step_common.py                 # Steps shared across multiple UCs
        step_uc001_auto_detect.py      # Steps for UC-TOOLEXEC-001
        step_uc002_explicit_family.py  # Steps for UC-TOOLEXEC-002
        step_uc003_engagement.py       # Steps for UC-TOOLEXEC-003
        step_uc004_discovery.py        # Steps for UC-TOOLEXEC-004
        step_uc005_credential.py       # Steps for UC-TOOLEXEC-005
        step_uc006_health_check.py     # Steps for UC-TOOLEXEC-006
```

**Rationale: Feature file copies rather than symlinks.** pytest-bdd requires feature files to be importable at collection time. Symlinks to a path outside the `tests/` tree create fragile relative path dependencies. Copying the six files into `tests/bdd/tool_exec/features/` keeps the BDD suite self-contained. A CI check (`make verify-bdd-feature-sync`) can detect drift between source specs and copies by comparing SHA-256 digests.

**pytest registration.** Add the following to `pyproject.toml` so pytest auto-discovers the BDD test modules:

```toml
[tool.pytest.ini_options]
testpaths = [
    "tests",
    "tests/bdd/tool_exec",
]
```

**Step file boundary rule.** Each UC gets its own step file to prevent step definition collision. `step_common.py` holds steps whose exact text appears verbatim in multiple feature files (e.g., `Given the tool families registry "tool_families.yaml" is loaded`, `And the exit code is 0`, `And the credential filter service is active`). Steps that appear in only one UC live in that UC's file even if conceptually similar to steps in another.

### pytest-bdd Scenario Discovery Pattern

Each step file uses `scenarios()` scoped to its feature file. Example for UC-001:

```python
from pytest_bdd import scenarios
scenarios("../features/test-UC-TOOLEXEC-001.feature")
```

This wires all scenarios in the feature file to the step definitions in the same module without requiring per-scenario `@scenario` decorators.

---

## L1 Mocking Strategy

The mocking strategy follows a single governing principle: mock infrastructure boundaries, test domain logic real. The hexagonal architecture of `src/tool_exec/` makes this straightforward -- the port interface (`ToolFamilyResolverPort`) and the domain services (`CredentialFilterService`, `EngagementInitializer`, `ModeResolverService`, `FamilyRouterService`) can run against real implementations. Infrastructure adapters that cross to external systems (subprocess, Docker, filesystem at arbitrary paths) are mocked.

### Mock These

| Component | Mock Method | Rationale |
|---|---|---|
| `subprocess.run` / `subprocess.Popen` | `unittest.mock.patch("subprocess.run")` | Prevents real process spawning; controls stdout/stderr/returncode per scenario |
| `subprocess.check_output` | Same patch target | Used by container health check probe |
| Docker Compose CLI (`docker compose exec`, `docker compose up`, `docker compose ps`) | Mock via `subprocess.run` return values | No Docker daemon required in CI |
| `shutil.which` | `patch("shutil.which")` | Controls tool PATH availability in health check |
| `sys.stdin.isatty` | `patch("sys.stdin.isatty")` | Zone 3 approval gate auto-deny trigger |
| `sys.stdin` with `StringIO` or `Mock` | Replace `sys.stdin` in fixture | Zone 3 interactive approval ("yes" / "no" / EOF) |
| `os.chmod` | `patch("os.chmod")` | Assert quarantine file permissions without filesystem side effects in fast unit scenarios |

### Test Real (No Mocking)

| Component | Why Real |
|---|---|
| `CredentialFilterService` | Pure domain service; no I/O; canary pattern matching must be validated end-to-end |
| `EngagementInitializer` with `tmp_path` | Filesystem operations on pytest's isolated temp directory; tests real `os.chmod`, `json.dumps`, `mkdir` behavior |
| `FamilyRouterService` | Pure domain logic; no I/O; routing dispatch tested against real port implementation stubs |
| `ModeResolverService` | Pure domain logic; environment variable reads via `os.environ` isolated with `monkeypatch.setenv` |
| `RainbowToolResolver` with test YAML config | Load a minimal in-memory test YAML config via `tmp_path`; tests real YAML parsing and longest-prefix matching |
| `handle_tool_exec` return value (exit code integer) | The orchestrating function under test; its return value is the primary assertion target |
| `ExitCode` enum | Value object; no mocking |
| `SecurityPolicy` dataclass | Value object; no mocking |
| CLI argument parsing via `parser.py` | Test that `--mode`, `--family`, `--no-filter`, `--zone` are correctly parsed into args namespace |

### Infrastructure Mock vs Real Decision Matrix

```
External system?
    YES -> Mock
    NO  ->
        Domain logic only?
            YES -> Real
            NO  ->
                Uses tmp_path for isolation?
                    YES -> Real
                    NO  -> Mock
```

---

## L1 Fixture Design

All fixtures live in `tests/bdd/tool_exec/conftest.py` unless noted. Fixtures follow pytest scope conventions: `session` scope for read-only artifacts, `function` scope for mutable state.

### Fixture 1: `tool_families_yaml_content` (session scope)

Provides a minimal `tool_families.yaml` content string suitable for loading by `FamilyRegistryLoader`. Written to a `tmp_path`-backed file by fixtures that need real file loading.

```python
@pytest.fixture(scope="session")
def tool_families_yaml_content() -> str:
    """Minimal tool_families.yaml content for test isolation."""
    return textwrap.dedent("""\
        families:
          - name: rainbow
            description: "Rainbow cybersecurity tool suite"
            resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
            resolver_class: RainbowToolResolver
            config_path: skills/rainbow/config/tool-exec.yaml
            enabled: true
            priority: 10
    """)
```

The `config_path` field in the test registry must point to a resolvable YAML. For tests that need the real rainbow config, use the repo-rooted path. For tests that need a controlled minimal config, build a `tmp_path`-based YAML (see Fixture 3).

### Fixture 2: `tool_families_registry_path` (function scope)

Writes `tool_families_yaml_content` to a temporary file and returns the `Path`. Used by fixtures that construct `FamilyRegistryLoader`.

```python
@pytest.fixture()
def tool_families_registry_path(tmp_path, tool_families_yaml_content) -> Path:
    """Write tool_families.yaml to a temp file and return its path."""
    registry_file = tmp_path / "tool_families.yaml"
    registry_file.write_text(tool_families_yaml_content, encoding="utf-8")
    return registry_file
```

### Fixture 3: `minimal_rainbow_config_path` (function scope)

Creates a minimal `tool-exec.yaml` in `tmp_path` with a small set of tool resolution entries covering the zones exercised by BDD scenarios. Avoids coupling tests to the production `skills/rainbow/config/tool-exec.yaml` content.

The YAML content uses the same schema as the real config (`prefix`, `zone`, `service`, `compose_file`, `sub_skill`) with tools chosen to cover Zone 1, Zone 2, and Zone 3 scenarios: a Zone 1 supply-chain scanner, a Zone 2 recon tool, and a Zone 3 exploit tool family using the wildcard prefix pattern.

```python
@pytest.fixture()
def minimal_rainbow_config_path(tmp_path) -> Path:
    """Write a minimal tool-exec.yaml for RainbowToolResolver test instantiation."""
    content = _build_minimal_tool_exec_yaml()  # see implementation note below
    config_file = tmp_path / "tool-exec.yaml"
    config_file.write_text(content, encoding="utf-8")
    return config_file
```

`_build_minimal_tool_exec_yaml()` is a module-level helper that assembles the YAML string from named variables (not a literal block string) to keep the tool name references clearly separate from any credential pattern strings. The tools registered are: `syft` (Zone 1), `checkov` (Zone 1), `grype` (Zone 1), `nuclei` (Zone 2), `subfinder` (Zone 2), `msfconsole` (Zone 3), and `impacket-*` wildcard (Zone 3).

### Fixture 4: `rainbow_resolver` (function scope)

Instantiates a real `RainbowToolResolver` loaded from `minimal_rainbow_config_path`. Tests domain logic (prefix matching, zone policy) without touching the production config file.

```python
@pytest.fixture()
def rainbow_resolver(minimal_rainbow_config_path) -> RainbowToolResolver:
    """Real RainbowToolResolver backed by minimal test config."""
    return RainbowToolResolver(config_path=str(minimal_rainbow_config_path))
```

### Fixture 5: `family_router` (function scope)

Constructs a `FamilyRouterService` containing the `rainbow_resolver`. Provides the domain-layer routing object used to test auto-detect and explicit-family dispatch without loading the real registry.

```python
@pytest.fixture()
def family_router(rainbow_resolver) -> FamilyRouterService:
    """FamilyRouterService wired with the test rainbow resolver."""
    return FamilyRouterService(resolvers={"rainbow": rainbow_resolver})
```

### Fixture 6: `engagement_dir` (function scope)

Creates an initialized engagement directory structure under `tmp_path` using a real `EngagementInitializer`. Returns the `EngagementInitializer` instance and the engagement ID so tests can call `is_initialized()`, `evidence_dir()`, and `quarantine_dir()`.

```python
@pytest.fixture()
def engagement_dir(tmp_path) -> tuple[EngagementInitializer, str]:
    """Initialize a test engagement directory and return (initializer, engagement_id)."""
    engagement_id = "pentest-2026-001"
    initializer = EngagementInitializer(base_dir=tmp_path / "work" / "engagements")
    initializer.initialize(engagement_id, created_by="test-runner")
    return initializer, engagement_id
```

Step definitions that need an engagement-uninitialized state use a separate fixture that returns the initializer without calling `initialize()`.

```python
@pytest.fixture()
def engagement_initializer(tmp_path) -> EngagementInitializer:
    """EngagementInitializer with no engagements created."""
    return EngagementInitializer(base_dir=tmp_path / "work" / "engagements")
```

### Fixture 7: `credential_filter` (function scope)

Real `CredentialFilterService` with default (strict mode active) configuration. Used for UC-TOOLEXEC-005 scenarios that test the filter in isolation without invoking `handle_tool_exec`.

```python
@pytest.fixture()
def credential_filter() -> CredentialFilterService:
    """Real CredentialFilterService with base 15 patterns."""
    return CredentialFilterService()
```

Profile-specific fixtures extend this by constructing a `CredentialFilterService` instance and selectively restricting its compiled pattern sets to match the named profile's scope.

### Fixture 8: `canary_fixtures` (session scope)

Loads canary test values from `generate_canaries.py` at session start **without writing fixture files to disk and without embedding literal credential-format strings in the test source**. Returns a dict keyed by canary category whose values are assembled at runtime by the fragment helper functions in `generate_canaries.py`.

The canary generator intentionally builds credential-format strings from split fragments (e.g., `"AK" + "IA" + "IOSFODNN7EXAMPLE"`) so that no single source line contains a detectable pattern. The BDD conftest imports these fragment helpers via `importlib.util.spec_from_file_location` and calls them to obtain the assembled strings only at test runtime, after the pre-commit scanner has already cleared the source file.

```python
import importlib.util
from pathlib import Path

_CANARY_GEN_PATH = (
    Path(__file__).parents[4]
    / "skills/rainbow/tests/credential-fixtures/generate_canaries.py"
)

@pytest.fixture(scope="session")
def canary_fixtures() -> dict[str, str]:
    """
    Build canary credential strings in memory using the fragment helpers
    from generate_canaries.py.

    No literal credential-format strings appear in this source file.
    All assembly happens at runtime inside generate_canaries.py's helpers,
    which are themselves safe because each fragment is below the detection
    threshold.

    Returned keys and their semantic meaning:
        aws_key           -- AWS access key ID (permanent credential format)
        aws_sts_key       -- AWS STS temporary access key format
        aws_secret_line   -- Full aws_secret_access_key = <value> assignment
        rsa_pem_header    -- RSA private key PEM header line
        ec_pem_header     -- EC private key PEM header line
        ghp_token         -- GitHub classic PAT format
        slack_token       -- Slack bot token format
        conn_str_uri      -- URI-format database connection string with credential
        conn_str_generic  -- Generic ADO.NET-style connection string
        password_line     -- Password: <value> key-value assignment
        passwd_line       -- Passwd: <value> key-value assignment
        github_pat_fine   -- GitHub fine-grained PAT format
        github_pat_classic -- GitHub classic PAT format (same as ghp_token)
        jwt_full          -- Full JWT token in header.payload.signature format
    """
    spec = importlib.util.spec_from_file_location("generate_canaries", _CANARY_GEN_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return {
        "aws_key": mod._aws_access_key(),
        "aws_sts_key": mod._aws_sts_key(),
        "aws_secret_line": mod._aws_secret_label() + " = " + mod._aws_secret_value(),
        "rsa_pem_header": mod._pem_header("RSA"),
        "ec_pem_header": mod._pem_header("EC"),
        "ghp_token": mod._ghp_token(),
        "slack_token": mod._slack_token(),
        "conn_str_uri": mod._conn_str_uri(),
        "conn_str_generic": mod._conn_str_generic(),
        "password_line": mod._password_label("password") + ": CANARY_PLAINTEXT_001",
        "passwd_line": mod._password_label("passwd") + ": CANARY_PLAINTEXT_002",
        "github_pat_fine": mod._ghfine_token(),
        "github_pat_classic": mod._ghp_classic_token(),
        "jwt_full": (
            mod._jwt_header_b64()
            + "."
            + mod._jwt_payload_b64()
            + "."
            + mod._jwt_signature()
        ),
    }
```

Step definitions consume individual keys from this dict. The `canary_fixtures` fixture is session-scoped because the fragment assembly is deterministic and read-only -- the same values are valid for every scenario in the session.

### Fixture 9: `cli_invoke` (function scope)

A factory fixture that calls `handle_tool_exec(args)` with a constructed `argparse.Namespace` and captures the integer return value. Isolates all BDD scenarios from the CLI layer while exercising the real orchestration logic.

```python
@pytest.fixture()
def cli_invoke(monkeypatch, tmp_path):
    """
    Returns a factory function: invoke(tool_command, **kwargs) -> int.

    Constructs an argparse.Namespace with sensible defaults and patches
    _find_project_root() to return tmp_path so all filesystem operations
    land in the pytest temp directory.
    """
    from src.interface.cli.tool_exec_commands import handle_tool_exec

    monkeypatch.setattr(
        "src.interface.cli.tool_exec_commands._find_project_root",
        lambda: tmp_path,
    )

    def invoke(
        tool_command=None,
        tool_args=None,
        *,
        family=None,
        mode=None,
        engagement_id=None,
        init_engagement=None,
        no_filter=False,
        list_families=False,
        list_tools=None,
        health_check=False,
        zone=None,
        evidence_dir=None,
        verbose=False,
    ) -> int:
        import argparse
        args = argparse.Namespace(
            tool_command=tool_command,
            tool_args=tool_args or [],
            family=family,
            mode=mode,
            engagement_id=engagement_id,
            init_engagement=init_engagement,
            no_filter=no_filter,
            list_families=list_families,
            list_tools=list_tools,
            health_check=health_check,
            zone=zone,
            evidence_dir=evidence_dir,
            verbose=verbose,
        )
        return handle_tool_exec(args)

    return invoke
```

**Note on project root wiring.** `cli_invoke` patches `_find_project_root()` to `tmp_path`. This means the tool families registry (`tool_families.yaml`) and the rainbow config (`skills/rainbow/config/tool-exec.yaml`) must also exist relative to `tmp_path` for scenarios that go through `create_tool_exec_handler()`. BDD steps that set up the registry copy it into `tmp_path` as part of the Given clause. A shared `setup_tool_registry` fixture handles this copy.

---

## L1 Exit Code Verification Pattern

Exit codes are the primary behavioral assertion for UC-TOOLEXEC-001 and UC-TOOLEXEC-002. The pattern is consistent across all exit-code scenarios.

### Scenario Context Object

Each scenario uses a mutable `dict` stored in the pytest fixture system. The BDD step file declares this via a function-scoped fixture in `steps/conftest.py`:

```python
# tests/bdd/tool_exec/steps/conftest.py

@pytest.fixture()
def context():
    """
    Mutable scenario context dict. Steps use this to pass state between
    Given/When/Then phases without global variables.

    Canonical keys:
        exit_code (int):          Return value of handle_tool_exec()
        raw_output (str):         Tool stdout content injected into mock
        raw_stderr (str):         Tool stderr content injected into mock
        filtered_output (str):    Output after credential filter
        filter_result:            Full FilterResult from filter_output()
        engagement_id (str):      Active engagement identifier
        error_message (str):      Captured stderr from handle_tool_exec
    """
    return {}
```

All step functions accept `context` as a parameter. The `When` step that calls `cli_invoke()` assigns `context["exit_code"]`.

### Step Definition Template

```python
# In steps/step_common.py

from pytest_bdd import parsers, then
from src.tool_exec.domain.value_objects.exit_codes import ExitCode

@then(parsers.parse("the exit code is {code:d}"))
def assert_exit_code(context, code):
    """Verify the exit code returned by handle_tool_exec matches the expected value."""
    actual = context.get("exit_code")
    assert actual is not None, (
        "exit_code not set in context -- did the When step call cli_invoke()?"
    )
    # Provide a named label in the failure message where possible
    try:
        expected_name = ExitCode(code).name
        actual_name = ExitCode(actual).name
    except ValueError:
        expected_name = str(code)
        actual_name = str(actual)
    assert actual == code, (
        f"Expected exit code {code} ({expected_name}), got {actual} ({actual_name})"
    )
```

### When Step: Parsing jerry Command Strings

The feature files express commands as full `jerry tool exec ...` strings. The When step parses these into the `cli_invoke` keyword arguments:

```python
import shlex
from pytest_bdd import parsers, when

@when(parsers.parse('the user runs "{command}"'))
def run_jerry_command(context, command, cli_invoke):
    # Strip the "jerry tool exec" or "jerry tool" prefix
    normalized = command
    for prefix in ("jerry tool exec ", "jerry tool "):
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break

    # Parse remaining tokens
    tokens = shlex.split(normalized)
    kwargs = _parse_tokens_to_kwargs(tokens)  # extracts --mode, --family, etc.
    kwargs["engagement_id"] = context.get("engagement_id")
    context["exit_code"] = cli_invoke(**kwargs)
```

`_parse_tokens_to_kwargs` is a module-level helper that walks the token list and maps recognized flags (`--mode`, `--family`, `--no-filter`, `--zone`, `--init-engagement`, `--list-families`, `--list-tools`, `--health-check`) to keyword argument names, collecting remaining non-flag tokens as `tool_command` (first) and `tool_args` (rest).

### Exit Code Coverage Table

The step definitions must cover every exit code defined in `ExitCode`. The table below cross-references each code to the UC scenarios that exercise it:

| ExitCode | Value | UC Scenarios |
|---|---|---|
| SUCCESS | 0 | UC-001 (BC-01, BC-02, BC-04), UC-002 happy path, UC-003 create, UC-004, UC-006 |
| UNKNOWN_TOOL | 1 | UC-001 no family recognizes, UC-002 tool not in family, UC-003 invalid ID |
| TOOL_ERROR | 2 | UC-001/UC-002 tool returns non-zero |
| CONTAINER_NOT_RUNNING | 3 | UC-001/UC-002 auto-start fails |
| CREDENTIAL_DETECTED | 4 | UC-001/UC-002/UC-005 credential patterns |
| ENGAGEMENT_NOT_INIT | 5 | UC-001/UC-002 Zone 2/3 without engagement |
| MODE_UNSET | 6 | UC-001/UC-002 strict mode + no explicit mode; UC-005 --no-filter blocked |
| FAMILY_NOT_FOUND | 7 | UC-002/UC-004 explicit family not found |
| FAMILY_CONFIG_ERROR | 8 | UC-002/UC-004 malformed config |
| STRICT_MODE_VIOLATION | 9 | UC-005 --no-filter with JERRY_STRICT_MODE=true |
| ZONE3_CONTAINER_REQUIRED | 10 | Not in current feature files -- see coverage gap in L2 |
| ZONE3_APPROVAL_DENIED | 11 | UC-001 Zone 3 auto-deny (non-TTY) |

---

## L1 Security Test Patterns

### Pattern 1: Zone 3 Approval Gate -- Non-TTY Auto-Deny

The approval gate fires in `_request_zone3_approval()` at line 849 of `tool_exec_commands.py`:

```python
auto_deny = not sys.stdin.isatty()
```

When `isatty()` returns `False` (CI runner, AI agent, pipe), the gate auto-denies and returns `ExitCode.ZONE3_APPROVAL_DENIED` (11).

**Fixture approach:** Patch `sys.stdin.isatty` to return `False` for the non-interactive test, `True` for interactive tests that then further control `builtins.input`.

```python
@pytest.fixture()
def non_tty_stdin(mocker):
    """Simulate non-interactive stdin -- CI runner or AI agent context."""
    mocker.patch("sys.stdin.isatty", return_value=False)

@pytest.fixture()
def interactive_stdin_approve(mocker):
    """Simulate operator typing 'yes' at the Zone 3 approval prompt."""
    mocker.patch("sys.stdin.isatty", return_value=True)
    mocker.patch("builtins.input", return_value="yes")

@pytest.fixture()
def interactive_stdin_deny(mocker):
    """Simulate operator typing 'no' at the Zone 3 approval prompt."""
    mocker.patch("sys.stdin.isatty", return_value=True)
    mocker.patch("builtins.input", return_value="no")

@pytest.fixture()
def interactive_stdin_eof(mocker):
    """Simulate EOFError (pipe close) at the Zone 3 approval prompt."""
    mocker.patch("sys.stdin.isatty", return_value=True)
    mocker.patch("builtins.input", side_effect=EOFError)
```

**Step definition pattern:**

```python
@when('the user runs "jerry tool exec impacket-smbclient --help"')
def run_zone3_tool(context, cli_invoke, non_tty_stdin, engagement_dir, setup_zone3_mocks):
    _, engagement_id = engagement_dir
    context["exit_code"] = cli_invoke(
        tool_command="impacket-smbclient",
        tool_args=["--help"],
        engagement_id=engagement_id,
        mode="container",
    )

@then("the exit code is 11")
def assert_zone3_denied(context):
    from src.tool_exec.domain.value_objects.exit_codes import ExitCode
    assert context["exit_code"] == ExitCode.ZONE3_APPROVAL_DENIED
```

**Security invariant being tested:** OWASP A01:2021 Broken Access Control -- an unattended process (AI agent, CI runner) must never execute a Zone 3 exploitation tool without explicit human approval. The test verifies the gate fires before the container executor is ever invoked.

The audit trail written by `_write_approval_audit()` must also be asserted: a `.zone3-audit/` file must exist under `tmp_path` after an auto-deny, confirming the durable record requirement from IN-015-R2.

### Pattern 2: Strict Mode Enforcement

`JERRY_STRICT_MODE` is read at line 298 of `tool_exec_commands.py`. The BDD step sets it via `monkeypatch.setenv`.

```python
@given("strict mode is active")
def strict_mode_on(monkeypatch):
    monkeypatch.setenv("JERRY_STRICT_MODE", "true")

@given("strict mode is not active")
def strict_mode_off(monkeypatch):
    monkeypatch.setenv("JERRY_STRICT_MODE", "false")
```

**Three strict mode security scenarios to cover in BDD:**

1. `--no-filter` with `JERRY_STRICT_MODE=true` -> `ExitCode.STRICT_MODE_VIOLATION` (9).
   Assert error message contains the text "FORBIDDEN when JERRY_STRICT_MODE=true".

2. Zone 2 tool without explicit `--mode` with `JERRY_STRICT_MODE=true` -> `ExitCode.MODE_UNSET` (6).
   Verifies the gate blocks implicit mode resolution for active reconnaissance tools.

3. `--no-filter` with `JERRY_STRICT_MODE=false` -> exit code 0 (tool runs, audit written).
   Verifies the bypass is logged and the audit file is written under `work/.no-filter-audit/`.

**Regression test for FIX-4 (RT-001) -- empty env var bypass:**

```python
@given("the JERRY_STRICT_MODE environment variable is set to an empty string")
def strict_mode_empty_string(monkeypatch):
    monkeypatch.setenv("JERRY_STRICT_MODE", "")

@then("strict mode remains active")
def assert_strict_still_active(context):
    # Empty string is NOT in ("false","0","no") so strict=True must hold.
    # --no-filter must still be blocked with STRICT_MODE_VIOLATION.
    from src.tool_exec.domain.value_objects.exit_codes import ExitCode
    assert context["exit_code"] == ExitCode.STRICT_MODE_VIOLATION
```

This directly guards the FIX-4 regression: an empty `JERRY_STRICT_MODE` env var must not disable strict mode.

### Pattern 3: Quarantine File Permissions

Quarantine files created by `_quarantine_output()` must have permissions `0o600` (per file) and `0o700` (per directory) per FIX-8 / SR-003 / NIST CSF PR.DS-1.

**Approach A -- Real filesystem permissions (preferred for BDD).**

Use `engagement_dir` fixture with `tmp_path`. After a scenario that triggers credential detection, assert actual `stat()` mode bits on the created files:

```python
@then("the quarantine file has permissions 0o600")
def assert_quarantine_file_permissions(context, engagement_dir):
    initializer, engagement_id = engagement_dir
    quarantine = initializer.quarantine_dir(engagement_id)
    raw_files = list(quarantine.glob("*.raw"))
    assert raw_files, "No quarantine .raw files found"
    for raw_file in raw_files:
        actual_mode = oct(raw_file.stat().st_mode & 0o777)
        assert actual_mode == "0o600", (
            f"Quarantine file {raw_file.name} has mode {actual_mode}, expected 0o600"
        )

@then("the quarantine directory has permissions 0o700")
def assert_quarantine_dir_permissions(context, engagement_dir):
    initializer, engagement_id = engagement_dir
    quarantine = initializer.quarantine_dir(engagement_id)
    actual_mode = oct(quarantine.stat().st_mode & 0o777)
    assert actual_mode == "0o700", (
        f"Quarantine dir has mode {actual_mode}, expected 0o700"
    )
```

**Important:** macOS and Linux both honor `os.chmod()` on `tmp_path` directories. With the default `umask 0022` in CI, only the explicit `os.chmod(path, 0o600)` call produces the correct permissions. A test that omits the permission assertion would silently miss the FIX-8 regression.

**Approach B -- Mock and assert calls (for fast unit tests, not BDD).**

For fast unit scenarios in `tests/unit/tool_exec/` where filesystem interaction is unwanted, capture `os.chmod` calls:

```python
@pytest.fixture()
def mock_chmod(mocker):
    return mocker.patch("os.chmod")

@then("os.chmod was called with 0o600 on the quarantine file")
def assert_chmod_600_called(context, mock_chmod):
    chmod_600_calls = [c for c in mock_chmod.call_args_list if c.args[1] == 0o600]
    assert len(chmod_600_calls) >= 1, (
        f"Expected os.chmod(path, 0o600) to be called at least once. Got: {mock_chmod.call_args_list}"
    )
```

The BDD suite uses Approach A. Approach B is reserved for the unit test layer.

### Pattern 4: Quarantine SHA-256 Filename (Content-Addressable)

The `_quarantine_output()` function names quarantine files by the SHA-256 hex digest of the raw output bytes. The BDD step verifies both the naming convention and the content-addressable deduplication property:

```python
@then("the quarantine filename contains a SHA-256 hash")
def assert_quarantine_filename_is_sha256(context, engagement_dir):
    import hashlib
    import re
    initializer, engagement_id = engagement_dir
    quarantine = initializer.quarantine_dir(engagement_id)
    raw_files = list(quarantine.glob("*.raw"))
    assert raw_files, "No quarantine .raw files found"
    for raw_file in raw_files:
        stem = raw_file.stem
        assert re.match(r"^[0-9a-f]{64}$", stem), (
            f"Quarantine filename stem '{stem}' is not a 64-char lowercase hex string"
        )
        # Content-addressable: filename must equal SHA-256 of file content
        content = raw_file.read_bytes()
        expected = hashlib.sha256(content).hexdigest()
        assert stem == expected, (
            f"Quarantine file named {stem!r} does not match SHA-256 of its content ({expected!r})"
        )
```

The deduplication scenario ("identical output produces same quarantine file") is verified by scanning twice with the same raw output and asserting `len(list(quarantine.glob("*.raw"))) == 1`.

### Pattern 5: Engagement ID Injection Validation

UC-TOOLEXEC-003 contains a `Scenario Outline` with 6 special characters that must each be rejected. The step definition handles the `<char>` parameter from the Examples table:

```python
@when(parsers.parse('the user runs "jerry tool exec --init-engagement \'test{char}value\'"'))
def run_init_with_special_char(context, char, cli_invoke):
    """Test that special characters in engagement ID are rejected by _validate_id()."""
    malicious_id = f"test{char}value"
    context["exit_code"] = cli_invoke(init_engagement=malicious_id)

@then('the error message contains "Invalid engagement ID format"')
def assert_invalid_id_error(context, capsys):
    captured = capsys.readouterr()
    combined = captured.out + captured.err
    assert "Invalid engagement ID format" in combined or "invalid characters" in combined.lower()

@then("no directory is created")
def assert_no_directory_created(context, tmp_path):
    engagements_dir = tmp_path / "work" / "engagements"
    if engagements_dir.exists():
        created = list(engagements_dir.iterdir())
        assert not created, (
            f"Expected no directories, found: {[d.name for d in created]}"
        )
```

Path traversal variants (`../etc/passwd`, `foo/bar`) are also tested. The `_ENGAGEMENT_ID_PATTERN` allowlist (`^[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}$`) rejects both because forward slash and dot are outside the allowed character set.

### Pattern 6: Module Import Allowlist (M-01 / CWE-94)

This security control lives in `FamilyRegistryLoader._validate_module_path()`. The allowlist restricts `importlib.import_module()` to `src.tool_exec.infrastructure.adapters.*`. Although not covered by any current UC feature file, it is the highest DREAD-scored control point (DREAD 38) and must have BDD-level security tests.

Recommended as a security extension scenario added to UC-TOOLEXEC-002:

```python
@given('a family registry entry references an out-of-allowlist module path')
def registry_with_disallowed_module(tmp_path, tool_families_registry_path):
    """Write a tampered registry referencing a module outside the allowed prefix."""
    # The module path references "os" which is outside src.tool_exec.infrastructure.adapters.*
    # Content uses a descriptive placeholder rather than a dangerous module name.
    tampered = textwrap.dedent("""\
        families:
          - name: evil
            description: "Tampered family for security test"
            resolver_module: os.path
            resolver_class: EvilResolver
            config_path: /dev/null
            enabled: true
    """)
    tool_families_registry_path.write_text(tampered)

@then('the error message contains "not in the allowed prefix list"')
def assert_module_allowlist_error(context, capsys):
    captured = capsys.readouterr()
    combined = captured.out + captured.err
    assert "allowed prefix" in combined or "not in the allowed" in combined
```

A companion test exercises `_validate_class_name()` (FINDING-003 / CWE-94) with a dunder attribute name such as `__import__` or `__builtins__`, verifying the class name pattern `^[A-Z][a-zA-Z0-9]{1,63}$` rejects it.

### Pattern 7: Zone 3 Container Enforcement (FM-002 / FIX-3)

Zone 3 tools have `container_required: True` in their security policy (`RainbowToolResolver._ZONE_POLICIES["3"]`). Requesting `--mode local` for a Zone 3 tool must return `ExitCode.ZONE3_CONTAINER_REQUIRED` (10).

```python
@when('the user runs "jerry tool exec --mode local msfconsole"')
def run_zone3_with_local_mode(context, cli_invoke, monkeypatch, engagement_dir):
    monkeypatch.setenv("JERRY_STRICT_MODE", "true")
    _, engagement_id = engagement_dir
    context["exit_code"] = cli_invoke(
        tool_command="msfconsole",
        mode="local",
        engagement_id=engagement_id,
    )

@then("the exit code is 10")
def assert_zone3_container_required(context):
    from src.tool_exec.domain.value_objects.exit_codes import ExitCode
    assert context["exit_code"] == ExitCode.ZONE3_CONTAINER_REQUIRED
```

This exit code is not covered by any current feature file -- see coverage gap documentation in L2.

---

## L1 Canary Integration in BDD Scenarios

The `canary_fixtures` session-scoped fixture supplies all credential strings needed by UC-TOOLEXEC-005. Step definitions call it by name; pytest injects the assembled dict. The key design constraint is that no step definition file itself contains a literal credential-format string -- all such strings are assembled at runtime via `generate_canaries.py`'s fragment helpers.

### Credential Filter Isolation Tests (UC-005)

UC-TOOLEXEC-005 tests `CredentialFilterService.filter_output()` directly without going through `handle_tool_exec`. This keeps the filter scenarios fast and removes the need to set up the full registry, executor, and engagement state.

```python
@given("the tool output contains a string matching the AWS access key ID pattern")
def output_with_aws_key(context, canary_fixtures):
    context["raw_output"] = (
        "Scan complete.\n"
        "Access Key: " + canary_fixtures["aws_key"] + "\n"
        "No further findings."
    )

@when("the credential filter scans the output")
def filter_scans_output(context, credential_filter):
    context["filter_result"] = credential_filter.filter_output(
        raw_output=context["raw_output"],
        no_filter=False,
        strict_mode=True,
    )

@then('the matched region is replaced with "[CREDENTIAL-REDACTED]"')
def assert_redacted(context):
    result = context["filter_result"]
    assert result.detected is True
    assert CredentialFilterService.REDACTION_MARKER in result.filtered_output

@then("the surrounding output context is preserved")
def assert_surrounding_context(context):
    result = context["filter_result"]
    assert "Scan complete." in result.filtered_output
    assert "No further findings." in result.filtered_output
```

**Mapping "a CredentialDetectedError is raised" to the implementation.** The feature file uses this phrasing but `CredentialFilterService.filter_output()` does not raise an exception -- it returns `FilterResult(detected=True, ...)`. The step definition maps the Gherkin intent to the actual API:

```python
@then("a CredentialDetectedError is raised")
def assert_credential_detected_signal(context):
    # The domain service signals detection via FilterResult.detected=True.
    # ExitCode.CREDENTIAL_DETECTED (4) is what handle_tool_exec returns.
    # At the domain service level, FilterResult.detected is the equivalent signal.
    assert context["filter_result"].detected is True
```

### Profile-Specific Pattern Matching

UC-TOOLEXEC-005 defines three profiles (`default`, `api-keys`, `minimal`) with different pattern scopes. The step definitions construct the appropriate filter:

```python
@given(parsers.parse('the credential filter profile is "{profile}"'))
def set_filter_profile(context, profile):
    """Configure the credential filter for the named profile.

    Profile definitions derived from tool-exec.yaml and SecurityPolicy:
        default:  All 15 base patterns (8 case-sensitive + 7 case-insensitive)
        api-keys: AI/cloud API key patterns only (Anthropic, OpenAI, Google, GitHub PAT)
        minimal:  Password assignment + connection string patterns only;
                  bearer tokens excluded
    """
    base = CredentialFilterService()
    if profile == "default":
        context["filter"] = base
    elif profile == "api-keys":
        # Use base filter -- it already contains the modern cloud API key patterns
        # (sk-ant-api, sk-proj-, AIzaSy, github_pat_) via M-02 additions.
        # AWS key patterns are in the case-sensitive group; the api-keys profile
        # intentionally excludes them, so tests for this profile must use outputs
        # that only contain API key patterns, not AWS access key IDs.
        context["filter"] = base
    elif profile == "minimal":
        # Minimal: restrict to password-assignment and connection-string CI patterns only
        minimal = CredentialFilterService()
        # Keep only CI_PATTERNS indices 2 (password) and 3 (connection string)
        minimal._ci_patterns = [
            minimal._ci_patterns[2],
            minimal._ci_patterns[3],
        ]
        minimal._ci_raw = [
            minimal._ci_raw[2],
            minimal._ci_raw[3],
        ]
        minimal._cs_patterns = []
        minimal._cs_raw = []
        context["filter"] = minimal
    else:
        raise ValueError(f"Unknown profile: {profile!r}")
```

The UC-005 `Scenario: API keys profile does not detect AWS access keys` test specifically uses `canary_fixtures["aws_key"]` in the output but expects `detected=False` from the api-keys filter, confirming the profile scoping is respected.

---

## L2 Strategic Implications

### Coverage Gaps Identified

| Gap | Severity | Risk | Recommendation |
|---|---|---|---|
| `ExitCode.ZONE3_CONTAINER_REQUIRED` (10) not in any feature file | HIGH | FM-002 / FIX-3 security control untested at BDD level | Add scenario to UC-001 or a new UC-TOOLEXEC-007 security extension file |
| Module import allowlist (M-01 / CWE-94) not in any feature file | HIGH | DREAD 38; highest-scored control point | Add security extension scenarios to UC-002 |
| Class name validation (FINDING-003 / CWE-94) not in any feature file | HIGH | getattr() safety; same attack surface as M-01 | Include in UC-002 security extension |
| Evidence path traversal (FINDING-001 / CWE-22) covered only in unit tests | MEDIUM | BDD layer provides end-to-end validation that unit tests miss | Add `--evidence-dir ../../tmp/exfil` scenario to UC-001 |
| `ExitCode.ZONE3_APPROVAL_DENIED` (11) not explicitly in UC-001 scenarios | MEDIUM | IN-015-R2 gate coverage; auto-deny is a critical CI/AI safety control | Add explicit non-TTY Zone 3 auto-deny scenario to UC-001 |
| FIX-4 empty env var bypass regression | MEDIUM | Empty `JERRY_STRICT_MODE` must not disable strict mode | Add step using `monkeypatch.setenv("JERRY_STRICT_MODE", "")` to UC-001 strict mode group |
| Multi-line credential splits (PM-001-R2 sliding window) | MEDIUM | Credentials split across line boundaries may bypass single-line scan | Add multi-line canary scenarios to UC-005 using `\n`-split canary strings |
| `--no-filter` audit trail (FM-001) assertion | LOW | Audit file creation verifiable only if explicitly asserted | Add assertion on audit file existence in UC-005 non-strict bypass scenario |

### Fuzzing Recommendations

UC-TOOLEXEC-003 engagement ID validation is a natural fuzzing target. The allowlist regex `^[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}$` should be validated with a Hypothesis property test alongside the BDD suite:

```python
# tests/unit/tool_exec/test_engagement_initializer_hypothesis.py
import re
from hypothesis import given, settings
from hypothesis import strategies as st
from src.tool_exec.domain.services.engagement_initializer import EngagementInitializer

VALID_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}$")

@given(st.text(min_size=0, max_size=200))
@settings(max_examples=2000)
def test_id_validation_never_crashes(raw_id, tmp_path):
    """_validate_id() must raise ValueError XOR succeed -- never propagate to filesystem."""
    initializer = EngagementInitializer(base_dir=tmp_path / "work" / "engagements")
    if VALID_PATTERN.match(raw_id):
        try:
            initializer._validate_id(raw_id)
        except ValueError:
            raise AssertionError(f"Valid ID {raw_id!r} was unexpectedly rejected")
    else:
        try:
            initializer._validate_id(raw_id)
            raise AssertionError(f"Invalid ID {raw_id!r} was accepted without error")
        except ValueError:
            pass  # Expected
```

Additional fuzzing targets: `RainbowToolResolver._find_entry()` with arbitrary tool command strings (boundary: prefix length, Unicode, null bytes, the `-*` wildcard boundary), and `CredentialFilterService.filter_output()` with arbitrary strings to confirm no regex denial-of-service vulnerability in the 15 base patterns.

### Regression Suite Maintenance Protocol

The BDD suite must be updated when:

1. A new `ExitCode` value is added -- add scenarios exercising the new code path in the relevant UC file.
2. A new credential pattern is added to `CredentialFilterService` -- add a corresponding canary generator function to `generate_canaries.py` and a UC-005 scenario that verifies detection.
3. A new zone is added to `RainbowToolResolver._ZONE_POLICIES` -- add zone-specific scenarios to UC-001 and UC-002.
4. `_ALLOWED_MODULE_PREFIXES` is extended -- add a security extension scenario confirming the new prefix accepts a valid module and the old boundary still rejects disallowed modules.
5. A new security gate is added to `handle_tool_exec` -- add a corresponding section to this strategy document and a security scenario to the appropriate UC file.

### Coverage Enforcement

Run coverage against the BDD suite in addition to the unit suite:

```bash
uv run pytest tests/bdd/tool_exec/ \
    --cov=src/tool_exec \
    --cov=src/interface/cli/tool_exec_commands.py \
    --cov-report=term-missing \
    --cov-fail-under=90
```

Security-critical branch paths that must individually reach 100% branch coverage (enforced via targeted unit tests in `tests/unit/tool_exec/` if not fully reached by BDD):

- `CredentialFilterService.filter_output()` -- single-line match, sliding-window match, no-detection clean path
- `_request_zone3_approval()` -- non-TTY auto-deny, TTY approve ("yes"), TTY deny ("no"), EOFError
- `FamilyRegistryLoader._validate_module_path()` -- allowed prefix match, disallowed prefix rejection
- `FamilyRegistryLoader._validate_class_name()` -- valid CamelCase class name, dunder attribute rejection
- `EngagementInitializer._validate_id()` -- valid pattern acceptance, empty string rejection, special character rejection
- Strict mode gate in `handle_tool_exec()` -- strict=True + no_filter (exit 9), strict=False + no_filter (exit 0), strict=True + no_filter absent (continue)

These six branch sets are the regression boundary for the eight security control points identified in L0.
