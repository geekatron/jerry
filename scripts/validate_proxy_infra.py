# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Validate proxy_infra scaffold against enforcement rules."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.infrastructure.internal.enforcement.pre_tool_enforcement_engine import (
    PreToolEnforcementEngine,
)

engine = PreToolEnforcementEngine()
root = Path("src/proxy_infra")
violations: list[tuple[str, str]] = []
checked = 0

for f in sorted(root.rglob("*.py")):
    if "__pycache__" in str(f):
        continue
    content = f.read_text()
    decision = engine.evaluate_write(str(f.resolve()), content)
    if decision.action == "block":
        violations.append((str(f), decision.reason))
    checked += 1

if violations:
    for path, reason in violations:
        print(f"BLOCK: {path}")
        print(f"  {reason}")
    sys.exit(1)
else:
    print(f"OK: {checked} files pass enforcement checks.")
    sys.exit(0)
