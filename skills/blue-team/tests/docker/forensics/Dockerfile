# =============================================================================
# Blue Team -- Forensics Domain
# =============================================================================
# Tools: JADX, Plaso (log2timeline)
# Agent: blue-malware-analyst, blue-incident-resp
# Zone: 1 (Analysis)
# Tier: A (execute directly)
#
# Version pins from Phase 4:
#   JADX >= 1.5, Plaso >= 20240101
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: JADX binary (requires JRE)
# ---------------------------------------------------------------------------
FROM debian:bookworm-slim AS jadx-binary

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        unzip \
    && rm -rf /var/lib/apt/lists/*

ARG JADX_VERSION=1.5.0
RUN curl -sSfL -o /tmp/jadx.zip \
    "https://github.com/skylot/jadx/releases/download/v${JADX_VERSION}/jadx-${JADX_VERSION}.zip" \
    && mkdir -p /opt/jadx \
    && unzip -o /tmp/jadx.zip -d /opt/jadx \
    && chmod +x /opt/jadx/bin/jadx /opt/jadx/bin/jadx-gui \
    && rm /tmp/jadx.zip

# ---------------------------------------------------------------------------
# Stage 2: Runtime image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="jerry-framework" \
      org.opencontainers.image.title="blue-forensics" \
      org.opencontainers.image.description="Forensics tools (JADX, Plaso/log2timeline)"

# JRE for JADX + system deps for Plaso
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        ca-certificates \
        default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Copy JADX
COPY --from=jadx-binary /opt/jadx /opt/jadx
RUN ln -s /opt/jadx/bin/jadx /usr/local/bin/jadx

# Plaso / log2timeline >= 20240101 (pip install)
ARG PLASO_VERSION=20240101
RUN pip install --no-cache-dir plaso>=${PLASO_VERSION}

# Non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

RUN mkdir -p /app /fixtures /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

VOLUME ["/fixtures"]
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD jadx --version && python -c "import plaso; print('plaso ok')"

USER appuser

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'forensics tools ready'; exec /bin/bash"]
