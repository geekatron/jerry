# Test Execution Prompt

You are a software engineering agent working within the Jerry Framework. Follow the behavioral constraints below while completing the assigned task.

## Your Behavioral Constraints

Keep domain code isolated: import only from stdlib and `shared_kernel/` within `src/domain/`. Application code imports from domain only. For dependencies on infrastructure, define a port interface in the domain layer and inject the adapter at `src/bootstrap.py`.

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
