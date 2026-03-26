# Learn to secure proxy credentials by storing them in macOS Keychain

> By the end of this tutorial you will have a DigitalOcean API key stored in
> macOS Keychain, verified via the `credentials_check_command`, visible in
> Keychain Access.app, and ready for the engage pipeline to use without any
> environment variable.

## What You Will Achieve

By the end of this tutorial, you will have:

- A DigitalOcean API key stored as an encrypted macOS Keychain item named
  `jerry-proxy / digitalocean`
- Confirmed that `credentials_check_command` reports `found=True, source="keychain"`
- Seen the keychain entry in Keychain Access.app
- Run `engage_command` with the stored credential (no env var required)
- Rotated the credential by deleting and re-storing it
- Cleaned up the test entry so your keychain is left tidy

## Prerequisites

Before starting, you need:

- macOS (Ventura 13 or later). The `keyring` library targets the macOS
  Security framework on this platform.
- Python environment prepared with `uv sync` run at the repo root. This
  installs the `keyring` package declared in `pyproject.toml`.
- A DigitalOcean account with permission to generate personal access tokens.
- The repo checked out and your working directory set to the repo root.

## Steps

### 1. Generate a DigitalOcean API key

Open your browser and navigate to the DigitalOcean control panel:

```
https://cloud.digitalocean.com/account/api/tokens
```

Click **Generate New Token**. Give it a name (for example `jerry-test`),
select **Read** and **Write** scopes, then click **Generate Token**.

Copy the token value. It starts with `dop_v1_`. This is the only time the
value is shown in plain text.

**Expected result:** You have a token string starting with `dop_v1_` copied
to your clipboard.

### 2. Open an interactive Python session

From the repo root, start the Python interpreter inside the project
environment:

```bash
uv run python
```

**Expected result:** The Python REPL prompt appears:

```
Python 3.11.x ...
>>>
```

### 3. Store the API key in macOS Keychain

At the Python prompt, run the following two lines. Replace
`dop_v1_YOUR_TOKEN_HERE` with the token you copied in step 1:

```python
from src.proxy_infra.interface.cli.proxy_commands import credentials_set_command
credentials_set_command("digitalocean", "dop_v1_YOUR_TOKEN_HERE")
```

macOS will display a permission dialog the first time a new service name
(`jerry-proxy`) is written to Keychain. Click **Always Allow** to let the
Python process write to Keychain without prompting on future calls.

**Expected result:** The function returns `None` with no output. No
exception is raised. The macOS permission dialog disappears after you
click **Always Allow**.

### 4. Verify the credential is stored

Run the check command at the same Python prompt:

```python
from src.proxy_infra.interface.cli.proxy_commands import credentials_check_command
result = credentials_check_command("digitalocean")
print(result)
```

**Expected result:**

```
CredentialCheckResult(found=True, provider='digitalocean', source='keychain')
```

`found=True` confirms the entry exists. `source='keychain'` confirms it was
read from macOS Keychain, not from an environment variable.

### 5. View the entry in Keychain Access.app

Open Keychain Access from Spotlight (`Cmd+Space`, type `Keychain Access`,
press `Return`).

In the search bar at the top right, type `jerry-proxy`.

**Expected result:** One item appears:

| Name | Kind | Keychain |
|------|------|----------|
| jerry-proxy | application password | login |

Double-click the entry. In the detail panel you will see:

- **Name:** `jerry-proxy`
- **Account:** `digitalocean`
- **Where:** `jerry-proxy`

Click **Show password** and authenticate with your login password or Touch
ID. The stored API key value appears.

Close the detail panel. Your key is encrypted at rest by the macOS Security
framework and protected by your login credentials and, when configured, by
Touch ID.

### 6. Run engage_command with the stored credential

The `engage_command` function provisions proxy infrastructure using the
adapter's `from_env()` factory. The `KeyringCredentialStore` is the adapter
used when the environment variable is absent.

At the Python prompt, confirm that `credentials_check_command` would supply
the credential to an adapter without needing an env var:

```python
# Simulate what engage_command does internally: retrieve without env var
from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
    KeyringCredentialStore,
)

store = KeyringCredentialStore()
key = store.get_credential("digitalocean")
print(f"Retrieved {len(key)} character key starting with {key[:10]}...")
```

**Expected result:**

```
Retrieved 71 character key starting with dop_v1_abc...
```

The character count reflects the length of your specific token (DigitalOcean
`dop_v1_` tokens are typically 71 characters). The full value is not printed.
This confirms the engage pipeline can retrieve the credential from Keychain
without any `JERRY_PROXY_DIGITALOCEAN_API_KEY` environment variable present.

### 7. Rotate the credential

Rotating a credential means removing the old key and storing a new one.
Generate a new token in the DigitalOcean control panel (step 1 again) and
then run:

```python
from src.proxy_infra.interface.cli.proxy_commands import (
    credentials_delete_command,
    credentials_set_command,
)

# Delete the old entry
deleted = credentials_delete_command("digitalocean")
print(f"Old credential deleted: {deleted}")

# Store the new entry
credentials_set_command("digitalocean", "dop_v1_YOUR_NEW_TOKEN_HERE")
print("New credential stored.")
```

**Expected result:**

```
Old credential deleted: True
New credential stored.
```

`True` confirms the old entry was found and removed. The new entry is now
in Keychain.

### 8. Clean up the test credential

Remove the credential you stored during this tutorial so your Keychain is
left in the state it was before you started:

```python
from src.proxy_infra.interface.cli.proxy_commands import credentials_delete_command

deleted = credentials_delete_command("digitalocean")
print(f"Test credential removed: {deleted}")
```

**Expected result:**

```
Test credential removed: True
```

Return to Keychain Access.app and search `jerry-proxy` again. No items
appear. The entry is gone.

## Security notes

The following properties apply once a credential is stored via this tutorial:

- The API key is encrypted at rest by the macOS Security framework
  (AES-256-CBC with a key derived from your login password).
- Touch ID authentication is required to show or export the value when your
  system security settings are configured for it.
- The key never appears in environment variables, process arguments, shell
  history, or log files. The `KeyringCredentialStore` implementation does not
  pass credential values to any logging call.
- In CI or Docker environments where an OS keychain is unavailable, the
  `EnvCredentialStore` reads credentials from the environment variable
  `JERRY_PROXY_DIGITALOCEAN_API_KEY`. The keychain tier and the environment
  variable tier are independent; setting one does not affect the other.

## What You Learned

You now know how to:

- Create a scoped DigitalOcean personal access token in the control panel
- Store a cloud provider API key using `credentials_set_command("digitalocean", key)`
- Confirm storage using `credentials_check_command("digitalocean")` and reading
  `result.found` and `result.source`
- Locate the keychain entry in Keychain Access.app under the service name
  `jerry-proxy`
- Retrieve credentials programmatically using `KeyringCredentialStore.get_credential`
- Rotate a credential using `credentials_delete_command` followed by
  `credentials_set_command`
- Clean up test credentials after a session

## Related

- **How-To Guide:** See `docs/howto/` for task-oriented guides on running
  `engage_command` against a live engagement config
- **Reference:** `src/proxy_infra/infrastructure/credentials/keyring_credential_store.py`
  — full `KeyringCredentialStore` API including `SERVICE_NAME` constant and
  all port methods
- **Reference:** `src/proxy_infra/infrastructure/adapters/env_credential_store.py`
  — `EnvCredentialStore` API and environment variable naming convention
  (`JERRY_PROXY_{PROVIDER}_API_KEY`)
- **Explanation:** `docs/explanation/` for the design rationale behind the
  two-tier credential storage model (ADR-PROJ023-008)
