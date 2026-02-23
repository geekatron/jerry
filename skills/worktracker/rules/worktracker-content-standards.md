# Worktracker Content Quality Standards

> Reference file for content quality in work items.
> Auto-loaded via SKILL.md `@` import. Referenced when creating or auditing work items.
> Source: PROJ-005-jerry-process-improvements (synthesis of ADO skill patterns + industry research)
> Created: 2026-02-17

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [The #1 Rule](#the-1-rule) | The single most important content quality principle |
| [Acceptance Criteria Standards](#acceptance-criteria-standards) | Format, limits, and writing rules for AC |
| [AC Bullet Count Limits](#ac-bullet-count-limits) | Hard limits by work item type |
| [AC Anti-Patterns](#ac-anti-patterns) | What AC must NOT contain |
| [Concrete vs Vague Examples](#concrete-vs-vague-examples) | Paired examples showing good and bad AC |
| [AC vs Definition of Done](#ac-vs-definition-of-done) | Separation guidance with universal test |
| [Where Implementation Details Belong](#where-implementation-details-belong) | Correct placement for technical details |
| [Writing Style](#writing-style) | Hemingway directive for concise content |
| [Pre-Finalization Quality Check](#pre-finalization-quality-check) | 4-question checklist before creating work items |
| [Scope Overflow and Splitting](#scope-overflow-and-splitting) | SPIDR framework for splitting oversized items |
| [Cross-References](#cross-references) | Links to related rule files |

---

## The #1 Rule

> **If engineers, UX designers, or QA need to ask clarifying questions, the Acceptance Criteria has failed.**

Every AC bullet must be specific enough that an engineer can build from it, a QA engineer can write test cases from it, and a UX designer can validate it -- without asking the author a single question.

If you find yourself writing AC that requires context not present in the work item, the AC is incomplete.

---

## Acceptance Criteria Standards

### Format Rules

| Rule | Requirement |
|------|-------------|
| Structure | Bullet points only. One sentence per criterion. |
| Voice | Start with an actor or system subject: "User can...", "System validates...", "API returns...", "Admin sees..." |
| Focus | Describe **outcomes observable** by users, testers, or systems |
| Precision | No ambiguous terms. Every criterion must be testable and verifiable |
| Brevity | Respect bullet count limits (see table below). If you need more, split the item |

### What AC Describes

- Observable behavior from the user's or system's perspective
- Specific validation rules with expected error messages
- Concrete data displayed or returned
- State changes visible to the actor

### What AC Does NOT Describe

- How to implement the feature (file paths, class names, method signatures)
- Process requirements that apply to all work items (code review, test coverage)
- Architecture or technology decisions
- Deployment or infrastructure concerns

---

## AC Bullet Count Limits

| Work Item Type | Max AC Bullets | If You Need More |
|----------------|---------------|------------------|
| Story (PBI) | 5 | Split the story using SPIDR |
| Bug | 5 | Split into separate bugs by symptom |
| Task | 5 | Break into subtasks |
| Enabler | 5 | Decompose into child tasks |
| Feature | 5 | Decompose into stories/enablers |

**Hard rule:** Exceeding these limits signals the scope is too large. See [Scope Overflow and Splitting](#scope-overflow-and-splitting).

---

## AC Anti-Patterns

| Anti-Pattern | Why It Fails | Rule Violated | Belongs In |
|-------------|-------------|---------------|------------|
| "All tests pass" | DoD item -- applies to every work item equally | WTI-008a | Definition of Done |
| "Code reviewed and approved" | DoD item -- applies to every work item equally | WTI-008a | Definition of Done |
| "Documentation updated" | DoD item -- applies to every work item equally | WTI-008a | Definition of Done |
| "Deployed to staging" | DoD item -- deployment is process, not feature | WTI-008a | Definition of Done |
| "Update AssetTypeRepository.cs" | Implementation detail -- specifies how, not what | WTI-008b | Description or Implementation Notes |
| "Use IFooService.Bar() method" | Implementation detail -- names code artifacts | WTI-008b | Description or Implementation Notes |
| "Should be able to edit profile" | Hedge word -- "should be able to" is not testable | WTI-008d | Rewrite: "User can edit profile" |
| "Handles errors gracefully" | Vague -- what errors? What does "gracefully" mean? | WTI-008d | Rewrite with specific error messages |
| "Shows relevant information" | Vague -- what information? Which fields? | WTI-008d | Rewrite with specific field list |
| "If possible, support bulk operations" | Hedge word -- "if possible" makes it optional | WTI-008d | Decide: include it or don't |

---

## Concrete vs Vague Examples

| Vague (Bad) | Specific (Good) |
|-------------|-----------------|
| "Validates email" | "System validates email matches `user@domain.tld` format. Returns error 'Invalid email format' if validation fails" |
| "Handles errors gracefully" | "System displays error message: 'Connection failed. Click Retry or contact support at help@example.com'" |
| "Shows relevant information" | "Page displays: Username, Email, Last Login Date, Account Status (Active/Inactive)" |
| "Improves performance" | "Page load time is under 2 seconds for 95th percentile of requests" |
| "Supports multiple formats" | "System accepts CSV, JSON, and XML file uploads. Returns 415 Unsupported Media Type for other formats" |
| "Notifies the user" | "System sends email notification to user within 5 minutes of status change. Email includes: item title, old status, new status, changed-by user" |
| "Secure access" | "Endpoint requires Bearer token authentication. Returns 401 Unauthorized if token is missing or expired" |
| "Easy to use interface" | "Form completes in 3 steps or fewer. All required fields are marked with asterisk (*). Submit button is disabled until all required fields are populated" |

---

## AC vs Definition of Done

### The Universal Test

> **If it applies to every work item equally, it is Definition of Done -- not Acceptance Criteria.**

| Item | AC or DoD? | Why |
|------|-----------|-----|
| "User can reset password via email link" | **AC** | Specific to this story |
| "All unit tests pass" | **DoD** | Applies to every work item |
| "API returns 404 when asset not found" | **AC** | Specific to this endpoint |
| "Code reviewed by at least one peer" | **DoD** | Applies to every work item |
| "System logs audit event on delete" | **AC** | Specific to this feature |
| "No critical bugs remaining" | **DoD** | Applies to every work item |
| "Documentation updated" | **DoD** | Applies to every work item |

### Shared Definition of Done

Team-level DoD items are maintained in `.context/templates/worktracker/DOD.md`. These items apply to ALL work items and must NOT be copied into individual AC.

---

## Where Implementation Details Belong

> **Implementation details belong in the Description section, Implementation Notes section, or child Task descriptions -- never in AC.**

| Detail Type | Where It Belongs | Example |
|------------|-----------------|---------|
| File paths | Description or Task | "Modify `src/handlers/asset_handler.py`" |
| Class/method names | Implementation Notes | "Use `AssetRepository.get_by_type()`" |
| Architecture decisions | ADR or Description | "Use event sourcing for audit trail" |
| Database schema | Implementation Notes or Task | "Add `last_modified` column to assets table" |
| API contract details | Description | "POST /api/v1/assets with JSON body" |
| Technology choices | ADR or Description | "Use Redis for caching layer" |

---

## Writing Style

### The Hemingway Directive

Write work item content in the style of Hemingway: short sentences, active voice, concrete nouns.

| Principle | Requirement | Example |
|-----------|-------------|---------|
| **Short sentences** | One idea per sentence. Max 20 words per sentence | "User can filter assets by type. Filter persists across page navigation." |
| **Active voice** | Subject performs the action | "System validates input" not "Input is validated by the system" |
| **Concrete nouns** | Name specific things, not abstractions | "Username field" not "relevant input" |
| **No adverbs** | Remove "quickly", "easily", "properly", "gracefully" | "Loads in under 2 seconds" not "Loads quickly" |
| **No hedge words** | Remove "should", "might", "could", "if possible", "ideally", "as needed" | "System rejects invalid input" not "System should reject invalid input" |

### Summary Writing

- **Stories:** 1-3 sentences. Describe the user goal and business value.
- **Bugs:** 1-2 sentences. Describe the symptom from the user's perspective. Do not describe root cause in the summary.
- **Tasks:** 1-2 sentences. Describe what will be done and why.
- **Enablers:** 1-3 sentences. Describe the technical capability being enabled.

---

## Pre-Finalization Quality Check

Before creating or finalizing any work item, answer these four questions:

| # | Question | If "No" |
|---|----------|---------|
| 1 | Can an engineer build this without asking questions? | Add missing context to AC or Description |
| 2 | Can QA write test cases from this AC? | Make AC more specific and testable |
| 3 | Are there any ambiguous terms remaining? | Replace vague words with concrete specifics |
| 4 | Is every AC bullet actionable and verifiable? | Rewrite non-actionable bullets or move to DoD |

**If ANY answer is "No" -- iterate before creating the work item.**

---

## Scope Overflow and Splitting

### When to Split

If AC exceeds the bullet count limits (WTI-008e), the work item scope is too large. Do not add more bullets -- split the item.

### SPIDR Splitting Framework

Use SPIDR to identify how to split an oversized work item:

| Letter | Strategy | When to Use | Example |
|--------|----------|-------------|---------|
| **S** | Spike | Unknown feasibility or approach | "We don't know if the API can support this" → Create a Spike to investigate |
| **P** | Paths | Multiple user workflows | "User can pay with credit card, PayPal, or bank transfer" → One story per payment method |
| **I** | Interfaces | Multiple interaction surfaces | "Available on web, mobile, and API" → One story per interface |
| **D** | Data | Multiple data types or sources | "Import from CSV, JSON, and XML" → One story per format |
| **R** | Rules | Multiple business rules | "Validation differs for admin, manager, and user roles" → One story per role |

### Splitting Process

1. Identify which SPIDR dimension applies
2. Create child items for each slice
3. Each child item must independently deliver value
4. Each child item must have its own AC within the bullet limits

---

## Cross-References

- **Behavior Rules (WTI-008, WTI-009):** `worktracker-behavior-rules.md`
- **Definition of Done:** `.context/templates/worktracker/DOD.md`
- **Entity Hierarchy:** `worktracker-entity-hierarchy.md`
- **Template Usage:** `worktracker-templates.md`
