# Purple Team Orchestration Template

> **Template Version:** 1.0.0
> **Project:** PROJ-023 Rainbow Series | **Phase:** 5, Purple Team Automation
> **ADR Reference:** ADR-PROJ023-001 (Accepted, Hybrid B+C architecture)
> **Design Reference:** `projects/PROJ-023-exploit-framework/work/design/phase-5-purple-automation.md`
> **Composition Reference:** `projects/PROJ-023-exploit-framework/work/design/phase-5-redblue-composition.md`
> **Schema Reference:** `docs/schemas/purple-team-checkpoint.schema.json`

## Document Sections

| Section | Purpose |
|---------|---------|
| [Template Usage](#template-usage) | When and how to invoke this template |
| [Exercise Configuration](#exercise-configuration) | Required and optional configuration variables |
| [Session 1: Red Phase](#session-1-red-phase) | Phases 1-3: Scope, Reconnaissance, Exploitation |
| [Session 2: Blue Phase](#session-2-blue-phase) | Phases 4-6: Detection, Analysis, Remediation |
| [Session 3: Purple Phase](#session-3-purple-phase) | Phases 7-8: Re-test, Report |
| [Session 4: Extended Loop (Conditional)](#session-4-extended-loop-conditional) | Second iteration when coverage target not met |
| [Checkpoint Schema: 19-Field Reference](#checkpoint-schema-19-field-reference) | All checkpoint fields with types and descriptions |
| [Termination Conditions](#termination-conditions) | Four conditions that exit the emulation-validation loop |
| [Exchange Directory Structure](#exchange-directory-structure) | Neutral zone for cross-skill data transfer |
| [Trust Boundary Enforcement](#trust-boundary-enforcement) | Adversary-taint quarantine rules |
| [Emulation-Validation Loop (A-E)](#emulation-validation-loop-a-e) | 5-phase automated cycle reference |
| [Coverage Gap Taxonomy](#coverage-gap-taxonomy) | Detection classification states |
| [Routing Trigger](#routing-trigger) | Keyword detection for template activation |
| [OWASP and Security References](#owasp-and-security-references) | Backend security controls applied |

---

## Template Usage

**This template is selected by the main context** when the user requests a purple team exercise. It is NOT an agent -- it is a coordination guide executed by the main context using the `/orchestration` skill pattern (Option B from Phase 5 design: `/orchestration` skill coordinates via multi-skill combination). No dedicated purple-team orchestrator agent exists.

**Invocation conditions (any of):**
- User mentions: purple team, purple team exercise, emulation-validation, detection coverage exercise, red vs blue, attack emulation, detection gap analysis
- User explicitly requests: "load purple team template", "start purple team exercise"

**Execution model:**
- Multi-session (minimum 3 sessions; 4th session conditional on coverage result)
- The main context loads this template and executes all coordination directly
- /red-team and /blue-team agents are invoked as workers via Task tool; they do not invoke each other
- All cross-skill data flows through `work/purple-team/exchange/{engagement-id}/` (neutral zone)

**P-003 Compliance (single-level nesting):** Main context is the sole orchestrator. All red-team and blue-team agents are direct children. No worker agent invokes another worker. Verified across all three session topologies in Phase 5 P-003 compliance analysis.

**Before starting:** Ask the user for the `engagement_id` if not provided. Generate it from the format `{org-slug}-{YYYYMMDD}` if the user does not have one. Then copy the Exercise Configuration block below and fill in all required values.

---

## Exercise Configuration

```yaml
# Purple Team Exercise Configuration
# Fill in ALL required fields before proceeding to Session 1.

exercise:
  engagement_id: "{org-slug}-{YYYYMMDD}"       # REQUIRED -- used in all file paths
  exercise_type: "purple-team"                  # Fixed value
  purple_team_mode: true                        # Signals all agents to produce purple-team artifacts

scope:
  target_org: "{organization name}"             # REQUIRED
  authorized_targets: []                        # REQUIRED -- list of authorized targets
  technique_allowlist: []                       # REQUIRED -- ATT&CK technique IDs in scope
  tactics_in_scope: []                          # REQUIRED -- ATT&CK tactic IDs (TA0001, etc.)
  persistence_authorized: false                 # RoE gate for red-persist (default: false)
  exfiltration_authorized: false                # RoE gate for red-exfil (default: false)
  data_types_permitted: []                      # Required if exfiltration_authorized: true

coverage:
  target_detection_rate: 0.80                  # Coverage success threshold (default: 0.80)
  max_iterations: 3                            # Maximum loop iterations (default: 3, per RT-M-010)
  plateau_threshold: 0.05                      # Minimum per-iteration improvement (default: 5%)
  plateau_window: 2                            # Consecutive iterations below threshold = plateau

output:
  engagement_dir: "work/red-team/engagements/{engagement-id}/"
  blue_team_dir: "work/blue-team/engagements/{engagement-id}/"
  exchange_dir: "work/purple-team/exchange/{engagement-id}/"
  checkpoint_dir: "work/blue-team/engagements/{engagement-id}/checkpoints/"
```

---

## Session 1: Red Phase

**Phases covered:** 1 (Engagement Scope), 2 (Intelligence Preparation), 3 (Offensive Operations)
**Mandatory termination:** Checkpoint MUST be written at Phase 3/4 boundary before ending this session.
**Estimated tokens:** 120K-165K (within 200K budget; ~35K+ headroom for output generation)

### Phase 1: Engagement Scope

**Agents:** red-lead (required), blue-lead (required)

**Instruction to main context:**

1. Invoke `red-lead` with the exercise configuration above. Set `purple_team_mode: true` in the scope document. red-lead produces:
   - Rules of Engagement (RoE) document with technique_allowlist validated
   - Engagement scope document at `work/red-team/engagements/{engagement-id}/scope.md`
   - Confirmation of RoE gates: `persistence_authorized`, `exfiltration_authorized`

2. Invoke `blue-lead` with the engagement scope from red-lead. blue-lead produces:
   - Detection baseline scope at `work/blue-team/engagements/{engagement-id}/scope.md`
   - Initial D3FEND coverage baseline scope (which techniques have existing coverage)
   - Assessment objectives aligned with red-team technique_allowlist

3. Handoff validation (RV-01 through RV-04):
   - Both scope documents exist and are non-empty
   - `technique_allowlist` is consistent between red scope and blue scope
   - `purple_team_mode: true` is confirmed in both scope documents

**Exit criteria:** Both scope documents accepted; RoE gates confirmed.

### Phase 2: Intelligence Preparation

**Agents:** blue-intel (required), blue-d3fend (required)

**Instruction to main context:**

1. Invoke `blue-intel` with the blue scope document. blue-intel produces:
   - Adversary profile at `work/blue-team/intel/{engagement-id}/adversary-profile.md`
   - Threat intelligence for techniques in scope (TTP analysis)
   - STIX 2.1 threat actor SDO if applicable

2. Invoke `blue-d3fend` with the technique_allowlist from Phase 1 and adversary profile from blue-intel. blue-d3fend produces:
   - D3FEND baseline coverage matrix at `work/blue-team/d3fend/{engagement-id}/coverage-baseline.md`
   - Initial CFE/DGE envelope stubs for techniques in scope
   - Gap priority ranking: which techniques have NO D3FEND countermeasure mapping

3. Construct the initial `d3fend_coverage_baseline` checkpoint field from the blue-d3fend output.

**Exit criteria:** Adversary profile produced; D3FEND baseline coverage matrix persisted; `d3fend_coverage_baseline` checkpoint field populated.

### Phase 3: Offensive Operations (Emulation)

**Purpose:** Red team agents emulate in-scope ATT&CK techniques. This is Loop Phase A of the emulation-validation cycle.

**Agents (select per technique_allowlist):**
- `red-recon` -- for TA0043 Reconnaissance, TA0007 Discovery techniques
- `red-exploit` -- for TA0001 Initial Access, TA0002 Execution, TA0040 Impact
- `red-privesc` -- for TA0004 Privilege Escalation, TA0006 Credential Access
- `red-lateral` -- for TA0008 Lateral Movement
- `red-persist` -- ONLY if `persistence_authorized: true` in RoE (TA0003, TA0005 persistence-phase)
- `red-exfil` -- ONLY if `exfiltration_authorized: true` in RoE (TA0009 Collection, TA0010 Exfiltration)

**Instruction to main context:**

For each agent invoked, pass:
- The scope document with `purple_team_mode: true`
- The technique_allowlist filtered to the agent's owned tactics
- The instruction to produce an emulation manifest artifact alongside standard output

Each red-team agent MUST produce (purple team mode extensions -- RM-1, RM-2, RM-3):

```yaml
# Emulation manifest per technique (written to engagement artifact directory)
emulation_manifest_entry:
  technique_id: "{T-ID}"                 # e.g., T1059.001
  technique_name: "{name}"
  tactic: "{tactic name}"
  emulation_agent: "{agent name}"
  emulation_status: "COMPLETE|EMULATION_SKIPPED|EMULATION_FAILED"
  artifacts:
    - path: "{artifact path}"            # Pattern: {technique-id}-{artifact-name}.{ext}
      type: "payload|log_evidence|config|pcap"
      taint_level: "engagement-generated"       # Per rbee-v1.schema.json: adversary-produced | adversary-controlled | engagement-generated
  network_indicators:
    - type: "domain|ip|url|user-agent"
      value: "{value}"
  host_indicators:
    - type: "file_hash|filename|registry_key|process"
      value: "{value}"
  behavioral_indicators:
    - type: "process-creation|registry-modification|service-installation|scheduled-task"
      description: "{behavior description}"
      detection_logic: "{pseudocode or natural language}"
```

If a technique cannot be emulated: document as `EMULATION_SKIPPED` with reason. If zero techniques are emulated: HALT and escalate to user (H-31).

**After all emulation agents complete:**

Consolidate all emulation manifest entries into a single manifest file:

```
work/red-team/engagements/{engagement-id}/emulation-manifest.yaml
```

Construct RBEE (Red-Blue Exchange Envelope) for each finding and write to:

```
work/purple-team/exchange/{engagement-id}/rbee/finding-F-{NNN}.yaml
```

Write exchange directory manifest:

```
work/purple-team/exchange/{engagement-id}/manifest.yaml
```

**Exit criteria:**
- At least 1 technique emulated per tactic in scope (or EMULATION_SKIPPED with reason for missing tactics)
- All emulation artifacts persisted to `work/red-team/engagements/{engagement-id}/`
- `emulation-manifest.yaml` produced
- RBEE envelopes produced for all emulated techniques
- Exchange manifest written

### Session 1 Checkpoint (MANDATORY)

**Write checkpoint before ending Session 1.** File path: `work/blue-team/engagements/{engagement-id}/checkpoints/checkpoint-s1.yaml`

Required checkpoint fields for Session 1 (see [Checkpoint Schema: 19-Field Reference](#checkpoint-schema-19-field-reference)):

```yaml
session_id: "purple-{engagement-id}-s1"
phase_completed: 3
artifacts_produced:
  - "work/red-team/engagements/{engagement-id}/scope.md"
  - "work/blue-team/engagements/{engagement-id}/scope.md"
  - "work/blue-team/intel/{engagement-id}/adversary-profile.md"
  - "work/blue-team/d3fend/{engagement-id}/coverage-baseline.md"
  - "work/red-team/engagements/{engagement-id}/emulation-manifest.yaml"
  - "work/purple-team/exchange/{engagement-id}/manifest.yaml"
  # Add all red-team artifact paths
agent_handoff_state:
  red-lead: { status: "completed" }
  blue-lead: { status: "completed" }
  blue-intel: { status: "completed" }
  blue-d3fend: { status: "completed" }
  # Add all agents invoked with status
next_phase_entry_point: "Phase 4: Detection Validation -- requires emulation-manifest.yaml and RBEE envelopes"
d3fend_coverage_baseline: {}              # Populate from blue-d3fend output
token_usage:
  work_tokens: 0                          # Fill with actual
  framework_overhead: 15350
  total: 0                               # Fill with actual
exercise_id: "purple-{engagement-id}"
skills_involved: ["/red-team", "/blue-team"]
cross_skill_handoffs_completed:
  - integration_point: "IP-5"
    from_skill: "/red-team"
    to_skill: "/blue-team"
    artifacts: ["work/purple-team/exchange/{engagement-id}/manifest.yaml"]
    taint_level: "adversary-modeled"              # Per rbee-v1.schema.json trust_classification.taint_level const
red_team_findings_digest:
  finding_count: 0                        # Fill with actual
  technique_ids: []                       # Fill with emulated technique IDs
  severity_distribution:
    critical: 0
    high: 0
    medium: 0
    low: 0
    informational: 0
exchange_envelope_manifest:
  rbee_count: 0                           # Fill with actual count
  cfe_count: 0
  dge_count: 0
  manifest_path: "work/purple-team/exchange/{engagement-id}/manifest.yaml"
coverage_delta:
  previous:
    verified_detection_rate: 0.0
    gap_count: 0                          # Fill with total techniques in scope
  current:
    verified_detection_rate: 0.0
    gap_count: 0
emulation_manifest:
  techniques: []                          # Populate from emulation-manifest.yaml
  artifact_count: 0
loop_state:
  current_phase: "A"
  iteration_number: 1
  target_detection_rate: 0.80            # From exercise configuration
  termination_reason: null
  is_terminated: false
```

---

## Session 2: Blue Phase

**Phases covered:** 4 (Detection Validation), 5 (Coverage Gap Analysis), 6 (Rule Generation)
**Session resumption:** Load `checkpoint-s1.yaml`. Validate all `artifacts_produced` paths exist (RV-02).
**Mandatory termination:** Checkpoint MUST be written at Phase 6/7 boundary before ending this session.
**Estimated tokens:** 89K-109K (within 200K budget; ~90K+ headroom)

### Session Resumption Protocol

Before invoking any agents:

1. Load `work/blue-team/engagements/{engagement-id}/checkpoints/checkpoint-s1.yaml`
2. Validate ALL `artifacts_produced` paths exist. If any path is missing: HALT, report missing artifacts (H-31).
3. Load `emulation_manifest` from checkpoint for artifact path references
4. Load `d3fend_coverage_baseline` for coverage context
5. Load `loop_state` to confirm `current_phase: "A"` is complete and Phase B is the entry point
6. Load `exchange_envelope_manifest` to enumerate RBEE envelopes available

### Phase 4: Detection Validation (Loop Phase B)

**Purpose:** Validate existing detection rules against emulation artifacts. This is Loop Phase B.

**Agents:** blue-detect, blue-siem, blue-monitor, blue-ioc

**Instruction to main context:**

1. Invoke `blue-ioc` with the RBEE envelope paths from the exchange manifest. blue-ioc produces:
   - YARA rules from file indicators: `work/blue-team/ioc/{engagement-id}/rules/yara/`
   - Sigma rules from behavioral indicators: `work/blue-team/ioc/{engagement-id}/rules/sigma/`
   - Suricata rules from network indicators: `work/blue-team/ioc/{engagement-id}/rules/suricata/`
   - STIX 2.1 indicator bundle: `work/blue-team/ioc/{engagement-id}/stix/indicators-bundle.json`
   - Transformation report: `work/blue-team/ioc/{engagement-id}/transformation-report.md`
   - Trust boundary enforcement: blue-ioc MUST NOT Read adversary artifact content directly; receive only RBEE envelope metadata (hashes, paths, ATT&CK IDs)

2. Invoke `blue-detect` with the YARA rules produced by blue-ioc. blue-detect:
   - Validates YARA syntax via `yr check` before any scanning
   - Scans emulation artifacts via `yr scan` (tool-mediated; does NOT Read artifacts into context)
   - Produces per-technique detection results with confidence bounds
   - Outputs: `work/blue-team/detection/{engagement-id}/yara-scan-results.md`

3. Invoke `blue-siem` with the Sigma rules produced by blue-ioc. blue-siem:
   - Validates Sigma YAML syntax via `sigma check`
   - Analyzes EVTX evidence from emulation artifacts using Hayabusa/Chainsaw if available
   - Produces per-technique log detection results
   - Outputs: `work/blue-team/siem/{engagement-id}/sigma-detection-results.md`

4. Invoke `blue-monitor` with the Suricata rules produced by blue-ioc. blue-monitor:
   - Validates rule syntax
   - Marks all Suricata/Falco validation as Tier C (methodology-only; no deployed infrastructure)
   - Produces per-technique network detection guidance
   - Outputs: `work/blue-team/monitoring/{engagement-id}/network-detection-results.md`

**Per-technique detection result format (required for Phase 5 handoff):**

```yaml
detection_result:
  technique_id: "{T-ID}"
  technique_name: "{name}"
  tactic: "{tactic}"
  composite_status: "NO_DETECTION|PARTIAL_DETECTION|FULL_DETECTION_UNVERIFIED|FULL_DETECTION_VERIFIED"
  file_detection: { agent: "blue-detect", result: "DETECTED|NOT_DETECTED", rule: "{path}", confidence: 0.0 }
  log_detection: { agent: "blue-siem", result: "DETECTED|NOT_DETECTED", rule: "{path}" }
  network_detection: { agent: "blue-monitor", result: "DETECTED|NOT_DETECTED", tier: "C", note: "Methodology-only" }
  ioc_match: { agent: "blue-ioc", result: "DETECTED|NOT_DETECTED", matched_iocs: [] }
  missing_coverage: []                   # What detection domains still need rules
```

**Exit criteria (Loop Phase B):** Per-technique detection result produced for each emulated technique. Detection validation report persisted.

### Phase 5: Coverage Gap Analysis (Loop Phase C)

**Agents:** blue-d3fend, blue-detect, blue-siem

**Instruction to main context:**

1. Aggregate detection results from Phase 4 into a coverage summary.

2. Invoke `blue-d3fend` with:
   - Phase 4 aggregate detection results
   - Current D3FEND coverage baseline from Session 1 checkpoint
   - Instruction to update coverage matrix with `purple_team_validated` fields (BM-2)
   blue-d3fend produces:
   - Updated coverage matrix: `work/blue-team/d3fend/{engagement-id}/coverage-matrix-iter-1.md`
   - Gap analysis report: `work/blue-team/d3fend/{engagement-id}/gap-analysis-iter-1.md`
   - Prioritized gap list (Priority 1: NO_DETECTION, Priority 2: PARTIAL_DETECTION, Priority 3: Tier-C Unverified)
   - DGE envelope: `work/purple-team/exchange/{engagement-id}/dge/d3fend-gap-analysis.yaml`

3. **Termination assessment (EVALUATE BEFORE Phase 6):**
   - Calculate current `verified_detection_rate`
   - Check against `target_detection_rate` from exercise configuration
   - Check `iteration_history` for plateau detection (delta < `plateau_threshold` for `plateau_window` consecutive iterations)
   - Check `loop_state.iteration_number` against `max_iterations`
   - If ANY termination condition is met: skip Phase 6 and proceed directly to Session 3 reporting

**Gap classification reference:**

| Classification | Definition | Phase 6 Priority |
|----------------|-----------|-----------------|
| `NO_DETECTION` | No rule exists for this technique in any detection domain | Priority 1 -- rule generation required |
| `PARTIAL_DETECTION` | Detection in some domains; confidence < 0.70; or single-domain only | Priority 2 -- enhancement needed |
| `FULL_DETECTION_UNVERIFIED` | Rules exist but Tier C (no deployed infrastructure for execution validation) | Priority 3 -- infrastructure gap, not rule gap |
| `FULL_DETECTION_VERIFIED` | Rules exist and execution-validated (Tier A/B tools confirmed detection) | No action -- covered |

**Exit criteria (Loop Phase C):** Gap analysis report produced; coverage matrix updated; termination assessment completed; rule generation priorities ranked.

### Phase 6: Rule Generation (Loop Phase D)

**Condition:** Only execute if termination assessment in Phase 5 returned CONTINUE.

**Agents:** blue-ioc, blue-siem, blue-monitor

**Instruction to main context:**

1. Invoke `blue-ioc` targeting Priority 1 gaps (NO_DETECTION techniques with file-based gaps):
   - Generate YARA rules with purple team provenance header (BM-3):
     ```yaml
     # Purple Team Provenance Header
     # technique_id: {T-ID}
     # purple_iteration: 1
     # gap_priority: 1
     # emulation_artifact: {artifact path that informed this rule}
     ```
   - Output: `work/blue-team/ioc/{engagement-id}/rules/yara/purple-iter-1/`
   - Validate all generated rules via `yr check` before marking as validated

2. Invoke `blue-siem` targeting Priority 1 and Priority 2 gaps with log-based components:
   - Generate Sigma rules with provenance header
   - Validate syntax via `sigma check`
   - Output: `work/blue-team/siem/{engagement-id}/sigma/purple-iter-1/`

3. Invoke `blue-monitor` targeting Priority 1 and Priority 2 gaps with network components:
   - Generate Suricata/Falco rules marked as Tier C
   - Output: `work/blue-team/monitoring/{engagement-id}/suricata/purple-iter-1/`

4. Update rule inventory file: `work/blue-team/engagements/{engagement-id}/rule-inventory.yaml` (BM-4)

**Rule generation failure handling:**
- If rule authoring fails for a technique (insufficient artifact detail): mark as `RULE_GENERATION_BLOCKED` with reason
- YARA rule fails `yr check` after 1 retry: mark as `UNVALIDATED` and continue
- Zero rules generated for Priority 1 gaps: HALT and escalate to user (H-31)

**Exit criteria (Loop Phase D):** New rules produced for all Priority 1 gaps (or documented as RULE_GENERATION_BLOCKED). Enhanced rules for Priority 2 gaps where feasible. Rule inventory updated.

### Session 2 Checkpoint (MANDATORY)

**Write checkpoint before ending Session 2.** File path: `work/blue-team/engagements/{engagement-id}/checkpoints/checkpoint-s2.yaml`

Update fields from Session 1 checkpoint with Session 2 results. Key updates:

```yaml
session_id: "purple-{engagement-id}-s2"
phase_completed: 6
next_phase_entry_point: "Phase 7: Re-test -- requires checkpoint-s2.yaml and rule-inventory.yaml"
detection_inventory:
  rules: []                             # Populate from rule-inventory.yaml
  total_count: 0
  validated_count: 0
iteration_history:
  - iteration_number: 1
    verified_detection_rate: 0.0        # Fill with actual
    rules_created: 0
    gaps_closed: 0
    delta_from_previous: 0.0
coverage_dashboard:
  verified_detection_rate: 0.0          # Fill with actual
  detection_rate: 0.0
  gap_count: 0
  iteration_number: 1
  validation_ratio: 0.0
coverage_delta:
  previous:
    verified_detection_rate: 0.0        # From Session 1
    gap_count: 0
  current:
    verified_detection_rate: 0.0        # Fill with actual
    gap_count: 0
  improvement:
    detection_rate_delta: 0.0
    gaps_closed: 0
    rules_created: 0
    rules_validated: 0
    rules_untestable: 0
loop_state:
  current_phase: "D"
  iteration_number: 1
  target_detection_rate: 0.80
  termination_reason: null              # Or fill if termination triggered
  is_terminated: false                  # Or true if termination triggered
exchange_envelope_manifest:
  rbee_count: 0                         # From Session 1 (unchanged)
  cfe_count: 0                          # Populated if CFE produced
  dge_count: 1                          # DGE produced in Phase 5
  manifest_path: "work/purple-team/exchange/{engagement-id}/manifest.yaml"
```

---

## Session 3: Purple Phase

**Phases covered:** 7 (Re-test / Re-validation), 8 (Joint Report)
**Session resumption:** Load `checkpoint-s2.yaml`. Validate all artifact paths.
**Estimated tokens:** 110K-150K (within 200K budget; ~50K+ headroom)

### Session Resumption Protocol

Before invoking any agents:

1. Load `work/blue-team/engagements/{engagement-id}/checkpoints/checkpoint-s2.yaml`
2. Validate ALL `artifacts_produced` paths exist (RV-02).
3. Load `detection_inventory` to get the updated rule set for re-validation
4. Load `coverage_dashboard` for quick orientation on current detection rates
5. Load `loop_state` to determine whether loop is terminated or re-validation is needed
6. Check termination conditions from Session 2 termination assessment
7. If `loop_state.is_terminated: true` -- skip Phase 7 re-test; proceed to Phase 8 reporting

### Phase 7: Re-test (Loop Phase E)

**Condition:** Only execute if `loop_state.is_terminated: false` from Session 2.

**Agents:** blue-detect, blue-siem, blue-monitor, blue-ioc (same as Phase 4)

**Instruction to main context:**

Execute the same detection validation workflow as Phase 4, but with the updated rule set from Phase 6.

1. Invoke `blue-detect` with updated YARA rules from `rule-inventory.yaml` (iteration 1 rules included)
2. Invoke `blue-siem` with updated Sigma rules
3. Invoke `blue-monitor` with updated Suricata/Falco rules

Produce per-technique detection results using the same format as Phase 4.

**Calculate coverage improvement delta:**

```
improvement_delta = current_verified_detection_rate - previous_verified_detection_rate
```

**Termination re-assessment (Loop Phase E exit):**

| Condition | Check | Action |
|-----------|-------|--------|
| Coverage target met | `verified_detection_rate >= target_detection_rate` | EXIT LOOP with PASS status |
| Iteration ceiling | `iteration_number >= max_iterations (3)` | EXIT LOOP with CEILING status |
| Plateau detected | `improvement_delta < plateau_threshold` for `plateau_window` consecutive iterations | EXIT LOOP with PLATEAU status |
| User termination | User explicitly requests exit | EXIT LOOP with USER_STOP status |
| Continue | None of the above | If Session 4 conditional is available, continue; otherwise EXIT LOOP with BEST_EFFORT status |

Report termination result to user per P-022. Present current best coverage metrics.

**Update `coverage_feedback_envelope` (CFE) for red team:**

Construct CFE and write to: `work/purple-team/exchange/{engagement-id}/cfe/coverage-feedback.yaml`

The CFE informs red-team (specifically red-vuln) which techniques now have detection coverage and which remain undetected, enabling detection-aware vulnerability priority adjustment.

### Phase 8: Joint Report

**Agents:** blue-lead (required), red-reporter (required), blue-d3fend (required)

**Instruction to main context:**

1. Invoke `blue-d3fend` to produce final D3FEND coverage analysis with `purple_team_validated` fields updated for all exercised techniques. Final matrix: `work/blue-team/d3fend/{engagement-id}/coverage-matrix-final.md`

2. Construct final Coverage Feedback Envelope (CFE) for red-lead. Write to: `work/purple-team/exchange/{engagement-id}/cfe/final-coverage-feedback.yaml`

3. Invoke `red-reporter` with:
   - The engagement scope document
   - The emulation manifest from Session 1
   - The final coverage matrix from blue-d3fend
   - The CFE (for red team's perspective on coverage)
   red-reporter produces joint engagement report at:
   `work/red-team/engagements/{engagement-id}/joint-purple-team-report.md`

4. Invoke `blue-lead` to produce the blue team assessment summary at:
   `work/blue-team/engagements/{engagement-id}/blue-assessment-summary.md`

**Joint report required sections:**

- L0: Executive summary with final `verified_detection_rate`, gap count, and exercise ROI
- L1: Per-technique results table (emulation status, detection status, rule inventory, D3FEND countermeasure)
- L1: Rule inventory with validation status (YARA, Sigma, Suricata, Falco counts)
- L1: D3FEND coverage matrix with Verified/Partial/Unverified/Gap breakdown
- L1: Loop iteration history (improvement per iteration)
- L2: Gap closure roadmap for remaining undetected techniques
- L2: Infrastructure recommendations for Tier C tool deployment (Unverified promotion path)

### Session 3 Final Checkpoint (MANDATORY)

**Write final checkpoint.** File path: `work/blue-team/engagements/{engagement-id}/checkpoints/checkpoint-s3.yaml`

Key fields:

```yaml
session_id: "purple-{engagement-id}-s3"
phase_completed: 8
loop_state:
  current_phase: "E"
  iteration_number: 1                     # Or actual final iteration
  is_terminated: true
  termination_reason: "target_met|ceiling_reached|plateau_detected|user_requested"
coverage_dashboard:
  verified_detection_rate: 0.0            # Final rate
  gap_count: 0                            # Final gap count
  confidence_qualifier: "NORMAL|DEGRADED_CONFIDENCE"
```

---

## Session 4: Extended Loop (Conditional)

**Trigger condition:** ALL of the following must be true:
- `loop_state.is_terminated: false` after Session 3 Phase 7 termination assessment
- `loop_state.iteration_number < max_iterations (3)`
- `improvement_delta >= plateau_threshold` (no plateau detected)
- User confirms they want a second loop iteration

**Phases covered:** Loop iteration 2 (Phases D and E again, iteration counter = 2)
**Estimated tokens:** 68K-83K (well within 200K budget)

**Instruction to main context:**

1. Load `checkpoint-s3.yaml`. Validate artifact paths.
2. Set `loop_state.iteration_number = 2`
3. Execute Phase 6 (Rule Generation, iteration 2) targeting remaining gaps
4. Execute Phase 7 (Re-test, iteration 2) with all rules from iterations 1 and 2
5. Re-evaluate termination conditions
6. If coverage target met or plateau detected: proceed to Phase 8 reporting
7. If iteration ceiling (3) reached: EXIT, report to user, proceed to Phase 8

Write Session 4 checkpoint: `checkpoint-s4.yaml`

**Loop iteration record for `iteration_history`:**

```yaml
iteration_history_entry:
  iteration_number: 2
  verified_detection_rate: 0.0           # Fill with actual
  rules_created: 0
  gaps_closed: 0
  delta_from_previous: 0.0              # Must be >= plateau_threshold to avoid termination
```

---

## Checkpoint Schema: 19-Field Reference

The checkpoint schema includes 16 base fields from `docs/schemas/purple-team-checkpoint.schema.json` plus 3 cross-skill fields added by Phase 5. All 19 fields are listed here for operator reference.

**5 Required Base Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | `purple-{engagement-id}-s{N}` format. Pattern: `^purple-[a-z0-9-]+-s[0-9]+$` |
| `phase_completed` | integer (1-8) | Last fully completed phase number |
| `artifacts_produced` | array[string] | File paths to all artifacts from this session |
| `agent_handoff_state` | object | Per-agent completion status and last handoff data |
| `next_phase_entry_point` | string | Entry criteria for next session |

**11 Optional Base Fields (strongly recommended):**

| Field | Type | Description |
|-------|------|-------------|
| `d3fend_coverage_baseline` | object | Running D3FEND coverage matrix state from blue-d3fend |
| `token_usage` | object | `work_tokens`, `framework_overhead`, `total` (all integers) |
| `exercise_id` | string | Cross-skill exercise ID. Pattern: `^[a-z]+-[a-z0-9-]+$` |
| `skills_involved` | array[string] | Skills participating (e.g., `["/red-team", "/blue-team"]`) |
| `cross_skill_handoffs_completed` | array[object] | Completed IP handoffs with `integration_point`, `from_skill`, `to_skill`, `artifacts`, `taint_level` (per rbee-v1.schema.json) |
| `pending_cross_skill_handoffs` | array[object] | Handoffs pending for next session with `prerequisite_artifacts` |
| `emulation_manifest` | object | Phase A technique-artifact-indicator mapping |
| `detection_inventory` | object | Current rule inventory (YARA, Sigma, Suricata, Falco) with validation status |
| `iteration_history` | array[object] | Per-iteration detection rate, rules created, gaps closed, delta |
| `coverage_dashboard` | object | Latest snapshot: `verified_detection_rate`, `detection_rate`, `gap_count`, `iteration_number` |
| `loop_state` | object | `current_phase` (A-E), `iteration_number`, `target_detection_rate`, `termination_reason`, `is_terminated` |

**3 Cross-Skill Extension Fields (Phase 5 additions):**

| Field | Type | Description |
|-------|------|-------------|
| `red_team_findings_digest` | object | Digest of red team findings: `finding_count`, `technique_ids` array, `severity_distribution` object. Enables quick orientation in Session 2 without loading full RBEE envelopes (CB-04). |
| `exchange_envelope_manifest` | object (required: `rbee_count`, `cfe_count`, `dge_count`, `manifest_path`) | Tracks all exchange envelopes produced. `manifest_path` points to `work/purple-team/exchange/{engagement-id}/manifest.yaml`. |
| `coverage_delta` | object | Pre/post coverage tracking: `previous` (rate + gap count), `current` (rate + gap count), `improvement` (`detection_rate_delta`, `gaps_closed`, `rules_created`, `rules_validated`, `rules_untestable`). |

**Total: 19 fields** (5 required + 14 optional; all validated against `docs/schemas/purple-team-checkpoint.schema.json`)

---

## Termination Conditions

The emulation-validation loop (Phases A-E) exits when ANY of the following conditions is met. Conditions are evaluated in precedence order.

| Priority | Condition | Threshold | Exit Status | Action |
|----------|-----------|----------|-------------|--------|
| 1 (highest) | **User termination** | User explicitly requests stop | `USER_STOP` | EXIT immediately. Persist all artifacts. Write checkpoint with `is_terminated: true`. Inform user of partial coverage achieved. |
| 2 | **Coverage target met** | `verified_detection_rate >= target_detection_rate` (default: 0.80) | `TARGET_MET` | EXIT with PASS. Produce final coverage dashboard. Proceed to Phase 8 reporting. |
| 3 | **Iteration ceiling reached** | `iteration_number >= max_iterations` (default: 3) | `CEILING_REACHED` | EXIT. Report to user per P-022 with current best result and remaining gaps. Proceed to Phase 8 reporting. |
| 4 (lowest) | **Coverage improvement plateau detected** | `improvement_delta < plateau_threshold` (default: 5%) for `plateau_window` (default: 2) consecutive iterations | `PLATEAU_DETECTED` | EXIT. Report plateau with analysis: remaining gaps are likely due to Tier C infrastructure dependencies or insufficient emulation artifacts, not rule authorship gaps. Proceed to Phase 8 reporting. |

**Plateau threshold derivation:** The 5% threshold (0.05) is more permissive than the agent routing standards plateau detection (0.01 for 3 iterations) because purple team coverage operates at coarser granularity -- a single new detection rule can shift coverage by 5-10% with a 10-20 technique pool. The 2-iteration window (vs. 3) reflects higher per-iteration cost (each loop spans a full session). These thresholds are provisional; calibrate after 3-5 exercises.

**On any termination:** Update `loop_state.is_terminated: true` and `loop_state.termination_reason` in the session checkpoint before ending.

---

## Exchange Directory Structure

All cross-skill data flows through the neutral exchange directory. Neither /red-team nor /blue-team agents write here directly -- the main context constructs all envelopes.

```
work/purple-team/exchange/{engagement-id}/
    manifest.yaml                               # Master envelope manifest (written by main context)
    rbee/                                       # Red-to-Blue Exchange Envelopes (IP-5)
        finding-F-001.yaml                      # One RBEE per red-team finding
        finding-F-002.yaml
        ...
    cfe/                                        # Coverage Feedback Envelopes (Blue-to-Red)
        coverage-feedback.yaml                  # Post-Phase-E feedback to red-vuln
        final-coverage-feedback.yaml            # Post-exercise final CFE to red-lead
    dge/                                        # D3FEND Gap Envelopes (Blue-to-Red)
        d3fend-gap-analysis.yaml                # blue-d3fend gap analysis to red-lead
```

**`manifest.yaml` format:**

```yaml
engagement_id: "{engagement-id}"
created: "2026-03-14T00:00:00Z"
envelopes:
  - type: "RBEE"
    path: "rbee/finding-F-001.yaml"
    technique_id: "T1059.001"
    created: "2026-03-14T10:00:00Z"
    taint_level: "adversary-modeled"              # Per rbee-v1.schema.json trust_classification.taint_level const
  - type: "CFE"
    path: "cfe/coverage-feedback.yaml"
    created: "2026-03-15T14:00:00Z"
    trust_level: "analysis-derived"
  - type: "DGE"
    path: "dge/d3fend-gap-analysis.yaml"
    created: "2026-03-15T15:00:00Z"
    trust_level: "analysis-derived"
```

---

## Trust Boundary Enforcement

All cross-skill data transfers enforce the Zone 1-to-Zone 1 trust boundary with adversary-taint propagation rules. These controls apply at every IP-5, CFE, and DGE transfer.

| Stage | Rule | Enforcement |
|-------|------|-------------|
| RBEE construction | Main context reads only structured YAML metadata from red-reporter L1 output; never reads binary adversary artifacts into context | Main context parses finding YAML; artifact content stays in `/red-team` output directory |
| blue-ioc ingestion | blue-ioc receives RBEE envelope paths; validates STIX schema on any STIX data; applies field size limit (2,000 chars) to free-text fields | Input validation per blue-ioc guardrails |
| blue-detect artifact scanning | blue-detect scans artifacts using `yr scan` via Bash tool; does NOT Read adversary artifact content into context window | Tool-mediated analysis only (Zone 1 enforcement) |
| blue-siem EVTX analysis | blue-siem invokes Hayabusa/Chainsaw on EVTX files via Bash; does NOT Read EVTX binary into context | Tool-mediated forensic analysis only |
| CFE construction | Main context reads detection results (not adversary artifacts) and constructs CFE; CFE trust_level = "analysis-derived" | Trust elevation from adversary-tainted to analysis-derived through tool-mediated processing |
| DGE construction | blue-d3fend produces DGE from coverage matrix (not raw red-team findings); DGE trust_level = "analysis-derived" | Same trust elevation as CFE |

**Credential filter:** All agents processing cross-skill handoffs apply the Rainbow credential filter pipeline per `skills/rainbow/rules/rainbow-credential-filter.md`. Three filter layers: L1 regex, L2 entropy, L3 structural. Fail-closed: if filter crashes, artifact is rejected.

---

## Emulation-Validation Loop (A-E)

Reference diagram for the 5-phase automated cycle:

```
LOOP ITERATION {N}
    |
    v
[Phase A: Emulation]                   -- Session 1 (first iteration only)
    | red-team agents emulate TTPs
    | Produce emulation-manifest.yaml
    | Write RBEE envelopes
    |
    v
[Phase B: Detection Validation]        -- Session 2 (Phase 4)
    | blue-detect: YARA scan
    | blue-siem: Sigma/EVTX analysis
    | blue-monitor: Suricata matching (Tier C)
    | blue-ioc: IOC matching
    |
    v
[Phase C: Gap Identification]          -- Session 2 (Phase 5)
    | blue-d3fend: ATT&CK -> D3FEND gap mapping
    | Termination assessment
    |
    | is_terminated? YES -> Skip Phase D -> Proceed to Session 3
    |               NO  -> Continue to Phase D
    v
[Phase D: Rule Generation]             -- Session 2 (Phase 6)
    | blue-ioc: YARA rules for file gaps
    | blue-siem: Sigma rules for log gaps
    | blue-monitor: Suricata/Falco for network gaps
    |
    v
[Phase E: Re-Validation]               -- Session 3 (Phase 7)
    | Same agents as Phase B
    | Updated rule inventory
    | Calculate improvement_delta
    | Termination re-assessment
    |
    | PASS/CEILING/PLATEAU/USER_STOP -> Phase 8 Reporting
    | CONTINUE (iteration < max)      -> Session 4 (next iteration)
```

---

## Coverage Gap Taxonomy

Technique state machine used throughout the exercise lifecycle:

| State | Definition | Next State Trigger |
|-------|-----------|-------------------|
| `NOT_IN_SCOPE` | Technique not selected for this exercise | User/red-lead adds to technique_allowlist |
| `IN_SCOPE` | Technique selected; awaiting emulation | Phase A execution |
| `EMULATED` | Phase A: emulation completed successfully | Phase B detection validation |
| `EMULATION_SKIPPED` | Phase A: technique could not be emulated (documented reason) | No Phase B for this technique; counted as gap |
| `EMULATION_FAILED` | Phase A: emulation attempt failed (documented reason) | Re-attempt in next iteration if applicable |
| `NO_DETECTION` | Phase B: no detection rule in any domain | Priority 1 for Phase D rule generation |
| `PARTIAL_DETECTION` | Phase B: some domains detected; confidence < 0.70 | Priority 2 for Phase D rule enhancement |
| `FULL_DETECTION_UNVERIFIED` | Phase B/E: rules exist but Tier C (not execution-validated) | Priority 3 -- infrastructure gap, not rule gap |
| `FULL_DETECTION_VERIFIED` | Phase B/E: Tier A/B validated detection confirmed | No action; contributes to `verified_detection_rate` |
| `RULE_GENERATED` | Phase D: new rule created for this technique | Phase E re-validation |
| `RULE_GENERATION_BLOCKED` | Phase D: rule authoring failed (insufficient artifact detail) | Document reason; report to user in Phase 8 |
| `COVERAGE_IMPROVED` | Phase E: detection status improved vs. prior iteration | Update coverage dashboard |
| `COVERAGE_UNCHANGED` | Phase E: no improvement despite new rules | Investigate root cause; may trigger plateau |
| `COVERAGE_REGRESSED` | Phase E: detection rate decreased (rule false-positive or invalidation) | Immediately investigate; escalate to user |

---

## Routing Trigger

This template is invoked via the `/orchestration` skill. The trigger map entry for purple team activation:

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Routing Action |
|---|---|---|---|---|
| purple team, purple team exercise, emulation-validation, detection coverage exercise, red vs blue, attack emulation, detection gap analysis | adversarial quality review, quality gate | 1 | "purple team" OR "emulation-validation" OR "detection coverage" (phrase match) | Load this template via `/orchestration`. |

**Routing rationale:** Priority 1 ensures `/orchestration` is selected first when purple team keywords are detected. Individual `/red-team` and `/blue-team` keywords continue to route to their respective skills for standalone engagements.

---

## OWASP and Security References

Backend security controls applied throughout purple team orchestration:

| OWASP Category | Control Applied |
|----------------|----------------|
| A01:2021 Broken Access Control | Trust boundary enforcement: adversary-tainted artifacts cannot be Read into agent context; tool-mediated analysis only |
| A03:2021 Injection | Input validation on all RBEE fields: field size limits, STIX schema validation, no direct adversary content ingestion |
| A05:2021 Security Misconfiguration | Exchange directory write-protected: only main context writes envelopes; both skills can Read |
| A09:2021 Logging Failures | All cross-skill handoffs logged in `manifest.yaml`; all envelope trust levels recorded |
| A10:2021 SSRF | No outbound connections from blue-team agents during artifact processing; tool-mediated scanning prevents SSRF via adversary-controlled content |

---

*Template Version: 1.0.0*
*ADR Reference: ADR-PROJ023-001 (Accepted, Hybrid B+C architecture)*
*Design Source: `projects/PROJ-023-exploit-framework/work/design/phase-5-purple-automation.md`*
*Composition Source: `projects/PROJ-023-exploit-framework/work/design/phase-5-redblue-composition.md`*
*Schema Source: `docs/schemas/purple-team-checkpoint.schema.json`*
*Created: 2026-03-16*
*Agent: eng-backend*
