from __future__ import annotations
import json
from .runtime import require_fabric

def nb_out(*, status: str, msg: str, extras: dict | None = None) -> None:
    """Exit the Fabric notebook with a structured JSON payload for pipelines."""
    require_fabric("nb_exit requires Fabric notebooks.")
    import notebookutils  # type: ignore
    payload = {"status": status.lower(), "message": msg}
    if extras:
        payload.update(extras)
    notebookutils.notebook.exit(json.dumps(payload, ensure_ascii=False))
