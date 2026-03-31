# Makefile -- compile BPF programs for 3-program architecture
#
# Programs:
#   connect4.bpf.o   -- cgroup/connect4 (redirect to Envoy:15001)
#   sockops.bpf.o    -- cgroup/sock_ops (port-to-cookie mapping)
#   getsockopt.bpf.o -- cgroup/getsockopt (SO_ORIGINAL_DST interception)
#
# Shared header: maps.h (C7: map schemas defined once)
#
# EN-023-009 PROJ-023-exploit-framework

BPF_TARGETS := connect4.bpf.o sockops.bpf.o getsockopt.bpf.o
BPF_HEADER  := maps.h

CLANG       ?= clang
ARCH        := $(shell uname -m | sed 's/x86_64/x86/' | sed 's/aarch64/arm64/')
GNU_TRIPLE  := $(shell dpkg-architecture -qDEB_HOST_GNU_TYPE 2>/dev/null || echo "aarch64-linux-gnu")
CFLAGS      := -O2 -target bpf -g \
               -D__TARGET_ARCH_$(ARCH) \
               -I. \
               -I/usr/include \
               -I/usr/include/$(GNU_TRIPLE) \
               $(shell pkg-config --cflags libbpf 2>/dev/null)

.PHONY: all clean

all: $(BPF_TARGETS)

%.bpf.o: %.bpf.c $(BPF_HEADER)
	$(CLANG) $(CFLAGS) -c $< -o $@
	@echo "[OK] $@ compiled"

clean:
	rm -f $(BPF_TARGETS)
