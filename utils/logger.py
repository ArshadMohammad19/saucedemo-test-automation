"""
Custom logger used across the framework.

Writes to both console and a rotating log file under logs/, so CI runs
leave a persistent artifact and local runs still get console feedback.
"""
import logging
import sys
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        # Avoid duplicate handlers if get_logger is called multiple times
        # for the same module (e.g. re-imports during test collection).
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(LOG_DIR / "test_run.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
