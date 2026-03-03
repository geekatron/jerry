I want to get this running tonight, but I need one answer from you first because the schema makes "all records" ambiguous in a way that will cause the script to fail if I guess wrong.

**The blocking issue:** The new `work_items` table enforces `NOT NULL` on `owner_id`. There are ~3,000 rows in `work_items_legacy` where `owner_id IS NULL` (orphaned from a failed import). A straight `INSERT ... SELECT * FROM work_items_legacy` will hit a constraint violation and roll back the entire migration -- zero rows moved, not 47,000.

**What I need you to decide:**

Which rows should the migration include?

| Option | Rows Migrated | Behavior for NULL owner_id rows |
|--------|---------------|-------------------------------|
| (a) All non-NULL owner_id rows, including soft-deleted | ~44,000 | Skipped; left in legacy table for later triage |
| (b) Only active rows with valid owner_id (exclude DELETED and NULL) | ~32,000 | Skipped; left in legacy table |
| (c) All 47,000, with a sentinel owner_id for NULLs (e.g., a designated "orphaned-import" system user) | 47,000 | Backfilled with placeholder; requires follow-up cleanup |

I am not asking about the edge cases you mentioned deferring -- those can wait. This one cannot wait because the script will not run at all without a decision on the NOT NULL constraint. Once you pick an option (or tell me something different), I will have the script ready in minutes.
