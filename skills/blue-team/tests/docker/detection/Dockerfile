# =============================================================================
# Blue Team -- Detection Domain
# =============================================================================
# Tools: YARA-X (yr CLI), Hayabusa, Chainsaw
# Agent: blue-detect, blue-siem
# Zone: 1 (Analysis)
# Tier: A (execute directly)
#
# Version pins from Phase 4 blue-team-skill-design.md:
#   YARA-X >= 0.9.0, Hayabusa >= 2.14, Chainsaw >= 2.9
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

ARG TARGETARCH=amd64

# YARA-X >= 0.9.0 (yr CLI)
ARG YARA_X_VERSION=0.9.0
RUN curl -sSfL -o /tmp/yara-x.tar.gz \
    "https://github.com/VirusTotal/yara-x/releases/download/v${YARA_X_VERSION}/yr-v${YARA_X_VERSION}-x86_64-unknown-linux-gnu.tar.gz" \
    && tar xzf /tmp/yara-x.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/yr \
    && rm /tmp/yara-x.tar.gz

# Hayabusa >= 2.14
ARG HAYABUSA_VERSION=2.17.0
RUN curl -sSfL -o /tmp/hayabusa.zip \
    "https://github.com/Yamato-Security/hayabusa/releases/download/v${HAYABUSA_VERSION}/hayabusa-${HAYABUSA_VERSION}-linux-x64-gnu.zip" \
    && unzip -o /tmp/hayabusa.zip -d /tmp/hayabusa_extract \
    && find /tmp/hayabusa_extract -name 'hayabusa*' -type f -executable -exec mv {} /usr/local/bin/hayabusa \; \
    && chmod +x /usr/local/bin/hayabusa \
    && rm -rf /tmp/hayabusa.zip /tmp/hayabusa_extract

# Chainsaw >= 2.9
ARG CHAINSAW_VERSION=2.9.2
RUN curl -sSfL -o /tmp/chainsaw.tar.gz \
    "https://github.com/WithSecureLabs/chainsaw/releases/download/v${CHAINSAW_VERSION}/chainsaw_x86_64-unknown-linux-gnu.tar.gz" \
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

# YARA-X Python binding for blue-ioc rule authoring validation
# sigma-cli for Sigma rule conversion and validation (blue-siem)
RUN pip install --no-cache-dir yara-x>=0.9.0 sigma-cli>=0.10

# Non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

RUN mkdir -p /app /fixtures /fixtures/yara-rules /fixtures/evtx-samples /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

VOLUME ["/fixtures", "/fixtures/yara-rules", "/fixtures/evtx-samples"]
WORKDIR /app

# Version pre-check per Phase 4 design: Tier A tools SHOULD verify version
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD yr --version && hayabusa --version && chainsaw --version

USER appuser

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'detection tools ready'; exec /bin/bash"]
