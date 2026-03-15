# =============================================================================
# Rainbow Series -- Cloud Security Domain
# =============================================================================
# Tools: Checkov, Prowler, Kubescape, Kyverno CLI, Cartography
# Agent: rainbow-cloud-auditor, rainbow-cloud-mapper
# Zone: 1/2 (Analysis / Engagement-scoped)
# Tier: A (Checkov, Prowler, Kubescape) / B (Kyverno)
#
# Prowler >= 4.0 (async, 15-60 min scans in production)
# Cartography requires Neo4j (provided via docker-compose neo4j service)
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Binary downloads
# ---------------------------------------------------------------------------
FROM debian:bookworm-slim AS binaries

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ARG TARGETARCH=amd64

# Kubescape >= 3.0
ARG KUBESCAPE_VERSION=3.0.8
RUN curl -sSfL -o /usr/local/bin/kubescape \
    "https://github.com/kubescape/kubescape/releases/download/v${KUBESCAPE_VERSION}/kubescape-ubuntu-latest" \
    && chmod +x /usr/local/bin/kubescape

# Kyverno CLI >= 1.11 (validate-only mode)
ARG KYVERNO_VERSION=1.12.3
RUN curl -sSfL -o /tmp/kyverno.tar.gz \
    "https://github.com/kyverno/kyverno/releases/download/v${KYVERNO_VERSION}/kyverno-cli_v${KYVERNO_VERSION}_linux_${TARGETARCH}.tar.gz" \
    && tar xzf /tmp/kyverno.tar.gz -C /usr/local/bin kyverno \
    && chmod +x /usr/local/bin/kyverno \
    && rm /tmp/kyverno.tar.gz

# ---------------------------------------------------------------------------
# Stage 2: Runtime image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="jerry-framework" \
      org.opencontainers.image.title="rainbow-cloud" \
      org.opencontainers.image.description="Cloud security posture and compliance tools"

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy binaries
COPY --from=binaries /usr/local/bin/kubescape /usr/local/bin/kubescape
COPY --from=binaries /usr/local/bin/kyverno /usr/local/bin/kyverno

# Python tools -- version-pinned
ARG CHECKOV_VERSION=3.2.0
ARG PROWLER_VERSION=4.3.0
ARG CARTOGRAPHY_VERSION=0.94.0

RUN pip install --no-cache-dir \
        checkov==${CHECKOV_VERSION} \
        prowler==${PROWLER_VERSION} \
        cartography==${CARTOGRAPHY_VERSION}

# Non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

RUN mkdir -p /app /fixtures /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

VOLUME ["/fixtures"]
WORKDIR /app

# Neo4j connection for Cartography (provided by docker-compose)
ENV NEO4J_URI="bolt://neo4j:7687"
ENV NEO4J_USER="neo4j"
ENV NEO4J_PASSWORD="test-only-not-real"

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD checkov --version && kubescape version

USER appuser

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'cloud tools ready'; exec /bin/bash"]
