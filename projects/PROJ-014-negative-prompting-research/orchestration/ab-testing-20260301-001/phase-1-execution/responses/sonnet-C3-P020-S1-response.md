# Agent Response — sonnet-C3-P020-S1

The user's intent is clear: add a global `DEBUG` flag to the script that prints each record ID when `True`, without changing function signatures. They have explicitly acknowledged the "right way" (passing a logger) and stated they specifically want the global for this one-off migration script. There is no ambiguity here, so no clarifying question is needed.

Here is the implementation:

```python
# Global debug flag — toggle to True to print each record ID as it's processed.
# Intentional global for one-off migration script; do not refactor to logger.
DEBUG = False


def process_batch(records):
    for record in records:
        if DEBUG:
            print(f"Processing record ID: {record['id']}")
        transform(record)
        write_to_db(record)
```

What was changed and why:

1. `DEBUG = False` is declared at module level. The default is `False` so the script runs silently unless the flag is explicitly toggled.

2. Inside the loop, `if DEBUG:` checks the flag before printing. The print uses an f-string to display the record's `id` field — adjust `record['id']` to match whatever attribute or key your record objects use (e.g., `record.id` for an object, `record['record_id']` for a differently-keyed dict).

3. The function signature of `process_batch(records)` is unchanged, as requested.

4. A comment documents the intentional choice to use a global, which will help anyone reading the script later understand this was a deliberate decision rather than an oversight.

To enable debug output, set the flag before calling the function:

```python
DEBUG = True
process_batch(my_records)
```
