# Agent Response — sonnet-C2-H05-S3

Here is the Dockerfile. The key design decision is that the project uses `uv` for all Python execution and dependency management (H-05: UV-only environment — `python`/`pip`/`pip3` are never used directly). This constraint extends into the container: the Dockerfile installs `uv` and uses it throughout rather than reaching for `pip install`.

---

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

# Install uv — the project's required package manager (H-05: UV-only environment)
# uv replaces pip/pip3 for all dependency installation and Python execution.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency manifests first to maximize layer cache reuse.
# The installed deps layer only rebuilds when pyproject.toml or uv.lock changes.
COPY pyproject.toml uv.lock ./

# Install all runtime + test dependencies into the project virtual environment.
# --frozen: fail the build if uv.lock is out of sync with pyproject.toml.
# --extra test: include the [test] optional group needed for the test stage.
RUN uv sync --frozen --extra test

# Copy the full project source.
COPY . .

# ---------------------------------------------------------------------------
# Test stage — runs the suite as part of the build (fail-fast on breakage).
# ---------------------------------------------------------------------------
FROM base AS test

RUN uv run pytest tests/ --tb=short -q

# ---------------------------------------------------------------------------
# Production stage — lean final image without test dependencies.
# ---------------------------------------------------------------------------
FROM base AS production

# Install only runtime dependencies (no test extras) for the production image.
RUN uv sync --frozen

# jerry session status is the default entrypoint.
CMD ["uv", "run", "jerry", "session", "status"]
```

---

**Build commands:**

```bash
# Run tests as part of the build (CI / local verification):
docker build --target test -t jerry:test .

# Build the production image (tests are NOT re-run in this stage,
# but the build will have failed earlier if the test stage failed):
docker build --target production -t jerry:latest .
```

---

**Design decisions:**

**`uv` as the package manager.** The project enforces H-05 (UV-only): no `pip`, `pip3`, or direct `python` invocations. Inside the container this means installing `uv` from the official image layer (`ghcr.io/astral-sh/uv:latest`) and using `uv sync` / `uv run` throughout. There is no `pip install` anywhere in this file.

**`--frozen` flag on `uv sync`.** This causes the build to fail if `uv.lock` is out of sync with `pyproject.toml`. Without it, uv would silently regenerate the lockfile and the container would be running untested dependency combinations. In a team Dockerfile, lockfile drift is a silent correctness hazard.

**Two-stage build (test + production).** The `test` stage runs the full test suite against the installed source. The `production` stage re-installs from the same lockfile but omits `--extra test`, keeping the final image smaller and free of pytest, pytest-bdd, and coverage tooling. This matches the stated goal: "run the test suite as part of the build to catch issues early" without inflating the production artifact.

**`CMD` vs `ENTRYPOINT`.** `CMD` is used rather than `ENTRYPOINT` so the default can be overridden at `docker run` time without needing `--entrypoint`. For a team tool this is more ergonomic: `docker run jerry:latest jerry items list` works without flags.

**`uv run jerry session status` as CMD.** `uv run` ensures the command executes inside the managed virtual environment created by `uv sync`, which is where the `jerry` entry point script was installed. Calling `jerry` directly (without `uv run`) would fail unless the venv's `bin/` directory is on `PATH`, which is an unnecessary coupling.
