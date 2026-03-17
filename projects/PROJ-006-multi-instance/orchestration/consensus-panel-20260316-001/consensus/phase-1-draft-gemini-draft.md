---
workflow_id: consensus-panel-20260316-001
phase_id: phase-1-draft
panel_topic: Best approach to implement the Consensus Panel runner
aDone.
d_by: gemini-pro (Independent Draft)
date: 2026-03-16
---

# Independent Draft: Consensus Panel Runner Implementation

This document presents a recommended design and implementation strategy for the Jerry Framework's Consensus Panel runner, in response to the intent document `consensus-panel-20260316-001`.

## Section 1: Implementation Approach

The recommended implementation is a **self-contained Python CLI script**, managed and executed via `uv run`.

This approach is superior to alternatives for the following reasons:

1.  **Robustness and Maintainability:** Python's `subprocess` module provides robust, cross-platform process management, including handling of PIDs, streams, and termination signals. Error handling, state management (parsing/writing YAML), and complex pre-flight logic are significantly cleaner and more maintainable in Python than in a pure bash script.
2.  **Alignment with Constraints:** The "uv run only" constraint strongly favors a Python-centric solution. This approach avoids brittle shell script dependencies and ensures the execution environment is consistent and managed by the project's chosen tooling.
3.  **Integration and Complexity:** While a Jerry Skill could work, it would introduce unnecessary coupling between the orchestration logic and the skill framework. A standalone CLI script is more modular, reusable, and easier to test in isolation. It can be invoked by a skill, but its core logic remains independent.

A single Python script can encapsulate all the required logic, from pre-flight checks to launching subprocesses and handing off to synthesis, providing a clear and linear execution flow.

## Section 2: Architecture

The runner will be composed of several distinct logical components, likely organized into a single Python script or a small module.

```
+---------------------------+
|   Consensus Runner CLI    | (main.py)
| (uv run consensus_runner) |
+-------------+-------------+
              |
              | 1. Initialize (reads workflow_id)
              v
+-------------+-------------+      +--------------------------+
|      State Manager        |----->| ORCHESTRATION.yaml       |
| (reads/writes state file) |<-----| (persisted state)        |
+---------------------------+      +--------------------------+
              |
              | 2. Execute Pre-flight
              v
+-------------+-------------+
|     Pre-flight Module     |
| - Platform/CLI/Auth checks|
| - Nested session guard    |
| - Composes panel          |
+-------------+-------------+
              |
              | 3. Run Draft/Critique Phases
              v
+-------------+-------------+
|       Worker Launcher     |
| - For each model:         |
|   - `subprocess.Popen`    | ------> [claude CLI] (subprocess)
|   - Manages PIDs/handles  | ------> [codex CLI]  (subprocess)
|   - Redirects stdout/err  | ------> [gemini CLI] (subprocess)
+-------------+-------------+
              |
              | 4. Monitor workers
              v
+-------------+-------------+
|   Wait/Timeout Handler    |
| - Polls subprocesses      |
| - Enforces PID timeouts   |
| - Kills hung processes    |
+-------------+-------------+
              |
              | 5. Verify and Handoff
              v
+-------------+-------------+      +--------------------------+
|   Output Verifier &       |----->|      orch-synthesizer    |
|   Synthesis Handoff       |      | (invoked via Task tool)  |
| - Checks for output files |      +--------------------------+
| - Handles gaps            |
| - Invokes synthesizer     |
+---------------------------+
```

**Component Responsibilities:**

1.  **Runner CLI (`main.py`):** The entry point. Parses command-line arguments (e.g., `workflow_id`), initializes the state manager, and orchestrates the calls to other components in sequence.
2.  **State Manager:** A class or set of functions responsible for all file I/O with `ORCHESTRATION.yaml`. It handles atomic writes (write to temp file, then rename) to prevent state corruption.
3.  **Pre-flight Module:** Executes the resolution chain. It returns a `PanelComposition` data structure detailing which models are available, their execution type (CLI or API), and their command-line templates. This module contains the `CLAUDECODE=1` nested session guard logic.
4.  **Worker Launcher:** Iterates through the `PanelComposition`. For each worker, it uses `subprocess.Popen` to launch the external CLI tool as a parallel OS subprocess, redirecting `stdout`/`stderr` to dedicated output files. It stores the `Popen` objects for monitoring.
5.  **Wait/Timeout Handler:** Manages the lifecycle of the running subprocesses. It polls for completion and enforces a strict per-PID timeout, escalating from `terminate()` to `kill()` if a process becomes unresponsive.
6.  **Output Verifier & Synthesis Handoff:** After the worker phase, this component checks that the expected output files exist and are non-empty. It records any failures (gaps) in the state file and then invokes the `orch-synthesizer` task with the paths to the successfully generated artifacts.

## Section 3: Key Implementation Details

Here is runnable Python pseudocode for the most complex parts of the implementation.

### Parallel Launch and Per-PID Wait with Timeout

This requires asynchronous management of subprocesses.

```python
import subprocess
import time
import os
import sys

# Assume models_to_run is a list of dicts from the pre-flight check
# e.g., [{'name': 'claude', 'command': ['claude', '...', '-o', 'claude_draft.md']}, ...]
models_to_run = [
    {
        "name": "claude",
        "command": ["claude", "prompt", "Make it so.", "-o", "./claude_draft.md"],
        "output_file": "./claude_draft.md"
    },
    {
        "name": "gemini",
        "command": ["gemini", "prompt", "Engage.", "-o", "./gemini_draft.md"],
        "output_file": "./gemini_draft.md"
    },
]
WORKER_TIMEOUT_SECONDS = 300  # 5 minutes

def run_worker_phase(workers):
    """
    Launches and monitors workers, handling timeouts and termination.
    Returns a dict of worker results {'worker_name': 'success' | 'timeout' | 'error'}.
    """
    procs = {}
    results = {}
    start_time = time.monotonic()

    # 1. Launch all workers in parallel
    for worker in workers:
        worker_name = worker['name']
        log_file = f"./{worker_name}.log"
        try:
            with open(log_file, 'wb') as f_log:
                # On Windows, need to handle process creation flags if shell is needed
                proc = subprocess.Popen(
                    worker['command'],
                    stdout=f_log,
                    stderr=f_log,
                )
                procs[worker_name] = proc
                print(f"Launched {worker_name} with PID {proc.pid}")
        except FileNotFoundError:
            print(f"Error: Command for {worker_name} not found.", file=sys.stderr)
            results[worker_name] = 'error'
        except Exception as e:
            print(f"Error launching {worker_name}: {e}", file=sys.stderr)
            results[worker_name] = 'error'

    running_procs = list(procs.items())

    # 2. Monitor running processes
    while running_procs:
        for worker_name, proc in list(running_procs):
            # Check for timeout
            if time.monotonic() - start_time > WORKER_TIMEOUT_SECONDS:
                print(f"Timeout exceeded for {worker_name} (PID {proc.pid}). Terminating.")
                proc.terminate() # SIGTERM
                try:
                    # Wait a moment for graceful shutdown
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    print(f"{worker_name} did not terminate gracefully. Killing.")
                    proc.kill() # SIGKILL
                results[worker_name] = 'timeout'
                running_procs.remove((worker_name, proc))
                continue

            # Check if process has finished
            if proc.poll() is not None:
                print(f"{worker_name} (PID {proc.pid}) finished with exit code {proc.returncode}.")
                if proc.returncode == 0:
                    results[worker_name] = 'success'
                else:
                    results[worker_name] = 'error'
                running_procs.remove((worker_name, proc))
        
        time.sleep(0.5) # Prevent busy-waiting

    return results

# run_worker_phase(models_to_run)
```

### Output Verification and Gap Handling

This runs after the monitoring loop is complete.

```python
import os

def verify_outputs(workers, results):
    """
    Checks for the existence and content of output files.
    Updates the results dict with verification status.
    """
    verified_results = results.copy()
    
    for worker in workers:
        worker_name = worker['name']
        output_file = worker['output_file']
        
        # Only verify if the process was thought to be successful
        if verified_results.get(worker_name) == 'success':
            try:
                # 1. Check if the file exists
                if not os.path.exists(output_file):
                    print(f"Verification failed for {worker_name}: Output file '{output_file}' not found.")
                    verified_results[worker_name] = 'gap_missing_file'
                    continue
                
                # 2. Check if the file is not empty
                if os.path.getsize(output_file) == 0:
                    print(f"Verification failed for {worker_name}: Output file '{output_file}' is empty.")
                    verified_results[worker_name] = 'gap_empty_file'
                    continue
                
                print(f"Output for {worker_name} verified successfully.")

            except OSError as e:
                print(f"Error accessing output file for {worker_name}: {e}", file=sys.stderr)
                verified_results[worker_name] = 'gap_read_error'

    # The runner can now decide how to proceed based on verified_results
    # e.g., only pass files from 'success' workers to the synthesizer.
    successful_drafts = [
        w['output_file'] for w in workers 
        if verified_results.get(w['name']) == 'success'
    ]
    
    print(f"
Proceeding to synthesis with drafts: {successful_drafts}")
    # ... logic to invoke orch-synthesizer with successful_drafts ...
    
    return verified_results

# results = run_worker_phase(models_to_run)
# final_status = verify_outputs(models_to_run, results)
# print("
Final Status:", final_status)
```

## Section 4: Risks and Edge Cases

1.  **Risk: Hung or Zombie Subprocesses.** A CLI tool might fail to terminate properly, consuming system resources. The `proc.terminate()` followed by `proc.kill()` mitigation is standard, but in complex parent/child process scenarios (common with CLIs that wrap other tools), child processes can be orphaned.
    *   **Mitigation:** On POSIX-like systems (including Git Bash), use `os.setsid` in the `Popen` call via the `preexec_fn` argument. This places the subprocess in a new process group. Then, you can kill the entire process group with `os.killpg(os.getpgid(proc.pid), signal.SIGKILL)`, ensuring all children are terminated. This is more robust than killing the parent PID alone.

2.  **Risk: Inconsistent CLI Output/Behavior.** The runner is a brittle integration point. A minor update to any of the managed CLIs (e.g., changing an argument, altering exit codes, new auth prompts) can break the runner.
    *   **Mitigation:** Implement a "conformance check" as part of the pre-flight. For each detected CLI, run a simple, non-destructive command like `claude --version`. This validates that the CLI is in the `PATH`, is executable, and returns a successful exit code before attempting complex prompts. All CLI command construction should be isolated in adapter functions to ease updates.

3.  **Risk: Race Conditions in File I/O.** While parallel processes write to dedicated files, the runner itself might read a file (e.g., a critique draft) while the model is still writing to it, leading to partial content reads.
    *   **Mitigation:** Implement a file-locking mechanism or a protocol where workers signal completion. A simple approach is for each worker to write its output to a temporary file (`draft.md.tmp`) and, upon successful completion, rename it to the final name (`draft.md`). The `os.rename` operation is atomic on most filesystems. The verifier module will only look for the final, non-`.tmp` filename.

## Section 5: Open Questions

1.  **Timeout Configuration:** What is the appropriate timeout duration for worker processes? Should this be a single global configuration value, or should it be configurable on a per-model or per-phase (draft vs. critique) basis?
2.  **Credential Management for API Fallback:** When a CLI is unavailable and the pre-flight check determines an API fallback is necessary, what is the defined mechanism for sourcing API keys? Will they be read from environment variables (e.g., `ANTHROPIC_API_KEY`), a central framework configuration file, or another source?
3.  **Detailed Synthesizer Contract:** What is the precise command-line interface for `orch-synthesizer`? Specifically, how should the list of draft files, critique files, and other contextual metadata be passed to it?
4.  **Retry Logic:** If a worker fails due to a transient error (e.g., a temporary network issue for an API-backed CLI), should the runner attempt a retry? If so, how many retries and with what backoff strategy?
