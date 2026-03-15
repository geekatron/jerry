# =============================================================================
# Blue Team -- Threat Intelligence Domain
# =============================================================================
# Tools: MISP modules (pymisp), python-stix2, taxii2-client
# Agent: blue-intel, blue-ioc, blue-d3fend
# Zone: 1 (Analysis)
# Tier: B (guide-then-execute)
#
# Version pins from Phase 4:
#   MISP >= 2.4 (PyMISP client), python-stix2 >= 3.0, taxii2-client >= 2.3
# =============================================================================

FROM python:3.12-slim AS runtime

LABEL maintainer="jerry-framework" \
      org.opencontainers.image.title="blue-intel" \
      org.opencontainers.image.description="Threat intelligence tools (MISP, STIX/TAXII)"

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Python threat intel tools -- version-pinned
ARG PYMISP_VERSION=2.4.190
ARG STIX2_VERSION=3.0.1
ARG TAXII2_CLIENT_VERSION=2.3.0

RUN pip install --no-cache-dir \
        pymisp==${PYMISP_VERSION} \
        stix2==${STIX2_VERSION} \
        taxii2-client==${TAXII2_CLIENT_VERSION}

# Non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

RUN mkdir -p /app /fixtures /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

VOLUME ["/fixtures"]
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import pymisp; import stix2; import taxii2client; print('intel tools ok')"

USER appuser

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'intel tools ready'; exec /bin/bash"]
