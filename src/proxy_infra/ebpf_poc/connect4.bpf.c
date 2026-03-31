// SPDX-License-Identifier: GPL-2.0
// connect4.bpf.c -- eBPF cgroup/connect4 transparent Envoy redirect
//
// Intercepts outbound IPv4 connect() from the container cgroup.
// Stores original destination in dst_lookup[cookie] for getsockopt to read.
// Rewrites destination to Envoy:15001 (transparent TCP listener).
//
// Skip rules (no redirect):
//   - SO_MARK == ENVOY_MARK (100) -- Envoy's own upstream connections (C2)
//   - Loopback (127.0.0.0/8) -- prevents redirect loops
//
// EN-023-009 / TASK-023-171 -- PROJ-023-exploit-framework

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>
#include "maps.h"

#define LOOPBACK_PREFIX 0x7f000000u
#define LOOPBACK_MASK   0xff000000u

/* SOL_SOCKET and SO_MARK for bpf_getsockopt (may not be in BPF UAPI) */
#ifndef SOL_SOCKET
#define SOL_SOCKET 1
#endif

#ifndef SO_MARK
#define SO_MARK 36
#endif

SEC("cgroup/connect4")
int connect4_redirect(struct bpf_sock_addr *ctx)
{
    /*
     * Check SO_MARK: skip redirect for Envoy upstream connections (C2).
     * IN-001 fix: check bpf_getsockopt return value. If the helper fails,
     * mark remains 0 which is safe (non-Envoy connections have mark 0).
     * A failure here means we cannot read the mark, so we conservatively
     * proceed with interception (fail-closed, not fail-open).
     */
    __u32 mark = 0;
    int ret = bpf_getsockopt(ctx, SOL_SOCKET, SO_MARK, &mark, sizeof(mark));
    if (ret == 0 && mark == ENVOY_MARK)
        return 1;

    __u32 dst_ip_nbo = ctx->user_ip4;
    __u32 dst_ip_hbo = bpf_ntohl(dst_ip_nbo);

    /* Skip loopback -- Docker DNS and local services on 127.x */
    if ((dst_ip_hbo & LOOPBACK_MASK) == LOOPBACK_PREFIX)
        return 1;

    /* Store original destination indexed by socket cookie */
    struct orig_dst orig = {
        .dst_ip   = dst_ip_nbo,
        .dst_port = ctx->user_port,
    };

    __u64 cookie = bpf_get_socket_cookie(ctx);
    bpf_map_update_elem(&dst_lookup, &cookie, &orig, BPF_ANY);

    /*
     * Redirect to Envoy transparent TCP listener (C1, C8).
     * SM-008: 127.0.0.1 assumes Envoy is co-located in the same network
     * namespace as the tool container (Docker Compose default bridge).
     * If Envoy moves to a separate namespace, use its routable IP instead.
     */
    ctx->user_ip4  = bpf_htonl(0x7f000001u);
    ctx->user_port = bpf_htons(ENVOY_PORT);

    return 1;
}

char LICENSE[] SEC("license") = "GPL";
