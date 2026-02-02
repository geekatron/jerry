# TODO Integration Rules

> Rules for integrating Claude Code's TODO list with the worktracker system.
> These META TODO items MUST ALWAYS be on your list.

---

## Task Management Tools

Use the task management tools (e.g. `TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet`) to manage your TODO list effectively.

---

## Required META TODO Items

The following META TODO items **MUST ALWAYS BE ON YOUR LIST**. These survive context compaction and ensure behavioral consistency.

### Project & Workflow Context

- **META:** You are in project `{JerryProjectId}` | Workflow Id: `{WorkflowId}`
- **META:** Keep your TODO list in sync with the orchestration plan showing the previous phase, current phase and next phase → current phase must show all tasks/subagents

### Work Tracker Sync

- **META:** Update the respective work tracker `*.md` files
- **META:** Capture and update decisions in the respective `*.md` files with detailed updates as YOU and the user go through Questions and Answers
- **META:** Update your respective `*.md` files with detailed updates as you are working/progressing through them
- **META:** Document detailed bugs, discoveries and impediments as they arise in their respective `*.md` files
- **META:** Keep your TODO list up to date
- **META:** Keep your TODO list in sync with your respective work tracker `*.md` files
- **META:** Keep your work tracker entities up to date with detailed updates so they are truthful, accurate and honest representation of the current state
- **META:** Keep your orchestration artifacts up to date with detailed updates so they are truthful, accurate and honest representation of the current state

### Quality & Integrity

- **META:** Do NOT take shortcuts. Do NOT use hacks to solve problems. If you are about to take a shortcut or apply a hack, ask yourself is there a better way? If you are about to answer no, try again. If you are truly blocked and want to take a shortcut or apply a hack, ask the user first. We are building mission-critical software and quality is king!
- **META:** Ask questions. Push back if something doesn't make sense or is misaligned.
- **META:** Be truthful, accurate, evidence based (citations, sources, references) and honest.

### Documentation Standards

- **META:** You MUST ALWAYS document your work so that it is understandable by yourself and three different personas:
  1. **ELI5** - Explain it to me like I'm Five - Simple analogy explanations
  2. **Engineer** - Deep Technical explanation with context
  3. **Architect** - Performance implications, tradeoffs, one-way door decisions and design rationale

### Research & Analysis

- **META:** You MUST ALWAYS perform any kind of research and analysis using at minimum the following Problem-Solving frameworks: 5W2H + Ishikawa + Pareto Analysis (80/20) + Failure Mode and Effects Analysis (FMEA) + 8D (Eight Disciplines) and NASA Systems Engineering Handbook framework before starting any implementation work.
- **META:** You MUST perform research and analysis using Context7 and search the internet for industry best practices, industry standards, innovative work and prior art on the topics you are working through.
- **META:** You MUST make data + evidence driven decisions based on industry best practices and prior art from authoritative sources such as Industry Experts, Industry Innovators, Industry Leaders, Community Experts, Community Innovators, Community Leaders ensuring you provide citations, references and sources.

### Persistence & Evidence

- **META:** You MUST persist your detailed analysis, discoveries, explorations, findings, research and synthesis in the repository.
- **META:** You MUST make all decisions in an evidence based process with citations, references and sources using industry best practices from industry leaders, industry experts, community leaders and community experts.

### Visualization

- **META:** You MUST make ASCII art and mermaid diagrams to illustrate your points wherever applicable including:
  - Activity diagrams
  - State diagrams
  - Flow charts
  - Sequence diagrams
  - Class diagrams
  - Component diagrams
  - Architecture diagrams
  - System context diagrams

---

## TODO-Worktracker Sync Requirements

Your TODO list MUST reflect the worktracker hierarchy:

```
TODO List Structure:
├── Current Epic
│   ├── Previous Features (context)
│   ├── Current Feature
│   │   ├── All Enablers OR Stories
│   │   └── Current Enabler/Story
│   │       └── All Tasks
│   └── Next Feature (upcoming)
└── Next Epic (preview)
```

**Rule:** TODO List MUST survive compaction and provide high fidelity.

---

## Orchestration Sync Requirements

When working with orchestrated workflows, your TODO MUST show:

```
Orchestration TODO Structure:
├── Previous Phase (context)
├── Current Phase
│   └── All tasks/subagents in current phase
└── Next Phase (upcoming)
```

---

## Additional Actions

You MUST reflect actions you are taking in the TODO list that are NOT captured in work tracker entities. These include:

- Ad-hoc research activities
- User questions being investigated
- Clarifications being sought
- Context gathering activities
- Any work-in-progress not yet formalized as a worktracker entity

---

## Quick Reference: META TODO Categories

| Category | Purpose |
|----------|---------|
| **Project Context** | Current project and workflow identity |
| **Sync** | Keep TODO ↔ Worktracker ↔ Orchestration in sync |
| **Quality** | No shortcuts, ask questions, be truthful |
| **Documentation** | ELI5 + Engineer + Architect lens |
| **Research** | Use frameworks, Context7, industry practices |
| **Persistence** | Persist everything, evidence-based decisions |
| **Visualization** | ASCII art and Mermaid diagrams |
