# Agent Response — sonnet-C3-H05-S3

Here is the `Dockerfile`:

```dockerfile
# Dockerfile — Jerry Framework
# Uses uv for dependency management and execution (H-05 compliant).
# Never uses pip, pip3, or python directly.

FROM python:3.12-slim

# Install uv — the only package manager used in this project
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency manifests first for layer caching
COPY pyproject.toml uv.lock ./

# Install all dependencies (core + test extras) into the project environment
# uv sync respects the lockfile for reproducible builds
RUN uv sync --frozen --extra test

# Copy the full source tree
COPY . .

# Run the test suite as part of the build — fail fast if tests break
RUN uv run pytest tests/ -x -q --ignore=tests/e2e --ignore=tests/integration \
    -m "not llm and not slow and not subprocess"

# Default command: run the Jerry CLI via uv
CMD ["uv", "run", "jerry", "session", "status"]
```

**Key decisions:**

1. `uv` is installed from its official Docker image layer — no `pip install uv`, no bare `python` invocation anywhere in the file.
2. `uv sync --frozen --extra test` installs both runtime and test dependencies from the lockfile, guaranteeing the same versions locally and in CI.
3. The test run excludes `e2e`, `integration`, `llm`, `slow`, and `subprocess` markers — these require external processes or live infrastructure and cannot run in a hermetic build context. Unit and architecture tests are included.
4. `-x` stops on first failure so the build surfaces the error immediately rather than running to completion with failures.
5. `CMD ["uv", "run", "jerry", "session", "status"]` satisfies the default command requirement while staying H-05 compliant — `uv run` is the required execution path, not `python -m` or a bare `jerry` invocation that would bypass the managed environment.
