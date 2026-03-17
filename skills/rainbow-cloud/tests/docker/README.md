# Docker Compose -- Rainbow Cloud Sub-Skill

> Placeholder for container orchestration. Depends on T0.8 (Docker Compose infrastructure phase).

## Required Containers

| Service | Image | Purpose | Port |
|---------|-------|---------|------|
| Neo4j | `neo4j:5-community` | Graph database for Cartography | 7474 (HTTP), 7687 (Bolt) |
| Cartography | `cartography-cncf/cartography:latest` | Infrastructure sync | N/A (CLI) |

## Neo4j Sidecar Dependency

Cartography requires a running Neo4j instance. The Docker Compose configuration will:

1. Start Neo4j community edition with default credentials
2. Wait for Neo4j health check before starting Cartography
3. Mount a volume for persistent graph data
4. Configure Bolt protocol on port 7687

## Deferred To

T0.8: Docker Compose infrastructure phase (Wave 0 infrastructure).

## Notes

- Neo4j community edition (free) is sufficient for Cartography
- Cartography sync requires cloud provider credentials mounted as secrets
- BDD tests for rainbow-cloud-mapper require Neo4j to be running
- Consider Neo4j memory tuning for large cloud environments (8GB+ heap recommended)
