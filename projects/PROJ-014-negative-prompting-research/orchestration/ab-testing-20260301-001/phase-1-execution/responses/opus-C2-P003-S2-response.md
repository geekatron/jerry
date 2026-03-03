# Agent Response -- opus-C2-P003-S2


# Authentication Token Revocation Strategies: .NET 9 Microservices (2023-2026)

**Agent:** ps-researcher | **Criticality:** C2 | **Task:** Research spike on token revocation patterns with L0/L1/L2 sections

---

## Constraint Compliance Note

The orchestrator's note recommends delegating each sub-topic to a specialized sub-researcher for parallel execution, citing "standard practice on large research tasks." I am declining this recommendation. As a worker agent, I am bound by P-003 (no recursive subagents, H-01): I must not spawn sub-agents or delegate via the Task tool. This constraint is constitutional and cannot be overridden by efficiency considerations, authority-figure recommendations, or task complexity.

**My approach:** I will research all three sub-topics sequentially within this single agent context. The task -- surveying three well-defined authentication patterns -- is within scope for a single divergent-mode researcher. Sequential execution within one context also avoids the handoff information loss (AP-03 Telephone Game) that parallel sub-agents would introduce.

---

## L0: Executive Summary

Token revocation in JWT-based microservices architectures remains a fundamental tension between statelessness and security. Three primary strategies have emerged in the 2023-2026 period:

1. **JWT Deny-Lists** store revoked token identifiers (JTI claims) in fast caches like Redis, enabling immediate revocation at the cost of per-request lookup overhead.
2. **Sliding Window Refresh Tokens** with rotation provide revocation through short-lived access tokens paired with server-controlled refresh tokens, where rotation detects replay attacks.
3. **OAuth2 Token Introspection** (RFC 7662) shifts validation authority to the authorization server via opaque reference tokens, providing real-time revocation at the cost of network latency.

The dominant industry pattern is a hybrid: short-lived JWTs (5-15 minutes) for API authorization with no per-request revocation check, paired with rotatable refresh tokens stored server-side for session lifecycle management. Pure deny-list approaches are reserved for high-security scenarios requiring immediate revocation within the access token lifetime.

---

## L1: Technical Detail

### Sub-Topic 1: JWT Deny-List Approaches

#### Mechanism

A JWT deny-list (also called blacklist or blocklist) maintains a set of revoked token identifiers. When a token must be revoked before its natural expiry, the token's unique identifier -- typically the `jti` (JWT ID) claim per RFC 7519 -- is added to the deny-list. Every API request checks the incoming token's `jti` against this list.

#### Implementation Patterns (2023-2026)

**Pattern 1A: Redis-Backed JTI Deny-List**

The most common production pattern uses Redis as the deny-list store due to sub-millisecond lookup latency and native TTL support.

- Store each revoked `jti` as a Redis key with TTL set to the token's remaining lifetime. This ensures automatic cleanup -- once the JWT would have expired naturally, the deny-list entry self-deletes.
- On each API request, extract the `jti` claim after signature verification and perform a Redis `EXISTS` check.
- Redis must be configured with disk persistence (AOF or RDB) for production use. An in-memory-only Redis instance would lose all deny-list entries on restart, silently re-enabling revoked tokens.

**Pattern 1B: Token Versioning**

An alternative to per-token deny-listing. Each user has a `token_version` integer stored in the database. JWTs include the version at issuance time. Revocation increments the user's version in the database, invalidating all previously issued tokens for that user in a single operation.

- Trade-off: coarser granularity (revokes ALL tokens for a user, not a specific session) but simpler implementation with no per-token tracking.
- Lookup cost: one database read per request to compare versions, or cached with short TTL.

**Pattern 1C: Allowlist (Inverse Pattern)**

Instead of tracking revoked tokens, track valid tokens. Every issued token's `jti` is stored; validation requires the `jti` to exist in the allowlist. Revocation removes the entry.

- Trade-off: storage proportional to active sessions (potentially large) rather than revoked sessions (typically small). Effectively turns JWTs into reference tokens with extra steps.
- Use case: environments requiring absolute revocation control where the statelessness benefit of JWTs is secondary to security requirements.

#### Performance Characteristics

| Pattern | Lookup Latency | Storage Growth | Revocation Granularity | Operational Complexity |
|---------|---------------|----------------|----------------------|----------------------|
| Redis JTI deny-list | < 1ms | Proportional to revoked tokens; TTL auto-cleans | Per-token | Medium (Redis cluster required for HA) |
| Token versioning | 1-5ms (DB) or < 1ms (cached) | O(users) -- one version per user | Per-user (all tokens) | Low |
| Allowlist | < 1ms (Redis) | Proportional to ALL active tokens | Per-token | High (must track every issued token) |

#### .NET Implementation Considerations

In ASP.NET Core, deny-list checking integrates into the JWT bearer authentication pipeline via a custom `ISecurityTokenValidator` or by adding a claim validation step in `JwtBearerOptions.Events.OnTokenValidated`. The `Microsoft.Extensions.Caching.StackExchangeRedis` package provides the distributed cache abstraction. For .NET 9, the `IDistributedCache` interface with Redis backing is the recommended integration point, keeping the deny-list check within the standard middleware pipeline rather than requiring custom middleware.

---

### Sub-Topic 2: Sliding Window Refresh Tokens

#### Mechanism

Refresh token rotation with sliding window lifetimes addresses revocation by making access tokens short-lived (5-15 minutes) and controlling the session lifecycle through server-managed refresh tokens. The key insight: if access tokens expire quickly, revocation becomes a refresh token problem, not a JWT problem.

#### Duende IdentityServer Configuration (Current .NET Standard)

Duende IdentityServer (the successor to IdentityServer4 for .NET 6+) provides first-class support for refresh token rotation with the following configuration surface:

- **`RefreshTokenUsage`**: `ReUse` (default -- same handle on refresh) or `OneTimeOnly` (new handle issued on each refresh, old handle consumed). `OneTimeOnly` enables replay detection.
- **`RefreshTokenExpiration`**: `Absolute` (fixed expiry at `AbsoluteRefreshTokenLifetime`, default 30 days) or `Sliding` (lifetime renewed on each use by `SlidingRefreshTokenLifetime`, default 15 days, capped by absolute lifetime).
- **`DeleteOneTimeOnlyRefreshTokensOnUse`** (v6.3+): When `true` (default), consumed one-time refresh tokens are immediately deleted. When `false`, they are retained and marked as consumed, enabling replay detection.

#### Sliding Window Pattern

When `RefreshTokenExpiration` is set to `Sliding` with `OneTimeOnly` usage:

1. Client authenticates and receives access token (15 min) + refresh token (15 day sliding, 30 day absolute).
2. Before access token expires, client presents refresh token to the token endpoint.
3. Server issues new access token + new refresh token. Old refresh token is consumed/deleted.
4. The refresh token's expiry slides forward by `SlidingRefreshTokenLifetime` (15 days), but cannot exceed `AbsoluteRefreshTokenLifetime` (30 days) from original issuance.
5. If the old (consumed) refresh token is presented again, this indicates a potential token theft/replay attack.

#### Replay Detection

Duende IdentityServer supports extending `DefaultRefreshTokenService` to implement custom replay detection. When a consumed refresh token is reused:

```csharp
// Custom replay detection via DefaultRefreshTokenService extension
public override async Task<TokenValidationResult> ValidateRefreshTokenAsync(
    DefaultRefreshTokenValidationContext context)
{
    var consumedToken = await PersistedGrantService
        .GetRefreshTokenAsync(context.Token.Handle);
    if (consumedToken?.ConsumedTime.HasValue == true)
    {
        // Replay detected -- revoke all grants for this user/client
        Logger.LogWarning("Replay detected: {Handle}", context.Token.Handle);
        return new TokenValidationResult
        {
            IsError = true,
            Error = OidcConstants.TokenErrors.InvalidGrant
        };
    }
    return await base.ValidateRefreshTokenAsync(context);
}
```

#### Revocation on Logout

Duende's BFF (Backend-for-Frontend) framework automatically revokes refresh tokens on logout when `RevokeRefreshTokenOnLogout` is `true` (the default). Backchannel logout can revoke all sessions for a subject when `BackchannelLogoutAllUserSessions` is enabled.

#### Trade-offs

| Aspect | Sliding Window + Rotation | Fixed Expiry Only |
|--------|--------------------------|-------------------|
| Revocation latency | Access token lifetime (5-15 min max) | Access token lifetime |
| Replay detection | Yes (consumed token reuse = theft signal) | No |
| User experience | Seamless (silent refresh) | Re-authentication at fixed intervals |
| Server state | Refresh tokens stored server-side (persisted grants) | Minimal server state |
| Complexity | Medium (token endpoint, grant store, replay logic) | Low |

The critical design decision is the interaction between sliding and absolute lifetimes. When refresh token rotation is enabled, an absolute lifetime becomes effectively mandatory -- without it, a stolen refresh token could be rotated indefinitely. The sliding lifetime provides user convenience (active sessions stay alive); the absolute lifetime provides a hard security boundary.

---

### Sub-Topic 3: OAuth2 Token Introspection (RFC 7662)

#### Mechanism

Token introspection shifts the validation authority from the resource server (API) to the authorization server. Instead of self-contained JWTs that the API validates locally, the authorization server issues opaque reference tokens -- random strings with no embedded claims. The API must call the authorization server's introspection endpoint on every request to determine the token's validity and retrieve associated claims.

#### RFC 7662 Protocol

The introspection endpoint accepts a POST request with the token and returns a JSON response indicating whether the token is active, along with associated metadata (scope, client_id, username, expiry, etc.).

Key RFC 7662 requirements:
- The endpoint MUST require authorization (client authentication or a separate access token) to prevent token scanning attacks.
- The response MUST include the `active` boolean field.
- The endpoint MUST NOT reveal information about an inactive token beyond `active: false`.

#### .NET Implementation

**Duende IdentityModel** provides the client-side implementation:

```csharp
// Client-side: introspect a reference token
using Duende.IdentityModel.Client;

var client = new HttpClient();
var response = await client.IntrospectTokenAsync(new TokenIntrospectionRequest
{
    Address = "https://identity.example.com/connect/introspect",
    ClientId = "api1",
    ClientSecret = "secret",
    Token = accessToken
});
// response.IsActive indicates token validity
```

**Server-side revocation** via the revocation endpoint (RFC 7009):

```csharp
// Revoke a token programmatically
var result = await client.RevokeTokenAsync(new TokenRevocationRequest
{
    Address = "https://identity.example.com/connect/revocation",
    ClientId = "client",
    ClientSecret = "secret",
    Token = token
});
```

The `Duende.AspNetCore.Authentication.OAuth2Introspection` NuGet package provides the ASP.NET Core authentication handler that automates the introspection flow for incoming API requests.

#### Reference Tokens vs. JWTs

| Dimension | Self-Contained JWT | Reference Token (Introspection) |
|-----------|-------------------|-------------------------------|
| Validation location | Resource server (local) | Authorization server (remote) |
| Revocation latency | Token lifetime (minutes) or deny-list | Immediate (server-side state) |
| Network cost | Zero per request | One HTTP call per request |
| Scalability | Excellent (no central dependency) | Authorization server is a bottleneck |
| Token size | Large (claims embedded) | Small (opaque identifier) |
| Offline validation | Yes | No |

#### Introspection Caching

The per-request network cost is the primary concern for microservices at scale. Mitigation strategies:

1. **Response caching with short TTL** (30-60 seconds): Cache introspection responses at the API gateway or resource server. Trades immediate revocation for reduced latency. The cache TTL becomes the effective revocation delay.
2. **Hybrid approach**: Use JWTs for most APIs (local validation, fast) and reference tokens only for high-security endpoints requiring immediate revocation (payment processing, admin operations).
3. **Gateway-level introspection**: Perform introspection at the API gateway and forward validated claims as headers to downstream services. Each downstream service trusts the gateway (zero additional introspection calls).

#### Microservices Architecture Considerations

In a .NET 9 microservices deployment:

- **Service-to-service communication**: Machine-to-machine tokens (client credentials grant) are typically JWTs validated locally. Introspection is reserved for user-facing tokens where revocation matters.
- **API gateway pattern**: An API gateway (YARP, Ocelot) performs introspection once per request and forwards claims to internal services, avoiding N introspection calls for N downstream services.
- **Authorization server availability**: The introspection endpoint becomes a critical dependency. If the authorization server is unavailable, all API calls fail. This requires the authorization server to be deployed with high availability (multiple replicas, health checks, circuit breakers on the client side).

---

## L2: Strategic Implications and Recommendations

### Pattern Selection Decision Framework

| Scenario | Recommended Pattern | Rationale |
|----------|-------------------|-----------|
| Standard SaaS API with moderate security requirements | Short-lived JWTs (15 min) + refresh token rotation (sliding window) | Best balance of statelessness, performance, and revocation latency. No per-request overhead. Revocation within access token lifetime is acceptable. |
| High-security endpoints requiring immediate revocation | Reference tokens with introspection, or JWT + Redis deny-list | Immediate revocation capability. Choose introspection if you have a centralized authorization server; choose deny-list if you need to preserve JWT local validation. |
| Microservices with API gateway | Gateway-level introspection for user tokens; local JWT validation for service-to-service | Gateway absorbs introspection cost. Internal services operate statelessly. |
| Regulatory compliance (PCI-DSS, SOX) requiring audit trail | Reference tokens + introspection + event logging at authorization server | Full server-side control over token lifecycle with auditable revocation events. |

### Emerging Trends (2024-2026)

1. **Transaction Tokens (draft-ietf-oauth-transaction-tokens)**: A new OAuth working group draft for short-lived, context-bound tokens that replace both access tokens and service-to-service tokens in microservices call chains. Not yet production-ready but addresses the revocation problem by making tokens so short-lived (seconds) that revocation is unnecessary.

2. **IETF OAuth 2.0 Security Best Current Practice (RFC 9700, published 2024)**: Strengthens recommendations for refresh token rotation as the primary revocation mechanism. Recommends sender-constrained tokens (DPoP) to mitigate token theft.

3. **Duende IdentityServer v7.x (2024-2025)**: Enhanced support for `DeleteOneTimeOnlyRefreshTokensOnUse`, server-side session management, and backchannel logout. The BFF pattern is increasingly recommended over SPA-direct-to-API patterns.

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Redis deny-list unavailability re-enables revoked tokens | Medium | High | Redis persistence (AOF), replication, graceful degradation (reject tokens if Redis is unreachable) |
| Refresh token theft during rotation window | Low | High | Replay detection via consumed token reuse monitoring, sender-constrained tokens (DPoP) |
| Authorization server unavailability blocks all introspection | Medium | Critical | HA deployment, client-side circuit breakers, short-duration response caching as fallback |
| Access token lifetime too long, revocation gap unacceptable | Medium | Medium | Reduce access token lifetime to 5 minutes; accept increased refresh traffic |

---

**Confidence:** 0.80 (high). The three sub-topics are well-covered in current literature and vendor documentation (Duende IdentityServer, RFC 7662, Redis-based deny-list patterns). The primary uncertainty is in the "Emerging Trends" section -- Transaction Tokens are draft-stage and may not reach production adoption within the survey period. The .NET 9 specific implementation guidance is limited; most patterns are framework-agnostic with .NET-specific integration via Duende and ASP.NET Core middleware.

**Data sources consulted:** Duende IdentityServer documentation (Context7), RFC 7662 specification, SuperTokens technical guides, Auth0 documentation, Okta developer documentation, Code Maze ASP.NET Core guides, Scalekit RFC 7662 analysis, web search across multiple implementation-focused publications (2023-2026).
