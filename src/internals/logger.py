"""
This module auto initialises a Logger and assign it to `genie_logger` variable.
`genie_logger` will be imported within other modules that need to log.

Usage:

from internals.logger import genie_logger

genie_logger.debug("CommandGenie logger is loaded")

"""
import logging
from logging.handlers import RotatingFileHandler
from internals.provider_log_path import LogPathProvider
from internals.shell_args import CliArgs
import coloredlogs


class Settings:
    """Internally used.
    Holds settings of the logger
    """

    log_format = (
        "%(asctime)s :: %(levelname)s :: %(message)s :: %(filename)s, %(funcName)s, line %(lineno)d "  # noqa: E501
    )
    log_file_path = LogPathProvider(create_path=True).get_path() / "commandgenie.log"


def _get_logger() -> logging.Logger:
    """Internally used function.
    Initialise the logger and returns it.

    The logger outputs to file and when requested by the --verbose flag to std out/std error.

    Returns:
        Logger: an initialised logger.
    """
    level = logging.DEBUG if CliArgs.VERBOSE else logging.INFO
    proj_logger = logging.getLogger("genie_logger")
    proj_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(Settings.log_format, datefmt="%Y-%m-%d,%H:%M:%S")

    file_path = Settings.log_file_path
    one_megabyte = 2**20  # roughly
    file_handler = RotatingFileHandler(file_path, backupCount=10, maxBytes=one_megabyte)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    proj_logger.addHandler(file_handler)
    coloredlogs.install(level=level, logger=proj_logger, fmt=Settings.log_format)

    return proj_logger


# Auto initialised logger, to be imported in other modules and be used to log.
genie_logger = _get_logger()
