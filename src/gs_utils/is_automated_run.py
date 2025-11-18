
def is_automated_run() -> bool:
    """Return True if executed from a pipeline activity."""
    import notebookutils  # type: ignore
    return notebookutils.runtime.context.get("isForPipeline")
