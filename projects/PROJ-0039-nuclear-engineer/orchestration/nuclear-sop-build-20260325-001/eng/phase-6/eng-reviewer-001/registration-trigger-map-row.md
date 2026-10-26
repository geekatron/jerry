# Registration: Trigger Map Row for /nuclear-sop

> **Purpose:** Draft row for `mandatory-skill-usage.md` Trigger Map table.
> **Format:** 5-column per RT-M-003 (`agent-routing-standards.md`).
> **Source:** Integration analysis Section 2.1 + synthesis spec Section 1.1.
> **Apply after:** QG-E6 PASS. User splices into `.context/rules/mandatory-skill-usage.md` Trigger Map table.

## Trigger Map Row

Copy this row and add it to the Trigger Map table in `.context/rules/mandatory-skill-usage.md`:

```
| nuclear sop, nuclear procedure, STAR self-check, pre-job brief, post-job brief, hold point, place-keeping, step sign-off, procedure compliance, continuous use, procedure use classification, operating experience capture, OE entry, nuclear rigor, nuclear discipline, sop brief, sop execute, sop capture, sop verify, nuclear workflow | adversarial, tournament, quality gate, transcript, VTT, SRT, penetration, exploit, code review, multi-phase, pipeline coordination, research, investigate, root cause, threat model, STRIDE, secure design | 12 | "nuclear procedure" OR "pre-job brief" OR "post-job brief" OR "STAR self-check" OR "hold point" OR "step sign-off" OR "place-keeping" OR "procedure compliance" (phrase match) | `/nuclear-sop` |
```

## Corresponding H-22 Rule Update

Add to the H-22 rule text in `mandatory-skill-usage.md` HARD Rules table:

```
MUST invoke `/nuclear-sop` for nuclear-inspired procedural execution requiring pre-job briefing, STAR self-checking, hold points, place-keeping, and OE capture.
```

## Collision Analysis Summary

> **CORRECTED / SUPERSEDED (2026-08-07, PROJ-032 remediation register REM-09):** The claim below that a
> `"nuclear workflow"` compound trigger resolved the `/orchestration` collision was incorrect — no such
> compound trigger existed in the drafted row above or in the applied row, so the documented activation
> keyword "nuclear workflow" deterministically resolved to `/orchestration` (priority 1 vs. 16) under
> routing Step 3. The live row in `.context/rules/mandatory-skill-usage.md` has since been extended with
> `"nuclear workflow" OR "nuclear sop" (phrase match)` compound triggers; routing Step 2
> (compound-trigger specificity overrides numeric priority) now resolves these phrases to `/nuclear-sop`.
> The live trigger map row is the SSOT; this document is superseded by it.

- **Zero unresolved collisions** across all 20 proposed keywords (verified against all existing trigger map entries)
- **Three partial collisions resolved** by existing mechanisms:
  - "compliance" (standalone) -> `/nasa-se` via priority (5 vs. 12); "procedure compliance" -> `/nuclear-sop` via compound trigger
  - "workflow" (standalone) -> `/orchestration` via priority (1 vs. 12); "nuclear workflow" -> `/nuclear-sop` via compound trigger *(INCORRECT as drafted — see correction note above)*
  - "quality gate" -> in nuclear-sop's NEGATIVE keyword list; yields to `/adversary`
- **Standalone "sop" excluded** as positive keyword per integration analysis recommendation (enterprise acronym false-match risk)

## Optional: /orchestration Negative Keyword Update

Consider adding "nuclear" and "sop" as negative keywords to the `/orchestration` trigger map row to prevent false matches when nuclear-sop-specific requests include "workflow" or "procedure":

```
Current /orchestration negative keywords: adversarial, transcript, root cause, debug
Proposed addition: nuclear, sop
```

This is RECOMMENDED (RT-M-004) but not required -- the priority ordering (orchestration=1, nuclear-sop=12) already resolves the collision.
