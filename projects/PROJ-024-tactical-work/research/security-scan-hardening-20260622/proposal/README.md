# Security Scan Hardening — Proposal Staging Directory

> PROPOSAL ONLY. These drafts await owner approval before any file is moved to `.github/`.
> Do NOT copy files here directly into the live repo. See "Deployment Checklist" below.

## Navigation

| Section | Purpose |
|---------|---------|
| [Draft File Map](#draft-file-map) | Each draft and its intended final destination |
| [Deployment Checklist](#deployment-checklist) | Steps to promote drafts to live |
| [Pre-requisites](#pre-requisites) | One-time repo setup needed before deploying |

---

## Draft File Map

| Draft File (in this directory) | Intended Final Destination | Notes |
|-------------------------------|---------------------------|-------|
| `action.yml` | `.github/actions/security-audit/action.yml` | Create the directory first |
| `ci.yml.security-job.draft` | Replaces the `security:` job block in `.github/workflows/ci.yml` | Paste block only; rest of ci.yml unchanged |
| `security-scan.yml.draft` | `.github/workflows/security-scan.yml` | Full file replacement |
| `audit-allowlist.yml` | `.github/security/audit-allowlist.yml` | Create the directory first |
| `scripts/security/audit_allowlist.py` | `scripts/security/audit_allowlist.py` | Create the directory first |
| `CODEOWNERS.addition` | Append two lines to `.github/CODEOWNERS` | Not a full replacement — append only; see file for exact lines |
| `VERIFY.md` | `projects/PROJ-024-tactical-work/research/security-scan-hardening-20260622/VERIFY.md` | Keep in research; not deployed to live repo root |

---

## Deployment Checklist

Run after the owner approves the ADR and these proposals.

1. Create required directories (idempotent):
   ```bash
   mkdir -p .github/actions/security-audit
   mkdir -p .github/security
   mkdir -p scripts/security
   ```

2. Create the "security-alert" label in the repo (one-time):
   ```bash
   gh label create "security-alert" \
     --color "d93f0b" \
     --description "Open CVE found in dependency tree"
   ```

3. Copy artifact files:
   ```bash
   cp proposal/action.yml .github/actions/security-audit/action.yml
   cp proposal/audit-allowlist.yml .github/security/audit-allowlist.yml
   cp proposal/scripts/security/audit_allowlist.py scripts/security/audit_allowlist.py
   ```

4. Append CODEOWNERS entries (do NOT overwrite; append only):
   ```bash
   # Read proposal/CODEOWNERS.addition for the exact lines and syntax rationale.
   # The two patterns use unescaped dots — matching the existing CODEOWNERS style.
   cat >> .github/CODEOWNERS << 'EOF'

   # Composite action and accept-list files
   .github/actions/   @geekatron
   .github/security/  @geekatron
   EOF
   ```

5. Apply the ci.yml security job patch:
   Open `.github/workflows/ci.yml` and replace the `security:` job block
   (lines 68-106) with the content of `proposal/ci.yml.security-job.draft`.

6. Replace security-scan.yml:
   ```bash
   cp proposal/security-scan.yml.draft .github/workflows/security-scan.yml
   ```

7. Run the local verification playbook to confirm RED before any dep bumps:
   See `VERIFY.md` — Claim A.

8. Bump the 9 CVE-affected packages and re-verify GREEN:
   See `VERIFY.md` — Claim B.

9. Commit and open a PR:
   ```bash
   git add .github/actions/ .github/security/ .github/workflows/ci.yml \
           .github/workflows/security-scan.yml scripts/security/ .github/CODEOWNERS
   git commit -m "ci: add security-audit composite action with CVE accept-list"
   ```

---

## Pre-requisites

- The `yaml` (PyYAML) package must be available in the `uv` environment.
  Verify: `uv run python -c "import yaml; print(yaml.__version__)"`.
  It is already present as a transitive dep of `mkdocs-material`.
  If it ever becomes direct: `uv add pyyaml`.

- `gh` CLI must be authenticated in the Actions environment.
  The scheduled workflow uses `secrets.GITHUB_TOKEN` (automatically provided).
  No additional secret setup is required.

- The `"security-alert"` label must exist in the repo before the first scheduled
  run after deployment.  See step 2 of the deployment checklist above.
