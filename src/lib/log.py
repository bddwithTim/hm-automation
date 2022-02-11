import logging
import logging.handlers
import os

from src.utils.utils import get_config


def setup_logger(logger_name, log_file, rotate=False, stream=True):
    config = get_config("config.yaml")
    log_directory = config["directory"]["logs"]

    if not os.path.exists(log_directory):
        os.mkdir(log_directory)

    log = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
    )

    if rotate:
        file_handler = logging.handlers.RotatingFileHandler(
            f"{log_directory}\\{log_file}", mode="w", maxBytes=1 * 1024 * 1024, backupCount=3
        )
    else:
        file_handler = logging.FileHandler(f"{log_directory}\\{log_file}", mode="w")

    file_handler.setFormatter(formatter)

    level = getattr(logging, config["log_level"])
    log.setLevel(level)
    log.addHandler(file_handler)

    if stream:
        formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)
