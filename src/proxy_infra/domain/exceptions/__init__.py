# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Domain exceptions for proxy infrastructure bounded context."""

from src.proxy_infra.domain.exceptions.api_key_expired_error import ApiKeyExpiredError
from src.proxy_infra.domain.exceptions.api_key_permission_error import ApiKeyPermissionError
from src.proxy_infra.domain.exceptions.burned_node_reuse_error import BurnedNodeReuseError
from src.proxy_infra.domain.exceptions.credential_not_found_error import CredentialNotFoundError
from src.proxy_infra.domain.exceptions.engagement_scope_error import EngagementScopeError
from src.proxy_infra.domain.exceptions.fingerprint_required_error import FingerprintRequiredError
from src.proxy_infra.domain.exceptions.invalid_engagement_id_error import InvalidEngagementIdError
from src.proxy_infra.domain.exceptions.invalid_node_transition_error import InvalidNodeTransitionError
from src.proxy_infra.domain.exceptions.manifest_integrity_error import ManifestIntegrityError
from src.proxy_infra.domain.exceptions.pool_capacity_exceeded_error import PoolCapacityExceededError
from src.proxy_infra.domain.exceptions.pool_limit_exceeded_error import PoolLimitExceededError
from src.proxy_infra.domain.exceptions.provision_error import ProvisionError

# Alias for backward compatibility (tests use ProvisioningError)
ProvisioningError = ProvisionError
from src.proxy_infra.domain.exceptions.teardown_error import TeardownError
from src.proxy_infra.domain.exceptions.vultr_ip_acl_mismatch_error import VultrIpAclMismatchError

__all__ = [
    "ApiKeyExpiredError",
    "ApiKeyPermissionError",
    "BurnedNodeReuseError",
    "CredentialNotFoundError",
    "EngagementScopeError",
    "FingerprintRequiredError",
    "InvalidEngagementIdError",
    "InvalidNodeTransitionError",
    "ManifestIntegrityError",
    "PoolCapacityExceededError",
    "PoolLimitExceededError",
    "ProvisionError",
    "ProvisioningError",
    "TeardownError",
    "VultrIpAclMismatchError",
]
