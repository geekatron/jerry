# Rainbow Supply Chain Verifier Container
# Tools: Cosign >= 2.2, Snyk CLI (latest stable)
# Purpose: Isolated environment for supply chain verification tools
# Security: Non-root user, health checks, minimal attack surface

FROM node:20-slim AS base

LABEL maintainer="jerry-framework"
LABEL description="Rainbow Supply Chain Verifier - Signature verification, license compliance"
LABEL version="1.0.0"

# Create non-root user
RUN groupadd -r verifier && useradd -r -g verifier -m -s /bin/bash verifier

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        git \
    && rm -rf /var/lib/apt/lists/*

ARG TARGETARCH=amd64

# Install Cosign >= 2.2 (pinned version -- no latest URL)
ARG COSIGN_VERSION=2.2.4
RUN ARCH="$([ "${TARGETARCH}" = "arm64" ] && echo "arm64" || echo "amd64")" && \
    curl -sSfL -o /usr/local/bin/cosign \
    "https://github.com/sigstore/cosign/releases/download/v${COSIGN_VERSION}/cosign-linux-${ARCH}" \
    && chmod +x /usr/local/bin/cosign

# Install Snyk CLI (pinned version)
ARG SNYK_VERSION=1.1292.0
RUN npm install -g snyk@${SNYK_VERSION}

# Create working directories
RUN mkdir -p /workspace/output /workspace/evidence && \
    chown -R verifier:verifier /workspace

# Switch to non-root user
USER verifier
WORKDIR /workspace

# Health check: verify all tools are accessible
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD cosign version && snyk version

# Default command: show tool versions
CMD ["bash", "-c", "echo '=== Rainbow SC Verifier ===' && cosign version && snyk version"]
