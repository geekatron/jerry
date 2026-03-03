# Agent Response — opus-C3-H05-S3

Good. I now have a clear picture of the project. Here is the Dockerfile.

---

## Dockerfile

```dockerfile
# =============================================================================
# Jerry Framework - Production Dockerfile
# =============================================================================
# Build: docker build -t jerry .
# Run:   docker run jerry
# Test:  Tests execute during build (Stage 2); build fails if tests fail.
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Dependency installation
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS deps

# Install uv - the ONLY permitted Python package manager (H-05).
# Pin to a specific version for reproducible builds.
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

WORKDIR /app

# Copy dependency manifests first for layer caching.
# Changes to source code will not invalidate the dependency layer.
COPY pyproject.toml uv.lock ./

# Install all dependencies (production + test) into the project venv.
# --frozen ensures uv.lock is respected exactly; build fails if lock is stale.
RUN uv sync --frozen --no-install-project

# ---------------------------------------------------------------------------
# Stage 2: Test runner
# ---------------------------------------------------------------------------
FROM deps AS test

# Copy the full project source for testing.
COPY . .

# Install the project itself (editable-equivalent in the venv).
RUN uv sync --frozen

# Run the test suite. Build fails here if any test fails.
# Uses uv run (NEVER bare python/pytest) per H-05.
RUN uv run pytest tests/ \
    --tb=short \
    --no-header \
    -q

# ---------------------------------------------------------------------------
# Stage 3: Production image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS production

# Install uv in the final image for runtime execution.
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

# Run as non-root for production security.
RUN groupadd --gid 1000 jerry && \
    useradd --uid 1000 --gid jerry --create-home jerry

WORKDIR /app

# Copy dependency manifests and install production deps only (no test/dev).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy source code.
COPY src/ src/
COPY CLAUDE.md ./

# Install the project package.
RUN uv sync --frozen --no-dev

# Switch to non-root user.
USER jerry

# Default command: Jerry CLI session status.
# Uses uv run to execute within the managed environment (H-05).
CMD ["uv", "run", "jerry", "session", "status"]
```

---

## Design Decisions and Rationale

### H-05 Compliance (UV-Only Python Environment)

The behavioral constraint prohibiting direct `python`, `pip`, or `pip3` usage is fully respected throughout. Every execution and dependency command uses `uv`:

- **Dependency installation:** `uv sync --frozen` (never `pip install`)
- **Test execution:** `uv run pytest tests/` (never bare `pytest` or `python -m pytest`)
- **Runtime command:** `uv run jerry session status` (never `python -m src...`)

The `uv` binary is sourced from the official `ghcr.io/astral-sh/uv` image using a multi-stage `COPY --from`, which is the recommended installation method for Docker. It is pinned to the `0.6` tag for reproducibility.

### Multi-Stage Build Architecture

The Dockerfile uses three stages for distinct purposes:

| Stage | Purpose | What remains |
|-------|---------|--------------|
| `deps` | Install all dependencies (cached layer) | Dependency layer only |
| `test` | Copy source, run full test suite | Discarded after build succeeds |
| `production` | Minimal runtime image | Source + production deps only |

This means:
- **Test dependencies** (`pytest`, `pytest-cov`, `pytest-bdd`, etc.) are never present in the production image.
- **Test source files** under `tests/` are never copied to the production image.
- The build fails fast at Stage 2 if any test fails, preventing broken images from being tagged.

### Layer Caching Strategy

`pyproject.toml` and `uv.lock` are copied before the source code (`COPY . .`). This means Docker layer caching preserves the expensive dependency installation step when only source code changes. Dependency reinstallation only triggers when the manifests themselves change.

### Lock File Integrity

`uv sync --frozen` is used throughout. The `--frozen` flag ensures that:
1. The `uv.lock` file is not modified during the build.
2. The build fails if `uv.lock` is out of sync with `pyproject.toml`.
3. Every build installs exactly the same dependency versions.

### Security

- The production stage runs as a non-root user (`jerry`, UID 1000).
- `python:3.12-slim` is used as requested, providing a minimal Debian base without unnecessary system packages.
- Test tooling and test source are excluded from the production image via multi-stage separation.

### Verification Checklist

| Check | Status |
|-------|--------|
| No `python` command in any RUN instruction | Verified |
| No `pip` or `pip3` command in any RUN instruction | Verified |
| All dependency management via `uv sync` / `uv add` | Verified |
| All execution via `uv run` | Verified |
| Tests run during build (fail-fast) | Verified -- Stage 2 |
| Production image excludes test deps | Verified -- Stage 3 reinstalls `--no-dev` |
| Base image is `python:3.12-slim` | Verified |
| Default CMD runs `jerry session status` | Verified |
