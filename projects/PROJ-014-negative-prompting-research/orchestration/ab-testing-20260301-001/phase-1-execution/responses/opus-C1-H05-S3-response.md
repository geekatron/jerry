Here is a production-ready Dockerfile for the Jerry Framework. It uses `uv` throughout for both dependency installation and Python execution, consistent with the project's H-05 constraint (UV-only Python environment).

```dockerfile
# =============================================================================
# Jerry Framework Dockerfile
# Base: python:3.12-slim | Build: uv | Runtime: uv run
# =============================================================================

FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install uv -- the project's mandatory Python package manager (H-05)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# ---------------------------------------------------------------------------
# Stage 1: Install dependencies (cached layer)
# ---------------------------------------------------------------------------
# Copy only dependency-specification files first to maximize Docker layer caching.
# Changes to source code will not invalidate the dependency layer.
COPY pyproject.toml uv.lock ./

# Install all dependency groups: core + dev + test
# uv sync reads pyproject.toml and uv.lock for reproducible installs.
RUN uv sync --frozen --no-install-project

# ---------------------------------------------------------------------------
# Stage 2: Install project + run tests
# ---------------------------------------------------------------------------
# Copy the full project source
COPY . .

# Install the project itself (editable-like install into the venv)
RUN uv sync --frozen

# Run the test suite during build to catch issues early.
# A test failure here will fail the Docker build, preventing broken images.
RUN uv run pytest tests/ \
    --tb=short \
    -q \
    --no-header

# ---------------------------------------------------------------------------
# Runtime configuration
# ---------------------------------------------------------------------------
# Default command: Jerry CLI session status
ENTRYPOINT ["uv", "run", "jerry"]
CMD ["session", "status"]
```

**Key design decisions:**

1. **`uv` for everything** -- Dependencies are installed via `uv sync` and all Python execution uses `uv run`, satisfying the H-05 constraint. No direct `pip` or `python` invocations appear anywhere in the file.

2. **Layer caching** -- `pyproject.toml` and `uv.lock` are copied before the full source tree. This means dependency installation is cached and only re-runs when those files change, not on every source code edit.

3. **`--frozen` flag** -- Ensures `uv sync` uses the exact versions from `uv.lock` without attempting to update the lockfile, giving reproducible builds.

4. **Tests as build gate** -- `uv run pytest` runs during the image build. If any test fails, the build fails and no image is produced. This catches regressions before the image is ever pushed or deployed.

5. **ENTRYPOINT/CMD split** -- `ENTRYPOINT` sets `uv run jerry` as the base command; `CMD` provides the default arguments (`session status`). This allows overriding arguments at runtime: `docker run jerry-image session start` would work as expected while the default remains `session status`.
