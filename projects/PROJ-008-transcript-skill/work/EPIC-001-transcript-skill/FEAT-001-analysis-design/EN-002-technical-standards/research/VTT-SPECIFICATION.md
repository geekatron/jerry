# WebVTT Format Specification Research

> **Researched:** 2026-01-25 (Updated with Live Web Research)
> **Task:** TASK-007
> **Enabler:** EN-002
> **Agent:** ps-researcher
> **Research Method:** Live web research (WebSearch, WebFetch)
> **W3C Spec Version:** W3C Candidate Recommendation (April 4, 2019)
> **Confidence:** High (official W3C specification verified)

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

The authoritative specification is the **W3C WebVTT: The Web Video Text Tracks Format**, published and maintained by the World Wide Web Consortium.

- **URL:** https://www.w3.org/TR/webvtt1/
- **Status:** W3C Candidate Recommendation (April 4, 2019)
- **Editors:** Simon Pieters (Opera Software, formerly)
- **Working Group:** W3C Timed Text Working Group
- **GitHub:** https://github.com/w3c/webvtt (Community Group Draft, actively maintained)
- **MIME Type:** `text/vtt`
- **File Extension:** `.vtt`

**Specification Status Note (from Live Research 2026-01-25):**
The document at W3C TR is a Candidate Recommendation, indicating "the document is believed to be stable and to encourage implementation by the developer community." Three features remain at-risk pending 2+ implementations: collision avoidance with snap-to-lines false, ::cue-region pseudo-element, and :past/:future pseudo-classes. Basic features are supported by all major browsers.

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
| Akamai | May generate UTF-8 BOM that causes parsing errors |
| Azure Media Services v3 | Generated VTT may fail in Edge browser |

### Parsing Challenges from Live Research

Based on real-world issues discovered during web research (2026-01-25):

**1. UTF-8 BOM Issue**
Some services (e.g., Akamai) generate VTT files with UTF-8 BOM (EF BB BF) that causes "Malformed WebVTT signature" errors in strict parsers like hls.js.

**Solution:**
```python
def strip_bom(content: bytes) -> str:
    """Strip UTF-8 BOM if present."""
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
    return content.decode('utf-8')
```

**2. Multiline Comment Handling**
Edge and IE11 (legacy) do not support multiline NOTE blocks properly, throwing parse errors.

**3. Timestamp Validation Edge Cases**
Per W3C spec, the parser must check that `-->` separator is present with spaces. If not, error: "Malformed time stamp (time stamps must be separated by '-->')".

**4. Strict vs. Non-Strict Parsing**
Some parsers (like node-webvtt) offer strict mode. Setting `strict: false` allows malformed files to parse, with errors collected in an `errors` array. Per spec: "the parser will create two cues even if the blank line between them is skipped. This is clearly a mistake, so a conformance checker will flag it as an error, but it is still useful to render the cues to the user."

**5. Browser-Specific Parsing Differences**
- Firefox: Very strict, stops parsing at first region edge case
- Chrome/Safari: More lenient, parse `.5` and `5.` as `0.5` and `5.0` (spec violation)
- Edge/IE: Skip zero-duration cues, may have own parsing bugs

**6. At-Risk Features (W3C CR Stage)**
The 2019 CR identifies three at-risk features requiring 2+ implementations:
- Collision avoidance with `snap-to-lines: false`
- `::cue-region` pseudo-element
- `:past/:future` pseudo-classes

**Source:** GitHub Issues, W3C Implementation Report - Accessed 2026-01-25

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

## Python Libraries for VTT Parsing

### webvtt-py (Recommended)

**Version:** 0.5.1
**PyPI:** https://pypi.org/project/webvtt-py/
**Documentation:** https://webvtt-py.readthedocs.io/
**GitHub:** https://github.com/glut23/webvtt-py
**License:** MIT

**Features:**
- Read, write, and convert WebVTT caption files
- Caption segmentation for HLS video
- Support for SRT and SBV format conversion
- Access to voice/speaker information
- Style block handling

**Installation:**
```bash
pip install webvtt-py
```

**Basic Usage:**
```python
import webvtt

# Read from file
for caption in webvtt.read('captions.vtt'):
    print(caption.start)       # Start timestamp as string
    print(caption.end)         # End timestamp as string
    print(caption.text)        # Clean caption text
    print(caption.voice)       # Voice/speaker if present
    print(caption.raw_text)    # Raw text with tags preserved
    print(caption.identifier)  # Cue identifier

# Read from file-like object
from io import StringIO
buffer = StringIO(vtt_content)
for caption in webvtt.from_buffer(buffer):
    print(caption.text)

# Read from string
for caption in webvtt.from_string(vtt_string):
    print(caption.text)

# Access styles
vtt = webvtt.read('captions.vtt')
for style in vtt.styles:
    print(style.text)

# Convert from SRT
vtt = webvtt.from_srt('captions.srt')
vtt.save()  # Saves as .vtt

# Write to file
vtt.save('output.vtt')
```

**Pros:**
- Simple, Pythonic API
- Native voice tag extraction
- Good for our transcript use case

**Cons:**
- Limited error recovery on malformed files
- No built-in validation

### pycaption

**Version:** 2.2.18
**PyPI:** https://pypi.org/project/pycaption/
**Documentation:** https://pycaption.readthedocs.io/
**GitHub:** https://github.com/pbs/pycaption
**License:** Apache 2.0
**Maintainer:** PBS (Public Broadcasting Service)

**Features:**
- Multi-format support (SAMI, DFXP/TTML, SRT, WebVTT, SCC)
- Read and write capability for most formats
- Styling and positioning support
- Tested with Python 3.8-3.12

**Installation:**
```bash
pip install pycaption
```

**Basic Usage:**
```python
import pycaption

# Read VTT file
reader = pycaption.WebVTTReader()
with open('captions.vtt') as f:
    captions_raw = f.read()

# Verify format
assert reader.detect(captions_raw)

# Parse to caption set
caption_set = reader.read(captions_raw)

# Get available languages
languages = caption_set.get_languages()

# Iterate captions
for lang in languages:
    for caption in caption_set.get_captions(lang):
        print(caption.get_text())  # Get text content
        print(caption.start)        # Start time in microseconds
        print(caption.end)          # End time in microseconds

# Convert to another format
writer = pycaption.SRTWriter()
srt_output = writer.write(caption_set)
```

**Pros:**
- Industrial-strength (used by PBS)
- Multi-format conversion
- Better for complex pipelines

**Cons:**
- More complex API
- Times in microseconds (requires conversion)

### Recommendation for Transcript Skill

**Primary Choice:** `webvtt-py`
- Simpler API matches our needs
- Native voice tag extraction
- Sufficient for transcript processing

**Fallback/Advanced:** `pycaption`
- If we need to support multiple caption formats
- If we need more robust parsing

---

## Browser Compatibility Notes

Based on W3C Implementation Report (Accessed 2026-01-25):

| Browser | Parser Quality | Known Issues |
|---------|----------------|--------------|
| Chrome/Chromium | Good | Parses invalid `.5` and `5.` as valid |
| Safari | Good | line align not supported, defaults -1 instead of auto |
| Firefox | Strict | Stops parsing at first region edge case |
| Edge/IE | Limited | Skips zero-duration cues, multiline comments break parsing |

**Key Finding:** The W3C spec notes "an important feature of WebVTT is that it is forgiving of badly formed files." However, browser implementations vary in strictness.

**Source:** [W3C WebVTT Implementation Report](https://www.w3.org/wiki/TimedText/WebVTT_Implementation_Report) - Accessed 2026-01-25

---

## References

1. World Wide Web Consortium (W3C). (2019, April 4). *WebVTT: The Web Video Text Tracks Format*. W3C Candidate Recommendation. https://www.w3.org/TR/webvtt1/ - Accessed 2026-01-25

2. Mozilla Developer Network. (2026). *Web Video Text Tracks Format (WebVTT)*. MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API/Web_Video_Text_Tracks_Format - Accessed 2026-01-25

3. W3C Text Tracks Community Group. (n.d.). *WebVTT GitHub Repository*. https://github.com/w3c/webvtt - Accessed 2026-01-25

4. webvtt-py Documentation. (n.d.). *Usage - webvtt-py 0.5.1 documentation*. https://webvtt-py.readthedocs.io/en/latest/usage.html - Accessed 2026-01-25

5. pycaption Documentation. (n.d.). *Welcome to pycaption's documentation!*. https://pycaption.readthedocs.io/ - Accessed 2026-01-25

6. BrassTranscripts. (2024). *Multi-Speaker Transcript Formats: SRT, VTT, JSON with Speaker Names*. https://brasstranscripts.com/blog/multi-speaker-transcript-formats-srt-vtt-json - Accessed 2026-01-25

7. GitHub Issues. (n.d.). *hls.js - Malformed WebVTT signature for UTF-8 BOM*. https://github.com/video-dev/hls.js/issues/1286 - Accessed 2026-01-25

8. World Wide Web Consortium (W3C). (n.d.). *TimedText/WebVTT Implementation Report*. https://www.w3.org/wiki/TimedText/WebVTT_Implementation_Report - Accessed 2026-01-25

9. WHATWG. (n.d.). *HTML Living Standard - 4.8.11 The track element*. https://html.spec.whatwg.org/multipage/media.html#the-track-element

10. World Wide Web Consortium (W3C). (2019). *WebVTT: The Web Video Text Tracks Format - 3. WebVTT file format*. Section 3. https://www.w3.org/TR/webvtt1/#file-structure

11. World Wide Web Consortium (W3C). (2019). *WebVTT: The Web Video Text Tracks Format - 4. Parsing*. Section 4. https://www.w3.org/TR/webvtt1/#parsing

12. World Wide Web Consortium (W3C). (2019). *WebVTT: The Web Video Text Tracks Format - 5. Rendering*. Section 5. https://www.w3.org/TR/webvtt1/#rendering

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

---

## Python Library: pysubs2 (Context7)

> **Source:** Context7 MCP - Library documentation (`/tkarabela/pysubs2`)
> **Access Date:** 2026-01-25
> **Note:** webvtt-py was not available in Context7; pysubs2 is documented as an alternative that supports WebVTT format

### Overview

Pysubs2 is a Python library for editing subtitle files, supporting various formats including SubStation Alpha (ASS/SSA), SubRip (SRT), WebVTT, MicroDVD, JSON, TMP, SAMI, and TTML. It includes a CLI tool for batch conversion and retiming.

- **Benchmark Score:** 92.6 (High quality)
- **Source Reputation:** High
- **Code Snippets Available:** 154

### Installation

```bash
pip install pysubs2
```

### WebVTT Support Details

From Context7 documentation:

> "WebVTT: Time-based format similar to SubRip, format identifier is `"vtt"`. Currently implemented as a flavour of SubRip, with no extra support for WebVTT-specific features like styles or subtitle alignment."

**Format identifier:** `"vtt"`

**Limitation:** pysubs2 treats WebVTT as a SubRip variant, meaning:
- Basic cue parsing works
- Voice tags (`<v>`) may not be natively extracted
- Style blocks are not preserved
- Region definitions are not supported

### Basic Usage

#### Loading VTT Files

```python
import pysubs2

# Load from file (auto-detects format from content)
subs = pysubs2.load("captions.vtt")

# Force VTT format explicitly
subs = pysubs2.load("captions.txt", format_="vtt")

# Load from string
vtt_content = """WEBVTT

00:00:00.000 --> 00:00:05.000
Hello, world!
"""
subs = pysubs2.SSAFile.from_string(vtt_content)
```

#### Accessing Cues and Timestamps

```python
import pysubs2

subs = pysubs2.load("transcript.vtt")

# Iterate through all subtitle events (cues)
for event in subs:
    print(f"Start: {event.start}ms")      # Start time in milliseconds
    print(f"End: {event.end}ms")          # End time in milliseconds
    print(f"Duration: {event.duration}ms") # Computed duration
    print(f"Text with tags: {event.text}") # May contain formatting tags
    print(f"Plain text: {event.plaintext}") # Strips all tags
    print("---")

# Access specific cue by index
first_cue = subs[0]
print(f"First cue: {first_cue.plaintext}")

# Get total number of cues
print(f"Total cues: {len(subs)}")
```

#### Working with Timestamps

```python
import pysubs2

# Create timestamps in milliseconds
time1 = pysubs2.make_time(s=1.5)                    # 1500ms
time2 = pysubs2.make_time(h=1, m=30, s=45, ms=500)  # 5445500ms
time3 = pysubs2.make_time(frames=50, fps=25)        # 2000ms (frame-based)

# Convert milliseconds to human-readable format
timestamp = pysubs2.time.ms_to_str(5445500)                    # "1:30:45"
timestamp_frac = pysubs2.time.ms_to_str(5445500, fractions=True)  # "1:30:45.500"

# Convert milliseconds to time components
times = pysubs2.time.ms_to_times(5445500)
print(f"Hours: {times.h}, Minutes: {times.m}, Seconds: {times.s}, Ms: {times.ms}")

# Parse timestamp strings
from pysubs2.time import TIMESTAMP, timestamp_to_ms

match = TIMESTAMP.match("0:00:00.420")
if match:
    ms = timestamp_to_ms(match.groups())  # Returns 420
```

#### Creating and Manipulating Cues

```python
import pysubs2

# Create a new subtitle file
subs = pysubs2.SSAFile()

# Create individual subtitle events
event1 = pysubs2.SSAEvent(
    start=pysubs2.make_time(s=1),
    end=pysubs2.make_time(s=3.5),
    text="Hello World!"
)

event2 = pysubs2.SSAEvent(
    start=pysubs2.make_time(m=1, s=30),
    end=pysubs2.make_time(m=1, s=35),
    text="Second subtitle"
)

# Add events to subtitle file (list-like interface)
subs.append(event1)
subs.append(event2)
subs.insert(0, pysubs2.SSAEvent(start=0, end=500, text="First!"))

# Modify existing events
subs[1].text = "Modified text"
subs[1].duration = 3000  # Automatically adjusts end time

# Remove events
del subs[0]
```

### Converting to/from VTT Format

```python
import pysubs2

# Load any supported format
subs = pysubs2.load("subtitles.srt")

# Save as WebVTT (auto-detects from extension)
subs.save("output.vtt")

# Force VTT format explicitly
subs.save("output.txt", format_="vtt")

# Convert to VTT string (in-memory)
vtt_string = subs.to_string("vtt")
print(vtt_string)
```

### Event Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `event.start` | int | Start time in milliseconds |
| `event.end` | int | End time in milliseconds |
| `event.duration` | int | Computed duration (end - start) |
| `event.text` | str | Text content (may contain tags) |
| `event.plaintext` | str | Text with all tags stripped |
| `event.style` | str | Style name (default: "Default") |
| `event.type` | str | "Dialogue" or "Comment" |
| `event.is_comment` | bool | True if type is "Comment" |
| `event.name` | str | Actor/speaker field (ASS-specific) |
| `event.layer` | int | Layer number (ASS-specific) |

### Handling Voice Tags (Speakers)

**Important:** pysubs2 does not natively extract WebVTT voice tags (`<v Speaker>`). For transcript processing, you need to extract speakers manually:

```python
import re
import pysubs2

VOICE_TAG_PATTERN = re.compile(r'<v\s+([^>]+)>')

def extract_speaker(text: str) -> str | None:
    """Extract speaker name from WebVTT voice tag."""
    match = VOICE_TAG_PATTERN.search(text)
    if match:
        return match.group(1).strip()
    return None

def strip_voice_tags(text: str) -> str:
    """Remove voice tags from text."""
    text = re.sub(r'<v\s+[^>]*>', '', text)
    text = re.sub(r'</v>', '', text)
    return text.strip()

# Usage with pysubs2
subs = pysubs2.load("transcript.vtt")

for event in subs:
    speaker = extract_speaker(event.text)
    clean_text = strip_voice_tags(event.text)

    print(f"Speaker: {speaker or 'Unknown'}")
    print(f"Text: {clean_text}")
    print(f"Time: {event.start}ms - {event.end}ms")
    print("---")
```

### Complete Example: Processing Meeting Transcript

```python
import re
from dataclasses import dataclass
from datetime import timedelta
import pysubs2

@dataclass
class TranscriptCue:
    """Processed transcript cue with speaker extraction."""
    speaker: str | None
    text: str
    start_ms: int
    end_ms: int

    @property
    def start_time(self) -> timedelta:
        return timedelta(milliseconds=self.start_ms)

    @property
    def end_time(self) -> timedelta:
        return timedelta(milliseconds=self.end_ms)

    @property
    def duration_ms(self) -> int:
        return self.end_ms - self.start_ms

VOICE_PATTERN = re.compile(r'<v\s+([^>]+)>')

def process_vtt_transcript(file_path: str) -> list[TranscriptCue]:
    """Process a VTT transcript file into structured cues."""
    subs = pysubs2.load(file_path)
    cues = []

    for event in subs:
        # Extract speaker from voice tag
        match = VOICE_PATTERN.search(event.text)
        speaker = match.group(1).strip() if match else None

        # Clean text (remove voice tags, get plain text)
        clean_text = re.sub(r'</?v[^>]*>', '', event.text)
        clean_text = clean_text.strip()

        cues.append(TranscriptCue(
            speaker=speaker,
            text=clean_text,
            start_ms=event.start,
            end_ms=event.end,
        ))

    return cues

# Example usage
if __name__ == "__main__":
    cues = process_vtt_transcript("meeting.vtt")

    # Group by speaker
    speakers = {}
    for cue in cues:
        speaker = cue.speaker or "Unknown"
        if speaker not in speakers:
            speakers[speaker] = []
        speakers[speaker].append(cue)

    # Print summary
    print(f"Total cues: {len(cues)}")
    print(f"Speakers found: {list(speakers.keys())}")
    print(f"Duration: {cues[-1].end_time if cues else 'N/A'}")
```

### Comparison: pysubs2 vs webvtt-py for Transcripts

| Feature | pysubs2 | webvtt-py |
|---------|---------|-----------|
| VTT parsing | Yes | Yes |
| Voice tag extraction | Manual | Native (`caption.voice`) |
| Multi-format support | 10+ formats | VTT, SRT, SBV only |
| Style block handling | No | Yes (read-only) |
| Timestamp access | Milliseconds (int) | String (HH:MM:SS.mmm) |
| API complexity | Moderate | Simple |
| Context7 docs | Yes | No |

### Recommendation for Transcript Skill

**Primary Choice:** `webvtt-py` (if available and sufficient)
- Native voice tag extraction via `caption.voice`
- Simpler API for VTT-specific use cases

**Alternative:** `pysubs2` (Context7 documented)
- Better for multi-format pipelines
- More powerful manipulation capabilities
- Requires manual voice tag extraction

**Hybrid Approach:**
```python
# Try webvtt-py first, fall back to pysubs2
try:
    import webvtt
    USE_WEBVTT_PY = True
except ImportError:
    import pysubs2
    USE_WEBVTT_PY = False
```

### References

1. pysubs2 GitHub Repository: https://github.com/tkarabela/pysubs2
2. pysubs2 Documentation: https://pysubs2.readthedocs.io/
3. Context7 Library ID: `/tkarabela/pysubs2`
4. PyPI: https://pypi.org/project/pysubs2/
