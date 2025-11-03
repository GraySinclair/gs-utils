from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, Optional, Iterable

from .runtime import require_fabric
from .secrets import get_secret

@dataclass(frozen=True, slots=True)
class SetupContext:
    """Return object from :func:`setup` with handy handles and values.

    Attributes
    ----------
    logger : logging.Logger
        Configured logger.
    secrets : Dict[str, str]
        Secret name -> value map fetched from Key Vault (may be empty).
    spark : Optional[object]
        Active SparkSession (if available/required), else ``None``.
    """
    logger: logging.Logger
    secrets: Dict[str, str] = field(default_factory=dict)
    spark: Optional[object] = None

def _configure_logger(name: str, level: str) -> logging.Logger:
    logger = logging.getLogger(name)
    # Idempotent: avoid duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S"
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.setLevel(level.upper())
    return logger

def setup(
    *,
    logger_name: str = "nb.gs",
    log_level: str = "INFO",
    kv_url: Optional[str] = None,
    secret_names: Optional[Iterable[str]] = None,
    require_spark: bool = False,
) -> SetupContext:
    """One-call bootstrap for Fabric notebooks.

    Parameters
    ----------
    logger_name : str
        Name for the root logger of this notebook/session.
    log_level : str
        Logging level (e.g., "INFO", "DEBUG").
    kv_url : str | None
        Azure Key Vault URL. If provided with `secret_names`, secrets are fetched.
    secret_names : Iterable[str] | None
        Iterable of secret names to fetch.
    require_spark : bool
        If True, ensure a SparkSession is active and return it on the context.
        If False, return spark handle when available but do not fail if missing.

    Returns
    -------
    SetupContext
        Frozen dataclass with `logger`, `secrets`, `spark`.

    Raises
    ------
    ImportError
        If called outside Fabric environment.
    RuntimeError
        If `require_spark=True` but no active SparkSession.
    """
    # Verify Fabric presence early
    require_fabric("setup() requires Microsoft Fabric.")

    # Configure logger
    logger = _configure_logger(logger_name, log_level)
    logger.debug("Logger configured", extra={"logger_name": logger_name, "level": log_level})

    # Optionally pick up Spark
    spark = None
    try:
        from pyspark.sql import SparkSession  # type: ignore
        spark = SparkSession.getActiveSession()
        if require_spark and spark is None:
            raise RuntimeError("No active SparkSession. Start a Spark session or set require_spark=False.")
        if spark is not None:
            logger.debug("Spark session detected")
    except Exception as exc:
        if require_spark:
            raise
        logger.debug("Spark not available", extra={"error": str(exc)})

    # Optionally fetch secrets
    secrets: Dict[str, str] = {}
    if kv_url and secret_names:
        for name in secret_names:
            secrets[name] = get_secret(kv_url, name)

    return SetupContext(logger=logger, secrets=secrets, spark=spark)
