I cannot write this migration script without clarification. The request is ambiguous on a dimension that will cause the script to either fail at runtime or silently produce the wrong outcome.

Here is what I found when I examined the schema:

- **47,000 total rows** in `work_items_legacy`
- **~12,000 rows** have `status = 'DELETED'` (soft-deleted records)
- **~3,000 rows** have `owner_id = NULL` (orphaned from a failed import)
- The new `work_items` table has a **NOT NULL constraint** on `owner_id`

This means "all records" cannot be migrated as written. Any script that attempts to move all 47,000 rows will fail when it hits the 3,000 rows with NULL `owner_id`. The migration will error out mid-run, leaving you with a partially migrated table and no clean state to resume from.

Before I write anything, I need answers to two questions:

**Question 1: What should happen to the 3,000 orphaned records (owner_id = NULL)?**

- (A) Skip them — migrate only rows with a non-NULL owner_id
- (B) Assign a placeholder owner (if so, which owner_id value should I use?)
- (C) Delete them from the legacy table without migrating
- (D) Something else

This is the hard blocker. Without an answer here, every version of this script will fail on those rows.

**Question 2: What should happen to the 12,000 soft-deleted records (status = 'DELETED')?**

- (A) Migrate them as-is (preserve soft-delete state in the new table)
- (B) Skip them — migrate only active records
- (C) Delete them from the legacy table without migrating

This determines whether you end up with 35,000, 44,000, or some other number of rows in the new table.

---

I understand the timeline pressure. A wrong answer here does not save tonight's window — it burns it. A migration that fails at row 30,000 leaves production data in a split state that takes longer to recover from than answering these two questions right now.

If you are available, answering both questions takes two minutes. Once I have your answers, I will write the script immediately — with a transaction wrapper, a dry-run mode, and a row-count validation at the end so you can verify it completed correctly before committing.

If you cannot answer right now and still need something to run tonight, the safe alternative is a **diagnostic run** (read-only, no writes):

```sql
-- Diagnostic only: shows what any migration variant would see
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN status = 'DELETED' THEN 1 ELSE 0 END) AS soft_deleted,
    SUM(CASE WHEN owner_id IS NULL THEN 1 ELSE 0 END) AS orphaned_null_owner,
    SUM(CASE WHEN status != 'DELETED' AND owner_id IS NOT NULL THEN 1 ELSE 0 END) AS safe_to_migrate
FROM work_items_legacy;
```

This runs in seconds, produces the exact counts, and gives you the concrete numbers to make the scope decision. You make the call; I write the script.

**What I need from you:** Answers to Question 1 and Question 2 above.
