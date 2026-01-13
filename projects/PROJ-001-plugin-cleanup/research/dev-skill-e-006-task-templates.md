# Research: Task Template Schemas for Software Development

**PS ID:** dev-skill
**Entry ID:** e-006
**Date:** 2026-01-09
**Author:** ps-researcher agent v2.0.0
**Topic:** Task template schemas for software development

---

## L0: Executive Summary (ELI5)

Task templates are like forms that help teams describe work consistently. Just like a job application has specific fields to fill out, task templates have fields like "title," "description," "who's doing it," and "what does done look like."

The best systems use:
1. **Hierarchical work items** - Big goals break into smaller tasks (Epic > Story > Task > Subtask)
2. **Clear done criteria** - A checklist everyone agrees means "finished"
3. **Testable acceptance criteria** - "Given X, When Y, Then Z" format
4. **Dependency tracking** - Which tasks must finish before others can start
5. **Agent-readable metadata** - Structured data that AI can parse and execute

For AI agents specifically, tasks need machine-readable inputs, outputs, success criteria, and dependency information encoded in a standard format (usually JSON Schema).

---

## L1: Technical Findings

### 1. Work Item Schemas

#### 1.1 Jira Issue Structure

Jira uses a hierarchical work type system with configurable fields [1]:

**Default Work Types:**
- **Epic** - High-level initiatives or features
- **Story** - User-centric requirements
- **Task** - Generic work units
- **Bug** - Defects or problems
- **Sub-task** - Smaller, actionable pieces of larger items

**Mandatory Fields:**
- Project (system)
- Issue Type (system)
- Summary (required)

**Common Fields:**
- Description
- Status (workflow-driven)
- Assignee
- Reporter
- Priority
- Linked Issues
- Labels
- Custom Fields

**Key Architecture Points:**
- Field configurations group fields for management
- Work type schemes associate types with projects/spaces
- Hierarchy is parent-child based, not type-restricted (except subtasks)
- 2026 update: Limit of 700 fields per configuration, 150 work types per scheme [2]

```yaml
# Conceptual Jira issue structure
issue:
  key: "PROJ-123"
  type: "Story"
  summary: "User login functionality"
  description: "As a user, I want to log in..."
  status: "In Progress"
  priority: "High"
  assignee: "developer@example.com"
  parent: "PROJ-100"  # Epic
  labels: ["authentication", "mvp"]
  custom_fields:
    story_points: 5
    sprint: "Sprint 23"
```

#### 1.2 Linear Issue Templates

Linear provides two template types [3]:

**Standard Templates:**
- Pre-fill issue properties
- Support placeholder text
- Applied at creation time

**Form Templates:**
- Structured input collection
- Required field validation
- Triggered via Slack integration or Asks

**Fillable Properties:**
- Team
- Status
- Priority
- Assignee
- Project
- Label
- Sub-issue relationships

**Scope:**
- Workspace templates (cross-team)
- Team templates (team-specific, access to team labels/statuses)

#### 1.3 GitHub Issues Schema

GitHub Issues supports two formats [4][5]:

**Markdown Templates (.md):**
```yaml
---
name: Bug Report
about: Report a bug in the software
title: '[BUG] '
labels: bug
assignees: ''
---

## Description
[Describe the bug]

## Steps to Reproduce
1.
2.
3.

## Expected Behavior

## Actual Behavior
```

**YAML Form Schema (.yml):**
```yaml
name: Bug Report
description: File a bug report
title: "[Bug]: "
labels: ["bug", "triage"]
assignees:
  - octocat
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  - type: input
    id: contact
    attributes:
      label: Contact Details
      description: How can we reach you?
      placeholder: ex. email@example.com
    validations:
      required: false
  - type: dropdown
    id: version
    attributes:
      label: Version
      description: What version are you running?
      options:
        - 1.0.0
        - 1.1.0
        - 2.0.0
      default: 0
    validations:
      required: true
  - type: checkboxes
    id: terms
    attributes:
      label: Code of Conduct
      options:
        - label: I agree to follow the Code of Conduct
          required: true
```

**Form Element Types:**
| Type | Purpose | Key Attributes |
|------|---------|----------------|
| markdown | Display text | value |
| input | Single-line text | label, description, placeholder, value |
| textarea | Multi-line text | label, description, placeholder, value, render |
| dropdown | Selection menu | label, options, multiple, default |
| checkboxes | Multiple selections | label, options[].label, options[].required |

#### 1.4 Azure DevOps Work Item Types

Azure DevOps uses process templates (Agile, Scrum, Basic, CMMI) [6]:

**Schema Structure (XML-based):**
- FIELDS section - Define fields and rules
- WORKFLOW section - Define states and transitions
- FORM section - Define UI layout

**REST API Field Access:**
```
GET https://dev.azure.com/{org}/{project}/_apis/wit/workitemtypes/{type}/fields?api-version=7.1
```

**Custom Field Reference Names:**
- Pattern: `Custom.{FieldName}` (no spaces)
- Example: `Custom.DevOpsTriage`

**Key Characteristics:**
- Single field type per project collection
- Encourages common field reuse across projects
- XML definition allows complex rules and transitions

---

### 2. Definition of Done (DoD)

#### 2.1 Scrum Guide 2020 Requirements

The Definition of Done is a formal description of the state of the Increment when it meets the quality measures required for the product [7]:

**Key Requirements:**
1. Creates transparency - shared understanding of completion
2. If item doesn't meet DoD, cannot be released or presented at Sprint Review
3. Returns to Product Backlog if incomplete
4. Developers must conform to DoD
5. Multiple teams on same product must share same DoD
6. Organizational DoD serves as minimum standard

**2020 Changes:**
- DoD created by Scrum Team (previously Development Team)
- DoD is now an artifact commitment (alongside Product Goal and Sprint Goal)

#### 2.2 SAFe Definition of Done

SAFe scales DoD across multiple levels [8]:

**Levels:**
1. **Team Level** - Individual team's DoD
2. **Program Level** - ART (Agile Release Train) DoD
3. **Large Solution Level** - Solution-wide DoD

**Relationship to Built-in Quality:**
- Flow
- Architecture and Design Quality
- Code Quality
- System Quality
- Release Quality

**Typical DoD Items:**
```markdown
## Team DoD Example
- [ ] Code complete and peer reviewed
- [ ] Unit tests written and passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Code merged to main branch
- [ ] Documentation updated
- [ ] No critical/high bugs open
- [ ] Demo-ready in staging environment
```

#### 2.3 DoD as Checklist Pattern

**PAT-001: Definition of Done Checklist**

Purpose: Provide objective completion criteria that can be validated.

```yaml
definition_of_done:
  code:
    - description: "Code complete and follows style guide"
      verifiable: true
      automated: true
    - description: "Peer code review completed"
      verifiable: true
      automated: false
  testing:
    - description: "Unit tests written and passing"
      verifiable: true
      automated: true
      threshold: "coverage >= 80%"
    - description: "Integration tests passing"
      verifiable: true
      automated: true
  documentation:
    - description: "API documentation updated"
      verifiable: true
      automated: false
    - description: "README updated if needed"
      verifiable: false
      automated: false
  deployment:
    - description: "Deployed to staging"
      verifiable: true
      automated: true
    - description: "Smoke tests passing"
      verifiable: true
      automated: true
```

---

### 3. Acceptance Criteria Formats

#### 3.1 BDD/Gherkin Given-When-Then

The Given-When-Then format comes from Behavior-Driven Development (BDD) [9]:

**Structure:**
- **Given** - Setup/preconditions
- **When** - Action/trigger
- **Then** - Expected outcome

**Example:**
```gherkin
Feature: User Authentication

  Scenario: Successful login with valid credentials
    Given a registered user with email "user@example.com"
    And the user has password "SecurePass123"
    When the user submits login with correct credentials
    Then the user should be redirected to dashboard
    And a session token should be created

  Scenario: Failed login with invalid password
    Given a registered user with email "user@example.com"
    When the user submits login with incorrect password
    Then an error message "Invalid credentials" should display
    And no session token should be created
```

**Additional Keywords:**
- **And** - Continue previous clause
- **But** - Negative continuation
- **Background** - Shared setup for all scenarios

**Best Practices:**
- 1-3 acceptance criteria per story
- Avoid vague terms ("fast," "user-friendly")
- Quantify performance: "responds within 200ms"
- Define UX: "completes in under 3 steps"

#### 3.2 INVEST Criteria

INVEST is a checklist for evaluating user story quality [10]:

| Letter | Criterion | Description | Why It Matters |
|--------|-----------|-------------|----------------|
| I | Independent | Self-contained, no dependencies | Avoids delays and blocking |
| N | Negotiable | Solution not prescribed | Enables collaboration |
| V | Valuable | Delivers user/customer value | Ensures ROI |
| E | Estimable | Effort can be assessed | Enables planning |
| S | Small | Fits in single iteration | Enables feedback loops |
| T | Testable | Clear pass/fail criteria | Enables validation |

**Sizing Guideline:**
- For 2-week iterations: average 3-4 days total work per story

**INVEST as Definition of Ready:**
Stories meeting all criteria are "ready" for development.

#### 3.3 Example Mapping

Example Mapping is a collaborative specification technique using colored cards [11]:

**Card Types:**
| Color | Represents | Purpose |
|-------|------------|---------|
| Yellow | Story | The feature being discussed |
| Blue | Rule | Business rules/constraints |
| Green | Example | Concrete scenarios |
| Red | Question | Unresolved items |

**Session Structure:**
- Participants: 3 amigos minimum (developer, tester, product person)
- Duration: ~25 minutes per well-understood story
- Output: Rules and Examples ready for Gherkin conversion

**Signals:**
- Many red cards = story not ready for development
- Many blue cards = story too big, needs splitting
- Many green cards per rule = rule too complex

**Results (Industry Data):**
- Requirement bugs reduced from 7-8 to 0-1
- Defect slippage reduced by 90%

#### 3.4 Specification by Example (SbE)

SbE uses realistic examples instead of abstract statements [12]:

**Key Principles:**
- Collaborative approach to requirements
- Examples serve as both specification and tests
- Living documentation through executable specs
- Bridges business and technical understanding

---

### 4. Task Decomposition Patterns

#### 4.1 NASA Work Breakdown Structure (WBS)

NASA's WBS Handbook provides authoritative guidance [13]:

**Key Principles:**
1. **Product-oriented** - Not organizational structure
2. **100% Rule** - WBS captures 100% of project scope
3. **Single WBS per project** - Includes in-house, contracted, partner work
4. **Standard top levels** - Levels 1-2 follow NASA templates
5. **Maximum 7 levels** - Appropriate subdivision for management insight

**Structure:**
```
Level 1: Project
├── Level 2: Major Segment
│   ├── Level 3: System/Element
│   │   ├── Level 4: Subsystem
│   │   │   └── Level 5: Work Package
```

**Anti-patterns to Avoid:**
- Design, Engineering, Manufacturing (not products)
- Phase A, Phase B (phases, not products)
- Direct Labor, Pipe Fitters (resources, not products)

**PAT-002: WBS Decomposition Pattern**
```yaml
wbs:
  id: "1.0"
  name: "User Authentication System"
  type: "product"
  children:
    - id: "1.1"
      name: "Login Module"
      children:
        - id: "1.1.1"
          name: "Credential Validation Service"
        - id: "1.1.2"
          name: "Session Management"
    - id: "1.2"
      name: "Registration Module"
      children:
        - id: "1.2.1"
          name: "User Profile Store"
        - id: "1.2.2"
          name: "Email Verification"
```

#### 4.2 Vertical Slicing

Vertical slicing implements functionality across all layers [14]:

**The Cake Analogy (Bill Wake, 2003):**
- System layers = cake layers (UI, Logic, Data)
- Vertical slice = cutting through all layers
- Delivers "essence of whole cake"

**Benefits:**
- Earlier user value delivery
- Faster feedback loops
- Transparency of progress
- Reduced risk per slice

**SPIDR Method for Story Splitting:**
| Letter | Technique | When to Use |
|--------|-----------|-------------|
| S | Spike | Need research/learning first |
| P | Path | Multiple ways to do something (card vs Apple Pay) |
| I | Interface | Different UIs for same function |
| D | Data | Different data types or sources |
| R | Rules | Business rules can be split |

**Additional Techniques:**
- Happy path first (defer edge cases)
- Split by CRUD operations
- Split validations into separate stories

**Anti-pattern: Horizontal Slicing**
```
# BAD: Horizontal slices
Story 1: Create web service
Story 2: Create database table
Story 3: Write tests

# GOOD: Vertical slice
Story 1: User can register with email (all layers)
```

#### 4.3 Functional Decomposition

Breaking functions into smaller, specific tasks [15]:

**Pattern:**
```
High-level function
├── Specific sub-function A
│   ├── Atomic operation A1
│   └── Atomic operation A2
└── Specific sub-function B
    ├── Atomic operation B1
    └── Atomic operation B2
```

**Decomposition Types:**
1. **Functional** - By function/behavior
2. **Object-Oriented** - By objects and interactions
3. **Domain** - By business domain (DDD style)
4. **Volatility-Based** - By areas of change

---

### 5. Metadata for Agent Execution

#### 5.1 Task Schema for Agents

Based on A2A Protocol and CrewAI patterns [16][17]:

**PAT-003: Agent Task Schema**
```yaml
task:
  id: "task-001"
  name: "Implement user login"
  description: "Create login endpoint with JWT authentication"

  # Input specification
  input:
    required:
      - name: "user_stories"
        type: "array"
        schema: "UserStory[]"
      - name: "codebase_path"
        type: "string"
    optional:
      - name: "style_guide"
        type: "string"
        default: "default-style.md"

  # Output specification
  output:
    format: "structured"
    schema:
      type: "object"
      properties:
        files_created:
          type: "array"
          items:
            type: "object"
            properties:
              path: { type: "string" }
              content: { type: "string" }
        files_modified:
          type: "array"
        tests_passing:
          type: "boolean"
        coverage:
          type: "number"

  # Success criteria
  success_criteria:
    - criterion: "All tests pass"
      validation: "automated"
      command: "pytest tests/"
      expected_exit_code: 0
    - criterion: "Coverage >= 80%"
      validation: "automated"
      command: "pytest --cov=src --cov-fail-under=80"
    - criterion: "No linting errors"
      validation: "automated"
      command: "ruff check src/"

  # Dependencies
  dependencies:
    requires:
      - task_id: "task-000"
        status: "completed"
    blocks:
      - task_id: "task-002"

  # Execution metadata
  execution:
    timeout_seconds: 3600
    retry_count: 3
    tools_available:
      - "file_read"
      - "file_write"
      - "bash_execute"
      - "web_search"
```

#### 5.2 Dependency Encoding with DAGs

Directed Acyclic Graphs for task dependencies [18]:

**Properties:**
- **Directed** - Edge (a,b) means b depends on a
- **Acyclic** - No circular dependencies
- **Topological ordering** - Valid execution sequence

**Encoding Methods:**
```yaml
# Method 1: Explicit edges
dependencies:
  - from: "task-001"
    to: "task-002"
    type: "finish-to-start"
  - from: "task-001"
    to: "task-003"
    type: "finish-to-start"

# Method 2: Task-level requires
tasks:
  - id: "task-002"
    requires: ["task-001"]
  - id: "task-003"
    requires: ["task-001"]
  - id: "task-004"
    requires: ["task-002", "task-003"]

# Method 3: Airflow-style operators
task_001 >> task_002
task_001 >> task_003
[task_002, task_003] >> task_004
```

**Dependency Types:**
| Type | Notation | Meaning |
|------|----------|---------|
| Finish-to-Start | FS | B starts after A finishes |
| Start-to-Start | SS | B starts when A starts |
| Finish-to-Finish | FF | B finishes when A finishes |
| Start-to-Finish | SF | B finishes when A starts |

#### 5.3 Success Criteria Encoding

Machine-readable validation rules [19]:

**PAT-004: Success Criteria Schema**
```yaml
success_criteria:
  - id: "sc-001"
    description: "Unit tests pass"
    type: "automated"
    validation:
      command: "pytest tests/unit/"
      expected:
        exit_code: 0
      timeout_seconds: 300
    break_on_fail: true

  - id: "sc-002"
    description: "Response time < 200ms"
    type: "automated"
    validation:
      command: "ab -n 100 -c 10 http://localhost:8080/api/login"
      expected:
        output_pattern: "Time per request.*[0-9]+\\.[0-9]+ \\[ms\\]"
        threshold:
          metric: "mean_response_time"
          operator: "<"
          value: 200
          unit: "ms"
    break_on_fail: false

  - id: "sc-003"
    description: "Code review approved"
    type: "manual"
    validation:
      check_type: "approval"
      required_approvers: 1
    break_on_fail: true
```

#### 5.4 OpenAI Function Calling Schema

For LLM-based agents using structured outputs [20]:

```json
{
  "name": "execute_task",
  "description": "Execute a development task",
  "strict": true,
  "parameters": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "Unique identifier for the task"
      },
      "action": {
        "type": "string",
        "enum": ["create_file", "modify_file", "run_command", "complete"]
      },
      "file_path": {
        "type": "string",
        "description": "Path to file (for file operations)"
      },
      "content": {
        "type": "string",
        "description": "File content or command to execute"
      },
      "reasoning": {
        "type": "string",
        "description": "Explanation for this action"
      }
    },
    "required": ["task_id", "action", "reasoning"],
    "additionalProperties": false
  }
}
```

#### 5.5 AutoGPT Task Format

Agent task decomposition pattern [21]:

```json
{
  "name": "DevGPT",
  "purpose": "DevGPT is an AI designed to implement software features by analyzing requirements, writing code, and validating through tests",
  "goals": [
    "Analyze the user story and acceptance criteria",
    "Design the solution architecture",
    "Implement the feature with tests",
    "Validate against acceptance criteria",
    "Document changes in CHANGELOG.md"
  ],
  "constraints": [
    "Only modify files within the project directory",
    "Run tests before marking complete",
    "Follow existing code style"
  ],
  "memory": {
    "short_term": "conversation_context",
    "long_term": "vector_db_retrieval"
  }
}
```

---

## L2: Strategic Patterns and Trade-offs

### PAT-001: Definition of Done Checklist

**Context:** Teams need objective completion criteria.

**Solution:** Create a structured checklist with verifiable items.

**Trade-offs:**
| Aspect | Benefit | Cost |
|--------|---------|------|
| Consistency | Same standard for all work | Initial setup overhead |
| Quality | Built-in quality gates | May slow initial velocity |
| Automation | Reduce manual checking | Requires CI/CD investment |
| Transparency | Clear expectations | Rigid if over-specified |

**When to use:** Always. Every team needs a DoD.

### PAT-002: WBS Decomposition Pattern

**Context:** Large features need breakdown into manageable work.

**Solution:** Product-oriented hierarchical decomposition following 100% rule.

**Trade-offs:**
| Aspect | Benefit | Cost |
|--------|---------|------|
| Completeness | Nothing missed | Overhead for small projects |
| Communication | Common reference | Requires upfront planning |
| Control | Roll-up metrics | May encourage waterfall thinking |

**When to use:** Projects with >20 person-days of effort, multiple contributors, or regulatory requirements.

### PAT-003: Agent Task Schema

**Context:** AI agents need structured input to execute tasks reliably.

**Solution:** JSON/YAML schema with inputs, outputs, dependencies, and success criteria.

**Trade-offs:**
| Aspect | Benefit | Cost |
|--------|---------|------|
| Reliability | Predictable execution | Schema design effort |
| Validation | Automated checking | May miss edge cases |
| Debugging | Clear failure points | Verbose specifications |

**Key Requirements for Agent-Executable Tasks:**
1. **Unambiguous inputs** - Type-safe, validated
2. **Measurable outputs** - Schema-defined structure
3. **Testable criteria** - Automated validation commands
4. **Explicit dependencies** - DAG-encoded relationships
5. **Timeout bounds** - Prevent infinite loops
6. **Tool permissions** - Constrained capabilities

### PAT-004: Success Criteria Schema

**Context:** Need to verify task completion automatically.

**Solution:** Machine-readable criteria with validation commands and thresholds.

**Trade-offs:**
| Aspect | Benefit | Cost |
|--------|---------|------|
| Objectivity | No subjective judgment | May miss qualitative aspects |
| Speed | Instant validation | Setup time per task |
| Consistency | Same checks every time | May become stale |

### PAT-005: Vertical Slicing Pattern

**Context:** Need to deliver value incrementally.

**Solution:** Cut through all layers for each story.

**Trade-offs:**
| Aspect | Benefit | Cost |
|--------|---------|------|
| Early Value | Users see progress | May duplicate infrastructure |
| Feedback | Fast learning | Requires cross-functional skills |
| Risk | Smaller failures | Refactoring as patterns emerge |

**Team Requirements:** Generalizing specialists who can work across layers.

---

## Recommended Task Schema for Jerry

Based on this research, a task schema for the dev-skill should include:

```yaml
# Jerry Dev-Skill Task Template v1.0
task:
  # Identity
  id: string  # e.g., "TASK-001"
  parent_id: string | null  # For subtasks
  title: string
  description: string

  # Classification
  type: enum[epic, story, task, subtask, bug, spike]
  priority: enum[critical, high, medium, low]
  labels: string[]

  # Assignment
  assignee: string | null
  reporter: string

  # Input Specification (for agent execution)
  inputs:
    required:
      - name: string
        type: string
        description: string
    optional:
      - name: string
        type: string
        default: any

  # Output Specification
  outputs:
    schema: JSONSchema

  # Acceptance Criteria (Gherkin format)
  acceptance_criteria:
    - scenario: string
      given: string[]
      when: string[]
      then: string[]

  # Definition of Done (checklist)
  definition_of_done:
    - item: string
      automated: boolean
      validation_command: string | null

  # Dependencies (DAG encoding)
  dependencies:
    requires: string[]  # Task IDs
    blocks: string[]    # Task IDs

  # Success Criteria (for automated validation)
  success_criteria:
    - criterion: string
      validation:
        type: enum[command, api, manual]
        command: string | null
        expected: any
      break_on_fail: boolean

  # Execution Metadata
  execution:
    timeout_seconds: integer
    tools_required: string[]
    environment: object

  # Lifecycle
  status: enum[backlog, ready, in_progress, review, done, cancelled]
  created_at: datetime
  updated_at: datetime
```

---

## References

[1] [Jira Issue Types: A Complete Guide for 2025 - Atlassian Community](https://community.atlassian.com/forums/App-Central-articles/Jira-Issue-Types-A-Complete-Guide-for-2025/ba-p/2928042)

[2] [Announcement: Changes to field and work type configuration in Jira Cloud](https://community.atlassian.com/forums/Jira-articles/Announcement-Changes-to-field-and-work-type-configuration-in/ba-p/3023478)

[3] [Issue templates - Linear Docs](https://linear.app/docs/issue-templates)

[4] [Configuring issue templates for your repository - GitHub Docs](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)

[5] [Syntax for GitHub's form schema - GitHub Docs](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)

[6] [About work items and work item types - Azure Boards | Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/about-work-items?view=azure-devops)

[7] [The 2020 Scrum Guide](https://scrumguides.org/scrum-guide.html)

[8] [Definition of Done - Scaled Agile Framework](https://framework.scaledagile.com/blog/glossary_term/definition-of-done)

[9] [Given-When-Then Acceptance Criteria: Guide (2025)](https://www.parallelhq.com/blog/given-when-then-acceptance-criteria)

[10] [What does INVEST Stand For? | Agile Alliance](https://agilealliance.org/glossary/invest/)

[11] [Introducing Example Mapping | Cucumber](https://cucumber.io/blog/bdd/example-mapping-introduction/)

[12] [Specification by example - Wikipedia](https://en.wikipedia.org/wiki/Specification_by_example)

[13] [NASA Work Breakdown Structure (WBS) Handbook](https://www.nasa.gov/wp-content/uploads/2025/06/nasa-wbs-handbook.pdf)

[14] [User Story Splitting - Vertical Slice vs Horizontal Slice](https://www.visual-paradigm.com/scrum/user-story-splitting-vertical-slice-vs-horizontal-slice/)

[15] [Breaking It Down: Decomposition Techniques for Better Software Development](https://medium.com/@khdevnet/breaking-it-down-decomposition-techniques-for-better-software-development-43d8d1048793)

[16] [Overview - A2A Protocol](https://a2a-protocol.org/latest/specification/)

[17] [Tasks - CrewAI](https://docs.crewai.com/en/concepts/tasks)

[18] [Dags - Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)

[19] [Automated Acceptance Tests and Requirements Traceability](https://www.methodsandtools.com/archive/archive.php?id=118)

[20] [Structured model outputs | OpenAI API](https://platform.openai.com/docs/guides/structured-outputs)

[21] [Decoding Auto-GPT - Maarten Grootendorst](https://www.maartengrootendorst.com/blog/autogpt/)

[22] [SPIDR: Five Simple but Powerful Ways to Split User Stories - Mountain Goat Software](https://www.mountaingoatsoftware.com/blog/five-simple-but-powerful-ways-to-split-user-stories)

[23] [What is DAG - Directed Acyclic Graph?](https://selek.tech/posts/dag-directed-acyclic-graph/)

[24] [LangChain Structured Output](https://docs.langchain.com/oss/python/langchain/structured-output)

---

## Extracted Patterns Summary

| Pattern ID | Name | Category |
|------------|------|----------|
| PAT-001 | Definition of Done Checklist | Quality Assurance |
| PAT-002 | WBS Decomposition Pattern | Task Decomposition |
| PAT-003 | Agent Task Schema | Agent Execution |
| PAT-004 | Success Criteria Schema | Validation |
| PAT-005 | Vertical Slicing Pattern | Incremental Delivery |
