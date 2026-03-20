# Rainbow Supply Chain Scanner Container
# Tools: Syft >= 1.0, Grype >= 0.74, Trivy >= 0.50, OSV-Scanner >= 2.0, Checkov >= 3.0
# Purpose: Isolated environment for supply chain scanning tools
# Security: Non-root user, health checks, minimal attack surface

FROM python:3.12-slim AS base

LABEL maintainer="jerry-framework"
LABEL description="Rainbow Supply Chain Scanner - SBOM generation, vulnerability scanning, IaC auditing"
LABEL version="1.0.0"

# Create non-root user
RUN groupadd -r scanner && useradd -r -g scanner -m -s /bin/bash scanner

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        git \
        unzip \
    && rm -rf /var/lib/apt/lists/*

ARG TARGETARCH=amd64

# Install Syft >= 1.0 (direct binary -- no piped shell execution)
ARG SYFT_VERSION=1.9.0
RUN ARCH="$([ "${TARGETARCH}" = "arm64" ] && echo "arm64" || echo "amd64")" && \
    curl -sSfL -o /tmp/syft.tar.gz \
    "https://github.com/anchore/syft/releases/download/v${SYFT_VERSION}/syft_${SYFT_VERSION}_linux_${ARCH}.tar.gz" \
    && tar xzf /tmp/syft.tar.gz -C /usr/local/bin syft \
    && chmod +x /usr/local/bin/syft \
    && rm /tmp/syft.tar.gz

# Install Grype >= 0.74 (direct binary -- no piped shell execution)
ARG GRYPE_VERSION=0.79.0
RUN ARCH="$([ "${TARGETARCH}" = "arm64" ] && echo "arm64" || echo "amd64")" && \
    curl -sSfL -o /tmp/grype.tar.gz \
    "https://github.com/anchore/grype/releases/download/v${GRYPE_VERSION}/grype_${GRYPE_VERSION}_linux_${ARCH}.tar.gz" \
    && tar xzf /tmp/grype.tar.gz -C /usr/local/bin grype \
    && chmod +x /usr/local/bin/grype \
    && rm /tmp/grype.tar.gz

# Install Trivy (direct binary; ARM64 only has .deb, amd64 has .tar.gz)
ARG TRIVY_VERSION=0.69.3
RUN if [ "${TARGETARCH}" = "arm64" ]; then \
      curl -sSfL -o /tmp/trivy.deb \
      "https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_Linux-ARM64.deb" \
      && dpkg -i /tmp/trivy.deb \
      && rm /tmp/trivy.deb; \
    else \
      curl -sSfL -o /tmp/trivy.tar.gz \
      "https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_Linux-64bit.tar.gz" \
      && tar xzf /tmp/trivy.tar.gz -C /usr/local/bin trivy \
      && chmod +x /usr/local/bin/trivy \
      && rm /tmp/trivy.tar.gz; \
    fi

# Install OSV-Scanner >= 2.0 (pinned version)
ARG OSV_SCANNER_VERSION=2.0.2
RUN ARCH="$([ "${TARGETARCH}" = "arm64" ] && echo "arm64" || echo "amd64")" && \
    curl -sSfL -o /usr/local/bin/osv-scanner \
    "https://github.com/google/osv-scanner/releases/download/v${OSV_SCANNER_VERSION}/osv-scanner_linux_${ARCH}" \
    && chmod +x /usr/local/bin/osv-scanner

# Install Checkov (>= 3.0)
RUN pip install --no-cache-dir checkov>=3.0

# Create working directories
RUN mkdir -p /workspace/output /workspace/evidence /home/scanner/.cache/grype /home/scanner/.cache/trivy && \
    chown -R scanner:scanner /workspace /home/scanner/.cache

# Allow pre-cached DBs to be used for up to 30 days between image rebuilds.
# Default is 5 days which causes failures in offline/air-gapped containers.
# To get fresh data: rebuild the image (grype db update runs during build).
ENV GRYPE_DB_MAX_ALLOWED_BUILT_AGE=720h
ENV GRYPE_DB_AUTO_UPDATE=false

# Switch to non-root user BEFORE downloading DBs so caches land in the right place
USER scanner

# Pre-download Grype vulnerability DB during build (network available).
# At runtime scanner-net routes through envoy-z1-update; first-run DB download
# takes 5-10 minutes and may timeout. Pre-cache eliminates cold-start delay.
RUN grype db update || true

# Pre-download Trivy vulnerability DB during build.
RUN trivy image --download-db-only --cache-dir /home/scanner/.cache/trivy || true
WORKDIR /workspace

# Health check: verify all tools are accessible
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD syft version && grype version && trivy --version && osv-scanner --version && checkov --version

# Default command: show tool versions
CMD ["bash", "-c", "echo '=== Rainbow SC Scanner ===' && syft version && grype version && trivy --version && osv-scanner --version && checkov --version"]
