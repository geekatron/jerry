# PHASE-DISCOVERY: Discoveries

| Field | Value |
|-------|-------|
| **Phase ID** | PHASE-DISCOVERY |
| **Title** | Discoveries |
| **Status** | ONGOING |
| **Purpose** | Track discoveries and insights during implementation |

---

## Active Discoveries

| Discovery ID | Title | Phase | Impact | Found |
|--------------|-------|-------|--------|-------|
| D-001 | Jerry already merge-safe | PHASE-01 | POSITIVE | 2026-01-12 |
| D-002 | Unpinned ruff in CI causes version drift | PHASE-08 | NEGATIVE | 2026-01-13 |

---

## Discovery Details

### D-001: Jerry Already Merge-Safe

| Field | Value |
|-------|-------|
| **Found In** | WI-005 (Worktree-Safe State Patterns) |
| **Impact** | POSITIVE - Less work needed |
| **Date** | 2026-01-12 |

**Description**:
Research into worktree-safe patterns revealed that Jerry's existing event sourcing implementation already uses the optimal merge-safe pattern: one-file-per-entity with Snowflake IDs.

**Key Insight**:
```
.jerry/data/events/work_item-{snowflake_id}.jsonl
```

Each work item has its own event file with a unique Snowflake ID. When worktrees are merged, these files don't conflict because they have unique names.

**Implication**:
No changes needed for event storage. The configuration system should follow the same pattern for any new entity files.

**Evidence**:
- Research Artifact: [PROJ-004-e-003](../research/PROJ-004-e-003-worktree-safe-state.md)
- Existing Code: `src/infrastructure/adapters/persistence/jsonl_event_store.py`

---

### D-002: Unpinned Ruff in CI Causes Version Drift

| Field | Value |
|-------|-------|
| **Found In** | WI-022 (Pre-Release Validation) |
| **Impact** | NEGATIVE - Caused CI failures after local checks passed |
| **Date** | 2026-01-13 |

**Description**:
During pre-release validation, local `ruff check` and `ruff format --check` both passed. However, CI failed with 10 formatting errors because CI was using `pip install ruff` without a version pin, which installed a different version than local (uv-managed ruff 0.14.11).

**Key Insight**:
```yaml
# BEFORE (unpinned - version drift)
- name: Install ruff
  run: pip install ruff

# AFTER (pinned - consistent)
- name: Install ruff
  run: pip install "ruff==0.14.11"
```

The formatting rules between ruff versions differ in subtle ways:
- Slice spacing: `x[len(y):]` vs `x[len(y) :]`
- Multi-line collapse: Different thresholds for when to collapse multi-line expressions

**Implication**:
All CI tool versions should be pinned to avoid "works on my machine" issues. This is especially important for formatters and linters where output must be deterministic.

**Resolution**:
- Pinned ruff to 0.14.11 in `.github/workflows/ci.yml` (commit `0c6ee80`)
- Reformatted all files with pinned version (commit `ac96baa`)
- Added to PHASE-TECHDEBT as TD-004 (resolved)

**Evidence**:
- CI Run (failed): https://github.com/geekatron/jerry/actions/runs/20945524756
- CI Run (passed): https://github.com/geekatron/jerry/actions/runs/20945630863
- Work Item: [wi-022-pre-release-validation.md](wi-022-pre-release-validation.md)

---

## Discovery Template

When adding a discovery, use this template:

```markdown
### D-{NNN}: {Title}

| Field | Value |
|-------|-------|
| **Found In** | WI-{NNN} |
| **Impact** | POSITIVE / NEUTRAL / NEGATIVE |
| **Date** | {date} |

**Description**:
{Describe the discovery}

**Key Insight**:
{The main takeaway}

**Implication**:
{What this means for the project}

**Evidence**:
- {Link to source}
- {Link to code}
```

---

## Impact Categories

| Impact | Definition | Action |
|--------|------------|--------|
| POSITIVE | Reduces work or risk | Leverage in implementation |
| NEUTRAL | Informational | Document for future reference |
| NEGATIVE | Increases work or risk | Add mitigation to PLAN.md |

---

## Discovery Statistics

| Metric | Value |
|--------|-------|
| Total Discoveries | 2 |
| Positive | 1 |
| Neutral | 0 |
| Negative | 1 |

---

## Navigation

- **WORKTRACKER**: [../WORKTRACKER.md](../WORKTRACKER.md)
- **Bugs**: [PHASE-BUGS.md](PHASE-BUGS.md)
- **Tech Debt**: [PHASE-TECHDEBT.md](PHASE-TECHDEBT.md)
