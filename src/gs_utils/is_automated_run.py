import os

def is_automated_run() -> bool:
    """Return True if executed from a pipeline activity."""
    return "FABRIC_JOB_RUN_ID" in os.environ or "PIPELINE_RUN_ID" in os.environ

if __name__ == "__main__":
  if is_automated_run():
      print("Running in pipeline")
  else:
      print("Running interactively")
