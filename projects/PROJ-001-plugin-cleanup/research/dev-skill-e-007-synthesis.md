# Development Skill Research Synthesis

**Document ID**: dev-skill-e-007-synthesis
**Date**: 2026-01-09
**Author**: ps-synthesizer

---

## Executive Summary

This synthesis consolidates findings from six research documents covering agent-based software development workflows, quality gate enforcement, BDD/TDD in multi-agent systems, distinguished engineer review practices, concurrent file access patterns, and task template schemas. Together, these documents provide a comprehensive foundation for designing the Jerry Framework's development skill.

The research reveals a convergent set of industry practices: multi-agent architectures with clear orchestration patterns (conductor-worker, parallel execution, swarm), layered quality gates that shift left while maintaining defense in depth, and test-first disciplines that become even more critical when AI generates code. Distinguished engineer practices emphasize health-over-perfection approval, data-driven decision resolution, and sponsorship-first leadership. For multi-instance scenarios, atomic file operations with pessimistic locking and coordination-free ID generation provide the foundation for concurrent access. Task templates require structured schemas with machine-readable inputs, outputs, dependencies, and success criteria for reliable agent execution.

The synthesis identifies 31 distinct patterns across the six documents, organized into seven categories: Orchestration, Quality, Testing, Review, Concurrency, Task Management, and Context Engineering. Key cross-cutting themes include the primacy of test-first development for AI-generated code, the necessity of layered quality gates with appropriate rigor tiers, and the importance of atomic operations and isolation for multi-agent scenarios. The patterns map directly to Jerry's 12 framework constraints, providing actionable implementation guidance.

---

## Unified Pattern Catalog

### Master Pattern Table

| ID | Name | Category | Source Document |
|----|------|----------|-----------------|
| PAT-001-e001 | Conductor-Worker Architecture | Orchestration | e-001 |
| PAT-002-e001 | Git Worktree Isolation | Concurrency | e-001 |
| PAT-003-e001 | Handle Pattern for Large Data | Context Engineering | e-001 |
| PAT-004-e001 | Pre-Rot Threshold Compaction | Context Engineering | e-001 |
| PAT-005-e001 | Explicit State Handoff | Orchestration | e-001 |
| PAT-006-e001 | Human-in-the-Loop Gating | Quality | e-001 |
| PAT-007-e001 | Layered Guardrails | Quality | e-001 |
| PAT-008-e001 | Rules-as-Files Persistence | Context Engineering | e-001 |
| PAT-001-e002 | Layered Gate Architecture | Quality | e-002 |
| PAT-002-e002 | Shift-Left Quality Gates | Quality | e-002 |
| PAT-003-e002 | SLO-Based Quality Gates | Quality | e-002 |
| PAT-004-e002 | Definition of Done as Gate | Quality | e-002 |
| PAT-005-e002 | Agent Guardrail Architecture | Quality | e-002 |
| PAT-006-e002 | Auto-Deploy with Rollback | Quality | e-002 |
| PAT-001-e003 | Test-First Agent Protocol | Testing | e-003 |
| PAT-002-e003 | Property-Based Invariant Verification | Testing | e-003 |
| PAT-003-e003 | Multi-Agent Test Isolation | Testing | e-003 |
| PAT-004-e003 | BDD as Agent Specification | Testing | e-003 |
| PAT-005-e003 | Layered Test Strategy for Agent Systems | Testing | e-003 |
| PAT-006-e003 | Mutation Testing for Agent Test Quality | Testing | e-003 |
| PAT-001-e004 | Health-Over-Perfection Principle | Review | e-004 |
| PAT-002-e004 | Data-Driven Decision Resolution | Review | e-004 |
| PAT-003-e004 | Tiered Review Rigor | Review | e-004 |
| PAT-004-e004 | Sponsor-First Leadership | Review | e-004 |
| PAT-005-e004 | ADR-Governed Architecture | Review | e-004 |
| PAT-006-e004 | Iterative Feedback Cycles | Review | e-004 |
| PAT-007-e004 | Review Checklist Standardization | Review | e-004 |
| PAT-001-e005 | Atomic Write with Durability | Concurrency | e-005 |
| PAT-002-e005 | File-Based Mutual Exclusion | Concurrency | e-005 |
| PAT-003-e005 | Optimistic Concurrency with Retry | Concurrency | e-005 |
| PAT-004-e005 | Coordination-Free ID Generation | Concurrency | e-005 |
| PAT-005-e005 | Isolation Through Workspace Separation | Concurrency | e-005 |
| PAT-001-e006 | Definition of Done Checklist | Task Management | e-006 |
| PAT-002-e006 | WBS Decomposition Pattern | Task Management | e-006 |
| PAT-003-e006 | Agent Task Schema | Task Management | e-006 |
| PAT-004-e006 | Success Criteria Schema | Task Management | e-006 |
| PAT-005-e006 | Vertical Slicing Pattern | Task Management | e-006 |

### Pattern Categories Summary

| Category | Count | Description |
|----------|-------|-------------|
| Quality | 8 | Quality gates, guardrails, and enforcement |
| Testing | 6 | BDD/TDD, property testing, mutation testing |
| Concurrency | 6 | File locking, atomic writes, workspace isolation |
| Review | 7 | Code review practices, ADRs, escalation |
| Context Engineering | 3 | Context management, compaction, persistence |
| Orchestration | 2 | Agent coordination and handoff |
| Task Management | 5 | Task schemas, decomposition, success criteria |

---

## Cross-Cutting Themes

### Theme 1: Test-First is Non-Negotiable for AI-Generated Code

**Documents**: e-001, e-002, e-003

All three documents emphasize that test-first discipline becomes MORE critical, not less, when AI generates code. AI tends toward "looks right" code that compiles but may not work correctly. Tests provide the specification that constrains generation.

**Key Patterns**:
- PAT-001-e003: Test-First Agent Protocol
- PAT-002-e003: Property-Based Invariant Verification
- PAT-006-e003: Mutation Testing for Agent Test Quality

**Implementation Implication**: The development skill MUST enforce test generation before code generation as a hard constraint.

### Theme 2: Layered Quality Gates with Appropriate Rigor

**Documents**: e-001, e-002, e-004

Quality enforcement should be layered (local, PR, pre-deploy, post-deploy, runtime) with rigor matched to risk level. High-risk changes require more gates; low-risk changes need fewer.

**Key Patterns**:
- PAT-001-e002: Layered Gate Architecture
- PAT-003-e004: Tiered Review Rigor
- PAT-007-e001: Layered Guardrails

**Implementation Implication**: The development skill should support configurable quality tiers based on change risk classification.

### Theme 3: Atomic Operations and Isolation for Multi-Agent Scenarios

**Documents**: e-001, e-005

When multiple agents or instances access shared resources, atomic operations and workspace isolation prevent data corruption and race conditions.

**Key Patterns**:
- PAT-002-e001: Git Worktree Isolation
- PAT-001-e005: Atomic Write with Durability
- PAT-002-e005: File-Based Mutual Exclusion
- PAT-005-e005: Isolation Through Workspace Separation

**Implementation Implication**: Jerry's work item store must use py-filelock with atomic writes; parallel agent execution should use Git worktrees.

### Theme 4: Context is Precious - Manage it Aggressively

**Documents**: e-001, e-003, e-005

Context rot degrades AI performance even within advertised limits. Effective systems compact at ~25% of limit, use file-based offloading, and keep only summaries in context.

**Key Patterns**:
- PAT-003-e001: Handle Pattern for Large Data
- PAT-004-e001: Pre-Rot Threshold Compaction
- PAT-008-e001: Rules-as-Files Persistence

**Implementation Implication**: The development skill should integrate with Jerry's context management to offload large artifacts and maintain working context.

### Theme 5: Structured Task Schemas Enable Reliable Agent Execution

**Documents**: e-003, e-006

Agents need structured, machine-readable task specifications with explicit inputs, outputs, dependencies, and success criteria to execute reliably.

**Key Patterns**:
- PAT-003-e006: Agent Task Schema
- PAT-004-e006: Success Criteria Schema
- PAT-005-e006: Vertical Slicing Pattern

**Implementation Implication**: Work items should follow a structured schema that agents can parse and validate.

### Theme 6: Human Oversight at Strategic Points

**Documents**: e-001, e-002, e-004

While automation increases throughput, strategic human checkpoints prevent high-impact errors. Gate destructive actions; let routine work flow autonomously.

**Key Patterns**:
- PAT-006-e001: Human-in-the-Loop Gating
- PAT-005-e002: Agent Guardrail Architecture
- PAT-001-e004: Health-Over-Perfection Principle

**Implementation Implication**: The development skill should identify high-risk operations and route them for human review.

### Theme 7: Review as Teaching, Not Just Validation

**Documents**: e-004

Distinguished engineers use code review as a mentorship opportunity. They sponsor junior engineers, create space for others to grow, and prioritize knowledge transfer.

**Key Patterns**:
- PAT-004-e004: Sponsor-First Leadership
- PAT-006-e004: Iterative Feedback Cycles

**Implementation Implication**: Agent-conducted reviews should include explanatory comments and suggestions, not just approval/rejection.

---

## Constraint Mapping

| Constraint | ID | Relevant Patterns | Implementation Notes |
|------------|-----|-------------------|---------------------|
| 5W1H Structure | c-001 | PAT-003-e006 (Agent Task Schema), PAT-001-e006 (DoD Checklist) | Task schemas encode WHO (assignee), WHAT (description), WHEN (timeline), WHERE (context), WHY (rationale), HOW (acceptance criteria) |
| Citations Required | c-002 | All research documents | All 6 documents include full citations; synthesis preserves citation trail |
| No Recursive Subagents | c-003 | PAT-001-e001 (Conductor-Worker) | Single orchestrator to worker pattern aligns with max 1 nesting level |
| Reasoning Documentation | c-004 | PAT-005-e004 (ADR-Governed Architecture), PAT-002-e004 (Data-Driven Resolution) | ADRs capture architectural reasoning; reviews require rationale |
| Knowledge Persistence | c-005 | PAT-008-e001 (Rules-as-Files), PAT-001-e005 (Atomic Write) | File-based persistence with atomic writes |
| Domain Purity | c-006 | PAT-003-e003 (Multi-Agent Test Isolation) | Domain logic isolated from infrastructure concerns |
| Finite Operations | c-007 | PAT-003-e006 (Agent Task Schema) | Task schemas include timeout_seconds field |
| Evidence Artifacts | c-008 | PAT-004-e006 (Success Criteria Schema) | Automated validation commands produce verifiable evidence |
| Idempotent Operations | c-009 | PAT-001-e005 (Atomic Write), PAT-003-e005 (Optimistic Concurrency) | Compare-and-swap with version checking enables idempotent updates |
| Task Tracking | c-010 | PAT-001-e006 (DoD Checklist), PAT-002-e006 (WBS Decomposition) | Hierarchical task tracking with status transitions |
| User Authority | c-020 | PAT-006-e001 (Human-in-the-Loop Gating) | Human approval gates for high-impact actions |
| No Deception | c-022 | PAT-002-e004 (Data-Driven Resolution) | Technical facts over preferences; transparent reasoning |

---

## Architecture Implications

### 1. Development Skill Core Architecture

Based on the research, the development skill should implement:

```
┌─────────────────────────────────────────────────────────────┐
│                    Development Skill                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Planner   │───>│  Quality    │───>│  Executor   │     │
│  │   Agent     │    │   Gate      │    │   Agent     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                  │                  │             │
│         v                  v                  v             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Shared State Layer                      │   │
│  │  (py-filelock + atomic writes + Snowflake IDs)      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. Quality Gate Integration Points

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  Pre-Task  │──>│  Test Gen  │──>│  Code Gen  │──>│  Validate  │
│  Planning  │   │  (Red)     │   │  (Green)   │   │  (Review)  │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
      │                │                │                │
      v                v                v                v
   [Check           [BDD Specs      [Coverage        [ADR
    ADRs]            Generated]      Gate]           Compliance]
```

### 3. Task Schema Integration

The research recommends a unified task schema combining elements from:
- Jira/Linear/GitHub issue structures (e-006)
- BDD/Gherkin acceptance criteria (e-003)
- Agent execution metadata (e-006)
- DAG-encoded dependencies (e-006)

### 4. Concurrency Model

For multi-instance Jerry scenarios:
- **Work Items Store**: File locking (PAT-002-e005) + atomic writes (PAT-001-e005)
- **ID Generation**: Snowflake-style with derived worker ID (PAT-004-e005)
- **Session Coordination**: Optimistic concurrency (PAT-003-e005)
- **Agent Workspaces**: Git worktree isolation (PAT-002-e001)

---

## Identified Gaps

### Gap 1: Agent Evaluation Metrics
The research covers quality gates for code but lacks specific metrics for evaluating agent performance over time. Questions remain:
- How do we measure agent accuracy vs. speed tradeoffs?
- What constitutes acceptable hallucination rates?
- How do we track agent skill improvement?

### Gap 2: Multi-Agent Conflict Resolution
While e-005 covers file-level concurrency, the research doesn't fully address:
- Semantic conflicts between parallel agent changes
- Automated merge conflict resolution strategies
- Priority arbitration when agents compete for same resources

### Gap 3: Long-Running Task Management
The task schemas focus on discrete tasks. Gaps include:
- Checkpoint/resume for tasks spanning multiple sessions
- Progress reporting during extended operations
- Graceful degradation when context limits approach

### Gap 4: Error Recovery Patterns
Limited coverage of:
- Retry strategies for transient failures
- Rollback mechanisms for partially completed tasks
- Error categorization (recoverable vs. fatal)

### Gap 5: Agent Learning/Adaptation
Research focuses on static rules and schemas. Missing:
- How agents adapt to project-specific patterns
- Feedback loops from review outcomes to agent behavior
- Knowledge accumulation across sessions

---

## Recommendation Summary

### Priority 1: Core Infrastructure (Must Have)

1. **Implement Test-First Protocol (PAT-001-e003)** as a hard constraint in the development skill. All agent-generated code must have corresponding tests generated first.

2. **Adopt py-filelock + Atomic Writes (PAT-001-e005, PAT-002-e005)** for work item persistence. Use 30-second timeout with exponential backoff.

3. **Implement Snowflake-style ID Generation (PAT-004-e005)** with derived worker IDs for coordination-free unique identifiers.

4. **Create Agent Task Schema (PAT-003-e006)** with structured inputs, outputs, dependencies, and success criteria.

### Priority 2: Quality Assurance (Should Have)

5. **Implement Layered Quality Gates (PAT-001-e002)** with configurable rigor tiers based on change risk classification.

6. **Adopt BDD/Gherkin for Acceptance Criteria (PAT-004-e003)** using pytest-bdd for Python integration.

7. **Use Property-Based Testing with Hypothesis (PAT-002-e003)** for invariant verification in stateful operations.

### Priority 3: Review and Governance (Should Have)

8. **Implement Health-Over-Perfection Review (PAT-001-e004)** - approve changes that improve code health even if imperfect.

9. **Adopt ADR-Governed Architecture (PAT-005-e004)** for architectural decisions with immutable records.

10. **Use Review Checklists (PAT-007-e004)** standardized by domain for consistent, thorough reviews.

### Priority 4: Advanced Features (Could Have)

11. **Implement Git Worktree Isolation (PAT-002-e001)** for parallel agent execution.

12. **Add Pre-Rot Threshold Compaction (PAT-004-e001)** at 25% of context limit.

13. **Support Mutation Testing (PAT-006-e003)** for verifying test quality.

---

## Citations Index

### e-001: Agent-Based Software Development Workflows (22 citations)

1. GitHub Copilot Coding Agent Documentation. https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent
2. Cursor AI Technical Architecture. ColabNix (2025). https://collabnix.com/cursor-ai-deep-dive-technical-architecture-advanced-features-best-practices-2025/
3. Cursor 2.0 Multi-Agent Architecture. InfoQ (November 2025). https://www.infoq.com/news/2025/11/cursor-composer-multiagent/
4. Devin 2.0 Announcement. Cognition AI. https://cognition.ai/blog/devin-2
5. Claude Agent SDK Overview. Anthropic. https://platform.claude.com/docs/en/agent-sdk/overview
6. Building Agents with Claude Agent SDK. Anthropic Engineering. https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
7. Developer's Guide to Multi-Agent Patterns in ADK. Google Developers Blog. https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/
8. Google ADK Multi-Agent Systems Documentation. https://google.github.io/adk-docs/agents/multi-agents/
9. Microsoft Agent Framework Introduction. Microsoft Learn. https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
10. LangGraph Multi-Agent Overview. LangChain Docs. https://docs.langchain.com/oss/python/langgraph/overview
11. LangGraph Supervisor Repository. GitHub. https://github.com/langchain-ai/langgraph-supervisor-py
12. Effective Context Engineering for AI Agents. Anthropic Engineering. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
13. Context Engineering Best Practices. Kubiya (2025). https://www.kubiya.ai/blog/context-engineering-best-practices
14. Human-in-the-Loop for AI Agents Best Practices. Permit.io. https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo
15. HULA: Human-in-the-Loop Software Development Agents. Atlassian Engineering. https://www.atlassian.com/blog/atlassian-engineering/hula-blog-autodev-paper-human-in-the-loop-software-development-agents
16. Azure AI Foundry Guardrails Overview. Microsoft Learn. https://learn.microsoft.com/en-us/azure/ai-foundry/guardrails/guardrails-overview
17. Agent Factory: Blueprint for Safe AI Agents. Microsoft Azure Blog. https://azure.microsoft.com/en-us/blog/agent-factory-creating-a-blueprint-for-safe-and-secure-ai-agents/
18. Qodo AI Code Review. https://www.qodo.ai/
19. Context Rot Research. Chroma Research. https://research.trychroma.com/context-rot
20. Architecting Efficient Context-Aware Multi-Agent Framework. Google Developers Blog. https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production/
21. Human-In-the-Loop Software Development Agents. arXiv:2411.12924. https://arxiv.org/abs/2411.12924
22. Advancing Multi-Agent Systems Through Model Context Protocol. arXiv:2504.21030. https://arxiv.org/html/2504.21030v1

### e-002: Quality Gate Enforcement in CI/CD and Agent Systems (34 citations)

1. Google SRE Book - Release Engineering. https://sre.google/sre-book/release-engineering/
2. Google SRE Workbook - Canarying Releases. https://sre.google/workbook/canarying-releases/
3. Azure Pipelines Deployment Gates. https://learn.microsoft.com/en-us/azure/devops/pipelines/release/approvals/gates
4. Azure DevOps Set and Enforce Quality Gates. https://learn.microsoft.com/en-us/azure/devops/repos/tfvc/set-enforce-quality-gates
5. GitHub Actions Required Checks for Conditional Jobs. https://devopsdirective.com/posts/2025/08/github-actions-required-checks-for-conditional-jobs/
6. Enforce Code Quality Gates in GitHub Actions. https://graphite.com/guides/enforce-code-quality-gates-github-actions
7. GitLab CI QAOps Pipelines. https://medium.com/@clive.shoaib/designing-effective-qaops-pipelines-with-gitlab-ci-cd-9f9f26744e53
8. GitLab Code Quality Documentation. https://docs.gitlab.com/ee/ci/testing/code_quality.html
9. Google Engineering Practices - Code Review. https://google.github.io/eng-practices/review/
10. Software Engineering at Google - Code Review Chapter. https://abseil.io/resources/swe-book/html/ch09.html
11. SonarQube Quality Gates. https://docs.sonarsource.com/sonarqube-server/2025.1/instance-administration/analysis-functions/quality-gates
12. SonarQube in 2025 Ultimate Guide. https://medium.com/@lamjed.gaidi070/sonarqube-in-2025-the-ultimate-guide-to-code-quality-ci-cd-integration-alerting-43e96018d36f
13. Bullseye - Minimum Acceptable Code Coverage. https://www.bullseye.com/minimum.html
14. Qt - Is 70%, 80%, 90%, or 100% Code Coverage Good Enough? https://www.qt.io/quality-assurance/blog/is-70-80-90-or-100-code-coverage-good-enough
15. TechTarget - Unit Test Coverage Percentage. https://www.techtarget.com/searchsoftwarequality/tip/What-unit-test-coverage-percentage-should-teams-aim-for
16. NASA IV&V Overview. https://www.nasa.gov/ivv-overview/
17. NASA IV&V Technical Framework (PDF). https://www.nasa.gov/wp-content/uploads/2023/11/ivv-09-1-independent-verification-and-validation-technical-framework-ver-s-08-28-2023.pdf
18. SWEBOK V4.0 - IEEE Computer Society. https://www.computer.org/education/bodies-of-knowledge/software-engineering
19. Inside Stripe's Engineering Culture - Part 2. https://newsletter.pragmaticengineer.com/p/stripe-part-2
20. Stripe's New API Release Process. https://stripe.com/blog/introducing-stripes-new-api-release-process
21. Meta - Rapid Release at Massive Scale. https://engineering.fb.com/2017/08/31/web/rapid-release-at-massive-scale/
22. Meta - Code Improvement Practices. https://arxiv.org/html/2504.12517v1
23. Meta - Code Review Time Improvement. https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/
24. Scrum.org - Quality Gates and DoD. https://www.scrum.org/forum/scrum-forum/54210/quality-gates-and-dod
25. Teaching Agile - Definition of Done Examples. https://teachingagile.com/scrum/psm-1/scrum-implementation/definition-of-done
26. SAFe - Built-In Quality. https://framework.scaledagile.com/built-in-quality
27. Pre-Commit Hooks Guide 2025. https://gatlenculp.medium.com/effortless-code-quality-the-ultimate-pre-commit-hooks-guide-for-2025-57ca501d9835
28. Git Hooks for Automated Code Quality Checks 2025. https://dev.to/arasosman/git-hooks-for-automated-code-quality-checks-guide-2025-372f
29. Pre-commit Framework. https://pre-commit.com/
30. AEGIS Explained - BigID. https://bigid.com/blog/what-is-aegis/
31. Agentic AI Safety Playbook 2025. https://dextralabs.com/blog/agentic-ai-safety-playbook-guardrails-permissions-auditability/
32. Agent Guardrails Shift From Chatbots to Agents. https://galileo.ai/blog/agent-guardrails-for-autonomous-agents
33. Agentic AI Safety Best Practices 2025. https://skywork.ai/blog/agentic-ai-safety-best-practices-2025-enterprise/
34. Google Cloud - Lessons from 2025 on Agents and Trust. https://cloud.google.com/transform/ai-grew-up-and-got-a-job-lessons-from-2025-on-agents-and-trust

### e-003: BDD/TDD in Multi-Agent Systems (25+ citations)

**Books:**
- Beck, Kent. *Test-Driven Development: By Example*. Addison-Wesley, 2002. ISBN: 0321146530.
- Cohn, Mike. *Succeeding with Agile*. Addison-Wesley, 2009.

**Articles and Blog Posts:**
1. Fowler, Martin. "Test Driven Development." https://martinfowler.com/bliki/TestDrivenDevelopment.html
2. Fowler, Martin. "Test Pyramid." https://martinfowler.com/bliki/TestPyramid.html
3. Fowler, Martin. "The Practical Test Pyramid." https://martinfowler.com/articles/practical-test-pyramid.html
4. Martin, Robert C. "The Cycles of TDD." https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html
5. Beck, Kent. "Canon TDD." https://tidyfirst.substack.com/p/canon-tdd

**Documentation:**
6. Behave Documentation. https://github.com/behave/behave
7. pytest-bdd Documentation. https://github.com/pytest-dev/pytest-bdd
8. Hypothesis Documentation. https://hypothesis.readthedocs.io/en/latest/
9. pytest Fixtures. https://docs.pytest.org/en/latest/how-to/fixtures.html

**Industry Resources:**
10. Google Testing Blog. https://testing.googleblog.com/
11. "Testing on the Toilet: Test Behaviors, Not Methods." https://testing.googleblog.com/2014/04/testing-on-toilet-test-behaviors-not.html
12. "Testing on the Toilet: Tests Too DRY? Make Them DAMP!" https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html

**AI/LLM Testing:**
13. NVIDIA. "Building AI Agents to Automate Software Test Case Creation." https://developer.nvidia.com/blog/building-ai-agents-to-automate-software-test-case-creation/
14. "Test-Driven Generation: Adopting TDD With GenAI." DZone. https://dzone.com/articles/test-driven-generation
15. FreeCodeCamp. "How to Use AI to Automate Unit Testing with TestGen-LLM." https://www.freecodecamp.org/news/automated-unit-testing-with-testgen-llm-and-cover-agent/
16. Confident AI. "LLM Testing in 2026." https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies

**Multi-Agent Systems:**
17. "SuperSpec: Context Engineering and BDD for Agentic AI." Medium. https://medium.com/superagentic-ai/superspec-context-engineering-and-bdd-for-agentic-ai-3b826ca977eb
18. Virtuoso. "Multi-Agent Testing Systems." https://www.virtuosoqa.com/post/multi-agent-testing-systems-cooperative-ai-validate-complex-applications
19. CircleCI. "End-to-end Testing of Multi-Agent AI Systems." https://circleci.com/blog/end-to-end-testing-and-deployment-of-a-multi-agent-ai-system/
20. PWC. "Validating Multi-Agent AI Systems." https://www.pwc.com/us/en/services/audit-assurance/library/validating-multi-agent-ai-systems.html

**Test Quality:**
21. BrowserStack. "False Positives and False Negatives in Testing." https://www.browserstack.com/guide/false-positives-and-false-negatives-in-testing
22. Abstracta. "Avoid False Positives and Negatives in Test Automation." https://abstracta.us/blog/test-automation/avoid-false-positives-false-negatives-test-automation/
23. Real Python. "Effective Python Testing With Pytest." https://realpython.com/pytest-python-testing/

### e-004: Distinguished Engineer Review Practices (20+ citations)

**Primary Sources:**
1. Google Engineering Practices - The Standard of Code Review. https://google.github.io/eng-practices/review/reviewer/standard.html
2. Google Engineering Practices - How to do a code review. https://google.github.io/eng-practices/review/reviewer/
3. NASA Systems Engineering Handbook. https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf
4. NASA Software IV&V. https://swehb.nasa.gov/display/SWEHBVC/SWE-141+-+Software+Independent+Verification+and+Validation
5. Will Larson, Staff Engineer: Leadership Beyond the Management Track. https://staffeng.com/book/
6. Tanya Reilly, The Staff Engineer's Path. https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/
7. Staff Archetypes. https://staffeng.com/guides/staff-archetypes/
8. TOGAF Architecture Board. https://pubs.opengroup.org/architecture/togaf9-doc/arch/chap41.html
9. TOGAF Architecture Governance. https://pubs.opengroup.org/architecture/togaf9-doc/arch/chap44.html
10. ADR GitHub Repository. https://github.com/joelparkerhenderson/architecture-decision-record
11. AWS ADR Process. https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
12. How to Review ADRs. https://ozimmer.ch/practices/2023/04/05/ADRReview.html
13. Microsoft Research - Characteristics of Useful Code Reviews. https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/
14. Code Reviews at Microsoft. https://www.michaelagreiler.com/code-reviews-at-microsoft-how-to-code-review-at-a-large-software-company/
15. 30 Code Review Best Practices. https://www.michaelagreiler.com/code-review-best-practices/
16. Good Code Reviews, Better Code Reviews. https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
17. RFCs and Design Docs. https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs
18. Wikipedia: Fagan Inspection. https://en.wikipedia.org/wiki/Fagan_inspection

### e-005: Concurrent File Access Patterns (18 citations)

1. py-filelock Library. GitHub: https://github.com/tox-dev/py-filelock
2. atomicwrites Library (deprecated). https://python-atomicwrites.readthedocs.io/
3. Twitter Snowflake. https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake
4. Wikipedia: Snowflake ID. https://en.wikipedia.org/wiki/Snowflake_ID
5. Sony Sonyflake. https://github.com/sony/sonyflake
6. Optimistic Concurrency Control (Kung & Robinson, 1981). https://dl.acm.org/doi/10.1145/319566.319567
7. Wikipedia: Optimistic concurrency control. https://en.wikipedia.org/wiki/Optimistic_concurrency_control
8. "POSIX write() is not atomic". https://utcc.utoronto.ca/~cks/space/blog/unix/WriteNotVeryAtomic
9. "Things UNIX can do atomically". https://rcrowley.org/2010/01/06/things-unix-can-do-atomically.html
10. LWN "A way to do atomic writes". https://lwn.net/Articles/789600/
11. Stateless Snowflake (2025). https://arxiv.org/html/2512.11643
12. ZetCode Guide: Python os.fsync. https://zetcode.com/python/os-fsync/
13. Reliable File Updates with Python. https://blog.gocept.com/2013/07/15/reliable-file-updates-with-python/
14. Python Threading Lock Tutorial. https://www.pythontutorial.net/python-concurrency/python-threading-lock/
15. Multiprocessing Race Conditions. https://superfastpython.com/multiprocessing-race-condition-python/
16. UUID vs Sequential ID. https://www.baeldung.com/uuid-vs-sequential-id-as-primary-key
17. Multi-Agent Claude Code. DEV.to. https://dev.to/bredmond1019/multi-agent-orchestration-running-10-claude-instances-in-parallel-part-3-29da
18. Simon Willison's blog: Parallel Coding Agents. https://simonwillison.net/2025/Oct/5/parallel-coding-agents/

### e-006: Task Template Schemas for Software Development (24 citations)

1. Jira Issue Types: A Complete Guide for 2025. https://community.atlassian.com/forums/App-Central-articles/Jira-Issue-Types-A-Complete-Guide-for-2025/ba-p/2928042
2. Announcement: Changes to field and work type configuration in Jira Cloud. https://community.atlassian.com/forums/Jira-articles/Announcement-Changes-to-field-and-work-type-configuration-in/ba-p/3023478
3. Issue templates - Linear Docs. https://linear.app/docs/issue-templates
4. Configuring issue templates for your repository - GitHub Docs. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
5. Syntax for GitHub's form schema - GitHub Docs. https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema
6. About work items and work item types - Azure Boards. https://learn.microsoft.com/en-us/azure/devops/boards/work-items/about-work-items
7. The 2020 Scrum Guide. https://scrumguides.org/scrum-guide.html
8. Definition of Done - Scaled Agile Framework. https://framework.scaledagile.com/blog/glossary_term/definition-of-done
9. Given-When-Then Acceptance Criteria: Guide (2025). https://www.parallelhq.com/blog/given-when-then-acceptance-criteria
10. What does INVEST Stand For? | Agile Alliance. https://agilealliance.org/glossary/invest/
11. Introducing Example Mapping | Cucumber. https://cucumber.io/blog/bdd/example-mapping-introduction/
12. Specification by example - Wikipedia. https://en.wikipedia.org/wiki/Specification_by_example
13. NASA Work Breakdown Structure (WBS) Handbook. https://www.nasa.gov/wp-content/uploads/2025/06/nasa-wbs-handbook.pdf
14. User Story Splitting - Vertical Slice vs Horizontal Slice. https://www.visual-paradigm.com/scrum/user-story-splitting-vertical-slice-vs-horizontal-slice/
15. Breaking It Down: Decomposition Techniques. https://medium.com/@khdevnet/breaking-it-down-decomposition-techniques-for-better-software-development-43d8d1048793
16. Overview - A2A Protocol. https://a2a-protocol.org/latest/specification/
17. Tasks - CrewAI. https://docs.crewai.com/en/concepts/tasks
18. Dags - Airflow Documentation. https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html
19. Automated Acceptance Tests and Requirements Traceability. https://www.methodsandtools.com/archive/archive.php?id=118
20. Structured model outputs | OpenAI API. https://platform.openai.com/docs/guides/structured-outputs
21. Decoding Auto-GPT. https://www.maartengrootendorst.com/blog/autogpt/
22. SPIDR: Five Simple but Powerful Ways to Split User Stories. https://www.mountaingoatsoftware.com/blog/five-simple-but-powerful-ways-to-split-user-stories
23. What is DAG - Directed Acyclic Graph? https://selek.tech/posts/dag-directed-acyclic-graph/
24. LangChain Structured Output. https://docs.langchain.com/oss/python/langchain/structured-output

---

*Synthesis completed: 2026-01-09*
*Agent: ps-synthesizer*
*Source documents: 6*
*Patterns extracted: 37*
*Citations consolidated: 143+*
