# =============================================================================
# Rainbow Series -- Reconnaissance Domain
# =============================================================================
# Tools: Subfinder, httpx, dnsx, Naabu, Katana, Nuclei, OWASP Amass, Maigret
# Agent: rainbow-recon-pipeline, rainbow-recon-osint
# Zone: 2 (Engagement-scoped)
# Tier: A (execute directly)
#
# Version pins: ProjectDiscovery tools from GitHub releases
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Go binary downloads (ProjectDiscovery suite)
# ---------------------------------------------------------------------------
FROM debian:bookworm-slim AS pd-binaries

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        unzip \
    && rm -rf /var/lib/apt/lists/*

ARG TARGETARCH=amd64

# ProjectDiscovery tools -- version-pinned
ARG SUBFINDER_VERSION=2.6.6
ARG HTTPX_VERSION=1.6.8
ARG DNSX_VERSION=1.2.1
ARG NAABU_VERSION=2.3.1
ARG KATANA_VERSION=1.1.0
ARG NUCLEI_VERSION=3.3.0

RUN for tool_pkg in \
        "subfinder:${SUBFINDER_VERSION}:projectdiscovery/subfinder" \
        "httpx:${HTTPX_VERSION}:projectdiscovery/httpx" \
        "dnsx:${DNSX_VERSION}:projectdiscovery/dnsx" \
        "naabu:${NAABU_VERSION}:projectdiscovery/naabu" \
        "katana:${KATANA_VERSION}:projectdiscovery/katana" \
        "nuclei:${NUCLEI_VERSION}:projectdiscovery/nuclei"; do \
        TOOL=$(echo "$tool_pkg" | cut -d: -f1); \
        VER=$(echo "$tool_pkg" | cut -d: -f2); \
        REPO=$(echo "$tool_pkg" | cut -d: -f3); \
        curl -sSfL -o "/tmp/${TOOL}.zip" \
            "https://github.com/${REPO}/releases/download/v${VER}/${TOOL}_${VER}_linux_${TARGETARCH}.zip" \
        && unzip -o "/tmp/${TOOL}.zip" -d /tmp/${TOOL}_extract \
        && mv /tmp/${TOOL}_extract/${TOOL} /usr/local/bin/${TOOL} \
        && chmod +x /usr/local/bin/${TOOL} \
        && rm -rf /tmp/${TOOL}.zip /tmp/${TOOL}_extract; \
    done

# OWASP Amass
ARG AMASS_VERSION=4.2.0
RUN curl -sSfL -o /tmp/amass.zip \
    "https://github.com/owasp-amass/amass/releases/download/v${AMASS_VERSION}/amass_Linux_${TARGETARCH}.zip" \
    && unzip -o /tmp/amass.zip -d /tmp/amass_extract \
    && mv /tmp/amass_extract/amass_Linux_${TARGETARCH}/amass /usr/local/bin/amass \
    && chmod +x /usr/local/bin/amass \
    && rm -rf /tmp/amass.zip /tmp/amass_extract

# ---------------------------------------------------------------------------
# Stage 2: Runtime image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="jerry-framework" \
      org.opencontainers.image.title="rainbow-recon" \
      org.opencontainers.image.description="Reconnaissance and OSINT tools"

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        git \
        ca-certificates \
        libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Go binaries
COPY --from=pd-binaries /usr/local/bin/subfinder /usr/local/bin/subfinder
COPY --from=pd-binaries /usr/local/bin/httpx /usr/local/bin/httpx
COPY --from=pd-binaries /usr/local/bin/dnsx /usr/local/bin/dnsx
COPY --from=pd-binaries /usr/local/bin/naabu /usr/local/bin/naabu
COPY --from=pd-binaries /usr/local/bin/katana /usr/local/bin/katana
COPY --from=pd-binaries /usr/local/bin/nuclei /usr/local/bin/nuclei
COPY --from=pd-binaries /usr/local/bin/amass /usr/local/bin/amass

# Maigret (pip install) -- OSINT username enumeration
ARG MAIGRET_VERSION=0.4.4
RUN pip install --no-cache-dir maigret==${MAIGRET_VERSION}

# Non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

RUN mkdir -p /app /fixtures /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

# Update Nuclei templates (as appuser)
USER appuser
RUN nuclei -update-templates 2>/dev/null || true

VOLUME ["/fixtures"]
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD subfinder -version && nuclei -version

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'recon tools ready'; exec /bin/bash"]
