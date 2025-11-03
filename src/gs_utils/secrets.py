from __future__ import annotations
from .runtime import require_fabric

def get_secret(vault_url: str, name: str) -> str:
    """Fetch a secret from Azure Key Vault using Fabric's workspace identity.

    Returns the string value or raises RuntimeError if missing/empty.
    """
    require_fabric("get_secret requires Fabric; `notebookutils` is unavailable.")
    import notebookutils  # type: ignore
    value = notebookutils.credentials.getSecret(vault_url, name)
    if not value:
        raise RuntimeError(f"Secret '{name}' not found or empty at '{vault_url}'.")
    return value
