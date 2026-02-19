# Transcript Playbook

> **Skill:** transcript
> **SKILL.md:** [transcript/SKILL.md](https://github.com/geekatron/jerry/blob/main/skills/transcript/SKILL.md)
> **Trigger keywords:** transcript, meeting notes, parse recording, meeting recording, VTT, SRT, captions

## Document Sections

| Section | Purpose |
|---------|---------|
| [When to Use](#when-to-use) | Activation criteria and exclusions |
| [Prerequisites](#prerequisites) | What must be in place before invoking |
| [Step-by-Step](#step-by-step) | Primary invocation path |
| [Examples](#examples) | Concrete invocation examples |
| [Troubleshooting](#troubleshooting) | Common failure modes |
| [Domain Contexts](#domain-contexts) | The 9 supported domain contexts with selection guidance |
| [Input Formats](#input-formats) | VTT, SRT, and plain text format handling |
| [Related Resources](#related-resources) | Cross-references to other playbooks and SKILL.md |

---

## When to Use

> **Invocation:** The transcript skill can be triggered by keyword detection (e.g.,
> "transcript", "meeting notes", "parse recording") or explicitly via the `/transcript`
> command. When triggered by keywords, Claude will ask for the file path if not provided.
> The skill uses a hybrid Python+LLM architecture: the Python CLI parser runs automatically
> for VTT files (~1,250x cheaper than LLM parsing), while SRT and plain text files use
> LLM-based parsing directly. The LLM instructions (ts-parser agent) handle format detection
> and Python invocation automatically — no manual CLI knowledge is required from the user.

### Use this skill when:

- You have a meeting recording transcript file (VTT, SRT, or plain text) that you need
  converted into structured notes
- You want to extract action items, decisions, open questions, or key topics from a meeting
- You need to process a Zoom, Teams, or other conferencing platform subtitle/caption file
- You want to generate a navigable Markdown knowledge packet from a recorded conversation
- You need domain-specific entity extraction from a meeting (commitments, architectural
  decisions, security findings, UX insights, etc.)
- You are processing a post-mortem, standup, sprint review, or similar structured meeting
  where structured output is required for follow-up

### Do NOT use this skill when:

- You want to summarize a document that is not a transcript or meeting recording — use
  `/problem-solving` for general research and analysis tasks
- You want to analyze a conversation that is already in structured note form — the skill
  requires a raw transcript file as input
- You have no transcript file to provide — the Phase 1 CLI parser requires an actual file
  path; it cannot operate on text pasted into the conversation

---

## Prerequisites

- **`JERRY_PROJECT` is set** — an active Jerry project is required (H-04). If not set,
  the session will not proceed. Run `jerry session start` to establish a session.
- **`uv` is installed** — all Python execution uses `uv run` (H-05). The Phase 1 CLI
  parser MUST be invoked via `uv run jerry transcript parse`. Never use `python` directly.
- **A transcript file is available** on the local filesystem — the parser requires an
  absolute or resolvable path to a VTT, SRT, or plain text transcript file.
- **The `jerry` CLI is installed** — verify with `uv run jerry --help`. The transcript
  subcommand must be available (`uv run jerry transcript parse --help`).
- **An output directory is specified or the default is acceptable** — output goes to
  `./transcript-output/` by default. Specify `--output-dir` to control placement.

---

## Step-by-Step

### Primary Path: Processing a VTT transcript with the two-phase workflow

The transcript skill uses a mandatory two-phase architecture:

- **Phase 1 (CLI — deterministic):** Python parser converts the raw file into structured
  JSON chunks. This is ~1,250x cheaper than LLM parsing and produces 100% accurate
  timestamps. This phase MUST use the CLI — never ask Claude to parse VTT directly.
  *(Cost basis: A 1-hour VTT transcript produces ~280K tokens of structured data.
  The Python parser processes this at zero API token cost in <1 second. LLM parsing
  of the same data requires ~280K input tokens + ~50K output tokens at API rates,
  yielding a ~1,250:1 cost ratio. See [SKILL.md Design Rationale](https://github.com/geekatron/jerry/blob/main/skills/transcript/SKILL.md#design-rationale-hybrid-pythonllm-architecture) for full methodology.)*
- **Phase 2+ (LLM agents — semantic):** Agents read the JSON chunks and produce the
  structured Markdown output packet.

**Steps:**

1. **Identify your transcript file path and desired output directory.** Use an absolute
   path to avoid ambiguity. Example:
   ```
   /Users/me/meetings/quarterly-review.vtt
   ```

2. **Invoke the transcript skill** with the file path and any optional flags:
   ```
   /transcript /Users/me/meetings/quarterly-review.vtt --output-dir /Users/me/output/quarterly-review/
   ```
   Or with a domain:
   ```
   /transcript /Users/me/meetings/quarterly-review.vtt --output-dir /Users/me/output/ --domain software-engineering
   ```

3. **Phase 1 executes automatically** — Claude runs the CLI parser:
   ```bash
   uv run jerry transcript parse "/Users/me/meetings/quarterly-review.vtt" \
       --output-dir "/Users/me/output/quarterly-review/"
   ```
   This produces three files in the output directory:
   - `index.json` (~8KB) — chunk metadata and speaker summary
   - `chunks/chunk-*.json` (~130KB each) — transcript segments in processable chunks
   - `canonical-transcript.json` (~930KB) — full parsed output **(NEVER read into context — see warning below)**

4. **Phase 2 — ts-extractor agent runs** — reads `index.json` and each `chunks/chunk-*.json`
   sequentially, then writes `extraction-report.json` with all extracted entities
   (action items, decisions, questions, topics, speakers).

5. **Phase 3 — ts-formatter agent runs** — reads `index.json` and `extraction-report.json`,
   then writes the 8-file Markdown output packet:
   - `00-index.md` — navigation hub
   - `01-summary.md` — executive summary
   - `02-transcript.md` — full formatted transcript
   - `03-speakers.md` — speaker directory
   - `04-action-items.md` — action items with citations
   - `05-decisions.md` — decisions with context
   - `06-questions.md` — open questions
   - `07-topics.md` — topic segments

6. **Phase 4 — ts-mindmap agents run** (unless `--no-mindmap` was specified) — generate
   visual summaries in `08-mindmap/mindmap.mmd` (Mermaid) and/or
   `08-mindmap/mindmap.ascii.txt` (ASCII). Mindmaps are ON by default per [ADR-006](https://github.com/geekatron/jerry/blob/main/skills/transcript/SKILL.md#design-rationale-mindmap-default-on-decision).

7. **Phase 5 — ps-critic runs** — validates quality against the >= 0.90 threshold (the transcript skill uses a skill-specific threshold lower than the general 0.92 SSOT; see the SKILL.md Design Rationale section for the selection rationale). If quality is below threshold, revision is triggered automatically.

8. **Review the output packet** — open `00-index.md` as the entry point for navigation
   across all generated files.

> **CRITICAL WARNING — `canonical-transcript.json`:** This file is generated by Phase 1
> and can be ~930KB (~280K tokens for large meetings). Agents MUST NEVER read
> `canonical-transcript.json` into context — it will fill the context window, cause
> summarization, and result in data loss. Always use `index.json` (~8KB) and
> `chunks/chunk-*.json` (~130KB each) instead. This is a documented architectural
> constraint (SKILL.md Large File Handling).

---

## Examples

### Example 1: Processing a VTT file with default settings

**User request:** `"/transcript /Users/me/meetings/standup-2026-02-18.vtt"`

**System behavior:** Claude invokes the Phase 1 CLI parser:
```bash
uv run jerry transcript parse "/Users/me/meetings/standup-2026-02-18.vtt" \
    --output-dir "./transcript-output/"
```
The parser produces `index.json`, `chunks/chunk-*.json`, and `canonical-transcript.json`
in `./transcript-output/`. Phase 2 agents then run ts-extractor, ts-formatter, and
ts-mindmap. The final output is an 8-file Markdown packet plus a mindmap in
`./transcript-output/`, with `00-index.md` as the navigation entry point.

---

### Example 2: Processing a software engineering standup with domain context

**User request:** `"/transcript /Users/me/meetings/sprint-review.vtt --output-dir /Users/me/notes/ --domain software-engineering"`

**System behavior:** Claude invokes the Phase 1 CLI parser with the `--domain` flag:
```bash
uv run jerry transcript parse "/Users/me/meetings/sprint-review.vtt" \
    --output-dir "/Users/me/notes/" \
    --domain software-engineering
```
The `software-engineering` domain context loads extraction rules tuned for standups and
sprint events: commitments, blockers, and risks are extracted in addition to the standard
action items, decisions, and questions. The output packet in `/Users/me/notes/` contains
domain-enriched entities attributed to speakers, with citations linking back to timestamps
in the original transcript.

---

### Example 3: Processing an SRT file without mindmaps

**User request:** `"/transcript /Users/me/captions/webinar.srt --no-mindmap"`

**System behavior:** Claude invokes the Phase 1 CLI parser. Because the input is an SRT
file (not VTT), LLM-based parsing is used instead of the Python parser — SRT and plain
text formats do not have the deterministic Python path that VTT uses. The `--no-mindmap`
flag suppresses the ts-mindmap phase. The output packet contains the standard 8 files
(00-index.md through 07-topics.md) but no `08-mindmap/` directory.

---

### Example 4: Processing a user research interview

**User request:** `"/transcript /Users/me/research/user-interview-001.vtt --domain user-experience --output-dir /Users/me/research/processed/"`

**System behavior:** Claude runs Phase 1 then orchestrates LLM agents with the
`user-experience` domain context, which activates verbatim quote preservation. The
extracted entities include user insights, pain points, and verbatim quotes attributed to
participants. The output is suitable for a UX research repository.

---

## Troubleshooting

| Symptom | Cause | Resolution |
|---------|-------|------------|
| `uv: command not found` when running Phase 1 | `uv` is not installed or not on PATH | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh`. Verify with `uv --version`. See H-05 — NEVER use `python` directly as a workaround. |
| `No such file or directory` error on the transcript file | The file path provided is incorrect or the file does not exist at that location | Verify the full absolute path to the transcript file. Use tab-completion or `ls` to confirm. Always quote paths that contain spaces. |
| `canonical-transcript.json` was read and context filled up / output is incomplete or summarized | An agent mistakenly read `canonical-transcript.json` into context, exhausting the token budget and triggering LLM summarization | Never read `canonical-transcript.json`. Use `index.json` (entry point, ~8KB) and `chunks/chunk-*.json` (~130KB each). If this happened, restart the Phase 2+ pipeline from ts-extractor using the existing chunk files. |
| Phase 1 CLI exits with non-zero code / `ParseError` | The transcript file is malformed, has an unsupported encoding, or is corrupted | Check the error message for the specific line number. VTT files must have a valid `WEBVTT` header. Try opening the file in a text editor to confirm it is valid UTF-8 and has correct VTT syntax. |
| Quality review score below 0.90 — ps-critic rejects output | Extraction quality was insufficient: missing citations, incomplete entity coverage, or formatting errors in the packet files | The ps-critic agent will identify specific defects. Address the flagged issues in the relevant packet file (e.g., `04-action-items.md`). Common causes: very short chunks (too few entities), low-quality source transcript (heavy background noise, overlapping speech), or unsupported speaker labeling format. |
| Domain-specific entities are missing from the output | The `--domain` flag was not specified, or the wrong domain was selected | Re-run the Phase 2+ agents (ts-extractor onwards) with the correct `--domain` flag. The Phase 1 JSON output (chunks) can be reused — only re-run from ts-extractor. See the domain table in the Domain Contexts section below. |
| Mindmap generation fails but core packet is intact | ts-mindmap agent encountered an error (e.g., content too sparse for a meaningful mindmap) | This is expected graceful degradation per [ADR-006](https://github.com/geekatron/jerry/blob/main/skills/transcript/SKILL.md#design-rationale-mindmap-default-on-decision). The 8-file packet remains valid. Use `--no-mindmap` on future invocations if mindmaps are not needed, or investigate the ts-mindmap error output for specific causes. |
| Agent fails mid-execution (e.g., ts-extractor or ts-formatter crashes partway through) | Token budget exhaustion, session interruption, or agent error during Phase 2+ processing | **1. Identify:** Check which phase failed — Phase 1 (CLI) artifacts (`index.json`, `chunks/`) are always recoverable since they are written by the Python parser. **2. Salvage:** Phase 1 output is reusable — the JSON chunks do not need to be regenerated. **3. Recover:** Re-run from the failed phase only: if ts-extractor failed, re-invoke it with the existing `index.json` and `chunks/` directory; if ts-formatter failed, re-invoke it with the existing `extraction-report.json`. The CLI parser does NOT need to re-run. |

---

## Domain Contexts

The transcript skill supports 9 domain contexts. Select the domain that best matches your
meeting type using the `--domain <name>` flag. If no domain is specified, `general` is
the default.

| Domain | Use For | Key Additional Entities |
|--------|---------|------------------------|
| `general` | Any transcript (default) | speakers, topics, questions |
| `transcript` | Base transcript entities, extends general | + segments, timestamps |
| `meeting` | Generic meetings | + action items, decisions, follow-ups |
| `software-engineering` | Standups, sprint planning, code reviews | + commitments, blockers, risks |
| `software-architecture` | ADR discussions, design sessions | + architectural decisions, alternatives, quality attributes |
| `product-management` | Roadmap planning, feature prioritization | + feature requests, user needs, stakeholder feedback |
| `user-experience` | Research interviews, usability tests | + user insights, pain points, verbatim quotes |
| `cloud-engineering` | Post-mortems, capacity planning | + incidents, root causes (blameless culture) |
| `security-engineering` | Security audits, threat modeling | + vulnerabilities, threats (STRIDE), compliance gaps |

**Domain selection examples:**
```bash
uv run jerry transcript parse "standup.vtt" --output-dir "./out/" --domain software-engineering
uv run jerry transcript parse "postmortem.vtt" --output-dir "./out/" --domain cloud-engineering
uv run jerry transcript parse "user-interview.vtt" --output-dir "./out/" --domain user-experience
```

---

## Input Formats

The transcript skill supports three input formats. The Phase 1 CLI parser handles each
as follows:

| Format | Extension | Parsing Method | Notes |
|--------|-----------|----------------|-------|
| **VTT** (WebVTT) | `.vtt` | Python parser (deterministic) | ~1,250x cheaper than LLM; 100% timestamp accuracy; MUST use CLI |
| **SRT** (SubRip) | `.srt` | LLM-based parsing | Full LLM API cost (~280K+ tokens for 1-hour file); processed by ts-extractor agent directly |
| **Plain text** | `.txt` | LLM-based parsing | Full LLM API cost; meeting notes, chat logs, or any unstructured transcript text |

**Command syntax for each format:**
```bash
# VTT (Zoom, Teams, Google Meet captions)
uv run jerry transcript parse "meeting.vtt" --output-dir "./output/"

# SRT (subtitle files)
uv run jerry transcript parse "captions.srt" --output-dir "./output/"

# Plain text meeting notes
uv run jerry transcript parse "notes.txt" --output-dir "./output/"
```

---

## Related Resources

- [SKILL.md](https://github.com/geekatron/jerry/blob/main/skills/transcript/SKILL.md) — Authoritative technical reference for
  the transcript skill, including full agent pipeline specifications, domain context YAML
  schemas, ADR design rationale, and quality threshold documentation
- [Problem-Solving Playbook](./problem-solving.md) — Use when you need to research,
  analyze, or investigate a topic (not for processing transcript files)
- [Orchestration Playbook](./orchestration.md) — Use when designing multi-phase workflows;
  the transcript skill itself uses an internal orchestration pipeline that can serve as a
  reference pattern
