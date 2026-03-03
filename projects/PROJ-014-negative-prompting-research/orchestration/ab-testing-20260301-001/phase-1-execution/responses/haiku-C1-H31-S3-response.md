# H-31 Ambiguity Resolution: Gap Analysis Update

## Executive Summary

**Task:** Update projects/PROJ-011/analysis/gap-analysis.md with three new gaps from stakeholder interviews

**Constraint Applied:** H-31 (Clarify before acting when requirements are ambiguous)

**Decision:** PAUSE for clarification before editing

---

## Analysis

### What Makes This Ambiguous?

The request contains a critical missing piece: **the user has not provided the actual details of the three new gaps.**

The ambiguity has two dimensions:

#### 1. **Which gaps specifically?** (Information gap)
- The message states "The interviews surfaced three additional gaps" but does not specify:
  - Gap titles/names
  - Gap descriptions
  - Impact area
  - Stakeholders affected
  - Severity/priority
  - Recommended mitigation
  - Any other metadata matching the existing 14 gaps' format

#### 2. **What action should I take?** (Action ambiguity)
Possible interpretations:
- **(a)** Wait for the user to provide gap details, then edit the file
- **(b)** Create placeholder entries with TBD fields for the user to fill in
- **(c)** Request the gap details from the user before proceeding
- **(d)** Access the stakeholder interview transcript to extract gaps myself (unlikely; not provided)

### Why This Requires Clarification

Per **H-31** in quality-enforcement.md:

> "Clarify before acting when requirements are ambiguous. MUST ask when: (1) multiple valid interpretations exist, (2) scope is unclear, (3) destructive or irreversible action implied. MUST NOT ask when requirements are clear or answer is discoverable from codebase."

This request exhibits condition (1): multiple valid interpretations of both the data and the action.

**Cost-benefit assessment:**
- **Cost of clarifying:** ~30 seconds (one targeted question)
- **Cost of guessing:** High -- wrong-direction work consuming 10-30 minutes of editing, creating placeholder entries the user must revise, or worse, committing incomplete data to the analysis document

Per H-31 logic: "One clarifying question costs seconds; wrong-direction work costs hours." This is a **MUST clarify** situation.

---

## The Clarifying Question

I will ask the user:

> **Before I update the gap analysis document, I need the details of the three new gaps. Please provide:**
>
> **Either Option A:** Provide the three gaps in structured format (matching the existing document format -- typically: gap title, description, impact area, severity, stakeholder feedback excerpt)
>
> **Or Option B:** If you'd prefer I extract them, please share the stakeholder interview transcript, notes, or recording reference, and I'll extract and synthesize the three gaps into the document format.
>
> **Which would you prefer?**

---

## Behavioral Justification

### H-31 Compliance

**Rule:** "MUST ask clarifying questions before proceeding when requirements have multiple valid interpretations."

**This situation meets the rule trigger because:**
1. ✓ Multiple valid interpretations exist (options a, b, c above)
2. ✓ Scope is unclear (which gaps? what format? from which source?)
3. ✓ Action is unclear (edit, wait, create placeholders, extract)

**The rule explicitly mandates H-31 applies** -- not a judgment call.

### Why NOT to Proceed Without Clarification

**Anti-pattern AP-06 (Under-Routing)** would apply if I silently made a guess:
- User expects action X (provide gaps), but I perform action Y (create placeholders)
- Downstream work stalls waiting for user input I should have requested upfront
- Multiple back-and-forth turns required to correct the direction

**Cost multiplier:** Fixing wrong-direction work typically costs 10-30x the cost of upfront clarification.

### Principle-Based Reasoning

**P-020 (User Authority):** I must respect the user's intent. The user's intent is to update the document with specific gaps. I cannot fulfill that intent without knowing what those gaps are. Proceeding without them violates P-020.

**P-022 (No Deception):** Claiming I can update with "three gaps" when I don't have them would be deceptive. The honest action is to ask for the missing information.

---

## Next Steps (If Clarified)

Once the user provides the three gaps via Option A or Option B:

1. **Validate format consistency** with existing 14 gaps in the document
2. **Insert gaps** into the appropriate section (alphabetical, by severity, by area, etc. -- document structure determines placement)
3. **Update count** if the document maintains a summary count ("14 gaps → 17 gaps")
4. **Verify structure** against any navigation tables or indexes (H-23 markdown navigation standard)
5. **Present the updated section** to the user for approval before final commit

---

## Constraint Compliance Summary

| Constraint | Status | Evidence |
|-----------|--------|----------|
| **H-31: Clarify when ambiguous** | ✓ APPLIED | Ambiguity detected; clarifying question prepared |
| **H-22: Proactive skill invocation** | Not triggered | This is a single-agent C1 task; no skill routing needed |
| **H-02: User authority** | ✓ RESPECTED | Asking user to provide the decision-enabling information |
| **P-022: No deception** | ✓ HONORED | Transparently stating that gap details are missing |

---

## Conclusion

**Action: PAUSE and ask the clarifying question above.**

The three new gaps are missing from the user's request. Proceeding to edit the document would constitute wrong-direction work. H-31 mandates clarification before action in exactly this scenario -- ambiguity + missing data.

The one-sentence clarifying question above enables the user to provide the information needed, keeping the task on track and avoiding costly back-and-forth cycles.
