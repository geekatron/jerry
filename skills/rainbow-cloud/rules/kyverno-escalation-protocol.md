# Kyverno Dual-Zone Escalation Protocol

> Defines when and how the rainbow-cloud-auditor agent escalates Kyverno operations from Zone 1 (validation) to Zone 2 (mutation) and Zone 3 (generation). Primary reference for Kyverno zone classification decisions.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Zone Classification](#zone-classification) | Kyverno operation-to-zone mapping |
| [Policy Analysis Procedure](#policy-analysis-procedure) | How to classify a Kyverno policy before execution |
| [Zone 1 Operations](#zone-1-operations) | Permitted validation and testing operations |
| [Zone 2 Escalation](#zone-2-escalation) | When and how to escalate to mutate mode |
| [Zone 3 Escalation](#zone-3-escalation) | Generate mode -- never execute |
| [Dry-Run Enforcement](#dry-run-enforcement) | How the apply command provides dry-run semantics |
| [Escalation Decision Tree](#escalation-decision-tree) | Step-by-step classification flowchart |
| [Traceability](#traceability) | Source references |

---

## Zone Classification

Kyverno CLI operations span three security zones based on the operation type. Classification is deterministic, based on the policy YAML content and CLI subcommand -- not on agent judgment.

| Operation | Zone | CLI Command | Authorization |
|-----------|------|-------------|---------------|
| `validate` (local resources) | Zone 1 | `kyverno apply <policy.yaml> --resource <resource.yaml>` | Project scope only (H-04) |
| `test` (policy test cases) | Zone 1 | `kyverno test <test-dir>` | Project scope only (H-04) |
| `json` (JSON payload validation) | Zone 1 | `kyverno json --payload <json> --policy <policy>` | Project scope only (H-04) |
| `mutate` (apply without local resource, targeting live cluster) | Zone 2 | `kyverno apply <policy.yaml>` (no `--resource`, targeting live cluster) | Engagement scope + cluster authorization |
| `generate` (resource generation) | Zone 3 | N/A -- NEVER execute | Per-operation human approval |

### Kyverno `apply` as Dry-Run

The Kyverno CLI `apply` command, when used with `--resource <file>`, performs a local dry-run against the provided resource manifest. It does NOT connect to a live Kubernetes cluster. This is the Zone 1 usage pattern.

The same `apply` command, when used WITHOUT `--resource` and targeting a live cluster context, performs actual policy enforcement (mutation). This is the Zone 2 usage pattern.

**The zone classification depends on whether `--resource` is specified, not on the `apply` keyword itself.**

---

## Policy Analysis Procedure

Before executing any Kyverno operation, the agent MUST classify the policy by analyzing its YAML content.

### Step 1: Parse Policy YAML

Read the policy file and extract the `spec.rules` array. Each rule has a `name` and one or more of: `validate`, `mutate`, `generate`.

### Step 2: Classify Rule Types

| Rule Type Found | Classification |
|-----------------|---------------|
| Only `validate` rules | Zone 1 eligible (with `--resource` flag) |
| Contains `mutate` rules | Zone 2 minimum (requires engagement scope) |
| Contains `generate` rules | Zone 3 (NEVER execute) |
| Mixed `validate` + `mutate` | Zone 2 minimum (highest zone wins) |
| Mixed with `generate` | Zone 3 (NEVER execute) |

### Step 3: Apply Zone Decision

- **Zone 1:** Proceed with `kyverno apply <policy> --resource <resource>` or `kyverno test <dir>`.
- **Zone 2:** HALT. Verify engagement scope. If scope exists and authorizes Kyverno mutation on the target cluster, proceed with explicit user awareness.
- **Zone 3:** HALT. Inform user that generate mode is not available. Return to orchestrator.

---

## Zone 1 Operations

Zone 1 permits the following Kyverno CLI operations. No engagement scope required.

### Validate Mode

```
kyverno apply <policy.yaml> --resource <resource.yaml>
```

- Validates the resource manifest against the policy rules locally.
- Produces pass/fail results per policy rule.
- Does NOT connect to any Kubernetes cluster.
- Use `--policy-report` to generate a policy report artifact.

### Test Mode

```
kyverno test <test-directory>
```

- Runs predefined test cases from a test manifest (typically `kyverno-test.yaml`).
- Compares expected outcomes against actual policy application results.
- Entirely local -- no cluster interaction.

### JSON Validation Mode

```
kyverno json --payload <json-payload> --policy <policy.yaml>
```

- Validates a JSON payload against CEL/JMESPath expressions in the policy.
- Entirely local -- no cluster interaction.

---

## Zone 2 Escalation

Kyverno mutation operations require Zone 2 engagement scope.

### When to Escalate

Escalate to Zone 2 when ANY of the following conditions are met:

1. The Kyverno policy YAML contains `mutate` rules.
2. The user requests Kyverno `apply` without `--resource` (targeting a live cluster).
3. The Kyverno operation targets a cluster context (kubeconfig reference).

### Escalation Procedure

1. **HALT** current execution immediately.
2. **Analyze** the policy to identify mutate rules and affected resources.
3. **Check** for engagement scope document at `skills/rainbow/output/{engagement-id}/SCOPE.md`.
4. **Validate scope:**
   - Target cluster is in `authorized_targets`.
   - Target cluster is NOT in `excluded_targets`.
   - `technique_allowlist` includes `kubernetes-policy-enforcement` or equivalent.
   - `time_window` includes current time.
   - `operator_approval` is present.
5. **If scope is valid:** Inform user of the mutation operation details (policy name, affected resources, target cluster) and proceed.
6. **If scope is missing or invalid:** Return `{halt: true, reason: 'engagement_scope_required_for_kyverno_mutate'}` and inform user per P-020.

---

## Zone 3 Escalation

Kyverno `generate` mode creates new Kubernetes resources. This is Zone 3 -- per-operation human approval.

### Agent Response to Generate Policies

The rainbow-cloud-auditor agent MUST:

1. **Detect** `generate` rules in the policy YAML during classification.
2. **HALT** execution immediately.
3. **Inform** the user that Kyverno generate mode is Zone 3 and requires per-operation human approval.
4. **Return** to rainbow-orchestrator with escalation reason.
5. **NEVER** execute a policy containing `generate` rules, even if other rules in the same policy are validate-only.

**Rationale:** Resource generation is irreversible at the cluster level and may create security-sensitive objects (NetworkPolicies, RBAC bindings, resource quotas). The blast radius justifies per-operation human approval.

---

## Dry-Run Enforcement

The Kyverno `apply` command provides built-in dry-run semantics when used with `--resource`. This section clarifies the enforcement model.

### Zone 1 Dry-Run (Default)

At Zone 1, all Kyverno `apply` operations MUST include `--resource <file>`:

```
kyverno apply policy.yaml --resource pod.yaml
```

This produces validation results without cluster interaction. The `--resource` flag forces local-only evaluation.

### Zone 2 Live Enforcement

At Zone 2, Kyverno `apply` WITHOUT `--resource` targets a live cluster:

```
kyverno apply policy.yaml
```

This applies the policy (including mutations) to the cluster. Requires engagement scope.

### Enforcement Rule

**The presence of `--resource` is the Zone 1/Zone 2 boundary for the `apply` command.**

The default dry-run enforcement configuration is defined in `kyverno-dryrun-enforcement.yaml`. This configuration specifies that all Kyverno operations at Zone 1 MUST target local resources (files), not live clusters.

---

## Escalation Decision Tree

```
Kyverno Operation Requested
    |
    v
[Parse policy YAML: extract spec.rules]
    |
    v
[Contains generate rules?]
    YES --> ZONE 3: HALT. Never execute. Inform user. Return to orchestrator.
    |
    NO
    v
[Contains mutate rules?]
    YES --> [--resource flag specified?]
                YES --> Execute locally (Zone 1). Report mutated resource as output.
                NO --> [Targeting live cluster?]
                         YES --> ZONE 2: Require engagement scope. Validate scope. Proceed if valid.
                         NO --> Reject. Ambiguous target. Ask user per H-31.
    |
    NO (validate-only or test)
    v
[--resource flag specified or test command?]
    YES --> ZONE 1: Execute. No engagement scope needed.
    NO --> [Targeting live cluster?]
             YES --> ZONE 2: Require engagement scope.
             NO --> Reject. No target specified. Ask user.
```

---

## Traceability

| Reference | Location |
|-----------|----------|
| ADR-PROJ023-001 (Architecture Decision) | `projects/PROJ-023-exploit-framework/work/design/skill-architecture.md` |
| Dual-Zone Tool Escalation Protocol | ADR-PROJ023-001, Section "Dual-Zone Tool Escalation Protocol" |
| Zone 1 Guardrail Profile | `skills/rainbow/rules/zone-1-analysis.md` |
| Zone 2 Guardrail Profile | `skills/rainbow/rules/zone-2-active.md` |
| Kyverno CLI Documentation | [kyverno.io/docs/kyverno-cli/](https://kyverno.io/docs/kyverno-cli/) |
| Kyverno Apply Command | [kyverno.io/docs/kyverno-cli/usage/apply/](https://kyverno.io/docs/kyverno-cli/usage/apply/) |
| Dry-Run Enforcement Config | `skills/rainbow-cloud/rules/kyverno-dryrun-enforcement.yaml` |
