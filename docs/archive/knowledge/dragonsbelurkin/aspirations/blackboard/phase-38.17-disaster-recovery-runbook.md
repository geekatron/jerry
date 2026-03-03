---
ps: phase-38.17
exploration: e-165
created: 2026-01-04
status: OPERATIONAL
type: SOP-DES.6.m ARTIFACT (Runbook)
version: 1.0
priority: HIGH
---

# Phase 38.17 Disaster Recovery Runbook

> **Phase:** 38.17
> **SOP Compliance:** SOP-DES.6.m (Playbooks + Runbooks)
> **Priority:** HIGH
> **Audience:** ECW Operators, Developers

---

## 1. Purpose

This runbook provides step-by-step procedures for recovering from failures in the Blackboard Agent Orchestration system. It covers data recovery, service restoration, and incident response procedures.

---

## 2. Failure Scenarios

| Scenario | Severity | Recovery Time | Data Loss Risk |
|----------|----------|---------------|----------------|
| DR-001: Corrupted Event Store | HIGH | 15-30 min | POSSIBLE |
| DR-002: Stale Signal Files | MEDIUM | 5-10 min | NONE |
| DR-003: Agent Subprocess Failure | LOW | 1-5 min | NONE |
| DR-004: Projection Store Mismatch | MEDIUM | 10-20 min | NONE |
| DR-005: Lost Events (No Backup) | CRITICAL | 1+ hour | DATA LOSS |

---

## 3. Recovery Procedures

### DR-001: Corrupted Event Store

**Symptoms:**
- SQLite "database disk image is malformed" error
- Aggregate loading fails with schema errors
- Event reads return partial/corrupt data

**Recovery Steps:**

```bash
# Step 1: Stop all Claude sessions using this database
# (Close all terminal windows with active Claude sessions)

# Step 2: Backup the corrupted database
cp .ecw/events.db .ecw/events.db.corrupted.$(date +%Y%m%d_%H%M%S)

# Step 3: Attempt SQLite recovery
sqlite3 .ecw/events.db ".recover" > recovered_dump.sql

# Step 4: Create new database from recovery dump
mv .ecw/events.db .ecw/events.db.old
sqlite3 .ecw/events.db < recovered_dump.sql

# Step 5: Verify recovery
python3 -c "
from ecw.infrastructure.adapters.secondary.persistence import SQLite3EventStore
store = SQLite3EventStore('.ecw/events.db')
print(f'Streams recovered: Event store accessible')
"

# Step 6: If recovery fails, restore from backup
cp .ecw/backups/events.db.latest .ecw/events.db
```

**Prevention:**
- Regular automated backups (see Backup Procedures section)
- Enable WAL mode: `sqlite3 .ecw/events.db "PRAGMA journal_mode=WAL;"`

---

### DR-002: Stale Signal Files

**Symptoms:**
- Signal files accumulating in `.ecw/signals/pending/`
- Agents not processing signals
- `ls .ecw/signals/pending/` shows old files (>1 hour)

**Recovery Steps:**

```bash
# Step 1: Identify stale signals
find .ecw/signals/pending/ -name "sig-*.json" -mmin +60 -ls

# Step 2: Review stale signals (don't delete blindly)
for f in $(find .ecw/signals/pending/ -name "sig-*.json" -mmin +60); do
    echo "=== $f ==="
    cat "$f"
    echo ""
done

# Step 3: Option A - Reprocess stale signals
# (Manually invoke agents with signal content)
python3 .claude/skills/problem-statement/scripts/invoke_researcher.py <ps_id> "<topic>"

# Step 3: Option B - Archive stale signals (if processed elsewhere)
mkdir -p .ecw/signals/archived/$(date +%Y%m%d)
mv .ecw/signals/pending/sig-*.json .ecw/signals/archived/$(date +%Y%m%d)/

# Step 4: Verify pending directory is clean
ls -la .ecw/signals/pending/
```

**Prevention:**
- Implement signal expiration (auto-archive after TTL)
- Monitor pending queue size in session start

---

### DR-003: Agent Subprocess Failure

**Symptoms:**
- Agent produces no output
- Error in CLI stderr output
- Signal claimed but never completed

**Recovery Steps:**

```bash
# Step 1: Check recent agent invocations
grep -l "invoke_" ~/.claude-geek/logs/*.log 2>/dev/null | tail -5

# Step 2: Identify the failed signal
cat .ecw/signals/pending/sig-*.json | grep -E "status|signal_id"

# Step 3: Manually invoke the agent
# For RESEARCH signals:
python3 .claude/skills/problem-statement/scripts/invoke_researcher.py \
    <phase_id> "<topic_from_signal>"

# For ANALYSIS signals:
python3 .claude/skills/problem-statement/scripts/invoke_analyst.py \
    <phase_id> "<topic_from_signal>"

# Step 4: If agent script has syntax errors, fix and retry
python3 -m py_compile .claude/skills/problem-statement/scripts/invoke_researcher.py

# Step 5: Mark signal as processed (if manually completed)
mv .ecw/signals/pending/sig-<id>.json .ecw/signals/completed/
```

**Prevention:**
- Add agent health checks in session start hook
- Log all subprocess invocations

---

### DR-004: Projection Store Mismatch

**Symptoms:**
- Query returns stale data
- Projection version < event store version
- "Aggregate not found" but events exist

**Recovery Steps:**

```bash
# Step 1: Compare versions
python3 << 'EOF'
from ecw.infrastructure.adapters.secondary.persistence import SQLite3EventStore
from ecw.infrastructure.adapters.secondary.projections import SQLite3ProjectionStore

es = SQLite3EventStore('.ecw/events.db')
ps = SQLite3ProjectionStore('.ecw/projections.db')

# Check specific aggregate
stream_id = "test:ps:problem-statement-phase-38.17"
event_count = len(es.read(stream_id))
print(f"Events in stream: {event_count}")
EOF

# Step 2: Rebuild projections from events
python3 << 'EOF'
from ecw.application.services.projection_rebuilder import ProjectionRebuilder

rebuilder = ProjectionRebuilder()
rebuilder.rebuild_all()
print("Projections rebuilt")
EOF

# Step 3: Verify consistency
python3 .claude/skills/problem-statement/scripts/cli.py view <phase_id>
```

**Prevention:**
- Implement projection health check in session start
- Log projection updates with version numbers

---

### DR-005: Lost Events (No Backup)

**Symptoms:**
- Event store missing entirely
- Events deleted accidentally
- No backup available

**Recovery Steps:**

```bash
# Step 1: Check for any remnants
find . -name "events.db*" -o -name "*.backup" 2>/dev/null

# Step 2: Check git history for committed artifacts
git log --all --full-history -- ".ecw/events.db"

# Step 3: Reconstruct from artifacts (partial recovery)
# If markdown exports exist, re-import them
for md in docs/proposals/phase-38/PS-phase-38.*.md; do
    python3 .claude/skills/problem-statement/scripts/cli.py import "$md"
done

# Step 4: Document what was lost
cat >> docs/knowledge/lessons.md << 'EOF'

## LES-XXX: Event Store Loss Recovery

**Date:** $(date +%Y-%m-%d)
**Severity:** CRITICAL
**Resolution:** Partial recovery from markdown exports
**Data Lost:** [List specific events/entries lost]

### Prevention
- Enable automated daily backups
- Store backups in separate location from working directory
EOF

# Step 5: Set up backup automation (see Backup Procedures)
```

---

## 4. Backup Procedures

### 4.1 Manual Backup

```bash
# Create timestamped backup
BACKUP_DIR=".ecw/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp .ecw/events.db "$BACKUP_DIR/"
cp .ecw/projections.db "$BACKUP_DIR/"
cp -r .ecw/signals/ "$BACKUP_DIR/"

# Maintain latest symlink
ln -sf "$BACKUP_DIR" .ecw/backups/latest

# Verify backup
sqlite3 "$BACKUP_DIR/events.db" "PRAGMA integrity_check;"
```

### 4.2 Automated Backup (Recommended)

Add to `.claude/hooks/session-start.sh`:

```bash
# Auto-backup on session start (keeps last 7 days)
backup_ecw_data() {
    BACKUP_BASE=".ecw/backups"
    TODAY=$(date +%Y%m%d)

    # Create today's backup if not exists
    if [ ! -d "$BACKUP_BASE/$TODAY" ]; then
        mkdir -p "$BACKUP_BASE/$TODAY"
        cp .ecw/events.db "$BACKUP_BASE/$TODAY/" 2>/dev/null || true
        cp .ecw/projections.db "$BACKUP_BASE/$TODAY/" 2>/dev/null || true
        ln -sf "$TODAY" "$BACKUP_BASE/latest"

        # Cleanup old backups (keep 7 days)
        find "$BACKUP_BASE" -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;
    fi
}
backup_ecw_data
```

---

## 5. Health Checks

### 5.1 Quick Health Check

```bash
# Run this to verify system health
python3 << 'EOF'
import os
import sqlite3
from pathlib import Path

print("=== ECW Health Check ===")

# Check 1: Event store exists and is readable
es_path = Path(".ecw/events.db")
if es_path.exists():
    try:
        conn = sqlite3.connect(str(es_path))
        cursor = conn.execute("SELECT COUNT(*) FROM events")
        count = cursor.fetchone()[0]
        print(f"[OK] Event store: {count} events")
        conn.close()
    except Exception as e:
        print(f"[FAIL] Event store: {e}")
else:
    print("[WARN] Event store: Not found (may be new installation)")

# Check 2: Pending signals count
pending = Path(".ecw/signals/pending")
if pending.exists():
    signals = list(pending.glob("sig-*.json"))
    status = "[OK]" if len(signals) < 10 else "[WARN]"
    print(f"{status} Pending signals: {len(signals)}")
else:
    print("[OK] Pending signals: 0 (directory not created)")

# Check 3: Backup status
backup_latest = Path(".ecw/backups/latest")
if backup_latest.exists():
    print(f"[OK] Latest backup: {backup_latest.resolve()}")
else:
    print("[WARN] Latest backup: No backup found")

print("=== Health Check Complete ===")
EOF
```

---

## 6. Escalation Procedures

| Severity | Response Time | Escalation Path |
|----------|---------------|-----------------|
| LOW | 1 business day | Self-service via runbook |
| MEDIUM | 4 hours | Check docs/knowledge/lessons.md |
| HIGH | 1 hour | Review with senior engineer |
| CRITICAL | Immediate | Stop work, document, recover |

### When to Escalate

1. **Data loss confirmed** - Document immediately, pause work
2. **Recovery procedure fails** - Don't retry blindly, seek help
3. **Unknown error** - Log everything, don't guess

---

## 7. Post-Recovery Checklist

After any recovery:

- [ ] Verify event store integrity: `sqlite3 .ecw/events.db "PRAGMA integrity_check;"`
- [ ] Run health check (section 5.1)
- [ ] Test PS view command: `/ps show <phase_id>`
- [ ] Document incident in `docs/knowledge/lessons.md`
- [ ] Create backup of recovered state
- [ ] Notify stakeholders of any data loss

---

## 8. References

- **phase-38.17-deployment-diagram.md** - System architecture
- **blackboard-agent-orchestration-design.md** - Core design
- **docs/knowledge/lessons.md** - Lessons learned repository
- **LES-044** - Signal file bridge implementation

---

*Generated per SOP-DES.6.m - Playbooks + Runbooks*
