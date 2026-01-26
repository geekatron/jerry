# WebVTT Format Specification Research

> **Researched:** 2026-01-25
> **Task:** TASK-007
> **Enabler:** EN-002
> **Agent:** ps-researcher

---

## L0: ELI5 Summary

WebVTT (Web Video Text Tracks) is a simple text format for displaying timed captions or subtitles with videos. Think of it like a script that tells the video player "show this text from time A to time B." It's the standard format used by YouTube, HTML5 video players, and most modern web applications for captions.

## L1: Engineer Summary

WebVTT is a UTF-8 encoded text format defined by the W3C for timed text tracks. A VTT file consists of a required `WEBVTT` header, followed by optional metadata blocks (NOTE, REGION, STYLE) and cue blocks. Each cue has an optional identifier, required timestamp range (`start --> end`), optional positioning settings, and a text payload that can include formatting tags like `<v>` for voice/speaker identification, `<c>` for styling classes, and standard HTML-like tags for bold/italic/underline. Timestamps follow `hh:mm:ss.ttt` or `mm:ss.ttt` format with millisecond precision. For transcript processing, the key elements are: (1) timestamp parsing with `-->` separator, (2) voice tags `<v Speaker>text</v>` for speaker identification, and (3) handling of multi-line cue payloads. Parsers must handle blank line separation between cues and gracefully recover from malformed input.

## L2: Architect Summary

When designing a VTT parser for transcript processing, key architectural considerations include: (1) **Streaming vs. DOM parsing** - VTT's line-based structure favors streaming parsers for large files, but our use case (entity extraction) benefits from full DOM representation for cross-cue analysis; (2) **Error tolerance** - real-world VTT files often deviate from spec (wrong line endings, BOM issues, timing overlaps), requiring a forgiving parser with clear error reporting; (3) **Speaker extraction strategy** - speakers appear in three patterns: voice tags (`<v>`), cue identifiers, and text prefixes (`Speaker:`), requiring multi-strategy extraction; (4) **Timestamp normalization** - both `mm:ss.ttt` and `hh:mm:ss.ttt` formats must normalize to consistent internal representation; (5) **Scalability** - meeting transcripts can be hours long with thousands of cues, so memory-efficient processing is essential. The parser should separate lexing (tokenization) from parsing (structure building) to enable extensibility and testability.

---

## Specification Overview

### Authoritative Source

The authoritative specification is the **W3C WebVTT: The Web Video Text Tracks Format** recommendation, published and maintained by the World Wide Web Consortium.

- **URL:** https://www.w3.org/TR/webvtt1/
- **Status:** W3C Recommendation (17 November 2019)
- **Editors:** Simon Pieters (Opera Software, formerly)

> "WebVTT is intended to be used for marking up external text track resources mainly for the purpose of captioning video content." (W3C, 2019, Section 1)

### File Structure

A WebVTT file consists of the following components in order:

```
1. Optional UTF-8 BOM (U+FEFF)
2. The string "WEBVTT"
3. Optional header text (on same line, after space/tab)
4. Two or more line terminators (blank line)
5. Zero or more blocks (cues, comments, regions, styles)
```

**Block Types:**
- **Cue blocks** - Timed text content
- **NOTE blocks** - Comments (not displayed)
- **REGION blocks** - Positioning definitions
- **STYLE blocks** - CSS styling (embedded)

### Minimal Valid VTT File

```vtt
WEBVTT

00:00:00.000 --> 00:00:05.000
Hello, world!
```

### Complete Example

```vtt
WEBVTT - Meeting Transcript

NOTE
This transcript was generated automatically.
Quality may vary.

REGION
id:fred
width:40%
lines:3
regionanchor:0%,100%
viewportanchor:10%,90%
scroll:up

STYLE
::cue {
  background-color: rgba(0,0,0,0.8);
  color: white;
}

::cue(v[voice="Alice"]) {
  color: cyan;
}

1
00:00:00.000 --> 00:00:02.500 line:0 position:10% align:start
<v Alice>Hello, how are you?

2
00:00:02.500 --> 00:00:05.000 region:fred
<v Bob>I'm doing great, thanks for asking!

3
00:00:05.500 --> 00:00:08.000
<v Alice><i>pauses</i> That's wonderful to hear.
```

---

## Header

### WEBVTT Signature

| Element | Required | Format | Notes |
|---------|----------|--------|-------|
| BOM | No | U+FEFF | Optional UTF-8 Byte Order Mark |
| Signature | Yes | `WEBVTT` | Case-sensitive, must be exact |
| Header text | No | ` [text]` or `\t[text]` | Space/tab + optional description |
| Blank line | Yes | Two line terminators | Separates header from body |

**Valid Headers:**
```
WEBVTT
WEBVTT Meeting Transcript 2026-01-25
WEBVTT - This is a description
WEBVTT	Tabs are allowed too
```

**Invalid Headers:**
```
webvtt            (lowercase)
WEBVTT:           (colon not allowed immediately after)
WEBVTT
text              (missing blank line before cues)
```

### Line Terminators

Per the W3C specification, line terminators can be:
- U+000D CARRIAGE RETURN (CR)
- U+000A LINE FEED (LF)
- U+000D U+000A (CRLF)

> "A WebVTT line terminator is the three-character sequence CRLF (U+000D U+000A), or the single character LF (U+000A), or the single character CR (U+000D)." (W3C, 2019, Section 3)

**Implementation Note:** Parsers should normalize all line endings to LF internally.

---

## Cue Structure

### Complete Cue Syntax

```
[cue identifier]
[start timestamp] --> [end timestamp] [cue settings]
[cue payload line 1]
[cue payload line 2]
...
[blank line or end of file]
```

### Cue Identifier

| Property | Value |
|----------|-------|
| Required | No |
| Format | Any text not containing `-->` or newlines |
| Purpose | Reference cues, link to chapters, identify speakers |
| Uniqueness | Not enforced by spec, but recommended |

**Common Patterns:**
```vtt
1                              (numeric)
cue-001                        (prefixed)
Alice-0:00:00                  (speaker+time)
chapter-introduction           (semantic)
```

**Edge Case:** Cue identifier cannot contain the substring `-->` as it would be parsed as a timestamp line.

### Timestamp Format

Timestamps specify when cues appear and disappear.

| Format | Pattern | Example | Notes |
|--------|---------|---------|-------|
| Long | `hh:mm:ss.ttt` | `01:23:45.678` | Hours 2+ digits |
| Short | `mm:ss.ttt` | `23:45.678` | Minutes 2 digits |
| Milliseconds | `.ttt` | Always 3 digits | Required, not optional |

**Grammar:**
```
timestamp ::= (hours ':')? minutes ':' seconds '.' milliseconds
hours     ::= [0-9]{2,}
minutes   ::= [0-5][0-9]
seconds   ::= [0-5][0-9]
milliseconds ::= [0-9]{3}
```

**Valid Timestamps:**
```
00:00:00.000
00:00.000
99:59:59.999
123:45:67.890    (invalid - seconds > 59, but some parsers accept)
```

**Invalid Timestamps:**
```
0:00:00.000      (hours must be 2+ digits if present)
00:00:00.00      (milliseconds must be exactly 3 digits)
00:00:00         (missing milliseconds)
00:60:00.000     (minutes > 59)
```

### Timestamp Arrow

The start and end timestamps are separated by ` --> ` (space, hyphen, hyphen, greater-than, space).

**Critical:** Spaces around `-->` are REQUIRED.

```
00:00:00.000 --> 00:00:05.000    (valid)
00:00:00.000-->00:00:05.000      (INVALID - missing spaces)
00:00:00.000  -->  00:00:05.000  (INVALID - extra spaces)
```

### Cue Timing Constraints

| Constraint | Specification | Handling |
|------------|---------------|----------|
| End > Start | End time must be greater than start time | Cue ignored if violated |
| Overlapping | Cues may overlap in time | Both displayed simultaneously |
| Zero duration | Start == End | Technically invalid per spec |
| Negative times | Not allowed | Parse error |

---

## Cue Settings

Cue settings appear after the end timestamp, separated by spaces.

### Setting Reference

| Setting | Purpose | Values | Default | Example |
|---------|---------|--------|---------|---------|
| `vertical` | Text direction | `rl` (right-to-left), `lr` (left-to-right) | (horizontal) | `vertical:rl` |
| `line` | Vertical position | Number, %, `auto` | `auto` | `line:0`, `line:100%` |
| `position` | Horizontal position | % (0-100) | Based on alignment | `position:50%` |
| `size` | Cue box width | % (0-100) | `100` | `size:80%` |
| `align` | Text alignment | `start`, `center`, `end`, `left`, `right` | `center` | `align:left` |
| `region` | Use named region | Region ID | (none) | `region:sidebar` |

### Line Setting Details

The `line` setting controls vertical placement:

```vtt
00:00:00.000 --> 00:00:05.000 line:0
Text at top of video

00:00:05.000 --> 00:00:10.000 line:100%
Text at bottom of video

00:00:10.000 --> 00:00:15.000 line:-1
Text one line up from bottom (line numbers from bottom are negative)
```

### Position Setting Details

The `position` setting controls horizontal placement:

```vtt
00:00:00.000 --> 00:00:05.000 position:10%
Text aligned to left 10%

00:00:05.000 --> 00:00:10.000 position:90%
Text aligned to right 90%
```

### Alignment Setting Details

| Value | Behavior |
|-------|----------|
| `start` | Align to writing-mode start (left for LTR, right for RTL) |
| `center` | Center alignment |
| `end` | Align to writing-mode end |
| `left` | Always left-aligned |
| `right` | Always right-aligned |

### Combined Example

```vtt
00:00:00.000 --> 00:00:05.000 line:0 position:10% align:start size:40%
<v Speaker>This text appears at top-left, 40% width, left-aligned
```

---

## Cue Payload Formatting

### Supported Tags

| Tag | Purpose | Syntax | Rendered As |
|-----|---------|--------|-------------|
| `<c>` | Class | `<c.classname>text</c>` | Styled span |
| `<i>` | Italic | `<i>text</i>` | Italicized text |
| `<b>` | Bold | `<b>text</b>` | Bold text |
| `<u>` | Underline | `<u>text</u>` | Underlined text |
| `<ruby>` | Ruby (CJK) | `<ruby>base<rt>annotation</rt></ruby>` | Ruby text |
| `<rt>` | Ruby text | Used within `<ruby>` | Annotation |
| `<v>` | Voice | `<v Speaker>text</v>` | Speaker identification |
| `<lang>` | Language | `<lang en>text</lang>` | Language annotation |

### Voice Tag (Critical for Transcript Processing)

The voice tag `<v>` is the primary mechanism for speaker identification in WebVTT:

```vtt
00:00:00.000 --> 00:00:02.000
<v Alice>Hello everyone!

00:00:02.000 --> 00:00:04.000
<v Bob>Hi Alice, good to see you.

00:00:04.000 --> 00:00:06.000
<v Alice>Bob, can you share your screen?
```

**Voice Tag Syntax:**
```
<v SPEAKER_NAME>text content</v>
<v SPEAKER_NAME>text content    (closing tag optional per spec)
```

**Important:** Per W3C spec, the closing `</v>` tag is OPTIONAL. Many generators omit it.

**Voice Tag Attributes:**
- The speaker name is the text between `<v ` and `>`
- Speaker names can contain spaces: `<v John Smith>`
- Multiple voices in one cue are allowed

**Multi-Voice Cue:**
```vtt
00:00:00.000 --> 00:00:04.000
<v Alice>Who has the report?</v>
<v Bob>I do, let me share it.
```

### Class Tag

Classes can be used for styling:

```vtt
00:00:00.000 --> 00:00:05.000
<c.highlight>Important announcement:</c> Meeting cancelled.
```

### Timestamp Tags (Karaoke)

Inline timestamps create karaoke-style highlighting:

```vtt
00:00:00.000 --> 00:00:05.000
Never gonna <00:00:01.500>give you <00:00:02.500>up
```

### Multi-line Payloads

Cue payloads can span multiple lines:

```vtt
00:00:00.000 --> 00:00:10.000
This is line one.
This is line two.
This is line three.
```

**Rendered as:** Three lines of text displayed together.

### Escaping Special Characters

| Character | Escape Sequence |
|-----------|-----------------|
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| Non-breaking space | `&nbsp;` |
| Left-to-right mark | `&lrm;` |
| Right-to-left mark | `&rlm;` |

---

## Speaker Identification Patterns

### Pattern 1: Voice Tags (Preferred)

The W3C-compliant method using `<v>` tags:

```vtt
00:00:00.000 --> 00:00:02.000
<v Alice Johnson>Let's begin the meeting.

00:00:02.000 --> 00:00:05.000
<v Bob Smith>Thanks Alice. First item on the agenda...
```

**Extraction Strategy:**
```python
# Regex pattern for voice tags
import re
voice_pattern = r'<v\s+([^>]+)>'
# Matches: <v Speaker Name>
# Group 1: Speaker Name
```

### Pattern 2: Cue Identifiers

Some systems encode speaker in the cue identifier:

```vtt
Alice-1
00:00:00.000 --> 00:00:02.000
Let's begin the meeting.

Bob-2
00:00:02.000 --> 00:00:05.000
Thanks Alice. First item on the agenda...
```

**Extraction Strategy:**
```python
# Identifier pattern (extract before hyphen or number)
identifier_pattern = r'^([A-Za-z\s]+?)[-\d]'
```

### Pattern 3: Text Prefixes (Informal)

Non-standard but common in generated transcripts:

```vtt
00:00:00.000 --> 00:00:02.000
Alice: Let's begin the meeting.

00:00:02.000 --> 00:00:05.000
Bob: Thanks Alice. First item on the agenda...
```

**Extraction Strategy:**
```python
# Colon prefix pattern
prefix_pattern = r'^([A-Za-z\s]+):\s*(.+)$'
# Group 1: Speaker, Group 2: Text
```

### Pattern 4: Square Brackets

Another common informal pattern:

```vtt
00:00:00.000 --> 00:00:02.000
[Alice] Let's begin the meeting.

00:00:02.000 --> 00:00:05.000
[Bob] Thanks Alice. First item on the agenda...
```

### Hybrid Detection Algorithm

For robust speaker extraction, implement fallback:

```python
def extract_speaker(cue):
    # Try voice tag first (most reliable)
    if match := re.search(r'<v\s+([^>]+)>', cue.text):
        return match.group(1)

    # Try cue identifier
    if cue.identifier and (match := re.match(r'^([A-Za-z\s]+)', cue.identifier)):
        candidate = match.group(1).strip()
        if looks_like_speaker_name(candidate):
            return candidate

    # Try text prefix patterns
    for pattern in [r'^([A-Za-z\s]+):\s', r'^\[([A-Za-z\s]+)\]\s']:
        if match := re.match(pattern, cue.text):
            return match.group(1)

    return None  # Unknown speaker
```

---

## Metadata Blocks

### NOTE Block

Comments that are not displayed to users:

```vtt
WEBVTT

NOTE
This is a single-line comment.

NOTE
This is a multi-line comment.
It can span multiple lines.
It ends at the next blank line.

00:00:00.000 --> 00:00:05.000
First cue after comments.
```

**Use Cases:**
- File metadata (author, date, version)
- Processing instructions
- Quality indicators
- Copyright notices

**Parsing Rule:** Everything after `NOTE` until blank line is comment text.

### STYLE Block

Embedded CSS for cue styling:

```vtt
WEBVTT

STYLE
::cue {
  font-family: Arial, sans-serif;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
}

::cue(b) {
  color: yellow;
}

::cue(v[voice="Alice"]) {
  color: cyan;
}

::cue(v[voice="Bob"]) {
  color: orange;
}
```

**Style Selectors:**
- `::cue` - All cues
- `::cue(b)` - Bold text in cues
- `::cue(i)` - Italic text in cues
- `::cue(v[voice="Name"])` - Specific speaker
- `::cue(.classname)` - Cues with class

**Note for Transcript Processing:** STYLE blocks indicate the VTT was created with presentation in mind. The voice attributes in selectors can help identify expected speakers.

### REGION Block

Defines positioning regions for cues:

```vtt
WEBVTT

REGION
id:speaker1
width:40%
lines:3
regionanchor:0%,100%
viewportanchor:10%,90%

REGION
id:speaker2
width:40%
lines:3
regionanchor:100%,100%
viewportanchor:90%,90%

00:00:00.000 --> 00:00:02.000 region:speaker1
<v Alice>Text in left region

00:00:00.000 --> 00:00:02.000 region:speaker2
<v Bob>Text in right region
```

**Region Settings:**

| Setting | Purpose | Example |
|---------|---------|---------|
| `id` | Region identifier | `id:sidebar` |
| `width` | Region width | `width:40%` |
| `lines` | Number of text lines | `lines:3` |
| `regionanchor` | Anchor point in region | `regionanchor:50%,100%` |
| `viewportanchor` | Position in viewport | `viewportanchor:50%,90%` |
| `scroll` | Scroll behavior | `scroll:up` |

---

## Edge Cases and Quirks

### Known Issues and Handling Recommendations

| Issue | Description | Handling Recommendation |
|-------|-------------|------------------------|
| BOM presence | UTF-8 BOM (EF BB BF) may precede WEBVTT | Strip BOM before parsing |
| Mixed line endings | Files may mix CR, LF, CRLF | Normalize all to LF |
| Trailing whitespace | Lines may have trailing spaces | Trim lines during parsing |
| Missing milliseconds | `00:00:00` instead of `00:00:00.000` | Accept but warn; default `.000` |
| Wrong timestamp format | `00:00:00,000` (comma instead of period) | SRT format leak; convert comma to period |
| Overlapping cues | Same time range for multiple cues | Valid per spec; preserve all |
| Empty cue payload | Timestamp with no text | Skip cue or preserve as placeholder |
| Nested tags | `<b><i>text</i></b>` | Valid; respect nesting |
| Unclosed tags | `<v Speaker>text` (no `</v>`) | Valid per spec; implicit close at cue end |
| HTML entities | `&amp;` `&lt;` etc. | Decode to characters |
| Invalid HTML entities | `&invalid;` | Preserve as-is |
| Cue identifier with `-->` | Would break parsing | Reject identifier |
| Negative line numbers | `line:-1` | Valid; count from bottom |
| Unicode speakers | `<v >`| Fully supported; preserve |
| Extremely long cues | Minutes of text in single cue | Valid; may indicate transcription tool artifact |
| Duplicate cue identifiers | Same ID used twice | Spec doesn't forbid; preserve both |
| Zero-duration cues | `00:00:00.000 --> 00:00:00.000` | Technically invalid; skip or warn |
| End before start | `00:05:00.000 --> 00:00:00.000` | Invalid; skip cue |
| Timestamp overflow | `99:99:99.999` | Invalid seconds/minutes; reject |

### Common Generator Quirks

| Generator | Known Quirk |
|-----------|-------------|
| YouTube | Uses `align:start` heavily; consistent voice tags |
| Zoom | May use text prefixes instead of voice tags |
| Rev.ai | Clean VTT but speaker as prefix `Speaker 1:` |
| Otter.ai | Uses voice tags; sometimes inconsistent speaker names |
| AWS Transcribe | Includes confidence markers in comments |
| Google Cloud | Uses `<c.colorXXXXXX>` for speaker colors |
| Whisper | Often lacks speaker identification |

### Character Encoding

**Requirement:** VTT files MUST be encoded as UTF-8.

> "A WebVTT file must be encoded as UTF-8." (W3C, 2019, Section 3.1)

**Implementation Notes:**
1. Accept UTF-8 BOM but don't require it
2. Reject files with other encodings (or attempt conversion with warning)
3. Handle all Unicode in speaker names, timestamps, and text

**BOM Handling:**
```python
def remove_bom(content: bytes) -> str:
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]  # Remove UTF-8 BOM
    return content.decode('utf-8')
```

---

## Implementation Considerations

### Parsing Strategy

**Recommended Approach: State Machine Parser**

```
States:
  INITIAL     -> Expect WEBVTT signature
  HEADER      -> Consume header text, expect blank line
  BODY        -> Expect block (cue, NOTE, STYLE, REGION)
  CUE_ID      -> Possible cue identifier
  CUE_TIMING  -> Timestamp line
  CUE_PAYLOAD -> Cue text content
  NOTE        -> Comment block
  STYLE       -> Style block
  REGION      -> Region block

Transitions:
  INITIAL + "WEBVTT" -> HEADER
  HEADER + blank_line -> BODY
  BODY + "NOTE" -> NOTE
  BODY + "STYLE" -> STYLE
  BODY + "REGION" -> REGION
  BODY + timestamp_line -> CUE_TIMING
  BODY + other_text -> CUE_ID
  CUE_ID + timestamp_line -> CUE_TIMING
  CUE_TIMING + text -> CUE_PAYLOAD
  CUE_PAYLOAD + blank_line -> BODY
  NOTE/STYLE/REGION + blank_line -> BODY
```

### Data Structures

```python
@dataclass
class WebVTTCue:
    identifier: str | None
    start_time: timedelta
    end_time: timedelta
    settings: dict[str, str]  # line, position, align, etc.
    payload: str  # Raw payload with tags
    voice: str | None  # Extracted speaker name
    text: str  # Payload with tags stripped

@dataclass
class WebVTTFile:
    header_text: str | None
    notes: list[str]
    styles: list[str]
    regions: list[WebVTTRegion]
    cues: list[WebVTTCue]

@dataclass
class WebVTTRegion:
    id: str
    width: str
    lines: int
    region_anchor: tuple[float, float]
    viewport_anchor: tuple[float, float]
    scroll: str | None
```

### Error Handling Strategy

| Error Severity | Action | Example |
|----------------|--------|---------|
| Fatal | Stop parsing, raise exception | Missing WEBVTT header |
| Error | Skip element, log warning | Invalid timestamp format |
| Warning | Continue with correction | Missing milliseconds |
| Info | Log for debugging | Unknown cue setting |

### Timestamp Parsing

```python
import re
from datetime import timedelta

TIMESTAMP_PATTERN = re.compile(
    r'(?:(\d{2,}):)?'    # Optional hours (2+ digits)
    r'(\d{2}):'           # Minutes (exactly 2 digits)
    r'(\d{2})'            # Seconds (exactly 2 digits)
    r'\.(\d{3})'          # Milliseconds (exactly 3 digits)
)

def parse_timestamp(ts: str) -> timedelta:
    match = TIMESTAMP_PATTERN.fullmatch(ts.strip())
    if not match:
        raise ValueError(f"Invalid timestamp: {ts}")

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2))
    seconds = int(match.group(3))
    milliseconds = int(match.group(4))

    if minutes > 59 or seconds > 59:
        raise ValueError(f"Invalid timestamp values: {ts}")

    return timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        milliseconds=milliseconds
    )
```

### Voice Tag Extraction

```python
import re
from html import unescape

VOICE_TAG_PATTERN = re.compile(r'<v\s+([^>]+)>', re.IGNORECASE)

def extract_voice(payload: str) -> str | None:
    """Extract speaker name from voice tag."""
    match = VOICE_TAG_PATTERN.search(payload)
    if match:
        return unescape(match.group(1).strip())
    return None

def strip_tags(payload: str) -> str:
    """Remove all VTT tags from payload."""
    # Remove voice tags but keep content
    text = re.sub(r'<v\s+[^>]*>', '', payload)
    # Remove closing voice tags
    text = re.sub(r'</v>', '', text)
    # Remove other tags
    text = re.sub(r'</?[cibu](?:\.[^>]*)?>|</[cibu]>', '', text)
    # Remove ruby tags
    text = re.sub(r'</?ruby>|</?rt>', '', text)
    # Remove lang tags
    text = re.sub(r'</?lang[^>]*>', '', text)
    # Remove timestamp tags
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    text = re.sub(r'<\d{2}:\d{2}\.\d{3}>', '', text)
    # Decode HTML entities
    text = unescape(text)
    return text.strip()
```

### Performance Considerations

| Concern | Recommendation |
|---------|----------------|
| Large files | Stream parsing, don't load entire file to memory |
| Many cues | Use generators for cue iteration |
| Regex compilation | Compile patterns once, reuse |
| String concatenation | Use StringIO for payload building |
| Timestamp parsing | Cache parsed values |

---

## Validation Checklist

For a parser to be considered spec-compliant:

- [ ] Accepts files starting with optional BOM
- [ ] Requires `WEBVTT` signature (case-sensitive)
- [ ] Accepts header text after space/tab
- [ ] Requires blank line after header
- [ ] Parses NOTE blocks as comments
- [ ] Parses STYLE blocks (even if not applying styles)
- [ ] Parses REGION blocks
- [ ] Handles cues with and without identifiers
- [ ] Validates timestamp format strictly
- [ ] Requires `-->` with surrounding spaces
- [ ] Parses all cue settings (line, position, size, align, vertical, region)
- [ ] Handles multi-line cue payloads
- [ ] Extracts voice tags correctly
- [ ] Preserves other formatting tags
- [ ] Handles HTML entities
- [ ] Handles Unicode content
- [ ] Gracefully handles malformed input
- [ ] Reports errors with line numbers

---

## Example VTT Files for Testing

### Minimal Valid File

```vtt
WEBVTT

00:00:00.000 --> 00:00:05.000
Hello, world!
```

### Full-Featured File

```vtt
WEBVTT Transcript of Sprint Planning Meeting

NOTE
Recorded: 2026-01-15
Participants: Alice, Bob, Carol

STYLE
::cue(v[voice="Alice"]) { color: cyan; }
::cue(v[voice="Bob"]) { color: yellow; }
::cue(v[voice="Carol"]) { color: lime; }

REGION
id:presenter
width:80%
lines:3
viewportanchor:50%,10%

intro
00:00:00.000 --> 00:00:03.500 align:center
<v Alice>Good morning everyone! Let's start the sprint planning.

bob-1
00:00:03.500 --> 00:00:07.000
<v Bob>Thanks Alice. I've prepared the backlog items.

00:00:07.000 --> 00:00:11.500
<v Carol><i>shares screen</i> Here's what we accomplished last sprint.

00:00:11.500 --> 00:00:15.000 region:presenter
<v Alice>Great progress! Our velocity was <b>23 points</b>.
```

### Edge Case File

```vtt
WEBVTT

NOTE Empty cue ahead

00:00:00.000 --> 00:00:01.000

NOTE Cue with unclosed voice tag

00:00:01.000 --> 00:00:03.000
<v Speaker With Long Name>This voice tag is not closed

NOTE Multi-line cue

00:00:03.000 --> 00:00:08.000
Line one
Line two
Line three

NOTE Unicode content

00:00:08.000 --> 00:00:12.000
<v >:

NOTE Overlapping cues

00:00:12.000 --> 00:00:15.000
<v Alice>First overlapping cue

00:00:13.000 --> 00:00:16.000
<v Bob>Second overlapping cue
```

---

## References

1. World Wide Web Consortium (W3C). (2019, November 17). *WebVTT: The Web Video Text Tracks Format*. W3C Recommendation. https://www.w3.org/TR/webvtt1/

2. WHATWG. (n.d.). *HTML Living Standard - 4.8.11 The track element*. https://html.spec.whatwg.org/multipage/media.html#the-track-element

3. Mozilla Developer Network. (2024). *WebVTT (Web Video Text Tracks)*. MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API

4. World Wide Web Consortium (W3C). (2019). *WebVTT: The Web Video Text Tracks Format - 3. WebVTT file format*. Section 3. https://www.w3.org/TR/webvtt1/#file-structure

5. World Wide Web Consortium (W3C). (2019). *WebVTT: The Web Video Text Tracks Format - 4. Parsing*. Section 4. https://www.w3.org/TR/webvtt1/#parsing

6. World Wide Web Consortium (W3C). (2019). *WebVTT: The Web Video Text Tracks Format - 5. Rendering*. Section 5. https://www.w3.org/TR/webvtt1/#rendering

---

## Appendix: Comparison with SRT Format

| Feature | WebVTT | SRT |
|---------|--------|-----|
| File extension | `.vtt` | `.srt` |
| Header | Required `WEBVTT` | None |
| Encoding | UTF-8 required | Often Latin-1/Windows-1252 |
| Timestamp format | `hh:mm:ss.ttt` | `hh:mm:ss,ttt` (comma!) |
| Timestamp arrow | ` --> ` | ` --> ` |
| Cue identifier | Optional, any format | Required, numeric |
| Styling | `<b>`, `<i>`, `<u>`, CSS | Limited `<b>`, `<i>`, `<u>` |
| Speaker tags | `<v Speaker>` | Not standardized |
| Metadata | NOTE, STYLE, REGION | None |
| Positioning | Full support | Limited |

**Conversion Note:** When converting SRT to VTT:
1. Add `WEBVTT` header
2. Change timestamp comma to period
3. Ensure UTF-8 encoding
4. Map speaker prefixes to voice tags

---

*Document generated by ps-researcher agent for PROJ-008 Transcript Skill*
