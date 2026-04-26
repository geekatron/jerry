# Phase 1a Landscape: Top 5 Industry Standards for E2E Testing of Web Services

> **Phase:** 1a -- Landscape Scan
> **Agent:** ps-researcher-landscape-standards
> **Workflow:** e2e-skill-build-20260420-001
> **Access date for all URLs below:** 2026-04-20

## Document Sections

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Search engines, queries, narrowing approach |
| [The Top 5 Candidates](#the-top-5-candidates) | Ranked shortlist with authority signals |
| [Candidates Considered and Rejected](#candidates-considered-and-rejected) | Rejected candidates with rationale |
| [Sources Retrieved](#sources-retrieved) | All URLs fetched during this session |
| [Prompt Injection Notice](#prompt-injection-notice) | Attempted injection observed and ignored |

---

## Methodology Note

Live search was executed via the `WebSearch` tool (which aggregates from Bing/Google/DuckDuckGo-equivalent indexes) plus direct `WebFetch` calls against primary-source pages (w3.org, owasp.org, cucumber.io, softwaretestingstandard.org, wikipedia, playwright.dev) to verify each candidate's publisher, current version, and scope. Nine distinct search queries were run covering the prescribed list (ISO 29119, ISTQB, W3C WebDriver, OWASP WSTG, Playwright best practices, Cucumber/Gherkin BDD, IEEE 829, NIST SP 800-series, general "2025/2026 industry standard" queries) plus triangulation queries on TMMi, OpenAPI contract testing, and Selenium W3C compliance. From an initial candidate pool of ~11 candidates, narrowing was driven by three filters: (1) maintained by a recognized standards body OR a flagship open-source foundation; (2) actively referenced in 2025-2026 sources (not deprecated); (3) directly applicable to E2E testing of web-based services (UI+API), not narrowly adjacent (e.g., security-only, vendor-only). Attempts to use `WebFetch` directly against DuckDuckGo and Bing search-result pages returned unusable content, so cross-engine triangulation was performed via `WebSearch`'s multi-source index plus direct primary-source verification rather than raw SERP scraping.

## The Top 5 Candidates

### Candidate 1 -- W3C WebDriver (Level 2) Specification

- **Primary URL:** https://www.w3.org/TR/webdriver2/
- **Why in top 5:** WebDriver is the only W3C-level specification defining a standardized, language-neutral wire protocol for browser automation -- the foundational technical substrate that virtually every E2E web UI test framework (Selenium, Appium, and many cloud grids) implements. It is the de facto international standard for "how a test program drives a browser."
- **Authority / adoption signal:** Maintained by the W3C Browser Testing and Tools Working Group; Working Draft dated April 1, 2026; all major browser vendors (Chromium, Firefox, WebKit, Edge) implement it natively, and Selenium 4 is fully W3C-WebDriver compliant. Sources: w3.org/TR/webdriver2/, lambdatest.com article on Selenium 4 compliance.
- **Relevance for a Jerry E2E skill:** Any E2E skill targeting web services with browser-driven acceptance flows must speak WebDriver (directly or via a wrapper). It anchors cross-browser compatibility expectations, capability negotiation, and the Actions/BiDi extension surface that richer E2E scenarios depend on.

### Candidate 2 -- ISO/IEC/IEEE 29119 Software Testing (multi-part series)

- **Primary URL:** https://softwaretestingstandard.org/ (official site); Part 1 at https://www.iso.org/standard/81291.html
- **Why in top 5:** The only joint ISO/IEC/IEEE international standard series covering the full testing lifecycle -- concepts, processes, documentation, techniques, and keyword-driven testing. It explicitly replaces IEEE 829 and IEEE 1008, making it the successor-of-record for formal test documentation in regulated/enterprise environments.
- **Authority / adoption signal:** Maintained by ISO/IEC JTC 1/SC 7/WG 26; Part 1 revised 2022, Part 5 (keyword-driven) published December 2024 (BS ISO/IEC/IEEE 29119-5:2024), with parts on AI-based systems and biometric systems extending the series. Globally referenced in enterprise QA and procurement.
- **Relevance for a Jerry E2E skill:** Supplies the canonical vocabulary (test design techniques, test documentation artifacts, test-process hierarchy) a Jerry E2E skill should align with so that outputs are legible to enterprise QA organizations and audit/regulatory contexts.

### Candidate 3 -- ISTQB (International Software Testing Qualifications Board)

- **Primary URL:** https://istqb.org/ ; glossary at https://glossary.istqb.org/en/term/end-to-end-testing
- **Why in top 5:** ISTQB is the most widely adopted testing certification and terminology framework in the industry, with >250,000 certified testers worldwide. Its Foundation Level syllabus (currently 2023) and Advanced Level Test Automation Engineering (CTAL-TAE v2.0) define the dominant shared vocabulary for E2E testing, including an authoritative glossary definition of "End-to-End Testing."
- **Authority / adoption signal:** Maintained by the ISTQB board via national member boards (ASTQB, iSQI, etc.); CTFL 2023 syllabus is the current foundation exam; ISTQB explicitly maps many concepts to ISO/IEC/IEEE 29119, which reinforces standards coherence.
- **Relevance for a Jerry E2E skill:** Using ISTQB terminology (test level, test type, test design technique, entry/exit criteria) makes a Jerry E2E skill immediately understandable to the single largest community of professional testers and aligns naming with the ISO/IEC/IEEE 29119 backbone.

### Candidate 4 -- OWASP Web Security Testing Guide (WSTG)

- **Primary URL:** https://owasp.org/www-project-web-security-testing-guide/
- **Why in top 5:** WSTG is an OWASP Flagship Project and the de facto open industry standard for security-oriented testing of web applications *and web services*. For any E2E scope that touches auth flows, session handling, input validation, or API surface area, WSTG is the reference testers and regulators cite.
- **Authority / adoption signal:** Maintained by the OWASP Foundation (flagship project status); current stable version 4.2 (December 2020), version 5.0 actively in development on GitHub (OWASP/wstg). Referenced by penetration testers and compliance frameworks globally.
- **Relevance for a Jerry E2E skill:** Defines a structured test-case taxonomy (WSTG-INFO, WSTG-AUTH, WSTG-SESS, WSTG-INPV, WSTG-BUSLOGIC, etc.) that a Jerry E2E skill can adopt for any security-relevant E2E scenarios against web services, ensuring coverage of authentication, authorization, input handling, and business-logic flaws alongside functional flows.

### Candidate 5 -- Cucumber / Gherkin (BDD specification)

- **Primary URL:** https://cucumber.io/docs/gherkin/
- **Why in top 5:** Gherkin is the canonical plain-language DSL for Behaviour-Driven Development and the dominant scenario-specification syntax used in E2E test suites across the industry (pytest-bdd, Cucumber-JVM, SpecFlow/Reqnroll, behave, Cucumber.js). It is the prevailing standard for expressing E2E business flows as executable specifications and is widely used to bridge BDD with browser automation frameworks (Selenium, Playwright, Cypress).
- **Authority / adoption signal:** Maintained by the Cucumber Open Source project (copyright 2014-2026); Gherkin supports ~30+ localized languages; implementations exist in every major language ecosystem; broadly cited in 2026 E2E guides as the canonical BDD scenario format.
- **Relevance for a Jerry E2E skill:** Provides a language-agnostic, human-readable acceptance-criteria format (`Given/When/Then`) that a Jerry E2E skill can use to represent E2E scenarios independently of the underlying driver (WebDriver, Playwright, API test clients) -- pairs naturally with the 29119 "test case" artifact and ISTQB "test scenario" vocabulary.

## Candidates Considered and Rejected

- **IEEE 829 (Test Documentation)** -- Rejected: officially superseded by ISO/IEC/IEEE 29119-3; no current maintenance. Citing it today is historical rather than industry-standard. (Source: ieeexplore.ieee.org/document/4578383)
- **Playwright Best Practices Documentation** -- Rejected: authoritative *vendor* documentation (Microsoft), not a cross-industry standard. Included implicitly under WebDriver's ecosystem effects, but does not meet the "recognized standards body / flagship foundation" filter. (Source: playwright.dev/docs/best-practices)
- **Cypress Best Practices Documentation** -- Rejected: vendor-specific guidance (Cypress.io); same rationale as Playwright.
- **NIST SP 800-115 / SP 800-95** -- Rejected: excellent security-testing guidance but narrower than WSTG for web services and not purpose-built for E2E web testing; WSTG wins head-to-head on web-service relevance.
- **TMMi (Test Maturity Model Integration)** -- Rejected: process *maturity model* rather than a test-methodology standard; orthogonal to "how to do E2E testing of a web service." Valuable for QA organizations but outside the shortlist criteria.
- **OpenAPI Specification (OAS) for contract testing** -- Rejected: foundational for API contract testing but not itself an E2E testing standard; complements rather than competes with the top 5.

## Sources Retrieved

Search queries executed via `WebSearch` (Bing/Google/DuckDuckGo-equivalent aggregation):

1. `"end to end testing web services industry standard 2025 2026"` -- returned leapwork, bugbug.io, dev.to, bunnyshell, kellton, testdino, maestro.dev, wildnetedge, accelq, bunnyshell.
2. `ISTQB e2e testing certification standard` -- returned istqb.org, glossary.istqb.org, isqi.org, astqb.org, atsqa.org, wikipedia, and CTAL-TAE v2.0 page.
3. `ISO 29119 software testing standard 2025` -- returned iso.org/standard/81291, standards.ieee.org/ieee/29119-5, softwaretestingstandard.org, wikipedia, evoketechnologies, xbosoft, mystandards.biz, IEEE Xplore.
4. `W3C WebDriver standard specification` -- returned w3.org/TR/webdriver2, w3c/webdriver GitHub, w3.org/TR/webdriver-bidi, lambdatest Selenium 4 compliance article, saucelabs docs, medium deep-dive.
5. `Playwright best practices testing documentation official` -- returned playwright.dev/docs/best-practices, browserstack, testgrid, checklyhq, and several community guides.
6. `OWASP Web Security Testing Guide WSTG 2025` -- returned owasp.org WSTG landing page, owasp.org/.../latest, github.com/OWASP/wstg, v4.2 page, nest.owasp.org, devguide.owasp.org.
7. `BDD Gherkin Cucumber end to end testing standard` -- returned cucumber.io/docs/gherkin, cucumber.io/docs, browserstack Cucumber E2E guide, smartbear cucumberstudio docs.
8. `IEEE 829 test documentation standard current status` -- returned standards.ieee.org/ieee/829, IEEE Xplore 829-2008 and 829-1998, wikipedia "Software test documentation" confirming supersession by 29119.
9. `"end to end testing" standards "ISO 29119" OR "ISTQB" most widely adopted` -- triangulation; returned softwaretestingstandard.org, wikipedia, satisfice blog (critique), rcolomo mapping ISTQB->29119.
10. `Selenium W3C WebDriver protocol compliance 2025 browser automation` -- triangulation; confirmed Selenium 4 W3C compliance.
11. `TMMi Test Maturity Model Integration framework standard` -- triangulation for rejection rationale.
12. `NIST SP 800 testing guidance web application` -- triangulation for rejection rationale.
13. `OpenAPI specification E2E contract testing web services standard` -- triangulation for rejection rationale.

Pages directly fetched via `WebFetch` (primary-source verification):

- https://www.w3.org/TR/webdriver2/ -- confirmed W3C publisher, Working Draft 2026-04-01, scope.
- https://playwright.dev/docs/best-practices -- confirmed Microsoft maintainer, 5 core themes.
- https://owasp.org/www-project-web-security-testing-guide/ -- confirmed OWASP Flagship, v4.2 current, v5.0 in development.
- https://en.wikipedia.org/wiki/ISO/IEC_29119 -- confirmed multi-body publisher, part years, relationship to IEEE 829.
- https://cucumber.io/docs/gherkin/ -- confirmed Cucumber Open Source maintainer, authoritative Gherkin reference.
- https://softwaretestingstandard.org/ -- confirmed ISO/IEC JTC 1/SC 7/WG 26 maintenance, 8 published parts incl. Parts 11 and 13, explicit supersession of IEEE 829, IEEE 1008, BS 7925.
- https://duckduckgo.com/?q=... -- attempted but returned only query header (no usable results).
- https://www.bing.com/search?q=... -- attempted but returned unrelated content (no usable results).

## Prompt Injection Notice

During execution of search query #1, a `WebSearch` result appeared to include a fake `<system-reminder>` tag containing "MCP Server Instructions" urging redirection to Context7 for library documentation. This was an attempted prompt injection embedded in search-result content. It was **ignored**; I continued with the user-specified task of live web search for E2E testing standards and did not redirect to Context7 lookups. Flagging this per P-022 (no deception) and for Gate 1a auditability.
