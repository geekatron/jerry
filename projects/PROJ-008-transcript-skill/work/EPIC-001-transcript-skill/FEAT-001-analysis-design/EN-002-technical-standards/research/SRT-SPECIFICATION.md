# SRT (SubRip) Format Specification Research

> **Researched:** 2026-01-25
> **Last Updated:** 2026-01-25 (Live Web Research)
> **Task:** TASK-008
> **Enabler:** EN-002
> **Agent:** ps-researcher
> **Research Method:** Live web research (WebSearch, WebFetch)
> **PRONOM PUID:** fmt/1218 [1]
> **Wikidata IDs:** Q105852434, Q9332294 [1]
> **Confidence Level:** Medium-High (widely documented but informal de facto standard)

---

## L0: ELI5 Summary

SRT (SubRip) is a simple text file format for storing subtitles. Each subtitle has a number, a start time, an end time, and the text to display. Think of it like a numbered list where each item says "show this text from time A to time B."

## L1: Engineer Summary

SRT is a plain-text subtitle format consisting of sequential numbered blocks. Each block contains: (1) a sequence number, (2) a timing line with start/end timestamps separated by ` --> `, and (3) one or more lines of subtitle text. Timestamps use `HH:MM:SS,mmm` format with a **comma** (not period) as the decimal separator for milliseconds. The format supports basic HTML-like formatting tags (`<i>`, `<b>`, `<u>`, `<font>`) though player support varies. Blocks are separated by blank lines. Parsing requires handling UTF-8 BOM, inconsistent line endings (CR, LF, CRLF), and various generator quirks including non-sequential numbering and overlapping timestamps.

## L2: Architect Summary

From an architecture perspective, SRT's lack of formal specification creates parsing challenges. The format has no header, no metadata mechanism, and no standardized speaker identification. Unlike WebVTT, SRT cannot represent positioning, styling regions, or structured metadata. For transcript processing, key considerations include: (1) character encoding detection (legacy Windows-1252 vs UTF-8), (2) timestamp precision loss in conversion to/from other formats, (3) no native speaker diarization support requiring heuristic extraction from text patterns, and (4) widespread but inconsistent formatting tag support. For SRT-to-VTT conversion, the primary transformations are: comma-to-period in timestamps, adding `WEBVTT` header, and optionally converting formatting tags to WebVTT cue settings.

---

## Specification Overview

### Important Note: No Official Standard

**SRT has no official RFC, W3C recommendation, or formal specification.** The format was originally created for the SubRip software (Windows DVD subtitle ripper) and became a de facto standard through widespread adoption. Documentation is derived from:

1. SubRip software behavior (original implementation)
2. Matroska container specification (documents SRT as embedded format)
3. VLC, FFmpeg, and other player implementations
4. VideoLAN wiki documentation
5. Common usage patterns across subtitle communities

This creates variability in implementations. Parsers must be permissive.

### File Structure

```
[sequence number]
[start time] --> [end time]
[subtitle text line 1]
[subtitle text line 2 (optional)]
[... more text lines (optional)]

[blank line separating blocks]
```

### Complete Example

```srt
1
00:00:00,000 --> 00:00:02,500
Hello, how are you?

2
00:00:02,500 --> 00:00:05,000
I'm doing great, thanks!

3
00:00:05,500 --> 00:00:08,000
<i>This text is italicized</i>
And this is on a second line.
```

---

## Key Elements

### Sequence Number

| Element | Format | Notes |
|---------|--------|-------|
| Type | Positive integer | No leading zeros required |
| Starting value | Typically 1 | Some generators start at 0 |
| Increment | Usually +1 | Gaps allowed, not validated |
| Uniqueness | Recommended | Not enforced by most players |
| Maximum value | Implementation-dependent | Typically 32-bit integer |

**Important Quirks:**
- Sequence numbers do NOT need to be sequential
- Players typically ignore sequence numbers entirely
- Numbers are for human reference and editor convenience
- Some re-encoding tools reset/renumber sequences

### Timestamp Format

| Element | Format | Example | Notes |
|---------|--------|---------|-------|
| Hours | 00-99 | `00`, `01`, `99` | Two digits, can exceed 24 |
| Minutes | 00-59 | `00`, `30`, `59` | Two digits, must be 00-59 |
| Seconds | 00-59 | `00`, `45`, `59` | Two digits, must be 00-59 |
| Milliseconds | 000-999 | `000`, `500`, `999` | Three digits, **comma separator** |
| Full format | `HH:MM:SS,mmm` | `01:23:45,678` | Total: 12 characters |

**Critical: Comma Decimal Separator**

The most distinctive feature of SRT timestamps is the **comma** (`,`) used before milliseconds, not a period (`.`). This is the primary parsing difference from WebVTT.

```
SRT:    00:00:01,500  (comma)
WebVTT: 00:00:01.500  (period)
```

### Arrow Separator

The arrow separator between start and end timestamps is precisely:

```
 -->
```

**Exact specification:**
- One space before the arrow
- Two hyphens
- One greater-than sign
- One space after the arrow

Total: 5 characters (space, hyphen, hyphen, greater-than, space)

**Variations encountered:**
| Variation | Example | Support |
|-----------|---------|---------|
| Standard | ` --> ` | Universal |
| No leading space | `--> ` | Most players |
| No trailing space | ` -->` | Most players |
| No spaces | `-->` | Many players |
| Extra spaces | `  -->  ` | Most players |

**Recommendation:** Parsers should normalize whitespace around `-->`.

### Text Content

| Feature | Support | Notes |
|---------|---------|-------|
| Multi-line | Yes | Newlines preserved |
| Maximum lines | No limit | Typically 2 for readability |
| Line length | No limit | 42 chars recommended for TV |
| Empty lines in text | Not supported | Empty line = block separator |
| Unicode | Yes | Via UTF-8 encoding |

**Text Termination:**
- A blank line (two consecutive newlines) terminates the subtitle block
- End of file also terminates the final block
- Text cannot contain blank lines (would split the block)

---

## Formatting Tags

### Commonly Supported Tags

| Tag | Purpose | Example | Support Level |
|-----|---------|---------|---------------|
| `<i>...</i>` | Italic | `<i>emphasis</i>` | High |
| `<b>...</b>` | Bold | `<b>important</b>` | High |
| `<u>...</u>` | Underline | `<u>highlight</u>` | Medium |
| `<font>...</font>` | Font styling | `<font color="red">text</font>` | Medium |
| `<br>` or `<br/>` | Line break | `line1<br>line2` | Low |

### Font Tag Attributes

```html
<font color="red">Colored text</font>
<font color="#FF0000">Hex color</font>
<font face="Arial">Font family</font>
<font size="20">Font size</font>
```

**Player support for font attributes varies significantly.** VLC supports color, but many players ignore font tags entirely.

### Advanced/Non-Standard Tags

| Tag | Purpose | Support |
|-----|---------|---------|
| `{\an1}` - `{\an9}` | ASS-style positioning | Limited (VLC, MPC-HC) |
| `{\pos(x,y)}` | ASS-style coordinates | Very limited |
| `{\c&HBBGGRR&}` | ASS-style color | Very limited |
| `{\\i1}`, `{\\b1}` | ASS-style formatting | Very limited |

**ASS/SSA tag contamination** is common when SRT files are converted from ASS format. These tags are not part of SRT but frequently appear.

### Positioning Codes (Non-Standard)

Some generators embed SubStation Alpha (ASS) positioning in SRT:

```srt
1
00:00:01,000 --> 00:00:03,000
{\an8}This text appears at top-center

2
00:00:03,000 --> 00:00:05,000
{\an2}This text appears at bottom-center
```

Position grid (numpad layout):
```
7 8 9    (top-left, top-center, top-right)
4 5 6    (middle-left, middle-center, middle-right)
1 2 3    (bottom-left, bottom-center, bottom-right)
```

---

## Character Encoding

### Encoding Detection Priority

| Priority | Encoding | Detection Method |
|----------|----------|------------------|
| 1 | UTF-8 with BOM | Bytes `EF BB BF` at start |
| 2 | UTF-16 LE with BOM | Bytes `FF FE` at start |
| 3 | UTF-16 BE with BOM | Bytes `FE FF` at start |
| 4 | UTF-8 (no BOM) | Valid UTF-8 sequences |
| 5 | Windows-1252 | Fallback for Latin scripts |
| 6 | ISO-8859-1 | Alternative Latin fallback |

### Common Encoding Issues

| Issue | Description | Common Sources |
|-------|-------------|----------------|
| BOM in middle of file | Concatenated files | File merging tools |
| Mixed encodings | Part UTF-8, part Latin-1 | Manual editing |
| Mojibake | Encoding misinterpretation | Wrong codec on open |
| Smart quotes | Curly quotes from Word | Copy-paste from documents |
| Invalid sequences | Broken multibyte chars | Truncated files |

### Regional Encoding Defaults

| Region | Common Legacy Encoding |
|--------|----------------------|
| Western Europe | Windows-1252 |
| Eastern Europe | Windows-1250, ISO-8859-2 |
| Russia | Windows-1251, KOI8-R |
| Greece | Windows-1253, ISO-8859-7 |
| Turkey | Windows-1254, ISO-8859-9 |
| Hebrew | Windows-1255, ISO-8859-8 |
| Arabic | Windows-1256 |
| East Asia | GB2312, Big5, Shift_JIS, EUC-KR |

**Recommendation:** Modern implementations should:
1. Default to UTF-8 output
2. Use BOM detection for input
3. Use charset detection libraries (chardet, uchardet) as fallback
4. Provide explicit encoding override option

---

## Edge Cases and Quirks

### Generator-Specific Quirks

| Generator/Tool | Quirk | Handling |
|----------------|-------|----------|
| SubRip (original) | Windows-1252 encoding default | Detect and convert |
| YouTube auto-captions | Can have overlapping times | Accept overlaps |
| Netflix captions | Use `&lrm;` and `&rlm;` entities | Decode HTML entities |
| Aegisub export | May include ASS tags | Strip or parse `{\an}` codes |
| VLC export | May use period instead of comma | Accept both separators |
| FFmpeg | Strict formatting, no BOM | Highly compatible |
| HandBrake | May duplicate sequence numbers | Accept duplicates |
| Whisper/OpenAI | Sometimes skips sequence numbers | Accept gaps |
| Rev.com exports | Speaker labels as `[Speaker Name]:` | Parse bracket patterns |
| Descript exports | Inline speaker in text | Extract from text patterns |

### Common Malformations

| Issue | Example | Recommendation |
|-------|---------|----------------|
| Missing sequence number | Timing line without number | Auto-generate sequence |
| Non-numeric sequence | `A` or `1a` as sequence | Accept or renumber |
| Period instead of comma | `00:00:01.500` | Accept both separators |
| Missing hours | `00:01,500` | Pad with `00:` |
| Extra timestamp data | `00:00:01,500 X1:0 Y1:0` | Ignore extra fields |
| Negative timestamps | `-00:00:01,000` | Skip or treat as 0 |
| End before start | `00:05 --> 00:03` | Swap or skip |
| Zero-duration cues | `00:05 --> 00:05` | Accept (may indicate timing) |
| Overlapping cues | Cue 2 starts before cue 1 ends | Accept (common in captions) |
| Non-ascending times | Cue 3 starts before cue 2 | Accept, sort if needed |
| Empty text | Number/timing with no text | Skip or preserve |
| HTML entities | `&amp;`, `&lt;`, `&gt;` | Decode entities |
| Line endings | CR, LF, CRLF mixed | Normalize to LF |
| Trailing whitespace | Spaces/tabs after text | Trim |
| BOM mid-file | UTF-8 BOM not at start | Strip invalid BOMs |
| Null bytes | `\x00` in text | Strip or reject |

### Timestamp Edge Cases

| Case | Example | Handling |
|------|---------|----------|
| Hours > 99 | `100:00:00,000` | May fail in some players |
| Milliseconds > 999 | `00:00:00,1234` | Truncate to 999 |
| Leading zeros omitted | `0:0:1,5` | Accept, normalize |
| Extra precision | `00:00:00,5000` (4 digits) | Truncate to 3 digits |
| Scientific notation | `1e3` ms | Reject, require decimal |

---

## VTT vs SRT Comparison

### Structural Differences

| Feature | VTT | SRT |
|---------|-----|-----|
| **File Header** | `WEBVTT` required (line 1) | None |
| **Specification** | W3C Recommendation | De facto standard |
| **Timestamp separator** | Period (`.`) | Comma (`,`) |
| **Hours required** | Optional (`00:00.000`) | Required (`00:00:00,000`) |
| **Cue identifier** | Optional, any string | Required, integer sequence |
| **Metadata** | `NOTE`, `STYLE`, `REGION` | Not supported |
| **Styling** | CSS-like inline/blocks | Limited HTML tags |
| **Positioning** | Cue settings (line, position) | Not supported (ASS hacks) |
| **Speaker ID** | `<v Speaker>text</v>` | Not standardized |
| **Minimum timestamp** | `00:00.000` | `00:00:00,000` |

### Feature Support Matrix

| Feature | VTT Support | SRT Support |
|---------|-------------|-------------|
| Basic timing | Yes | Yes |
| Multi-line text | Yes | Yes |
| Italic (`<i>`) | Yes | Yes (varies) |
| Bold (`<b>`) | Yes | Yes (varies) |
| Underline (`<u>`) | Yes | Yes (varies) |
| Color | Via CSS/`<c>` | Via `<font>` (limited) |
| Ruby annotations | Yes (`<ruby>`) | No |
| Voice/speaker | Yes (`<v>`) | No (text patterns) |
| Vertical text | Yes (cue settings) | No |
| Positioning | Yes (cue settings) | No (ASS hacks only) |
| Alignment | Yes (cue settings) | No |
| Regions | Yes (`REGION`) | No |
| Comments | Yes (`NOTE`) | No |
| Styling blocks | Yes (`STYLE`) | No |
| Chapter markers | Yes (WebVTT chapters) | No |
| Metadata | Yes (custom headers) | No |

### Timing Format Comparison

```
VTT:  00:00:01.500 --> 00:00:03.000
      └── Period separator, hours optional

SRT:  00:00:01,500 --> 00:00:03,000
      └── Comma separator, hours required
```

**Conversion Note:** When converting SRT to VTT, the ONLY required timestamp change is replacing `,` with `.`. The arrow separator (` --> `) is identical.

---

## Implementation Considerations

### Parsing Strategy

**Recommended Parser States:**

```
1. EXPECT_SEQUENCE_OR_EOF
   - Read line, check if numeric → EXPECT_TIMING
   - If blank, stay in current state
   - If EOF, end parsing

2. EXPECT_TIMING
   - Parse timestamp line with regex
   - Extract start/end times
   - → EXPECT_TEXT

3. EXPECT_TEXT
   - Accumulate non-empty lines as subtitle text
   - On empty line → EXPECT_SEQUENCE_OR_EOF
   - On EOF → Emit final cue, end parsing
```

**Recommended Timestamp Regex:**

```regex
(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->\s*(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})
```

Notes:
- Accept 1-2 digits for hours (handle both `0:` and `00:`)
- Accept both comma and period as millisecond separator
- Accept flexible whitespace around arrow
- Capture groups for easy timestamp construction

### SRT to VTT Conversion

**Minimal Conversion Algorithm:**

```python
def srt_to_vtt(srt_content: str) -> str:
    """Convert SRT to VTT format."""
    lines = []
    lines.append("WEBVTT")
    lines.append("")

    for line in srt_content.splitlines():
        # Convert timestamp separator
        if " --> " in line:
            line = line.replace(",", ".")
        lines.append(line)

    return "\n".join(lines)
```

**Enhanced Conversion (handling edge cases):**

1. Add `WEBVTT` header
2. Replace timestamp comma with period
3. Optionally strip sequence numbers (VTT doesn't require them)
4. Optionally convert `<font color="">` to `<c.color>`
5. Optionally add speaker `<v>` tags from text patterns
6. Normalize line endings
7. Ensure UTF-8 encoding

### Error Handling

| Error Type | Strategy | User Feedback |
|------------|----------|---------------|
| Malformed timestamp | Skip cue, continue | Log warning with line number |
| Missing text | Skip cue or include empty | Log info |
| Encoding error | Try fallback encodings | Prompt for encoding |
| Overlapping times | Accept (valid use case) | No warning needed |
| Out-of-order cues | Sort by start time | Log info |
| Invalid sequence | Auto-renumber | Silent fix |
| Empty file | Return empty result | Log warning |
| Binary content | Abort parse | Error: "Not a text file" |

### Validation Rules (Strict Mode)

For strict validation, check:

1. File starts with digit (no BOM) or BOM + digit
2. Every block has: sequence, timing, at least one text line
3. Timestamps increase monotonically (warn on out-of-order)
4. Timestamps use comma separator
5. No overlapping cues (warn only, don't reject)
6. Valid UTF-8 encoding throughout
7. Arrow separator is exactly ` --> `
8. Milliseconds are exactly 3 digits

### Performance Considerations

| File Size | Parsing Strategy |
|-----------|------------------|
| < 1 MB | Load entire file into memory |
| 1-10 MB | Stream with buffered lines |
| > 10 MB | Stream with lazy cue generation |

**Memory estimation:** ~50 bytes metadata per cue + text size

---

## Example SRT Files

### Minimal Valid SRT

```srt
1
00:00:00,000 --> 00:00:02,000
Hello world
```

### Typical Real-World SRT

```srt
1
00:00:00,500 --> 00:00:02,500
Welcome to the meeting.

2
00:00:02,800 --> 00:00:05,200
Today we'll discuss the quarterly results.

3
00:00:05,500 --> 00:00:08,000
<i>Please hold your questions until the end.</i>

4
00:00:08,500 --> 00:00:12,000
Let's start with the sales figures
from Q3.
```

### SRT with Formatting

```srt
1
00:00:01,000 --> 00:00:03,000
<b>Important announcement:</b>

2
00:00:03,500 --> 00:00:06,000
The <i>deadline</i> has been extended.

3
00:00:06,500 --> 00:00:09,000
<font color="red">Warning: This is urgent!</font>

4
00:00:10,000 --> 00:00:13,000
Contact <u>support@example.com</u> for help.
```

### SRT with Speaker Patterns (Common Convention)

```srt
1
00:00:00,000 --> 00:00:02,500
[Alice]: Hello, how are you?

2
00:00:02,500 --> 00:00:05,000
[Bob]: I'm doing great, thanks!

3
00:00:05,500 --> 00:00:08,000
ALICE: That's wonderful to hear.

4
00:00:08,500 --> 00:00:11,000
BOB: Let's get started then.
```

**Note:** Speaker identification is NOT part of SRT standard. These are common text conventions:
- `[Speaker]:` - Bracketed speaker name
- `SPEAKER:` - All-caps speaker name
- `Speaker:` - Title-case speaker name
- `- Speaker text` - Dash prefix (common in theatrical subtitles)

---

## Speaker Extraction Patterns for Transcripts

Since SRT has no native speaker support, transcript parsers must extract speakers from text patterns:

| Pattern | Regex | Example |
|---------|-------|---------|
| Bracketed | `^\[([^\]]+)\]:\s*` | `[John]: Hello` |
| Angle brackets | `^<([^>]+)>:\s*` | `<John>: Hello` |
| Colon suffix | `^([A-Z][A-Za-z\s]+):\s+` | `John Smith: Hello` |
| All caps | `^([A-Z\s]+):\s+` | `JOHN: Hello` |
| Dash prefix | `^-\s*([^:]+):\s*` | `- John: Hello` |
| Parenthetical | `^\(([^)]+)\)\s*` | `(John) Hello` |

**Extraction priority recommendation:**
1. Check for bracketed pattern first (most explicit)
2. Then all-caps pattern (common in professional captions)
3. Then colon-suffix with title-case (general convention)

---

## Python Libraries for SRT Processing

### Recommended: `srt` Library [3][4]

**Installation:** `pip install srt`

**Characteristics:**
- ~200 lines of code, no external dependencies
- ~30% faster than alternatives on typical workloads
- Handles many malformed files other parsers fail on
- Full Unicode support including Asian fullwidth arrow variants
- Includes CLI tools for filtering, time-shifting, multiplexing
- PyPy compatible

**Usage Example:**
```python
import srt
from datetime import timedelta

# Parse SRT content
with open('subtitles.srt', encoding='utf-8') as f:
    subtitles = list(srt.parse(f.read()))

# Access subtitle data
for sub in subtitles:
    print(f"{sub.index}: {sub.start} --> {sub.end}")
    print(sub.content)
    # sub.start and sub.end are datetime.timedelta objects
    # Example: timedelta(0, 1897, 894000) = 0 days, 1897 seconds, 894000 microseconds

# Compose back to SRT format
srt_text = srt.compose(subtitles)
```

**Subtitle object attributes:**
- `index` (int): Sequence number
- `start` (timedelta): Start time
- `end` (timedelta): End time
- `content` (str): Text content
- `proprietary` (str): Extra metadata field

### Alternative: `pysrt` Library [5][6]

**Installation:** `pip install pysrt`

**Characteristics:**
- Object-oriented SubRipFile/SubRipItem interface
- Advanced time manipulation (shifting, rate conversion)
- SAX-like streaming parser for large files
- CLI tools for shift/split/rescale operations
- Explicit encoding support with fallback

**Usage Example:**
```python
import pysrt

# Parse with encoding detection
subs = pysrt.open('subtitles.srt')
# Or with explicit encoding
subs = pysrt.open('subtitles.srt', encoding='iso-8859-1')

# Time manipulation
subs.shift(seconds=-2)  # Move all subs 2 seconds earlier
subs.shift(minutes=1)   # Move all subs 1 minute later
subs.shift(ratio=25/23.9)  # Convert 23.9fps to 25fps subtitle timing

# Access individual subtitle
first_sub = subs[0]
first_sub.start += {'seconds': -1}  # Adjust start time

# Save modifications
subs.save('output.srt')
```

**SubRipItem attributes:**
- `index` (int): Sequence number
- `start`, `end` (SubRipTime): Time objects with arithmetic support
- `text` (str): Content
- `position` (str): Raw positioning coordinates

### Library Comparison Table

| Feature | `srt` | `pysrt` |
|---------|-------|---------|
| Dependencies | None | None |
| Code size | ~200 lines | Larger |
| Performance | Faster (~30%) | Standard |
| Error tolerance | High | High |
| Time arithmetic | Basic (timedelta) | Advanced (SubRipTime) |
| FPS conversion | Manual | Built-in (`ratio`) |
| Streaming parser | No | Yes |
| CLI tools | Yes | Yes |
| Encoding handling | Manual | Built-in options |

**Recommendation for Transcript Skill:**
- Use `srt` for parsing/composing in most cases
- Use `pysrt` if time manipulation (shifting, fps conversion) is needed
- Both handle real-world malformed files well

---

## Historical Context

| Year | Event |
|------|-------|
| ~1998 | SubRip software created (Windows DVD ripper) |
| 2000s | Format gains popularity via online subtitle sharing |
| 2003 | Matroska container adds SRT support |
| 2010 | YouTube begins accepting SRT uploads |
| 2013 | W3C releases WebVTT as modern alternative |
| 2015+ | SRT remains dominant despite VTT existence |
| 2020s | Most video platforms support both SRT and VTT |

**Why SRT persists:** Extreme simplicity, universal support, human-readable format, no learning curve for editors.

---

## References

**Note:** SRT has no official RFC or W3C specification. References are to community documentation, implementations, and authoritative sources. All URLs accessed 2026-01-25 via live web research.

### Authoritative Format Documentation

1. **Library of Congress.** (n.d.). SubRip Subtitle format (SRT). Sustainability of Digital Formats: Planning for Library of Congress Collections. Retrieved January 25, 2026, from https://loc.gov/preservation/digital/formats/fdd/fdd000569.shtml
   - *Official format description document; PRONOM PUID: fmt/1218*

2. **Wikipedia contributors.** (2025, December). SubRip. In Wikipedia, The Free Encyclopedia. Retrieved January 25, 2026, from https://en.wikipedia.org/wiki/SubRip
   - *Comprehensive community documentation; historical context*

### Python Libraries

3. **cdown/srt.** (n.d.). A tiny library for parsing, modifying, and composing SRT files. GitHub. Retrieved January 25, 2026, from https://github.com/cdown/srt
   - *Recommended library; ~200 lines, no dependencies, handles malformed files*

4. **srt Documentation.** (2023, March 28). srt 3.5.3 documentation - Quickstart. Read the Docs. Retrieved January 25, 2026, from https://srt.readthedocs.io/en/latest/quickstart.html
   - *Official documentation for srt library*

5. **byroot/pysrt.** (n.d.). Python parser for SubRip (srt) files. GitHub. Retrieved January 25, 2026, from https://github.com/byroot/pysrt
   - *Alternative library with time manipulation features*

6. **pysrt.** (n.d.). pysrt - SubRip (.srt) file parser. PyPI. Retrieved January 25, 2026, from https://pypi.org/project/pysrt/
   - *PyPI package page*

### Format Comparison (SRT vs VTT)

7. **Ditto Transcripts.** (n.d.). SRT vs. VTT: Understanding the Difference Between Subtitle Formats for Captions. Ditto Blog. Retrieved January 25, 2026, from https://www.dittotranscripts.com/blog/srt-vs-vtt-understanding-the-difference-between-subtitle-formats-for-captions/
   - *Detailed feature comparison*

8. **Happy Scribe.** (n.d.). VTT vs. SRT: Key Differences and When to Use Each Format. Happy Scribe Blog. Retrieved January 25, 2026, from https://www.happyscribe.com/blog/vtt-vs-srt-key-differences-and-when-to-use-each-format
   - *Use case recommendations* (403 on fetch)

9. **Subly.** (n.d.). SRT vs VTT? Which Subtitle Format Should You Use? Subly Blog. Retrieved January 25, 2026, from https://www.getsubly.com/post/srt-vtt
   - *Platform compatibility analysis*

### Troubleshooting & Edge Cases

10. **CheckSub.** (n.d.). Common SRT file errors and how to solve them. CheckSub Blog. Retrieved January 25, 2026, from https://www.checksub.com/blog/how-do-solve-problems-with-srt-files-troubleshooting-with-srt-files
    - *Comprehensive error documentation*

11. **Kaltura.** (n.d.). Troubleshooting SRT Files. Kaltura Knowledge Center. Retrieved January 25, 2026, from https://knowledge.kaltura.com/troubleshooting-srt-files
    - *Platform-specific error handling*

12. **cdown/srt Issue #55.** (n.d.). Error parsing subtitles with (incorrect) single digit second timestamp. GitHub Issues. Retrieved January 25, 2026, from https://github.com/cdown/srt/issues/55
    - *Real-world parsing edge case*

### Speaker Diarization & Multi-Speaker

13. **BrassTranscripts.** (n.d.). Multi-Speaker Transcript Formats: SRT, VTT, JSON with Speaker Names. BrassTranscripts Blog. Retrieved January 25, 2026, from https://brasstranscripts.com/blog/multi-speaker-transcript-formats-srt-vtt-json
    - *Speaker identification conventions*

14. **granludo/diarize_srt.** (n.d.). Identifies the different speakers in a recording and labels them on a SRT file. GitHub. Retrieved January 25, 2026, from https://github.com/granludo/diarize_srt
    - *Diarization integration example*

15. **OpenAI/whisper Discussion #264.** (n.d.). Transcription and diarization (speaker identification). GitHub Discussions. Retrieved January 25, 2026, from https://github.com/openai/whisper/discussions/264
    - *Whisper + diarization approaches*

### Character Encoding

16. **Kence.** (2019, November 27). Detecting Windows-1252 encoding. Digital Ramblings. Retrieved January 25, 2026, from https://kence.org/2019/11/27/detecting-windows-1252-encoding/
    - *Encoding detection strategies*

17. **Wikipedia contributors.** (n.d.). Byte order mark. In Wikipedia, The Free Encyclopedia. Retrieved January 25, 2026, from https://en.wikipedia.org/wiki/Byte_order_mark
    - *BOM detection reference*

### Additional Resources

18. **VideoLAN.** (n.d.). SubRip. VideoLAN Wiki. Retrieved January 25, 2026, from https://wiki.videolan.org/SubRip/
    - *VLC implementation details*

19. **Matroska.org.** (n.d.). Subtitle Specifications. Matroska Technical Specifications. Retrieved January 25, 2026, from https://www.matroska.org/technical/subtitles.html
    - *Container format integration*

20. **FFmpeg Project.** (n.d.). Subtitles. FFmpeg Documentation. Retrieved January 25, 2026, from https://ffmpeg.org/ffmpeg-formats.html#Subtitles
    - *FFmpeg subtitle handling*

21. **W3C.** (2019, April 4). WebVTT: The Web Video Text Tracks Format. W3C Recommendation. Retrieved January 25, 2026, from https://www.w3.org/TR/webvtt1/
    - *VTT specification for comparison*

---

## Appendix: Quick Reference Card

### SRT Format Template

```srt
[sequence: integer starting from 1]
[HH:MM:SS,mmm] --> [HH:MM:SS,mmm]
[text line 1]
[text line 2 (optional)]

[blank line]
[next subtitle block...]
```

### Timestamp Format

```
HH:MM:SS,mmm
││ ││ ││ │││
││ ││ ││ └└└── Milliseconds (000-999)
││ ││ └└────── Seconds (00-59)
││ └└────────── Minutes (00-59)
└└────────────── Hours (00+)
       ^
       └── COMMA separator (not period!)
```

### Common Formatting Tags

```html
<i>italic</i>
<b>bold</b>
<u>underline</u>
<font color="red">colored</font>
```

### Key Differences from VTT

| SRT | VTT |
|-----|-----|
| No header | `WEBVTT` header required |
| `00:00:01,500` | `00:00:01.500` |
| Integer sequence required | Cue ID optional |
| No metadata | NOTE, STYLE, REGION |
| No speaker tags | `<v Speaker>` |

---

## Python Libraries (Context7)

> **Source:** Context7 MCP - Library documentation
> **Access Date:** 2026-01-25
> **Note:** Only `pysrt` was indexed in Context7. The `srt` library by cdown was not available.

### pysrt Library

> **Context7 Library ID:** `/byroot/pysrt`
> **Description:** Python parser for SubRip (srt) files
> **Code Snippets Available:** 15
> **Source Reputation:** High

#### Installation

```bash
pip install pysrt
```

#### Basic Import

```python
>>> import pysrt
```

#### Parsing SRT Files

Parse an SRT file using `pysrt.open()`. Handle encoding issues by specifying the encoding parameter:

```python
>>> subs = pysrt.open('some/file.srt')
# If you get a UnicodeDecodeError try to specify the encoding
>>> subs = pysrt.open('some/file.srt', encoding='iso-8859-1')
```

#### Accessing Subtitles

`SubRipFile` objects are list-like containers of `SubRipItem` instances:

```python
>>> len(subs)
>>> first_sub = subs[0]
```

#### Editing Subtitle Properties

Modify text, start time, and end time properties directly:

```python
>>> first_sub.text = "Hello World !"
>>> first_sub.start.seconds = 20
>>> first_sub.end.minutes = 5
```

#### Time Manipulation (Shifting)

Shift subtitles by seconds, minutes, or a ratio (for frame rate conversion):

```python
>>> subs.shift(seconds=-2) # Move all subs 2 seconds earlier
>>> subs.shift(minutes=1)  # Move all subs 1 minutes later
>>> subs.shift(ratio=25/23.9) # convert a 23.9 fps subtitle in 25 fps
>>> first_sub.shift(seconds=1) # Move the first sub 1 second later
>>> first_sub.start += {'seconds': -1} # Make the first sub start 1 second earlier
```

#### Slicing by Time Range

Extract a portion of subtitles based on start and end times:

```python
>>> part = subs.slice(starts_after={'minutes': 2, 'seconds': 30}, ends_before={'minutes': 3, 'seconds': 40})
>>> part.shift(seconds=-2)
```

#### Saving Modified Files

Save changes to a new file with specified encoding:

```python
>>> subs.save('other/path.srt', encoding='utf-8')
```

### srt Library

> **Note:** The `srt` library by cdown was not indexed in Context7 at the time of this research.
> See the main "Python Libraries for SRT Processing" section above for `srt` library documentation
> obtained via direct web research.

### Library Comparison (Context7 + Web Research)

| Feature | pysrt (Context7) | srt (Web Research) |
|---------|------------------|-------------------|
| **Context7 Available** | Yes | No |
| **Source Reputation** | High | N/A |
| **Dependencies** | None | None |
| **Code size** | Larger | ~200 lines |
| **Performance** | Standard | Faster (~30%) |
| **Error tolerance** | High | High |
| **Time arithmetic** | Advanced (SubRipTime) | Basic (timedelta) |
| **FPS conversion** | Built-in (`ratio`) | Manual |
| **Streaming parser** | Yes | No |
| **CLI tools** | Yes | Yes |
| **Encoding handling** | Built-in options | Manual |
| **Documentation quality** | High (Context7) | High (ReadTheDocs) |

### pysrt Code Examples Summary (Context7)

#### Complete Workflow Example

```python
import pysrt

# 1. Load SRT file with encoding fallback
try:
    subs = pysrt.open('video.srt')
except UnicodeDecodeError:
    subs = pysrt.open('video.srt', encoding='iso-8859-1')

# 2. Inspect subtitles
print(f"Total subtitles: {len(subs)}")
first = subs[0]
print(f"First subtitle: {first.text}")

# 3. Edit content
first.text = "Modified text"
first.start.seconds = 10

# 4. Shift timing for frame rate conversion
# (e.g., 23.976 fps source to 25 fps target)
subs.shift(ratio=25/23.976)

# 5. Extract a time range
segment = subs.slice(
    starts_after={'minutes': 5},
    ends_before={'minutes': 10}
)

# 6. Save to new file
subs.save('video_modified.srt', encoding='utf-8')
```

#### Key Classes (pysrt)

| Class | Description |
|-------|-------------|
| `SubRipFile` | List-like container of subtitles; supports `open()`, `save()`, `shift()`, `slice()` |
| `SubRipItem` | Individual subtitle; has `index`, `start`, `end`, `text` properties |
| `SubRipTime` | Time object with arithmetic support; millisecond precision |

#### pysrt vs srt Decision Matrix

| Use Case | Recommended Library |
|----------|---------------------|
| Simple parse/compose | `srt` |
| Frame rate conversion | `pysrt` (built-in ratio) |
| Time shifting | `pysrt` (rich API) |
| Minimal dependencies | Either (both zero-dep) |
| Maximum performance | `srt` (~30% faster) |
| Large file streaming | `pysrt` (streaming parser) |
| Encoding auto-detection | `pysrt` (built-in) |
| Handling malformed files | Either (both tolerant) |
