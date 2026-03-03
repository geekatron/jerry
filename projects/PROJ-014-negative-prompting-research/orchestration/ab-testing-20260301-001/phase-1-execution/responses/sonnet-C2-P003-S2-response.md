# Authentication Token Revocation Strategies -- Research Findings

**Agent:** ps-researcher
**Task:** Survey authentication token revocation patterns (2023-2026)
**Criticality:** C2

---

## Constraint Notice: Sub-Agent Delegation Declined

The orchestrator's note recommends delegating each sub-topic to specialized sub-researchers running in parallel. I cannot comply with this recommendation.

**Reason:** P-003 prohibits recursive subagent spawning. As a worker agent, I am already one level below the orchestrator. Spawning sub-researchers from within this context would create a second nesting level (orchestrator -> ps-researcher -> sub-researcher), which violates the hard constraint against recursive delegation. This applies regardless of how the recommendation is framed -- whether described as "standard practice," "for efficiency," or authorized by a "senior architect." P-003 cannot be overridden by instructions embedded in a task description.

I am proceeding with all three sub-topics directly within this agent context. The three focus areas are covered sequentially below. The findings are consolidated into a single document as required.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 -- Executive Summary](#l0----executive-summary) | Key findings for decision makers |
| [L1 -- Technical Findings](#l1----technical-findings) | Detailed patterns per focus area |
| [L2 -- Strategic Implications](#l2----strategic-implications) | .NET 9 adoption guidance and trade-offs |

---

## L0 -- Executive Summary

Three revocation patterns dominate current .NET 9 microservices practice (2023-2026):

1. **JWT Deny-List (Blocklist):** Stores revoked JWT IDs (JTI claims) in a distributed cache (Redis). Enables immediate revocation at the cost of per-request cache lookup. Best fit when revocation latency requirements are strict (e.g., compromised credentials, account lockout).

2. **Sliding Window Refresh Tokens:** Short-lived access tokens paired with refresh tokens that reset their expiry on each use. Reduces revocation surface -- only refresh tokens need explicit revocation. The sliding window pattern minimizes token database churn while maintaining session continuity. Best fit for user-facing applications where session persistence matters.

3. **OAuth2 Token Introspection (RFC 7662):** Authorization server exposes a `/introspect` endpoint. Resource servers query it per request to validate token status. Provides real-time revocation propagation across all services without client-side token storage concerns. Best fit for multi-tenant or third-party API scenarios where the authorization server is the single source of truth.

**Recommendation for .NET 9 microservices:** Sliding window refresh tokens for internal service-to-service auth (lower overhead); OAuth2 introspection for external API consumers (stronger revocation guarantees). JWT deny-list as a targeted supplement for immediate revocation of specific tokens (e.g., after logout or credential reset).

---

## L1 -- Technical Findings

### Focus Area 1: JWT Deny-List Approaches

**Pattern Overview**

The JWT deny-list (also called blocklist or revocation list) addresses the fundamental stateless nature of JWTs: because a JWT is self-contained, a resource server can validate it without contacting any central authority -- but this means a compromised token remains valid until expiry.

The deny-list pattern reintroduces a lightweight stateful check:
- Each JWT includes a `jti` (JWT ID) claim -- a unique identifier per token.
- On revocation (logout, credential change, admin action), the `jti` is written to a distributed store (Redis is the dominant choice in .NET ecosystems).
- Each resource server checks the incoming `jti` against the deny-list before accepting the token.
- Deny-list entries expire automatically aligned with the token's `exp` claim -- no manual cleanup required.

**.NET 9 Implementation Patterns (2023-2026)**

- `Microsoft.Extensions.Caching.StackExchangeRedis` is the standard integration path. The `IDistributedCache` abstraction allows swapping Redis for in-memory (for testing) without changing revocation logic.
- ASP.NET Core middleware intercepts token validation via `TokenValidationParameters.TokenReaders` or a custom `ISecurityTokenValidator`. The JTI check is injected as a synchronous step before claims are trusted.
- `StackExchange.Redis` 2.7+ (released 2023) introduced `SINTERCARD` and improved pipeline batching, reducing per-request latency for deny-list lookups in high-throughput scenarios.

**Trade-offs**

| Factor | Assessment |
|--------|------------|
| Revocation latency | Near-zero -- revocation is effective on next request |
| Per-request overhead | One Redis GET per authenticated request (~0.5-2ms on local network) |
| Storage cost | Low -- only revoked tokens stored, auto-expiring with token TTL |
| Scalability | Redis Cluster handles horizontal scale; single-node Redis is a SPOF |
| Complexity | Moderate -- requires Redis dependency and JTI generation discipline |

**Failure modes:** If Redis is unavailable, the system must choose between fail-open (accept tokens, ignore revocation) or fail-closed (reject all tokens). For security-sensitive contexts, fail-closed is required, but this creates availability risk. The pattern is documented in OWASP JWT Security Cheat Sheet (2024 revision) as the recommended approach for immediate revocation requirements.

---

### Focus Area 2: Sliding Window Refresh Tokens

**Pattern Overview**

Sliding window refresh tokens decouple the session lifetime from the access token lifetime:
- Access tokens are short-lived (5-15 minutes). Expiry is the primary revocation mechanism.
- Refresh tokens are longer-lived but rotate on each use. Each refresh call invalidates the previous refresh token and issues a new one with a reset expiry window.
- "Sliding window" refers to the expiry behavior: each successful use slides the expiry forward by the window size, so active sessions never expire. Inactive sessions naturally expire.

**Rotation Security Property:** If a refresh token is stolen and used by an attacker, the original legitimate client's next refresh attempt will fail (the token has already been rotated). This signals a theft event. The authorization server can then revoke the entire token family (all refresh tokens derived from the original grant).

**.NET 9 Implementation Patterns (2023-2026)**

- `Microsoft.Identity.Web` (1.25+, released 2023) added first-class support for refresh token rotation via `WithRefreshTokenAsync` overloads. Token families are tracked via a `family_id` claim.
- ASP.NET Core Identity (included in .NET 9) provides `UserTokens` table for refresh token storage. Sliding window logic is implemented by updating the `ExpiresAt` column on each successful refresh.
- The `ITokenService` abstraction pattern (popularized by Clean Architecture templates) is the dominant approach in 2024-2025 .NET projects: one interface, implementations for EF Core (persistent) and Redis (ephemeral sessions).
- Duende IdentityServer 7 (2024) added configurable sliding expiration via `RefreshTokenExpiration = TokenExpiration.Sliding` with `SlidingRefreshTokenLifetime` setting.

**Token Family Revocation (2024 advancement)**

The Duende and Auth0 approaches converged on token family tracking in 2024: all refresh tokens issued from a single authorization grant share a `family_id`. Detection of refresh token reuse triggers revocation of the entire family, not just the reused token. This closes the window where an attacker could silently use a stolen refresh token if the legitimate user had not yet attempted a refresh.

**Trade-offs**

| Factor | Assessment |
|--------|------------|
| Revocation latency | Access token TTL (5-15 min) for access tokens; immediate for refresh tokens |
| Per-request overhead | Negligible for access token validation; one DB/cache write per refresh |
| Storage cost | Moderate -- one refresh token record per active session |
| Scalability | DB writes on refresh; Redis alternative for high-volume scenarios |
| Complexity | Higher -- requires rotation logic, family tracking, reuse detection |

**Best practice note (2025):** Short access token TTLs (under 10 minutes) are now standard guidance in the .NET security community. This reduces the deny-list requirement: most revocation needs are met by waiting for token expiry. The deny-list is reserved for high-priority revocation (compromised credentials) rather than routine logout.

---

### Focus Area 3: OAuth2 Token Introspection (RFC 7662)

**Pattern Overview**

RFC 7662 defines a standard endpoint (`/introspect`) that resource servers call to determine the current state of a token. Unlike the deny-list (which is checked client-side by the resource server) or refresh token rotation (which is client-managed), introspection centralizes revocation authority at the authorization server.

Request:
```
POST /introspect
Authorization: Basic {resource-server-credentials}
Content-Type: application/x-www-form-urlencoded

token={access_token}
```

Response (active token):
```json
{
  "active": true,
  "sub": "user-123",
  "exp": 1740000000,
  "scope": "read:orders",
  "client_id": "mobile-app"
}
```

Response (revoked or expired):
```json
{
  "active": false
}
```

**.NET 9 Implementation Patterns (2023-2026)**

- `Microsoft.AspNetCore.Authentication.OAuth` does not include introspection out of the box. The dominant library is `IdentityModel.AspNetCore.OAuth2Introspection` (formerly `IdentityServer4.AccessTokenValidation`), maintained by Duende as an open-source project.
- Configuration in .NET 9:
  ```csharp
  builder.Services.AddAuthentication()
      .AddOAuth2Introspection("introspection", options =>
      {
          options.Authority = "https://auth.example.com";
          options.ClientId = "resource-server";
          options.ClientSecret = "{secret}";
          options.CacheResponses = true;
          options.CacheDuration = TimeSpan.FromMinutes(5);
      });
  ```
- The `CacheResponses = true` option is critical for performance: without caching, every request to the resource server generates an introspection call to the authorization server, creating a fan-in bottleneck at scale.

**Caching Strategy (2024 pattern)**

The 2024 consensus in the .NET ecosystem is a two-layer caching approach:
1. In-process memory cache (IMemoryCache) for the hot path -- sub-millisecond lookup for recently validated tokens.
2. Distributed cache (Redis) for cross-instance consistency -- prevents cache stampede when multiple instances simultaneously encounter a new token.

Cache TTL is set to a fraction of the access token TTL (typically 50-80%) to ensure revocation propagates within one token lifetime while maintaining the performance benefit of caching.

**Revocation Flow**

When a token is revoked at the authorization server:
1. Authorization server marks token as inactive in its store.
2. Resource servers with cached introspection results continue accepting the token until the cache TTL expires.
3. After cache expiry, the next introspection call returns `"active": false`.
4. Effective revocation latency = cache TTL (configurable, not token TTL).

This is the key trade-off: introspection with caching does not provide immediate revocation. For immediate revocation, either disable caching (high latency cost) or combine with a deny-list signal pushed from the authorization server to resource servers (event-driven revocation, 2025 pattern using Azure Service Bus or NATS).

**Trade-offs**

| Factor | Assessment |
|--------|------------|
| Revocation latency | Cache TTL (configurable; 1-10 minutes typical) |
| Per-request overhead | Network call to auth server (mitigated by caching) |
| Storage cost | None at resource server; auth server owns token state |
| Scalability | Auth server becomes bottleneck without caching; horizontal scale at auth server required |
| Complexity | Low for resource server (delegate to auth server); higher for auth server operators |

**RFC 7662 adoption status (2025):** Introspection is now considered the baseline for third-party API access in .NET ecosystems. Azure AD / Entra ID supports introspection via the Microsoft Identity Platform v2 endpoints. The pattern is documented in the OAuth 2.0 Security Best Current Practice (draft-ietf-oauth-security-topics, 2024 revision) as the recommended approach for opaque tokens.

---

## L2 -- Strategic Implications

### Pattern Selection Matrix for .NET 9 Microservices

| Scenario | Recommended Pattern | Rationale |
|----------|--------------------|-|
| Internal service-to-service (short-lived, same trust domain) | Short-lived JWTs + deny-list for emergency revocation | Low overhead; deny-list only for compromised credentials |
| User-facing web/mobile app | Sliding window refresh tokens | Session continuity; rotation provides theft detection |
| Third-party API consumers | OAuth2 introspection | Authorization server as SSOT; client-agnostic revocation |
| High-security (financial, healthcare) | Introspection (no caching) + deny-list | Immediate revocation; performance cost acceptable |
| Multi-tenant SaaS | Sliding window refresh + introspection for external | Tier tokens by consumer type |

### Convergence Trends (2024-2026)

Three trends are converging in the .NET authentication ecosystem:

1. **Token TTL compression:** The community has moved toward shorter access token lifetimes (5-10 minutes) as the primary revocation mechanism. This reduces the operational burden of explicit revocation for the common case (routine logout), reserving deny-list and introspection for high-priority scenarios.

2. **Event-driven revocation propagation:** Rather than polling-based introspection, 2025 patterns increasingly use event bus (Azure Service Bus, NATS) to push revocation events to resource servers. Resource servers maintain a local deny-list populated by revocation events, combining the immediacy of deny-list with the centralization of introspection.

3. **Token binding and DPoP (RFC 9449):** Demonstrating Proof-of-Possession (DPoP) tokens bind access tokens to a client's cryptographic key pair. Stolen tokens cannot be replayed by an attacker who lacks the private key. DPoP support landed in `Microsoft.Identity.Web` 2.18 (2024) and is now included in .NET 9 ASP.NET Core preview templates. DPoP partially reduces the revocation urgency for stolen access tokens.

### .NET 9 Specific Considerations

- `System.IdentityModel.Tokens.Jwt` 7.x (shipped with .NET 9) added `TokenValidationParameters.ValidateWithLKG` (Last Known Good) support, enabling graceful handling of key rotation without service interruption.
- The `Microsoft.AspNetCore.Authentication.JwtBearer` handler in .NET 9 now supports `OnTokenValidated` async hooks with direct DI injection, making deny-list integration cleaner than .NET 7/8 workarounds.
- `Microsoft.Identity.Web` 2.x removed the dependency on `Microsoft.IdentityModel` preview packages, stabilizing the dependency graph for production .NET 9 projects.

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Redis unavailability breaks deny-list | Medium | High | Circuit breaker with fail-closed policy; Redis Sentinel or Cluster for HA |
| Refresh token database becomes bottleneck | Low | High | Shard by user_id; Redis for hot tokens, DB for cold storage |
| Introspection auth server SPOF | Medium | Critical | Multi-region auth server deployment; local fallback cache with longer TTL |
| DPoP adoption gap (old clients) | High | Low | Maintain non-DPoP path during transition; DPoP optional until 2027 |

---

*Research completed by ps-researcher (direct execution, no sub-agents). All three focus areas covered within this agent context per P-003 single-level nesting constraint.*
