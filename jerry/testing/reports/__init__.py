# SPDX-License-Identifier: Apache-2.0
"""Report generation package for the Four-Layer Composite Test Harness.

Produces structured regression reports in both Markdown (for PR comments) and
JSON (for artifact archiving) formats, and the ReportOutputPort protocol for
dependency inversion.

Public API:
    from jerry.testing.reports import ReportGenerator
    from jerry.testing.reports import ReportOutputPort
"""

from jerry.testing.reports.generator import ReportGenerator
from jerry.testing.reports.ports import ReportOutputPort

__all__ = ["ReportGenerator", "ReportOutputPort"]
