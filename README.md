# gs-utils

Helpers for Microsoft Fabric notebooks with **runtime validation** and a single-call **`setup()`** to bootstrap logging, Spark, and Key Vault secrets.

## Quick start (inside a Fabric notebook)

```python
%pip install --upgrade build

import os, subprocess, sys
os.chdir("/lakehouse/default/Files/dev/gs-utils")  # adjust

subprocess.run([sys.executable, "-m", "build", "--wheel"], check=True)
%pip install ./dist/gs_utils-0.2.0-py3-none-any.whl --force-reinstall

from gs_utils import setup, nb_exit, get_secret

ctx = setup(
    logger_name="nb.gs",
    log_level="INFO",
    kv_url="https://<kv>.vault.azure.net/",
    secret_names=["INTACCT_SENDERID", "INTACCT_CLIENT_ID"],
    require_spark=False,   # set True if your code assumes Spark
)

ctx.logger.info("All set", extra={"secrets_loaded": list(ctx.secrets)})
# nb_exit(status="success", msg="Ready", extras={"rows_written": 123})
```

## What `setup()` does

- Validates Fabric runtime (lazy import of `notebookutils`).
- Configures a structured console logger.
- Optionally fetches a list of AKV secrets via `notebookutils.credentials.getSecret`.
- Optionally ensures a Spark session handle is returned (does not auto-create a new session).
- Returns a frozen dataclass `SetupContext` with handy attributes.
