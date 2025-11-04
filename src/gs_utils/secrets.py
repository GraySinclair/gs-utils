from __future__ import annotations
from .fail_utils import nb_out, get_logger

log = get_logger(name="nb.secrets",level="INFO")

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
    try:
        value = notebookutils.credentials.getSecret(vault_url, secret_name)
        log.info(f"Secret '{secret_name}' returned from vault.")
    except:
        _msg = f"Secret '{secret_name}' not found or empty at '{vault_url}'."
        log.critical(_msg)
        nb_out(status="failed", msg=_msg)
    return value

__all__ = ["get_secret", "nb_out", "get_logger"]