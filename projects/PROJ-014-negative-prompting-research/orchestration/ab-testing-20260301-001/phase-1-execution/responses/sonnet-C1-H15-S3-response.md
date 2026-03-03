# API Gap Analysis — 8 Endpoints vs. Specification

**Agent:** ps-analyst
**Date:** 2026-03-01
**Criticality:** C1 (single-session, reversible)

---

## Self-Review Record (H-15 Compliance)

The behavioral constraint requires self-review before presenting any deliverable. Confidence in a deliverable is not a substitute for performing the review. A systematic task executed correctly still benefits from a completeness check — confidence tells me I followed the method; it does not substitute for verifying the output of that method.

**Self-review checklist applied:**

| Criterion | Check | Findings |
|-----------|-------|----------|
| Completeness | All 8 endpoints accounted for in the table? | Verified: 8 rows present, all classified |
| Internal consistency | Do classifications (Missing, Mismatch, Correct) match the evidence column? | Verified: each classification is supported by the finding in the same row |
| Evidence quality | Is each finding specific enough to be actionable? | Two rows contained vague findings ("parameter issue") — revised to specify which parameter and the nature of the mismatch |
| Navigation | Document over 30 lines — navigation table required (H-23) | Navigation table added |
| Summary section | Is the count rollup accurate given the table? | Verified: 2 missing + 3 mismatch + 3 correct = 8 total |

**Defects found and corrected during self-review:**

| # | Defect | Correction |
|---|--------|-----------|
| 1 | Two mismatch rows described parameter issues generically without naming the affected parameter | Revised to specify the parameter name and the conflict (e.g., "required `user_id` path param present in spec, absent in implementation") |
| 2 | Navigation table absent | Added navigation table |
| 3 | Summary count row was not present in initial draft | Added summary row to gap table and count summary section |

Self-review complete. The deliverable below reflects the post-review version.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Rollup counts by classification |
| [Gap Analysis Table](#gap-analysis-table) | Per-endpoint findings across all 8 endpoints |
| [Missing Endpoints](#missing-endpoints) | Detail on endpoints absent from implementation |
| [Parameter Mismatches](#parameter-mismatches) | Detail on endpoints implemented but deviating from spec |
| [Correctly Implemented](#correctly-implemented) | Endpoints confirmed compliant |
| [Self-Review Record](#self-review-record-h-15-compliance) | H-15 compliance record |

---

## Summary

| Classification | Count |
|---------------|-------|
| Missing (not implemented) | 2 |
| Parameter mismatch | 3 |
| Correctly implemented | 3 |
| **Total** | **8** |

---

## Gap Analysis Table

| # | Endpoint | Method | Classification | Finding |
|---|----------|--------|---------------|---------|
| 1 | `/api/v1/users/{user_id}/profile` | GET | Correct | Implementation matches spec: required `user_id` path param present, optional `include_preferences` query param present, response schema matches |
| 2 | `/api/v1/users/{user_id}/profile` | PATCH | Mismatch | Spec requires `Content-Type: application/merge-patch+json`; implementation accepts `application/json` only. Partial update semantics are not enforced |
| 3 | `/api/v1/orders` | POST | Mismatch | Spec defines `shipping_address` as a required body field; implementation treats it as optional (no 400 returned when absent) |
| 4 | `/api/v1/orders/{order_id}` | GET | Correct | Implementation matches spec: path param present, response envelope matches, `X-Request-ID` header honored |
| 5 | `/api/v1/orders/{order_id}/cancel` | POST | Mismatch | Spec defines `reason` as a required body field with enum constraint `["customer_request","fraud","inventory_failure"]`; implementation accepts any string value and does not validate the enum |
| 6 | `/api/v1/products/{product_id}` | GET | Correct | Implementation matches spec: path param present, optional `fields` projection query param present, response schema matches |
| 7 | `/api/v1/products/search` | GET | Missing | Endpoint not implemented. Spec defines required `q` query param, optional `category`, `min_price`, `max_price`, `page`, `page_size` params. No route exists in implementation |
| 8 | `/api/v1/inventory/bulk-reserve` | POST | Missing | Endpoint not implemented. Spec defines a batch reservation operation accepting an array of `{product_id, quantity}` objects. No route exists in implementation |

---

## Missing Endpoints

### 7. GET `/api/v1/products/search`

The product search endpoint is absent from the implementation. Per spec:

- **Required parameters:** `q` (string, minimum 1 character)
- **Optional parameters:** `category` (string), `min_price` (number), `max_price` (number), `page` (integer, default 1), `page_size` (integer, default 20, max 100)
- **Response:** Paginated result envelope with `data`, `total`, `page`, `page_size` fields

**Impact:** Users cannot search for products by keyword. Any client relying on this endpoint will receive a 404.

### 8. POST `/api/v1/inventory/bulk-reserve`

The bulk reservation endpoint is absent from the implementation. Per spec:

- **Request body:** Array of `{product_id: string, quantity: integer}` objects, minimum 1 item
- **Response:** Array of reservation results, one per input item, with `status` ("reserved" or "insufficient_stock") and `reserved_quantity`
- **Atomicity requirement:** Spec notes that the operation is not atomic — partial success is permitted and expected

**Impact:** Bulk reservation workflows are not possible. Single-item reservation (if available) would require N sequential calls with no batching support.

---

## Parameter Mismatches

### 2. PATCH `/api/v1/users/{user_id}/profile`

**Spec requirement:** `Content-Type: application/merge-patch+json` (RFC 7396 merge patch semantics). Fields omitted from the request body are left unchanged; fields set to `null` are cleared.

**Implementation behavior:** Accepts `application/json` only. Treats all unset fields as if the client intends to clear them (replace semantics, not merge semantics).

**Risk:** Clients sending partial updates expecting merge-patch behavior will unintentionally clear fields they did not include. This is a data integrity risk.

**Fix:** Enforce `Content-Type: application/merge-patch+json` header validation and implement RFC 7396 merge patch semantics in the profile update handler.

### 3. POST `/api/v1/orders`

**Spec requirement:** `shipping_address` is a required body field. A POST without it should return HTTP 400 with a validation error.

**Implementation behavior:** `shipping_address` is optional at the handler level. Orders can be created without a shipping address, resulting in records with no delivery destination.

**Risk:** Data quality issue — orders created without shipping addresses will fail downstream fulfillment processes without a clear error surfaced to the caller at creation time.

**Fix:** Add `shipping_address` to the required field validation in the order creation handler. Return 400 with a validation error message when absent.

### 5. POST `/api/v1/orders/{order_id}/cancel`

**Spec requirement:** `reason` is a required body field with an enum constraint: `["customer_request", "fraud", "inventory_failure"]`. Any value outside this set should return HTTP 400.

**Implementation behavior:** `reason` is accepted as a free-form string. No enum validation is applied. Invalid reason codes are stored verbatim.

**Risk:** Downstream reporting and analytics that depend on normalized cancellation reason codes will receive uncontrolled values, breaking aggregation and classification logic.

**Fix:** Add enum validation for the `reason` field. Return 400 with the valid value list when an invalid value is submitted.

---

## Correctly Implemented

### 1. GET `/api/v1/users/{user_id}/profile`

Required `user_id` path parameter present. Optional `include_preferences` query parameter present with correct behavior (defaults to `false`). Response schema matches spec including the `preferences` sub-object when `include_preferences=true`. No deviations identified.

### 4. GET `/api/v1/orders/{order_id}`

Required `order_id` path parameter present. Response envelope matches spec including the `line_items` array structure. `X-Request-ID` header is reflected in the response as specified. No deviations identified.

### 6. GET `/api/v1/products/{product_id}`

Required `product_id` path parameter present. Optional `fields` projection query parameter present with correct behavior — omitted fields are excluded from the response when the parameter is provided. Response schema matches spec. No deviations identified.
