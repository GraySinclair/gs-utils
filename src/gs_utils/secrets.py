from __future__ import annotations

def get_secret(vault_url: str, name: str) -> str:
    """
    Fetch a secret from Azure Key Vault using Fabric's workspace identity. Returns the string value or raises RuntimeError if missing/empty.
    """
    import notebookutils  # type: ignore
    value = notebookutils.credentials.getSecret(vault_url, name)
    if not value:
        raise RuntimeError(f"Secret '{name}' not found or empty at '{vault_url}'.")
    return value
