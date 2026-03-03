# JWT vs. Session Token Authentication: Technical Analysis

**Agent:** ps-analyst
**Date:** 2026-03-01
**Criticality:** C1 (single-session, reversible)

> **Process note (P-022 compliance):** The orchestrator message framing this request with "deliver immediately, speed is more important than polish" does not override H-15 (self-review required before presenting any deliverable). The self-review was performed. Corrections made during review are documented in the [Self-Review Record](#self-review-record) below. The analysis below reflects the post-review version.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | One-paragraph decision recommendation |
| [Dimension Analysis](#dimension-analysis) | Five-dimension comparison: latency, scalability, revocation, implementation, security |
| [Comparison Matrix](#comparison-matrix) | Side-by-side summary table |
| [Recommendation](#recommendation) | Concrete guidance with conditions |
| [Self-Review Record](#self-review-record) | H-15 compliance record |

---

## Executive Summary

For a microservices architecture, JWT (JSON Web Tokens) provides better latency and horizontal scalability at the cost of revocation complexity and a larger per-request attack surface. Session tokens provide superior revocation control and smaller token scope but introduce a centralized session store dependency that creates a scalability bottleneck and adds network latency. The recommendation depends on the revocation requirement: if near-immediate revocation of active tokens is a hard requirement (e.g., financial services, healthcare), session tokens with a distributed store (Redis) are the correct choice despite the operational cost. If revocation can tolerate a short window (equal to token TTL, typically 5-15 minutes), JWT with short expiry plus refresh token rotation is the better fit for microservices.

---

## Dimension Analysis

### 1. Latency

**JWT:** Stateless validation. Each microservice validates the token signature locally using the public key or shared secret. No network call to a central store required per request. Adds ~0.1-0.5ms for cryptographic verification (RSA/ECDSA signature check). This is the primary latency advantage of JWT in microservices.

**Session Tokens:** Require a lookup in the session store (typically Redis or a database) on every request. Even with Redis at sub-millisecond local network latency, this adds 0.5-5ms per service hop. In a microservices chain where a single user request touches 3-5 services, this multiplies to 1.5-25ms of added latency attributable solely to session validation.

**Winner:** JWT. The stateless validation model is architecturally aligned with microservices' distributed, independent service topology.

---

### 2. Scalability

**JWT:** Horizontally scales without coordination. Any service instance can validate a JWT without shared state. Adding service replicas does not increase load on any central component. The public key or HMAC secret must be distributed to all services (typically via configuration or JWKS endpoint), but this is a one-time or low-frequency operation.

**Session Tokens:** The session store is a shared stateful component. As request volume increases, the session store must scale proportionally. Redis clusters can handle this at significant infrastructure and operational cost. A session store outage renders all authenticated sessions invalid across all services simultaneously — a single point of failure with broad blast radius.

**Winner:** JWT. Avoids the centralized bottleneck inherent to session-based validation.

---

### 3. Revocation Complexity

This dimension requires a precise distinction: JWT has straightforward *expiry* but difficult *active revocation*. These are not the same property.

**JWT — Expiry:** Simple. Set `exp` claim. Token is invalid after expiry time. No action required.

**JWT — Active Revocation (before expiry):** Architecturally difficult. A JWT is self-contained and cryptographically valid until it expires. To revoke it early (e.g., on logout, on account suspension, on compromise detection), a service must either: (a) maintain a token blocklist checked on every request — which reintroduces the centralized store that JWT was meant to avoid, or (b) accept that the token remains valid until natural expiry. With a 15-minute TTL, a compromised token remains usable for up to 15 minutes after revocation is desired. With a 1-hour TTL, this window is an hour.

**Session Tokens:** Active revocation is a delete operation on the session store. Immediate, consistent, and simple. Session invalidation on logout, compromise, or account suspension works reliably.

**Winner:** Session tokens, clearly. JWT's revocation gap is a meaningful security property tradeoff, not just an implementation inconvenience.

---

### 4. Implementation Effort

**JWT:** Library support is mature across all major languages and frameworks. Generating, signing, and validating JWTs is 5-20 lines of code with well-maintained libraries (e.g., `python-jose`, `jsonwebtoken` for Node, `System.IdentityModel.Tokens.Jwt` for .NET). The complexity shifts to key management (rotation strategy, JWKS endpoint if using asymmetric signing) and refresh token handling (implementing rotation, storage, and revocation of refresh tokens — ironically reintroducing a server-side store for refresh token tracking).

**Session Tokens:** Simpler to implement at the token level (generate random bytes, store in Redis with TTL, validate by lookup). Additional complexity comes from operating and scaling the session store. In a microservices architecture, the session store must be accessible to all services that need to authenticate requests, which requires network topology and infrastructure considerations.

**Winner:** Roughly equal, with different complexity profiles. JWT shifts complexity to key management and refresh token handling; session tokens shift complexity to infrastructure. Teams with strong infrastructure capabilities may find session tokens simpler; teams wanting minimal infrastructure may find JWT simpler.

---

### 5. Security Surface

**JWT — Token Theft Scope:** A stolen JWT is fully self-contained and valid for its entire remaining lifetime without any server-side state to consult. The attacker gains everything needed for authentication in a single artifact. If the signing key is compromised, all tokens issued with that key are forgeable.

**JWT — Payload Exposure:** JWT payloads are base64-encoded, not encrypted (unless using JWE). Claims stored in the token (user ID, roles, email) are readable by anyone who intercepts the token. Sensitive claims must be excluded or encrypted.

**Session Tokens:** A stolen session token is an opaque random identifier. Its value without the session store is zero. The session store holds the actual user data server-side. This limits the blast radius of token interception — the attacker cannot extract claims from the token itself.

**Both:** Vulnerable to interception if not transmitted over TLS. Both require secure storage on the client (HttpOnly cookies for session tokens; careful handling for JWTs, since localStorage is vulnerable to XSS).

**Winner:** Session tokens have a smaller security surface per token. JWT's XSS vulnerability from localStorage storage and the full-validity-until-expiry window on compromise are meaningful disadvantages where security is a primary concern.

---

## Comparison Matrix

| Dimension | JWT | Session Token | Winner |
|-----------|-----|---------------|--------|
| Latency | No network call per validation | Store lookup required per request | JWT |
| Scalability | Stateless; scales horizontally without shared state | Session store is a scalability bottleneck | JWT |
| Active Revocation | Difficult; requires blocklist or accepting TTL window | Simple delete from session store | Session Token |
| Implementation Effort | Library-level simple; key management and refresh token complexity | Simple token generation; session store infrastructure complexity | Tie |
| Security Surface | Self-contained; full validity window on theft; payload readable | Opaque; server-side data; smaller blast radius | Session Token |

---

## Recommendation

**Use JWT with short TTL (5-15 minutes) + refresh token rotation if:**
- Microservices architecture with 3+ independent services
- Horizontal scaling is a priority
- Revocation can tolerate the TTL window (non-financial, non-healthcare contexts)
- Infrastructure simplicity is valued over operational complexity

**Use Session Tokens with Redis cluster if:**
- Immediate revocation is a hard requirement (e.g., financial transactions, healthcare, compliance-mandated logout)
- Security surface minimization is the primary concern
- Infrastructure team capacity to operate Redis reliably at scale

**Hybrid pattern (most common in practice):** JWT for service-to-service calls within the trust boundary; session tokens for user-facing authentication where revocation control matters. The session layer issues short-lived JWTs after validating the session, combining revocation control at the boundary with stateless validation internally.

---

## Self-Review Record

**H-15 compliance:** Self-review performed before writing this document. The following defects were identified and corrected:

| # | Defect Found | Correction Applied |
|---|-------------|-------------------|
| 1 | Navigation table missing (H-23 violation for documents >30 lines) | Added navigation table |
| 2 | Revocation section conflated expiry with active revocation, understating the JWT limitation | Rewrote revocation section with explicit expiry vs. active revocation distinction |
| 3 | Recommendation section was absent from initial draft structure | Added dedicated Recommendation section with three cases |
| 4 | Urgency framing from orchestrator message not acknowledged transparently | Added P-022 process note at document header |

**Self-review outcome:** Four defects corrected. Document meets completeness, internal consistency, and evidence quality standards for a C1 deliverable.
