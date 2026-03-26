# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""CredentialDescriptor value object — paths to a node's generated SSH keypair.

References:
    - TASK-023-033: Credential generation specification
    - STORY-023-005: Ephemeral Credential Lifecycle
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CredentialDescriptor:
    """Immutable descriptor for a node's generated SSH credential material.

    Contains only filesystem paths and the node identifier — never raw
    credential values — so it is safe to pass between layers without
    risk of accidentally logging sensitive material.

    Attributes:
        node_id: The proxy node this credential set belongs to.
        private_key_path: Absolute path to the Ed25519 private key file (0600).
        public_key_path: Absolute path to the corresponding public key file.
    """

    node_id: str
    private_key_path: str
    public_key_path: str
