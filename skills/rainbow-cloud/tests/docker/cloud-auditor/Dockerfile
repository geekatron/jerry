FROM python:3.11-slim
RUN pip install --no-cache-dir checkov>=3.0 && \
    curl -LO https://github.com/prowler-cloud/prowler/releases/latest/download/prowler-linux-amd64 && \
    chmod +x prowler-linux-amd64 && mv prowler-linux-amd64 /usr/local/bin/prowler
RUN curl -LO https://github.com/kubescape/kubescape/releases/latest/download/kubescape-ubuntu-latest && \
    chmod +x kubescape-ubuntu-latest && mv kubescape-ubuntu-latest /usr/local/bin/kubescape
WORKDIR /work
ENTRYPOINT ["/bin/sh"]
