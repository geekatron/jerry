# ts-parser Parsing Rules Reference

> LLM fallback parsing rules for VTT, SRT, and plain text formats.
> Used by ts-parser FALLBACK role for non-VTT files and Python parser error recovery.

---

## VTT Parsing Rules (FR-001)

```
WEBVTT files contain:
- Header: "WEBVTT" (required)
- Cues: timestamp line + payload lines (may span multiple text lines)

VOICE TAG PATTERN (with optional closing tag):
─────────────────────────────────────────────
Opening tag: <v SPEAKER_NAME>
Closing tag: </v> (optional per W3C spec, but common in practice)

Single-line example:
  <v Alice>Good morning everyone.</v>

Multi-line example (real-world pattern):
  <v Sam Chen>All right. Yeah.
  So I guess I was a little interested in</v>

MULTI-LINE PAYLOAD HANDLING:
────────────────────────────
- Cue payloads MAY span multiple text lines
- Voice tag opens on first line, closes on last line
- All lines between belong to same utterance
- Concatenate lines with SINGLE SPACE (normalize whitespace)
- Strip closing </v> tag from extracted text

Extract:
- start_ms: Convert HH:MM:SS.mmm to milliseconds
- end_ms: Convert HH:MM:SS.mmm to milliseconds
- speaker: Extract from <v> tag, or null if absent
- text: Content between tags (or after opening tag if no closing)
       MUST strip closing </v> from extracted text
       MUST normalize multi-line to single space-separated string

IMPORTANT: Accept BOTH with and without closing </v> tags
per PAT-002 (Defensive Parsing: "Accept liberally, produce consistently").
```

## SRT Parsing Rules (FR-002)

```
SRT files contain:
- Index: Sequential number
- Timestamp line: HH:MM:SS,mmm --> HH:MM:SS,mmm
- Text lines: One or more lines

Speaker Pattern: SPEAKER: text or Speaker: text
Example: Alice: Good morning everyone.

Extract:
- start_ms: Convert (note: SRT uses comma for ms separator)
- end_ms: Convert
- speaker: Extract from "Name:" prefix, or null if absent
- text: Content after speaker prefix
```

## Plain Text Parsing Rules (FR-003)

```
Plain text files have NO timestamps. Detect speaker patterns:

Pattern 1: "Name: text"
Pattern 2: "[Name] text"
Pattern 3: "NAME: text" (all caps)

Extract:
- start_ms: null (no timestamp available)
- end_ms: null
- speaker: Extract from detected pattern
- text: Remaining content

IMPORTANT: Do NOT fabricate timestamps. Use null for both start_ms and end_ms.
```

## Timestamp Normalization (NFR-006)

```
Convert all timestamp formats to milliseconds (integer):

Input: "01:23:45.678" (VTT)
       -> hours=1, minutes=23, seconds=45, ms=678
       -> (1*3600 + 23*60 + 45) * 1000 + 678
       -> 5025678

Input: "01:23:45,678" (SRT with comma)
       -> Same calculation
       -> 5025678

Precision: 10 milliseconds (round to nearest 10ms)
```
