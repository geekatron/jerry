/* SPDX-License-Identifier: GPL-2.0 */
/*
 * maps.h -- Shared BPF map schemas for 3-program architecture
 *
 * Included by: connect4.bpf.c, sockops.bpf.c, getsockopt.bpf.c
 * Constraint C7: map schemas MUST be defined in shared header for consistency.
 * Constraint C2: ENVOY_MARK must be exactly 100.
 * Constraint C8: ENVOY_PORT must be exactly 15001.
 *
 * EN-023-009 -- PROJ-023-exploit-framework
 */

#ifndef __MAPS_H__
#define __MAPS_H__

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

/* Envoy transparent TCP listener port (C8: reserved for Envoy only) */
#define ENVOY_PORT      15001

/* SO_MARK value for Envoy upstream sockets (C2: must be exactly 100) */
#define ENVOY_MARK      100

/* Original destination stored by connect4, read by getsockopt */
struct orig_dst {
    __u32 dst_ip;    /* Network byte order */
    __u32 dst_port;  /* Network byte order, lower 16 bits significant */
};

/*
 * dst_lookup: socket_cookie -> original destination
 * Written by: connect4 (on connect() interception)
 * Read by:    getsockopt (when Envoy calls getsockopt(SO_ORIGINAL_DST))
 *
 * LRU eviction failure mode (CC-015): when >4096 concurrent connections
 * exist, the oldest entries are silently evicted. A getsockopt lookup for
 * an evicted cookie returns NULL, causing the program to return 1
 * (passthrough) — Envoy receives the kernel's default -ENOPROTOOPT.
 * This is fail-open for evicted connections only; active connections
 * within the map capacity are unaffected. Monitor engagement connection
 * concurrency; 4096 covers typical engagement scenarios.
 */
struct {
    __uint(type, BPF_MAP_TYPE_LRU_HASH);
    __uint(max_entries, 4096);
    __type(key,   __u64);            /* socket cookie */
    __type(value, struct orig_dst);
} dst_lookup SEC(".maps");

/*
 * port_cookie: source_port -> socket_cookie
 * Written by: sockops (on ACTIVE_ESTABLISHED)
 * Read by:    getsockopt (to chain source_port -> cookie -> original dst)
 *
 * Key is __u32 to match bpf_sock_ops->local_port type (host byte order).
 *
 * LRU_HASH: auto-evicts oldest entries when full, preventing silent exhaustion
 * under sustained traffic (IN-004/PM-001/SM-006 fix). Also handles TIME_WAIT
 * port reuse (PM-007) by naturally overwriting stale entries.
 */
struct {
    __uint(type, BPF_MAP_TYPE_LRU_HASH);
    __uint(max_entries, 4096);
    __type(key,   __u32);   /* source port, host byte order */
    __type(value, __u64);   /* socket cookie */
} port_cookie SEC(".maps");

#endif /* __MAPS_H__ */
