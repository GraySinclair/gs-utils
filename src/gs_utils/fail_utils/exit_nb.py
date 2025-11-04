from __future__ import annotations
import json
from .logging_utils import get_logger

log = get_logger(name="nb.exit",level="INFO")

def nb_out(*, status: str, msg: str , extras: dict | None = None) -> None:
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
    import notebookutils  # type: ignore
    payload = {"status": status.lower(), "msg": msg}

    if extras:
        payload.update(extras)
    log.debug(payload)
    
    # notebookutils.notebook.exit(json.dumps(payload, ensure_ascii=False))
    notebookutils.notebook.exit(payload)

__all__ = ["nb_out", "get_logger"]
