# About the eBPF Architecture Decision: From Dual-Path Proxying to Unified Envoy

> This document explains why the exploit framework's transparent TCP interception moved from a single BPF program with a SocksBridge sidecar to a three-program BPF architecture that routes all traffic through Envoy. It explores the reasoning behind each approach, what made the dual-path design fundamentally fragile, and why paying the cost of three kernel programs was the right trade to make.

> **Scope:** This explanation covers the architectural reasoning behind ADR-PROJ023-008's evolution from Option A to Option C. It does not cover BPF program internals (see the reference documentation), Envoy configuration specifics (see the how-to guide), or the broader engagement lifecycle beyond traffic interception.

## Document Sections

| Section | Purpose |
|---------|---------|
| [The Problem: Why Transparent Proxying Is Hard](#the-problem-why-transparent-proxying-is-hard) | Context for the interception challenge |
| [Three Approaches to Transparent TCP Interception](#three-approaches-to-transparent-tcp-interception) | Conceptual description of each option |
| [Why Unified Envoy Won](#why-unified-envoy-won) | The reasoning and what tipped the balance |
| [The Cost of Three Programs](#the-cost-of-three-programs) | Acknowledging the complexity and why it is worth it |
| [What We Gave Up](#what-we-gave-up) | Honest discussion of trade-offs and limitations |
| [Connection to the Broader Architecture](#connection-to-the-broader-architecture) | How traffic interception fits into the engagement lifecycle |
| [Further Reading](#further-reading) | Links to the ADR, reference doc, and how-to guide |

---

## The Problem: Why Transparent Proxying Is Hard

A penetration testing framework needs to see and control every byte that leaves a tool container. When an operator runs nmap against a target network, or impacket attempts an SMB authentication, or pwntools sends a custom exploit payload, the framework must intercept that traffic, verify the destination falls within the engagement scope, route it through the authorized proxy infrastructure, and log it for evidence integrity. The tool itself should be unaware that any of this is happening -- that is what "transparent" means in this context.

The difficulty arises because tools speak different protocols at different layers. HTTP-based tools like curl or Nuclei happily respect an `HTTP_PROXY` environment variable, and Envoy is purpose-built to handle HTTP traffic with sophisticated routing, filtering, and observability. But raw TCP tools -- the ones that build packets from scratch, speak binary protocols, or open sockets to arbitrary ports -- ignore proxy environment variables entirely. They call `connect()` on a socket and expect to reach the destination directly.

This creates what we came to call the dual-path problem. HTTP traffic has a clean, well-understood path through Envoy. Raw TCP traffic needs a separate mechanism entirely. And that separation is where the architectural weakness lives, because every parallel enforcement path is a parallel escape path.

The fundamental question was not "how do we intercept TCP connections?" -- there are well-known mechanisms for that. The question was "how do we intercept them in a way that produces a single, unified enforcement point rather than two divergent ones?"

---

## Three Approaches to Transparent TCP Interception

### Option A: The Bypass Map and the Bridge

The original design used a single eBPF program attached to each tool container's cgroup at the `connect4` hook point. When any process in the container called `connect()` for an IPv4 destination, the BPF program fired before the kernel's network stack even began forming a packet. It rewrote the destination address, redirecting the connection to a SocksBridge component listening on 127.0.0.1:12345 within the container's network namespace.

SocksBridge was a custom Python component that read the original destination from a BPF map (keyed by socket cookie), then forwarded the traffic through the engagement's SOCKS5 proxy chain. It was, in effect, a userspace relay that translated BPF-intercepted connections into proxied ones.

HTTP traffic, meanwhile, continued to flow through Envoy via the `HTTP_PROXY` environment variable -- a completely separate path with its own scope enforcement, its own logging, and its own failure modes.

This architecture needed a `bypass_ips` map in the BPF program. Without it, the BPF program would intercept Envoy's own outbound connections, the proxy's connections, and connections to the SocksBridge itself, creating redirect loops. The bypass map was essentially an allow-list of IP addresses that the BPF program should leave alone. It was populated at container startup and had to be maintained whenever proxy addresses changed.

The approach worked. It intercepted raw TCP traffic and routed it through the proxy chain. But it carried three compounding problems. First, the bypass map was a mutable data structure that defined which traffic escaped enforcement -- an attractive target for manipulation and a source of subtle misconfiguration bugs. Second, two parallel proxy paths meant two separate scope enforcement implementations, two logging pipelines, and two sets of failure modes to reason about. Third, SocksBridge itself was a custom component with its own attack surface, its own resource consumption, and its own maintenance burden. Every custom component in a security-critical path is a liability.

### Option B: The Kernel Network Stack Approach

The second approach considered was iptables with REDIRECT and TPROXY rules. This is the traditional Linux mechanism for transparent proxying: iptables rules rewrite packet destinations in the kernel's network stack, and the receiving proxy recovers the original destination via `getsockopt(SO_ORIGINAL_DST)` using conntrack state.

The approach is well-understood and battle-tested in many production environments. However, it was rejected for this specific context because it required `CAP_NET_ADMIN` in every tool container -- a significant capability expansion that contradicts the principle of running tools with minimal privileges. The BPF approach, by contrast, attaches programs externally from an init sidecar; the tool containers themselves need zero BPF or networking capabilities.

There is also an isolation granularity gap. iptables rules operate at the network namespace level, not the container level. In Docker's default networking mode, containers sharing a network namespace would share iptables rules, creating cross-container interference. The BPF cgroup-based approach provides per-container isolation because each container has its own cgroup hierarchy.

TPROXY, the more sophisticated variant, requires `IP_TRANSPARENT` socket options and a specific kernel module that may not be available in all environments. This added another layer of environmental dependency without solving the capability escalation problem.

Option B was never a serious contender for the exploit framework. It was evaluated primarily as a completeness exercise -- understanding what the traditional approach offered and why the BPF path was fundamentally better suited to containerized workloads.

### Option C: Three Programs, One Path

The third approach -- the one ultimately selected -- uses three BPF programs working in concert. The first program, `connect4`, fires on every outbound `connect()` call, stores the original destination in a map keyed by socket cookie, and rewrites the destination to Envoy's transparent listener on port 15001. The second program, `sockops`, fires when the TCP connection reaches the `ACTIVE_ESTABLISHED` state and records a mapping from the connection's source port to its socket cookie. The third program, `getsockopt`, intercepts Envoy's `getsockopt(SO_ORIGINAL_DST)` call and performs a two-step lookup -- source port to cookie to original destination -- returning the real target to Envoy.

The critical difference is that ALL traffic, both HTTP and raw TCP, flows through Envoy. There is no SocksBridge. There is no bypass map. Envoy's `original_dst` listener filter recovers the real destination from the BPF chain, and Envoy's route configuration enforces engagement scope for every connection type. HTTP traffic hits Envoy's forward proxy listener as before; raw TCP traffic hits Envoy's transparent TCP listener on a different port but within the same Envoy process, using the same scope enforcement pattern.

Loop prevention -- the problem that the bypass map was built to solve -- is handled through `SO_MARK`. Envoy sets socket mark 100 on all its upstream connections. The `connect4` BPF program checks this mark on every interception and skips the redirect for marked sockets. This is a fundamentally different approach to loop prevention: instead of maintaining a mutable list of addresses to exempt, the proxy identifies itself on every socket it creates. The exemption travels with the socket, not with a separately maintained data structure.

---

## Why Unified Envoy Won

The core insight is deceptively simple: the number of enforcement paths is the number of escape paths. Every time you add a parallel proxy chain, you are not adding to your security posture -- you are adding to the surface area an attacker or a misconfiguration can exploit.

With Option A, an attacker who could manipulate the `bypass_ips` map could exempt arbitrary destinations from BPF interception. Even without malicious manipulation, a misconfiguration in the bypass map could silently allow traffic to reach the network without passing through any proxy. The SocksBridge had its own scope enforcement logic (called OPSEC-F1 in the original design), but that logic had to be implemented, tested, and maintained independently of Envoy's scope enforcement. Two implementations of the same security policy is one implementation too many.

Option C collapses the two paths into one. Envoy is the single enforcement point for all outbound traffic. This means scope enforcement is defined once, in Envoy's route configuration, using Envoy's mature and well-tested filtering pipeline. It means logging and evidence collection happen in one place, through Envoy's access logs. It means failure modes are concentrated in one component rather than distributed across two.

There is an argument, and it is a fair one, that concentrating all traffic through a single component creates a single point of failure. If Envoy crashes, all tool traffic stops. However, this is true of the HTTP path regardless -- HTTP tools already depend entirely on Envoy. The question is whether it is better to have one component whose failure stops everything (and whose failure is therefore immediately visible and quickly diagnosed) or two components whose partial failures create subtle, hard-to-diagnose enforcement gaps. We believe the former is preferable in a security-critical system where silent failure is worse than loud failure.

The decision was also influenced by the maturity gap between the components. Envoy is battle-tested infrastructure maintained by a large open-source community, extensively fuzzed, and deployed at massive scale across the industry. SocksBridge was a custom Python relay written specifically for this framework. When the question is "through which component should security-critical traffic flow?", the answer should favor the component with the deeper testing pedigree and the broader operational track record.

---

## The Cost of Three Programs

Intellectual honesty demands acknowledging that Option C is more complex at the kernel level. One BPF program became three. One BPF map became two. The data flow acquired a temporal dependency -- the `sockops` program must populate the `port_cookie` map before the `getsockopt` program reads it -- that does not exist when a single program handles everything.

This complexity cost is real, and it would be misleading to dismiss it. Three BPF programs means three separate compilation units, three sets of verifier constraints to satisfy, three programs that must be loaded, pinned to the BPF filesystem, and attached to the correct cgroup in the right order. The `BpfManager` component that orchestrates this lifecycle is necessarily more sophisticated than one that manages a single program.

The shared maps introduce their own coordination concerns. Both `dst_lookup` and `port_cookie` are LRU hash maps with 4096 entries. Under extreme concurrency -- more simultaneous connections than the map capacity -- the oldest entries evict automatically. If a connection's entry is evicted before Envoy's `getsockopt` call retrieves it, that connection loses its original destination information. This is a fail-open condition for the evicted connection specifically, though Envoy's route configuration will still reject connections to out-of-scope destinations if it can recover the address by other means.

The temporal dependency between programs is architecturally fundamental. BPF programs cannot synchronize with each other; they fire independently based on kernel events. The `connect4` program stores the original destination when `connect()` is called. The `sockops` program records the port-to-cookie mapping when the TCP handshake completes. The `getsockopt` program reads both maps when Envoy queries the original destination. In practice, the ordering is naturally correct because Envoy's acceptance of a connection happens after the TCP handshake, which is after `sockops` fires. But this is a temporal guarantee based on the Linux kernel's TCP state machine, not an explicit synchronization primitive. A different kernel version or a different TCP implementation could, in principle, change the ordering.

The key question is whether this kernel-level complexity is a net increase or a net decrease in system-wide complexity. We argue it is a net decrease. The three BPF programs replace not just the single BPF program, but also the SocksBridge component, the bypass_ips map, the dual-path scope enforcement logic, and the separate raw TCP logging pipeline. The complexity moved from the application layer -- where it manifested as multiple interacting components with separate failure modes -- to the kernel layer, where it manifests as a well-defined data flow between three cooperating programs. The kernel-level complexity is paid once and debugged once; the application-level complexity of Option A would have been paid on every change to the proxy infrastructure.

---

## What We Gave Up

No architectural decision comes without trade-offs, and it is worth being explicit about what Option C does not solve and what limitations it carries.

The architecture is IPv4-only. The `connect4` BPF program hooks `cgroup/connect4`, which fires only for IPv4 connections. IPv6 is handled operationally by disabling it on tool containers via sysctl at startup. This is pragmatic -- the engagement targets in the current framework are IPv4-addressed -- but it means the architecture will need revisiting if IPv6 targets become relevant. A corresponding `connect6` program would need to be written and integrated into the same map chain.

The BPF programs depend on specific kernel capabilities available in Docker Desktop's LinuxKit kernel. As of this writing, LinuxKit ships kernel 6.12, which supports cgroup BPF attachment, `bpf_get_socket_cookie()`, and the `BPF_CGROUP_SETSOCKOPT` / `BPF_CGROUP_GETSOCKOPT` program types. Docker Desktop kernel updates could introduce breaking changes, though this risk is mitigated by the fact that BPF program types and helper functions have strong backward compatibility guarantees in the Linux kernel's BPF subsystem.

The LRU map eviction behavior under extreme concurrency is a known limitation, not a resolved one. With 4096 entries, the maps comfortably handle hundreds of concurrent connections. But a tool that opens thousands of connections simultaneously -- a port scanner running a full SYN sweep, for example -- could exhaust the map capacity and cause evictions. The evicted connections would lose their original destination information, and Envoy would see an invalid or missing destination from the `getsockopt` call. This is mitigated at the Envoy layer (connections without valid destinations are refused), but it means the tool's connection attempt fails silently rather than being transparently proxied. A future improvement could increase map capacity or implement a dynamic sizing mechanism, though larger maps consume more kernel memory per container.

There is also an operational overhead to the three-program model that should not be understated. Debugging a failed connection requires tracing through three BPF programs and two maps to understand where the data flow broke. The diagnostic path -- "Did `connect4` store the destination? Did `sockops` map the port? Did `getsockopt` find both entries?" -- is longer than Option A's single-program diagnostic. The BPF programs include diagnostic return codes and comments (documented as PM-011 in the implementation) to aid this process, but the cognitive load of debugging a three-stage pipeline is inherently higher than debugging a single stage.

---

## Connection to the Broader Architecture

Traffic interception is one layer in a larger architecture that spans the full engagement lifecycle. Understanding where it fits helps clarify why the unified Envoy approach matters beyond the immediate technical benefits.

The exploit framework operates through a three-zone security model. Zone 1 containers run analysis tools that never touch the network (supply chain scanners, YARA rule engines, static analysis). Zone 2 containers run reconnaissance tools that probe targets passively or actively through the proxy infrastructure. Zone 3 containers run exploitation tools that interact with targets through proxied connections. The BPF interception layer sits at the boundary between tool containers in Zones 2 and 3 and the network, ensuring that every outbound connection passes through Envoy before reaching the proxy chain.

The engagement lifecycle, orchestrated by the `/cyber-ops` skill, follows a six-phase sequence: Define, Provision, Execute, Analyze, Report, Teardown. The BPF architecture is deployed during the Provision phase, when the `BpfManager` loads and attaches all three programs to each tool container's cgroup. During the Execute phase, every tool invocation benefits from the transparent interception without any tool-specific configuration. During Teardown, the `BpfManager` detaches programs and cleans up map pins.

This lifecycle integration is where the unified Envoy approach pays its largest dividend. Because all traffic flows through Envoy, the scope translator -- a component that converts the engagement scope document into Envoy route configuration -- controls the entire enforcement surface with a single configuration update. With Option A's dual-path design, the scope translator would have needed to update both Envoy's route configuration (for HTTP) and SocksBridge's allow-list (for raw TCP). That is two configuration artifacts, two reload mechanisms, and two potential consistency gaps between what HTTP enforcement permits and what TCP enforcement permits.

The connection to evidence integrity is similarly strengthened. Envoy's access logs capture every connection attempt, including the original destination, the proxied destination, and the outcome (allowed or denied). With a single proxy path, the evidence log is complete by construction -- there is no class of traffic that bypasses the logging point. This completeness property would have required explicit verification with Option A, because traffic through SocksBridge would have been logged by a different mechanism in a different format.

---

## Further Reading

- **Decision Record:** ADR-PROJ023-008 (`projects/PROJ-023-exploit-framework/work/design/ADR-PROJ023-008-bpf-vs-iptables.md`) -- the formal architecture decision record documenting the evaluation, original Option A selection, and subsequent supersession by Option C.
- **Reference:** The eBPF reference documentation covers program specifications, map schemas, return codes, and the BpfManager API in neutral, structured detail.
- **How-To Guide:** The eBPF how-to guide covers practical tasks like loading programs, attaching to cgroups, and debugging map lookups.
- **Implementation:** EN-023-009 (three-program BPF implementation) and EN-023-010 (Envoy unified path with SO_MARK loop prevention). Both are internal work items in `projects/PROJ-023-exploit-framework/`.
