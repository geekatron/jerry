# Barrier 2 Handoff: nse → ps

> **Workflow:** jerry-persona-20260114
> **Barrier:** barrier-2 (Analysis Exchange)
> **From:** NASA SE Track (nse-architect-001)
> **To:** Problem-Solving Track (ps-synthesizer-001)
> **Date:** 2026-01-14

---

## Purpose

This handoff provides the Problem-Solving Track with key architecture decisions for the Persona Voice Guide synthesis. The ps-synthesizer-001 agent should use these findings to create a unified voice guide that integrates both the analysis recommendations and the technical implementation details.

---

## Key Insights from Persona Integration Architecture

### 1. Architecture Pattern: Persona Bounded Context

The architecture introduces a new bounded context following Hexagonal Architecture:

```
src/persona/
├── domain/           # MessageCatalog, VoiceMode, JerryLevel
├── application/      # Queries, Handlers, Ports
└── infrastructure/   # TOML adapters, presenters
```

**Synthesis Implication:** Voice guide should reference this structure for implementation guidance.

### 2. Personality Injection Points

Four key touchpoints where personality is injected:

| Injection Point | File Location | Voice Elements |
|-----------------|---------------|----------------|
| **Session Start Hook** | `session_start.py` | ASCII splash, greeting, quotes |
| **CLI Adapter** | `adapter.py` | Success/error/status messages |
| **Error Handling** | `exceptions.py` | Jerry severity levels |
| **CLAUDE.md/Skills** | Documentation | Tone guidelines |

**Synthesis Implication:** Voice guide should include examples for each injection point.

### 3. Three Voice Modes

| Mode | Character | Use Case |
|------|-----------|----------|
| **saucer_boy** | Playful, skiing metaphors | Default, most interactions |
| **professional** | Structured, helpful, no metaphors | Enterprise contexts |
| **minimal** | Just the facts | CI/CD, scripting |

**Synthesis Implication:** Voice guide should show same message in all three modes.

### 4. ASCII Splash Screen Specification

```
     _                        _____                                           _
    | | ___ _ __ _ __ _   _  |  ___| __ __ _ _ __ ___   _____      _____  _ __| | __
 _  | |/ _ \ '__| '__| | | | | |_ | '__/ _` | '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
| |_| |  __/ |  | |  | |_| | |  _|| | | (_| | | | | | |  __/\ V  V / (_) | |  |   <
 \___/ \___|_|  |_|   \__, | |_|  |_|  \__,_|_| |_| |_|\___| \_/\_/ \___/|_|  |_|\_\
                      |___/

                         "The best skier is the one having the most fun."
                                        - Shane McConkey

Session initialized. Let's make some turns.
```

**Synthesis Implication:** This ASCII art is ready for inclusion in the voice guide.

### 5. Message Catalog Structure

Messages stored in TOML with placeholder interpolation:

```toml
[session.start.success]
saucer_boy = "Session started: {session_id}. Fresh powder awaits!"
professional = "Session started successfully. ID: {session_id}"
minimal = "Started: {session_id}"

[jerry_level.mild]
saucer_boy = "Minor wobble - lost the line for a sec. Let me recover..."
professional = "Minor context gap detected. Recalibrating."
minimal = "Recovering."
```

**Synthesis Implication:** Voice guide should include full message catalog reference.

### 6. Configuration Schema

```toml
[persona]
enabled = true                    # Master toggle
voice_mode = "saucer_boy"         # saucer_boy | professional | minimal
show_splash = true                # ASCII art on session start
include_quotes = true             # Shane McConkey quotes
jerry_severity_enabled = true     # Context-rot warnings
```

Environment overrides: `JERRY_PERSONA_*`

**Synthesis Implication:** Voice guide should document configuration options.

### 7. Jerry Severity Spectrum (Technical)

| Level | Technical Trigger | User Message |
|-------|-------------------|--------------|
| **Mild** | Minor context gap | "Minor wobble - lost the line for a sec." |
| **Standard** | Lost thread | "Caught an edge there - full yard sale." |
| **Full** | Significant issue | "That run went sideways. Time to sideslip back up." |
| **Mega** | User intervention needed | "Red flag conditions. This needs human judgment." |

**Synthesis Implication:** Voice guide should map these to actual error conditions.

### 8. ADR Draft Included

The architecture includes a draft ADR (ADR-PERSONA-001) that:
- Documents the decision rationale
- Lists consequences (positive and negative)
- References all research artifacts

**Synthesis Implication:** Final voice guide should include or reference this ADR.

---

## Implementation Migration Path

The architecture recommends this phased implementation:

1. **Phase 1:** Configuration schema and defaults
2. **Phase 2:** Message catalog infrastructure
3. **Phase 3:** Wire presenter into session_start.py
4. **Phase 4:** Wire presenter into CLIAdapter
5. **Phase 5:** Add Jerry severity to exception handling
6. **Phase 6:** Update CLAUDE.md with voice guidelines

**Synthesis Implication:** Voice guide should align with this migration path.

---

## Testing Strategy Summary

| Test Type | Focus | Files |
|-----------|-------|-------|
| **Unit** | Message catalog, voice mode, Jerry level | `tests/persona/unit/` |
| **Integration** | CLI persona integration | `tests/persona/integration/` |
| **Contract** | Required keys exist for all voices | `tests/persona/contract/` |
| **BDD** | End-to-end persona presentation | `tests/persona/bdd/` |

**Synthesis Implication:** Voice guide should reference test requirements.

---

## Key Quotes for Voice Guide

From Shane McConkey (include in voice guide):

> "The best skier on the mountain is the one having the most fun."

> "If you're not having fun, you're doing it wrong."

> "I just try to make people laugh and push things a little bit."

> "Nobody said you can't."

---

## Source Artifact

Full architecture available at:
`nse/phase-2/nse-architect-001/persona-integration-architecture.md`

---

*Handoff generated for cross-pollinated pipeline barrier synchronization.*
