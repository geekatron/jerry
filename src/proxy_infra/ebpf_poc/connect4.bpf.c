// SPDX-License-Identifier: GPL-2.0
// connect4.bpf.c -- eBPF cgroup/connect4 transparent SOCKS5 redirect
//
// Intercepts outbound IPv4 connect() from the container cgroup.
// Stores original destination in array map[0] for bridge to read.
// Rewrites destination to 127.0.0.1:BRIDGE_PORT (local bridge).
//
// Bypass rules (no redirect):
//   - Loopback (127.0.0.0/8) — prevents redirect loops with bridge
//   - Destinations in bypass_ips map — proxy-node IPs populated by entrypoint
//
// EN-023-001 PoC -- PROJ-023-exploit-framework

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

#define BRIDGE_PORT     12345
#define LOOPBACK_PREFIX 0x7f000000u
#define LOOPBACK_MASK   0xff000000u
/* Docker subnet skip removed — per-container cgroup attachment solved the isolation */

struct orig_dst {
    __u32 dst_ip;
    __u32 dst_port;
};

/* Array map[0]: latest intercepted destination (bridge reads this) */
struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __uint(max_entries, 1);
    __type(key,   __u32);
    __type(value, struct orig_dst);
} dst_latest SEC(".maps");

/* LRU hash keyed by socket cookie for bpftool inspection */
struct {
    __uint(type, BPF_MAP_TYPE_LRU_HASH);
    __uint(max_entries, 4096);
    __type(key,   __u64);
    __type(value, struct orig_dst);
} dst_lookup SEC(".maps");

/* Bypass set: IPs that should NOT be redirected (proxy-node IPs) */
struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 64);
    __type(key,   __u32);    /* IP in network byte order */
    __type(value, __u8);     /* 1 = bypass */
} bypass_ips SEC(".maps");

SEC("cgroup/connect4")
int connect4_redirect(struct bpf_sock_addr *ctx)
{
    __u32 dst_ip_nbo = ctx->user_ip4;
    __u32 dst_ip_hbo = bpf_ntohl(dst_ip_nbo);

    /* Skip loopback — bridge and Docker DNS are on 127.x */
    if ((dst_ip_hbo & LOOPBACK_MASK) == LOOPBACK_PREFIX)
        return 1;

    /* Skip bypass IPs (proxy nodes — bridge connects to these directly) */
    __u8 *bypass = bpf_map_lookup_elem(&bypass_ips, &dst_ip_nbo);
    if (bypass)
        return 1;

    struct orig_dst orig = {
        .dst_ip   = dst_ip_nbo,
        .dst_port = ctx->user_port,
    };

    /* Write to array[0] for bridge */
    __u32 zero = 0;
    bpf_map_update_elem(&dst_latest, &zero, &orig, BPF_ANY);

    /* Store in LRU hash for inspection */
    __u64 cookie = bpf_get_socket_cookie(ctx);
    bpf_map_update_elem(&dst_lookup, &cookie, &orig, BPF_ANY);

    /* Rewrite to local bridge */
    ctx->user_ip4  = bpf_htonl(0x7f000001u);
    ctx->user_port = bpf_htons(BRIDGE_PORT);

    return 1;
}

char LICENSE[] SEC("license") = "GPL";
