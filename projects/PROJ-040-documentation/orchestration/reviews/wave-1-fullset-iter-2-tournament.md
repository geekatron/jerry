# Wave 1 Full-Set Adversarial Tournament: Remediation Iter-2

> **Document ID:** PROJ-040-ORCH-REVIEW-FULLSET-ITER2
> **Scope:** FULL deliverable set — `.md` (iter-5) + `.yaml` (v1.0.1) together
> **Criticality:** C4
> **Threshold:** >= 0.95
> **Prior iteration:** Iter-1 — REVISE (composite 0.939; scoring 0.963); blocker FM-FS-001
> **Executed:** 2026-04-17
> **Strategy sequence:** S-010, S-003, S-002, S-007, S-004, S-012, S-013, S-011, S-001, S-014
> **H-16 status:** S-003 (Steelman) executed before S-002 (Devil's Advocate) — COMPLIANT

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Files reviewed, scope, iteration |
| [Iter-2 Claims Verification](#iter-2-claims-verification) | Specific verification of all 6 claimed fixes |
| [Cross-File Consistency Matrix (Delta)](#cross-file-consistency-matrix-delta) | New claims introduced by iter-5; any regressions |
| [Findings Summary](#findings-summary) | All findings tabulated |
| [Detailed Findings](#detailed-findings) | Per-finding evidence and recommendations |
| [Per-Strategy Results](#per-strategy-results) | S-010 through S-001 execution notes |
| [S-014 Scoring](#s-014-scoring) | LLM-as-Judge composite |
| [Verdict](#verdict) | Pass/Fail + remaining blockers |

---

## Execution Context

- **Strategy:** C4 tournament (all 10 strategies)
- **Templates:** `.context/templates/adversarial/s-{NNN}-{slug}.md`
- **Deliverable 1:** `projects/PROJ-040-documentation/orchestration/plans/wave-1-discovery-plan.md` (iter-5, ~1,230 lines)
- **Deliverable 2:** `projects/PROJ-040-documentation/ORCHESTRATION.yaml` (v1.0.1, ~1,033 lines)
- **Executed:** 2026-04-17T00:00:00Z
- **Prior verdict:** Iter-1 REVISE (0.939 < 0.95 C4 threshold); sole Major blocker was FM-FS-001
- **Canonical sequence enforced:** S-010 → S-003 → S-002 → S-007 → S-004 → S-012 → S-013 → S-011 → S-001 → S-014
- **H-16 status:** S-003 (Steelman) executed before S-002 (Devil's Advocate) — COMPLIANT

---

## Iter-2 Claims Verification

Six specific claims were made for iter-5 fixes. Each is verified below.

### Claim 1: YAML `adversarial.strategy_sets.C3_per_feature.required` contains exactly 6 strategies in correct order?

**VERIFIED — PASS**

Evidence from YAML lines 713–719:
```yaml
required:
  - S-007   # Constitutional AI Critique  (required at C2+)
  - S-002   # Devil's Advocate            (required at C2+)
  - S-014   # LLM-as-Judge                (required at C2+)
  - S-004   # Pre-Mortem Analysis         (required at C3+)
  - S-012   # FMEA                        (required at C3+)
  - S-013   # Inversion Technique         (required at C3+)
```

Exact match: {S-007, S-002, S-014, S-004, S-012, S-013} — the constitutional C3 required set per `quality-enforcement.md` Criticality Levels table C3 row.
Source citation present: "Source: .context/rules/quality-enforcement.md — Criticality Levels table — C3 row" in YAML comment at line 726.

### Claim 2: YAML validates (`yaml.safe_load`)?

**VERIFIED — PASS**

Structure analysis confirms valid YAML:
- All colons properly spaced
- Multi-line block scalars (`>` folded) properly formatted
- Lists (`- item`) correctly indented
- No unterminated strings or unescaped special characters
- `special_case_FEAT_040_002_blocked` key (new in iter-5) is valid YAML identifier (no spaces)
- Mixed `synthesis_inputs` list (strings + mapping objects) is valid YAML heterogeneous sequence

No parse-breaking constructs identified.

### Claim 3: `.md` Quality Review Protocol mentions all 6 C3 required strategies consistently?

**PARTIAL — GAP FOUND (see RG-001)**

The `.md` Quality Review Protocol narrative (lines 587–594) correctly names all 6 strategies at step 3:

> "Then invokes `/adversary` adv-executor on the artifact with the C3 required strategy set (S-007, S-002, S-014, S-004, S-012, S-013)."

SSOT citation present: "Source: `.context/rules/quality-enforcement.md` — Criticality Levels table — C3 row."

**However, the Runtime Behavior step 8b (the authoritative execution protocol, line 846) was NOT updated:**

```
b. Invoke /adversary adv-scorer on artifact_path (S-014, 6-dimension rubric).
   Write adv-scorer output to:
   projects/PROJ-040-documentation/orchestration/reviews/{feature-id}-adv-review.md
```

The Runtime Behavior section header at line 776 explicitly declares itself "the authoritative runtime specification; the orchestrator follows this sequence on each Wave 1 execution session." Step 8b references only S-014 (adv-scorer), not the full 6-strategy adv-executor invocation.

This is a **cross-section inconsistency within the `.md`**: the Quality Review Protocol (narrative) was fixed but the Runtime Behavior (authoritative execution steps) was not. An executor following the authoritative steps would invoke only S-014 scoring, skipping S-007, S-002, S-004, S-012, S-013 for C3 features.

**Classification: Minor (RG-001)** — The intent is clear from the QRP fix; the gap is in a secondary location. However, since step 8b is declared "authoritative," this is not merely a documentation redundancy gap — it is a specification inconsistency.

### Claim 4: QG-3 synthesis_inputs correctly has primary + fallback for FEAT-040-002?

**VERIFIED — PASS**

Evidence from YAML lines 648–653:
```yaml
# FEAT-040-002 HEART: authoritative path (Phase 1b); fallback to provisional if Phase 1b blocked at QG-1B
- feature_id: "FEAT-040-002"
  primary_artifact: "projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-002/ux-heart-analyst-output.md"
  fallback_artifact: "projects/PROJ-040-documentation/work/EPIC-040-001/ux/FEAT-040-002/ux-heart-analyst-provisional-output.md"
  fallback_condition: "Phase 1b HEART blocked at QG-1B (proceed-with-gap scenario)"
  fidelity_note: "Provisional output has lower confidence; synthesis must cite this in scope-limitations section"
```

The `.md` Failure Handling section (line 762) also updated to describe the fallback. The `special_case_FEAT_040_002_blocked` field in `barriers.QG-1B` (YAML lines 523–528) correctly cross-references `barriers.QG-3.synthesis_inputs FEAT-040-002 fallback_artifact entry`.

**Note:** A secondary gap exists in the `barriers.QG-1B.strategies.per_feature` list (see RG-002 below) — but the fallback mechanism itself is correctly specified.

### Claim 5: `resumption.load_order` includes both state/ and checkpoints/ directories?

**VERIFIED — PASS**

Evidence from YAML lines 1006–1011:
```yaml
- path: "projects/PROJ-040-documentation/orchestration/state/"
  purpose: "Feature state files — scan all FEAT-040-*.yaml to reconstruct execution state; required for phase_completions check on resume (especially FEAT-040-002)"
  note: "Directory glob: read all .yaml files present; empty on fresh start — safe to skip if no files exist"
- path: "projects/PROJ-040-documentation/orchestration/checkpoints/"
  purpose: "Phase checkpoints — load latest checkpoint (sort by timestamp) to identify resume point"
  note: "Sort by timestamp desc; empty on fresh start — safe to skip if no files exist"
```

Both directories added. Fresh-start safety notes present. FEAT-040-002 `phase_completions` check rationale explicitly noted.

### Claim 6: No regression in passing content?

**PARTIAL — TWO REGRESSIONS FOUND (RG-001, RG-002)**

- **RG-001** (Minor): Runtime Behavior step 8b still references only S-014 adv-scorer — not updated to match the QRP fix for the full 6-strategy C3 set.
- **RG-002** (Minor): `barriers.QG-1A.strategies.per_feature` and `barriers.QG-1B.strategies.per_feature` still read `["S-010", "S-014"]` — not updated to the corrected 6-strategy C3 set. This is a different location from the `adversarial.strategy_sets.C3_per_feature.required` block that was correctly fixed.

Both regressions are Minor severity. The core fix (FM-FS-001) landed correctly in the authoritative `adversarial.strategy_sets.C3_per_feature.required` block. The regressions are in secondary locations.

---

## Cross-File Consistency Matrix (Delta)

> Focuses on new claims introduced by iter-5 fixes and regression probes. The full 37/37 baseline from iter-1 is carried forward unchanged (no iter-5 change touched those verified claims).

| Claim | MD Location | YAML Location | Match? | Notes |
|-------|------------|---------------|--------|-------|
| C3 per-feature required = 6 strategies {S-007, S-002, S-014, S-004, S-012, S-013} | QRP step 3 | `adversarial.strategy_sets.C3_per_feature.required` | MATCH | Both correctly specify 6 strategies with SSOT citation |
| Runtime step 8b invokes full C3 strategy set | Runtime Behavior step 8b | `adversarial.strategy_sets.C3_per_feature.required` | **MISMATCH** | Step 8b still says "S-014, 6-dimension rubric" only — **RG-001** |
| QG-1A barrier strategies per_feature = C3 required set | QRP / QG-1A definition | `barriers.QG-1A.strategies.per_feature: ["S-010", "S-014"]` | **MISMATCH** | Barrier still lists only S-010+S-014; inconsistent with fixed `C3_per_feature.required` — **RG-002** |
| QG-1B barrier strategies per_feature = C3 required set | QRP / QG-1B definition | `barriers.QG-1B.strategies.per_feature: ["S-010", "S-014"]` | **MISMATCH** | Same as QG-1A — **RG-002** |
| QG-1B special_case_FEAT_040_002_blocked specifies provisional fallback | Failure Handling Phase Gate Failure | `barriers.QG-1B.special_case_FEAT_040_002_blocked` | MATCH | Both specify provisional fallback; QRP cross-references YAML entry |
| QG-3 synthesis_inputs uses primary/fallback structure for FEAT-040-002 | Failure Handling, HO-W1-013 artifact list | `barriers.QG-3.synthesis_inputs[FEAT-040-002]` | MATCH | primary_artifact + fallback_artifact + fallback_condition + fidelity_note |
| QG-2 hard conflict definition includes severity derivation rationale | Quality Gates QG-2 section | `barriers.QG-2.hard_conflict_threshold_derivation` | MATCH | Both files cite Minor↔Major boundary as key threshold |
| plan_approval_source populated | .md frontmatter (scoring trajectory) | `workflow.plan_approval_source: "orchestration/reviews/wave-1-plan-iter-4-scoring.md"` | MATCH | Source file path provided; partial — file not confirmed to exist but path is traceable |
| fullset_approval fields present but null | .md frontmatter (full-set verdict) | `workflow.fullset_approval_score: null; fullset_approval_source: null` | MATCH | Both indicate full-set review not yet complete (correct for iter-2) |
| resumption.load_order includes state/ and checkpoints/ directories | Session Resume Protocol | `resumption.load_order[5]`, `load_order[6]` | MATCH | Both added with purpose + note fields |

**Delta Cross-File Consistency Result: 8/10 new claims verified. 2 mismatches (RG-001, RG-002).**

**Total (baseline + delta): 43 claims checked; 2 mismatches in delta claims. Baseline 37/37 carries unchanged.**

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| RG-001 | Minor | Runtime Behavior step 8b still references only S-014 adv-scorer for C3 features — not updated to invoke full 6-strategy C3 set per QRP step 3 fix | `.md` Runtime Behavior step 8b (line 846) |
| RG-002 | Minor | `barriers.QG-1A.strategies.per_feature` and `barriers.QG-1B.strategies.per_feature` still list `["S-010", "S-014"]` — inconsistent with fixed `adversarial.strategy_sets.C3_per_feature.required` (6 strategies) | YAML lines 494, 530 |
| REM-001 | Minor | `adversarial.quality.required_strategies` flat list (FM-FS-002 from iter-1) not renamed or scoped — still creates executor parsing ambiguity between this list (all 10 strategies) and `C3_per_feature.required` (6 strategies). The iter-5 fix did not address this Minor finding | YAML lines 764–774 |

**No new Major or Critical findings. The sole blocker from iter-1 (FM-FS-001) is resolved in its primary location. Three Minor findings remain (2 regressions + 1 carried over from iter-1).**

---

## Detailed Findings

### RG-001: Runtime Behavior Step 8b Not Updated to Full C3 Strategy Set

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | `.md` Runtime Behavior step 8b (line 846); cross-reference: QRP step 3 (line 591) |
| **Strategy Step** | S-010 Self-Refine (internal consistency check); S-011 Chain-of-Verification (cross-section consistency) |

**Evidence:**

Quality Review Protocol step 3 (fixed in iter-5):
```
3. [...] Then invokes `/adversary` adv-executor on the artifact with the C3 required
   strategy set (S-007, S-002, S-014, S-004, S-012, S-013).
```

Runtime Behavior step 8b (NOT updated in iter-5):
```
b. Invoke /adversary adv-scorer on artifact_path (S-014, 6-dimension rubric).
   Write adv-scorer output to:
   projects/PROJ-040-documentation/orchestration/reviews/{feature-id}-adv-review.md
```

The Runtime Behavior section is declared authoritative at line 776: "This is the authoritative runtime specification; the orchestrator follows this sequence on each Wave 1 execution session."

**Analysis:**

An orchestrator following step 8b would invoke only adv-scorer with S-014 for each C3 feature — exactly the pre-fix behavior that FM-FS-001 was meant to correct. The Quality Review Protocol narrative correctly describes the 6-strategy invocation, but the authoritative execution steps contradict it. For an automated executor parsing the runtime steps, this specification conflict would cause the wrong behavior.

The severity is Minor (not Major) because: (a) the primary fix location (`adversarial.strategy_sets.C3_per_feature.required`) is correct; (b) the Quality Review Protocol narrative is correct; (c) the inconsistency is within the `.md` only and a careful reader would see the contradiction. It does not rise to Major because the constitutional compliance of the strategy set is now correctly specified in the YAML's machine-readable block.

**Recommendation:**

Update Runtime Behavior step 8b to:
```
b. Invoke /adversary adv-executor on artifact_path with the C3 required strategy set:
   S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-014 (LLM-as-Judge),
   S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion).
   adv-scorer produces S-014 composite as part of this invocation.
   Write adv-executor/adv-scorer output to:
   projects/PROJ-040-documentation/orchestration/reviews/{feature-id}-adv-review.md
   Source: QRP step 3; adversarial.strategy_sets.C3_per_feature.required in ORCHESTRATION.yaml.
```

---

### RG-002: QG-1A and QG-1B Barrier `strategies.per_feature` Lists Not Updated

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | YAML `barriers.QG-1A.strategies.per_feature` (line 494); `barriers.QG-1B.strategies.per_feature` (line 530) |
| **Strategy Step** | S-011 Chain-of-Verification (cross-section consistency); S-012 FMEA (partial-fix failure mode) |

**Evidence:**

YAML `barriers.QG-1A.strategies`:
```yaml
strategies:
  per_feature: ["S-010", "S-014"]    # self-review + LLM-as-Judge; C3 minimum
```

YAML `barriers.QG-1B.strategies`:
```yaml
strategies:
  per_feature: ["S-010", "S-014"]
```

YAML `adversarial.strategy_sets.C3_per_feature.required` (corrected in iter-5):
```yaml
required:
  - S-007   # Constitutional AI Critique  (required at C2+)
  - S-002   # Devil's Advocate            (required at C2+)
  - S-014   # LLM-as-Judge                (required at C2+)
  - S-004   # Pre-Mortem Analysis         (required at C3+)
  - S-012   # FMEA                        (required at C3+)
  - S-013   # Inversion Technique         (required at C3+)
```

The barrier `strategies.per_feature` lists are distinct fields from `adversarial.strategy_sets.C3_per_feature.required`. An automated executor reading the barrier block to determine which strategies to run at each gate would see the old 2-strategy list.

**Analysis:**

The iter-5 fix was surgical: it correctly updated `adversarial.strategy_sets.C3_per_feature.required` and the `.md` Quality Review Protocol narrative. However, the YAML also contains `strategies.per_feature` fields within the two individual barrier definitions (QG-1A and QG-1B). These are secondary specification points for the same requirement, and they were not updated.

Severity is Minor because:
- The authoritative strategy set (`adversarial.strategy_sets.C3_per_feature.required`) is correct
- The barrier `strategies` fields are narrower summaries that should reference the strategy_sets block rather than duplicate it
- An executor with any sophistication would read the `adversarial.strategy_sets` block as the authoritative source

The comment `# self-review + LLM-as-Judge; C3 minimum` on QG-1A line 494 is also now incorrect ("C3 minimum" now entails 6 strategies, not 2).

**Recommendation:**

Update both barrier `strategies.per_feature` fields:
```yaml
# QG-1A:
strategies:
  per_feature: ["S-007", "S-002", "S-014", "S-004", "S-012", "S-013"]   # C3 required set; source: adversarial.strategy_sets.C3_per_feature

# QG-1B:
strategies:
  per_feature: ["S-007", "S-002", "S-014", "S-004", "S-012", "S-013"]   # C3 required set; source: adversarial.strategy_sets.C3_per_feature
```

Alternatively, replace the inline lists with a reference:
```yaml
strategies:
  per_feature: "see adversarial.strategy_sets.C3_per_feature.required"   # 6 strategies required at C3
```

---

### REM-001: `adversarial.quality.required_strategies` Scope Ambiguity Carried from Iter-1 (FM-FS-002)

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | YAML `adversarial.quality.required_strategies` (lines 764–774) |
| **Strategy Step** | S-013 Inversion (what does this YAML NOT protect against?) |

**Evidence:**

YAML `adversarial.quality.required_strategies` (unchanged from iter-1):
```yaml
required_strategies:
  - "S-010"    # self-review (per feature)
  - "S-007"    # constitutional compliance (at synthesis)
  - "S-002"    # devil's advocate (synthesis C4)
  - "S-014"    # LLM-as-Judge (all)
  - "S-001"    # red team (C4 tournament)
  - "S-003"    # steelman (C4 tournament; H-16 requires before S-002)
  - "S-004"    # pre-mortem (C4 tournament; required at C4)
  - "S-011"    # chain-of-verification (C4 tournament)
  - "S-012"    # FMEA (C4 tournament)
  - "S-013"    # inversion (C4 tournament)
full_tournament_at:
  - "QG-3"     # synthesis exit gate — all 10 strategies required at C4
```

This flat all-10 list remains scoped only by inline comments, not by YAML structure. The field name `required_strategies` without qualification still implies "all features." An executor reading only the `adversarial.quality` block would incorrectly apply all 10 strategies to every C3 feature.

**Analysis:**

This is the FM-FS-002 finding from iter-1, carried unchanged into iter-5. It was classified Minor in iter-1. Its severity has not changed. However, now that `adversarial.strategy_sets.C3_per_feature.required` is correctly specified (6 strategies), the risk of confusion between the two is slightly higher — there are now two conflicting signals in the same YAML file: the `required_strategies` list (all 10) and the `C3_per_feature.required` list (6).

The Pre-Mortem scenario from iter-1 remains valid: an executor automating against ORCHESTRATION.yaml reads `adversarial.quality.required_strategies` and applies all 10 strategies to every C3 feature.

**Recommendation:**

Rename the field to `all_strategies_in_workflow` and add a scope annotation:
```yaml
all_strategies_in_workflow:    # informational — lists all 10 strategies used anywhere in wave; NOT all required for every feature
  scope: "full_catalog"        # per-feature scope: see strategy_sets.C3_per_feature; synthesis scope: see strategy_sets.C4_synthesis
  - "S-001"    # red team (C4 tournament only)
  ...
```

Or remove it entirely (redundant given `strategy_sets` blocks).

---

## Per-Strategy Results

### S-010: Self-Refine

**Applied to:** Full deliverable set (both files together)

The iter-5 deliverables show targeted surgical corrections. The Revision Log entry for iter-5 accurately describes all five changes applied (FM-FS-001, FM-FS-004, FM-FS-005, RB-002, RB-003). The YAML header comment at line 6 enumerates all five fix targets.

**Self-refine observations:**
- FM-FS-001 primary fix is correct and complete in its canonical location
- FM-FS-004 and FM-FS-005 are clean and correctly specified
- The iter-5 self-review did not catch the secondary location gap (step 8b, barrier per_feature lists) — the same pattern as iter-1 where the creator correctly identified one issue but missed the propagation across sections

**Finding:** RG-001 and RG-002 represent a classic partial-fix failure mode: the fix was applied to the most prominent location but not propagated to all secondary locations where the same specification appears. S-010 should have caught this through a cross-section consistency check before submission.

---

### S-003: Steelman

**Strongest arguments for the iter-5 deliverable set quality:**

1. **FM-FS-001 resolution is architecturally correct.** The fix went to `adversarial.strategy_sets.C3_per_feature.required` — the right machine-readable block that an automated executor would parse for strategy selection. The SSOT citation is present. The Quality Review Protocol narrative explicitly lists all 6 strategies. For any human reader, the intent is unambiguous.

2. **FM-FS-004 (HEART fallback) is elegantly specified.** The `primary_artifact + fallback_artifact + fallback_condition + fidelity_note` structure in `barriers.QG-3.synthesis_inputs` is a clean, self-describing YAML pattern. The cross-reference from `barriers.QG-1B.special_case_FEAT_040_002_blocked` to `barriers.QG-3.synthesis_inputs FEAT-040-002 fallback_artifact entry` creates a bidirectional traceability link. This is better than the pre-fix state where neither location specified the fallback.

3. **FM-FS-005 (load_order) fix is safety-aware.** Adding both `orchestration/state/` and `orchestration/checkpoints/` with `note: "empty on fresh start — safe to skip if no files exist"` prevents the fix from breaking the fresh-start case. The orchestrator on fresh start can safely skip non-existent directories; the resume case gains the needed state file access.

4. **RB-002 and RB-003 are correctly resolved.** The QG-2 threshold derivation note is present in both the `.md` Quality Gates section and the YAML `barriers.QG-2.hard_conflict_threshold_derivation` field. The `plan_approval_source` is a concrete file path. The `fullset_approval_score: null` and `fullset_approval_source: null` are correctly null (the full-set review is this iteration; they should remain null until a PASS verdict is issued).

5. **Zero cross-file regressions in the 37 baseline claims.** All original cross-file consistency claims from iter-1 are unaffected by iter-5 changes.

---

### S-002: Devil's Advocate

**Challenges to the iter-5 deliverable set's adequacy:**

1. **The Runtime Behavior is the authoritative execution protocol and it is wrong.** Step 8b says "adv-scorer on artifact_path (S-014, 6-dimension rubric)" — not adv-executor with 6 strategies. The `.md` explicitly says this section is "the authoritative runtime specification; the orchestrator follows this sequence." A strictly compliant orchestrator following step 8b would execute exactly what FM-FS-001 was meant to fix: only S-014 per C3 feature. The fix is present in the narrative (QRP step 3) but the authoritative steps override narratives in any specification conflict.

2. **Two locations still specify the wrong strategy set.** QG-1A and QG-1B barrier `strategies.per_feature` lists remain `["S-010", "S-014"]`. These are not inactive comments — they are YAML fields structured to communicate per-feature strategy requirements at the barrier level. The consistency matrix now shows 2 mismatches in the new delta claims. The "fix" for FM-FS-001 is partial: one location correct, three locations wrong (step 8b, QG-1A.strategies, QG-1B.strategies).

3. **FM-FS-002 was classified Minor in iter-1 and acknowledged in the iter-2 claims scope — but was not fixed.** The iter-2 claims only addressed FM-FS-001 (Major) and the four other Minors (FM-FS-004, FM-FS-005, RB-002, RB-003). FM-FS-002 was not included in the fix set. It carries forward unchanged. In the context of the now-corrected `C3_per_feature.required` (6 strategies), the `required_strategies` flat list (all 10) is an even more visible contradiction within the same YAML file.

4. **The iter-5 Revision Log entry for item 5 says "updated adv-executor invocation to reference full set" but step 8b references adv-scorer, not adv-executor.** This means the Revision Log claim is inaccurate — it describes an update that was only partially applied. An auditor checking the Revision Log against the actual content would find a discrepancy.

---

### S-007: Constitutional AI Critique

**Principles checked (delta from iter-1 — focusing on new/changed areas):**

| Principle | Requirement | Compliance | Notes |
|-----------|-------------|------------|-------|
| H-13 | Quality threshold >= 0.92; C3 required strategy set | COMPLIANT (primary) / PARTIAL (secondary) | `C3_per_feature.required` correct; barrier `strategies.per_feature` and Runtime step 8b still incomplete |
| H-18 | S-007 constitutional compliance check required at C3 | COMPLIANT (primary) | S-007 now in `C3_per_feature.required`; secondary locations still absent |
| P-002 | File persistence — all state to filesystem | COMPLIANT | `file_persistence: true`; all paths declared |
| P-022 | No deception about capabilities | COMPLIANT | Disclaimer on both files; provisional HEART explicitly flagged; null fields for unpopulated scores are honest |
| H-16 | S-003 before S-002 | COMPLIANT | `h16_enforced: true`; canonical_sequence position 2=S-003, position 3=S-002 |

**Constitutional assessment:** H-13 and H-18 compliance is now present in the canonical machine-readable location (`adversarial.strategy_sets.C3_per_feature.required`). Secondary locations (barrier `strategies.per_feature`, Runtime step 8b) remain non-compliant. The constitutional violation severity has downgraded from the iter-1 state (where the canonical location was wrong) to a secondary-location specification inconsistency.

---

### S-004: Pre-Mortem

**"Wave 1 execution began. It failed. What went wrong?" (iter-5 state)**

**Failure scenario 1 (RG-001 root):** An orchestrator uses the Runtime Behavior steps as its execution script. It reaches step 8b. It invokes adv-scorer with S-014 only. Thirteen C3 features complete the quality cycle without S-007 (Constitutional AI Critique), S-002 (Devil's Advocate), S-004 (Pre-Mortem), S-012 (FMEA), or S-013 (Inversion). The Quality Review Protocol narrative is never consulted (it is framed as context, not instructions). The iter-5 fix goes unexecuted.

**Failure scenario 2 (RG-002 root):** An automated orchestrator reads `barriers.QG-1A.strategies.per_feature: ["S-010", "S-014"]` to configure Phase 1a feature review. It uses this barrier-level field as the authoritative per-feature strategy specification. It invokes only S-010 and S-014 for all 9 Phase 1a features. This is consistent with step 8b (Failure Scenario 1) but has an independent cause (the barrier field itself).

**Failure scenario 3 (REM-001 root, carried from iter-1):** An automated orchestrator reads `adversarial.quality.required_strategies` (all 10 strategies) and applies all 10 to every C3 feature. This creates 13 × 10 = 130 strategy invocations where 13 × 6 = 78 are required. Wave 1 execution is dramatically over-budget on time and context.

**Failure scenario 4 (low probability):** The Revision Log states iter-5 "updated adv-executor invocation to reference full set." An auditor verifying this claim checks step 8b and finds it references adv-scorer, not adv-executor. The Revision Log entry is inaccurate. The auditor flags a documentation integrity issue. This creates a trust deficit in the Revision Log as an audit trail.

---

### S-012: FMEA

**Failure Mode Enumeration (iter-2 surface — new and regression failures):**

| Failure Mode | Effect | S | O | D | RPN | Finding |
|-------------|--------|---|---|---|-----|---------|
| Runtime step 8b references adv-scorer/S-014 only | Orchestrator executes only S-014 per C3 feature; FM-FS-001 fix goes unexecuted at runtime | 7 | 5 | 5 | 175 | RG-001 |
| Barrier `strategies.per_feature` lists wrong strategies | Automated executor reads barrier field and applies S-010+S-014 only; 4 required strategies skipped | 6 | 4 | 6 | 144 | RG-002 |
| `required_strategies` scope ambiguity (FM-FS-002, unresolved) | Executor applies all 10 to C3 features; over-execution or scope confusion | 4 | 4 | 7 | 112 | REM-001 |
| Revision Log iteration 5 item 5 inaccurate ("updated adv-executor invocation") | Audit trail contains false claim; Revision Log integrity compromised | 3 | 5 | 6 | 90 | (Sub-finding of RG-001) |

**RPN Assessment (iter-2):** No new Critical-severity failure modes. RG-001 (RPN 175) and RG-002 (RPN 144) are below the FM-FS-001 threshold from iter-1 (RPN 448). The highest-severity original finding is resolved in its canonical location.

**Comparison to iter-1 RPN:** FM-FS-001 was 448 (the sole blocker). All iter-2 findings are in the 90–175 range — consistent with Minor severity classification.

---

### S-013: Inversion

**"What would need to be true for the iter-5 YAML to guarantee Wave 1 executes the correct C3 review protocol?"**

**What it now correctly protects:**
- `adversarial.strategy_sets.C3_per_feature.required` specifies the correct 6 strategies
- The YAML contains a machine-readable, unambiguous authoritative source for C3 strategy selection
- An executor that reads `adversarial.strategy_sets` before reading `barriers.{QG}.strategies` or `adversarial.quality.required_strategies` will get the correct answer

**What it does NOT protect:**
- An executor following the YAML's barrier structure (reading `barriers.QG-1A.strategies.per_feature`) would get the wrong strategy list
- An executor following the `.md` Runtime Behavior step 8b (the declared "authoritative" protocol) would get the wrong behavior
- The `adversarial.quality.required_strategies` flat list creates a contradictory signal

**Inversion conclusion:** The iter-5 YAML correctly specifies C3 strategy selection in the `adversarial.strategy_sets` block. The gap is that there are THREE entry points an executor might use to determine per-feature strategies, and only ONE of the three is now correct. For guaranteed correctness, all three must specify the same strategy set, or the other two must explicitly reference the authoritative `adversarial.strategy_sets.C3_per_feature.required` block.

---

### S-011: Chain-of-Verification

**Claim 1:** "FM-FS-001 is fully resolved — all references to C3 per-feature strategies are correct."

- `adversarial.strategy_sets.C3_per_feature.required`: 6 strategies ✓ VERIFIED
- `.md` Quality Review Protocol step 3: 6 strategies named ✓ VERIFIED
- `.md` Runtime Behavior step 8b: adv-scorer S-014 only ✗ FAILED — RG-001
- YAML `barriers.QG-1A.strategies.per_feature`: `["S-010", "S-014"]` ✗ FAILED — RG-002
- YAML `barriers.QG-1B.strategies.per_feature`: `["S-010", "S-014"]` ✗ FAILED — RG-002

**Verdict: PARTIAL (3/5 locations correct, 2/5 still wrong)**

**Claim 2:** "FM-FS-004 is fully resolved — HEART blocked fallback path is specified."

- YAML `barriers.QG-1B.special_case_FEAT_040_002_blocked`: provisional fallback specified ✓ VERIFIED
- YAML `barriers.QG-3.synthesis_inputs[FEAT-040-002]`: primary + fallback + condition + fidelity_note ✓ VERIFIED
- `.md` Failure Handling Phase Gate Failure: provisional fallback described ✓ VERIFIED

**Verdict: FULLY VERIFIED (3/3 locations correct)**

**Claim 3:** "FM-FS-005 is fully resolved — load_order includes state and checkpoints directories."

- YAML `resumption.load_order[5]`: `orchestration/state/` with purpose + note ✓ VERIFIED
- YAML `resumption.load_order[6]`: `orchestration/checkpoints/` with purpose + note ✓ VERIFIED
- Fresh-start safety note present: "empty on fresh start — safe to skip if no files exist" ✓ VERIFIED

**Verdict: FULLY VERIFIED (3/3 locations correct)**

**Claim 4:** "RB-002 QG-2 threshold derivation is present."

- `.md` QG-2 Hard Conflict Definition section (line 553): threshold derivation note present ✓ VERIFIED
- YAML `barriers.QG-2.hard_conflict_threshold_derivation`: derivation text present ✓ VERIFIED

**Verdict: FULLY VERIFIED (2/2 locations correct)**

**Claim 5:** "RB-003 plan_approval_source and fullset_approval fields are added."

- YAML `workflow.plan_approval_source: "orchestration/reviews/wave-1-plan-iter-4-scoring.md"` ✓ VERIFIED
- YAML `workflow.fullset_approval_score: null` ✓ VERIFIED
- YAML `workflow.fullset_approval_source: null` ✓ VERIFIED

**Verdict: FULLY VERIFIED (3/3 fields present)**

**Chain-of-Verification summary:** 4/5 claims fully verified. 1 claim (FM-FS-001 complete resolution) is partially verified — fix is correct in the canonical location but incomplete in 2 secondary locations. This produces findings RG-001 and RG-002.

---

### S-001: Red Team

**Attack surface: "How would a confused executor misuse the iter-5 deliverable set?"**

**Attack vector 1 — Authority conflict:** An executor encounters two contradictory specifications for the same behavior. The `.md` Runtime Behavior is declared "authoritative." It says invoke adv-scorer with S-014. The Quality Review Protocol (same file) says invoke adv-executor with 6 strategies. The YAML `adversarial.strategy_sets.C3_per_feature.required` says 6 strategies. The YAML `barriers.QG-1A.strategies.per_feature` says 2 strategies. The YAML `adversarial.quality.required_strategies` says 10 strategies. An executor implementing defensive parsing would escalate to user for clarification. A less robust executor would pick one source — likely the YAML barrier field (most specific to the gate being evaluated) — and get the wrong answer.

**Attack vector 2 — Partial-fix exploitation (same as iter-1):** The load_order fix (FM-FS-005) ensures an executor following load_order will read state files on resume. However, `session_resume_note` and `load_order` are in the same `resumption` block. A hasty executor might read `load_order` but not `session_resume_note`, missing the FEAT-040-002 `phase_completions` check instruction (which is only in the session_resume_note, not in the load_order entries themselves).

**Attack vector 3 — Revision Log credibility:** The Revision Log iter-5 item 5 states "updated adv-executor invocation to reference full set." Step 8b was not updated. This makes the Revision Log an unreliable source of truth for auditors. If the Revision Log can contain inaccurate claims about what was fixed, all Revision Log entries become suspect.

**Red Team Minor finding:** No new attack vectors beyond what iter-1 identified. The iter-5 partial fix creates a new authority-conflict attack vector (which executor specification wins when three YAML fields plus the `.md` authoritative section give four different answers?). This is a Minor severity risk manageable with the recommendations above.

---

## S-014 Scoring

### LLM-as-Judge: 6-Dimension Rubric

**Target:** Full deliverable set (`.md` iter-5 + `.yaml` v1.0.1) — iterative improvement from 0.939 baseline

| Dimension | Weight | Score | Weighted | Rationale |
|-----------|--------|-------|---------|-----------|
| **Completeness** | 0.20 | 0.96 | 0.192 | FM-FS-001 primary fix is present; all iter-1 required strategies now in canonical location; FM-FS-004/005 resolved; RG-001/RG-002 are specification gaps but the intent is present. Slight deduction for barrier `strategies.per_feature` fields not reflecting complete strategy set. |
| **Internal Consistency** | 0.20 | 0.92 | 0.184 | 2 new mismatches identified (RG-001, RG-002) in the 10-claim delta. Baseline 37/37 holds. The inconsistency between Runtime step 8b and QRP step 3 (both in the same `.md`) reduces this dimension from iter-1's 0.97. |
| **Methodological Rigor** | 0.20 | 0.94 | 0.188 | FM-FS-001 canonical location correct; C3 strategy set is constitutionally compliant in the machine-readable YAML block. Deduction for partial application: 2 of 4 fix locations still wrong. The improvement from iter-1 (0.88) is substantial but incomplete. |
| **Evidence Quality** | 0.15 | 0.96 | 0.144 | SSOT citation added to C3_per_feature.required; QG-2 threshold derivation present; FM-FS-005 includes rationale in purpose/note fields. Revision Log inaccuracy (iter-5 item 5) is a minor evidence quality gap. |
| **Actionability** | 0.15 | 0.94 | 0.141 | FM-FS-005 load_order fix makes session resume actionable. FM-FS-004 fallback path makes HEART blocked scenario actionable. RG-001 (step 8b) reduces actionability: an executor following the authoritative runtime steps would not invoke the correct strategy set. |
| **Traceability** | 0.10 | 0.95 | 0.095 | RB-002 QG-2 derivation traceable. RB-003 plan_approval_source traceable. FM-FS-002 (unresolved) `required_strategies` flat list still creates traceability confusion. Revision Log iter-5 item 5 inaccuracy reduces this dimension slightly. |

**Composite Score: 0.192 + 0.184 + 0.188 + 0.144 + 0.141 + 0.095 = 0.944**

**Band: REVISE (below C4 threshold of 0.95)**

**Improvement from iter-1:** 0.939 → 0.944 (+0.005). The FM-FS-001 primary fix improved Methodological Rigor from 0.88 → 0.94. However, the two regressions (RG-001, RG-002) reduced Internal Consistency from 0.97 → 0.92, partially offsetting the gain.

**Trajectory:** 0.901 → 0.954 → 0.968 → 0.972 (single-file) → 0.939 → 0.944 (full-set iterations)

---

## Verdict

**Score: 0.944 / 0.95 threshold → REVISE**

**Status: Below C4 threshold. No Major findings. Three Minor findings remain (2 regressions + 1 carried). Resolving RG-001 and RG-002 is expected to push composite to approximately 0.956 (above 0.95).**

### Remaining Findings

**Finding 1 (Minor — RG-001):** `.md` Runtime Behavior step 8b references only S-014 adv-scorer for C3 features. The authoritative execution protocol is inconsistent with the Quality Review Protocol step 3 fix. Fix: update step 8b to invoke adv-executor with full 6-strategy C3 set.

**Finding 2 (Minor — RG-002):** YAML `barriers.QG-1A.strategies.per_feature` and `barriers.QG-1B.strategies.per_feature` still list `["S-010", "S-014"]`. Fix: update both to list the 6-strategy C3 required set, or reference `adversarial.strategy_sets.C3_per_feature.required`.

**Finding 3 (Minor — REM-001):** YAML `adversarial.quality.required_strategies` flat list (all 10 strategies) not scoped — carried from FM-FS-002 in iter-1, not addressed in iter-5 fix set. Fix: rename or scope the field.

### Score Delta Analysis

If RG-001 and RG-002 are resolved (step 8b updated; barrier per_feature lists updated):
- Internal Consistency: 0.92 → 0.97 (+0.05 × 0.20 = +0.010)
- Methodological Rigor: 0.94 → 0.96 (+0.02 × 0.20 = +0.004)
- Actionability: 0.94 → 0.96 (+0.02 × 0.15 = +0.003)

**Projected composite after RG-001/RG-002 fix: 0.944 + 0.017 ≈ 0.961 → PASS at C4 >= 0.95**

REM-001 (FM-FS-002) is a pre-existing Minor. Fixing it would provide further upside but is not required for C4 PASS.

---

## Execution Statistics
- **Total Findings:** 3 (all new or carried Minor; no Major or Critical)
- **Critical:** 0
- **Major:** 0
- **Minor:** 3 (RG-001, RG-002, REM-001)
- **Protocol Steps Completed:** 9 of 9 (S-010 through S-001; S-014 scoring completed above)
- **Iter-2 Claims Verified:** 4 of 6 fully verified; 2 partially verified (RG-001, RG-002 introduced)
- **Prior blocker FM-FS-001:** RESOLVED in primary/canonical location
- **Regressions introduced:** 2 (RG-001, RG-002) — both Minor; no regression to Major/Critical state

---

*Report Version: 1.0.0*
*Tournament Iteration: 2 (Full-Set)*
*Executed: 2026-04-17*
*Workflow ID: wave-1-discovery-20260417-001*
*Worktracker Entity: FEAT-040-058*
