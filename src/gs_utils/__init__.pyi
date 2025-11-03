def get_secret(vault_url: str, secret_name: str) -> str:
    """
    Retrieve a secret from Azure Key Vault using Fabric-managed identity.

    Args:
        vault_url: The full Key Vault URL, e.g. "https://myvault.vault.azure.net/"
        secret_name: The secret name to retrieve.

    Returns:
        The secret value as a string.
    """
    ...

def nb_out(*, status: str, msg: str, extras: dict | None = None) -> None:
    """
    Exit the Fabric notebook with a structured JSON payload for pipelines.

    Args:
        status: Short status keyword such as "success", "failure", or "default".
        msg: Human-readable message describing the outcome or context.
        extras: Optional dictionary of additional key-value pairs to include at the top level of the JSON payload.
    
    Example:
        ```python
        import gs_utils as gs

        gs.nb_out(
                status="success",
                msg="ETL complete",
                extras={"rows_written": 1523, "duration_s": 18.4},
            )
        ```
    """
    ...

from logging import Logger
def config_logger(name: str, level: int | str = ...) -> Logger:
    """
    Return configured logger.
    
    Args:
        name:  Logger name.
        level: Log level, either string (e.g. "DEBUG") or numeric constant.
    """
    ...
