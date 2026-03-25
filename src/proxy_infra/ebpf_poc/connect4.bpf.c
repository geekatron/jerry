// SPDX-License-Identifier: GPL-2.0
// connect4.bpf.c -- eBPF cgroup/connect4 transparent SOCKS5 redirect
//
// Intercepts every outbound IPv4 connect() from the container cgroup.
// Stores the original {dst_ip, dst_port} in an LRU hash map keyed by
// {src_ip, src_port} so userspace can recover it via bpftool map dump.
// Rewrites the destination to 127.0.0.1:1080 (local microsocks).
//
// Loop prevention: loopback (127.0.0.0/8) connections bypass redirect.
//
// Compile: clang -O2 -target bpf -c connect4.bpf.c -o connect4.bpf.o
//
// EN-023-001 PoC -- PROJ-023-exploit-framework

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

#define SOCKS_PORT      1080
#define LOOPBACK_PREFIX 0x7f000000u  /* 127.0.0.0/8 in host byte order */
#define LOOPBACK_MASK   0xff000000u

/* Map key: PID only (msg_src_ip4 not accessible in cgroup/connect4 context) */
struct conn_key {
    __u32 pid;       /* bpf_get_current_pid_tgid() >> 32 */
    __u32 pad;       /* alignment */
};

/* Map value: original destination before rewrite */
struct orig_dst {
    __u32 dst_ip;    /* network byte order */
    __u16 dst_port;  /* network byte order */
    __u16 pad;
};

/*
 * LRU hash: {src_ip, src_port} -> {original_dst_ip, original_dst_port}
 *
 * LRU eviction prevents unbounded growth without explicit cleanup.
 * 1024 entries covers concurrent connection bursts in a PoC workload.
 * Production: increase to 65536.
 */
struct {
    __uint(type, BPF_MAP_TYPE_LRU_HASH);
    __uint(max_entries, 1024);
    __type(key,   struct conn_key);
    __type(value, struct orig_dst);
} map_orig_dst SEC(".maps");

SEC("cgroup/connect4")
int connect4_redirect(struct bpf_sock_addr *ctx)
{
    __u32 dst_ip;
    __u16 dst_port;

    /* ctx->user_ip4 and ctx->user_port are in network byte order */
    dst_ip   = bpf_ntohl(ctx->user_ip4);
    dst_port = bpf_ntohs((__u16)ctx->user_port);

    /* Skip loopback (127.0.0.0/8) -- includes 127.0.0.1:1080 itself */
    if ((dst_ip & LOOPBACK_MASK) == LOOPBACK_PREFIX)
        return 1;

    /* Store original destination keyed by PID (msg_src_ip4 not accessible) */
    __u64 pid_tgid = bpf_get_current_pid_tgid();
    struct conn_key key = {
        .pid = (__u32)(pid_tgid >> 32),
        .pad = 0,
    };
    struct orig_dst orig = {
        .dst_ip   = ctx->user_ip4,      /* keep network byte order */
        .dst_port = (__u16)ctx->user_port,
        .pad      = 0,
    };
    bpf_map_update_elem(&map_orig_dst, &key, &orig, BPF_ANY);

    /* Rewrite destination to local microsocks on 127.0.0.1:1080 */
    ctx->user_ip4  = bpf_htonl(0x7f000001u);   /* 127.0.0.1 */
    ctx->user_port = bpf_htons(SOCKS_PORT);

    return 1; /* Allow the (rewritten) connection */
}

char LICENSE[] SEC("license") = "GPL";
