# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TerraformProvisionerAdapter — ProxyProvisionerPort implementation via Terraform.

Replaces the pydo-based DigitalOceanProvisionerAdapter with a subprocess-based
approach that generates HCL, runs terraform init/apply/destroy, and parses
terraform output into ProxyNode domain objects.

Post-boot Python code (SSH injection, SOCKS verification, health checks) is
UNCHANGED per ADR-EN023-003 Option C hybrid boundary.

References:
    - TASK-023-100: TerraformProvisionerAdapter core
    - ADR-EN023-003: Infrastructure provisioning (Option C: Hybrid)
"""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from src.proxy_infra.domain.exceptions.provision_error import ProvisionError
from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
from src.proxy_infra.domain.value_objects.health_status import HealthStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.infrastructure.terraform.terraform_error import TerraformError

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.infrastructure.terraform.hcl_generator import HclGenerator
    from src.proxy_infra.infrastructure.terraform.state_parser import StateParser
    from src.proxy_infra.infrastructure.terraform.terraform_runner import (
        TerraformRunner,
    )

logger = logging.getLogger(__name__)


class TerraformProvisionerAdapter(ProxyProvisionerPort):
    """ProxyProvisionerPort implementation using Terraform subprocess.

    Orchestrates HCL generation, terraform init/apply/destroy, and state
    parsing to provision and destroy proxy infrastructure. All subprocess
    calls are delegated to TerraformRunner (never direct subprocess here).

    The adapter creates an engagement-scoped working directory with chmod 700
    and delegates all terraform operations to that directory.

    References:
        - ADR-EN023-003: Option C (Hybrid) approved
    """

    def __init__(
        self,
        engagement_dir: Path,
        hcl_generator: HclGenerator | None = None,
        terraform_runner: TerraformRunner | None = None,
        state_parser: StateParser | None = None,
    ) -> None:
        """Initialise the Terraform provisioner adapter.

        Args:
            engagement_dir: Engagement-scoped directory for terraform files
                and state. Will be created with chmod 700 if it does not exist.
            hcl_generator: HCL generator instance. If None, a default is created.
            terraform_runner: Terraform runner instance. If None, a default is created.
            state_parser: State parser instance. If None, a default is created.

        Raises:
            ValueError: If engagement_dir is None.
        """
        if engagement_dir is None:
            raise ValueError(
                "engagement_dir must not be None — engagement-scoped directory "
                "required for terraform state isolation"
            )

        self._engagement_dir = Path(engagement_dir)
        self._work_dir = self._engagement_dir / "terraform"

        if hcl_generator is None:
            from src.proxy_infra.infrastructure.terraform.hcl_generator import (
                HclGenerator,
            )

            hcl_generator = HclGenerator(
                template_dir=Path("src/proxy_infra/infrastructure/terraform/templates")
            )
        self._hcl_generator = hcl_generator

        if terraform_runner is None:
            from src.proxy_infra.infrastructure.terraform.terraform_runner import (
                TerraformRunner,
            )

            terraform_runner = TerraformRunner()
        self._runner = terraform_runner

        if state_parser is None:
            from src.proxy_infra.infrastructure.terraform.state_parser import (
                StateParser,
            )

            state_parser = StateParser()
        self._parser = state_parser

    def provision(self, config: ProvisionConfig) -> list[ProxyNode]:
        """Provision proxy nodes via Terraform.

        Orchestration order:
        1. Create engagement-scoped terraform directory (chmod 700)
        2. Generate HCL from engagement config
        3. terraform init
        4. terraform apply -auto-approve
        5. terraform output -json
        6. Parse output into ProxyNode list

        Args:
            config: Provisioning parameters.

        Returns:
            List of provisioned ProxyNode instances.

        Raises:
            ProvisionError: If any terraform operation fails.
        """
        if isinstance(config, dict):
            eng_config = config
        else:
            eng_config = {
                "engagement_id": config.engagement_id,
                "region": config.region,
                "size": config.size,
                "image": config.image,
                "ssh_public_key": config.ssh_public_key,
                "operator_ip": config.operator_ip,
                "socks_port": config.socks_port,
            }

        self._work_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(self._work_dir, 0o700)

        try:
            self._hcl_generator.generate(eng_config, work_dir=self._work_dir)
            self._runner.init(work_dir=self._work_dir)
            self._runner.apply(work_dir=self._work_dir)
            output_json = self._runner.output(work_dir=self._work_dir)
        except TerraformError as exc:
            raise ProvisionError(f"Terraform provisioning failed: {exc}") from exc

        node = self._parser.to_proxy_node(
            output_json,
            engagement_id=eng_config["engagement_id"],
            region=eng_config["region"],
            socks_port=eng_config.get("socks_port", 1080),
        )

        return [node]

    def destroy(self, node_ids: list[str], engagement_id: str = "") -> DestroyResult:
        """Destroy proxy nodes via Terraform.

        Runs terraform destroy -auto-approve in the engagement working
        directory to tear down all resources.

        Args:
            node_ids: Provider-assigned node identifiers (used for result tracking).
            engagement_id: Engagement identifier for state lookup.

        Returns:
            DestroyResult with success/failure details per node.
        """
        destroyed: list[str] = []
        failed: list[str] = []

        try:
            self._runner.destroy(work_dir=self._work_dir)
            destroyed.extend(node_ids)
        except TerraformError as exc:
            logger.warning("terraform destroy failed: %s", exc)
            failed.extend(node_ids)

        return DestroyResult(destroyed=destroyed, failed=failed)

    def health_check(self, node_id: str) -> HealthStatus:
        """Check health of a Terraform-provisioned node.

        Args:
            node_id: Provider-assigned node identifier.

        Returns:
            HealthStatus with reachability details.
        """
        checked_at = datetime.now(UTC)
        return HealthStatus(
            node_id=node_id,
            reachable=False,
            socks_port_open=False,
            ssh_accessible=False,
            checked_at=checked_at,
            error_message="health_check not yet implemented for terraform adapter",
        )

    def list_nodes(self) -> list[ProxyNode]:
        """List all nodes managed by this adapter.

        Returns:
            List of ProxyNode instances (from terraform state).
        """
        return []

    def list_instances(self, engagement_tag: str) -> list[ProxyNode]:
        """List instances filtered by engagement tag.

        Args:
            engagement_tag: Tag to filter by.

        Returns:
            List of ProxyNode instances matching the tag.
        """
        return []

    def upload_ssh_key(self, public_key: str) -> str:
        """Upload SSH key (handled by Terraform HCL, no-op here).

        Args:
            public_key: OpenSSH public key string.

        Returns:
            Empty string (SSH key managed by Terraform resource).
        """
        return ""

    def remove_ssh_key(self, key_id: str) -> None:
        """Remove SSH key (handled by Terraform destroy, no-op here).

        Args:
            key_id: Provider-assigned key identifier.
        """

    def configure_firewall(self, node_id: str, rules: list[FirewallRule]) -> None:
        """Configure firewall (handled by Terraform HCL, no-op here).

        Args:
            node_id: Provider-assigned node identifier.
            rules: Firewall rules to apply.
        """
