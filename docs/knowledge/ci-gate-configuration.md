# CI Gate Configuration

> Branch protection and CI pipeline recommendations for the Jerry Framework skill composition pipeline.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Pre-Commit Hooks](#pre-commit-hooks) | Local defense-in-depth hooks |
| [Branch Protection (FM-01)](#branch-protection-fm-01) | Preventing `--no-verify` bypass |
| [CI Jobs](#ci-jobs) | Authoritative pipeline gates |

---

## Pre-Commit Hooks

Pre-commit hooks provide local defense-in-depth validation. They are **not** authoritative gates — developers can bypass them with `--no-verify`. See `.pre-commit-config.yaml` for the full hook list.

Skill composition hooks:

| Hook ID | Purpose | Trigger Files |
|---------|---------|---------------|
| `skill-compose-validation` | SCV-001 through SCV-007 checks on composed SKILL.md | `skills/*/SKILL.md`, `skills/*/composition/skill.jerry.yaml` |
| `skill-schema-validation` | JSON Schema validation of frontmatter and canonical YAML | Same as above + `docs/schemas/*skill*.json` |

## Branch Protection (FM-01)

The `--no-verify` flag bypasses all pre-commit hooks. This is an intentional git escape hatch for emergencies, but it means local validation can be skipped entirely.

**Recommendation:** Configure branch protection rules on `main` and `develop` branches to require CI status checks to pass before merge.

**Required CI checks** (map to pre-commit hook IDs in `.pre-commit-config.yaml`):

| Pre-Commit Hook ID | CI Job Name | Validates |
|--------------------|-------------|-----------|
| `skill-compose-validation` | Match hook ID or GitHub Actions job name | SCV-001 through SCV-007 post-composition checks |
| `skill-schema-validation` | Match hook ID or GitHub Actions job name | JSON Schema validation (`check_skill_schemas.py --all`) |
| `pytest` | Match hook ID or GitHub Actions job name | Full test suite including composition pipeline tests |

**Note:** The CI job names in branch protection must match the `name:` field of the corresponding GitHub Actions workflow job. If the repository uses a CI workflow file (e.g., `.github/workflows/ci.yml`), verify the job names match before configuring branch protection. The pre-commit hook IDs above serve as reference identifiers — actual CI job names depend on the workflow configuration.

**GitHub Settings Path:**
1. Repository Settings > Branches > Branch protection rules
2. Add rule for `main` (and `develop` if applicable)
3. Enable "Require status checks to pass before merging"
4. Search for and add the CI job names from your workflow
5. Verify that the required checks correspond to the hooks listed above

This ensures that even if a developer uses `--no-verify` locally, the CI pipeline catches validation failures before code reaches protected branches.

## CI Jobs

CI provides the authoritative validation gate. Pre-commit hooks are defense-in-depth that catch issues earlier in the workflow.

| Layer | Mechanism | Bypass Risk |
|-------|-----------|-------------|
| Pre-commit (local) | `.pre-commit-config.yaml` hooks | `--no-verify` bypasses all hooks |
| CI (authoritative) | GitHub Actions workflow jobs | Cannot be bypassed without branch protection changes |
| Branch protection | Required status checks | Requires admin access to modify |

---

*Source: FM-01 (FMEA finding, RPN 126). See `projects/PROJ-012-agent-optimization/reviews/s-012-fmea-skill-pipeline.md`.*
