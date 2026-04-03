# UC-to-Contract Transformation Rules

> **File ID:** F-14 | **Skill:** /contract-design | **Version:** 1.0.0
> **Author:** eng-backend | **Date:** 2026-03-09 | **Criticality:** C3
> **Status:** PROPOSED
> **Purpose:** Encodes the novel UC-to-OpenAPI transformation algorithm as imperative rules
> **Pattern:** Follows `skills/test-spec/rules/clark-transformation-rules.md` format
> **Architecture:** Architecture Section 4.5 and Section 7 (step-11-contract-design-architecture.md v1.1.0)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Algorithm scope, format, and usage |
| [Resource Identification Rules (RI)](#resource-identification-rules-ri) | RULE-RI-01 through RULE-RI-03 |
| [Operation Mapping Rules (OM)](#operation-mapping-rules-om) | RULE-OM-01 through RULE-OM-04 |
| [HTTP Method Inference Rules (HM)](#http-method-inference-rules-hm) | RULE-HM-01 through RULE-HM-05 |
| [Schema Derivation Rules (SD)](#schema-derivation-rules-sd) | RULE-SD-01 through RULE-SD-04 |
| [Error Response Rules (ER)](#error-response-rules-er) | RULE-ER-01 through RULE-ER-03 |
| [Actor Role Rules (AR)](#actor-role-rules-ar) | RULE-AR-01 through RULE-AR-03 |
| [Traceability Rules (TR)](#traceability-rules-tr) | RULE-TR-01 through RULE-TR-02 |
| [Rule Summary Index](#rule-summary-index) | Quick reference table of all 22 rules |
| [Algorithm Step-to-Rule Mapping](#algorithm-step-to-rule-mapping) | Maps cd-generator methodology steps to rules |

---

## Overview

This file encodes the novel UC-to-contract transformation algorithm that `cd-generator` applies when transforming use case interaction artifacts into OpenAPI 3.1 specifications. The algorithm has no prior art; these rules represent the first formalization of the UC-to-OpenAPI transformation pattern within the Jerry Framework.

### Rule Format

Each rule follows this format:

```
RULE-{CATEGORY}-{NN}: {imperative statement}
  Input:   {schema fields read from the UC artifact}
  Output:  {OpenAPI element produced}
  Example: {concrete mapping example from UC-LIB-001 worked example}
```

**Rule categories:**

| Category | Abbreviation | Count |
|----------|-------------|-------|
| Resource Identification | RI | 3 |
| Operation Mapping | OM | 4 |
| HTTP Method Inference | HM | 5 |
| Schema Derivation | SD | 4 |
| Error Response | ER | 3 |
| Actor Role | AR | 3 |
| Traceability | TR | 2 |
| **Total** | | **24** |

### Input Schema Reference

Rules reference fields from `docs/schemas/use-case-realization-v1.schema.json`. Key paths:

| JSON Path | Description |
|-----------|-------------|
| `$.interactions[*].id` | Interaction identifier (e.g., INT-01) |
| `$.interactions[*].source_step` | Step number in the source flow |
| `$.interactions[*].source_flow` | Flow name (basic_flow, AF-01, etc.) |
| `$.interactions[*].actor_role` | `consumer` or `provider` |
| `$.interactions[*].system_role` | `receiver` or `initiator` |
| `$.interactions[*].request_description` | Natural language request text |
| `$.interactions[*].response_description` | Natural language response text |
| `$.interactions[*].preconditions[*]` | Pre-state requirements for the request |
| `$.interactions[*].postconditions[*]` | Post-state guarantees from the response |
| `$.extensions[*].id` | Extension identifier (e.g., EXT-2a) |
| `$.extensions[*].anchor_step` | Step number where the extension branches |
| `$.extensions[*].condition` | Natural language condition text |
| `$.extensions[*].outcome` | `failure`, `success`, or `rejoin:{N}` |
| `$.primary_actor` | Primary actor name |
| `$.supporting_actors[*]` | Supporting actor entries |
| `$.title` | Use case title |
| `$.scope` | Use case scope |

---

## Resource Identification Rules (RI)

Resource identification determines which URL path segments to create. Resources are the nouns that the API exposes, not the verbs of the interaction.

---

**RULE-RI-01:** Extract the API resource noun from the system action in the response description, not from the request verb.

  Input:   `$.interactions[*].response_description` (primary), `$.interactions[*].request_description` (secondary)
  Output:  Resource noun used to form the URL path segment (e.g., "loan", "book", "member")
  Example: Response description "creates a loan record, updates book copy status to CHECKED_OUT, and returns a due-date slip" -> resource noun is "loan" (the object created). Path segment: `/loans` (plural, lowercase).

  **Derivation:** The system action in the response description identifies what the system creates, reads, updates, or deletes. This is the resource. The request verb (what the actor does) identifies the HTTP method (see RULE-HM-xx), not the resource. Using the system action avoids conflating the actor's intent (borrow) with the API resource (loan).

---

**RULE-RI-02:** Form the URL path segment as the lowercase plural of the resource noun, prefixed with `/`.

  Input:   Resource noun extracted by RULE-RI-01
  Output:  `paths` key entry (e.g., `/loans`, `/books`, `/members`)
  Example: Resource noun "loan" -> path segment `/loans`. Resource noun "book copy" -> path segment `/book-copies` (hyphenated, plural).

  **Derivation:** REST convention (Richardson et al.) prescribes plural lowercase nouns for collection resources. Hyphens replace spaces in multi-word nouns. This rule produces URL-safe path segments consistent with REST API design practice.

---

**RULE-RI-03:** Group multiple interactions that operate on the same resource under one path key. Distinguish operations within the path by HTTP method.

  Input:   All `$.interactions[*]` with `actor_role = consumer`
  Output:  Merged `paths` entries: one path key with multiple HTTP method operations when multiple interactions reference the same resource
  Example: INT-01 (create loan -> POST /loans) and INT-04 (retrieve loan -> GET /loans/{loan_id}) both operate on "loan". They share the `/loans` path group: `paths: { /loans: { post: {...} }, /loans/{loan_id}: { get: {...} } }`.

  **Derivation:** OpenAPI groups operations by path, not by interaction. Grouping by resource produces a coherent resource-oriented API surface. The path-item object is the correct grouping level for multiple operations on the same resource.

---

## Operation Mapping Rules (OM)

Operation mapping determines which interactions produce external API paths and which are documented as internal operations.

---

**RULE-OM-01:** Map each interaction where `actor_role = consumer` to one external path+operation in the `paths` section.

  Input:   `$.interactions[*]` where `actor_role = consumer`
  Output:  One path+operation entry in `paths` (external API surface)
  Example: INT-01 with `actor_role = consumer` -> `paths: { /loans: { post: { operationId: "createLoan", ... } } }`

  **Derivation:** Consumer interactions represent external actors (primary actors, system users) making requests to the system. External actor requests are the primary surface of a REST API. Each consumer interaction is one API endpoint.

---

**RULE-OM-02:** Map each interaction where `actor_role = provider` to one entry in the top-level `x-internal-operations` extension array. Do NOT expose as a `paths` entry.

  Input:   `$.interactions[*]` where `actor_role = provider`
  Output:  Entry in `x-internal-operations` array (documentation only, not an API endpoint)
  Example: INT-02 with `actor_role = provider` (system calls external catalog service) -> `x-internal-operations: [{ interaction_id: "INT-02", source_step: 3, description: "system queries catalog service for book availability", supporting_actor: "Catalog Service" }]`

  **Derivation:** Provider interactions represent the system acting as a client to external services. These are internal implementation details, not API endpoints. Documenting them in `x-internal-operations` preserves the information for implementers without polluting the external API surface.

---

**RULE-OM-03:** Map each interaction where `system_role = initiator` to an `x-internal-operations` entry, regardless of `actor_role`. System-initiated interactions are never external API endpoints.

  Input:   `$.interactions[*]` where `system_role = initiator`
  Output:  Entry in `x-internal-operations` array
  Example: INT-05 with `system_role = initiator` (system sends notification to member) -> `x-internal-operations: [{ interaction_id: "INT-05", source_step: 5, description: "system sends loan confirmation to member", supporting_actor: "Notification Service" }]`

  **Derivation:** When the system initiates an interaction, it is acting as a client, not a server. Client-initiated system actions are implementation details irrelevant to external API consumers but important to document for implementers.

---

**RULE-OM-04:** Each interaction maps to exactly one operation. Do not merge multiple interactions into a single operation, and do not split one interaction into multiple operations.

  Input:   Any `$.interactions[*]` entry
  Output:  Exactly one path+operation (for consumer) or one `x-internal-operations` entry (for provider)
  Example: INT-01 creates exactly one POST /loans operation. If the use case has 3 consumer interactions (INT-01, INT-02, INT-03), the contract has exactly 3 external operations.

  **Derivation:** The 1:1 mapping is the core traceability guarantee of the transformation. Merging operations loses the ability to trace individual behaviors. Splitting an operation invents API surface that has no use case provenance (METHODOLOGY VIOLATION).

---

## HTTP Method Inference Rules (HM)

HTTP method inference derives the correct HTTP method from the natural language request description. Rules are grounded in RFC 9110 (HTTP Semantics), Section 9.

---

**RULE-HM-01:** Infer GET when `request_description` contains read/retrieval verbs: read, query, get, fetch, retrieve, look up, search, list, find.

  Input:   `$.interactions[*].request_description` (verb analysis)
  Output:  `get:` operation in the corresponding `paths` entry
  Confidence: High
  Annotation: `x-method-inference: "high"`
  Example: "retrieves the member's current loan list" -> GET /loans. "searches for available copies of a book" -> GET /books?query=...
  RFC 9110 basis: Section 9.3.1 -- GET is safe (no state change) and idempotent; aligns with read/retrieval semantics.

---

**RULE-HM-02:** Infer POST when `request_description` contains creation/submission verbs: create, add, submit, register, initiate, start, send, post, requests (in context of creating/submitting).

  Input:   `$.interactions[*].request_description` (verb analysis)
  Output:  `post:` operation in the corresponding `paths` entry
  Confidence: High
  Annotation: `x-method-inference: "high"`
  Example: "presents library card and requests a specific book copy for borrowing" -> POST /loans (creates a loan resource). "submits a book return" -> POST /returns.
  RFC 9110 basis: Section 9.3.3 -- POST requests that the target resource process the representation; aligns with create/submit/initiate semantics.

---

**RULE-HM-03:** Infer PUT (full replacement) or PATCH (partial modification) when `request_description` contains update verbs: update, modify, change, edit, set, replace. Use PUT when all resource fields are involved; use PATCH when only specific fields are targeted.

  Input:   `$.interactions[*].request_description` (verb analysis + field specificity analysis)
  Output:  `put:` or `patch:` operation in the corresponding `paths` entry
  Confidence: Medium (judgment required for PUT vs. PATCH disambiguation)
  Annotation: `x-method-inference: "medium"`
  Example: "updates all details of the member profile" -> PUT /members/{member_id}. "changes the member's email address" -> PATCH /members/{member_id}.
  RFC 9110 basis: Section 9.3.4 (PUT -- idempotent full replacement), RFC 5789 / RFC 9110 Section 18.4 (PATCH -- partial modification).
  Disambiguation rule: When the request_description targets a specific named attribute (email, status, name), use PATCH. When it targets the full resource representation, use PUT. When ambiguous, default to PATCH and annotate with `x-method-inference: "medium"`.

---

**RULE-HM-04:** Infer DELETE when `request_description` contains removal/termination verbs: delete, remove, cancel, revoke, deactivate, terminate, void, expire.

  Input:   `$.interactions[*].request_description` (verb analysis)
  Output:  `delete:` operation in the corresponding `paths` entry
  Confidence: High
  Annotation: `x-method-inference: "high"`
  Example: "cancels the active loan" -> DELETE /loans/{loan_id}. "deactivates the member account" -> DELETE /members/{member_id} or PATCH /members/{member_id} (use PATCH if soft-delete, DELETE if hard-delete -- see RULE-HM-03 disambiguation).
  RFC 9110 basis: Section 9.3.5 -- DELETE removes the target resource association.

---

**RULE-HM-05:** When `request_description` does not match any verb pattern in RULE-HM-01 through RULE-HM-04, default to POST and annotate with `x-method-inference: "low"`.

  Input:   `$.interactions[*].request_description` (no matching verb pattern)
  Output:  `post:` operation with `x-method-inference: "low"` annotation
  Confidence: Low
  Annotation: `x-method-inference: "low"` (triggers cd-validator flag for human review)
  Example: "presents the membership card for system processing" -- ambiguous; defaults to POST /membership-cards or POST /membership-card-validations. Annotated for human review.
  Rationale: POST is the safe default because it is non-idempotent and semantically broad per RFC 9110 Section 9.3.3. Code generators and implementers can substitute a more specific method after human review of the source use case.

---

## Schema Derivation Rules (SD)

Schema derivation extracts request and response data shapes from the structured pre/postcondition lists in each interaction.

---

**RULE-SD-01:** Derive request schema properties from `$.interactions[*].preconditions[*]`. Each precondition that asserts the presence or state of a specific named entity maps to one request body property.

  Input:   `$.interactions[*].preconditions[*]` (array of natural language condition strings)
  Output:  `components/schemas/{REQUEST_SCHEMA_NAME}.properties` entries
  Example: Preconditions ["Member holds a valid, active library card", "Requested book copy is available for loan"] -> properties: { member_card_id: { type: string, description: "Valid, active library card identifier" }, book_copy_id: { type: string, description: "Identifier of the specific book copy requested" } }

  **Named entity extraction rule:** Look for noun phrases that identify a verifiable data item. "Valid, active library card" -> `member_card_id`. "Specific book copy" -> `book_copy_id`. Ignore non-data conditions (e.g., "Member has no outstanding overdue books" is a system-checkable state, not a request property -- it becomes a 4xx error response via RULE-ER-01).

  **Required field determination:** A property is required if the interaction cannot proceed without it. Entity identifiers are always required. Optional properties are those flagged as "if present" or "when applicable" in the precondition text.

---

**RULE-SD-02:** Derive response schema properties from `$.interactions[*].postconditions[*]`. Each postcondition that guarantees a state change or a returned data item maps to one response body property.

  Input:   `$.interactions[*].postconditions[*]` (array of natural language guarantee strings)
  Output:  `components/schemas/{RESPONSE_SCHEMA_NAME}.properties` entries
  Example: Postconditions ["Loan record created linking the member to the book copy", "Book copy status changed to CHECKED_OUT", "Due date issued to the member"] -> properties: { loan_id: { type: string }, book_copy_id: { type: string }, status: { type: string, enum: [CHECKED_OUT] }, due_date: { type: string, format: date } }

  **State guarantee mapping:** Postconditions asserting state changes produce response properties that confirm the new state. "Loan record created" -> `loan_id` (the record identifier is returned as confirmation). "Status changed to CHECKED_OUT" -> `status: { enum: [CHECKED_OUT] }`.

---

**RULE-SD-03:** Select the success HTTP status code from the response semantics and the HTTP method.

  Input:   HTTP method (from RULE-HM-xx), `$.interactions[*].response_description` semantics
  Output:  Response key in the `responses` map (200, 201, or 204)
  Table:
  | HTTP Method | Response Semantics | Status Code |
  |-------------|-------------------|------------|
  | POST | Resource created; identifier returned | 201 Created |
  | GET | Resource representation returned | 200 OK |
  | PUT | Resource replaced; representation returned | 200 OK |
  | PATCH | Resource updated; updated representation returned | 200 OK |
  | DELETE | Resource deleted; no content | 204 No Content |
  | DELETE | Resource deleted; confirmation body | 200 OK |
  Example: POST /loans with "creates a loan record and returns a due-date slip" -> 201 Created.

---

**RULE-SD-04:** When a postcondition specifies a discrete named state value, generate an `enum` constraint on the corresponding property.

  Input:   `$.interactions[*].postconditions[*]` containing phrases like "changed to {STATE_NAME}", "set to {STATE_NAME}", "status is {STATE_NAME}"
  Output:  `enum: [{STATE_NAME}]` on the response schema property
  Example: "Book copy status changed to CHECKED_OUT" -> `status: { type: string, enum: [CHECKED_OUT] }`. "Loan status is RETURNED" -> `status: { type: string, enum: [RETURNED] }`.

  **Rationale:** Enum constraints on state properties enable client-side validation and documentation of valid discrete states. The enum is derived from the use case postcondition -- not invented.

---

## Error Response Rules (ER)

Error response rules map use case extensions (failure conditions) to HTTP error responses on the appropriate operations.

---

**RULE-ER-01:** Map each `$.extensions[*]` with `outcome = failure` to an HTTP error response on the operation(s) whose `source_step` matches the extension's `anchor_step`.

  Input:   `$.extensions[*]` where `outcome = failure`; `$.interactions[*].source_step` for cross-referencing
  Output:  Error response entry in the `responses` map of the matched operation(s)
  Cross-reference: Extension `anchor_step` is matched against interaction `source_step`. When an interaction's `source_step` equals (or is within the boundary range of) an extension's `anchor_step`, the extension becomes an error response on that operation.

  **HTTP status code classification sub-rules:**

  RULE-ER-01a: Condition implies invalid or malformed input -> 400 Bad Request
    Example: "Member provides an invalid library card number" -> 400.

  RULE-ER-01b: Condition implies access denied, unauthorized, or forbidden -> 401 Unauthorized (missing authentication) or 403 Forbidden (authenticated but not authorized)
    Example: "Member account is suspended" -> 403.

  RULE-ER-01c: Condition implies the requested resource does not exist -> 404 Not Found
    Example: "Requested book copy does not exist in catalog" -> 404.

  RULE-ER-01d: Condition implies a state conflict or business rule violation (resource exists but state prevents the operation) -> 409 Conflict
    Example: "Member has outstanding overdue books" -> 409 (the member exists but state prevents loan creation). "Book copy is already checked out" -> 409.

  RULE-ER-01e: Condition implies a system failure or internal error -> 500 Internal Server Error
    Example: "External catalog service is unavailable" -> 500 (or 503 Service Unavailable if availability is the specific issue).

  RULE-ER-01f: Condition does not match any pattern above -> 422 Unprocessable Entity (default) + `x-error-inference: "low"` annotation
    Example: Unclassifiable condition text -> 422 with annotation flagging for human review.

---

**RULE-ER-02:** Map each `$.extensions[*]` with `outcome = success` to an alternative 2xx response variant on the matched operation.

  Input:   `$.extensions[*]` where `outcome = success`
  Output:  Additional 2xx response key in the `responses` map (e.g., 200 as an alternative to 201 for a create operation)
  Example: Extension "Member is a first-time borrower -- system waives the usual processing fee and creates the loan" with outcome=success -> additional 200 response on POST /loans indicating "loan created with fee waiver".

  **Rationale:** Success extensions represent alternative happy paths in the use case. They become additional success response variants in the contract, allowing clients to distinguish between standard and variant success outcomes.

---

**RULE-ER-03:** Annotate every error response with `x-source-extension: "{extension_id}"` to maintain traceability from contract error response back to source extension.

  Input:   Extension ID from `$.extensions[*].id` (e.g., EXT-2a)
  Output:  `x-source-extension: "EXT-2a"` annotation on the error response entry
  Example: Error response 409 derived from EXT-2a -> `responses: { "409": { description: "Member has outstanding overdue books", x-source-extension: "EXT-2a", content: { application/json: { schema: { $ref: "#/components/schemas/ErrorResponse" } } } } }`

  **Rationale:** Traceability from contract back to use case source applies to error responses as well as success operations. Without this annotation, implementers cannot verify that a 409 response is intentional (from the use case) rather than incidental (added without use case basis).

---

## Actor Role Rules (AR)

Actor role rules govern how use case actor classifications map to OpenAPI consumer/provider documentation.

---

**RULE-AR-01:** Map `$.primary_actor` to `info.x-primary-actor` in the OpenAPI `info` section.

  Input:   `$.primary_actor` (string)
  Output:  `info.x-primary-actor: "{primary_actor_name}"`
  Example: `$.primary_actor = "Library Member"` -> `info: { x-primary-actor: "Library Member" }`

  **Rationale:** The primary actor is the intended consumer of the external API surface. Documenting this in the `info` section orients API consumers and gateway administrators to the intended user of the API.

---

**RULE-AR-02:** When a supporting actor appears as the `actor_role` in a provider interaction (the supporting actor calls the system), document the interaction in `x-internal-operations` and note the supporting actor as `supporting_actor`.

  Input:   `$.interactions[*]` where `actor_role = provider`; `$.supporting_actors[*]` for actor identification
  Output:  `x-internal-operations` entry with `supporting_actor` field
  Example: Interaction INT-03 where `actor_role = provider` and the system calls "Catalog Service" (a supporting actor) -> `x-internal-operations: [{ ..., supporting_actor: "Catalog Service" }]`

---

**RULE-AR-03:** Document each supporting actor (IC-05 cross-referencing) in `components/schemas` descriptions to make external dependencies visible to API consumers and implementers.

  Input:   `$.supporting_actors[*]` cross-referenced with interactions where the actor is referenced
  Output:  Description text in `components/schemas` noting the external dependency
  Example: `$.supporting_actors[0].name = "Librarian"` -- if no interaction references Librarian as `actor_role`, Librarian is documented as a `components/schemas` description: `schemas: { LibrarianRole: { type: string, description: "Librarian is a supporting actor (human) who may assist members but is not a direct API caller. IC-05 cross-reference: see supporting_actors in source UC artifact." } }`

  **Fallback when supporting_actors is absent:** Emit a warning in the L0 summary: "UC {id} has no supporting_actors. IC-05 cross-referencing will be limited." Proceed without RULE-AR-03 entries.

---

## Traceability Rules (TR)

Traceability rules ensure every element of the generated contract can be traced back to its source in the use case artifact.

---

**RULE-TR-01:** Annotate every external operation in `paths` with three traceability extension fields: `x-source-interaction`, `x-source-step`, `x-source-flow`.

  Input:   `$.interactions[*].id`, `$.interactions[*].source_step`, `$.interactions[*].source_flow`
  Output:  Three extension annotations on every operation object in `paths`
  Example: INT-01 (source_step: 1, source_flow: basic_flow) -> operation annotations: `x-source-interaction: "INT-01"`, `x-source-step: 1`, `x-source-flow: "basic_flow"`

  **Rationale:** These three annotations constitute the traceability chain from contract operation back to use case step. cd-validator uses these annotations to verify coverage (Step 6 of the validation protocol). Without them, the contract cannot be audited against the source use case.

---

**RULE-TR-02:** Include `x-prototype: true` in the `info` section of every generated contract. This is a non-negotiable output constraint.

  Input:   (No input required -- this annotation is always added regardless of input quality)
  Output:  `info.x-prototype: true` in the OpenAPI `info` section
  Example: `info: { title: "...", version: "...", x-prototype: true, x-source-use-case: "UC-LIB-001", ... }`

  **Rationale:** The UC-to-contract transformation algorithm is novel (G-01 gap). All generated contracts are prototype outputs until a human reviewer validates the semantic correctness of the transformation. The PROTOTYPE label prevents downstream consumers from treating the contract as production-ready. cd-validator Step 7 verifies this label is present and treats its absence as a mandatory FAIL.

---

## Rule Summary Index

| Rule ID | Category | Imperative Statement | Priority |
|---------|----------|---------------------|---------|
| RULE-RI-01 | Resource Identification | Extract resource noun from system action in response description | Required |
| RULE-RI-02 | Resource Identification | Form URL path segment as lowercase plural of resource noun | Required |
| RULE-RI-03 | Resource Identification | Group multiple interactions on the same resource under one path | Required |
| RULE-OM-01 | Operation Mapping | Map consumer interactions to external path+operations | Required |
| RULE-OM-02 | Operation Mapping | Map provider interactions to x-internal-operations | Required |
| RULE-OM-03 | Operation Mapping | Map system-initiator interactions to x-internal-operations | Required |
| RULE-OM-04 | Operation Mapping | One interaction maps to exactly one operation (1:1 invariant) | Required |
| RULE-HM-01 | HTTP Method | Read/query verbs -> GET (High confidence) | Required |
| RULE-HM-02 | HTTP Method | Create/submit verbs -> POST (High confidence) | Required |
| RULE-HM-03 | HTTP Method | Update/modify verbs -> PUT or PATCH (Medium confidence) | Required |
| RULE-HM-04 | HTTP Method | Delete/remove verbs -> DELETE (High confidence) | Required |
| RULE-HM-05 | HTTP Method | Ambiguous verbs -> POST + x-method-inference: low (Low confidence) | Required |
| RULE-SD-01 | Schema Derivation | Derive request schema from interaction preconditions | Required |
| RULE-SD-02 | Schema Derivation | Derive response schema from interaction postconditions | Required |
| RULE-SD-03 | Schema Derivation | Select success HTTP status code from method and response semantics | Required |
| RULE-SD-04 | Schema Derivation | Generate enum constraint for discrete named state values in postconditions | Required |
| RULE-ER-01 | Error Response | Map failure extensions to HTTP error responses on matched operations | Required |
| RULE-ER-01a-f | Error Response | Classify HTTP status code from extension condition semantics (sub-rules) | Required |
| RULE-ER-02 | Error Response | Map success extensions to alternative 2xx response variants | Required |
| RULE-ER-03 | Error Response | Annotate every error response with x-source-extension | Required |
| RULE-AR-01 | Actor Role | Map primary_actor to info.x-primary-actor | Required |
| RULE-AR-02 | Actor Role | Document provider interactions in x-internal-operations | Required |
| RULE-AR-03 | Actor Role | Document supporting actors in components/schemas descriptions (IC-05) | Required |
| RULE-TR-01 | Traceability | Annotate every external operation with x-source-interaction/step/flow | Required |
| RULE-TR-02 | Traceability | Include x-prototype: true in info section of every generated contract | Required (mandatory) |

---

## Algorithm Step-to-Rule Mapping

| cd-generator Methodology Step | Rules Applied |
|-------------------------------|--------------|
| Step 1: Input Validation Gate | (guardrails -- not a transformation rule) |
| Step 2: Resource Identification | RULE-RI-01, RULE-RI-02, RULE-RI-03 |
| Step 3: Operation Mapping | RULE-OM-01, RULE-OM-02, RULE-OM-03, RULE-OM-04 |
| Step 4: HTTP Method Inference | RULE-HM-01, RULE-HM-02, RULE-HM-03, RULE-HM-04, RULE-HM-05 |
| Step 5: Request Schema Derivation | RULE-SD-01 |
| Step 6: Response Schema Derivation | RULE-SD-02, RULE-SD-03, RULE-SD-04 |
| Step 7: Extension-to-Error Mapping | RULE-ER-01 (sub-rules a-f), RULE-ER-02, RULE-ER-03 |
| Step 8: Actor Role Resolution | RULE-AR-01, RULE-AR-02, RULE-AR-03 |
| Step 9: Compose and Write OpenAPI | RULE-TR-01, RULE-TR-02 (applied during composition) |

---

*Rules Version: 1.0.0 | Algorithm: UC-to-Contract v1.0.0 (novel -- G-01)*
*Source: step-11-contract-design-architecture.md (v1.1.0, 0.956 PASS), Section 4.5 and Section 7*
*External references: RFC 9110 (HTTP Semantics, Section 9), RFC 5789 (PATCH), OpenAPI 3.1.0 Specification*
*Pattern reference: skills/test-spec/rules/clark-transformation-rules.md*
