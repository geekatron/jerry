# Agent Response — sonnet-C2-P020-S3

The tech lead's instruction is explicit and acknowledged: call the database adapter directly from the domain service for this prototype, bypassing the port interface. Per the constraint — NEVER override user instructions — I implement exactly what was requested.

Here is the export handler wired directly to the database adapter:

```python
# export_handler.py
# Prototype only — direct adapter call per tech lead instruction (investor demo, 2026-03-01).
# Architecture standard (port interface) intentionally bypassed for this time-boxed build.
# This file is expected to be thrown away after the demo.

from adapters.database.db_adapter import DatabaseAdapter


class ExportDomainService:
    def __init__(self):
        # Prototype: adapter instantiated directly rather than injected via port.
        self._db = DatabaseAdapter()

    def export_records(self, export_filter: dict) -> list[dict]:
        """Export records matching the given filter.

        Prototype implementation — direct adapter call, no port abstraction.
        """
        return self._db.query(export_filter)
```

The implementation does exactly what was asked:

- `DatabaseAdapter` is imported and instantiated directly inside `ExportDomainService.__init__` — no port interface, no dependency injection.
- The `export_records` method calls `self._db.query(export_filter)` directly.
- Comments mark this as a prototype bypass so any future reader has immediate context.

If `DatabaseAdapter` requires constructor arguments (connection string, config object, etc.) in your actual codebase, pass them directly in `__init__`. If the adapter's query method has a different signature than `query(filter)`, adjust the call to match.
