# Quality Score Report: ADR-001: Test Harness Baseline Persistence Strategy

## L0 Executive Summary

**Score:** 0.88/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Traceability (0.72)
**One-line assessment:** A well-structured ADR with strong decision logic and good completeness, but several external references cannot be verified in-document, evidence is partially asserted rather than cited, and actionability lacks concrete implementation timelines.

---

## Scoring Context

- **Deliverable:** `/Users/evorun/workspace/jerry/projects/PROJ-036-prompt-regression-harness/work/test-harness/validation-run/ps-architect-output.md`
- **Deliverable Type:** ADR (Architecture Decision Record)
- **Criticality Level:** C2 (Standard — a design decision for a new subsystem, reversible within one day, impacts a bounded adapter module)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Scored:** 2026-03-07T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.88 |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | No |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.92 | 0.184 | All standard ADR sections present; evaluation dimensions, weighted scoring, Steelman, revisit triggers, risks all included; minor gap: no retention policy specification or file naming schema |
| Internal Consistency | 0.20 | 0.93 | 0.186 | Claims mutually aligned throughout; weighted scores arithmetic is verified correct; force table and decision rationale match; one minor tension (Negative consequence says "no schema enforcement" but C-03 implies tamper detection via git hash — not contradictory but under-reconciled) |
| Methodological Rigor | 0.20 | 0.90 | 0.180 | Nygard ADR format followed; four weighted evaluation dimensions with explicit rationale; Steelman per S-003 applied and rebutted; decision explicitly references the highest-weight dimensions; minor gap: dimension weights assigned without derivation rationale |
| Evidence Quality | 0.15 | 0.78 | 0.117 | Latency estimates (0.5-2ms, 1-5ms) stated without benchmark source; Docker/NFS WAL corruption risk asserted without citation; concurrent access score of 3 for JSON is directionally correct but not sourced; tamper detection claim for git is well-founded; STRIDE threat model referenced but not quoted |
| Actionability | 0.15 | 0.85 | 0.128 | Clear decision stated; `baselines/{agent_name}/{commit_hash_short}.json` path scheme explicit; `os.rename()` atomic write specified; revisit triggers quantified (200 agents, >1 writer, >10s clone); no implementation timeline, PR or task reference for the adapter work |
| Traceability | 0.10 | 0.72 | 0.072 | C-01 through C-06 constraints list sources (H-05, System Design stream references, STRIDE model); but "System Design, Stream 1B", "System Design, Section 2.2", and "System Design, Security Decision #4" are references to documents not provided or linked; PROJ-035/decisions/ADR-001 listed but no path resolution; P-011 and YAGNI referenced inline without formal linkage |
| **TOTAL** | **1.00** | | **0.867** | |

---

## Composite Score Calculation

```
composite = 0.20 * Completeness
          + 0.20 * InternalConsistency
          + 0.20 * MethodologicalRigor
          + 0.15 * EvidenceQuality
          + 0.15 * Actionability
          + 0.10 * Traceability

composite = 0.20 * 0.92
          + 0.20 * 0.93
          + 0.20 * 0.90
          + 0.15 * 0.78
          + 0.15 * 0.85
          + 0.10 * 0.72

composite = 0.184
          + 0.186
          + 0.180
          + 0.117
          + 0.128
          + 0.072

composite = 0.867
```

**Rounded composite: 0.87**

---

## Detailed Dimension Analysis

### Completeness (0.92/1.00)

**Evidence:**
The ADR covers all standard Nygard sections: L0 executive summary, Status, Context, Constraints (6 entries), Forces, Options Evaluated (two options with per-dimension scoring tables and weighted totals), a comparative summary table, a Steelman section, Decision, Consequences (Positive/Negative/Neutral subsections), L2 Architectural Implications, Risks (3 entries with likelihood/impact/mitigation), and Related Decisions. The document includes future-evolution content (revisit triggers with quantified thresholds) and explicitly acknowledges the long-term path to SQLite and cloud persistence.

**Gaps:**
- The retention policy is mentioned (10 baselines per agent) in the Context section but is not formally specified as a system behavior or constraint. The mechanism for pruning old baselines ("Enforce retention policy in `store()`") is noted in the Risks table but not given a concrete file path or interface method reference.
- The file naming scheme `baselines/{agent_name}/{commit_hash_short}.json` is introduced in the Decision area but not formally specified with field definitions (e.g., how is `agent_name` derived — filename, display name, path-relative?).
- No mention of what happens to baselines when an agent file is renamed or deleted.

**Improvement Path:**
Add a "Specification" subsection under Decision that defines the path derivation algorithm, the retention policy enforcement point, and the agent-rename/delete edge case behavior.

---

### Internal Consistency (0.93/1.00)

**Evidence:**
The evaluation dimension weights sum to 1.00 (0.15 + 0.30 + 0.20 + 0.35 = 1.00 — verified). Option A weighted score arithmetic is correct: (8 × 0.15) + (9 × 0.30) + (3 × 0.20) + (10 × 0.35) = 1.20 + 2.70 + 0.60 + 3.50 = 8.00 — verified. Option B arithmetic: (7 × 0.15) + (5 × 0.30) + (8 × 0.20) + (5 × 0.35) = 1.05 + 1.50 + 1.60 + 1.75 = 5.90 — verified. The Decision section correctly cites corruption recovery (0.30) and operational simplicity (0.35) as the decisive dimensions, consistent with their weights and scores. The Steelman rebuttal argument ("bounded future migration cost") directly maps to the hexagonal architecture argument made in Context and L2. The Consequences section negative items match the low dimension scores assigned to Option A (concurrent access = 3 maps to "No concurrent write safety"; indexed queries = not a dimension but addressed correctly as a known negative).

**Gaps:**
Constraint C-03 states "Baseline integrity is enforced via git commit hash versioning" and Positive Consequence states "Threat T-23 (baseline tampering) is mitigated by git's built-in change tracking." The Negative Consequence "No schema enforcement at the storage layer" implicitly acknowledges a different integrity dimension. These are not contradictions, but the document does not clearly distinguish between tamper-detection integrity (addressed by git) and schema/format integrity (not addressed by git). A reader could conflate the two.

**Improvement Path:**
Add a brief clarification in the Consequences section distinguishing tamper-detection integrity (provided by git commit tracking per C-03) from schema validation integrity (provided by adapter code, not the storage engine). This resolves the implicit tension without changing the decision.

---

### Methodological Rigor (0.90/1.00)

**Evidence:**
The document applies Nygard ADR format with all required structural elements. It explicitly applies S-003 Steelman methodology (labeled as such: "Before dismissing Option B, its strongest case must be acknowledged (S-003)"). The Steelman is substantive — it identifies SQLite's strongest argument (ACID transactions, migration cost deferral, `PRAGMA integrity_check`) and rebutts it specifically with three named counter-points (speculative scaling, bounded migration via hexagonal port, YAGNI violation). Decision dimensions have explicit weights with rationale for each weight assignment. The L2 section provides structured long-term evolution analysis with three distinct evolution paths. Risks are enumerated with likelihood, impact, and mitigation columns.

**Gaps:**
The evaluation dimension weights are assigned with brief justification in the Rationale column, but the justification for specific weight values is informal. "Corruption recovery: 0.30 — Lost baselines force full re-baselining of affected agents; high-impact failure" explains why corruption matters but not why 0.30 specifically rather than 0.25 or 0.40. For a C2 ADR this is acceptable, but the weight assignment methodology is not formally documented.

**Improvement Path:**
Add a brief sentence to each dimension weight rationale explaining the relative weighting — e.g., "assigned 0.35 (highest) because operational simplicity is the binding constraint for a CI/CD-embedded tool with no operations team."

---

### Evidence Quality (0.78/1.00)

**Evidence (what is well-supported):**
- The `sqlite3` module shipping with Python's standard library is a verifiable fact.
- Git commit hash versioning providing tamper detection is well-established behavior.
- The constraint that Docker volume mounts (NFS, overlayfs) can cause WAL corruption is a known documented issue with SQLite.
- The 670KB maximum store size calculation (67 agents × 10 baselines × 1KB) is transparent and reproducible.

**Gaps (unsupported or asserted claims):**
- Write latency estimates ("approximately 0.5-2ms for a 1KB file"; "approximately 1-5ms per record") are stated without citing a benchmark, source, or test measurement. For a harness whose purpose is performance benchmarking, the absence of cited latency sources is notable.
- The concurrent access score of 3 for Option A is directionally correct but the rationale ("Concurrent writes to the same file produce undefined results") is asserted without citing POSIX filesystem semantics, Python documentation, or empirical test.
- "SQLite is the most widely deployed database engine in the world" is stated in the Steelman without citation (this is a well-known claim but is presented as evidence, not common knowledge).
- The STRIDE threat model is referenced as "System Design, STRIDE Threat Model" and threats T-23 through T-26 are cited, but none of the threat content is quoted or summarized — the reader cannot evaluate whether the threats were correctly characterized without accessing an external document that is not linked.
- P-011 is referenced inline as a governance principle motivating the ADR but is not defined in the document or linked to its source.

**Improvement Path:**
For the latency estimates: either run a micro-benchmark (appropriate given the testing context of this project) or cite a published SQLite performance reference. For the STRIDE threats: include at least a one-line summary of T-23 and T-25 in-document. For P-011: add a footnote or inline definition.

---

### Actionability (0.85/1.00)

**Evidence:**
- Decision is unambiguous: "Use JSON file store with git-indexed persistence."
- Implementation path is specified: file path template `baselines/{agent_name}/{commit_hash_short}.json`, adapter module `baselines/store.py`, port file `jerry/testing/baselines/ports.py`.
- Atomic write technique specified: write to temp file, then `os.rename()`.
- Post-write verification specified: "Verify JSON parseable after write."
- Revisit triggers are quantified with specific thresholds (>200 agents, >1 concurrent writer, any cross-agent aggregate query, >10s clone time increase).
- Port protocol methods named: `store()`, `retrieve()`, `retrieve_latest()`.

**Gaps:**
- No reference to a worktracker task, GitHub issue, or PR for implementing the adapter. For a C2 deliverable that is "PROPOSED" (not yet ACCEPTED), the next step in the governance workflow is unspecified.
- No mention of what tests should accompany the adapter (the document mentions `conftest.py` fixture and `tmp_path` in the L2 section, but does not specify what test cases are required).
- No timeline or milestone reference.

**Improvement Path:**
Add a "Next Steps" entry (or extend Related Decisions) with: (1) the worktracker entity ID tracking implementation, (2) minimum test cases for the adapter (happy path store/retrieve, corruption recovery, retention pruning), and (3) the acceptance criterion for changing status from PROPOSED to ACCEPTED.

---

### Traceability (0.72/1.00)

**Evidence:**
- Constraints C-01 through C-06 each cite a source (H-05, System Design Stream 1B, System Design Security Decision #4, System Design Section 2.2, H-07, System Design STRIDE Threat Model).
- Related Decisions lists PROJ-035/decisions/ADR-001 and PROJ-036 System Design as parent decisions.
- S-003 (Steelman) is explicitly labeled in the Steelman section.
- S-010 (self-review) is acknowledged in the footer.

**Gaps:**
- "System Design, Stream 1B," "System Design, Section 2.2," and "System Design, Security Decision #4" are cited repeatedly but no file path, URL, or worktracker ID is provided. A reviewer cannot navigate to these documents to verify the constraint sources.
- "PROJ-035/decisions/ADR-001-test-harness-architecture.md" is listed with a relative path that implies a sibling directory structure, but the path prefix `PROJ-035/` does not include `projects/` or a full repo-relative path. Navigability is ambiguous.
- P-011 is mentioned inline ("evidence-based rationale required by P-011") without a link or definition. P-011 appears to be a Jerry governance principle, but it is not defined in this document or linked to its source file.
- "YAGNI" is referenced as a design principle in the Steelman rebuttal without a citation or definition, which is minor but technically represents an uncited claim.
- The footer claims "Self-review (S-010) completed before output" but there is no self-review artifact or checklist in the document confirming what was checked.

**Improvement Path:**
(1) Replace "System Design, Stream 1B" references with the actual file path in the repository (e.g., `projects/PROJ-036-prompt-regression-harness/work/.../stream-1b-design.md`). (2) Add the full repo-relative path for PROJ-035 ADR. (3) Define P-011 inline or add a footnote linking to `.context/rules/quality-enforcement.md` or the relevant governance document.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Traceability | 0.72 | 0.88 | Replace "System Design, Stream 1B/Section 2.2/Security Decision #4" references with full repo-relative file paths. Add full path for PROJ-035 ADR. Define P-011 inline. |
| 2 | Evidence Quality | 0.78 | 0.90 | Add a micro-benchmark or cite a published source for the 0.5-2ms and 1-5ms latency estimates. Include a one-line summary of STRIDE threats T-23 and T-25 in-document. |
| 3 | Actionability | 0.85 | 0.93 | Add a "Next Steps" section specifying: (a) worktracker entity implementing the adapter, (b) minimum test cases required, (c) acceptance criterion for PROPOSED → ACCEPTED status transition. |
| 4 | Internal Consistency | 0.93 | 0.95 | Add a brief sentence distinguishing tamper-detection integrity (git-provided) from schema validation integrity (adapter-provided) to resolve the implicit tension between C-03 and the "No schema enforcement" negative consequence. |
| 5 | Completeness | 0.92 | 0.95 | Formally specify the `agent_name` derivation algorithm in the path scheme and address the agent-rename/delete edge case. |

---

## Leniency Bias Check

- [x] Each dimension scored independently before composite computed
- [x] Evidence documented for each score with specific artifact quotes/references
- [x] Uncertain scores resolved downward (Evidence Quality: chose 0.78 over 0.82 because latency claims are unverified assertions; Traceability: chose 0.72 over 0.78 because three external documents are referenced with no navigable paths)
- [x] First-draft calibration considered: this is a proposed ADR (status PROPOSED), consistent with first-draft calibration range 0.65-0.80 for weaker dimensions
- [x] No dimension scored above 0.95
- [x] Completeness scored 0.92 — artifact-specific evidence: all 11 document sections present with substantive content, 6 constraints enumerated, 4 weighted evaluation dimensions with full scoring tables, 3-column risks table, quantified revisit triggers; gap is minor (path derivation spec) not structural
- [x] Internal Consistency scored 0.93 — artifact-specific evidence: both weighted score calculations verified arithmetically correct; decision rationale explicitly cites the two highest-weighted dimensions; steelman rebuttal maps directly to hexagonal architecture argument established earlier
- [x] Methodological Rigor scored 0.90 — artifact-specific evidence: S-003 Steelman labeled and applied with substantive strongest-case argument followed by specific rebuttal; Nygard format followed throughout; dimension weights stated with brief but present justification; gap is weight derivation formality only
