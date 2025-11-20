# Quick start
### Download Latest .whl Directly From Github
```python
from pathlib import Path
import requests

dest_dir = Path("/lakehouse/default/Files/pkg") # or wherever you want to save it

# --- resolve latest wheel URL ---
api_url = f"https://api.github.com/repos/GraySinclair/gs-utils/releases/latest"
resp = requests.get(api_url, headers={"Accept": "application/vnd.github+json"})
resp.raise_for_status()
release = resp.json()

assets = release.get("assets", [])
asset = next((a for a in assets if a.get("name", "").endswith(".whl")), None)

if not asset: raise RuntimeError(f"No wheel asset found in latest release.")
url, filename = asset["browser_download_url"], asset["name"]

# creates the directory if missing
dest_dir.mkdir(parents=True, exist_ok=True) 
tmp_path = (dest_dir / filename).with_suffix(".part")

with requests.get(url, stream=True, allow_redirects=True) as r:
    r.raise_for_status()
    with tmp_path.open("wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

final_path = dest_dir / filename
tmp_path.replace(final_path)
print(f"Downloaded wheel to: {final_path}")
```

### For production pipeline runs:
    - Create an 'environment' item in the workspace. 
    - Add this .whl to the custom libraries tab. 
    - Ensure the environment is in published status.
    - Attach env to the notebook:
        - Home Tab > Environment > Change Environment

## API Functions & Usage:
### Import statement:
```python
import gs_utils as gs
```

### Bootstrapped Logger Setup With `gs.get_logger()`:
 - Timezone converted from server to local time. -ZoneInfo("America/Chicago")
 - Stream flush logs as they record instead of on cell completion.(Still logs in cases where raised exceptions prevent buffered logs from being flushed.)
```python
log = gs.get_logger(name="nb.nbname", level="info")
log.info("Hello World!")
```

### Access Azure Key Vault Secrets With `gs.get_secret()`:
 - Shortcut for notebookutils.credentials.get_secret()
```python
vault_url = "https://<yourvault>.vault.azure.net/"
secret1 = gs.get_secret(vault_url=vault_url, secret_name="your_secret")
```

### Standardize Parameter Access In Pipeline Post-Notebook Run With `gs.nb_out()`:
 - Access in your next pipeline activity with:
           `@json(activity('Notebook1').output.result.exitValue).status`
```python
your_dict = {
    "rows_written": 1532,
    "other_parameter": "lorem ipsum"
    }

# Gracefully exits notebook. Automatic passing of any included parameters.
gs.nb_out(status="success", msg="ETL Completed", extras=your_dict)

# ================ Output ================
exitValue = {
        "status":          "success",
        "msg":             "ETL complete",
        "rows_written":    1532,
        "other_parameter": "lorem ipsum"
        }
```
### Use `gs.get_enabled_tables()` to keep a living control panel at the top of your notebook:
- Useful when stakeholders ask for custom singular runs without having to alter/re-upload config files
    - Just set `is_enabled`, run for stakeholder, then reset to True
```python
control_panel = [
    {"table_name": "sponsors",           "is_enabled": True},
    {"table_name": "sessions",           "is_enabled": True},
    {"table_name": "sessionrecords",     "is_enabled": True},
    {"table_name": "programs",           "is_enabled": True},
    {"table_name": "people",             "is_enabled": True},
    {"table_name": "overallcompliance",  "is_enabled": True},
    {"table_name": "organizationpeople", "is_enabled": True},
    {"table_name": "jurisdictions",      "is_enabled": True},
    {"table_name": "jurisdictionpeople", "is_enabled": True},
]

tables_to_run = gs.get_enabled_tables(control_panel)
```
