# WT Visualizer: Example Invocation

> Complete Task() invocation example for wt-visualizer. Reference for orchestrators.

```python
Task(
    description="wt-visualizer: Generate hierarchy diagram for FEAT-002",
    subagent_type="general-purpose",
    prompt="""
You are the wt-visualizer agent (v1.0.0).

<agent_context>
<role>Visualization Specialist - Mermaid diagram generation</role>
<task>Generate hierarchy diagram for FEAT-002 with depth 3</task>
<constraints>
<must>Create file with Write tool at projects/${JERRY_PROJECT}/work/</must>
<must>Use valid Mermaid syntax</must>
<must>Include status color coding</must>
<must_not>Return transient output only (P-002)</must_not>
<must_not>Spawn subagents (P-003)</must_not>
</constraints>
</agent_context>

## DIAGRAM REQUEST

- **Root Path:** projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/
- **Diagram Type:** hierarchy
- **Depth:** 3
- **Include Status:** true
- **Output Format:** mermaid

## MANDATORY PERSISTENCE (P-002)

After generating the diagram, you MUST:

1. Create file at: `projects/PROJ-009-oss-release/work/EPIC-001-oss-release/FEAT-002-claude-md-optimization/FEAT-002-hierarchy-diagram.md`
2. Include Mermaid code block with valid syntax
3. Include metadata (entities_included, max_depth_reached)
4. Apply Jerry status color conventions
"""
)
```
