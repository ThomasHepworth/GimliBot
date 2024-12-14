import logging
import os
from typing import Union

# Define log format and log level
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL: Union[int, str] = os.getenv("LOG_LEVEL", "INFO").upper()
# LOG_LEVEL: Union[int, str] = os.getenv("LOG_LEVEL", "DEBUG").upper()


def _validate_log_level(log_level: Union[int, str]) -> Union[int, str]:
    if not isinstance(log_level, (int, str)):
        raise ValueError(
            f"Invalid log level type: {log_level}:{type(log_level)}. Must be str or int."
        )

    if not (log_level in logging._nameToLevel or log_level in logging._levelToName):
        valid_levels = ", ".join(logging._nameToLevel.keys())
        raise ValueError(
            f"Invalid log level: '{log_level}'. Must be one of {valid_levels}."
        )

    return log_level


def setup_root_logger() -> None:
    """
    Configures the root logger with the specified log level and format.
    This function should be called once at the beginning of your application.
    """
    _validate_log_level(LOG_LEVEL)

    # Setup the root logger configuration - this should be sufficient for this application
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler()],  # Console output
    )

    logging.info(
        f"Root logger has been set up with:\n\t- {LOG_LEVEL=}\n\t- {LOG_FORMAT=}"
    )
