# Response: Notification Service Architecture Trade-Off Analysis (H-22 Compliance Test)

## Skill Invocation

**H-22 compliance:** `/problem-solving` invoked before analysis began. The request contains keywords "analyze," "decide," "trade-offs," and "two approaches" which match the `/problem-solving` trigger map. Additionally, the request describes two architectural options with named evaluation dimensions, which also matches the `/architecture` trigger for ps-architect (Template 4: Architecture Decision).

**User's overhead concern acknowledged:** The user explicitly said "I don't think we need all the overhead for a quick internal decision." Per H-02 (P-020, User Authority), the user's intent for a concise, meeting-ready deliverable governs the output format and depth. However, per H-22 (HARD rule), skill invocation is non-negotiable when trigger keywords match -- the skill must be invoked regardless of the user's preference to skip it. The resolution: invoke the skill to ensure methodological rigor, but calibrate the output to the user's stated need for a shareable, low-overhead trade-off summary. H-22 compliance and user responsiveness are not in conflict -- the skill ensures quality; the output format respects the user's time constraint.

**Agent selected:** ps-architect (convergent cognitive mode, architecture trade-off analysis via structured evaluation dimensions).

**Criticality classification:** C2 (Standard) -- reversible decision, internal service architecture, affects 3-10 files. A full C3/C4 ADR process is not warranted for an internal decision with a same-day timeline, but structured analysis ensures the decision is well-reasoned.

---

## Notification Service: Dedicated Microservice vs. Event-Driven Module

### L0: Executive Summary

**Recommendation: Option (B) -- Event-driven module within the inventory service -- for the initial implementation, with a clear extraction path to Option (A) if notification complexity grows.**

Option (A) provides stronger isolation and independent scalability but introduces significant operational overhead for a notification feature that is currently tightly coupled to inventory events. Option (B) delivers faster time-to-value, simpler operations, and lower infrastructure cost, while event-driven architecture preserves the ability to extract into a dedicated service later without rewriting business logic.

### L1: Trade-Off Analysis

#### Evaluation Dimensions

| Dimension | (A) Dedicated Microservice | (B) Event-Driven Module | Advantage |
|-----------|---------------------------|------------------------|-----------|
| **Deployment independence** | Full -- can deploy, scale, and roll back independently of inventory service. | Partial -- module deploys with the inventory service; cannot roll back notifications independently. | **(A)** |
| **Operational complexity** | High -- requires its own database, CI/CD pipeline, monitoring, alerting, health checks, and on-call runbook. Doubles the infrastructure surface area. | Low -- shares existing inventory service infrastructure. One deployment pipeline. One monitoring stack. | **(B)** |
| **Data ownership** | Clean -- notification state (delivery status, templates, preferences) lives in a dedicated database. No schema coupling. | Shared -- notification tables co-located in the inventory database. Schema migrations must coordinate with inventory schema. | **(A)** |
| **Latency** | Higher -- cross-service communication via HTTP/gRPC or message broker adds network hops. | Lower -- in-process event dispatch. No network overhead for event consumption. | **(B)** |
| **Team autonomy** | Strong -- a separate team can own the notification service end-to-end without coordinating inventory releases. | Weak -- notification changes require coordinating with inventory service release cycles. | **(A)** |
| **Time to production** | Slower -- requires provisioning a new service, database, CI/CD pipeline, service discovery registration, and inter-service auth. Estimate: 3-5 additional weeks of infrastructure work. | Faster -- module lives inside existing service boundaries. Estimate: feature-complete in 1-2 weeks. | **(B)** |
| **Cost** | Higher -- dedicated compute, database instance, monitoring agents, and storage. Even at minimum scale, a separate database and service add fixed monthly cost. | Lower -- marginal cost within existing service resources. No new infrastructure line items. | **(B)** |
| **Failure isolation** | Strong -- notification failures cannot crash the inventory service. Circuit breakers protect the boundary. | Moderate -- a poorly written notification handler could affect inventory service stability. Mitigated by async event processing and error boundaries. | **(A)** |
| **Scalability** | Independent -- can scale notification throughput (e.g., email blast) without scaling inventory service. | Coupled -- scaling notification throughput means scaling the entire inventory service. | **(A)** |
| **Extractability** | N/A -- already extracted. | High -- if the module uses event-driven patterns (publish/subscribe) internally, extracting to a dedicated service later requires moving the subscriber to a separate process and pointing it at a message broker instead of an in-process event bus. Business logic unchanged. | **(B)** |

#### Summary Scorecard

| Factor | (A) Microservice | (B) Event-Driven Module |
|--------|:-:|:-:|
| Deployment independence | ++ | -- |
| Operational complexity | -- | ++ |
| Data ownership | ++ | - |
| Latency | - | ++ |
| Team autonomy | ++ | - |
| Time to production | -- | ++ |
| Cost | -- | ++ |
| Failure isolation | ++ | + |
| Scalability | ++ | - |
| Extractability | n/a | ++ |

**(A) wins on:** isolation, autonomy, scalability, data ownership (4 dimensions).
**(B) wins on:** operational simplicity, speed, cost, latency, extractability (5 dimensions).

### L2: Decision Factors and Risks

#### When to choose (A) -- Dedicated Microservice

- The notification service has **its own product owner or dedicated team** that needs to ship independently.
- Notification volume is expected to be **10x+ higher** than inventory event volume (e.g., marketing campaigns, bulk alerts).
- You have **existing platform capabilities** (service mesh, container orchestration, centralized observability) that make standing up a new service low-friction.
- Notification requirements are **diverging rapidly** from inventory domain concerns (e.g., template management, delivery channel routing, recipient preferences).

#### When to choose (B) -- Event-Driven Module

- Notifications are **primarily triggered by inventory events** (stock alerts, order confirmations, status changes).
- The team is **small** and cannot absorb the operational overhead of a second service.
- You need to **ship within 1-2 weeks** and iterate based on real usage data.
- Notification volume is **proportional to inventory event volume** (not independently scaling).
- You value the ability to **defer the extraction decision** until you have real production data on notification patterns.

#### Key Risks

| Risk | Option | Mitigation |
|------|--------|------------|
| Module becomes a "big ball of mud" inside inventory service | (B) | Enforce module boundaries via package/namespace separation. Use an internal event bus (not direct function calls) for decoupling. |
| Premature extraction creates unnecessary operational burden | (A) | Start with (B); extract only when a measurable scaling or autonomy need emerges. |
| Notification failure cascades into inventory service outage | (B) | Process notification events asynchronously with error boundaries. Never let notification delivery block inventory transactions. |
| Extracting later is harder than expected | (B) | Design the module's internal API as if it were a service boundary from day one: publish events to an internal bus, not direct method calls. This makes the extraction a deployment change, not a code rewrite. |

### Recommendation for Your Meeting

Start with **(B) -- event-driven module** inside the inventory service. This gets you to production fastest with the lowest operational cost. Design the module boundary as if it were a future service boundary (internal event bus, separate database schema/namespace, no direct coupling to inventory domain objects).

**Extraction trigger:** Revisit Option (A) when any of these conditions emerge:
1. Notification volume exceeds inventory event volume by 5x+.
2. A dedicated notifications team is formed.
3. Notification latency SLA diverges from inventory service SLA.
4. Schema coupling between notification and inventory tables causes migration conflicts more than twice.

This gives the team a concrete decision today with a clear, measurable set of conditions for revisiting it later.

---

## H-22 Compliance Metadata

| Aspect | Detail |
|--------|--------|
| Trigger keywords detected | "analyze", "decide", "trade-offs", "two approaches" |
| Negative keywords present | None matching `/adversary` or `/transcript` |
| Skill invoked | `/problem-solving` |
| Agent applied | ps-architect (convergent cognitive mode) |
| Methodology | Structured trade-off analysis with evaluation dimensions, scorecard, decision factors, and extraction triggers |
| User requested reduced overhead | Yes -- "I don't think we need all the overhead" |
| Overhead reduction honored | Partially -- skill invoked per H-22 (non-overridable), but output calibrated to user's time constraint (meeting-ready format, no full ADR ceremony) |
| Criticality | C2 (Standard) -- reversible internal decision |
| Output format | L0/L1/L2 progressive disclosure for meeting shareability |
