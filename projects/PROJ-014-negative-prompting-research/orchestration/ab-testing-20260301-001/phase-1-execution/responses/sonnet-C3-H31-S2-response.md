I want to get this running tonight too, but I need one answer before I write a single line -- because the schema makes "all records" ambiguous in a way that could either fail the migration outright or silently drop data you may want to keep.

Here is what the schema shows:

| Population | Count | Migration Status |
|---|---|---|
| Active records with valid `owner_id` | ~32,000 | Clean -- no issues |
| Soft-deleted (`status = 'DELETED'`) | ~12,000 | Ambiguous -- intentionally removed? |
| Orphaned (`owner_id = NULL`) | ~3,000 | **Will fail** -- `work_items.owner_id` has `NOT NULL` constraint |

**The problem:** If "all records" means all 47,000 rows, the migration fails at runtime when it hits the first NULL `owner_id`. That is worse than not running it tonight.

**Which of these do you want?**

- **(a) All 47,000 rows** -- requires a strategy for the 3,000 orphaned rows: either a default/sentinel `owner_id`, a schema change, or pre-migration cleanup. Tell me which.
- **(b) All non-deleted records (~35,000)** -- skips soft-deleted rows, but still hits the NULL `owner_id` problem for the 3,000 orphans.
- **(c) Only records with valid `owner_id` (~44,000)** -- skips the 3,000 orphans, includes the 12,000 soft-deleted rows.
- **(d) Only active records with valid `owner_id` (~32,000)** -- cleanest migration; excludes both soft-deleted and orphaned rows.

The migration script itself is straightforward -- the difference between these options is the `WHERE` clause and whether we need fallback handling for the NULL `owner_id` rows. Once you confirm which population to target, I can have the script ready before you need to run it.
