# Docker Test Infrastructure Placeholder

> Container infrastructure for mitmproxy and Frida execution environment. Deferred to T0.8 container delivery wave.

## Planned Contents

- `Dockerfile.mitmproxy` -- mitmproxy >= 10.0 with Python scripting support
- `Dockerfile.frida` -- Frida >= 16.0 with frida-tools CLI suite
- `docker-compose.runtime.yaml` -- Orchestrated test environment with target services
- `target-service/` -- Mock HTTP service for mitmproxy interception testing
- `target-binary/` -- Mock binary for Frida instrumentation testing

## Status

NOT IMPLEMENTED. Placeholder per ADR-PROJ023-001 delivery roadmap. Container infrastructure is planned for T0.8 wave (consistent tool availability).

## Compensating Controls

Until container infrastructure exists:
- AD-010 degradation levels handle tool unavailability
- BDD scenarios validate agent behavioral compliance independent of tool availability
- P-022 disclosure ensures agent reports tool gaps honestly
