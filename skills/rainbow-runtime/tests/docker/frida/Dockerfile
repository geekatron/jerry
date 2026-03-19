# =============================================================================
# Rainbow Runtime -- Frida
# =============================================================================
# Tools: frida, frida-trace, frida-ps, frida-ls-devices
# Agent: rainbow-runtime-instrument
# Zone: 3 (Exploitation -- process instrumentation)
# Tier: A (execute directly via docker compose exec)
#
# Frida requires a target process -- exits without one.
# Container uses bash entrypoint; tools dispatched via docker compose exec.
# SYS_PTRACE capability required (set in compose file).
# =============================================================================

FROM python:3.11-slim

RUN pip install --no-cache-dir frida-tools>=12.0

WORKDIR /work

# Verify frida is installed
RUN python3 -c "import frida; print('frida', frida.__version__)"

# Container stays alive for CLI dispatch.
# frida commands are invoked per-operation via docker compose exec.
ENTRYPOINT ["/bin/bash"]
CMD ["-c", "echo 'Frida ready'; exec /bin/bash"]
