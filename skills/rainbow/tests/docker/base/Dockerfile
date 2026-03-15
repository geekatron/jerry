# =============================================================================
# Rainbow Series -- Base Image
# =============================================================================
# Multi-stage base image for all /rainbow and /blue-team containerized testing.
# All domain-specific Dockerfiles extend this base via FROM rainbow-base:latest.
#
# Contents:
#   - Python 3.12-slim with common utilities
#   - Credential filter dependencies (regex + entropy detection)
#   - Non-root execution (appuser:appgroup, UID 1000)
#   - Read-only /fixtures mount point
#
# SLSA: Build process documented (Level 1)
# CIS Docker Benchmark: 4.1 (non-root), 4.6 (HEALTHCHECK), 4.9 (minimal packages)
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Build dependencies
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-base.txt /tmp/requirements-base.txt
RUN pip install --no-cache-dir --prefix=/install -r /tmp/requirements-base.txt

# ---------------------------------------------------------------------------
# Stage 2: Runtime image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="jerry-framework" \
      org.opencontainers.image.title="rainbow-base" \
      org.opencontainers.image.description="Base image for Rainbow Series containerized testing" \
      org.opencontainers.image.source="https://github.com/geekatron/jerry"

# CIS 4.9: Install only required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        git \
        unzip \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /install /usr/local

# CIS 4.1: Create non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Create standard directories
RUN mkdir -p /app /fixtures /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

# Read-only fixtures mount point
VOLUME ["/fixtures"]

WORKDIR /app

# CIS 4.6: Add health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# CIS 4.1: Run as non-root
USER appuser

# Default entrypoint -- overridden by domain images
ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'rainbow-base ready'; exec /bin/bash"]
