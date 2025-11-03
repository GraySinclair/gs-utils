import logging
from datetime import datetime
from zoneinfo import ZoneInfo

class CentralTimeFormatter(logging.Formatter):
    """Formatter that forces Central Time (DST-aware)."""
    def formatTime(self, record, datefmt=None):
        local_dt = datetime.fromtimestamp(record.created, tz=ZoneInfo("America/Chicago"))
        return local_dt.strftime(datefmt or "%Y-%m-%d %H:%M:%S %Z")

class FlushStreamHandler(logging.StreamHandler):
    """StreamHandler that flushes immediately after each record."""
    def emit(self, record):
        super().emit(record)
        self.flush()

def config_logger(name: str, level: str | int = logging.INFO) -> logging.Logger:
    """
    Return configured logger.
    
    Args:
        name:  Logger name.
        level: Log level, either string (e.g. "DEBUG") or numeric constant.
    """
    # Resolve string levels like "debug" -> logging.DEBUG
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not any(isinstance(h, FlushStreamHandler) for h in logger.handlers):
        h = FlushStreamHandler()
        h.setFormatter(CentralTimeFormatter("[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"))
        logger.addHandler(h)

    logger.propagate = False
    return logger
