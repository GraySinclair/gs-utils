from __future__ import annotations

def get_secret(vault_url: str, secret_name: str) -> str:
    """
    Retrieve a secret from Azure Key Vault using Fabric-managed identity.

    Args:
        vault_url: The full Key Vault URL, e.g. "https://myvault.vault.azure.net/"
        secret_name: The secret name to retrieve.

    Returns:
        The secret value as a string.
    """
    import notebookutils  # type: ignore
    value = notebookutils.credentials.getSecret(vault_url, name)
    if not value:
        raise RuntimeError(f"Secret '{name}' not found or empty at '{vault_url}'.")
    return value
