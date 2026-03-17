FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir checkov>=3.0
RUN curl -sSfL -o /usr/local/bin/prowler \
    https://github.com/prowler-cloud/prowler/releases/latest/download/prowler-linux-amd64 && \
    chmod +x /usr/local/bin/prowler
RUN curl -sSfL -o /usr/local/bin/kubescape \
    https://github.com/kubescape/kubescape/releases/latest/download/kubescape-ubuntu-latest && \
    chmod +x /usr/local/bin/kubescape
RUN useradd --create-home appuser
USER appuser
WORKDIR /work
HEALTHCHECK --interval=30s --timeout=10s CMD checkov --version && prowler --version
ENTRYPOINT ["/bin/sh"]
