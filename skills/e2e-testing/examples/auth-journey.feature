# auth-journey.feature
#
# PURPOSE: Conventional E2E calibration example for P-E2E-02 declarative style.
# Used by:
#   - e2e-author: as a calibration reference for declarative Gherkin authoring
#   - e2e-verifier: as the primary calibration example for assertion-sensitivity classification
#   - e2e-test-generation.md: as the worked example referenced in the template
#
# WSTG COVERAGE:
#   @wstg:WSTG-v42-ATHN-01  -- credentials transported securely; auth failure handling
#   @wstg:WSTG-v42-SESS-02  -- session token expiry after inactivity
#   @wstg:WSTG-v42-SESS-07  -- logout clears session state
#   @wstg:WSTG-v42-ATHZ-01  -- authorisation: post-logout access denial
#
# ASSERTION CLASSIFICATION NOTES (inline, for e2e-verifier calibration):
#   VERIFIED assertions are marked with # [VERIFIED: reason]
#   RAN-ONLY assertions are marked with # [RAN-ONLY: reason]
#   See validation-strategy.md Section 1.3 for the full taxonomy.
#
# CORPUS STATUS: This file is a calibration reference, NOT a corpus entry.
# Do not count it toward the 20-scenario eval corpus threshold (P-E2E-09).
#
# [UNVALIDATED -- corpus n<20; assertion_sensitivity_rate thresholds are informational]

Feature: User Authentication Journey
  As a registered user of the application
  I want to authenticate securely using my credentials
  So that I can access my account while being protected from unauthorised access

  Background:
    Given the application is accessible at "https://app.acme.com"
    And the login page is rendered and ready to accept input
    And no active session cookie exists in the browser

  # ---------------------------------------------------------------------------
  # HAPPY PATH: Successful login
  # ---------------------------------------------------------------------------

  @basis:STORY-042 @basis:WSTG-v42-ATHN-01 @wstg:WSTG-v42-ATHN-01 @risk:HIGH @criticality:C2
  Scenario: Successful login with valid credentials
    # Tests: Level 1 (navigation), Level 2 (identity), Level 3 (isolation)
    Given a registered user with email "alice@acme.com" and a known valid password
    And the user "bob@example.com" also has a registered account with separate data
    When the user submits login credentials for "alice@acme.com"
    Then the application redirects the user to the dashboard
    # [RAN-ONLY: URL navigation confirmed but no content verified yet]
    Then the dashboard page displays "Welcome, alice@acme.com"
    # [VERIFIED: Identity-level check -- would fail if wrong user session established]
    Then the dashboard does not display any data attributed to "bob@example.com"
    # [VERIFIED: Isolation-level check -- would fail if horizontal privilege escalation occurred]
    Then a session cookie is present with the Secure and HttpOnly flags set
    # [VERIFIED: Security property -- would fail if session were issued without transport security flags]

  # ---------------------------------------------------------------------------
  # FAILURE PATH: Invalid credentials rejected
  # ---------------------------------------------------------------------------

  @basis:WSTG-v42-ATHN-01 @wstg:WSTG-v42-ATHN-01 @risk:HIGH @criticality:C2
  Scenario: Login fails with invalid credentials and does not leak account existence
    Given an unauthenticated user
    When the user submits login credentials with a valid email and an incorrect password
    Then the application displays an authentication error message
    # [RAN-ONLY: Confirms error is shown but does not verify message content]
    Then the error message reads "Invalid email or password"
    # [VERIFIED: Content-level check -- would fail if message leaked whether the email exists]
    Then the error message does not contain the word "email" or "password" individually in a way that confirms which field is wrong
    # [VERIFIED: Enumeration-resistance check -- would fail if error discriminated between bad email and bad password]
    Then no session cookie is set
    # [VERIFIED: Security property -- would fail if partial or invalid session were issued]
    Then the login page remains accessible for retry without a lockout
    # [VERIFIED: Rate-limit context -- subsequent assertions check lockout behaviour separately]

  # ---------------------------------------------------------------------------
  # BOUNDARY: Session expiry after inactivity timeout
  # ---------------------------------------------------------------------------

  @basis:WSTG-v42-SESS-02 @wstg:WSTG-v42-SESS-02 @risk:HIGH @criticality:C2
  Scenario: Session expires after configured inactivity timeout
    # Tests: session lifecycle boundary -- verifies token expiry is enforced server-side
    Given an authenticated user with email "alice@acme.com" and an active session cookie
    And the application session inactivity timeout is configured to 30 minutes
    When the session has been idle for longer than the configured inactivity timeout
    And the user attempts to access a protected resource
    Then the application rejects the request with a session-expired response
    # [VERIFIED: Security property -- would fail if expired session were accepted; server-side enforcement]
    Then the application redirects the user to the login page
    # [RAN-ONLY: Navigation confirmed; does not verify the expired session cookie is cleared]
    Then the session cookie previously issued is no longer accepted by the application
    # [VERIFIED: Token invalidation check -- would fail if the server still accepted the expired token]
    Then the previously visited protected resource is not accessible without re-authentication
    # [VERIFIED: Access control -- would fail if the resource were cached or accessible without a valid session]

  # ---------------------------------------------------------------------------
  # LOGOUT: Session cleared on explicit logout
  # ---------------------------------------------------------------------------

  @basis:WSTG-v42-SESS-07 @basis:WSTG-v42-ATHZ-01 @wstg:WSTG-v42-SESS-07 @wstg:WSTG-v42-ATHZ-01 @risk:HIGH @criticality:C2
  Scenario: Logout clears session and redirects to public page
    # Tests: WSTG-SESS-07 (logout invalidates session) and WSTG-ATHZ-01 (post-logout access denial)
    Given an authenticated user with email "alice@acme.com" and an active session cookie
    When the user initiates a logout
    Then the application redirects the user to the public login page
    # [RAN-ONLY: Navigation only -- does not verify the session was server-side invalidated]
    Then the session cookie is removed or invalidated in the browser
    # [VERIFIED: Client-side token clearance -- would fail if the cookie persisted after logout]
    Then a direct request to a protected dashboard URL returns a redirect to the login page
    # [VERIFIED: Post-logout access denial -- would fail if the session remained valid server-side]
    Then the previously issued session token is no longer accepted by the application
    # [VERIFIED: Server-side invalidation -- distinguishes from client-only cookie deletion]
    Then the application does not expose any residual session data on the public login page
    # [VERIFIED: Data leakage check -- would fail if logout cached user data in the page state]
