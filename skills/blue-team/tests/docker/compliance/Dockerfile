# =============================================================================
# Blue Team -- Compliance Domain
# =============================================================================
# Tools: Checkov, Trivy, Prowler, Kubescape, kube-bench, OpenSCAP, Cosign
# Agent: blue-comply, blue-posture-k8s, blue-posture-sys
# Zone: 1 (Analysis)
# Tier: A (Checkov, Trivy, Prowler, Kubescape, kube-bench, Cosign)
#       B (OpenSCAP -- guide-then-execute, SCAP profile selection)
#
# Version pins from Phase 4:
#   Checkov >= 3.0, Trivy >= 0.50, Prowler >= 4.0, Kubescape >= 3.0,
#   kube-bench >= 0.8, OpenSCAP >= 1.3, Cosign >= 2.2
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Binary downloads
# ---------------------------------------------------------------------------
FROM debian:bookworm-slim AS binaries

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        tar \
    && rm -rf /var/lib/apt/lists/*

ARG TARGETARCH

# Trivy >= 0.50 (direct tarball download; naming: Linux-ARM64 vs Linux-64bit)
ARG TRIVY_VERSION=0.69.3
RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo "ARM64" || echo "64bit") && \
    curl -sSfL -o /tmp/trivy.tar.gz \
    "https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_Linux-${ARCH}.tar.gz" \
    && tar xzf /tmp/trivy.tar.gz -C /usr/local/bin trivy \
    && chmod +x /usr/local/bin/trivy \
    && rm /tmp/trivy.tar.gz

# Kubescape >= 3.0 (v4.x uses kubescape_{VERSION}_linux_{ARCH} naming)
ARG KUBESCAPE_VERSION=4.0.3
RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo "arm64" || echo "amd64") && \
    curl -sSfL -o /usr/local/bin/kubescape \
    "https://github.com/kubescape/kubescape/releases/download/v${KUBESCAPE_VERSION}/kubescape_${KUBESCAPE_VERSION}_linux_${ARCH}" \
    && chmod +x /usr/local/bin/kubescape

# kube-bench >= 0.8
ARG KUBE_BENCH_VERSION=0.8.0
RUN curl -sSfL -o /tmp/kube-bench.tar.gz \
    "https://github.com/aquasecurity/kube-bench/releases/download/v${KUBE_BENCH_VERSION}/kube-bench_${KUBE_BENCH_VERSION}_linux_${TARGETARCH}.tar.gz" \
    && tar xzf /tmp/kube-bench.tar.gz -C /usr/local/bin kube-bench \
    && chmod +x /usr/local/bin/kube-bench \
    && rm /tmp/kube-bench.tar.gz

# Cosign >= 2.2 (verify-only)
ARG COSIGN_VERSION=2.2.4
RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo "arm64" || echo "amd64") && \
    curl -sSfL -o /usr/local/bin/cosign \
    "https://github.com/sigstore/cosign/releases/download/v${COSIGN_VERSION}/cosign-linux-${ARCH}" \
    && chmod +x /usr/local/bin/cosign

# ---------------------------------------------------------------------------
# Stage 2: Runtime image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="jerry-framework" \
      org.opencontainers.image.title="blue-compliance" \
      org.opencontainers.image.description="Compliance scanning and posture assessment tools"

# OpenSCAP >= 1.3 (apt install) + system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        git \
        ca-certificates \
        libopenscap33 \
        openscap-common \
        openscap-utils \
        ssg-base \
        ssg-debderived \
    && rm -rf /var/lib/apt/lists/*

# Copy binaries
COPY --from=binaries /usr/local/bin/trivy /usr/local/bin/trivy
COPY --from=binaries /usr/local/bin/kubescape /usr/local/bin/kubescape
COPY --from=binaries /usr/local/bin/kube-bench /usr/local/bin/kube-bench
COPY --from=binaries /usr/local/bin/cosign /usr/local/bin/cosign

# Python compliance tools (checkov and prowler have conflicting transitive deps
# when pinned to old versions; install separately with minimum version bounds)
RUN pip install --no-cache-dir checkov>=3.0
RUN pip install --no-cache-dir prowler>=4.0

# Non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

RUN mkdir -p /app /fixtures /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

VOLUME ["/fixtures"]
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD checkov --version && trivy --version && kubescape version && cosign version

USER appuser

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'compliance tools ready'; exec /bin/bash"]
