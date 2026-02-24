# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Agents Bounded Context - Canonical Agent Build Pipeline.

Provides vendor-agnostic agent definition management:
- Canonical source format (.agent.yaml + .prompt.md)
- Build pipeline to generate vendor-specific agent files
- Extract pipeline to reverse-engineer canonical from existing files
- Validation and drift detection

CLI: jerry agents build|extract|validate|list|diff

References:
    - ADR-PROJ010-003: LLM Portability Architecture
    - agent-development-standards.md: H-34 agent definition standards
"""
