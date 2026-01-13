# Trade-Off and Systems Analysis: INV-NAV-2026-001

**Document ID:** ANA-NAV-2026-001-R1
**Analyst:** ps-analyst (v2.1.0)
**Date:** 2026-01-12
**Test ID:** PS-ORCH-007 (Step 2 of 3)

---

## L0: Executive Summary

The investigation report (INV-NAV-2026-001-R1) presents a **logically sound and well-evidenced root cause analysis**. The 5 Whys chain correctly traces the 14.95% delta-V discrepancy to a configuration management gap introduced during ML augmentation of the navigation system.

**Validation Verdict:** VALIDATED with minor adjustments

| Aspect | Assessment | Confidence Adjustment |
|--------|------------|----------------------|
| Root Cause Chain | Valid | +2% (to 90%) |
| FMEA Prioritization | Valid with recalibration | No change |
| Corrective Actions | Feasible, reordered | N/A |
| Risk Assessment | Accurate | Confirmed |

**Key Recommendations:**
1. Prioritize SA-001 (automated version check) before IA-001 (ground update)
2. Add missing failure mode: FM-007 (ML model drift without recalibration trigger)
3. Establish quantitative success criteria for corrective actions

---

## L1: Summary Analysis

### 1.1 Root Cause Validation Summary

The investigation correctly identifies a **multi-level causation chain**:

```
CM Gap (Root) → Async Versioning (Systemic) → Version Mismatch (Primary) → SRP Coefficient Delta (Direct) → 14.95% Discrepancy (Observed)
```

**Validation Points:**
- Mathematical verification confirms SRP coefficient difference accounts for observed delta-V difference (1.5 m/s calculated vs 1.6 m/s observed)
- Evidence quality is strong at proximate levels (95% confidence for version mismatch) and moderately strong at systemic levels (85-88%)
- No alternative explanations identified that would better fit the evidence

### 1.2 FMEA Assessment Summary

The FMEA is appropriately structured with reasonable RPN calibration. FM-004 (No physics model sync requirement, RPN=196) is correctly identified as highest priority.

**Adjustments Recommended:**
- FM-005 severity may be under-rated; ML hazard unknowns warrant S=7 (vs current S=6)
- Missing failure mode: ML model drift without recalibration trigger

### 1.3 Corrective Action Priority Summary

| Rank | Action ID | Rationale |
|------|-----------|-----------|
| 1 | SA-001 | Implement CI/CD gate before any software update to prevent recurrence |
| 2 | IA-001 | Update ground system after CI/CD gate exists |
| 3 | IA-002 | Use calibrated coefficients for immediate operations |
| 4 | LA-001 | SRD amendment addresses root cause |
| 5 | LA-002 | ML hazard analysis for comprehensive risk reduction |

### 1.4 Risk Assessment Validation

| Risk Type | Investigation Finding | Analyst Assessment | Verdict |
|-----------|----------------------|-------------------|---------|
| Immediate | LOW | LOW | CONFIRMED |
| Systemic | HIGH | HIGH | CONFIRMED |
| Residual (post-corrective) | Not assessed | MEDIUM-LOW | ADDED |

---

## L2: Detailed Technical Analysis

### 2.1 Root Cause Validation (5 Whys Chain)

#### Why #1 Analysis
**Claim:** AI used higher SRP force estimates, requiring more delta-V.
**Evidence Quality:** STRONG
- SRP contribution range (1.4-1.8 m/s) is physically reasonable
- 18% higher SRP compensation factor aligns with coefficient difference
- Discrepancy magnitude (1.6 m/s) is within expected range

**Logical Soundness:** The causal link between SRP modeling and delta-V calculation is physically correct. Higher assumed SRP force would require more delta-V to achieve the same trajectory.

**Verdict:** VALIDATED

#### Why #2 Analysis
**Claim:** Flight software v4.2.1 updated SRP model with area-varying coefficients.
**Evidence Quality:** STRONG
- Release notes document FSW-4.2.1-SRP-001 feature
- Coefficient values provided (Cr=1.8 default vs Cr=1.54 calibrated)
- 14.4% difference matches observed 14.95% within measurement tolerance

**Logical Soundness:** The physics is correct. Calibrated Cr values based on actual spacecraft reflectivity would differ from worst-case defaults.

**Potential Gap:** No evidence provided that v4.2.1 Cr value (1.54) was validated against actual on-orbit measurements. However, this does not invalidate the root cause conclusion.

**Verdict:** VALIDATED

#### Why #3 Analysis
**Claim:** Ground system at v4.2.0 did not receive SRP update.
**Evidence Quality:** STRONG
- Version numbers confirmed via logs and telemetry
- v4.2.1 explicitly documented as flight-only patch

**Logical Soundness:** Version asymmetry is definitively established.

**Verdict:** VALIDATED

#### Why #4 Analysis
**Claim:** CM process allows independent versioning without model parity check.
**Evidence Quality:** MODERATE
- PR-SW-102 cited but not fully analyzed
- 6-month gap since last compatibility review established
- No documented requirement for SRP model parity

**Logical Soundness:** The systemic gap is plausible but relies on procedural analysis rather than direct evidence of a breakdown.

**Potential Alternative:** Could the CM process have been correctly followed but insufficiently specified? (Same practical outcome, different remediation focus)

**Verdict:** VALIDATED with note that remediation should address both process definition and adherence

#### Why #5 Analysis
**Claim:** ML augmentation added post-design without updating CM requirements.
**Evidence Quality:** MODERATE
- SRD section 4.3.2 predates ML integration (confirmed)
- ML added 18 months ago (v4.0) without SRD amendment
- Post-launch calibration in v4.2.1 without CM review

**Logical Soundness:** This is the true root cause. The design assumption of algorithm parity was invalidated by ML integration, but documentation and processes were not updated.

**Verdict:** VALIDATED

#### Alternative Explanations Considered

| Alternative | Likelihood | Reason for Rejection |
|-------------|------------|---------------------|
| Sensor malfunction | Very Low | Star tracker, IMU all nominal |
| Ephemeris error | Very Low | 2-hour sync confirmed current |
| Calculation bug in ML model | Low | Mathematical verification confirms physics model as cause |
| Deliberate override | Very Low | No evidence; defense-in-depth worked |

**Conclusion:** No alternative explanation better fits the evidence. The investigation's root cause is the most parsimonious explanation.

### 2.2 FMEA Assessment

#### RPN Calibration Review

| ID | S | O | D | RPN | Assessment |
|----|---|---|---|-----|------------|
| FM-001 | 8 | 6 | 3 | 144 | **Appropriate.** Version mismatch is detectable with proper tooling (D=3 reasonable). |
| FM-002 | 7 | 5 | 4 | 140 | **Appropriate.** Default coefficients are a known risk area. |
| FM-003 | 8 | 4 | 5 | 160 | **Appropriate.** Training bias is subtle but critical when detected. |
| FM-004 | 7 | 7 | 4 | 196 | **Correctly highest.** Systemic gap has high occurrence potential. |
| FM-005 | 6 | 5 | 6 | 180 | **Under-rated severity.** Unknown failure modes from ML integration could be S=7-8 (see adjustment below). |
| FM-006 | 10 | 2 | 2 | 40 | **Appropriate.** Current validation is effective (this incident proves it). |

#### Recommended Severity Adjustment: FM-005

**Current:** S=6 (Minor mission impact)
**Recommended:** S=7 (Moderate mission impact)

**Rationale:** Unknown failure modes from post-design ML integration represent potential for undetected systematic errors. The incident under analysis is one manifestation; other latent failure modes may exist. Given the safety-critical nature of navigation, underestimating severity is riskier than overestimating.

**Adjusted RPN for FM-005:** 7 x 5 x 6 = **210** (would become highest priority)

#### Missing Failure Mode: FM-007

| ID | Failure Mode | Potential Effect | S | O | D | RPN |
|----|--------------|------------------|---|---|---|-----|
| FM-007 | ML model drift without recalibration trigger | Gradual degradation of recommendation quality | 7 | 5 | 6 | 210 |

**Rationale:** The ML model was fine-tuned 14 days prior. There is no documented trigger for recalibration when physics models change, sensor characteristics drift, or operating conditions shift. This failure mode is distinct from FM-003 (training inconsistency) as it addresses ongoing operational drift rather than initial training error.

**Recommended Action:** Implement ML model performance monitoring with automated alerts when recommendation variance exceeds threshold.

#### Updated FMEA Priority Order

1. **FM-007:** ML model drift without recalibration trigger (RPN=210) - NEW
2. **FM-005:** Post-design ML integration gaps (RPN=210, adjusted)
3. **FM-004:** No physics model sync requirement (RPN=196)
4. **FM-003:** ML model trained on inconsistent data (RPN=160)
5. **FM-001:** Flight/Ground SW version mismatch (RPN=144)
6. **FM-002:** Default SRP coefficients used (RPN=140)
7. **FM-006:** Validation process bypass (RPN=40)

### 2.3 Corrective Action Analysis

#### Immediate Actions (0-48 hours)

| ID | Action | Feasibility | Cost | Benefit | Dependencies | Analysis |
|----|--------|-------------|------|---------|--------------|----------|
| IA-001 | Update ground system to v4.2.1 | HIGH | LOW (already developed) | HIGH (eliminates direct cause) | None | **CAUTION:** Without SA-001 first, this may mask future mismatches. Recommend waiting for CI/CD gate. |
| IA-002 | Use calibrated SRP coefficients | HIGH | LOW | HIGH | IA-001 completion | Can proceed immediately as manual override while IA-001 pending. |
| IA-003 | Verify ML model assumptions | MEDIUM | MEDIUM | HIGH | Access to training logs | Essential but may require ML team deep dive. |

**Recommendation:** Execute IA-002 and IA-003 immediately. Delay IA-001 until SA-001 is at least designed (to avoid embedding future risk).

#### Short-term Actions (1-4 weeks)

| ID | Action | Feasibility | Cost | Benefit | Dependencies | Analysis |
|----|--------|-------------|------|---------|--------------|----------|
| SA-001 | Automated version compatibility check in CI/CD | HIGH | MEDIUM | VERY HIGH (prevents recurrence) | CI/CD infrastructure | **HIGHEST PRIORITY.** This should be expedited to 0-72 hours if possible. |
| SA-002 | Add physics model comparison to pre-burn checklist | HIGH | LOW | MEDIUM (manual, error-prone) | Checklist governance | Good interim measure while SA-001 develops. |
| SA-003 | ML model revalidation | MEDIUM | MEDIUM | HIGH | Ground system update (IA-001) | Blocked by IA-001 but can prepare test cases now. |

**Recommendation:** SA-001 should be elevated to immediate priority. Implement basic version check gate within 72 hours, then enhance over 1-4 weeks.

#### Long-term Actions (1-6 months)

| ID | Action | Feasibility | Cost | Benefit | Dependencies | Analysis |
|----|--------|-------------|------|---------|--------------|----------|
| LA-001 | Amend SRD section 4.3.2 | HIGH | LOW | VERY HIGH (addresses root cause) | Systems engineering review board | Should be expedited to 4-6 weeks. |
| LA-002 | ML hazard analysis | MEDIUM | HIGH | HIGH (comprehensive risk reduction) | LA-001 informs scope | Can start in parallel with LA-001. |
| LA-003 | Physics model config baseline with drift detection | MEDIUM | HIGH | VERY HIGH | Architecture review | Addresses FM-007. |
| LA-004 | Model provenance tracking | MEDIUM | MEDIUM | HIGH | MLOps infrastructure | Enables FM-003 prevention. |

**Recommendation:** Prioritize LA-001 and LA-003. LA-002 and LA-004 can follow.

#### Dependency Graph

```
                    ┌─────────────────────────────────────────────┐
                    │                                             │
                    ▼                                             │
              ┌─────────┐                                        │
              │ SA-001  │ ← HIGHEST PRIORITY                     │
              │ CI/CD   │   (expedite to 72h)                    │
              └────┬────┘                                        │
                   │                                             │
           ┌───────┴───────┐                                     │
           ▼               ▼                                     │
      ┌─────────┐    ┌─────────┐                                │
      │ IA-001  │    │ SA-002  │ (interim checklist)            │
      │ GSW Upd │    └─────────┘                                │
      └────┬────┘                                               │
           │                                                    │
           ▼                                                    │
      ┌─────────┐         ┌─────────┐                          │
      │ SA-003  │         │ LA-001  │ ← ROOT CAUSE FIX         │
      │ ML Reval│         │ SRD Amd │                          │
      └─────────┘         └────┬────┘                          │
                               │                               │
                    ┌──────────┼──────────┐                    │
                    ▼          ▼          ▼                    │
              ┌─────────┐ ┌─────────┐ ┌─────────┐             │
              │ LA-002  │ │ LA-003  │ │ LA-004  │             │
              │ ML Haz  │ │ Drift   │ │ Proven  │ ────────────┘
              └─────────┘ └─────────┘ └─────────┘    (feedback loop)
```

#### Recommended Priority Ordering

| Priority | Action ID | Timeframe | Rationale |
|----------|-----------|-----------|-----------|
| 1 | SA-001 (basic) | 0-72 hours | Prevent recurrence before any update |
| 2 | IA-002 | 0-24 hours | Enable safe immediate operations |
| 3 | IA-003 | 0-48 hours | Verify no other mismatches |
| 4 | SA-002 | 48-72 hours | Manual backup for SA-001 |
| 5 | IA-001 | 72-96 hours | Update ground after safety gate exists |
| 6 | SA-001 (full) | 1-2 weeks | Complete automation |
| 7 | SA-003 | 2-3 weeks | Requires IA-001 |
| 8 | LA-001 | 4-6 weeks | Root cause formal remediation |
| 9 | LA-003 | 2-3 months | Drift detection infrastructure |
| 10 | LA-002 | 3-4 months | Comprehensive ML hazard analysis |
| 11 | LA-004 | 4-6 months | Full provenance system |

### 2.4 Risk Assessment Validation

#### Immediate Risk: LOW - CONFIRMED

**Rationale:**
- Validation process caught the discrepancy before maneuver execution
- Spacecraft is in stable state with delayed maneuver
- No safety impact occurred
- Defense-in-depth demonstrated effectiveness

**Evidence:** The incident timeline shows discrepancy was flagged at T-0 and maneuver was delayed.

#### Systemic Risk: HIGH - CONFIRMED

**Rationale:**
- Root cause (CM gap) persists across entire ML-augmented navigation system
- Other physics models (gravity harmonics, atmospheric drag, third-body effects) may have similar synchronization gaps
- Unknown failure modes exist per FM-005
- Organizational siloing increases recurrence likelihood

**Evidence:** The CM process PR-SW-102 explicitly allows async versioning. Last compatibility review was 6 months ago.

#### Residual Risk Assessment (Post-Corrective Actions)

Assuming all corrective actions are implemented:

| Risk Type | Initial | Post-Immediate | Post-Short-Term | Post-Long-Term |
|-----------|---------|----------------|-----------------|----------------|
| Immediate | LOW | VERY LOW | VERY LOW | NEGLIGIBLE |
| Systemic | HIGH | MEDIUM-HIGH | MEDIUM | LOW |

**Residual Systemic Risk Drivers (Post-Long-Term):**
- ML model performance degradation between recalibrations
- Undiscovered physics model dependencies
- Organizational memory decay (training, documentation)
- Future capability additions following similar anti-pattern

**Recommended Residual Risk Mitigation:**
- Annual physics model parity audit
- ML model performance monitoring dashboard
- Cross-team review requirement in CM process

---

## 3. Synthesis and Recommendations

### 3.1 Investigation Quality Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Evidence Quality | 4/5 | Strong at proximate levels, moderate at systemic |
| Logical Soundness | 5/5 | 5 Whys chain is valid and complete |
| Root Cause Identification | 5/5 | True root cause (CM gap from ML integration) correctly identified |
| FMEA Calibration | 4/5 | Minor adjustments recommended |
| Corrective Action Coverage | 4/5 | Comprehensive but needs prioritization adjustment |
| Risk Assessment | 5/5 | Accurate immediate and systemic risk levels |

**Overall Investigation Quality: 4.5/5**

### 3.2 Key Recommendations

1. **Expedite SA-001:** Implement basic version compatibility check within 72 hours before executing IA-001. This prevents embedding the anti-pattern.

2. **Add FM-007 to FMEA:** ML model drift without recalibration trigger is a significant latent failure mode not captured in current analysis.

3. **Adjust FM-005 severity:** Increase from S=6 to S=7 to reflect safety-critical nature of unknown ML failure modes.

4. **Establish quantitative success criteria:** Each corrective action should have measurable completion criteria (e.g., "SA-001 complete when 100% of flight/ground releases trigger automatic model coefficient comparison in CI/CD pipeline with documented pass/fail gate").

5. **Track residual risk:** Continue monitoring systemic risk post-corrective actions via quarterly physics model parity audits.

### 3.3 Corrective Action Prioritization (Final)

| Rank | ID | Action | Timeframe |
|------|-----|--------|-----------|
| 1 | SA-001 | Version compatibility CI/CD gate (basic) | 0-72 hours |
| 2 | IA-002 | Calibrated SRP coefficients for operations | 0-24 hours |
| 3 | IA-003 | ML model assumption verification | 0-48 hours |
| 4 | SA-002 | Pre-burn checklist physics comparison | 48-72 hours |
| 5 | IA-001 | Ground system update to v4.2.1 | 72-96 hours |
| 6 | SA-001 | Version compatibility CI/CD gate (full) | 1-2 weeks |
| 7 | SA-003 | ML model revalidation | 2-3 weeks |
| 8 | LA-001 | SRD section 4.3.2 amendment | 4-6 weeks |
| 9 | LA-003 | Physics model drift detection | 2-3 months |
| 10 | LA-002 | ML hazard analysis | 3-4 months |
| 11 | LA-004 | Model provenance tracking | 4-6 months |

---

## 4. Appendices

### Appendix A: Root Cause Confidence Calculation

```
Base confidence from investigation: 88%

Adjustments:
+2% Mathematical verification strongly confirms SRP as cause
+1% No viable alternative explanations
-1% Some procedural evidence is inferred rather than directly observed

Adjusted confidence: 90%
```

### Appendix B: FMEA Recalibration Summary

| ID | Original RPN | Adjusted RPN | Change |
|----|--------------|--------------|--------|
| FM-001 | 144 | 144 | No change |
| FM-002 | 140 | 140 | No change |
| FM-003 | 160 | 160 | No change |
| FM-004 | 196 | 196 | No change |
| FM-005 | 180 | 210 | S increased 6→7 |
| FM-006 | 40 | 40 | No change |
| FM-007 | N/A | 210 | New failure mode added |

### Appendix C: Cost-Benefit Matrix

| Action | Implementation Cost | Operational Cost | Risk Reduction Benefit | Net Value |
|--------|---------------------|------------------|----------------------|-----------|
| SA-001 | MEDIUM | LOW | VERY HIGH | VERY HIGH |
| IA-001 | LOW | NONE | HIGH | HIGH |
| LA-001 | LOW | NONE | VERY HIGH | VERY HIGH |
| LA-003 | HIGH | MEDIUM | HIGH | MEDIUM-HIGH |
| LA-002 | HIGH | LOW | HIGH | MEDIUM-HIGH |

---

## session_context

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "ps-orch-007-test"
  source_agent: "ps-analyst"
  target_agent: "ps-reporter"
  timestamp: "2026-01-12T15:47:00Z"
  analysis_type: "investigation-validation"
  payload:
    investigation_validated: true
    investigation_quality_score: 4.5
    root_cause_confidence_adjusted: 0.90
    root_cause_confirmation: "CM gap introduced when ML-assisted navigation was added without updating synchronization requirements between flight and ground physics models"
    corrective_actions_prioritized:
      - id: "SA-001-basic"
        action: "Version compatibility CI/CD gate (basic)"
        priority: 1
        timeframe: "0-72 hours"
        rationale: "Prevent recurrence before any update"
      - id: "IA-002"
        action: "Use calibrated SRP coefficients"
        priority: 2
        timeframe: "0-24 hours"
        rationale: "Enable safe immediate operations"
      - id: "IA-003"
        action: "Verify ML model assumptions"
        priority: 3
        timeframe: "0-48 hours"
        rationale: "Confirm no other mismatches"
      - id: "SA-002"
        action: "Pre-burn checklist physics comparison"
        priority: 4
        timeframe: "48-72 hours"
        rationale: "Manual backup for SA-001"
      - id: "IA-001"
        action: "Update ground system to v4.2.1"
        priority: 5
        timeframe: "72-96 hours"
        rationale: "Update after safety gate exists"
      - id: "LA-001"
        action: "SRD section 4.3.2 amendment"
        priority: 8
        timeframe: "4-6 weeks"
        rationale: "Root cause formal remediation"
    key_recommendations:
      - "Expedite SA-001 (CI/CD gate) to 72 hours before executing IA-001"
      - "Add FM-007 (ML model drift without recalibration trigger) to FMEA with RPN=210"
      - "Adjust FM-005 severity from S=6 to S=7 (adjusted RPN=210)"
      - "Establish quantitative success criteria for each corrective action"
      - "Implement quarterly physics model parity audits for residual risk monitoring"
    fmea_adjustments:
      - id: "FM-005"
        original_rpn: 180
        adjusted_rpn: 210
        reason: "Severity increased 6→7 for safety-critical ML unknowns"
      - id: "FM-007"
        original_rpn: null
        adjusted_rpn: 210
        reason: "New failure mode: ML model drift without recalibration trigger"
    risk_assessment:
      immediate: "LOW"
      immediate_status: "CONFIRMED"
      systemic: "HIGH"
      systemic_status: "CONFIRMED"
      residual_post_corrective: "LOW"
      residual_drivers:
        - "ML model performance degradation between recalibrations"
        - "Undiscovered physics model dependencies"
        - "Organizational memory decay"
    confidence: 0.92
    evidence_quality: "strong"
```

---

**Document Status:** COMPLETE
**Next Step:** ps-reporter synthesis for stakeholder communication
