# Dockerfile -- EN-023-001 eBPF cgroup/connect4 PoC (Full Chain)
# Ubuntu 24.04 | clang bpftool libbpf microsocks python3 bridge
FROM ubuntu:24.04 AS build

ARG MICROSOCKS_VERSION=1.0.5
ARG MICROSOCKS_SHA256=939d1851a18a4c03f3cc5c92ff7a50eaf045da7814764b4cb9e26921db15abc8

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    clang llvm libbpf-dev linux-libc-dev linux-tools-common linux-tools-generic \
    build-essential dpkg-dev curl ca-certificates pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Compile BPF program
WORKDIR /build/bpf
COPY connect4.bpf.c Makefile ./
RUN GNU_TRIPLE=$(dpkg-architecture -qDEB_HOST_GNU_TYPE) && \
    ln -sf /usr/include/${GNU_TRIPLE}/asm /usr/include/asm && \
    make

# Build microsocks (fallback local proxy for testing)
WORKDIR /build/microsocks
RUN curl -fsSL \
    "https://github.com/rofl0r/microsocks/archive/refs/tags/v${MICROSOCKS_VERSION}.tar.gz" \
    -o microsocks.tar.gz && \
    echo "${MICROSOCKS_SHA256}  microsocks.tar.gz" | sha256sum -c - && \
    tar xzf microsocks.tar.gz --strip-components=1 && \
    make

# Runtime stage
FROM ubuntu:24.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    linux-tools-common linux-tools-generic libbpf1 iproute2 curl python3 \
    netcat-openbsd socat \
    && rm -rf /var/lib/apt/lists/*

# Symlink actual bpftool binary (bypass version-checking wrapper)
COPY --from=build /usr/lib/linux-tools/*/bpftool /usr/local/bin/bpftool
RUN chmod +x /usr/local/bin/bpftool

COPY --from=build /build/bpf/connect4.bpf.o /opt/ebpf/connect4.bpf.o
COPY --from=build /build/microsocks/microsocks /usr/local/bin/microsocks
COPY bridge.py /opt/ebpf/bridge.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh /opt/ebpf/bridge.py

ENTRYPOINT ["/entrypoint.sh"]
