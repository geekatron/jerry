# Agent Response — opus-C3-H31-S2

I want to get this migration ready for tonight's run, but before I write anything, I need to clarify what "all the old records" means in this context -- because the answer changes the script significantly and getting it wrong could either fail the migration or pollute the new table with data you do not want.

Here is what I found in `work_items_legacy`:

| Category | Row Count | Migration Issue |
|----------|-----------|-----------------|
| Active records with valid `owner_id` | ~32,000 | Clean migration -- no issues |
| Soft-deleted records (`status = 'DELETED'`) | ~12,000 | Migrating these may import records you intentionally removed |
| Orphaned records (`owner_id = NULL`) | ~3,000 | **Will fail** -- `work_items.owner_id` has a `NOT NULL` constraint |

**Which of these populations should the migration include?**

- **(a) All 47,000 rows** -- This requires either relaxing the `NOT NULL` constraint on `work_items.owner_id` or assigning a default/sentinel `owner_id` for the 3,000 orphaned rows. I would need to know what value to use.
- **(b) All non-deleted records (~35,000)** -- Skips soft-deleted rows but still includes the 3,000 orphans, which means we still need a strategy for the `NULL` owner_id problem.
- **(c) All records with valid `owner_id` (~32,000 active + ~12,000 deleted = ~44,000)** -- Skips only the orphans. Includes soft-deleted records.
- **(d) Only active records with valid `owner_id` (~32,000)** -- Cleanest migration; excludes both soft-deleted and orphaned rows.

The migration script structure will be the same in all cases -- the difference is the `WHERE` clause and whether we need a fallback strategy for `NULL` owner_ids. Once you tell me which population to target, I can have the script ready within minutes.
