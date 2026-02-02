
# Domain-Specific Problem-Solving Playbooks (Evidence-Based)
*(Designed for Principal & Distinguished practitioners; still teachable to ELI5)*

> **How to use these playbooks**
> 1) **Frame** with 5W1H (Who/What/Where/When/Why/How)
> 2) **Classify** the situation (Simple / Complicated / Complex / Chaotic) using the misuse tree in this pack
> 3) Apply the domain playbook as a **specialized overlay**
> 4) Close the loop: **verify + learn + institutionalize**

These playbooks are grounded in widely adopted prior art:
- **NASA systems engineering lifecycle thinking and disciplined technical processes** (NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev 2) [NASA PDF]
- **SRE/operations incident response and blameless postmortems** (Google SRE Book & Workbook; Incident Management Guide) [Google SRE]
- **Security incident handling guidance** (NIST SP 800-61r2 archived but still widely referenced; also CSRC landing page notes withdrawal/supersession) [NIST CSRC]
- **Scientific inquiry principles** (National Academies; NIH/NCBI) [National Academies, NIH]
- **Skill acquisition research** (Ericsson deliberate practice; Dreyfus model; Fitts & Posner stages) [Ericsson; Dreyfus; APA/other academic]
- **Food safety and cooking controls** (USDA FSIS safe temps; FDA Food Code & HACCP guidelines; Codex General Principles of Food Hygiene) [USDA; FDA; Codex/FAO]

References are at the end with links.

---

## A. Software Engineering Playbook (Delivery + Reliability)
### Intended use
- Debugging, incidents, performance regressions, architecture decisions, migrations, operational readiness.

### Core evidence-based prior art
- **Incident management & learning**: structured response, clear roles, and post-incident learning loops (Google SRE).
  - Google describes incidents as inevitable in complex systems and emphasizes defined incident processes plus learning via postmortems.
  - Postmortems: written record of incident, impact, actions, root cause(s), follow-ups; blameless culture improves learning.
  Sources: Google SRE Incident Management Guide (PDF) + SRE Book/Workbook postmortem chapters.

### Software-specific loop (ASCII)
```
Signal/Alert/User report
        |
        v
1) TRIAGE (stabilize users)  ---> 2) DIAGNOSE (find cause) ---> 3) FIX (mitigate/remediate)
        |                                |                           |
        v                                v                           v
   Rollback?                        Hypothesis tests            Deploy change
   Rate limit?                      (logs/metrics/traces)       Validate SLOs
   Feature flag?                    Narrow scope                Write postmortem
        |                                |                           |
        └-------------------------------> VERIFY ----------------------┘
                                        (did we stop impact?)
                                              |
                                              v
                                           LEARN
                                   (postmortem, runbooks,
                                    automation, tests)
```

### Minimal roles and artifacts (SRE-aligned)
- **Incident Commander**: keeps timeline, makes decisions, reduces thrash.
- **Operations / Comms**: manages stakeholders + status updates.
- **Subject Matter Experts**: one or more deep debuggers; avoid too many cooks.

Artifacts:
- Live incident doc (timeline, hypotheses, actions)
- Runbooks/playbooks
- Postmortem with action items and owners

### Decision rules
- If users are impacted: **mitigate first** (restore service) then diagnose deeper.
- Prefer changes that are **reversible** (rollback/flag) under time pressure.
- In “unknown unknowns”, use **hypothesis-driven** debugging:
  - “If X were true, we should see Y in telemetry.”

### Diagnostic techniques (choose based on classification)
- **Simple**: known fix (restart, rollback, clear queue, etc.) and document.
- **Complicated**: expert analysis (profiling, tracing, repro, load testing).
- **Complex**: reduce blast radius; probe with safe experiments; gather data.
- **Chaotic**: act to stabilize (stop the bleeding), then reclassify.

### Common software failure modes
- Solving before framing (“fix first, understand later”)
- No single incident lead (decision thrash)
- Unbounded changes during incident (making the system less knowable)
- Skipping the learning loop (no postmortem/runbook updates)

---

## B. Security Playbook (Incidents + Design Assurance)
### Intended use
- Security incidents, suspected compromise, vulnerability response, threat modeling.

### Core evidence-based prior art
- **Incident handling lifecycle**: preparation; detection & analysis; containment, eradication & recovery; post-incident activity (NIST SP 800-61r2 – archived).
- **Preventive systems thinking**: HACCP-like hazard/control thinking is analogous in spirit—identify hazards, define controls, monitor, verify, document (FDA HACCP; Codex/FAO).

### Security incident lifecycle (ASCII)
```
PREPARE
  |
  v
DETECT & ANALYZE  --->  CONTAIN  --->  ERADICATE  --->  RECOVER
  |                     |              |                 |
  v                     v              v                 v
Evidence logging      Stop spread     Remove cause      Restore service
Triage severity       Isolate hosts   Patch/rotate      Monitor for relapse
Scope boundaries      Disable creds   Reimage etc.      Lessons learned
  |
  v
POST-INCIDENT
  - root cause
  - control gaps
  - playbook updates
  - measurement
```

### Evidence integrity rules (high leverage)
- **Preserve evidence**: logs, snapshots, hashes, chain-of-custody where applicable.
- **Minimize contamination**: don’t “poke randomly” on compromised systems.
- **Time synchronization matters**: align timelines across systems.

### Decision rules
- If compromise suspected: prioritize **containment** over “perfect understanding”.
- Security decisions must explicitly reason about:
  - attacker capability
  - attack surface
  - control strength
  - detection coverage

### Design-time security (Red Team overlay)
Apply after solution selection:
- “How would an attacker abuse this?”
- “What assumption is weakest?”
- “What is the highest-impact failure mode?”

---

## C. Science Playbook (Inquiry + Model Building)
### Intended use
- Research questions, experiments, measurement design, analytics, causal reasoning.

### Core evidence-based prior art
- **Scientific knowledge accumulates through discovery, confirmation, correction** and relies on statistical inference and replication (National Academies; NIH/NCBI).
- Guiding principles include **testable/refutable hypotheses**, ruling out competing hypotheses, and the importance of replication/generalization (National Academies).

### Scientific inquiry loop (ASCII)
```
Observation / anomaly / curiosity
            |
            v
Frame (5W1H) + Define variables
            |
            v
Hypotheses (multiple competing explanations)
            |
            v
Design test
- what would falsify?
- controls? confounders?
- measurement reliability?
            |
            v
Run experiment / collect data
            |
            v
Analyze
- estimate uncertainty
- check assumptions
            |
            v
Conclude (tentative)
            |
            v
Replicate / generalize / revise model
```
### Decision rules
- Always articulate: “What evidence would change my mind?”
- Prefer multiple competing hypotheses to avoid premature convergence.
- Separate **measurement** errors from **model** errors.

### Common scientific failure modes
- P-hacking / retrofitting hypotheses
- Confounding mistaken for causality
- Single-study overconfidence (lack of replication)
- Poor measurement / instrument drift

---

## D. Skills Acquisition Playbook (Learning Anything Fast, Safely)
### Intended use
- Motor skills (skiing, dancing), cognitive skills (architecture), crafts (baking), performance under pressure.

### Core evidence-based prior art
- **Deliberate practice**: expert performance is strongly linked to structured, effortful practice with feedback and targeted improvement (Ericsson 1993; Ericsson overview PDFs).
- **Stages of skill acquisition**:
  - Fitts & Posner: cognitive → associative → autonomous.
  - Dreyfus: novice → advanced beginner → competent → proficient → expert (Stuart Dreyfus, 2004).

### Skill-building loop (ASCII)
```
Define skill + standard of performance
             |
             v
Decompose into subskills
             |
             v
Pick ONE subskill to train today
             |
             v
Deliberate practice set:
- short reps
- immediate feedback
- correction
- rest
             |
             v
Measure improvement
             |
             v
Integrate into full performance
             |
             v
Review: what changed? what stuck?
```

### Decision rules
- Train at the edge of ability (not comfort, not chaos).
- Use fast feedback (coach, video, instrumentation).
- Build “error library”: common errors + corrections.

### Common learning failure modes
- Repeating mistakes (practice without feedback)
- Too much complexity too early (skipping stages)
- Fatigue masquerading as “lack of talent”
- No measurement (no idea if improving)

---

## E. Cooking Playbook (Quality + Safety + Iteration)
### Intended use
- Reproducible cooking outcomes, high-quality results, safe food handling, debugging recipes.

### Core evidence-based prior art
- **Food safety critical limits**:
  - Safe internal temperatures (USDA FSIS; foodsafety.gov).
  - “Danger zone” and time/temperature controls (FDA Food Code resources).
- **Preventive control mindset**: HACCP principles and Codex General Principles of Food Hygiene (Codex/FAO; FDA HACCP).

### Cooking control system (ASCII)
```
Goal (taste + texture + safety)
         |
         v
5W1H frame (ingredient, method, equipment, constraints)
         |
         v
Identify critical control points (CCPs)
- temperature
- time
- contamination routes
- cooling/holding
         |
         v
Execute + measure (thermometer, scale, timer)
         |
         v
Taste/texture check + safety check
         |
         v
Adjust (one variable at a time)
         |
         v
Document (recipe as a spec)
```

### Decision rules
- If food safety is involved: **safety first** (temps, cross-contamination, cooling rules).
- When debugging a recipe: change **one variable at a time**.
- For repeatability: treat recipes like software—version them.

### Common cooking failure modes
- No measurement (eyeballing everything)
- Changing many variables simultaneously
- Ignoring thermal realities (pan temp, carryover cooking)
- Unsafe handling (time/temp abuse)

---

## References (authoritative sources)
### Systems engineering / decision contexts
- NASA Systems Engineering Handbook (NASA/SP-2016-6105 Rev 2) PDF: https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf
- NASA NTRS entry for the handbook: https://ntrs.nasa.gov/citations/20170001761
- Cynefin (ordered vs unordered contexts): Snowden & Boone, “A Leader’s Framework for Decision Making” (2007) PDF mirror: https://www.systemswisdom.com/sites/default/files/Snowdon-and-Boone-A-Leader%27s-Framework-for-Decision-Making_0.pdf

### Software reliability / operations
- Google SRE Incident Management Guide (PDF): https://sre.google/static/pdf/IncidentManagementGuide.pdf
- Google SRE Book – Postmortem culture: https://sre.google/sre-book/postmortem-culture/
- Google SRE Workbook – Postmortem culture: https://sre.google/workbook/postmortem-culture/

### Security incident response
- NIST CSRC landing page for SP 800-61r2 (notes withdrawal): https://csrc.nist.gov/pubs/sp/800/61/r2/final
- Archived PDF of NIST SP 800-61r2: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r2.pdf

### Scientific inquiry
- National Academies – Guiding principles for scientific inquiry: https://www.nationalacademies.org/read/10236/chapter/5
- National Academies – Scientific methods and knowledge: https://www.nationalacademies.org/read/25303/chapter/5
- NIH/NCBI – Scientific methods and knowledge (book chapter): https://www.ncbi.nlm.nih.gov/books/NBK547541/
- NIH/NCBI – Scientific principles & research practices: https://www.ncbi.nlm.nih.gov/books/NBK234526/

### Skill acquisition
- Ericsson (expertise overview PDF referencing 1993 deliberate practice work): https://cseweb.ucsd.edu/classes/fa08/cse599/Papers/Ericsson.pdf
- MIT-hosted “Expert Performance” PDF with Ericsson references: https://web.mit.edu/6.969/www/readings/expertise.pdf
- Dreyfus (2004) five-stage model PDF: https://www.bumc.bu.edu/facdev-medicine/files/2012/03/Dreyfus-skill-level.pdf

### Cooking safety & preventive controls
- USDA FSIS Safe Temperature Chart: https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/safe-temperature-chart
- foodsafety.gov Safe Minimum Internal Temperatures: https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures
- FDA Food Code 2022 (landing): https://www.fda.gov/food/fda-food-code/food-code-2022
- FDA HACCP Principles & Application Guidelines: https://www.fda.gov/food/hazard-analysis-critical-control-point-haccp/haccp-principles-application-guidelines
- Codex/FAO General Principles of Food Hygiene (includes HACCP system): https://openknowledge.fao.org/server/api/core/bitstreams/6866dc55-d2c0-48dd-a528-a4d634f1b0b4/content
