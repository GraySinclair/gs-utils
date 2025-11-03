from __future__ import annotations

def _require_fabric(msg: str | None = None) -> None:
    """Assert we are running inside Microsoft Fabric by checking for `notebookutils`."""
    try:
        import notebookutils  # type: ignore
    except Exception as exc:
        raise ImportError(msg or "This feature requires Microsoft Fabric (`notebookutils` not found).") from exc
