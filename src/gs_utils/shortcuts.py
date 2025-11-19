
def load_cfg(path: str, maxbytes: int = 102400) -> dict:
    """
    Load a small JSON config (single dict) from OneLake.

    Args:
        path: FileSystem URI (abfss://... or 'Files/...' etc.).
        max_bytes: Safety cap for how many bytes to read.

    Returns:
        Parsed JSON as a Python dict.
    """
    import notebookutils # type: ignore
    import json # type: ignore
    raw = notebookutils.fs.head(path, max_bytes=maxbytes)
    return json.loads(raw)

def is_automated_run() -> bool:
    """Return True if executed from a pipeline activity."""
    import notebookutils  # type: ignore
    return notebookutils.runtime.context.get("isForPipeline")
