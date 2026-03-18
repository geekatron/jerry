FROM python:3.11-slim
ARG TARGETARCH=amd64
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir checkov>=3.0 prowler>=4.0
RUN ARCH=$([ "$TARGETARCH" = "arm64" ] && echo "arm64" || echo "amd64") && \
    KSVER=$(curl -sSf https://api.github.com/repos/kubescape/kubescape/releases/latest | python3 -c "import json,sys; print(json.load(sys.stdin)['tag_name'].lstrip('v'))") && \
    curl -sSfL -o /usr/local/bin/kubescape \
    "https://github.com/kubescape/kubescape/releases/latest/download/kubescape_${KSVER}_linux_${ARCH}" && \
    chmod +x /usr/local/bin/kubescape
RUN useradd --create-home appuser
USER appuser
WORKDIR /work
HEALTHCHECK --interval=30s --timeout=10s CMD checkov --version && prowler --version
ENTRYPOINT ["/bin/sh"]
