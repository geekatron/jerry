# ST-004: Threshold Unification (5-tier SSOT)

> **Type:** story
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-21
> **Due:** --
> **Completed:** 2026-02-21
> **Parent:** FEAT-002
> **Owner:** --

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | User story and scope |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Dependencies](#dependencies) | Relationships |
| [History](#history) | Status changes |

---

## Summary

Jerry's 5-tier threshold system (NOMINAL/LOW/WARNING/CRITICAL/EMERGENCY) replaces jerry-statusline's previous 2-tier color system (warning/critical). Jerry is the SSOT for threshold values. jerry-statusline reads the `thresholds` block from Jerry's JSON response and applies tier-to-color mapping.

**Tier-to-color mapping (jerry-statusline):**
- NOMINAL / LOW → green
- WARNING → yellow
- CRITICAL / EMERGENCY → red

Jerry's config defines threshold values (not hardcoded). The `thresholds` block in `jerry context estimate` output surfaces the actual configured values, enabling statusline to adapt without code changes.

---

## Acceptance Criteria

- [x] Jerry config has 5-tier threshold keys: `context_monitor.nominal_threshold`, `.low_threshold`, `.warning_threshold`, `.critical_threshold`, `.emergency_threshold`
- [x] `jerry context estimate` response includes `thresholds` block with all 5 values
- [x] jerry-statusline reads `thresholds` from Jerry response (not hardcoded)
- [x] Tier-to-color mapping: NOMINAL/LOW=green, WARNING=yellow, CRITICAL/EMERGENCY=red
- [x] Threshold changes in Jerry config propagate to statusline without statusline code changes

---

## Dependencies

**Depends On:**
- EN-009 (ContextEstimate VO includes thresholds block)
- EN-012 (CLI command surfaces thresholds in JSON output)

**Enables:**
- ST-005 (jerry-statusline reads thresholds from Jerry response)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-21 | Claude | completed | 5-tier threshold SSOT in Jerry config. Thresholds block in CLI output. jerry-statusline reads and applies. |
