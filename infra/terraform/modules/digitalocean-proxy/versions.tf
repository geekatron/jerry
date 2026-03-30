# Provider version constraints for the digitalocean-proxy module.
# Pinned to exact version to prevent supply chain drift.
# Update via: terraform init -upgrade (after changing version below).

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "= 2.43.0"
    }
  }
}
