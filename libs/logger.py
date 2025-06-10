import logging
from typing import Union

import coloredlogs
from typeguard import typechecked


@typechecked
def configure_logging(log_level: Union[int, str] = logging.INFO) -> None:
    """
    Configure logging with colores output.
    """

    # the log format
    log_format = "%(asctime)s [%(levelname)8s] %(name)s:%(lineno)d (%(process)d/%(threadName)s) - %(message)s"

    # hide matplotlib
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("httpcore.connection").setLevel(logging.WARNING)
    logging.getLogger("httpcore.http11").setLevel(logging.WARNING)
    logging.getLogger("openai._base_client").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("peewee").setLevel(logging.WARNING)

    coloredlogs.install(
        level=log_level,
        fmt=log_format,
        level_styles={
            "DEBUG": {"color": "cyan"},
            "INFO": {"color": "green"},
            "WARNING": {"color": "yellow"},
            "ERROR": {"color": "red"},
            "CRITICAL": {"color": "red", "bold": True, "background": "white"},
        },
        field_styles={
            "asctime": {"color": "white"},
            "levelname": {"bold": True},
            "name": {"color": "blue", "bold": True},
            "lineno": {"color": "magenta"},
            "process": {"color": "green"},
            "threadName": {"color": "yellow"},
            "message": {"color": "white"},
        },
        milliseconds=True,
    )
