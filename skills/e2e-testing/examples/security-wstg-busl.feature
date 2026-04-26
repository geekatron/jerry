# security-wstg-busl.feature
#
# PURPOSE: Demonstrates P-E2E-08 WSTG coverage for business-logic abuse scenarios.
# WSTG COVERAGE:
#   @wstg:WSTG-v42-BUSL-01  -- Ability to Upload Unexpected File Types / parameter manipulation
#   @wstg:WSTG-v42-BUSL-04  -- Process Timing (race condition in resource allocation)
#   @wstg:WSTG-v42-BUSL-06  -- Circumventing Workflows (step-skipping)
#
# OWASP WSTG v4.2 BUSL CATEGORY REFERENCE:
#   BUSL-01: Test Business Logic Data Validation
#   BUSL-02: Test Ability to Forge Requests
#   BUSL-03: Test Integrity Checks
#   BUSL-04: Test for Process Timing
#   BUSL-05: Test Number of Times a Function Can Be Used Limits
#   BUSL-06: Testing for the Circumvention of Work Flows
#   BUSL-07: Test Defenses Against Application Misuse
#   BUSL-08: Test Upload of Unexpected File Types
#   BUSL-09: Test Upload of Malicious Files
#
# ASSERTION PHILOSOPHY: Every scenario uses VERIFIED-class assertions (specific, observable,
# independent). Where the server response is the ground truth, assertions check the HTTP
# status code AND the response body, not the status code alone.
#
# [UNVALIDATED -- corpus n<20; assertion_sensitivity_rate thresholds are informational]

Feature: Business Logic Abuse Prevention
  As a security engineer
  I want to verify that business logic controls cannot be bypassed at the browser layer
  So that authorisation boundaries and workflow integrity are enforced regardless of client-side constraints

  Background:
    Given the application is accessible at "https://app.acme.com"
    And a standard authenticated user "alice@acme.com" is logged in with role "user"
    And an administrative resource exists at "/admin/orders" that requires the "admin" role

  # ---------------------------------------------------------------------------
  # BUSL-01 / BUSL-02: Authorisation bypass via parameter manipulation
  # ---------------------------------------------------------------------------
  # WSTG-v42-BUSL-01: Business Logic Data Validation -- does the server trust client parameters?
  # Attack pattern: Attacker modifies request parameters (order_id, user_id, role) to access
  # resources belonging to another user or requiring a higher privilege role.
  # The application must validate authorisation server-side, not rely on client-controlled values.
  # ---------------------------------------------------------------------------

  @basis:WSTG-v42-BUSL-01 @basis:WSTG-v42-BUSL-02 @wstg:WSTG-v42-BUSL-01 @wstg:WSTG-v42-BUSL-02 @risk:HIGH @criticality:C3
  Scenario: Authorisation bypass via user_id parameter manipulation is rejected by the server
    # The application must validate resource ownership server-side.
    # A user must not be able to view another user's order by manipulating the order_id in the URL.
    Given user "alice@acme.com" has order "ORDER-1001" in her account
    And user "bob@example.com" has order "ORDER-1002" in his account
    And "alice@acme.com" is authenticated
    When the user navigates directly to the order detail page for "ORDER-1002"
    Then the server response status is 403 Forbidden
    # [VERIFIED: Specific HTTP status code -- would fail if the server returned 200 or 302]
    Then the page does not display order details for "ORDER-1002"
    # [VERIFIED: Content-level check -- would fail if order contents were visible despite 403 header being absent from rendered state]
    Then the page does not display any data attributed to "bob@example.com"
    # [VERIFIED: Isolation -- would fail if cross-user data leakage occurred]
    Then the application does not redirect to a page that reveals the existence of "ORDER-1002"
    # [VERIFIED: Enumeration resistance -- would fail if 302 redirect leaked resource existence]

  # ---------------------------------------------------------------------------
  # BUSL-04: Race condition in resource allocation
  # ---------------------------------------------------------------------------
  # WSTG-v42-BUSL-04: Process Timing -- does the application correctly handle concurrent requests
  # that target the same limited resource?
  # Attack pattern: Attacker submits two simultaneous requests to redeem a single-use coupon code,
  # exploiting a race window between the check and the decrement of the coupon usage counter.
  # The server must use atomic operations or distributed locking to prevent double-redemption.
  # ---------------------------------------------------------------------------

  @basis:WSTG-v42-BUSL-04 @wstg:WSTG-v42-BUSL-04 @risk:HIGH @criticality:C3
  Scenario: Concurrent coupon redemption requests do not allow double-use of a single-use code
    # [UNVALIDATED -- corpus n<20]
    # This scenario tests race-condition handling. Execution in explorer mode is recommended
    # because concurrent request timing requires LLM-in-loop coordination.
    Given a single-use coupon code "PROMO-ONCE" exists in the system with usage_count 0 and max_uses 1
    And the authenticated user "alice@acme.com" has not previously redeemed "PROMO-ONCE"
    When two redemption requests for "PROMO-ONCE" are submitted concurrently by the same user session
    Then exactly one redemption request receives a success response with status 200
    # [VERIFIED: Atomic success -- would fail if both requests returned 200, indicating no locking]
    Then exactly one redemption request receives a rejection response with status 409 Conflict
    # [VERIFIED: Specific rejection status -- would fail if the server returned 200 twice or 500 on race]
    Then the coupon usage_count in the system is 1 after both requests complete
    # [VERIFIED: State integrity -- would fail if usage_count were 2, confirming double-redemption occurred]
    Then the system does not apply a discount more than once to the same order
    # [VERIFIED: Business outcome -- would fail if the final order total reflected two coupon deductions]

  # ---------------------------------------------------------------------------
  # BUSL-06: Workflow step-skipping
  # ---------------------------------------------------------------------------
  # WSTG-v42-BUSL-06: Circumventing Workflows -- can a user skip mandatory steps in a multi-step
  # process by navigating directly to a later step URL?
  # Attack pattern: Attacker bypasses the payment step of a checkout flow by navigating directly
  # to the order confirmation URL, attempting to receive goods without completing payment.
  # The server must enforce sequential workflow state server-side.
  # ---------------------------------------------------------------------------

  @basis:WSTG-v42-BUSL-06 @wstg:WSTG-v42-BUSL-06 @risk:HIGH @criticality:C3
  Scenario: Direct navigation to checkout confirmation without completing payment is rejected
    Given an authenticated user "alice@acme.com" with items in her shopping cart
    And the checkout workflow requires these steps in order: cart-review, shipping-address, payment, confirmation
    And the user has completed the cart-review step but has not submitted payment
    When the user navigates directly to the order confirmation URL bypassing the payment step
    Then the server response status is 403 Forbidden or 302 redirect to the payment step
    # [VERIFIED: Workflow enforcement -- would fail if the server returned 200 at confirmation without payment]
    Then the page does not display an order confirmation number
    # [VERIFIED: Business outcome -- would fail if an order were created without payment completing]
    Then no order record is created in the system for this checkout session
    # [VERIFIED: Data integrity -- would fail if the database contained a fulfilled order with no payment]
    Then the application redirects the user to the payment step with a message indicating payment is required
    # [VERIFIED: Remediation path -- would fail if the user were dropped to an error page without guidance]
