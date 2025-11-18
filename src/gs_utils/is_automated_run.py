
def is_automated_run() -> bool:
    """Return True if executed from a pipeline activity."""
    import notebookutils # Type: Ignore
    return notebookutils.runtime.context.get("isForPipeline")
