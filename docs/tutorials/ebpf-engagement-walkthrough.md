# Learn eBPF Transparent Proxying by Running a Full Engagement Stack

> By the end of this tutorial, you will have started an Envoy+BPF engagement stack, verified that all three BPF programs are attached, routed live traffic through Envoy via BPF redirect, confirmed scope enforcement blocked an unauthorized connection, inspected Envoy access logs, and torn down the stack with clean BPF removal.

## Document Sections

| Section | Purpose |
|---------|---------|
| [What You Will Achieve](#what-you-will-achieve) | The concrete end state you are building toward |
| [Prerequisites](#prerequisites) | What you need before starting |
| [Step 1: Start the engagement stack](#1-start-the-engagement-stack) | Bring up Envoy, tool container, and targets |
| [Step 2: Verify BPF programs are loaded](#2-verify-bpf-programs-are-loaded) | Confirm all three programs are pinned to bpffs |
| [Step 3: Verify BPF programs are attached to the container cgroup](#3-verify-bpf-programs-are-attached-to-the-container-cgroup) | Check the cgroup attachment |
| [Step 4: Inspect the BPF maps before any traffic](#4-inspect-the-bpf-maps-before-any-traffic) | Confirm the maps start empty |
| [Step 5: Make an HTTP request through Envoy](#5-make-an-http-request-through-envoy) | Route a request via BPF redirect and watch the map fill |
| [Step 6: Confirm Envoy logged the request](#6-confirm-envoy-logged-the-request) | Read the Envoy access log |
| [Step 7: Make a raw TCP connection through the BPF chain](#7-make-a-raw-tcp-connection-through-the-bpf-chain) | Send non-HTTP TCP through BPF intercept |
| [Step 8: Test scope enforcement](#8-test-scope-enforcement) | Watch Envoy deny an out-of-scope connection |
| [Step 9: Verify SO_MARK loop prevention](#9-verify-so_mark-loop-prevention) | Confirm Envoy's own upstream traffic is not re-intercepted |
| [Step 10: Tear down and verify BPF cleanup](#10-tear-down-and-verify-bpf-cleanup) | Stop everything and confirm maps are gone |
| [What You Learned](#what-you-learned) | Summary of the skills you built |
| [What Next](#what-next) | Where to go from here |

---

## What You Will Achieve

By the end of this tutorial, you will have:

1. Started the Envoy+BPF engagement stack with all services healthy.
2. Verified that all three BPF programs (`connect4`, `sockops`, `getsockopt`) are pinned to bpffs and attached to the tool container's cgroup.
3. Made an HTTP request routed transparently through Envoy via BPF redirect — without setting `HTTP_PROXY` in the shell.
4. Made a raw TCP connection through the same BPF chain to a TCP echo target.
5. Confirmed that Envoy's deny-by-default rule blocked a connection to an unauthorized host.
6. Read Envoy's JSON access log to trace the routing decision.
7. Torn down the stack and confirmed the BPF pins were removed.

---

## Prerequisites

Before starting, you need:

- **Docker Desktop** running on macOS or Linux with BPF support. On macOS, Docker Desktop uses a LinuxKit VM that includes BPF cgroup support. On Linux, you need kernel 5.7 or later with `CONFIG_CGROUP_BPF=y`.
- **The Jerry framework cloned** to your machine with `uv sync` completed. The eBPF PoC directory (`src/proxy_infra/ebpf_poc/`) must be present.
- **Docker Compose** v2.x (ships with Docker Desktop). Run `docker compose version` to confirm.
- **Basic familiarity with Docker Compose** — you know what `up`, `exec`, and `down` mean.
- **`bpftool`** is not required on your host. All `bpftool` commands in this tutorial run inside the `hybrid-tool` container, which ships with it.

> **Note on LinuxKit:** Docker Desktop on macOS routes containers through a LinuxKit VM. BPF cgroup programs attach to the VM's kernel, not the macOS kernel. The tutorial steps work identically — Docker Compose abstracts this.

---

## 1. Start the engagement stack

Change to the eBPF PoC directory and start the Envoy+BPF integration stack.

```bash
cd src/proxy_infra/ebpf_poc
docker compose -f docker-compose.envoy-integration.yml up -d --wait
```

Docker Compose will build the `hybrid-tool` container image on first run (this takes about two minutes — it compiles the three BPF programs with Clang). Subsequent starts reuse the cached image.

**Expected result:** All five services start and the `--wait` flag returns only after the `envoy` healthcheck passes. You should see output like:

```
[+] Running 5/5
 ✔ Container ebpf-envoy-integration-proxy-node-1   Started
 ✔ Container ebpf-envoy-integration-envoy-1        Healthy
 ✔ Container ebpf-envoy-integration-http-target-1  Started
 ✔ Container ebpf-envoy-integration-tcp-target-1   Started
 ✔ Container ebpf-envoy-integration-hybrid-tool-1  Started
```

If the build fails at the Clang compile step, confirm Docker Desktop has internet access to pull `ubuntu:24.04`.

---

## 2. Verify BPF programs are loaded

List the BPF programs pinned to the bpffs filesystem inside the tool container. [UNTESTED: bpftool output format may vary by kernel version]

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool bpftool prog list
```

**Expected result:** You should see at least three entries with types `cgroup_sock_addr` (connect4), `cgroup_sockopt` (getsockopt), and `cgroup_sock_ops` (sockops). The program names `connect4_redirect`, `sockops_port_cookie`, and `getsockopt_orig_dst` appear in the output. For example:

```
12: cgroup_sock_addr  name connect4_redirect  tag ...
13: cgroup_sock_ops   name sockops_port_cookie  tag ...
14: cgroup_sockopt    name getsockopt_orig_dst  tag ...
```

The exact IDs differ between runs. What matters is that all three program types appear.

---

## 3. Verify BPF programs are attached to the container cgroup

Confirm all three programs are attached to the container's cgroup directory. [UNTESTED: cgroup path structure depends on Docker and kernel version]

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool sh -c \
  'bpftool cgroup show $(find /sys/fs/cgroup/docker -maxdepth 1 -name "$(hostname)*" -type d | head -1)'
```

**Expected result:** Three lines appear, one per attach type. You should see `connect4`, `sock_ops`, and `getsockopt` listed:

```
ID       AttachType      AttachFlags     Name
12       connect4                        connect4_redirect
13       sock_ops                        sockops_port_cookie
14       getsockopt                      getsockopt_orig_dst
```

The `jerry-intercept` child cgroup is the one the `intercept` wrapper uses. Run this to see it:

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool sh -c \
  'bpftool cgroup show $(find /sys/fs/cgroup/docker -maxdepth 1 -name "$(hostname)*" -type d | head -1)/jerry-intercept'
```

**Expected result:** The same three programs appear, because child cgroups inherit their parent's attached BPF programs.

---

## 4. Inspect the BPF maps before any traffic

Look at the `dst_lookup` map — it stores original destinations that `connect4` intercepts. At this point, no traffic has been sent, so the map is empty.

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool bpftool map dump pinned /sys/fs/bpf/rainbow_maps/dst_lookup
```

**Expected result:** The command prints `Found 0 elements` or returns with no output. This confirms BPF is loaded and the map exists, but no connections have been intercepted yet.

---

## 5. Make an HTTP request through Envoy

Send an HTTP request to `http-target` (172.31.1.20) from inside the tool container. The tool container cannot reach this host directly — it is on the `hybrid-egress` network, which the tool container does not have a direct route to. The BPF `connect4` program intercepts the `connect()` call and rewrites the destination to `127.0.0.1:15001` (Envoy's transparent TCP listener). Envoy then forwards to the real destination.

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool curl -v http://172.31.1.20/
```

**Expected result:** The nginx welcome page HTML appears in the terminal output. You should see `HTTP/1.1 200 OK` in the response headers:

```
< HTTP/1.1 200 OK
< Server: nginx/1.27.x
...
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
```

Now check the `dst_lookup` map again. The entry that `connect4` wrote before rewriting the destination should now be there.

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool bpftool map dump pinned /sys/fs/bpf/rainbow_maps/dst_lookup
```

**Expected result:** At least one entry appears. The `dst_ip` field holds the original destination IP (`172.31.1.20` encoded as a 32-bit integer) and `dst_port` holds port 80. You should see something like:

```
key: ...  value: {"dst_ip":335676844,"dst_port":5120}
Found 1 element
```

The integer values are raw kernel byte-order representations of the IP and port.

---

## 6. Confirm Envoy logged the request

Read Envoy's JSON access log to verify that Envoy handled the request — not a direct connection.

```bash
docker compose -f docker-compose.envoy-integration.yml logs envoy | tail -5
```

**Expected result:** A JSON log line appears for the request. The `authority` field shows `172.31.1.20`, `response_code` is `200`, and `upstream_cluster` is `original_dst_cluster`. For example:

```json
{"ts":"2026-...","method":"GET","authority":"172.31.1.20","path":"/",
 "upstream":"172.31.1.20:80","upstream_cluster":"original_dst_cluster",
 "response_code":200,"zone":"hybrid-integration-test","verdict":"via_upstream"}
```

This confirms the request traveled through BPF interception to Envoy, and Envoy forwarded it to the target — not a direct tool-to-target connection.

---

## 7. Make a raw TCP connection through the BPF chain

Use the `intercept` wrapper to run a Python TCP client inside the `jerry-intercept` cgroup. The BPF `connect4` program intercepts the `connect()` call, rewrites the destination to Envoy:15001, and the `sockops` program records the port-to-cookie mapping so that `getsockopt` can tell Envoy the original destination. Envoy resolves where to forward the TCP stream using `SO_ORIGINAL_DST`. [UNTESTED: requires the tcp-target socat echo server to be running]

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool \
  intercept python3 -c "
import socket
s = socket.socket()
s.settimeout(5)
s.connect(('172.31.1.30', 4444))
s.sendall(b'hello\n')
print(s.recv(1024).decode().strip())
s.close()
"
```

**Expected result:** The TCP echo target responds and you see:

```
TCP_ECHO_OK
```

Now check the `port_cookie` map to confirm `sockops` recorded the connection:

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool bpftool map dump pinned /sys/fs/bpf/rainbow_maps/port_cookie
```

**Expected result:** At least one entry appears in the `port_cookie` map. Each entry maps an ephemeral source port number (key) to a socket cookie (value). These entries were written by the `sockops` program at TCP handshake completion, so that `getsockopt` could chain source_port to cookie to original destination for Envoy's `SO_ORIGINAL_DST` call.

---

## 8. Test scope enforcement

Try to connect to an IP address that is not in the Envoy allowlist. The BPF `connect4` program still intercepts the `connect()` and rewrites it to Envoy:15001. Envoy then applies its scope rules — `192.0.2.1` is not in the `http_target_allowed` virtual host, so the `deny_all` catch-all fires. [UNTESTED: 192.0.2.1 is a documentation-reserved address that should not be routable]

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool \
  intercept sh -c 'nc -w 3 192.0.2.1 80; echo "exit code: $?"'
```

**Expected result:** The connection is refused by Envoy's `deny_all_tcp` cluster, which has no endpoints. The netcat command exits with a non-zero exit code within three seconds. The terminal shows:

```
exit code: 1
```

Check the Envoy log to see the deny verdict:

```bash
docker compose -f docker-compose.envoy-integration.yml logs envoy | grep deny | tail -3
```

**Expected result:** A log entry appears showing the `deny_all_tcp` cluster handled the connection, confirming Envoy enforced scope — not a firewall drop:

```json
{"upstream_cluster":"deny_all_tcp","response_code":0,"verdict":"no_healthy_upstream"}
```

---

## 9. Verify SO_MARK loop prevention

The `connect4` BPF program has a skip rule: if the socket carries `SO_MARK == 100`, `connect4` returns `1` (passthrough) without rewriting the destination. Envoy sets `SO_MARK=100` on every upstream socket it opens, using the `original_dst_cluster` socket option in its configuration. This prevents Envoy's own outbound connections from being re-intercepted by BPF and causing a redirect loop.

Check the `dst_lookup` map and verify it contains no entries with Envoy's internal address (`127.0.0.1`) as the original destination — because Envoy's upstream traffic is never intercepted.

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec hybrid-tool bpftool map dump pinned /sys/fs/bpf/rainbow_maps/dst_lookup
```

**Expected result:** The map contains entries from Steps 5 and 7. All `dst_ip` values represent the tool's original target IPs (`172.31.1.20` and `172.31.1.30`). No entry has `dst_ip` corresponding to `127.0.0.1` (which would be `16777343` in little-endian uint32). Envoy's connections to upstream targets are absent from the map, proving `SO_MARK=100` is working.

You can confirm the SO_MARK is set on Envoy's upstream sockets by inspecting the Envoy configuration file that was mounted into the container:

```bash
docker compose -f docker-compose.envoy-integration.yml \
  exec envoy grep -A5 "SO_MARK" /etc/envoy/envoy.yaml
```

**Expected result:** The configuration block shows `int_value: 100` under the `socket_options` section of the `original_dst_cluster`:

```yaml
socket_options:
- description: 'SO_MARK for BPF loop prevention (C2: must be 100)'
  level: 1
  name: 36
  int_value: 100
  state: STATE_PREBIND
```

---

## 10. Tear down and verify BPF cleanup

Stop and remove all containers. The `hybrid-tool` container's process exit causes the bpffs pins to be cleaned up by the OS once no process holds a reference to the program file descriptors.

```bash
docker compose -f docker-compose.envoy-integration.yml down
```

**Expected result:** All five containers stop and are removed:

```
[+] Running 6/6
 ✔ Container ebpf-envoy-integration-hybrid-tool-1  Removed
 ✔ Container ebpf-envoy-integration-envoy-1        Removed
 ✔ Container ebpf-envoy-integration-http-target-1  Removed
 ✔ Container ebpf-envoy-integration-tcp-target-1   Removed
 ✔ Container ebpf-envoy-integration-proxy-node-1   Removed
 ✔ Network ebpf-envoy-integration_hybrid-internal  Removed
```

Confirm the BPF pin files are gone from bpffs on your host. Run this on your host machine (not inside a container):

```bash
ls /sys/fs/bpf/rainbow_maps/ 2>/dev/null && echo "pins still present" || echo "pins removed"
```

**Expected result:** You see `pins removed`. The bpffs directory no longer exists, confirming the BPF programs were unloaded when the container exited. If you see `pins still present`, run `sudo rm -rf /sys/fs/bpf/rainbow_maps /sys/fs/bpf/rainbow_connect4 /sys/fs/bpf/rainbow_sockops /sys/fs/bpf/rainbow_getsockopt` to clean up manually.

> **macOS note:** On macOS, `/sys/fs/bpf/` lives inside the LinuxKit VM, not on your macOS filesystem. You cannot check it directly from the macOS Terminal. The absence of a running container is sufficient confirmation that the BPF programs are gone.

---

## What You Learned

You now know how to:

- Start the Envoy+BPF engagement stack using `docker compose -f docker-compose.envoy-integration.yml up -d --wait`.
- Verify all three BPF programs are loaded by running `bpftool prog list` inside the tool container.
- Confirm cgroup attachment by running `bpftool cgroup show` on the container's cgroup path.
- Observe BPF interception in action by reading the `dst_lookup` and `port_cookie` maps with `bpftool map dump`.
- Send HTTP and raw TCP traffic through the BPF chain and confirm Envoy handled the routing.
- Confirm Envoy's scope enforcement blocks unauthorized targets via the `deny_all_tcp` cluster.
- Verify that Envoy's upstream connections carry `SO_MARK=100` and are not re-intercepted by BPF.
- Stop the engagement stack and confirm BPF pins are cleaned up with `docker compose down`.

---

## What Next

You have walked through the full engagement lifecycle once. Here is where to go deeper:

- **Reference — eBPF Transparent Proxy:** [`docs/reference/ebpf-transparent-proxy.md`](../reference/ebpf-transparent-proxy.md) — Full specification of the three BPF program contracts, map schemas (`dst_lookup`, `port_cookie`), `BpfManager` API, and the `SO_MARK=100` loop prevention constraint.
- **How-To Guide — Add BPF to a Tool Container:** [`docs/playbooks/ebpf-tool-container.md`](../playbooks/ebpf-tool-container.md) — How to configure BPF transparent proxying for your own tool container in a real engagement.
- **Explanation — The eBPF Architecture Decision:** [`docs/research/ebpf-architecture-decision.md`](../research/ebpf-architecture-decision.md) — Why the three-program design (connect4 + sockops + getsockopt) was chosen over the earlier bridge+SOCKS5 approach, and what trade-offs it makes.
