import logging
import logging.handlers

from src.utils.util import get_config


def setup_logger(logger_name, log_file, rotate=False, stream=True):
    data = get_config("config.yaml")

    log = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
    )

    if rotate:
        file_handler = logging.handlers.RotatingFileHandler(
            r".\logs\\{}".format(log_file), mode="w", maxBytes=1 * 1024 * 1024, backupCount=3
        )
    else:
        file_handler = logging.FileHandler(r".\logs\\{}".format(log_file), mode="w")

    file_handler.setFormatter(formatter)

    level = getattr(logging, data["log_level"])
    log.setLevel(level)
    log.addHandler(file_handler)

    if stream:
        formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)
