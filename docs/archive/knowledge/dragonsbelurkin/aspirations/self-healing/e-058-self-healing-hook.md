# E-058: Self-Healing Stop Hook Mechanism for Discovery Preservation

> **Research Document**
> **PS Reference:** phase-38.16 (e-058)
> **Created:** 2026-01-05
> **Author:** ps-researcher agent
> **Status:** Complete

---

## Executive Summary

This research investigates how to design a self-healing mechanism within Claude Code's Stop hook that enables Claude to retroactively capture discoveries before session ends. Unlike simple blocking (which halts Claude but doesn't correct behavior), self-healing enables Claude to take corrective action during the same turn.

**Key Findings:**
1. Stop hook can BLOCK Claude's response completion via exit code 2 + stderr or JSON `decision: block`
2. Stop hook output goes to Claude's context - Claude receives and can ACT on the feedback
3. Self-healing requires a three-component MAPE-K architecture: Monitor, Analyze, Execute (Plan delegated to Claude)
4. The "healing" mechanism is Claude itself responding to structured prompts from the Stop hook
5. File-based state persists healing instructions across the subprocess isolation boundary

---

## Research Questions

1. How can we detect when discoveries were made but not captured?
2. How can the Stop hook enable Claude to retroactively capture discoveries?
3. What feedback mechanisms modify Claude's behavior (not just block it)?
4. How do we implement this within Claude Code's subprocess isolation constraints?

---

## W-MATRIX Analysis

### WHO: Actors Involved

| Actor | Role | Evidence |
|-------|------|----------|
| **Claude (Agent)** | Primary actor who makes discoveries and must capture them | Claude's responses contain discovery language ("I found...", "This reveals...") |
| **Stop Hook (Subprocess)** | Detector/Analyzer that monitors Claude's output and returns feedback | Stop hooks receive `assistant_response` in stdin JSON (line 22 of `stop.sh`) |
| **Knowledge Detector Module** | Detection engine that identifies uncaptured knowledge | `knowledge_detector.py` already implements pattern matching for assumptions, decisions, patterns |
| **User** | Beneficiary of captured knowledge; provides correction if needed | User's messages checked for corrections via `detect-corrections` |
| **File System** | State bridge enabling hook-to-Claude communication | Hooks cannot access MCP (LES-030), must use `.ecw/` file-based state |

**Actor Interaction Flow:**
```
Claude → generates response with discoveries
Stop Hook → receives response, runs detection
Stop Hook → writes healing prompt to file + returns blocking JSON
Claude → receives blocking reason, reads healing file
Claude → executes healing (captures discoveries)
Stop Hook → next turn verifies capture
```

### WHAT: Technical Mechanisms Available

#### Detection Mechanisms (existing)

1. **Knowledge Detector Patterns** (`knowledge_detector.py` lines 137-218)
   - Assumption patterns: "I assume...", "presumably...", "probably..."
   - Decision patterns: "I decided...", "we chose...", "the approach is..."
   - Discovery indicators: "I found...", "this reveals...", "discovered that..."
   - Confidence levels: HIGH, MEDIUM, LOW

2. **Transcript Access** (Stop hook stdin)
   ```json
   {
     "session_id": "string",
     "transcript_path": "string",
     "assistant_response": "string",  // Claude's full response
     "stop_reason": "string"
   }
   ```

3. **File-Based State** (`.ecw/` directory)
   - `violations.json` - tracks enforcement violations
   - `config.json` - enforcement configuration
   - Extensible for healing state

#### Correction/Healing Mechanisms (to implement)

1. **Stop Hook Blocking with Structured Prompt**
   ```json
   {
     "continue": false,
     "decision": "block",
     "reason": "HEALING REQUIRED: 3 discoveries detected but not captured..."
   }
   ```

2. **Healing Instructions File** (new)
   ```
   .ecw/healing/pending-captures.json
   {
     "session_id": "...",
     "detected_at": "2026-01-05T...",
     "items": [
       {
         "type": "discovery",
         "text": "Found that hooks cannot access MCP",
         "suggested_key": "kb:dis:hook-mcp-isolation",
         "confidence": "HIGH"
       }
     ],
     "instructions": "Capture these items using context_save or add to knowledge files"
   }
   ```

3. **Session Metrics Tracking** (`session_metrics.py`)
   - `discoveries_made` counter
   - `discoveries_captured` counter
   - Health status calculation

### WHERE: Implementation Location

| Component | Location | Purpose |
|-----------|----------|---------|
| **Discovery Detector** | `.claude/hooks/discovery_detector.py` (new, extends `knowledge_detector.py`) | Add discovery-specific patterns |
| **Healing State Manager** | `.claude/hooks/healing_state.py` (new) | Manage `.ecw/healing/` files |
| **Stop Hook Enhancement** | `.claude/hooks/stop.sh` (modify lines 265-310) | Add healing check and structured output |
| **Session Metrics Extension** | `.claude/hooks/session_metrics.py` (extend) | Add discovery tracking |
| **CLAUDE.md Trigger** | `CLAUDE.md` rule section | Add trigger phrase for healing response |

**Implementation Architecture:**
```
.claude/hooks/
├── stop.sh                    # Entry point (enhanced)
├── knowledge_detector.py      # Existing detection (extend)
├── discovery_detector.py      # New: discovery-specific patterns
├── healing_state.py           # New: manages healing workflow
└── session_metrics.py         # Extended: discovery tracking

.ecw/
└── healing/
    ├── pending-captures.json  # Items awaiting capture
    ├── healing-log.json       # Healing action history
    └── session-discoveries.json # Session discovery count
```

### WHEN: Trigger Conditions

| Trigger | Condition | Action |
|---------|-----------|--------|
| **End of Turn** | Stop hook fires naturally | Run discovery detection |
| **Discovery Detected** | Pattern match in `assistant_response` | Increment `discoveries_made` counter |
| **Missing Capture** | `discoveries_made > discoveries_captured` | Write healing instructions |
| **Healing Required** | Uncaptured count > 0 at turn end | Block with healing prompt |
| **Session End Signal** | User says "end session", compaction imminent | Urgent healing block |
| **Threshold Breach** | >3 uncaptured discoveries | HIGH urgency healing |

**Trigger Decision Tree:**
```
Stop hook fires
    │
    ├── Parse assistant_response
    │
    ├── Run discovery detection
    │   └── Count discoveries in response
    │
    ├── Check session metrics
    │   └── Compare discoveries_made vs captured
    │
    ├── If uncaptured > 0:
    │   │
    │   ├── Write pending-captures.json
    │   │
    │   ├── Calculate urgency
    │   │   ├── >3 uncaptured → HIGH
    │   │   ├── session ending → CRITICAL
    │   │   └── otherwise → NORMAL
    │   │
    │   └── Return blocking JSON with healing prompt
    │
    └── If all captured:
        └── Return continue: true
```

### WHY: Root Cause and Solution Rationale

#### Root Cause Analysis (5 Whys)

| # | Why | Answer |
|---|-----|--------|
| 1 | Why are discoveries lost? | Claude doesn't capture them before session ends |
| 2 | Why doesn't Claude capture them? | No reminder/prompt to do so during work |
| 3 | Why no reminder? | Stop hook only warns at session end, doesn't enable correction |
| 4 | Why doesn't warning enable correction? | Warning just shows text; doesn't block or provide action |
| 5 | Why can't warning provide action? | Hook design was "inform only", not "inform and heal" |

**Root Cause:** The Stop hook was designed as a passive observer (warn only) rather than an active controller (block and heal).

#### Solution Rationale

**From Control Theory:**
Self-adaptive systems require a feedback loop with:
1. **Monitor** - Observe system state
2. **Analyze** - Detect deviation from desired state
3. **Plan** - Determine corrective action
4. **Execute** - Apply correction
5. **Knowledge** - Learn from past incidents

**Mapping to Claude Code:**
| MAPE-K Component | Implementation |
|------------------|----------------|
| **Monitor** | Stop hook reads `assistant_response` |
| **Analyze** | Knowledge detector identifies uncaptured discoveries |
| **Plan** | Claude interprets healing instructions (delegated to agent) |
| **Execute** | Claude uses context_save or writes to knowledge files |
| **Knowledge** | Healing log persists learning across sessions |

**Why Self-Healing Works:**
1. Stop hook can BLOCK Claude's response completion
2. Blocking reason goes INTO Claude's context
3. Claude can READ the reason and RESPOND to it
4. Claude has full capability to capture discoveries
5. Next turn, Stop hook verifies capture occurred

### HOW: Step-by-Step Mechanism

#### Phase 1: Detection (Stop Hook Subprocess)

```python
# discovery_detector.py (new module)

DISCOVERY_PATTERNS = [
    (r"\bI\s+(?:have\s+)?(?:found|discovered)\s+(?:that\s+)?", Confidence.HIGH, "found_that"),
    (r"\bthis\s+(?:shows|reveals|indicates|demonstrates)\b", Confidence.HIGH, "reveals"),
    (r"\bturns?\s+out\s+(?:that\s+)?", Confidence.HIGH, "turns_out"),
    (r"\binterestingly\b", Confidence.MEDIUM, "interestingly"),
    (r"\bkey\s+(?:insight|finding|observation)\b", Confidence.HIGH, "key_insight"),
    (r"\bimportant(?:ly)?\s+(?:to\s+note|observation)\b", Confidence.HIGH, "important"),
    (r"\brealized\s+(?:that\s+)?", Confidence.MEDIUM, "realized"),
    (r"\blearned\s+(?:that\s+)?", Confidence.MEDIUM, "learned"),
]

def detect_discoveries(text: str) -> DetectionResult:
    """Detect discovery language in text."""
    return detect_with_patterns(text, DISCOVERY_PATTERNS, KnowledgeType.DISCOVERY)
```

#### Phase 2: State Management (File-Based Bridge)

```python
# healing_state.py (new module)

import json
from pathlib import Path
from datetime import datetime

HEALING_DIR = Path(".ecw/healing")

def write_pending_captures(session_id: str, discoveries: list[Detection]) -> Path:
    """Write pending captures for Claude to process."""
    HEALING_DIR.mkdir(parents=True, exist_ok=True)

    pending = {
        "session_id": session_id,
        "detected_at": datetime.utcnow().isoformat(),
        "uncaptured_count": len(discoveries),
        "items": [
            {
                "type": "discovery",
                "text": d.context,
                "suggested_key": f"kb:dis:{generate_slug(d.matched_text)}",
                "confidence": d.confidence.value,
                "pattern": d.pattern_name,
            }
            for d in discoveries
        ],
        "instructions": generate_healing_instructions(len(discoveries))
    }

    path = HEALING_DIR / "pending-captures.json"
    path.write_text(json.dumps(pending, indent=2))
    return path

def generate_healing_instructions(count: int) -> str:
    """Generate clear healing instructions for Claude."""
    return f"""
HEALING REQUIRED: {count} discovery/discoveries detected but not captured.

To complete this healing:
1. Read .ecw/healing/pending-captures.json for details
2. For each item, either:
   a) Use context_save(key="kb:dis:...", value="...") to persist to memory
   b) Add to docs/knowledge/discoveries.md with proper formatting
3. After capturing, clear the file or mark items as captured

This ensures knowledge is not lost when the session ends or compacts.
"""
```

#### Phase 3: Stop Hook Enhancement

```bash
# stop.sh (enhanced section around line 265)

# =============================================================================
# DISCOVERY HEALING CHECK (Self-Healing Mechanism)
# =============================================================================

DISCOVERIES_MADE=0
DISCOVERIES_CAPTURED=0
HEALING_REQUIRED=false

if [[ -n "$ASSISTANT_RESPONSE" ]] && [[ -f "$HOOKS_DIR/discovery_detector.py" ]]; then
    # Detect discoveries in response
    DISCOVERY_RESULT=$(python3 "$HOOKS_DIR/discovery_detector.py" detect "$ASSISTANT_RESPONSE" 2>/dev/null || echo '{}')
    DISCOVERIES_MADE=$(echo "$DISCOVERY_RESULT" | jq -r '.count // 0')

    if [[ "$DISCOVERIES_MADE" -gt 0 ]]; then
        # Check if captures were made (look for context_save or knowledge file edits)
        # This is a heuristic check
        CAPTURE_INDICATORS=$(echo "$ASSISTANT_RESPONSE" | grep -c "context_save\|kb:dis:\|## Discovery\|## DIS-" || echo "0")

        if [[ "$CAPTURE_INDICATORS" -lt "$DISCOVERIES_MADE" ]]; then
            HEALING_REQUIRED=true

            # Write healing state for Claude to process
            SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
            python3 "$HOOKS_DIR/healing_state.py" write-pending "$SESSION_ID" "$DISCOVERY_RESULT"

            # Calculate urgency
            if [[ "$DISCOVERIES_MADE" -gt 3 ]]; then
                URGENCY="HIGH"
            else
                URGENCY="NORMAL"
            fi
        fi
    fi
fi

# Build healing output if required
if [[ "$HEALING_REQUIRED" == "true" ]]; then
    HEALING_PATH="$PROJECT_DIR/.ecw/healing/pending-captures.json"
    HEALING_MSG="HEALING REQUIRED: $DISCOVERIES_MADE discovery(ies) detected but not captured.\n\nRead $HEALING_PATH for items to capture.\n\nTo heal: use context_save() for each item or add to knowledge files."

    # Return blocking response
    cat <<EOF
{
  "continue": false,
  "decision": "block",
  "reason": "$HEALING_MSG"
}
EOF
    exit 0
fi
```

#### Phase 4: CLAUDE.md Integration (Trigger Phrase)

```markdown
## Trigger Phrases (addition to CLAUDE.md)

| User Says | Claude Does |
|-----------|-------------|
| "heal discoveries" | Read .ecw/healing/pending-captures.json and capture items |
| [Stop hook healing block] | Read healing file and capture discoveries |
```

#### Phase 5: Verification Loop

```python
# healing_state.py (verification function)

def verify_captures(session_id: str) -> dict:
    """Verify that pending captures have been completed."""
    pending_path = HEALING_DIR / "pending-captures.json"

    if not pending_path.exists():
        return {"status": "no_pending", "remaining": 0}

    pending = json.loads(pending_path.read_text())

    # Check if same session
    if pending.get("session_id") != session_id:
        return {"status": "stale_session", "remaining": len(pending.get("items", []))}

    # Remaining items not marked captured
    remaining = [
        item for item in pending.get("items", [])
        if not item.get("captured", False)
    ]

    if not remaining:
        # All captured - clean up
        pending_path.unlink()
        return {"status": "all_captured", "remaining": 0}

    return {"status": "pending", "remaining": len(remaining)}
```

---

## Self-Healing Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SELF-HEALING FEEDBACK LOOP                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                │
│  │    Claude    │────▶│  Stop Hook   │────▶│  Detection   │                │
│  │  (Response)  │     │  (Fires)     │     │  (Analyze)   │                │
│  └──────────────┘     └──────────────┘     └──────────────┘                │
│         │                                         │                         │
│         │                                         ▼                         │
│         │                              ┌──────────────────┐                 │
│         │                              │  Discoveries > 0 │                 │
│         │                              │  not captured?   │                 │
│         │                              └────────┬─────────┘                 │
│         │                                       │                           │
│         │                          ┌────────────┴────────────┐             │
│         │                          ▼                         ▼             │
│         │                   ┌─────────────┐          ┌─────────────┐       │
│         │                   │     YES     │          │     NO      │       │
│         │                   └──────┬──────┘          └──────┬──────┘       │
│         │                          │                        │              │
│         │                          ▼                        ▼              │
│         │               ┌──────────────────┐    ┌──────────────────┐       │
│         │               │ Write Healing    │    │ Continue: true   │       │
│         │               │ State to File    │    │ (Normal flow)    │       │
│         │               └────────┬─────────┘    └──────────────────┘       │
│         │                        │                                          │
│         │                        ▼                                          │
│         │               ┌──────────────────┐                               │
│         │               │ Return Block     │                               │
│         │               │ + Healing Prompt │                               │
│         │               └────────┬─────────┘                               │
│         │                        │                                          │
│         ▼                        ▼                                          │
│  ┌──────────────────────────────────────────┐                              │
│  │ Claude Receives Block + Healing Reason   │                              │
│  │ (Prompt injected into context)           │                              │
│  └────────────────────┬─────────────────────┘                              │
│                       │                                                     │
│                       ▼                                                     │
│  ┌──────────────────────────────────────────┐                              │
│  │ Claude Reads .ecw/healing/pending.json   │                              │
│  │ Claude Executes Captures (context_save)  │                              │
│  └────────────────────┬─────────────────────┘                              │
│                       │                                                     │
│                       ▼                                                     │
│  ┌──────────────────────────────────────────┐                              │
│  │ Next Turn: Stop Hook Verifies Captures   │                              │
│  │ If complete → Continue: true             │                              │
│  │ If pending → Block again                 │                              │
│  └──────────────────────────────────────────┘                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Critical Implementation Constraints

### Constraint 1: Subprocess Isolation (LES-030)

**Problem:** Hooks run as subprocesses and cannot access MCP context.

**Solution:** File-based state bridge
- Stop hook WRITES to `.ecw/healing/pending-captures.json`
- Claude READS from this file when blocked
- Claude uses MCP to execute captures
- Stop hook VERIFIES capture by checking file or memory

**Reference:** `/sidequests/evolving-claude-workflow/docs/knowledge/hook-mcp-limitation.md`

### Constraint 2: Stop Hook Blocking Mechanism

**Problem:** Stop hook must use correct blocking syntax.

**Solution:** Exit code 0 with JSON `decision: block`
```json
{
  "continue": false,
  "decision": "block",
  "reason": "Healing prompt text goes here"
}
```

**Reference:** `claude-code-hooks-best-practices.md` lines 76-115

### Constraint 3: Claude Must Act on Healing Prompt

**Problem:** Blocking alone doesn't make Claude act.

**Solution:**
1. CLAUDE.md includes trigger phrase recognition
2. Healing prompt includes explicit instructions
3. File path provided for detailed capture info

**Reference:** `CLAUDE.md` Trigger Phrases section

---

## Comparison with Alternative Approaches

| Approach | Detection | Correction | Pros | Cons |
|----------|-----------|------------|------|------|
| **Warn Only** | Yes | No | Simple, non-blocking | No correction happens |
| **Block Only** | Yes | No | Prevents completion | User must intervene |
| **Self-Healing (Proposed)** | Yes | Yes (via Claude) | Automated correction | Complexity |
| **External Service** | Yes | Yes (via API) | Reliable | Requires infra |
| **User Prompt** | No | Manual | User control | Knowledge lost |

**Recommendation:** Self-Healing (Proposed) balances automation with existing constraints.

---

## Validation Criteria

### Functional Requirements

1. **F1:** Stop hook detects discoveries in assistant_response
2. **F2:** Uncaptured discoveries trigger blocking response
3. **F3:** Blocking reason includes healing instructions
4. **F4:** Claude reads and acts on healing file
5. **F5:** Captures persist to memory or knowledge files
6. **F6:** Verification confirms capture completion

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Discovery detection rate | >90% | Manual audit of 10 sessions |
| Healing completion rate | >80% | Pending captures resolved |
| False positive rate | <10% | Non-discoveries flagged |
| User intervention rate | <20% | Manual intervention needed |

---

## 12. Validation Status (Soft Enforcement)

| Category | Status | Notes |
|----------|--------|-------|
| W-DIMENSION COVERAGE | 6/6 | WHO, WHAT, WHERE, WHEN, WHY, HOW all addressed |
| FRAMEWORK APPLICATION | 5/5 | 5W1H, 5 Whys, MAPE-K applied |
| EVIDENCE & GAPS | 4/4 | Sources cited, unknowns documented |
| OUTPUT SECTIONS | 4/4 | Executive summary, W-MATRIX, recommendations, knowledge items |

**Quality Status:** COMPLETE (19/19 criteria met)

---

## Sources

| # | Source | URL/Path | Key Contribution |
|---|--------|----------|------------------|
| 1 | Claude Code Hooks Best Practices | `sidequests/evolving-claude-workflow/docs/research/claude-code-hooks-best-practices.md` | Hook lifecycle, blocking mechanism, exit codes |
| 2 | Hook MCP Limitation | `sidequests/evolving-claude-workflow/docs/knowledge/hook-mcp-limitation.md` | Subprocess isolation constraint (LES-030) |
| 3 | Knowledge Detector | `.claude/hooks/knowledge_detector.py` | Detection patterns and confidence levels |
| 4 | Stop Hook Implementation | `.claude/hooks/stop.sh` | Current implementation, integration point |
| 5 | Session Metrics | `.claude/hooks/session_metrics.py` | Session health tracking pattern |
| 6 | GeeksforGeeks Self-Healing Systems | https://www.geeksforgeeks.org/system-design/self-healing-systems-system-design/ | MAPE-K architecture, feedback loops |
| 7 | SpringerLink Self-Adaptive Systems | https://link.springer.com/chapter/10.1007/978-3-642-02161-9_3 | Feedback control loop design |
| 8 | When to Capture Decision Tree | `design/decision-trees/when-to-capture.md` | Knowledge capture triggers |
| 9 | Hooks Documentation | `.claude/docs/hooks.md` | Hook configuration, enforcement levels |
| 10 | Hook System Architecture | `design/architecture/hook-system.md` | Hook lifecycle diagram |

---

## Knowledge Items Generated

### PAT-053: Self-Healing Hook Pattern
- **Title:** Stop Hook Self-Healing via File-Based State Bridge
- **Context:** When a Stop hook needs to trigger corrective action by Claude
- **Pattern:**
  1. Hook detects issue in `assistant_response`
  2. Hook writes structured healing state to `.ecw/healing/`
  3. Hook returns `decision: block` with healing instructions
  4. Claude reads healing file and executes correction
  5. Next turn, hook verifies correction
- **Anti-pattern:** Hook trying to directly call MCP tools (impossible due to subprocess isolation)
- **Reference:** LES-030, MAPE-K architecture

### PAT-054: Discovery Detection Pattern
- **Title:** Pattern Matching for Discovery Language
- **Context:** Detecting discoveries in Claude's responses for knowledge capture
- **Pattern:** Use regex patterns matching discovery indicators ("I found...", "this reveals...", "key insight...") with confidence levels
- **Anti-pattern:** Only detecting explicit "discovered" keyword (misses implicit discoveries)
- **Reference:** Extends `knowledge_detector.py` approach

### LES-052: Blocking Without Healing is Insufficient
- **Title:** Stop Hook Blocking Without Healing Prompt Leaves Knowledge Uncaptured
- **Context:** Initial design had Stop hook warning only, which users ignore
- **Lesson:** Blocking must include actionable healing instructions AND a file-based state bridge for Claude to read and act on
- **Prevention:** Always pair Stop hook blocks with healing state files and explicit instructions
- **Reference:** E-058 root cause analysis

### ASM-059: Claude Responds to Structured Healing Prompts
- **Title:** Claude Will Act on Healing Prompts in Stop Hook Block Reason
- **Context:** Self-healing mechanism assumes Claude reads and acts on blocking reason
- **Assumption:** When Stop hook returns `decision: block` with healing instructions, Claude will read the healing file and execute captures
- **Impact:** If Claude ignores healing prompts, manual intervention required
- **Confidence:** MEDIUM (needs validation)
- **Reference:** Based on Claude's instruction-following behavior, not tested in production

---

## Recommendations

### Immediate Actions

1. **Implement `discovery_detector.py`** - Extend `knowledge_detector.py` with discovery patterns
2. **Implement `healing_state.py`** - File-based state manager for healing workflow
3. **Enhance `stop.sh`** - Add healing check section (lines 265-310 area)
4. **Add CLAUDE.md trigger** - Recognize healing prompts and act on them

### Future Enhancements

1. **Urgency escalation** - After 3 blocks, mark as CRITICAL and prepend to user message
2. **Learning loop** - Track healing success rate and adjust patterns
3. **Dashboard integration** - Show healing metrics in session dashboard
4. **Smart detection** - Use LLM to assess discovery importance (not just pattern matching)

---

## Conclusion

A self-healing Stop hook mechanism is feasible within Claude Code's architectural constraints. The key insight is that while hooks cannot directly access MCP, they CAN influence Claude's behavior through:

1. **Blocking** - Prevents turn completion, forcing attention
2. **Prompt injection** - Block reason becomes part of Claude's context
3. **File-based state** - Structured instructions Claude can read and act on

The proposed MAPE-K architecture (Monitor-Analyze-Plan-Execute-Knowledge) delegates the "Plan" and "Execute" phases to Claude itself, working around subprocess isolation. This makes Claude the "actuator" in the feedback loop, with the Stop hook serving as the "sensor" and "controller."

Implementation requires approximately 300 lines of new Python code plus Stop hook modifications, all leveraging existing patterns from knowledge detection and enforcement systems.
