# Dockerfile: promptfoo Containerized Runtime
# PROJ-036 Prompt Regression Harness — Layer 1 (CI/CD Gate)
#
# Purpose: Isolate promptfoo (Node.js) from Jerry's UV-only Python environment.
#   Provides a reproducible, hardened container for promptfoo evaluation runs.
#   Fulfills ADR-001 Section 2.3 architectural decision: "promptfoo runs in Docker — not directly installed."
#
# Security controls per system-design.md Section 3 (threat model, threats T-01–T-04):
#   MC-01: No secrets baked into image — API key injected at runtime via environment variable
#   MC-07: Immutable filesystem layers; non-root user; dropped capabilities at runtime
#   MC-08: Base image pinned to SHA digest (not :latest tag) for supply chain integrity
#   MC-10: All source mounts are read-only (:ro) — enforced at docker run invocation
#   MC-13: Memory and CPU limits enforced at docker run invocation (not in Dockerfile)
#   MC-14: --cap-drop=ALL and --security-opt=no-new-privileges:true at runtime
#
# Build: docker build -t jerry-promptfoo:latest docker/promptfoo/
# Run (Smoke): docker run --rm --network=none -v $(pwd)/tests:/workspace/tests:ro jerry-promptfoo:latest eval --config /workspace/tests/prompt-regression/promptfoo-config.yaml
# Run (Standard/Full): docker run --rm -e ANTHROPIC_API_KEY=... -v $(pwd)/tests:/workspace/tests:ro jerry-promptfoo:latest eval ...
#
# H-05 compliance note: This Dockerfile installs Node.js (not Python).
#   Python assertion scripts are invoked from WITHIN the container via UV
#   by mounting the Jerry project root read-only and using uv run python.
#   The container includes uv for this purpose. pip is used ONLY to bootstrap uv;
#   all subsequent Python execution uses uv run (H-05 compliant).
#
# FR-025: promptfoo Docker isolation (no npm/Node.js in pyproject.toml)
# Revision: Stream 3A initial implementation

# ==============================================================================
# Stage 1: Node.js base with promptfoo installation
# Base image pinned to digest for supply chain integrity (MC-08)
# Using node:20-alpine for minimal attack surface
# ==============================================================================
# MC-08: Base image pinned to SHA-256 digest for supply chain integrity.
# To verify: docker pull node:20-alpine3.21 && docker inspect --format='{{index .RepoDigests 0}}' node:20-alpine3.21
# To update: resolve new tag digest and replace the sha256 value below.
FROM node:20-alpine3.21@sha256:eb0b81f6eb35ec5ecd1cab181801f93a6314127580b416e6e290363b724e1686 AS base

# Metadata labels for image identification and security scanning
LABEL maintainer="jerry-framework"
LABEL org.opencontainers.image.title="jerry-promptfoo"
LABEL org.opencontainers.image.description="promptfoo containerized runtime for PROJ-036 prompt regression harness"
LABEL org.opencontainers.image.source="https://github.com/geekatron/jerry"
LABEL proj036.layer="layer1-cicd-gate"
LABEL proj036.security.mc07="non-root-user,dropped-capabilities"
LABEL proj036.security.mc08="sha256-digest-pinned"

# Security: Create non-root user for promptfoo execution (MC-07)
# UID/GID 1001 reserved for promptfoo runner
RUN addgroup -g 1001 -S promptfoo && \
    adduser -u 1001 -S promptfoo -G promptfoo

# ==============================================================================
# Stage 2: Install promptfoo globally
# Version pinned for reproducibility (part of MC-08 supply chain control)
# ==============================================================================
# Install promptfoo at pinned version
# IMPORTANT: Update version here + re-baseline whenever promptfoo is upgraded
ENV PROMPTFOO_VERSION="0.86.0"

RUN npm install -g "promptfoo@${PROMPTFOO_VERSION}" --no-audit --no-fund && \
    # Verify installation
    promptfoo --version && \
    # Clean npm cache to reduce image size
    npm cache clean --force && \
    # Remove npm's temp files
    rm -rf /root/.npm /tmp/npm-* /tmp/.npm

# ==============================================================================
# Stage 3: Install UV for Python assertion script execution (H-05 compliance)
# Python assertion scripts (Layer 2 integration) must use `uv run python`
# ==============================================================================
ENV UV_VERSION="0.5.29"

RUN apk add --no-cache \
        # python3 + pip: transitive dependency of base image node:20-alpine3.21.
        # Version determined by Alpine 3.21 package repository (currently python3~3.12).
        # Pinning accepted as transitive: the Alpine package version is locked by the
        # base image tag (alpine3.21), and python3 is used only to bootstrap uv.
        python3 \
        py3-pip \
        # git for file:// prompt references and git hash resolution
        git \
        # jq for JSON processing in scripts
        jq \
        # ca-certificates for HTTPS (LLM API calls in Standard/Full modes)
        ca-certificates && \
    # Install UV at pinned version via pip (H-05: UV-only Python execution)
    # Using pip here solely to install uv itself; all subsequent Python work uses uv run.
    pip install --no-cache-dir "uv==${UV_VERSION}" && \
    # Verify UV installation
    uv --version

# ==============================================================================
# Security hardening: Runtime environment
# ==============================================================================
# Disable promptfoo telemetry (privacy + security: no data exfiltration)
ENV PROMPTFOO_DISABLE_TELEMETRY=1

# Disable promptfoo update checks (reduces external network calls, supply chain risk)
ENV PROMPTFOO_DISABLE_UPDATE_CHECK=1

# Cache disabled by default; override with -e PROMPTFOO_CACHE_ENABLED=true for local dev
ENV PROMPTFOO_CACHE_ENABLED=false

# Set home directory for non-root user
ENV HOME=/home/promptfoo

# Evaluation mode defaults to smoke (safe default — no LLM calls)
ENV EVALUATION_MODE=smoke

# Agent ID placeholder — must be set at runtime
ENV AGENT_ID=""

# ==============================================================================
# Workspace configuration
#
# Workspace is mounted read-only at runtime — not baked into image.
# This ensures: (1) no secrets in image, (2) no workspace tampering from container.
# Mounts expected at runtime:
#   -v $(pwd)/tests/prompt-regression:/workspace/tests:ro
#   -v $(pwd)/skills:/workspace/skills:ro
#   -v $(pwd)/baselines:/workspace/baselines:ro
#   -v $(pwd)/tests/prompt-regression/results:/workspace/output:rw
# ==============================================================================
WORKDIR /workspace

# Create output directory owned by non-root user
# (output volume is mounted rw; other mounts are ro)
RUN mkdir -p /workspace/output && \
    chown -R promptfoo:promptfoo /workspace

# ==============================================================================
# Switch to non-root user for all subsequent operations (MC-07)
# ==============================================================================
USER promptfoo

# ==============================================================================
# Health check: verify promptfoo is available and responsive
# ==============================================================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD promptfoo --version || exit 1

# ==============================================================================
# Entrypoint: promptfoo CLI
#
# The container exposes the promptfoo CLI directly.
# Callers pass sub-commands: eval, view, list, etc.
#
# Example invocations:
#   eval --config /workspace/tests/promptfoo-config.yaml
#   eval --config /workspace/tests/test-cases/ps-researcher.yaml --no-progress-bar
# ==============================================================================
ENTRYPOINT ["promptfoo"]

# Default command: show help (safe no-op for misconfigured runs)
CMD ["--help"]
