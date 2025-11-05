# Quick start (Inside a Fabric notebook)
### Download & Install Latest .whl Directly From Github
```python
from pathlib import Path
import requests

# --- config ---
repo = "GraySinclair/gs-utils"
dest_dir = Path("/lakehouse/default/Files/pkg") # or wherever you want to save it

# --- resolve latest wheel URL ---
api_url = f"https://api.github.com/repos/{repo}/releases/latest"
resp = requests.get(api_url, headers={"Accept": "application/vnd.github+json"}, timeout=(10, 120))
resp.raise_for_status()
release = resp.json()

assets = release.get("assets", [])
asset = next((a for a in assets if a.get("name", "").endswith(".whl")), None)
if not asset:
    raise RuntimeError(f"No wheel asset found in latest release of {repo}.")

url = asset["browser_download_url"]
filename = asset["name"]

# --- download atomically ---
dest_dir.mkdir(parents=True, exist_ok=True) # creates the directory if missing
tmp_path = (dest_dir / filename).with_suffix(".part")

with requests.get(url, stream=True, allow_redirects=True, timeout=timeout) as r:
    r.raise_for_status()
    with tmp_path.open("wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

tmp_path.replace(dest_path)
print(f"Downloaded wheel to: {dest_path}")
```
- Ensure you copy the link from the wheel in your lakehouse files prior to running the below
### Install via PIP(In-line) 
- This only works in interactive runs for testing.
- For production/automated pipeline runs:
    - Create an 'environment' item in the workspace. 
    - Add this .whl to the custom libraries tab. 
    - Ensure the environment is in published status.
    - Attach env to the notebook: At the top of your notebook--
    -     Home Tab > Environment > Change Environment
```python
%pip install /lakehouse/default/Files/pkg/gs_utils-0.3.2-py3-none-any.whl
```
## API Functions & Usage:
### Import statement:
```python
import gs_utils as gs
```

### Bootstrapped Logger Setup With `get_logger()`:
 - Timezone converted from server to local time. -ZoneInfo("America/Chicago")
 - Stream flush logs as they record instead of on cell completion.(Still logs in cases where raised exceptions prevent buffered logs from being flushed.)
```python
log = gs.get_logger(name="nb.nbname", level="info")
log.info("Hello World!")
```

### Access Azure Key Vault Secrets With `get_secret()`:
 - Self-redacted secrets. Prevents accidental logging.
```python
vault_url = "https://<yourvault>.vault.azure.net/"
secret1 = gs.get_secret(vault_url=vault_url, secret_name="your_secret")
```

### Standardize Parameter Access In Pipeline Post-Notebook Run With `nb_out()`:
 - Access in your next pipeline activity with `@json(activity('Notebook1').output.result.exitValue).status`
```python
your_dict = {
    "rows_written": 1532,
    "other_parameter": "lorem ipsum"
    }

# Gracefully exits notebook. Automatic passing of any included parameters.
gs.nb_out(status="success", msg="ETL Completed", extras=your_dict)
```
