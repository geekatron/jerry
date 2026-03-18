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

# Install Syft (>= 1.0)
RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

# Install Grype (>= 0.74)
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Install Trivy (>= 0.50)
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Install OSV-Scanner (>= 2.0)
RUN curl -sSfL "https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_linux_${TARGETARCH}" -o /usr/local/bin/osv-scanner && \
    chmod +x /usr/local/bin/osv-scanner

# Install Checkov (>= 3.0)
RUN pip install --no-cache-dir checkov>=3.0

# Create working directories
RUN mkdir -p /workspace/output /workspace/evidence && \
    chown -R scanner:scanner /workspace

# Switch to non-root user
USER scanner
WORKDIR /workspace

# Health check: verify all tools are accessible
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD syft version && grype version && trivy --version && osv-scanner --version && checkov --version

# Default command: show tool versions
CMD ["bash", "-c", "echo '=== Rainbow SC Scanner ===' && syft version && grype version && trivy --version && osv-scanner --version && checkov --version"]
