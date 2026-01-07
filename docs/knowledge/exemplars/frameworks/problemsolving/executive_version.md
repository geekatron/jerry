
# Executive Version (Leadership-Safe)
*(Outcome-oriented, low jargon, high leverage)*

## Why this matters
Organizations lose time and reliability not because teams can’t “think”, but because they:
- Solve the wrong problem
- Use the wrong method for the situation
- Fail to retain learning

This document provides a **repeatable problem-solving operating system** that works across:
software, security, science, operations, product, and even non-technical disciplines.

---

## The One-Slide Model (the operating system)

1) **Frame** the problem (Who/What/Where/When/Why/How)  
2) **Classify** the situation: Simple / Complicated / Complex / Chaotic  
3) **Diagnose** with the right tool (root cause vs hypothesis)  
4) **Generate options** (diverge)  
5) **Decide** with explicit tradeoffs (converge)  
6) **Act** with reversibility when uncertain  
7) **Verify & learn** (institutionalize improvements)

This structure matches best practices across systems engineering, SRE operations, security incident handling, and scientific inquiry.  
(Examples: NASA systems engineering guidance; Google SRE incident management & postmortems; NIST incident response lifecycle; National Academies on scientific inquiry.)

---

## What leaders should demand (behavioral contracts)

### A) Before action: a 60-second framing
Every team must be able to answer:
- What is happening?
- Who is affected?
- What is the impact?
- What are we trying to accomplish?
- What evidence do we have? What are we missing?

### B) Correct mode selection
- **Chaotic**: stabilize first (stop harm), then analyze.
- **Simple**: follow known playbooks; document improvements.
- **Complicated**: expert analysis + tests; make reasoning explicit.
- **Complex**: experiment safely; prefer reversible moves.

### C) Written learning loop
For any material failure or incident, require:
- A written record (what happened, impact, timeline)
- Root cause(s) or best current explanation
- Clear follow-up actions with owners and due dates
- Updates to runbooks, tests, monitoring, controls

This aligns with industry incident learning practices (e.g., postmortems in SRE).

---

## Operating metrics leaders can track (simple, robust)

### 1) Time-to-stabilize (TTS)
How quickly did we stop customer harm?

### 2) Recurrence rate
Are similar incidents returning? If yes, learning loop isn’t working.

### 3) Action item closure rate
% of corrective actions completed on time.

### 4) “Known unknowns” shrink rate
Are teams reducing uncertainty over time (better monitoring, better documentation)?

---

## What to avoid (leadership anti-patterns)

- Rewarding heroics over systems improvement
- Demanding certainty in complex situations (leads to fake confidence)
- Treating postmortems as blame exercises (destroys learning)
- “Standardizing” solutions before measuring local reality

---

## References (selected)
- NASA Systems Engineering Handbook (NASA/SP-2016-6105 Rev 2): https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf  
- Google SRE Incident Management Guide (PDF): https://sre.google/static/pdf/IncidentManagementGuide.pdf  
- Google SRE Book – Postmortem culture: https://sre.google/sre-book/postmortem-culture/  
- NIST SP 800-61r2 landing page (notes withdrawal; archived): https://csrc.nist.gov/pubs/sp/800/61/r2/final  
- National Academies – Guiding principles for scientific inquiry: https://www.nationalacademies.org/read/10236/chapter/5  
