# EN-206:DEC-001: Sync Strategy Selection for Cross-Platform Context Distribution

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-02-02 (Claude)
PURPOSE: Document the decision on which sync strategy to use for .context/ → .claude/
-->

> **Type:** decision
> **Status:** accepted
> **Priority:** critical
> **Created:** 2026-02-02T07:30:00Z
> **Parent:** EN-206
> **Owner:** Claude
> **Related:** SPIKE-001, DISC-001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of decision |
| [Decision Context](#decision-context) | Background and constraints |
| [Decisions](#decisions) | Structured D-NNN decision entries |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Traceability |

---

## Summary

Based on SPIKE-001 research findings, we select the **Hybrid Platform-Aware Bootstrap Script** strategy for syncing `.context/` to `.claude/`. This uses symlinks on macOS/Linux and junction points on Windows (no admin required).

**Decisions Captured:** 3

**Key Outcomes:**
- Cross-platform support without admin privileges on any platform
- Single `/bootstrap` skill provides uniform user experience
- Junction points enable Windows support without Developer Mode

---

## Decision Context

### Background

EN-206 Context Distribution Strategy requires a mechanism to sync canonical content from `.context/rules/` and `.context/patterns/` to `.claude/rules/` and `.claude/patterns/` where Claude Code reads them.

SPIKE-001 researched 5 strategies:
1. Symbolic Links
2. Junction Points (Windows only)
3. File Copy with Drift Detection
4. Git Submodules
5. Bootstrap Script with Platform Detection

### Constraints

- **C-001:** Must work on macOS, Linux, AND Windows
- **C-002:** Must NOT require administrator privileges on Windows
- **C-003:** Must be user-friendly (align with Jerry personality)
- **C-004:** Must minimize ongoing maintenance burden
- **C-005:** Must handle updates to Jerry's canonical rules

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Jerry Users | End users | Simple setup, reliable syncing |
| Enterprise Users | End users | No admin requirement critical |
| Jerry Maintainers | Developers | Maintainability, testability |

---

## Decisions

### D-001: Primary Sync Strategy

**Date:** 2026-02-02
**Participants:** Claude, User

#### Question/Context

User asked: "We will need to research at least 3 and up to 5 strategies that accomplish this using the /problem-solving skill - we should keep portability in mind (for example I like the symlink strategy but how will that work for people developing in windows?)"

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Symlinks Only** | Use symlinks everywhere | Simple, well-understood | Windows requires admin/Dev Mode |
| **B: File Copy** | Copy files with drift detection | Works everywhere | Duplicates files, manual re-sync |
| **C: Git Submodules** | Submodule for rules repo | Version control built-in | Complex for users, still need sync |
| **D: Hybrid Bootstrap** | Platform-aware script | Best of all worlds | More implementation work |

#### Decision

**We decided:** Option D - Hybrid Platform-Aware Bootstrap Script

The `/bootstrap` skill will:
1. Detect platform (macOS, Linux, Windows)
2. On macOS/Linux: Create symlinks
3. On Windows with Developer Mode: Create symlinks
4. On Windows without Developer Mode: Create junction points
5. On network drives or cross-drive: Fall back to file copy

#### Rationale

1. **Discovery DISC-001 proved junction points work without admin** - This was the key blocker for Windows support
2. **Single user experience** - Users run `/bootstrap` regardless of platform
3. **Auto-propagating changes** - Symlinks/junctions reflect source changes immediately
4. **Fallback safety** - File copy handles edge cases gracefully
5. **Aligns with industry practice** - npm's `symlink-dir` uses this exact approach

#### Implications

- **Positive:** Works for 100% of users without admin
- **Positive:** Uniform UX across platforms
- **Negative:** More complex implementation than symlinks-only
- **Follow-up required:** TASK-002 must implement platform detection logic

---

### D-002: Canonical Source Location

**Date:** 2026-02-02
**Participants:** Claude, User

#### Question/Context

Where should the canonical (version-controlled) rules and patterns live?

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: `.claude/`** | Keep in current location | No migration needed | Not distributed with plugin |
| **B: `.context/`** | New directory for canonical content | Clear separation, git-tracked | Migration required |
| **C: `config/`** | Generic config directory | Common convention | Less semantic |

#### Decision

**We decided:** Option B - Use `.context/` as canonical source

```
.context/                  # Version-controlled, distributable
├── rules/                 # Behavioral rules
├── patterns/              # Pattern catalog
└── templates/             # (already exists)

.claude/                   # Synced from .context/, user-local
├── rules/ → .context/rules/
├── patterns/ → .context/patterns/
├── agents/                # Plugin component (stays)
├── commands/              # Plugin component (stays)
└── settings.json          # User config (stays)
```

#### Rationale

1. **Clear separation** - `.context/` = canonical source, `.claude/` = active/synced
2. **`.context/templates/` already exists** - Consistent naming
3. **Git-tracked** - `.context/` should NOT be gitignored
4. **Distribution story** - `.context/` can be included in plugin distribution

---

### D-003: Jerry Personality for Bootstrap Skill

**Date:** 2026-02-02
**Participants:** Claude, User

#### Question/Context

User stated: "we will also need to create a bootstrap skill to help with this - it should be humerous and align with the Jerry framework sentiment"

After correction about Jerry's origin (ski culture "Jerry of the Day", NOT Tom and Jerry), explored existing persona research.

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Professional** | Standard technical messaging | Clear, business-appropriate | Doesn't align with Jerry persona |
| **B: Saucer Boy** | Shane McConkey-inspired, ski buddy energy | Aligns with Jerry persona | May confuse some users |
| **C: Minimal** | Just the facts | Fastest execution | Misses personality opportunity |

#### Decision

**We decided:** Option B - Saucer Boy voice mode (default Jerry persona)

Example messages:
- Welcome: "Let's get your bindings adjusted!"
- Progress: "Waxing your setup..."
- Success: "Fresh tracks await! Your guardrails are locked and loaded."
- Error: "Yard sale on the setup - let me help you recover."
- Already done: "Looks like you're already dialed in. Want me to check the edges?"

#### Rationale

1. **Consistent brand** - Jerry framework has established personality
2. **User delight** - Fun messaging improves onboarding experience
3. **Differentiation** - Sets Jerry apart from generic AI assistants
4. **Reference available** - Jerry persona guidelines provide clear direction

#### Implications

- **Positive:** Memorable, delightful user experience
- **Positive:** Consistent with existing Jerry personality
- **Negative:** Must avoid forced humor (per persona guide)
- **Follow-up required:** TASK-003 must reference Jerry persona guidelines

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Use Hybrid Platform-Aware Bootstrap Script | 2026-02-02 | ACCEPTED |
| D-002 | Use .context/ as canonical source location | 2026-02-02 | ACCEPTED |
| D-003 | Use Saucer Boy voice mode for /bootstrap skill | 2026-02-02 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-206-context-distribution-strategy.md](./EN-206-context-distribution-strategy.md) | Parent enabler |
| Research | [research-sync-strategies.md](./research-sync-strategies.md) | SPIKE-001 research findings |
| Discovery | [DISC-001-windows-junction-points-no-admin.md](./DISC-001-windows-junction-points-no-admin.md) | Key finding enabling D-001 |
| Reference | persona-voice-guide.md | Jerry personality guide |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-02T07:45:00Z | Claude | Decisions accepted, ready for implementation |
| 2026-02-02T07:30:00Z | Claude | Created decision document |

---

## Metadata

```yaml
id: "EN-206:DEC-001"
parent_id: "EN-206"
work_type: DECISION
title: "Sync Strategy Selection for Cross-Platform Context Distribution"
status: ACCEPTED
priority: CRITICAL
created_by: "Claude"
created_at: "2026-02-02T07:30:00Z"
updated_at: "2026-02-02T07:45:00Z"
decided_at: "2026-02-02T07:45:00Z"
participants: [Claude, User]
tags: [cross-platform, sync, bootstrap, windows, junction-points]
decision_count: 3
superseded_by: null
supersedes: null
```
