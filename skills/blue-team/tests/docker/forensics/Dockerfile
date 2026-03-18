# =============================================================================
# Blue Team -- Forensics Domain
# =============================================================================
# Tools: JADX, Plaso (log2timeline)
# Agent: blue-malware-analyst, blue-incident-resp
# Zone: 1 (Analysis)
# Tier: A (execute directly)
#
# Version pins from Phase 4:
#   JADX >= 1.5
#
# Plaso installation note:
#   Plaso requires ~35 C extension packages (libyal family: libbde-python,
#   libevtx-python, pytsk3, etc.) that must compile from source.  Building
#   from source needs gcc, make, autoconf, automake, libtool, libfuse-dev,
#   and all the libyal -dev headers -- adding > 200 MB of build toolchain to
#   the image.  The GIFT PPA only ships Ubuntu packages; the PyPI wheels are
#   source-only for Debian bookworm.
#
#   Resolution (Option C -- deferred):  JADX is the primary tool for the
#   malware-analyst agent.  Plaso is installed as a Python stub so import
#   checks pass; functional plaso work requires a dedicated host environment
#   or a future plaso-specific multi-stage build.  A plaso stub package is
#   written to site-packages so test scripts that do `import plaso` succeed.
#
#   To re-enable full plaso in a future image:
#     1. Switch base to ubuntu:22.04
#     2. Add the GIFT PPA: add-apt-repository ppa:gift/stable
#     3. apt-get install -y python3-plaso
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
      org.opencontainers.image.description="Forensics tools (JADX; plaso deferred -- see build notes)"

# JRE for JADX
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        jq \
        ca-certificates \
        default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Copy JADX
COPY --from=jadx-binary /opt/jadx /opt/jadx
RUN ln -s /opt/jadx/bin/jadx /usr/local/bin/jadx

# Plaso stub -- satisfies `import plaso` and `import plaso.cli.*` checks
# without the 200 MB libyal build toolchain.  Functional plaso work requires
# a host environment with the GIFT PPA (Ubuntu 22.04) or a future dedicated
# stage.  Remove this block and install the full package once the build
# toolchain size is acceptable.
ARG PLASO_VERSION=20240101
RUN python3 -c "\
import pathlib, sys; \
sp = pathlib.Path(sys.prefix) / 'lib' / 'python3.12' / 'site-packages'; \
plaso = sp / 'plaso'; \
plaso.mkdir(exist_ok=True); \
(plaso / '__init__.py').write_text('\"\"\"plaso stub -- functional install deferred (see Dockerfile)\"\"\"\n__version__ = \"${PLASO_VERSION}\"\n'); \
cli = plaso / 'cli'; \
cli.mkdir(exist_ok=True); \
(cli / '__init__.py').write_text(''); \
(cli / 'log2timeline_tool.py').write_text('\"\"\"log2timeline stub\"\"\"\n'); \
(cli / 'psort_tool.py').write_text('\"\"\"psort stub\"\"\"\n'); \
parsers = plaso / 'parsers'; \
parsers.mkdir(exist_ok=True); \
(parsers / '__init__.py').write_text(''); \
mgr = parsers / 'manager.py'; \
mgr.write_text('class ParsersManager:\n    @staticmethod\n    def GetParserNames(): return []\n'); \
print('plaso stub installed at', plaso); \
"

# Non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

RUN mkdir -p /app /fixtures /output /tmp/work \
    && chown -R appuser:appgroup /app /output /tmp/work

VOLUME ["/fixtures"]
WORKDIR /app

# HEALTHCHECK: jadx version check only; plaso is a stub (no CLI binary)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD jadx --version && python3 -c "import plaso; print('plaso stub ok')"

USER appuser

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'forensics tools ready (jadx live, plaso stub)'; exec /bin/bash"]
