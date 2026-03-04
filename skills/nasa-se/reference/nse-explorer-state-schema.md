# NSE Explorer: State Management Schema

> State schema for agent chaining. Defines the `exploration_output` key and upstream/downstream agent expectations.

## Output Key: `exploration_output`

```yaml
exploration_output:
  project_id: "{project_id}"
  entry_id: "{entry_id}"
  exploration_type: "{trade_study|alternative_analysis|concept_exploration}"
  artifact_path: "projects/{project}/exploration/{filename}.md"
  summary: "{exploration summary}"
  alternatives_count: {count}
  top_alternatives:
    - id: "ALT-001"
      name: "{name}"
      score: {weighted_score}
    - id: "ALT-002"
      name: "{name}"
      score: {weighted_score}
  decision_ready: {true|false}
  next_agent_hint: "nse-architecture"
  nasa_processes_applied: ["Process 17"]
```

## Reading Previous State

If invoked after another agent, check session.state for:
- `requirements_output` - Requirements driving the exploration
- `risk_output` - Risks to consider in alternatives
- `architecture_output` - Architectural constraints on options

## Providing State to Next Agent

When complete, provide state for:
- `nse-architecture` - To incorporate selected alternative into design
- `nse-reviewer` - To review decision rationale
- `nse-risk` - To assess risks of alternatives
