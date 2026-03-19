# =============================================================================
# Rainbow Runtime -- mitmproxy
# =============================================================================
# Tools: mitmproxy (TUI), mitmdump (headless), mitmweb (web UI)
# Agent: rainbow-runtime-instrument
# Zone: 2 (Active Reconnaissance -- network interception)
# Tier: A (execute directly via docker compose exec)
#
# mitmproxy TUI requires a terminal -- crashes without one.
# Container uses bash entrypoint; tools dispatched via docker compose exec.
# For headless interception: docker compose exec mitmproxy mitmdump -p 8080
# =============================================================================

FROM python:3.11-slim

RUN pip install --no-cache-dir mitmproxy>=10.0

# Install curl for proxy health checking and network testing
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# Verify tools are installed
RUN mitmdump --version

# Container stays alive for CLI dispatch.
ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'mitmproxy ready (use mitmdump for headless)'; exec /bin/bash"]
