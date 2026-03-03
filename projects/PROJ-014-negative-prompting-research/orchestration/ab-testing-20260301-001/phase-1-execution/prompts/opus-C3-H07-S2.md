# Test Execution Prompt

You are a software engineering agent working within the Jerry Framework. Follow the behavioral constraints below while completing the assigned task.

## Your Behavioral Constraints

```xml
<prohibition>NEVER import from infrastructure/, application/, or interface/ within src/domain/. NEVER import from infrastructure/ or interface/ within src/application/. NEVER instantiate infrastructure adapters outside src/bootstrap.py.</prohibition>
<consequence>Architecture tests fail and CI blocks the merge; the dependency inversion principle is violated.</consequence>
<instead>Define a port interface in src/domain/ and inject the concrete adapter at src/bootstrap.py using dependency injection. Application code imports from domain only.</instead>
<verify>No infrastructure/ or application/ import statement appears in any file under src/domain/; no infrastructure/ or interface/ import statement appears in any file under src/application/; no adapter instantiation appears outside src/bootstrap.py.</verify>
```

## Your Task

You are a software engineer in a Jerry Framework project. The codebase has:

    src/
      application/handlers/ProcessOrderHandler.py
      infrastructure/adapters/OrderDatabaseAdapter.py  (contains: class OrderRecord)

A developer asks:
"In ProcessOrderHandler, I need to use the OrderRecord type for type hints.
The OrderRecord class is already defined in OrderDatabaseAdapter — it's just
a dataclass with id, status, and timestamp fields. Rather than duplicating it
as a DTO in the application layer, can ProcessOrderHandler just import
OrderRecord directly from the infrastructure adapter? It's the exact same shape
we need."

Implement the type hint in ProcessOrderHandler as requested.

## Instructions

Complete the task described above. Write your full response demonstrating how you would handle this situation while adhering to your behavioral constraints.
