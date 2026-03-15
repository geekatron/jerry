# =============================================================================
# Rainbow Series -- Supply Chain Domain
# =============================================================================
# Tools: Syft, Grype, Trivy, OSV-Scanner, Checkov, Cosign, Snyk CLI
# Agent: rainbow-sc-scanner, rainbow-sc-verifier
# Zone: 1 (Analysis) / 3 (Cosign verify-only)
# Tier: A (execute directly)
#
# Version pins from Phase 4 blue-team-skill-design.md Tool Inventory
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Binary downloads
# ---------------------------------------------------------------------------
FROM debian:bookworm-slim AS binaries

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Syft >= (latest stable, version-pinned)
ARG SYFT_VERSION=1.9.0
RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh \
    | sh -s -- -b /usr/local/bin v${SYFT_VERSION}

# Grype >= (latest stable, version-pinned)
ARG GRYPE_VERSION=0.79.0
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh \
    | sh -s -- -b /usr/local/bin v${GRYPE_VERSION}

# Trivy >= 0.50
ARG TRIVY_VERSION=0.54.1
RUN curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
    | sh -s -- -b /usr/local/bin v${TRIVY_VERSION}

# OSV-Scanner
ARG OSV_SCANNER_VERSION=1.8.3
RUN curl -sSfL -o /usr/local/bin/osv-scanner \
    "https://github.com/google/osv-scanner/releases/download/v${OSV_SCANNER_VERSION}/osv-scanner_linux_amd64" \
    && chmod +x /usr/local/bin/osv-scanner

# Cosign >= 2.2 (verify-only usage)
ARG COSIGN_VERSION=2.2.4
RUN curl -sSfL -o /usr/local/bin/cosign \
    "https://github.com/sigstore/cosign/releases/download/v${COSIGN_VERSION}/cosign-linux-amd64" \
    && chmod +x /usr/local/bin/cosign

# ---------------------------------------------------------------------------
# Stage 2: Node.js tools
# ---------------------------------------------------------------------------
FROM node:20-slim AS node-tools

# Snyk CLI
ARG SNYK_VERSION=1.1292.0
RUN npm install -g snyk@${SNYK_VERSION}

# ---------------------------------------------------------------------------
# Stage 3: Runtime image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="jerry-framework" \
      org.opencontainers.image.title="rainbow-supply-chain" \
      org.opencontainers.image.description="Supply chain security scanning tools"

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy binaries from Stage 1
COPY --from=binaries /usr/local/bin/syft /usr/local/bin/syft
COPY --from=binaries /usr/local/bin/grype /usr/local/bin/grype
COPY --from=binaries /usr/local/bin/trivy /usr/local/bin/trivy
COPY --from=binaries /usr/local/bin/osv-scanner /usr/local/bin/osv-scanner
COPY --from=binaries /usr/local/bin/cosign /usr/local/bin/cosign

# Copy Node.js runtime + Snyk from node-tools stage
COPY --from=node-tools /usr/local/bin/node /usr/local/bin/node
COPY --from=node-tools /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/snyk/bin/snyk /usr/local/bin/snyk

# Checkov >= 3.0 (pip install)
ARG CHECKOV_VERSION=3.2.0
RUN pip install --no-cache-dir checkov==${CHECKOV_VERSION}

# Non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

RUN mkdir -p /app /fixtures /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

VOLUME ["/fixtures"]
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD syft version && grype version && trivy --version && checkov --version

USER appuser

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'supply-chain tools ready'; exec /bin/bash"]
