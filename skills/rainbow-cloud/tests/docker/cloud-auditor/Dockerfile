FROM python:3.11-slim
ARG TARGETARCH=amd64
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir checkov>=3.0 prowler>=4.0
# Kubescape -- pinned version, no runtime API resolution
ARG KUBESCAPE_VERSION=4.0.3
RUN ARCH="$([ "${TARGETARCH}" = "arm64" ] && echo "arm64" || echo "amd64")" && \
    curl -sSfL -o /usr/local/bin/kubescape \
    "https://github.com/kubescape/kubescape/releases/download/v${KUBESCAPE_VERSION}/kubescape_${KUBESCAPE_VERSION}_linux_${ARCH}" && \
    chmod +x /usr/local/bin/kubescape
RUN useradd --create-home appuser
USER appuser
WORKDIR /work
HEALTHCHECK --interval=30s --timeout=10s CMD checkov --version && prowler --version
ENTRYPOINT ["/bin/sh"]
