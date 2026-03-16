# Runtime Interception Protocol

> Zone classification and escalation rules for mitmproxy and Frida operations. Authoritative dual-zone boundary specification for the /rainbow-runtime sub-skill.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | Why this protocol exists |
| [Zone Classification Matrix](#zone-classification-matrix) | Exhaustive operation-to-zone mapping |
| [mitmproxy Classification](#mitmproxy-classification) | mitmproxy-specific zone rules |
| [Frida Classification](#frida-classification) | Frida-specific zone rules |
| [Script Content Analysis](#script-content-analysis) | How to classify scripts before execution |
| [Escalation Procedure](#escalation-procedure) | Zone 2 to Zone 3 escalation flow |
| [Fail-Closed Default](#fail-closed-default) | Unrecognized operations default to Zone 3 |
| [Traceability](#traceability) | ADR and design source references |

---

## Purpose

The runtime interception protocol defines the Zone 2/Zone 3 boundary for mitmproxy and Frida operations. This is the dual-zone classification authority for `/rainbow-runtime`. The protocol operates on the principle that **passive observation is Zone 2** and **active modification is Zone 3**. Any operation that changes target system state requires per-operation human approval (P-020) per zone-3-exploit.md.

This classification is based on the specific CLI flags, script content, and API calls -- not on agent judgment.

---

## Zone Classification Matrix

### mitmproxy Operations

| Operation | CLI Pattern | Zone | Rationale |
|-----------|------------|------|-----------|
| Regular proxy capture | `mitmproxy --listen-port <port>` | Zone 2 | Passive traffic observation |
| Transparent proxy capture | `mitmproxy --mode transparent --showhost` | Zone 2 | Passive traffic observation |
| Reverse proxy capture | `mitmproxy --mode reverse:<spec>` | Zone 2 | Passive traffic observation |
| Local process capture | `mitmproxy --mode local:<process>` | Zone 2 | Passive traffic observation |
| SOCKS5 proxy capture | `mitmproxy --mode socks5` | Zone 2 | Passive traffic observation |
| WireGuard proxy capture | `mitmproxy --mode wireguard` | Zone 2 | Passive traffic observation |
| Non-interactive capture | `mitmdump -w <file>` | Zone 2 | Passive traffic capture to file |
| Flow replay (read-only) | `mitmdump -n -r <file>` | Zone 2 | Read-only analysis of captured flows |
| Flow filtering | `mitmdump -n -r <file> "<filter>"` | Zone 2 | Read-only filtered analysis |
| Web interface capture | `mitmweb --listen-port <port>` | Zone 2 | Passive traffic observation via web UI |
| Script: logging only | `mitmproxy -s log-script.py` | Zone 2 | Script only logs, does not modify traffic |
| Script: response modification | `mitmproxy -s modify-script.py` | **Zone 3** | Script modifies request/response content |
| Script: header injection | `mitmdump -s inject-headers.py` | **Zone 3** | Script modifies HTTP headers |
| Script: body replacement | `mitmdump -s replace-body.py` | **Zone 3** | Script modifies HTTP body content |
| Script: status code modification | `mitmdump -s change-status.py` | **Zone 3** | Script modifies HTTP status codes |

### Frida Operations

| Operation | CLI Pattern | Zone | Rationale |
|-----------|------------|------|-----------|
| Process listing | `frida-ps` / `frida-ps -U` / `frida-ps -R` | Zone 2 | Read-only enumeration |
| Device listing | `frida-ls-devices` | Zone 2 | Read-only enumeration |
| Function discovery | `frida-discover -n <process>` | Zone 2 | Read-only discovery |
| Function tracing | `frida-trace -n <process> -i <pattern>` | Zone 2 | Read-only call tracing |
| Java method tracing | `frida-trace -U <pkg> -j '<class>!<method>'` | Zone 2 | Read-only method tracing |
| Read-only script attach | `frida -n <process> -l read-script.js` | Zone 2 | Script uses only send()/console.log() |
| Process termination | `frida-kill -n <process>` | **Zone 3** | Modifies target system state |
| Write hook script | `frida -n <process> -l write-script.js` | **Zone 3** | Script uses Interceptor.replace or args modification |
| Memory patching | `frida -n <process> -l patch-script.js` | **Zone 3** | Script uses Memory.write* operations |
| Function replacement | `frida -n <process> -l replace-script.js` | **Zone 3** | Script uses Interceptor.replace |
| Return value modification | `frida -n <process> -l retval-script.js` | **Zone 3** | Script calls retval.replace() |

---

## mitmproxy Classification

### Zone 2 Proxy Modes (All Modes, Capture Only)

mitmproxy supports seven proxy modes. ALL modes are Zone 2 when used for capture only (no modification scripts).

| Mode | Flag | Purpose |
|------|------|---------|
| Regular | `--mode regular` (default) | Client configures proxy manually |
| Transparent | `--mode transparent` | Network-level interception (requires iptables/pf setup) |
| Reverse | `--mode reverse:<spec>` | Forward all traffic to specific upstream server |
| Local | `--mode local:<process>` | Intercept specific local process traffic |
| SOCKS5 | `--mode socks5` | SOCKS5 proxy mode |
| WireGuard | `--mode wireguard` | WireGuard tunnel-based interception |
| Upstream | `--mode upstream:<spec>` | Forward to upstream proxy server |

### mitmproxy Script Classification

The `-s` flag loads a Python script. The script content determines zone classification.

**Zone 2 script indicators (read-only):**
- `flow.response.content` read without assignment
- `ctx.log()` calls
- `flow.request.url` read without modification
- No `flow.response =`, `flow.request.headers[...] =`, `flow.response.status_code =` assignments

**Zone 3 script indicators (modification):**
- `flow.response.content = ...`
- `flow.response.set_text(...)`
- `flow.request.headers[...] = ...`
- `flow.response.headers[...] = ...`
- `flow.response.status_code = ...`
- `flow.request.url = ...`
- `flow.request.content = ...`
- `flow.kill()` (drops connection)

### mitmdump Output Flags

| Flag | Zone | Purpose |
|------|------|---------|
| `-w <file>` | Zone 2 | Write flows to file |
| `-r <file>` | Zone 2 | Read flows from file |
| `-n` | Zone 2 | No bind to proxy port (replay mode) |
| `-C <file>` | Zone 2 | Replay client requests from file |
| `-s <script>` | Zone 2 or 3 | Depends on script content (see above) |

---

## Frida Classification

### Read-Only vs. Write Operations

The distinction between Zone 2 and Zone 3 for Frida is based on whether the instrumentation script reads or writes target process state.

**Zone 2 (Read-Only) API calls:**
- `Interceptor.attach(ptr, { onEnter(args) { send(...); }, onLeave(retval) { send(...); } })` -- observation only via send()
- `Memory.readByteArray(ptr, length)`
- `Memory.readUtf8String(ptr)`
- `Module.findExportByName(module, name)`
- `Module.enumerateExports(module)`
- `Process.enumerateModules()`
- `Thread.backtrace(context)`
- `DebugSymbol.fromAddress(ptr)`
- `Stalker.follow(threadId, { events: { call: true } })` -- code tracing (read-only observation)

**Zone 3 (Write/Modification) API calls:**
- `Interceptor.replace(ptr, new NativeCallback(...))`
- `args[N] = ptr(...)` or `args[N] = new NativePointer(...)` inside onEnter
- `retval.replace(ptr(...))` inside onLeave
- `Memory.writeByteArray(ptr, bytes)`
- `Memory.writeUtf8String(ptr, string)`
- `Memory.protect(ptr, size, 'rwx')`
- `Memory.patchCode(ptr, size, callback)`
- `new NativeFunction(ptr, retType, argTypes)` when called with side effects

### Frida Connection Modes

All connection modes are Zone 2 for establishing the instrumentation session. The zone classification depends on the script content, not the connection method.

| Mode | Flag | Purpose |
|------|------|---------|
| Local process (name) | `-n <name>` | Attach to local process by name |
| Local process (PID) | `-p <pid>` | Attach to local process by PID |
| USB device | `-U` | Attach to process on USB-connected device |
| Remote device | `-R` / `-H <host>` | Attach to process on remote device |
| Spawn mode | `-f <binary>` | Spawn new process and attach |

---

## Script Content Analysis

Before executing any script (mitmproxy `-s` or Frida `-l`), the agent MUST:

1. **Read the script file** using the Read tool.
2. **Scan for Zone 3 indicators** using the patterns defined above.
3. **Classify the script** as Zone 2 or Zone 3.
4. **If Zone 3:** HALT and present approval request to operator.
5. **If Zone 2:** Proceed with execution.
6. **If classification is ambiguous:** Default to Zone 3 (fail-closed).

### Compound Scripts

Scripts may contain both read-only and write operations. If ANY write operation is present, the ENTIRE script is classified as Zone 3. There is no partial zone classification.

---

## Escalation Procedure

When a Zone 3 operation is identified:

1. **HALT** -- Stop all execution immediately.
2. **Classify** -- Document the Zone 3 classification reason (which specific operation triggers escalation).
3. **Prepare approval request** -- Construct the approval structure per zone-3-exploit.md Section "Per-Operation Approval Requirement".
4. **Present to operator** -- Display full approval request including script content.
5. **Await explicit approval** -- Only "yes" or equivalent affirmative constitutes approval.
6. **Log decision** -- Record approval or rejection in Zone 3 audit log.
7. **Execute or return** -- On approval, execute with full Zone 3 audit logging. On rejection, return to orchestrator.

---

## Fail-Closed Default

For any operation not explicitly listed in the Zone Classification Matrix:

- **Unrecognized mitmproxy flag or mode:** Zone 3
- **Unrecognized Frida CLI tool:** Zone 3
- **Unrecognized Frida API call in script:** Zone 3
- **Script content that cannot be parsed:** Zone 3
- **Binary scripts or obfuscated scripts:** Zone 3

The fail-closed default ensures that novel or unexpected operations receive the highest-privilege zone classification and require explicit human approval.

---

## Traceability

| Reference | Location |
|-----------|----------|
| ADR-PROJ023-001 (Architecture Decision) | `projects/PROJ-023-exploit-framework/work/design/skill-architecture.md` |
| Zone 2 Guardrail Profile | `skills/rainbow/rules/zone-2-active.md` |
| Zone 3 Guardrail Profile | `skills/rainbow/rules/zone-3-exploit.md` |
| Credential Filter Rules | `skills/rainbow/rules/rainbow-credential-filter.md` |
| Engagement Lifecycle | `skills/rainbow/rules/engagement-lifecycle.md` |
| mitmproxy Documentation | `https://docs.mitmproxy.org/stable/` |
| Frida Documentation | `https://frida.re/docs/home/` |
