```dockerfile
FROM python:3.12-slim

# Install uv -- the project's required package manager (H-05: uv-only environment)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency manifests first for layer caching
COPY pyproject.toml uv.lock ./

# Install all dependencies including test extras
# uv sync installs into the project's virtual environment
RUN uv sync --extra test --frozen

# Copy application source
COPY src/ ./src/
COPY tests/ ./tests/

# Run the test suite as part of the build -- catches issues early
# Uses uv run per H-05 (never python/pytest directly)
RUN uv run pytest --tb=short -q

# Default command: run the Jerry CLI session status
CMD ["uv", "run", "jerry", "session", "status"]
```
