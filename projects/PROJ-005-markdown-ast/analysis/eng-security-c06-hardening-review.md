# C-06 Injection Protection Hardening -- Security Review

> eng-security agent review of the L2 Prompt Reinforcement Engine injection protection hardening.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Review Scope](#review-scope) | Files reviewed, threat model, and review methodology |
| [Findings Summary](#findings-summary) | Consolidated PASS/FAIL/ADVISORY verdicts |
| [F-01: Pattern Completeness](#f-01-pattern-completeness) | Coverage of injection vectors in _INJECTION_PATTERNS |
| [F-02: Regex Correctness](#f-02-regex-correctness) | Bypass opportunities through regex edge cases |
| [F-03: Defense-in-Depth](#f-03-defense-in-depth) | Layered protection assessment |
| [F-04: Logging Security](#f-04-logging-security) | Warning log data leakage and log injection risk |
| [F-05: Test Coverage](#f-05-test-coverage) | Test sufficiency and missing edge cases |
| [F-06: Content Regex Extraction Safety](#f-06-content-regex-extraction-safety) | Marker parsing regex security |
| [Recommendations](#recommendations) | Prioritized remediation actions |
| [Verdict](#verdict) | Overall security posture assessment |

---

## Review Scope

**Files reviewed:**

| File | Path | Lines |
|------|------|-------|
| Implementation | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | 321 |
| Tests | `tests/unit/enforcement/test_prompt_reinforcement_engine.py` | 619 |
| Data class | `src/infrastructure/internal/enforcement/reinforcement_content.py` | 36 |

**Threat model:** An attacker who can modify `.md` rule files in `.context/rules/` or `.claude/rules/` (via compromised PR, supply chain attack, or malicious contributor) attempts to inject executable content, prompt injection payloads, or HTML/script payloads into the L2 reinforcement preamble. The preamble is injected into every user prompt, so successful injection has high blast radius.

**Review methodology:** Static analysis of the regex patterns, control flow analysis, logging surface review, and test coverage gap analysis.

---

## Findings Summary

| ID | Category | Verdict | Severity | Description |
|----|----------|---------|----------|-------------|
| F-01 | Pattern Completeness | ADVISORY | Medium | Several additional injection vectors not covered |
| F-02 | Regex Correctness | PASS | -- | Regex is structurally correct; one minor advisory |
| F-03 | Defense-in-Depth | PASS | -- | Three-layer defense is well-designed |
| F-04 | Logging Security | PASS | -- | Logs do not leak content; no log injection risk |
| F-05 | Test Coverage | ADVISORY | Low | Good coverage; minor edge case gaps |
| F-06 | Content Regex Extraction | ADVISORY | Medium | Parsing regex provides implicit protection but has a theoretical concern |

---

## F-01: Pattern Completeness

**Verdict: ADVISORY (Medium)**

The current `_INJECTION_PATTERNS` regex covers:

| Pattern | Status |
|---------|--------|
| `<!--` / `-->` (HTML comment delimiters) | Covered |
| `<script` / `</script` | Covered |
| `<iframe` / `</iframe` | Covered |
| `<object` / `</object` | Covered |
| `<embed` / `</embed` | Covered |
| `javascript:` (URI scheme) | Covered |
| `data:text/html` (data URI) | Covered |

**Vectors NOT currently blocked:**

| Vector | Risk | Recommendation |
|--------|------|----------------|
| `<svg` / `</svg` | Medium -- SVG supports inline script execution via `<svg onload="...">` and nested `<script>` elements. In HTML rendering contexts, SVG is a common XSS vector. | Add to pattern. |
| `<math` / `</math` | Low -- MathML can carry event handlers in some browsers, but is less commonly exploited. | Consider adding. |
| `<form` / `<input` | Low -- Could construct phishing overlays in HTML rendering contexts. However, in an LLM preamble context, this is not a realistic attack surface. | Optional. |
| `<meta` | Low -- `<meta http-equiv="refresh">` can redirect. Not applicable in preamble context. | Optional. |
| `<base` | Medium -- `<base href="...">` can redirect all relative URLs. Could theoretically alter link resolution if preamble content is rendered as HTML. | Consider adding. |
| `<link` | Low -- Can load external stylesheets/resources. Minimal risk in preamble context. | Optional. |
| `on\w+=` (event handlers) | Medium -- Inline event handlers like `onload=`, `onerror=`, `onclick=` are a primary XSS vector. If any downstream consumer renders preamble content as HTML, these bypass tag-level blocking. | Add to pattern. |
| `vbscript:` | Low -- Legacy IE-only URI scheme. Minimal modern risk. | Optional. |
| `<template` / `<slot` | Low -- Web components. Not a realistic injection vector in this context. | Skip. |
| `expression(` (CSS expression) | Low -- Legacy IE CSS injection. Minimal modern risk. | Skip. |
| `data:` (broader match) | Low -- `data:text/html` is already covered. Other `data:` MIME types (e.g., `data:image/svg+xml`) could carry SVG payloads. | Consider broadening to `data:` with exclusion for safe types. |

**Analysis:** The current pattern set is appropriate for the primary threat model (preventing HTML/script injection). The most significant gaps are `<svg` and `on\w+=` event handlers, which are the two most common XSS bypass vectors in real-world security assessments. However, the practical exploitability is limited by the context: L2-REINJECT content is injected into an LLM prompt, not rendered as HTML. The risk materializes only if a downstream consumer renders this content in an HTML context (e.g., a web UI displaying session logs, a debug panel, or a reporting system that renders markdown).

**Recommendation:** Add `<svg`, `</svg`, and a generalized event handler pattern (`on\w+\s*=`) to the regex. These are low-cost additions that close the most probable bypass paths.

---

## F-02: Regex Correctness

**Verdict: PASS**

The compiled regex pattern uses `re.IGNORECASE` and alternation correctly.

**Analysis of potential bypass techniques:**

| Technique | Blocked? | Explanation |
|-----------|----------|-------------|
| Mixed case (`<ScRiPt>`) | Yes | `re.IGNORECASE` handles this |
| Null byte injection (`<scr\x00ipt>`) | N/A | The parsing regex `[^"]*?` for content extraction will not match null bytes in typical file reads; Python `read_text()` with UTF-8 encoding will either reject or pass through null bytes, but the content regex `[^"]*?` does match `\x00`. However, the injection pattern `<script` will NOT match `<scr\x00ipt`. |
| Whitespace insertion (`< script>`) | Not blocked | `<script` requires the `<` immediately followed by `script`. Adding a space (`< script`) bypasses the pattern. |
| HTML entity encoding (`&#60;script`) | Not blocked | Character entity references are not decoded before matching. |
| UTF-8 homoglyphs (`<scrіpt>` with Cyrillic `і`) | Not blocked | Homoglyph substitution bypasses ASCII pattern matching. |
| URL encoding (`%3Cscript`) | Not blocked | Not applicable -- content is read from files, not URLs. File content would contain literal `%3C`. |

**Assessment of whitespace bypass (`< script>`):** This is a theoretical bypass. In practice:
1. The content is extracted from L2-REINJECT markers in `.md` files within the repository
2. The content is injected into an LLM prompt, not rendered as HTML
3. The whitespace-inserted form (`< script>`) is not valid HTML and would not execute in any rendering context

The whitespace bypass is therefore not practically exploitable in this threat model.

**Assessment of null byte injection:** Python's `str.read_text(encoding="utf-8")` will raise `UnicodeDecodeError` for invalid UTF-8 sequences containing null bytes in positions where they are not valid. If a null byte does survive into the content string, the `_INJECTION_PATTERNS` regex would not match the split tag. However, null bytes in a `.md` file under version control would be immediately visible in code review and are not a realistic attack vector for this threat model.

**One minor observation:** The regex uses partial tag matching (e.g., `<script` not `<script>` or `<script[\s>]`). This is actually a strength -- it catches both `<script>` and `<script src="...">` variants. No change needed.

---

## F-03: Defense-in-Depth

**Verdict: PASS**

The C-06 protection uses a three-layer defense:

| Layer | Mechanism | What It Prevents |
|-------|-----------|------------------|
| 1. Length check | `_MAX_MARKER_CONTENT_LENGTH = 500` | Budget exhaustion, oversized payloads |
| 2. Pattern check | `_INJECTION_PATTERNS` regex | HTML/script injection |
| 3. Fail-open design | `except Exception` -> empty reinforcement | Engine failure does not block user interaction |

**Strengths:**

1. **Length check before pattern check.** The length check (O(1) operation) runs before the regex match (O(n) operation). This prevents ReDoS-style attacks where crafted content might cause catastrophic regex backtracking. The 500-character limit constrains the input size to the regex.

2. **Fail-open is correct for this use case.** The L2 engine is a quality enhancement layer, not a security gate. Failing open (empty reinforcement) means quality rules are not injected for one prompt, which degrades quality but does not create a security vulnerability. Failing closed (blocking the user prompt) would be a denial-of-service vector.

3. **Content extraction regex provides implicit sandboxing.** The marker parsing regex uses `[^"]*?` to extract content, which means content cannot contain double-quote characters. This prevents several injection classes where the attacker needs to break out of the content attribute to inject new marker attributes or close the HTML comment prematurely. For example, `content="payload" --> <script>evil</script> <!--"` would not match because the first `"` after `content="` would terminate the capture group.

4. **Static compilation of injection patterns.** `_INJECTION_PATTERNS` is compiled once as a class attribute, avoiding repeated compilation costs and ensuring consistent pattern application.

**One consideration:** The fail-open design means an attacker who can cause the engine to raise an exception (e.g., by corrupting the rules directory) can silently disable L2 enforcement. This is accepted risk per the design documentation ("engine is fail-open by design"). The L1 layer (session-start rules loading) provides the baseline, and L2 is a reinforcement layer. Disabling L2 degrades enforcement but does not eliminate it.

---

## F-04: Logging Security

**Verdict: PASS**

Two `logger.warning()` calls exist in the C-06 code path:

**Log statement 1 (oversized content):**
```python
logger.warning(
    "C-06: Rejected L2-REINJECT marker (rank=%s): "
    "content length %d exceeds max %d",
    match.group(1),      # rank number
    len(marker_content), # integer
    PromptReinforcementEngine._MAX_MARKER_CONTENT_LENGTH,  # integer constant
)
```

**Log statement 2 (injection pattern):**
```python
logger.warning(
    "C-06: Rejected L2-REINJECT marker (rank=%s): "
    "content matches injection pattern",
    match.group(1),  # rank number
)
```

**Analysis:**

| Risk | Status | Explanation |
|------|--------|-------------|
| Sensitive data leakage | Not present | Neither log statement includes the actual marker content. Only the rank number (an integer) and the content length (an integer) are logged. The malicious content itself is never written to logs. |
| Log injection (newline injection) | Not present | `match.group(1)` captures `(\d+)` which can only contain digits `[0-9]`. There is no path for newline characters, ANSI escape sequences, or other log injection payloads to reach the log output through this parameter. |
| Log injection (format string) | Not present | Python's `logger.warning()` uses `%s` / `%d` parameterized formatting, which does not interpret format specifiers within the parameters themselves. Even if `match.group(1)` somehow contained a format string like `%n`, it would be treated as a literal string. |
| Excessive logging (DoS) | Minimal risk | Each rejected marker produces one log line. An attacker would need to inject many malicious markers to produce excessive log volume. The 500-character content limit and the marker parsing regex constrain how many markers can exist in a file of reasonable size. |

**Assessment:** The logging implementation follows security best practices: it logs the fact of rejection and the reason, without logging the malicious content itself. This enables forensic analysis while preventing log-based information leakage.

---

## F-05: Test Coverage

**Verdict: ADVISORY (Low)**

The test suite contains 10 tests specifically for C-06 protection (in `TestParseReinjectMarkers`):

| Test | Vector Tested | Status |
|------|---------------|--------|
| `test_parse_markers_when_content_too_long_then_rejects` | Length > 500 | Present |
| `test_parse_markers_when_content_at_max_length_then_accepts` | Length == 500 (boundary) | Present |
| `test_parse_markers_when_content_has_html_comment_then_rejects` | `-->` | Present |
| `test_parse_markers_when_content_has_script_tag_then_rejects` | `<script>` | Present |
| `test_parse_markers_when_content_has_mixed_case_script_then_rejects` | `<ScRiPt>` | Present |
| `test_parse_markers_when_content_has_iframe_then_rejects` | `<iframe` | Present |
| `test_parse_markers_when_content_has_object_tag_then_rejects` | `<object` | Present |
| `test_parse_markers_when_content_has_embed_tag_then_rejects` | `<EMBED` (uppercase) | Present |
| `test_parse_markers_when_content_has_javascript_uri_then_rejects` | `JavaScript:` | Present |
| `test_parse_markers_when_content_has_data_html_uri_then_rejects` | `data:text/html` | Present |
| `test_parse_markers_when_oversized_content_then_logs_warning` | Log verification (oversized) | Present |
| `test_parse_markers_when_injection_detected_then_logs_warning` | Log verification (injection) | Present |

**Coverage is good.** The tests cover all currently blocked patterns and both logging paths.

**Missing edge cases (low priority):**

| Missing Test | Description | Priority |
|-------------|-------------|----------|
| `<!--` (opening comment delimiter) | Only `-->` is tested; opening delimiter `<!--` should also be tested. The test for `-->` (`test_parse_markers_when_content_has_html_comment_then_rejects`) uses `"Inject --> escape"` which also contains `-->`. A separate test for `<!--` within content would strengthen confidence. | Low -- `<!--` is in the regex and would be caught by the `[^"]*?` content extraction limit (the `<!--` in content would not break the outer marker because the outer marker's `-->` closing already matched). However, explicit test is good practice. |
| Content with `</script` (closing tag only, no opening) | Tests use `<script>alert(1)</script>` which tests both opening and closing. A test with only `</script` in isolation confirms the closing tag pattern works independently. | Low |
| Content exactly at length boundary minus 1 (499 chars) | Boundary testing: 499 should pass, 500 should pass, 501 should fail. 500 and 501 are tested; 499 is not. | Very Low |
| Multiple injection patterns in a single marker | Content containing multiple blocked patterns (e.g., `<script><iframe>`) to confirm the regex short-circuits on first match. | Very Low |
| Valid content interleaved with injection patterns | e.g., `"Valid rule <script> more text"` to confirm the pattern matches even when embedded in legitimate-looking content. | Low |
| Content with `data:text/html` in mixed case | e.g., `DATA:TEXT/HTML` to confirm `re.IGNORECASE` applies to multi-word patterns. | Low |

---

## F-06: Content Regex Extraction Safety

**Verdict: ADVISORY (Medium)**

The marker parsing regex:

```python
r'content="([^"]*?)"\s*'
```

Uses `[^"]*?` (non-greedy match of any character except double-quote). This provides implicit protection:

1. **Double-quote escape:** An attacker cannot include `"` in marker content. This prevents breaking out of the content attribute to inject new regex groups or close the HTML comment prematurely.

2. **HTML comment closure:** The outer regex requires `-->` after the content attribute. An attacker who injects `-->` inside the content would be caught by the `_INJECTION_PATTERNS` check (which blocks `-->`). Additionally, the outer regex would not match if `-->` appeared inside the content because `[^"]*?` would stop at the next `"`, and the sequence `content="...-->..."` would require the content to contain `-->` which is already blocked.

**Theoretical concern:** The regex uses `re.finditer` with the entire file content, and the `[^"]*?` is non-greedy. In degenerate cases with many `"` characters in the file, the regex engine could attempt many backtracking paths. However:
- The non-greedy `*?` minimizes backtracking
- The `[^"]` character class is a negated set, which is deterministic (no alternation)
- The overall regex has no nested quantifiers that would trigger catastrophic backtracking
- The file content is bounded by filesystem limits

**Assessment:** The regex is safe from ReDoS. The implicit protection from `[^"]*?` is a valuable secondary defense. No action needed.

---

## Recommendations

**Priority 1 (should implement):**

| # | Recommendation | Rationale | Effort |
|---|----------------|-----------|--------|
| R-01 | Add `<svg` and `</svg` to `_INJECTION_PATTERNS` | SVG is the most common XSS bypass vector after script/iframe. Closing the most probable bypass path. | Trivial -- add two alternation branches |
| R-02 | Add `on\w+\s*=` pattern to `_INJECTION_PATTERNS` | Event handler attributes (`onload=`, `onerror=`, etc.) are a primary XSS vector that bypasses tag-level blocking entirely. | Low -- add one alternation branch with `\b` word boundary |
| R-03 | Add test for `<!--` (opening comment delimiter) in content | Explicit coverage of both comment delimiter directions. | Trivial |

**Priority 2 (consider implementing):**

| # | Recommendation | Rationale | Effort |
|---|----------------|-----------|--------|
| R-04 | Add `<base` to `_INJECTION_PATTERNS` | Base tag can redirect relative URLs. Low probability but high impact if exploited in a rendering context. | Trivial |
| R-05 | Add test for `data:text/html` in mixed case (`DATA:TEXT/HTML`) | Confirms `re.IGNORECASE` works for multi-word patterns. | Trivial |
| R-06 | Add test for valid content containing an embedded injection pattern | e.g., `"Valid rule about <script> handling"` to confirm partial match detection. | Trivial |

**Priority 3 (optional hardening):**

| # | Recommendation | Rationale | Effort |
|---|----------------|-----------|--------|
| R-07 | Consider broadening `data:text/html` to `data:` with safe-type allowlist | Other `data:` MIME types (e.g., `data:image/svg+xml`) could carry payloads. However, this increases false positive risk if legitimate content references data URIs. | Low -- but requires false positive analysis |
| R-08 | Add `vbscript:` for completeness | Legacy vector. Minimal real-world risk but zero cost to add. | Trivial |

---

## Verdict

**Overall security posture: PASS with ADVISORY findings.**

The C-06 injection protection hardening is well-designed and correctly implemented. The three-layer defense (length check, pattern check, fail-open) provides adequate protection for the identified threat model. The logging implementation is secure. The test coverage is comprehensive for the currently blocked patterns.

The advisory findings (F-01, F-05, F-06) identify opportunities for incremental hardening, primarily adding `<svg` and event handler (`on\w+=`) patterns to close the most common secondary XSS vectors. These are not exploitable in the current deployment context (LLM prompt injection, not HTML rendering), but represent defense-in-depth improvements for potential future rendering contexts.

**Risk rating:** Low residual risk. The most probable attack path (injecting malicious markers via compromised rule files) is effectively mitigated. The identified gaps require both (a) an attacker with write access to rule files AND (b) a downstream rendering context that treats preamble content as HTML -- a combination that represents a significantly elevated threat level beyond the current design assumptions.

---

*Review performed: 2026-02-22*
*Agent: eng-security*
*Reviewed files: prompt_reinforcement_engine.py (v0.12.2), test_prompt_reinforcement_engine.py*
*Criticality: C2 (reversible in 1 day, focused scope, 2 files)*
