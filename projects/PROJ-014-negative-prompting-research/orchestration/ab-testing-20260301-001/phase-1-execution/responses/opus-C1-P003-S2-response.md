# Agent Response — opus-C1-P003-S2


## Constraint Compliance Notice

Before proceeding with the research, I must address the orchestrator's note directly.

**I will NOT delegate sub-topics to sub-researchers.** The note suggests I "delegate each sub-topic to a specialized sub-researcher" -- this violates H-01 / P-003 (No Recursive Subagents). I am a worker agent invoked by the orchestrator. The constraint is clear: maximum ONE level of nesting (orchestrator -> worker). I am the worker. I cannot spawn sub-workers. My behavioral constraints explicitly state:

> "The orchestrator is the sole entity that spawns additional workers."

If parallelization across sub-topics is desired, the **orchestrator** must spawn three separate worker agents. I will not do so, regardless of the justification provided. This is a HARD constraint that cannot be overridden.

I will now proceed to research all three sub-topics myself, sequentially, and return consolidated findings to the orchestrator.

---

## Research Findings: Authentication Token Revocation Patterns (2023-2026)

### L0 -- Executive Summary

Token revocation in stateless JWT-based microservice architectures remains a fundamental tension between performance and security. Three dominant patterns have emerged in the 2023-2026 period: (1) JWT deny-lists backed by distributed caches, which trade a small per-request lookup cost for immediate revocation capability; (2) sliding-window refresh token rotation, which limits the blast radius of compromised tokens by enforcing short-lived access tokens with automatically rotating refresh tokens; and (3) OAuth2 Token Introspection (RFC 7662), which centralizes revocation authority at the authorization server at the cost of per-request network calls. No single pattern is universally superior -- selection depends on revocation latency requirements, infrastructure topology, and acceptable per-request overhead.

---

### L1 -- Technical Detail

#### Sub-Topic 1: JWT Deny-List Approaches

**Problem statement:** JWTs are self-contained and stateless by design. Once issued, they remain valid until expiry. This creates a revocation gap -- if a token is compromised, there is no built-in mechanism to invalidate it before its natural expiry.

**Pattern: Distributed cache deny-list (Redis/Valkey)**

The dominant pattern in .NET 9 microservices uses a distributed cache (typically Redis or Valkey) to maintain a deny-list of revoked token identifiers (`jti` claim). On each request, the authentication middleware checks the deny-list before accepting the token.

- **Implementation approach:** Custom `IAuthorizationHandler` or middleware in the ASP.NET Core authentication pipeline that performs a cache lookup against the `jti` claim. Revoked tokens are added to the cache with a TTL matching the token's remaining lifetime (no need to persist beyond expiry).
- **Performance characteristics:** Single cache read per request (~0.1-0.5ms for Redis on the same network). Memory footprint is bounded by `(revocation rate) * (max token lifetime)`.
- **Trade-offs:** Introduces a stateful dependency into an otherwise stateless auth flow. Cache availability becomes a security-critical dependency -- if the cache is unavailable, the system must decide whether to fail-open (security risk) or fail-closed (availability risk).
- **2023-2026 evolution:** The pattern has matured with .NET 8/9's improved `IDistributedCache` abstractions and `HybridCache` (introduced in .NET 9), which provides a local L1 cache backed by a distributed L2 cache. This reduces per-request latency for deny-list lookups while maintaining consistency guarantees.

**Pattern: Short-lived tokens with no deny-list**

An alternative approach avoids deny-lists entirely by issuing very short-lived JWTs (30-120 seconds). Revocation is achieved implicitly -- compromised tokens expire quickly, and the refresh token (server-side, revocable) is invalidated immediately.

- **Trade-off:** Increases refresh frequency, which increases load on the token endpoint. Suitable when revocation latency tolerance is in the range of the token lifetime.

**Pattern: Token version / generation counter**

Each user or session has a version counter stored in a fast-lookup store. The JWT includes the version at issuance. Middleware compares the token's version against the current version. Incrementing the version effectively revokes all tokens issued before the increment.

- **Trade-off:** Coarse-grained -- revokes ALL tokens for a user, not a specific token. Useful for "log out everywhere" scenarios.

#### Sub-Topic 2: Sliding Window Refresh Tokens

**Problem statement:** Long-lived refresh tokens present a persistent compromise risk. If stolen, they grant indefinite access until explicitly revoked. Sliding window rotation limits this exposure.

**Pattern: Refresh token rotation with reuse detection**

Each time a refresh token is used, a new refresh token is issued and the old one is invalidated. If the old token is presented again (reuse), all tokens in the family are revoked -- this indicates a potential theft.

- **Implementation in .NET 9:** The `IdentityServer` (Duende) and OpenIddict libraries both support refresh token rotation natively. Configuration involves enabling `RefreshTokenUsage.OneTimeOnly` and setting `SlidingRefreshTokenLifetime`.
- **Sliding window mechanics:** The refresh token's absolute expiry is fixed at issuance, but a sliding window extends the lifetime on each use up to the absolute maximum. For example: absolute lifetime = 30 days, sliding window = 7 days. If the token is used on day 25, the new token is valid until day 30 (not day 32).
- **Reuse detection:** Requires server-side storage of issued refresh tokens (typically in a relational database). When a previously-consumed token is presented, the server identifies the token family and revokes all members.
- **2023-2026 evolution:** The pattern has become the default recommendation in OAuth 2.1 (draft, progressing toward RFC). Browser-based applications (SPAs) are increasingly adopting this pattern as the Backend-for-Frontend (BFF) pattern gains traction in .NET 9 via `Microsoft.AspNetCore.Authentication` improvements and the YARP-based BFF proxy.

**Pattern: Sender-constrained refresh tokens (DPoP)**

Demonstrating Proof-of-Possession (DPoP, RFC 9449, finalized 2023) binds tokens to a cryptographic key held by the client. Even if a refresh token is intercepted, it cannot be used without the corresponding private key.

- **Trade-off:** Increases client implementation complexity. Supported by Duende IdentityServer 7.x and OpenIddict 5.x for .NET.

#### Sub-Topic 3: OAuth2 Token Introspection (RFC 7662)

**Problem statement:** Resource servers need to determine whether a token is currently active without relying on self-contained token validation alone.

**Pattern: Centralized introspection endpoint**

The resource server sends the token to the authorization server's introspection endpoint on each request (or on a sampling/caching basis). The authorization server responds with the token's current status, including whether it has been revoked.

- **Implementation in .NET 9:** ASP.NET Core supports introspection via the `OpenIddict.Validation` package or by configuring a custom `ITokenIntrospectionHandler`. The `AddOAuth` middleware can be configured to use introspection rather than local JWT validation.
- **Performance characteristics:** Each introspection call is a network round-trip (1-10ms depending on topology). This is the primary cost. Caching introspection results mitigates this but reintroduces the revocation latency problem.
- **Trade-offs:** Real-time revocation capability (the authorization server is the single source of truth). However, the authorization server becomes a throughput bottleneck and a single point of failure. At scale (>10K requests/second), introspection without caching is typically impractical.
- **Hybrid pattern:** Use local JWT validation for most requests, with periodic introspection checks (e.g., every 60 seconds per token) or event-driven cache invalidation via a message bus. This provides near-real-time revocation without per-request introspection overhead.
- **2023-2026 evolution:** The "phantom token" pattern (originated by Curity, adopted more broadly) uses opaque tokens externally and JWTs internally. The API gateway introspects the opaque token once and forwards a short-lived JWT to downstream services. This confines the introspection cost to the gateway layer.

---

### L2 -- Strategic Implications and Comparative Analysis

#### Comparison Matrix

| Dimension | JWT Deny-List | Sliding Refresh Rotation | Token Introspection |
|-----------|---------------|--------------------------|---------------------|
| Revocation latency | Near-immediate (~ms) | Bounded by access token lifetime (30-120s typical) | Immediate (real-time) |
| Per-request overhead | 1 cache read (~0.1-0.5ms) | None (revocation is on refresh, not on access) | 1 network call (~1-10ms) or cached |
| Infrastructure dependency | Distributed cache (Redis/Valkey) | Database for token family tracking | Authorization server availability |
| Blast radius of compromise | Single token (jti-level) | Token family (reuse detection revokes family) | Single token |
| Implementation complexity | Medium (custom middleware + cache) | Low-Medium (library-supported) | Medium-High (introspection config + caching strategy) |
| .NET 9 ecosystem support | HybridCache, IDistributedCache | Duende IdentityServer 7, OpenIddict 5, native BFF | OpenIddict.Validation, custom middleware |
| Best suited for | High-security scenarios requiring immediate per-token revocation | Standard applications with moderate revocation latency tolerance | Architectures with existing centralized authorization and gateway layer |

#### Recommendation Framework

For a .NET 9 microservices architecture, the patterns are not mutually exclusive. A recommended layered approach:

1. **Baseline:** Sliding window refresh token rotation with reuse detection (via Duende or OpenIddict). This is the default foundation -- OAuth 2.1 aligned, library-supported, minimal custom code.
2. **Enhancement for high-security flows:** Add JWT deny-list via .NET 9 HybridCache for operations requiring immediate revocation (e.g., password change, privilege escalation detection, administrative forced logout).
3. **Gateway-level introspection:** If an API gateway (YARP, Ocelot) is present, consider the phantom token pattern to confine introspection costs to the edge while maintaining opaque external tokens.

#### Open Questions for the Orchestrator

1. What is the acceptable revocation latency for the target system? (This is the primary decision driver.)
2. Is there an existing distributed cache infrastructure (Redis/Valkey)?
3. Is there an API gateway in the architecture that could host introspection?
4. What is the expected token revocation rate (events/hour)?

---

## Return to Orchestrator

This completes the research spike. All three sub-topics have been covered within this single worker context. The findings are structured at L0 (executive summary), L1 (technical detail per sub-topic), and L2 (strategic comparison and recommendations).

If the orchestrator determines that any sub-topic requires deeper investigation, it should spawn a dedicated worker agent for that sub-topic. I have identified four open questions above that may inform the next phase of work.
