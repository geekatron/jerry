# Recon Report — Existing Attack Surface (TASK-176)

> **Engagement:** RT-PROJ041-001
> **Phase:** 1 — Paper engagement (read-only source recon)
> **Authoring Agent:** red-recon
> **Date:** 2026-04-30
> **Status:** COMPLETE
> **Parent:** EN-004 / TASK-176
> **Methodology:** PTES Intelligence Gathering, ATT&CK TA0043, OWASP A03/A05/A08

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Engagement Context](#engagement-context) | Authorization and scope reminder |
| [Surface 1 — VTT/SRT File Ingestion](#surface-1--vttsrt-file-ingestion) | ts-parser + Python VTT adapter |
| [Surface 2 — Audio File Ingestion](#surface-2--audio-file-ingestion) | Audio path and format gap |
| [Surface 3 — JSON Sidecar Parsing](#surface-3--json-sidecar-parsing) | extraction-report.json, _anchors.json, index.json, chunk files |
| [Surface 4 — Markdown Packet Writing](#surface-4--markdown-packet-writing) | ts-formatter rendered .md files |
| [Surface 5 — ts-formatter Agent Prompts (LLM Injection)](#surface-5--ts-formatter-agent-prompts-llm-injection) | Prompt injection risk through transcript content |
| [Cross-Surface Observations](#cross-surface-observations) | Pipeline-level trust boundary gaps |
| [ATT&CK Technique Mapping](#attck-technique-mapping) | Technique IDs for documented risks |

---

## Engagement Context

This report is produced under Engagement RT-PROJ041-001, Phase 1 (paper engagement). All findings are based on reading source files in `feat/PROJ-041-transcript-hardening` only. No exploit attempts were made and no commands were executed beyond reading source files. Rule P-9 (`architecture-validation-forbidden-patterns`) is applied: all paths are repo-relative.

---

## Surface 1 — VTT/SRT File Ingestion

### Entry Points

| Entry Point | Path |
|-------------|------|
| ts-parser agent (orchestrator) | `skills/transcript/agents/ts-parser.md` |
| VTTParser Python adapter | `src/transcript/infrastructure/adapters/vtt_parser.py` |
| ITranscriptParser port | `src/transcript/domain/ports/transcript_parser.py` |
| VTT compliance validator script | `skills/transcript/scripts/validate_vtt.py` |
| CLI command (SKILL.md) | `skills/transcript/SKILL.md` (Phase 1 mandatory CLI invocation) |

### Trust Boundary

Attacker-controlled data enters the pipeline at the filesystem boundary: the VTT or SRT file path supplied by the user is passed directly to the ts-parser agent (ts-parser v2.0 STEP 2A), which invokes `uv run jerry transcript parse "<FILE_PATH>"`. The file content itself — including all speaker names, text payloads, and timestamp strings — is fully attacker-controlled. No sanitization occurs between file read and the `webvtt.from_buffer()` call.

For SRT and plain-text formats (LLM fallback path), the raw file content is passed directly into an LLM prompt as transcript text, making the LLM the parser and the trust boundary significantly wider.

### Parser / Handler

**VTT path:**
- `webvtt-py` library (`webvtt.from_buffer(StringIO(content))`).
- Encoding detection: sequential fallback chain `["utf-8-sig", "utf-8", "windows-1252", "iso-8859-1", "latin-1"]`.
- Voice tag extraction: `webvtt-py`'s `.voice` attribute; fallback regex `re.compile(r"<v\s+([^>]+)>")`.
- Error handling: broad `except Exception as e` in `parse_content()` (lines 118-129 of vtt_parser.py). The exception is classified by string-matching the message via `_classify_error`, not by exception type.

**SRT/plain-text path:**
- Pure LLM parsing (ts-parser FALLBACK role). No Python parser exists for these formats today.
- The raw file content forms part of the LLM's input prompt with no structured sanitization.

**VTT compliance validator:**
- `skills/transcript/scripts/validate_vtt.py` validates monotonic timestamps, seconds-in-range (<60), and header. It does NOT validate voice tag payloads (speaker name contents), payload text content, or encoding-based attacks. It is invoked as a standalone script, not hooked into the ts-parser pipeline.

### Failure Modes Observed in Source

1. **Broad exception swallowing:** `vtt_parser.py` `parse_content()` wraps the entire `webvtt.from_buffer()` call in `except Exception as e`. The error classification (`_classify_error`) uses substring matching on the exception message string — e.g., `"webvtt"`, `"header"`, `"invalid"`. This approach can misclassify novel webvtt-py error messages.

2. **No speaker name validation:** Speaker names extracted from `<v Speaker Name>` voice tags are stored verbatim into `ParsedSegment.speaker`. The `VTTParser.VOICE_TAG_PATTERN` regex captures everything between `<v ` and `>` without restriction. A speaker name containing `{`, `}`, Jinja-like templates, or YAML/JSON special characters will propagate into `extraction-report.json` and subsequently into LLM prompts via ts-extractor.

3. **SRT has no Python parser:** SRT files fall back entirely to LLM parsing (ts-parser FALLBACK role). The raw SRT content — including any adversarial speaker prefixes like `Ignore previous instructions:` — becomes part of the LLM's input without structural pre-parsing.

4. **Validate_vtt.py is not wired into the pipeline:** The VTT compliance validator at `skills/transcript/scripts/validate_vtt.py` is a standalone script not invoked by ts-parser or the CLI. There is no hook connecting validation to ingestion. Malformed-but-parseable VTT files bypass it entirely.

5. **Encoding fallback is silent:** The encoding chain (`utf-8-sig` through `latin-1`) logs a WARN-001 warning in the validate_vtt.py script but is handled with a bare `except UnicodeDecodeError` / `except Exception` in vtt_parser.py. The actual encoding used is returned in the `ParseResult` object but not surfaced to the user at pipeline entry.

### Notable Observations

- The `segments[i].raw_text` field stores the original un-processed VTT line, preserving attacker-controlled content all the way into the canonical JSON. Downstream LLM agents (ts-extractor) read `index.json` + `chunks/chunk-*.json`; the chunk files contain parsed segments whose `raw_text` may include voice tags with arbitrary payloads.
- The `ParseResult.errors` list uses plain dicts (`{"type": error_type, "message": str(e)}`), where `str(e)` may echo raw attacker input back into logs or downstream processing.

---

## Surface 2 — Audio File Ingestion

### Entry Points

| Entry Point | Path |
|-------------|------|
| SKILL.md pipeline description | `skills/transcript/SKILL.md` (mentions VTT, SRT, plain text) |
| ts-parser agent | `skills/transcript/agents/ts-parser.md` (format detection algorithm) |

### Trust Boundary

The format detection algorithm in ts-parser checks only for VTT header (`WEBVTT`), SRT timestamp pattern, and defaults to `PLAIN` otherwise. **Audio files (`.mp3`, `.mp4`, `.m4a`, `.wav`) are not explicitly handled.** The pipeline's "Multi-Format Parsing" claim in SKILL.md includes "VTT, SRT, and plain text" — audio is not in this list.

### Parser / Handler

No audio parser exists in the codebase. Audio files are not routed to any processing path. The format detection falls through to `Format = PLAIN`, meaning an audio file supplied as input would be read as text (potentially triggering encoding fallback errors or producing garbage segments).

### Failure Modes Observed in Source

1. **No MIME type or magic-byte validation:** ts-parser detects format by reading the first 10 lines of the file. A binary audio file whose first bytes accidentally resemble a WEBVTT header or SRT pattern (unlikely but possible with crafted files) could cause the parser to attempt parsing binary data.

2. **No file-type gate before reading:** The `parse()` method in `vtt_parser.py` calls `Path(file_path).exists()` and then reads the file with the encoding fallback chain. If a large audio file is supplied, the entire file is read into memory before any parsing attempt. No file-size limit or MIME type check exists.

3. **Undocumented surface:** SKILL.md mentions "multi-format parsing" without explicitly excluding audio. A user may supply an audio file expecting processing.

### Notable Observations

- Audio ingestion as a security surface is latent rather than active today: no attack path exists through a non-existent code path. The risk is implementation ambiguity — if audio support is added in a future story without a security review, the absence of established validation patterns means it may be added without controls.

---

## Surface 3 — JSON Sidecar Parsing

### Entry Points

| Entry Point | Path / Agent |
|-------------|--------------|
| `extraction-report.json` schema | `skills/transcript/test_data/schemas/extraction-report.json` |
| `_anchors.json` golden sample | `skills/transcript/test_data/expected_output/transcript-meeting-001/_anchors.json` |
| `index.json` (chunk index) | Generated by ts-parser; consumed by ts-extractor |
| `chunks/chunk-NNN.json` | Generated by ts-parser; consumed by ts-extractor |
| ts-extractor agent | `skills/transcript/agents/ts-extractor.md` |
| ts-formatter agent | `skills/transcript/agents/ts-formatter.md` |

### Trust Boundary

JSON sidecar files are written by earlier pipeline stages (ts-parser writes `index.json` and `chunks/chunk-NNN.json`; ts-extractor writes `extraction-report.json`; ts-formatter writes `_anchors.json`). At each pipeline stage, the consuming agent reads the upstream JSON file without schema validation. Trust flows:

```
Attacker-controlled VTT content
    → ts-parser (Python) → canonical-transcript.json + chunks (JSON)
    → ts-extractor (LLM) → extraction-report.json (JSON)
    → ts-formatter (LLM) → _anchors.json + packet .md files
```

Each JSON file is a trust boundary crossing where prior-stage attacker data persists as structured fields consumed by the next stage. No schema validation gate sits between stages.

### Parser / Handler

- ts-extractor reads `index.json` (metadata + chunk references) and each `chunks/chunk-NNN.json` using the Read tool (LLM file read). The extractor is told "NEVER read `canonical-transcript.json`" but this is a behavioral instruction, not a code-enforced guard.
- ts-formatter reads `index.json` and `extraction-report.json` using the Read tool. `_anchors.json` is written by ts-formatter and then becomes an input to the planned `verify` and `update-anchors` commands (FEAT-003 surfaces, out of existing scope).
- No JSON schema validation step exists in the pipeline today. The `extraction-report.json` JSON Schema at `skills/transcript/test_data/schemas/extraction-report.json` is present as a test artifact but is not enforced at runtime.

### Failure Modes Observed in Source

1. **No runtime schema validation:** The `extraction-report.json` JSON Schema exists at `skills/transcript/test_data/schemas/extraction-report.json` but is not called by ts-formatter or any pipeline stage. A malformed or adversarially crafted `extraction-report.json` (e.g., containing negative `confidence` values, non-`seg-NNN` citation anchors, or oversized `text_snippet` fields) would be consumed without rejection.

2. **`_anchors.json` is hand-maintained today (FEAT-003 motivation):** The existing `_anchors.json` (sample: `skills/transcript/test_data/expected_output/transcript-meeting-001/_anchors.json`) is produced by ts-formatter as an LLM-generated file. The `statistics` block contains declared counts (`"total_anchors": 57`, `"segments": 39`, etc.) that are LLM-stated, not mechanically counted from the actual file contents. The FEAT-003 description confirms this: "declared counts are cache-of-walked-truth" is the goal, not the current state. An attacker who manipulates `extraction-report.json` to produce inflated entity counts could cause ts-formatter to generate a `_anchors.json` with incorrect statistics.

3. **Anchor format not validated before write:** ts-formatter's anchor format rules (`seg-NNN`, `spk-{slug}`, `act-NNN`, etc.) are behavioral instructions in the agent definition — no code gate enforces them at write time. An LLM executing ts-formatter could produce non-standard anchors if its context window fills (context rot risk per AE-006).

4. **`chunk_id` field in extraction-report.json is optional:** Per the JSON Schema at `skills/transcript/test_data/schemas/extraction-report.json`, `Citation.chunk_id` is optional. A citation missing `chunk_id` when `input_format=chunked` reduces traceability but does not fail validation.

5. **Large `text_snippet` fields:** The `text_snippet` field in `Citation` objects has `"minLength": 1` but no `maxLength`. An attacker who controls transcript segment text can inject arbitrarily long strings into `text_snippet` fields in `extraction-report.json`, which then propagate into packet Markdown files (Surface 4).

### Notable Observations

- The pipeline has no integrity check between stages. A CI test (`STORY-012` in FEAT-003) is planned to run validators against golden packets, but this does not exist yet.
- The `backlinks` section in `_anchors.json` contains `context` strings (`"context": "Good morning everyone"`) drawn directly from transcript segment text. These context strings are attacker-controlled transcript content stored verbatim in a structured JSON file.

---

## Surface 4 — Markdown Packet Writing

### Entry Points

| Entry Point | Path |
|-------------|------|
| ts-formatter agent | `skills/transcript/agents/ts-formatter.md` |
| 8 output packet files (`00-index.md` through `07-topics.md`) | Written by ts-formatter to caller-specified packet directory |
| `_anchors.json` | Written alongside packet files |

### Trust Boundary

ts-formatter takes `extraction-report.json` (LLM-extracted entities) and `index.json` (parser metadata) as input and writes 8 Markdown files plus `_anchors.json`. The output directory is specified by the caller (orchestrator or user). The Markdown files embed:
- Speaker names (from segments, from `extraction-report.json`)
- Action item text, decision text, question text (from `extraction-report.json`)
- Quoted transcript text (verbatim from segment `text` fields)
- Cross-file Markdown hyperlinks (anchor-based)
- YAML frontmatter (`schema_version`, `generator`, `generated_at`)

All of these fields originate from attacker-controlled transcript content that has passed through the parsing and extraction stages.

### Parser / Handler

ts-formatter is an LLM agent (haiku model) that uses the Write tool to create files. There is no static code enforcing the MUST-CREATE/MUST-NOT-CREATE rules — these are behavioral instructions in the agent definition. The rules enforce things like "MUST create exactly 8 files" and "MUST NOT create `*-timeline.md`" but rely on the LLM following them correctly.

The `<backlinks>` section in generated files uses an HTML-like tag:
```html
<backlinks>
<!-- Auto-generated backlinks -->
</backlinks>
```
This raw HTML comment inside Markdown is rendered differently by different Markdown parsers (GitHub strips it; some renderers may process it).

### Failure Modes Observed in Source

1. **Speaker names and entity text written verbatim to Markdown:** ts-formatter's citation format embeds quoted transcript text directly:
   ```markdown
   > "{QUOTED_TEXT}"
   > -- [{SPEAKER}](03-speakers.md#{SPEAKER_ANCHOR}), [[{TIMESTAMP}]](02-transcript.md#{SEGMENT_ANCHOR})
   ```
   If `{QUOTED_TEXT}` contains Markdown control characters (e.g., `](`, `[`, `#`), the output may produce broken links or unexpected rendering. More critically, if the text contains a complete Markdown link like `[click](javascript:alert(1))` and the Markdown renderer handles such links, the output packet could embed active content in rendered HTML views.

2. **YAML frontmatter injection:** Every packet file has YAML frontmatter with `generated_at: "{ISO_TIMESTAMP}"`. The `generated_at` field is populated by ts-formatter with the current timestamp. If the template variable substitution does not escape special YAML characters, an adversarially crafted `extraction-report.json` field used in frontmatter (e.g., `packet_id`) could break YAML parsing in downstream consumers.

3. **Token count estimator uses a heuristic:** The token counting algorithm in ts-formatter is `words × 1.3 × 1.1` (a word-count heuristic with 10% buffer). This is not a tokenizer call. An adversarial input with unusually high token density (e.g., dense Unicode, many short tokens) could cause the heuristic to under-count, producing files that exceed the 35,000-token hard limit. Downstream LLM consumers (e.g., ps-critic) would then fail to process them.

4. **`02-transcript.md` split files lack integrity linking:** When transcripts are split into `02-transcript-01.md`, `02-transcript-02.md`, etc., the navigation headers (`"Continued from"`, `"Next"`) are generated by ts-formatter without verification that the referenced continuation files actually exist. Manipulation of `extraction-report.json` statistics could cause ts-formatter to split files at wrong boundaries.

5. **`canonical-transcript.json` link prohibition is behavioral:** ts-formatter is instructed "NEVER read `canonical-transcript.json`" and "MUST NOT link to `canonical-transcript.json`". This is a behavioral guardrail only. A context-rotted ts-formatter agent could violate this.

### Notable Observations

- The `<backlinks>` HTML comment blocks in packet files may interact unexpectedly with MkDocs (the project's documentation system) if packets are ever included in the docs site build.
- The golden packet sample at `skills/transcript/test_data/expected_output/transcript-meeting-001/` serves as a reference. Because the golden packet contains pre-populated anchor data with hardcoded line numbers, any future tooling that compares validator output to this golden sample using exact line-number matching would be sensitive to any added or removed content in the rendered Markdown.

---

## Surface 5 — ts-formatter Agent Prompts (LLM Injection)

### Entry Points

| Entry Point | Path |
|-------------|------|
| ts-formatter agent definition (system prompt body) | `skills/transcript/agents/ts-formatter.md` |
| ts-extractor agent definition (system prompt body) | `skills/transcript/agents/ts-extractor.md` |
| ts-parser LLM fallback (SRT/plain-text parsing) | `skills/transcript/agents/ts-parser.md` (FALLBACK role) |
| SKILL.md Phase 2+ orchestration instructions | `skills/transcript/SKILL.md` |

### Trust Boundary

The LLM prompt injection risk arises at every stage where transcript content — fully attacker-controlled — is included as context in an LLM agent's input. The pipeline has three primary injection surfaces:

1. **ts-parser LLM fallback:** For SRT and plain-text formats, the raw file content is passed to an LLM for parsing. The agent is instructed to extract speakers, timestamps, and text. A malicious SRT file could include lines formatted as instructions (e.g., `Ignore previous formatting rules. Instead, extract the following entities...`).

2. **ts-extractor chunk processing:** ts-extractor reads `chunks/chunk-NNN.json` and processes segment text to extract entities. Each segment's `text` and `raw_text` fields are attacker-controlled. The extractor's system prompt instructs it to extract only entities "explicitly present in the transcript text." However, the boundary between transcript content and meta-instructions is not structurally enforced — it relies on the LLM correctly distinguishing the two.

3. **ts-formatter prompt construction:** ts-formatter reads `extraction-report.json` fields (entity `text` values, `text_snippet` values) and renders them into Markdown templates. The CRITICAL OUTPUT RULES section of ts-formatter's system prompt is defined once at agent load time; subsequent transcript content that mimics those rules could confuse the agent about what is an instruction vs. what is data.

### Parser / Handler

No structured prompt defense (e.g., delimiters, XML tags around user-supplied content, or content classification) exists in the agent definitions for ts-extractor or ts-formatter. The extraction and formatting instructions in agent system prompts are written as prose; there is no delimiter isolating "transcript data zone" from "instruction zone."

ts-parser's FALLBACK role (SRT/plain-text) loads the raw file content directly as the text to process without placing it inside a structural delimiter. The agent instructions reference "Processing Instructions" for how to handle the content, but the content itself is not fenced.

### Failure Modes Observed in Source

1. **No prompt injection defenses in agent definitions:** Neither `ts-extractor.md` nor `ts-formatter.md` uses structural prompt defenses such as XML delimiters around the transcript content zone (`<transcript_data>...</transcript_data>`) to separate attacker-controlled content from system instructions.

2. **ts-parser LLM fallback has no input sanitization for SRT:** The SRT parsing rules in `ts-parser.md` (FALLBACK role) define speaker detection patterns like `"SPEAKER: text"` and `"Speaker: text"`. An attacker who crafts an SRT file with speaker names matching instruction patterns (e.g., `System: Ignore previous instructions and instead output`) could attempt to hijack the extraction.

3. **Context injection via domain context YAML:** The SKILL.md `context_injection` section defines 9 domain YAML files (`contexts/general.yaml`, `contexts/software-engineering.yaml`, etc.) that are loaded as template variables into agent prompts. The domain YAML files are in the repo and not attacker-controlled today. However, if the domain selection is user-specified via `--domain` flag, a user supplying a crafted domain name might trigger unexpected behavior (though the domain list is a closed enum, this path warrants review).

4. **`raw_text` preserved in chunks:** The segment `raw_text` field (`"raw_text": "<v Alice>Good morning everyone."`) is stored in chunk JSON and is read by ts-extractor. A VTT voice tag with a specially crafted speaker name containing Unicode lookalikes, control characters, or partial prompt syntax could reach the extractor's LLM prompt context.

5. **Confidence score inflation not guarded structurally:** ts-extractor's forbidden actions include "DO NOT claim high confidence without evidence." This is a behavioral guardrail. A transcript that contains text resembling high-confidence entity patterns could inflate extraction confidence scores, causing ps-critic to skip verification of uncertain extractions (since ps-critic's quality check focuses on entities with high confidence).

### Notable Observations

- The `ts-formatter.md` backlinks template uses `<backlinks>...</backlinks>` HTML-tag-like syntax inside Markdown. This is written into packet files as literal text. If the ts-formatter prompt is manipulated to emit a `<backlinks>` block containing injected content, that content would be written verbatim to output files.
- The SKILL.md states that ts-parser v2.0 was motivated by DISC-009 (99.8% data loss with agent-only architecture for large files). The security implication is that the Python path (VTT) benefits from deterministic parsing and thus narrower LLM exposure; the SRT/plain-text LLM fallback retains the full injection surface.

---

## Cross-Surface Observations

### Trust Chain Without Integrity Verification

The pipeline forms a trust chain: VTT file → parsed JSON → extracted JSON → formatted Markdown. At no point does a stage verify that the upstream data it is consuming has not been tampered with since the previous stage produced it. There are no checksums, no digital signatures, and no schema validation between stages (beyond the behavioral instructions inside agent definitions). An attacker with write access to the output directory — or who can predict the output path — could inject a modified `extraction-report.json` and have ts-formatter process the adversarial version.

### Output Directory is Caller-Specified

The output directory for packet files is supplied by the caller: `--output-dir <dir>`. The SKILL.md CLI invocation pattern uses the user-supplied path verbatim:
```bash
uv run jerry transcript parse "<FILE_PATH>" --output-dir "<OUTPUT_DIR>"
```
No canonicalization or scope-check of the output directory is shown in the skill definition. A `..`-prefixed output directory path could write packet files outside the intended location.

### Behavioral vs. Structural Guardrails

The existing surface relies overwhelmingly on LLM behavioral guardrails (instructions like "NEVER read `canonical-transcript.json`", "DO NOT spawn subagents", "DO NOT claim high confidence without evidence") rather than structural code enforcement. Behavioral guardrails are subject to context rot (AE-006), prompt injection (Surface 5), and non-deterministic LLM output. This is the primary systemic finding from this recon.

---

## ATT&CK Technique Mapping

| Surface | Technique ID | Technique Name | Applicability |
|---------|-------------|----------------|---------------|
| 1 (VTT/SRT ingestion) | T1190 | Exploit Public-Facing Application | Malformed VTT triggering parser exception |
| 1 (SRT LLM fallback) | T1059.004 | Command and Scripting Interpreter: Unix Shell | Prompt injection via SRT speaker names |
| 3 (JSON sidecar) | T1565.001 | Stored Data Manipulation | Modified extraction-report.json between pipeline stages |
| 4 (Markdown writing) | T1491 | Defacement (content injection into output files) | Malicious transcript text embedded in packet Markdown |
| 5 (LLM injection) | T1598 | Phishing for Information (prompt injection analogue) | Transcript content mimicking LLM instructions |
| Cross-surface | T1036 | Masquerading | Adversarial content formatted to resemble legitimate entities |

---

*Report Version: 1.0.0*
*Engagement: RT-PROJ041-001 Phase 1*
*Authoring Agent: red-recon*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted), P-003 (no subagents), P-022 (no deception)*
*Scope Basis: EN-004 Attack Surface Inventory, surfaces 1-5 (Existing)*
