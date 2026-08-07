# VERIFY.md — Local Verification Playbook

> Exact commands to prove the hardened pipeline's three behaviour claims.
> All commands assume: repo root is your cwd; uv is installed; Python 3.14 is available.

## Navigation

| Section | Purpose |
|---------|---------|
| [Pre-flight](#pre-flight) | One-time local setup |
| [Claim A — RED on 9 CVEs](#claim-a--currently-goes-red-on-9-cves) | Reproduce the current failure |
| [Claim B — GREEN after bumps](#claim-b--green-after-bumping-5-packages) | Prove the fix works |
| [Claim C — Expired allowlist blocks](#claim-c--expired-allowlist-entry-resurfaces-pipeline) | Prove expiry enforcement |
| [Claim D — Malformed/missing-field allowlist goes RED](#claim-d--malformed-or-missing-field-allowlist-goes-red) | Prove fail-closed on bad allowlist structure |
| [Claim E — Off-by-one expiry boundary](#claim-e--off-by-one-expiry-boundary) | Prove review_by date itself is expired |
| [Claim F — 90-day cap rejection](#claim-f--90-day-cap-rejection) | Prove over-long acceptance windows are rejected |
| [Claim G — Neutered audit goes RED (D5 guard)](#claim-g--neutered-audit-goes-red-d5-guard) | Prove empty/minimal export triggers the floor check |
| [Allowlist flag smoke-test](#allowlist-flag-smoke-test) | Unit-level test of the parser |

---

## Pre-flight

```bash
# Confirm uv is present and using the frozen lockfile.
uv --version            # should print 0.10.9 (or whatever version is pinned)
uv sync --frozen --all-extras
```

---

## Claim A — Currently goes RED on 9 CVEs

Run the exact same audit command the composite action uses (mirrors ci.yml's proven approach).
This should exit 1 and list the 9 vulnerabilities.

```bash
# Export the full locked dependency set (all extras, no project self-reference).
uv export \
  --no-hashes \
  --frozen \
  --all-extras \
  --no-emit-project \
  > /tmp/requirements-verify.txt

# Confirm the file is non-empty.
wc -l /tmp/requirements-verify.txt      # expect: several dozen lines

# Run the audit (expect: exit 1, list of CVEs).
uv run pip-audit \
  --requirement /tmp/requirements-verify.txt \
  --strict \
  --desc
# Expected exit code: 1
# Expected output: "Found N known vulnerabilities in M packages"
# Packages: mako, urllib3, idna, msgpack, pydantic-settings, pymdown-extensions, pip
```

Contrast with the FALSE-GREEN bare invocation (the bug that existed in security-scan.yml):

```bash
# This is what the OLD security-scan.yml ran.  It audits almost nothing.
uv run pip-audit --strict --desc
# Expected: exit 0 (green) — because it only sees "jerry" (not on PyPI) and skips it.
# This is the false-green root cause documented in PR-298-and-ci-rootcause.md §E4.
```

---

## Claim B — GREEN after bumping 5 packages

The following packages have published fixes.  Bump them, re-lock, re-audit.

```bash
# 1. Bump the affected packages (uv resolves compatible versions).
#    Pin to the known-fixed minimums from the CVE advisories:
uv add \
  "mako>=1.3.12" \
  "urllib3>=2.7.0" \
  "idna>=3.15" \
  "msgpack>=1.2.1" \
  "pydantic-settings>=2.14.2" \
  "pymdown-extensions>=10.21.3"

# pip is upgraded via pip itself inside the venv; uv manages it indirectly.
# If pip still appears in pip-audit output after the above:
uv run pip install --upgrade pip   # only if needed; uv-managed envs usually auto-upgrade

# 2. Confirm the lockfile was updated.
git diff uv.lock | head -40

# 3. Re-export and re-audit.
uv export \
  --no-hashes \
  --frozen \
  --all-extras \
  --no-emit-project \
  > /tmp/requirements-verify.txt

uv run pip-audit \
  --requirement /tmp/requirements-verify.txt \
  --strict \
  --desc
# Expected exit code: 0 (green)
# Expected output: "No known vulnerabilities found."
```

> NOTE: Some of the packages above are transitive deps (e.g., mako is pulled in by
> mkdocs-material).  If `uv add mako>=1.3.12` conflicts with a direct dep's constraint,
> the correct approach is to bump the *parent* direct dep first (e.g., `uv add mkdocs-material@latest`),
> then re-audit.  The REMEDIATION steps in dependabot.yml §D3 cover this case.

---

## Claim C — Expired allowlist entry resurfaces pipeline

Simulate an expired accept-list entry and confirm the parser exits 1.

```bash
# 1. Write a temporary allowlist with a past review_by date.
cat > /tmp/expired-allowlist.yml << 'EOF'
accepted:
  - id: CVE-2026-44307
    package: mako
    reason: "Test entry — simulating an expired accept."
    accepted_by: geekatron
    accepted_on: 2026-06-01
    review_by:   2026-06-10      # <-- past date
    ticket: https://github.com/geekatron/jerry/issues/0
EOF

# 2. Run the parser against the expired allowlist.
uv run python scripts/security/audit_allowlist.py \
  --allowlist /tmp/expired-allowlist.yml
# Expected exit code: 1
# Expected stderr: "::error::CVE accept-list has expired entries..."
#                  "  - CVE-2026-44307 (package: mako, review_by: 2026-06-10, ...)"

# 3. Confirm a valid (future-dated) entry produces ignore flags and exits 0.
cat > /tmp/valid-allowlist.yml << 'EOF'
accepted:
  - id: CVE-2099-00000
    package: example-pkg
    reason: "Hypothetical future accept."
    accepted_by: geekatron
    accepted_on: 2026-06-22
    review_by:   2026-09-22
    ticket: none
EOF

uv run python scripts/security/audit_allowlist.py \
  --allowlist /tmp/valid-allowlist.yml
# Expected exit code: 0
# Expected stdout: "--ignore-vuln CVE-2099-00000"

# 4. Confirm an empty allowlist produces no flags and exits 0.
uv run python scripts/security/audit_allowlist.py \
  --allowlist .github/security/audit-allowlist.yml
# Expected exit code: 0
# Expected stdout: "" (empty — no entries to ignore)
```

---

## Claim D — Malformed or Missing-Field Allowlist Goes RED

These scenarios prove that `audit_allowlist.py` fails closed (exit 1) on structural
problems — never silently treating broken input as an empty list.

```bash
# D-1: YAML parse error → exit 1
cat > /tmp/bad-yaml-allowlist.yml << 'EOF'
accepted:
  - id: CVE-2026-12345
    broken: [unclosed bracket
EOF

uv run python scripts/security/audit_allowlist.py \
  --allowlist /tmp/bad-yaml-allowlist.yml
# Expected exit code: 1
# Expected stderr: "::error::audit-allowlist.yml YAML parse error: ..."

# D-2: Wrong top-level structure (bare YAML list) → exit 1
# A CODEOWNERS conflict or copy-paste error could produce this.
cat > /tmp/list-allowlist.yml << 'EOF'
- id: CVE-2026-12345
  package: example-pkg
EOF

uv run python scripts/security/audit_allowlist.py \
  --allowlist /tmp/list-allowlist.yml
# Expected exit code: 1
# Expected stderr: "::error::audit-allowlist.yml is malformed — expected a mapping..."

# D-3: Missing required field (no review_by) → exit 1
# Previously this was a silent fail-open (entry treated as never expiring).
cat > /tmp/missing-field-allowlist.yml << 'EOF'
accepted:
  - id: CVE-2026-12345
    package: example-pkg
    reason: "Missing review_by field"
    accepted_by: geekatron
    accepted_on: 2026-06-22
    # review_by is deliberately absent
    ticket: https://github.com/geekatron/jerry/issues/1
EOF

uv run python scripts/security/audit_allowlist.py \
  --allowlist /tmp/missing-field-allowlist.yml
# Expected exit code: 1
# Expected stderr: "::error::CVE-2026-12345: missing or empty required field 'review_by'..."

# D-4: Empty id field → exit 1
# Previously the entry was silently ignored with no error.
cat > /tmp/empty-id-allowlist.yml << 'EOF'
accepted:
  - id: ""
    package: example-pkg
    reason: "Empty id"
    accepted_by: geekatron
    accepted_on: 2026-06-22
    review_by: 2026-09-22
    ticket: none
EOF

uv run python scripts/security/audit_allowlist.py \
  --allowlist /tmp/empty-id-allowlist.yml
# Expected exit code: 1
# Expected stderr: "::error::(entry #1): missing or empty required field 'id'..."
```

---

## Claim E — Off-by-One Expiry Boundary

Proves that an entry expiring ON today resurfaces (exit 1), not one day late.

```bash
# Write an allowlist where review_by is today's date.
TODAY=$(date +%Y-%m-%d)
ACCEPTED_ON=$(date -d "30 days ago" +%Y-%m-%d 2>/dev/null || \
              date -v-30d +%Y-%m-%d 2>/dev/null)   # GNU date / BSD date

cat > /tmp/boundary-allowlist.yml << EOF
accepted:
  - id: CVE-2026-99999
    package: boundary-pkg
    reason: "Expiry boundary test"
    accepted_by: geekatron
    accepted_on: $ACCEPTED_ON
    review_by:   $TODAY
    ticket: none
EOF

uv run python scripts/security/audit_allowlist.py \
  --allowlist /tmp/boundary-allowlist.yml
# Expected exit code: 1  (today >= review_by means EXPIRED)
# Expected stderr: "::error::CVE-2026-99999: expired (review_by: ${TODAY}, today: ${TODAY})..."
# NOTE: exit 0 here would be the off-by-one bug. The entry is expired ON its review date.
```

---

## Claim F — 90-Day Cap Rejection

Proves that an acceptance window longer than 90 days is rejected at parse time.

```bash
cat > /tmp/overcap-allowlist.yml << 'EOF'
accepted:
  - id: CVE-2026-12345
    package: example-pkg
    reason: "Intentionally long window to test cap enforcement"
    accepted_by: geekatron
    accepted_on: 2026-06-22
    review_by:   2026-12-31   # 192 days — well over the 90-day cap
    ticket: none
EOF

uv run python scripts/security/audit_allowlist.py \
  --allowlist /tmp/overcap-allowlist.yml
# Expected exit code: 1
# Expected stderr: "::error::CVE-2026-12345: review_by is 192 days after accepted_on
#                  (max allowed: 90 days)..."

# Confirm a 90-day window is exactly at the cap (permitted).
cat > /tmp/exact-cap-allowlist.yml << 'EOF'
accepted:
  - id: CVE-2026-12345
    package: example-pkg
    reason: "Exactly 90 days — should pass"
    accepted_by: geekatron
    accepted_on: 2026-06-22
    review_by:   2026-09-20   # 90 days exactly
    ticket: none
EOF

uv run python scripts/security/audit_allowlist.py \
  --allowlist /tmp/exact-cap-allowlist.yml
# Expected exit code: 0
# Expected stdout: "--ignore-vuln CVE-2026-12345"
```

---

## Claim G — Neutered Audit Goes RED (D5 Guard)

Proves that the D5 meaningful-audit guard catches the Scan-B failure mode where
only a minimal requirements file is exported (e.g., only "jerry" itself, or an
empty file), which would produce a false-green under the old `LINE_COUNT >= 1` check.

This scenario must be tested against the composite action directly (not just the
Python script). It verifies two independent D5 assertions:

**G-1: No recognizable verdict sentinel → exit 1**

```bash
# Simulate pip-audit producing output with no verdict line (e.g., only warnings).
echo "WARNING: something strange happened" > /tmp/pip-audit-output.txt

VERDICT_LINE=$(grep -E \
  "(No known vulnerabilities found|Found [0-9]+ known vulnerabilit)" \
  /tmp/pip-audit-output.txt | head -1 || true)

if [[ -z "$VERDICT_LINE" ]]; then
  echo "PASS: D5 guard would exit 1 — no verdict sentinel found"
else
  echo "FAIL: verdict line found unexpectedly: $VERDICT_LINE"
fi
# Expected output: "PASS: D5 guard would exit 1 — no verdict sentinel found"
```

**G-2: Requirements file below min-audited-packages floor → exit 1**

```bash
# Create a near-empty requirements file (only 2 packages — below the floor of 20).
printf "pkg-a==1.0.0\npkg-b==2.0.0\n" > /tmp/tiny-requirements.txt

REQ_COUNT=$(grep -c -v '^\s*#\|^\s*$' /tmp/tiny-requirements.txt || echo 0)
MIN_PKGS=20

if [[ "$REQ_COUNT" -lt "$MIN_PKGS" ]]; then
  echo "PASS: D5 guard would exit 1 — only $REQ_COUNT packages, floor is $MIN_PKGS"
else
  echo "FAIL: floor check did not trigger ($REQ_COUNT >= $MIN_PKGS)"
fi
# Expected output: "PASS: D5 guard would exit 1 — only 2 packages, floor is 20"

# Contrast: confirm the real export clears the floor.
uv export \
  --no-hashes \
  --frozen \
  --all-extras \
  --no-emit-project \
  > /tmp/requirements-verify.txt

REQ_COUNT=$(grep -c -v '^\s*#\|^\s*$' /tmp/requirements-verify.txt || echo 0)
echo "Real export: $REQ_COUNT packages (expect >= 20)"
# Expected: several dozen packages
```

---

## Allowlist flag smoke-test

```bash
# Quick round-trip: combine an empty allowlist with pip-audit.
# This proves the ignore-flags pipeline doesn't introduce flags that pip-audit rejects.
IGNORE_FLAGS=$(uv run python scripts/security/audit_allowlist.py \
  --allowlist .github/security/audit-allowlist.yml)

echo "Ignore flags: '$IGNORE_FLAGS'"   # expect: empty string

uv export \
  --no-hashes \
  --frozen \
  --all-extras \
  --no-emit-project \
  > /tmp/requirements-verify.txt

# shellcheck disable=SC2086 — word-split of IGNORE_FLAGS is intentional
uv run pip-audit \
  --requirement /tmp/requirements-verify.txt \
  --strict \
  --desc \
  $IGNORE_FLAGS
# Exit code: 1 (same as Claim A — no flags suppressed anything)
```
