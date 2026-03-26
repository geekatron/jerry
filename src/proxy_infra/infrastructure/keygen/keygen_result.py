# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""KeygenResult value object — paths to generated SSH keypair files (H-10: one class per file)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KeygenResult:
    """Result of SSH keypair generation.

    Attributes:
        private_key_path: Path to the generated Ed25519 private key file.
        public_key_path: Path to the generated Ed25519 public key file (.pub).
    """

    private_key_path: Path
    public_key_path: Path
