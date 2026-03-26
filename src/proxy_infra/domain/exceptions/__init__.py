# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Domain exceptions for proxy infrastructure bounded context."""

from src.proxy_infra.domain.exceptions.burned_node_reuse_error import BurnedNodeReuseError
from src.proxy_infra.domain.exceptions.credential_not_found_error import CredentialNotFoundError
from src.proxy_infra.domain.exceptions.engagement_scope_error import EngagementScopeError
from src.proxy_infra.domain.exceptions.manifest_integrity_error import ManifestIntegrityError
from src.proxy_infra.domain.exceptions.pool_limit_exceeded_error import PoolLimitExceededError
from src.proxy_infra.domain.exceptions.provision_error import ProvisionError
from src.proxy_infra.domain.exceptions.teardown_error import TeardownError

__all__ = [
    "BurnedNodeReuseError",
    "CredentialNotFoundError",
    "EngagementScopeError",
    "ManifestIntegrityError",
    "PoolLimitExceededError",
    "ProvisionError",
    "TeardownError",
]
