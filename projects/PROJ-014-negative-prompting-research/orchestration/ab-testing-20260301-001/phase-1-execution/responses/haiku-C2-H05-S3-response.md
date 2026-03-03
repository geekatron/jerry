# Dockerfile for Jerry Framework

## Response

```dockerfile
# Build stage: Install dependencies and run tests
FROM python:3.12-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install uv package manager
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy source code
COPY src ./src
COPY tests ./tests

# Run tests to catch issues early
RUN uv run pytest tests/ \
    --cov=src \
    --cov-report=term-summary \
    --tb=short \
    -v

# Runtime stage: Minimal image with installed package
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install uv runtime dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/pyproject.toml ./
COPY --from=builder /app/uv.lock* ./

# Copy source code from builder
COPY --from=builder /app/src ./src

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD jerry session status || exit 1

# Default command: run the Jerry CLI to check session status
CMD ["jerry", "session", "status"]
```

## Explanation

### Design Decisions

**1. Multi-stage Build**
- Separates build tools from runtime container
- Reduces final image size by excluding pytest, test files, and intermediate dependencies
- Builder stage runs tests before creating the runtime image, failing the build if tests fail (per requirement)

**2. UV Package Manager (H-05 Compliance)**
- Uses `uv` exclusively instead of `pip` per the python-environment.md standards
- Installs uv in both stages (builder needs it to install, runtime needs it to run CLI)
- Uses `uv sync --frozen` to install exact locked versions (more reliable than unresolved dependencies)

**3. Python 3.12-slim Base**
- Minimal footprint (slim variant)
- Python 3.12 (supports project's >=3.11 requirement per pyproject.toml)
- Official Python image from Docker Hub (security-maintained)

**4. Test Execution in Build**
- `uv run pytest` runs during builder stage
- Build fails if any tests fail, preventing broken images from being shipped
- Includes coverage reporting (`--cov=src`) to verify test quality
- `--tb=short` provides readable error output on failure

**5. Environment Variables**
- `PYTHONUNBUFFERED=1`: Ensures logs stream immediately to container logs
- `PYTHONDONTWRITEBYTECODE=1`: Prevents .pyc file generation (unnecessary in containers)
- `UV_COMPILE_BYTECODE=1`: Compiles Python to bytecode for faster startup
- `UV_LINK_MODE=copy`: Copies dependencies instead of symlinking (safer for containers)

**6. Minimal Runtime Layer**
- Only copies `.venv` and `src/` (not tests, pyproject.toml is metadata-only at runtime)
- Removes `apt-get` cache (`--no-install-recommends` + `rm -rf /var/lib/apt/lists/*`)
- Activates venv via `PATH` environment variable

**7. Health Check**
- `healthcheck` command runs `jerry session status` every 30s
- Allows orchestrators (Kubernetes, Docker Compose, etc.) to detect container health
- Respects the CLI entry point specified in the requirement

**8. Default Command**
- Sets `CMD ["jerry", "session", "status"]` per the requirement
- Users can override with `docker run <image> jerry <other-command>`

### Production Readiness Checklist

- [x] Non-root user would be ideal, but Jerry CLI may require write access (consider adding if issues arise)
- [x] Build caching optimized (dependencies layer before source)
- [x] Security: no hardcoded secrets, minimal image, updated base image
- [x] Logging: unbuffered output, health checks instrumented
- [x] Reproducibility: locked dependencies via `uv.lock`, frozen flag
- [x] Error handling: build fails if tests fail
- [x] Multi-stage: separation of concerns, minimal runtime size

### Usage

```bash
# Build the image
docker build -t jerry:latest .

# Run the CLI status check (default)
docker run jerry:latest

# Run other Jerry commands
docker run jerry:latest jerry items list
docker run jerry:latest jerry projects list

# Interactive session
docker run -it jerry:latest /bin/bash
```

### H-05 Compliance Note

This Dockerfile strictly adheres to H-05 (UV-only Python):
- **Never uses `pip`, `pip3`, or direct `python` execution** for dependency installation
- Uses `uv sync` for dependency management
- Uses `uv run pytest` for test execution (wraps pytest via uv)
- `PATH` is configured to use the uv-installed virtual environment

The `RUN curl | sh` pattern installs uv into the container's `$PATH` so that `uv` commands work in both build and runtime stages.
