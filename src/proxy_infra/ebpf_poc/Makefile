# Makefile -- compile connect4.bpf.c to BPF object
#
# Requires: clang, linux-headers or linux-tools-generic (for bpf/bpf_helpers.h)
# Ubuntu 24.04: apt-get install -y clang linux-tools-generic libbpf-dev
#
# EN-023-001 PoC

BPF_TARGET  := connect4.bpf.o
BPF_SRC     := connect4.bpf.c

CLANG       ?= clang
ARCH        := $(shell uname -m | sed 's/x86_64/x86/' | sed 's/aarch64/arm64/')
GNU_TRIPLE  := $(shell dpkg-architecture -qDEB_HOST_GNU_TYPE 2>/dev/null || echo "aarch64-linux-gnu")
CFLAGS      := -O2 -target bpf -g \
               -D__TARGET_ARCH_$(ARCH) \
               -I/usr/include \
               -I/usr/include/$(GNU_TRIPLE) \
               $(shell pkg-config --cflags libbpf 2>/dev/null)

.PHONY: all clean

all: $(BPF_TARGET)

$(BPF_TARGET): $(BPF_SRC)
	$(CLANG) $(CFLAGS) -c $< -o $@
	@echo "[OK] $(BPF_TARGET) compiled"

clean:
	rm -f $(BPF_TARGET)
