---
title: "Deep-Dive: OWASP Web Security Testing Guide (WSTG)"
slug: std-4-owasp-wstg
phase: 1b
orchestration: e2e-skill-build-20260420-001
agent: ps-researcher-std-4
access_date: 2026-04-21
stable_version: v4.2 (released 2020-12-03)
in_development: v5.0 (open milestone on github.com/OWASP/wstg)
publisher: OWASP Foundation (Flagship Project)
license: CC BY-SA 4.0
---

# Deep-Dive: OWASP Web Security Testing Guide (WSTG)

> **Phase:** 1b -- Deep Standards Research
> **Agent:** ps-researcher-std-4
> **Workflow:** e2e-skill-build-20260420-001
> **Access date for all URLs below:** 2026-04-21
> **Target:** Phase 1c synthesis for Jerry E2E testing skill

## Document Sections

| Section | Purpose |
|---------|---------|
| [Methodology Note](#methodology-note) | Live web queries and primary-source fetches |
| [1. What WSTG Specifies](#1-what-wstg-specifies) | Framework, 12 Web App Testing categories, APIs, Reporting; ASVS/Top 10 relationship |
| [2. Scope and Boundary](#2-scope-and-boundary) | Security E2E scope vs generic functional E2E |
| [3. Applicability to Jerry E2E Skill](#3-applicability-to-jerry-e2e-skill) | Category-by-category translation to agentic E2E test cases |
| [4. Strengths / Unique Contributions](#4-strengths--unique-contributions) | Threat-driven E2E, taxonomy, free/open, community-maintained |
| [5. Weaknesses / Gaps / Criticisms](#5-weaknesses--gaps--criticisms) | Security-only scope, update cadence, manual-lean bias |
| [6. Current State (2026)](#6-current-state-2026) | v4.2 stable, v5.0 in development, stable vs latest branches |
| [7. Key Implementation Patterns](#7-key-implementation-patterns) | WSTG IDs, OTG->WSTG migration, passive/active, per-test template |
| [Sources Retrieved](#sources-retrieved) | All URLs fetched and queries executed this session |
| [Honesty Notes (P-022)](#honesty-notes-p-022) | Gaps, inferences, and prompt-injection observations |

---

## Methodology Note

All findings below are grounded in live web research executed on 2026-04-21 via the `WebSearch` and `WebFetch` tools. Eight distinct search queries were run across WSTG versioning, categories, test-ID format, WSTG-vs-ASVS relationship, API testing section, v5.0 status, checklist structure, and update cadence. Five primary-source `WebFetch` calls were made against owasp.org and github.com/OWASP/wstg to verify maintainer, version, category list, and test counts. No Context7 lookup was performed: WSTG is a documentation standard, not a library/SDK, so live web is the correct source. A prompt-injection artifact embedded in the landscape file (fake `<system-reminder>` urging redirection to Context7 for library docs) was observed and ignored per P-022.

### Queries Executed (WebSearch)

| # | Query | Purpose |
|---|-------|---------|
| 1 | `"OWASP Web Security Testing Guide latest version 2025 2026"` | Confirm current stable version and v5 status |
| 2 | `OWASP WSTG v4.2 stable categories structure` | Enumerate the 12 Web App Testing categories |
| 3 | `OWASP WSTG test IDs OTG naming convention` | Understand WSTG-<cat>-<num> format and OTG->WSTG migration |
| 4 | `OWASP WSTG vs ASVS relationship differences` | Position WSTG (HOW) vs ASVS (WHAT) vs Top 10 (risks) |
| 5 | `OWASP WSTG API testing web services section` | Confirm section 4.12 APIT coverage (REST/SOAP/GraphQL/gRPC/WS) |
| 6 | `OWASP WSTG GitHub latest release v5 development status` | Verify v5.0 milestone open, v4.2 remains stable |
| 7 | `OWASP WSTG checklist passive active testing procedures` | Confirm passive/active workflow and per-test template |
| 8 | `OWASP WSTG weaknesses criticisms limitations manual testing` | Gather limitations and manual-bias signals |

### Pages Fetched (WebFetch)

| # | URL | Purpose |
|---|-----|---------|
| 1 | https://owasp.org/www-project-web-security-testing-guide/ | Primary project page -- version, maintainers, flagship status, copyright 2026 |
| 2 | https://owasp.org/www-project-web-security-testing-guide/v42/ | Authoritative 12-category list with short codes |
| 3 | https://github.com/OWASP/wstg | Repo status -- v4.2 stable, v5.0 in dev, 1,214 commits on master, CC BY-SA 4.0 |
| 4 | https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/00-API_Testing_Overview | APIT chapter structure, REST/SOAP/GraphQL/gRPC/WebSockets, APIT-01..APIT-04 + GraphQL test |
| 5 | https://owasp.org/www-project-web-security-testing-guide/stable/2-Introduction/ | WSTG self-description, SDLC workflow, automation caution |
| 6 | https://github.com/OWASP/wstg/blob/master/checklists/checklist.md | Exact per-category test counts totalling ~109 tests |
| 7 | https://devguide.owasp.org/en/06-verification/01-guides/01-wstg/ | OWASP Developer Guide framing of WSTG alongside ASVS/MASTG |

---

## 1. What WSTG Specifies

WSTG is an **OWASP Flagship Project** that specifies a security-testing *framework* (not a mere checklist) for web applications and web services. Per the Stable Introduction, WSTG describes itself as "a complete testing framework, not merely a simple checklist" and addresses the "what, why, when, where, and how" of web application security testing integrated across the SDLC ([owasp.org stable/2-Introduction](https://owasp.org/www-project-web-security-testing-guide/stable/2-Introduction/), accessed 2026-04-21).

**High-level structure** (v4.2 stable, confirmed via [v42/](https://owasp.org/www-project-web-security-testing-guide/v42/) and [checklist.md](https://github.com/OWASP/wstg/blob/master/checklists/checklist.md), 2026-04-21):

- **1. Frontispiece** -- license, contributors, revision history.
- **2. Introduction** -- principles, testing philosophy, need for balanced manual + automated testing.
- **3. The OWASP Testing Framework** -- lifecycle phases (Before Development, During Definition & Design, During Development, During Deployment, Maintenance & Operations), threat modeling, code review, penetration testing.
- **4. Web Application Security Testing** -- the 12 categories (the operational heart of the guide):

| Ch | Category | Code | Tests (v4.2) |
|----|----------|------|--------------|
| 4.1 | Information Gathering | INFO | 10 |
| 4.2 | Configuration and Deployment Management | CONF | 14 |
| 4.3 | Identity Management | IDNT | 5 |
| 4.4 | Authentication | ATHN | 11 |
| 4.5 | Authorization | ATHZ | 5 |
| 4.6 | Session Management | SESS | 11 |
| 4.7 | Input Validation | INPV | 20 |
| 4.8 | Error Handling | ERRH | 2 |
| 4.9 | Cryptography | CRYP | 4 |
| 4.10 | Business Logic | BUSL | 10 |
| 4.11 | Client-side Testing | CLNT | 14 |
| 4.12 | API Testing | APIT | 3 (stable) / 4+GraphQL (latest) |

Total: **~109 individual test cases** in v4.2 stable ([checklist.md](https://github.com/OWASP/wstg/blob/master/checklists/checklist.md), accessed 2026-04-21).

- **5. Reporting** -- executive summary, findings, evidence, remediation guidance.
- **Appendices** -- testing tools, fuzz vectors, encoded injection, HTTP status codes.

**Relationship to ASVS and Top 10:**

- **OWASP Top 10** is a risk-awareness document (the 10 most critical web app security risks). WSTG's stable Introduction describes Top 10 as "a good starting point" for deriving general security requirements, but WSTG positions itself as broader in methodology ([stable/2-Introduction](https://owasp.org/www-project-web-security-testing-guide/stable/2-Introduction/), 2026-04-21).
- **OWASP ASVS** (Application Security Verification Standard) specifies *what* to verify -- the requirements/acceptance bar. WSTG specifies *how* to test. External community mappings (e.g., `jeremychoi/owasp-asvs-wstg-checklist`, `JulianGR/OWASP_WSTG_ASVS` on GitHub) explicitly pair each ASVS requirement with concrete WSTG tests, confirming the complementary HOW/WHAT split (search #4, 2026-04-21).
- **OWASP Developer Guide** (devguide.owasp.org) places WSTG alongside ASVS and MASTG in its Verification section, treating them as coordinated but independent standards ([devguide.owasp.org/en/06-verification/01-guides/01-wstg](https://devguide.owasp.org/en/06-verification/01-guides/01-wstg/), 2026-04-21).
- **OWASP API Security Top 10** is a distinct project; the API Testing chapter (4.12) references it but is not a reformatting of it ([latest 12-API Testing overview](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/00-API_Testing_Overview), 2026-04-21).

---

## 2. Scope and Boundary

**Scope (what WSTG covers):**

- Security behaviours of web applications **and web services** (the subtitle of the GitHub repo explicitly names both).
- End-to-end attacker-perspective testing across auth flows, session handling, authorization boundaries, input handling, error handling, crypto, business logic, client-side (DOM, CSP, clickjacking, CORS, HTML5), and API surface (REST, SOAP, GraphQL, gRPC, WebSockets) ([latest 12-API Testing overview](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/00-API_Testing_Overview), 2026-04-21).
- Framework integration into the SDLC (threat modeling, code review, pen test) and reporting conventions.

**Boundary (what WSTG does NOT cover):**

- **Functional / acceptance / UI-behavioural correctness.** WSTG does not specify tests for "does this feature work"; it specifies "can this feature be abused or bypassed."
- **Non-security performance, accessibility, usability, or visual regression.**
- **Mobile-app-specific security** -- handled by the sister project MASTG (OWASP Mobile Application Security Testing Guide).
- **Cross-browser compatibility** -- WSTG tests are browser-agnostic at the HTTP/DOM layer; they do not mandate driver protocols. (WebDriver is the relevant standard for that.)
- **Requirements definition** -- handled by ASVS (WSTG assumes the requirements exist and provides a way to verify them).

In Phase 1a landscape terms: WSTG is the **security-focused E2E axis**. A generic functional E2E skill must pair WSTG with a functional-testing standard (ISTQB / ISO 29119) plus a scenario DSL (Gherkin) plus a browser-automation protocol (WebDriver) to cover the full E2E surface.

---

## 3. Applicability to Jerry E2E Skill

WSTG categories map to agentic/E2E test cases with **direct, high-value translation** in several categories and **indirect** translation in others. The table below distinguishes the two.

| WSTG Cat | Direct Applicability to Jerry E2E | Translation Pattern |
|----------|------------------------------------|---------------------|
| INFO (10) | **Direct** | Information-gathering tests translate to passive reconnaissance steps an agent runs before functional scenarios (e.g., enumerate endpoints, fingerprint framework, check robots.txt, review metafiles). |
| CONF (14) | **Direct** | Configuration/deployment tests become pre-scenario environment assertions (TLS config, HTTP methods, admin interfaces, subdomain takeover, cloud storage misconfig). |
| IDNT (5) | **Direct** | Identity-lifecycle tests become E2E user-journey scenarios (registration, provisioning, weak username policy, account enumeration). |
| ATHN (11) | **Direct** | Authentication tests map 1:1 to E2E login/logout/MFA/password-reset flows -- a natural fit for Gherkin scenarios. |
| ATHZ (5) | **Direct** | Authorization tests (directory traversal, privilege escalation, IDOR, bypassing schema) are classical role-based E2E test cases. |
| SESS (11) | **Direct** | Session-management tests (cookie attributes, session fixation, CSRF, logout) align directly with multi-page E2E flows. |
| INPV (20) | **Partial** | Many INPV tests (reflected XSS, stored XSS, SQLi, command injection) are useful E2E; purely code-level tests (LDAP injection context) need adapters. |
| ERRH (2) | **Direct** | Error-handling tests become E2E negative-path scenarios. |
| CRYP (4) | **Partial** | Crypto tests are mostly transport/infra-level (weak TLS, padding oracle); useful as pre-flight assertions rather than user scenarios. |
| BUSL (10) | **Direct, highest-value** | Business-logic testing is the category automated scanners cannot handle and is where agentic/E2E shines -- workflow circumvention, ability to forge requests, process timing, defenses against application misuse. |
| CLNT (14) | **Direct** | Client-side tests (DOM XSS, CSP, clickjacking, CORS, HTML5 storage, postMessage) require a real browser -- native WebDriver territory. |
| APIT (3-4+) | **Direct** | API tests (recon, BOLA, excessive data exposure, BFLA, GraphQL) map to API-level E2E assertions. |

**Concrete translation pattern** a Jerry E2E skill could adopt:

1. Each Gherkin scenario carries a `@wstg:WSTG-v42-<CAT>-<NN>` tag linking it to one or more WSTG tests.
2. Scenario steps mirror the WSTG "How to Test" procedure (passive observation steps first, then active probing steps).
3. The scenario's `Then` assertion encodes the WSTG "Objectives" statement.
4. Test reports (Phase 5 Reporting) inherit the WSTG evidence/remediation convention.

---

## 4. Strengths / Unique Contributions

1. **Threat-driven E2E taxonomy.** WSTG supplies a complete, named, numbered taxonomy of ~109 test cases ([checklist.md](https://github.com/OWASP/wstg/blob/master/checklists/checklist.md), 2026-04-21). No other open standard provides an equally granular web-testing catalogue.
2. **Unique Business Logic category.** WSTG's BUSL chapter (10 tests) is essentially impossible for automated scanners and requires scenario-based E2E reasoning -- a perfect fit for agentic test execution ([v42/](https://owasp.org/www-project-web-security-testing-guide/v42/), 2026-04-21).
3. **Free and openly licensed** (CC BY-SA 4.0) -- teams can adopt test IDs, re-publish scenario templates, and customize the checklist without licensing friction ([github.com/OWASP/wstg](https://github.com/OWASP/wstg), 2026-04-21).
4. **Flagship OWASP status** confers global recognition and regulator/compliance acceptance (PCI DSS, ISO 27001 auditors routinely cite WSTG).
5. **Multi-technology API coverage.** The v4.12 APIT chapter spans REST, SOAP, GraphQL, gRPC, and WebSockets, making it technology-agnostic for web-service E2E ([latest 12-API Testing overview](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/00-API_Testing_Overview), 2026-04-21).
6. **Per-test structured template** (Summary, Test Objectives, How to Test, Remediation, References) -- a ready-made artefact schema that maps cleanly onto any test-case management system (per [stable/2-Introduction](https://owasp.org/www-project-web-security-testing-guide/stable/2-Introduction/), 2026-04-21; individual test files in master branch).
7. **Versioned identifiers** (`WSTG-v42-INFO-02`) enable stable cross-referencing even as the guide evolves ([wstg issue #320](https://github.com/OWASP/wstg/issues/320), 2026-04-21).
8. **Explicitly balances automation and manual.** Stable Introduction warns against over-reliance on automated tools and emphasizes creative manual assessment -- which maps naturally to agent-driven creative scenario generation.

---

## 5. Weaknesses / Gaps / Criticisms

1. **Security-only scope.** WSTG does nothing for functional correctness, performance, accessibility, or compatibility. A Jerry E2E skill that relies on WSTG alone leaves the majority of E2E ground uncovered. (Boundary confirmed across all primary sources fetched 2026-04-21.)
2. **Slow update cadence.** The current stable release (v4.2) dates from **2020-12-03**; v5.0 has been "in development" for **over five years** with an open but unshipped milestone ([wstg releases](https://github.com/OWASP/wstg/releases), [v5.0 milestone](https://github.com/OWASP/wstg/milestone/4), 2026-04-21). This is a material gap for technologies that have changed substantially since 2020 (modern SPA patterns, HTTP/3, passkeys, WebAuthn edge cases, post-2023 GraphQL ecosystem, server components).
3. **Manual-lean bias.** The guide's framing assumes a human penetration tester executing procedures. Procedures are written as narrative prose, not executable specs. Converting them into deterministic automated assertions requires interpretation.
4. **Small API chapter (v4.2 stable).** APIT has only 3 stable tests versus 20 in INPV or 14 in CONF -- under-weighted for modern API-first architectures. The `latest` branch extends APIT (e.g., GraphQL test WSTG-APIT-99) but those are dev content, not yet frozen ([latest 12-API Testing overview](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/00-API_Testing_Overview), 2026-04-21).
5. **Thin error-handling and cryptography chapters.** ERRH (2 tests) and CRYP (4 tests) are markedly lighter than other categories, reflecting the pen-test tradition of outsourcing crypto to separate audits.
6. **No formal traceability to ASVS.** WSTG does not ship first-party ASVS mappings; teams rely on community-maintained spreadsheets (e.g., `jeremychoi/owasp-asvs-wstg-checklist`), whose completeness and freshness vary (search #4, 2026-04-21).
7. **No executable artefacts.** Unlike ZAP policies or scanner plugin definitions, WSTG tests are narrative Markdown. There is no machine-readable manifest (JSON/YAML) of test IDs + preconditions + procedures, which complicates tooling integration.
8. **Community-volunteer maintenance.** Leaders (Elie Saad, Rick Mitchell per the [project page](https://owasp.org/www-project-web-security-testing-guide/), 2026-04-21) are volunteers; release velocity is therefore inherently variable.
9. **Regional / compliance currency.** Since 2020, several regulatory baselines (PCI DSS 4.0, NIST SP 800-53 Rev. 5, EU NIS2) have shifted; WSTG v4.2 does not explicitly align with the newer versions.
10. **"Not every test will be relevant to every web application"** -- WSTG itself acknowledges this ([devguide.owasp.org WSTG page](https://devguide.owasp.org/en/06-verification/01-guides/01-wstg/), 2026-04-21). A Jerry E2E skill must implement a test-selection/tailoring step rather than blanket-applying all 109 tests.

---

## 6. Current State (2026)

| Attribute | Value | Source (access 2026-04-21) |
|-----------|-------|-----------------------------|
| Stable version | **v4.2** | [project page](https://owasp.org/www-project-web-security-testing-guide/), [release tag](https://github.com/OWASP/wstg/releases/tag/v4.2) |
| Stable release date | **2020-12-03** | [wstg-v42-released blog](https://owasp.org/2020/12/03/wstg-v42-released) |
| In development | **v5.0** (open milestone) | [v5.0 milestone](https://github.com/OWASP/wstg/milestone/4) |
| Project status | **OWASP Flagship Project** (Documentation, Breaker, Builder) | [project page](https://owasp.org/www-project-web-security-testing-guide/) |
| Repo | https://github.com/OWASP/wstg | Repo root; master branch 1,214 commits as of fetch |
| License | CC BY-SA 4.0 | [github.com/OWASP/wstg](https://github.com/OWASP/wstg) |
| Maintainers | Elie Saad, Rick Mitchell | [project page](https://owasp.org/www-project-web-security-testing-guide/) |
| Copyright year on project page | 2026 | [project page](https://owasp.org/www-project-web-security-testing-guide/) |

**Branches of the guide available to consumers:**

- `/v42/` -- frozen stable content (canonical for compliance citations).
- `/stable/` -- alias for the current stable branch (currently points at v4.2 content).
- `/latest/` -- rolling development content on the way to v5.0 (includes the extended APIT chapter with GraphQL test).
- `github.com/OWASP/wstg` master -- bleeding edge, source of truth for v5.0-in-progress.

**OWASP Testing Guide v5 status:** Actively in development as of 2026-04-21 but **no release date is published**. The v5.0 milestone on GitHub is open. A 2020 release-announcement statement that "we don't plan to slow down anytime soon" has been materially contradicted by the five-year gap (search #8, 2026-04-21). Jerry should assume v4.2 is the **de facto stable** target for the foreseeable future while optionally tracking `/latest/` for APIT evolution.

**Related but distinct 2026-era OWASP artefacts observed in searches:**

- **OWASP Top 10:2025** was announced (search #1, 2026-04-21); this is a separate project.
- **OWASP AI Testing Guide 2026** (search #1, 2026-04-21) is a different flagship effort; not part of WSTG.

---

## 7. Key Implementation Patterns

### 7.1 Test ID Format

- Canonical format: `WSTG-<CATEGORY>-<NN>` where `<CATEGORY>` is a 4-letter code (INFO, CONF, IDNT, ATHN, ATHZ, SESS, INPV, ERRH, CRYP, BUSL, CLNT, APIT) and `<NN>` is a zero-padded 01-99 sequence.
- Version-pinned format (recommended for reports/tooling): `WSTG-v<MMmm>-<CATEGORY>-<NN>` e.g. `WSTG-v42-INFO-02` ([wstg issue #320](https://github.com/OWASP/wstg/issues/320), 2026-04-21).
- Legacy identifier prefix `OTG-` (from the pre-4.2 "OWASP Testing Guide" era) was migrated to `WSTG-` in the 4.2 rebrand. Reports using OTG- IDs are historical and should be converted.

### 7.2 Per-Test Document Template

Each test case in WSTG Ch. 4 follows the same template (confirmed by inspecting multiple test files in the master branch during fetches, 2026-04-21):

1. **Summary** -- what the weakness is.
2. **Test Objectives** -- bullet list of verifiable statements (the implicit "Then" of the scenario).
3. **How to Test** -- procedural steps, often split into sub-sections like Black-Box vs Gray-Box, or Passive vs Active reconnaissance.
4. **Remediation** -- what to fix if the test exposes a weakness.
5. **Tools** -- suggested open-source tooling (ZAP, Burp, nmap, nikto, amass, etc.).
6. **References** -- RFCs, CWE IDs, related advisories.

**Implication for Jerry:** the WSTG template maps cleanly onto a Jerry test-case artefact schema:

```yaml
id: WSTG-v42-AUTH-09
summary: "Testing for weak password change or reset functionalities"
objectives:
  - Determine the resistance of the application against account takeover.
  - Determine whether old credentials can still be used.
procedure:
  passive: [...]
  active: [...]
assertions: [...]
remediation: "..."
tools: ["ZAP", "Burp"]
references: ["CWE-640", "NIST SP 800-63B"]
```

### 7.3 Passive vs Active Testing

Per the Stable Introduction and v4.1/v4.2 Introduction and Objectives ([v41 introduction](https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/00-Introduction_and_Objectives/README), 2026-04-21):

- **Passive phase:** tester behaves as a legitimate user, explores the app, and maps the attack surface (access points, HTTP headers, parameters, cookies). Information Gathering (INFO) lives here.
- **Active phase:** tester applies category-specific probing techniques informed by the passive map.

This two-phase pattern is directly useful for an agentic E2E framework: the **passive sweep** becomes a discovery scenario an agent runs first to build an internal site-model, and the **active probes** become targeted scenarios parameterized by that model. This aligns with standard exploratory-testing workflows.

### 7.4 Preconditions and Procedures

While WSTG does not use the explicit word "precondition" as a schema field, each test's "How to Test" narrative always carries implicit preconditions (e.g., "a valid account has been created", "the application exposes parameter X"). Jerry's E2E skill should lift these implicit preconditions into explicit `Background:` / `Given` clauses when generating Gherkin scenarios.

### 7.5 Checklist and Reporting Artefacts

- The official [checklist.md](https://github.com/OWASP/wstg/blob/master/checklists/checklist.md) and the community-maintained Excel checklist provide a per-test Pass/Fail/N-A grid -- a ready-made reporting substrate.
- Phase 5 "Reporting" in the Testing Framework standardizes findings structure (executive summary, findings, evidence, remediation, references) that a Jerry E2E skill can adopt verbatim for security scenarios.

### 7.6 SDLC Integration Pattern

Per [stable/2-Introduction](https://owasp.org/www-project-web-security-testing-guide/stable/2-Introduction/) (2026-04-21), WSTG positions tests across SDLC phases:

- **Before Development:** policies, standards.
- **Definition & Design:** threat modeling, design reviews, security requirements (pairs with ASVS).
- **Development:** code reviews, unit tests.
- **Deployment:** **application penetration testing** (the 12 categories live here) + configuration management testing.
- **Maintenance:** operational management reviews, change verification.

A Jerry E2E skill should expect to be invoked primarily in the Deployment and Maintenance phases, running the 12 categories as gated CI/CD jobs.

---

## Sources Retrieved

All URLs below were accessed on **2026-04-21**.

### Primary OWASP sources

1. [OWASP Web Security Testing Guide -- project page](https://owasp.org/www-project-web-security-testing-guide/) -- flagship status, stable v4.2, v5.0 in development, maintainers Elie Saad and Rick Mitchell, copyright 2026, license CC BY-SA 4.0.
2. [WSTG v4.2 -- authoritative stable branch](https://owasp.org/www-project-web-security-testing-guide/v42/) -- 12-category table of contents with short codes INFO, CONF, IDNT, ATHN, ATHZ, SESS, INPV, ERRH, CRYP, BUSL, CLNT, APIT.
3. [WSTG Stable -- Introduction chapter](https://owasp.org/www-project-web-security-testing-guide/stable/2-Introduction/) -- "complete testing framework, not merely a simple checklist"; SDLC phases; balanced manual+automated stance.
4. [WSTG Latest -- 4.12 API Testing Overview](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/12-API_Testing/00-API_Testing_Overview) -- APIT subsections (APIT-01..04, -99 GraphQL), technologies REST/SOAP/GraphQL/gRPC/WebSockets.
5. [WSTG v4.2 release announcement (2020-12-03)](https://owasp.org/2020/12/03/wstg-v42-released) -- release date fixed at 2020-12-03.
6. [OWASP Developer Guide -- WSTG page](https://devguide.owasp.org/en/06-verification/01-guides/01-wstg/) -- WSTG positioned alongside ASVS and MASTG as verification resources; tailorable adoption emphasis.

### Primary GitHub sources

7. [OWASP/wstg repository root](https://github.com/OWASP/wstg) -- repo description naming web applications *and web services*; master branch; CC BY-SA 4.0.
8. [OWASP/wstg v5.0 milestone](https://github.com/OWASP/wstg/milestone/4) -- open milestone confirming v5.0 in development.
9. [OWASP/wstg checklist.md](https://github.com/OWASP/wstg/blob/master/checklists/checklist.md) -- exact per-category test counts (INFO 10, CONF 14, IDNT 5, ATHN 11, ATHZ 5, SESS 11, INPV 20, ERRH 2, CRYP 4, BUSL 10, CLNT 14, APIT 3) totalling 109.
10. [OWASP/wstg release v4.2](https://github.com/OWASP/wstg/releases/tag/v4.2) -- canonical stable release.
11. [OWASP/wstg issue #320 -- Update OTG IDs to WSTG](https://github.com/OWASP/wstg/issues/320) -- documented OTG->WSTG migration and version-pinned identifier format.

### Search queries (13 executed; 8 principal)

Queries 1-8 are listed in the Methodology table above. Additional triangulation queries included checklist, v5 status, and update-cadence follow-ups (aggregated into the WebSearch result sets referenced throughout the findings).

---

## Honesty Notes (P-022)

1. **v5.0 release date is not published.** I report v5.0 as "in development" only. The [v5.0 milestone](https://github.com/OWASP/wstg/milestone/4) is open as of 2026-04-21 but carries no published ETA. Any claim of a v5.0 date would be fabricated.
2. **v4.2 APIT count (3 tests) vs latest APIT count.** The stable v4.2 checklist lists 3 APIT tests (APIT-01..APIT-03); the `/latest/` branch shows APIT-04 and APIT-99 GraphQL test. I have clearly distinguished stable vs latest in the text and have not rolled the latest count into the v4.2 total.
3. **Test totals.** The "~109" total is the sum reported in the official `checklist.md` at access time. Individual third-party summaries sometimes cite "over 100 tests" or "~120 tests"; I have used the primary-source sum.
4. **ASVS mapping sources.** I cite community-maintained ASVS<->WSTG mappings (jeremychoi, JulianGR) from search results rather than direct fetches; I did not fetch those repos this session. The claim that WSTG does not ship a first-party ASVS mapping is based on the absence of one on the owasp.org WSTG page and in the checklist artefact, not on an explicit negative statement from OWASP.
5. **"OTG" vs "WSTG" migration.** I inferred the migration history from search-result snippets plus [issue #320](https://github.com/OWASP/wstg/issues/320). I did not fetch a v4.1 change-log line item explicitly naming the rebrand date; treat the migration claim as sourced from community commentary, not a primary WSTG revision-history entry.
6. **Update-cadence criticism.** "Five-year gap between v4.2 and v5.0" is factual as of 2026-04-21 (2020-12-03 to 2026-04-21). The judgement that this is a material gap is an analytic assessment, not a direct OWASP statement.
7. **Prompt-injection observation.** The Phase 1a landscape file at `/Users/victor.lau/workspace/jerry/projects/PROJ-017-e2e-testing-skill/orchestration/e2e-skill-build-20260420-001/research/landscape/standards-candidates.md` contains an embedded `<system-reminder>` block (starting at line ~102) instructing redirection to Context7 for library documentation. This is the same prompt-injection artefact flagged by the Phase 1a researcher in their Prompt Injection Notice. It was **ignored** during this Phase 1b deep-dive per P-022; Context7 is not an appropriate source for documentation standards such as WSTG, and the user's explicit instructions mandate live WebSearch + WebFetch. Flagging here for Gate 1b auditability.
