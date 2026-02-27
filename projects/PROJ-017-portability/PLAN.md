# PROJ-017: Platform Portability

## Overview

Cross-platform compatibility fixes to ensure Jerry works on Windows, macOS, and Linux.

## Status

- **Created:** 2026-02-26
- **Status:** Active
- **Source:** PORT-001 Portability Analysis

## Work Items

| ID | Type | Title | GitHub Issue | Status |
|----|------|-------|--------------|--------|
| BUG-017-001 | Bug | statusLine uses python3 (Windows) | [#113](https://github.com/geekatron/jerry/issues/113) | Open |
| BUG-017-002 | Bug | Migration scripts bash-only | [#114](https://github.com/geekatron/jerry/issues/114) | Open |
| BUG-017-003 | Bug | Symlinks need elevated privileges (Windows) | [#115](https://github.com/geekatron/jerry/issues/115) | Open |
| BUG-017-004 | Bug | Missing .gitattributes | [#116](https://github.com/geekatron/jerry/issues/116) | Open |
| BUG-017-005 | Bug | Hardcoded path separator | [#117](https://github.com/geekatron/jerry/issues/117) | Open |
| BUG-017-006 | Bug | macOS symlink resolution | [#118](https://github.com/geekatron/jerry/issues/118) | Open |
| BUG-017-007 | Bug | /tmp in docstrings | [#119](https://github.com/geekatron/jerry/issues/119) | Open |

## Analysis Artifacts

- `skills/eng-team/output/PORT-001/eng-security-portability-analysis.md` - Full analysis
- `skills/eng-team/output/PORT-001/issue-drafts.md` - Issue draft templates
- `skills/eng-team/output/PORT-001/adv-scorer-quality-report.md` - Quality gate results
