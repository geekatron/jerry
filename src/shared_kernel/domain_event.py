"""
Domain Event - Base class for all domain events.

Domain events are immutable value objects representing significant state changes
in the domain. They capture what happened, when, and to which aggregate.

This module implements the event infrastructure per ADR-009 (Event Storage Mechanism).

References:
    - ADR-009: Event Storage Mechanism
    - Martin Fowler: Domain Events (https://martinfowler.com/eaaDev/DomainEvent.html)
    - Eric Evans: Domain-Driven Design (Domain Events pattern)

Exports:
    DomainEvent: Base class for all domain events
    EventRegistry: Registry for event type deserialization
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, ClassVar, Type

from .vertex_id import EventId


def _generate_event_id() -> str:
    """Generate a unique event ID."""
    return str(EventId.generate())


def _current_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class DomainEvent:
    """
    Base class for all domain events.

    Domain events are immutable value objects that capture significant state
    changes in the domain. They are the foundation for event sourcing and
    audit trails.

    Attributes:
        event_id: Unique identifier for this event instance
        aggregate_id: ID of the aggregate this event belongs to
        aggregate_type: Type name of the aggregate (e.g., "WorkItem")
        version: Version number of the aggregate after this event
        timestamp: When the event occurred (UTC)

    Example:
        >>> event = DomainEvent(
        ...     aggregate_id="WORK-001",
        ...     aggregate_type="WorkItem",
        ... )
        >>> event.event_id.startswith("EVT-")
        True
        >>> event.version
        1

    Invariants:
        - Immutable (frozen dataclass)
        - aggregate_id must not be empty
        - aggregate_type must not be empty
        - version must be positive (>= 1)
        - timestamp is always UTC
    """

    # Required fields with defaults that must be overridden or auto-generated
    aggregate_id: str
    aggregate_type: str

    # Auto-generated fields with defaults
    event_id: str = field(default_factory=_generate_event_id)
    timestamp: datetime = field(default_factory=_current_timestamp)
    version: int = 1

    # Class-level registry reference (set by EventRegistry)
    _registry: ClassVar[EventRegistry | None] = None

    def __post_init__(self) -> None:
        """Validate event after initialization."""
        if not self.aggregate_id:
            raise ValueError("aggregate_id cannot be empty")
        if not self.aggregate_type:
            raise ValueError("aggregate_type cannot be empty")
        if self.version < 1:
            raise ValueError("version must be >= 1")

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize event to dictionary.

        Returns:
            Dictionary with all event fields, JSON-serializable.
            Includes event_type for deserialization support.

        Example:
            >>> event = DomainEvent(aggregate_id="WORK-001", aggregate_type="WorkItem")
            >>> data = event.to_dict()
            >>> data["event_type"]
            'DomainEvent'
        """
        return {
            "event_type": self.__class__.__name__,
            "event_id": self.event_id,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "version": self.version,
            "timestamp": self.timestamp.isoformat(),
            **self._payload(),
        }

    def _payload(self) -> dict[str, Any]:
        """
        Return event-specific payload data.

        Override in subclasses to include additional fields.

        Returns:
            Dictionary of additional event-specific data.
        """
        return {}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DomainEvent:
        """
        Deserialize event from dictionary.

        Args:
            data: Dictionary containing event fields

        Returns:
            Reconstructed DomainEvent instance

        Note:
            For subclass-aware deserialization, use EventRegistry.deserialize()
        """
        timestamp_str = data.get("timestamp")
        timestamp = (
            datetime.fromisoformat(timestamp_str)
            if timestamp_str
            else _current_timestamp()
        )

        return cls(
            event_id=data.get("event_id", _generate_event_id()),
            aggregate_id=data["aggregate_id"],
            aggregate_type=data["aggregate_type"],
            version=data.get("version", 1),
            timestamp=timestamp,
        )

    def __eq__(self, other: object) -> bool:
        """Events are equal if they have the same event_id."""
        if not isinstance(other, DomainEvent):
            return NotImplemented
        return self.event_id == other.event_id

    def __hash__(self) -> int:
        """Hash by event_id for set/dict usage."""
        return hash(self.event_id)


class EventRegistry:
    """
    Registry for domain event types.

    Enables polymorphic deserialization of events based on event_type field.
    Supports decorator-based and explicit registration.

    Example:
        >>> registry = EventRegistry()
        >>> registry.register(DomainEvent)
        >>> event = registry.deserialize({"event_type": "DomainEvent", ...})

    Example with decorator:
        >>> registry = EventRegistry()
        >>> @registry.register
        ... class CustomEvent(DomainEvent):
        ...     pass
    """

    def __init__(self) -> None:
        """Initialize empty registry."""
        self._event_types: dict[str, Type[DomainEvent]] = {}

    @property
    def event_types(self) -> dict[str, Type[DomainEvent]]:
        """Return read-only copy of registered event types."""
        return dict(self._event_types)

    def register(
        self, event_class: Type[DomainEvent]
    ) -> Type[DomainEvent]:
        """
        Register an event class for deserialization.

        Can be used as a decorator or called directly.

        Args:
            event_class: The event class to register

        Returns:
            The same event class (for decorator usage)

        Example:
            >>> registry = EventRegistry()
            >>> registry.register(DomainEvent)
            <class 'DomainEvent'>
        """
        self._event_types[event_class.__name__] = event_class
        return event_class

    def get(self, event_type: str) -> Type[DomainEvent] | None:
        """
        Get registered event class by type name.

        Args:
            event_type: The event class name

        Returns:
            The registered class, or None if not found
        """
        return self._event_types.get(event_type)

    def deserialize(self, data: dict[str, Any]) -> DomainEvent:
        """
        Deserialize an event using the appropriate registered class.

        Args:
            data: Dictionary containing event_type and event fields

        Returns:
            Deserialized event instance

        Raises:
            ValueError: If event_type is not registered
        """
        event_type = data.get("event_type")
        if not event_type:
            raise ValueError("Missing event_type in data")

        event_class = self.get(event_type)
        if event_class is None:
            raise ValueError(f"Unknown event type: {event_type}")

        return event_class.from_dict(data)


# Global registry for convenience
_global_registry = EventRegistry()
_global_registry.register(DomainEvent)


def get_global_registry() -> EventRegistry:
    """Get the global event registry."""
    return _global_registry
