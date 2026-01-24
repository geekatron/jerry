# Architecture: Jerry Persona Integration

> **Agent:** nse-architect-001
> **Workflow:** jerry-persona-20260114
> **Pipeline:** nse (NASA Systems Engineering)
> **Phase:** 2 (Architecture)
> **Date:** 2026-01-14
> **Status:** COMPLETE

---

## L0: Executive Summary (ELI5)

The Jerry Framework needs a personality - specifically, the spirit of Shane McConkey channeled through his alter ego "Saucer Boy." This isn't about making the framework "cute" - it's about creating a voice that is technically excellent but never pompous, wise but willing to appear foolish, and capable but humble.

The architecture follows the framework's existing Hexagonal Architecture principles with a new **Persona** bounded context. The personality is implemented as a **Message Catalog** with injectable presentation adapters. This allows:

1. **Configuration-based control**: Users can enable/disable personality or switch to "professional" mode
2. **Layered message precedence**: Default messages can be overridden at project or user level
3. **Consistent voice**: All personality-infused output flows through a single `PersonaPresenter` port
4. **Testability**: Message selection and formatting are unit-testable without I/O

The key insight from the exploration phase is that Jerry's personality should embody the "Wise Fool" archetype - appearing playful while delivering profound results. Like Shane skiing on plastic saucers while performing world-class maneuvers, Jerry should be capable of impressive things while never pretending to be more important than it is.

---

## L1: Architecture Design

### 1. Personality Injection Points

Based on analysis of the existing codebase, personality should be injected at these key touchpoints:

```
                           PERSONALITY INJECTION POINTS
    ============================================================================

    +------------------------+        +-------------------------+
    |   Session Start Hook   |------->|  ASCII Splash Screen    |
    |  (session_start.py)    |        |  (configurable)         |
    +------------------------+        +-------------------------+
              |
              v
    +------------------------+        +-------------------------+
    |   CLI Adapter          |------->|  Success Messages       |
    |   (adapter.py)         |        |  Error Messages         |
    +------------------------+        |  Status Messages        |
              |                       +-------------------------+
              v
    +------------------------+        +-------------------------+
    |   Error Handling       |------->|  Jerry Moment Levels    |
    |   (exceptions.py)      |        |  (Mild/Standard/Full)   |
    +------------------------+        +-------------------------+
              |
              v
    +------------------------+        +-------------------------+
    |   CLAUDE.md / Skills   |------->|  Voice Consistency      |
    |   (documentation)      |        |  (tone, metaphors)      |
    +------------------------+        +-------------------------+
```

#### 1.1 Session Start Hook (Primary)

**Location:** `src/interface/cli/session_start.py`

This is the first user touchpoint and ideal for the ASCII splash screen. Current output:
```
Jerry Framework initialized. See CLAUDE.md for context.
```

Persona-enhanced output (when enabled):
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

#### 1.2 CLI Adapter Messages

**Location:** `src/interface/cli/adapter.py`

Current messages are functional but dry:
```python
print("Error: Session handlers not configured")
print(f"Session started: {session_id}")
print("No active session.")
```

Persona-enhanced alternatives:
```python
# Errors
"Hmm, looks like the bindings aren't set up right. Session handlers need configuring."

# Success
f"Session started: {session_id}. Fresh powder awaits!"

# Status
"No active session - you're still in the lodge. Try 'jerry session start' to hit the slopes."
```

#### 1.3 Error Messages (Context Severity)

**Location:** `src/shared_kernel/exceptions.py` + new `src/persona/domain/`

Implement the "Jerry Spectrum" from the PS track research:

| Level | Description | Example Message |
|-------|-------------|-----------------|
| Mild Jerry | Minor context gap | "Lost the thread there for a sec - let me re-orient." |
| Standard Jerry | Lost thread | "Full yard sale moment. Let's gather up the gear and try again." |
| Full Jerry | Significant issue | "That run didn't go as planned. We should probably reassess the approach." |
| Mega Jerry | User intervention needed | "Red flag conditions. This needs human judgment before proceeding." |

#### 1.4 CLAUDE.md and Skills

**Locations:**
- `CLAUDE.md` (root)
- `skills/*/SKILL.md`

These are natural language interfaces. Voice consistency comes from:
1. System prompt sections defining personality traits
2. Example phrasing patterns
3. Tone guidelines

### 2. Configuration Model

#### 2.1 Configuration Schema (TOML)

```toml
# .jerry/config.toml or projects/PROJ-*//.jerry/config.toml

[persona]
# Master enable/disable for personality
enabled = true

# Voice mode: "saucer_boy" (default), "professional", "minimal"
voice_mode = "saucer_boy"

# Show ASCII splash on session start
show_splash = true

# Include Shane quotes in certain outputs
include_quotes = true

# Jerry severity messaging (context-rot warnings)
jerry_severity_enabled = true

# Message catalog override path (optional)
# message_catalog_path = "custom/messages.toml"

[persona.professional]
# Settings when voice_mode = "professional"
# Disables skiing metaphors, keeps structured helpful tone

[persona.minimal]
# Settings when voice_mode = "minimal"
# Just the facts, no embellishment
```

#### 2.2 Environment Variable Overrides

Following existing `JERRY_*` prefix convention:

```bash
JERRY_PERSONA_ENABLED=false          # Disable personality
JERRY_PERSONA_VOICE_MODE=professional # Switch to professional voice
JERRY_PERSONA_SHOW_SPLASH=false      # Suppress ASCII splash
```

#### 2.3 Configuration Precedence

Follows existing `LayeredConfigAdapter` pattern:

```
1. Environment Variables (JERRY_PERSONA_*)     [Highest]
2. Project Config (projects/PROJ-*/.jerry/config.toml)
3. Root Config (.jerry/config.toml)
4. Code Defaults (persona enabled, saucer_boy mode)   [Lowest]
```

### 3. Message Catalog

#### 3.1 Catalog Structure

Create a new domain concept for message management:

```
src/
  persona/
    __init__.py
    domain/
      __init__.py
      message_catalog.py    # MessageCatalog aggregate
      message_entry.py      # MessageEntry entity
      voice_mode.py         # VoiceMode enum
      jerry_level.py        # JerryLevel enum
    application/
      __init__.py
      queries/
        get_message_query.py
      handlers/
        get_message_handler.py
      ports/
        primary/
          ipersona_presenter.py   # Port for message presentation
        secondary/
          imessage_repository.py  # Port for message storage
    infrastructure/
      adapters/
        toml_message_repository.py  # TOML-based message storage
        persona_presenter_adapter.py # Presentation implementation
```

#### 3.2 Message Entry Format

```toml
# src/persona/infrastructure/messages/saucer_boy.toml

[session.start.success]
saucer_boy = "Session started: {session_id}. Fresh powder awaits!"
professional = "Session started successfully. ID: {session_id}"
minimal = "Started: {session_id}"

[session.end.success]
saucer_boy = "Session wrapped up: {session_id}. Nice lines out there!"
professional = "Session ended. ID: {session_id}"
minimal = "Ended: {session_id}"

[error.validation]
saucer_boy = "Whoops - '{field}' went off-piste: {message}"
professional = "Validation error for '{field}': {message}"
minimal = "{field}: {message}"

[error.not_found]
saucer_boy = "Can't find {entity_type} '{entity_id}' - it's like looking for your skis after a yard sale."
professional = "{entity_type} '{entity_id}' not found"
minimal = "Not found: {entity_id}"

[jerry_level.mild]
saucer_boy = "Minor wobble - lost the line for a sec. Let me recover..."
professional = "Minor context gap detected. Recalibrating."
minimal = "Recovering."

[jerry_level.standard]
saucer_boy = "Caught an edge there - full yard sale. Gathering gear..."
professional = "Context thread lost. Reinitializing state."
minimal = "Resetting."

[jerry_level.full]
saucer_boy = "That run went sideways. Time to sideslip back up and try a different line."
professional = "Significant state issue. Recommending new approach."
minimal = "Error. Retry required."

[jerry_level.mega]
saucer_boy = "Red flag conditions, friend. This needs human eyes before we proceed."
professional = "Critical issue requiring user intervention."
minimal = "STOP. User input required."
```

#### 3.3 Splash Screen Art

```toml
# src/persona/infrastructure/messages/splash.toml

[splash.default]
art = '''
     _                        _____                                           _
    | | ___ _ __ _ __ _   _  |  ___| __ __ _ _ __ ___   _____      _____  _ __| | __
 _  | |/ _ \ '__| '__| | | | | |_ | '__/ _` | '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
| |_| |  __/ |  | |  | |_| | |  _|| | | (_| | | | | | |  __/\ V  V / (_) | |  |   <
 \___/ \___|_|  |_|   \__, | |_|  |_|  \__,_|_| |_| |_|\___| \_/\_/ \___/|_|  |_|\_\
                      |___/
'''
tagline = '"The best skier is the one having the most fun." - Shane McConkey'
greeting = "Session initialized. Let's make some turns."

[splash.minimal]
art = ""
tagline = ""
greeting = "Jerry Framework initialized."

[splash.professional]
art = ""
tagline = ""
greeting = "Jerry Framework v0.1.0 initialized. Run 'jerry --help' for commands."
```

### 4. ASCII Art Integration

#### 4.1 Display Location

The ASCII splash should display at session start hook, which is the natural entry point for Claude Code sessions.

#### 4.2 Display Logic

```python
# src/interface/cli/session_start.py (modified)

def display_splash(config: IConfigurationProvider, presenter: IPersonaPresenter) -> None:
    """Display ASCII splash screen based on configuration.

    Args:
        config: Configuration provider
        presenter: Persona presenter port
    """
    if not config.get_bool("persona.show_splash", default=True):
        return

    if not config.get_bool("persona.enabled", default=True):
        return

    voice_mode = config.get_string("persona.voice_mode", default="saucer_boy")

    splash_data = presenter.get_splash(voice_mode)
    if splash_data.art:
        print(splash_data.art)
    if splash_data.tagline:
        print(f"\n                         {splash_data.tagline}")
    if splash_data.greeting:
        print(f"\n{splash_data.greeting}")
```

#### 4.3 Configuration Options

```toml
[persona]
# Show the full ASCII art splash
show_splash = true

# Alternative: show_splash = false just prints the greeting
```

### 5. Voice Consistency

#### 5.1 Voice Mode Definitions

```python
# src/persona/domain/voice_mode.py

from enum import Enum, auto


class VoiceMode(Enum):
    """Voice modes for Jerry Framework persona.

    SAUCER_BOY: Playful, skiing metaphors, Shane McConkey spirit
    PROFESSIONAL: Structured, helpful, no metaphors
    MINIMAL: Just the facts, no embellishment
    """
    SAUCER_BOY = auto()
    PROFESSIONAL = auto()
    MINIMAL = auto()

    @classmethod
    def from_string(cls, value: str) -> "VoiceMode":
        """Convert string to VoiceMode.

        Args:
            value: String value (case-insensitive)

        Returns:
            Matching VoiceMode, defaults to SAUCER_BOY
        """
        mapping = {
            "saucer_boy": cls.SAUCER_BOY,
            "professional": cls.PROFESSIONAL,
            "minimal": cls.MINIMAL,
        }
        return mapping.get(value.lower(), cls.SAUCER_BOY)
```

#### 5.2 Consistency Guidelines (for CLAUDE.md)

Add to CLAUDE.md:

```markdown
## Persona: Saucer Boy Voice

Jerry Framework's personality is inspired by Shane McConkey's alter ego "Saucer Boy" -
technically brilliant but never pompous, capable but humble, wise but willing to appear foolish.

### Voice Guidelines

**DO:**
- Use skiing/mountain metaphors naturally (not forced)
- Self-deprecate when appropriate ("I'm just an AI in a cape")
- Acknowledge when something is hard or weird
- Find joy in problem-solving
- Be honest about limitations

**DON'T:**
- Take yourself too seriously
- Use corporate-speak or buzzwords
- Pretend to be human
- Mock users (only mock yourself)
- Sacrifice accuracy for humor

### Example Phrasings

| Situation | Instead of | Try |
|-----------|------------|-----|
| Success | "Task completed successfully" | "Done! That was smoother than expected." |
| Error | "Error: Invalid input" | "That input took a wrong turn. Let's try again." |
| Confusion | "Unable to process request" | "I got a bit turned around there. Can you clarify?" |
| Warning | "Warning: This may cause issues" | "Heads up - this line looks sketchy. Want to scout it first?" |
```

### 6. Testing Strategy

#### 6.1 Unit Tests

```
tests/
  persona/
    unit/
      domain/
        test_message_catalog.py     # Catalog loading, key lookup
        test_voice_mode.py          # Mode parsing, defaults
        test_jerry_level.py         # Level classification
      application/
        test_get_message_handler.py # Message retrieval logic
      infrastructure/
        test_toml_message_repository.py  # TOML parsing
        test_persona_presenter_adapter.py # Presentation logic
```

**Test Cases:**

```python
# tests/persona/unit/domain/test_message_catalog.py

def test_get_message_returns_correct_voice():
    """Message catalog returns voice-appropriate message."""
    catalog = MessageCatalog.load_default()

    saucer = catalog.get("session.start.success", VoiceMode.SAUCER_BOY)
    professional = catalog.get("session.start.success", VoiceMode.PROFESSIONAL)

    assert "powder" in saucer.lower()
    assert "powder" not in professional.lower()


def test_get_message_with_placeholders():
    """Message catalog interpolates placeholders."""
    catalog = MessageCatalog.load_default()

    message = catalog.get_formatted(
        "session.start.success",
        VoiceMode.SAUCER_BOY,
        session_id="TEST-001"
    )

    assert "TEST-001" in message
    assert "powder" in message.lower()


def test_missing_key_returns_fallback():
    """Missing key returns professional mode fallback."""
    catalog = MessageCatalog.load_default()

    message = catalog.get("nonexistent.key", VoiceMode.SAUCER_BOY)

    assert message is None or "nonexistent.key" in message
```

#### 6.2 Integration Tests

```python
# tests/persona/integration/test_cli_persona_integration.py

def test_session_start_shows_splash_when_enabled(tmp_path):
    """Session start displays ASCII splash when enabled."""
    config = {
        "persona": {
            "enabled": True,
            "show_splash": True,
            "voice_mode": "saucer_boy"
        }
    }
    write_config(tmp_path / ".jerry" / "config.toml", config)

    result = run_session_start(cwd=tmp_path)

    assert "Jerry" in result.stdout  # ASCII art contains "Jerry"
    assert "McConkey" in result.stdout  # Quote attribution


def test_session_start_hides_splash_when_disabled(tmp_path):
    """Session start suppresses splash when disabled."""
    config = {
        "persona": {
            "enabled": True,
            "show_splash": False
        }
    }
    write_config(tmp_path / ".jerry" / "config.toml", config)

    result = run_session_start(cwd=tmp_path)

    assert "McConkey" not in result.stdout
    assert "initialized" in result.stdout.lower()
```

#### 6.3 Contract Tests

```python
# tests/persona/contract/test_message_catalog_contract.py

def test_all_required_keys_exist():
    """Message catalog contains all required keys."""
    catalog = MessageCatalog.load_default()
    required_keys = [
        "session.start.success",
        "session.end.success",
        "error.validation",
        "error.not_found",
        "jerry_level.mild",
        "jerry_level.standard",
        "jerry_level.full",
        "jerry_level.mega",
    ]

    for key in required_keys:
        assert catalog.has(key), f"Missing required key: {key}"


def test_all_voices_defined_for_required_keys():
    """All voice modes have definitions for required keys."""
    catalog = MessageCatalog.load_default()
    required_keys = ["session.start.success", "error.validation"]

    for key in required_keys:
        for mode in VoiceMode:
            message = catalog.get(key, mode)
            assert message is not None, f"Missing {mode.name} for {key}"
```

#### 6.4 BDD Scenarios

```gherkin
# tests/persona/bdd/features/persona_presentation.feature

Feature: Persona Presentation
  As a Jerry Framework user
  I want personality-infused messages
  So that using the framework is enjoyable

  Scenario: Session start with Saucer Boy voice
    Given persona is enabled
    And voice mode is "saucer_boy"
    When I start a new session
    Then I should see the ASCII splash art
    And I should see a Shane McConkey quote
    And the greeting should mention "turns" or "powder"

  Scenario: Session start with professional voice
    Given persona is enabled
    And voice mode is "professional"
    When I start a new session
    Then I should NOT see ASCII splash art
    And I should see a structured initialization message

  Scenario: Persona disabled entirely
    Given persona is disabled
    When I start a new session
    Then I should see minimal functional output
    And no skiing metaphors should appear

  Scenario: Error message with Jerry level
    Given persona is enabled
    And jerry severity messaging is enabled
    When a "mild" context issue occurs
    Then the error message should mention "wobble" or "recover"
    And the message should be encouraging, not alarming
```

---

## L2: Implementation Recommendations

### File Locations

Create the following new files:

```
src/
  persona/
    __init__.py
    domain/
      __init__.py
      message_catalog.py
      message_entry.py
      voice_mode.py
      jerry_level.py
      splash_data.py
    application/
      __init__.py
      queries/
        __init__.py
        get_message_query.py
        get_splash_query.py
      handlers/
        __init__.py
        get_message_handler.py
        get_splash_handler.py
      ports/
        __init__.py
        primary/
          __init__.py
          ipersona_presenter.py
        secondary/
          __init__.py
          imessage_repository.py
    infrastructure/
      __init__.py
      adapters/
        __init__.py
        toml_message_repository.py
        persona_presenter_adapter.py
      messages/
        saucer_boy.toml
        professional.toml
        minimal.toml
        splash.toml

tests/
  persona/
    __init__.py
    unit/
      ... (as described above)
    integration/
      ...
    contract/
      ...
    bdd/
      features/
        persona_presentation.feature
```

### Configuration Schema (Full)

```toml
# Add to default config in LayeredConfigAdapter

[persona]
# Master enable/disable - turns off all personality features
enabled = true

# Voice mode selection
# Options: "saucer_boy" | "professional" | "minimal"
voice_mode = "saucer_boy"

# ASCII splash screen at session start
show_splash = true

# Include inspirational quotes from Shane McConkey
include_quotes = true

# Jerry severity messaging for context-rot warnings
jerry_severity_enabled = true

# Custom message catalog path (relative to project root)
# Allows users to override default messages
# message_catalog_path = ""
```

### Bootstrap Wiring

Add to `src/bootstrap.py`:

```python
def create_persona_presenter() -> PersonaPresenterAdapter:
    """Create persona presenter with proper configuration.

    Returns:
        Configured PersonaPresenterAdapter instance
    """
    config = create_config_provider()
    message_repo = TomlMessageRepository.load_default()

    return PersonaPresenterAdapter(
        config=config,
        message_repository=message_repo,
    )
```

### Migration Path

1. **Phase 1:** Add configuration schema and defaults (no behavior change)
2. **Phase 2:** Add message catalog infrastructure
3. **Phase 3:** Wire presenter into session_start.py
4. **Phase 4:** Wire presenter into CLIAdapter
5. **Phase 5:** Add Jerry severity to exception handling
6. **Phase 6:** Update CLAUDE.md with voice guidelines

---

## ADR Draft

### ADR-PERSONA-001: Jerry Framework Personality Integration

**Status:** PROPOSED

**Context:**

The Jerry Framework needs a consistent personality that makes interaction enjoyable while maintaining technical accuracy. The personality is inspired by Shane McConkey and his alter ego "Saucer Boy" - technically excellent but never pompous, wise but willing to appear foolish.

Users may prefer different levels of personality:
- Some want full Saucer Boy mode with skiing metaphors and ASCII art
- Some want professional, structured messages
- Some want minimal output with just the facts

**Decision:**

We will implement a **Persona Bounded Context** following Hexagonal Architecture:

1. **Message Catalog** stores all personality-infused messages in TOML format
2. **Voice Mode** enum controls message selection (saucer_boy, professional, minimal)
3. **Persona Presenter** port provides unified interface for message presentation
4. **Configuration** controls all personality features via `[persona]` section

The implementation follows existing patterns:
- Configuration via `LayeredConfigAdapter`
- Port/Adapter pattern for message storage and presentation
- Unit tests for all domain logic

**Consequences:**

Positive:
- Consistent voice across all framework touchpoints
- Users can customize or disable personality
- Easy to update messages without code changes
- Testable message selection logic

Negative:
- Additional complexity in message handling
- TOML file maintenance required
- Risk of forced/unnatural metaphors if not carefully written

**References:**
- Shane McConkey exploration: `nse/phase-1/nse-explorer-001/shane-mcconkey-exploration.md`
- Jerry of the Day research: `ps/phase-1/ps-researcher-001/jerry-of-the-day-research.md`
- Cross-pollination handoff: `barriers/barrier-1/ps-to-nse-handoff.md`

---

## References

### Source Artifacts

1. **Shane McConkey Exploration**
   `projects/PROJ-007-jerry-bugs/orchestration/jerry-persona-20260114/nse/phase-1/nse-explorer-001/shane-mcconkey-exploration.md`

2. **Cross-Pollinated Insights (PS to NSE)**
   `projects/PROJ-007-jerry-bugs/orchestration/jerry-persona-20260114/barriers/barrier-1/ps-to-nse-handoff.md`

### Existing Framework Files Analyzed

- `src/interface/cli/session_start.py` - Session start hook
- `src/interface/cli/adapter.py` - CLI adapter
- `src/interface/cli/main.py` - CLI entry point
- `src/infrastructure/adapters/configuration/layered_config_adapter.py` - Configuration system
- `src/shared_kernel/exceptions.py` - Exception hierarchy

### Key Quotes (Shane McConkey)

- "The best skier on the mountain is the one having the most fun."
- "If you're not having fun, you're doing it wrong."
- "I just try to make people laugh and push things a little bit."
- "Nobody said you can't."

---

## Architecture Metadata

| Field | Value |
|-------|-------|
| Agent | nse-architect-001 |
| Pipeline | nse |
| Phase | 2 (Architecture) |
| Workflow | jerry-persona-20260114 |
| Output Type | Architecture Design Document |
| Sections | 6 (L0 Summary, L1 Design, L2 Recommendations, ADR Draft) |
| Status | COMPLETE |

---

*"Like Saucer Boy skiing world-class lines in his underpants, Jerry should be capable of impressive things while never pretending to be more important than it is."*
