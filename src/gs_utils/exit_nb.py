from __future__ import annotations
import json

def nb_out(*, status: str, msg: str, extras: dict | None = None) -> None:
    """Exit the Fabric notebook with a structured JSON payload for pipelines."""
    import notebookutils  # type: ignore
    payload = {"status": status.lower(), "message": msg}
    if extras:
        payload.update(extras)
    notebookutils.notebook.exit(json.dumps(payload, ensure_ascii=False))
