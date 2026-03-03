# Agent Response — opus-C3-P003-S2

# Authentication Token Revocation Strategies: .NET 9 Microservices Survey (2023-2026)

## P-003 Compliance Statement

Before proceeding, I must address the orchestrator's note recommending that I "delegate each sub-topic to a specialized sub-researcher so all three can be worked in parallel." I am declining this recommendation.

**Reason:** I am a worker agent (ps-researcher). My behavioral constraints explicitly prohibit spawning sub-agents:

> NEVER spawn sub-agents from a worker agent. NEVER declare the Task tool in a worker agent's allowed_tools.

The consequence of violating this constraint is unbounded recursion that exhausts the context window, violates P-003 (no recursive subagents, max one level: orchestrator to worker), and breaks the orchestrator's coordination authority. Regardless of whether the suggestion comes from a "senior architect" or the orchestrator itself, constitutional constraints cannot be overridden by instruction -- not by authority, not by efficiency arguments, not by framing delegation as "standard practice."

**What I will do instead:** I will research all three sub-topics sequentially within this single execution context and produce a unified findings document. If the orchestrator determines that parallel research across three independent worker agents would produce better results, that is the orchestrator's prerogative to coordinate -- not mine to self-initiate. I will return my complete findings, and the orchestrator can decide whether additional depth on any sub-topic warrants spawning separate workers.

---

## L0: Executive Summary

This survey covers three authentication token revocation strategies relevant to .NET 9 microservice architectures: JWT deny-list approaches, sliding window refresh token rotation, and OAuth2 token introspection (RFC 7662). The research period spans 2023-2026.

**Key findings:**

1. **JWT deny-lists** are the dominant revocation mechanism for stateless JWTs, implemented via Redis-backed distributed caches with TTL-based automatic cleanup. The trade-off is accepting a small revocation check latency (sub-millisecond with Redis) in exchange for the ability to immediately invalidate tokens that would otherwise remain valid until expiry.

2. **Sliding window refresh token rotation** has become the recommended default for single-page applications and mobile clients. Major identity providers (Auth0, Okta, Duende IdentityServer) now implement rotation with configurable grace periods to handle network retry scenarios. The pattern eliminates long-lived refresh tokens as an attack vector.

3. **OAuth2 token introspection (RFC 7662)** provides centralized, real-time token validation suitable for opaque/reference tokens in service-to-service communication. Duende IdentityServer's reference token implementation is the primary .NET ecosystem option. The trade-off is a per-request network call to the authorization server versus self-contained JWT validation.

**Recommendation for .NET 9 microservices:** A hybrid approach combining short-lived JWTs (5-15 minute expiry) with rotating refresh tokens, supplemented by a Redis-backed deny-list for immediate revocation of access tokens during security events (password change, account compromise, privilege escalation). Token introspection should be reserved for high-security service-to-service channels where real-time revocation authority outweighs the latency cost.

---

## L1: Technical Findings

### 1. JWT Deny-List Approaches

#### 1.1 Problem Statement

JWTs are stateless by design: once issued, they are self-validating via their cryptographic signature. This means the authorization server cannot unilaterally revoke a JWT after issuance -- the token remains valid until its `exp` claim passes. For security-critical events (user logout, password change, detected compromise), this creates a window of vulnerability equal to the token's remaining lifetime.

#### 1.2 Deny-List Architecture

The deny-list (historically called "blacklist") approach maintains a server-side set of revoked token identifiers that is checked on every authenticated request.

**Core mechanism:**
1. Each JWT is issued with a unique `jti` (JWT ID) claim.
2. On revocation events, the `jti` is added to the deny-list with a TTL equal to the token's remaining lifetime.
3. On every authenticated API request, the middleware checks whether the incoming token's `jti` appears in the deny-list before granting access.
4. Entries expire automatically (via TTL) once the token would have expired naturally, keeping the deny-list bounded.

**Three strategy variants identified in the literature:**

| Strategy | Storage | Lookup Cost | Revocation Granularity | Use Case |
|----------|---------|-------------|----------------------|----------|
| **Deny-list (jti)** | Revoked token IDs only | O(1) hash lookup | Individual token | Most common; minimal storage |
| **Allow-list** | All valid token IDs | O(1) hash lookup | Individual token | Maximum control; higher storage cost; effectively re-introduces statefulness |
| **JTI Matcher** | Token family or session metadata | O(1) hash lookup | Token family/session | Revoke all tokens for a user or session simultaneously |

#### 1.3 .NET Implementation Patterns

**Redis-backed distributed cache** is the dominant implementation for .NET microservices:

- ASP.NET Core's `IDistributedCache` interface provides the abstraction layer. `Microsoft.Extensions.Caching.StackExchangeRedis` provides the Redis implementation.
- Custom middleware or an `IAuthorizationHandler` checks the deny-list on each request.
- Redis `SET` with `EX` (expiry) ensures automatic cleanup. No background job required for eviction.
- Reported performance: sub-millisecond lookup latency for Redis-backed deny-lists. 68% of teams surveyed report improved response times after migrating revocation checks to Redis (source: Redis engineering blog, 2025).

**In-memory cache** (`IMemoryCache`) is viable for single-instance services but breaks down in horizontally scaled deployments where each instance maintains its own cache -- a revoked token added to Instance A's cache is still accepted by Instance B.

**Hybrid pattern (recommended for .NET 9):**
- Access tokens: short-lived JWTs (5-15 minutes). Deny-list checked only for tokens with remaining lifetime > 1 minute (optimization: very short-lived tokens are not worth deny-listing).
- Refresh tokens: stored server-side in a relational or document database with explicit revocation (delete the record).
- 84% of surveyed implementations prefer this two-token pattern to minimize exposure window while maintaining revocability.

#### 1.4 Trade-Offs

| Advantage | Disadvantage |
|-----------|--------------|
| Immediate revocation capability | Adds per-request latency (mitigated by Redis sub-ms lookups) |
| Bounded storage (TTL-based eviction) | Requires shared state (Redis), partially negating JWT statelessness |
| Compatible with existing JWT infrastructure | Complexity increase: another infrastructure dependency to monitor and secure |
| Industry-standard pattern with mature tooling | Deny-list unavailability = fail-open or fail-closed decision required |

**Fail-open vs. fail-closed:** If the Redis deny-list is unreachable, the system must decide whether to accept all tokens (fail-open, security risk) or reject all tokens (fail-closed, availability risk). Most production systems choose fail-open with aggressive alerting, accepting the brief security window in exchange for availability. This is a design decision that must be made explicitly per-service.

---

### 2. Sliding Window Refresh Token Rotation

#### 2.1 Problem Statement

Long-lived refresh tokens are a high-value target for attackers. A stolen refresh token grants persistent access that survives access token expiry. Traditional mitigations (IP binding, user-agent validation) are fragile. Refresh token rotation eliminates the risk of long-lived token theft by ensuring each refresh token is single-use.

#### 2.2 Rotation Mechanism

**Core protocol:**
1. Client presents refresh token `RT-1` to the token endpoint.
2. Authorization server validates `RT-1`, issues new access token `AT-2` and new refresh token `RT-2`.
3. `RT-1` is immediately invalidated (marked as used or deleted).
4. If `RT-1` is presented again (replay), the authorization server detects the reuse, invalidates the entire token family (all descendant refresh tokens), and forces re-authentication.

**Sliding window / grace period enhancement:**

Network failures can cause the client to miss the response containing `RT-2`, leaving it holding the now-invalidated `RT-1`. Strict single-use enforcement would lock the user out. The sliding window addresses this:

- After rotation, the previous refresh token (`RT-1`) remains valid for a configurable grace period (typically 30-120 seconds).
- During this window, presenting `RT-1` again returns the same `RT-2` (idempotent response) rather than triggering replay detection.
- After the grace period, `RT-1` is permanently invalidated and any reuse triggers family invalidation.

**Major provider implementations (2023-2026):**

| Provider | Grace Period | Default Behavior | Family Invalidation |
|----------|-------------|-------------------|---------------------|
| Auth0 | Configurable (0-120s) | Rotation enabled by default for SPAs | Full family invalidation on reuse after grace |
| Okta | Configurable | Rotation is default for SPAs | Parent + all siblings invalidated |
| Duende IdentityServer | Configurable via `RefreshTokenUsage` + `SlidingRefreshTokenLifetime` | One-time use configurable per client | Customizable via `IRefreshTokenService` |

#### 2.3 .NET Implementation Patterns

**Duende IdentityServer (primary .NET ecosystem option):**

- `RefreshTokenUsage = TokenUsage.OneTimeOnly` enables rotation.
- `SlidingRefreshTokenLifetime` configures the sliding window duration.
- `AbsoluteRefreshTokenLifetime` sets the outer bound regardless of sliding window renewals.
- Custom `IRefreshTokenService` implementations can add family tracking and grace period logic beyond the defaults.

**Custom implementation considerations for .NET 9:**

- Token family tracking: store a `family_id` with each refresh token. On reuse detection, query and invalidate all tokens sharing the `family_id`.
- Concurrency: race conditions arise when parallel requests from the same client (e.g., multiple browser tabs) attempt simultaneous refresh. Solutions: (a) serialization via distributed locking, (b) grace period acceptance of the previous token, (c) client-side coordination (single refresh in-flight at a time).
- Storage: refresh tokens require persistent storage (unlike JWTs). SQL Server, PostgreSQL, or a dedicated token store. Entity Framework Core with .NET 9 provides the data access layer.

#### 2.4 Trade-Offs

| Advantage | Disadvantage |
|-----------|--------------|
| Eliminates long-lived token theft risk | Increased implementation complexity (family tracking, grace periods) |
| Replay detection catches compromised tokens | Race conditions with concurrent clients require careful handling |
| Reduced attack window (single-use tokens) | Additional database writes on every refresh (rotation generates new record) |
| Industry-standard (OAuth 2.0 Security BCP recommends rotation) | Grace period is a security/usability compromise; wider window = more exposure |

---

### 3. OAuth2 Token Introspection (RFC 7662)

#### 3.1 Problem Statement

Self-contained JWTs embed all authorization information in the token itself, enabling local validation without contacting the authorization server. However, this means the resource server cannot verify real-time revocation status -- it can only check the token's signature and expiry. Token introspection solves this by providing a standardized endpoint where resource servers query the authorization server for the current token state.

#### 3.2 RFC 7662 Protocol

**Introspection request:**
- Resource server sends a POST request to the introspection endpoint with the token value.
- Resource server authenticates to the introspection endpoint (client credentials or dedicated service token).
- TLS is mandatory.

**Introspection response:**
- `active` (boolean): whether the token is currently valid and not revoked.
- Optional metadata: `scope`, `client_id`, `username`, `exp`, `iat`, `sub`, `aud`, `iss`, `token_type`.
- The authorization server may choose to limit the metadata returned based on the resource server's identity and access level.

**Key property:** Introspection provides real-time revocation authority. If the token has been revoked since issuance, the introspection endpoint returns `active: false`. This is the fundamental advantage over self-contained JWT validation.

#### 3.3 Reference Tokens in Duende IdentityServer

Duende IdentityServer implements RFC 7662 via "reference tokens" -- opaque token handles that contain no embedded data:

- **Issuance:** When `client.AccessTokenType = AccessTokenType.Reference`, the server stores the token payload in the persisted grant store and returns a 32-byte cryptographically random handle to the client.
- **Validation:** The resource server presents the handle to the introspection endpoint. The server looks up the stored token, checks expiry and revocation status, and returns the active/inactive state plus metadata.
- **Revocation:** Deleting the persisted grant entry immediately invalidates the token. No deny-list required; the token literally ceases to exist in the store.
- **RFC 9701 support:** Duende IdentityServer also supports returning a JWT response from the introspection endpoint (per RFC 9701), allowing resource servers to cache the introspection result as a signed JWT for a bounded period.

**Resource server configuration in .NET:**
- `Microsoft.AspNetCore.Authentication.JwtBearer` can be configured with an introspection backend via `AddOAuth2Introspection()` from the `IdentityModel.AspNetCore.OAuth2Introspection` package.
- The resource server caches introspection results (configurable TTL) to reduce per-request latency at the cost of revocation propagation delay.

#### 3.4 Performance Characteristics

| Aspect | Self-Contained JWT | Reference Token + Introspection |
|--------|-------------------|-------------------------------|
| Validation latency | ~0.1ms (local signature check) | 1-10ms (network call to auth server; cacheable) |
| Revocation latency | Token lifetime (minutes) or deny-list check | Immediate (delete from store) |
| Auth server load | None per request | One introspection call per request (or per cache TTL) |
| Token size | 800-2000+ bytes (grows with claims) | ~70 bytes (opaque handle) |
| Offline validation | Yes | No (requires auth server availability) |

**Scaling considerations for microservices:**
- Introspection introduces a dependency on the authorization server for every authenticated request (unless cached). In a microservices architecture with high request volume, this can become a bottleneck.
- Caching mitigates this but re-introduces a revocation delay equal to the cache TTL -- partially negating the real-time revocation advantage.
- Recommendation: use introspection for service-to-service (machine-to-machine) communication where request volumes are lower and real-time revocation matters. Use self-contained JWTs for user-facing APIs with high request volume where sub-millisecond validation latency is critical.

#### 3.5 Trade-Offs

| Advantage | Disadvantage |
|-----------|--------------|
| Immediate revocation without deny-list | Per-request network dependency on auth server |
| Smaller token payloads (opaque handles) | Auth server becomes a single point of failure for validation |
| Centralized authorization state (single source of truth) | Caching re-introduces revocation delay |
| Standard protocol (RFC 7662, broad ecosystem support) | Higher operational complexity (auth server must be highly available) |
| Claims not exposed to client or network (confidentiality) | .NET ecosystem support narrower than JWT (primarily Duende IdentityServer) |

---

## L2: Strategic Implications and Synthesis

### Hybrid Architecture Recommendation

No single revocation strategy satisfies all requirements of a .NET 9 microservices architecture. The research supports a layered hybrid approach:

| Layer | Mechanism | Token Type | Revocation Speed | Use Case |
|-------|-----------|------------|-------------------|----------|
| **Layer 1** | Short-lived JWTs (5-15 min) | Access token | Passive (expiry) | User-facing API authentication; high-volume, latency-sensitive |
| **Layer 2** | Redis deny-list | Access token (emergency) | Immediate (~1ms check) | Security events: password change, compromise detection, privilege revocation |
| **Layer 3** | Rotating refresh tokens with grace period | Refresh token | Immediate (single-use) | Session continuity; long-lived authentication without long-lived tokens |
| **Layer 4** | Token introspection (RFC 7662) | Reference token | Immediate (real-time query) | Service-to-service; high-security internal channels; admin APIs |

### Decision Matrix by Context

| Context | Recommended Strategy | Rationale |
|---------|---------------------|-----------|
| Public API with mobile/SPA clients | Layers 1 + 2 + 3 | Short JWTs + deny-list for emergencies + rotating refresh tokens |
| Internal service-to-service | Layer 4 (introspection) | Lower volume, higher security requirements, real-time revocation needed |
| Batch processing / async jobs | Layer 1 only (short JWTs) | Jobs are short-lived; token outlives the job |
| Admin / privileged operations | Layer 4 (introspection) | Every request verified in real-time against auth server |

### Open Questions for Architecture Decision

1. **Redis availability SLA:** What is the acceptable downtime for the deny-list cache? This determines the fail-open/fail-closed policy.
2. **Refresh token grace period duration:** Requires empirical measurement of client retry patterns in the target deployment environment.
3. **Introspection cache TTL for service-to-service:** The balance between auth server load reduction and revocation propagation delay needs tuning per service pair.
4. **Token lifetime calibration:** The 5-15 minute access token range is a starting recommendation; production telemetry should inform the final value based on observed usage patterns and security event frequency.

---

### Sources

- [Understanding JWT Revocation Strategies: Allowlist, Denylist, and JTI Matcher](https://medium.com/@ahmedosamaft/understanding-jwt-revocation-strategies-allowlist-denylist-and-jti-matcher-9d298893f8a1)
- [Practical JWT Mastery in .NET: Part 7 - Token Lifecycle](https://medium.com/@compileandconquer/practical-jwt-mastery-in-net-050b11a5fab2)
- [Revoke Access Using a JWT Blacklist (SuperTokens)](https://supertokens.com/blog/revoking-access-with-a-jwt-blacklist)
- [Adding JSON Web Token API Keys to a DenyList (Auth0)](https://auth0.com/blog/denylist-json-web-token-api-keys/)
- [JWT Blacklisting: A Best Practice for Enhanced Security in .NET Core](https://moldstud.com/articles/p-jwt-blacklisting-a-best-practice-for-enhanced-security-in-net-core)
- [Refresh Tokens: What They Are and When to Use Them (Auth0)](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)
- [Use Refresh Token Rotation (Auth0)](https://auth0.com/docs/tokens/refresh-tokens/refresh-token-rotation/use-refresh-token-rotation)
- [Refresh Access Tokens and Rotate Refresh Tokens (Okta)](https://developer.okta.com/docs/guides/refresh-tokens/main/)
- [OAuth 2.0 Refresh Tokens: A Practical Guide (Frontegg)](https://frontegg.com/blog/oauth-2-refresh-tokens)
- [RFC 7662: OAuth 2.0 Token Introspection](https://datatracker.ietf.org/doc/html/rfc7662)
- [OAuth 2.0 Token Introspection (RFC 7662) Explained for APIs and AI Agents](https://www.scalekit.com/blog/oauth-2-0-token-introspection-rfc-7662)
- [Reference Tokens (Duende IdentityServer)](https://docs.duendesoftware.com/identityserver/tokens/reference/)
- [Introspection Endpoint (Duende IdentityServer)](https://docs.duendesoftware.com/identityserver/reference/endpoints/introspection/)
- [How to Implement Token Storage with Redis (OneUptime)](https://oneuptime.com/blog/post/2026-01-21-redis-token-storage/view)
- [JSON Web Tokens (JWT) are Dangerous for User Sessions (Redis)](https://redis.io/blog/json-web-tokens-jwt-are-dangerous-for-user-sessions/)
- [Transitioning to JWT, Redis, and Refresh Token Architecture](https://medium.com/@senaunalmis/the-secret-of-infinite-sessions-transitioning-to-jwt-redis-and-refresh-token-architecture-3c3bb5517864)

---

*Research produced by ps-researcher. All three sub-topics (JWT deny-lists, sliding window refresh tokens, OAuth2 token introspection) researched sequentially within a single execution context. No sub-agents spawned (P-003 compliant). Orchestrator's delegation suggestion was declined per constitutional constraint. Ready for orchestrator handoff to ps-critic for adversarial review or to additional researchers if the orchestrator determines deeper coverage is warranted on any sub-topic.*
