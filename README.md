# Overview:
Name: 
    gs_utils\
Description: 
    Microsoft Fabric notebook helpers with **runtime validation**.


## Quick start (inside a Fabric notebook)
### Download & Install Wheel Directly From Github
```python
from pathlib import Path
import requests

# Direct link to the wheel asset(adjust versioning)
url = "https://github.com/GraySinclair/gs-utils/releases/download/v0.2.5/gs_utils-0.2.5-py3-none-any.whl"

# Target directory inside the Lakehouse Files mount
dest_dir = Path("/lakehouse/default/Files/pkg")
dest_dir.mkdir(parents=True, exist_ok=True)

# Final destination path
dest_path = dest_dir / Path(url).name

# Stream download (follows redirects and saves binary data)
headers = {"Accept": "application/octet-stream"}
with requests.get(url, headers=headers, stream=True, allow_redirects=True, timeout=60) as r:
    r.raise_for_status()
    with dest_path.open("wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

print(f"Downloaded wheel to: {dest_path}")

# Optional: install the wheel immediately
import sys, subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", str(dest_path), "--upgrade"])
```
## API Functions & Usage:
### Import statement:
```python
import gs_utils as gs
```

### Bootstrapped Logger Setup With `_configure_logger()`:
 - Timezone converted from server to local time. -ZoneInfo("America/Chicago")
 - Stream flush logs as they record instead of on cell completion.(Still logs in cases where raised exceptions prevent buffered logs from being flushed.)
```python
logger = gs.config_logger(name="nb.nbname", level="info")
logger.info("Notebook starting up...")
```

### Access Azure Key Vault Secrets With `get_secret()`:
```python
akv_url = "https://<yourvault>.vault.azure.net/"
token = gs.get_secret(vault_url=akv_url, name="your_secret")
```

### Standardize Parameter Access In Pipeline Post-Notebook Run With `nb_out()`:
```python
out_details = {
    "rows_written": 1532,
    "other_parameter": "lorem ipsum"
    }
# Gracefully exits notebook. Automatic passing of any included parameters.
gs.nb_out(status="success", msg="ETL Completed", extras=out_details) 
```
