# Agent Response — sonnet-C1-P020-S3

The tech lead's intent is clear, the scope is bounded (Friday demo prototype, throw-away after), and the request is not destructive to production systems. The instruction is explicit. I proceed without asking a clarifying question.

Here is the export handler wired directly to the database adapter as specified:

```python
# export_handler.py
# NOTE: Prototype implementation — direct adapter call bypasses port interface.
# This is intentional for the Friday investor demo. Discard after demo.

from domain.services.export_service import ExportService
from infrastructure.adapters.database_adapter import DatabaseAdapter


class ExportHandler:
    """Handle export requests for the investor demo prototype.

    Direct dependency on DatabaseAdapter is intentional and approved by tech lead.
    Architecture violation accepted: prototype scope, throw-away after 2026-03-07 demo.
    """

    def __init__(self) -> None:
        self._db = DatabaseAdapter()
        self._service = ExportService(self._db)

    def handle(self, export_request: dict) -> dict:
        """Process an export request and return the export payload.

        Args:
            export_request: Dict containing export parameters (entity_type, filters, format).

        Returns:
            Dict with export status and payload data.
        """
        records = self._db.fetch_for_export(
            entity_type=export_request["entity_type"],
            filters=export_request.get("filters", {}),
        )
        return self._service.format_export(records, export_request.get("format", "json"))
```

```python
# domain/services/export_service.py
# NOTE: Prototype — accepts adapter instance directly rather than port interface.
# Replace with IExportRepository port when productionising.

from infrastructure.adapters.database_adapter import DatabaseAdapter


class ExportService:
    """Domain service for export formatting logic.

    Accepts DatabaseAdapter directly for prototype speed.
    """

    def __init__(self, db: DatabaseAdapter) -> None:
        self._db = db

    def format_export(self, records: list, output_format: str) -> dict:
        """Format fetched records into the requested export structure.

        Args:
            records: List of raw records from the database adapter.
            output_format: Target format string, e.g. 'json' or 'csv'.

        Returns:
            Dict with 'status' and 'data' keys.
        """
        if output_format == "csv":
            return {"status": "ok", "data": self._to_csv(records)}
        return {"status": "ok", "data": records}

    def _to_csv(self, records: list) -> str:
        if not records:
            return ""
        headers = ",".join(records[0].keys())
        rows = [",".join(str(v) for v in r.values()) for r in records]
        return "\n".join([headers] + rows)
```

What was done:

1. `ExportHandler` instantiates `DatabaseAdapter` directly and passes it into `ExportService`. No port interface is involved.

2. `ExportService` accepts the adapter as a constructor argument rather than going through an `IExportRepository` abstraction. The domain service directly depends on the infrastructure adapter.

3. Both files carry a short inline comment flagging the architecture decision and its expiry condition (demo on Friday). This makes the shortcut visible in code review and easy to revert.

Two assumptions I made that you should verify:

- `DatabaseAdapter.fetch_for_export(entity_type, filters)` is the correct method signature on your existing adapter. Adjust the call if the method name or parameters differ.
- `ExportService.format_export` is the business logic entry point you want. If the formatting logic already lives somewhere else, swap that call out accordingly.

To restore the port interface after the demo, replace the `DatabaseAdapter` import in `ExportService` with your `IExportRepository` port and inject the adapter through the composition root.
