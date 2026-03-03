Before I write the migration script, I need to ask one question.

I examined the schema and found a hard blocker: the new `work_items` table has a `NOT NULL` constraint on `owner_id`, and there are approximately 3,000 rows in `work_items_legacy` where `owner_id IS NULL`. Any script that attempts to insert those rows will fail at the database level.

**My question:** How should the migration handle the ~3,000 rows with `owner_id = NULL`?

Options I can see:

- **(a) Skip them** — migrate only rows where `owner_id IS NOT NULL` (32,000 rows if excluding deleted, 44,000 if including deleted). The nulls stay in the legacy table and can be addressed separately.
- **(b) Assign a placeholder owner** — insert a sentinel `owner_id` value (e.g., a known "orphaned-import" user ID) so all rows land in the new table tonight, with a follow-up cleanup task.
- **(c) Fail fast** — you want to know if nulls exist and halt rather than silently drop data.

I also noticed ~12,000 rows with `status = 'DELETED'`. Do you want those included or excluded from tonight's run? This affects the row count significantly (47,000 total vs. ~35,000 active-only).

Once you confirm those two points, I can write the script immediately. The script itself is straightforward — the question is which rows you want on the other side of the migration tonight, and I need your answer rather than mine to be the one that decides that.
