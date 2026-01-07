
# Framework Misuse Decision Tree (Stop Using the Wrong Tool)

This is a **guardrail**. Its job is to prevent the most expensive class of mistakes:
> **Using the right framework in the wrong context.**

It’s heavily inspired by context-based decision making (Cynefin) and by the practical necessity of stabilizing chaotic systems before analysis.  
See Snowden & Boone (2007).

---

## Misuse tree (ASCII)

```
START
  |
  v
Is there immediate danger / active damage / safety or security breach?
  |
  +-- YES --> CHAOTIC MODE
  |          - Act to stabilize first
  |          - Reduce blast radius
  |          - Establish control & observability
  |          - THEN reclassify (Simple/Complicated/Complex)
  |
  +-- NO ---> Do we have a known playbook with high success rate?
             |
             +-- YES --> SIMPLE MODE
             |          - Follow best practice
             |          - Avoid “creative overengineering”
             |          - Document & improve runbook
             |
             +-- NO ---> Can experts analyze cause-effect reliably?
                        |
                        +-- YES --> COMPLICATED MODE
                        |          - Use expert analysis
                        |          - Root cause tools (5 Whys, Fishbone)
                        |          - Validate with tests/data
                        |
                        +-- NO ---> COMPLEX MODE
                                   - Probe with safe-to-fail experiments
                                   - Observe emergent behavior
                                   - Prefer reversible moves
                                   - Learn and iterate
```

---

## Common misuse patterns (and what to do instead)

### 1) Root cause analysis during chaos
**Symptom:** “Let’s do 5 Whys right now” while users are burning.  
**Fix:** Stabilize first; then do analysis/postmortem.  
(Aligns with incident handling lifecycles and SRE practice.)

### 2) “Best practices” in complex adaptive systems
**Symptom:** Copying a template architecture without local probes.  
**Fix:** Run small experiments; measure; iterate.  
(Complex domain requires probe–sense–respond.)

### 3) Improvisation as a permanent solution
**Symptom:** Heroics, tribal knowledge, no documentation.  
**Fix:** Convert improvisation into engineering: runbooks, automation, controls.

### 4) Brainstorming + judgment at the same time
**Symptom:** Idea generation collapses and everyone converges early.  
**Fix:** Separate diverge from converge (two-phase thinking).

---

## References
- Snowden & Boone, “A Leader’s Framework for Decision Making” (2007) PDF: https://www.systemswisdom.com/sites/default/files/Snowdon-and-Boone-A-Leader%27s-Framework-for-Decision-Making_0.pdf
