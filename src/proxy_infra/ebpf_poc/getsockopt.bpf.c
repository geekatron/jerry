// SPDX-License-Identifier: GPL-2.0
// getsockopt.bpf.c -- SO_ORIGINAL_DST Interception (cgroup/getsockopt)
//
// Intercepts getsockopt(SOL_IP, SO_ORIGINAL_DST) calls from Envoy.
// Chain lookup: source_port -> port_cookie -> cookie -> dst_lookup -> orig dst.
// Returns the real original destination that connect4.bpf.c saved before redirect.
//
// Constraint C6: ONLY intercepts SO_ORIGINAL_DST; returns 1 (passthrough)
//                for all other getsockopt calls.
//
// Attach: cgroup/getsockopt on Envoy container cgroup
// Maps:   dst_lookup (read), port_cookie (read)
//
// TASK-023-170 -- EN-023-009 -- PROJ-023-exploit-framework

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>
#include "maps.h"

/* SO_ORIGINAL_DST from linux/netfilter_ipv4.h (not always available in BPF) */
#define SO_ORIGINAL_DST 80

#ifndef SOL_IP
#define SOL_IP 0
#endif

#ifndef AF_INET
#define AF_INET 2
#endif

/* Minimal sockaddr_in for BPF optval writes (avoids libc header deps) */
struct sockaddr_in_bpf {
    __u16 sin_family;
    __u16 sin_port;      /* Network byte order */
    __u32 sin_addr;      /* Network byte order */
    __u8  sin_zero[8];
};

SEC("cgroup/getsockopt")
int getsockopt_orig_dst(struct bpf_sockopt *ctx)
{
    /*
     * C6: ONLY intercept SO_ORIGINAL_DST; passthrough everything else.
     * IN-006 note: SOL_IP == IPPROTO_IP == 0. Level 0 is unambiguous here
     * because SO_ORIGINAL_DST (80) is unique to SOL_IP/netfilter context.
     * No other protocol uses optname 80 at level 0.
     */
    if (ctx->level != SOL_IP || ctx->optname != SO_ORIGINAL_DST)
        return 1;

    /* Need socket context to read the peer (source) port */
    if (!ctx->sk)
        return 1;

    /*
     * ctx->sk->dst_port: remote port in network byte order (lower 16 bits).
     * This is the tool container's ephemeral source port as seen from Envoy.
     * Convert to host byte order to match sockops's local_port key format.
     */
    __u32 peer_port = bpf_ntohs((__u16)ctx->sk->dst_port);

    /* Chain lookup: peer_port -> cookie -> original destination */
    /*
     * Chain lookup: peer_port -> cookie -> original destination.
     *
     * Diagnostic (PM-011): if either lookup returns NULL, this program
     * returns 1 (passthrough) and Envoy receives kernel -ENOPROTOOPT.
     * Possible causes: (a) sockops hasn't fired yet for this connection
     * (PM-002 race window — TCP handshake not yet ESTABLISHED), (b) LRU
     * eviction under high connection concurrency, (c) connection not
     * intercepted by connect4 (loopback or SO_MARK=100 bypass).
     * Operator diagnostic: run `bpftool map dump pinned /sys/fs/bpf/maps/port_cookie`
     * and check for the peer port entry.
     */
    __u64 *cookie = bpf_map_lookup_elem(&port_cookie, &peer_port);
    if (!cookie)
        return 1;  /* No port_cookie entry; see PM-011 diagnostic above */

    struct orig_dst *orig = bpf_map_lookup_elem(&dst_lookup, cookie);
    if (!orig)
        return 1;  /* No dst_lookup entry; cookie may have been LRU-evicted */

    /* Bounds check: optval must have room for sockaddr_in */
    struct sockaddr_in_bpf *sa = ctx->optval;
    if ((void *)(sa + 1) > ctx->optval_end)
        return 1;  /* Buffer too small; let kernel handle */

    /* Write the real original destination into the optval buffer */
    sa->sin_family = AF_INET;
    /*
     * SM-009: (__u16) cast is safe because connect4 stores ctx->user_port
     * which is __be16 zero-extended to __u32. The upper 16 bits are always
     * zero. sin_port expects __be16, so the cast preserves byte order.
     */
    sa->sin_port   = (__u16)orig->dst_port;
    sa->sin_addr   = orig->dst_ip;           /* Already network byte order */
    __builtin_memset(sa->sin_zero, 0, sizeof(sa->sin_zero));

    /*
     * Write optlen and retval with asm barrier between them.
     * Without the barrier, clang -O2 merges these two adjacent 32-bit
     * writes (offsets 32 and 36 in bpf_sockopt) into a single 64-bit
     * store, which the BPF verifier rejects as "invalid bpf_context
     * access off=32 size=8" (context fields require exact-width access).
     */
    ctx->retval = 0;  /* Override kernel -ENOPROTOOPT; signal success */
    asm volatile("" ::: "memory");
    ctx->optlen = (__s32)sizeof(struct sockaddr_in_bpf);

    return 1;  /* Allow the getsockopt to complete with our values */
}

char LICENSE[] SEC("license") = "GPL";
