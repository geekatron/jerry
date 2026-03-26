# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Cloud-init template generation for proxy node provisioning.

Produces cloud-config YAML for two proxy node types:

  - Type A (SSH tunnel endpoint): openssh-server, hardened SSH config,
    authorized_keys, UFW firewall.
  - Type B (microsocks direct SOCKS5): microsocks v1.0.5 installed from
    pinned release tarball with SHA-256 verification, systemd unit using
    EnvironmentFile=/etc/microsocks.env, UFW, dead man switch cron.

F-C-001 REMEDIATION: Zero credentials in rendered YAML.  No SOCKS5
usernames, passwords, SSH private keys, or API keys.  Credentials are
injected post-boot via SSH (7-step sequence).

References:
    - TASK-023-031: Cloud-Init Template Generation (Type A SSH + Type B Microsocks)
    - EPIC-023-007: Proxy infrastructure automation
    - F-C-001: IMDS exposes cloud-init user_data in plaintext (CVSS 8.8)
    - FM-027: Use pinned release tarball, NOT git clone
    - EN-023-001: PoC verified microsocks v1.0.5 SHA-256
"""

from __future__ import annotations

import re
from enum import Enum
from textwrap import dedent


# ---------------------------------------------------------------------------
# Supply chain constants (FM-027, EN-023-001)
# ---------------------------------------------------------------------------

_MICROSOCKS_VERSION = "1.0.5"
# SHA-256 of v1.0.5.tar.gz, verified by EN-023-001 PoC (2026-03-24)
_MICROSOCKS_SHA256 = "939d1851a18a4c03f3cc5c92ff7a50eaf045da7814764b4cb9e26921db15abc8"

# Credential-like patterns used by assert_no_credentials().
# Patterns that begin with "-----" are treated as literal substring matches.
_CREDENTIAL_PATTERNS: list[str] = [
    r"PROXY_USER\s*=\s*\S+",
    r"PROXY_PASS\s*=\s*\S+",
    r"SOCKS5_PASS\s*=\s*\S+",
    r"password:\s*\S+",
    r"proxy_password\s*=\s*\S+",
    "-----BEGIN " + "OPENSSH PRIVATE KEY-----",
    "-----BEGIN " + "RSA PRIVATE KEY-----",
    "-----BEGIN " + "EC PRIVATE KEY-----",
    r"dop_v1_[a-f0-9]{20,}",
]


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------


class CloudInitType(Enum):
    """Proxy node cloud-init template type selector."""

    TYPE_A_SSH_ENDPOINT = "type_a_ssh_endpoint"
    TYPE_B_MICROSOCKS = "type_b_microsocks"


class CloudInitTemplateGenerator:
    """Renders cloud-init user-data for proxy node provisioning.

    Produces credential-free cloud-config YAML (F-C-001 remediation).
    SOCKS5 credentials are never accepted as parameters; they are injected
    post-boot via the 7-step SSH injection sequence.

    Usage::

        generator = CloudInitTemplateGenerator()
        yaml_str = generator.render(
            template_type=CloudInitType.TYPE_B_MICROSOCKS,
            ssh_public_key="ssh-ed25519 AAAA... operator@jerry",
            socks_port=1080,
            operator_ip="203.0.113.1",
            engagement_id="ENG-001",
        )
    """

    def render(
        self,
        *,
        template_type: CloudInitType,
        ssh_public_key: str,
        socks_port: int,
        operator_ip: str,
        engagement_id: str,
    ) -> str:
        """Render a cloud-init cloud-config YAML string.

        Args:
            template_type: Which proxy configuration to generate.
            ssh_public_key: Operator SSH public key injected into
                authorized_keys.  Must be the PUBLIC key only -- private
                key material is never accepted (F-C-001).
            socks_port: TCP port for SOCKS5 (e.g. 1080).
            operator_ip: Source IP allowed through UFW for SSH and SOCKS5.
            engagement_id: Engagement identifier embedded in node metadata.

        Returns:
            A cloud-config YAML string suitable for passing as VPS
            ``user_data``.

        Raises:
            TypeError: If any credential parameter (``socks5_username``,
                ``socks5_password``) is supplied -- credentials are never
                template variables (F-C-001 architectural constraint).
        """
        if template_type is CloudInitType.TYPE_A_SSH_ENDPOINT:
            return self._render_type_a(
                ssh_public_key=ssh_public_key,
                socks_port=socks_port,
                operator_ip=operator_ip,
                engagement_id=engagement_id,
            )
        if template_type is CloudInitType.TYPE_B_MICROSOCKS:
            return self._render_type_b(
                ssh_public_key=ssh_public_key,
                socks_port=socks_port,
                operator_ip=operator_ip,
                engagement_id=engagement_id,
            )
        raise ValueError(f"Unknown template type: {template_type!r}")  # pragma: no cover

    def get_post_boot_injection_steps(self) -> list[str]:
        """Return the 7-step post-boot credential injection sequence.

        The CLM executes these steps after cloud-init completes to inject
        SOCKS5 credentials and bring the proxy to READY status.

        Returns:
            Ordered list of 7 step descriptions (TASK-023-031 AC).
        """
        return [
            # Step 1
            "Poll SSH availability on port 22 (timeout 180s, poll interval 5s; FM-004)",
            # Step 2
            "Connect to proxy node via SSH using the engagement Ed25519 key",
            # Step 3
            (
                "Generate SOCKS5 credentials on-node: "
                "openssl rand -hex 16 -> PROXY_USER, openssl rand -hex 32 -> PROXY_PASS"
            ),
            # Step 4
            (
                "Write credential environment file: "
                "echo 'PROXY_USER=<user>\\nPROXY_PASS=<pass>' | "
                "sudo tee /etc/microsocks.env && sudo chmod 0600 /etc/microsocks.env"
            ),
            # Step 5
            "Start microsocks service: sudo systemctl start microsocks",
            # Step 6
            (
                "Verify SOCKS5 connectivity: "
                "curl --socks5-hostname <node_ip>:<port> --proxy-user <user>:<pass> "
                "https://ifconfig.me"
            ),
            # Step 7
            (
                "Write node to pool manifest with status READY and verified SSH fingerprint "
                "(PI-007)"
            ),
        ]

    # ------------------------------------------------------------------
    # Private rendering helpers
    # ------------------------------------------------------------------

    def _render_type_a(
        self,
        *,
        ssh_public_key: str,
        socks_port: int,
        operator_ip: str,
        engagement_id: str,
    ) -> str:
        """Render Type A: SSH tunnel endpoint cloud-config.

        Configures:
        - openssh-server with hardened settings (key-only, no root login)
        - authorized_keys populated with operator SSH public key
        - UFW firewall (SSH from operator IP only)
        - unattended-upgrades for OS hardening
        - Engagement metadata file
        """
        # Build authorized_keys write_files entry separately so the public
        # key value is cleanly embedded with correct indentation.
        cloud_config = dedent(f"""\
            #cloud-config
            # Jerry CLM Proxy Provisioner -- Type A SSH Tunnel Endpoint (credential-free)
            # TASK-023-031 | Engagement: {engagement_id}
            # F-C-001: zero credentials in user_data

            package_update: true
            package_upgrade: false

            packages:
              - openssh-server
              - ufw
              - unattended-upgrades

            write_files:
              - path: /etc/ssh/sshd_config.d/99-jerry-hardening.conf
                owner: root:root
                permissions: "0644"
                content: |
                  # Jerry CLM SSH hardening (TASK-023-031 AC)
                  PasswordAuthentication no
                  PermitRootLogin no
                  ChallengeResponseAuthentication no
                  UsePAM yes
                  X11Forwarding no
                  PrintMotd no
                  AcceptEnv LANG LC_*
                  Subsystem sftp /usr/lib/openssh/sftp-server

              - path: /root/.ssh/authorized_keys
                owner: root:root
                permissions: "0600"
                content: |
                  {ssh_public_key}

              - path: /etc/jerry-proxy-metadata.yaml
                owner: root:root
                permissions: "0644"
                content: |
                  engagement_id: {engagement_id}
                  proxy_type: type_a_ssh_endpoint
                  operator_ip: {operator_ip}

            runcmd:
              # UFW firewall: allow SSH from operator IP only
              - ufw default deny incoming
              - ufw default allow outgoing
              - ufw allow from {operator_ip} to any port 22 proto tcp
              - ufw --force enable

              # Reload sshd to apply hardened config
              - systemctl reload ssh || systemctl reload sshd

              # Enable unattended security upgrades (OS hardening)
              - systemctl enable unattended-upgrades
              - systemctl start unattended-upgrades

              # Signal SSH readiness
              - touch /var/run/jerry-proxy-ssh-ready
        """)
        return cloud_config

    def _render_type_b(
        self,
        *,
        ssh_public_key: str,
        socks_port: int,
        operator_ip: str,
        engagement_id: str,
    ) -> str:
        """Render Type B: microsocks direct SOCKS5 cloud-config.

        Configures:
        - microsocks v1.0.5 installed from pinned tarball + SHA-256 (FM-027)
        - systemd unit with EnvironmentFile=/etc/microsocks.env (F-C-001)
        - Service ENABLED but NOT started (credentials injected post-boot)
        - UFW firewall (SSH + SOCKS5 from operator IP)
        - Dead man switch cron
        - unattended-upgrades for OS hardening
        """
        cloud_config = dedent(f"""\
            #cloud-config
            # Jerry CLM Proxy Provisioner -- Type B microsocks SOCKS5 (credential-free)
            # TASK-023-031 | Engagement: {engagement_id}
            # F-C-001: zero credentials in user_data; EnvironmentFile injected post-boot
            # FM-027: pinned release tarball with SHA-256 verification

            package_update: true
            package_upgrade: false

            packages:
              - build-essential
              - curl
              - ufw
              - unattended-upgrades

            write_files:
              - path: /etc/systemd/system/microsocks.service
                owner: root:root
                permissions: "0644"
                content: |
                  [Unit]
                  Description=MicroSocks SOCKS5 Proxy
                  After=network.target

                  [Service]
                  Type=simple
                  EnvironmentFile=/etc/microsocks.env
                  ExecStart=/usr/local/bin/microsocks -p {socks_port} -u ${{PROXY_USER}} -P ${{PROXY_PASS}}
                  Restart=always
                  RestartSec=3

                  [Install]
                  WantedBy=multi-user.target

              - path: /root/.ssh/authorized_keys
                owner: root:root
                permissions: "0600"
                content: |
                  {ssh_public_key}

              - path: /etc/jerry-proxy-metadata.yaml
                owner: root:root
                permissions: "0644"
                content: |
                  engagement_id: {engagement_id}
                  proxy_type: type_b_microsocks
                  operator_ip: {operator_ip}
                  socks_port: {socks_port}

            runcmd:
              # Install microsocks from pinned release tarball (FM-027, EN-023-001)
              # SHA-256 verified: {_MICROSOCKS_SHA256}
              - |
                set -e
                MICROSOCKS_VERSION="{_MICROSOCKS_VERSION}"
                MICROSOCKS_SHA256="{_MICROSOCKS_SHA256}"
                cd /tmp
                curl -fsSL "https://github.com/rofl0r/microsocks/archive/refs/tags/v${{MICROSOCKS_VERSION}}.tar.gz" -o microsocks.tar.gz
                echo "${{MICROSOCKS_SHA256}}  microsocks.tar.gz" | sha256sum -c - || {{ echo "CHECKSUM FAILED"; exit 1; }}
                tar xzf microsocks.tar.gz
                cd "microsocks-${{MICROSOCKS_VERSION}}" && make && cp microsocks /usr/local/bin/
                rm -rf /tmp/microsocks*

              # UFW firewall: allow SSH and SOCKS5 from operator IP only
              - ufw default deny incoming
              - ufw default allow outgoing
              - ufw allow from {operator_ip} to any port 22 proto tcp
              - ufw allow from {operator_ip} to any port {socks_port} proto tcp
              - ufw --force enable

              # Enable microsocks service (do NOT start -- credentials injected post-boot)
              # TASK-023-031 AC: microsocks MUST NOT start until /etc/microsocks.env exists
              - systemctl daemon-reload
              - systemctl enable microsocks

              # Enable unattended security upgrades (OS hardening)
              - systemctl enable unattended-upgrades
              - systemctl start unattended-upgrades

              # Dead man switch: self-destruct script (checks metadata TTL)
              - |
                cat > /usr/local/bin/jerry-self-destruct.sh << 'SCRIPT'
                #!/bin/bash
                MARKER=/etc/jerry-proxy-metadata.yaml
                [ -f "$MARKER" ] || exit 0
                TTL_HOURS=$(grep ttl_hours "$MARKER" 2>/dev/null | awk '{{print $2}}')
                [ -z "$TTL_HOURS" ] && exit 0
                CREATED=$(stat -c %Y "$MARKER")
                NOW=$(date +%s)
                DEADLINE=$((CREATED + TTL_HOURS * 3600))
                if [ "$NOW" -gt "$DEADLINE" ]; then
                  logger "Jerry proxy TTL expired. Shutting down."
                  shutdown -h now
                fi
                SCRIPT
              - chmod +x /usr/local/bin/jerry-self-destruct.sh
              - echo "*/5 * * * * root /usr/local/bin/jerry-self-destruct.sh" >> /etc/crontab

              # Signal SSH readiness for CLM post-boot credential injection
              - touch /var/run/jerry-proxy-ssh-ready
        """)
        return cloud_config


# ---------------------------------------------------------------------------
# Validation utility (public)
# ---------------------------------------------------------------------------


def assert_no_credentials(rendered_yaml: str) -> None:
    """Scan rendered YAML for credential-like patterns and raise if found.

    Implements the F-C-001 scan from the test suite as a reusable utility.
    Callers (adapters, tests) can invoke this after rendering to enforce
    the zero-credentials invariant before submitting ``user_data`` to
    a cloud provider API.

    Args:
        rendered_yaml: The rendered cloud-config YAML string to inspect.

    Raises:
        ValueError: If any credential-like pattern is detected in the
            rendered output, with a description of which pattern matched.
    """
    for pattern in _CREDENTIAL_PATTERNS:
        if pattern.startswith("-----"):
            if pattern in rendered_yaml:
                raise ValueError(
                    f"F-C-001 VIOLATION: private key header detected in "
                    f"rendered cloud-init user_data.  "
                    f"Credential material must never appear in user_data "
                    f"(IMDS plaintext exposure, CVSS 8.8)."
                )
        else:
            match = re.search(pattern, rendered_yaml)
            if match:
                raise ValueError(
                    f"F-C-001 VIOLATION: credential pattern '{pattern}' "
                    f"detected at position {match.start()} in rendered "
                    f"cloud-init user_data.  "
                    f"Credential material must never appear in user_data "
                    f"(IMDS plaintext exposure, CVSS 8.8)."
                )
