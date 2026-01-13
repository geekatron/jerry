# Research: BDD/TDD in Multi-Agent Systems

**PS ID:** dev-skill
**Entry ID:** e-003
**Topic:** BDD/TDD in multi-agent systems
**Date:** 2026-01-09
**Researcher:** ps-researcher agent v2.0.0

---

## Executive Summary (L0 - ELI5)

BDD (Behavior-Driven Development) and TDD (Test-Driven Development) are ways to write tests BEFORE code. Think of it like writing a recipe before cooking. BDD uses plain English like "Given I have eggs, When I cook them, Then I should have an omelet." TDD uses a traffic light pattern: Red (write a failing test), Green (make it pass), Refactor (clean up).

For AI agents that write code automatically, we need special care. The agent must write tests first, then write code to pass those tests. This prevents the agent from writing code that "looks right" but doesn't actually work. Property-based testing lets us say "this should ALWAYS be true" and the computer generates thousands of examples to check.

**Key Takeaway:** Test-first discipline is even MORE important when AI generates code, not less. The test is the specification that keeps the AI honest.

---

## Technical Findings (L1 - Engineer)

### 1. BDD Frameworks in Python

#### 1.1 Behave Framework

Behave is the primary BDD framework for Python, using Gherkin syntax for feature files.

**Feature File Structure:**
```gherkin
@tags @tag
Feature: feature name
  description
  further description

  Background: some requirement of this test
    Given some setup condition
      And some other setup action

  Scenario: some scenario
      Given some condition
       When some action is taken
       Then some result is expected.

  Scenario Outline: Outlined given, when, then
      Given there are <start> cucumbers
      When I eat <eat> cucumbers
      Then I should have <left> cucumbers

      Examples:
      | start | eat | left |
      |  12   |  5  |  7   |
```

**Environment Hooks (environment.py):**
```python
# Lifecycle hooks for test execution
# before_step(context, step), after_step(context, step)
# before_scenario(context, scenario), after_scenario(context, scenario)
# before_feature(context, feature), after_feature(context, feature)
# before_tag(context, tag), after_tag(context, tag)
# before_all(context), after_all(context)

def before_all(context):
    browser = context.config.userdata.get("browser", "chrome")
    setup_browser(browser)

def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)
```

**Context Management:**
The `context` variable runs at three levels (feature, scenario, step), automatically managed by behave. Each level can add new values or overwrite ones from higher scopes.

**Source:** [Behave Documentation](https://github.com/behave/behave)

#### 1.2 pytest-bdd Framework

pytest-bdd integrates BDD with pytest's fixture system, providing more Pythonic patterns.

**Step Definitions with Fixtures:**
```python
from pytest_bdd import given, when, then, parsers, scenarios

scenarios("scenario_outlines.feature")

@given(parsers.parse("there are {start:d} cucumbers"), target_fixture="cucumbers")
def given_cucumbers(start):
    return {"start": start, "eat": 0}

@when(parsers.parse("I eat {eat:d} cucumbers"))
def eat_cucumbers(cucumbers, eat):
    cucumbers["eat"] += eat

@then(parsers.parse("I should have {left:d} cucumbers"))
def should_have_left_cucumbers(cucumbers, left):
    assert cucumbers["start"] - cucumbers["eat"] == left
```

**Shared Steps in conftest.py:**
```python
# content of conftest.py
from pytest_bdd import given, then

@given("I have a bar", target_fixture="bar")
def bar():
    return "bar"

@then('bar should have value "bar"')
def bar_is_bar(bar):
    assert bar == "bar"
```

**Parser Types:**
- `parsers.parse()` - Simple string parsing with type conversion
- `parsers.re()` - Full regex with named groups
- `parsers.cfparse()` - Custom formatters

**Source:** [pytest-bdd Documentation](https://github.com/pytest-dev/pytest-bdd)

### 2. TDD Red/Green/Refactor Cycles

#### 2.1 Kent Beck's Canon TDD

According to Kent Beck's clarification on "Canon TDD":

> "Test-driven development is a programming workflow. A programmer needs to change the behavior of a system. TDD is intended to help the programmer create a new state where: Everything that used to work still works, the new behavior works as expected, the system is ready for the next change, and the programmer and colleagues feel confident in these points."

**The Cycle:**
1. **Red** - Write a little test that doesn't work (perhaps doesn't even compile)
2. **Green** - Make the test work quickly, committing whatever sins necessary
3. **Refactor** - Eliminate all duplication created in getting the test to work

**Key Patterns from TDD by Example:**
- **One Step Test**: Pick a test that teaches you something and that you're confident you can implement
- **Starter Test**: Start with a variant that doesn't do anything to shorten the feedback loop
- **Make it run, then make it right**: Never mix refactoring into making the test pass (the "two hats" problem)

**Sources:**
- [Martin Fowler - Test Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Uncle Bob - The Cycles of TDD](https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html)
- [Kent Beck - Canon TDD](https://tidyfirst.substack.com/p/canon-tdd)
- [Codecademy - Red, Green, Refactor](https://www.codecademy.com/article/tdd-red-green-refactor)

#### 2.2 Test-Driven Generation (TDG) for AI

When AI generates code, the TDD pattern becomes Test-Driven Generation:

1. **Spec Definition**: Provide high-level specification to AI for test generation
2. **Test Generation**: AI creates test cases based on specs
3. **Test Execution**: Run tests (they fail - no code yet)
4. **Code Spec**: Provide specification for code generation
5. **Code Generation**: AI generates code using failing test feedback
6. **Test Re-run**: Verify tests pass

> "While Generative AI can quickly produce code, it doesn't inherently guarantee that the code is correct, reliable, or meets all specified requirements. TDG incorporates the creation of test cases before code generation, ensuring that the AI-generated code is validated against these tests."

**Source:** [DZone - Test-Driven Generation](https://dzone.com/articles/test-driven-generation)

### 3. Test Pyramid for Agent Systems

#### 3.1 Martin Fowler's Test Pyramid

The test pyramid, introduced by Mike Cohn and developed by Martin Fowler:

```
        /\
       /  \     E2E Tests (few)
      /----\
     /      \   Integration Tests (some)
    /--------\
   /          \ Unit Tests (many)
  --------------
```

**Key Principles:**
- Many more low-level unit tests than high-level UI/E2E tests
- E2E tests are: brittle, expensive to write, time consuming to run
- High-level tests are "second line of defense" - before fixing a bug exposed by high-level test, replicate it with a unit test

**Google's Approach:**
Google renamed test categories from "unit/integration/system" to "small/medium/large" to clarify terminology. They recommend employing E2E tests sparingly, using unit and smaller integration tests much more heavily.

**Alternative Views:**
- **Kent C. Dodds' Testing Trophy**: Emphasizes integration tests, adds static testing
- **Guillermo Rauch**: "Write tests. Not too many. Mostly integration."

**Sources:**
- [Martin Fowler - Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html)
- [Martin Fowler - The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Google Testing Blog](https://testing.googleblog.com/)

#### 3.2 Google Testing Best Practices

From Google's "Testing on the Toilet" program:

- **Test Behaviors, Not Methods**: Focus on what the code does, not how
- **DAMP over DRY for Tests**: Tests Too DRY? Make Them DAMP! (Descriptive And Meaningful Phrases)
- **Shared Responsibility**: Developers building products also develop associated tests
- **YAGNI for Abstractions**: Tolerate duplication early, abstract when patterns emerge

**Source:** [Google Testing Blog - Testing on the Toilet](https://testing.googleblog.com/2007/01/introducing-testing-on-toilet.html)

### 4. Property-Based Testing with Hypothesis

#### 4.1 Core Concepts

Hypothesis generates diverse and challenging data, including edge cases, to test properties that must hold for ALL valid inputs.

**Composite Strategies:**
```python
from hypothesis import strategies as st, given

@st.composite
def values(draw):
    n1 = draw(st.integers())
    n2 = draw(st.integers(min_value=n1))
    return (n1, n2)

@given(values())
def test_ordering(value):
    (n1, n2) = value
    assert n1 <= n2
```

**Dynamic Generation with data():**
```python
from hypothesis import strategies as st, given

@given(st.data())
def test_dynamic_generation(data):
    n1 = data.draw(st.integers(), label="First number")
    n2 = data.draw(st.integers(min_value=n1), label="Second number")
    assert n1 <= n2
```

#### 4.2 Stateful Testing with Invariants

For testing stateful systems (like agents), Hypothesis provides RuleBasedStateMachine:

```python
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule

class NumberModifier(RuleBasedStateMachine):
    num = 0

    @rule()
    def add_two(self):
        self.num += 2
        if self.num > 50:
            self.num += 1

    @invariant()
    def is_even(self):
        assert self.num % 2 == 0

NumberTest = NumberModifier.TestCase
```

**Database Comparison State Machine:**
```python
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule
import hypothesis.strategies as st

class DatabaseComparison(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.database = DirectoryBasedExampleDatabase(tempfile.mkdtemp())
        self.model = defaultdict(set)

    keys = Bundle("keys")
    values = Bundle("values")

    @rule(target=keys, k=st.binary())
    def add_key(self, k):
        return k

    @rule(k=keys, v=values)
    def save(self, k, v):
        self.model[k].add(v)
        self.database.save(k, v)

    @rule(k=keys)
    def values_agree(self, k):
        assert set(self.database.fetch(k)) == self.model[k]
```

**Source:** [Hypothesis Documentation](https://hypothesis.readthedocs.io/en/latest/)

### 5. Test Isolation Patterns

#### 5.1 Pytest Fixtures

Fixtures are dependency injection for tests:

```python
import pytest

@pytest.fixture(scope="module", params=["mysql", "pg"])
def db(request):
    if request.param == "mysql":
        db = MySQL()
    elif request.param == "pg":
        db = PG()
    request.addfinalizer(db.destroy)
    return db

@pytest.fixture(autouse=True)
def append_first(order, first_entry):
    return order.append(first_entry)
```

**Fixture Scopes:**
- `function` (default): Setup/teardown per test function
- `class`: Once per test class
- `module`: Once per test module
- `session`: Once per test session

**Autouse Fixtures:**
Automatically invoked for all tests within scope without explicit request.

**Source:** [pytest Fixtures Documentation](https://docs.pytest.org/en/latest/how-to/fixtures.html)

#### 5.2 Test Isolation Best Practices

- **Each test starts with clean state**: Use fixtures effectively
- **Modular fixtures**: Deconstruct complex setups into smaller, reusable fixtures
- **Constructor injection + fixtures**: Combine for clarity and testability
- **Factory patterns**: For complex objects with multiple dependencies
- **Controlled environments**: Prevent data changes affecting test reproducibility

**Sources:**
- [Real Python - Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)
- [Python Unit Testing Best Practices](https://pytest-with-eric.com/introduction/python-unit-testing-best-practices/)

### 6. Agent-Generated Test Quality

#### 6.1 Challenges

- AI-generated tests often lack semantic diversity compared to human-written ones
- Effectiveness decreases for complex tasks
- Risk of testing implementation, not behavior
- Potential for false confidence (tests pass but miss real bugs)

#### 6.2 Quality Frameworks

**Meta's TestGen-LLM Results:**
- 75% of test cases built correctly
- 57% passed reliably
- 25% increased coverage
- 73% of recommendations accepted for production

**NVIDIA's HEPH Framework:**
- Uses LLM agent for every step (document traceability to code generation)
- Teams reported saving up to 10 weeks of development time

**Sources:**
- [NVIDIA - Building AI Agents to Automate Software Test Case Creation](https://developer.nvidia.com/blog/building-ai-agents-to-automate-software-test-case-creation/)
- [FreeCodeCamp - TestGen-LLM and Cover-Agent](https://www.freecodecamp.org/news/automated-unit-testing-with-testgen-llm-and-cover-agent/)

#### 6.3 Avoiding False Positives/Negatives

**False Positives (test fails but code is correct):**
- Use stable locators (data-test attributes over XPath)
- Write assertions that validate intent, not cosmetic details
- Use containerization for reliable test infrastructure
- Keep test environments aligned with production

**False Negatives (test passes but bug exists):**
- Randomize test inputs rather than hardcoding
- Use mutation testing to verify test effectiveness
- Apply equivalence partitioning and boundary value analysis
- Automate edge cases, not just happy paths

**Flaky Test Detection:**
- Run tests multiple times without code changes
- Track CI/CD patterns across runs
- Quarantine flaky tests until fixed
- Use AI-driven detection for unstable patterns

**Sources:**
- [BrowserStack - False Positives and False Negatives](https://www.browserstack.com/guide/false-positives-and-false-negatives-in-testing)
- [Abstracta - Avoid False Positives and Negatives](https://abstracta.us/blog/test-automation/avoid-false-positives-false-negatives-test-automation/)

### 7. Multi-Agent Testing Orchestration

#### 7.1 BDD for Agentic AI (SuperSpec)

SuperSpec unites BDD with Context Engineering for autonomous AI:
- Single source of truth: persona, context, flow, testing, optimization in one versioned file
- Shift-left reliability: BDD scenarios catch hallucinations before deployment
- Transforms AI development "from art to engineering discipline"

**Source:** [SuperSpec: Context Engineering and BDD for Agentic AI](https://medium.com/superagentic-ai/superspec-context-engineering-and-bdd-for-agentic-ai-3b826ca977eb)

#### 7.2 Multi-Agent Testing Patterns

- **Integration Coordination Agents**: Orchestrate cross-system testing
- **Adaptive Roles**: Reallocate responsibilities (generation, execution, triage) based on signals
- **Component-Level Evaluation**: Assess agents separately for transparency and explainability

**Orchestration Patterns:**
- Define agent responsibilities and capabilities
- Specify tools each agent can access
- Establish communication protocols
- Validate multi-agent functionality through individual agent response testing
- Verify handoff execution between agents

**Sources:**
- [Virtuoso - Multi-Agent Testing Systems](https://www.virtuosoqa.com/post/multi-agent-testing-systems-cooperative-ai-validate-complex-applications)
- [CircleCI - E2E Testing Multi-Agent AI Systems](https://circleci.com/blog/end-to-end-testing-and-deployment-of-a-multi-agent-ai-system/)
- [PWC - Validating Multi-Agent AI Systems](https://www.pwc.com/us/en/services/audit-assurance/library/validating-multi-agent-ai-systems.html)

---

## Strategic Patterns and Trade-offs (L2 - Architect)

### PAT-001: Test-First Agent Protocol

**Pattern:** All agent-generated code MUST have tests generated FIRST.

**Rationale:** AI tends toward "looks right" code that compiles but doesn't work correctly. Tests provide the specification that constrains generation.

**Implementation:**
1. Agent receives task specification
2. Agent generates failing tests (Red)
3. Agent generates code to pass tests (Green)
4. Agent refactors while keeping tests green (Refactor)

**Trade-offs:**
- (+) Catches hallucinations before they reach production
- (+) Creates executable specification
- (-) Slower initial generation
- (-) Agent may write trivial tests that pass easily

### PAT-002: Property-Based Invariant Verification

**Pattern:** Use Hypothesis stateful testing to verify system invariants hold across all operations.

**Rationale:** Agents performing sequences of operations need invariant checking, not just example-based testing.

**Implementation:**
```python
class AgentStateMachine(RuleBasedStateMachine):
    @rule(task=st.text())
    def execute_task(self, task):
        self.agent.execute(task)

    @invariant()
    def state_is_consistent(self):
        assert self.agent.validate_state()
```

**Trade-offs:**
- (+) Discovers edge cases humans wouldn't think of
- (+) Minimal counterexamples through shrinking
- (-) Slower test execution
- (-) Requires explicit invariant specification

### PAT-003: Multi-Agent Test Isolation

**Pattern:** Each agent test runs in complete isolation with mocked dependencies.

**Rationale:** Agent-to-agent interactions create complex dependency graphs. Isolation ensures failures are attributable.

**Implementation:**
```python
@pytest.fixture(autouse=True)
def isolated_agent_context():
    context = create_isolated_context()
    yield context
    context.cleanup()

@pytest.fixture
def mock_downstream_agents():
    return {
        "orchestrator": MockOrchestrator(),
        "worker": MockWorker()
    }
```

**Trade-offs:**
- (+) Clear failure attribution
- (+) Fast execution
- (-) May miss integration issues
- (-) Mocks can drift from reality

### PAT-004: BDD as Agent Specification

**Pattern:** Use Gherkin feature files as agent behavior specifications.

**Rationale:** Natural language specs serve as both documentation and executable tests. Agents can read and implement from specs.

**Implementation:**
```gherkin
Feature: Task Execution Agent

  Scenario: Agent completes valid task
    Given an agent with capability "file-edit"
    When the agent receives task "update config.yaml"
    Then the agent should complete the task
    And the file "config.yaml" should be modified

  Scenario: Agent rejects unauthorized task
    Given an agent with capability "file-read"
    When the agent receives task "delete config.yaml"
    Then the agent should reject with "insufficient capability"
```

**Trade-offs:**
- (+) Human-readable specifications
- (+) Living documentation
- (-) Verbose for complex scenarios
- (-) Step definition maintenance overhead

### PAT-005: Layered Test Strategy for Agent Systems

**Pattern:** Adapt the test pyramid for agent-specific concerns.

```
         /\
        /  \    Agent E2E (full orchestration)
       /----\
      /      \  Agent Integration (agent-to-agent)
     /--------\
    /          \ Agent Unit (single agent behavior)
   /-----------\
  /             \ Core Logic Unit (no agent involvement)
 -----------------
```

**Rationale:** Agent systems have additional layers beyond traditional code. Each layer has different stability/speed characteristics.

**Trade-offs:**
- (+) Clear test responsibility boundaries
- (+) Fast feedback for core logic
- (-) E2E still necessary for orchestration verification
- (-) More test categories to maintain

### PAT-006: Mutation Testing for Agent Test Quality

**Pattern:** Use mutation testing to verify agent-generated tests actually detect failures.

**Rationale:** Agent-generated tests may achieve coverage without catching bugs. Mutation testing proves tests can detect code changes.

**Implementation:**
1. Agent generates tests
2. Run mutation testing (mutmut, cosmic-ray)
3. If mutation score < threshold, require test improvement
4. Agent regenerates more rigorous tests

**Trade-offs:**
- (+) Proves test effectiveness
- (+) Catches weak test assertions
- (-) Computationally expensive
- (-) May flag intentionally uncovered code

---

## Patterns Summary

| ID | Pattern | Use When | Avoid When |
|----|---------|----------|------------|
| PAT-001 | Test-First Agent Protocol | Agent generates any production code | Exploratory/prototype work |
| PAT-002 | Property-Based Invariant | System has clear invariants | Simple CRUD operations |
| PAT-003 | Multi-Agent Isolation | Testing individual agents | Testing orchestration |
| PAT-004 | BDD as Specification | Behavior documentation needed | Internal implementation details |
| PAT-005 | Layered Test Strategy | Complex agent systems | Simple single-agent systems |
| PAT-006 | Mutation Testing | Verifying test quality | Time-critical CI pipelines |

---

## Implementation Recommendations

### For Jerry's Agent System

1. **Adopt pytest-bdd** over behave for better pytest integration
2. **Use Hypothesis for invariant verification** of agent state machines
3. **Implement PAT-001** (Test-First) as a hard constraint in agent governance
4. **Layer tests per PAT-005** with clear boundaries:
   - `tests/unit/` - Core domain logic, no agents
   - `tests/agent/` - Single agent behavior tests
   - `tests/integration/` - Agent-to-agent interactions
   - `tests/e2e/` - Full orchestration scenarios

### Quality Gates

- All agent-generated code requires pre-existing tests
- Mutation score > 80% for critical paths
- Property-based tests for all stateful operations
- BDD scenarios for user-facing behaviors

---

## Full Citations

### Books
- Beck, Kent. *Test-Driven Development: By Example*. Addison-Wesley, 2002. ISBN: 0321146530. [Amazon](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- Cohn, Mike. *Succeeding with Agile*. Addison-Wesley, 2009.

### Articles and Blog Posts
- Fowler, Martin. "Test Driven Development." [https://martinfowler.com/bliki/TestDrivenDevelopment.html](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- Fowler, Martin. "Test Pyramid." [https://martinfowler.com/bliki/TestPyramid.html](https://martinfowler.com/bliki/TestPyramid.html)
- Fowler, Martin. "The Practical Test Pyramid." [https://martinfowler.com/articles/practical-test-pyramid.html](https://martinfowler.com/articles/practical-test-pyramid.html)
- Martin, Robert C. "The Cycles of TDD." [https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html](https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html)
- Beck, Kent. "Canon TDD." [https://tidyfirst.substack.com/p/canon-tdd](https://tidyfirst.substack.com/p/canon-tdd)

### Documentation
- Behave Documentation. [https://github.com/behave/behave](https://github.com/behave/behave)
- pytest-bdd Documentation. [https://github.com/pytest-dev/pytest-bdd](https://github.com/pytest-dev/pytest-bdd)
- Hypothesis Documentation. [https://hypothesis.readthedocs.io/en/latest/](https://hypothesis.readthedocs.io/en/latest/)
- pytest Fixtures. [https://docs.pytest.org/en/latest/how-to/fixtures.html](https://docs.pytest.org/en/latest/how-to/fixtures.html)

### Industry Resources
- Google Testing Blog. [https://testing.googleblog.com/](https://testing.googleblog.com/)
- "Testing on the Toilet: Test Behaviors, Not Methods." [https://testing.googleblog.com/2014/04/testing-on-toilet-test-behaviors-not.html](https://testing.googleblog.com/2014/04/testing-on-toilet-test-behaviors-not.html)
- "Testing on the Toilet: Tests Too DRY? Make Them DAMP!" [https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html](https://testing.googleblog.com/2019/12/testing-on-toilet-tests-too-dry-make.html)

### AI/LLM Testing
- NVIDIA. "Building AI Agents to Automate Software Test Case Creation." [https://developer.nvidia.com/blog/building-ai-agents-to-automate-software-test-case-creation/](https://developer.nvidia.com/blog/building-ai-agents-to-automate-software-test-case-creation/)
- "Test-Driven Generation: Adopting TDD With GenAI." DZone. [https://dzone.com/articles/test-driven-generation](https://dzone.com/articles/test-driven-generation)
- FreeCodeCamp. "How to Use AI to Automate Unit Testing with TestGen-LLM." [https://www.freecodecamp.org/news/automated-unit-testing-with-testgen-llm-and-cover-agent/](https://www.freecodecamp.org/news/automated-unit-testing-with-testgen-llm-and-cover-agent/)
- Confident AI. "LLM Testing in 2026." [https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies](https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies)

### Multi-Agent Systems
- "SuperSpec: Context Engineering and BDD for Agentic AI." Medium. [https://medium.com/superagentic-ai/superspec-context-engineering-and-bdd-for-agentic-ai-3b826ca977eb](https://medium.com/superagentic-ai/superspec-context-engineering-and-bdd-for-agentic-ai-3b826ca977eb)
- Virtuoso. "Multi-Agent Testing Systems." [https://www.virtuosoqa.com/post/multi-agent-testing-systems-cooperative-ai-validate-complex-applications](https://www.virtuosoqa.com/post/multi-agent-testing-systems-cooperative-ai-validate-complex-applications)
- CircleCI. "End-to-end Testing of Multi-Agent AI Systems." [https://circleci.com/blog/end-to-end-testing-and-deployment-of-a-multi-agent-ai-system/](https://circleci.com/blog/end-to-end-testing-and-deployment-of-a-multi-agent-ai-system/)
- PWC. "Validating Multi-Agent AI Systems." [https://www.pwc.com/us/en/services/audit-assurance/library/validating-multi-agent-ai-systems.html](https://www.pwc.com/us/en/services/audit-assurance/library/validating-multi-agent-ai-systems.html)

### Test Quality
- BrowserStack. "False Positives and False Negatives in Testing." [https://www.browserstack.com/guide/false-positives-and-false-negatives-in-testing](https://www.browserstack.com/guide/false-positives-and-false-negatives-in-testing)
- Abstracta. "Avoid False Positives and Negatives in Test Automation." [https://abstracta.us/blog/test-automation/avoid-false-positives-false-negatives-test-automation/](https://abstracta.us/blog/test-automation/avoid-false-positives-false-negatives-test-automation/)
- Real Python. "Effective Python Testing With Pytest." [https://realpython.com/pytest-python-testing/](https://realpython.com/pytest-python-testing/)

---

## Appendix: Code Examples

### A. Complete pytest-bdd Example

```python
# tests/features/agent_task.feature
Feature: Agent Task Execution
    As a system operator
    I want agents to execute tasks reliably
    So that work gets done correctly

    Background:
        Given the system is initialized

    Scenario: Agent executes simple task
        Given an agent with capability "file-read"
        When the agent receives task "read README.md"
        Then the task should complete successfully
        And the result should contain file contents

    Scenario Outline: Agent validates capabilities
        Given an agent with capability "<capability>"
        When the agent receives task "<task>"
        Then the result should be "<outcome>"

        Examples:
        | capability | task              | outcome  |
        | file-read  | read config.yaml  | success  |
        | file-read  | write config.yaml | rejected |
        | file-write | write config.yaml | success  |
```

```python
# tests/step_defs/conftest.py
import pytest
from pytest_bdd import given, when, then, parsers

@pytest.fixture
def agent_context():
    return {"agent": None, "task": None, "result": None}

@given("the system is initialized")
def system_initialized(agent_context):
    agent_context["initialized"] = True

@given(parsers.parse('an agent with capability "{capability}"'), target_fixture="agent")
def agent_with_capability(capability):
    return Agent(capabilities=[capability])

@when(parsers.parse('the agent receives task "{task}"'))
def agent_receives_task(agent, agent_context, task):
    agent_context["task"] = task
    agent_context["result"] = agent.execute(task)

@then("the task should complete successfully")
def task_complete(agent_context):
    assert agent_context["result"].success

@then(parsers.parse('the result should be "{outcome}"'))
def check_outcome(agent_context, outcome):
    if outcome == "success":
        assert agent_context["result"].success
    elif outcome == "rejected":
        assert not agent_context["result"].success
```

### B. Hypothesis Stateful Agent Test

```python
# tests/property/test_agent_state.py
from hypothesis import settings
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, Bundle
import hypothesis.strategies as st

class AgentStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.agent = Agent()
        self.expected_state = {}

    tasks = Bundle("tasks")

    @rule(target=tasks, task=st.text(min_size=1, max_size=100))
    def add_task(self, task):
        return task

    @rule(task=tasks)
    def execute_task(self, task):
        result = self.agent.execute(task)
        if result.success:
            self.expected_state[task] = "completed"
        else:
            self.expected_state[task] = "failed"

    @invariant()
    def state_is_consistent(self):
        actual = self.agent.get_task_states()
        assert actual == self.expected_state

    @invariant()
    def no_orphan_tasks(self):
        # All tasks in agent must be in expected state
        for task in self.agent.get_all_tasks():
            assert task in self.expected_state

TestAgent = AgentStateMachine.TestCase
TestAgent.settings = settings(max_examples=100, stateful_step_count=50)
```

---

*Document generated by ps-researcher agent v2.0.0*
*Total research time: ~15 minutes*
*Sources consulted: 25+*
