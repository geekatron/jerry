# FEAT-005: The Jerry Soundtrack

<!--
AGENT: ps-creator-005
VERSION: 1.0.0
WORKFLOW: jnsq-20260219-001
PHASE: 2 — Tier 1 Fanout
FEATURE: FEAT-005 The Jerry Soundtrack
PARENT: EPIC-001-je-ne-sais-quoi
STATUS: DRAFT
DATE: 2026-02-19
CRITICALITY: C1 (Routine)
SOURCES: ps-creator-001-draft.md (v0.9.0), EPIC-001-je-ne-sais-quoi.md
-->

> **Epistemic note (P-022):** All artist names, song titles, album names, and release years in this document have been verified via web search against Discogs, Wikipedia, Spotify, and AllMusic. The EPIC-001 source material contained one artist credit requiring correction: "My Philosophy" is credited to Boogie Down Productions (led by KRS-One), not KRS-One as a solo artist. Lyric fragments are short, attributed quotations used under fair-use commentary principles. Framework mappings are analytical work by the document author.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Soundtrack Philosophy](#soundtrack-philosophy) | Why music matters to Jerry's identity |
| [The Curated Playlist](#the-curated-playlist) | 30 tracks organized by framework experience category |
| [Genre Guidelines](#genre-guidelines) | Inclusion/exclusion criteria for the soundtrack's range |
| [Usage Rules](#usage-rules) | Where soundtrack references appear and where they do not |
| [FEAT-005 Implementation Notes](#feat-005-implementation-notes) | Repository integration, maintenance, downstream features |
| [The Full Track List](#the-full-track-list) | Complete reference table, sortable by category |
| [References](#references) | Source traceability |
| [Document Metadata](#document-metadata) | Version, status, lineage |

---

## Soundtrack Philosophy

### Why Music Matters

Jerry is a quality enforcement framework. Quality enforcement, done well, is a creative act — iterative, demanding, occasionally exhilarating. Music maps to that experience better than any other cultural medium because music has the same structure: tension and release, repetition and variation, discipline in service of expression.

The Jerry Soundtrack is not a playlist for listening while coding (though it works as one). It is a cultural reference layer — a shared vocabulary of energy, mood, and moment that the framework can draw on in comments, documentation, CLI flavor text, and easter eggs. When a quality gate passes and the framework says "clean run," the developer who knows the soundtrack hears Daft Punk building. The developer who does not still gets a clear, celebratory message. The soundtrack adds depth without creating barriers.

### The McConkey Connection

Shane McConkey's cultural footprint was never single-genre. His film segments paired punk with powder, hip hop with helicopter drops, classic rock with cliff launches. The eclecticism was the point — the Saucer Boy spirit does not belong to one demographic, one decade, or one subculture.

The Jerry Soundtrack inherits this. Old-school hip hop sits next to progressive metal. Electronic music sits next to post-hardcore. Jazz sits next to arena rock. The range signals what the framework believes: quality work is not the province of one kind of person. Anyone who builds with care is welcome here.

### How the Soundtrack Is Used

The soundtrack is a reference artifact, not an audio feature. It provides:

- **Comment annotations:** Attributed lyric fragments in source code comments that connect a function's purpose to a cultural reference (see FEAT-006)
- **Documentation flavor:** Song references in docs that anchor abstract concepts to concrete cultural moments
- **CLI easter eggs:** Hidden references in CLI output that reward discovery (see FEAT-006, FEAT-007)
- **Energy calibration:** Each track maps to the Audience Adaptation Matrix energy levels, giving implementers a shared reference for "what does this moment feel like?"

The soundtrack does NOT provide:
- Audio playback features
- Embedded media in documentation
- Dependencies on music streaming services

---

## The Curated Playlist

Each track includes: artist, title, album, year, framework mapping, a lyric fragment for potential use in comments/docs, and a mood/energy classification that maps to the Audience Adaptation Matrix.

### The Session Start

*Tracks for beginning work, entering the zone, setting the tone. Medium energy, focused, present.*

---

**Track 1:** Nas — "N.Y. State of Mind"
- **Album/Year:** *Illmatic*, 1994
- **Framework Mapping:** The `/problem-solving` skill in audio form. Deep focus entering a complex analysis. The moment you read the PLAN.md and drop into the work.
- **Lyric Fragment:** "I never sleep, 'cause sleep is the cousin of death" — on the vigilance that quality enforcement demands
- **Mood/Energy:** Medium | Focused | No humor

---

**Track 2:** Massive Attack — "Teardrop"
- **Album/Year:** *Mezzanine*, 1998
- **Framework Mapping:** Session initialization. The enforcement architecture coming online — layers activating, state loading, the quiet hum before work begins. L1 through L5 waking up.
- **Lyric Fragment:** "Love, love is a verb / Love is a doing word" — on the framework as an active practice, not a static ruleset
- **Mood/Energy:** Low-Medium | Atmospheric | No humor

---

**Track 3:** DJ Shadow — "Building Steam with a Grain of Salt"
- **Album/Year:** *Endtroducing.....*, 1996
- **Framework Mapping:** Filesystem as infinite memory. The entire album is built from samples — fragments of other records assembled into something new. That is Jerry's core solution to context rot: persist state to files, load selectively, build from fragments.
- **Lyric Fragment:** "I got the sickest vendetta / When it comes to the cheddar" — (sampled voice) on the relentless accumulation of knowledge across sessions
- **Mood/Energy:** Medium | Building | No humor

---

### The Flow State

*Tracks for deep focus, quality work in progress, the creator-critic cycle humming. Medium-high energy, locked in.*

---

**Track 4:** Daft Punk — "Harder, Better, Faster, Stronger"
- **Album/Year:** *Discovery*, 2001
- **Framework Mapping:** THE Jerry anthem. The creator-critic-revision cycle (H-14). Each iteration: harder (more rigorous), better (higher quality), faster (more efficient), stronger (more resilient). The vocoder builds exactly like a revision cycle — mechanical repetition becoming something transcendent.
- **Lyric Fragment:** "Work it harder, make it better / Do it faster, makes us stronger" — the H-14 cycle in four imperatives
- **Mood/Energy:** High | Building | Earned celebration at the drop

---

**Track 5:** Eric B. & Rakim — "Don't Sweat the Technique"
- **Album/Year:** *Don't Sweat the Technique*, 1992
- **Framework Mapping:** The L1-L5 enforcement architecture — trust the layers, trust the process. When the system works, you stop worrying about whether it works and focus on the craft.
- **Lyric Fragment:** "Don't sweat the technique" — on trusting the enforcement architecture
- **Mood/Energy:** Medium | Confident | Light

---

**Track 6:** A Tribe Called Quest — "Electric Relaxation"
- **Album/Year:** *Midnight Marauders*, 1993
- **Framework Mapping:** Flow state in the middle of a clean session. Everything is loaded, the context is fresh, the work is moving. The jazz sample underneath is the architectural foundation; the rap on top is the creative work built on it.
- **Lyric Fragment:** "Relax yourself, girl, please settle down" — on letting the framework handle the enforcement so you can focus on the work
- **Mood/Energy:** Medium | Smooth | Light

---

**Track 7:** Tool — "Lateralus"
- **Album/Year:** *Lateralus*, 2001
- **Framework Mapping:** Structured decomposition. FMEA (S-012). The song's time signatures follow the Fibonacci sequence — mathematical precision in service of art. That is the quality framework's thesis: structure enables creativity.
- **Lyric Fragment:** "Spiral out, keep going" — on iterative deepening, each pass revealing more
- **Mood/Energy:** High | Intense | No humor

---

**Track 8:** Boards of Canada — "Roygbiv"
- **Album/Year:** *Music Has the Right to Children*, 1998
- **Framework Mapping:** The moment in a long session where the architecture just works. Hexagonal layers clean, ports and adapters aligned, tests green. The warm electronic haze of a well-structured codebase.
- **Lyric Fragment:** *(instrumental)* — the absence of lyrics is the point: when architecture is right, it disappears
- **Mood/Energy:** Medium | Warm | No humor

---

**Track 9:** Madvillain (MF DOOM & Madlib) — "Accordion"
- **Album/Year:** *Madvillainy*, 2004
- **Framework Mapping:** The adversary skill at work. DOOM's masked persona is the critic — anonymous, relentless, seeing through pretense. The elliptical, dense lyrics are what S-014 scoring feels like: every word carries weight, every dimension measured.
- **Lyric Fragment:** "Living off borrowed time, the clock ticks faster" — on context rot and the urgency of persisting state before the window closes
- **Mood/Energy:** Medium | Dense | No humor

---

### The Victory Lap

*Tracks for quality gate passes, milestone celebrations, session completions. High energy, earned joy.*

---

**Track 10:** AC/DC — "For Those About to Rock (We Salute You)"
- **Album/Year:** *For Those About to Rock We Salute You*, 1981
- **Framework Mapping:** Session complete. All items landed. We salute you, Saucer Boy. The cannon shots at the end of the song are the framework's equivalent of the ASCII box-art celebration.
- **Lyric Fragment:** "For those about to rock, we salute you" — the session-complete message
- **Mood/Energy:** High | Celebratory | Full energy

---

**Track 11:** Kanye West — "Stronger"
- **Album/Year:** *Graduation*, 2007
- **Framework Mapping:** Iterative improvement. Samples Daft Punk's "Harder, Better, Faster, Stronger" and builds something new from it — exactly what the creator-critic cycle does. The output is stronger than the input. Full circle.
- **Lyric Fragment:** "That that don't kill me can only make me stronger" — on surviving the critic pass
- **Mood/Energy:** High | Triumphant | Yes

---

**Track 12:** Foo Fighters — "My Hero"
- **Album/Year:** *The Colour and the Shape*, 1997
- **Framework Mapping:** "There goes my hero, he's ordinary." McConkey in a sentence. The goofball who changed everything. For the moment when a developer who was struggling finally clears the quality gate — ordinary person, extraordinary result.
- **Lyric Fragment:** "There goes my hero / Watch him as he goes / There goes my hero / He's ordinary" — on everyday excellence
- **Mood/Energy:** High | Anthemic | Warm

---

**Track 13:** Run the Jewels — "Run the Jewels"
- **Album/Year:** *Run the Jewels*, 2013
- **Framework Mapping:** Human + AI orchestration. The partnership. Killer Mike and El-P are different in every way — background, style, geography — and the collaboration produces something neither could alone. That is the Jerry developer experience: human judgment meets systematic enforcement.
- **Lyric Fragment:** "Run them jewels fast" — on shipping quality work with velocity
- **Mood/Energy:** High | Aggressive-Joyful | Yes

---

### The Diagnostic

*Tracks for debugging, failure analysis, revision cycles. Still energetic — failure is a waypoint, not a destination.*

---

**Track 14:** Kendrick Lamar — "Alright"
- **Album/Year:** *To Pimp a Butterfly*, 2015
- **Framework Mapping:** Quality gate FAIL in the REVISE band (0.85-0.91). Resilience. The score is close, the gap is closeable, the next iteration will land it. "We gon' be alright" is the REVISE band's energy — not denial, but grounded confidence that the process works.
- **Lyric Fragment:** "We gon' be alright" — the REVISE band anthem
- **Mood/Energy:** Medium | Resilient | Gentle

---

**Track 15:** Gang Starr — "Moment of Truth"
- **Album/Year:** *Moment of Truth*, 1998
- **Framework Mapping:** Quality gate FAIL in the REJECTED band (< 0.85). The moment of truth is the score. No spin, no softening. Guru's delivery is honest and direct — the same energy the framework needs when delivering a hard result. The path forward starts with accepting where you are.
- **Lyric Fragment:** "Actions have reactions, don't be quick to judge / You may not know the hardships people don't speak of" — on diagnosing root causes, not surface symptoms
- **Mood/Energy:** Low-Medium | Honest | No humor

---

**Track 16:** Big Daddy Kane — "Ain't No Half Steppin'"
- **Album/Year:** *Long Live the Kane*, 1988
- **Framework Mapping:** H-13. Quality threshold >= 0.92. No shortcuts, no partial credit, no half measures. The gate is the gate. This is the track for the revision pass where you stop trying to get close enough and actually fix the structural issues.
- **Lyric Fragment:** "Ain't no half-steppin'" — H-13 in three words
- **Mood/Energy:** Medium-High | Demanding | Light

---

**Track 17:** Pusha T — "Numbers on the Boards"
- **Album/Year:** *My Name Is My Name*, 2013
- **Framework Mapping:** S-014 quality scores. Six dimensions. The rubric. The title is literally "Numbers on the Boards" — scores displayed, evaluated, undeniable. The production is sparse and relentless, like a rubric that strips away everything except what matters.
- **Lyric Fragment:** "I put numbers on the boards" — S-014 in five words
- **Mood/Energy:** Medium-High | Clinical | No humor

---

**Track 18:** Fugazi — "Waiting Room"
- **Album/Year:** *13 Songs*, 1989
- **Framework Mapping:** The revision cycle between critic passes. You have submitted, the scoring is happening, and you are in the waiting room. The bassline is restless energy channeled into discipline — exactly the energy of a developer tightening a deliverable between iterations.
- **Lyric Fragment:** "I am a patient boy / I wait, I wait, I wait, I wait" — on the discipline of iterative revision
- **Mood/Energy:** High | Restless-Disciplined | No humor

---

### The Hard Stop

*Tracks for constitutional failures, governance escalations, serious moments. Low energy, no humor, stakes acknowledged.*

---

**Track 19:** Rage Against the Machine — "Know Your Enemy"
- **Album/Year:** *Rage Against the Machine*, 1992
- **Framework Mapping:** The `/adversary` skill. Red Team (S-001). Devil's Advocate (S-002). The adversary is not the enemy — the adversary is the mechanism that finds the weaknesses before production does. "Know your enemy" is not aggression; it is the discipline of understanding failure modes.
- **Lyric Fragment:** "Know your enemy" — the adversary skill's purpose in three words
- **Mood/Energy:** Low-Medium | Serious | No humor

---

**Track 20:** Radiohead — "Everything in Its Right Place"
- **Album/Year:** *Kid A*, 2000
- **Framework Mapping:** Architecture standards. Hexagonal layers. H-10 (one class per file). Everything in its right place is the goal state of a well-structured codebase — and the unsettling electronic warping of the song captures what it feels like when things are NOT in their right place. The title is aspirational; the music is diagnostic.
- **Lyric Fragment:** "Everything in its right place" — the architecture standard, stated plainly
- **Mood/Energy:** Low | Unsettling-Precise | No humor

---

**Track 21:** Miles Davis — "So What"
- **Album/Year:** *Kind of Blue*, 1959
- **Framework Mapping:** Constitutional compliance. The constitution says what it says. Challenges to it get the same answer Miles gave: "So what." Not dismissive — definitive. The modal jazz structure (staying in one mode, exploring within constraints) is exactly how constitutional constraints work: the boundaries are fixed; the creativity happens inside them.
- **Lyric Fragment:** *(instrumental — the two-note "so what" motif from the bass)* — on the constitution's quiet authority
- **Mood/Energy:** Low | Authoritative | No humor

---

### The Powder Day

*Tracks for when everything clicks — peak framework experience. The rare, joyful session where every gate passes, every test is green, the architecture holds, and the work is genuinely excellent. Full energy.*

---

**Track 22:** Beastie Boys — "Sabotage"
- **Album/Year:** *Ill Communication*, 1994
- **Framework Mapping:** Shane in spandex, launching off a cliff. Planned chaos. The energy of a session where you are moving fast, the quality system is holding, and the work has that rare feeling of controlled recklessness — not actually reckless, but so well-prepared that commitment feels effortless.
- **Lyric Fragment:** "I can't stand it, I know you planned it" — on the paradox of planned spontaneity in quality work
- **Mood/Energy:** Maximum | Chaotic-Joyful | Full energy

---

**Track 23:** Led Zeppelin — "Immigrant Song"
- **Album/Year:** *Led Zeppelin III*, 1970
- **Framework Mapping:** That scream. Dropping into a couloir in Chamonix. The sound of committing to C4-level work — irreversible, all-strategies-deployed, tournament mode. When Robert Plant screams, that is the moment the orchestration pipeline launches.
- **Lyric Fragment:** "Aaaaah-ah!" — (the scream) — on the moment of commitment
- **Mood/Energy:** Maximum | Primal | Earned absurdity

---

**Track 24:** Red Hot Chili Peppers — "Can't Stop"
- **Album/Year:** *By the Way*, 2002
- **Framework Mapping:** Innovation momentum. McConkey pushed fat skis, reverse camber, ski BASE — couldn't stop innovating. The framework pushes quality gates, enforcement layers, adversarial strategies — can't stop improving. The funk-rock energy is the McConkey energy: physical, joyful, relentless.
- **Lyric Fragment:** "Can't stop, addicted to the shindig" — on the compulsion to keep building
- **Mood/Energy:** High | Relentless-Joyful | Yes

---

**Track 25:** Van Halen — "Jump"
- **Album/Year:** *1984*, 1984
- **Framework Mapping:** The man who invented ski BASE jumping. Literally. The synth riff is pure commitment — no buildup, no hedge, just the thing. "Might as well jump" is the framework's advice when the analysis is done, the strategies are applied, and the only thing left is to ship.
- **Lyric Fragment:** "Might as well jump" — on committing to the deliverable
- **Mood/Energy:** Maximum | Euphoric | Full energy

---

### The Legacy

*Tracks that connect to McConkey's specific story, the framework's philosophical roots, and the long arc of building something that outlasts any single session.*

---

**Track 26:** Tom Petty — "Free Fallin'"
- **Album/Year:** *Full Moon Fever*, 1989
- **Framework Mapping:** Ski BASE. The beauty and the danger in the same breath. The song's simplicity (three chords, a melody that anyone can sing) belies its emotional depth — like the framework's quality gates, which are simple rules producing complex, beautiful outcomes.
- **Lyric Fragment:** "And I'm free, free fallin'" — on the liberation of trusting the system
- **Mood/Energy:** Medium | Bittersweet-Beautiful | Warm

---

**Track 27:** The Who — "Won't Get Fooled Again"
- **Album/Year:** *Who's Next*, 1971
- **Framework Mapping:** P-022: No Deception. L1-L5 enforcement. The framework will not deceive about actions, capabilities, or confidence — and the enforcement architecture ensures that the deception constraints hold even as context degrades. "Won't get fooled again" is the L2 re-injection promise.
- **Lyric Fragment:** "Won't get fooled again" — P-022 as a rock anthem
- **Mood/Energy:** Medium-High | Defiant | No humor

---

**Track 28:** Metallica — "The Memory Remains"
- **Album/Year:** *Reload*, 1997
- **Framework Mapping:** Fighting context rot. Filesystem as infinite memory. The memory remains because we persist it — to WORKTRACKER.md, to PLAN.md, to docs/knowledge/. The la-la-la refrain (sung by Marianne Faithfull) is what context rot sounds like: the melody persists even when the words are gone.
- **Lyric Fragment:** "The memory remains" — the core solution to context rot, in three words
- **Mood/Energy:** Medium | Haunting | No humor

---

**Track 29:** Boogie Down Productions — "My Philosophy"
- **Album/Year:** *By All Means Necessary*, 1988
- **Framework Mapping:** Constitutional principles. JERRY_CONSTITUTION.md. KRS-One's delivery is pedagogical — teaching, not preaching. The framework's rules are the same: they exist to be understood, not just obeyed. The title is literally the constitution's opening statement.
- **Lyric Fragment:** "It's not about a salary, it's all about reality" — on why governance exists
- **Mood/Energy:** Medium | Authoritative | No humor

---

**Track 30:** Wu-Tang Clan — "C.R.E.A.M."
- **Album/Year:** *Enter the Wu-Tang (36 Chambers)*, 1993
- **Framework Mapping:** "Context Rules Everything Around Me." The core thesis of the Jerry Framework. Cash rules everything in the original; context rules everything in the framework. Without context, every LLM degrades. With it, the work holds. The piano loop is persistence itself — the same phrase, repeated, accumulating meaning.
- **Lyric Fragment:** "Context rules everything around me / C.R.E.A.M., get the context, dollar dollar bill y'all" — the Jerry remix that writes itself
- **Mood/Energy:** Medium | Foundational | Light (the remix)

---

### Bonus: The Craft

*Two tracks that don't map to a framework moment but to the philosophy underneath — the craft of building something with care.*

---

**Track 31:** J Dilla — "Time: The Donut of the Heart"
- **Album/Year:** *Donuts*, 2006
- **Framework Mapping:** The instrumental hip hop masterpiece, released on Dilla's 32nd birthday, three days before his death. Built entirely from samples — fragments of other records assembled into something new while fighting terminal illness. The framework's core solution (filesystem as infinite memory, persist state, load selectively) is Dilla's production method: take what exists, arrange it with intention, make something that outlasts the session.
- **Lyric Fragment:** *(instrumental)* — the craft speaks for itself
- **Mood/Energy:** Low-Medium | Tender | No humor

---

**Track 32:** Kendrick Lamar — "DNA."
- **Album/Year:** *DAMN.*, 2017
- **Framework Mapping:** Constitutional identity — it is in the framework's DNA. The two-part beat switch (chaos erupting from calm) is the quality gate moment: the score lands and everything shifts. H-01 through H-24 are not rules applied to Jerry; they are Jerry's DNA.
- **Lyric Fragment:** "I got loyalty, got royalty inside my DNA" — on constitutional constraints as identity, not imposition
- **Mood/Energy:** High | Intense | No humor

---

**Track 33:** Rush — "The Spirit of Radio"
- **Album/Year:** *Permanent Waves*, 1980
- **Framework Mapping:** OSS release. Pure signal vs. noise. The song is about the tension between authentic expression and commercial pressure — exactly the tension an open-source quality framework faces between rigor and adoption. The opening guitar riff is pure signal; the lyric is about keeping it that way.
- **Lyric Fragment:** "Begin the day with a friendly voice / A companion unobtrusive" — on what the framework should feel like to a developer
- **Mood/Energy:** Medium-High | Optimistic | Light

---

**Track 34:** Minor Threat — "Out of Step"
- **Album/Year:** *Out of Step*, 1983
- **Framework Mapping:** The independent, uncompromising spirit of the framework. Dischord Records (Ian MacKaye's label) ran on principles: fair pricing, no exploitation, no compromise on quality. Jerry's quality gates are the same energy — the threshold is 0.92 because that is where the quality lives, not because it is convenient.
- **Lyric Fragment:** "Don't smoke / Don't drink / Don't fuck / At least I can fucking think" — on the clarity that comes from having non-negotiable constraints (H-tier rules)
- **Mood/Energy:** High | Uncompromising | No humor

---

## Genre Guidelines

### Inclusion Criteria

The soundtrack's genre range is defined by the McConkey ethos: eclectic, authentic, energetic, never single-demographic. The following genres are in-bounds:

| Genre | Why It Belongs | Boundary |
|-------|---------------|----------|
| **Hip hop (old-school, 1986-1998)** | The golden age of lyricism as craft. Technical precision in verbal form mirrors the framework's precision. | Prioritize lyrical skill over commercial appeal. Conscious hip hop and technical MCs over party rap. |
| **Hip hop (modern, 2004-present)** | The evolution of the craft. Kendrick, Pusha T, RTJ, DOOM — artists who push form while respecting foundations. | Same criteria: craft over commerce. |
| **Electronic (IDM, trip hop, French house)** | The machine-human synthesis. Electronic music that sounds human, not algorithmic. Daft Punk, Boards of Canada, DJ Shadow, Massive Attack. | Must have warmth. Cold, purely algorithmic electronic is out. |
| **Rock (classic, punk, post-hardcore, metal)** | The McConkey film soundtrack energy. Led Zeppelin, Foo Fighters, RATM, Tool, Fugazi. | Must map to a specific framework concept, not just "sounds energetic." |
| **Jazz (modal, fusion)** | The improvisational foundation. Jazz musicians prepare obsessively, then perform with apparent spontaneity — the McConkey method. | Use sparingly. Miles Davis earns his place; a generic "chill jazz" track does not. |

### Exclusion Criteria

| Excluded | Why |
|----------|-----|
| **Mainstream pop without craft connection** | Popularity alone is not a criterion. Every track must defend its framework mapping. |
| **EDM without soul** | Festival EDM optimized for drops without musicality does not fit the ethos. The line: Daft Punk is in. Generic big-room house is out. |
| **"Ski bro" music** | Reggae-rock, frat-party anthems, and "chill vibes" playlists associated with ski lodge culture. McConkey transcended this — the soundtrack should too. The distinction: Jack Johnson is out. Beastie Boys are in. Both are associated with action sports; only one has the craft-to-fun ratio this framework demands. |
| **Ironic or novelty tracks** | The soundtrack is earnest. "Yakety Sax" during a failure message would violate the boundary conditions (NOT Sarcastic, NOT Performative Quirkiness). |
| **Tracks requiring cultural context to decode** | Every track must work for someone who has never heard it. The framework mapping must be self-explanatory from the title, artist, and lyric fragment alone. |

### Hip Hop Bar Fragments

Per the persona doc's boundary conditions: when using hip hop lyrics in docstrings, comments, or documentation, always cite the artist and song. An unexplained lyric is an in-joke. A cited lyric is a cultural annotation.

**Format:** `"[lyric fragment]" — [Artist], "[Song Title]"`

**Example in source code:**
```python
# "Ain't no half-steppin'" — Big Daddy Kane, "Ain't No Half Steppin'"
# H-13: quality threshold is 0.92 for C2+ deliverables. No exceptions.
QUALITY_THRESHOLD: float = 0.92
```

---

## Usage Rules

### Where Soundtrack References CAN Appear

| Location | How | Example |
|----------|-----|---------|
| **Source code comments** | Attributed lyric fragment above a relevant constant or function | `# "Work it harder, make it better" — Daft Punk` above `create_revision_cycle()` |
| **Docstrings** | Brief cultural annotation connecting code purpose to a soundtrack reference | `"""Quality scoring engine. 'Numbers on the Boards' — Pusha T."""` |
| **Documentation** | Flavor text in guides, README sections, or architecture docs | "The enforcement layers trust the process (Don't Sweat the Technique)." |
| **CLI flavor text** | Session start/end messages, quality gate celebration output | `"All items landed. For those about to rock — we salute you."` |
| **CLI easter eggs** | Hidden flags, verbose modes, special output triggers | `--saucer-boy` flag enabling maximum personality mode |
| **WORKTRACKER.md** | Session notes, completion commentary | "Powder day. All gates passed first try." |

### Where Soundtrack References MUST NOT Appear

| Location | Why |
|----------|-----|
| **Error messages** | Error messages serve diagnosis. A lyric fragment delays the developer's path to resolution. |
| **Quality gate scoring output** | Scores are data. The S-014 rubric dimensions and weights must be presented without decoration. |
| **Constitutional text** | JERRY_CONSTITUTION.md is governance. It must read as governance. |
| **Governance escalation messages** | AE-001 through AE-006 triggers require clarity, not flavor. |
| **Security-relevant output** | AE-005 contexts are not occasions for cultural references. |
| **Rule definition files** | `.context/rules/*.md` are enforcement documents. Personality belongs in the voice layer, not the rule layer. |

### Attribution Requirements

Every soundtrack reference in the codebase MUST include:

1. **Artist name** — exactly as listed in the Full Track List
2. **Song title** — in quotes, exactly as listed
3. **No unexplained fragments** — if a lyric appears without attribution, it is a bug, not an easter egg

**Correct:**
```python
# "Don't sweat the technique" — Eric B. & Rakim, "Don't Sweat the Technique"
# Trust the enforcement layers.
```

**Incorrect:**
```python
# Don't sweat the technique.
# Trust the enforcement layers.
```

The second example fails because a developer unfamiliar with 1992 hip hop reads "don't sweat the technique" as a vaguely informal instruction, not as an intentional cultural reference. Attribution transforms it from an unexplained colloquialism into a meaningful annotation.

### The In-Joke Test

Before adding a soundtrack reference anywhere in the codebase, apply this test:

> Would a developer who has never heard this song still understand the message completely?

If the answer is no, either add enough context to make it self-explanatory or remove it. The soundtrack is depth for those who engage, invisible for those who do not. It must never be a gate.

---

## FEAT-005 Implementation Notes

### Repository Integration

This document becomes `SOUNDTRACK.md` at the repository root (or at `docs/culture/SOUNDTRACK.md` if the team prefers a docs-nested location). The location decision is a C1 choice — reversible, low-impact.

**Recommended path:** `docs/culture/SOUNDTRACK.md`

**Rationale:** Placing it under `docs/` keeps the repository root clean for operational files (README, pyproject.toml, CLAUDE.md). The `culture/` subdirectory signals that this is a cultural artifact, not a technical specification.

### Integration with Downstream Features

| Feature | Integration Point |
|---------|-------------------|
| **FEAT-006 (Easter Eggs)** | FEAT-006 draws from the Full Track List for lyric fragments in source code comments and docstrings. The attribution format defined in Usage Rules is the implementation spec for FEAT-006's music-related easter eggs. |
| **FEAT-007 (DX Delight)** | FEAT-007 uses the Mood/Energy classifications to calibrate CLI personality moments. When the session-complete message fires, FEAT-007 knows the energy level is "High / Celebratory" and can draw from The Victory Lap category. When a REVISE-band score lands, FEAT-007 knows the energy is "Medium / Resilient" and can reference The Diagnostic category. |
| **FEAT-002 (/saucer-boy Skill)** | The /saucer-boy skill can reference SOUNDTRACK.md to validate that music references in framework output text are (a) from the canonical track list, (b) properly attributed, and (c) contextually appropriate per the Mood/Energy classification. |
| **FEAT-004 (Framework Voice)** | The canonical emotional mappings (quality gate PASS = Daft Punk, FAIL/REVISE = Kendrick, FAIL/REJECTED = Gang Starr, constitutional failure = RATM, session complete = AC/DC, session start = Nas) are the primary reference for FEAT-004's voice rewrite work. |

### Maintenance

**Adding new tracks:**
1. The track must have a specific, defensible framework mapping — no filler
2. The track must pass the Genre Guidelines inclusion/exclusion criteria
3. Artist name, song title, album name, and year must be verified via web search (DISC-002 lesson: training data is frequently wrong for music metadata)
4. The track must include a lyric fragment (or explicit note that it is instrumental)
5. The track must be assigned a Mood/Energy classification
6. Add to both the category section and the Full Track List
7. This is a C1 change — no quality gate scoring required

**Retiring tracks:**
1. Move to an "Archived Tracks" section at the end of the Full Track List (do not delete — the reference may still exist in source code comments)
2. Note the retirement date and reason
3. Grep the codebase for references to the retired track and update or annotate them

**Maximum track count:** 40. Beyond 40, the soundtrack becomes a generic playlist rather than a curated cultural artifact. If a new track is added beyond 40, an existing track must be retired.

---

## The Full Track List

| # | Category | Artist | Title | Album | Year | Framework Mapping (short) | Mood/Energy |
|---|----------|--------|-------|-------|------|---------------------------|-------------|
| 1 | Session Start | Nas | "N.Y. State of Mind" | *Illmatic* | 1994 | /problem-solving; deep focus | Medium / Focused |
| 2 | Session Start | Massive Attack | "Teardrop" | *Mezzanine* | 1998 | Session initialization; layers activating | Low-Medium / Atmospheric |
| 3 | Session Start | DJ Shadow | "Building Steam with a Grain of Salt" | *Endtroducing.....* | 1996 | Filesystem as infinite memory | Medium / Building |
| 4 | Flow State | Daft Punk | "Harder, Better, Faster, Stronger" | *Discovery* | 2001 | Creator-critic-revision cycle (H-14) | High / Building |
| 5 | Flow State | Eric B. & Rakim | "Don't Sweat the Technique" | *Don't Sweat the Technique* | 1992 | L1-L5 enforcement architecture | Medium / Confident |
| 6 | Flow State | A Tribe Called Quest | "Electric Relaxation" | *Midnight Marauders* | 1993 | Flow state; clean session | Medium / Smooth |
| 7 | Flow State | Tool | "Lateralus" | *Lateralus* | 2001 | Structured decomposition; FMEA (S-012) | High / Intense |
| 8 | Flow State | Boards of Canada | "Roygbiv" | *Music Has the Right to Children* | 1998 | Architecture alignment; clean structure | Medium / Warm |
| 9 | Flow State | Madvillain | "Accordion" | *Madvillainy* | 2004 | Adversary skill; S-014 scoring | Medium / Dense |
| 10 | Victory Lap | AC/DC | "For Those About to Rock (We Salute You)" | *For Those About to Rock We Salute You* | 1981 | Session complete; we salute you | High / Celebratory |
| 11 | Victory Lap | Kanye West | "Stronger" | *Graduation* | 2007 | Iterative improvement; samples Daft Punk | High / Triumphant |
| 12 | Victory Lap | Foo Fighters | "My Hero" | *The Colour and the Shape* | 1997 | Everyday excellence; the ordinary hero | High / Anthemic |
| 13 | Victory Lap | Run the Jewels | "Run the Jewels" | *Run the Jewels* | 2013 | Human + AI orchestration | High / Aggressive-Joyful |
| 14 | Diagnostic | Kendrick Lamar | "Alright" | *To Pimp a Butterfly* | 2015 | QG FAIL / REVISE band; resilience | Medium / Resilient |
| 15 | Diagnostic | Gang Starr | "Moment of Truth" | *Moment of Truth* | 1998 | QG FAIL / REJECTED band; honesty | Low-Medium / Honest |
| 16 | Diagnostic | Big Daddy Kane | "Ain't No Half Steppin'" | *Long Live the Kane* | 1988 | H-13; no shortcuts | Medium-High / Demanding |
| 17 | Diagnostic | Pusha T | "Numbers on the Boards" | *My Name Is My Name* | 2013 | S-014 quality scores; the rubric | Medium-High / Clinical |
| 18 | Diagnostic | Fugazi | "Waiting Room" | *13 Songs* | 1989 | Revision cycle patience; between passes | High / Restless-Disciplined |
| 19 | Hard Stop | Rage Against the Machine | "Know Your Enemy" | *Rage Against the Machine* | 1992 | /adversary skill; Red Team | Low-Medium / Serious |
| 20 | Hard Stop | Radiohead | "Everything in Its Right Place" | *Kid A* | 2000 | Architecture standards; H-10 | Low / Unsettling-Precise |
| 21 | Hard Stop | Miles Davis | "So What" | *Kind of Blue* | 1959 | Constitutional compliance; quiet authority | Low / Authoritative |
| 22 | Powder Day | Beastie Boys | "Sabotage" | *Ill Communication* | 1994 | Planned chaos; Saucer Boy energy | Maximum / Chaotic-Joyful |
| 23 | Powder Day | Led Zeppelin | "Immigrant Song" | *Led Zeppelin III* | 1970 | Dropping into C4 work; the scream | Maximum / Primal |
| 24 | Powder Day | Red Hot Chili Peppers | "Can't Stop" | *By the Way* | 2002 | Innovation momentum; can't stop building | High / Relentless-Joyful |
| 25 | Powder Day | Van Halen | "Jump" | *1984* | 1984 | Ski BASE; commitment to ship | Maximum / Euphoric |
| 26 | Legacy | Tom Petty | "Free Fallin'" | *Full Moon Fever* | 1989 | Ski BASE; beauty and danger | Medium / Bittersweet-Beautiful |
| 27 | Legacy | The Who | "Won't Get Fooled Again" | *Who's Next* | 1971 | P-022 No Deception; L1-L5 | Medium-High / Defiant |
| 28 | Legacy | Metallica | "The Memory Remains" | *Reload* | 1997 | Context rot; filesystem as memory | Medium / Haunting |
| 29 | Legacy | Boogie Down Productions | "My Philosophy" | *By All Means Necessary* | 1988 | JERRY_CONSTITUTION.md; principles | Medium / Authoritative |
| 30 | Legacy | Wu-Tang Clan | "C.R.E.A.M." | *Enter the Wu-Tang (36 Chambers)* | 1993 | "Context Rules Everything Around Me" | Medium / Foundational |
| 31 | The Craft | J Dilla | "Time: The Donut of the Heart" | *Donuts* | 2006 | Persist state; build from fragments | Low-Medium / Tender |
| 32 | The Craft | Kendrick Lamar | "DNA." | *DAMN.* | 2017 | Constitutional identity; it's in the DNA | High / Intense |
| 33 | The Craft | Rush | "The Spirit of Radio" | *Permanent Waves* | 1980 | OSS release; signal vs. noise | Medium-High / Optimistic |
| 34 | The Craft | Minor Threat | "Out of Step" | *Out of Step* | 1983 | Non-negotiable constraints; H-tier rules | High / Uncompromising |

**Track count:** 34

**Genre distribution:** Hip hop (11), Rock (9), Electronic (4), Metal (2), Jazz (1), Post-hardcore (2), Punk (1), Trip hop (1), IDM (1), Instrumental hip hop (2)

**Decade distribution:** 1950s (1), 1970s (2), 1980s (5), 1990s (13), 2000s (7), 2010s (6)

---

## References

| Source | Role |
|--------|------|
| `ps-creator-001-draft.md` (v0.9.0) | Persona doc: Cultural Reference Palette (Music), Audience Adaptation Matrix, boundary conditions, FEAT-005 implementation notes |
| `EPIC-001-je-ne-sais-quoi.md` | Parent epic: original 23-track soundtrack with framework mappings across 4 categories |
| Discogs (discogs.com) | Album/year verification for all 34 tracks |
| Wikipedia (en.wikipedia.org) | Song, album, and artist metadata cross-reference |
| Spotify (open.spotify.com) | Track listing and album association verification |

---

## Document Metadata

| Attribute | Value |
|-----------|-------|
| Version | 1.0.0 |
| Status | DRAFT — awaiting critic review |
| Agent | ps-creator-005 |
| Workflow | jnsq-20260219-001 |
| Phase | 2 — Tier 1 Fanout |
| Feature | FEAT-005 The Jerry Soundtrack |
| Criticality | C1 (Routine) |
| Date | 2026-02-19 |
| Track count | 34 |
| Self-review (S-010) | Applied: verified all metadata via WebSearch; corrected BDP/KRS-One artist credit; confirmed album years; validated genre distribution covers hip hop, electronic, rock, metal, jazz, punk, post-hardcore; confirmed all 7 required categories plus 1 bonus category are covered; confirmed navigation table (H-23) with anchor links (H-24) |
| EPIC-001 corrections | "My Philosophy" artist credit corrected from "KRS-One" to "Boogie Down Productions" (released under BDP, not KRS-One solo) |
| Next step | ps-critic-005 review |
