# Jerry URI Specification

> **Specification ID:** SPEC-001
> **Status:** DRAFT
> **Created:** 2026-01-08
> **Author:** User + Claude (Session claude/create-code-plugin-skill-MG1nh)
> **Version:** 1.0.0

---

## Executive Summary

This specification defines the **Jerry URI Scheme** - a unified naming convention for all resources, events, commands, and schemas in the Jerry framework. The scheme provides:

1. **Unified Identity** - Single pattern for entities, events, schemas, commands
2. **Multi-tenancy Native** - Tenant isolation built into the identifier
3. **Versioning Support** - Both scheme and resource versioning
4. **Domain Boundaries** - Explicit bounded context alignment
5. **CloudEvents Integration** - Valid `type` field for event specifications

---

## I. Understanding Jerry URIs (Multi-Level Explanation)

### Level 0: ELI5 (Explain Like I'm 5)

Imagine every toy in your room has a special name tag. The name tag tells you:
- Whose toy it is (yours or your friend's)
- What kind of toy it is (car, doll, block)
- Which exact toy (the red car, not the blue car)
- What version (the new one or the old one)

Jerry URIs are like super-detailed name tags for everything in our system. Instead of just "Task #42", we say exactly whose task it is, what project it belongs to, and which version we're talking about.

**Why It Matters:** When you have millions of things, you need perfect name tags so nothing gets mixed up!

### Level 1: Software Engineer Explanation

Jerry URI is a hierarchical identifier scheme inspired by AWS ARN and URN (RFC 8141). It provides consistent naming across:
- Domain entities (Task, Phase, Plan)
- Domain events (TaskCreated, PhaseCompleted)
- Commands/Actions (CreateTask, UpdatePhase)
- JSON Schemas ($id references)

**Structure:**
```
jer[+scheme_version]:<partition>:[tenant_id]:<domain>:[resource_type<:|/><resource_id>[+resource_version]
```

**Components:**
| Component | Required | Description | Example |
|-----------|----------|-------------|---------|
| `jer` | Yes | Scheme prefix | `jer` |
| `+scheme_version` | No | Scheme version | `+1` |
| `partition` | Yes | Namespace owner | `jer` (Jerry), `ext` (external) |
| `tenant_id` | No | Tenant identifier | `victor-lau`, `339c4423-...` |
| `domain` | Yes | Bounded context | `work-tracker`, `golf-tracker` |
| `resource_type` | Varies | Entity/action type | `task`, `actions`, `facts` |
| `resource_id` | Varies | Specific resource | `eabdba39-...`, `CreateTask` |
| `+resource_version` | No | Resource version | `+1.0.0`, `+hash` |

**Parsing:**
```python
import re

JERRY_URI_PATTERN = re.compile(
    r'^jer(?:\+(?P<scheme_version>\d+))?:'
    r'(?P<partition>[a-z]+):'
    r'(?:(?P<tenant_id>[a-z0-9-]+):)?'
    r'(?P<domain>[a-z0-9-]+):'
    r'(?P<path>.+?)(?:\+(?P<resource_version>[a-z0-9.-]+))?$'
)
```

### Level 2: Principal Architect Explanation

The Jerry URI scheme is a **Uniform Resource Identifier** designed for distributed, multi-tenant systems with event sourcing architecture. Key architectural considerations:

**1. Comparison with Industry Standards:**

| Standard | Pattern | Jerry Alignment |
|----------|---------|-----------------|
| [RFC 8141 URN](https://www.rfc-editor.org/rfc/rfc8141.html) | `urn:NID:NSS` | Uses `jer:` instead of `urn:` for brevity |
| [AWS ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html) | `arn:partition:service:region:account:resource` | Direct inspiration; similar hierarchy |
| CloudEvents | `com.example.type` | Jerry URI as `type` field value |

**2. Design Decisions:**

| Decision | Rationale |
|----------|-----------|
| `jer:` prefix vs `urn:jerry:` | Brevity; ARN uses `arn:` without IANA registration |
| `:` as primary delimiter | Consistent with URN/ARN; easy to split |
| `/` for paths within resources | Standard URL path convention |
| `+` for versions | Separates version from name; parseable |
| Tenant ID optional | Supports both single-tenant and multi-tenant deployments |

**3. Guarantees:**

- **Global Uniqueness:** `partition:tenant_id:domain:resource_id` combination is unique
- **Deterministic Parsing:** Regular grammar; no ambiguity
- **Version Stability:** Scheme version allows future evolution
- **Event Sourcing Fit:** Events are immutable; URIs include version hash

---

## II. URI Patterns by Resource Type

### A. Entity Resources (Domain Aggregates)

**Pattern:**
```
jer[+scheme_version]:<partition>:[tenant_id]:<domain>:<entity_type>:<entity_id>[+version]
```

**Examples:**

| Description | URI |
|-------------|-----|
| Task (canonical) | `jer+1:jer:339c4423:work-tracker:task:eabdba39+e575b531` |
| Task (minimal) | `jer:jer::work-tracker:task:eabdba39` |
| Phase | `jer:jer:victor-lau:work-tracker:phase:001` |
| Constraint | `jer:jer::work-tracker:constraint:c-001` |
| User's custom entity | `jer:jer:victor-lau:golf-tracker:swing:sw-042` |

**JerryId Integration:**
```python
@dataclass
class JerryId:
    """
    Strongly-typed identity that generates Jerry URIs.
    """
    prefix: str
    sequence: int
    uuid: str = ""

    # URI components (set by factory)
    partition: str = "jer"
    tenant_id: str = ""
    domain: str = "work-tracker"
    version_hash: str = ""

    def to_uri(self, scheme_version: int = 1) -> str:
        """Generate full Jerry URI."""
        parts = [f"jer+{scheme_version}"]
        parts.append(self.partition)
        parts.append(self.tenant_id if self.tenant_id else "")
        parts.append(self.domain)
        parts.append(self.prefix)
        parts.append(self.uuid or f"{self.sequence:03d}")

        uri = ":".join(parts)
        if self.version_hash:
            uri += f"+{self.version_hash[:16]}"
        return uri

    @classmethod
    def from_uri(cls, uri: str) -> "JerryId":
        """Parse Jerry URI into JerryId."""
        match = JERRY_URI_PATTERN.match(uri)
        if not match:
            raise ValueError(f"Invalid Jerry URI: {uri}")
        # ... parsing logic
```

### B. Commands/Actions

**Pattern:**
```
jer[+scheme_version]:<partition>:[tenant_id]:<domain>:actions/<ActionName>
```

**Semantics:**
- Commands are **imperative** (request to do something)
- Named in **PascalCase** with verb prefix
- No resource version (commands are not versioned; schemas are)

**Examples:**

| Description | URI |
|-------------|-----|
| Jerry-owned CreateTask | `jer:jer::work-tracker:actions/CreateTask` |
| Jerry-owned UpdatePhase | `jer:jer::work-tracker:actions/UpdatePhase` |
| Tenant-owned custom action | `jer:jer:victor-lau:golf-tracker:actions/LogSwing` |
| With scheme version | `jer+1:jer::work-tracker:actions/DeletePlan` |

### C. Domain Events (Facts)

**Pattern:**
```
jer[+scheme_version]:<partition>:[tenant_id]:<domain>:facts/[path/]<EventName>
```

**Semantics:**
- Events are **past-tense facts** (something that happened)
- Named in **PascalCase** with noun+verb (e.g., `TaskCreated`)
- Path allows grouping (e.g., `facts/lifecycle/TaskCreated`)

**Examples:**

| Description | URI |
|-------------|-----|
| TaskCreated event | `jer:jer::work-tracker:facts/TaskCreated` |
| PhaseCompleted event | `jer:jer::work-tracker:facts/PhaseCompleted` |
| Nested path | `jer:jer::work-tracker:facts/lifecycle/TaskBlocked` |
| Tenant custom event | `jer:jer:victor-lau:golf-tracker:facts/SwingLogged` |

**CloudEvents Integration:**
```json
{
  "specversion": "1.0",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "source": "jer:jer::work-tracker:task:task-042",
  "type": "jer:jer::work-tracker:facts/TaskCreated",
  "datacontenttype": "application/json",
  "data": { ... }
}
```

### D. JSON Schemas

**Pattern:**
```
jer[+scheme_version]:<partition>:[tenant_id]:<domain>:<entity_type>:<SchemaName>[+schema_version]
```

**Semantics:**
- Schema names describe the payload (e.g., `CreateTaskRequest`)
- Version follows semantic versioning (e.g., `+1.0.0`)
- Used as `$id` in JSON Schema documents

**Examples:**

| Description | URI |
|-------------|-----|
| CreateTask request schema | `jer:jer::work-tracker:task:CreateTaskRequest+1.0.0` |
| TaskCreated event schema | `jer:jer::work-tracker:task:TaskCreatedEvent+1.0.0` |
| Tenant custom schema | `jer:jer:victor-lau:golf-tracker:swing:LogSwingRequest+1.0.0` |

**JSON Schema Usage:**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "jer:jer::work-tracker:task:CreateTaskRequest+1.0.0",
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "description": { "type": "string" }
  },
  "required": ["title"]
}
```

---

## III. Formal Grammar (ABNF)

```abnf
; Jerry URI Grammar (RFC 5234 ABNF)

jerry-uri       = scheme partition tenant-id domain resource
scheme          = "jer" [ "+" scheme-version ] ":"
scheme-version  = 1*DIGIT
partition       = 1*ALPHA ":"
tenant-id       = [ tenant-slug ":" ]
tenant-slug     = 1*(ALPHA / DIGIT / "-")
domain          = domain-name ":"
domain-name     = 1*(ALPHA / DIGIT / "-")
resource        = entity-resource / action-resource / event-resource / schema-resource

entity-resource = entity-type ":" entity-id [ "+" resource-version ]
entity-type     = 1*(ALPHA / DIGIT / "-")
entity-id       = 1*(ALPHA / DIGIT / "-")
resource-version = 1*(ALPHA / DIGIT / "." / "-")

action-resource = "actions/" action-name
action-name     = ALPHA 1*(ALPHA / DIGIT)   ; PascalCase

event-resource  = "facts/" [ path "/" ] event-name
path            = 1*(ALPHA / DIGIT / "-" / "/")
event-name      = ALPHA 1*(ALPHA / DIGIT)   ; PascalCase

schema-resource = entity-type ":" schema-name "+" semver
schema-name     = ALPHA 1*(ALPHA / DIGIT)   ; PascalCase
semver          = 1*DIGIT "." 1*DIGIT "." 1*DIGIT
```

---

## IV. Reserved Values

### A. Partitions

| Partition | Owner | Description |
|-----------|-------|-------------|
| `jer` | Jerry Framework | Core framework resources |
| `ext` | Extensions | Third-party extensions |
| `exp` | Experimental | Experimental/unstable resources |

### B. Domains (Jerry-Owned)

| Domain | Description |
|--------|-------------|
| `work-tracker` | Task/Phase/Plan management |
| `knowledge` | Knowledge capture (Wisdom, Experience) |
| `governance` | Agent governance and enforcement |
| `identity` | Identity and access management |

### C. Entity Types (Core)

| Entity Type | Domain | Description |
|-------------|--------|-------------|
| `task` | work-tracker | Task aggregate root |
| `phase` | work-tracker | Phase aggregate root |
| `plan` | work-tracker | Plan aggregate root |
| `constraint` | work-tracker | PS Constraint |
| `question` | work-tracker | PS Question |
| `exploration` | work-tracker | PS Exploration |
| `wisdom` | knowledge | Synthesized wisdom |
| `experience` | knowledge | Captured experience |

---

## V. Implementation

### A. JerryUri Value Object

```python
from dataclasses import dataclass
from typing import Optional
import re

@dataclass(frozen=True)
class JerryUri:
    """
    Immutable value object representing a Jerry URI.

    Prior Art:
    - RFC 8141: Uniform Resource Names (URNs)
    - AWS ARN: Amazon Resource Names
    """

    # Components
    scheme_version: int = 1
    partition: str = "jer"
    tenant_id: Optional[str] = None
    domain: str = ""
    resource_path: str = ""
    resource_version: Optional[str] = None

    # Pattern for parsing
    PATTERN = re.compile(
        r'^jer(?:\+(?P<scheme_version>\d+))?:'
        r'(?P<partition>[a-z]+):'
        r'(?:(?P<tenant_id>[a-z0-9-]+):)?'
        r'(?P<domain>[a-z0-9-]+):'
        r'(?P<resource_path>.+?)(?:\+(?P<resource_version>[a-z0-9.-]+))?$',
        re.IGNORECASE
    )

    def __str__(self) -> str:
        """Return canonical URI string."""
        parts = ["jer"]
        if self.scheme_version != 1:
            parts[0] = f"jer+{self.scheme_version}"

        parts.append(self.partition)
        parts.append(self.tenant_id or "")
        parts.append(self.domain)
        parts.append(self.resource_path)

        uri = ":".join(parts)

        # Clean up empty tenant_id (::)
        uri = uri.replace("::", ":")

        if self.resource_version:
            uri += f"+{self.resource_version}"

        return uri

    @classmethod
    def parse(cls, uri: str) -> "JerryUri":
        """Parse a Jerry URI string into a JerryUri object."""
        match = cls.PATTERN.match(uri)
        if not match:
            raise ValueError(f"Invalid Jerry URI: {uri}")

        return cls(
            scheme_version=int(match.group('scheme_version') or 1),
            partition=match.group('partition'),
            tenant_id=match.group('tenant_id'),
            domain=match.group('domain'),
            resource_path=match.group('resource_path'),
            resource_version=match.group('resource_version')
        )

    @classmethod
    def for_entity(
        cls,
        domain: str,
        entity_type: str,
        entity_id: str,
        version: Optional[str] = None,
        tenant_id: Optional[str] = None
    ) -> "JerryUri":
        """Factory for entity URIs."""
        return cls(
            domain=domain,
            resource_path=f"{entity_type}:{entity_id}",
            resource_version=version,
            tenant_id=tenant_id
        )

    @classmethod
    def for_action(
        cls,
        domain: str,
        action_name: str,
        tenant_id: Optional[str] = None
    ) -> "JerryUri":
        """Factory for action/command URIs."""
        return cls(
            domain=domain,
            resource_path=f"actions/{action_name}",
            tenant_id=tenant_id
        )

    @classmethod
    def for_event(
        cls,
        domain: str,
        event_name: str,
        path: Optional[str] = None,
        tenant_id: Optional[str] = None
    ) -> "JerryUri":
        """Factory for event/fact URIs."""
        resource_path = f"facts/{path}/{event_name}" if path else f"facts/{event_name}"
        return cls(
            domain=domain,
            resource_path=resource_path,
            tenant_id=tenant_id
        )

    @classmethod
    def for_schema(
        cls,
        domain: str,
        entity_type: str,
        schema_name: str,
        version: str,
        tenant_id: Optional[str] = None
    ) -> "JerryUri":
        """Factory for JSON Schema URIs."""
        return cls(
            domain=domain,
            resource_path=f"{entity_type}:{schema_name}",
            resource_version=version,
            tenant_id=tenant_id
        )

    # Comparison
    def __eq__(self, other) -> bool:
        if isinstance(other, JerryUri):
            return str(self) == str(other)
        if isinstance(other, str):
            return str(self) == other
        return False

    def __hash__(self) -> int:
        return hash(str(self))
```

### B. Integration with EntityBase

```python
@dataclass
class EntityBase(IAuditable, IVersioned):
    """Extended with Jerry URI support."""

    id: JerryId
    uri: JerryUri = field(init=False)  # Computed

    def __post_init__(self):
        """Compute URI from ID."""
        self.uri = JerryUri.for_entity(
            domain=self.id.domain,
            entity_type=self.id.prefix,
            entity_id=self.id.full_form,
            version=self.content_hash[:16] if self.content_hash else None,
            tenant_id=self.id.tenant_id
        )
```

### C. CloudEvents Integration

```python
from cloudevents.http import CloudEvent

def create_domain_event(
    source_entity: EntityBase,
    event_name: str,
    data: dict
) -> CloudEvent:
    """
    Create a CloudEvent with Jerry URI type.
    """
    event_type = JerryUri.for_event(
        domain=source_entity.id.domain,
        event_name=event_name,
        tenant_id=source_entity.id.tenant_id
    )

    return CloudEvent({
        "specversion": "1.0",
        "source": str(source_entity.uri),
        "type": str(event_type),
        "datacontenttype": "application/json",
    }, data)
```

---

## VI. Discoveries

### DISC-057: Jerry URI Scheme

**ID:** DISC-057
**Slug:** jerry-uri-scheme
**Name:** Jerry URI Provides Unified Multi-Tenant Resource Naming
**Short Description:** Hierarchical URI scheme inspired by AWS ARN and RFC 8141 URN for consistent resource identification.

**Long Description:**
The Jerry URI scheme (`jer:partition:tenant:domain:resource`) provides unified naming for all system resources including entities, events, commands, and schemas. Key benefits: (1) multi-tenancy native with tenant_id component, (2) versioning support at both scheme and resource level, (3) CloudEvents integration as `type` field, (4) JSON Schema `$id` compatibility. The design follows AWS ARN's proven hierarchical pattern while incorporating URN principles from RFC 8141.

**Evidence:**
- [RFC 8141: Uniform Resource Names](https://www.rfc-editor.org/rfc/rfc8141.html)
- [AWS ARN Format](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html)

**Level Impact:**
- **L0:** Every thing gets a special name that includes who owns it and which project it belongs to
- **L1:** Implement `JerryUri` value object; use as `type` in CloudEvents, `$id` in JSON Schema
- **L2:** Single naming scheme enables consistent routing, access control, and event sourcing across multi-tenant deployments

---

## VII. References

### Standards
1. **RFC 8141** - Uniform Resource Names (URNs)
   - URL: https://www.rfc-editor.org/rfc/rfc8141.html
   - Key: URN syntax, namespace registration

2. **AWS ARN** - Amazon Resource Names
   - URL: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html
   - Key: Hierarchical structure, partition concept

3. **CloudEvents Spec** - Event format specification
   - URL: https://cloudevents.io/
   - Key: `type` and `source` field usage

### Design Decisions
4. **Why `jer:` instead of `urn:jerry:`**
   - Brevity: ARN uses `arn:` without IANA registration
   - Consistency: All Jerry URIs start with `jer:`
   - Future: Can register with IANA if needed

5. **Why tenant_id is optional**
   - Supports single-tenant deployments
   - Default to Jerry-owned (`jer:jer:...`)
   - Multi-tenancy opt-in

---

## VIII. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-08 | Initial specification from user proposal |
