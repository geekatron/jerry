# Container Test Infrastructure -- Placeholder

> Deferred to T0.8 (container infrastructure). Container Dockerfiles for rainbow-recon tool isolation will be created when the shared container infrastructure from T0.8 is available.

## Planned Containers

| Container | Tools | Base Image |
|-----------|-------|------------|
| recon-pipeline | Subfinder, httpx, dnsx, Naabu, Katana, Nuclei | golang:1.24-alpine (ProjectDiscovery tools) |
| recon-osint | OWASP Amass, Maigret | python:3.12-slim + golang:1.24-alpine |

## Dependency

This directory depends on T0.8 container infrastructure which provides:
- Shared base images
- Network isolation profiles
- Volume mount conventions
- Container health checks

Do NOT create Dockerfiles here until T0.8 is complete.
