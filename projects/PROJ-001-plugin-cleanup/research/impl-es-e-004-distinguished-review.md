# Distinguished Engineer Review Patterns for Event Sourcing

**Research ID:** impl-es-e-004
**Entry ID:** e-004
**PS Context:** impl-es (Event Sourcing Implementation)
**Topic:** Distinguished Engineer Review Patterns for Event Sourcing Systems
**Date:** 2026-01-09
**Author:** ps-researcher agent v2.0.0

---

## L0: Executive Summary (ELI5)

**What is this?**

This document captures how senior engineers (Staff, Principal, Distinguished) should review code in Event Sourcing systems. It combines industry best practices from Google, Microsoft, and AWS with domain-specific patterns for DDD, CQRS, and Event Sourcing.

**Key Takeaways:**

1. **Code health over perfection** - Approve changes that improve the system even if not perfect
2. **Layer boundaries are sacred** - Domain layer must never depend on infrastructure
3. **Events are immutable contracts** - Review event design as carefully as public APIs
4. **Idempotency is mandatory** - Every command handler must handle duplicate executions
5. **Aggregate boundaries define transactions** - One transaction = one aggregate

**Why does this matter?**

Event Sourcing systems are complex and have unique review requirements. Improper event design or boundary violations create technical debt that is extremely expensive to fix post-deployment.

---

## L1: Technical Findings (Engineer Level)

### 1. Google Code Review Standards

Google's Engineering Practices provide the foundation for modern code review.

#### What to Look For (Per Google)

| Area | Focus Points |
|------|--------------|
| **Design** | Overall design, system interactions, change belongs in codebase |
| **Functionality** | Code behaves as intended, good for users |
| **Complexity** | Can be understood quickly, no over-engineering |
| **Tests** | Correct, well-designed automated tests |
| **Naming** | Clear names for variables, classes, methods |
| **Comments** | Explain WHY, not WHAT |
| **Style** | Follow style guide (absolute authority) |
| **Consistency** | Match existing codebase unless it worsens health |
| **Documentation** | Update READMEs when functionality changes |

Source: [Google Engineering Practices - What to Look For](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

#### The Standard of Code Review

> "Reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn't perfect."

Key principles:
- **Continuous improvement** over perfection
- **Technical facts and data** overrule opinions
- **Style guide is absolute authority** on style matters
- **Respond within one business day** maximum

Source: [Google Engineering Practices - Standard](https://google.github.io/eng-practices/review/reviewer/standard.html)

#### Complexity and Over-Engineering

> "A particular type of complexity is over-engineering, where developers have made the code more generic than it needs to be, or added functionality that isn't presently needed by the system. Reviewers should be especially vigilant about over-engineering."

Encourage developers to:
- Solve the problem that needs solving NOW
- Not speculate about future problems
- Keep solutions as simple as possible

---

### 2. Microsoft Code Review Best Practices

Microsoft's Engineering Fundamentals Playbook provides structured guidance.

#### Two-Pass Review Structure

**First Pass - Design Review:**
- Verify PR descriptions and logical coherence
- Check for user-facing changes with appropriate documentation
- Assess architectural patterns and interaction design

**Second Pass - Code Quality:**
- **Complexity:** Single responsibility, function length, argument count (>3 = potential issue)
- **Naming:** Clear, descriptive identifiers
- **Error Handling:** Explicit, graceful management
- **Functionality:** Race conditions, optimization, security, PII protection
- **Style:** Adherence to established conventions
- **Tests:** Committed alongside code, covering edge cases

Source: [Microsoft Engineering Playbook - Reviewer Guidance](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/)

#### Communication Guidelines

- Be positive - use encouraging language
- Prefix minor concerns with "Nit:"
- Use "we" or "this line" rather than "you" (code reviews are not personal)
- Prefer questions over statements
- Explain WHY changes are needed, ideally with examples

Source: [Microsoft - 30 Code Review Best Practices](https://www.michaelagreiler.com/code-review-best-practices/)

---

### 3. Hexagonal Architecture Review Patterns

For Event Sourcing systems following hexagonal architecture, layer boundary enforcement is critical.

#### Layer Boundary Rules

| Layer | May Import From | Must NOT Import From |
|-------|-----------------|---------------------|
| Domain | (stdlib only) | Application, Infrastructure, Interface |
| Application | Domain | Infrastructure, Interface |
| Infrastructure | Domain, Application | Interface |
| Interface | All inner layers | - |

Source: [AWS Hexagonal Architecture Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html)

#### Ports and Adapters Review Checklist

- [ ] Domain layer has NO external imports (stdlib only)
- [ ] Ports (interfaces) defined in domain/application
- [ ] Adapters implement ports, not the reverse
- [ ] Communication between adapters and application ONLY through ports
- [ ] No technology-specific types leak into domain layer
- [ ] Business exceptions used in domain (not technical exceptions)

Source: [Hexagonal Architecture Guide - Booking.com](https://medium.com/booking-com-development/hexagonal-architecture-a-practical-guide-5bc6d5a6a056)

#### Boundary Enforcement with ArchUnit

Automated enforcement can prevent accidental boundary violations:

```
Rules can prevent accidental leaks of technical specifics into the domain
layer, preserving the clean boundaries that Hexagonal Architecture relies on.
```

Source: [Hexagonal Architecture - Focus on Domain](https://scalastic.io/en/hexagonal-architecture-domain/)

---

### 4. Event Sourcing Specific Reviews

Event Sourcing introduces unique review requirements.

#### Aggregate Boundary Validation

From Eric Evans (DDD):

> "An aggregate is a cluster of associated objects that we treat as a unit for the purpose of data changes. Each aggregate has a root and a boundary."

**Review Checklist:**
- [ ] Aggregate root controls all access to internal objects
- [ ] External objects hold references to root ONLY
- [ ] One transaction = one aggregate
- [ ] Changes recorded atomically within aggregate
- [ ] Clear consistency boundary defined

Source: [Microsoft - Domain Events Design](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation)

#### Cross-Aggregate Transactions

> "Many DDD authors like Eric Evans and Vaughn Vernon advocate the rule that one transaction = one aggregate and therefore argue for eventual consistency across aggregates."

**Review Concerns:**
- If spanning aggregates in one transaction, is it justified?
- Are side effects to other aggregates via eventual consistency?
- Is the aggregate boundary too narrow? Too wide?

Source: [Microsoft - Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

---

### 5. Event Naming Conventions

Event naming requires special attention as events become immutable contracts.

#### Naming Rules

| Rule | Good Example | Bad Example |
|------|--------------|-------------|
| Use past tense verbs | `OrderShipped` | `ShipOrder` |
| Avoid CRUD terms | `CustomerRegistered` | `CustomerCreated` |
| Be specific, not generic | `BusinessUserRegistered` | `UserRegistered` |
| Version at beginning | `v1.payments.failed` | `payments.failed.v1` |

Source: [Event Naming Guide - Arrange Act Assert](https://arrangeactassert.com/posts/how-i-name-events/)

#### Pluralization Guidelines

| Context | Pattern | Example |
|---------|---------|---------|
| Collections | Plural | `v1.payees.created` |
| Processes | Singular | `v1.transaction.authorised` |
| Sub-entities | Plural | `v1.order.items.shipped` |

Source: [Confluent - Event Design Best Practices](https://developer.confluent.io/courses/event-design/best-practices/)

#### Event Design Review Checklist

- [ ] Name uses past tense verb (something HAPPENED)
- [ ] Name reflects business meaning, not CRUD operation
- [ ] Payload contains all necessary context
- [ ] Event is self-describing (consumer doesn't need external lookup)
- [ ] Version strategy defined for evolution
- [ ] No PII/sensitive data in event (or explicitly encrypted)

Source: [Kurrent - What's in an Event Name](https://www.kurrent.io/blog/whats-in-an-event-name)

---

### 6. Idempotency Verification

Idempotency is mandatory in Event Sourcing systems.

#### Why Idempotency Matters

> "Event publication might be at least once, and so consumers of the events must be idempotent. They must not reapply the update described in an event if the event is handled more than once."

Source: [Microsoft - Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)

#### Idempotency Implementation Patterns

**Pattern 1: Predictable IDs**
Generate stream identifiers deterministically from business data rather than random UUIDs.

```
Example: Guest stay account = GuestID + RoomID
Same logical operation always targets same stream.
```

**Pattern 2: Transaction Tracking**
Maintain collection of processed transaction IDs within aggregate state. Check before executing.

**Pattern 3: Return Empty on Duplicate**
Return empty event array when command should be ignored (rather than throwing).

**Pattern 4: Optimistic Concurrency Control**
Include expected stream versions when appending events. Storage rejects mismatches.

Source: [Event-Driven.io - Idempotent Command Handling](https://event-driven.io/en/idempotent_command_handling/)

#### Idempotency Review Checklist

- [ ] Command handler checks for duplicate execution
- [ ] Idempotency key/ID mechanism in place
- [ ] Expected version included in append operations
- [ ] Retry policy configured for concurrency errors
- [ ] Empty result returned for idempotent no-ops (not exception)
- [ ] Naturally idempotent operations identified and documented

Source: [Microservices.io - Idempotent Consumer Pattern](https://microservices.io/patterns/communication-style/idempotent-consumer.html)

#### Naturally Idempotent vs Non-Idempotent

| Naturally Idempotent | NOT Naturally Idempotent |
|---------------------|-------------------------|
| Set membership (add item to set) | Increment/decrement operations |
| Upsert operations | Withdrawals/transfers |
| Status transitions (to same state) | Append-only operations |

Source: [Jonathan Oliver - Idempotency Patterns](https://blog.jonathanoliver.com/idempotency-patterns/)

---

### 7. Staff Engineer Review Focus

Staff+ engineers have different review responsibilities than senior ICs.

#### Staff Engineer Archetypes (Will Larson)

| Archetype | Primary Responsibility | Review Focus |
|-----------|----------------------|--------------|
| **Tech Lead** | Guides execution for team cluster | Cross-team coordination, technical vision |
| **Architect** | Owns technical domain success | API design, system coherence, technical debt |
| **Solver** | Addresses critical high-risk problems | Deep problem analysis, solution validation |
| **Right Hand** | Extends executive capacity | Cross-cutting concerns, fire management |

Source: [StaffEng.com - Staff Archetypes](https://staffeng.com/guides/staff-archetypes/)

#### Strategic Thinking in Reviews

> "Strategic thinking takes critical and creative thinking a step further. When you exercise strategic thinking, you're ensuring that the decisions you make today will stand the test of time."

**Strategic Review Questions:**
- Does this change align with long-term technical direction?
- Will this create technical debt? Is that acceptable?
- Are we solving the problem or just the symptom?
- What are the second-order effects?

Source: [InfoQ - Staff+ Strategic Thinking](https://www.infoq.com/articles/staff-plus-strategic-thinking/)

#### Sponsorship Over Heroics

> "You're far more likely to change your company's long-term trajectory by growing the engineers around you than through personal heroics."

**In Reviews:**
- Use reviews as teaching opportunities
- Explain the WHY behind suggestions
- Invite growing engineers to participate
- Credit good patterns publicly

Source: [Tanya Reilly - The Staff Engineer's Path](https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/)

---

## L2: Strategic Patterns and Trade-offs (Architect Level)

### PAT-ES-001: Event Schema as API Contract

**Pattern:** Treat event schemas with the same rigor as public APIs.

**Rationale:** Events become immutable once published. Breaking changes are extremely expensive.

**Review Requirements:**
| Aspect | Requirement |
|--------|-------------|
| Naming | Past tense, business meaning |
| Versioning | Strategy defined before first publish |
| Payload | Self-describing, complete context |
| Evolution | Additive changes only after v1 |

**Trade-offs:**
| Benefit | Cost |
|---------|------|
| Consumer stability | Slower schema evolution |
| Clear contracts | More upfront design effort |
| Audit trail | Storage overhead for metadata |

---

### PAT-ES-002: Aggregate Boundary Enforcement

**Pattern:** Rigorously validate aggregate boundaries match consistency requirements.

**Review Questions:**
1. Can this aggregate be split? (Too large = transaction bottleneck)
2. Should these aggregates merge? (Cross-aggregate transactions = smell)
3. Is eventual consistency acceptable between these entities?
4. Does the aggregate protect its invariants?

**Warning Signs:**
- Multiple aggregates modified in one transaction
- Aggregate that rarely changes together internally
- Business rule spanning aggregate boundaries

---

### PAT-ES-003: Idempotency-First Design

**Pattern:** Every command handler must handle duplicate execution gracefully.

**Implementation Tiers:**
| Tier | Approach | Use Case |
|------|----------|----------|
| Basic | Optimistic concurrency | Single-writer scenarios |
| Standard | Transaction ID tracking | Multi-writer scenarios |
| Advanced | Distributed idempotency keys | Cross-service operations |

**Review Checklist:**
- [ ] What happens if this command executes twice?
- [ ] Is there a natural idempotency key?
- [ ] Is optimistic concurrency sufficient?
- [ ] Are retry semantics documented?

---

### PAT-ES-004: Layer Boundary Audit

**Pattern:** Use static analysis to enforce hexagonal layer boundaries.

**Implementation:**
- ArchUnit tests for Java/Kotlin
- Custom analyzers for other languages
- CI pipeline enforcement

**Violations to Flag:**
| Violation | Example | Fix |
|-----------|---------|-----|
| Domain imports infrastructure | `import CosmosClient` in entity | Extract to port interface |
| Application imports interface | `import HttpRequest` in use case | Use DTOs |
| Cross-layer direct instantiation | `new CosmosAdapter()` in domain | Dependency injection |

---

### PAT-ES-005: Tiered Review Rigor for ES Systems

**Pattern:** Match review depth to change risk in Event Sourcing context.

| Risk Level | Change Type | Review Approach |
|------------|-------------|-----------------|
| **Critical** | Event schema changes | Senior + Architect, ADR required |
| **High** | Aggregate boundaries | Senior reviewer, domain expert |
| **Medium** | Command handlers | Standard 2-reviewer process |
| **Low** | Read models/projections | 1 reviewer, self-review |

**Special Escalation:**
- Any event schema change: Requires Architecture review
- Any aggregate split/merge: Requires data migration plan
- Any cross-aggregate transaction: Requires explicit justification

---

## Output Levels Reference

This document provides three levels of detail:

| Level | Audience | Content |
|-------|----------|---------|
| **L0** | Stakeholders, Managers | Executive summary, key takeaways |
| **L1** | Engineers | Technical findings, checklists, examples |
| **L2** | Architects, Principals | Strategic patterns, trade-offs, decision frameworks |

---

## References and Citations (P-001, P-004 Compliance)

### Primary Sources

1. **Google Engineering Practices**
   - [What to Look For in Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
   - [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)
   - [GitHub Repository](https://github.com/google/eng-practices)

2. **Microsoft Engineering**
   - [Reviewer Guidance](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/)
   - [Code Reviews Playbook](https://microsoft.github.io/code-with-engineering-playbook/code-reviews/)
   - [30 Code Review Best Practices - Dr. Michaela Greiler](https://www.michaelagreiler.com/code-review-best-practices/)

3. **Event Sourcing & DDD**
   - [Microsoft - Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
   - [Microsoft - Domain Events Design](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/domain-events-design-implementation)
   - [Idempotent Command Handling - Event-Driven.io](https://event-driven.io/en/idempotent_command_handling/)
   - [Idempotent Consumer Pattern - Microservices.io](https://microservices.io/patterns/communication-style/idempotent-consumer.html)

4. **Architecture Patterns**
   - [Hexagonal Architecture - AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html)
   - [Hexagonal Architecture Guide - Booking.com](https://medium.com/booking-com-development/hexagonal-architecture-a-practical-guide-5bc6d5a6a056)
   - [Hexagonal Architecture - Focus on Domain](https://scalastic.io/en/hexagonal-architecture-domain/)

5. **Event Naming**
   - [Event Naming Guide - Arrange Act Assert](https://arrangeactassert.com/posts/how-i-name-events/)
   - [Event Design Best Practices - Confluent](https://developer.confluent.io/courses/event-design/best-practices/)
   - [What's in an Event Name - Kurrent](https://www.kurrent.io/blog/whats-in-an-event-name)

6. **Staff Engineering**
   - [Staff Archetypes - StaffEng.com](https://staffeng.com/guides/staff-archetypes/)
   - [Staff+ Strategic Thinking - InfoQ](https://www.infoq.com/articles/staff-plus-strategic-thinking/)
   - [The Staff Engineer's Path - Tanya Reilly](https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/)

7. **Idempotency Patterns**
   - [Jonathan Oliver - Idempotency Patterns](https://blog.jonathanoliver.com/idempotency-patterns/)
   - [Idempotency in Event Processing](https://danielwilliansc.medium.com/idempotency-in-event-processing-744b2b19fb55)
   - [Understanding Idempotency - EDA Visuals](https://eda-visuals.boyney.io/visuals/understanding-idempotency)

---

## Appendix: Quick Reference Card

### Distinguished Engineer Review Mindset for Event Sourcing

```
Before Review:
- Is this improving code health? (Google standard)
- What's the risk tier? (PAT-ES-005)
- Does this touch event schemas? (PAT-ES-001)
- Does this cross aggregate boundaries? (PAT-ES-002)

During Review:
- Check layer boundaries (PAT-ES-004)
- Verify idempotency handling (PAT-ES-003)
- Use data, not opinion (Google)
- Plan for iteration (multiple passes)

After Review:
- Document key decisions (ADRs for architectural)
- Consider sponsorship opportunities
- Update checklists if gaps found
```

### Event Sourcing Review Checklist Summary

```
[ ] Event names use past tense
[ ] Event payloads are self-describing
[ ] Aggregate boundaries are correct
[ ] One transaction = one aggregate
[ ] Idempotency handling verified
[ ] Layer boundaries respected
[ ] No domain layer external dependencies
[ ] Tests cover happy path + edge cases
[ ] Error handling is explicit
[ ] Documentation updated if needed
```
