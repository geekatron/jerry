// SPDX-License-Identifier: GPL-2.0
// sockops.bpf.c -- Port-to-Cookie Mapping (cgroup/sock_ops)
//
// On BPF_SOCK_OPS_ACTIVE_ESTABLISHED_CB (outbound TCP handshake complete),
// stores source_port -> socket_cookie in the shared port_cookie BPF hash map.
// This mapping is consumed by getsockopt.bpf.c to resolve original
// destinations for Envoy's SO_ORIGINAL_DST interception.
//
// Attach: cgroup/sock_ops on tool container cgroup
// Maps:   port_cookie (write), dst_lookup (present via maps.h, unused here)
//
// TASK-023-169 -- EN-023-009 -- PROJ-023-exploit-framework

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include "maps.h"

SEC("sockops")
int sockops_port_cookie(struct bpf_sock_ops *skops)
{
    /* Only act on outbound TCP connection established events */
    if (skops->op != BPF_SOCK_OPS_ACTIVE_ESTABLISHED_CB)
        return 1;

    /* local_port: tool's ephemeral source port (host byte order, __u32) */
    __u32 src_port = skops->local_port;

    /* Get the socket cookie for this connection */
    __u64 cookie = bpf_get_socket_cookie(skops);

    /* Store source_port -> cookie for getsockopt.bpf.c to chain-lookup */
    bpf_map_update_elem(&port_cookie, &src_port, &cookie, BPF_ANY);

    return 1;
}

char LICENSE[] SEC("license") = "GPL";
