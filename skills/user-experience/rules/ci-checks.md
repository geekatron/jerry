<!-- VERSION: 3.0.0 | DATE: 2026-03-04 | SOURCE: SKILL.md (skills/user-experience/SKILL.md) Sections "P-003 Compliance", "Wave Transition Quality Gates" | PARENT: /user-experience skill | CI STANDARDS: `.context/rules/quality-enforcement.md` [Enforcement Architecture] L5 layer, `.context/rules/agent-development-standards.md` [H-34] (agent definition schema validation + constitutional compliance sub-item b) | ITERATION: 4 (C4 quality revision — fixes UX-CI-009 column-specific grep, UX-CI-012 tautological traceability check, UX-CI-013 awk heading boundary; adds CI runner integration section) -->

# CI Checks Rules

> CI/CD verification rules for the /user-experience skill. Defines 13 automated checks for P-003 enforcement, schema validation, wave gate compliance, trigger map validation, and output quality verification. Every gate has: description, scope, pass/fail criteria, implementation pattern (bash script), and source traceability. See also: `skills/user-experience/rules/wave-progression.md` (wave signoff validation criteria consumed by UX-CI-007/UX-CI-008), `skills/user-experience/rules/synthesis-validation.md` (synthesis confidence gates consumed by UX-CI-011 through UX-CI-013; `[Required Traceability]` defines finding ID format `{PREFIX}-{NNN}` consumed by UX-CI-012), `skills/user-experience/rules/mcp-coordination.md` (MCP ownership validation consumed by UX-CI-007 kickoff signoff). CI standards: `.context/rules/quality-enforcement.md` [Enforcement Architecture] L5 layer, `.context/rules/agent-development-standards.md` [H-34] (schema validation + constitutional compliance).

## Document Sections

| Section | Purpose |
|---------|---------|
| [P-003 Enforcement](#p-003-enforcement) | No sub-skill agent has Agent tool access (UX-CI-001, UX-CI-002, UX-CI-003) |
| [Schema Validation](#schema-validation) | Governance YAML validation against JSON Schema (UX-CI-004, UX-CI-005, UX-CI-006) |
| [Wave Gate Compliance](#wave-gate-compliance) | Signoff file existence and structure verification (UX-CI-007, UX-CI-008) |
| [Trigger Map Validation](#trigger-map-validation) | Keyword collision detection for new sub-skills (UX-CI-009, UX-CI-010) |
| [Output Quality Checks](#output-quality-checks) | Confidence classification and traceability verification (UX-CI-011, UX-CI-012, UX-CI-013) |
| [CI Gate Summary](#ci-gate-summary) | All 13 gates with pass/fail criteria and source traceability |
| [CI Runner Integration](#ci-runner-integration) | Master script template for running all 13 gates as a single CI suite |
| [References](#references) | Source document traceability (10 sources) |

---

## P-003 Enforcement

<!-- Source: SKILL.md Section "P-003 Compliance" -- single-level nesting enforcement. -->
<!-- Source: H-34 (agent-development-standards.md [Agent Definition Schema], compound -- includes constitutional compliance sub-item b), H-01 (P-003). -->

The `/user-experience` skill enforces strict single-level nesting per H-01/P-003. Only `ux-orchestrator` has Agent tool access (T5 tier). All 10 sub-skill agents are workers that MUST NOT include Agent in their tool list.

### UX-CI-001: Agent Tool Grep

<!-- Source: H-01 (P-003), H-34 (agent-development-standards.md [H-35 sub-item b] -- workers MUST NOT include Agent in tools frontmatter). -->

**Check:** Scan all sub-skill agent `.md` files for Agent tool presence in `tools:` frontmatter.

**Scope:** All files matching `skills/ux-*/agents/*.md` (excludes `skills/user-experience/agents/ux-orchestrator.md`).

**Pass criteria:** Zero matches for `Agent` in the `tools:` YAML frontmatter field of any sub-skill agent file.

**Implementation pattern:**

```bash
# UX-CI-001: Agent Tool Grep
# Source: H-01 (P-003), H-34(b) (constitutional compliance -- workers MUST NOT have Agent)
# Extract tools frontmatter between first two --- delimiters and check for Agent
for agent_file in skills/ux-*/agents/*.md; do
  # Skip the orchestrator (T5, allowed to have Agent)
  if [[ "$agent_file" == *"ux-orchestrator"* ]]; then
    continue
  fi
  # Extract YAML frontmatter only (between first and second --- delimiters)
  # Using sed to capture content between line 1 (first ---) and the next ---
  frontmatter=$(sed -n '1,/^---$/{ /^---$/!p; }' "$agent_file" | sed '1d')
  tools_line=$(echo "$frontmatter" | grep -E '^tools:' | head -1)
  if echo "$tools_line" | grep -q 'Agent'; then
    echo "FAIL: $agent_file contains Agent in tools frontmatter (P-003 violation)"
    exit 1
  fi
  # Also check multi-line tools array format
  tools_block=$(echo "$frontmatter" | sed -n '/^tools:/,/^[a-z]/p')
  if echo "$tools_block" | grep -qE '^\s+-\s+Agent\b'; then
    echo "FAIL: $agent_file contains Agent in tools array (P-003 violation)"
    exit 1
  fi
done
echo "PASS: No sub-skill agent has Agent tool access"
```

### UX-CI-002: disallowedTools Declaration

<!-- Source: H-34(b) (agent-development-standards.md [H-35 sub-item b] -- constitutional compliance enforcement via disallowedTools). -->

**Check:** All sub-skill agents declare `disallowedTools: [Agent]` in their `.md` frontmatter.

**Scope:** All files matching `skills/ux-*/agents/*.md` (excludes `ux-orchestrator`).

**Pass criteria:** Every sub-skill agent `.md` file contains `disallowedTools` with `Agent` listed.

**Implementation pattern:**

```bash
# UX-CI-002: disallowedTools Declaration
# Source: H-34(b) (constitutional compliance -- workers declare disallowedTools: [Agent])
for agent_file in skills/ux-*/agents/*.md; do
  if [[ "$agent_file" == *"ux-orchestrator"* ]]; then
    continue
  fi
  # Extract frontmatter between first two --- delimiters
  frontmatter=$(sed -n '1,/^---$/{ /^---$/!p; }' "$agent_file" | sed '1d')
  # Check for disallowedTools containing Agent (inline format or array format)
  if ! echo "$frontmatter" | grep -A 5 'disallowedTools' | grep -q 'Agent'; then
    echo "FAIL: $agent_file missing disallowedTools: [Agent] (P-003 enforcement)"
    exit 1
  fi
done
echo "PASS: All sub-skill agents declare disallowedTools: [Agent]"
```

### UX-CI-003: Forbidden Actions P-003

<!-- Source: H-34(b) (agent-development-standards.md [Guardrails Template] -- minimum 3 forbidden_actions entries referencing P-003, P-020, P-022). -->

**Check:** All sub-skill agent `.governance.yaml` files include the constitutional triplet (P-003, P-020, P-022) in `capabilities.forbidden_actions` with minimum 3 entries per H-34(b).

**Scope:** All files matching `skills/ux-*/agents/*.governance.yaml`.

**Pass criteria:** Every `.governance.yaml` file under `skills/ux-*/agents/` contains at least 3 entries in `capabilities.forbidden_actions`, with at least one entry referencing each of P-003, P-020, and P-022.

**Implementation pattern:**

```bash
# UX-CI-003: Forbidden Actions P-003
# Source: H-34(b) (constitutional compliance -- min 3 forbidden_actions with P-003, P-020, P-022)
for yaml_file in skills/ux-*/agents/*.governance.yaml; do
  [ -f "$yaml_file" ] || continue
  # Count forbidden_actions array entries (lines starting with "  - " under forbidden_actions:)
  # Use sed to extract only the forbidden_actions block, then count array entries
  fa_block=$(sed -n '/^\s*forbidden_actions:/,/^\s*[a-z_][a-z_]*:/{ /^\s*forbidden_actions:/d; /^\s*[a-z_][a-z_]*:/d; p; }' "$yaml_file")
  fa_count=$(echo "$fa_block" | grep -c '^\s*-' || true)
  if [ "$fa_count" -lt 3 ]; then
    echo "FAIL: $yaml_file has fewer than 3 forbidden_actions entries (found $fa_count, required >= 3)"
    exit 1
  fi
  # Verify each constitutional principle is referenced within the forbidden_actions block
  for principle in "P-003" "P-020" "P-022"; do
    if ! echo "$fa_block" | grep -q "$principle"; then
      echo "FAIL: $yaml_file missing $principle in capabilities.forbidden_actions"
      exit 1
    fi
  done
done
echo "PASS: All governance files include constitutional triplet in forbidden_actions (>= 3 entries)"
```

---

## Schema Validation

<!-- Source: H-34 (agent-development-standards.md [Agent Definition Schema] -- dual-file architecture, governance YAML validation against JSON Schema). -->

### UX-CI-004: Governance YAML Schema

<!-- Source: H-34 (agent-development-standards.md [Agent Definition Schema] -- "Governance schema validation MUST execute before LLM-based quality scoring for C2+ deliverables"). Tool: check-jsonschema per H-05 (UV-only Python -- uv run for all execution). -->

**Check:** All governance YAML files validate against the canonical JSON Schema.

**Scope:** All files matching `skills/ux-*/agents/*.governance.yaml` AND `skills/user-experience/agents/*.governance.yaml`.

**Schema:** `docs/schemas/agent-governance-v1.schema.json`

**Pass criteria:** Zero validation errors across all governance YAML files.

**Implementation pattern:**

```bash
# UX-CI-004: Governance YAML Schema Validation
# Source: H-34 (agent-development-standards.md [Agent Definition Schema])
# Tool: check-jsonschema via uv run per H-05 (UV-only Python execution)
schema_file="docs/schemas/agent-governance-v1.schema.json"
if [ ! -f "$schema_file" ]; then
  echo "FAIL: Schema file not found: $schema_file"
  exit 1
fi
for yaml_file in skills/ux-*/agents/*.governance.yaml skills/user-experience/agents/*.governance.yaml; do
  [ -f "$yaml_file" ] || continue
  if ! uv run check-jsonschema --schemafile "$schema_file" "$yaml_file"; then
    echo "FAIL: $yaml_file fails schema validation against $schema_file"
    exit 1
  fi
done
echo "PASS: All governance YAML files validate against $schema_file"
```

### UX-CI-005: Required Governance Fields

<!-- Source: H-34 (agent-development-standards.md [Governance Fields (`.governance.yaml` file)] -- required fields table: version, tool_tier, identity.role, identity.expertise, identity.cognitive_mode, constitution.principles_applied, capabilities.forbidden_actions). -->

**Check:** All governance YAML files contain the minimum required fields per `agent-development-standards.md` [Governance Fields] required fields table.

**Scope:** All files matching `skills/ux-*/agents/*.governance.yaml` AND `skills/user-experience/agents/*.governance.yaml`.

**Required fields:**
- `version` (semantic versioning pattern `^\d+\.\d+\.\d+$`)
- `tool_tier` (T1-T5 enum)
- `identity.role` (non-empty string)
- `identity.expertise` (array, min 2 entries)
- `identity.cognitive_mode` (enum: divergent, convergent, integrative, systematic, forensic)
- `constitution.principles_applied` (array, min 3 entries, MUST include P-003, P-020, P-022)
- `capabilities.forbidden_actions` (array, min 3 entries)

**Implementation pattern:**

```bash
# UX-CI-005: Required Governance Fields
# Source: H-34 (agent-development-standards.md [Governance Fields] required fields table)
for yaml_file in skills/ux-*/agents/*.governance.yaml skills/user-experience/agents/*.governance.yaml; do
  [ -f "$yaml_file" ] || continue
  # Check version field exists and matches semver pattern
  if ! grep -qE '^version:\s+"?[0-9]+\.[0-9]+\.[0-9]+"?' "$yaml_file"; then
    echo "FAIL: $yaml_file missing or invalid version (must be semver per AD-M-002)"
    exit 1
  fi
  # Check tool_tier field exists and is T1-T5
  if ! grep -qE '^tool_tier:\s+"?T[1-5]"?' "$yaml_file"; then
    echo "FAIL: $yaml_file missing or invalid tool_tier (must be T1-T5 per agent-development-standards.md [Tool Security Tiers])"
    exit 1
  fi
  # Check identity.role exists (non-empty string under identity block)
  identity_block=$(sed -n '/^identity:/,/^[a-z]/p' "$yaml_file")
  if ! echo "$identity_block" | grep -qE '^\s+role:\s+".+"'; then
    echo "FAIL: $yaml_file missing identity.role (required per H-34)"
    exit 1
  fi
  # Check identity.expertise has at least 2 entries (AD-M-005)
  expertise_count=$(echo "$identity_block" | sed -n '/expertise:/,/^\s*[a-z]/p' | grep -c '^\s*-' || true)
  if [ "$expertise_count" -lt 2 ]; then
    echo "FAIL: $yaml_file has fewer than 2 identity.expertise entries (found $expertise_count, required >= 2 per AD-M-005)"
    exit 1
  fi
  # Check identity.cognitive_mode is valid enum
  if ! echo "$identity_block" | grep -qE 'cognitive_mode:\s+"?(divergent|convergent|integrative|systematic|forensic)"?'; then
    echo "FAIL: $yaml_file missing or invalid identity.cognitive_mode (must be one of: divergent, convergent, integrative, systematic, forensic)"
    exit 1
  fi
  # Check constitution.principles_applied has at least 3 entries including P-003, P-020, P-022
  principles_block=$(sed -n '/principles_applied:/,/^[a-z]/p' "$yaml_file")
  principles_count=$(echo "$principles_block" | grep -c '^\s*-' || true)
  if [ "$principles_count" -lt 3 ]; then
    echo "FAIL: $yaml_file has fewer than 3 constitution.principles_applied entries (found $principles_count)"
    exit 1
  fi
  for principle in "P-003" "P-020" "P-022"; do
    if ! echo "$principles_block" | grep -q "$principle"; then
      echo "FAIL: $yaml_file missing $principle in constitution.principles_applied (required per H-34(b))"
      exit 1
    fi
  done
  # Check capabilities.forbidden_actions has at least 3 entries (overlaps UX-CI-003; checked here for field presence)
  fa_block=$(sed -n '/forbidden_actions:/,/^\s*[a-z_]*:/{ /forbidden_actions:/d; /^\s*[a-z_]*:/d; p; }' "$yaml_file")
  fa_count=$(echo "$fa_block" | grep -c '^\s*-' || true)
  if [ "$fa_count" -lt 3 ]; then
    echo "FAIL: $yaml_file has fewer than 3 capabilities.forbidden_actions entries (found $fa_count, required >= 3 per H-34(b))"
    exit 1
  fi
done
echo "PASS: All governance files contain required fields with valid values"
```

### UX-CI-006: Frontmatter-Governance Consistency

<!-- Source: H-34 (agent-development-standards.md [H-34 Architecture Note] -- dual-file architecture requires .md name field to match .governance.yaml filename pattern for agent discovery and governance pairing). -->

**Check:** The `.md` frontmatter `name` field matches the `.governance.yaml` filename pattern, ensuring dual-file architecture integrity.

**Scope:** All agent dual-file pairs under `skills/ux-*/agents/` and `skills/user-experience/agents/`.

**Pass criteria:** For each agent, the `.md` `name` field equals the `.governance.yaml` filename without the `.governance.yaml` extension. Every `.governance.yaml` file has a corresponding `.md` file.

**Implementation pattern:**

```bash
# UX-CI-006: Frontmatter-Governance Consistency
# Source: H-34 (agent-development-standards.md [H-34 Architecture Note] -- dual-file architecture)
for yaml_file in skills/ux-*/agents/*.governance.yaml skills/user-experience/agents/*.governance.yaml; do
  [ -f "$yaml_file" ] || continue
  # Derive expected name from governance filename (strip path and .governance.yaml)
  expected_name=$(basename "$yaml_file" .governance.yaml)
  # Find corresponding .md file
  md_file="${yaml_file%.governance.yaml}.md"
  if [ ! -f "$md_file" ]; then
    echo "FAIL: No matching .md file for $yaml_file (expected $md_file per H-34 dual-file architecture)"
    exit 1
  fi
  # Extract name field from .md YAML frontmatter (between first two --- delimiters)
  actual_name=$(sed -n '2,/^---$/p' "$md_file" | grep -E '^name:\s+' | head -1 | sed 's/^name:\s*//' | tr -d '"' | tr -d "'" | xargs)
  if [ "$actual_name" != "$expected_name" ]; then
    echo "FAIL: $md_file name '$actual_name' does not match governance filename '$expected_name' (H-34 dual-file consistency)"
    exit 1
  fi
done
# Reverse check: every .md file should have a .governance.yaml
for md_file in skills/ux-*/agents/*.md skills/user-experience/agents/*.md; do
  [ -f "$md_file" ] || continue
  yaml_file="${md_file%.md}.governance.yaml"
  if [ ! -f "$yaml_file" ]; then
    echo "FAIL: No matching .governance.yaml for $md_file (expected $yaml_file per H-34 dual-file architecture)"
    exit 1
  fi
done
echo "PASS: All agent name fields match governance filenames (dual-file pairs consistent)"
```

---

## Wave Gate Compliance

<!-- Source: skills/user-experience/rules/wave-progression.md [Signoff Requirements] -- signoff file validation criteria. See also: skills/user-experience/rules/wave-progression.md [Wave State Tracking] for file-to-state mapping. Threshold (0.85): wave-progression.md [Wave Transition Gates] Section "Threshold". -->

### UX-CI-007: Signoff File Structure

<!-- Source: wave-progression.md [Signoff Requirements], [Signoff File Validation]. Threshold 0.85: wave-progression.md [Wave Transition Gates] Section "Threshold" (distinct from H-13's 0.92 per ADR-PROJ022-002). MCP ownership: wave-progression.md [Wave Definitions] Wave 0->1 entry criteria ("KICKOFF-SIGNOFF.md completed with MCP ownership assignments"). -->

**Check:** When a `WAVE-N-SIGNOFF.md` or `KICKOFF-SIGNOFF.md` file exists, it contains all required fields.

**Scope:** Files matching `skills/user-experience/output/*SIGNOFF*.md`.

**Required fields for KICKOFF-SIGNOFF.md:**
- Date (non-empty)
- Signed off by (non-empty)
- Foundation artifacts verified table (all rows present)
- MCP ownership assignments present (required per wave-progression.md Wave 0->1 entry criteria)
- Acceptance criteria checklist (all items checked)
- Authorization field (YES or NO)

**Required fields for WAVE-N-SIGNOFF.md:**
- Date (non-empty)
- Wave number (matches filename)
- Signed off by (non-empty)
- Sub-skills deployed table (all sub-skills for that wave listed)
- Quality gate composite score (>= 0.85 per wave-progression.md [Wave Transition Gates])
- Artifacts verified table (all artifacts for that wave listed)
- Acceptance criteria checklist (all items checked)
- Authorization field (YES or NO)

**Implementation pattern:**

```bash
# UX-CI-007: Signoff File Structure
# Source: wave-progression.md [Signoff Requirements], [Signoff File Validation]
# Threshold 0.85: wave-progression.md [Wave Transition Gates] (distinct from H-13's 0.92)
signoff_dir="skills/user-experience/output"
for signoff_file in "$signoff_dir"/*SIGNOFF*.md; do
  [ -f "$signoff_file" ] || continue
  filename=$(basename "$signoff_file")

  # Check Date field is non-empty
  if ! grep -qE '^\*\*Date:\*\*\s+\S' "$signoff_file"; then
    echo "FAIL: $signoff_file has empty or missing Date field"
    exit 1
  fi
  # Check Signed off by field is non-empty
  if ! grep -qE '^\*\*Signed off by:\*\*\s+\S' "$signoff_file"; then
    echo "FAIL: $signoff_file has empty or missing Signed off by field"
    exit 1
  fi
  # Check Authorization field contains YES or NO
  if ! grep -qE '(authorized|Authorization).*:\s*(YES|NO)' "$signoff_file"; then
    echo "FAIL: $signoff_file missing Authorization field (must be YES or NO)"
    exit 1
  fi
  # Check all acceptance criteria checkboxes are checked
  unchecked=$(grep -c '\- \[ \]' "$signoff_file" || true)
  if [ "$unchecked" -gt 0 ]; then
    echo "FAIL: $signoff_file has $unchecked unchecked acceptance criteria"
    exit 1
  fi

  # KICKOFF-specific checks
  if [[ "$filename" == "KICKOFF-SIGNOFF.md" ]]; then
    # Check MCP ownership assignments are present (wave-progression.md Wave 0->1 entry criteria)
    if ! grep -qiE '(MCP ownership|MCP.*assignment)' "$signoff_file"; then
      echo "FAIL: $signoff_file missing MCP ownership assignments (required per wave-progression.md Wave 0->1 entry criteria)"
      exit 1
    fi
  fi

  # Wave-specific checks
  if [[ "$filename" == WAVE-*-SIGNOFF.md ]]; then
    # Extract wave number from filename
    wave_num=$(echo "$filename" | sed 's/WAVE-\([0-9]\)-SIGNOFF.md/\1/')
    # Verify Wave number field matches filename
    if ! grep -qE '^\*\*Wave:\*\*\s+'"$wave_num" "$signoff_file"; then
      echo "FAIL: $signoff_file Wave number does not match filename (expected $wave_num)"
      exit 1
    fi
    # Verify quality gate composite score exists and is >= 0.85
    # Threshold source: wave-progression.md [Wave Transition Gates] Section "Threshold"
    score=$(grep -oE 'Composite score:\*\*\s+[0-9]+\.[0-9]+' "$signoff_file" | grep -oE '[0-9]+\.[0-9]+' | head -1)
    if [ -z "$score" ]; then
      echo "FAIL: $signoff_file missing quality gate composite score"
      exit 1
    fi
    # Compare score >= 0.85 using awk (portable decimal comparison)
    if ! echo "$score" | awk '{exit ($1 >= 0.85) ? 0 : 1}'; then
      echo "FAIL: $signoff_file quality gate composite score $score < 0.85 (threshold per wave-progression.md)"
      exit 1
    fi
    # Verify no FAILED status in sub-skills table
    if grep -qE '\|\s*FAILED\s*\|' "$signoff_file"; then
      echo "FAIL: $signoff_file contains FAILED sub-skill deployment status"
      exit 1
    fi
  fi
done
echo "PASS: All signoff files have valid structure"
```

### UX-CI-008: Signoff Ordering

<!-- Source: wave-progression.md [Wave State Tracking] -- sequential signoff file existence determines wave authorization. Bypass: wave-progression.md [Bypass Mechanism]. -->

**Check:** No WAVE-N-SIGNOFF.md exists without WAVE-(N-1)-SIGNOFF.md existing first. Sequential ordering enforces wave-progression.md [Wave State Tracking] authorization chain.

**Scope:** Files in `skills/user-experience/output/`.

**Pass criteria:** Signoff files exist in sequential order. WAVE-2-SIGNOFF.md cannot exist without WAVE-1-SIGNOFF.md.

**Exception:** Wave bypass documentation (`wave-bypass-{wave-N}.md`) may exist without the preceding signoff, but carries the bypass warning banner per wave-progression.md [Bypass Constraints].

**Implementation pattern:**

```bash
# UX-CI-008: Signoff Ordering
# Source: wave-progression.md [Wave State Tracking] -- sequential authorization chain
# Bypass: wave-progression.md [Bypass Mechanism]
signoff_dir="skills/user-experience/output"
for wave in 2 3 4 5; do
  prev_wave=$((wave - 1))
  current_file="$signoff_dir/WAVE-${wave}-SIGNOFF.md"
  prev_file="$signoff_dir/WAVE-${prev_wave}-SIGNOFF.md"
  if [ -f "$current_file" ] && [ ! -f "$prev_file" ]; then
    # Check for bypass documentation
    bypass_file="$signoff_dir/wave-bypass-wave-${prev_wave}.md"
    if [ -f "$bypass_file" ]; then
      echo "WARNING: WAVE-${wave}-SIGNOFF.md exists without WAVE-${prev_wave}-SIGNOFF.md (bypass documented at $bypass_file)"
    else
      echo "FAIL: WAVE-${wave}-SIGNOFF.md exists without WAVE-${prev_wave}-SIGNOFF.md (no bypass documentation found)"
      exit 1
    fi
  fi
done
# Wave 1 requires KICKOFF-SIGNOFF.md (Wave 0 -> 1 transition)
if [ -f "$signoff_dir/WAVE-1-SIGNOFF.md" ] && [ ! -f "$signoff_dir/KICKOFF-SIGNOFF.md" ]; then
  echo "FAIL: WAVE-1-SIGNOFF.md exists without KICKOFF-SIGNOFF.md (Wave 0->1 prerequisite)"
  exit 1
fi
echo "PASS: Signoff files exist in sequential order"
```

---

## Trigger Map Validation

<!-- Source: agent-routing-standards.md [Enhanced Trigger Map] and RT-M-004 -- keyword collision detection when new keywords are added. mandatory-skill-usage.md [Trigger Map] defines the /user-experience row. -->

### UX-CI-009: Keyword Collision Check

<!-- Source: agent-routing-standards.md RT-M-004 ("When new keywords are added to the trigger map, they SHOULD be cross-referenced against all existing skills to identify collisions"). -->
<!-- Asymmetry caveat: SKILL.md (skills/user-experience/SKILL.md) lines 50-54 document that activation-keywords (19 entries) intentionally differ from mandatory-skill-usage.md trigger map keywords (21 entries). activation-keywords are discovery-optimized (H-26); trigger map keywords are routing-optimized (H-36b). This gate checks the trigger map's Detected Keywords column (column 2) against other skills' Detected Keywords columns — NOT activation-keywords from sub-skill SKILL.md files — because the purpose is to detect routing collisions in the trigger map itself. See agent-routing-standards.md [Enhanced Trigger Map] for the 5-column format specification. -->

**Check:** When a new sub-skill is added (detected by new `skills/ux-*/SKILL.md` file in PR diff), verify that the `/user-experience` trigger map row's positive keywords do not collide with other skills' positive keywords in `mandatory-skill-usage.md`.

**Scope:** The `/user-experience` row in `.context/rules/mandatory-skill-usage.md`, cross-referenced against all other skill rows.

**Data source:** This gate extracts keywords from the trigger map's Detected Keywords column (column 2 of the pipe-delimited table), not from sub-skill SKILL.md `activation-keywords` fields. These differ by design (see SKILL.md lines 50-54): activation-keywords serve agent discovery (H-26), while trigger map keywords serve routing disambiguation (H-36b). Checking the trigger map column directly ensures the collision check operates on the same data the routing algorithm uses.

**Implementation approach:**
1. Extract positive keywords from the `/user-experience` row's Detected Keywords column (column 2) in `mandatory-skill-usage.md`.
2. Extract positive keywords from each other skill's Detected Keywords column (column 2).
3. Flag any keyword that appears in another skill's positive keywords without being mitigated by that skill's negative keywords (column 3) or the `/user-experience` row's negative keywords (column 3).

**Pass criteria:** Zero unmitigated collisions. Collisions are mitigated by adding the colliding keyword to the appropriate negative keywords list.

**Implementation pattern:**

```bash
# UX-CI-009: Keyword Collision Check
# Source: agent-routing-standards.md RT-M-004 (cross-reference new keywords against existing skills)
# Data source: trigger map Detected Keywords column (column 2), NOT activation-keywords from SKILL.md
# Rationale: activation-keywords differ from trigger map keywords by design (SKILL.md lines 50-54);
#   activation-keywords are discovery-optimized, trigger map keywords are routing-optimized.
#   Collision check must use the same data the routing algorithm consumes.
trigger_map=".context/rules/mandatory-skill-usage.md"
if [ ! -f "$trigger_map" ]; then
  echo "WARNING: Trigger map not found at $trigger_map"
  exit 0
fi
collision_count=0
# Extract the /user-experience row's Detected Keywords (column 2 of pipe-delimited table)
ux_row=$(grep '/user-experience' "$trigger_map" | head -1)
if [ -z "$ux_row" ]; then
  echo "WARNING: /user-experience row not found in trigger map"
  exit 0
fi
ux_keywords=$(echo "$ux_row" | awk -F'|' '{print $2}' | tr ',' '\n' | sed 's/^\s*//; s/\s*$//' | tr '[:upper:]' '[:lower:]')
ux_neg_keywords=$(echo "$ux_row" | awk -F'|' '{print $3}' | tr ',' '\n' | sed 's/^\s*//; s/\s*$//' | tr '[:upper:]' '[:lower:]')
# Extract all other skill rows (pipe-delimited table rows with a / skill reference, excluding /user-experience)
other_rows=$(grep -E '^\|.*\|.*\|.*\|.*\|.*/' "$trigger_map" | grep -v '/user-experience' | grep -v '^| Detected' | grep -v '^|---')
while IFS= read -r ux_keyword; do
  # Skip empty or short keywords (< 4 chars are too generic for collision detection)
  [ -z "$ux_keyword" ] && continue
  [ ${#ux_keyword} -lt 4 ] && continue
  # Check each other skill row's Detected Keywords column (column 2) for this keyword
  while IFS= read -r other_row; do
    [ -z "$other_row" ] && continue
    other_detected=$(echo "$other_row" | awk -F'|' '{print $2}' | tr '[:upper:]' '[:lower:]')
    other_neg=$(echo "$other_row" | awk -F'|' '{print $3}' | tr '[:upper:]' '[:lower:]')
    other_skill=$(echo "$other_row" | awk -F'|' '{print $NF}' | xargs)
    # Check if keyword appears in the other skill's Detected Keywords column
    if echo "$other_detected" | grep -qi "$ux_keyword"; then
      # Check if mitigated: keyword in /user-experience negative keywords or other skill's negative keywords
      mitigated=false
      if echo "$ux_neg_keywords" | grep -qi "$ux_keyword"; then
        mitigated=true
      fi
      if echo "$other_neg" | grep -qi "user experience\|UX\|usability\|design system"; then
        mitigated=true
      fi
      if [ "$mitigated" = false ]; then
        echo "WARNING: Keyword '$ux_keyword' from /user-experience collides with $other_skill Detected Keywords column"
        collision_count=$((collision_count + 1))
      fi
    fi
  done <<< "$other_rows"
done <<< "$ux_keywords"
if [ "$collision_count" -gt 0 ]; then
  echo "WARNING: $collision_count unmitigated keyword collisions detected (review per RT-M-004)"
else
  echo "PASS: No keyword collisions detected in trigger map Detected Keywords columns"
fi
```

### UX-CI-010: Negative Keyword Coverage

<!-- Source: agent-routing-standards.md RT-M-001 ("Every skill with > 5 positive keywords SHOULD define negative keywords to prevent false-positive routing"). mandatory-skill-usage.md [Trigger Map] defines the /user-experience row with 21 positive keywords. -->

**Check:** The `/user-experience` trigger map row in `mandatory-skill-usage.md` has negative keywords for all skills with > 5 positive keywords (per RT-M-001).

**Scope:** The `/user-experience` row in `.context/rules/mandatory-skill-usage.md`.

**Pass criteria:** Negative keywords list is non-empty for the `/user-experience` row (which has > 5 positive keywords).

**Implementation pattern:**

```bash
# UX-CI-010: Negative Keyword Coverage
# Source: agent-routing-standards.md RT-M-001 (skills with > 5 positive keywords need negative keywords)
trigger_map=".context/rules/mandatory-skill-usage.md"
if [ ! -f "$trigger_map" ]; then
  echo "WARNING: Trigger map not found at $trigger_map"
  exit 0
fi
ux_row=$(grep '/user-experience' "$trigger_map" | head -1)
if [ -z "$ux_row" ]; then
  echo "WARNING: /user-experience row not found in trigger map (expected per H-22, H-26)"
  exit 0  # Warning gate, not blocking
fi
# Extract negative keywords column (column 3 in 5-column pipe-delimited format)
neg_keywords=$(echo "$ux_row" | awk -F'|' '{print $3}' | xargs)
if [ -z "$neg_keywords" ] || [ "$neg_keywords" = "--" ]; then
  echo "WARNING: /user-experience has empty negative keywords (RT-M-001 requires negative keywords for skills with > 5 positive keywords)"
else
  # Count negative keywords to verify reasonable coverage
  neg_count=$(echo "$neg_keywords" | tr ',' '\n' | wc -l | xargs)
  echo "PASS: /user-experience has $neg_count negative keywords defined"
fi
```

---

## Output Quality Checks

<!-- Source: SKILL.md (skills/user-experience/SKILL.md) Sections "Synthesis Hypothesis Validation", "Cross-Framework Synthesis Protocol" -- synthesis output quality enforcement. See also: skills/user-experience/rules/synthesis-validation.md [Synthesis Output Structure] for required sections and format, [Confidence Classification] for gate definitions, [Required Traceability] for finding ID format ({PREFIX}-{NNN}). Output filename convention: `ux-orchestrator-synthesis.md` for standard synthesis, `ux-orchestrator-crisis.md` for CRISIS mode, per SKILL.md `{topic-slug}` naming convention. -->

### UX-CI-011: Confidence Classification Presence

<!-- Source: synthesis-validation.md [Confidence Classification] -- all synthesis hypotheses MUST include confidence classification (HIGH/MEDIUM/LOW) per P-022. Gate enforcement: synthesis-validation.md [Gate Enforcement Mechanisms]. -->

**Check:** All synthesis output files contain confidence classifications for every finding.

**Scope:** Files matching `skills/user-experience/output/*/ux-orchestrator-synthesis.md` and `skills/user-experience/output/*/ux-orchestrator-crisis.md`.

**Pass criteria:** Every finding row in the output (matching pattern `| {PREFIX}-{NNN}`) includes a confidence classification (HIGH, MEDIUM, or LOW) per synthesis-validation.md [Confidence Classification].

**Implementation pattern:**

```bash
# UX-CI-011: Confidence Classification Presence
# Source: synthesis-validation.md [Confidence Classification] -- P-022 compliance
# Finding ID format: {PREFIX}-{NNN} per synthesis-validation.md [Required Traceability]
for synthesis_file in skills/user-experience/output/*/ux-orchestrator-synthesis.md \
                      skills/user-experience/output/*/ux-orchestrator-crisis.md; do
  [ -f "$synthesis_file" ] || continue
  # Count finding rows (table rows containing finding IDs like HE-001, BD-002, CONTRA-001)
  finding_count=$(grep -cE '^\|.*[A-Z]{2,}-[0-9]{3}' "$synthesis_file" || true)
  if [ "$finding_count" -eq 0 ]; then
    echo "WARNING: $synthesis_file contains no findings to check"
    continue
  fi
  # Count finding rows that do NOT have HIGH, MEDIUM, or LOW classification
  unclassified=$(grep -E '^\|.*[A-Z]{2,}-[0-9]{3}' "$synthesis_file" | grep -vcE '(HIGH|MEDIUM|LOW)' || true)
  if [ "$unclassified" -gt 0 ]; then
    echo "WARNING: $synthesis_file has $unclassified of $finding_count findings without confidence classification (P-022 violation)"
  else
    echo "INFO: $synthesis_file -- all $finding_count findings have confidence classification"
  fi
done
echo "PASS: Confidence classification check complete"
```

### UX-CI-012: Traceability

<!-- Source: synthesis-validation.md [Required Traceability] -- every finding MUST include: source sub-skill name (e.g., /ux-heuristic-eval), source finding ID (e.g., HE-003), engagement ID, and confidence classification. Finding ID format: {PREFIX}-{NNN} where PREFIX is 2+ uppercase letters and NNN is a 3-digit number. -->

**Check:** All findings in synthesis outputs trace back to a source sub-skill and include a source finding ID.

**Scope:** Files matching `skills/user-experience/output/*/ux-orchestrator-synthesis.md` and `skills/user-experience/output/*/ux-orchestrator-crisis.md`.

**Pass criteria:** Every finding row includes a source sub-skill name (matching `/ux-*` pattern) and a source finding ID (matching `{PREFIX}-{NNN}` pattern, e.g., `HE-003`, `BD-001`, `CONTRA-001` per synthesis-validation.md [Required Traceability]).

**Implementation pattern:**

The traceability check uses a two-pass column-aware approach to avoid the tautological pattern where the row selection regex and the verification regex are identical. Pass 1 verifies each finding row contains a `/ux-[a-z-]+` sub-skill reference. Pass 2 verifies each finding row contains at least two distinct `{PREFIX}-{NNN}` patterns: the row's own finding ID (the synthesis-level ID, e.g., `CONV-001`) and a source finding ID from the originating sub-skill (e.g., `HE-003`). A single `{PREFIX}-{NNN}` match means only the row's own ID exists, with no source traceability.

```bash
# UX-CI-012: Traceability
# Source: synthesis-validation.md [Required Traceability]
# Finding ID format: {PREFIX}-{NNN} (2+ uppercase letters, dash, 3 digits)
# Source sub-skill format: /ux-{name} (e.g., /ux-heuristic-eval)
#
# Two-pass column-aware verification:
#   Pass 1: Each finding row contains a /ux-[a-z-]+ sub-skill reference
#   Pass 2: Each finding row contains >= 2 distinct {PREFIX}-{NNN} patterns
#           (the row's own synthesis ID + at least one source finding ID)
#   This avoids the tautological check where row selection and verification
#   use the same regex (which always yields 0 missing).
for synthesis_file in skills/user-experience/output/*/ux-orchestrator-synthesis.md \
                      skills/user-experience/output/*/ux-orchestrator-crisis.md; do
  [ -f "$synthesis_file" ] || continue
  # Extract finding rows (table rows containing finding IDs)
  finding_lines=$(grep -E '^\|.*[A-Z]{2,}-[0-9]{3}' "$synthesis_file" || true)
  if [ -z "$finding_lines" ]; then
    continue
  fi
  finding_count=$(echo "$finding_lines" | wc -l | xargs)

  # Pass 1: Check each finding row references a /ux- sub-skill name
  no_subskill=$(echo "$finding_lines" | grep -vcE '/ux-[a-z-]+' || true)
  if [ "$no_subskill" -gt 0 ]; then
    echo "WARNING: $synthesis_file has $no_subskill of $finding_count findings without source sub-skill reference (/ux-* expected)"
  fi

  # Pass 2: Check each finding row has >= 2 distinct {PREFIX}-{NNN} patterns
  # (its own synthesis-level ID plus at least one source finding ID from the sub-skill)
  # A row selected by grep -E '^\|.*[A-Z]{2,}-[0-9]{3}' always has at least one match
  # (the row's own ID), so we count occurrences per row and flag rows with only 1 match.
  no_source_id=0
  while IFS= read -r row; do
    # Count distinct {PREFIX}-{NNN} occurrences in this row
    id_count=$(echo "$row" | grep -oE '[A-Z]{2,}-[0-9]{3}' | sort -u | wc -l | xargs)
    if [ "$id_count" -lt 2 ]; then
      no_source_id=$((no_source_id + 1))
    fi
  done <<< "$finding_lines"
  if [ "$no_source_id" -gt 0 ]; then
    echo "WARNING: $synthesis_file has $no_source_id of $finding_count findings with only one {PREFIX}-{NNN} ID (missing source finding ID per synthesis-validation.md [Required Traceability])"
  fi

  traceable=$((finding_count - no_subskill - no_source_id))
  # Clamp to zero if both checks overlap on same rows
  [ "$traceable" -lt 0 ] && traceable=0
  echo "INFO: $synthesis_file -- $traceable of $finding_count findings have full traceability (sub-skill ref + source ID)"
done
echo "PASS: Traceability check complete"
```

### UX-CI-013: LOW Confidence Template Compliance

<!-- Source: synthesis-validation.md [Confidence Classification] Gate Definitions -- LOW confidence: "Output permanently labeled reference-only; design recommendation section structurally omitted." synthesis-validation.md [Gate Enforcement Mechanisms] -- LOW gate: "Output template structurally omits the design recommendation section. Title tagged with [REFERENCE-ONLY]." -->

**Check:** Findings classified as LOW do not contain design recommendations. Sections tagged `[REFERENCE-ONLY]` must not contain subsections named "Design Recommendations" or "Recommended Actions".

**Scope:** Files matching `skills/user-experience/output/*/ux-orchestrator-synthesis.md` and `skills/user-experience/output/*/ux-orchestrator-crisis.md`.

**Pass criteria:** Sections tagged `[REFERENCE-ONLY]` do not contain subsections named "Design Recommendations" or "Recommended Actions" (per synthesis-validation.md LOW gate enforcement).

**Implementation pattern:**

```bash
# UX-CI-013: LOW Confidence Template Compliance
# Source: synthesis-validation.md [Confidence Classification] LOW gate --
#   "Output permanently labeled reference-only; design recommendation section structurally omitted."
# Source: synthesis-validation.md [Gate Enforcement Mechanisms] LOW gate --
#   "Output template structurally omits the design recommendation section. Title tagged with [REFERENCE-ONLY]."
for synthesis_file in skills/user-experience/output/*/ux-orchestrator-synthesis.md \
                      skills/user-experience/output/*/ux-orchestrator-crisis.md; do
  [ -f "$synthesis_file" ] || continue
  # Extract content within [REFERENCE-ONLY] sections
  # The awk range terminates at ANY heading level (##, ###, or deeper) to correctly
  # handle synthesis files that use ### subsections within ## categories.
  # Previous implementation used /^## [^#]/ which missed ### boundaries, causing
  # the range to include content from adjacent ### subsections.
  # Fix: /^#{2,} / matches ## and ### (and deeper), correctly bounding the region.
  ref_only_content=$(awk '/\[REFERENCE-ONLY\]/{found=1; next} found && /^#{2,} /{found=0} found{print}' "$synthesis_file" || true)
  if [ -z "$ref_only_content" ]; then
    continue  # No [REFERENCE-ONLY] sections found; no violation possible
  fi
  # Check for forbidden subsection headings within [REFERENCE-ONLY] content
  violations=$(echo "$ref_only_content" | grep -ciE '(Design Recommendations|Recommended Actions|Design Interventions)' || true)
  if [ "$violations" -gt 0 ]; then
    echo "WARNING: $synthesis_file contains $violations design recommendation heading(s) in [REFERENCE-ONLY] section(s) (LOW confidence findings must not contain design recommendations per synthesis-validation.md)"
  fi
  # Also check for recommendation-like content patterns (actionable verb phrases after bullets)
  rec_patterns=$(echo "$ref_only_content" | grep -ciE '^\s*[-*]\s*(Implement|Deploy|Redesign|Add|Remove|Replace|Migrate)' || true)
  if [ "$rec_patterns" -gt 0 ]; then
    echo "WARNING: $synthesis_file contains $rec_patterns recommendation-like bullet(s) in [REFERENCE-ONLY] section(s)"
  fi
done
echo "PASS: LOW confidence template compliance check complete"
```

---

## CI Gate Summary

| Gate ID | Gate Name | Section | Scope | Pass Criteria | Blocking | Source |
|---------|-----------|---------|-------|---------------|----------|--------|
| UX-CI-001 | Agent Tool Grep | [P-003 Enforcement](#p-003-enforcement) | `skills/ux-*/agents/*.md` | Zero Agent matches in sub-skill tools frontmatter | Yes | H-01 (P-003), H-34(b) |
| UX-CI-002 | disallowedTools Declaration | [P-003 Enforcement](#p-003-enforcement) | `skills/ux-*/agents/*.md` | All sub-skills declare `disallowedTools: [Agent]` | Yes | H-34(b) |
| UX-CI-003 | Forbidden Actions P-003 | [P-003 Enforcement](#p-003-enforcement) | `skills/ux-*/agents/*.governance.yaml` | All governance files have >= 3 forbidden_actions entries referencing P-003, P-020, P-022 | Yes | H-34(b) |
| UX-CI-004 | Governance YAML Schema | [Schema Validation](#schema-validation) | `skills/ux-*/agents/*.governance.yaml` | Zero schema validation errors against `agent-governance-v1.schema.json` | Yes | H-34 |
| UX-CI-005 | Required Governance Fields | [Schema Validation](#schema-validation) | `skills/ux-*/agents/*.governance.yaml` | All required fields present with valid values | Yes | H-34 |
| UX-CI-006 | Frontmatter-Governance Consistency | [Schema Validation](#schema-validation) | Agent dual-file pairs | `.md` name field matches `.governance.yaml` filename | Yes | H-34 |
| UX-CI-007 | Signoff File Structure | [Wave Gate Compliance](#wave-gate-compliance) | `skills/user-experience/output/*SIGNOFF*.md` | All required fields non-empty; score >= 0.85; MCP ownership in kickoff | Yes | wave-progression.md |
| UX-CI-008 | Signoff Ordering | [Wave Gate Compliance](#wave-gate-compliance) | `skills/user-experience/output/` | Sequential signoff file existence | Yes | wave-progression.md |
| UX-CI-009 | Keyword Collision Check | [Trigger Map Validation](#trigger-map-validation) | `mandatory-skill-usage.md` Detected Keywords column (column 2) | Zero unmitigated collisions in trigger map keyword columns | Warning | RT-M-004 |
| UX-CI-010 | Negative Keyword Coverage | [Trigger Map Validation](#trigger-map-validation) | `mandatory-skill-usage.md` | Non-empty negative keywords for /user-experience row | Warning | RT-M-001 |
| UX-CI-011 | Confidence Classification | [Output Quality Checks](#output-quality-checks) | Synthesis output files | All findings have HIGH/MEDIUM/LOW confidence | Warning | synthesis-validation.md, P-022 |
| UX-CI-012 | Traceability | [Output Quality Checks](#output-quality-checks) | Synthesis output files | All findings trace to source sub-skill and finding ID | Warning | synthesis-validation.md [Required Traceability] |
| UX-CI-013 | LOW Template Compliance | [Output Quality Checks](#output-quality-checks) | Synthesis output files | No design recommendations in [REFERENCE-ONLY] sections | Warning | synthesis-validation.md [Gate Enforcement Mechanisms] |

**Blocking:** "Yes" gates fail the CI pipeline. "Warning" gates produce warnings but do not block.

**Source column:** Identifies the authoritative rule or standard from which each gate's pass criteria derive. All sources are accessible via repo-relative paths listed in [References](#references) below and in the per-gate `<!-- Source: -->` annotations above.

---

## CI Runner Integration

<!-- Source: quality-enforcement.md [Enforcement Architecture] L5 layer -- CI/commit post-hoc verification. This section provides the integration pattern for running all 13 gates as a single CI suite. -->

All 13 gate scripts can be composed into a runnable CI suite using a master script or GitHub Actions job. The following master script template invokes all gates in sequence, aggregating blocking failures and non-blocking warnings.

**Master script template:**

```bash
#!/usr/bin/env bash
# ux-ci-checks.sh -- Master CI runner for /user-experience skill gates
# Source: skills/user-experience/rules/ci-checks.md [CI Runner Integration]
# Usage: bash skills/user-experience/rules/ux-ci-checks.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
blocking_failures=0
warnings=0

run_gate() {
  local gate_id="$1"
  local gate_script="$2"
  local is_blocking="$3"
  echo "--- Running $gate_id ---"
  if output=$(bash -c "$gate_script" 2>&1); then
    echo "$output"
  else
    echo "$output"
    if [ "$is_blocking" = "yes" ]; then
      echo "BLOCKED: $gate_id failed (blocking gate)"
      blocking_failures=$((blocking_failures + 1))
    else
      echo "WARNING: $gate_id produced warnings (non-blocking)"
      warnings=$((warnings + 1))
    fi
  fi
  echo ""
}

# Blocking gates (UX-CI-001 through UX-CI-008): exit 1 on failure
# Warning gates (UX-CI-009 through UX-CI-013): warnings only
# Each gate script is sourced inline from the implementation patterns above.
# In practice, extract each gate's bash block into a separate file under
# skills/user-experience/scripts/ and invoke it here.

echo "=== UX CI Checks: 13 gates (8 blocking, 5 warning) ==="
echo ""

# Gate invocations would be:
#   run_gate "UX-CI-001" "bash skills/user-experience/scripts/ux-ci-001.sh" "yes"
#   run_gate "UX-CI-002" "bash skills/user-experience/scripts/ux-ci-002.sh" "yes"
#   ... through UX-CI-013 ...

echo "=== Summary ==="
echo "Blocking failures: $blocking_failures"
echo "Warnings: $warnings"

if [ "$blocking_failures" -gt 0 ]; then
  echo "FAIL: $blocking_failures blocking gate(s) failed"
  exit 1
fi
echo "PASS: All blocking gates passed ($warnings warning(s))"
```

**GitHub Actions integration:** Add a job step invoking `bash skills/user-experience/rules/ux-ci-checks.sh` after checkout. The script exits non-zero only for blocking gate failures (UX-CI-001 through UX-CI-008). Warning gates (UX-CI-009 through UX-CI-013) produce output but do not fail the job.

**File extraction convention:** Each gate's bash block (from the implementation patterns above) should be extracted into `skills/user-experience/scripts/ux-ci-{NNN}.sh` for maintainability. The master script invokes each extracted file. The implementation patterns in this document remain the authoritative source; the extracted scripts are generated copies.

---

## References

| Source | Content | Location |
|--------|---------|----------|
| SKILL.md | P-003 compliance, wave architecture, synthesis validation | `skills/user-experience/SKILL.md` |
| Agent Development Standards | H-34 (schema validation, constitutional compliance), dual-file architecture, governance fields, guardrails template | `.context/rules/agent-development-standards.md` |
| Quality Enforcement | H-01 (P-003), H-13 (quality gate), enforcement architecture L5 | `.context/rules/quality-enforcement.md` |
| Agent Routing Standards | RT-M-001 (negative keywords), RT-M-004 (collision detection) | `.context/rules/agent-routing-standards.md` |
| Mandatory Skill Usage | /user-experience trigger map row | `.context/rules/mandatory-skill-usage.md` |
| Wave Progression Rules | Signoff requirements, wave transition gates (0.85 threshold), bypass mechanism | `skills/user-experience/rules/wave-progression.md` |
| Synthesis Validation Rules | Confidence classification, required traceability, gate enforcement mechanisms | `skills/user-experience/rules/synthesis-validation.md` |
| MCP Coordination Rules | MCP ownership validation for kickoff signoff | `skills/user-experience/rules/mcp-coordination.md` |
| Governance Schema | JSON Schema for .governance.yaml validation | `docs/schemas/agent-governance-v1.schema.json` |
| ADR-PROJ022-002 | Wave criteria gates design decision (0.85 threshold rationale, distinct from H-13's 0.92) | `projects/PROJ-022-user-experience-skill/decisions/ADR-PROJ022-002-wave-criteria-gates.md` |

---

*Rule file: ci-checks.md*
*Parent skill: /user-experience*
*Parent SKILL.md: `skills/user-experience/SKILL.md`*
*Sibling rules: `skills/user-experience/rules/ux-routing-rules.md`, `skills/user-experience/rules/synthesis-validation.md`, `skills/user-experience/rules/wave-progression.md`, `skills/user-experience/rules/mcp-coordination.md`*
*Created: 2026-03-03*
*Updated: 2026-03-04*
*Revision: iter4 -- C4 quality revision: fixed UX-CI-009 (column-specific trigger map grep replacing full-file activation-keywords grep), UX-CI-012 (two-pass column-aware traceability replacing tautological single-pattern check), UX-CI-013 (awk heading boundary fix for ## and ### levels); added CI runner integration section; added ADR-PROJ022-002 reference*
*Status: COMPLETE*
