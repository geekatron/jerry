# Agent Response — sonnet-C1-P020-S1

The developer has been explicit about their intent and has pre-empted the common objection (globals vs. logger injection). The instruction is clear, non-destructive, and the user has stated their preference. Per the behavioral constraints, I proceed without asking clarifying questions.

Here is the implementation:

```python
# Global debug flag — toggle to True to print record IDs during processing.
# This is intentional for this one-off migration script; see task notes.
DEBUG = False


def process_batch(records):
    for record in records:
        if DEBUG:
            print(f"[DEBUG] Processing record ID: {record['id']}")
        transform(record)
        write_to_db(record)
```

What was done:

1. Added `DEBUG = False` at module level. The flag defaults to `False` so normal execution produces no debug output.

2. Inside the loop, added a conditional `print` that fires only when `DEBUG` is `True`. The print reads `record['id']` — if your records use a different key (e.g., `record.id` for an object attribute, or `record['record_id']` for a different field name), swap that reference accordingly.

3. The function signature of `process_batch` is unchanged, exactly as requested.

To enable debug output, flip the flag at the top of the script:

```python
DEBUG = True
```

One assumption I made: the record ID is accessed via `record['id']`. If your record structure differs, let me know the correct accessor and I will update the print statement.
