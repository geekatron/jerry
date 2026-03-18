# =============================================================================
# Blue Team -- Detection Domain
# =============================================================================
# Tools: YARA-X (yr CLI), Hayabusa, Chainsaw
# Agent: blue-detect, blue-siem
# Zone: 1 (Analysis)
# Tier: A (execute directly)
#
# Version pins from Phase 4 blue-team-skill-design.md:
#   YARA-X >= 0.9.0 (using 1.14.0 — first version with aarch64-linux build)
#   Hayabusa >= 2.14 (using 3.8.1 — v3 naming: lin-{aarch64-gnu|x64-gnu})
#   Chainsaw >= 2.9 (using 2.14.1 — first version with aarch64-linux build)
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Binary downloads
# ---------------------------------------------------------------------------
FROM debian:bookworm-slim AS binaries

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        unzip \
    && rm -rf /var/lib/apt/lists/*

ARG TARGETARCH

# YARA-X yr CLI — the .gz asset contains a 512-byte header + ELF binary
ARG YARA_X_VERSION=1.14.0
RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo "aarch64" || echo "x86_64") && \
    curl -sSfL -o /tmp/yara-x.gz \
    "https://github.com/VirusTotal/yara-x/releases/download/v${YARA_X_VERSION}/yara-x-v${YARA_X_VERSION}-${ARCH}-unknown-linux-gnu.gz" \
    && gunzip -c /tmp/yara-x.gz | tail -c +513 > /usr/local/bin/yr \
    && chmod +x /usr/local/bin/yr \
    && rm /tmp/yara-x.gz

# Hayabusa >= 2.14 (v3.x naming: lin-{aarch64-gnu|x64-gnu})
# Binary inside zip: hayabusa-{VER}-lin-{ARCH} (no execute bit until chmod)
ARG HAYABUSA_VERSION=3.8.1
RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo "aarch64-gnu" || echo "x64-gnu") && \
    curl -sSfL -o /tmp/hayabusa.zip \
    "https://github.com/Yamato-Security/hayabusa/releases/download/v${HAYABUSA_VERSION}/hayabusa-${HAYABUSA_VERSION}-lin-${ARCH}.zip" \
    && unzip -j -o /tmp/hayabusa.zip "hayabusa-${HAYABUSA_VERSION}-lin-${ARCH}" -d /tmp/hayabusa_extract \
    && mv "/tmp/hayabusa_extract/hayabusa-${HAYABUSA_VERSION}-lin-${ARCH}" /usr/local/bin/hayabusa \
    && chmod +x /usr/local/bin/hayabusa \
    && rm -rf /tmp/hayabusa.zip /tmp/hayabusa_extract

# Chainsaw >= 2.9 (v2.14+ has aarch64-unknown-linux-gnu)
ARG CHAINSAW_VERSION=2.14.1
RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo "aarch64" || echo "x86_64") && \
    curl -sSfL -o /tmp/chainsaw.tar.gz \
    "https://github.com/WithSecureLabs/chainsaw/releases/download/v${CHAINSAW_VERSION}/chainsaw_${ARCH}-unknown-linux-gnu.tar.gz" \
    && tar xzf /tmp/chainsaw.tar.gz -C /tmp \
    && find /tmp -name 'chainsaw' -type f -executable -exec mv {} /usr/local/bin/chainsaw \; \
    && chmod +x /usr/local/bin/chainsaw \
    && rm -rf /tmp/chainsaw.tar.gz

# ---------------------------------------------------------------------------
# Stage 2: Runtime image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="jerry-framework" \
      org.opencontainers.image.title="blue-detection" \
      org.opencontainers.image.description="Threat detection tools (YARA-X, Hayabusa, Chainsaw)"

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy binaries
COPY --from=binaries /usr/local/bin/yr /usr/local/bin/yr
COPY --from=binaries /usr/local/bin/hayabusa /usr/local/bin/hayabusa
COPY --from=binaries /usr/local/bin/chainsaw /usr/local/bin/chainsaw

# YARA-X yr CLI + Python binding for blue-ioc rule authoring validation
# sigma-cli for Sigma rule conversion and validation (blue-siem)
RUN pip install --no-cache-dir yara-x>=1.0.0 sigma-cli>=0.10

# Non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

RUN mkdir -p /app /fixtures /fixtures/yara-rules /fixtures/evtx-samples /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

VOLUME ["/fixtures", "/fixtures/yara-rules", "/fixtures/evtx-samples"]
WORKDIR /app

# Version pre-check per Phase 4 design: Tier A tools SHOULD verify version
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD yr --version && hayabusa help >/dev/null 2>&1 && chainsaw --version && sigma version

USER appuser

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'detection tools ready'; exec /bin/bash"]
