# ps-critic Tool Invocation Examples

> Detailed tool usage examples for the ps-critic agent, including AST-based operations for structured deliverable analysis.

## Standard Tool Invocation Examples

1. **Reading artifact to critique:**
   ```
   Read(file_path="projects/${JERRY_PROJECT}/decisions/work-024-e-399-auth-design-v2.md")
   → Load the generator's output for evaluation
   ```

2. **Finding related artifacts for context:**
   ```
   Glob(pattern="projects/${JERRY_PROJECT}/decisions/work-024-*.md")
   → Locate all versions for trend analysis
   ```

3. **Checking for specific quality indicators:**
   ```
   Grep(pattern="## (Trade-offs|Risks|Assumptions)", path="artifact.md", output_mode="content")
   → Verify required sections exist
   ```

4. **Creating critique output (MANDATORY per P-002):**
   ```
   Write(
       file_path="projects/${JERRY_PROJECT}/critiques/work-024-e-400-iter2-critique.md",
       content="# Critique: Authentication Design v2\n\n## L0: Executive Summary..."
   )
   ```

## AST-Based Operations (PREFERRED for structured deliverable analysis)

When critiquing deliverables that are Jerry entity files or rule documents,
use the `/ast` skill to extract structured information before applying the
S-014 scoring rubric.

5. **Extracting entity context for scoring setup:**
   ```bash
   uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast frontmatter {artifact_path}
   # Returns: {"Type": "story", "Status": "in_progress", "Parent": "FEAT-001", ...}
   # Use the "Type" field to select the appropriate schema for Completeness scoring
   ```

6. **Checking nav table compliance for Completeness dimension (H-23/H-24):**
   ```bash
   uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast validate {artifact_path} --nav
   # Returns: {"is_valid": true/false, "missing_entries": [...], "orphaned_entries": [...]}
   # Nav table violations = Completeness dimension deduction (missing sections)
   ```

7. **Schema validation for entity deliverables:**
   ```bash
   uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ast validate {artifact_path} --schema {entity_type}
   # Returns: {"schema_valid": true/false, "schema_violations": [...]}
   # Schema violations inform Completeness (0.20) and Methodological Rigor (0.20) scoring
   # Inspect schema_violations array for field_path and message details
   ```

**Migration Note (ST-010):** For deliverables that are Jerry entity files, use
`jerry ast validate path --schema entity_type` to get schema violations BEFORE applying
S-014 rubric dimensions. Schema violations directly impact the Completeness and
Methodological Rigor scores.
