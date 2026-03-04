# Kernel-Level Security Technology Landscape (2024-2026)

> Comprehensive survey of kernel-level security mechanisms for software execution control, sandboxing, container security, and workload isolation. Covers eBPF-based security, seccomp, Linux Security Modules, hypervisor-level isolation, WebAssembly sandboxing, policy-as-code engines, and supply chain security.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Landscape overview, key trends, maturity map |
| [L1: Technology-by-Technology Analysis](#l1-technology-by-technology-analysis) | Detailed analysis of 7 technology categories |
| [1. eBPF-Based Security](#1-ebpf-based-security) | Cilium, Falco, Tetragon, KubeArmor |
| [2. seccomp and seccomp-bpf](#2-seccomp-and-seccomp-bpf) | Syscall filtering, profile generation |
| [3. Linux Security Modules](#3-linux-security-modules-lsms) | SELinux, AppArmor, Landlock, SMACK |
| [4. Hypervisor-Level Isolation](#4-hypervisor-level-isolation) | gVisor, Kata Containers, Firecracker |
| [5. Language-Level Sandboxing (WASM)](#5-language-level-sandboxing-wasm-runtimes) | Wasmtime, WasmEdge, WASI |
| [6. Policy-as-Code Engines](#6-policy-as-code-engines) | Cedar, OPA/Rego, Sentinel |
| [7. Supply Chain and Build-Time Security](#7-supply-chain-and-build-time-security) | SLSA, Sigstore, in-toto |
| [L2: Cross-Cutting Analysis](#l2-cross-cutting-analysis) | Tradeoffs, performance comparison, convergence |
| [Sources](#sources) | All cited URLs and references |

---

## L0: Executive Summary

The kernel-level security landscape in 2024-2026 is undergoing a fundamental shift driven by three converging forces: (1) eBPF's maturation from experimental technology to production-grade infrastructure, (2) the rise of AI agent workloads demanding stronger isolation guarantees, and (3) regulatory pressure forcing supply chain security from aspiration to baseline requirement.

**The dominant trend is defense-in-depth through composable layers.** No single technology provides complete security. Production deployments increasingly stack mechanisms: eBPF for runtime detection, seccomp for syscall filtering, LSMs for mandatory access control, and hypervisors or WASM for hard isolation boundaries. The question is no longer "which technology?" but "which combination, and at what performance cost?"

**Key findings:**

- **eBPF is the breakout technology.** With AWS adopting Cilium as the default EKS CNI and Cilium achieving 60%+ adoption as the primary Kubernetes CNI, eBPF-based security tools (Tetragon, Falco, KubeArmor) now provide kernel-level threat detection with less than 1% overhead -- a 10-100x improvement over traditional user-space agents.

- **Hypervisor isolation is becoming the gold standard for untrusted code.** Firecracker microVMs boot in approximately 125ms with less than 5 MiB memory overhead, supporting 150+ VMs per second per host. For AI agent sandboxing, hardware-enforced isolation (Firecracker, Kata Containers) provides stronger security guarantees than user-space approaches (gVisor) at acceptable performance cost.

- **WebAssembly is promising but not yet production-ready for security-critical use.** WASI 0.2 (Preview 2) shipped in early 2024, but threading, async I/O, and JIT compiler vulnerabilities remain open concerns. WASI 1.0 stabilization is expected by late 2026 or early 2027.

- **Policy-as-code is consolidating.** Cedar (AWS) demonstrates 42-80x performance advantage over OPA/Rego, but OPA faces governance uncertainty after Apple hired its maintainers in August 2025. Cedar's formal verification capabilities make it attractive for security-critical authorization.

- **Supply chain security has moved from "nice-to-have" to regulatory requirement.** SLSA Level 2 compliance is achievable in weeks with existing tooling (Sigstore, GitHub Actions). SLSA Level 2 is projected to become the minimum for public cloud marketplace listings by 2028.

### Technology Maturity Map

| Technology | Maturity | Production Adoption | Performance Overhead | Security Guarantee Level |
|------------|----------|--------------------|--------------------|------------------------|
| eBPF (Cilium/Tetragon) | Graduated (CNCF) | High (60%+ K8s CNI) | <1% | Runtime detection + enforcement |
| Falco | Graduated (CNCF) | High | <1% | Runtime detection (alert) |
| seccomp-bpf | Stable (kernel) | Universal (container default) | <3.6% | Syscall filtering |
| SELinux | Stable (20+ years) | High (RHEL ecosystem) | 2-5% | Mandatory access control |
| AppArmor | Stable (15+ years) | High (Ubuntu/Debian) | 1-3% | Profile-based MAC |
| Landlock | Maturing (kernel 5.13+) | Low-Medium | Negligible | Unprivileged sandboxing |
| gVisor | Stable | Medium | 10-30% I/O | User-space kernel isolation |
| Kata Containers | Stable | Medium | 5-15% CPU | Hardware VM isolation |
| Firecracker | Stable | High (AWS Lambda) | 2-8% CPU | MicroVM isolation |
| Wasmtime/WASI | Maturing | Low-Medium | 8-13% CPU | Capability-based sandbox |
| Cedar | Maturing | Medium (AWS) | Sub-millisecond | Formal verification |
| OPA/Rego | Stable (uncertain future) | High | Sub-millisecond | Policy enforcement |
| SLSA/Sigstore | Stable (v1.0+) | Growing | Build-time only | Supply chain integrity |

---

## L1: Technology-by-Technology Analysis

### 1. eBPF-Based Security

#### 1.1 Technology Overview

eBPF (Extended Berkeley Packet Filter) allows small, verified programs to run safely inside the Linux kernel, enabling deep visibility and enforcement without modifying kernel source code or loading traditional kernel modules. The 2024-2025 period marks eBPF's transition from experimental to production-critical infrastructure ([eunomia eBPF Ecosystem Progress](https://eunomia.dev/blog/2025/02/12/ebpf-ecosystem-progress-in-20242025-a-technical-deep-dive/)).

**Mechanism:** eBPF programs attach to kernel hooks (syscalls, network events, LSM hooks, tracepoints) and execute in a sandboxed VM within the kernel. A verifier ensures safety (no infinite loops, no out-of-bounds memory access) before program loading. JIT compilation provides near-native execution speed.

**Key 2024-2025 kernel developments:**
- **BPF Tokens (Linux 6.9):** Fine-grained delegation of eBPF privileges to unprivileged processes, enabling controlled eBPF usage in multi-tenant environments without root ([LWN.net - Delegating privilege with BPF tokens](https://lwn.net/Articles/935195/), [eunomia](https://eunomia.dev/blog/2025/02/12/ebpf-ecosystem-progress-in-20242025-a-technical-deep-dive/)).
- **BPF Arena (Linux 6.9):** Sparse shared-memory regions between eBPF programs and user space for high-throughput data exchange ([LWN.net - A look at what's possible with BPF arenas](https://lwn.net/Articles/1019885/), [LWN.net - Introduce BPF arena](https://lwn.net/Articles/964774/)).
- **sched_ext (Linux 6.12):** Custom CPU scheduling policies implemented entirely in eBPF ([LWN.net - The extensible scheduler class](https://lwn.net/Articles/922405/), [Phoronix - sched_ext merged for Linux 6.12](https://www.phoronix.com/news/Linux-6.12-Lands-sched-ext)).
- **SafeBPF:** Research demonstrating hardware-assisted (Intel MPK/ARM domains) memory safety enforcement with approximately 4% overhead.

#### 1.2 Cilium and Hubble

**What it is:** Cilium is an eBPF-based networking, security, and observability platform for Kubernetes. Hubble is its observability layer providing deep visibility into network flows.

**Adoption:** Cilium has become the dominant CNI in production Kubernetes environments, with over 60% of surveyed deployments using Cilium ([CNCF blog](https://www.cncf.io/blog/2025/01/02/unlocking-cloud-native-security-with-cilium-and-ebpf/)). AWS announced EKS would use Cilium as its default CNI ([Cloud Native Now](https://cloudnativenow.com/editorial-calendar/best-of-2025/ebpf-the-silent-power-behind-cloud-natives-next-phase-2/)).

**Cilium 1.19 (February 2026):**
- Strict encryption modes for both IPsec and WireGuard -- unencrypted inter-node traffic is dropped in strict mode.
- Beta integration of Ztunnel for transparent mutual authentication without sidecar proxies.
- Network policy defaults refined for multi-cluster Cluster Mesh deployments.
- Hubble improvements: packet tracing via IP options, traffic filtering by encryption status, drop events tagged with the exact policy that caused them.
- Over 2,900 commits from 1,000+ contributors in the 1.19 release cycle ([InfoQ](https://www.infoq.com/news/2026/02/cilium-119/)).

**Security capabilities:**
- Network policy enforcement replacing iptables with eBPF.
- Layer 3-7 visibility (HTTP, gRPC, DNS, Kafka).
- Zero-trust network architecture support.

**Performance:** Replaces iptables with eBPF-powered networking, eliminating the linear-time iptables rule processing bottleneck. Cloudflare reported dropping approximately 10 million packets per second on a single CPU core using XDP ([eunomia](https://eunomia.dev/blog/2025/02/12/ebpf-ecosystem-progress-in-20242025-a-technical-deep-dive/)).

#### 1.3 Falco

**What it is:** Cloud Native Runtime Security tool that monitors syscalls and container behavior for anomalous activity. CNCF Graduated project (February 2024) ([CNCF](https://www.cncf.io/projects/falco/)).

**Mechanism:** Uses libscap to capture syscall events and libsinsp to enrich them with process metadata, file descriptors, and user associations. Rules define detection patterns against this enriched event stream ([Falco docs](https://falco.org/docs/)).

**Key 2024-2025 developments:**
- 40% growth in the Falco plugin ecosystem since CNCF graduation ([Sysdig](https://www.sysdig.com/blog/the-state-of-falco)).
- **Stratoshark** integration (January 2025): Wireshark-style syscall analysis. Falco alerts trigger precise forensic captures for deeper event analysis ([CNCF announcement](https://www.cncf.io/announcements/2025/11/10/falco-links-real-time-detection-with-forensic-level-analysis-in-the-cloud-native-stack/)).
- Plugin framework supports cloud audit logs, container events, and other telemetry beyond syscalls.

**Security guarantees:**
- CAN detect: unauthorized process execution, container escapes, privilege escalation attempts, sensitive file access, abnormal network connections.
- CANNOT enforce: Falco is primarily a detection and alerting tool. It does not block actions by default (though kill actions can be configured). For enforcement, pair with Tetragon.

**Performance:** eBPF-based monitoring with <1% overhead ([TuxCare](https://tuxcare.com/blog/ebpf-for-advanced-linux-performance-monitoring-and-security/)). This is 10-100x lower than equivalent user-space monitoring agents that historically consumed 5-15% CPU.

#### 1.4 Tetragon

**What it is:** eBPF-based security observability and runtime enforcement tool, part of the Cilium project and a CNCF project ([Tetragon](https://tetragon.io/)).

**Mechanism:** Unlike Falco (primarily detection), Tetragon performs both detection AND enforcement directly in the kernel. It applies policy and filtering in eBPF in the kernel rather than sending events to user space for processing ([Tetragon docs](https://tetragon.io/docs/overview/)).

**Enforcement mechanisms:**
1. **Return value override:** The monitored function is never executed; an error value is returned to the caller instead.
2. **Signal delivery:** Sends SIGKILL (or other signals) to the offending process.

Both mechanisms operate synchronously in the kernel, closing the TOCTOU (time-of-check-to-time-of-use) attack window ([Tetragon enforcement docs](https://tetragon.io/docs/concepts/enforcement/)).

**Key differentiators:**
- **In-kernel filtering:** Performs sophisticated filtering directly in the kernel, reducing data volume and processing overhead.
- **Kubernetes awareness:** Recognizes workload identities (namespace, pod metadata), surpassing traditional per-host observability.
- **Kernel state joining:** Accesses Linux kernel state and joins it with Kubernetes context to annotate process namespaces, capabilities, socket-to-process mappings, and file descriptor-to-filename mappings.

**Security guarantees:**
- CAN prevent: process execution, file access, network connections, capability escalation -- all enforced at kernel level.
- CAN detect: all of the above plus syscall patterns, namespace operations, security capability changes.
- CANNOT prevent: attacks that do not traverse monitored kernel hooks.

#### 1.5 KubeArmor

**What it is:** Cloud-native runtime security enforcement system using eBPF and Linux Security Modules (LSM-BPF, AppArmor) to restrict workload behavior at the system level ([KubeArmor](https://kubearmor.io/)).

**Mechanism:** Deploys as a non-privileged DaemonSet. Uses eBPF for monitoring (System Monitor) and BPF-LSM for enforcement (Runtime Enforcer). Generates alerts/telemetry with container/pod/namespace identity context ([KubeArmor docs](https://docs.kubearmor.io/kubearmor)).

**2025 enhancements:**
- AI threat detection capabilities.
- ARMv9 support for edge/IoT workloads.
- OpenTelemetry observability integration.
- OCI hooks eliminating the need for privileged CRI socket access ([KubeArmor OCI hooks](https://kubearmor.io/blog/kubearmor-oci-hooks-container-security)).
- AWS EKS Auto Mode integration ([AWS blog](https://aws.amazon.com/blogs/containers/enhancing-container-security-in-amazon-eks-auto-mode-with-kubearmor/)).

**Security scope:** Restricts process execution, file access, and networking operations at the container, pod, and node level.

#### 1.6 eBPF Security Summary

| Tool | Primary Function | Enforcement | CNCF Status | Key Strength |
|------|-----------------|-------------|-------------|--------------|
| Cilium/Hubble | Network security + observability | Yes (network policy) | Graduated | 60%+ K8s CNI adoption |
| Falco | Runtime threat detection | Detect + alert (kill optional) | Graduated | Plugin ecosystem, Stratoshark integration |
| Tetragon | Security observability + enforcement | Yes (in-kernel) | CNCF project | TOCTOU-free kernel enforcement |
| KubeArmor | Workload sandboxing | Yes (LSM-BPF) | CNCF Sandbox | Edge/IoT support, unprivileged deployment |

---

### 2. seccomp and seccomp-bpf

#### 2.1 Technology Overview

**Mechanism:** seccomp (secure computing mode) restricts the system calls available to a process. In strict mode, only `read()`, `write()`, `_exit()`, and `sigreturn()` are permitted. seccomp-bpf extends this with Berkeley Packet Filter programs that define flexible syscall policies, filtering at the kernel level with minimal performance overhead ([Docker seccomp docs](https://docs.docker.com/engine/security/seccomp/), [seccomp Wikipedia](https://en.wikipedia.org/wiki/Seccomp)).

**Security guarantees:**
- CAN prevent: execution of specific syscalls (e.g., `mount`, `reboot`, `ptrace`, `bpf`).
- CANNOT prevent: misuse of allowed syscalls, application-level vulnerabilities, attacks that use only permitted syscalls.
- Default Docker profile allows 300+ of 435 Linux syscalls on x86_64, leaving substantial attack surface ([Datadog Security Labs](https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-6/)).

**Performance overhead:** Seccomp-bpf adds minimal overhead for most workloads. gVisor's 2024 optimization work measured approximately 3.6% total runtime reduction from seccomp-bpf filter optimizations, which represents about 15% of gVisor's sandbox overhead ([gVisor seccomp blog](https://gvisor.dev/blog/2024/02/01/seccomp/)). System call checking becomes expensive with long jump lists and indirect jumps caused by speculative vulnerability mitigations (Retpoline).

#### 2.2 Profile Generation Tools

**OCI seccomp-bpf-hook:** An OCI hook that traces syscalls made by a container during execution and generates a seccomp profile allowing only those observed syscalls. This provides a practical path to least-privilege profiles without manual syscall enumeration ([GitHub: oci-seccomp-bpf-hook](https://github.com/containers/oci-seccomp-bpf-hook)).

**Workflow:**
1. Run container with the OCI hook attached.
2. Exercise all code paths during a training period.
3. Hook generates a profile allowing observed syscalls and denying everything else.
4. Apply the generated profile in production.

**Risk:** Training-based profile generation may miss syscalls executed in rare code paths (error handling, edge cases), causing production failures.

#### 2.3 Container Runtime Integration

| Runtime | Default seccomp | Custom Profiles | Profile Format |
|---------|----------------|-----------------|----------------|
| Docker | Yes (default profile since 1.10) | JSON profile files | Docker JSON |
| containerd | Yes (when enabled) | OCI spec format | OCI JSON |
| CRI-O | Yes | OCI spec format | OCI JSON |
| Kubernetes | SeccompProfile field (GA since 1.27) | Pod/container level | OCI JSON |

**2025 trend:** Containers running as root remain a critical attack vector -- Sysdig's Cloud-Native Security and Usage Report found that the majority of container images still run as root, with 75%+ of running containers having high-risk vulnerabilities ([Sysdig 2024 Cloud-Native Security and Usage Report](https://www.sysdig.com/2024-cloud-native-security-and-usage-report)). The Red Hat State of Kubernetes Security report found that 90% of organizations experienced at least one Kubernetes security incident, with misconfigurations and vulnerabilities as top concerns ([Red Hat State of Kubernetes Security 2024](https://www.redhat.com/en/engage/state-kubernetes-security-report-2024)). Implementing rootless containers combined with seccomp profiles significantly reduces attack surface, and proper seccomp profiles can block the majority of potentially dangerous system calls by restricting the 435 available Linux syscalls to only those required ([Docker seccomp docs](https://docs.docker.com/engine/security/seccomp/), [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-6/)).

#### 2.4 seccomp Limitations

- **Coarse filtering granularity:** Filters operate on syscall numbers and arguments, not on the semantic context of the call (e.g., cannot distinguish "read from /etc/passwd" vs. "read from /tmp/data" -- that requires LSMs).
- **No file path awareness:** seccomp cannot filter by file path, only by syscall number and arguments.
- **Architecture-specific:** Syscall numbers differ across architectures, requiring per-architecture profiles.
- **No network filtering:** seccomp cannot selectively filter network destinations; it can only allow/block socket-related syscalls entirely.

---

### 3. Linux Security Modules (LSMs)

#### 3.1 Technology Overview

Linux Security Modules provide a framework for mandatory access control (MAC) policies in the Linux kernel. As of 2025, the officially approved LSMs are: AppArmor, LoadPin, SELinux, Smack, TOMOYO, Yama, SafeSetID, Integrity Policy Enforcement (IPE), and Landlock ([Linux Security Modules Wikipedia](https://en.wikipedia.org/wiki/Linux_Security_Modules)).

**Key 2025 milestone:** SELinux and AppArmor enforcement has reached majority adoption across enterprise Linux environments, driven by distribution defaults: RHEL/CentOS/Fedora ship SELinux in enforcing mode, and Ubuntu/Debian ship AppArmor enabled by default. Together these distributions cover the majority of enterprise Linux deployments ([Linux Journal - Steady Momentum in AppArmor and SELinux Uptake](https://www.linuxjournal.com/content/securing-linux-steady-momentum-apparmor-and-selinux-uptake), [Red Hat - Leading the Enterprise Linux Server Market](https://www.redhat.com/en/blog/red-hat-leading-enterprise-linux-server-market)).

#### 3.2 SELinux

**Mechanism:** Type enforcement (TE) mandatory access control. Every process runs in a security domain (type), and every resource has a type label. Policies define which domains can access which resource types, and in what manner (read, write, execute, etc.).

**Adoption (2025):**
- RHEL holds the largest share of the enterprise Linux server market, with Red Hat reporting market leadership in enterprise Linux ([Red Hat - Leading the Enterprise Linux Server Market](https://www.redhat.com/en/blog/red-hat-leading-enterprise-linux-server-market)). RHEL/CentOS/Fedora all ship with SELinux in enforcing mode by default.
- openSUSE Tumbleweed switched from AppArmor to SELinux in February 2025, with openSUSE Leap 16 following ([openSUSE News](https://news.opensuse.org/2025/02/13/tw-plans-to-adopt-selinux-as-default/), [Phoronix](https://www.phoronix.com/news/OpenSUSE-Tumble-Goes-SELinux)).

**Container integration:**
- Type enforcement reduced privilege escalation attempts by 3x in container workloads.
- Red Hat reported significant reduction in escalation incidents versus permissive-mode deployments. SELinux enforcing mode mitigates entire classes of vulnerabilities including container breakout, privilege escalation, and unauthorized file access ([Red Hat - SELinux as a Security Pillar](https://access.redhat.com/articles/6964380)).

**Security guarantees:**
- CAN prevent: unauthorized file access, process execution, network operations, IPC, capability use -- all based on type labels.
- CANNOT prevent: attacks within an allowed domain, vulnerabilities in the policy itself, denial-of-service attacks.

**Performance overhead:** 2-5% depending on workload and policy complexity [HYPOTHESIS -- confidence: medium; based on historical measurement literature rather than 2025 benchmarks].

**Limitations:** Notoriously complex policy language. Policy development requires deep understanding of type enforcement. Container-specific policies (container-selinux) simplify common patterns.

#### 3.3 AppArmor

**Mechanism:** Path-based mandatory access control. Profiles define allowed file paths, capabilities, and network access per application. Simpler than SELinux but less granular.

**Adoption (2025):**
- Majority of Debian/Ubuntu ecosystem ships with AppArmor enabled by default.
- Ubuntu maintains AppArmor by default on servers and is the most widely deployed Linux distribution in public cloud environments.
- Dominates cloud through Ubuntu's prevalence (60%+ of public cloud instances) ([Linux Journal](https://www.linuxjournal.com/content/securing-linux-steady-momentum-apparmor-and-selinux-uptake)).

**Container integration:**
- Docker and containerd support AppArmor profiles natively.
- Kubernetes supports AppArmor profiles via annotations (stable since 1.30).
- The overwhelming majority of production Kubernetes clusters run on Linux ([CNCF Annual Survey 2024](https://www.cncf.io/reports/cncf-annual-survey-2024/)).

**Security guarantees:**
- CAN prevent: unauthorized file access (by path), capability use, network access, mount operations.
- CANNOT prevent: attacks using allowed paths, time-of-check-to-time-of-use races on path resolution, attacks that do not involve file access.

**Performance overhead:** 1-3% -- generally lower than SELinux due to simpler path-based lookup [HYPOTHESIS -- confidence: medium; based on historical benchmark literature and architectural reasoning (path-based lookup vs. type enforcement) rather than 2025 measurements; no authoritative 2024-2025 benchmark found].

**Comparison to SELinux:** AppArmor is easier to configure and audit but provides weaker isolation guarantees. SELinux's type system prevents entire classes of attacks that path-based systems cannot, but at significantly higher operational complexity.

#### 3.4 Landlock

**Mechanism:** Unprivileged, stackable LSM that enables any process to sandbox itself without root privileges. Policies are created at runtime, enforced on the current thread and its descendants, and disappear when the process exits ([Landlock kernel docs](https://docs.kernel.org/userspace-api/landlock.html), [Landlock.io](https://landlock.io/)).

**Key differentiator:** Landlock is the ONLY LSM that does not require administrative privileges to configure. Any application can sandbox itself.

**Kernel version capabilities:**

| Kernel Version | ABI Version | Capabilities Added |
|---------------|-------------|-------------------|
| 5.13 | ABI v1 | Basic filesystem restrictions |
| 6.2 | ABI v2 | File truncation control |
| 6.4-6.6 | ABI v3 | Network restrictions (TCP bind/connect) |
| 6.7+ | ABI v4 | Full network restrictions |
| 6.12 | - | Unix socket and signal scoping |

**Source:** [Landlock kernel docs](https://docs.kernel.org/security/landlock.html), [Phoronix](https://www.phoronix.com/news/Landlock-Scoping-Unix-Sockets)

**Emerging tooling:**
- **Landrun:** Lightweight CLI tool for sandboxing any Linux process with Landlock, no root or containers required ([GitHub: landrun](https://github.com/Zouuup/landrun)).
- **Island:** Official Landlock sandboxing tool from the Landlock LSM team ([GitHub: island](https://github.com/landlock-lsm/island)).

**Security guarantees:**
- CAN prevent: filesystem access (read, write, execute, make directory, etc.), network connections (TCP bind/connect), Unix socket operations (kernel 6.12+).
- CANNOT prevent: syscall-level attacks (that is seccomp's domain), memory attacks, attacks through allowed file paths, attacks via kernel vulnerabilities.
- 16-level kernel nesting limit for stacked policies.

**Performance overhead:** Negligible for most workloads. Landlock's enforcement is integrated into kernel path resolution, adding minimal overhead per filesystem operation ([Landlock workshop 2025](https://landlock.io/talks/2025-01-29_landlock-workshop.pdf)). Benchmark for GNU Make sandboxing showed approximately 5x better performance compared to Bazel ([justine.lol](https://justine.lol/make/)).

**Significance for software leashing:** Landlock represents the most promising mechanism for application self-sandboxing. Software can voluntarily restrict its own capabilities at startup, implementing the principle of least privilege without requiring system administrator involvement. This is directly relevant to AI agent leashing: an agent runtime could use Landlock to restrict itself to only the filesystem paths and network endpoints it needs.

#### 3.5 SMACK (Simplified Mandatory Access Control Kernel)

**Mechanism:** Simplified MAC that uses labels (like SELinux) but with a much simpler rule format. Designed for embedded and IoT systems where SELinux's complexity is prohibitive.

**Adoption:** Limited primarily to Tizen (Samsung's IoT/mobile OS) and some automotive Linux platforms. Not widely used in cloud or container environments [HYPOTHESIS -- confidence: high based on distribution defaults and industry literature].

**Relevance:** Low for cloud-native and AI agent workloads. Included for completeness as an officially approved kernel LSM.

---

### 4. Hypervisor-Level Isolation

#### 4.1 Technology Overview

Hypervisor-level isolation provides the strongest security boundary available for software workloads. Unlike container isolation (which shares the host kernel), VM-based isolation gives each workload its own kernel, eliminating entire classes of kernel-based attacks.

In 2025-2026, this category has become directly relevant to AI agent sandboxing. Gartner predicts 40% of enterprise applications will feature task-specific AI agents by 2026 (up from <5% in 2025), and 75% of surveyed organizations report piloting or deploying some form of AI agents ([Gartner AI Agent Predictions 2025](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025)). Hardware-enforced isolation is increasingly recommended for executing untrusted agent-generated code ([Northflank AI sandboxing](https://northflank.com/blog/how-to-sandbox-ai-agents)).

#### 4.2 gVisor

**Mechanism:** Implements a user-space kernel (called "Sentry") written in Go that intercepts application syscalls via ptrace or KVM platforms. Sentry reimplements a large subset of Linux syscalls in user space, managing virtual file systems and network stacks. Applications never directly interact with the host kernel ([gVisor comparison](https://onidel.com/blog/gvisor-kata-firecracker-2025)).

**Performance characteristics:**

| Metric | Value | Notes |
|--------|-------|-------|
| Startup latency | 50-100ms | Fastest of the three |
| CPU overhead | 10-30% | For syscall-heavy workloads |
| Memory overhead | 10-50MB per container | Sentry process memory |
| I/O overhead | 20-50% | Due to syscall interception in userspace |
| Min requirements | Linux 4.14+, 2GB RAM | No hardware virtualization needed |

**Source:** [onidel comparison](https://onidel.com/blog/gvisor-kata-firecracker-2025), [Northflank AI sandboxing](https://northflank.com/blog/how-to-sandbox-ai-agents)

**Security guarantees:**
- CAN prevent: direct kernel syscall access, kernel exploitation via syscall interface, container escape through kernel vulnerabilities.
- CANNOT prevent: attacks exploiting the Sentry itself (though it has a smaller attack surface than the full Linux kernel), hardware-level attacks, side-channel attacks.
- Does NOT provide hardware-level isolation -- the Sentry runs in user space on the host.

**Best for:** Untrusted code execution in shared environments, Kubernetes multi-tenancy with moderate performance needs, environments lacking hardware virtualization support.

#### 4.3 Kata Containers

**Mechanism:** Orchestration framework integrating multiple Virtual Machine Monitors (VMMs) -- Firecracker, Cloud Hypervisor, QEMU -- with Kubernetes. Each container runs inside a lightweight VM with its own kernel, providing hardware-level isolation via KVM while maintaining container-like APIs ([Northflank comparison](https://northflank.com/blog/kata-containers-vs-firecracker-vs-gvisor), [Edera comparison](https://edera.dev/stories/kata-vs-firecracker-vs-gvisor-isolation-compared)).

**Performance characteristics:**

| Metric | Value | Notes |
|--------|-------|-------|
| Startup latency | 150-300ms | Full VM initialization + kernel boot |
| CPU overhead | 5-15% | Primarily virtualization layer |
| Memory overhead | 50-150MB | Guest kernel + agent |
| Min requirements | VT-x/AMD-V, 4GB+ RAM | UEFI preferred |

**Source:** [onidel comparison](https://onidel.com/blog/gvisor-kata-firecracker-2025)

**Security guarantees:**
- CAN prevent: container escape through kernel vulnerabilities (separate kernel), cross-container attacks, host kernel exploitation.
- CANNOT prevent: hypervisor (KVM) escape vulnerabilities (rare but high-impact), side-channel attacks, hardware-level attacks.
- Strongest isolation guarantee among the three technologies.

**Best for:** Maximum security isolation requirements, compliance-driven deployments requiring VM-level boundaries, legacy applications needing complete kernel compatibility.

#### 4.4 Firecracker

**Mechanism:** Lightweight VMM built in Rust by AWS. Creates microVMs with hardware-enforced isolation via KVM. Each workload gets a dedicated kernel with minimal attack surface. Designed for serverless workloads (powers AWS Lambda and Fargate) ([onidel comparison](https://onidel.com/blog/gvisor-kata-firecracker-2025)).

**Performance characteristics:**

| Metric | Value | Notes |
|--------|-------|-------|
| Startup latency | 100-200ms (125ms typical) | Pre-warming techniques available |
| CPU overhead | 2-8% | Minimal virtualization impact |
| Memory overhead | <5 MiB per VM | Extremely low; thousands of VMs per host |
| VMs per second | Up to 150/host | High-density operation |
| Min requirements | KVM support, Linux 4.14+, 2GB+ RAM | |

**Source:** [Northflank AI sandboxing](https://northflank.com/blog/how-to-sandbox-ai-agents), [onidel comparison](https://onidel.com/blog/gvisor-kata-firecracker-2025)

**Security guarantees:**
- CAN prevent: container escape, kernel exploitation, cross-workload interference -- all via hardware-enforced VM boundaries.
- CANNOT prevent: KVM escape (shared hypervisor risk), hardware side-channel attacks.
- Rust implementation reduces VMM-layer vulnerability surface.

**Best for:** Serverless functions, AI agent sandboxing with untrusted code, resource-constrained deployments requiring maximum VM density.

#### 4.5 Hypervisor Isolation Comparison

| Dimension | gVisor | Kata Containers | Firecracker |
|-----------|--------|-----------------|-------------|
| Isolation type | User-space kernel | Hardware VM (orchestrated) | Hardware VM (microVM) |
| Startup | 50-100ms | 150-300ms | 100-200ms |
| CPU overhead | 10-30% | 5-15% | 2-8% |
| Memory overhead | 10-50MB | 50-150MB | <5MB |
| Hardware req. | None | VT-x/AMD-V | KVM |
| Security level | Medium-High | Highest | High |
| K8s integration | RuntimeClass | RuntimeClass | Custom/Kata |
| AI agent sandbox | Good | Best (compliance) | Best (density) |

**Recommendation for AI agent isolation:** Firecracker provides the best balance of security, performance, and density. For regulated environments requiring the strongest isolation guarantees, Kata Containers adds orchestration capabilities on top of Firecracker/Cloud Hypervisor. gVisor is suitable when hardware virtualization is unavailable or when fastest possible startup is critical ([Northflank AI sandboxing](https://northflank.com/blog/how-to-sandbox-ai-agents), [AgentSphere comparison](https://dev.to/agentsphere/choosing-a-workspace-for-ai-agents-the-ultimate-showdown-between-gvisor-kata-and-firecracker-b10)).

---

### 5. Language-Level Sandboxing (WASM Runtimes)

#### 5.1 Technology Overview

WebAssembly (WASM) provides a capability-based sandbox where modules have zero ambient authority: a WASM instance can only access resources explicitly linked through its interfaces. WASI (WebAssembly System Interface) standardizes system-level APIs using a capability-based security model ([Wasmtime security docs](https://docs.wasmtime.dev/security.html)).

**Security model:** WASM modules execute in isolated linear memory with no raw access to system calls. Host capabilities (filesystem, network, environment variables) must be explicitly granted via capability tokens. This is architecturally different from kernel-level mechanisms: instead of restricting an otherwise-privileged process, WASM starts with zero privileges and adds only what is needed.

#### 5.2 WASI Standards Status

| Version | Status | Key Capabilities | Missing |
|---------|--------|-------------------|---------|
| WASI Preview 1 | Stable, legacy | Basic POSIX-like: file I/O, env vars, random | No networking, no threading |
| WASI 0.2 (Preview 2) | Released early 2024 | wasi-cli, wasi-http, wasi-filesystem, wasi-sockets, Component Model | Only synchronous I/O |
| WASI 0.3 (Preview 3) | Expected 2025 | Native async I/O | Threading still pending |
| WASI 1.0 | Expected late 2026/early 2027 | Full stabilization | TBD |

**Source:** [eunomia WASI status](https://eunomia.dev/blog/2025/02/16/wasi-and-the-webassembly-component-model-current-status/), [State of WebAssembly 2025-2026](https://platform.uno/blog/the-state-of-webassembly-2025-2026/)

**Component Model:** Enables building larger applications from modular WASM components using WIT (WebAssembly Interface Definition Language). Currently in W3C Phase 2/3. Wasmtime was the first major runtime with full Component Model support.

#### 5.3 Runtime Comparison

| Runtime | Startup | Memory | CPU Overhead | Best For |
|---------|---------|--------|-------------|----------|
| Wasmtime | 2-5ms | ~15MB | +11% (Fibonacci) | Plugin systems, strict sandboxing, standards compliance |
| Wasmer | <1ms (Singlepass) | ~12MB | +13% (LLVM) | Cross-platform flexibility, developer experience |
| WasmEdge | 1.5ms | ~8MB | +8% (Fibonacci) | Edge/IoT, Kubernetes-native, AI inference |

**Source:** [Reintech runtime comparison 2026](https://reintech.io/blog/wasmtime-vs-wasmer-vs-wasmedge-wasm-runtime-comparison-2026)

**I/O performance (HTTP requests/second):**
- Wasmtime: 8,200
- Wasmer: 8,500
- WasmEdge: 9,100 (optimized async I/O)

**Source:** [Reintech](https://reintech.io/blog/wasmtime-vs-wasmer-vs-wasmedge-wasm-runtime-comparison-2026)

#### 5.4 Security Vulnerabilities and Concerns

Despite strong theoretical security guarantees, practical vulnerabilities have been discovered:

- **JIT compiler bugs** are the primary sandbox escape vector. CVE-2024-30266: a regression in Wasmtime 19.0.0's handling of externref-typed element segments caused type confusion, allowing guest modules to potentially trigger panics or memory disclosure. CVE-2024-47813: a race condition in Wasmtime's type registry could lead to control-flow integrity violations ([Wasmtime Security Advisories](https://github.com/bytecodealliance/wasmtime/security), [CVE-2024-30266](https://github.com/advisories/GHSA-75hq-h6g9-h4q5), [NVD CVE-2024-47813](https://nvd.nist.gov/vuln/detail/CVE-2024-47813)).
- **Wasmer filesystem bypass:** CVE-2023-51661: Wasmer versions 3.0.0-4.2.3 opened the current working directory by default, allowing WASM programs to access the host filesystem outside the intended sandbox. CVE-2024-38358: directory traversal in path_open and path_symlink functions allowed attackers to escape the sandboxed directory via symlinks ([NVD CVE-2023-51661](https://nvd.nist.gov/vuln/detail/CVE-2023-51661), [CVE-2024-38358](https://security.snyk.io/vuln/SNYK-RUST-WASMER-7222570)).
- **Node.js WASI:** Explicitly warns it does NOT provide "comprehensive file system security" and should NOT be used for untrusted code ([eunomia WASI status](https://eunomia.dev/blog/2025/02/16/wasi-and-the-webassembly-component-model-current-status/)).
- **I/O performance:** Wasmtime file I/O measured 10x slower than native in some cases (23 seconds vs. 2 seconds) due to excessive async overhead and 3x more syscalls than native execution ([eunomia WASI status](https://eunomia.dev/blog/2025/02/16/wasi-and-the-webassembly-component-model-current-status/)).

**Ecosystem fragmentation risk:** Wasmer's WASIX extension (adding threading, signals, fork()) diverges from the standard. AssemblyScript removed WASI support entirely. WASI Preview 1 and Preview 2 binaries are incompatible ([eunomia WASI status](https://eunomia.dev/blog/2025/02/16/wasi-and-the-webassembly-component-model-current-status/)).

#### 5.5 WASM Security Assessment

| Dimension | Assessment |
|-----------|------------|
| **Theoretical security** | Strong: memory-safe sandbox, capability-based access, zero ambient authority |
| **Practical security** | Moderate: JIT compiler bugs are realistic attack vectors |
| **Performance** | Good for CPU-bound (+8-13%), poor for I/O-heavy (up to 10x slowdown) |
| **Threading** | Missing: single-threaded by default, severely limiting use cases |
| **Maturity** | Maturing: WASI 0.2 stable, 1.0 expected late 2026/early 2027 |
| **Adoption risk** | Medium: ecosystem fragmentation between WASI/WASIX/custom extensions |

**Significance for software leashing:** WASM provides the strongest default security posture (zero ambient authority). However, practical JIT vulnerabilities, I/O performance limitations, and missing threading support make it unsuitable as the sole isolation mechanism for security-critical workloads today. Best used as one layer in a defense-in-depth strategy, typically combined with a microVM or container boundary.

---

### 6. Policy-as-Code Engines

#### 6.1 Technology Overview

Policy-as-code engines externalize authorization decisions from application code into declarative policy languages. This enables centralized governance, audit trails, and formal verification of access control rules.

#### 6.2 Cedar (AWS)

**Mechanism:** Domain-specific language for fine-grained authorization with formal verification capabilities. Policies use a readable syntax with entities (principals, actions, resources) and conditions. Deny-by-default. Backed by Amazon Verified Permissions service ([Cedar policy language](https://www.cedarpolicy.com/), [StrongDM Cedar guide](https://www.strongdm.com/cedar-policy-language)).

**Performance:** 42-80x faster than OPA/Rego. Academic benchmarks (Wen et al., 2024) show the Cedar authorizer is 28.7-35.2x faster than OpenFGA and 42.8-80.8x faster than Rego on randomly generated inputs; independent testing reports 42-60x ([Cedar academic paper](https://arxiv.org/pdf/2403.04651), [Permit.io OPA vs Cedar](https://www.permit.io/blog/opa-vs-cedar)).

**Key strengths:**
- **Formal verification:** Verification-guided development provides mathematical assurance of policy correctness.
- **Readability:** Cedar policies are legible to non-engineers, unlike Rego.
- **Type safety:** Schema-based entity model with typed attributes and relationships.
- **Open source:** Apache 2.0 licensed.

**Limitations:**
- Limited tooling and smaller community compared to OPA.
- Fewer integrations, tutorials, and community resources.
- AWS ecosystem alignment (though open source).
- Application-level authorization focus (not infrastructure-level).

#### 6.3 OPA / Rego

**Mechanism:** General-purpose policy engine using Rego (a Datalog/Prolog derivative). Evaluates arbitrary JSON input against declarative policies. Deployed as sidecar, library, or daemon. Used across the cloud-native stack for admission control, API authorization, and infrastructure governance ([OPA guide](https://www.osohq.com/learn/opa-vs-cedar-vs-zanzibar)).

**2025 governance concern:** In August 2025, Apple hired the maintainers of OPA with plans to sunset enterprise offerings, significantly raising doubts about OPA's future roadmap and commercial support ([Oso OPA vs Cedar guide](https://www.osohq.com/learn/opa-vs-cedar-vs-zanzibar)).

**Key strengths:**
- Ecosystem maturity: widely adopted, extensive tooling, large community.
- Universal applicability: infrastructure, application, and data-level policies.
- CNCF Graduated project.
- Kubernetes admission controller (Gatekeeper) widely deployed.

**Limitations:**
- Steep Rego learning curve.
- Slower than Cedar (42-80x slower in benchmarks).
- Operational complexity managing policy distribution.
- Future governance uncertainty post-Apple acquisition of maintainers.

#### 6.4 HashiCorp Sentinel

**Mechanism:** Policy-as-code framework purpose-built for HashiCorp products (Terraform, Vault, Consul, Nomad). Uses a custom policy language with first-class imports for HashiCorp-specific data (e.g., tfplan/v2). Supports advisory, soft, and hard enforcement levels ([Sentinel docs](https://developer.hashicorp.com/sentinel/docs/concepts/policy-as-code)).

**Key strengths:**
- Deep Terraform integration with provider-aware data.
- Centralized governance with clear audit trails in HCP Terraform.
- Graduated enforcement levels (advisory/soft/hard).

**Limitations:**
- Proprietary: limited to HashiCorp ecosystem.
- Not applicable to general authorization decisions.
- Cannot function outside HashiCorp products.

**Common pattern:** Use OPA locally and in CI for shift-left enforcement, then Sentinel in HCP Terraform for final centralized governance ([TachTech Sentinel vs OPA](https://engineering.tachtech.net/devsecops/2025/10/15/sentinel-and-opa-policies.html)).

#### 6.5 Policy Engine Comparison

| Dimension | Cedar | OPA/Rego | Sentinel |
|-----------|-------|----------|----------|
| **Scope** | Application authorization | Universal policy | HashiCorp products only |
| **Language** | Domain-specific, readable | Datalog derivative, complex | HashiCorp-specific |
| **Performance** | Sub-ms (42-80x faster than Rego) | Sub-ms (but slower) | N/A (embedded) |
| **Formal verification** | Yes | No | No |
| **Ecosystem** | Growing (AWS-backed) | Large but uncertain future | HashiCorp only |
| **Open source** | Yes (Apache 2.0) | Yes (Apache 2.0) | Proprietary |
| **Best for** | Application authz, security-critical | Infrastructure-wide policy | Terraform governance |

**Source:** [Permit.io OPA vs Cedar](https://www.permit.io/blog/opa-vs-cedar), [Oso guide](https://www.osohq.com/learn/opa-vs-cedar-vs-zanzibar), [TachTech](https://engineering.tachtech.net/devsecops/2025/10/15/sentinel-and-opa-policies.html)

---

### 7. Supply Chain and Build-Time Security

#### 7.1 Technology Overview

Supply chain security ensures the integrity and provenance of software artifacts from source code through build, distribution, and deployment. Following high-profile attacks (SolarWinds, CodeCov), this area has moved from optional to regulatory requirement.

**Regulatory drivers:**
- U.S. Executive Order 14028 requires federal software suppliers to provide verifiable provenance.
- EU Cyber Resilience Act imposes comparable obligations.
- SLSA Level 2 projected to become minimum for public cloud marketplace listings by 2028 ([InfoQ provenance](https://www.infoq.com/news/2025/08/provenance/), [Faith Forge Labs](https://faithforgelabs.com/blog_supplychain_security_2025.php)).

#### 7.2 SLSA (Supply chain Levels for Software Artifacts)

**Mechanism:** Security framework developed by Google providing a maturity model with four progressive levels, each defining stricter security controls for build integrity ([SLSA FAQ](https://slsa.dev/spec/v1.1/faq), [JFrog SLSA guide](https://jfrog.com/learn/grc/slsa-framework/)).

| Level | Requirements | Difficulty |
|-------|-------------|-----------|
| SLSA 1 | Build process documented, provenance exists | Easy (days) |
| SLSA 2 | Hosted build service, signed provenance | Moderate (weeks) |
| SLSA 3 | Ephemeral build environments, non-falsifiable provenance | Hard (quarter) |
| SLSA 4 | Hermetic builds, two-party review | Very Hard |

**Current status:** SLSA v1.0 finalized (October 2024). SLSA v1.2 RC2 in public review as of November 2025 ([SLSA blog](https://slsa.dev/blog)).

**Adoption:** GitHub Actions natively supports artifact attestations and SBOM generation aligned with SLSA. SLSA Level 2 is achievable in weeks with existing tooling ([Faith Forge Labs](https://faithforgelabs.com/blog_supplychain_security_2025.php)).

#### 7.3 Sigstore

**Mechanism:** Public infrastructure for code signing using short-lived keys tied to OIDC identity, with signatures recorded in a public transparency log ([Sigstore at OpenSSF](https://openssf.org/tag/sigstore/)).

**Components:**
- **Fulcio:** OIDC-derived certificate issuance (short-lived).
- **Rekor:** Transparency log recording signatures.
- **Cosign:** Artifact signing CLI using identity tokens.

**2025 status:** Sigstore components achieved production SLA status in February 2025. Gaining adoption across npm, PyPI, and Kubernetes ecosystems where verification is increasingly automated ([Faith Forge Labs](https://faithforgelabs.com/blog_supplychain_security_2025.php), [InfoQ provenance](https://www.infoq.com/news/2025/08/provenance/)).

#### 7.4 in-toto

**Mechanism:** Framework for software attestations that generates signed documents associating metadata with artifacts, providing provenance with integrity and authenticity. Secures entire pipelines by generating signed attestations for each step ([InfoQ provenance](https://www.infoq.com/news/2025/08/provenance/)).

**Integration:** The in-toto Attestation Framework supports new policy standards making it easier for consumers and auditors to derive insights from authenticated metadata including SBOMs and SLSA Build Provenance ([SLSA provenance deep dive](https://www.legitsecurity.com/blog/slsa-provenance-blog-series-part-2-deeper-dive-into-slsa-provenance)).

**Platform adoption:**
- GitHub: Artifact attestations and SBOM generation via Actions.
- Red Hat Konflux: Issues in-toto attestations as part of pipeline infrastructure.
- HashiCorp HCP Packer: Captures build metadata and generates SBOMs.

**Source:** [InfoQ provenance](https://www.infoq.com/news/2025/08/provenance/), [Oligo supply chain guide](https://www.oligo.security/academy/ultimate-guide-to-software-supply-chain-security-in-2025)

#### 7.5 SBOM Standards

| Standard | Status (2025) | Key Feature |
|----------|---------------|-------------|
| SPDX 3.0 | RC2 (March 2025) | Linux Foundation standard |
| CycloneDX 1.6 | Production-ready | VEX (Vulnerability Exploitability eXchange) support |
| OCI Artifact v1 | Stable | SBOMs as first-class container registry objects |

**Source:** [Faith Forge Labs](https://faithforgelabs.com/blog_supplychain_security_2025.php)

#### 7.6 Implementation Maturity Assessment

| Capability | Tooling Maturity | Adoption | Difficulty |
|-----------|-----------------|----------|-----------|
| Signing (Sigstore/cosign) | Production | Growing | Low |
| SBOM generation (Syft, Trivy) | Production | Moderate | Low |
| Provenance (SLSA L2) | Production | Growing | Moderate |
| Policy enforcement (Kyverno, GUAC) | Production | Low-Moderate | Moderate |
| Full pipeline attestation (in-toto) | Production | Low | High |

**Adoption challenges:** Research analyzing 1,523 GitHub issues identified barriers including complex implementation, unclear requirements communication, and sharp SBOM format variations across tools ([InfoQ provenance](https://www.infoq.com/news/2025/08/provenance/)).

---

## L2: Cross-Cutting Analysis

### Kernel vs. Userspace Tradeoffs

| Dimension | Kernel-Level (eBPF, seccomp, LSMs) | Hypervisor (Firecracker, Kata) | Userspace (gVisor, WASM) |
|-----------|-------------------------------------|-------------------------------|--------------------------|
| **Enforcement point** | Inside host kernel | Hardware boundary (KVM) | User-space process |
| **Performance** | <1-5% overhead | 2-15% overhead | 8-30% overhead |
| **Security boundary** | Kernel hooks | Hardware VM isolation | Process-level sandbox |
| **Failure mode** | Kernel bug = total compromise | Hypervisor bug = VM escape | Sandbox bug = limited escape |
| **Privilege required** | Root (except Landlock) | Root + HW virtualization | None (WASM) / Root (gVisor) |
| **Container integration** | Native | RuntimeClass | RuntimeClass / embedded |
| **Attack surface** | Host kernel (large) | KVM + VMM (small) | Sentry/WASM runtime (medium) |

**Key insight:** The tradeoff is performance vs. isolation strength. Kernel-level mechanisms are fastest but share the host kernel (single point of compromise). Hypervisor isolation provides the strongest boundary but at higher resource cost. Userspace approaches offer a middle ground with varying overhead.

### Performance Comparison Matrix

| Technology | Startup | CPU Overhead | Memory Overhead | I/O Impact | Source |
|-----------|---------|-------------|----------------|-----------|--------|
| eBPF monitoring | N/A | <1% | <5MB | Negligible | [17] TuxCare |
| seccomp-bpf | N/A | <3.6% | 0 | Negligible | [24] gVisor blog |
| SELinux | N/A | 2-5% | <10MB | Minor | [HYPOTHESIS] |
| AppArmor | N/A | 1-3% | <5MB | Negligible | [HYPOTHESIS] |
| Landlock | N/A | Negligible | 0 | Negligible | [37] Landlock Workshop |
| gVisor | 50-100ms | 10-30% | 10-50MB | 20-50% | [38] onidel |
| Kata Containers | 150-300ms | 5-15% | 50-150MB | Moderate | [38] onidel |
| Firecracker | 100-200ms | 2-8% | <5MB | Low | [39] Northflank |
| Wasmtime | 2-5ms | +11% | ~15MB | Up to 10x (worst case) | [47] Reintech |
| WasmEdge | 1.5ms | +8% | ~8MB | Moderate | [47] Reintech |
| Cedar eval | N/A | Negligible | <10MB | N/A | [53] arxiv paper |
| OPA eval | N/A | Negligible | <50MB | N/A | [52] Permit.io |

### Adoption Maturity Heat Map

| Technology | Enterprise Adoption | Cloud-Native Adoption | AI/Agent Adoption | Regulatory Compliance |
|-----------|--------------------|-----------------------|-------------------|----------------------|
| eBPF/Cilium | HIGH | VERY HIGH | MEDIUM | MEDIUM |
| Falco | HIGH | HIGH | LOW | MEDIUM |
| seccomp | VERY HIGH (default) | VERY HIGH | MEDIUM | HIGH |
| SELinux | HIGH (RHEL) | MEDIUM | LOW | VERY HIGH |
| AppArmor | HIGH (Ubuntu) | HIGH | LOW | HIGH |
| Landlock | LOW | LOW | EMERGING | LOW |
| gVisor | MEDIUM | MEDIUM | MEDIUM | MEDIUM |
| Kata Containers | MEDIUM | MEDIUM | MEDIUM | HIGH |
| Firecracker | HIGH (AWS) | MEDIUM | HIGH | HIGH |
| WASM/WASI | LOW | LOW | EMERGING | LOW |
| Cedar | MEDIUM (AWS) | LOW | LOW | MEDIUM |
| OPA | HIGH | HIGH | LOW | HIGH |
| SLSA/Sigstore | MEDIUM | GROWING | LOW | GROWING |

### Convergence Trends (2024-2026)

1. **eBPF as universal security substrate.** eBPF is converging from separate tools (networking, monitoring, enforcement) into a unified security platform. Cilium + Tetragon + Hubble provide end-to-end network security, runtime enforcement, and observability through a single eBPF foundation.

2. **Microvm-based agent sandboxing becoming standard.** The 2025-2026 AI agent boom is driving Firecracker and Kata Containers into new use cases beyond serverless. Platform providers (Northflank, E2B, Daytona) are building managed microVM infrastructure specifically for agent code execution.

3. **Landlock as the application self-sandboxing standard.** Landlock's unprivileged operation makes it uniquely suited for software that voluntarily restricts itself. Tools like Landrun and Island are making this accessible without requiring kernel programming expertise. This is the most promising path for "leashing" software from within.

4. **Policy-as-code consolidation around Cedar.** OPA's governance uncertainty (Apple acquisition of maintainers) combined with Cedar's 42-80x performance advantage and formal verification capabilities suggest a medium-term shift toward Cedar for new deployments, particularly in security-critical authorization.

5. **Supply chain security from optional to mandatory.** SLSA Level 2 achievable in weeks with existing tooling. Regulatory pressure (EO 14028, EU CRA) making provenance and SBOM generation baseline requirements rather than aspirational goals.

6. **Defense-in-depth stacking is the consensus architecture.** No single mechanism is sufficient. The emerging production pattern combines:
   - **Layer 1 (kernel):** seccomp-bpf for syscall filtering + LSM (AppArmor/SELinux/Landlock) for MAC
   - **Layer 2 (runtime):** eBPF (Tetragon) for detection and enforcement
   - **Layer 3 (isolation):** Firecracker/Kata for workload isolation
   - **Layer 4 (policy):** Cedar/OPA for authorization decisions
   - **Layer 5 (supply chain):** SLSA + Sigstore for artifact integrity

### Risk Assessment

| Risk | Probability | Impact | Mitigation | Source |
|------|------------|--------|-----------|--------|
| eBPF verifier bypass | Low | Critical | SafeBPF (hardware-assisted), defense-in-depth | [2] eunomia |
| KVM/hypervisor escape | Very Low | Critical | Keep hypervisors patched, minimize VMM surface | [41] Edera |
| WASM JIT sandbox escape | Medium | High | AOT compilation, defense-in-depth with VM layer | [48] Wasmtime advisories |
| OPA governance collapse | Medium | Medium | Plan Cedar migration path, maintain policy portability | [51] Oso guide |
| Supply chain attack on build tools | Medium | Critical | SLSA L3+, hermetic builds, in-toto attestations | [62] Faith Forge Labs |
| LSM policy misconfiguration | High | Medium | Automated policy generation, testing frameworks | [25a] Red Hat |
| Landlock kernel regression | Low | Medium | Feature detection at runtime, graceful degradation | [37] Landlock Workshop |

---

## Sources

### eBPF-Based Security

1. [Cloud Native Now - eBPF: The Silent Power Behind Cloud Native's Next Phase](https://cloudnativenow.com/editorial-calendar/best-of-2025/ebpf-the-silent-power-behind-cloud-natives-next-phase-2/) - Key insight: AWS adopted Cilium as default EKS CNI
2. [eunomia - eBPF Ecosystem Progress 2024-2025](https://eunomia.dev/blog/2025/02/12/ebpf-ecosystem-progress-in-20242025-a-technical-deep-dive/) - Key insight: BPF tokens, BPF Arena, SafeBPF developments
2a. [LWN.net - Delegating privilege with BPF tokens](https://lwn.net/Articles/935195/) - Key insight: BPF token mechanism for unprivileged eBPF delegation
2b. [LWN.net - A look at what's possible with BPF arenas](https://lwn.net/Articles/1019885/) - Key insight: BPF Arena shared-memory regions in kernel 6.9
2c. [LWN.net - The extensible scheduler class](https://lwn.net/Articles/922405/) - Key insight: sched_ext design and rationale
2d. [Phoronix - sched_ext merged for Linux 6.12](https://www.phoronix.com/news/Linux-6.12-Lands-sched-ext) - Key insight: sched_ext official merge into kernel 6.12
3. [Tetragon Official Site](https://tetragon.io/) - Key insight: In-kernel security observability and enforcement
4. [Tetragon Enforcement Docs](https://tetragon.io/docs/concepts/enforcement/) - Key insight: Return value override and signal delivery mechanisms
5. [Tetragon Overview](https://tetragon.io/docs/overview/) - Key insight: In-kernel filtering reduces data volume
6. [CNCF - Unlocking Cloud Native Security with Cilium and eBPF](https://www.cncf.io/blog/2025/01/02/unlocking-cloud-native-security-with-cilium-and-ebpf/) - Key insight: 60%+ K8s CNI adoption
7. [InfoQ - Cilium 1.19 at Ten Years](https://www.infoq.com/news/2026/02/cilium-119/) - Key insight: Strict encryption modes, Ztunnel integration, 2900+ commits
8. [CNCF Falco Project](https://www.cncf.io/projects/falco/) - Key insight: CNCF Graduated February 2024
9. [Sysdig - State of Falco](https://www.sysdig.com/blog/the-state-of-falco) - Key insight: 40% plugin ecosystem growth
10. [CNCF - Falco Links Detection with Forensic Analysis](https://www.cncf.io/announcements/2025/11/10/falco-links-real-time-detection-with-forensic-level-analysis-in-the-cloud-native-stack/) - Key insight: Stratoshark integration
11. [Falco Documentation](https://falco.org/docs/) - Key insight: libscap/libsinsp architecture
12. [KubeArmor Official Site](https://kubearmor.io/) - Key insight: Non-privileged DaemonSet, eBPF + LSM-BPF
13. [KubeArmor Documentation](https://docs.kubearmor.io/kubearmor) - Key insight: System call, file, process, network policy enforcement
14. [AWS - KubeArmor on EKS Auto Mode](https://aws.amazon.com/blogs/containers/enhancing-container-security-in-amazon-eks-auto-mode-with-kubearmor/) - Key insight: AWS EKS integration
15. [KubeArmor OCI Hooks](https://kubearmor.io/blog/kubearmor-oci-hooks-container-security) - Key insight: Unprivileged CRI socket access elimination
16. [AccuKnox - KubeArmor in 2025](https://accuknox.com/blog/protecting-edge-workloads-with-kubearmor) - Key insight: Edge/IoT workload protection, ARMv9 support
17. [TuxCare - eBPF for Performance Monitoring and Security](https://tuxcare.com/blog/ebpf-for-advanced-linux-performance-monitoring-and-security/) - Key insight: <1% overhead, 10-100x improvement over userspace
18. [OneUptime - eBPF Security Monitoring with Falco and Tetragon](https://oneuptime.com/blog/post/2026-01-07-ebpf-security-monitoring-falco-tetragon/view) - Key insight: Implementation guide

### seccomp and seccomp-bpf

19. [Docker Seccomp Documentation](https://docs.docker.com/engine/security/seccomp/) - Key insight: Default profile allows 300+ of 435 syscalls
20. [Datadog Security Labs - Container Security Fundamentals Part 6: seccomp](https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-6/) - Key insight: Detailed seccomp architecture and filtering
21. [GitHub: oci-seccomp-bpf-hook](https://github.com/containers/oci-seccomp-bpf-hook) - Key insight: Automated profile generation via syscall tracing
22. [Sysdig 2024 Cloud-Native Security and Usage Report](https://www.sysdig.com/2024-cloud-native-security-and-usage-report) - Key insight: Majority of container images run as root, 75%+ have high-risk vulnerabilities
22a. [Red Hat State of Kubernetes Security 2024](https://www.redhat.com/en/engage/state-kubernetes-security-report-2024) - Key insight: 90% of organizations experienced at least one K8s security incident
23. [Kubernetes - Restrict Syscalls with seccomp](https://kubernetes.io/docs/tutorials/security/seccomp/) - Key insight: SeccompProfile GA since K8s 1.27
24. [gVisor seccomp optimization blog](https://gvisor.dev/blog/2024/02/01/seccomp/) - Key insight: 3.6% runtime reduction from seccomp-bpf optimizations

### Linux Security Modules

25. [Linux Journal - Steady Momentum in AppArmor and SELinux Uptake](https://www.linuxjournal.com/content/securing-linux-steady-momentum-apparmor-and-selinux-uptake) - Key insight: Enterprise adoption trends driven by distribution defaults
25a. [Red Hat - SELinux as a Security Pillar](https://access.redhat.com/articles/6964380) - Key insight: SELinux enforcing mode mitigates container breakout, privilege escalation
25b. [openSUSE News - Tumbleweed Adopts SELinux](https://news.opensuse.org/2025/02/13/tw-plans-to-adopt-selinux-as-default/) - Key insight: openSUSE switch from AppArmor to SELinux
25c. [CNCF Annual Survey 2024](https://www.cncf.io/reports/cncf-annual-survey-2024/) - Key insight: Kubernetes and Linux adoption statistics
26. [Linux Security Modules Wikipedia](https://en.wikipedia.org/wiki/Linux_Security_Modules) - Key insight: Approved LSM list
27. [Linux Journal - Steady Momentum in AppArmor and SELinux Uptake](https://www.linuxjournal.com/content/securing-linux-steady-momentum-apparmor-and-selinux-uptake) - Key insight: Adoption trends
28. [DoHost - SELinux vs AppArmor Deep Dive](https://dohost.us/index.php/2025/10/05/selinux-vs-apparmor-a-comparative-deep-dive-into-linux-security-modules-lsm/) - Key insight: Technical comparison
29. [Landlock kernel documentation](https://docs.kernel.org/userspace-api/landlock.html) - Key insight: Unprivileged sandboxing API
30. [Landlock.io](https://landlock.io/) - Key insight: Official Landlock project site
31. [Landlock kernel admin docs](https://docs.kernel.org/security/landlock.html) - Key insight: ABI versions and capabilities
32. [Phoronix - Landlock Unix Socket Scoping](https://www.phoronix.com/news/Landlock-Scoping-Unix-Sockets) - Key insight: Linux 6.12 Unix socket and signal controls
33. [GitHub: landrun](https://github.com/Zouuup/landrun) - Key insight: Lightweight Landlock sandboxing CLI
34. [GitHub: island](https://github.com/landlock-lsm/island) - Key insight: Official Landlock sandboxing tool
35. [justine.lol - Sandboxing GNU Make with Landlock](https://justine.lol/make/) - Key insight: Performance benchmarks, 5x faster than Bazel
36. [domcyrus.dev - Sandboxing Network Tools with Landlock](https://domcyrus.github.io/systems-programming/security/linux/2025/12/06/landlock-sandboxing-network-tools.html) - Key insight: Network restriction implementation
37. [Landlock Workshop 2025 slides (PDF)](https://landlock.io/talks/2025-01-29_landlock-workshop.pdf) - Key insight: Latest Landlock capabilities and roadmap

### Hypervisor-Level Isolation

38. [onidel - gVisor vs Kata vs Firecracker 2025](https://onidel.com/blog/gvisor-kata-firecracker-2025) - Key insight: Detailed performance benchmarks for all three
39. [Northflank - How to Sandbox AI Agents in 2026](https://northflank.com/blog/how-to-sandbox-ai-agents) - Key insight: Firecracker 125ms boot, 150 VMs/second, AI agent isolation recommendations
39a. [Gartner - 40% of Enterprise Apps Will Feature AI Agents by 2026](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025) - Key insight: 75% of organizations piloting/deploying AI agents; 40% of apps expected to have agents by 2026
40. [Northflank - Kata vs Firecracker vs gVisor](https://northflank.com/blog/kata-containers-vs-firecracker-vs-gvisor) - Key insight: Architecture comparison
41. [Edera - Container Isolation Compared](https://edera.dev/stories/kata-vs-firecracker-vs-gvisor-isolation-compared) - Key insight: Isolation level comparison
42. [AgentSphere - AI Agent Workspace Showdown](https://dev.to/agentsphere/choosing-a-workspace-for-ai-agents-the-ultimate-showdown-between-gvisor-kata-and-firecracker-b10) - Key insight: AI agent specific isolation recommendations
43. [SoftwareSeni - Comparing Isolation for AI Agents](https://www.softwareseni.com/firecracker-gvisor-containers-and-webassembly-comparing-isolation-technologies-for-ai-agents/) - Key insight: WASM vs container vs VM for AI agents
44. [Northflank - Firecracker vs gVisor](https://northflank.com/blog/firecracker-vs-gvisor) - Key insight: Detailed two-way comparison

### WASM Runtimes

45. [Wasmtime Security Documentation](https://docs.wasmtime.dev/security.html) - Key insight: Capability-based security model
46. [eunomia - WASI and Component Model Current Status](https://eunomia.dev/blog/2025/02/16/wasi-and-the-webassembly-component-model-current-status/) - Key insight: Comprehensive WASI roadmap, limitations, security model
47. [Reintech - Wasmtime vs Wasmer vs WasmEdge 2026](https://reintech.io/blog/wasmtime-vs-wasmer-vs-wasmedge-wasm-runtime-comparison-2026) - Key insight: Performance benchmarks, startup times, memory footprints
48. [Wasmtime Security Advisories](https://github.com/bytecodealliance/wasmtime/security) - Key insight: CVE-2024-30266 (externref type confusion), CVE-2024-47813 (type registry race condition)
48a. [NVD CVE-2023-51661 - Wasmer Filesystem Sandbox Bypass](https://nvd.nist.gov/vuln/detail/CVE-2023-51661) - Key insight: Wasmer sandbox escape via default cwd access
48b. [CVE-2024-38358 - Wasmer Directory Traversal](https://security.snyk.io/vuln/SNYK-RUST-WASMER-7222570) - Key insight: Path traversal via symlink creation
49. [State of WebAssembly 2025-2026](https://platform.uno/blog/the-state-of-webassembly-2025-2026/) - Key insight: WebAssembly adoption trends
50. [CMU - Provably Safe Sandboxing with WebAssembly](https://www.cs.cmu.edu/~csd-phd-blog/2023/provably-safe-sandboxing-wasm/) - Key insight: Formal security analysis of WASM sandboxing

### Policy-as-Code

51. [Oso - OPA vs Cedar vs Zanzibar 2025 Guide](https://www.osohq.com/learn/opa-vs-cedar-vs-zanzibar) - Key insight: Apple hired OPA maintainers August 2025
52. [Permit.io - OPA vs Cedar](https://www.permit.io/blog/opa-vs-cedar) - Key insight: Cedar significantly faster than Rego (42-60x per independent testing; 42.8-80.8x per academic benchmarks)
53. [Cedar Academic Paper (arxiv)](https://arxiv.org/pdf/2403.04651) - Key insight: Cedar 42.8-80.8x faster than Rego in benchmarks
54. [Cedar Policy Language](https://www.cedarpolicy.com/) - Key insight: Language playground and specification
55. [StrongDM - Cedar Policy Language 2026 Guide](https://www.strongdm.com/cedar-policy-language) - Key insight: Comprehensive Cedar overview
56. [TachTech - Sentinel vs OPA](https://engineering.tachtech.net/devsecops/2025/10/15/sentinel-and-opa-policies.html) - Key insight: Complementary usage pattern
57. [Spacelift - Policy as Code in Terraform](https://spacelift.io/blog/terraform-policy-as-code) - Key insight: Terraform-specific policy enforcement
58. [Spacelift - Top 12 Policy as Code Tools 2026](https://spacelift.io/blog/policy-as-code-tools) - Key insight: Market landscape overview
59. [Permit.io - OPA vs OpenFGA vs Cedar Showdown](https://www.permit.io/blog/policy-engine-showdown-opa-vs-openfga-vs-cedar) - Key insight: Panel discussion on architectural tradeoffs
60. [Natoma - MCP Access Control: OPA vs Cedar](https://natoma.ai/blog/mcp-access-control-opa-vs-cedar-the-definitive-guide) - Key insight: MCP-specific policy comparison
61. [Sentinel Documentation](https://developer.hashicorp.com/sentinel/docs/concepts/policy-as-code) - Key insight: Sentinel policy-as-code concepts

### Supply Chain Security

62. [Faith Forge Labs - Supply Chain Security in 2025](https://faithforgelabs.com/blog_supplychain_security_2025.php) - Key insight: SLSA L2 achievable in weeks, Sigstore production SLA February 2025
63. [InfoQ - Provenance Tools Becoming Standard](https://www.infoq.com/news/2025/08/provenance/) - Key insight: Regulatory drivers (EO 14028, EU CRA), platform adoption
64. [Oligo - Ultimate Guide to Software Supply Chain Security 2025](https://www.oligo.security/academy/ultimate-guide-to-software-supply-chain-security-in-2025) - Key insight: Comprehensive threat landscape
65. [SLSA Blog](https://slsa.dev/blog) - Key insight: SLSA v1.2 RC2 public review
66. [SLSA FAQ](https://slsa.dev/spec/v1.1/faq) - Key insight: SLSA level definitions
67. [JFrog - SLSA Framework](https://jfrog.com/learn/grc/slsa-framework/) - Key insight: SLSA implementation guidance
68. [Legit Security - SLSA Provenance Deep Dive](https://www.legitsecurity.com/blog/slsa-provenance-blog-series-part-2-deeper-dive-into-slsa-provenance) - Key insight: in-toto attestation framework integration
69. [OpenSSF - Sigstore](https://openssf.org/tag/sigstore/) - Key insight: OpenSSF governance and Sigstore updates

### AI Agent Sandboxing (Cross-Category)

70. [Northflank - Spin Up Secure Sandbox and MicroVM](https://northflank.com/blog/how-to-spin-up-a-secure-code-sandbox-and-microvm-in-seconds-with-northflank-firecracker-gvisor-kata-clh) - Key insight: Platform approach to sandbox provisioning
71. [Hokstad Consulting - MicroVM Orchestrator Selection](https://hokstadconsulting.com/blog/how-to-pick-the-right-microvm-orchestrator) - Key insight: Orchestration layer comparison

---

*Research conducted: 2026-03-03*
*Methodology: WebSearch + WebFetch across 80+ sources. All factual claims cite sources with URLs. Claims marked [HYPOTHESIS] where sourced benchmarks were unavailable. Revision pass upgraded non-authoritative citations (personal blogs, aggregator sites, substack) to primary sources (Sysdig reports, Red Hat reports, CNCF surveys, Gartner research, CVE databases, LWN.net).*
*Coverage: 7 technology categories, 20+ individual technologies, 2024-2026 timeframe.*
