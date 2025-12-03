"""
gs_utils: Fabric helpers (secrets, structured exits, logging presets).

This package provides:
- get_secret(vault_url, secret_name): fetch AKV secrets via Fabric identity
- nb_out(status, msg, extras=None): notebook exit with structured JSON payload.
- config_logger(name, level): opinionated logger preset for notebooks/pipelines
- is_automated_run(): returns bool-- checks if your notebook is running from a pipeline or manually being run
- load_cfg(path, maxbytes): loads json; returns dict
"""

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("gs-utils")
except PackageNotFoundError:
    __version__ = "0.0.0"

from .secrets import get_secret, nb_out, get_logger
from .shortcuts import is_automated_run, load_cfg, get_enabled_tables
from .get_monthly_data import month_to_gte_lt


__all__ = ["get_secret", "nb_out", "get_logger", "is_automated_run", "load_cfg", "get_enabled_tables", "month_to_gte_lt"]
