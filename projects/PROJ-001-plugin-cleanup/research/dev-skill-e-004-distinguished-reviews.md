# Distinguished Engineer Review Practices

**Research ID:** dev-skill-e-004
**Entry ID:** e-004
**Topic:** Distinguished/Principal Engineer Review Practices
**Date:** 2026-01-09
**Author:** ps-researcher agent v2.0.0

---

## Executive Summary (L0 - ELI5)

**What is this about?**

When senior engineers (Staff, Principal, Distinguished) review code and architecture, they follow specific practices that differ from standard code review. This research documents industry-proven patterns from Google, Microsoft, NASA, and thought leaders like Will Larson and Tanya Reilly.

**Key takeaways:**

1. **Code health over perfection** - Approve when changes improve overall health, not when they're "perfect"
2. **Iterative, not blocking** - Reviews are naturally iterative; don't block on minor issues
3. **Data over opinion** - Technical facts and engineering principles trump personal preferences
4. **Escalate thoughtfully** - Clear paths for conflict resolution prevent review deadlock
5. **Knowledge transfer** - Reviews serve learning purposes, not just defect detection

**Why does this matter?**

Distinguished engineers set the quality bar for entire organizations. Their review practices directly influence engineering culture, code quality, and team velocity.

---

## Technical Findings (L1 - Engineer Level)

### 1. Google Code Review Standards

Google's engineering practices represent one of the most influential code review frameworks in industry.

#### Core Philosophy

> "Reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn't perfect."
> -- [Google Engineering Practices](https://google.github.io/eng-practices/review/reviewer/standard.html)

#### The Standard of Code Review

| Principle | Description |
|-----------|-------------|
| **Improve, Don't Perfect** | Accept code that makes things better, even if not ideal |
| **Balance Progress vs Quality** | Developers must be able to make progress; blocking creates disincentive |
| **Continuous Improvement** | Seek steady improvement, not perfection |
| **Data Over Opinion** | Technical facts and measurable evidence override preferences |

#### Approval Criteria

1. **Approve when improvements outweigh imperfections**
2. **Reject only when necessary** - Deny approval only if feature is unwanted or quality genuinely declines
3. **Minor suggestions**: Use "Nit:" prefix for non-critical points the author can ignore
4. **Style guide authority**: The official style guide is absolute
5. **Consistency matters**: Match existing codebase unless it worsens health

#### Conflict Resolution Escalation

```
Direct discussion (author <-> reviewer)
         |
         v
Face-to-face / video conversation
         |
         v
Team leads / maintainers
         |
         v
Engineering managers
```

**Critical Rule:** Don't leave code review blocked - resolve conflicts promptly.

#### Response Time Expectation

> "One business day is the maximum time it should take to respond to a code review request."

---

### 2. NASA IV&V (Independent Verification & Validation)

NASA's approach represents formal, high-rigor review for safety-critical systems.

#### Verification vs Validation

| Aspect | Verification | Validation |
|--------|--------------|------------|
| Question | "Did we build it right?" | "Did we build the right thing?" |
| Focus | Conformance to design specs | Meeting user needs |
| Method | Technical review | User acceptance |

#### IV&V Independence Dimensions

1. **Technical independence** - Separate expertise from development team
2. **Managerial independence** - Different reporting structure
3. **Financial independence** - Separate budget authority

#### Peer Review Methods

From [NASA Software Engineering Handbook](https://swehb.nasa.gov/):

- Participation in planned software peer reviews or software inspections
- Recording peer review measurements
- Status reporting to stakeholders
- Results of current or completed analysis
- Defect and risk identification

#### V&V Planning Elements

- Functional demonstrations
- Acceptance testing against mathematical models
- Software peer reviews/inspections
- Behavior validation in simulated environments
- Analysis methods

---

### 3. Principal/Staff Engineer Role (Larson & Reilly)

#### Four Staff Engineer Archetypes (Will Larson)

From [StaffEng.com](https://staffeng.com/guides/staff-archetypes/):

| Archetype | Primary Responsibility | Review Focus |
|-----------|----------------------|--------------|
| **Tech Lead** | Guides execution for team cluster | Cross-team coordination, technical vision |
| **Architect** | Owns technical domain success | API design, system coherence, technical debt |
| **Solver** | Addresses critical high-risk problems | Deep problem analysis, solution validation |
| **Right Hand** | Extends executive capacity | Cross-cutting concerns, fire management |

#### Key Staff+ Activities

From [Staff Engineer book](https://staffeng.com/book/):

1. **Setting technical direction** - Defining and editing where teams should head
2. **Mentorship and sponsorship** - Growing engineers around you
3. **Injecting engineering context** - Bringing technical perspective to org decisions
4. **Exploration** - Investigating unknown territories
5. **Being glue** (Tanya Reilly) - Connecting disparate parts of organization

#### Sponsorship Over Heroics

> "You're far more likely to change your company's long-term trajectory by growing the engineers around you than through personal heroics."

**Sponsorship activities:**
- Creating space for others to shine
- Encouraging engineers to present at company meetings
- Inviting others to "The Room" when appropriate
- Empowering soft skill development

#### Technical Quality Ownership

From Larson's guidance on managing technical quality:

1. Start with lightweight solutions
2. Progress to larger ones only if necessary
3. Prioritize understanding specific problem areas
4. Roll out new practices gradually
5. Focus on success with few teams before scaling

---

### 4. Architecture Decision Records (ADRs)

#### ADR Lifecycle States

From [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html):

```
Proposed --> Review --> Accepted
                   \--> Rejected

Accepted --> Superseded (by newer ADR)
```

**Key Principle:** Accepted/Rejected ADRs are **immutable**. To change an accepted decision, create a new ADR.

#### ADR Minimum Contents

| Section | Purpose |
|---------|---------|
| **Context** | The situation requiring a decision |
| **Decision** | The choice made |
| **Consequences** | Impact on project and deliverables |

**Focus on WHY, not HOW.**

#### Review Process

1. **Creation** - Any team member can create; designate owner
2. **Review Meeting** - Dedicated reading time (10-15 minutes)
3. **Discussion** - Team adds comments and questions
4. **Decision** - Approve, Reject, or Request Improvement

#### Decision Outcomes

| Outcome | Action |
|---------|--------|
| **Needs Improvement** | Stays "Proposed"; owner assigns action items |
| **Rejected** | Document reason; prevent future re-discussion |
| **Approved** | Add timestamp, version, stakeholders; mark "Accepted" |

#### ADR in Code Review

- Use ADRs during code and architectural reviews
- Code reviewers flag violations and link to relevant ADRs
- Changes must conform to accepted ADRs

---

### 5. TOGAF Architecture Governance

#### Architecture Board Responsibilities

From [TOGAF Standard](https://pubs.opengroup.org/architecture/togaf9-doc/arch/chap41.html):

1. Visible escalation mechanism for decisions outside established boundaries
2. Resolve ambiguities, issues, or conflicts
3. Ensure consistent architecture implementation
4. Formal acceptance and approval through consensus
5. Maintain link between implementation and strategic objectives

#### Compliance Review Checkpoints

- **ADM compliance** - Development of architecture itself
- **Architecture compliance** - Implementation of architecture(s)
- Normally mandated by enterprise CIO or Architecture Board
- Annual reviews typical for major projects

#### Dispensation Process

When deviations are necessary:
1. Register the change
2. Monitor compliance
3. Assess suitability
4. Document through Architecture Compliance assessments

---

### 6. Microsoft Code Review Research

#### Empirical Findings

From [Microsoft Research](https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/):

| Finding | Implication |
|---------|-------------|
| Feedback quality decreases with change size | Keep changes small |
| Useful comments increase in first year, then plateau | Experience matters, but growth slows |
| Usefulness depends on linguistic characteristics | Politeness and comprehensibility matter |
| 36% perform code reviews multiple times daily | Review is core engineering activity |

#### 30 Best Practices Summary (Dr. Michaela Greiler)

**For Authors:**
1. Self-review first
2. Keep changes small (< 400 lines ideal)
3. Group related modifications
4. Write descriptive summaries
5. Run tests beforehand
6. Automate quality checks
7. Limit to 2 active reviewers
8. Include experienced AND junior reviewers

**For Reviewers:**
1. Be constructive and respectful
2. Use synchronous discussion when needed
3. Document outcomes
4. Explain reasoning (WHY feedback matters)
5. Reject rarely (should be exceptional)
6. Schedule dedicated review time
7. Respond promptly (< 1 business day)
8. Focus on substance over style
9. Start with tests
10. Use checklists

---

### 7. Iterative Review Patterns

#### The Nature of Code Reviews

> "Code reviews rarely wrap up after just one round of feedback. They're naturally iterative."

#### When to Block vs Iterate

| Block | Don't Block |
|-------|-------------|
| Security vulnerabilities | Minor style preferences |
| Breaking changes | Non-breaking refactoring opportunities |
| Missing critical tests | Additional nice-to-have tests |
| Architectural violations | Alternative valid approaches |

#### Extended Discussion Handling

**Good Practice:**
- Switch to in-person after lengthy back-and-forth
- Proactively reach out when many comments

**Better Practice:**
- Initiate direct contact after first pass if extensive
- Recognize pattern: "many comments = likely misunderstanding"

#### Consensus-Building Mechanisms

From W3C Decision-Making:

1. **Primary approach**: Consensus building over voting
2. **Formal objections**: Require specific technical grounds
3. **Good-faith requirement**: Demonstrate effort to resolve through normal processes
4. **Escalation path**: Clear hierarchy when consensus fails

---

### 8. Fagan Inspection Method

The formal, high-rigor review method from IBM (1976).

#### Process Stages

```
Planning --> Overview --> Preparation --> Inspection --> Rework --> Follow-up
                                              ^              |
                                              |______________|
                                                (iterate)
```

#### Defined Roles

| Role | Responsibility |
|------|----------------|
| **Author** | Created the work product |
| **Moderator** | Plans and coordinates inspection |
| **Reader** | Reads through documents |
| **Recorder** | Documents defects found |
| **Inspector** | Examines for possible defects |

#### Effectiveness Metrics (IBM)

- Doubled lines of code shipped since 1976
- Defects per thousand lines reduced by two-thirds
- Single most effective software quality control method

---

## Strategic Patterns and Trade-offs (L2 - Architect Level)

### PAT-001: Health-Over-Perfection Principle

**Pattern:** Approve changes that improve overall code health even if imperfect.

**Trade-offs:**

| Benefit | Cost |
|---------|------|
| Higher velocity | Some technical debt accrues |
| Developer morale | Requires cleanup passes |
| Lower review latency | Inconsistent quality ceiling |

**When to Apply:**
- Standard feature development
- Iterative improvement cycles
- Teams with good test coverage

**When NOT to Apply:**
- Security-sensitive code
- Public API changes
- Safety-critical systems

---

### PAT-002: Data-Driven Decision Resolution

**Pattern:** Resolve review conflicts with technical facts and measurable evidence, not personal preference.

**Implementation:**
1. Request benchmarks/metrics when performance claims conflict
2. Reference style guides for formatting disputes
3. Cite documentation for API design decisions
4. Defer to consistency with existing codebase

**Escalation Hierarchy:**
```
1. Direct evidence comparison
2. Style guide authority
3. Engineering principles
4. Codebase consistency
5. Manager escalation (last resort)
```

---

### PAT-003: Tiered Review Rigor

**Pattern:** Match review depth to change risk level.

| Tier | Risk Level | Review Approach |
|------|------------|-----------------|
| **T1** | Low (config, docs) | Self-review + 1 reviewer |
| **T2** | Medium (features) | 2 reviewers, standard process |
| **T3** | High (security, APIs) | Senior reviewer, ADR if architectural |
| **T4** | Critical (safety) | Formal inspection, IV&V consideration |

---

### PAT-004: Sponsor-First Leadership

**Pattern:** Distinguished engineers create opportunities for others rather than solving everything personally.

**Mechanisms:**
- Delegate visible work to growing engineers
- Invite mid-level engineers to architecture discussions
- Review to teach, not just validate
- Credit contributors publicly

**Anti-patterns:**
- Hero engineering (solving everything yourself)
- Gatekeeping knowledge
- Review-as-approval-stamp (no feedback)

---

### PAT-005: ADR-Governed Architecture

**Pattern:** Use immutable Architecture Decision Records to govern technical direction.

**Workflow:**
```
Architectural Question
        |
        v
Search existing ADRs --> Found? --> Follow decision
        |                              |
        v                              v
Create new ADR        ADR violation? --> Link in review
        |
        v
Review & Approve/Reject
        |
        v
Reference in code reviews
```

**Trade-offs:**

| Benefit | Cost |
|---------|------|
| Consistent architecture | Process overhead |
| Decision audit trail | Initial setup effort |
| Onboarding documentation | ADR maintenance burden |

---

### PAT-006: Iterative Feedback Cycles

**Pattern:** Design reviews for multiple rounds rather than single-pass perfection.

**Implementation:**
1. First pass: Major concerns only
2. Second pass: Medium issues
3. Final pass: Nitpicks (optional for author)

**Switching to Synchronous:**
- After 3+ comment rounds
- When misunderstanding is apparent
- For sensitive feedback

---

### PAT-007: Review Checklist Standardization

**Pattern:** Use domain-specific checklists to ensure consistent, thorough reviews.

**Effectiveness:** Studies show checklist-driven reviews increase defect detection by 66.7%.

**Example Checklist Categories:**
- [ ] Tests cover happy path and edge cases
- [ ] Error handling is comprehensive
- [ ] API changes are backward compatible
- [ ] Security implications considered
- [ ] Performance impact assessed
- [ ] Documentation updated

---

## References and Citations

### Primary Sources

1. **Google Engineering Practices**
   - [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)
   - [How to do a code review](https://google.github.io/eng-practices/review/reviewer/)
   - [GitHub Repository](https://github.com/google/eng-practices)

2. **NASA Systems Engineering**
   - [NASA Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)
   - [Software IV&V](https://swehb.nasa.gov/display/SWEHBVC/SWE-141+-+Software+Independent+Verification+and+Validation)
   - [Verification and Validation Plan Outline](https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/)

3. **Staff Engineering Books**
   - Will Larson, [Staff Engineer: Leadership Beyond the Management Track](https://staffeng.com/book/)
   - Tanya Reilly, [The Staff Engineer's Path](https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/)
   - [Staff Archetypes](https://staffeng.com/guides/staff-archetypes/)

4. **TOGAF Architecture Governance**
   - [Architecture Board](https://pubs.opengroup.org/architecture/togaf9-doc/arch/chap41.html)
   - [Architecture Governance](https://pubs.opengroup.org/architecture/togaf9-doc/arch/chap44.html)
   - [Architecture Compliance](https://pubs.opengroup.org/architecture/togaf9-doc/arch/chap42.html)

5. **Architecture Decision Records**
   - [ADR GitHub Repository](https://github.com/joelparkerhenderson/architecture-decision-record)
   - [AWS ADR Process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
   - [ADR.github.io](https://adr.github.io/)
   - [How to Review ADRs](https://ozimmer.ch/practices/2023/04/05/ADRReview.html)

6. **Microsoft Research**
   - [Characteristics of Useful Code Reviews](https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/)
   - [Code Reviews at Microsoft](https://www.michaelagreiler.com/code-reviews-at-microsoft-how-to-code-review-at-a-large-software-company/)
   - [30 Code Review Best Practices](https://www.michaelagreiler.com/code-review-best-practices/)

7. **Pragmatic Engineer**
   - [Good Code Reviews, Better Code Reviews](https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/)
   - [RFCs and Design Docs](https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs)
   - [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)

8. **Fagan Inspection**
   - [Wikipedia: Fagan Inspection](https://en.wikipedia.org/wiki/Fagan_inspection)
   - [From Fagan to Google Approach](https://medium.com/ereflections/a-new-trend-on-software-engineering-with-modern-code-review-from-michal-fagan-to-google-approach-c2121870504c)

### Industry Resources

- [LeadDev: Who Are Staff, Principal, and Distinguished Engineers?](https://leaddev.com/career-ladders/who-are-staff-principal-and-distinguished-engineers)
- [LeadDev: The Reality of Being a Principal Engineer](https://leaddev.com/career-paths-progression-promotion/reality-being-principal-engineer)
- [Swarmia: Complete Guide to Code Reviews](https://www.swarmia.com/blog/a-complete-guide-to-code-reviews/)
- [Daily.dev: Software Engineering Best Practices for Code Review](https://daily.dev/blog/software-engineering-best-practices-for-code-review)

---

## Extracted Patterns Summary

| Pattern ID | Name | Primary Source |
|------------|------|----------------|
| PAT-001 | Health-Over-Perfection Principle | Google |
| PAT-002 | Data-Driven Decision Resolution | Google |
| PAT-003 | Tiered Review Rigor | NASA/Industry |
| PAT-004 | Sponsor-First Leadership | Larson/Reilly |
| PAT-005 | ADR-Governed Architecture | AWS/TOGAF |
| PAT-006 | Iterative Feedback Cycles | Microsoft/Pragmatic Engineer |
| PAT-007 | Review Checklist Standardization | Microsoft Research |

---

## Appendix: Quick Reference Card

### Distinguished Engineer Review Mindset

```
Before Review:
- Is this improving code health? (PAT-001)
- What's the risk tier? (PAT-003)
- Are there relevant ADRs? (PAT-005)

During Review:
- Focus on substance, not style
- Use data, not opinion (PAT-002)
- Plan for iteration (PAT-006)

After Review:
- Document key decisions
- Consider sponsorship opportunities (PAT-004)
- Update checklists if gaps found (PAT-007)
```

### Response Time Targets

| Context | Target |
|---------|--------|
| Standard code review | < 1 business day |
| Architecture review | < 3 business days |
| ADR review meeting | Scheduled weekly |
| Urgent/blocking | Same day |

### Escalation Decision Tree

```
Disagreement?
    |
    v
Data available? --Yes--> Compare evidence
    |
    No
    v
Style guide covers? --Yes--> Follow guide
    |
    No
    v
Engineering principle applies? --Yes--> Apply principle
    |
    No
    v
Consistency with codebase? --Yes--> Match existing
    |
    No
    v
Escalate to team lead/manager
```
