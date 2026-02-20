# PROJ-005: Markdown AST Infrastructure — Implementation Plan

> Investigate and implement an AST-based approach to markdown manipulation, replacing raw text operations with structured parsing, transformation, and rendering across the full Jerry surface.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Project scope and goals |
| [Problem Statement](#problem-statement) | What we're solving |
| [Hypothesis](#hypothesis) | Core thesis to validate |
| [Epics](#epics) | Work breakdown |
| [Milestones](#milestones) | Key delivery points |
| [Success Criteria](#success-criteria) | Definition of done |

---

## Overview

PROJ-005 investigates whether an AST (Abstract Syntax Tree) intermediary for markdown files would improve Claude's efficiency and reliability when manipulating Jerry's documentation surface. Today, all markdown operations — worktracker entities, skills, rules, templates, orchestration plans, ADRs — are performed through raw text find-and-replace on `.md` files. This is brittle, schema-unaware, and makes validation difficult.

**Target scope:** Full Jerry surface — worktracker entities (EPIC, FEAT, TASK, etc.), skill definitions, rules, templates, orchestration plans, ADRs, and all Claude-consumed markdown.

**Language constraint:** Python only (UV ecosystem). Must evaluate 5+ existing libraries plus the build-from-scratch option.

## Problem Statement

**Current pain:**
1. Raw text manipulation of `.md` files is error-prone — edit operations depend on exact string matching
2. No schema validation — blockquote frontmatter, navigation tables, section structure can silently break
3. Structural queries are expensive — finding "all FEAT with status pending" requires grep + parsing
4. Template instantiation is string interpolation — no node-level manipulation
5. Cross-file consistency checks require ad-hoc parsing per file type
6. Claude spends significant tokens reading/writing raw markdown that could be structured operations

**Desired state:**
1. Parse markdown into a structured AST (JSON or Python objects)
2. Manipulate via typed API — query nodes, update fields, validate schemas
3. Render back to clean, consistent markdown for human readability
4. Integrate into Jerry CLI or as Claude-accessible tooling
5. Schema enforcement at parse/render time

## Hypothesis

We hypothesize that:
1. An AST intermediary will reduce token consumption for markdown operations by enabling targeted node manipulation instead of full-file text replacement
2. Schema validation at parse time will catch structural errors that currently propagate silently
3. Existing Python markdown AST libraries can handle Jerry's markdown dialect (blockquote frontmatter, navigation tables, Mermaid diagrams, template placeholders)
4. The integration overhead is justified by efficiency gains across the full Jerry surface

## Epics

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| EPIC-001 | Markdown AST Infrastructure | pending | high |

### EPIC-001 Features

| ID | Title | Status |
|----|-------|--------|
| FEAT-001 | AST Strategy Evaluation & Library Selection | pending |

### EPIC-001 Spikes

| ID | Title | Status | Parent |
|----|-------|--------|--------|
| SPIKE-001 | Python Markdown AST Library Landscape | pending | FEAT-001 |
| SPIKE-002 | AST-First Architecture Feasibility Assessment | pending | FEAT-001 |

## Milestones

| Milestone | Target | Status |
|-----------|--------|--------|
| SPIKE-001 complete — 5+ libraries evaluated with evidence | TBD | pending |
| SPIKE-002 complete — go/no-go recommendation on AST strategy | TBD | pending |
| FEAT-001 complete — library selected or build decision made | TBD | pending |
| Architecture decision (ADR) published | TBD | pending |
| MVP integration with Jerry CLI or hidden skills | TBD | pending |

## Success Criteria

- [ ] 5+ Python markdown AST libraries evaluated with evidence (sources, benchmarks, feature matrices)
- [ ] Build-from-scratch option formally assessed against buy options
- [ ] Go/no-go decision on AST strategy with adversarial review (S-002, S-003, S-013)
- [ ] If go: library selected, integration architecture defined, migration path for skills documented
- [ ] If no-go: alternative strategy documented with rationale
- [ ] All decisions backed by evidence (citations, references, proof-of-concept results)
