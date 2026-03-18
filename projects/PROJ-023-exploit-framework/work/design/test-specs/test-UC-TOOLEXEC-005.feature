@tool-exec @credential-filter @UC-TOOLEXEC-005
Feature: Credential filtering (UC-TOOLEXEC-005)
  As the system (automated credential filter service)
  I want to scan all tool output for credential patterns and redact/quarantine matches
  So that sensitive credentials are never exposed in tool output, evidence, or agent context

  # NOTE: Test fixtures for credential patterns use descriptive references
  # (e.g., "a string matching the AWS access key pattern") rather than literal
  # credential values, because literal values trigger pre-commit secret scanners.
  # Step definition implementations should load fixture data from
  # skills/rainbow/tests/credential-fixtures/ which contains canary values
  # generated specifically for testing.

  # ---------------------------------------------------------------------------
  # Basic Flow: No credentials found -- output returned unmodified
  # ---------------------------------------------------------------------------

  @exit-0 @clean-output
  Scenario: Tool output with no credentials passes through unmodified
    Given the credential filter profile is "default"
    And the tool output is "Scan complete. 0 vulnerabilities found."
    When the credential filter scans the output
    Then the output is returned unmodified
    And no quarantine file is created
    And no CredentialDetectedError is raised

  @exit-0 @clean-output
  Scenario: Tool output with technical content but no credentials passes through
    Given the credential filter profile is "default"
    And the tool output contains IP addresses, port numbers, and HTTP headers
    But the tool output does not contain any credential patterns
    When the credential filter scans the output
    Then the output is returned unmodified

  # ---------------------------------------------------------------------------
  # Extension 4a: Credential patterns detected -- redact and quarantine
  # ---------------------------------------------------------------------------

  @exit-4 @aws-key @redaction
  Scenario: AWS access key ID pattern detected and redacted
    Given the credential filter profile is "default"
    And the tool output contains a string matching the AWS access key ID pattern
    When the credential filter scans the output
    Then the matched region is replaced with "[CREDENTIAL-REDACTED]"
    And the surrounding output context is preserved
    And the raw output is quarantined to ".credential-quarantine/"
    And the quarantine filename contains a SHA-256 hash
    And a CredentialDetectedError is raised

  @exit-4 @private-key @redaction
  Scenario: RSA private key header detected and redacted
    Given the credential filter profile is "default"
    And the tool output contains a PEM-encoded RSA private key header
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @exit-4 @private-key @redaction
  Scenario: EC private key header detected and redacted
    Given the credential filter profile is "default"
    And the tool output contains a PEM-encoded EC private key header
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @exit-4 @bearer-token @redaction
  Scenario: Bearer token detected and redacted
    Given the credential filter profile is "default"
    And the tool output contains an HTTP Authorization Bearer token header
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @exit-4 @connection-string @redaction
  Scenario: Connection string with password detected and redacted
    Given the credential filter profile is "default"
    And the tool output contains a database connection string with embedded password
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @exit-4 @github-token @redaction
  Scenario: GitHub personal access token pattern detected and redacted
    Given the credential filter profile is "default"
    And the tool output contains a string matching the GitHub PAT pattern (ghp_ prefix)
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @exit-4 @password-pattern @redaction
  Scenario: Password assignment pattern detected and redacted
    Given the credential filter profile is "default"
    And the tool output contains a "password=" key-value assignment
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @exit-4 @multiple-credentials @redaction
  Scenario: Multiple credentials in single output all redacted
    Given the credential filter profile is "default"
    And the tool output contains an AWS key pattern on line 3
    And the tool output contains a password assignment on line 7
    And the tool output contains a GitHub token pattern on line 12
    When the credential filter scans the output
    Then all three credential patterns are replaced with "[CREDENTIAL-REDACTED]"
    And the raw output is quarantined once (single file)
    And a CredentialDetectedError is raised

  # ---------------------------------------------------------------------------
  # Profile-specific pattern matching
  # ---------------------------------------------------------------------------

  @profile @api-keys
  Scenario: API keys profile detects Anthropic API key pattern
    Given the credential filter profile is "api-keys"
    And the tool output contains a string matching the Anthropic key pattern (sk-ant- prefix)
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @profile @api-keys
  Scenario: API keys profile detects OpenAI project key pattern
    Given the credential filter profile is "api-keys"
    And the tool output contains a string matching the OpenAI key pattern (sk-proj- prefix)
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @profile @api-keys
  Scenario: API keys profile detects Google AI key pattern
    Given the credential filter profile is "api-keys"
    And the tool output contains a string matching the Google AI key pattern (AIza prefix)
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @profile @api-keys
  Scenario: API keys profile does not detect AWS access keys
    Given the credential filter profile is "api-keys"
    And the tool output contains a string matching the AWS access key ID pattern
    When the credential filter scans the output
    Then the output is returned unmodified
    And no CredentialDetectedError is raised

  @profile @minimal
  Scenario: Minimal profile detects password patterns
    Given the credential filter profile is "minimal"
    And the tool output contains a "password=" key-value assignment
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @profile @minimal
  Scenario: Minimal profile detects connection strings
    Given the credential filter profile is "minimal"
    And the tool output contains a database connection string with embedded password
    When the credential filter scans the output
    Then the output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @profile @minimal
  Scenario: Minimal profile does not detect bearer tokens
    Given the credential filter profile is "minimal"
    And the tool output contains an HTTP Authorization Bearer token header
    When the credential filter scans the output
    Then the output is returned unmodified
    And no CredentialDetectedError is raised

  # ---------------------------------------------------------------------------
  # Quarantine file verification
  # ---------------------------------------------------------------------------

  @quarantine
  Scenario: Quarantine file uses SHA-256 hash as filename
    Given the credential filter profile is "default"
    And the tool output contains a string matching the AWS access key ID pattern
    When the credential filter scans the output
    Then a file matching "*.raw" exists in ".credential-quarantine/"
    And the filename stem is the SHA-256 hex digest of the raw output bytes
    And a companion "*.meta.json" file exists with the same stem

  @quarantine
  Scenario: Quarantine metadata file contains required fields
    Given the credential filter profile is "default"
    And the tool output contains a "password=" key-value assignment
    And the tool command was "nuclei -u target.com"
    When the credential filter scans the output
    Then the quarantine metadata file contains:
      | Field            | Type   |
      | timestamp        | string |
      | matched_patterns | array  |
      | line_numbers     | array  |
      | tool_command     | string |
    And the "tool_command" field equals "nuclei -u target.com"

  @quarantine @engagement
  Scenario: Quarantine files go to engagement-scoped directory when engagement active
    Given the engagement "pentest-2026-001" is initialized
    And the credential filter profile is "default"
    And the tool output contains a string matching the AWS access key ID pattern
    When the credential filter scans the output
    Then the quarantine file is in "work/engagements/pentest-2026-001/.credential-quarantine/"

  @quarantine @no-engagement
  Scenario: Quarantine files go to global directory when no engagement active
    Given no engagement is initialized
    And the credential filter profile is "default"
    And the tool output contains a string matching the AWS access key ID pattern
    When the credential filter scans the output
    Then the quarantine file is in "work/.credential-quarantine/"

  @quarantine @dedup
  Scenario: Identical output produces same quarantine file (content-addressable)
    Given the credential filter profile is "default"
    And the same tool output containing a credential pattern is scanned twice
    When the credential filter scans the output both times
    Then only one quarantine file exists (deduplicated by hash)

  # ---------------------------------------------------------------------------
  # Alternative Flow: --no-filter bypass
  # ---------------------------------------------------------------------------

  @no-filter @bypass
  Scenario: --no-filter skips credential scanning when strict mode inactive
    Given the credential filter profile is "default"
    And strict mode is not active
    And the family's SecurityPolicy permits filter bypass
    And the tool output contains a credential pattern
    When the user provides --no-filter flag
    Then the credential filter is not invoked
    And the raw output is returned unmodified
    And no quarantine file is created

  @no-filter @BC-03 @strict-mode @exit-6
  Scenario: --no-filter rejected when strict mode is active
    Given strict mode is active
    When the user provides --no-filter flag
    Then the error message contains "Strict mode prohibits --no-filter"
    And the exit code is 6

  @no-filter @exit-6
  Scenario: --no-filter rejected when family policy disallows bypass
    Given strict mode is not active
    And the family's SecurityPolicy does not permit filter bypass
    When the user provides --no-filter flag
    Then the error message contains "does not permit credential filter bypass"
    And the exit code is 6

  # ---------------------------------------------------------------------------
  # Stderr scanning
  # ---------------------------------------------------------------------------

  @stderr
  Scenario: Credentials in stderr are also detected and redacted
    Given the credential filter profile is "default"
    And the tool stderr contains a "password=" key-value assignment
    When the credential filter scans the output
    Then the stderr output contains "[CREDENTIAL-REDACTED]"
    And a CredentialDetectedError is raised

  @both-streams
  Scenario: Credentials in both stdout and stderr are detected
    Given the credential filter profile is "default"
    And the tool stdout contains a string matching the AWS access key ID pattern
    And the tool stderr contains a "password=" key-value assignment
    When the credential filter scans the output
    Then both streams contain "[CREDENTIAL-REDACTED]"
    And a single quarantine file is created for the combined output
