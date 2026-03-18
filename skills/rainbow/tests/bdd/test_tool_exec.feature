@rainbow @tool-exec @ADR-PROJ023-001
Feature: Rainbow Tool Executor (jerry tool exec)
  As a security operator
  I want tool execution to resolve configurably between local and container mode
  So that I can run cybersecurity tools in isolated containers or locally based on environment

  # ---------------------------------------------------------------------------
  # Background: shared fixture wiring (not real Docker — test harness stubs)
  # ---------------------------------------------------------------------------

  Background:
    Given the jerry tool exec wrapper is on the PATH
    And the tool-exec.yaml config file is present at the auto-detected location
    And no engagement is initialized by default

  # ---------------------------------------------------------------------------
  # BC-01: Local mode resolves to direct CLI execution
  # ADR ref: BC-01 — RAINBOW_TOOL_MODE=local -> exec tool directly on host
  # ---------------------------------------------------------------------------

  @BC-01 @zone-1 @local-mode
  Scenario: BC-01 — local mode executes a known Zone 1 tool directly on the host
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "checkov" is present in the resolution table as Zone 1
    When jerry tool exec is called with arguments "checkov --version"
    Then the wrapper executes "checkov --version" directly on the host without docker
    And the exit code is 0
    And the credential filter is applied to the captured output

  @BC-01 @zone-2 @local-mode
  Scenario: BC-01 — local mode executes a known Zone 2 tool directly on the host
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "subfinder" is present in the resolution table as Zone 2
    When jerry tool exec is called with arguments "subfinder -h"
    Then the wrapper executes "subfinder -h" directly on the host without docker
    And the exit code is 0

  @BC-01 @zone-3 @local-mode
  Scenario: BC-01 — local mode executes a known Zone 3 tool directly on the host
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "impacket-smbclient" is present in the resolution table as Zone 3
    When jerry tool exec is called with arguments "impacket-smbclient --help"
    Then the wrapper executes "impacket-smbclient --help" directly on the host without docker
    And no docker compose exec is invoked

  # ---------------------------------------------------------------------------
  # BC-02: Container mode resolves to docker compose exec
  # ADR ref: BC-02 — RAINBOW_TOOL_MODE=container -> docker compose exec -T
  # ---------------------------------------------------------------------------

  @BC-02 @zone-3 @container-mode
  Scenario: BC-02 — container mode routes a Zone 3 tool through docker compose exec
    Given RAINBOW_TOOL_MODE is set to "container"
    And the tool command "impacket-smbclient" is present in the resolution table with service "exploit-ops"
    And the compose file for "rainbow-exploit" is discoverable
    And the container service "exploit-ops" is running
    When jerry tool exec is called with arguments "impacket-smbclient --help"
    Then the wrapper invokes "docker compose exec -T exploit-ops impacket-smbclient --help"
    And the exit code is 0
    And the credential filter is applied to the captured output

  @BC-02 @zone-2 @container-mode
  Scenario: BC-02 — container mode routes a Zone 2 recon tool through docker compose exec
    Given RAINBOW_TOOL_MODE is set to "container"
    And the tool command "subfinder" is present in the resolution table with service "recon-pipeline"
    And the compose file for "rainbow-recon" is discoverable
    And the container service "recon-pipeline" is running
    When jerry tool exec is called with arguments "subfinder -h"
    Then the wrapper invokes "docker compose exec -T recon-pipeline subfinder -h"
    And the -T flag is present in the docker compose exec invocation
    And the exit code is 0

  @BC-02 @zone-1 @container-mode
  Scenario: BC-02 — container mode routes a Zone 1 supply-chain tool through docker compose exec
    Given RAINBOW_TOOL_MODE is set to "container"
    And the tool command "syft" is present in the resolution table with service "scanner"
    And the compose file for "rainbow-supply-chain" is discoverable
    And the container service "scanner" is running
    When jerry tool exec is called with arguments "syft --version"
    Then the wrapper invokes "docker compose exec -T scanner syft --version"
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # BC-03: Strict mode rejects Zone 2/3 tools when RAINBOW_TOOL_MODE is unset
  # ADR ref: BC-03 — unset + Zone 2/3 + RAINBOW_STRICT_MODE=true -> exit 6
  # ---------------------------------------------------------------------------

  @BC-03 @zone-3 @strict-mode @security
  Scenario: BC-03 — Zone 3 tool rejected when RAINBOW_TOOL_MODE is unset in strict mode
    Given RAINBOW_TOOL_MODE is unset
    And RAINBOW_STRICT_MODE is set to "true"
    And the tool command "impacket-smbclient" is present in the resolution table as Zone 3
    When jerry tool exec is called with arguments "impacket-smbclient --help"
    Then the wrapper exits with code 6
    And an error message is emitted containing "RAINBOW_TOOL_MODE is not set"
    And an error message is emitted containing "Zone 2/3"
    And no tool command is executed on the host or in a container

  @BC-03 @zone-2 @strict-mode @security
  Scenario: BC-03 — Zone 2 tool rejected when RAINBOW_TOOL_MODE is unset in strict mode
    Given RAINBOW_TOOL_MODE is unset
    And RAINBOW_STRICT_MODE is set to "true"
    And the tool command "subfinder" is present in the resolution table as Zone 2
    When jerry tool exec is called with arguments "subfinder -h"
    Then the wrapper exits with code 6
    And an error message is emitted containing "RAINBOW_TOOL_MODE is not set"

  @BC-03 @strict-mode @default-behavior
  Scenario: BC-03 — default strict_mode in config is true, matching env behavior
    Given RAINBOW_TOOL_MODE is unset
    And RAINBOW_STRICT_MODE is unset
    And the config file specifies "strict_mode: true"
    And the tool command "nuclei" is present in the resolution table as Zone 2
    When jerry tool exec is called with arguments "nuclei -version"
    Then the wrapper exits with code 6

  # ---------------------------------------------------------------------------
  # BC-04: Zone 1 falls back to local safely when RAINBOW_TOOL_MODE is unset
  # ADR ref: BC-04 — unset + Zone 1 tool -> fall back to local mode
  # ---------------------------------------------------------------------------

  @BC-04 @zone-1 @fallback @safe-default
  Scenario: BC-04 — Zone 1 tool falls back to local execution when RAINBOW_TOOL_MODE is unset
    Given RAINBOW_TOOL_MODE is unset
    And RAINBOW_STRICT_MODE is set to "true"
    And the tool command "checkov" is present in the resolution table as Zone 1
    When jerry tool exec is called with arguments "checkov --version"
    Then the wrapper executes "checkov --version" directly on the host without docker
    And the exit code is 0
    And no error about RAINBOW_TOOL_MODE is emitted

  @BC-04 @zone-1 @fallback
  Scenario: BC-04 — Zone 1 tool "trivy" falls back to local safely
    Given RAINBOW_TOOL_MODE is unset
    And the tool command "trivy" is present in the resolution table as Zone 1
    When jerry tool exec is called with arguments "trivy --version"
    Then the wrapper executes "trivy --version" directly on the host without docker
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # BC-05: Unknown tool prefix returns exit 1
  # ADR ref: BC-05 — tool not in resolution table -> exit 1
  # ---------------------------------------------------------------------------

  @BC-05 @unknown-tool @security
  Scenario: BC-05 — completely unknown tool prefix returns exit code 1
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "notarealtool" is NOT present in the resolution table
    When jerry tool exec is called with arguments "notarealtool --help"
    Then the wrapper exits with code 1
    And an error message is emitted containing "Unknown tool prefix"
    And no tool command is executed on the host or in a container

  @BC-05 @unknown-tool @security
  Scenario: BC-05 — tool with misleading partial prefix match is rejected when not in table
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "impacket" is NOT a complete entry in the resolution table
    And the resolution table contains "impacket-*" as a wildcard entry
    When jerry tool exec is called with arguments "impacket --help"
    Then the wrapper exits with code 1
    And an error message is emitted containing "Unknown tool prefix"

  @BC-05 @unknown-tool
  Scenario: BC-05 — empty tool prefix returns exit code 1
    Given RAINBOW_TOOL_MODE is set to "local"
    When jerry tool exec is called with no tool arguments
    Then the wrapper exits with a non-zero code
    And a usage or error message is emitted

  # ---------------------------------------------------------------------------
  # BC-06: Container not running triggers auto-start attempt
  # ADR ref: BC-06 — container mode + service not running -> auto-start; exit 3 on failure
  # ---------------------------------------------------------------------------

  @BC-06 @container-mode @auto-start
  Scenario: BC-06 — stopped container service triggers auto-start attempt
    Given RAINBOW_TOOL_MODE is set to "container"
    And the tool command "impacket-smbclient" is present in the resolution table with service "exploit-ops"
    And the compose file for "rainbow-exploit" exists on disk
    And the container service "exploit-ops" is NOT running
    When jerry tool exec is called with arguments "impacket-smbclient --help"
    Then the wrapper attempts "docker compose up -d exploit-ops"
    And if auto-start succeeds the tool executes and exits with code 0
    And if auto-start fails the wrapper exits with code 3

  @BC-06 @container-mode @auto-start-failure @security
  Scenario: BC-06 — auto-start failure returns exit code 3 with actionable error
    Given RAINBOW_TOOL_MODE is set to "container"
    And the tool command "subfinder" is present in the resolution table with service "recon-pipeline"
    And the compose file for "rainbow-recon" exists on disk
    And the container service "recon-pipeline" is NOT running
    And docker compose up -d returns a non-zero exit code
    When jerry tool exec is called with arguments "subfinder -h"
    Then the wrapper exits with code 3
    And an error message is emitted containing "not running"
    And an error message is emitted containing "docker compose"
    And no credential filter placeholder is emitted

  # ---------------------------------------------------------------------------
  # BC-07: Credential filter quarantines detected material
  # ADR ref: BC-07 — credential detected in output -> quarantine; exit 4
  # ---------------------------------------------------------------------------

  @BC-07 @credential-filter @security @OWASP-INPVAL
  Scenario: BC-07 — AWS access key in tool output is quarantined and exit 4 returned
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "checkov" is present in the resolution table as Zone 1
    And the tool output contains a line matching the AWS access key pattern "AKIA[A-Z0-9]{16}"
    When jerry tool exec is called with arguments "checkov --version"
    Then the wrapper exits with code 4
    And the raw output is written to the quarantine directory
    And a metadata JSON file is written alongside the quarantine file
    And the agent receives a placeholder containing "[CREDENTIAL-FILTER]"
    And the placeholder contains "quarantined"
    And the placeholder does NOT contain any credential material

  @BC-07 @credential-filter @security @OWASP-INPVAL
  Scenario: BC-07 — generic API token pattern in tool output is quarantined
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "trivy" is present in the resolution table as Zone 1
    And the tool output contains a line matching the API token pattern "api_key: [A-Za-z0-9_-]{20,}"
    When jerry tool exec is called with arguments "trivy --version"
    Then the wrapper exits with code 4
    And a quarantine file exists in the quarantine directory
    And the agent-facing output contains the text "[CREDENTIAL-FILTER]"

  @BC-07 @credential-filter @security @OWASP-INPVAL
  Scenario: BC-07 — clean tool output passes through without quarantine
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "checkov" is present in the resolution table as Zone 1
    And the tool output contains no credential pattern
    When jerry tool exec is called with arguments "checkov --version"
    Then the wrapper exits with code 0
    And no quarantine file is created
    And the full tool output is returned to the caller

  @BC-07 @credential-filter @strict-mode @security
  Scenario: BC-07 — --no-filter is FORBIDDEN when RAINBOW_STRICT_MODE is true
    Given RAINBOW_TOOL_MODE is set to "local"
    And RAINBOW_STRICT_MODE is set to "true"
    And the tool command "checkov" is present in the resolution table as Zone 1
    When jerry tool exec is called with "--no-filter checkov --version"
    Then the wrapper exits with a non-zero code
    And an error message is emitted containing "--no-filter is FORBIDDEN"
    And the tool is NOT executed

  # ---------------------------------------------------------------------------
  # BC-08: Engagement not initialized returns exit 5
  # ADR ref: BC-08 — --engagement <id> provided but not initialized -> exit 5
  # ---------------------------------------------------------------------------

  @BC-08 @engagement @security
  Scenario: BC-08 — uninitialized engagement ID causes exit 5
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "checkov" is present in the resolution table as Zone 1
    And no engagement directory exists for engagement ID "ENG-TEST-001"
    When jerry tool exec is called with "--engagement ENG-TEST-001 checkov --version"
    Then the wrapper exits with code 5
    And an error message is emitted containing "not initialized"
    And an error message is emitted containing "ENG-TEST-001"
    And no tool command is executed

  @BC-08 @engagement @positive
  Scenario: BC-08 — initialized engagement ID allows tool execution with evidence persistence
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "checkov" is present in the resolution table as Zone 1
    And engagement "ENG-TEST-002" has been initialized via --init-engagement
    When jerry tool exec is called with "--engagement ENG-TEST-002 checkov --version"
    Then the wrapper exits with code 0
    And an evidence file is written under the engagement evidence directory
    And a metadata JSON file accompanies the evidence file containing "sha256_raw"

  @BC-08 @engagement @init
  Scenario: BC-08 — --init-engagement creates the required directory structure
    Given no engagement directory exists for engagement ID "ENG-INIT-001"
    When jerry tool exec is called with "--init-engagement ENG-INIT-001"
    Then the wrapper exits with code 0
    And a directory "work/engagements/ENG-INIT-001/evidence" is created
    And a directory "work/engagements/ENG-INIT-001/reports" is created
    And a directory "work/engagements/ENG-INIT-001/.credential-quarantine" is created
    And a file "work/engagements/ENG-INIT-001/engagement-init.json" is created
    And the init JSON file contains "engagement_id" equal to "ENG-INIT-001"

  # ---------------------------------------------------------------------------
  # BC-09: Zone 3 network grant/revoke protocol (Phase 6 spec — pending impl)
  # ADR ref: BC-09 — Zone 3 + container networking + P-020 approval -> grant/revoke
  # Note: BC-09 is a Phase 6 specification. These scenarios are tagged @pending
  # to document the expected behavior without requiring current implementation.
  # ---------------------------------------------------------------------------

  @BC-09 @zone-3 @container-mode @network-grant @pending @phase-6
  Scenario: BC-09 — Zone 3 container tool receives temporary network grant before execution
    Given RAINBOW_TOOL_MODE is set to "container"
    And the tool command "impacket-smbclient" is present in the resolution table as Zone 3
    And the container service "exploit-ops" is running with network_mode none
    And per-operation P-020 human approval has been granted
    When jerry tool exec is called with arguments "impacket-smbclient //10.0.0.1/ADMIN$ -k"
    Then the wrapper grants a temporary network connection to the container before tool execution
    And the tool executes via docker compose exec within the granted network context
    And the wrapper revokes the network connection unconditionally after tool completion
    And the network revocation occurs even when the tool exits with a non-zero code

  @BC-09 @zone-3 @container-mode @network-grant @pending @phase-6
  Scenario: BC-09 — network revocation is unconditional on tool failure
    Given RAINBOW_TOOL_MODE is set to "container"
    And the tool command "msfconsole" is present in the resolution table as Zone 3
    And the container service "exploit-msf" is running with network_mode none
    And per-operation P-020 human approval has been granted
    When jerry tool exec is called with arguments "msfconsole -x exit"
    And the tool exits with a non-zero exit code
    Then the wrapper revokes the network connection unconditionally
    And the exit code surfaced to the caller reflects the tool failure, not the revocation

  # ---------------------------------------------------------------------------
  # Config precedence: CLI > env > file > default
  # ADR ref: L1 Configuration Mechanism — four-level hierarchy
  # ---------------------------------------------------------------------------

  @config-precedence @ADR-PROJ023-001
  Scenario: Config precedence — CLI flag overrides environment variable
    Given RAINBOW_TOOL_MODE is set to "container"
    And the tool command "checkov" is present in the resolution table as Zone 1
    And the container service "cloud-auditor" is running
    When jerry tool exec is called with "--mode local checkov --version"
    Then the wrapper executes "checkov --version" directly on the host without docker
    And the exit code is 0

  @config-precedence @ADR-PROJ023-001
  Scenario: Config precedence — environment variable overrides config file
    Given RAINBOW_TOOL_MODE is set to "container"
    And the config file specifies "default_mode: local"
    And the tool command "syft" is present in the resolution table as Zone 1
    And the container service "scanner" is running
    When jerry tool exec is called with arguments "syft --version"
    Then the effective mode is "container" (environment variable wins over config file)
    And the wrapper invokes "docker compose exec -T scanner syft --version"

  @config-precedence @ADR-PROJ023-001
  Scenario: Config precedence — config file overrides hardcoded default
    Given RAINBOW_TOOL_MODE is unset
    And the config file specifies "default_mode: container"
    And the tool command "trivy" is present in the resolution table as Zone 1
    And the container service "compliance" is running
    When jerry tool exec is called with arguments "trivy --version"
    Then the effective mode is "container" (config file wins over hardcoded default of local)
    And the wrapper invokes a docker compose exec command

  @config-precedence @ADR-PROJ023-001
  Scenario: Config precedence — hardcoded default is local when all other levels are absent
    Given RAINBOW_TOOL_MODE is unset
    And no config file is present
    And the tool command "checkov" is present in the resolution table as Zone 1
    When jerry tool exec is called with arguments "checkov --version"
    Then the effective mode is "local" (hardcoded safe default)
    And the wrapper executes "checkov --version" directly on the host without docker

  # ---------------------------------------------------------------------------
  # Strict mode prevents --no-filter across all zones
  # ADR ref: L1 Configuration Mechanism — RAINBOW_STRICT_MODE
  # ---------------------------------------------------------------------------

  @strict-mode @no-filter @security @OWASP-INPVAL
  Scenario: Strict mode rejects --no-filter regardless of zone
    Given RAINBOW_TOOL_MODE is set to "local"
    And RAINBOW_STRICT_MODE is set to "true"
    And the tool command "trivy" is present in the resolution table as Zone 1
    When jerry tool exec is called with "--no-filter trivy --version"
    Then the wrapper exits with a non-zero code
    And an error message is emitted containing "FORBIDDEN"
    And the tool is NOT executed

  @strict-mode @no-filter @security
  Scenario: --no-filter is permitted when RAINBOW_STRICT_MODE is false
    Given RAINBOW_TOOL_MODE is set to "local"
    And RAINBOW_STRICT_MODE is set to "false"
    And the tool command "checkov" is present in the resolution table as Zone 1
    When jerry tool exec is called with "--no-filter checkov --version"
    Then the wrapper executes "checkov --version" without applying the credential filter
    And the exit code is 0

  # ---------------------------------------------------------------------------
  # Longest-prefix matching (ADR R-1 mitigation)
  # Validates the resolution table matches the most-specific prefix
  # ---------------------------------------------------------------------------

  @resolution @longest-prefix
  Scenario: Resolution uses longest-prefix match for wildcard tool families
    Given RAINBOW_TOOL_MODE is set to "local"
    And the resolution table contains "impacket-*" mapped to service "exploit-ops"
    When jerry tool exec is called with arguments "impacket-GetADUsers --help"
    Then the tool is resolved via the "impacket-*" wildcard entry
    And the resolved service is "exploit-ops"
    And the exit code is not 1

  @resolution @wildcard-family
  Scenario Outline: Resolution correctly maps each tool family to its container service
    Given RAINBOW_TOOL_MODE is set to "local"
    And the tool command "<tool_prefix>" is present in the resolution table
    When jerry tool exec is called with arguments "<tool_prefix> --version"
    Then the resolved sub_skill is "<sub_skill>"
    And the resolved security zone is "<zone>"

    Examples:
      | tool_prefix     | sub_skill            | zone |
      | checkov         | rainbow-cloud        | 1    |
      | prowler         | rainbow-cloud        | 1    |
      | kubescape       | rainbow-cloud        | 1    |
      | syft            | rainbow-supply-chain | 1    |
      | grype           | rainbow-supply-chain | 1    |
      | trivy           | rainbow-supply-chain | 1    |
      | subfinder       | rainbow-recon        | 2    |
      | httpx           | rainbow-recon        | 2    |
      | nuclei          | rainbow-recon        | 2    |
      | impacket-smbclient | rainbow-exploit   | 3    |
      | pwntools        | rainbow-exploit      | 3    |
      | msfconsole      | rainbow-exploit      | 3    |
      | empire          | rainbow-exploit      | 3    |
      | mitmproxy       | rainbow-runtime      | 2    |
      | frida           | rainbow-runtime      | 2    |

  # ---------------------------------------------------------------------------
  # Health check mode
  # ADR ref: L1 Tool Executor Specification — --health-check
  # ---------------------------------------------------------------------------

  @health-check @operations
  Scenario: --health-check reports running services without executing any tool
    Given RAINBOW_TOOL_MODE is set to "container"
    And at least one container service is running
    When jerry tool exec is called with "--health-check"
    Then no tool command is executed
    And the output contains service status for each entry in the resolution table
    And the exit code is 0 when all services are running

  @health-check @operations
  Scenario: --health-check exits non-zero when one or more services are down
    Given RAINBOW_TOOL_MODE is set to "container"
    And at least one container service is NOT running
    When jerry tool exec is called with "--health-check"
    Then the exit code is non-zero
    And a [DOWN] status line is emitted for the stopped service
