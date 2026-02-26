# GitHub Issue Draft: Diataxis Documentation Framework Skill

## Document Sections

| Section | Purpose |
|---------|---------|
| [Title](#title) | Issue title |
| [Labels](#labels) | Issue labels |
| [Body](#body) | Full issue body |
| [The problem](#the-problem) | Why this skill is needed |
| [Why a skill with agents](#why-a-skill-with-agents) | Architectural rationale |
| [Proposed skill architecture](#proposed-skill-architecture) | Directory structure |
| [Agent specifications](#agent-specifications) | Per-agent design with Diataxis principles |
| [Agent governance summary](#agent-governance-summary) | H-34 compliance table |
| [Routing and trigger keywords](#routing-and-trigger-keywords) | Trigger map entry with collision analysis |
| [Integration points](#integration-points) | Cross-skill connections |
| [Diataxis standards rule file](#diataxis-standards-rule-file) | Content specification for diataxis-standards.md |
| [SKILL.md description draft](#skillmd-description-draft) | H-26 compliant description text |
| [What this enables](#what-this-enables) | Capability summary |
| [Implementation plan](#implementation-plan) | Four-phase rollout |
| [Acceptance criteria](#acceptance-criteria) | Verification checklist |
| [Why this matters](#why-this-matters) | Strategic context |

---

## Title

Add /diataxis skill — four-quadrant documentation framework with specialized agents for tutorials, how-to guides, reference, and explanation

## Labels

enhancement

## Body

### The problem

Jerry has skills for systems engineering, adversarial quality, problem-solving, architecture decisions, offensive security, and even a personality layer. But it has nothing for the thing that makes all of those skills accessible to anyone who isn't already inside the framework: **documentation**.

Right now, Jerry has no systematic methodology for deciding what type of documentation to create or which structure and quality criteria to apply. Rule files follow structural conventions (H-23/H-25/H-26) but the documentation methodology — what to write, for whom, and with what relationship to the reader — is undirected. The result is docs that blur the line between teaching someone how to use the framework and explaining why the framework works the way it does — and neither job gets done well when they're tangled together.

The [Diataxis framework](https://diataxis.fr/) solves this. It's a lightweight, proven documentation methodology [adopted by Cloudflare, Gatsby, Vonage, and hundreds of other projects](https://diataxis.fr/adoption/). It identifies four documentation types organized along two axes:

|  | **Acquisition** (learning) | **Application** (working) |
|--|:--:|:--:|
| **Practical** (doing) | Tutorials | How-to Guides |
| **Theoretical** (understanding) | Explanation | Reference |

Each quadrant has distinct quality criteria, anti-patterns, and a specific relationship to the reader. Mixing them is the root cause of documentation that feels simultaneously too detailed and not helpful enough.

You don't take the same line through a couloir that you take through a meadow. Same mountain, different terrain, different technique. That's Diataxis — four types of terrain, four ways to ride.

### Why a skill with agents

Jerry's architecture is built for exactly this. Skills encapsulate domain methodology. Agents encode specialized expertise. The Diataxis framework maps cleanly onto Jerry's agent model:

- **Four documentation types** -> four specialist writer agents, each encoding the quality criteria, anti-patterns, and voice for their quadrant
- **Two axes** (practical/theoretical, acquisition/application) -> routing logic that classifies documentation requests and sends them to the right agent
- **Quality criteria per quadrant** -> built-in self-review against Diataxis principles before presenting output
- **Cross-quadrant awareness** -> agents know what belongs in their quadrant and what should be redirected elsewhere

This is not a template collection. It's a documentation methodology engine that understands the difference between "teach me" and "show me how" and "tell me about" and "what are the options" — and produces the right kind of document for each.

### Proposed skill architecture

```
/diataxis
├── SKILL.md                           # Skill definition, triggers, routing
├── agents/
│   ├── diataxis-tutorial.md           # Tutorial writer (learning-oriented)
│   ├── diataxis-tutorial.governance.yaml
│   ├── diataxis-howto.md              # How-to guide writer (goal-oriented)
│   ├── diataxis-howto.governance.yaml
│   ├── diataxis-reference.md          # Reference writer (information-oriented)
│   ├── diataxis-reference.governance.yaml
│   ├── diataxis-explanation.md        # Explanation writer (understanding-oriented)
│   ├── diataxis-explanation.governance.yaml
│   ├── diataxis-classifier.md         # Classifies docs into quadrants
│   ├── diataxis-classifier.governance.yaml
│   ├── diataxis-auditor.md            # Audits existing docs for quadrant mixing
│   └── diataxis-auditor.governance.yaml
├── rules/
│   └── diataxis-standards.md          # Quality criteria per quadrant
└── templates/
    ├── tutorial-template.md
    ├── howto-template.md
    ├── reference-template.md
    └── explanation-template.md
```

**Template structural differentiation:**

| Template | Required Structural Elements |
|----------|------------------------------|
| tutorial-template.md | Numbered steps; prerequisite block; "What you will achieve" intro; each step has observable output marker |
| howto-template.md | Goal statement in title; numbered steps (task-oriented); "If you need X, do Y" variant handling sections |
| reference-template.md | Table or definition-list structure; no narrative prose; standard entry format per entity type |
| explanation-template.md | Continuous prose sections; no numbered steps; "Why" framing; acknowledges complexity and multiple perspectives |

### Agent specifications

**`diataxis-tutorial`** — Tutorial Writer
- Cognitive mode: `systematic` (step-by-step procedural completeness; tutorials are concrete, sequential experiences — each step produces a visible result before the next begins)
- Expertise: Pedagogical design, learning-by-doing methodology, tutorial sequencing
- Key Diataxis principles encoded:
  - Tutorials are *experiences*, not *explanations* — "the first rule of teaching: don't try to teach"
  - Must be meaningful (sense of achievement), successful (completable), logical (sensible progression), and usefully complete (exposes all necessary actions)
  - Minimize explanation ruthlessly; stay concrete; ignore alternatives
  - Every step produces a visible, comprehensible result
  - Aspire to perfect reliability — unexpected outcomes destroy learner confidence
- Anti-patterns to prevent: abstraction, extended explanation, offering choices, information overload
- Jerry voice integration: Output must conform to Jerry's documentation voice conventions. Specifically: prefer active voice, direct address, and concrete examples over passive and abstract descriptions. Diataxis quadrant principles take precedence for structure; Jerry voice conventions apply to prose style. Voice guidelines per quadrant will be specified in `diataxis-standards.md` Section 5.
- Model: `sonnet` (procedural step-by-step writing with concrete outputs; systematic mode reduces need for opus-level reasoning)

**`diataxis-howto`** — How-to Guide Writer
- Cognitive mode: `convergent` (focused on solving a specific problem)
- Expertise: Goal-oriented technical writing, problem-field navigation, procedural clarity
- Key Diataxis principles encoded:
  - How-to guides are about *goals and problems*, not tools — written from user perspective
  - Contain action and only action — no digression, explanation, or teaching
  - Address real-world complexity with adaptability; practical usability over completeness
  - Precise titles that state what will be accomplished
  - Achieve flow: smooth progress grounded in user activities
- Anti-patterns to prevent: conflating with tutorials, tool-focused guidance, unnecessary procedures, completeness over focus
- Jerry voice integration: Output must conform to Jerry's documentation voice conventions. Active voice preferred; how-to guides use direct address ("Run the command", not "The command should be run"). Voice guidelines per quadrant will be specified in `diataxis-standards.md` Section 5.
- Model: `sonnet` (focused procedural writing, clear task)

**`diataxis-reference`** — Reference Writer
- Cognitive mode: `systematic` (procedural completeness, structured description)
- Expertise: Technical description, API documentation, structured information architecture
- Key Diataxis principles encoded:
  - Sole aim: describe as succinctly as possible, in an orderly way
  - Must be wholly authoritative with no ambiguity — functions like a map
  - Mirror the machinery's structure in documentation organization
  - Neutral description is the key imperative — state facts plainly
  - Use standard patterns and consistent format for consultability
  - Include examples that illustrate without instructing
- Anti-patterns to prevent: marketing claims, instructions/recipes, narrative explanation, stylistic flourishes, auto-generated docs as sole strategy
- Jerry voice integration: Output must conform to Jerry's documentation voice conventions. Neutral, plain language preferred; reference documentation avoids personality flourishes while remaining precise and readable. Voice guidelines per quadrant will be specified in `diataxis-standards.md` Section 5.
- Model: `sonnet` (systematic description, structured output)

**`diataxis-explanation`** — Explanation Writer
- Cognitive mode: `divergent` (explores broadly, makes connections, provides context)
- Expertise: Conceptual writing, design rationale, contextual analysis, architectural narrative
- Key Diataxis principles encoded:
  - Explanation is discursive — permits reflection, deepens understanding
  - Answers "Can you tell me about...?" — broader perspective than task-focused docs
  - Make connections across topics; provide context for design decisions, historical reasons, constraints
  - Acknowledge perspective and opinion; multiple viewpoints strengthen understanding
  - Best consumed away from active work — enriches thinking, not immediate action
- Anti-patterns to prevent: instructional content creeping in, scattering explanation across other sections, treating explanation as less important
- Jerry voice integration: Output must conform to Jerry's documentation voice conventions. Explanation documents may use richer prose than other quadrants while maintaining clarity. Active voice and direct address remain preferred. Voice guidelines per quadrant will be specified in `diataxis-standards.md` Section 5.
- Model: `opus` (conceptual exploration requires complex reasoning)

**`diataxis-classifier`** — Documentation Classifier (T1 Read-Only)
- Cognitive mode: `convergent` (evaluates input, produces classification decision)
- Expertise: Diataxis quadrant analysis, documentation type identification, content routing
- Architecture: **T1 classifier (read-only, no delegation)**. The classifier receives a documentation request or existing document, analyzes it against the two Diataxis axes (practical/theoretical, acquisition/application), and returns a structured classification result. The classifier does NOT invoke writer agents — the caller (user or orchestrator) is responsible for invoking the appropriate writer agent based on the classification. This design keeps the classifier at T1 (Read, Glob, Grep), avoids H-36 circuit breaker concerns, and maintains clear separation of classification from generation per the specialist agent pattern.
- Multi-quadrant decomposition: When a request spans multiple quadrants, the classifier returns a decomposition recommendation listing each quadrant with rationale, the recommended document sequence (e.g., "Tutorial first, then Reference"), and which content belongs in which quadrant. The caller is responsible for invoking writer agents in the recommended sequence.
- **Classifier Output Schema:**
  ```
  {
    "quadrant": "tutorial" | "howto" | "reference" | "explanation" | "multi",
    "confidence": float (0.0-1.0),
    "rationale": string (1-2 sentences explaining axis placement),
    "axis_placement": {
      "practical_theoretical": "practical" | "theoretical" | "mixed",
      "acquisition_application": "acquisition" | "application" | "mixed"
    },
    "decomposition": [  // present only when quadrant == "multi"
      {"quadrant": "...", "content_scope": "...", "sequence": int}
    ]
  }
  ```
  Confidence threshold: if `confidence < 0.70`, the classifier MUST use `escalate_to_user` fallback and request user confirmation before returning a classification.
  User override: the caller may reject the classification and re-invoke with an explicit quadrant hint (`"hint_quadrant": "howto"`). The classifier must honor explicit hints.
- **Confidence Derivation**: The classifier uses Claude's structured output (JSON mode / `tool_use` with typed schema) to generate the classification result as a valid JSON object. The `confidence` field is computed from the classifier's axis placement certainty — it is NOT derived from LLM self-assessment (which is known to be overconfident), but from a deterministic rubric based on `axis_placement` values:
  - `confidence = 1.0`: both axes unambiguous (e.g., `"practical"` + `"acquisition"` → tutorial)
  - `confidence = 0.85`: one axis clear, the other `"mixed"` placement
  - `confidence = 0.70`: both axes `"mixed"` (borderline multi-quadrant)
  - `confidence < 0.70`: classifier cannot resolve — `escalate_to_user` fires automatically
  This derivation is mechanistically enforceable: the `axis_placement.practical_theoretical` and `axis_placement.acquisition_application` values drive the score deterministically. The 0.70 threshold will reliably fire on genuine borderline cases (both axes mixed). The `confidence` value is a structured rubric-derived certainty score, not a statistically calibrated probability.
- **Misclassification Recovery**: If the writer agent produces output that the user identifies as the wrong document type, the recommended recovery path is: (1) If the user knows the correct document type: invoke the correct writer agent directly with the original input and specify the intended type explicitly. (2) If unsure of the correct type: invoke `diataxis-classifier` with a `hint_quadrant` parameter to confirm the intended quadrant. This recovery path should be documented in the SKILL.md description.
- Model: `haiku` (fast classification task)

**`diataxis-auditor`** — Documentation Auditor (T2 Read-Write)
- Cognitive mode: `systematic` (compliance checking, completeness verification)
- Expertise: Diataxis compliance assessment, quadrant mixing detection, coverage gap analysis
- Architecture: **T2 (Read, Glob, Grep, Write, Edit)**. The auditor takes a list of file paths as input (not a directory path), enabling the caller to scope the audit precisely. This avoids recursive directory traversal and keeps input predictable. For files exceeding 500 lines, the auditor uses offset/limit parameters per CB-05 to prevent single-file context exhaustion.
- Input format: The auditor receives file paths as a markdown list in the session context, one absolute path per line, formatted as `- /path/to/file.md`. The caller constructs this list from the files they wish to audit. The auditor does not accept directory paths.
- Purpose: Audits existing documentation against Diataxis principles. Identifies quadrant mixing (the most common Diataxis anti-pattern), missing quadrants, and quality gaps. Produces a structured audit report with remediation recommendations ordered by severity.
- Model: `sonnet` (balanced analysis with structured output)

### Agent governance summary

Per H-34 dual-file architecture, each agent has a `.md` (Claude Code frontmatter + system prompt) and `.governance.yaml` (validated against `docs/schemas/agent-governance-v1.schema.json`).

| Field | diataxis-tutorial | diataxis-howto | diataxis-reference | diataxis-explanation | diataxis-classifier | diataxis-auditor |
|-------|-------------------|----------------|--------------------|--------------------|---------------------|------------------|
| `version` | 0.1.0 | 0.1.0 | 0.1.0 | 0.1.0 | 0.1.0 | 0.1.0 |
| `identity.role` | Tutorial Writer | How-to Guide Writer | Reference Writer | Explanation Writer | Documentation Classifier | Documentation Auditor |
| `identity.expertise` | Pedagogical design; learning-by-doing methodology; tutorial sequencing | Goal-oriented technical writing; problem-field navigation; procedural clarity | Technical description; API documentation; structured information architecture | Conceptual writing; design rationale; contextual analysis; architectural narrative | Diataxis quadrant analysis; documentation type identification; content routing | Diataxis compliance assessment; quadrant mixing detection; coverage gap analysis |
| `tool_tier` | T2 | T2 | T2 | T2 | T1 | T2 |
| `cognitive_mode` | systematic | convergent | systematic | divergent | convergent | systematic |
| `model` | sonnet | sonnet | sonnet | opus | haiku | sonnet |
| `forbidden_actions` (min 3) | Spawn recursive subagents (P-003); Override user decisions (P-020); Misrepresent capabilities or confidence (P-022) | same | same | same | same | same |
| `forbidden_actions` (domain) | Include explanation or "why" content in tutorial steps | Include teaching/explanation; offer alternatives without goal framing | Include procedural sequences; use marketing or subjective language | Include step-by-step instructions or imperative action sequences | Invoke writer agents directly (T1 boundary) | Audit directories — accepts file path list only |
| `constitution.principles_applied` | P-003, P-020, P-022 | P-003, P-020, P-022 | P-003, P-020, P-022 | P-003, P-020, P-022 | P-003, P-020, P-022 | P-003, P-020, P-022 |
| Task tool access | No (worker) | No (worker) | No (worker) | No (worker) | No (worker) | No (worker) |
| `guardrails.fallback_behavior` | warn_and_retry | warn_and_retry | warn_and_retry | warn_and_retry | escalate_to_user* | warn_and_retry |

\* Classifier uses `escalate_to_user` (not `warn_and_retry`) because misclassification produces an incorrect document type — a worse outcome than asking the user to clarify intent. Per ADS guardrail selection, convergent classification agents should escalate rather than retry with potentially wrong output.

All six agents are workers (invoked via Task by the caller). None include Task in their tools, per H-34(b). All `.governance.yaml` files must validate against the governance JSON Schema at CI gate.

### Routing and trigger keywords

Per `agent-routing-standards.md` enhanced trigger map format:

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| documentation, tutorial, how-to, howto, reference docs, explanation, diataxis, write docs, document this, user guide, getting started, quickstart, API docs, developer guide | adversarial, tournament, quality gate, transcript, penetration, exploit, requirements, specification, V&V | 11 | "write tutorial" OR "write docs" OR "write documentation" OR "how-to guide" OR "reference docs" OR "document the" (phrase match) | `/diataxis` |

Priority 11 is the next sequential slot — the 10 existing skills occupy priorities 1-10 with no gaps (orchestration=1, transcript=2, saucer-boy=3, saucer-boy-framework-voice=4, nasa-se=5, problem-solving=6, adversary=7, ast=8, eng-team=9, red-team=10).

#### RT-M-004 keyword collision analysis

Cross-reference of all proposed keywords against the 10 existing skill trigger map entries in `mandatory-skill-usage.md`:

| Proposed Keyword | Collision with Existing Skill? | Collision Skill | Resolution |
|---|---|---|---|
| documentation | No direct collision | — | Clean. No existing skill uses this keyword. |
| tutorial | No direct collision | — | Clean. Unique to /diataxis. |
| how-to | No direct collision | — | Clean. |
| howto | No direct collision | — | Clean. |
| reference docs | No direct collision | — | Compound form avoids ambiguity with standalone "reference". |
| explanation | No direct collision | — | Clean. |
| diataxis | No direct collision | — | Framework-specific term; zero collision risk. |
| write docs | No direct collision | — | Clean. Action verb + domain noun. |
| document this | No direct collision | — | Clean. |
| user guide | No direct collision | — | Clean. |
| getting started | No direct collision | — | Clean. |
| quickstart | No direct collision | — | Clean. |
| API docs | No direct collision | — | Clean. |
| developer guide | No direct collision | — | Clean. |

**Context collision zones** (co-occurring keywords from different skills in the same request):

| Collision Zone | Example Request | Skills Matched | Resolution |
|---|---|---|---|
| "documentation" + "requirements" | "Write documentation about the requirements" | `/diataxis` (documentation) + `/nasa-se` (requirements) | `/nasa-se` negative keyword "requirements" added to `/diataxis`. Compound trigger "write documentation" takes specificity precedence for explicit documentation requests. |
| "documentation" + "design" | "Document the design decisions" | `/diataxis` (documentation) + `/nasa-se` (design) | Compound trigger "document the" matches `/diataxis` with specificity override. If no compound match, priority ordering resolves: `/nasa-se` (5) wins over `/diataxis` (11) — correct for "review the design" but incorrect for "document the design". The compound triggers handle the documentation-intent cases. |
| "documentation" + "architecture" | "Create architecture documentation" | `/diataxis` (documentation) + `/nasa-se` (architecture) | Same resolution as design: compound triggers capture documentation-intent; priority ordering handles ambiguous cases correctly. |
| "docs" (standalone) | "Check the docs for errors" | `/diataxis` (docs) | Removed "docs" as standalone keyword — too broad, triggers on "check docs" which is not a documentation-writing request. Retained only in compound forms: "write docs", "reference docs", "API docs". |

**Changes from analysis:**
1. Removed standalone "docs" keyword — retained only in compound triggers ("write docs", "reference docs", "API docs") to reduce false positives from "check the docs" type requests
2. Added "requirements", "specification", "V&V" to negative keywords — suppresses co-occurrence with /nasa-se domain terms
3. Added "write documentation" and "document the" as compound triggers — provides specificity override when documentation intent is explicit alongside /nasa-se keywords

### Integration points

- **`/problem-solving`**: Research phase may produce findings that need documentation — `/diataxis` classifier determines which quadrant the output belongs in
- **`/nasa-se`**: Requirements and design artifacts can feed into reference documentation; collision zones documented in [routing analysis](#rt-m-004-keyword-collision-analysis)
- **`/adversary`**: Diataxis agents integrate with the creator-critic-revision cycle (H-14) for C2+ documentation deliverables
- **`/eng-team`**: Security documentation benefits from Diataxis quadrant separation — security how-to guides vs. security architecture explanation vs. security API reference
- **Jerry's own docs**: The skill can be used reflexively to improve Jerry's own documentation (`.context/rules/`, `skills/*/SKILL.md`, `docs/knowledge/`)
- **Documentation Quality Gate**: When the creator-critic-revision cycle (H-14) is triggered for documentation deliverables produced by `/diataxis` writer agents, the `diataxis-auditor` SHOULD be invoked as part of the quality check. Recommended workflow: (1) writer agent produces document, (2) auditor reviews for quadrant mixing and quality criteria compliance, (3) S-014 scoring applied to final output. This integrates Diataxis-specific quality dimensions into the standard Jerry quality gate.

### Diataxis standards rule file

The rule file `skills/diataxis/rules/diataxis-standards.md` must contain the following sections before Phase 2 agent implementation begins:

**1. Per-quadrant quality criteria** (5-10 required criteria per quadrant):

| Quadrant | Required Quality Criteria |
|----------|----------------|
| Tutorial | Completable end-to-end; every step has visible result; no unexplained steps; no alternatives offered; concrete not abstract |
| How-to | Goal stated in title; action-only content; addresses real-world variations; no teaching/explaining; achieves flow |
| Reference | Mirrors code structure; wholly authoritative; no ambiguity; neutral tone; standard formatting; examples illustrate not instruct |
| Explanation | Discursive (not procedural); makes connections; provides context; acknowledges perspective; enriches understanding |

**2. Per-quadrant anti-patterns** (3-5 per quadrant):

| Quadrant | Anti-patterns |
|----------|--------------|
| Tutorial | Abstraction, extended explanation, offering choices, information overload, untested steps |
| How-to | Conflating with tutorial, tool-focused guidance, unnecessary procedures, completeness over focus |
| Reference | Marketing claims, instructions/recipes, narrative explanation, stylistic flourishes |
| Explanation | Instructional content creeping in, scattering across sections, treating as less important |

**3. Detection heuristics for quadrant mixing** (signal -> detection -> action):

| Signal | Detection Method | Agent Action | Severity |
|--------|-----------------|-------------|----------|
| Imperative verbs ("do this") in explanation documents | 2+ imperative verb sequences in a paragraph within explanation output | Flag with `[QUADRANT-MIX: procedural content in explanation]`; note in output: "Section X contains procedural content that may belong in a how-to guide" | Minor (1-2 instances), Major (3+ — recommend decomposition) |
| "Why" digressions in tutorial steps | Explanatory paragraph (3+ sentences without action verbs) between tutorial steps | Flag with `[QUADRANT-MIX: explanation in tutorial]`; move content to "Further reading" appendix or remove | Minor (1 instance), Major (2+ — tutorial reliability at risk) |
| Choice/alternative offerings in tutorials | "Alternatively" or "you could also" or "Option A/B" constructions in tutorial | Flag with `[QUADRANT-MIX: how-to content in tutorial]`; select one path, remove alternatives | Major (any instance — tutorials must have exactly one path) |
| Procedural sequences in reference entries | Numbered step lists (3+ steps) within reference documentation entries | Flag with `[QUADRANT-MIX: procedural content in reference]`; convert to descriptive prose or link to how-to guide | Minor (1 instance), Major (2+ sequences) |
| Marketing language in reference | Superlatives ("best", "fastest"), comparative claims, or promotional tone in reference | Flag with `[ANTI-PATTERN: marketing in reference]`; rewrite to neutral descriptive tone | Major (any instance — reference must be neutral) |

**Required writer agent behavior (single SSOT):** All writer agents (`diataxis-tutorial`, `diataxis-howto`, `diataxis-reference`, `diataxis-explanation`) implementing these detection heuristics MUST apply them to their own output as part of H-15 self-review, supplemented with Diataxis-specific criteria. When a mixing signal is detected in the agent's own output: (a) flag it with the appropriate `[QUADRANT-MIX: ...]` tag, (b) describe the flagged content to the user, (c) ask whether to remove/revise the flagged section or keep it with an `[ACKNOWLEDGED]` marker. This ensures all four writer agents apply uniform anti-pattern enforcement without duplicating the heuristic specifications across four agent definition files.

**4. Classification decision guide** (including borderline cases):
- Document cannot be classified into any quadrant -> escalate to user per H-31
- Document contains content from 3+ quadrants -> recommend decomposition into separate documents
- Classification confidence below 70% -> present classification with confidence score, ask user to confirm
- Section 4 must include at minimum 5 worked examples of borderline classification cases:
  - (a) A detailed how-to guide that explains the rationale for each step (how-to vs. explanation)
  - (b) A tutorial that covers conceptual background before the first step (tutorial vs. explanation)
  - (c) A reference entry that includes a brief usage example (reference vs. how-to)
  - (d) A document requested as "explain how X works" (explanation vs. how-to)
  - (e) A SKILL.md-style document combining reference and explanation (multi-quadrant — demonstrates decomposition)

**5. Jerry voice guidelines for each quadrant:**
- Per-quadrant prose style guidelines ensuring Diataxis output matches Jerry's established documentation voice
- Active voice, direct address, and concrete examples preferred across all quadrants
- Quadrant-specific tone guidance (e.g., tutorial voice is encouraging and concrete; reference voice is neutral and precise; explanation voice may be richer and more discursive)
- **Minimum content bar for Section 5:** The voice guidelines section MUST include at minimum:
  - (a) 3 concrete per-quadrant before/after voice rewrites demonstrating Jerry voice applied to Diataxis content — e.g., Tutorial: "Before: 'The user should navigate to the settings page.' After: 'Navigate to the settings page.'"; How-to: "Before: 'It is possible to configure X by modifying Y.' After: 'Configure X by modifying Y.'"; Reference: "Before: 'This command can be used to list items.' After: 'Lists items. Syntax: `command [options]`'"
  - (b) A list of Jerry-specific voice markers applicable across all quadrants (active voice; first-person commands; no passive constructions; no "it is possible to" or "one can"; concrete over abstract)
  - (c) At least 1 anti-example per quadrant showing prose that violates Jerry voice conventions (e.g., tutorial step in passive voice; reference entry with marketing language; explanation using imperative "you must")

**Maintenance:** `diataxis-standards.md` and `docs/knowledge/diataxis-framework.md` should be reviewed for continued accuracy at each Jerry major version release, or whenever significant changes to the Diataxis framework guidance are published at diataxis.fr.

### SKILL.md description draft

Per H-26 (WHAT+WHEN+triggers, <=1024 chars, no XML tags), the proposed SKILL.md description:

> **`/diataxis`** — Four-quadrant documentation framework. Produces tutorials (learning by doing), how-to guides (goal-oriented tasks), reference documentation (authoritative description), and explanation (conceptual understanding) using the Diataxis methodology. Invoke when: creating new documentation for any project or skill, auditing existing docs for quadrant mixing, or classifying whether a documentation request should be a tutorial, guide, reference, or explanation. Triggers: documentation, tutorial, how-to, howto, reference docs, explanation, diataxis, write docs, user guide, getting started, quickstart, API docs, developer guide.

This draft demonstrates H-26 compliance: WHAT (four-quadrant Diataxis methodology), WHEN (creating/auditing/classifying documentation), triggers (14 keywords listed). Length: ~430 characters — within the 1024-char limit.

### What this enables

1. **Any project, any domain**: The skill is general-purpose. It works for Jerry's own docs, for user projects consuming Jerry as a plugin, for any documentation effort where Diataxis applies.
2. **Quadrant routing**: Users say "write a tutorial for X" or "document the API for Y" and get the right type of document with the right voice, structure, and quality criteria — automatically.
3. **Audit existing docs**: Point the auditor at a file list and get a report on which docs are mixing quadrants, which quadrants are missing, and what to fix.
4. **Template-driven consistency**: Each quadrant has a template encoding structure, voice guidelines, and Diataxis-specific quality markers.
5. **Integration with quality gate**: Documentation deliverables go through the same creator-critic-revision cycle as any other C2+ Jerry deliverable, with Diataxis-specific quality dimensions added to the scoring rubric.

**Note:** The `/diataxis` skill produces single-quadrant documents or explicit multi-quadrant decompositions. Hybrid documents that blend quadrants by convention (e.g., SKILL.md combining reference and how-to sections) are outside scope — the skill produces clean single-quadrant artifacts and recommends how to decompose hybrids when asked. The skill dogfoods by improving single-quadrant docs within Jerry's documentation ecosystem.

Different terrain, different technique. But always the same mountain — making something understandable. The Diataxis skill gives Jerry four ways to ride that mountain instead of one.

### Implementation plan

**Phase 1: Foundation**
- Create project directory `projects/PROJ-NNN-diataxis-skill/` with standard worktracker structure
- Research Diataxis framework in depth (already partially done in this issue) — produce a knowledge document at `docs/knowledge/diataxis-framework.md` with required sections: (1) Diataxis framework overview with the four-quadrant grid, (2) Per-quadrant deep dive with canonical examples from diataxis.fr, (3) Common anti-patterns with examples, (4) Classification decision guide for ambiguous requests (with at least 5 worked borderline case examples)
- Design skill architecture: SKILL.md, agent definitions, routing integration
- Register skill in CLAUDE.md and AGENTS.md per H-26
- Create `skills/diataxis/rules/diataxis-standards.md` with all five required sections (quality criteria, anti-patterns, detection heuristics, classification decision guide, Jerry voice guidelines) — this is a Phase 1 deliverable because Phase 2 agents depend on it

**Phase 2: Core agents (schema validation gate)**
- Implement the four writer agents (`diataxis-tutorial`, `diataxis-howto`, `diataxis-reference`, `diataxis-explanation`) with `.md` + `.governance.yaml` dual-file architecture per H-34
- Implement `diataxis-classifier` for quadrant routing (T1, returns classification — does not invoke agents)
- Create templates for each quadrant in `skills/diataxis/templates/`
- **Phase 2 gate:** Validate each of the 5 Phase 2 agent `.governance.yaml` files (tutorial, howto, reference, explanation, classifier) against `docs/schemas/agent-governance-v1.schema.json` before proceeding to Phase 3. All 5 must pass schema validation with zero errors (zero errors = zero JSON Schema Draft 2020-12 validation errors as reported by `jerry ast validate --schema agent-governance`). *Implementation note: verify the exact CLI flag syntax (`--schema agent-governance`) against `jerry ast --help` before Phase 2 gate execution, as the CLI interface may evolve between proposal approval and implementation.*

**Phase 3: Auditor and integration**
- Implement `diataxis-auditor` agent (T2) for existing documentation assessment
- Integrate with `mandatory-skill-usage.md` trigger map (priority 11, between `/red-team` at 10 and future skills)
- Integration testing: verify routing, quadrant classification accuracy, template application
- Document the skill's own usage using the skill itself (dogfooding)

**Phase 4: Quality and validation**
- Run adversarial quality review on all agent definitions using the C2 required strategy set: S-003 (Steelman Technique, per H-16 — must precede Devil's Advocate), S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge), per quality-enforcement.md
- Test creator-critic-revision cycle with documentation deliverables
- Produce sample documentation across all four quadrants as validation artifacts
- Run classifier accuracy test suite (50 requests, >=90% overall accuracy; >=80% borderline case accuracy reported separately)

### Acceptance criteria

- [ ] `/diataxis` skill registered in CLAUDE.md and AGENTS.md per H-26
- [ ] SKILL.md created with WHAT+WHEN+triggers description per H-26 (consolidated H-28)
- [ ] Four writer agents (`diataxis-tutorial`, `diataxis-howto`, `diataxis-reference`, `diataxis-explanation`) implemented with `.md` + `.governance.yaml` per H-34
- [ ] `diataxis-classifier` agent implemented as T1 read-only classifier for quadrant routing
- [ ] `diataxis-auditor` agent implemented as T2 for documentation assessment with file path list input
- [ ] All agents include constitutional compliance triplet (P-003, P-020, P-022) in `.governance.yaml` `constitution.principles_applied` per H-34(b)
- [ ] No worker agent includes `Task` in tools per H-34(b)
- [ ] Five Phase 2 agent `.governance.yaml` files (tutorial, howto, reference, explanation, classifier) validate at Phase 2 gate; `diataxis-auditor.governance.yaml` validates at Phase 3 completion (zero validation errors each)
- [ ] Per-quadrant quality criteria documented in `skills/diataxis/rules/diataxis-standards.md` with all five sections (quality criteria, anti-patterns, detection heuristics, classification decision guide with 5+ borderline examples, Jerry voice guidelines); Section 5 must include at minimum 3 per-quadrant before/after voice rewrites, a list of Jerry-specific voice markers, and 1 anti-example per quadrant
- [ ] Templates created for all four quadrants
- [ ] Trigger map entry added to `mandatory-skill-usage.md` with negative keywords, priority, and compound triggers per RT-M-004 collision analysis
- [ ] `docs/knowledge/diataxis-framework.md` knowledge document produced with all four required sections (framework overview, per-quadrant deep dive, common anti-patterns, classification decision guide with 5+ borderline case examples)
- [ ] At least one sample document produced per quadrant as validation artifact
- [ ] At least 2 existing Jerry documentation files have been improved by invoking `/diataxis` skill agents (not manually rewritten), with: (a) agent invocation logs or session records as evidence, (b) the original and improved file versions committed to the repository for before/after comparison
- [ ] Skill routing tested: "write a tutorial for X" routes to tutorial agent, "document the API" routes to reference agent, etc.
- [ ] `diataxis-classifier` accuracy >= 90% on a 50-request test suite constructed using the following methodology: (a) requests drafted by someone other than the implementer, (b) at least 10 borderline/adversarial cases (requests that span quadrant boundaries or could plausibly be misclassified — e.g., "Explain how to set up Redis" spanning explanation and how-to), (c) test suite peer-reviewed and cases documented with expected classification rationale before running; includes 4 unambiguous requests per quadrant (16), 10+ borderline cases, 4 ambiguous multi-quadrant requests, 4 non-documentation requests that should NOT route to `/diataxis`. Borderline case accuracy >= 80% reported separately. **Solo developer fallback**: If no peer reviewer is available, the test suite author must: (i) document their selection rationale for each of the 10+ borderline cases in writing, (ii) include at least 5 of the 5 worked examples from Section 4 of the classification decision guide as test cases (ensuring baseline coverage), (iii) post the test suite in the GitHub issue or PR for community review before Phase 4 sign-off.
- [ ] Audit capability tested against existing Jerry documentation with file path list input
- [ ] New project `PROJ-NNN-diataxis-skill` created with worktracker structure

### Why this matters

Jerry is preparing for open-source release. The framework has 12 skills, 60+ agents, hundreds of rule files, and a governance framework that would make NASA nod approvingly. What it doesn't have is a systematic way to explain any of that to someone who just installed the plugin and wants to know what to do next.

The Diataxis framework is the industry standard for solving this. It's lightweight, proven, and maps perfectly onto Jerry's agent architecture. Building it as a skill means every project that uses Jerry gets documentation methodology for free — not just Jerry itself.

You can have the sickest line on the mountain, but if nobody can find the trailhead, you're just skiing alone. Diataxis is the trailhead map.
