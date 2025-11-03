"""gs_utils: Fabric helpers (secrets, structured exits, logging presets).

This package provides:
- get_secret(vault_url, secret_name): fetch AKV secrets via Fabric identity
- nb_out(status, msg, extras=None): notebook exit with structured JSON payload.
- config_logger(name, level): opinionated logger preset for notebooks/pipelines
"""

from .secrets import get_secret
from .exit_nb import nb_out
from .get_logger import config_logger

__all__ = ["get_secret", "nb_out", "config_logger"]
