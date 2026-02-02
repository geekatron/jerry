"""
Entities - Objects with identity that can change over time.

Entities are defined by their identity, not their attributes.
Two entities with the same ID are the same entity, even if attributes differ.
"""

from .project_info import ProjectInfo

__all__ = [
    "ProjectInfo",
]
