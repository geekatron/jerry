# Model Selection Capability Effort Analysis

> **PS ID:** work-025
> **Entry ID:** e-001
> **Topic:** Model Selection Capability Effort Analysis
> **Agent:** ps-analyst v2.0.0
> **Date:** 2026-01-30

---

## Document Audience (Triple-Lens)

| Level | Audience | Focus |
|-------|----------|-------|
| **L0 (ELI5)** | Product managers, stakeholders | Problem scope, effort estimate, value |
| **L1 (Engineer)** | Developers implementing the feature | Technical changes, file modifications, testing |
| **L2 (Architect)** | System designers | Architecture impacts, design patterns, trade-offs |

---

## L0: Executive Summary (ELI5)

### What is the Problem?

Right now, when the transcript skill runs, each agent (parser, extractor, formatter, etc.) uses a **hardcoded** model specified in their agent definition files. For example:
- `ts-parser` always uses `haiku` (fast, cheap)
- `ts-extractor` always uses `sonnet` (smart, expensive)
- `ts-formatter` always uses `sonnet` (smart, expensive)

Users have **NO WAY** to customize which models to use for their specific needs. If you want to:
- Use `opus` for super-high-quality extraction
- Use `haiku` for all agents to save costs on simple transcripts
- Mix and match models based on transcript complexity

...you're out of luck. The models are **hardcoded in agent .md files**.

### Why Does This Matter?

Different transcripts have different needs:
- **Simple standup notes** → Use `haiku` everywhere (10x cheaper)
- **Critical legal deposition** → Use `opus` for extraction (highest accuracy)
- **Budget-constrained analysis** → Minimize costs with selective model use
- **Experimental testing** → Try different model combinations

The current architecture **prevents this flexibility**, forcing all users to use the same expensive model mix regardless of their needs.

### What's the Effort?

**Medium to Large (M-L)** - This is non-trivial but achievable.

**Estimated effort:** 3-5 days for a skilled engineer

**Why it's not trivial:**
1. Model selection happens in **multiple places** (SKILL.md, agent .md files, Task tool invocations)
2. Need to **thread model parameters** through the entire invocation chain
3. Requires **validation** to prevent invalid model choices
4. Need **backward compatibility** so existing invocations still work
5. Testing across **multiple agent types** and model combinations

### Recommendation

**Implement this feature** - The value is high and the architecture supports it with moderate effort.

**Phased Approach:**
- **Phase 1 (MVP):** Simple CLI flag (2 days)
- **Phase 2 (Full):** Per-agent model selection (3 days)

---

## L1: Technical Analysis (Engineer)

### Current Architecture

#### Model Specification Today

Models are specified in **YAML frontmatter** of agent definition files:

```yaml
# File: skills/transcript/agents/ts-parser.md
---
name: ts-parser
version: "2.0.0"
model: "haiku"  # ← HARDCODED HERE
---
```

**Where models are used:**

| Component | Current Behavior | Model Source |
|-----------|------------------|--------------|
| SKILL.md orchestration | Invokes agents via Task tool | Not specified in SKILL.md |
| Task tool calls | `Task(subagent_type="general-purpose")` | No model parameter exists |
| Agent .md files | YAML frontmatter `model: "haiku"` | Hardcoded in file |
| Claude Code runtime | Reads agent .md, uses model field | Consumes from YAML |

#### Invocation Chain (v2.3.0)

```
User: /transcript file.vtt
    ↓
SKILL.md (skills/transcript/SKILL.md)
    ↓
Phase 1: CLI parsing (uv run jerry transcript parse ...)
    ↓
Phase 2: Task(subagent_type="general-purpose", prompt="You are ts-extractor...")
    ↓
Claude Code reads: skills/transcript/agents/ts-extractor.md
    ↓
Extracts: model: "sonnet"  ← CONSUMED HERE
    ↓
Runs ts-extractor using sonnet model
```

**Key Insight:** Claude Code's Task tool appears to read the agent .md file to determine which model to use. The model is **NOT** passed as a Task parameter today.

### 5W2H Analysis

#### WHAT needs to change?

1. **SKILL.md** - Add parameter parsing for model selection
2. **Agent .md files** - Keep default models, make them overridable
3. **Task tool invocations** - Pass model parameter (if supported)
4. **CLI (jerry transcript)** - Accept model flags
5. **Validation logic** - Ensure valid model choices
6. **Documentation** - Update PLAYBOOK.md, RUNBOOK.md

#### WHERE are changes needed?

| File/Component | Change Type | Effort |
|----------------|-------------|--------|
| `skills/transcript/SKILL.md` | Add parameter parsing | **Medium** |
| `skills/transcript/agents/*.md` | Document override behavior | **Low** |
| `skills/transcript/docs/PLAYBOOK.md` | Usage examples | **Low** |
| `skills/transcript/docs/RUNBOOK.md` | Model selection guidance | **Low** |
| CLI (`src/transcript/cli.py`) | Add `--model-*` flags | **Medium** |
| Agent invocations in SKILL.md | Pass model to Task tool | **High** (unknown if supported) |

#### WHO is affected?

| Stakeholder | Impact | Change Required |
|-------------|--------|-----------------|
| **End Users** | New capability | Learn new CLI flags |
| **Skill Orchestrator (SKILL.md)** | Logic changes | Parse and pass models |
| **Agent Definitions** | Documentation updates | Add override notes |
| **Jerry CLI** | New parameters | Flag parsing |
| **Claude Code Task Tool** | Unknown | May need Claude Code platform support |

#### WHY is this challenging?

1. **Claude Code Task Tool Unknown:** We don't know if Task supports model override
2. **Parameter Threading:** Model choice must flow: CLI → SKILL.md → Task → Agent runtime
3. **Validation Complexity:** Need to validate model names, ensure compatibility
4. **Backward Compatibility:** Existing invocations without model flags must still work
5. **Testing Matrix:** 5 agents × 3 models = 15 combinations to test

#### WHEN would this be used?

**Use Cases:**

| Scenario | Model Selection Strategy | Business Value |
|----------|-------------------------|----------------|
| Simple standup notes | `--model-all haiku` | 90% cost reduction |
| Legal deposition | `--model-extractor opus` | Highest accuracy |
| Budget-constrained | `--model-parser haiku --model-formatter haiku` | Minimize costs |
| Quality testing | Try different extraction models | Find optimal quality/cost |
| Experimental research | Test model capabilities | Innovation |

#### HOW would it work? (Proposed Design)

**Option A: Single Model Override (Simple)**

```bash
# Use haiku for all agents
uv run jerry transcript parse file.vtt --model haiku
```

**Option B: Per-Agent Model Selection (Full)**

```bash
# Mix and match
uv run jerry transcript parse file.vtt \
    --model-parser haiku \
    --model-extractor opus \
    --model-formatter sonnet \
    --model-mindmap haiku
```

**Implementation Flow:**

```
1. User invokes: jerry transcript parse file.vtt --model-extractor opus
   ↓
2. CLI parses flags → model_overrides = {"extractor": "opus"}
   ↓
3. CLI passes to SKILL.md context (if possible) OR stores in state
   ↓
4. SKILL.md orchestration reads model_overrides
   ↓
5. When invoking ts-extractor:
   - IF model_overrides["extractor"] exists → use "opus"
   - ELSE → use default from ts-extractor.md ("sonnet")
   ↓
6. Task tool invocation:
   - IF Claude Code Task supports model parameter → pass it
   - ELSE → need alternative approach (modify agent .md? context injection?)
```

#### HOW MUCH effort?

**Component Breakdown:**

| Component | Effort | Risk | Notes |
|-----------|--------|------|-------|
| CLI flag parsing | **S (4h)** | Low | Standard argparse extension |
| SKILL.md parameter handling | **M (8h)** | Medium | Parse, validate, thread through |
| Task tool model passing | **L (16h)** | **HIGH** | Unknown if Task supports this |
| Agent .md documentation | **S (2h)** | Low | Add override notes |
| Validation logic | **M (6h)** | Medium | Model name validation, defaults |
| Testing | **L (12h)** | Medium | 5 agents × 3 models = matrix |
| Documentation | **S (4h)** | Low | Update guides |
| **TOTAL** | **52h (~6.5 days)** | | Assumes full per-agent solution |

**MVP (Single Model Override):**

| Component | Effort | Total |
|-----------|--------|-------|
| CLI flag `--model` | S (4h) | 4h |
| SKILL.md global model | M (8h) | 8h |
| Task tool integration | L (12h) | 12h |
| Basic testing | M (6h) | 6h |
| Docs | S (2h) | 2h |
| **TOTAL** | | **32h (~4 days)** |

### Architectural Constraints

#### Claude Code Task Tool

**CRITICAL UNKNOWN:** Does Claude Code's Task tool support a `model` parameter?

**Evidence to investigate:**
```python
# Current invocation (from SKILL.md analysis)
Task(
    description="Extract entities from transcript",
    subagent_type="general-purpose",
    prompt="You are ts-extractor v1.3.0..."
)

# Does this work?
Task(
    description="Extract entities from transcript",
    subagent_type="general-purpose",
    model="opus",  # ← CAN WE DO THIS?
    prompt="You are ts-extractor v1.3.0..."
)
```

**Mitigation if Task doesn't support model parameter:**

1. **Context Injection Approach:**
   ```markdown
   You are ts-extractor v1.3.0.

   **MODEL OVERRIDE:** Use claude-3-opus-20250514 instead of default sonnet.
   ```
   - Risk: Agent might ignore the override instruction
   - Reliability: Unknown

2. **Dynamic Agent .md Generation:**
   - Generate temporary agent .md file with model override
   - Point Task to custom agent definition
   - Risk: File system side effects, cleanup complexity

3. **Hybrid Approach:**
   - Use Task model parameter if available
   - Fall back to context injection if not

#### Validation Requirements

**Model Name Validation:**

```python
VALID_MODELS = {
    "haiku": "claude-3-haiku-20240307",
    "sonnet": "claude-3-sonnet-20250514",
    "opus": "claude-3-opus-20250514",
    "sonnet-4.5": "claude-sonnet-4-5-20250929",  # Newest
}

AGENT_COMPATIBILITY = {
    "ts-parser": ["haiku", "sonnet"],  # Orchestration logic, avoid opus
    "ts-extractor": ["sonnet", "opus", "sonnet-4.5"],  # Quality-sensitive
    "ts-formatter": ["sonnet", "opus"],  # Formatting quality
    "ts-mindmap-*": ["haiku", "sonnet"],  # Simple task
}
```

**Validation Logic:**

1. Check model name is in `VALID_MODELS`
2. Check model is compatible with agent (warn if not recommended)
3. Provide default if not specified

### Breaking Changes Analysis

**Backward Compatibility:**

✅ **NO BREAKING CHANGES** if implemented correctly:

1. Default behavior unchanged (use hardcoded models from agent .md)
2. Model flags are **optional** - existing invocations work as-is
3. Agent .md files maintain default `model:` field as fallback

**Migration Path:**

None required. New capability is additive.

---

## L2: Strategic Assessment (Architect)

### Design Pattern Analysis

#### Pattern: Strategy Pattern for Model Selection

```
┌─────────────────────────────────────────────────────────┐
│              Model Selection Strategy                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────┐                                         │
│  │   User     │                                         │
│  │ Invocation │                                         │
│  └─────┬──────┘                                         │
│        │                                                │
│        ▼                                                │
│  ┌────────────────────┐                                 │
│  │  Model Selector    │                                 │
│  │  (SKILL.md)        │                                 │
│  │                    │                                 │
│  │  IF override:      │                                 │
│  │    use user choice │                                 │
│  │  ELSE:             │                                 │
│  │    use agent.md    │                                 │
│  │    default         │                                 │
│  └─────┬──────────────┘                                 │
│        │                                                │
│        ▼                                                │
│  ┌────────────────────┐                                 │
│  │  Task Invocation   │                                 │
│  │  with model param  │                                 │
│  └────────────────────┘                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Advantages:**
- Single responsibility: Model selection logic in one place
- Open/closed: Add new models without changing agents
- Dependency inversion: Agents depend on abstraction, not concrete models

**Disadvantages:**
- Complexity: Additional layer of indirection
- Testing: More combinations to validate

### Performance Implications

#### Cost Analysis (Per 1000-segment Transcript)

**Current (Hardcoded):**

| Agent | Model | Cost (est.) |
|-------|-------|------------|
| ts-parser | haiku | $0.10 |
| ts-extractor | sonnet | $3.50 |
| ts-formatter | sonnet | $2.00 |
| ts-mindmap-* | sonnet | $1.00 |
| **TOTAL** | | **$6.60** |

**User-Optimized (All Haiku):**

| Agent | Model | Cost (est.) |
|-------|-------|------------|
| ts-parser | haiku | $0.10 |
| ts-extractor | haiku | $0.35 |
| ts-formatter | haiku | $0.20 |
| ts-mindmap-* | haiku | $0.10 |
| **TOTAL** | | **$0.75** |

**Savings:** 88% cost reduction for simple transcripts

**Quality-Optimized (Critical Extraction):**

| Agent | Model | Cost (est.) |
|-------|-------|------------|
| ts-parser | haiku | $0.10 |
| ts-extractor | **opus** | $14.00 |
| ts-formatter | sonnet | $2.00 |
| ts-mindmap-* | haiku | $0.10 |
| **TOTAL** | | **$16.20** |

**Cost:** 145% increase, but **highest possible accuracy** for critical work

### Quality Attribute Trade-offs

| Quality Attribute | Impact | Direction | Mitigation |
|-------------------|--------|-----------|------------|
| **Flexibility** | High | ↑ | Users can optimize cost/quality |
| **Complexity** | Medium | ↑ | More configuration options to understand |
| **Testability** | High | ↓ | Exponential test matrix (agents × models) |
| **Maintainability** | Low | ↔ | Well-isolated change |
| **Performance** | Variable | ↕ | Depends on user model choices |
| **Cost** | High | ↕ | Users control their cost/quality trade-off |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Task tool doesn't support model param** | Medium | **High** | Investigate Task API, use fallback strategies |
| **Invalid model choices break agents** | Medium | Medium | Validation + compatibility matrix |
| **Users choose poor models** | High | Low | Documentation + recommended defaults |
| **Testing complexity explodes** | High | Medium | Prioritize critical combinations |
| **Breaking existing invocations** | Low | High | Careful backward compatibility design |

### One-Way Door Decisions

**Reversible (Two-Way Doors):**
- CLI flag naming (`--model` vs `--agent-model`)
- Default model choices
- Validation warnings vs errors

**Irreversible (One-Way Doors):**
- ❌ **NONE** - This is additive, no one-way doors

All decisions can be changed later without breaking backward compatibility.

### Alternative Approaches Considered

#### Alternative 1: Environment Variables

```bash
export TRANSCRIPT_MODEL_EXTRACTOR=opus
uv run jerry transcript parse file.vtt
```

**Pros:**
- No CLI changes needed
- Works with existing infrastructure

**Cons:**
- Less discoverable than CLI flags
- Global state (not invocation-specific)
- Harder to use in scripts

**Verdict:** ❌ Rejected - CLI flags are more user-friendly

#### Alternative 2: Config File

```yaml
# ~/.jerry/transcript-config.yaml
models:
  parser: haiku
  extractor: opus
  formatter: sonnet
```

**Pros:**
- Persistent configuration
- Can share configs across team

**Cons:**
- Requires config file management
- Less transparent than CLI flags
- Complexity for simple use cases

**Verdict:** ⚠️ Future enhancement - Not MVP, but consider for v2

#### Alternative 3: Agent .md Hot-Swapping

Dynamically rewrite agent .md files before invocation.

**Pros:**
- No Claude Code Task tool dependency

**Cons:**
- File system side effects
- Race conditions in concurrent invocations
- Complexity of cleanup

**Verdict:** ❌ Rejected - Too fragile

### Recommended Approach

**Two-Phase Implementation:**

#### Phase 1: MVP (Single Model Override)

```bash
jerry transcript parse file.vtt --model haiku
```

**Scope:**
- Single `--model` flag applies to ALL agents (except parser, which stays haiku)
- Validation for model name
- Documentation updates
- Basic testing (3 model variants × 1 transcript)

**Effort:** 4 days
**Value:** 80% of use cases (cost optimization for simple transcripts)
**Risk:** Low (small scope)

#### Phase 2: Full (Per-Agent Selection)

```bash
jerry transcript parse file.vtt \
    --model-extractor opus \
    --model-formatter sonnet
```

**Scope:**
- Per-agent model flags
- Compatibility validation (warn on poor choices)
- Comprehensive testing
- Advanced documentation (cost/quality trade-off guide)

**Effort:** +2 days (incremental from Phase 1)
**Value:** Remaining 20% (power users, research use cases)
**Risk:** Medium (testing complexity)

---

## Recommendations

### Immediate Actions (High Priority)

1. **Investigate Claude Code Task Tool API** (2h)
   - Can Task accept a `model` parameter?
   - If not, what are the alternatives?
   - Document findings in DISC file

2. **Create Spike for Model Override Proof of Concept** (4h)
   - Modify SKILL.md to pass model to one agent
   - Test if it works
   - Document approach

3. **Define Model Compatibility Matrix** (2h)
   - Which models work with which agents?
   - What are the recommended defaults?
   - Document in RUNBOOK.md

### Implementation Sequence (Phased)

**Week 1: Research & Design**
- Day 1: Task tool investigation + PoC
- Day 2: Design document (ADR)
- Day 3: Validation logic design

**Week 2: Phase 1 MVP**
- Day 1-2: CLI flag + SKILL.md changes
- Day 3: Testing + bug fixes
- Day 4: Documentation

**Week 3: Phase 2 (Optional)**
- Day 1-2: Per-agent flags
- Day 3: Advanced testing
- Day 4: Final documentation

### Success Criteria

**MVP Success:**
- ✅ Users can specify `--model haiku` and all agents use haiku (except parser)
- ✅ Existing invocations without flag work unchanged
- ✅ Validation prevents invalid model names
- ✅ Documentation shows cost/quality trade-offs

**Full Success (Phase 2):**
- ✅ Users can mix models per agent
- ✅ Compatibility warnings guide good choices
- ✅ Comprehensive test coverage
- ✅ Performance benchmarks documented

---

## Conclusion

**Effort Estimate:** Medium to Large (M-L)
- **MVP:** 4 days (32 hours)
- **Full:** 6 days (48 hours)

**Risk Level:** Medium
- **Primary Risk:** Task tool model parameter support unknown
- **Mitigation:** PoC spike to resolve uncertainty early

**Business Value:** High
- 88% cost savings for simple transcripts (use haiku)
- Precision control for critical work (use opus)
- Flexibility for experimentation and research

**Recommendation:** **PROCEED WITH PHASED APPROACH**

Start with MVP (single model override) to deliver quick value with low risk. Expand to per-agent selection if user demand justifies the additional complexity.

**Next Steps:**
1. Spike: Investigate Task tool model parameter (2h)
2. ADR: Document model selection architecture (4h)
3. DISC: If Task doesn't support model param, create discovery for alternative (2h)

---

## References

**Files Analyzed:**
- `/skills/transcript/SKILL.md` - Orchestration logic
- `/skills/transcript/agents/ts-parser.md` - Parser agent (model: haiku)
- `/skills/transcript/agents/ts-extractor.md` - Extractor agent (model: sonnet)
- `/skills/transcript/agents/ts-formatter.md` - Formatter agent (model: sonnet)
- `/skills/problem-solving/agents/ps-critic.md` - Critic agent (model: sonnet)

**Related Work:**
- Jerry Constitution v1.0 - Principle P-002 (File Persistence)
- SKILL.md v2.3.0 - Current orchestration architecture
- TDD-FEAT-004 - Hybrid Infrastructure (v2.0 basis)

**Industry Prior Art:**
- OpenAI Agent Guide - Configuration flexibility
- LangChain - Model selection patterns
- Anthropic Claude API - Model variants (haiku/sonnet/opus)

---

*Document Version: 1.0.0*
*Analysis Completed: 2026-01-30*
*ps-analyst Agent: v2.0.0*
*Framework: 5W2H + FMEA + Pareto Analysis*
